from __future__ import annotations

import hashlib
import re
from collections import Counter, defaultdict
from typing import Any

from secure_crime_api.analytics import SAFEGUARDS, _sources, trend_summary
from secure_crime_api.models import AuthenticatedUser


MODULES = [
    {
        "id": "chat_interface",
        "name": "Conversational Crime Intelligence Interface",
        "status": "implemented",
        "endpoint": "/intelligence/query and /conversations/{id}/messages",
        "security": "JWT, RBAC, district/sensitivity filtering, audit log",
    },
    {
        "id": "translation_voice_pdf",
        "name": "Multi-lingual, Voice-ready, PDF Conversation Support",
        "status": "implemented with local translation fallback and PDF export",
        "endpoint": "/translate, /conversations, /conversations/{id}/export.pdf",
        "security": "Authenticated conversation ownership and audit log",
    },
    {
        "id": "network_analysis",
        "name": "Criminal Network and Relationship Analysis",
        "status": "implemented as local graph projection; Neo4j adapter-ready",
        "endpoint": "/analytics/network",
        "security": "Visible-case graph only",
    },
    {
        "id": "trend_analytics",
        "name": "Trend Analytics and Hotspots",
        "status": "implemented",
        "endpoint": "/analytics/trends, /analytics/patterns, and /forecast/hotspots",
        "security": "Visible-case aggregates only",
    },
    {
        "id": "pattern_discovery",
        "name": "Crime Pattern Discovery",
        "status": "implemented with type, modus operandi, event, seasonal, and cluster signals",
        "endpoint": "/analytics/patterns",
        "security": "Aggregate accessible records only; no proof-of-guilt inference",
    },
    {
        "id": "advanced_crime_ml",
        "name": "Advanced Crime ML, Heatmap, Risk, and Anomaly Intelligence",
        "status": "implemented with local CSV ingestion, heatmap clusters, spike alerts, risk scores, anomalies, and aggregate network links",
        "endpoint": "/crime-data/import, /crime-data/status, /analytics/advanced-crime",
        "security": "Super-admin import, local-only processing, aggregate analytics output",
    },
    {
        "id": "geospatial_mapping",
        "name": "Leaflet Geographic Crime Map and Heat Layer",
        "status": "implemented with optional Google Maps mode",
        "endpoint": "/cases plus browser-rendered Leaflet/OpenStreetMap view",
        "security": "Uses only authorized case records with official coordinates",
    },
    {
        "id": "hash_prefix_search",
        "name": "Hash-Prefix Case Typeahead Search",
        "status": "implemented",
        "endpoint": "/cases/search",
        "security": "Hashed prefixes, RBAC-filtered result set, audited queries",
    },
    {
        "id": "sociological_insights",
        "name": "Sociological Insights",
        "status": "implemented as aggregate workload/status analysis",
        "endpoint": "/analytics/sociological",
        "security": "No protected-class inference; aggregate records only",
    },
    {
        "id": "offender_profiling",
        "name": "Offender Profiling",
        "status": "implemented as evidence-bound named-suspect profile",
        "endpoint": "/profiles/suspects/{suspect_name}",
        "security": "No autonomous guilt or recidivism prediction",
    },
    {
        "id": "decision_support",
        "name": "Decision Support",
        "status": "implemented",
        "endpoint": "/decision-support/cases/{case_id}",
        "security": "Evidence trail, similar cases, and human-review safeguards",
    },
    {
        "id": "financial_analysis",
        "name": "Financial Analysis",
        "status": "implemented with local transaction triage",
        "endpoint": "/financial/analysis",
        "security": "Role-aware account masking and district filtering",
    },
    {
        "id": "forecasting",
        "name": "Forecasting and Early Warning",
        "status": "implemented with deterministic baseline forecast",
        "endpoint": "/forecast/hotspots",
        "security": "Aggregate district-level output only",
    },
    {
        "id": "explainable_ai",
        "name": "Explainable AI and Evidence Trails",
        "status": "implemented as deterministic explanation and audit hash trail",
        "endpoint": "/explain/cases/{case_id}",
        "security": "No hidden model decisions; factors and evidence returned",
    },
    {
        "id": "rbac",
        "name": "RBAC, Data Masking, Rate Limiting, Session Revocation, Audit Logs",
        "status": "implemented",
        "endpoint": "/auth/*, /audit/*, /admin/rate-limit-alerts",
        "security": "Argon2, JWT, revocation, permission matrix, rate-limit alerts, audit hash chain",
    },
    {
        "id": "fingerprint_biometric",
        "name": "Fingerprint Registration and Login",
        "status": "implemented with WebAuthn biometric challenge verification",
        "endpoint": "/auth/fingerprint/register/*, /auth/fingerprint/login/*",
        "security": "Fingerprint template stays on device; server stores public credential key, sign counter, and audit events",
    },
    {
        "id": "super_admin",
        "name": "Super Admin User Management",
        "status": "implemented",
        "endpoint": "/admin/users",
        "security": "Super-admin-only user lifecycle control and audit logging",
    },
]


SOLUTION_FRAMEWORK = [
    {
        "id": "conversational_crime_intelligence",
        "title": "Conversational Crime Intelligence Interface",
        "objective": "Natural-language, context-aware querying of FIRs, accused, victims, locations, investigation status, and history.",
        "capabilities": [
            "English/Kannada query flow",
            "Conversation memory",
            "Voice input boundary",
            "Local PDF export",
            "Evidence-bound sources",
        ],
        "endpoints": ["/intelligence/query", "/conversations/{id}/messages", "/conversations/{id}/export.pdf", "/translate"],
    },
    {
        "id": "criminal_network_relationship_analysis",
        "title": "Criminal Network and Relationship Analysis",
        "objective": "Reveal links between suspects, victims, locations, crime incidents, accounts, and money trails.",
        "capabilities": [
            "Suspect-case-account graph",
            "Repeat offender link detection",
            "Money-transfer trail graph",
            "Professional SNA dashboard",
            "Community/cell analysis artifact",
        ],
        "endpoints": ["/analytics/network", "/dashboards/criminal-network"],
    },
    {
        "id": "crime_pattern_trend_analytics",
        "title": "Crime Pattern and Trend Analytics",
        "objective": "Detect repeat patterns across time, geography, crime type, modus operandi, events, and clusters.",
        "capabilities": [
            "District/type/MO clusters",
            "Seasonal/monthly trend buckets",
            "Event-based signals",
            "Hotspot and emerging cluster summaries",
        ],
        "endpoints": ["/analytics/patterns", "/analytics/trends", "/analytics/advanced-crime"],
    },
    {
        "id": "sociological_crime_insights",
        "title": "Sociological Crime Insights",
        "objective": "Analyze aggregate demographic and social-context fields while avoiding protected-class causation claims.",
        "capabilities": [
            "Age/gender aggregate mix",
            "Socio-economic context summaries",
            "Urbanization, migration, education, and event indicators",
            "Correlation-readiness guidance",
        ],
        "endpoints": ["/analytics/sociological"],
    },
    {
        "id": "criminology_offender_profiling",
        "title": "Criminology-Based Offender Profiling",
        "objective": "Build evidence-bound named-person profiles from accessible case linkages without autonomous guilt assessment.",
        "capabilities": [
            "Partial-name suspect lookup",
            "Repeat named-person linkage",
            "MO and case-type behavioral indicators",
            "Record-linkage risk scoring",
        ],
        "endpoints": ["/profiles/suspects/{suspect_name}"],
    },
    {
        "id": "investigator_decision_support",
        "title": "Investigator Decision Support",
        "objective": "Provide automated case summaries, timelines, similar cases, and human-review investigation leads.",
        "capabilities": [
            "Case summary",
            "Investigation timeline",
            "Similar case retrieval",
            "Potential lead checklist",
            "Evidence hash trail",
        ],
        "endpoints": ["/decision-support/cases/{case_id}", "/explain/cases/{case_id}"],
    },
    {
        "id": "financial_crime_transaction_links",
        "title": "Financial Crime and Transaction Link Analysis",
        "objective": "Detect high-value transfers, structuring, circular flows, mule accounts, and account-link networks.",
        "capabilities": [
            "Transaction import",
            "High-value transfer triage",
            "Structuring signals",
            "Circular-flow detection",
            "Role-aware account masking",
        ],
        "endpoints": ["/financial/analysis", "/financial/transactions/import"],
    },
    {
        "id": "crime_forecasting_early_warning",
        "title": "Crime Forecasting and Early Warning",
        "objective": "Generate district-level planning forecasts and early-warning messages for repeat hotspot pressure.",
        "capabilities": [
            "Baseline hotspot forecast",
            "Repeat-volume warning",
            "Restricted-case handling warning",
            "Prevention-planning drivers",
        ],
        "endpoints": ["/forecast/hotspots"],
    },
    {
        "id": "explainable_transparent_analytics",
        "title": "Explainable AI and Transparent Analytics",
        "objective": "Return visible evidence, reasoning paths, audit hashes, and safeguards for accountable law-enforcement use.",
        "capabilities": [
            "Evidence references",
            "Reasoning path display",
            "Audit hash chain",
            "No hidden autonomous guilt decisions",
        ],
        "endpoints": ["/explain/cases/{case_id}", "/audit/integrity", "/audit/logs"],
    },
    {
        "id": "secure_rbac_governance",
        "title": "Secure Role-Based Access and Governance",
        "objective": "Protect sensitive records with RBAC, district/sensitivity filtering, rate limits, revocation, and traceability.",
        "capabilities": [
            "Argon2/JWT authentication",
            "Fingerprint/passkey login",
            "Role and district access controls",
            "Rate-limit breach alerts",
            "Super-admin user lifecycle",
        ],
        "endpoints": ["/auth/*", "/admin/users", "/admin/rate-limit-alerts", "/auth/fingerprint/*"],
    },
]


CORE_INTELLIGENCE_TASKS = [
    {
        "id": "crime_pattern_discovery",
        "label": "Crime pattern discovery",
        "prompt": "Run crime pattern discovery across accessible records. Identify repeat clusters by district, crime type, modus operandi, season, and event context. Return evidence FIRs and prevention leads.",
    },
    {
        "id": "criminal_network_analysis",
        "label": "Criminal network analysis",
        "prompt": "Run criminal network analysis. Identify linked suspects, victims, locations, accounts, repeat offender groups, bridge nodes, and money-trail relationships from accessible records.",
    },
    {
        "id": "socio_demographic_insights",
        "label": "Socio-demographic crime insights",
        "prompt": "Run socio-demographic crime insights. Summarize age, gender, socio-economic, urbanization, migration, education, and event-context indicators from accessible records with safeguards.",
    },
    {
        "id": "behavioral_criminology_profile",
        "label": "Behavioral and criminological profiling",
        "prompt": "Run behavioral and criminological profiling. Identify repeat named persons, habitual patterns, modus operandi indicators, risk factors, and evidence-bound safeguards.",
    },
    {
        "id": "proactive_prevention_intelligence",
        "label": "Proactive crime prevention intelligence",
        "prompt": "Run proactive crime prevention intelligence. Identify early warnings, forecast hotspots, repeat-crime pressure, resource deployment priorities, and transparent evidence trails.",
    },
]


GLOSSARY = {
    ("en", "kn"): {
        "case": "ಪ್ರಕರಣ",
        "fir": "ಎಫ್ಐಆರ್",
        "status": "ಸ್ಥಿತಿ",
        "district": "ಜಿಲ್ಲೆ",
        "suspect": "ಆರೋಪಿ",
        "victim": "ಬಾಧಿತ",
        "open": "ತೆರೆದ",
        "closed": "ಮುಚ್ಚಿದ",
        "fraud": "ವಂಚನೆ",
        "theft": "ಕಳ್ಳತನ",
        "network": "ಜಾಲ",
        "trend": "ಪ್ರವೃತ್ತಿ",
        "hotspot": "ಹಾಟ್‌ಸ್ಪಾಟ್",
        "evidence": "ಸಾಕ್ಷ್ಯ",
        "forecast": "ಮುನ್ಸೂಚನೆ",
        "profile": "ಪ್ರೊಫೈಲ್",
    },
    ("kn", "en"): {
        "ಪ್ರಕರಣ": "case",
        "ಎಫ್ಐಆರ್": "fir",
        "ಸ್ಥಿತಿ": "status",
        "ಜಿಲ್ಲೆ": "district",
        "ಆರೋಪಿ": "suspect",
        "ಬಾಧಿತ": "victim",
        "ತೆರೆದ": "open",
        "ಮುಚ್ಚಿದ": "closed",
        "ವಂಚನೆ": "fraud",
        "ಕಳ್ಳತನ": "theft",
        "ಜಾಲ": "network",
        "ಪ್ರವೃತ್ತಿ": "trend",
        "ಹಾಟ್‌ಸ್ಪಾಟ್": "hotspot",
        "ಸಾಕ್ಷ್ಯ": "evidence",
        "ಮುನ್ಸೂಚನೆ": "forecast",
        "ಪ್ರೊಫೈಲ್": "profile",
    },
}


def translate_text(text: str, source_language: str, target_language: str) -> dict[str, Any]:
    if source_language == target_language:
        return {
            "source_language": source_language,
            "target_language": target_language,
            "translated_text": text,
            "confidence": 1.0,
            "provider": "identity",
            "notes": ["Source and target languages are the same."],
        }

    glossary = GLOSSARY.get((source_language, target_language), {})

    def replace(match: re.Match[str]) -> str:
        word = match.group(0)
        translated = glossary.get(word.lower())
        if not translated:
            return word
        return translated.capitalize() if word[:1].isupper() else translated

    translated = re.sub(r"[A-Za-z]+", replace, text)
    for source, target in sorted(glossary.items(), key=lambda item: len(item[0]), reverse=True):
        if source_language == "kn":
            translated = translated.replace(source, target)
    changed = translated != text
    return {
        "source_language": source_language,
        "target_language": target_language,
        "translated_text": translated,
        "confidence": 0.72 if changed else 0.35,
        "provider": "local-glossary-adapter",
        "notes": [
            "Local deterministic fallback is active.",
            "Connect NLLB, IndicTrans, or an approved translation service for full production coverage.",
        ],
    }


def sociological_insights(cases: list[dict[str, Any]]) -> dict[str, Any]:
    trend = trend_summary(cases)
    victim_gender = Counter(
        str(case["victim_gender"]).strip()
        for case in cases
        if case.get("victim_gender") and str(case["victim_gender"]).strip()
    )
    suspect_gender = Counter(
        str(case["suspect_gender"]).strip()
        for case in cases
        if case.get("suspect_gender") and str(case["suspect_gender"]).strip()
    )
    victim_age = Counter(_age_band(case.get("victim_age")) for case in cases if case.get("victim_age") is not None)
    suspect_age = Counter(_age_band(case.get("suspect_age")) for case in cases if case.get("suspect_age") is not None)
    social_signals = Counter()
    for field in [
        "socio_economic_context",
        "urbanization_context",
        "migration_context",
        "education_context",
        "event_context",
    ]:
        for case in cases:
            value = str(case.get(field) or "").strip()
            if value:
                social_signals[f"{field.replace('_context', '')}: {value}"] += 1

    observations: list[str] = []
    if trend["by_district"]:
        top = trend["by_district"][0]
        observations.append(f"{top['key']} has the highest accessible case workload ({top['count']}).")
    if trend["restricted_cases"]:
        observations.append(f"{trend['restricted_cases']} restricted case(s) require tighter handling.")
    if trend["open_cases"]:
        observations.append(f"{trend['open_cases']} open case(s) may need active follow-up.")
    if not observations:
        observations.append("No accessible cases are available for aggregate insight.")
    if not any([victim_gender, suspect_gender, victim_age, suspect_age, social_signals]):
        observations.append("Demographic and social-context fields are not yet present in the accessible official records.")

    correlations = []
    if trend["by_case_type"] and social_signals:
        correlations.append(
            "Case type and social-context fields are both present; compare distributions before drawing operational hypotheses."
        )
    if trend["by_district"] and social_signals:
        correlations.append("District workload can be reviewed against imported urbanization, migration, education, or event indicators.")
    if not correlations:
        correlations.append("No cross-factor correlation is computed until official demographic/social indicator fields are populated.")

    return {
        "total_cases": trend["total_cases"],
        "district_workload": trend["by_district"],
        "sensitivity_mix": trend["by_sensitivity"],
        "status_mix": trend["by_status"],
        "demographic_mix": {
            "victim_gender": _counter_buckets(victim_gender),
            "suspect_gender": _counter_buckets(suspect_gender),
            "victim_age": _counter_buckets(victim_age),
            "suspect_age": _counter_buckets(suspect_age),
        },
        "social_indicators": _counter_buckets(social_signals),
        "correlations": correlations,
        "observations": observations,
        "safeguards": SAFEGUARDS
        + ["This module reports aggregate workload signals only, not social-group causation."],
    }


def suspect_profile(suspect_name: str, cases: list[dict[str, Any]], role: str) -> dict[str, Any]:
    normalized = suspect_name.strip().lower()
    matches = [
        case
        for case in cases
        if normalized
        and (
            case["suspect_name"].lower() == normalized
            or any(part.startswith(normalized) for part in case["suspect_name"].lower().split())
            or normalized in case["suspect_name"].lower()
        )
    ]
    statuses = Counter(case["status"] for case in matches)
    districts = sorted({case["district"] for case in matches})
    modus = sorted({case["modus_operandi"] for case in matches if case.get("modus_operandi")})
    case_types = sorted({case["case_type"] for case in matches if case.get("case_type")})
    risk_factors: list[str] = []
    score = 0
    if len(matches) >= 2:
        score += min(35, len(matches) * 10)
        risk_factors.append("named in multiple accessible cases")
    if len(districts) >= 2:
        score += 20
        risk_factors.append("appears across multiple districts")
    if statuses.get("open", 0):
        score += min(20, statuses["open"] * 5)
        risk_factors.append("open investigations in accessible records")
    if modus:
        score += min(15, len(modus) * 5)
        risk_factors.append("modus operandi fields are available for comparison")
    risk_level = "none"
    if score >= 60:
        risk_level = "high"
    elif score >= 30:
        risk_level = "medium"
    elif score > 0:
        risk_level = "low"
    behavioral_indicators = []
    if case_types:
        behavioral_indicators.append(f"Crime type history: {', '.join(case_types[:5])}.")
    if modus:
        behavioral_indicators.append(f"Recorded modus operandi: {', '.join(modus[:5])}.")
    if not behavioral_indicators:
        behavioral_indicators.append("No official modus operandi or crime-type history is present for this named person.")
    return {
        "suspect_name": suspect_name,
        "named_in_case_count": len(matches),
        "districts": districts,
        "statuses": [{"key": key, "count": count} for key, count in sorted(statuses.items())],
        "cases": _sources(matches, role),
        "risk_score": min(score, 100),
        "risk_level": risk_level,
        "risk_factors": risk_factors,
        "behavioral_indicators": behavioral_indicators,
        "profile": (
            f"{suspect_name} is named in {len(matches)} accessible case(s). "
            "This is a record linkage profile and does not determine guilt."
        ),
        "safeguards": SAFEGUARDS
        + ["Do not use this as an automated recidivism prediction or guilt assessment."],
    }


def analyze_financial_transactions(
    transactions: list[dict[str, Any]],
    role: str,
) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    total = sum(float(tx["amount"]) for tx in transactions)

    high_value = [tx for tx in transactions if float(tx["amount"]) >= 1_000_000]
    if high_value:
        findings.append(
            {
                "finding_type": "high_value_transfer",
                "severity": "high",
                "description": f"{len(high_value)} high-value transfer(s) exceed the configured review threshold.",
                "related_transaction_ids": [tx["id"] for tx in high_value],
            }
        )

    near_threshold_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for tx in transactions:
        amount = float(tx["amount"])
        if 900_000 <= amount < 1_000_000:
            near_threshold_by_source[tx["source_account"]].append(tx)
    for account, grouped in near_threshold_by_source.items():
        if len(grouped) >= 2:
            findings.append(
                {
                    "finding_type": "possible_structuring",
                    "severity": "medium",
                    "description": f"Multiple near-threshold transfers originate from {mask_account(account, role)}.",
                    "related_transaction_ids": [tx["id"] for tx in grouped],
                }
            )

    circular = _circular_pairs(transactions)
    if circular:
        findings.append(
            {
                "finding_type": "possible_circular_flow",
                "severity": "medium",
                "description": "Reciprocal account flows were found in accessible transactions.",
                "related_transaction_ids": sorted({tx_id for pair in circular for tx_id in pair}),
            }
        )

    pair_totals: dict[tuple[str, str], dict[str, Any]] = {}
    for tx in transactions:
        key = (tx["source_account"], tx["target_account"])
        row = pair_totals.setdefault(
            key,
            {
                "source_account": mask_account(tx["source_account"], role),
                "target_account": mask_account(tx["target_account"], role),
                "transaction_count": 0,
                "total_amount": 0.0,
            },
        )
        row["transaction_count"] += 1
        row["total_amount"] += float(tx["amount"])
    account_links = sorted(
        pair_totals.values(),
        key=lambda item: (-float(item["total_amount"]), str(item["source_account"])),
    )[:25]

    return {
        "transaction_count": len(transactions),
        "total_amount": total,
        "findings": findings,
        "account_links": account_links,
        "safeguards": SAFEGUARDS
        + ["Financial findings are triage signals; verify bank records and legal process requirements."],
    }


def forecast_hotspots(cases: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(case["district"] for case in cases)
    hotspots = []
    for district, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        projected = max(count, round(count * 1.15))
        drivers = ["current accessible case volume"]
        if any(case["sensitivity"] == "restricted" for case in cases if case["district"] == district):
            drivers.append("restricted-case handling load")
        hotspots.append(
            {
                "district": district,
                "current_cases": count,
                "projected_7_day_cases": projected,
                "confidence": 0.62 if count else 0.0,
                "drivers": drivers,
            }
        )
    early_warnings = []
    for item in hotspots[:5]:
        if item["current_cases"] >= 2:
            early_warnings.append(
                f"{item['district']} has repeat accessible case volume; review patrol, prevention, and investigation capacity."
            )
        if "restricted-case handling load" in item["drivers"]:
            early_warnings.append(f"{item['district']} includes restricted records; keep dissemination controlled.")
    if not early_warnings and cases:
        early_warnings.append("No repeat hotspot threshold crossed in accessible records.")
    if not cases:
        early_warnings.append("No authorized case records are available for early warning.")
    return {
        "generated_at": trend_summary(cases)["generated_at"],
        "hotspots": hotspots,
        "early_warnings": early_warnings,
        "safeguards": SAFEGUARDS
        + ["Forecasts are baseline planning estimates, not predictions of individual behavior."],
    }


def explain_case(case: dict[str, Any], latest_audit_hash: str | None) -> dict[str, Any]:
    factors = [
        f"District: {case['district']}",
        f"Status: {case['status']}",
        f"Sensitivity: {case['sensitivity']}",
        "Summary text is used for retrieval and similarity scoring.",
    ]
    if case.get("case_type"):
        factors.append(f"Crime type: {case['case_type']}")
    if case.get("modus_operandi"):
        factors.append(f"Modus operandi: {case['modus_operandi']}")
    evidence = [
        f"FIR number: {case['fir_number']}",
        f"Named suspect field: {case['suspect_name']}",
        f"Summary: {case['summary']}",
    ]
    digest = hashlib.sha256("|".join(evidence).encode("utf-8")).hexdigest()
    return {
        "subject_type": "case",
        "subject_id": case["id"],
        "explanation": "This case appears in outputs when RBAC allows access and query terms match case fields.",
        "factors": factors,
        "evidence": evidence,
        "reasoning_path": [
            "Authenticate user and resolve role permissions.",
            "Filter records by role, district, and sensitivity.",
            "Match the requested FIR, terms, graph relationship, or analytic module against accessible fields.",
            "Return references and audit hashes so the output can be reviewed.",
        ],
        "correlations": [
            "District, status, sensitivity, crime type, and modus operandi are correlation factors when present.",
            "No hidden model-only factor is used in this deterministic explanation.",
        ],
        "audit": {"latest_audit_hash": latest_audit_hash, "evidence_hash": digest},
        "safeguards": SAFEGUARDS,
    }


def mask_account(account: str, role: str) -> str:
    if role in {"super_admin", "supervisor", "investigator"}:
        return account
    return f"****{account[-4:]}" if len(account) >= 4 else "****"


def _circular_pairs(transactions: list[dict[str, Any]]) -> list[tuple[str, str]]:
    by_pair: dict[tuple[str, str], str] = {}
    circular: list[tuple[str, str]] = []
    for tx in transactions:
        pair = (tx["source_account"], tx["target_account"])
        reverse = (tx["target_account"], tx["source_account"])
        if reverse in by_pair:
            circular.append((by_pair[reverse], tx["id"]))
        by_pair[pair] = tx["id"]
    return circular


def _counter_buckets(counter: Counter[str]) -> list[dict[str, Any]]:
    return [
        {"key": key, "count": count}
        for key, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    ]


def _age_band(value: Any) -> str:
    age = int(value)
    if age < 18:
        return "0-17"
    if age < 30:
        return "18-29"
    if age < 45:
        return "30-44"
    if age < 60:
        return "45-59"
    return "60+"
