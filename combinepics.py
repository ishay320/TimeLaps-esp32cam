from typing import List
import numpy as np
import glob
from PIL import Image
import argparse
from multiprocessing import Pool
from tqdm import tqdm
from utils import readImagesToList


def meanImages(names: List[str], out_name: str):
    """
    do mean on the list of images and save it
    """
    img_array = readImagesToList(names)

    # Do the calculations
    combined = np.mean(img_array, axis=0)
    combined_normelized = combined.astype(np.uint8)

    # Save
    Image.fromarray(combined_normelized).save(out_name)


def addImages(names: List[str], out_name: str):
    """
    add all the images on the list and save it
    """
    img_array = readImagesToList(names)

    # Do the calculations
    combined = np.add(img_array, axis=0)
    combined_normelized = combined.astype(np.uint8)

    # Save
    Image.fromarray(combined_normelized).save(out_name)


def show_images(input_folder, output_folder, combine_num=5, processes=8):
    """
    process the folder photos
    """
    print(input_folder + "/*.jpg")
    images = glob.glob(input_folder + "/*.jpg")

    # cut the list for the pool
    counter = 0  # names for output
    set_counter = 0  # count the sets
    img_array = []  # Array of input name sized set
    tmp_arr = []  # set array
    out_names = []  # output names array
    for name in images:
        tmp_arr += [name]
        set_counter += 1

        if set_counter % combine_num == 0:
            out_names += [output_folder + "\\" + str(counter).zfill(6) + ".jpg"]
            counter += 1
            img_array += [tmp_arr]
            tmp_arr = []

    # Pool
    pool = Pool(processes=processes)
    jobs = [
        pool.apply_async(func=meanImages, args=(*argument,))
        if isinstance(argument, tuple)
        else pool.apply_async(func=meanImages, args=(argument,))
        for argument in zip(img_array, out_names)
    ]
    pool.close()
    result_list_tqdm = []
    for job in jobs:
        result_list_tqdm.append(job.get())


def argument_handling():
    """
    returns the argument of the user - input folder and output file
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", required=True, type=str, help="Insert path to the folder of the files"
    )
    parser.add_argument(
        "-o", required=True, type=str, help="Insert location you want to save the files"
    )
    args = parser.parse_args()
    return args.i, args.o


def main(input_folder = None, output_folder = None):
    if input_folder is None and output_folder is None:
        input_folder, output_folder = argument_handling()

    show_images(input_folder, output_folder)

if __name__ == "__main__":
    main()