import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui


import cfg.game as game_cfg
import lib.view_lib as view_lib

# 标签+按钮
class HLabelButton(QtWidgets.QLabel):
    def __init__(self, *args):
        super(HLabelButton, self).__init__(*args)
        # 设置背景色
        view_lib.set_background_color(self)

    # 初始化
    def init(self, width, heigth, label_str, button_str, button_click_fun):
        def_size_w = width / 2
        self.label = QtWidgets.QLabel(label_str, self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.resize(def_size_w, heigth)
        self.button = QtWidgets.QPushButton(button_str, self)
        self.button.resize(def_size_w, heigth)
        self.button.move(def_size_w, 0)
        self.button.clicked.connect(button_click_fun)
        self.resize(width, heigth)

    # 获取文本
    def text(self):
        return self.button.text()

    # 设置文本
    def setText(self, in_str):
        return self.button.setText(in_str)


# 标签+循环按钮
# 继承HLabelButton 附加按钮函数
class HLabelLoopButton(HLabelButton):
    def __init__(self, *args):
        super(HLabelLoopButton, self).__init__(*args)
        self.button_str_list = []

    # 初始化
    def init(self, width, heigth, label_str, button_str, button_str_list):
        self.button_str_list = button_str_list
        super(HLabelLoopButton, self).init(
            width, heigth, label_str, button_str, self.click_button
        )

    # 循环按钮
    def click_button(self):
        idx = 0
        now_button_str = self.button.text()
        # 寻找下一个字符串
        for item in self.button_str_list:
            idx += 1
            if item == now_button_str:
                break

        # 超出范围说明找不到，设为第一个
        if idx >= len(self.button_str_list):
            idx = 0
        self.button.setText(self.button_str_list[idx])


# 标签+输入框
class HLabelEdit(QtWidgets.QLabel):
    def __init__(self, *args):
        super(HLabelEdit, self).__init__(*args)
        # 设置背景色
        view_lib.set_background_color(self)

    # 初始化
    def init(self, width, heigth, label_str, edit_str):
        def_size_w = width / 2
        self.label = QtWidgets.QLabel(label_str, self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.resize(def_size_w, heigth)
        self.edit = QtWidgets.QLineEdit(edit_str, self)
        self.edit.resize(def_size_w, heigth)
        self.edit.move(def_size_w, 0)
        self.resize(width, heigth)

    # 获取文本
    def text(self):
        return self.edit.text()

    # 设置文本
    def setText(self, in_str):
        return self.edit.setText(in_str)
