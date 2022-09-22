from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import cfg.game as game_cfg

# 轨迹默认配置视图
class TrajectoryChangeView(QLabel):
    select_trajectory_id = 0
    def __init__(self, *args):
        super(TrajectoryChangeView, self).__init__(*args)
        self.resize(game_cfg.button_size[0], game_cfg.button_size[1]*4)
        # 设置背景色
        self.setAutoFillBackground(True)
        palette_white = QPalette()
        palette_white.setColor(QPalette.Window, QColor(game_cfg.def_color))
        self.setPalette(palette_white)
        # 上方标题
        def_size_w = game_cfg.button_size[0]/2
        self.label_loop = QLabel("轨迹修改", self)
        self.label_loop.setAlignment(Qt.AlignCenter)
        self.label_loop.resize(game_cfg.button_size[0], game_cfg.button_size[1])
        self.label_loop.move(0,0)
        
        # 轨迹编号
        def_size_w = game_cfg.button_size[0]/2
        self.label_id = QLabel("轨迹编号", self)
        self.label_id.setAlignment(Qt.AlignCenter)
        self.label_id.resize(def_size_w, game_cfg.button_size[1])
        self.label_id.move(0,game_cfg.button_size[1])
        self.edit_id = QLineEdit("0", self)
        self.edit_id.setAlignment(Qt.AlignCenter)
        self.edit_id.resize(def_size_w, game_cfg.button_size[1])
        self.edit_id.move(def_size_w,game_cfg.button_size[1])
        # 默认移动时间
        self.label_move_time = QLabel("移动时间", self)
        self.label_move_time.setAlignment(Qt.AlignCenter)
        self.label_move_time.resize(def_size_w, game_cfg.button_size[1])
        self.label_move_time.move(0, game_cfg.button_size[1]*2)
        self.edit_move_time = QLineEdit("1", self)
        self.edit_move_time.setAlignment(Qt.AlignCenter)
        self.edit_move_time.resize(def_size_w, game_cfg.button_size[1])
        self.edit_move_time.move(def_size_w,game_cfg.button_size[1]*2)
        # 确定修改
        self.button_change = QPushButton("确定修改", self)
        self.button_change.resize(game_cfg.button_size[0], game_cfg.button_size[1])
        self.button_change.move(0, game_cfg.button_size[1]*3)
        self.button_change.clicked.connect(self.click_change)
        

    # 点击确定修改
    def click_change(self):
        self.parent().change_trajectory()
    
    
    # 设置选中的轨迹点
    def set_select_trajectory(self, trajectory_obj):
        self.select_trajectory_id = trajectory_obj.trajectory_id
        self.edit_id.setText(str(trajectory_obj.trajectory_id))
        self.edit_move_time.setText(str(trajectory_obj.wait_time))

            
        




