from django.db import models
from django import newforms as forms
from django.newforms import form_for_model
from xbaydnsweb.web.models import ViewMatch

class SmartModel(models.Model):
    """SmartModel"""
    now_viewmatch = models.ManyToManyField(ViewMatch,filter_interface=models.HORIZONTAL)
    
    def __str__(self):
        return "SmartModel"

SmartForm=form_for_model(SmartModel)
#class SmartForm(forms.Form):
#    vm=forms.ModelMultipleChoiceField(queryset=ViewMatch.objects.all())