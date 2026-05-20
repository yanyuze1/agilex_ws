# agilex_piper_arm_description

ROS2 package containing URDF description files for the Agilex Piper 6-DOF robotic arm.

## Overview

This package provides the robot description for the Agilex Piper robotic arm, including URDF/XACRO files, 3D meshes, and visualization launch files for RViz and Foxglove Studio.

## Launch Parameters

Both launch files support the following parameter:

- `include_gripper` (default: false): Include the gripper in the robot model
- `run_rviz` (default: false): Launch RViz locally (RViz launch only)
- `rviz_config`: Path to RViz configuration file (RViz launch only)

## Usage

### RViz Visualization

Launch with GUI (local, arm only):
```bash
ros2 launch agilex_piper_arm_description display_rviz.launch.py run_rviz:=true
```

Launch with GUI (local, with gripper):
```bash
ros2 launch agilex_piper_arm_description display_rviz.launch.py run_rviz:=true include_gripper:=true
```

Launch for remote visualization (arm only):
```bash
ros2 launch agilex_piper_arm_description display_rviz.launch.py run_rviz:=false
```

Launch for remote visualization (with gripper):
```bash
ros2 launch agilex_piper_arm_description display_rviz.launch.py run_rviz:=false include_gripper:=true
```

### Foxglove Studio Visualization

Arm only:
```bash
ros2 launch agilex_piper_arm_description display_foxglove.launch.py
```

With gripper:
```bash
ros2 launch agilex_piper_arm_description display_foxglove.launch.py include_gripper:=true
```

Connect Foxglove Studio to `ws://<foxglove_bridge_ip>:8765`.

### Using the XACRO Macros

#### Arm Only
```xml
<xacro:include filename="$(find agilex_piper_arm_description)/urdf/agilex_piper_arm_macro.xacro" />

<xacro:agilex_piper_arm prefix="arm_" parent="base_link">
  <origin xyz="0 0 0" rpy="0 0 0" />
</xacro:agilex_piper_arm>
```

#### Arm with Gripper
```xml
<xacro:include filename="$(find agilex_piper_arm_description)/urdf/agilex_piper_arm_macro.xacro" />
<xacro:include filename="$(find agilex_piper_arm_description)/urdf/agilex_piper_gripper_macro.xacro" />

<xacro:agilex_piper_arm prefix="arm_" parent="base_link">
  <origin xyz="0 0 0" rpy="0 0 0" />
</xacro:agilex_piper_arm>

<xacro:agilex_piper_gripper prefix="arm_" parent="arm_tool0">
  <origin xyz="0 0 0" rpy="0 0 0" />
</xacro:agilex_piper_gripper>
```

#### Convenient Pre-built Options
- `agilex_piper_arm.urdf.xacro`: Arm only
- `agilex_piper_arm_wi_gripper.urdf.xacro`: Arm with gripper

## Robot Specifications

- **DOF:** 6 revolute joints
- **Coordinate frames:** world → base_link → link1-6 → tool0
- **Joint ranges:** -150° to +150° (joint1), 0° to +180° (joint2), -170° to 0° (joint3), ±100° (joint4), ±70° (joint5), ±120° (joint6)

## License

Apache-2.0. URDF model derived from [Agilex Robotics Piper repository](https://github.com/agilexrobotics/piper_ros).
