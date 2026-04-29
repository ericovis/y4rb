from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

_PROJECT_ROOT = Path(__file__).parent.parent


@pytest.fixture(scope="session")
def built_binary(tmp_path_factory: pytest.TempPathFactory) -> Path:
    dist_dir = tmp_path_factory.mktemp("dist")
    work_dir = tmp_path_factory.mktemp("work")
    subprocess.run(
        [
            str(_PROJECT_ROOT / "bin" / "run"),
            "pyinstaller",
            "y4rb.spec",
            "--noconfirm",
            "--distpath",
            str(dist_dir),
            "--workpath",
            str(work_dir),
        ],
        check=True,
        cwd=_PROJECT_ROOT,
    )
    return dist_dir / "y4rb"


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
    assert (tmp_path / "template.html").exists()
    assert (tmp_path / "style.css").exists()
    assert "Created resume.yml" in result.stdout
    assert "Created template.html" in result.stdout
    assert "Created style.css" in result.stdout


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
