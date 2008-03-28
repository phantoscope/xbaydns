#!/usr/bin/env python
# encoding: utf-8
"""
idcview.py

Created by QingFeng on 2008-03-17.
Copyright (c) 2007 xBayDNS Team. All rights reserved.
"""

from decimal import Decimal
from operator import itemgetter
import os, sys

def pingtype_weight(pingtype,v,data_value=-1):
    if data_value == -1:data_value=v
    pingtype=pingtype.upper()
    rule={
        'OUT_OF_REACH':0,
        'other':(data_value+v)/2,
    }
    return rule.get(pingtype,rule.get('other'))
    
def cmptuple(x, y):
    if (x[1] - y[1] < 0): return -1
    elif (x[1] - y[1] == 0): return 0
    else: return 1

def convfiles(files):
    data={}
    for f in files:
        filename = os.path.basename(f)
        agent_ip, sampledate = filename.split('_')
        for r in open(f):
            #OUT_OF_REACH,PING_GATEWAY,-1
            if r.strip()=='':
                continue
            ip,pingtype,pingavg,pingtime=map(lambda x:x.strip(),r.split(','))
            if ip not in data:
                data[ip]=[(agent_ip, pingtype_weight(pingtype,Decimal(pingavg)))]
            else:
                data[ip].append((agent_ip, pingtype_weight(pingtype,Decimal(pingavg))))
    for ip in data.keys():
        data[ip].sort(cmp=cmptuple)
    data=sorted(data.items(),key=itemgetter(1))
    return data
    
agentfiles = sys.argv[1:]
datafile = "idcview_out.txt"
datafile_obj = open(datafile, "w")
data = convfiles(agentfiles)
for ip, latencies in data:
    datafile_obj.write("%s,%s"%(ip, latencies[0][0]))
    for latency in latencies:
        datafile_obj.write(",%.3f"%latency[1])
    datafile_obj.write('\n')
datafile_obj.close()
