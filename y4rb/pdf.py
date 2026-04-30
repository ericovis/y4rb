from __future__ import annotations

import os
import subprocess  # nosec B404
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import BrowserType, sync_playwright

from y4rb.config import Config
from y4rb.renderer import render as render_html

# When running as a PyInstaller binary the extraction temp dir changes every
# launch, so browsers installed there are immediately lost. Pin them to a
# stable user-owned directory instead.
if getattr(sys, "frozen", False):
    os.environ.setdefault(
        "PLAYWRIGHT_BROWSERS_PATH", str(Path.home() / ".y4rb" / "browsers")
    )


def render_pdf(cfg: Config, output: Path) -> None:
    html = render_html(cfg.resume, cfg.template, cfg.style)

    with tempfile.NamedTemporaryFile(
        suffix=".html", delete=False, mode="w", encoding="utf-8"
    ) as f:
        f.write(html)
        tmp_html = Path(f.name)

    try:
        with sync_playwright() as p:
            _ensure_chromium(p.chromium)
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"file://{tmp_html}", wait_until="networkidle")
            page.pdf(path=str(output), format="A4", print_background=True)
            browser.close()
    finally:
        tmp_html.unlink(missing_ok=True)


def _ensure_chromium(chromium: BrowserType) -> None:
    if not Path(chromium.executable_path).exists():
        print("Chromium not found, installing via Playwright...")
        if getattr(sys, "frozen", False):
            from playwright._impl._driver import compute_driver_executable

            driver_executable, driver_cli = compute_driver_executable()
            subprocess.run([str(driver_executable), driver_cli, "install", "chromium"], check=True)  # nosec B603
        else:
            subprocess.run(  # nosec B603
                [sys.executable, "-m", "playwright", "install", "chromium"],
                check=True,
            )
