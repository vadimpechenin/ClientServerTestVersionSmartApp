from threading import Thread
from kivy.uix.screenmanager import Screen

import io
from os.path import getsize

from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import weakref

# Библиотеки для формирования структуры пересылаемого сообщения
from message.messageStructure import MessageStructure
from message.messageStructureParameter import MessageStructureParameter
from message.messageResponceParameter import MessageResponceParameter

from client.applicationEnvironment import appEnvironment

from client.clientModule import MySocket

import cv2

import time

class QRWindow(Screen):
    # Класс для работы по отсылке фотографий
    #loadfile = ObjectProperty(None)
    #text_input = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(QRWindow, self).__init__(*args, **kwargs)
        #self.sock = MySocket()
        Thread(target=self.get_data).start()
        #t1 = FuncThread(self.get_data).start()
        # Объект - запрос на сервер
        self.messageParameter = MessageStructureParameter()
        # Объект - ответ с сервера
        self.messageResponce = MessageResponceParameter()
        self.popup = None
        self.popup1 = None
        self.popup2 = None
        self.popup3 = None
        self.popup4 = None

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

        appEnvironment.QRWindowObj = self
        self.koef = appEnvironment.koef
        self.PopupGrid = None
        #self.sock = appEnvironment.sock


    def allRequest(self):
        self.ifTriggerPhotio1 = 3
        self.messageParameter.code_request0 = 1
        self.messageParameter.code_request1 = 1

        filename=[]
        #filename.append('D:\\2014 осень\\6_im.jpg')
        filename.append('D:\\2014spring\\1\\6_1.jpg')


        path = ''

        self.filename_g = []
        self.ImageLoad(path, filename)
        filename = []
        filename.append('D:\\2014spring\\1\\6_2.jpg')
        self.ImageLoad(path, filename)
        filename = []
        filename.append('D:\\2014spring\\1\\6_3.jpg')
        self.ImageLoad(path, filename)

        self.send_data = 1


    def ImageLoad(self,path, filename):

        data = io.BytesIO(open(filename[0], "rb").read())
        im = CoreImage(data, ext="png")
        if self.ifTriggerPhotio1==1:

            self.filename_g = filename[0]
            #Запись информации о дате для детали
            if (self.messageParameter.code_request0) == 2:
                reversed_name_of_data = ''
                reversed_string = ''
                if (len(filename[0]) >= 19):
                    for i in range(19):
                        reversed_name_of_data = reversed_name_of_data + filename[0][-i - 5]
                    reversed_string = reversed_name_of_data[::-1]
                self.messageParameter.nameOfImage = reversed_string
        else:

            self.filename_g.append(filename[0])

        file = cv2.imread(filename[0])

        sizeOfImage = getsize(filename[0])

        self.messageParameter.Images.append(file)
        self.messageParameter.sizeOfImages.append(sizeOfImage)


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
        if self.booleanPhoto==True:
            if (self.ifTriggerPhotio1==1):
                self.filename_g = None
            elif (self.ifTriggerPhotio1==3):
                self.filename_g = []
                self.triggerPhoto1 = 2
            self.booleanPhoto = False
        print(self.triggerPhoto1)
        appEnvironment.FileChooseObj.clear_selection()
        appEnvironment.FileChooseObj.choose()
        self.load(appEnvironment.FileChooseObj.selection,appEnvironment.FileChooseObj.selection)
        #content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        #self._popup = Popup(title="Load file", content=content,
                            #size_hint=(0.9, 0.9))
        #self._popup.open()

    def load(self, path, filename):
        #self.dismiss_popup()
        self.ImageLoad(path, filename)
        if (self.ifTriggerPhotio1 == 3) and (self.triggerPhoto1>0):
            self.triggerPhoto1 -=1
            self.triggerPhoto2 +=1
            self.imgPress()


    def get_data(self):
        while True:
            time.sleep(0.3)
            if (self.send_data==1):
                try:
                    print('Зашел в отправку сообщения')
                    self.sock = MySocket(host = appEnvironment.host, port = appEnvironment.port)
                    self.sock.send_data(self.messageParameter)
                    self.messageParameter = MessageStructure.ClearObject(self.messageParameter)
                    self.send_data = 2
                except:
                    self.popupForSocket(appEnvironment.title, appEnvironment.text)
                    self.send_data = 0

            if (self.send_data == 2):

                self.messageResponce = self.sock.get_data()
                self.send_data = 0
                if (self.messageResponce.message=='Изображение пришло'):
                    self.Responce_name_detail_popup()
                elif (self.messageResponce.message=='Список возможных месторасположений детали'):
                    self.Responce_location_popup()
                elif (self.messageResponce.message == 'Изменения внесены'):
                    self.Responce_name_detail_popup()

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
        content4 = Button(text='Закрыть', halign='center', size= (int(200 * self.koef), int(50 * self.koef)),
                          size_hint=(None, None), pos = (int(50 * self.koef), int(50 * self.koef)), pos_hint=(None, None))
        PopupGrid.add_widget(content4)
        self.popup1 = Popup(title='Считайте QR', title_align='center', content =PopupGrid, auto_dismiss=False,
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
        content4 = Button(text='Закрыть', halign='center', size= (int(200 * self.koef), int(50 * self.koef)),
                          size_hint=(None, None), pos = (int(50 * self.koef), int(50 * self.koef)), pos_hint=(None, None))
        PopupGrid.add_widget(content4)
        self.popup1 = Popup(title='Выберите фото с ' + str(self.triggerPhoto2) + ' ракурса', title_align='center', content =PopupGrid, auto_dismiss=False,
                            size_hint=(None, None), pos_hint={"center_x": 0.5, "top": 0.32},
                            size=(int(300 * self.koef), int(120 * self.koef)))
        #content4.bind(on_press=self.popup1.dismiss)
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
        PopupGrid = GridLayout(rows=4, size_hint_y=None)
        PopupGrid.add_widget(Label(text=text))

        host1 = TextInput()
        PopupGrid.add_widget(host1)#
        PopupGrid.ids['host1'] = weakref.ref(host1)
        PopupGrid.ids.host1.text = appEnvironment.host
        PopupGrid.ids.host1.multiline = True

        port1 = TextInput()
        PopupGrid.add_widget(port1)  #
        PopupGrid.ids['port1'] = weakref.ref(port1)
        PopupGrid.ids.port1.text = str(appEnvironment.port)
        PopupGrid.ids.port1.multiline = True
        content = Button(text='Закрыть')
        PopupGrid.add_widget(content)
        self.popup4 = Popup(title=title, content=PopupGrid,
                      auto_dismiss=False, size_hint=(None, None), size=(int(300 * self.koef), int(200 * self.koef)))
        self.PopupGrid = PopupGrid
        content.bind(on_press=self.closePopupForSocket)
        self.popup4.open()

    def closePopupForSocket(self, *args):
        self.hostAdress()
        self.popup4.dismiss()

    def hostAdress(self):

        appEnvironment.host = self.PopupGrid.ids.host1.text
        appEnvironment.port = int(self.PopupGrid.ids.port1.text)