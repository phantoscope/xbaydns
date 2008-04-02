#!/usr/bin/env python
# encoding: utf-8
"""
这个文件中记录了所有的全局静态配置变量。现在只有named.conf所属路径和nameddb目录存储路径。
可以使用环境变量来设置配置，环境变量定义如下：
bind启动时的chroot目录，如果没有使用chroot设置为/
XBAYDNS_CHROOT_PATH
bind的配置文件路径
XBAYDNS_BIND_CONF
bind的启动脚本
XBAYDNS_BIND_START
bind的停止脚本
XBAYDNS_BIND_STOP
bind的重启脚本
XBAYDNS_BIND_RESTART
运行bind的用户
XBAYDNS_BIND_USER
所有的环境变量会
"""


import re
import os
import platform
import pwd
import sys
import errno

system, _, release, version, machine, processor = platform.uname()
system, release, version = platform.system_alias(system, release,version)
release = re.compile(r"^\d+.\d+").search(release).group()

# 安装路径，是否能传进来？暂时写成根据相对路径
installdir = os.path.dirname(os.path.realpath(__file__)) + "/.."
# 这里记录了bind启动的chroot根目录

#TODO: the following varirable should read from configuration ile
#    : varible not defined in configuration should be set to ''
chroot_path = ""
# 这里记录了named.conf所存储的路径
namedconf = ""
# bind运行的用户名
named_user = ""
# 这是bind的启动脚本
namedstart = ""
# 这是bind的停止脚本
namedstop = ""
# 这是bind的重启脚本
namedrestart = ""

namedef = {'Darwin':
                {'chroot_path':'/', 
                'namedconf':'/etc', 
                'named_user':'root', 
                'namedstart':'sudo service org.isc.named start;sleep 2', 
                'namedstart':'sudo service org.isc.named restart;sleep 2', 
                'namedstop':'sudo service org.isc.named stop'},
           'FreeBSD':
                {'chroot_path':'/var/named', 
                'namedconf':'/etc/namedb', 
                'named_user':'bind', 
                'namedstart':'/etc/rc.d/named start',
                'namedrestart':'/etc/rc.d/named restart',
                'namedstop':'/etc/rc.d/named stop'},
           'OpenBSD':
                {'chroot_path':'/var/named', 
                'namedconf':'/var/named', 
                'named_user':'named', 
                'namedstart':'/etc/rc.d/named start',
                'namedrestart':'/etc/rc.d/named restart',
                'namedstop':'/etc/rc.d/named stop'},
           'Linux':
                {'chroot_path':'/', 
                'namedconf':'/etc', 
                'named_user':'named', 
                'namedstart':'/etc/rc.d/named start',
                'namedrestart':'/etc/rc.d/named restart',
                'namedstop':'/etc/rc.d/named stop'}}

if     ((system == 'Darwin') and (release == '9.1.0')) \
    or ((system == 'FreeBSD') and (release >= '6.2')) \
    or ((system == 'OpenBSD') and (release >= '4.2')) \
    or (system == 'Linux'): 
        if len(chroot_path) == 0:
            chroot_path = namedef[system]['chroot_path']
        if len(namedconf) == 0:
            namedconf = namedef[system]['namedconf']
        if len(named_user) == 0:
            named_user = namedef[system]['named_user']
        if len(namedstart) == 0:
            namedstart = namedef[system]['namedstart']
        if len(namedstop) == 0:
            namedstop = namedef[system]['namedstop']
        if len(namedrestart) == 0:
            namedrestart = namedef[system]['namedrestart']

chroot_path = os.getenv('XBAYDNS_CHROOT_PATH', chroot_path)
namedconf  = os.getenv('XBAYDNS_BIND_CONF', namedconf)
named_user  = os.getenv('XBAYDNS_BIND_USER', named_user)
namedstart = os.getenv('XBAYDNS_BIND_START', namedstart)
namedstop = os.getenv('XBAYDNS_BIND_STOP', namedstop)
namedrestart = os.getenv('XBAYDNS_BIND_RESTART', namedrestart)


try:
    named_uid = pwd.getpwnam(named_user)[2]

except KeyError:
    print "No such a user %s. I'll exit."%named_user
    sys.exit(errno.EINVAL)
        

default_acl = dict(internal=('127.0.0.1', '10.217.24.0/24'))
filename_map = dict(acl='acl/acldef.conf')
default_zone_file = "defaultzone.conf"
default_soa = 'localhost'
default_ns = 'ns1.sina.com.cn'
default_admin = 'huangdong@gmail.com'
