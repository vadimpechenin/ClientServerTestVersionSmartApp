from threading import Thread
from kivy.uix.screenmanager import Screen


# Библиотеки для формирования структуры пересылаемого сообщения
from message.messageStructure import MessageStructure
from message.messageStructureParameter import MessageStructureParameter
from message.messageResponceParameter import MessageResponceParameter

from client.applicationEnvironment import appEnvironment

import time


class ReportsWindow(Screen):
    def __init__(self, *args, **kwargs):
        super(ReportsWindow, self).__init__(*args, **kwargs)
        self.sock = appEnvironment.sock
        self.ciphers_filter = []
        Thread(target=self.textInInput).start()
        self.listOfItemsView = 0 #Переменная для обмена сообщениями с сервером в части отчетов
        self.param_for_filter = 1  # С каким атрибутом работаем
        self.ifTriggerReport = 0  # Прорисовка и обновление отчета по результатам запроса
        # Объект - запрос на сервер
        self.messageParameter = MessageStructureParameter()
        # Объект - ответ с сервера
        self.messageResponce = MessageResponceParameter()
        appEnvironment.ReportsWindowObj = self

    def fillData(self, listOfItemsView):
        self.listOfItemsView = listOfItemsView

    def fillDataFilter(self, listOfItemsView, messageParameter):
        self.listOfItemsView = listOfItemsView
        self.messageParameter = messageParameter

    def textInInput(self):
        # Функция для вывода информации в текстовые окна приложения
        while True:
            time.sleep(0.4)
            if (self.listOfItemsView == 2):
                # Отправка запроса на сервер и получения ответа, заполняющего пределы для фильтров
                self.messageParameter.code_request0 = 5
                self.messageParameter.code_request1 = 0

                print('Зашел в отправку сообщения')
                self.sock.send_data(self.messageParameter)

                self.messageParameter = MessageStructure.ClearObject(self.messageParameter)
                self.listOfItemsView = 4
            if (self.listOfItemsView == 4):

                self.messageResponce =  self.sock.get_data()
                if (self.messageResponce.message == 'Пределы для фильтров'):
                    self.listOfItemsView = 1

            if (self.listOfItemsView == 1):
                # Заполнение текстовых полей
                if len(self.messageParameter.type_name_list) > 0:
                    textstr = ''
                    for item in self.messageParameter.type_name_list:
                        textstr = textstr + item + '; '
                    self.ids.text_input1.text = textstr
                if len(self.messageParameter.workshop_number_list) > 0:
                    textstr = ''
                    for item in self.messageParameter.workshop_number_list:
                        textstr = textstr + item + '; '
                    self.ids.text_input2.text = textstr
                if len(self.messageParameter.lot_number_list) > 0:
                    textstr = ''
                    for item in self.messageParameter.lot_number_list:
                        textstr = textstr + item + '; '
                    self.ids.text_input3.text = textstr

                # Данные для ползунков
                self.ids.slider_d1.min = round(self.messageResponce.imbalance_list[0] - 0.05, 2)
                self.ids.slider_d1.max = round(self.messageResponce.imbalance_list[1] + 0.05, 2)
                self.ids.slider_d1.value = round(self.messageResponce.imbalance_list[0] - 0.05, 2)
                self.ids.slider_d2.min = round(self.messageResponce.imbalance_list[0] - 0.05, 2)
                self.ids.slider_d2.max = round(self.messageResponce.imbalance_list[1] + 0.05, 2)
                self.ids.slider_d2.value = round(self.messageResponce.imbalance_list[1] + 0.05, 2)

                self.ids.slider_d3.min = round(self.messageResponce.diameter_list[0] - 0.05, 2)
                self.ids.slider_d3.max = round(self.messageResponce.diameter_list[1] + 0.05, 2)
                self.ids.slider_d3.value = round(self.messageResponce.diameter_list[0] - 0.05, 2)
                self.ids.slider_d4.min = round(self.messageResponce.diameter_list[0] - 0.05, 2)
                self.ids.slider_d4.max = round(self.messageResponce.diameter_list[1] + 0.05, 2)
                self.ids.slider_d4.value = round(self.messageResponce.diameter_list[1] + 0.05, 2)

                self.listOfItemsView = 0

            if (self.listOfItemsView == 3):
                # Проверка нулевых значений перед отправкой. Если 0, или противоречивые - исправление
                if len(self.messageParameter.type_name_list) == 0:
                    self.messageParameter.type_name_list = self.messageResponce.type_name_list
                if len(self.messageParameter.workshop_number_list) == 0:
                    self.messageParameter.workshop_number_list = self.messageResponce.workshop_number_list
                if len(self.messageParameter.lot_number_list) == 0:
                    self.messageParameter.lot_number_list = self.messageResponce.lot_number_list

                # Отправка запроса на сервер для получения ответа для формирования отчета
                self.messageParameter.code_request0 = 6
                self.messageParameter.code_request1 = 0
                self.sock.send_data(self.messageParameter)

                self.messageParameter = MessageStructure.ClearObject(self.messageParameter)

                self.listOfItemsView = 5

            if (self.listOfItemsView == 5):
                # Получение ответа для формирования отчета
                self.messageResponce =  self.sock.get_data()
                if (self.messageResponce.message == 'Отчет с учетом фильтров'):
                    self.listOfItemsView = 0
                    self.ifTriggerReport = 1

    def ScrollWindowFilterType(self):
        self.param_for_filter = 1
        appEnvironment.FilterWindowObj.fillData(self.param_for_filter, self.messageResponce,
                                                self.messageParameter)
        # Переход в конкретное описание детали
        self.manager.current = 'filterOfItem'
        # Переход окна вправо (текущее уходит влево)
        self.manager.transition.direction = "left"
        # self.ScrollWindowFilter()

    def ScrollWindowFilterWorkshop(self):
        self.param_for_filter = 2
        appEnvironment.FilterWindowObj.fillData(self.param_for_filter, self.messageResponce, self.messageParameter)
        # Переход в конкретное описание детали
        self.manager.current = 'filterOfItem'
        # Переход окна вправо (текущее уходит влево)
        self.manager.transition.direction = "left"
        # self.ScrollWindowFilter()

    def ScrollWindowFilterLot(self):
        self.param_for_filter = 3
        appEnvironment.FilterWindowObj.fillData(self.param_for_filter, self.messageResponce,
                                                self.messageParameter)
        # Переход в конкретное описание детали
        self.manager.current = 'filterOfItem'
        # Переход окна вправо (текущее уходит влево)
        self.manager.transition.direction = "left"
        # self.ScrollWindowFilter()

    def DataForReportAndDataFromDataBase(self):
        # Функция для формирования запроса и получения ответа по данным для отчета
        self.messageParameter.imbalance_list = []
        self.messageParameter.imbalance_list.append(round(self.ids.slider_d1.value, 2))
        self.messageParameter.imbalance_list.append(round(self.ids.slider_d2.value, 2))
        self.messageParameter.diameter_list = []
        self.messageParameter.diameter_list.append(round(self.ids.slider_d3.value, 2))
        self.messageParameter.diameter_list.append(round(self.ids.slider_d4.value, 2))
        self.listOfItemsView = 3
        appEnvironment.MainReportObj.fillData(self.ifTriggerReport,self.listOfItemsView, self.messageResponce)