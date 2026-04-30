# personal website

a small corner of the internet — research, code, recipes, thoughts.
built with [astro](https://astro.build) + [tailwind css](https://tailwindcss.com).

## running locally

```bash
npm install      # first time only
npm run dev      # dev server on http://localhost:4321
npm run build    # production build into ./dist
npm run preview  # preview the production build locally
```

## adding content

new post (recipe, thought, note)
→ create `src/content/posts/your-slug.md` with frontmatter:

```yaml
---
title: your title
description: one-line teaser
date: 2026-05-01
emoji: 🥐
tags: [recipe]   # recipe | thought | project | art | code
---
```

new project
→ create `src/content/projects/your-slug.md` with the matching frontmatter
(see existing projects for the schema).

new gallery image
→ drop into `public/gallery/`, add an entry in `src/pages/gallery.astro`.

## structure

```
src/
├── content/
│   ├── posts/         # markdown posts
│   └── projects/      # markdown projects
├── components/        # header, footer, cards, tags
├── layouts/           # BaseLayout, PostLayout
├── pages/             # routed pages
├── styles/global.css  # design tokens & prose styles
└── content.config.ts  # collection schemas

public/                # static assets (favicon, images, cv.pdf)
```

## design tokens

all colors and fonts live in `src/styles/global.css` under the `@theme` block.
edit there to retune the palette site-wide.
