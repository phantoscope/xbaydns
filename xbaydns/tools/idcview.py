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

'''
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
'''

def convfiles(files):
    agents = []
    data = {}
    for filename in files:
        agent_name = filename.split('_')[0]
        agents.append(agent_name)
        file_obj = open(filename, "r")
        line = file_obj.readline()
        preip, pingtype, latency, datetime = line.split(',')
        if preip not in data:
            data[preip] = {}
        latency_sum = Decimal(latency)
        record_count = 1
        for line in file_obj:
            ip, pingtype, latency, datetime = line.split(',')
            if preip != ip:
                if preip not in data:
                    data[preip] = {}
                data[preip][agent_name] = latency_sum/record_count
                preip = ip
                latency_sum = Decimal(latency)
                record_count = 1
            else:
                latency_sum += Decimal(latency)
                record_count += 1
        if preip not in data:
            data[preip] = {}
            data[preip][agent_name] = latency_sum/record_count           
    return (agents, data)


agentfiles = sys.argv[1:]
agents, data = convfiles(agentfiles)
datafile = "idcview_out.txt"
datafile_obj = open(datafile, "w")
# write header
header = ""
for agent_name in agents:
    header += "%s,"%agent_name
datafile_obj.write("%s\n"%header[:-1])
for ip, latency_agents in data.items():
    datafile_obj.write("%s"%ip)
    for agent_name in agents:
        if agent_name not in latency_agents:
            datafile_obj.write(",-1")
        else:
            datafile_obj.write(",%.2f"%latency_agents[agent_name])
    datafile_obj.write("\n")
datafile_obj.close()
