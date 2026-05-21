# Copilot Instructions for Dance On Time

## Project Overview

**Dance On Time** is a Jekyll-based webpage hosted on GitHub Pages. It serves as a landing page for a dance studio with sections for Home, About Us, Classes, Schedule, and Contact Us. The design prioritizes clean, modern aesthetics with accessibility in mind.

**Hosting & Domain:**
- Hosted on GitHub Pages (static site generator)
- Domain: danceontime.com (registered with Cloudflare DNS)
- No server-side runtime or backend services

## Architecture

### Tech Stack
- **Static Site Generator**: Jekyll (Ruby-based, v4.3+)
- **Hosting**: GitHub Pages (automatic deployment from repository)
- **Theme**: Serif Jekyll Theme (Bootstrap 5-based)
- **Styling**: Bootstrap 5 CSS framework (via CDN) + SCSS customization structure
- **Scripting**: Bootstrap's built-in JavaScript + Vanilla JavaScript

**Serif Theme Demo & Documentation:**
- Live Demo: https://jekyll-serif.netlify.app/
- Responsive, professional business theme with modern Bootstrap styling
- Includes navbar, footer, card layouts, and responsive grid system

### Directory Structure (Jekyll Standard with Serif Theme)
```
danceontime/
├── _config.yml           # Jekyll configuration
├── _layouts/
│   └── default.html      # Main layout (Bootstrap-based)
├── _includes/            # Reusable HTML partials
├── _sass/
│   ├── components/       # Custom SCSS component overrides
│   │   ├── _buttons.scss
│   │   ├── _header.scss
│   │   ├── _footer.scss
│   │   ├── _main-menu.scss
│   │   ├── _content.scss
│   │   ├── _type.scss
│   │   └── _page.scss
│   └── bootstrap/        # Bootstrap SCSS files (imported from gem)
├── assets/
│   ├── css/style.scss    # Main SCSS entry point
│   ├── images/
│   ├── fonts/
│   └── js/
├── index.md              # Homepage
├── about.md              # About Us section
├── contact.md            # Contact Us section
├── services/             # Services section (multiple pages)
├── waivers/              # Waivers section (multiple pages)
├── _old_content/         # Backup of content before theme migration
└── _site/                # Generated output (do not edit)
```

## Development Workflow

### Local Setup & Testing
```bash
# Install Ruby dependencies (one-time setup)
bundle install

# Serve locally with live reload (Docker)
docker-compose up

# Visit http://localhost:4000 to view changes in real-time
```

**Requirements:**
- Ruby 3.2+ (for Bootstrap 5 SCSS support)
- RubyGems and Bundler
- Docker & Docker Compose (for consistent environment) OR
- GCC and Make (development tools for local Ruby setup)

### Build & Deploy
- **Automatic**: Push to GitHub main branch → GitHub Pages builds and deploys automatically
- **Local Build**: Run `docker-compose exec jekyll bundle exec jekyll build` to generate `_site/` folder
- **Live Reload**: Enabled during Docker development for instant preview of changes

### Styling & Theme Customization

The Serif theme uses Bootstrap 5 for styling:
- **Bootstrap CSS**: Currently loaded via CDN (`https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css`)
- **Custom SCSS**: Add overrides in `_sass/components/` files (currently using Bootstrap defaults)
- **SCSS Structure**: Main entry point is `assets/css/style.scss` which imports Bootstrap and component partials

To customize theme colors or styles:
1. Edit files in `_sass/components/` (e.g., `_header.scss`, `_footer.scss`)
2. Add custom variables to `_sass/bootstrap/_variables.scss` if needed
3. Rebuild with `docker-compose restart` to see changes

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
- CSS: `assets/css/style.scss` (SCSS entry point, compiled to CSS in base layout)
- Images: `assets/images/` (reference as `/assets/images/filename.jpg`)
- JavaScript: `assets/js/` (Bootstrap JS bundle included via CDN)

## Integration & Dependencies

### External Resources
- **Bootstrap CSS & JS**: Loaded via CDN for quick setup
- **Fonts**: System fonts or self-hosted only
- **Icons**: SVG inline or Bootstrap Icons if needed
- **Forms**: Consider using Formspree, Basin, or email-based solutions (GitHub Pages is static)

### Gems & Packages
- **Ruby Gems**: Bootstrap 5, Jekyll 4.3+ (specified in Gemfile)
- **No NPM Packages**: Use only native HTML, CSS, and JavaScript
- **No build tools**: Jekyll handles all site generation automatically

## Critical Rules for Copilot

1. **Never add NPM dependencies** - Confirm with user before any package addition
2. **Bootstrap is approved** - Serif theme uses Bootstrap 5 CSS framework
3. **Use Bootstrap classes** - For layout and styling (navbar, container, row, col, etc.)
4. **Markdown for content** - Use .md files with YAML Front Matter
5. **Jekyll Liquid only** - No other template languages
6. **Reference _config.yml** - For site-wide settings (title, description, etc.)
7. **No custom CSS unless necessary** - Bootstrap defaults are professional and complete

## Common Tasks

### Add a New Page
1. Create `page-name.md` in root
2. Add YAML Front Matter with title, layout, permalink
3. Write content in Markdown below Front Matter

### Update Navigation
- Edit `_layouts/default.html` navbar section
- Reference new pages via their `permalink` values

### Change Site Title/Description
- Edit `_config.yml` (accessed via `{{ site.title }}` in templates)

### Customize Colors/Styles
- Edit component files in `_sass/components/` (e.g., `_header.scss`)
- Add Bootstrap color variables or custom SCSS
- Rebuild with `docker-compose restart`

### Add Contact Form
- Use external service (Formspree, etc.) since GitHub Pages is static
- Form action points to external endpoint

## Deployment Notes

- GitHub Pages automatically builds Jekyll and deploys from main branch
- Changes to main branch appear live within minutes
- Check GitHub Pages settings: Settings → Pages → Source should be "GitHub Actions"

---

**Last Updated**: May 21, 2026 | Jekyll 4.3+ with Serif Theme (Bootstrap 5) on GitHub Pages
