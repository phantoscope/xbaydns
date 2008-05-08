# encoding: utf-8
"""
namedconf.py

Created by QingFeng on 2007-11-22.
Copyright (c) 2007 yanxu. All rights reserved.
"""

import logging.config
import base64
import os,tempfile,time
from xbaydns.conf import sysconf

log = logging.getLogger('xbaydns.tools.namedconf')

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
        self.unchanged_view_list=[]
        
    def addViewUnChanged(self,unchanged_hash_list):
        self.unchanged_view_list = map(lambda x:'view_view%s'%x,unchanged_hash_list)
        
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
    def addView(self,view,slaves,matchClient=[]):
        tsig='%s-view-key'%view
        if len(matchClient)>0:
            matchClient=map(lambda x:'"%s";'%x,matchClient)
            matchClient=''.join(matchClient)
        else:
            matchClient=''
        keys='''
key "%s" {
    algorithm hmac-md5;
    secret "%s";
};
'''
        keys=keys%(tsig,self.genSecret(tsig))
        key_tsig='key "%s"'%tsig
        s='''view "%s" { match-clients { %s%s; }; %%s };
        '''%(view,matchClient,key_tsig)
        for slave in slaves:
            server='''server %s { keys "%s"; };
            '''%(slave,tsig)
            s = s + server
        self.views[view]=keys+s
        return keys+s
    
    '''
    update view(view,match-client) 更新view 

    参数说明： 
    view 增加的view的名称 
    match-client 匹配于该view的acl汇总
    '''
    def updateView(self,view,matchClient=[]):
        return self.addView(view,matchClient)
    
    def genSecret(self,key):
        return base64.b64encode(key)
    '''
    load view(view,match-client) 更新view 

    参数说明： 
    view 增加的view的名称 
    match-client 匹配于该view的acl汇总
    '''
    def loadViewKey(self,view):
        key='%s-view-key'%view
        return {key:self.genSecret(key)}
    
    '''
    del view(view) 删除view 

    参数说明： 
    view 要删除的view的名称
    '''
    def delView(self,view):
        if view in self.views:
            del self.views[view]
            return True
        return False
       
    '''
    add domain(domain) 增加一个DNS域。
    '''
    def addDomain(self,domain=[]):
        cmds='include "defaultzone.conf";'
        for view in self.views.keys():
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
                    include = 'include "defaultzone.conf";'
                    self.domains[view]={'defaultzone':include}
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
    def getSerial(self,zonefilepath):
        import traceback
        from dns import zone,rdatatype,rdataset,rdata
        try:
            zoneinfo = zone.from_file(zonefilepath,check_origin=False)
            soaset = zoneinfo.get_rdataset(zoneinfo.origin,rdatatype.SOA)
            if len(soaset) > 0:
                return soaset[0].serial + 1
        except:
            d=int(time.time())
            return '%s'%(d)
    
    '''
    del domain(domain) 删除一个DNS域 
    参数说明： 
        domain 需要删除的DNS域名
    '''
    def delDomain(self,domain):
        for view in self.domains.keys():
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
            f = open(pathname,'w')
            f.write(v)
            f.close()
        
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
            f = open(pathname,'w')
            f.write(value)
            f.close()
            
    def checkDefaultDomain(self,file):
        try:
            os.stat(file)
            return True
        except:
            return False
    
    '''
    保存view中声名的zone文件
    '''
    @pathIsExists       
    def __saveDomains(self,path=sysconf.namedconf):
        from xbaydnsweb.web.models import Domain,Record
        for view,domains in self.domains.items():
            if view not in self.unchanged_view_list:
                for domain,value in domains.items():
                    if domain=='defaultzone':continue
                    zonefilepath=os.path.join(path,"%s"
                            %self.getDomainFileName(domain,view))
                    if view == 'viewdefault' and checkDefaultDomain(zonefilepath) == True:
                        continue
                    f=open(zonefilepath,"w")
                    domain_admin=sysconf.default_admin
                    domain_ttl='3600'
                    info=Domain.objects.filter(name=domain)
                    nsrecord=Record.objects.filter(domain=info[0],record_type__record_type='NS')
                    nsareords=[]
                    filtered_ns = {}
                    for ns in nsrecord:
                        try:
                            r_name = ns.record_info[:ns.record_info.index('.')]
                        except:
                            r_name = ns.record_info
                        filtered_ns.update({"%s%s%s%s"%(ns.record_type.record_type,ns.name,ns.domain.name,ns.idc):ns})
                        nsareords.extend(Record.objects.filter(name=r_name,domain=ns.domain,record_type__record_type='A'))
                    allnsinfo='\n'.join( map(lambda x:'%s            NS    %s'%(x.name,x.record_info),filtered_ns.values()) )
                    allnsainfo='\n'.join( map(lambda x:'%s            A    %s'%(x.name,x.record_info),nsareords) )
                    domain_admin=str(info[0].mainter)
                    domain_ttl=str(info[0].ttl)
    
                    zonedata='''$ORIGIN %(domain)s.
$TTL %(ttl)s    ;10 minute
%(domain)s. IN SOA %(soa)s. %(admin)s. (
                %(time)s	; serial
                60		    ; refresh (1 minute)
                3600	    ; retry (1 hour)
	            604800	    ; expire (1 week)
	            3600	    ; minimum (1 hour)
	    )
%(ns)s
%(nsa)s
'''%{'domain':domain,'time':self.getSerial(zonefilepath),
                     'ns':allnsinfo,'soa':sysconf.default_soa,
                     'admin':domain_admin,'ttl':domain_ttl,'nsa':allnsainfo}
                    f.write(zonedata)
                    f.close()
        dpath=os.path.join(sysconf.chroot_path,sysconf.namedconf,'dynamic')
        os.system("chown -R %s:wheel %s"%(sysconf.named_user,dpath))
    
    def convAclViewResult(self):
        """将acl_include顺序化"""
        acls, views, acl_default, view_default = [],[],[],[]
        for conf in self.acl_include:
            if conf.find('default')!=-1:
                if conf.find('acl')!=-1:
                    acl_default.append(conf)
                elif conf.find('view')!=-1:
                    view_default.append(conf)
            elif conf.find('acl')!=-1:
                acls.append(conf)
            elif conf.find('view')!=-1:
                views.append(conf)
        return acls+acl_default+views+view_default

    '''
    保存acldef.conf文件,保存所有生成的include语句
    '''
    @pathIsExists
    def __saveAcldef(self,path):
        acl_file=os.path.join(
                path,sysconf.filename_map['acl'])
        new_include=self.convAclViewResult()
        f = open(acl_file,'w')
        f.write('\n'.join(new_include))
        f.close()
    '''
    保存acl和views的配置文件
    ''' 
    def save(self,path=sysconf.namedconf):
        self.__saveAcls(path)
        self.__saveViews(path)
        self.__saveDomains(path)
        self.__saveAcldef(path)

    def reload(self):
        """重新加载配置文件，返回0为成功"""
        return os.system("rndc reload")

    def check_configfile(self):
        """检查生成的named.conf的配置正确，返回0为正确"""
        return os.system("named-checkconf -z")

    def named_restart(self):
        """重启named"""
        os.system(sysconf.namedstop)
        return os.system(sysconf.namedstart)
