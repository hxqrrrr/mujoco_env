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
from scipy.spatial.transform import Rotation as R


def get_body_position(model, data, body_name):
    body_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, body_name)
    if body_id == -1:
        raise ValueError(f"找不到物体 '{body_name}'")
    return data.xpos[body_id]
    
def calculate_camera_matrix(cam_pos, target_pos, up_vector=None):
    if up_vector is None:
        up_vector = np.array([0, 0, 1])
    
    # 计算前向向量（从摄像头指向目标）
    forward = target_pos - cam_pos
    forward = forward / np.linalg.norm(forward)
    
    # 计算右向量
    right = np.cross(forward, up_vector)
    right = right / np.linalg.norm(right)
    
    # 重新计算上向量以确保正交性
    up = np.cross(right, forward)
    up = up / np.linalg.norm(up)
    
    # 构建旋转矩阵
    R = np.array([right, up, -forward])
    return R.flatten()

def quar2euler(quat_mujoco):
    quat_mujoco = np.array([quat_mujoco[3], quat_mujoco[0], quat_mujoco[1], quat_mujoco[2]])
    r = R.from_quat(quat_mujoco)
    euler = r.as_euler('xyz', degrees=True)
    return euler

def init_controller(model, data):
    pass

def controller(model, data):
    # 小车的运动控制
    data.ctrl[0] = 10  # 左轮速度
    data.ctrl[1] = 0   # 右轮速度

def print_camera_info(model, data, camera_id):
    """打印摄像头的详细信息"""
    print("\n=== 摄像头信息 ===")
    print(f"摄像头ID: {camera_id}")
    
    # 打印位置信息
    cam_pos = data.cam_xpos[camera_id]
    print(f"位置 (xpos): {cam_pos}")
    
    # 打印方向矩阵
    cam_mat = data.cam_xmat[camera_id].reshape(3,3)
    print("方向矩阵 (xmat):")
    print(cam_mat)
    
    # 打印目标物体（box）的位置
    box_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, "box")
    if box_id != -1:
        box_pos = data.xpos[box_id]
        print(f"目标物体位置: {box_pos}")
        
        # 计算相对位置
        relative_pos = cam_pos - box_pos
        print(f"相对位置 (摄像头相对于box): {relative_pos}")
    
    # 打印其他相机参数
    print(f"fovy: {model.cam_fovy[camera_id]}")  # 视场角
    print("===========================\n")

def get_box_position(model, data):
    """获取小车位置"""
    box_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, "box")
    return data.xpos[box_id]

def update_camera(cam, box_pos):
    """更新相机视角"""
    # 设置相机位置（固定在空间中的某个点）
    cam.lookat[0] = box_pos[0]  # x坐标跟随小车
    cam.lookat[1] = box_pos[1]  # y坐标跟随小车
    cam.lookat[2] = box_pos[2]  # z坐标跟随小车
    
    # 设置相机距离和角度
    cam.distance = 4.0  # 相机到观察点的距离
    cam.azimuth = 90   # 水平角度
    cam.elevation = -20  # 垂直角度（负值表示从上方看）

def print_box_info(data, box_pos):
    """打印小车位置信息"""
    print("\n=== 小车信息 ===")
    print(f"位置: x={box_pos[0]:.2f}, y={box_pos[1]:.2f}, z={box_pos[2]:.2f}")
    print(f"速度: 左轮={data.ctrl[0]:.2f}, 右轮={data.ctrl[1]:.2f}")
    print("================\n")

# 设置 XML 文件路径
xml_path = 'diff_car.xml'  
dirname = os.path.dirname(__file__)  
abspath = os.path.join(dirname, xml_path)  
xml_path = abspath  

# 加载 MuJoCo 模型
model = mj.MjModel.from_xml_path(xml_path)  
data = mj.MjData(model)  

# 创建场景和相机
scene = mj.MjvScene(model, maxgeom=10000)
cam = mj.MjvCamera()

# 设置相机类型为自由视角
cam.type = mj.mjtCamera.mjCAMERA_FREE

# 创建窗口和上下文
glfw.init()
window = glfw.create_window(1200, 900, "Camera View", None, None)
glfw.make_context_current(window)
context = mj.MjrContext(model, mj.mjtFontScale.mjFONTSCALE_150.value)

# 设置渲染选项
opt = mj.MjvOption()

# 设置控制器
mj.set_mjcb_control(controller)

# 渲染循环
frame_count = 0  # 添加帧计数器
while not glfw.window_should_close(window):
    # 更新物理
    mj.mj_step(model, data)
    
    # 获取小车位置并更新相机
    box_pos = get_box_position(model, data)
    update_camera(cam, box_pos)
    
    # 每60帧（约1秒）打印一次位置信息
    frame_count += 1
    if frame_count % 60 == 0:
        print_box_info(data, box_pos)
    
    # 更新场景
    mj.mjv_updateScene(
        model, 
        data, 
        opt, 
        None, 
        cam, 
        mj.mjtCatBit.mjCAT_ALL.value, 
        scene
    )
    
    # 渲染
    viewport = mj.MjrRect(0, 0, 1200, 900)
    mj.mjr_render(viewport, scene, context)
    
    # 交换缓冲区
    glfw.swap_buffers(window)
    glfw.poll_events()

# 清理资源
glfw.terminate()
