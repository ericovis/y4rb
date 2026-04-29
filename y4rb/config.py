from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel


class Config(BaseModel):
    resume: Path
    template: Path
    style: Path | None = None


def resolve_config(config_path: Path | None = None) -> Config:
    raw = _load_raw_config(config_path)

    resume = _require(
        raw.get("resume"),
        ["resume.yaml", "resume.yml"],
        "resume data file",
    )
    template = _require(
        raw.get("template"),
        ["template.html", "template.j2.html"],
        "template file",
    )
    style = _optional(raw.get("style"), ["style.css"])

    return Config(resume=resume, template=template, style=style)


def _load_raw_config(config_path: Path | None) -> dict[str, Any]:
    if config_path is not None:
        data = yaml.safe_load(config_path.read_text())
        return data if isinstance(data, dict) else {}

    for name in ("y4rb.yaml", "y4rb.yml"):
        path = Path(name)
        if path.exists():
            data = yaml.safe_load(path.read_text())
            return data if isinstance(data, dict) else {}

    return {}


def _require(explicit: str | None, defaults: list[str], label: str) -> Path:
    if explicit is not None:
        p = Path(explicit).resolve()
        if not p.exists():
            raise FileNotFoundError(f"File not found: {p}")
        return p

    for name in defaults:
        p = Path(name)
        if p.exists():
            return p.resolve()

    tried = " or ".join(defaults)
    raise FileNotFoundError(f"Could not find {label}: tried {tried}")


def _optional(explicit: str | None, defaults: list[str]) -> Path | None:
    if explicit is not None:
        p = Path(explicit).resolve()
        return p if p.exists() else None

    for name in defaults:
        p = Path(name)
        if p.exists():
            return p.resolve()

    return None
