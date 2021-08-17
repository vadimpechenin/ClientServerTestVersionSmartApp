import copy

class ClientProxyParameters():

    def __init__(self):
        self.HOST = ''
        self.PORT = 0

    def copyFrom(self,right):
        #Скопировать данные из right в текущий класс
        self.HOST = right.HOST
        self.PORT = right.PORT
