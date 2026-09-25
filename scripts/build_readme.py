#!/usr/bin/env python3
"""Copia las historias principales de docs/USER_STORIES.md al README §5.

docs/USER_STORIES.md es la única fuente de las historias. Las marcadas con ⭐
en su título se copian, en el orden en que aparecen, entre los marcadores
BEGIN/END del README. Nunca se edita a mano esa zona del README.

Uso:
    python3 scripts/build_readme.py          # regenera el README
    python3 scripts/build_readme.py --check  # falla (exit 1) si no está al día
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORIES = ROOT / "docs" / "USER_STORIES.md"
README = ROOT / "readme.md"

BEGIN = "<!-- BEGIN historias-principales: generado por scripts/build_readme.py desde docs/USER_STORIES.md; no editar a mano -->"
END = "<!-- END historias-principales -->"

STORY_RE = re.compile(
    r"^### (US-\d+ · [^\n]+?) ⭐\n(.*?^```gherkin\n.*?^```)$",
    re.MULTILINE | re.DOTALL,
)


def main_stories(text: str) -> list[tuple[str, str]]:
    stories = STORY_RE.findall(text)
    if not stories:
        sys.exit(f"No hay historias marcadas con ⭐ en {STORIES.relative_to(ROOT)}")
    return stories


def to_readme(body: str) -> str:
    # Los enlaces relativos de docs/ tienen que resolverse desde la raíz.
    return body.replace("](../readme.md#", "](#").replace("](./", "](docs/")


def render(text: str) -> str:
    parts = [
        f"**Historia de Usuario {n}**\n\n#### {title}\n{to_readme(body)}"
        for n, (title, body) in enumerate(main_stories(text), start=1)
    ]
    return "\n\n".join(parts)


def main() -> int:
    readme = README.read_text(encoding="utf-8")
    start, end = readme.find(BEGIN), readme.find(END)
    if start == -1 or end == -1 or end < start:
        sys.exit(f"Faltan los marcadores BEGIN/END en {README.name}")

    generated = render(STORIES.read_text(encoding="utf-8"))
    updated = f"{readme[:start]}{BEGIN}\n\n{generated}\n\n{readme[end:]}"

    if "--check" in sys.argv[1:]:
        if updated != readme:
            print(f"{README.name} no está al día: ejecuta python3 scripts/build_readme.py")
            return 1
        print(f"{README.name} está al día")
        return 0

    if updated != readme:
        README.write_text(updated, encoding="utf-8")
        print(f"{README.name} actualizado")
    else:
        print(f"{README.name} ya estaba al día")
    return 0


if __name__ == "__main__":
    sys.exit(main())
