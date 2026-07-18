from __future__ import annotations

import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any

from secure_crime_api.models import AuthenticatedUser
from secure_crime_api.rbac import can_access_case
from secure_crime_api.redaction import mask_case


SAFEGUARDS = [
    "Use this output as an investigative aid, not as a determination of guilt.",
    "Verify all findings against source records before operational action.",
    "Responses only use records the current role is allowed to access.",
]


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def visible_cases(user: AuthenticatedUser, cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [case for case in cases if can_access_case(user, case)]


def trend_summary(cases: list[dict[str, Any]]) -> dict[str, Any]:
    by_district = Counter(case["district"] for case in cases)
    by_status = Counter(case["status"] for case in cases)
    by_sensitivity = Counter(case["sensitivity"] for case in cases)
    by_case_type = Counter(_known_value(case.get("case_type")) for case in cases if _known_value(case.get("case_type")))
    by_modus = Counter(_known_value(case.get("modus_operandi")) for case in cases if _known_value(case.get("modus_operandi")))
    by_month = Counter(_case_month(case) for case in cases if _case_month(case))
    return {
        "total_cases": len(cases),
        "open_cases": by_status.get("open", 0),
        "restricted_cases": by_sensitivity.get("restricted", 0),
        "by_district": _counter_buckets(by_district),
        "by_status": _counter_buckets(by_status),
        "by_sensitivity": _counter_buckets(by_sensitivity),
        "by_case_type": _counter_buckets(by_case_type),
        "by_modus_operandi": _counter_buckets(by_modus),
        "by_month": _counter_buckets(by_month),
        "generated_at": now_utc(),
    }


def network_graph(
    cases: list[dict[str, Any]],
    transactions: list[dict[str, Any]] | None = None,
    role: str = "viewer",
    focus_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    nodes: dict[str, dict[str, Any]] = {}
    links: dict[tuple[str, str, str], dict[str, Any]] = {}
    cases_by_id = {case["id"]: case for case in cases}
    suspect_node_by_case: dict[str, str] = {}
    outgoing_accounts: set[str] = set()
    incoming_accounts: set[str] = set()
    account_context: dict[str, dict[str, Any]] = {}

    for case in cases:
        masked = mask_case(case, role)
        case_node_id = f"case:{case['id']}"
        suspect_node_id = f"person:{_slug(case['suspect_name'])}"
        victim_node_id = f"victim:{_slug(case['victim_name'])}"
        district_node_id = f"district:{_slug(case['district'])}"
        suspect_node_by_case[case["id"]] = suspect_node_id

        case_meta = _case_node_metadata(case, masked)
        case_ref = _case_reference(case, masked)
        _upsert_node(nodes, case_node_id, case["fir_number"], "case", case, case_meta)
        _upsert_node(
            nodes,
            suspect_node_id,
            masked["suspect_name"],
            "suspect",
            case,
            {
                "suspect_name": masked["suspect_name"],
                "age": case.get("suspect_age"),
                "gender": case.get("suspect_gender"),
                "aadhaar_number": case.get("suspect_aadhaar"),
                "cases": [case_ref],
            },
        )
        _upsert_node(
            nodes,
            victim_node_id,
            masked["victim_name"],
            "victim",
            case,
            {"victim_name": masked["victim_name"], "cases": [case_ref]},
        )
        _upsert_node(nodes, district_node_id, case["district"], "district", case)
        _upsert_link(
            links,
            suspect_node_id,
            case_node_id,
            "NAMED_IN_CASE",
            case["id"],
            {"cases": [case_ref]},
        )
        _upsert_link(links, victim_node_id, case_node_id, "VICTIM_IN_CASE", case["id"], {"cases": [case_ref]})
        _upsert_link(links, case_node_id, district_node_id, "REPORTED_IN", case["id"], {"cases": [case_ref]})

        if _known_value(case.get("case_type")):
            type_node_id = f"type:{_slug(case['case_type'])}"
            _upsert_node(nodes, type_node_id, case["case_type"], "crime_type", case)
            _upsert_link(links, case_node_id, type_node_id, "CLASSIFIED_AS", case["id"], {"cases": [case_ref]})
        if _known_value(case.get("modus_operandi")):
            mo_node_id = f"mo:{_slug(case['modus_operandi'])}"
            _upsert_node(nodes, mo_node_id, case["modus_operandi"], "modus_operandi", case)
            _upsert_link(
                links,
                case_node_id,
                mo_node_id,
                "USES_MODUS_OPERANDI",
                case["id"],
                {"cases": [case_ref]},
            )

    for tx in transactions or []:
        if tx.get("case_id") and tx["case_id"] not in cases_by_id:
            continue
        source_node_id = f"account:{_slug(tx['source_account'])}"
        target_node_id = f"account:{_slug(tx['target_account'])}"
        district_case = cases_by_id.get(tx.get("case_id") or "", {"district": tx["district"], "id": tx.get("case_id") or tx["id"]})
        transfer_meta = _transaction_metadata(tx, role)
        linked_case = cases_by_id.get(tx.get("case_id") or "")
        linked_case_ref = _case_reference(linked_case, mask_case(linked_case, role)) if linked_case else None
        outgoing_accounts.add(source_node_id)
        incoming_accounts.add(target_node_id)
        account_context.setdefault(source_node_id, district_case)
        account_context.setdefault(target_node_id, district_case)
        _upsert_node(
            nodes,
            source_node_id,
            _mask_account(tx["source_account"], role),
            "financial_account",
            district_case,
            {
                "account": _mask_account(tx["source_account"], role),
                **_account_metadata(tx, "source", role),
                "outgoing_transfers": [transfer_meta],
                "linked_cases": [linked_case_ref] if linked_case_ref else [],
            },
        )
        _upsert_node(
            nodes,
            target_node_id,
            _mask_account(tx["target_account"], role),
            "financial_account",
            district_case,
            {
                "account": _mask_account(tx["target_account"], role),
                **_account_metadata(tx, "target", role),
                "incoming_transfers": [transfer_meta],
                "linked_cases": [linked_case_ref] if linked_case_ref else [],
            },
        )
        _upsert_link(
            links,
            source_node_id,
            target_node_id,
            "TRANSFERRED_TO",
            tx.get("case_id") or tx["id"],
            {"transactions": [transfer_meta]},
        )
        _upsert_account_holder_node(
            nodes,
            links,
            source_node_id,
            tx,
            "source",
            district_case,
            role,
            transfer_meta,
            linked_case_ref,
        )
        _upsert_account_holder_node(
            nodes,
            links,
            target_node_id,
            tx,
            "target",
            district_case,
            role,
            transfer_meta,
            linked_case_ref,
        )
        if tx.get("case_id"):
            case_node_id = f"case:{tx['case_id']}"
            suspect_node_id = suspect_node_by_case.get(tx["case_id"])
            _append_metadata_item(nodes[case_node_id], "transfers", transfer_meta)
            if suspect_node_id and suspect_node_id in nodes:
                _append_metadata_item(nodes[suspect_node_id], "financial_trails", transfer_meta)
            _upsert_link(
                links,
                case_node_id,
                source_node_id,
                "HAS_FINANCIAL_SOURCE",
                tx["case_id"],
                {"transactions": [transfer_meta]},
            )
            _upsert_link(
                links,
                case_node_id,
                target_node_id,
                "HAS_FINANCIAL_TARGET",
                tx["case_id"],
                {"transactions": [transfer_meta]},
            )
        _upsert_bank_detail_nodes(
            nodes,
            links,
            source_node_id,
            tx,
            "source",
            district_case,
            role,
            transfer_meta,
        )
        _upsert_bank_detail_nodes(
            nodes,
            links,
            target_node_id,
            tx,
            "target",
            district_case,
            role,
            transfer_meta,
        )

    for account_node_id in sorted(incoming_accounts - outgoing_accounts):
        account_node = nodes.get(account_node_id)
        if not account_node:
            continue
        dead_node_id = f"deadend:{account_node_id.removeprefix('account:')}"
        account_label = account_node["label"]
        district_case = account_context.get(account_node_id, {"district": "Unknown", "id": dead_node_id})
        _upsert_node(
            nodes,
            dead_node_id,
            "Trail ends",
            "dead_end",
            district_case,
            {
                "account": account_label,
                "reason": "No outgoing transfer from this account is present in accessible records.",
            },
        )
        _upsert_link(
            links,
            account_node_id,
            dead_node_id,
            "TRAIL_ENDS_AT",
            district_case.get("id", dead_node_id),
            {
                "account": account_label,
                "reason": "No outgoing transfer from this account is present in accessible records.",
            },
        )

    return {
        "nodes": list(nodes.values()),
        "links": list(links.values()),
        "generated_at": now_utc(),
        "focus": focus_metadata or {},
    }


def classify_intent(query: str) -> str:
    text = query.lower()
    if any(word in text for word in ["profile", "habitual", "repeat offender", "risk score", "criminology", "behavioral"]):
        return "offender_profile"
    if any(word in text for word in ["money", "financial", "transaction", "account", "trail", "laundering"]):
        return "financial_analysis"
    if any(word in text for word in ["forecast", "early warning", "early warnings", "predict", "prevention", "preventive", "proactive", "resource deployment"]):
        return "forecasting"
    if any(word in text for word in ["sociological", "demographic", "migration", "urban", "education", "economic"]):
        return "sociological_insight"
    if any(word in text for word in ["network", "relation", "relationship", "associate", "link", "connected", "gang", "cell"]):
        return "network_analysis"
    if any(word in text for word in ["pattern", "cluster", "modus", "mo"]):
        return "pattern_discovery"
    if any(word in text for word in ["trend", "hotspot", "count", "district", "status", "seasonal"]):
        return "trend_analysis"
    if any(word in text for word in ["summary", "summarize", "similar", "lead", "next step", "decision"]):
        return "decision_support"
    if any(word in text for word in ["fir", "case", "suspect", "victim", "complainant"]):
        return "direct_retrieval"
    return "general"


def answer_query(
    query: str,
    cases: list[dict[str, Any]],
    user: AuthenticatedUser,
    include_sources: bool,
    conversation_context: str | None = None,
) -> dict[str, Any]:
    contextual_query = f"{conversation_context or ''} {query}".strip()
    intent = classify_intent(contextual_query)
    accessible_cases = visible_cases(user, cases)
    ranked = rank_cases(contextual_query, accessible_cases)

    if intent == "trend_analysis":
        trend = trend_summary(accessible_cases)
        top_district = trend["by_district"][0]["key"] if trend["by_district"] else "none"
        answer = (
            f"You can access {trend['total_cases']} case(s). "
            f"{trend['open_cases']} are open. The top district in scope is {top_district}."
        )
        sources = ranked[:5]
    elif intent == "pattern_discovery":
        patterns = discover_crime_patterns(accessible_cases)
        if patterns["clusters"]:
            cluster = patterns["clusters"][0]
            answer = (
                f"Pattern discovery found a cluster: {cluster['explanation']} "
                f"Evidence FIRs: {', '.join(cluster['fir_numbers'][:5])}."
            )
        else:
            answer = "No repeat pattern cluster is visible in the records available to your role."
        sources = ranked[:5]
    elif intent == "network_analysis":
        graph = network_graph(accessible_cases)
        suspects = [node for node in graph["nodes"] if node["type"] == "suspect"]
        repeat = [node for node in suspects if node["case_count"] > 1]
        if repeat:
            names = ", ".join(node["label"] for node in repeat[:3])
            bridge_links = len([link for link in graph["links"] if link["relationship"] in {"NAMED_IN", "VICTIM_IN", "OCCURRED_IN"}])
            answer = (
                f"Criminal network analysis found repeat named suspects in accessible records: {names}. "
                f"The visible graph contains {len(graph['nodes'])} node(s), {len(graph['links'])} link(s), "
                f"and {bridge_links} person/case/location association edge(s). Open the Network or SNA Dashboard page for visual link analysis."
            )
        else:
            answer = (
                f"Network review found no repeat named suspects in accessible records. "
                f"The visible graph still contains {len(graph['nodes'])} node(s) and {len(graph['links'])} link(s) for case, location, victim, suspect, and account review."
            )
        sources = ranked[:5]
    elif intent == "sociological_insight":
        trend = trend_summary(accessible_cases)
        top_signal = trend["by_district"][0]["key"] if trend["by_district"] else "no district"
        answer = (
            f"Sociological view is limited to supplied official fields. "
            f"The strongest workload signal in scope is {top_signal}; demographic and social correlations require imported attributes."
        )
        sources = ranked[:5]
    elif intent == "offender_profile":
        suspect_counts = Counter(
            str(case.get("suspect_name") or "").strip()
            for case in accessible_cases
            if str(case.get("suspect_name") or "").strip()
            and str(case.get("suspect_name") or "").strip().lower() not in {"unknown", "n/a", "na"}
        )
        repeat_suspects = [(name, count) for name, count in suspect_counts.most_common(5) if count >= 2]
        if repeat_suspects:
            names = ", ".join(f"{name} ({count})" for name, count in repeat_suspects)
            answer = (
                f"Behavioral and criminological profiling found repeat named-person signals: {names}. "
                "Review their linked FIRs, districts, case types, and modus operandi fields. This is record-linkage intelligence, not a guilt or recidivism decision."
            )
            repeat_names = {name for name, _count in repeat_suspects}
            repeat_cases = [case for case in accessible_cases if case.get("suspect_name") in repeat_names]
            sources = repeat_cases[:5]
        elif ranked:
            answer = (
                f"Use offender profiling on the named suspect from FIR {ranked[0]['fir_number']}. "
                "The profile will be evidence-bound and will not determine guilt."
            )
            sources = ranked[:5]
        else:
            answer = "Provide a suspect/person name from authorized records to build an evidence-bound profile."
            sources = []
    elif intent == "financial_analysis":
        answer = "Financial analysis reviews imported transaction records for high-value, structuring, circular-flow, and account-link signals."
        sources = ranked[:5]
    elif intent == "forecasting":
        trend = trend_summary(accessible_cases)
        if trend["by_district"]:
            answer = f"Early warning should prioritize {trend['by_district'][0]['key']} based on current accessible case volume."
        else:
            answer = "No accessible case volume is available for district-level early warning."
        sources = ranked[:5]
    elif intent == "decision_support":
        if ranked:
            top = ranked[0]
            answer = (
                f"Decision support can summarize FIR {top['fir_number']} and compare it "
                "with accessible cases that share district, status, suspect, or summary terms."
            )
        else:
            answer = "No accessible case matched the request closely enough for decision support."
        sources = ranked[:5]
    elif intent == "direct_retrieval" and is_broad_case_listing_query(query) and accessible_cases:
        trend = trend_summary(accessible_cases)
        sample_firs = ", ".join(case["fir_number"] for case in accessible_cases[:5])
        answer = (
            f"You can access {trend['total_cases']} case(s). "
            f"{trend['open_cases']} are open. Sample accessible FIRs: {sample_firs}."
        )
        sources = accessible_cases[:5]
    elif ranked:
        top = ranked[0]
        answer = (
            f"FIR {top['fir_number']} in {top['district']} is the closest accessible case for this question. "
            f"Current status is {top['status']}."
        )
        sources = ranked[:5]
    else:
        answer = (
            "I could not find an accessible case match. Try a FIR number, district, "
            "case status, or a named person from records you are authorized to view."
        )
        sources = []

    return {
        "intent": intent,
        "answer": answer,
        "visible_case_count": len(accessible_cases),
        "sources": _sources(sources, user.role) if include_sources else [],
        "safeguards": SAFEGUARDS,
    }


def is_broad_case_listing_query(query: str) -> bool:
    terms = set(_terms(query))
    return bool(terms & {"all", "list", "show", "copy", "copies", "karnataka"}) and bool(terms & {"case", "cases", "fir", "firs"})


def build_decision_support(
    case: dict[str, Any],
    all_visible_cases: list[dict[str, Any]],
    role: str,
    notes: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    masked_case = mask_case(case, role)
    similar = similar_cases(case, all_visible_cases)
    timeline = [
        f"{case['created_at']}: FIR {case['fir_number']} entered from {case.get('source_system') or 'case registry'}.",
    ]
    if case.get("incident_at"):
        timeline.insert(0, f"{case['incident_at']}: Incident date/time recorded.")
    if case.get("updated_at") and case.get("updated_at") != case.get("created_at"):
        timeline.append(f"{case['updated_at']}: Case status or metadata updated.")
    for note in notes or []:
        timeline.append(f"{note['created_at']}: Note by {note.get('author_username') or note['author_user_id']}.")

    evidence = [
        f"FIR {case['fir_number']} is recorded in {case['district']}.",
        f"Current status is {case['status']}.",
        f"Sensitivity level is {case['sensitivity']}.",
        f"Summary on record: {case['summary']}",
    ]
    if _known_value(case.get("case_type")):
        evidence.append(f"Crime type: {case['case_type']}.")
    if _known_value(case.get("modus_operandi")):
        evidence.append(f"Modus operandi: {case['modus_operandi']}.")
    leads = [
        "Review shared suspect, victim, location, modus operandi, and financial-account links in the network graph.",
        "Compare evidence and outcome patterns from similar accessible cases.",
    ]
    if case.get("latitude") is not None and case.get("longitude") is not None:
        leads.append("Check nearby geocoded incidents and current hotspot forecast before field deployment.")
    if case["sensitivity"] == "restricted":
        leads.append("Apply restricted-case handling before sharing the support pack.")
    return {
        "case": masked_case,
        "summary": f"FIR {case['fir_number']} is a {case['status']} case in {case['district']}.",
        "evidence": evidence,
        "investigation_timeline": timeline,
        "similar_cases": similar,
        "recommended_next_steps": [
            "Confirm the case facts against primary records before field action.",
            "Review case notes and evidence custody records for gaps.",
            "Check similar accessible cases for shared modus operandi or district coordination needs.",
            "Record any follow-up action in the audit-backed case notes.",
        ],
        "investigative_leads": leads,
        "safeguards": SAFEGUARDS,
    }


def rank_cases(query: str, cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    terms = set(_terms(query))
    scored: list[tuple[int, dict[str, Any]]] = []
    for case in cases:
        haystack = " ".join(
            [
                case["fir_number"],
                case["district"],
                case["status"],
                case["complainant_name"],
                case["victim_name"],
                case["suspect_name"],
                case["summary"],
                str(case.get("case_type") or ""),
                str(case.get("modus_operandi") or ""),
                str(case.get("source_record_id") or ""),
                str(case.get("event_context") or ""),
            ]
        ).lower()
        score = sum(1 for term in terms if term in haystack)
        if case["fir_number"].lower() in query.lower():
            score += 10
        if score:
            scored.append((score, case))

    scored.sort(key=lambda item: (-item[0], item[1]["fir_number"]))
    return [case for _, case in scored]


def similar_cases(case: dict[str, Any], cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    target_terms = set(_terms(case["summary"]))
    results: list[tuple[int, dict[str, Any], list[str]]] = []
    for candidate in cases:
        if candidate["id"] == case["id"]:
            continue
        reasons: list[str] = []
        score = 0
        if candidate["district"] == case["district"]:
            score += 2
            reasons.append("same district")
        if candidate["status"] == case["status"]:
            score += 1
            reasons.append("same status")
        if candidate["suspect_name"].lower() == case["suspect_name"].lower():
            score += 3
            reasons.append("same named suspect")
        if _known_value(candidate.get("case_type")) and candidate.get("case_type") == case.get("case_type"):
            score += 2
            reasons.append("same crime type")
        if _known_value(candidate.get("modus_operandi")) and candidate.get("modus_operandi") == case.get("modus_operandi"):
            score += 3
            reasons.append("same modus operandi")
        shared_terms = target_terms.intersection(_terms(candidate["summary"]))
        if shared_terms:
            score += min(len(shared_terms), 3)
            reasons.append("overlapping summary terms")
        if score:
            results.append((score, candidate, reasons))

    results.sort(key=lambda item: (-item[0], item[1]["fir_number"]))
    return [
        {
            "case_id": candidate["id"],
            "fir_number": candidate["fir_number"],
            "district": candidate["district"],
            "status": candidate["status"],
            "reason": ", ".join(reasons),
        }
        for _, candidate, reasons in results[:5]
    ]


def discover_crime_patterns(cases: list[dict[str, Any]]) -> dict[str, Any]:
    by_case_type = Counter(_known_value(case.get("case_type")) for case in cases if _known_value(case.get("case_type")))
    by_modus = Counter(_known_value(case.get("modus_operandi")) for case in cases if _known_value(case.get("modus_operandi")))
    by_month = Counter(_case_month(case) for case in cases if _case_month(case))
    by_event = Counter(_known_value(case.get("event_context")) for case in cases if _known_value(case.get("event_context")))
    clusters: list[dict[str, Any]] = []
    grouped: dict[tuple[str | None, str | None, str | None], list[dict[str, Any]]] = defaultdict(list)
    for case in cases:
        district = _known_value(case.get("district"))
        case_type = _known_value(case.get("case_type"))
        modus = _known_value(case.get("modus_operandi"))
        keys: set[tuple[str | None, str | None, str | None]] = set()
        if district:
            keys.add((district, None, None))
        if district and case_type:
            keys.add((district, case_type, None))
        if district and modus:
            keys.add((district, None, modus))
        if district and case_type and modus:
            keys.add((district, case_type, modus))
        for key in keys:
            grouped[key].append(case)

    for (district, case_type, modus), grouped_cases in grouped.items():
        if len(grouped_cases) < 2:
            continue
        firs = [case["fir_number"] for case in sorted(grouped_cases, key=lambda item: item["fir_number"])]
        confidence = min(0.92, 0.48 + len(grouped_cases) * 0.08 + (0.08 if case_type and modus else 0))
        descriptor = ", ".join(part for part in [district, case_type, modus] if part)
        clusters.append(
            {
                "key": descriptor,
                "district": district,
                "case_type": case_type,
                "modus_operandi": modus,
                "count": len(grouped_cases),
                "fir_numbers": firs,
                "confidence": round(confidence, 2),
                "explanation": f"{len(grouped_cases)} accessible case(s) share {descriptor}.",
            }
        )

    clusters.sort(key=lambda item: (-item["count"], item["key"]))
    data_quality = []
    if cases and not by_case_type:
        data_quality.append("No official case_type values are present in accessible records.")
    if cases and not by_modus:
        data_quality.append("No official modus_operandi values are present in accessible records.")
    if cases and not by_month:
        data_quality.append("No incident_at timestamps are present; created_at/year are used only for basic chronology.")
    if not cases:
        data_quality.append("No authorized case records are available for pattern discovery.")

    return {
        "total_cases": len(cases),
        "by_case_type": _counter_buckets(by_case_type),
        "by_modus_operandi": _counter_buckets(by_modus),
        "by_month": _counter_buckets(by_month),
        "event_trends": _counter_buckets(by_event),
        "clusters": clusters[:12],
        "data_quality": data_quality,
        "safeguards": SAFEGUARDS
        + ["Pattern clusters are investigative leads, not proof of organization or guilt."],
    }


def _counter_buckets(counter: Counter[str]) -> list[dict[str, Any]]:
    return [
        {"key": key, "count": count}
        for key, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    ]


def _known_value(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _case_month(case: dict[str, Any]) -> str | None:
    raw = case.get("incident_at") or case.get("created_at")
    if not raw:
        return str(case.get("year")) if case.get("year") else None
    try:
        return datetime.fromisoformat(str(raw).replace("Z", "+00:00")).strftime("%Y-%m")
    except ValueError:
        return str(case.get("year")) if case.get("year") else None


def _terms(text: str) -> list[str]:
    return [term for term in re.findall(r"[a-z0-9]+", text.lower()) if len(term) >= 3]


def _slug(text: str) -> str:
    value = "-".join(re.findall(r"[a-z0-9]+", str(text).lower()))
    return value or "unknown"


def _case_reference(case: dict[str, Any], masked_case: dict[str, Any]) -> dict[str, Any]:
    return {
        "case_id": case["id"],
        "case_number": case.get("source_record_id") or case["id"],
        "fir_number": case["fir_number"],
        "district": case["district"],
        "status": case["status"],
        "sensitivity": case["sensitivity"],
        "case_type": case.get("case_type"),
        "modus_operandi": case.get("modus_operandi"),
        "summary": masked_case["summary"],
        "suspect_name": masked_case["suspect_name"],
        "victim_name": masked_case["victim_name"],
        "incident_at": case.get("incident_at"),
    }


def _case_node_metadata(case: dict[str, Any], masked_case: dict[str, Any]) -> dict[str, Any]:
    metadata = _case_reference(case, masked_case)
    metadata.update(
        {
            "year": case.get("year"),
            "complainant_name": masked_case["complainant_name"],
            "latitude": case.get("latitude"),
            "longitude": case.get("longitude"),
            "source_system": case.get("source_system"),
            "source_record_id": case.get("source_record_id"),
            "transfers": [],
        }
    )
    return metadata


def _transaction_metadata(transaction: dict[str, Any], role: str) -> dict[str, Any]:
    return {
        "transaction_id": transaction["id"],
        "occurred_at": transaction.get("occurred_at"),
        "source_account": _mask_account(transaction["source_account"], role),
        "target_account": _mask_account(transaction["target_account"], role),
        "source_account_holder": _mask_person_name(transaction.get("source_account_holder"), role),
        "target_account_holder": _mask_person_name(transaction.get("target_account_holder"), role),
        "source_bank_name": _known_value(transaction.get("source_bank_name")),
        "source_ifsc_code": _known_value(transaction.get("source_ifsc_code")),
        "source_branch": _known_value(transaction.get("source_branch")),
        "source_bank_manager_phone": _mask_phone(transaction.get("source_bank_manager_phone"), role),
        "target_bank_name": _known_value(transaction.get("target_bank_name")),
        "target_ifsc_code": _known_value(transaction.get("target_ifsc_code")),
        "target_branch": _known_value(transaction.get("target_branch")),
        "target_bank_manager_phone": _mask_phone(transaction.get("target_bank_manager_phone"), role),
        "amount": transaction.get("amount", 0),
        "currency": transaction.get("currency") or "INR",
        "district": transaction.get("district"),
        "case_id": transaction.get("case_id"),
        "description": transaction.get("description"),
    }


def _account_metadata(transaction: dict[str, Any], side: str, role: str) -> dict[str, Any]:
    return {
        "account_holder": _mask_person_name(transaction.get(f"{side}_account_holder"), role),
        "bank_name": _known_value(transaction.get(f"{side}_bank_name")),
        "ifsc_code": _known_value(transaction.get(f"{side}_ifsc_code")),
        "branch": _known_value(transaction.get(f"{side}_branch")),
        "bank_manager_phone": _mask_phone(transaction.get(f"{side}_bank_manager_phone"), role),
    }


def _upsert_account_holder_node(
    nodes: dict[str, dict[str, Any]],
    links: dict[tuple[str, str, str], dict[str, Any]],
    account_node_id: str,
    transaction: dict[str, Any],
    side: str,
    district_case: dict[str, Any],
    role: str,
    transfer_meta: dict[str, Any],
    linked_case_ref: dict[str, Any] | None,
) -> None:
    holder = _mask_person_name(transaction.get(f"{side}_account_holder"), role)
    if not holder:
        return
    account_label = _mask_account(transaction[f"{side}_account"], role)
    holder_node_id = f"person:{_slug(holder)}"
    _upsert_node(
        nodes,
        holder_node_id,
        holder,
        "suspect",
        district_case,
        {
            "suspect_name": holder,
            "account_holder": holder,
            "accounts": [account_label],
            "linked_cases": [linked_case_ref] if linked_case_ref else [],
            "financial_trails": [transfer_meta],
        },
    )
    _upsert_link(
        links,
        holder_node_id,
        account_node_id,
        "ACCOUNT_HOLDER_OF",
        transaction.get("case_id") or transaction["id"],
        {"transactions": [transfer_meta], "account_holder": holder},
    )


def _upsert_bank_detail_nodes(
    nodes: dict[str, dict[str, Any]],
    links: dict[tuple[str, str, str], dict[str, Any]],
    account_node_id: str,
    transaction: dict[str, Any],
    side: str,
    district_case: dict[str, Any],
    role: str,
    transfer_meta: dict[str, Any],
) -> None:
    account_label = _mask_account(transaction[f"{side}_account"], role)
    bank_name = _known_value(transaction.get(f"{side}_bank_name"))
    ifsc_code = _known_value(transaction.get(f"{side}_ifsc_code"))
    branch = _known_value(transaction.get(f"{side}_branch"))
    manager_phone = _mask_phone(transaction.get(f"{side}_bank_manager_phone"), role)
    previous_node_id = account_node_id

    if bank_name:
        bank_node_id = f"bank:{_slug(bank_name)}"
        _upsert_node(
            nodes,
            bank_node_id,
            bank_name,
            "bank",
            district_case,
            {"bank_name": bank_name, "accounts": [account_label], "transactions": [transfer_meta]},
        )
        _upsert_link(
            links,
            account_node_id,
            bank_node_id,
            "ACCOUNT_HELD_AT_BANK",
            transaction.get("case_id") or transaction["id"],
            {"transactions": [transfer_meta]},
        )
        previous_node_id = bank_node_id

    if ifsc_code:
        ifsc_node_id = f"ifsc:{_slug(ifsc_code)}"
        _upsert_node(
            nodes,
            ifsc_node_id,
            ifsc_code,
            "ifsc",
            district_case,
            {
                "ifsc_code": ifsc_code,
                "bank_name": bank_name,
                "branch": branch,
                "accounts": [account_label],
                "transactions": [transfer_meta],
            },
        )
        _upsert_link(
            links,
            previous_node_id,
            ifsc_node_id,
            "ROUTED_BY_IFSC",
            transaction.get("case_id") or transaction["id"],
            {"transactions": [transfer_meta]},
        )
        previous_node_id = ifsc_node_id

    if branch:
        branch_node_id = f"branch:{_slug(bank_name or 'bank')}:{_slug(branch)}"
        _upsert_node(
            nodes,
            branch_node_id,
            branch,
            "branch",
            district_case,
            {
                "branch": branch,
                "bank_name": bank_name,
                "ifsc_code": ifsc_code,
                "accounts": [account_label],
                "transactions": [transfer_meta],
            },
        )
        _upsert_link(
            links,
            previous_node_id,
            branch_node_id,
            "SERVICED_BY_BRANCH",
            transaction.get("case_id") or transaction["id"],
            {"transactions": [transfer_meta]},
        )
        previous_node_id = branch_node_id

    if manager_phone:
        manager_node_id = f"manager:{_slug(bank_name or 'bank')}:{_slug(branch or ifsc_code or account_label)}"
        _upsert_node(
            nodes,
            manager_node_id,
            manager_phone,
            "bank_manager",
            district_case,
            {
                "bank_manager_phone": manager_phone,
                "branch": branch,
                "bank_name": bank_name,
                "ifsc_code": ifsc_code,
                "accounts": [account_label],
                "transactions": [transfer_meta],
            },
        )
        _upsert_link(
            links,
            previous_node_id,
            manager_node_id,
            "BRANCH_MANAGER_CONTACT",
            transaction.get("case_id") or transaction["id"],
            {"transactions": [transfer_meta]},
        )


def _upsert_node(
    nodes: dict[str, dict[str, Any]],
    node_id: str,
    label: str,
    node_type: str,
    case: dict[str, Any],
    metadata: dict[str, Any] | None = None,
) -> None:
    node = nodes.setdefault(
        node_id,
        {"id": node_id, "label": label, "type": node_type, "case_count": 0, "districts": [], "metadata": {}},
    )
    node["case_count"] += 1
    if case["district"] not in node["districts"]:
        node["districts"].append(case["district"])
    if metadata:
        _merge_metadata(node["metadata"], metadata)


def _upsert_link(
    links: dict[tuple[str, str, str], dict[str, Any]],
    source: str,
    target: str,
    relationship: str,
    case_id: str,
    metadata: dict[str, Any] | None = None,
) -> None:
    link = links.setdefault(
        (source, target, relationship),
        {"source": source, "target": target, "relationship": relationship, "weight": 0, "case_ids": [], "metadata": {}},
    )
    link["weight"] += 1
    if case_id not in link["case_ids"]:
        link["case_ids"].append(case_id)
    if metadata:
        _merge_metadata(link["metadata"], metadata)


def _merge_metadata(target: dict[str, Any], incoming: dict[str, Any]) -> None:
    for key, value in incoming.items():
        if value is None:
            continue
        if isinstance(value, list):
            target.setdefault(key, [])
            for item in value:
                if item is not None:
                    _append_unique(target[key], item)
        elif isinstance(value, dict):
            target.setdefault(key, {})
            _merge_metadata(target[key], value)
        else:
            target[key] = value


def _append_metadata_item(node: dict[str, Any], key: str, item: dict[str, Any]) -> None:
    metadata = node.setdefault("metadata", {})
    metadata.setdefault(key, [])
    _append_unique(metadata[key], item)


def _append_unique(items: list[Any], item: Any) -> None:
    if item not in items:
        items.append(item)


def _mask_account(account: str, role: str) -> str:
    if role in {"super_admin", "supervisor", "investigator"}:
        return account
    return f"****{account[-4:]}" if len(account) >= 4 else "****"


def _mask_person_name(name: Any, role: str) -> str | None:
    text = _known_value(name)
    if text is None:
        return None
    if role in {"viewer", "policymaker"}:
        return f"{text[0].upper()}. ***" if text else text
    return text


def _mask_phone(phone: Any, role: str) -> str | None:
    text = _known_value(phone)
    if text is None:
        return None
    if role in {"super_admin", "supervisor", "investigator"}:
        return text
    return f"****{text[-4:]}" if len(text) >= 4 else "****"


def _sources(cases: list[dict[str, Any]], role: str) -> list[dict[str, Any]]:
    masked = [mask_case(case, role) for case in cases]
    return [
        {
            "case_id": case["id"],
            "fir_number": case["fir_number"],
            "district": case["district"],
            "status": case["status"],
            "sensitivity": case["sensitivity"],
            "excerpt": str(case["summary"])[:240],
        }
        for case in masked
    ]
