from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from jinja2 import ChoiceLoader, Environment, FileSystemLoader, select_autoescape

_BUILTIN_TEMPLATES = Path(__file__).parent / "templates"


def render(
    resume: Path,
    template: Path,
    style: Path | None = None,
    *,
    preview: bool = False,
    reload: bool = False,
) -> str:
    data: Any = yaml.safe_load(resume.read_text())
    style_content = style.read_text() if style else None
    env = Environment(
        loader=ChoiceLoader([
            FileSystemLoader(str(template.parent)),
            FileSystemLoader(str(_BUILTIN_TEMPLATES)),
        ]),
        autoescape=select_autoescape(["html"]),
    )
    source = '{% extends "_base.html" %}\n' + template.read_text()
    tmpl = env.from_string(source)
    return tmpl.render(resume=data, style=style_content, preview=preview, reload=reload)
