from typing import List
import glob
import numpy as np
from PIL import Image
import argparse
import cv2


def argument_handling():
    """
    returns the argument of the user - input folder and output file
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", required=True, type=str, help="Insert path to the folder of the files"
    )
    parser.add_argument(
        "-o", required=True, type=str, help="Insert the path you want to save the file"
    )
    args = parser.parse_args()
    return args.i, args.o


def batch_process(names: List[str]) -> List:
    """
    gets list of names and process them
    returns the processed image
    """
    # Check if empty
    if len(names) == 0:
        return None

    # Start the main array with first file size
    main_frame = np.asarray(np.array(Image.open(names[0])).shape[0:1])

    # Load all images
    for i, image_name in enumerate(names):
        image = Image.open(image_name)
        thresh = image_to_light_threshold(image)
        main_frame = main_frame + thresh
        # print(f"done: {(i/len(names))*100:.4f}\tdoing: {image_name}")

    return main_frame


def process_multi(input_folder: str):
    """
    process the folder photos and output processed frame
    """
    print(input_folder + "/*.jpg")
    images_name = glob.glob(input_folder + "/*.jpg")

    # Get size of images for main array
    main_frame = np.asarray(np.array(Image.open(images_name[0])).shape[0:1])

    # run on the files and process
    for i, image_name in enumerate(images_name):
        image = Image.open(image_name)
        thresh = image_to_light_threshold(image)
        main_frame = main_frame + thresh
        # print(f"done: {i/len(images_name)}\tdoing: {image_name}")

    # Normalize
    main_frame = main_frame / len(images_name)
    return main_frame


def image_to_light_threshold(image) -> cv2.Mat:
    """
    gets image and output image of where the sun light is
    """
    # Convert image to HSV
    frame_HSV = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2HSV)

    # Get only the lightest part of image
    (low_H, low_S, low_V) = 0, 0, 210
    (high_H, high_S, high_V) = 255, 255, 255
    inRange = cv2.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
    return inRange

def main(input_folder = None, output_folder = None, show = True):
    if input_folder is None and output_folder is None:
        input_folder, output_folder = argument_handling()
    image = process_multi(input_folder)

    # Process image for output
    image = image.astype("float64")
    # Normalization
    image /= image.max() / 1

    cv2.imwrite(f"{output_folder}/light.png", image * 255)
    if show:
        cv2.imshow("normal", np.array(image))
        cv2.waitKey(0)

if __name__ == "__main__":
    main()
