from client.applicationEnvironment import appEnvironment
from client.clientModule import MySocket
from kivy.lang import Builder
from kivy.factory import Factory

from client.windowClasses.smartAppClient import SmartAppClient
from client.windowClasses.loadDialog import LoadDialog
from client.windowClasses.fourthWindow import FourthWindow
from client.windowClasses.neiroClassWindow import NeiroClassWindow
from client.windowClasses.funcThread import FuncThread
from client.windowClasses.reportsWindowDetail import ReportsWindowDetail


class Bootstrap():

    @staticmethod
    def initEnviroment():
        appEnvironment.sock = MySocket()
        appEnvironment.koef = 1
        appEnvironment.kv = Builder.load_file("kvfiles/my.kv")
        #appEnvironment.LoadDialogObj = LoadDialog
        Factory.register('LoadDialog', cls=LoadDialog)
        #directory_kv_files = 'kvfiles'

        appEnvironment.SmartAppClientObj = SmartAppClient()

    @staticmethod
    def run():
        appEnvironment.SmartAppClientObj.run()

