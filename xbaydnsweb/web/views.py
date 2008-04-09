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
groupdel xdagent
groupadd xdagent
useradd xdagent -g xdagent -s /sbin/nologin -d /home/xdagent
mkdir -p /home/xdagent/{prog,iplatency}
mv /tmp/rsync-key /home/xdagent
mv /tmp/rsync-key.pub /home/xdagent

rsync -avz -e 'ssh -i /home/xdagent/rsync-key' xdagent@MASTERIP:/home/xdagent/prog /home/xdagent
rsync -avz -e 'ssh -i /home/xdagent/rsync-key' xdagent@MASTERIP:/home/xdagent/agent.conf /home/xdagent
chmod +x /home/xdagent/prog/*
chown -R xdagent:xdagent /home/xdagent
chmod 700 /home/xdagent

/home/xdagent/prog/InstallCrontab.sh
"""


def regen_allkey():
    #TODO: it's awful to refresh all key when update one key
    for idc in IDC.objects.all():
        if idc.pubkey.startswith('ssh-dss'):
            open('/home/xbaydns/.ssh/authorized_keys', 'a').write(idc.pubkey + '\n')

    for key_file in os.listdir('/home/xbaydns/slave/keys'):
        key_string = open('/home/xbaydns/slave/keys/%s' % key_file, 'r').read()
        open('/home/xbaydns/.ssh/authorized_keys', 'a').write(key_string)


def create_agent(request, authzcode, pubkey):
    pubkey = pubkey.replace(',', '/').replace(';', ' ')
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
    open('/home/xbaydns/.ssh/authorized_keys', 'w').write('')

    regen_allkey()
    resp_stream = '%s:%s' % (idc.alias, install_agent_script)
    return HttpResponse(resp_stream)

def create_slave(request, slavename, pubkey):
    pubkey = pubkey.replace(',', '/').replace(';', ' ')

    #TODO: 

    open('/home/xbaydns/slave/keys/%s' % slavename, 'w').write(pubkey)

    regen_allkey()

    return HttpResponse('done.')
