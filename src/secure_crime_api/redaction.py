from __future__ import annotations

from collections.abc import Mapping
from typing import Any


MASKING_RULES: dict[str, dict[str, str]] = {
    "super_admin": {},
    "supervisor": {},
    "investigator": {},
    "analyst": {
        "complainant_phone": "last_4",
        "complainant_name": "name_initial",
        "victim_name": "name_initial",
    },
    "viewer": {
        "complainant_phone": "full",
        "complainant_name": "name_initial",
        "victim_name": "name_initial",
        "suspect_name": "name_initial",
    },
    "policymaker": {
        "complainant_phone": "full",
        "complainant_name": "name_initial",
        "victim_name": "name_initial",
        "suspect_name": "name_initial",
    },
}


def mask_value(value: Any, rule: str) -> Any:
    if value is None:
        return value
    text = str(value)
    if rule == "full":
        return "***MASKED***"
    if rule == "last_4":
        suffix = text[-4:] if len(text) >= 4 else text
        return f"****{suffix}"
    if rule == "name_initial":
        clean = text.strip()
        if not clean:
            return clean
        return f"{clean[0].upper()}. ***"
    return value


def mask_case(case: Mapping[str, Any], role: str) -> dict[str, Any]:
    rules = MASKING_RULES.get(role, {})
    masked = dict(case)
    for field, rule in rules.items():
        if field in masked:
            masked[field] = mask_value(masked[field], rule)
    return masked
