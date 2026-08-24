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
    slug = page.get("slug", "")
    flooring = {"flooring-cost-calculator", "laminate-flooring-calculator", "vinyl-flooring-calculator", "hardwood-flooring-calculator", "carpet-calculator", "room-flooring-calculator", "flooring-box-calculator", "bathroom-tile-calculator", "kitchen-tile-calculator", "paver-calculator"}
    paint = {"wall-paint-calculator", "room-paint-calculator", "ceiling-paint-calculator", "exterior-paint-calculator", "paint-cost-calculator", "paint-gallon-calculator", "paint-coverage-calculator", "fence-paint-calculator", "house-paint-calculator"}
    landscape = {"soil-calculator", "topsoil-calculator", "garden-bed-soil-calculator", "river-rock-calculator"}
    concrete = {"concrete-slab-calculator", "concrete-cost-calculator", "concrete-bag-calculator", "concrete-patio-calculator", "concrete-driveway-calculator", "concrete-footing-calculator", "cubic-yard-calculator", "concrete-waste-calculator", "how-much-concrete-do-i-need"}
    roofing = {"roof-area-calculator", "shingle-calculator", "roofing-material-calculator"}
    if slug in flooring:
        return """<div class="article" style="background:#eef4f0;border-radius:12px"><h2>Working material calculator</h2><div class="grid"><label>Area (ft²)<input id="tool_area" type="number" value="180" min="0" step="any"></label><label>Waste (%)<input id="tool_waste" type="number" value="10" min="0" step="any"></label><label>Package coverage (ft²/box)<input id="tool_pack" type="number" value="20" min="0.1" step="any"></label><label>Price ($/box)<input id="tool_price" type="number" value="45" min="0" step="any"></label></div><button class="btn primary" type="button" onclick="toolFloor()">Calculate</button><div id="tool_result" class="formula">Enter measurements to calculate.</div><script>function toolFloor(){const a=+tool_area.value,w=+tool_waste.value,p=+tool_pack.value,c=+tool_price.value;if(!(a>0&&w>=0&&p>0&&c>=0)){tool_result.textContent='Check the inputs.';return}const q=a*(1+w/100),n=Math.ceil(q/p);tool_result.innerHTML='Purchase quantity: '+q.toFixed(0)+' ft²<br>Packages: '+n+' boxes<br>Material cost: $'+(n*c).toFixed(2)}</script></div>"""
    if slug in paint:
        return """<div class="article" style="background:#eef4f0;border-radius:12px"><h2>Working paint calculator</h2><div class="grid"><label>Surface area (ft²)<input id="tool_area" type="number" value="420" min="0" step="any"></label><label>Openings (ft²)<input id="tool_open" type="number" value="40" min="0" step="any"></label><label>Coats<input id="tool_coats" type="number" value="2" min="1" step="1"></label><label>Coverage (ft²/gal)<input id="tool_cov" type="number" value="350" min="1" step="any"></label><label>Container size (gal)<input id="tool_pack" type="number" value="1" min="0.1" step="any"></label><label>Price ($/container)<input id="tool_price" type="number" value="42" min="0" step="any"></label></div><button class="btn primary" type="button" onclick="toolPaint()">Calculate</button><div id="tool_result" class="formula">Enter measurements to calculate.</div><script>function toolPaint(){const a=+tool_area.value,o=+tool_open.value,co=+tool_coats.value,c=+tool_cov.value,p=+tool_pack.value,pr=+tool_price.value;if(!(a>0&&o>=0&&o<a&&co>0&&c>0&&p>0&&pr>=0)){tool_result.textContent='Check the inputs.';return}const n=Math.ceil((a-o)*co/c/p);tool_result.innerHTML='Paintable area: '+(a-o).toFixed(0)+' ft²<br>Containers: '+n+'<br>Material cost: $'+(n*pr).toFixed(2)}</script></div>"""
    if slug in landscape:
        return """<div class="article" style="background:#eef4f0;border-radius:12px"><h2>Working bulk material calculator</h2><div class="grid"><label>Length (ft)<input id="tool_l" type="number" value="20" min="0" step="any"></label><label>Width (ft)<input id="tool_w" type="number" value="10" min="0" step="any"></label><label>Depth (in)<input id="tool_d" type="number" value="3" min="0" step="any"></label><label>Waste (%)<input id="tool_waste" type="number" value="10" min="0" step="any"></label><label>Density (lb/yd³)<input id="tool_density" type="number" value="2700" min="1" step="any"></label><label>Price ($/ton)<input id="tool_price" type="number" value="55" min="0" step="any"></label></div><button class="btn primary" type="button" onclick="toolBulk()">Calculate</button><div id="tool_result" class="formula">Enter measurements to calculate.</div><script>function toolBulk(){const l=+tool_l.value,w=+tool_w.value,d=+tool_d.value,x=+tool_waste.value,den=+tool_density.value,p=+tool_price.value;if(!(l>0&&w>0&&d>=0&&x>=0&&den>0&&p>=0)){tool_result.textContent='Check the inputs.';return}const yd=l*w*(d/12)/27*(1+x/100),tons=yd*den/2000;tool_result.innerHTML='Order volume: '+yd.toFixed(2)+' yd³<br>Estimated weight: '+tons.toFixed(2)+' short tons<br>Material cost: $'+(tons*p).toFixed(2)}</script></div>"""
    if slug in concrete:
        return """<div class="article" style="background:#eef4f0;border-radius:12px"><h2>Working concrete calculator</h2><div class="grid"><label>Length (ft)<input id="tool_l" type="number" value="20" min="0" step="any"></label><label>Width (ft)<input id="tool_w" type="number" value="12" min="0" step="any"></label><label>Thickness (in)<input id="tool_t" type="number" value="4" min="0" step="any"></label><label>Waste (%)<input id="tool_waste" type="number" value="7" min="0" step="any"></label><label>Price ($/yd³)<input id="tool_price" type="number" value="165" min="0" step="any"></label></div><button class="btn primary" type="button" onclick="toolConcrete()">Calculate</button><div id="tool_result" class="formula">Enter measurements to calculate.</div><script>function toolConcrete(){const l=+tool_l.value,w=+tool_w.value,t=+tool_t.value,x=+tool_waste.value,p=+tool_price.value;if(!(l>0&&w>0&&t>0&&x>=0&&p>=0)){tool_result.textContent='Check the inputs.';return}const yd=l*w*(t/12)/27*(1+x/100);tool_result.innerHTML='Concrete to order: '+yd.toFixed(2)+' yd³<br>Metric volume: '+(yd*.764555).toFixed(2)+' m³<br>Material cost: $'+(yd*p).toFixed(2)}</script></div>"""
    if slug in roofing:
        return """<div class="article" style="background:#eef4f0;border-radius:12px"><h2>Working roofing calculator</h2><div class="grid"><label>Building length (ft)<input id="tool_l" type="number" value="40" min="0" step="any"></label><label>Building width (ft)<input id="tool_w" type="number" value="30" min="0" step="any"></label><label>Slope factor<input id="tool_factor" type="number" value="1.15" min="1" step="any"></label><label>Waste (%)<input id="tool_waste" type="number" value="10" min="0" step="any"></label><label>Bundles per square<input id="tool_bundles" type="number" value="3" min="1" step="any"></label></div><button class="btn primary" type="button" onclick="toolRoof()">Calculate</button><div id="tool_result" class="formula">Enter measurements to calculate.</div><script>function toolRoof(){const l=+tool_l.value,w=+tool_w.value,f=+tool_factor.value,x=+tool_waste.value,b=+tool_bundles.value;if(!(l>0&&w>0&&f>=1&&x>=0&&b>0)){tool_result.textContent='Check the inputs.';return}const area=l*w*f*(1+x/100),sq=area/100;tool_result.innerHTML='Roofing area: '+area.toFixed(0)+' ft²<br>Roofing squares: '+sq.toFixed(2)+'<br>Shingle bundles: '+Math.ceil(sq*b)}</script></div>"""
    if slug == "deck-board-calculator":
        return """<div class="article" style="background:#eef4f0;border-radius:12px"><h2>Working deck board calculator</h2><div class="grid"><label>Deck length (ft)<input id="tool_l" type="number" value="16" min="0" step="any"></label><label>Deck width (ft)<input id="tool_w" type="number" value="12" min="0" step="any"></label><label>Board face width (in)<input id="tool_bw" type="number" value="5.5" min="0.1" step="any"></label><label>Gap (in)<input id="tool_gap" type="number" value="0.125" min="0" step="any"></label><label>Board stock length (ft)<input id="tool_bl" type="number" value="16" min="0.1" step="any"></label><label>Waste (%)<input id="tool_waste" type="number" value="10" min="0" step="any"></label></div><button class="btn primary" type="button" onclick="toolDeck()">Calculate</button><div id="tool_result" class="formula">Enter measurements to calculate.</div><script>function toolDeck(){const l=+tool_l.value,w=+tool_w.value,bw=+tool_bw.value,g=+tool_gap.value,bl=+tool_bl.value,x=+tool_waste.value;if(!(l>0&&w>0&&bw>0&&g>=0&&bl>0&&x>=0)){tool_result.textContent='Check the inputs.';return}const boards=Math.ceil(w*12/(bw+g)*(1+x/100)),feet=boards*l;tool_result.innerHTML='Deck boards: '+boards+'<br>Planned linear feet: '+feet.toFixed(0)}</script></div>"""
    if slug == "fence-post-calculator":
        return """<div class="article" style="background:#eef4f0;border-radius:12px"><h2>Working fence post calculator</h2><div class="grid"><label>Fence length (ft)<input id="tool_l" type="number" value="100" min="0" step="any"></label><label>Post spacing (ft)<input id="tool_s" type="number" value="8" min="0.1" step="any"></label><label>Gate openings (ft)<input id="tool_gate" type="number" value="4" min="0" step="any"></label><label>Extra corner/end posts<input id="tool_extra" type="number" value="2" min="0" step="1"></label></div><button class="btn primary" type="button" onclick="toolFence()">Calculate</button><div id="tool_result" class="formula">Enter measurements to calculate.</div><script>function toolFence(){const l=+tool_l.value,s=+tool_s.value,g=+tool_gate.value,e=+tool_extra.value;if(!(l>0&&s>0&&g>=0&&e>=0)){tool_result.textContent='Check the inputs.';return}const runs=Math.max(0,l-g),posts=Math.ceil(runs/s)+1+e;tool_result.innerHTML='Fence runs: '+runs.toFixed(0)+' ft<br>Planning posts: '+posts}</script></div>"""
    return ""


def _result_actions() -> str:
    return """<div class="tool-actions" style="margin:12px 0;display:flex;gap:8px;flex-wrap:wrap"><button class="btn" type="button" onclick="copyRenoEstimate()">Copy estimate</button><button class="btn" type="button" onclick="window.print()">Print estimate</button></div><script>function copyRenoEstimate(){const title=document.querySelector('h1')?.innerText||'RenoMetric estimate';const result=document.getElementById('tool_result')?.innerText||'';const text=title+'\\n'+result;if(navigator.clipboard){navigator.clipboard.writeText(text).then(()=>alert('Estimate copied.')).catch(()=>{})}}</script>"""


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
    tool = _interactive_tool(page, base)
    actions = _result_actions() if tool else ""
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} | RenoMetric</title><meta name="description" content="{html.escape(description)}"><link rel="canonical" href="{canonical}"><meta name="robots" content="index,follow"><meta property="og:title" content="{html.escape(title)} | RenoMetric"><meta property="og:description" content="{html.escape(description)}"><meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><link rel="stylesheet" href="{base}/assets/styles.css"><script type="application/ld+json">{json.dumps(schema, separators=(',', ':'))}</script></head><body><header class="nav"><div class="wrap nav-in"><a class="brand" href="{base}/">Reno<span>Metric</span></a><nav class="nav-links"><a href="{base}/#calculators">Calculators</a><a href="{base}/methodology.html">Methodology</a><a href="{base}/about.html">About</a></nav></div></header><main><section class="hero"><div class="wrap"><span class="eyebrow">{html.escape(page['category'])}</span><h1 style="font-size:clamp(2.7rem,6vw,5rem)">{html.escape(title)}</h1><p>{html.escape(description)}</p><div class="pill-row"><span class="pill">Planning guide</span><span class="pill">No sign-up</span><span class="pill">Transparent assumptions</span></div></div></section><section class="section"><div class="wrap"><article class="article"><span class="tag">Start with real measurements</span><h2>Quick answer</h2><p>{html.escape(description)} Use the working RenoMetric calculator below for the actual estimate, then use this page to check assumptions, package rounding and project-specific considerations.</p>{tool}{actions}<p><a class="btn primary" href="{parent_url}">Open the working {html.escape(page['parent'].title())} calculator</a></p><h2>Formula</h2><div class="formula">{html.escape(page['formula'])}</div><h2>Worked planning example</h2><p>{html.escape(page['example'])}</p><h2>Common uses</h2><ul>{uses}</ul><h2>How to get a better estimate</h2><p>Measure the actual project rather than relying on listing dimensions. For irregular spaces, split the surface into simple measurable sections and add the results. Use the exact product label for package coverage, yield, density or square-foot coverage whenever it is available.</p><p>Keep waste and package rounding as separate steps. Waste covers cuts, breakage, pattern matching and unavoidable offcuts. Package rounding reflects the fact that many materials are sold only in complete bags, boxes, bundles or cans.</p><p class="note"><b>Before you buy:</b> this page is a planning guide, not a contractor quotation or structural design. Verify final quantities with the product manufacturer, supplier or installer when project conditions could materially change the result.</p><h2>{html.escape(title)} FAQ</h2>{faqs}<h2>Use the calculator</h2><p><a class="pill" href="{parent_url}">Open {html.escape(page['parent'].title())} Calculator</a> <a class="pill" href="{base}/#calculators">Browse all RenoMetric calculators</a></p></article></div></section></main>{_footer(base)}</body></html>'''


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
