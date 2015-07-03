# 接口定义 #
## 文件：xbaydns/dnsapi/namedconf.py ##
### 类：class NamedConf ###
#### addAcl ####
addAcl (acl,aclmatch)
增加一个acl

参数说明：
  * acl 要增加的acl的名称
  * aclmatech 增加的acl中的match地址

例子:
> 在名为internal的acl中增加一个叫127.0.0.1的match地址
  * addAcl('internal',['127.0.0.1',])

#### delAcl ####
delAcl(acl)
删除一个acl

参数说明：
  * acl 要删除的acl的名称

例子:
> 删除名为internal的acl
  * delAcl('internal')

## addView ##
  * addView(view,match-client)
增加view

参数说明：
  * view 增加的view的名称
  * match-client 匹配于该view的acl汇总（列表）

例子:
添加名为internal的view,acl为['127.0.0.1','10.10.10.10/24',]
> ＊addView('internal',['127.0.0.1','10.10.10.10/24',])

## updateView ##
updateView(view,match-client)
更新view

参数说明：
  * view 增加的view的名称
  * match-client 匹配于该view的acl汇总

例子:
  * pdateView('internal',['127.0.0.1',])

## delView ##
delView(view)
删除view

参数说明：
  * view 要删除的view的名称

## update record ##
update record(view,domain,record)

更新DNS记录。对于记录的操作我们尽量使用dns的接口进行，因为使用接口可以保证数据的一致性，同时也会减少服务器对于错误数据的实时判断，最重要的它还支持了全网服务器的IXFR的区数据同步。整体的操作如下图所示：

![http://xbaydns.googlecode.com/svn/trunk/docs/img/RecordUpdate.png](http://xbaydns.googlecode.com/svn/trunk/docs/img/RecordUpdate.png)

参数说明：
  * view：需要更新记录所属view的名称
  * domain：需要更新记录所属domain的名称
  * record：要更新记录的数据。参考pythondns的相关函数

工作流程：
  1. 按照view的名称找到TSIG的key
  1. 使用找到的key向localhost的dns服务器发出一个更新记录的请求

## add record ##
add record(view,domain,record)

增加DNS记录

参数说明：
  * view：需要更新记录所属view的名称
  * domain：需要更新记录所属domain的名称
  * record：要增加记录的数据。参考pythondns的相关函数

工作流程：
  1. 按照view的名称找到TSIG的key
  1. 使用找到的key向localhost的dns服务器发出一个更新记录的请求

## del record ##
del record(view,domain,record)
删除DNS记录

参数说明：
  * view：需要更新记录所属view的名称
  * domain：需要更新记录所属domain的名称
  * record：要删除记录的数据。参考pythondns的相关函数

工作流程：
  1. 按照view的名称找到TSIG的key
  1. 使用找到的key向localhost的dns服务器发出一个更新记录的请求

## add domain ##
add domain(domain)
增加一个DNS域。增加DNS的域是需要做与BIND相关的工作，重点在bind的named.conf文件上。由于是配置文件，所以在操作完成之前都需要做一个检查，否则会出现问题。现在没有考虑更多的slave的问题，先把master的dns更新解决，再讨论slave的问题。总体的更新流程如下图所示：

![http://xbaydns.googlecode.com/svn/trunk/docs/img/DomainUpdate.png](http://xbaydns.googlecode.com/svn/trunk/docs/img/DomainUpdate.png)

参数说明：
  * domain 需要增加的DNS域名

所属文件:
  * xbaydns/tools/namedconf.py

工作流程：
  1. 确认本机是否有该DNS域名的解晰，如果没有继续，如果有，则返回已经有该域回的exception
  1. 在本机的named.conf中的每一个view中增加该域的zone声明
  1. 使用 named-checkconf 检查zone文件的书写正确性
  1. 在本机的dynamic目录中增加每个view该域的缺省zone数据区文件
  1. 使用named-checkzone检查zone数据区文件的书写正确性
  1. 将相应的文件复制到运行目录中
  1. 使用rndc reload重新加载bind配置文件

## del domain ##
del domain(domain)
删除一个DNS域

参数说明：
  * domain 需要删除的DNS域名

所属文件:
  * xbaydns/tools/namedconf.py

工作流程：
  1. 在本机的dynamic目录中删除每个view该域的zone数据区文件和动态更新数据区文件
  1. 在本机的named.conf中的每一个view中增加该域的zone声明
  1. 使用 named-checkconf 检查zone文件的书写正确性
  1. 使用named-checkzone检查zone数据区文件的书写正确性
  1. 将相应的文件复制到运行目录中
  1. 使用rndc reload重新加载bind配置文件

## reload bind ##
reload bind([[view](view.md)],[[domain](domain.md)])
重载bind配置文件

参数说明：
  * view 重载的view名称
  * domain 重载的 domain名称

工作流程：
  1. 调用rndc的reload命令执行该指令

## sync bind ##
sync bind(remont)
从主机同步回本机的bind配置。本命令只定义，先不实现。在确认了bind的配置文件后再进行这个API的开发。

# 配置定义 #
  * sysconf.py

namedconf bind的named.conf文件路径。默认在FreeBSD下它指向了/etc/namedb。

nameddb  bind的nemd zone文件路径。默认在FreeBSD下它指向了/etc/namedb。

# 包定义 #
xbaydns/utils

一些通用的工具类

xbaydns/conf

一些通用的配置类

xbaydns/tests

系统的unit test代码

xbaydns/tools

系统使用的工具

## NSUpdate ##

### `__init__` ###

```
__init__(self, addr, domain, view = False, port = 53)
```

作用: NSUpdate对象进行初始化

参数说明：
  * addr 目标DNS服务器地址
  * domain 目标zone名称
  * view 目标view名称，默认无
  * port 目标DNS服务端口，默认53

例：
```
nsupdate_obj = nsupdate.NSUpdate('127.0.0.1', 'sina.com.cn.')
```

### `addRecord` ###

```
addRecord(self, recordlist)
```

作用：添加一条DNS记录

参数说明：
  * recordlist DNS记录列表，形式如下：
[[NAME, TTL, CLASS, TYPE, [RECORD\_STRING1, RECORD\_STRING2, ...]],...]
```
recordlist = [['foo', 3600, 'IN', 'A', ['202.108.33.32', '202.108.35.50']],
             ['', 86400, 'IN', 'MX', ['10 mx1', '20 mx2.sina.com.cn.']]]
```

### `removeRecord` ###

```
removeRecord(self, recordlist, entire_node = False)
```

作用：删除一条DNS记录，或整个节点

参数说明：
  * recordlist 当entire\_node为False时，同addRecord中的形式，但ttl可以忽略。
当entire\_node为True时，形式为：
[NAME1, NAME2,...]
```
recordlist = ['foo', 'bar']
```

### `updateRecord` ###

```
updateRecord(self, recordlist)
```

_NOT IMPLEMENT_

### `commitChanges` ###

```
commitChanges(self, timeout = None, usetcp = True)
```

作用：提交pending的更新

参数说明：
  * timeout 发送更新到DNS的超时时间，默认永远不超时。
  * usetcp 使用TCP连接，False时使用UDP。

### `queryRecord` ###

```
queryRecord(self, name, rdtype = 'A', usetcp = False, timeout = 30, rdclass = 'IN')
```

作用：在本对象初始化时所指定的view中查询

参数说明：
> 见queryRecord\_Independent

调用示例：
```
queryRecord('foo')
queryRecord('', rdtype = 'MX', usetcp = True)
queryRecord('bar', rdtype = 'CNAME', rdclass = 'ANY')
```

### `queryRecord_Independent` ###

```
queryRecord_Independent(self, name, view = False, rdtype = 'A', usetcp = False, timeout = 30, rdclass = 'IN')
```

作用：DNS查询

参数说明：
  * name 要查询的域名。
  * view 要查询的view名称，默认无
  * rdtype 要查询的记录类型，默认A。
  * usetcp 是否使用TCP连接，True时使用TCP连接。默认UDP。
  * timeout 查询超时时间，单位秒，默认30。
  * rdclass 要查询的记录CLASS，默认IN。

调用示例：
```
queryRecord_Independent('foo')
queryRecord_Independent('', rdtype = 'MX', usetcp = True)
queryRecord_Independent('bar', view = 'internal', rdtype = 'CNAME', rdclass = 'ANY')
```

### 出错处理 ###

_均抛出\*NSUpdateException\*类型的异常_