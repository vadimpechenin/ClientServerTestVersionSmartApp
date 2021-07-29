#kivy-приложение для умного склада

#Импорт классов, отвечающих за бизнес-логику окон
from client.bootstrap import Bootstrap


if __name__ == '__main__':
    Bootstrap.initEnviroment()
    Bootstrap.run()
