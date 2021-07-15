"""
Реализация socket клиент, передача сообщения и картинки
"""
import os
import time
import socket


class MySocket:
    #HOST = '192.168.0.158'
    HOST = 'localhost'
    PORT = 54545
    def __init__(self, host=HOST, port=PORT):

        self.sock = socket.socket()
        self.sock.connect((host, port))


    def get_data(self):

        # считывает и отправляет картинку
        file = open('image.jpg', mode="rb")  # считываем картинку

        imageSize = os.path.getsize('image.jpg')
        print("Size of image:", imageSize)
        self.sock.send(str(imageSize).encode())
        time.sleep(0.1)

        while imageSize > 0:
            data = file.read(2048)
            self.sock.send(data)
            imageSize = imageSize - 2048

        print("Image was sent")
        file.close()