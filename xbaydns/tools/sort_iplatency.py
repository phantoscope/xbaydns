#!/opt/xbaydns/bin/python
import os,sys
import traceback

def sort(speeds_dict):
    result = [[''],-1]
    for idc,speed in speeds_dict.items():
        if result[1] > float(speed.strip()) and float(speed.strip())>=0:
            result[0] = [idc]
            result[1] = float(speed.strip())
        elif  result[1] == float(speed.strip()) and float(speed.strip())>=0:
            result[0].append(idc)
        elif result[1] < 0:
            result = [[idc],float(speed.strip())]
    if result[1] <0:
        return speeds_dict.keys()
    else:
        return result[0]

def gensort(CONF_FILE):
#CONF_FILE='/opt/xbaydns/home/xbaydns/view/idcview/idcview.current'
#CONF_FILE='c:/2.txt'
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
