from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from secure_crime_api.models import CaseCreate, UserCreate
from secure_crime_api.security import hash_password


_CRIME_INCIDENT_BUCKET_FIELDS = {
    "district",
    "crime_type",
    "modus_operandi",
    "premise_desc",
    "weapon_desc",
    "time_bucket",
    "victim_gender",
    "victim_descent",
    "incident_month",
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _clean_filter(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _message_from_row(row: sqlite3.Row) -> dict[str, Any]:
    item = dict(row)
    try:
        item["metadata"] = json.loads(item.pop("metadata_json") or "{}")
    except (TypeError, json.JSONDecodeError):
        item["metadata"] = {}
    return item


class Database:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_schema(self) -> None:
        with self.connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    full_name TEXT NOT NULL,
                    role TEXT NOT NULL CHECK (role IN ('super_admin', 'supervisor', 'investigator', 'analyst', 'policymaker', 'viewer')),
                    district TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS cases (
                    id TEXT PRIMARY KEY,
                    fir_number TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    district TEXT NOT NULL,
                    status TEXT NOT NULL CHECK (status IN ('open', 'under_review', 'closed')),
                    case_type TEXT,
                    modus_operandi TEXT,
                    incident_at TEXT,
                    complainant_name TEXT NOT NULL,
                    complainant_phone TEXT NOT NULL,
                    victim_name TEXT NOT NULL,
                    victim_age INTEGER,
                    victim_gender TEXT,
                    suspect_name TEXT NOT NULL,
                    suspect_age INTEGER,
                    suspect_gender TEXT,
                    summary TEXT NOT NULL,
                    sensitivity TEXT NOT NULL CHECK (sensitivity IN ('standard', 'restricted')),
                    latitude REAL,
                    longitude REAL,
                    socio_economic_context TEXT,
                    urbanization_context TEXT,
                    migration_context TEXT,
                    education_context TEXT,
                    event_context TEXT,
                    source_system TEXT,
                    source_record_id TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE (fir_number, year)
                );

                CREATE TABLE IF NOT EXISTS case_notes (
                    id TEXT PRIMARY KEY,
                    case_id TEXT NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
                    author_user_id TEXT NOT NULL REFERENCES users(id),
                    body TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS case_search_index (
                    prefix_hash TEXT NOT NULL,
                    case_id TEXT NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
                    field TEXT NOT NULL,
                    weight INTEGER NOT NULL,
                    PRIMARY KEY (prefix_hash, case_id, field)
                );

                CREATE TABLE IF NOT EXISTS case_search_terms (
                    term TEXT PRIMARY KEY,
                    frequency INTEGER NOT NULL DEFAULT 1
                );

                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL REFERENCES users(id),
                    title TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS conversation_messages (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
                    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
                    content TEXT NOT NULL,
                    metadata_json TEXT NOT NULL DEFAULT '{}',
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS financial_transactions (
                    id TEXT PRIMARY KEY,
                    occurred_at TEXT NOT NULL,
                    source_account TEXT NOT NULL,
                    target_account TEXT NOT NULL,
                    source_account_holder TEXT,
                    target_account_holder TEXT,
                    source_bank_name TEXT,
                    source_ifsc_code TEXT,
                    source_branch TEXT,
                    source_bank_manager_phone TEXT,
                    target_bank_name TEXT,
                    target_ifsc_code TEXT,
                    target_branch TEXT,
                    target_bank_manager_phone TEXT,
                    amount REAL NOT NULL,
                    currency TEXT NOT NULL,
                    district TEXT NOT NULL,
                    case_id TEXT REFERENCES cases(id) ON DELETE SET NULL,
                    description TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS file_uploads (
                    id TEXT PRIMARY KEY,
                    uploaded_at TEXT NOT NULL,
                    uploaded_by TEXT,
                    original_filename TEXT NOT NULL,
                    stored_path TEXT NOT NULL,
                    content_type TEXT,
                    extension TEXT NOT NULL,
                    sha256 TEXT NOT NULL,
                    size_bytes INTEGER NOT NULL,
                    case_id TEXT REFERENCES cases(id) ON DELETE SET NULL,
                    upload_type TEXT NOT NULL,
                    parsed_case_count INTEGER NOT NULL DEFAULT 0,
                    skipped_case_count INTEGER NOT NULL DEFAULT 0,
                    status TEXT NOT NULL,
                    notes TEXT NOT NULL,
                    extracted_preview TEXT,
                    extracted_summary TEXT,
                    extracted_summary_kn TEXT,
                    extraction_status TEXT,
                    extracted_char_count INTEGER NOT NULL DEFAULT 0,
                    extracted_metadata_json TEXT NOT NULL DEFAULT '{}',
                    fir_reconstruction_xml TEXT,
                    fir_reconstruction_status TEXT
                );

                CREATE TABLE IF NOT EXISTS biometric_credentials (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    credential_id TEXT NOT NULL UNIQUE,
                    public_key_cose BLOB NOT NULL,
                    sign_count INTEGER NOT NULL DEFAULT 0,
                    transports_json TEXT NOT NULL DEFAULT '[]',
                    label TEXT,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL,
                    last_used_at TEXT
                );

                CREATE TABLE IF NOT EXISTS biometric_challenges (
                    id TEXT PRIMARY KEY,
                    challenge TEXT NOT NULL UNIQUE,
                    user_id TEXT,
                    username TEXT,
                    purpose TEXT NOT NULL CHECK (purpose IN ('registration', 'authentication')),
                    rp_id TEXT NOT NULL,
                    origin TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    consumed_at TEXT,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS crime_incidents (
                    id TEXT PRIMARY KEY,
                    source_system TEXT NOT NULL,
                    source_record_id TEXT NOT NULL,
                    reported_at TEXT,
                    incident_at TEXT,
                    incident_year INTEGER,
                    incident_month TEXT,
                    incident_hour INTEGER,
                    time_bucket TEXT,
                    area_code TEXT,
                    district TEXT NOT NULL,
                    report_district TEXT,
                    part_code TEXT,
                    crime_code TEXT,
                    crime_type TEXT NOT NULL,
                    modus_operandi TEXT,
                    victim_age INTEGER,
                    victim_gender TEXT,
                    victim_descent TEXT,
                    premise_code TEXT,
                    premise_desc TEXT,
                    weapon_code TEXT,
                    weapon_desc TEXT,
                    status_code TEXT,
                    status_desc TEXT,
                    location TEXT,
                    cross_street TEXT,
                    latitude REAL,
                    longitude REAL,
                    grid_lat REAL,
                    grid_lon REAL,
                    imported_at TEXT NOT NULL,
                    UNIQUE (source_system, source_record_id)
                );

                CREATE TABLE IF NOT EXISTS revoked_tokens (
                    jti TEXT PRIMARY KEY,
                    expires_at TEXT NOT NULL,
                    revoked_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS rate_limit_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    actor_user_id TEXT,
                    actor_username TEXT,
                    actor_role TEXT,
                    client_ip TEXT,
                    method TEXT NOT NULL,
                    path TEXT NOT NULL,
                    limit_per_minute INTEGER NOT NULL,
                    window_seconds INTEGER NOT NULL,
                    request_count INTEGER NOT NULL,
                    request_id TEXT,
                    acknowledged_at TEXT,
                    acknowledged_by TEXT
                );

                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    actor_user_id TEXT,
                    actor_username TEXT,
                    actor_role TEXT,
                    action TEXT NOT NULL,
                    resource_type TEXT NOT NULL,
                    resource_id TEXT,
                    status TEXT NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    request_id TEXT,
                    detail_json TEXT NOT NULL,
                    prev_hash TEXT,
                    entry_hash TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_cases_district ON cases(district);
                CREATE INDEX IF NOT EXISTS idx_cases_fir_nocase ON cases(fir_number COLLATE NOCASE);
                CREATE INDEX IF NOT EXISTS idx_cases_source_record_nocase ON cases(source_record_id COLLATE NOCASE);
                CREATE INDEX IF NOT EXISTS idx_cases_suspect_nocase ON cases(suspect_name COLLATE NOCASE);
                CREATE INDEX IF NOT EXISTS idx_cases_victim_nocase ON cases(victim_name COLLATE NOCASE);
                CREATE INDEX IF NOT EXISTS idx_cases_complainant_nocase ON cases(complainant_name COLLATE NOCASE);
                CREATE INDEX IF NOT EXISTS idx_cases_type_nocase ON cases(case_type COLLATE NOCASE);
                CREATE INDEX IF NOT EXISTS idx_cases_incident_at ON cases(incident_at);
                CREATE INDEX IF NOT EXISTS idx_cases_updated_at ON cases(updated_at);
                CREATE INDEX IF NOT EXISTS idx_case_search_prefix ON case_search_index(prefix_hash, weight DESC);
                CREATE INDEX IF NOT EXISTS idx_case_search_terms_frequency ON case_search_terms(frequency DESC);
                CREATE INDEX IF NOT EXISTS idx_conversation_user ON conversations(user_id);
                CREATE INDEX IF NOT EXISTS idx_financial_district ON financial_transactions(district);
                CREATE INDEX IF NOT EXISTS idx_file_uploads_case ON file_uploads(case_id);
                CREATE INDEX IF NOT EXISTS idx_file_uploads_uploaded_at ON file_uploads(uploaded_at);
                CREATE INDEX IF NOT EXISTS idx_biometric_credentials_user ON biometric_credentials(user_id);
                CREATE INDEX IF NOT EXISTS idx_biometric_challenges_lookup ON biometric_challenges(challenge, purpose);
                CREATE INDEX IF NOT EXISTS idx_crime_incident_source ON crime_incidents(source_system, source_record_id);
                CREATE INDEX IF NOT EXISTS idx_crime_incident_time ON crime_incidents(incident_at);
                CREATE INDEX IF NOT EXISTS idx_crime_incident_district ON crime_incidents(district);
                CREATE INDEX IF NOT EXISTS idx_crime_incident_type ON crime_incidents(crime_type);
                CREATE INDEX IF NOT EXISTS idx_crime_incident_grid ON crime_incidents(grid_lat, grid_lon);
                CREATE INDEX IF NOT EXISTS idx_crime_incident_district_type ON crime_incidents(district, crime_type);
                CREATE INDEX IF NOT EXISTS idx_crime_incident_time_bucket ON crime_incidents(time_bucket);
                CREATE INDEX IF NOT EXISTS idx_crime_incident_victim_gender ON crime_incidents(victim_gender);
                CREATE INDEX IF NOT EXISTS idx_crime_incident_district_time ON crime_incidents(district, time_bucket);
                CREATE INDEX IF NOT EXISTS idx_crime_incident_type_time ON crime_incidents(crime_type, time_bucket);
                CREATE INDEX IF NOT EXISTS idx_rate_limit_alerts_created_at ON rate_limit_alerts(created_at);
                CREATE INDEX IF NOT EXISTS idx_rate_limit_alerts_ack ON rate_limit_alerts(acknowledged_at);
                CREATE INDEX IF NOT EXISTS idx_audit_created_at ON audit_logs(created_at);
                CREATE INDEX IF NOT EXISTS idx_audit_entry_hash ON audit_logs(entry_hash);
                CREATE INDEX IF NOT EXISTS idx_audit_logs_actor ON audit_logs(actor_user_id, id DESC);
                CREATE INDEX IF NOT EXISTS idx_audit_logs_resource ON audit_logs(resource_type, resource_id, id DESC);
                """
            )
            self._ensure_columns(
                conn,
                "financial_transactions",
                {
                    "source_bank_name": "TEXT",
                    "source_account_holder": "TEXT",
                    "target_account_holder": "TEXT",
                    "source_ifsc_code": "TEXT",
                    "source_branch": "TEXT",
                    "source_bank_manager_phone": "TEXT",
                    "target_bank_name": "TEXT",
                    "target_ifsc_code": "TEXT",
                    "target_branch": "TEXT",
                    "target_bank_manager_phone": "TEXT",
                },
            )
            self._ensure_column(conn, "file_uploads", "extracted_summary", "TEXT")
            self._ensure_column(conn, "file_uploads", "extracted_summary_kn", "TEXT")
            self._ensure_column(conn, "file_uploads", "extraction_status", "TEXT")
            self._ensure_column(conn, "file_uploads", "extracted_char_count", "INTEGER NOT NULL DEFAULT 0")
            self._ensure_column(conn, "file_uploads", "extracted_metadata_json", "TEXT NOT NULL DEFAULT '{}'")
            self._ensure_column(conn, "file_uploads", "fir_reconstruction_xml", "TEXT")
            self._ensure_column(conn, "file_uploads", "fir_reconstruction_status", "TEXT")

    def create_file_upload(
        self,
        *,
        uploaded_by: str | None,
        original_filename: str,
        stored_path: str,
        content_type: str | None,
        extension: str,
        sha256: str,
        size_bytes: int,
        case_id: str | None,
        upload_type: str,
        parsed_case_count: int,
        skipped_case_count: int,
        status: str,
        notes: str,
        extracted_preview: str | None = None,
        extracted_summary: str | None = None,
        extracted_summary_kn: str | None = None,
        extraction_status: str | None = None,
        extracted_char_count: int = 0,
        extracted_metadata: dict[str, Any] | None = None,
        fir_reconstruction_xml: str | None = None,
        fir_reconstruction_status: str | None = None,
    ) -> dict[str, Any]:
        upload_id = str(uuid.uuid4())
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO file_uploads (
                    id, uploaded_at, uploaded_by, original_filename, stored_path,
                    content_type, extension, sha256, size_bytes, case_id, upload_type,
                    parsed_case_count, skipped_case_count, status, notes, extracted_preview,
                    extracted_summary, extracted_summary_kn, extraction_status, extracted_char_count,
                    extracted_metadata_json, fir_reconstruction_xml, fir_reconstruction_status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    upload_id,
                    utc_now_iso(),
                    uploaded_by,
                    original_filename,
                    stored_path,
                    content_type,
                    extension,
                    sha256,
                    size_bytes,
                    case_id,
                    upload_type,
                    parsed_case_count,
                    skipped_case_count,
                    status,
                    notes,
                    extracted_preview,
                    extracted_summary,
                    extracted_summary_kn,
                    extraction_status,
                    extracted_char_count,
                    json.dumps(extracted_metadata or {}, sort_keys=True),
                    fir_reconstruction_xml,
                    fir_reconstruction_status,
                ),
            )
            row = conn.execute("SELECT * FROM file_uploads WHERE id = ?", (upload_id,)).fetchone()
            return dict(row)

    def get_file_upload(self, upload_id: str) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute(
                """
                SELECT file_uploads.*,
                       cases.fir_number AS linked_fir_number,
                       cases.district AS linked_district,
                       cases.sensitivity AS linked_sensitivity
                FROM file_uploads
                LEFT JOIN cases ON cases.id = file_uploads.case_id
                WHERE file_uploads.id = ?
                """,
                (upload_id,),
            ).fetchone()
            return dict(row) if row else None

    def list_file_uploads(self, query: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 250))
        search = (query or "").strip().casefold()
        clauses: list[str] = []
        params: list[Any] = []
        if search:
            like = f"%{search}%"
            clauses.append(
                """
                (
                    LOWER(file_uploads.original_filename) LIKE ?
                    OR LOWER(file_uploads.upload_type) LIKE ?
                    OR LOWER(file_uploads.status) LIKE ?
                    OR LOWER(file_uploads.sha256) LIKE ?
                    OR LOWER(COALESCE(file_uploads.extracted_preview, '')) LIKE ?
                    OR LOWER(COALESCE(file_uploads.extracted_summary, '')) LIKE ?
                    OR LOWER(COALESCE(file_uploads.extracted_summary_kn, '')) LIKE ?
                    OR LOWER(COALESCE(file_uploads.extracted_metadata_json, '')) LIKE ?
                    OR LOWER(COALESCE(file_uploads.fir_reconstruction_xml, '')) LIKE ?
                    OR LOWER(COALESCE(cases.fir_number, '')) LIKE ?
                    OR LOWER(COALESCE(cases.district, '')) LIKE ?
                    OR LOWER(COALESCE(cases.suspect_name, '')) LIKE ?
                    OR LOWER(COALESCE(cases.victim_name, '')) LIKE ?
                    OR LOWER(COALESCE(cases.complainant_name, '')) LIKE ?
                )
                """
            )
            params.extend([like] * 14)
        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        with self.connect() as conn:
            rows = conn.execute(
                f"""
                SELECT file_uploads.*,
                       cases.fir_number AS linked_fir_number,
                       cases.district AS linked_district,
                       cases.sensitivity AS linked_sensitivity
                FROM file_uploads
                LEFT JOIN cases ON cases.id = file_uploads.case_id
                {where_sql}
                ORDER BY file_uploads.uploaded_at DESC, file_uploads.original_filename ASC
                LIMIT ?
                """,
                (*params, safe_limit),
            ).fetchall()
            return [dict(row) for row in rows]

    def create_biometric_challenge(
        self,
        *,
        challenge: str,
        user_id: str | None,
        username: str | None,
        purpose: str,
        rp_id: str,
        origin: str,
        expires_at: str,
    ) -> dict[str, Any]:
        challenge_id = str(uuid.uuid4())
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO biometric_challenges (
                    id, challenge, user_id, username, purpose, rp_id, origin, expires_at, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (challenge_id, challenge, user_id, username, purpose, rp_id, origin, expires_at, utc_now_iso()),
            )
            row = conn.execute("SELECT * FROM biometric_challenges WHERE id = ?", (challenge_id,)).fetchone()
            return dict(row)

    def consume_biometric_challenge(self, challenge: str, purpose: str) -> dict[str, Any] | None:
        now = utc_now_iso()
        with self.connect() as conn:
            row = conn.execute(
                """
                SELECT * FROM biometric_challenges
                WHERE challenge = ? AND purpose = ? AND consumed_at IS NULL AND expires_at >= ?
                """,
                (challenge, purpose, now),
            ).fetchone()
            if not row:
                return None
            conn.execute("UPDATE biometric_challenges SET consumed_at = ? WHERE id = ?", (now, row["id"]))
            return dict(row)

    def create_biometric_credential(
        self,
        *,
        user_id: str,
        credential_id: str,
        public_key_cose: bytes,
        sign_count: int,
        transports: list[str] | None = None,
        label: str | None = None,
    ) -> dict[str, Any]:
        record_id = str(uuid.uuid4())
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO biometric_credentials (
                    id, user_id, credential_id, public_key_cose, sign_count, transports_json, label, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record_id,
                    user_id,
                    credential_id,
                    public_key_cose,
                    sign_count,
                    json.dumps(transports or [], sort_keys=True),
                    label,
                    utc_now_iso(),
                ),
            )
            row = conn.execute("SELECT * FROM biometric_credentials WHERE id = ?", (record_id,)).fetchone()
            return dict(row)

    def list_biometric_credentials_for_user(self, user_id: str) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM biometric_credentials
                WHERE user_id = ? AND is_active = 1
                ORDER BY created_at DESC
                """,
                (user_id,),
            ).fetchall()
            return [dict(row) for row in rows]

    def get_biometric_credential_by_credential_id(self, credential_id: str) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM biometric_credentials WHERE credential_id = ? AND is_active = 1",
                (credential_id,),
            ).fetchone()
            return dict(row) if row else None

    def update_biometric_credential_use(self, credential_id: str, sign_count: int) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                UPDATE biometric_credentials
                SET sign_count = ?, last_used_at = ?
                WHERE credential_id = ?
                """,
                (sign_count, utc_now_iso(), credential_id),
            )

    def _ensure_columns(self, conn: sqlite3.Connection, table: str, columns: dict[str, str]) -> None:
        existing = {row["name"] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
        for name, definition in columns.items():
            if name not in existing:
                conn.execute(f"ALTER TABLE {table} ADD COLUMN {name} {definition}")
            self._ensure_user_roles_allowed(conn)
            self._ensure_column(conn, "cases", "latitude", "REAL")
            self._ensure_column(conn, "cases", "longitude", "REAL")
            self._ensure_column(conn, "cases", "case_type", "TEXT")
            self._ensure_column(conn, "cases", "modus_operandi", "TEXT")
            self._ensure_column(conn, "cases", "incident_at", "TEXT")
            self._ensure_column(conn, "cases", "victim_age", "INTEGER")
            self._ensure_column(conn, "cases", "victim_gender", "TEXT")
            self._ensure_column(conn, "cases", "suspect_age", "INTEGER")
            self._ensure_column(conn, "cases", "suspect_gender", "TEXT")
            self._ensure_column(conn, "cases", "socio_economic_context", "TEXT")
            self._ensure_column(conn, "cases", "urbanization_context", "TEXT")
            self._ensure_column(conn, "cases", "migration_context", "TEXT")
            self._ensure_column(conn, "cases", "education_context", "TEXT")
            self._ensure_column(conn, "cases", "event_context", "TEXT")
            self._ensure_column(conn, "cases", "source_system", "TEXT")
            self._ensure_column(conn, "cases", "source_record_id", "TEXT")
            self._ensure_crime_incident_schema(conn)
        self.rebuild_case_search_index_if_empty()

    def _ensure_column(self, conn: sqlite3.Connection, table: str, column: str, definition: str) -> None:
        columns = {row["name"] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
        if column not in columns:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")

    def _ensure_crime_incident_schema(self, conn: sqlite3.Connection) -> None:
        for column, definition in {
            "grid_lat": "REAL",
            "grid_lon": "REAL",
            "time_bucket": "TEXT",
            "incident_month": "TEXT",
            "incident_year": "INTEGER",
            "incident_hour": "INTEGER",
        }.items():
            self._ensure_column(conn, "crime_incidents", column, definition)

    def _ensure_user_roles_allowed(self, conn: sqlite3.Connection) -> None:
        row = conn.execute(
            "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'users'"
        ).fetchone()
        table_sql = str(row["sql"]) if row else ""
        if "super_admin" in table_sql and "policymaker" in table_sql:
            return
        conn.executescript(
            """
            PRAGMA foreign_keys = OFF;
            CREATE TABLE users_new (
                id TEXT PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('super_admin', 'supervisor', 'investigator', 'analyst', 'policymaker', 'viewer')),
                district TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL
            );
            INSERT INTO users_new (id, username, full_name, role, district, password_hash, is_active, created_at)
            SELECT id, username, full_name, role, district, password_hash, is_active, created_at FROM users;
            DROP TABLE users;
            ALTER TABLE users_new RENAME TO users;
            PRAGMA foreign_keys = ON;
            """
        )

    def user_count(self) -> int:
        with self.connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS total FROM users").fetchone()
            return int(row["total"])

    def create_user(self, user: UserCreate) -> dict[str, Any]:
        user_id = str(uuid.uuid4())
        now = utc_now_iso()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO users
                    (id, username, full_name, role, district, password_hash, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    user.username,
                    user.full_name,
                    user.role,
                    user.district,
                    hash_password(user.password),
                    1 if user.is_active else 0,
                    now,
                ),
            )
            row = conn.execute(
                """
                SELECT id, username, full_name, role, district, password_hash, is_active
                FROM users WHERE id = ?
                """,
                (user_id,),
            ).fetchone()
            return dict(row)

    def list_users(self) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT id, username, full_name, role, district, is_active
                FROM users
                ORDER BY role ASC, username ASC
                """
            ).fetchall()
            return [dict(row) for row in rows]

    def bootstrap_user_if_empty(self, user: UserCreate) -> dict[str, Any] | None:
        if self.user_count() > 0:
            return None
        return self.create_user(user)

    def get_user_by_username(self, username: str) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute(
                """
                SELECT id, username, full_name, role, district, password_hash, is_active
                FROM users WHERE username = ?
                """,
                (username,),
            ).fetchone()
            return dict(row) if row else None

    def get_user_by_id(self, user_id: str) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute(
                """
                SELECT id, username, full_name, role, district, is_active
                FROM users WHERE id = ?
                """,
                (user_id,),
            ).fetchone()
            return dict(row) if row else None

    def update_password_hash(self, user_id: str, password_hash: str) -> None:
        with self.connect() as conn:
            conn.execute(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (password_hash, user_id),
            )

    def update_user(
        self,
        user_id: str,
        *,
        full_name: str | None = None,
        role: str | None = None,
        district: str | None = None,
        is_active: bool | None = None,
    ) -> dict[str, Any] | None:
        updates: list[str] = []
        values: list[Any] = []
        if full_name is not None:
            updates.append("full_name = ?")
            values.append(full_name)
        if role is not None:
            updates.append("role = ?")
            values.append(role)
        if district is not None:
            updates.append("district = ?")
            values.append(district)
        if is_active is not None:
            updates.append("is_active = ?")
            values.append(1 if is_active else 0)
        if not updates:
            return self.get_user_by_id(user_id)
        values.append(user_id)
        with self.connect() as conn:
            conn.execute(f"UPDATE users SET {', '.join(updates)} WHERE id = ?", tuple(values))
            row = conn.execute(
                """
                SELECT id, username, full_name, role, district, is_active
                FROM users WHERE id = ?
                """,
                (user_id,),
            ).fetchone()
            return dict(row) if row else None

    def delete_user(self, user_id: str) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute(
                """
                SELECT id, username, full_name, role, district, is_active
                FROM users WHERE id = ?
                """,
                (user_id,),
            ).fetchone()
            if not row:
                return None
            dependency_counts = conn.execute(
                """
                SELECT
                  (SELECT COUNT(*) FROM conversations WHERE user_id = ?) AS conversations,
                  (SELECT COUNT(*) FROM case_notes WHERE author_user_id = ?) AS case_notes
                """,
                (user_id, user_id),
            ).fetchone()
            conn.execute("UPDATE biometric_credentials SET is_active = 0 WHERE user_id = ?", (user_id,))
            conn.execute(
                "UPDATE biometric_challenges SET consumed_at = ? WHERE user_id = ? AND consumed_at IS NULL",
                (utc_now_iso(), user_id),
            )
            item = dict(row)
            if int(dependency_counts["conversations"]) or int(dependency_counts["case_notes"]):
                conn.execute(
                    """
                    UPDATE users
                    SET username = ?, full_name = ?, is_active = 0
                    WHERE id = ?
                    """,
                    (f"deleted-{user_id[:8]}", "Deleted account", user_id),
                )
                item["delete_mode"] = "deactivated_retained_for_audit"
                return item
            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            item["delete_mode"] = "deleted"
            return item

    def revoke_token(self, jti: str, expires_at: str) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO revoked_tokens (jti, expires_at, revoked_at)
                VALUES (?, ?, ?)
                """,
                (jti, expires_at, utc_now_iso()),
            )

    def is_token_revoked(self, jti: str) -> bool:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT 1 FROM revoked_tokens WHERE jti = ?",
                (jti,),
            ).fetchone()
            return row is not None

    def create_case(self, case: CaseCreate) -> dict[str, Any]:
        case_id = str(uuid.uuid4())
        now = utc_now_iso()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO cases (
                    id, fir_number, year, district, status, case_type, modus_operandi,
                    incident_at, complainant_name, complainant_phone, victim_name,
                    victim_age, victim_gender, suspect_name, suspect_age, suspect_gender,
                    summary, sensitivity, latitude, longitude, socio_economic_context,
                    urbanization_context, migration_context, education_context, event_context,
                    source_system, source_record_id,
                    created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    case_id,
                    case.fir_number,
                    case.year,
                    case.district,
                    case.status,
                    case.case_type,
                    case.modus_operandi,
                    case.incident_at.isoformat() if case.incident_at else None,
                    case.complainant_name,
                    case.complainant_phone,
                    case.victim_name,
                    case.victim_age,
                    case.victim_gender,
                    case.suspect_name,
                    case.suspect_age,
                    case.suspect_gender,
                    case.summary,
                    case.sensitivity,
                    case.latitude,
                    case.longitude,
                    case.socio_economic_context,
                    case.urbanization_context,
                    case.migration_context,
                    case.education_context,
                    case.event_context,
                    case.source_system,
                    case.source_record_id,
                    now,
                    now,
                ),
            )
            row = conn.execute("SELECT * FROM cases WHERE id = ?", (case_id,)).fetchone()
            created = dict(row)
            self._index_case_in_conn(conn, created)
            return created

    def get_case(self, case_id: str) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM cases WHERE id = ?", (case_id,)).fetchone()
            return dict(row) if row else None

    def list_cases(self) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM cases
                ORDER BY updated_at DESC, fir_number ASC
                """
            ).fetchall()
            return [dict(row) for row in rows]

    def update_case_status(self, case_id: str, status: str) -> dict[str, Any] | None:
        now = utc_now_iso()
        with self.connect() as conn:
            conn.execute(
                "UPDATE cases SET status = ?, updated_at = ? WHERE id = ?",
                (status, now, case_id),
            )
            row = conn.execute("SELECT * FROM cases WHERE id = ?", (case_id,)).fetchone()
            if not row:
                return None
            updated = dict(row)
            self._index_case_in_conn(conn, updated)
            return updated

    def search_cases(self, query: str, limit: int = 20) -> dict[str, Any]:
        terms = normalized_search_terms(query)
        safe_limit = max(1, min(limit, 50))
        if not terms:
            return {"terms": [], "results": []}

        hashes = [prefix_hash(term) for term in terms]
        placeholders = ",".join("?" for _ in hashes)
        with self.connect() as conn:
            rows = conn.execute(
                f"""
                SELECT case_id, SUM(weight) AS score, COUNT(DISTINCT prefix_hash) AS matched_terms
                FROM case_search_index
                WHERE prefix_hash IN ({placeholders})
                GROUP BY case_id
                HAVING matched_terms = ?
                ORDER BY score DESC, case_id ASC
                LIMIT ?
                """,
                (*hashes, len(hashes), safe_limit * 10),
            ).fetchall()
            if not rows:
                return {"terms": terms, "results": []}

            scores = {row["case_id"]: int(row["score"]) for row in rows}
            case_ids = list(scores)
            case_placeholders = ",".join("?" for _ in case_ids)
            cases = conn.execute(
                f"SELECT * FROM cases WHERE id IN ({case_placeholders})",
                tuple(case_ids),
            ).fetchall()

        case_by_id = {row["id"]: dict(row) for row in cases}
        ordered = [
            {"case": case_by_id[case_id], "score": scores[case_id]}
            for case_id in case_ids
            if case_id in case_by_id
        ]
        return {"terms": terms, "results": ordered[:safe_limit]}

    def rebuild_case_search_index_if_empty(self) -> None:
        with self.connect() as conn:
            index_count = conn.execute("SELECT COUNT(*) AS total FROM case_search_index").fetchone()
            term_count = conn.execute("SELECT COUNT(*) AS total FROM case_search_terms").fetchone()
            if int(index_count["total"]) > 0 and int(term_count["total"]) > 0:
                return
            conn.execute("DELETE FROM case_search_index")
            conn.execute("DELETE FROM case_search_terms")
            cases = conn.execute("SELECT * FROM cases").fetchall()
            for row in cases:
                self._index_case_in_conn(conn, dict(row))

    def _index_case_in_conn(self, conn: sqlite3.Connection, case: dict[str, Any]) -> None:
        conn.execute("DELETE FROM case_search_index WHERE case_id = ?", (case["id"],))
        entries: dict[tuple[str, str], int] = {}
        weighted_fields = {
            "fir_number": 90,
            "suspect_name": 70,
            "case_type": 68,
            "modus_operandi": 66,
            "district": 60,
            "status": 45,
            "victim_name": 40,
            "victim_gender": 20,
            "suspect_gender": 20,
            "socio_economic_context": 34,
            "urbanization_context": 28,
            "migration_context": 28,
            "education_context": 28,
            "event_context": 28,
            "complainant_name": 35,
            "sensitivity": 30,
            "summary": 15,
            "source_record_id": 85,
            "source_system": 20,
        }
        for field, weight in weighted_fields.items():
            raw_value = str(case.get(field, ""))
            for term in normalized_search_terms(raw_value):
                conn.execute(
                    """
                    INSERT INTO case_search_terms (term, frequency)
                    VALUES (?, 1)
                    ON CONFLICT(term) DO UPDATE SET frequency = frequency + 1
                    """,
                    (term,),
                )
            for prefix in searchable_prefixes(raw_value):
                key = (prefix_hash(prefix), field)
                entries[key] = max(entries.get(key, 0), weight)

        conn.executemany(
            """
            INSERT OR REPLACE INTO case_search_index (prefix_hash, case_id, field, weight)
            VALUES (?, ?, ?, ?)
            """,
            [(hash_value, case["id"], field, weight) for (hash_value, field), weight in entries.items()],
        )

    def case_search_vocabulary(
        self,
        *,
        first_char: str | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        limit: int = 5000,
    ) -> list[str]:
        safe_limit = max(1, min(limit, 20_000))
        clauses: list[str] = []
        params: list[Any] = []
        if first_char:
            clauses.append("substr(term, 1, 1) = ?")
            params.append(first_char.casefold()[:1])
        if min_length is not None:
            clauses.append("length(term) >= ?")
            params.append(max(1, int(min_length)))
        if max_length is not None:
            clauses.append("length(term) <= ?")
            params.append(max(1, int(max_length)))
        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        with self.connect() as conn:
            rows = conn.execute(
                f"""
                SELECT term
                FROM case_search_terms
                {where_sql}
                ORDER BY frequency DESC, term ASC
                LIMIT ?
                """,
                (*params, safe_limit),
            ).fetchall()
            return [str(row["term"]) for row in rows]

    def create_case_note(self, case_id: str, author_user_id: str, body: str) -> dict[str, Any]:
        note_id = str(uuid.uuid4())
        now = utc_now_iso()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO case_notes (id, case_id, author_user_id, body, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (note_id, case_id, author_user_id, body, now),
            )
            row = conn.execute("SELECT * FROM case_notes WHERE id = ?", (note_id,)).fetchone()
            return dict(row)

    def list_case_notes(self, case_id: str) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT case_notes.id, case_notes.case_id, case_notes.author_user_id,
                       case_notes.body, case_notes.created_at, users.username AS author_username
                FROM case_notes
                LEFT JOIN users ON users.id = case_notes.author_user_id
                WHERE case_notes.case_id = ?
                ORDER BY case_notes.created_at ASC, case_notes.id ASC
                """,
                (case_id,),
            ).fetchall()
            return [dict(row) for row in rows]

    def create_conversation(self, user_id: str, title: str) -> dict[str, Any]:
        conversation_id = str(uuid.uuid4())
        now = utc_now_iso()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO conversations (id, user_id, title, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (conversation_id, user_id, title, now, now),
            )
            row = conn.execute(
                "SELECT * FROM conversations WHERE id = ?",
                (conversation_id,),
            ).fetchone()
            return dict(row)

    def get_conversation(self, conversation_id: str) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM conversations WHERE id = ?",
                (conversation_id,),
            ).fetchone()
            return dict(row) if row else None

    def add_conversation_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        message_id = str(uuid.uuid4())
        now = utc_now_iso()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO conversation_messages
                    (id, conversation_id, role, content, metadata_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (message_id, conversation_id, role, content, json.dumps(metadata or {}, sort_keys=True), now),
            )
            conn.execute(
                "UPDATE conversations SET updated_at = ? WHERE id = ?",
                (now, conversation_id),
            )
            row = conn.execute(
                """
                SELECT id, conversation_id, role, content, metadata_json, created_at
                FROM conversation_messages WHERE id = ?
                """,
                (message_id,),
            ).fetchone()
            return _message_from_row(row)

    def list_conversation_messages(self, conversation_id: str) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT id, conversation_id, role, content, metadata_json, created_at
                FROM conversation_messages
                WHERE conversation_id = ?
                ORDER BY created_at ASC, id ASC
                """,
                (conversation_id,),
            ).fetchall()
            return [_message_from_row(row) for row in rows]

    def create_financial_transaction(
        self,
        *,
        occurred_at: str,
        source_account: str,
        target_account: str,
        source_account_holder: str | None = None,
        target_account_holder: str | None = None,
        source_bank_name: str | None = None,
        source_ifsc_code: str | None = None,
        source_branch: str | None = None,
        source_bank_manager_phone: str | None = None,
        target_bank_name: str | None = None,
        target_ifsc_code: str | None = None,
        target_branch: str | None = None,
        target_bank_manager_phone: str | None = None,
        amount: float,
        currency: str,
        district: str,
        case_id: str | None,
        description: str,
    ) -> dict[str, Any]:
        transaction_id = str(uuid.uuid4())
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO financial_transactions (
                    id, occurred_at, source_account, target_account,
                    source_account_holder, target_account_holder,
                    source_bank_name, source_ifsc_code, source_branch, source_bank_manager_phone,
                    target_bank_name, target_ifsc_code, target_branch, target_bank_manager_phone,
                    amount, currency, district, case_id, description
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    transaction_id,
                    occurred_at,
                    source_account,
                    target_account,
                    source_account_holder,
                    target_account_holder,
                    source_bank_name,
                    source_ifsc_code,
                    source_branch,
                    source_bank_manager_phone,
                    target_bank_name,
                    target_ifsc_code,
                    target_branch,
                    target_bank_manager_phone,
                    amount,
                    currency,
                    district,
                    case_id,
                    description,
                ),
            )
            row = conn.execute(
                "SELECT * FROM financial_transactions WHERE id = ?",
                (transaction_id,),
            ).fetchone()
            return dict(row)

    def list_financial_transactions(self) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM financial_transactions
                ORDER BY occurred_at DESC, id ASC
                """
            ).fetchall()
            return [dict(row) for row in rows]

    def reset_crime_incidents(self, source_system: str | None = None) -> None:
        with self.connect() as conn:
            if source_system:
                conn.execute("DELETE FROM crime_incidents WHERE source_system = ?", (source_system,))
            else:
                conn.execute("DELETE FROM crime_incidents")

    def insert_crime_incident_batch(self, rows: list[dict[str, Any]]) -> int:
        if not rows:
            return 0
        now = utc_now_iso()
        values = []
        for row in rows:
            values.append(
                (
                    row["id"],
                    row["source_system"],
                    row["source_record_id"],
                    row.get("reported_at"),
                    row.get("incident_at"),
                    row.get("incident_year"),
                    row.get("incident_month"),
                    row.get("incident_hour"),
                    row.get("time_bucket"),
                    row.get("area_code"),
                    row["district"],
                    row.get("report_district"),
                    row.get("part_code"),
                    row.get("crime_code"),
                    row["crime_type"],
                    row.get("modus_operandi"),
                    row.get("victim_age"),
                    row.get("victim_gender"),
                    row.get("victim_descent"),
                    row.get("premise_code"),
                    row.get("premise_desc"),
                    row.get("weapon_code"),
                    row.get("weapon_desc"),
                    row.get("status_code"),
                    row.get("status_desc"),
                    row.get("location"),
                    row.get("cross_street"),
                    row.get("latitude"),
                    row.get("longitude"),
                    row.get("grid_lat"),
                    row.get("grid_lon"),
                    now,
                )
            )
        with self.connect() as conn:
            before = conn.total_changes
            conn.executemany(
                """
                INSERT OR IGNORE INTO crime_incidents (
                    id, source_system, source_record_id, reported_at, incident_at,
                    incident_year, incident_month, incident_hour, time_bucket,
                    area_code, district, report_district, part_code, crime_code,
                    crime_type, modus_operandi, victim_age, victim_gender,
                    victim_descent, premise_code, premise_desc, weapon_code,
                    weapon_desc, status_code, status_desc, location, cross_street,
                    latitude, longitude, grid_lat, grid_lon, imported_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                values,
            )
            return conn.total_changes - before

    def crime_incident_count(self) -> int:
        with self.connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS total FROM crime_incidents").fetchone()
            return int(row["total"])

    def crime_data_status(self) -> dict[str, Any]:
        with self.connect() as conn:
            status = dict(
                conn.execute(
                    """
                    SELECT
                        COUNT(*) AS imported_count,
                        COALESCE(SUM(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 ELSE 0 END), 0) AS geocoded_count,
                        MIN(incident_at) AS first_incident_at,
                        MAX(incident_at) AS latest_incident_at
                    FROM crime_incidents
                    """
                ).fetchone()
            )
            status["source_systems"] = self._bucket_query(conn, "source_system", "crime_incidents", 10)
            status["by_district"] = self._bucket_query(conn, "district", "crime_incidents", 100)
            status["by_crime_type"] = self._bucket_query(conn, "crime_type", "crime_incidents", 25)
            return status

    def crime_heatmap_rows(self, limit: int = 500) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 2000))
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT
                    grid_lat AS latitude,
                    grid_lon AS longitude,
                    district,
                    crime_type AS top_crime_type,
                    time_bucket AS dominant_time_bucket,
                    COUNT(*) AS incident_count,
                    AVG(CASE WHEN weapon_desc IS NOT NULL AND weapon_desc != '' THEN 1.0 ELSE 0.0 END) AS weapon_share
                FROM crime_incidents
                WHERE grid_lat IS NOT NULL AND grid_lon IS NOT NULL
                GROUP BY grid_lat, grid_lon, district, crime_type, time_bucket
                ORDER BY incident_count DESC, district ASC, crime_type ASC
                LIMIT ?
                """,
                (safe_limit,),
            ).fetchall()
            return [dict(row) for row in rows]

    def recent_baseline_rows(self, recent_start: str, baseline_start: str, limit: int = 500) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 2000))
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT
                    district,
                    crime_type,
                    SUM(CASE WHEN incident_at >= ? THEN 1 ELSE 0 END) AS recent_count,
                    SUM(CASE WHEN incident_at >= ? AND incident_at < ? THEN 1 ELSE 0 END) AS baseline_count,
                    AVG(CASE WHEN incident_hour >= 20 OR incident_hour < 6 THEN 1.0 ELSE 0.0 END) AS night_share,
                    AVG(CASE WHEN weapon_desc IS NOT NULL AND weapon_desc != '' THEN 1.0 ELSE 0.0 END) AS weapon_share
                FROM crime_incidents
                WHERE incident_at IS NOT NULL
                  AND incident_at >= ?
                GROUP BY district, crime_type
                HAVING recent_count > 0
                ORDER BY recent_count DESC, baseline_count DESC
                LIMIT ?
                """,
                (recent_start, baseline_start, recent_start, baseline_start, safe_limit),
            ).fetchall()
            return [dict(row) for row in rows]

    def crime_network_rows(self, limit: int = 120) -> dict[str, list[dict[str, Any]]]:
        safe_limit = max(1, min(limit, 500))
        with self.connect() as conn:
            district_type = conn.execute(
                """
                SELECT district, crime_type, COUNT(*) AS weight
                FROM crime_incidents
                GROUP BY district, crime_type
                ORDER BY weight DESC
                LIMIT ?
                """,
                (safe_limit,),
            ).fetchall()
            type_mo = conn.execute(
                """
                SELECT crime_type, modus_operandi, COUNT(*) AS weight
                FROM crime_incidents
                WHERE modus_operandi IS NOT NULL AND modus_operandi != ''
                GROUP BY crime_type, modus_operandi
                ORDER BY weight DESC
                LIMIT ?
                """,
                (safe_limit,),
            ).fetchall()
            type_premise = conn.execute(
                """
                SELECT crime_type, premise_desc, COUNT(*) AS weight
                FROM crime_incidents
                WHERE premise_desc IS NOT NULL AND premise_desc != ''
                GROUP BY crime_type, premise_desc
                ORDER BY weight DESC
                LIMIT ?
                """,
                (safe_limit,),
            ).fetchall()
            type_weapon = conn.execute(
                """
                SELECT crime_type, weapon_desc, COUNT(*) AS weight
                FROM crime_incidents
                WHERE weapon_desc IS NOT NULL AND weapon_desc != ''
                GROUP BY crime_type, weapon_desc
                ORDER BY weight DESC
                LIMIT ?
                """,
                (safe_limit,),
            ).fetchall()
            return {
                "district_type": [dict(row) for row in district_type],
                "type_mo": [dict(row) for row in type_mo],
                "type_premise": [dict(row) for row in type_premise],
                "type_weapon": [dict(row) for row in type_weapon],
            }

    def crime_incident_intelligence_aggregate(
        self,
        filters: dict[str, Any] | None = None,
        limit: int = 40,
    ) -> dict[str, Any]:
        safe_limit = max(5, min(limit, 100))
        where_sql, params = self._crime_incident_where(filters or {})
        with self.connect() as conn:
            conn.execute("DROP TABLE IF EXISTS temp_scoped_crime_incidents")
            conn.execute(
                f"""
                CREATE TEMP TABLE temp_scoped_crime_incidents AS
                SELECT
                    district, crime_type, modus_operandi, premise_desc, weapon_desc,
                    time_bucket, incident_hour, victim_age, victim_gender, victim_descent,
                    incident_month, incident_at, latitude, longitude, grid_lat, grid_lon
                FROM crime_incidents
                WHERE {where_sql}
                """,
                params,
            )
            summary = dict(
                conn.execute(
                    """
                    SELECT
                        COUNT(*) AS total_incidents,
                        COALESCE(SUM(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 ELSE 0 END), 0) AS geocoded_count,
                        MIN(incident_at) AS first_incident_at,
                        MAX(incident_at) AS latest_incident_at
                    FROM temp_scoped_crime_incidents
                    """,
                ).fetchone()
            )
            top_patterns = conn.execute(
                """
                SELECT
                    district,
                    crime_type,
                    COALESCE(NULLIF(modus_operandi, ''), 'unknown') AS modus_operandi,
                    COALESCE(NULLIF(premise_desc, ''), 'unknown') AS premise_desc,
                    COALESCE(NULLIF(weapon_desc, ''), 'none') AS weapon_desc,
                    COALESCE(NULLIF(time_bucket, ''), 'unknown') AS time_bucket,
                    COUNT(*) AS incident_count,
                    AVG(CASE WHEN incident_hour >= 20 OR incident_hour < 6 THEN 1.0 ELSE 0.0 END) AS night_share,
                    AVG(CASE WHEN weapon_desc IS NOT NULL AND weapon_desc != '' THEN 1.0 ELSE 0.0 END) AS weapon_share,
                    AVG(CASE WHEN victim_age IS NOT NULL AND victim_age >= 0 THEN victim_age ELSE NULL END) AS average_victim_age
                FROM temp_scoped_crime_incidents
                GROUP BY district, crime_type, modus_operandi, premise_desc, weapon_desc, time_bucket
                ORDER BY incident_count DESC, district ASC, crime_type ASC
                LIMIT ?
                """,
                (safe_limit,),
            ).fetchall()
            heat_clusters = conn.execute(
                """
                SELECT
                    grid_lat AS latitude,
                    grid_lon AS longitude,
                    district,
                    crime_type AS top_crime_type,
                    time_bucket AS dominant_time_bucket,
                    COUNT(*) AS incident_count,
                    AVG(CASE WHEN weapon_desc IS NOT NULL AND weapon_desc != '' THEN 1.0 ELSE 0.0 END) AS weapon_share
                FROM temp_scoped_crime_incidents
                WHERE grid_lat IS NOT NULL
                  AND grid_lon IS NOT NULL
                GROUP BY grid_lat, grid_lon, district, crime_type, time_bucket
                ORDER BY incident_count DESC, district ASC, crime_type ASC
                LIMIT ?
                """,
                (safe_limit,),
            ).fetchall()
            age_bands = conn.execute(
                """
                SELECT
                    CASE
                        WHEN victim_age IS NULL OR victim_age < 0 THEN 'unknown'
                        WHEN victim_age < 18 THEN 'minor'
                        WHEN victim_age BETWEEN 18 AND 24 THEN '18-24'
                        WHEN victim_age BETWEEN 25 AND 44 THEN '25-44'
                        WHEN victim_age BETWEEN 45 AND 64 THEN '45-64'
                        ELSE '65+'
                    END AS key,
                    COUNT(*) AS count
                FROM temp_scoped_crime_incidents
                GROUP BY key
                ORDER BY count DESC, key ASC
                LIMIT 12
                """,
            ).fetchall()
            network_edges = {
                "district_type": self._incident_edge_query(
                    conn, "district", "crime_type", "1 = 1", (), safe_limit, table="temp_scoped_crime_incidents"
                ),
                "type_mo": self._incident_edge_query(
                    conn, "crime_type", "modus_operandi", "1 = 1", (), safe_limit, table="temp_scoped_crime_incidents"
                ),
                "type_premise": self._incident_edge_query(
                    conn, "crime_type", "premise_desc", "1 = 1", (), safe_limit, table="temp_scoped_crime_incidents"
                ),
                "type_weapon": self._incident_edge_query(
                    conn, "crime_type", "weapon_desc", "1 = 1", (), safe_limit, table="temp_scoped_crime_incidents"
                ),
                "type_time": self._incident_edge_query(
                    conn, "crime_type", "time_bucket", "1 = 1", (), safe_limit, table="temp_scoped_crime_incidents"
                ),
            }

            return {
                **summary,
                "filters": filters or {},
                "by_district": self._incident_bucket_query(
                    conn, "district", "1 = 1", (), 25, table="temp_scoped_crime_incidents"
                ),
                "by_crime_type": self._incident_bucket_query(
                    conn, "crime_type", "1 = 1", (), 25, table="temp_scoped_crime_incidents"
                ),
                "by_modus_operandi": self._incident_bucket_query(
                    conn, "modus_operandi", "1 = 1", (), 25, table="temp_scoped_crime_incidents"
                ),
                "by_premise": self._incident_bucket_query(
                    conn, "premise_desc", "1 = 1", (), 25, table="temp_scoped_crime_incidents"
                ),
                "by_weapon": self._incident_bucket_query(
                    conn, "weapon_desc", "1 = 1", (), 25, table="temp_scoped_crime_incidents"
                ),
                "by_time_bucket": self._incident_bucket_query(
                    conn, "time_bucket", "1 = 1", (), 12, table="temp_scoped_crime_incidents"
                ),
                "by_victim_gender": self._incident_bucket_query(
                    conn, "victim_gender", "1 = 1", (), 12, table="temp_scoped_crime_incidents"
                ),
                "by_victim_descent": self._incident_bucket_query(
                    conn, "victim_descent", "1 = 1", (), 20, table="temp_scoped_crime_incidents"
                ),
                "by_month": self._incident_bucket_query(
                    conn, "incident_month", "1 = 1", (), 24, table="temp_scoped_crime_incidents"
                ),
                "victim_age_bands": [dict(row) for row in age_bands],
                "top_patterns": [dict(row) for row in top_patterns],
                "heat_clusters": [dict(row) for row in heat_clusters],
                "network_edges": network_edges,
            }

    def _crime_incident_where(self, filters: dict[str, Any]) -> tuple[str, tuple[Any, ...]]:
        clauses = ["1 = 1"]
        params: list[Any] = []
        scope_district = _clean_filter(filters.get("scope_district"))
        requested_district = _clean_filter(filters.get("district"))
        if scope_district and requested_district and scope_district.casefold() != requested_district.casefold():
            clauses.append("0 = 1")
        elif requested_district:
            clauses.append("district = ?")
            params.append(requested_district)
        elif scope_district:
            clauses.append("district = ?")
            params.append(scope_district)

        terms = [term.casefold() for term in filters.get("terms", []) if _clean_filter(term)]
        term_clauses = []
        for term in terms[:6]:
            pattern = f"%{term}%"
            term_clauses.append(
                """
                (
                    LOWER(district) LIKE ?
                    OR LOWER(crime_type) LIKE ?
                    OR LOWER(modus_operandi) LIKE ?
                    OR LOWER(premise_desc) LIKE ?
                    OR LOWER(weapon_desc) LIKE ?
                    OR LOWER(status_desc) LIKE ?
                    OR LOWER(location) LIKE ?
                )
                """
            )
            params.extend([pattern] * 7)
        if term_clauses:
            clauses.append(" AND ".join(term_clauses))

        time_buckets = [_clean_filter(value) for value in filters.get("time_buckets", [])]
        time_buckets = [value for value in time_buckets if value]
        if time_buckets:
            placeholders = ",".join("?" for _ in time_buckets)
            clauses.append(f"time_bucket IN ({placeholders})")
            params.extend(time_buckets)

        victim_gender = _clean_filter(filters.get("victim_gender"))
        if victim_gender:
            clauses.append("victim_gender = ?")
            params.append(victim_gender)

        victim_age_min = filters.get("victim_age_min")
        if victim_age_min is not None:
            clauses.append("victim_age >= ?")
            params.append(int(victim_age_min))
        victim_age_max = filters.get("victim_age_max")
        if victim_age_max is not None:
            clauses.append("victim_age <= ?")
            params.append(int(victim_age_max))

        return " AND ".join(clauses), tuple(params)

    def _incident_bucket_query(
        self,
        conn: sqlite3.Connection,
        field: str,
        where_sql: str,
        params: tuple[Any, ...],
        limit: int,
        table: str = "crime_incidents",
    ) -> list[dict[str, Any]]:
        if field not in _CRIME_INCIDENT_BUCKET_FIELDS:
            raise ValueError(f"Unsupported incident bucket field: {field}")
        if table not in {"crime_incidents", "temp_scoped_crime_incidents"}:
            raise ValueError(f"Unsupported incident table: {table}")
        rows = conn.execute(
            f"""
            SELECT {field} AS key, COUNT(*) AS count
            FROM {table}
            WHERE {where_sql}
              AND {field} IS NOT NULL
              AND {field} != ''
            GROUP BY {field}
            ORDER BY count DESC, key ASC
            LIMIT ?
            """,
            (*params, max(1, min(limit, 100))),
        ).fetchall()
        return [dict(row) for row in rows]

    def _incident_edge_query(
        self,
        conn: sqlite3.Connection,
        source_field: str,
        target_field: str,
        where_sql: str,
        params: tuple[Any, ...],
        limit: int,
        table: str = "crime_incidents",
    ) -> list[dict[str, Any]]:
        if source_field not in _CRIME_INCIDENT_BUCKET_FIELDS or target_field not in _CRIME_INCIDENT_BUCKET_FIELDS:
            raise ValueError("Unsupported incident edge fields")
        if table not in {"crime_incidents", "temp_scoped_crime_incidents"}:
            raise ValueError(f"Unsupported incident table: {table}")
        rows = conn.execute(
            f"""
            SELECT {source_field} AS source, {target_field} AS target, COUNT(*) AS weight
            FROM {table}
            WHERE {where_sql}
              AND {source_field} IS NOT NULL
              AND {source_field} != ''
              AND {target_field} IS NOT NULL
              AND {target_field} != ''
            GROUP BY {source_field}, {target_field}
            ORDER BY weight DESC, source ASC, target ASC
            LIMIT ?
            """,
            (*params, max(1, min(limit, 100))),
        ).fetchall()
        return [dict(row) for row in rows]

    def _bucket_query(
        self,
        conn: sqlite3.Connection,
        field: str,
        table: str,
        limit: int,
    ) -> list[dict[str, Any]]:
        rows = conn.execute(
            f"""
            SELECT {field} AS key, COUNT(*) AS count
            FROM {table}
            WHERE {field} IS NOT NULL AND {field} != ''
            GROUP BY {field}
            ORDER BY count DESC, key ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]

    def latest_audit_hash(self) -> str | None:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT entry_hash FROM audit_logs ORDER BY id DESC LIMIT 1"
            ).fetchone()
            return str(row["entry_hash"]) if row else None

    def create_rate_limit_alert(
        self,
        *,
        actor_user_id: str | None,
        actor_username: str | None,
        actor_role: str | None,
        client_ip: str | None,
        method: str,
        path: str,
        limit_per_minute: int,
        window_seconds: int,
        request_count: int,
        request_id: str | None,
    ) -> dict[str, Any]:
        with self.connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO rate_limit_alerts (
                    created_at, actor_user_id, actor_username, actor_role,
                    client_ip, method, path, limit_per_minute, window_seconds,
                    request_count, request_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    utc_now_iso(),
                    actor_user_id,
                    actor_username,
                    actor_role,
                    client_ip,
                    method,
                    path,
                    limit_per_minute,
                    window_seconds,
                    request_count,
                    request_id,
                ),
            )
            row = conn.execute(
                "SELECT * FROM rate_limit_alerts WHERE id = ?",
                (cursor.lastrowid,),
            ).fetchone()
            return dict(row)

    def list_rate_limit_alerts(
        self,
        limit: int = 50,
        *,
        include_acknowledged: bool = False,
    ) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        where = "" if include_acknowledged else "WHERE acknowledged_at IS NULL"
        with self.connect() as conn:
            rows = conn.execute(
                f"""
                SELECT * FROM rate_limit_alerts
                {where}
                ORDER BY id DESC
                LIMIT ?
                """,
                (safe_limit,),
            ).fetchall()
            return [dict(row) for row in rows]

    def acknowledge_rate_limit_alert(self, alert_id: int, acknowledged_by: str) -> dict[str, Any] | None:
        with self.connect() as conn:
            conn.execute(
                """
                UPDATE rate_limit_alerts
                SET acknowledged_at = COALESCE(acknowledged_at, ?),
                    acknowledged_by = COALESCE(acknowledged_by, ?)
                WHERE id = ?
                """,
                (utc_now_iso(), acknowledged_by, alert_id),
            )
            row = conn.execute(
                "SELECT * FROM rate_limit_alerts WHERE id = ?",
                (alert_id,),
            ).fetchone()
            return dict(row) if row else None

    def insert_audit_log(self, entry: dict[str, Any]) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO audit_logs (
                    created_at, actor_user_id, actor_username, actor_role, action,
                    resource_type, resource_id, status, ip_address, user_agent,
                    request_id, detail_json, prev_hash, entry_hash
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entry["created_at"],
                    entry.get("actor_user_id"),
                    entry.get("actor_username"),
                    entry.get("actor_role"),
                    entry["action"],
                    entry["resource_type"],
                    entry.get("resource_id"),
                    entry["status"],
                    entry.get("ip_address"),
                    entry.get("user_agent"),
                    entry.get("request_id"),
                    json.dumps(entry.get("detail", {}), sort_keys=True),
                    entry.get("prev_hash"),
                    entry["entry_hash"],
                ),
            )

    def list_audit_logs(self, limit: int = 100) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT id, created_at, actor_user_id, actor_username, actor_role,
                       action, resource_type, resource_id, status, request_id, entry_hash
                FROM audit_logs
                ORDER BY id DESC
                LIMIT ?
                """,
                (safe_limit,),
            ).fetchall()
            return [dict(row) for row in rows]

    def list_user_activity(self, user_id: str, limit: int = 100) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT id, created_at, actor_user_id, actor_username, actor_role,
                       action, resource_type, resource_id, status, request_id,
                       detail_json, entry_hash
                FROM audit_logs
                WHERE actor_user_id = ?
                   OR (resource_type = 'user' AND resource_id = ?)
                ORDER BY id DESC
                LIMIT ?
                """,
                (user_id, user_id, safe_limit),
            ).fetchall()
            events: list[dict[str, Any]] = []
            for row in rows:
                item = dict(row)
                try:
                    item["detail"] = json.loads(item.pop("detail_json") or "{}")
                except (TypeError, json.JSONDecodeError):
                    item["detail"] = {}
                events.append(item)
            return events

    def iter_audit_logs(self) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT id, created_at, actor_user_id, actor_username, actor_role,
                       action, resource_type, resource_id, status, ip_address,
                       user_agent, request_id, detail_json, prev_hash, entry_hash
                FROM audit_logs
                ORDER BY id ASC
                """
            ).fetchall()
            return [dict(row) for row in rows]


def normalized_search_terms(query: str) -> list[str]:
    terms = []
    for raw in re.findall(r"[^\W_]+", query.casefold(), flags=re.UNICODE):
        if len(raw) >= 2:
            terms.append(raw[:64])
    return terms[:24]


def searchable_prefixes(text: str) -> set[str]:
    prefixes: set[str] = set()
    for term in normalized_search_terms(text):
        max_prefix = min(len(term), 32)
        for length in range(2, max_prefix + 1):
            prefixes.add(term[:length])
    return prefixes


def prefix_hash(prefix: str) -> str:
    return hashlib.sha256(prefix.casefold().encode("utf-8")).hexdigest()
