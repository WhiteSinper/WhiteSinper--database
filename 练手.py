import requests
def getHTMLText(url):
    try:
        Header = {'user-agent':'Mozilla/5.0'}
        r = requests.get(url,headers = Header,timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"


if __name__== "__main__":
    url = "http://baidu.com"
    print(getHTMLText(url))