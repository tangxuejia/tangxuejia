from __future__ import annotations

import html
import importlib.util
import json
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_site"
BASE = os.environ.get("RENOMETRIC_BASE", "")
ORIGIN = os.environ.get("RENOMETRIC_ORIGIN", "https://renometric.pages.dev")

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)

skip_top = {".git", ".github", ".netlify", "_site"}
skip_files = {"_redirects", "_headers", "netlify.toml"}

for item in ROOT.iterdir():
    if item.name in skip_top or item.name in skip_files:
        continue
    dest = OUT / item.name
    if item.is_dir():
        shutil.copytree(item, dest)
    elif item.is_file():
        shutil.copy2(item, dest)

(OUT / ".nojekyll").write_text("", encoding="utf-8")

# Adapt host-neutral source paths to the current GitHub Pages project path.
for page_path in OUT.rglob("*.html"):
    text = page_path.read_text(encoding="utf-8")
    text = text.replace("https://renometric.netlify.app", ORIGIN)
    text = text.replace("https://tangxuejia.github.io/tangxuejia", ORIGIN)
    text = re.sub(r'href="/(?!tangxuejia/)', f'href="{BASE}/', text)
    text = re.sub(r"href='/((?!tangxuejia/))", f"href='{BASE}/", text)
    text = re.sub(r'src="/(?!tangxuejia/)', f'src="{BASE}/', text)
    text = re.sub(r"src='/((?!tangxuejia/))", f"src='{BASE}/", text)
    if not BASE:
        text = text.replace('href="/tangxuejia/', 'href="/').replace("href='/tangxuejia/", "href='/").replace('src="/tangxuejia/', 'src="/').replace("src='/tangxuejia/", "src='/")
    text = text.replace(
        '<form name="contact" method="POST"',
        '<form name="contact" method="POST" onsubmit="event.preventDefault();alert(\'Contact form is temporarily unavailable while RenoMetric is on its free preview host.\');"',
    )
    page_path.write_text(text, encoding="utf-8")

app = OUT / "assets" / "app.js"
if app.exists():
    text = app.read_text(encoding="utf-8")
    text = text.replace("https://renometric.netlify.app", ORIGIN)
    text = text.replace("location.replace('/#calculators')", f"location.replace('{BASE}/#calculators')")
    text = text.replace('href="/calculators/', f'href="{BASE}/calculators/')
    app.write_text(text, encoding="utf-8")

for name in ("robots.txt", "sitemap.xml"):
    p = OUT / name
    if p.exists():
        p.write_text(p.read_text(encoding="utf-8").replace("https://renometric.netlify.app", ORIGIN).replace("https://tangxuejia.github.io/tangxuejia", ORIGIN), encoding="utf-8")

scripts_dir = ROOT / ".github" / "scripts"
renderer = None
renderer_path = scripts_dir / "seo-renderer.py"
if renderer_path.exists():
    spec = importlib.util.spec_from_file_location("renometric_seo_renderer", renderer_path)
    if spec and spec.loader:
        renderer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(renderer)

calc_dir = OUT / "calculators"
calc_dir.mkdir(exist_ok=True)
planning_pages: list[dict] = []

# Generate distinct long-tail planning pages. These are WebPage resources that
# point to a real working core calculator instead of pretending to be standalone apps.
if renderer:
    for idx, seo_script in enumerate(sorted(scripts_dir.glob("seo-pages-v*.py")), start=1):
        spec = importlib.util.spec_from_file_location(f"renometric_seo_batch_{idx}", seo_script)
        if not spec or not spec.loader:
            continue
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not hasattr(module, "seo_pages"):
            continue
        for page in module.seo_pages():
            planning_pages.append(page)
            target = calc_dir / f"{page['slug']}.html"
            target.write_text(renderer.render_planning_page(page, BASE, ORIGIN), encoding="utf-8")

# Normalize all calculator/project-page canonicals to clean URLs so .html and
# directory variants do not compete in search.
for src in list(calc_dir.glob("*.html")):
    slug = src.stem
    clean_url = f"{ORIGIN}/calculators/{slug}"
    text = src.read_text(encoding="utf-8")
    if '<link rel="canonical"' in text:
        text = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="{clean_url}">', text, count=1)
    else:
        text = text.replace("</head>", f'<link rel="canonical" href="{clean_url}"></head>', 1)
    text = re.sub(r'<meta property="og:url" content="[^"]+">', f'<meta property="og:url" content="{clean_url}">', text)
    src.write_text(text, encoding="utf-8")

# GitHub Pages has no rewrite engine, so materialize clean routes.
for src in list(calc_dir.glob("*.html")):
    clean = calc_dir / src.stem
    clean.mkdir(exist_ok=True)
    shutil.copy2(src, clean / "index.html")

# Practical guide library lives separately from calculator/project pages.
guides_dir = OUT / "guides"
guides_dir.mkdir(exist_ok=True)
guide_pages: list[dict] = []
if renderer:
    for idx, guide_script in enumerate(sorted(scripts_dir.glob("seo-guides-v*.py")), start=1):
        spec = importlib.util.spec_from_file_location(f"renometric_guide_batch_{idx}", guide_script)
        if not spec or not spec.loader:
            continue
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not hasattr(module, "seo_guides"):
            continue
        for page in module.seo_guides():
            guide_pages.append(page)
            clean = guides_dir / page["slug"]
            clean.mkdir(exist_ok=True)
            (clean / "index.html").write_text(renderer.render_guide(page, BASE, ORIGIN), encoding="utf-8")

# Trust pages also receive friendly clean routes.
for slug in ("about", "methodology", "privacy", "terms", "contact"):
    src = OUT / f"{slug}.html"
    if src.exists():
        clean = OUT / slug
        clean.mkdir(exist_ok=True)
        shutil.copy2(src, clean / "index.html")

TOPICS = {
    "concrete": {
        "title": "Concrete Calculators & Guides",
        "description": "Concrete volume, bags, slabs, patios, driveways, footings, waste and cubic-yard planning resources.",
        "links": [
            ("concrete", "Concrete Calculator"),
            ("concrete-slab-calculator", "Concrete Slab Calculator"),
            ("concrete-cost-calculator", "Concrete Cost Calculator"),
            ("concrete-bag-calculator", "Concrete Bag Calculator"),
            ("concrete-patio-calculator", "Concrete Patio Calculator"),
            ("concrete-driveway-calculator", "Concrete Driveway Calculator"),
            ("concrete-footing-calculator", "Concrete Footing Calculator"),
            ("cubic-yard-calculator", "Cubic Yard Calculator"),
            ("concrete-waste-calculator", "Concrete Waste Calculator"),
            ("how-much-concrete-do-i-need", "How Much Concrete Do I Need?"),
        ],
    },
    "flooring": {
        "title": "Flooring & Tile Calculators",
        "description": "Flooring square footage, boxes, material cost, laminate, vinyl, hardwood, carpet, bathroom tile and kitchen tile planning.",
        "links": [
            ("flooring", "Flooring Calculator"),
            ("tile", "Tile Calculator"),
            ("flooring-cost-calculator", "Flooring Cost Calculator"),
            ("laminate-flooring-calculator", "Laminate Flooring Calculator"),
            ("vinyl-flooring-calculator", "Vinyl Flooring Calculator"),
            ("hardwood-flooring-calculator", "Hardwood Flooring Calculator"),
            ("carpet-calculator", "Carpet Calculator"),
            ("room-flooring-calculator", "Room Flooring Calculator"),
            ("flooring-box-calculator", "Flooring Box Calculator"),
            ("bathroom-tile-calculator", "Bathroom Tile Calculator"),
            ("kitchen-tile-calculator", "Kitchen Tile Calculator"),
        ],
    },
    "paint": {
        "title": "Paint Calculators & Guides",
        "description": "Paint gallons, room walls, ceilings, exterior surfaces, cost, coverage, fences and whole-house planning.",
        "links": [
            ("paint", "Paint Calculator"),
            ("wall-paint-calculator", "Wall Paint Calculator"),
            ("room-paint-calculator", "Room Paint Calculator"),
            ("ceiling-paint-calculator", "Ceiling Paint Calculator"),
            ("exterior-paint-calculator", "Exterior Paint Calculator"),
            ("paint-cost-calculator", "Paint Cost Calculator"),
            ("paint-gallon-calculator", "Paint Gallon Calculator"),
            ("paint-coverage-calculator", "Paint Coverage Calculator"),
            ("fence-paint-calculator", "Fence Paint Calculator"),
            ("house-paint-calculator", "House Paint Calculator"),
        ],
    },
    "landscaping": {
        "title": "Landscaping Material Calculators",
        "description": "Gravel, mulch, soil, topsoil, pavers, garden beds and river-rock volume planning.",
        "links": [
            ("gravel", "Gravel Calculator"),
            ("mulch", "Mulch Calculator"),
            ("soil-calculator", "Soil Calculator"),
            ("topsoil-calculator", "Topsoil Calculator"),
            ("paver-calculator", "Paver Calculator"),
            ("garden-bed-soil-calculator", "Garden Bed Soil Calculator"),
            ("river-rock-calculator", "River Rock Calculator"),
        ],
    },
    "roofing-decks-fences": {
        "title": "Roofing, Deck & Fence Calculators",
        "description": "Roof area, shingles, roofing materials, deck boards, fence posts and spacing resources for early project planning.",
        "links": [
            ("roofing", "Roofing Calculator"),
            ("roof-area-calculator", "Roof Area Calculator"),
            ("shingle-calculator", "Shingle Calculator"),
            ("roofing-material-calculator", "Roofing Material Calculator"),
            ("deck", "Deck Calculator"),
            ("deck-board-calculator", "Deck Board Calculator"),
            ("fence", "Fence Calculator"),
            ("fence-post-calculator", "Fence Post Calculator"),
        ],
    },
}


def render_topic(slug: str, topic: dict) -> str:
    canonical = f"{ORIGIN}/topics/{slug}"
    project_cards = "".join(
        f'<article class="card"><a href="{BASE}/calculators/{item_slug}"><span class="tag">Project page</span><h3>{html.escape(title)}</h3><p>Open the RenoMetric resource for this project.</p></a></article>'
        for item_slug, title in topic["links"]
    )
    related_guides = [g for g in guide_pages if g.get("topic") == slug]
    guide_cards = "".join(
        f'<article class="card"><a href="{BASE}/guides/{g["slug"]}"><span class="tag">Guide</span><h3>{html.escape(g["title"])}</h3><p>{html.escape(g["description"])}</p></a></article>'
        for g in related_guides
    )
    all_items = [
        {"@type": "ListItem", "position": i, "name": title, "url": f"{ORIGIN}/calculators/{item_slug}"}
        for i, (item_slug, title) in enumerate(topic["links"], start=1)
    ]
    offset = len(all_items)
    all_items.extend(
        {"@type": "ListItem", "position": offset + i, "name": g["title"], "url": f"{ORIGIN}/guides/{g['slug']}"}
        for i, g in enumerate(related_guides, start=1)
    )
    schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": topic["title"],
        "description": topic["description"],
        "url": canonical,
        "mainEntity": {"@type": "ItemList", "itemListElement": all_items},
    }
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(topic['title'])} | RenoMetric</title><meta name="description" content="{html.escape(topic['description'])}"><link rel="canonical" href="{canonical}"><meta name="robots" content="index,follow"><link rel="stylesheet" href="{BASE}/assets/styles.css"><script type="application/ld+json">{json.dumps(schema, separators=(',', ':'))}</script></head><body><header class="nav"><div class="wrap nav-in"><a class="brand" href="{BASE}/">Reno<span>Metric</span></a><nav class="nav-links"><a href="{BASE}/#calculators">Calculators</a><a href="{BASE}/guides/">Guides</a><a href="{BASE}/methodology.html">Methodology</a></nav></div></header><main><section class="hero"><div class="wrap"><span class="eyebrow">Project topic hub</span><h1 style="font-size:clamp(2.7rem,6vw,5rem)">{html.escape(topic['title'])}</h1><p>{html.escape(topic['description'])}</p></div></section><section class="section"><div class="wrap"><div class="section-head"><div><span class="tag">Choose a project</span><h2>Calculators and planning pages</h2></div><p>Start with the page closest to the job you are estimating, then use the related working core calculator for the actual numbers.</p></div><div class="grid">{project_cards}</div>{f'<div class="section-head" style="margin-top:42px"><div><span class="tag">Practical guides</span><h2>Measure and plan better.</h2></div></div><div class="grid">{guide_cards}</div>' if guide_cards else ''}<article class="article"><h2>How to use this topic hub</h2><p>Measure the real project first, choose the resource closest to the work you are planning, then replace generic assumptions with exact product coverage, yield, package size or spacing guidance from the supplier. RenoMetric is designed for transparent planning rather than hidden assumptions.</p><p class="note"><b>Planning only:</b> final quantities can change with site conditions, installation method, product specifications and local requirements.</p></article></div></section></main><footer class="footer"><div class="wrap"><p class="legal">© 2026 RenoMetric. Transparent home-improvement planning tools and guides.</p></div></footer></body></html>'''


topics_dir = OUT / "topics"
topics_dir.mkdir(exist_ok=True)
for topic_slug, topic in TOPICS.items():
    target = topics_dir / topic_slug
    target.mkdir(exist_ok=True)
    (target / "index.html").write_text(render_topic(topic_slug, topic), encoding="utf-8")

# Build guide library index.
guide_cards = "".join(
    f'<article class="card"><a href="{BASE}/guides/{g["slug"]}"><span class="tag">{html.escape(g["category"])}</span><h3>{html.escape(g["title"])}</h3><p>{html.escape(g["description"])}</p></a></article>'
    for g in guide_pages
)
guide_index_schema = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "Home Improvement Planning Guides",
    "description": "Practical measurement, material and estimating guides from RenoMetric.",
    "url": f"{ORIGIN}/guides",
}
(guides_dir / "index.html").write_text(
    f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Home Improvement Planning Guides | RenoMetric</title><meta name="description" content="Practical measurement, material and estimating guides for concrete, flooring, paint, landscaping, roofing, decks and fences."><link rel="canonical" href="{ORIGIN}/guides"><meta name="robots" content="index,follow"><link rel="stylesheet" href="{BASE}/assets/styles.css"><script type="application/ld+json">{json.dumps(guide_index_schema, separators=(',', ':'))}</script></head><body><header class="nav"><div class="wrap nav-in"><a class="brand" href="{BASE}/">Reno<span>Metric</span></a><nav class="nav-links"><a href="{BASE}/#calculators">Calculators</a><a href="{BASE}/guides/">Guides</a><a href="{BASE}/methodology.html">Methodology</a></nav></div></header><main><section class="hero"><div class="wrap"><span class="eyebrow">RenoMetric guides</span><h1>Measure better.<br>Estimate with context.</h1><p>Short, practical guides for the assumptions behind common home-improvement material calculations.</p></div></section><section class="section"><div class="wrap"><div class="grid">{guide_cards}</div></div></section></main><footer class="footer"><div class="wrap"><p class="legal">© 2026 RenoMetric. Planning resources for homeowners and DIY projects.</p></div></footer></body></html>''',
    encoding="utf-8",
)

# Insert topic architecture into the homepage and keep visible resource count honest.
home = OUT / "index.html"
if home.exists():
    text = home.read_text(encoding="utf-8")
    topic_cards = "".join(
        f'<article class="card"><a href="{BASE}/topics/{slug}"><span class="tag">Topic hub</span><h3>{html.escape(topic["title"])}</h3><p>{html.escape(topic["description"])}</p></a></article>'
        for slug, topic in TOPICS.items()
    )
    section = f'<section class="section"><div class="wrap"><div class="section-head"><div><span class="tag">Project topic hubs</span><h2>Go deeper by project.</h2></div><p>Explore focused calculator clusters and practical guides for common renovation jobs.</p></div><div class="grid">{topic_cards}</div><p style="margin-top:22px"><a class="btn" href="{BASE}/guides/">Browse all practical guides</a></p></div></section>'
    marker = '<section class="section"><div class="wrap"><div class="section-head"><div><span class="tag">The RenoMetric standard</span>'
    if marker in text:
        text = text.replace(marker, section + marker, 1)
    resource_count = len(list(calc_dir.glob("*.html"))) + len(guide_pages)
    text = text.replace('<span><b>10</b> launch tools</span>', f'<span><b>{resource_count}</b> planning resources</span>')
    home.write_text(text, encoding="utf-8")

# Rebuild sitemap from the actual generated resource set.
urls = [f"{ORIGIN}/"]
urls.extend(f"{ORIGIN}/{slug}" for slug in ("about", "methodology", "privacy", "terms", "contact"))
urls.extend(f"{ORIGIN}/topics/{slug}" for slug in TOPICS)
urls.append(f"{ORIGIN}/guides")
urls.extend(f"{ORIGIN}/guides/{g['slug']}" for g in guide_pages)
urls.extend(f"{ORIGIN}/calculators/{src.stem}" for src in sorted(calc_dir.glob("*.html")))
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += "\n".join(f"  <url><loc>{url}</loc></url>" for url in urls)
sitemap += "\n</urlset>\n"
(OUT / "sitemap.xml").write_text(sitemap, encoding="utf-8")

(OUT / "404.html").write_text(
    f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found — RenoMetric</title><link rel="stylesheet" href="{BASE}/assets/styles.css"></head><body><main class="section"><div class="wrap"><article class="article"><h1>Page not found</h1><p>The page may have moved.</p><p><a class="btn primary" href="{BASE}/">Back to RenoMetric</a></p></article></div></main></body></html>''',
    encoding="utf-8",
)

print(
    f"Built GitHub Pages artifact at {OUT} with "
    f"{len(list(calc_dir.glob('*.html')))} calculator/project pages, "
    f"{len(guide_pages)} guides and {len(TOPICS)} topic hubs"
)
