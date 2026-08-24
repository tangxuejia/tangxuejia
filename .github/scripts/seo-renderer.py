from __future__ import annotations

import html
import json


def _faq_schema(faqs: list[tuple[str, str]]) -> dict:
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }


def _footer(base: str) -> str:
    return f'''<footer class="footer"><div class="wrap"><div class="footer-grid"><div><a class="brand" href="{base}/">Reno<span>Metric</span></a><p>Fast, transparent planning calculators and practical guides for home improvement and DIY projects.</p></div><div><b>Explore</b><p><a href="{base}/#calculators">Calculators</a><br><a href="{base}/methodology.html">Methodology</a><br><a href="{base}/about.html">About</a></p></div><div><b>Legal</b><p><a href="{base}/privacy.html">Privacy</a><br><a href="{base}/terms.html">Terms</a><br><a href="{base}/contact.html">Contact</a></p></div></div><p class="legal">© 2026 RenoMetric. Estimates are for planning only. Confirm product specifications, site conditions and final quantities with the relevant supplier or qualified professional.</p></div></footer>'''



def _interactive_tool(page: dict, base: str) -> str:
    slug = page.get("slug")
    if slug == "flooring-cost-calculator":
        return f'''<div class="article" style="background:#eef4f0;border-radius:12px"><h2>Working flooring cost calculator</h2><div class="grid"><label>Area (ft²)<input id="ic_area" type="number" value="180" min="0" step="any"></label><label>Waste (%)<input id="ic_waste" type="number" value="10" min="0" step="any"></label><label>Package coverage (ft²/box)<input id="ic_pack" type="number" value="20" min="0.1" step="any"></label><label>Price ($/box)<input id="ic_price" type="number" value="45" min="0" step="any"></label></div><button class="btn primary" type="button" onclick="flooringCostCalc()">Calculate</button><div id="ic_result" class="formula">Enter measurements to calculate.</div><script>function flooringCostCalc(){{const a=+ic_area.value,w=+ic_waste.value,p=+ic_pack.value,price=+ic_price.value;if(!(a>0&&w>=0&&p>0&&price>=0)){{ic_result.textContent='Check the inputs.';return}}const order=a*(1+w/100),boxes=Math.ceil(order/p);ic_result.innerHTML='Purchase area: '+order.toFixed(0)+' ft²<br>Boxes: '+boxes+'<br>Material cost:     title = page["title"]
    description = page["description"]
    canonical = f"{origin}/calculators/{page['slug']}"
    parent_url = f"{base}/calculators/{page['parent']}"
    tool = _interactive_tool(page, base)
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "name": title,
                "description": description,
                "url": canonical,
                "isPartOf": {"@type": "WebSite", "name": "RenoMetric", "url": f"{origin}/"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "RenoMetric", "item": f"{origin}/"},
                    {"@type": "ListItem", "position": 2, "name": "Calculators", "item": f"{origin}/#calculators"},
                    {"@type": "ListItem", "position": 3, "name": title, "item": canonical},
                ],
            },
            _faq_schema(page["faqs"]),
        ],
    }
    uses = "".join(f"<li>{html.escape(x)}</li>" for x in page["uses"])
    faqs = "".join(
        f'<div class="faq"><h3>{html.escape(q)}</h3><p>{html.escape(a)}</p></div>'
        for q, a in page["faqs"]
    )
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} | RenoMetric</title><meta name="description" content="{html.escape(description)}"><link rel="canonical" href="{canonical}"><meta name="robots" content="index,follow"><meta property="og:title" content="{html.escape(title)} | RenoMetric"><meta property="og:description" content="{html.escape(description)}"><meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><link rel="stylesheet" href="{base}/assets/styles.css"><script type="application/ld+json">{json.dumps(schema, separators=(',', ':'))}</script></head><body><header class="nav"><div class="wrap nav-in"><a class="brand" href="{base}/">Reno<span>Metric</span></a><nav class="nav-links"><a href="{base}/#calculators">Calculators</a><a href="{base}/methodology.html">Methodology</a><a href="{base}/about.html">About</a></nav></div></header><main><section class="hero"><div class="wrap"><span class="eyebrow">{html.escape(page['category'])}</span><h1 style="font-size:clamp(2.7rem,6vw,5rem)">{html.escape(title)}</h1><p>{html.escape(description)}</p><div class="pill-row"><span class="pill">Planning guide</span><span class="pill">No sign-up</span><span class="pill">Transparent assumptions</span></div></div></section><section class="section"><div class="wrap"><article class="article"><span class="tag">Start with real measurements</span><h2>Quick answer</h2><p>{html.escape(description)} Use the working RenoMetric calculator below for the actual estimate, then use this page to check assumptions, package rounding and project-specific considerations.</p>{tool}<p><a class="btn primary" href="{parent_url}">Open the working {html.escape(page['parent'].title())} calculator</a></p><h2>Formula</h2><div class="formula">{html.escape(page['formula'])}</div><h2>Worked planning example</h2><p>{html.escape(page['example'])}</p><h2>Common uses</h2><ul>{uses}</ul><h2>How to get a better estimate</h2><p>Measure the actual project rather than relying on listing dimensions. For irregular spaces, split the surface into simple measurable sections and add the results. Use the exact product label for package coverage, yield, density or square-foot coverage whenever it is available.</p><p>Keep waste and package rounding as separate steps. Waste covers cuts, breakage, pattern matching and unavoidable offcuts. Package rounding reflects the fact that many materials are sold only in complete bags, boxes, bundles or cans.</p><p class="note"><b>Before you buy:</b> this page is a planning guide, not a contractor quotation or structural design. Verify final quantities with the product manufacturer, supplier or installer when project conditions could materially change the result.</p><h2>{html.escape(title)} FAQ</h2>{faqs}<h2>Use the calculator</h2><p><a class="pill" href="{parent_url}">Open {html.escape(page['parent'].title())} Calculator</a> <a class="pill" href="{base}/#calculators">Browse all RenoMetric calculators</a></p></article></div></section></main>{_footer(base)}</body></html>'''


def render_guide(page: dict, base: str, origin: str) -> str:
    title = page["title"]
    description = page["description"]
    canonical = f"{origin}/guides/{page['slug']}"
    parent_url = f"{base}/calculators/{page['parent']}"
    steps_html = "".join(
        f'<li><b>{html.escape(step[0])}</b> {html.escape(step[1])}</li>' for step in page["steps"]
    )
    faq_html = "".join(
        f'<div class="faq"><h3>{html.escape(q)}</h3><p>{html.escape(a)}</p></div>'
        for q, a in page["faqs"]
    )
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": title,
                "description": description,
                "mainEntityOfPage": canonical,
                "author": {"@type": "Organization", "name": "RenoMetric"},
                "publisher": {"@type": "Organization", "name": "RenoMetric"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "RenoMetric", "item": f"{origin}/"},
                    {"@type": "ListItem", "position": 2, "name": "Guides", "item": f"{origin}/guides"},
                    {"@type": "ListItem", "position": 3, "name": title, "item": canonical},
                ],
            },
            _faq_schema(page["faqs"]),
        ],
    }
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} | RenoMetric</title><meta name="description" content="{html.escape(description)}"><link rel="canonical" href="{canonical}"><meta name="robots" content="index,follow"><meta property="og:title" content="{html.escape(title)} | RenoMetric"><meta property="og:description" content="{html.escape(description)}"><meta property="og:type" content="article"><meta property="og:url" content="{canonical}"><link rel="stylesheet" href="{base}/assets/styles.css"><script type="application/ld+json">{json.dumps(schema, separators=(',', ':'))}</script></head><body><header class="nav"><div class="wrap nav-in"><a class="brand" href="{base}/">Reno<span>Metric</span></a><nav class="nav-links"><a href="{base}/#calculators">Calculators</a><a href="{base}/guides/">Guides</a><a href="{base}/methodology.html">Methodology</a></nav></div></header><main><section class="hero"><div class="wrap"><span class="eyebrow">{html.escape(page['category'])} guide</span><h1 style="font-size:clamp(2.7rem,6vw,5rem)">{html.escape(title)}</h1><p>{html.escape(description)}</p></div></section><section class="section"><div class="wrap"><article class="article"><h2>Quick answer</h2><p>{html.escape(page['answer'])}</p><p><a class="btn primary" href="{parent_url}">Use the related calculator</a></p><h2>Step by step</h2><ol>{steps_html}</ol><h2>Formula or rule of thumb</h2><div class="formula">{html.escape(page['formula'])}</div><h2>Example</h2><p>{html.escape(page['example'])}</p><h2>Common mistakes</h2><p>{html.escape(page['mistakes'])}</p><p class="note"><b>Planning note:</b> product yields, installation methods, site conditions and local requirements can change the final quantity. Use the exact manufacturer or supplier information before purchasing.</p><h2>FAQ</h2>{faq_html}<h2>Related tool</h2><p><a class="pill" href="{parent_url}">Open the related calculator</a> <a class="pill" href="{base}/guides/">Browse all guides</a></p></article></div></section></main>{_footer(base)}</body></html>'''
+(boxes*price).toFixed(2)}}</script></div>'''
    if slug == "wall-paint-calculator":
        return f'''<div class="article" style="background:#eef4f0;border-radius:12px"><h2>Working wall paint calculator</h2><div class="grid"><label>Wall area (ft²)<input id="ip_area" type="number" value="420" min="0" step="any"></label><label>Openings (ft²)<input id="ip_open" type="number" value="40" min="0" step="any"></label><label>Coats<input id="ip_coats" type="number" value="2" min="1" step="1"></label><label>Coverage (ft²/gal)<input id="ip_cov" type="number" value="350" min="1" step="any"></label><label>Container size (gal)<input id="ip_pack" type="number" value="1" min="0.1" step="any"></label></div><button class="btn primary" type="button" onclick="wallPaintCalc()">Calculate</button><div id="ip_result" class="formula">Enter measurements to calculate.</div><script>function wallPaintCalc(){{const a=+ip_area.value,o=+ip_open.value,co=+ip_coats.value,c=+ip_cov.value,p=+ip_pack.value;if(!(a>0&&o>=0&&o<a&&co>0&&c>0&&p>0)){{ip_result.textContent='Check the inputs.';return}}const gallons=Math.ceil((a-o)*co/c/p);ip_result.innerHTML='Paintable area: '+(a-o).toFixed(0)+' ft²<br>Containers: '+gallons}}</script></div>'''
    if slug == "roof-area-calculator":
        return f'''<div class="article" style="background:#eef4f0;border-radius:12px"><h2>Working roof area calculator</h2><div class="grid"><label>Building length (ft)<input id="ir_l" type="number" value="40" min="0" step="any"></label><label>Building width (ft)<input id="ir_w" type="number" value="30" min="0" step="any"></label><label>Roof slope factor<input id="ir_factor" type="number" value="1.15" min="1" step="any"></label><label>Waste (%)<input id="ir_waste" type="number" value="10" min="0" step="any"></label></div><button class="btn primary" type="button" onclick="roofAreaCalc()">Calculate</button><div id="ir_result" class="formula">Enter measurements to calculate.</div><script>function roofAreaCalc(){{const l=+ir_l.value,w=+ir_w.value,f=+ir_factor.value,x=+ir_waste.value;if(!(l>0&&w>0&&f>=1&&x>=0)){{ir_result.textContent='Check the inputs.';return}}const area=l*w*f*(1+x/100);ir_result.innerHTML='Roof area with waste: '+area.toFixed(0)+' ft²<br>Roofing squares: '+(area/100).toFixed(2)}}</script></div>'''
    return ""

def render_planning_page(page: dict, base: str, origin: str) -> str:
    title = page["title"]
    description = page["description"]
    canonical = f"{origin}/calculators/{page['slug']}"
    parent_url = f"{base}/calculators/{page['parent']}"
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "name": title,
                "description": description,
                "url": canonical,
                "isPartOf": {"@type": "WebSite", "name": "RenoMetric", "url": f"{origin}/"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "RenoMetric", "item": f"{origin}/"},
                    {"@type": "ListItem", "position": 2, "name": "Calculators", "item": f"{origin}/#calculators"},
                    {"@type": "ListItem", "position": 3, "name": title, "item": canonical},
                ],
            },
            _faq_schema(page["faqs"]),
        ],
    }
    uses = "".join(f"<li>{html.escape(x)}</li>" for x in page["uses"])
    faqs = "".join(
        f'<div class="faq"><h3>{html.escape(q)}</h3><p>{html.escape(a)}</p></div>'
        for q, a in page["faqs"]
    )
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} | RenoMetric</title><meta name="description" content="{html.escape(description)}"><link rel="canonical" href="{canonical}"><meta name="robots" content="index,follow"><meta property="og:title" content="{html.escape(title)} | RenoMetric"><meta property="og:description" content="{html.escape(description)}"><meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><link rel="stylesheet" href="{base}/assets/styles.css"><script type="application/ld+json">{json.dumps(schema, separators=(',', ':'))}</script></head><body><header class="nav"><div class="wrap nav-in"><a class="brand" href="{base}/">Reno<span>Metric</span></a><nav class="nav-links"><a href="{base}/#calculators">Calculators</a><a href="{base}/methodology.html">Methodology</a><a href="{base}/about.html">About</a></nav></div></header><main><section class="hero"><div class="wrap"><span class="eyebrow">{html.escape(page['category'])}</span><h1 style="font-size:clamp(2.7rem,6vw,5rem)">{html.escape(title)}</h1><p>{html.escape(description)}</p><div class="pill-row"><span class="pill">Planning guide</span><span class="pill">No sign-up</span><span class="pill">Transparent assumptions</span></div></div></section><section class="section"><div class="wrap"><article class="article"><span class="tag">Start with real measurements</span><h2>Quick answer</h2><p>{html.escape(description)} Use the working RenoMetric calculator below for the actual estimate, then use this page to check assumptions, package rounding and project-specific considerations.</p><p><a class="btn primary" href="{parent_url}">Open the working {html.escape(page['parent'].title())} calculator</a></p><h2>Formula</h2><div class="formula">{html.escape(page['formula'])}</div><h2>Worked planning example</h2><p>{html.escape(page['example'])}</p><h2>Common uses</h2><ul>{uses}</ul><h2>How to get a better estimate</h2><p>Measure the actual project rather than relying on listing dimensions. For irregular spaces, split the surface into simple measurable sections and add the results. Use the exact product label for package coverage, yield, density or square-foot coverage whenever it is available.</p><p>Keep waste and package rounding as separate steps. Waste covers cuts, breakage, pattern matching and unavoidable offcuts. Package rounding reflects the fact that many materials are sold only in complete bags, boxes, bundles or cans.</p><p class="note"><b>Before you buy:</b> this page is a planning guide, not a contractor quotation or structural design. Verify final quantities with the product manufacturer, supplier or installer when project conditions could materially change the result.</p><h2>{html.escape(title)} FAQ</h2>{faqs}<h2>Use the calculator</h2><p><a class="pill" href="{parent_url}">Open {html.escape(page['parent'].title())} Calculator</a> <a class="pill" href="{base}/#calculators">Browse all RenoMetric calculators</a></p></article></div></section></main>{_footer(base)}</body></html>'''


def render_guide(page: dict, base: str, origin: str) -> str:
    title = page["title"]
    description = page["description"]
    canonical = f"{origin}/guides/{page['slug']}"
    parent_url = f"{base}/calculators/{page['parent']}"
    steps_html = "".join(
        f'<li><b>{html.escape(step[0])}</b> {html.escape(step[1])}</li>' for step in page["steps"]
    )
    faq_html = "".join(
        f'<div class="faq"><h3>{html.escape(q)}</h3><p>{html.escape(a)}</p></div>'
        for q, a in page["faqs"]
    )
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": title,
                "description": description,
                "mainEntityOfPage": canonical,
                "author": {"@type": "Organization", "name": "RenoMetric"},
                "publisher": {"@type": "Organization", "name": "RenoMetric"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "RenoMetric", "item": f"{origin}/"},
                    {"@type": "ListItem", "position": 2, "name": "Guides", "item": f"{origin}/guides"},
                    {"@type": "ListItem", "position": 3, "name": title, "item": canonical},
                ],
            },
            _faq_schema(page["faqs"]),
        ],
    }
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} | RenoMetric</title><meta name="description" content="{html.escape(description)}"><link rel="canonical" href="{canonical}"><meta name="robots" content="index,follow"><meta property="og:title" content="{html.escape(title)} | RenoMetric"><meta property="og:description" content="{html.escape(description)}"><meta property="og:type" content="article"><meta property="og:url" content="{canonical}"><link rel="stylesheet" href="{base}/assets/styles.css"><script type="application/ld+json">{json.dumps(schema, separators=(',', ':'))}</script></head><body><header class="nav"><div class="wrap nav-in"><a class="brand" href="{base}/">Reno<span>Metric</span></a><nav class="nav-links"><a href="{base}/#calculators">Calculators</a><a href="{base}/guides/">Guides</a><a href="{base}/methodology.html">Methodology</a></nav></div></header><main><section class="hero"><div class="wrap"><span class="eyebrow">{html.escape(page['category'])} guide</span><h1 style="font-size:clamp(2.7rem,6vw,5rem)">{html.escape(title)}</h1><p>{html.escape(description)}</p></div></section><section class="section"><div class="wrap"><article class="article"><h2>Quick answer</h2><p>{html.escape(page['answer'])}</p><p><a class="btn primary" href="{parent_url}">Use the related calculator</a></p><h2>Step by step</h2><ol>{steps_html}</ol><h2>Formula or rule of thumb</h2><div class="formula">{html.escape(page['formula'])}</div><h2>Example</h2><p>{html.escape(page['example'])}</p><h2>Common mistakes</h2><p>{html.escape(page['mistakes'])}</p><p class="note"><b>Planning note:</b> product yields, installation methods, site conditions and local requirements can change the final quantity. Use the exact manufacturer or supplier information before purchasing.</p><h2>FAQ</h2>{faq_html}<h2>Related tool</h2><p><a class="pill" href="{parent_url}">Open the related calculator</a> <a class="pill" href="{base}/guides/">Browse all guides</a></p></article></div></section></main>{_footer(base)}</body></html>'''
