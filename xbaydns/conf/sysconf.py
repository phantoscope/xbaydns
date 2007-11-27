#!/usr/bin/env python
# encoding: utf-8
"""
这个文件中记录了所有的全局静态配置变量。现在只有named.conf所属路径和nameddb目录存储路径。
"""

# 安装路径，是否能传进来？暂时写成根据相对路径
import os
import platform

system, _, release, version, machine, processor = platform.uname()
system, release, version = platform.system_alias(system, release,version)

installdir = os.path.dirname(os.path.realpath(__file__)) + "/.."
# 这里记录了bind启动的chroot根目录
chroot_path = "/var/named"
# 这里记录了named.conf所存储的路径
namedconf = "/etc/namedb"

if (system == 'Darwin'  and release == '9.1.0'):
    #操作系统为Mac OSX 10.5
    chroot_path = "/"
    namedconf = "/etc"
elif (system == "FreeBSD" and release[:3] == "7.0"):
    #操作系统为FreeBSD 7.0
    chroot_path = "/var/named"
    namedconf = "/etc/namedb"

default_acl = dict(internal=('127.0.0.1', '10.217.24.0/24'))
filename_map = dict(acl='acl/acldef.conf', defzone='defaultzone.conf')
# 这里匹配了在不同的操作系统中使用的bind用户
named_user_map = dict(freebsd='bind', openbsd='named', darwin='root')

