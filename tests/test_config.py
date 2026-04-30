import pytest
from pathlib import Path

from y4rb.config import resolve_config


def test_resolves_default_files(config_dir: Path) -> None:
    cfg = resolve_config()
    assert cfg.resume == (config_dir / "resume.yml").resolve()
    assert cfg.template == (config_dir / "template.html").resolve()
    assert cfg.style == (config_dir / "style.css").resolve()


def test_falls_back_to_resume_yaml(config_dir: Path) -> None:
    (config_dir / "resume.yml").rename(config_dir / "resume.yaml")
    cfg = resolve_config()
    assert cfg.resume == (config_dir / "resume.yaml").resolve()


def test_falls_back_to_j2_template(config_dir: Path) -> None:
    (config_dir / "template.html").rename(config_dir / "template.j2.html")
    cfg = resolve_config()
    assert cfg.template == (config_dir / "template.j2.html").resolve()


def test_config_file_overrides_defaults(config_dir: Path) -> None:
    (config_dir / "y4rb.yaml").write_text("resume: resume.yml\ntemplate: template.html\n")
    cfg = resolve_config()
    assert cfg.resume == (config_dir / "resume.yml").resolve()
    assert cfg.template == (config_dir / "template.html").resolve()


def test_explicit_directory(config_dir: Path, tmp_path: Path) -> None:
    resume_dir = tmp_path / "myresume"
    resume_dir.mkdir()
    (resume_dir / "resume.yml").write_bytes((config_dir / "resume.yml").read_bytes())
    (resume_dir / "template.html").write_bytes((config_dir / "template.html").read_bytes())
    cfg = resolve_config(resume_dir)
    assert cfg.resume == (resume_dir / "resume.yml").resolve()
    assert cfg.template == (resume_dir / "template.html").resolve()


def test_explicit_directory_picks_up_config_file(config_dir: Path, tmp_path: Path) -> None:
    resume_dir = tmp_path / "myresume"
    resume_dir.mkdir()
    (resume_dir / "resume.yml").write_bytes((config_dir / "resume.yml").read_bytes())
    (resume_dir / "template.html").write_bytes((config_dir / "template.html").read_bytes())
    (resume_dir / "y4rb.yaml").write_text("resume: resume.yml\ntemplate: template.html\n")
    cfg = resolve_config(resume_dir)
    assert cfg.resume == (resume_dir / "resume.yml").resolve()
    assert cfg.template == (resume_dir / "template.html").resolve()


def test_raises_when_resume_missing(config_dir: Path) -> None:
    (config_dir / "resume.yml").unlink()
    with pytest.raises(FileNotFoundError, match="resume"):
        resolve_config()


def test_raises_when_template_missing(config_dir: Path) -> None:
    (config_dir / "template.html").unlink()
    with pytest.raises(FileNotFoundError, match="template"):
        resolve_config()


def test_config_style_missing_returns_none(config_dir: Path) -> None:
    (config_dir / "y4rb.yaml").write_text(
        "resume: resume.yml\ntemplate: template.html\nstyle: nonexistent.css\n"
    )
    cfg = resolve_config()
    assert cfg.style is None


def test_preview_defaults_to_true(config_dir: Path) -> None:
    cfg = resolve_config()
    assert cfg.preview is True


def test_preview_can_be_disabled(config_dir: Path) -> None:
    (config_dir / "y4rb.yaml").write_text(
        "resume: resume.yml\ntemplate: template.html\npreview: false\n"
    )
    cfg = resolve_config()
    assert cfg.preview is False
