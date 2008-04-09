# encoding: utf-8
from django.utils.translation import gettext_lazy as _
from django.db import models
import traceback
import logging.config
from xbaydns.dnsapi import nsupdate
from django.core import validators
from xbaydnsweb import conftoresults
from xbaydnsweb.web.utils import *

log = logging.getLogger('xbaydnsweb.web.models')

class Domain(models.Model):
    """Domain Model"""
    name = models.CharField(max_length=100,verbose_name=_('domain_name_verbose_name'),help_text='Example:sina.com.cn')

    class Admin:
        list_display = ('name',)
        #search_fields = ('name',)
    class Meta:
        ordering = ('name',)
        verbose_name = _('domain_verbose_name')
        verbose_name_plural = _('domain_verbose_name_plural')
    def __unicode__(self):
        return self.name

class IDC(models.Model):
    """IDC Model"""
    name = models.CharField(max_length=100,verbose_name=_('idc_name_verbose_name'),help_text='Example:西单机房')
    alias = models.CharField(max_length=100,verbose_name=_('idc_alias_verbose_name'),help_text='用于Agent的别名,例如:xd')


    authzcode = models.CharField(max_length=100,blank=True, verbose_name=_('idc_authzcode_verbose_name'))
    pubkey = models.TextField(max_length=1024,blank=True, verbose_name=_('idc_pubkey_verbose_name'))



    class Admin:
        list_display = ('name','alias')
        #search_fields = ('',)
    class Meta:
        ordering = ('name',)
        verbose_name = _('idc_verbose_name')
        verbose_name_plural = _('idc_verbose_name_plural')
    def __unicode__(self):
        return self.name
    
class RecordType(models.Model):
    """Record types"""
    record_type = models.CharField(max_length=10,verbose_name=_('record_type'),help_text='')
    
    class Admin:
        list_display = ('record_type',)
        #search_fields = ('ip','record','idc')
    class Meta:
        ordering = ('record_type',)
        verbose_name = _('record_type_name')
        verbose_name_plural = _('record_type_name_plural')

    def __unicode__(self):
        return self.record_type
    
class Record(models.Model):
    """Record Model"""
    name = models.CharField(max_length=100,verbose_name=_('record_name_verbose_name'),help_text='例如:www')
    domain = models.ForeignKey(Domain,verbose_name=_('record_domain_verbose_name'))
    idc = models.ForeignKey(IDC,verbose_name=_('record_idc_verbose_name'),blank=True)
    record_type = models.ForeignKey(RecordType,verbose_name=_('record_type_name'))
    record_info = models.CharField(max_length=100,verbose_name=_('record_info_name'))
    is_defaultidc = models.BooleanField(default=False,verbose_name=_('record_is_defaultidc_verbose_name'))
    ttl = models.IntegerField(verbose_name=_('record_ttl_verbose_name'))
    
    def save(self):
        super(Record,self).save()
        conftoresults.main()
        saveAllConf()
        
    def delete(self):
        super(Record,self).delete()
        conftoresults.main()
        saveAllConf()
        
    class Admin:
        list_display = ('name','domain','idc','is_defaultidc','record_type','record_info','ttl')
        search_fields = ('name','domain','idc','record_info','record_type')
        fields = (
                (_('record_fields_domaininfo_verbose_name'), {'fields': ('record_type','name','domain','ttl')}),
                (_('record_fields_idcinfo_verbose_name'), {'fields': ('record_info','idc','is_defaultidc',)}),
        )
        #list_filter = ('is_defaultidc', 'idc')
    class Meta:
        ordering = ('name',)
        verbose_name = _('record_verbose_name')
        verbose_name_plural = _('record_verbose_name_plural')
    def __unicode__(self):
        return '%s.%s in %s'%(self.name,self.domain,self.idc)

class Result(models.Model):
    """Result Model"""
    ip = models.IPAddressField(verbose_name=_('result_ip_verbose_name'),help_text='例如:202.101.34.44')
    record = models.ForeignKey(Record,verbose_name=_('result_record_verbose_name'))
    idc = models.ForeignKey(IDC,verbose_name=_('result_idc_verbose_name'))

    class Admin:
        list_display = ('ip','record','idc')
        #search_fields = ('ip','record','idc')
    class Meta:
        ordering = ('record',)
        verbose_name = _('result_verbose_name')
        verbose_name_plural = _('result_verbose_name_plural')
    def __unicode__(self):
        return "%s to %s go %s"%(self.ip,self.record,self.idc)

class IPArea(models.Model):
    """IP Area Management"""
    ip = models.CharField(max_length=100,verbose_name='',help_text='')
    view = models.CharField(max_length=100)
    acl = models.CharField(max_length=100)
    
    class Admin:
        list_display = ('ip','view','acl')
        #search_fields = ('ip','record','idc')
    class Meta:
        ordering = ('view','acl')
        verbose_name = 'IPArea'
        verbose_name_plural = 'IPArea'

    def __unicode__(self):
        return self.ip