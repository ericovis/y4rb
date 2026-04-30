import warnings
from pathlib import Path

import pytest

from y4rb.renderer import _strip_root_selectors, render


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


def test_strip_root_selectors_removes_body() -> None:
    css = "body { color: red; }\np { margin: 0; }"
    with pytest.warns(UserWarning, match="'body'"):
        result = _strip_root_selectors(css)
    assert "body" not in result
    assert "p { margin: 0; }" in result


def test_strip_root_selectors_removes_html() -> None:
    css = "html { box-sizing: border-box; }\np { margin: 0; }"
    with pytest.warns(UserWarning, match="'html'"):
        result = _strip_root_selectors(css)
    assert "html" not in result
    assert "p { margin: 0; }" in result


def test_strip_root_selectors_removes_both() -> None:
    css = "html { box-sizing: border-box; }\nbody { font-size: 14px; }\np { margin: 0; }"
    with pytest.warns(UserWarning):
        result = _strip_root_selectors(css)
    assert "html" not in result
    assert "body" not in result
    assert "p { margin: 0; }" in result


def test_strip_root_selectors_no_warning_when_clean() -> None:
    css = "#resume { font-size: 14px; }\np { margin: 0; }"
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        result = _strip_root_selectors(css)
    assert result == css


def test_strip_root_selectors_ignores_class_and_element_prefixes() -> None:
    css = ".body { color: red; }\ntbody { border: none; }"
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        result = _strip_root_selectors(css)
    assert result == css


def test_render_wraps_content_in_resume_div(resume_file: Path, template_file: Path) -> None:
    html = render(resume_file, template_file)
    assert '<div id="resume">' in html
