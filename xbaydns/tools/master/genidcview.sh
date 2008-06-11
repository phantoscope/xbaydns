#!/bin/sh

export PATH=$PATH:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin

PPATH=`dirname $0`
if [ -f "$PPATH/../master.conf" ]; then
	. $PPATH/../master.conf
	. $PPATH/../xdenv
fi

cd $PPATH/../agent/iplatency

for file in *
do
 if [ "$file" = "*" ]; then exit 0; fi;
 agentname=`echo $file | sed -e 's/-.*//'`
 cat $file >> $PPATH/../view/iplatency/$agentname
done

cd $PPATH/../view/iplatency
for file in *
do
 sort $file | uniq > dummy && mv dummy $file
done

${XDPREFIX}/bin/python2.5 ${XDPREFIX}/bin/xdidc2view
