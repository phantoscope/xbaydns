#!/bin/sh

PPATH=`dirname $0`
if [ -f "$PPATH/agent.conf" ]; then
	. $PPATH/agent.conf
fi

cd $PPATH
rsync -avz -e 'ssh -i /home/xbaydns/.rsync-key' \
 xbaydns\@$MASTER_IP:/home/xbaydns/data/iplist ../data/iplist

