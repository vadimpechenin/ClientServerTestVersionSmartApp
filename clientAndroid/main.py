# -*- coding: utf-8 -*-

"""
Мобильное приложение для умного склада. Идентификация деталей, отслеживание их жизненного цикла
"""
from __future__ import unicode_literals
from kivy.utils import platform
from plyer import filechooser

from os.path import getsize, join, basename

from kivy.app import App
#Для кодировки
import os
from kivy.lang.builder import Builder

#Библиотеки для многих страниц
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
#Библиотека для всплывающих окон
from kivy.uix.popup import Popup
import io
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.textinput import TextInput

import time

# Для размера окна
from kivy.core.window import Window

from applicationEnvironment import appEnvironment

koef = appEnvironment.koef #3


if (appEnvironment.koef == 1):
    Window.size = (420, 800)
else:
    Window.size = (1100, 2300)


import weakref
from threading import Thread
from clientProxy import ClientProxy

# Библиотеки для формирования структуры пересылаемого сообщения
from message.messageStructure import MessageStructure
from message.messageStructureParameter import MessageStructureParameter
from message.messageResponceParameter import MessageResponceParameter

triggerPhoto = 1
ifTriggerPhotio = 3

# Классы для окон
class MainWindow(Screen):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.listOfItemsView = 0  # Переменная для обмена сообщениями с сервером в части отчетов
        self.fourthTrigger = 0
        self.send_data = 0
        self.popup6 = None
        self.index = 0
        Thread(target=self.testConnection).start()
        self.koef = appEnvironment.koef

    def testConnection(self):
        while True:
            time.sleep(0.3)
            if (self.send_data == 1):
                if appEnvironment.ClientProxyObj.connect():
                    self.popupForSocketYes()
                    # time.sleep(8)
                    # self.send_data = 0
                else:
                    self.popupForSocketNone()
                    # time.sleep(8)

                #appEnvironment.ClientProxyObj.disconnect()
                if (self.index == 1):
                    self.triggerForServerFourth()
                elif (self.index == 2):
                    self.triggerForServer()
                self.send_data = 0


    def triggerConnection(self, index):
        self.send_data = 1
        self.index = index

    def triggerForServer(self):
        # Метод для изменения переменных, отвечающих за запуск потока общения с сервером
        appEnvironment.listOfItemsView = 2
        #appEnvironment.ReportsWindowObj.fillData(self.listOfItemsView)

    def triggerForServerFourth(self):
        # Метод для загрузки списка номенклатуры в окне Номенклатура
        appEnvironment.fourthTrigger = 1
        #appEnvironment.FourthWindowObj.fillData(self.fourthTrigger)

    def popupForSocketNone(self):
        PopupGrid = GridLayout(rows=2, size_hint_y=None)
        PopupGrid.add_widget(Label(text='Соединение отсутствует'))
        content = Button(text='Закрыть')
        PopupGrid.add_widget(content)
        self.popup6 = Popup(title='Ошибка', content=PopupGrid,
                            auto_dismiss=False, size_hint=(None, None),
                            size=(int(300 * appEnvironment.koef), int(200 * appEnvironment.koef)))

        content.bind(on_press=self.popup6.dismiss)
        self.popup6.open()

    def popupForSocketYes(self):
        PopupGrid = GridLayout(rows=2, size_hint_y=None)
        PopupGrid.add_widget(Label(text='Соединение есть'))
        content = Button(text='Закрыть')
        PopupGrid.add_widget(content)
        self.popup6 = Popup(title='Успех', content=PopupGrid,
                            auto_dismiss=False, size_hint=(None, None),
                            size=(int(300 * appEnvironment.koef), int(200 * appEnvironment.koef)))

        content.bind(on_press=self.popup6.dismiss)
        self.popup6.open()

class NeiroClassWindow(Screen):
    global triggerPhoto
    #Класс для создания фото, чтобы их потом загрузить в нейросеть для классификации и идентификации.
    def __init__(self, *args, **kwargs):
        super(NeiroClassWindow, self).__init__(*args, **kwargs)
        self.fileName = None
        self.camera = None
        self.popup = None
        self.popup1 = None

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
        imgTime = time.strftime("%m_%d_%Y_%I_%M_%S_%p")
        b = basename('IMG_{}.jpg')
        self.fileName = "IMG_{}.jpg".format(imgTime)

        if platform == 'android':
            base_dir = '/storage/emulated/0/DCIM'
        else:
            base_dir = '/'
        #base_dir = '/storage/emulated/0/DCIM'
        photo_file_name = join(base_dir, b)
        photo_file_name=photo_file_name.format(imgTime)
        self.camera.export_to_png(photo_file_name)
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


class QRWindow(Screen):
    # Класс для считывания QR, или загрузки изображения для считывания QR
    def __init__(self, *args, **kwargs):
        super(QRWindow, self).__init__(*args, **kwargs)
        Thread(target=self.get_data).start()
        # Объект - запрос на сервер
        self.messageParameter = MessageStructureParameter()
        # Объект - ответ с сервера
        self.messageResponce = MessageResponceParameter()
        self.popup = None
        self.popup1 = None
        self.popup2 = None
        self.popup3 = None
        self.popup4 = None
        self.popup6 = None

        self.send_data = 0
        self.code_request0 = 0  # Специальный код, опеределяющий действия на сервере
        self.code_request1 = 0  # Специальный код, опеределяющий QR или NN
        self.filename_g = None
        self.triggerPhoto1 = 1
        self.ifTriggerPhotio1 = 3
        self.triggerPhoto2 = 1
        self.workshop_number_list = []
        self.lot_number_list = []
        self.type_list = []
        self.booleanPhoto = True
        self.boolWorkchopLot = True

        self.koef = appEnvironment.koef
        self.PopupGrid = None
        appEnvironment.QRWindowObj = self
        #self.FileChooseObj = FileChoose()

    def ImageLoad(self, path, filename):
        try:
            data = io.BytesIO(open(filename[0], "rb").read())
        except:
            self.popupForSocketNoBytes()
        else:
            try:
                im = CoreImage(data, ext="png")
            except:
                self.popupForSocketNoImageCore()

        if self.ifTriggerPhotio1 == 1:

            self.filename_g = filename[0]
            # Запись информации о дате для детали
            if (self.messageParameter.code_request0) == 2:
                reversed_name_of_data = ''
                reversed_string = ''
                if (len(filename[0]) >= 22):
                    for i in range(22):
                        reversed_name_of_data = reversed_name_of_data + filename[0][-i - 5]
                    reversed_string = reversed_name_of_data[::-1]
                self.messageParameter.nameOfImage = reversed_string
        else:

            self.filename_g.append(filename[0])

        # file = cv2.imread(filename[0]) #Библеотека opencv не работает на android

        sizeOfImage = getsize(filename[0])

        self.messageParameter.Images.append(data)
        self.messageParameter.sizeOfImages.append(sizeOfImage)

        #self.ids.ImageBoxId.add_widget(Image(texture=im.texture))
        self.ids.ImageBoxId.add_widget(Image(texture=im.texture))

    def ImageDel(self):
        # удаляет все виджеты, которые находяться в another_box
        for i in range(len(self.ids.ImageBoxId.children)):
            self.ids.ImageBoxId.remove_widget(self.ids.ImageBoxId.children[-1])

    def ImageSent(self):
        # Отправляет картинку
        self.send_data = 1

    # Функции для загрузки файлов

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load_main(self):

        self.btn()

    def show_load(self):
        if self.booleanPhoto == True:
            if (self.ifTriggerPhotio1 == 1):
                self.filename_g = None
            elif (self.ifTriggerPhotio1 == 3):
                self.filename_g = []
                self.triggerPhoto1 = 2
            self.booleanPhoto = False
        print(self.triggerPhoto1)
        #self.FileChooseObj.clear_selection()
        #self.FileChooseObj.choose()
        #self.load(self.FileChooseObj.selection, self.FileChooseObj.selection)
        # Переход в конкретное описание детали
        self.manager.current = 'filechoose'
        # Переход окна вправо (текущее уходит влево)
        self.manager.transition.direction = "left"


    def load(self, path, filename):
        # self.dismiss_popup()
        self.ImageLoad(path, filename)
        if (self.ifTriggerPhotio1 == 3) and (self.triggerPhoto1 > 0):
            self.triggerPhoto1 -= 1
            self.triggerPhoto2 += 1
            self.imgPress()

    def get_data(self):
        while True:
            time.sleep(0.3)
            if (self.send_data == 1):
                if appEnvironment.ClientProxyObj.connect():
                    self.messageResponce = appEnvironment.ClientProxyObj.sendRequest(self.messageParameter)
                    if self.messageResponce != None:
                        self.send_data = 0
                        if (self.messageResponce.message == 'Изображение пришло'):
                            self.Responce_name_detail_popup()
                        elif (self.messageResponce.message == 'Список возможных месторасположений детали'):
                            self.Responce_location_popup()
                        elif (self.messageResponce.message == 'Изменения внесены'):
                            self.Responce_name_detail_popup()
                    else:
                        self.popupForSocketNone()
                        self.send_data = 0

                    self.messageParameter = MessageStructure.ClearObject(self.messageParameter)
                    appEnvironment.ClientProxyObj.disconnect()
                else:
                    self.popupForSocket(appEnvironment.title, appEnvironment.text)
                    self.send_data = 0

            if (appEnvironment.triggerSelectImage == 1):
                try:
                    self.load(appEnvironment.filenameEnv, appEnvironment.filenameEnv)
                except:
                    self.popupForSocketNo()
                appEnvironment.triggerSelectImage = 0

    # Блок с всплывающими окнами
    # Включение всплывающего окна
    def btn(self, *args):
        # create content and add to the popup
        self.booleanPhoto = True
        self.triggerPhoto2 = 1
        self.ImageDel()
        PopupGrid = GridLayout(cols=2, size_hint_y=None)
        content2 = Button(text='QR', halign='left', size_hint=(0.4, 0.1), pos_hint={'x': 0.1, 'top': 0.1})
        PopupGrid.add_widget(content2)
        content3 = Button(text='Изображение', halign='left', size_hint=(0.4, 0.1), pos_hint={'x': 0.1, 'top': 0.1})
        PopupGrid.add_widget(content3)

        self.popup = Popup(title='Сделайте выбор', title_align='center', content=PopupGrid, auto_dismiss=False,
                           size_hint=(None, None), size=(int(300 * self.koef), int(200 * self.koef)))
        # bind the on_press event of the button to the dismiss function
        #
        content2.bind(on_press=self.QRPress_main)  # self.QRPress()
        content3.bind(on_press=self.imgPress)
        # open the popup
        self.popup.open()

    def QRPress_main(self, *args):
        print("QR")
        self.popup.dismiss()
        PopupGrid = GridLayout(cols=2, size_hint_y=None)
        content2 = Button(text='Тип детали', halign='left', size_hint=(0.4, 0.1), pos_hint={'x': 0.1, 'top': 0.1})
        PopupGrid.add_widget(content2)
        content3 = Button(text='Запись в базу', halign='left', size_hint=(0.4, 0.1), pos_hint={'x': 0.1, 'top': 0.1})
        PopupGrid.add_widget(content3)

        self.popup2 = Popup(title='Сделайте выбор', title_align='center', content=PopupGrid, auto_dismiss=False,
                            size_hint=(None, None), size=(int(300 * self.koef), int(200 * self.koef)))
        # bind the on_press event of the button to the dismiss function
        #
        content2.bind(on_press=self.QRPress_type)  # self.QRPress()
        content3.bind(on_press=self.QRPress_base_location_list)
        # open the popup
        self.popup2.open()

    def QRPress_type(self, *args):
        print("QR type")
        self.messageParameter.code_request0 = 1
        self.messageParameter.code_request1 = 0
        self.popup2.dismiss()
        self.ifTriggerPhotio1 = 1
        PopupGrid = GridLayout(cols=1, pos_hint={'center_x': 0.6, 'center_y': 0.32})
        content4 = Button(text='Закрыть', halign='center', size=(int(200 * self.koef), int(50 * self.koef)),
                          size_hint=(None, None), pos=(int(50 * self.koef), int(50 * self.koef)), pos_hint=(None, None))
        PopupGrid.add_widget(content4)
        self.popup1 = Popup(title='Считайте QR', title_align='center', content=PopupGrid, auto_dismiss=False,
                            size_hint=(None, None), pos_hint={"center_x": 0.5, "top": 0.32},
                            size=(int(300 * self.koef), int(120 * self.koef)))
        content4.bind(on_press=self.closePopup)
        self.popup1.open()

    def QRPress_base_location_list(self, *args):
        print("QR base")
        self.messageParameter.code_request0 = 3
        self.messageParameter.code_request1 = 0
        time.sleep(0.2)
        self.send_data = 1
        self.popup2.dismiss()

    def QRPress_base(self, *args):
        print("QR base")
        self.messageParameter.code_request0 = 2
        self.messageParameter.code_request1 = 0
        self.ifTriggerPhotio1 = 1
        PopupGrid = GridLayout(cols=1, pos_hint={'center_x': 0.6, 'center_y': 0.32})
        content4 = Button(text='Закрыть', halign='center', size=(int(200 * self.koef), int(50 * self.koef)),
                          size_hint=(None, None), pos=(int(50 * self.koef), int(50 * self.koef)), pos_hint=(None, None))
        PopupGrid.add_widget(content4)
        self.popup1 = Popup(title='Считайте QR', title_align='center', content=PopupGrid, auto_dismiss=False,
                            size_hint=(None, None), pos_hint={"center_x": 0.5, "top": 0.32},
                            size=(int(300 * self.koef), int(120 * self.koef)))
        content4.bind(on_press=self.closePopup)
        self.popup1.open()

    def imgPress(self, *args):
        print("Изображение")
        self.messageParameter.code_request0 = 1
        self.messageParameter.code_request1 = 1
        self.popup.dismiss()
        self.ifTriggerPhotio1 = 3
        PopupGrid = GridLayout(cols=1, pos_hint={'center_x': 0.6, 'center_y': 0.32})
        content4 = Button(text='Закрыть', halign='center', size=(int(200 * self.koef), int(50 * self.koef)),
                          size_hint=(None, None), pos=(int(50 * self.koef), int(50 * self.koef)), pos_hint=(None, None))
        PopupGrid.add_widget(content4)
        self.popup1 = Popup(title='Выберите фото с ' + str(self.triggerPhoto2) + ' ракурса', title_align='center',
                            content=PopupGrid, auto_dismiss=False,
                            size_hint=(None, None), pos_hint={"center_x": 0.5, "top": 0.32},
                            size=(int(300 * self.koef), int(120 * self.koef)))
        # content4.bind(on_press=self.popup1.dismiss)
        content4.bind(on_press=self.closePopup)
        self.popup1.open()

    def Responce_name_detail_popup(self, *args):
        print("Ответ с сервера по типу детали")
        self.ifTriggerPhotio1 = 3
        PopupGrid = GridLayout(cols=1, pos_hint={'center_x': 0.6, 'center_y': 0.32})
        content4 = Button(text='Закрыть', halign='center', size=(int(200 * self.koef), int(50 * self.koef)),
                          size_hint=(None, None), pos=(int(50 * self.koef), int(50 * self.koef)), pos_hint=(None, None))
        PopupGrid.add_widget(content4)
        self.popup3 = Popup(title='Тип детали: ' + self.messageResponce.responce[0], title_align='center',
                            content=PopupGrid, auto_dismiss=False,
                            size_hint=(None, None), pos_hint={"center_x": 0.5, "top": 0.32},
                            size=(int(300 * self.koef), int(120 * self.koef)))
        # content4.bind(on_press=self.popup1.dismiss)
        content4.bind(on_press=self.closePopupResponce)
        self.popup3.open()

    def Responce_check_in_popup(self, *args):
        print("Ответ с сервера по изменению данных по детали")
        self.ifTriggerPhotio1 = 3
        PopupGrid = GridLayout(cols=1, pos_hint={'center_x': 0.6, 'center_y': 0.32})
        content4 = Button(text='Закрыть', halign='center', size=(int(200 * self.koef), int(50 * self.koef)),
                          size_hint=(None, None), pos=(int(50 * self.koef), int(50 * self.koef)), pos_hint=(None, None))
        PopupGrid.add_widget(content4)
        self.popup3 = Popup(title=self.messageResponce.responce[0], title_align='center',
                            content=PopupGrid, auto_dismiss=False,
                            size_hint=(None, None), pos_hint={"center_x": 0.5, "top": 0.32},
                            size=(int(300 * self.koef), int(120 * self.koef)))
        # content4.bind(on_press=self.popup1.dismiss)
        content4.bind(on_press=self.closePopupResponce)
        self.popup3.open()

    def Responce_location_popup(self, *args):
        print("Ответ с сервера по спискам расположения деталей пришли")
        if self.boolWorkchopLot == True:
            self.workshop_number_list = []
            self.lot_number_list = []
            self.workshop_number_list = self.messageResponce.workshop_number_list
            self.lot_number_list = self.messageResponce.lot_number_list
            PopupGrid = GridLayout(cols=1, size_hint_y=None)
            # Убедимся, что высота такая, чтобы было что прокручивать.
            PopupGrid.bind(minimum_height=PopupGrid.setter('height'))
            self.toggle = [0 for _ in range(len(self.workshop_number_list))]

            for index in range(len(self.workshop_number_list)):
                self.toggle[index] = ToggleButton(
                    text=self.workshop_number_list[index], size_hint_y=None,
                    group='cipher', height=30 * self.koef,
                )
                self.toggle[index].bind(on_press=self.changer)
                PopupGrid.add_widget(self.toggle[index])
        else:
            PopupGrid = GridLayout(cols=1, size_hint_y=None)
            # Убедимся, что высота такая, чтобы было что прокручивать.
            PopupGrid.bind(minimum_height=PopupGrid.setter('height'))
            self.toggle = [0 for _ in range(len(self.lot_number_list))]

            for index in range(len(self.lot_number_list)):
                self.toggle[index] = ToggleButton(
                    text=self.lot_number_list[index], size_hint_y=None,
                    group='cipher', height=30 * self.koef,
                )
                self.toggle[index].bind(on_press=self.changer)
                PopupGrid.add_widget(self.toggle[index])

        self.popup3 = Popup(title='Выберите месторасположение детали', title_align='center',
                            content=PopupGrid, auto_dismiss=False,
                            size_hint=(None, None), pos_hint={"center_x": 0.5, "top": 0.32},
                            size=(int(300 * self.koef), int(120 * self.koef)))
        self.popup3.open()

    def changer(self, *args):
        if self.boolWorkchopLot == True:
            for i in range(len(self.workshop_number_list)):
                if self.toggle[i].state == 'down':
                    self.messageParameter.workshopNumber = self.workshop_number_list[i]

            self.boolWorkchopLot = False
            self.popup3.dismiss()
            self.Responce_location_popup()
        else:
            for i in range(len(self.lot_number_list)):
                if self.toggle[i].state == 'down':
                    self.messageParameter.lotNumber = self.lot_number_list[i]
            self.boolWorkchopLot = True
            self.popup3.dismiss()
            self.closePopupResponceLocation()

    def closePopup(self, *args):
        self.popup1.dismiss()
        self.show_load()

    def closePopupResponce(self, *args):
        self.popup3.dismiss()
        self.messageResponce = MessageStructure.ClearObjectResponce(self.messageResponce)

    def closePopupResponceLocation(self, *args):
        self.popup3.dismiss()
        self.messageResponce = MessageStructure.ClearObjectResponce(self.messageResponce)
        self.QRPress_base()

    def popupForSocket(self, title, text):
        PopupGrid = GridLayout(rows=4, size_hint_y=1)
        PopupGrid.add_widget(Label(text=text, size_hint=(1, 1)))

        host1 = TextInput(size_hint=(1, 1))
        PopupGrid.add_widget(host1)  #
        PopupGrid.ids['host1'] = weakref.ref(host1)
        PopupGrid.ids.host1.text = appEnvironment.host
        PopupGrid.ids.host1.multiline = True

        port1 = TextInput(size_hint=(1, 1))
        PopupGrid.add_widget(port1)  #
        PopupGrid.ids['port1'] = weakref.ref(port1)
        PopupGrid.ids.port1.text = str(appEnvironment.port)
        PopupGrid.ids.port1.multiline = True
        content = Button(text='Закрыть', size_hint=(1, 1))
        PopupGrid.add_widget(content)
        self.popup4 = Popup(title=title, content=PopupGrid,
                            auto_dismiss=False, size_hint=(None, None),
                            size=(int(300 * self.koef), int(200 * self.koef)))
        self.PopupGrid = PopupGrid
        content.bind(on_press=self.closePopupForSocket)
        self.popup4.open()

    def closePopupForSocket(self, *args):
        self.hostAdress()
        self.popup4.dismiss()

    def hostAdress(self):

        appEnvironment.host = self.PopupGrid.ids.host1.text
        appEnvironment.port = int(self.PopupGrid.ids.port1.text)

    def popupForSocketNone(self):
        PopupGrid = GridLayout(rows=1, size_hint_y=None)
        PopupGrid.add_widget(Label(text='Сообщение не отправлено или не принят ответ'))
        content = Button(text='Закрыть')
        PopupGrid.add_widget(content)
        self.popup6 = Popup(title='Ошибка', content=PopupGrid,
                            auto_dismiss=False, size_hint=(None, None),
                            size=(int(300 * appEnvironment.koef), int(200 * appEnvironment.koef)))

        content.bind(on_press=self.popup6.dismiss)
        self.popup6.open()

    def popupForSocketNo(self):
        PopupGrid = GridLayout(rows=1, size_hint_y=None)
        PopupGrid.add_widget(Label(text='No image to choose'))
        content = Button(text='Закрыть')
        PopupGrid.add_widget(content)
        self.popup6 = Popup(title='Ошибка', content=PopupGrid,
                            auto_dismiss=False, size_hint=(None, None),
                            size=(int(300 * appEnvironment.koef), int(200 * appEnvironment.koef)))

        content.bind(on_press=self.popup6.dismiss)
        self.popup6.open()

    def popupForSocketNoBytes(self):
        PopupGrid = GridLayout(rows=1, size_hint_y=None)
        PopupGrid.add_widget(Label(text='No image to bytes'))
        content = Button(text='Закрыть')
        PopupGrid.add_widget(content)
        self.popup6 = Popup(title='Ошибка', content=PopupGrid,
                            auto_dismiss=False, size_hint=(None, None),
                            size=(int(300 * appEnvironment.koef), int(200 * appEnvironment.koef)))

        content.bind(on_press=self.popup6.dismiss)
        self.popup6.open()

    def popupForSocketNoImageCore(self):
        PopupGrid = GridLayout(rows=1, size_hint_y=None)
        PopupGrid.add_widget(Label(text='No image Core'))
        content = Button(text='Закрыть')
        PopupGrid.add_widget(content)
        self.popup6 = Popup(title='Ошибка', content=PopupGrid,
                            auto_dismiss=False, size_hint=(None, None),
                            size=(int(300 * appEnvironment.koef), int(200 * appEnvironment.koef)))

        content.bind(on_press=self.popup6.dismiss)
        self.popup6.open()

class FileChoose(Screen):

    def __init__(self, *args, **kwargs):
        super(FileChoose, self).__init__(*args, **kwargs)
        #self.selection = ListProperty([])
        #self.filepaths = []
        self.popup = None

    def selected(self, filename):
        try:
            self.ids.my_image.source = filename[0]
        except:
            self.popupForSocketNo()
        else:
            try:
                self.popupForSocketYes(filename[0])
                appEnvironment.filenameEnv = []
                appEnvironment.filenameEnv.append(filename[0])
            except:
                pass

    def dellwidget(self):
        # удаляет все виджеты, которые находяться в another_box
        self.ids.my_image.source = ""
        #appEnvironment.triggerSelectImage = 1
        appEnvironment.QRWindowObj.load(appEnvironment.filenameEnv, appEnvironment.filenameEnv)

    def popupForSocketYes(self,filename):
        PopupGrid = GridLayout(rows=2, size_hint_y=None)
        PopupGrid.add_widget(Label(text=filename))
        content = Button(text='Закрыть')
        PopupGrid.add_widget(content)
        self.popup = Popup(title='Успех', content=PopupGrid,
                            auto_dismiss=False, size_hint=(None, None),
                            size=(int(300 * appEnvironment.koef), int(200 * appEnvironment.koef)))

        content.bind(on_press=self.popup.dismiss)
        self.popup.open()

    def popupForSocketNo(self):
        PopupGrid = GridLayout(rows=2, size_hint_y=None)
        PopupGrid.add_widget(Label(text='Ничего не вышло'))
        content = Button(text='Закрыть')
        PopupGrid.add_widget(content)
        self.popup = Popup(title='Провал', content=PopupGrid,
                           auto_dismiss=False, size_hint=(None, None),
                           size=(int(300 * appEnvironment.koef), int(200 * appEnvironment.koef)))

        content.bind(on_press=self.popup.dismiss)
        self.popup.open()

class FourthWindow(Screen):
    #Окно для просмотра номенклатуры деталей
    def __init__(self, *args, **kwargs):
        super(FourthWindow, self).__init__(*args, **kwargs)
        self.listOfItems=True
        self.listOfItems = True
        Thread(target=self.textInInputFourth).start()
        # Объект - запрос на сервер
        self.messageParameter = MessageStructureParameter()
        # Объект - ответ с сервера
        self.messageResponce = MessageResponceParameter()
        self.partName = ''
        #self.fourthTrigger = 0 # Переключатель для работы с потоком
        self.koef = appEnvironment.koef

    def textInInputFourth(self):

        while True:
            time.sleep(0.4)
            if (appEnvironment.fourthTrigger == 1):
                # Отправка запроса на сервер и получения ответа, заполняющего список номенклатуры деталей
                self.messageParameter.code_request0 = 0
                self.messageParameter.code_request1 = 0

                if appEnvironment.ClientProxyObj.connect():
                    self.messageResponce = appEnvironment.ClientProxyObj.sendRequest(self.messageParameter)
                    self.messageParameter = MessageStructure.ClearObject(self.messageParameter)
                    if self.messageResponce != None:
                        if (self.messageResponce.message == 'Список номенклатуры деталей'):
                            appEnvironment.fourthTrigger = 0
                    else:
                        self.popupForSocketNone()
                        appEnvironment.fourthTrigger = 0

                    appEnvironment.ClientProxyObj.disconnect()
                else:
                    self.popupForSocket(appEnvironment.title, appEnvironment.text)
                    appEnvironment.fourthTrigger = 0

            if (appEnvironment.fourthTrigger == 3):
                # Отправка запроса на сервер и получения ответа, заполняющего отчет для выбранного вида детали
                self.messageParameter.code_request0 = 7
                self.messageParameter.code_request1 = 0

                print('Зашел в отправку сообщения')
                if appEnvironment.ClientProxyObj.connect():
                    self.messageResponce = appEnvironment.ClientProxyObj.sendRequest(self.messageParameter)
                    self.messageParameter = MessageStructure.ClearObject(self.messageParameter)
                    if self.messageResponce != None:
                        if (self.messageResponce.message == 'Отчет по номенклатуре деталей'):
                            appEnvironment.reportsWindowDetailPartName = self.partName
                            appEnvironment.reportsWindowDetailMessageResponce = self.messageResponce
                            appEnvironment.fourthTrigger = 0
                    else:
                        self.popupForSocketNone()
                        appEnvironment.fourthTrigger = 0

                    appEnvironment.ClientProxyObj.disconnect()
                else:
                    self.popupForSocket(appEnvironment.title, appEnvironment.text)
                    appEnvironment.fourthTrigger = 0

    def ScrollWindow(self):
        if (self.listOfItems == True):
            # self.ids.ScrollWindowid.add_widget(ScrollView(size_hint=[1, 1]))
            self.ids.Scrollbuttonid.text = "Список номенклатуры выведен"
            leftGrid = GridLayout(cols=1, size_hint_y=None)
            # Убедимся, что высота такая, чтобы было что прокручивать.
            leftGrid.bind(minimum_height=leftGrid.setter('height'))
            ciphers = self.messageResponce.type_name_list

            self.toggle = [0 for _ in range(len(ciphers))]

            for index in range(len(ciphers)):
                self.toggle[index] = ToggleButton(
                    text=ciphers[index], size_hint_y=None,
                    group='cipher', height=30 * self.koef,
                )
                self.toggle[index].bind(on_press=self.changer)
                leftGrid.add_widget(self.toggle[index])

            self.ids.ScrollWindowid.add_widget(leftGrid)
            self.listOfItems = False
        else:
            # удаляет все виджеты, которые находяться в another_box
            for i in range(len(self.ids.ScrollWindowid.children)):
                self.ids.ScrollWindowid.remove_widget(self.ids.ScrollWindowid.children[-1])
            self.listOfItems = True
            self.ids.Scrollbuttonid.text = "Просмотреть номенклатуру"

    def changer(self, *args):
        ciphers = self.messageResponce.type_name_list
        for i in range(len(ciphers)):
            if self.toggle[i].state == 'down':
                self.partName = ciphers[i]

        self.messageParameter.message = self.partName
        appEnvironment.fourthTrigger = 3
        time.sleep(0.4)
        # Переход в конкретное описание детали
        self.manager.current = 'reportOfItem'
        # Переход окна вправо (текущее уходит влево)
        self.manager.transition.direction = "left"

    def popupForSocket(self, title, text):
        PopupGrid = GridLayout(rows=4, size_hint_y=1)
        PopupGrid.add_widget(Label(text=text,size_hint=(1, 1)))

        host1 = TextInput(size_hint=(1, 1))
        PopupGrid.add_widget(host1)  #
        PopupGrid.ids['host1'] = weakref.ref(host1)
        PopupGrid.ids.host1.text = appEnvironment.host
        PopupGrid.ids.host1.multiline = True

        port1 = TextInput(size_hint=(1, 1))
        PopupGrid.add_widget(port1)  #
        PopupGrid.ids['port1'] = weakref.ref(port1)
        PopupGrid.ids.port1.text = str(appEnvironment.port)
        PopupGrid.ids.port1.multiline = True
        content = Button(text='Закрыть',size_hint=(1, 1))
        PopupGrid.add_widget(content)
        #PopupGrid.content(size_hint=(1, 0.3))
        self.popup4 = Popup(title=title, content=PopupGrid,
                            auto_dismiss=False, size_hint=(None, None),
                            size=(int(300 * self.koef), int(200 * self.koef)), padding = 50 * self.koef)
        self.PopupGrid = PopupGrid
        content.bind(on_press=self.closePopupForSocket)
        self.popup4.open()

    def closePopupForSocket(self, *args):
        self.hostAdress()
        self.popup4.dismiss()
        # https://kivy.org/doc/stable/api-kivy.uix.screenmanager.html
        # appEnvironment.WindowManagerObj.switch_to(appEnvironment.MainWindowObj, direction='right')

    def hostAdress(self):
        appEnvironment.host = self.PopupGrid.ids.host1.text
        appEnvironment.port = int(self.PopupGrid.ids.port1.text)


class ReportsWindowDetail(Screen):
    def __init__(self, *args, **kwargs):
        super(ReportsWindowDetail, self).__init__(*args, **kwargs)
        self.listOfItems = True
        # Объект - ответ с сервера
        self.messageResponce = None
        self.partName = ''

    def windowDraw(self):
        # global messageResponce
        self.messageResponce = appEnvironment.reportsWindowDetailMessageResponce
        self.partName = appEnvironment.reportsWindowDetailPartName
        if (self.listOfItems == True) and (self.messageResponce != None):
            #img_str = cv2.imencode('.jpg', self.messageResponce.Images[0])[1].tostring()
            #im_bytes = io.BytesIO(img_str)
            #img_str = cv2.imencode('.jpg', self.messageResponce.Images[0])[1].tobytes()
            #im_bytes = io.BytesIO(img_str)
            im_bytes = self.messageResponce.Images[0]
            im = CoreImage(im_bytes, ext="png")
            self.ids.ImageBoxId2.add_widget(Image(texture=im.texture))

            self.ids.ButtonScrollWindowReportid.text = self.partName
            leftGrid1 = GridLayout(cols=2, spacing=10, size_hint_y=None)  # , size_hint_y=10, size_hint_x=10)
            # Убедимся, что высота такая, чтобы было что прокручивать.
            leftGrid1.bind(minimum_height=leftGrid1.setter('height'), minimum_width=leftGrid1.setter('width'))  #
            self.toggle = []
            for i in range(len(self.messageResponce.report_list)):
                nasted = []
                self.toggle.append(nasted)
                for j in range(len(self.messageResponce.report_list[0])):
                    nasted.append('')

            for index in range(len(self.messageResponce.report_list[0])):
                width = 200 * koef

                self.toggle[0][index] = Label(
                    size_hint_y=None,
                    size_hint_x=None,
                    height=40 * koef,
                    width=width,
                    # ,
                    padding=(10 * koef, 10 * koef),
                    text=str(self.messageResponce.report_list[0][index]),
                )
                leftGrid1.add_widget(self.toggle[0][index])

                self.toggle[1][index] = Label(
                    size_hint_y=None,
                    size_hint_x=None,
                    height=40 * koef,
                    width=width,
                    # ,
                    padding=(10 * koef, 10 * koef),
                    text=str(self.messageResponce.report_list[1][index]),
                )
                leftGrid1.add_widget(self.toggle[1][index])

            # Убедимся, что высота такая, чтобы было что прокручивать.
            leftGrid1.bind(minimum_height=leftGrid1.setter('height'), minimum_width=leftGrid1.setter('width'))
            self.ids.ScrollWindowReportid.add_widget(leftGrid1)
            self.listOfItems = False
        else:
            # удаляет все виджеты, которые находяться в another_box
            pass

    def dellwidgetAll(self):
        # удаляет все виджеты, которые находяться в another_box

        for i in range(len(self.ids.ScrollWindowReportid.children)):
            self.ids.ScrollWindowReportid.remove_widget(self.ids.ScrollWindowReportid.children[-1])

        for i in range(len(self.ids.ImageBoxId2.children)):
            self.ids.ImageBoxId2.remove_widget(self.ids.ImageBoxId2.children[-1])

        self.ids.ButtonScrollWindowReportid.text = 'Нажмите'
        self.messageResponce = None
        self.partName = ''
        self.listOfItems = True
        appEnvironment.fourthTrigger = 1

class ReportsWindow(Screen):
    #Report window main screen
    def __init__(self, *args, **kwargs):
        super(ReportsWindow, self).__init__(*args, **kwargs)
        self.ciphers_filter = []
        Thread(target=self.textInInput).start()
        self.listOfItemsView = 0  # Переменная для обмена сообщениями с сервером в части отчетов
        #self.param_for_filter = 1  # С каким атрибутом работаем
        #self.ifTriggerReport = 0  # Прорисовка и обновление отчета по результатам запроса
        # Объект - запрос на сервер
        #self.messageParameter = MessageStructureParameter()
        # Объект - ответ с сервера
        #self.messageResponce = MessageResponceParameter()
        self.koef = appEnvironment.koef

    def textInInput(self):
        # Функция для вывода информации в текстовые окна приложения
        while True:
            time.sleep(0.4)
            if (appEnvironment.listOfItemsView == 2):
                # Отправка запроса на сервер и получения ответа, заполняющего пределы для фильтров
                appEnvironment.reportWindowMessageParameter.code_request0 = 5
                appEnvironment.reportWindowMessageParameter.code_request1 = 0
                print('Зашел в отправку сообщения')
                if appEnvironment.ClientProxyObj.connect():
                    appEnvironment.reportWindowmessageResponce = appEnvironment.ClientProxyObj.sendRequest(appEnvironment.reportWindowMessageParameter)
                    appEnvironment.reportWindowMessageParameter = MessageStructure.ClearObject(appEnvironment.reportWindowMessageParameter)
                    if appEnvironment.reportWindowmessageResponce  != None:
                        if (appEnvironment.reportWindowmessageResponce .message == 'Пределы для фильтров'):
                            appEnvironment.listOfItemsView = 1
                    else:
                        self.popupForSocketNone()
                        appEnvironment.listOfItemsView = 0

                    appEnvironment.ClientProxyObj.disconnect()
                else:
                    self.popupForSocket(appEnvironment.title, appEnvironment.text)
                    appEnvironment.listOfItemsView = 0

            if (appEnvironment.listOfItemsView == 1):
                # Заполнение текстовых полей
                if len(appEnvironment.reportWindowMessageParameter.type_name_list) > 0:
                    textstr = ''
                    for item in appEnvironment.reportWindowMessageParameter.type_name_list:
                        textstr = textstr + item + '; '
                    self.ids.text_input1.text = textstr
                if len(appEnvironment.reportWindowMessageParameter.workshop_number_list) > 0:
                    textstr = ''
                    for item in appEnvironment.reportWindowMessageParameter.workshop_number_list:
                        textstr = textstr + item + '; '
                    self.ids.text_input2.text = textstr
                if len(appEnvironment.reportWindowMessageParameter.lot_number_list) > 0:
                    textstr = ''
                    for item in appEnvironment.reportWindowMessageParameter.lot_number_list:
                        textstr = textstr + item + '; '
                    self.ids.text_input3.text = textstr

                # Данные для ползунков
                self.ids.slider_d1.min = round(appEnvironment.reportWindowmessageResponce.imbalance_list[0] - 0.05, 2)
                self.ids.slider_d1.max = round(appEnvironment.reportWindowmessageResponce.imbalance_list[1] + 0.05, 2)
                self.ids.slider_d1.value = round(appEnvironment.reportWindowmessageResponce.imbalance_list[0] - 0.05, 2)
                self.ids.slider_d2.min = round(appEnvironment.reportWindowmessageResponce.imbalance_list[0] - 0.05, 2)
                self.ids.slider_d2.max = round(appEnvironment.reportWindowmessageResponce.imbalance_list[1] + 0.05, 2)
                self.ids.slider_d2.value = round(appEnvironment.reportWindowmessageResponce.imbalance_list[1] + 0.05, 2)

                self.ids.slider_d3.min = round(appEnvironment.reportWindowmessageResponce.diameter_list[0] - 0.05, 2)
                self.ids.slider_d3.max = round(appEnvironment.reportWindowmessageResponce.diameter_list[1] + 0.05, 2)
                self.ids.slider_d3.value = round(appEnvironment.reportWindowmessageResponce.diameter_list[0] - 0.05, 2)
                self.ids.slider_d4.min = round(appEnvironment.reportWindowmessageResponce.diameter_list[0] - 0.05, 2)
                self.ids.slider_d4.max = round(appEnvironment.reportWindowmessageResponce.diameter_list[1] + 0.05, 2)
                self.ids.slider_d4.value = round(appEnvironment.reportWindowmessageResponce.diameter_list[1] + 0.05, 2)

                appEnvironment.listOfItemsView = 0

            if (appEnvironment.listOfItemsView == 3):
                # Проверка нулевых значений перед отправкой. Если 0, или противоречивые - исправление
                if len(appEnvironment.reportWindowMessageParameter.type_name_list) == 0:
                    appEnvironment.reportWindowMessageParameter.type_name_list = appEnvironment.reportWindowmessageResponce.type_name_list
                if len(appEnvironment.reportWindowMessageParameter.workshop_number_list) == 0:
                    appEnvironment.reportWindowMessageParameter.workshop_number_list = appEnvironment.reportWindowmessageResponce.workshop_number_list
                if len(appEnvironment.reportWindowMessageParameter.lot_number_list) == 0:
                    appEnvironment.reportWindowMessageParameter.lot_number_list = appEnvironment.reportWindowmessageResponce.lot_number_list

                # Отправка запроса на сервер для получения ответа для формирования отчета
                appEnvironment.reportWindowMessageParameter.code_request0 = 6
                appEnvironment.reportWindowMessageParameter.code_request1 = 0

                if appEnvironment.ClientProxyObj.connect():
                    appEnvironment.reportWindowmessageResponce= appEnvironment.ClientProxyObj.sendRequest(appEnvironment.reportWindowMessageParameter)
                    appEnvironment.reportWindowMessageParameter = MessageStructure.ClearObject(appEnvironment.reportWindowMessageParameter)
                    if appEnvironment.reportWindowmessageResponce != None:
                        if (appEnvironment.reportWindowmessageResponce.message == 'Отчет с учетом фильтров'):
                            appEnvironment.listOfItemsView = 0
                            appEnvironment.ifTriggerReport = 1
                    else:
                        self.popupForSocketNone()
                        appEnvironment.listOfItemsView = 0

                    appEnvironment.ClientProxyObj.disconnect()
                else:
                    self.popupForSocket(appEnvironment.title, appEnvironment.text)
                    appEnvironment.listOfItemsView = 0

    def ScrollWindowFilterType(self):
        appEnvironment.param_for_filter = 1
        #appEnvironment.FilterWindowObj.fillData(self.param_for_filter, self.messageResponce,
        #                                        self.messageParameter)
        # Переход в конкретное описание детали
        self.manager.current = 'filterOfItem'
        # Переход окна вправо (текущее уходит влево)
        self.manager.transition.direction = "left"
        # self.ScrollWindowFilter()

    def ScrollWindowFilterWorkshop(self):
        appEnvironment.param_for_filter = 2
        #appEnvironment.FilterWindowObj.fillData(self.param_for_filter, self.messageResponce, self.messageParameter)
        # Переход в конкретное описание детали
        self.manager.current = 'filterOfItem'
        # Переход окна вправо (текущее уходит влево)
        self.manager.transition.direction = "left"
        # self.ScrollWindowFilter()

    def ScrollWindowFilterLot(self):
        appEnvironment.param_for_filter = 3
        #appEnvironment.FilterWindowObj.fillData(self.param_for_filter, self.messageResponce,
        #                                        self.messageParameter)
        # Переход в конкретное описание детали
        self.manager.current = 'filterOfItem'
        # Переход окна вправо (текущее уходит влево)
        self.manager.transition.direction = "left"
        # self.ScrollWindowFilter()

    def DataForReportAndDataFromDataBase(self):
        # Функция для формирования запроса и получения ответа по данным для отчета
        appEnvironment.reportWindowMessageParameter.imbalance_list = []
        appEnvironment.reportWindowMessageParameter.imbalance_list.append(round(self.ids.slider_d1.value, 2))
        appEnvironment.reportWindowMessageParameter.imbalance_list.append(round(self.ids.slider_d2.value, 2))
        appEnvironment.reportWindowMessageParameter.diameter_list = []
        appEnvironment.reportWindowMessageParameter.diameter_list.append(round(self.ids.slider_d3.value, 2))
        appEnvironment.reportWindowMessageParameter.diameter_list.append(round(self.ids.slider_d4.value, 2))
        appEnvironment.listOfItemsView = 3
        time.sleep(0.4)
        #appEnvironment.MainReportObj.fillData(self.ifTriggerReport, self.listOfItemsView, self.messageResponce)

    def popupForSocket(self, title, text):
        PopupGrid = GridLayout(rows=4, size_hint_y=1)
        PopupGrid.add_widget(Label(text=text, size_hint=(1, 1)))

        host1 = TextInput(size_hint=(1, 1))
        PopupGrid.add_widget(host1)  #
        PopupGrid.ids['host1'] = weakref.ref(host1)
        PopupGrid.ids.host1.text = appEnvironment.host
        PopupGrid.ids.host1.multiline = True

        port1 = TextInput(size_hint=(1, 1))
        PopupGrid.add_widget(port1)  #
        PopupGrid.ids['port1'] = weakref.ref(port1)
        PopupGrid.ids.port1.text = str(appEnvironment.port)
        PopupGrid.ids.port1.multiline = True
        content = Button(text='Закрыть', size_hint=(1, 1))
        PopupGrid.add_widget(content)
        self.popup4 = Popup(title=title, content=PopupGrid,
                            auto_dismiss=False, size_hint=(None, None),
                            size=(int(300 * self.koef), int(200 * self.koef)))
        self.PopupGrid = PopupGrid
        content.bind(on_press=self.closePopupForSocket)
        self.popup4.open()

    def closePopupForSocket(self, *args):
        self.hostAdress()
        self.popup4.dismiss()
        # https://kivy.org/doc/stable/api-kivy.uix.screenmanager.html
        # appEnvironment.WindowManagerObj.switch_to(appEnvironment.MainWindowObj, direction='right')

    def hostAdress(self):

        appEnvironment.host = self.PopupGrid.ids.host1.text
        appEnvironment.port = int(self.PopupGrid.ids.port1.text)

class FilterWindow(Screen):
    def __init__(self, *args, **kwargs):
        super(FilterWindow, self).__init__(*args, **kwargs)
        self.listOfItems = True
        self.param_for_filter = 1  #С каким атрибутом работаем
        self.ciphers_filter = []
        # Объект - ответ с сервера
        #self.messageResponce = None
        # Объект - запрос на сервер
        #self.messageParameter = None
        self.koef = appEnvironment.koef

    def ScrollWindowFilter(self):
        if appEnvironment.param_for_filter == 1:
            appEnvironment.reportWindowMessageParameter.type_name_list = []
            self.ciphers_filter = appEnvironment.reportWindowmessageResponce.type_name_list
        elif appEnvironment.param_for_filter == 2:
            appEnvironment.reportWindowMessageParameter.workshop_number_list = []
            self.ciphers_filter = appEnvironment.reportWindowmessageResponce.workshop_number_list
        elif appEnvironment.param_for_filter == 3:
            appEnvironment.reportWindowMessageParameter.lot_number_list = []
            self.ciphers_filter = appEnvironment.reportWindowmessageResponce.lot_number_list

        leftGrid = GridLayout(cols=1, size_hint_y=None)
        leftGrid.bind(minimum_height=leftGrid.setter('height'))

        leftGrid = GridLayout(cols=1, size_hint_y=None)
        #Убедимся, что высота такая, чтобы было что прокручивать.

        self.toggle = [0 for _ in range(len(self.ciphers_filter))]

        for index in range(len(self.ciphers_filter)):
            self.toggle[index] = ToggleButton(
                text= self.ciphers_filter[index],  size_hint_y=None,
                group= self.ciphers_filter[index], height=30*self.koef
                )
            #self.toggle[index].bind(on_press=self.changer)
            leftGrid.add_widget(self.toggle[index])

        self.ids.ScrollWindowFilterid.add_widget(leftGrid)

    def changerFilter(self, *args):
        list_button_down = []
        if len(self.ciphers_filter)==0:
            title = 'Предупреждение'
            text = 'Не выведен список'
            self.popupForFilter(title, text)
        else:
            for i in range(len(self.ciphers_filter)):
                if self.toggle[i].state == 'down':
                    if appEnvironment.param_for_filter == 1:
                        list_button_down.append(appEnvironment.reportWindowmessageResponce.type_name_list[i])
                        appEnvironment.reportWindowMessageParameter.type_name_list.append(appEnvironment.reportWindowmessageResponce.type_name_list[i])
                    if appEnvironment.param_for_filter == 2:
                        list_button_down.append(appEnvironment.reportWindowmessageResponce.workshop_number_list[i])
                        appEnvironment.reportWindowMessageParameter.workshop_number_list.append(appEnvironment.reportWindowmessageResponce.workshop_number_list[i])
                    if appEnvironment.param_for_filter == 3:
                        list_button_down.append(appEnvironment.reportWindowmessageResponce.lot_number_list[i])
                        appEnvironment.reportWindowMessageParameter.lot_number_list.append(appEnvironment.reportWindowmessageResponce.lot_number_list[i])

            if (len(list_button_down)==0):
                title = 'Предупреждение'
                text='Ничего не выбрано'
                self.popupForFilter(title, text)
            else:
                title = 'Предупреждение'
                text = 'Выбор сохранен'
                self.popupForFilter(title, text)

    def popupForFilter(self,title,text):
        PopupGrid = GridLayout(rows=2, size_hint_y=None)
        PopupGrid.add_widget(Label(text=text))
        content = Button(text='Закрыть')
        PopupGrid.add_widget(content)
        popup = Popup(title=title, content=PopupGrid,
                      auto_dismiss=False, size_hint=(None, None), size=(int(300 * self.koef), int(200 * self.koef)))

        content.bind(on_press=popup.dismiss)
        popup.open()

    def dellwidgetfilter(self):
        # удаляет все виджеты, которые находяться в another_box
        for i in range(len(self.ids.ScrollWindowFilterid.children)):
            self.ids.ScrollWindowFilterid.remove_widget(self.ids.ScrollWindowFilterid.children[-1])
        appEnvironment.listOfItemsView = 1

class MainReport(Screen):
    def __init__(self, *args, **kwargs):
        super(MainReport, self).__init__(*args, **kwargs)
        Thread(target=self.threadWindowDrawMainReport).start()
        # Объект - ответ с сервера
        #self.messageResponce = None
        #self.listOfItemsView = 0 #Переменная для обмена сообщениями с сервером в части отчетов
        #self.ifTriggerReport = 0  # Прорисовка и обновление отчета по результатам запроса
        self.koef = appEnvironment.koef

    def threadWindowDrawMainReport(self):
        while True:
            time.sleep(0.3)
            if (appEnvironment.ifTriggerReport == 1):
                self.windowDrawMainReport()
                appEnvironment.ifTriggerReport = 0

    def windowDrawMainReport(self):
        leftGrid1 = GridLayout(cols=len(appEnvironment.reportWindowmessageResponce.report_list[0]), spacing=10,
                               size_hint_y=None)  # , size_hint_y=10, size_hint_x=10)
        # Убедимся, что высота такая, чтобы было что прокручивать.
        leftGrid1.bind(minimum_height=leftGrid1.setter('height'), minimum_width=leftGrid1.setter('width'))  #
        self.toggle = []
        for i in range(len(appEnvironment.reportWindowmessageResponce.report_list)):
            nasted = []
            self.toggle.append(nasted)
            for j in range(len(appEnvironment.reportWindowmessageResponce.report_list[0])):
                nasted.append('')
        for index in range(len(appEnvironment.reportWindowmessageResponce.report_list[0])):
            if (index == 0):
                width = 50 * self.koef
            else:
                width = 150 * self.koef

            self.toggle[0][index] = Label(
                size_hint_y=None,
                size_hint_x=None,
                height=40 * self.koef,
                width=width,
                # ,
                padding=(10 * self.koef, 10 * self.koef),
                text=str(appEnvironment.reportWindowmessageResponce.report_list[0][index]),
                #color=(1, 1, 1, 1)
                # text_size=(self.width, None)
            )
            #with self.toggle[0][index].canvas.before:
                #Color(0, 1, 0, 0.25)
                #Rectangle(pos=self.toggle[0][index].pos, size=self.toggle[0][index].size)
            leftGrid1.add_widget(self.toggle[0][index])

        for index in range(1, len(appEnvironment.reportWindowmessageResponce.report_list)):
            for index1 in range(len(appEnvironment.reportWindowmessageResponce.report_list[0])):
                if (index1 == 0):
                    width = 50 * self.koef
                else:
                    width = 150 * self.koef

                self.toggle[index][index1] = Label(
                    size_hint_y=None,
                    size_hint_x=None,
                    height=40 * self.koef,
                    width=width,
                    # text_size=(self.width, None),
                    padding=(10 * self.koef, 10 * self.koef),
                    text=str(appEnvironment.reportWindowmessageResponce.report_list[index][index1]),
                    # text_size=(self.width, None)
                )
                leftGrid1.add_widget(self.toggle[index][index1])
            # Убедимся, что высота такая, чтобы было что прокручивать.
        leftGrid1.bind(minimum_height=leftGrid1.setter('height'), minimum_width=leftGrid1.setter('width'))
        self.ids.ScrollWindowReportMainid.add_widget(leftGrid1)

    def dellwidget(self):
        # удаляет все виджеты, которые находяться в another_box
        for i in range(len(self.ids.ScrollWindowReportMainid.children)):
            self.ids.ScrollWindowReportMainid.remove_widget(self.ids.ScrollWindowReportMainid.children[-1])
        appEnvironment.ifTriggerReport = 0
        appEnvironment.listOfItemsView = 2

# Менеджер перехода между страницами и передачи данных
class WindowManager(ScreenManager):
    pass

class P(FloatLayout):
    pass

#Функция для всплывающего окна
def show_popup():
    show = P()

    popupWindow = Popup(title="Popup Window", content = show, size_hint=(None,None), size=(400,400))

    popupWindow.open()


kv = Builder.load_file("kvfiles/my.kv")

# Класс, наследующий от App
class MyMainApp(App):
    title = 'Умный склад'

    #Метод build - обеспечивает наличие на окне приложение виджета
    #Может вернуть только один виджет
    def build(self):
        #Создание лэйаута
        #описано в файле my.kv
        return kv

    #Метод для кодировки русских символов в описании
    def load_all_kv_files(self, directory_kv_files):
        for kv_file in os.listdir(directory_kv_files):
            kv_file = os.path.join(directory_kv_files, kv_file)
            if os.path.isfile(kv_file) and kv_file.endswith("kv"):
                with open(kv_file, encoding="utf-8") as kv:
                    Builder.load_string(kv.read())

if __name__ == '__main__':
    directory_kv_files = 'kvfiles'
    #MyMainApp().load_all_kv_files(directory_kv_files)
    appEnvironment.ClientProxyObj = ClientProxy()
    MyMainApp().run()

