#!/bin/sh

export PATH=$PATH:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin
PPATH=`dirname $0`
if [ -f "$PPATH/../slave.conf" ]; then
	. $PPATH/../slave.conf
	. $PPATH/../xdenv
fi

cd ${PPATH}
rsync -avz -e 'ssh -i ../rsync-key' \
 xbaydns\@${MASTER_IP}:${XBAYDNSHOME}/slave/named/etc/acl ${PPATH}/../named/etc/

if ! diff ${PPATH}/../named/etc/acl  ${XBAYDNS_CHROOT_PATH}/etc/acl  > /dev/null 2>&1; then
    rsync -avz ${PPATH}/../named/etc/acl ${XBAYDNS_CHROOT_PATH}/etc/
    touch need_reload
fi

cd ${PPATH}
rsync -avz -e 'ssh -i ../rsync-key' \
 xbaydns\@${MASTER_IP}:${XBAYDNSHOME}/slave/named/etc/view  ${PPATH}/../named/etc/

if ! diff ${PPATH}/../named/etc/view  ${XBAYDNS_CHROOT_PATH}/etc/view  > /dev/null 2>&1; then
    rsync -avz ${PPATH}/../named/etc/view ${XBAYDNS_CHROOT_PATH}/etc/
    touch need_reload
fi

if [ -f need_reload ]; then
   ${XBAYDNS_CHROOT_PATH}/sbin/rndc reload
   rm need_reload
fi
