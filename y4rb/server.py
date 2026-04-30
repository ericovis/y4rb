from __future__ import annotations

import queue
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import watchfiles

from y4rb.config import Config
from y4rb.renderer import render


class ResumeServer:
    def __init__(self, config: Config) -> None:
        self.config = config
        self._html = ""
        self._clients: list[queue.Queue[str]] = []
        self._lock = threading.Lock()
        self._rebuild()

    def _rebuild(self) -> None:
        self._html = render(
            self.config.resume,
            self.config.template,
            style=self.config.style,
            preview=True,
            reload=True,
        )

    def _broadcast(self) -> None:
        with self._lock:
            for q in self._clients:
                q.put("reload")

    def _add_client(self, q: queue.Queue[str]) -> None:
        with self._lock:
            self._clients.append(q)

    def _remove_client(self, q: queue.Queue[str]) -> None:
        with self._lock:
            if q in self._clients:
                self._clients.remove(q)

    def _watch_loop(self) -> None:
        paths: list[Path] = [self.config.resume, self.config.template]
        if self.config.style:
            paths.append(self.config.style)
        for _ in watchfiles.watch(*paths):
            try:
                self._rebuild()
            except Exception as e:
                print(f"Rebuild error: {e}", flush=True)
                continue
            self._broadcast()

    def _make_handler(self) -> type[BaseHTTPRequestHandler]:
        outer = self

        class _Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                if self.path == "/":
                    outer._serve_index(self)
                elif self.path == "/events":
                    outer._serve_events(self)
                else:
                    self.send_error(404)

            def log_message(self, format: str, *args: Any) -> None:
                pass

        return _Handler

    def _serve_index(self, h: BaseHTTPRequestHandler) -> None:
        body = self._html.encode("utf-8")
        h.send_response(200)
        h.send_header("Content-Type", "text/html; charset=utf-8")
        h.send_header("Content-Length", str(len(body)))
        h.end_headers()
        h.wfile.write(body)

    def _serve_events(self, h: BaseHTTPRequestHandler) -> None:
        h.send_response(200)
        h.send_header("Content-Type", "text/event-stream")
        h.send_header("Cache-Control", "no-cache")
        h.send_header("Connection", "keep-alive")
        h.end_headers()

        q: queue.Queue[str] = queue.Queue()
        self._add_client(q)
        try:
            while True:
                try:
                    msg = q.get(timeout=15)
                    h.wfile.write(f"data: {msg}\n\n".encode())
                    h.wfile.flush()
                except queue.Empty:
                    # keep-alive heartbeat
                    h.wfile.write(b": heartbeat\n\n")
                    h.wfile.flush()
        except OSError:
            pass
        finally:
            self._remove_client(q)

    def run(self, host: str, port: int) -> None:
        watcher = threading.Thread(target=self._watch_loop, daemon=True)
        watcher.start()

        class _Server(ThreadingHTTPServer):
            def handle_error(self, request: Any, client_address: Any) -> None:
                import sys

                if isinstance(sys.exc_info()[1], (ConnectionResetError, BrokenPipeError)):
                    return
                super().handle_error(request, client_address)

        httpd = _Server((host, port), self._make_handler())
        print(f"Serving resume at http://{host}:{port}  (Ctrl+C to stop)", flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")
