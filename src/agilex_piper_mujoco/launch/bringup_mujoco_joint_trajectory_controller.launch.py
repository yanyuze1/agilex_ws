#!/usr/bin/env python3
# *********************************************************************************************************************
# Copyright [2025] Renesas Electronics Corporation and/or its licensors. All Rights Reserved.
#
# The contents of this file (the "contents") are proprietary and confidential to Renesas Electronics Corporation
# and/or its licensors ("Renesas") and subject to statutory and contractual protections.
#
# Unless otherwise expressly agreed in writing between Renesas and you: 1) you may not use, copy, modify, distribute,
# display, or perform the contents; 2) you may not use any name or mark of Renesas for advertising or publicity
# purposes or in connection with your use of the contents; 3) RENESAS MAKES NO WARRANTY OR REPRESENTATIONS ABOUT THE
# SUITABILITY OF THE CONTENTS FOR ANY PURPOSE; THE CONTENTS ARE PROVIDED "AS IS" WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY, INCLUDING THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NON-INFRINGEMENT; AND 4) RENESAS SHALL NOT BE LIABLE FOR ANY DIRECT, INDIRECT, SPECIAL, OR CONSEQUENTIAL DAMAGES,
# INCLUDING DAMAGES RESULTING FROM LOSS OF USE, DATA, OR PROJECTS, WHETHER IN AN ACTION OF CONTRACT OR TORT, ARISING
# OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THE CONTENTS. Third-party contents included in this file may
# be subject to different terms.
# *********************************************************************************************************************

"""
Launch file for Agilex Piper arm MuJoCo simulation with joint trajectory control.

This launch file starts:
- mujoco_sim: MuJoCo physics simulation with ros2_control plugin
- robot_state_publisher: Publishes TF transforms from URDF
- joint_state_broadcaster: Publishes joint states from simulation
- agilex_piper_joint_trajectory_controller: Trajectory control for arm joints (joint1-joint6)
- agilex_piper_gripper_position_controller: Position control for gripper (joint7-joint8)

Usage:
  ros2 launch agilex_piper_mujoco bringup_mujoco_joint_trajectory_controller.launch.py

Test joint trajectory commands:
  # Using action interface (recommended):
  ros2 action send_goal /agilex_piper_joint_trajectory_controller/follow_joint_trajectory control_msgs/action/FollowJointTrajectory "
  trajectory:
    joint_names: [joint1, joint2, joint3, joint4, joint5, joint6]
    points:
    - positions: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
      time_from_start: {sec: 0, nanosec: 0}
    - positions: [0.785, 0.5, -0.5, 0.0, 0.0, 0.0]
      time_from_start: {sec: 3, nanosec: 0}
    - positions: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
      time_from_start: {sec: 6, nanosec: 0}
  "

  # Using topic interface (streaming):
  ros2 topic pub /agilex_piper_joint_trajectory_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "
  joint_names: [joint1, joint2, joint3, joint4, joint5, joint6]
  points:
  - positions: [0.785, 0.0, 0.0, 0.0, 0.0, 0.0]
    velocities: []
    accelerations: []
    time_from_start: {sec: 2, nanosec: 0}
  "

Test gripper commands:
  # Open gripper
  ros2 topic pub --once /agilex_piper_gripper_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.035, -0.035]}"
  # Close gripper
  ros2 topic pub --once /agilex_piper_gripper_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.0, 0.0]}"

Note:
- Joint trajectory controller provides smooth, time-parameterized motion between waypoints
- Supports velocity and acceleration control for smoother movement
- Action interface provides feedback during trajectory execution
"""

import os

import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit, OnProcessStart
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    """Generate launch description for Agilex Piper MuJoCo simulation with trajectory control."""
    # Package paths
    agilex_piper_mujoco_path = get_package_share_directory('agilex_piper_mujoco')

    # URDF file with MuJoCo ros2_control configuration
    xacro_file = os.path.join(
        agilex_piper_mujoco_path,
        'urdf',
        'agilex_piper.mj.urdf.xacro'
    )

    # Process xacro to get robot description
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    robot_description = {'robot_description': doc.toxml()}

    # Controller configuration file for trajectory control
    config_file = PathJoinSubstitution([
        FindPackageShare('agilex_piper_mujoco'),
        'config',
        'agilex_piper_mujoco_controller.yaml'
    ])

    # Nodes and actions
    mujoco_simulate_app = Node(
        package='mujoco_sim_ros2',
        executable='mujoco_sim',
        parameters=[config_file],
        output='screen'
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        name='joint_state_broadcaster_spawner',
        output='screen',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
    )

    agilex_piper_joint_trajectory_controller = Node(
        package='controller_manager',
        executable='spawner',
        name='joint_trajectory_controller_spawner',
        output='screen',
        arguments=[
            'agilex_piper_joint_trajectory_controller',
            '--controller-manager', '/controller_manager',
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
        ],
    )

    # Launch description
    return LaunchDescription([
        mujoco_simulate_app,
        robot_state_publisher,
        # Start joint_state_broadcaster when mujoco_sim starts
        RegisterEventHandler(
            event_handler=OnProcessStart(
                target_action=mujoco_simulate_app,
                on_start=[joint_state_broadcaster],
            )
        ),
        # Start trajectory controller after joint_state_broadcaster
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=joint_state_broadcaster,
                on_exit=[agilex_piper_joint_trajectory_controller],
            )
        ),
        # Start gripper controller after trajectory controller
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=agilex_piper_joint_trajectory_controller,
                on_exit=[agilex_piper_gripper_position_controller],
            )
        )
    ])
