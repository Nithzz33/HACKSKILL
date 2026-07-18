# Zoho Catalyst AppSail Deployment

This project is a FastAPI web service with its frontend mounted from the same app, so the right Catalyst target is AppSail.

## What Was Made Catalyst-Ready

- `catalyst_app.py` is the AppSail entry file.
- `secure_crime_api.catalyst_entry` starts Uvicorn on `X_ZOHO_CATALYST_LISTEN_PORT`, which AppSail checks at runtime.
- `SECURE_API_DEMO_MODE=true` seeds evaluator users, demo/template FIRs, money-trail records, and aggregate crime incidents into a clean database.
- `.dockerignore` keeps local SQLite data, logs, and browser profiles out of deployment images.
- `scripts/build_catalyst_appsail.py` creates a compact managed-runtime bundle in `dist/catalyst-appsail`.

## Recommended Hackathon Path

Use AppSail as a Catalyst-managed Python 3.12 runtime.

1. Create and test locally:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\python -m pip install --upgrade pip
   .\.venv\Scripts\pip install -r requirements.txt
   $env:PYTHONPATH="src"
   $env:X_ZOHO_CATALYST_LISTEN_PORT="9000"
   $env:SECURE_API_ENVIRONMENT="production"
   $env:SECURE_API_DATABASE_PATH="$env:TEMP\ksp_secure_system_demo.db"
   $env:SECURE_API_JWT_SECRET="replace-with-a-long-random-demo-secret-123456"
   $env:SECURE_API_ALLOWED_HOSTS="localhost,127.0.0.1"
   $env:SECURE_API_DEMO_MODE="true"
   .\.venv\Scripts\python.exe catalyst_app.py
   ```

2. Open `http://127.0.0.1:9000`.

3. Build the AppSail bundle:

   ```powershell
   .\.venv\Scripts\python.exe scripts\build_catalyst_appsail.py
   ```

   For the managed runtime, install dependencies into the bundle from Linux or WSL so native wheels match Catalyst's Linux runtime:

   ```bash
   python3 scripts/build_catalyst_appsail.py --install-dependencies
   ```

4. Initialize or add an AppSail service with the Catalyst CLI. Choose:

   - Runtime type: Catalyst-Managed Runtime
   - Stack: Python 3.12
   - Build path: the absolute path to `dist/catalyst-appsail`
   - Startup command: `python3 -u catalyst_app.py`

5. After the CLI creates `app-config.json`, copy the environment variables from `app-config.managed.example.json` and replace `SECURE_API_JWT_SECRET` with a strong project secret.

6. Deploy the AppSail service:

   ```powershell
   catalyst deploy --only appsail
   ```

## Safer Dependency Path

This app uses native Python packages such as numpy, pandas, matplotlib, kaleido, and PyMuPDF. If a managed-runtime upload built from Windows gives native wheel errors, deploy as an AppSail custom runtime using the checked-in Dockerfile:

```powershell
docker build --platform linux/amd64 -t ksp-catalyst-appsail:latest .
```

Then initialize AppSail as a Docker Image or Docker Archive in the Catalyst CLI. The Dockerfile already runs `python -m secure_crime_api.catalyst_entry`, which respects `X_ZOHO_CATALYST_LISTEN_PORT`.

## Demo Users

When `SECURE_API_DEMO_MODE=true`, these evaluator users are available:

| Username | Password | Role |
| --- | --- | --- |
| `superadmin` | `admin123` | Super Admin |
| `supervisor` | `admin123` | Supervisor |
| `investigator` | `admin123` | Investigator |
| `analyst` | `admin123` | Analyst |
| `policymaker` | `admin123` | Policymaker |
| `viewer` | `admin123` | Viewer |
| `admin` | `SecureAdminPassword123!` | Bootstrap Admin |

Demo records are clearly marked as demo/template data in summaries and should be replaced with approved competition or official records before any real-world use.
