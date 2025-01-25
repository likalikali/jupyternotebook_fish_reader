from pynput import keyboard
import time
from IPython.display import clear_output, display
import os
import json

# 打开txt文件
filename = '1.txt'
progress_file = f'{filename}progress.json'  # 用于保存进度的文件

def read_lines(file_name):
    # 读取文件的所有行
    with open(file_name, 'r') as file:
        lines = file.readlines()
    return lines

# 尝试从进度文件中读取保存的进度
def load_progress():
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            progress = json.load(f)
            return progress.get('current_line_index', 0)
    return 0

# 保存当前进度
def save_progress():
    progress = {'current_line_index': current_line_index}
    with open(progress_file, 'w') as f:
        json.dump(progress, f)

lines = read_lines(filename)  # 读取所有行
current_line_index = load_progress()  # 加载上次的进度
max_lines = len(lines)  # 文件的总行数

# 定义一个函数来打印当前行和进度
def print_current_line():
    clear_output(wait=True)  # 清除之前的输出
    # 显示当前行及进度
    display(f"[{current_line_index + 1}/{max_lines}]{lines[current_line_index].strip()}")

# 监听按键的函数
def on_press(key):
    global current_line_index
    try:
        if key.char == 'e':  # 按 'e' 键退出程序
            clear_output(wait=True)  # 清除之前的输出
            print("程序已退出.")
            save_progress()  # 保存进度
            return False  # 停止监听

        if key.char == 's':  # 向下
            if current_line_index < max_lines - 1:
                current_line_index += 1
            print_current_line()

        elif key.char == 'w':  # 向上
            if current_line_index > 0:
                current_line_index -= 1
            print_current_line()

    except AttributeError:
        # 忽略特殊键（如 shift, ctrl 等）
        pass
    
    except Exception as e:
        # 捕获其他异常，防止程序退出
        pass

# 捕获 KeyboardInterrupt 异常，确保程序退出时保存进度
try:
    # 启动键盘监听
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

except KeyboardInterrupt:
    # 捕获到 KeyboardInterrupt 时保存进度
    clear_output(wait=True)  # 清除之前的输出
    print("检测到 KeyboardInterrupt，程序已退出.")
    save_progress()  # 保存进度