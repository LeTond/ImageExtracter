import threading
import queue
import os
from multiprocessing import Queue

from PIL import Image, ImageChops


class DiffImage(threading.Thread):  # класс по сравнению картинок.
    """Потоковый обработчик"""

    def __init__(self, queue):
        """Инициализация потока"""
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        """Запуск потока"""
        while True:
            # Получаем пару путей из очереди
            files = self.queue.get()
            # Делим и сравниваем
            self.comparing(files.split(':')[0], files.split(':')[1])
            # Отправляем сигнал о том, что задача завершена
            self.queue.task_done()

    ## TODO: Доработать через субстракцию по порогу
    @staticmethod
    def comparing(img1, img2):
        image_1 = Image.open(img1)
        image_2 = Image.open(img2)
        result = ImageChops.difference(image_1, image_2)
        # if result is None:
        #     print(img1, img2, 'matches')
        count = 0
        for i in result.histogram():
            if i == 0:
                count += 1
        if count > 420:
            os.remove(img2)
            # slice_number -= 1
            # length -= 1
        # else:
            # slice_number -= 1
            # length -= 1

        return


def main(path):
    imgs = os.listdir(path)  # Получаем список картинок
    q = queue.Queue()

    # Запускаем поток и очередь
    for i in range(8):  # 4 - кол-во одновременных потоков
        t = DiffImage(q)
        t.setDaemon(True)
        t.start()

        # Даем очереди нужные пары файлов для проверки
    check_file = 0
    current_file = 0

    while check_file < len(imgs):
        if current_file == check_file:
            current_file += 1
            continue
        print(current_file, check_file)
        q.put(path + imgs[current_file] + ':' + path + imgs[check_file])
        current_file += 1
        if current_file == len(imgs):
            check_file += 1
            current_file = check_file

            # Ждем завершения работы очереди
    q.join()


if __name__ == "__main__":
    path = 'video_2021-12-13_14-42-59/'
    main(path)
