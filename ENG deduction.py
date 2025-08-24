import tkinter as tk
from tkinter import filedialog, Text, Scrollbar
import easyocr
import cv2
from PIL import Image, ImageTk

# Initialize the OCR reader
reader = easyocr.Reader(['en'])

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if file_path:
        # Load image
        image = cv2.imread(file_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image.thumbnail((400, 400))

        # Show image in the GUI
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo

        # Perform OCR
        result = reader.readtext(file_path)
        text_output.delete(1.0, tk.END)

        for detection in result:
            text_output.insert(tk.END, detection[1] + '\n')

# Build the GUI
root = tk.Tk()
root.title("Handwritten Text Detector")

# Image display area
image_label = tk.Label(root)
image_label.pack(pady=10)

# Button to open image
button = tk.Button(root, text="Open Image", command=open_image)
button.pack(pady=5)

# Scrollable text box
scrollbar = Scrollbar(root)
text_output = Text(root, height=10, width=50, yscrollcommand=scrollbar.set)
scrollbar.config(command=text_output.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Start the GUI loop
root.mainloop()
