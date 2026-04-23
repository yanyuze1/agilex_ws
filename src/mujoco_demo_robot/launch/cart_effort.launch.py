import os
import xacro

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription

from launch_ros.actions import Node
from launch.actions import ExecuteProcess, RegisterEventHandler, TimerAction
from launch.event_handlers import OnProcessStart, OnProcessExit

from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    ## arguments
    mujoco_ros2_control_demos_path = os.path.join(
        get_package_share_directory('mujoco_ros2_control_demos'))
    xacro_file = os.path.join(mujoco_ros2_control_demos_path,
                              'urdf',
                              'test_cart_effort.xacro.urdf')

    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    robot_description = {'robot_description': doc.toxml()}

    config_file = PathJoinSubstitution([
        FindPackageShare('mujoco_demo_robot'),
        "config",
        "cart_effort.yaml"
    ])

    ## actions
    mujoco_simulate_app = Node(
        package='mujoco_sim_ros2',
        executable='mujoco_sim',
        parameters=[config_file],
        output='screen')

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    joint_state_broadcaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen'
    )

    joint_effort_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'effort_controller'],
        output='screen'
    )

    ## LaunchDescription
    return LaunchDescription([
        mujoco_simulate_app,
        robot_state_publisher,
        RegisterEventHandler(
            event_handler=OnProcessStart(
                target_action=mujoco_simulate_app,
                on_start=[joint_state_broadcaster],
            )
        ),
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=joint_state_broadcaster,
                on_exit=[joint_effort_controller],
            )
        )
    ])
