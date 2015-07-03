# 简介 #

xbaydns-tools是系列工具。这系列工具用于完成 xbaydns的辅助工作，它们将系统逻辑进行封装，同时扩展系统功能，更多的，把大量人工进行的工作通过计算机来完成。


# 说明 #

## logtolist ##
logtolist用以将收集到的dns log转换成为性能agent的反向探测数据库。
输入：dns的query log
输出：性能agent的ip list数据
处理：
  * 提取IP数据
  * 对IP数据进行排重
  * 转换IP数据为agent所需要的格式

### agent ###
agent将一组ip数据做为目标，进行网络的速度探测。它会将性能探测的数据收集起来，以供将来的分析。
输入：logtolist的ip列表数据
输出：测试结果
处理：
  * 十分钟一次，一次五个包
  * 尝试 ping
  * 尝试 DNS Lookup
  * 尝试 网关 ping

### idcview ###
idcview将aggent测试出来的结果集，统计和计算出servergroup和view之间的对应关系。使得gslb的策略能应用到GSLB系统中去。
输入：agent的测试结果
输出：xbaydns的管理工具所需要的ip地址访问策略
处理：
  * 目录下的所有的结果进行汇总（文件名：agent\_日期）
  * 对同一ip地址的结果进行对比
  * 加权平均后得出一个ip地址的idc速度顺序