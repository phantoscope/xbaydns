# encoding: utf-8
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core import validators
from xbaydns.dnsapi import nsupdate
from xbaydnsweb import conftoresults
from datetime import datetime
import traceback
import logging.config
import re,hashlib,time

log = logging.getLogger('xbaydnsweb.web.models')

class Domain(models.Model):
    """Domain Model"""
    name = models.CharField(max_length=100,verbose_name=_('domain_name_verbose_name'),help_text='Example:sina.com.cn')
    default_ns = models.CharField(max_length=100,verbose_name='默认NS',help_text='ns1.sina.com.cn')
    idc = models.ForeignKey('IDC',verbose_name=_('record_idc_verbose_name'))
    record_info = models.CharField(max_length=100,verbose_name=_('record_info_name'))
    mainter = models.CharField(max_length=100,verbose_name='',help_text='')
    ttl = models.IntegerField(max_length=100,verbose_name='TTL',help_text='3600')

    def save(self):
        from xbaydnsweb.web.utils import *
        super(Domain,self).save()
        rt=RecordType.objects.get(record_type='NS')
        Record.objects.create(name=self.default_ns,domain=self,record_type=rt,
                            record_info=self.record_info,ttl=self.ttl,idc=self.idc)
        saveAllConf()
    def delete(self):
        from xbaydnsweb.web.utils import *
        super(Domain,self).delete()
        saveAllConf()
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


    authzcode = models.CharField(max_length=1024, blank=True,verbose_name=_('idc_authzcode_verbose_name'))
    pubkey = models.TextField(max_length=1024,blank=True, verbose_name=_('idc_pubkey_verbose_name'))
    regtime = models.DateTimeField(blank=True, null=True, verbose_name=_('idc_regtime_verbose_name'))

    class Admin:
        list_display = ('name','alias', 'authzcode', 'regtime')
        #search_fields = ('',)
        fields = (
               (_('idc_verbose_name'), {'fields': ('name','alias')}),
        )

    class Meta:
        ordering = ('name',)
        verbose_name = _('idc_verbose_name')
        verbose_name_plural = _('idc_verbose_name_plural')

    def save(self):
        from xbaydnsweb.web.utils import *
        tohash = "%s%f" % (self.alias, time.time())
        self.authzcode = hashlib.sha1(tohash).hexdigest()
        self.pubkey = ''
        super(IDC,self).save()

    def regsave(self):
        self.regtime = datetime.now()
        super(IDC,self).save()

    def __unicode__(self):
        return self.name

class Node(models.Model):
    """ Node Model """
    name = models.CharField(max_length=100, verbose_name=_('node_name_verbose_name'))
    codename = models.CharField(max_length=100, verbose_name=_('node_codename_verbose_name'))
    ip = models.CharField(max_length=100, verbose_name=_('node_ip_verbose_name'))
    type = models.CharField(max_length=32, blank=True,verbose_name=_('node_type_verbose_name'))
    authzcode = models.CharField(max_length=1024, blank=True,verbose_name=_('node_authzcode_verbose_name'))
    pubkey = models.TextField(max_length=1024,blank=True, verbose_name=_('node_pubkey_verbose_name'))
    regtime = models.DateTimeField(blank=True, null=True, verbose_name=_('node_regtime_verbose_name'))

    class Admin:
        list_display = ('name','codename', 'authzcode', 'regtime')
        fields = (
               (_('node_verbose_name'), {'fields': ('name','codename','ip')}),
        )

    class Meta:
        ordering = ('name',)
        verbose_name = _('node_verbose_name')
        verbose_name_plural = _('node_verbose_name_plural')

    def save(self):
        from xbaydnsweb.web.utils import *
        self.type = 'slave'
        tohash = "%s%f" % (self.codename , time.time())
        self.authzcode = hashlib.sha1(tohash).hexdigest()
        self.pubkey = ''
        super(Node,self).save()
        update_allow_transfer(self.ip)

    def regsave(self):
        self.regtime = datetime.now()
        super(Node,self).save()

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
    
class IPArea(models.Model):
    """IP Area Management"""
    ip = models.TextField(verbose_name='',help_text='')
    view = models.CharField(max_length=100)
    acl = models.CharField(max_length=100)
    service_route = models.TextField(verbose_name='service_route',help_text='')
    
    class Admin:
        list_display = ('ip','view','acl','service_route')
        #search_fields = ('ip','record','idc')
    class Meta:
        ordering = ('view','acl')
        verbose_name = 'IPArea'
        verbose_name_plural = 'IPArea'

    def __unicode__(self):
        return self.ip

def isValiableRInfo(field_data,all_data):
    r_type = RecordType.objects.get(id=all_data['record_type'])
    if r_type == 'A':
        ipv4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
        ipv4_re.match(str(field_data), 1)  
    elif r_type == 'CNAME':
        try:
            name = field_data[:field_data.index('.')]
            domain = field_data[field_data.index('.')+1:]
            
            if len(Record.objects.filter(name=name,domain__name=domain)) == 0:
                raise validators.ValidationError("field synax error")
        except:
            raise validators.ValidationError("field synax error")
    elif r_type == 'A':
        pass

def isDuplicateRecord(field_data,all_data):
    if len(Record.objects.filter(name=str(all_data['name']),domain__id=str(all_data['domain']),idc__id=str(all_data['idc']),\
                          record_type__id=str(all_data['record_type']),record_info=str(all_data['record_info']))) >0:
        raise validators.ValidationError(_("duplicate_record"))
    
class Record(models.Model):
    """Record Model"""
    name = models.CharField(max_length=100,verbose_name=_('record_name_verbose_name'),help_text='例如:www',validator_list=[isDuplicateRecord])
    domain = models.ForeignKey(Domain,verbose_name=_('record_domain_verbose_name'))
    idc = models.ForeignKey(IDC,verbose_name=_('record_idc_verbose_name'))
    record_type = models.ForeignKey(RecordType,verbose_name=_('record_type_name'))
    record_info = models.CharField(max_length=100,verbose_name=_('record_info_name'))
    is_defaultidc = models.BooleanField(default=False,verbose_name=_('record_is_defaultidc_verbose_name'))
    ttl = models.IntegerField(verbose_name=_('record_ttl_verbose_name'))

    def save(self):
        from xbaydnsweb.web.utils import *
        from xbaydns.conf import sysconf
        super(Record,self).save()
        try:
            if self.idc.alias not in getDetectedIDC() or self.record_type.record_type != 'A':
                for iparea in IPArea.objects.all():
                    self.viewname = iparea.view
                    record_nsupdate(self)
            else:
                if len(Result.objects.filter(idc__alias=self.idc.alias)) == 0:
                    conftoresults.main()
                    saveAllConf()
                else:
                    if len(Record.objects.filter(name=self.name,domain=self.domain,idc=self.idc))==0:
                        conftoresults.main()
                        saveAllConf()
                    else:
                        for iparea in IPArea.objects.all():
                            if ("%s.%s"%(self.name,self.domain),self.idc.alias) in list(eval(iparea.service_route)):
                                self.viewname = iparea.view
                                record_nsupdate(self) 
           
            if self.is_defaultidc == True:
                self.viewname="view_default"
                record_nsupdate(self)
        except:
            super(Record,self).delete()
            print traceback.print_exc()

    def delete(self):
        from xbaydnsweb.web.utils import *
        if len(Record.objects.filter(record_type__record_type='NS',domain=self.domain))==1:
            return 
        if self.is_defaultidc == True:
                self.viewname="view_default"
                record_delete(self)
        if len(Result.objects.filter(idc__alias=self.idc.alias)) != 0:
            if len(Record.objects.filter(name=self.name,domain=self.domain,idc=self.idc))==1:
                conftoresults.main()
                saveAllConf()
            else:
                for iparea in IPArea.objects.all():
                    if ("%s.%s"%(self.name,self.domain),self.idc.alias) in list(eval(iparea.service_route)):
                        self.viewname = iparea.view
                        record_delete(self)
        else:
            for iparea in IPArea.objects.all():
                self.viewname = iparea.view
                record_delete(self)
        super(Record,self).delete()
        
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
    record = models.CharField(max_length=200,verbose_name=_('result_record_verbose_name'))
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

