#kivy-приложение
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

import time
from client.clientModule import MySocket
from os.path import dirname, join, basename, isfile
from os import listdir
from threading import Thread


#Библиотека для всплывающих окон
from kivy.uix.popup import Popup
import io
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage

#Библиотеки для многих страниц
from kivy.uix.screenmanager import ScreenManager, Screen

#Для чтения файлов с диска
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.factory import Factory

send_data=0
filename_g = None

# Классы для окон
class WindowManager(ScreenManager):
    pass

class MainWindow(Screen):
    pass


class LoadDialog(Screen):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class QRWindow(Screen):
    # Класс для работы по отсылке фотографий
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(QRWindow, self).__init__(*args, **kwargs)
        self.sock = MySocket()
        Thread(target=self.get_data).start()

    def ImageLoad(self,path, filename):
        global filename_g
        data = io.BytesIO(open(filename[0], "rb").read())
        #data = io.BytesIO(open("IMAGE.jpg", "rb").read())
        im = CoreImage(data, ext="png")
        filename_g = filename[0]
        self.ids.ImageBoxId.add_widget(Image(texture=im.texture))


    def ImageDel(self):
        # удаляет все виджеты, которые находяться в another_box
        for i in range(len(self.ids.ImageBoxId.children)):
            self.ids.ImageBoxId.remove_widget(self.ids.ImageBoxId.children[-1])

    def ImageSent(self):
        # Отправляет картинку
        global send_data
        global filename_g
        send_data = 1


    #Для загрузки файлов

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        #with open(join(path, filename[0])) as stream:
        #    self.text_input.text = stream.read()

        self.dismiss_popup()
        self.ImageLoad(path, filename)

    def get_data(self):
        global send_data
        global filename_g
        while True:
            time.sleep(0.1)
            if (send_data==1):
                self.sock.get_data(filename_g)
                send_data=0
class CameraClick(Screen):

    def __init__(self, **kwargs):
        #send_data = 0
        super(CameraClick, self).__init__(**kwargs)
        self.fileName = None
        self.camera = None
        #self.sock = MySocket()
        #Thread(target=self.get_data).start()

    def initCamera(self):
        self.camera = self.ids.camera
        self.camera.resolution = (640, 480)
        self.camera.keep_ratio = True
        self.camera.play = False
        self.camera.allow_stretch = True

    def on_enter(self, *args):
        self.initCamera()

    def capturePhoto(self):
        #global send_data
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        # Изменение для сохранения в папку
        b = basename('IMG_{}.png')
        #b = basename('image.jpg')
        DCIM = join(b) #'DCIM'
        camera.export_to_png(DCIM.format(timestr))
        #camera.export_to_png(DCIM)
        print("Captured")
        #send_data = 1


kv = Builder.load_file("kvfiles/my.kv")

class TestCamera(App):

    def build(self):
        return kv
        #return CameraClick()

    # Метод для кодировки русских символов в описании
    def load_all_kv_files(self, directory_kv_files):
        for kv_file in listdir(directory_kv_files):
            kv_file = join(directory_kv_files, kv_file)
            if isfile(kv_file) and kv_file.endswith("kv"):
                with open(kv_file, encoding="utf-8") as kv:
                    Builder.load_string(kv.read())

Factory.register('LoadDialog', cls=LoadDialog)

if __name__ == '__main__':
    #TestCamera().run()
    directory_kv_files = 'kvfiles'
    TestCamera().load_all_kv_files(directory_kv_files)
    TestCamera().run()