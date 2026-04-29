from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape


def render(resume: Path, template: Path) -> str:
    data: Any = yaml.safe_load(resume.read_text())
    env = Environment(
        loader=FileSystemLoader(str(template.parent)),
        autoescape=select_autoescape(["html"]),
    )
    tmpl = env.get_template(template.name)
    return tmpl.render(resume=data)
