#!/usr/bin/env python
# encoding: utf-8
"""
iplatency.py

Created by Razor <bg1tpt AT gmail.com> on 2008-03-17.
Copyright (c) 2007 xBayDNS Team. All rights reserved.

"""

import os, re, socket, struct, sys
import threading

PING_CMD = "ping -c5 -q %s"
PING_RE = re.compile(".* min/avg/max/\D+ = ([0-9.]+)/([0-9.]+)/([0-9.]+).* ms")
NETMASK_C = 0xFFFFFF00
DEFAULT_GATEWAY = 1

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
    pass

def getlatency_gateway(ip):
    ip_nl = socket.htonl(struct.unpack("I", socket.inet_aton(ip))[0])
    net_nl = ip_nl & NETMASK_C
    gateway_ip_nl = net_nl + DEFAULT_GATEWAY
    gateway_ip = socket.inet_ntoa(struct.pack("I", socket.ntohl(gateway_ip_nl)))
    return getlatency_ping(gateway_ip)

def main():
    print getlatency_ping('202.108.35.50')
    print getlatency_gateway('202.108.35.50')
    
if __name__ == '__main__':
    sys.exit(main())
    