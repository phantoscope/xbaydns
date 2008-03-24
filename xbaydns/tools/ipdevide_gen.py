#!/usr/bin/python
import random

def ipdevide_gen(ip_count, devides_count):
    ips = set()
    devides = []
    while len(ips) <= ip_count:
        ips.add(ipgen())
    for i in range(devides_count):
        devides.append(randevide(list(ips)[:]))
    return devides

def ipgen():
    return "%d.%d.%d.%d"%(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def randevide(ips):
    devide = []
    while True:
        ipcount = random.randint(0, len(ips))
        ec = []
        for i in range(ipcount):
            while True:
                index = random.randint(0, len(ips))
                try:
                    ec.append(ips[index])
                    del ips[index]
                    break
                except IndexError:
                    continue
        devide.append(ec)
        if len(ips) == 0:
            break
    return devide

# test
#print ipdevide_gen(4, 3)
