# Dance On Time - Jekyll Site

A professional, multi-service celebration platform for dance instruction, DJ services, and custom portable dance floors. Built with Jekyll and hosted on GitHub Pages.

**GitHub Repository:** `git@github.com:rfair404/danceontime.com.git`

**Website:** https://danceontime.com

## Quick Start with Docker

No need to install Ruby or Bundler locally. Everything runs in Docker.

### Prerequisites
- Docker and Docker Compose installed

### Development

Start the Jekyll development server:
```bash
docker-compose up
```

Visit `http://localhost:4000` to see your site. Changes are automatically reloaded.

### Build Commands

**Generate static site:**
```bash
docker-compose run --rm jekyll bundle exec jekyll build
```

**Access the shell inside the container:**
```bash
docker-compose run --rm jekyll bash
```

**Install new gems:**
```bash
docker-compose run --rm jekyll bundle add gem-name
```

**Stop the server:**
```bash
docker-compose down
```

## Project Structure

```
danceontime/
├── _config.yml           # Jekyll configuration
├── _layouts/             # HTML templates
├── _includes/            # Reusable HTML partials
├── assets/               # CSS, images, fonts
├── services/             # Service pages
│   ├── instruction.md    # Dance instruction
│   ├── dj.md             # DJ services
│   └── floor.md          # Dance floor rental
├── index.md              # Homepage
├── about.md              # About Us
├── classes.md            # Dance Lessons
├── contact.md            # Contact Us
├── docker-compose.yml    # Docker configuration
├── Dockerfile            # Docker image definition
├── Gemfile               # Ruby dependencies
└── README.md             # This file
```

## Services Offered

### Dance Instruction
Professional dance lessons specializing in:
- Country Two Step
- Waltz
- Swing
- Salsa
- Bachata

Wedding packages: 4, 6, and 8-lesson options including couples and father-of-bride dances. In-studio (Madison, GA) and in-home lessons available.

### DJ Services
Professional DJ with music curation expertise:
- Personalized playlist building with couples
- Classy, clean music (no club music or profanity)
- Room reading and all-night energy
- MC services and special moment coordination

### Custom Portable Dance Floors
Professional-grade custom-built wood dance floors:
- Modular design: 8'x12' to 48'x48'
- Perfect for any venue size
- Professional installation and removal
- Works with all dance styles

## Creating Content

### Add a New Page

Create a new `.md` file (e.g., `gallery.md`) with YAML Front Matter:

```yaml
---
layout: default
title: Gallery
permalink: /gallery/
---

Your content here...
```

### Update Navigation

Edit `_layouts/default.html` to add links to new pages.

### Customize Site Settings

Edit `_config.yml` for site title, description, and other metadata.

## Design Principles

- Clean, minimal CSS (no frameworks)
- Vanilla JavaScript only
- No external dependencies or emojis
- Responsive design with flexbox/grid
- Focus on accessibility
- Professional, classy aesthetic

## Deployment

### Automatic Deployment (GitHub Pages)
1. Push changes to the `main` branch
2. GitHub Actions automatically builds and deploys
3. Site updates appear at https://danceontime.com within minutes

### Manual Build
```bash
docker-compose run --rm jekyll bundle exec jekyll build
```

Generated static files are in the `_site/` folder.

## Git Workflow

Clone the repository:
```bash
git clone git@github.com:rfair404/danceontime.com.git
cd danceontime
```

Make changes and commit:
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

---

**Hosted on:** GitHub Pages | **Domain:** danceontime.com | **Built with:** Jekyll + Docker
