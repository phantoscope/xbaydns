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

    resp = eval(stream)
    if resp['retcode'] == 'FAIL':
        print('Sorry, %s', resp['retmsg'])
        sys.exit(1)

    open('/home/xdagent/myname', 'w').write(resp['yourname'])
    open('/home/xdagent/.ssh/known_hosts', 'w').write(server + ' ' + resp['master_pubkey'])


def reg_slave(server, authzcode, pubkey):
    import urllib2
    url = "http://%s/slave/create/%s/%s/" % (server, authzcode, pubkey.replace('/',',').replace(' ', ';')[0:len(pubkey) - 1])
    print "URL:%s" % url
    sock = urllib2.urlopen(url)
    stream = sock.read()
    sock.close()

    resp = eval(stream)
    if resp['retcode'] == 'FAIL':
        print('Sorry, %s', resp['retmsg'])
        sys.exit(1)
 
    open('/home/xdslave/myname', 'w').write(resp['yourname'])
    open('/home/xdslave/.ssh/known_hosts', 'w').write(server + ' ' + resp['master_pubkey'])

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

    options, args = parser.parse_args()

    if (len(options.server) == 0) or not (len(args) == 1):
        parser.print_help()
        sys.exit(1)
    if (args[0] == 'agent'):
        if len(options.authzcode) == 0:
            parser.print_help()
            sys.exit(1)

        pubkey_string = open('/home/xdagent/rsync-key.pub').read()
        return reg_agent(options.server, options.authzcode, pubkey_string)
    elif (args[0] == 'slave'):
        if len(options.authzcode) == 0:
            parser.print_help()
            sys.exit(1)
        pubkey_string = open('/home/xdslave/rsync-key.pub').read()
        return reg_slave(options.server, options.authzcode, pubkey_string)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
