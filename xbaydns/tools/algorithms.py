#!/usr/bin/env python
# encoding: utf-8
"""
algorithms.py

Created by Razor <bg1tpt AT gmail.com> on 2008-03-22.
Copyright (c) 2008 xBayDNS Team. All rights reserved.

"""

def ecintersection(*devides):
    if len(devides) == 0:
        return 1
    
    # construct complete set
    complete_set = set()
    for ec in devides[0]:
        for element in ec:
            complete_set.add(element)
    
    ec_array = []
    ec_dict_template = {}
    # construct ec dictionary templete
    for element in complete_set:
        ec_dict_template[element] = set()
    
    # construct ec for every element from the factor set
    for devide in devides:
        ec_dict = ec_dict_template.copy()
        for ec in devide:
            ec_set = set()
            for element in ec:
                ec_set.add(element)
            for element in ec:
                ec_dict[element] = ec_dict[element].union(ec_set)
        ec_array.append(ec_dict)

    # get the intersection of every element's ec
    ec_insect = {}
    for element in complete_set:
        for ec_dict in ec_array:
            try:
                ec_insect[element]
            except KeyError:
                ec_insect[element] = ec_dict[element]
                continue
            ec_insect[element].intersection_update(ec_dict[element])
    #print ec_insect

    # convert to factor set
    factor_set = []
    i = 0
    for ec in ec_insect.itervalues():
        try:
            if factor_set[i - 1] == ec:
                continue
        except IndexError:
            pass
        factor_set.append(ec)
        i += 1
    #print factor_set
    return factor_set

# test
#ecintersection([[0,1], [2,3,4], [5]], [[0],[1,2], [3,4], [5]])
