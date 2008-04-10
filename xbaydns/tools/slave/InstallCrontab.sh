#!/bin/sh

export PATH=$PATH:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin
PPATH=`dirname $0`
if [ -f "$PPATH/../slave.conf" ]; then
	. $PPATH/../slave.conf
fi

cd $PPAT/..

if [ ! -f crontab ]; then
	exit 0
fi

crontab -u xdslave -l > old_crontab
if ! diff crontab old_crontab > /dev/null 2>&1 ; then
	crontab -u xdslave crontab
fi
