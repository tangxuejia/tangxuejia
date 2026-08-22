from __future__ import annotations

import html
import importlib.util
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_site"
BASE = "/tangxuejia"
ORIGIN = "https://tangxuejia.github.io/tangxuejia"

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

for page_path in OUT.rglob("*.html"):
    text = page_path.read_text(encoding="utf-8")
    text = text.replace("https://renometric.netlify.app", ORIGIN)
    text = text.replace('href="/', f'href="{BASE}/')
    text = text.replace("href='/", f"href='{BASE}/")
    text = text.replace('src="/', f'src="{BASE}/')
    text = text.replace("src='/", f"src='{BASE}/")
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
        p.write_text(p.read_text(encoding="utf-8").replace("https://renometric.netlify.app", ORIGIN), encoding="utf-8")

calc_dir = OUT / "calculators"
calc_dir.mkdir(exist_ok=True)

scripts_dir = ROOT / ".github" / "scripts"
renderer = None
renderer_path = scripts_dir / "seo-pages-v2.py"
if renderer_path.exists():
    spec = importlib.util.spec_from_file_location("renometric_seo_renderer", renderer_path)
    if spec and spec.loader:
        renderer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(renderer)

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
            target = calc_dir / f"{page['slug']}.html"
            target.write_text(renderer.render_page(page, BASE, ORIGIN), encoding="utf-8")

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

for src in list(calc_dir.glob("*.html")):
    slug = src.stem
    clean = calc_dir / slug
    clean.mkdir(exist_ok=True)
    shutil.copy2(src, clean / "index.html")

for slug in ("about", "methodology", "privacy", "terms", "contact"):
    src = OUT / f"{slug}.html"
    if src.exists():
        clean = OUT / slug
        clean.mkdir(exist_ok=True)
        shutil.copy2(src, clean / "index.html")

TOPICS = {
    "concrete": {
        "title": "Concrete Calculators & Guides",
        "description": "Concrete volume, bags, slabs, patios, driveways, footings, waste and cubic-yard planning tools.",
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
        "description": "Roof area, shingles, roofing materials, deck boards, fence posts and spacing tools for early project planning.",
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
    cards = "".join(
        f'<article class="card"><a href="{BASE}/calculators/{item_slug}"><span class="tag">Calculator</span><h3>{html.escape(title)}</h3><p>Open the RenoMetric planning page for this project.</p></a></article>'
        for item_slug, title in topic["links"]
    )
    schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": topic["title"],
        "description": topic["description"],
        "url": canonical,
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": [
                {"@type": "ListItem", "position": i, "name": title, "url": f"{ORIGIN}/calculators/{item_slug}"}
                for i, (item_slug, title) in enumerate(topic["links"], start=1)
            ],
        },
    }
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(topic['title'])} | RenoMetric</title><meta name="description" content="{html.escape(topic['description'])}"><link rel="canonical" href="{canonical}"><meta name="robots" content="index,follow"><link rel="stylesheet" href="{BASE}/assets/styles.css"><script type="application/ld+json">{json.dumps(schema, separators=(',', ':'))}</script></head><body><header class="nav"><div class="wrap nav-in"><a class="brand" href="{BASE}/">Reno<span>Metric</span></a><nav class="nav-links"><a href="{BASE}/#calculators">Calculators</a><a href="{BASE}/methodology.html">Methodology</a><a href="{BASE}/about.html">About</a></nav></div></header><main><section class="hero"><div class="wrap"><span class="eyebrow">Project topic hub</span><h1 style="font-size:clamp(2.7rem,6vw,5rem)">{html.escape(topic['title'])}</h1><p>{html.escape(topic['description'])}</p></div></section><section class="section"><div class="wrap"><div class="section-head"><div><span class="tag">Choose a project</span><h2>Calculators and planning guides</h2></div><p>Start with the page that matches the job you are estimating. Each page keeps assumptions visible and links back to a working core calculator.</p></div><div class="grid">{cards}</div><article class="article"><h2>How to use this topic hub</h2><p>Measure the real project first, choose the calculator closest to the work you are planning, then replace generic defaults with the exact product coverage, yield, package size or spacing guidance from the supplier. RenoMetric is designed for transparent planning rather than hidden assumptions.</p><p class="note"><b>Planning only:</b> final quantities can change with site conditions, installation method, product specifications and local requirements.</p></article></div></section></main><footer class="footer"><div class="wrap"><p class="legal">© 2026 RenoMetric. Transparent home-improvement planning tools.</p></div></footer></body></html>'''

topics_dir = OUT / "topics"
topics_dir.mkdir(exist_ok=True)
for topic_slug, topic in TOPICS.items():
    target = topics_dir / topic_slug
    target.mkdir(exist_ok=True)
    (target / "index.html").write_text(render_topic(topic_slug, topic), encoding="utf-8")

home = OUT / "index.html"
if home.exists():
    text = home.read_text(encoding="utf-8")
    topic_cards = "".join(
        f'<article class="card"><a href="{BASE}/topics/{slug}"><span class="tag">Topic hub</span><h3>{html.escape(topic["title"])}</h3><p>{html.escape(topic["description"])}</p></a></article>'
        for slug, topic in TOPICS.items()
    )
    section = f'<section class="section"><div class="wrap"><div class="section-head"><div><span class="tag">Project topic hubs</span><h2>Go deeper by project.</h2></div><p>Explore focused calculator clusters for the jobs homeowners and DIYers search most often.</p></div><div class="grid">{topic_cards}</div></div></section>'
    marker = '<section class="section"><div class="wrap"><div class="section-head"><div><span class="tag">The RenoMetric standard</span>'
    if marker in text:
        text = text.replace(marker, section + marker, 1)
    text = text.replace('<span><b>10</b> launch tools</span>', f'<span><b>{len(list(calc_dir.glob("*.html")))}</b> calculators & guides</span>')
    home.write_text(text, encoding="utf-8")

urls = [f"{ORIGIN}/"]
urls.extend(f"{ORIGIN}/{slug}" for slug in ("about", "methodology", "privacy", "terms", "contact"))
urls.extend(f"{ORIGIN}/topics/{slug}" for slug in TOPICS)
urls.extend(f"{ORIGIN}/calculators/{src.stem}" for src in sorted(calc_dir.glob("*.html")))
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += "\n".join(f"  <url><loc>{url}</loc></url>" for url in urls)
sitemap += "\n</urlset>\n"
(OUT / "sitemap.xml").write_text(sitemap, encoding="utf-8")

(OUT / "404.html").write_text(
    f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found — RenoMetric</title><link rel="stylesheet" href="{BASE}/assets/styles.css"></head><body><main class="section"><div class="wrap"><article class="article"><h1>Page not found</h1><p>The page may have moved.</p><p><a class="btn primary" href="{BASE}/">Back to RenoMetric</a></p></article></div></main></body></html>''',
    encoding="utf-8",
)

print(f"Built GitHub Pages artifact at {OUT} with {len(list(calc_dir.glob('*.html')))} calculator/SEO pages and {len(TOPICS)} topic hubs")
