#coding:utf-8
import requests
import re
from lxml import etree
from requests.adapters import HTTPAdapter

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))
# 房天下
# for item in locations[:]:
# 	if item == "\xa0":
# 		locations.remove(item)


# 获取列表页跳转详情页的链接
# 
def getInfoUrls(url):
    
    # 组装新房链接
    list_url = []
    new_url = url.replace('.fang','.newhouse.fang')+'/house/s' #新房url
    flag = True 
    while flag:
        print(new_url)
        new_r = requests.get(new_url,headers=headers)
        status_code = new_r.status_code #状态码
        charset = new_r.encoding
        print(status_code)
        print(charset)
        # 执行响应码等于200的地址
        if status_code == 200:
            list_html = etree.HTML(new_r.text)
            list_items = list_html.xpath('//div[@class="nl_con clearfix"]/ul/li')

            for list_item in list_items:
                itme_url = list_item.xpath('.//div[@class="nlc_img"]/a/@href')
                if len(itme_url) > 0:
                    list_url.append(itme_url[0].replace('//','/').replace('/?','?').strip('/'))

            # 下一页
            pattern = re.compile(r'<a class="next"  href="(.*?)">下一页</a>')
            next_page_url = pattern.findall(new_r.content.decode("gbk"))
            print(next_page_url)
            if len(next_page_url) == 0:
                break
            new_url = url.replace('.fang','.newhouse.fang')+next_page_url[0]
            # print(new_url)

    return list_url
# 详情页数据获取
def getInfoItems(info_urls, province, city):
    for info_url in info_urls:
        new_info_url = 'http://'+info_url.replace('http://','').replace('https://','') # 拼成正确的url
        print(new_info_url)
        info_r = requests.get(new_info_url, headers=headers)
        info_r.encoding = "gbk" # 转码
        info_html = etree.HTML(info_r.text)
        title = ''
        price = ''
        address = ''
        # 第一种方案
        title_1ist_1 = info_html.xpath('//h1[@class="lp-name"]/span/text()')
        price_list_1 = info_html.xpath('//div[@class="l-price"]/strong/text()')
        address_list_1 = info_html.xpath('//span[@style="width:301px;"]/@title')
        print(address_list_1)
        # 第二种方案
        title_list_2 = info_html.xpath('//div[@class="tit"]/h1/strong/text()')
        price_list_2 = info_html.xpath('//span[@class="prib cn_ff"]/text()')
        address_list_2 = info_html.xpath('//div[@id="xfptxq_B04_12"]/span/@title')

        #第三种方案 处理楼盘地址
        address_list_3 = info_html.xpath('//span[@style="width:300px;"]/i/@title')
        print(address_list_2)
        if len(title_1ist_1) > 0:
            title = title_1ist_1[0]

        if len(title_list_2) > 0:
            title = title_list_2[0]

        if len(price_list_1) > 0:
            price = price_list_1[0]
        if len(price_list_2) > 0:
            price = price_list_2[0]

        if len(address_list_1) > 0:
            address = address_list_1[0]
        if len(address_list_2) > 0:
            address = address_list_2[0]
        if len(address_list_3) > 0:
            address = address_list_3[0]
        res_str = "项目名称："+title+"\t项目地址："+address+"\t售价："+price+"\tURL："+new_info_url+"\n"
        print(res_str)
        # 写入文件
        fileName = province+'-'+city+'-ftx.txt'
        f = open(fileName, 'a+')
        f.write(res_str)
        f.close()

# 组装省份数据
# 
def getLoactions(html):
    dics = {}
    # 获取按省份选取得所有tr的id 进行分组
    tr_ids = html.xpath('//div[@id="c02"]/table[@class="table01"]/tr/@id')
    new_tr_ids = [] # 不重复的tr id 列表
    # return tr_ids
    for ids in tr_ids:
        if ids not in new_tr_ids:
            new_tr_ids.append(ids)
    # return new_tr_ids
    for id in new_tr_ids: # 循环分组id 循环内的都属于一组
        group_tr = html.xpath('//div[@id="c02"]/table[@class="table01"]/tr[@id="'+id+'"]') # 按分组id获取行
        group_name = '' # 分组名称
        group_item = {}
        for tr in group_tr:
            temp_name_list = tr.xpath('.//strong/text()')
            # print(temp_name_list)
            if len(temp_name_list) > 0:
                if temp_name_list[0] != '\xa0':
                    if group_name == '':
                        group_name = temp_name_list[0]
                    
            # print(group_name)
            item_names = tr.xpath('.//a/text()')
            item_urls = tr.xpath('.//a/@href')
            # print(item_names)
            # print(item_urls)
            for i,item in enumerate(item_names):
                # print(item)
                group_item[item] = item_urls[i]
        # return group_item
        if group_name != '其它':
            if group_name == '山西':
                dics[group_name] = group_item
    return dics

# 执行体
if __name__ == '__main__':
    url = "https://www.fang.com/SoufunFamily.htm?ctm=1.bj.xf_search.head.29"

    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    try:
        r = requests.get(url,headers=headers)

        html = etree.HTML(r.text)
    
        locations = getLoactions(html)

        for key_type,value in locations.items():
            print(key_type+'--------start')
            for k_type,v in value.items():
                info_urls = getInfoUrls(v)
                getInfoItems(info_urls,key_type,k_type)
            print(key_type+'--------end'+"\n")
            break
    except Exception as e:
        print("其他错误："+str(e))
    
