from __future__ import annotations

def seo_guides() -> list[dict]:
    return [
        {
            "slug": "home-improvement-material-calculator-reference",
            "title": "Home Improvement Material Calculator Reference",
            "category": "Renovation Planning",
            "topic": "renovation",
            "parent": "renovation-cost-calculator",
            "description": "A practical way to turn measurements into material quantities, package counts and a safer buying checklist before a home-improvement project.",
            "answer": "The most useful estimate is not one big number: it connects the measured area or volume to the exact product coverage, a visible waste allowance and the way the material is sold. Measure each project section, calculate the needed amount, round to complete packages or delivery units, then verify the label, site conditions and supplier minimums before buying.",
            "steps": [
                ("Measure the real work", "Split the project into simple sections and record length, width, depth, openings, slopes or linear runs with the units shown."),
                ("Calculate the needed quantity", "Use the related calculator and keep raw volume, coverage, waste and package rounding visible so the result can be checked."),
                ("Match the product", "Replace generic coverage, yield, density, stock length or spacing assumptions with the exact product or supplier data."),
                ("Plan the purchase", "Round up to complete bags, boxes, cans, bundles, stock lengths or delivery increments, then compare access, labor and return limits."),
                ("Run a final risk check", "Confirm permits, structural requirements, substrate, drainage, delivery access and any condition that can change the estimate."),
            ],
            "formula": "purchase quantity = ceil((measured quantity × (1 + project allowance)) ÷ exact package coverage or yield)",
            "example": "For a 200 ft² flooring area with 10% layout allowance and cartons covering 20 ft², plan for 220 ft² and buy 11 complete cartons. For concrete, use volume and the exact bag yield or supplier order unit instead of treating bag weight as coverage.",
            "mistakes": "Using floor area for wall paint, using nominal package size instead of labeled coverage, rounding down, hiding waste inside an unexplained number, and treating a planning estimate as a structural design or fixed quote.",
            "faqs": [
                ("Why does the same project need different quantities with different products?", "Coverage, yield, density, package size and installation method vary by product, so the exact label or supplier sheet should control the final purchase estimate."),
                ("How much waste should I add?", "There is no universal percentage. Use the layout, cuts, shape, surface condition and installer or supplier guidance, and keep the allowance visible."),
                ("Can RenoMetric replace a contractor, engineer or inspector?", "No. RenoMetric explains planning arithmetic and assumptions. Safety-critical design, permits, site conditions and final quotes require the appropriate qualified professional."),
                ("What is the fastest way to use this site?", "Start with the calculator closest to the material, read the assumptions beside the result, then open the related guide to check what the number leaves out."),
            ],
        },
    ]
