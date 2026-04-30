# Getting Started

## Installation

**Via pip:**

```bash
pip install y4rb
```

**Standalone binary** (no Python required): download the binary for your platform from the [Releases](https://github.com/ericovis/y4rb/releases) page and place it somewhere on your `PATH`.

After downloading, verify the SHA256 hash against `checksums.sha256` in the same release.

## Create a resume project

```bash
y4rb init my-resume
cd my-resume
```

This creates the following layout:

```
resume.yml          — your resume data
tailored/           — job-specific variants
template/
  resume.j2.html    — Jinja2 HTML layout
  head.j2.html      — <head> content (fonts, meta)
  style.css         — stylesheet
AGENTS.md           — AI agent instructions
```

## Edit your resume

Open `resume.yml` and fill in your details:

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
  Experienced software engineer specialising in distributed systems
  and developer tooling.

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

All top-level fields are optional — omitting a section removes it from the rendered output.

## Preview

```bash
y4rb preview
```

Opens a live-reload browser preview at `http://localhost:8080`. Changes to `resume.yml`, the template, or the stylesheet are reflected immediately without refreshing.

Use `--port` to change the port:

```bash
y4rb preview --port 3000
```

## Export to PDF

```bash
y4rb render --output resume.pdf
```

## Tailored variants

To target a specific job, copy your master resume and adjust the copy:

```bash
cp resume.yml tailored/acme-backend.yml
# edit tailored/acme-backend.yml
y4rb preview --resume tailored/acme-backend.yml
y4rb render --resume tailored/acme-backend.yml --output acme-backend.pdf
```

Keep `resume.yml` as the comprehensive master. Each tailored file should be a complete standalone YAML.
