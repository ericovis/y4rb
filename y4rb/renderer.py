from __future__ import annotations

import re
import warnings
from pathlib import Path
from typing import Any

import yaml
from jinja2 import ChoiceLoader, Environment, FileSystemLoader, select_autoescape

_BUILTIN_TEMPLATES = Path(__file__).parent / "templates"

_ROOT_SELECTOR_RE = re.compile(
    r'(?<![.#:\w-])(?:html|body)(?![\w.#:-])\s*\{[^{}]*\}',
    re.DOTALL,
)


def _strip_root_selectors(css: str) -> str:
    """Remove html/body rules from user CSS; they conflict with the #resume wrapper."""
    if _ROOT_SELECTOR_RE.search(css):
        warnings.warn(
            "'html' and 'body' selectors in style.css are ignored — use '#resume' instead.",
            UserWarning,
            stacklevel=3,
        )
        return _ROOT_SELECTOR_RE.sub("", css)
    return css


def render(
    resume: Path,
    template: Path,
    style: Path | None = None,
    *,
    preview: bool = False,
    reload: bool = False,
) -> str:
    data: Any = yaml.safe_load(resume.read_text())
    style_content = _strip_root_selectors(style.read_text()) if style else None
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
