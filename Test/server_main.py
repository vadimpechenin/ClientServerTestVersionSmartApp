"""
Серверная часть проекта УМНИК 2021 "Умный склад"
версия 1
Реализация с сокетами
"""
import cv2
import os
import numpy as np

#Переменные для начальной инициализации базы данных
#Классы для работы приложения
from Handlers.Server_class import MainCommandHandler as ServerSmartApp
from Handlers.CheckIn.CheckInCommandHandlerParameter import CheckInCommandHandlerParameter
from Handlers.NomRequest.NomRequestCommandHandlerParameter import NomRequestCommandHandlerParameter
from Handlers.PartIdentification.PartIdentificationCommandHandlerParameter import PartIdentificationCommandHandlerParameter
from Handlers.loadDictLocation.loadDictLocationHandlerParameter import LoadDictLocationHandlerParameter
from Handlers.loadDictType.loadDictTypeHandlerParameter import LoadDictTypeHandlerParameter
from Handlers.loadAllCharacteristics.loadAllCharacteristicsHandlerParameter import LoadAllCharacteristicsHandlerParameter
from Handlers.loadReport.loadReportHandlerParameter import LoadReportHandlerParameter
from Handlers.loadReportNomenclature.loadReportNomenclatureHandlerParameter import LoadReportHandlerNomenclatureParameter

#Подключение всего функционала по работе с изображениями и базой данных
serversmartapp = ServerSmartApp()

import socket
import time
from common.socketHelper import SocketHelper

from message.messageStructure import MessageStructure
from message.messageStructureParameter import MessageStructureParameter
from message.messageResponceParameter import MessageResponceParameter

# Объект - запрос на сервер
messageParameter = MessageStructureParameter()
#Объект - ответ с сервера
messageResponce = MessageResponceParameter()


#БЛОК КОНСТАНТ
host = 'localhost'
#host = '192.168.0.151'
#host = '10.8.0.34'
port = 54545

BUFFER_LENGTH = 2048

path = 'D:\\PYTHON\\Programms\\Smart_app_UMNIK\\Client_server_version_1\\Test\\'


serversocket = socket.socket()

serversocket.bind((host, port))

serversocket.listen(1)
print("Server is listening", '\n')

clientsocket,addr = serversocket.accept()

helper = SocketHelper(clientsocket)

print("got a connection from %s" % str(addr))


def save_image(messageParameter):

    global BUFFER_LENGTH
    k = 1
    for j in range(len(messageParameter.Images)):
        cv2.imwrite('image_server' + str(k) + '.jpg',messageParameter.Images[j])
        print("Размер принятого изображения: ", messageParameter.sizeOfImages[k-1])
        #time.sleep(0.3)
        k+=1
    k = 0


# Имитатор основного цикла
while True:
    try:

        sizeOfRequest = helper.readInt()
        print("Размер принимаемого сообщения: " + str(sizeOfRequest))
        messageParameterAsBytes = helper.readBytesArray(sizeOfRequest)
        messageParameter = MessageStructure.RestoreFromBytes(messageParameterAsBytes)

        print("Код от клиента, основной:" + str(messageParameter.code_request0) + ", дополнительный:" + str(messageParameter.code_request1))
        #time.sleep(0.3)
        # Принимаю картинку
        if messageParameter.code_request0 == 1:
            save_image(messageParameter)
        if messageParameter.code_request0 == 3 and messageParameter.code_request1 == 0:
            operation_type = 3
            parameters = LoadDictLocationHandlerParameter(operation_type)
            g = 0
        if messageParameter.code_request0 == 2 and messageParameter.code_request1 == 0:
            save_image(messageParameter)

        # Основной выбор

        #code_request0 = int(input("Получение отчета (0), или идентификация (1), или запись в базу (2) или выйти из цикла (3): "))
        if (messageParameter.code_request0==0):
            operation_type = 0
            parameters = NomRequestCommandHandlerParameter(operation_type)
        elif (messageParameter.code_request0 == 7):

            parameters = LoadReportHandlerNomenclatureParameter(messageParameter.message)
        elif (messageParameter.code_request0==5):
            operation_type = 5
            parameters = LoadAllCharacteristicsHandlerParameter(operation_type)
        elif (messageParameter.code_request0==6):

            parameters = LoadReportHandlerParameter(messageParameter.type_name_list, messageParameter.workshop_number_list,
                                                    messageParameter.lot_number_list, messageParameter.imbalance_list,
                                                    messageParameter.diameter_list)
        elif (messageParameter.code_request0==1):
            #code_request1 = int(input("Введите QR (0) или NN (1): "))
            operation_type = messageParameter.code_request1


            if (messageParameter.code_request1 == 0):
                name_image = 'image_server1.jpg'
                # Блок загрузки изображения
                image = cv2.imread(path + name_image)

            elif (messageParameter.code_request1 == 1):
                image=[]
                for i in range(3):
                    name_image = 'image_server' + str(i+1) + '.jpg'
                    f = cv2.imread(path + name_image)
                    if (i==0):
                        image = {}
                        #image = np.zeros((3,f.shape[0], f.shape[1], f.shape[2])).astype('uint8')
                    image[i] = f
                    #image[i, :, :, :] = f
            parameters = PartIdentificationCommandHandlerParameter(image, operation_type)
        elif (messageParameter.code_request0==2):
            # Блок загрузки изображения
            name_image = 'image_server1.jpg'
            # Блок загрузки изображения
            image = cv2.imread(path + name_image)
            operation_type = 0
            parameters = CheckInCommandHandlerParameter(image, operation_type, messageParameter.nameOfImage, messageParameter.workshopNumber, messageParameter.lotNumber)
        elif (messageParameter.code_request0==6):
            print('Выход')
            break

        result_request = serversmartapp.initFunction(messageParameter.code_request0, parameters)
        print(result_request)

        MessageStructure.ClearObjectResponce(messageResponce)
        if messageParameter.code_request0 == 0:
            messageResponce.message = 'Список номенклатуры деталей'
            messageResponce.type_name_list = result_request

            messageResponceAsBytes = MessageStructure.SaveToBytes(messageResponce)

            helper.writeInt(len(messageResponceAsBytes))
            print("Размер отсылаемого ответа:", len(messageResponceAsBytes))

            helper.writeBytesArray(messageResponceAsBytes)
            print("Ответ отправлен")

        if messageParameter.code_request0 == 7:
            messageResponce.message = 'Отчет по номенклатуре деталей'
            messageResponce.report_list.append(['ID', 'Дата', 'Цех', 'Участок'])
            for item in result_request:
                messageResponce.report_list.append(item)

            messageResponceAsBytes = MessageStructure.SaveToBytes(messageResponce)

            helper.writeInt(len(messageResponceAsBytes))
            print("Размер отсылаемого ответа:", len(messageResponceAsBytes))

            helper.writeBytesArray(messageResponceAsBytes)
            print("Ответ отправлен")

        if messageParameter.code_request0 == 5:
            messageResponce.message = 'Пределы для фильтров'

            messageResponce.type_name_list = result_request.pop(0)
            workshop_list = []
            lot_list =[]
            for workshop_count, lot_count in result_request[0]:
                if workshop_count not in workshop_list:
                    workshop_list.append(workshop_count)
                if lot_count not in lot_list:
                    lot_list.append(lot_count)

            messageResponce.workshop_number_list = workshop_list
            messageResponce.lot_number_list = lot_list

            imbalance_list = []
            diameter_list = []
            for imbalance_count, diameter_count in result_request[1]:
                if imbalance_count not in imbalance_list:
                    imbalance_list.append(imbalance_count)
                if diameter_count not in diameter_list:
                    diameter_list.append(diameter_count)

            messageResponce.imbalance_list.append(round(min(imbalance_list),2))
            messageResponce.imbalance_list.append(round(max(imbalance_list),2))
            messageResponce.diameter_list.append(round(min(diameter_list),2))
            messageResponce.diameter_list.append(round(max(diameter_list),2))

            messageResponceAsBytes = MessageStructure.SaveToBytes(messageResponce)

            helper.writeInt(len(messageResponceAsBytes))
            print("Размер отсылаемого ответа:", len(messageResponceAsBytes))

            helper.writeBytesArray(messageResponceAsBytes)
            print("Ответ отправлен")

        if messageParameter.code_request0 == 6:
            # Данные запроса по отчету
            messageResponce.message = 'Отчет с учетом фильтров'
            messageResponce.report_list.append(['ID', 'Тип', 'Дата', 'Цех', 'Участок', 'Дисбаланс', 'Диаметр'])
            for item in result_request:
                messageResponce.report_list.append(item)

            messageResponceAsBytes = MessageStructure.SaveToBytes(messageResponce)
            helper.writeInt(len(messageResponceAsBytes))
            print("Размер отсылаемого ответа:", len(messageResponceAsBytes))

            helper.writeBytesArray(messageResponceAsBytes)
            print("Ответ отправлен")


        if messageParameter.code_request0 == 1:
            messageResponce.message = 'Изображение пришло'
            detail_name_responce_dict = result_request.pop(0)
            detail_name_responce = detail_name_responce_dict['type_name']
            messageResponce.responce.append(detail_name_responce)
            messageResponceAsBytes = MessageStructure.SaveToBytes(messageResponce)

            helper.writeInt(len(messageResponceAsBytes))
            print("Размер отсылаемого ответа:", len(messageResponceAsBytes))

            helper.writeBytesArray(messageResponceAsBytes)
            print("Ответ отправлен")

        if messageParameter.code_request0 == 3:
            messageResponce.message = 'Список возможных месторасположений детали'
            workshop_list = []
            lot_list =[]
            for workshop_count, lot_count in result_request:
                if workshop_count not in workshop_list:
                    workshop_list.append(workshop_count)
                if lot_count not in lot_list:
                    lot_list.append(lot_count)

            messageResponce.workshop_number_list=workshop_list
            messageResponce.lot_number_list=lot_list
            messageResponceAsBytes = MessageStructure.SaveToBytes(messageResponce)

            helper.writeInt(len(messageResponceAsBytes))
            print("Размер отсылаемого ответа:", len(messageResponceAsBytes))

            helper.writeBytesArray(messageResponceAsBytes)
            print("Ответ отправлен")

        if messageParameter.code_request0 == 2:
            messageResponce.message = 'Изменения внесены'
            workshop_list = []
            lot_list = []
            messageResponce.responce.append(result_request)
            messageResponceAsBytes = MessageStructure.SaveToBytes(messageResponce)

            helper.writeInt(len(messageResponceAsBytes))
            print("Размер отсылаемого ответа:", len(messageResponceAsBytes))

            helper.writeBytesArray(messageResponceAsBytes)
            print("Ответ отправлен")

    except Exception as err:
        print(str(err), '\n')
        break

serversocket.close()


