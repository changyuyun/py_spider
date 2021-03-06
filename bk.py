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

# 获取详情页数据并存储到文件中
def getInfoAndSave(dics,headers):
    for province,city_dics in dics.items():
        for city,url_list in city_dics.items():
        	# 写入文件
            fileName = province+'-'+city+'-bk.txt'
            for url in url_list:
                response = makeRequest(url,headers)
                html = etree.HTML(response.text)
                project_name_list = html.xpath('//h2[@class="DATA-PROJECT-NAME"]/text()') # 项目名称列表
                price_list = html.xpath('(//div[@class="price"])[1]/span[@class="price-number"]/text()') #项目单价列表
                address_list = html.xpath('(//div[@class="middle-info animation"])[1]/ul/li/span[@class="content"]/text()') # 项目地址列表
                project_name = ''
                price = ''
                address = ''
                if len(project_name_list) > 0:
                    project_name = project_name_list[0].strip()

                if len(price_list) > 0:
                    price = price_list[0].strip()

                if len(address_list) > 0:
                    address = address_list[0].strip()
                content = "项目名称："+project_name+"\t项目地址："+address+"\t单价："+price+"\n"
                print(content)
                f = open(fileName, 'a')
                f.write(content.encode("gbk",'ignore').decode("gbk", "ignore"))
                f.close()


def testA(headers):
    url = 'https://yuncheng.fang.ke.com/loupan/p_xghybkcuj/'
    response = makeRequest(url,headers)
    html = etree.HTML(response.text)
    project_name_list = html.xpath('//h2[@class="DATA-PROJECT-NAME"]/text()') # 项目名称列表
    price_list = html.xpath('(//div[@class="price"])[1]/span[@class="price-number"]/text()') #项目单价列表
    address_list = html.xpath('(//div[@class="middle-info animation"])[1]/ul/li/span[@class="content"]/text()') # 项目地址列表
    project_name = ''
    price = ''
    address = ''
    if len(project_name_list) > 0:
        project_name = project_name_list[0].strip()

    if len(price_list) > 0:
        price = price_list[0].strip()

    if len(address_list) > 0:
        address = address_list[0].strip()
    print(project_name)
    print(price)
    print(address)
    content = "项目名称："+project_name+"\t项目地址："+address+"\t单价："+price+"\n"


if __name__ == '__main__':
    # 首页
    url = 'https://www.ke.com/city'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    # testA(headers)
    response_home = makeRequest(url, headers)
    dics = getLocations(response_home)
    # 爬取山西房源
    shanxi_dics = {'山西':dics['山西']} # 假定只爬取山西
    # 最终的urls字典及列表
    shanxi_dics = getListItems(shanxi_dics, headers)
    # print(shanxi_dics)
    getInfoAndSave(shanxi_dics,headers)