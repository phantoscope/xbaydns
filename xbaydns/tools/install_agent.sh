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
MASTER_PUB="ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAgEAr6BUi1BteZ4K8Jbvht1gmYK/pR6MKMSbXVgjb4y/J72NddfUwkbr6dAtdj6VBQiTNlsQaGOVEwZZDjbEAGoJhR3POngAlsIyjftgOI0kpIyH6LINOqrT2e9dpXx5uIZGY+3SaE8+is/THr12sWw87w2YIi+muQteP7dVCH499bEzzTRRz1FLz35t8kfdq9ptfJyeprBsKSnIntTyMc9tGbqojw7ReG7BITMqd6mbedNJ/Z2aKaf634puMmAyZ0tj14GlHHyQOrGOlFsP6DM/6QhOqfISJacb5kWJ4FhUyZ/aEcm4sNNfvHYWZdz6IkB7WUAryZizSBU7WmIQ7DIXLlfx6lp2s04dq5o2Ju8X8FUaO9rpvD6gUit4Q7Haefeml+JLW//TSf9GhJPpBTs5yeybb5jUxORlsoe39f/dhJyofZVcLCikHCxpyGbywbZPNKNSyypHzhTaGDWXVu0eEFho8WspLMqnPE2zpDP3woAB6fjpQfW9khEskLgrnsp8coE2tAT/Kt46Qn9JzbuIcaX9m3LmoP0GBei2JcbgkE+Qi0BEu62bs0LKmXL1lbL+roVkg8XBySV2e6Hildg9S20TyFJJyrDAbdB0qyQCjusMOs1FmrXBjJ8Lj/3bc2XmYMjdR5/Gw5kkag6CfwurG5vG9gC9N4vXpzmH+3Lvs2U="
MASTERIP="10.210.132.70"

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
read -p "Be sure the public key is pasted, then press any key to continue" nouse

# add the master's public key to authorized
echo ${MASTER_PUB} > ${INSTALLPATH}/.ssh/authorized_keys

# rsync agent
mkdir -p ${INSTALLPATH}/iplatency
rsync -az -e 'ssh -i ${INSTALLPATH}/.ssh/id_rsa' ${USER}@${MASTERIP}:${INSTALLPATH}/agent/\* ${INSTALLPATH}/iplatency

# add to cron
grep -v iplatency /etc/crontab > /tmp/crontab.xbaydns
echo "*	*/1	*	*	*	${USER}	${INSTALLPATH}/iplatency/iplatency_agent.sh" >> /tmp/crontab.xbaydns
mv /tmp/crontab.xbaydns /etc/crontab
