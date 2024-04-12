import math
import numpy as np
import Navigation as nv
#import AruCoLib as AL

def getGPSCoordinates(GPSLoc):
    '''Looks for the JSON file that contains the necessary GPS coordinates and returns them.
       Input: JSON file location
       Output: GPS coordinates array
    '''
    
    pass

def calculateHeading(visual=False, GLL: list[list[float]]=None, pixLoc=None):
    '''Calculates which direction to go based on inputs.
       Inputs: visual (true/false), GLL (current GPS lat and long, dest GPS lat and long), pixLoc (pixel location in image)
       Output: will figure that out when i start ROS stuff
    '''
    currentPos = GLL[0]
    destinationPos = GLL[1]

    dir = headingDir(currentPos, destinationPos)

    print("CurrentPos: {}, destination: {}".format(currentPos, destinationPos))

    currentAng = 0
    print("CurrentAng: {}".format(currentAng))

    currentDir = [math.cos(currentAng), math.sin(currentAng)]
    currentDir = [p/coordinateNorm(currentPos) for p in currentDir]
    print("Current direction: {}".format(currentDir))

    targetDir = [destinationPos[0]-currentPos[0], destinationPos[1]-currentPos[1]]
    #targetDir = [destinationPos[0], destinationPos[1]]
    targetDir = [p/coordinateNorm(destinationPos) for p in targetDir]
    print("Target point direction: {}".format(targetDir))

    delta = math.atan(np.linalg.norm(np.cross(targetDir, currentDir))/np.dot(targetDir, currentDir))
    print("delta: {}".format(dir*math.degrees(delta)))
    
    return delta

def coordinateNorm(point: list[float]):
    return math.sqrt((point[0]**2)+(point[1]**2))

def headingDir(GLLc: list[float]=None, GLLt: list[float]=None):
    if GLLc[1] > GLLt[1]:
        return -1
    elif GLLc[1] < GLLt[1]:
        return 1
    else:
        return 1
    
'''
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
    pass'''

if __name__ == "__main__":
    #main()
    calculateHeading(GLL=[[10.0, 6.0], [4.0, 5.0]])