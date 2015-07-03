# 区数据文件 #
[[PageOutline](PageOutline.md)]
区数据文件用来存储一个域中的资源记录。这些资源记录说明了域中所有的主机，当然，它也可以说明一些其它的如子域这样的信息。总之，说明一个域的内容的信息都是存储在这个文件中。这个文件是由named.conf引用的。


# 示例 #
```
$TTL 1h

sina.com.cn. IN SOA localhost. hd.localhost. (
        20071019 ; serial
        3h       ; refresh
        1h       ; retry
        1w       ; expiration
        1h )     ; minimum

sina.com.cn.    IN      NS      ns1.sina.com.cn.
ns1             IN      A       10.217.24.63
ns2             IN      A       192.168.1.104

```