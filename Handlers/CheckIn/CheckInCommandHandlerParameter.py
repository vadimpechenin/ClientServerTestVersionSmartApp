from Handlers.BaseCommandHandlerParameter import BaseCommandHandlerParameter

class CheckInCommandHandlerParameter(BaseCommandHandlerParameter):
    def __init__(self,image, operation_type, date_time, workshop, lot):
        self.image = image
        self.operation_type = operation_type
        self.date_time = date_time
        self.workshop = workshop
        self.lot = lot