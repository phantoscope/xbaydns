# encoding: utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse
from xbaydnsweb.web.models import Record,Result
from xbaydnsweb.web.templatetags.webtags import resultToHtml

def smartload(request):
    result={}
    records=Record.objects.all()
    for record in records:
        if record.name not in result:
            result[record.name]={}
        for rs in Result.objects.filter(record=record):
            if rs.idc.name not in result[record.name]:
                result[record.name][rs.idc.name]=[]
            result[record.name][rs.idc.name].append(rs.ip)
    return render_to_response('admin/smartload.html',locals())
    
#def gennamedconf(request):
#    return HttpResponse("生成完毕")