#coding:utf-8
"""
破解滑块验证码
"""
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from request.spider.blibli.utils.config import *

class Crack_bb(object):

    def __init__(self):
        self.url = URL
        self.email = EMAIL
        self.password = PASSWORD
        self.brower = webdriver.Chrome()
        self.wait = WebDriverWait(self.brower, 15)

    def __del__(self):
        self.brower.close()
        print(1)
    def crack_login(self):
        print(1)

    def open(self):
        print(1)




if __name__ == '__main__':
    crack = Crack_bb()
    crack.crack_login()