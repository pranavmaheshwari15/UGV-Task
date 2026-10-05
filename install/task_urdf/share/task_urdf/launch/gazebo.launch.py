import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    pkg_name = 'task_urdf'

    # Paths
    xacro_file = os.path.join(get_package_share_directory(pkg_name), 'urdf', 'sedan.urdf.xacro')
    rviz_config_file = os.path.join(get_package_share_directory(pkg_name), 'rviz', 'ugv_config.rviz')
    gazebo_ros_share = get_package_share_directory('gazebo_ros')

    # Process Xacro model
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    robot_description = {'robot_description': doc.toxml(), 'use_sim_time': True}

    # 1. Robot State Publisher Node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    # 2. Include Gazebo World launch
    launch_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_share, 'launch', 'gazebo.launch.py')
        )
    )

    # 3. Spawn UGV Entity in Gazebo
    node_spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'sedan','-z','0.1'],
        output='screen'
    )

    # 4. Launch RViz2 (with sim time enabled)
    node_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        parameters=[{'use_sim_time': True}],
        arguments=['-d', rviz_config_file] if os.path.exists(rviz_config_file) else []
    )

    return LaunchDescription([
        node_robot_state_publisher,
        launch_gazebo,
        node_spawn_entity,
        node_rviz
    ])