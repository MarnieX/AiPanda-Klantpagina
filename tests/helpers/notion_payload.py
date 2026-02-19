"""Helpers to simulate Notion payload rendering from the klantpagina template."""

from __future__ import annotations

from pathlib import Path


def _team_columns_markdown(consultants: list[dict]) -> str:
    blocks = ["<columns>"]
    for c in consultants:
        blocks.extend([
            "\t<column>",
            f"\t\t![]({c['foto_url']})",
            f"\t\t**{c['naam']}**",
            f"\t\t{c['functie']}",
            f"\t\t{c['telefoon']}",
            f"\t\t{c['email']}",
            "\t</column>",
        ])
    blocks.append("</columns>")
    return "\n".join(blocks)


def render_klantpagina_template(
    template_path: Path,
    fields: dict[str, str],
    consultants: list[dict],
) -> str:
    """Render the markdown template to a Notion-ready string."""
    raw = template_path.read_text(encoding="utf-8")
    start_marker = "```markdown"
    end_marker = "\n```"
    start_idx = raw.index(start_marker) + len(start_marker)
    end_idx = raw.index(end_marker, start_idx)
    content = raw[start_idx:end_idx].lstrip("\n")

    # Replace hero image placeholder first (or remove line entirely).
    panda_image_url = fields.get("PANDA_IMAGE_URL", "").strip()
    if panda_image_url:
        content = content.replace("[PANDA_IMAGE_URL]", panda_image_url)
    else:
        content = content.replace("![]([PANDA_IMAGE_URL])\n", "")

    # Replace simple placeholders.
    for key, value in fields.items():
        if key == "PANDA_IMAGE_URL":
            continue
        content = content.replace(f"[{key}]", value)

    # Replace static team example columns with dynamic consultants columns.
    team_heading = "## Jouw AI Panda Team"
    start = content.index(team_heading)
    columns_start = content.index("<columns>", start)
    columns_end = content.index("</columns>", columns_start) + len("</columns>")
    dynamic_columns = _team_columns_markdown(consultants)
    content = content[:columns_start] + dynamic_columns + content[columns_end:]

    return content


def build_notion_create_pages_payload(
    bedrijfsnaam: str,
    markdown_content: str,
    parent_page_id: str | None = None,
) -> dict:
    """Build a simulated notion-create-pages payload for validation tests."""
    payload = {
        "title": f"AI Panda x {bedrijfsnaam}",
        "content": markdown_content,
    }
    if parent_page_id:
        payload["parent"] = {"page_id": parent_page_id}
    return payload
