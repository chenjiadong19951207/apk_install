# _*_ coding:utf-8 _*_
import os
import re
import tkinter as tk
from tkinter import *
from tkinter import ttk, scrolledtext
import threading


class apk_install:
    def __init__(self):
        self.path = r"D:\apks"  # apk包的路径

    def install_and_open(self, device_name, apk_name):
        # 安装游戏
        os.system("adb -s" + device_name + "install -r" + self.path + "\\" + apk_name)
        # 启动游戏的指令 shell  am  start -n   包名/主activity
        # os.system("adb -s" + device_name + "shell am start -n com.****") 包名

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


# 界面ui
class APKTk():
    def __init__(self, apk_install):
        self.root = Tk();
        self.root.geometry('800x300')
        self.root.title("APK安装器")
        self.apk_name = StringVar()
        self.apk_name.set("输入完整包名")
        self.Apk_install = apk_install
        self.select_device_list = []
        self.device_list = self.Apk_install.get_device_list()
        self.cb_list = []
        # self.root.mainloop()

    # 制作多选框
    def mul_check_box(self):
        print("制作多选框", self.device_list)
        for index, item in enumerate(self.device_list):
            self.select_device_list.append(tk.StringVar())
            cb = Checkbutton(self.root, text=item, variable=self.select_device_list[-1], onvalue=item, offvalue='')
            # cb = Checkbutton(self.root,text=item,onvalue=item,offvalue='')
            self.cb_list.append(cb)
            cb.grid(row=index, column=0, sticky='w')
            cb.select()

    # 刷新设备列表
    def refresh_data(self):
        print("刷新设备列表")
        for item in self.cb_list:
            item.grid_remove()
            self.cb_list = []
            self.device_list = self.Apk_install.get_device_list()
            self.select_device_list = []
            self.mul_check_box()

    # 全选设备列表
    def select_all(self):
        for index, item in enumerate(self.device_list):
            self.device_list[index].set(item)

    # 安装按钮
    def install_button(self):
        button_install = Button(self.root, text='安装', command=self.install)
        button_install.grid(row=len(self.device_list) + 1, column=1)

    # 刷新设备列表按钮
    def refresh_button(self):
        button_refresh = Button(self.root, text='刷新', command=self.refresh_data)
        button_refresh.grid(row=len(self.device_list) + 1, column=2)

    def input_text(self):
        entry_log = Entry(self.root, width=65, textvariable=self.apk_name)
        entry_log.grid(row=len(self.device_list)+1,column=0,sticky='w')

    def get_apk_name(self):
        return self.apk_name.get()

    def mainloop(self):
        self.root.mainloop()

    def install(self):
        selected_device_list = [i.get() for i in self.select_device_list if i.get()]
        print(selected_device_list)
        apkName = self.get_apk_name()
        print(apkName)
        for device in selected_device_list:
            threading.Thread(target=self.Apk_install.install_and_open, args=(device, apkName)).start()
            print("启动" + device)


if __name__ == '__main__':
    Apk_install = apk_install()
    # print(device_list)
    apkTk = APKTk(Apk_install)
    apkTk.mul_check_box()
    apkTk.input_text()
    apkTk.install_button()
    apkTk.refresh_button()
    apkTk.root.mainloop()
