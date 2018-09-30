
# 数据管理类
class DataMgr:
    # 是否开启快捷键功能
    openFlag = True
    # 记录按下的键，只是按下，没有弹起
    keyDown = []
    # 保存记录快捷键对应坐标的字典{"number" : [x,y],...}
    postion = {}