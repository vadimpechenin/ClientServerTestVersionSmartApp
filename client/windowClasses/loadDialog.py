#Библиотеки для многих страниц
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

class LoadDialog(Screen):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)