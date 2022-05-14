import multiprocessing
from typing import List
import numpy as np
import glob
from PIL import Image
import argparse
from multiprocessing import Pool


def readImagesToList(names: List[str]) -> list:
    img_array = []
    for name in names:
        with open(name, "rb") as file:
            pix = np.asarray(Image.open(file))
            img_array.append(pix)
    return img_array


def meanImages(names: List[str], out_name: str):
    img_array = readImagesToList(names)

    combined = np.mean(img_array, axis=0)
    combined_normelized = combined.astype(np.uint8)
    Image.fromarray(combined_normelized).save(out_name)


def addImages(names: List[str], out_name: str):
    img_array = readImagesToList(names)

    combined = np.add(img_array, axis=0)
    combined_normelized = combined.astype(np.uint8)
    Image.fromarray(combined_normelized).save(out_name)

    # pool = Pool()                         # Create a multiprocessing Pool
    # pool.map(process_image, data_inputs)  # process data_inputs iterable with pool


def show_images(input_folder, output_folder):
    print(input_folder + "/*.jpg")
    images = glob.glob(input_folder + "/*.jpg")

    # For pool
    counter = 0  # For output names
    set_counter = 0  # count the sets
    img_array = []  # Array of input name sized set
    tmp_arr = []  # set array
    out_names = []  # output names array
    for name in images:
        tmp_arr += [name]
        set_counter += 1

        if set_counter % 5 == 0:
            out_names += [output_folder + "\\" + str(counter).zfill(6) + ".jpg"]
            counter += 1
            img_array += [tmp_arr]
            tmp_arr = []
    for i in zip(out_names, img_array):
        print(i)

    ## TODO: add progress
    # Running the pool
    with multiprocessing.Pool(processes=8) as pool:
        results = pool.starmap(meanImages, zip(img_array, out_names))
    print(len(results))

    # while(counter < len(images)):
    #     for _ in range(5):
    #         with open(images[counter], 'rb') as file:
    #             print(images[counter], "  percentage: ", "{:.3f}".format((counter / len(images)) * 100))
    #             pix = np.asarray(Image.open(file))
    #             img_array.append(pix)
    #         counter += 1
    #     combined = np.mean(img_array, axis=0)
    #     combined_normelized = combined.astype(np.uint8)
    #     Image.fromarray(combined_normelized).save(output_folder + "\\" + str(set_counter).zfill(6) + ".jpg")
    #     img_array = []
    #     set_counter += 1


def argument_handling():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", required=True, type=str, help="Insert path to the folder of the files"
    )
    parser.add_argument(
        "-o", required=True, type=str, help="Insert location you want to save the files"
    )
    args = parser.parse_args()
    return args.i, args.o


if __name__ == "__main__":
    input_folder, output_folder = argument_handling()
    show_images(input_folder, output_folder)
