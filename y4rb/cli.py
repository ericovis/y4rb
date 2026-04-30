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
def init(
    directory: Path = typer.Argument(
        Path("."), help="Directory to initialize (default: current directory)"
    ),
) -> None:
    """Initialize a new resume project in the given directory."""
    directory.mkdir(parents=True, exist_ok=True)
    for name in _DEFAULT_FILES:
        dest = directory / name
        if dest.exists():
            typer.echo(f"Skipping {name} (already exists)")
            continue
        dest.write_bytes((_DEFAULTS / name).read_bytes())
        typer.echo(f"Created {name}")


@app.command()
def render(
    directory: Path | None = typer.Option(
        None, "--dir", "-d", help="Directory containing resume files (default: current directory)"
    ),
    output: Path = typer.Option(
        Path("resume.pdf"), "--output", "-o", help="Output PDF path"
    ),
) -> None:
    """Render the resume to a PDF file."""
    try:
        cfg = resolve_config(directory)
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

    from y4rb.pdf import render_pdf

    render_pdf(cfg, output)
    typer.echo(f"PDF saved to {output}")


@app.command()
def preview(
    directory: Path | None = typer.Option(
        None, "--dir", "-d", help="Directory containing resume files (default: current directory)"
    ),
    port: int = typer.Option(8080, "--port", "-p", help="Port to serve on"),
    host: str = typer.Option("127.0.0.1", "--host", help="Host to bind to"),
) -> None:
    """Preview the resume locally with live reload."""
    try:
        cfg = resolve_config(directory)
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

    ResumeServer(cfg).run(host, port)
