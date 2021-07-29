from kivy.uix.screenmanager import Screen
# Для всплывающих окон
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from client.applicationEnvironment import appEnvironment

class FilterWindow(Screen):
    def __init__(self, *args, **kwargs):
        super(FilterWindow, self).__init__(*args, **kwargs)
        self.listOfItems = True
        self.param_for_filter = 1  #С каким атрибутом работаем
        # Объект - ответ с сервера
        self.messageResponce = None
        # Объект - запрос на сервер
        self.messageParameter = None
        appEnvironment.FilterWindowObj = self
        self.koef = appEnvironment.koef

    def fillData(self, param_for_filter, messageResponce, messageParameter):
        # Фильтр для чего применять (1 - тип, 2 - цех, 3 - участок)
        self.param_for_filter = param_for_filter
        self.messageResponce = messageResponce
        self.messageParameter = messageParameter

    def ScrollWindowFilter(self):
        if self.param_for_filter == 1:
            self.messageParameter.type_name_list = []
            self.ciphers_filter = self.messageResponce.type_name_list
        elif self.param_for_filter == 2:
            self.messageParameter.workshop_number_list = []
            self.ciphers_filter = self.messageResponce.workshop_number_list
        elif self.param_for_filter == 3:
            self.messageParameter.lot_number_list = []
            self.ciphers_filter = self.messageResponce.lot_number_list

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
        for i in range(len( self.ciphers_filter)):
            if self.toggle[i].state == 'down':
                if self.param_for_filter == 1:
                    list_button_down.append(self.messageResponce.type_name_list[i])
                    self.messageParameter.type_name_list.append(self.messageResponce.type_name_list[i])
                if self.param_for_filter == 2:
                    list_button_down.append(self.messageResponce.workshop_number_list[i])
                    self.messageParameter.workshop_number_list.append(self.messageResponce.workshop_number_list[i])
                if self.param_for_filter == 3:
                    list_button_down.append(self.messageResponce.lot_number_list[i])
                    self.messageParameter.lot_number_list.append(self.messageResponce.lot_number_list[i])

        appEnvironment.ReportsWindowObj.fillDataFilter(self.listOfItemsView, self.messageParameter)
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

        self.listOfItemsView = 1
