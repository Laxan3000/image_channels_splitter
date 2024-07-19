import numpy as np
from PIL import Image
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
from typing import Optional


DEFAULT_SAVE_MODE: str = "L" # Grayscale
FILE_TYPE: list[tuple[str, str]] = [("PNG image", f"*.png")]
DEFAULT_EXTENSION: str = "png"
GRAYSCALE_ERROR: str = "Image must be grayscale!"


def get_file(title: str) -> str:
    return askopenfilename(
        defaultextension= DEFAULT_EXTENSION,
        filetypes= FILE_TYPE,
        title= title
    )


def get_compression() -> int:
    while True:
        compression: str = input(
            "Please select a compression level (0-9) [6]: "
        ) or '6'

        if '0' <= compression[0] <= '9':
            return int(compression)


def separate_channels() -> bool:
    if not (file_name := get_file("Please select the image to convert")):
        return False

    with Image.open(file_name) as image:
        image_mode: str = image.mode
 
        if not image_mode.startswith("RGB"):
            print("The image mode used for this image is not supported!")
            return False

        save_folder: str = askdirectory(title= "Where would you like to save all the channels?")
        compress_level: int = get_compression()
        array: np.ndarray = np.array(image)

        # Save the red channel
        Image.fromarray(
            array[:, :, 0],
            mode= DEFAULT_SAVE_MODE
        ).save(
            save_folder + "/red.png",
            DEFAULT_EXTENSION,
            compress_level= compress_level
        )

        # Save the green channel
        Image.fromarray(
            array[:, :, 1],
            mode= DEFAULT_SAVE_MODE
        ).save(
            save_folder + "/green.png",
            DEFAULT_EXTENSION,
            compress_level= compress_level
        )

        # Save the blue channel
        Image.fromarray(
            array[:, :, 2],
            mode= DEFAULT_SAVE_MODE
        ).save(
            save_folder + "/blue.png",
            DEFAULT_EXTENSION,
            compress_level= compress_level
        )

        # Save the alpha channel if it exists
        if image_mode[-1] == "A":
            Image.fromarray(
                array[:, :, 3],
                mode= DEFAULT_SAVE_MODE
            ).save(
                save_folder + "/alpha.png",
                DEFAULT_EXTENSION,
                compress_level= compress_level
            )

    return True


def get_channel(channel: str) -> Optional[Image.Image]:
    while True:
        if not (red_file := get_file(f"Please select the {channel} channel")):
            return None

        if (red_image := Image.open(red_file)).mode == DEFAULT_SAVE_MODE:
            break

        print(GRAYSCALE_ERROR)

    return red_image


def merge_channels() -> bool:
    # Open each image or return if the user cancelled any of the operations
    if not (red_image := get_channel("RED")) \
    or not (green_image := get_channel("GREEN")) \
    or not (blue_image := get_channel("BLUE")):
        return False

    # Ask if the image has an alpha channel, otherwise its variable is set to False
    alpha_file = False
    if input("Is there an ALPHA channel? [Y/n]: ").casefold() == "y" \
    and not (alpha_file := get_channel("ALPHA")):
        return False

    mode: str = "RGB"

    sequence: list[np.ndarray] = [
        np.array(red_image),
        np.array(green_image),
        np.array(blue_image)
    ]

    # Close the images previously opened
    red_image.close()
    green_image.close()
    blue_image.close()

    if alpha_file:
        mode += "A"
        sequence.append(np.array(alpha_file))
        alpha_file.close()

    Image.fromarray(
        np.dstack(sequence),
        mode= mode
    ).save(
        asksaveasfilename(
            defaultextension= DEFAULT_EXTENSION,
            filetypes= FILE_TYPE,
            title= "How would you like to save the file?"
        ),
        DEFAULT_EXTENSION,
        compress_level= get_compression()
    )
    
    return True


# Returns True if the program has to be executed again
# Otherwise it returns False
def main() -> bool:
    print(
        "What would you like to do?:",
        "a - Separate channels from image",
        "b - Merge channels into an image",
        "c - Close the program",
        sep="\n",
    )

    success: bool = bool()
    match (input("Select your answer: ") or ' ')[0]:
        case 'a':
            success = separate_channels()

        case 'b':
            success = merge_channels()
            
        case 'c':
            return False

        case _:
            return True

    print(
        "Conversion done! Bye :)"
        if success else
        "Operation canceled"
    )

    input("-- Press any key to re-run the program --")

    return True


if __name__ == "__main__":
    print("Welcome to this amazing program!")
    while main(): print()
