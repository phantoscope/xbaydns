#!/usr/bin/env python
# encoding: utf-8

from __future__ import generators
import time, sets
from types import *

def quicksort(dict,keys):
    result = (keys[0],float(dict[keys[0]].strip()))
    for k,v in dict.items():
        if k in keys: 
            if result[1] > float(dict[k].strip()):
                result = (k,dict[k])
        else:
            pass
    return result[0]

def getRoute(selection):
    result = ''
    for i in selection:
        result = result + ','+i[0]
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
            for ip,speeds in self.matrix.items():
                self.ips.setdefault(ip,[])
                result = quicksort(speeds,servers)
                self.ips[ip].append((result,service))
        partitions = {}
        for ip, selection in self.ips.items():
            route = getRoute(selection)
            partitions.setdefault(route,[])
            partitions[route].append(ip)
        return partitions
                
if __name__=='__main__':
    import random
    services = {'www' :['D1', 'D2'], 'ftp' :['D2', 'D3'], 'mtv' : ['D1','D3']}
    pmatrix = PerformanceMatrix(services)
    for i in range(1,10):
        pmatrix.ip(ipgen(),speeds = {'D1':random.randint(1,10),'D2':random.randint(1,10),'D3':random.randint(1,10)})
    #pmatrix.ip('10.210.12.1',speeds = {'D1':1,'D2':2,'D3':3})
    #pmatrix.ip('10.210.12.2',speeds = {'D1':3,'D2':2,'D3':1})
    #pmatrix.ip('10.210.12.3',speeds = {'D1':2,'D2':3,'D3':1})
    #pmatrix.ip('10.210.12.4',speeds = {'D1':1,'D2':2,'D3':3})
    start = time.time()
    print pmatrix.partitions()
    end = time.time()
    print "cost time: %f"%(end-start)
    print pmatrix.ips