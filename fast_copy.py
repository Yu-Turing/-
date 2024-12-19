import shutil
import os
import sys


def copy_and_rename_items(source_item_path, num_copies, new_names):
    """
    复制文件或文件夹并改名
    :param source_item_path: 源文件或文件夹的绝对路径
    :param num_copies: 要复制的份数
    :param new_names: 新文件名或文件夹名的列表，长度要和 num_copies 一致
    """
    if len(new_names)!= num_copies:
        raise ValueError("新文件名/文件夹名列表长度与要复制的份数不一致")
    for i in range(num_copies):
        new_item_path = os.path.join(os.path.dirname(source_item_path), new_names[i])
        if os.path.isfile(source_item_path):
            try:
                shutil.copy2(source_item_path, new_item_path)
            except Exception as e:
                print(f"复制文件时出现错误: {e}")
        elif os.path.isdir(source_item_path):
            try:
                shutil.copytree(source_item_path, new_item_path)
            except Exception as e:
                print(f"复制文件夹时出现错误: {e}")
        else:
            print(f"提供的源路径 {source_item_path} 既不是文件也不是文件夹，请检查。")


if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        # 如果是打包后的可执行文件（PyInstaller）
        current_directory = os.path.dirname(sys.executable)
    else:
        # 如果是普通的 Python 脚本
        current_directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(current_directory, "config.txt")
    print("current_directory：", current_directory)
    print("config_file_path：", config_file_path)
    default_config_content = [
        "original_file.txt\n",  # 默认的源文件名，可按需修改
        "3\n",  # 默认的要复制的份数，可按需修改
        "new_file_1.txt\n",  # 默认的新文件名示例，可按需修改
        "new_file_2.txt\n",
        "new_file_3.txt\n"
    ]
    try:
        print("我看看能不能打开")
        try:
            with open(config_file_path, 'r', encoding='utf-8') as config_file:
                print("我打开了!!!!!!!!")
                lines = config_file.readlines()
                source_item = lines[0].strip()
                num_copies = int(lines[1].strip())
                new_names = [name.strip() for name in lines[2:]]
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                source_item_path = os.path.join(desktop_path, source_item)
                copy_and_rename_items(source_item_path, num_copies, new_names)
        except Exception as e:
            print(f"使用 utf-8 编码打开文件时出现错误: {e}")
            # 尝试使用 ANSI 编码打开
            with open(config_file_path, 'r', encoding='ansi') as config_file:
                print("我使用 ANSI 打开了!!!!!!!!")
                lines = config_file.readlines()
                source_item = lines[0].strip()
                num_copies = int(lines[1].strip())
                new_names = [name.strip() for name in lines[2:]]
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                source_item_path = os.path.join(desktop_path, source_item)
                copy_and_rename_items(source_item_path, num_copies, new_names)
    except FileNotFoundError:
        print("配置文件 config.txt 未找到，将自动创建默认配置文件。")
        with open(config_file_path, 'w', encoding='utf-8') as new_config_file:
            new_config_file.writelines(default_config_content)
    except IndexError:
        print("配置文件 config.txt 内容格式不正确，请检查。")
    except ValueError as e:
        print(f"参数解析出现错误: {e}")