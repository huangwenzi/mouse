import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui

import cfg.game as game_cfg

# 轨迹默认配置视图
class TrajectoryCfgView(QtWidgets.QLabel):
    def __init__(self, *args):
        super(TrajectoryCfgView, self).__init__(*args)
        self.resize(game_cfg.button_size[0], game_cfg.button_size[1]*4)
        # 设置背景色
        self.setAutoFillBackground(True)
        palette_white = QtGui.QPalette()
        palette_white.setColor(QtGui.QPalette.Window, QtGui.QColor(game_cfg.def_color))
        self.setPalette(palette_white)
        # 上方标题
        def_size_w = game_cfg.button_size[0]/2
        self.label_title = QtWidgets.QLabel("轨迹配置", self)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.resize(game_cfg.button_size[0], game_cfg.button_size[1])
        self.label_title.move(0,0)
        
        # 轨迹循环
        def_size_w = game_cfg.button_size[0]/2
        self.label_loop = QtWidgets.QLabel("轨迹循环", self)
        self.label_loop.setAlignment(QtCore.Qt.AlignCenter)
        self.label_loop.resize(def_size_w, game_cfg.button_size[1])
        self.label_loop.move(0,game_cfg.button_size[1])
        self.button_loop = QtWidgets.QPushButton("否", self)
        self.button_loop.resize(def_size_w, game_cfg.button_size[1])
        self.button_loop.move(def_size_w, game_cfg.button_size[1])
        self.button_loop.clicked.connect(self.click_loop)
        # 默认移动时间
        self.label_move_time = QtWidgets.QLabel("移动时间", self)
        self.label_move_time.setAlignment(QtCore.Qt.AlignCenter)
        self.label_move_time.resize(def_size_w, game_cfg.button_size[1])
        self.label_move_time.move(0, game_cfg.button_size[1]*2)
        self.edit_move_time = QtWidgets.QLineEdit("1", self)
        self.edit_move_time.setAlignment(QtCore.Qt.AlignCenter)
        self.edit_move_time.resize(def_size_w, game_cfg.button_size[1])
        self.edit_move_time.move(def_size_w,game_cfg.button_size[1]*2)
        # 轨迹穿透
        self.label_penetrate = QtWidgets.QLabel("轨迹穿透", self)
        self.label_penetrate.setAlignment(QtCore.Qt.AlignCenter)
        self.label_penetrate.resize(def_size_w, game_cfg.button_size[1])
        self.label_penetrate.move(0, game_cfg.button_size[1]*3)
        self.button_penetrate = QtWidgets.QPushButton("否", self)
        self.button_penetrate.resize(def_size_w, game_cfg.button_size[1])
        self.button_penetrate.move(def_size_w, game_cfg.button_size[1]*3)
        self.button_penetrate.clicked.connect(self.click_penetrate)

    # 修改循环状态
    def click_loop(self):
        if self.button_loop.text() == "否":
            self.button_loop.setText("是")
        else:
            self.button_loop.setText("否")
    
    # 修改穿透状态
    def click_penetrate(self):
        if self.button_penetrate.text() == "否":
            self.button_penetrate.setText("是")
        else:
            self.button_penetrate.setText("否")
            
        




