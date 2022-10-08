import sys
import PyQt5.QtWidgets as QtWidgets
import view.main_view as main_view


# 带gui的鼠标功能


def run():
    app = QtWidgets.QApplication([])

    # 不赋值界面会一闪而过，被回收
    main_biew = main_view.MainView()

    sys.exit(app.exec_())  # 应用进入主循环。在这个地方，事件处理开始执行。主循环用于接收来自窗口触发的事件，
    # 并且转发他们到widget应用上处理。如果我们调用exit()方法或主widget组件被销毁，主循环将退出。
    # sys.exit()方法确保一个不留垃圾的退出。系统环境将会被通知应用是怎样被结束的。


run()
