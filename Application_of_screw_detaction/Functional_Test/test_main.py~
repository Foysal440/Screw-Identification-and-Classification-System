import cv2
import numpy as np
import json
from PIL import Image
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES

# Load category information from JSON
try:
    with open("screw_data.json", "r") as f:
        category_info = json.load(f)
except FileNotFoundError:
    print("Error: 'screw_data.json' file not found. Ensure it's in the same directory as the script.")
    category_info = {}


def analyze_screw_image(image):
    """
    Analyze an image using basic feature detection (edge detection).
    """
    img_cv = np.array(image)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, threshold1=50, threshold2=150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_count = len(contours)
    if contour_count > 50:
        return 9  # Torx Screw
    elif contour_count > 20:
        return 10  # Phillips Screw
    else:
        return 1  # Long Lag Screw (default)


def analyze_video(file_path):
    """
    Analyze a video frame by frame and classify the screw type.
    """
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        print(f"Error: Unable to open video file {file_path}")
        return

    frame_interval = 10  # Analyze every 10th frame
    frame_count = 0
    predictions = []

    print("Analyzing video frames...")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            # Convert the frame to PIL Image format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_image = Image.fromarray(frame_rgb)

            # Analyze the frame and collect predictions
            prediction = analyze_screw_image(frame_image)
            predictions.append(prediction)

        frame_count += 1

    cap.release()

    if predictions:
        # Use majority voting to determine the screw type
        final_prediction = max(set(predictions), key=predictions.count)
        print("Video Analysis Result:")
        info = category_info.get(str(final_prediction), {"name": "Unknown", "type": "Unknown", "description": "No description available."})
        for key, value in info.items():
            print(f"  - {key.capitalize()}: {value}")
    else:
        print("No frames analyzed. Video may be empty or invalid.")


def analyze_file(file_path):
    """
    Analyze an image or video file and display screw information.
    """
    if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
        try:
            img = Image.open(file_path)
            plt.imshow(img)
            plt.axis('off')
            plt.show()
            category_id = analyze_screw_image(img)
        except Exception as e:
            print(f"Error analyzing image: {e}")
            return
    elif file_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
        analyze_video(file_path)
        return
    else:
        print("Unsupported file format! Please provide a valid image or video file.")
        return

    info = category_info.get(str(category_id), {"name": "Unknown", "type": "Unknown", "description": "No description available."})
    print("Detected Screw Information:")
    for key, value in info.items():
        print(f"  - {key.capitalize()}: {value}")


def select_file_gui():
    """
    Open a file dialog to select an image or video file.
    """
    print("Opening file dialog...")
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select an Image or Video File",
        filetypes=[("Image and Video Files", "*.jpg *.jpeg *.png *.bmp *.tiff *.mp4 *.avi *.mkv *.mov")]
    )
    root.destroy()
    return file_path


def gui_upload_screen():
    """
    Create a GUI for uploading an image or video file.
    """
    def open_file_dialog():
        file_path = filedialog.askopenfilename(
            title="Select an Image or Video File",
            filetypes=[("Image and Video Files", "*.jpg *.jpeg *.png *.bmp *.tiff *.mp4 *.avi *.mkv *.mov")]
        )
        if file_path:
            print(f"File selected: {file_path}")
            analyze_file(file_path)

    def on_drop(event):
        file_path = event.data.strip()
        print(f"File dragged: {file_path}")
        analyze_file(file_path)

    root = TkinterDnD.Tk()  # Use TkinterDnD for drag-and-drop support
    root.title("Upload File")
    root.geometry("400x200")

    label = Label(root, text="Drag & Drop a File Here or Click Upload", font=("Helvetica", 12))
    label.pack(pady=20)

    upload_button = Button(root, text="Upload File", command=open_file_dialog, font=("Helvetica", 10))
    upload_button.pack(pady=10)

    # Add drag-and-drop functionality
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', on_drop)

    root.mainloop()


if __name__ == "__main__":
    print("How would you like to provide the file?")
    print("1: Enter the file path manually.")
    print("2: Use the GUI to upload or drag-and-drop a file.")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        file_path = input("Enter the full path to the image or video file: ").strip()
        if file_path:
            print(f"File path entered: {file_path}")
            analyze_file(file_path)
        else:
            print("No path provided. Exiting...")
    elif choice == "2":
        print("Launching GUI...")
        gui_upload_screen()
    else:
        print("Invalid choice. Exiting...")
