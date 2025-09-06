import tkinter as tk
from tkinter import ttk
import os
import random
from tkinter import messagebox
import sys
import threading
import time
import shutil

# 全局变量
picking = False
root = None
start_button = None
stop_button = None
result_display = None
global_path = ""

def start_picking():
    global picking
    picking = True
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    continuous_picking()

def stop_picking():
    global picking
    picking = False
    result = result_display.cget("text")
    
    history_path = os.path.join(global_path, '_internal', 'history.txt')
    try:
        with open(history_path, 'a', encoding='utf-8') as file:
            file.write('\n' + result)
    except Exception as e:
        print(f"保存历史记录失败: {e}")
    
    if delete_result_from_source.get():
        try:
            default_path = os.path.join(global_path, '_internal', 'default.txt')
            with open(default_path, 'r+', encoding='utf-8') as file:
                lines = file.readlines()
                current_result = result_display.cget("text") + '\n'
                if current_result in lines:
                    lines.remove(current_result)
                    file.seek(0)
                    file.truncate()
                    file.writelines(lines)
        except Exception as e:
            print(f"删除结果失败: {e}")
    
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

def continuous_picking():
    default_path = os.path.join(global_path, '_internal', 'default.txt')
    try:
        with open(default_path, 'r', encoding='utf-8') as file:
            data = [line.strip() for line in file.readlines() if line.strip()]
    except Exception as e:
        messagebox.showerror("错误", f"无法读取默认签号文件: {e}")
        stop_picking()
        return

    def update_display():
        if picking and data:
            result = random.choice(data)
            result_display.config(text=result, font=("Helvetica", result_font_size.get()))
            try:
                delay_time = float(delay.get())
                if not 0.01 <= delay_time <= 1:
                    messagebox.showerror("错误", "抽取频率应在0.01-1秒之间")
                    stop_picking()
                    return
                root.after(int(delay_time * 1000), update_display)
            except ValueError:
                messagebox.showerror("错误", "无效的延迟时间")
                stop_picking()
        elif not data:
            messagebox.showerror("错误", "签号列表为空")
            stop_picking()

    update_display()

def listen_keyboard():
    """在Debian上使用tkinter内置的键盘事件监听"""
    def on_space_press(event):
        global picking
        if not picking:
            start_picking()
        else:
            stop_picking()
    
    root.bind('<space>', on_space_press)
    
    # 保持线程运行
    while True:
        time.sleep(1)

def reset_default_list():
    try:
        default_bf_path = os.path.join(global_path, '_internal', 'default.bf')
        default_path = os.path.join(global_path, '_internal', 'default.txt')
        if os.path.exists(default_bf_path):
            shutil.copy(default_bf_path, default_path)
            messagebox.showinfo("成功", "已重置默认签号列表")
        else:
            messagebox.showerror("错误", "找不到备份文件，重置失败！")
    except Exception as e:
        messagebox.showerror("错误", f"重置失败: {e}")

def save_edited_list(text_widget):
    try:
        content = text_widget.get("1.0", tk.END)
        default_path = os.path.join(global_path, '_internal', 'default.txt')
        with open(default_path, 'w', encoding='utf-8') as file:
            file.write(content)
        messagebox.showinfo("成功", "签号列表已保存")
        text_widget.master.destroy()
    except Exception as e:
        messagebox.showerror("错误", f"保存失败: {e}")

def edit_default_list():
    try:
        default_path = os.path.join(global_path, '_internal', 'default.txt')
        if not os.path.exists(default_path):
            messagebox.showerror("错误", f"找不到 {default_path} 文件")
            return
            
        with open(default_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        edit_window = tk.Toplevel(root)
        edit_window.title("编辑签号列表")
        edit_window.geometry("600x500")
        edit_window.attributes('-topmost', True)
        
        main_frame = tk.Frame(edit_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(main_frame, wrap=tk.WORD)
        scrollbar = tk.Scrollbar(main_frame, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.insert(tk.END, content)
        text_widget.config(font=("宋体", 12))
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        button_frame = tk.Frame(edit_window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        cancel_button = tk.Button(button_frame, text="取消", command=edit_window.destroy, 
                                height=1, width=8, bg='lightcoral', font=("楷体", 12))
        cancel_button.pack(side=tk.RIGHT, padx=5)
        
        save_button = tk.Button(button_frame, text="保存", command=lambda: save_edited_list(text_widget), 
                              height=1, width=8, bg='lightgreen', font=("楷体", 12))
        save_button.pack(side=tk.RIGHT, padx=5)
        
    except Exception as e:
        messagebox.showerror("错误", f"编辑失败: {e}")

def show_history():
    history_path = os.path.join(global_path, '_internal', 'history.txt')
    try:
        with open(history_path, 'r', encoding='utf-8') as file:
            history_content = file.readlines()
    except:
        history_content = []
    
    history_window = tk.Toplevel(root)
    history_window.title("历史记录")
    history_window.geometry("300x400")
    history_window.attributes('-topmost', True)
    
    frame = tk.Frame(history_window)
    frame.pack(fill=tk.BOTH, expand=True)
    
    text_widget = tk.Text(frame, wrap=tk.WORD)
    scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    
    text_widget.tag_configure("center", justify='center')
    text_widget.config(state=tk.NORMAL, bg='lightyellow', font=("楷体", 14))
    
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    for item in history_content:
        if item.strip():
            text_widget.insert(tk.END, item.strip() + '\n', "center")
    
    text_widget.config(state=tk.DISABLED)

def create_lottery_frame(parent):
    """创建抽签功能的Frame"""
    frame = tk.Frame(parent, bg='lightskyblue')
    
    global start_button, stop_button, result_display, result_font_size, delay, delete_result_from_source
    
    delay = tk.StringVar(value="0.03")
    result_font_size = tk.IntVar(value=100)
    delete_result_from_source = tk.BooleanVar(value=True)
    
    button_frame = tk.Frame(frame, bg='lightskyblue')
    button_frame.pack(pady=10)
    
    start_button = tk.Button(button_frame, text="开始", command=start_picking, 
                           height=1, width=8, bg='lightgreen', font=("楷体", 15))
    start_button.pack(side=tk.LEFT, padx=10)
    
    stop_button = tk.Button(button_frame, text="停止", command=stop_picking, 
                          height=1, width=8, bg='lightgreen', font=("楷体", 15), state=tk.DISABLED)
    stop_button.pack(side=tk.LEFT, padx=10)

    tk.Label(frame, text="结果：", bg='lightskyblue', font=("楷体", 15)).pack()
    result_display = tk.Label(frame, text="", font=("Helvetica", result_font_size.get()), 
                            bg='lightskyblue', fg='black')
    result_display.pack()

    def copy_result():
        result_text = result_display.cget("text")
        root.clipboard_clear()
        root.clipboard_append(result_text)
        messagebox.showinfo("成功", "结果已复制到剪贴板")
    
    copy_button = tk.Button(frame, text="复制结果", command=copy_result, 
                          height=1, width=8, bg='lightgreen', font=("楷体", 15))
    copy_button.pack(pady=5)

    settings_frame = tk.Frame(frame, bg='lightskyblue')
    settings_frame.pack(pady=10)
    
    tk.Label(settings_frame, text="抽取频率(0.01~1秒)：", bg='lightskyblue', 
            font=("楷体", 12)).grid(row=0, column=0, sticky='e', padx=5)
    delay_entry = tk.Entry(settings_frame, textvariable=delay, width=8, font=("楷体", 12))
    delay_entry.grid(row=0, column=1, sticky='w', padx=5)
    
    tk.Label(settings_frame, text="字体大小：", bg='lightskyblue', 
            font=("楷体", 12)).grid(row=1, column=0, sticky='e', padx=5)
    font_size_entry = tk.Entry(settings_frame, textvariable=result_font_size, width=8, font=("楷体", 12))
    font_size_entry.grid(row=1, column=1, sticky='w', padx=5)

    delete_checkbox = tk.Checkbutton(frame, text="停止时从列表中删除结果", 
                                   variable=delete_result_from_source, 
                                   bg='lightskyblue', font=("楷体", 12))
    delete_checkbox.pack(pady=5)

    list_management_frame = tk.Frame(frame, bg='lightskyblue')
    list_management_frame.pack(pady=10)
    
    reset_button = tk.Button(list_management_frame, text="重置签号列表", command=reset_default_list, 
                            height=1, width=12, bg='lightgreen', font=("楷体", 12))
    reset_button.pack(side=tk.LEFT, padx=5)
    
    edit_button = tk.Button(list_management_frame, text="编辑签号列表", command=edit_default_list, 
                           height=1, width=12, bg='lightgreen', font=("楷体", 12))
    edit_button.pack(side=tk.LEFT, padx=5)

    history_button = tk.Button(frame, text="历史记录", command=show_history, 
                             height=1, width=10, bg='lightgreen', font=("楷体", 15))
    history_button.pack(pady=10)

    tip_label = tk.Label(frame, text="提示：按空格键开始/停止抽签", 
                       bg='lightskyblue', font=("楷体", 12))
    tip_label.pack(side=tk.BOTTOM, pady=10)
    
    return frame

def create_lucky_draw_frame(parent):
    """创建抓阄功能的Frame"""
    main_frame = tk.Frame(parent, bg='lightgreen')
    
    input_frames = []
    entries = []
    draw_button = None
    
    def create_initial_interface():
        """初始界面"""
        for widget in main_frame.winfo_children():
            widget.destroy()
        
        tk.Label(main_frame, text="请输入抓阄种类数量：", 
                bg='lightgreen', font=("楷体", 16)).pack(pady=15)
        
        num_entry = tk.Entry(main_frame, width=10, font=("楷体", 16))
        num_entry.pack(pady=10)
        num_entry.insert(0, "1")
        
        tk.Button(main_frame, text="确定", command=lambda: create_draw_list(num_entry),
                height=1, width=8, bg='lightgreen', font=("楷体", 16)).pack(pady=15)
    
    def create_draw_list(num_entry):
        """创建抓阄种类输入界面"""
        nonlocal input_frames, entries, draw_button
        try:
            num = int(num_entry.get())
            if num < 1 or num > 20:
                messagebox.showerror("错误", "种类数量应在1到20之间", parent=main_frame)
                return
            
            for frame in input_frames:
                frame.destroy()
            input_frames.clear()
            entries.clear()
            
            if draw_button:
                draw_button.destroy()
            
            for i in range(num):
                input_frame = tk.Frame(main_frame, bg='lightgreen')
                input_frame.pack(pady=8)
                
                tk.Label(input_frame, text=f"种类{i+1}：", bg='lightgreen', 
                        font=("楷体", 16)).pack(side=tk.LEFT)
                
                name_entry = tk.Entry(input_frame, width=15, font=("楷体", 16))
                name_entry.pack(side=tk.LEFT, padx=5)
                name_entry.insert(0, f"种类{i+1}")
                
                tk.Label(input_frame, text="数量：", bg='lightgreen', 
                        font=("楷体", 16)).pack(side=tk.LEFT)
                
                count_entry = tk.Entry(input_frame, width=5, font=("楷体", 16))
                count_entry.pack(side=tk.LEFT, padx=5)
                count_entry.insert(0, "1")
                
                entries.append((name_entry, count_entry))
                input_frames.append(input_frame)
            
            draw_button = tk.Button(main_frame, text="开始抓阄", command=start_draw_process,
                                  height=1, width=12, bg='lightgreen', font=("楷体", 16))
            draw_button.pack(pady=20)
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效数字", parent=main_frame)

    def start_draw_process():
        """开始抓阄流程"""
        try:
            draw_types = []
            total_count = 0
            
            for name_entry, count_entry in entries:
                name = name_entry.get().strip()
                count = int(count_entry.get())
                
                if not name:
                    messagebox.showerror("错误", "种类名称不能为空", parent=main_frame)
                    return
                if count <= 0:
                    messagebox.showerror("错误", "数量必须大于0", parent=main_frame)
                    return
                
                draw_types.append({
                    "name": name, 
                    "count": count, 
                    "original_count": count,
                    "assigned_students": []
                })
                total_count += count
            
            default_path = os.path.join(global_path, '_internal', 'default.txt')
            try:
                with open(default_path, 'r', encoding='utf-8') as file:
                    students = [line.strip() for line in file.readlines() if line.strip()]
            except Exception as e:
                messagebox.showerror("错误", f"无法读取学生名单: {str(e)}", parent=main_frame)
                return
            
            if len(students) < total_count:
                messagebox.showerror("错误", f"需要{total_count}人，但只有{len(students)}人", parent=main_frame)
                return
            
            random.shuffle(students)
            
            for widget in main_frame.winfo_children():
                widget.destroy()
            
            create_draw_execution_interface(students, draw_types)
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效数字", parent=main_frame)

    def create_draw_execution_interface(students, draw_types):
        """创建抓阄执行界面"""
        container = tk.Frame(main_frame, bg='lightgreen')
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 学生列表框架
        student_frame = tk.Frame(container, bg='lightgreen')
        student_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(student_frame, text="学生列表", bg='lightgreen', 
                font=("楷体", 16)).pack(pady=5)
        
        student_text = tk.Text(student_frame, height=12, width=20,
                             font=("楷体", 14), bg='white')
        scrollbar_student = tk.Scrollbar(student_frame, orient=tk.VERTICAL)
        student_text.config(yscrollcommand=scrollbar_student.set)
        scrollbar_student.config(command=student_text.yview)
        
        for student in students:
            student_text.insert(tk.END, student + "\n")
        
        scrollbar_student.pack(side=tk.RIGHT, fill=tk.Y)
        student_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        student_text.config(state=tk.DISABLED)
        
        # 抓阄结果框架
        result_frame = tk.Frame(container, bg='lightgreen')
        result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(result_frame, text="抓阄结果", bg='lightgreen', 
                font=("楷体", 16)).pack(pady=5)
        
        result_text = tk.Text(result_frame, height=12, width=30,
                            font=("楷体", 14), bg='white')
        scrollbar_result = tk.Scrollbar(result_frame, orient=tk.VERTICAL)
        result_text.config(yscrollcommand=scrollbar_result.set)
        scrollbar_result.config(command=result_text.yview)
        
        # 初始化结果显示
        result_data = []
        for draw_type in draw_types:
            result_data.append({
                "name": draw_type["name"],
                "count": 0,
                "original_count": draw_type["original_count"],
                "students": []
            })
            result_text.insert(tk.END, f"{draw_type['name']} (0/{draw_type['original_count']})\n\n")
        
        scrollbar_result.pack(side=tk.RIGHT, fill=tk.Y)
        result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        result_text.config(state=tk.DISABLED)
        
        # 当前学生显示
        current_student_var = tk.StringVar(value="")
        tk.Label(main_frame, textvariable=current_student_var, 
                bg='lightgreen', font=("楷体", 18)).pack(pady=5)
        
        # 控制按钮框架
        button_frame = tk.Frame(main_frame, bg='lightgreen')
        button_frame.pack(pady=10)
        
        draw_button = tk.Button(button_frame, text="抽取", 
                              height=1, width=8, bg='lightgreen', 
                              font=("楷体", 16))
        draw_button.pack(side=tk.LEFT, padx=10)
        
        back_button = tk.Button(button_frame, text="返回", 
                              command=create_initial_interface,
                              height=1, width=8, bg='lightgreen', 
                              font=("楷体", 16))
        back_button.pack(side=tk.LEFT, padx=10)
        
        def update_result_display():
            """更新结果显示"""
            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)
            for data in result_data:
                result_text.insert(tk.END, f"{data['name']} ({data['count']}/{data['original_count']}):\n")
                if data['students']:
                    # 每行显示最多8个学生名字
                    for i in range(0, len(data['students']), 8):
                        group = data['students'][i:i+8]
                        result_text.insert(tk.END, ", ".join(group) + "\n")
                result_text.insert(tk.END, "\n")
            result_text.config(state=tk.DISABLED)
        
        def draw_next_student():
            """抽取下一位学生"""
            if not students:
                messagebox.showinfo("完成", "所有学生已完成抓阄！", parent=main_frame)
                return
            
            if all(draw_type["count"] == 0 for draw_type in draw_types):
                messagebox.showinfo("完成", "所有类型已分配完毕！", parent=main_frame)
                return
            
            # 获取学生
            student = students.pop(0)
            current_student_var.set(f"当前: {student}")
            
            # 选择类型
            available_types = [i for i, t in enumerate(draw_types) if t["count"] > 0]
            if not available_types:
                return
            
            chosen_index = random.choice(available_types)
            chosen_type = draw_types[chosen_index]
            chosen_type["count"] -= 1
            chosen_type["assigned_students"].append(student)
            
            # 更新结果数据
            result_data[chosen_index]["count"] += 1
            result_data[chosen_index]["students"].append(student)
            
            # 在学生列表中添加标记
            student_text.config(state=tk.NORMAL)
            content = student_text.get("1.0", tk.END)
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if line.startswith(student) and "→" not in line:
                    line_num = i + 1
                    student_text.delete(f"{line_num}.0", f"{line_num}.end")
                    student_text.insert(f"{line_num}.0", f"{student} → {chosen_type['name']}")
                    break
            student_text.config(state=tk.DISABLED)
            
            # 更新结果显示
            update_result_display()
        
        draw_button.config(command=draw_next_student)
        update_result_display()
    
    create_initial_interface()
    return main_frame

def ensure_necessary_files():
    """确保必要的文件和目录存在"""
    internal_dir = os.path.join(global_path, '_internal')
    if not os.path.exists(internal_dir):
        os.makedirs(internal_dir)
        file_path = os.path.join(internal_dir, filename)
def main():
    global root, global_path
    
    # 获取当前路径
    if getattr(sys, 'frozen', False):
        global_path = os.path.dirname(sys.executable)
    else:
        global_path = os.path.dirname(os.path.abspath(__file__))
    
    # 确保必要文件存在
    ensure_necessary_files()
    
    # 创建主窗口
    root = tk.Tk()
    root.title("抽签助手 - Linux Debian版")
    root.geometry("700x600")
    root.configure(bg='lightskyblue')
    
    # 设置窗口居中
    root.update_idletasks()
    width = 700
    height = 600
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.attributes('-topmost', True)

    # 创建导航栏
    nav_frame = tk.Frame(root, bg='white', height=40)
    nav_frame.pack(fill=tk.X, pady=0)
    nav_frame.pack_propagate(False)
    
    # 抽签按钮
    lottery_btn = tk.Button(nav_frame, text="抽签", height=1, bg='lightskyblue', 
                          font=("楷体", 14), relief=tk.FLAT, bd=0)
    lottery_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # 抓阄按钮
    draw_btn = tk.Button(nav_frame, text="抓阄", height=1, bg='white', 
                        font=("楷体", 14), relief=tk.FLAT, bd=0)
    draw_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # 创建内容容器
    container = tk.Frame(root)
    container.pack(fill=tk.BOTH, expand=True)
    
    # 创建两个功能的Frame
    lottery_frame = create_lottery_frame(container)
    draw_frame = create_lucky_draw_frame(container)
    
    # 初始显示抽签界面
    lottery_frame.pack(fill=tk.BOTH, expand=True)
    draw_frame.pack_forget()
    
    # 切换函数
    def show_lottery():
        lottery_btn.config(bg='lightskyblue')
        draw_btn.config(bg='white')
        draw_frame.pack_forget()
        lottery_frame.pack(fill=tk.BOTH, expand=True)
    
    def show_draw():
        lottery_btn.config(bg='white')
        draw_btn.config(bg='lightgreen')
        lottery_frame.pack_forget()
        draw_frame.pack(fill=tk.BOTH, expand=True)
    
    # 绑定按钮事件
    lottery_btn.config(command=show_lottery)
    draw_btn.config(command=show_draw)
    
    # 绑定键盘事件
    def on_space_press(event):
        global picking
        if not picking:
            start_picking()
        else:
            stop_picking()
    
    root.bind('<space>', on_space_press)
    
    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    main()