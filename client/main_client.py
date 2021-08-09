#kivy-приложение для умного склада

#Импорт классов, отвечающих за бизнес-логику окон
from client.bootstrap import Bootstrap
from kivy.utils import platform

if __name__ == '__main__':

    if platform == 'android':
        from android.permissions import request_permissions, Permission

        request_permissions([
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.INTERNET,
        ])

    Bootstrap.initEnviroment()
    Bootstrap.run()
