#!/usr/bin/env python
# encoding: utf-8
"""
idcview.py

Created by QingFeng on 2008-03-17.
Copyright (c) 2007 xBayDNS Team. All rights reserved.
"""

from decimal import Decimal
from operator import itemgetter

def pingtype_weight(pingtype,v,data_value=0):
    pingtype=pingtype.upper()
    if pingtype == 'OUT_OF_REACH':
        return 0
    else:
        if data_value==0:
            return v
        else:
            return (data_value+v)/2
    return v

def convfiles(files):
    data={}
    for f in files:
        for r in open(f):
            #OUT_OF_REACH,PING_GATEWAY,-1
            ip,pingtype,pingavg,pingtime=map(lambda x:x.strip(),r.split(','))
            if ip not in data:
                data[ip]=pingtype_weight(pingtype, Decimal(pingavg) )
            else:
                data[ip]=pingtype_weight(pingtype, Decimal(pingavg),data[ip] )
    data=sorted(data.items(),key=itemgetter(1))
    return data
    
