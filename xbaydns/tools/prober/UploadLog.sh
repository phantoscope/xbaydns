#!/bin/sh

export PATH=$PATH:/sbin:/usr/sbin:/usr/local/bin

PPATH=`dirname $0`
HOST_IP=`ifconfig | grep inet | head -n1 | sed -e 's/:/ /' | awk '{print $3}'`

if [ -f "$PPATH/agent.conf" ]; then
	. $PPATH/agent.conf
fi

cd $PPATH
rsync -avz -e 'ssh -i /home/named/rsync-key' $QUERY_LOG_FILE named\@$CNT_CENTER_IP:/home/named/data/${HOST_IP}-named.log
