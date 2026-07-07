"""Generate and upload a synthetic KSP FIR corpus from the master FIR schema.

This utility treats the supplied KSP FIR copy as the master layout reference,
creates 100 schema-matched FIR copies, and uploads them to the local web app.

The generated records are explicitly marked as synthetic/template records.
They are intended to train and verify the chatbot search/indexing pipeline,
not to represent real Karnataka State Police records.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import re
import sys
import textwrap
import zipfile
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from html import escape as xml_escape
from pathlib import Path
from typing import Iterable


TEMPLATE_VERSION = "ksp-master-fir-copy-v1"
SOURCE_SYSTEM = "synthetic_master_ksp_fir_template"


DISTRICTS = [
    ("Bengaluru Urban", "Bengaluru South Police Station", 12.9716, 77.5946),
    ("Bengaluru Rural", "Chennarayapatana PS", 13.2257, 77.5750),
    ("Mysuru", "Mysuru South Police Station", 12.2958, 76.6394),
    ("Mandya", "Mandya Town PS", 12.5218, 76.8951),
    ("Tumakuru", "Tumakuru Town PS", 13.3379, 77.1173),
    ("Hassan", "Hassan Extension PS", 13.0033, 76.1004),
    ("Shivamogga", "Shivamogga Rural PS", 13.9299, 75.5681),
    ("Dharwad", "Hubballi Suburban PS", 15.3647, 75.1240),
    ("Belagavi", "Belagavi Market PS", 15.8497, 74.4977),
    ("Kalaburagi", "Kalaburagi Rural PS", 17.3297, 76.8343),
    ("Vijayapura", "Vijayapura Gandhi Chowk PS", 16.8302, 75.7100),
    ("Ballari", "Ballari Rural PS", 15.1394, 76.9214),
    ("Udupi", "Udupi Town PS", 13.3409, 74.7421),
    ("Dakshina Kannada", "Mangaluru South PS", 12.9141, 74.8560),
    ("Kolar", "Kolar Town PS", 13.1367, 78.1291),
    ("Chikkamagaluru", "Chikkamagaluru Town PS", 13.3161, 75.7720),
]


CASE_TYPES = [
    ("Financial Fraud", "BNS 318(4), IT Act 66D", "wallet mule account and layered bank transfer"),
    ("Cyber Fraud", "BNS 318(4), IT Act 66C/66D", "phishing link and SIM swap"),
    ("Vehicle Theft", "BNS 303(2)", "night parking area vehicle theft"),
    ("Burglary", "BNS 331(4), 305", "house breaking by duplicate key"),
    ("Assault", "BNS 115(2), 118(1), 352", "group assault after local dispute"),
    ("Robbery", "BNS 309(4)", "two-wheeler chain snatching"),
    ("Narcotics", "NDPS Act 20(b), 22", "inter-district courier route"),
    ("Extortion", "BNS 308(2)", "threat call demanding payment"),
    ("Homicide", "BNS 103(1)", "weapon assault during late-night quarrel"),
    ("Missing Person", "Karnataka Police Manual", "missing adult with last phone tower evidence"),
]


FIRST_NAMES = [
    "Ravi",
    "Mahesh",
    "Akash",
    "Anita",
    "Lakshmi",
    "Suresh",
    "Kiran",
    "Deepak",
    "Prakash",
    "Manjunath",
    "Naveen",
    "Shwetha",
    "Pooja",
    "Arun",
    "Vijay",
    "Sunil",
    "Ramesh",
    "Ganesh",
    "Santosh",
    "Kavitha",
]

LAST_NAMES = [
    "Kumar",
    "Shetty",
    "Gowda",
    "Rao",
    "Naik",
    "Patil",
    "Sharma",
    "Hegde",
    "Murthy",
    "Poojary",
    "Reddy",
    "Kulkarni",
]


MASTER_SCHEMA_FIELDS = [
    {"section": "heading", "label": "FIRST INFORMATION REPORT", "page": 1, "required": True},
    {"section": "heading", "label": "KARNATAKA STATE POLICE", "page": 1, "required": True},
    {"section": "1", "label": "District", "key": "district", "page": 1, "required": True},
    {"section": "1", "label": "Crime No", "key": "crime_no", "page": 1, "required": True},
    {"section": "1", "label": "FIR Date", "key": "fir_date", "page": 1, "required": True},
    {"section": "1", "label": "Circle/Sub Division", "key": "circle_subdivision", "page": 1, "required": True},
    {"section": "1", "label": "PS", "key": "police_station", "page": 1, "required": True},
    {"section": "1", "label": "Act & Section", "key": "act_section", "page": 1, "required": True},
    {"section": "2", "label": "Information received at the PS", "key": "information_received_at", "page": 1, "required": True},
    {"section": "2", "label": "Written/Oral", "key": "information_mode", "page": 1, "required": True},
    {"section": "3", "label": "Occurrence of Offence Day", "key": "occurrence_day", "page": 1, "required": True},
    {"section": "3", "label": "From Date", "key": "occurrence_from_date", "page": 1, "required": True},
    {"section": "3", "label": "To Date", "key": "occurrence_to_date", "page": 1, "required": True},
    {"section": "3", "label": "General Diary reference", "key": "general_diary_reference", "page": 1, "required": True},
    {"section": "4", "label": "Place of occurence with full address", "key": "place_of_occurrence", "page": 1, "required": True},
    {"section": "4", "label": "Distance from PS", "key": "distance_from_ps", "page": 1, "required": True},
    {"section": "4", "label": "Village", "key": "village", "page": 1, "required": True},
    {"section": "5", "label": "Complainant/Informant", "key": "complainant_name", "page": 1, "required": True},
    {"section": "5", "label": "Father's/Husband's Name", "key": "complainant_guardian", "page": 2, "required": False},
    {"section": "5", "label": "Email", "key": "complainant_email", "page": 2, "required": False},
    {"section": "5", "label": "Phone", "key": "complainant_phone", "page": 2, "required": False},
    {"section": "5", "label": "Nationality", "key": "complainant_nationality", "page": 2, "required": False},
    {"section": "5", "label": "Sex", "key": "complainant_gender", "page": 2, "required": False},
    {"section": "5", "label": "Address", "key": "complainant_address", "page": 2, "required": True},
    {"section": "6", "label": "Details of known/suspected/unknown accused", "key": "accused", "page": 2, "required": True},
    {"section": "7", "label": "Reasons for delay in reporting by the complainant/informant", "key": "delay_reason", "page": 2, "required": False},
    {"section": "8", "label": "Particulars of properties stolen/involved", "key": "property_details", "page": 3, "required": False},
    {"section": "9", "label": "Total value of property stolen/involved", "key": "property_value", "page": 3, "required": False},
    {"section": "10", "label": "F.I.R Contents", "key": "fir_contents", "page": 3, "required": True},
    {"section": "11", "label": "Action Taken", "key": "action_taken", "page": 4, "required": True},
    {"section": "11", "label": "Investigating Officer", "key": "investigating_officer", "page": 4, "required": True},
]


@dataclass
class FirRecord:
    index: int
    fir_number: str
    crime_no: str
    year: int
    district: str
    police_station: str
    circle_subdivision: str
    fir_date: str
    incident_at: str
    status: str
    case_type: str
    act_section: str
    modus_operandi: str
    complainant_name: str
    complainant_phone: str
    complainant_address: str
    victim_name: str
    victim_age: int
    victim_gender: str
    suspect_name: str
    suspect_age: int
    suspect_gender: str
    accused_names: list[str]
    place_of_occurrence: str
    latitude: float
    longitude: float
    summary: str
    investigation_note: str
    source_record_id: str


def clean_filename(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-")


def person_name(i: int, offset: int = 0) -> str:
    first = FIRST_NAMES[(i + offset) % len(FIRST_NAMES)]
    last = LAST_NAMES[(i * 3 + offset) % len(LAST_NAMES)]
    return f"{first} {last}"


def generate_records(count: int) -> list[FirRecord]:
    random.seed(20260610)
    start_date = datetime(2026, 1, 3, 9, 30)
    records: list[FirRecord] = []
    statuses = ["open", "under_review", "closed"]
    genders = ["Male", "Female"]
    for i in range(1, count + 1):
        district, station, base_lat, base_lon = DISTRICTS[(i - 1) % len(DISTRICTS)]
        case_type, act_section, mo = CASE_TYPES[(i - 1) % len(CASE_TYPES)]
        incident_time = start_date + timedelta(days=i * 2, hours=i % 9, minutes=(i * 7) % 50)
        fir_time = incident_time + timedelta(hours=2 + (i % 5))
        suspect = "Ravi Kumar" if i in {1, 17, 42, 73} else person_name(i, 2)
        victim = person_name(i, 6)
        complainant = person_name(i, 10)
        accused = [suspect, person_name(i, 4), person_name(i, 8)]
        lat = round(base_lat + random.uniform(-0.18, 0.18), 6)
        lon = round(base_lon + random.uniform(-0.18, 0.18), 6)
        fir_number = f"KSP-FIR-2026-{i:04d}"
        status = statuses[i % len(statuses)]
        summary = (
            f"Synthetic KSP FIR template training record generated from the master schema. "
            f"{case_type} reported at {station}, {district}. Suspect {suspect}; "
            f"complainant {complainant}; victim {victim}; MO: {mo}. "
            f"Use as demo/template data only."
        )
        records.append(
            FirRecord(
                index=i,
                fir_number=fir_number,
                crime_no=f"{i:04d}/2026",
                year=2026,
                district=district,
                police_station=station,
                circle_subdivision=f"{district} Sub Division",
                fir_date=fir_time.strftime("%d/%m/%Y"),
                incident_at=incident_time.isoformat(),
                status=status,
                case_type=case_type,
                act_section=act_section,
                modus_operandi=mo,
                complainant_name=complainant,
                complainant_phone=f"9{random.randint(100000000, 999999999)}",
                complainant_address=f"House {100 + i}, Ward {1 + i % 20}, {district}, Karnataka",
                victim_name=victim,
                victim_age=18 + (i * 3) % 55,
                victim_gender=genders[(i + 1) % 2],
                suspect_name=suspect,
                suspect_age=19 + (i * 5) % 50,
                suspect_gender=genders[i % 2],
                accused_names=accused,
                place_of_occurrence=f"Near Ward {1 + i % 20} market road, {district}, Karnataka",
                latitude=lat,
                longitude=lon,
                summary=summary,
                investigation_note=(
                    "Generated by Python automation from the KSP FIR master schema; "
                    "verify against original evidence before operational use."
                ),
                source_record_id=f"{SOURCE_SYSTEM}:{fir_number}",
            )
        )
    return records


def master_schema_payload(master_pdf: Path | None) -> dict:
    payload = {
        "template_version": TEMPLATE_VERSION,
        "source_pdf": str(master_pdf) if master_pdf else None,
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "warning": "Synthetic corpus schema only; generated cases are not real police records.",
        "fields": MASTER_SCHEMA_FIELDS,
        "pages": [],
    }
    if not master_pdf or not master_pdf.exists():
        return payload

    try:
        import fitz  # type: ignore
    except Exception as exc:  # pragma: no cover - depends on local runtime
        payload["pdf_lookup_status"] = f"PyMuPDF unavailable: {exc}"
        return payload

    document = fitz.open(str(master_pdf))
    payload["page_count"] = document.page_count
    for page_index, page in enumerate(document, start=1):
        text = page.get_text("text")
        blocks = []
        for block in page.get_text("blocks"):
            x0, y0, x1, y1, block_text, *_ = block
            cleaned = " ".join(str(block_text).split())
            if cleaned:
                blocks.append(
                    {
                        "bbox": [round(x0, 2), round(y0, 2), round(x1, 2), round(y1, 2)],
                        "text": cleaned[:500],
                    }
                )
        payload["pages"].append(
            {
                "page": page_index,
                "width": round(page.rect.width, 2),
                "height": round(page.rect.height, 2),
                "text_sha256": hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest(),
                "text_preview": text[:1200],
                "blocks": blocks[:80],
            }
        )
    return payload


def write_master_lookup(output_dir: Path, master_pdf: Path | None) -> None:
    schema_dir = output_dir / "master_schema"
    schema_dir.mkdir(parents=True, exist_ok=True)
    payload = master_schema_payload(master_pdf)
    (schema_dir / "ksp_master_fir_schema.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    lines = [
        "KSP MASTER FIR TEMPLATE LOOKUP",
        f"Template version: {TEMPLATE_VERSION}",
        f"Source PDF: {payload.get('source_pdf')}",
        "",
        "Strict metadata fields:",
    ]
    for field in MASTER_SCHEMA_FIELDS:
        req = "required" if field.get("required") else "optional"
        key = field.get("key", "-")
        lines.append(f"- Page {field.get('page')}: Section {field.get('section')} / {field['label']} / {key} / {req}")
    if payload.get("pages"):
        lines.extend(["", "PDF page lookup:"])
        for page in payload["pages"]:
            lines.append(
                f"- Page {page['page']}: {page['width']}x{page['height']}, "
                f"text hash {page['text_sha256'][:16]}, blocks {len(page['blocks'])}"
            )
    (schema_dir / "ksp_master_fir_lookup.txt").write_text("\n".join(lines), encoding="utf-8")


def wrap(value: str, width: int = 92) -> list[str]:
    return textwrap.wrap(value, width=width, replace_whitespace=False) or [""]


def fir_pages(record: FirRecord) -> list[list[str]]:
    received = datetime.fromisoformat(record.incident_at) + timedelta(hours=2)
    occurrence_day = datetime.fromisoformat(record.incident_at).strftime("%A")
    accused_lines = []
    for idx, accused in enumerate(record.accused_names, start=1):
        accused_lines.append(
            f"{idx} Accused Adult {record.suspect_gender} {accused}(A{idx}) / Father Unknown / "
            f"General / {record.district}, Karnataka / Occupation Unknown / Suspect"
        )

    page1 = [
        "FIRST INFORMATION REPORT",
        "KARNATAKA STATE POLICE",
        "Before the Honourable Jurisdictional Court",
        "(Under Section 173 Bharatiya Nagarik Suraksha Sanhita)",
        "1.",
        f"District : {record.district}",
        f"Crime No : {record.crime_no}",
        f"FIR Date : {record.fir_date}",
        f"Circle/Sub Division : {record.circle_subdivision}",
        f"PS : {record.police_station}",
        f"Act & Section : {record.act_section}",
        "2.(b) Information received at the PS : " + received.strftime("%d/%m/%Y %H:%M:%S"),
        "Written/Oral : Written",
        "From Time : " + datetime.fromisoformat(record.incident_at).strftime("%H:%M:%S"),
        "To Time : " + (datetime.fromisoformat(record.incident_at) + timedelta(minutes=40)).strftime("%H:%M:%S"),
        "From Date : " + datetime.fromisoformat(record.incident_at).strftime("%d/%m/%Y"),
        "To Date : " + datetime.fromisoformat(record.incident_at).strftime("%d/%m/%Y"),
        f"3.(a) Occurence of Offence Day : {occurrence_day}",
        "(c) Reasons for Delay in reporting by the Complainant / Informant : no",
        "(d) General Diary reference Entry No. & Time : 1 , " + received.strftime("%H:%M:%S"),
        "4.(a) Place of occurence with full address",
        record.place_of_occurrence,
        "(b) Distance from PS : 5km towards city limits",
        f"(c) Village : Ward {1 + record.index % 20}",
        "Beat Name : Beat-05",
        f"District : {record.district}",
        "5.Complainant/Informant :",
        record.complainant_name,
        "Father's/Husband's Name : Not recorded",
    ]
    page2 = [
        "(g) Email : not-recorded@example.invalid",
        f"(h) Phone : {record.complainant_phone}",
        "(i) Nationality : Indian",
        f"(j) Sex : {'Male' if record.index % 2 else 'Female'}",
        f"(k) Address : {record.complainant_address}",
        "6.Details of known/suspected/unknown accused with full particulars",
        "AgeSexPerson TypeName / Father Name / Caste / AddressOccupationTypeSl.No.",
        *accused_lines,
        "7.Reasons for delay in reporting by the complainant/informant",
        "No delay stated in the generated template record.",
    ]
    page3 = [
        "8.Particulars of properties stolen/involved",
        "Sl.No.Property TypeEstimated ValueDescription",
        f"1 Evidence related to {record.case_type} 0 Stored as digital/template evidence",
        "9.Total value of property stolen/involved : 0",
        "10.F.I.R Contents (attach separate sheet, if required)",
        *wrap(record.summary, 88),
        *wrap(
            f"Victim: {record.victim_name}; Suspect: {record.suspect_name}; "
            f"Complainant: {record.complainant_name}; Modus Operandi: {record.modus_operandi}.",
            88,
        ),
    ]
    page4 = [
        "11.(a) Action Taken :",
        f"Registered FIR {record.fir_number}, assigned investigation, and marked status as {record.status}.",
        "(c) If the Police Officer does not proceed to the spot for investigation the reasons there of should be mentioned :",
        "Investigation proceeds as per law and generated verification workflow.",
        "(b) Investigation Officer Details",
        "Investigating Officer : Inspector KSP Template Verification",
        "Rank : Police Inspector",
        "Police Station : " + record.police_station,
        "Signature of Officer in charge, Police Station",
        f"Source Record ID : {record.source_record_id}",
        "Template warning : synthetic FIR generated for chatbot and search verification only.",
    ]
    return [page1, page2, page3, page4]


def write_docx(path: Path, pages: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    paragraphs = []
    for page_no, page in enumerate(pages, start=1):
        if page_no > 1:
            paragraphs.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
        for line in page:
            paragraphs.append(
                '<w:p><w:r><w:t xml:space="preserve">'
                + xml_escape(line)
                + "</w:t></w:r></w:p>"
            )
    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        "<w:body>"
        + "".join(paragraphs)
        + "<w:sectPr><w:pgSz w:w=\"12240\" w:h=\"15840\"/><w:pgMar w:top=\"720\" w:right=\"720\" "
        'w:bottom="720" w:left="720"/></w:sectPr></w:body></w:document>'
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        "</Types>"
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="word/document.xml"/>'
        "</Relationships>"
    )
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("word/document.xml", document_xml)


def pdf_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def page_content(lines: list[str]) -> bytes:
    commands = ["BT", "/F1 9 Tf", "14 TL"]
    y = 760
    for line in lines[:58]:
        safe = pdf_escape(line[:112])
        commands.append(f"1 0 0 1 36 {y} Tm ({safe}) Tj")
        y -= 13
    commands.append("ET")
    return "\n".join(commands).encode("latin-1", errors="replace")


def write_pdf(path: Path, pages: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    objects: list[bytes] = []

    def add_object(payload: bytes) -> int:
        objects.append(payload)
        return len(objects)

    catalog_id = add_object(b"<< /Type /Catalog /Pages 2 0 R >>")
    pages_id = add_object(b"PLACEHOLDER")
    font_id = add_object(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    page_ids = []
    for page_lines in pages:
        content = page_content(page_lines)
        content_id = add_object(
            b"<< /Length " + str(len(content)).encode("ascii") + b" >>\nstream\n" + content + b"\nendstream"
        )
        page_id = add_object(
            (
                f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 612 792] "
                f"/Resources << /Font << /F1 {font_id} 0 R >> >> /Contents {content_id} 0 R >>"
            ).encode("ascii")
        )
        page_ids.append(page_id)
    objects[pages_id - 1] = (
        f"<< /Type /Pages /Kids [{' '.join(str(page_id) + ' 0 R' for page_id in page_ids)}] "
        f"/Count {len(page_ids)} >>"
    ).encode("ascii")
    assert catalog_id == 1

    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for obj_id, payload in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{obj_id} 0 obj\n".encode("ascii"))
        output.extend(payload)
        output.extend(b"\nendobj\n")
    xref = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n"
        ).encode("ascii")
    )
    path.write_bytes(bytes(output))


def write_case_sheet(path: Path, records: list[FirRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "fir_number",
        "year",
        "district",
        "status",
        "case_type",
        "modus_operandi",
        "incident_at",
        "complainant_name",
        "complainant_phone",
        "victim_name",
        "victim_age",
        "victim_gender",
        "suspect_name",
        "suspect_age",
        "suspect_gender",
        "summary",
        "sensitivity",
        "latitude",
        "longitude",
        "socio_context",
        "urbanization_context",
        "migration_context",
        "education_context",
        "event_context",
        "source_system",
        "source_record_id",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            row = {
                "fir_number": record.fir_number,
                "year": record.year,
                "district": record.district,
                "status": record.status,
                "case_type": record.case_type,
                "modus_operandi": record.modus_operandi,
                "incident_at": record.incident_at,
                "complainant_name": record.complainant_name,
                "complainant_phone": record.complainant_phone,
                "victim_name": record.victim_name,
                "victim_age": record.victim_age,
                "victim_gender": record.victim_gender,
                "suspect_name": record.suspect_name,
                "suspect_age": record.suspect_age,
                "suspect_gender": record.suspect_gender,
                "summary": record.summary,
                "sensitivity": "standard",
                "latitude": record.latitude,
                "longitude": record.longitude,
                "socio_context": "template training record; verify before operational use",
                "urbanization_context": "district-level synthetic urban/rural context",
                "migration_context": "not verified",
                "education_context": "not verified",
                "event_context": "template corpus generation",
                "source_system": SOURCE_SYSTEM,
                "source_record_id": record.source_record_id,
            }
            writer.writerow(row)


def generate_corpus(output_dir: Path, master_pdf: Path | None, count: int) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_master_lookup(output_dir, master_pdf)
    records = generate_records(count)
    docs_dir = output_dir / "fir_docs"
    pdf_dir = output_dir / "fir_pdfs"
    for record in records:
        pages = fir_pages(record)
        base_name = clean_filename(record.fir_number)
        write_docx(docs_dir / f"{base_name}.docx", pages)
        write_pdf(pdf_dir / f"{base_name}.pdf", pages)
    write_case_sheet(output_dir / "ksp_generated_case_sheet.csv", records)
    manifest = {
        "template_version": TEMPLATE_VERSION,
        "source_system": SOURCE_SYSTEM,
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "record_count": len(records),
        "case_sheet": str(output_dir / "ksp_generated_case_sheet.csv"),
        "fir_docx_dir": str(docs_dir),
        "fir_pdf_dir": str(pdf_dir),
        "records": [asdict(record) for record in records],
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def api_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def login(client, username: str, password: str) -> str:
    response = client.post("/auth/login", json={"username": username, "password": password})
    response.raise_for_status()
    data = response.json()
    return data["access_token"]


def fetch_case_map(client, token: str) -> dict[str, str]:
    case_map: dict[str, str] = {}
    response = client.get("/cases", headers=api_headers(token))
    response.raise_for_status()
    payload = response.json()
    cases = payload if isinstance(payload, list) else payload.get("items", [])
    for case in cases:
        fir_number = case.get("fir_number")
        if fir_number:
            case_map[str(fir_number)] = str(case.get("id"))
    return case_map


def upload_file(client, token: str, file_path: Path, upload_type: str, case_id: str | None, auto_import: bool) -> dict:
    mime = "application/pdf" if file_path.suffix.lower() == ".pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    if file_path.suffix.lower() == ".csv":
        mime = "text/csv"
    data = {
        "upload_type": upload_type,
        "source_system": SOURCE_SYSTEM,
        "auto_import": "true" if auto_import else "false",
    }
    if case_id:
        data["case_id"] = case_id
    with file_path.open("rb") as handle:
        response = client.post(
            "/files/upload",
            headers=api_headers(token),
            data=data,
            files={"file": (file_path.name, handle, mime)},
            timeout=60,
        )
    response.raise_for_status()
    return response.json()


def upload_exists(client, token: str, filename: str) -> bool:
    response = client.get(
        "/files/uploads",
        headers=api_headers(token),
        params={"q": filename, "limit": 20},
    )
    response.raise_for_status()
    payload = response.json()
    items = payload if isinstance(payload, list) else payload.get("items", [])
    return any(item.get("original_filename") == filename for item in items)


def upload_corpus(
    output_dir: Path,
    base_url: str,
    username: str,
    password: str,
    upload_format: str,
    skip_existing: bool,
) -> dict:
    try:
        import httpx
    except Exception as exc:  # pragma: no cover - local env dependent
        raise RuntimeError("httpx is required for upload. Install project requirements first.") from exc

    manifest_path = output_dir / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing manifest: {manifest_path}")

    with httpx.Client(base_url=base_url.rstrip("/"), timeout=60) as client:
        token = login(client, username, password)

        case_sheet = output_dir / "ksp_generated_case_sheet.csv"
        case_sheet_result = upload_file(client, token, case_sheet, "case_sheet", None, auto_import=True)
        case_map = fetch_case_map(client, token)

        folder = output_dir / ("fir_pdfs" if upload_format == "pdf" else "fir_docs")
        suffix = ".pdf" if upload_format == "pdf" else ".docx"
        uploaded = []
        skipped = []
        for file_path in sorted(folder.glob(f"*{suffix}")):
            if skip_existing and upload_exists(client, token, file_path.name):
                skipped.append(file_path.name)
                continue
            fir_number = file_path.stem
            result = upload_file(
                client,
                token,
                file_path,
                "fir_copy",
                case_map.get(fir_number),
                auto_import=False,
            )
            uploaded.append({"file": file_path.name, "upload_id": result.get("upload_id"), "case_id": case_map.get(fir_number)})

        verification = client.post(
            "/intelligence/query",
            headers=api_headers(token),
            json={
                "query": "show FIR KSP-FIR-2026-0001 and complainant Ravi Kumar related records",
                "language": "en",
                "conversation_id": "ksp-corpus-verification",
                "include_sources": True,
            },
            timeout=60,
        )
        verification.raise_for_status()
        verification_payload = verification.json()
        return {
            "case_sheet_upload": case_sheet_result,
            "case_count_after_import": len(case_map),
            "uploaded_files": len(uploaded),
            "skipped_files": len(skipped),
            "uploaded_sample": uploaded[:5],
            "skipped_sample": skipped[:5],
            "verification_answer": verification_payload.get("answer", "")[:1200],
            "verification_sources": verification_payload.get("sources", [])[:10],
        }


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate/upload synthetic KSP FIR corpus.")
    sub = parser.add_subparsers(dest="command", required=True)

    generate = sub.add_parser("generate", help="Generate master lookup, case sheet, DOCX, and PDF files.")
    generate.add_argument("--master-pdf", type=Path, default=None)
    generate.add_argument("--output", type=Path, default=Path("outputs/ksp_fir_corpus"))
    generate.add_argument("--count", type=int, default=100)

    upload = sub.add_parser("upload", help="Upload generated corpus to the local web application.")
    upload.add_argument("--output", type=Path, default=Path("outputs/ksp_fir_corpus"))
    upload.add_argument("--base-url", default="http://127.0.0.1:8000")
    upload.add_argument("--username", default="supervisor")
    upload.add_argument("--password", default="ChangeMe!12345")
    upload.add_argument("--format", choices=["pdf", "docx"], default="pdf")
    upload.add_argument("--skip-existing", action="store_true")

    both = sub.add_parser("all", help="Generate and upload in one command.")
    both.add_argument("--master-pdf", type=Path, default=None)
    both.add_argument("--output", type=Path, default=Path("outputs/ksp_fir_corpus"))
    both.add_argument("--count", type=int, default=100)
    both.add_argument("--base-url", default="http://127.0.0.1:8000")
    both.add_argument("--username", default="supervisor")
    both.add_argument("--password", default="ChangeMe!12345")
    both.add_argument("--format", choices=["pdf", "docx"], default="pdf")
    both.add_argument("--skip-existing", action="store_true")

    return parser.parse_args(list(argv))


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.command in {"generate", "all"}:
        manifest = generate_corpus(args.output, args.master_pdf, args.count)
        print(json.dumps({"generated": manifest["record_count"], "output": str(args.output)}, indent=2))
    if args.command in {"upload", "all"}:
        result = upload_corpus(
            args.output,
            args.base_url,
            args.username,
            args.password,
            args.format,
            args.skip_existing,
        )
        print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
