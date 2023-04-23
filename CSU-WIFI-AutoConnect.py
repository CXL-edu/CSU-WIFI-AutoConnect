"""
author: 陈晓龙
date: 2023-04-20
description: 用于自动连接CSU校园网的脚本
"""
import time
import winreg
import requests
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys


class auto_wifi():
    def __init__(self, wifi_name: str, url: str, username: str, password: str):
        self.wifi_name = wifi_name
        self.url = url
        self.username = username
        self.password = password

        # Open the Internet Settings registry key
        self.internet_settings = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                           r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                                           0, winreg.KEY_ALL_ACCESS)

    def disable_proxy(self, times=5):
        # Check if the proxy is enabled
        if winreg.QueryValueEx(self.internet_settings, 'ProxyEnable'):
            # Disable the proxy
            winreg.SetValueEx(self.internet_settings, 'ProxyEnable', 0, winreg.REG_DWORD, 0)
            time.sleep(times)

    def enable_proxy(self):
        winreg.SetValueEx(self.internet_settings, 'ProxyEnable', 0, winreg.REG_DWORD, 1)  # Enable the proxy
        # winreg.CloseKey(self.internet_settings) # Close the registry key

    def check_internet(self):
        # Check the response status code
        self.disable_proxy()
        try:
            response = requests.get('https://www.baidu.com/', timeout=60)
            if response.status_code == 200:
                print('已连接网络，可正常上网')
                self.enable_proxy()
                time.sleep(60)
                return True   # The current WiFi can connect to the internet.
        except:
            return False

    def check_wifi(self):
        return self.wifi_name.encode() in subprocess.check_output("netsh wlan show interfaces")

    def connect_wifi(self):
        subprocess.check_output(f"netsh wlan connect name={self.wifi_name}")
        print(f'成功连接到{self.wifi_name}')

    def login(self):
        service = Service(r'msedgedriver.exe')      # 创建一个Service对象
        options = webdriver.EdgeOptions()           # 创建一个EdgeOptions对象，并设置一些选项
        options.add_argument('--start-maximized')   # 最大化运行（全屏窗口）,不设置，取元素会报错
        options.service = service
        driver = webdriver.Edge(options=options)    # 使用Chrome浏览器

        driver.get(self.url)
        time.sleep(1)
        try:
            elem = driver.find_element(By.XPATH, '//*[@id="login-box"]/div/div[3]/div[1]/div/form/input[2]')
            elem.send_keys(self.username)
            elem = driver.find_element(By.XPATH, '//*[@id="login-box"]/div/div[3]/div[1]/div/form/input[3]')
            elem.send_keys(self.password)
            elem = driver.find_element(By.XPATH, '//*[@id="login-box"]/div/div[3]/div[1]/div/form/input[1]')
            elem.send_keys(Keys.RETURN)
            print(f'成功登录上{self.wifi_name}')
        except Exception as e:
            print(f'已登录上{self.wifi_name}，无需重复登录')

        # driver.quit()


# 主程序
if __name__ == "__main__":
    wifi_name = "CSU-WIFI" # "Redmi K40 Pro+"
    url = "https://portal.csu.edu.cn/"  # 校园网登录网址
    username = "214711105"  # 校园网账户
    password = "cxl124572"  # 校园网密码
    auto_wifi = auto_wifi(wifi_name, url, username, password)

    print('https://github.com/CXL-edu/CSU-WIFI-AutoConnect.git\n'
          '本脚本用于自动连接中南大学校园网，由于网络不稳定\n'
          '为防止远程服务器掉线导致不能远程控制，写下此脚本\n\n'
          '***************************************\n\n'
          '该脚本实现如下功能:\n'
          '1、自动判断是否联网（绕过代理）\n'
          '2、自动连接CSU-WIFI\n'
          '3、自动登录214711105账号和其密码\n\n'
          '***************************************\n\n'
          'Note：\n'
          '单个账号最多支持3个设备，使用自己的账号密码请修改py文件\n'
          '请将该脚本的exe文件按鼠标右键生成快捷方式并放置到启动路径下\n'
          '==============================================\n')

    while True:
        print('请保持该脚本在远端服务器运行，以保证网络连接')
        try:
            if not auto_wifi.check_internet():
                print('网络不可上网，正在尝试关闭代理，并重连CSU-WiFi进行登录')
                # auto_wifi.check_wifi()
                auto_wifi.connect_wifi()
                # time.sleep(10)
                auto_wifi.login()
        except Exception as e:
            print(e)
        time.sleep(10)

