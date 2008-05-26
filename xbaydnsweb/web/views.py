# encoding: utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.utils.translation import ugettext as _
from xbaydnsweb.web.models import Record,Result
from xbaydnsweb.web.templatetags.webtags import resultToHtml
from xbaydnsweb.web.utils import saveAllConf
from xbaydns.conf import sysconf
from django.conf import settings
import traceback
from xbaydnsweb.web.models import IDC, Node
import os
import datetime

def loadgenview(request):
    from xbaydns.conf import sysconf
    from xbaydnsweb import conftoresults
    try:
        conftoresults.main()
        saveAllConf()
    except:
        pass
    return HttpResponseRedirect('/web/iparea/')

def preview(request):
    from xbaydnsweb import conftoresults
    try:
        conftoresults.main(preview=True)
    except:
        pass
    return HttpResponseRedirect('/web/previewarea/')

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
        if record.name[-1] == '.':
            k = str(record.name)
        else:
            k="%s.%s"%(record.name,record.domain)
        if k not in result:
            result[k]={}
        for rs in Result.objects.filter(record=k,idc=record.idc):
            if rs.idc.name not in result[k]:
                result[k][rs.idc.name]=[]
            result[k][rs.idc.name].append(rs.ip)
    return render_to_response('admin/smartload.html',locals())

def regen_allkey():
    #TODO: it's awful to refresh all key when update one key
    print os.path.join(sysconf.xdprefix, 'home/xbaydns/.ssh/authorized_keys')
    open(os.path.join(sysconf.xdprefix, 'home/xbaydns/.ssh/authorized_keys'), 'w').write('')
    try:
        for idc in IDC.objects.all():
            if idc.pubkey.startswith('ssh-dss'):
                open(os.path.join(sysconf.xdprefix, 'home/xbaydns/.ssh/authorized_keys'), 'a').write(idc.pubkey + '\n')
        for node in Node.objects.filter(type = 'slave'):
            if node.pubkey.startswith('ssh-dss'):
                open(os.path.join(sysconf.xdprefix, 'home/xbaydns/.ssh/authorized_keys'), 'a').write(node.pubkey + '\n')
    except:
        print traceback.print_exc()
        return False

    return True

def create_agent(request, authzcode, pubkey):
    pubkey = pubkey.replace(',', '/').replace(';', ' ')
    print "AUTHZCODE:%s" % authzcode
    print "PUBKEY:%s" % pubkey

    resp = {}

    try:
        idc = IDC.objects.get(authzcode=authzcode)
    except:
        print traceback.print_exc()
        resp['retcode'] = 'FAIL'
        resp['retmsg'] = "Can't validate your authzcode"
        return HttpResponse(repr(resp))

    idc.pubkey = pubkey

    try:
        idc.regsave()
        master_pubkey=open('/etc/ssh/ssh_host_rsa_key.pub', 'r').read()
    except:
        print traceback.print_exc()
        resp['retcode'] = 'FAIL'
        resp['retmsg'] = "Internal server error"
        return HttpResponse(repr(resp))


    if regen_allkey():
        resp['retcode'] = 'SUCC'
        resp['yourname'] = idc.alias
        resp['master_pubkey'] = master_pubkey
        resp['xbaydnshome'] = os.path.join(sysconf.xdprefix, 'home/xbaydns')
    else:
        resp['retcode'] = 'FAIL'
        resp['retmsg'] = "Internal server error"
    return HttpResponse(repr(resp))

def create_slave(request, authzcode, pubkey):
    pubkey = pubkey.replace(',', '/').replace(';', ' ')
    print "AUTHZCODE:%s" % authzcode
    print "PUBKEY:%s" % pubkey

    resp = {}

    try:
        node = Node.objects.get(authzcode=authzcode)
    except:
        print traceback.print_exc()
        resp['retcode'] = 'FAIL'
        resp['retmsg'] = "Can't validate your authzcode"
        return HttpResponse(repr(resp))

    node.pubkey = pubkey

    try:
        node.regsave()
        master_pubkey=open('/etc/ssh/ssh_host_rsa_key.pub', 'r').read()
    except:
        print traceback.print_exc()
        resp['retcode'] = 'FAIL'
        resp['retmsg'] = "Internal server error"
        return HttpResponse(repr(resp))

    if regen_allkey():
        resp['retcode'] = 'SUCC'
        resp['yourname'] = node.codename
        resp['master_pubkey'] = master_pubkey
        resp['xbaydnshome'] = os.path.join(sysconf.xdprefix, 'home/xbaydns')
    else:
        resp['retcode'] = 'FAIL'
        resp['retmsg'] = "Internal server error"

    return HttpResponse(repr(resp))
