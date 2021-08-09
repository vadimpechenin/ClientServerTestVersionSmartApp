from client.applicationEnvironment import appEnvironment
from client.clientModule import MySocket
from kivy.lang import Builder
from kivy.factory import Factory
# Для размера окна
from kivy.core.window import Window

from client.windowClasses.smartAppClient import SmartAppClient
from client.windowClasses.fourthWindow import FourthWindow
from client.windowClasses.neiroClassWindow import NeiroClassWindow
from client.windowClasses.funcThread import FuncThread
from client.windowClasses.reportsWindowDetail import ReportsWindowDetail
from client.windowClasses.qrWindow import QRWindow
from client.windowClasses.reportsWindow import ReportsWindow
from client.windowClasses.filterWindow import FilterWindow
from client.windowClasses.mainReport import MainReport
from client.windowClasses.fileChoose import FileChoose

from client.windowClasses.windowManager import WindowManager
from client.windowClasses.mainWindow import MainWindow

class Bootstrap():

    @staticmethod
    def initEnviroment():
        appEnvironment.sock = MySocket()
        appEnvironment.koef = 1
        if (appEnvironment.koef == 1):
            Window.size = (420, 800)
        else:
            Window.size = (1100, 2300)

        appEnvironment.kv = Builder.load_file("kvfiles/my.kv")
        #appEnvironment.LoadDialogObj = LoadDialog
        #Factory.register('LoadDialog', cls=LoadDialog)
        #directory_kv_files = 'kvfiles'

        appEnvironment.SmartAppClientObj = SmartAppClient()

    @staticmethod
    def run():
        appEnvironment.SmartAppClientObj.run()

