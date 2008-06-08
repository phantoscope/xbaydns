#!/opt/xbaydns/bin/python
import os,sys
import traceback

def sort(speeds_dict):
    result = [[''],-1]
    r = []
    l = speeds_dict.values()
    l.sort()
    for speed in l:
        if float(speed.strip()) > 0:
            for k,v in speeds_dict.items():
                if v == speed:
                    if k not in r:
                        r.append(k)
    return r


def gensort(CONF_FILE):
#CONF_FILE='/opt/xbaydns/home/xbaydns/view/idcview/idcview.current'
    CONF_FILE='c:/2.txt'
    sort_dict = {}
    result_dict = {}
    for i,r in enumerate(open(CONF_FILE)):
        if i==0:
            agents=r.split(',')
            agents=map(lambda x:x.strip(),agents)
            continue
        r=r.split(',')
        ip,times=r[0],r[1:]
        speeds_dict ={}
        for agent,time in zip(agents,times):
            speeds_dict.update({agent:time})
        sort_dict.setdefault(ip,speeds_dict)
    f = open('./result.txt','w')
    for ip,speeds in sort_dict.items():
        result = sort(speeds)
        result_dict.update({ip:result})
        print '%s:%s'%(ip,result)
    
    
if __name__=="__main__":
    gensort(sys.argv[1])
