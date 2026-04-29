from __future__ import annotations

import http.client
import queue
import threading
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

from y4rb.server import ResumeServer


@pytest.fixture
def resume_server(config_dir: Path) -> ResumeServer:
    from y4rb.config import resolve_config
    return ResumeServer(resolve_config())


@pytest.fixture
def live_server(resume_server: ResumeServer):
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), resume_server._make_handler())
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{port}"
    httpd.shutdown()


def test_rebuild_produces_html(resume_server: ResumeServer) -> None:
    assert "<!DOCTYPE html>" in resume_server._html
    assert "Jane Doe" in resume_server._html


def test_rebuild_includes_reload_script(resume_server: ResumeServer) -> None:
    assert "EventSource" in resume_server._html


def test_broadcast_sends_reload_to_all_clients(resume_server: ResumeServer) -> None:
    q1: queue.Queue[str] = queue.Queue()
    q2: queue.Queue[str] = queue.Queue()
    resume_server._add_client(q1)
    resume_server._add_client(q2)
    resume_server._broadcast()
    assert q1.get_nowait() == "reload"
    assert q2.get_nowait() == "reload"


def test_add_client_appends_to_list(resume_server: ResumeServer) -> None:
    q: queue.Queue[str] = queue.Queue()
    resume_server._add_client(q)
    assert q in resume_server._clients


def test_remove_client_removes_from_list(resume_server: ResumeServer) -> None:
    q: queue.Queue[str] = queue.Queue()
    resume_server._add_client(q)
    resume_server._remove_client(q)
    assert q not in resume_server._clients


def test_remove_nonexistent_client_is_safe(resume_server: ResumeServer) -> None:
    q: queue.Queue[str] = queue.Queue()
    resume_server._remove_client(q)


def test_get_root_returns_200(live_server: str) -> None:
    with urllib.request.urlopen(live_server + "/") as resp:
        assert resp.status == 200
        body = resp.read().decode()
    assert "Jane Doe" in body


def test_get_root_content_type_is_html(live_server: str) -> None:
    with urllib.request.urlopen(live_server + "/") as resp:
        assert "text/html" in resp.headers.get("Content-Type", "")


def test_get_unknown_path_returns_404(live_server: str) -> None:
    host_port = live_server.removeprefix("http://")
    host, port_str = host_port.rsplit(":", 1)
    conn = http.client.HTTPConnection(host, int(port_str), timeout=5)
    conn.request("GET", "/notfound")
    resp = conn.getresponse()
    assert resp.status == 404
    conn.close()


def test_get_events_returns_sse_headers(live_server: str) -> None:
    host_port = live_server.removeprefix("http://")
    host, port_str = host_port.rsplit(":", 1)
    conn = http.client.HTTPConnection(host, int(port_str), timeout=5)
    conn.request("GET", "/events")
    resp = conn.getresponse()
    assert resp.status == 200
    assert "text/event-stream" in (resp.getheader("Content-Type") or "")
    conn.close()
