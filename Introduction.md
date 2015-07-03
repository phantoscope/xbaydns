# 概述 #

xbaydns是一个基于Web的BIND 9管理界面。与通常我们所知道的管理界面所不同的是，它尽可能的将DNS的管理简化，并帮助用户建立起一个容易管理、维护、扩展的DNS系统。

一个普通的DNS服器可以提供域名的解析、代理、缓存这样的服务。我们期望DNS不但是一个服务，它更应该承担起GSLB、用户访问加速这样的任务。而在现实的环境中，应用DNS已经能够很好的完成这样的工作。所以沿着从前的经历，我们启动了xBayDNS这个项目，它的目的是让DNS服务在承担着GSLB和访问加速这样的工作时更容易管理。做为xBayDNS附加的礼物，也可以从中学到如何形成一个基于DNS的GSLB和用户访问加速的原理。

# 出发点 #

什么是GSLB呢？GSLB就是一个把互联网世界划分成片，让用户最快、不中断的访问服务的方法。一个简单的方法就像下图这样把用户按地域划分为片，让他们访问为该片区提供服务的服务器们：

![http://xbaydns.googlecode.com/svn/trunk/docs/img/GSLB.png](http://xbaydns.googlecode.com/svn/trunk/docs/img/GSLB.png)

在xBayDNS系统中我们把这看为四组对象：

![http://xbaydns.googlecode.com/svn/trunk/docs/img/DNSDist.png](http://xbaydns.googlecode.com/svn/trunk/docs/img/DNSDist.png)

  * 用户来源
由ACL和View来定义出用户来源
  * 用户来源组
将用户来源划分成组，这样方便群体操作
  * 服务器
就是DNS的记录了，这些记录就是我们的一台台服务器
  * 服务器组
把服务器分组，这样方便群体操作。

# 工作原理 #
## 视图 ##
在BIND中有一个功能特性：view。它的功能是按IP区别出不同的用户，把用户解析到不同的服务器上去。一个简单的应用就是一台DNS服务对于英国用户发出的www.abc.com这样的解析请求，它可以将www.abc.com解析到英国的服务器。而对于一个中国用户发出的www.abc.com这样的解析请求，解析到中国的服务器上去。这样就形成了在整个互联网上跨国家、跨机房的用户最短路径访问的能力。

## 轮询 ##
在BIND中，同样是www.abc.com这样的记录，可以解析到多个IP上去。bind可以按我们的要求，将A、B、C三个用户的请求分到三个不同的IP上。这样它又可以实现在整个互联网上跨国家、跨机房的负载均衡的能力。

# 实现 #
在xBayDNS的1.0版本中，它先会实现两类功能，一类是对BIND的named.conf的管理，一类是对域名记录的管理：
  * 对named.conf的管理
    1. acl的管理
    1. view的管理
    1. zone的管理
    1. zone数据文件的初始化和删除管理
  * 对域名记录的管理
以下我们会对这两种管理的方法进行说明。

## 对named.conf的管理 ##
named.conf文件是BIND的启动配置文件，它里面存储了大量的BIND自身的设置信息。这个文件的特点是无法通过BIND的API进行管理，BIND对它只是读，没有写入的功能。另一个特点就是在BIND的主、辅服务器上的设置更是不相同。最重要的就是如果这个文件出现了错误，哪么一个BIND就无法对外正常提供服务（无法正常启动）。

为了保证对这个文件进行操作时的准确性，我们采用了如下方法：
  * 生成的文件均在临时目录中，经过named-checkconf检查通过后才会更新正在使用的配置文件
  * 尽量使用named.conf的include文件，减少在编辑文件时的冲突

对于named.conf的操作，通常如下图所示：

![http://xbaydns.googlecode.com/svn/trunk/docs/img/DomainUpdate.png](http://xbaydns.googlecode.com/svn/trunk/docs/img/DomainUpdate.png)

## 对域名记录的管理 ##
通常来讲，域名记录的管理从数量和复杂度上都远高于对named.conf的操作。所以我们尽量使用BIND的API进行操作。这个API就是DNS协议中的update接口，由于这个接口是基于Socket的接口，所以对于数据文件的冲突、多台服务器间的复制等工作都交给BIND自身来进行。这样可以保证数据一但被BIND接受，哪么一定会是正确的。

对于域名记录的操作，通常如下图所示：

![http://xbaydns.googlecode.com/svn/trunk/docs/img/RecordUpdate.png](http://xbaydns.googlecode.com/svn/trunk/docs/img/RecordUpdate.png)

# 附注 #
GSLB（Global Server Load Balance），它的作用是让每一个互联网的用户能够访问到与自己最近的服务，同时也基于整个互联网提供负载均衡的能力。

# ToDo #
  * 我们还会对named.conf文件的操作可能产生的冲突进行深入的研究，尝试寻找一些更好的方法进行处理。欢迎大家提出自己的想法和建议。
  * 针对于named.conf的分发还没有细的研究，但是，在主服务器的工作告一段落后，我们会进行这方面的深入研究和实现。