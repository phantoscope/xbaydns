#!/bin/sh

export PATH=$PATH:/sbin:/usr/sbin:/usr/local/bin

PPATH=`dirname $0`
#HOST_IP=`ifconfig | grep inet | head -n1 | sed -e 's/:/ /' | awk '{print $3}'`
AGENT_NAME=`cat $PPATH/../myname`
if [ -f "$PPATH/agent.conf" ]; then
	. $PPATH/agent.conf
fi

cd $PPATH
python iplatency.py ../data/iplist ../data/${AGENT_NAME}-`date "+%Y-%m-%d"`

