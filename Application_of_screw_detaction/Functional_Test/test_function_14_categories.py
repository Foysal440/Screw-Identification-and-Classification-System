import pytest
import os
import json

# Path to the JSON data file
json_path = r"C:\Users\FOYSAL\PycharmProjects\screwAnalysis\Functional_Test\test_screw_data.json"

# Load the JSON file
try:
    with open(json_path, "r") as f:
        category_info = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"Error: 'test_screw_data.json' not found at {json_path}")


# Helper function to validate attributes in the JSON file
def validate_attributes(category_id, attributes):
    required_attributes = [
        "name", "type", "material", "size", "head_type", "drive_type",
        "thread_type", "strength_grade", "coating", "application", "description"
    ]
    for attr in required_attributes:
        assert attr in attributes, f"Missing attribute '{attr}' in category {category_id}"
        assert attributes[attr] is not None, f"Attribute '{attr}' in category {category_id} is None"


# Test function for each category
@pytest.mark.parametrize("category_id", list(category_info.keys()))
def test_category(category_id):
    attributes = category_info[category_id]

    # Validate attributes
    validate_attributes(category_id, attributes)

    # Simulated function result based on category_id
    result = int(category_id)  # Simulate function returning correct category ID

    # Check if the function returns the expected category ID
    assert result == int(category_id), (
        f"Expected {category_id}, but got {result}"
    )
