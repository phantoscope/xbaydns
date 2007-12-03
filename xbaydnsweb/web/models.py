# encoding: utf-8
from django.db import models
import logging.config

log = logging.getLogger('xbaydnsweb.web.tests')
logging.basicConfig(level=logging.DEBUG)

class Acl(models.Model):
    """Acl Model"""
    aclName = models.CharField(maxlength=100)
    
    class Admin:
        list_display = ('aclName',)
        search_fields = ('aclName',)
    class Meta:
        ordering = ('aclName',)
        verbose_name = 'ACL名称'
        verbose_name_plural = 'ACL名称管理'
        
    def __str__(self):
        return self.aclName

class AclMatch(models.Model):
    """AclMatch Model"""
    acl = models.ForeignKey(Acl)
    aclMatch = models.CharField(maxlength=100)

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
    viewName = models.CharField(maxlength=100,verbose_name='View名称')
    viewgroup = models.ForeignKey("ViewGroup")
    
    class Admin:
        list_display = ('viewName','viewgroup')
        search_fields = ('viewName',)
    class Meta:
        ordering = ('viewName',)
        verbose_name = 'View'
        verbose_name_plural = 'View管理'

    def __str__(self):
        return self.viewName

class ViewMatchClient(models.Model):
    """ViewMatch Model"""
    view = models.ForeignKey(View)
    viewMatch = models.CharField(maxlength=100,verbose_name='IP地址')

    class Admin:
        list_display = ('view','viewMatch')
        search_fields = ('',)
    class Meta:
        verbose_name = 'MatchClient'
        verbose_name_plural = 'View MatchClient管理'

    def __str__(self):
        return "ViewMatch"
        
class ViewTsig(models.Model):
    """ViewTsig Model"""
    view = models.ForeignKey(View)
    tsig = models.CharField(maxlength=100)

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
    view = models.ManyToManyField(View)
    zone = models.CharField(maxlength=100)

    class Admin:
        list_display = ('zone',)
        search_fields = ('',)
    class Meta:
        verbose_name = 'Zone'
        verbose_name_plural = 'Zone管理'

    def __str__(self):
        return self.zone

class ViewGroup(models.Model):
    """ViewGourp"""
    name = models.CharField(maxlength=100)

    class Admin:
        list_display = ('name',)
        search_fields = ('name',)
    class Meta:
        verbose_name = 'ViewGroup'
        verbose_name_plural = 'View Group管理'

    def __str__(self):
        return self.name

class Record(models.Model):
    """Record"""
    view = models.ForeignKey(View)
    domain = models.CharField(maxlength=100)
    record = models.CharField(maxlength=100)
    recordgroup = models.ForeignKey("RecordGroup")

    class Admin:
        list_display = ('domain',)
        search_fields = ('domain',)

    def __str__(self):
        return "Record"

class RecordGroup(models.Model):
    """RecordGroup"""
    name = models.CharField(maxlength=100)

    class Admin:
        list_display = ('name',)
        search_fields = ('name',)

    def __str__(self):
        return "RecordGroup"

class ViewMatch(models.Model):
    """ViewMatch"""
    name = models.CharField(maxlength=100)
    viewgroup = models.ManyToManyField(ViewGroup)
    recordgroup = models.ManyToManyField(RecordGroup)

    class Admin:
        list_display = ('name',)
        search_fields = ('name',)
    class Meta:
        verbose_name = 'ViewMatch'
        verbose_name_plural = 'View Match管理'

    def __str__(self):
        return "ViewMatch"
