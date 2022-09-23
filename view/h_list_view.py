import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui


import cfg.game as game_cfg
import lib.view_lib as view_lib

# 单排列表label
class HListLabel(QtWidgets.QLabel):
    def __init__(self, *args):
        super(HListLabel, self).__init__(*args)
        # 设置背景色
        view_lib.set_background_color(self)
        self.def_w = game_cfg.button_size[0]
        self.def_h = game_cfg.button_size[1]
        self.view_list = []
    
    # 添加元素
    def add_view(self, add_view:QtWidgets.QWidget, idx=-1, def_size = True):
        # 是否使用默认尺寸
        if def_size:
            add_view.resize(self.def_w, self.def_h)
        # idx是否有效
        if idx >= 0 and len(self.view_list) > idx:
            self.view_list.insert(idx, add_view)
        else:
            self.view_list.append(add_view)
        
        # 重排位置
        view_heigth = 0
        max_width = 0
        for item in self.view_list:
            item:QtWidgets.QWidget = item
            item_width = item.width()
            if item_width > max_width:
                max_width = item_width
            item.move(0,view_heigth)
            view_heigth += item.height()
        # 重设列表大小
        self.resize(max_width, view_heigth)
        














