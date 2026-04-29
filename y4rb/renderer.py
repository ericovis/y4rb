from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape


def render(resume: Path, template: Path, style: Path | None = None) -> str:
    data: Any = yaml.safe_load(resume.read_text())
    style_content = style.read_text() if style else None
    env = Environment(
        loader=FileSystemLoader(str(template.parent)),
        autoescape=select_autoescape(["html"]),
    )
    tmpl = env.get_template(template.name)
    return tmpl.render(resume=data, style=style_content)
