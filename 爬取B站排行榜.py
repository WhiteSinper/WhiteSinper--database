import requests
import re
from requests.exceptions import RequestException
import json


def get_all_page(url):
    try:
        headers = {
             'User-Agent':'www.Mozilla/5 .0 (Macintosh; Intel Mac 05 X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('<li.*?<div\sclass="img"><a href="//(.*?)"\starget.*?lazy-image.*?title">(.*?)</a>.*?b-icon\splay"></i>(.*?)</span>.*?b-icon\sview"></i>(.*?)</span>.*?b-icon\sauthor"></i>(.*?)</span>.*?pts.*?<div>(.*?)</div>综合得分.*?</li>', re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield{
            'CoverPath':item[0],
            'Title':item[1],
            'ViewCount':item[2].strip(),
            'ShareCount':item[3].strip(),
            'UpId':item[4].strip(),
            'Score':item[5]
        }

def getSql(dbpath,table_name,list):

    createsql(dbpath,table_name)

    for item in list:
        sql = '''
            insert into %s values ('%s','%s','%s','%s','%s','%s','%s','%s')
        '''%(table_name,item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7])

        intosql(dbpath,sql)

    print("已经获得数据保存到sql数据库")

def intosql(dbpath,sql):

    conn = sqlite3.connect(dbpath)

    c = conn.cursor()

    try:
        c.execute(sql)

        conn.commit()
    except Exception:
        print("执行sql语句失败")
    finally:
        conn.close()
    print("已经执行sql语句！")

def createsql(dbpath,table_name):
    list_id = ['list','name','id','location','number','barrage','maker','mark']
    sql = '''
        create table %s(
            %s varchar ,
            %s varchar,
            %s varchar,
            %s varchar,
            %s varchar ,
            %s varchar,
            %s varchar,
            %s varchar 
        )
    '''%(table_name,list_id[0],list_id[1],list_id[2],list_id[3],list_id[4],list_id[5],list_id[6],list_id[7])
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    try:
        c.execute(sql)
        conn.commit()
    except Exception:
        print("执行sql语句失败")
    finally:
        conn.close()
    print("已经创建指定数据库，添加表头！")



def main():
    url = 'https://www.bilibili.com/v/popular/rank/'
    urlpaths=('all','guochuang','douga','music','dance',
             'game','technology','digital','life','food','kichiku','fashion','ent','cinephile','origin','rookie')
    for urlpath in urlpaths:
        upath = url + urlpath
        html = get_all_page(upath)
        for item in parse_one_page(html):
            with open(urlpath+'.txt','a',encoding='utf-8') as f:
                print(item)
                f.write(json.dumps(item,ensure_ascii=False) +'\n')
main()

