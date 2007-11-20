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
from xbaydns.utils import shtools

import errno
import getopt
import logging.config
import os
import sys
from tempfile import mkdtemp
import time

#log = logging.getLogger('xbaydns.tools.initconf')
CUR_DIR = os.getcwd()
TMPL_DIR = CUR_DIR + "/templates"
TMPL_DEFAULTZONE = "%s/defaultzone.tmpl"%TMPL_DIR
TMPL_NAMEDCONF = "%s/namedconf.tmpl"%TMPL_DIR
TMPL_NAMEDROOT = "%s/namedroot.tmpl"%TMPL_DIR
DEF_BASEDIR = "/etc"
ERR_BACKUP = 1000
DEF_ACL = dict(internal=('127.0.0.1', '10.217.24.0/24'))
FILENAME_MAP = dict(acl='acldef.conf', defzone='defaultzone.conf')

def acl_file(acls):
    '''acls = dict(aclname=('ip0', 'net0'))'''
    acl_content = ""
    for aclname, aclvalue in acls.iteritems():
        acl_content += 'acl "%s" { '%aclname
        for aclnet in aclvalue:
            acl_content += "%s; "%aclnet
        acl_content += "};\n"
    return acl_content

def defaultzone_file():
    if os.path.isfile(TMPL_DEFAULTZONE) == False:
        return False
    else:
        return open(TMPL_DEFAULTZONE, "r").read() + "\n"

def named_root_file():
    if os.path.isfile(TMPL_NAMEDROOT) == False:
        return False
    else:
        return open(TMPL_NAMEDROOT, "r").read()

def namedconf_file(include_files):
    if os.path.isfile(TMPL_DEFAULTZONE) == False:
        return False
    else:
        namedconf = open(TMPL_NAMEDCONF, "r").read() + "\n"
        for filename in include_files.itervalues():
            namedconf += 'include "%s"\n'%filename
        return namedconf + "\n"

def make_localhost():
    pass
    
def backup_conf(real_basedir, backdir):
    if os.path.isdir(real_basedir + "/namedb") == False:
        return False
    else:
        retcode = shtools.execute(executable = "tar", args = "-cjf %s/namedconf_%s.tar.bz2 %s/namedb"%(backdir, time.strftime("%y%m%d%H%M"), real_basedir))
        if retcode == 0:
            return True
        else:
            return False

def create_destdir():
    tmpdir = mkdtemp()
    os.makedirs("%s/namedb/acl"%tmpdir)
    os.mkdir("%s/namedb/dynamic"%tmpdir)
    os.chown("%s/namedb/dynamic"%tmpdir, 53)
    os.mkdir("%s/namedb/master"%tmpdir)
    os.mkdir("%s/namedb/slave"%tmpdir)
    os.chown("%s/namedb/slave"%tmpdir, 53)
    return tmpdir

def create_conf(tmpdir):
    
    acl = acl_file(DEF_ACL)
    defzone = defaultzone_file()
    namedroot = named_root_file()

    if acl == False or defzone == False or namedroot == False:
        return False
    else:
        tmpfile = open("%s/namedb/acl/%s"%(tmpdir, FILENAME_MAP['acl']), "w")
        tmpfile.write(acl)
        tmpfile.close()
        tmpfile = open("%s/namedb/%s"%(tmpdir, FILENAME_MAP['defzone']), "w")
        tmpfile.write(defzone)
        tmpfile.close()
        tmpfile = open("%s/namedb/named.root"%tmpdir, "w")
        tmpfile.write(namedroot)
        tmpfile.close()
        namedconf = namedconf_file(FILENAME_MAP)
        tmpfile = open("%s/namedb/named.conf"%tmpdir, "w")
        tmpfile.write(namedconf)
        tmpfile.close()
        return True
        
def install_conf(tmpdir, real_basedir):
    ret = shtools.execute(executable="rm", args="-rf %s/namedb"%real_basedir)
    if ret == 0:
        ret = shtools.execute(executable="mkdir", args="-p %s"%real_basedir)
        if ret == 0:
            ret = shtools.execute(executable="mv", args="%s/namedb %s"%(tmpdir, real_basedir))
            if ret == 0:
                return True
    else:
        return False
    
def usage():
    print "usage: %s [-db]"%__file__
    
def main():
    # check root
    if os.getuid() != 0:
        print "You need be root to run this program."
        return errno.EPERM
    # parse options
    try:
        opts = getopt.getopt(sys.argv[1:], "d:b:")
    except getopt.GetoptError:
        usage()
        return errno.EINVAL
    basedir = DEF_BASEDIR
    backup = False
    backdir = ""
    for optname, optval in opts[0]:
        if optname == "-d":
            basedir = optval
        elif optname == "-b":
            backup = True
            backdir = optval
    real_basedir = os.path.dirname(os.path.realpath(basedir + "/namedb"))
    # backup
    if backup == True:
        if os.path.isdir(real_basedir + "/namedb") == True:
            ret = backup_conf(real_basedir, backdir)
            if ret == False:
                print "Backup failed."
                return -1
        else:
            print "No namedb in basedir, I'll continue."
    # that's my business
    tmpdir = create_destdir()
    if create_conf(tmpdir) == False or install_conf(tmpdir, real_basedir) == False:
        print "Create configuration files failed."
        return -1
    else:
        os.rmdir(tmpdir)
        return 0

if __name__ == '__main__':
    sys.exit(main())
