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
