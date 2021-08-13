
#Библиотеки для многих страниц
from kivy.uix.screenmanager import Screen
# Для всплывающих окон
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
import time

from client.applicationEnvironment import appEnvironment

triggerPhoto = 1
ifTriggerPhotio = 3
koef = 1


class NeiroClassWindow(Screen):
    global triggerPhoto
    #Класс для создания фото, чтобы их потом загрузить в нейросеть для классификации и идентификации.
    def __init__(self, *args, **kwargs):
        super(NeiroClassWindow, self).__init__(*args, **kwargs)
        self.fileName = None
        self.camera = None
        self.popup = None
        self.popup1 = None
        appEnvironment.NeiroClassWindowObj = self

    #Включение всплывающего окна
    def btn(self,*args):
        # create content and add to the popup
        PopupGrid = GridLayout(cols=2, size_hint_y=None)
        content2 = Button(text='QR', halign='left', size_hint=(0.4, 0.1), pos_hint={'x': 0.1, 'top': 0.1})
        PopupGrid.add_widget(content2)
        content3 = Button(text='Изображение', halign='left', size_hint=(0.4, 0.1), pos_hint={'x': 0.1, 'top': 0.1})
        PopupGrid.add_widget(content3)

        self.popup = Popup(title='Сделайте выбор', title_align = 'center', content=PopupGrid, auto_dismiss=False, size_hint=(None, None), size=(int(300*koef), int(200*koef)))
        # bind the on_press event of the button to the dismiss function
        #
        content2.bind(on_press=self.QRPress)#self.QRPress()
        content3.bind(on_press=self.imgPress)
        # open the popup
        self.popup.open()

    def initCamera(self):
        self.camera = self.ids.camera
        self.camera.resolution = (640, 480)
        self.camera.keep_ratio = True
        self.camera.play = False
        self.camera.allow_stretch = True

    def on_enter(self, *args):
        self.initCamera()

    def capturePhoto(self):
        global triggerPhoto, ifTriggerPhotio
        imgTime = time.strftime("%m_%d_%Y_%I_%M_%S_%p") #        imgTime = time.strftime("%m_%d_%Y_%I_%M_%p") #

        self.fileName = "IMG_{}.png".format(imgTime)
        self.camera.export_to_png(self.fileName)
        print("Выполнено фотографирование")
        triggerPhoto +=1
        if (triggerPhoto<=ifTriggerPhotio):
            PopupGrid = GridLayout(cols=1, pos_hint={'center_x': 0.6, 'center_y': 0.32})
            content4 = Button(text='Закрыть', halign='center', size=(int(200 * koef), int(50 * koef)),
                              size_hint=(None, None), pos=(int(50 * koef), int(50 * koef)),
                              pos_hint=(None, None))  # size_hint=(0.1, 0.01),pos_hint={'x': 0.1, 'top': 0.5}
            PopupGrid.add_widget(content4)
            self.popup1 = Popup(title='Сделайте фото ' + str(triggerPhoto) + ' ракурса', title_align='center', content=PopupGrid,
                                auto_dismiss=False,
                                size_hint=(None, None), pos_hint={"center_x": 0.5, "top": 0.32},
                                size=(int(300 * koef), int(120 * koef)))
            content4.bind(on_press=self.popup1.dismiss)
            self.popup1.open()
        else:
            #self.popup1.dismiss()
            triggerPhoto = 1
            self.btn()

    def QRPress(self, *args):
        global ifTriggerPhotio
        print("QR")
        self.popup.dismiss()
        ifTriggerPhotio = 1
        PopupGrid = GridLayout(cols=1, pos_hint={'center_x': 0.6, 'center_y': 0.32})
        content4 = Button(text='Закрыть', halign='center', size= (int(200 * koef), int(50 * koef)),
                          size_hint=(None, None), pos = (int(50 * koef), int(50 * koef)), pos_hint=(None, None))
        PopupGrid.add_widget(content4)
        self.popup1 = Popup(title='Считайте QR', title_align='center', content =PopupGrid, auto_dismiss=False,
                            size_hint=(None, None), pos_hint={"center_x": 0.5, "top": 0.32},
                            size=(int(300 * koef), int(120 * koef)))
        content4.bind(on_press=self.popup1.dismiss)
        self.popup1.open()


    def imgPress(self, *args):
        global ifTriggerPhotio, triggerPhoto
        print("изображение")
        self.popup.dismiss()
        ifTriggerPhotio = 3
        PopupGrid = GridLayout(cols=1, pos_hint={'center_x': 0.6, 'center_y': 0.32})
        content4 = Button(text='Закрыть', halign='center', size= (int(200 * koef), int(50 * koef)),
                          size_hint=(None, None), pos = (int(50 * koef), int(50 * koef)), pos_hint=(None, None))
        PopupGrid.add_widget(content4)
        self.popup1 = Popup(title='Сделайте фото с ' + str(triggerPhoto) + ' ракурса', title_align='center', content =PopupGrid, auto_dismiss=False,
                            size_hint=(None, None), pos_hint={"center_x": 0.5, "top": 0.32},
                            size=(int(300 * koef), int(120 * koef)))
        content4.bind(on_press=self.popup1.dismiss)
        self.popup1.open()
