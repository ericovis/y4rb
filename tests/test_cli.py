from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from y4rb.cli import app

runner = CliRunner()


def test_preview_exits_1_when_resume_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["preview"])
    assert result.exit_code == 1
    assert "Error" in result.output


def test_preview_starts_server_on_success(config_dir: Path) -> None:
    with patch("y4rb.cli.ResumeServer") as mock_cls:
        mock_cls.return_value.run = MagicMock()
        result = runner.invoke(app, ["preview"])
    assert result.exit_code == 0
    mock_cls.return_value.run.assert_called_once_with("127.0.0.1", 8080)


def test_preview_accepts_custom_port(config_dir: Path) -> None:
    with patch("y4rb.cli.ResumeServer") as mock_cls:
        mock_cls.return_value.run = MagicMock()
        result = runner.invoke(app, ["preview", "--port", "9000"])
    assert result.exit_code == 0
    mock_cls.return_value.run.assert_called_once_with("127.0.0.1", 9000)


def test_preview_accepts_custom_host(config_dir: Path) -> None:
    with patch("y4rb.cli.ResumeServer") as mock_cls:
        mock_cls.return_value.run = MagicMock()
        result = runner.invoke(app, ["preview", "--host", "0.0.0.0"])
    assert result.exit_code == 0
    mock_cls.return_value.run.assert_called_once_with("0.0.0.0", 8080)


def test_render_exits_1_when_resume_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["render"])
    assert result.exit_code == 1
    assert "Error" in result.output


def test_render_calls_render_pdf(config_dir: Path, tmp_path: Path) -> None:
    output = tmp_path / "out.pdf"
    with patch("y4rb.pdf.render_pdf") as mock_pdf:
        result = runner.invoke(app, ["render", "--output", str(output)])
    assert result.exit_code == 0
    mock_pdf.assert_called_once()
    assert str(output) in result.output


def test_render_uses_default_output_name(config_dir: Path) -> None:
    with patch("y4rb.pdf.render_pdf") as mock_pdf:
        result = runner.invoke(app, ["render"])
    assert result.exit_code == 0
    args = mock_pdf.call_args
    assert args[0][1].name == "resume.pdf"


def _make_playwright_mock(tmp_path: Path) -> MagicMock:
    page = MagicMock()
    browser = MagicMock()
    browser.new_page.return_value = page
    chromium = MagicMock()
    chromium.launch.return_value = browser

    def fake_pdf(**kwargs: object) -> None:
        Path(str(kwargs["path"])).write_bytes(b"%PDF fake")

    page.pdf.side_effect = fake_pdf

    pw_ctx = MagicMock()
    pw_ctx.__enter__ = MagicMock(return_value=pw_ctx)
    pw_ctx.__exit__ = MagicMock(return_value=False)
    pw_ctx.chromium = chromium
    return pw_ctx


def test_init_creates_default_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert (tmp_path / "resume.yml").exists()
    assert (tmp_path / "template.html").exists()
    assert (tmp_path / "style.css").exists()
    assert "Created resume.yml" in result.output
    assert "Created template.html" in result.output
    assert "Created style.css" in result.output


def test_init_skips_existing_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "resume.yml").write_text("existing")
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert "Skipping resume.yml" in result.output
    assert (tmp_path / "resume.yml").read_text() == "existing"


def test_init_then_render_produces_pdf(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)

    init_result = runner.invoke(app, ["init"])
    assert init_result.exit_code == 0

    output = tmp_path / "resume.pdf"
    pw_mock = _make_playwright_mock(tmp_path)
    with patch("y4rb.pdf.sync_playwright", return_value=pw_mock):
        render_result = runner.invoke(app, ["render", "--output", str(output)])

    assert render_result.exit_code == 0
    assert output.exists()
    assert output.read_bytes().startswith(b"%PDF")
