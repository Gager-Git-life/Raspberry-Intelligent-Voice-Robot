#coding:utf-8
import socket
import sys
import os
import wave
import numpy as np


host = "192.168.2.23"
port = 6543

# 创建 socket 对象
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
# 绑定端口号
serversocket.bind((host, port))
# 设置最大连接数，超过后排队
serversocket.listen(3)
print("[*]>>> 本地ip:{0}  监听端口:{1}".format(host,port))
print("[*]>>> TCP 服务器正在监听中 。。。")


file = wave.open("test.wav",'rb')
params=file.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]
clientsocket,addr = serversocket.accept()
print("链接地址:{}".format(addr))

strData = file.readframes(1024)
while strData != '':
  clientsocket.sendall(strData)
  os.system("echo -n '.' ")
  strData = file.readframes(1024)
print("\n文件:{}传输完成".format("test.wav"))
clientsocket.close()
