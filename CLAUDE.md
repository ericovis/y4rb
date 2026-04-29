This is a simple resumé builder that uses HTML, CSS and YAML to generate resumés. HTML and CSS will define the overall look while YAML will define the data.


## Project Structure

```
bin/
  run          — Wrapper: uv run <args>
  y4rb         — Wrapper: uv run main.py <args>
  test         — Wrapper: uv run pytest -vvv
y4rb/
  cli.py       — Typer CLI entry point; exposes the `preview` command
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
- **CLI** (`y4rb/cli.py`): single `preview` command via Typer. Options: `--config/-c`, `--port/-p` (default 8080), `--host` (default 127.0.0.1).


## Tools

This repo uses `uv` for package and project management. Convenience scripts in `bin/` wrap `uv run` — always prefer these over calling tools directly.

| Script | What it does |
|--------|--------------|
| `./bin/run <args>` | Runs `uv run <args>` — use this as the base runner |
| `./bin/y4rb <args>` | Runs `main.py` (e.g. `./bin/y4rb preview`) |
| `./bin/test` | Runs `pytest -vvv` |

Examples:
- Run the app: `./bin/run python main.py`
- Preview resume: `./bin/y4rb preview`
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


## Code Verification Loop

Before considering any task complete, run in order:
1. `./bin/run ruff check .` — must pass with no errors
2. `./bin/run ty check` — must pass with no errors
3. `./bin/test` — all tests must pass
