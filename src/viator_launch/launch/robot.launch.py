import launch
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

hello_node = ComposableNode(
    package='hello_world',
    plugin='hello_world::hello_node',
    name='hello_node'
)

testing_node = Node(
    package='interface',
    executable='testingNode',
    name='testing_node'
)

# Composable Nodes launched in a Composable Node container will share a process
# and can use very fast inter-process communication instead of publishing
# messages over a network socket.
# Note: "Composable Node container" does not mean "Docker-like container".
robot_container = ComposableNodeContainer(
    name='robot',
    package='rclcpp_components',
    namespace='',
    executable='component_container',
    composable_node_descriptions=[
        hello_node
    ],
    output='screen',
    emulate_tty=True
)


def generate_launch_description():
    return launch.LaunchDescription([
        robot_container, testing_node
    ])
