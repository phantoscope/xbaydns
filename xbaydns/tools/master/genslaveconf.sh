export PATH=$PATH:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin

PPATH=`dirname $0`
if [ -f "$PPATH/../master.conf" ]; then
        . $PPATH/../master.conf
        . $PPATH/../xdenv
fi

export MASTER_PATH=${XBAYDNS_CHROOT_PATH}/etc
export SLAVE_PATH=${XDPREFIX}/home/xbaydns/slave/named/etc

mkdir -p $SLAVE_PATH
rm -f $SLAVE_PATH/acl/*
cp -rf $MASTER_PATH/acl $SLAVE_PATH
rm -f $SLAVE_PATH/view/*
cp -rf $MASTER_PATH/view $SLAVE_PATH

find $SLAVE_PATH/view/ -type f -name "*" | xargs sed -i.master -e "s/type master;/type slave;\n        masters{ ${MASTER_IP}; };/g"
find $SLAVE_PATH/view/ -type f -name "*" | xargs sed -i.master -e "s/server .* { keys \(.*\) };[ ]*$/server ${MASTER_IP} { keys \1 };/g" -e "N;/server .* { keys \(.*\) };[ ]*$/D"
rm $SLAVE_PATH/view/*.master
