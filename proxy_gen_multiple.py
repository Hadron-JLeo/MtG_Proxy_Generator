import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageOps
from math import ceil

A4_WIDTH, A4_HEIGHT = 2480, 3508
IMG_WIDTH, IMG_HEIGHT = int(63 * 11.811), int(88 * 11.811)

def calc_page_amt(imgs:list):
    img_amt:int = len(imgs)
    print(img_amt)
    page_amt: int = ceil(img_amt/9)

    return page_amt
# END of function definition dcalc_page_amt(list)

# Function to select images and create a PNG
def create_png(imgs:list=[], filename:str='output.png'):

    x_offset, y_offset = 0, 0
    margin = 20  # Margin between images

    # Create a blank A4-sized image (white background)
    a4_image = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")

    for file_path in imgs:
        # Open image, convert to RGB, and resize it (PIL supports webp natively)
        img = Image.open(file_path).convert("RGB")
        img = ImageOps.fit(img, (IMG_WIDTH, IMG_HEIGHT))
        
        # Paste the image onto the A4 canvas at the current position
        a4_image.paste(img, (x_offset, y_offset))

        # Update position for next image
        x_offset += IMG_WIDTH + margin
        if x_offset + IMG_WIDTH > A4_WIDTH:
            x_offset = 0
            y_offset += IMG_HEIGHT + margin
            if y_offset + IMG_HEIGHT > A4_HEIGHT:
                break  # Stop if no space left on the canvas

    # Save the final A4-sized PNG
    a4_image.save(filename)

# ---- END of function definition create_png(void) ---- #

def get_images():
    file_paths = filedialog.askopenfilenames(
        title="Select Images", 
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp")],
        multiple=True  # Allow selecting multiple images at once
    )

    if not file_paths:
        # exit
        print('Caution; no images selected!')
        return

    return file_paths
# ---- END of function definition get_images(void) ---- #


def create_pages(imgs:list):
    
    img_counter:int = 0

    for i in range(calc_page_amt(imgs)):
        print(f'creating page {i}')

        create_png(imgs[img_counter:img_counter+9], f'output_{img_counter}.png')

        print(f'Page {i} contains: {imgs}', end='/n')
        img_counter+=9

# ---- END of function definition create_pages(list) ---- #

def main():
    root = tk.Tk()
    my_imgs:list = get_images()
    root.withdraw()  # Hide the root window

    # create_png()
    create_pages(my_imgs)

    print('Script Done running')
# ---- END of function definition main(void) ---- #


if __name__ == '__main__':
    main()
