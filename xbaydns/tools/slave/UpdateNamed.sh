#!/bin/sh

export PATH=$PATH:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin
PPATH=`dirname $0`
if [ -f "$PPATH/../slave.conf" ]; then
	. $PPATH/../slave.conf
	. /home/xdslave/xdenv
fi

cd $PPATH/..

rsync -avz -e 'ssh -i /home/xdslave/rsync-key' \
 xbaydns\@$MASTER_IP:/home/xbaydns/slave/named/etc/acl /home/xdslave/named/etc/


rsync -avz -e 'ssh -i /home/xdslave/rsync-key' \
 xbaydns\@$MASTER_IP:/home/xbaydns/slave/named/etc/view  /home/xdslave/named/etc/

