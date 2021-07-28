#Библиотеки для многих страниц
# Для всплывающих окон
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

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
            self.ids.ButtonScrollWindowReportid.text = self.partName
            leftGrid1 = GridLayout(cols=len(self.messageResponce.report_list[0]), spacing=10, size_hint_y=None)#, size_hint_y=10, size_hint_x=10)
            # Убедимся, что высота такая, чтобы было что прокручивать.
            leftGrid1.bind(minimum_height=leftGrid1.setter('height'), minimum_width=leftGrid1.setter('width'))#
            self.toggle = []
            for i in range(len(self.messageResponce.report_list)):
                nasted = []
                self.toggle.append(nasted)
                for j in range(len(self.messageResponce.report_list[0])):
                    nasted.append('')

            for index in range(len(self.messageResponce.report_list[0])):
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
                    text=str(self.messageResponce.report_list[0][index]),
                    #color=(1, 1, 1, 1)
                    #text_size=(self.width, None)
                )
                #with self.toggle[0][index].canvas.before:
                    #Color(0, 1, 0, 0.25)
                    #Rectangle(pos=self.toggle[0][index].pos, size=self.toggle[0][index].size)
                leftGrid1.add_widget(self.toggle[0][index])

            for index in range(1,len(self.messageResponce.report_list)):
                for index1 in range(len(self.messageResponce.report_list[0])):
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
                        text=str(self.messageResponce.report_list[index][index1]),
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
        self.messageResponce = None
        self.partName = ''