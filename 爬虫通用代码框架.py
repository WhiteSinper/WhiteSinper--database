import requests
def getHTMLText(url):
    try:
        r = requests.get(url,timeout = 30)
        r.raise_for_status()
        #如果状态码不是200，则为HTTPErroor异常
        #注意r.raise_for_status和r.status_code的区别。前者是在内部判断，不需要额外增加if语句
        #利于使用try-except进行异常处理
        r.encoding = r.apparent_encoding
        #将猜测的编码方式改为根据网页内容分析出来的编码方式，从而有效避免乱码
        return r.text
    except:
        return "产生异常"



if __name__ == "__main__":
    url = "http://baidu.com"
    print(getHTMLText(url))
