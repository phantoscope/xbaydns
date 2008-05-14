#!/usr/bin/env python
# encoding: utf-8

import sys

def wherepkg(pkgname):
    path  = sys.path
    for p in path:
        if not p.find(pkgname) == -1:
            print p

def main():
    wherepkg('site-packages/xbaydns')

if __name__ == "__main__":
    main()
