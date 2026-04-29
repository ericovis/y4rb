from pathlib import Path

from y4rb.renderer import render


def test_preview_flag_includes_pagedjs(resume_file: Path, template_file: Path) -> None:
    html = render(resume_file, template_file, preview=True)
    assert "pagedjs" in html


def test_preview_flag_false_excludes_pagedjs(resume_file: Path, template_file: Path) -> None:
    html = render(resume_file, template_file, preview=False)
    assert "pagedjs" not in html


def test_reload_flag_includes_eventsource(resume_file: Path, template_file: Path) -> None:
    html = render(resume_file, template_file, reload=True)
    assert "EventSource" in html


def test_reload_flag_false_excludes_eventsource(resume_file: Path, template_file: Path) -> None:
    html = render(resume_file, template_file, reload=False)
    assert "EventSource" not in html


def test_render_title_uses_resume_name(resume_file: Path, template_file: Path) -> None:
    html = render(resume_file, template_file)
    assert "Jane Doe" in html
    assert "Resumé" in html


def test_render_escapes_html_in_data(tmp_path: Path) -> None:
    resume = tmp_path / "resume.yml"
    resume.write_text('name: "<script>alert(1)</script>"\ntitle: Test\n')
    template = tmp_path / "template.html"
    template.write_text("{% block content %}<p>{{ resume.name }}</p>{% endblock %}")
    html = render(resume, template)
    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_render_with_style_inlines_css(resume_file: Path, template_file: Path, style_file: Path) -> None:
    html = render(resume_file, template_file, style=style_file)
    assert "<style>" in html
    css_content = style_file.read_text()
    assert css_content[:20] in html
