#!/bin/sh

export PATH=$PATH:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin

PPATH=`dirname $0`
if [ -f "$PPATH/../agent.conf" ]; then
	. $PPATH/../agent.conf
fi

cd $PPATH
rsync -avz -e 'ssh -i ${XDPREFIX}/home/xdagent/rsync-key' xbaydns\@$MASTER_IP:${XDPREFIX}/home/xbaydns/agent/prog/* .
rsync -avz -e 'ssh -i ${XDPREFIX}/home/xdagent/rsync-key' xbaydns\@$MASTER_IP:${XDPREFIX}/home/xbaydns/agent/agent.conf ..

chmod +x ${XDPREFIX}/home/xdagent/prog/*
