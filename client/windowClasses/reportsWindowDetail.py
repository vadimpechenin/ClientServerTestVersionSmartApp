#Библиотеки для многих страниц
# Для всплывающих окон
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
import io
import cv2

from client.applicationEnvironment import appEnvironment

koef = 1

class ReportsWindowDetail(Screen):
    def __init__(self, *args, **kwargs):
        super(ReportsWindowDetail, self).__init__(*args, **kwargs)
        self.listOfItems = True
        # Объект - ответ с сервера
        self.messageResponce = None
        self.partName = ''
        appEnvironment.ReportsWindowDetailObj = self

    def fillData(self, partName, messageResponce):
        self.partName = partName
        self.messageResponce = messageResponce

    def windowDraw(self):
        #global messageResponce
        if (self.listOfItems == True) and (self.messageResponce!=None):
            img_str = cv2.imencode('.jpg', self.messageResponce.Images[0])[1].tostring()
            im_bytes = io.BytesIO(img_str)

            im = CoreImage(im_bytes, ext="png")
            self.ids.ImageBoxId2.add_widget(Image(texture=im.texture))

            self.ids.ButtonScrollWindowReportid.text = self.partName
            leftGrid1 = GridLayout(cols=2, spacing=10, size_hint_y=None)#, size_hint_y=10, size_hint_x=10)
            # Убедимся, что высота такая, чтобы было что прокручивать.
            leftGrid1.bind(minimum_height=leftGrid1.setter('height'), minimum_width=leftGrid1.setter('width'))#
            self.toggle = []
            for i in range(len(self.messageResponce.report_list)):
                nasted = []
                self.toggle.append(nasted)
                for j in range(len(self.messageResponce.report_list[0])):
                    nasted.append('')

            for index in range(len(self.messageResponce.report_list[0])):
                width = 200*koef

                self.toggle[0][index] = Label(
                size_hint_y=None,
                size_hint_x=None,
                height=40*koef,
                width=width,
                #,
                padding=(10*koef, 10*koef),
                    text=str(self.messageResponce.report_list[0][index]),
                )
                leftGrid1.add_widget(self.toggle[0][index])

                self.toggle[1][index] = Label(
                size_hint_y=None,
                size_hint_x=None,
                height=40*koef,
                width=width,
                #,
                padding=(10*koef, 10*koef),
                    text=str(self.messageResponce.report_list[1][index]),
                )
                leftGrid1.add_widget(self.toggle[1][index])

            # Убедимся, что высота такая, чтобы было что прокручивать.
            leftGrid1.bind(minimum_height=leftGrid1.setter('height'), minimum_width=leftGrid1.setter('width'))
            self.ids.ScrollWindowReportid.add_widget(leftGrid1)
            self.listOfItems = False
        else:
            # удаляет все виджеты, которые находяться в another_box
            for i in range(len(self.ids.ScrollWindowReportid.children)):
                self.ids.ScrollWindowReportid.remove_widget(self.ids.ScrollWindowReportid.children[-1])

            for i in range(len(self.ids.ImageBoxId2.children)):
                self.ids.ImageBoxId2.remove_widget(self.ids.ImageBoxId2.children[-1])

            self.listOfItems = True
        #pass

    def dellwidget(self):
        # удаляет все виджеты, которые находяться в another_box

        for i in range(len(self.ids.ScrollWindowReportid.children)):
            self.ids.ScrollWindowReportid.remove_widget(self.ids.ScrollWindowReportid.children[-1])

        for i in range(len(self.ids.ImageBoxId2.children)):
            self.ids.ImageBoxId2.remove_widget(self.ids.ImageBoxId2.children[-1])
        self.ids.ButtonScrollWindowReportid.text = 'Нажмите'
        self.messageResponce = None
        self.partName = ''

    def dellwidgetAll(self):
        # удаляет все виджеты, которые находяться в another_box

        for i in range(len(self.ids.ScrollWindowReportid.children)):
            self.ids.ScrollWindowReportid.remove_widget(self.ids.ScrollWindowReportid.children[-1])

        for i in range(len(self.ids.ImageBoxId2.children)):
            self.ids.ImageBoxId2.remove_widget(self.ids.ImageBoxId2.children[-1])

        self.ids.ButtonScrollWindowReportid.text = 'Нажмите'
        self.messageResponce = None
        self.partName = ''
        fourthTrigger = 1
        appEnvironment.FourthWindowObj.fillData(fourthTrigger)