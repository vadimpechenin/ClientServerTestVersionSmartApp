"""
Серверный класс для проекта "Умный Склад", в котором реализованы три метода:
checkIn детали - зафиксировать место и время детали по QR коду
protocolRequest - вызов протокола для клиента
partIdentification - определение типа детали (по QR или нейронным сетям)
"""

#Классы для работы приложения
from Detections.QR_detector import QR_detector
from Detections.NN_class import NN_detector

from db.sql_data_base import SQL_data_base

from Handlers.BaseCommandHandler import BaseCommandHandler
from Handlers.NomRequest.NomRequestCommandHandler import NomRequestCommandHandler
from Handlers.PartIdentification.PartIdentificationCommandHandler import PartIdentificationCommandHandler
from Handlers.CheckIn.CheckInCommandHandler import CheckInCommandHandler
from Handlers.loadDictLocation.loadDictLocationHandler import LoadDictLocationHandler
from Handlers.loadDictType.loadDictTypeHandler import LoadDictTypeHandler
from Handlers.loadAllCharacteristics.loadAllCharacteristicsHandler import LoadAllCharacteristicsHandler
from Handlers.loadReport.loadReportHandler import LoadReportHandler
from Handlers.loadReportNomenclature.loadReportNomenclatureHandler import LoadReportNomenclatureHandler

class MainCommandHandler(BaseCommandHandler):
    def __init__(self):
        id = 1
        pl_table = [1, 1, 1, 1, 1]
        imbalance_tolerance = 3
        self.data_base = SQL_data_base(id, pl_table, imbalance_tolerance)
        #self.data_base.table_create()
        self.data_base.create_session()
        #self.data_base.init_repletion_data_base()
        # Класс для обработки QR
        self.qrdet = QR_detector()
        self.dict={}
        self.dict[0] = NomRequestCommandHandler(self.data_base)
        self.dict[1] = PartIdentificationCommandHandler(self.data_base,self.qrdet)
        self.dict[2] = CheckInCommandHandler(self.data_base, self.qrdet)
        self.dict[3] = LoadDictLocationHandler(self.data_base)
        self.dict[4] = LoadDictTypeHandler(self.data_base)
        self.dict[5] = LoadAllCharacteristicsHandler(self.data_base)
        self.dict[6] = LoadReportHandler(self.data_base)
        self.dict[7] = LoadReportNomenclatureHandler(self.data_base)

    def initFunction(self,code_request, parameter):
        result = None
        if code_request in self.dict:
            handler = self.dict[code_request]
            result = handler.execute(parameter)

        return result