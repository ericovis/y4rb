from pathlib import Path

from y4rb.renderer import render


def test_renders_name_and_title(resume_file: Path, template_file: Path) -> None:
    html = render(resume_file, template_file)
    assert "Jane Doe" in html
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


def test_head_file_overrides_default_head(resume_file: Path, tmp_path: Path) -> None:
    template = tmp_path / "resume.j2.html"
    template.write_text("{% block content %}<p>{{ resume.name }}</p>{% endblock %}")
    head = tmp_path / "head.j2.html"
    head.write_text('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter">')
    html = render(resume_file, template)
    assert "<!DOCTYPE html>" in html
    assert "fonts.googleapis.com" in html
    assert "Jane Doe" in html
