import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from typing import List
from PIL import Image, ImageOps
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Constants
DPI: int = 300
MM_TO_INCH: float = 0.0393701

A4_WIDTH: int = int(210 * MM_TO_INCH * DPI)  # 210mm width
A4_HEIGHT: int = int(297 * MM_TO_INCH * DPI)  # 297mm height

IMG_WIDTH: int = int(63 * MM_TO_INCH * DPI)  # Card width in mm
IMG_HEIGHT: int = int(88 * MM_TO_INCH * DPI)  # Card height in mm

MARGIN: int = 10  # Margin between images in pixels


def select_files() -> List[Path]:
    """Open a file dialog to select multiple image files."""
    file_paths = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp")],
        multiple=True
    )
    return [Path(path) for path in file_paths]


def select_save_path() -> Path:
    """Open a save dialog to choose the output PNG file path."""
    save_path = filedialog.asksaveasfilename(
        title="Save As",
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png")]
    )
    return Path(save_path) if save_path else None


def create_png(file_paths: List[Path], save_path: Path) -> None:
    """Create a PNG image arranged on an A4-sized canvas.

    Args:
        file_paths: List of selected image file paths.
        save_path: Path where the resulting PNG should be saved.
    """
    if not file_paths:
        logging.warning('No images selected. Aborting.')
        return

    if save_path is None:
        logging.warning('No save path selected. Aborting.')
        return

    x_offset: int = 0
    y_offset: int = 0

    # Create a blank A4-sized image (white background)
    a4_image: Image.Image = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")

    for file_path in file_paths:
        try:
            img: Image.Image = Image.open(file_path).convert("RGB")
        except Exception as e:
            logging.error(f"Failed to open image {file_path}: {e}")
            continue

        img = ImageOps.fit(img, (IMG_WIDTH, IMG_HEIGHT))

        # Paste the image onto the A4 canvas at the current position
        a4_image.paste(img, (x_offset, y_offset))

        # Update position for next image
        x_offset += IMG_WIDTH + MARGIN
        if x_offset + IMG_WIDTH > A4_WIDTH:
            x_offset = 0
            y_offset += IMG_HEIGHT + MARGIN
            if y_offset + IMG_HEIGHT > A4_HEIGHT:
                logging.info('No more space on A4 page. Stopping image placement.')
                break  # Stop if no space left

    # Save the final A4-sized PNG
    try:
        a4_image.save(save_path)
        logging.info(f'Successfully saved to: {save_path}')
    except Exception as e:
        logging.error(f"Failed to save image: {e}")


if __name__ == "__main__":
    root: tk.Tk = tk.Tk()
    root.withdraw()  # Hide the root window

    selected_files: List[Path] = select_files()
    save_file_path: Path = select_save_path()
    create_png(selected_files, save_file_path)

    logging.info('Script finished running.')
