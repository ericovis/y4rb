import shutil
from pathlib import Path

import pytest

_FIXTURE_DIR = Path(__file__).parent.parent / "y4rb" / "defaults"


@pytest.fixture
def resume_file() -> Path:
    return _FIXTURE_DIR / "resume.yml"


@pytest.fixture
def template_file() -> Path:
    return _FIXTURE_DIR / "template" / "resume.j2.html"


@pytest.fixture
def style_file() -> Path:
    return _FIXTURE_DIR / "template" / "style.css"


@pytest.fixture
def head_file() -> Path:
    return _FIXTURE_DIR / "template" / "head.j2.html"


@pytest.fixture
def config_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Temp dir populated from the resume fixture folder, set as CWD."""
    shutil.copy(_FIXTURE_DIR / "resume.yml", tmp_path / "resume.yml")
    (tmp_path / "template").mkdir()
    shutil.copy(
        _FIXTURE_DIR / "template" / "resume.j2.html",
        tmp_path / "template" / "resume.j2.html",
    )
    shutil.copy(
        _FIXTURE_DIR / "template" / "head.j2.html",
        tmp_path / "template" / "head.j2.html",
    )
    shutil.copy(
        _FIXTURE_DIR / "template" / "style.css",
        tmp_path / "template" / "style.css",
    )
    monkeypatch.chdir(tmp_path)
    return tmp_path
