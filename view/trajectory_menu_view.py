import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import pyautogui
import time
import json

import cfg.game as game_cfg
import lib.view_lib as view_lib
import lib.util_lib as util_lib
import view.trajectory_add_cfg_view as trajectory_add_cfg_view
import view.trajectory_change_view as trajectory_change_view
import view.h_list_view as h_list_view

# 枚举
class Enum(object):
    # 菜单类型
    menu_type_add = 1  # 添加轨迹
    menu_type_run = 2  # 运行轨迹
    menu_type_del = 3  # 删除轨迹
    menu_type_plan = 4  # 重排编号
    menu_type_change = 5  # 修改轨迹
    menu_type_load = 6  # 加载轨迹
    menu_type_save = 7  # 保存轨迹
    # 运行状态
    menu_run_start = 1  # 正常运行
    menu_run_stop = 2  # 停止运行


# 轨迹鼠标菜单
class TrajectoryMenuView(QtWidgets.QLabel):
    select_menu_1 = 0  # 选择的菜单1
    now_trajectory_id = 1

    def __init__(self, *args):
        super(TrajectoryMenuView, self).__init__(*args)
        # 基础设置
        desktop = QtWidgets.QApplication.desktop()
        self.resize(desktop.width() - game_cfg.button_size[0], desktop.height())
        self.move(game_cfg.button_size[0], 0)
        # view_lib.set_background_color(self)   # 这个不能启用，还有add_label

        # 初始化按钮
        self.menu_list = h_list_view.HListLabel(self)
        self.button_add = QtWidgets.QPushButton("添加轨迹", self.menu_list)
        self.button_add.clicked.connect(self.click_add)
        self.button_run = QtWidgets.QPushButton("运行轨迹", self)
        self.button_run.clicked.connect(self.click_run)
        self.button_del = QtWidgets.QPushButton("删除单个", self)
        self.button_del.clicked.connect(self.click_del)
        self.button_plan = QtWidgets.QPushButton("重排编号", self)
        self.button_plan.clicked.connect(self.click_plan)
        self.button_change = QtWidgets.QPushButton("修改轨迹", self)
        self.button_change.clicked.connect(self.click_change)
        self.button_load = QtWidgets.QPushButton("加载轨迹", self)
        self.button_load.clicked.connect(self.click_load)
        self.button_save = QtWidgets.QPushButton("保存轨迹", self)
        self.button_save.clicked.connect(self.click_save)
        # 添加到列表管理
        self.menu_list.add_view(self.button_add)
        self.menu_list.add_view(self.button_run)
        self.menu_list.add_view(self.button_del)
        self.menu_list.add_view(self.button_plan)
        self.menu_list.add_view(self.button_change)
        self.menu_list.add_view(self.button_load)
        self.menu_list.add_view(self.button_save)

        # 背景label 隔绝添加轨迹和轨迹的点击
        self.add_label = Trajectory_add_label(self)
        self.add_label.resize(
            desktop.width() - game_cfg.button_size[0] * 2, desktop.height()
        )
        self.add_label.move(game_cfg.button_size[0], 0)

        # 轨迹配置 y加偏移，windows有任务栏
        self.trajectory_cfg_view = trajectory_add_cfg_view.TrajectoryCfgView(self)
        self.trajectory_cfg_view.move(
            0,
            desktop.height()
            - self.trajectory_cfg_view.height()
            - game_cfg.taskbar_y_deviation,
        )

        # 数据
        self.trajectory_list = []
        self.run_timer = None
        self.run_status = Enum.menu_run_stop
        self.add_trajectory_time = time.time()

        # # 资源加载
        # self.add_pix = QPixmap()
        # self.add_pix.load("./image/tar.png")
        # 字体
        self.def_font = QtGui.QFont()
        self.def_font.setFamily("Arial")  # 括号里可以设置成自己想要的其它字体
        self.def_font.setPointSize(18)  # 括号里的数字可以设置成自己想要的字体大小

        # 默认选择第一个
        self.click_add()

    # 点击添加
    def click_add(self):
        # 设置功能选中
        self.set_select_menu_1(Enum.menu_type_add)
        view_lib.set_select_color(self.button_add)
        # 背景label置顶
        self.add_label.show()
        self.add_label.raise_()
        self.add_trajectory_time = time.time()

    # 点击运行
    def click_run(self):
        # 设置功能选中
        self.set_select_menu_1(Enum.menu_type_run)
        view_lib.set_select_color(self.button_run)

        # 先最小化
        self.parent().showMinimized()
        # 是否有有效列表
        list_len = len(self.trajectory_list)
        if list_len <= 0:
            return
        # 开始执行轨迹
        self.run_status = Enum.menu_run_start
        # 轨迹是否循环
        is_loop = self.trajectory_cfg_view.loop_label_button.text() == "是"
        while True:
            for trajectory_obj in self.trajectory_list:
                pyautogui.moveTo(
                    trajectory_obj.pos.x(),
                    trajectory_obj.pos.y(),
                    trajectory_obj.move_time,
                )
                # 是否停止运行
                if self.run_status == Enum.menu_run_stop:
                    self.parent().showMaximized()
                    return
                pyautogui.mouseDown()
                pyautogui.mouseUp()
            if not is_loop:
                self.parent().showMaximized()
                return

    # 删除轨迹
    def click_del(self):
        # 设置功能选中
        self.set_select_menu_1(Enum.menu_type_del)
        view_lib.set_select_color(self.button_del)

    # 重排编号
    def click_plan(self):
        # 设置功能选中
        self.set_select_menu_1(Enum.menu_type_plan)
        view_lib.set_select_color(self.button_plan)

        now_idx = 1
        for trajectory_obj in self.trajectory_list:
            trajectory_obj: TrajectoryObj = trajectory_obj
            trajectory_obj.set_trajectory_id(now_idx)
            now_idx += 1
        self.now_trajectory_id = now_idx

    # 修改轨迹
    def click_change(self):
        # 设置功能选中
        self.set_select_menu_1(Enum.menu_type_change)
        view_lib.set_select_color(self.button_change)
        # 添加修改视图
        self.trajectory_change_view = trajectory_change_view.TrajectoryChangeView(self)
        self.trajectory_change_view.move(
            0,
            self.height()
            - self.trajectory_cfg_view.height()
            - self.trajectory_change_view.height()
            - game_cfg.taskbar_y_deviation,
        )
        self.trajectory_change_view.show()

    # 加载轨迹
    def click_load(self):
        # 设置功能选中
        self.set_select_menu_1(Enum.menu_type_load)
        view_lib.set_select_color(self.button_load)

        util_lib.create_dir("./trajectory_file")
        path = QtWidgets.QFileDialog.getOpenFileNames(
            self, "加载轨迹", "./trajectory_file", "json Files(*.json)"
        )
        # filename = QtWidgets.QFileDialog.getOpenFileNames(self,'加载轨迹',"./trajectory_file", "All Files(*);;json Files(*.json)")
        if not path or len(path) < 1 or len(path[0]) < 1 or path[0][0] == "":
            return
        else:
            # 读取文件
            save_json = []
            with open(path[0][0], "r", encoding="utf8") as fp:
                save_json = json.load(fp)
            # 先删除旧数据
            for trajectory_obj in self.trajectory_list:
                trajectory_obj: TrajectoryObj = trajectory_obj
                trajectory_obj.close()
            self.trajectory_list = []
            # 加载数据
            # 加载轨迹
            for item in save_json["trajectory_list"]:
                # 初始化轨迹点
                x = item["pos"][0]
                y = item["pos"][1]
                add_trajectory_obj = TrajectoryObj(self)
                add_trajectory_obj.trajectory_id = item["trajectory_id"]
                add_trajectory_obj.pos = QtCore.QPoint(x, y)
                add_trajectory_obj.move_time = item["move_time"]
                add_trajectory_obj.resize(30, 30)
                add_trajectory_obj.setText(str(item["trajectory_id"]))
                add_trajectory_obj.move(
                    x - game_cfg.button_size[0] - 30 / 2, y - 30 / 2
                )
                add_trajectory_obj.setFont(self.def_font)
                add_trajectory_obj.setAlignment(QtCore.Qt.AlignCenter)
                add_trajectory_obj.show()
                self.trajectory_list.append(add_trajectory_obj)
            # 加载配置
            self.now_trajectory_id = save_json["cfg_map"]["now_trajectory_id"]

    # 保存轨迹
    def click_save(self):
        # 设置功能选中
        self.set_select_menu_1(Enum.menu_type_save)
        view_lib.set_select_color(self.button_save)

        util_lib.create_dir("./trajectory_file")
        path = "./trajectory_file/%s.json" % (time.strftime("%Y-%m-%d_%H-%M-%S"))
        path = QtWidgets.QFileDialog.getSaveFileName(
            self, "选择保存路径", path, "json(*.json)"
        )
        if path[0] == "":
            return
        else:
            # 转换数据
            save_json = {}
            # 轨迹点数据
            trajectory_list_list = []
            for trajectory_obj in self.trajectory_list:
                trajectory_obj: TrajectoryObj = trajectory_obj
                x = trajectory_obj.pos.x()
                y = trajectory_obj.pos.y()
                trajectory_list_list.append(
                    {
                        "trajectory_id": trajectory_obj.trajectory_id,
                        "move_time": trajectory_obj.move_time,
                        "pos": [x, y],
                    }
                )
            # 配置数据
            cfg_map = {"now_trajectory_id": self.now_trajectory_id}
            save_json["trajectory_list"] = trajectory_list_list
            save_json["cfg_map"] = cfg_map
            with open(path[0], "w", encoding="utf8") as fp:
                json.dump(save_json, fp)

    # 轨迹对象被点击
    def click_trajectory(self, trajectory_obj):
        trajectory_obj: TrajectoryObj = trajectory_obj
        # 根据选择的菜单类型操作
        if self.select_menu_1 == Enum.menu_type_del:
            # 删除轨迹
            trajectory_obj.hide()
            trajectory_obj.close()
            self.trajectory_list.remove(trajectory_obj)
        elif self.select_menu_1 == Enum.menu_type_change:
            self.trajectory_change_view.set_select_trajectory(trajectory_obj)

    # 触发键盘点击
    def click_key(self, key):
        if not hasattr(key, "char"):
            return
        char = key.char
        if self.select_menu_1 == Enum.menu_type_run:
            print("char:%s" % (char))
            if char == "1":
                self.run_status = Enum.menu_run_stop

    # 获取轨迹对象
    def get_trajectory_obj(self, trajectory_id):
        for item in self.trajectory_list:
            if item.trajectory_id == trajectory_id:
                return item
        return None

    # 设置选中的菜单
    def set_select_menu_1(self, select_type):
        if self.select_menu_1 == select_type:
            return

        # 先取消其他选择
        if self.select_menu_1 == Enum.menu_type_add:
            # 添加轨迹
            view_lib.reset_select_color(self.button_add)
            # 放下添加背景
            self.add_label.hide()
        elif self.select_menu_1 == Enum.menu_type_run:
            # 运行轨迹
            view_lib.reset_select_color(self.button_run)
            if self.run_timer:
                self.run_timer.sotp()
                self.run_timer = None
        elif self.select_menu_1 == Enum.menu_type_del:
            # 删除轨迹
            view_lib.reset_select_color(self.button_del)
        elif self.select_menu_1 == Enum.menu_type_plan:
            # 重新编号
            view_lib.reset_select_color(self.button_plan)
        elif self.select_menu_1 == Enum.menu_type_change:
            # 修改轨迹
            view_lib.reset_select_color(self.button_change)
            self.trajectory_change_view.close()
        elif self.select_menu_1 == Enum.menu_type_load:
            # 修改轨迹
            view_lib.reset_select_color(self.button_load)
        elif self.select_menu_1 == Enum.menu_type_save:
            # 修改轨迹
            view_lib.reset_select_color(self.button_save)
        else:
            pass

        # 修改成对应的选择
        self.select_menu_1 = select_type

    # 添加轨迹点
    def add_trajectory_obj(self, x, y):
        # 初始化轨迹点
        add_trajectory_obj = TrajectoryObj(self)
        add_trajectory_obj.trajectory_id = self.now_trajectory_id
        add_trajectory_obj.pos = QtGui.QCursor.pos()
        add_trajectory_obj.move_time = int(
            self.trajectory_cfg_view.move_time_label_edit.text()
        )
        add_trajectory_obj.resize(30, 30)
        add_trajectory_obj.setText("%s" % (add_trajectory_obj.trajectory_id))
        add_trajectory_obj.move(x - game_cfg.button_size[0] - 30 / 2, y - 30 / 2)
        add_trajectory_obj.setFont(self.def_font)
        add_trajectory_obj.setAlignment(QtCore.Qt.AlignCenter)
        add_trajectory_obj.show()
        self.now_trajectory_id += 1
        self.trajectory_list.append(add_trajectory_obj)
        # 背景label置顶
        self.add_label.raise_()
        # 轨迹是否穿透
        if self.trajectory_cfg_view.penetrate_label_button.text() == "是":
            # 最小化，然后点击一下
            self.parent().showMinimized()
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            # 最大化
            self.parent().showMaximized()
        # 耗时是否跟随
        now = time.time()
        if self.trajectory_cfg_view.time_follow_label_button.text() == "是":
            # 保留两位小数
            move_time = now - self.add_trajectory_time
            add_trajectory_obj.move_time = round(move_time, 2)
        self.add_trajectory_time = now

    # 修改轨迹
    def change_trajectory(self):
        # 修改编号
        trajectory_obj: TrajectoryObj = self.get_trajectory_obj(
            self.trajectory_change_view.select_trajectory_id
        )
        old_trajectory_id = trajectory_obj.trajectory_id
        old_move_time = trajectory_obj.move_time
        new_trajectory_id = util_lib.str_to_int(
            self.trajectory_change_view.id_label_edit.text(), old_trajectory_id
        )
        new_move_time = util_lib.str_to_float(
            self.trajectory_change_view.move_time_label_edit.text(), old_move_time
        )
        self.trajectory_list.remove(trajectory_obj)
        # 把等于新编号的轨迹往后推
        id_idx = new_trajectory_id
        for item in self.trajectory_list:
            if item.trajectory_id == id_idx:
                item.set_trajectory_id(id_idx + 1)
                id_idx += 1
        # 加到最后
        trajectory_obj.set_trajectory_id(new_trajectory_id)
        trajectory_obj.move_time = new_move_time
        self.trajectory_list.append(trajectory_obj)
        # 排序
        def takeSecond(elem):
            return elem.trajectory_id

        self.trajectory_list.sort(key=takeSecond)


# 轨迹添加背景label
class Trajectory_add_label(QtWidgets.QLabel):
    def __init__(self, *args):
        super(Trajectory_add_label, self).__init__(*args)

    # 鼠标事件
    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.buttons() == QtCore.Qt.LeftButton:  # 左键按下
            # print("单击鼠标左键")  # 响应测试语句
            # 触发上面的添加
            pos = QtGui.QCursor.pos()
            self.parent().add_trajectory_obj(pos.x(), pos.y())
        # elif event.buttons() == Qt.RightButton:  # 右键按下
        #     print("单击鼠标右键")  # 响应测试语句
        # elif event.buttons() == Qt.MidButton:  # 中键按下
        #     print("单击鼠标中键")  # 响应测试语句
        # elif event.buttons() == Qt.LeftButton | Qt.RightButton:  # 左右键同时按下
        #     print("单击鼠标左右键")  # 响应测试语句
        # elif event.buttons() == Qt.LeftButton | Qt.MidButton:  # 左中键同时按下
        #     print("单击鼠标左中键")  # 响应测试语句
        # elif event.buttons() == Qt.MidButton | Qt.RightButton:  # 右中键同时按下
        #     print("单击鼠标右中键")  # 响应测试语句
        # elif event.buttons() == Qt.LeftButton | Qt.MidButton | Qt.RightButton:  # 左中右键同时按下
        #     print("单击鼠标左中右键")  # 响应测试语句


# 轨迹对象
class TrajectoryObj(QtWidgets.QLabel):
    trajectory_id = 0  # id
    move_time = 1  # 移动时间
    pos: QtCore.QPoint = None  # 绝对坐标

    def __init__(self, *args):
        super(TrajectoryObj, self).__init__(*args)

    # 重写信号抛出
    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == QtCore.Qt.LeftButton:
            # 被点击
            self.parent().click_trajectory(self)

    # 设置轨迹id
    def set_trajectory_id(self, trajectory_id):
        self.trajectory_id = trajectory_id
        self.setText(str(trajectory_id))
