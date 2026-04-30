from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel


class Config(BaseModel):
    resume: Path
    template: Path
    style: Path | None = None
    preview: bool = True


def resolve_config(directory: Path | None = None) -> Config:
    base = directory.resolve() if directory is not None else Path.cwd()
    raw = _load_raw_config(base)

    resume = _require(
        raw.get("resume"),
        ["resume.yaml", "resume.yml"],
        "resume data file",
        base,
    )
    template = _require(
        raw.get("template"),
        ["template.html", "template.j2.html"],
        "template file",
        base,
    )
    style = _optional(raw.get("style"), ["style.css"], base)
    preview = bool(raw.get("preview", True))

    return Config(resume=resume, template=template, style=style, preview=preview)


def _load_raw_config(base: Path) -> dict[str, Any]:
    for name in ("y4rb.yaml", "y4rb.yml"):
        path = base / name
        if path.exists():
            data = yaml.safe_load(path.read_text())
            return data if isinstance(data, dict) else {}

    return {}


def _require(explicit: str | None, defaults: list[str], label: str, base: Path) -> Path:
    if explicit is not None:
        p = (base / explicit).resolve()
        if not p.exists():
            raise FileNotFoundError(f"File not found: {p}")
        return p

    for name in defaults:
        p = base / name
        if p.exists():
            return p.resolve()

    tried = " or ".join(defaults)
    raise FileNotFoundError(f"Could not find {label}: tried {tried}")


def _optional(explicit: str | None, defaults: list[str], base: Path) -> Path | None:
    if explicit is not None:
        p = (base / explicit).resolve()
        return p if p.exists() else None

    for name in defaults:
        p = base / name
        if p.exists():
            return p.resolve()

    return None
