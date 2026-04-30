# y4rb — Yet Another Resumé Builder

**y4rb** is a resume builder that turns a YAML file and an HTML/CSS template into a polished PDF. You own the design — y4rb just connects the data to the template and handles rendering.

## How it works

- **YAML** holds your resume data (name, experience, skills, etc.)
- **HTML + CSS** defines the visual layout
- **y4rb** renders the template with your data and exports a pixel-perfect PDF via headless Chromium

## Quick start

```bash
# Install
pip install y4rb

# Scaffold a new project
y4rb init my-resume
cd my-resume

# Live preview in browser
y4rb preview

# Export to PDF
y4rb render --output resume.pdf
```

## Features

- Live-reload browser preview — edits to YAML, template, or CSS reflect instantly
- Multiple resume variants from one project — keep a master `resume.yml` and job-specific copies in `tailored/`
- Standalone binary — no Python required on the target machine (download from [Releases](https://github.com/ericovis/y4rb/releases))
- pip installable — `pip install y4rb`
