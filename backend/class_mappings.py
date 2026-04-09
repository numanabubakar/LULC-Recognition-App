"""Class label mappings for each LULC dataset."""

EUROSAT_CLASSES = {
    0: "Annual Crop",
    1: "Forest",
    2: "Herbaceous Vegetation",
    3: "Highway",
    4: "Industrial",
    5: "Pasture",
    6: "Permanent Crop",
    7: "Residential",
    8: "River",
    9: "Sea Lake"
}

MLRSNET_CLASSES = {
    0: "Airplane",
    1: "Airport",
    2: "Bareland",
    3: "Baseball Diamond",
    4: "Basketball court",
    5: "Beach",
    6: "Bridge",
    7: "Chaparral",
    8: "Cloud",
    9: "Commercial Area",
    10: "Dense Residential Area",
    11: "Desert",
    12: "Eroded Farmland",
    13: "Farmland",
    14: "Forest",
    15: "Freeway",
    16: "Golf Course",
    17: "Ground Track Field",
    18: "Harbor Port",
    19: "Industrial Area",
    20: "intersection",
    21: "Island",
    22: "Lake",
    23: "Meadow",
    24: "Mobile Home Park",
    25: "Mountain",
    26: "Overpass",
    27: "Park",
    28: "Parking Lot",
    29: "Parkway",
    30: "Railway",
    31: "Railway Station",
    32: "River",
    33: "Roundabout",
    34: "Shipping Yard",
    35: "Snowberg",
    36: "Sparse Residential Area",
    37: "Stadium",
    38: "Storage Tank",
    39: "Swimming Pool",
    40: "Tennis Court",
    41: "Terrace",
    42: "Transmission Tower",
    43: "Vegetable Greenhouse",
    44: "Wetland",
    45: "Wind Turbine",
}

PATTERNNET_CLASSES = {
    0: "Airplane",
    1: "Baseball diamond",
    2: "Basketball court",
    3: "Beach",
    4: "Bridge",
    5: "Cemetery",
    6: "Chaparral",
    7: "Christmas Tree Farm",
    8: "Closed Road",
    9: "Coastal Mansion",
    10: "Crosswalk",
    11: "Dense Residential",
    12: "Ferry Terminal",
    13: "Football Field",
    14: "Forest",
    15: "Freeway",
    16: "Golf Course",
    17: "Harbor",
    18: "Intersection",
    19: "Mobile Home Park",
    20: "Nursing Home",
    21: "Oil Gas Field",
    22: "Oil Well",
    23: "Overpass",
    24: "Parking Lot",
    25: "Parking Space",
    26: "Railway",
    27: "River",
    28: "Runway",
    29: "Runway Marking",
    30: "Shipping Yard",
    31: "Solar Panel",
    32: "Sparse Residential",
    33: "Storage Tank",
    34: "Swimming Pool",
    35: "Tennis Court",
    36: "Transformer Station",
    37: "Wastewater Treatment Plant",
     
}

def get_class_label(model_type: str, class_idx: int) -> str:
    """Get class label for given model type and class index."""
    mappings = {
        "eurosat": EUROSAT_CLASSES,
        "mlrsnet": MLRSNET_CLASSES,
        "patternnet": PATTERNNET_CLASSES,
    }
    return mappings[model_type].get(class_idx, f"Unknown Class {class_idx}")


def get_num_classes(model_type: str) -> int:
    """Get number of classes for given model type."""
    mappings = {
        "eurosat": EUROSAT_CLASSES,
        "mlrsnet": MLRSNET_CLASSES,
        "patternnet": PATTERNNET_CLASSES,
    }
    return len(mappings[model_type])
