#!/bin/sh

PPATH=`dirname $0`
if [ -f "$PPATH/agent.conf" ]; then
	. $PPATH/agent.conf
fi

cd $PPATH

if cat ../data/*.log > ../data/dummy ; then
	python logtolist.py ../data/dummy ../data/iplist
	rm -f ../data/dummy
fi

