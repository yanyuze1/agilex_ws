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
Launch file for displaying Agilex Piper Arm with Foxglove Studio visualization.

This launch file starts:
- robot_state_publisher: Publishes TF transforms from URDF
- joint_state_publisher: Publishes joint states with configurable initial positions
- foxglove_bridge: WebSocket bridge for Foxglove Studio visualization

Launch arguments:
- include_gripper: Include gripper in the robot model (default: false)

Usage:
  # Display arm only:
  ros2 launch agilex_piper_arm_description display_foxglove.launch.py

  # Display arm with gripper:
  ros2 launch agilex_piper_arm_description display_foxglove.launch.py include_gripper:=true

  Then connect Foxglove Studio to ws://localhost:8765
"""

import os
from typing import List

import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import FrontendLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs) -> List[Node]:
    """Setup function to evaluate launch configurations at runtime."""
    # Get launch configurations
    include_gripper_value = LaunchConfiguration('include_gripper').perform(context)

    package_name = 'agilex_piper_arm_description'

    # Paths
    pkg_share = get_package_share_directory(package_name)

    # Choose URDF based on gripper configuration
    if include_gripper_value.lower() == 'true':
        xacro_file = os.path.join(pkg_share, 'urdf', 'agilex_piper_arm_wi_gripper.urdf.xacro')
    else:
        xacro_file = os.path.join(pkg_share, 'urdf', 'agilex_piper_arm.urdf.xacro')

    foxglove_bridge_launch = os.path.join(
        get_package_share_directory('foxglove_bridge'),
        'launch',
        'foxglove_bridge_launch.xml'
    )

    # Process the XACRO file
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    # Nodes
    nodes: List[Node] = [
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description_raw}]
        ),
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen',
            parameters=[{
                'zeros.joint2': 0.5236,  # 30 degrees
            }]
        ),
        # Foxglove bridge for web-based visualization
        IncludeLaunchDescription(
            FrontendLaunchDescriptionSource(foxglove_bridge_launch)
        )
    ]

    return nodes


def generate_launch_description() -> LaunchDescription:
    """Generate launch description for Agilex Piper Arm with Foxglove visualization."""
    # Declare arguments
    include_gripper_arg = DeclareLaunchArgument(
        'include_gripper',
        default_value='false',
        description='Include gripper in the robot model (true/false)'
    )

    return LaunchDescription([
        include_gripper_arg,
        OpaqueFunction(function=launch_setup)
    ])
