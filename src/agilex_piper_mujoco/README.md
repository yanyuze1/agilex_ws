# agilex_piper_mujoco

MuJoCo simulation package for the Agilex Piper robotic arm with `ros2_control` integration.

## Overview

This package provides a complete simulation environment for the Agilex Piper 6-DOF robotic arm with gripper in MuJoCo physics engine. It integrates with ROS2 control framework to enable development and testing of various control strategies.

## Features

- MuJoCo physics simulation with ros2_control integration
- Multiple control modes:
  - Joint position control
  - Joint trajectory control
  - Cartesian motion control (end-effector space)
- Independent gripper control
- Robot state publishing for visualization

## Usage

### Joint Position Control

Launch simulation:
```bash
ros2 launch agilex_piper_mujoco bringup_mujoco_joint_position_controller.launch.py
```

Control arm joints:
```bash
# Home position
ros2 topic pub --once /agilex_piper_joint_position_controller/commands \
  std_msgs/msg/Float64MultiArray "{data: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}"

# Move joint1
ros2 topic pub --once /agilex_piper_joint_position_controller/commands \
  std_msgs/msg/Float64MultiArray "{data: [0.785, 0.0, 0.0, 0.0, 0.0, 0.0]}"
```

Control gripper:
```bash
# Open gripper
ros2 topic pub --once /agilex_piper_gripper_position_controller/commands \
  std_msgs/msg/Float64MultiArray "{data: [0.035, -0.035]}"

# Close gripper
ros2 topic pub --once /agilex_piper_gripper_position_controller/commands \
  std_msgs/msg/Float64MultiArray "{data: [0.0, 0.0]}"
```

### Joint Trajectory Control

Launch simulation:
```bash
ros2 launch agilex_piper_mujoco bringup_mujoco_joint_trajectory_controller.launch.py
```

Send trajectory via action:
```bash
ros2 action send_goal /agilex_piper_joint_trajectory_controller/follow_joint_trajectory \
  control_msgs/action/FollowJointTrajectory -f <trajectory_file.yaml>
```

### Cartesian Motion Control

Launch simulation:
```bash
ros2 launch agilex_piper_mujoco bringup_mujoco_cartesian_motion_controller.launch.py
```

Send Cartesian pose:
```bash
ros2 topic pub --once /agilex_piper_cartesian_motion_controller/target_frame \
  geometry_msgs/msg/PoseStamped "{
    header: {frame_id: 'base_link'},
    pose: {
      position: {x: 0.2, y: 0.0, z: 0.2},
      orientation: {x: 0.0, y: 1.0, z: 0.0, w: 0.0}
    }
  }"
```

Monitor state:
```bash
ros2 topic echo /agilex_piper_cartesian_motion_controller/current_pose
```
