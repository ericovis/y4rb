import shutil
from pathlib import Path

import pytest

from y4rb.config import resolve_config

_DEFAULTS_TEMPLATE = Path(__file__).parent.parent / "y4rb" / "defaults" / "template"


def test_resolves_default_files(config_dir: Path) -> None:
    cfg = resolve_config()
    assert cfg.resume == (config_dir / "resume.yml").resolve()
    assert cfg.template == (config_dir / "template" / "resume.j2.html").resolve()
    assert cfg.style == (config_dir / "template" / "style.css").resolve()
    assert cfg.head == (config_dir / "template" / "head.j2.html").resolve()


def test_falls_back_to_resume_yaml(config_dir: Path) -> None:
    (config_dir / "resume.yml").rename(config_dir / "resume.yaml")
    cfg = resolve_config()
    assert cfg.resume == (config_dir / "resume.yaml").resolve()


def test_falls_back_to_template_html_in_subdir(config_dir: Path) -> None:
    (config_dir / "template" / "resume.j2.html").rename(
        config_dir / "template" / "template.html"
    )
    cfg = resolve_config()
    assert cfg.template == (config_dir / "template" / "template.html").resolve()


def test_falls_back_to_flat_template_html(config_dir: Path) -> None:
    (config_dir / "template" / "resume.j2.html").unlink()
    shutil.copy(_DEFAULTS_TEMPLATE / "resume.j2.html", config_dir / "template.html")
    cfg = resolve_config()
    assert cfg.template == (config_dir / "template.html").resolve()


def test_falls_back_to_flat_style_css(config_dir: Path) -> None:
    (config_dir / "template" / "style.css").unlink()
    shutil.copy(_DEFAULTS_TEMPLATE / "style.css", config_dir / "style.css")
    cfg = resolve_config()
    assert cfg.style == (config_dir / "style.css").resolve()


def test_explicit_directory(config_dir: Path, tmp_path: Path) -> None:
    resume_dir = tmp_path / "myresume"
    resume_dir.mkdir()
    (resume_dir / "resume.yml").write_bytes((config_dir / "resume.yml").read_bytes())
    (resume_dir / "template").mkdir()
    (resume_dir / "template" / "resume.j2.html").write_bytes(
        (config_dir / "template" / "resume.j2.html").read_bytes()
    )
    cfg = resolve_config(resume_dir)
    assert cfg.resume == (resume_dir / "resume.yml").resolve()
    assert cfg.template == (resume_dir / "template" / "resume.j2.html").resolve()


def test_resume_file_override(config_dir: Path) -> None:
    tailored = config_dir / "tailored"
    tailored.mkdir()
    variant = tailored / "acme.yml"
    variant.write_bytes((config_dir / "resume.yml").read_bytes())
    cfg = resolve_config(resume_file=Path("tailored/acme.yml"))
    assert cfg.resume == variant.resolve()


def test_resume_file_override_absolute(config_dir: Path) -> None:
    variant = config_dir / "custom.yml"
    variant.write_bytes((config_dir / "resume.yml").read_bytes())
    cfg = resolve_config(resume_file=variant)
    assert cfg.resume == variant.resolve()


def test_resume_file_override_missing_raises(config_dir: Path) -> None:
    with pytest.raises(FileNotFoundError, match="nonexistent.yml"):
        resolve_config(resume_file=Path("nonexistent.yml"))


def test_raises_when_resume_missing(config_dir: Path) -> None:
    (config_dir / "resume.yml").unlink()
    with pytest.raises(FileNotFoundError, match="resume"):
        resolve_config()


def test_raises_when_template_missing(config_dir: Path) -> None:
    (config_dir / "template" / "resume.j2.html").unlink()
    with pytest.raises(FileNotFoundError, match="template"):
        resolve_config()


def test_no_head_returns_none(config_dir: Path) -> None:
    (config_dir / "template" / "head.j2.html").unlink()
    cfg = resolve_config()
    assert cfg.head is None


def test_style_missing_returns_none(config_dir: Path) -> None:
    (config_dir / "template" / "style.css").unlink()
    cfg = resolve_config()
    assert cfg.style is None
