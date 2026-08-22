from __future__ import annotations

def seo_guides() -> list[dict]:
    pages=[
        ("concrete-driveway-thickness-guide","Concrete Driveway Thickness Planning Guide","Concrete & Masonry","concrete","concrete-driveway-calculator"),
        ("concrete-footing-size-guide","Concrete Footing Volume Planning Guide","Concrete & Masonry","concrete","concrete-footing-calculator"),
        ("small-bathroom-remodel-budget","Small Bathroom Remodel Budget Guide","Renovation & Remodeling","flooring","bathroom-remodel-cost-calculator"),
        ("kitchen-backsplash-tile-calculator","How to Calculate Kitchen Backsplash Tile","Flooring & Tile","flooring","kitchen-tile-calculator"),
        ("room-flooring-square-footage-guide","How to Calculate Room Flooring Square Footage","Flooring & Tile","flooring","room-flooring-calculator"),
        ("garden-bed-soil-depth-guide","Garden Bed Soil Depth Planning Guide","Landscaping","landscaping","garden-bed-soil-calculator"),
        ("river-rock-coverage-guide","How to Calculate River Rock Coverage","Landscaping","landscaping","river-rock-calculator"),
        ("roof-shingle-waste-guide","Roof Shingle Waste and Bundle Planning Guide","Roofing, Decks & Fences","roofing-decks-fences","shingle-calculator"),
        ("deck-material-waste-guide","Deck Material Waste Planning Guide","Roofing, Decks & Fences","roofing-decks-fences","deck-board-calculator"),
        ("exterior-paint-coverage-guide","Exterior Paint Coverage Planning Guide","Paint & Finishes","paint","exterior-paint-calculator"),
    ]
    result=[]
    for slug,title,category,topic,parent in pages:
        result.append({
            "slug":slug,"title":title,"category":category,"topic":topic,"parent":parent,
            "description":f"Practical planning guidance for {title.lower().replace(' guide','')}, with visible measurements, assumptions and purchase rounding.",
            "answer":"Start with measured project dimensions, use the exact product or project specification, keep waste and package rounding separate, and confirm final quantities with a supplier or qualified professional.",
            "steps":[("Define the project.","Separate rooms, surfaces, sections or material layers."),("Measure accurately.","Use consistent units and record each dimension."),("Apply the right assumptions.","Use product coverage, installed depth, spacing, pitch or project scope."),("Round and review.","Round to supplier units and check site, code and installation requirements.")],
            "formula":"planning quantity = measured geometry × product or project factor",
            "example":"A transparent estimate keeps the measured area or volume visible, then shows allowances, package coverage and rounding before the final planning quantity.",
            "mistakes":"Do not copy a generic allowance or product yield when the selected material label, layout or site condition provides more specific information.",
            "faqs":[("Is this a final quote?","No. It is a planning estimate before local supplier and contractor confirmation."),("Why do quantities vary?","Product size, installation method, layout, access, waste and site conditions all affect the result."),("When is professional advice needed?","Use qualified guidance for structural, roofing, waterproofing, utility and code-related decisions.")],
        })
    return result
