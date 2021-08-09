'''
Example of an Android filechooser.
'''
from __future__ import unicode_literals


from plyer import filechooser

from client.applicationEnvironment import appEnvironment
from kivy.properties import ListProperty


#Библиотеки для многих страниц
from kivy.uix.screenmanager import Screen


class FileChoose(Screen):
    '''
    Button that triggers 'filechooser.open_file()' and processes
    the data response from filechooser Activity.
    '''

    def __init__(self, *args, **kwargs):
        super(FileChoose, self).__init__(*args, **kwargs)
        #self.fileName = None
        self.selection = []
        appEnvironment.FileChooseObj = self
        #self.shoose()

    def choose(self):
        '''
        Call plyer filechooser API to run a filechooser Activity.
        '''
        filechooser.open_file(on_selection=self.handle_selection)
        #self.ids.result.text = str(self.selection)

    def handle_selection(self, selection):
        '''
        Callback function for handling the selection response from Activity.
        '''
        self.selection.extend(selection)

    def clear_selection(self):
        '''
        Callback function for handling the selection response from Activity.
        '''
        self.selection = []