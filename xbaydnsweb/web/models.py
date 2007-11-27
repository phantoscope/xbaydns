from django.db import models

class Acl(models.Model):
    """Acl Model"""
    aclName = models.CharField(blank=True, maxlength=100)
    aclMatch = models.CharField(blank=True, maxlength=100)
    
    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __str__(self):
        return self.aclName
        
class View(models.Model):
    """View Model"""
    viewName = models.CharField(blank=True, maxlength=100)
    matchClients = models.CharField(blank=True, maxlength=100)
    tsigs = models.CharField(blank=True, maxlength=100)
    
    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __str__(self):
        return self.viewName

class Domain(models.Model):
    """Domain Model"""
    view = models.ForeignKey(View)
    domains = models.CharField(blank=True, maxlength=100)

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __str__(self):
        return "Domain"
