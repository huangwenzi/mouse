from pynput import keyboard
import keysEvent as keysEventMd
keysEvent = keysEventMd.keysEvent
keysRet = keysEventMd.keysRet
import dataMgr as dataMgrMd

# 数据管理的类
dataMgr = dataMgrMd.DataMgr()

# 键盘按下
def on_press(key):
    ret = keysEvent.keyDown(dataMgr, key)
    # 返回的是退出
    if ret == keysRet.isExit:
        return False

# 键盘弹起
def on_release(key):
    keysEvent.keyUp(dataMgr, key)

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# 使用方法
# 0是目前唯一辅助键
# 0 + "1~9" 可以记录鼠标位置给对应数字
# "1~9"     触发鼠标移动到对应位置并点击功能
# 0 + "."   开启和关闭功能
# 0 + "+"   截取全屏，保存在当前目录下的screenshot