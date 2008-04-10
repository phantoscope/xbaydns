#!/bin/sh

PPATH=`dirname $0`
if [ -f "$PPATH/slave.conf" ]; then
	. $PPATH/slave.conf
	. /home/xdslave/xdenv
fi

cd $PPATH
rsync -avz -e 'ssh -i /home/xdslave/rsync-key' \
 xbaydns\@$MASTER_IP:/home/xbaydns/slave/named/etc/acl $XBAYDNS_CHROOT_PATH/etc/

rsync -avz -e 'ssh -i /home/xdslave/rsync-key' \
 xbaydns\@$MASTER_IP:/home/xbaydns/slave/named/etc/view $XBAYDNS_CHROOT_PATH/etc/

rsync -avz -e 'ssh -i /home/xdslave/rsync-key' \
 xbaydns\@$MASTER_IP:/home/xbaydns/slave/named/etc/dynamic $XBAYDNS_CHROOT_PATH/etc/
