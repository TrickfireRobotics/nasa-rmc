import serial

class GPSComms():
    def __init__(self, port, baud):
        self.comPort = port
        self.buadrate = baud

    def startReceiving(self):
        self.result = serial.serial(self.comPort, self.buadrate, timeout=2)
        return self.result
    
    def closeConnection(self):
        self.result.close()

    def latitude(self):
        pass

    def longitude(self):
        pass
