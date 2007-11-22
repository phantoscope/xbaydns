#!/usr/bin/env python
# encoding: utf-8
"""
这个文件中记录了所有的全局静态配置变量。现在只有named.conf所属路径和nameddb目录存储路径。
"""

# 安装路径，是否能传进来？暂时写成根据相对路径
import os
installdir = os.path.dirname(os.path.realpath(__file__)) + "/.."
# 这里记录了named.conf所存储的路径
namedconf = "/etc/namedb"
# 这里记录了dynamic、master和slave目录所有的路径
nameddb = "/etc/namedb"
default_acl = dict(internal=('127.0.0.1', '10.217.24.0/24'))
filename_map = dict(acl='acl/acldef.conf', defzone='/defaultzone.conf')