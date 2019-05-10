#coding:utf-8
import os
import sys
import uuid
import requests
import hashlib
import time
import json
#import youdaocei

reload(sys)
sys.setdefaultencoding('utf-8')

YOUDAO_URL = 'http://openapi.youdao.com/api'
APP_KEY = '0799d0ffd0bd3449'
APP_SECRET = 'bplIfXRWEXekCmhhe4R5JUrJHXGHLEOn'

lan_dict = {"zh-CHS":"zh","en":"en","ja":"jp","ko":"kor","fr":"fra","es":"spa",
            "pt":"pt","ru":"ru"}
"""
zh-lan_dict = {u"中文":"zh-CHS",u"英语":"en",u"日语":"ja",u"韩语":"ko",
               u"法语":"fr",u"西班牙语":"es",u"俄语":"ru"}
"""
lan_list = ["中文","英语","日语","韩语","法语","西班牙语","俄语"]
zh_lan_list = ["zh-CHS","en","ja","ko","fr","es","ru"]

def zh_lan(zh_txt):
  for i in range(7):
    if zh_txt == lan_list[i]:
      #print(lan_list[i]+zh_lan_list[i])
      return zh_lan_list[i]

langua = ''
text = ''

def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr)
    return hash_algorithm.hexdigest()


#对输入字符串长度进行处理
def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def connect(sour_lan,targ_lan,txt):
  #global langua,text
  """
  print(
           中文:zh-CHS  英文:en     日文:ja
           韩文:ko      法文:fr     西班牙文:es
           葡萄牙文:pt  俄文:ru     越南文:vi
           德文:de      阿拉伯文:ar 印尼文:id
        )
  """
  """
  print("翻译格式:from|to|str 如:zh-CHS|en|你好")
  q = raw_input("输入:")
  quit = ['q','Q']
  if(q in quit):
    sys.exit()
  #print(q)
  msg = txt.split('|')
  print(msg)
  if(len(msg) != 3):
    print("输入格式错误,重试")
    return  
  """
  data = {}
  data['from'] = zh_lan(sour_lan)
  #print(data['from'])
  data['to'] = zh_lan(targ_lan)
  #print(data['to'])
  #langua = data['to']
  data['signType'] = 'v3'
  curtime = str(int(time.time()))
  data['curtime'] = curtime
  salt = str(uuid.uuid1())
  signStr = APP_KEY + truncate(txt.encode('utf-8')) + salt + curtime + APP_SECRET
  sign = encrypt(signStr)
  data['appKey'] = APP_KEY
  data['q'] = txt
  data['salt'] = salt
  data['sign'] = sign

  response = do_request(data)
  #print response.text
  target = json.loads(response.text.decode("utf-8"))
  result = ''
  print(target)
  #if(data['to'].lower() == 'en'):
  #  result = target["web"][0]['value'][0]
  
  result = target['translation'][0]
  print("翻译结果:{}".format(result))
  #text = result
  #print(text)
  return result

def DW_Mp3(filename,lan,text):
  url = "https://fanyi.baidu.com/gettts?lan=" + lan + "&text=" + text + "&spd=3&source=web"
  print("url："+ url)
  dw_r = requests.get(url)
  if dw_r.status_code == 200:
    print("请求正确正在开始下载文件...")
    with open(filename,"wb") as f:
      f.write(dw_r.content)
    print("音频文件下载完成")
    return 1
  else:
    print("请求出现错误,下载失败")
    return 0

#zh_lan("中文")

#connect("中文","俄语","你好")

"""
if __name__ == '__main__':
  while(True):
    connect()
    if(text != ''):
      if(os.path.exists("*.wav") or os.path.exists("*.mp3")):
        os.system("rm *.wav *.mp3")
      DW_Mp3('test.mp3',lan_dict[langua], text)
      if(os.path.exists('test.mp3')):
        os.system("mplayer test.mp3")
        #os.system("ffmpeg -i test.mp3 -f wav test.wav")
"""
