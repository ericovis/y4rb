from __future__ import annotations

from importlib.resources import files
from pathlib import Path

import typer

from y4rb.config import resolve_config
from y4rb.server import ResumeServer

app = typer.Typer(no_args_is_help=True)

_DEFAULTS = files("y4rb") / "defaults"
_DEFAULT_FILES = ("resume.yml", "template.html", "style.css")


@app.command()
def init() -> None:
    """Initialize a new resume project in the current directory."""
    for name in _DEFAULT_FILES:
        dest = Path(name)
        if dest.exists():
            typer.echo(f"Skipping {name} (already exists)")
            continue
        dest.write_bytes((_DEFAULTS / name).read_bytes())
        typer.echo(f"Created {name}")


@app.command()
def render(
    config: Path | None = typer.Option(
        None, "--config", "-c", help="Path to y4rb config file (default: y4rb.yaml/yml)"
    ),
    output: Path = typer.Option(
        Path("resume.pdf"), "--output", "-o", help="Output PDF path"
    ),
) -> None:
    """Render the resume to a PDF file."""
    try:
        cfg = resolve_config(config)
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

    from y4rb.pdf import render_pdf

    render_pdf(cfg, output)
    typer.echo(f"PDF saved to {output}")


@app.command()
def preview(
    config: Path | None = typer.Option(
        None, "--config", "-c", help="Path to y4rb config file (default: y4rb.yaml/yml)"
    ),
    port: int = typer.Option(8080, "--port", "-p", help="Port to serve on"),
    host: str = typer.Option("127.0.0.1", "--host", help="Host to bind to"),
) -> None:
    """Preview the resume locally with live reload."""
    try:
        cfg = resolve_config(config)
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

    ResumeServer(cfg).run(host, port)
