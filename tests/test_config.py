import pytest
from pathlib import Path

from y4rb.config import resolve_config


def test_resolves_yaml_resume_and_html_template(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "resume.yaml").write_text("name: Test")
    (tmp_path / "template.html").write_text("<h1>test</h1>")

    cfg = resolve_config()

    assert cfg.resume == (tmp_path / "resume.yaml").resolve()
    assert cfg.template == (tmp_path / "template.html").resolve()
    assert cfg.style is None


def test_falls_back_to_resume_yml(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "resume.yml").write_text("name: Test")
    (tmp_path / "template.html").write_text("<h1>test</h1>")

    cfg = resolve_config()

    assert cfg.resume == (tmp_path / "resume.yml").resolve()


def test_falls_back_to_j2_template(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "resume.yaml").write_text("name: Test")
    (tmp_path / "template.j2.html").write_text("<h1>test</h1>")

    cfg = resolve_config()

    assert cfg.template == (tmp_path / "template.j2.html").resolve()


def test_picks_up_style_css(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "resume.yaml").write_text("name: Test")
    (tmp_path / "template.html").write_text("<h1>test</h1>")
    (tmp_path / "style.css").write_text("body {}")

    cfg = resolve_config()

    assert cfg.style == (tmp_path / "style.css").resolve()


def test_config_file_overrides_defaults(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "my-resume.yaml").write_text("name: Custom")
    (tmp_path / "my-template.html").write_text("<h1>test</h1>")
    (tmp_path / "y4rb.yaml").write_text(
        "resume: my-resume.yaml\ntemplate: my-template.html\n"
    )

    cfg = resolve_config()

    assert cfg.resume == (tmp_path / "my-resume.yaml").resolve()
    assert cfg.template == (tmp_path / "my-template.html").resolve()


def test_explicit_config_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data.yaml").write_text("name: Explicit")
    (tmp_path / "tmpl.html").write_text("<h1>test</h1>")
    config_file = tmp_path / "custom.yaml"
    config_file.write_text("resume: data.yaml\ntemplate: tmpl.html\n")

    cfg = resolve_config(config_file)

    assert cfg.resume == (tmp_path / "data.yaml").resolve()
    assert cfg.template == (tmp_path / "tmpl.html").resolve()


def test_raises_when_resume_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "template.html").write_text("<h1>test</h1>")

    with pytest.raises(FileNotFoundError, match="resume"):
        resolve_config()


def test_raises_when_template_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "resume.yaml").write_text("name: Test")

    with pytest.raises(FileNotFoundError, match="template"):
        resolve_config()


def test_config_style_missing_file_returns_none(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "resume.yaml").write_text("name: Test")
    (tmp_path / "template.html").write_text("<h1>test</h1>")
    (tmp_path / "y4rb.yaml").write_text(
        "resume: resume.yaml\ntemplate: template.html\nstyle: nonexistent.css\n"
    )

    cfg = resolve_config()

    assert cfg.style is None
