# Copilot Instructions for Dance On Time

## Project Overview

**Dance On Time** is a Jekyll-based webpage hosted on GitHub Pages. It serves as a landing page for a dance studio with sections for Home, About Us, Classes, Schedule, and Contact Us. The design prioritizes clean, modern aesthetics with accessibility in mind.

**Hosting & Domain:**
- Hosted on GitHub Pages (static site generator)
- Domain: danceontime.com (registered with Cloudflare DNS)
- No server-side runtime or backend services

## Architecture

### Tech Stack
- **Static Site Generator**: Jekyll (Ruby-based)
- **Hosting**: GitHub Pages (automatic deployment from repository)
- **Styling**: CSS only (no frameworks or preprocessors unless explicitly requested)
- **Scripting**: Vanilla JavaScript only

### Directory Structure (Jekyll Standard)
```
danceontime/
├── _config.yml           # Jekyll configuration
├── _layouts/             # HTML templates (base, page, etc.)
├── _includes/            # Reusable HTML partials
├── assets/               # CSS, images, fonts
│   ├── css/
│   ├── images/
│   └── js/
├── index.md              # Homepage
├── about.md              # About Us section
├── classes.md            # Classes section
├── schedule.md           # Schedule section
├── contact.md            # Contact Us section
└── _site/                # Generated output (do not edit)
```

## Development Workflow

### Local Setup & Testing
```bash
# Install Ruby dependencies (one-time setup)
bundle install

# Serve locally with live reload
bundle exec jekyll serve --livereload

# Visit http://localhost:4000 to view changes in real-time
```

**Requirements:**
- Ruby 2.7.0 or higher
- RubyGems and Bundler
- GCC and Make (development tools)

### Build & Deploy
- Automatic: Push to GitHub main branch → GitHub Actions builds and deploys
- Manual: Run `bundle exec jekyll build` to generate `_site/` folder

## Code Conventions & Patterns

### Page Creation
- Use Markdown files (.md) in root or subdirectories
- Include YAML Front Matter for metadata:
  ```yaml
  ---
  layout: page
  title: Class Schedule
  permalink: /schedule/
  ---
  ```
- Layout files in `_layouts/` use Liquid templating syntax

### Liquid Templating (Jekyll Template Language)
```liquid
<!-- Use for dynamic content -->
{{ site.title }}          <!-- From _config.yml -->
{% for item in site.data %} <!-- Loop over data -->
  {{ item.name }}
{% endfor %}
```

### Asset Organization
- CSS: `assets/css/style.css` (included in base layout)
- Images: `assets/images/` (reference as `/assets/images/filename.jpg`)
- JavaScript: `assets/js/` (minimal, inline if under 1KB)

### Styling Constraints
- No CSS frameworks (Bootstrap, Tailwind, etc.)
- CSS-only solutions for responsive design (media queries, flexbox, grid)
- Inline critical CSS in `_layouts/default.html` for performance

## Integration & Dependencies

### External Resources (If Needed)
- **Fonts**: System fonts or self-hosted only
- **Icons**: SVG inline or minimal icon sets
- **Forms**: Consider using Formspree, Basin, or email-based solutions (GitHub Pages is static)

### No NPM Packages
- Use only native HTML, CSS, and JavaScript
- No build tools (Webpack, Gulp, Vite, etc.)
- Jekyll handles all site generation automatically

## Critical Rules for Copilot

1. **Never add NPM dependencies** - Confirm with user before any package addition
2. **HTML, CSS, JavaScript only** - No frontend frameworks
3. **No special characters or emojis** - Use plain text and Unicode safely
4. **Minimalist code** - Clean, readable, no unnecessary complexity
5. **Markdown for content** - Use .md files with YAML Front Matter
6. **Jekyll Liquid only** - No other template languages
7. **Reference _config.yml** - For site-wide settings (title, description, etc.)

## Common Tasks

### Add a New Page
1. Create `page-name.md` in root
2. Add YAML Front Matter with title, layout, permalink
3. Write content in Markdown below Front Matter

### Update Navigation
- Edit `_includes/nav.html` or equivalent
- Reference new pages via their `permalink` values

### Change Site Title/Description
- Edit `_config.yml` (accessed via `{{ site.title }}` in templates)

### Add Contact Form
- Use external service (Formspree, etc.) since GitHub Pages is static
- Form action points to external endpoint

## Deployment Notes

- GitHub Actions automatically builds Jekyll and deploys to `gh-pages` branch
- Changes to main branch appear live within minutes
- Check GitHub Pages settings: Settings → Pages → Source should be "GitHub Actions"

---

**Last Updated**: May 20, 2026 | Pure Jekyll + GitHub Pages static site
