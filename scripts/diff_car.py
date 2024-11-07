#两轮小车测试代码
#直接在终端即可运行
#需要安装mujoco库
#pip install mujoco
import mujoco as mj
from mujoco.glfw import glfw
import numpy as np
import os
from scipy.spatial.transform import Rotation as R

xml_path = 'diff_car.xml' #xml file (assumes this is in the same folder as this file)
simend = 100 #simulation time
print_camera_config = 1 #set to 1 to print camera config
                        #this is useful for initializing view of the model)

# 鼠标回调参数初始化
button_left = False
button_middle = False
button_right = False
lastx = 0
lasty = 0

def quar2euler(quat_mujoco):
    #mujoco quat is constant,x,y,z
    #scipy quaut is x,y,z,constant
    quat_mujoco=np.array([quat_mujoco[3],quat_mujoco[0],quat_mujoco[1],quat_mujoco[2]])

    r = R.from_quat(quat_mujoco)
    euler = r.as_euler('xyz', degrees=True)
    return euler

def init_controller(model,data):
    #initialize the controller here. This function is called once, in the beginning
    pass

def controller(model, data):
    #put the controller here. This function is called inside the simulation.
    data.ctrl[0] = 10
    data.ctrl[1] = 0

def keyboard(window, key, scancode, act, mods):
    if act == glfw.PRESS and key == glfw.KEY_BACKSPACE:
        mj.mj_resetData(model, data)
        mj.mj_forward(model, data)

def mouse_button(window, button, act, mods):
    # update button state
    global button_left
    global button_middle
    global button_right

    button_left = (glfw.get_mouse_button(
        window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS)
    button_middle = (glfw.get_mouse_button(
        window, glfw.MOUSE_BUTTON_MIDDLE) == glfw.PRESS)
    button_right = (glfw.get_mouse_button(
        window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS)

    # update mouse position
    glfw.get_cursor_pos(window)

def mouse_move(window, xpos, ypos):
    # compute mouse displacement, save
    global lastx
    global lasty
    global button_left
    global button_middle
    global button_right

    dx = xpos - lastx
    dy = ypos - lasty
    lastx = xpos
    lasty = ypos

    # no buttons down: nothing to do
    if (not button_left) and (not button_middle) and (not button_right):
        return

    # get current window size
    width, height = glfw.get_window_size(window)
    

    # get shift key state
    PRESS_LEFT_SHIFT = glfw.get_key(
        window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS
    PRESS_RIGHT_SHIFT = glfw.get_key(
        window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS
    mod_shift = (PRESS_LEFT_SHIFT or PRESS_RIGHT_SHIFT)

    # determine action based on mouse button
    if button_right:
        if mod_shift:
            action = mj.mjtMouse.mjMOUSE_MOVE_H
        else:
            action = mj.mjtMouse.mjMOUSE_MOVE_V
    elif button_left:
        if mod_shift:
            action = mj.mjtMouse.mjMOUSE_ROTATE_H
        else:
            action = mj.mjtMouse.mjMOUSE_ROTATE_V
    else:
        action = mj.mjtMouse.mjMOUSE_ZOOM

    mj.mjv_moveCamera(model, action, dx/height,
                      dy/height, scene, cam)

def scroll(window, xoffset, yoffset):
    action = mj.mjtMouse.mjMOUSE_ZOOM
    mj.mjv_moveCamera(model, action, 0.0, -0.05 *
                      yoffset, scene, cam)

#得到当前文件的绝对路径
dirname = os.path.dirname(__file__)
abspath = os.path.join(dirname + "/" + xml_path)
xml_path = abspath

# 配置MuJoCo数据结构
model = mj.MjModel.from_xml_path(xml_path)  # MuJoCo model
data = mj.MjData(model)                # MuJoCo data
cam = mj.MjvCamera()                        # Abstract camera
opt = mj.MjvOption()                        # visualization options

# 创建窗口并初始化OpenGL
glfw.init()
window = glfw.create_window(1200, 900, "Demo", None, None)
glfw.make_context_current(window)
glfw.swap_interval(1)

# 初始化场景、摄像机、选项、上下文
mj.mjv_defaultCamera(cam)
mj.mjv_defaultOption(opt)
scene = mj.MjvScene(model, maxgeom=10000)
context = mj.MjrContext(model, mj.mjtFontScale.mjFONTSCALE_150.value)

# 鼠标交互初始化
glfw.set_key_callback(window, keyboard)
glfw.set_cursor_pos_callback(window, mouse_move)
glfw.set_mouse_button_callback(window, mouse_button)
glfw.set_scroll_callback(window, scroll)

# 相机参数初始化
cam.azimuth = 90
cam.elevation = -45
cam.distance = 20
cam.lookat = np.array([0.0, 0.0, 0])

#initialize the controller
init_controller(model,data)

#set the controller
mj.set_mjcb_control(controller)








# # 获取摄像头的索引  
# camera_name = "my_camera"  
# camera_id = -1  
# for i in range(model.ncam):  
#     if mj.mj_id2name(model, mj.mjtObj.mjOBJ_CAMERA, i) == camera_name:  
#         print(f"找到了摄像头 '{camera_name}', 索引为 {i}.")  
#         camera_id = i  
#         break  

# if camera_id == -1:  
#     print(f"在模型中找不到摄像头 '{camera_name}'.")  
#     exit(1)  

# # 获取摄像头的位置和方向  
# camera_pos = model.cam_pos[camera_id * 3:(camera_id + 1) * 3]  
# camera_mat = model.cam_mat0[camera_id * 9:(camera_id + 1) * 9]  

# # 渲染摄像头图像  
# img = np.zeros((480, 640, 3), dtype=np.uint8)  
# # mj.mjr_render(model, data)  
# # mj.mjr_readPixels(img, model, data, camera_id)  

# # 使用OpenCV显示图像  
# import cv2  
# print(f"图像大小: 640x480")  
# cv2.imshow("MuJoCo 摄像头", img)  
# cv2.waitKey(0)  
# cv2.destroyAllWindows()









# Run simulation loop
# 仿真主循环
while not glfw.window_should_close(window):
    time_prev = data.time

    while (data.time - time_prev < 1.0/60.0):
        mj.mj_step(model, data)

    #print the position of the car
    # print(data.qpos[0:3])
    quat = np.array([data.qpos[3],data.qpos[4],data.qpos[5],data.qpos[6]])
    euler = quar2euler(quat)
    # print('yaw=',euler[2])
    print(data.site_xpos[0])

    if (data.time>=simend):
        break;

    # get framebuffer viewport
    viewport_width, viewport_height = glfw.get_framebuffer_size(
        window)
    viewport = mj.MjrRect(0, 0, viewport_width, viewport_height)

    #print camera configuration (help to initialize the view)
    if (print_camera_config==1):
        print('cam.azimuth =',cam.azimuth,';','cam.elevation =',cam.elevation,';','cam.distance = ',cam.distance)
        print('cam.lookat =np.array([',cam.lookat[0],',',cam.lookat[1],',',cam.lookat[2],'])')

    # Update scene and render
    mj.mjv_updateScene(model, data, opt, None, cam,
                       mj.mjtCatBit.mjCAT_ALL.value, scene)
    mj.mjr_render(viewport, scene, context)

    # swap OpenGL buffers (blocking call due to v-sync)
    glfw.swap_buffers(window)

    # process pending GUI events, call GLFW callbacks
    glfw.poll_events()

glfw.terminate()
