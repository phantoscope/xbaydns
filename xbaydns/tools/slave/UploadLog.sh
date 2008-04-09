#!/bin/sh

export PATH=$PATH:/sbin:/usr/sbin:/usr/local/bin

PPATH=`dirname $0`
#HOST_IP=`ifconfig | grep inet | head -n1 | sed -e 's/:/ /' | awk '{print $3}'`
SLAVE_NAME=`cat $PPATH/../myname`
if [ -f "$PPATH/agent.conf" ]; then
	. $PPATH/agent.conf
	. /home/xdslave/xdenv
fi

cd $PPATH
rsync -avz -e 'ssh -i /home/xdslave/rsync-key' $XBAYDNS_CHROOT_PATH/var/log/named.log xbaydns\@$MASTER_IP:/home/xbaydns/slave/log/${SLAVE_NAME}-named.log
