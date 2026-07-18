from __future__ import annotations

import sqlite3
import io
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from secure_crime_api import app as app_module
from secure_crime_api.app import create_app
from secure_crime_api.config import Settings
from secure_crime_api.intent_taxonomy import classify_master_intent, taxonomy_status
from secure_crime_api.kannada_lexicon import load_kannada_lexicon, normalize_kannada_query
from secure_crime_api.models import CaseCreate, UserCreate
from secure_crime_api.storage import Database


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    settings = Settings(
        environment="test",
        database_path=tmp_path / "test.db",
        jwt_secret="test-secret-that-is-long-enough-for-hs256",
        rate_limit_per_minute=1_000,
        allowed_hosts="testserver",
    )
    db = Database(settings.database_path)
    db.init_schema()
    for user in [
        UserCreate(
            username="superadmin",
            password="StrongPassword!123",
            full_name="Super Admin",
            role="super_admin",
            district="state",
        ),
        UserCreate(
            username="supervisor",
            password="StrongPassword!123",
            full_name="Supervisor",
            role="supervisor",
            district="state",
        ),
        UserCreate(
            username="investigator",
            password="StrongPassword!123",
            full_name="Investigator",
            role="investigator",
            district="Bengaluru",
        ),
        UserCreate(
            username="analyst",
            password="StrongPassword!123",
            full_name="Analyst",
            role="analyst",
            district="Bengaluru",
        ),
        UserCreate(
            username="policymaker",
            password="StrongPassword!123",
            full_name="Policymaker",
            role="policymaker",
            district="state",
        ),
        UserCreate(
            username="viewer",
            password="StrongPassword!123",
            full_name="Viewer",
            role="viewer",
            district="Bengaluru",
        ),
    ]:
        db.create_user(user)

    for case in [
        CaseCreate(
            fir_number="BLR-001",
            year=2026,
            district="Bengaluru",
            status="open",
            complainant_name="Asha Rao",
            complainant_phone="+91-9876543210",
            victim_name="Kiran Rao",
            suspect_name="Ravi Kumar",
            summary="Standard Bengaluru case",
            sensitivity="standard",
        ),
        CaseCreate(
            fir_number="BLR-002",
            year=2026,
            district="Bengaluru",
            status="open",
            complainant_name="Meera Iyer",
            complainant_phone="+91-9000012345",
            victim_name="Meera Iyer",
            suspect_name="Unknown",
            summary="Restricted Bengaluru case",
            sensitivity="restricted",
        ),
        CaseCreate(
            fir_number="MYS-001",
            year=2026,
            district="Mysuru",
            status="open",
            complainant_name="Arun Shetty",
            complainant_phone="+91-9888811111",
            victim_name="Arun Shetty",
            suspect_name="Mahesh N",
            summary="Mysuru case",
            sensitivity="standard",
        ),
    ]:
        db.create_case(case)

    cases = {case["fir_number"]: case for case in db.list_cases()}
    db.create_financial_transaction(
        occurred_at="2026-06-01T10:00:00+00:00",
        source_account="IN-BLR-0000123456",
        target_account="IN-BLR-0000654321",
        amount=1_250_000.0,
        currency="INR",
        district="Bengaluru",
        case_id=cases["BLR-001"]["id"],
        description="Large transfer linked to fraud complaint review.",
    )
    db.create_financial_transaction(
        occurred_at="2026-06-02T11:00:00+00:00",
        source_account="IN-BLR-0000222200",
        target_account="IN-MYS-0000333300",
        amount=950_000.0,
        currency="INR",
        district="Bengaluru",
        case_id=cases["BLR-001"]["id"],
        description="Near-threshold transfer for structuring triage.",
    )
    db.create_financial_transaction(
        occurred_at="2026-06-02T13:00:00+00:00",
        source_account="IN-BLR-0000222200",
        target_account="IN-MYS-0000444400",
        amount=940_000.0,
        currency="INR",
        district="Bengaluru",
        case_id=cases["BLR-001"]["id"],
        description="Second near-threshold transfer for structuring triage.",
    )

    app = create_app(settings=settings, database=db)
    with TestClient(app) as test_client:
        test_client.app.state.raw_db = db
        yield test_client


def login(client: TestClient, username: str) -> str:
    response = client.post(
        "/auth/login",
        json={"username": username, "password": "StrongPassword!123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def minimal_docx_bytes(lines: list[str]) -> bytes:
    body = "".join(
        f"<w:p><w:r><w:t>{line}</w:t></w:r></w:p>"
        for line in lines
    )
    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{body}</w:body>"
        "</w:document>"
    )
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("word/document.xml", document_xml)
    return buffer.getvalue()


def minimal_pdf_bytes(page_count: int = 2) -> bytes:
    from pypdf import PdfWriter

    writer = PdfWriter()
    for _index in range(page_count):
        writer.add_blank_page(width=240, height=320)
    buffer = io.BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


def test_login_rejects_bad_password(client: TestClient) -> None:
    response = client.post(
        "/auth/login",
        json={"username": "investigator", "password": "wrong"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_fingerprint_registration_options_are_authenticated(client: TestClient) -> None:
    denied = client.post("/auth/fingerprint/register/options", json={})
    assert denied.status_code in {401, 403}

    token = login(client, "investigator")
    response = client.post("/auth/fingerprint/register/options", json={}, headers=auth(token))
    assert response.status_code == 200
    public_key = response.json()["publicKey"]
    assert public_key["rp"]["name"] == "KSP Secure Intelligence"
    assert public_key["user"]["name"] == "investigator"
    assert public_key["authenticatorSelection"]["userVerification"] == "required"
    assert len(public_key["challenge"]) >= 32


def test_fingerprint_login_options_require_enrolled_user(client: TestClient) -> None:
    response = client.post("/auth/fingerprint/login/options", json={"username": "viewer"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Fingerprint login is not enrolled"


def test_fingerprint_login_options_return_enrolled_credentials(client: TestClient) -> None:
    db: Database = client.app.state.raw_db
    user = db.get_user_by_username("investigator")
    assert user is not None
    credential_id = "dGVzdC1maW5nZXJwcmludA"
    db.create_biometric_credential(
        user_id=user["id"],
        credential_id=credential_id,
        public_key_cose=b"\xa1\x01\x02",
        sign_count=0,
        transports=["internal", "usb"],
        label="Test fingerprint",
    )

    response = client.post("/auth/fingerprint/login/options", json={"username": "investigator"})
    assert response.status_code == 200
    public_key = response.json()["publicKey"]
    assert public_key["userVerification"] == "required"
    assert public_key["allowCredentials"] == [
        {"type": "public-key", "id": credential_id, "transports": ["internal", "usb"]}
    ]


def test_viewer_gets_masked_standard_cases_only(client: TestClient) -> None:
    token = login(client, "viewer")
    response = client.get("/cases", headers=auth(token))
    assert response.status_code == 200
    cases = response.json()

    assert [case["fir_number"] for case in cases] == ["BLR-001"]
    assert cases[0]["complainant_phone"] == "***MASKED***"
    assert cases[0]["complainant_name"] == "A. ***"
    assert cases[0]["suspect_name"] == "R. ***"


def test_analyst_cannot_read_restricted_case(client: TestClient) -> None:
    supervisor_token = login(client, "supervisor")
    all_cases = client.get("/cases", headers=auth(supervisor_token)).json()
    restricted_case = next(case for case in all_cases if case["fir_number"] == "BLR-002")

    analyst_token = login(client, "analyst")
    response = client.get(f"/cases/{restricted_case['id']}", headers=auth(analyst_token))
    assert response.status_code == 403


def test_investigator_can_update_district_case_but_not_other_district(client: TestClient) -> None:
    supervisor_token = login(client, "supervisor")
    all_cases = client.get("/cases", headers=auth(supervisor_token)).json()
    bengaluru_case = next(case for case in all_cases if case["fir_number"] == "BLR-001")
    mysuru_case = next(case for case in all_cases if case["fir_number"] == "MYS-001")

    investigator_token = login(client, "investigator")
    ok = client.patch(
        f"/cases/{bengaluru_case['id']}/status",
        json={"status": "under_review"},
        headers=auth(investigator_token),
    )
    denied = client.patch(
        f"/cases/{mysuru_case['id']}/status",
        json={"status": "under_review"},
        headers=auth(investigator_token),
    )

    assert ok.status_code == 200
    assert ok.json()["status"] == "under_review"
    assert denied.status_code == 403


def test_viewer_cannot_update_status(client: TestClient) -> None:
    supervisor_token = login(client, "supervisor")
    case_id = client.get("/cases", headers=auth(supervisor_token)).json()[0]["id"]

    viewer_token = login(client, "viewer")
    response = client.patch(
        f"/cases/{case_id}/status",
        json={"status": "closed"},
        headers=auth(viewer_token),
    )

    assert response.status_code == 403


def test_policymaker_gets_aggregate_intelligence_not_case_records(client: TestClient) -> None:
    token = login(client, "policymaker")
    cases = client.get("/cases", headers=auth(token))
    assert cases.status_code == 403

    trends = client.get("/analytics/trends", headers=auth(token))
    assert trends.status_code == 200
    assert trends.json()["total_cases"] == 0


def test_logout_revokes_token(client: TestClient) -> None:
    token = login(client, "investigator")
    logout = client.post("/auth/logout", headers=auth(token))
    assert logout.status_code == 200

    response = client.get("/auth/me", headers=auth(token))
    assert response.status_code == 401
    assert response.json()["detail"] == "Token revoked"


def test_audit_integrity_detects_tampering(client: TestClient) -> None:
    supervisor_token = login(client, "supervisor")
    response = client.get("/audit/integrity", headers=auth(supervisor_token))
    assert response.status_code == 200
    assert response.json()["valid"] is True

    db: Database = client.app.state.raw_db
    with sqlite3.connect(db.path) as conn:
        conn.execute(
            "UPDATE audit_logs SET detail_json = ? WHERE id = (SELECT MIN(id) FROM audit_logs)",
            ('{"tampered": true}',),
        )
        conn.commit()

    tampered = client.get("/audit/integrity", headers=auth(supervisor_token))
    assert tampered.status_code == 200
    assert tampered.json()["valid"] is False


def test_security_headers_present(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "SAMEORIGIN"
    assert response.headers["cache-control"] == "no-store"


def test_frontend_is_served_at_root(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "KSP Secure Intelligence" in response.text
    assert 'data-panel="framework"' in response.text
    assert 'data-panel="sna"' in response.text
    assert "/dashboards/criminal-network" in response.text
    css = client.get("/static/styles.css")
    assert css.status_code == 200


def test_criminal_network_dashboard_is_served_from_website(client: TestClient) -> None:
    response = client.get("/dashboards/criminal-network")
    assert response.status_code == 200
    assert "Criminal Network Analysis" in response.text

    png = client.get("/dashboards/criminal-network/files/criminal_network_dashboard.png")
    assert png.status_code == 200
    assert png.headers["content-type"].startswith("image/png")

    traversal = client.get("/dashboards/criminal-network/files/../criminal_network_dashboard.html")
    assert traversal.status_code == 404


def test_frontend_strips_sensitive_query_params(client: TestClient) -> None:
    response = client.get(
        "/?username=supervisor&password=ChangeMe%2112345",
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"] == "/"


def test_frontend_exposes_clean_crime_data_chat_ui(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "chat-scope-bar" in response.text
    assert "Answers from crime records" in response.text
    assert "Understands normal questions" in response.text
    assert "Ask like normal" in response.text


def test_modules_catalog_covers_requested_platform(client: TestClient) -> None:
    response = client.get("/modules")
    assert response.status_code == 200
    module_ids = {module["id"] for module in response.json()}
    assert {
        "chat_interface",
        "network_analysis",
        "trend_analytics",
        "sociological_insights",
        "offender_profiling",
        "decision_support",
        "financial_analysis",
        "forecasting",
        "explainable_ai",
        "rbac",
    }.issubset(module_ids)


def test_framework_catalog_exposes_solution_pillars_and_nlp_tasks(client: TestClient) -> None:
    response = client.get("/framework")
    assert response.status_code == 200
    body = response.json()
    assert "Crime Analytics Platform" in body["title"]
    assert len(body["solution_framework"]) == 10
    task_labels = {task["label"] for task in body["core_tasks"]}
    assert "Crime pattern discovery" in task_labels
    assert "Criminal network analysis" in task_labels
    assert "Proactive crime prevention intelligence" in task_labels


def test_hash_prefix_case_search_is_rbac_filtered(client: TestClient) -> None:
    token = login(client, "viewer")
    response = client.get("/cases/search?q=Ra", headers=auth(token))
    assert response.status_code == 200
    body = response.json()
    assert body["normalized_terms"] == ["ra"]
    assert body["result_count"] == 1
    assert body["results"][0]["case"]["fir_number"] == "BLR-001"


def test_intelligence_name_prefix_lookup_matches_full_name(client: TestClient) -> None:
    token = login(client, "supervisor")
    response = client.post(
        "/intelligence/query",
        json={"query": "names RAVI", "include_sources": True},
        headers=auth(token),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "direct_retrieval"
    assert body["visible_case_count"] == 1
    assert "Ravi Kumar" in body["answer"]
    assert body["sources"][0]["fir_number"] == "BLR-001"
    assert body["query_analysis"]["data_scope"] == "crime_data_only"
    assert "ravi" in body["query_analysis"]["interpreted_terms"]
    assert any("No external knowledge" in item for item in body["safeguards"])

    full_name = client.post(
        "/intelligence/query",
        json={"query": "Ravi Kumar", "include_sources": False},
        headers=auth(token),
    )
    assert full_name.status_code == 200
    assert "Ravi Kumar" in full_name.json()["answer"]


def test_intelligence_response_uses_crime_assistant_contract(client: TestClient) -> None:
    token = login(client, "supervisor")
    response = client.post(
        "/intelligence/query",
        json={"query": "WHERE NAME IS Ravi Kumar LIMIT 10", "include_sources": True},
        headers=auth(token),
    )
    assert response.status_code == 200
    body = response.json()
    answer = body["answer"]
    assert "Intent:" not in answer
    assert "Selected Module:" not in answer
    assert "Orchestration Flow:" not in answer
    assert "Confidence:" not in answer
    assert "Direct Answer:" not in answer
    assert "Reasoning:" not in answer
    assert "Ravi Kumar" in answer
    assert "BLR-001" in answer
    assert "Evidence references:" in answer
    assert "Suggested actions:" in answer
    assert body["selected_module"] == "MODULE 1: Conversational Crime Intelligence"
    assert body["selected_api"] == "POST /intelligence/query"
    assert "High" in body["confidence"]
    assert body["confidence"].startswith("92%")
    assert body["reasoning"]
    assert body["suggested_followups"]
    assert body["extracted_entities"]["fir_number"] == "BLR-001"
    assert body["conversation_memory"]["current_suspect"] == "Ravi Kumar"
    assert body["orchestration_trace"] == [
        "User",
        "Chat Interface",
        "LLM Intent Detection (strict sql case search)",
        "Orchestrator",
        "MODULE 1: Conversational Crime Intelligence (POST /intelligence/query)",
        "Response Generator",
        "Chat UI",
    ]
    assert body["query_analysis"]["interpreted_filters"]["orchestration_trace"] == body["orchestration_trace"]
    assert body["query_analysis"]["interpreted_filters"]["generated_intent_variations"] >= 1000
    assert body["presentation"]["audience"] == "investigator"
    assert body["presentation"]["show_debug_metadata"] is False
    assert body["presentation"]["show_intent"] is False
    assert body["presentation"]["show_module"] is False
    assert body["presentation"]["show_api"] is False
    assert body["presentation"]["show_confidence"] is False
    assert body["presentation"]["show_query_analysis"] is False
    assert body["presentation"]["render_evidence"] is True
    assert body["presentation"]["render_actions"] is True


def test_master_intent_taxonomy_generates_required_variations() -> None:
    status = taxonomy_status()
    assert status["category_count"] == 20
    assert status["total_variations"] >= 1000
    assert min(status["categories"].values()) >= 50
    assert classify_master_intent("hlo")["intent"] == "conversation_smalltalk"
    assert classify_master_intent("what is your moto?")["intent"] == "system_identity"
    assert classify_master_intent("who filed complaint against Ravi Kumar?")["category"] == "complainant_lookup"
    assert classify_master_intent("show money trail for A1")["category"] == "money_trails"
    assert classify_master_intent("ನಮಸ್ಕಾರ")["intent"] == "conversation_smalltalk"


def test_greeting_intent_returns_clean_chatbot_reply_without_record_lookup(client: TestClient) -> None:
    token = login(client, "supervisor")
    response = client.post(
        "/intelligence/query",
        json={"query": "hlo", "include_sources": True},
        headers=auth(token),
    )
    assert response.status_code == 200
    body = response.json()
    answer = body["answer"]
    assert body["intent"] == "conversation_smalltalk"
    assert "Hello" in answer
    assert "Intent:" not in answer
    assert "Evidence references:" not in answer
    assert "Suggested actions:" not in answer
    assert body["visible_case_count"] == 0
    assert body["sources"] == []
    assert body["presentation"]["render_evidence"] is False
    assert body["presentation"]["render_actions"] is False
    assert body["query_analysis"]["interpreted_filters"]["master_intent_category"] == "greeting"


def test_intelligence_complainant_lookup_answers_direct_question(client: TestClient) -> None:
    token = login(client, "supervisor")
    response = client.post(
        "/intelligence/query",
        json={"query": "Who filed complaint against Ravi Kumar?", "include_sources": True},
        headers=auth(token),
    )
    assert response.status_code == 200
    body = response.json()
    answer = body["answer"]
    assert body["intent"] == "complainant_lookup"
    assert "Complainant:" in answer
    assert "Asha Rao" in answer
    assert "FIR Number:" in answer
    assert "BLR-001" in answer
    assert "Top accessible match" not in answer
    assert "Found " not in answer
    assert body["sources"][0]["fir_number"] == "BLR-001"
    assert body["extracted_entities"]["complainant_name"] == "Asha Rao"
    assert body["conversation_memory"]["current_suspect"] == "Ravi Kumar"


def test_intelligence_kannada_complainant_lookup_answers_direct_question(client: TestClient) -> None:
    token = login(client, "supervisor")
    response = client.post(
        "/intelligence/query",
        json={
            "query": "ಕಂಪ್ಲೇಂಟ್ ಅನ್ನು ಯಾರು ಕೊಟ್ಟಿದ್ದಾರೆ ರವಿಕುಮಾರ್ ಹೆಸರಲ್ಲಿ?",
            "include_sources": True,
        },
        headers=auth(token),
    )
    assert response.status_code == 200
    body = response.json()
    answer = body["answer"]
    assert body["intent"] == "complainant_lookup"
    assert "ಉದ್ದೇಶ:" not in answer
    assert "ಆಯ್ಕೆ ಮಾಡಿದ ಘಟಕ:" not in answer
    assert "ವಿಶ್ವಾಸ:" not in answer
    assert "ಕಾರಣ:" not in answer
    assert "ದೂರುದಾರರ ಹೆಸರು:" in answer
    assert "Asha Rao" in answer
    assert "BLR-001" in answer
    assert "Top accessible match" not in answer
    assert body["query_analysis"]["interpreted_filters"]["language"] == "kn"
    assert body["presentation"]["show_debug_metadata"] is False
    assert body["presentation"]["show_intent"] is False
    assert body["presentation"]["show_module"] is False
    assert body["presentation"]["show_confidence"] is False
    assert body["extracted_entities"]["person_name"] == "Ravi Kumar"
    assert body["conversation_memory"]["current_suspect"] == "Ravi Kumar"


def test_kannada_dictionary_resource_is_loaded_for_query_learning() -> None:
    lexicon = load_kannada_lexicon()
    normalized = normalize_kannada_query("ಅಕ್ಷರ")
    assert lexicon.entry_count == 10_000
    assert len(lexicon.words) >= 4_000
    assert "ಅಕ್ಷರ" in lexicon.words
    assert normalized["dictionary"]["word_count"] == len(lexicon.words)
    assert normalized["dictionary"]["entry_count"] == lexicon.entry_count
    assert normalized["corrections"] == {}


def test_intelligence_complainant_lookup_lists_multiple_firs(client: TestClient) -> None:
    db: Database = client.app.state.raw_db
    db.create_case(
        CaseCreate(
            fir_number="BLR-003",
            year=2026,
            district="Bengaluru",
            status="under_review",
            complainant_name="Mahesh Kumar",
            complainant_phone="+91-8123456789",
            victim_name="Priya Rao",
            suspect_name="Ravi Kumar",
            summary="Second Bengaluru case involving Ravi Kumar for complainant lookup.",
            sensitivity="standard",
        )
    )
    token = login(client, "supervisor")
    response = client.post(
        "/intelligence/query",
        json={"query": "Who filed complaint against Ravi Kumar?", "include_sources": True},
        headers=auth(token),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "complainant_lookup"
    assert body["visible_case_count"] == 2
    assert "Ravi Kumar appears in 2 FIR records" in body["answer"]
    assert "Complainant: Asha Rao" in body["answer"]
    assert "Complainant: Mahesh Kumar" in body["answer"]
    assert "Please specify the FIR number" in body["answer"]
    assert {source["fir_number"] for source in body["sources"]} == {"BLR-001", "BLR-003"}


def test_copilot_system_and_admin_intents_do_not_run_crime_search(client: TestClient) -> None:
    token = login(client, "superadmin")
    system_response = client.post(
        "/intelligence/query",
        json={"query": "Who are you and what can you do?", "include_sources": True},
        headers=auth(token),
    )
    assert system_response.status_code == 200
    system_body = system_response.json()
    assert system_body["intent"] == "system_identity"
    assert "KSP AI Crime Intelligence Assistant" in system_body["answer"]
    assert "motto" in system_body["answer"].lower()
    assert system_body["selected_api"] == "No crime API called"
    assert system_body["sources"] == []
    assert system_body["query_analysis"]["data_scope"] == "system_metadata"
    assert "Top accessible match" not in system_body["answer"]

    motto_response = client.post(
        "/intelligence/query",
        json={"query": "what is your moto?", "include_sources": True},
        headers=auth(token),
    )
    assert motto_response.status_code == 200
    motto_body = motto_response.json()
    assert motto_body["intent"] == "system_identity"
    assert motto_body["selected_api"] == "No crime API called"
    assert "motto" in motto_body["answer"].lower()
    assert "interpreted NLP" not in motto_body["answer"]
    assert "Suggested actions:" not in motto_body["answer"]
    assert motto_body["presentation"]["render_evidence"] is False
    assert motto_body["presentation"]["render_actions"] is False

    admin_response = client.post(
        "/intelligence/query",
        json={"query": "show users and permissions", "include_sources": True},
        headers=auth(token),
    )
    assert admin_response.status_code == 200
    admin_body = admin_response.json()
    assert admin_body["intent"] == "admin_user_management"
    assert admin_body["selected_module"] == "MODULE 10: Security and Governance"
    assert "create user" in admin_body["answer"].lower()
    assert "passwords are never readable" in admin_body["answer"].lower()
    assert admin_body["query_analysis"]["data_scope"] == "governance_data_only"


def test_admin_intent_respects_rbac_inside_copilot(client: TestClient) -> None:
    token = login(client, "investigator")
    response = client.post(
        "/intelligence/query",
        json={"query": "show users", "include_sources": True},
        headers=auth(token),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "admin_user_management"
    assert "cannot manage user accounts" in body["answer"]
    assert body["query_analysis"]["interpreted_filters"]["permission"] == "user:read denied"


def test_copilot_extracts_structured_entities_from_query(client: TestClient) -> None:
    token = login(client, "supervisor")
    response = client.post(
        "/intelligence/query",
        json={
            "query": "Find FIR BLR-001 phone 9876543210 account ICICI-AC-556677 vehicle KA01AB1234 in Bengaluru on 2026-06-01",
            "include_sources": True,
        },
        headers=auth(token),
    )
    assert response.status_code == 200
    entities = response.json()["extracted_entities"]
    assert entities["fir_number"] == "BLR-001"
    assert entities["phone"] == ["9876543210"]
    assert entities["account"] == ["ICICI-AC-556677"]
    assert entities["vehicle"] == ["KA01AB1234"]
    assert entities["district"] == ["Bengaluru"]
    assert entities["date"] == ["2026-06-01"]


def test_conversation_memory_resolves_followup_subject(client: TestClient) -> None:
    token = login(client, "supervisor")
    created = client.post(
        "/conversations",
        json={"title": "Ravi follow-up"},
        headers=auth(token),
    )
    assert created.status_code == 200
    conversation_id = created.json()["id"]

    first = client.post(
        f"/conversations/{conversation_id}/messages",
        json={"query": "Who filed complaint against Ravi Kumar?"},
        headers=auth(token),
    )
    assert first.status_code == 200
    first_body = first.json()
    assert first_body["intelligence"]["conversation_memory"]["current_suspect"] == "Ravi Kumar"

    followup = client.post(
        f"/conversations/{conversation_id}/messages",
        json={"query": "What is the case status?"},
        headers=auth(token),
    )
    assert followup.status_code == 200
    body = followup.json()
    intelligence = body["intelligence"]
    assert intelligence["intent"] == "case_status"
    assert "Current status" in intelligence["answer"]
    assert "open" in intelligence["answer"]
    assert "BLR-001" in intelligence["answer"]
    assert intelligence["conversation_memory"]["current_suspect"] == "Ravi Kumar"
    assert body["assistant_message"]["metadata"]["conversation_memory"]["current_suspect"] == "Ravi Kumar"


def test_conversation_memory_routes_network_and_money_followups_to_suspect(client: TestClient) -> None:
    token = login(client, "supervisor")
    created = client.post(
        "/conversations",
        json={"title": "Ravi network follow-up"},
        headers=auth(token),
    )
    conversation_id = created.json()["id"]

    first = client.post(
        f"/conversations/{conversation_id}/messages",
        json={"query": "Show Ravi Kumar profile"},
        headers=auth(token),
    )
    assert first.status_code == 200
    assert first.json()["intelligence"]["conversation_memory"]["current_suspect"] == "Ravi Kumar"

    network = client.post(
        f"/conversations/{conversation_id}/messages",
        json={"query": "Show network"},
        headers=auth(token),
    )
    assert network.status_code == 200
    network_body = network.json()["intelligence"]
    assert network_body["intent"] == "criminal_network_analysis"
    assert "Ravi Kumar" in network_body["answer"]
    assert "BLR-001" in network_body["answer"]
    assert network_body["selected_module"] == "MODULE 2: Criminal Network Analysis"
    assert network_body["conversation_memory"]["current_suspect"] == "Ravi Kumar"

    money = client.post(
        f"/conversations/{conversation_id}/messages",
        json={"query": "Show money trail"},
        headers=auth(token),
    )
    assert money.status_code == 200
    money_body = money.json()["intelligence"]
    assert money_body["intent"] == "financial_analysis"
    assert "Money trail for Ravi Kumar" in money_body["answer"]
    assert "IN-BLR-0000123456" in money_body["answer"]
    assert money_body["selected_module"] == "MODULE 7: Financial Crime Analytics"


def test_intelligence_broad_case_listing_returns_sources(client: TestClient) -> None:
    token = login(client, "supervisor")
    response = client.post(
        "/intelligence/query",
        json={"query": "LIST ALL THE KARNATAKA CASE COPY", "include_sources": True},
        headers=auth(token),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "direct_retrieval"
    assert "You can access" in body["answer"]
    assert "No accessible case/person record matched" not in body["answer"]
    assert body["sources"]

    only_response = client.post(
        "/intelligence/query",
        json={"query": "SHOW THE KARNATAKA CASES ONLY", "include_sources": True},
        headers=auth(token),
    )
    assert only_response.status_code == 200
    only_body = only_response.json()
    assert only_body["intent"] == "direct_retrieval"
    assert "You can access" in only_body["answer"]
    assert "No accessible case/person record matched" not in only_body["answer"]
    assert only_body["query_analysis"]["interpreted_terms"] == []
    assert only_body["sources"]


def test_intelligence_noisy_named_person_lookup_ignores_instruction_words(client: TestClient) -> None:
    token = login(client, "supervisor")
    response = client.post(
        "/intelligence/query",
        json={"query": "SEARCH WHERE RAVI NAMED ACUSE FILE NUMBER", "include_sources": True},
        headers=auth(token),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "accused_lookup"
    assert body["visible_case_count"] == 1
    assert "Ravi Kumar" in body["answer"]
    assert "No accessible case/person record matched" not in body["answer"]
    assert body["query_analysis"]["interpreted_terms"] == ["ravi"]
    assert body["sources"][0]["fir_number"] == "BLR-001"

    natural_response = client.post(
        "/intelligence/query",
        json={"query": "WHAT CRIME IS SUSPECT RAVI KUMAR INVOLVED IN GIVE CASE FILE NUMBER", "include_sources": True},
        headers=auth(token),
    )
    assert natural_response.status_code == 200
    natural_body = natural_response.json()
    assert natural_body["intent"] == "accused_lookup"
    assert natural_body["visible_case_count"] == 1
    assert "Ravi Kumar" in natural_body["answer"]
    assert natural_body["query_analysis"]["interpreted_terms"] == ["ravi", "kumar"]
    assert natural_body["sources"][0]["fir_number"] == "BLR-001"


def test_intelligence_strict_sql_search_finds_identifier_and_exact_names(client: TestClient) -> None:
    token = login(client, "supervisor")
    identifier_response = client.post(
        "/intelligence/query",
        json={"query": "FIR BLR-001 file", "include_sources": True},
        headers=auth(token),
    )
    assert identifier_response.status_code == 200
    identifier_body = identifier_response.json()
    assert identifier_body["intent"] == "strict_sql_case_search"
    assert identifier_body["visible_case_count"] == 1
    assert identifier_body["sources"][0]["fir_number"] == "BLR-001"
    assert identifier_body["query_analysis"]["interpreted_filters"]["sql_strategy"] == "identifier_exact"

    name_response = client.post(
        "/intelligence/query",
        json={"query": "WHERE NAME IS Ravi Kumar OR Mahesh LIMIT 10", "include_sources": True},
        headers=auth(token),
    )
    assert name_response.status_code == 200
    name_body = name_response.json()
    assert name_body["intent"] == "strict_sql_case_search"
    assert name_body["visible_case_count"] == 2
    assert {source["fir_number"] for source in name_body["sources"]} == {"BLR-001", "MYS-001"}
    assert name_body["query_analysis"]["interpreted_filters"]["limit"] == 10


def test_intelligence_strict_sql_search_honors_top_limit_and_spelling_correction(client: TestClient) -> None:
    db: Database = client.app.state.raw_db
    for index in range(12):
        db.create_case(
            CaseCreate(
                fir_number=f"THF-{index:03}",
                year=2026,
                district="Bengaluru",
                status="open",
                case_type="THEFT",
                modus_operandi="Night market theft",
                incident_at=datetime(2026, 6, min(index + 1, 28), tzinfo=timezone.utc),
                complainant_name=f"Theft Complainant {index}",
                complainant_phone="+91-8000000000",
                victim_name=f"Theft Victim {index}",
                suspect_name=f"Theft Suspect {index}",
                summary="Theft case recorded for strict SQL search testing.",
                sensitivity="standard",
            )
        )

    token = login(client, "supervisor")
    top_response = client.post(
        "/intelligence/query",
        json={"query": "top 10 theft cases desc limit 10", "include_sources": True},
        headers=auth(token),
    )
    assert top_response.status_code == 200
    top_body = top_response.json()
    assert top_body["intent"] == "strict_sql_case_search"
    assert top_body["visible_case_count"] == 10
    assert len(top_body["sources"]) == 10
    assert all(source["fir_number"].startswith("THF-") for source in top_body["sources"])
    assert top_body["query_analysis"]["interpreted_filters"]["limit"] == 10
    assert top_body["query_analysis"]["interpreted_filters"]["order"] == "descending"

    typo_response = client.post(
        "/intelligence/query",
        json={"query": "top 10 thetf cases", "include_sources": True},
        headers=auth(token),
    )
    assert typo_response.status_code == 200
    typo_body = typo_response.json()
    assert typo_body["intent"] == "strict_sql_case_search"
    assert typo_body["visible_case_count"] == 10
    assert typo_body["query_analysis"]["interpreted_filters"]["spelling_corrections"]["thetf"] == "theft"
    assert "corrected spelling" in typo_body["answer"].lower()


def test_intelligence_strict_sql_search_corrects_person_name_typo(client: TestClient) -> None:
    token = login(client, "supervisor")
    response = client.post(
        "/intelligence/query",
        json={"query": "WHERE SUSPECT NAME IS Ravvi Kumar LIMIT 10", "include_sources": True},
        headers=auth(token),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "strict_sql_case_search"
    assert body["visible_case_count"] == 1
    assert body["sources"][0]["fir_number"] == "BLR-001"
    assert body["query_analysis"]["interpreted_filters"]["spelling_corrections"]["ravvi"] == "ravi"


def test_suspect_profile_supports_partial_name(client: TestClient) -> None:
    token = login(client, "supervisor")
    response = client.get("/profiles/suspects/Ravi", headers=auth(token))
    assert response.status_code == 200
    body = response.json()
    assert body["named_in_case_count"] == 1
    assert body["cases"][0]["fir_number"] == "BLR-001"


def test_intelligence_high_risk_question_routes_to_suspect_profile(client: TestClient) -> None:
    token = login(client, "supervisor")
    response = client.post(
        "/intelligence/query",
        json={"query": "is Ravi high risk suspect", "include_sources": True},
        headers=auth(token),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "offender_profile"
    assert body["selected_module"] == "MODULE 5: Suspect Profiling"
    assert "Risk profile for Ravi Kumar" in body["answer"]
    assert "No accessible case record contains" not in body["answer"]
    assert body["sources"][0]["fir_number"] == "BLR-001"
    assert body["extracted_entities"]["suspect_name"] == "Ravi Kumar"
    assert "high risk" not in body["extracted_entities"]["person_name"].lower()


def test_intelligence_suggested_actions_are_contextual_not_placeholders(client: TestClient) -> None:
    token = login(client, "supervisor")
    response = client.post(
        "/intelligence/query",
        json={"query": "Ravi", "include_sources": True},
        headers=auth(token),
    )
    assert response.status_code == 200
    body = response.json()
    actions = body["presentation"]["suggested_actions"]
    assert actions
    assert all("specific" not in action.lower() for action in actions)
    assert all("another suspect" not in action.lower() for action in actions)
    assert any("BLR-001" in action or "Ravi Kumar" in action for action in actions)


def test_supervisor_can_import_official_case_records(client: TestClient) -> None:
    token = login(client, "supervisor")
    response = client.post(
        "/cases/import",
        json={
            "source_system": "authorized-test-source",
            "records": [
                {
                    "fir_number": "AUTH-001",
                    "year": 2026,
                    "district": "Mandya",
                    "status": "open",
                    "complainant_name": "Official Complainant",
                    "complainant_phone": "0000000000",
                    "victim_name": "Official Victim",
                    "suspect_name": "Official Subject",
                    "summary": "Official imported record for test verification.",
                    "sensitivity": "standard",
                    "latitude": 12.52,
                    "longitude": 76.9,
                    "source_record_id": "SRC-001",
                }
            ],
        },
        headers=auth(token),
    )
    assert response.status_code == 200
    assert response.json()["imported"] == 1

    search = client.get("/cases/search?q=SRC-001", headers=auth(token))
    assert search.status_code == 200
    assert search.json()["results"][0]["case"]["fir_number"] == "AUTH-001"


def test_supervisor_can_upload_csv_case_sheet(client: TestClient) -> None:
    token = login(client, "supervisor")
    csv_body = (
        "fir_number,year,district,status,complainant_name,complainant_phone,victim_name,suspect_name,summary,sensitivity,source_record_id\n"
        "CSV-001,2026,Hassan,open,Sheet Complainant,1111111111,Sheet Victim,Sheet Suspect,Uploaded CSV case details,standard,CSV-SRC-001\n"
    )
    response = client.post(
        "/files/upload",
        data={"upload_type": "case_sheet", "source_system": "csv-upload-test", "auto_import": "true"},
        files={"file": ("cases.csv", csv_body, "text/csv")},
        headers=auth(token),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["imported"] == 1
    assert body["skipped"] == 0
    assert body["sha256"]

    search = client.get("/cases/search?q=CSV-SRC-001", headers=auth(token))
    assert search.status_code == 200
    assert search.json()["results"][0]["case"]["fir_number"] == "CSV-001"


def test_investigator_can_upload_fir_copy_for_accessible_case(client: TestClient) -> None:
    supervisor_token = login(client, "supervisor")
    bengaluru_case = next(
        case for case in client.get("/cases", headers=auth(supervisor_token)).json() if case["fir_number"] == "BLR-001"
    )
    token = login(client, "investigator")
    response = client.post(
        "/files/upload",
        data={"upload_type": "fir_copy", "case_id": bengaluru_case["id"], "source_system": "fir-copy-test"},
        files={
            "file": (
                "fir-copy.pdf",
                minimal_pdf_bytes(2),
                "application/pdf",
            )
        },
        headers=auth(token),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["upload_type"] == "fir_copy"
    assert body["case_id"] == bengaluru_case["id"]
    assert body["imported"] == 0
    assert body["sha256"]

    listed = client.get("/files/uploads?q=fir-copy&limit=10", headers=auth(token))
    assert listed.status_code == 200
    uploads = listed.json()
    assert uploads[0]["id"] == body["upload_id"]
    assert uploads[0]["linked_fir_number"] == "BLR-001"
    assert uploads[0]["preview_supported"] is True

    detail = client.get(f"/files/uploads/{body['upload_id']}", headers=auth(token))
    assert detail.status_code == 200
    assert detail.json()["original_filename"] == "fir-copy.pdf"

    preview = client.get(f"/files/uploads/{body['upload_id']}/content", headers=auth(token))
    assert preview.status_code == 200
    assert preview.headers["content-type"].startswith("application/pdf")
    assert preview.headers["content-disposition"].startswith("inline;")
    assert preview.content.startswith(b"%PDF")

    pages = client.get(f"/files/uploads/{body['upload_id']}/pages", headers=auth(token))
    assert pages.status_code == 200
    assert pages.json()["page_count"] == 2
    assert pages.json()["visible_pages"] == [1, 2]

    rendered = client.get(f"/files/uploads/{body['upload_id']}/render.png", headers=auth(token))
    assert rendered.status_code == 200
    assert rendered.headers["content-type"] == "image/png"
    assert rendered.content.startswith(b"\x89PNG")


def test_pdf_preview_prefers_original_page_even_after_text_extraction(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(app_module, "render_pdf_page_png", lambda content, page: b"original-pdf-page")
    monkeypatch.setattr(app_module, "render_text_document_png", lambda upload: b"generated-summary-page")
    rendered = app_module.render_upload_png(
        {
            "extension": ".pdf",
            "original_filename": "official-ksp-fir.pdf",
            "extracted_preview": "Extracted FIR text",
            "extracted_summary": "Generated summary",
            "extracted_summary_kn": "Generated Kannada summary",
        },
        b"%PDF-1.4\n",
        1,
    )
    assert rendered == b"original-pdf-page"


def test_uploaded_docx_is_extracted_summarized_and_searchable(client: TestClient) -> None:
    supervisor_token = login(client, "supervisor")
    bengaluru_case = next(
        case for case in client.get("/cases", headers=auth(supervisor_token)).json() if case["fir_number"] == "BLR-001"
    )
    token = login(client, "investigator")
    docx_body = minimal_docx_bytes(
        [
            "FIR Number: BLR-001",
            "Complainant: Asha Rao",
            "Accused: Ravi Kumar",
            "Victim: Kiran Rao",
            "Police Station: Bengaluru South Police Station",
            "Status: Open",
            "Investigation note: Ravi Kumar is named in the uploaded FIR copy for verification.",
        ]
    )
    response = client.post(
        "/files/upload",
        data={"upload_type": "fir_copy", "case_id": bengaluru_case["id"], "source_system": "docx-extraction-test"},
        files={
            "file": (
                "ravi-kumar-fir.docx",
                docx_body,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
        headers=auth(token),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["extraction_status"] == "extracted"
    assert body["extracted_char_count"] > 50
    assert "Ravi Kumar" in body["extracted_preview"]
    assert "Complainant: Asha Rao" in body["extracted_summary"]
    assert "ದೂರುದಾರರು: Asha Rao" in body["extracted_summary_kn"]
    assert "ಆರೋಪಿತ" in body["extracted_summary_kn"]

    listed = client.get("/files/uploads?q=Ravi%20Kumar&limit=10", headers=auth(token))
    assert listed.status_code == 200
    matches = listed.json()
    assert any(item["id"] == body["upload_id"] for item in matches)
    matched = next(item for item in matches if item["id"] == body["upload_id"])
    assert matched["extracted_summary"]
    assert matched["extracted_summary_kn"]
    assert matched["preview_supported"] is True

    rendered = client.get(f"/files/uploads/{body['upload_id']}/render.png", headers=auth(token))
    assert rendered.status_code == 200
    assert rendered.headers["content-type"] == "image/png"
    assert rendered.content.startswith(b"\x89PNG")


def test_uploaded_fir_copy_gets_strict_xml_reconstruction(client: TestClient) -> None:
    supervisor_token = login(client, "supervisor")
    bengaluru_case = next(
        case for case in client.get("/cases", headers=auth(supervisor_token)).json() if case["fir_number"] == "BLR-001"
    )
    token = login(client, "investigator")
    fir_docx = minimal_docx_bytes(
        [
            "FIRST INFORMATION REPORT",
            "KARNATAKA STATE POLICEBefore the Honourable Court of Test Court (Under Section 173 Bharatiya Nagarik Suraksha Sanhita)",
            "1.District : Bengaluru DistCrime No : 0099/2026FIR Date : 10/06/2026Circle/Sub Division : East Sub-DPS : Indiranagar PS Act & Section : THE BHARATIYA NYAYA SANHITA (BNS), 2023 (U/s-318)",
            "2.(b) Information received at the PS : 10/06/2026 21:00:00Written/Oral : WrittenFrom Time : To Time :From Date : To Date :",
            "3. 10/06/202610/06/202620:00:0020:20:00(a) Occurence of Offence Day : Wednesday(c) Reasons for Delay in reporting by the Complainant / Informantno(d) General Diary reference Entry No. & Time : 7 , 21:05:00",
            "4.(a) Place of occurence with full addressMG Road, Bengaluru, Karnataka(b) Distance from PS : 2km towards east(c) Village : Bengaluru Beat Name : CENTRAL 01District :",
            "5.Complainant/Informant:Ravi Kumar / Suresh Kumar(g) Email(f) Faxravi@example.com(e) Caste(d) Religion(b) Age(c) Occupation40Officer:::(h) Phone No.:9999999999(i) Nationality:India: Date of Issue : (j) Passport No.(k) Address : Bengaluru, Karnataka(l) Sex:Male(m) Whether complainant has seen the occurence or merely heard of it :seen",
            "AgeSexPerson TypeName / Father Name / Caste / AddressOccupationTypeSl.No.1 AccusedAdultMaleAkash Shetty(A1) / Ramesh Shetty, Bengaluru6.Details of known/suspected/unknown accused with full particulars",
            "7. Details of Victims with full particulars",
            "8. Particulars of Property stolen/involved with value(Attach separate sheet if necessary)Sl.No.Property TypeEstimated Value (in Rs.)Item description1 Total Value of the property Stolen / Involved : 9. Inquest Report/U.D. Case No. if any :",
            "10. F.I.R Contents (Attach separate sheet if necessary) This is the strict FIR reconstruction test narrative.11. (b) Is the F.I.R read over and explained in his/her language to the complainant and a copy given to the complainant free of cost? : Yes(a) Action Taken :Investigation(c) If the Police Officer does not proceed to the spot for investigation or if he declines to investigate. U/S 157 Cr.PC provision (a)or (b) / 176 Bharatiya Nagarik Suraksha Sanhita (BNSS) the reasons there of should be mentioned : YES VISITED",
            "12. Signature/Thumb impression of the complainant13. Date and time of dispatch to the Court : 10/06/2026 21:30:00 Name: TEST OFFICER - HC 100 14. Name of PC/HC who carried the FIR to the Court : Test Carrier , PC 200 Read Over and Found to be correct Date and Time : 10/06/2026 21:25:00Signature of the SHO Copy to :Superintendent of Police/Commissioner of Police",
        ]
    )
    response = client.post(
        "/files/upload",
        data={"upload_type": "fir_copy", "case_id": bengaluru_case["id"], "source_system": "fir-xml-test"},
        files={
            "file": (
                "strict-fir-copy.docx",
                fir_docx,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
        headers=auth(token),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["fir_reconstruction_status"] == "strict_valid"
    assert body["extracted_metadata"]["values"]["crime_no"] == "0099/2026"
    assert body["extracted_metadata"]["values"]["complainant_name"] == "Ravi Kumar"
    assert body["extracted_metadata"]["accused"][0]["name"] == "Akash Shetty(A1)"
    assert "<Field key=\"crime_no\" label=\"Crime No\"" in body["fir_reconstruction_xml"]
    assert "<Value>0099/2026</Value>" in body["fir_reconstruction_xml"]

    xml = client.get(f"/files/uploads/{body['upload_id']}/fir.xml", headers=auth(token))
    assert xml.status_code == 200
    assert xml.headers["content-type"].startswith("application/xml")
    assert b"KSPFirstInformationReport" in xml.content
    assert b"strict FIR reconstruction test narrative" in xml.content


def test_only_super_admin_can_manage_users(client: TestClient) -> None:
    supervisor_token = login(client, "supervisor")
    denied = client.get("/admin/users", headers=auth(supervisor_token))
    assert denied.status_code == 403

    admin_token = login(client, "superadmin")
    listed = client.get("/admin/users", headers=auth(admin_token))
    assert listed.status_code == 200
    assert {user["username"] for user in listed.json()}.issuperset({"superadmin", "supervisor"})

    created = client.post(
        "/admin/users",
        json={
            "username": "mandya.viewer",
            "password": "AnotherStrong!123",
            "full_name": "Mandya Viewer",
            "role": "viewer",
            "district": "Mandya",
        },
        headers=auth(admin_token),
    )
    assert created.status_code == 200
    user_id = created.json()["id"]
    assert created.json()["role"] == "viewer"

    updated = client.patch(
        f"/admin/users/{user_id}",
        json={"role": "analyst", "district": "Mysuru", "is_active": False},
        headers=auth(admin_token),
    )
    assert updated.status_code == 200
    assert updated.json()["role"] == "analyst"
    assert updated.json()["district"] == "Mysuru"
    assert updated.json()["is_active"] is False
    blocked_login = client.post(
        "/auth/login",
        json={"username": "mandya.viewer", "password": "AnotherStrong!123"},
    )
    assert blocked_login.status_code == 401

    reset = client.post(
        f"/admin/users/{user_id}/reset-password",
        json={"password": "Replacement!12345"},
        headers=auth(admin_token),
    )
    assert reset.status_code == 200
    assert reset.json()["status"] == "password_reset"

    activity = client.get(f"/admin/users/{user_id}/activity?limit=10", headers=auth(admin_token))
    assert activity.status_code == 200
    assert activity.json()["user"]["username"] == "mandya.viewer"
    assert {"USER_CREATE", "USER_UPDATE", "USER_PASSWORD_RESET"}.issubset(
        {event["action"] for event in activity.json()["events"]}
    )

    superadmin_id = next(user["id"] for user in listed.json() if user["username"] == "superadmin")
    self_delete = client.delete(f"/admin/users/{superadmin_id}", headers=auth(admin_token))
    assert self_delete.status_code == 400

    deleted = client.delete(f"/admin/users/{user_id}", headers=auth(admin_token))
    assert deleted.status_code == 200
    assert deleted.json()["status"] == "deleted"
    relisted = client.get("/admin/users", headers=auth(admin_token))
    assert "mandya.viewer" not in {user["username"] for user in relisted.json()}


def test_rate_limit_breach_alert_identifies_authenticated_user(tmp_path: Path) -> None:
    settings = Settings(
        environment="test",
        database_path=tmp_path / "limited.db",
        jwt_secret="test-secret-that-is-long-enough-for-hs256",
        rate_limit_per_minute=2,
        allowed_hosts="testserver",
    )
    db = Database(settings.database_path)
    db.init_schema()
    db.create_user(
        UserCreate(
            username="superadmin",
            password="StrongPassword!123",
            full_name="Super Admin",
            role="super_admin",
            district="state",
        )
    )
    db.create_user(
        UserCreate(
            username="investigator",
            password="StrongPassword!123",
            full_name="Investigator",
            role="investigator",
            district="Bengaluru",
        )
    )
    app = create_app(settings=settings, database=db)

    with TestClient(app) as limited_client:
        investigator_token = login(limited_client, "investigator")
        admin_token = login(limited_client, "superadmin")

        assert limited_client.get("/cases", headers=auth(investigator_token)).status_code == 200
        assert limited_client.get("/cases", headers=auth(investigator_token)).status_code == 200
        breached = limited_client.get("/cases", headers=auth(investigator_token))
        assert breached.status_code == 429
        assert breached.headers["x-ratelimit-remaining"] == "0"

        alerts = limited_client.get("/admin/rate-limit-alerts", headers=auth(admin_token))
        assert alerts.status_code == 200
        body = alerts.json()
        assert body[0]["actor_username"] == "investigator"
        assert body[0]["actor_role"] == "investigator"
        assert body[0]["path"] == "/cases"

        acknowledged = limited_client.post(
            f"/admin/rate-limit-alerts/{body[0]['id']}/acknowledge",
            headers=auth(admin_token),
        )
        assert acknowledged.status_code == 200
        assert acknowledged.json()["acknowledged_by"] == "superadmin"


def test_unauthenticated_rate_limit_blocks_same_ip_across_api(tmp_path: Path) -> None:
    settings = Settings(
        environment="test",
        database_path=tmp_path / "unauth-limited.db",
        jwt_secret="test-secret-that-is-long-enough-for-hs256",
        rate_limit_per_minute=1,
        allowed_hosts="testserver",
    )
    db = Database(settings.database_path)
    db.init_schema()
    app = create_app(settings=settings, database=db)

    with TestClient(app) as limited_client:
        assert limited_client.get("/health").status_code == 200
        breached = limited_client.get("/modules")
        assert breached.status_code == 429
        assert breached.json()["detail"] == "Rate limit exceeded"

        blocked = limited_client.get("/health")
        assert blocked.status_code == 429
        assert blocked.json()["detail"] == "Unauthenticated device or IP temporarily blocked"

    alerts = db.list_rate_limit_alerts(include_acknowledged=True)
    assert alerts[0]["actor_username"] is None
    assert alerts[0]["client_ip"] == "testclient"


def test_viewer_cannot_use_intelligence_query(client: TestClient) -> None:
    token = login(client, "viewer")
    response = client.post(
        "/intelligence/query",
        json={"query": "show cases in Bengaluru"},
        headers=auth(token),
    )
    assert response.status_code == 403


def test_analyst_intelligence_filters_restricted_and_other_district(client: TestClient) -> None:
    token = login(client, "analyst")
    response = client.post(
        "/intelligence/query",
        json={"query": "show BLR cases", "include_sources": True},
        headers=auth(token),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["visible_case_count"] == 1
    assert [source["fir_number"] for source in body["sources"]] == ["BLR-001"]


def test_conversation_roundtrip_and_pdf_export(client: TestClient) -> None:
    token = login(client, "investigator")
    created = client.post(
        "/conversations",
        json={"title": "Fraud review"},
        headers=auth(token),
    )
    assert created.status_code == 200
    conversation_id = created.json()["id"]

    exchange = client.post(
        f"/conversations/{conversation_id}/messages",
        json={"query": "summarize FIR BLR-001"},
        headers=auth(token),
    )
    assert exchange.status_code == 200
    assert exchange.json()["intelligence"]["intent"] == "decision_support"

    exported = client.get(
        f"/conversations/{conversation_id}/export.pdf",
        headers=auth(token),
    )
    assert exported.status_code == 200
    assert exported.headers["content-type"] == "application/pdf"
    assert exported.content.startswith(b"%PDF")


def test_financial_analysis_detects_triage_findings(client: TestClient) -> None:
    token = login(client, "investigator")
    response = client.get("/financial/analysis", headers=auth(token))
    assert response.status_code == 200
    finding_types = {finding["finding_type"] for finding in response.json()["findings"]}
    assert {"high_value_transfer", "possible_structuring"}.issubset(finding_types)


def test_network_graph_exposes_suspect_case_and_money_trail_metadata(client: TestClient) -> None:
    token = login(client, "superadmin")
    response = client.get("/analytics/network", headers=auth(token))
    assert response.status_code == 200
    body = response.json()

    ravi = next(node for node in body["nodes"] if node["type"] == "suspect" and node["label"] == "Ravi Kumar")
    ravi_cases = ravi["metadata"]["cases"]
    assert ravi_cases[0]["fir_number"] == "BLR-001"
    assert ravi_cases[0]["status"] == "open"

    case_id = ravi_cases[0]["case_id"]
    case_node = next(node for node in body["nodes"] if node["id"] == f"case:{case_id}")
    assert case_node["metadata"]["fir_number"] == "BLR-001"
    assert case_node["metadata"]["suspect_name"] == "Ravi Kumar"
    assert case_node["metadata"]["transfers"]

    transfer_links = [link for link in body["links"] if link["relationship"] == "TRANSFERRED_TO"]
    assert transfer_links
    transfer_amounts = [
        transaction["amount"]
        for link in transfer_links
        for transaction in link["metadata"]["transactions"]
    ]
    assert 1_250_000.0 in transfer_amounts


def test_network_graph_supports_bank_metadata_nodes_and_dead_ends(client: TestClient) -> None:
    token = login(client, "superadmin")
    cases = client.get("/cases", headers=auth(token)).json()
    case_id = next(case["id"] for case in cases if case["fir_number"] == "BLR-001")

    imported = client.post(
        "/financial/transactions/import",
        headers=auth(token),
        json={
            "source_system": "bank-ledger",
            "records": [
                {
                    "occurred_at": "2026-06-03T09:00:00+00:00",
                    "source_account": "IN-BLR-0000654321",
                    "target_account": "IN-END-0000777700",
                    "source_account_holder": "A2",
                    "target_account_holder": "A3",
                    "source_bank_name": "Karnataka Cooperative Bank",
                    "source_ifsc_code": "KCBL0001234",
                    "source_branch": "Bengaluru Central",
                    "source_bank_manager_phone": "+91-8000011111",
                    "target_bank_name": "Mysuru Rural Bank",
                    "target_ifsc_code": "MRBL0007777",
                    "target_branch": "Mysuru East",
                    "target_bank_manager_phone": "+91-8000022222",
                    "amount": 550000.0,
                    "currency": "INR",
                    "district": "Bengaluru",
                    "case_id": case_id,
                    "description": "Follow-on transfer with official bank metadata.",
                }
            ],
        },
    )
    assert imported.status_code == 200

    graph = client.get("/analytics/network", headers=auth(token)).json()
    node_types = {node["type"] for node in graph["nodes"]}
    assert {"bank", "ifsc", "branch", "bank_manager", "dead_end"}.issubset(node_types)
    assert any(node["label"] == "Karnataka Cooperative Bank" for node in graph["nodes"])
    assert any(node["label"] == "KCBL0001234" for node in graph["nodes"])
    assert any(node["label"] == "Bengaluru Central" for node in graph["nodes"])
    assert any(node["label"] == "+91-8000011111" for node in graph["nodes"])
    assert any(node["type"] == "suspect" and node["label"] == "A2" for node in graph["nodes"])
    assert any(node["type"] == "suspect" and node["label"] == "A3" for node in graph["nodes"])
    assert any(link["relationship"] == "ACCOUNT_HOLDER_OF" for link in graph["links"])
    assert any(link["relationship"] == "TRAIL_ENDS_AT" for link in graph["links"])

    focused = client.get(
        "/analytics/network?focus=IN-BLR-0000654321&focus_type=account",
        headers=auth(token),
    )
    assert focused.status_code == 200
    focused_graph = focused.json()
    assert focused_graph["focus"]["active"] is True
    assert focused_graph["focus"]["focus_type"] == "account"
    assert focused_graph["focus"]["case_count"] == 1
    assert focused_graph["focus"]["transaction_count"] == 2
    assert focused_graph["focus"]["linked_firs"] == ["BLR-001"]
    focused_labels = {node["label"] for node in focused_graph["nodes"]}
    assert {"A2", "A3", "IN-BLR-0000654321", "IN-END-0000777700"}.issubset(focused_labels)
    assert "IN-MYS-0000333300" not in focused_labels
    assert any(alert["title"] == "Criminal database link found" for alert in focused_graph["focus"]["alerts"])


def test_pattern_discovery_counts_each_case_once(client: TestClient) -> None:
    token = login(client, "supervisor")
    response = client.get("/analytics/patterns", headers=auth(token))
    assert response.status_code == 200
    clusters = response.json()["clusters"]
    bengaluru = next(cluster for cluster in clusters if cluster["key"] == "Bengaluru")
    assert bengaluru["count"] == 2
    assert bengaluru["fir_numbers"] == ["BLR-001", "BLR-002"]


def test_super_admin_imports_crime_csv_for_ml_heatmap(client: TestClient, tmp_path: Path) -> None:
    csv_path = tmp_path / "crime.csv"
    csv_path.write_text(
        "\n".join(
            [
                "DR_NO,Date Rptd,DATE OCC,TIME OCC,AREA,AREA NAME,Rpt Dist No,Part 1-2,Crm Cd,Crm Cd Desc,Mocodes,Vict Age,Vict Sex,Vict Descent,Premis Cd,Premis Desc,Weapon Used Cd,Weapon Desc,Status,Status Desc,Crm Cd 1,Crm Cd 2,Crm Cd 3,Crm Cd 4,LOCATION,Cross Street,LAT,LON",
                "1,6/1/2026 0:00,6/1/2026 0:00,2130,1,Central,101,1,510,VEHICLE - STOLEN,0344,25,M,O,101,STREET,,,IC,Invest Cont,510,,,,100 MAIN ST,,34.05,-118.25",
                "2,6/2/2026 0:00,6/2/2026 0:00,2200,1,Central,101,1,510,VEHICLE - STOLEN,0344,31,F,O,101,STREET,,,IC,Invest Cont,510,,,,100 MAIN ST,,34.05,-118.25",
                "3,5/1/2026 0:00,5/1/2026 0:00,1000,2,Harbor,201,1,330,BURGLARY FROM VEHICLE,1402,40,M,O,128,BUS STOP,,,AA,Adult Arrest,330,,,,200 OCEAN AV,,33.75,-118.29",
                "4,6/3/2026 0:00,6/3/2026 0:00,2230,3,Newton,301,1,110,CRIMINAL HOMICIDE,0416,45,M,H,101,STREET,102,HAND GUN,IC,Invest Cont,110,,,,300 MAIN ST,,34.10,-118.30",
                "5,6/4/2026 0:00,6/4/2026 0:00,1400,3,Newton,301,1,668,\"CREDIT CARDS, FRAUD USE ($950.01 & OVER)\",1822,68,F,H,502,MULTI-UNIT DWELLING,,,IC,Invest Cont,668,,,,400 FRAUD ST,,34.11,-118.31",
                "6,6/5/2026 0:00,6/5/2026 0:00,2100,4,Pacific,401,1,110,CRIMINAL HOMICIDE,0416,52,M,B,101,\"VEHICLE, PASSENGER/TRUCK\",307,VEHICLE,IC,Invest Cont,110,,,,500 TRUCK AV,,34.12,-118.32",
                "7,6/6/2026 0:00,6/6/2026 0:00,2300,5,Olympic,501,1,110,CRIMINAL HOMICIDE,0416,37,F,W,101,STREET,207,KNIFE WITH BLADE 6INCHES OR LESS,IC,Invest Cont,110,,,,600 KNIFE RD,,34.13,-118.33",
            ]
        ),
        encoding="utf-8",
    )
    token = login(client, "superadmin")
    imported = client.post(
        "/crime-data/import",
        json={
            "path": str(csv_path),
            "source_system": "test-crime-csv",
            "reset_source": True,
        },
        headers=auth(token),
    )
    assert imported.status_code == 200
    assert imported.json()["imported"] == 7

    status = client.get("/crime-data/status", headers=auth(token))
    assert status.status_code == 200
    assert status.json()["imported_count"] == 7
    assert status.json()["geocoded_count"] == 7

    advanced = client.get("/analytics/advanced-crime", headers=auth(token))
    assert advanced.status_code == 200
    body = advanced.json()
    assert body["heatmap_points"]
    assert body["risk_areas"]
    assert body["network"]["nodes"]

    intelligence_queries = {
        "crime_pattern_discovery": "Crime pattern discovery for vehicle at night",
        "criminal_network_analysis": "Criminal network analysis for vehicle crime by MO weapon and premise",
        "socio_demographic_crime_insight": "Socio-demographic crime insights for female vehicle victims",
        "behavioral_criminological_profiling": "Behavioral criminological profiling for vehicle crime",
        "proactive_crime_prevention_intelligence": "Proactive crime prevention intelligence for vehicle hotspots",
    }
    for expected_intent, query in intelligence_queries.items():
        response = client.post(
            "/intelligence/query",
            json={"query": query, "include_sources": False},
            headers=auth(token),
        )
        assert response.status_code == 200
        payload = response.json()
        assert payload["intent"] == expected_intent
        assert payload["visible_case_count"] >= 1
        assert "incident" in payload["answer"].lower()

    broad_scope = client.post(
        "/intelligence/query",
        json={"query": "Crime pattern discovery across all stored incidents", "include_sources": False},
        headers=auth(token),
    )
    assert broad_scope.status_code == 200
    broad_payload = broad_scope.json()
    assert broad_payload["intent"] == "crime_pattern_discovery"
    assert broad_payload["visible_case_count"] >= 1
    assert broad_payload["query_analysis"]["interpreted_terms"] == []

    forecast_query = client.post(
        "/intelligence/query",
        json={"query": "forecast the crime for next 7 days", "include_sources": False},
        headers=auth(token),
    )
    assert forecast_query.status_code == 200
    forecast_payload = forecast_query.json()
    assert forecast_payload["intent"] == "proactive_crime_prevention_intelligence"
    assert forecast_payload["selected_module"] == "MODULE 8: Forecasting"
    assert forecast_payload["selected_api"] == "GET /forecast/hotspots"
    assert forecast_payload["visible_case_count"] >= 1
    assert forecast_payload["query_analysis"]["interpreted_terms"] == []
    assert "No imported incident records matched" not in forecast_payload["answer"]

    launcher_queries = {
        "crime_pattern_discovery": "Run crime pattern discovery across accessible records. Identify repeat clusters by district, crime type, modus operandi, season, and event context. Return evidence FIRs and prevention leads.",
        "criminal_network_analysis": "Run criminal network analysis. Identify linked suspects, victims, locations, accounts, repeat offender groups, bridge nodes, and money-trail relationships from accessible records.",
        "socio_demographic_crime_insight": "Run socio-demographic crime insights. Summarize age, gender, socio-economic, urbanization, migration, education, and event-context indicators from accessible records with safeguards.",
        "behavioral_criminological_profiling": "Run behavioral and criminological profiling. Identify repeat named persons, habitual patterns, modus operandi indicators, risk factors, and evidence-bound safeguards.",
        "proactive_crime_prevention_intelligence": "Run proactive crime prevention intelligence. Identify early warnings, forecast hotspots, repeat-crime pressure, resource deployment priorities, and transparent evidence trails.",
    }
    for expected_intent, query in launcher_queries.items():
        response = client.post(
            "/intelligence/query",
            json={"query": query, "include_sources": False},
            headers=auth(token),
        )
        assert response.status_code == 200
        payload = response.json()
        assert payload["intent"] == expected_intent
        assert payload["visible_case_count"] >= 1
        assert "No imported incident records matched" not in payload["answer"]

    weapon_query = client.post(
        "/intelligence/query",
        json={"query": "KILL BY WEAPON", "include_sources": False},
        headers=auth(token),
    )
    assert weapon_query.status_code == 200
    weapon_payload = weapon_query.json()
    assert weapon_payload["intent"] == "crime_trend_intelligence"
    assert weapon_payload["visible_case_count"] == 3
    assert "CRIMINAL HOMICIDE" in weapon_payload["answer"]
    assert "HAND GUN" in weapon_payload["answer"]
    assert "KNIFE" in weapon_payload["answer"]
    assert "VEHICLE" in weapon_payload["answer"]
    assert "VEHICLE - STOLEN" not in weapon_payload["answer"]

    money_fraud = client.post(
        "/intelligence/query",
        json={"query": "MONEY FRAUD", "include_sources": False},
        headers=auth(token),
    )
    assert money_fraud.status_code == 200
    money_payload = money_fraud.json()
    assert money_payload["intent"] == "crime_trend_intelligence"
    assert money_payload["visible_case_count"] == 1
    assert "FRAUD" in money_payload["answer"]
    assert "Financial analysis reviews imported transaction records" not in money_payload["answer"]

    age_fraud = client.post(
        "/intelligence/query",
        json={"query": "AGE FRAUD", "include_sources": False},
        headers=auth(token),
    )
    assert age_fraud.status_code == 200
    age_payload = age_fraud.json()
    assert age_payload["intent"] == "socio_demographic_crime_insight"
    assert age_payload["visible_case_count"] == 1
    assert "65+" in age_payload["answer"]

    truck_homicide = client.post(
        "/intelligence/query",
        json={"query": "KILLED BY TRUCK", "include_sources": False},
        headers=auth(token),
    )
    assert truck_homicide.status_code == 200
    truck_payload = truck_homicide.json()
    assert truck_payload["intent"] == "crime_trend_intelligence"
    assert truck_payload["visible_case_count"] == 1
    assert "CRIMINAL HOMICIDE" in truck_payload["answer"]
    assert "VEHICLE" in truck_payload["answer"]

    knife_homicide = client.post(
        "/intelligence/query",
        json={"query": "KILLED BY KNIFE", "include_sources": False},
        headers=auth(token),
    )
    assert knife_homicide.status_code == 200
    knife_payload = knife_homicide.json()
    assert knife_payload["intent"] == "crime_trend_intelligence"
    assert knife_payload["visible_case_count"] == 1
    assert "CRIMINAL HOMICIDE" in knife_payload["answer"]
    assert "KNIFE" in knife_payload["answer"]

    conversation = client.post(
        "/conversations",
        json={"title": "Context isolation check"},
        headers=auth(token),
    )
    assert conversation.status_code == 200
    conversation_id = conversation.json()["id"]
    first_message = client.post(
        f"/conversations/{conversation_id}/messages",
        json={"query": "Crime pattern discovery for vehicle at night"},
        headers=auth(token),
    )
    assert first_message.status_code == 200
    second_message = client.post(
        f"/conversations/{conversation_id}/messages",
        json={"query": "KILL BY WEAPON"},
        headers=auth(token),
    )
    assert second_message.status_code == 200
    second_intelligence = second_message.json()["intelligence"]
    assert second_intelligence["visible_case_count"] == 3
    assert "CRIMINAL HOMICIDE" in second_intelligence["answer"]
    assert "HAND GUN" in second_intelligence["answer"]
    assert "VEHICLE - STOLEN" not in second_intelligence["answer"]


def test_forecast_and_explain_are_permissioned(client: TestClient) -> None:
    supervisor_token = login(client, "supervisor")
    forecast = client.get("/forecast/hotspots", headers=auth(supervisor_token))
    assert forecast.status_code == 200
    assert forecast.json()["hotspots"]

    case_id = client.get("/cases", headers=auth(supervisor_token)).json()[0]["id"]
    explanation = client.get(f"/explain/cases/{case_id}", headers=auth(supervisor_token))
    assert explanation.status_code == 200
    assert explanation.json()["audit"]["evidence_hash"]
