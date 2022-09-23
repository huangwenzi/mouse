import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui

import cfg.game as game_cfg
import lib.view_lib as view_lib
import view.h_list_view as h_list_view
import view.h_row_view as h_row_view

# 轨迹默认配置视图
class TrajectoryChangeView(h_list_view.HListLabel):
    select_trajectory_id = 0
    def __init__(self, *args):
        super(TrajectoryChangeView, self).__init__(*args)
        # 上方标题
        self.label_title = QtWidgets.QLabel("轨迹修改", self)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        view_lib.set_background_color(self.label_title)
        # 轨迹编号
        self.id_label_edit = h_row_view.HLabelEdit(self)
        self.id_label_edit.init(game_cfg.button_size[0],game_cfg.button_size[1],"轨迹编号","0")
        # 移动时间
        self.move_time_label_edit = h_row_view.HLabelEdit(self)
        self.move_time_label_edit.init(game_cfg.button_size[0],game_cfg.button_size[1],"移动时间","1")
        # 确定修改
        self.button_change = QtWidgets.QPushButton("确定修改", self)
        self.button_change.clicked.connect(self.click_change)
        # 添加到菜单列表
        self.add_view(self.label_title)
        self.add_view(self.id_label_edit)
        self.add_view(self.move_time_label_edit)
        self.add_view(self.button_change)
        

    # 点击确定修改
    def click_change(self):
        self.parent().change_trajectory()
    
    
    # 设置选中的轨迹点
    def set_select_trajectory(self, trajectory_obj):
        self.select_trajectory_id = trajectory_obj.trajectory_id
        self.id_label_edit.setText(str(trajectory_obj.trajectory_id))
        self.move_time_label_edit.setText(str(trajectory_obj.move_time))

            
        




