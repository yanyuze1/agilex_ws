<div align="center">
  <h1>Mujoco of agilex arm</h1>
  <table>
    <tr>
      <td align="center">
        <a href="https://global.agilex.ai/products/piper">
          <img src="./src/agilex_piper_mujoco/models/agilex_piper/piper.png" alt="AgileX PiPER" width="280" />
        </a>
        <br />
        <sub><strong>AgileX PiPER</strong></sub>
      </td>
      <td align="center">
        <a href="https://global.agilex.ai/products/nero">
          <img src="https://global.agilex.ai/cdn/shop/files/7_-_3.png?v=1765176593&amp;width=1946" alt="AgileX NERO" width="280" />
        </a>
        <br />
        <sub><strong>AgileX NERO</strong></sub>
      </td>
    </tr>
  </table>
  <p>
    <strong><kbd>中文</kbd></strong>
    <a href="./README_EN.md"><kbd>English</kbd></a>
  </p>
</div>

## 1. 项目描述

本项目是 Agilex 机械臂系列的 MuJoCo 仿真仓库，会随着系列项目推进持续更新。当前我也在并行推进其他长期机器人项目，因此更新节奏未必完全稳定，但这个仓库会持续维护、迭代，并逐步补充更多功能模块。

## 2. 项目使用

### 2.1 Docker 使用

推荐以工作空间的 `src` 目录为基础，通过 Docker 构建项目环境，这样可以尽量避免依赖配置问题。使用方式如下：

```bash
mkdir agilex && cd agilex
git clone https://github.com/yanyuze1/agilex_ws.git
cd agilex_ws/docker
```

Docker 常用命令：

```bash
docker compose up -d --build --remove-orphans           # 构建容器
docker compose up -d mujoco_agilex                      # 启动容器，-d 表示不进入终端
docker compose ps                                       # 查看容器状态
docker compose exec mujoco_agilex bash                  # 进入容器
docker compose down                                     # 停止并清理容器
```

### 2.2 编译

```bash
cd agilex_ws
colcon build --symlink-install
source install/setup.bash
```

### 2.3 机械臂位置模式运行

```bash
# 启动
ros2 launch agilex_piper_mujoco bringup_mujoco_joint_position_controller.launch.py

# 发布关节位置
ros2 topic pub --once /agilex_piper_joint_position_controller/commands \
  std_msgs/msg/Float64MultiArray "{data: [0.7, 0.0, 0.0, 0.0, 0.0, 0.0]}"
```

### 2.4 夹爪控制

```bash
# 开夹爪
ros2 topic pub --once /agilex_piper_gripper_position_controller/commands \
  std_msgs/msg/Float64MultiArray "{data: [0.035, -0.035]}"

# 关闭夹爪
ros2 topic pub --once /agilex_piper_gripper_position_controller/commands \
  std_msgs/msg/Float64MultiArray "{data: [0.0, 0.0]}"
```

### 2.5 机械臂笛卡尔模式运行

```bash
# 启动
ros2 launch agilex_piper_mujoco bringup_mujoco_cartesian_motion_controller.launch.py

# 发布末端位置
ros2 topic pub --once /agilex_piper_cartesian_motion_controller/target_frame \
  geometry_msgs/msg/PoseStamped "{
    header: {frame_id: 'base_link'},
    pose: {
      position: {x: 0.2, y: 0.0, z: 0.2},
      orientation: {x: 0.0, y: 1.0, z: 0.0, w: 0.0}
    }
  }"
```

### 2.6 状态检测

```bash
ros2 topic echo /agilex_piper_cartesian_motion_controller/current_pose
```

## 3. 当前效果

![MuJoCo simulation demo](./images/2026-04-23-18-14-56.gif)

## 4. Todo

- [x] 基础环境构建，支持 Piper 机械臂
- [ ] 添加 Agilex Nero 机械臂支持
- [ ] 添加视觉模块
- [ ] 完成控制器模块替换
- [ ] 推进强化学习部署测试
- [ ] 推进视觉抓取测试
- [ ] 推进各类 VA 的部署测试
- [ ] 推进各类 VLA 的部署测试

## 5. 后言

本次更新先到这里。后续内容会继续在这个仓库中维护，也会逐步加入更多有意思的功能和模块。感谢所有提供基础框架和思路的开源项目作者，我们也是站在巨人的肩膀上把这个项目一点点做起来的。

## 6. 参考项目

- https://github.com/renesas-rdk/agilex_piper_mujoco
- https://github.com/renesas-rdk/agilex_piper_arm_description
- https://github.com/renesas-rdk/mujoco_sim_ros2
