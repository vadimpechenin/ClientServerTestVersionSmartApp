#kivy-приложение
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time
from client.clientModule import MySocket
from os.path import dirname, join, basename, isfile
from os import listdir
from threading import Thread

#Библиотеки для многих страниц
from kivy.uix.screenmanager import ScreenManager, Screen

send_data=0

# Классы для окон
class WindowManager(ScreenManager):
    pass

class MainWindow(Screen):
    pass

class CameraClick(Screen):

    def __init__(self, **kwargs):
        #send_data = 0
        super(CameraClick, self).__init__(**kwargs)
        self.fileName = None
        self.camera = None
        self.sock = MySocket()
        Thread(target=self.get_data).start()

    def initCamera(self):
        self.camera = self.ids.camera
        self.camera.resolution = (640, 480)
        self.camera.keep_ratio = True
        self.camera.play = False
        self.camera.allow_stretch = True

    def on_enter(self, *args):
        self.initCamera()

    def capturePhoto(self):
        global send_data
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        # Изменение для сохранения в папку
        #b = basename('IMG_{}.png')
        b = basename('image.jpg')
        DCIM = join(b) #'DCIM'
        #camera.export_to_png(DCIM.format(timestr))
        camera.export_to_png(DCIM)
        print("Captured")
        send_data = 1

    def get_data(self):
        global send_data
        while True:
            time.sleep(0.1)
            if (send_data==1):
                self.sock.get_data()
                send_data=0

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

if __name__ == '__main__':
    #TestCamera().run()
    directory_kv_files = 'kvfiles'
    TestCamera().load_all_kv_files(directory_kv_files)
    TestCamera().run()