import Navigation as nv
import AruCoLib as AL

def getGPSCoordinates(GPSLoc):
    '''Looks for the JSON file that contains the necessary GPS coordinates and returns them.
       Input: JSON file location
       Output: GPS coordinates array
    '''
    pass

def calculateHeading(visual=False, GLL=None, pixLoc=None):
    '''Calculates which direction to go based on inputs.
       Inputs: visual (true/false), GLL (GPS lat and long), pixLoc (pixel location in image)
       Output: will figure that out when i start ROS stuff
    '''
    pass

def main():
    GPSSentence1 = ""
    GPSSentence2 = ""
    GPSCoor = []
    arrivalFlag = 0

    GPS1 = nv.GPSComms("/dev/tty0", 9600).startReceiving()
    GPS2 = nv.GPSComms("/dev/tty1", 9600).startReceiving()

    # main loop for the given coordinates
    for destination in GPSCoor:
        GPSSentence1 = GPS1.read() # read until end character
        GPSSentence2 = GPS2.read() # read until end character
    pass

if __name__ == "__main__":
    main()