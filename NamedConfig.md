# Introduction #
named.conf中的配置很多，我们需要满足以下要求：
  * 支持分辨出访问者的来源（view）
  * 组织好zone文件的目录结构（控制同一目录中的文件数量）
  * 组织好各个view的认证文件（key）
  * named.conf中的配置文件频繁变更的部分应被分离出来，方便传送

# 目录结构 #
```
/etc/namedb（named配置文件根目录）
        |
        +--acl（acl配置文件存储目录）
        |
        +--dynamic（存储动态更新的master zone目录）
        |
        +--master（存储手工维护的master zone目录）
        |
        +--slave（存储slave zone目录）
        |
        +--view（存储所有view的定义目录）
```

# 文件结构 #

## named.conf ##
```
options {
        // chroot相关设置
        directory       "/etc/namedb";
        pid-file        "/var/run/named/pid";
        dump-file       "/var/dump/named_dump.db";
        statistics-file "/var/stats/named.stats";

        // These zones are already covered by the empty zones listed below.
        // If you remove the related empty zones below, comment these lines out.
        disable-empty-zone "255.255.255.255.IN-ADDR.ARPA";
        disable-empty-zone "0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.IP6.ARPA";
        disable-empty-zone "1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.IP6.ARPA";

        // 否定递归请求
        recursion no;
        allow-transfer { 127.0.0.1; };
        allow-update { 127.0.0.1; };
};

// 导入acl的定义
include "acldef.conf";

// 导入logging的定义
include "logging.conf"

```

## acldef.conf ##
acldef.conf是定义了所有的acl信息。这里可以定义用户来访的区域。你可以在这里任意定义acl，比如：
```
acl "internal" { 127.0.0.1; };
acl "hdhost" { 10.217.24.0/24; };
```
如果你的acl足够的多，而且非常大，哪么应该将acl分片，放入acl子目录中。这时acldef.conf中的内容如下表示：
```
acl "internal" { 127.0.0.1; };
acl "hdhost" { 10.217.24.0/24; };
include "acl/cncacl.conf";
```

## logging.conf ##
缺省我们什么log都记，需要时会更改为简单的方式。
```
logging {

        category default {
                _default_log;
        };

        channel _default_log  {
                file "/var/log/named.log";
                severity debug;
                print-time yes;
        };
};
```

## master/empty.db ##
```
$TTL 3h
@ SOA @ nobody.localhost. 42 1d 12h 1w 3h
        ; Serial, Refresh, Retry, Expire, Neg. cache TTL

@       NS      @

; Silence a BIND warning
@       A       127.0.0.1
```

## master/localhost-reverse.db ##
```
$TTL 3h
@ SOA localhost. nobody.localhost. 42 1d 12h 1w 3h
        ; Serial, Refresh, Retry, Expire, Neg. cache TTL

        NS      localhost.

1.0.0   PTR     localhost.

1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0 PTR localhost.
```

## master/localhost-forward.db ##
```
$TTL 3h
localhost. SOA localhost. nobody.localhost. 42 1d 12h 1w 3h
        ; Serial, Refresh, Retry, Expire, Neg. cache TTL

        NS      localhost.

        A       127.0.0.1
        AAAA    ::1
```

## defaultzone.conf ##
defaultzone是按照RFC的要求加入了缺省必须的zone数据
```
// 这里的数据会在所有的view中出现
// 根服务器指向
zone "." { type hint; file "named.root"; };

// RFC 1912
zone "localhost"        { type master; file "master/localhost-forward.db"; };
zone "127.in-addr.arpa" { type master; file "master/localhost-reverse.db"; };
zone "255.in-addr.arpa" { type master; file "master/empty.db"; };

// RFC 1912-style zone for IPv6 localhost address
zone "0.ip6.arpa"       { type master; file "master/localhost-reverse.db"; };

// "This" Network (RFCs 1912 and 3330)
zone "0.in-addr.arpa"           { type master; file "master/empty.db"; };

// IANA Reserved - Unlikely to ever be assigned
zone "1.in-addr.arpa"           { type master; file "master/empty.db"; };
zone "2.in-addr.arpa"           { type master; file "master/empty.db"; };
zone "223.in-addr.arpa"         { type master; file "master/empty.db"; };

// Public Data Networks (RFC 3330)
zone "14.in-addr.arpa"          { type master; file "master/empty.db"; };

// Private Use Networks (RFC 1918)
zone "10.in-addr.arpa"          { type master; file "master/empty.db"; };
zone "16.172.in-addr.arpa"      { type master; file "master/empty.db"; };
zone "17.172.in-addr.arpa"      { type master; file "master/empty.db"; };
zone "18.172.in-addr.arpa"      { type master; file "master/empty.db"; };
zone "19.172.in-addr.arpa"      { type master; file "master/empty.db"; };
zone "20.172.in-addr.arpa"      { type master; file "master/empty.db"; };
zone "21.172.in-addr.arpa"      { type master; file "master/empty.db"; };
zone "22.172.in-addr.arpa"      { type master; file "master/empty.db"; };
zone "23.172.in-addr.arpa"      { type master; file "master/empty.db"; };
zone "24.172.in-addr.arpa"      { type master; file "master/empty.db"; };
zone "25.172.in-addr.arpa"      { type master; file "master/empty.db"; };
zone "26.172.in-addr.arpa"      { type master; file "master/empty.db"; };
zone "27.172.in-addr.arpa"      { type master; file "master/empty.db"; };
zone "28.172.in-addr.arpa"      { type master; file "master/empty.db"; };
zone "29.172.in-addr.arpa"      { type master; file "master/empty.db"; };
zone "30.172.in-addr.arpa"      { type master; file "master/empty.db"; };
zone "31.172.in-addr.arpa"      { type master; file "master/empty.db"; };
zone "168.192.in-addr.arpa"     { type master; file "master/empty.db"; };

// Link-local/APIPA (RFCs 3330 and 3927)
zone "254.169.in-addr.arpa"     { type master; file "master/empty.db"; };

// TEST-NET for Documentation (RFC 3330)
zone "2.0.192.in-addr.arpa"     { type master; file "master/empty.db"; };

// Router Benchmark Testing (RFC 3330)
zone "18.198.in-addr.arpa"      { type master; file "master/empty.db"; };
zone "19.198.in-addr.arpa"      { type master; file "master/empty.db"; };

// IANA Reserved - Old Class E Space
zone "240.in-addr.arpa"         { type master; file "master/empty.db"; };
zone "241.in-addr.arpa"         { type master; file "master/empty.db"; };
zone "242.in-addr.arpa"         { type master; file "master/empty.db"; };
zone "243.in-addr.arpa"         { type master; file "master/empty.db"; };
zone "244.in-addr.arpa"         { type master; file "master/empty.db"; };
zone "245.in-addr.arpa"         { type master; file "master/empty.db"; };
zone "246.in-addr.arpa"         { type master; file "master/empty.db"; };
zone "247.in-addr.arpa"         { type master; file "master/empty.db"; };
zone "248.in-addr.arpa"         { type master; file "master/empty.db"; };
zone "249.in-addr.arpa"         { type master; file "master/empty.db"; };
zone "250.in-addr.arpa"         { type master; file "master/empty.db"; };
zone "251.in-addr.arpa"         { type master; file "master/empty.db"; };
zone "252.in-addr.arpa"         { type master; file "master/empty.db"; };
zone "253.in-addr.arpa"         { type master; file "master/empty.db"; };
zone "254.in-addr.arpa"         { type master; file "master/empty.db"; };

// IPv6 Unassigned Addresses (RFC 4291)
zone "1.ip6.arpa"               { type master; file "master/empty.db"; };
zone "3.ip6.arpa"               { type master; file "master/empty.db"; };
zone "4.ip6.arpa"               { type master; file "master/empty.db"; };
zone "5.ip6.arpa"               { type master; file "master/empty.db"; };
zone "6.ip6.arpa"               { type master; file "master/empty.db"; };
zone "7.ip6.arpa"               { type master; file "master/empty.db"; };
zone "8.ip6.arpa"               { type master; file "master/empty.db"; };
zone "9.ip6.arpa"               { type master; file "master/empty.db"; };
zone "a.ip6.arpa"               { type master; file "master/empty.db"; };
zone "b.ip6.arpa"               { type master; file "master/empty.db"; };
zone "c.ip6.arpa"               { type master; file "master/empty.db"; };
zone "d.ip6.arpa"               { type master; file "master/empty.db"; };
zone "e.ip6.arpa"               { type master; file "master/empty.db"; };
zone "0.f.ip6.arpa"             { type master; file "master/empty.db"; };
zone "1.f.ip6.arpa"             { type master; file "master/empty.db"; };
zone "2.f.ip6.arpa"             { type master; file "master/empty.db"; };
zone "3.f.ip6.arpa"             { type master; file "master/empty.db"; };
zone "4.f.ip6.arpa"             { type master; file "master/empty.db"; };
zone "5.f.ip6.arpa"             { type master; file "master/empty.db"; };
zone "6.f.ip6.arpa"             { type master; file "master/empty.db"; };
zone "7.f.ip6.arpa"             { type master; file "master/empty.db"; };
zone "8.f.ip6.arpa"             { type master; file "master/empty.db"; };
zone "9.f.ip6.arpa"             { type master; file "master/empty.db"; };
zone "a.f.ip6.arpa"             { type master; file "master/empty.db"; };
zone "b.f.ip6.arpa"             { type master; file "master/empty.db"; };
zone "0.e.f.ip6.arpa"           { type master; file "master/empty.db"; };
zone "1.e.f.ip6.arpa"           { type master; file "master/empty.db"; };
zone "2.e.f.ip6.arpa"           { type master; file "master/empty.db"; };
zone "3.e.f.ip6.arpa"           { type master; file "master/empty.db"; };
zone "4.e.f.ip6.arpa"           { type master; file "master/empty.db"; };
zone "5.e.f.ip6.arpa"           { type master; file "master/empty.db"; };
zone "6.e.f.ip6.arpa"           { type master; file "master/empty.db"; };
zone "7.e.f.ip6.arpa"           { type master; file "master/empty.db"; };

// IPv6 ULA (RFC 4193)
zone "c.f.ip6.arpa"             { type master; file "master/empty.db"; };
zone "d.f.ip6.arpa"             { type master; file "master/empty.db"; };

// IPv6 Link Local (RFC 4291)
zone "8.e.f.ip6.arpa"           { type master; file "master/empty.db"; };
zone "9.e.f.ip6.arpa"           { type master; file "master/empty.db"; };
zone "a.e.f.ip6.arpa"           { type master; file "master/empty.db"; };
zone "b.e.f.ip6.arpa"           { type master; file "master/empty.db"; };

// IPv6 Deprecated Site-Local Addresses (RFC 3879)
zone "c.e.f.ip6.arpa"           { type master; file "master/empty.db"; };
zone "d.e.f.ip6.arpa"           { type master; file "master/empty.db"; };
zone "e.e.f.ip6.arpa"           { type master; file "master/empty.db"; };
zone "f.e.f.ip6.arpa"           { type master; file "master/empty.db"; };

// IP6.INT is Deprecated (RFC 4159)
zone "ip6.int"                  { type master; file "master/empty.db"; };

```

## named.root ##
named.root说明了互联网的根服务器的地址，需要及时的更新
```
;       This file holds the information on root name servers needed to
;       initialize cache of Internet domain name servers
;       (e.g. reference this file in the "cache  .  <file>"
;       configuration file of BIND domain name servers).
;
;       This file is made available by InterNIC
;       under anonymous FTP as
;           file                /domain/named.root
;           on server           FTP.INTERNIC.NET
;       -OR-                    RS.INTERNIC.NET
;
;       last update:    Nov 01, 2007
;       related version of root zone:   2007110100
;
;
; formerly NS.INTERNIC.NET
;
.                        3600000  IN  NS    A.ROOT-SERVERS.NET.
A.ROOT-SERVERS.NET.      3600000      A     198.41.0.4
;
; formerly NS1.ISI.EDU
;
.                        3600000      NS    B.ROOT-SERVERS.NET.
B.ROOT-SERVERS.NET.      3600000      A     192.228.79.201
;
; formerly C.PSI.NET
;
.                        3600000      NS    C.ROOT-SERVERS.NET.
C.ROOT-SERVERS.NET.      3600000      A     192.33.4.12
;
; formerly TERP.UMD.EDU
;
.                        3600000      NS    D.ROOT-SERVERS.NET.
D.ROOT-SERVERS.NET.      3600000      A     128.8.10.90
;
; formerly NS.NASA.GOV
;
.                        3600000      NS    E.ROOT-SERVERS.NET.
E.ROOT-SERVERS.NET.      3600000      A     192.203.230.10
;
; formerly NS.ISC.ORG
;
.                        3600000      NS    F.ROOT-SERVERS.NET.
F.ROOT-SERVERS.NET.      3600000      A     192.5.5.241
;
; formerly NS.NIC.DDN.MIL
;
.                        3600000      NS    G.ROOT-SERVERS.NET.
G.ROOT-SERVERS.NET.      3600000      A     192.112.36.4
;
; formerly AOS.ARL.ARMY.MIL
;
.                        3600000      NS    H.ROOT-SERVERS.NET.
H.ROOT-SERVERS.NET.      3600000      A     128.63.2.53
;
; formerly NIC.NORDU.NET
;
.                        3600000      NS    I.ROOT-SERVERS.NET.
I.ROOT-SERVERS.NET.      3600000      A     192.36.148.17
;
; operated by VeriSign, Inc.
;
.                        3600000      NS    J.ROOT-SERVERS.NET.
J.ROOT-SERVERS.NET.      3600000      A     192.58.128.30
;
; operated by RIPE NCC
;
.                        3600000      NS    K.ROOT-SERVERS.NET.
K.ROOT-SERVERS.NET.      3600000      A     193.0.14.129
;
; operated by ICANN
;
.                        3600000      NS    L.ROOT-SERVERS.NET.
L.ROOT-SERVERS.NET.      3600000      A     199.7.83.42
;
; operated by WIDE
;
.                        3600000      NS    M.ROOT-SERVERS.NET.
M.ROOT-SERVERS.NET.      3600000      A     202.12.27.33
; End of File
```

# 操作系统兼容 #
操作系统的兼容适配是在sysconf中进行的。也就是说在sysconf中有以下代码进行适配：
```
system, _, release, version, machine, processor = platform.uname()
system, release, version = platform.system_alias(system, release,version)

if (system == 'Darwin'  and release == '9.1.0'):
    #操作系统为Mac OSX 10.5
    chroot_path = "/"
    namedconf = "/etc"
elif (system == "FreeBSD" and release[:3] == "7.0"):
    #操作系统为FreeBSD 7.0
    chroot_path = "/var/named"
    namedconf = "/etc/namedb"
```
我们所需要做的就是在系统中尽可能清晰的适配出bind所运行的chroot（如果没有使用chroot启动的操作系统，设置它为/就好）和named.conf所在的目录（namedconf）。

## Mac OSX 10.5 ##
Mac OSX 10.5的BIND版本为BIND 9.4.1-P1。没有使用chroot运行bind，named.conf在/etc/中。
```
    chroot_path = "/"
    namedconf = "/etc"
```

## FreeBSD 7.0 ##
FreeBSD 7.0的BIND版本为BIND 9.4.1-P1。使用了chroot运行bind，chroot目录为/var/named，named.conf在/etc/namedb中。
```
    chroot_path = "/var/named"
    namedconf = "/etc/namedb"
```

## OpenBSD 4.2 ##
OpenBSD 4.2的BIND版本为BIND 9.3.4。使用了chroot运行bind。chrrot目录为/var/named。named.conf在/etc中。
```
    named_user = "named"
    chroot_path = "/var/named"
    namedconf = "/etc"
```