#!/usr/bin/env python
# encoding: utf-8
"""
idcview.py

Created by QingFeng on 2008-03-17.
Copyright (c) 2007 xBayDNS Team. All rights reserved.
"""

from decimal import Decimal
from operator import itemgetter
import os, sys, time

from xbaydns.conf import sysconf

def convfiles(files):
    agents = []
    data = {}
    for filename in files:
        agent_name = os.path.basename(filename).split('_')[0]
        agents.append(agent_name)
        file_obj = open(filename, "r")
        line = file_obj.readline()
        try:
            preip, pingtype, latency, datetime = line.split(',')
        except Exception, e:
            print line
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

def main():
    if len(sys.argv) == 1:
        logdir = os.path.join(sysconf.xbaydnsdb, 'agent_logs')
        if os.path.isdir(logdir) == False:
            print "No such a directory %s"%logdir
            sys.exit(1)
        else:
            agentfiles = os.listdir(logdir)
            agentfiles = map(lambda x:os.path.join(logdir, x), agentfiles)
    else:
        agentfiles = sys.argv[1:]
    
    if len(agentfiles) == 0:
        print "No logs in the directory %s"%sysconf.xbaydnsdb
        sys.exit(1)
    
    outputdir = os.path.join(sysconf.xbaydnsdb, 'idcview')
    if os.path.isdir(outputdir) == False:
        try:
            os.mkdir(outputdir)
        except OSError, e:
            print e.strerror
            sys.exit(1)
    outputfile = "%s/idcview.%s"%(outputdir, time.strftime("%Y-%m-%d"))
    agents, data = convfiles(agentfiles)
    outputfile_obj = open(outputfile, "w")
    # write header
    header = ""
    for agent_name in agents:
        header += "%s,"%agent_name
    outputfile_obj.write("%s\n"%header[:-1])
    for ip, latency_agents in data.items():
        outputfile_obj.write("%s"%ip)
        for agent_name in agents:
            if agent_name not in latency_agents:
                outputfile_obj.write(",-1")
            else:
                outputfile_obj.write(",%.2f"%latency_agents[agent_name])
        outputfile_obj.write("\n")
    outputfile_obj.close()
    outputlink = "%s/idcview.current"%outputdir
    if os.path.islink(outputlink) == True:
        os.remove(outputlink)
    try:
        os.symlink(outputfile, outputlink)
    except OSError, e:
        print e.strerror
        sys.exit(1)

if __name__ == "__main__":
    main()    