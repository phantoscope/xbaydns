#!/bin/sh

#/home/xbaydns/slave/named
export MASTER_PATH=/home/xbaydns/named
export SLAVE_PATH=/home/xbaydns/named
echo "SLAVE_PATH",$SLAVE_PATH
mkdir -p $SLAVE_PATH
cp -rf $MASTER_PATH/acl $SLAVE_PATH
cp -rf $MASTER_PATH/view $SLAVE_PATH
cp -rf $MASTER_PATH/dynamic $SLAVE_PATH
find $SLAVE_PATH/view/* | xargs -Iaa sed -i.master s/"type master;"/"type slave;"/g aa
rm $SLAVE_PATH/view/*.master
