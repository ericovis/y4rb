This is a simple resumé builder that uses HTML, CSS and YAML to generate resumés. HTML and CSS will define the overall look while YAML will define the data.


## Project Structure

```
y4rb/
  cli.py       — Typer CLI entry point; exposes the `serve` command
  config.py    — Config resolution: reads y4rb.yaml and locates resume/template/style files
  renderer.py  — Jinja2 rendering: loads YAML data and renders the HTML template
  server.py    — Dev server with live-reload via SSE (watchfiles watches resume/template/style)
resume/
  resume.yml   — Sample resume data (YAML)
  template.html — Jinja2 HTML template; resume data exposed as `resume` variable
  style.css    — Stylesheet linked from the template
tests/
  test_config.py   — Unit tests for config resolution logic
  test_renderer.py — Unit tests for the Jinja2 renderer
main.py        — Entry point: calls cli.app()
y4rb.yaml      — Project config pointing to resume/, template, and style paths
```


## Architecture

- **Config** (`y4rb/config.py`): reads `y4rb.yaml` (or `y4rb.yml`) from CWD, or falls back to default filenames (`resume.yaml`/`resume.yml`, `template.html`/`template.j2.html`, `style.css`). Returns a `Config(resume, template, style)` Pydantic model.
- **Renderer** (`y4rb/renderer.py`): loads YAML with PyYAML, renders via Jinja2 with `autoescape` enabled. Template receives the entire YAML document as `resume`.
- **Server** (`y4rb/server.py`): stdlib `ThreadingHTTPServer`, serves `/` (HTML), `/style.css`, and `/events` (SSE). A background thread uses `watchfiles` to watch the resume/template/style files and broadcasts `reload` events to connected clients.
- **CLI** (`y4rb/cli.py`): single `serve` command via Typer. Options: `--config/-c`, `--port/-p` (default 8080), `--host` (default 127.0.0.1).


## Tools

This repo uses `uv` for package and project management. Always use `uv run` to execute any tool or script — never call `python`, `ruff`, `ty`, `pytest`, or other project tools directly.

Examples:
- Run the app: `uv run python main.py`
- Serve resume: `uv run python main.py serve` (or `uv run y4rb serve`)
- Lint: `uv run ruff check .`
- Format: `uv run ruff format .`
- Type check: `uv run ty check`
- Tests: `uv run pytest`


## Key Dependencies

| Package | Purpose |
|---------|---------|
| `jinja2` | HTML template rendering |
| `pyyaml` | YAML resume data parsing |
| `pydantic` | Config model validation |
| `typer` | CLI framework |
| `watchfiles` | File watching for live reload |


## Code Verification Loop

Before considering any task complete, run in order:
1. `uv run ruff check .` — must pass with no errors
2. `uv run ty check` — must pass with no errors
3. `uv run pytest` — all tests must pass
