from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from secure_crime_api.models import CaseCreate
from secure_crime_api.security import hash_password
from secure_crime_api.storage import Database, utc_now_iso


DEMO_SOURCE = "ksp-hackathon-demo"


DEMO_USERS = [
    ("superadmin", "Super Admin", "super_admin", "state"),
    ("admin", "Bootstrap Admin", "super_admin", "state"),
    ("supervisor", "State Supervisor", "supervisor", "state"),
    ("investigator", "Bengaluru Investigator", "investigator", "Bengaluru Urban"),
    ("analyst", "Bengaluru Analyst", "analyst", "Bengaluru Urban"),
    ("policymaker", "Policy Planner", "policymaker", "state"),
    ("viewer", "Bengaluru Viewer", "viewer", "Bengaluru Urban"),
]


def seed_demo_data(db: Database, *, demo_password: str = "admin123") -> None:
    """Populate a clean Catalyst demo database with evaluator-ready records."""

    for username, full_name, role, district in DEMO_USERS:
        _ensure_demo_user(
            db,
            username=username,
            password=demo_password if username != "admin" else "SecureAdminPassword123!",
            full_name=full_name,
            role=role,
            district=district,
        )

    _ensure_demo_cases(db)
    _ensure_demo_transactions(db)
    _ensure_demo_incidents(db)


def _ensure_demo_user(
    db: Database,
    *,
    username: str,
    password: str,
    full_name: str,
    role: str,
    district: str,
) -> None:
    existing = db.get_user_by_username(username)
    if existing:
        db.update_user(
            existing["id"],
            full_name=full_name,
            role=role,
            district=district,
            is_active=True,
        )
        db.update_password_hash(existing["id"], hash_password(password))
        return

    with db.connect() as conn:
        conn.execute(
            """
            INSERT INTO users
                (id, username, full_name, role, district, password_hash, is_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, 1, ?)
            """,
            (str(uuid.uuid4()), username, full_name, role, district, hash_password(password), utc_now_iso()),
        )


def _ensure_demo_cases(db: Database) -> None:
    existing = {(case["fir_number"], int(case["year"])) for case in db.list_cases()}
    for case in _demo_cases():
        key = (case.fir_number, case.year)
        if key not in existing:
            db.create_case(case)
            existing.add(key)


def _demo_cases() -> list[CaseCreate]:
    return [
        CaseCreate(
            fir_number="BLR-CYB-042",
            year=2026,
            district="Bengaluru Urban",
            status="open",
            case_type="Cyber Financial Fraud",
            modus_operandi="phishing link and SIM swap",
            incident_at=datetime(2026, 7, 4, 10, 15, tzinfo=timezone.utc),
            complainant_name="Prakash Kumar",
            complainant_phone="+91-9000012345",
            victim_name="Prakash Kumar",
            victim_age=38,
            victim_gender="Male",
            suspect_name="Pooja Naik",
            suspect_age=31,
            suspect_gender="Female",
            summary=(
                "Demo/template FIR: victim reported a phishing link followed by SIM swap activity, "
                "with rapid transfers to mule accounts across Bengaluru and Mysuru branches."
            ),
            sensitivity="standard",
            latitude=12.9716,
            longitude=77.5946,
            socio_economic_context="urban salaried banking user",
            urbanization_context="metro digital payments corridor",
            migration_context="inter-district account movement",
            education_context="graduate professional",
            event_context="weekend online shopping campaign",
            source_system=DEMO_SOURCE,
            source_record_id="DEMO-BLR-CYB-042",
        ),
        CaseCreate(
            fir_number="BLR-CYB-043",
            year=2026,
            district="Bengaluru Urban",
            status="under_review",
            case_type="Cyber Financial Fraud",
            modus_operandi="phishing link and SIM swap",
            incident_at=datetime(2026, 7, 6, 14, 40, tzinfo=timezone.utc),
            complainant_name="Santosh Sharma",
            complainant_phone="+91-9000012346",
            victim_name="Santosh Sharma",
            victim_age=44,
            victim_gender="Male",
            suspect_name="Pooja Naik",
            suspect_age=31,
            suspect_gender="Female",
            summary=(
                "Demo/template FIR: second phishing complaint shares a device fingerprint and "
                "beneficiary branch pattern with BLR-CYB-042."
            ),
            sensitivity="restricted",
            latitude=12.9352,
            longitude=77.6245,
            socio_economic_context="small business owner",
            urbanization_context="commercial district",
            migration_context="same beneficiary cluster",
            education_context="college educated",
            event_context="festival discount campaign",
            source_system=DEMO_SOURCE,
            source_record_id="DEMO-BLR-CYB-043",
        ),
        CaseCreate(
            fir_number="MYS-BRK-011",
            year=2026,
            district="Mysuru",
            status="open",
            case_type="House Breaking",
            modus_operandi="duplicate key entry at night",
            incident_at=datetime(2026, 6, 26, 23, 20, tzinfo=timezone.utc),
            complainant_name="Naveen Rao",
            complainant_phone="+91-9000012347",
            victim_name="Naveen Rao",
            victim_age=52,
            victim_gender="Male",
            suspect_name="Naveen Sharma",
            suspect_age=29,
            suspect_gender="Male",
            summary=(
                "Demo/template FIR: night house breaking near a transit road with duplicate key access "
                "and CCTV overlap with another property offence."
            ),
            sensitivity="standard",
            latitude=12.2958,
            longitude=76.6394,
            socio_economic_context="residential middle income area",
            urbanization_context="peri-urban growth zone",
            migration_context="seasonal worker movement",
            education_context="secondary education",
            event_context="local market closure day",
            source_system=DEMO_SOURCE,
            source_record_id="DEMO-MYS-BRK-011",
        ),
        CaseCreate(
            fir_number="UDU-CHN-022",
            year=2026,
            district="Udupi",
            status="open",
            case_type="Chain Snatching",
            modus_operandi="two-wheeler drive-by snatching",
            incident_at=datetime(2026, 6, 21, 19, 5, tzinfo=timezone.utc),
            complainant_name="Pooja Kumar",
            complainant_phone="+91-9000012348",
            victim_name="Pooja Kumar",
            victim_age=34,
            victim_gender="Female",
            suspect_name="Ramesh Naik",
            suspect_age=27,
            suspect_gender="Male",
            summary=(
                "Demo/template FIR: drive-by chain snatching near a bus stand; vehicle route overlaps "
                "with prior coastal district incidents."
            ),
            sensitivity="standard",
            latitude=13.3409,
            longitude=74.7421,
            socio_economic_context="public transit commuter",
            urbanization_context="coastal town corridor",
            migration_context="tourist and commuter flow",
            education_context="college area",
            event_context="evening peak movement",
            source_system=DEMO_SOURCE,
            source_record_id="DEMO-UDU-CHN-022",
        ),
        CaseCreate(
            fir_number="MNG-AST-008",
            year=2026,
            district="Dakshina Kannada",
            status="under_review",
            case_type="Assault",
            modus_operandi="group assault after local dispute",
            incident_at=datetime(2026, 6, 28, 21, 30, tzinfo=timezone.utc),
            complainant_name="Shwetha Poojary",
            complainant_phone="+91-9000012349",
            victim_name="Mahesh Rao",
            victim_age=41,
            victim_gender="Male",
            suspect_name="Akash Reddy",
            suspect_age=33,
            suspect_gender="Male",
            summary=(
                "Demo/template FIR: group assault with witness statements, prior threat call, "
                "and district-level event context."
            ),
            sensitivity="restricted",
            latitude=12.9141,
            longitude=74.856,
            socio_economic_context="mixed commercial locality",
            urbanization_context="port city expansion",
            migration_context="interstate labor flow",
            education_context="mixed literacy area",
            event_context="local procession spillover",
            source_system=DEMO_SOURCE,
            source_record_id="DEMO-MNG-AST-008",
        ),
        CaseCreate(
            fir_number="HUB-VTH-019",
            year=2026,
            district="Dharwad",
            status="closed",
            case_type="Vehicle Theft",
            modus_operandi="night parking area vehicle theft",
            incident_at=datetime(2026, 5, 17, 2, 10, tzinfo=timezone.utc),
            complainant_name="Manjunath Rao",
            complainant_phone="+91-9000012350",
            victim_name="Manjunath Rao",
            victim_age=46,
            victim_gender="Male",
            suspect_name="Ganesh Hegde",
            suspect_age=35,
            suspect_gender="Male",
            summary=(
                "Demo/template FIR: motorcycle theft from a parking cluster; recovery closed after "
                "cross-district vehicle check."
            ),
            sensitivity="standard",
            latitude=15.3647,
            longitude=75.124,
            socio_economic_context="transport worker locality",
            urbanization_context="industrial logistics corridor",
            migration_context="truck route movement",
            education_context="vocational workforce",
            event_context="night market activity",
            source_system=DEMO_SOURCE,
            source_record_id="DEMO-HUB-VTH-019",
        ),
    ]


def _ensure_demo_transactions(db: Database) -> None:
    if db.list_financial_transactions():
        return

    cases = {case["fir_number"]: case for case in db.list_cases()}
    blr_42 = cases.get("BLR-CYB-042")
    blr_43 = cases.get("BLR-CYB-043")
    if not blr_42 or not blr_43:
        return

    transaction_rows = [
        {
            "occurred_at": "2026-07-04T10:32:00+00:00",
            "source_account": "IN-BLR-PRK-0001",
            "target_account": "IN-BLR-MULE-1001",
            "source_account_holder": "Prakash Kumar",
            "target_account_holder": "A2",
            "source_bank_name": "Karnataka Cooperative Bank",
            "source_ifsc_code": "KCBL0001234",
            "source_branch": "Bengaluru Central",
            "source_bank_manager_phone": "+91-8000011111",
            "target_bank_name": "Mysuru Rural Bank",
            "target_ifsc_code": "MRBL0007777",
            "target_branch": "Mysuru East",
            "target_bank_manager_phone": "+91-8000022222",
            "amount": 1250000.0,
            "currency": "INR",
            "district": "Bengaluru Urban",
            "case_id": blr_42["id"],
            "description": "Demo transfer: high-value movement after phishing complaint.",
        },
        {
            "occurred_at": "2026-07-04T11:04:00+00:00",
            "source_account": "IN-BLR-MULE-1001",
            "target_account": "IN-MYS-LAYER-2200",
            "source_account_holder": "A2",
            "target_account_holder": "A3",
            "source_bank_name": "Mysuru Rural Bank",
            "source_ifsc_code": "MRBL0007777",
            "source_branch": "Mysuru East",
            "source_bank_manager_phone": "+91-8000022222",
            "target_bank_name": "Coastal Finance Bank",
            "target_ifsc_code": "CFBK0009012",
            "target_branch": "Udupi Market",
            "target_bank_manager_phone": "+91-8000033333",
            "amount": 950000.0,
            "currency": "INR",
            "district": "Bengaluru Urban",
            "case_id": blr_42["id"],
            "description": "Demo transfer: near-threshold layering transaction.",
        },
        {
            "occurred_at": "2026-07-06T15:18:00+00:00",
            "source_account": "IN-BLR-SAN-0002",
            "target_account": "IN-BLR-MULE-1001",
            "source_account_holder": "Santosh Sharma",
            "target_account_holder": "A2",
            "source_bank_name": "Karnataka Cooperative Bank",
            "source_ifsc_code": "KCBL0002234",
            "source_branch": "Koramangala",
            "source_bank_manager_phone": "+91-8000044444",
            "target_bank_name": "Mysuru Rural Bank",
            "target_ifsc_code": "MRBL0007777",
            "target_branch": "Mysuru East",
            "target_bank_manager_phone": "+91-8000022222",
            "amount": 940000.0,
            "currency": "INR",
            "district": "Bengaluru Urban",
            "case_id": blr_43["id"],
            "description": "Demo transfer: shared mule account across two FIRs.",
        },
    ]
    for row in transaction_rows:
        db.create_financial_transaction(**row)


def _ensure_demo_incidents(db: Database) -> None:
    if db.crime_incident_count() > 0:
        return
    db.insert_crime_incident_batch(_demo_incidents())


def _demo_incidents() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    recent_start = datetime(2026, 7, 1, 9, tzinfo=timezone.utc)
    for index in range(18):
        rows.append(
            _incident(
                source_record_id=f"DEMO-CYBER-RECENT-{index + 1:03d}",
                occurred_at=recent_start + timedelta(days=index % 12, hours=index % 7),
                district="Bengaluru Urban",
                crime_type="Cyber Financial Fraud",
                modus_operandi="phishing link and SIM swap",
                premise_desc="online banking channel",
                weapon_desc="digital credential compromise",
                latitude=12.9716 + (index % 4) * 0.01,
                longitude=77.5946 + (index % 5) * 0.01,
                victim_age=32 + (index % 28),
                victim_gender="Male" if index % 2 else "Female",
            )
        )

    baseline_start = datetime(2026, 1, 10, 18, tzinfo=timezone.utc)
    for index in range(5):
        rows.append(
            _incident(
                source_record_id=f"DEMO-CYBER-BASELINE-{index + 1:03d}",
                occurred_at=baseline_start + timedelta(days=index * 21),
                district="Bengaluru Urban",
                crime_type="Cyber Financial Fraud",
                modus_operandi="phishing link and SIM swap",
                premise_desc="online banking channel",
                weapon_desc="digital credential compromise",
                latitude=12.94 + index * 0.01,
                longitude=77.61 + index * 0.01,
                victim_age=35 + index,
                victim_gender="Male",
            )
        )

    other_patterns = [
        ("Mysuru", "House Breaking", "duplicate key entry at night", "residential building", "iron rod", 12.2958, 76.6394),
        ("Udupi", "Chain Snatching", "two-wheeler drive-by snatching", "bus stand", "", 13.3409, 74.7421),
        ("Dharwad", "Vehicle Theft", "night parking area vehicle theft", "public parking", "", 15.3647, 75.124),
        ("Dakshina Kannada", "Assault", "group assault after local dispute", "market street", "knife", 12.9141, 74.856),
    ]
    for pattern_index, pattern in enumerate(other_patterns):
        district, crime_type, modus, premise, weapon, lat, lon = pattern
        for offset in range(4):
            rows.append(
                _incident(
                    source_record_id=f"DEMO-{pattern_index + 1}-{offset + 1:03d}",
                    occurred_at=datetime(2026, 6, 12 + offset, 20 + (offset % 3), tzinfo=timezone.utc),
                    district=district,
                    crime_type=crime_type,
                    modus_operandi=modus,
                    premise_desc=premise,
                    weapon_desc=weapon,
                    latitude=lat + offset * 0.01,
                    longitude=lon + offset * 0.01,
                    victim_age=26 + offset * 5,
                    victim_gender="Female" if offset % 2 else "Male",
                )
            )
    return rows


def _incident(
    *,
    source_record_id: str,
    occurred_at: datetime,
    district: str,
    crime_type: str,
    modus_operandi: str,
    premise_desc: str,
    weapon_desc: str,
    latitude: float,
    longitude: float,
    victim_age: int,
    victim_gender: str,
) -> dict[str, Any]:
    hour = occurred_at.hour
    if 5 <= hour < 12:
        time_bucket = "morning"
    elif 12 <= hour < 17:
        time_bucket = "afternoon"
    elif 17 <= hour < 21:
        time_bucket = "evening"
    else:
        time_bucket = "night"

    return {
        "id": str(uuid.uuid4()),
        "source_system": DEMO_SOURCE,
        "source_record_id": source_record_id,
        "reported_at": occurred_at.isoformat(),
        "incident_at": occurred_at.isoformat(),
        "incident_year": occurred_at.year,
        "incident_month": occurred_at.strftime("%Y-%m"),
        "incident_hour": hour,
        "time_bucket": time_bucket,
        "area_code": district[:3].upper(),
        "district": district,
        "report_district": district,
        "part_code": "1",
        "crime_code": crime_type[:12].upper(),
        "crime_type": crime_type,
        "modus_operandi": modus_operandi,
        "victim_age": victim_age,
        "victim_gender": victim_gender,
        "victim_descent": "demo",
        "premise_code": premise_desc[:12].upper(),
        "premise_desc": premise_desc,
        "weapon_code": weapon_desc[:12].upper() if weapon_desc else "",
        "weapon_desc": weapon_desc,
        "status_code": "IC",
        "status_desc": "Investigation continuing",
        "location": f"{district} demo location",
        "cross_street": "",
        "latitude": latitude,
        "longitude": longitude,
        "grid_lat": round(latitude, 2),
        "grid_lon": round(longitude, 2),
    }
