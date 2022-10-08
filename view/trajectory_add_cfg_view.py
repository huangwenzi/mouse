import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui

import cfg.game as game_cfg
import lib.view_lib as view_lib
import view.h_list_view as h_list_view
import view.h_row_view as h_row_view

# 轨迹默认配置视图
class TrajectoryCfgView(h_list_view.HListLabel):
    def __init__(self, *args):
        super(TrajectoryCfgView, self).__init__(*args)
        # 上方标题
        self.label_title = QtWidgets.QLabel("轨迹配置", self)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        view_lib.set_background_color(self.label_title)
        # 轨迹循环
        self.loop_label_button = h_row_view.HLabelLoopButton(self)
        self.loop_label_button.init(
            game_cfg.button_size[0], game_cfg.button_size[1], "轨迹循环", "否", ["否", "是"]
        )
        # 默认移动时间
        self.move_time_label_edit = h_row_view.HLabelEdit(self)
        self.move_time_label_edit.init(
            game_cfg.button_size[0], game_cfg.button_size[1], "移动时间", "1"
        )
        # 轨迹穿透
        self.penetrate_label_button = h_row_view.HLabelLoopButton(self)
        self.penetrate_label_button.init(
            game_cfg.button_size[0], game_cfg.button_size[1], "轨迹穿透", "否", ["否", "是"]
        )
        # 耗时跟随
        self.time_follow_label_button = h_row_view.HLabelLoopButton(self)
        self.time_follow_label_button.init(
            game_cfg.button_size[0], game_cfg.button_size[1], "耗时跟随", "否", ["否", "是"]
        )
        # 添加到菜单列表
        self.add_view(self.label_title)
        self.add_view(self.loop_label_button)
        self.add_view(self.move_time_label_edit)
        self.add_view(self.penetrate_label_button)
        self.add_view(self.time_follow_label_button)
