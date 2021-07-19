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


    def get_data(self,filename,server_code):

        # считывает и отправляет картинку
        #file = open('image.jpg', mode="rb")  # считываем картинку
        self.sock.send(str(server_code).encode())
        time.sleep(0.5)

        for i in server_code:
            code_request1 = int(i)

        print(code_request1)

        if (code_request1==0):
           self.send_image(filename)
        else:
            for file in filename:
                self.send_image(file)

    def send_image(self,filename):
        file = open(filename, mode="rb")

        # imageSize = os.path.getsize('image.jpg')
        imageSize = os.path.getsize(filename)
        print("Размер отсылаемого изображения:", imageSize)

        self.sock.send(str(imageSize).encode())
        time.sleep(0.5)

        while imageSize > 0:
            data = file.read(2048)
            self.sock.send(data)
            imageSize = imageSize - 2048

        print("Image was sent")
        file.close()
