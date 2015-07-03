# 介绍 #
我们的开发环境分为以下几部分：
  * 本机的开发环境
  * 源代码管理
  * 集成与测试环境
这里我会逐步丰富开发环境中的信息。

# 本机的开发环境 #
## osx ##
### osx 10.5 ###

Python：使用osx 10.5自带的python 2.5.1

BIND：使用osx 10.5自带的BIND 9.4.1-P1
### Linux ###
### Windwos ###
### FreeBSD ###

# 源代码管理 #
源代码管理使用google code的subversion。可以在http://code.google.com/p/xbaydns/source看到相关的信息。简单看一下svn的checkout的命令：
svn checkout https://xbaydns.googlecode.com/svn/trunk/ xbaydns --username huangdong
就可以看到大多数的信息。现在除了huangdong，请不要在trunk之外的地方进行提交。huangdong会在合适的时间通知大家对svn进行冻结，在发布时会在tag中发布合适的版本。

# 集成与测试环境 #
## 集成测试服务器 ##
集成测试服务器运行trac/svnsync/bitten，相关的文档可以到HD的blog上去看。到时也会有相关的文档整理过来。将来我们会在互联网上架服务器专门跑这个集成测试服务器的。

## 集成测试客户端 ##
集成测试客户端就是运行bitten-slave的客户端。它需要安装xbaydns的依赖包，这其中包括：
  * easy\_setup
  * bitten
  * pythondns
  * Django

# 生产环境 #
我们预计生着环境为FreeBSD，晚些时候会考虑到更多的操作系统。如果你不确认足够了解自己所使用的操作系统，哪么建议你来使用FreeBSD。