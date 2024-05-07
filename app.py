import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import os
import numpy as np

# Author information
AUTHOR_NAME = "FRC"

def browse_image():
    global image_path
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*"), ("Image Files", "*.jpg *.jpeg *.png")])
    print(f"Selected file: {file_path}")  # Debug line
    if file_path:
        try:
            img = Image.open(file_path)
            img.thumbnail((600, 600))
            photo = ImageTk.PhotoImage(img)
            canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            canvas.image = photo
            
            # Update the image_path variable
            image_path = file_path
            
            process_button.config(state=tk.NORMAL)
        except Exception as e:
            print(f"Error loading image: {e}")  # Debug line

def process_image(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to HSV color space
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for red color in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Create a mask to identify red pixels
    mask_red = cv2.inRange(hsv_img, lower_red, upper_red)

    # Set non-red pixels to white
    img[mask_red == 0] = [255, 255, 255]

    # Set red pixels to black
    img[mask_red != 0] = [0, 0, 0]

    # Set non-black pixels to white
    img[np.where((img != [0, 0, 0]).all(axis=-1))] = [255, 255, 255]

    return img


def process_and_save_image():
    if image_path:
        output_image = process_image(image_path)
        output_directory = 'Analizadas'
        os.makedirs(output_directory, exist_ok=True)
        output_file_name = os.path.basename(image_path)
        output_image_path = os.path.join(output_directory, output_file_name)
        cv2.imwrite(output_image_path, output_image)
        print("Imagen guardada en: ", output_image_path)
        
        # Show confirmation message
        messagebox.showinfo("Imagen guardada correctamente", f"La imagen fue grardada en: \n{output_image_path}")

def add_new_image():
    browse_image()

def exit_application():
    root.quit()

# Create the main window
root = tk.Tk()
root.title("Analizador de Granizometros")

# Author label
author_label = tk.Label(root, text=f"Created by {AUTHOR_NAME}")
author_label.pack(pady=10)

# Create a canvas to display the image
canvas = tk.Canvas(root, width=600, height=600)
canvas.pack()

# Create buttons
browse_button = tk.Button(root, text="Buscar Imagen", command=browse_image, border=5, relief="raised", bg="blue", fg="white")
browse_button.pack(pady=10)

process_button = tk.Button(root, text="Procesar Imagen", command=process_and_save_image, state=tk.DISABLED, border=5, relief="raised", bg="green", fg="white")
process_button.pack(pady=5)

new_image_button = tk.Button(root, text="Nueva Imagen", command=add_new_image, border=5, relief="raised", bg="blue", fg="white")
new_image_button.pack(pady=5)

exit_button = tk.Button(root, text="Salir", command=exit_application, border=5, relief="raised", bg="red", fg="white")
exit_button.pack(pady=5)

# Initialize variables
image_path = None

# Run the application
root.mainloop()
