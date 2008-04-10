#!/bin/sh

export PATH=$PATH:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin
PPATH=`dirname $0`
if [ -f "$PPATH/../agent.conf" ]; then
	. $PPATH/../agent.conf
fi

cd $PPATH/..

if [ ! -f crontab ]; then
	exit 0
fi

crontab -u xdagent -l > old_crontab
if ! diff crontab old_crontab > /dev/null 2>&1 ; then
	crontab -u xdagent crontab
fi
