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
MASTER_PUB="ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAgEAvU9ro9cXksNrwrApyRjKgNFpjyqU7f/TWpLDbUXjzgXFR7MRJs+6HoCEU7aRoupwvzXOstA/0Hsl0EqE+Sb8CtFYNcYxDfjDRMObJYf4JS7zK3TAvRIdrAosdNcehhH2sOexc1emyaE4E8xnqAy3OKA8ATzCRpmHJqpjpPX9bZ/o8NAZn0o+E3VGysLzi5GvOwe4v20Uzj6hcIZyWeBzrpYQ8S2m24XWDE9c4PMNm7XnULYznMG2+2GZWn1x87EWKJMZ1BGizIFSdzV58tbI8f5+hlIgWRn40S+2JYBIja9w0hcGAmGChsEaS9VFchqmUi4DQyM/cXkVU3KkFpBpOHeEPUK68mmnP+IzYQ4Gwkkfmrdf7hr9eC0DE5GP0/W6r+eHI6Hk0Opv5GpJxW2n6Lyupo99iexg4lySLXWdLiV5DrnE4zpNexeh5SbfVJ+TTFUdW77OupsQoWfu+vFUe78DtFhkWXcinJAEqUx2hHMR0WqIbT34JLhvGPh2l7uqntrv7LdoRZIrP5bLgo3ud2nUQMhHDmsccMmTUqEoMe1imq+dvRIFnJuA6JZsX+Oca3hqcv+sy8QZBKlFyVlIyuzWhcDFgHrhKQqUgYw0j5vcX5F+QM2aEir2pgfoFIUrwk4UZvAHeR9ra5U0E2BG4ChUcGu9dFpNBJlRpePpsp8= root@november.sysdev.sina.com.cn"
KNOWN_MASTER="10.210.132.70 ssh-dss AAAAB3NzaC1kc3MAAACBAJDkyyiXLub85a741dYGe6dY2k9rQqUP/HH+MLiEV8Yk11F4tYzP28ByDjtM60BZzaQztjAT96+ZrsHIc3rPgua8TkJ92zyu8UqNp+cz7QZemJMYY4ysWav5OOJM6VkSmFHugr0zR3AIIV9/hFQuPmOeDR7NvDJEwrWnPYzISdghAAAAFQCfJr9dI26UIkrGbP2gxwJbmEhSuwAAAIBkD39AlTA9e+UjzjPyBMqBFjdOY6T1tqB3DjvtmXQg5W3+lheXnVvasQZdhQyeMHw0bDXxgcpJDNFtHcoyqaKgvVtnuGu1xMBNj1BlJJkEG7IY/z4tJHMZVihJXNzMNPlcWlQS8DfxIL8hgwqDeuZNY7OQsbGaVhmWB3ZOxfYiBQAAAIAx/vRc6PPdwhP16+xogNqqgfIf/rdH2IxJAC2WMHCFJd1BvZZU5jRNWIq16F2nMycHV8EFmK3CZbnBa28quZQYmGCcqa/6YxgjWxVRFX7gVSbriBbrIhl7emy5t15clRLXQBinOJbiPUaGn6DxEoAaowFPKufro3etnEJeVLNkBQ=="
MASTERIP="10.210.132.70"

if [ "`id -u`" != "0" ]; then
	echo "Run this script using root user."
	exit 1
fi

# create user and group
case ${OSTYPE} in
	FreeBSD) 
		pw groupadd ${GROUP} -g${GID}
		pw useradd ${USER} -u${UID} -s/usr/libexec/smrsh -d${INSTALLPATH}
		ln -s `which rsync` /usr/libexec/sm.bin/rsync
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
echo ${KNOWN_MASTER} > ${INSTALLPATH}/.ssh/known_hosts

# rsync agent
mkdir -p ${INSTALLPATH}/iplatency
rsync -az -e "ssh -i ${INSTALLPATH}/.ssh/id_rsa" ${USER}@${MASTERIP}:${INSTALLPATH}/agent/\* ${INSTALLPATH}/iplatency
chown -R xbaydns:xbaydns ${INSTALLPATH}
chown -R xbaydns:xbaydns ${INSTALLPATH}/.ssh

# add to cron
grep -v iplatency /etc/crontab > /tmp/crontab.xbaydns
echo "*	*/1	*	*	*	${USER}	/bin/sh ${INSTALLPATH}/iplatency/iplatency_agent.sh" >> /tmp/crontab.xbaydns
mv /tmp/crontab.xbaydns /etc/crontab
