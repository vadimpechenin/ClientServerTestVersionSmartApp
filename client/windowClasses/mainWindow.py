from kivy.uix.screenmanager import Screen
from client.applicationEnvironment import appEnvironment

from client.windowClasses.clientProxyParametersWindow import ClientProxyParametersWindow
from message.clientProxyParameters import ClientProxyParameters

class MainWindow(Screen):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.listOfItemsView = 0  # Переменная для обмена сообщениями с сервером в части отчетов
        self.fourthTrigger = 0
        appEnvironment.MainWindowObj = self

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


        """
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