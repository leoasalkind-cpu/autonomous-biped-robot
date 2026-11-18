from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package="biped_sensors",
            executable="bno055_node",
            name="bno055_node",
            output="screen",
        ),
        Node(
            package="biped_sensors",
            executable="microphone_node",
            name="microphone_node",
            output="screen",
            parameters=[{"device": "plughw:3,0"}],
        ),
    ])
