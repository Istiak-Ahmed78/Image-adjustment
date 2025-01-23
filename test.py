from PIL import Image

# Open the base and overlay images
base_img = Image.open('test_image_directory/original_image.png').convert('RGBA')
combined = Image.open('test_image_directory/White screen.png').convert('RGBA')
overlay_img = Image.open('test_image_directory/Frammed_image.png').convert('RGBA')
import os

# combined.paste(overlay_img, position, overlay_img)
# Convert the overlay image to RGBA mode

# base_img = base_img.resize(overlay_img.size, Image.Resampling.LANCZOS)

# Define the position where the overlay image will be pasted
position = (1000, 50)

# Overlay the image over base image
combined.paste(base_img, position, base_img)
# combined.paste(overlay_img, (0, 0), overlay_img)
file_path = 'overlayed_image.png'

# Check if the file exists before deleting
if os.path.exists(file_path):
    os.remove(file_path)
    print(f"{file_path} has been deleted.")
else:
    print(f"{file_path} does not exist.")
# Save the resulting image
combined.save(file_path,'PNG')