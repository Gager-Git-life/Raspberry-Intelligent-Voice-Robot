#coding:utf-8
import wave
import socket
import sys
import os
import time
import numpy as np
import threading
import Turling as TL
import yuyinshibie as yysb
import yuyinhecheng as yyhc
import youdaofy as fy
from random import choice
from multiprocessing import Pool
#from wangyiyun import Down_from_url

udp_port_flg = False
file_flg = False
clean_flg = True
first_flg = True
end_flg = False
# 获取本地主机名
#host = socket.gethostname()
host = "192.168.43.96"
wav_host = '192.168.43.58'
port = 6543
wav_port = 23
udp_port = ' '

wavcount = 0
channels = 1
sampwidth = 2
framerate = 44100


def TCP_Get_Port():
  global udp_port_flg,udp_port
  print("[*]>>> 本地ip:{0}  监听端口:{1}".format(host,port))
  print("[*]>>> TCP 服务器正在监听中 。。。")
  while(not udp_port_flg):
    # 建立客户端连接
    clientsocket,addr = serversocket.accept()      
    print("[*]>>> 连接地址: %s" % str(addr))
    # 接收小于 1024 字节的数据
    udp_port = clientsocket.recv(1024)
    print(udp_port)
    #time.sleep(0.01)
    if(udp_port.strip() != ''):
      udp_port_flg = True
  print("[*]>>> udp 链接端口为:{0} 类型为:{1}".format(udp_port,type(udp_port)))
  #serversocket.send("port received".encode())
  serversocket.close()


# 创建 socket 对象
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#serversocket.setblocking(False)   
# 将socket设置为非阻塞. 在创建socket对象后就进行该操作.
serversocket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
# 绑定端口号
serversocket.bind((host, port))
# 设置最大连接数，超过后排队
serversocket.listen(6)
print("[*]>>> 本地ip:{0}  监听端口:{1}".format(host,port))
print("[*]>>> TCP 服务器正在监听中 。。。")


def TCP_Send_File(filename):
  clientsocket,addr = serversocket.accept()
  """
  wav_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  wav_socket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
  wav_socket.bind((host, wav_port))
  wav_socket.listen(2)
  print("[INFO]>>> 等待wav客服端连接")
  """
  print("链接地址:{}".format(addr))
  with open(filename,'rb') as f:
    while(True):
      msg = f.read(1024)
      if(msg):
        clientsocket.sendall(msg)
      else:
        break
  print("文件:{}传输完成".format(filename))
  clientsocket.close()

def TCP_Send_Wav(filename,host,port):
  
  wav_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  #wav_socket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
  wav_socket.connect((host, port))
  #wav_socket.listen(2)
  
  print("begin")
  #打开一个声音文件，，返回一个声音的实例
  file = wave.open(filename,"rb") 
  #获取wav文件的参数（以tuple形式输出），依次为(声道数，采样精度，采样率，帧数，......)
  params=file.getparams()
  nchannels, sampwidth, framerate, nframes = params[:4]
  print("当前文件:{0},采样率:{1},通道数:{2}".format(filename,framerate,nchannels))
  #clientsocket,addr = wav_socket.accept()
  #print("链接地址:{}".format(addr))
  data = file.readframes(4096)
  while data != '':
    wav_socket.sendall(data)
    data = file.readframes(4096)
    os.system("echo -n '.' ")
  print("\n文件:{}传输完成".format(filename))
  wav_socket.close()

def TCP_Recv_Wav(clientsocket,modes,filename):
  global file_flg,wavcount
  if(os.path.exists(filename)):
    os.system("rm " + filename)
  os.system("rm *.wav")
  if(modes == '0'):
    file = open(filename,'wb')
  else:
    file = wave.open(filename,"wb")
    file.setnchannels(channels)
    file.setsampwidth(sampwidth)
    file.setframerate(framerate)

  #clientsocket.settimeout(0.5) #设置超时间
  print("[INFO]>>> 准备接受wav数据:")
  while(1):
    try: 
      #clientsocket.settimeout(10)#设置超时间
      msg = clientsocket.recv(1024)
      wavcount += 1
      if msg == '':
        print("\n[INFO]>>> 接收到结束字符")
        break
        #pass
      elif(modes == '0'):
        file.write(msg)
        os.system("echo -n '.' ")
      else:
        file.writeframes(msg)
        if(wavcount%10 == 0):
          os.system("echo -n '.' ")
          #msg = ' '
    except Exception:
      print("\n[INFO]>>> 终止传输")
      break
  file.close()
  clientsocket.close()
  print("\n[INFO]>>> wav数据传输完成.")
  os.system("mplayer " + filename)
  Wav_com(filename)

def TCP_Tra(filename,modes):
  count = 0
  while(True):
    # 建立客户端连接
    clientsocket,addr = serversocket.accept()
    count += 1
    clientsocket.settimeout(0.1)
    print("\n[*]>>> 第[{}]个连接者,地址为:{}".format(count,str(addr)))
    print("[*]>>> 设置完成等待数据 。。。")
    """
       接收小于 1024 字节的数据
       socket.recv(),是一个阻塞型功能函数，在没有接收到任何数据的情况下是会一直等待，你发送空字符实际上就是没有发送字符。
    """
    filenames = "{}.wav".format(count)
    if(count >1):
      TCP_Recv_Wav(clientsocket,modes,filename)
    else:
      t1 = threading.Thread(target = TCP_Recv_Wav, args = (clientsocket,modes,filenames))
      t1.setDaemon(True)
      t1.start()
    #TCP_Recv_Wav(clientsocket,modes,filename)

def UDP_Bagin(port):
  global end_flg
  udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  udpsocket.bind((host,port))
  while(True):
    data, addr = udpsocket.recvfrom(1024)
    if data == '1234':
       end_flg = True

def UDP_File_Tra():
  global udp_port
  udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  udpsocket.bind((host,int(udp_port)))
  if(os.path.exists("sound.wav")):
    os.system("echo "" > sound.wav")
  file = open("sound.wav",'w')
  print("[*]>>> udp 设置完成等待数据 。。。")
  count = 0
  while True:
    data, addr = udpsocket.recvfrom(1024)
    if not data:
      break
    else:
      file.write(data)
      data = ''
      #count += 1
      #if(count/100 == 0):
      #  print ".",
      #time.sleep(0.001)
  file.close()
  udpsocket.close()
  print("[*]>>> 文件传输完成!")


"""
channels:通道 sampwidth:采样比特位数
framerate:采样频率 wave_data:写入数据流
"""

def Generate_Wav_Write(channels,sampwidth,framerate,wave_data):
  f = wave.open(filename,"wb")
  f.setnchannels(channels)
  f.setsampwidth(sampwidth)
  f.setframerate(framerate)
  f.writeframes(wave_data.tostring())
  f.close()


def play_wav():
  if(len(sys.argv) == 3):
    FindPath = sys.argv[1]
    FileNames = os.listdir(FindPath)
    Filename = choice(FileNames)
    print("音频源文件:{}".format(Filename))
    if(os.path.exists("test.wav")):
      os.remove("test.wav")
    Filename = sys.argv[1]+"'{}'".format(Filename)
    os.system("ffmpeg -i " + Filename  + " -acodec pcm_u8 -ar "+sys.argv[2]+" -ac 1 test.wav")
  TCP_Send_Wav("test.wav",wav_host,wav_port)



def Wav_com(filename,token=yysb.get_access_token()):
  commd = yysb.Asr_main(filename,token)
  #return commd
  if(commd != '' and '音乐' in commd):
    #os.system("python /home/python_test/wangyiyun/wangyiyun.py 推荐")
    song_date_path = time.strftime('%Y.%m.%d/',time.localtime(time.time()))
    if('推荐' in commd):
      if(not os.path.exists('/home/music/{}'.format(song_date_path))):
        os.system("python /home/python_test/wangyiyun/wangyiyun.py 推荐")
      FileNames = os.listdir('/home/music/{}'.format(song_date_path))
    else:
      FileNames = os.listdir('/home/music/')
    for i in range(len(FileNames)):
      Filename = choice(FileNames)
      while(os.path.splitext(Filename)[1] != '.mp3'):
        Filename = choice(FileNames)
      print(Filename)
      if('推荐' in commd):
        music_path = "/home/music/{0}'{1}'".format(song_date_path ,Filename)
      else:
        music_path = "/home/music/'{}'".format(Filename)
    #os.system("mplayer /home/music/'{}'".format(Filename))
    #TCP_Send_Wav("/home/music/'{}'".format(Filename))
    #play_wav()
      os.system("ffmpeg -i " + music_path  + " -acodec pcm_u8 -ar 48000 -ac 1 test.wav")
      TCP_Send_Wav("test.wav",wav_host,wav_port)
  elif(commd == "识别error"):
    yyhc.tts_main("数据传输失败了,请重启",token)
    TCP_Send_Wav("test.wav",wav_host,wav_port)
  elif("翻译" in commd):
    if(commd[0] == "把" or commd[0] == '吧'):
      commd = commd[3:]
    txt = commd.split("翻译成")[0]
    targ = commd.split("翻译成")[1]
    result = fy.connect('中文',targ,txt)
    print("从:{0} 翻译成:{1} 结果为:{2}".format("中文",targ,result))
    #print("翻译对象:" + fy.lan_dict[zh_lan(targ)])
    fy.DW_Mp3('test.mp3',fy.lan_dict[fy.zh_lan(targ)], result)
    if(os.path.exists("test.wav")):
      os.remove("test.wav")
    os.system("ffmpeg -i test.mp3 -acodec pcm_u8 -ar 48000 -ac 1 test.wav")
    #yyhc.tts_main(result,token)
    TCP_Send_Wav("test.wav",wav_host,wav_port)
  elif('关闭' in commd):
    os.system("python killprocess.py mplayer")
    TCP_Send_Wav("test.wav",wav_host,wav_port)
  else:
    #print("error")
    words = TL.Tuling(commd)
    yyhc.tts_main(words,token)
    TCP_Send_Wav("test.wav",wav_host,wav_port)


if __name__ == "__main__":
  """
  if(sys.argv[1] == '0'):
    TCP_Tra("test.wav",sys.argv[2])
  elif(sys.argv[1] == '1'):
    TCP_Send_File("test.wav")
  else:
    play_wav()
    #TCP_Send_Wav("test.wav")
  """
  #po=Pool(2) #定义⼀个进程池，最⼤进程数3
  #po.apply_async(TCP_Tra,("test.wav",'1'))
  #po.apply_async(wav_count)
  #po.close() #关闭进程池，关闭后po不再接收新的请求
  #po.join() 
  TCP_Tra("test.wav",'1')
  #play_wav()
