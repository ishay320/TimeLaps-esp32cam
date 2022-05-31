from ast import List
import numpy as np
from PIL import Image


def readImagesToList(names: List(str)) -> List:
    """
    load images from names to list
    and returns list of images
    """
    img_array = []
    for name in names:
        with open(name, "rb") as file:
            pix = np.asarray(Image.open(file))
            img_array.append(pix)
    return img_array
