# 这里说明bind的基本操作 #
[[PageOutline](PageOutline.md)]

## bind控制命令 ##
### 启动bind ###
不同的操作系统可能会使用不同的方法启动bind，在openbsd中使用一个chroot来启动bind，而在linux中有时它是直接启动的一个进程。通常情况下bind的启动命令是
```
/usr/sbin/named
```
它会默认配置文件的路径是/etc/named.conf。特别的，在openbsd下，运行bind的chroot把root设置在了/var/named中，所以配置文件就是/var/named/etc/named.conf了。

#### OpenBSD的bind启动 ####
openbsd没有单独的bind启动命令。需要在/etc/rc.conf中将named打开：
```
named_flags=""
```
使用rc脚本启动：
```
sudo sh /etc/rc
```

#### ubuntu的bind启动 ####
可以使用init.rd中的启动脚本启动：
```
sudo /etc/init.rd/named start
```

#### OSX中的bind启动 ####
在osx中需要使用launchd来启动named：
```
sudo service org.isc.named start
```
在osx下需要对named做一些配置，参见[在OSX下配置DNS服务器](http://blog.opensource.org.cn/hdcola/2007/10/osxdns.html)

### 停止bind ###
可以使用rndc直接停止：
```
sudo rndc stop
```
#### ubuntu的bind停止 ####
除了使用rndc来停止服务，也可以使用init.rd中的脚本：
```
sudo /etc/init.rd/named stop
```

### 重新加载配置 ###
使用rndc进行：
```
sudo rndc reload
```

## bind配置文件 ##
bind的配置文件主要有三种，最基础的是named.conf文件，它是bind启动时所需要的文件，其它的配置文件都是由它引用来的。第二个是rndc.conf文件，它默认会被named.conf包含，里面存储着rndc的客户端的认证key。第三类是zone数据库文件，这些文件说明每一个域的具体信息。

通常来讲named.conf文件都存储在/etc/named.conf中。

## rndc操作 ##
rndc是用于对域名服务器进行控制的命令，所有的bind控制指令都是由rndc发出的。通常rndc的语法如下：
```
rndc [-b source-address] [-c config-file] [-k key-file] [-s server] [-p port] [-V] [-y key_id] {command}
```

### 参数说明 ###
  * -b source-address
使用指定的源地止连接到目标服务器上。

  * -c config-file
使用指定的配置文件启动rndc。缺省的情况下，rndc使用的配置文件存在/etc/rndc.conf。

  * -k key-file
使用指定的key文件。缺省的情况下，rndc使用的key文件存在/etc/rndc.key。

  * -s server
连接到的目标服务器地址，也就是使用rndc控制的目标服务器地址。缺省的目标服务器可以通过rndc.conf指定，如果没有指定哪么就会是127.0.0.1。

  * -p port
连接到目标机器的端口号。缺省是953。

  * -V
打开详细的log信息。

> -y keyid
使用key文件中指定的keyid。

### 支持的命令 ###
  * reload
重新加载配置文件和zone。

  * reload zone [[view](class.md)]
重新加载一个单独的zone。

  * refresh zone [[view](class.md)]
安排立即维护某个zone。

  * retransfer zone [[view](class.md)]
不检查序列号，重新传输一个zone。

  * freeze zone [[view](class.md)]
中止更新一个动态zone，并将这个zone的动态更新数据合并进区数据文件中去。

  * thaw zone [[view](class.md)]
打开一个冻结的动态zone，并且重新加载它的数据。

  * reconfig
重新加载配置文件，同时只更新新的zone数据。

  * stats
将服务器的统计信息写到统计文件中。注意，它会放到服务器的当前目录下的named.stats中。

  * querylog
触发查询的记录日志。

  * dumpdb [-all|-cache|-zones] [...](view.md)
把缓存导出到一个文件中。注意，它会导出到服务器的当前目录下的named\_dump.db。

  * stop
保存没完成的更新到master文件，并且停止服务器。

  * stop -p
保存没完成的更新到master文件，并且停止服务器，并给出进程号。

  * halt
停止域名服务器，不将没完成的更新保存完成。

  * halt -p
停止域名服务器，不将没完成的更新保存完成，并给出进程号。

  * trace
将调试信息附加到服务器的当前目录下的named.run后面。

  * trace level
设置调试级别。

  * notrace
关闭调试。

  * flush
将cache都flush。

  * flush [view](view.md)
将一个view的cache flush。

  * flushname name [view](view.md)
将输入的名称的cache进行flush。

  * status
显示服务器的状态信息。

  * recursing
dump出当前所有的递归查询。