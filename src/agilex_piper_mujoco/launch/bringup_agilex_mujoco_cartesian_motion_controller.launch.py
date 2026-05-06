#!/usr/bin/env python3

import os
import tempfile

import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, RegisterEventHandler
from launch.event_handlers import OnProcessExit, OnProcessStart
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def _write_cartesian_controller_robot_description_file(
    controller_name,
    robot_description_xml,
):
    param_file = tempfile.NamedTemporaryFile(
        mode='w',
        encoding='utf-8',
        prefix=f'{controller_name}_',
        suffix='_robot_description.yaml',
        delete=False,
    )

    param_file.write(f'{controller_name}:\n')
    param_file.write('  ros__parameters:\n')
    param_file.write('    robot_description: |\n')
    for line in robot_description_xml.splitlines():
        param_file.write(f'      {line}\n')

    param_file.close()
    return param_file.name


def generate_launch_description():
    agilex_piper_mujoco_path = get_package_share_directory('agilex_piper_mujoco')

    xacro_file = os.path.join(
        agilex_piper_mujoco_path,
        'urdf',
        'agilex_piper.mj.urdf.xacro',
    )

    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    robot_description_xml = doc.toxml()
    robot_description = {'robot_description': robot_description_xml}

    config_file = PathJoinSubstitution([
        FindPackageShare('agilex_piper_mujoco'),
        'config',
        'agilex_piper_mujoco_controller.yaml',
    ])

    cartesian_controller_name = 'agilex_piper_cartesian_motion_controller'
    cartesian_controller_robot_description_file = (
        _write_cartesian_controller_robot_description_file(
            cartesian_controller_name,
            robot_description_xml,
        )
    )

    agilex_mujoco_exec = LaunchConfiguration('agilex_mujoco_exec')

    mujoco_model_file = os.path.join(
        agilex_piper_mujoco_path,
        'models',
        'demo',
        'piper_slope_demo.xml',
    )

    mujoco_simulate_app = ExecuteProcess(
        cmd=[
            agilex_mujoco_exec,
            '-r', 'piper',
            '-s', mujoco_model_file,
            '-p', 'ros2_control',
            '--ros-args',
            '--params-file', config_file,
        ],
        output='screen',
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_description],
    )

    joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        name='joint_state_broadcaster_spawner',
        output='screen',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager', '/controller_manager',
            '--controller-manager-timeout', '60',
        ],
    )

    agilex_piper_cartesian_motion_controller = Node(
        package='controller_manager',
        executable='spawner',
        name='cartesian_motion_controller_spawner',
        output='screen',
        arguments=[
            cartesian_controller_name,
            '--controller-manager', '/controller_manager',
            '--controller-manager-timeout', '60',
            '--param-file', config_file,
            '--param-file', cartesian_controller_robot_description_file,
        ],
    )

    agilex_piper_gripper_position_controller = Node(
        package='controller_manager',
        executable='spawner',
        name='gripper_controller_spawner',
        output='screen',
        arguments=[
            'agilex_piper_gripper_position_controller',
            '--controller-manager', '/controller_manager',
            '--controller-manager-timeout', '60',
        ],
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'agilex_mujoco_exec',
            default_value=(
                '/home/agilex/project/piper/agilex_mujoco/'
                'simulate/build_ros2/agilex_mujoco'
            ),
        ),
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
                on_exit=[agilex_piper_cartesian_motion_controller],
            )
        ),
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=agilex_piper_cartesian_motion_controller,
                on_exit=[agilex_piper_gripper_position_controller],
            )
        ),
    ])
