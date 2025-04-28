import tkinter as tk
from tkinter import filedialog
from typing import Tuple, List
from PIL import Image, ImageOps

# Constants
A4_WIDTH: int = 2480  # A4 size in pixels at 300 DPI
A4_HEIGHT: int = 3508
IMG_WIDTH: int = int(63 * 11.811)  # Convert 63mm to pixels at 300 DPI
IMG_HEIGHT: int = int(88 * 11.811)  # Convert 88mm to pixels at 300 DPI
MARGIN: int = 10  # Margin between images


def select_files() -> Tuple[str, ...]:
    """Open a file dialog to select multiple image files."""
    return filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp")],
        multiple=True
    )


def select_save_path() -> str:
    """Open a save dialog to choose the output PNG file path."""
    return filedialog.asksaveasfilename(
        title="Save As",
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png")]
    )


def create_png(file_paths: Tuple[str, ...], save_path: str) -> None:
    """Create a PNG image arranged on an A4-sized canvas.

    Args:
        file_paths: Tuple of selected image file paths.
        save_path: Path where the resulting PNG should be saved.
    """
    if not file_paths:
        print('Caution: no images selected!')
        return

    if not save_path:
        print('Caution: no save path selected!')
        return

    x_offset: int = 0
    y_offset: int = 0

    # Create a blank A4-sized image (white background)
    a4_image: Image.Image = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")

    for file_path in file_paths:
        # Open image, convert to RGB, and resize it
        img: Image.Image = Image.open(file_path).convert("RGB")
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
    a4_image.save(save_path)
    print(f'Successfully saved to: {save_path}')


if __name__ == "__main__":
    root: tk.Tk = tk.Tk()
    root.withdraw()  # Hide the root window

    selected_files: Tuple[str, ...] = select_files()
    save_file_path: str = select_save_path()
    create_png(selected_files, save_file_path)

    print('Script finished running.')
