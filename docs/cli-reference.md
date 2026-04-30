# CLI Reference

## `y4rb init`

Scaffold a new resume project.

```
y4rb init [DIRECTORY]
```

| Argument | Default | Description |
|---|---|---|
| `DIRECTORY` | `.` (current directory) | Where to create the project |

Creates `resume.yml`, `template/`, `tailored/`, `AGENTS.md`, and a `CLAUDE.md` symlink pointing to `AGENTS.md`.

**Example:**

```bash
y4rb init my-resume
```

---

## `y4rb preview`

Start a live-reload browser preview.

```
y4rb preview [OPTIONS]
```

| Option | Default | Description |
|---|---|---|
| `-d`, `--dir` | `.` | Resume project directory |
| `-r`, `--resume` | `resume.yml` | Path to the YAML resume file |
| `-p`, `--port` | `8080` | Port to listen on |
| `--host` | `127.0.0.1` | Host to bind to |

Serves the rendered resume at `http://<host>:<port>/`. Watches the YAML, template, and stylesheet for changes and sends a reload signal to the browser automatically.

**Examples:**

```bash
# Default preview
y4rb preview

# Preview a tailored variant
y4rb preview --resume tailored/acme-backend.yml

# Bind on all interfaces
y4rb preview --host 0.0.0.0 --port 8080
```

---

## `y4rb render`

Export the resume to a PDF file.

```
y4rb render [OPTIONS]
```

| Option | Default | Description |
|---|---|---|
| `-d`, `--dir` | `.` | Resume project directory |
| `-r`, `--resume` | `resume.yml` | Path to the YAML resume file |
| `-o`, `--output` | `resume.pdf` | Output PDF path |

Uses headless Chromium via Playwright. Chromium is installed automatically on first use to `~/.y4rb/browsers/` when running as a standalone binary.

**Examples:**

```bash
# Render master resume
y4rb render --output resume.pdf

# Render a tailored variant
y4rb render --resume tailored/acme-backend.yml --output acme-backend.pdf
```
