"""
Реализация socket клиент, передача сообщения и картинки
"""
import os
import time
import socket

from common.socketHelper import SocketHelper

from message.messageStructure import MessageStructure


class MySocket:
    #HOST = '192.168.0.158'
    HOST = 'localhost'
    PORT = 54545
    BUFFER_LENGTH = 2048

    def __init__(self, host=HOST, port=PORT):

        self.sock = socket.socket()
        self.sock.connect((host, port))
        self.helper = SocketHelper(self.sock)

    def get_data(self,messageParameter):

        messageParameterAsBytes = MessageStructure.SaveToBytes(messageParameter)

        self.helper.writeInt(len(messageParameterAsBytes))
        print("Размер отсылаемого сообщения:", len(messageParameterAsBytes))

        self.helper.writeBytesArray(messageParameterAsBytes)
        print("Сообщение отправлено")
        #time.sleep(0.5)

