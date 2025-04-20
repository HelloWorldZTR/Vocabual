"""
随机二次元壁纸
"""

import os
import time
import random
import requests

from PyQt5.QtGui import QPixmap

def __getAppRoot():
    """
    获取当前应用的根目录
    @return: str
    """
    return os.path.dirname(os.path.abspath(__file__)).replace('utils', '')

def getTodayWallpaper():
    """
    获取一张壁纸，每天固定一张
    @return: QPixmap | None
    """
    today = time.strftime('%Y-%m-%d')
    wallpaper_path = os.path.join(__getAppRoot(), 'wallpapers')
    if not os.path.exists(wallpaper_path):
        os.makedirs(wallpaper_path)
    wallpaper_file = os.path.join(wallpaper_path, f'{today}.jpg')

    # 清理之前的旧壁纸
    for file in os.listdir(wallpaper_path):
        if file.endswith('.jpg') or file.endswith('.png') and file != f'{today}.jpg':
            os.remove(os.path.join(wallpaper_path, file))

    # 如果今天已经有壁纸了，就不再下载了
    if os.path.exists(wallpaper_file):
        return QPixmap(wallpaper_file)
    else: # 下载壁纸
        url = 'https://tc.alcy.cc'
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(wallpaper_file, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return QPixmap(os.path.join(wallpaper_path, f'{today}.jpg'))
        else:
            return None




    
