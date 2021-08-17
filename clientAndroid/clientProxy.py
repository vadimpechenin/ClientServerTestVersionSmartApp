import socket
from threading import Lock
from clientModule import MySocket
from applicationEnvironment import appEnvironment
from common.socketHelper import SocketHelper

from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import weakref

class ClientProxy():

    def __init__(self):
        self.sock = None
        self.mutex_request = Lock()
        self.popup5 = None
        self.koef = appEnvironment.koef
        self.PopupGrid = None
        #self.isConnected = False
        #pass

    def connect(self):
        if self.isConnected():
            return True
        try:
            self.sock = MySocket(host=appEnvironment.host, port=appEnvironment.port)
        except:
            self.sock = None
        # self.isConnected = (self.sock != None)
        return (self.sock != None)  # self.isConnected

    def disconnect(self):
        if self.isConnected:
            self.sock.sock.close()
            self.sock = None

    def isConnected(self):
        return self.sock != None

    def sendRequest(self,messageParameter):
        self.mutex_request.acquire()
        try:
            self.sock.send_data(messageParameter)
            messageResponce = self.sock.get_data()
        except:
            #self.popupForSocket(appEnvironment.title, appEnvironment.text)
            messageResponce = None
        self.mutex_request.release()

        return messageResponce

    def popupForSocket(self):
        PopupGrid = GridLayout(rows=1, size_hint_y=None)
        PopupGrid.add_widget(Label(text='Сообщение не отправлено или не принят ответ'))

        popup4 = Popup(title='Ошибка', content=PopupGrid,
                            auto_dismiss=False, size_hint=(None, None),
                            size=(int(300 * appEnvironment.koef), int(200 * appEnvironment.koef)))
        content = Button(text='Закрыть')
        content.bind(on_press=self.popup4.dismiss())
        self.popup4.open()

    def configure(self, title, text):
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
        self.popup5 = Popup(title=title, content=PopupGrid,
                            auto_dismiss=False, size_hint=(None, None),
                            size=(int(300 * self.koef), int(200 * self.koef)))
        self.PopupGrid = PopupGrid
        content.bind(on_press=self.closePopupForSocket)
        self.popup5.open()

    def closePopupForSocket(self, *args):
        self.hostAdress()
        self.popup5.dismiss()

    def hostAdress(self):

        appEnvironment.host = self.PopupGrid.ids.host1.text
        appEnvironment.port = int(self.PopupGrid.ids.port1.text)
