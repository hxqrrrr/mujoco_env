# mujoco_env

#### 使用方法
克隆此仓库\
pip install mujoco
#### 文档介绍

template文件夹里保存了py代码初始模板，diff_car.py是两轮小车的仿真代码，运行即玩。

trossen_vx300s文件夹中保存了vx300s.xml和vx300s.py,demo.py。demo.py用于实现vx300s机械臂的初始化。vx300s.py是模板文件。后缀xml表示文件包含仿真模型参数。

[vx300s](https://github.com/google-deepmind/mujoco_menagerie/tree/main/trossen_vx300s)是由Trossen Robotics开发的[ViperX 300 6DOF](https://www.trossenrobotics.com/viperx-300-robot-arm-6dof.aspx)的简化机器人描述 (MJCF) 。

------

#### 有用的资料

**mujoco：**

mujoco仓库：https://github.com/google-deepmind/mujoco

mujoco文档：https://mujoco.readthedocs.io/en/stable/python.html#

mujoco简单使用方法视频：https://www.youtube.com/watch?v=I5QvXfo8L4o&list=PLc7bpbeTIk75dgBVd07z6_uKN1KQkwFRK&index=11

**others：**

gazebosim：https://gazebosim.org/home

brax：https://github.com/google/brax

openai gym：https://github.com/Farama-Foundation/Gymnasium

Aloha&Lerobot指南：https://mlc.trossenrobotics.com/

ROS wiki：https://wiki.ros.org/urdf/XML

dora：https://github.com/dora-rs/dora-lerobot
