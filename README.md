# HACKSKILL

## Secure Crime Intelligence API

This repository contains a secure backend foundation for a crime analytics and conversational intelligence platform. It focuses on the security control plane first: authentication, authorization, auditability, PII handling, official-data ingestion, and safe API defaults.

## What Is Built

- FastAPI service with security headers, request-size limits, and in-memory rate limiting on API endpoints.
- Argon2 password hashing and short-lived signed JWT access tokens.
- Token revocation on logout.
- Role-based access control for super admin, supervisor, investigator, analyst, and viewer roles.
- District and sensitivity row-level checks for case access.
- Role-aware PII masking for case data.
- SQLite persistence with parameterized queries.
- Official-record import endpoint with provenance fields.
- Hash-prefix indexed typeahead search for large case collections.
- Super admin dashboard/API for user creation, updates, activation control, and password resets.
- Super admin rate-limit breach alerts showing authenticated users or unauthenticated client IPs.
- Leaflet geographic map with OpenStreetMap tiles, official-coordinate markers, local heat layer, and optional Google Maps mode.
- Append-only audit log with a hash chain and integrity verification.
- Tests for login, RBAC, masking, revocation, audit integrity, and case access boundaries.
- Conversational intelligence endpoint with evidence-bound answers.
- Conversation sessions with PDF export.
- Local English/Kannada translation adapter fallback.
- Network graph projection from accessible case records.
- Trend, sociological, forecasting, financial, suspect-profile, decision-support, and explainability modules.
- Production-shape Docker Compose stack with PostgreSQL/PostGIS, Neo4j, Elasticsearch, MinIO, Prometheus, and Grafana service definitions.

## Implemented Module Map

| Module from brief | Endpoint(s) |
| --- | --- |
| Chat interface | `POST /intelligence/query`, `POST /conversations/{id}/messages` |
| Multi-lingual support | `POST /translate` |
| Voice/PDF support | Voice-ready API boundary, `GET /conversations/{id}/export.pdf` |
| Network analysis | `GET /analytics/network` |
| Trend analytics | `GET /analytics/trends` |
| Geospatial mapping | Leaflet frontend, optional Google Maps, `GET /cases` |
| Hash-prefix search | `GET /cases/search` |
| Sociological insights | `GET /analytics/sociological` |
| Offender profiling | `GET /profiles/suspects/{suspect_name}` |
| Decision support | `GET /decision-support/cases/{case_id}` |
| Financial analysis | `GET /financial/analysis` |
| Forecasting | `GET /forecast/hotspots` |
| Explainable AI | `GET /explain/cases/{case_id}` |
| RBAC/audit/masking/rate limits | `POST /auth/login`, `POST /auth/logout`, `GET /audit/*`, `GET /admin/rate-limit-alerts` |
| Super admin user management | `GET /admin/users`, `POST /admin/users`, `PATCH /admin/users/{id}`, `GET /admin/users/{id}/activity`, `POST /admin/users/{id}/reset-password`, `DELETE /admin/users/{id}` |

`GET /modules` returns the live module catalog and implementation status.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set `SECURE_API_JWT_SECRET` to a long random value. For first setup only, provide a bootstrap administrator:

```text
SECURE_API_BOOTSTRAP_USERNAME=<authorized-admin-username>
SECURE_API_BOOTSTRAP_PASSWORD=<strong-temporary-password>
SECURE_API_BOOTSTRAP_FULL_NAME=<administrator-name>
```

Then run:

```powershell
.\.venv\Scripts\uvicorn secure_crime_api.app:app --app-dir src --reload
```

Open:

- API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

Remove the bootstrap credentials from `.env` after the first account is created.

## Zoho Catalyst AppSail Hosting

This repository is ready to host as a Zoho Catalyst AppSail service. The deployed app serves the FastAPI backend and the static frontend from one process.

- AppSail entrypoint: [catalyst_app.py](C:/Users/saini/OneDrive/Documents/ksp/catalyst_app.py)
- Deployment guide: [deploy/zoho-catalyst/README.md](C:/Users/saini/OneDrive/Documents/ksp/deploy/zoho-catalyst/README.md)
- Example managed-runtime config: [deploy/zoho-catalyst/app-config.managed.example.json](C:/Users/saini/OneDrive/Documents/ksp/deploy/zoho-catalyst/app-config.managed.example.json)

For a hackathon demo, set:

```text
SECURE_API_DEMO_MODE=true
SECURE_API_DEMO_PASSWORD=admin123
```

That seeds evaluator accounts and demo/template FIR, analytics, and money-trail records into a clean database. Use `superadmin` / `admin123` to demonstrate all modules.

Build the Catalyst managed-runtime bundle with:

```powershell
.\.venv\Scripts\python.exe scripts\build_catalyst_appsail.py
```

If native Python wheels cause deployment issues, use the Dockerfile as an AppSail custom runtime image.

## Zoho Catalyst Slate Static Demo

The repository root also contains a Slate-compatible static demo:

- [index.html](C:/Users/saini/OneDrive/Documents/ksp/index.html)
- [static/demo-data.json](C:/Users/saini/OneDrive/Documents/ksp/static/demo-data.json)

This prevents the Slate preview from showing 404 when the project is deployed as a static site. On `*.onslate.in`, the frontend automatically switches to static demo mode, supports evaluator login, populates dashboards from bundled demo records, and answers the chatbot prompt `forecast the crime for next 7 days`.

Use Slate for the quick hackathon preview URL. Use AppSail for the full live FastAPI backend with authentication, persistence, imports, audit writes, and PDF/export APIs.

## Official Data

No mock operational records are seeded by the application. Load Karnataka State Police data only from an authorized source using `POST /cases/import`.

Each imported record can include:

- FIR number, year, district, status, sensitivity
- complainant, victim, suspect, and summary fields
- optional `latitude` and `longitude` for map/heatmap rendering
- `source_system` and `source_record_id` for provenance

The frontend uses Leaflet as the default geographic map and renders only coordinates present in authorized case records. Google Maps remains optional and is loaded only when an API key is entered in the map panel.

## Example Import Shape

```json
{
  "source_system": "authorized-ksp-source",
  "records": [
    {
      "fir_number": "OFFICIAL-FIR-NUMBER",
      "year": 2026,
      "district": "OFFICIAL-DISTRICT",
      "status": "open",
      "complainant_name": "OFFICIAL-VALUE",
      "complainant_phone": "OFFICIAL-VALUE",
      "victim_name": "OFFICIAL-VALUE",
      "suspect_name": "OFFICIAL-VALUE",
      "summary": "OFFICIAL-VALUE",
      "sensitivity": "standard",
      "latitude": null,
      "longitude": null,
      "source_record_id": "OFFICIAL-SOURCE-ID"
    }
  ]
}
```

## Test

```powershell
.\.venv\Scripts\pytest
```

## Production-Shape Stack

The local API uses SQLite for development. The repo also includes production-oriented scaffolding:

- [docker-compose.prod.yml](C:/Users/saini/OneDrive/Documents/ksp/docker-compose.prod.yml)
- [database/schema.sql](C:/Users/saini/OneDrive/Documents/ksp/database/schema.sql)
- [database/neo4j_schema.cypher](C:/Users/saini/OneDrive/Documents/ksp/database/neo4j_schema.cypher)
- [monitoring/prometheus.yml](C:/Users/saini/OneDrive/Documents/ksp/monitoring/prometheus.yml)

Run it with:

```powershell
docker compose -f docker-compose.prod.yml up --build
```

## Production Notes

- Set `SECURE_API_ENVIRONMENT=production`.
- Use a strong unique `SECURE_API_JWT_SECRET`.
- Place the service behind TLS.
- Replace SQLite with PostgreSQL before multi-instance deployment.
- Partition or shard `case_search_index` by prefix hash for very large datasets.
- Move rate limiting and token revocation storage to Redis or the primary database for horizontally scaled deployments.
- Keep unauthenticated IP/device blocking at the edge proxy as well as in the API process for production deployments.
- Send audit logs to append-only storage or a SIEM.
- Connect approved production adapters for NLLB/IndicTrans translation, ASR/TTS, Neo4j graph queries, Elastic search, object storage, and model serving.
- The suspect profile and forecast modules are intentionally evidence-bound and aggregate-focused. They do not make autonomous guilt, criminality, or recidivism determinations.
