import launch
from launch_ros.actions import Node

can_moteus_node = Node(package="can_moteus", executable="can_moteus", name="can_moteus_node")


drivebase_node = Node(package="drivebase", executable="drivebase", name="drivebase_node")


mission_control_updater_node = Node(
    package="mission_control_updater",
    executable="mission_control_updater",
    name="mission_control_updater_node",
)

arm_node = Node(package="arm", executable="arm", name="arm_node")

heartbeat_node = Node(package="heartbeat", executable="heartbeat", name="heartbeat_node")

# This is the example node. It will show ROS timers, subscribers, and publishers
# To include it in the startup, add it to the array in the generate_launch_description() method
example_node = Node(package="example_node", executable="myExampleNode", name="my_example_node")


def generate_launch_description() -> launch.LaunchDescription:  # pylint: disable=invalid-name
    return launch.LaunchDescription(
        [can_moteus_node, drivebase_node, mission_control_updater_node, arm_node, heartbeat_node]
    )
