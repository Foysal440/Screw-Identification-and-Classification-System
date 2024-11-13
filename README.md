# Screw-Identification-and-Classification-System
This project provides a tool for analyzing and identifying various types of screws, bolts, and nuts based on uploaded images. Using basic feature detection with OpenCV, the tool classifies the screw type and provides detailed information on the detected item, including material, head type, thread type, strength grade, coating, and application. This tool is particularly useful for professionals in manufacturing, construction, and repair who need fast, detailed identification of hardware.

# Features
Image Analysis with OpenCV: Uses edge detection and contour analysis to identify screw types based on visual features.
Comprehensive Screw Database: Includes detailed information for each screw type, covering material, size, head and drive types, and more.
User-Friendly Interface: Allows users to upload an image of a screw and receive detailed information about the screw’s specifications and typical applications.
# Demo
Once an image is uploaded, the tool will:

# Display the image.
Identify and classify the screw type based on contour analysis.
Output a detailed report about the screw, including name, type, material, size, coating, and a description of its typical uses.
# Getting Started
Prerequisites
Python 3.6+
Jupyter Notebook (or Google Colab)
Required libraries:
OpenCV
NumPy
Matplotlib
PIL (Python Imaging Library)
IPyWidgets (for the file upload widget)
# Install dependencies using:
pip install opencv-python-headless numpy matplotlib pillow ipywidgets shapely
# Installation
Clone the repository:git clone https://github.com/Foysal440/screw-identification.git
# Navigate to the project directory:

# cd screw-identification
Launch Jupyter Notebook:

# jupyter notebook
Open the notebook and follow the instructions to run the tool.
# Usage
###Upload an Image: Use the provided widget to upload an image of a screw.
###Analyze the Image: The program will process the image, detecting contours and analyzing features.
###View the Results: After processing, the tool displays detailed information about the screw, including:
Name, type, material, size, head and drive types, thread type, strength grade, coating, and application.Project Structure
###notebook.ipynb: Main notebook file for running the tool.
###category_info.py: Contains the detailed category information for each screw type.
###utils.py: Utility functions for feature detection, image display, and analysis.
# Contributing
Contributions are welcome! Please submit a pull request or open an issue if you have suggestions for improvement.

# License
This project is licensed under the MIT License. See LICENSE for more details.

# Contact
For questions or feedback, feel free to reach out:

Email: niloyhasanfoysal440@gmail.com
GitHub: Foysal440
