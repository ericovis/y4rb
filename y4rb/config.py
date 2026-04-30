from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel


class Config(BaseModel):
    resume: Path
    template: Path
    style: Path | None = None
    head: Path | None = None


def resolve_config(
    directory: Path | None = None,
    resume_file: Path | None = None,
) -> Config:
    base = directory.resolve() if directory is not None else Path.cwd()

    if resume_file is not None:
        p = (base / resume_file).resolve()
        if not p.exists():
            raise FileNotFoundError(f"File not found: {p}")
        resume = p
    else:
        resume = _require(
            ["resume.yaml", "resume.yml"],
            "resume data file",
            base,
        )

    template = _require(
        [
            "template/resume.j2.html",
            "template/template.html",
            "template.j2.html",
            "template.html",
        ],
        "template file",
        base,
    )
    style = _optional(["template/style.css", "style.css"], base)
    head = _optional(["template/head.j2.html"], base)

    return Config(resume=resume, template=template, style=style, head=head)


def _require(defaults: list[str], label: str, base: Path) -> Path:
    for name in defaults:
        p = base / name
        if p.exists():
            return p.resolve()

    tried = " or ".join(defaults)
    raise FileNotFoundError(f"Could not find {label}: tried {tried}")


def _optional(defaults: list[str], base: Path) -> Path | None:
    for name in defaults:
        p = base / name
        if p.exists():
            return p.resolve()

    return None
