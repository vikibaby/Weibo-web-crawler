import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import json
import csv
import pandas


userid = "1723516811" #chenrui

weibo = pandas.read_csv(userid+".csv")
commentsid_list = weibo['id'].values

csvfilename = userid +"_comments.csv"

host = 'm.weibo.cn'
base_url = 'https://%s/api/container/getIndex?' % host
user_agent = 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1 wechatdevtools/0.7.0 MicroMessenger/6.3.9 Language/zh_CN webview/0'

headers = {
    'Host': host,
    'Referer': 'https://m.weibo.cn/u/'+userid,
    'User-Agent': user_agent
}



def get_comments(commentsid,page):
    url = 'http://m.weibo.cn/api/comments/show?id='+str(commentsid)+'&page=' + str(page)
    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('抓取错误', e.args)




# 解析页面返回的json数据
def parse_page(resjson,commentsid):

    items = resjson.get('data').get('data')
    for item in items:

        data = {
            'commentsid':commentsid,
            'id': item.get('id'),
            'created_at': item.get('created_at'),
            'text': pq(item.get("text")).text(),  # 仅提取内容中的文本
            'like_counts':item.get('like_counts'),
            'liked':item.get('liked')
        }
        yield data


if __name__ == '__main__':

    with open(csvfilename, 'w', newline='',encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['commentsid','id', 'created_at','text','like_counts','liked'])
        writer.writeheader()

    for commentsid in commentsid_list:

        for page in range(1,10):  # 抓取前十页的数据

            json = get_comments(commentsid,page)

            if json is not None and json.get('ok') == True:
                results = parse_page(json,commentsid)
                with open(csvfilename, 'a', newline='',encoding='utf-8-sig') as f:
                    writer = csv.DictWriter(f, fieldnames=['commentsid','id', 'created_at','text','like_counts','liked'])
                    writer.writerows(results)
            else:
                print(commentsid,"break at page & json",page,json)
                break

        #data = json.loads((json.dumps(results))
        #with open('result.csv', 'a', newline='',encoding='utf-8-sig') as f:
            #writer = csv.writer(f)
            #writer = csv.DictWriter(f, fieldnames=['id', 'created_at','text'])
            #writer.writeheader()
            #writer.writerows(results)
