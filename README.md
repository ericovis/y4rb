# y4rb — Yet Another Resumé Builder

Resume builder that turns a YAML file and an HTML/CSS template into a PDF. You own the design — y4rb connects the data to the template and handles rendering.

## Install

```bash
pip install y4rb
```

Or download a standalone binary (no Python required) from [Releases](https://github.com/ericovis/y4rb/releases). Verify the download against `checksums.sha256` in the same release.

## Quick start

```bash
y4rb init my-resume
cd my-resume
y4rb preview        # live-reload browser preview at localhost:8080
y4rb render         # export resume.pdf
```

## Resume data

Edit `resume.yml` in your project:

```yaml
name: Jane Smith
title: Senior Software Engineer
email: jane@example.com
phone: "+1 555 000 0000"
location: San Francisco, CA
links:
  - label: GitHub
    url: https://github.com/janesmith

summary: >
  Experienced engineer specialising in distributed systems and developer tooling.

experience:
  - company: Acme Corp
    title: Senior Engineer
    location: San Francisco, CA
    start: Jan 2021
    end: Present
    highlights:
      - Reduced p99 API latency by 40% through query optimisation
      - Led migration of monolith to microservices

education:
  - institution: State University
    degree: B.Sc. Computer Science
    start: 2014
    end: 2018

skills:
  Languages: "Python, Go, TypeScript"
  Infrastructure: "Kubernetes, Terraform, AWS"
```

All top-level fields are optional.

## Tailored variants

Keep a master `resume.yml` and job-specific copies in `tailored/`:

```bash
cp resume.yml tailored/acme-backend.yml
# edit the copy
y4rb preview --resume tailored/acme-backend.yml
y4rb render  --resume tailored/acme-backend.yml --output acme-backend.pdf
```

## CLI

| Command | Description |
|---|---|
| `y4rb init [dir]` | Scaffold a new resume project |
| `y4rb preview` | Live-reload browser preview (default port 8080) |
| `y4rb render` | Export to PDF (default `resume.pdf`) |

All commands accept `--dir`/`-d` to point at a project directory and `--resume`/`-r` to select a YAML file.

## Template

The generated project includes a ready-to-use template. To customise:

- **Layout** — edit `template/resume.j2.html` (Jinja2; resume data available as `{{ resume.field }}`)
- **Styles** — edit `template/style.css` (inlined at render time)
- **Head** — edit `template/head.j2.html` for fonts, meta tags, etc.

## License

MIT
