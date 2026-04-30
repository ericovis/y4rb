# Styling

y4rb gives you full control over the look of your resume through two files in your project's `template/` directory:

| File | Purpose |
|---|---|
| `template/style.css` | All visual styling — typography, layout, colours, spacing |
| `template/head.j2.html` | `<head>` content — fonts loaded via `<link>` or `@font-face`, meta tags, page title |

## How the HTML is structured

When y4rb renders your resume it wraps your template inside a fixed scaffold provided by `_base.html`. You never edit this file directly — it is the engine that handles the page, styles, live-reload, and PDF layout:

```
<html>
  <head>
    <!-- head.j2.html is included here -->
    <!-- style.css is inlined here -->
    <!-- pagedjs polyfill (preview only) -->
  </head>
  <body>
    <div id="resume">
      <!-- your resume.j2.html content goes here -->
    </div>
  </body>
</html>
```

Your `resume.j2.html` only provides the **content block** — the markup inside `#resume`. The `<html>`, `<head>`, and `<body>` tags are part of the scaffold and cannot be changed from your template.

### What this means for CSS

Because your content lives inside `<div id="resume">`, any `html` or `body` rules you write in `style.css` will be **silently stripped** at render time and a warning will be printed. This prevents your rules from conflicting with the page scaffold.

Use these selectors instead:

| Instead of | Use |
|---|---|
| `body { font-family: ... }` | `#resume { font-family: ... }` |
| `body { color: ... }` | `#resume { color: ... }` |
| `html { background: ... }` | `@page { background-color: ... }` |

## Styling the resume page with `@page`

Page dimensions, margins, and background colour are controlled with the CSS [`@page`](https://developer.mozilla.org/en-US/docs/Web/CSS/@page) at-rule. This is the correct place for anything that affects the printed page itself rather than the resume content.

The default template ships with:

```css
@page {
    size: A4;
    margin: 1cm;
    background-color: #fff;
}

@page:first {
    margin-top: 2cm;
}
```

### `@page` examples

**Letter size with generous margins:**

```css
@page {
    size: letter;
    margin: 2cm 2.5cm;
    background-color: #fff;
}
```

**A4 landscape:**

```css
@page {
    size: A4 landscape;
    margin: 1.5cm 2cm;
}
```

**Coloured page background:**

```css
@page {
    size: A4;
    margin: 1cm;
    background-color: #f8f6f2;
}
```

**Different top margin on the first page only:**

```css
@page {
    size: A4;
    margin: 1cm;
}

@page:first {
    margin-top: 3cm;
}
```

**Custom page size (e.g. square):**

```css
@page {
    size: 148mm 148mm;
    margin: 1cm;
}
```

See the full list of supported descriptors in the [MDN `@page` reference](https://developer.mozilla.org/en-US/docs/Web/CSS/@page).

## Styling the resume content with `#resume`

Everything inside the resume wrapper is styled through `#resume` and its descendants. This is where you control the base font, size, line height, and colour:

```css
#resume {
    font-family: "Inter", sans-serif;
    font-size: 13px;
    line-height: 1.6;
    color: #1a1a1a;
}
```

## Using custom fonts

### Google Fonts (recommended for most cases)

Add a `<link>` tag to `template/head.j2.html`, then reference the font family in `style.css`.

**`template/head.j2.html`:**

```html
<title>{{ resume.name }} — Resumé</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet" />
```

**`template/style.css`:**

```css
#resume {
    font-family: "Inter", sans-serif;
}
```

You can mix multiple families — one for headings and one for body text:

**`template/head.j2.html`:**

```html
<title>{{ resume.name }} — Resumé</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet" />
```

**`template/style.css`:**

```css
#resume {
    font-family: "Source Sans 3", sans-serif;
    font-size: 13px;
}

h1, h2 {
    font-family: "Playfair Display", serif;
}
```

### Local font files with `@font-face`

If you have font files in your project (e.g. inside `template/fonts/`), declare them with `@font-face` directly in `style.css`. Paths are relative to `style.css`.

```css
@font-face {
    font-family: "MyFont";
    src: url("fonts/MyFont-Regular.woff2") format("woff2");
    font-weight: 400;
    font-style: normal;
}

@font-face {
    font-family: "MyFont";
    src: url("fonts/MyFont-Bold.woff2") format("woff2");
    font-weight: 700;
    font-style: normal;
}

#resume {
    font-family: "MyFont", sans-serif;
}
```

### Embedding a font inline (self-contained PDF)

To produce a PDF that carries the font inside it without relying on external files, base64-encode the font and embed it directly in the `@font-face` declaration:

```css
@font-face {
    font-family: "MyFont";
    src: url("data:font/woff2;base64,<BASE64_STRING_HERE>") format("woff2");
    font-weight: 400;
    font-style: normal;
}
```

Generate the base64 string with:

```bash
base64 -i MyFont-Regular.woff2 | tr -d '\n'
```

Then paste the output in place of `<BASE64_STRING_HERE>`.

### System fonts (no external dependencies)

Use a system font stack when you want zero external dependencies and consistent results across machines:

```css
#resume {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}
```

Or a classic serif stack:

```css
#resume {
    font-family: Georgia, "Times New Roman", Times, serif;
}
```
