#!/usr/bin/env python
# encoding: utf-8

from __future__ import generators
import time, sets
from types import *

def quicksort(dict,keys):
    for i,idc in enumerate(keys):
        if i == 0:
            result = [[idc],float(dict[idc].strip())]
        else:
            if result[1] > float(dict[idc].strip()) and float(dict[idc].strip())>=0:
                result[0] = [idc]
                result[1] = float(dict[idc].strip())
            elif  result[1] == float(dict[idc].strip()) and float(dict[idc].strip())>=0:
                result[0].append(idc)
            elif result[1] < 0:
                result = [[idc],float(dict[idc].strip())]
    if result[1] <0:
        return keys
    else:
        return result[0]

def getRoute(selection):
    result = ''
    for i in selection:
        result = result + ','+str(i[0])
    return result[1:]

def ipgen():
    return "%d.%d.%d.%d"%(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class PerformanceMatrix:
    def __init__(self,services):
        if services == None:
            self.services = {}
        else:
            self.services = services
        self.matrix = {}
        self.ips ={}
        
    def ip(self,ip,speeds):
        self.matrix.setdefault(ip,speeds)
    
    def partitions(self):
        for service,servers in self.services.items():
            print service,servers
            for ip,speeds in self.matrix.items():
                result = quicksort(speeds,servers)
                if result > 0:
                    self.ips.setdefault(ip,[])
                    self.ips[ip].append((result,service))
        partitions = {}
        for ip, selection in self.ips.items():
            route = getRoute(selection)
            partitions.setdefault(route,[])
            partitions[route].append(ip)
        return partitions
                
if __name__=='__main__':
    import random
    services = {'www.hello.com' :['xd', 'gz'], 'ftp.hello.com' :['gz', 'xa'], 'www.world.com' : ['xd','xa']}
    pmatrix = PerformanceMatrix(services)
    #for i in range(1,10):
    #    pmatrix.ip(ipgen(),speeds = {'D1':random.randint(1,10),'D2':random.randint(1,10),'D3':random.randint(1,10)})
    pmatrix.ip('99.1.1.1',speeds = {'xd':'5','gz':'10','xa':'15'})
    pmatrix.ip('99.2.2.2',speeds = {'xd':'5','gz':'15','xa':'20'})
    pmatrix.ip('99.3.3.3',speeds = {'xd':'5','gz':'20','xa':'25'})
    pmatrix.ip('99.4.4.4',speeds = {'xd':'15','gz':'10','xa':'5'})
    pmatrix.ip('99.5.5.5',speeds = {'xd':'20','gz':'15','xa':'10'})
    pmatrix.ip('99.6.6.6',speeds = {'xd':'10','gz':'15','xa':'5'})
    pmatrix.ip('99.7.7.7',speeds = {'xd':'20','gz':'15','xa':'5'})
    pmatrix.ip('99.8.8.8',speeds = {'xd':'10','gz':'10','xa':'10'})
    pmatrix.ip('99.9.9.9',speeds = {'xd':'10','gz':'-1','xa':'-1'})
    pmatrix.ip('99.10.10.10',speeds = {'xd':'10','gz':'-1','xa':'5'})
    pmatrix.ip('99.11.11.11',speeds = {'xd':'-1','gz':'-1','xa':'-1'})
    print pmatrix.matrix
    start = time.time()
    print pmatrix.partitions()
    end = time.time()
    print "cost time: %f"%(end-start)
    print pmatrix.ips