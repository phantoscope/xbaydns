#!/opt/xbaydns/bin/python
import os,sys
import traceback

def sort(speeds_dict):
    if speeds_dict.has_key(-1):
        speeds_dict.pop(-1)
    keys = speeds_dict.keys()
    keys.sort()
    return map(speeds_dict.get, keys)[:2]
    
    

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
            agent = agent.strip()
            time = float(time.strip())
            if speeds_dict.has_key(time):
                speeds_dict[time].append(agent)
            else:
                speeds_dict.update({time:[agent]})
        sort_dict.setdefault(ip,speeds_dict)
    f = open('./result.txt','w')
    for ip,speeds in sort_dict.items():
        result = sort(speeds)
        result_dict.update({ip:result})
        if len(result)==2:
            print '%s:%s    %s'%(ip,result[0],result[1])
        elif len(result)==1:
            print '%s:%s    %s'%(ip,result[0])
        else:
            print '%s:%s'%(ip,[])
    
    
if __name__=="__main__":
    gensort(sys.argv[1])
