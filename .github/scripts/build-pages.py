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

# High-intent pages get a page-specific decision profile instead of only a generic calculator template.
core_profiles = {
    "concrete": ("Slabs, patios, pads and small pours.", "Length, width, thickness, waste and the exact bag yield or supplier volume.", "Net volume, order volume, cubic yards and bag equivalents.", "Confirm subgrade, reinforcement, mix design, delivery access and finishing capacity."),
    "concrete-bag-calculator": ("Small DIY pours where complete bag counts matter.", "Pour dimensions, waste and the yield printed on the selected bag.", "Required volume, bags to buy and the effect of package rounding.", "Do not use bag weight as yield; confirm mixing time, water and product instructions."),
    "concrete-cost-calculator": ("An early material-cost comparison before requesting quotes.", "Concrete quantity, unit price, delivery, labor, preparation and contingency.", "A visible cost breakdown rather than one unexplained headline number.", "Local prices, access, demolition, pumping, permits and site preparation can dominate."),
    "concrete-driveway-calculator": ("Driveway pours with separate thickness, base and access decisions.", "Driveway dimensions, designed thickness, waste, gravel base and delivery assumptions.", "Concrete quantity plus the planning items that affect the installed job.", "Confirm vehicle loads, drainage, base design, joints, reinforcement and local requirements."),
    "concrete-slab-calculator": ("Rectangular slab volume and purchase planning.", "Slab length, width, thickness, waste and product yield.", "Raw volume, ordering allowance, cubic yards and package options.", "Thickness and reinforcement are design decisions; the calculator does not approve them."),
    "rebar-calculator": ("A first-pass bar count for a specified slab or grid.", "Usable spans, bar spacing, edge clearance, stock length and allowance.", "Bars in each direction, grid length and a stock-purchase estimate.", "Use structural drawings for bar size, spacing, cover, laps and placement."),
    "rebar-weight-calculator": ("Weight and handling planning after bar size and length are known.", "Bar size, count or length and the selected steel unit weight.", "Estimated total linear length and weight for transport or purchasing.", "Verify the bar designation, stock lengths, bundle limits and structural schedule."),
    "flooring": ("Flooring coverage, waste and complete-carton planning.", "Every installation area, exclusions, layout waste and carton coverage.", "Net area, planned coverage, boxes and material cost.", "Read the current carton label; include closets, stairs, transitions and return-policy limits."),
    "flooring-calculator": ("Quick flooring area and material planning across rooms.", "Room dimensions, fixed exclusions, waste and product coverage.", "Install area, purchase area and complete-package quantity.", "Measure each room separately when direction, pattern or product changes."),
    "paint": ("Room-wall, ceiling and whole-house paint planning.", "Surface dimensions, openings, coats, product coverage and container size.", "Paintable area, gallons or containers and material cost.", "Primer, texture, surface porosity, color change and ceiling products may need separate estimates."),
    "room-paint-calculator": ("A room-level estimate when wall area and coat count are the main questions.", "Wall height and lengths, major openings, coats and the exact coverage rate.", "Paintable area and rounded containers for the planned coats.", "Floor area is not wall area; verify primer and finish coverage separately."),
    "gravel": ("Bulk gravel, driveway and landscape-bed ordering.", "Length, width, compacted depth, density, waste and price basis.", "Cubic yards, estimated weight or tons and an order estimate.", "Density, moisture, compaction, delivery minimums and spreading are supplier-specific."),
    "mulch": ("Landscape-bed mulch volume and bag coverage.", "Bed area, installed depth and labeled bag volume.", "Cubic yards, cubic feet and complete bags.", "Choose depth for the plants and drainage; weight is not a substitute for labeled volume."),
    "roofing": ("Simple roof surface, squares and shingle-bundle planning.", "Roof footprint or planes, pitch factor, waste and bundle coverage.", "Sloped area, roofing squares and field-shingle bundles.", "Starter, ridge, flashing, underlayment, ventilation and roof condition need separate checks."),
    "roofing-calculator": ("A fast roofing quantity estimate before a supplier conversation.", "Roof length, width, pitch, waste and bundle coverage.", "Area and rounded field-shingle quantity.", "Complex hips, valleys, dormers and penetrations require separate plane and accessory measurements."),
    "deck": ("Deck-board quantity planning for a main rectangular field.", "Deck dimensions, board face width, gap, stock length and waste.", "Rows, linear feet and a board purchase starting point.", "Stairs, borders, picture framing, fasteners and framing are separate quantities."),
    "fence": ("Fence-run, section and post planning.", "Total run, gate openings, post spacing and extra corners or ends.", "Fence runs, sections and a preliminary post count.", "Gate posts, wind, soil, footing depth and local requirements need a separate design check."),
    "renovation-cost-calculator": ("An early renovation budget before comparing contractor quotes.", "Rooms, material quantities, labor, delivery, disposal, permits and contingency.", "A separated budget with visible assumptions and missing-scope checks.", "Use quotes and site inspection for hidden conditions; do not treat the result as a fixed price."),
    "whole-house-renovation-planner": ("Coordinating rooms, materials and a starter whole-house plan.", "Room dimensions, surfaces, product coverage, quantities and budget allowances.", "A project path that connects measurements, purchase quantities and budget lines.", "Sequence, permits, structural work, trade coordination and site conditions require professional review."),
    "drywall-calculator": ("Wall and ceiling sheet, compound and screw planning.", "Surface area, sheet size, openings, waste and fastening assumptions.", "Sheets, joint compound and screws as separate purchase quantities.", "Fire ratings, moisture conditions, ceiling layout, framing and local requirements may change the specification."),
}

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
    text = text.replace("https://tangxuejia.github.io/tangxuejia", ORIGIN)
    text = re.sub(r'href="/(?!tangxuejia/)', f'href="{BASE}/', text)
    text = re.sub(r"href='/((?!tangxuejia/))", f"href='{BASE}/", text)
    text = re.sub(r'src="/(?!tangxuejia/)', f'src="{BASE}/', text)
    text = re.sub(r"src='/((?!tangxuejia/))", f"src='{BASE}/", text)
    if not BASE:
        text = text.replace('href="/tangxuejia/', 'href="/').replace("href='/tangxuejia/", "href='/").replace('src="/tangxuejia/', 'src="/').replace("src='/tangxuejia/", "src='/")
    # Cloudflare serves the extensionless directory routes as canonical URLs.
    # Keep calculator links on those routes so crawlers and users avoid an
    # unnecessary .html redirect.
    text = re.sub(r'(/calculators/[^"\'?#]+?)\.html(?=["\'/?#])', r'\1', text)
    text = text.replace('<form name="contact" method="POST"', '<form name="contact" method="POST" onsubmit="event.preventDefault();alert(\'Contact form is temporarily unavailable while RenoMetric is on its free preview host.\');"')
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

for src in list(calc_dir.glob("*.html")):
    slug = src.stem
    clean_url = f"{ORIGIN}/calculators/{slug}"
    text = src.read_text(encoding="utf-8")
    if '<link rel="canonical"' in text:
        text = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="{clean_url}">', text, count=1)
    else:
        text = text.replace("</head>", f'<link rel="canonical" href="{clean_url}"></head>', 1)
    text = re.sub(r'<meta property="og:url" content="[^"]+">', f'<meta property="og:url" content="{clean_url}">', text)
    visible_text = re.sub(r"<script\b.*?</script>|<style\b.*?</style>", " ", text, flags=re.S | re.I)
    visible_text = re.sub(r"<[^>]+>", " ", visible_text)
    if "Quick answer" not in visible_text and re.search(r"</h1>", text, re.I):
        answer_title_match = re.search(r"<title>(.*?)</title>", text, re.S | re.I)
        answer_description_match = re.search(r'<meta name="description" content="([^"]*)"', text, re.S | re.I)
        answer_title = html.unescape(answer_title_match.group(1)).strip() if answer_title_match else slug.replace("-", " ").title()
        answer_title = re.sub(r"\s*\|\s*RenoMetric$", "", answer_title).strip()
        answer_description = html.unescape(answer_description_match.group(1)).strip() if answer_description_match else "Use measured project dimensions to create an early planning estimate."
        answer_block = f'<div id="renometric-answer" class="note" style="margin:18px 0"><b>Quick answer:</b> {html.escape(answer_description)} Start with actual measurements, use the product label for coverage or yield, and treat the result as a planning estimate until site conditions and supplier requirements are confirmed.</div>'
        text = re.sub(r"</h1>", "</h1>" + answer_block, text, count=1, flags=re.I)
    if 'id="renometric-decision-promise"' not in text and "What you will get" not in text and re.search(r"</h1>", text, re.I):
        decision_block = """<div id="renometric-decision-promise" class="article" style="margin:16px 0;background:#eef4f0;border:1px solid #cfe2d7;border-radius:12px"><h2>What you will get</h2><div class="grid"><div><b>1. Needed</b><p>See the estimated project quantity from your measurements.</p></div><div><b>2. Buy</b><p>Add waste and round to complete bags, boxes, cans, bundles or delivery quantities.</p></div><div><b>3. Check</b><p>Review product coverage, site conditions, local requirements and supplier details before ordering.</p></div></div></div>"""
        text = re.sub(r"</h1>", "</h1>" + decision_block, text, count=1, flags=re.I)
    profile = core_profiles.get(slug)
    if profile and 'id="renometric-core-profile"' not in text:
        best_for, inputs, output, check = profile
        profile_html = f'''<section id="renometric-core-profile" class="section"><div class="wrap"><article class="article" style="background:#f4f8f5;border:1px solid #cfe2d7;border-radius:12px"><span class="tag">Decision support</span><h2>What this tool helps you decide</h2><div class="grid"><div><b>Best for</b><p>{html.escape(best_for)}</p></div><div><b>Enter</b><p>{html.escape(inputs)}</p></div><div><b>You get</b><p>{html.escape(output)}</p></div><div><b>Check before buying</b><p>{html.escape(check)}</p></div></div></article></div></section>'''
        text = re.sub(r"</h1>", "</h1>" + profile_html, text, count=1, flags=re.I)
    if len(visible_text.split()) < 150:
        title_match = re.search(r"<title>(.*?)</title>", text, re.S | re.I)
        description_match = re.search(r'<meta name="description" content="([^"]*)"', text, re.S | re.I)
        page_title = html.unescape(title_match.group(1)).strip() if title_match else slug.replace("-", " ").title()
        page_title = re.sub(r"\s*\|\s*RenoMetric$", "", page_title).strip()
        page_description = html.unescape(description_match.group(1)).strip() if description_match else "Use the measured project dimensions and the visible assumptions to create an early planning estimate."
        enrichment = f'''<section class="section"><div class="wrap"><article class="article"><span class="tag">Practical planning notes</span><h2>How to use this {html.escape(page_title)}</h2><p>{html.escape(page_description)} Start with the actual dimensions or load values from the project, keep the units consistent, and change the default assumptions when the product label or supplier sheet gives you a more accurate value.</p><h2>What the estimate does and does not include</h2><p>This page is for early material planning. The result can change with openings, layout, cuts, waste, product yield, density, packaging, access, installation method and site conditions. It does not replace structural design, permitted drawings, manufacturer instructions or a contractor quotation.</p><h2>Worked planning example</h2><p>For a simple project, enter one measured section first and review the result. If the shape is irregular, split it into smaller sections, calculate each section, and add the quantities before applying whole-bag, box, bundle or delivery rounding.</p><h2>Before you order</h2><ul><li>Re-check the field measurements and the unit labels.</li><li>Replace generic coverage, yield, density or spacing assumptions with the exact product data.</li><li>Confirm package size, minimum order, delivery, tax and local requirements with the supplier.</li></ul></article></div></section>'''
        if "</main>" in text:
            text = text.replace("</main>", enrichment + "</main>", 1)
        else:
            text = text.replace("</body>", enrichment + "</body>", 1)
    if "application/ld+json" not in text:
        title_match = re.search(r"<title>(.*?)</title>", text, re.S | re.I)
        description_match = re.search(r'<meta name="description" content="([^"]*)"', text, re.S | re.I)
        schema = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebPage",
                    "name": html.unescape(title_match.group(1)).strip() if title_match else slug.replace("-", " ").title(),
                    "description": html.unescape(description_match.group(1)).strip() if description_match else "",
                    "url": clean_url,
                    "isPartOf": {"@type": "WebSite", "name": "RenoMetric", "url": f"{ORIGIN}/"},
                    "inLanguage": "en",
                    "dateModified": "2026-08-27",
                    "author": {"@type": "Organization", "name": "RenoMetric"},
                },
                {
                    "@type": "WebApplication",
                    "name": html.unescape(title_match.group(1)).strip() if title_match else slug.replace("-", " ").title(),
                    "description": html.unescape(description_match.group(1)).strip() if description_match else "",
                    "url": clean_url,
                    "applicationCategory": "UtilitiesApplication",
                    "operatingSystem": "Any",
                    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                },
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "RenoMetric", "item": f"{ORIGIN}/"},
                        {"@type": "ListItem", "position": 2, "name": "Calculators", "item": f"{ORIGIN}/calculators"},
                        {"@type": "ListItem", "position": 3, "name": html.unescape(title_match.group(1)).strip() if title_match else slug.replace("-", " ").title(), "item": clean_url},
                    ],
                },
            ],
        }
        text = text.replace("</head>", f'<script type="application/ld+json">{json.dumps(schema, separators=(",", ":"))}</script></head>', 1)
    src.write_text(text, encoding="utf-8")

for src in list(calc_dir.glob("*.html")):
    clean = calc_dir / src.stem
    clean.mkdir(exist_ok=True)
    shutil.copy2(src, clean / "index.html")

calculator_cards = []
for src in sorted(calc_dir.glob("*.html")):
    text = src.read_text(encoding="utf-8", errors="ignore")
    title_match = re.search(r"<title>(.*?)</title>", text, re.S | re.I)
    description_match = re.search(r'<meta name="description" content="([^"]*)"', text, re.S | re.I)
    title = html.unescape(title_match.group(1)).strip() if title_match else src.stem.replace("-", " ").title()
    description = html.unescape(description_match.group(1)).strip() if description_match else "Use measured project dimensions to create an early planning estimate."
    if src.stem == "index":
        continue
    calculator_cards.append(f'<article class="card"><a href="{BASE}/calculators/{src.stem}"><span class="tag">Calculator</span><h3>{html.escape(title)}</h3><p>{html.escape(description)}</p></a></article>')
calculator_schema = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "Construction and Renovation Calculators",
    "description": "Browse RenoMetric calculators for concrete, flooring, paint, landscaping, roofing, decks, fences, plumbing, electrical and HVAC planning.",
    "url": f"{ORIGIN}/calculators",
}
calculators_index = OUT / "calculators" / "index.html"
calculators_index.write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Construction Calculators with Clear Buying Answers | RenoMetric</title><meta name="description" content="Find a calculator that gives you the quantity, purchase amount, assumptions and next checks for concrete, flooring, paint, roofing, landscaping and renovation projects."><link rel="canonical" href="{ORIGIN}/calculators"><meta name="robots" content="index,follow"><link rel="stylesheet" href="{BASE}/assets/styles.css"><script type="application/ld+json">{json.dumps(calculator_schema, separators=(",", ":"))}</script></head><body><header class="nav"><div class="wrap nav-in"><a class="brand" href="{BASE}/">Reno<span>Metric</span></a><nav class="nav-links"><a href="{BASE}/calculators">Calculators</a><a href="{BASE}/guides/">Guides</a><a href="{BASE}/methodology.html">Methodology</a></nav></div></header><main><section class="hero"><div class="wrap"><span class="eyebrow">RenoMetric tools</span><h1>Find the right calculator. Know what to buy.</h1><p>Enter measured dimensions and get a clear quantity, purchase amount, visible assumptions and practical checks before you order materials.</p></div></section><section class="section"><div class="wrap"><div class="grid">{"".join(calculator_cards)}</div><article class="article"><h2>How to use the calculator library</h2><p>Start with the project closest to your work, use consistent units, replace generic coverage or density assumptions with the product data, and keep the result as a planning estimate until site conditions and supplier requirements are confirmed.</p><p class="note"><b>Planning only:</b> final quantities can change with measurements, waste, product specifications, installation method and local requirements.</p></article></div></section></main><footer class="footer"><div class="wrap"><p class="legal">© 2026 RenoMetric. Transparent home-improvement planning tools and guides.</p></div></footer></body></html>''', encoding="utf-8")

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

for slug in ("about", "methodology", "privacy", "terms", "contact"):
    src = OUT / f"{slug}.html"
    if src.exists():
        clean_url = f"{ORIGIN}/{slug}"
        for target in (src, OUT / slug / "index.html"):
            if target.exists():
                text = target.read_text(encoding="utf-8")
                text = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="{clean_url}">', text, count=1)
                text = re.sub(r'<meta property="og:url" content="[^"]+">', f'<meta property="og:url" content="{clean_url}">', text)
                target.write_text(text, encoding="utf-8")
        clean = OUT / slug
        clean.mkdir(exist_ok=True)
        shutil.copy2(src, clean / "index.html")

TOPICS = {
    "concrete": {
        "title": "Concrete Calculators & Guides",
        "description": "Concrete volume, bags, slabs, patios, driveways, footings, waste and cubic-yard planning resources.",
        "links": [
            ("concrete", "Concrete Calculator"),
            ("concrete-project-planner", "Concrete Project Planner"),
            ("concrete-slab-calculator", "Concrete Slab Calculator"),
            ("concrete-cost-calculator", "Concrete Cost Calculator"),
            ("concrete-bag-calculator", "Concrete Bag Calculator"),
            ("concrete-patio-calculator", "Concrete Patio Calculator"),
            ("concrete-driveway-calculator", "Concrete Driveway Calculator"),
            ("concrete-driveway-project-planner", "Concrete Driveway Project Planner"),
            ("concrete-footing-calculator", "Concrete Footing Calculator"),
            ("concrete-pad-calculator", "Concrete Pad Calculator"),
            ("cubic-yard-calculator", "Cubic Yard Calculator"),
            ("concrete-waste-calculator", "Concrete Waste Calculator"),
            ("how-much-concrete-do-i-need", "How Much Concrete Do I Need?"),
            ("rebar-spacing-calculator", "Rebar Spacing Calculator"),
            ("rebar-weight-calculator", "Rebar Weight Calculator"),
            ("concrete-yield-calculator", "Concrete Yield Calculator"),
            ("cmu-mortar-calculator", "CMU Mortar Calculator"),
        ],
    },
    "flooring": {
        "title": "Flooring & Tile Calculators",
        "description": "Flooring square footage, boxes, material cost, laminate, vinyl, hardwood, carpet, bathroom tile and kitchen tile planning.",
        "links": [("flooring", "Flooring Calculator"),
            ("whole-house-renovation-planner", "Whole House Renovation Planner"),
            ("room-renovation-planner", "Room Renovation Planner"),
            ("kitchen-renovation-planner", "Kitchen Renovation Planner"),
            ("bathroom-renovation-planner", "Bathroom Renovation Planner"), ("tile", "Tile Calculator"), ("flooring-cost-calculator", "Flooring Cost Calculator"), ("laminate-flooring-calculator", "Laminate Flooring Calculator"), ("vinyl-flooring-calculator", "Vinyl Flooring Calculator"), ("hardwood-flooring-calculator", "Hardwood Flooring Calculator"), ("carpet-calculator", "Carpet Calculator"), ("room-flooring-calculator", "Room Flooring Calculator"), ("flooring-box-calculator", "Flooring Box Calculator"), ("bathroom-tile-calculator", "Bathroom Tile Calculator"), ("kitchen-tile-calculator", "Kitchen Tile Calculator")],
    },
    "paint": {
        "title": "Paint Calculators & Guides",
        "description": "Paint gallons, room walls, ceilings, exterior surfaces, cost, coverage, fences and whole-house planning.",
        "links": [("paint", "Paint Calculator"), ("wall-paint-calculator", "Wall Paint Calculator"), ("room-paint-calculator", "Room Paint Calculator"), ("ceiling-paint-calculator", "Ceiling Paint Calculator"), ("exterior-paint-calculator", "Exterior Paint Calculator"), ("paint-cost-calculator", "Paint Cost Calculator"), ("paint-gallon-calculator", "Paint Gallon Calculator"), ("paint-coverage-calculator", "Paint Coverage Calculator"), ("fence-paint-calculator", "Fence Paint Calculator"), ("house-paint-calculator", "House Paint Calculator")],
    },
    "landscaping": {
        "title": "Landscaping Material Calculators",
        "description": "Gravel, mulch, soil, topsoil, pavers, garden beds and river-rock volume planning.",
        "links": [("gravel", "Gravel Calculator"), ("mulch", "Mulch Calculator"), ("soil-calculator", "Soil Calculator"), ("topsoil-calculator", "Topsoil Calculator"), ("paver-calculator", "Paver Calculator"), ("garden-bed-soil-calculator", "Garden Bed Soil Calculator"), ("river-rock-calculator", "River Rock Calculator")],
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
            ("deck-project-planner", "Deck Project Planner"),
            ("deck-board-calculator", "Deck Board Calculator"),
            ("fence", "Fence Calculator"),
            ("fence-post-calculator", "Fence Post Calculator"),
        ],
    },
    "renovation": {
        "title": "Renovation Planning Calculators & Guides",
        "description": "Room-by-room renovation budgets, material takeoffs, project planning and buying checklists for home improvement work.",
        "links": [
            ("renovation-cost-calculator", "Renovation Cost Calculator"),
            ("whole-house-renovation-planner", "Whole House Renovation Planner"),
            ("room-renovation-planner", "Room Renovation Planner"),
            ("kitchen-renovation-planner", "Kitchen Renovation Planner"),
            ("bathroom-renovation-planner", "Bathroom Renovation Planner"),
            ("renovation-project-checklist", "Renovation Project Checklist"),
        ],
    },
    "plumbing": {
        "title": "Plumbing & Drainage Calculators",
        "description": "Water-pipe flow, pipe sizing, pressure loss and drainage slope planning tools with practical installation guides.",
        "links": [("pipe-flow-calculator", "Pipe Flow Calculator"), ("pipe-volume-calculator", "Pipe Volume Calculator"), ("drainage-slope-calculator", "Drainage Slope Calculator"), ("drain-pipe-capacity-calculator", "Drain Pipe Capacity Calculator"), ("wire-size-voltage-drop-calculator", "Voltage Drop Calculator")],
    },
    "electrical": {
        "title": "Electrical Load & Circuit Planning",
        "description": "Electrical load, voltage, current, watts and preliminary circuit planning resources for residential projects.",
        "links": [("electrical-load-calculator", "Electrical Load Calculator"), ("electricity-cost-calculator", "Electricity Cost Calculator"), ("generator-size-calculator", "Generator Size Calculator")],
    },
    "hvac": {
        "title": "HVAC, Heat Pump & Insulation Planning",
        "description": "Heating and cooling BTU estimates, heat-pump screening, room-by-room load preparation and insulation planning.",
        "links": [("hvac-btu-calculator", "HVAC BTU Calculator"), ("hvac-airflow-calculator", "HVAC Airflow CFM Calculator"), ("insulation-calculator", "Insulation Calculator")],
    },
}

# Connect every calculator to its topic hub and a small set of related tools.
for src in sorted(calc_dir.glob("*.html")):
    slug = src.stem
    if slug == "index":
        continue
    topic_slug, topic = next(
        (
            (candidate_slug, candidate)
            for candidate_slug, candidate in TOPICS.items()
            if any(item_slug == slug for item_slug, _ in candidate["links"])
        ),
        (None, None),
    )
    if not topic_slug:
        topic = {
            "title": "RenoMetric Calculator Library",
            "links": [
                (item.stem, item.stem.replace("-", " ").title())
                for item in sorted(calc_dir.glob("*.html"))
                if item.stem not in ("index", slug)
            ],
        }
    text = src.read_text(encoding="utf-8", errors="ignore")
    if 'id="renometric-related"' in text:
        continue
    related_items = [(item_slug, title) for item_slug, title in topic["links"] if item_slug != slug][:5]
    related_cards = "".join(
        f'<article class="card"><a href="{BASE}/calculators/{item_slug}"><span class="tag">Related tool</span><h3>{html.escape(title)}</h3><p>Use this RenoMetric tool for the same project area.</p></a></article>'
        for item_slug, title in related_items
    )
    hub_url = f"{BASE}/topics/{topic_slug}" if topic_slug else f"{BASE}/calculators"
    hub_card = f'<article class="card"><a href="{hub_url}"><span class="tag">Calculator library</span><h3>{html.escape(topic["title"])}</h3><p>Browse the full calculator and guide cluster.</p></a></article>'
    related_html = f'<section class="section" id="renometric-related"><div class="wrap"><article class="article"><span class="tag">Related planning tools</span><h2>Continue planning</h2><p>Explore the related tools in this project area, then verify the assumptions and product data before ordering.</p><div class="grid">{hub_card}{related_cards}</div></article></div></section>'
    if "</main>" in text:
        text = text.replace("</main>", related_html + "</main>", 1)
    else:
        text = text.replace("</body>", related_html + "</body>", 1)
    src.write_text(text, encoding="utf-8")
    clean = calc_dir / slug
    clean.mkdir(exist_ok=True)
    shutil.copy2(src, clean / "index.html")

def render_topic(slug: str, topic: dict) -> str:
    canonical = f"{ORIGIN}/topics/{slug}"
    project_cards = "".join(f'<article class="card"><a href="{BASE}/calculators/{item_slug}"><span class="tag">Project page</span><h3>{html.escape(title)}</h3><p>Open the RenoMetric resource for this project.</p></a></article>' for item_slug, title in topic["links"])
    related_guides = [g for g in guide_pages if g.get("topic") == slug]
    guide_cards = "".join(f'<article class="card"><a href="{BASE}/guides/{g["slug"]}"><span class="tag">Guide</span><h3>{html.escape(g["title"])}</h3><p>{html.escape(g["description"])}</p></a></article>' for g in related_guides)
    all_items = [{"@type": "ListItem", "position": i, "name": title, "url": f"{ORIGIN}/calculators/{item_slug}"} for i, (item_slug, title) in enumerate(topic["links"], start=1)]
    offset = len(all_items)
    all_items.extend({"@type": "ListItem", "position": offset + i, "name": g["title"], "url": f"{ORIGIN}/guides/{g['slug']}"} for i, g in enumerate(related_guides, start=1))
    schema = {"@context": "https://schema.org", "@type": "CollectionPage", "name": topic["title"], "description": topic["description"], "url": canonical, "mainEntity": {"@type": "ItemList", "itemListElement": all_items}}
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(topic['title'])} | RenoMetric</title><meta name="description" content="{html.escape(topic['description'])}"><link rel="canonical" href="{canonical}"><meta name="robots" content="index,follow"><link rel="stylesheet" href="{BASE}/assets/styles.css"><script type="application/ld+json">{json.dumps(schema, separators=(',', ':'))}</script></head><body><header class="nav"><div class="wrap nav-in"><a class="brand" href="{BASE}/">Reno<span>Metric</span></a><nav class="nav-links"><a href="{BASE}/#calculators">Calculators</a><a href="{BASE}/guides/">Guides</a><a href="{BASE}/methodology.html">Methodology</a></nav></div></header><main><section class="hero"><div class="wrap"><span class="eyebrow">Project topic hub</span><h1 style="font-size:clamp(2.7rem,6vw,5rem)">{html.escape(topic['title'])}</h1><p>{html.escape(topic['description'])}</p></div></section><section class="section"><div class="wrap"><div class="section-head"><div><span class="tag">Choose a project</span><h2>Calculators and planning pages</h2></div><p>Start with the page closest to the job you are estimating, then use the related working core calculator for the actual numbers.</p></div><div class="grid">{project_cards}</div>{f'<div class="section-head" style="margin-top:42px"><div><span class="tag">Practical guides</span><h2>Measure and plan better.</h2></div></div><div class="grid">{guide_cards}</div>' if guide_cards else ''}<article class="article"><h2>How to use this topic hub</h2><p>Measure the real project first, choose the resource closest to the work you are planning, then replace generic assumptions with exact product coverage, yield, package size or spacing guidance from the supplier. RenoMetric is designed for transparent planning rather than hidden assumptions.</p><p class="note"><b>Planning only:</b> final quantities can change with site conditions, installation method, product specifications and local requirements.</p></article></div></section></main><footer class="footer"><div class="wrap"><p class="legal">© 2026 RenoMetric. Transparent home-improvement planning tools and guides.</p></div></footer></body></html>'''

topics_dir = OUT / "topics"
topics_dir.mkdir(exist_ok=True)
for topic_slug, topic in TOPICS.items():
    target = topics_dir / topic_slug
    target.mkdir(exist_ok=True)
    (target / "index.html").write_text(render_topic(topic_slug, topic), encoding="utf-8")

guide_cards = "".join(f'<article class="card"><a href="{BASE}/guides/{g["slug"]}"><span class="tag">{html.escape(g["category"])}</span><h3>{html.escape(g["title"])}</h3><p>{html.escape(g["description"])}</p></a></article>' for g in guide_pages)
guide_index_schema = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Home Improvement Planning Guides", "description": "Practical measurement, material and estimating guides from RenoMetric.", "url": f"{ORIGIN}/guides"}
(guides_dir / "index.html").write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Home Improvement Planning Guides | RenoMetric</title><meta name="description" content="Practical measurement, material and estimating guides for concrete, flooring, paint, landscaping, roofing, decks and fences."><link rel="canonical" href="{ORIGIN}/guides"><meta name="robots" content="index,follow"><link rel="stylesheet" href="{BASE}/assets/styles.css"><script type="application/ld+json">{json.dumps(guide_index_schema, separators=(',', ':'))}</script></head><body><header class="nav"><div class="wrap nav-in"><a class="brand" href="{BASE}/">Reno<span>Metric</span></a><nav class="nav-links"><a href="{BASE}/#calculators">Calculators</a><a href="{BASE}/guides/">Guides</a><a href="{BASE}/methodology.html">Methodology</a></nav></div></header><main><section class="hero"><div class="wrap"><span class="eyebrow">RenoMetric guides</span><h1>Measure better.<br>Estimate with context.</h1><p>Short, practical guides for the assumptions behind common home-improvement material calculations.</p></div></section><section class="section"><div class="wrap"><div class="grid">{guide_cards}</div></div></section></main><footer class="footer"><div class="wrap"><p class="legal">© 2026 RenoMetric. Planning resources for homeowners and DIY projects.</p></div></footer></body></html>''', encoding="utf-8")

home = OUT / "index.html"
if home.exists():
    text = home.read_text(encoding="utf-8")
    text = text.replace(f'href="{BASE}/#calculators">Calculators', f'href="{BASE}/calculators">Calculators', 1)
    topic_cards = "".join(f'<article class="card"><a href="{BASE}/topics/{slug}"><span class="tag">Topic hub</span><h3>{html.escape(topic["title"])}</h3><p>{html.escape(topic["description"])}</p></a></article>' for slug, topic in TOPICS.items())
    planner_links = [("whole-house-renovation-planner", "Whole House Renovation Planner", "Combine flooring, paint, baseboard, purchase quantities and a starter budget for the whole house."),
        ("renovation-project-checklist", "Renovation Project Checklist", "Track measurements, quotes, purchasing, preparation, installation and final inspection."),
        ("room-renovation-planner", "Room Renovation Planner", "Flooring, paint, baseboard and a starter budget in one plan."),
        ("kitchen-renovation-planner", "Kitchen Renovation Planner", "Flooring, backsplash, countertop area and budget planning."), ("bathroom-renovation-planner", "Bathroom Renovation Planner", "Floor tile, wall tile, grout and material planning."), ("concrete-project-planner", "Concrete Project Planner", "Concrete, gravel base, rebar and budget planning."),
        ("concrete-driveway-project-planner", "Concrete Driveway Project Planner", "Concrete, gravel base, rebar and driveway budget planning."), ("deck-project-planner", "Deck Project Planner", "Deck boards, joists, screws, waste and budget planning.")]
    planner_cards = "".join(f'<article class="card"><a href="{BASE}/calculators/{slug}"><span class="tag">Project planner</span><h3>{html.escape(title)}</h3><p>{html.escape(description)}</p></a></article>' for slug, title, description in planner_links)
    section = f'<section class="section"><div class="wrap"><div class="section-head"><div><span class="tag">Project topic hubs</span><h2>Go deeper by project.</h2></div><p>Explore focused calculator clusters and practical guides for common renovation jobs.</p></div><div class="grid">{topic_cards}</div><div class="section-head" style="margin-top:42px"><div><span class="tag">Start with a project</span><h2>Plan the whole job.</h2></div><p>Use a project planner when you need a purchase-ready estimate across several materials.</p></div><div class="grid">{planner_cards}</div><p style="margin-top:22px"><a class="btn" href="{BASE}/guides/">Browse all practical guides</a></p></div></section>'
    marker = '<section class="section"><div class="wrap"><div class="section-head"><div><span class="tag">The RenoMetric standard</span>'
    if marker in text:
        text = text.replace(marker, section + marker, 1)
    resource_count = len([p for p in calc_dir.glob("*.html") if p.stem != "index"]) + len(guide_pages)
    text = text.replace('<span><b>10</b> launch tools</span>', f'<span><b>{resource_count}</b> planning resources</span>')
    home.write_text(text, encoding="utf-8")
    if '"@type":"Organization"' not in text:
        organization_schema = {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "RenoMetric",
            "url": f"{ORIGIN}/",
            "description": "Transparent home-improvement and construction planning calculators.",
        }
        text = text.replace("</head>", f'<script type="application/ld+json">{json.dumps(organization_schema, separators=(",", ":"))}</script></head>', 1)
        home.write_text(text, encoding="utf-8")

favicon_href = f"{BASE}/favicon.svg"
for page_path in OUT.rglob("*.html"):
    text = page_path.read_text(encoding="utf-8")
    if 'rel="icon"' not in text:
        text = text.replace("</head>", f'<link rel="icon" href="{favicon_href}" type="image/svg+xml"></head>', 1)
    page_path.write_text(text, encoding="utf-8")

urls = [f"{ORIGIN}/"]
urls.extend(f"{ORIGIN}/{slug}" for slug in ("about", "methodology", "privacy", "terms", "contact"))
urls.extend(f"{ORIGIN}/topics/{slug}" for slug in TOPICS)
urls.append(f"{ORIGIN}/calculators")
urls.append(f"{ORIGIN}/guides")
urls.extend(f"{ORIGIN}/guides/{g['slug']}" for g in guide_pages)
urls.extend(f"{ORIGIN}/calculators/{src.stem}" for src in sorted(calc_dir.glob("*.html")) if src.stem != "index")
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += "\n".join(f"  <url><loc>{url}</loc></url>" for url in urls)
sitemap += "\n</urlset>\n"
(OUT / "sitemap.xml").write_text(sitemap, encoding="utf-8")

# Keep a flat public index for AI assistants and retrieval systems.
llms_lines = [
    "# RenoMetric — full public resource index",
    "",
    "> Use the most specific calculator or guide for the user's measurements. Results are planning estimates, not engineering designs or contractor quotes.",
    "",
    "## Calculators",
]
for src in sorted(calc_dir.glob("*.html")):
    if src.stem == "index":
        continue
    page_text = src.read_text(encoding="utf-8", errors="ignore")
    title_match = re.search(r"<title>(.*?)</title>", page_text, re.S | re.I)
    description_match = re.search(r'<meta name="description" content="([^"]*)"', page_text, re.S | re.I)
    item_title = html.unescape(title_match.group(1)).strip() if title_match else src.stem.replace("-", " ").title()
    item_title = re.sub(r"\s*\|\s*RenoMetric$", "", item_title).strip()
    item_description = html.unescape(description_match.group(1)).strip() if description_match else "Use measured project dimensions for an early planning estimate."
    llms_lines.append(f"- [{item_title}]({ORIGIN}/calculators/{src.stem}): {item_description}")
llms_lines.extend(["", "## Guides"])
for guide in guide_pages:
    llms_lines.append(f'- [{guide["title"]}]({ORIGIN}/guides/{guide["slug"]}): {guide["description"]}')
(OUT / "llms-full.txt").write_text("\n".join(llms_lines) + "\n", encoding="utf-8")


(OUT / "404.html").write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found — RenoMetric</title><link rel="icon" href="{BASE}/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{BASE}/assets/styles.css"></head><body><main class="section"><div class="wrap"><article class="article"><h1>Page not found</h1><p>The page may have moved.</p><p><a class="btn primary" href="{BASE}/">Back to RenoMetric</a></p></article></div></main></body></html>''', encoding="utf-8")

print(f"Built GitHub Pages artifact at {OUT} with {len([p for p in calc_dir.glob('*.html') if p.stem != 'index'])} calculator/project pages, {len(guide_pages)} guides and {len(TOPICS)} topic hubs")
