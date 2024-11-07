'''
已经实现：
向diff_car.xml文件添加<camera>,实现了摄像头的索引、渲染、显示
qustion：
1.摄像头的位置修改后，显示的视野不改变
2.某些位置不能设置摄像头，报错
3.怎么把摄像头附着在运动物体上，镜头跟随物体移动        
'''





import mujoco as mj  
from mujoco.glfw import glfw  
import numpy as np  
import os  
import cv2  

# 设置 XML 文件路径
xml_path = 'diff_car.xml'  
dirname = os.path.dirname(__file__)  
abspath = os.path.join(dirname, xml_path)  
xml_path = abspath  

# 加载 MuJoCo 模型
model = mj.MjModel.from_xml_path(xml_path)  
data = mj.MjData(model)  

# 创建场景、相机和选项对象
max_geom = 10000  # 设置最大几何体数量
scene = mj.MjvScene(model, max_geom)  # 正确创建 mjvScene 对象
opt = mj.MjvOption()
cam = mj.MjvCamera()

# 获取摄像头的索引
camera_name = "my_camera"  
camera_id = -1  
for i in range(model.ncam):  
    if mj.mj_id2name(model, mj.mjtObj.mjOBJ_CAMERA, i) == camera_name:  
        print(f"找到了摄像头 '{camera_name}', 索引为 {i}.")  
        camera_id = i  
        break  

if camera_id == -1:  
    print(f"在模型中找不到摄像头 '{camera_name}'.")  
    exit(1)  

# 创建 GLFW 窗口
if not glfw.init():
    print("无法初始化 GLFW")
    exit(1)

window = glfw.create_window(640, 480, "MuJoCo 渲染", None, None)
glfw.make_context_current(window)

# 创建 OpenGL 上下文
context = mj.MjrContext(model, max_geom)

# 创建用于存储图像和深度数据的 NumPy 数组
img_buffer = np.zeros((480, 640, 3), dtype=np.uint8)  # RGB 图像缓冲区
depth_buffer = np.zeros((480, 640), dtype=np.float32)  # 深度缓冲区

# 渲染循环
while not glfw.window_should_close(window):
    # 更新模型状态
    mj.mj_step(model, data)

    # 更新场景并渲染
    mj.mjv_updateScene(model, data, opt, None, cam, mj.mjtCatBit.mjCAT_ALL.value, scene)
    
    # 创建视口并渲染场景
    viewport = mj.MjrRect(0, 0, 640, 480)
    mj.mjr_render(viewport, scene, context)

    # 从 MuJoCo 渲染结果获取图像和深度数据
    mj.mjr_readPixels(img_buffer, depth_buffer, viewport, context)

    # 显示图像
    cv2.imshow("MuJoCo 摄像头", img_buffer)  
    
    # 检查窗口是否关闭
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 清理资源
glfw.terminate()
cv2.destroyAllWindows()