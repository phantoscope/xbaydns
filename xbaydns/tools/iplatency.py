#!/usr/bin/env python
# encoding: utf-8
"""
iplatency.py

Created by Razor <bg1tpt AT gmail.com> on 2008-03-17.
Copyright (c) 2008 xBayDNS Team. All rights reserved.

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
MAX_TESTING = 5

pool_sema = threading.BoundedSemaphore(MAX_TESTING)
file_mutex = threading.Lock()

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
    if len(querytime_lst) > 0:
        latencys['query']['avg'] = float(sum(querytime_lst))/len(querytime_lst)
        latencys['query']['min'] = min(querytime_lst)
        latencys['query']['max'] = max(querytime_lst)
        latencys['run']['avg'] = sum(runtimes_lst)/len(runtimes_lst)
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
        if len(latencys['query']) == 0:
            latencys = getlatency_gateway(ip)
            if len(latencys) == 0:
                pingtype = "OUT_OF_REACH"
                latency = -1
            else:
                pingtype = "PING_GATEWAY"
                latency = latencys['avg']
        else:
            pingtype = "NS_QUERY"
            latency = latencys['query']['avg']
    else:
        pingtype = "PING_HOST"
        latency = latencys['avg']
    return (pingtype, latency)

def threadmain(ip, fileobj):
    pool_sema.acquire(True)
    pingtype, latency = getlatency(ip)
    pool_sema.release()
    file_mutex.acquire()
    fileobj.write("%s,%s,%s,%s\n"%(ip, pingtype, latency, time.strftime("%Y-%m-%d %H:%M:%S")))
    file_mutex.release()

def main():
    threads = []
    input = "/dev/stdin"
    output = "/dev/stdout"
    if len(sys.argv) == 1:
        pass
    elif len(sys.argv) == 2:
        input = sys.argv[1]
    elif len(sys.argv) == 3:
        input = sys.argv[1]
        output = sys.argv[2]
    else:
        print "Usage: xxxxxxxxxx"
        return 1
    try:
        iplst = open(input, "r")
        latency_file = open(output, "a")
    except IOError, e:
        print e.strerror
        return 1
    while True:
        ip = iplst.readline().strip('\n')
        if ip == '':
            break
        threads.append(threading.Thread(target=threadmain, args=(ip, latency_file)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    latency_file.close()
    return 0

if __name__ == '__main__':
    sys.exit(main())
