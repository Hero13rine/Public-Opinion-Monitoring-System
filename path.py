## 获得某个路径下所有文件夹与子文件的树形结构
import json, os

def list_dir(path, res):
    for i in os.listdir(path):
        temp_dir = os.path.join(path, i)
        if os.path.isdir(temp_dir):
            temp = {"dirname": temp_dir, 'child_dirs': [], 'files': []}
            res['child_dirs'].append(list_dir(temp_dir, temp))
        else:
            res['files'].append(i)
    return res

def get_config_dirs():
    res = {'dirname': 'root', 'child_dirs': [], 'files': []}  # 当前路径认为是root根目录，向其子文件夹与子文件填充
    return list_dir(r'./app', res)   # 输入路径

if __name__ == '__main__':
    print(json.dumps(get_config_dirs()))
