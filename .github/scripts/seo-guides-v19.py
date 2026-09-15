from __future__ import annotations


def seo_guides() -> list[dict]:
    return [
    {
        "slug": "how-many-bags-of-deck-mud-do-i-need",
        "title": "How Many Bags of Deck Mud Do I Need?",
        "category": "Concrete & Masonry",
        "topic": "deck-mud",
        "parent": "deck-mud-calculator",
        "description": "Learn how to calculate deck mud bags from square footage, average bed depth, waste and the labeled yield of the dry-pack product.",
        "answer": "To estimate deck mud bags, multiply the area in square feet by the average bed depth in feet, add a visible waste allowance, divide by the product yield per bag and round up. Use the exact yield on the bag because dry-pack products do not all cover the same volume.",
        "steps": [
            [
                "Measure the bed area",
                "Record the actual length and width of each simple section in feet. For an irregular shower floor, split it into rectangles and add the areas."
            ],
            [
                "Choose the average depth",
                "Use the designed or specified average bed depth. A sloped base may need separate sections when the thickness changes materially."
            ],
            [
                "Calculate dry-pack volume",
                "Multiply area by depth after converting inches to feet. Keep the raw volume visible before adding waste."
            ],
            [
                "Convert volume to bags",
                "Add the project allowance, divide by the labeled yield per bag and round up to complete bags."
            ],
            [
                "Check the system",
                "Confirm drain, substrate, waterproofing, slope and product instructions before ordering or installing."
            ]
        ],
        "formula": "deck mud volume = area × (depth ÷ 12); bags = ceil(volume × (1 + waste) ÷ labeled yield)",
        "example": "A 4 ft × 4 ft area with an average 2 in bed is 2.67 ft³ before waste. With 10% allowance it is about 2.93 ft³. If the selected product yields 0.5 ft³ per bag, the planning quantity is 6 bags.",
        "mistakes": "Using the deepest point as the average, treating bag weight as volume, forgetting slope, or copying a generic yield instead of reading the selected product label.",
        "faqs": [
            [
                "Can I calculate deck mud by square feet?",
                "Yes. Square footage is the starting area, but bag quantity also depends on average depth, waste and the actual yield printed on the product."
            ],
            [
                "How much deck mud do I need for a 4×4 shower?",
                "The answer depends on the average bed depth and product yield. A 4×4 area at 2 inches is about 2.67 ft³ before waste."
            ],
            [
                "Is deck mud the same as concrete?",
                "No. Deck mud or dry-pack mortar has different proportions, workability and installation uses. Follow the selected system instructions."
            ]
        ]
    },
    {
        "slug": "how-to-calculate-marble-quantity",
        "title": "How to Calculate Marble Quantity in Square Feet",
        "category": "Flooring & Tile",
        "topic": "marble",
        "parent": "marble-quantity-calculator",
        "description": "Calculate marble tile square footage, pieces and boxes from measured area, tile dimensions, layout waste and package count.",
        "answer": "To calculate marble quantity, measure the surface in square feet, add waste for cuts and vein matching, divide by the face area of one tile, then round up pieces and complete boxes separately. The carton label and layout plan control the final order.",
        "steps": [
            [
                "Measure the surface",
                "Measure each floor, wall or backsplash section and add the areas. Subtract only fixed openings that will not receive tile."
            ],
            [
                "Convert tile size",
                "Multiply tile length by width in inches and divide by 144 to get square feet per tile."
            ],
            [
                "Add layout allowance",
                "Increase the net area for cuts, breakage, pattern, directional layout and marble vein matching."
            ],
            [
                "Calculate pieces and boxes",
                "Divide planned coverage by tile face area, round pieces up, then divide by pieces per box and round boxes up."
            ],
            [
                "Verify the lot",
                "Confirm tile shade, lot availability, returns and the installer’s layout before purchasing."
            ]
        ],
        "formula": "planned area = surface area × (1 + waste); pieces = ceil(planned area ÷ tile face area); boxes = ceil(pieces ÷ pieces per box)",
        "example": "A 60 ft² surface using 12 in × 24 in marble has a 2 ft² tile face. With 12% allowance, planned coverage is 67.2 ft², requiring 34 pieces before rounding to complete boxes.",
        "mistakes": "Using nominal room dimensions, ignoring vein matching, rounding only the square footage but not boxes, or assuming every carton has the same coverage.",
        "faqs": [
            [
                "How do I calculate marble quantity for a floor?",
                "Measure the floor area in square feet, add layout waste, divide by the square-foot face area of one tile and round up to complete cartons."
            ],
            [
                "How much extra marble should I buy?",
                "The allowance depends on tile size, room shape, pattern, cuts, breakage and vein matching. A simple rectangle and a book-matched layout should not use the same assumption."
            ],
            [
                "Does the calculator choose the marble layout?",
                "No. It estimates quantity. The installer or supplier should confirm direction, vein matching, lot consistency and final cuts."
            ]
        ]
    },
    {
        "slug": "how-many-bags-of-self-leveling-underlayment-do-i-need",
        "title": "How Many Bags of Self-Leveling Underlayment Do I Need?",
        "category": "Flooring & Tile",
        "topic": "self-leveling",
        "parent": "self-leveling-calculator",
        "description": "Estimate self-leveling underlayment bags from floor area, average depth, waste and the exact product yield.",
        "answer": "Estimate self-leveling bags by multiplying floor area by the measured average depth, adding waste, dividing by the labeled yield per bag and rounding up. Primer, minimum depth, maximum depth and substrate preparation can change the real requirement.",
        "steps": [
            [
                "Map the floor",
                "Measure the actual floor area and mark low spots, transitions, drains and areas that will not receive underlayment."
            ],
            [
                "Measure several depths",
                "Take readings across a grid and calculate a designed average rather than using one unusually deep low spot."
            ],
            [
                "Calculate volume",
                "Convert depth from inches to feet, then multiply area by average depth."
            ],
            [
                "Convert to bags",
                "Add the allowance, divide by the exact product yield and round up to complete bags."
            ],
            [
                "Check installation limits",
                "Verify primer, mixing time, edge dams, minimum/maximum depth and substrate compatibility."
            ]
        ],
        "formula": "underlayment volume = area × (average depth ÷ 12); bags = ceil(volume × (1 + waste) ÷ labeled yield)",
        "example": "A 200 ft² floor at a 1/4 in average depth is about 4.17 ft³ before allowance. With 10% allowance it is about 4.58 ft³; a product yielding 0.45 ft³ per bag would require 11 bags.",
        "mistakes": "Measuring only the deepest area, using floor-leveler coverage from another product, ignoring primer or porosity, or pouring beyond the product depth limit.",
        "faqs": [
            [
                "How many bags of self-leveling compound do I need?",
                "Use floor area, average depth, waste and the labeled yield per bag. Divide adjusted volume by the yield and round up."
            ],
            [
                "How do I measure average depth for self-leveler?",
                "Measure a grid of points, identify the designed finished level and use an approved average. Large variations may need separate sections or additional preparation."
            ],
            [
                "Does self-leveling compound fix every uneven floor?",
                "No. The substrate must be sound, clean, primed and within the product’s approved conditions. Follow the manufacturer’s installation method."
            ]
        ]
    },
    {
        "slug": "how-much-floor-mud-do-i-need",
        "title": "How Much Floor Mud Do I Need?",
        "category": "Concrete & Masonry",
        "topic": "floor-mud",
        "parent": "floor-mud-calculator",
        "description": "Calculate floor mud or dry-pack mortar volume and bags for tile beds, shower floors and measured mortar-bed areas.",
        "answer": "Calculate floor mud by multiplying the area by average bed thickness, adding waste, dividing by the specified product yield and rounding up to complete bags. For sloped or irregular floors, use designed sections instead of guessing one thickness.",
        "steps": [
            [
                "Measure each area",
                "Record the length and width of each mortar-bed section. Split L-shaped or irregular floors into simple rectangles."
            ],
            [
                "Determine average thickness",
                "Use the design or system specification. For a slope, calculate sections or a reliable average based on the finished elevations."
            ],
            [
                "Find volume",
                "Convert thickness to feet and multiply by area. Keep the raw mortar volume separate from waste."
            ],
            [
                "Convert to bags",
                "Add the chosen allowance, divide by the actual yield and round up."
            ],
            [
                "Check the installation system",
                "Confirm substrate, waterproofing, drain, slope and the specified mix before buying materials."
            ]
        ],
        "formula": "floor mud volume = area × (average thickness ÷ 12); bags = ceil(volume × (1 + waste) ÷ labeled yield)",
        "example": "A 5 ft × 6 ft area at a 1.5 in average bed is 3.75 ft³ before waste. With 10% allowance it is about 4.13 ft³; at 0.5 ft³ per bag, plan for 9 bags.",
        "mistakes": "Confusing floor mud with concrete, using the lowest or highest thickness as the average, forgetting slope, or treating the estimate as a waterproofing or structural design.",
        "faqs": [
            [
                "How much floor mud do I need?",
                "Multiply floor area by average bed thickness in feet, add waste, divide by the product yield and round up to complete bags."
            ],
            [
                "Is floor mud the same as concrete?",
                "No. Floor mud or dry-pack mortar has different proportions and uses. Use the mix specified for the installation system."
            ],
            [
                "How do I calculate a sloped shower floor?",
                "Use the designed average thickness or split the slope into sections. The drain, waterproofing and system requirements must be confirmed separately."
            ]
        ]
    },
    {
        "slug": "how-much-mortar-do-i-need-for-tuckpointing",
        "title": "How Much Mortar Do I Need for Tuckpointing?",
        "category": "Concrete & Masonry",
        "topic": "tuckpointing",
        "parent": "tuckpointing-calculator",
        "description": "Estimate tuckpointing and repointing mortar from joint length, width, depth, waste and the labeled product yield.",
        "answer": "Estimate tuckpointing mortar by multiplying total joint length by joint width and depth, adding allowance for irregular joints and preparation loss, dividing by the labeled yield and rounding up. Mortar compatibility matters as much as quantity.",
        "steps": [
            [
                "Measure joint length",
                "Add the linear feet of all repair runs. For a wall, measure representative sections if the joint pattern is consistent."
            ],
            [
                "Measure width and depth",
                "Use actual joint dimensions in inches and convert them to feet for the volume calculation."
            ],
            [
                "Calculate joint volume",
                "Multiply length by width and depth. Include only the material being removed and replaced."
            ],
            [
                "Add preparation allowance",
                "Account for irregular joints, voids, overfill, cleanup and unavoidable loss, then convert to bags using actual yield."
            ],
            [
                "Verify mortar compatibility",
                "Check strength, color, vapor behavior, historic-masonry requirements and the repair specification before mixing."
            ]
        ],
        "formula": "mortar volume = length × (joint width ÷ 12) × (joint depth ÷ 12); bags = ceil(volume × (1 + waste) ÷ labeled yield)",
        "example": "A 500 linear-foot run at 3/8 in wide and 3/4 in deep is about 0.37 ft³ before allowance. With 20% allowance it is about 0.44 ft³; at 0.5 ft³ per bag, the arithmetic rounds to 1 bag, but actual preparation may require more.",
        "mistakes": "Measuring visible face area instead of joint volume, assuming all joints have the same depth, using an incompatible high-strength mortar, or ignoring removal and preparation loss.",
        "faqs": [
            [
                "How much mortar do I need for tuckpointing?",
                "Multiply joint length by joint width and depth in feet, add an allowance for irregular work, divide by labeled yield and round up."
            ],
            [
                "How deep should joints be removed?",
                "Remove deteriorated material only as required by the repair specification and use suitable tools and safety practices."
            ],
            [
                "Can I use any mortar for tuckpointing?",
                "No. Mortar strength, movement, color, vapor behavior and historic-masonry compatibility should be checked before selecting a product."
            ]
        ]
    },
    {
        "slug": "how-much-concrete-do-i-need-for-a-screed",
        "title": "How Much Concrete Do I Need for a Screed?",
        "category": "Concrete & Masonry",
        "topic": "concrete-screed",
        "parent": "concrete-screed-calculator",
        "description": "Calculate concrete volume for a screed-formed slab or pour in cubic yards and cubic meters, including a visible ordering allowance.",
        "answer": "For a screed-formed pour, multiply length by width by thickness, convert the volume to cubic yards or cubic meters, add a stated allowance and confirm the supplier’s delivery increment. Screeding levels concrete but does not change the geometric volume.",
        "steps": [
            [
                "Measure the pour",
                "Record the actual length and width of the slab or section. Split complex shapes into measurable rectangles."
            ],
            [
                "Confirm thickness",
                "Use the specified slab thickness and check edges, slopes, thickened areas and subgrade variation."
            ],
            [
                "Calculate raw volume",
                "Multiply length by width by thickness after converting inches to feet, then convert cubic feet to cubic yards."
            ],
            [
                "Add an order allowance",
                "Keep waste, subgrade variation and ordering minimums visible rather than hiding them in a rounded result."
            ],
            [
                "Confirm placement logistics",
                "Check truck access, pump or wheelbarrow placement, crew size, finishing window and supplier minimums."
            ]
        ],
        "formula": "concrete volume = length × width × (thickness ÷ 12); cubic yards = cubic feet ÷ 27; order volume = volume × (1 + allowance)",
        "example": "A 20 ft × 12 ft pour at 4 in is 960 ft³, or about 2.96 yd³ before allowance. With 7% allowance it is about 3.17 yd³; the supplier may require a different order increment.",
        "mistakes": "Rounding raw volume down, ignoring thickened edges or uneven subgrade, treating screeding as a quantity adjustment, or ordering without confirming truck access and minimum load.",
        "faqs": [
            [
                "How much concrete do I need for a screed?",
                "Calculate length × width × thickness, convert to cubic yards or cubic meters, add an allowance and confirm the supplier order increment."
            ],
            [
                "What does screed mean in concrete work?",
                "A screed strikes off and levels freshly placed concrete. The concrete quantity still comes from the pour geometry."
            ],
            [
                "Does screeding change the concrete volume?",
                "No. It changes placement and finishing; thickness, dimensions, subgrade and thickened sections determine quantity."
            ]
        ]
    }
]
