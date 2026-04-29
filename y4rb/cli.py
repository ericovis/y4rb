from __future__ import annotations

from pathlib import Path

import typer

from y4rb.config import resolve_config
from y4rb.server import ResumeServer

app = typer.Typer(no_args_is_help=True)


@app.command()
def serve(
    config: Path | None = typer.Option(
        None, "--config", "-c", help="Path to y4rb config file (default: y4rb.yaml/yml)"
    ),
    port: int = typer.Option(8080, "--port", "-p", help="Port to serve on"),
    host: str = typer.Option("127.0.0.1", "--host", help="Host to bind to"),
) -> None:
    """Serve the resume locally with live reload."""
    try:
        cfg = resolve_config(config)
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

    ResumeServer(cfg).run(host, port)
