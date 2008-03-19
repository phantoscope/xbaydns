from django.shortcuts import render_to_response
from xbaydnsweb.web.forms import SmartForm

def smartload(request):
    f=SmartForm()
    return render_to_response('admin/smartload.html',locals())