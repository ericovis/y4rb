# Working with Claude Code

`y4rb init` creates a `CLAUDE.md` file at the project root (a symlink to `AGENTS.md`). Claude Code reads it automatically when you open a session inside the project — no setup needed.

```bash
cd my-resume
claude
```

`CLAUDE.md` gives Claude the project layout, YAML schema, CSS authoring rules, and the constraint that matters most: never invent experience, only rephrase and reorder what already exists. Edit it at any time to add personal constraints or preferred phrasing.

---

## Example prompts

**Tailor for a job posting (paste description):**

```
Tailor my resume for this job and save it to tailored/acme-backend.yml.
Output a complete YAML file — do not omit any sections.

<paste job description>
```

**Tailor from a URL:**

```
Tailor my resume for the job at https://example.com/jobs/123 and save it
to tailored/acme-backend.yml. Output a complete YAML file.
```

**Rewrite the summary for a different audience:**

```
Rewrite the summary in resume.yml for a Staff Engineer role at a fintech company.
Focus on reliability, scale, and cross-functional influence. Max 4 sentences.
```

**Sharpen specific bullets:**

```
Rewrite the Acme Corp highlights in resume.yml to lead with reliability
and incident response work. Do not add anything that isn't already there.
```

**Trim for length:**

```
My resume is running long. Suggest what to remove or shorten from the skills
sections given that I'm targeting a pure backend role.
```

**Preview and export without leaving the session:**

```
Preview tailored/acme-backend.yml on port 3000, then render it to acme-backend.pdf.
```

Claude Code can run `y4rb` commands directly, so the full loop — edit YAML, preview, export — happens in one session. If you prefer to run the commands yourself:

```bash
y4rb preview --resume tailored/acme-backend.yml
y4rb render  --resume tailored/acme-backend.yml --output acme-backend.pdf
```
