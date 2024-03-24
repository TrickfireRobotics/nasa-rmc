import cv2

class ArUcoProcessing:
    def __init__(self, _img):
        self.img = cv2.imread(_img)

        arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        arucoParams = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

        self.corners = None
        self.tagID = None

    def detectTags(self):
        (corn, ids, rejects) = self.detector.detectMarkers(self.img)
        self.corners = corn
        self.tagID = ids

        if len(corn) > 0:
            ids = ids.flatten()

            for (markerCorn, markerId) in zip(corn, ids):
                corners = markerCorn.reshape((4, 2))
                (topL, topR, bottomR, bottomL) = corners

                topR = (int(topR[0]), int(topR[1]))
                topL = (int(topL[0]), int(topL[1]))
                bottomL = (int(bottomL[0]), int(bottomL[1]))
                bottomR = (int(bottomR[0]), int(bottomR[1]))

                cv2.line(self.img, topL, topR, (0, 255, 0), 2)
                cv2.line(self.img, topR, bottomR, (0, 255, 0), 2)
                cv2.line(self.img, bottomR, bottomL, (0, 255, 0), 2)
                cv2.line(self.img, bottomL, topL, (0, 255, 0), 2)

                cv2.putText(self.img, str(markerId), (topL[0], topL[1]-15), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 0), 2)

        return self.img

    def getTagID(self):
        return self.tagID
    
    def xPos(self):
        for arr in self.corners:
            for coor in arr:
                (TL, TR, BR, BL) = coor
                avgx = int((TL[0] + TR[0])/2)
                avgy = int((TL[1] + BL[1])/2)
                print("avg x: {}, avg y: {}".format(avgx, avgy))
                cv2.circle(self.img, (avgx, avgy), 4, (0, 0, 255), -1)

        return (self.img, avgx)
    

if __name__ == "__main__":
    classify = ArUcoProcessing("C:\\Users\\richa\\Desktop\\Python\\ARUCO Tags\\testing.jpg")
    cv2.imshow("test", classify.detectTags())
    cv2.waitKey(0)
    print(classify.getTagID())

    cv2.imshow("test", classify.xPos()[0])
    cv2.waitKey(0)
