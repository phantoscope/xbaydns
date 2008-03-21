#!/bin/sh

INSTALL_DIR="/data0/xbaydns/iplatency"
OUTPUT_DIR="/data0/xbaydns/iplatency_log"
IPLATENCY_PATH="${INSTALL_DIR}/iplatency.py"
CURDATE=`date "+%Y-%m-%d"`
HOST_IP=`ifconfig | grep inet | head -n1 | awk '{print $2}'`
OUTPUT_FILE=${HOST_IP}_${CURDATE}
CONTROLLER_IP="10.210.132.71"
IPLST="/data0/xbaydns/iplst/iplst.txt"
AGENT_PRIVATE_KEY="/data0/xbaydns/keys/agent"

ssh -i ${AGENT_PRIVATE_KEY} iplatency@${CONTROLLER} cat ${IPLST} |
${IPLATENCY_PATH} >> ${OUTPUT_FILE}