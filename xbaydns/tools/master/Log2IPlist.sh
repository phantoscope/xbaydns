#!/bin/sh

PPATH=`dirname $0`
if [ -f "$PPATH/agent.conf" ]; then
	. $PPATH/agent.conf
fi

cd $PPATH

if cat ../slave/named/log/*.log > ../slave/named/log/dummy ; then
	python logtolist.py ../slave/named/log/dummy ../iplist
	rm -f ../slave/named/log/dummy
fi

