#!/bin/sh

export PATH=$PATH:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin

PPATH=`dirname $0`
#HOST_IP=`ifconfig | grep inet | head -n1 | sed -e 's/:/ /' | awk '{print $3}'`
SLAVE_NAME=`cat $PPATH/../myname`
if [ -f "$PPATH/../slave.conf" ]; then
	. $PPATH/../slave.conf
	. $PPATH/../xdenv
fi

cd ${PPATH}
rsync -avz -e "ssh -i ${PPATH}/../rsync-key" ${XBAYDNS_CHROOT_PATH}/var/log/query.log xbaydns\@$MASTER_IP:${XBAYDNSHOME}/slave/named/log/${SLAVE_NAME}-query.log
