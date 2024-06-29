import sys
import rclpy
from rclpy.node import Node
import moteus
import threading
from . import moteus_thread_manager
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import String, Float32
from usb.core import find as finddev

import sys
sys.path.append("/home/trickfire/urc-2023/src")

from utility.color_text import ColorCodes
from utility.canbus_mappings import CanBusMappings

class RosMotuesBridge(Node):
    """
        This is the node that connects the Moteus Motor Controllers
        with the rest of the ROS codebase. You can easily add new
        motors using the addMotor() function from the self.threadManager.
        
        You can attempt to reconnect to the Moteus Controllers during runtime.
        The CANFD-USB is reset every time the code is execute from the ./launch.sh
    """
    
    def __init__(self):
        super().__init__("can_moteus_node")
        self.get_logger().info(ColorCodes.BLUE_OK + "Launching can_moteus node" + ColorCodes.ENDC)
        
        
        # Reset the CANFD-USB
        # run "lsusb" in cmd with the CANFD-USB connected
        # to find the idVendor and the idProduct
        dev = finddev(idVendor=0x0483, idProduct=0x5740)
        dev.reset()
        

        self.threadManager = None
        self.canbusMappings = CanBusMappings()
        
        self.reconnectToMoteusSub = self.create_subscription(Float32, "reconnectMoteusControllers", self.reconnect, 1)
        
        self.createMoteusMotors()
        
    def reconnect(self, msg):
        """
            Gracefully shuts down the threadManager and creates a new instance of 
            the threadManager object.
        
        """
        self.get_logger().info("Reconnecting")
        self.threadManager.reconnectMotors()

    def createMoteusMotors(self):
        """
            Creates the threadManager and adds all the moteus motors
        """
        
        
        self.threadManager = moteus_thread_manager.MoteusThreadManager(self)
        
        self.threadManager.addMotor(self.canbusMappings.CANID_REAR_RIGHT_DRIVE_MOTOR, "rear_right_drive_motor")
        self.threadManager.addMotor(self.canbusMappings.CANID_MID_RIGHT_DRIVE_MOTOR, "mid_right_drive_motor")
        self.threadManager.addMotor(self.canbusMappings.CANID_FRONT_RIGHT_DRIVE_MOTOR, "front_right_drive_motor")
        
        self.threadManager.addMotor(self.canbusMappings.CANID_REAR_LEFT_DRIVE_MOTOR, "rear_left_drive_motor")
        self.threadManager.addMotor(self.canbusMappings.CANID_MID_LEFT_DRIVE_MOTOR, "mid_left_drive_motor")
        self.threadManager.addMotor(self.canbusMappings.CANID_FRONT_LEFT_DRIVE_MOTOR, "front_left_drive_motor")

        self.threadManager.start()
        
        
        

def main(args=None):
    """
        The entry point of the node.
    """
    
    rclpy.init(args=args)
    try:
        node = RosMotuesBridge()
        rclpy.spin(node)
    
    except KeyboardInterrupt:
        pass
    except ExternalShutdownException:
        # This is done when we ctrl-c the progam to shut it down
        node.get_logger().info(ColorCodes.BLUE_OK + "Shutting down can_moteus" + ColorCodes.ENDC)
        node.threadManager.terminateAllThreads()
        node.destroy_node()
        sys.exit(0)

if __name__ == "__main__":
    main()