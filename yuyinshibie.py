#coding:utf-8
import os
import sys 
import time
import json 
import urllib2 
import base64 
import requests
reload(sys) 
sys.setdefaultencoding("utf-8")

def get_access_token(): 
  url = "https://openapi.baidu.com/oauth/2.0/token" 
  body = { 
	"grant_type":"client_credentials", 
	"client_id":"Ll0c53MSac6GBOtpg22ZSGAU", 
	"client_secret":"44c8af396038a24e34936227d4a19dc2", 
  }

  r = requests.post(url,data=body,verify=True)
  respond = json.loads(r.text)
  return respond["access_token"]

def yuyinshibie_api(audio_data,token): 
  speech_data = base64.b64encode(audio_data).decode("utf-8") 
  speech_length = len(audio_data) 
  post_data = { 
	"format" : "pcm", 
	"rate" : "16000", 
	"channel" : "1", 
	"cuid" : "B8-27-EB-BA-24-14", 
	"token" : token, 
	"speech" : speech_data, 
	"len" : speech_length 
  }

  url = "http://vop.baidu.com/server_api"
  json_data = json.dumps(post_data).encode("utf-8")
  json_length = len(json_data)
  #print(json_data)

  req = urllib2.Request(url, data=json_data)
  req.add_header("Content-Type", "application/json")
  req.add_header("Content-Length", json_length)

  print("asr start request\n")
  resp = urllib2.urlopen(req)
  print("asr finish request\n")
  resp = resp.read()
  resp_data = json.loads(resp.decode("utf-8"))
  #print(resp_data)
  if resp_data["err_no"] == 0:
    return resp_data["result"]
  else:
    print(resp_data)
    return 'error'

def data_com(func):
  def wrap(*args,**kwargs):
    if(os.path.exists("test.wav")):
      #time.sleep(2)
      #os.system("mplayer test.wav")
      #os.system("ffmpeg -y  -i sound.wav  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 16k.pcm")
      os.system("ffmpeg -y  -i test.wav  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 16k.pcm")
      #token =  get_access_token()
      os.system("rm test.wav")
      msg = func(*args,**kwargs)
      os.system("rm 16k.pcm")
      return msg
  return wrap

@data_com
def asr_main(filename,tok): 
  try: 
    f = open(filename, "rb") 
    audio_data = f.read() 
    f.close() 
    resp = yuyinshibie_api(audio_data,tok) 
    #os.system('rm ' + filename)
    print("数据:{0}  类型:{1}".format(resp[0],type(resp[0])))
    if resp != 'error':
      if resp[0] != '':
        result = str(resp[0].encode("utf-8")).replace('。','')
        print(result)
        return result
    else:
      return '识别error'
  except Exception as e: 	
    print ("e:{}".format(e))
    #return "识别失败".encode("utf-8")
    return "识别error"

def Asr_main(filename,tok):
  try:
    #os.system("mplayer test.wav")
    os.system("ffmpeg -y  -i "+filename+"  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 16k.pcm")
    f = open("16k.pcm", "rb")
    audio_data = f.read()
    f.close()
    resp = yuyinshibie_api(audio_data,tok)
    os.system('rm ' + filename)
    print("数据:{0}  类型:{1}".format(resp[0],type(resp[0])))
    if resp != 'error':
      if resp[0] != '':
        result = str(resp[0].encode("utf-8")).replace('。','')
        print(result)
        return result
    #os.system("rm test.wav 16k.pcm")
    else:
      return '识别error'
  except Exception as e:
    print ("e:{}".format(e))
    #return "识别失败".encode("utf-8")
    return "识别error"

"""
if __name__ == "__main__":
  token = get_access_token()
  while True:
    if(os.path.exists("test.wav")):
      time.sleep(5)
      result = Asr_main("test.wav",token)
      print(result)
"""
"""!
class ShiBie():

    def __init__(self,filename):
        self.filename = filename

    def get_access_token(self,):
        #用于获取百度openapi的token api接口
        url = "https://openapi.baidu.com/oauth/2.0/token"
        #数据体
        body = {
                "grant_type":"client_credentials",
                "client_id":"Ll0c53MSac6GBOtpg22ZSGAU",
                "client_secret":"44c8af396038a24e34936227d4a19dc2",
        }
        #采用post方式访问网页
        r = requests.post(url,data=body,verify=True)
        #获取响应数据
        respond = json.loads(r.text)
        #以字典方式得到token
        return respond["access_token"]

    def get_response_data(self,audio_data):
        #根据第一个方法得到token
        token = self.get_access_token()
        #把音频数据编码成base64格式然后解码成utf-8格式
        speech_data = base64.b64encode(audio_data).decode("utf-8")
        #求取音频数据大小
        speech_length = len(audio_data)
        #数据字典
        post_data = {
                    "format" : "wav",
                    "rate" : 16000,
                    "channel" : 1,
                    "cuid" : "B8-27-EB-BA-24-14",
                    "token" : token,
                    "speech" : speech_data,
                    "len" : speech_length
        }
        #语音识别api接口
        url = "http://vop.baidu.com/server_api"
        #把数据以json格式存储并以utf-8格式编码
        json_data = json.dumps(post_data).encode("utf-8")
        #求大小
        json_length = len(json_data)
        #以post方式请求
        req = urllib2.Request(url, data=json_data)
        #添加http头部信息，获取响应
        req.add_header("Content-Type", "application/json")
        req.add_header("Content-Length", json_length)
        resp = urllib2.urlopen(req)
        resp = resp.read()
        #以json方式加载得到的数据
        resp_data = json.loads(resp.decode("utf-8"))
        if resp_data["err_no"] == 0:
            return resp_data["result"]
        else:
            print(resp_data)
        return None

    def asr_main(self,):
        try:
            f = open(self.filename, "rb")
            audio_data = f.read()
            f.close()
            resp = self.get_response_data(audio_data)
            os.system('rm voice.wav')
            return resp[0]
        except Exception,e:
            print "e:",e
            return "识别失败".encode("utf-8")   
"""
