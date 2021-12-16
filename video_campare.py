import os
from PIL import Image, ImageChops
from pprint import pprint
import natsort


def read_directory(path):
    list_ = os.listdir(path)
    return list_


def compare_images(list_files, path):
    length = len(list_files) - 1
    slice_number = length - 1
    while slice_number != -1:
        image_1 = Image.open(f'{path}/{list_files[slice_number]}')
        image_2 = Image.open(f'{path}/{list_files[length]}')
        result = ImageChops.difference(image_1, image_2)

        count = 0
        for i in result.histogram():
            if i == 0:
                count += 1
        if count > 420:
            os.remove(f'{path}/{list_files[length]}')
            slice_number -= 1
            length -= 1
        else:
            slice_number -= 1
            length -= 1


if __name__ == '__main__':
    inList = natsort.natsorted(read_directory('video_2021-12-13_14-42-59'))
    compare_images(inList, 'video_2021-12-13_14-42-59')
