from __future__ import annotations

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

# GitHub Pages should serve files as-is instead of invoking Jekyll.
(OUT / ".nojekyll").write_text("", encoding="utf-8")

# Adapt public URLs only in the generated Pages artifact. The source tree remains
# host-neutral / Netlify-compatible for later custom-domain deployment.
for html in OUT.rglob("*.html"):
    text = html.read_text(encoding="utf-8")
    text = text.replace("https://renometric.netlify.app", ORIGIN)
    text = text.replace('href="/', f'href="{BASE}/')
    text = text.replace("href='/", f"href='{BASE}/")
    text = text.replace('src="/', f'src="{BASE}/')
    text = text.replace("src='/", f"src='{BASE}/")
    # Netlify Forms are not available on GitHub Pages. Prevent a broken POST while
    # retaining the trust/contact page until a permanent contact endpoint is added.
    text = text.replace(
        '<form name="contact" method="POST"',
        '<form name="contact" method="POST" onsubmit="event.preventDefault();alert(\'Contact form is temporarily unavailable while RenoMetric is on its free preview host.\');"',
    )
    html.write_text(text, encoding="utf-8")

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

# GitHub Pages has no rewrite engine. Materialize the clean calculator URLs as
# directories so /calculators/concrete/ resolves to an actual index.html.
calc_dir = OUT / "calculators"
if calc_dir.exists():
    for src in list(calc_dir.glob("*.html")):
        slug = src.stem
        clean = calc_dir / slug
        clean.mkdir(exist_ok=True)
        shutil.copy2(src, clean / "index.html")

# Friendly clean routes for trust pages, while keeping the .html versions too.
for slug in ("about", "methodology", "privacy", "terms", "contact"):
    src = OUT / f"{slug}.html"
    if src.exists():
        clean = OUT / slug
        clean.mkdir(exist_ok=True)
        shutil.copy2(src, clean / "index.html")

# A simple 404 that preserves navigation back to the project site.
(OUT / "404.html").write_text(
    f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found — RenoMetric</title><link rel="stylesheet" href="{BASE}/assets/styles.css"></head><body><main class="section"><div class="wrap"><article class="article"><h1>Page not found</h1><p>The page may have moved.</p><p><a class="btn primary" href="{BASE}/">Back to RenoMetric</a></p></article></div></main></body></html>''',
    encoding="utf-8",
)

print(f"Built GitHub Pages artifact at {OUT}")
