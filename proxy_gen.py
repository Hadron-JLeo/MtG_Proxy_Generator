import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageOps

# Constants
A4_WIDTH, A4_HEIGHT = 2480, 3508  # A4 size in pixels at 300 DPI
IMG_WIDTH = int(63 * 11.811)      # Convert 63mm to pixels at 300 DPI
IMG_HEIGHT = int(88 * 11.811)     # Convert 88mm to pixels at 300 DPI
MARGIN = 10                       # Margin between images


def select_files():
    """Open a file dialog to select multiple image files."""
    return filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp")],
        multiple=True
    )


def create_png(file_paths):
    """Create a PNG image arranged on an A4-sized canvas."""
    if not file_paths:
        print('Caution: no images selected!')
        return

    x_offset, y_offset = 0, 0

    # Create a blank A4-sized image (white background)
    a4_image = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")

    for file_path in file_paths:
        # Open image, convert to RGB, and resize it
        img = Image.open(file_path).convert("RGB")
        img = ImageOps.fit(img, (IMG_WIDTH, IMG_HEIGHT))

        # Paste the image onto the A4 canvas at the current position
        a4_image.paste(img, (x_offset, y_offset))

        # Update position for next image
        x_offset += IMG_WIDTH + MARGIN
        if x_offset + IMG_WIDTH > A4_WIDTH:
            x_offset = 0
            y_offset += IMG_HEIGHT + MARGIN
            if y_offset + IMG_HEIGHT > A4_HEIGHT:
                break  # Stop if no space left on the canvas

    # Save the final A4-sized PNG
    a4_image.save("output.png")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    selected_files = select_files()
    create_png(selected_files)
    print('Script finished running.')
