# Менеджер перехода между страницами и передачи данных
from kivy.uix.screenmanager import ScreenManager
from client.applicationEnvironment import appEnvironment

class WindowManager(ScreenManager):
    def __init__(self, *args, **kwargs):
        super(WindowManager, self).__init__(*args, **kwargs)
        appEnvironment.WindowManagerObj = self