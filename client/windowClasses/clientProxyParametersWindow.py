from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

from client.applicationEnvironment import appEnvironment

from message.clientProxyParameters import ClientProxyParameters

import weakref

from threading import Lock, Thread


class ClientProxyParametersWindow():
    #Окно для редактирования параметров

    def __init__(self):
        self.value = ClientProxyParameters()
        self.isOK = False
        self.koef = appEnvironment.koef
        self.popup5 = None
        self.endCallback = None
        self.configure()

    def execute(self, clientProxyParameters, endCallback):
        self.value.copyFrom(clientProxyParameters)
        self.endCallback = endCallback
        self.isOK = False
        self.configure()

    def configure(self):
        title = 'Параметры сервера'
        PopupGrid = GridLayout(rows=4, size_hint_y=None)
        #PopupGrid.add_widget(Label(text=text))

        host1 = TextInput()
        PopupGrid.add_widget(host1)  #
        PopupGrid.ids['host1'] = weakref.ref(host1)
        PopupGrid.ids.host1.text = self.value.HOST
        PopupGrid.ids.host1.multiline = True

        port1 = TextInput()
        PopupGrid.add_widget(port1)  #
        PopupGrid.ids['port1'] = weakref.ref(port1)
        PopupGrid.ids.port1.text = str(self.value.PORT)
        PopupGrid.ids.port1.multiline = True

        contentClose = Button(text='Закрыть')
        PopupGrid.add_widget(contentClose)

        contentCancel = Button(text='Отменить')
        PopupGrid.add_widget(contentCancel)

        self.popup5 = Popup(title=title, content=PopupGrid,
                            auto_dismiss=False, size_hint=(None, None),
                            size=(int(300 * self.koef), int(200 * self.koef)))

        self.PopupGrid = PopupGrid
        contentClose.bind(on_press=self.okWindow)
        contentCancel.bind(on_press=self.cancelWindow)
        #self.popup5.open()


    def cancelWindow(self, *args):
        self.isOK = False
        self.popup5.dismiss()
        self.endCallback(self.isOK, self.value)


    def okWindow(self, *args):
        self.isOK = True
        self.value.HOST = self.PopupGrid.ids.host1.text
        self.value.PORT = int(self.PopupGrid.ids.port1.text)
        self.popup5.dismiss()
        self.endCallback(self.isOK, self.value)

