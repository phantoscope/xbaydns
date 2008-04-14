# encoding: utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from xbaydnsweb.web.models import Record,Result
from xbaydnsweb.web.templatetags.webtags import resultToHtml
from xbaydnsweb.web.utils import saveAllConf
from django.conf import settings
import traceback
from xbaydnsweb.web.models import IDC
import base64
import os

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
        for rs in Result.objects.filter(record=record):
            if rs.idc.name not in result[k]:
                result[k][rs.idc.name]=[]
            result[k][rs.idc.name].append(rs.ip)
    return render_to_response('admin/smartload.html',locals())

#TODO:awful
install_agent_script = """
rm -rf /home/xdagent
userdel xdagent
useradd xdagent -g named -s /sbin/nologin -d /home/xdagent
mkdir -p /home/xdagent/{.ssh,prog,iplatency}
mv /tmp/rsync-key /home/xdagent
mv /tmp/rsync-key.pub /home/xdagent
touch /home/xdagent/.ssh/known_hosts

rsync -avz -e 'ssh -i /home/xdagent/rsync-key' xbaydns@MASTERIP:/home/xbaydns/agent/prog /home/xdagent
rsync -avz -e 'ssh -i /home/xdagent/rsync-key' xbaydns@MASTERIP:/home/xbaydns/agent/agent.conf /home/xdagent
crontab -u xdagent -l >/home/xdagent/old_crontab 2>/dev/null
crontab -u xdagent /home/xdagent/prog/crontab

chmod +x /home/xdagent/prog/*
chown -R xdagent:named /home/xdagent
chmod 700 /home/xdagent
"""


def regen_allkey():
    #TODO: it's awful to refresh all key when update one key
    open('/home/xbaydns/.ssh/authorized_keys', 'w').write('')
    try:
        for idc in IDC.objects.all():
            if idc.pubkey.startswith('ssh-dss'):
                open('/home/xbaydns/.ssh/authorized_keys', 'a').write(idc.pubkey + '\n')
        for idc in Node.objects.filter(type = 'slave'):
            if node.pubkey.startswith('ssh-dss'):
                open('/home/xbaydns/.ssh/authorized_keys', 'a').write(node.pubkey + '\n')
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
        idc.save()
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
        resp['script'] = install_agent_script
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
        node.save()
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
    else:
        resp['retcode'] = 'FAIL'
        resp['retmsg'] = "Internal server error"

    return HttpResponse(repr(resp))
