from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyautogui

import cfg.game as game_cfg
import lib.view_lib as view_lib

# 菜单类型
menu_type_add = 1       # 添加轨迹
menu_type_del = 2       # 删除轨迹
menu_type_plan = 3      # 重排编号


# 轨迹鼠标菜单
class TrajectoryMenuView(QLabel):
    select_menu_1 = menu_type_add   # 默认添加
    now_add_id = 1
    
    def __init__(self, *args):
        super(TrajectoryMenuView, self).__init__(*args)
        # 基础设置
        desktop = QApplication.desktop()
        self.resize(desktop.width() - game_cfg.button_size[0], desktop.height())
        self.move(game_cfg.button_size[0], 0)
        
        # 初始化按钮
        self.button_add = QPushButton("添加轨迹", self)
        self.button_add.resize(game_cfg.button_size[0], game_cfg.button_size[1])
        self.button_add.move(0,0)
        self.button_add.clicked.connect(self.click_add)
        self.button_run = QPushButton("运行轨迹", self)
        self.button_run.resize(game_cfg.button_size[0], game_cfg.button_size[1])
        self.button_run.move(0,game_cfg.button_size[1])
        self.button_run.clicked.connect(self.click_run)
        # self.button_del = QPushButton("删除单个", self)
        # self.button_del.resize(game_cfg.button_size[0], game_cfg.button_size[1])
        # self.button_del.move(0,0)
        # self.button_del.clicked.connect(self.click_del)
        # self.button_plan = QPushButton("重排编号", self)
        # self.button_plan.resize(game_cfg.button_size[0], game_cfg.button_size[1])
        # self.button_plan.move(0,0)
        # self.button_plan.clicked.connect(self.click_plan)

        # 背景label 隔绝添加轨迹和轨迹的点击
        self.add_label = Trajectory_add_label(self)
        self.add_label.resize(desktop.width() - game_cfg.button_size[0]*2, desktop.height())
        self.add_label.move(game_cfg.button_size[0], 0)
        
        # 数据
        self.trajectory_list = []
        self.run_add_id = 0
        self.run_end_add_id = 0
        self.run_timer = None
        
        # 资源加载
        self.add_pix = QPixmap()
        self.add_pix.load("./image/tar.png")
        # 字体
        self.def_font = QFont()
        self.def_font.setFamily("Arial") #括号里可以设置成自己想要的其它字体
        self.def_font.setPointSize(18)   #括号里的数字可以设置成自己想要的字体大小
        
        # 默认选择第一个
        self.click_add()
        

    # 点击添加
    def click_add(self):
        self.select_menu_1 = menu_type_add
        # 设置功能选中
        view_lib.button_select(self.button_add)
        # 背景label置顶
        self.add_label.raise_()
    
    # 点击运行
    def click_run(self):
        # 先最小化
        self.parent().showMinimized()
        # 是否有有效列表
        list_len = len(self.trajectory_list)
        if list_len <= 0:
            return
        self.run_add_id = 0
        self.run_end_add_id = list_len
        first_obj:TrajectoryObj = self.trajectory_list[0]
        if self.run_timer:
            self.run_timer.stop()
        self.run_timer = view_lib.GTimer(first_obj.wait_time, self.trajectory_run)
        pyautogui.moveTo(first_obj.pos.x(), first_obj.pos.y(), first_obj.wait_time)
        
        
    # 轨迹运行
    def trajectory_run(self):
        # 关掉定时器，并点击
        self.run_timer.stop()
        pyautogui.mouseDown()
        pyautogui.mouseUp()
        
        # 是否结束
        self.run_add_id += 1
        if self.run_add_id >= self.run_end_add_id:
            return
        
        # 运行到下一个轨迹点
        next_obj:TrajectoryObj = self.trajectory_list[self.run_add_id]
        self.run_timer = view_lib.GTimer(next_obj.wait_time, self.trajectory_run)
        pyautogui.moveTo(next_obj.pos.x(), next_obj.pos.y(), next_obj.wait_time)
        
        
    # 添加轨迹点
    def add_trajectory_obj(self, x, y):
        # 初始化轨迹点
        add_trajectory_obj = TrajectoryObj(self)
        add_trajectory_obj.add_id = self.now_add_id
        add_trajectory_obj.pos = QCursor.pos()
        # size = self.add_pix.size()
        # add_trajectory_obj.resize(size)
        # add_trajectory_obj.setPixmap(self.add_pix)
        # add_trajectory_obj.move(x - game_cfg.button_size[0] - size.width()/2, y - size.height()/2)
        add_trajectory_obj.resize(30,30)
        add_trajectory_obj.setText("%s"%(add_trajectory_obj.add_id))
        add_trajectory_obj.move(x - game_cfg.button_size[0] - 30/2, y - 30/2)
        add_trajectory_obj.setFont(self.def_font)
        add_trajectory_obj.setAlignment(Qt.AlignCenter)
        add_trajectory_obj.show()
        self.now_add_id += 1
        self.trajectory_list.append(add_trajectory_obj)
        # 背景label置顶
        self.add_label.raise_()
        

        
class Trajectory_add_label(QLabel):
    def __init__(self, *args):
        super(Trajectory_add_label, self).__init__(*args)
        
    # 鼠标事件
    def mousePressEvent(self, event:QMouseEvent):
        if event.buttons() == Qt.LeftButton:  # 左键按下
            print("单击鼠标左键")  # 响应测试语句
            # 触发上面的添加
            pos = QCursor.pos()
            self.parent().add_trajectory_obj(pos.x(), pos.y())
        # elif event.buttons() == Qt.RightButton:  # 右键按下
        #     print("单击鼠标右键")  # 响应测试语句
        # elif event.buttons() == Qt.MidButton:  # 中键按下
        #     print("单击鼠标中键")  # 响应测试语句
        # elif event.buttons() == Qt.LeftButton | Qt.RightButton:  # 左右键同时按下
        #     print("单击鼠标左右键")  # 响应测试语句
        # elif event.buttons() == Qt.LeftButton | Qt.MidButton:  # 左中键同时按下
        #     print("单击鼠标左中键")  # 响应测试语句
        # elif event.buttons() == Qt.MidButton | Qt.RightButton:  # 右中键同时按下
        #     print("单击鼠标右中键")  # 响应测试语句
        # elif event.buttons() == Qt.LeftButton | Qt.MidButton | Qt.RightButton:  # 左中右键同时按下
        #     print("单击鼠标左中右键")  # 响应测试语句


# 轨迹对象
class TrajectoryObj(QLabel):
    add_id = 0      # id
    wait_time = 1   # 等待时间
    pos:QPoint = None      # 绝对坐标
    def __init__(self, *args):
        super(TrajectoryObj, self).__init__(*args)
    
        













