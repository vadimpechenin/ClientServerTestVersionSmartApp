from kivy.app import App
from kivy.lang import Builder
from os.path import dirname, join, basename, isfile, getsize
from os import listdir
from client.applicationEnvironment import appEnvironment


class SmartAppClient(App):
    title = 'Умный склад'

    def build(self):
        return appEnvironment.kv
        #return CameraClick()

    # Метод для кодировки русских символов в описании
    def load_all_kv_files(self, directory_kv_files):
        for kv_file in listdir(directory_kv_files):
            kv_file = join(directory_kv_files, kv_file)
            if isfile(kv_file) and kv_file.endswith("kv"):
                with open(kv_file, encoding="utf-8") as kv:
                    Builder.load_string(kv.read())