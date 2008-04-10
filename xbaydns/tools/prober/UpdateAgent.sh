#!/bin/sh

export PATH=$PATH:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin

PPATH=`dirname $0`
if [ -f "$PPATH/../agent.conf" ]; then
	. $PPATH/../agent.conf
fi

cd $PPATH
rsync -avz -e 'ssh -i /home/xdagent/rsync-key' xbaydns\@$MASTER_IP:/home/xbaydns/agent/prog/* .
rsync -avz -e 'ssh -i /home/xdagent/rsync-key' xbaydns\@$MASTER_IP:/home/xbaydns/agent/agent.conf ..

chmod +x /home/xdagent/prog/*
