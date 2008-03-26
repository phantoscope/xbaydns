#!/opt/local/bin/python2.5
# encoding: utf-8
"""
conftoresults.py

Created by QingFeng on 2008-03-26.
Copyright (c) 2008 xBayDNS Team. All rights reserved.
"""

import os,sys
sys.path.append('/Users/yanxu/python/xbaydns/source/trunk/xbaydns')
sys.path.append(os.path.join('/Users/yanxu/python/xbaydns/source/trunk/xbaydnsweb', '..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'xbaydnsweb.settings'

from xbaydnsweb.web.models import IDC,Result,Record

def main():
    map(lambda x:x.delete(),Result.objects.all())
    
    for r in open("/Users/yanxu/Downloads/idcview_out.txt"):
        r=r.split(',')
        ip,idc=r[0],r[1]
        print ip,idc
        for record in Record.objects.filter(idc__alias=idc):
            result_idc=IDC.objects.get(alias=idc)
            Result.objects.create(ip=ip,record=record,idc=result_idc)

if __name__ == '__main__':
    main()

