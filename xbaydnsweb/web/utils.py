#!/usr/bin/env python
# encoding: utf-8
"""
utils.py

Created by QingFeng on 2007-12-02.
Copyright (c) 2007 yanxu. All rights reserved.
"""
import logging.config
from xbaydnsweb.web.models import *
from xbaydns.tools.namedconf import *

log = logging.getLogger('xbaydnsweb.web.utils')
logging.basicConfig(level=logging.DEBUG)

def saveAllConf(path):
    nc = NamedConf()
    for acl in Acl.objects.all():
        matchs=map(lambda x:x.aclMatch,
                AclMatch.objects.filter(acl=acl))
        nc.addAcl(acl.aclName,matchs)
    for view in View.objects.all():
        view_matchs=map(lambda x:x.viewMatchClient,
                ViewMatch.objects.filter(view=view))
        tsig_matchs=map(lambda x:x.tsig,
                ViewTsig.objects.filter(view=view))
        nc.addView(view.viewName,view_matchs,tsig_matchs)
    for domain in Domain.objects.all():
        domain_matchs=map(lambda x:x.viewMatchClient,
                ViewMatch.objects.filter(view=view))
        nc.addDomain(view.viewName,domain_matchs)
    nc.save(path)
