#!/bin/sh

export PATH=$PATH:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin
PPATH=`dirname $0`
if [ -f "$PPATH/../slave.conf" ]; then
	. $PPATH/../slave.conf
	. /home/xdslave/xdenv
fi

cd $PPATH/..

if ! diff /home/xdslave/named/etc/acl  $XBAYDNS_CHROOT_PATH/etc/acl  > /dev/null 2>&1; then
    rsync -avz /home/xdslave/named/etc/acl $XBAYDNS_CHROOT_PATH/etc/
    touch need_reload
fi


if ! diff /home/xdslave/named/etc/view  $XBAYDNS_CHROOT_PATH/etc/view  > /dev/null 2>&1; then
    rsync -avz /home/xdslave/named/etc/view $XBAYDNS_CHROOT_PATH/etc/
    touch need_reload
fi

if [ -f need_reload ]; then
   chown -R named:named $XBAYDNS_CHROOT_PATH/etc/{acl,view}
   chmod -R 770 $XBAYDNS_CHROOT_PATH/etc/{acl,view}
   rndc reload
   rm need_reload
fi
