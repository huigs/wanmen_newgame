import requests
import random
import hashlib
import json
import pprint
import time

appid = '12345678'
key  = 'dasd457dawgjj54j01qf'
 
url = 'https://fanyi.baidu.com/pcnewcollection?'
#需要翻译的文本
q = '建设中国特色社会主义'
#原语言
from_language ='zh'
#目的语言
to_language = 'en'
#随机数
salt = random.randint(32768, 65536)
#签名
sign = appid+q+str(salt)+key
sign = sign.encode('utf-8')
sign_new = hashlib.md5(sign).hexdigest()

prefix='https://fanyi.baidu.com/pcnewcollection?req=check&fanyi_src=%E4%B8%AD%E5%9B%BD&direction=zh2en&_='

t = time.time()
nowTime = lambda:int(round(t * 1000))
print (nowTime());              #毫秒级时间戳，基于lambda
#生成URL
#new_url = url + 'q='+q+'&from='+from_language+'&to='+to_language+'&appid='+appid+'&salt='+str(salt)+'&sign='+sign_new
#new_url = 'https://fanyi.baidu.com/pcnewcollection?req=check&fanyi_src=%E4%B8%AD%E5%9B%BD&direction=zh2en&_=1545638156767'
new_url = prefix+str(nowTime())

res = requests.get(new_url)
print(res.text)
#json_data = json.loads(res.text)
#translate_result = json_data["trans_result"]["dst"]
#pprint.pprint(json_data["trans_result"])