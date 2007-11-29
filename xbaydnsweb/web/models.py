# encoding: utf-8
from django.db import models
from xbaydns.conf import sysconf
from xbaydns.tools.namedconf import *
import logging.config

log = logging.getLogger('xbaydnsweb.web.tests')
logging.basicConfig(level=logging.DEBUG)

class Acl(models.Model):
    """Acl Model"""
    aclName = models.CharField(blank=True, maxlength=100)
    
    class Admin:
        list_display = ('aclName',)
        search_fields = ('aclName',)
    class Meta:
        ordering = ('aclName',)
        verbose_name = 'ACL名称'
        verbose_name_plural = 'ACL名称管理'
        
    def __str__(self):
        return self.aclName
        
    def saveConf(self,path=sysconf.namedconf):
        nc = NamedConf()
        matchs=map(lambda x:x.aclMatch,
                AclMatch.objects.filter(
                    acl__aclName=self.aclName))
        nc.addAcl(self.aclName,matchs)
        nc.save(path)

    @staticmethod
    def saveAllConf(path=sysconf.namedconf):
        nc = NamedConf()
        for acl in Acl.objects.all():
            matchs=map(lambda x:x.aclMatch,AclMatch.objects.filter(acl=acl))
            nc.addAcl(acl.aclName,matchs)
        nc.save(path)
    
class AclMatch(models.Model):
    """AclMatch Model"""
    acl = models.ForeignKey(Acl)
    aclMatch = models.CharField(blank=True, maxlength=100)

    class Admin:
        list_display = ('acl','aclMatch')
        search_fields = ('',)
    class Meta:
        verbose_name = 'ACL'
        verbose_name_plural = 'ACL管理'

    def __str__(self):
        return "AclMatch"

class View(models.Model):
    """View Model"""
    viewName = models.CharField(blank=True, maxlength=100)
    
    class Admin:
        list_display = ('viewName',)
        search_fields = ('viewName',)
    class Meta:
        ordering = ('viewName',)
        verbose_name = 'View名称'
        verbose_name_plural = 'View名称管理'

    def __str__(self):
        return self.viewName

class ViewMatch(models.Model):
    """ViewMatch Model"""
    view = models.ForeignKey(View)
    viewMatchClient = models.CharField(blank=True, maxlength=100)

    class Admin:
        list_display = ('view','viewMatchClient')
        search_fields = ('',)
    class Meta:
        verbose_name = 'View'
        verbose_name_plural = 'View管理'

    def __str__(self):
        return "ViewMatch"
        
class ViewTsig(models.Model):
    """ViewTsig Model"""
    view = models.ForeignKey(View)
    tsig = models.CharField(blank=True, maxlength=100)

    class Admin:
        list_display = ('view','tsig')
        search_fields = ('',)
    class Meta:
        verbose_name = 'View Tsig'
        verbose_name_plural = 'View Tsig管理'

    def __str__(self):
        return "ViewTsig"

class Domain(models.Model):
    """Domain Model"""
    view = models.ForeignKey(View)
    domain = models.CharField(blank=True, maxlength=100)

    class Admin:
        list_display = ('view','domain')
        search_fields = ('domain',)
    class Meta:
        verbose_name = 'Zone'
        verbose_name_plural = 'Zone管理'

    def __str__(self):
        return "Domain"
