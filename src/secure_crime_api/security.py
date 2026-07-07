from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from secure_crime_api.config import Settings
from secure_crime_api.models import AuthenticatedUser, UserPublic


password_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=64 * 1024,
    parallelism=2,
    hash_len=32,
    salt_len=16,
)


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return password_hasher.verify(password_hash, password)
    except VerifyMismatchError:
        return False
    except Exception:
        return False


def password_needs_rehash(password_hash: str) -> bool:
    return password_hasher.check_needs_rehash(password_hash)


def create_access_token(user: UserPublic, settings: Settings) -> tuple[str, datetime, str]:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=settings.token_ttl_minutes)
    jti = str(uuid.uuid4())
    payload: dict[str, Any] = {
        "iss": settings.jwt_issuer,
        "sub": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "role": user.role,
        "district": user.district,
        "jti": jti,
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
    return token, expires_at, jti


def decode_access_token(token: str, settings: Settings) -> AuthenticatedUser:
    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=["HS256"],
        issuer=settings.jwt_issuer,
        options={"require": ["exp", "iat", "iss", "sub", "jti"]},
    )
    return AuthenticatedUser(
        id=str(payload["sub"]),
        username=str(payload["username"]),
        full_name=str(payload["full_name"]),
        role=payload["role"],
        district=str(payload["district"]),
        jti=str(payload["jti"]),
    )
