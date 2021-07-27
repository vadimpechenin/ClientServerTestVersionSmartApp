#kivy-приложение
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

import time
from client.clientModule import MySocket
from os.path import dirname, join, basename, isfile, getsize
from os import listdir
from threading import Thread


#Библиотека для всплывающих окон
from kivy.uix.popup import Popup
import io
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

#Библиотеки для многих страниц
from kivy.uix.screenmanager import ScreenManager, Screen

#Для чтения файлов с диска
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.factory import Factory

# Для всплывающих окон
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton

# Для размера окна
from kivy.core.window import Window

import cv2

# Библиотеки для формирования структуры пересылаемого сообщения
from message.messageStructure import MessageStructure
from message.messageStructureParameter import MessageStructureParameter
from message.messageResponceParameter import MessageResponceParameter


send_data=0
code_request0 = 0 #Специальный код, опеределяющий действия на сервере
code_request1 = 0 #Специальный код, опеределяющий QR или NN
filename_g = None
koef = 1
triggerPhoto = 1
ifTriggerPhotio = 3

triggerPhoto1 = 1
ifTriggerPhotio1 = 3
triggerPhoto2 = 1
workshop_number_list = []
lot_number_list = []
type_list = []

# Объект - запрос на сервер
messageParameter = MessageStructureParameter()
#Объект - ответ с сервера
messageResponce = MessageResponceParameter()

booleanPhoto = True
boolWorkchopLot = True

if (koef == 1):
    Window.size = (420, 800)
else:
    Window.size = (1100, 2300)

ciphers=[]
comments=[]
titleOfItems=['№','Дата изготовления','Месторасположение']
itemsOfDetails = [[1, '10.02.2021', 'Цех №1'], [3, '25.02.2021', 'Цех сбороки'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [12, '25.04.2021', 'Цех №10'], [13, '25.04.2021', 'Цех №4'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5'],
                  [8, '25.05.2021', 'Цех №1'], [10, '25.04.2021', 'Цех №3'], [11, '25.04.2021', 'Цех №5']
                 ]
#k=len(t)
#print(t[1][1])
for j in range(20):
    string_line = str(j+1) + '. Деталь ' + str(j+1)
    ciphers.append(string_line)
    string_line1= "### "+ str(j+1) + " ###"
    comments.append(string_line1)
listOfItems=True

resText = ''

#Искусственное заполнение ответа с сервера, нужно для формирования данных для фильтров
listOfItemsView = 0 #Переменная для обмена сообщениями с сервером в части отчетов
param_for_filter = 1  #С каким атрибутом работаем
ifTriggerReport = 0 #Прорисовка и обновление отчета по результатам запроса

#Подключение к серверу (1 точка для подключения)
sock = MySocket()
# Классы для окон

class MainWindow(Screen):

    def triggerForServer(self):
        global listOfItemsView
        # Метод для изменения переменных, отвечающих за запуск потока общения с сервером
        listOfItemsView = 2
        time.sleep(0.3)


class LoadDialog(Screen):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class QRWindow(Screen):
    # Класс для работы по отсылке фотографий
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(QRWindow, self).__init__(*args, **kwargs)
        #self.sock = MySocket()
        Thread(target=self.get_data).start()
        self.popup = None
        self.popup1 = None
        self.popup2 = None
        self.popup3 = None


    def allRequest(self):
        global filename_g, send_data, ifTriggerPhotio1, messageParameter
        ifTriggerPhotio1 = 3
        messageParameter.code_request0 = 1
        messageParameter.code_request1 = 1

        filename=[]
        #filename.append('D:\\2014 осень\\6_im.jpg')
        filename.append('D:\\2014spring\\1\\6_1.jpg')


        path = ''


        filename_g = []
        self.ImageLoad(path, filename)
        filename = []
        filename.append('D:\\2014spring\\1\\6_2.jpg')
        self.ImageLoad(path, filename)
        filename = []
        filename.append('D:\\2014spring\\1\\6_3.jpg')
        self.ImageLoad(path, filename)
        #filename_g = filename[0]

        send_data = 1


    def ImageLoad(self,path, filename):
        global filename_g, triggerPhoto1, ifTriggerPhotio1, messageParameter
        data = io.BytesIO(open(filename[0], "rb").read())
        # data = io.BytesIO(open("IMAGE.jpg", "rb").read())
        im = CoreImage(data, ext="png")
        if ifTriggerPhotio1==1:

            filename_g = filename[0]
            #Запись информации о дате для детали
            if (messageParameter.code_request0) == 2:
                reversed_name_of_data = ''
                reversed_string = ''
                if (len(filename[0]) >= 19):
                    for i in range(19):
                        reversed_name_of_data = reversed_name_of_data + filename[0][-i - 5]
                    reversed_string = reversed_name_of_data[::-1]
                messageParameter.nameOfImage = reversed_string
        else:

            filename_g.append(filename[0])

        file = cv2.imread(filename[0])

        sizeOfImage = getsize(filename[0])

        messageParameter.Images.append(file)
        messageParameter.sizeOfImages.append(sizeOfImage)


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
        #self.get_data()
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
        global messageParameter, messageResponce
        global sock
        while True:
            time.sleep(0.3)
            if (send_data==1):
                print('Зашел в отправку сообщения')
                #self.sock.send_data(messageParameter)
                sock.send_data(messageParameter)
                messageParameter = MessageStructure.ClearObject(messageParameter)
                send_data = 2
            if (send_data == 2):
                #messageResponce = self.sock.get_data()

                messageResponce = sock.get_data()
                send_data = 0
                if (messageResponce.message=='Изображение пришло'):
                    self.Responce_name_detail_popup()
                elif (messageResponce.message=='Список возможных месторасположений детали'):
                    self.Responce_location_popup()
                elif (messageResponce.message == 'Изменения внесены'):
                    self.Responce_name_detail_popup()

    """

    def get_data(self):
        global send_data
        global filename_g
        global code_request0, code_request1
        print('Зашел в отправку изображения')

        self.sock.get_data(filename_g, code_request0, code_request1)
    """
    # Блок с всплывающими окнами
    # Включение всплывающего окна
    def btn(self, *args):
        # create content and add to the popup
        global booleanPhoto, triggerPhoto2
        booleanPhoto = True
        triggerPhoto2 = 1
        self.ImageDel()
        PopupGrid = GridLayout(cols=2, size_hint_y=None)
        content2 = Button(text='QR', halign='left', size_hint=(0.4, 0.1), pos_hint={'x': 0.1, 'top': 0.1})
        PopupGrid.add_widget(content2)
        content3 = Button(text='Изображение', halign='left', size_hint=(0.4, 0.1), pos_hint={'x': 0.1, 'top': 0.1})
        PopupGrid.add_widget(content3)

        self.popup = Popup(title='Сделайте выбор', title_align='center', content=PopupGrid, auto_dismiss=False,
                           size_hint=(None, None), size=(int(300 * koef), int(200 * koef)))
        # bind the on_press event of the button to the dismiss function
        #
        content2.bind(on_press=self.QRPress_main)  # self.QRPress()
        content3.bind(on_press=self.imgPress)
        # open the popup
        self.popup.open()

    def QRPress_main(self, *args):
        global ifTriggerPhotio1
        global code_request0, code_request1, messageParameter
        print("QR")
        self.popup.dismiss()
        PopupGrid = GridLayout(cols=2, size_hint_y=None)
        content2 = Button(text='Тип детали', halign='left', size_hint=(0.4, 0.1), pos_hint={'x': 0.1, 'top': 0.1})
        PopupGrid.add_widget(content2)
        content3 = Button(text='Запись в базу', halign='left', size_hint=(0.4, 0.1), pos_hint={'x': 0.1, 'top': 0.1})
        PopupGrid.add_widget(content3)

        self.popup2 = Popup(title='Сделайте выбор', title_align='center', content=PopupGrid, auto_dismiss=False,
                           size_hint=(None, None), size=(int(300 * koef), int(200 * koef)))
        # bind the on_press event of the button to the dismiss function
        #
        content2.bind(on_press=self.QRPress_type)  # self.QRPress()
        content3.bind(on_press=self.QRPress_base_location_list)
        # open the popup
        self.popup2.open()

    def QRPress_type(self, *args):
        global ifTriggerPhotio1
        global code_request0, code_request1, messageParameter
        print("QR type")
        messageParameter.code_request0 = 1
        messageParameter.code_request1 = 0
        self.popup2.dismiss()
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

    def QRPress_base_location_list(self, *args):
        global ifTriggerPhotio1, send_data
        global code_request0, code_request1, messageParameter
        print("QR base")
        messageParameter.code_request0 = 3
        messageParameter.code_request1 = 0
        time.sleep(0.2)
        send_data = 1
        self.popup2.dismiss()


    def QRPress_base(self, *args):
        global ifTriggerPhotio1, send_data
        global code_request0, code_request1, messageParameter
        print("QR base")
        messageParameter.code_request0 = 2
        messageParameter.code_request1 = 0
        ifTriggerPhotio1 = 1
        PopupGrid = GridLayout(cols=1, pos_hint={'center_x': 0.6, 'center_y': 0.32})
        content4 = Button(text='Закрыть', halign='center', size=(int(200 * koef), int(50 * koef)),
                          size_hint=(None, None), pos=(int(50 * koef), int(50 * koef)), pos_hint=(None, None))
        PopupGrid.add_widget(content4)
        self.popup1 = Popup(title='Считайте QR', title_align='center', content=PopupGrid, auto_dismiss=False,
                            size_hint=(None, None), pos_hint={"center_x": 0.5, "top": 0.32},
                            size=(int(300 * koef), int(120 * koef)))
        content4.bind(on_press=self.closePopup)
        self.popup1.open()

    def imgPress(self, *args):
        global ifTriggerPhotio1, triggerPhoto1, triggerPhoto2
        global code_request0, code_request1
        print("Изображение")
        messageParameter.code_request0 = 1
        messageParameter.code_request1 = 1
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


    def Responce_name_detail_popup(self, *args):
        global messageResponce
        print("Ответ с сервера по типу детали")
        ifTriggerPhotio1 = 3
        PopupGrid = GridLayout(cols=1, pos_hint={'center_x': 0.6, 'center_y': 0.32})
        content4 = Button(text='Закрыть', halign='center', size=(int(200 * koef), int(50 * koef)),
                          size_hint=(None, None), pos=(int(50 * koef), int(50 * koef)), pos_hint=(None, None))
        PopupGrid.add_widget(content4)
        self.popup3 = Popup(title='Тип детали: ' + messageResponce.responce[0], title_align='center',
                            content=PopupGrid, auto_dismiss=False,
                            size_hint=(None, None), pos_hint={"center_x": 0.5, "top": 0.32},
                            size=(int(300 * koef), int(120 * koef)))
        # content4.bind(on_press=self.popup1.dismiss)
        content4.bind(on_press=self.closePopupResponce)
        self.popup3.open()

    def Responce_check_in_popup(self, *args):
        global messageResponce
        print("Ответ с сервера по изменению данных по детали")
        ifTriggerPhotio1 = 3
        PopupGrid = GridLayout(cols=1, pos_hint={'center_x': 0.6, 'center_y': 0.32})
        content4 = Button(text='Закрыть', halign='center', size=(int(200 * koef), int(50 * koef)),
                          size_hint=(None, None), pos=(int(50 * koef), int(50 * koef)), pos_hint=(None, None))
        PopupGrid.add_widget(content4)
        self.popup3 = Popup(title=messageResponce.responce[0], title_align='center',
                            content=PopupGrid, auto_dismiss=False,
                            size_hint=(None, None), pos_hint={"center_x": 0.5, "top": 0.32},
                            size=(int(300 * koef), int(120 * koef)))
        # content4.bind(on_press=self.popup1.dismiss)
        content4.bind(on_press=self.closePopupResponce)
        self.popup3.open()

    def Responce_location_popup(self, *args):
        global messageResponce, workshop_number_list, lot_number_list, boolWorkchopLot
        print("Ответ с сервера по спискам расположения деталей пришли")
        if boolWorkchopLot == True:
            workshop_number_list = []
            lot_number_list = []
            workshop_number_list = messageResponce.workshop_number_list
            lot_number_list = messageResponce.lot_number_list
            PopupGrid = GridLayout(cols=1, size_hint_y=None)
            # Убедимся, что высота такая, чтобы было что прокручивать.
            PopupGrid.bind(minimum_height=PopupGrid.setter('height'))
            self.toggle = [0 for _ in range(len(workshop_number_list))]

            for index in range(len(workshop_number_list)):
                self.toggle[index] = ToggleButton(
                    text=workshop_number_list[index], size_hint_y=None,
                    group='cipher', height=30 * koef,
                )
                self.toggle[index].bind(on_press=self.changer)
                PopupGrid.add_widget(self.toggle[index])
        else:
            PopupGrid = GridLayout(cols=1, size_hint_y=None)
            # Убедимся, что высота такая, чтобы было что прокручивать.
            PopupGrid.bind(minimum_height=PopupGrid.setter('height'))
            self.toggle = [0 for _ in range(len(lot_number_list))]

            for index in range(len(lot_number_list)):
                self.toggle[index] = ToggleButton(
                    text=lot_number_list[index], size_hint_y=None,
                    group='cipher', height=30 * koef,
                )
                self.toggle[index].bind(on_press=self.changer)
                PopupGrid.add_widget(self.toggle[index])

        self.popup3 = Popup(title='Выберите месторасположение детали', title_align='center',
                            content=PopupGrid, auto_dismiss=False,
                            size_hint=(None, None), pos_hint={"center_x": 0.5, "top": 0.32},
                            size=(int(300 * koef), int(120 * koef)))
        # content4.bind(on_press=self.popup1.dismiss)
        #content4.bind(on_press=self.closePopupResponceLocation)
        self.popup3.open()

    def changer(self, *args):
        global messageParameter, workshop_number_list, lot_number_list, boolWorkchopLot
        if boolWorkchopLot == True:
            for i in range(len(workshop_number_list)):
                if self.toggle[i].state == 'down':
                    messageParameter.workshopNumber = workshop_number_list[i]

            boolWorkchopLot = False
            self.popup3.dismiss()
            self.Responce_location_popup()
        else:
            for i in range(len(lot_number_list)):
                if self.toggle[i].state == 'down':
                    messageParameter.lotNumber = lot_number_list[i]
            boolWorkchopLot = True
            self.popup3.dismiss()
            self.closePopupResponceLocation()


    def closePopup(self, *args):
        self.popup1.dismiss()
        self.show_load()

    def closePopupResponce(self, *args):
        global messageResponce
        self.popup3.dismiss()
        messageResponce = MessageStructure.ClearObjectResponce(messageResponce)

    def closePopupResponceLocation(self, *args):
        global messageResponce
        self.popup3.dismiss()
        messageResponce = MessageStructure.ClearObjectResponce(messageResponce)
        self.QRPress_base()

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
        imgTime = time.strftime("%m_%d_%Y_%I_%M_%p")
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

class FourthWindow(Screen):
    #Окно для просмотра номенклатуры деталей
    def __init__(self, *args, **kwargs):
        super(FourthWindow, self).__init__(*args, **kwargs)
        self.listOfItems=True
    def ScrollWindow(self):
        if (self.listOfItems==True):
            #self.ids.ScrollWindowid.add_widget(ScrollView(size_hint=[1, 1]))
            self.ids.Scrollbuttonid.text = "Список номенклатуры выведен"
            leftGrid = GridLayout(cols=1, size_hint_y=None)
            #Убедимся, что высота такая, чтобы было что прокручивать.
            leftGrid.bind(minimum_height=leftGrid.setter('height'))

            self.toggle = [0 for _ in range(len(ciphers))]

            for index in range(len(ciphers)):
                self.toggle[index] = ToggleButton(
                    text=ciphers[index],  size_hint_y=None,
                    group='cipher', height=30*koef,
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
        global resText
        for i in range(len(ciphers)):
            if self.toggle[i].state == 'down':
                resText = comments[i]
        #Переход в конкретное описание детали
        self.manager.current = 'reportOfItem'
        #Переход окна вправо (текущее уходит влево)
        self.manager.transition.direction = "left"

class ReportsWindowDetail(Screen):
    def __init__(self, *args, **kwargs):
        super(ReportsWindowDetail, self).__init__(*args, **kwargs)
        self.listOfItems = True
    def windowDraw(self):
        if (self.listOfItems == True):
            self.ids.ButtonScrollWindowReportid.text = resText
            leftGrid1 = GridLayout(cols=len(titleOfItems), spacing=10, size_hint_y=None)#, size_hint_y=10, size_hint_x=10)
            # Убедимся, что высота такая, чтобы было что прокручивать.
            leftGrid1.bind(minimum_height=leftGrid1.setter('height'), minimum_width=leftGrid1.setter('width'))#
            self.toggle = []
            for i in range(len(itemsOfDetails)+1):
                nasted = []
                self.toggle.append(nasted)
                for j in range(len(itemsOfDetails[0])):
                    nasted.append('')

            for index in range(len(titleOfItems)):
                if (index == 0):
                    width = 50*koef
                else:
                    width = 150*koef

                self.toggle[0][index] = Label(
                size_hint_y=None,
                size_hint_x=None,
                height=40*koef,
                width=width,
                #,
                padding=(10*koef, 10*koef),
                    text=str(titleOfItems[index]),
                    color=(1, 1, 1, 1)
                    #text_size=(self.width, None)
                )
                with self.toggle[0][index].canvas.before:
                    Color(0, 1, 0, 0.25)
                    Rectangle(pos=self.toggle[0][index].pos, size=self.toggle[0][index].size)
                leftGrid1.add_widget(self.toggle[0][index])

            for index in range(1,len(itemsOfDetails)+1):
                for index1 in range(len(itemsOfDetails[0])):
                    if (index1 == 0):
                        width = 50*koef
                    else:
                        width = 150*koef

                    self.toggle[index][index1] = Label(
                        size_hint_y=None,
                        size_hint_x=None,
                        height=40*koef,
                        width=width,
                        #text_size=(self.width, None),
                        padding=(10*koef, 10*koef),
                        text=str(itemsOfDetails[index-1][index1]),
                        #text_size=(self.width, None)
                    )
                    leftGrid1.add_widget(self.toggle[index][index1])
            # Убедимся, что высота такая, чтобы было что прокручивать.
            leftGrid1.bind(minimum_height=leftGrid1.setter('height'), minimum_width=leftGrid1.setter('width'))
            self.ids.ScrollWindowReportid.add_widget(leftGrid1)
            self.listOfItems = False
        else:
            # удаляет все виджеты, которые находяться в another_box
            for i in range(len(self.ids.ScrollWindowReportid.children)):
                self.ids.ScrollWindowReportid.remove_widget(self.ids.ScrollWindowReportid.children[-1])
            self.listOfItems = True
        #pass
    def dellwidget(self):
        # удаляет все виджеты, которые находяться в another_box

        for i in range(len(self.ids.ScrollWindowReportid.children)):
            self.ids.ScrollWindowReportid.remove_widget(self.ids.ScrollWindowReportid.children[-1])
        self.ids.ButtonScrollWindowReportid.text = 'Нажмите'
        global resText
        resText = ''


class ReportsWindow(Screen):
    def __init__(self, *args, **kwargs):
        super(ReportsWindow, self).__init__(*args, **kwargs)
        #self.sock = MySocket()
        self.ciphers_filter = []
        Thread(target=self.textInInput).start()
        # self.textInInput()

    def textInInput(self):
        # Функция для вывода информации в текстовые окна приложения
        global messageParameter, messageResponce
        global listOfItemsView, ifTriggerReport
        global sock
        while True:
            time.sleep(0.4)
            if (listOfItemsView == 2):
                # Отправка запроса на сервер и получения ответа, заполняющего пределы для фильтров
                messageParameter.code_request0 = 5
                messageParameter.code_request1 = 0

                print('Зашел в отправку сообщения')
                #self.sock.send_data(messageParameter)
                sock.send_data(messageParameter)

                messageParameter = MessageStructure.ClearObject(messageParameter)
                listOfItemsView = 4
            if (listOfItemsView == 4):
                #messageResponce = self.sock.get_data()
                messageResponce = sock.get_data()
                if (messageResponce.message == 'Пределы для фильтров'):
                    listOfItemsView = 1
                    #pass

                """
                messageResponce.type_name_list = ['Деталь 1', 'Деталь 2', 'Деталь 3', 'Деталь 4', 'Деталь 5',
                                                  'Деталь 6']
                messageResponce.workshop_number_list = ['1', '2', '3', '4', '5', '6']
                messageResponce.lot_number_list = ['1', '2', '3']
                messageResponce.imbalance_list = [0, 5]
                messageResponce.diameter_list = [0, 10]
                """
                #listOfItemsView = 1

            if (listOfItemsView == 1):
                # Заполнение текстовых полей
                if len(messageParameter.type_name_list) > 0:
                    textstr = ''
                    for item in messageParameter.type_name_list:
                        textstr = textstr + item + '; '
                    self.ids.text_input1.text = textstr
                if len(messageParameter.workshop_number_list) > 0:
                    textstr = ''
                    for item in messageParameter.workshop_number_list:
                        textstr = textstr + item + '; '
                    self.ids.text_input2.text = textstr
                if len(messageParameter.lot_number_list) > 0:
                    textstr = ''
                    for item in messageParameter.lot_number_list:
                        textstr = textstr + item + '; '
                    self.ids.text_input3.text = textstr

                # Данные для ползунков
                self.ids.slider_d1.min = round(messageResponce.imbalance_list[0] - 0.05, 2)
                self.ids.slider_d1.max = round(messageResponce.imbalance_list[1] + 0.05, 2)
                self.ids.slider_d1.value = round(messageResponce.imbalance_list[0] - 0.05, 2)
                self.ids.slider_d2.min = round(messageResponce.imbalance_list[0] - 0.05, 2)
                self.ids.slider_d2.max = round(messageResponce.imbalance_list[1] + 0.05, 2)
                self.ids.slider_d2.value = round(messageResponce.imbalance_list[1] + 0.05, 2)

                self.ids.slider_d3.min = round(messageResponce.diameter_list[0] - 0.05, 2)
                self.ids.slider_d3.max = round(messageResponce.diameter_list[1] + 0.05, 2)
                self.ids.slider_d3.value = round(messageResponce.diameter_list[0] - 0.05, 2)
                self.ids.slider_d4.min = round(messageResponce.diameter_list[0] - 0.05, 2)
                self.ids.slider_d4.max = round(messageResponce.diameter_list[1] + 0.05, 2)
                self.ids.slider_d4.value = round(messageResponce.diameter_list[1] + 0.05, 2)

                listOfItemsView = 0

            if (listOfItemsView == 3):
                # Проверка нулевых значений перед отправкой. Если 0, или противоречивые - исправление
                if len(messageParameter.type_name_list) == 0:
                    messageParameter.type_name_list = messageResponce.type_name_list
                if len(messageParameter.workshop_number_list) == 0:
                    messageParameter.workshop_number_list = messageResponce.workshop_number_list
                if len(messageParameter.lot_number_list) == 0:
                    messageParameter.lot_number_list = messageResponce.lot_number_list

                # Отправка запроса на сервер для получения ответа для формирования отчета
                messageParameter.code_request0 = 6
                messageParameter.code_request1 = 0
                sock.send_data(messageParameter)

                messageParameter = MessageStructure.ClearObject(messageParameter)

                listOfItemsView = 5

            if (listOfItemsView == 5):
                # Получение ответа для формирования отчета
                messageResponce = sock.get_data()
                if (messageResponce.message == 'Отчет с учетом фильтров'):
                    """
                    messageResponce.report_list = [['ID', 'Тип', 'Дата', 'Цех', 'Участок', 'Дисбаланс', 'Диаметр'],
                                                   [1, 'Деталь 1', '1/1/2020 1:30 PM', '3', '2', 0.2, 5],
                                                   [10, 'Деталь 1', '10/5/2021 1:30 AM', '3', '2', 0.5, 5]]
                    """
                    listOfItemsView = 0
                    ifTriggerReport = 1

    def ScrollWindowFilterType(self):
        global param_for_filter
        param_for_filter = 1
        # Переход в конкретное описание детали
        self.manager.current = 'filterOfItem'
        # Переход окна вправо (текущее уходит влево)
        self.manager.transition.direction = "left"
        # self.ScrollWindowFilter()

    def ScrollWindowFilterWorkshop(self):
        global param_for_filter
        param_for_filter = 2
        # Переход в конкретное описание детали
        self.manager.current = 'filterOfItem'
        # Переход окна вправо (текущее уходит влево)
        self.manager.transition.direction = "left"
        # self.ScrollWindowFilter()

    def ScrollWindowFilterLot(self):
        global param_for_filter
        param_for_filter = 3
        # Переход в конкретное описание детали
        self.manager.current = 'filterOfItem'
        # Переход окна вправо (текущее уходит влево)
        self.manager.transition.direction = "left"
        # self.ScrollWindowFilter()

    def DataForReportAndDataFromDataBase(self):
        # Функция для формирования запроса и получения ответа по данным для отчета
        global listOfItemsView
        global messageParameter
        messageParameter.imbalance_list = []
        messageParameter.imbalance_list.append(round(self.ids.slider_d1.value, 2))
        messageParameter.imbalance_list.append(round(self.ids.slider_d2.value, 2))
        messageParameter.diameter_list = []
        messageParameter.diameter_list.append(round(self.ids.slider_d3.value, 2))
        messageParameter.diameter_list.append(round(self.ids.slider_d4.value, 2))
        listOfItemsView = 3

class FilterWindow(Screen):
    def __init__(self, *args, **kwargs):
        super(FilterWindow, self).__init__(*args, **kwargs)
        #self.ScrollWindowFilter()
        #Фильтр для чего применять (1 - тип, 2 - цех, 3 - участок)

    def ScrollWindowFilter(self):
        global param_for_filter

        global messageResponce, messageParameter
        if param_for_filter == 1:
            messageParameter.type_name_list = []
            self.ciphers_filter = messageResponce.type_name_list
        elif param_for_filter == 2:
            messageParameter.workshop_number_list = []
            self.ciphers_filter = messageResponce.workshop_number_list
        elif param_for_filter == 3:
            messageParameter.lot_number_list = []
            self.ciphers_filter = messageResponce.lot_number_list

        leftGrid = GridLayout(cols=1, size_hint_y=None)
        leftGrid.bind(minimum_height=leftGrid.setter('height'))

        leftGrid = GridLayout(cols=1, size_hint_y=None)
        #Убедимся, что высота такая, чтобы было что прокручивать.

        self.toggle = [0 for _ in range(len(self.ciphers_filter))]

        for index in range(len(self.ciphers_filter)):
            self.toggle[index] = ToggleButton(
                text= self.ciphers_filter[index],  size_hint_y=None,
                group= self.ciphers_filter[index], height=30*koef
                )
            #self.toggle[index].bind(on_press=self.changer)
            leftGrid.add_widget(self.toggle[index])

        self.ids.ScrollWindowFilterid.add_widget(leftGrid)

    def changerFilter(self, *args):
        global messageResponce, messageParameter
        global param_for_filter

        list_button_down = []
        for i in range(len( self.ciphers_filter)):
            if self.toggle[i].state == 'down':
                if param_for_filter == 1:
                    list_button_down.append(messageResponce.type_name_list[i])
                    messageParameter.type_name_list.append(messageResponce.type_name_list[i])
                if param_for_filter == 2:
                    list_button_down.append(messageResponce.workshop_number_list[i])
                    messageParameter.workshop_number_list.append(messageResponce.workshop_number_list[i])
                if param_for_filter == 3:
                    list_button_down.append(messageResponce.lot_number_list[i])
                    messageParameter.lot_number_list.append(messageResponce.lot_number_list[i])

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
                      auto_dismiss=False, size_hint=(None, None), size=(int(300 * koef), int(200 * koef)))

        content.bind(on_press=popup.dismiss)
        popup.open()

    def dellwidgetfilter(self):
        # удаляет все виджеты, которые находяться в another_box
        global listOfItemsView
        for i in range(len(self.ids.ScrollWindowFilterid.children)):
            self.ids.ScrollWindowFilterid.remove_widget(self.ids.ScrollWindowFilterid.children[-1])

        listOfItemsView = 1

class MainReport(Screen):
    def __init__(self, *args, **kwargs):
        super(MainReport, self).__init__(*args, **kwargs)

        Thread(target=self.threadWindowDrawMainReport).start()

    def threadWindowDrawMainReport(self):
        global messageParameter, messageResponce
        global ifTriggerReport
        while True:
            time.sleep(0.3)
            if (ifTriggerReport == 1):
                self.windowDrawMainReport()
                ifTriggerReport = 0

    def windowDrawMainReport(self):
        global messageResponce
        leftGrid1 = GridLayout(cols=len(messageResponce.report_list[0]), spacing=10,
                               size_hint_y=None)  # , size_hint_y=10, size_hint_x=10)
        # Убедимся, что высота такая, чтобы было что прокручивать.
        leftGrid1.bind(minimum_height=leftGrid1.setter('height'), minimum_width=leftGrid1.setter('width'))  #
        self.toggle = []
        for i in range(len(messageResponce.report_list)):
            nasted = []
            self.toggle.append(nasted)
            for j in range(len(messageResponce.report_list[0])):
                nasted.append('')
        for index in range(len(messageResponce.report_list[0])):
            if (index == 0):
                width = 50 * koef
            else:
                width = 150 * koef

            self.toggle[0][index] = Label(
                size_hint_y=None,
                size_hint_x=None,
                height=40 * koef,
                width=width,
                # ,
                padding=(10 * koef, 10 * koef),
                text=str(messageResponce.report_list[0][index]),
                color=(1, 1, 1, 1)
                # text_size=(self.width, None)
            )
            with self.toggle[0][index].canvas.before:
                Color(0, 1, 0, 0.25)
                Rectangle(pos=self.toggle[0][index].pos, size=self.toggle[0][index].size)
            leftGrid1.add_widget(self.toggle[0][index])

        for index in range(1, len(messageResponce.report_list)):
            for index1 in range(len(messageResponce.report_list[0])):
                if (index1 == 0):
                    width = 50 * koef
                else:
                    width = 150 * koef

                self.toggle[index][index1] = Label(
                    size_hint_y=None,
                    size_hint_x=None,
                    height=40 * koef,
                    width=width,
                    # text_size=(self.width, None),
                    padding=(10 * koef, 10 * koef),
                    text=str(messageResponce.report_list[index][index1]),
                    # text_size=(self.width, None)
                )
                leftGrid1.add_widget(self.toggle[index][index1])
            # Убедимся, что высота такая, чтобы было что прокручивать.
        leftGrid1.bind(minimum_height=leftGrid1.setter('height'), minimum_width=leftGrid1.setter('width'))
        self.ids.ScrollWindowReportMainid.add_widget(leftGrid1)

    def dellwidget(self):
        # удаляет все виджеты, которые находяться в another_box
        global ifTriggerReport, listOfItemsView
        for i in range(len(self.ids.ScrollWindowReportMainid.children)):
            self.ids.ScrollWindowReportMainid.remove_widget(self.ids.ScrollWindowReportMainid.children[-1])
        ifTriggerReport = 0
        listOfItemsView = 1

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

class CameraClick(Screen):

    def __init__(self, **kwargs):
        #send_data = 0
        super(CameraClick, self).__init__(**kwargs)
        self.fileName = None
        self.camera = None

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
        #timestr = time.strftime("%Y%m%d_%H%M%S")
        timestr = time.strftime("%m_%d_%Y_%I_%M_%p")
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
    title = 'Умный склад'

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