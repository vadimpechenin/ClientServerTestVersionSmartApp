from Handlers.BaseCommandHandler import BaseCommandHandler

class CheckInCommandHandler(BaseCommandHandler):
    def __init__(self, data_base,qrdet):
        self.data_base = data_base
        self.qrdet = qrdet

    def execute(self, parameters):
        code = self.qrdet.main_detect(parameters.image)
        # Запрос к базе данных на внесение изменений по id
        ciphers = self.data_base.updata_for_id(code)
        return ciphers