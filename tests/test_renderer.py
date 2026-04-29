from pathlib import Path

from y4rb.renderer import render


def test_renders_name_and_title(resume_file: Path, template_file: Path) -> None:
    html = render(resume_file, template_file)
    assert "Joseph Klimber" in html
    assert "Senior Software Engineer" in html


def test_renders_contact_info(resume_file: Path, template_file: Path) -> None:
    html = render(resume_file, template_file)
    assert "jane.doe@example.com" in html
    assert "San Francisco, CA" in html


def test_renders_experience(resume_file: Path, template_file: Path) -> None:
    html = render(resume_file, template_file)
    assert "Acme Corp" in html
    assert "BuildFast Inc" in html


def test_renders_skills(resume_file: Path, template_file: Path) -> None:
    html = render(resume_file, template_file)
    assert "Python" in html
    assert "Kubernetes" in html


def test_inlines_style(resume_file: Path, template_file: Path, style_file: Path) -> None:
    html = render(resume_file, template_file, style=style_file)
    assert "<style>" in html


def test_no_style_tag_without_css(resume_file: Path, template_file: Path) -> None:
    html = render(resume_file, template_file)
    assert "<style>" not in html
