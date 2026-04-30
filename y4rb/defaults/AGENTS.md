# y4rb Resume Project

This directory is a **y4rb** resume project. y4rb builds professional résumés from YAML data and an HTML/CSS template.

## Directory Structure

```
resume.yml          — master resume data (edit this to update your resume)
tailored/           — job-specific resume variants (complete YAML files)
template/
  resume.j2.html    — Jinja2 HTML template defining the resume layout
  head.j2.html      — <head> content: title, fonts, meta tags
  style.css         — stylesheet
AGENTS.md           — this file
CLAUDE.md           — symlink to AGENTS.md
```

## Resume Data Schema

`resume.yml` (and any file in `tailored/`) follows this structure:

```yaml
name: string                   # Full name
title: string                  # Job title / headline
email: string
phone: string
location: string
links:
  - label: string              # Display text
    url: string                # Full URL
summary: string                # 2–4 sentence career summary

experience:
  - company: string
    title: string              # Role title
    location: string
    start: string              # e.g. "Jan 2021"
    end: string                # e.g. "Present"
    highlights:
      - string                 # One achievement per bullet

education:
  - institution: string
    degree: string
    start: string | int        # e.g. 2012
    end: string | int

skills:
  Category: "item1, item2, item3"   # Key is category label
```

All top-level fields are optional — omitting a section removes it from the rendered resume.

## Creating a Tailored Resume

To create a resume tailored to a specific job:

1. Copy `resume.yml` to `tailored/<company>-<role>.yml`
2. Edit the copy — rewrite `summary`, adjust `title`, reorder `experience` highlights to emphasize relevant work
3. Preview: `y4rb preview --resume tailored/<company>-<role>.yml`
4. Export PDF: `y4rb render --resume tailored/<company>-<role>.yml --output <company>-<role>.pdf`

Keep `resume.yml` as the comprehensive master. Each tailored file is a **complete, standalone** YAML — copy the full contents and selectively rewrite rather than leaving fields empty.

## CLI Commands

```bash
# Live preview in browser (hot-reload on file changes)
y4rb preview

# Preview a specific resume variant
y4rb preview --resume tailored/acme-corp-backend.yml

# Render to PDF
y4rb render --output resume.pdf

# Render a specific variant
y4rb render --resume tailored/acme-corp-backend.yml --output acme-corp.pdf

# Preview from a different directory
y4rb preview --dir /path/to/project
```

## Style Authoring Guidelines

All resume content is wrapped in `<div id="resume">`. This is the correct target for any styles that would normally go on `body` or `html`.

**Rules:**
- Never use `body { ... }` or `html { ... }` as selectors — they are automatically stripped at render time and a warning is issued
- Use `#resume { ... }` for document-level typography (font, size, line-height, color)
- **Background color belongs in `@page { ... }`, not on `#resume` or any element selector**
- Use specific element or class selectors for everything else

**Why:** In preview mode, pagedjs takes over `<body>` and injects its own class structure. Styles on `body` escape the page boundary and break the preview layout. `#resume` exists in both preview and PDF output, so it is always safe. Background color set on an element (even `#resume`) bleeds into the outer chrome in preview mode — pagedjs reads `@page` to style the page sheet, which is the correct and consistent target for both preview and PDF.

**Example — correct:**
```css
@page {
  size: A4;
  margin: 1cm;
  background-color: #fff;  /* page background goes here */
}

#resume {
  font-family: "Georgia", serif;
  font-size: 14px;
  line-height: 1.5;
  color: #1a1a1a;
  /* no background-color here */
}
```

**Example — will cause preview/PDF mismatch:**
```css
#resume {
  background-color: #fff; /* wrong — use @page instead */
}
```

**Example — will be stripped with a warning:**
```css
body {
  font-family: "Georgia", serif; /* ignored */
}
```

## Template Customization

- **Layout:** edit `template/resume.j2.html` — it's a [Jinja2](https://jinja.palletsprojects.com/) template; resume data is available as `{{ resume.field }}`
- **Fonts / meta:** edit `template/head.j2.html` — plain HTML injected into `<head>`, use it for Google Fonts or viewport tweaks
- **Styles:** edit `template/style.css` — standard CSS, inlined at render time

## Agent Workflow

When asked to tailor a resume for a specific job:

1. Read `resume.yml` to understand the candidate's full background
2. Identify which experience bullets, skills, and summary phrases best match the target role
3. Create `tailored/<company>-<role>.yml` as a full copy with targeted rewrites
4. Do not hallucinate experience or credentials — only rephrase and reorder what exists
