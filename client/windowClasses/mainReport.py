from threading import Thread
from kivy.uix.screenmanager import Screen

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from client.applicationEnvironment import appEnvironment
import time


class MainReport(Screen):
    def __init__(self, *args, **kwargs):
        super(MainReport, self).__init__(*args, **kwargs)
        Thread(target=self.threadWindowDrawMainReport).start()
        # Объект - ответ с сервера
        self.messageResponce = None
        self.listOfItemsView = 0 #Переменная для обмена сообщениями с сервером в части отчетов
        self.ifTriggerReport = 0  # Прорисовка и обновление отчета по результатам запроса
        self.koef = appEnvironment.koef
        appEnvironment.MainReportObj = self

    def fillData(self, ifTriggerReport, listOfItemsView, messageResponce):
        self.ifTriggerReport = ifTriggerReport
        self.listOfItemsView = listOfItemsView
        self.messageResponce = messageResponce

    def threadWindowDrawMainReport(self):
        while True:
            time.sleep(0.3)
            if (self.ifTriggerReport == 1):
                self.windowDrawMainReport()
                self.ifTriggerReport = 0

    def windowDrawMainReport(self):
        leftGrid1 = GridLayout(cols=len(self.messageResponce.report_list[0]), spacing=10,
                               size_hint_y=None)  # , size_hint_y=10, size_hint_x=10)
        # Убедимся, что высота такая, чтобы было что прокручивать.
        leftGrid1.bind(minimum_height=leftGrid1.setter('height'), minimum_width=leftGrid1.setter('width'))  #
        self.toggle = []
        for i in range(len(self.messageResponce.report_list)):
            nasted = []
            self.toggle.append(nasted)
            for j in range(len(self.messageResponce.report_list[0])):
                nasted.append('')
        for index in range(len(self.messageResponce.report_list[0])):
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
                text=str(self.messageResponce.report_list[0][index]),
                #color=(1, 1, 1, 1)
                # text_size=(self.width, None)
            )
            #with self.toggle[0][index].canvas.before:
                #Color(0, 1, 0, 0.25)
                #Rectangle(pos=self.toggle[0][index].pos, size=self.toggle[0][index].size)
            leftGrid1.add_widget(self.toggle[0][index])

        for index in range(1, len(self.messageResponce.report_list)):
            for index1 in range(len(self.messageResponce.report_list[0])):
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
                    text=str(self.messageResponce.report_list[index][index1]),
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
        self.ifTriggerReport = 0
        self.listOfItemsView = 1