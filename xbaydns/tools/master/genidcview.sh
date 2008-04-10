#!/bin/sh

PPATH=`dirname $0`
if [ -f "$PPATH/../master.conf" ]; then
	. $PPATH/../master.conf
fi

cd $PPATH/../agent/iplatency

for file in *
do
 agentname=`echo $file | sed -e 's/-.*//'`
 cat $file >> $PPATH/../view/iplatency/$agentname
done

cd $PPATH/../view/iplatency
for file in *
do
 sort $file > dummy && mv dummy $file
done

