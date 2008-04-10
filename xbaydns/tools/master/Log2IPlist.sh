#!/bin/sh

PPATH=`dirname $0`
if [ -f "$PPATH/../master.conf" ]; then
	. $PPATH/../master.conf
fi

cd $PPATH

if cat ../slave/named/log/*.log > ../slave/named/log/dummy ; then
	python logtolist.py ../slave/named/log/dummy ../iplist
	rm -f ../slave/named/log/dummy
fi

