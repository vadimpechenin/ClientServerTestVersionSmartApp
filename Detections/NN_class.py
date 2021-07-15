"""
Класс для определения типа деталей с фотографий с помощью сверточных нейронных сетей
"""

import numpy as np
from os.path import dirname, join, basename, isfile
import cv2

net_file_name = "D:\\PYTHON\\Programms\\Smart_app_UMNIK\\Server_version\\NN_save"


class NN_detector():
    def __init__(self):
        self.pl_real_photo = 1  # загрузка теста реальных фотографий
        self.pl_depth = 3  # Если используются проекции, то есть 112*112*3
        self.num_classes = 5
        self.size_of_image = (112, 112)
        self.optimizer = ['sgd', 'adam']

    def load_NN_model(self):
        global net_file_name
        from keras.models import model_from_json

        print("Загружаю сеть из файлов")
        # Загружаем данные об архитектуре сети
        name_NN_json = "Classification_stl_2021_2VGG_" + str(self.pl_depth) + ".json"
        path_NN_json = join(net_file_name, name_NN_json)
        json_file = open(path_NN_json, "r")
        loaded_model_json = json_file.read()
        json_file.close()
        # Создаем модель
        model = model_from_json(loaded_model_json)
        # Загружаем сохраненные веса в модель
        name_NN_h5 = "Classification_stl_2021_2VGG_" + str(self.pl_depth) + ".h5"
        path_NN_h5 = join(net_file_name, name_NN_h5)
        model.load_weights(path_NN_h5)
        print("Загрузка сети завершена")
        # Компилируем загруженную модель
        model.compile(loss='categorical_crossentropy', optimizer=self.optimizer[1],
                      metrics=['accuracy'])

        return model

    def classification_NN(self,image,model):
        Xv = self.load_image(image)
        c = model.predict(Xv)
        class_result = np.argmax(c)
        return class_result

    def load_image(self,image):
        # Загрузка и сохранение изображений
        features = []
        for i in range(3):
            f = image[i,:,:,:]
            gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
            fr = cv2.resize(gray, self.size_of_image)
            features.append(fr)

        X = np.array(features)
        Xv = self.reshape_data_VGG_2021_3D(X, 1, self.size_of_image)
        return Xv

    def reshape_data_VGG_2021_3D(self, X, N, size_of_image):
        Xt = np.zeros((N, size_of_image[0], size_of_image[1], 3))
        for i in range(N):
            Xt[i, :, :, 0] = cv2.resize(X[0, :, :], size_of_image).astype(np.float32)
            Xt[i, :, :, 1] = cv2.resize(X[1, :, :], size_of_image).astype(np.float32)
            Xt[i, :, :, 2] = cv2.resize(X[2, :, :], size_of_image).astype(np.float32)
        Xt = Xt / Xt.max()

        return Xt








