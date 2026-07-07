from __future__ import annotations

from secure_crime_api.models import AuthenticatedUser


PERMISSIONS: dict[str, set[str]] = {
    "super_admin": {
        "admin:*",
        "analytics:*",
        "audit:*",
        "case:*",
        "conversation:*",
        "explain:*",
        "financial:*",
        "forecast:*",
        "intelligence:*",
        "profile:*",
        "search:*",
        "sociological:*",
        "translation:*",
        "user:*",
    },
    "supervisor": {
        "case:*",
        "analytics:read",
        "conversation:*",
        "explain:read",
        "financial:read",
        "financial:import",
        "forecast:read",
        "intelligence:query",
        "profile:read",
        "search:case",
        "sociological:read",
        "translation:use",
        "audit:read",
        "audit:verify",
    },
    "investigator": {
        "case:read",
        "case:update",
        "case:note",
        "analytics:read",
        "conversation:*",
        "explain:read",
        "financial:read",
        "financial:import",
        "forecast:read",
        "intelligence:query",
        "profile:read",
        "search:case",
        "sociological:read",
        "translation:use",
    },
    "analyst": {
        "case:read",
        "analytics:read",
        "conversation:*",
        "explain:read",
        "financial:read",
        "forecast:read",
        "intelligence:query",
        "profile:read",
        "search:case",
        "sociological:read",
        "translation:use",
    },
    "policymaker": {
        "analytics:read",
        "conversation:*",
        "forecast:read",
        "intelligence:query",
        "sociological:read",
        "translation:use",
    },
    "viewer": {"case:read", "search:case"},
}


def role_has_permission(role: str, permission: str) -> bool:
    permissions = PERMISSIONS.get(role, set())
    if permission in permissions:
        return True
    resource, _, action = permission.partition(":")
    return f"{resource}:*" in permissions and bool(action)


def can_access_case(user: AuthenticatedUser, case: dict) -> bool:
    if user.role == "policymaker":
        return False
    if user.role in {"super_admin", "supervisor"}:
        return True
    if case["district"] != user.district:
        return False
    if case["sensitivity"] == "restricted" and user.role in {"analyst", "viewer"}:
        return False
    return True
