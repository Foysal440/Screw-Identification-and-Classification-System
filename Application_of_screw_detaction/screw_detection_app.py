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

    def analyze_image(self, file_path):
        """
        Analyze an image and classify the screw.
        """
        try:
            img = PILImage.open(file_path)
            img_cv = np.array(img)
            gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, threshold1=50, threshold2=150)
            edge_count = np.sum(edges > 0)

            if edge_count > 10000:
                category_id = "1"
            elif edge_count > 5000:
                category_id = "2"
            else:
                category_id = "3"

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
            edge_counts = []
            frame_interval = 10

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_count % frame_interval == 0:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray, 50, 150)
                    edge_counts.append(np.sum(edges > 0))

                frame_count += 1

            cap.release()

            if edge_counts:
                avg_edge_count = np.mean(edge_counts)
                if avg_edge_count > 10000:
                    category_id = "1"
                elif avg_edge_count > 5000:
                    category_id = "2"
                else:
                    category_id = "3"

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
                return "No frames analyzed. Video might be empty or invalid."
        except Exception as e:
            return f"Error analyzing video: {e}"


if __name__ == "__main__":
    ScrewDetectionApp().run()
