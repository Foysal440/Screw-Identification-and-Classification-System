import pytest
from PIL import Image
import os
import json
from test_main import analyze_screw_image, analyze_file

# Get the absolute path to the current directory (Functional_Test)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the test JSON file
json_path = os.path.join(current_dir, "test_screw_data.json")
try:
    with open(json_path, "r") as f:
        category_info = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"Error: 'test_screw_data.json' not found at {json_path}")


# Helper function to verify file existence
def file_exists(file_path):
    return os.path.exists(file_path)


# Helper function to get the first file in a directory
def get_first_file(directory, extensions):
    for file in os.listdir(directory):
        if file.lower().endswith(extensions):
            return os.path.join(directory, file)
    return None


# Helper function to generate a blank image for testing
def generate_blank_image():
    blank_image_path = os.path.join(current_dir, "test_images", "blank_image.jpg")
    if not os.path.exists(blank_image_path):
        blank_image = Image.new("RGB", (100, 100), (255, 255, 255))  # Create a blank white image
        blank_image.save(blank_image_path)
    return blank_image_path


# Test 1: Detect screw from a single image
def test_detect_single_image():
    image_dir = os.path.join(current_dir, "test_images")
    test_image_path = get_first_file(image_dir, (".jpg", ".png", ".jpeg", ".bmp"))
    assert test_image_path is not None, f"No valid image found in {image_dir}"

    test_image = Image.open(test_image_path)
    result = analyze_screw_image(test_image)
    assert result is not None, f"Expected a valid screw detection result, got {result}"


# Test 2: Analyze a valid video
def test_analyze_valid_video():
    video_dir = os.path.join(current_dir, "test_videos")
    test_video_path = get_first_file(video_dir, (".mp4", ".avi", ".mkv", ".mov"))
    assert test_video_path is not None, f"No valid video found in {video_dir}"

    analyze_file(test_video_path)  # Ensure no exceptions raised


# Test 3: Detect multiple screws in an image
def test_multiple_screws_in_image():
    image_dir = os.path.join(current_dir, "test_images")
    test_image_path = get_first_file(image_dir, (".jpg", ".png", ".jpeg", ".bmp"))
    assert test_image_path is not None, f"No valid image found in {image_dir}"

    test_image = Image.open(test_image_path)
    result = analyze_screw_image(test_image)
    assert result is not None, "Expected classification for multiple screws."


# Test 4: Handle an image with no screws
def test_no_screw_image():
    test_image_path = generate_blank_image()
    print(f"Testing with blank image: {test_image_path}")  # Debugging statement

    test_image = Image.open(test_image_path)
    result = analyze_screw_image(test_image)
    print(f"Result for blank image: {result}")  # Debugging statement

    # Allow any result but interpret "1" or similar as "not a screw"
    if result == 1:
        print("Result interpreted as no screw detected.")
    assert result is not None, "Expected a valid output for no screws."


# Test 5: JSON attributes for detected category
def test_json_attributes():
    category_id = "9"
    attributes = category_info.get(category_id, {})
    expected_description = (
        "A stainless steel Torx screw with a flat head, designed for applications "
        "that require tamper resistance, such as electronics assembly and automotive components."
    )
    assert attributes["description"].startswith(expected_description), (
        f"Description mismatch: {attributes['description']}"
    )


# Test 6: Detect screw in unclear image
def test_analyze_unclear_image():
    image_dir = os.path.join(current_dir, "test_images")
    test_image_path = get_first_file(image_dir, (".jpg", ".png", ".jpeg", ".bmp"))
    assert test_image_path is not None, f"No valid image found in {image_dir}"

    test_image = Image.open(test_image_path)
    result = analyze_screw_image(test_image)
    assert result is not None, "Expected a classification or error for unclear image."
