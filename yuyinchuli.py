#coding:utf-8
import os
import re
import time
import Camera
import string
import Turling
import Luyin
import yuyinhecheng
import yuyinshibie
import killprocess
import RPi.GPIO as GPIO
import zhongwen_zhuan
from random import choice
from wechart.wechartAPI import wechart_self_msg
tok = yuyinshibie.get_access_token()

song_list = []

def LED(pin, on_off):
    LED = pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED,GPIO.OUT)
    if on_off == 1:
        GPIO.output(LED,GPIO.HIGH)
    else:
        GPIO.output(LED,GPIO.LOW)
     

def songer_song(songer):
    global song_list
    Songer = '"*' + songer    
    Songer = Songer + '*"'
    os.system("touch song.txt")
    os.system("find /home/树莓派语音/music/ -name "+Songer+" > song.txt")
    for line_info in open("song.txt"):
        if ('.mp3' not in line_info):
            if ('.m4a' not in line_info):
                continue
        if line_info in song_list:
            continue
        song_list.append(line_info)
        os.system("mplayer "+line_info)
    if(len(song_list) < 1):
        print("播放失败")
    else:
        print("歌曲播放完成完毕")

def suiji_song(num):
    global song_list
    for i in range(1,num+1):
        FindPath = '/home/树莓派语音/music'
        FileNames = os.listdir(FindPath)
        info = choice(FileNames)
        if '.mp3' not in info:
                continue
        if info in song_list:
                continue
        song_list.append(info)
        print("当前歌曲为:" + info)
        #song_list.append(info)
        info1 = "mplayer /home/树莓派语音/music/" + info
        os.system(info1)

def lianxu_song():
    os.system("ls /home/树莓派语音/music > /home/树莓派语音/music/music.lst")
    os.system("mplayer -playlist /home/树莓派语音/music/music.lst") 

def zhuanhuan(info):
    num = []
    output = 0
    zifu = ['一','二','三','四','五','六','七','八','九','十']
    for m in zifu:
        if m in info:
            m = zhongwen_zhuan.zhuan_shuzi(m,output)
            num.append(m)
    print(num)
    return num

def delect_zifu(info):
    if '&' in info:
        info.replace('&', '_')
    if ' ' in info:
        info.replace(' ', '_')
    if '，' in info:
        info.replace('，', '')
    if '-' in info:
        info.replace('-', '_')
    if '너' in info:
        info.replace('너','_')
    return info

def naozhong(info):
    song = ' '
    e = 0
    b = info.find('为')
    c = info[b:].replace('为', '')
    d = c.find('点')
    t1 = c[:d]
    t2 = c[d+1:e]

    if c.find('音') != -1:
        e = c.find('音')
        song = c[e+2:] + '.mp3'
    else:  
        os.system("ls /home/树莓派语音/music")
        song = raw_input("请选择:")
    str = t2+ ' ' + t1 + ' * * * mplayer /home/树莓派语音2/Music/' + song + '\n'
    os.system('touch cron1.cron')
    file = open('cron1.cron','w+')
    file.write(str)
    file.close()
    str = 'crontab cron1.cron > ~/log \n'
    os.system(str)
    os.system('rm cron1.cron')

def email(info):
    flg = False
    num = ''
    #Name = info.split('给')[1]
    #Name = info[info.find('给')+1:].encode("utf-8")
    Name = info  
    print Name
    #print(type(Name))
    email_dic = {'陈杰':'451651191','胡勇':'1635256194','邹星':'550301631','刘洋':'1747712696','陈宝华':'731404855','自己':'774254007',
                 '文惠':'1834037639'}
    flg = email_dic.has_key(Name)
    #print flg
    if flg:
        num =  email_dic.get(Name)
    else:
        Name = raw_input("请手动输入收件人qq:")
        num = str(Name)
    os.system('cp email_sendmsg_mod.txt msg.txt')
    os.system('nano msg.txt')
    if num.strip()=='':
        print("您没有这个收件人")
    else:
        os.system('python email_fs.py ' + num)
def Tixing(info,flag):
    tex = '*'
    info1 = '*'
    #info1 = info.split('提醒')[0]
    #tex = info.split('提醒')[1]
    if flag == 'T':
        info1 = info.split('提醒')[0]
        tex = info.split('提醒')[1]
        tex = "是时候" + info.split('我')[1] + "了"
    else:
        info1 = info
        tex = flag
    os.system("touch time.txt")
    os.system("date > time.txt")
    file = open("time.txt","r+")
    date = file.read()
    file.close()
    yue = date[date.find('年')+4:date.find('月')].encode("utf-8")
    print("月:" + yue )
    ri = date[date.find('月')+4:date.find('日')].encode("utf-8")
    print("日:" + ri)
    #os.system("rm time.txt")
    #对月进行处理
    pro_yue = '*'
    yue1 = ' '
    yue_flag = 0
    if '月' in info1:
        yue_flag = 1
        pro_yue = info[:info1.find('月')]
        if '每' in pro_yue:
            yue1 = '*'
        elif '下' in pro_yue:
            yue1 = str(int(yue) + 1)
        elif '下下' in pro_yue:
            yue1 = str(int(yue) + 2)
        elif '这个' in pro_yue or '本' in pro_yue:
            yue1 = yue
        elif zhongwen_zhuan.info_in_E(pro_yue):
           yue1 =  zhongwen_zhuan.zhuan_huan(pro_yue, yue1)
            
    #对日进行处理
    pro_ri = '*'
    ri1 = '0'
    ri_flag = 0
    time_ri = ['每天','今天','明天','后天','大后天']
    if ('号' in info1) or ('日' in info1):
        ri_flag = 1
        if yue_flag == 1:
            #print(str(info))
            pro_ri = info[info.find('月')+1:info.find('号')].encode("utf-8")  
            #ri1 = ri.encode('gbk')    
            print(pro_ri, type(pro_ri))
            if zhongwen_zhuan.info_in_E(pro_ri):
               ri1 = zhongwen_zhuan.zhuan_huan(pro_ri, ri1)
            else:
               ri1 = ri
        else:
            if '号' in info1:
                pro_ri = info1[:info1.find('号')]
            elif '日' in info1:
                pro_ri = info1[:info1.find('日')]
            if zhongwen_zhuan.info_in_E(pro_ri):
                ri1 = zhongwen_zhuan.zhuan_huan(pro_ri, ri1)
            else:
                ri1 = ri
    
    else:
        for i in time_ri:
            if i in info1:
                if(time_ri.index(i) == 0):
                    ri_flag = 2
                else:
                    ri_flag = 1
                    t = 0
                    t = int(ri) + int(time_ri.index(i)) - 1
                    shi1 = zhongwen_zhuan.Str(t)
        if(ri_flag == 2):
            yue1 = '*'
            ri1 = '*'  
    #对时进行处理
    pro_shi = '*'
    shi1 = ' '
    shi_flag = 0
    if '早上' in info1 or '上午' in info1:
        shi_flag = 1
        if '早上' in info1:
            pro_shi = info1[info1.find('上')+1:info1.find('点')].encode("utf-8")
        elif '上午' in info1:
            pro_shi = info1[info1.find('午')+1:info1.find('点')].encode("utf-8")
        print("时:" + pro_shi)
        if zhongwen_zhuan.info_in_E(pro_shi):
            shi1 = zhongwen_zhuan.zhuan_huan(pro_shi , shi1)
            print("L_时:" + shi1)
        else:
            print("时间错误-shi")
            shi1 = '8'
    elif '下午' in info1 or '晚上' in info1:
        shi_flag = 2
        if('下午' in info1):
            pro_shi = info1[info1.find('午')+1:info1.find('点')].encode("utf-8")
        elif '晚上' in info1:
            pro_shi = info1[info1.find('上')+1:info1.find('点')].encode("utf-8")
        if zhongwen_zhuan.info_in_E(pro_shi):
            t = 0
            t = zhongwen_zhuan.zhuan_shuzi(pro_shi , t) + 12
            shi1 = zhongwen_zhuan.Str(t)
            print("L_时:" + shi1)
        else:
            print("时间错误-shi")
  
    #对分进行处理
    pro_fen = '0'
    fen1 = '0'
    if '整' in info1:
        fen1 = '00'
    elif '半' in info1:
        fen1 = '30'
    else:
        if('分' in info1):
            pro_fen = info1[info1.find('点')+1:info1.find('分')]
        else:
            pro_fen = info1[info1.find('点')+1:]
            if pro_fen is None:
                fen1 = '00'
        if zhongwen_zhuan.info_in_E(pro_fen):
            fen1 = zhongwen_zhuan.zhuan_huan(pro_fen,fen1)
            if len(fen1) == 1:
                fen1 = '0' + fen1
        else:
            fen1 = '00' 
    
    #合成指令:20 8 * * * mplayer /home/树莓派语音2/Music/AfterTheAfterparty.mp3
    #url = "http://tsn.baidu.com/text2audio?tex="+tex+"&lan=zh&cuid=7519663&ctp=1&tok="+tok+"&per=4"
    #com = fen+ " " +shi+ " " +ri+ " " +yue + " * mpg123 " +url+ "\n"
    #com = fen+ " " +shi+ " " +ri+ " " +yue + " * mplayer /home/树莓派语音2/提醒音.wav" + '\n' 
    #com = "echo " + str(com) + " >> tixing.txt"
    if not yue_flag:
        yue1 = '*'
    if not ri_flag:
        ri1 = '*'
    com = "***"
    if flag == 'T':
        com = fen1 + " " + shi1 + " " + ri1 + " " + yue1 + " * python /home/树莓派语音2/Tx.py " +tex + "\n"
        print "我的提醒:",com
    else:
        com = fen1 + " " + shi1 + " " + ri1 + " " + yue1 + " * " + tex + "\n"
    os.system('touch tixing.txt')
    file = open('tixing.txt','w+')
    file.write(com)
    file.close()
 
    os.system("crontab -l >> tixing.txt")
    str = 'crontab tixing.txt > ~/log \n'
    os.system(str)
    os.system('rm tixing.txt')

def data_pro(info):
    data = ''
    yue = ''
    ri = ''
    list1 = ['今天', '明天' , '后天', '大后天']
    list2 = ['这个月','下个月','下下个月']
    for l1 in list1:
        if l1 in info:
            data = l1
            break
    yue = info[:info.find('月')]
    
#12306火车票语音录入处理
def tickets_msg_pro(info):
    date = info
    Time = ''
    place = ''
    first_station = ''
    last_station = ''
    os.system("touch time.txt")
    os.system("date > time.txt")
    file = open('time.txt','r+')
    time = file.read()
    file.close()
    print("date:" + time)
    nian = time[:time.find('年')].encode("utf-8")
    print("年:" + nian)
    yue = time[time.find('年')+4:time.find('月')].encode("utf-8")
    print("月:" + yue)    
    ri = time[time.find('月')+4:time.find('日')].encode("utf-8")
    print("日:" + ri)
    ri1 = 0
    yue1 = 0
    time_ri = ['今天','明天','后天','大后天']
    time_yue = ['这个','下个']
    if '的车票' in info:
        place = info[info.find('从')+1:info.find('的车')]
    else:
        place = info[info.find('从')+1:info.find('的火')]
    print(place)
    first_station = place[:place.find('到')]
    print("起始站:" + first_station)
    last_station = place[place.find('到')+1:]
    print("到达站:" + last_station)
    Time = info[:info.find('从')]
    print("时间信息:" + Time)    
    if '月' in info and '号' in info:
        Time_yue = Time[:Time.find('月')]
        Time_ri = Time[Time.find('月')+1:Time.find('号')]
        print("解析出的月和日:" + Time_yue + '-' + Time_ri)
        #print(yue)
        #如果是数字字符表示
        if zhongwen_zhuan.info_in_U(Time_yue) or zhongwen_zhuan.info_in_E(Time_yue) or (Time_yue in time_yue):
            #print('mark')
            #把号解析出来
            #ri = Time[Time.find('月')+1:Time.find('号')].encode("utf-8")
            #print(ri)
            #字符转数字
            if (zhongwen_zhuan.info_in_U(Time_ri) or zhongwen_zhuan.info_in_E(Time_ri)):
                #print("解析出的日:" + ri1)
                RI = zhongwen_zhuan.zhuan_shuzi(Time_ri,ri1)
                ri1 = RI 
                print("解析出的日:" + str(ri1))
            else:
                date = raw_input("手动输入日期(号):")
                RI = zhongwen_zhuan.zhuan_shuzi(date,ri1)
                ri1 = RI
            if Time_yue in time_yue:
                yue1 = int(yue) + int(time_yue.index(Time_yue))
            else:
                YUE = zhongwen_zhuan.zhuan_shuzi(Time_yue,yue1)
                yue1 = YUE
        
        elif (zhongwen_zhuan.info_in_U(Time_ri) or zhongwen_zhuan.info_in_E(Time_ri)):
            date = raw_input("手动输入日期(月):")
            YUE = zhongwen_zhuan.zhuan_shuzi(date,yue1)
            yue1 = YUE 
            RI = zhongwen_zhuan.zhuan_shuzi(Time_ri,ri1)
            ri1 = RI
        
        else:
            Data = raw_input("手动输入日期(月-日):")
            yue = Data[:Data.find("-")]
            ri = Data[Data.find("-")+1:]
            yue1 = int(yue)
            ri1 = int(ri)
            """!
            if zhongwen_zhuan.info_in_E(yue) == 1:
                zhongwen_zhuan.zhuan_shuzi(yue,yue1)
            if zhongwen_zhuan.info_in_U(ri) == 1:
                ri = info[:info.find('号')].encode("utf-8")
            elif zhongwen_zhuan.info_in_E(ri) == 1:
                ri = zhongwen_zhuan.zhuan_huan(ri,ri1)

            ri = zhongwen_zhuan.zhuan_shuzi(ri,ri1)
            yue = time[time.find('年')+4:time.find('月')].encode("utf-8") 
            yue = zhongwen_zhuan.zhuan_shuzi(yue,yue1)   
            for i in time_L2:
                if i in Time:
                    if '这个月' in info or '本月' in info:
                        pass
                    elif '下个' in info:
                        yue += 1
                    else:
                        yuyinhecheng.tts_main('请输入有效的日期',tok)
            """
    elif '号' in info:
        data = Time[:Time.find('号')]
        if zhongwen_zhuan.info_in_U(data) or zhongwen_zhuan.info_in_E(data):
            RI = zhongwen_zhuan.zhuan_shuzi(data,ri1) 
            ri1 = RI
            yue1 = int(yue)
        else:
            Data = raw_input("请输入有效日期(月-日):")
            yue = Data[:Data.find('-')]
            ri = Data[Data.find('-')+1:]
            yue1 = int(yue)
            ri1 = int(ri)
  
    else:
        if Time in time_ri:
            Data = time_ri.index(Time)
            ri1 = int(ri) + int(Data)
            yue1 = int(yue)
    print("确认的月:" + str(type(yue1)) + str(yue1))
    print("确认的日:" + str(type(ri1)) + str(ri1))  
    if len(str(ri1)) == 1:
        ri1  = '0' + str(ri1)
    if len(str(yue1)) == 1:
        yue1 = '0' + str(yue1)          
    msg = str(first_station) + ' ' + str(last_station)+ ' ' + str(nian)+'-'+str(yue1)+'-'+str(ri1)
    print(msg)
    return msg

def wechat_Send_Pro(info):
    msg = info.split('发送')[1]
    time = info.split('发送')[0]
    print("时间:%s  主体:%s" %(time,msg))
    head = "python wechart/wechartAPI.py "
    cmd = wechart_tex_pro(msg)
    time_type = ['今天','明天','后天','早上','上午','凌晨','下午','晚上','点']
    flag = 0
    for i in time_type:
        if i in time:
            flag = 1
    if flag:
        Tixing(time, head+cmd) 
    else:
        os.system(head + cmd)

def wechart_tex_pro(info):
    print("准备发送。。。")
    username = info[info.find('给')+1:info.find('内容')]
    if(username is None):
        print("发送对象有误")
    else:
        text = info[info.find('内容是')+3:]
    return ("-s " + username + " -t " + text) 
   

def wechart_listen():
    try:
        os.system("python wechart/wechartAPI.py -r")
    except Exception,e:
        print("运行出错:" + e)

def wechart_share(info,file):
    username = info[info.find("分享给")+3:info.find("音乐")]
    try:
        print("分享%s给%s" %(file,username))
        os.system("rm wechart/*.pyc")
        os.system("python wechart/wechartAPI.py -s " + username + " -f " + file)
    except Exception,e:
        print("分享出错:" + e)

def command_process(info):
    global song_list
    #LED相关
    tex = ' '
    delect_zifu(info)
    if '皮卡丘' in info:
        tex = '在。。。的'
        yuyinhecheng.tts_main(tex,tok)
    elif '灯' in info:
        pin = zhuanhuan(info)
        if '开' in info:
            for i in pin:
                LED(i, 1)
        elif '关' in info:
            for i in pin:
                LED(i, 0)   
        else:
            tex = "您是开灯还是关灯啊？"
            yuyinhecheng.tts_main(tex,tok)
    #DHT11相关
    elif '环境' in info:
        os.system("python DHT11.py")
    #相机相关
    elif '相机' in info:
        if '延时' in info:
            t = zhuanhuan(info)
            if t :
                Camera.Camera(t)
            else: 
                Camera.Camera(5)
        elif '视频' in info:
            t = zhuanhuan(info)
            Camera.Camera_video()
        elif '人脸' in info:
            Camera.Camera_max() 
        elif ('采集' in info):
            print("开始采集人脸数据")
            os.system("python /home/树莓派语音/Raspberry-Face-Recognition/face_datasets.py")
            time.sleep(0.5)
        elif '训练' in info:
            print("开始训练")
            os.system("python /home/树莓派语音2/Raspberry-Face-Recognition/training.py") 
        elif '身份' in info:
            os.system("python /home/树莓派语音/Raspberry-Face-Recognition/face_recognition.py")
        elif '关' in info:
            os.system("/etc/init.d/webcam stop")
        else:
            os.system("python xiangji.py")
            #pass
    #音乐相关   
    elif ('音乐' in info) or ('歌' in info):
        global song_list
        if '下载' in info:
            mu = info.split("音乐")[1]
            info = "python3 download_song.py " + mu
            os.system(info)
        elif '歌手' in info:
            songer = info.split("歌手")[1]
            print songer
            songer_song(songer)
            #os.system("python Music/songer.py " + songer)        
        elif '连续' in info:
            lianxu_song()
        elif ('停' in info):
            print("kill -STOP " + killprocess.getpid_by_name('mplayer'))
            os.system("kill -STOP " + killprocess.getpid_by_name('mplayer'))
        elif ('关闭' in info):
            print("关闭所有音乐播放")
            os.system("kill " + killprocess.getpid_by_name('mplayer'))
            song_list.clear()
        elif ('继续' in info):
            print("kill -CONT " + killprocess.getpid_by_name('mplayer'))
            os.system("kill -CONT " + killprocess.getpid_by_name('mplayer'))
        elif '上一首' in info:
            info = song_list[len(song_list)-2]
            os.system("kill -STOP " + killprocess.getpid_by_name('mplayer'))
            os.system("mplayer " + info)
        elif '下一首' in info:
            #os.system("python killprocess.py mplayer")
            killprocess.kill_process_by_name('mplayer')
        #elif info.split('音乐')[1] != '':
        #    os.system("mplayer Music/" + info + ".mp3")
        elif '分享' in info:
            f_music = " "
            if("/home" in song_list[len(song_list)-1]):
                f_music = song_list[len(song_list)-1].strip()
            else:
                f_music = "/home/树莓派语音/music/"
                f_music = f_music + song_list[len(song_list)-1]
            wechart_share(info,f_music)

        elif ('列表' in info) or ('菜单' in info):
            os.system("ls /home/树莓派语音/music")
            #info = raw_input("输入歌曲信息:")
            os.system("python /home/树莓派语音/music/songer.py")
        elif info.split('音乐')[1] != '':
            song_list.append(info.split('音乐')[1] + ".mp3")
            os.system("python songer.py " + info.split('音乐')[1] + ".mp3")
            """1
            os.system("mplayer Music/" + info.split('音乐')[1] + ".mp3")
            os.system("touch music.lst")
            os.system("ls /home/树莓派语音/music > music.lst")
            with open('music.lst','r') as mus:
                for line in mus.readlines():
                    if info.split('音乐')[1] in line:
                        os.system("python songer.py " + info.split('音乐')[1])
                        break
                    else:
                        yuyinhecheng.tts_main('歌库中没有这首音乐',tok)
                        break
                        #os.system("python3 download_song.py "+ str(info.split('音乐')[1]))
            os.system("rm music.lst")
            """
        else:
            suiji_song(15)    
        
    #闹钟相关        
    elif '闹钟' in info:
        if '开' in info:
            naozhong(info)  
        elif '关' in info:
            os.system("crontab -r")
        else:
            tex= "您可以开闹钟和关闭闹钟"
            yuyinhecheng.tts_main(tex,tok)
            os.system("crontab -l")
    #邮箱相关
    elif ('邮箱' in info) or ('邮件' in info):
        if '看' in info:
            info = "python email_js.py 3362296153@qq.com thibqlcuhoqzchgj pop.qq.com 3"
            os.system(info)
        elif '发' in info:
            info = info[info.find('给')+1:].encode("utf-8")
            email(info)
    #12306火车票
    elif '车票' in info:
        if '查一下' in info:
            info = info[info.find('查一下')+1:]
        elif '查' in info:
            info = info[info.find('查')+1:]
        tex = tickets_msg_pro(info)
        print(tex)
        #list = tickets.cli()
        #yuyinhecheng.tts_main(list,tok)
        #print(ret)
        os.system('python /home/树莓派语音2/tra_station/tickets.py '+ tex)
        #print(resul)
    #备忘录
    elif '提醒' in info:
        if '查看' in info.split("提")[0]:
            os.system("crontab -l")
        elif '删除' in info.split("提")[0]:
            if '全部' in info or '所以' in info:
                os.system("crontab -r")
            else:
                pass
        elif info.split("提醒")[1] == '':
            pass
        else:    
            Tixing(info,'T')
            os.system("crontab -l")
       

    #开放外网端口
    elif '外网' in info:
        if '开' in info:
            os.system("sh /home/Ngrok/ngrok.sh")
        if '关' in info:
            killprocess.kill_process_by_name('ngrok')          
    #文件系统
    elif '文件' in info:
        tex = ''
        if '查' in info:
            if info.split("文件")[1] == '':
                tex = raw_input("输入文件名:")
            else:
                tex = info.split("文件")[1]
            os.system("find / -name "+ tex)
            tex = '已帮您找到相关结果'
            yuyinhecheng.tts_main(tex,tok)
        elif '开' in info:
            tex = raw_input("输入文件名:")
            os.system("nano "+tex)
        else:
            pass
    elif '微信' in info:
        if("打开" in info and "内容" not in info):
            wechart_listen()
        elif "发送" in info:
            wechat_Send_Pro(info)
    else:   
        tex = Turling.Tuling(info)
        yuyinhecheng.tts_main(tex,tok)  
       
