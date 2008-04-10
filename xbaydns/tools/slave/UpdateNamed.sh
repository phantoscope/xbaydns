#!/bin/sh

export PATH=$PATH:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin
PPATH=`dirname $0`
if [ -f "$PPATH/../slave.conf" ]; then
	. $PPATH/../slave.conf
	. /home/xdslave/xdenv
fi

cd $PPATH/..

rsync -avz -e 'ssh -i /home/xdslave/rsync-key' \
 xbaydns\@$MASTER_IP:/home/xbaydns/slave/named/etc/acl /home/xdslave/named/etc/

if ! diff /home/xdslave/named/etc/acl  $XBAYDNS_CHROOT_PATH/etc/acl  > /dev/null 2>&1; then
    rsync /home/xdslave/named/etc/acl $XBAYDNS_CHROOT_PATH/etc/
    touch need_reload
fi


rsync -avz -e 'ssh -i /home/xdslave/rsync-key' \
 xbaydns\@$MASTER_IP:/home/xbaydns/slave/named/etc/view  /home/xdslave/named/etc/

if ! diff /home/xdslave/named/etc/view  $XBAYDNS_CHROOT_PATH/etc/view  > /dev/null 2>&1; then
    rsync /home/xdslave/named/etc/view $XBAYDNS_CHROOT_PATH/etc/
    touch need_reload
fi

if [ -f need_reload ]; then
   rndc reload
   rm need_reload
fi
