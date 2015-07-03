# named.conf说明 #
[[PageOutline](PageOutline.md)]
named.conf都会存在/etc中。它说明了bind的配置，但是它通常并不包括域名数据库文件。所有bind的控制选项都是在named.conf中设置的。

# acl #
生成地址的匹配列表变量
语法：
```
acl name {
    address_match_list;
};
```

# include #
将指定的文件插入到include语句的地方
语法：
```
include path_name;
```

# options #
## options forward-only ##
让你的域名服务器只使用转发器来解析域名

## options no-recursion ##
使域名服务器不执行域名的递归解析

# view #
创建并配置一个视图

# zone #
配置域名服务器所管理的区

# 示例 #
```
acl clients {
        localnets;
        ::1;
};

options {
        version "";     // remove this to allow version queries

        listen-on    { any; };
        listen-on-v6 { any; };

        allow-recursion { clients; };
};

logging {
        category lame-servers { null; };
};

zone "." {
        type hint;
        file "standard/root.hint";
};

zone "localhost" {
        type master;
        file "standard/localhost";
        allow-transfer { localhost; };
};

zone "127.in-addr.arpa" {
        type master;
        file "standard/loopback";
        allow-transfer { localhost; };
};

zone "0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa" {
        type master;
        file "standard/loopback6.arpa";
        allow-transfer { localhost; };
};

zone "sina.com.cn" {
        type master;
        file "master/sina.com.cn";
};
```