from threading import Thread
from kivy.uix.screenmanager import Screen


# Библиотеки для формирования структуры пересылаемого сообщения
from message.messageStructure import MessageStructure
from message.messageStructureParameter import MessageStructureParameter
from message.messageResponceParameter import MessageResponceParameter

from client.applicationEnvironment import appEnvironment
from client.clientModule import MySocket


from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

import weakref

import time


class ReportsWindow(Screen):
    def __init__(self, *args, **kwargs):
        super(ReportsWindow, self).__init__(*args, **kwargs)
        #self.sock = appEnvironment.sock
        self.ciphers_filter = []
        Thread(target=self.textInInput).start()
        self.listOfItemsView = 0 #Переменная для обмена сообщениями с сервером в части отчетов
        self.param_for_filter = 1  # С каким атрибутом работаем
        self.ifTriggerReport = 0  # Прорисовка и обновление отчета по результатам запроса
        # Объект - запрос на сервер
        self.messageParameter = MessageStructureParameter()
        # Объект - ответ с сервера
        self.messageResponce = MessageResponceParameter()
        self.koef = appEnvironment.koef
        appEnvironment.ReportsWindowObj = self
        self.sock = None

    def fillData(self, listOfItemsView):
        self.listOfItemsView = listOfItemsView

    def fillDataFilter(self, listOfItemsView, messageParameter):
        self.messageParameter = messageParameter
        self.listOfItemsView = listOfItemsView

    def fillDataReport(self, listOfItemsView):
        #self.messageResponce = messageResponce
        self.listOfItemsView = listOfItemsView

    def textInInput(self):
        # Функция для вывода информации в текстовые окна приложения
        while True:
            time.sleep(0.4)
            if (self.listOfItemsView == 2):
                # Отправка запроса на сервер и получения ответа, заполняющего пределы для фильтров
                self.messageParameter.code_request0 = 5
                self.messageParameter.code_request1 = 0
                print('Зашел в отправку сообщения')
                if appEnvironment.ClientProxyObj.connect():
                    self.messageResponce = appEnvironment.ClientProxyObj.sendRequest(self.messageParameter)
                    self.messageParameter = MessageStructure.ClearObject(self.messageParameter)
                    if self.messageResponce != None:
                        if (self.messageResponce.message == 'Пределы для фильтров'):
                            self.listOfItemsView = 1
                    else:
                        self.popupForSocketNone()
                        self.listOfItemsView = 0


                else:
                    self.popupForSocket(appEnvironment.title, appEnvironment.text)
                    self.listOfItemsView = 0

                """
                try:
                    if (appEnvironment.sock is not None):
                        appEnvironment.sock.sock.close()
                        appEnvironment.sock = None
                    print('Зашел в отправку сообщения')
                    appEnvironment.sock = MySocket(host=appEnvironment.host, port=appEnvironment.port)
                except:
                    self.popupForSocket(appEnvironment.title, appEnvironment.text)
                    self.listOfItemsView = 0
                else:
                    appEnvironment.sock.send_data(self.messageParameter)

                    self.messageParameter = MessageStructure.ClearObject(self.messageParameter)
                    self.listOfItemsView = 4


            if (self.listOfItemsView == 4):

                self.messageResponce =  appEnvironment.sock.get_data()
                if (self.messageResponce.message == 'Пределы для фильтров'):
                    self.listOfItemsView = 1
            """
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

                if appEnvironment.ClientProxyObj.connect():
                    self.messageResponce = appEnvironment.ClientProxyObj.sendRequest(self.messageParameter)
                    self.messageParameter = MessageStructure.ClearObject(self.messageParameter)
                    if self.messageResponce != None:
                        if (self.messageResponce.message == 'Отчет с учетом фильтров'):
                            self.listOfItemsView = 0
                            self.ifTriggerReport = 1
                    else:
                        self.popupForSocketNone()
                        self.listOfItemsView = 0


                else:
                    self.popupForSocket(appEnvironment.title, appEnvironment.text)
                    self.listOfItemsView = 0

                """
                appEnvironment.sock.send_data(self.messageParameter)

                self.messageParameter = MessageStructure.ClearObject(self.messageParameter)

                self.listOfItemsView = 5

            if (self.listOfItemsView == 5):
                # Получение ответа для формирования отчета
                self.messageResponce =  appEnvironment.sock.get_data()
                if (self.messageResponce.message == 'Отчет с учетом фильтров'):
                    self.listOfItemsView = 0
                    self.ifTriggerReport = 1
            """
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
        time.sleep(0.4)
        appEnvironment.MainReportObj.fillData(self.ifTriggerReport,self.listOfItemsView, self.messageResponce)

    def popupForSocket(self, title, text):
        PopupGrid = GridLayout(rows=4, size_hint_y=None)
        PopupGrid.add_widget(Label(text=text))

        host1 = TextInput()
        PopupGrid.add_widget(host1)  #
        PopupGrid.ids['host1'] = weakref.ref(host1)
        PopupGrid.ids.host1.text = appEnvironment.host
        PopupGrid.ids.host1.multiline = True

        port1 = TextInput()
        PopupGrid.add_widget(port1)  #
        PopupGrid.ids['port1'] = weakref.ref(port1)
        PopupGrid.ids.port1.text = str(appEnvironment.port)
        PopupGrid.ids.port1.multiline = True
        content = Button(text='Закрыть')
        PopupGrid.add_widget(content)
        self.popup4 = Popup(title=title, content=PopupGrid,
                            auto_dismiss=False, size_hint=(None, None),
                            size=(int(300 * self.koef), int(200 * self.koef)))
        self.PopupGrid = PopupGrid
        content.bind(on_press=self.closePopupForSocket)
        self.popup4.open()

    def closePopupForSocket(self, *args):
        self.hostAdress()
        self.popup4.dismiss()
        #https://kivy.org/doc/stable/api-kivy.uix.screenmanager.html
        #appEnvironment.WindowManagerObj.switch_to(appEnvironment.MainWindowObj, direction='right')

    def hostAdress(self):

        appEnvironment.host = self.PopupGrid.ids.host1.text
        appEnvironment.port = int(self.PopupGrid.ids.port1.text)