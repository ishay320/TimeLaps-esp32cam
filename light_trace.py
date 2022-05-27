
from typing import List
import glob
import numpy as np
from PIL import Image
import argparse
import cv2
import concurrent.futures

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


def readImagesToList(names: List[str]) -> list:
    img_array = []
    for name in names:
        with open(name, "rb") as file:
            pix = np.asarray(Image.open(file))
            img_array.append(pix)
    return img_array

def batch_process(names: List[str]):
    if len(names) == 0:
        return None
    main_frame = np.asarray(np.array(Image.open(names[0])).shape[0:1])
    for i, image_name in enumerate(names):
        image = Image.open(image_name)
        thresh = image_to_light_threshold(image)
        main_frame = main_frame + thresh
        print(f"done: {i/len(names):.4f}\tdoing: {image_name}")
    # main_frame = main_frame / len(names)
    return main_frame

def process(input_folder, output_folder):
    print(input_folder + "/*.jpg")
    images_name = glob.glob(input_folder + "/*.jpg")
    f = open("test1.txt",'w')

    main_frame = np.asarray(np.array(Image.open(images_name[0])).shape[0:1])
    threads_num = 8
    with concurrent.futures.ThreadPoolExecutor(threads_num) as executor:
        list_part = len(images_name) / threads_num
        futures = [executor.submit(batch_process, images_name[int(i * list_part) : min(int((i + 1) * list_part), len(images_name))]) for i in range(threads_num)]   # submit return a "future result".
       
        for res in concurrent.futures.as_completed(futures):   # return each result as soon as it is completed:
            r = res.result()
            if r is None:
                continue
            print("thread done ")
            main_frame = main_frame + r

    # main_frame = np.asarray(np.array(Image.open(images_name[0])).shape[0:1])
    # for i, image_name in enumerate(images_name):
    #     image = Image.open(image_name)
    #     thresh = image_to_light_threshold(image)
    #     main_frame = main_frame + thresh
    #     print(f"done: {i/len(images_name)}\tdoing: {image_name}")
    # main_frame = main_frame / len(images_name)
    return main_frame

def image_to_light_threshold(image):
    (low_H, low_S, low_V) = 0,0,210
    (high_H, high_S, high_V) = 255,255,255
    frame_HSV = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2HSV)
    inRange = cv2.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
    return inRange

if __name__ == "__main__":
    folder_in, out_file = argument_handling()
    image = process(folder_in, out_file)
    # image = Image.open("D:/test1_fail/000035.jpg")

    # cv2.imshow("inrange", image_to_light_threshold(image))
    image = image.astype('float64')
    image /= image.max()/1
    cv2.imshow("normal", np.array(image))
    cv2.imwrite(f"{out_file}light.png", image *255)
    cv2.waitKey(0)