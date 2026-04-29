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


def test_extends_base_with_head_block(resume_file: Path, tmp_path: Path) -> None:
    template = tmp_path / "template.html"
    template.write_text(
        '{% block head %}<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter">{% endblock %}'
        "{% block content %}<p>{{ resume.name }}</p>{% endblock %}"
    )
    html = render(resume_file, template)
    assert "<!DOCTYPE html>" in html
    assert "fonts.googleapis.com" in html
    assert "Joseph Klimber" in html
