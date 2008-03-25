#!/bin/sh

# install_agent.sh
# create xbaydns user and generate the ssh key.
# Created by Razor <bg1tpt AT gmail.com> on 2008-03-24.
# Copyright (c) 2008 xBayDNS Team. All rights reserved.

USER="xbaydns"
GROUP="xbaydns"
UID=60190
GID=60190
OSTYPE="`uname`"
KEYBITS=2048
INSTALLPATH="/data0/xbaydns"
MASTER_PUB="ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAsGSPcihMTxXki3WCdTq+gTf5WlzC8uVFTDqloIeiwNEMJFpgEKYx28lsEiEElT1ovP260yPr3L02OsUeeq/rRG4ow4FZjH+1xoFYgRbfY0Juls5HKS3b8NotflOdZWmG85JXjC/fxSPpnmwjx3cS/q5WweXmzcA5h24fjZXp+xJJ5DZUAq9RlDtA/8ROZD4H6EUnu/KwGpvpb6p/pvOrcohw8Wk6m8gT6H8n6gt0XRsRPo0PUry9CzOxjiJl0/sz86aSU+NlSCnxmqigx6FfO2s4KpbVfV8kzsvlwW7X8aVUtU7NE3/d7VE+M8ZV2v/KR4+MUHJr9aYBhxbbe8aT1w== root@razor"
MASTERIP="10.210.132.71"

if [ "`id -u`" != "0" ]; then
	echo "Run this script using root user."
	exit 1
fi

# create user and group
case ${OSTYPE} in
	FreeBSD) 
		pw groupadd ${GROUP} -g${GID}
		pw useradd ${USER} -u${UID} -s/sbin/nologin -d${INSTALLPATH}
	;;
	*) echo "Not implement";;
esac

# generate ssh key
mkdir -p ${INSTALLPATH}/.ssh
ssh-keygen -t rsa -b ${KEYBITS} -f ${INSTALLPATH}/.ssh/id_rsa -N ''
echo "Please paste the public key to the master's authorized_keys (the line below):"
cat ${INSTALLPATH}/.ssh/id_rsa.pub

# add the master's public key to authorized
echo ${MASTER_PUB} > ${INSTALLPATH}/.ssh/authorized_keys

# rsync agent
# rsync -az -e 'ssh -i ${INSTALLPATH}/.ssh/id_rsa' ${USER}@${MASTERIP}:${INSTALLPATH}/agent/\* ${INSTALLPATH}

# add to cron
grep -v iplatency /etc/crontab > /tmp/crontab.xbaydns
echo "*	*/1	*	*	*	${USER}	${INSTALLPATH}/iplatency/iplatency_agent.sh" >> /tmp/crontab.xbaydns
mv /tmp/crontab.xbaydns /etc/crontab
