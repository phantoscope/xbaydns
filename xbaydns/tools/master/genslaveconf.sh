#!/bin/sh

export PATH=$PATH:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin
source /home/xbaydns/xdenv
source /home/xbaydns/master.conf

export MASTER_PATH=$XBAYDNS_CHROOT_PATH/etc
export SLAVE_PATH=/home/xbaydns/slave/named/etc

slave_replace()
{
cat $1 | sed "s/server .* { keys \(.*\) };[ ]*$/server $MASTER_IP { keys \1 };/g" | sed "s/type master;/type slave;\n        masters{ $MASTER_IP; };/g" | uniq >$1.out
mv $1.out $1
}

mkdir -p $SLAVE_PATH
rm -f $SLAVE_PATH/acl/*
cp -rf $MASTER_PATH/acl $SLAVE_PATH

rm -f $SLAVE_PATH/view/*
cp -rf $MASTER_PATH/view $SLAVE_PATH

for i in `find $SLAVE_PATH/view/*`
do
 slave_replace $i
done
