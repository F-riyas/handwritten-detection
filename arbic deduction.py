import tkinter as tk
from tkinter import filedialog, Text, Scrollbar, Checkbutton, IntVar
import easyocr
import cv2
from PIL import Image, ImageTk

# Initialize the OCR reader for Arabic
reader = easyocr.Reader(['ar'])

def preprocess_image(image_cv):
    # Convert to grayscale
    gray = cv2.cvtColor(image_cv, cv2.COLOR_RGB2GRAY)
    # Apply Gaussian Blur
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    # Adaptive Thresholding
    thresh = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    return cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)  # convert back to RGB for easyocr

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if file_path:
        # Load image
        image_cv = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_cv)
        image_pil.thumbnail((400, 400))

        # Show image in the GUI
        photo = ImageTk.PhotoImage(image_pil)
        image_label.config(image=photo)
        image_label.image = photo

        # Check if enhancement is selected
        if enhance_var.get() == 1:
            processed_image = preprocess_image(image_cv)
            result = reader.readtext(processed_image, detail=1)
        else:
            result = reader.readtext(image_cv, detail=1)

        # Display OCR results
        text_output.delete(1.0, tk.END)
        for detection in result:
            text_output.insert(tk.END, detection[1] + '\n')

# Build the GUI
root = tk.Tk()
root.title("Arabic Handwritten Text Detector")

# Image display area
image_label = tk.Label(root)
image_label.pack(pady=10)

# Enhance image option
enhance_var = IntVar()
enhance_checkbox = Checkbutton(root, text="Enhance Image for Handwriting", variable=enhance_var)
enhance_checkbox.pack()

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
