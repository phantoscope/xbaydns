# 教学与入门 #
  * [DNS入门PPT](http://docs.google.com/Presentation?id=dtpwt9z_201ftcgdj)
  * [DNS分布PPT](http://docs.google.com/Presentation?id=dtpwt9z_354hqzcph)
  * [BIND跟踪与调试PPT](http://docs.google.com/Doc?id=dtpwt9z_423fmrhgq)
以上PPT是学习使用，在讲解过一次后会有视频放在首页
  * [nslookup的使用](http://code.google.com/p/xbaydns/wiki/nslookup)
  * [bind的named.conf配置项](http://code.google.com/p/xbaydns/wiki/bindconf)
  * [bind的基本操作指令](http://code.google.com/p/xbaydns/wiki/bin9base)
  * [区数据文件配置项](http://code.google.com/p/xbaydns/wiki/zonedata)

# 系统结构和功能 #
  * 在系统中支持百万条域名记录
  * 在系统中支持多点分布的部署
  * 在系统中支持大容量的dns查询
  * 支持web上的数据管理
  * 通过访问路径优化用户访问速度

# 已经知的挑战 #
  * DNS基于view的部署与实施
  * 由于加入了view，哪么bind的整体管理和部署
  * 由于数据量很大，所以系统结构会非常重要
  * 访问路径优化的方法和实施策略