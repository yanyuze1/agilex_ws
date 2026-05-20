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
Launch file for displaying Agilex NERO arm in RViz.

This launch file starts:
- robot_state_publisher
- joint_state_publisher_gui
- rviz2

Launch arguments:
- rviz_config: Path to RViz configuration file
- run_rviz: Whether to launch RViz and joint GUI locally

Usage:
  ros2 launch agilex_nero_arm_description display_rviz.launch.py run_rviz:=true
"""

import os
from typing import List

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo, OpaqueFunction
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs) -> List[Node]:
    """Setup function to evaluate launch configurations at runtime."""
    # Get launch configurations
    rviz_config = LaunchConfiguration('rviz_config')
    run_rviz = LaunchConfiguration('run_rviz')

    package_name = 'agilex_nero_arm_description'

    # Paths
    pkg_share = get_package_share_directory(package_name)

    urdf_file = os.path.join(pkg_share, 'urdf', 'agilex_nero_arm.urdf')
    with open(urdf_file, 'r', encoding='utf-8') as file:
        robot_description_raw = file.read()

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
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            condition=IfCondition(run_rviz)
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config],
            condition=IfCondition(run_rviz)
        ),
        # Log message when RViz is configured to run remotely
        LogInfo(
            msg=(
                '\n'
                '========================================\n'
                'RViz is configured to run remotely for visualization.\n'
                'Run on remote PC:\n'
                '   ros2 run joint_state_publisher_gui joint_state_publisher_gui &\n'
                '   ros2 run rviz2 rviz2 -d <path_to>/nero_arm_display.rviz\n'
                '========================================\n'
            ),
            condition=UnlessCondition(run_rviz)
        )
    ]

    return nodes


def generate_launch_description() -> LaunchDescription:
    """Generate launch description for Agilex nero Arm visualization."""
    package_name = 'agilex_nero_arm_description'

    # Paths
    pkg_share = get_package_share_directory(package_name)
    default_rviz_config_path = os.path.join(pkg_share, 'rviz', 'nero_arm_display.rviz')

    # Launch arguments
    launch_args: List[DeclareLaunchArgument] = [
        DeclareLaunchArgument(
            name='rviz_config',
            default_value=default_rviz_config_path,
            description='Path to RViz config file'
        ),
        DeclareLaunchArgument(
            name='run_rviz',
            default_value='true',
            description=(
                'Launch RViz and joint GUI locally. Default is false for headless robot operation. '
                'When false, run RViz on remote PC with: ros2 run rviz2 rviz2 '
                'and joint GUI with: ros2 run joint_state_publisher_gui joint_state_publisher_gui '
                'And then load the RViz config file from RViz (rviz/nero_arm_display.rviz).'
            )
        )
    ]

    return LaunchDescription(launch_args + [OpaqueFunction(function=launch_setup)])
