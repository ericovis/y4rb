from pathlib import Path

from y4rb.renderer import render


def test_renders_simple_fields(tmp_path: Path) -> None:
    (tmp_path / "resume.yaml").write_text("name: Jane Doe\ntitle: Engineer\n")
    (tmp_path / "template.html").write_text(
        "<h1>{{ resume.name }}</h1><p>{{ resume.title }}</p>"
    )

    html = render(tmp_path / "resume.yaml", tmp_path / "template.html")

    assert "<h1>Jane Doe</h1>" in html
    assert "<p>Engineer</p>" in html


def test_renders_nested_data(tmp_path: Path) -> None:
    (tmp_path / "resume.yaml").write_text("contact:\n  email: jane@example.com\n")
    (tmp_path / "template.html").write_text("<p>{{ resume.contact.email }}</p>")

    html = render(tmp_path / "resume.yaml", tmp_path / "template.html")

    assert "jane@example.com" in html


def test_renders_list_data(tmp_path: Path) -> None:
    (tmp_path / "resume.yaml").write_text(
        "skills:\n  - Python\n  - Go\n"
    )
    (tmp_path / "template.html").write_text(
        "{% for s in resume.skills %}<li>{{ s }}</li>{% endfor %}"
    )

    html = render(tmp_path / "resume.yaml", tmp_path / "template.html")

    assert "<li>Python</li>" in html
    assert "<li>Go</li>" in html
