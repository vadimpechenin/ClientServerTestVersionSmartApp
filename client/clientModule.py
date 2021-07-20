"""
Реализация socket клиент, передача сообщения и картинки
"""
import os
import time
import socket

from common.socketHelper import SocketHelper



class MySocket:
    #HOST = '192.168.0.158'
    HOST = 'localhost'
    PORT = 54545
    BUFFER_LENGTH = 2048

    def __init__(self, host=HOST, port=PORT):

        self.sock = socket.socket()
        self.sock.connect((host, port))
        self.helper = SocketHelper(self.sock)

    def get_data(self,filename,code_request0, code_request1):

        # считывает и отправляет картинку
        #file = open('image.jpg', mode="rb")  # считываем картинку
        # Превратить информацию о размере изображения в байты и задать определенную длину байт


        self.helper.writeInt(code_request0)
        self.helper.writeInt(code_request1)
        #time.sleep(0.5)

        #print(code_request0)
        #print(code_request1)

        if (code_request0>0) and(code_request0<3):
            #Если есть коды для отправки картинок (запрос названия или сохранение в базу), то отправляем картинки
            if (code_request1==0):
               self.send_image(filename)
            else:
                for file in filename:
                    self.send_image(file)

    def send_image(self, filename):

        file = open(filename, mode="rb")

        sizeOfImage = os.path.getsize(filename)

        print("Размер отсылаемого изображения:", sizeOfImage)

        self.helper.writeInt(sizeOfImage)

        while sizeOfImage > 0:
            partSize = min(sizeOfImage, self.BUFFER_LENGTH)
            data = file.read(partSize)
            self.helper.writeBytesArray(data)
            sizeOfImage = sizeOfImage - partSize

        print("Изображение отправлено")
        file.close()
