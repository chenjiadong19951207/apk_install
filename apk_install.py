# _*_ coding:utf-8 _*_
import os
import re
import tkinter as tk
from tkinter import *
from tkinter import ttk,scrolledtext
import threading

class apk_isntall:
    def __init__(self):
        self.path = r'D:\apks'  # apk包的路径

    def install_and_open(self,device_name,apk_name):
        # 安装游戏
        os.system("adb -s"+ device_name +"install -r" +self.path+"\\"+apk_name)
        # 启动游戏的指令 shell  am  start -n   包名/主activity
        # os.system("adb -s" + device_name + "shell am start -n com.") 包名

    def get_device_list(self):
        os.system("adb devices")
        res = os.popen("adb devices").readlines()
        device_list = [re.sub.split('\t')[0] for re.sub in res[1:-1]]  # 正则根据回车切割
        return device_list

    def get_apk_list(self):
        list_name = []
        for file in os.listdir(self.path):
            list_name.append(file)
        return list_name

#界面ui
class APKTk():
