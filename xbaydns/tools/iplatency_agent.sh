#!/bin/sh

# iplatency_agent.sh
# get ip list from controller by ssh, and invoke iplatency to get latencies
# Created by Razor <bg1tpt AT gmail.com> on 2008-03-17.
# Copyright (c) 2008 xBayDNS Team. All rights reserved.

PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/games:/usr/local/sbin:/usr/local/bin:/usr/X11R6/bin

INSTALL_DIR="/data0/xbaydns/iplatency"
OUTPUT_DIR="/data0/xbaydns/iplatency_log"
IPLATENCY_PATH="${INSTALL_DIR}/iplatency.py"
CURDATE=`date "+%Y-%m-%d"`
HOST_IP=`ifconfig | grep inet | head -n1 | awk '{print $2}'`
OUTPUT_FILE=${HOST_IP}_${CURDATE}
CONTROLLER_IP="10.210.132.71"
IPLST="/data0/xbaydns/iplst/iplst.txt"
AGENT_PRIVATE_KEY="/data0/xbaydns/keys/agent"

mkdir -p ${OUTPUT_DIR}
ssh -i ${AGENT_PRIVATE_KEY} iplatency@${CONTROLLER} cat ${IPLST} |
${IPLATENCY_PATH} >> ${OUTPUT_FILE}
