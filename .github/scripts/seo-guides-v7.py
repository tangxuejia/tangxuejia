from __future__ import annotations

def seo_guides() -> list[dict]:
    pages = [
        ("concrete-patio-cost-guide","How Much Does a Concrete Patio Cost?","Concrete & Masonry","concrete","concrete-cost-calculator","Build an early concrete patio budget from slab volume, forms, reinforcement, finishing and labor.","Separate measured concrete quantity from forms, base preparation, delivery, finishing and labor before comparing prices."),
        ("concrete-walkway-calculator-guide","How to Calculate Concrete for a Walkway","Concrete & Masonry","concrete","concrete","Estimate walkway concrete from length, width, thickness and separate sections.","Measure each walkway section, calculate volume in cubic feet, convert to cubic yards and keep allowance visible."),
        ("flooring-box-coverage-guide","How to Read Flooring Box Coverage","Flooring & Tile","flooring","flooring-box-calculator","Use the exact square-foot coverage printed on a flooring carton to avoid under-ordering.","Carton coverage varies by product and must be used after waste is added to the measured area."),
        ("hardwood-flooring-waste-guide","Hardwood Flooring Waste Percentage Guide","Flooring & Tile","flooring","hardwood-flooring-calculator","Plan hardwood flooring waste for room shape, board length, layout and cuts.","Simple rooms may need less allowance than angled layouts, multiple rooms and pattern-sensitive installations."),
        ("paint-primer-coverage-guide","How Much Primer Do I Need?","Paint & Finishes","paint","paint-coverage-calculator","Estimate primer from surface area, coats and the actual product coverage rate.","Primer coverage depends on the product, substrate, porosity and color transition; calculate it separately from finish paint."),
        ("paint-fence-calculator-guide","How Much Paint for a Fence?","Paint & Finishes","paint","fence-paint-calculator","Estimate fence paint from total fence surface, both sides, coats and product coverage.","Measure fence length and height, determine whether one or both sides are painted, then apply coats and coverage."),
        ("topsoil-volume-guide","How to Calculate Topsoil Volume","Landscaping","landscaping","topsoil-calculator","Convert garden bed length, width and depth into topsoil cubic yards or bags.","Use installed depth in feet, calculate cubic feet and divide by 27 for cubic yards."),
        ("mulch-cubic-yard-guide","How Many Cubic Yards of Mulch Do I Need?","Landscaping","landscaping","mulch","Estimate bulk mulch from bed area and installed depth before ordering by cubic yard.","Calculate each bed section separately, add volumes and review existing mulch before choosing the final depth."),
        ("shingle-bundle-calculator-guide","How Many Shingle Bundles Do I Need?","Roofing, Decks & Fences","roofing-decks-fences","shingle-calculator","Convert roofing squares into shingle bundles using the exact package coverage and roof layout.","Estimate roof squares first, then use the selected shingle label because bundle coverage varies by product and exposure."),
        ("deck-board-linear-feet-guide","How Many Deck Boards Do I Need?","Roofing, Decks & Fences","roofing-decks-fences","deck-board-calculator","Estimate deck-board rows and linear feet from deck size, board width, gap and waste.","Use actual installed board face width, add the required gap, round rows up and include board-length cuts."),
    ]
    result=[]
    for slug,title,category,topic,parent,description,answer in pages:
        result.append({
            "slug":slug,"title":title,"category":category,"topic":topic,"parent":parent,
            "description":description,"answer":answer,
            "steps":[("Measure the project.","Use consistent units and split irregular areas into simple sections."),("Choose product assumptions.","Use the exact coverage, package size, board width or density."),("Calculate quantity.","Apply the visible area, volume or row formula."),("Round the purchase.","Use complete boxes, bags, bundles, rolls or boards.")],
            "formula":"purchase quantity = measured quantity × project factor, rounded to the supplier unit",
            "example":"Start with measured geometry, add the project-specific allowance, then round using the actual product package or supplier rule.",
            "mistakes":"Do not use a generic product coverage or hidden waste percentage when the selected product label provides better information.",
            "faqs":[("Is this a final purchase quantity?","No. Confirm product specifications, site conditions and supplier ordering rules before buying."),("Why is waste separate?","Waste depends on cuts, layout, breakage and installation complexity, not just geometric area."),("Can this replace professional advice?","No. Structural, roofing, waterproofing and code-related work should be confirmed with qualified professionals.")],
        })
    return result
