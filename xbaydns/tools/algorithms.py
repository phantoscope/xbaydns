#!/usr/bin/env python
# encoding: utf-8
"""
algorithms.py

Created by Razor <bg1tpt AT gmail.com> on 2008-03-22.
Copyright (c) 2008 xBayDNS Team. All rights reserved.

"""
import time, sets

def ecintersection(*devides):
    if len(devides) == 0:
        return 1
    
    # construct complete set
    complete_set = sets.Set()
    for ec in devides[0]:
        for element in ec:
            complete_set.add(element)

    ec_dict = {}
    # construct ec dictionary
    for element in complete_set:
        ec_dict[element] = sets.Set()

    # construct ec for every element from the factor set and get intersection
    for devide in devides:
        for ec in devide:
            ec_set = sets.Set()
            for element in ec:
                ec_set.add(element)
            for element in ec:
                if len(ec_dict[element]) == 0:
                    ec_dict[element] = ec_set
                else:
                    ec_dict[element] = ec_dict[element].intersection(ec_set)
#                    ec_dict[element].intersection_update(ec_set)       is there a python's bug?
    print ec_dict

    # convert to factor set
    factor_set = []
    for ec in ec_dict.itervalues():
        seen = False
        for factor in factor_set:
            if factor == ec:
                seen = True
                break
        if seen == False:
            factor_set.append(ec)
    #print factor_set
    return factor_set
'''
def ecintersection_matrix(*devides):
    if len(devides) == 0:
        return 1
    
    # construct complete set
    complete_set = set()
    for ec in devides[0]:
        for element in ec:
            complete_set.add(element)

    # construct element hash
    ehash = []
    for element in complete_set:
        ehash.append(element)

    # ec into matrix
    for devide in devides:
        ec_matrix = zeros((len(complete_set),)*2)
'''

if __name__=='__main__':
    # test
    import ipdevide_gen
    testdev = ipdevide_gen.ipdevide_gen(16, 3)#4个IP3组
    print testdev
    for dev in testdev:
        print "dev: %s"%str(dev)
    start = time.time()
    result = ecintersection(*testdev)
    end = time.time()
    print "factor set: %s"%str(result)
    print "cost time: %f"%(end-start)

