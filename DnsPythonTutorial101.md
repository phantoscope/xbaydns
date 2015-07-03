# dnspython 简明入门教程 #

（整理中……）

## 适合读者 ##

在开始进一步的阅读之前，本教程假设您至少了解或具有下列知识或经验：
  * 对 DNS 域名体系的基本知识具有一定的了解；
  * 能读懂简单的 zone 配置文件；
  * 能使用 `nslookup` 进行简单的操作；
  * 熟悉 Python 程序设计语言。

## 目录 ##

  * dnspython 简介
  * 安装 dnspython
  * dnspython 的 API 文档
  * 在 Python 交互环境中学习本教程
  * 对域名进行操作
  * 一些 DNS 参数及其在 dnspython 中的定义
    * Domain System Class
    * Resource Record Type
    * 更多参数
  * 使用解释器
    * Resolver 和 Stub Resolver
    * 模块 dns.resolver
  * 使用 dnspython 操作 zone 数据
    * 理解一些 dnspython 的类及其之间的关系
    * 读取 Zone 信息
    * 向 Zone 对象中添加记录
  * ...

## dnspython 简介 ##

**dnspython** 是用于 Python 程序设计语言的 DNS 工具。
  * 支持几乎所有的记录类型。
  * 可以用于查询、传输以及动态更新zone信息。
  * 支持 TSIG（Transaction SIGnature，事务签名）认证消息以及 EDNSO（Extended DNS，扩展DNS）。

**dnspython** 同时提供了高层级和低层级访问DNS的能力。
  * 高层级的类为指定了名称、类型和类的数据处理查询。
  * 低层级的类允许程序直接处理 DNS 的 zone、消息、名称和记录。

## 安装 dnspython ##

**dnspython** 完全由 Python 语言实现，因此，安装 dnspython 相当方便。

| 提示：许多 Linux 发行版的软件仓库中都包含 dnspython。例如，在 Ubuntu 中，可以使用 apt-get install python-dnspython 来安装。 |
|:--------------------------------------------------------------------------------------------|

  * 访问 dnspython 下载页面： http://www.dnspython.org/kits/1.5.0/
  * 下载最新版本的 dnspython，目前是 dnspython-1.5.0.tar.gz，解开压缩包。Windows 用户可以下载 dnspython-1.5.0.win32.exe 安装包。
  * 有许多种方法可以安装 dnspython：
    * 进入解开的文件夹，运行 `python setup.py install`。
    * 或者，简单地将加开的文件夹放置到环境变量 `PYTHONPATH` 所指向的文件夹中。例如 `/usr/lib/python2.5/site-packages` 或者 `C:\Python25\Lib\site-packages` 等，根据你的操作系统和 Python 环境而定。
    * 或者，也可以使用 setuptools 的 `easy_install` 命令安装该文件。
    * Windows 下还可以使用 .exe 安装包直接安装。
  * 启动一个 Python 交互式环境，输入 `import dns`，如果一切正常，将不会有额外的输出信息。

## dnspython 的 API 文档 ##

  * **dnspython** 为程序员准备了近乎完美的 API 文档（由 epydoc 生成）。
  * 您可以通过 http://www.dnspython.org/docs/1.5.0/html/ 在线访问。
  * 您也可以通过 http://www.dnspython.org/kits/1.5.0/ 下载该文档到本地。

## 在 Python 交互环境中学习本教程 ##

  * 本教程主要通过具体的例子来帮助读者学习、理解和掌握 dnspython。在接下来的部分，我们的实例可以在一个连续的 Python 交互环境中进行。
  * 进入终端(或者控制台，这取决于您习惯如何称呼它)，执行 `python` 进入交互式的 Python 环境。
  * 或者，您也可以使用您喜欢的 Python 交互式环境，例如 pyshell 等，通常一些增强的 shell 提供了代码自动补全以及语法高亮功能，可能会对您的学习提供额外的帮助。

## 对域名进行操作 ##

  * 域名是 DNS 系统中最基本的对象。
  * dnspython 通过类 [dns.name.Name](http://www.dnspython.org/docs/1.5.0/html/public/dns.name.Name-class.html) 提供了对域名信息进行封装。
  * 对于类 [dns.name.Name](http://www.dnspython.org/docs/1.5.0/html/public/dns.name.Name-class.html) 的实例，我们可以进行一些操作。
  * 请看下面的例子（已经准备好了交互式 Python 环境了吗）：

```
>>> import dns.name

>>> n1 = dns.name.from_text('google.com')
>>> print type(n1)
<class 'dns.name.Name'>
```

  * 首先，我们导入模块 `dns.name`。
  * 通过函数 `dns.name.from_text()`，我们很方便的从字符串 `google.com` 创建了一个类 `dns.name.Name` 的实例。
  * 随后，我们通过 `type()` 函数证实了这一点。
  * 让我们再创建几个类 `dns.name.Name` 的实例。

```
>>> n0 = dns.name.from_text('com')
>>> n2 = dns.name.from_text('www.google.com')
>>> n3 = dns.name.from_text('www.google.cn')
```

  * 类 `dns.name.Name` 的方法 `is_subdomain()` 和 `is_superdomain` 可以帮助我们判读一个域名是否是另一个域名的子域或者超域。

```
>>> n0.is_superdomain(n2)
True
>>> n0.is_superdomain(n3)
False
>>> n2.is_subdomain(n1)
True
>>> n3.is_subdomain(n1)
False
>>> n1.is_subdomain(n1)
True
>>> n1.is_superdomain(n1)
True
```

  * 通过上面的例子我们看到，`com` 是 `www.google.com` 的 super domain，不是 `www.google.cn` 的 super domain。反过来说，`www.google.com` 是 `com` 的 subdoamin 成立，而 `www.google.cn` 是 `com` 的 subdomain 不成立。
  * 我们还意识到一个 `dns.name.Name` 总是自己的 super domain 和 subdomain。
  * 让我们看看如何处理域名间的相对关系：

```
>>> r1 = n2.relativize(n1)
>>> print r1
www
>>> r2 = n2 - n1
>>> r1 == r2
True
```

  * 我们看到，通过 `relativize()` 方法可以获得一个域名相对其 superdomain 的部分，例如 n2 相对 n1 的部分是 www。
  * 我们也可以使用减(-)操作得到等价结果。那么，是否可以使用加(+)操作处理域名呢？

```
>>> r1 + n1 == n2
True
```

  * 答案是肯定的。
  * [dnspython 的示例页面](http://www.dnspython.org/examples.html)中 Manipulate domain names 一节也提供了一些操作域名的例子。
  * 类 `dns.name.Name` 也支持通配符，例如，您可以使用 `dns.name.from_text('*.google.com')` 来创建一个使用通配符的实例。
  * 更详尽的关于类 `dns.name.Name` 的信息，请参考 [API 文档](http://www.dnspython.org/docs/1.5.0/html/public/dns.name.Name-class.html)。

## 一些 DNS 参数及其在 dnspython 中的定义 ##

  * 在玩了一点域名操作魔术之后，在进行实质性的工作之前，我们先来复习一下一些 DNS 的知识。
  * 本节中，我们主要是复习一下 DNS 的参数。

### Domain System Class ###

  * 域名体系类(Domain System Class)是一个 16 位数值的编码，用于表示一组或者一个协议。我们最经常使用 class 是 IN，表示 Internet 系统。此外，经常在文献中提及的还有 CH，表示 Chaos 系统，等等。
  * 在 [RFC1035](http://tools.ietf.org/html/rfc1035) 和其它一些文献中，定义了域名体系类(Domain System Class)，以下是一些常用的类：

| **十进制数值** | **名称**    | **表示** |
|:----------|:----------|:-------|
| 1            | 互联网       | IN     |
| 3            | Chaos(CH) | CH     |
| 255       | 任意(仅用于 QCLASS) |        |

  * 模块 [dns.rdataclass](http://www.dnspython.org/docs/1.5.0/html/public/dns.rdataclass-module.html) 定义了这些常数（Python 中并不存在常数的概念，不过根据习惯我们这么称呼它）。
  * 我们可以在 Python 中通过 `dns.rdataclass.IN` 或者 `dns.rdataclass.from_text('IN')` 来表示 IN class。

### Resource Record Type ###

  * 资源记录类型(Resource Record Type)是一个 16 位数值的编码，表示资源记录中资源的类型。这里类型指的是抽象的资源。
  * 在 [RFC1035](http://tools.ietf.org/html/rfc1035) 等一些文献中，定义了资源记录类型(Resource Record Type)，以下是一些 IN class 中常用的类型：

| **类型** | **值** | **含义** |
|:-------|:------|:-------|
| A      |  1    | 主机地址   |
| NS     |  2    | 经过授权的名称服务器 |
| CNAME  |  5    | 用作别名的规范名称 |
| SOA    |  6    | 标记开始一个授权区域 |
| PTR    | 12    | 域名指针   |
| MX     | 15    | 邮件交换   |
| TXT    | 16    | 文本字符串  |

  * 模块 [dns.rdatatype](http://www.dnspython.org/docs/1.5.0/html/public/dns.rdatatype-module.html) 定义了这些常数。
  * 我们可以在 Python 中通过 `dns.rdatatype.MX` 或者 `dns.rdataclass.from_text('MX')` 来表示 MX 类型。
  * `dns.rdatatype` 中的定义只是类型本身，我们知道，不同类型的记录具有不同的信息，那么在 dnspython 中是如何定义的呢？
  * 在 dnspython 中，通过类 [dns.rdata.Rdata](http://www.dnspython.org/docs/1.5.0/html/public/dns.rdata.Rdata-class.html) 的子类来表示各种类型的记录。
  * 例如：
    * 类 [dns.rdtypes.IN.A.A](http://www.dnspython.org/docs/1.5.0/html/public/dns.rdtypes.IN.A.A-class.html) 是 A 记录的抽象，其实例具有属性 `address`。
    * 类 [dns.rdtypes.ANY.MX.MX](http://www.dnspython.org/docs/1.5.0/html/public/dns.rdtypes.ANY.MX.MX-class.html) 是 MX 记录的抽象，其实例具有属性 `exchange` 和 `preference`。
  * 使用 dnspython 进行查询、修改等操作时，我们将非常频繁的与这些 `dns.rdata.Rdata` 的子类打交道。因此，花一点时间研读一下相应的 [API 文档](http://www.dnspython.org/docs/1.5.0/html/public/dns.rdata.Rdata-class.html)绝对是值得的。

### 更多参数 ###

  * 操作代码(Operation Code)，如 Query、Notify、Update 等，对应的模块是 [dns.opcode](http://www.dnspython.org/docs/1.5.0/html/public/dns.opcode-module.html)。
  * 响应代码(Response Code)，如 NoError、FormErr 等，对应的模块是 [dns.rcode](http://www.dnspython.org/docs/1.5.0/html/public/dns.rcode-module.html)。对于各种用于表示出错的响应代码，在模块 [dns.exception](http://www.dnspython.org/docs/1.5.0/html/public/dns.exception-module.html) 中具有相应 Exception 类。
  * 要了解更详尽的信息，请阅读 [DOMAIN NAME SYSTEM PARAMETERS](http://www.iana.org/assignments/dns-parameters)，这是一份提纲挈领性质的文件，列出了较本节更详尽的信息，以及定义这些信息的相应的 RFC 编号。

## 使用解释器 ##

### Resolver 和 Stub Resolver ###

  * 关于解释器(resolver)和桩解释器(stub resolver)的详细信息，请参考 [RFC 1034](http://tools.ietf.org/html/rfc1034)。
  * 简单的说：
    * 解释器(resolver)是用户程序与域名服务器之间的接口。
    * 桩解释器(stub resolver)是一种 resolver 的实现方案：
      * 并未在本地实现完整的 resolver 所需的功能。
      * 通过访问支持递归查询的域名服务器来实现 resolver 的功能。

### 模块 dns.resolver ###

  * 使用模块 [dns.resolver](http://www.dnspython.org/docs/1.5.0/html/public/dns.resolver-module.html)，我们可以实现一些类似 `nslookup` 的功能。
  * 模块 `dns.resolver` 定义了类 [dns.resolver.Resolver](http://www.dnspython.org/docs/1.5.0/html/public/dns.resolver.Resolver-class.html)，这是一个 stub resolver。
  * 模块 `dns.resolver` 还定义了类 [dns.resolver.Answer](http://www.dnspython.org/docs/1.5.0/html/public/dns.resolver.Answer-class.html)，用于封装 Resolver 的返回信息。
  * 操作中，我们可以将类 `dns.resolver.Answer` 的实例看作是包含若干 `dns.rdata.Rdata` 某个子类的实例的列表。
  * 下面，将通过具体的例子来讲解如何使用 `dns.resolver`。例如，我们想要查询 gmail.com 这个域名的邮件交换记录。
  * 在 `nslookup` 中，我们会这么做：

```
$ nslookup
> set type=MX
> gmail.com
```

  * 我们将会得到类似下面的信息：

```
...

gmail.com       MX preference = 5, mail exchanger = gmail-smtp-in.l.google.com
gmail.com       MX preference = 10, mail exchanger = alt1.gmail-smtp-in.l.google.com
gmail.com       MX preference = 10, mail exchanger = alt2.gmail-smtp-in.l.google.com
gmail.com       MX preference = 50, mail exchanger = gsmtp163.google.com
gmail.com       MX preference = 50, mail exchanger = gsmtp183.google.com

...
```

  * 使用 `dns.resolver`，我们可以这么做：

```
>>> import dns.resolver

>>> answers = dns.resolver.query('gmail.com', 'MX')
>>> for rdata in answers:
...     print 'MX preference =', rdata.preference, 'mail exchanger =', rdata.exchange
```

  * 我们将会得到类似下面的运行结果：

```
MX preference = 5 mail exchanger = gmail-smtp-in.l.google.com.
MX preference = 10 mail exchanger = alt1.gmail-smtp-in.l.google.com.
MX preference = 10 mail exchanger = alt2.gmail-smtp-in.l.google.com.
MX preference = 50 mail exchanger = gsmtp163.google.com.
MX preference = 50 mail exchanger = gsmtp183.google.com.
```

  * 和 `nslookup` 的返回结果比较一下，是否大体上是一致的？
  * 在这个例子中，我们使用 `dns.resolver.query(...)` 进行查询，这实际上是调用默认的 Resolver 实例进行的，相当于：

```
R = dns.resolver.get_default_resolver()
R.query(...)
```

  * `nslookup` 缺省使用系统默认的域名服务器进行查询，`dns.resolver.Resolver` 也是如此。在 POSIX 兼容环境中，这是通过初始化 Resolver 实例时读取 `/etc/resolv.conf` 配置文件，在 Windows 中，这是通过读取注册表，来实现的。
  * 大多数情况下，我们使用 `dns.resolver.query(...)` 函数就足够了。详细参数请查阅 [API 文档](http://www.dnspython.org/docs/1.5.0/html/public/dns.resolver-module.html#query)。

## 使用 dnspython 操作 zone 数据 ##

  * 传统上（根据 [RFC 1034](http://tools.ietf.org/html/rfc1034) 的阐述），域名体系假设所有的数据都来源于分布于域名体系的各个主机上的主文件(master files)中。这些主文件由本地系统管理员负责更新。它们是可以被本地域名服务器读取的文本文件，并经由域名服务器得以被域名体系的用户访问。
  * 这些文本文件中信息最多的组成部分是用于描述各个区域(Zone)的定义的文件。
  * **dnspython** 提供了强大的功能帮助我们访问和处理 Zone 信息。

### 理解一些 dnspython 的类及其之间的关系 ###

  * 类 [dns.zone.Zone](http://www.dnspython.org/docs/1.5.0/html/public/dns.zone.Zone-class.html) 表示一个 DNS 区域(Zone)。在数据结构上，可以理解为一个以节点名称(类 dns.name.Name 的实例)为键，以节点对象(类型为 dns.node.Node 的实例)为值的数据字典(dict)。
  * 类 [dns.node.Node](http://www.dnspython.org/docs/1.5.0/html/public/dns.node.Node-class.html) 表示一个 Zone 中节点。在数据结构上，一个节点可以理解为一组资源记录数据集(类 dns.rdataset.Rdataset 的实例)的实例的列表(list)。
  * 类 [dns.rdataset.Rdataset](http://www.dnspython.org/docs/1.5.0/html/public/dns.rdataset.Rdataset-class.html) 表示一组具有相同 class 和 type 的记录。在数据结构上，一个 dns.rdataset.Rdataset 可以理解为一组 dns.rdata.Rdata 的同一个子类的实例组成的列表(list)。
  * 下面的草图可以帮助我们理解上述各个类之间的关系：

```
    +---------------+ 1           * +---------------+
    | dns.zone.Zone |---------------| dns.node.Node |
    +---------------+               +---------------+
                                            | 1
                                            |
                                            | *
   +-----------------+ *       1 +-----------------------+           
   | dns.rdata.Rdata |-----------| dns.rdataset.Rdataset |
   +-----------------+           +-----------------------+
```

### 读取 Zone 信息 ###

  * 模块 [dns.zone](http://www.dnspython.org/docs/1.5.0/html/public/dns.zone-module.html) 提供了三种读取现有数据生成 `dns.zone.Zone` 实例的函数。
  * 它们分别是 `from_file()`、`from_text()` 以及 `from_xfr()`。
  * 本节主要使用 `from_text()` 函数进行示例，`from_file()` 的使用与其类似。
  * 关于 `from_xfr()` 函数的使用，我们将在稍后的章节提及。
  * 首先，我们先准备一个用于示例的区域信息字符串，具有 Bind 管理经验的读者应该很熟悉：

```
>>> dataString = """$TTL    604800
... @       IN      SOA     example.com. webmaster.example.com. (
...                               1         ; Serial
...                          604800         ; Refresh
...                           86400         ; Retry
...                         2419200         ; Expire
...                          604800 )       ; Negative Cache TTL
... ;
... @       IN      NS      ns1.example.com.
... @       IN      NS      ns2.example.com.
... @       IN      A       127.0.0.1
... www     IN      A       127.0.0.1
... ftp     IN      A       127.0.0.1
"""
```

  * 正像这个 Zone 数据显示我们将在 example.com 这个域名下工作，为了方便，我们为之定义一个 `dns.name.Name` 对象。

```
>>> originName = dns.name.from_text("exmaple.com")
```

  * 从上面的 `dataString` 中生成 `dns.zone.Zone` 对象非常容易：

```
>>> import dns.zone
>>> 
>>> zoneObj = dns.zone.from_text(dataString, originName, relativize=False)
>>> print type(zoneObj)
<class 'dns.zone.Zone'>
```

  * 上面我们提到，可以将 `dns.zone.Zone` 理解为一个 `<dns.name.Name, dns.node.Node>` 序偶的数据字典。因此下面的例子可以帮助我们方便的了解一个 `dns.zone.Zone` 对象包含什么样的信息：

```
>>> def printZone(zoneObj):
...     names = zoneObj.nodes.keys()
...     names.sort()
... 
...     for name in names:
...         print zoneObj.nodes[name].to_text(name)
```

  * 现在，让我们执行该函数，看看我们之前的 zoneObj 对象包含了什么信息：

```
>>> printZone(zoneObj)
exmaple.com. 604800 IN SOA example.com. webmaster.example.com. 1 604800 86400 2419200 604800
exmaple.com. 604800 IN NS ns1.example.com.
exmaple.com. 604800 IN NS ns2.example.com.
exmaple.com. 604800 IN A 127.0.0.1
ftp.exmaple.com. 604800 IN A 127.0.0.1
www.exmaple.com. 604800 IN A 127.0.0.1
```

  * 函数 `printZone()` 主要是通过 `dns.node.Node` 对象的 `to_text()` 方法输出文本的。
  * 在实际使用中，我们需要更细致的对 `dns.node.Node` 对象中的信息进行操作。
  * 回顾一下前面提到的一些 dnspython 类之间的关系，大家跟我一起默念，一个 Zone 包含多个 Node，一个 Node 包含多个 Rdataset，一个 Rdataset 包含多个 Rdata，……
  * 好的，现在你已经掌握 dnspython 处理 Zone 的万能魔咒了！改进一下 `printZone`：

```
>>> import dns.rdataclass, dns.rdatatype
>>> 
>>> def printZone2(zoneObj):
...     names = zoneObj.nodes.keys()
...     names.sort()
... 
...     for name in names:
...         node = zoneObj[name]
...         print "================================"
...         print "Node Name:", name
...         print "================================"
...         for rdataset in node.rdatasets:
...             print "Class: ", dns.rdataclass.to_text(rdataset.rdclass), \
                      "Record Type: ", dns.rdatatype.to_text(rdataset.rdtype)
...             for rdata in rdataset:
...                 print "rdata:", rdata
...             print "--------------------------------"
...         print "================================"
```

  * 现在，让我们执行该函数，看看其运行结果如何：

```
>>> printZone2(zoneObj)
================================
Node Name: exmaple.com.
================================
Class:  IN Record Type:  SOA
rdata: example.com. webmaster.example.com. 1 604800 86400 2419200 604800
--------------------------------
Class:  IN Record Type:  NS
rdata: ns1.example.com.
rdata: ns2.example.com.
--------------------------------
Class:  IN Record Type:  A
rdata: 127.0.0.1
--------------------------------
================================
================================
Node Name: ftp.exmaple.com.
================================
Class:  IN Record Type:  A
rdata: 127.0.0.1
--------------------------------
================================
================================
Node Name: www.exmaple.com.
================================
Class:  IN Record Type:  A
rdata: 127.0.0.1
--------------------------------
================================
```

  * 看，我们已经能够从 Zone 对象开始层层深入，直至其中的每一个资源记录了，不是吗？

### 向 Zone 对象中添加记录 ###

  * 接下来，我们打算在上述区域中增加一个 mail.example.com 的 A 记录，并将 example.com 的 MX 记录设置为 mail.example.com。
  * 首先，让我们创建一个 A 记录：

```
>>> import dns.rdata
>>> 
>>> newRdata = dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.A, "127.0.0.1")
```

  * 要如何将之放置到 `zoneObj` 中呢？
  * 在 `zoneObj` 中查找 `mail.example.com` 节点，如果不存在就创建它。

```
newNode = zoneObj.find_node(dns.name.from_text("mail", originName), create=True)
```

  * 接下来，在这个节点中查找 class 为 IN，type 为 A 的 rdataset，如果不存在就创建它。

```
newRdataset = newNode.find_rdataset(dns.rdataclass.IN, dns.rdatatype.A, create=True)
```

  * 现在，可以把我们新建的 A 记录放到相应的 RdataSet 中了：

```
>>> newRdataset.add(newRdata)
```

  * 在此执行我们的自定义函数 `printZone()`，确认我们的改动是否已经生效：

```
>>> printZone(zoneObj)
exmaple.com. 604800 IN SOA example.com. webmaster.example.com. 1 604800 86400 2419200 604800
exmaple.com. 604800 IN NS ns1.example.com.
exmaple.com. 604800 IN NS ns2.example.com.
exmaple.com. 604800 IN A 127.0.0.1
ftp.exmaple.com. 604800 IN A 127.0.0.1
mail.exmaple.com. 0 IN A 127.0.0.1
www.exmaple.com. 604800 IN A 127.0.0.1
```

  * 注意到 mail.example.com 已经加入其中了吗？
  * TODO: TTL 的问题
  * 类似的，下面代码可以用于在 `zoneObj` 中添加一条 MX 记录：

```
>>> newNode = zoneObj.find_node(dns.name.from_text("", originName), create=True)
>>> newRdataset = newNode.find_rdataset(dns.rdataclass.IN, dns.rdatatype.MX, create=True)
>>> newRdata = dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.MX, "10 mail.example.com")
>>> newRdataset.add(newRdata)
>>> printZone(zoneObj)
exmaple.com. 604800 IN SOA example.com. webmaster.example.com. 1 604800 86400 2419200 604800
exmaple.com. 604800 IN NS ns1.example.com.
exmaple.com. 604800 IN NS ns2.example.com.
exmaple.com. 604800 IN A 127.0.0.1
exmaple.com. 0 IN MX 10 mail.example.com
ftp.exmaple.com. 604800 IN A 127.0.0.1
mail.exmaple.com. 0 IN A 127.0.0.1
www.exmaple.com. 604800 IN A 127.0.0.1
```

## TODO ##

  * dns.zone.from\_xfr() 的用法
  * dns.query.Query 以及 dns.update.Update 的用法