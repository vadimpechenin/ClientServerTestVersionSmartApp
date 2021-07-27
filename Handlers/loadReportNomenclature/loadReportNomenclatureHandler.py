from Handlers.BaseCommandHandler import BaseCommandHandler

class LoadReportNomenclatureHandler(BaseCommandHandler):
    def __init__(self, data_base):
        self.data_base = data_base

    def execute(self, parameters):
        # Запрос к базе данных на получение данных для отчета
        ciphers = self.data_base.data_for_report_nomenclature(parameters)
        return ciphers