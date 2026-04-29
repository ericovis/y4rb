from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import BrowserType, sync_playwright

from y4rb.config import Config
from y4rb.renderer import render as render_html


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
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            check=True,
        )
