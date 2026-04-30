from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

_PROJECT_ROOT = Path(__file__).parent.parent


@pytest.fixture(scope="session")
def built_binary() -> Path:
    build_script = _PROJECT_ROOT / "bin" / "build"
    cmd = ["bash", str(build_script)] if sys.platform == "win32" else [str(build_script)]
    subprocess.run(cmd, check=True, cwd=_PROJECT_ROOT)
    name = "y4rb.exe" if sys.platform == "win32" else "y4rb"
    return _PROJECT_ROOT / "dist" / name


def test_binary_help(built_binary: Path) -> None:
    result = subprocess.run([str(built_binary), "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "init" in result.stdout
    assert "render" in result.stdout
    assert "preview" in result.stdout


def test_binary_init(built_binary: Path, tmp_path: Path) -> None:
    result = subprocess.run(
        [str(built_binary), "init"],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    assert result.returncode == 0
    assert (tmp_path / "resume.yml").exists()
    assert (tmp_path / "template" / "resume.j2.html").exists()
    assert (tmp_path / "template" / "style.css").exists()
    assert (tmp_path / "template" / "head.j2.html").exists()
    assert (tmp_path / "tailored").is_dir()
    assert (tmp_path / "AGENTS.md").exists()
    assert (tmp_path / "CLAUDE.md").is_symlink()
    assert "Created resume.yml" in result.stdout
    assert "Created template/resume.j2.html" in result.stdout


def test_binary_render(built_binary: Path, tmp_path: Path) -> None:
    subprocess.run([str(built_binary), "init"], check=True, cwd=tmp_path)
    output = tmp_path / "resume.pdf"
    result = subprocess.run(
        [str(built_binary), "render", "--output", str(output)],
        capture_output=True,
        text=True,
        cwd=tmp_path,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr
    assert output.exists()
    assert output.read_bytes().startswith(b"%PDF")
