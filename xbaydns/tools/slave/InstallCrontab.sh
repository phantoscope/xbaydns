#!/bin/sh

PPATH=`dirname $0`
if [ -f "$PPATH/agent.conf" ]; then
	. $PPATH/agent.conf
fi

cd $PPATH

if [ ! -f crontab ]; then
	exit 0
fi

crontab -u xdslave -l > old_crontab
if ! diff crontab old_crontab > /dev/null 2>&1 ; then
	crontab -u xdslave crontab
fi
