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
import base64

class Crack_bb(object):

    def __init__(self):
        self.url = URL
        self.email = EMAIL
        self.password = PASSWORD
        self.brower = webdriver.Chrome()
        self.wait = WebDriverWait(self.brower, 15)

    # 登录
    def crack_login(self):
        # 打开登录界面，输入账户和密码
        print('打开登录界面')
        self.open()
        # 点击登录按钮
        print('点击登录按钮')
        button = self.get_slider_show_button()
        button.click()
        # 保存图片
        print('保存滑块图片')
        sleep(3)
        self.get_pic()
        # 无缺口图片
        fullImage = Image.open('full.png')
        # 有缺口图片
        sliceImage = Image.open('slice.png')
        # 偏移量
        print('计算偏移量')
        left = self.get_gap(fullImage, sliceImage)
        print(left)
        # 获取移动轨迹
        print('生成移动轨迹')
        track = self.get_track(left)
        print(track)
        # 获取拖动按钮
        print('获取拖动按钮')
        sliderButton = self.get_act_slider_button()
        # 移动滑块
        print('移动滑块')
        self.move_to_gap(sliderButton, track)


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
        slider_show_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@class,'btn') and contains(@class, 'btn-login')]")))
        return slider_show_button

    # 获取无缺口图片和有缺口图片
    def get_pic(self):
        picName = ['full.png', 'slice.png']
        className = ['geetest_canvas_fullbg', 'geetest_canvas_bg']

        for i in range(len(className)):
            js = "var change = document.getElementsByClassName('"+className[i]+"'); return change[0].toDataURL('image/png');"
            im_info = self.brower.execute_script(js)
            self.save_pic(im_info, picName[i])

    # 解码获取到的图片写入文件，保存图片
    def save_pic(self, data, fileName):
        data = data.split(',')[1]
        data = base64.b64decode(data)
        with open(fileName, 'wb') as f:
            f.write(data)

    # 获取缺口偏移量
    def get_gap(self, fullImage, sliceImage):
        left = 10
        for i in range(left, fullImage.size[0]):
            for j in range(fullImage.size[1]):
                if not self.is_pixel_equal(fullImage, sliceImage, i, j):
                    left = i
                    return left
        return left

    # 判断两个像素点是否相同
    def is_pixel_equal(self, fullImage, sliceImage, x, y):
        pixel_1 = fullImage.load()[x, y]
        pixel_2 = sliceImage.load()[x, y]
        threshold = 40
        if abs(pixel_1[0] - pixel_2[0]) < threshold and abs(pixel_1[1] - pixel_2[1]) < threshold and abs(pixel_1[2] - pixel_2[2]) < threshold:
            return True
        else:
            return False

    # 由偏移量获取移动轨迹
    def get_track(self, distance):
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        distance = distance - 16
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 1
        # 初速度
        v = 0
        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            current += move
            track.append(round(move))
        return track

    # 获取拖动按钮
    def get_act_slider_button(self):
        sliderButton = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='geetest_slider_button']")))
        return sliderButton

    # 模拟拖动碎片
    def move_to_gap(self, sliderButton, track):
        # 点击鼠标右键，不松开
        ActionChains(self.brower).click_and_hold(sliderButton).perform()
        for x in track:
            # 鼠标从当前位置移动到某个坐标
            ActionChains(self.brower).move_by_offset(x, 0).perform()
            sleep(0.5)

        ActionChains(self.brower).release().perform()


if __name__ == '__main__':
    crack = Crack_bb()
    crack.crack_login()