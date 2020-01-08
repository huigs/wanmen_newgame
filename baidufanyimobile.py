from urllib import request, parse
import json

def translateBaidu(text):
    content = text
    url = "https://fanyi.baidu.com/basetrans"

    data = {
        "query": content,
        "from": "en",
        "to": "zh",
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36",
    }

    # 数据编码
    data = parse.urlencode(data).encode()

    # response = requests.post(url, data=data, headers=headers)

    req = request.Request(url=url, data=data, headers=headers)

    rsp = request.urlopen(req)

    html = rsp.read().decode()
    print(html)

    js_info = json.loads(html)
    js = json.dumps(js_info, sort_keys=True, indent=4, ensure_ascii=False, separators=(',', ':'))
    print(js)

    # print(data)
    # print(rsp.text)
    # print(rsp.request.url)     #请求地址
    # print(rsp.url)              #响应地址
    # print(rsp.request.headers)  #请求头
    # print(rsp.headers)          #响应头
    # print(rsp.content.decode('unicode - escape'))  # 显示出来unicode的中文
    # print response.text
    # print(rsp.read)

translateBaidu("boy")