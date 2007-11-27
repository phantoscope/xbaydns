#!/usr/bin/env python
# encoding: utf-8
"""
nsupdate.py

Created by Razor on 2007-11-19.
Copyright (c) 2007 xBayDNS Team. All rights reserved.

update DNS server on FLY...
"""

from dns import name, query, rdataclass, rdatatype, \
                            resolver, tsigkeyring, update, zone

class NSUpdate:
    def __init__(self, addr, port = 53):
        self.addr = addr
        self.port = port
        
    def getZoneInfo(self):
        pass
        
    def addRecord(self):
        pass
        
    def removeRecord(self):
        pass
        
    def updateRecord(self):
        pass
        
    def queryRecord(self, name, view = False, rdtype = 'A', usetcp = False, timeout = 30, rdclass = 'IN'):
        '''
        query a record though the specified NS server.
        '''
        resolv = resolver.Resolver()
        resolv.nameservers = [self.addr]
        resolv.port = self.port
        resolv.lifetime = timeout
        if view != False:
            # get TSIG
            tsigkey = tsigkeyring.from_text({'keyname' : 'xxxxxxxx'})
            resolv.use_tsig(tsigkey)
        try:
            resultset = resolv.query(name, rdatatype.from_text(rdtype), 
                                               rdataclass.from_text(rdclass), tcp = usetcp)
        except resolver.Timeout:
            # query time exceed the lifetime
            return False
        except resolver.NXDOMAIN:
            # the query name does not exist
            return False
        except resolver.NoAnswer:
            # the response did not contain an answer
            return False
        except resolver.NoNameservers:
            # no non-broken nameservers are available to answer the question.
            return False
        return [ record.to_text() for record in resultset ]

