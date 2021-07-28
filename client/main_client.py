#kivy-приложение


import time
from client.clientModule import MySocket
from os.path import dirname, join, basename, isfile, getsize
from os import listdir
from threading import Thread, Lock


#Библиотека для всплывающих окон
from kivy.uix.popup import Popup
import io
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

#Библиотеки для многих страниц
from kivy.uix.screenmanager import ScreenManager, Screen

#Для чтения файлов с диска
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.factory import Factory

# Для всплывающих окон
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton

# Для размера окна
from kivy.core.window import Window

import cv2

#Импорт классов, отвечающих за бизнес-логику окон
#from client.windowClasses import *
from client.bootstrap import Bootstrap
from client.windowClasses.loadDialog import LoadDialog


from client.applicationEnvironment import appEnvironment

# Библиотеки для формирования структуры пересылаемого сообщения
from message.messageStructure import MessageStructure
from message.messageStructureParameter import MessageStructureParameter
from message.messageResponceParameter import MessageResponceParameter

koef = 1


# Объект - запрос на сервер
messageParameter = MessageStructureParameter()
#Объект - ответ с сервера
messageResponce = MessageResponceParameter()

if (koef == 1):
    Window.size = (420, 800)
else:
    Window.size = (1100, 2300)

#Искусственное заполнение ответа с сервера, нужно для формирования данных для фильтров
listOfItemsView = 0 #Переменная для обмена сообщениями с сервером в части отчетов
param_for_filter = 1  #С каким атрибутом работаем
ifTriggerReport = 0 #Прорисовка и обновление отчета по результатам запроса
fourthTrigger = 0
#Подключение к серверу (1 точка для подключения)
#sock = MySocket()
# Классы для окон

class MainWindow(Screen):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        appEnvironment.MainWindowObj = self

    def triggerForServer(self):
        global listOfItemsView
        # Метод для изменения переменных, отвечающих за запуск потока общения с сервером
        listOfItemsView = 2
        time.sleep(0.3)

    def triggerForServerFourth(self):
        global fourthTrigger
        # Метод для загрузки списка номенклатуры в окне Номенклатура
        fourthTrigger = 1
        appEnvironment.FourthWindowObj.fillData(fourthTrigger)
        #time.sleep(0.3)


class ReportsWindow(Screen):
    def __init__(self, *args, **kwargs):
        super(ReportsWindow, self).__init__(*args, **kwargs)
        self.sock = appEnvironment.sock
        self.ciphers_filter = []
        Thread(target=self.textInInput).start()
        # self.textInInput()

    def textInInput(self):
        # Функция для вывода информации в текстовые окна приложения
        global messageParameter, messageResponce
        global listOfItemsView, ifTriggerReport
        while True:
            time.sleep(0.4)
            if (listOfItemsView == 2):
                # Отправка запроса на сервер и получения ответа, заполняющего пределы для фильтров
                messageParameter.code_request0 = 5
                messageParameter.code_request1 = 0

                print('Зашел в отправку сообщения')
                self.sock.send_data(messageParameter)

                messageParameter = MessageStructure.ClearObject(messageParameter)
                listOfItemsView = 4
            if (listOfItemsView == 4):

                messageResponce =  self.sock.get_data()
                if (messageResponce.message == 'Пределы для фильтров'):
                    listOfItemsView = 1

            if (listOfItemsView == 1):
                # Заполнение текстовых полей
                if len(messageParameter.type_name_list) > 0:
                    textstr = ''
                    for item in messageParameter.type_name_list:
                        textstr = textstr + item + '; '
                    self.ids.text_input1.text = textstr
                if len(messageParameter.workshop_number_list) > 0:
                    textstr = ''
                    for item in messageParameter.workshop_number_list:
                        textstr = textstr + item + '; '
                    self.ids.text_input2.text = textstr
                if len(messageParameter.lot_number_list) > 0:
                    textstr = ''
                    for item in messageParameter.lot_number_list:
                        textstr = textstr + item + '; '
                    self.ids.text_input3.text = textstr

                # Данные для ползунков
                self.ids.slider_d1.min = round(messageResponce.imbalance_list[0] - 0.05, 2)
                self.ids.slider_d1.max = round(messageResponce.imbalance_list[1] + 0.05, 2)
                self.ids.slider_d1.value = round(messageResponce.imbalance_list[0] - 0.05, 2)
                self.ids.slider_d2.min = round(messageResponce.imbalance_list[0] - 0.05, 2)
                self.ids.slider_d2.max = round(messageResponce.imbalance_list[1] + 0.05, 2)
                self.ids.slider_d2.value = round(messageResponce.imbalance_list[1] + 0.05, 2)

                self.ids.slider_d3.min = round(messageResponce.diameter_list[0] - 0.05, 2)
                self.ids.slider_d3.max = round(messageResponce.diameter_list[1] + 0.05, 2)
                self.ids.slider_d3.value = round(messageResponce.diameter_list[0] - 0.05, 2)
                self.ids.slider_d4.min = round(messageResponce.diameter_list[0] - 0.05, 2)
                self.ids.slider_d4.max = round(messageResponce.diameter_list[1] + 0.05, 2)
                self.ids.slider_d4.value = round(messageResponce.diameter_list[1] + 0.05, 2)

                listOfItemsView = 0

            if (listOfItemsView == 3):
                # Проверка нулевых значений перед отправкой. Если 0, или противоречивые - исправление
                if len(messageParameter.type_name_list) == 0:
                    messageParameter.type_name_list = messageResponce.type_name_list
                if len(messageParameter.workshop_number_list) == 0:
                    messageParameter.workshop_number_list = messageResponce.workshop_number_list
                if len(messageParameter.lot_number_list) == 0:
                    messageParameter.lot_number_list = messageResponce.lot_number_list

                # Отправка запроса на сервер для получения ответа для формирования отчета
                messageParameter.code_request0 = 6
                messageParameter.code_request1 = 0
                self.sock.send_data(messageParameter)

                messageParameter = MessageStructure.ClearObject(messageParameter)

                listOfItemsView = 5

            if (listOfItemsView == 5):
                # Получение ответа для формирования отчета
                messageResponce =  self.sock.get_data()
                if (messageResponce.message == 'Отчет с учетом фильтров'):
                    listOfItemsView = 0
                    ifTriggerReport = 1

    def ScrollWindowFilterType(self):
        global param_for_filter
        param_for_filter = 1
        # Переход в конкретное описание детали
        self.manager.current = 'filterOfItem'
        # Переход окна вправо (текущее уходит влево)
        self.manager.transition.direction = "left"
        # self.ScrollWindowFilter()

    def ScrollWindowFilterWorkshop(self):
        global param_for_filter
        param_for_filter = 2
        # Переход в конкретное описание детали
        self.manager.current = 'filterOfItem'
        # Переход окна вправо (текущее уходит влево)
        self.manager.transition.direction = "left"
        # self.ScrollWindowFilter()

    def ScrollWindowFilterLot(self):
        global param_for_filter
        param_for_filter = 3
        # Переход в конкретное описание детали
        self.manager.current = 'filterOfItem'
        # Переход окна вправо (текущее уходит влево)
        self.manager.transition.direction = "left"
        # self.ScrollWindowFilter()

    def DataForReportAndDataFromDataBase(self):
        # Функция для формирования запроса и получения ответа по данным для отчета
        global listOfItemsView, ifTriggerReport
        global messageParameter, messageResponce
        messageParameter.imbalance_list = []
        messageParameter.imbalance_list.append(round(self.ids.slider_d1.value, 2))
        messageParameter.imbalance_list.append(round(self.ids.slider_d2.value, 2))
        messageParameter.diameter_list = []
        messageParameter.diameter_list.append(round(self.ids.slider_d3.value, 2))
        messageParameter.diameter_list.append(round(self.ids.slider_d4.value, 2))
        listOfItemsView = 3

        appEnvironment.MainReportObj.fillData(ifTriggerReport,listOfItemsView, messageResponce)

class FilterWindow(Screen):
    def __init__(self, *args, **kwargs):
        super(FilterWindow, self).__init__(*args, **kwargs)
        #self.ScrollWindowFilter()
        #Фильтр для чего применять (1 - тип, 2 - цех, 3 - участок)

    def ScrollWindowFilter(self):
        global param_for_filter

        global messageResponce, messageParameter
        if param_for_filter == 1:
            messageParameter.type_name_list = []
            self.ciphers_filter = messageResponce.type_name_list
        elif param_for_filter == 2:
            messageParameter.workshop_number_list = []
            self.ciphers_filter = messageResponce.workshop_number_list
        elif param_for_filter == 3:
            messageParameter.lot_number_list = []
            self.ciphers_filter = messageResponce.lot_number_list

        leftGrid = GridLayout(cols=1, size_hint_y=None)
        leftGrid.bind(minimum_height=leftGrid.setter('height'))

        leftGrid = GridLayout(cols=1, size_hint_y=None)
        #Убедимся, что высота такая, чтобы было что прокручивать.

        self.toggle = [0 for _ in range(len(self.ciphers_filter))]

        for index in range(len(self.ciphers_filter)):
            self.toggle[index] = ToggleButton(
                text= self.ciphers_filter[index],  size_hint_y=None,
                group= self.ciphers_filter[index], height=30*koef
                )
            #self.toggle[index].bind(on_press=self.changer)
            leftGrid.add_widget(self.toggle[index])

        self.ids.ScrollWindowFilterid.add_widget(leftGrid)

    def changerFilter(self, *args):
        global messageResponce, messageParameter
        global param_for_filter

        list_button_down = []
        for i in range(len( self.ciphers_filter)):
            if self.toggle[i].state == 'down':
                if param_for_filter == 1:
                    list_button_down.append(messageResponce.type_name_list[i])
                    messageParameter.type_name_list.append(messageResponce.type_name_list[i])
                if param_for_filter == 2:
                    list_button_down.append(messageResponce.workshop_number_list[i])
                    messageParameter.workshop_number_list.append(messageResponce.workshop_number_list[i])
                if param_for_filter == 3:
                    list_button_down.append(messageResponce.lot_number_list[i])
                    messageParameter.lot_number_list.append(messageResponce.lot_number_list[i])

        if (len(list_button_down)==0):
            title = 'Предупреждение'
            text='Ничего не выбрано'
            self.popupForFilter(title, text)
        else:
            title = 'Предупреждение'
            text = 'Выбор сохранен'
            self.popupForFilter(title, text)


    def popupForFilter(self,title,text):
        PopupGrid = GridLayout(rows=2, size_hint_y=None)
        PopupGrid.add_widget(Label(text=text))
        content = Button(text='Закрыть')
        PopupGrid.add_widget(content)
        popup = Popup(title=title, content=PopupGrid,
                      auto_dismiss=False, size_hint=(None, None), size=(int(300 * koef), int(200 * koef)))

        content.bind(on_press=popup.dismiss)
        popup.open()

    def dellwidgetfilter(self):
        # удаляет все виджеты, которые находяться в another_box
        global listOfItemsView
        for i in range(len(self.ids.ScrollWindowFilterid.children)):
            self.ids.ScrollWindowFilterid.remove_widget(self.ids.ScrollWindowFilterid.children[-1])

        listOfItemsView = 1

# Менеджер перехода между страницами и передачи данных
class WindowManager(ScreenManager):
    pass

if __name__ == '__main__':
    Bootstrap.initEnviroment()
    Bootstrap.run()
