from __future__ import annotations

import textwrap
from datetime import datetime, timezone


def render_conversation_pdf(title: str, messages: list[dict]) -> bytes:
    lines = [
        title,
        f"Exported: {datetime.now(timezone.utc).isoformat()}",
        "",
    ]
    for message in messages:
        prefix = message["role"].upper()
        created_at = message["created_at"]
        lines.append(f"{prefix} {created_at}")
        lines.extend(textwrap.wrap(message["content"], width=92) or [""])
        lines.append("")

    pages = [lines[i : i + 46] for i in range(0, len(lines), 46)] or [[]]
    objects: list[str] = []
    page_object_ids: list[int] = []

    objects.append("<< /Type /Catalog /Pages 2 0 R >>")
    objects.append("")
    objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    for page in pages:
        content = _page_content(page)
        content_id = len(objects) + 1
        objects.append(f"<< /Length {len(content.encode('latin-1', 'replace'))} >>\nstream\n{content}\nendstream")
        page_id = len(objects) + 1
        page_object_ids.append(page_id)
        objects.append(
            "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 3 0 R >> >> /Contents {content_id} 0 R >>"
        )

    kids = " ".join(f"{page_id} 0 R" for page_id in page_object_ids)
    objects[1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_object_ids)} >>"

    return _build_pdf(objects)


def _page_content(lines: list[str]) -> str:
    commands = ["BT", "/F1 10 Tf", "50 750 Td", "14 TL"]
    for line in lines:
        commands.append(f"({_escape(line)}) Tj")
        commands.append("T*")
    commands.append("ET")
    return "\n".join(commands)


def _build_pdf(objects: list[str]) -> bytes:
    chunks = ["%PDF-1.4\n%\xE2\xE3\xCF\xD3\n"]
    offsets: list[int] = []
    current = len(chunks[0].encode("latin-1"))
    for index, obj in enumerate(objects, start=1):
        offsets.append(current)
        chunk = f"{index} 0 obj\n{obj}\nendobj\n"
        chunks.append(chunk)
        current += len(chunk.encode("latin-1", "replace"))

    xref_offset = current
    xref = ["xref", f"0 {len(objects) + 1}", "0000000000 65535 f "]
    xref.extend(f"{offset:010d} 00000 n " for offset in offsets)
    trailer = [
        "\n".join(xref),
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>",
        "startxref",
        str(xref_offset),
        "%%EOF",
    ]
    chunks.append("\n".join(trailer))
    return "".join(chunks).encode("latin-1", "replace")


def _escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
