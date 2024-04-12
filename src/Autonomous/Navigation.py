import serial

class GPSComms():
    def __init__(self, port, baud):
        self.comPort = port
        self.buadrate = baud
        self.GPSkeys = ['GPRMC', 'GPRMB']


    def checkSignal(self):
        self.info = serial.serial(self.comPort, self.buadrate, timeout=2)

        if self.info:
            received = str(self.info.readline())

            if received is not 'None' and self.GPSkeys in received:
                '''Check key sentences for needed information'''
                if self.GPSkeys[0] in received:
                    #currentLat, currentLong, theta =
                    ...

                if self.GPSkeys[1] in received:
                    #do thing
                    ...
                
                return received #change this to latitude, longitude, and bearing
            
        else:
            print("Could not connect to serial...")
            return -1

        return self.result
    
    def closeConnection(self):
        self.info.close()

    def latitude(self):
        pass

    def longitude(self):
        pass
