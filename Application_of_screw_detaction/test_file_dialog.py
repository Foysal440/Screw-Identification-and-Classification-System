from tkinter import Tk, filedialog

def select_file_gui():
    print("Opening file dialog...")
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    root.destroy()  # Close the root window
    if file_path:
        print(f"File selected: {file_path}")
    else:
        print("No file selected.")

if __name__ == "__main__":
    select_file_gui()
