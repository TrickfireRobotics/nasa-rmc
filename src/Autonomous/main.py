import Navigation as nv


def main():
    GPSSentence1 = ""
    GPSSentence2 = ""
    GPSCoor = []
    arrivalFlag = 0

    GPS1 = nv.GPSComms("/dev/tty0", 9600).startReceiving()
    GPS2 = nv.GPSComms("/dev/tty1", 9600).startReceiving()

    for destination in GPSCoor:
        GPSSentence1 = GPS1.read() # read until end character
        GPSSentence2 = GPS2.read() # read until end character
    pass

if __name__ == "__main__":
    main()