#coding:utf-8
import urllib
import requests
import json
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


def getHtml(url):
	page = urllib.urlopen(url)
	html = page.read()
	return html

def Tuling1(info):
	key = 'a51088c0e7a8450da37aedc84119ad25'
	api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='
	#info = raw_input('手动输入')
	request = api + info
	response = getHtml(request)
	dic_json = json.loads(response)
	print 'Gager: '.decode('utf-8') + dic_json['text'] + dic_json['url'] 
	return str(dic_json['url'])

def get_url(info):
    key = '05ba411481c8cfa61b91124ef7389767'
    api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='
    if len(info) > 2:
        request = api + info
        response = getHtml(request)
        dic_json = json.loads(response)
        print 'Gager: '.decode('utf-8') + dic_json['text'] + dic_json['url']
        str_url = dic_json['url']
        file = open("get_url_result.txt","w+")
        file.write(str_url)
        file.close()
    else:
        print 'input no thing'




def Tuling(words):
    Tuling_API_KEY = "a51088c0e7a8450da37aedc84119ad25"

    body = {"key":Tuling_API_KEY,"info":words.encode("utf-8")}

    urL = "http://www.tuling123.com/openapi/api"
    r = requests.post(urL,data=body,verify=True)
    
    if r:
        #print(r)
        #if json.loads(r.url) != '':
        #    print('url:',json.loads(r.url))   
	date = json.loads(r.text)
        #if urL != '':
        #    print urL["url"]
	#	return urL["url"]
        
	print "Gager:"+date["text"]
        return date["text"]
 
    else:
        return None

#while True:
#    info = raw_input("�?")
#    Tuling1(info)
"""
if __name__ == "__main__":
    #get_url('给我查一下从新化到长沙的火车')
  Tuling(sys.argv[1])
"""
