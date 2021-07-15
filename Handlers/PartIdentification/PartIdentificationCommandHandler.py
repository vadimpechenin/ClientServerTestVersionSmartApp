from Handlers.BaseCommandHandler import BaseCommandHandler
from Detections.NN_class import NN_detector

class PartIdentificationCommandHandler(BaseCommandHandler):
    def __init__(self, data_base,qrdet):
        self.data_base = data_base
        self.qrdet = qrdet
        # Класс для классификации с помощью нейронных сетей
        self.nndet = NN_detector()
        self.classification_model_nn = self.nndet.load_NN_model()  # загрузка модели классификации

    def execute(self, parameters):
        # Запрос к базе данных на получение списка видов деталей
        if (parameters.operation_type == 0):
            code = self.qrdet.main_detect(parameters.image)
        elif (parameters.operation_type == 1):
            code = self.nndet.classification_NN(parameters.image, self.classification_model_nn)
        # Запрос к базе данных на получение детали по id
        ciphers = self.data_base.search_for_id(code)
        return ciphers