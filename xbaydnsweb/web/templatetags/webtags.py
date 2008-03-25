# encoding: utf-8
"""
webtags.py

Created by QingFeng on 2008-03-23.
Copyright (c) 2008 xBayDNS Team. All rights reserved.
"""

from django import template

register = template.Library()

@register.simple_tag
def resultToHtml(results):
    print results
    html=''
    for record,idcs in results.items():
        s='%s'%record
        for idc,ips in idcs.items():
            s+='-%s:%s'%(idc,','.join(ips))
        html+='<li>%s</li>'%s
    return '<ul>%s</ul>'%html
