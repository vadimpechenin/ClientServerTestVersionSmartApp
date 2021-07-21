"""
Реализация socket клиент, передача сообщения и картинки
"""
import os
import time
import socket

from common.socketHelper import SocketHelper

from message.messageStructure import MessageStructure
from message.messageResponceParameter import MessageResponceParameter


class MySocket:
    #HOST = '192.168.0.158'
    HOST = 'localhost'
    PORT = 54545
    BUFFER_LENGTH = 2048
    # Объект - ответ с сервера
    messageResponce = MessageResponceParameter()

    def __init__(self, host=HOST, port=PORT):

        self.sock = socket.socket()
        self.sock.connect((host, port))
        self.helper = SocketHelper(self.sock)
        self.messageResponce = MessageResponceParameter()

    def send_data(self,messageParameter):

        messageParameterAsBytes = MessageStructure.SaveToBytes(messageParameter)

        self.helper.writeInt(len(messageParameterAsBytes))
        print("Размер отсылаемого сообщения:", len(messageParameterAsBytes))

        self.helper.writeBytesArray(messageParameterAsBytes)
        print("Сообщение отправлено")
        #time.sleep(0.5)

    def get_data(self):

        sizeOfResponce = self.helper.readInt()
        print("Размер принимаемого сообщения: " + str(sizeOfResponce))
        messageResponcetAsBytes = self.helper.readBytesArray(sizeOfResponce)
        self.messageResponce = MessageStructure.RestoreFromBytes(messageResponcetAsBytes)

        print("Ответ получен")

        return self.messageResponce
        #time.sleep(0.5)


