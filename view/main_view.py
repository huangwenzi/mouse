from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import cfg.game as game_cfg
import lib.view_lib as view_lib
import view.trajectory_menu_view as trajectory_menu_view

# 主界面
class MainView(QMainWindow):
    # 当前选中的一级菜单
    menu_select_1:QPushButton = None
    # 当前选中的二级菜单
    menu_select_2:QLabel = None
    
    def __init__(self, *args):
        super(MainView, self).__init__(*args)
        self.setWindowTitle('主界面')
        # 窗口最大化
        desktop = QApplication.desktop()
        rect = desktop.availableGeometry()
        self.setGeometry(rect)
        self.move(0,0)
        # 窗口透明
        # self.setWindowOpacity(0.3)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)    # 置顶
        self.setWindowFlags(Qt.FramelessWindowHint)     # 去掉边框
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 放一个label在后面
        self.bg_label = QLabel("", self)
        self.bg_label.resize(desktop.width(), desktop.height())
        op = QGraphicsOpacityEffect()
        op.setOpacity(0.1)
        self.bg_label.setGraphicsEffect(op)
        self.bg_label.setAutoFillBackground(True)
        
        # 功能按钮
        # 添加轨迹鼠标
        self.trajectory_button = QPushButton("轨迹鼠标", self)
        self.trajectory_button.resize(game_cfg.button_size[0], game_cfg.button_size[1])
        self.trajectory_button.move(0,0)
        self.trajectory_button.clicked.connect(self.click_trajectory)
        self.show()
    
    # 清除其他菜单选项
    def clear_select(self):
        if self.menu_select_1:
            view_lib.reset_button_select(self.menu_select_1)
        if self.menu_select_2:
            self.menu_select_2.close_view()
        self.menu_select_1 = None
        self.menu_select_2 = None
    
    # 点击轨迹按钮
    def click_trajectory(self):
        # 清除其他菜单选项
        self.clear_select()
        # 设置功能选中
        view_lib.button_select(self.trajectory_button)
        # 弹出二级菜单
        self.menu_select_2 = trajectory_menu_view.TrajectoryMenuView(self)
        self.menu_select_2.show()
    
    # # 鼠标事件
    # def mousePressEvent(self, event):
    #     if event.buttons() == Qt.LeftButton:  # 左键按下
    #         print("单击鼠标左键")  # 响应测试语句
    #     elif event.buttons() == Qt.RightButton:  # 右键按下
    #         print("单击鼠标右键")  # 响应测试语句
    #     elif event.buttons() == Qt.MidButton:  # 中键按下
    #         print("单击鼠标中键")  # 响应测试语句
    #     elif event.buttons() == Qt.LeftButton | Qt.RightButton:  # 左右键同时按下
    #         print("单击鼠标左右键")  # 响应测试语句
    #     elif event.buttons() == Qt.LeftButton | Qt.MidButton:  # 左中键同时按下
    #         print("单击鼠标左中键")  # 响应测试语句
    #     elif event.buttons() == Qt.MidButton | Qt.RightButton:  # 右中键同时按下
    #         print("单击鼠标右中键")  # 响应测试语句
    #     elif event.buttons() == Qt.LeftButton | Qt.MidButton | Qt.RightButton:  # 左中右键同时按下
    #         print("单击鼠标左中右键")  # 响应测试语句