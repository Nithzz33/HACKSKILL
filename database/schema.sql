CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('super_admin', 'supervisor', 'investigator', 'analyst', 'policymaker', 'viewer')),
    district TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS cases (
    id UUID PRIMARY KEY,
    fir_number TEXT NOT NULL,
    year INTEGER NOT NULL,
    district TEXT NOT NULL,
    status TEXT NOT NULL,
    case_type TEXT,
    modus_operandi TEXT,
    incident_at TIMESTAMPTZ,
    complainant_name TEXT NOT NULL,
    complainant_phone TEXT NOT NULL,
    victim_name TEXT NOT NULL,
    victim_age INTEGER,
    victim_gender TEXT,
    suspect_name TEXT NOT NULL,
    suspect_age INTEGER,
    suspect_gender TEXT,
    summary TEXT NOT NULL,
    sensitivity TEXT NOT NULL,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    socio_economic_context TEXT,
    urbanization_context TEXT,
    migration_context TEXT,
    education_context TEXT,
    event_context TEXT,
    source_system TEXT,
    source_record_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (fir_number, year)
);

CREATE TABLE IF NOT EXISTS case_search_index (
    prefix_hash TEXT NOT NULL,
    case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    field TEXT NOT NULL,
    weight INTEGER NOT NULL,
    PRIMARY KEY (prefix_hash, case_id, field)
);

CREATE TABLE IF NOT EXISTS case_notes (
    id UUID PRIMARY KEY,
    case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    author_user_id UUID NOT NULL REFERENCES users(id),
    body TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    title TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS conversation_messages (
    id UUID PRIMARY KEY,
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS financial_transactions (
    id UUID PRIMARY KEY,
    occurred_at TIMESTAMPTZ NOT NULL,
    source_account TEXT NOT NULL,
    target_account TEXT NOT NULL,
    amount NUMERIC(14, 2) NOT NULL,
    currency TEXT NOT NULL,
    district TEXT NOT NULL,
    case_id UUID REFERENCES cases(id) ON DELETE SET NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS crime_incidents (
    id TEXT PRIMARY KEY,
    source_system TEXT NOT NULL,
    source_record_id TEXT NOT NULL,
    reported_at TIMESTAMPTZ,
    incident_at TIMESTAMPTZ,
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
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    grid_lat DOUBLE PRECISION,
    grid_lon DOUBLE PRECISION,
    imported_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (source_system, source_record_id)
);

CREATE TABLE IF NOT EXISTS revoked_tokens (
    jti TEXT PRIMARY KEY,
    expires_at TIMESTAMPTZ NOT NULL,
    revoked_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS rate_limit_alerts (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    actor_user_id UUID,
    actor_username TEXT,
    actor_role TEXT,
    client_ip INET,
    method TEXT NOT NULL,
    path TEXT NOT NULL,
    limit_per_minute INTEGER NOT NULL,
    window_seconds INTEGER NOT NULL,
    request_count INTEGER NOT NULL,
    request_id TEXT,
    acknowledged_at TIMESTAMPTZ,
    acknowledged_by TEXT
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    actor_user_id UUID,
    actor_username TEXT,
    actor_role TEXT,
    action TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    resource_id TEXT,
    status TEXT NOT NULL,
    ip_address INET,
    user_agent TEXT,
    request_id TEXT,
    detail_json JSONB NOT NULL,
    prev_hash TEXT,
    entry_hash TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_cases_district ON cases(district);
CREATE INDEX IF NOT EXISTS idx_case_search_prefix ON case_search_index(prefix_hash, weight DESC);
CREATE INDEX IF NOT EXISTS idx_audit_hash ON audit_logs(entry_hash);
CREATE INDEX IF NOT EXISTS idx_financial_district ON financial_transactions(district);
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
