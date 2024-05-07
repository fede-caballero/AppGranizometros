import cv2
import numpy as np
import os

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

"""
# Path to your input image
input_image_path = '/home/fede-caballero/Granizometros/a-analizar/190331-S27-OS-CAL.jpg'

# Process the image
output_image = process_image(input_image_path)

# Create a directory to save the result if it doesn't exist
output_directory = 'output_images'
os.makedirs(output_directory, exist_ok=True)

# Save the resulting image to the output directory
output_image_path = os.path.join(output_directory, '190331-S27-OS-CAL.jpg')
cv2.imwrite(output_image_path, output_image)

print("Result image saved at:", output_image_path)"""
