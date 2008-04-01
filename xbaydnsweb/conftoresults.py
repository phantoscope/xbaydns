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
from operator import itemgetter

def findFastSpeed(agents,times):
    times=map(lambda x:float(x.strip()),times)
    values=dict(zip(agents,times))
    values_sort=sorted( values.items(), key=itemgetter(1) )
    print "values_sort",values_sort
    return values_sort

def main():
    map(lambda x:x.delete(),Result.objects.all())
    
    for i,r in enumerate(open("/tmp/idcview_out.txt")):
        if i==0:
            agents=r.split(',')
            agents=map(lambda x:x.strip(),agents)
            continue
        r=r.split(',')
        ip,times=r[0],r[1:]
        print ip
        flag={}
        for idc,fasttime in findFastSpeed(agents,times):
            if fasttime==-1.00:continue
            records=Record.objects.filter(idc__alias=idc)
            print records
            for j,record in enumerate(records):
                print record
                flagkey='%s.%s'%(record.name,record.domain)
                print "flagkey",flagkey,flag.get(flagkey,False),j
                if flagkey in flag:
                    if j!=0:
                        #if record.name!=records[j-1].name or record.domain!=records[j-1].domain:
                        if flag.get(flagkey,'')!=records[j-1].idc:
                            print "True:True"
                            continue
                    elif j==0:
                        if flagkey in flag:
                            print "True:True"
                            continue
                print "GOGO"
                Result.objects.create(ip=ip,record=record,idc=record.idc)
                flag[flagkey]=record.idc
    for record in Record.objects.filter(is_defaultidc=True):
        Result.objects.create(ip='any',record=record,idc=record.idc)

if __name__ == '__main__':
    main()

