#!/usr/bin/env python
# encoding: utf-8
"""
dbset.py

Created by Razor <bg1tpt AT gmail.com> on 2008-03-31
Copyright (c) 2008 xBayDNS Team. All rights reserved.

"""

import bsddb, pickle, os

class Set():

    def __init__(self):
        self._dbname = os.tmpnam()
        try:
            self._dbobj = bsddb.btopen(self._dbname)
        except:
            pass

    def add(self, element):
        if element == None:
            return False
        element_str = pickle.dumps(element)
        print type(element_str)
        self._dbobj[element_str] = '1'
        return True
    
    def __getitem__(self, element):
        if element == None:
            return False
        element_str = pickle.dumps(element)
        return self._dbobj[element_str]
