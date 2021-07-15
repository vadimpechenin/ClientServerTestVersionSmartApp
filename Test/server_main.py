"""
Серверная часть проекта УМНИК 2021 "Умный склад"
версия 1
Реализация с сокетами
"""
import cv2
import os
import numpy as np

#Переменные для начальной инициализации базы данных
number_of_image = 7
#Классы для работы приложения
from Handlers.Server_class import MainCommandHandler as ServerSmartApp
from Handlers.CheckIn.CheckInCommandHandlerParameter import CheckInCommandHandlerParameter
from Handlers.NomRequest.NomRequestCommandHandlerParameter import NomRequestCommandHandlerParameter
from Handlers.PartIdentification.PartIdentificationCommandHandlerParameter import PartIdentificationCommandHandlerParameter

serversmartapp = ServerSmartApp()

import socket
import time

serversocket = socket.socket()

host = 'localhost'
#host = '192.168.0.158'
port = 54545

serversocket.bind((host, port))

serversocket.listen(1)
print("Server is listening", '\n')

clientsocket,addr = serversocket.accept()

print("got a connection from %s" % str(addr))

# Имитатор основного цикла
while True:
    try:
        data = clientsocket.recv(2048)
        time.sleep(0.5)
        
        parameters = None
        operation_type = None
        # Основной выбор
        code_request0 = int(input("Получение отчета (0), или идентификация (1), или запись в базу (2) или выйти из цикла (3): "))
        if (code_request0==0):
            operation_type = 0
            parameters = NomRequestCommandHandlerParameter(operation_type)
        elif (code_request0==1):
            code_request1 = int(input("Введите QR (0) или NN (1): "))
            operation_type = code_request1

            if (code_request1 == 0):
                path = 'D:\\PYTHON\\Programms\\Smart_app_UMNIK\\Server_version\\QR_images\\'
                name_image = str(number_of_image) + '_im.jpg'
                # Блок загрузки изображения
                image = cv2.imread(path + name_image)

            elif (code_request1 == 1):
                path = 'D:\\PYTHON\\Programms\\Smart_app_UMNIK\\Server_version\\NN_images\\'
                image=[]
                for i in range(3):
                    b = os.path.join(path, str(number_of_image) + '_' + str(i + 1) + '.jpg')
                    f = cv2.imread(b)
                    if (i==0):
                        image = np.zeros((3,f.shape[0], f.shape[1], f.shape[2])).astype('uint8')
                    image[i,:,:,:] = f
            parameters = PartIdentificationCommandHandlerParameter(image, operation_type)
        elif (code_request0==2):
            # Блок загрузки изображения
            path = 'D:\\PYTHON\\Programms\\Smart_app_UMNIK\\Server_version\\QR_images\\'
            name_image = str(number_of_image) + '_im.jpg'
            # Блок загрузки изображения
            image = cv2.imread(path + name_image)
            operation_type = 0
            parameters = CheckInCommandHandlerParameter(image, operation_type)
        else:
            print('Выход')
            break

        result_request = serversmartapp.initFunction(code_request0, parameters)
        print(result_request)


    except Exception as err:
        print(str(err), '\n')
        break

serversocket.close()