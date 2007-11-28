#!/usr/bin/env python
# encoding: utf-8
"""
nsupdate.py

Created by Razor on 2007-11-19.
Copyright (c) 2007 xBayDNS Team. All rights reserved.

update DNS server on FLY...
"""

from dns import name, query, rdataclass, rdatatype, rdataset,\
                            rdata, resolver, tsigkeyring, update, zone

class NSUpdate:
    def __init__(self, addr, domain, view = False, port = 53):
        self.addr = addr
        self.port = port
        self.domain = domain
        self.view = view
        self.tsigkey = None
        if view != False:
            # get TSIG
            self.tsigkey = tsigkeyring.from_text({'keyname' : 'xxxxxxxx'})
        self.domain_info = self._getDomainInfo()
        self.updatemsg = update.Update(self.domain, keyring = self.tsigkey)
        
    def _getDomainInfo(self):
        # get full zone by xfr, for checking before add/remove/update records
        domain_info = zone.from_xfr(query.xfr(self.addr, self.domain, keyring = self.tsigkey))
        return domain_info
    
    def _updateWrapper(self, func, recordlist):
        for name, ttl, rdclass, rdtype, token in recordlist:
            rdatalist = []
            for token_str in token:
                rdatalist.append(rdata.from_text(
                        rdataclass.from_text(rdclass),
                        rdatatype.from_text(rdtype),
                        token_str,
                        origin = self.domain))
            recordset = rdataset.from_rdata_list(ttl, rdatalist)
            func(name, recordset)
                    
    def addRecord(self, recordlist):
        '''
        generate an update message for adding record.
        : param domain: the name of the domain. string.
        : param recordlist: list of the records to be added.
        '''
        self._updateWrapper(self.updatemsg.add, recordlist)
        
    def removeRecord(self, recordlist, entire_node = False):
        '''
        generate an update message for removing record.
        '''
        if entire_node == True:
            for name in recordlist:
                self.updatemsg.delete(name)
        else:
            self._updateWrapper(self.updatemsg.delete, recordlist)
        
    def updateRecord(self, recordlist):
        '''
        generate an update message for updating record.
        '''
        pass

    def commitChanges(self, timeout = None, usetcp = True):
        '''
        send the update messages to NS server
        '''
        if usetcp == True:
            query_wrapper = query.tcp
        else:
            query_wrapper = query.udp
        response = query_wrapper(self.updatemsg, self.addr, timeout, self.port)
        print response
        self.updatemsg = update.Update(self.domain, keyring = self.tsigkey)
        
    def queryRecord(self, name, view = False, rdtype = 'A', 
                    usetcp = False, timeout = 30, rdclass = 'IN'):
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

