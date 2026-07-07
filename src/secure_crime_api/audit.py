from __future__ import annotations

import hashlib
import json
from typing import Any

from fastapi import Request

from secure_crime_api.models import AuthenticatedUser
from secure_crime_api.storage import Database, utc_now_iso


def _canonical_entry(entry: dict[str, Any]) -> str:
    return json.dumps(entry, sort_keys=True, separators=(",", ":"), default=str)


def compute_entry_hash(entry: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_entry(entry).encode("utf-8")).hexdigest()


def write_audit_log(
    db: Database,
    *,
    action: str,
    resource_type: str,
    status: str,
    request: Request | None = None,
    user: AuthenticatedUser | None = None,
    resource_id: str | None = None,
    detail: dict[str, Any] | None = None,
) -> None:
    prev_hash = db.latest_audit_hash()
    entry: dict[str, Any] = {
        "created_at": utc_now_iso(),
        "actor_user_id": user.id if user else None,
        "actor_username": user.username if user else None,
        "actor_role": user.role if user else None,
        "action": action,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "status": status,
        "ip_address": request.client.host if request and request.client else None,
        "user_agent": request.headers.get("user-agent") if request else None,
        "request_id": getattr(request.state, "request_id", None) if request else None,
        "detail": detail or {},
        "prev_hash": prev_hash,
    }
    entry["entry_hash"] = compute_entry_hash(entry)
    db.insert_audit_log(entry)


def verify_audit_chain(db: Database) -> dict[str, Any]:
    previous_hash: str | None = None
    checked = 0
    for row in db.iter_audit_logs():
        detail = json.loads(row["detail_json"])
        entry = {
            "created_at": row["created_at"],
            "actor_user_id": row["actor_user_id"],
            "actor_username": row["actor_username"],
            "actor_role": row["actor_role"],
            "action": row["action"],
            "resource_type": row["resource_type"],
            "resource_id": row["resource_id"],
            "status": row["status"],
            "ip_address": row["ip_address"],
            "user_agent": row["user_agent"],
            "request_id": row["request_id"],
            "detail": detail,
            "prev_hash": row["prev_hash"],
        }
        if row["prev_hash"] != previous_hash:
            return {
                "valid": False,
                "checked": checked,
                "failed_at": row["id"],
                "reason": "previous hash mismatch",
            }
        if compute_entry_hash(entry) != row["entry_hash"]:
            return {
                "valid": False,
                "checked": checked,
                "failed_at": row["id"],
                "reason": "entry hash mismatch",
            }
        previous_hash = row["entry_hash"]
        checked += 1
    return {"valid": True, "checked": checked}
