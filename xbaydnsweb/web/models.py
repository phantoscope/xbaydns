# encoding: utf-8
from django.utils.translation import gettext_lazy as _
from django.db import models
import logging.config
from xbaydns.dnsapi import nsupdate

log = logging.getLogger('xbaydnsweb.web.models')

class Domain(models.Model):
    """Domain Model"""
    name = models.CharField(max_length=100,verbose_name='域名',help_text='Example:sina.com.cn')

    class Admin:
        list_display = ('name',)
        #search_fields = ('name',)
    class Meta:
        ordering = ('name',)
        verbose_name = _('domain_verbose_name')
        verbose_name_plural = '1.1 '+str(_('domain_verbose_name_plural'))
    def __unicode__(self):
        return self.name

class IDC(models.Model):
    """IDC Model"""
    name = models.CharField(max_length=100,verbose_name='名称',help_text='Example:西单机房')
    alias = models.CharField(max_length=100,verbose_name='别名',help_text='用于Agent的别名,例如:xd')

    class Admin:
        list_display = ('name','alias')
        #search_fields = ('',)
    class Meta:
        ordering = ('name',)
        verbose_name = _('idc_verbose_name')
        verbose_name_plural = '1.2 '+str(_('idc_verbose_name_plural'))
    def __unicode__(self):
        return self.name

class Record(models.Model):
    """Record Model"""
    name = models.CharField(max_length=100,verbose_name='名称',help_text='例如:www')
    domain = models.ForeignKey(Domain,verbose_name='所属域名')
    idc = models.ForeignKey(IDC,verbose_name='所属机房')
    ip = models.IPAddressField(verbose_name='解析IP',help_text='例如:202.101.34.44')
    
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
                ('域名信息', {'fields': ('name','domain',)}),
                ('机房信息', {'fields': ('ip','idc',)}),
        )
    class Meta:
        ordering = ('name',)
        verbose_name = _('record_verbose_name')
        verbose_name_plural = '1.3 '+str(_('record_verbose_name_plural'))
    def __unicode__(self):
        return '%s.%s in %s'%(self.name,self.domain,self.idc)

class Result(models.Model):
    """Result Model"""
    ip = models.IPAddressField(verbose_name='来源IP',help_text='例如:202.101.34.44')
    record = models.ForeignKey(Record,verbose_name='访问记录')
    idc = models.ForeignKey(IDC,verbose_name='访问机房')

    class Admin:
        list_display = ('ip','record','idc')
        #search_fields = ('ip','record','idc')
    class Meta:
        ordering = ('record',)
        verbose_name = _('result_verbose_name')
        verbose_name_plural = '1.4 '+str(_('result_verbose_name_plural'))
    def __unicode__(self):
        return "%s to %s go %s"%(self.ip,self.record,self.idc)


