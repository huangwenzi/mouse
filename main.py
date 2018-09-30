from pynput import keyboard
import keysEvent as keysEventMd
keysEvent = keysEventMd.keysEvent
import dataMgr as dataMgrMd

# 数据管理的类
dataMgr = dataMgrMd.DataMgr()

# 键盘按下
def on_press(key):
    keysEvent.keyDown(dataMgr, key)

# 键盘弹起
def on_release(key):
    keysEvent.keyUp(dataMgr, key)

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()


