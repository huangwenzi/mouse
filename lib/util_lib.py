import os



# 字符串转浮点数
def str_to_float(in_str, def_ret):
    try:
        return float(in_str)
    except Exception as err:
        return def_ret

# 字符串转整数
def str_to_int(in_str, def_ret):
    try:
        return int(in_str)
    except Exception as err:
        return def_ret

# 如果目录不存在就创建
def create_dir(path):
    if os.path.exists(path):
        return
    else:
        os.makedirs(path)










