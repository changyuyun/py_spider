#coding:utf-8
"""
破解滑块验证码
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from request.spider.blibli.utils.config import *
from time import sleep
from io import BytesIO
from PIL import Image

class Crack_bb(object):

    def __init__(self):
        self.url = URL
        self.email = EMAIL
        self.password = PASSWORD
        self.brower = webdriver.Chrome()
        self.wait = WebDriverWait(self.brower, 15)

    def __del__(self):
        # self.brower.close()
        print(1)
    # 登录
    def crack_login(self):
        # 打开登录界面，输入账户和密码
        self.open()
        # 点击登录按钮
        button = self.get_slider_show_button()
        button.click()


    # 打开登录界面
    def open(self):
        # 访问登录界面
        self.brower.get(self.url)
        # 邮箱
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
        # 密码
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))
        # 输入邮箱
        username.clear()
        username.send_keys(self.email)
        # 输入密码
        password.clear()
        password.send_keys(self.password)
        sleep(3)

    def get_slider_show_button(self):
        slider = self.wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@class,'btn') and contains(@class, 'btn-login')]")))
        return slider

if __name__ == '__main__':
    crack = Crack_bb()
    crack.crack_login()