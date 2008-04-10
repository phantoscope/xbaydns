#!/usr/bin/env python
# encoding: utf-8
"""
dbset.py

Created by samhoo <samhoo@gmail.com> on 2008-4-5
Copyright (c) 2008 xBayDNS Team. All rights reserved.

"""

import os
import sys 
import base64

def reg_agent(server, authzcode, pubkey):
    import urllib2
    url = "http://%s/agent/create/%s/%s/" % (server, authzcode, pubkey.replace('/',',').replace(' ', ';')[0:len(pubkey) - 1])
    sock = urllib2.urlopen(url)
    stream = sock.read()
    sock.close()

    index = stream.find(':')
    if index < 0 or stream == 'sorry':
        print("sorry, you can't install agent, check your authz code again")
        sys.exit(1)
    agent_name = stream[0 : index]
    index2 = stream[index + 1 : len(stream)].find(':')
    master_pubkey = stream[index + 1: index2 - 1]
    install_script = stream[index2 + 1 : len(stream)]

    os.system('touch /tmp/agent.sh')
    open('/tmp/agent.sh', 'w').write(install_script.replace('MASTERIP', server))
    os.chmod('/tmp/agent.sh', 0755)
    os.system('/tmp/agent.sh')
    open('/home/xdagent/myname', 'w').write(agent_name)
    open('/home/xdagent/.ssh/known_hosts', 'w').write(master_pubkey)

def reg_slave(server, slavename, pubkey):
    import urllib2
    url = "http://%s/slave/create/%s/%s/" % (server, slavename, pubkey.replace('/',',').replace(' ', ';')[0:len(pubkey) - 1])
    print "URL:%s" % url
    sock = urllib2.urlopen(url)
    stream = sock.read()
    sock.close()
 
    if stream == 'sorry': 
        print("sorry, you can't install slave, check your master ip again")
        sys.exit(1)

    index = stream.find(':')
    master_pubkey = stream[index + 1: len(stream)]
    open('/home/xdslave/myname', 'w').write(slavename)
    open('/home/xdslave/.ssh/known_hosts', 'w').write(master_pubkey)

def main():
    """Main entry point for running the xdagent ."""
#    from xbaydns import __version__ as VERSION
    from optparse import OptionParser
    VERSION = ''

    parser = OptionParser(usage='usage: %prog <slave|agent> [options]',
                          version='%%prog %s' % VERSION)
    parser.add_option('-m', '--master', action='store', dest='server',
                      default='', help='xbaydns master ip')
    parser.add_option('-a', '--authzcode', dest='authzcode',
                      default='', help='authzcode for authentication')
    parser.add_option('-s', '--slavename', dest='slavename',
                      default='', help='slave name')

    options, args = parser.parse_args()

    if (len(options.server) == 0) or not (len(args) == 1):
        parser.print_help()
        sys.exit(1)
    if (args[0] == 'agent'):
        if len(options.authzcode) == 0:
            parser.print_help()
            sys.exit(1)

        os.system('rm -rf /tmp/rsync-key*')
        os.system('ssh-keygen -t dsa -f /tmp/rsync-key -N ""')
        pubkey_string = open('/tmp/rsync-key.pub').read()
        print pubkey_string
        return reg_agent(options.server, options.authzcode, pubkey_string)
    elif (args[0] == 'slave'):
        if len(options.slavename) == 0:
            parser.print_help()
            sys.exit(1)
        pubkey_string = open('/home/xdslave/rsync-key.pub').read()
        return reg_slave(options.server, options.slavename, pubkey_string)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
