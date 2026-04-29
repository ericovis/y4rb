from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from y4rb.config import Config
from y4rb.pdf import _ensure_chromium, render_pdf


@pytest.fixture
def pdf_config(config_dir: Path) -> Config:
    from y4rb.config import resolve_config
    return resolve_config()


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


def test_render_pdf_creates_output_file(pdf_config: Config, tmp_path: Path) -> None:
    output = tmp_path / "out.pdf"
    pw_mock = _make_playwright_mock(tmp_path)

    with patch("y4rb.pdf.sync_playwright", return_value=pw_mock):
        render_pdf(pdf_config, output)

    assert output.exists()


def test_render_pdf_navigates_to_html_file(pdf_config: Config, tmp_path: Path) -> None:
    output = tmp_path / "out.pdf"
    pw_mock = _make_playwright_mock(tmp_path)

    with patch("y4rb.pdf.sync_playwright", return_value=pw_mock):
        render_pdf(pdf_config, output)

    page = pw_mock.chromium.launch.return_value.new_page.return_value
    goto_url = page.goto.call_args[0][0]
    assert goto_url.startswith("file://")
    assert goto_url.endswith(".html")


def test_ensure_chromium_skips_install_when_present(tmp_path: Path) -> None:
    fake_exe = tmp_path / "chromium"
    fake_exe.touch()
    chromium = MagicMock()
    chromium.executable_path = str(fake_exe)

    with patch("subprocess.run") as mock_run:
        _ensure_chromium(chromium)

    mock_run.assert_not_called()


def test_ensure_chromium_installs_when_missing(tmp_path: Path) -> None:
    chromium = MagicMock()
    chromium.executable_path = str(tmp_path / "nonexistent")

    with patch("subprocess.run") as mock_run:
        _ensure_chromium(chromium)

    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert "playwright" in args
    assert "install" in args
    assert "chromium" in args
