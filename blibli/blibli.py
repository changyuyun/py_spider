#coding:utf-8
from utils.config import *
from selenium import webdriver

class Crack_bb(object):
    def __init__(self):
        self.url = URL
        self.email = EMAIL
        self.password = PASSWORD
        self.brower = webdriver.chrome
    def __del__(self):
        # self.brower.close()
        print(1)
    def crack_login(self):
        print(1)
    def open(self):
        print(1)




if __name__ == '__main__':
    crack = Crack_bb()
    crack.crack_login()