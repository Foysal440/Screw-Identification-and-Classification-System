import pytest
import json
import os

# Path to the JSON data file
json_path = r"C:\Users\FOYSAL\PycharmProjects\screwAnalysis\Functional_Test\test_screw_data.json"

# Load the JSON file
try:
    with open(json_path, "r") as f:
        category_info = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"Error: 'test_screw_data.json' not found at {json_path}")

# Test for missing attributes in the JSON data
def test_missing_attributes():
    required_attributes = [
        "name", "type", "material", "size", "head_type", "drive_type",
        "thread_type", "strength_grade", "coating", "application", "description"
    ]

    for category_id, attributes in category_info.items():
        for attr in required_attributes:
            assert attr in attributes, f"Missing attribute '{attr}' in category {category_id}"
            assert attributes[attr] is not None, f"Attribute '{attr}' in category {category_id} is None"

# Test for unique category IDs
def test_unique_category_ids():
    category_ids = list(category_info.keys())
    assert len(category_ids) == len(set(category_ids)), "Duplicate category IDs found in JSON data."

# Test for valid attribute values
def test_valid_attribute_values():
    for category_id, attributes in category_info.items():
        assert attributes["name"].strip(), f"Invalid 'name' for category {category_id}"
        assert attributes["type"] in ["Screw", "Nut", "Bolt"], f"Invalid 'type' for category {category_id}"
        assert attributes["material"].strip(), f"Invalid 'material' for category {category_id}"
        assert attributes["size"].startswith("M"), f"Invalid 'size' for category {category_id}"
        assert attributes["head_type"].strip(), f"Invalid 'head_type' for category {category_id}"
        assert attributes["drive_type"].strip(), f"Invalid 'drive_type' for category {category_id}"
        assert attributes["application"].strip(), f"Invalid 'application' for category {category_id}"

# Test for duplicates in names or descriptions
def test_no_duplicate_names_or_descriptions():
    names = set()
    descriptions = set()

    for category_id, attributes in category_info.items():
        name = attributes["name"]
        description = attributes["description"]

        assert name not in names, f"Duplicate name found: {name}"
        assert description not in descriptions, f"Duplicate description found: {description}"

        names.add(name)
        descriptions.add(description)

# Test for description length
def test_description_length():
    for category_id, attributes in category_info.items():
        description = attributes["description"]
        assert 20 <= len(description) <= 500, (
            f"Description length for category {category_id} is invalid. Length: {len(description)}"
        )

# Test for proper size format
def test_size_format():
    for category_id, attributes in category_info.items():
        size = attributes["size"]
        assert size.startswith("M") and size[1:].isdigit(), f"Invalid size format for category {category_id}: {size}"

# Test for valid strength grade format
def test_strength_grade_format():
    for category_id, attributes in category_info.items():
        strength_grade = attributes["strength_grade"]
        assert strength_grade.startswith("Grade "), f"Invalid strength grade format for category {category_id}"
        grade_number = strength_grade.split(" ")[-1]
        assert grade_number.replace(".", "").isdigit(), f"Invalid strength grade value for category {category_id}"
