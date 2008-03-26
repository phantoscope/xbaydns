# encoding: utf-8
from django.utils.translation import gettext_lazy as _
from django.db import models
import logging.config
from xbaydns.dnsapi import nsupdate

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

    class Admin:
        list_display = ('name','alias')
        #search_fields = ('',)
    class Meta:
        ordering = ('name',)
        verbose_name = _('idc_verbose_name')
        verbose_name_plural = _('idc_verbose_name_plural')
    def __unicode__(self):
        return self.name

class Record(models.Model):
    """Record Model"""
    name = models.CharField(max_length=100,verbose_name=_('record_name_verbose_name'),help_text='例如:www')
    domain = models.ForeignKey(Domain,verbose_name=_('record_domain_verbose_name'))
    idc = models.ForeignKey(IDC,verbose_name=_('record_idc_verbose_name'))
    ip = models.IPAddressField(verbose_name=_('record_ip_verbose_name'),help_text='例如:202.101.34.44')
    
    def save(self):
        try:
            nsupobj = nsupdate.NSUpdate('127.0.0.1',str(self.domain),view=self.idc.alias)
            #['foo', 3600, 'IN', 'A', ['192.168.1.1', '172.16.1.1']]#record style
            add_data=[[self.name,3600,'IN','A',[self.ip,]],]
            if self.id!=None:
                old_r=Record.objects.get(id=self.id)
                del_data=[[old_r.name,3600,'IN','A',[old_r.ip,]],]
                nsupobj.removeRecord(del_data)
            nsupobj.addRecord(add_data)
            nsupobj.commitChanges()
        except:
            print "NSUpdate Error!"
        super(Record,self).save()
    def delete(self):
        try:
            nsupobj = nsupdate.NSUpdate('127.0.0.1',str(self.domain),view=self.idc.alias)
            del_data=[[self.name,3600,'IN','A',[self.ip,]],]
            #['foo', 3600, 'IN', 'A', ['192.168.1.1', '172.16.1.1']]#record style
            nsupobj.removeRecord(del_data)
            nsupobj.commitChanges()
        except:
            print "NSUpdate Error!"
        super(Record,self).delete()
    class Admin:
        list_display = ('name','domain','idc','ip')
        search_fields = ('name','domain','idc','ip')
        fields = (
                (_('record_fields_domaininfo_verbose_name'), {'fields': ('name','domain',)}),
                (_('record_fields_idcinfo_verbose_name'), {'fields': ('ip','idc',)}),
        )
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


