#!/usr/bin/env python
# encoding: utf-8
"""
initconf.py

Created by 黄 冬 on 2007-11-19.
Copyright (c) 2007 xBayDNS Team. All rights reserved.

初始化bind的配置文件。运行这个程序需要root的权限。不管你是什么操作系统，它的初始化都是将
/etc/namedb
目录进行初始化
"""

import logging.config
import os
import sys

log = logging.getLogger('xbaydns.tools.initconf')

def create_dir(path):
	cur = os.path.join(path)
	os.mkdir(cur)
	return cur

def main():
	pass


if __name__ == '__main__':
	main()

