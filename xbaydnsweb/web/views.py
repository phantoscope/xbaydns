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
    except:
        print traceback.print_exc()
        return False

    try:
        for key_file in os.listdir('/home/xbaydns/slave/keys'):
            print "key:%s" % key_file
            key_string = open('/home/xbaydns/slave/keys/%s' % key_file, 'r').read()
            open('/home/xbaydns/.ssh/authorized_keys', 'a').write(key_string)
    except:
        print traceback.print_exc()
        return False
    return True

def create_agent(request, authzcode, pubkey):
    pubkey = pubkey.replace(',', '/').replace(';', ' ')
    print "AUTHZCODE:%s" % authzcode
    print "PUBKEY:%s" % pubkey
    try:
        idc = IDC.objects.get(authzcode=authzcode)
    except:
        print traceback.print_exc()
        return HttpResponse('sorry')

    idc.pubkey = pubkey
    try:
        idc.save()
    except:
        print traceback.print_exc()
        return HttpResponse('sorry')

    try:
        master_pubkey=open('/etc/ssh/ssh_host_rsa_key.pub', 'r').read()
    except:
        print traceback.print_exc()
        return HttpResponse('sorry')

    if regen_allkey():
        resp_stream = '%s:%s:%s' % (idc.alias, master_pubkey, install_agent_script)
        return HttpResponse(resp_stream)
    else:
        return HttpResponse('sorry')

def create_slave(request, slavename, pubkey):
    print "SLAVENAME:%s" % slavename
    pubkey = pubkey.replace(',', '/').replace(';', ' ')

    print "SLAVENAME:%s" % slavename
    print "PUBKEY:%s" % pubkey
    try:
        open('/home/xbaydns/slave/keys/%s' % slavename, 'w').write(pubkey + '\n')
    except:
        print traceback.print_exc()
        return HttpResponse('sorry')

    try:
        master_pubkey=open('/etc/ssh/ssh_host_rsa_key.pub', 'r').read()
    except:
        print traceback.print_exc()
        return HttpResponse('sorry')

    regen_allkey()
    return HttpResponse('done:%s' % master_pubkey)


