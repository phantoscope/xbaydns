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

install_script = """
userdel xbaydns
groupdel xbaydns
rm -rf /home/xbaydns
groupadd xbaydns
useradd xbaydns -g xbaydns -s /bin/nologin -d /home/xbaydns
mkdir -p /home/xbaydns
mkdir -p /home/xbaydns/{agent,data}
mv /tmp/rsync-key /home/xbaydns/.rsync-key

rsync -avz -e 'ssh -i /home/xbaydns/.rsync-key' xbaydns@10.210.128.24:/home/xbaydns/agent /home/xbaydns
chmod +x /home/xbaydns/agent/*.sh
chown -R xbaydns:xbaydns /home/xbaydns
chmod 700 /home/xbaydns

/home/xbaydns/agent/InstallCrontab.sh
"""

def create_agent(request, authzcode, pubkey):
    # querey agent model by  authz_code
    
    pubkey = pubkey.replace(',', '/').replace(';', ' ')
    try:
        idc = IDC.objects.get(authzcode=authzcode)
    except:
        print traceback.print_exc()
        return HttpResponse('sorry')

    idc.pubkey = pubkey
    resp_stream = '%s:%s' % (idc.alias, install_script)
    try:
        idc.save()
    except:
        print traceback.print_exc()
        return HttpResponse('sorry')
    #TODO: re-generate the ssh key
    open('/home/xbaydns/.ssh/authorized_keys', 'w').write('')
    for idc in IDC.objects.all():
        print idc.pubkey
        if idc.pubkey.startswith('ssh-dss'):
            open('/home/xbaydns/.ssh/authorized_keys', 'a').write(idc.pubkey + '\n')
    return HttpResponse(resp_stream)

