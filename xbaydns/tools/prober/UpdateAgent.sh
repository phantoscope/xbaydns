#!/bin/sh

PPATH=`dirname $0`
if [ -f "$PPATH/agent.conf" ]; then
	. $PPATH/agent.conf
fi

cd $PPATH
rsync -avz -e 'ssh -i /home/named/rsync-key' named\@$CNT_CENTER_IP:/home/named/agent/* .

