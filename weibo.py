import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import json
import csv


#userid = "1723516811" #chenrui
userid = "2093001685" #9bish page(80,280)
host = 'm.weibo.cn'
base_url = 'https://%s/api/container/getIndex?' % host
user_agent = 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1 wechatdevtools/0.7.0 MicroMessenger/6.3.9 Language/zh_CN webview/0'

headers = {
    'Host': host,
    'Referer': 'https://m.weibo.cn/u/'+userid,
    'User-Agent': user_agent
}

csvfilename = userid+".csv"


def get_single_page(page):
    params = {
        'type': 'uid',
        'value': int(userid),
        'containerid': int("107603"+userid),
        'page': page
    }
    url = base_url + urlencode(params)
    #print(url)

    try:
        response = requests.get(url, headers=headers)
        #response2 = requests.get(url, headers=comments)

        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('抓取错误', e.args)


# 解析页面返回的json数据
def parse_page(json):
    items = json.get('data').get('cards')
    for item in items:
        item = item.get('mblog')
        if item:
            data = {
                'id': item.get('id'),
                'created_at': item.get('created_at'),
                'text': pq(item.get("text")).text()  # 仅提取内容中的文本
            }
            yield data


if __name__ == '__main__':
    with open(csvfilename, 'w', newline='',encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'created_at','text'])
        writer.writeheader()

    for page in range(253,300):  # 抓取前十页的数据
        json = get_single_page(page)
        if json is not None and json.get('ok') == True:
            results = parse_page(json)

            with open(csvfilename, 'a', newline='',encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'created_at','text'])
                writer.writerows(results)
        else:
            print("break at page & json",page,json)
            break
