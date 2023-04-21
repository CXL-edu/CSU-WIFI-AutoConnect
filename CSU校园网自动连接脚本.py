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

    @staticmethod
    def check_internet():
        # Check the response status code
        try:
            response = requests.get('https://www.baidu.com/', timeout=30)
            print('response.status_code:', response.status_code)
            return response.status_code == 200  # The current WiFi can connect to the internet.
        except:
            return False

    def check_wifi(self):
        return self.wifi_name.encode() in subprocess.check_output("netsh wlan show interfaces")

    def connect_wifi(self):
        subprocess.check_output(f"netsh wlan connect name={self.wifi_name}")

    def disable_proxy(self):
        # Check if the proxy is enabled
        if winreg.QueryValueEx(self.internet_settings, 'ProxyEnable'):
            # Disable the proxy
            winreg.SetValueEx(self.internet_settings, 'ProxyEnable', 0, winreg.REG_DWORD, 0)

    def login(self):
        # 创建一个Service对象
        service = Service(r'msedgedriver.exe')
        # 创建一个EdgeOptions对象，并设置一些选项
        options = webdriver.EdgeOptions()
        options.add_argument('--start-maximized')  # 最大化运行（全屏窗口）,不设置，取元素会报错
        options.service = service
        driver = webdriver.Edge(options=options)  # 使用Chrome浏览器

        driver.get(self.url)
        time.sleep(1)
        try:
            elem = driver.find_element(By.XPATH, '//*[@id="login-box"]/div/div[3]/div[1]/div/form/input[2]')
            elem.send_keys(self.username)
            elem = driver.find_element(By.XPATH, '//*[@id="login-box"]/div/div[3]/div[1]/div/form/input[3]')
            elem.send_keys(self.password)
            elem = driver.find_element(By.XPATH, '//*[@id="login-box"]/div/div[3]/div[1]/div/form/input[1]')
            elem.send_keys(Keys.RETURN)
            time.sleep(5)
        except:
            # 如果已经连接，则跳出
            pass

        winreg.SetValueEx(self.internet_settings, 'ProxyEnable', 0, winreg.REG_DWORD, 1) # Enable the proxy
        # winreg.CloseKey(self.internet_settings) # Close the registry key
        # driver.quit()


# 主程序
if __name__ == "__main__":
    wifi_name = "CSU-WIFI" # "Redmi K40 Pro+"
    url = "https://portal.csu.edu.cn/"  # 校园网登录网址
    username = "账户"  # 校园网账户
    password = "密码"  # 校园网密码
    auto_wifi = auto_wifi(wifi_name, url, username, password)

    while True:
        try:
            if not auto_wifi.check_internet():
                # auto_wifi.check_wifi()
                auto_wifi.disable_proxy()
                auto_wifi.connect_wifi()
                # time.sleep(10)
                auto_wifi.login()
        except Exception as e:
            print(e)
        time.sleep(60)

