# nslookup使用 #

nslookup是一个非常容易使用的交互式dns客户端。我们会使用它的交互状态查看dns服务器的状态。你输入一个名字时它会按你的要求向dns服务器发出查询的请求并返回结果。

# server #
反回现在的服务器设置。或是将查询的目标服务器设置为你指定的服务器。

# set keyword[=value] #
set命令可以改变lookup的状态信息。
## set all ##
显示出所有set的参数信息。
## set [no](no.md)debug ##
打开或关闭调试信息。
## set type ##
设置查询的信息类型。（缺省为A）

# exit #
退出nslookup