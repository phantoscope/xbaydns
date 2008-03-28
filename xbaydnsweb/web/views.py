# encoding: utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from xbaydnsweb.web.models import Record,Result
from xbaydnsweb.web.templatetags.webtags import resultToHtml
from xbaydnsweb.web.utils import saveAllConf
from django.conf import settings
import traceback

def smartload(request):
    if request.method == 'POST':
        msg = _("Smart View Msg Complete")
        try:
            saveAllConf(settings.OUTPUT_CONF)
        except:
            print traceback.print_exc()
            msg = _("Smart View Msg Error")
    result={}
    for record in Record.objects.all():
        if record.name not in result:
            result[record.name]={}
        for rs in Result.objects.filter(record=record):
            if rs.idc.name not in result[record.name]:
                result[record.name][rs.idc.name]=[]
            result[record.name][rs.idc.name].append(rs.ip)
    return render_to_response('admin/smartload.html',locals())
