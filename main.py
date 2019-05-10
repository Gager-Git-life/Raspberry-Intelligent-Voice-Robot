#coding:utf-8
from yuyinshibie import main
from file_re import TCP_Tra
import file_re 


if __name__ == "__main__":
  while(True):
    TCP_Tra()
    print("[*]>>> 开始识别。。。。。")
    if(file_re.file_flg):
      main()
      file_re.clean_flg = True
      file_re.file_flg = False
      file_re.first_flg = True
