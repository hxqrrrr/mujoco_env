# scripts

#### 文件介绍

- [trossen_vx300s文件夹](.\trossen_vx300s)中保存了vx300s.xml和vx300s.py,control.py。control.py用于实现vx300s机械臂的初始化。vx300s.py是模板文件。后缀xml表示文件包含仿真模型参数。
- [vx300s](https://github.com/google-deepmind/mujoco_menagerie/tree/main/trossen_vx300s)是由Trossen Robotics开发的[ViperX 300 6DOF](https://www.trossenrobotics.com/viperx-300-robot-arm-6dof.aspx)的简化机器人描述 (MJCF) 。
- template_mujoco.py是mujoco环境运行代码模板，diff_car.py是两轮小车的仿真代码，diff_car.xml包含全部小车参数，适合作为首次使用mujoco的参考。

-----

#### mujoco介绍

mujoco主要有三个部分，**模型模板(.xml)、包(pip)、代码模板(.py)**:

**模型模板(.xml)**：包含仿真模型和环境的全部信息

**包(pip)**：使用pip安装的mujoco包，代码调用的来源

**代码模板(.py)**：借助模板使用mujoco的api，读取.xml和控制信息，加载仿真环境

------

#### **TODO：**

- [ ] 将[gym _lowcostrobot仓库](https://github.com/perezjln/gym-lowcostrobot)中的[mujoco相关样例](https://github.com/perezjln/gym-lowcostrobot/tree/main/examples)移植到该仓库跑通
- [ ] 将[gym _lowcostrobot仓库](https://github.com/perezjln/gym-lowcostrobot)中的[lerobot相关样例](https://github.com/perezjln/gym-lowcostrobot/tree/main/examples)移植到该仓库跑通
