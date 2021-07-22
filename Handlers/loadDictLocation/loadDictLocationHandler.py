from Handlers.BaseCommandHandler import BaseCommandHandler

class LoadDictLocationHandler(BaseCommandHandler):
    def __init__(self,data_base):
        self.data_base = data_base

    def execute(self,parameters):
        # Запрос к базе данных на получение списка видов деталей
        g = parameters.operation_type
        ciphers = self.data_base.list_of_workshop_lot()
        return ciphers