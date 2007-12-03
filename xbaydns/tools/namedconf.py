# encoding: utf-8
"""
namedconf.py

Created by QingFeng on 2007-11-22.
Copyright (c) 2007 yanxu. All rights reserved.
"""

import logging.config
import os,tempfile,datetime
from xbaydns.conf import sysconf

log = logging.getLogger('xbaydns.tests.namedconftest')
logging.basicConfig(level=logging.DEBUG)

def pathIsExists(func):
    def mkconfdir(path,childpath):
        try:
            path_all=os.path.join(path,childpath)
            os.stat(path_all)
        except OSError:
            os.mkdir(path_all)
    def wrapper(*args):
        path=args[1]
        mkconfdir(path,'acl/')
        mkconfdir(path,'view/')
        mkconfdir(path,'dynamic/')
        func(args[0],args[1])
    return wrapper

class NamedConf(object):
    def __init__(self):
        self.acls={}
        self.views={}
        self.domains={}
        self.acl_include=[]
    '''
    add acl (acl,aclmatch) 增加一个acl 
    参数说明： 
    acl 要增加的acl的名称 
    aclmatech 增加的acl中的match地址
    '''
    def addAcl(self,acl,aclmatch):
        s='''
            acl "%s" { %s; };
        '''%(acl,';'.join(aclmatch))
        self.acls[acl]=s
        return s
        
    '''
    del acl(acl) 删除一个acl 

    参数说明： 
    acl 要删除的acl的名称
    '''
    def delAcl(self,acl):
        if acl in self.acls:
            del self.acls[acl]
            return True
        return False
    
    '''
    add view(view,match-client) 

    增加view 

    参数说明： 
    view 增加的view的名称 
    match-client 匹配于该view的acl汇总
    '''
    def addView(self,view,matchClient=[],tsig=[]):
        tsig=map(lambda x:'key %s'%x,tsig)
        s='''view "%s" { match-clients { %s; }; %%s };
        '''%(view,';'.join(matchClient+tsig))
        self.views[view]=s
        return s
    
    '''
    update view(view,match-client) 更新view 

    参数说明： 
    view 增加的view的名称 
    match-client 匹配于该view的acl汇总
    '''
    def updateView(self,view,matchClient=[],tsig=[]):
        return self.addView(view,matchClient,tsig)
    
    '''
    load view(view,match-client) 更新view 

    参数说明： 
    view 增加的view的名称 
    match-client 匹配于该view的acl汇总
    '''
    def loadViewKey(self,view):
        import base64
        return base64.b64encode('%s-key'%view)
    
    '''
    del view(view) 删除view 

    参数说明： 
    view 增加的view的名称
    '''
    def delView(self,view):
        if view in self.views:
            del self.views[view]
            return True
        return False
       
    '''
    add domain(view,domain) 增加一个DNS域。
    '''
    def addDomain(self,view,domain=[]):
    	cmds=''
        for d in domain:
            fname=self.getDomainFileName(d,view)
            s='''
                zone "%(domain)s" {
                    type master;
                    file "%(fname)s";
                };'''%{'domain':d,
                       'fname':fname}
            cmds+=s
            if view not in self.domains:
                self.domains[view]={}
            self.domains[view].update({d:s})
        return cmds
    '''
    获得zone文件名
    '''
    def getDomainFileName(self,domain,view):
        return "dynamic/%(view)s.%(domain)s.file"%{'domain':domain,'view':view}
    '''
    获取Serial
    '''
    def getSerial(self):
        d=datetime.datetime.now()
        return '%s%s%s01'%(d.year,str(d.month).zfill(2),str(d.day).zfill(2))
    
    '''
    del domain(view,domain) 删除一个DNS域 
    参数说明： 
        view   对应的view名
        domain 需要删除的DNS域名
    '''
    def delDomain(self,view,domain):
        if view in self.domains:
            if domain in self.domains[view]:
                del self.domains[view][domain]
                return True
        return False
    
    '''
    用于校验生成出的配置文件
    '''
    def __checkfile(self):
        pass
        
    '''
    cp正确的文件到指定位置
    '''
    def __cpfile(self):
        pass
    
    '''
    保存所有acl配置文件
    '''
    @pathIsExists
    def __saveAcls(self,path=sysconf.namedconf):
        for k,v in self.acls.items():
            fname=os.path.join('acl/',k+'.conf')
            pathname=os.path.join(path,fname)
            self.acl_include.append('include "%s";'%fname)
            open(pathname,'w').write(v)
        
    '''
    保存所有view配置文件
    '''
    @pathIsExists
    def __saveViews(self,path=sysconf.namedconf):
        for k,v in self.views.items():
            fname=os.path.join('view/',k+'.conf')
            pathname=os.path.join(path,fname)
            self.acl_include.append('include "%s";'%fname)
            value = ''
            if k in self.domains:
                value = v%'\n'.join(self.domains[k].values())
            else:
                value = v%''
            open(pathname,'a').write(value)
            
    '''
    保存view中声名的zone文件
    '''
    @pathIsExists       
    def __saveDomains(self,path=sysconf.namedconf):
        for view,domains in self.domains.items():
            for domain,value in domains.items():
                f=open(os.path.join(path,"%s"
                        %self.getDomainFileName(domain,view)),"w")
                zonedata='''
                $ORIGIN .
                $TTL 3600       ; 1 hour
                %(domain)s IN SOA  %(soa)s (
                            %(time)s ; serial
                            60         ; refresh (1 minute)
                            3600       ; retry (1 hour)
                            604800     ; expire (1 week)
                            3600       ; minimum (1 hour)
                            )
                %(domain)s  IN      NS      %(ns)s
                '''%{'domain':domain,'time':self.getSerial(),
                     'ns':sysconf.default_ns,'soa':sysconf.default_soa}
                f.write(zonedata)
                f.close()
    
    '''
    保存acldef.conf文件,保存所有生成的include语句
    '''
    @pathIsExists
    def __saveAcldef(self,path):
        acl_file=os.path.join(
                path,sysconf.filename_map['acl'])
        open(acl_file,'w').write('\n'.join(self.acl_include))
    '''
    保存acl和views的配置文件
    ''' 
    def save(self,path=sysconf.namedconf):
        self.__saveAcls(path)
        self.__saveViews(path)
        self.__saveDomains(path)
        self.__saveAcldef(path)