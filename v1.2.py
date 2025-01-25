from pynput import keyboard
import time
from IPython.display import clear_output, display
import os
import json

# 打开txt文件
filename = '1.txt'  
progress_file = f'{filename}progress.json'  # 用于保存进度的文件

# 生成器函数，逐行读取文件
def read_line_by_line(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            yield line.strip()  # strip() 用于去除行末的换行符

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

# 逐行读取文件并返回行数
def count_lines(file_name):
    with open(file_name, 'r') as file:
        return sum(1 for _ in file)

# 获取文件总行数
max_lines = count_lines(filename)
current_line_index = load_progress()  # 加载上次的进度

# 定义一个函数来打印当前行和进度
def print_current_line():
    clear_output(wait=True)  # 清除之前的输出
    display(f"[{current_line_index + 1}/{max_lines}]{current_line.strip()}")

# 监听按键的函数
def on_press(key):
    global current_line_index, current_line, line_generator

    try:
        if key.char == 'e':  # 按 'e' 键退出程序
            clear_output(wait=True)  # 清除之前的输出
            print("程序已退出.")
            save_progress()  # 保存进度
            return False  # 停止监
        
        elif key.char == 's':  # 向下
            if current_line_index < max_lines - 1:
                current_line_index += 1
                current_line = next(line_generator)  # 跳到下一行
            print_current_line()

        elif key.char == 'w':  # 向上
            if current_line_index > 0:
                current_line_index -= 1
                # 重新创建生成器并跳到前一个行
                line_generator = read_line_by_line(filename)
                for _ in range(current_line_index):
                    next(line_generator)
                current_line = next(line_generator)
            print_current_line()

        elif key.char == 'j':  # 按 'j' 键跳转到指定行
            clear_output(wait=True)  # 清除之前的输出
            # 提示用户输入跳转的行号
            print("请输入行号以跳转：", end="")
            user_input = input()  # 获取用户输入
            try:
                jump_line = int(user_input) - 1  # 转换为零基索引
                if 0 <= jump_line < max_lines:
                    current_line_index = jump_line
                    # 跳转到指定行
                    line_generator = read_line_by_line(filename)
                    for _ in range(current_line_index):
                        next(line_generator)
                    current_line = next(line_generator)
                    print_current_line()  # 打印跳转后的行
                else:
                    print("行号超出范围，请输入有效的行号。")
            except ValueError:
                print("请输入有效的数字行号。")

    except AttributeError:
        # 忽略特殊键（如 shift, ctrl 等）
        pass
    except Exception as e:
        # 捕获其他异常，防止程序退出
        print(e)

try:
    print('请先点击这里')
    # 创建生成器
    line_generator = read_line_by_line(filename)
    # 跳到当前保存的进度行
    for _ in range(current_line_index):
        next(line_generator)
    current_line = next(line_generator)  # 获取当前行

    # 启动键盘监听
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
        
# 捕获 KeyboardInterrupt 异常，确保程序退出时保存进度
except KeyboardInterrupt:
    clear_output(wait=True)  # 清除之前的输出
    # 捕获到 KeyboardInterrupt 时保存进度
    print("检测到 KeyboardInterrupt，程序已退出.")
    save_progress()  # 保存进度