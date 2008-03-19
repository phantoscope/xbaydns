from django.shortcuts import render_to_response

def smartload(request):
    return render_to_response('admin/smartload.html',locals())