#!/usr/bin/env python
# encoding: utf-8
"""
algorithms.py

Created by Razor <bg1tpt AT gmail.com> on 2008-03-22.
Copyright (c) 2008 xBayDNS Team. All rights reserved.

"""
from __future__ import generators
import time, sets
from types import *

def ecintersection(*devides):
    if len(devides) == 0:
        return 1
    s1 = time.time()
    # construct complete set
    complete_set = sets.Set()
    print devides
    for ec in flatten22(devides[0],isScalar):
        complete_set.add(ec)
    e1 = time.time()
    print "cost sec1 time: %f"%(e1-s1) 
    
    s2 = time.time()
    ec_dict = {}
    # construct ec dictionary
    #map(lambda element:ec_dict.setdefault(element,sets.Set()),complete_set)
    e2 = time.time()
    print "cost sec2 time: %f"%(e2-s2) 
    
    s3 = time.time()
    # construct ec for every element from the factor set and get intersection
    for devide in devides:
        for ec in devide:
            ec_set = sets.Set(ec)
            for element in ec:
                if ec_dict.has_key(element) == False:
                    ec_dict[element] = ec_set
                else:
                    ec_dict[element] = ec_dict[element].intersection(ec_set)
    e3 = time.time()
    print "cost sec3 time: %f"%(e3-s3) 
    #print ec_dict
    
    s4 = time.time()
    # convert to factor set
    factor_set = []
    for ec in ec_dict.itervalues():
        try:
            factor_set.index(ec)
        except:
            factor_set.append(ec)
            
    e4 = time.time()
    print "cost sec4 time: %f"%(e4-s4) 
    #print factor_set
    return factor_set



def flatten22(sequence, scalarp):
    for item in sequence:
        if scalarp(item):
            yield item
        else:
            for subitem in flatten22(item, scalarp):
                yield subitem
                
def canLoopOver(maybeIterable):
    if type(maybeIterable) == ListType:
        return 1
    else:
        return 0
    
def isScalar(obj):
    return not canLoopOver(obj)


if __name__=='__main__':
    # test
    import ipdevide_gen
    testdev = ipdevide_gen.ipdevide_gen(500, 30)#4个IP3组
    print testdev
#    for dev in testdev:
#        print "dev: %s"%str(dev)
    start = time.time()
    result = ecintersection(*testdev)
    end = time.time()
    print "factor set: %s"%str(result)
    print "cost time: %f"%(end-start)

