from __future__ import annotations

import math
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from secure_crime_api.analytics import SAFEGUARDS, now_utc
from secure_crime_api.storage import Database


def advanced_crime_analytics(db: Database) -> dict[str, Any]:
    status = db.crime_data_status()
    cache_key = {
        "imported_count": int(status["imported_count"] or 0),
        "geocoded_count": int(status["geocoded_count"] or 0),
        "latest_incident_at": status.get("latest_incident_at"),
    }
    cached = load_cached_analytics(db.path, cache_key)
    if cached:
        return cached

    latest = _parse_iso(status.get("latest_incident_at"))
    if latest:
        recent_start = (latest - timedelta(days=30)).isoformat()
        baseline_start = (latest - timedelta(days=365)).isoformat()
    else:
        recent_start = now_utc().isoformat()
        baseline_start = (now_utc() - timedelta(days=365)).isoformat()

    heatmap_points = heatmap_points_from_rows(db.crime_heatmap_rows(700))
    risk_areas, alerts, anomalies = risk_alerts_and_anomalies(
        db.recent_baseline_rows(recent_start, baseline_start, 1200)
    )
    network = aggregate_network(db.crime_network_rows(100))

    data_quality = []
    imported_count = int(status["imported_count"] or 0)
    geocoded_count = int(status["geocoded_count"] or 0)
    if not imported_count:
        data_quality.append("No crime incident CSV records have been imported yet.")
    elif not geocoded_count:
        data_quality.append("Imported records do not include usable latitude/longitude.")
    elif geocoded_count < imported_count:
        data_quality.append(f"{imported_count - geocoded_count} imported incident(s) are missing usable coordinates.")
    data_quality.append(
        "This model uses local statistical baselines: grid clustering, recent-vs-historical spike ratios, and z-score anomaly signals."
    )

    response = {
        "generated_at": datetime.now(timezone.utc),
        "imported_count": imported_count,
        "geocoded_count": geocoded_count,
        "heatmap_points": heatmap_points,
        "spatiotemporal_clusters": heatmap_points[:80],
        "emerging_trend_alerts": alerts,
        "risk_areas": risk_areas,
        "anomalies": anomalies,
        "network": network,
        "data_quality": data_quality,
        "safeguards": SAFEGUARDS
        + [
            "Risk scores are planning signals, not predictions about an individual.",
            "The uploaded CSV does not include offender identities; offender networks are limited to crime type, MO, location, premise, weapon, and district relationships.",
        ],
    }
    save_cached_analytics(db.path, cache_key, response)
    return response


def heatmap_points_from_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not rows:
        return []
    max_count = max(1, max(int(row["incident_count"]) for row in rows))
    points = []
    for row in rows:
        count = int(row["incident_count"])
        weapon_share = float(row.get("weapon_share") or 0)
        normalized = count / max_count
        score = min(100, round(normalized * 80 + weapon_share * 20))
        points.append(
            {
                "latitude": float(row["latitude"]),
                "longitude": float(row["longitude"]),
                "weight": max(0.25, min(2.5, 0.3 + normalized * 2.2)),
                "incident_count": count,
                "district": row["district"],
                "top_crime_type": row["top_crime_type"],
                "dominant_time_bucket": row["dominant_time_bucket"] or "unknown",
                "risk_level": risk_level(score),
            }
        )
    return points


def risk_alerts_and_anomalies(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    risk_areas = []
    alerts = []
    anomalies = []
    for row in rows:
        recent = int(row["recent_count"] or 0)
        baseline = int(row["baseline_count"] or 0)
        night_share = float(row["night_share"] or 0)
        weapon_share = float(row["weapon_share"] or 0)
        expected = max(1.0, baseline / 11.0)
        spike_ratio = recent / expected
        z_score = (recent - expected) / math.sqrt(expected)
        score = min(100, round(recent * 1.8 + min(spike_ratio, 6) * 10 + night_share * 12 + weapon_share * 18))
        drivers = []
        if spike_ratio >= 1.5:
            drivers.append(f"{spike_ratio:.1f}x recent spike over baseline expectation")
        if night_share >= 0.35:
            drivers.append("high night-time share")
        if weapon_share >= 0.2:
            drivers.append("weapon-linked incident share")
        if not drivers:
            drivers.append("current recent incident volume")

        risk_areas.append(
            {
                "district": row["district"],
                "crime_type": row["crime_type"],
                "score": score,
                "risk_level": risk_level(score),
                "recent_count": recent,
                "baseline_count": baseline,
                "night_share": round(night_share, 3),
                "weapon_share": round(weapon_share, 3),
                "drivers": drivers,
            }
        )

        if recent >= 10 and spike_ratio >= 1.5:
            alerts.append(
                {
                    "district": row["district"],
                    "crime_type": row["crime_type"],
                    "recent_count": recent,
                    "baseline_expected": round(expected, 2),
                    "spike_ratio": round(spike_ratio, 2),
                    "severity": risk_level(score),
                    "explanation": (
                        f"{row['crime_type']} in {row['district']} is {spike_ratio:.1f}x above "
                        "the local historical monthly expectation."
                    ),
                }
            )

        if recent >= 5 and z_score >= 2.5:
            anomalies.append(
                {
                    "district": row["district"],
                    "crime_type": row["crime_type"],
                    "recent_count": recent,
                    "expected_count": round(expected, 2),
                    "z_score": round(z_score, 2),
                    "explanation": (
                        f"{row['district']} / {row['crime_type']} deviates from the baseline "
                        f"by z={z_score:.2f}."
                    ),
                }
            )

    risk_areas.sort(key=lambda item: (-item["score"], -item["recent_count"], item["district"]))
    alerts.sort(key=lambda item: (-_severity_rank(item["severity"]), -item["spike_ratio"], -item["recent_count"]))
    anomalies.sort(key=lambda item: (-item["z_score"], -item["recent_count"]))
    return risk_areas[:60], alerts[:40], anomalies[:40]


def aggregate_network(edge_groups: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    nodes: dict[str, dict[str, Any]] = {}
    links: dict[tuple[str, str, str], dict[str, Any]] = {}

    def node(node_id: str, label: str, node_type: str, district: str | None = None, weight: int = 1) -> None:
        item = nodes.setdefault(
            node_id,
            {"id": node_id, "label": label, "type": node_type, "case_count": 0, "districts": []},
        )
        item["case_count"] += weight
        if district and district not in item["districts"]:
            item["districts"].append(district)

    def link(source: str, target: str, relationship: str, weight: int) -> None:
        item = links.setdefault(
            (source, target, relationship),
            {"source": source, "target": target, "relationship": relationship, "weight": 0, "case_ids": []},
        )
        item["weight"] += weight

    for row in edge_groups["district_type"]:
        weight = int(row["weight"])
        district_id = f"district:{_slug(row['district'])}"
        type_id = f"type:{_slug(row['crime_type'])}"
        node(district_id, row["district"], "district", row["district"], weight)
        node(type_id, row["crime_type"], "crime_type", row["district"], weight)
        link(district_id, type_id, "HAS_CRIME_TYPE", weight)

    for row in edge_groups["type_mo"]:
        weight = int(row["weight"])
        type_id = f"type:{_slug(row['crime_type'])}"
        mo_id = f"mo:{_slug(row['modus_operandi'])}"
        node(type_id, row["crime_type"], "crime_type", weight=weight)
        node(mo_id, row["modus_operandi"], "modus_operandi", weight=weight)
        link(type_id, mo_id, "USES_MODUS_OPERANDI", weight)

    for row in edge_groups["type_premise"]:
        weight = int(row["weight"])
        type_id = f"type:{_slug(row['crime_type'])}"
        premise_id = f"premise:{_slug(row['premise_desc'])}"
        node(type_id, row["crime_type"], "crime_type", weight=weight)
        node(premise_id, row["premise_desc"], "premise", weight=weight)
        link(type_id, premise_id, "OCCURS_AT_PREMISE", weight)

    for row in edge_groups["type_weapon"]:
        weight = int(row["weight"])
        type_id = f"type:{_slug(row['crime_type'])}"
        weapon_id = f"weapon:{_slug(row['weapon_desc'])}"
        node(type_id, row["crime_type"], "crime_type", weight=weight)
        node(weapon_id, row["weapon_desc"], "weapon", weight=weight)
        link(type_id, weapon_id, "LINKED_WEAPON", weight)

    return {"nodes": list(nodes.values())[:400], "links": list(links.values())[:500], "generated_at": datetime.now(timezone.utc)}


def risk_level(score: int) -> str:
    if score >= 70:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def _severity_rank(value: str) -> int:
    return {"high": 3, "medium": 2, "low": 1}.get(value, 0)


def _parse_iso(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def _slug(value: Any) -> str:
    text = str(value or "").lower()
    slug = "-".join(part for part in "".join(ch if ch.isalnum() else " " for ch in text).split() if part)
    return slug[:80] or "unknown"


def load_cached_analytics(database_path: Path, cache_key: dict[str, Any]) -> dict[str, Any] | None:
    path = cache_path(database_path)
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as handle:
            cached = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None
    if cached.get("cache_key") != cache_key:
        return None
    return cached.get("payload")


def save_cached_analytics(database_path: Path, cache_key: dict[str, Any], payload: dict[str, Any]) -> None:
    path = cache_path(database_path)
    try:
        with path.open("w", encoding="utf-8") as handle:
            json.dump({"cache_key": cache_key, "payload": payload}, handle, default=str)
    except OSError:
        return


def cache_path(database_path: Path) -> Path:
    return database_path.with_suffix(".advanced_crime_cache.json")
