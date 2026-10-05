import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command

def generate_launch_description():
    pkg_path = get_package_share_directory('task_urdf')
    xacro_file = os.path.join(pkg_path, 'urdf', 'sedan.xacro')
    controller_config = os.path.join(pkg_path, 'config', 'controllers.yaml')

    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]), value_type=str
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    controller_manager_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[{'robot_description': robot_description}, controller_config],
        output='screen'
    )

    joint_broad_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_broad']
    )

    diff_cont_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['diff_cont']
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher_node,
        controller_manager_node,
        joint_broad_spawner,
        diff_cont_spawner,
        rviz_node
    ])