from Handlers.BaseCommandHandlerParameter import BaseCommandHandlerParameter

class LoadDictLocationHandlerParameter(BaseCommandHandlerParameter):
    def __init__(self,operation_type):
        self.operation_type = operation_type