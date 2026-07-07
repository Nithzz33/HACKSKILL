from __future__ import annotations

import re
from dataclasses import dataclass, replace
from difflib import SequenceMatcher
from typing import Any

from secure_crime_api.analytics import SAFEGUARDS
from secure_crime_api.models import AuthenticatedUser
from secure_crime_api.rbac import can_access_case
from secure_crime_api.redaction import mask_case
from secure_crime_api.storage import Database, normalized_search_terms, prefix_hash


NAME_FIELDS = ("suspect_name", "victim_name", "complainant_name")
CASE_TEXT_FIELDS = (
    "case_type",
    "modus_operandi",
    "summary",
    "event_context",
    "district",
    "status",
    "source_record_id",
    "fir_number",
)

STRICT_FILLER_TERMS = {
    "a",
    "about",
    "all",
    "and",
    "any",
    "by",
    "case",
    "cases",
    "complainant",
    "complaint",
    "copy",
    "desc",
    "detail",
    "details",
    "file",
    "files",
    "find",
    "fir",
    "for",
    "from",
    "give",
    "in",
    "is",
    "limit",
    "name",
    "named",
    "no",
    "number",
    "of",
    "only",
    "or",
    "order",
    "person",
    "records",
    "search",
    "show",
    "suspect",
    "suspects",
    "the",
    "top",
    "victim",
    "victims",
    "where",
    "with",
}

SEVERITY_TERMS = {"brutal", "violent", "grave", "grievous", "weapon", "weapons", "deadly"}

CRIME_SYNONYM_GROUPS = {
    "murder": {"murder", "murders", "murdered", "homicide", "kill", "killed", "killing", "death"},
    "homicide": {"murder", "murders", "murdered", "homicide", "kill", "killed", "killing", "death"},
    "kill": {"murder", "murders", "murdered", "homicide", "kill", "killed", "killing", "death"},
    "theft": {"theft", "thefts", "stolen", "steal", "stealing", "larceny"},
    "stolen": {"theft", "thefts", "stolen", "steal", "stealing", "larceny"},
    "fraud": {"fraud", "frauds", "cheating", "scam", "money", "financial"},
    "robbery": {"robbery", "robberies", "robbed"},
    "burglary": {"burglary", "burglaries", "housebreaking"},
    "assault": {"assault", "assaults", "attack", "attacked"},
    "vehicle": {"vehicle", "vehicles", "auto", "car", "cars", "truck", "trucks"},
    "ಕೊಲೆ": {"ಕೊಲೆ", "ಹತ್ಯೆ", "murder", "homicide"},
    "ಹತ್ಯೆ": {"ಕೊಲೆ", "ಹತ್ಯೆ", "murder", "homicide"},
    "ಕಳ್ಳತನ": {"ಕಳ್ಳತನ", "theft", "stolen"},
    "ದರೋಡೆ": {"ದರೋಡೆ", "robbery"},
    "ವಂಚನೆ": {"ವಂಚನೆ", "fraud", "cheating"},
}

COMMON_MISSPELLINGS = {
    "acuse": "accused",
    "accuse": "accused",
    "complaintant": "complainant",
    "complaintent": "complainant",
    "firr": "fir",
    "muder": "murder",
    "mudrer": "murder",
    "murdre": "murder",
    "murdr": "murder",
    "robery": "robbery",
    "thetf": "theft",
    "theift": "theft",
    "thef": "theft",
}

IDENTIFIER_STOP_WORDS = {"case", "file", "fir", "limit", "name", "no", "number", "top"}
IDENTIFIER_RE = re.compile(
    r"\b(?:[a-z]{2,}[a-z0-9]*[-/][a-z0-9][a-z0-9/-]*|[0-9a-f]{8}-[0-9a-f-]{27,})\b",
    re.IGNORECASE,
)
CONTEXT_IDENTIFIER_RE = re.compile(
    r"\b(?:fir|case|file|number)\s*(?:no|number|#|:)\s*([a-z0-9][a-z0-9/-]{2,})\b",
    re.IGNORECASE,
)
STRICT_BLOCKER_TERMS = {"decision", "lead", "leads", "next", "similar", "summarize", "summary", "timeline"}


@dataclass(frozen=True)
class StrictSearchPlan:
    limit: int
    order_desc: bool
    identifiers: tuple[str, ...]
    names: tuple[str, ...]
    name_fields: tuple[str, ...]
    category_terms: tuple[str, ...]
    optional_terms: tuple[str, ...]
    strategy: str
    explicit_limit: bool


def answer_strict_case_search_query(
    *,
    query: str,
    db: Database,
    user: AuthenticatedUser,
    include_sources: bool,
) -> dict[str, Any] | None:
    plan = parse_strict_search_plan(query)
    if plan is None:
        return None

    matches = execute_plan(db, user, plan, corrections={})
    corrections: dict[str, str] = {}
    if not matches:
        corrections = suggest_corrections(db, plan)
        if corrections:
            matches = execute_plan(db, user, plan, corrections=corrections)

    if not matches:
        return {
            "intent": "strict_sql_case_search",
            "answer": no_match_answer(plan, corrections),
            "visible_case_count": 0,
            "sources": [],
            "query_analysis": plan_query_analysis(query, plan, corrections),
            "safeguards": strict_safeguards(),
        }

    limited = matches[: plan.limit]
    masked = [mask_case(case, user.role) for case in limited]
    return {
        "intent": "strict_sql_case_search",
        "answer": result_answer(plan, masked, corrections),
        "visible_case_count": len(masked),
        "sources": case_sources(limited, user.role) if include_sources else [],
        "query_analysis": plan_query_analysis(query, plan, corrections),
        "safeguards": strict_safeguards(),
    }


def parse_strict_search_plan(query: str) -> StrictSearchPlan | None:
    text = query.casefold()
    terms = normalized_search_terms(query)
    if set(terms).intersection(STRICT_BLOCKER_TERMS):
        return None
    limit, explicit_limit = parse_limit(text)
    identifiers = tuple(parse_identifiers(query))
    names = tuple(parse_names(query))
    name_fields = tuple(name_fields_for_query(text))
    order_desc = bool({"desc", "latest", "newest", "recent"}.intersection(terms))
    has_top = "top" in terms

    meaningful = [
        term
        for term in terms
        if term not in STRICT_FILLER_TERMS and not term.isdigit() and not any(term in normalized_search_terms(name) for name in names)
    ]
    category_terms, optional_terms = expand_category_terms(meaningful)

    if identifiers:
        strategy = "identifier_exact"
    elif names:
        strategy = "person_name"
    elif has_top or explicit_limit:
        strategy = "top_case_records"
    else:
        return None

    return StrictSearchPlan(
        limit=limit,
        order_desc=order_desc,
        identifiers=identifiers,
        names=names,
        name_fields=name_fields,
        category_terms=tuple(category_terms),
        optional_terms=tuple(optional_terms),
        strategy=strategy,
        explicit_limit=explicit_limit,
    )


def parse_limit(text: str) -> tuple[int, bool]:
    found: list[int] = []
    for pattern in [r"\btop\s+(\d{1,3})\b", r"\blimit\s+(\d{1,3})\b", r"\bfirst\s+(\d{1,3})\b"]:
        found.extend(int(match) for match in re.findall(pattern, text))
    if not found:
        return 10, False
    return max(1, min(found[-1], 50)), True


def parse_identifiers(query: str) -> list[str]:
    values = [match.group(0) for match in IDENTIFIER_RE.finditer(query)]
    values.extend(match.group(1) for match in CONTEXT_IDENTIFIER_RE.finditer(query))
    output: list[str] = []
    for value in values:
        cleaned = value.strip(" .,:;()[]{}").casefold()
        if not any(char.isdigit() for char in cleaned):
            continue
        if cleaned in IDENTIFIER_STOP_WORDS or len(cleaned) < 3:
            continue
        if cleaned not in output:
            output.append(cleaned)
    return output[:8]


def parse_names(query: str) -> list[str]:
    patterns = [
        r"(?:where\s+)?(?:suspect|victim|complainant|complaint(?:\s+given\s+person)?|person)?\s*name\s*(?:is|=|called|named)\s+(.+)",
        r"(?:where\s+)?(?:suspect|victim|complainant|complaint(?:\s+given\s+person)?)\s*(?:is|=|called|named)\s+(.+)",
    ]
    tail = ""
    for pattern in patterns:
        match = re.search(pattern, query, flags=re.IGNORECASE)
        if match:
            tail = match.group(1)
            break
    if not tail:
        return []
    tail = re.split(
        r"\b(?:limit|top|desc|ascending|order\s+by|case\s+file|file\s+number|fir\s+number|case\s+number|status|district)\b",
        tail,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]
    parts = re.split(r"\s+(?:or|and)\s+|[,;/]", tail, flags=re.IGNORECASE)
    names: list[str] = []
    for part in parts:
        words = [
            word
            for word in re.findall(r"[^\W_]+", part, flags=re.UNICODE)
            if word.casefold() not in STRICT_FILLER_TERMS and not word.isdigit()
        ]
        if words:
            name = " ".join(words).strip()
            if name and name.casefold() not in {item.casefold() for item in names}:
                names.append(name)
    return names[:10]


def name_fields_for_query(text: str) -> list[str]:
    fields: list[str] = []
    if "suspect" in text or "accused" in text:
        fields.append("suspect_name")
    if "victim" in text:
        fields.append("victim_name")
    if "complainant" in text or "complaint" in text:
        fields.append("complainant_name")
    return fields or list(NAME_FIELDS)


def expand_category_terms(terms: list[str]) -> tuple[list[str], list[str]]:
    required: list[str] = []
    optional: list[str] = []
    for term in terms:
        if term in SEVERITY_TERMS:
            optional.append(term)
            continue
        group = CRIME_SYNONYM_GROUPS.get(term)
        if group:
            for item in sorted(group):
                if item not in required:
                    required.append(item)
        elif term not in required:
            required.append(term)
    return required[:16], optional[:6]


def execute_plan(
    db: Database,
    user: AuthenticatedUser,
    plan: StrictSearchPlan,
    *,
    corrections: dict[str, str],
) -> list[dict[str, Any]]:
    if user.role == "policymaker":
        return []
    if plan.identifiers:
        return query_identifiers(db, user, plan)
    if plan.names:
        return query_names(db, user, plan, corrections)
    return query_top_cases(db, user, plan, corrections)


def query_identifiers(db: Database, user: AuthenticatedUser, plan: StrictSearchPlan) -> list[dict[str, Any]]:
    access_sql, access_params = access_clause(user)
    id_clauses: list[str] = []
    params: list[Any] = []
    for identifier in plan.identifiers:
        id_clauses.append("(c.id = ? OR c.fir_number = ? COLLATE NOCASE OR c.source_record_id = ? COLLATE NOCASE)")
        params.extend([identifier, identifier, identifier])
    where_sql = " AND ".join([access_sql, f"({' OR '.join(id_clauses)})"])
    with db.connect() as conn:
        rows = conn.execute(
            f"""
            SELECT c.*
            FROM cases c
            WHERE {where_sql}
            ORDER BY {case_order_sql(plan.order_desc)}
            LIMIT ?
            """,
            (*access_params, *params, plan.limit),
        ).fetchall()
    return [dict(row) for row in rows if can_access_case(user, dict(row))]


def query_names(
    db: Database,
    user: AuthenticatedUser,
    plan: StrictSearchPlan,
    corrections: dict[str, str],
) -> list[dict[str, Any]]:
    scored: dict[str, tuple[int, dict[str, Any]]] = {}
    for name in plan.names:
        terms = corrected_terms(normalized_search_terms(name), corrections)
        if not terms:
            continue
        rows = query_index_terms(
            db,
            user,
            terms=terms,
            fields=plan.name_fields,
            required_count=len(set(terms)),
            limit=max(plan.limit * 12, 50),
            order_desc=plan.order_desc,
        )
        for row in rows:
            score = name_match_score(row, terms, plan.name_fields)
            if score <= 0:
                continue
            previous = scored.get(row["id"])
            if previous is None or score > previous[0]:
                scored[row["id"]] = (score, row)
    ordered = sorted(
        scored.values(),
        key=lambda item: (-item[0], sort_date(item[1]), item[1]["fir_number"]),
        reverse=False,
    )
    return [row for _score, row in ordered[: plan.limit]]


def query_top_cases(
    db: Database,
    user: AuthenticatedUser,
    plan: StrictSearchPlan,
    corrections: dict[str, str],
) -> list[dict[str, Any]]:
    terms = corrected_terms(list(plan.category_terms), corrections)
    if not terms:
        return query_all_cases(db, user, plan)
    rows = query_index_terms(
        db,
        user,
        terms=terms,
        fields=CASE_TEXT_FIELDS,
        required_count=1,
        limit=max(plan.limit * 10, 80),
        order_desc=plan.order_desc,
    )
    optional = corrected_terms(list(plan.optional_terms), corrections)
    if optional:
        rows.sort(key=lambda row: (optional_score(row, optional), row.get("_search_score", 0), sort_date(row)), reverse=True)
    return rows[: plan.limit]


def query_all_cases(db: Database, user: AuthenticatedUser, plan: StrictSearchPlan) -> list[dict[str, Any]]:
    access_sql, access_params = access_clause(user)
    with db.connect() as conn:
        rows = conn.execute(
            f"""
            SELECT c.*
            FROM cases c
            WHERE {access_sql}
            ORDER BY {case_order_sql(plan.order_desc)}
            LIMIT ?
            """,
            (*access_params, plan.limit),
        ).fetchall()
    return [dict(row) for row in rows if can_access_case(user, dict(row))]


def query_index_terms(
    db: Database,
    user: AuthenticatedUser,
    *,
    terms: list[str],
    fields: tuple[str, ...],
    required_count: int,
    limit: int,
    order_desc: bool,
) -> list[dict[str, Any]]:
    unique_terms = list(dict.fromkeys(term for term in terms if term))
    if not unique_terms:
        return []
    hashes = [prefix_hash(term) for term in unique_terms]
    hash_placeholders = ",".join("?" for _ in hashes)
    field_placeholders = ",".join("?" for _ in fields)
    access_sql, access_params = access_clause(user)
    with db.connect() as conn:
        rows = conn.execute(
            f"""
            SELECT c.*, SUM(i.weight) AS search_score, COUNT(DISTINCT i.prefix_hash) AS matched_terms
            FROM case_search_index i
            JOIN cases c ON c.id = i.case_id
            WHERE i.prefix_hash IN ({hash_placeholders})
              AND i.field IN ({field_placeholders})
              AND {access_sql}
            GROUP BY c.id
            HAVING matched_terms >= ?
            ORDER BY search_score DESC, {case_order_sql(order_desc)}
            LIMIT ?
            """,
            (*hashes, *fields, *access_params, max(1, required_count), max(1, min(limit, 1000))),
        ).fetchall()
    output = []
    for row in rows:
        item = dict(row)
        item["_search_score"] = int(item.pop("search_score") or 0)
        if can_access_case(user, item):
            output.append(item)
    return output


def access_clause(user: AuthenticatedUser) -> tuple[str, tuple[Any, ...]]:
    clauses = ["1 = 1"]
    params: list[Any] = []
    if user.role not in {"super_admin", "supervisor"}:
        clauses.append("c.district = ?")
        params.append(user.district)
    if user.role in {"analyst", "viewer"}:
        clauses.append("c.sensitivity = 'standard'")
    return " AND ".join(clauses), tuple(params)


def case_order_sql(desc: bool) -> str:
    direction = "DESC" if desc else "ASC"
    if desc:
        return "COALESCE(c.incident_at, c.updated_at, c.created_at) DESC, c.fir_number DESC"
    return f"COALESCE(c.incident_at, c.updated_at, c.created_at) {direction}, c.fir_number ASC"


def sort_date(case: dict[str, Any]) -> str:
    return str(case.get("incident_at") or case.get("updated_at") or case.get("created_at") or "")


def name_match_score(case: dict[str, Any], terms: list[str], fields: tuple[str, ...]) -> int:
    best = 0
    phrase = " ".join(terms).casefold()
    for field in fields:
        value = str(case.get(field) or "").strip()
        field_terms = normalized_search_terms(value)
        field_text = " ".join(field_terms)
        if field_text == phrase:
            best = max(best, 120)
        if all(term in field_terms for term in terms):
            best = max(best, 90 + len(terms))
        if all(any(token.startswith(term) or term.startswith(token) for token in field_terms) for term in terms):
            best = max(best, 70 + len(terms))
        if any(term in field_terms for term in terms):
            best = max(best, 35)
    return best


def optional_score(case: dict[str, Any], terms: list[str]) -> int:
    haystack = " ".join(str(case.get(field) or "") for field in CASE_TEXT_FIELDS).casefold()
    return sum(1 for term in terms if term.casefold() in haystack)


def corrected_terms(terms: list[str], corrections: dict[str, str]) -> list[str]:
    return [corrections.get(term, term) for term in terms]


def suggest_corrections(db: Database, plan: StrictSearchPlan) -> dict[str, str]:
    candidates: list[str] = []
    for name in plan.names:
        candidates.extend(normalized_search_terms(name))
    candidates.extend(plan.category_terms)
    candidates.extend(plan.optional_terms)
    corrections: dict[str, str] = {}
    for term in dict.fromkeys(candidates):
        if term in STRICT_FILLER_TERMS or len(term) < 3:
            continue
        correction = COMMON_MISSPELLINGS.get(term) or best_local_term(db, term)
        if correction and correction != term:
            corrections[term] = correction
    return corrections


def best_local_term(db: Database, term: str) -> str | None:
    known_terms = set(CRIME_SYNONYM_GROUPS)
    known_terms.update(COMMON_MISSPELLINGS.values())
    local_vocab = db.case_search_vocabulary(
        first_char=term[:1],
        min_length=max(2, len(term) - 2),
        max_length=len(term) + 2,
        limit=5000,
    )
    pool = list(known_terms) + local_vocab
    best_score = 0.0
    best = None
    for candidate in pool:
        score = SequenceMatcher(None, term, candidate).ratio()
        if score > best_score:
            best_score = score
            best = candidate
    return best if best and best_score >= 0.78 else None


def result_answer(plan: StrictSearchPlan, cases: list[dict[str, Any]], corrections: dict[str, str]) -> str:
    correction_text = correction_sentence(corrections)
    header = (
        f"Case files selected by {strategy_label(plan)}"
        f" with requested limit {plan.limit}."
    )
    lines = [header + (f" {correction_text}" if correction_text else "")]
    for index, case in enumerate(cases, 1):
        case_no = case.get("source_record_id") or case.get("id")
        people = "; ".join(
            item
            for item in [
                f"suspect {case.get('suspect_name')}" if case.get("suspect_name") else "",
                f"victim {case.get('victim_name')}" if case.get("victim_name") else "",
                f"complainant {case.get('complainant_name')}" if case.get("complainant_name") else "",
            ]
            if item
        )
        case_type = case.get("case_type") or "case type not recorded"
        lines.append(
            f"{index}. FIR {case['fir_number']} | Case no {case_no} | {case['district']} | "
            f"{case['status']} | {case_type} | {people}."
        )
    return "\n".join(lines)


def no_match_answer(plan: StrictSearchPlan, corrections: dict[str, str]) -> str:
    correction_text = correction_sentence(corrections)
    target = strategy_label(plan)
    return (
        f"I could not find an accessible case file for {target}. "
        f"{correction_text + ' ' if correction_text else ''}"
        "Try the exact FIR/case number, a full or partial suspect/victim/complainant name, or a crime type such as theft, murder, fraud, robbery, burglary, or assault."
    )


def strategy_label(plan: StrictSearchPlan) -> str:
    if plan.strategy == "identifier_exact":
        return "exact FIR/case-number SQL search"
    if plan.strategy == "person_name":
        fields = ", ".join(field.replace("_", " ") for field in plan.name_fields)
        names = ", ".join(plan.names)
        return f"name SQL search for {names} in {fields}"
    if plan.category_terms:
        return f"top-N SQL search for {', '.join(plan.category_terms[:5])}"
    return "top-N SQL search across accessible cases"


def correction_sentence(corrections: dict[str, str]) -> str:
    if not corrections:
        return ""
    rendered = ", ".join(f"'{source}' as '{target}'" for source, target in corrections.items())
    return f"I corrected spelling using the local case vocabulary: {rendered}."


def case_sources(cases: list[dict[str, Any]], role: str) -> list[dict[str, Any]]:
    sources = []
    for case in cases:
        masked = mask_case(case, role)
        excerpt_parts = [
            str(masked.get("summary") or "")[:180],
            f"Suspect: {masked.get('suspect_name')}" if masked.get("suspect_name") else "",
            f"Victim: {masked.get('victim_name')}" if masked.get("victim_name") else "",
            f"Complainant: {masked.get('complainant_name')}" if masked.get("complainant_name") else "",
        ]
        sources.append(
            {
                "case_id": masked["id"],
                "fir_number": masked["fir_number"],
                "district": masked["district"],
                "status": masked["status"],
                "sensitivity": masked["sensitivity"],
                "excerpt": " | ".join(part for part in excerpt_parts if part),
            }
        )
    return sources


def plan_query_analysis(query: str, plan: StrictSearchPlan, corrections: dict[str, str]) -> dict[str, Any]:
    filters: dict[str, Any] = {
        "sql_strategy": plan.strategy,
        "limit": plan.limit,
        "order": "descending" if plan.order_desc else "ranked",
    }
    if plan.identifiers:
        filters["identifiers"] = list(plan.identifiers)
    if plan.names:
        filters["names"] = list(plan.names)
        filters["name_fields"] = list(plan.name_fields)
    if plan.category_terms:
        filters["category_terms"] = list(plan.category_terms)
    if plan.optional_terms:
        filters["ranking_terms"] = list(plan.optional_terms)
    if corrections:
        filters["spelling_corrections"] = corrections
    return {
        "original_query": query,
        "normalized_query": " ".join(normalized_search_terms(query)),
        "interpreted_terms": [
            term
            for term in normalized_search_terms(query)
            if term not in STRICT_FILLER_TERMS and not term.isdigit()
        ][:12],
        "interpreted_filters": filters,
        "evidence_mode": "indexed_sql_case_search",
        "data_scope": "crime_data_only",
    }


def strict_safeguards() -> list[str]:
    return SAFEGUARDS + [
        "Strict search uses indexed FIR/case identifiers, person-name fields, and crime-type terms before fuzzy correction.",
        "Spelling correction is limited to terms already present in local crime records or approved crime terminology.",
    ]
