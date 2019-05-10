#coding:utf-8
import os
import requests
from http.cookiejar import LWPCookieJar
from http.cookiejar import Cookie
import json
import time
from encrypt import encrypted_request,AES_encrypt



DEFAULT_TIMEOUT = 10
BASE_URL = "http://music.163.com"
conf_path = os.path.join(os.path.expanduser("~"), ".netease-musicbox")
cookie_path = cookie_path = os.path.join(conf_path, "cookie")

header = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "music.163.com",
            "Referer": "http://music.163.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        }

cookie_jar = LWPCookieJar(cookie_path)
#print("加载cookie")
cookie_jar.load()
session = requests.Session()
#print("设置会话")
session.cookies = cookie_jar
for cookie in cookie_jar:
  if cookie.is_expired():
    cookie_jar.clear()
    print("删除cookie")
#print("cooki加载完成")


def raw_request(method, endpoint, data=None):
  #print("进入请求")
  resp = ''
  if method == "GET":
    resp = session.get(
           endpoint, params=data, headers=header, timeout=DEFAULT_TIMEOUT
    )
  elif method == "POST":
    resp = session.post(
            endpoint, data=data, headers=header, timeout=DEFAULT_TIMEOUT
    )
  print(resp.status_code)
  return resp

# 生成Cookie对象
def make_cookie(name, value):
  return Cookie(
            version=0,
            name=name,
            value=value,
            port=None,
            port_specified=False,
            domain="music.163.com",
            domain_specified=True,
            domain_initial_dot=False,
            path="/",
            path_specified=True,
            secure=False,
            expires=None,
            discard=False,
            comment=None,
            comment_url=None,
            rest=None,
  )

def request(method, path, params={}, default={"code": -1}, custom_cookies={}):
  endpoint = "{}{}".format(BASE_URL, path)
  print("请求url:{}".format(endpoint))
  csrf_token = ""
  for cookie in session.cookies:
    if cookie.name == "__csrf":
      csrf_token = cookie.value
      print("csrf_token数据:{}".format(csrf_token))
      break
  params.update({"csrf_token": csrf_token})
  #print("解析前数据:{}".format(params))
  data = default

  for key, value in custom_cookies.items():
    cookie = make_cookie(key, value)
    session.cookies.set_cookie(cookie)

  params = encrypted_request(params)
  #print("params数据:{}".format(params))
  try:
    print("开始请求")
    resp = raw_request(method, endpoint, params)
    print(resp)
    data = resp.json()
    #print("data:{}".format(data['msg'])) 
    #return data
  except requests.exceptions.RequestException as e:
    print("请求失败:{}".format(e))
  except ValueError as e:
    #log.error("Path: {}, response: {}".format(path, resp.text[:200]))
    print("error:{}".format(e))
  finally:
    #print("请求出现错误")
    return data

def login(username, password):
  #print("准备从本地加载cookie")
  session.cookies.load()
  #print("加载完成")
  path = ''
  params = {}
  if username.isdigit():
    print("使用手机号登陆")
    path = "/weapi/login/cellphone"
    params = dict(phone=username, password=password, rememberLogin="true")
  else:
    # magic token for login
    # see https://github.com/Binaryify/NeteaseCloudMusicApi/blob/master/router/login.js#L15
    print("使用邮箱登陆")
    client_token = (
        "1_jVUMqWEPke0/1/Vu56xCmJpo5vP1grjn_SOVVDzOc78w8OKLVZ2JH7IfkjSXqgfmh"
    )
    path = "/weapi/login"
    params = dict(
         username=username,
         password=password,
         rememberLogin="true",
         clientToken=client_token,
    )
  #print("开始请求")
  data = request("POST", path, params)
  session.cookies.save()
  #print(data)
  return data


song_dict = {}
song_author = {}

# 每日推荐歌曲
def recommend_playlist(total=True, offset=0, limit=20):
  global song_dict 
  global song_author
  path = "/weapi/v1/discovery/recommend/songs"  # NOQA
  params = dict(total=total, offset=offset, limit=limit, csrf_token="")
  result = request("POST", path, params).get("recommend", [])
  song_list = []
  #song_dict = {}
  song_author = {}
  #print(result[0]['artists'][0]['name'])
  for i in range(30):
    song_dict[result[i]['id']] = result[i]['name'].encode('utf-8')
    song_author[result[i]['id']] = result[i]['artists'][0]['name'].encode('utf-8')
    #print(result[i]['name'])
    song_list.append(result[i]['id'])
  #for key,value in song_dict.items():
  #  print("[Name]>>>{0}\t [ID]>>>{1}".format(key,value))
  #print(song_author)
  return song_list



# 搜索单曲(1)，歌手(100)，专辑(10)，歌单(1000)，用户(1002) *(type)*
def search(keywords, stype=1, offset=0, total="true", limit=50):
  path = "/weapi/search/get"
  params = dict(s=keywords, type=stype, offset=offset, total=total, limit=limit)
  result = request("POST", path, params).get("result", {})
  find_list = []
  for i in range(19):
    find_list.append(result['songs'][i]['id'])
    #print result['songs'][i]['artists'][0]['id']
  print(find_list)
  return find_list

#通过音频id获取MP3文件url
def Display_song_url(id):
  url = 'https://music.163.com/weapi/song/enhance/player/url?csrf_token='
  iv = "0102030405060708"
  first_key = "0CoJUm6Qyw8W8jud"
  first_Param = "{\"ids\":\"["+str(id)+"]\",\"br\":128000,\"csrf_token\":\"\"}"
  second_key = 16 * 'F'
  h_encText = AES_encrypt(first_Param, first_key, iv)
  h_encText = AES_encrypt(h_encText, second_key, iv)
  encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
  data = {"params":h_encText,"encSecKey": encSecKey}
  response = session.post(url, headers=header, data=data)
  json_dict = response.json()
  #print(json_dict['data'][0]['url'])
  return json_dict['data'][0]['url']


# 用户歌单
def user_playlist(uid, offset=0, limit=50):
  path = "/weapi/user/playlist"
  params = dict(uid=uid, offset=offset, limit=limit, csrf_token="")
  return request("POST", path, params).get("playlist", [])


# 新碟上架
def new_albums(offset=0, limit=50):
  path = "/weapi/album/new"
  params = dict(area="ALL", offset=offset, total=True, limit=limit)
  return request("POST", path, params).get("albums", [])

# 歌单（网友精选碟） hot||new http://music.163.com/#/discover/playlist/
def top_playlists(category="全部", order="hot", offset=0, limit=50):
  path = "/weapi/playlist/list"
  params = dict(
       cat=category, order=order, offset=offset, total="true", limit=limit
  )
  return request("POST", path, params).get("playlists", [])

 # 热门歌手 http://music.163.com/#/discover/artist/
 def top_artists(offset=0, limit=100):
   path = "/weapi/artist/top"
   params = dict(offset=offset, total=True, limit=limit)
   return request("POST", path, params).get("artists", [])

# 热门单曲 http://music.163.com/discover/toplist?id=
def top_songlist(idx=0, offset=0, limit=100):
  playlist_id = TOP_LIST_ALL[idx][1]
  return playlist_detail(playlist_id)

# 歌手单曲
def artists(artist_id):
  path = "/weapi/v1/artist/{}".format(artist_id)
  return request("POST", path).get("hotSongs", [])

#下载mp3音频文件
def Down_from_url():
  global song_dict 
  global song_author
  list_id = recommend_playlist(total=True, offset=0, limit=20)
  url_list = []
  count = 0
  print("[INFO]>>> 开始下载音频文件")
  for list in list_id:
    url = Display_song_url(list)
    with open("music/{0}_{1}.mp3".format(song_author[list],song_dict[list]),'wb') as f:
      req = session.get(url)
      f.write(req.content)
      print("[INFO]>>> 第{}个音频文件下载完成".format(count))
    count += 1
  print("[INFO]>>> 所以文件下载完成")

#Down_from_url()

#recommend_playlist(total=True, offset=0, limit=20)
#login('13739000242','asdoyj774254007')
#list_1 = search("飞云之上", stype=1, offset=0, total="true", limit=50)
