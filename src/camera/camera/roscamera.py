import rclpy  # Python Client Library for ROS 2
from rclpy.node import Node  # Handles the creation of nodes
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
from rclpy.executors import MultiThreadedExecutor
import cv2 # OpenCV library
from pathlib import Path
from typing import Any
from custom_interfaces.srv import CameraFrame

"""
Function returns a list of working camera IDs to capture every camera connected to the robot
"""
def getCameras() -> list[int]:
    nonWorkingPorts = 0
    devPort = 0
    workingPorts = []

    while nonWorkingPorts < 6:
        camera = cv2.VideoCapture(devPort)
        if not camera.isOpened():
            nonWorkingPorts += 1
        else:
            isReading, img = camera.read()
            _ = camera.get(3)
            _ = camera.get(4)
            if isReading:
                workingPorts.append(devPort)
        
        devPort += 1
    
    return workingPorts


class RosCamera(Node):
    def __init__(self, frameServiceName: str, cameraID: int) -> None:
        super().__init__("ros_camera")
        self.get_logger().info("Launching roscamera node")
        self.get_logger().info("Using cameraID: " + str(cameraID))
        
        self.frame_service = self.create_service(
            CameraFrame, frameServiceName, self.frameServiceHandler
        )
        
        # The argument '0' gets the default webcam.
        self.cap = cv2.VideoCapture(cameraID)

        # Used to convert between ROS and OpenCV images
        self.br = CvBridge()
        
        self.cameraID = cameraID # Store camera ID
    
    """
    Callback function of frame service. Returns a CompressedImage as a response.
    
    Request parameter is defined as an int, however, this is not used because
    the client can choose which camera service to request frames from.
        ex. (list of service names and corresponding cameraID)
            /get_video_frames0 -> cameraID: 0
            /get_video_frames1 -> cameraID: 1
            /get_video_frames2 -> cameraID: 2
                and so on...
    """
    def frameServiceHandler(self, _: Any, response: CameraFrame.Response) -> CameraFrame.Response:
        # Capture frame-by-frame
        # This method returns True/False as well as the video frame.
        ret, frame = self.cap.read()
            
        if ret: 
            # Assign compressed frame data to the response message.
            response.frame = self.br.cv2_to_compressed_imgmsg(frame)
        else:
            self.get_logger().info("From camera" + str(self.cameraID) + ": failed to capture!")

        return response
            

def main(args=None):
    rclpy.init(args=args)
    try:
        # We need an executor because running .spin() is a blocking function.
        # using the MultiThreadedExecutor, we can control multiple nodes
        executor = MultiThreadedExecutor()
        nodes = []
        cameraNumber = 0

        for cameraID in getCameras():
            node = RosCamera("get_video_frames" + str(cameraNumber), cameraID)
            nodes.append(node)
            executor.add_node(node)
            cameraNumber += 1
        
        try:
            executor.spin()
        finally:
            executor.shutdown()
            for node in nodes:
                node.destroy_node()
        
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()
