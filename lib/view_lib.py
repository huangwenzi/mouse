from PyQt5.QtWidgets import *
from PySide2.QtCore import *

import cfg.game as game_cfg



# 设置按钮选中
def button_select(button:QPushButton):
    button.setStyleSheet("background-color: %s"%(game_cfg.button_select_color))

# 重置按钮选中
def reset_button_select(button:QPushButton):
    button.setStyleSheet("background-color: %s"%(game_cfg.def_color))

# 定时器
class GTimer(QTimer):
    def __init__(self, Time, fun):
        super(GTimer, self).__init__()
        self.setInterval(Time * 1000)
        self.timeout.connect(fun)
        self.start()








