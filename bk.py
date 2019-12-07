#coding:utf-8
import requests
import re
import math
from lxml import etree
from requests.adapters import HTTPAdapter

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))

def makeRequest(url,headers):
    response = requests.get(url, headers=headers)
    # print(response.status_code)
    return response

# 获取地址词典
def getLocations(response_home):
    html = etree.HTML(response_home.text)
    location_li = html.xpath('(//div[@class="city_list_section"])[1]/ul/li')
    dics = {}
    for li in location_li:
        province_divs = li.xpath('.//div[@class="city_province"]')
        for province_div in province_divs:
            province = province_div.xpath('.//div[@class="city_list_tit c_b"]/text()')
            province = province[0].strip('\n').strip()
            province_item_dics = {}
            item_lis = province_div.xpath('.//ul/li')
            for item_li in item_lis:
                item_name = item_li.xpath('.//a/text()')
                item_url = item_li.xpath('.//a/@href')
                province_item_dics[item_name[0]] = 'https:'+item_url[0].replace('.fang.','.').replace('.ke.','.fang.ke.')+'/loupan'
            dics[province] = province_item_dics
    return dics

# 获取新房列表中的url链接
def getListItems(dics, headers):
    # print(dics)
    for province,city_dics in dics.items():
        # print(city_dics)
        for city,url in city_dics.items():
            # print(url)
            now_url = url
            temp_response = makeRequest(now_url, headers)
            temp_html = etree.HTML(temp_response.text)
            # 总数据条数
            total_data = temp_html.xpath('//div[@class="page-box"]/@data-total-count')
            count = int(total_data[0])
            # 总页数
            total_page = math.ceil(float(count)/10)
            flag = True 
            page = 1
            list_url = []
            while flag:
                
                response = makeRequest(now_url, headers)
                print(now_url)
                print(response.status_code)
                if response.status_code != 200:
                    print('状态导致结束')
                    break
                html = etree.HTML(response.text)
                list_urls = html.xpath('//ul[@class="resblock-list-wrapper"]/li/a/@href')
                for temp_url in list_urls:
                    list_url.append(url.replace('/loupan','')+temp_url)
                
                print('当前页码：'+str(page))
                print('总页数：'+str(total_page))
                if page >= total_page:
                    print('结束')
                    break
                page = page+1
                r = now_url.rfind('/pg')
                if r != -1:
                    now_url = now_url[:r]
                # print(r)
                now_url = now_url+'/pg'+str(page)
            # print(list_url)
            dics[province][city] = list_url
        break
    return dics

# 获取下一页列表链接


if __name__ == '__main__':
    # 首页
    url = 'https://www.ke.com/city'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    response_home = makeRequest(url, headers)
    dics = getLocations(response_home)
    shanxi_dics = {'山西':dics['山西']}
    # 最终的urls字典及列表
    shanxi_dics = getListItems(shanxi_dics, headers)
    print(shanxi_dics)