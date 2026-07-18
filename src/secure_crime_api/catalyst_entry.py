from __future__ import annotations

import os

import uvicorn


def _listen_port() -> int:
    for key in ("X_ZOHO_CATALYST_LISTEN_PORT", "PORT", "SECURE_API_PORT"):
        value = os.getenv(key)
        if value:
            return int(value)
    return 8000


def main() -> None:
    uvicorn.run(
        "secure_crime_api.app:app",
        host=os.getenv("SECURE_API_HOST", "0.0.0.0"),
        port=_listen_port(),
        proxy_headers=True,
        forwarded_allow_ips=os.getenv("SECURE_API_FORWARDED_ALLOW_IPS", "*"),
    )


if __name__ == "__main__":
    main()
