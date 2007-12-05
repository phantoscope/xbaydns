About xBayDNS
=============

xBayDNS是一个基于Web的BIND 9管理界面。与通常我们所知道的管理界面所不同的是，它尽可能的将DNS的管理简化，并帮助用户建立起一个容易管理、维护、
扩展的DNS系统。

一个普通的DNS服器可以提供域名的解析、代理、缓存这样的服务。我们期望DNS不但是一个服务，它更应该承担起GSLB、用户访问加速这样的任务。而在现实的环境中，
应用DNS已经能够很好的完成这样的工作。所以沿着从前的经历，我们启动了xBayDNS这个项目，它的目的是让DNS服务在承担着GSLB和访问加速这样的工作时更容
易管理。做为xBayDNS附加的礼物，也可以从中学到如何形成一个基于DNS的GSLB和用户访问加速的原理。

xBayDNS的特性如下：
 * 基于Web的BIND管理
 * 非常容易的支持多种操作系统（现有我们考虑支持的就有FreeBSD、OpenBSD、MacOSX、Linux）
 * 支持ACL、View、TSIG这样的BIND高级管理功能

什么时候使用xBayDNS？
 * 你需要简单的管理一台BIND的DNS服务器
 * 一套基于DNS的GSLB系统
 * 一套基于DNS的分布式GSLB系统

Install
=============

xBayDNS需要以下软件：
 * BIND （>9.4.1）
 * Django （0.96.1）
 * dnspython （1.6）
 * python（2.5）

Release Notes
=============

1.0
 * 支持FreeBSD 7.0操作系统
 * 支持BIND 9.4.1P1
 * 支持DNS的初始化操作
 * 支持DNS的A、MX、NS、CNAME记录的管理
 * 支持ACL的管理
 * 支持View的管理
 * 支持基于View（TSIG）的域名记录管理