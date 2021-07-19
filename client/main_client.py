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

# Для всплывающих окон
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

# Для размера окна
from kivy.core.window import Window

send_data=0
server_code = '00' #Специальный код, опеределяющий действия на сервере
filename_g = None
koef = 1
triggerPhoto1 = 1
ifTriggerPhotio1 = 3
triggerPhoto2 = 1

booleanPhoto = True

if (koef == 1):
    Window.size = (420, 800)
else:
    Window.size = (1100, 2300)

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
        self.popup = None
        self.popup1 = None

    def ImageLoad(self,path, filename):
        global filename_g, triggerPhoto1, ifTriggerPhotio1
        data = io.BytesIO(open(filename[0], "rb").read())
        # data = io.BytesIO(open("IMAGE.jpg", "rb").read())
        im = CoreImage(data, ext="png")
        if ifTriggerPhotio1==1:

            filename_g = filename[0]
        else:

            filename_g.append(filename[0])

        self.ids.ImageBoxId.add_widget(Image(texture=im.texture))


    def ImageDel(self):
        # удаляет все виджеты, которые находяться в another_box
        for i in range(len(self.ids.ImageBoxId.children)):
            self.ids.ImageBoxId.remove_widget(self.ids.ImageBoxId.children[-1])

    def ImageSent(self):
        # Отправляет картинку
        global send_data
        global filename_g
        global server_code
        send_data = 1
        #server_code = '10'

    # Функции для загрузки файлов

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load_main(self):
        global triggerPhoto1, ifTriggerPhotio1, booleanForPopup

        self.btn()

    def show_load(self):
        global filename_g, booleanPhoto, triggerPhoto1
        if booleanPhoto==True:
            if (ifTriggerPhotio1==1):
                filename_g = None
            elif (ifTriggerPhotio1==3):
                filename_g = []
                triggerPhoto1 = 2
            booleanPhoto = False
        print(triggerPhoto1)
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        global ifTriggerPhotio1, triggerPhoto1, triggerPhoto2
        #with open(join(path, filename[0])) as stream:
        #    self.text_input.text = stream.read()

        self.dismiss_popup()
        self.ImageLoad(path, filename)
        if (ifTriggerPhotio1 == 3) and (triggerPhoto1>0):
            triggerPhoto1 -=1
            triggerPhoto2 +=1
            self.imgPress()


    def get_data(self):
        global send_data
        global filename_g
        global server_code
        while True:
            time.sleep(0.1)
            if (send_data==1):
                self.sock.get_data(filename_g,server_code)
                send_data=0

    # Блок с всплывающими окнами
    # Включение всплывающего окна
    def btn(self, *args):
        # create content and add to the popup
        global booleanPhoto
        booleanPhoto = True
        PopupGrid = GridLayout(cols=2, size_hint_y=None)
        content2 = Button(text='QR', halign='left', size_hint=(0.4, 0.1), pos_hint={'x': 0.1, 'top': 0.1})
        PopupGrid.add_widget(content2)
        content3 = Button(text='Изображение', halign='left', size_hint=(0.4, 0.1), pos_hint={'x': 0.1, 'top': 0.1})
        PopupGrid.add_widget(content3)

        self.popup = Popup(title='Сделайте выбор', title_align='center', content=PopupGrid, auto_dismiss=False,
                           size_hint=(None, None), size=(int(300 * koef), int(200 * koef)))
        # bind the on_press event of the button to the dismiss function
        #
        content2.bind(on_press=self.QRPress)  # self.QRPress()
        content3.bind(on_press=self.imgPress)
        # open the popup
        self.popup.open()

    def QRPress(self, *args):
        global ifTriggerPhotio1
        global server_code
        print("QR")
        server_code = '10'
        self.popup.dismiss()
        ifTriggerPhotio1 = 1
        PopupGrid = GridLayout(cols=1, pos_hint={'center_x': 0.6, 'center_y': 0.32})
        content4 = Button(text='Закрыть', halign='center', size= (int(200 * koef), int(50 * koef)),
                          size_hint=(None, None), pos = (int(50 * koef), int(50 * koef)), pos_hint=(None, None))
        PopupGrid.add_widget(content4)
        self.popup1 = Popup(title='Считайте QR', title_align='center', content =PopupGrid, auto_dismiss=False,
                            size_hint=(None, None), pos_hint={"center_x": 0.5, "top": 0.32},
                            size=(int(300 * koef), int(120 * koef)))
        content4.bind(on_press=self.closePopup)
        self.popup1.open()


    def imgPress(self, *args):
        global ifTriggerPhotio1, triggerPhoto1, triggerPhoto2
        global server_code
        print("Изображение")
        server_code = '11'
        self.popup.dismiss()
        ifTriggerPhotio1 = 3
        PopupGrid = GridLayout(cols=1, pos_hint={'center_x': 0.6, 'center_y': 0.32})
        content4 = Button(text='Закрыть', halign='center', size= (int(200 * koef), int(50 * koef)),
                          size_hint=(None, None), pos = (int(50 * koef), int(50 * koef)), pos_hint=(None, None))
        PopupGrid.add_widget(content4)
        self.popup1 = Popup(title='Выберите фото с ' + str(triggerPhoto2) + ' ракурса', title_align='center', content =PopupGrid, auto_dismiss=False,
                            size_hint=(None, None), pos_hint={"center_x": 0.5, "top": 0.32},
                            size=(int(300 * koef), int(120 * koef)))
        #content4.bind(on_press=self.popup1.dismiss)
        content4.bind(on_press=self.closePopup)
        self.popup1.open()

    def closePopup(self, *args):
        self.popup1.dismiss()
        self.show_load()


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