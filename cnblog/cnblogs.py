# -*- coding:utf-8 -*-

"""
使用urllib库爬取博客园文章
"""
import json
from urllib import request, error, parse
from colorama import init, Fore
from pyquery import PyQuery as pq
from tqdm import tqdm
import time
from utils import str2dict


# 获取文章信息
def get_data(url, page):
    # if page == 0:
        # 生成请求对象
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    request_obj = request.Request(url=url, data=None, headers=headers)

    # else:
    #     headerss = '''
    #     accept: text/plain, */*; q=0.01
    #     accept-encoding: gzip, deflate, br
    #     accept-language: zh-CN,zh;q=0.9
    #     cache-control: no-cache
    #     content-length: 140
    #     content-type: application/json; charset=UTF-8
    #     origin: https://www.cnblogs.com
    #     pragma: no-cache
    #     referer: https://www.cnblogs.com/
    #     sec-fetch-mode: cors
    #     sec-fetch-site: same-origin
    #     user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36
    #     x-requested-with: XMLHttpRequest
    #     content-type: application/json
    #     '''
    #     headers = str2dict(headerss)
    #     headers = {
    #         'content-type':'application/json'
    #     }
    #     payload = {
    #         "CategoryId": 808,
    #         "CategoryType": "SiteHome",
    #         "ItemListActionName": "AggSitePostList",
    #         "PageIndex": 2,
    #         "ParentCategoryId": 0,
    #         "TotalPostCount": 4000
    #     }
    #     # print(json.dumps(payload)) 字典转json
    #     # return True
    #     params = bytes(parse.urlencode(payload).encode(encoding='UTF8'))
    #     print(params)
    #     return True
    #     data = bytes(parse.urlencode(payload), encoding='utf-8')
    #     request_obj = request.Request(url=url, data=params, headers=headers, method="POST")
    response = request.urlopen(request_obj)
    if response.status == 200:
       return response
    else:
       return None


# 解析数据
def parse_data(response):
    # print(response)
    html = response.read().decode('utf-8')
    doc = pq(html)
    divs = doc('.post_item').items()
    # 最终存储的数据
    data = []
    for div in divs:
        temp_data = {}
        temp_data['title'] = div.find('.titlelnk').text()
        temp_data['url'] = div.find('.titlelnk').attr('href')
        temp_data['short'] = div.find('.post_item_summary').text()
        temp_data['author'] = div.find('.post_item_foot .lightblue').text()
        temp_data['author_page_url'] = div.find('.post_item_foot .lightblue').attr('href')
        temp_data['create_time'] = div.find('.post_item_foot').text().split()[2] +' '+ div.find('.post_item_foot').text().split()[3]
        temp_data['comment_counts'] = div.find('.article_comment .gray').text()
        temp_data['read_counts'] = div.find('.article_view .gray').text()

        data.append(temp_data)
    return data

def main(url, page = 0):
    """
    主函数
    :param url: 访问链接
    :param page: 页码
    :return None
    """
    response = get_data(url, page)
    data = parse_data(response)
    print(data)

if __name__ == '__main__':
    print(Fore.RED+ 'start')
    url = 'https://www.cnblogs.com/'
    main(url, 0)
    # for i in tqdm(range(10), desc='抓取进度', ncols = 100):
    #     if i == 0:
    #         url = 'https://www.cnblogs.com/'
    #         main(url, 0)
    #     else:
    #         url = 'https://www.cnblogs.com/AggSite/AggSitePostList'
    #         # url = 'https://www.cnblogs.com/mvc/AggSite/PostList.aspx'
    #         main(url, i+1)


    # main(url, '')
    print(Fore.RED+'end')