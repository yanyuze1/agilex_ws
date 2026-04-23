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
Launch file for displaying Agilex Piper Arm in RViz with joint state GUI.

This launch file starts:
- robot_state_publisher: Publishes TF transforms from URDF
- joint_state_publisher_gui: GUI for controlling joint positions (when run_rviz is true)
- rviz2: Visualization tool (when run_rviz is true)

Launch arguments:
- rviz_config: Path to RViz configuration file
- run_rviz: Whether to launch RViz and joint GUI locally (default: false for remote use)
- include_gripper: Include gripper in the robot model (default: false)

Usage examples:
1. Run everything locally on the robot (arm only):
   ros2 launch agilex_piper_arm_description display_rviz.launch.py run_rviz:=true

2. Run everything locally with gripper:
   ros2 launch agilex_piper_arm_description display_rviz.launch.py run_rviz:=true include_gripper:=true

3. Run on robot with RViz on remote PC (arm only):
   On robot:
   ros2 launch agilex_piper_arm_description display_rviz.launch.py run_rviz:=false

   On remote PC:
   ros2 run joint_state_publisher_gui joint_state_publisher_gui & rviz2
   And then load the RViz config file from RViz (rviz/piper_arm_display.rviz).

4. Run on robot with RViz on remote PC (with gripper):
   On robot:
   ros2 launch agilex_piper_arm_description display_rviz.launch.py run_rviz:=false include_gripper:=true

   On remote PC:
   ros2 run joint_state_publisher_gui joint_state_publisher_gui & rviz2
   And then load the RViz config file from RViz (rviz/piper_arm_display.rviz).
"""

import os
from typing import List

import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo, OpaqueFunction
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs) -> List[Node]:
    """Setup function to evaluate launch configurations at runtime."""
    # Get launch configurations
    include_gripper_value = LaunchConfiguration('include_gripper').perform(context)
    rviz_config = LaunchConfiguration('rviz_config')
    run_rviz = LaunchConfiguration('run_rviz')

    package_name = 'agilex_piper_arm_description'

    # Paths
    pkg_share = get_package_share_directory(package_name)

    # Choose URDF based on gripper configuration
    if include_gripper_value.lower() == 'true':
        xacro_file = os.path.join(pkg_share, 'urdf', 'agilex_piper_arm_wi_gripper.urdf.xacro')
    else:
        xacro_file = os.path.join(pkg_share, 'urdf', 'agilex_piper_arm.urdf.xacro')

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
                '   ros2 run rviz2 rviz2 -d <path_to>/piper_arm_display.rviz\n'
                '========================================\n'
            ),
            condition=UnlessCondition(run_rviz)
        )
    ]

    return nodes


def generate_launch_description() -> LaunchDescription:
    """Generate launch description for Agilex Piper Arm visualization."""
    package_name = 'agilex_piper_arm_description'

    # Paths
    pkg_share = get_package_share_directory(package_name)
    default_rviz_config_path = os.path.join(pkg_share, 'rviz', 'piper_arm_display.rviz')

    # Launch arguments
    launch_args: List[DeclareLaunchArgument] = [
        DeclareLaunchArgument(
            name='rviz_config',
            default_value=default_rviz_config_path,
            description='Path to RViz config file'
        ),
        DeclareLaunchArgument(
            name='run_rviz',
            default_value='false',
            description=(
                'Launch RViz and joint GUI locally. Default is false for headless robot operation. '
                'When false, run RViz on remote PC with: ros2 run rviz2 rviz2 '
                'and joint GUI with: ros2 run joint_state_publisher_gui joint_state_publisher_gui '
                'And then load the RViz config file from RViz (rviz/piper_arm_display.rviz).'
            )
        ),
        DeclareLaunchArgument(
            name='include_gripper',
            default_value='false',
            description='Include gripper in the robot model (true/false)'
        )
    ]

    return LaunchDescription(launch_args + [OpaqueFunction(function=launch_setup)])
