from kivy.uix.screenmanager import Screen
from client.applicationEnvironment import appEnvironment

class MainWindow(Screen):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.listOfItemsView = 0  # Переменная для обмена сообщениями с сервером в части отчетов
        self.fourthTrigger = 0
        appEnvironment.MainWindowObj = self


    def triggerForServer(self):
        # Метод для изменения переменных, отвечающих за запуск потока общения с сервером
        self.listOfItemsView = 2
        appEnvironment.ReportsWindowObj.fillData(self.listOfItemsView)

    def triggerForServerFourth(self):
        # Метод для загрузки списка номенклатуры в окне Номенклатура
        self.fourthTrigger = 1
        appEnvironment.FourthWindowObj.fillData(self.fourthTrigger)