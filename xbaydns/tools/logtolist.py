#!/usr/bin/env python
# encoding: utf-8
"""
logtolist.py

Created by QingFeng on 2008-03-16.
Copyright (c) 2008 xBayDNS Team. All rights reserved.
"""
import re, sys

def logtolist(s):
    data={}
    c=re.compile("\d+\.\d+\.\d+\.\d+")
    for ip in c.findall(s):
        data[ip]=''
    return data.keys()

def main(logfile, iplist):
    log = open(logfile, "r").read()
    ips = logtolist(log)
    iplistfile = open(iplist, "w")
    for ip in ips:
        iplistfile.write("%s\n"%ip)
    iplistfile.close()
    return

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: %s logfile outputfile"%__file__
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
