from Handlers.BaseCommandHandlerParameter import BaseCommandHandlerParameter

class LoadReportHandlerParameter(BaseCommandHandlerParameter):
    def __init__(self,type_name_list, workshop_number_list, lot_number_list, imbalance_list, diameter_list):
        self.type_name_list = type_name_list
        self.workshop_number_list = workshop_number_list
        self.lot_number_list = lot_number_list
        self.imbalance_list = imbalance_list
        self.diameter_list = diameter_list


