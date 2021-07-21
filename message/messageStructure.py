import pickle

class MessageStructure:
    #Класс для упаковки данных в сообщении для сокетов (коды, картинки, сообщения)
    def __init__(self):
        pass

    @staticmethod
    def InitParameter(parameter):
        parameter.CommandCode = 12
        with open("1212.jpg", "rb") as image:
            imageContent = image.read()
            parameter.Images.append(imageContent)

        with open("1313.jpg", "rb") as image:
            imageContent = image.read()
            parameter.Images.append(imageContent)

    @staticmethod
    def SaveToBytes(parameter):
        result = pickle.dumps(parameter, pickle.HIGHEST_PROTOCOL)
        return result

    @staticmethod
    def RestoreFromBytes(parameterAsBytes):
        result = pickle.loads(parameterAsBytes)
        return result

    @staticmethod
    def ClearObject(parameter):
        parameter.code_request0 = 0
        parameter.code_request0 = 0
        parameter.Images = []
        parameter.sizeOfImages = []
        return parameter