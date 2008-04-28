#!/bin/sh

export PATH=$PATH:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin

PPATH=`dirname $0`
if [ -f "$PPATH/../agent.conf" ]; then
	. $PPATH/../agent.conf
fi

cd $PPATH
rsync -avz -e 'ssh -i ../rsync-key' xbaydns\@${MASTER_IP}:${XBAYDNSHOME}/iplist ../iplist
