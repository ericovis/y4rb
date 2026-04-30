This is a simple resumé builder that uses HTML, CSS and YAML to generate resumés. HTML and CSS will define the overall look while YAML will define the data.


## Project Structure

```
bin/
  run          — Wrapper: uv run <args>
  y4rb         — Wrapper: uv run main.py <args>
  test         — Wrapper: uv run pytest -vvv
  build        — Wrapper: uv run pyinstaller y4rb.spec --noconfirm
y4rb/
  cli.py       — Typer CLI entry point; exposes `init`, `render`, and `preview` commands
  config.py    — Config resolution: locates resume/template/style/head files by convention
  renderer.py  — Jinja2 rendering: loads YAML data and renders via template inheritance
  server.py    — Dev server with live-reload via SSE (watchfiles watches resume/template/style)
  pdf.py       — PDF export via Playwright/headless Chromium
  defaults/    — Bundled starter files copied by `init` (resume.yml, template/, AGENTS.md, etc.)
  templates/   — Built-in Jinja2 base templates (_base.html, head.j2.html)
tests/
  conftest.py         — Shared fixtures (resume, template, style, head, config_dir)
  test_config.py      — Unit tests for config resolution logic
  test_renderer.py    — Unit tests for the Jinja2 renderer
  test_renderer_extra.py — Additional renderer tests
  test_cli.py         — CLI command tests
  test_server.py      — Server tests
  test_binary.py      — PyInstaller binary smoke tests
  test_pdf.py         — PDF rendering tests
main.py        — Entry point: calls cli.app()
y4rb.spec      — PyInstaller build spec
```


## Architecture

- **Config** (`y4rb/config.py`): resolves files by convention from a base directory (defaults to CWD). Looks for `resume.yaml`/`resume.yml`, `template/resume.j2.html` (or legacy `template.html`), `template/style.css`/`style.css`, and `template/head.j2.html`. Returns a `Config(resume, template, style, head)` Pydantic model. No project-level config file — all resolution is convention-based.
- **Renderer** (`y4rb/renderer.py`): loads YAML with PyYAML, renders via Jinja2 with `autoescape` enabled. Uses `ChoiceLoader` combining the user's template directory and built-in `y4rb/templates/`. Every template auto-extends `_base.html`, which handles the `<html>`/`<head>`/`<body>` scaffold, style inlining, pagedjs polyfill (preview mode), and SSE live-reload script.
- **Server** (`y4rb/server.py`): stdlib `ThreadingHTTPServer`, serves `/` (HTML) and `/events` (SSE). Style is inlined in the HTML — no separate `/style.css` route. A background thread uses `watchfiles` to watch resume/template/style files and broadcasts `reload` events to connected clients.
- **PDF** (`y4rb/pdf.py`): renders HTML to a temp file and uses Playwright's sync API with headless Chromium to export A4 PDF. Auto-installs Chromium if missing. When running as a PyInstaller binary, browser binaries are pinned to `~/.y4rb/browsers/`.
- **CLI** (`y4rb/cli.py`): three commands via Typer:
  - `init [directory]` — scaffolds a new resume project (copies defaults, creates `tailored/`, symlinks `CLAUDE.md → AGENTS.md`)
  - `preview [--dir/-d] [--resume/-r] [--port/-p] [--host]` — live-reload browser preview (default port 8080, host 127.0.0.1)
  - `render [--dir/-d] [--resume/-r] [--output/-o]` — exports to PDF (default `resume.pdf`)


## Resume Project Layout (user-created via `init`)

```
resume.yml          — master resume data
tailored/           — job-specific complete YAML variants
template/
  resume.j2.html    — Jinja2 HTML template (resume layout)
  head.j2.html      — <head> content: title, fonts, meta tags
  style.css         — stylesheet (inlined at render time)
AGENTS.md           — AI agent instructions for tailoring resumes
CLAUDE.md           — symlink to AGENTS.md
.gitignore
```


## Tools

This repo uses `uv` for package and project management. Convenience scripts in `bin/` wrap `uv run` — always prefer these over calling tools directly.

| Script | What it does |
|--------|--------------|
| `./bin/run <args>` | Runs `uv run <args>` — use this as the base runner |
| `./bin/y4rb <args>` | Runs `main.py` (e.g. `./bin/y4rb preview`) |
| `./bin/test` | Runs `pytest -vvv` |
| `./bin/build` | Builds standalone binary via PyInstaller |

Examples:
- Run the app: `./bin/run python main.py`
- Init a new project: `./bin/y4rb init ./my-resume`
- Preview resume: `./bin/y4rb preview`
- Render to PDF: `./bin/y4rb render --output resume.pdf`
- Lint: `./bin/run ruff check .`
- Format: `./bin/run ruff format .`
- Type check: `./bin/run ty check`
- Tests: `./bin/test`


## Key Dependencies

| Package | Purpose |
|---------|---------|
| `jinja2` | HTML template rendering |
| `pyyaml` | YAML resume data parsing |
| `pydantic` | Config model validation |
| `typer` | CLI framework |
| `watchfiles` | File watching for live reload |
| `playwright` | Headless Chromium for PDF export |


## Code Verification Loop

Before considering any task complete, run in order:
1. `./bin/run ruff check .` — must pass with no errors
2. `./bin/run ty check` — must pass with no errors
3. `./bin/run bandit -r y4rb/` — must pass with no high-severity findings
4. `./bin/test` — all tests must pass
