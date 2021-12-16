import cv2
import os


def create_directory(directory):
    directory_name = directory.rstrip('.mp4')
    try:
        os.mkdir(directory_name)
        print(f"created directory: {directory_name}")
    except FileExistsError:
        pass
    return directory_name


def video_converter(video_file: str):
    directory = create_directory(video_file)
    video = cv2.VideoCapture(video_file)
    success, image = video.read()
    count = 1
    while success:
        cv2.imwrite(f"{directory}/image_%d.jpg" % count, image)
        success, image = video.read()
        print('Saved image ', count)
        count += 1


if __name__ == '__main__':
    filename = 'video_2021-12-13_14-42-59.mp4'
    # create_directory(filename)
    video_converter(filename)
