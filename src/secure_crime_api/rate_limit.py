from __future__ import annotations

import time
from collections import defaultdict, deque
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from fastapi import Request, Response
from jwt import InvalidTokenError
from starlette.middleware.base import BaseHTTPMiddleware

from secure_crime_api.audit import write_audit_log
from secure_crime_api.models import AuthenticatedUser
from secure_crime_api.security import decode_access_token


@dataclass(frozen=True)
class RateLimitActor:
    user: AuthenticatedUser | None
    identity: str

class InMemoryRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.window_seconds = 60
        self.alert_cooldown_seconds = 60
        self.clients: dict[str, deque[float]] = defaultdict(deque)
        self.last_alert_at: dict[str, float] = {}
        self.blocked_unauthenticated_clients: dict[str, float] = {}

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        if self._is_non_api_asset(request.url.path):
            return await call_next(request)

        client = request.client.host if request.client else "unknown"
        actor = self._actor_from_request(request, client)
        now = time.monotonic()
        if actor.user is None:
            blocked_until = self.blocked_unauthenticated_clients.get(client, 0)
            if now < blocked_until:
                retry_after = max(1, int(blocked_until - now))
                self._record_breach(request, actor, client, f"ip:{client}:unauthenticated", self.requests_per_minute + 1, now)
                return self._rate_limited_response(retry_after, "Unauthenticated device or IP temporarily blocked")
            key = f"{actor.identity}:unauthenticated:any-api"
        else:
            key = f"{actor.identity}:{request.method}:{request.url.path}"
        bucket = self.clients[key]
        while bucket and now - bucket[0] > self.window_seconds:
            bucket.popleft()

        if len(bucket) >= self.requests_per_minute:
            if actor.user is None:
                self.blocked_unauthenticated_clients[client] = now + self.window_seconds
            self._record_breach(request, actor, client, key, len(bucket) + 1, now)
            return self._rate_limited_response(self.window_seconds, "Rate limit exceeded")

        bucket.append(now)
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(max(0, self.requests_per_minute - len(bucket)))
        response.headers["X-RateLimit-Reset"] = str(self.window_seconds)
        return response

    def _is_non_api_asset(self, path: str) -> bool:
        return path == "/" or path.startswith("/static/")

    def _rate_limited_response(self, retry_after: int, message: str) -> Response:
        return Response(
            content=f'{{"detail":"{message}"}}',
            status_code=429,
            media_type="application/json",
            headers={
                "Retry-After": str(retry_after),
                "X-RateLimit-Limit": str(self.requests_per_minute),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(retry_after),
            },
        )

    def _actor_from_request(self, request: Request, client: str) -> RateLimitActor:
        authorization = request.headers.get("authorization", "")
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer" or not token:
            return RateLimitActor(user=None, identity=f"ip:{client}")

        try:
            settings = request.app.state.settings
            db = request.app.state.db
            user = decode_access_token(token, settings)
            stored = db.get_user_by_id(user.id)
            if not stored:
                return RateLimitActor(user=None, identity=f"ip:{client}")
            return RateLimitActor(user=user, identity=f"user:{user.id}")
        except (AttributeError, InvalidTokenError, ValueError):
            return RateLimitActor(user=None, identity=f"ip:{client}")

    def _record_breach(
        self,
        request: Request,
        actor: RateLimitActor,
        client: str,
        key: str,
        request_count: int,
        now: float,
    ) -> None:
        if now - self.last_alert_at.get(key, 0) < self.alert_cooldown_seconds:
            return
        self.last_alert_at[key] = now

        try:
            db = request.app.state.db
            db.create_rate_limit_alert(
                actor_user_id=actor.user.id if actor.user else None,
                actor_username=actor.user.username if actor.user else None,
                actor_role=actor.user.role if actor.user else None,
                client_ip=client,
                method=request.method,
                path=request.url.path,
                limit_per_minute=self.requests_per_minute,
                window_seconds=self.window_seconds,
                request_count=request_count,
                request_id=getattr(request.state, "request_id", None),
            )
            write_audit_log(
                db,
                action="RATE_LIMIT_BREACH",
                resource_type="rate_limit",
                resource_id=request.url.path,
                status="DENIED",
                request=request,
                user=actor.user,
                detail={
                    "client_ip": client,
                    "method": request.method,
                    "path": request.url.path,
                    "limit_per_minute": self.requests_per_minute,
                    "request_count": request_count,
                },
            )
        except Exception:
            # A limiter must continue protecting the API even if alert persistence is unavailable.
            return
