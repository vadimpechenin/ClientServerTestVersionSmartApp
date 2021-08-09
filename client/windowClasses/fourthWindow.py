
from threading import Thread
# Библиотеки для формирования структуры пересылаемого сообщения
from message.messageStructure import MessageStructure
from message.messageStructureParameter import MessageStructureParameter
from message.messageResponceParameter import MessageResponceParameter

import time

from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

import weakref

from client.applicationEnvironment import appEnvironment
from client.clientModule import MySocket

class FourthWindow(Screen):
    #Окно для просмотра номенклатуры деталей
    def __init__(self, *args, **kwargs):
        super(FourthWindow, self).__init__(*args, **kwargs)
        self.listOfItems = True
        Thread(target=self.textInInputFourth).start()
        # Объект - запрос на сервер
        self.messageParameter = MessageStructureParameter()
        # Объект - ответ с сервера
        self.messageResponce = MessageResponceParameter()
        self.partName = ''
        self.fourthTrigger = 0 # Переключатель для работы с потоком
        appEnvironment.FourthWindowObj = self
        self.koef = appEnvironment.koef
        #self.sock = appEnvironment.sock

    def fillData(self,fourthTriggerOutdoor):
        self.fourthTrigger = fourthTriggerOutdoor

    def textInInputFourth(self):

        while True:
            time.sleep(0.4)
            if (self.fourthTrigger == 1):
                # Отправка запроса на сервер и получения ответа, заполняющего список номенклатуры деталей
                self.messageParameter.code_request0 = 0
                self.messageParameter.code_request1 = 0
                try:
                    print('Зашел в отправку сообщения')
                    self.sock = MySocket(appEnvironment.host, port=appEnvironment.port)
                    # self.sock.send_data(messageParameter)
                    self.sock.send_data(self.messageParameter)

                    self.messageParameter = MessageStructure.ClearObject(self.messageParameter)
                    self.fourthTrigger = 2
                except:
                    self.popupForSocket(appEnvironment.title, appEnvironment.text)
                    self.fourthTrigger = 0

            if (self.fourthTrigger == 2):
                self.messageResponce = self.sock.get_data()
                if (self.messageResponce.message == 'Список номенклатуры деталей'):
                    self.fourthTrigger = 0

            if (self.fourthTrigger == 3):
                # Отправка запроса на сервер и получения ответа, заполняющего отчет для выбранного вида детали
                self.messageParameter.code_request0 = 7
                self.messageParameter.code_request1 = 0

                print('Зашел в отправку сообщения')
                # self.sock.send_data(messageParameter)
                self.sock.send_data(self.messageParameter)

                self.messageParameter = MessageStructure.ClearObject(self.messageParameter)
                self.fourthTrigger = 4

            if (self.fourthTrigger == 4):
                self.messageResponce = self.sock.get_data()

                if (self.messageResponce.message == 'Отчет по номенклатуре деталей'):
                    appEnvironment.ReportsWindowDetailObj.fillData(self.partName, self.messageResponce)
                    self.fourthTrigger = 0

    def ScrollWindow(self):
        if (self.listOfItems==True):
            #self.ids.ScrollWindowid.add_widget(ScrollView(size_hint=[1, 1]))
            self.ids.Scrollbuttonid.text = "Список номенклатуры выведен"
            leftGrid = GridLayout(cols=1, size_hint_y=None)
            #Убедимся, что высота такая, чтобы было что прокручивать.
            leftGrid.bind(minimum_height=leftGrid.setter('height'))
            ciphers = self.messageResponce.type_name_list

            self.toggle = [0 for _ in range(len(ciphers))]

            for index in range(len(ciphers)):
                self.toggle[index] = ToggleButton(
                    text=ciphers[index],  size_hint_y=None,
                    group='cipher', height=30*self.koef,
                    )
                self.toggle[index].bind(on_press=self.changer)
                leftGrid.add_widget(self.toggle[index])

            self.ids.ScrollWindowid.add_widget(leftGrid)
            self.listOfItems = False
        else:
            # удаляет все виджеты, которые находяться в another_box
            for i in range(len(self.ids.ScrollWindowid.children)):
                self.ids.ScrollWindowid.remove_widget(self.ids.ScrollWindowid.children[-1])
            self.listOfItems = True
            self.ids.Scrollbuttonid.text = "Просмотреть номенклатуру"

    def changer(self, *args):
        ciphers = self.messageResponce.type_name_list
        for i in range(len(ciphers)):
            if self.toggle[i].state == 'down':
                self.partName = ciphers[i]

        self.messageParameter.message = self.partName
        self.fourthTrigger = 3
        time.sleep(0.4)
        #Переход в конкретное описание детали
        self.manager.current = 'reportOfItem'
        #Переход окна вправо (текущее уходит влево)
        self.manager.transition.direction = "left"

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
        appEnvironment.WindowManagerObj.switch_to(appEnvironment.MainWindowObj, direction='right')

    def hostAdress(self):

        appEnvironment.host = self.PopupGrid.ids.host1.text
        appEnvironment.port = int(self.PopupGrid.ids.port1.text)