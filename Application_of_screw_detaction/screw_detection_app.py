import json
import os
import cv2
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from PIL import Image as PILImage
from kivy.graphics.texture import Texture
from skimage.feature import local_binary_pattern

class ScrewDetectionApp(App):
    def build(self):
        self.title = "Screw Detection System"
        self.file_path = None

        # Load screw category information from JSON
        try:
            with open("screw_data.json", "r") as f:
                self.category_info = json.load(f)
        except FileNotFoundError:
            self.category_info = {}
            print("Error: 'screw_data.json' file not found.")

        # Main layout
        main_layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Title label
        title_label = Label(
            text="Screw Detection System",
            size_hint=(1, 0.1),
            font_size="24sp",
            bold=True
        )
        main_layout.add_widget(title_label)

        # Instruction label
        instruction_label = Label(
            text="Upload an Image or Video for Analysis or Drag and Drop Files",
            size_hint=(1, 0.1),
            font_size="16sp"
        )
        main_layout.add_widget(instruction_label)

        # Display area for image or video
        self.image_widget = Image(size_hint=(1, 0.6))
        main_layout.add_widget(self.image_widget)

        # Buttons for file upload and analysis
        button_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.1), spacing=10)

        upload_button = Button(text="Upload File", size_hint=(0.5, 1))
        upload_button.bind(on_press=self.open_file_chooser)
        button_layout.add_widget(upload_button)

        analyze_button = Button(text="Analyze File", size_hint=(0.5, 1))
        analyze_button.bind(on_press=self.analyze_file)
        button_layout.add_widget(analyze_button)

        main_layout.add_widget(button_layout)

        # Results display
        self.result_display = TextInput(
            text="Analysis results will be displayed here.",
            size_hint=(1, 0.2),
            readonly=True,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            font_size="14sp",
        )
        main_layout.add_widget(self.result_display)

        # Enable drag and drop
        Window.bind(on_dropfile=self.on_file_drop)

        return main_layout

    def open_file_chooser(self, instance):
        filechooser_popup = BoxLayout(orientation="vertical", padding=10, spacing=10)
        filechooser = FileChooserListView(
            filters=["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tiff", "*.mp4", "*.avi", "*.mkv", "*.mov"]
        )
        filechooser_popup.add_widget(filechooser)

        select_button = Button(text="Select", size_hint=(1, 0.2))
        select_button.bind(
            on_press=lambda x: self.load_file(filechooser.selection[0] if filechooser.selection else None)
        )
        filechooser_popup.add_widget(select_button)

        popup = Popup(title="Select File", content=filechooser_popup, size_hint=(0.9, 0.9))
        select_button.bind(on_press=popup.dismiss)
        popup.open()

    def on_file_drop(self, window, file_path):
        self.load_file(file_path.decode("utf-8"))

    def load_file(self, file_path):
        if file_path and os.path.isfile(file_path):
            self.file_path = file_path
            if self.file_path.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff")):
                img = PILImage.open(self.file_path)
                img.thumbnail((400, 400))
                data = np.array(img)
                texture = Texture.create(size=(data.shape[1], data.shape[0]), colorfmt="rgb")
                texture.blit_buffer(data.tobytes(), colorfmt="rgb", bufferfmt="ubyte")
                self.image_widget.texture = texture
                self.result_display.text = f"Selected Image: {self.file_path}"
            elif self.file_path.lower().endswith((".mp4", ".avi", ".mkv", ".mov")):
                self.result_display.text = f"Selected Video: {self.file_path}"
                self.image_widget.source = ""
            else:
                self.result_display.text = "Unsupported file format!"
        else:
            self.result_display.text = "No file selected or file not found!"

    def analyze_file(self, instance):
        if self.file_path:
            if self.file_path.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff")):
                self.result_display.text = "Analyzing Image..."
                analysis_result = self.analyze_image(self.file_path)
                self.result_display.text = analysis_result
            elif self.file_path.lower().endswith((".mp4", ".avi", ".mkv", ".mov")):
                self.result_display.text = "Analyzing Video..."
                analysis_result = self.analyze_video(self.file_path)
                self.result_display.text = analysis_result
            else:
                self.result_display.text = "Unsupported File Format!"
        else:
            self.result_display.text = "No file selected!"

    def is_screw_detected(self, file_path):
        """
        Finalized screw detection logic: Balances flexible screw detection and strict non-screw rejection.
        """
        try:
            # Step 1: Load the image and convert to grayscale
            img = PILImage.open(file_path)
            img_cv = np.array(img)
            gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)

            # Step 2: Preprocessing
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Reduce noise
            edges = cv2.Canny(blurred, threshold1=30, threshold2=100)  # Edge detection
            edge_density = np.sum(edges > 0) / edges.size  # Calculate edge density

            print(f"Edge density: {edge_density:.4f}")  # Debugging feedback

            # Step 3: Validate Edge Density
            if edge_density < 0.005 or edge_density > 0.35:  # Screws have moderate edge density
                print("Rejected: Edge density outside valid range.")
                return False

            # Step 4: Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contours:
                print("Rejected: No contours found.")
                return False  # No contours found

            # Step 5: Analyze the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            perimeter = cv2.arcLength(largest_contour, True)
            circularity = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0
            x, y, w, h = cv2.boundingRect(largest_contour)
            aspect_ratio = float(w) / h

            print(
                f"Area: {area}, Circularity: {circularity:.4f}, Aspect Ratio: {aspect_ratio:.4f}")  # Debugging feedback

            # Step 6: Validate Contour Properties
            if area < 300 or area > 50000:  # Allow small to medium screws
                print("Rejected: Area outside valid range.")
                return False
            if circularity < 0.1 or circularity > 1.2:  # Allow slightly irregular shapes
                print("Rejected: Circularity outside valid range.")
                return False
            if aspect_ratio < 0.2 or aspect_ratio > 6.0:  # Allow screws to be elongated or slightly wide
                print("Rejected: Aspect ratio outside valid range.")
                return False

            # Step 7: Validate Thread-Like Structures (Optional)
            child_contours, _ = cv2.findContours(edges[y:y + h, x:x + w], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            thread_contours = [c for c in child_contours if 20 < cv2.contourArea(c) < 500]

            print(f"Thread count: {len(thread_contours)}")  # Debugging feedback

            if len(thread_contours) < 2:  # Require at least 2 thread-like features
                print("Warning: Not enough thread-like structures, but continuing.")

            # Step 8: Validate Edge Alignment
            edge_projection = np.sum(edges[y:y + h, x:x + w], axis=1)  # Vertical edge projection
            edge_variation = np.std(edge_projection) / np.mean(edge_projection)
            print(f"Edge variation: {edge_variation:.4f}")  # Debugging feedback
            if edge_variation > 2.5:  # Reject chaotic edge patterns
                print("Rejected: Edge alignment too chaotic.")
                return False

            # Step 9: Final Check
            print("Screw detected!")
            return True

        except Exception as e:
            print(f"Error in screw detection: {e}")
            return False

    def analyze_image(self, file_path):
        """
        Analyze an image and classify the screw with refined logic.
        """
        try:
            # Step 1: Check if a screw is present in the image
            if not self.is_screw_detected(file_path):
                return "No screw detected in the image. Please upload a valid screw image."

            # Step 2: Load the image and preprocess
            img = PILImage.open(file_path)
            img_cv = np.array(img)
            gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)

            # Enhanced edge detection
            edges = cv2.Canny(gray, threshold1=50, threshold2=150)

            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            area = cv2.contourArea(largest_contour)
            perimeter = cv2.arcLength(largest_contour, True)
            aspect_ratio = float(w) / h
            circularity = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0

            # Decision logic based on extracted features
            if aspect_ratio > 0.8 and aspect_ratio < 1.2 and circularity > 0.8:
                category_id = "5"  # Shiny Screw (Circular, decorative projects)
            elif aspect_ratio < 0.5 and area > 10000:
                category_id = "1"  # Long Lag Screw (Heavy-duty fastening)
            elif aspect_ratio < 0.5 and area <= 10000:
                category_id = "2"  # Lag Wood Screw (Structural fastening)
            elif aspect_ratio > 1.2 and circularity < 0.6:
                category_id = "3"  # Wood Screw (General fastening)
            elif aspect_ratio > 0.8 and aspect_ratio < 1.2 and circularity < 0.8:
                category_id = "6"  # Black Oxide Screw (Industrial/automotive)
            elif area > 15000:
                category_id = "8"  # Bolt (Heavy-duty)
            elif aspect_ratio > 0.8 and aspect_ratio < 1.2 and w < 50 and h < 50:
                category_id = "10"  # Phillips Screw (General home projects)
            elif aspect_ratio > 0.8 and aspect_ratio < 1.2 and w < 30 and h < 30:
                category_id = "12"  # Flat Head Machine Screw
            elif aspect_ratio < 0.8 and circularity < 0.6 and area < 5000:
                category_id = "13"  # Pan Head Sheet Metal Screw
            elif aspect_ratio > 0.5 and aspect_ratio < 0.8 and circularity < 0.7:
                category_id = "14"  # Self-Tapping Screw
            else:
                category_id = "3"  # Default to Wood Screw if no exact match

            # Retrieve screw details from JSON data
            info = self.category_info.get(
                category_id,
                {
                    "name": "Unknown",
                    "type": "Unknown",
                    "material": "Unknown",
                    "size": "Unknown",
                    "head_type": "Unknown",
                    "drive_type": "Unknown",
                    "thread_type": "Unknown",
                    "strength_grade": "Unknown",
                    "coating": "Unknown",
                    "application": "Unknown",
                    "description": "No description available."
                }
            )

            # Create detailed results
            details = (
                f"Detected Screw Information:\n"
                f"  - Name: {info['name']}\n"
                f"  - Type: {info['type']}\n"
                f"  - Material: {info['material']}\n"
                f"  - Size: {info['size']}\n"
                f"  - Head Type: {info['head_type']}\n"
                f"  - Drive Type: {info['drive_type']}\n"
                f"  - Thread Type: {info['thread_type']}\n"
                f"  - Strength Grade: {info['strength_grade']}\n"
                f"  - Coating: {info['coating']}\n"
                f"  - Application: {info['application']}\n"
                f"  - Description: {info['description']}\n"
                f"\nDetection Metrics:\n"
                f"  - Aspect Ratio: {aspect_ratio:.2f}\n"
                f"  - Circularity: {circularity:.2f}\n"
                f"  - Area: {area:.2f}\n"
                f"  - Bounding Box: Width={w}, Height={h}\n"
            )
            return details

        except Exception as e:
            return f"Error analyzing image: {e}"

    def analyze_video(self, file_path):
        """
        Analyze a video frame by frame and classify the screw.
        """
        try:
            cap = cv2.VideoCapture(file_path)
            if not cap.isOpened():
                return "Error: Cannot open video file."

            frame_count = 0
            analysis_results = []
            frame_interval = 10  # Analyze every 10th frame

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_count % frame_interval == 0:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray, 50, 150)
                    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    largest_contour = max(contours, key=cv2.contourArea) if contours else None
                    contour_area = cv2.contourArea(largest_contour) if largest_contour is not None else 0

                    if len(contours) > 50 and contour_area > 10000:
                        analysis_results.append("1")
                    elif len(contours) > 30 and contour_area > 5000:
                        analysis_results.append("2")
                    else:
                        analysis_results.append("3")

                frame_count += 1

            cap.release()

            if analysis_results:
                # Aggregate results
                most_common_category = max(set(analysis_results), key=analysis_results.count)
                info = self.category_info.get(
                    most_common_category,
                    {
                        "name": "Unknown",
                        "type": "Unknown",
                        "material": "Unknown",
                        "size": "Unknown",
                        "head_type": "Unknown",
                        "drive_type": "Unknown",
                        "thread_type": "Unknown",
                        "strength_grade": "Unknown",
                        "coating": "Unknown",
                        "application": "Unknown",
                        "description": "No description available."
                    }
                )

                details = (
                    f"Detected Screw Information:\n"
                    f"  - Name: {info['name']}\n"
                    f"  - Type: {info['type']}\n"
                    f"  - Material: {info['material']}\n"
                    f"  - Size: {info['size']}\n"
                    f"  - Head_type: {info['head_type']}\n"
                    f"  - Drive_type: {info['drive_type']}\n"
                    f"  - Thread_type: {info['thread_type']}\n"
                    f"  - Strength_grade: {info['strength_grade']}\n"
                    f"  - Coating: {info['coating']}\n"
                    f"  - Application: {info['application']}\n"
                    f"  - Description: {info['description']}"
                )
                return details
            else:
                return "No valid frames analyzed."

        except Exception as e:
            return f"Error analyzing video: {e}"


if __name__ == "__main__":
    ScrewDetectionApp().run()
