#!/usr/bin/env python
# encoding: utf-8
"""
iplatency.py

Created by Razor <bg1tpt AT gmail.com> on 2008-03-17.
Copyright (c) 2007 xBayDNS Team. All rights reserved.

"""

import os, re, socket, struct, sys, time
import threading

PING_CMD = "ping -c5 -q %s"
PING_RE = re.compile(".* min/avg/max/\D+ = ([0-9.]+)/([0-9.]+)/([0-9.]+).* ms")
NETMASK_C = 0xFFFFFF00
DEFAULT_GATEWAY = 1
DIG_CMD = "dig +noanswer +noquestion @%s . NS"
DIG_RE = re.compile("Query time: (\d+) msec")
MAXQUERIES = 5
QUERY_INTERVAL = 5

def getlatency_ping(ip):
    latencys = {}
    ping = os.popen(PING_CMD%ip, "r")
    while True:
        output = ping.readline()
        if output == '':
            break
        if PING_RE.match(output) != None:
            latencys['min'], latencys['avg'], latencys['max'] = PING_RE.match(output).groups()
            break
    ping.close()
    return latencys

def getlatency_queryns(ip):
    latencys = dict(query={}, run={})
    querytime_lst = []
    runtimes_lst = []
    count = 0
    while count < MAXQUERIES:
        time_start = time.time()
        dig = os.popen(DIG_CMD%ip, "r")
        output = dig.read()
        time_end = time.time()
        dig.close()
        querytime = DIG_RE.findall(output)
        if len(querytime) != 0:
            querytime_lst.append(int(querytime[0]))
            runtimes_lst.append(round((time_end - time_start) * 1000, 3))
        time.sleep(QUERY_INTERVAL)
        count += 1
    latencys['query']['avg'] = float(sum(querytime_lst))/len(querytime_lst)
    latencys['query']['min'] = min(querytime_lst)
    latencys['query']['max'] = max(querytime_lst)
    latencys['run']['avg'] = sum(runtimes_lst)/len(querytime_lst)
    latencys['run']['min'] = min(runtimes_lst)
    latencys['run']['max'] = max(runtimes_lst)
    return latencys

def getlatency_gateway(ip):
    ip_nl = socket.htonl(struct.unpack("I", socket.inet_aton(ip))[0])        # "I" unsigned int
    net_nl = ip_nl & NETMASK_C
    gateway_ip_nl = net_nl + DEFAULT_GATEWAY
    gateway_ip = socket.inet_ntoa(struct.pack("I", socket.ntohl(gateway_ip_nl)))
    return getlatency_ping(gateway_ip)

def getlatency(ip):
    latencys = getlatency_ping(ip)
    if len(latencys) == 0:
        latencys = getlatency_queryns(ip)
        if len(latencys) == 0:
            latencys = getlatency_gateway(ip)
            if len(latencys) == 0:
                pingtype = "OUT_OF_REACH"
                latency = -1
            else:
                pingtype = "PING_GATEWAY"
                latency = latencys['avg']
        else:
            pingtype = "NS_QUERY"
            latency = latencys['run']['avg']
    else:
        pingtype = "PING_HOST"
        latency = latencys['avg']
    print pingtype, latency

def main():
    #print getlatency_ping('202.108.35.50')
    #print getlatency_gateway('202.108.35.50')
    #print getlatency_queryns('10.210.12.10')
    #print getlatency_queryns('202.106.182.153')
    getlatency('202.108.35.50')
    getlatency('10.210.12.10')
    getlatency('202.106.182.153')
    getlatency('202.106.0.20')
    
if __name__ == '__main__':
    sys.exit(main())
