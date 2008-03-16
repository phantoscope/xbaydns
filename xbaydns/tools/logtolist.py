#!/usr/bin/env python
# encoding: utf-8
"""
logtolist.py

Created by QingFeng on 2008-03-16.
Copyright (c) 2008 xBayDNS Team. All rights reserved.
"""
import re

def logtolist(s):
    data={}
    c=re.compile("\d+\.\d+\.\d+\.\d+")
    for ip in c.findall(s):
        data[ip]=''
    return data.keys()

