from django.db import models

class Acl(models.Model):
    """Acl Model"""
    aclName = models.CharField(blank=True, maxlength=100)
    
    class Admin:
        list_display = ('aclName',)
        search_fields = ('',)

    def __str__(self):
        return self.aclName
        
class AclMatch(models.Model):
    """AclMatch Model"""
    acl = models.ForeignKey(Acl)
    aclMatch = models.CharField(blank=True, maxlength=100)

    class Admin:
        list_display = ('acl','aclMatch')
        search_fields = ('',)

    def __str__(self):
        return "AclMatch"

class View(models.Model):
    """View Model"""
    viewName = models.CharField(blank=True, maxlength=100)
    
    class Admin:
        list_display = ('viewName',)
        search_fields = ('',)

    def __str__(self):
        return self.viewName

class ViewMatch(models.Model):
    """ViewMatch Model"""
    view = models.ForeignKey(View)
    viewMatchClient = models.CharField(blank=True, maxlength=100)

    class Admin:
        list_display = ('view','viewMatchClient')
        search_fields = ('',)

    def __str__(self):
        return "ViewMatch"
        
class ViewTsig(models.Model):
    """ViewTsig Model"""
    view = models.ForeignKey(View)
    tsig = models.CharField(blank=True, maxlength=100)

    class Admin:
        list_display = ('view','tsig')
        search_fields = ('',)

    def __str__(self):
        return "ViewTsig"

class Domain(models.Model):
    """Domain Model"""
    view = models.ForeignKey(View)
    domain = models.CharField(blank=True, maxlength=100)

    class Admin:
        list_display = ('view','domain')
        search_fields = ('',)

    def __str__(self):
        return "Domain"
