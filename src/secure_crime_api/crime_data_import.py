from __future__ import annotations

import csv
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any

from secure_crime_api.storage import Database


DATE_FORMATS = ("%m/%d/%Y %H:%M", "%m/%d/%Y %H:%M:%S", "%m/%d/%Y")


def import_crime_csv(
    db: Database,
    path: Path,
    *,
    source_system: str,
    limit: int | None = None,
    reset_source: bool = False,
    batch_size: int = 5000,
) -> dict[str, Any]:
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(str(path))

    if reset_source:
        db.reset_crime_incidents(source_system)

    imported = 0
    skipped = 0
    batch: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if limit is not None and imported + skipped >= limit:
                break
            incident = normalize_crime_row(row, source_system)
            if not incident:
                skipped += 1
                continue
            batch.append(incident)
            if len(batch) >= batch_size:
                imported += db.insert_crime_incident_batch(batch)
                batch.clear()
        if batch:
            imported += db.insert_crime_incident_batch(batch)

    return {
        "imported": imported,
        "skipped": skipped,
        "source_system": source_system,
        "path": str(path),
    }


def normalize_crime_row(row: dict[str, str], source_system: str) -> dict[str, Any] | None:
    source_record_id = clean(row.get("DR_NO"))
    district = clean(row.get("AREA NAME")) or "Unspecified"
    crime_type = clean(row.get("Crm Cd Desc")) or "Unspecified"
    if not source_record_id:
        return None

    reported_at = parse_datetime(row.get("Date Rptd"))
    occurred = parse_datetime(row.get("DATE OCC"))
    hour = parse_time_hour(row.get("TIME OCC"))
    incident_at = merge_date_hour(occurred, hour) or occurred
    latitude = parse_float(row.get("LAT"))
    longitude = parse_float(row.get("LON"))
    if latitude == 0 and longitude == 0:
        latitude = None
        longitude = None

    return {
        "id": stable_id(source_system, source_record_id),
        "source_system": source_system,
        "source_record_id": source_record_id,
        "reported_at": reported_at.isoformat() if reported_at else None,
        "incident_at": incident_at.isoformat() if incident_at else None,
        "incident_year": incident_at.year if incident_at else None,
        "incident_month": incident_at.strftime("%Y-%m") if incident_at else None,
        "incident_hour": hour,
        "time_bucket": time_bucket(hour),
        "area_code": clean(row.get("AREA")),
        "district": district,
        "report_district": clean(row.get("Rpt Dist No")),
        "part_code": clean(row.get("Part 1-2")),
        "crime_code": clean(row.get("Crm Cd")),
        "crime_type": crime_type,
        "modus_operandi": clean(row.get("Mocodes")),
        "victim_age": parse_int(row.get("Vict Age")),
        "victim_gender": clean(row.get("Vict Sex")),
        "victim_descent": clean(row.get("Vict Descent")),
        "premise_code": clean(row.get("Premis Cd")),
        "premise_desc": clean(row.get("Premis Desc")),
        "weapon_code": clean(row.get("Weapon Used Cd")),
        "weapon_desc": clean(row.get("Weapon Desc")),
        "status_code": clean(row.get("Status")),
        "status_desc": clean(row.get("Status Desc")),
        "location": clean(row.get("LOCATION")),
        "cross_street": clean(row.get("Cross Street")),
        "latitude": latitude,
        "longitude": longitude,
        "grid_lat": round(latitude, 2) if latitude is not None else None,
        "grid_lon": round(longitude, 2) if longitude is not None else None,
    }


def clean(value: str | None) -> str | None:
    text = (value or "").strip()
    return " ".join(text.split()) or None


def parse_datetime(value: str | None) -> datetime | None:
    text = clean(value)
    if not text:
        return None
    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(text, date_format)
        except ValueError:
            continue
    return None


def parse_time_hour(value: str | None) -> int | None:
    text = clean(value)
    if not text:
        return None
    digits = "".join(ch for ch in text if ch.isdigit()).zfill(4)
    if len(digits) < 4:
        return None
    hour = int(digits[:2])
    return hour if 0 <= hour <= 23 else None


def merge_date_hour(value: datetime | None, hour: int | None) -> datetime | None:
    if not value or hour is None:
        return value
    return value.replace(hour=hour, minute=0, second=0, microsecond=0)


def parse_float(value: str | None) -> float | None:
    text = clean(value)
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def parse_int(value: str | None) -> int | None:
    text = clean(value)
    if not text:
        return None
    try:
        parsed = int(float(text))
    except ValueError:
        return None
    return parsed if parsed >= 0 else None


def time_bucket(hour: int | None) -> str:
    if hour is None:
        return "unknown"
    if 5 <= hour < 12:
        return "morning"
    if 12 <= hour < 17:
        return "afternoon"
    if 17 <= hour < 22:
        return "evening"
    return "night"


def stable_id(source_system: str, source_record_id: str) -> str:
    digest = hashlib.sha256(f"{source_system}:{source_record_id}".encode("utf-8")).hexdigest()
    return digest[:32]
