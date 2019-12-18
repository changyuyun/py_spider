import requests
from lxml import etree
from requests.adapters import HTTPAdapter

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))


def makeRequest(url, headers):
    response = requests.get(url, headers)
    return response

def main(url):
    headers = {
        'user - agent': 'Mozilla/5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 79.0.3945.79 Safari / 537.36'
    }
    rs = makeRequest(url, headers)
    html = etree.HTML(rs.text)
    types = html.xpath('//div[@class="suf-list J_suffixList"]/ul/text()')
    print(rs.text)

if __name__ == '__main__':
    url = 'https://wanwang.aliyun.com/domain/searchresult#/?keyword=&suffix=com'
    main(url)
