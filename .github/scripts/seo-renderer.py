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
    return f'''<footer class="footer"><div class="wrap"><div class="footer-grid"><div><a class="brand" href="{base}/">Reno<span>Metric</span></a><p>Fast, transparent planning calculators and practical guides for home improvement and DIY projects.</p></div><div><b>Explore</b><p><a href="{base}/calculators">Calculators</a><br><a href="{base}/methodology.html">Methodology</a><br><a href="{base}/about.html">About</a></p></div><div><b>Legal</b><p><a href="{base}/privacy.html">Privacy</a><br><a href="{base}/terms.html">Terms</a><br><a href="{base}/contact.html">Contact</a></p></div></div><p class="legal">© 2026 RenoMetric. Estimates are for planning only. Confirm product specifications, site conditions and final quantities with the relevant supplier or qualified professional.</p></div></footer>'''



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
    if slug == "deck-mud-calculator":
        return """<div class="article" style="background:#eef4f0;border-radius:12px"><h2>Working deck mud calculator</h2><div class="grid"><label>Length (ft)<input id="tool_l" type="number" value="4" min="0" step="any"></label><label>Width (ft)<input id="tool_w" type="number" value="4" min="0" step="any"></label><label>Average depth (in)<input id="tool_d" type="number" value="2" min="0" step="any"></label><label>Waste (%)<input id="tool_waste" type="number" value="10" min="0" step="any"></label><label>Yield per bag (ft³)<input id="tool_yield" type="number" value="0.5" min="0.01" step="any"></label></div><button class="btn primary" type="button" onclick="toolDeckMud()">Calculate</button><div id="tool_result" class="formula">Enter measurements to calculate.</div><script>function toolDeckMud(){const l=+tool_l.value,w=+tool_w.value,d=+tool_d.value,x=+tool_waste.value,y=+tool_yield.value;if(!(l>0&&w>0&&d>0&&x>=0&&y>0)){tool_result.textContent='Check the inputs.';return}const ft=l*w*d/12,adj=ft*(1+x/100),bags=Math.ceil(adj/y);tool_result.innerHTML='Dry-pack volume: '+adj.toFixed(2)+' ft³<br>Estimated bags: '+bags+'<br>Use the exact labeled yield before ordering.'}</script></div>"""
    if slug == "marble-quantity-calculator":
        return """<div class="article" style="background:#eef4f0;border-radius:12px"><h2>Working marble quantity calculator</h2><div class="grid"><label>Surface area (ft²)<input id="tool_area" type="number" value="60" min="0" step="any"></label><label>Tile length (in)<input id="tool_tl" type="number" value="12" min="0.1" step="any"></label><label>Tile width (in)<input id="tool_tw" type="number" value="24" min="0.1" step="any"></label><label>Waste (%)<input id="tool_waste" type="number" value="12" min="0" step="any"></label><label>Tiles per box<input id="tool_box" type="number" value="4" min="1" step="1"></label></div><button class="btn primary" type="button" onclick="toolMarble()">Calculate</button><div id="tool_result" class="formula">Enter measurements to calculate.</div><script>function toolMarble(){const a=+tool_area.value,tl=+tool_tl.value,tw=+tool_tw.value,x=+tool_waste.value,b=+tool_box.value;if(!(a>0&&tl>0&&tw>0&&x>=0&&b>0)){tool_result.textContent='Check the inputs.';return}const tileArea=tl*tw/144,planned=a*(1+x/100),pieces=Math.ceil(planned/tileArea),boxes=Math.ceil(pieces/b);tool_result.innerHTML='Planned coverage: '+planned.toFixed(1)+' ft²<br>Marble pieces: '+pieces+'<br>Boxes: '+boxes+'<br>Vein matching and layout cuts may increase waste.'}</script></div>"""
    if slug == "self-leveling-calculator":
        return """<div class="article" style="background:#eef4f0;border-radius:12px"><h2>Working self-leveling calculator</h2><div class="grid"><label>Floor area (ft²)<input id="tool_area" type="number" value="200" min="0" step="any"></label><label>Average depth (in)<input id="tool_d" type="number" value="0.25" min="0" step="any"></label><label>Waste (%)<input id="tool_waste" type="number" value="10" min="0" step="any"></label><label>Yield per bag (ft³)<input id="tool_yield" type="number" value="0.45" min="0.01" step="any"></label></div><button class="btn primary" type="button" onclick="toolLeveler()">Calculate</button><div id="tool_result" class="formula">Enter measurements to calculate.</div><script>function toolLeveler(){const a=+tool_area.value,d=+tool_d.value,x=+tool_waste.value,y=+tool_yield.value;if(!(a>0&&d>0&&x>=0&&y>0)){tool_result.textContent='Check the inputs.';return}const v=a*d/12*(1+x/100),bags=Math.ceil(v/y);tool_result.innerHTML='Adjusted volume: '+v.toFixed(2)+' ft³<br>Estimated bags: '+bags+'<br>Confirm primer, depth limits and product yield.'}</script></div>"""
    if slug == "floor-mud-calculator":
        return """<div class="article" style="background:#eef4f0;border-radius:12px"><h2>Working floor mud calculator</h2><div class="grid"><label>Length (ft)<input id="tool_l" type="number" value="5" min="0" step="any"></label><label>Width (ft)<input id="tool_w" type="number" value="6" min="0" step="any"></label><label>Average bed thickness (in)<input id="tool_d" type="number" value="1.5" min="0" step="any"></label><label>Waste (%)<input id="tool_waste" type="number" value="10" min="0" step="any"></label><label>Yield per bag (ft³)<input id="tool_yield" type="number" value="0.5" min="0.01" step="any"></label></div><button class="btn primary" type="button" onclick="toolFloorMud()">Calculate</button><div id="tool_result" class="formula">Enter measurements to calculate.</div><script>function toolFloorMud(){const l=+tool_l.value,w=+tool_w.value,d=+tool_d.value,x=+tool_waste.value,y=+tool_yield.value;if(!(l>0&&w>0&&d>0&&x>=0&&y>0)){tool_result.textContent='Check the inputs.';return}const v=l*w*d/12*(1+x/100),bags=Math.ceil(v/y);tool_result.innerHTML='Adjusted mortar volume: '+v.toFixed(2)+' ft³<br>Estimated bags: '+bags+'<br>Confirm slope, substrate and system instructions.'}</script></div>"""
    if slug == "tuckpointing-calculator":
        return """<div class="article" style="background:#eef4f0;border-radius:12px"><h2>Working tuckpointing calculator</h2><div class="grid"><label>Joint length (linear ft)<input id="tool_l" type="number" value="500" min="0" step="any"></label><label>Joint width (in)<input id="tool_w" type="number" value="0.375" min="0" step="any"></label><label>Joint depth (in)<input id="tool_d" type="number" value="0.75" min="0" step="any"></label><label>Waste (%)<input id="tool_waste" type="number" value="20" min="0" step="any"></label><label>Yield per bag (ft³)<input id="tool_yield" type="number" value="0.5" min="0.01" step="any"></label></div><button class="btn primary" type="button" onclick="toolTuckpoint()">Calculate</button><div id="tool_result" class="formula">Enter measurements to calculate.</div><script>function toolTuckpoint(){const l=+tool_l.value,w=+tool_w.value,d=+tool_d.value,x=+tool_waste.value,y=+tool_yield.value;if(!(l>0&&w>0&&d>0&&x>=0&&y>0)){tool_result.textContent='Check the inputs.';return}const v=l*(w/12)*(d/12)*(1+x/100),bags=Math.ceil(v/y);tool_result.innerHTML='Adjusted mortar volume: '+v.toFixed(2)+' ft³<br>Estimated bags: '+bags+'<br>Mortar compatibility and joint preparation require verification.'}</script></div>"""
    if slug == "concrete-screed-calculator":
        return """<div class="article" style="background:#eef4f0;border-radius:12px"><h2>Working concrete screed calculator</h2><div class="grid"><label>Length (ft)<input id="tool_l" type="number" value="20" min="0" step="any"></label><label>Width (ft)<input id="tool_w" type="number" value="12" min="0" step="any"></label><label>Thickness (in)<input id="tool_t" type="number" value="4" min="0" step="any"></label><label>Waste (%)<input id="tool_waste" type="number" value="7" min="0" step="any"></label></div><button class="btn primary" type="button" onclick="toolScreed()">Calculate</button><div id="tool_result" class="formula">Enter measurements to calculate.</div><script>function toolScreed(){const l=+tool_l.value,w=+tool_w.value,t=+tool_t.value,x=+tool_waste.value;if(!(l>0&&w>0&&t>0&&x>=0)){tool_result.textContent='Check the inputs.';return}const yd=l*w*(t/12)/27*(1+x/100);tool_result.innerHTML='Concrete to order: '+yd.toFixed(2)+' yd³<br>Metric volume: '+(yd*.764555).toFixed(2)+' m³<br>Confirm placement, access and supplier order increments.'}</script></div>"""
    return ""


def _metric_tool(page: dict) -> str:
    slug = page.get("slug", "")
    flooring = {"flooring-cost-calculator", "laminate-flooring-calculator", "vinyl-flooring-calculator", "hardwood-flooring-calculator", "carpet-calculator", "room-flooring-calculator", "flooring-box-calculator", "bathroom-tile-calculator", "kitchen-tile-calculator", "paver-calculator"}
    paint = {"wall-paint-calculator", "room-paint-calculator", "ceiling-paint-calculator", "exterior-paint-calculator", "paint-cost-calculator", "paint-gallon-calculator", "paint-coverage-calculator", "fence-paint-calculator", "house-paint-calculator"}
    landscape = {"soil-calculator", "topsoil-calculator", "garden-bed-soil-calculator", "river-rock-calculator"}
    concrete = {"concrete-slab-calculator", "concrete-cost-calculator", "concrete-bag-calculator", "concrete-patio-calculator", "concrete-driveway-calculator", "concrete-footing-calculator", "cubic-yard-calculator", "concrete-waste-calculator", "how-much-concrete-do-i-need"}
    roofing = {"roof-area-calculator", "shingle-calculator", "roofing-material-calculator"}
    if slug in flooring:
        return """<details class="article" style="margin-top:16px"><summary><b>Use Metric inputs (m² and package coverage)</b></summary><div class="grid"><label>Area (m²)<input id="metric_area" type="number" value="16.7" min="0" step="any"></label><label>Waste (%)<input id="metric_waste" type="number" value="10" min="0" step="any"></label><label>Package coverage (m²/box)<input id="metric_pack" type="number" value="1.86" min="0.01" step="any"></label><label>Price ($/box)<input id="metric_price" type="number" value="45" min="0" step="any"></label></div><button class="btn primary" type="button" onclick="metricFloor()">Calculate Metric estimate</button><div id="metric_result" class="formula">Enter metric measurements.</div><script>function metricFloor(){const a=+metric_area.value,w=+metric_waste.value,p=+metric_pack.value,c=+metric_price.value;if(!(a>0&&w>=0&&p>0&&c>=0)){metric_result.textContent='Check the metric inputs.';return}const q=a*(1+w/100),n=Math.ceil(q/p);metric_result.innerHTML='Purchase quantity: '+q.toFixed(2)+' m²<br>Packages: '+n+' boxes<br>Material cost: $'+(n*c).toFixed(2)}</script></details>"""
    if slug in paint:
        return """<details class="article" style="margin-top:16px"><summary><b>Use Metric inputs (m² and liters)</b></summary><div class="grid"><label>Surface area (m²)<input id="metric_area" type="number" value="39" min="0" step="any"></label><label>Openings (m²)<input id="metric_open" type="number" value="3.7" min="0" step="any"></label><label>Coats<input id="metric_coats" type="number" value="2" min="1" step="1"></label><label>Coverage (m²/L)<input id="metric_cov" type="number" value="9" min="0.1" step="any"></label><label>Container size (L)<input id="metric_pack" type="number" value="3.78" min="0.1" step="any"></label><label>Price ($/container)<input id="metric_price" type="number" value="42" min="0" step="any"></label></div><button class="btn primary" type="button" onclick="metricPaint()">Calculate Metric estimate</button><div id="metric_result" class="formula">Enter metric measurements.</div><script>function metricPaint(){const a=+metric_area.value,o=+metric_open.value,co=+metric_coats.value,c=+metric_cov.value,p=+metric_pack.value,pr=+metric_price.value;if(!(a>0&&o>=0&&o<a&&co>0&&c>0&&p>0&&pr>=0)){metric_result.textContent='Check the metric inputs.';return}const liters=(a-o)*co/c,n=Math.ceil(liters/p);metric_result.innerHTML='Paintable area: '+(a-o).toFixed(2)+' m²<br>Paint needed: '+liters.toFixed(2)+' L<br>Containers: '+n+'<br>Material cost: $'+(n*pr).toFixed(2)}</script></details>"""
    if slug in landscape:
        return """<details class="article" style="margin-top:16px"><summary><b>Use Metric inputs (m, cm, m³ and metric tonnes)</b></summary><div class="grid"><label>Length (m)<input id="metric_l" type="number" value="6.1" min="0" step="any"></label><label>Width (m)<input id="metric_w" type="number" value="3.05" min="0" step="any"></label><label>Depth (cm)<input id="metric_d" type="number" value="7.5" min="0" step="any"></label><label>Waste (%)<input id="metric_waste" type="number" value="10" min="0" step="any"></label><label>Density (kg/m³)<input id="metric_density" type="number" value="1600" min="1" step="any"></label><label>Price ($/metric tonne)<input id="metric_price" type="number" value="55" min="0" step="any"></label></div><button class="btn primary" type="button" onclick="metricBulk()">Calculate Metric estimate</button><div id="metric_result" class="formula">Enter metric measurements.</div><script>function metricBulk(){const l=+metric_l.value,w=+metric_w.value,d=+metric_d.value,x=+metric_waste.value,den=+metric_density.value,p=+metric_price.value;if(!(l>0&&w>0&&d>=0&&x>=0&&den>0&&p>=0)){metric_result.textContent='Check the metric inputs.';return}const m3=l*w*(d/100)*(1+x/100),tons=m3*den/1000;metric_result.innerHTML='Order volume: '+m3.toFixed(2)+' m³<br>Estimated weight: '+tons.toFixed(2)+' metric tonnes<br>Material cost: $'+(tons*p).toFixed(2)}</script></details>"""
    if slug in concrete:
        return """<details class="article" style="margin-top:16px"><summary><b>Use Metric inputs (m, cm and m³)</b></summary><div class="grid"><label>Length (m)<input id="metric_l" type="number" value="6.1" min="0" step="any"></label><label>Width (m)<input id="metric_w" type="number" value="3.66" min="0" step="any"></label><label>Thickness (cm)<input id="metric_t" type="number" value="10" min="0" step="any"></label><label>Waste (%)<input id="metric_waste" type="number" value="7" min="0" step="any"></label><label>Price ($/m³)<input id="metric_price" type="number" value="215" min="0" step="any"></label></div><button class="btn primary" type="button" onclick="metricConcrete()">Calculate Metric estimate</button><div id="metric_result" class="formula">Enter metric measurements.</div><script>function metricConcrete(){const l=+metric_l.value,w=+metric_w.value,t=+metric_t.value,x=+metric_waste.value,p=+metric_price.value;if(!(l>0&&w>0&&t>0&&x>=0&&p>=0)){metric_result.textContent='Check the metric inputs.';return}const m3=l*w*(t/100)*(1+x/100);metric_result.innerHTML='Concrete to order: '+m3.toFixed(2)+' m³<br>Material cost: $'+(m3*p).toFixed(2)}</script></details>"""
    if slug in roofing:
        return """<details class="article" style="margin-top:16px"><summary><b>Use Metric inputs (m²)</b></summary><div class="grid"><label>Building length (m)<input id="metric_l" type="number" value="12.2" min="0" step="any"></label><label>Building width (m)<input id="metric_w" type="number" value="9.14" min="0" step="any"></label><label>Slope factor<input id="metric_factor" type="number" value="1.15" min="1" step="any"></label><label>Waste (%)<input id="metric_waste" type="number" value="10" min="0" step="any"></label><label>Bundles per square<input id="metric_bundles" type="number" value="3" min="1" step="any"></label></div><button class="btn primary" type="button" onclick="metricRoof()">Calculate Metric estimate</button><div id="metric_result" class="formula">Enter metric measurements.</div><script>function metricRoof(){const l=+metric_l.value,w=+metric_w.value,f=+metric_factor.value,x=+metric_waste.value,b=+metric_bundles.value;if(!(l>0&&w>0&&f>=1&&x>=0&&b>0)){metric_result.textContent='Check the metric inputs.';return}const area=l*w*f*(1+x/100),squares=area/9.2903;metric_result.innerHTML='Roofing area: '+area.toFixed(2)+' m²<br>Roofing squares: '+squares.toFixed(2)+'<br>Shingle bundles: '+Math.ceil(squares*b)}</script></details>"""
    if slug == "deck-board-calculator":
        return """<details class="article" style="margin-top:16px"><summary><b>Use Metric inputs (m and cm)</b></summary><div class="grid"><label>Deck length (m)<input id="metric_l" type="number" value="4.88" min="0" step="any"></label><label>Deck width (m)<input id="metric_w" type="number" value="3.66" min="0" step="any"></label><label>Board face width (cm)<input id="metric_bw" type="number" value="14" min="0.1" step="any"></label><label>Gap (cm)<input id="metric_gap" type="number" value="0.32" min="0" step="any"></label><label>Board stock length (m)<input id="metric_bl" type="number" value="4.88" min="0.1" step="any"></label><label>Waste (%)<input id="metric_waste" type="number" value="10" min="0" step="any"></label></div><button class="btn primary" type="button" onclick="metricDeck()">Calculate Metric estimate</button><div id="metric_result" class="formula">Enter metric measurements.</div><script>function metricDeck(){const l=+metric_l.value,w=+metric_w.value,bw=+metric_bw.value,g=+metric_gap.value,bl=+metric_bl.value,x=+metric_waste.value;if(!(l>0&&w>0&&bw>0&&g>=0&&bl>0&&x>=0)){metric_result.textContent='Check the metric inputs.';return}const boards=Math.ceil(w*100/(bw+g)*(1+x/100)),meters=boards*l;metric_result.innerHTML='Deck boards: '+boards+'<br>Planned linear meters: '+meters.toFixed(2)}</script></details>"""
    if slug == "fence-post-calculator":
        return """<details class="article" style="margin-top:16px"><summary><b>Use Metric inputs (m)</b></summary><div class="grid"><label>Fence length (m)<input id="metric_l" type="number" value="30.5" min="0" step="any"></label><label>Post spacing (m)<input id="metric_s" type="number" value="2.44" min="0.1" step="any"></label><label>Gate openings (m)<input id="metric_gate" type="number" value="1.22" min="0" step="any"></label><label>Extra corner/end posts<input id="metric_extra" type="number" value="2" min="0" step="1"></label></div><button class="btn primary" type="button" onclick="metricFence()">Calculate Metric estimate</button><div id="metric_result" class="formula">Enter metric measurements.</div><script>function metricFence(){const l=+metric_l.value,s=+metric_s.value,g=+metric_gate.value,e=+metric_extra.value;if(!(l>0&&s>0&&g>=0&&e>=0)){metric_result.textContent='Check the metric inputs.';return}const runs=Math.max(0,l-g),posts=Math.ceil(runs/s)+1+e;metric_result.innerHTML='Fence runs: '+runs.toFixed(2)+' m<br>Planning posts: '+posts}</script></details>"""
    return ""


def _result_actions() -> str:
    return """<div class="tool-actions" style="margin:12px 0;display:flex;gap:8px;flex-wrap:wrap"><button class="btn" type="button" onclick="copyRenoEstimate()">Copy estimate</button><button class="btn" type="button" onclick="window.print()">Print estimate</button><button class="btn" type="button" onclick="shareRenoEstimate()">Share</button><span id="reno-action-status" aria-live="polite"></span></div><script>function renoEstimateText(){const title=document.querySelector('h1')?.innerText||'RenoMetric estimate';const result=document.getElementById('tool_result')?.innerText||'';return title+'\\n'+result}function copyRenoEstimate(){const text=renoEstimateText(),status=document.getElementById('reno-action-status');if(!navigator.clipboard){if(status)status.textContent='Copy is unavailable in this browser.';return}navigator.clipboard.writeText(text).then(()=>{if(status)status.textContent='Estimate copied.'}).catch(()=>{if(status)status.textContent='Copy failed.'})}function shareRenoEstimate(){const text=renoEstimateText(),status=document.getElementById('reno-action-status');if(navigator.share){navigator.share({title:document.querySelector('h1')?.innerText||'RenoMetric estimate',text:text,url:location.href}).catch(()=>{});return}if(navigator.clipboard){navigator.clipboard.writeText(text).then(()=>{if(status)status.textContent='Copied for sharing.'}).catch(()=>{if(status)status.textContent='Sharing is unavailable.'})}else if(status)status.textContent='Sharing is unavailable.'}</script>"""


def _purchase_checklist() -> str:
    return """<div class="article" style="margin-top:16px;background:#fff8e8;border-left:4px solid #d99b2b"><h2>Before you buy</h2><div class="grid"><label><input type="checkbox"> Re-check the measured dimensions</label><label><input type="checkbox"> Confirm product yield or package coverage</label><label><input type="checkbox"> Add waste and whole-package rounding</label><label><input type="checkbox"> Confirm delivery, tax and supplier fees</label><label><input type="checkbox"> Check local code or professional requirements</label></div><p class="note">Use the calculator result as a planning quantity, then verify the final order with the product label or supplier quote.</p></div>"""



def _decision_promise() -> str:
    return """<div class="article" style="margin:16px 0;background:#eef4f0;border:1px solid #cfe2d7;border-radius:12px"><h2>What you will get</h2><div class="grid"><div><b>1. Needed</b><p>Use your measurements to see the estimated project quantity.</p></div><div><b>2. Buy</b><p>Add waste and round to complete bags, boxes, cans, bundles or delivery quantities.</p></div><div><b>3. Check</b><p>Review product coverage, site conditions, local requirements and supplier details before ordering.</p></div></div></div>"""



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
                "dateModified": "2026-08-27",
                "author": {"@type": "Organization", "name": "RenoMetric"},
            },
            {
                "@type": "WebApplication",
                "name": title,
                "description": description,
                "url": canonical,
                "applicationCategory": "UtilitiesApplication",
                "operatingSystem": "Any",
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "RenoMetric", "item": f"{origin}/"},
                    {"@type": "ListItem", "position": 2, "name": "Calculators", "item": f"{origin}/calculators"},
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
    actions = _metric_tool(page) + _purchase_checklist() + (_result_actions() if tool else "")
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} | RenoMetric</title><meta name="description" content="{html.escape(description)}"><link rel="canonical" href="{canonical}"><meta name="robots" content="index,follow"><meta property="og:title" content="{html.escape(title)} | RenoMetric"><meta property="og:description" content="{html.escape(description)}"><meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><link rel="stylesheet" href="{base}/assets/styles.css"><script type="application/ld+json">{json.dumps(schema, separators=(',', ':'))}</script></head><body><header class="nav"><div class="wrap nav-in"><a class="brand" href="{base}/">Reno<span>Metric</span></a><nav class="nav-links"><a href="{base}/calculators">Calculators</a><a href="{base}/methodology.html">Methodology</a><a href="{base}/about.html">About</a></nav></div></header><main><section class="hero"><div class="wrap"><span class="eyebrow">{html.escape(page['category'])}</span><h1 style="font-size:clamp(2.7rem,6vw,5rem)">{html.escape(title)}</h1><p>{html.escape(description)}</p><div class="pill-row"><span class="pill">Planning guide</span><span class="pill">No sign-up</span><span class="pill">Transparent assumptions</span></div></div></section><section class="section"><div class="wrap"><article class="article"><span class="tag">Start with real measurements</span><h2>Quick answer</h2><p><b>{html.escape(page.get("answer", description))}</b> Use the working RenoMetric calculator below for the actual estimate, then use this page to check assumptions, package rounding and project-specific considerations.</p>{_decision_promise()}{tool}{actions}<p><a class="btn primary" href="{parent_url}">Open the working {html.escape(page['parent'].title())} calculator</a></p><h2>Formula</h2><div class="formula">{html.escape(page['formula'])}</div><h2>Worked planning example</h2><p>{html.escape(page['example'])}</p><h2>Common uses</h2><ul>{uses}</ul><h2>How to get a better estimate</h2><p>Measure the actual project rather than relying on listing dimensions. For irregular spaces, split the surface into simple measurable sections and add the results. Use the exact product label for package coverage, yield, density or square-foot coverage whenever it is available.</p><p>Keep waste and package rounding as separate steps. Waste covers cuts, breakage, pattern matching and unavoidable offcuts. Package rounding reflects the fact that many materials are sold only in complete bags, boxes, bundles or cans.</p><p class="note"><b>Before you buy:</b> this page is a planning guide, not a contractor quotation or structural design. Verify final quantities with the product manufacturer, supplier or installer when project conditions could materially change the result.</p><h2>{html.escape(title)} FAQ</h2>{faqs}<h2>Use the calculator</h2><p><a class="pill" href="{parent_url}">Open {html.escape(page['parent'].title())} Calculator</a> <a class="pill" href="{base}/calculators">Browse all RenoMetric calculators</a></p></article></div></section></main>{_footer(base)}<script src=\"{base}/assets/workspace.js\" defer></script></body></html>'''


def _decision_table(page: dict) -> str:
    rows_by_slug = {
        "concrete-slab-bag-vs-ready-mix-guide": [
            ("Project volume", "Small, accessible pours may suit bags; larger or continuous pours usually suit ready-mix.", "Confirm exact volume, supplier minimums and truck access."),
            ("Labor and placement", "Bagged concrete needs repeated mixing and enough people to place and finish it.", "Protect the finishing window and plan water, mixing and cleanup."),
            ("True cost", "Compare delivered concrete, labor, equipment, delivery and waste—not just bag price.", "Use local supplier pricing and the actual site constraints."),
        ],
        "rebar-grid-quantity-planning-guide": [
            ("Grid layout", "Count bars in both directions across the usable span.", "Confirm bar size, spacing, cover and laps from the design."),
            ("Purchase quantity", "Add cutting and lap allowance, then round to stock lengths.", "Check the stock lengths actually sold by the supplier."),
            ("Structural decision", "A quantity estimate does not choose reinforcement design.", "Use structural drawings or qualified design guidance."),
        ],
        "concrete-patio-cost-breakdown-guide": [
            ("Scope", "Separate concrete, base, forms, reinforcement, finishing and labor.", "Make demolition, disposal and permits visible line items."),
            ("Access", "Truck access, pumping and hand placement can change the installed cost.", "Ask contractors to price the same access assumptions."),
            ("Site preparation", "Excavation, drainage and weak subgrade can outweigh the concrete material cost.", "Confirm existing conditions before comparing quotes."),
        ],
        "flooring-box-coverage-and-waste-guide": [
            ("Net area", "Measure every area receiving the same product and remove only fixed exclusions.", "Keep closets, transitions and stairs in the installation scope."),
            ("Layout waste", "Simple rectangles need less allowance than patterns, angles or many cuts.", "Use the installer’s cut plan and the product return policy."),
            ("Carton coverage", "Divide planned square footage by the exact carton coverage and round up.", "Read the current carton label rather than a listing headline."),
        ],
        "room-paint-two-coats-guide": [
            ("Paintable area", "Use wall and ceiling surface area, subtracting meaningful openings.", "Do not use floor area as a substitute for wall area."),
            ("Coats and coverage", "Multiply by the planned coats, then divide by the exact product coverage.", "Separate primer and ceiling products when they differ."),
            ("Surface condition", "Texture, color changes and application method affect actual coverage.", "Allow for touch-up and the product manufacturer’s guidance."),
        ],
        "mulch-bag-coverage-by-depth-guide": [
            ("Bed area", "Split irregular beds into simple measurable sections.", "Measure the actual planted area rather than guessing from the property size."),
            ("Installed depth", "Convert inches to feet before calculating cubic feet.", "Use a depth appropriate for plants, drainage and existing mulch."),
            ("Bag size", "Divide volume by the labeled bag volume and round up.", "Check settling and the current bag label."),
        ],
        "roof-area-pitch-measurement-guide": [
            ("Roof geometry", "Calculate each roof plane and apply its correct pitch factor.", "Separate additions, porches, dormers, hips and valleys."),
            ("Ordering", "Convert surface area to squares or bundles using the product label.", "Add starter, ridge, flashing and other accessories separately."),
            ("Safety", "A ground or plan-based estimate is safer than an unsafe roof measurement.", "Use proper equipment or a qualified professional for difficult roofs."),
        ],
        "deck-board-linear-feet-guide": [
            ("Board module", "Use actual face width plus the installation gap to count rows.", "Follow the selected manufacturer’s spacing instructions."),
            ("Project zones", "Calculate the main field, stairs, borders and picture framing separately.", "Do not assume all offcuts can be reused."),
            ("Stock lengths", "Round the plan to boards that are actually available.", "Review cuts, joins and waste before purchasing."),
        ],
        "fence-gate-post-estimate-guide": [
            ("Gate layout", "A typical gate opening needs two dedicated gate posts.", "Check the actual gate system, hinge and latch layout."),
            ("Post loading", "Heavy, wide or wind-exposed gates may need stronger posts and footings.", "Do not substitute ordinary line posts without verification."),
            ("Footings", "Fence length alone does not determine footing design.", "Confirm soil, embedment, concrete and local requirements."),
        ],
        "concrete-driveway-gravel-base-guide": [
            ("Compacted depth", "Calculate area times the specified compacted base depth.", "Do not use concrete thickness as a substitute for base depth."),
            ("Delivered volume", "Loose delivered aggregate can exceed the compacted volume.", "Ask the supplier how compaction and allowance are represented."),
            ("Site condition", "Soil, drainage, climate and vehicle loads affect the base requirement.", "Confirm the specification before ordering material."),
        ],
    }
    rows = rows_by_slug.get(page.get("slug"), [
        ("Measurements", "Start with accurate project dimensions and the correct units.", "Replace generic assumptions with site measurements."),
        ("Product data", "Use the actual package yield, coverage or density.", "Check the current manufacturer or supplier label."),
        ("Final decision", "Treat the result as an early planning estimate.", "Confirm final quantities and requirements before purchase."),
    ])
    body = "".join(
        f"<tr><th scope=\"row\">{html.escape(label)}</th><td>{html.escape(guidance)}</td><td>{html.escape(verify)}</td></tr>"
        for label, guidance, verify in rows
    )
    return f"""<h2>Decision guide</h2><div style="overflow-x:auto"><table><thead><tr><th>Decision point</th><th>What the estimate tells you</th><th>What to verify</th></tr></thead><tbody>{body}</tbody></table></div>"""


def _authority_section(page: dict, base: str) -> str:
    source_map = {
        "how-to-read-concrete-bag-yield-label": [
            ("American Concrete Institute (ACI)", "https://www.concrete.org/", "Concrete materials and placement guidance."),
        ],
        "concrete-ordering-delivery-minimum-guide": [
            ("National Ready Mixed Concrete Association (NRMCA)", "https://www.nrmca.org/", "Ready-mix concrete and industry information."),
        ],
        "flooring-carton-coverage-ordering-guide": [
            ("National Wood Flooring Association (NWFA)", "https://woodfloors.org/", "Wood-flooring installation and care information."),
            ("Tile Council of North America (TCNA)", "https://www.tcnatile.com/", "Tile installation and standards information."),
        ],
        "paint-primer-vs-finish-quantity-guide": [
            ("U.S. Environmental Protection Agency — Safer Choice", "https://www.epa.gov/saferchoice", "Product and ingredient information for safer coating choices."),
        ],
        "driveway-gravel-delivery-tonnage-guide": [
            ("Federal Highway Administration (FHWA)", "https://highways.dot.gov/", "Transportation and pavement resources."),
            ("USDA Natural Resources Conservation Service (NRCS)", "https://www.nrcs.usda.gov/", "Soil, drainage and conservation information."),
        ],
        "roofing-accessory-order-checklist": [
            ("National Roofing Contractors Association (NRCA)", "https://www.nrca.net/", "Roofing practice and contractor guidance."),
        ],
        "rebar-stock-length-cutting-allowance-guide": [
            ("American Concrete Institute (ACI)", "https://www.concrete.org/", "Concrete and reinforcement design guidance."),
        ],
        "renovation-material-takeoff-checklist": [
            ("International Code Council (ICC)", "https://www.iccsafe.org/", "Building-safety and model-code information."),
        ],
        "concrete-slab-bag-vs-ready-mix-guide": [
            ("American Concrete Institute (ACI)", "https://www.concrete.org/", "Concrete and reinforcement design guidance."),
            ("National Ready Mixed Concrete Association (NRMCA)", "https://www.nrmca.org/", "Ready-mix concrete and industry information."),
        ],
        "rebar-grid-quantity-planning-guide": [
            ("American Concrete Institute (ACI)", "https://www.concrete.org/", "Concrete and reinforcement design guidance."),
        ],
        "concrete-patio-cost-breakdown-guide": [
            ("American Concrete Institute (ACI)", "https://www.concrete.org/", "Concrete and reinforcement design guidance."),
            ("National Ready Mixed Concrete Association (NRMCA)", "https://www.nrmca.org/", "Ready-mix concrete and industry information."),
        ],
        "flooring-box-coverage-and-waste-guide": [
            ("National Wood Flooring Association (NWFA)", "https://woodfloors.org/", "Wood-flooring installation and care information."),
            ("Tile Council of North America (TCNA)", "https://www.tcnatile.com/", "Tile installation and standards information."),
        ],
        "room-paint-two-coats-guide": [
            ("U.S. Environmental Protection Agency — Safer Choice", "https://www.epa.gov/saferchoice", "Product and ingredient information for safer cleaning and coating choices."),
        ],
        "mulch-bag-coverage-by-depth-guide": [
            ("USDA Natural Resources Conservation Service (NRCS)", "https://www.nrcs.usda.gov/", "Soil, drainage and conservation information."),
        ],
        "roof-area-pitch-measurement-guide": [
            ("National Roofing Contractors Association (NRCA)", "https://www.nrca.net/", "Roofing practice and contractor guidance."),
        ],
        "deck-board-linear-feet-guide": [
            ("American Wood Council (AWC)", "https://awc.org/", "Wood construction and span guidance."),
        ],
        "fence-gate-post-estimate-guide": [
            ("International Code Council (ICC)", "https://www.iccsafe.org/", "Model-code and building-safety information."),
        ],
        "concrete-driveway-gravel-base-guide": [
            ("Federal Highway Administration (FHWA)", "https://highways.dot.gov/", "Transportation, pavement and ground-condition resources."),
        ],
    }
    sources = source_map.get(page.get("slug"), [])
    links = "".join(
        f'<li><a href="{url}" rel="noopener noreferrer">{html.escape(name)}</a> — {html.escape(note)}</li>'
        for name, url, note in sources
    )
    return f'<h2>Authority and verification</h2><p>RenoMetric provides transparent planning arithmetic, not a structural design or contractor quote. Verify final decisions with the current product label or supplier data, the applicable local requirements, and a qualified professional when the project is safety-critical.</p><ul><li><a href="{base}/methodology.html">RenoMetric methodology</a> — formulas, units and planning limitations.</li>{links}</ul>'


def _decision_faqs(page: dict) -> list[tuple[str, str]]:
    extra = {
        "concrete-slab-bag-vs-ready-mix-guide": [
            ("Does this estimate replace a contractor quote?", "No. It compares planning quantities and decision factors; confirm delivery, labor, access and final scope with the supplier or contractor."),
            ("What product data should I verify before buying?", "Verify the exact bag yield, ready-mix minimum order, mix specification, delivery window and local project requirements."),
        ],
        "rebar-grid-quantity-planning-guide": [
            ("Does this choose rebar size or spacing?", "No. Use the structural drawings or qualified design for bar size, spacing, cover, laps and placement."),
            ("Does the result include purchase waste?", "It can include a visible lap or cutting allowance, but stock lengths and the actual cutting plan still need review."),
        ],
        "concrete-patio-cost-breakdown-guide": [
            ("Does this include every patio cost?", "No. Separate demolition, excavation, base, forms, reinforcement, finishing, delivery, access, labor and permits."),
            ("Why can two same-size patios cost differently?", "Site preparation, access, pumping, disposal and finishing requirements can differ substantially."),
        ],
        "flooring-box-coverage-and-waste-guide": [
            ("Is the result net flooring or boxes to buy?", "The purchase estimate adds the chosen waste allowance and rounds up to complete cartons."),
            ("Should I use the listing coverage or carton label?", "Use the current product carton or manufacturer specification for the exact coverage."),
        ],
        "room-paint-two-coats-guide": [
            ("Does this include primer?", "Treat primer as a separate product and coat when the surface or product system requires it."),
            ("Will texture change the gallons needed?", "Yes. Texture, porosity, color change and application method can reduce practical coverage."),
        ],
        "mulch-bag-coverage-by-depth-guide": [
            ("Is the answer based on bag weight?", "No. Use the labeled volume per bag; weight does not reliably indicate coverage."),
            ("Does this choose the correct mulch depth?", "No. Choose depth based on plants, drainage and landscape conditions."),
        ],
        "roof-area-pitch-measurement-guide": [
            ("Does this calculate every roofing material?", "It estimates surface area; starter, ridge, flashing, valleys and penetrations should be listed separately."),
            ("Can I measure a roof safely myself?", "Use plans or ground measurements when possible and do not access a roof without proper safety equipment."),
        ],
        "deck-board-linear-feet-guide": [
            ("Does this include stairs and borders?", "The main field should be calculated separately from stairs, borders and picture framing."),
            ("Does this size the deck framing?", "No. Joists, spans, ledger details and footings require separate structural planning."),
        ],
        "fence-gate-post-estimate-guide": [
            ("Does a heavy gate need stronger posts?", "Often yes; gate width, weight, hardware, wind and soil affect post and footing requirements."),
            ("Does this determine footing depth?", "No. Confirm embedment, concrete and local requirements for the fence system and site."),
        ],
        "concrete-driveway-gravel-base-guide": [
            ("Is the result compacted or delivered volume?", "The calculation starts with compacted volume; confirm the supplier's allowance for loose delivered material."),
            ("Does this design the driveway base?", "No. Soil, drainage, climate and vehicle loads determine the required base design."),
        ],
    }
    return extra.get(page.get("slug"), [])


def render_guide(page: dict, base: str, origin: str) -> str:
    title = page["title"]
    description = page["description"]
    canonical = f"{origin}/guides/{page['slug']}"
    parent_url = f"{base}/calculators/{page['parent']}"
    steps_html = "".join(
        f'<li><b>{html.escape(step[0])}</b> {html.escape(step[1])}</li>' for step in page["steps"]
    )
    all_faqs = page["faqs"] + _decision_faqs(page)
    faq_html = "".join(
        f'<div class="faq"><h3>{html.escape(q)}</h3><p>{html.escape(a)}</p></div>'
        for q, a in all_faqs
    )
    decision_html = _decision_table(page)
    authority_html = _authority_section(page, base)
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
                "dateModified": "2026-08-27",
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "RenoMetric", "item": f"{origin}/"},
                    {"@type": "ListItem", "position": 2, "name": "Guides", "item": f"{origin}/guides"},
                    {"@type": "ListItem", "position": 3, "name": title, "item": canonical},
                ],
            },
            _faq_schema(all_faqs),
        ],
    }
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} | RenoMetric</title><meta name="description" content="{html.escape(description)}"><link rel="canonical" href="{canonical}"><meta name="robots" content="index,follow"><meta property="og:title" content="{html.escape(title)} | RenoMetric"><meta property="og:description" content="{html.escape(description)}"><meta property="og:type" content="article"><meta property="og:url" content="{canonical}"><link rel="stylesheet" href="{base}/assets/styles.css"><script type="application/ld+json">{json.dumps(schema, separators=(',', ':'))}</script></head><body><header class="nav"><div class="wrap nav-in"><a class="brand" href="{base}/">Reno<span>Metric</span></a><nav class="nav-links"><a href="{base}/calculators">Calculators</a><a href="{base}/guides/">Guides</a><a href="{base}/methodology.html">Methodology</a></nav></div></header><main><section class="hero"><div class="wrap"><span class="eyebrow">{html.escape(page['category'])} guide</span><h1 style="font-size:clamp(2.7rem,6vw,5rem)">{html.escape(title)}</h1><p>{html.escape(description)}</p></div></section><section class="section"><div class="wrap"><article class="article"><h2>Quick answer</h2><p>{html.escape(page['answer'])}</p><p><a class="btn primary" href="{parent_url}">Use the related calculator</a></p><h2>Step by step</h2><ol>{steps_html}</ol><h2>Formula or rule of thumb</h2><div class="formula">{html.escape(page['formula'])}</div><h2>Example</h2><p>{html.escape(page['example'])}</p><h2>Common mistakes</h2><p>{html.escape(page['mistakes'])}</p><p class="note"><b>Planning note:</b> product yields, installation methods, site conditions and local requirements can change the final quantity. Use the exact manufacturer or supplier information before purchasing.</p>{decision_html}{authority_html}<h2>FAQ</h2>{faq_html}<h2>Related tool</h2><p><a class="pill" href="{parent_url}">Open the related calculator</a> <a class="pill" href="{base}/guides/">Browse all guides</a></p></article></div></section></main>{_footer(base)}</body></html>'''
