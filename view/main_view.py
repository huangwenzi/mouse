import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import pynput.keyboard as keyboard
import threading

import cfg.game as game_cfg
import lib.view_lib as view_lib
import view.trajectory_menu_view as trajectory_menu_view

main_view = None

# 起线程监听键盘事件
def on_release(key):
    if main_view:
        main_view.click_key(key)
def click_key():
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()
t = threading.Thread(target=click_key, name='keyboard', args=())
t.start()


# 主界面
class MainView(QtWidgets.QMainWindow):
    # 当前选中的一级菜单
    menu_select_1:QtWidgets.QPushButton = None
    # 当前选中的二级菜单
    menu_select_2:QtWidgets.QLabel = None
    
    def __init__(self, *args):
        super(MainView, self).__init__(*args)
        self.setWindowTitle('主界面')
        # 窗口最大化
        desktop = QtWidgets.QApplication.desktop()
        rect = desktop.availableGeometry()
        self.setGeometry(rect)
        self.move(0,0)
        # 去掉边框
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # 放一个label在后面
        self.bg_label = QtWidgets.QLabel("", self)
        self.bg_label.resize(desktop.width(), desktop.height())
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0.1)
        self.bg_label.setGraphicsEffect(op)
        self.bg_label.setAutoFillBackground(True)
        
        # 功能按钮
        # 添加轨迹鼠标
        self.trajectory_button = QtWidgets.QPushButton("轨迹鼠标", self)
        self.trajectory_button.resize(game_cfg.button_size[0], game_cfg.button_size[1])
        self.trajectory_button.move(0,0)
        self.trajectory_button.clicked.connect(self.click_trajectory)
        self.show()
        global main_view
        main_view = self
    
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
        
        self.menu_select_1 = self.trajectory_button
        # 弹出二级菜单
        self.menu_select_2 = trajectory_menu_view.TrajectoryMenuView(self)
        self.menu_select_2.show()

    # 键盘点击
    def click_key(self, Key):
        if self.menu_select_2 and hasattr(self.menu_select_2, "click_key"):
            self.menu_select_2.click_key(Key)
        pass
        