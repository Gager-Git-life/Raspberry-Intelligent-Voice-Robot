#coding:utf-8
import os
import sys 
import urllib2 
import json 
import os
import time 
import yuyinshibie
import requests
#from yuyinshibie import ShiBie

tok = yuyinshibie.get_access_token()
#import yuyinshibie
reload(sys) 
sys.setdefaultencoding("utf-8")

"""
#语音合成api文档地址:http://ai.baidu.com/docs#/TTS-API/top
#yuyinhecheng_api()用于合成语音url
#tts_main()使用mpg123播放语音
"""
#tok = yuyinshibie.get_access_token()

def yuyinhecheng_api(tok,tex): 
	cuid = "7519663" 
	spd = "4" 
	url = "http://tsn.baidu.com/text2audio?tex="+str(tex)+"&lan=zh&cuid=7519663&ctp=1&tok="+tok+"&per=4" 
	return url

def tts_main(words,tok): 
  voice_url = yuyinhecheng_api(tok,words)
  r = requests.get(voice_url)
  with open("get_wav.mp3",'wb') as f:
    #os.system('mpg123 "%s"'%voice_url)
    f.write(r.content)
  time.sleep(0.5)
  if(os.path.exists("test.wav")):
    os.system("rm test.wav")
  os.system("ffmpeg -i get_wav.mp3 -acodec pcm_u8 -ar 48000 -ac 1 test.wav")
  os.system("rm get_wav.mp3")
#tts_main(sys.argv[1],tok)

"""!
class HeCheng():

    def __init__(self,):
        self.spd = spd
        self.text = text
        self.token = ShiBie()

    def get_request_url(self,):
        url = "http://tsn.baidu.com/text2audio?tex=" +str(self.text)+"&lan=zh&cuid=7519663&ctp=1&tok="+str(self.token.get_access_token())+"&per=" + str(self.spd)

    def tts_main(self,):
        voice_url = self.get_request_url()
        os.system('mpg123 "%s"'%voice_url)
        time.sleep(0.5)

"""
"""不使用
def tx_tts_main():
        tex = ''
        tok = yuyinshibie.get_access_token()
        if len(sys.argv) == 2:
            tex = sys.argv[1]
        else:
            tex = '你有一个提醒'
        voice_url = yuyinhecheng_api(tok,tex)
        os.system('mpg123 "%s"'%voice_url)
        time.sleep(0.5)

if __name__== "__main__":
    word = str(sys.argv[1])
    tts_main(word,tok)
"""
