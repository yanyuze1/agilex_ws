![alt text](images/2026-04-23-18-14-56.gif)
#  1. 项目描述
本项目为Agilex机械臂系列mujoco仿真项目仓库，该仓库会随着系列项目的推进不定时进行更新，当前计划可查看本人飞书查看项目情况项目飞书，这个项目预计将会是一个超长期项目。开的坑有点小多，暂时得梳理一下先。目前开了Unitree Go2的大坑，大坑里面包含了许多模块，现在又开个Agilex机械臂的坑，确实是没办法保证项目的更新和开发进度稳定推进，有不少的项目代码都需要花费大量的精力和时间才能理解后才能应用起来，不过不必担心项目是肯定会一直进行维护和更新的。
# 2. 项目使用
##  2.1 docker使用
个人首要推荐使用docker进行项目的构建，因为这样可以避免环境依赖配置问题。具体使用方式如下：
```bash
mkdir agilex_ws && cd agilex_ws

```
# 更新计划
 1. 添加agilex nero机械臂
 2. 添加视觉模块
 3. 完成控制器模块的替换
 4. 完成vla的应用
# 后言
ok本次更新到此，有关后续的内容会在此仓库进行更新，也会在未来不断的添加有意思的功能和模块。感谢各位，尤其感谢为本次项目提供了基本框架和思路的开源项目的大佬们，我们是站在了巨人的肩上完成的这一个项目。
# 参考项目
https://github.com/renesas-rdk/agilex_piper_mujoco
https://github.com/renesas-rdk/agilex_piper_arm_description
https://github.com/renesas-rdk/mujoco_sim_ros2
