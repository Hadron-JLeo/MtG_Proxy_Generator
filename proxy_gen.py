import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageOps, ImageDraw

# Function to select images and create a PNG
def create_png():
    # Select multiple images at once through file dialog (include .webp files)
    file_paths = filedialog.askopenfilenames(
        title="Select Images", 
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp")],
        multiple=True  # Allow selecting multiple images at once
    )
    
    # If no images selected, exit
    if not file_paths:
        print('Caution; no images selected!')
        return

    # A4 size in pixels at 300 DPI: 2480 x 3508
    a4_width, a4_height = 2480, 3508
    img_width, img_height = int(63 * 11.811), int(88 * 11.811)  # Convert 63x88mm to pixels at 300 DPI
    x_offset, y_offset = 0, 0
    margin = 10  # Margin between images

    # Create a blank A4-sized image (white background)
    a4_image = Image.new("RGB", (a4_width, a4_height), "white")
    draw = ImageDraw.Draw(a4_image)

    for file_path in file_paths:
        # Open image, convert to RGB, and resize it (PIL supports webp natively)
        img = Image.open(file_path).convert("RGB")
        img = ImageOps.fit(img, (img_width, img_height))
        
        # Paste the image onto the A4 canvas at the current position
        a4_image.paste(img, (x_offset, y_offset))

        # Update position for next image
        x_offset += img_width + margin
        if x_offset + img_width > a4_width:
            x_offset = 0
            y_offset += img_height + margin
            if y_offset + img_height > a4_height:
                break  # Stop if no space left on the canvas

    # Save the final A4-sized PNG
    a4_image.save("output.png")
    # print("PNG created successfully.")

# GUI to trigger image selection and PNG creation
root = tk.Tk()
root.withdraw()  # Hide the root window
create_png()
print('Script Done running')
