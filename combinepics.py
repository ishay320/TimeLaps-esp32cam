import numpy as np
import glob
from PIL import Image
import argparse

def show_images(input_folder,output_folder):
    print(input_folder + "/*.jpg")
    images = glob.glob(input_folder + "/*.jpg")
    counter = 0
    set_counter = 0
    img_array = []

    while(counter < len(images)):
        for _ in range(5):
            with open(images[counter], 'rb') as file:
                print(images[counter], "  percentage: ", "{:.3f}".format((counter / len(images)) * 100))
                pix = np.asarray(Image.open(file))
                img_array.append(pix)
            counter += 1
        combined = np.mean(img_array, axis=0)
        combined_normelized = combined.astype(np.uint8)
        Image.fromarray(combined_normelized).save(output_folder + "\\" + str(set_counter).zfill(6) + ".jpg")
        img_array = []
        set_counter += 1

def argument_handling():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True, type=str, help='Insert path to the folder of the files')
    parser.add_argument('-o', required=True, type=str, help='Insert location you want to save the files')
    args = parser.parse_args()
    return args.i, args.o


if __name__ == "__main__":
    input_folder, output_folder = argument_handling()
    show_images(input_folder,output_folder)
