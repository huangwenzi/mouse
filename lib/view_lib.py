import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui

import cfg.game as game_cfg

palette_white = QtGui.QPalette()
palette_white.setColor(QtGui.QPalette.Window, QtGui.QColor(game_cfg.def_color))

# 默认背景色
def set_background_color(view: QtWidgets.QWidget):
    view.setAutoFillBackground(True)
    view.setPalette(palette_white)


# 设置选中颜色
def set_select_color(button: QtWidgets.QWidget):
    button.setStyleSheet("background-color: %s" % (game_cfg.button_select_color))


# 重置选中颜色
def reset_select_color(button: QtWidgets.QWidget):
    button.setStyleSheet("background-color: %s" % (game_cfg.def_color))


# 定时器
class GTimer(QtCore.QTimer):
    def __init__(self, Time, fun):
        super(GTimer, self).__init__()
        self.setInterval(Time * 1000)
        self.timeout.connect(fun)
        self.start()
