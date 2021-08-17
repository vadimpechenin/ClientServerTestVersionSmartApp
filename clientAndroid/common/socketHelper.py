

class SocketHelper:
    INT_VALUE_SIZE_IN_BYTES = 8

    def __init__(self,sock):
        self.sock = sock


    def writeInt(self,value):
        #Метод отправки целого числа в сокет
        valueInBytes = value.to_bytes(self.INT_VALUE_SIZE_IN_BYTES, byteorder='big')
        print('Отосланные байты числа: ' + str(value) + ' : ' + str(valueInBytes))
        self.writeBytesArray(valueInBytes)

    def readInt(self):
        #Метод приема целого числа из сокета
        valueInBytes = self.readBytesArray(self.INT_VALUE_SIZE_IN_BYTES)
        print('Прочитанные байты числа: ' + str(valueInBytes))
        value = int.from_bytes(valueInBytes, byteorder='big')
        return value

    def writeBytesArray(self, data):
        # Запись массива байт в сокет
        self.sock.sendall(data)

    def readBytesArray(self, dataSize):
        # Чтение массива байт из сокета
        data = bytearray()
        while len(data) < dataSize:
            partSize = dataSize - len(data)
            data+=self.sock.recv(partSize)
        return bytes(data)
