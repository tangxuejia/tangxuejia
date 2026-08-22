from __future__ import annotations

import importlib.util
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

urls = [f"{ORIGIN}/"]
urls.extend(f"{ORIGIN}/{slug}" for slug in ("about", "methodology", "privacy", "terms", "contact"))
urls.extend(f"{ORIGIN}/calculators/{src.stem}" for src in sorted(calc_dir.glob("*.html")))
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += "\n".join(f"  <url><loc>{url}</loc></url>" for url in urls)
sitemap += "\n</urlset>\n"
(OUT / "sitemap.xml").write_text(sitemap, encoding="utf-8")

(OUT / "404.html").write_text(
    f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found — RenoMetric</title><link rel="stylesheet" href="{BASE}/assets/styles.css"></head><body><main class="section"><div class="wrap"><article class="article"><h1>Page not found</h1><p>The page may have moved.</p><p><a class="btn primary" href="{BASE}/">Back to RenoMetric</a></p></article></div></main></body></html>''',
    encoding="utf-8",
)

print(f"Built GitHub Pages artifact at {OUT} with {len(list(calc_dir.glob('*.html')))} calculator/SEO pages")
