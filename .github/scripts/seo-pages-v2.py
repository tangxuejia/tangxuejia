from __future__ import annotations

import html
import json
from pathlib import Path


def seo_pages() -> list[dict]:
    return [
        {
            "slug": "flooring-cost-calculator",
            "title": "Flooring Cost Calculator",
            "category": "Flooring & Tile",
            "parent": "flooring",
            "description": "Estimate flooring material cost from room size, waste allowance, box coverage and price per box or square foot.",
            "formula": "estimated material cost = purchase quantity × unit price",
            "example": "A 12 × 15 ft room is 180 ft². With 10% waste, plan for about 198 ft² before rounding to full boxes.",
            "uses": ["Laminate and vinyl budgets", "Hardwood planning", "Comparing box prices", "Early renovation budgets"],
            "faqs": [
                ("Does this include labor?", "No. RenoMetric focuses on material planning. Labor, removal, subfloor repair, trim, delivery and tax should be budgeted separately."),
                ("Should I use price per box or per square foot?", "Use the unit your supplier actually quotes. If flooring is sold by the box, round the material quantity to complete boxes before multiplying by price."),
                ("How much waste should I add?", "Ten percent is a common planning starting point for straightforward rooms, but diagonal layouts, patterned installs and complex cuts can require more."),
            ],
        },
        {
            "slug": "laminate-flooring-calculator",
            "title": "Laminate Flooring Calculator",
            "category": "Flooring & Tile",
            "parent": "flooring",
            "description": "Estimate laminate flooring square footage and full boxes, including a visible waste allowance for cuts and offcuts.",
            "formula": "purchase area = room area × (1 + waste rate)",
            "example": "For a 10 × 14 ft room, raw area is 140 ft². At 10% waste, plan around 154 ft² before box rounding.",
            "uses": ["Bedrooms", "Living rooms", "Rental updates", "Whole-room laminate replacement"],
            "faqs": [
                ("How many boxes of laminate do I need?", "Divide the purchase area by the exact coverage printed on one box and round up to the next whole box."),
                ("Do I include closets?", "Yes, if they will receive the same flooring. Measure closets separately when their shape makes the main room dimensions misleading."),
                ("Is 10% waste always enough?", "Not always. Pattern matching, angled walls, diagonal installations and damaged boards can increase the allowance."),
            ],
        },
        {
            "slug": "vinyl-flooring-calculator",
            "title": "Vinyl Flooring Calculator",
            "category": "Flooring & Tile",
            "parent": "flooring",
            "description": "Plan vinyl plank or tile flooring quantity from measured area, waste allowance and package coverage.",
            "formula": "boxes = ceil((floor area × waste factor) ÷ box coverage)",
            "example": "A 16 × 12 ft room is 192 ft². With 8% waste the planning area is about 207.4 ft², then round up to full boxes.",
            "uses": ["Luxury vinyl plank", "Vinyl tile", "Kitchens", "Basements and utility rooms"],
            "faqs": [
                ("Can I use this for LVP?", "Yes. Enter the room measurements and the square-foot coverage shown on the LVP carton."),
                ("Should I subtract cabinets?", "For fixed cabinets that will never have flooring beneath them, you may subtract their footprint. Keep the measurement conservative if the layout is uncertain."),
                ("Why round up to full boxes?", "Retail flooring is normally purchased in complete packages, so the order quantity must cover the project after package rounding."),
            ],
        },
        {
            "slug": "hardwood-flooring-calculator",
            "title": "Hardwood Flooring Calculator",
            "category": "Flooring & Tile",
            "parent": "flooring",
            "description": "Estimate hardwood flooring quantity and boxes with room area, cutting allowance and package coverage kept visible.",
            "formula": "required area = measured area + cutting and waste allowance",
            "example": "A 200 ft² room with a 12% planning allowance needs about 224 ft² before full-carton rounding.",
            "uses": ["Solid hardwood", "Engineered hardwood", "Room additions", "Replacement flooring"],
            "faqs": [
                ("Why can hardwood need more waste?", "Board length variation, defects, color selection and staggered joints can create more offcuts than a simple rectangular sheet product."),
                ("Can I combine several rooms?", "Yes. Calculate each room separately, add the purchase areas, then round using the actual box coverage."),
                ("Should I buy an extra box?", "Some owners keep spare matching boards for future repairs, but that is a project choice rather than a calculator requirement."),
            ],
        },
        {
            "slug": "carpet-calculator",
            "title": "Carpet Calculator",
            "category": "Flooring & Tile",
            "parent": "flooring",
            "description": "Estimate carpet area for rooms and understand why roll width, seam layout and installation direction can raise the actual order quantity.",
            "formula": "room area = length × width",
            "example": "A 13 × 11 ft bedroom measures 143 ft², but roll width and seam placement may require ordering more than the geometric area.",
            "uses": ["Bedrooms", "Living rooms", "Hallways", "Rental turnovers"],
            "faqs": [
                ("Is square footage enough to order carpet?", "Not always. Carpet is commonly supplied in fixed roll widths, so a professional layout can require extra material for seams and direction."),
                ("Does the calculator include stairs?", "Treat stairs separately. Treads, risers and nosings need their own measurements and installation allowance."),
                ("Can I convert square feet to square yards?", "Yes. Divide square feet by 9 for a basic area conversion, then confirm the installer’s ordering method."),
            ],
        },
        {
            "slug": "room-flooring-calculator",
            "title": "Room Flooring Calculator",
            "category": "Flooring & Tile",
            "parent": "flooring",
            "description": "Calculate room square footage and the purchase quantity needed after waste and box rounding.",
            "formula": "room area = length × width",
            "example": "A 9.5 × 12 ft room is 114 ft². Add your chosen waste rate and round to the actual package size.",
            "uses": ["Bedrooms", "Home offices", "Dining rooms", "Single-room remodels"],
            "faqs": [
                ("What if the room is L-shaped?", "Split it into rectangles, calculate each section, then add the areas before applying waste."),
                ("Do I measure baseboards?", "No. Flooring area uses the floor footprint. Baseboard and trim are separate linear-foot calculations."),
                ("Should door recesses be included?", "Include areas that will actually receive flooring, including recesses and closets when applicable."),
            ],
        },
        {
            "slug": "flooring-box-calculator",
            "title": "Flooring Box Calculator",
            "category": "Flooring & Tile",
            "parent": "flooring",
            "description": "Convert required flooring area into complete boxes using the exact carton coverage from the product label.",
            "formula": "boxes = ceil(required square feet ÷ square feet per box)",
            "example": "If the project requires 214 ft² and each box covers 23.6 ft², 9.07 boxes rounds up to 10 complete boxes.",
            "uses": ["Laminate cartons", "LVP cartons", "Engineered wood boxes", "Tile package planning"],
            "faqs": [
                ("Why can’t I buy 9.1 boxes?", "Most flooring is sold only in complete cartons, so the calculated box count must be rounded up."),
                ("Do I add waste before box rounding?", "Yes. Apply the waste allowance to the measured area first, then divide by package coverage."),
                ("Can box coverage vary by product?", "Yes. Always use the coverage printed on the exact SKU you plan to buy."),
            ],
        },
        {
            "slug": "bathroom-tile-calculator",
            "title": "Bathroom Tile Calculator",
            "category": "Flooring & Tile",
            "parent": "tile",
            "description": "Estimate bathroom floor or wall tile quantity with measured surface area, tile size, waste allowance and box coverage.",
            "formula": "tile quantity = surface area ÷ tile face area, then add waste",
            "example": "A 5 × 8 ft bathroom floor is 40 ft². With 12% waste, plan for about 44.8 ft² before box rounding.",
            "uses": ["Bathroom floors", "Shower walls", "Tub surrounds", "Accent walls"],
            "faqs": [
                ("Should I subtract the vanity?", "Subtract only areas that definitely will not receive tile. For uncertain layouts, keeping a small reserve is safer."),
                ("How much tile waste is typical?", "Simple straight layouts may use around 10%, while diagonal patterns, niches and many cuts can require more."),
                ("Can I calculate shower walls too?", "Yes. Measure each tiled wall separately and subtract large untiled openings only when appropriate."),
            ],
        },
        {
            "slug": "kitchen-tile-calculator",
            "title": "Kitchen Tile Calculator",
            "category": "Flooring & Tile",
            "parent": "tile",
            "description": "Estimate tile for kitchen floors and backsplashes using measured area, tile dimensions, cutting allowance and package size.",
            "formula": "purchase area = tiled surface area × waste factor",
            "example": "A backsplash 15 ft long and 18 in high covers 22.5 ft² before outlets, cuts and waste allowance.",
            "uses": ["Kitchen floors", "Backsplashes", "Pantry floors", "Feature walls"],
            "faqs": [
                ("How do I measure a backsplash?", "Multiply the total backsplash length by its height, then subtract large non-tiled areas if useful."),
                ("Do outlets reduce the tile order much?", "Usually not enough to rely on for savings. Small openings also create extra cutting and breakage."),
                ("Should I add more for patterned tile?", "Often yes. Pattern matching and centered layouts can increase offcuts compared with a simple running layout."),
            ],
        },
        {
            "slug": "wall-paint-calculator",
            "title": "Wall Paint Calculator",
            "category": "Paint & Finishes",
            "parent": "paint",
            "description": "Estimate gallons of wall paint from wall area, openings, number of coats and the coverage rate printed on the can.",
            "formula": "paint gallons = (paintable wall area × coats) ÷ coverage per gallon",
            "example": "Four walls totaling 420 ft², two coats and 350 ft²/gal coverage need about 2.4 gallons before purchase rounding.",
            "uses": ["Bedrooms", "Living rooms", "Hallways", "Interior repainting"],
            "faqs": [
                ("Do I subtract windows and doors?", "You can subtract meaningful openings for a tighter estimate, though small openings often offset some cutting and touch-up waste."),
                ("How many coats should I plan?", "Two coats are common for color consistency, but primer, color changes and product instructions can alter the plan."),
                ("What coverage number should I use?", "Use the coverage range stated on the exact paint product because texture and application method affect real coverage."),
            ],
        },
        {
            "slug": "room-paint-calculator",
            "title": "Room Paint Calculator",
            "category": "Paint & Finishes",
            "parent": "paint",
            "description": "Estimate room paint for four walls using room dimensions, ceiling height, openings, coats and product coverage.",
            "formula": "wall area = 2 × (length + width) × wall height",
            "example": "A 12 × 10 ft room with 8 ft walls has 352 ft² of gross wall area before subtracting doors and windows.",
            "uses": ["Bedrooms", "Home offices", "Nurseries", "Apartment turnovers"],
            "faqs": [
                ("Does this include the ceiling?", "Not unless you intentionally add ceiling area. Ceiling paint is best estimated separately because product and finish may differ."),
                ("Should closets be included?", "Include them if they will be painted with the same product. Measure them separately for clearer planning."),
                ("Why does the result round up?", "Paint is sold in fixed container sizes, and a small reserve is useful for cutting in and touch-ups."),
            ],
        },
        {
            "slug": "ceiling-paint-calculator",
            "title": "Ceiling Paint Calculator",
            "category": "Paint & Finishes",
            "parent": "paint",
            "description": "Estimate ceiling paint from ceiling area, coat count and the coverage rate for the exact ceiling paint you plan to use.",
            "formula": "ceiling paint = (length × width × coats) ÷ coverage",
            "example": "A 14 × 16 ft ceiling is 224 ft². Two coats equal 448 coverage ft² before rounding to container size.",
            "uses": ["Flat ceilings", "Bedroom ceilings", "Kitchen ceilings", "Whole-house repainting"],
            "faqs": [
                ("Is one coat enough on a ceiling?", "Sometimes, but stains, repairs and color changes may require primer or a second finish coat."),
                ("Can I use wall paint coverage numbers?", "Use the label for the actual ceiling product. Different formulations and surfaces can change coverage."),
                ("What about vaulted ceilings?", "Measure the sloped surface rather than using floor area when the slope materially increases actual ceiling area."),
            ],
        },
        {
            "slug": "exterior-paint-calculator",
            "title": "Exterior Paint Calculator",
            "category": "Paint & Finishes",
            "parent": "paint",
            "description": "Plan exterior wall paint using measured facade area, openings, coats and real product coverage.",
            "formula": "paintable exterior area = gross wall area − large openings",
            "example": "A 40 ft wide wall that averages 18 ft high has about 720 ft² gross area before subtracting major windows and doors.",
            "uses": ["Siding", "Stucco", "Exterior masonry", "Garage exteriors"],
            "faqs": [
                ("Does rough siding use more paint?", "It can. Rough, porous or heavily textured surfaces often reduce practical coverage compared with the label maximum."),
                ("Should I include primer?", "Primer should be estimated separately when the substrate, repair work or paint system requires it."),
                ("How do I handle gable ends?", "Measure rectangular sections and triangular gables separately, then add their areas."),
            ],
        },
        {
            "slug": "paint-cost-calculator",
            "title": "Paint Cost Calculator",
            "category": "Paint & Finishes",
            "parent": "paint",
            "description": "Estimate paint material cost from gallons required, container size, coats and the current price of the product you plan to buy.",
            "formula": "material cost = containers required × price per container",
            "example": "If a project needs 3 gallons and one-gallon cans cost $42, the paint-only budget starts around $126 before tax and supplies.",
            "uses": ["Comparing paint lines", "Room budgets", "Exterior budgets", "DIY material planning"],
            "faqs": [
                ("Does this include brushes and supplies?", "No. Tape, rollers, trays, primer, patching materials, ladders and labor are separate costs."),
                ("Should I compare price per gallon?", "Yes, but also compare coverage, coat requirements and container sizes because the cheapest gallon may not produce the lowest project cost."),
                ("Are sales and tax included?", "Only if you enter prices that already reflect them. Use current local prices for the most useful estimate."),
            ],
        },
        {
            "slug": "paint-gallon-calculator",
            "title": "Paint Gallon Calculator",
            "category": "Paint & Finishes",
            "parent": "paint",
            "description": "Convert paintable square footage and coat count into gallons using a product-specific coverage rate.",
            "formula": "gallons = total coat area ÷ square feet covered per gallon",
            "example": "700 coat-ft² at 350 ft² per gallon equals 2 gallons before allowing for surface texture and touch-ups.",
            "uses": ["Interior walls", "Ceilings", "Exterior walls", "Primer planning"],
            "faqs": [
                ("How many square feet does a gallon cover?", "Many products publish a range around 350–400 ft² per gallon, but use the exact label because substrate and application change real coverage."),
                ("Do two coats double the paint?", "For planning, multiply the paintable area by the number of coats. Actual second-coat usage may vary, but this is a transparent starting point."),
                ("Can I mix gallon and quart sizes?", "Yes. After estimating total volume, compare available container sizes to reduce unnecessary leftover paint."),
            ],
        },
        {
            "slug": "paint-coverage-calculator",
            "title": "Paint Coverage Calculator",
            "category": "Paint & Finishes",
            "parent": "paint",
            "description": "Estimate how much surface a known quantity of paint can cover based on the manufacturer’s square-foot-per-gallon rating.",
            "formula": "total coverage = gallons × coverage per gallon ÷ coats",
            "example": "Two gallons rated at 375 ft² each provide about 750 single-coat ft², or about 375 ft² for two equal coats.",
            "uses": ["Checking leftover paint", "Comparing products", "Planning second coats", "Estimating small projects"],
            "faqs": [
                ("Why does actual coverage vary?", "Porosity, texture, color change, roller nap, spray loss and application thickness can all change practical coverage."),
                ("Can I rely on the maximum label coverage?", "For purchasing, a conservative value within the manufacturer’s published range is often safer than assuming the maximum."),
                ("Does primer have the same coverage?", "Not necessarily. Estimate primer using its own product label."),
            ],
        },
        {
            "slug": "fence-paint-calculator",
            "title": "Fence Paint Calculator",
            "category": "Paint & Finishes",
            "parent": "paint",
            "description": "Estimate paint or stain area for a fence by length, height, number of coated sides, coats and product coverage.",
            "formula": "coated area = fence length × height × coated sides",
            "example": "A 100 ft fence that is 6 ft high has 600 ft² on one side or 1,200 ft² for both sides before coats.",
            "uses": ["Wood fences", "Privacy fences", "Fence stain", "Exterior maintenance"],
            "faqs": [
                ("Should both sides be counted?", "Yes if both sides will be coated. Multiply the face area by two before applying coat count."),
                ("Do gaps reduce the area?", "They can, but posts, rails and edges add surface area back. For planning, use a conservative adjustment rather than assuming every gap is a full saving."),
                ("Can I use this for stain?", "Yes for area planning, but use the stain manufacturer’s coverage rate because penetrating stains can differ greatly from paint."),
            ],
        },
        {
            "slug": "house-paint-calculator",
            "title": "House Paint Calculator",
            "category": "Paint & Finishes",
            "parent": "paint",
            "description": "Estimate whole-house paint quantity by combining wall areas and applying separate coat and coverage assumptions for each surface type.",
            "formula": "total paint = sum of each paintable surface × coats ÷ product coverage",
            "example": "For a whole-house plan, calculate rooms or exterior elevations separately, then total gallons by paint product and finish.",
            "uses": ["Whole-home interiors", "Rental repainting", "Exterior repainting", "Pre-purchase budgeting"],
            "faqs": [
                ("Should every room use one coverage rate?", "Only when the same product and similar surface conditions apply. Separate calculations are better when finishes or products differ."),
                ("How do I include trim?", "Trim is often easier to estimate separately using linear measurements or a dedicated trim-paint allowance."),
                ("Does the calculator replace a contractor quote?", "No. It is a material-planning tool. Access, repairs, prep work, labor and site conditions can dominate a professional quote."),
            ],
        },
    ]


def render_page(page: dict, base: str, origin: str) -> str:
    title = page["title"]
    description = page["description"]
    canonical = f"{origin}/calculators/{page['slug']}"
    parent_url = f"{base}/calculators/{page['parent']}"
    faq_entities = [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in page["faqs"]
    ]
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebApplication",
                "name": title,
                "applicationCategory": "UtilitiesApplication",
                "operatingSystem": "Any",
                "isAccessibleForFree": True,
                "description": description,
                "url": canonical,
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "RenoMetric", "item": f"{origin}/"},
                    {"@type": "ListItem", "position": 2, "name": "Calculators", "item": f"{origin}/#calculators"},
                    {"@type": "ListItem", "position": 3, "name": title, "item": canonical},
                ],
            },
            {"@type": "FAQPage", "mainEntity": faq_entities},
        ],
    }
    uses = "".join(f"<li>{html.escape(x)}</li>" for x in page["uses"])
    faqs = "".join(
        f"<div class=\"faq\"><h3>{html.escape(q)}</h3><p>{html.escape(a)}</p></div>" for q, a in page["faqs"]
    )
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} — Free Estimator | RenoMetric</title><meta name="description" content="{html.escape(description)}"><link rel="canonical" href="{canonical}"><meta name="robots" content="index,follow"><meta property="og:title" content="{html.escape(title)} | RenoMetric"><meta property="og:description" content="{html.escape(description)}"><meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><link rel="stylesheet" href="{base}/assets/styles.css"><script type="application/ld+json">{json.dumps(schema, separators=(',', ':'))}</script></head><body><header class="nav"><div class="wrap nav-in"><a class="brand" href="{base}/">Reno<span>Metric</span></a><nav class="nav-links"><a href="{base}/#calculators">Calculators</a><a href="{base}/methodology.html">Methodology</a><a href="{base}/about.html">About</a></nav></div></header><main><section class="hero"><div class="wrap"><span class="eyebrow">{html.escape(page['category'])}</span><h1 style="font-size:clamp(2.7rem,6vw,5rem)">{html.escape(title)}</h1><p>{html.escape(description)}</p><div class="pill-row"><span class="pill">Free planning tool</span><span class="pill">No sign-up</span><span class="pill">Transparent assumptions</span></div></div></section><section class="section"><div class="wrap"><article class="article"><span class="tag">Start with real measurements</span><h2>Quick answer</h2><p>{html.escape(description)} RenoMetric keeps the geometry, waste allowance and package rounding visible so you can change the estimate to match the exact product you plan to buy.</p><p><a class="btn primary" href="{parent_url}">Open the working {html.escape(page['parent'].title())} calculator</a></p><h2>Formula</h2><div class="formula">{html.escape(page['formula'])}</div><h2>Worked planning example</h2><p>{html.escape(page['example'])}</p><h2>Common uses</h2><ul>{uses}</ul><h2>How to get a better estimate</h2><p>Measure the actual project rather than relying on listing dimensions. For irregular spaces, split the surface into simple rectangles or other measurable sections and add the results. Then use the product label for package coverage, yield or square-foot coverage instead of a generic assumption.</p><p>Apply waste before package rounding. Waste accounts for cuts, breakage, pattern matching and unavoidable offcuts; package rounding accounts for the fact that flooring, tile and paint are sold in fixed container sizes. Those are different steps and should stay visible.</p><p class="note"><b>Before you buy:</b> this page is for planning, not a contractor quotation. Verify the final quantity with the product manufacturer, supplier or installer when project conditions could materially change coverage or waste.</p><h2>{html.escape(title)} FAQ</h2>{faqs}<h2>Related calculator</h2><p><a class="pill" href="{parent_url}">Use the full {html.escape(page['parent'].title())} Calculator</a> <a class="pill" href="{base}/#calculators">Browse all RenoMetric calculators</a></p></article></div></section></main><footer class="footer"><div class="wrap"><div class="footer-grid"><div><a class="brand" href="{base}/">Reno<span>Metric</span></a><p>Fast, transparent planning calculators for home improvement and DIY projects.</p></div><div><b>Explore</b><p><a href="{base}/#calculators">Calculators</a><br><a href="{base}/methodology.html">Methodology</a><br><a href="{base}/about.html">About</a></p></div><div><b>Legal</b><p><a href="{base}/privacy.html">Privacy</a><br><a href="{base}/terms.html">Terms</a><br><a href="{base}/contact.html">Contact</a></p></div></div><p class="legal">© 2026 RenoMetric. Estimates are for planning only. Confirm product specifications, site conditions and final quantities with the relevant supplier or qualified professional.</p></div></footer></body></html>'''
