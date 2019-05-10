#coding:utf-8
import sys,os

def getpid_by_name(name):
    cmd = "ps -e | grep %s" % name
    f = os.popen(cmd)
    txt = f.readlines()
    if len(txt) == 0:
        print "no process \"%s\"!!" % name
        return
    else:
       for line in txt:
        colum = line.split()
        pid = colum[0]
    return str(pid)

def kill_process_by_name(name):
    cmd = "ps -e | grep %s" % name
    f = os.popen(cmd)
    txt = f.readlines()
    if len(txt) == 0:
        print "no process \"%s\"!!" % name
        return
    else:
       for line in txt:
       	colum = line.split()
       	pid = colum[0]
       	cmd = "kill -9 %d" % int(pid)
       	rc = os.system(cmd)
       	if rc == 0 : 
       	    print "exec \"%s\" success!!" % cmd
       	else:
           print "exec \"%s\" failed!!" % cmd
    return
#if __name__ == "__main__":
#    if len(sys.argv) == 1:
#        name=raw_input("plz input the process name which you want to kill :")
#    else:
#        name=sys.argv[1]
kill_process_by_name(sys.argv[1])
