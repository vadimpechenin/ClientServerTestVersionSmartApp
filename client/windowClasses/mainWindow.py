from kivy.uix.screenmanager import Screen
from client.applicationEnvironment import appEnvironment

from client.windowClasses.clientProxyParametersWindow import ClientProxyParametersWindow
from message.clientProxyParameters import ClientProxyParameters

from threading import Thread

import time

from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import weakref

class MainWindow(Screen):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.listOfItemsView = 0  # Переменная для обмена сообщениями с сервером в части отчетов
        self.fourthTrigger = 0
        self.send_data = 0
        self.popup6 = None
        self.index = 0
        Thread(target=self.testConnection).start()
        self.koef = appEnvironment.koef
        appEnvironment.MainWindowObj = self

    #Проверка нажатия на кнопку
    def on_press(self, index):
        flash_display_screen = self.manager.get_screen('flash_display')
        setattr(flash_display_screen, 'index', index)
        self.manager.current = 'flash_display'

    def testConnection(self):
        while True:
            time.sleep(0.3)
            if (self.send_data==1):
                if appEnvironment.ClientProxyObj.connect():
                    self.popupForSocketYes()

                    #time.sleep(8)
                    #self.send_data = 0
                else:
                    self.popupForSocketNone()
                    #time.sleep(8)
                if (self.index == 1):
                    self.triggerForServerFourth()
                elif (self.index == 2):
                    self.triggerForServer()
                self.index= 0
                self.send_data = 0


    def triggerConnection(self, index):
        self.send_data = 1
        self.index = index
    """
    def testeMethod(self):
        parameters= ClientProxyParameters()
        parameters.HOST = appEnvironment.host
        parameters.PORT = appEnvironment.port
        window = ClientProxyParametersWindow()
        isOK = window.execute(parameters, self.testeMethodEndCallback)

    def testeMethodEndCallback(self, result, parameters):
        if result:
            appEnvironment.host = parameters.HOST
            appEnvironment.port = parameters.PORT
        else:
            ddd = 0


        
        if isOK:
            appEnvironment.host = parameters.HOST
            appEnvironment.port = parameters.PORT
        else:
            t = 1
        """
    def triggerForServer(self):
        # Метод для изменения переменных, отвечающих за запуск потока общения с сервером
        self.listOfItemsView = 2
        appEnvironment.ReportsWindowObj.fillData(self.listOfItemsView)

    def triggerForServerFourth(self):
        # Метод для загрузки списка номенклатуры в окне Номенклатура
        self.fourthTrigger = 1
        appEnvironment.FourthWindowObj.fillData(self.fourthTrigger)

    def popupForSocketNone(self):
        PopupGrid = GridLayout(rows=2, size_hint_y=None)
        PopupGrid.add_widget(Label(text='Соединение отсутствует'))
        content = Button(text='Закрыть')
        PopupGrid.add_widget(content)
        self.popup6 = Popup(title='Ошибка', content=PopupGrid,
                            auto_dismiss=False, size_hint=(None, None),
                            size=(int(300 * appEnvironment.koef), int(200 * appEnvironment.koef)))

        content.bind(on_press=self.popup6.dismiss)
        self.popup6.open()

    def popupForSocketYes(self):
        PopupGrid = GridLayout(rows=2, size_hint_y=None)
        PopupGrid.add_widget(Label(text='Соединение есть'))
        content = Button(text='Закрыть')
        PopupGrid.add_widget(content)
        self.popup6 = Popup(title='Успех', content=PopupGrid,
                            auto_dismiss=False, size_hint=(None, None),
                            size=(int(300 * appEnvironment.koef), int(200 * appEnvironment.koef)))

        content.bind(on_press=self.popup6.dismiss)
        self.popup6.open()