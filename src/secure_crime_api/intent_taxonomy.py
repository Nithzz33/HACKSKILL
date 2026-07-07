from __future__ import annotations

import re
from dataclasses import dataclass
from itertools import product
from typing import Any


@dataclass(frozen=True)
class IntentCategory:
    key: str
    canonical_intent: str
    response_rule: str
    query_records: bool
    starts: tuple[str, ...]
    subjects: tuple[str, ...]
    qualifiers: tuple[str, ...]
    keywords: tuple[str, ...]


EN_CASE_NAMES = ("Ravi Kumar", "Mahesh", "Akash Shetty", "A1", "FIR BLR-001")
DISTRICTS = ("Bengaluru", "Mysuru", "Tumakuru", "Kalaburagi", "Karnataka")
CRIME_TYPES = ("murder", "theft", "fraud", "vehicle theft", "assault")
KANNADA_NAMES = (
    "\u0cb0\u0cb5\u0cbf\u0c95\u0cc1\u0cae\u0cbe\u0cb0\u0ccd",
    "\u0cae\u0cb9\u0cc7\u0cb6\u0ccd",
    "\u0c85\u0c95\u0cbe\u0cb6\u0ccd",
)


INTENT_CATEGORIES: tuple[IntentCategory, ...] = (
    IntentCategory(
        key="greeting",
        canonical_intent="conversation_smalltalk",
        response_rule="Friendly greeting only. Do not query crime records.",
        query_records=False,
        starts=("hi", "hello", "hlo", "hey", "good morning", "good evening", "namaskara"),
        subjects=("", "ksp ai", "assistant", "team", "sir"),
        qualifiers=("", "please", "are you ready", "start"),
        keywords=("hi", "hello", "hlo", "hey", "namaskara", "good morning", "good evening"),
    ),
    IntentCategory(
        key="capability_questions",
        canonical_intent="system_identity",
        response_rule="Explain KSP AI capabilities without querying crime records.",
        query_records=False,
        starts=(
            "what can you do",
            "who are you",
            "help",
            "show capabilities",
            "explain system",
            "what is your motto",
            "what is your moto",
            "what is your mission",
            "what is your purpose",
            "how can you help",
            "how should i ask",
            "what all can you do",
            "show all features",
            "show full capability",
        ),
        subjects=("ksp ai", "crime assistant", "platform", "chatbot", "system"),
        qualifiers=("", "for investigators", "for analysts", "in Kannada", "briefly"),
        keywords=(
            "what can you do",
            "who are you",
            "capability",
            "capabilities",
            "help",
            "motto",
            "moto",
            "mission",
            "purpose",
            "how can you help",
            "how should i ask",
            "what all can you do",
            "features",
            "full capability",
        ),
    ),
    IntentCategory(
        key="fir_lookup",
        canonical_intent="fir_lookup",
        response_rule="Prioritize FIR number, police station, status, persons, and evidence reference.",
        query_records=True,
        starts=("show", "find", "search", "open", "fetch"),
        subjects=("FIR details", "FIR file", "FIR number", "case file", "record"),
        qualifiers=EN_CASE_NAMES,
        keywords=("fir", "file", "number", "details"),
    ),
    IntentCategory(
        key="case_lookup",
        canonical_intent="case_summary",
        response_rule="Return direct case details and evidence reference.",
        query_records=True,
        starts=("show", "find", "search", "summarize", "open"),
        subjects=("case", "case status", "case summary", "case details", "investigation record"),
        qualifiers=EN_CASE_NAMES + DISTRICTS,
        keywords=("case", "status", "summary", "details"),
    ),
    IntentCategory(
        key="suspect_profile",
        canonical_intent="offender_profile",
        response_rule="Show profile summary, linked FIRs, evidence references, and suggested actions.",
        query_records=True,
        starts=("show", "tell me about", "profile", "search", "what did"),
        subjects=("suspect", "accused", "person", "offender", "named person"),
        qualifiers=EN_CASE_NAMES,
        keywords=("suspect", "accused", "profile", "offender", "details"),
    ),
    IntentCategory(
        key="victim_lookup",
        canonical_intent="victim_lookup",
        response_rule="Show victim field, FIR, status, complainant, and evidence reference.",
        query_records=True,
        starts=("show", "find", "search", "who is", "list"),
        subjects=("victim", "victim name", "victim details", "injured person", "complainant linked victim"),
        qualifiers=EN_CASE_NAMES,
        keywords=("victim", "victim name", "injured"),
    ),
    IntentCategory(
        key="complainant_lookup",
        canonical_intent="complainant_lookup",
        response_rule="Prioritize complainant name, FIR number, police station, status, and evidence source.",
        query_records=True,
        starts=("who filed", "who gave", "find", "show", "search"),
        subjects=("complaint", "complainant", "complaint by", "complaint filed by", "reporter"),
        qualifiers=EN_CASE_NAMES,
        keywords=("complainant", "complaint", "who filed", "filed complaint", "complaint by"),
    ),
    IntentCategory(
        key="network_analysis",
        canonical_intent="criminal_network_analysis",
        response_rule="Show linked people, cases, locations, accounts, and relationship evidence.",
        query_records=True,
        starts=("show", "find", "run", "analyze", "map"),
        subjects=("network", "links", "associates", "relationships", "criminal cell"),
        qualifiers=EN_CASE_NAMES + CRIME_TYPES,
        keywords=("network", "link", "links", "associate", "relationship", "cell"),
    ),
    IntentCategory(
        key="money_trails",
        canonical_intent="financial_analysis",
        response_rule="Show transaction chain, accounts, dead ends, circular flows, and linked FIRs.",
        query_records=True,
        starts=("show", "trace", "find", "analyze", "map"),
        subjects=("money trail", "transaction chain", "account chain", "fund transfer", "mule account"),
        qualifiers=EN_CASE_NAMES,
        keywords=("money", "trail", "transaction", "transfer", "account", "mule"),
    ),
    IntentCategory(
        key="fraud_analysis",
        canonical_intent="financial_analysis",
        response_rule="Show fraud-linked cases, money movement, account indicators, and evidence sources.",
        query_records=True,
        starts=("show", "find", "analyze", "detect", "list"),
        subjects=("fraud", "financial fraud", "money fraud", "cyber fraud", "bank fraud"),
        qualifiers=EN_CASE_NAMES + DISTRICTS,
        keywords=("fraud", "financial", "bank", "cyber"),
    ),
    IntentCategory(
        key="hotspot_analysis",
        canonical_intent="crime_trend_intelligence",
        response_rule="Show hotspot area, crime type, count, period, and prevention lead.",
        query_records=True,
        starts=("show", "find", "map", "analyze", "list"),
        subjects=("hotspots", "heat map", "crime cluster", "risk area", "district hotspot"),
        qualifiers=DISTRICTS + CRIME_TYPES,
        keywords=("hotspot", "hotspots", "heatmap", "heat", "cluster"),
    ),
    IntentCategory(
        key="trend_analysis",
        canonical_intent="crime_trend_intelligence",
        response_rule="Show trend summary by time, geography, crime type, and evidence window.",
        query_records=True,
        starts=("show", "compare", "analyze", "trend", "list"),
        subjects=("trend", "seasonal trend", "district trend", "crime trend", "monthly trend"),
        qualifiers=DISTRICTS + CRIME_TYPES,
        keywords=("trend", "seasonal", "month", "district", "count"),
    ),
    IntentCategory(
        key="forecasting",
        canonical_intent="proactive_crime_prevention_intelligence",
        response_rule="Show early warning and prevention planning without claiming certainty.",
        query_records=True,
        starts=("forecast", "predict", "show", "find", "identify"),
        subjects=("hotspot forecast", "early warning", "risk forecast", "prevention plan", "future risk"),
        qualifiers=DISTRICTS + CRIME_TYPES,
        keywords=("forecast", "predict", "early warning", "prevention", "proactive"),
    ),
    IntentCategory(
        key="audit_requests",
        canonical_intent="admin_audit_lookup",
        response_rule="Use audit/RBAC data only; no case inference.",
        query_records=False,
        starts=("show", "check", "list", "review", "audit"),
        subjects=("audit log", "activity", "access history", "rate limit breach", "traceability"),
        qualifiers=("", "today", "latest", "for user", "for admin"),
        keywords=("audit", "activity", "access history", "rate limit", "traceability"),
    ),
    IntentCategory(
        key="user_management",
        canonical_intent="admin_user_management",
        response_rule="Use governance data only; describe account controls and RBAC restrictions.",
        query_records=False,
        starts=("show", "create", "block", "delete", "reset"),
        subjects=("users", "user account", "roles", "permissions", "admin dashboard"),
        qualifiers=("", "investigator", "analyst", "super admin", "district user"),
        keywords=("user", "users", "role", "permission", "block", "delete", "reset password"),
    ),
    IntentCategory(
        key="kannada_greetings",
        canonical_intent="conversation_smalltalk",
        response_rule="Friendly Kannada greeting only. Do not query crime records.",
        query_records=False,
        starts=("\u0ca8\u0cae\u0cb8\u0ccd\u0c95\u0cbe\u0cb0", "\u0cb9\u0cc8", "\u0cb9\u0cc6\u0cb2\u0ccd\u0cb2\u0ccb", "\u0cb6\u0cc1\u0cad \u0cac\u0cc6\u0cb3\u0c97\u0ccd\u0c97\u0cc6", "\u0cb6\u0cc1\u0cad \u0cb8\u0cbe\u0caf\u0c82\u0c95\u0cbe\u0cb2"),
        subjects=("", "\u0c95\u0cc6\u0c8e\u0cb8\u0ccd\u0caa\u0cbf", "\u0c8e\u0c90", "\u0cb8\u0cb9\u0cbe\u0caf\u0c95", "\u0cb8\u0cbf\u0cb8\u0ccd\u0c9f\u0cae\u0ccd"),
        qualifiers=("", "\u0ca6\u0caf\u0cb5\u0cbf\u0c9f\u0ccd\u0c9f\u0cc1", "\u0cb8\u0cbf\u0ca6\u0ccd\u0ca7\u0cb5\u0cbf\u0ca6\u0cc6\u0caf\u0cbe", "\u0caa\u0ccd\u0cb0\u0cbe\u0cb0\u0c82\u0cad\u0cbf\u0cb8\u0cbf", "\u0cb8\u0cb9\u0cbe\u0caf"),
        keywords=("\u0ca8\u0cae\u0cb8\u0ccd\u0c95\u0cbe\u0cb0", "\u0cb9\u0cc8", "\u0cb6\u0cc1\u0cad"),
    ),
    IntentCategory(
        key="kannada_fir_queries",
        canonical_intent="fir_lookup",
        response_rule="Return FIR details in Kannada/English evidence-safe format.",
        query_records=True,
        starts=("\u0ca4\u0ccb\u0cb0\u0cbf\u0cb8\u0cbf", "\u0cb9\u0cc1\u0ca1\u0cc1\u0c95\u0cbf", "\u0ca4\u0cb0\u0cbf", "\u0c93\u0caa\u0ca8\u0ccd", "\u0c95\u0cca\u0ca1\u0cbf"),
        subjects=("\u0c8e\u0cab\u0ccd\u0c90\u0c86\u0cb0\u0ccd", "\u0caa\u0ccd\u0cb0\u0c95\u0cb0\u0ca3", "\u0ca6\u0cbe\u0c96\u0cb2\u0cc6", "\u0cab\u0cc8\u0cb2\u0ccd", "\u0cb8\u0c82\u0c96\u0ccd\u0caf\u0cc6"),
        qualifiers=KANNADA_NAMES,
        keywords=("\u0c8e\u0cab\u0ccd\u0c90\u0c86\u0cb0\u0ccd", "\u0caa\u0ccd\u0cb0\u0c95\u0cb0\u0ca3", "\u0cab\u0cc8\u0cb2\u0ccd"),
    ),
    IntentCategory(
        key="kannada_suspect_queries",
        canonical_intent="accused_lookup",
        response_rule="Return suspect/accused record details with FIR evidence.",
        query_records=True,
        starts=("\u0ca4\u0ccb\u0cb0\u0cbf\u0cb8\u0cbf", "\u0cb9\u0cc1\u0ca1\u0cc1\u0c95\u0cbf", "\u0caf\u0cbe\u0cb0\u0cc1", "\u0ca4\u0cbf\u0cb3\u0cbf\u0cb8\u0cbf", "\u0cb5\u0cbf\u0cb5\u0cb0"),
        subjects=("\u0c86\u0cb0\u0ccb\u0caa\u0cbf", "\u0cb6\u0c82\u0c95\u0cbf\u0ca4", "\u0cb5\u0ccd\u0caf\u0c95\u0ccd\u0ca4\u0cbf", "\u0cb9\u0cc6\u0cb8\u0cb0\u0cc1", "\u0caa\u0ccd\u0cb0\u0cca\u0cab\u0cc8\u0cb2\u0ccd"),
        qualifiers=KANNADA_NAMES,
        keywords=("\u0c86\u0cb0\u0ccb\u0caa\u0cbf", "\u0cb6\u0c82\u0c95\u0cbf\u0ca4", "\u0cb9\u0cc6\u0cb8\u0cb0\u0cc1"),
    ),
    IntentCategory(
        key="timeline_requests",
        canonical_intent="decision_support",
        response_rule="Show investigation timeline, status, events, and evidence references.",
        query_records=True,
        starts=("show", "build", "summarize", "generate", "create"),
        subjects=("timeline", "investigation timeline", "case history", "event history", "sequence"),
        qualifiers=EN_CASE_NAMES,
        keywords=("timeline", "history", "sequence", "events"),
    ),
    IntentCategory(
        key="export_requests",
        canonical_intent="conversation_export",
        response_rule="Export only the current authorized conversation/report.",
        query_records=False,
        starts=("export", "download", "save", "generate", "create"),
        subjects=("pdf", "report", "conversation", "case summary", "evidence pack"),
        qualifiers=("", "locally", "for this chat", "for selected case", "as PDF"),
        keywords=("export", "download", "pdf", "save", "report"),
    ),
)


def generate_intent_variations(per_category: int = 50) -> dict[str, list[str]]:
    output: dict[str, list[str]] = {}
    for category in INTENT_CATEGORIES:
        variations: list[str] = []
        for start, subject, qualifier in product(category.starts, category.subjects, category.qualifiers):
            text = " ".join(part for part in [start, subject, qualifier] if part).strip()
            text = re.sub(r"\s+", " ", text)
            if text and text not in variations:
                variations.append(text)
            if len(variations) >= per_category:
                break
        output[category.key] = variations
    return output


def taxonomy_status(per_category: int = 50) -> dict[str, Any]:
    variations = generate_intent_variations(per_category)
    return {
        "category_count": len(variations),
        "per_category_minimum": per_category,
        "total_variations": sum(len(items) for items in variations.values()),
        "categories": {key: len(items) for key, items in variations.items()},
    }


def classify_master_intent(query: str) -> dict[str, Any]:
    text = re.sub(r"\s+", " ", query.casefold()).strip()
    padded = f" {text} "
    best: tuple[int, IntentCategory] | None = None
    for category in INTENT_CATEGORIES:
        score = 0
        for keyword in category.keywords:
            key = keyword.casefold()
            if " " in key and key in text:
                score += 4
            elif re.search(rf"(?<!\w){re.escape(key)}(?!\w)", padded):
                score += 3
        if category.key in {"greeting", "kannada_greetings"} and text in {item.casefold() for item in category.starts}:
            score += 8
        if score and (best is None or score > best[0]):
            best = (score, category)
    if not best:
        return {
            "category": "unknown",
            "intent": "crime_data",
            "query_records": True,
            "response_rule": "Use normal crime-data orchestration.",
            "score": 0,
        }
    score, category = best
    return {
        "category": category.key,
        "intent": category.canonical_intent,
        "query_records": category.query_records,
        "response_rule": category.response_rule,
        "score": score,
    }
