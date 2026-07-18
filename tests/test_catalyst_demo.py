from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from secure_crime_api.app import create_app
from secure_crime_api.config import Settings


def test_catalyst_demo_mode_seeds_evaluator_workflow(tmp_path: Path) -> None:
    settings = Settings(
        environment="production",
        database_path=tmp_path / "catalyst-demo.db",
        jwt_secret="test-secret-that-is-long-enough-for-hs256",
        allowed_hosts="testserver",
        rate_limit_per_minute=1_000,
        demo_mode=True,
        demo_password="admin123",
    )
    app = create_app(settings=settings)

    with TestClient(app) as client:
        login = client.post("/auth/login", json={"username": "superadmin", "password": "admin123"})
        assert login.status_code == 200
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        cases = client.get("/cases", headers=headers)
        assert cases.status_code == 200
        fir_numbers = {case["fir_number"] for case in cases.json()}
        assert {"BLR-CYB-042", "MYS-BRK-011", "UDU-CHN-022"}.issubset(fir_numbers)

        network = client.get("/analytics/network", headers=headers)
        assert network.status_code == 200
        labels = {node["label"] for node in network.json()["nodes"]}
        assert {"Pooja Naik", "Karnataka Cooperative Bank", "IN-BLR-MULE-1001"}.issubset(labels)

        advanced = client.get("/analytics/advanced-crime", headers=headers)
        assert advanced.status_code == 200
        body = advanced.json()
        assert body["imported_count"] >= 20
        assert body["heatmap_points"]
