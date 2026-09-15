from __future__ import annotations

def seo_guides() -> list[dict]:
    return [
        {
            "slug": "how-to-budget-a-kitchen-remodel",
            "title": "How to Build a Kitchen Remodel Budget",
            "category": "Renovation & Remodeling", "topic": "flooring", "parent": "kitchen-remodel-cost-calculator",
            "description": "Plan an early kitchen remodel budget by separating cabinets, countertops, appliances, flooring, labor and site work.",
            "answer": "Define the scope first, then estimate cabinets, countertops, appliances, flooring, lighting, plumbing, labor, permits and disposal as separate line items.",
            "steps": [("Define the layout.", "A cosmetic refresh differs from moving walls or plumbing."), ("List materials.", "Separate cabinets, counters, appliances and finishes."), ("Estimate trades.", "Include electrical, plumbing, installation and demolition."), ("Add site allowances.", "Keep permits, disposal and uncertainty visible.")],
            "formula": "early budget = materials + trade labor + demolition + permits + site allowance",
            "example": "A useful kitchen budget compares cabinet, countertop, appliance and labor ranges instead of relying on one generic cost per square foot.",
            "mistakes": "Do not use an online average as a quote without adjusting for local labor, layout changes and selected finish level.",
            "faqs": [("Are appliances included?", "Include them only if they are part of the planned scope."), ("Does moving plumbing change cost?", "Usually. Relocating plumbing and electrical services can add significant trade work."), ("Should cabinets be measured first?", "Yes. Cabinet layout drives many countertop, appliance and installation quantities.")],
        },
        {
            "slug": "how-to-estimate-concrete-cost",
            "title": "How to Estimate Concrete Cost",
            "category": "Concrete & Masonry", "topic": "concrete", "parent": "concrete-cost-calculator",
            "description": "Build an early concrete cost estimate from volume, delivery, reinforcement, forming, labor and site conditions.",
            "answer": "Calculate the concrete quantity first, then separate ready-mix price, delivery, forms, reinforcement, pumping, finishing, labor and site preparation.",
            "steps": [("Measure the pour.", "Calculate slabs, footings or pads separately."), ("Price the material.", "Use current supplier pricing and minimum-order rules."), ("Add project components.", "Include forms, reinforcement, pumping and finishing."), ("Review site work.", "Account for excavation, base, access and disposal.")],
            "formula": "early cost = concrete + delivery + forms + reinforcement + labor + site work",
            "example": "Two pours with the same cubic-yard quantity can have different totals when one needs pumping, complex forms or extensive excavation.",
            "mistakes": "Do not multiply cubic yards by a single rate and call it a quote; delivery, access and finishing can materially change the total.",
            "faqs": [("Does the concrete price include delivery?", "Sometimes, but supplier terms vary. Ask whether delivery, fuel or short-load charges are separate."), ("Should reinforcement be included?", "Yes, when the project design calls for it."), ("Can this estimate structural work?", "No. Structural thickness, reinforcement and footing design require qualified project guidance.")],
        },
        {
            "slug": "how-to-estimate-flooring-cost",
            "title": "How to Estimate Flooring Cost",
            "category": "Flooring & Tile", "topic": "flooring", "parent": "flooring-cost-calculator",
            "description": "Estimate flooring cost by separating measured area, waste, product price, underlayment, transitions, removal and labor.",
            "answer": "Calculate the purchase area after waste, multiply by the selected product price, then add underlayment, trim, transitions, removal, preparation and installation.",
            "steps": [("Measure the floor.", "Split irregular rooms into simple sections."), ("Add waste.", "Use a layout-specific allowance."), ("Price materials.", "Include flooring, underlayment, trim and transitions."), ("Add services.", "Include removal, subfloor preparation and labor.")],
            "formula": "early cost = material area × unit price + accessories + labor + preparation",
            "example": "A 500 ft² floor with 8% waste requires 540 ft² of product before adding underlayment, trim and installation.",
            "mistakes": "Do not compare product prices without checking coverage, grade, installation method and accessory requirements.",
            "faqs": [("Is installation priced by square foot?", "Often, but minimum charges, stairs, patterns and preparation can change the quote."), ("Do I need underlayment?", "Product and subfloor requirements determine whether underlayment is needed."), ("Should old flooring removal be separate?", "Yes. Removal and disposal can be a substantial part of the project.")],
        },
    ]
