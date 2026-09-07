# H3C R1110 三层技术-IP路由命令参考

H3C S6520X-EI & S6520X-HI系列以太网交换机三层技术 -IP 路由命令参考新华三技术有限公司http://www.h3c.com资料版本：6W100-20180821产品版本：Release 1110

未经本公司书面许可，任何单位和个人不得擅自摘抄、复制本书内容的部分或全部，并不得以任何形式传播。
H3C、 、H3CS、H3CIE、H3CNE、Aolynk、 、H Care、 、IRF、NetPilot、Netflow、SecEngine、SecPath、SecCenter、SecBlade、Comware、ITCMM、HUASAN、华三均为新华三技术有限公司的商标。对于本手册中出现的其它公司的商标、产品标识及商品名称，由各自权利人拥有。
由于产品版本升级或其他原因，本手册内容有可能变更。H3C 保留在没有任何通知或者提示的情况下对本手册的内容进行修改的权利。本手册仅作为使用指导，H3C 尽全力在本手册中提供准确的信息，但是 H3C 并不确保手册内容完全没有错误，本手册中的所有陈述、信息和建议也不构成任何明示或暗示的担保。

## 00-前言

前 言本命令参考主要介绍各路由协议命令，包括 IPv4、IPv6 网络的各种路由命令，以及影响路由选择或者路由表生成策略的命令。
前言部分包含如下内容：
• 读者对象
• 本书约定
• 资料意见反馈

### 读者对象

本手册主要适用于如下工程师：
网络规划人员
•
• 现场技术支持与维护人员
• 负责网络配置和维护的网络管理员

### 本书约定

#### 1. 命令行格式约定

格 式 意 义粗体 命令行关键字（命令中保持不变、必须照输的部分）采用加粗字体表示。
斜体 命令行参数（命令中必须由实际值进行替代的部分）采用斜体表示。
表示用“[ ]”括起来的部分在命令配置时是可选的。
[ ] { x | y | ... } 表示从多个选项中仅选取一个。
[ x | y | ... ] 表示从多个选项中选取一个或者不选。
{ x | y | ... } * 表示从多个选项中至少选取一个。
[ x | y | ... ] * 表示从多个选项中选取一个、多个或者不选。
&<1-n> 表示符号&前面的参数可以重复输入1～n次。
\# 由“#”号开始的行表示为注释行。

#### 2. 图形界面格式约定

格 式 意 义< > 带尖括号“ < > ”表示按钮名，如“单击 < 确定 > 按钮”。
[ ] 带方括号“[ ]”表示窗口名、菜单名和数据表，如“弹出[新建用户]窗口”。
多级菜单用“/”隔开。如[文件/新建/文件夹]多级菜单表示[文件]菜单下的[新建]子菜单下/的[文件夹]菜单项。

#### 3. 各类标志

本书还采用各种醒目标志来表示在操作过程中应该特别注意的地方，这些标志的意义如下：
该标志后的注释需给予格外关注，不当的操作可能会对人身造成伤害。
提醒操作中应注意的事项，不当的操作可能会导致数据丢失或者设备损坏。
为确保设备配置成功或者正常工作而需要特别关注的操作或信息。
对操作内容的描述进行必要的补充和说明。
配置、操作、或使用设备的技巧、小窍门。

#### 4. 图标约定

本书使用的图标及其含义如下：
该图标及其相关描述文字代表一般网络设备，如路由器、交换机、防火墙等。
该图标及其相关描述文字代表一般意义下的路由器，以及其他运行了路由协议的设备。
该图标及其相关描述文字代表二、三层以太网交换机，以及运行了二层协议的设备。
该图标及其相关描述文字代表无线控制器、无线控制器业务板和有线无线一体化交换机的无线控制引擎设备。
该图标及其相关描述文字代表无线接入点设备。
TT该图标及其相关描述文字代表无线终结单元。
TT该图标及其相关描述文字代表无线终结者。
该图标及其相关描述文字代表无线Mesh设备。
该图标代表发散的无线射频信号。
该图标代表点到点的无线射频信号。
该图标及其相关描述文字代表防火墙、UTM、多业务安全网关、负载均衡等安全设备。
该图标及其相关描述文字代表防火墙插卡、负载均衡插卡、NetStream插卡、SSL VPN插卡、IPS插卡、ACG插卡等安全插卡。

#### 5. 示例约定

由于设备型号不同、配置不同、版本升级等原因，可能造成本手册中的内容与用户使用的设备显示信息不一致。实际使用中请以设备显示的内容为准。
本手册中出现的端口编号仅作示例，并不代表设备上实际具有此编号的端口，实际使用中请以设备上存在的端口编号为准。

### 资料意见反馈

如果您在使用过程中发现产品资料的任何问题，可以通过以下方式反馈：
E-mail：info@h3c.com感谢您的反馈，让我们做得更好！

## 01-IP路由基础命令

目 录路由基础配置命令

### 1 IP路由基础

1 IP路由基础

#### 1.1 IP路由基础配置命令

##### 1.1.1 address-family ipv4

命令用来创建 地址族，并进入 地址族视图。
address-family ipv4 RIB IPv4 RIB IPv4命令用来删除 地址族和 地址族视图下的所有undo address-family ipv4 RIB IPv4 RIB IPv4配置。
【命令】
address-family ipv4 undo address-family ipv4【缺省情况】
不存在 RIB IPv4 地址族。
【视图】
视图RIB【缺省用户角色】
network-admin【举例】
\# 创建 RIB IPv4 地址族，并进入 RIB IPv4 地址族视图。
<Sysname> system-view [Sysname] rib [Sysname-rib] address-family ipv4 [Sysname-rib-ipv4]

##### 1.1.2 address-family ipv6

命令用来创建 地址族，并进入 地址族视图。
address-family ipv6 RIB IPv6 RIB IPv6命令用来删除 地址族和 地址族视图下的所有配置。
undo address-family RIB IPv6 RIB IPv6【命令】
address-family ipv6 undo address-family ipv6【缺省情况】
不存在 RIB IPv6 地址族。
【视图】
RIB 视图【缺省用户角色】
network-admin

【举例】
\# 创建 RIB IPv6 地址族，并进入 RIB IPv6 地址族视图。
<Sysname> system-view [Sysname] rib [Sysname-rib] address-family ipv6 [Sysname-rib-ipv6]

##### 1.1.3 display ip routing-table

命令用来显示路由表的信息。
display ip routing-table【命令】
display ip routing-table [ all-vpn-instance | vpn-instance vpn-instance-name ] [ verbose ] display ip routing-table [ all-routes ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
all-vpn-instance：显示所有 实例的路由表信息。
VPN vpn-instance-name：显示指定 的信息。vpn-instance-name 表示vpn-instance VPN MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。
all-routes：显示公网和所有 VPN 实例的路由表信息。
verbose：显示全部路由表的详细信息，包括激活路由和未激活路由。如果未指定本参数，将显示激活路由的概要信息。
【使用指导】
如果不指定任何参数时，则显示公网的信息。
【举例】
显示路由表中当前激活路由的概要信息。
\# <Sysname> display ip routing-table Destinations : 12 Routes : 12 Destination/Mask Proto Pre Cost NextHop Interface
0.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
127.0.0.0/8 Direct 0 0 127.0.0.1 InLoop0
127.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
127.0.0.1/32 Direct 0 0 127.0.0.1 InLoop0
127.255.255.255/32 Direct 0 0 127.0.0.1 InLoop0
192.168.1.0/24 Direct 0 0 192.168.1.40 Vlan11

192.168.1.0/32 Direct 0 0 192.168.1.40 Vlan11
192.168.1.40/32 Direct 0 0 127.0.0.1 InLoop0
192.168.1.255/32 Direct 0 0 192.168.1.40 Vlan11
224.0.0.0/4 Direct 0 0 0.0.0.0 NULL0
224.0.0.0/24 Direct 0 0 0.0.0.0 NULL0
255.255.255.255/32 Direct 0 0 127.0.0.1 InLoop0
\# 显示公网和所有 VPN 实例中当前激活路由的概要信息。
<Sysname> display ip routing-table all-routes
VPN instance: public instance
Destinations : 10 Routes : 10
Destination/Mask Proto Pre Cost NextHop Interface
0.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
1.1.1.0/24 Static 60 0 192.168.47.4 Vlan11
127.0.0.0/8 Direct 0 0 127.0.0.1 InLoop0
127.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
127.0.0.1/32 Direct 0 0 127.0.0.1 InLoop0
127.255.255.255/32 Direct 0 0 127.0.0.1 InLoop0
192.168.1.40/32 Direct 0 0 127.0.0.1 InLoop0
224.0.0.0/4 Direct 0 0 0.0.0.0 NULL0
224.0.0.0/24 Direct 0 0 0.0.0.0 NULL0
255.255.255.255/32 Direct 0 0 127.0.0.1 InLoop0
VPN instance: vpn1
Destinations : 10 Routes : 10
Destination/Mask Proto Pre Cost NextHop Interface
0.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
1.1.2.0/24 Static 60 0 2.2.1.1 Vlan11
3.3.1.0/24 BGP 255 0 55.1.1.2 Vlan12
127.0.0.0/8 Direct 0 0 127.0.0.1 InLoop0
127.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
127.0.0.1/32 Direct 0 0 127.0.0.1 InLoop0
127.255.255.255/32 Direct 0 0 127.0.0.1 InLoop0
224.0.0.0/4 Direct 0 0 0.0.0.0 NULL0
224.0.0.0/24 Direct 0 0 0.0.0.0 NULL0
255.255.255.255/32 Direct 0 0 127.0.0.1 InLoop0
\# 显示所有 VPN 实例下的 IPv4 路由信息。
<Sysname> display ip routing-table all-vpn-instance
VPN instance: vpn1
Destinations : 10 Routes : 10
Destination/Mask Proto Pre Cost NextHop Interface
0.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
1.1.2.0/24 Static 60 0 2.2.1.1 Vlan11
3.3.1.0/24 BGP 255 0 55.1.1.2 Vlan12

127.0.0.0/8 Direct 0 0 127.0.0.1 InLoop0
127.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
127.0.0.1/32 Direct 0 0 127.0.0.1 InLoop0
127.255.255.255/32 Direct 0 0 127.0.0.1 InLoop0
224.0.0.0/4 Direct 0 0 0.0.0.0 NULL0
224.0.0.0/24 Direct 0 0 0.0.0.0 NULL0
255.255.255.255/32 Direct 0 0 127.0.0.1 InLoop0
VPN instance: vpn2
Destinations : 9 Routes : 9
Destination/Mask Proto Pre Cost NextHop Interface
0.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
1.1.3.0/24 Static 60 0 3.3.1.1 Vlan13
127.0.0.0/8 Direct 0 0 127.0.0.1 InLoop0
127.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
127.0.0.1/32 Direct 0 0 127.0.0.1 InLoop0
127.255.255.255/32 Direct 0 0 127.0.0.1 InLoop0
224.0.0.0/4 Direct 0 0 0.0.0.0 NULL0
224.0.0.0/24 Direct 0 0 0.0.0.0 NULL0
255.255.255.255/32 Direct 0 0 127.0.0.1 InLoop0
表1-1 display ip routing-table 命令显示信息描述表
字段 描述
路由表所属的公网或VPN实例信息，公网路由显示为public instance，私网路由
VPN instance
显示为VPN实例名称
Destinations 目的地址个数
Routes 路由条数
目的地址/掩码长度
Destination/Mask
Proto 发现该路由的路由协议类型
Pre 路由的优先级
路由的度量值
Cost
NextHop 此路由的下一跳地址
Interface 出接口，即到该目的网段的数据包将从此接口发出
Summary count 路由数目
\# 显示路由表的全部详细信息。
<Sysname> display ip routing-table verbose
Destinations : 2 Routes : 2
Destination: 0.0.0.0/32
Protocol: Direct

Process ID: 0 SubProtID: 0x0 Age: 08h34m37s Cost: 0 Preference: 0 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active NoAdv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0x2 OrigAs: 0 NibID: 0x10000000 LastAs: 0 AttrID: 0xffffffff Neighbor: 0.0.0.0 Flags: 0x1000c OrigNextHop: 127.0.0.1 Label: NULL RealNextHop: 127.0.0.1 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: InLoopBack0 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0 Destination: 1.1.1.0/24 Protocol: Static Process ID: 0 SubProtID: 0x0 Age: 04h20m37s Cost: 0 Preference: 60 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0x2 OrigAs: 0 NibID: 0x10000003 LastAs: 0 AttrID: 0xffffffff Neighbor: 0.0.0.0 Flags: 0x1008c OrigNextHop: 192.168.47.4 Label: NULL RealNextHop: 192.168.47.4 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: Vlan-interface11 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0 \# 显示所有 VPN 实例内所有路由的详细信息。
<Sysname> display ip routing-table all-vpn-instance verbose VPN instance: vpn1 Destinations : 1 Routes : 1 Destination: 0.0.0.0/32 Protocol: Direct Process ID: 0 SubProtID: 0x0 Age: 08h34m37s Cost: 0 Preference: 0 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active NoAdv

OrigTblID: 0x0 OrigVrf: vpn1 TableID: 0x2 OrigAs: 0 NibID: 0x10000000 LastAs: 0 AttrID: 0xffffffff Neighbor: 0.0.0.0 Flags: 0x1000c OrigNextHop: 127.0.0.1 Label: NULL RealNextHop: 127.0.0.1 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: InLoopBack0 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0 VPN instance: vpn2 Destinations : 1 Routes : 1 Destination: 1.1.1.0/24 Protocol: Static Process ID: 0 SubProtID: 0x0 Age: 04h20m37s Cost: 0 Preference: 60 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: vpn2 TableID: 0x2 OrigAs: 0 NibID: 0x10000003 LastAs: 0 AttrID: 0xffffffff Neighbor: 0.0.0.0 Flags: 0x1008c OrigNextHop: 192.168.47.4 Label: NULL RealNextHop: 192.168.47.4 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: Vlan-interface11 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0表1-2 display ip routing-table verbose 命令显示信息描述表字段 描述路由表所属的公网或VPN实例信息，公网路由显示为public instance，私网路由显示为VPN instance VPN实例名称Destinations 目的地址个数Routes 路由条数目的地址/掩码Destination Protocol 发现该路由的路由协议类型Process ID 进程号路由子协议ID SubProtID Age 此路由在路由表中存在的时间

字段 描述Cost 路由的度量值Preference 路由的优先级IP优先级值IpPre QosLocalID QoS本地ID Tag 路由标记路由状态描述：
• Active：有效的单播路由
• Adv：允许对外发送的路由
• Inactive：非激活路由标志State
• NoAdv：不允许发布的路由
• Vrrp：VRRP 产生的路由
• Nat ： NAT 产生的路由
• TunE：Tunnel 隧道的标志OrigTblID 原始路由表ID OrigVrf 路由所属的原始VPN，显示为default-vrf表示公网TableID 路由所在路由表的ID初始AS号OrigAs NibID 下一跳ID LastAs 最后AS号AttrID 路由属性ID号Neighbor 路由协议的邻居地址Flags 路由标志位OrigNextHop 此路由的下一跳地址标签Label RealNextHop 路由真实下一跳BkLabel 备份标签BkNexthop 备份下一跳地址隧道ID Tunnel ID Interface 出接口，即到该目的网段的数据包将从此接口发出BkTunnel ID 备份隧道ID备份出接口BkInterface FtnIndex FTN表项索引TrafficIndex 流量统计索引值，取值范围为1～64，N/A表示无效值Connector 表示BGP为MD VPN特性所携带的Connector属性，具体取值为BGP对等体在交换

字段 描述VPN-IPv4路由时携带源PE的地址，N/A表示没有该属性路由数目Summary count PathID BGP路由的Add-Path ID

##### 1.1.4 display ip routing-table acl

命令用来显示通过指定 过滤的路由信息。
display ip routing-table acl ACL【命令】
display ip routing-table [ vpn-instance vpn-instance-name ] acl ipv4-acl-number [ verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
vpn-instance vpn-instance-name：显示指定 VPN 的信息。vpn-instance-name 表示MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示公网的信息。
ipv4-acl-number：基本 ACL 的编号，取值范围为 2000～2999。
verbose：显示通过指定 ACL 过滤的所有路由的详细信息。如果未指定本参数，将只显示通过指定 过滤的激活路由的概要信息。
ACL【使用指导】
如果用户指定的 ACL 不存在或者 ACL 中没有任何规则，将显示所有的路由信息。
【举例】
\# 配置 ACL 2000，并设置路由过滤规则。
<Sysname> system-view [Sysname] acl basic 2000 [Sysname-acl-ipv4-basic-2000] rule permit source 192.168.1.0 0.0.0.255 [Sysname-acl-ipv4-basic-2000] rule deny source any显示通过 过滤的激活路由的概要信息。
\# ACL 2000 [Sysname-acl-ipv4-basic-2000] display ip routing-table acl 2000 Summary count : 4 Destination/Mask Proto Pre Cost NextHop Interface
192.168.1.0/24 Direct 0 0 192.168.1.111 Vlan11
192.168.1.0/32 Direct 0 0 192.168.1.111 Vlan11

192.168.1.111/32 Direct 0 0 127.0.0.1 InLoop0
192.168.1.255/32 Direct 0 0 192.168.1.111 Vlan11
以上显示信息解释请参见 表 1-1。
显示通过 过滤的所有路由的详细信息。
\# ACL 2000
<Sysname> display ip routing-table acl 2000 verbose
Summary count : 4
Destination: 192.168.1.0/24
Protocol: Direct
Process ID: 0
SubProtID: 0x1 Age: 04h20m37s
Cost: 0 Preference: 0
IpPre: N/A QosLocalID: N/A
Tag: 0 State: Active Adv
OrigTblID: 0x0 OrigVrf: default-vrf
TableID: 0x2 OrigAs: 0
NibID: 0x10000003 LastAs: 0
AttrID: 0xffffffff Neighbor: 0.0.0.0
Flags: 0x10080 OrigNextHop: 192.168.1.111
Label: NULL RealNextHop: 192.168.1.111
BkLabel: NULL BkNextHop: N/A
Tunnel ID: Invalid Interface: Vlan-interface11
BkTunnel ID: Invalid BkInterface: N/A
FtnIndex: 0x0 TrafficIndex: N/A
Connector: N/A PathID: 0x0
Destination: 192.168.1.0/32
Protocol: Direct
Process ID: 0
SubProtID: 0x0 Age: 04h20m37s
Cost: 0 Preference: 0
IpPre: N/A QosLocalID: N/A
Tag: 0 State: Active NoAdv
OrigTblID: 0x0 OrigVrf: default-vrf
TableID: 0x2 OrigAs: 0
NibID: 0x10000003 LastAs: 0
AttrID: 0xffffffff Neighbor: 0.0.0.0
Flags: 0x1008c OrigNextHop: 192.168.1.111
Label: NULL RealNextHop: 192.168.1.111
BkLabel: NULL BkNextHop: N/A
Tunnel ID: Invalid Interface: Vlan-interface11
BkTunnel ID: Invalid BkInterface: N/A
FtnIndex: 0x0 TrafficIndex: N/A
Connector: N/A PathID: 0x0
Destination: 192.168.1.111/32
Protocol: Direct

Process ID: 0 SubProtID: 0x1 Age: 04h20m37s Cost: 0 Preference: 0 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active NoAdv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0x2 OrigAs: 0 NibID: 0x10000000 LastAs: 0 AttrID: 0xffffffff Neighbor: 0.0.0.0 Flags: 0x10004 OrigNextHop: 127.0.0.1 Label: NULL RealNextHop: 127.0.0.1 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: InLoopBack0 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0 Destination: 192.168.1.255/32 Protocol: Direct Process ID: 0 SubProtID: 0x0 Age: 04h20m37s Cost: 0 Preference: 0 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active NoAdv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0x2 OrigAs: 0 NibID: 0x10000003 LastAs: 0 AttrID: 0xffffffff Neighbor: 0.0.0.0 Flags: 0x1008c OrigNextHop: 192.168.1.111 Label: NULL RealNextHop: 192.168.1.111 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: Vlan-interface11 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0以上显示信息解释请参见 表 1-2。

##### 1.1.5 display ip routing-table ip-address

display ip routing-table ip-address 命令用来显示指定目的地址的路由信息。
display ip routing-table ip-address1 to ip-address2 命令用来显示指定目的地址范围内的路由信息。
【命令】
display ip routing-table [ vpn-instance vpn-instance-name ] ip-address [ mask-length | mask ] [ longer-match ] [ verbose ] display ip routing-table [ vpn-instance vpn-instance-name ] ip-address1 to ip-address2 [ verbose ]

【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
vpn-instance-name：显示指定 VPN 的信息。vpn-instance-name 表示vpn-instance MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示公网的信息。
ip-address：目的 IP 地址，点分十进制格式。
mask-length：网络掩码长度，取值范围为 0～32。
mask：网络掩码，点分十进制格式。
longer-match：匹配掩码更长的路由。
ip-address1 to ip-address2：IP 地址范围。ip-address1 和 ip-address2 共同决定一个地址范围，只有地址在此范围内的路由才会被显示。
verbose：显示全部路由表的详细信息，包括激活路由和未激活路由。如果未指定本参数，将显示激活路由的概要信息。
【使用指导】
使用不同的可选参数，命令的输出也不相同，以下是对该命令不同形式的输出说明：
• display ip routing-table ip-address显示满足如下条件的所有激活路由：
用户输入的目的 IP 地址同路由表中各条路由的子网掩码值进行与运算；
(cid:123)
路由表中各条路由的目的 IP 地址同其自身子网掩码值进行与运算；
(cid:123)
两次运算结果相同的路由条目将被显示出来。
(cid:123)
• display ip routing-table ip-address mask显示满足如下条件的所有激活路由：
用户输入的目的 IP 地址同用户输入的子网掩码值进行与运算；
(cid:123)
路由表中各条路由的目的 IP 地址同用户输入的子网掩码值进行与运算；
(cid:123)
两次运算结果相同，并且掩码小于等于用户输入的子网掩码的路由条目将被显示出来。
(cid:123)
• display ip routing-table ip-address longer-match显示满足如下条件的所有激活路由：
用户输入的目的 IP 地址同路由表中各条路由的子网掩码值进行与运算；
(cid:123)
路由表中各条路由的目的 IP 地址同其自身子网掩码值进行与运算；
(cid:123)
两次运算结果相同，并且子网掩码最长匹配的路由条目将被显示出来。
(cid:123)
• display ip routing-table ip-address mask longer-match显示满足如下条件的所有激活路由：
用户输入的目的 地址同用户输入的子网掩码值进行与运算；
IP (cid:123)
路由表中各条路由的目的 地址同用户输入的子网掩码值进行与运算；
IP (cid:123)

两次运算结果相同，掩码小于等于用户输入的子网掩码，同时子网掩码最长匹配的路由条(cid:123)
目将被显示出来。
• display ip routing-table ip-address1 to ip-address2显示 到 之间的激活路由，目的地址与掩码（32 位）同ip-address1/32 ip-address2/32时在指定范围内才会显示。
【举例】
\# 显示目的地址为 11.0.0.1 的路由信息。
<Sysname> display ip routing-table 11.0.0.1 Summary count : 3 Destination/Mask Proto Pre Cost NextHop Interface
11.0.0.0/8 Static 60 0 0.0.0.0 NULL0
11.0.0.0/16 Static 60 0 0.0.0.0 NULL0
11.0.0.0/24 Static 60 0 0.0.0.0 NULL0 \# 显示目的地址/掩码为 11.0.0.1/20 的路由信息。
<Sysname> display ip routing-table 11.0.0.1 20 Summary count : 2 Destination/Mask Proto Pre Cost NextHop Interface
11.0.0.0/8 Static 60 0 0.0.0.0 NULL0
11.0.0.0/16 Static 60 0 0.0.0.0 NULL0显示目的地址为 并且掩码最长匹配的路由信息。
\# 11.0.0.1 <Sysname> display ip routing-table 11.0.0.1 longer-match Summary count : 1 Destination/Mask Proto Pre Cost NextHop Interface
11.0.0.0/24 Static 60 0 0.0.0.0 NULL0显示目的地址/掩码为 并且掩码最长匹配的路由信息。
\# 11.0.0.1/20 <Sysname> display ip routing-table 11.0.0.1 20 longer-match Summary count : 1 Destination/Mask Proto Pre Cost NextHop Interface
11.0.0.0/16 Static 60 0 0.0.0.0 NULL0显示目的地址从 到 范围内的路由信息。
\# 1.1.1.0 5.5.5.0 <Sysname> display ip routing-table 1.1.1.0 to 5.5.5.0 Summary count : 4 Destination/Mask Proto Pre Cost NextHop Interface
1.1.1.1/32 Direct 0 0 127.0.0.1 InLoop0

2.2.2.0/24 Direct 0 0 2.2.2.1 Vlan2
3.3.3.1/32 Direct 0 0 127.0.0.1 InLoop0
4.4.4.1/32 Direct 0 0 127.0.0.1 InLoop0
\# 显示目的地址为 1.2.3.4 的路由的详细信息。
<Sysname> display ip routing-table 1.2.3.4 verbose
Summary count : 1
Destination: 1.2.3.4/32
Protocol: O_INTRA
Process ID: 0
SubProtID: 0x1 Age: 00h00m37s
Cost: 0 Preference: 255
IpPre: N/A QosLocalID: N/A
Tag: 0 State: Active Adv
OrigTblID: 0x0 OrigVrf: default-vrf
TableID: 0x2 OrigAs: 200
NibID: 0x15000000 LastAs: 200
AttrID: 0x0 Neighbor: 192.168.47.2
Flags: 0x10060 OrigNextHop: 192.168.47.2
Label: NULL RealNextHop: 192.168.47.2
BkLabel: NULL BkNextHop: N/A
Tunnel ID: Invalid Interface: Vlan-interface11
BkTunnel ID: Invalid BkInterface: N/A
FtnIndex: 0x0 TrafficIndex: N/A
Connector: N/A PathID: 0x0
以上显示信息的解释请参见 表 1-1。

##### 1.1.6 display ip routing-table prefix-list

display ip routing-table prefix-list 命令用来显示通过指定前缀列表过滤的路由信息。
【命令】
display ip routing-table [ vpn-instance vpn-instance-name ] prefix-list prefix-list-name [ verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
vpn-instance vpn-instance-name：显示指定 VPN 的信息。vpn-instance-name 表示MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示公网的信息。
prefix-list-name：前缀列表名称，为 1～63 个字符的字符串，区分大小写。

verbose：当使用该参数时，显示通过过滤规则的所有路由的详细信息。如果未指定本参数，将只显示通过过滤规则的激活路由的概要信息。
【使用指导】
如果指定的前缀列表不存在，将显示所有的路由信息。
【举例】
\# 配置地址前缀列表 test 允许前缀为 1.1.1.0，掩码长度为 24 的路由通过。
<Sysname> system-view [Sysname] ip prefix-list test permit 1.1.1.0 24显示通过前缀列表 过滤的激活路由的概要信息。
\# test [Sysname] display ip routing-table prefix-list test Summary count : 1 Destination/Mask Proto Pre Cost NextHop Interface
1.1.1.0/24 Direct 0 0 1.1.1.2 Vlan11以上显示信息的解释请参见 表 1-1。
\# 显示通过前缀列表 test 过滤的所有路由的详细信息。
[Sysname] display ip routing-table prefix-list test verbose Summary count : 1 Destination: 1.1.1.0/24 Protocol: Direct Process ID: 0 SubProtID: 0x1 Age: 04h20m37s Cost: 0 Preference: 0 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0x2 OrigAs: 0 NibID: 0x10000003 LastAs: 0 AttrID: 0xffffffff Neighbor: 0.0.0.0 Flags: 0x1008c OrigNextHop: 1.1.1.2 Label: NULL RealNextHop: 1.1.1.2 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: Vlan-interface11 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0以上显示信息的解释请参见 表 1-2。

##### 1.1.7 display ip routing-table protocol

display ip routing-table protocol 命令用来显示指定协议生成或发现的路由信息。

【命令】
display ip routing-table [ vpn-instance vpn-instance-name ] protocol protocol [ inactive | verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
vpn-instance vpn-instance-name：显示指定 VPN 的信息。vpn-instance-name 表示MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示公网的信息。
protocol：显示指定路由协议的信息。
inactive：显示未激活路由的信息。如果未指定本参数，则显示激活路由和未激活路由的信息。
verbose：当使用该参数时，显示路由的详细信息。如果未指定本参数，将显示路由的概要信息。
【举例】
显示所有直连路由的概要信息。
\# <Sysname> display ip routing-table protocol direct Summary count : 9 Direct Routing Table Status : <Active> Summary count : 9 Destination/Mask Proto Pre Cost NextHop Interface
0.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
2.2.2.0/24 Direct 0 0 2.2.2.1 Vlan2
2.2.2.0/32 Direct 0 0 2.2.2.1 Vlan2
2.2.2.2/32 Direct 0 0 127.0.0.1 InLoop0
2.2.2.255/32 Direct 0 0 2.2.2.1 Vlan2
127.0.0.0/8 Direct 0 0 127.0.0.1 InLoop0
127.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
127.0.0.1/32 Direct 0 0 127.0.0.1 InLoop0
127.255.255.255/32 Direct 0 0 127.0.0.1 InLoop0 Direct Routing Table Status : <Inactive> Summary count : 0 \# 显示静态路由表。
<Sysname> display ip routing-table protocol static Summary count : 1 Static Routing Table Status : <Active>

Summary count : 0 Static Routing Table Status : <Inactive> Summary count : 1 Destination/Mask Proto Pre Cost NextHop Interface
1.2.3.0/24 Static 60 0 1.2.4.5 Vlan10 \# 显示所有 OSPF 路由的详细信息。
<Sysname> display ip routing-table protocol ospf verbose Summary count : 1 Destination: 1.1.1.2/32 Protocol: O_INTRA Process ID: 0 SubProtID: 0x6 Age: 00h03m54s Cost: 0 Preference: 255 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0x2 OrigAs: 200 NibID: 0x16000000 LastAs: 200 AttrID: 0x0 Neighbor: 192.168.47.2 Flags: 0x10060 OrigNextHop: 192.168.47.2 Label: NULL RealNextHop: 192.168.47.2 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: Vlan-interface11 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0以上显示信息的解释请参见 表 1-1。

##### 1.1.8 display ip routing-table statistics

命令用来显示路由表中的综合路由统计信息。综合display ip routing-table statistics路由统计信息包括路由总数目、路由协议添加/删除路由数目、激活路由数目。
【命令】
display ip routing-table [ all-routes | all-vpn-instance | vpn-instance vpn-instance-name ] statistics【视图】
任意视图【缺省用户角色】
network-admin network-operator

【参数】
all-routes：显示公网和所有 VPN 实例的信息。
all-vpn-instance：显示所有 VPN 实例的信息。
vpn-instance vpn-instance-name：显示指定 VPN 的信息。vpn-instance-name 表示MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。
【使用指导】
如果不指定任何参数时，则显示公网的信息。
【举例】
显示公网路由表中的综合路由统计信息。
\# <Sysname> display ip routing-table statistics Total prefixes: 15 Active prefixes: 15 Proto Routes Active Added Deleted DIRECT 12 12 30 18 STATIC 3 3 5 2 RIP 0 0 0 0 OSPF 0 0 0 0 IS-IS 0 0 0 0 BGP 0 0 0 0 Total 15 15 35 20显示公网和所有 实例路由表中的综合路由统计信息。
\# VPN <Sysname> display ip routing-table all-routes statistics Total prefixes: 11 Active prefixes: 11 Proto Routes Active Added Deleted DIRECT 8 8 8 0 STATIC 3 3 5 2 RIP 0 0 0 0 OSPF 0 0 0 0 IS-IS 0 0 0 0 LISP 0 0 0 0 BGP 0 0 0 0 Total 11 11 13 2 \# 显示指定 VPN 实例路由表中的综合路由统计信息。
<Sysname> display ip routing-table vpn-instance vpn1 statistics Total prefixes: 11 Active prefixes: 11 Proto Routes Active Added Deleted DIRECT 8 8 8 0 STATIC 3 3 5 2 RIP 0 0 0 0 OSPF 0 0 0 0

IS-IS 0 0 0 0 LISP 0 0 0 0 BGP 0 0 0 0 Total 11 11 13 2 \# 显示所有 VPN 实例路由表中的综合路由统计信息。
<Sysname> display ip routing-table all-vpn-instance statistics Total prefixes: 11 Active prefixes: 11 Proto Routes Active Added Deleted DIRECT 8 8 8 0 STATIC 3 3 5 2 RIP 0 0 0 0 OSPF 0 0 0 0 IS-IS 0 0 0 0 LISP 0 0 0 0 BGP 0 0 0 0 Total 11 11 13 2表1-3 display ip routing-table statistics 命令显示信息描述表字段 描述Total prefixes 总的前缀数目Active prefixes 总的激活前缀数目Proto 路由协议Routes 总的路由数目活跃的、正在使用的路由数目Active Added 路由器启动后或在上一次清除路由表后，路由表中添加的路由数目Deleted 标记为删除的路由数目（此类路由在等待一段时间后会被释放）
Total 各种类型路由数目的总和

##### 1.1.9 display ip routing-table summary

命令用来显示路由表的概要信息，包括最大等价路由display ip routing-table summary数、最大可激活路由前缀数、剩余可激活路由前缀数等。
【命令】
display ip routing-table [ vpn-instance vpn-instance-name ] summary【视图】
任意视图【缺省用户角色】
network-admin network-operator

【参数】
vpn-instance vpn-instance-name：显示指定 VPN 的信息。vpn-instance-name 表示MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示公网的信息。
【举例】
\# 显示公网的路由表概要信息。
<Sysname> display ip routing-table summary Max ECMP: 32 Max Active Route: 262144 Remain Active Route: 262126 \# 显示 vpn1 实例的路由表概要信息。
<Sysname> display ip routing-table vpn-instance vpn1 summary Max ECMP: 32 Max Active Route: 262144 Remain Active Route: 262134 Threshold value of active routes alert: 65100表1-4 display ip routing-table summary 命令显示信息描述表字段 描述Max ECMP 最大等价路由数Max Active Route 最多支持激活路由前缀数剩余可激活路由前缀数Remain Active Route显示最多支持激活路由前缀数的告警门限：
• 如果在 VPN 实例中配置了命令 routing-table limit number simply-alert，则显示信息字段为 Threshold value of active routes alert，取值表示产生告警的门限值。当 实例的激活路由前缀数超过该取值时，可以继续激活VPN新的路由前缀，但会产生 告警和日志信息Trap Threshold value of active routes alert • 若在 VPN 实例中配置了命令 routing-table limit number warn-threshold，则显示信息字段为 Threshold value percentage of max active routes，取值表示当（VPN 实例中的激活路由前缀数/最多支持激活路由前缀数×100）达到 warn-threshold 时，产生 Trap 告警和日志信息，但仍然允许增加激活路由前缀。当 实例中的激活路由前缀由数达到最多支持激活路由前缀数VPN目时，不再激活新的路由前缀

##### 1.1.10 display ipv6 rib attribute

display ipv6 rib attribute 命令用来显示 IPv6 RIB 的路由属性信息。
【命令】
display ipv6 rib attribute [ attribute-id ]【视图】
任意视图

【缺省用户角色】
network-admin network-operator【参数】
attribute-id：路由属性 ID 值，取值范围为十六进制数 0～ffffffff。
【举例】
\# 显示 IPv6 RIB 的路由属性信息。
<Sysname> display ipv6 rib attribute Total number of attribute(s): 1 Detailed information of attribute 0x9:
Flag: 0x0 Protocol: BGP4+ instance default Address family: IPv6 Reference count: 0 Local preference: 0 Ext-communities number: 0 Ext-communities value: N/A Communities number: 0 Communities value: N/A AS-path number: 0 AS-path value: N/A以上显示信息的解释请参见 表 1-9。

##### 1.1.11 display ipv6 rib graceful-restart

命令用来显示 IPv6 RIB 的 GR 状态信息。
display ipv6 rib graceful-restart【命令】
display ipv6 rib graceful-restart【视图】
任意视图【缺省用户角色】
network-admin network-operator【举例】
\# 显示 IPv6 RIB 的 GR 状态信息。
<Sysname> display ipv6 rib graceful-restart RIB GR state : Phase2-calculation end RCOM GR state : Flush end Protocol GR state:
No. Protocol Lifetime FD State Start/End
--------------------------------------------------

1 DIRECT6 480 29 End No/No 2 STATIC6 480 32 End No/No 3 ISISV6 480 30 End No/No以上显示信息的解释请参见 表 1-10。

##### 1.1.12 display ipv6 rib nib

命令用来显示 IPv6 RIB 的下一跳信息。
display ipv6 rib nib【命令】
display ipv6 rib nib [ self-originated ] [ nib-id ] [ verbose ] display ipv6 rib nib protocol protocol [ verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
self-originated：路由管理自己生成的下一跳。
nib-id：路由下一跳 ID 值，取值范围为十六进制数 1～ffffffff。
verbose：显示详细信息。如果未指定本参数，则显示概要信息。
protocol protocol：显示指定路由协议的下一跳信息。
【举例】
\# 显示 IPv6 RIB 的下一跳信息。
<Sysname> display ipv6 rib nib Total number of nexthop(s): 151 NibID: 0x20000000 Sequence: 0 Type: 0x1 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: ::
IFIndex: 0x111 LocalAddr: ::
TopoNthp: Invalid NibID: 0x20000001 Sequence: 1 Type: 0x1 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: ::1 IFIndex: 0x112 LocalAddr: ::1 TopoNthp: Invalid（省略部分显示信息）
显示 下一跳的详细信息。
\# IPv6 RIB

<Sysname> display ipv6 rib nib verbose Total number of nexthop(s): 151 NibID: 0x20000000 Sequence: 0 Type: 0x1 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: ::
IFIndex: 0x111 LocalAddr: ::
TopoNthp: Invalid RefCnt: 4 FlushRefCnt: 1 Flag: 0x84 Version: 1 1 nexthop(s):
PrefixIndex: 0 OrigNexthop: ::
RelyDepth: 0 RealNexthop: ::
Interface: NULL0 LocalAddr: ::
TunnelCnt: 0 Vrf: default-vrf TunnelID: N/A Topology:
Weight: 0 NibID: 0x20000001 Sequence: 1 Type: 0x1 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: ::1 IFIndex: 0x112 LocalAddr: ::1 TopoNthp: Invalid RefCnt: 4 FlushRefCnt: 1 Flag: 0x84 Version: 1 1 nexthop(s):
PrefixIndex: 0 OrigNexthop: ::1 RelyDepth: 0 RealNexthop: ::1 Interface: InLoop0 LocalAddr: ::1 TunnelCnt: 0 Vrf: default-vrf TunnelID: N/A Topology:
Weight: 0 NibID: 0x26000001 Sequence: 1 Type: 0x1 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: 121::2 IFIndex: 0x112 LocalAddr: ::
TopoNthp: Invalid Instance: default NibID: 0x26000002 Sequence: 1 Type: 0x1 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: 122::2 IFIndex: 0x112 LocalAddr: ::

TopoNthp: Invalid Instance: abc（省略部分显示信息）
以上显示信息的解释请参见 表 1-11 和 表 1-12。

##### 1.1.13 display ipv6 route-direct nib

命令用来显示 IPv6 直连路由下一跳信息。
display ipv6 route-direct nib【命令】
display ipv6 route-direct nib [ nib-id ] [ verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
nib-id：路由邻居 ID 值，取值范围为十六进制数 1～ffffffff。
verbose：显示详细信息。如果未指定本参数，则显示概要信息。
【举例】
\# 显示 IPv6 直连路由下一跳信息。
<Sysname> display ipv6 route-direct nib Total number of nexthop(s): 115 NibID: 0x20000000 Sequence: 0 Type: 0x1 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: ::
IFIndex: 0x111 LocalAddr: ::
TopoNthp: Invalid NibID: 0x20000001 Sequence: 1 Type: 0x1 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: ::1 IFIndex: 0x112 LocalAddr: ::1 TopoNthp: Invalid \# 显示 IPv6 直连路由下一跳详细信息。
<Sysname> display ipv6 route-direct nib verbose Total number of nexthop(s): 115

NibID: 0x20000000 Sequence: 0 Type: 0x1 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: ::
IFIndex: 0x111 LocalAddr: ::
RefCnt: 1 FlushRefCnt: 0 Flag: 0x2 Version: 1 1 nexthop(s):
PrefixIndex: 0 OrigNexthop: ::
RelyDepth: 0 RealNexthop: ::
Interface: NULL0 LocalAddr: ::
TunnelCnt: 0 Vrf: default-vrf TunnelID: N/A Topology:
Weight: 0 NibID: 0x20000001 Sequence: 1 Type: 0x1 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: ::1 IFIndex: 0x112 LocalAddr: ::1 RefCnt: 1 FlushRefCnt: 0 Flag: 0x2 Version: 1 1 nexthop(s):
PrefixIndex: 0 OrigNexthop: ::1 RelyDepth: 0 RealNexthop: ::1 Interface: InLoop0 LocalAddr: ::1 TunnelCnt: 0 Vrf: default-vrf TunnelID: N/A Topology:
Weight: 0以上显示信息的解释请参见 表 1-13 和 表 1-14。

##### 1.1.14 display ipv6 routing-table

display ipv6 routing-table 命令用来显示 IPv6 路由表的信息。
【命令】
display ipv6 routing-table [ all-vpn-instance | vpn-instance vpn-instance-name ] [ verbose ] display ipv6 routing-table [ all-routes ]【视图】
任意视图【缺省用户角色】
network-admin network-operator

【参数】
all-vpn-instance：显示所有 VPN 实例的路由信息。
vpn-instance vpn-instance-name：显示指定 VPN 的信息。vpn-instance-name 表示MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。
all-routes：显示公网和所有 VPN 实例的路由表信息。
verbose：显示 IPv6 路由表的详细信息，包括激活路由和未激活路由。如果未指定本参数，将显示激活路由的概要信息。
【使用指导】
如果不指定任何参数时，则显示公网的信息。
【举例】
\# 显示当前路由表的概要信息。
<Sysname> display ipv6 routing-table Destinations : 2 Routes : 2 Destination: ::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: FE80::/10 Protocol : Direct NextHop : :: Preference: 0 Interface : InLoop0 Cost : 0 \# 显示公网和所有 VPN 实例中当前激活路由的概要信息。
<Sysname> display ipv6 routing-table all-routes VPN instance: public instance Destinations : 2 Routes : 2 Destination: ::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: FE80::/10 Protocol : Direct NextHop : :: Preference: 0 Interface : InLoop0 Cost : 0 VPN instance: vpn1 Destinations : 2 Routes : 2 Destination: ::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: 1:2::3:4/128 Protocol : Static NextHop : :: Preference: 60

Interface : NULL0 Cost : 0 \# 显示所有 VPN 实例下的 IPv6 路由信息。
<Sysname> display ipv6 routing-table all-vpn-instance VPN instance: vpn1 Destinations : 2 Routes : 2 Destination: ::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: 1:2::3:4/128 Protocol : Static NextHop : :: Preference: 60 Interface : NULL0 Cost : 0 VPN instance: vpn2 Destinations : 1 Routes : 1 Destination: ::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0表1-5 display ipv6 routing-table 命令显示信息描述表字段 描述路由表所属的公网或VPN实例信息，公网路由显示为public instance，私网路由VPN instance显示为VPN实例名称Destinations 目的地址个数Routes 路由条数Destination 目的网络/主机的IPv6地址和前缀下一跳地址NextHop Preference 路由优先级Interface 出接口，即到该目的地址的数据包将从此接口发出发现该路由的路由协议类型Protocol Cost 路由的开销值Summary count 路由数目显示路由表的详细路由信息。
\# <Sysname> display ipv6 routing-table verbose Destinations : 2 Routes : 2 Destination: ::1/128 Protocol: Direct

Process ID: 0 SubProtID: 0x0 Age: 19h23m02s Cost: 0 Preference: 0 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active NoAdv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0xa OrigAs: 0 NibID: 0x20000000 LastAs: 0 AttrID: 0xffffffff Neighbor: ::
Flags: 0x10004 OrigNextHop: ::1 Label: NULL RealNextHop: ::1 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: InLoopBack0 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0 Destination: 12::/96 Protocol: Direct Process ID: 0 SubProtID: 0x0 Age: 00h01m47s Cost: 0 Preference: 0 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0xa OrigAs: 0 NibID: 0x20000003 LastAs: 0 AttrID: 0xffffffff Neighbor: ::
Flags: 0x10080 OrigNextHop: ::
Label: NULL RealNextHop: ::
BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: Vlan-interface11 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0 \# 显示所有 VPN 实例内所有路由的详细信息。
<Sysname> display ipv6 routing-table all-vpn-instance verbose VPN instance: vpn1 Destinations : 2 Routes : 2 Destination: ::1/128 Protocol: Direct Process ID: 0 SubProtID: 0x0 Age: 19h23m02s Cost: 0 Preference: 0 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active NoAdv

OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0xa OrigAs: 0 NibID: 0x20000000 LastAs: 0 AttrID: 0xffffffff Neighbor: ::
Flags: 0x10004 OrigNextHop: ::1 Label: NULL RealNextHop: ::1 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: InLoopBack0 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0 Destination: 12::1/128 Protocol: Direct Process ID: 0 SubProtID: 0x0 Age: 00h01m45s Cost: 0 Preference: 0 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active NoAdv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0xa OrigAs: 0 NibID: 0x20000000 LastAs: 0 AttrID: 0xffffffff Neighbor: ::
Flags: 0x10004 OrigNextHop: ::1 Label: NULL RealNextHop: ::1 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: Vlan-interface11 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0表1-6 display ipv6 routing-table verbose 命令显示信息描述表字段 描述路由表所属的公网或VPN实例信息，公网路由显示为public instance，私网路由显示为VPN instance VPN实例名称Destination 目的网络/主机的IPv6地址和前缀Protocol 发现该路由的路由协议类型进程号Process ID SubProtID 路由子协议ID Age 此路由在路由表中存在的时间路由的度量值Cost Preference 路由的优先级IpPre IP优先级值QosLocalID QoS本地ID

字段 描述Tag 路由标记路由状态描述：
• Active：有效的单播路由
• Adv：允许对外发送的路由
• Inactive：非激活路由标志State
• NoAdv：不允许发布的路由
• Vrrp：VRRP 产生的路由
• Nat：NAT 产生的路由
• TunE：Tunnel 隧道的标志OrigTblID 原始路由表ID OrigVrf 路由所属的原始VPN，显示为default-vrf表示公网TableID 路由所在路由表的ID初始AS号OrigAs NibID 下一跳ID LastAs 最后AS号AttrID 路由属性ID号路由协议的邻居地址Neighbor Flags 路由标志位OrigNextHop 此路由的下一跳地址Label 标签RealNextHop 路由真实下一跳BkLabel 备份标签BkNexthop 备份下一跳地址隧道ID Tunnel ID Interface 出接口，即到该目的网段的数据包将从此接口发出BkTunnel ID 备份隧道ID BkInterface 备份出接口FTN表项索引FtnIndex TrafficIndex 流量统计索引值，取值范围为1～64，N/A表示无效值表示BGP为MD VPN特性所携带的Connector属性，具体取值为BGP对等体在交换Connector VPN-IPv4路由时携带源PE的地址，N/A表示没有该属性路由数目Summary count PathID BGP路由的Add-Path ID

##### 1.1.15 display ipv6 routing-table acl

display ipv6 routing-table acl 命令用来显示通过指定 IPv6 ACL 过滤的 IPv6 路由信息。
【命令】
display ipv6 routing-table [ vpn-instance vpn-instance-name ] acl ipv6-acl-number [ verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
vpn-instance-name：显示指定 VPN 的信息。vpn-instance-name 表示vpn-instance的 实例名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则MPLS L3VPN VPN显示公网的信息。
ipv6-acl-number：基本 编号，取值范围为 2000～2999。
IPv6 ACL verbose：显示通过指定 过滤的所有路由的详细信息。如果未指定本参数，只显示通过IPv6 ACL IPv6 ACL 过滤的激活路由的概要信息。
【使用指导】
如果指定的 IPv6 ACL 不存在或者 IPv6 ACL 中没有任何规则，将显示所有的 IPv6 路由信息。
【举例】
\# 显示通过 IPv6 ACL 2000 过滤的激活路由的概要信息。
<Sysname> display ipv6 routing-table acl 2000 Summary count : 6 Destination : ::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: 12::/96 Protocol : Direct NextHop : :: Preference: 0 Interface : Vlan11 Cost : 0 Destination: 12::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: 11::1/128 Protocol : O_INTER NextHop : FE80::A1F:3FFF:FE45:206 Preference: 10 Interface : Vlan11 Cost : 2

Destination: FE80::/10 Protocol : Direct NextHop : :: Preference: 0 Interface : InLoop0 Cost : 0 Destination: FF00::/8 Protocol : Direct NextHop : :: Preference: 0 Interface : NULL0 Cost : 0以上显示信息的解释请参见 表 1-5。
\# 显示通过 IPv6 ACL 2000 过滤的所有路由的详细信息。
<Sysname> display ipv6 routing-table acl 2000 verbose Summary count : 6 Destination: ::1/128 Protocol: Direct Process ID: 0 SubProtID: 0x0 Age: 19h29m12s Cost: 0 Preference: 0 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active NoAdv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0xa OrigAs: 0 NibID: 0x20000000 LastAs: 0 AttrID: 0xffffffff Neighbor: ::
Flags: 0x10004 OrigNextHop: ::1 Label: NULL RealNextHop: ::1 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: InLoopBack0 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0 Destination: 12::/96 Protocol: Direct Process ID: 0 SubProtID: 0x0 Age: 00h07m57s Cost: 0 Preference: 0 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0xa OrigAs: 0 NibID: 0x20000003 LastAs: 0 AttrID: 0xffffffff Neighbor: ::
Flags: 0x10080 OrigNextHop: ::
Label: NULL RealNextHop: ::
BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: Vlan-interface11 BkTunnel ID: Invalid BkInterface: N/A

FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0 Destination: 12::1/128 Protocol: Direct Process ID: 0 SubProtID: 0x0 Age: 00h07m55s Cost: 0 Preference: 0 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active NoAdv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0xa OrigAs: 0 NibID: 0x20000000 LastAs: 0 AttrID: 0xffffffff Neighbor: ::
Flags: 0x10004 OrigNextHop: ::1 Label: NULL RealNextHop: ::1 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: InLoopBack0 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0 Destination: 11::1/128 Protocol: O_INTER Process ID: 1 SubProtID: 0x2 Age: 00h06m43s Cost: 2 Preference: 10 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0xa OrigAs: 0 NibID: 0x23000003 LastAs: 0 AttrID: 0x ffffffff Neighbor: ::
Flags: 0x10041 OrigNextHop: FE80::A1F:3FFF:FE45:206 Label: NULL RealNextHop: FE80::A1F:3FFF:FE45:206 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: Vlan-interface11 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0 Destination: FE80::/10 Protocol: Direct Process ID: 0 SubProtID: 0x0 Age: 19h29m12s Cost: 0 Preference: 0 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active NoAdv

OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0xa OrigAs: 0 NibID: 0x20000002 LastAs: 0 AttrID: 0xffffffff Neighbor: ::
Flags: 0x10084 OrigNextHop: ::
Label: NULL RealNextHop: ::
BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: InLoopBack0 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0 Destination: FF00::/8 Protocol: Direct Process ID: 0 SubProtID: 0x0 Age: 19h29m12s Cost: 0 Preference: 0 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active NoAdv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0xa OrigAs: 0 NibID: 0x20000001 LastAs: 0 AttrID: 0xffffffff Neighbor: ::
Flags: 0x10014 OrigNextHop: ::
Label: NULL RealNextHop: ::
BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: NULL0 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0以上显示信息的解释请参见 表 1-6。

##### 1.1.16 display ipv6 routing-table ipv6-address

命令用来显示指定目的地址的IPv6路由信息。
display ipv6 routing-table ipv6-address命令用来显示指定display ipv6 routing-table ipv6-address1 to ipv6-address2目的地址范围内的 IPv6 路由信息。
【命令】
display ipv6 routing-table [ vpn-instance vpn-instance-name ] ipv6-address [ prefix-length ] [ longer-match ] [ verbose ] display ipv6 routing-table [ vpn-instance vpn-instance-name ] ipv6-address1 to ipv6-address2 [ verbose ]【视图】
任意视图

【缺省用户角色】
network-admin network-operator【参数】
vpn-instance-name：显示指定 VPN 的信息。vpn-instance-name 表示vpn-instance的 实例名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则MPLS L3VPN VPN显示公网的信息。
ipv6-address：IPv6 目的地址。
prefix-length：前缀长度，取值范围为 0～128。
longer-match：匹配并显示前缀最长的路由条目。
ipv6-address2：IPv6 地址范围。ipv6-address1 和ipv6-address1 to ipv6-address2共同决定一个地址范围，只有地址在此范围内的路由才会被显示。
verbose：显示激活和未激活路由的详细信息。如果未指定本参数，将显示激活路由的概要信息。
【使用指导】
使用不同的可选参数，命令的输出也不相同，以下是对该命令不同形式的输出说明：
• display ipv6 routing-table ipv6-address显示满足如下条件的所有激活路由：
用户输入的目的 IPv6 地址同路由表中各条路由的前缀长度值进行与运算；
(cid:123)
路由表中各条路由的目的 IPv6 地址同其自身前缀长度值进行与运算；
(cid:123)
两次运算结果相同的路由条目将被显示出来。
(cid:123)
• display ipv6 routing-table ipv6-address prefix-length显示满足如下条件的所有激活路由：
用户输入的目的 地址同用户输入的前缀长度值进行与运算；
IPv6 (cid:123)
路由表中各条路由的目的 地址同用户输入的前缀长度值进行与运算；
IPv6 (cid:123)
两次运算结果相同，并且路由表中前缀长度小于等于用户输入的前缀长度的路由条目将被(cid:123)
显示出来。
• display ipv6 routing-table ipv6-address longer-match显示满足如下条件的所有激活路由：
用户输入的目的 地址同路由表中各条路由的前缀长度值进行与运算；
IPv6 (cid:123)
路由表中各条路由的目的 地址同其自身前缀长度值进行与运算；
IPv6 (cid:123)
两次运算结果相同，同时前缀长度最长匹配的路由条目将被显示出来。
(cid:123)
• display ipv6 routing-table ipv6-address prefix-length longer-match显示满足如下条件的所有激活路由：
用户输入的目的 IPv6 地址同用户输入的前缀长度值进行与运算；
(cid:123)
路由表中各条路由的目的 IPv6 地址同用户输入的前缀长度值进行与运算；
(cid:123)
两次运算结果相同，路由表中前缀长度小于等于用户输入的前缀长度，同时前缀长度最长(cid:123)
匹配的路由条目将被显示出来。
• display ipv6 routing-table ipv6-address1 to ipv6-address2

显示 ipv6-address1/128 到 ipv6-address2/128 之间的路由，目的 IPv6 地址与前缀长度（128 位）同时在指定范围内才会显示。
【举例】
\# 显示目的 IPv6 地址/前缀为 10::1/127 的 IPv6 路由信息。
<Sysname> display ipv6 routing-table 10::1 127 Summary count: 3 Destination: 10::/64 Protocol : Static NextHop : :: Preference: 60 Interface : NULL0 Cost : 0 Destination: 10::/68 Protocol : Static NextHop : :: Preference: 60 Interface : NULL0 Cost : 0 Destination: 10::/120 Protocol : Static NextHop : :: Preference: 60 Interface : NULL0 Cost : 0 \# 显示目的 IPv6 地址/前缀为 10::1/127 并且掩码最长匹配的 IPv6 路由信息。
<Sysname> display ipv6 routing-table 10::1 127 longer-match Summary count : 1 Destination: 10::/120 Protocol : Static NextHop : :: Preference: 60 Interface : NULL0 Cost : 0显示目的 地址从 100::到 300::范围内的 路由信息。
\# IPv6 IPv6 <Sysname> display ipv6 routing-table 100:: to 300::
Summary count : 3 Destination: 100::/64 Protocol : Static NextHop : :: Preference: 60 Interface : NULL0 Cost : 0 Destination: 200::/64 Protocol : Static NextHop : :: Preference: 60 Interface : NULL0 Cost : 0 Destination: 300::/64 Protocol : Static NextHop : :: Preference: 60 Interface : NULL0 Cost : 0显示目的 地址/前缀为 的 路由的详细信息。
\# IPv6 1:2::3:4/128 IPv6 <Sysname> display ipv6 routing-table 1:2::3:4 128 verbose

Summary count : 1 Destination: 1:2::3:4/128 Protocol: O_INTRA Process ID: 1 SubProtID: 0x1 Age: 00h01m14s Cost: 1 Preference: 10 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0xa OrigAs: 0 NibID: 0x23000002 LastAs: 0 AttrID: 0xffffffff Neighbor: ::
Flags: 0x10041 OrigNextHop: FE80::A1F:3FFF:FE45:206 Label: NULL RealNextHop: FE80::A1F:3FFF:FE45:206 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: Vlan-interface11 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0以上显示信息的解释请参见 表 1-5。

##### 1.1.17 display ipv6 routing-table prefix-list

命令用来显示通过指定前缀列表过滤的display ipv6 routing-table prefix-list IPv6路由信息。
【命令】
display ipv6 routing-table [ vpn-instance vpn-instance-name ] prefix-list prefix-list-name [ verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
vpn-instance vpn-instance-name：显示指定 VPN 的信息。vpn-instance-name 表示MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示公网的信息。
prefix-list-name：IPv6 前缀列表的名称，为 1～63 个字符的字符串，区分大小写。
verbose：显示所有路由的详细信息。如果未指定本参数，只显示激活路由的概要信息。
【使用指导】
如果指定的前缀列表不存在，将显示所有的路由信息。

【举例】
\# 配置地址前缀列表 test 允许前缀为::1，前缀长度为 128 的 IPv6 路由通过。
<Sysname> system-view [Sysname] ipv6 prefix-list test permit ::1 128 \# 显示通过前缀列表 test 过滤的 IPv6 激活路由的概要信息。
[Sysname] display ipv6 routing-table prefix-list test Summary count : 1 Destination: ::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0以上显示信息的解释请参见 表 1-5。
\# 显示通过前缀列表 test 过滤的所有 IPv6 路由的详细信息。
[Sysname] display ipv6 routing-table prefix-list test verbose Summary count : 1 Destination: ::1/128 Protocol: Direct Process ID: 0 SubProtID: 0x0 Age: 08h57m19s Cost: 0 Preference: 0 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active NoAdv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0xa OrigAs: 0 NibID: 0x20000000 LastAs: 0 AttrID: 0xffffffff Neighbor: ::
Flags: 0x10004 OrigNextHop: ::1 Label: NULL RealNextHop: ::1 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: InLoopBack0 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0以上显示信息的解释请参见 表 1-6。

##### 1.1.18 display ipv6 routing-table protocol

命令用来显示指定协议生成或发现的 IPv6 路由信display ipv6 routing-table protocol息。
【命令】
display ipv6 routing-table [ vpn-instance vpn-instance-name ] protocol protocol [ inactive | verbose ]

【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
vpn-instance-name：显示指定 VPN 的信息。vpn-instance-name 表示vpn-instance MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示公网的信息。
protocol：显示指定路由协议的信息。
inactive：如果配置了该参数，此命令只显示未激活路由信息。如果未指定本参数，将显示所有激活和未激活路由信息。
verbose：显示激活和未激活路由的详细信息。如果未指定本参数，将显示路由的概要信息。
【举例】
\# 显示所有 IPv6 直连路由的概要信息。
<Sysname> display ipv6 routing-table protocol direct Summary count : 3 Direct Routing Table Status : <Active> Summary count : 3 Destination: ::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: FE80::/10 Protocol : Direct NextHop : :: Preference: 0 Interface : InLoop0 Cost : 0 Destination: FF00::/8 Protocol : Direct NextHop : :: Preference: 0 Interface : NULL0 Cost : 0 Direct Routing Table Status : <Inactive> Summary count : 0 \# 显示 IPv6 静态路由表。
<Sysname> display ipv6 routing-table protocol static Summary count : 3 Static Routing table Status : <Active> Summary count : 3

Destination: 2::2/128 Protocol : Static NextHop : fe80::2 Preference: 60 Interface : Vlan12 Cost : 0 Destination: 2::2/128 Protocol : Static NextHop : fe80::3 Preference: 60 Interface : Vlan12 Cost : 0 Destination: 3::3/128 Protocol : Static NextHop : 2::2 Preference: 60 Interface : Vlan12 Cost : 0 Static Routing table Status : <Inactive> Summary count : 0 \# 显示所有 OSPFv3 路由的详细信息。
<Sysname> display ipv6 routing-table protocol ospfv3 verbose Summary count : 1 Destination: 22::22/128 Protocol: O_INTER Process ID: 0 SubProtID: 0x6 Age: 00h04m15s Cost: 0 Preference: 255 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0xa OrigAs: 200 NibID: 0x25000001 LastAs: 200 AttrID: 0x3 Neighbor: 121::2 Flags: 0x10060 OrigNextHop: 121::2 Label: NULL RealNextHop: 121::2 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: Vlan-interface11 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0以上显示信息的解释请参见 表 1-5。

##### 1.1.19 display ipv6 routing-table statistics

display ipv6 routing-table statistics 命令用来显示 IPv6 路由表中的综合路由统计信息。综合路由统计信息包括路由总数、路由协议添加 / 删除路由数目、激活路由数目。
【命令】
display ipv6 routing-table [ all-routes | all-vpn-instance | vpn-instance vpn-instance-name ] statistics

【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
all-routes：显示公网和所有 VPN 实例的信息。
all-vpn-instance：显示所有 VPN 实例的信息。
vpn-instance-name：显示指定 VPN 的信息。vpn-instance-name 表示vpn-instance的 实例名称，为 1～31 个字符的字符串，区分大小写。
MPLS L3VPN VPN【使用指导】
如果不指定任何参数时，则显示公网的信息。
【举例】
\# 显示公网路由表中综合路由统计信息。
<Sysname> display ipv6 routing-table statistics Total prefixes: 8 Active prefixes: 8 Proto Routes Active Added Deleted DIRECT 5 5 5 0 STATIC 3 3 3 0 RIPng 0 0 0 0 OSPFv3 0 0 0 0 IS-ISv6 0 0 0 0 BGP4+ 0 0 0 0 Total 8 8 8 0 \# 显示公网和所有 VPN 实例路由表中的综合路由统计信息。
<Sysname> display ipv6 routing-table all-routes statistics Total prefixes: 6 Active prefixes: 6 Proto Routes Active Added Deleted DIRECT 3 3 3 0 STATIC 3 3 5 2 RIPng 0 0 0 0 OSPFv3 0 0 0 0 IS-ISv6 0 0 0 0 LISP 0 0 0 0 BGP4+ 0 0 0 0 Total 6 6 8 2显示指定 实例路由表中的综合路由统计信息。
\# VPN <Sysname> display ipv6 routing-table vpn-instance vpn1 statistics

Total prefixes: 11 Active prefixes: 11 Proto Routes Active Added Deleted DIRECT 8 8 8 0 STATIC 3 3 5 2 RIPng 0 0 0 0 OSPFv3 0 0 0 0 IS-ISv6 0 0 0 0 LISP 0 0 0 0 BGP4+ 0 0 0 0 Total 11 11 13 2 \# 显示所有 VPN 实例路由表中的综合路由统计信息。
<Sysname> display ipv6 routing-table all-vpn-instance statistics Total prefixes: 11 Active prefixes: 11 Proto Routes Active Added Deleted DIRECT 8 8 8 0 STATIC 3 3 5 2 RIPng 0 0 0 0 OSPFv3 0 0 0 0 IS-ISv6 0 0 0 0 LISP 0 0 0 0 BGP4+ 0 0 0 0 Total 11 11 13 2表1-7 display ipv6 routing-table statistics 命令显示信息描述表字段 描述Total prefixes 总的前缀数目Active prefixes 总的激活前缀数目Proto 路由协议总的路由数目Routes Active 激活的、正在使用的路由数目Added 路由器启动后或在上一次清除路由表后，路由表中添加的路由数目Deleted 标记为删除的路由数目（此类路由在等待一段时间后会被释放）
Total 各种类型路由数目的总和

##### 1.1.20 display ipv6 routing-table summary

display ipv6 routing-table summary 命令用来显示 IPv6 路由表的概要信息，包括最大等价路由数、最大可激活路由前缀数、剩余可激活路由前缀数等。
【命令】
display ipv6 routing-table [ vpn-instance vpn-instance-name ] summary

【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
vpn-instance-name：显示指定 VPN 的信息。vpn-instance-name 表示vpn-instance MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示公网的信息。
【举例】
\# 显示公网的路由表概要信息。
<Sysname> display ipv6 routing-table summary Max ECMP: 32 Max Active Route: 262144 Remain Active Route: 262126显示实例 的路由表概要信息。
\# vpn1 <Sysname> display ipv6 routing-table vpn-instance vpn1 summary Max ECMP: 32 Max Active Route: 262144 Remain Active Route: 262134 Threshold value of active routes alert: 65100以上显示信息的解释请参见 表 1-4。

##### 1.1.21 display max-ecmp-num

命令用来显示系统支持 IPv4 最大等价路由的条数。
display max-ecmp-num【命令】
display max-ecmp-num【视图】
任意视图【缺省用户角色】
network-admin network-operator【举例】
\# 显示系统支持 IPv4 最大等价路由的条数。
<Sysname> display max-ecmp-num Max-ECMP-Num in use: 6 Max-ECMP-Num at the next reboot: 10

表1-8 display max-ecmp-num 命令显示信息描述表字段 描述Max-ECMP-Num in use 当前使用的最大等价路由的条数下次启动后的最大等价路由的条数Max-ECMP-Num at the next reboot

##### 1.1.22 display rib attribute

display rib attribute 命令用来显示 RIB 的路由属性信息。
【命令】
display rib attribute [ attribute-id ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
attribute-id：路由属性 ID 值，取值范围为十六进制数 0～ffffffff。
【举例】
\# 显示 RIB 的路由属性信息。
<Sysname> display rib attribute Total number of attribute(s): 10 Detailed information of attribute 0x0:
Flag: 0x0 Protocol: BGP instance default Address family: IPv4 Reference count: 0 Act-RT reference count: 0 Flush flag: 0 Local preference: 0 Ext-communities number: 26 Ext-communities value: <RT: 1:1> <RT: 2:2> <RT: 3:3> <RT: 123.123.123.123:65535 > <RT: 1234567890:65535> <RT: 123.123.123.123:65534> <RT : 4:4> <RT: 5:5> <RT: 6:6> <RT: 7:7> <RT: 8:8> <RT: 9:9> <RT: 10:10> <RT: 10:1> <RT: 10:11> <RT: 10:12> <RT: 10:
13> <RT: 10:14> <RT: 10:15> <RT: 10:16> ...
Communities number: 0 Communities value: N/A AS-path number: 0 AS-path value: N/A SFlow AS-path length: 0

SFlow AS-path value: N/A Detailed information of attribute 0x1:
Flag: 0x0 Protocol: BGP Address family: IPv4 Reference count: 0 Act-RT reference count: 0 Flush flag: 0 Local prefrence: 0 Ext-communities number: 1 Ext-communities value: <RT: 1:2> Communities number: 0 Communities value: N/A AS-path number: 0 AS-path value: N/A表1-9 display rib attribute 命令显示信息描述表字段 描述Total number of attribute(s): attribute的总个数Flag 标志位产生该属性的协议Protocol Address family 地址簇类型Reference count 引用计数Act-RT reference count 被激活路由引用次数Flush flag 下刷FIB标记，0表示属性没有下刷FIB，1表示属性已经下刷FIB Local prefrence 本地优先级Ext-communities number 扩展团体属性个数扩展团体属性值（个数为0显示N/A，最多显示20个，超出部分用…表示）
Ext-communities value Communities number 团体属性个数Communities value 团体属性值（个数为0显示N/A，最多显示20个，超出部分用…表示）
AS-path number AS-path个数（AS-path个数为所有AS号之和）
AS-path值（AS-path值不区分AS-set、AS-sequence、联盟AS-set、联盟AS-path value AS-sequence；个数为0显示N/A，最多显示20个，超出部分用…表示）
SFlow AS-path length sFlow AS-path属性长度SFlow AS-path value sFlow AS-path值（长度为0显示N/A，最多显示80个，超出部分用…表示）

##### 1.1.23 display rib graceful-restart

命令用来显示 RIB 的 GR 状态信息。
display rib graceful-restart

【命令】
display rib graceful-restart【视图】
任意视图【缺省用户角色】
network-admin network-operator【举例】
显示 的 状态信息。
\# RIB GR <Sysname> display rib graceful-restart RIB GR state : Phase2-calculation end RCOM GR state : Flush end Protocol GR state:
No. Protocol Lifetime FD State Start/End
-------------------------------------------------- 1 DIRECT 100 30 End No/No 2 STATIC 480 34 End No/No 3 OSPF 480 36 End No/No 4 ISIS 480 32 End No/No 5 LDP 480 35 End No/No 6 SLSP 480 29 End No/No表1-10 display rib graceful-restart 命令显示信息描述表字段 描述GR状态：
RIB
• Start：协议 GR 开始
• IGP end：所有 IGP 协议 GR 结束
• VPN-triggering end：VPN 路由触发优选结束
• VPN-calculation end：VPN 路由优选结束
• end：所有路由协议 结束Routing protocol GR RIB GR state
• NSR-calculation unfinished：NSR 优选未完成状态
• start：所有路由触发优选开始Triggering
• Triggering end：所有路由触发优选结束
• Phase1-calculation end：第一阶段优选结束
• All end：所有协议 GR 结束
• Phase2-calculation end：第二阶段优选结束GR状态：
RCOM
• Start：协议 GR 开始RCOM GR state
• VPN-calculation end：VPN 路由优选结束
• VPN-notification end：VPN 路由上报结束
• Routing protocol end：所有路由协议 GR 结束

字段 描述
• NSR-calculation unfinished：NSR 优选未完成状态
•Phase1-calculation end：第一阶段优选结束
• Notification end：所有路由上报结束
• Phase2-calculation end：第二阶段优选结束
• Flush start：开始下刷 FIB
• Flush end：下刷 FIB 结束协议GR状态Protocol GR state No. 编号Protocol 协议名称Lifetime 倒换过程中协议的路由信息/标签信息在RIB中的存活时间，单位为秒协议进程与RIB连接的句柄FD协议 GR 状态：
• Init：协议 GR 初始化状态
• Listen：协议 GR 监听状态State
• Idle：协议 GR 空闲状态
• Active：协议 激活状态GR
• Start：协议 GR 开始状态
• End：协议 结束状态GR
• No：表示该消息未发送Start/End
• Yes：表示该消息已发送

##### 1.1.24 display rib nib

命令用来显示 的下一跳信息。
display rib nib RIB【命令】
display rib nib [ self-originated ] [ nib-id ] [ verbose ] display rib nib protocol protocol [ verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
self-originated：路由管理自己生成的下一跳信息。
nib-id：路由下一跳信息的 值，取值范围为十六进制数 1～ffffffff。
ID

verbose：显示详细信息。如果未指定本参数，则显示概要信息。
protocol：显示指定路由协议生成的下一跳信息。
protocol【举例】
显示 的下一跳信息。
\# RIB <Sysname> display rib nib Total number of nexthop(s): 176 NibID: 0x10000000 Sequence: 0 Type: 0x1 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: 0.0.0.0 IFIndex: 0x111 LocalAddr: 0.0.0.0 TopoNthp: 0 NibID: 0x10000001 Sequence: 1 Type: 0x1 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: 127.0.0.1 IFIndex: 0x112 LocalAddr: 127.0.0.1 TopoNthp: 0 NibID: 0x10000002 Sequence: 2 Type: 0x5 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: 127.0.0.1 IFIndex: 0x112 LocalAddr: 127.0.0.1 TopoNthp: 0 NibID: 0x16000000 Sequence: 3 Type: 0x21 Flushed: No UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: 12.1.1.2 IFIndex: 0x0 LocalAddr: 0.0.0.0 TopoNthp: 0 Instance: abc表1-11 display rib nib 命令显示信息描述表字段 描述Total number of Nexthop(s) 总的下一跳个数NibID 下一跳 ID下一跳序列号Sequence Type 下一跳类型

字段 描述Flushed 是否下刷UserKey0 第一个协议保留数据第二个协议保留数据UserKey1 VrfNthp 下一跳所在VPN索引，显示为0表示公网Nexthop 下一跳地址IFIndex 接口索引本地接口地址LocalAddr（暂不支持）下一跳所在拓扑索引，显示为0表示公网拓扑（目前IPv6不支持TopoNthp子拓扑，显示为Invalid）
Instance BGP实例名称子下一跳的ID SubNibID SubSeq 子下一跳的序列号NthpCnt 子下一跳的下一跳计数Samed 子下一跳中相同下一跳计数子下一跳类型：
NthpType IP：下一跳是IP转发类型\# 显示 RIB 下一跳详细信息。
<Sysname> display rib nib verbose Total number of nexthop(s): 176 NibID: 0x10000000 Sequence: 0 Type: 0x1 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: 0.0.0.0 IFIndex: 0x111 LocalAddr: 0.0.0.0 TopoNthp: 0 RefCnt: 6 FlushRefCnt: 2 Flag: 0x84 Version: 1 1 nexthop(s):
PrefixIndex: 0 OrigNexthop: 0.0.0.0 RelyDepth: 0 RealNexthop: 0.0.0.0 Interface: NULL0 LocalAddr: 0.0.0.0 TunnelCnt: 0 Vrf: default-vrf TunnelID: N/A Topology: base Weight: 0 NibID: 0x10000001 Sequence: 1 Type: 0x1 Flushed: Yes UserKey0: 0x0 VrfNthp: 0

UserKey1: 0x0 Nexthop: 127.0.0.1 IFIndex: 0x112 LocalAddr: 127.0.0.1 TopoNthp: 0 RefCnt: 11 FlushRefCnt: 5 Flag: 0x84 Version: 1 1 nexthop(s):
PrefixIndex: 0 OrigNexthop: 127.0.0.1 RelyDepth: 0 RealNexthop: 127.0.0.1 Interface: InLoop0 LocalAddr: 127.0.0.1 TunnelCnt: 0 Vrf: default-vrf TunnelID: N/A Topology: base Weight: 0 NibID: 0x15000003 Sequence: 3 Type: 0x43 Flushed: Yes UserKey0: 0x100010000 VrfNthp: 0 UserKey1: 0x0 Nexthop: 22.22.22.22 IFIndex: 0x0 LocalAddr: 0.0.0.0 TopoNthp: 0 Instance: default RefCnt: 9 FlushRefCnt: 3 Flag: 0x84 Version: 1 Policy: tnl-policy1 1 nexthop(s):
PrefixIndex: 0 OrigNexthop: 22.22.22.22 RelyDepth: 1 RealNexthop: 13.1.1.2 Interface: Vlan11 LocalAddr: 13.1.1.1 TunnelCnt: 1 Vrf: default-vrf TunnelID: 1025 Topology: base Weight: 0表1-12 命令显示信息描述表display rib nib verbose字段 描述Policy 隧道策略名x nexthop (s) 下一跳具体值（前面数值表示下一跳个数）
等价时下一跳序号PrefixIndex Vrf VPN实例名，显示为default-vrf表示公网OrigNexthop 原始下一跳真实下一跳RealNexthop Interface 出接口LocalAddr 本地接口地址RelyDepth 迭代深度

字段 描述TunnelCnt 迭代到隧道的个数TunnelID 迭代到隧道的ID（暂不支持）拓扑名称，显示为base表示公网拓扑（目前IPv6不支持子拓扑，显示Topology为空）
Weight 等价路由各路由的权重，取值为0表示不是等价路由Instance BGP实例名称下一跳信息的引用计数RefCnt FlushRefCnt 下一跳信息的下刷引用计数Flag 下一跳信息的标志位Version 下一跳信息的版本号

##### 1.1.25 display route-direct nib

命令用来显示直连路由下一跳信息。
display route-direct nib【命令】
display route-direct nib [ nib-id ] [ verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
nib-id：路由邻居 ID 值，取值范围为十六进制数 1～ffffffff。
verbose：显示详细信息。如果未指定本参数，则显示概要信息。
【举例】
\# 显示直连路由下一跳信息。
<Sysname> display route-direct nib Total number of nexthop(s): 116 NibID: 0x10000000 Sequence: 0 Type: 0x1 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: 0.0.0.0 IFIndex: 0x111 LocalAddr: 0.0.0.0 TopoNthp: 0 NibID: 0x10000001 Sequence: 1

Type: 0x1 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: 127.0.0.1 IFIndex: 0x112 LocalAddr: 127.0.0.1 TopoNthp: 0（省略部分显示信息）
表1-13 display route-direct nib 命令显示信息描述表字段 描述Total number of nexthop(s) 总的下一跳个数NibID NIB ID号NIB序列号Sequence Type NIB类型Flushed 是否下刷 FIB UserKey0 NIB协议保留数据1 UserKey1 NIB协议保留数据2 VrfNthp 下一跳所在VPN索引，显示为0表示公网Nexthop 下一跳信息接口索引IFIndex LocalAddr 本地接口地址下一跳所在拓扑索引，显示为0表示公网拓扑（目前IPv6不支持子拓扑，显示为TopoNthp Invalid）
\# 显示直连路由下一跳详细信息。
<Sysname> display route-direct nib verbose Total number of nexthop(s): 116 NibID: 0x10000000 Sequence: 0 Type: 0x1 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: 0.0.0.0 IFIndex: 0x111 LocalAddr: 0.0.0.0 RefCnt: 2 FlushRefCnt: 0 Flag: 0x2 Version: 1 1 nexthop(s):
PrefixIndex: 0 OrigNexthop: 0.0.0.0 RelyDepth: 0 RealNexthop: 0.0.0.0 Interface: NULL0 LocalAddr: 0.0.0.0 TunnelCnt: 0 Vrf: default-vrf TunnelID: N/A Topology: base Weight: 0

NibID: 0x10000001 Sequence: 1 Type: 0x1 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: 127.0.0.1 IFIndex: 0x112 LocalAddr: 127.0.0.1 RefCnt: 5 FlushRefCnt: 0 Flag: 0x2 Version: 1 1 nexthop(s):
PrefixIndex: 0 OrigNexthop: 127.0.0.1 RelyDepth: 0 RealNexthop: 127.0.0.1 Interface: InLoop0 LocalAddr: 127.0.0.1 TunnelCnt: 0 Vrf: default-vrf TunnelID: N/A Topology: base Weight: 0（省略部分显示信息）
表1-14 display route-direct nib verbose 命令显示信息描述表字段 描述x nexthop (s) 下一跳具体值（前面数值表示下一跳个数）
PrefixIndex 等价时下一跳序号VPN实例名，显示为default-vrf表示公网Vrf OrigNexthop 原始下一跳RealNexthop 真实下一跳Interface 出接口localAddr 本地接口地址RelyDepth 迭代深度TunnelCnt 迭代到隧道的个数迭代到隧道的ID TunnelID（暂不支持）拓扑名称，显示为base表示公网拓扑（目前IPv6不支持子拓扑，显示Topology为空）
Weight 等价路由各路由的权重，取值为0表示不是等价路由下一跳信息的引用计数RefCnt FlushRefCnt 下一跳信息的下刷引用计数Flag 下一跳信息的标志位Version 下一跳信息的版本号

##### 1.1.26 fib lifetime

fib lifetime 命令用来配置 IPv4/IPv6 路由在 FIB 中的最大存活时间。

命令用来恢复缺省情况。
undo fib lifetime【命令】
fib lifetime seconds undo fib lifetime【缺省情况】
IPv4/IPv6 路由在 FIB 中的最大存活时间为 600 秒。
【视图】
RIB IPv4 地址族视图RIB IPv6 地址族视图【缺省用户角色】
network-admin【参数】
seconds：路由在 中的最大存活时间，取值范围为 0～6000，单位为秒。取值为 时表示，协FIB 0议或 RIB 进程倒换并重新恢复后，会立即通知 FIB 老化表项。
【使用指导】
配置本命令后，协议在未配置 GR 或 NSR 的情况下，协议或 RIB 倒换重新恢复后，会延迟配置的seconds，再通知 FIB 老化表项。
【举例】
配置 路由在 中的最大存活时间为 秒。
\# IPv4 FIB 60 <Sysname> system-view [Sysname] rib [Sysname-rib] address-family ipv4 [Sysname-rib-ipv4] fib lifetime 60

##### 1.1.27 flush route-attribute

flush route-attribute 命令用来配置 RIB 向 FIB 下发路由时会携带属性消息。
undo flush route-attribute 命令用来取消该配置。
【命令】
flush route-attribute protocol undo flush route-attribute protocol【缺省情况】
RIB 向 FIB 下发路由时不携带属性消息。
【视图】
地址族视图RIB IPv4【缺省用户角色】
network-admin

【参数】
protocol：路由协议，目前只支持 BGP。
【举例】
\# 配置 RIB 向 FIB 下发 BGP 路由时会携带属性消息。
<Sysname> system-view [Sysname] rib [Sysname-rib] address-family ipv4 [Sysname-rib-ipv4] flush route-attribute bgp

##### 1.1.28 inter-protocol fast-reroute

inter-protocol fast-reroute 命令用来开启 RIB IPv4/IPv6 地址族的不同协议间快速重路由功能。
undo inter-protocol fast-reroute 命令用来关闭 RIB IPv4/IPv6 地址族的不同协议间快速重路由功能。
【命令】
inter-protocol fast-reroute [ vpn-instance vpn-instance-name ] undo inter-protocol fast-reroute [ vpn-instance vpn-instance-name ]【缺省情况】
不同协议间快速重路由功能处于关闭状态。
【视图】
RIB IPv4 地址族视图RIB IPv6 地址族视图【缺省用户角色】
network-admin【参数】
vpn-instance-name：开启指定 VPN 实例的不同协议间快速重路由功能。
vpn-instance表示 的 实例名称，为 1～31 个字符的字符串，区分大vpn-instance-name MPLS L3VPN VPN小写。如果未指定本参数，则开启 RIB IPv4/IPv6 地址族中公网的不同协议间快速重路由功能。
【使用指导】
通过配置不同协议间快速重路由功能，可将不同协议的下一跳作为备份下一跳。当路由器检测到网络故障时，将使用备份下一跳替换失效下一跳，通过备份下一跳来指导报文的转发，从而大大缩短了流量中断的时间。
如果 RIB 表中去往同一目的地的不同路由的下一跳和出接口均相同，使用该命令不会生成备份下一跳。
使用不同协议间的快速重路由功能生成备份下一跳时可能会造成环路。
【举例】
\# 开启 RIB IPv4 地址族中公网的不同协议间快速重路由功能。
<Sysname> system-view

[Sysname] rib [Sysname-rib] address-family ipv4 [Sysname-rib-ipv4] inter-protocol fast-reroute

##### 1.1.29 ip route fast-switchover enable

命令用来开启 IPv4 路由快速切换功能。
ip route fast-switchover enable命令用来关闭 IPv4 路由快速切换功能。
undo ip route fast-switchover enable【命令】
ip route fast-switchover enable undo ip route fast-switchover enable【缺省情况】
IPv4 路由快速切换功能处于关闭状态。
【视图】
系统视图【缺省用户角色】
network-admin【使用指导】
在未开启本功能的情况下，当某个物理接口为大量路由（包括等价路由和主备路由的主路由）连接下一跳的出接口时，如果该接口所在的链路故障时，设备需要先删除失效链路对应的所有 表ARP项，然后通知 FIB 删除失效的 FIB 表项，处理时间过长，流量无法快速切换到可用路径。通过开启本功能，当接口所在的链路故障时，设备直接通知 FIB 删除失效的 FIB 表项，以加快路由的切换、缩短流量中断的时间。
【举例】
\# 开启 IPv4 路由快速切换功能。
<Sysname> system-view [Sysname] ip route fast-switchover enable

##### 1.1.30 ipv6 route fast-switchover enable

ipv6 route fast-switchover enable 命令用来开启 IPv6 路由快速切换功能。
undo ipv6 route fast-switchover enable 命令用来关闭 IPv6 路由快速切换功能。
【命令】
ipv6 route fast-switchover enable undo ipv6 route fast-switchover enable【缺省情况】
IPv6 路由快速切换功能处于关闭状态。
【视图】
系统视图

【缺省用户角色】
network-admin【使用指导】
在未开启本功能的情况下，当某个物理接口为大量路由（包括等价路由和主备路由的主路由）连接下一跳的出接口时，如果该接口所在的链路故障时，设备需要先删除失效链路对应的所有 表项，ND然后通知 FIB 删除失效的 FIB 表项，处理时间过长，流量无法快速切换到可用路径。通过开启本功能，当接口所在的链路故障时，设备直接通知 FIB 删除失效的 FIB 表项，以加快路由的切换、缩短流量中断的时间。
【举例】
开启 路由快速切换功能。
\# IPv6 <Sysname> system-view [Sysname] ipv6 route fast-switchover enable

##### 1.1.31 max-ecmp-num

max-ecmp-num 命令用来配置系统支持 IPv4 最大等价路由的条数。
【命令】
max-ecmp-num number【缺省情况】
系统支持最大等价路由的条数为 8。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
number：IPv4 最大等价路由的条数，取值范围为 1～64。
【举例】
\# 配置系统支持 IPv4 最大等价路由的条数为 10。
<Sysname> system-view [Sysname] max-ecmp-num 10 The configuration will take effect at the next reboot. Continue? [Y/N]:y Reboot device to make the configuration take effect.
重启后，系统支持 IPv4 最大等价路由的条数为 10。

##### 1.1.32 non-stop-routing

non-stop-routing 命令用来使能路由的 NSR 功能。
命令用来关闭路由的 功能。
undo non-stop-routing NSR【命令】
non-stop-routing

undo non-stop-routing【缺省情况】
路由的 功能处于关闭状态。
NSR【视图】
RIB IPv4 地址族视图RIB IPv6 地址族视图【缺省用户角色】
network-admin【举例】
\# 使能 IPv4 路由的 NSR 功能。
<Sysname> system-view [Sysname] rib [Sysname-rib] address-family ipv4 [Sysname-rib-ipv4] non-stop-routing

##### 1.1.33 protocol lifetime

protocol lifetime 命令用来配置 IPv4/IPv6 路由和标签在 RIB 中的最大存活时间。
undo protocol lifetime 命令用来恢复缺省情况。
【命令】
protocol protocol [ instance instance-name ] lifetime seconds undo protocol protocol [ instance instance-name ] lifetime【缺省情况】
IPv4/IPv6 路由和标签在 RIB 中的最大存活时间为 480 秒。
【视图】
RIB IPv4 地址族视图RIB IPv6 地址族视图【缺省用户角色】
network-admin【参数】
protocol：路由协议。
instance instance-name：BGP 实例名称，instance-name 为 1～31 个字符的字符串，区分大小写。如果未指定本参数，将配置所有 BGP 实例的最大存活时间。只有当 protocol 是 bgp时该参数可选。
seconds：最大存活时间，取值范围为 1 ～ 6000 ，单位为秒。
【使用指导】
如果配置了该命令，且协议配置 的情况下，需要注意该时间不要与 时间冲突，即必须要保GR GR证协议能够在该时间内完成 GR 并将全部表项下发 RIB，否则会导致 GR 失败并断流。

【举例】
\# 配置 RIB 中 RIP 路由和标签的最大存活时间为 60 秒。
<Sysname> system-view [Sysname] rib [Sysname-rib] address-family ipv4 [Sysname-rib-ipv4] protocol rip lifetime 60

##### 1.1.34 protocol nexthop recursive-lookup

命令用来配置路由按照路由策略进行迭代下一跳查找。
protocol nexthop recursive-lookup命令用来取消该配置。
undo protocol nexthop recursive-lookup【命令】
protocol protocol nexthop recursive-lookup route-policy route-policy-name undo protocol protocol nexthop recursive-lookup route-policy【缺省情况】
未配置路由按路由策略进行下一跳迭代查找。
【视图】
RIB IPv4 地址族视图RIB IPv6 地址族视图【缺省用户角色】
network-admin【参数】
protocol：路由协议，RIB 地址族视图下支持 bgp、static，RIB 地址族视图下支持IPv4 IPv6 bgp4+。
route-policy-name：指定路由策略名，为 1～63 个字符的字符串，区分大小写。
【使用指导】
通过配置按路由策略迭代下一跳，可以对路由迭代的结果进行控制。例如：当路由发生变化时，路由管理需要对非直连的下一跳重新进行迭代。如果不对迭代的结果路由进行任何限制，则路由管理可能会将下一跳迭代到一个错误的转发路径上，从而造成流量丢失。此时，可以通过配置本功能，将错误的依赖路由过滤掉，使路由迭代到通过路由策略过滤的指定依赖路由上。
配置路由策略时，如果配置了 apply 子句，apply 子句不会生效。
配置路由策略时，请确保至少有一个正确的依赖路由能够通过该策略的过滤，否则可能导致相关路由不可达，无法正确指导转发。
【举例】
\# 配置静态路由按照路由策略 policy1 进行下一跳迭代查找。
<Sysname> system-view [Sysname] rib [Sysname-rib] address-family ipv4 [Sysname-rib-ipv4] protocol static nexthop recursive-lookup route-policy policy1

##### 1.1.35 reset ip routing-table statistics protocol

reset ip routing-table statistics protocol 命令用来清除路由表中的路由统计信息。
【命令】
reset ip routing-table statistics protocol [ vpn-instance vpn-instance-name ] { protocol | all } reset ip routing-table [ all-routes | all-vpn-instance ] statistics protocol { protocol | all }【视图】
用户视图【缺省用户角色】
network-admin【参数】
vpn-instance-name：清除指定 VPN 的路由统计信息。vpn-instance-name vpn-instance表示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。
all-routes：清除公网和所有 实例的路由统计信息。
VPN all-vpn-instance：清除所有 实例的路由统计信息。
VPN protocol：清除 路由表中指定路由协议的统计信息。
IPv4 all：清除 路由表中所有路由协议的统计信息。
IPv4【使用指导】
如果没有指定 all-routes、vpn-instance 和 all-vpn-instance 参数，则清除公网的路由统计信息。
【举例】
\# 清除路由表中的路由统计信息。
<Sysname> reset ip routing-table statistics protocol all

##### 1.1.36 reset ipv6 routing-table statistics protocol

reset ipv6 routing-table statistics protocol 命令用来清除 IPv6 路由表中的综合路由统计信息。
【命令】
reset ipv6 routing-table statistics protocol [ vpn-instance vpn-instance-name ] { protocol | all } reset ipv6 routing-table [ all-routes | all-vpn-instance ] statistics protocol { protocol | all }【视图】
用户视图【缺省用户角色】
network-admin

【参数】
vpn-instance vpn-instance-name：清除指定 VPN 的路由统计信息。vpn-instance-name表示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。
all-routes：清除公网和所有 VPN 实例的路由统计信息。
all-vpn-instance：清除所有 VPN 实例的路由统计信息。
protocol：清除 IPv6 路由表中指定路由协议的统计信息。
all：清除 IPv6 路由表中所有路由协议的统计信息。
【使用指导】
如果没有指定 all-routes、vpn-instance 和 参数，则清除公网的路由all-vpn-instance统计信息。
【举例】
\# 清除 IPv6 路由表中所有路由协议的综合路由统计信息。
<Sysname> reset ipv6 routing-table statistics protocol all

##### 1.1.37 rib

命令用来进入 RIB 视图。
rib命令用来删除 RIB 视图下的所有配置。
undo rib【命令】
rib undo rib【视图】
系统视图【缺省用户角色】
network-admin【举例】
\# 进入 RIB 视图。
<Sysname> system-view [Sysname] rib [Sysname-rib]

##### 1.1.38 routing-table limit

routing-table limit 命令用来配置设备支持的最大 IPv4/IPv6 激活路由前缀数。
undo routing-table limit 命令用来恢复缺省情况。
【命令】
routing-table limit number simply-alert undo routing-table limit

【缺省情况】
不限制设备支持的最大 IPv4/IPv6 激活路由前缀数。
【视图】
RIB IPv4 地址族视图RIB IPv6 地址族视图【缺省用户角色】
network-admin【参数】
number：设备支持的最大 激活路由前缀数目，取值范围为 1～4294967295。
IPv4/IPv6 simply-alert：当设备的 激活路由前缀数超过最大支持的激活路由前缀数目时，可以IPv4/IPv6继续激活新的路由前缀，但会产生一条日志信息。
【使用指导】
RIB IPv4 地址族视图下的配置用于控制公网和所有 VPN 实例内 IPv4 激活路由的总数。
RIB IPv6 地址族视图下的配置用于控制公网和所有 VPN 实例内 IPv6 激活路由的总数。
【举例】
\# 配置当前设备上的 RIB IPv4地址族视图下公网和所有 VPN实例内 IPv4激活路由的总数超过 1000时，可以继续激活新的路由前缀，但是会产生一条日志信息。
<Sysname> system-view [Sysname] rib [Sysname-rib] address-family ipv4 [Sysname-rib-ipv4] routing-table limit 1000 simply-alert

## 02-静态路由命令

目 录静态路由配置命令

### 1 静态路由

1静态路由

#### 1.1 静态路由配置命令

##### 1.1.1 delete static-routes all

命令用来删除所有静态路由。
delete static-routes all【命令】
delete [ vpn-instance vpn-instance-name ] static-routes all【视图】
系统视图【缺省用户角色】
network-admin【参数】
： 删 除 指 定 实 例 的 所 有 静 态 路 由 。
vpn-instance vpn-instance-name VPN vpn-instance-name 表示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则表示删除公网的所有静态路由。
【使用指导】
使用本命令删除静态路由时，系统会提示确认，确认后才会删除所配置的所有静态路由。
使用 命令可以删除一条静态路由，而使用undo ip route-static delete static-routes命令可以删除包括缺省路由在内的所有静态路由。
all【举例】
\# 删除所有静态路由。
<Sysname> system-view [Sysname] delete static-routes all This will erase all IPv4 static routes and their configurations, you must reconf igure all static routes.
Are you sure?[Y/N]:y【相关命令】
• ip route-static

##### 1.1.2 display route-static nib

命令用来显示静态路由下一跳信息。
display route-static nib【命令】
display route-static nib [ nib-id ] [ verbose ]【视图】
任意视图

【缺省用户角色】
network-admin network-operator【参数】
nib-id：路由邻居 ID 值，取值范围为十六进制数 1～ffffffff。如果未指定本参数，则显示所有的静态路由下一跳信息。
verbose：显示详细信息。如果未指定本参数，则显示概要信息。
【举例】
显示静态路由下一跳信息。
\# <Sysname> display route-static nib Total number of nexthop(s): 44 NibID: 0x11000000 Sequence: 0 Type: 0x21 Flushed: Yes UserKey0: 0x111 VrfNthp: 0 UserKey1: 0x0 Nexthop: 0.0.0.0 IFIndex: 0x111 LocalAddr: 0.0.0.0 TopoNthp: 0 ExtType: 0x0 NibID: 0x11000001 Sequence: 1 Type: 0x41 Flushed: Yes UserKey0: 0x0 VrfNthp: 5 UserKey1: 0x0 Nexthop: 2.2.2.2 IFIndex: 0x0 LocalAddr: 0.0.0.0 TopoNthp: 0 ExtType: 0x0表1-1 display route-static nib 命令显示信息描述表字段 描述总的下一跳个数Total number of nexthop(s)
NibID NIB ID 号Sequence NIB序列号Type NIB类型是否下刷FIB Flushed UserKey0 NIB协议保留数据1 UserKey1 NIB协议保留数据2 VrfNthp 下一跳所在 VPN 索引，显示为 0 表示公网Nexthop 下一跳信息IFIndex 接口索引

字段 描述LocalAddr 本地接口地址TopoNthp （暂不支持）下一跳所在拓扑索引，显示为0表示公网拓扑NIB扩展类型ExtType \# 显示静态路由下一跳详细信息。
<Sysname> display route-static nib verbose Total number of nexthop(s): 44 NibID: 0x11000000 Sequence: 0 Type: 0x21 Flushed: Yes UserKey0: 0x111 VrfNthp: 0 UserKey1: 0x0 Nexthop: 0.0.0.0 IFIndex: 0x111 LocalAddr: 0.0.0.0 TopoNthp: 0 ExtType: 0x0 RefCnt: 2 FlushRefCnt: 0 Flag: 0x2 Version: 1 1 nexthop(s):
PrefixIndex: 0 OrigNexthop: 0.0.0.0 RelyDepth: 0 RealNexthop: 0.0.0.0 Interface: NULL0 LocalAddr: 0.0.0.0 TunnelCnt: 0 Vrf: default-vrf TunnelID: N/A Topology: base Weight: 1000000 NibID: 0x11000001 Sequence: 1 Type: 0x41 Flushed: Yes UserKey0: 0x0 VrfNthp: 5 UserKey1: 0x0 Nexthop: 2.2.2.2 IFIndex: 0x0 LocalAddr: 0.0.0.0 TopoNthp: 0 ExtType: 0x0 RefCnt: 1 FlushRefCnt: 0 Flag: 0x12 Version: 1 2 nexthop(s):
PrefixIndex: 0 OrigNexthop: 2.2.2.2 RelyDepth: 7 RealNexthop: 8.8.8.8 Interface: Vlan11 LocalAddr: 12.12.12.12 TunnelCnt: 0 Vrf: default-vrf TunnelID: N/A Topology: base Weight: 1000000 PrefixIndex: 0 OrigNexthop: 2.2.2.2 RelyDepth: 9 RealNexthop: 0.0.0.0 Interface: NULL0 LocalAddr: 0.0.0.0 TunnelCnt: 0 Vrf: default-vrf TunnelID: N/A Topology: base Weight: 1000000

表1-2 display route-static nib verbose 命令显示信息描述表字段 描述x nexthop (s) 下一跳具体值（前面数值表示下一跳个数）
等价时下一跳序号PrefixIndex OrigNexthop 原始下一跳RelyDepth 迭代深度真实下一跳RealNexthop Interface 出接口localAddr 本地接口地址TunnelCnt 迭代到隧道的个数VPN实例名，显示为default-vrf表示公网Vrf TunnelID 迭代到隧道的ID Topology （暂不支持）拓扑名称，显示为base表示公网拓扑Weight 等价路由各路由的权重，取值为0表示不是等价路由RefCnt 下一跳信息的引用计数FlushRefCnt 下一跳信息的下刷引用计数Flag 下一跳信息的标志位下一跳信息的版本号Version ExtType NIB扩展类型

##### 1.1.3 display route-static routing-table

命令用来显示静态路由表信息。
display route-static routing-table【命令】
display route-static routing-table [ vpn-instance vpn-instance-name ] [ ip-address { mask-length | mask } ]【视图】
任意视图【缺省用户角色】
network-admin network-operator

【参数】
vpn-instance vpn-instance-name：显示指定 VPN 实例的信息。vpn-instance-name 表示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示公网的信息。
ip-address：目的 地址，点分十进制。如果未指定本参数，则显示所有的静态路由表信息。
IP mask-length：网络掩码长度，取值范围为 0～32。
mask：网络掩码，点分十进制格式。
【举例】
显示静态路由表信息。
\# <Sysname> display route-static routing-table Total number of routes: 24 Status: * - valid
*Destination: 0.0.0.0/0 NibID: 0x1100000a NextHop: 2.2.2.10 MainNibID: N/A BkNextHop: N/A BkNibID: N/A Interface: Vlan-interface11 TableID: 0x2 BkInterface: Vlan-interface12 Flag: 0x82d01 BfdSrcIp: N/A DbIndex: 0xd BfdIfIndex: 0x0 Type: Normal BfdVrfIndex: 0 TrackIndex: 0xffffffff Label: NULL Preference: 60 vrfIndexDst: 0 BfdMode: N/A vrfIndexNH: 0 Permanent: 0 Tag: 0 Destination: 0.0.0.0/0 NibID: 0x1100000b NextHop: 2.2.2.11 MainNibID: N/A BkNextHop: N/A BkNibID: N/A Interface: Vlan-interface13 TableID: 0x2 BkInterface: Vlan-interface14 Flag: 0x82d01 BfdSrcIp: N/A DbIndex: 0xd BfdIfIndex: 0x0 Type: Normal BfdVrfIndex: 0 TrackIndex: 0xffffffff Label: NULL Preference: 60 vrfIndexDst: 0 BfdMode: N/A vrfIndexNH: 0 Permanent: 0 Tag: 0表 命令显示信息描述表1-3 display route-static routing-table字段 描述Total number of routes 总的路由条数

字段 描述Destination 目的地址/掩码NibID 下一跳信息ID FRR静态路由主下一跳信息ID MainNibID BkNibID FRR静态路由备下一跳信息ID NextHop 此路由的下一跳地址BkNextHop 此路由的备份下一跳地址出接口，即到该目的网段的数据包将从此接口发出Interface BkInterface 备份出接口TableID 路由所在的表ID路由标志位Flag DbIndex 路由所在DB的DB索引路由类型：
• Normal：普通类型的静态路由Type • DHCP：DHCP 类型的静态路由
• NAT：NAT 类型的静态路由
• IPsec：IPsec 类型的静态路由BfdSrcIp BFD非直连会话源地址BfdIfIndex BFD使用的接口索引BFD所在VPN索引，显示为0表示公网BfdVrfIndex BFD模式：
• N/A：未配置 BFD 会话BfdMode
• Ctrl：控制报文方式的 BFD 会话
• Echo：echo 报文方式的 BFD 会话Track索引TrackIndex NQA Label 标签Preference 路由优先级vrfIndexDst 目的所在VPN索引，显示为0表示公网下一跳所在VPN索引，显示为0表示公网vrfIndexNH Permanent 永久静态路由标志（1表示永久静态路由）
Tag 路由标记

##### 1.1.4 ip route-static

命令用来配置静态路由。
ip route-static

命令用来删除指定的静态路由。
undo ip route-static【命令】
ip route-static { dest-address { mask-length | mask } | group group-name } { interface-type interface-number [ next-hop-address ] [ backup-interface interface-type interface-number [ backup-nexthop backup-nexthop-address ] [ permanent ] | bfd { control-packet | echo-packet } | permanent | track track-entry-number ] | next-hop-address [ recursive-lookup host-route ] [ bfd control-packet bfd-source ip-address | permanent | track track-entry-number ] | vpn-instance d-vpn-instance-name next-hop-address [ recursive-lookup host-route ] [ bfd control-packet bfd-source ip-address | permanent | track track-entry-number ] } [ preference preference ] [ tag tag-value ] [ description text ] undo ip route-static { dest-address { mask-length | mask } | group group-name } [ interface-type interface-number [ next-hop-address ] | next-hop-address | vpn-instance d-vpn-instance-name next-hop-address ] [ preference preference ] ip route-static vpn-instance s-vpn-instance-name { dest-address { mask-length | mask } | group group-name } { interface-type interface-number [ next-hop-address ] [ backup-interface interface-type interface-number [ backup-nexthop backup-nexthop-address ] [ permanent ] | bfd { control-packet | echo-packet } | permanent | track track-entry-number ] | next-hop-address [ recursive-lookup host-route ] [ public ] [ bfd control-packet bfd-source ip-address | permanent | track track-entry-number ] | vpn-instance d-vpn-instance-name next-hop-address [ recursive-lookup host-route ] [ bfd control-packet bfd-source ip-address | permanent | track track-entry-number ] } [ preference preference ] [ tag tag-value ] [ description text ] undo ip route-static vpn-instance s-vpn-instance-name { dest-address { mask-length | mask } | group group-name } [ interface-type interface-number [ next-hop-address ] | next-hop-address [ public ] | vpn-instance d-vpn-instance-name next-hop-address ] [ preference preference ]【缺省情况】
未配置静态路由。
【视图】
系统视图【缺省用户角色】
network-admin

【参数】
vpn-instance s-vpn-instance-name：指定源 VPN 实例。s-vpn-instance-name 表示MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。每个 VPN 实例都有自己的路由表，配置的静态路由将被加入指定 实例的路由表。
VPN dest-address：静态路由的目的 地址，点分十进制格式。
IP mask-length：网络掩码长度，取值范围为 0～32。
mask：网络掩码，点分十进制格式。
group-name：指定静态路由配置组。group-name 表示配置组名称，为 1～31 个字符的group字符串，区分大小写。
d-vpn-instance-name：指定目的 实例。d-vpn-instance-name 表vpn-instance VPN示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果指定目的 VPN实例，静态路由将根据配置的 在目的 VPN 中查找出接口。
next-hop-address interface-number：指定静态路由的出接口类型和接口号。在指定静态路interface-type由的出接口类型和接口号时需要注意的事项，详见使用指导。
next-hop-address：指定路由的下一跳的 IP 地址，点分十进制格式。在指定路由的下一跳的 IP地址时需要注意的事项，详见使用指导。
host-route：指定静态路由只能迭代到主机路由。
recursive-lookup interface-number：备份出接口。对于备份出接口backup-interface interface-type为非 P2P 类型的接口时（包括 NBMA 类型接口或广播类型接口），必须同时指定其对应的备份下一跳地址。interface-type interface-number 为指定的接口类型和编号。
backup-nexthop backup-nexthop-address：备份下一跳地址。
bfd：使能 BFD（Bidirectional Forwarding Detection，双向转发检测）功能，对静态路由下一跳的可达性进行快速检测，当下一跳不可达时可以快速切换到备份路由。
control-packet：通过 BFD 控制报文方式实现 BFD 功能。
ip-address：BFD 源 IP 地址。建议配置为 Loopback 接口 IP 地址。
bfd-source echo-packet：通过 BFD echo 报文方式实现 BFD 功能。
permanent：指定为永久静态路由。即使在出接口 down 时，配置的永久静态路由仍然保持 active状态。
track-entry-number：将静态路由与 Track 项相关联，track-entry-number 为 Track track项的序号，取值范围为 1～1024。关于 的详细介绍，请参见“可靠性配置指导”中的“Track”。
Track public：指定静态路由下一跳处于公网实例。
preference：指定静态路由的优先级，取值范围为 1～255，缺省值为 60。
preference tag-value：静态路由 Tag 值，用于标识该条静态路由，以便在路由策略中根据 Tag 对路由tag进行灵活的控制。tag-value 的取值范围为 1～4294967295，缺省值为 0。关于路由策略的详细信息，请参见“三层技术-IP 路由配置指导”中的“路由策略”。
description text：配置的静态路由描述信息，取值范围为 1～60 个字符。除“?”外，可以包含空格等特殊字符。

【使用指导】
如果目的 IP 地址和掩码都为 0.0.0.0（或掩码为 0），则配置的路由为缺省路由。当没有匹配的路由表项时，将使用缺省路由进行报文转发。
对不同的优先级配置，可采用不同的路由管理策略。例如，为同一目的地配置多条路由，如果指定相同的优先级，则实现路由负载分担；如果指定不同的优先级，则实现路由备份。
配置静态路由时，可根据实际需要指定出接口或下一跳地址。需要注意的是：
对于 接口，配置了出接口就不需要配置下一跳地址。
• Null0对于点到点接口，配置时可以只指定出接口，不指定下一跳地址。这样，即使对端地址发生
•了变化也无须改变配置。
对于 NBMA、P2MP 等接口，需要进行 地址到链路层地址的映射，建议同时配置出接口和
• IP下一跳 IP 地址。
• 对于广播类型接口，需要通过下一跳 IP 地址来获取下一跳的物理地址，配置时需要指定出接口和下一跳 IP 地址。特殊情况下也可以不配置下一跳 IP 地址，比如 VXLAN 的跨 VPN 引流组网。
配置静态路由时需要注意的是：
路由振荡时，使能 BFD 检测功能可能会加剧振荡，需谨慎使用。关于 BFD 的详细介绍，请参
•考“可靠性配置指导”中的“BFD”。
如果 模块通过 探测私网静态路由中下一跳的可达性，静态路由下一跳的 实
• Track NQA VPN例号与 NQA 测试组配置的实例号必须相同，才能进行正常的探测。
• 在静态路由进行迭代时，Track 项监测的应该是静态路由真正的下一跳，而不是配置的下一跳。
否则，可能导致错误地将有效路由判断为无效路由。
• 参数 permanent 不能和 bfd、track 一起进行配置。
当使用 recursive-lookup host-route 参数指定静态路由迭代到主机路由时，需要在下一跳对应的出接口上配置 开启 ARP 直连路由通告功能，通告 32 位arp route-direct advertise主机路由。
按配置组配置静态路由时，配置组下的所有前缀会应用相同的下一跳、出接口信息。如果配置组不存在或者配置组中没有任何前缀，则不会创建静态路由。
【举例】
\# 配置静态路由，其目的地址为 1.1.1.1/24，指定下一跳为 2.2.2.2，Tag 值为 45，描述信息为“for internet”。
<Sysname> system-view [Sysname] ip route-static 1.1.1.1 24 2.2.2.2 tag 45 description for internet【相关命令】
• arp route-direct advertise（三层技术-IP 业务命令参考/ARP）
• display ip routing-table protocol（三层技术-IP 路由命令参考/IP 路由基础）
• ip route-static-group
• prefix

##### 1.1.5 ip route-static arp-request

ip route-static arp-request 命令用来配置向静态路由下一跳发送 ARP 请求功能。
undo ip route-static arp-request 命令用来关闭向静态路由下一跳发送 ARP 请求功能。
【命令】
ip route-static arp-request [ interval interval ] undo ip route-static arp-request【缺省情况】
静态路由发送 ARP 请求功能处于关闭状态。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
interval：发送 ARP 请求的时间间隔，取值范围为 1～300，单位为秒，缺省值为 5。
【使用指导】
配置静态路由通过指定 参数迭代到主机路由，或按照路由策recursive-lookup host-route略迭代到主机路由时，如果因为下一跳主机不主动发送免费 等原因导致设备上主机路由对应ARP的 ARP 表项不存在，就会造成主机路由不存在、静态路由无法激活，这种场景下可以配置本命令，定时向不带出接口且下一跳迭代失败的静态路由的下一跳发送 ARP 请求，当收到主机的 ARP 应答后，主机路由存在，静态路由便会自动激活，这时停止向该静态路由下一跳发送 ARP 请求。
【举例】
配置向静态路由下一跳发送 请求功能，且发送时间间隔为 秒。
\# ARP 10 <Sysname> system-view [Sysname] ip route-static arp-request interval 10【相关命令】
•ip route-static
• recursive-lookup（三层技术-IP 路由命令参考/IP 路由基础）
protocol nexthop

##### 1.1.6 ip route-static default-preference

ip route-static default-preference 命令用来配置静态路由的缺省优先级。
undo ip route-static default-preference 命令用来恢复缺省情况。
【命令】
ip route-static default-preference default-preference undo ip route-static default-preference【缺省情况】
静态路由的缺省优先级为 60。

【视图】
系统视图【缺省用户角色】
network-admin【参数】
default-preference：静态路由缺省优先级的值，取值范围为 1～255。
【使用指导】
如果在配置静态路由时没有指定优先级，就会使用缺省优先级。
重新配置缺省优先级后，新设置的缺省优先级仅对新增的静态路由有效。
【举例】
\# 配置静态路由的缺省优先级为 120。
<Sysname> system-view [Sysname] ip route-static default-preference 120【相关命令】
protocol（三层技术-IP 路由命令参考/IP 路由基础）
• display ip routing-table

##### 1.1.7 ip route-static fast-reroute auto

命令用来配置静态路由自动快速重路由功能。
ip route-static fast-reroute auto命令用来关闭静态路由自动快速重路由功能。
undo ip route-static fast-reroute auto【命令】
ip route-static fast-reroute auto undo ip route-static fast-reroute auto【缺省情况】
静态路由自动快速重路由功能处于关闭状态。
【视图】
系统视图【缺省用户角色】
network-admin【举例】
\# 配置静态路由自动快速重路由功能。
<Sysname> system-view [Sysname] ip route-static fast-reroute auto

##### 1.1.8 ip route-static primary-path-detect bfd echo

命令用来使能静态路由中主用链路的ip route-static primary-path-detect bfd echo BFD（Echo 方式）检测功能。

命令用来关闭静态路由中主用链路的undo ip route-static primary-path-detect bfd BFD（Echo 方式）检测功能。
【命令】
ip route-static primary-path-detect bfd echo undo ip route-static primary-path-detect bfd【缺省情况】
静态路由中主用链路的 BFD（Echo 方式）检测功能处于关闭状态。
【视图】
系统视图【缺省用户角色】
network-admin【使用指导】
配置本功能后，静态路由的快速重路由特性中的主用链路将使用 BFD（Echo 方式）进行检测。
【举例】
\# 配置静态路由快速重路由特性中主用链路使能 BFD（Echo 方式）功能。
<Sysname> system-view [Sysname] ip route-static 1.1.1.1 32 vlan-interface 10 2.2.2.2 backup-interface vlan-interface 11 backup-nexthop 3.3.3.3 [Sysname] ip route-static primary-path-detect bfd echo

##### 1.1.9 ip route-static-group

ip route-static-group 命令用来创建静态路由配置组，并进入静态路由配置组视图。如果指定的静态路由配置组已经存在，则直接进入静态路由配置组视图。
命令用来删除静态路由配置组。
undo ip route-static-group【命令】
ip route-static-group group-name undo ip route-static-group group-name【缺省情况】
不存在静态路由配置组。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
group-name：指定静态路由配置组。group-name 表示静态路由配置组名称，为 1～31 个字符的字符串，区分大小写。

【举例】
\# 创建静态路由配置组 test，并进入静态路由配置组视图。
<Sysname> system-view [Sysname] ip route-static-group test [Sysname-route-static-group-test]【相关命令】
•ip route-static
• prefix

##### 1.1.10 prefix

prefix 命令用来在静态路由配置组中增加前缀。
undo prefix 命令用来在静态路由配置组中删除前缀。
【命令】
prefix dest-address { mask-length | mask } undo prefix dest-address { mask-length | mask }【缺省情况】
静态路由配置组中未配置前缀。
【视图】
静态路由配置组视图【缺省用户角色】
network-admin【参数】
dest-address：静态路由的目的 IP 地址，点分十进制格式。
mask-length：网络掩码长度，取值范围为 0～32。
mask：网络掩码，点分十进制格式。
【使用指导】
在静态路由配置组视图下可以多次配置该命令，添加多个前缀，并通过命令ip route-static批量创建静态路由；如果已经通过命令 批量创建了静态路由，group ip route-static group后续向配置组中增加前缀，则会一并生成该前缀对应的静态路由。
【举例】
\# 在静态路由配置组 test 中，增加前缀 1.1.1.1/32。
<Sysname> system-view [Sysname] ip route-static-group test [Sysname-route-static-group-test] prefix 1.1.1.1 32【相关命令】
•ip route-static
•ip route-static-group

## 03-RIP命令

目 录配置命令

### 1 RIP

1 RIP

#### 1.1 RIP配置命令

##### 1.1.1 checkzero

命令用来使能 RIP-1 报文的零域检查功能。
checkzero命令用来关闭零域检查功能。
undo checkzero【命令】
checkzero undo checkzero【缺省情况】
报文的零域检查功能处于使能状态。
RIP-1【视图】
RIP 视图【缺省用户角色】
network-admin【使用指导】
使能零域检查功能后，零域中包含非零位的 RIP-1 报文将被拒绝处理。如果用户能确保所有报文都是可信任的，则可以不进行该项检查，以节省 处理时间。
CPU【举例】
\# 关闭进程号为 1 的 RIP 进程对 RIP-1 报文的零域检查功能。
<Sysname> system-view [Sysname] rip [Sysname-rip-1] undo checkzero

##### 1.1.2 default cost

命令用来配置引入路由的缺省度量值。
default cost命令用来恢复缺省情况。
undo default cost【命令】
default cost cost-value undo default cost【缺省情况】
引入路由的缺省度量值为 0 。
【视图】
RIP 视图

【缺省用户角色】
network-admin【参数】
cost-value：引入路由的缺省度量值，取值范围为 0～16。
【使用指导】
当使用 命令从其它协议引入路由时，如果不指定具体的度量值，则引入路由的度import-route量值为 default cost 所指定的值。
【举例】
\# 配置从其它路由协议引入路由的缺省度量值为 3。
<Sysname> system-view [Sysname] rip 1 [Sysname-rip-1] default cost 3【相关命令】
•import-route

##### 1.1.3 default-route

default-route 命令用来配置 RIP 进程下的所有接口以指定度量值向 RIP 邻居发布一条缺省路由。
undo default-route 命令用来恢复缺省情况。
【命令】
default-route { only | originate } [ cost cost-value | route-policy route-policy-name ] * undo default-route【缺省情况】
不向 RIP 邻居发送缺省路由。
【视图】
RIP 视图【缺省用户角色】
network-admin【参数】
only：配置只发送缺省路由，不发送普通路由。
originate：配置既发送普通路由，又发送缺省路由。
cost-value：缺省路由的度量值，取值范围为 1～15，缺省值为 1。
route-policy-name：路由策略名称，route-policy-name 为 1～63 个字route-policy符的字符串，区分大小写。只有当前路由器的路由表中有路由匹配 指定的route-policy-name路由策略时，才发送缺省路由。
【使用指导】
配置了发布缺省路由的 RIP 路由器不接收来自 RIP 邻居的缺省路由。

【举例】
\# 配置 RIP进程100的所有接口向 RIP邻居发布一条度量值为 2的缺省路由，而且只发送缺省路由，不发送普通路由。
<Sysname> system-view [Sysname] rip 100 [Sysname-rip-100] default-route only cost 2【相关命令】
• rip default-route

##### 1.1.4 display rip

命令用来显示 RIP 的当前运行状态及配置信息。
display rip【命令】
display rip [ process-id ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：RIP 进程号，取值范围为 1～65535。如果未指定本参数，则显示所有 RIP 进程的当前运行状态及配置信息。
【举例】
\# 显示所有 RIP 进程的当前运行状态及配置信息。
<Sysname> display rip Public VPN-instance name:
RIP process: 1 RIP version: 1 Preference: 100 Routing policy: abc Fast-reroute:
Routing policy: frr Checkzero: Enabled Default cost: 0 Summary: Enabled Host routes: Enabled Maximum number of load balanced routes: 8 Update time : 30 secs Timeout time : 180 secs Suppress time : 120 secs Garbage-collect time : 120 secs Update output delay: 20(ms) Output count: 3 Graceful-restart interval: 60 secs Triggered Interval : 5 50 200

Silent interfaces: None Default routes: Originate Default routes cost: 3 Verify-source: Enabled Networks:
1.0.0.0 Configured peers:
197.168.6.2 Triggered updates sent: 0 Number of routes changes: 1 Number of replies to queries: 0表1-1 display rip 命令显示信息描述表字段 描述Public VPN-instance name RIP进程运行在公网实例下Private VPN-instance name RIP进程应用于指定VPN实例RIP进程号RIP process RIP version RIP版本，取值为1或2 Preference RIP路由优先级Fast-reroute RIP快速重路由Routing policy 路由策略是否使能对RIP-1报文的零域进行检查的功能
•Checkzero Enable 表示已使能
• Disabled 表示关闭Default cost 引入路由的缺省度量值路由聚合功能是否使能Summary • Enabled 表示已使能
• Disabled 表示关闭是否允许接收主机路由Host routes • Enabled 表示允许
• 表示不允许Disabled Maximum number of load balanced routes 等价路由的最大数目Update time Update定时器的值，单位为秒Timeout time Timeout定时器的值，单位为秒Suppress定时器的值，单位为秒Suppress time Garbage-collect time Garbage-Collect定时器的值，单位为秒Update output delay 接口发送 RIP 报文的时间间隔Output count 接口一次发送RIP报文的最大个数Graceful-restart interval GR重启间隔时间，单位为秒

字段 描述Triggered Interval 发送触发更新的时间间隔Silent interfaces 工作在抑制状态的接口（这些接口不发送周期更新报文）
是否向RIP邻居发布一条缺省路由
• Only：表示只发布缺省路由Default routes
•Originate：表示同时发布缺省路由和普通路由
• Disabled：表示不发布缺省路由Default routes cost RIP进程下发布缺省路由的度量值是否使能对接收到的RIP路由更新报文进行源IP地址检查的功能Verify-source • Enable 表示已使能
• Disabled 表示关闭使能RIP的网段地址Networks Configured peers 配置的邻居Triggered updates sent 发送的触发更新报文数Number of routes changes RIP进程改变路由数据库的统计数据Number of replies to queries RIP请求的响应报文数

##### 1.1.5 display rip database

display rip database 命令用来显示 RIP 数据库的激活路由。
【命令】
display rip process-id database [ ip-address { mask-length | mask } ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：RIP 进程号，取值范围为 1～65535。
}：显示指定目的地址和掩码的激活路由信息。如果未指ip-address { mask-length | mask定本参数，将显示 RIP 的所有激活路由信息。
【举例】
\# 显示 RIP 进程 100 数据库的所有激活路由。
<Sysname> display rip 100 database
1.0.0.0/8, auto-summary
1.1.1.0/24, cost 16, interface summary

1.1.1.0/24, cost 0, nexthop 1.1.1.1, RIP-interface
1.1.2.0/24, cost 0, imported
2.0.0.0/8, auto-summary
2.0.0.0/8, cost 1, nexthop 1.1.1.2
\# 显示 RIP 进程 100 数据库中指定地址和掩码为 1.1.1.0/24 的激活路由。
<Sysname> display rip 100 database 1.1.1.0 24
1.1.1.0/24, cost 16, interface summary
1.1.1.0/24, cost 0, nexthop 1.1.1.1, RIP-interface
表1-2 命令显示信息描述表
display rip database
字段 描述
cost 度量值
auto-summary 表示该条路由是RIP的自动聚合路由
表示该条路由是RIP的接口聚合路由
interface summary
nexthop 下一跳地址
RIP-interface 使能RIP协议的接口的直连路由
表示该条路由是从其它路由协议引入的
imported

##### 1.1.6 display rip graceful-restart

display rip graceful-restart 命令用来显示 RIP 进程的 GR 状态信息。
【命令】
display rip [ process-id ] graceful-restart【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：RIP 进程号，取值范围为 1～65535。如果未指定本参数，则显示所有 RIP 进程的GR 状态信息。
【举例】
显示 进程的 状态信息。
\# RIP 1 GR <Sysname> display rip 1 graceful-restart RIP process: 1 Graceful Restart capability : Enabled Current GR state : Normal Graceful Restart period : 60 seconds Graceful Restart remaining time : 0 seconds

表1-3 display rip graceful-restart 命令显示信息描述表字段 描述RIP process RIP进程号GR使能状态Graceful Restart capability • Enabled：使能了 GR 能力
• Disabled：关闭了 能力GR当前GR所处状态Current GR state • Under GR：进程正在 GR
• Normal：普通状态Graceful Restart period GR重启间隔时间Graceful Restart remaining time GR结束剩余时间

##### 1.1.7 display rip interface

命令用来显示 RIP 的接口信息。
display rip interface【命令】
display rip process-id interface [ interface-type interface-number ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：RIP 进程号，取值范围为 1～65535。
interface-type interface-number：接口类型和编号。如果未指定本参数，将显示 RIP 的所有接口信息。
【举例】
显示 进程 的接口信息。
\# RIP 1 <Sysname> display rip 1 interface Total: 1 Interface: Vlan-interface10 Address/Mask: 1.1.1.1/24 Version: RIPv1 MetricIn: 0 MetricIn route policy: Not designated MetricOut: 1 MetricOut route policy: Not designated Split-horizon/Poison-reverse: On/Off Input/Output: On/On Default route: Off Update output delay: 20(ms) Output count: 3

Current number of packets/Maximum number of packets: 0/2000表1-4 display rip interface 命令显示信息描述表字段 描述Total 运行RIP协议的接口总数Interface 运行RIP协议的接口的名称运行RIP协议的接口的IP地址/掩码Address/Mask Version 接口上运行的RIP协议的版本MetricIn 接收路由的附加度量值接收路由的附加度量值应用的路由策略，取值为Not designated表示没有对接收路由的附加度量值使用路由策略，如果对接收路由的附加度量值使用了路由MetricIn route policy策略，取值为使用的路由策略名称MetricOut 发送路由的附加度量值发送路由的附加度量值应用的路由策略，取值为Not designated表示没有对发MetricOut route policy 送路由的附加度量值使用路由策略，如果对发送路由的附加度量值使用了路由策略，取值为使用的路由策略名称Split-horizon 是否使能了水平分割（On表示使能，Off表示关闭）
Poison-reverse 是否使能了毒性逆转（On表示使能，Off表示关闭）
是否允许接口接收（Input）/发送（Output）RIP报文（On表示允许，Off表示Input/Output不允许）
是否允许向RIP邻居发送缺省路由
• Only：表示只发布缺省路由
• Originate：表示同时发布缺省路由和普通路由Default route
• No-originate：表示只发布普通路由
• Off：表示不发布缺省路由Default route cost RIP接口下配置发布缺省路由的度量值Update output delay 接口发送RIP报文的时间间隔Output count 接口一次发送RIP报文的最大个数Current number of packets显示当前接口待发送的报文数量和最多可以发送的报文数量/Maximum number of packets

##### 1.1.8 display rip neighbor

display rip neighbor 命令用来显示 RIP 进程的邻居信息。
【命令】
display rip process-id neighbor [ interface-type interface-number ]【视图】
任意视图

【缺省用户角色】
network-admin network-operator【参数】
process-id：RIP 进程号，取值范围为 1～65535。
interface-number：接口类型和编号。如果未指定本参数，将显示 RIP 的interface-type所有邻居信息。
【举例】
显示 进程 的邻居信息。
\# RIP 1 <Sysname> display rip 1 neighbor Neighbor address: 197.168.2.3 Interface : Vlan-interface10 Version : RIPv2 Last update: 00h00m02s Relay nbr : N/A BFD session: N/A Bad packets: 0 Bad routes : 0表1-5 display rip neighbor 命令显示信息描述表字段 描述邻居地址Neighbor address Interface 出接口Version 收到邻居RIP报文的版本Last update 上次收到邻居更新报文距离现在时间是否是非直连邻居Relay nbr BFD session BFD会话类型Bad packets 接口收到的错误报文数目Bad routes 接口收到的错误路由数目

##### 1.1.9 display rip non-stop-routing

display rip non-stop-routing 命令用来显示 RIP 进程的 NSR 状态信息。
【命令】
display rip [ process-id ] non-stop-routing【视图】
任意视图【缺省用户角色】
network-admin network-operator

【参数】
process-id：RIP 进程号，取值范围为 1～65535。如果未指定本参数，则显示所有 RIP 进程的NSR 状态信息。
【举例】
显示 进程的 状态信息。
\# RIP 1 NSR <Sysname> display rip 1 non-stop-routing RIP process: 1 Nonstop Routing capability: Enabled Current NSR state : Finish表1-6 display rip non-stop-routing 命令显示信息描述表字段 描述RIP process RIP进程号NSR使能状态Nonstop Routing capability • Enabled：使能 NSR
• Disabled：不使能 NSR当前NSR所处状态
• Initialization：初始准备
• Smooth：数据平滑Current NSR state
• Advertising：发布路由
• Redistribution：路由引入处理
• Finish：完成

##### 1.1.10 display rip route

display rip route 命令用来显示 RIP 的路由信息。
【命令】
display rip process-id route [ ip-address { mask-length | mask } [ verbose ] | peer ip-address | statistics ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：RIP 进程号，取值范围为 1～65535。
ip-address { mask-length | mask }：显示指定目的地址和掩码的路由信息。

verbose：显示当前 RIP 路由表中指定目的地址和掩码的所有路由信息。如果未指定本参数，则只显示指定目的地址和掩码的最优 路由。
RIP ip-address：显示从指定邻居学到的所有路由信息。
peer statistics：显示路由的统计信息。路由的统计信息包括路由总数目，各个邻居的路由数目。
【使用指导】
如果未指定任何参数，将显示 RIP 的所有路由信息。
【举例】
\# 显示进程号为 1 的 RIP 进程所有的路由信息。
<Sysname> display rip 1 route Route Flags: R - RIP, T - TRIP P - Permanent, A - Aging, S - Suppressed, G - Garbage-collect D - Direct, O - Optimal, F - Flush to RIB
---------------------------------------------------------------------------- Peer 1.1.1.1 on Vlan-interface10 Destination/Mask Nexthop Cost Tag Flags Sec
3.0.0.0/8 1.1.1.1 1 0 RAOF 24 Local route Destination/Mask Nexthop Cost Tag Flags Sec
4.4.4.4/32 0.0.0.0 0 0 RDOF -
1.1.1.0/24 0.0.0.0 0 0 RDOF - \# 显示进程号为 1 的 RIP 进程指定路由的全部路由信息。
<Sysname> display rip 1 route 3.0.0.0 8 verbose Route Flags: R - RIP, T - TRIP P - Permanent, A - Aging, S - Suppressed, G - Garbage-collect D - Direct, O - Optimal, F - Flush to RIB
---------------------------------------------------------------------------- Peer 1.1.1.1 on Vlan-interface10 Destination/Mask OrigNexthop/RealNexthop Cost Tag Flags Sec
3.0.0.0/8 1.1.1.1/1.1.1.1 1 0 RAOF 16表1-7 display rip route 命令显示信息描述表字段 描述路由标志：
• R：RIP 生成的路由
• P：该路由永久有效
• A：该路由处于老化时期
• S：该路由处于抑制时期Route Flags
• G：该路由处于 Garbage-collect 时期
• D：RIP 生成的直连路由
• O ：该路由处于最优路由状态
• F：该路由已经被下刷到 RIB Peer X.X.X.X on interface-type在RIP接口上从指定邻居学到的路由信息interface-number

字段 描述Local route RIP本地生成的直连路由Destination/Mask 目的IP地址/掩码路由的下一跳地址Nexthop如果路由来自直连邻居，那么路由的真实下一跳就是原始下一跳；如果路OrigNexthop/RealNexthop 由来自非直连邻居，对于成功迭代的路由RealNexthop则显示迭代出来的下一跳，否则不显示Cost 度量值路由标记Tag Flags 路由信息所处状态Sec 路由信息所处状态对应的定时器时间显示进程号为 的 进程的路由统计信息。
\# 1 RIP <Sysname> display rip 1 route statistics Peer Optimal/Aging Optimal/Permanent Garbage
1.1.1.1 1/1 0/0 0 Local 2/0 0/0 0 Total 3/1 0/0 0表1-8 display rip route statistics 命令显示信息描述表字段 描述Peer RIP邻居IP地址路由信息中处于最优路由状态的路由条数Optimal Aging 路由信息中处于老化状态的路由条数Permanent 路由信息中处于永久有效状态的路由条数Garbage 路由信息中处于Garbage-collection状态的路由条数Local RIP本地生成的直连路由条数的总和Total 从所有RIP邻居学习到的路由条数的总和

##### 1.1.11 dscp

命令用来配置 发送协议报文的 优先级。
dscp RIP DSCP命令用来恢复缺省情况。
undo dscp【命令】
dscp dscp-value undo dscp【缺省情况】
RIP 发送协议报文的 DSCP 优先级为 48。

【视图】
RIP 视图【缺省用户角色】
network-admin【参数】
dscp-value：DSCP 值，取值范围为 0～63。
【举例】
\# 配置 RIP 进程 1 发送协议报文的 DSCP 优先级为 63。
<Sysname> system-view [Sysname] rip 1 [Sysname-rip-1] dscp 63

##### 1.1.12 fast-reroute

命令用来配置 快速重路由功能。
fast-reroute RIP命令用来关闭 快速重路由功能。
undo fast-reroute RIP【命令】
fast-reroute route-policy route-policy-name undo fast-reroute【缺省情况】
RIP 快速重路由功能处于关闭状态。
【视图】
RIP 视图【缺省用户角色】
network-admin【参数】
： 为 通 过 策 略 的 路 由 指 定 备 份 下 一 跳 。
route-policy route-policy-name route-policy-name 为路由策略名，为 1～63 个字符的字符串，区分大小写。
【使用指导】
RIP 快速重路由功能只适合在主链路三层接口 up，主链路由双通变为单通或者不通的情况下使用。
在主链路三层接口 的情况下，本功能不可用。单通现象，即一条链路上的两端，有且只有一down端可以收到另一端发来的报文，此链路称为单向链路。
RIP 快速重路由功能仅对非迭代 RIP 路由（即从直连邻居学到 RIP 路由）有效。
等价路由不支持快速重路由功能。
【举例】
\# 配置对通过策略 frr 的路由指定备份下一跳信息。
<Sysname> system-view [Sysname] ip prefix-list abc index 10 permit 100.1.1.0 24

[Sysname] route-policy frr permit node 10 [Sysname-route-policy-frr-10] if-match ip address prefix-list abc [Sysname-route-policy-frr-10] apply fast-reroute backup-interface vlan-interface 1 backup-nexthop 193.1.1.8 [Sysname-route-policy-frr-10] quit [Sysname] rip 100 [Sysname-rip-100] fast-reroute route-policy frr

##### 1.1.13 filter-policy export

命令用来配置 RIP 对发布的路由信息进行过滤。
filter-policy export命令用来取消 RIP 对发布路由信息的过滤。
undo filter-policy export【命令】
ipv4-acl-number filter-policy { | prefix-list prefix-list-name } export [ protocol [ process-id ] | interface-type interface-number ] undo filter-policy export [ protocol [ process-id ] | interface-type interface-number ]【缺省情况】
RIP 不对发布的路由信息进行过滤。
【视图】
视图RIP【缺省用户角色】
network-admin【参数】
ipv4-acl-number：用于过滤发布的路由信息的 IPv4 ACL 编号，取值范围为 2000～3999。
prefix-list prefix-list-name：指定用于过滤发布路由信息的 IP 地址前缀列表名称。
为 IP 地址前缀列表名称，为 1～63 个字符的字符串，区分大小写。
prefix-list-name protocol：被过滤路由信息的路由协议。
process-id：被过滤路由信息的路由协议的进程号，取值范围为 1～65535。仅当路由协议为 rip、ospf、isis 时需要指定进程号，若未指定，缺省进程号为 1。
interface-number：过滤指定接口发布的路由信息，interface-type interface-type为接口类型和编号。
interface-number【使用指导】
一个协议或接口只能配置一个过滤策略。如果未指定协议或接口，就认为是配置全局过滤策略，同样每次只能配置一个。多次执行本命令，最后一次执行的命令生效。
如果已经配置了基于协议或接口的过滤策略，删除时必须指定 protocol 或 interface-type。
interface-number当配置的是高级 ACL（3000～3999）时，其使用规则如下：
• 使用命令rule [ rule-id ] { deny | permit } ip source sour-addr来过滤指定目的地址的路由。
sour-wildcard

使用命令
• rule [ rule-id ] { deny | permit } ip source sour-addr来过滤指定目的地址和掩sour-wildcard destination dest-addr dest-wildcard码的路由。
其中，source 用来过滤路由目的地址，destination 用来过滤路由掩码，配置的掩码应该是连续的（当配置的掩码不连续时该过滤掩码的条件不生效）。
【举例】
\# 配置使用编号为 2000 的基本 ACL 来对发布的路由信息进行过滤。
<Sysname> system-view [Sysname] acl basic 2000 [Sysname-acl-ipv4-basic-2000] rule deny source 192.168.10.0 0.0.0.255 [Sysname-acl-ipv4-basic-2000] quit [Sysname] rip 1 [Sysname-rip-1] filter-policy 2000 export \# 配置按照地址前缀列表来过滤发布的路由信息。
<Sysname> system-view [Sysname] ip prefix-list abc index 10 permit 11.0.0.0 8 [Sysname] rip 1 [Sysname-rip-1] filter-policy prefix-list abc export \# 使用编号为 3000 的高级 ACL 对发布的路由进行过滤，只允许 113.0.0.0/16 通过。
<Sysname> system-view [Sysname] acl advanced 3000 [Sysname-acl-ipv4-adv-3000] rule 10 permit ip source 113.0.0.0 0 destination 255.255.0.0 0 [Sysname-acl-ipv4-adv-3000] rule 100 deny ip [Sysname-acl-ipv4-adv-3000] quit [Sysname] rip 1 [Sysname-rip 1] filter-policy 3000 export【命令参考】
• acl（ACL 和 QoS 命令参考/ACL）
• import-route
• ip prefix-list（三层技术-IP 路由命令参考/路由策略）

##### 1.1.14 filter-policy import

命令用来配置 对接收的路由信息进行过滤。
filter-policy import RIP命令用来取消对接收路由信息的过滤。
undo filter-policy import【命令】
filter-policy { ipv4-acl-number | gateway prefix-list-name | prefix-list prefix-list-name [ gateway prefix-list-name ] } import [ interface-type interface-number ] undo filter-policy import [ interface-type interface-number ]【缺省情况】
不对接收的路由信息进行过滤。
RIP

【视图】
RIP 视图【缺省用户角色】
network-admin【参数】
ipv4-acl-number：用于过滤发布的路由信息的 编号，取值范围为 2000～3999。
IPv4 ACL prefix-list-name：指定用于过滤接收路由信息的 IP 地址前缀列表名称。
prefix-list prefix-list-name 为 IP 地址前缀列表名称，为 1～63 个字符的字符串，区分大小写。
： 基 于 要 加 入 到 路 由 表 的 路 由 信 息 的 下 一 跳 进 行 过 滤 。
gateway prefix-list-name prefix-list-name 为 IP 地址前缀列表名称，为 1～63 个字符的字符串，区分大小写。
interface-type interface-number：过滤指定接口接收的路由信息，interface-type为接口类型和编号。
interface-number【使用指导】
一个接口只能配置一个过滤策略。如果未指定接口，就认为是配置全局过滤策略，同样每次只能配置一个。多次执行本命令，最后一次执行的命令生效。
如果已经配置了基于接口的过滤策略，删除时必须指定 interface-number。
interface-type当配置的是高级 ACL（3000～3999）时，其使用规则如下：
使用命令
• rule [ rule-id ] { deny | permit } ip source sour-addr sour-wildcard 来过滤指定目的地址的路由。
• 使用命令 rule [ rule-id ] { deny | permit } ip source sour-addr sour-wildcard destination dest-addr dest-wildcard 来过滤指定目的地址和掩码的路由。
其中，source 用来过滤路由目的地址，destination 用来过滤路由掩码，配置的掩码应该是连续的（当配置的掩码不连续时该过滤掩码的条件不生效）。
【举例】
\# 配置使用编号为 2000 的基本 ACL 来对接收的路由信息进行过滤。
<Sysname> system-view [Sysname] acl basic 2000 [Sysname-acl-ipv4-basic-2000] rule deny source 192.168.10.0 0.0.0.255 [Sysname-acl-ipv4-basic-2000] quit [Sysname] rip 1 [Sysname-rip-1] filter-policy 2000 import \# 配置按照地址前缀列表来过滤接收的路由信息。
<Sysname> system-view [Sysname] ip prefix-list abc index 10 permit 11.0.0.0 8 [Sysname] rip 1 [Sysname-rip-1] filter-policy prefix-list abc import \# 使用编号为 3000 的高级 ACL 对接收的路由进行过滤，只允许 113.0.0.0/16 通过。
<Sysname> system-view [Sysname] acl advanced 3000 [Sysname-acl-ipv4-adv-3000] rule 10 permit ip source 113.0.0.0 0 destination 255.255.0.0 0

[Sysname-acl-ipv4-adv-3000] rule 100 deny ip [Sysname-acl-ipv4-adv-3000] quit [Sysname] rip 1 [Sysname-rip-1] filter-policy 3000 import【命令参考】
acl（ACL 和 QoS 命令参考/ACL）
•
• prefix-list（三层技术-IP 路由命令参考/路由策略）
ip

##### 1.1.15 graceful-restart

命令用来使能 RIP 协议的 GR 能力。
graceful-restart undo graceful-restart 命令用来关闭 RIP 协议的 GR 能力。
【命令】
graceful-restart undo graceful-restart【缺省情况】
协议的 能力处于关闭状态。
RIP GR【视图】
RIP 视图【缺省用户角色】
network-admin【使用指导】
RIP GR 特性与 RIP NSR 特性互斥，即 和 命令互斥，graceful-restart non-stop-routing不能同时配置。
【举例】
\# 使能 RIP 进程 1 的 GR 能力。
<Sysname> system-view [Sysname] rip 1 [Sysname-rip-1] graceful-restart

##### 1.1.16 graceful-restart interval

命令用来配置 协议的 重启间隔时间。
graceful-restart interval RIP GR命令用来恢复缺省情况。
undo graceful-restart interval【命令】
graceful-restart interval interval undo graceful-restart interval【缺省情况】
RIP 协议的 GR 重启间隔时间为 60 秒。

【视图】
RIP 视图【缺省用户角色】
network-admin【参数】
interval：指定 协议的 重启间隔时间（期望重启时间），取值范围为 5～360，单位为秒。
RIP GR【举例】
\# 配置 RIP 进程 1 的 GR 重启间隔时间为 200 秒。
<Sysname> system-view [Sysname] rip 1 [Sysname-rip-1] graceful-restart interval 200

##### 1.1.17 host-route

命令用来允许 接收主机路由。
host-route RIP命令用来禁止 接收主机路由。
undo host-route RIP【命令】
host-route undo host-route【缺省情况】
允许 RIP 接收主机路由。
【视图】
RIP 视图【缺省用户角色】
network-admin【使用指导】
在某些特殊情况下，路由器会收到大量来自同一网段的主机路由。这些路由对于路由寻址没有多少作用，却占用了大量的资源；此时可以使用 undo host-route 命令禁止接收主机路由，以节省网络资源。
该命令仅对 RIPv2 报文携带的路由有效，对 RIPv1 报文携带的路由无效。
【举例】
\# 禁止 RIP 接收主机路由。
<Sysname> system-view [Sysname] rip 1 [Sysname-rip-1] undo host-route

##### 1.1.18 import-route

命令用来从其它路由协议引入路由。
import-route

命令用来取消引入外部路由信息。
undo import-route【命令】
import-route bgp [ as-number ] [ allow-ibgp ] [ cost cost-value | route-policy route-policy-name | tag tag ] * undo import-route bgp import-route { direct | static } [ cost cost-value | route-policy route-policy-name | tag tag ] * undo import-route { direct | static } import-route { isis | ospf | rip } [ process-id | all-processes ] [ allow-direct | cost cost-value | route-policy route-policy-name | tag tag ] * undo import-route { isis | ospf | rip } [ process-id | all-processes ]【缺省情况】
不引入其它路由。
RIP【视图】
RIP 视图【缺省用户角色】
network-admin【参数】
bgp：引入 BGP 协议的路由。
direct：引入直连路由。
isis：引入 IS-IS 协议的路由。
ospf：引入 OSPF 协议的路由。
rip：引入 RIP 协议的路由。
static：引入静态路由。
as-number：引入指定 AS 内的路由。as-number 为 AS 号，取值范围为 1～4294967295。如果没有指定本参数，则引入所有的 IPv4 EBGP 路由。建议配置时指定 AS 号，否则引入的 IPv4 EBGP路由数量过多时，会引发设备内存资源紧张等问题。
process-id：IS-IS、OSPF 或 RIP 路由协议的进程号，取值范围为 1～65535，缺省值为 1。
all-processes：引入 IS-IS、OSPF 或 RIP 路由协议所有进程的路由。
allow-ibgp：允许引入 IBGP 路由。import-route 表示只引入 EBGP 路由；import-route bgp表示将 路由也引入，容易引起路由环路，请慎用。
bgp allow-ibgp IBGP allow-direct：在引入的路由中包含使能了该协议的接口网段路由。如果未指定本参数，在引入协议路由时不会包含使能了该协议的接口网段路由。当 allow-direct 与 route-policy route-policy-name 参数一起使用时，需要注意路由策略中配置的匹配规则不要与接口路由信息存在冲突，否则会导致 配置失效。例如，当配置 参数引入 OSPF allow-direct allow-direct直连时，在路由策略中不要配置 匹配条件，否则，allow-direct 参数if-match route-type失效。
cost cost-value：所要引入路由的度量值，取值范围为 0～16，缺省值为 0。

route-policy-name：路由策略名称，route-policy-name 为 1～63 个字route-policy符的字符串，区分大小写。
tag：所要引入路由的标记值，取值范围为 0～65535，缺省值为 0。
tag【使用指导】
只 能 引 入 路 由 表 中 状 态 为 active 的 路 由 ， 是 否 为 active 状 态 可 以 通 过 display ip命令来查看。
routing-table protocol undo import-route { isis | ospf | rip } all-processes 命令只能取消 import-route命令的配置，不能取消{ isis | ospf | rip } all-processes import-route { isis | ospf命令的配置。
| rip } process-id【举例】
\# 引入静态路由，并将其度量值设置为 4。
<Sysname> system-view [Sysname] rip 1 [Sysname-rip-1] import-route static cost 4【命令参考】
• default cost

##### 1.1.19 maximum load-balancing

maximum load-balancing 命令用来配置 RIP 最大等价路由条数。
undo maximum load-balancing 命令用来恢复缺省情况。
【命令】
maximum load-balancing number undo maximum load-balancing【缺省情况】
RIP 支持的等价路由的最大条数与系统支持最大等价路由的条数相同。
【视图】
视图RIP【缺省用户角色】
network-admin【参数】
number：等价路由的最大条数，当 number 取值为 1 时，相当于不进行负载分担。取值范围为 1～m。m 为系统支持的最大等价路由条数。m 的取值为 64 和 命令取值中的最小值，max-ecmp-num通过 命令对 进行修改，那么修改的 取值在设备重启后生效。
max-ecmp-num m m【使用指导】
通过配置 max-ecmp-num 命令，对系统支持最大等价路由的条数进行修改，导致当前 RIP 支持的等价路由的最大条数大于 命令的取值，那么设备重启后，RIP 支持的等价路由的max-ecmp-num最大条数自动修改为 的取值。
max-ecmp-num

【举例】
\# 配置 RIP 最大等价路由条数为 2。
<Sysname> system-view [Sysname] rip [Sysname-rip-1] maximum load-balancing 2【相关命令】
• max-ecmp-num（三层技术-IP 路由命令参考/IP 路由基础）

##### 1.1.20 network

network 命令用来在指定网段上使能 RIP。
undo network 命令用来在指定网段上关闭 RIP。
【命令】
network network-address [ wildcard-mask ] undo network network-address【缺省情况】
没有网段使能 RIP。
【视图】
RIP 视图【缺省用户角色】
network-admin【参数】
network-address：指定网段的地址，其取值可以为各个接口的 IP 网络地址。
wildcard-mask：IP 地址掩码的反码，相当于将 IP 地址的掩码取反（0 变 1，1 变 0）。其中，“1”表示忽略 IP 地址中对应的位，“0”表示必须保留此位。（例如：子网掩码 255.0.0.0，该掩码的反码为 0.255.255.255）。如果未指定本参数，将按照自然网段进行。
【使用指导】
RIP 只在指定网段的接口上运行，指定网段可以配置掩码；对于不在指定网段上的接口，RIP 既不在它上面接收和发送路由，也不将它的接口路由发布出去。因此，RIP 启动后必须指定其工作网段。
在单进程情况下，可以使用 0.0.0.0 命令在所有接口上使能 RIP；在多进程情况下，无法network使用 0.0.0.0 命令。
network RIP 不支持将同一物理接口下的不同网段使能到不同的 RIP 进程中。
【举例】
在指定网段 上使能 进程 100。
\# 129.102.0.0 RIP <Sysname> system-view [Sysname] rip 100 [Sysname-rip-100] network 129.102.0.0【相关命令】
• rip enable

##### 1.1.21 non-stop-routing

non-stop-routing 命令用来使能 RIP 协议的 NSR 功能。
undo non-stop-routing 命令用来关闭 RIP 协议的 NSR 功能。
【命令】
non-stop-routing undo non-stop-routing【缺省情况】
RIP 协议的 NSR 功能处于关闭状态。
【视图】
视图RIP【缺省用户角色】
network-admin【使用指导】
各个进程的 NSR 功能是相互独立的，只对本进程生效。如果存在多个 RIP 进程，建议在各个进程下使能 RIP NSR 功能。
RIP NSR 特性与 RIP GR 特性互斥，即 和 命令互斥，non-stop-routing graceful-restart不能同时配置。
【举例】
\# 配置 RIP 进程 1 使能 NSR 功能。
<Sysname> system-view [Sysname] rip 1 [Sysname-rip-1] non-stop-routing

##### 1.1.22 output-delay

用来配置 报文的发送速率。
output-delay RIP命令用来恢复缺省情况。
undo output-delay【命令】
output-delay time count count undo output-delay【缺省情况】
接口发送 RIP 报文的时间间隔为 20 毫秒，一次最多发送 3 个 RIP 报文。
【视图】
RIP 视图【缺省用户角色】
network-admin

【参数】
time：接口发送 RIP 报文的时间间隔，取值范围为 10～100，单位为毫秒。
count：接口一次发送 RIP 报文的最大个数，取值范围为 1～30。
【举例】
\# 配置 RIP 进程 1 的所有接口发送 RIP 报文的时间间隔为 60 毫秒，一次最多发送 10 个 RIP 报文。
<Sysname> system-view [Sysname] rip 1 [Sysname-rip-1] output-delay 60 count 10

##### 1.1.23 peer

peer 命令用来配置 NBMA（Non-Broadcast Multi-Access，非广播多路访问）网络中 RIP 邻居的IP 地址，并使更新报文以单播形式发送到对端，而不采用正常的组播或广播的形式。
命令用来取消指定邻居 IP 地址。
undo peer【命令】
peer ip-address undo peer ip-address【缺省情况】
RIP 不向任何定点地址发送单播更新报文。
【视图】
RIP 视图【缺省用户角色】
network-admin【参数】
ip-address：RIP 邻居 IP 地址，用点分十进制格式表示。
【使用指导】
当 邻居与当前设备直连时不推荐使用该命令，因为这样可能会造成对端同时收到同一路由信息RIP的组播（或广播）和单播两种形式的报文。
配置本命令时，必须同时配置 undo validate-source-address 命令，即取消对接收到的 RIP路由更新报文进行源 IP 地址检查。
【举例】
\# 配置 RIP 邻居的 IP 地址为 202.38.165.1。
<Sysname> system-view [Sysname] rip 1 [Sysname-rip-1] peer 202.38.165.1【相关命令】
• validate-source-address

##### 1.1.24 preference

preference 命令用来配置 RIP 路由的优先级。
undo preference 命令用来恢复缺省情况。
【命令】
preference { preference | route-policy route-policy-name } * undo preference【缺省情况】
RIP 路由的优先级为 100。
【视图】
视图RIP【缺省用户角色】
network-admin【参数】
preference：RIP 路由优先级的值，取值范围为 1～255，取值越小，优先级越高。
route-policy route-policy-name：路由策略名称，route-policy-name 为 1～63 个字符的字符串，区分大小写。对满足特定条件的路由设置优先级。
【使用指导】
通过指定 参数，可应用路由策略对特定的路由设置优先级：
route-policy如果在路由策略中已经设置了匹配路由的优先级，则匹配路由取路由策略设置的优先级，其
•它路由取 preference 命令所设优先级。
• 如果在路由策略中没有设置匹配路由的优先级，则所有路由都取 preference 命令所设优先级。
【举例】
\# 配置 RIP 路由的优先级为 120。
<Sysname> system-view [Sysname] rip 1 [Sysname-rip-1] preference 120

##### 1.1.25 reset rip process

reset rip process 命令用来重启指定 RIP 进程。
【命令】
reset rip process-id process【视图】
用户视图【缺省用户角色】
network-admin

【参数】
process-id：RIP 进程号，取值范围为 1～65535。
【使用指导】
执行该命令后，系统提示用户确认是否重启 RIP 协议。
【举例】
重启进程号为 的 进程。
\# 100 RIP <Sysname> reset rip 100 process Reset RIP process? [Y/N]:y

##### 1.1.26 reset rip statistics

命令用来清除指定 进程的统计信息，便于在调试时重新记录统计reset rip statistics RIP数据。
【命令】
reset rip process-id statistics【视图】
用户视图【缺省用户角色】
network-admin【参数】
process-id：RIP 进程号，取值范围为 1～65535。
【举例】
\# 清除进程号为 100 的 RIP 进程的统计信息。
<Sysname> reset rip 100 statistics

##### 1.1.27 rip

命令用来启动 RIP，并进入 视图。
rip RIP命令用来关闭 RIP。
undo rip【命令】
rip [ process-id ] [ vpn-instance vpn-instance-name ] undo rip [ process-id ]【缺省情况】
系统没有运行 RIP。
【视图】
系统视图【缺省用户角色】
network-admin

【参数】
process-id：RIP 进程号，取值范围为 1～65535，缺省值为 1。
vpn-instance vpn-instance-name：指定 RIP 所属的 VPN 实例。vpn-instance-name 表示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则表示 位于公网中。
RIP【使用指导】
必须先启动 RIP 进程，才能配置 RIP 的各种全局性参数，而配置与接口相关的参数时，可以不受这个限制。
关闭 RIP 进程后，原来配置的接口参数也同时失效。
【举例】
\# 启动 RIP 进程 1，并进入 RIP 视图。
<Sysname> system-view [Sysname] rip [Sysname-rip-1]

##### 1.1.28 rip authentication-mode

rip authentication-mode 命令用来配置 RIP-2 的验证方式及验证参数。
undo rip authentication-mode 命令用来恢复缺省情况。
【命令】
rip authentication-mode { md5 { rfc2082 { cipher | plain } string key-id | rfc2453 { cipher | plain } string } | simple { cipher | plain } string } undo rip authentication-mode【缺省情况】
未配置 RIP-2 的验证方式。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
md5：MD5 验证方式。
rfc2082：指定 MD5 验证报文使用 RFC 2082 规定的报文格式。
cipher：以密文方式设置密钥。
plain：以明文方式设置密钥，该密钥将以密文形式存储。
string：密钥字符串，区分大小写。明文密钥为 1～16 个字符的字符串，密文密钥为 33～53 个字符的字符串。
key-id：验证字标识符，取值范围为 1～255。
rfc2453：指定 MD5 验证报文使用 RFC 2453 规定的报文格式（IETF 标准）。

simple：简单验证方式。
【使用指导】
每次验证只支持一个验证字，新输入的验证字将覆盖旧验证字。
当 的版本为 时，虽然在接口视图下仍然可以配置验证方式，但由于 不支持认证，RIP RIP-1 RIP-1因此该配置不会生效。
【举例】
\# 在接口 Vlan-interface10 上配置 RFC 2453 格式的 MD5 明文验证，密钥为 rose。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] rip version 2 [Sysname-Vlan-interface10] rip authentication-mode md5 rfc2453 plain rose【命令参考】
• rip version

##### 1.1.29 rip bfd enable

rip bfd enable 命令用来使能 RIP 的 BFD 功能。
undo rip bfd enable 命令用来关闭 RIP 的 BFD 功能。
【命令】
rip bfd enable undo rip bfd enable【缺省情况】
RIP 的 BFD 功能处于关闭状态。
【视图】
接口视图【缺省用户角色】
network-admin【使用指导】
RIP 支持采用 BFD 的直连 echo 检测方式和非直连 control 检测方式。
RIP 的邻居是单跳的概念，适合采用 BFD 的 echo 单向检测方式，但是，经过多跳到达邻居时 echo方式则会失效。
由于 peer 命令与邻居之间没有对应关系，undo peer 操作并不能立刻删除邻居，因此不能立刻删除 BFD 会话。
本命令与 命令互斥，不能同时使用。
rip bfd enable destination【举例】
在接口 使能 的 功能。
\# Vlan-interface11 RIP BFD <Sysname> system-view [Sysname] interface vlan-interface 11 [Sysname-Vlan-interface11] rip bfd enable

##### 1.1.30 rip bfd enable destination

rip bfd enable destination 命令用来使能 RIP 指定目的地址的 BFD 功能。
undo rip bfd enable 命令用来关闭 RIP 指定目的地址的 BFD 功能。
【命令】
rip bfd enable destination ip-address undo rip bfd enable【缺省情况】
RIP 指定目的地址的 BFD 功能处于关闭状态。
【视图】
接口视图【缺省用户角色】
network-admin【使用指导】
该命令指定了链路检测的目的地址，当到该目的地址的链路出现故障时，便不再从该接口收发任何RIP 报文。
该命令只支持采用 BFD 的直连 echo 检测方式。
该命令与 命令互斥，不能同时使用。
rip bfd enable【举例】
在接口 使能 指定目的地址 的 功能。
\# Vlan-interface10 RIP 202.38.165.1 BFD <Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] rip bfd enable destination 202.38.165.1

##### 1.1.31 rip default-route

命令用来配置 RIP 接口以指定度量值向 RIP 邻居发布一条缺省路由。
rip default-route命令用来禁止 RIP 接口向 RIP 邻居发布缺省路由。
undo rip default-route【命令】
rip default-route { { only | originate } [ cost cost-value | route-policy route-policy-name ] * | no-originate } undo rip default-route【缺省情况】
RIP 接口是否发布缺省路由以 RIP 进程配置为准。
【视图】
接口视图【缺省用户角色】
network-admin

【参数】
only：配置只发送缺省路由，不发送普通路由。
originate：配置既发送普通路由，又发送缺省路由。
cost-value：缺省路由的度量值，取值范围为 1～15，缺省值为 1。
route-policy route-policy-name：路由策略名称，route-policy-name 为 1～63 个字符的字符串，区分大小写。只有当前路由器的路由表中有路由匹配 指定的route-policy-name路由策略时，才发送缺省路由。
no-originate：配置只发送普通路由，不发布缺省路由。
【使用指导】
配置了发布缺省路由的 路由器不接收来自 邻居的缺省路由。
RIP RIP【举例】
\# 配置接口 Vlan-interface10 以指定度量值 2 向 RIP 邻居发布一条缺省路由，而且只发送缺省路由，不发送普通路由。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] rip default-route only cost 2 \# 指定接口 Vlan-interface10 以指定度量值 2 向 RIP 邻居既发布缺省路由，而且发送普通路由。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] rip default-route originate cost 2【相关命令】
•default-route

##### 1.1.32 rip enable

命令用来在接口上使能 RIP。
rip enable命令用来在接口上关闭 RIP。
undo rip enable【命令】
rip process-id enable [ exclude-subip ] undo rip enable【缺省情况】
接口上没有使能 RIP。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
process-id：RIP 进程号，取值范围为 1～65535。
exclude-subip：不包括接口的从 IP 地址。如果未指定本参数，将包括接口的从 IP 地址。

【使用指导】
本命令的优先级高于 network 命令。
【举例】
\# 在接口 Vlan-interface10 上使能 RIP 进程 100。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] rip 100 enable【相关命令】
• network

##### 1.1.33 rip input

命令用来允许接口接收 RIP 报文。
rip input命令用来禁止接口接收 RIP 报文。
undo rip input【命令】
rip input undo rip input【缺省情况】
允许接口接收 RIP 报文。
【视图】
接口视图【缺省用户角色】
network-admin【举例】
\# 禁止接口 Vlan-interface10 接收 RIP 报文。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] undo rip input

##### 1.1.34 rip max-packet-length

命令用来配置 RIP 报文的最大长度。
rip max-packet-length命令用来恢复缺省情况。
undo rip max-packet-length【命令】
rip max-packet-length value undo rip max-packet-length【缺省情况】
报文的最大长度为 字节。
RIP 512

【视图】
接口视图【缺省用户角色】
network-admin【参数】
value：指定 报文的最大长度，取值范围为 32～65535，单位为字节。
RIP【使用指导】
由于不同厂商对 RIP 报文最大长度的支持情况不同，要谨慎使用本特性，以免出现不兼容的情况。
在配置认证的情况下，如果配置不当可能会造成报文无法发送，建议用户按照下面进行配置：
简单验证方式时，RIP 报文的最大长度不小于 字节；
• 52验证方式（使用 规定的报文格式）时，RIP 报文的最大长度不小于 字节；
• MD5 RFC 2453 56验证方式（使用 规定的报文格式）时，RIP 报文的最大长度不小于 字节。
• MD5 RFC 2082 72如果配置值大于接口 MTU，则报文的最大长度为接口 MTU。
【举例】
\# 在接口 Vlan-interface10 配置 RIP 报文的最大长度为 1024 字节。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] rip max-packet-length 1024

##### 1.1.35 rip metricin

命令用来配置接口接收 路由时的附加度量值。
rip metricin RIP命令用来恢复缺省情况。
undo rip metricin【命令】
rip metricin [ route-policy route-policy-name ] value undo rip metricin【缺省情况】
接口接收 RIP 路由时的附加度量值为 0。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
route-policy-name：路由策略名称，route-policy-name 为 1～63 个字route-policy符的字符串，区分大小写。对满足特定条件的路由设置附加度量值。
value：接收附加度量值，取值范围为 0～16。

【使用指导】
当接口收到一条合法的 RIP 路由，在将其加入路由表前，附加度量值会被加到该路由上。因此，增加接口的接收附加度量值，该接口收到的 RIP 路由的度量值也会相应增加，当附加度量值与原路由度量值之和大于 16，该条路由的度量值取 16。
通过指定 参数，可应用路由策略对接口接收的特定路由设置附加度量值：
route-policy如果通过 命令设置了匹配路由的附加度量值，则匹配路由的附加度量值取
• apply cost apply cost 命令 value 参数设置的值，不匹配路由的附加度量值取本命令 value 参数所设的值。本命令不支持通过 apply cost 命令中的+、-关键字对接口接收 RIP 路由的附加度量值进行增加、减少的设置。
• 如果没有通过 命令设置路由的附加度量值，则所有接收路由的附加度量值都取apply cost本命令 参数所设的值。
value【举例】
\# 对接口 Vlan-interface10 接收的 RIP 路由附加度量值进行设置。其中，1.0.0.0/8 网段路由的附加度量值设置为 6，其它网段路由的附加度量值设置为 2。
<Sysname> system-view [Sysname] ip prefix-list 123 permit 1.0.0.0 8 [Sysname] route-policy abc permit node 10 [Sysname-route-policy-abc-10] if-match ip address prefix-list 123 [Sysname-route-policy-abc-10] apply cost 6 [Sysname-route-policy-abc-10] quit [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] rip metricin route-policy abc 2【相关命令】
cost（三层技术-IP 路由命令参考/路由策略）
• apply

##### 1.1.36 rip metricout

命令用来配置接口发送 路由时的附加度量值。
rip metricout RIP命令用来恢复缺省情况。
undo rip metricout【命令】
rip metricout [ route-policy route-policy-name ] value undo rip metricout【缺省情况】
接口发送 RIP 路由时的附加度量值为 1。
【视图】
接口视图【缺省用户角色】
network-admin

【参数】
route-policy route-policy-name：路由策略名称，route-policy-name 为 1～63 个字符的字符串，区分大小写。对满足特定条件的路由设置附加度量值。
value：发送附加度量值，取值范围为 1～16。
【使用指导】
当发布一条 路由时，附加度量值会在发布该路由之前附加在这条路由上。因此，增加一个接口RIP的发送附加度量值，该接口发送的 RIP 路由的度量值也会相应增加。
通过指定 route-policy 参数，可应用路由策略对接口发布的特定路由设置附加度量值：
如果通过 命令设置了匹配路由的附加度量值，则匹配路由的附加度量值取
• apply cost apply cost 命令 value 参数设置的值，不匹配路由的附加度量值取本命令 value 参数所设的值。本命令不支持通过 命令中的+、-关键字对接口发布 RIP 路由的附加度apply cost量值进行增加、减少的设置。
如果没有通过 命令设置路由的附加度量值，则所有发布路由的附加度量值都取
• apply cost本命令 value 参数所设的值。
【举例】
\# 对接口 Vlan-interface10 发送的 RIP 路由附加度量值进行设置。其中，1.0.0.0/8 网段路由的附加度量值设置为 6，其它网段路由的附加度量值设置为 2。
<Sysname> system-view [Sysname] ip prefix-list 123 permit 1.0.0.0 8 [Sysname] route-policy abc permit node 10 [Sysname-route-policy-abc-10] if-match ip address prefix-list 123 [Sysname-route-policy-abc-10] apply cost 6 [Sysname-route-policy-abc-10] quit [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] rip metricout route-policy abc 2【相关命令】
• apply cost（三层技术-IP 路由命令参考/路由策略）

##### 1.1.37 rip mib-binding

rip mib-binding 命令用来配置 RIP 进程绑定 MIB。
命令用来恢复缺省情况。
undo rip mib-binding【命令】
rip mib-binding process-id undo rip mib-binding【缺省情况】
MIB 绑定在进程号最小的 RIP 进程上。
【视图】
系统视图

【缺省用户角色】
network-admin【参数】
process-id：RIP 进程号，取值范围为 1～65535。
【使用指导】
如果指定的 不存在，配置 进程绑定命令不生效。
process-id RIP如果配置了 RIP 进程绑定 MIB，若删除 对应的 RIP 进程，则同时删除 RIP 进程绑定process-id MIB 配置，MIB 绑定到进程号最小的 RIP 进程上。
【举例】
\# 配置 RIP 进程 100 绑定 MIB。
<Sysname> system-view [Sysname] rip mib-binding 100

##### 1.1.38 rip output

命令用来允许接口发送 RIP 报文。
rip output undo rip output 命令用来禁止接口发送 RIP 报文。
【命令】
rip output undo rip output【缺省情况】
允许接口发送 报文。
RIP【视图】
接口视图【缺省用户角色】
network-admin【举例】
\# 禁止接口 Vlan-interface10 发送 RIP 报文。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] undo rip output

##### 1.1.39 rip output-delay

rip output-delay 命令用来配置接口下 RIP 报文的发送速率。
undo rip output-delay 命令用来恢复缺省情况。
【命令】
rip output-delay time count count undo rip output-delay

【缺省情况】
RIP 报文的发包速率由进程全局的配置决定。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
time：接口发送 RIP 报文的时间间隔，取值范围为 10～100，单位为毫秒。
count：接口一次发送 报文的最大个数，取值范围为 1～30。
RIP【举例】
\# 在接口 Vlan-interface10 配置发送 RIP 报文的时间间隔为 30 毫秒，一次最多发送 6 个 RIP 报文。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] rip output-delay 30 count 6【相关命令】
• output-delay

##### 1.1.40 rip poison-reverse

rip poison-reverse 命令用来使能毒性逆转功能。
undo rip poison-reverse 命令用来关闭毒性逆转功能。
【命令】
rip poison-reverse undo rip poison-reverse【缺省情况】
毒性逆转功能处于关闭状态。
【视图】
接口视图【缺省用户角色】
network-admin【举例】
\# 在接口 Vlan-interface10 上配置对 RIP 更新报文进行毒性逆转。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] rip poison-reverse

##### 1.1.41 rip primary-path-detect bfd echo

rip primary-path-detect bfd echo 命令用来使能 RIP 协议中主用链路使能 BFD（Echo方式）检测功能。
命令用来关闭 RIP 协议中主用链路的 BFD（Echo 方式）
undo rip primary-path-detect bfd检测功能。
【命令】
rip primary-path-detect bfd echo undo rip primary-path-detect bfd【缺省情况】
RIP 协议中主用链路的 BFD Echo 检测功能处于关闭状态。
【视图】
接口视图【缺省用户角色】
network-admin【使用指导】
配置本功能后，RIP 协议的快速重路由特性中的主用链路将使用 BFD（Echo 方式）进行检测。
【举例】
\# 在接口 Vlan-interface10 上配置 RIP 协议快速重路由特性中主用链路使能 BFD（Echo 方式）检测功能。
<Sysname> system-view [Sysname] rip 1 [Sysname-rip-1] fast-reroute route-policy frr [Sysname-rip-1] quit [Sysname] bfd echo-source-ip 1.1.1.1 [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] rip primary-path-detect bfd echo

##### 1.1.42 rip split-horizon

命令用来使能水平分割功能。
rip split-horizon命令用来关闭水平分割功能。
undo rip split-horizon【命令】
rip split-horizon undo rip split-horizon【缺省情况】
水平分割功能处于使能状态。
【视图】
接口视图

【缺省用户角色】
network-admin【使用指导】
通常情况下，为了防止路由环路的出现，水平分割是必要的，因此，建议不要关闭水平分割。当因为特殊需要，如为保证协议的正确执行，需要关闭水平分割时，请一定要确认是否必要。
如果同时使能了水平分割和毒性逆转，则只有毒性逆转功能生效。
【举例】
\# 在接口 Vlan-interface10 上配置水平分割。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] rip split-horizon

##### 1.1.43 rip summary-address

命令用来配置一条聚合路由。
rip summary-address命令用来取消指定的聚合路由。
undo rip summary-address【命令】
rip summary-address ip-address { mask-length | mask } undo rip summary-address ip-address { mask-length | mask }【缺省情况】
未配置聚合路由。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
ip-address：聚合路由的目的 地址。
IP mask-length：聚合路由的网络掩码长度，取值范围为 0～32。
mask：聚合路由的网络掩码，点分十进制格式。
【使用指导】
该功能仅在自动路由聚合功能被关闭时才能生效。
【举例】
\# 在接口 Vlan-interface10 下配置一条聚合路由。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] rip summary-address 10.0.0.0 255.255.255.0【相关命令】
•summary

##### 1.1.44 rip version

rip version 命令用来配置接口运行的 RIP 版本。
undo rip version 命令用来恢复缺省情况。
【命令】
rip version { 1 | 2 [ broadcast | multicast ] } undo rip version【缺省情况】
未配置接口运行的 RIP 版本。接口只能发送 RIP-1 广播报文，可以接收 RIP-1 广播/单播报文、RIP-2广播/组播/单播报文。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
1：接口运行 RIP 协议的版本为 RIP-1。
2：接口运行 RIP 协议的版本为 RIP-2。
]：RIP-2 报文的发送方式为广播方式（broadcast）还是组播方[ broadcast | multicast式（multicast），缺省为组播方式（multicast）。
【使用指导】
如果接口上配置了 RIP 版本，以接口配置的为准；如果接口上没有配置 RIP 版本，接口运行的 RIP版本以全局配置的为准。
当接口运行的 RIP 版本为 RIP-1 时：
• 发送 RIP-1 广播报文
• 接收 RIP-1 广播/单播报文当接口运行在 RIP-2 广播方式时：
• 发送 RIP-2 广播报文
• 接收 RIP-1 广播/单播报文、RIP-2 广播/组播/单播报文当接口运行在 RIP-2 组播方式时：
发送 组播报文
• RIP-2接收 广播/组播/单播报文
• RIP-2【举例】
\# 配置接口 Vlan-interface10 以广播方式发送 RIP-2 报文。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] rip version 2 broadcast【相关命令】
• version

##### 1.1.45 silent-interface

silent-interface 命令用来配置接口工作在抑制状态，即接口只接收 RIP 报文而不发送 RIP 报文。
命令用来取消接口的抑制状态。
undo silent-interface【命令】
silent-interface { interface-type interface-number | all } undo silent-interface { interface-type interface-number | all }【缺省情况】
允许所有接口发送 报文。
RIP【视图】
RIP 视图【缺省用户角色】
network-admin【参数】
interface-number：接口类型和编号。
interface-type all：抑制所有接口。
【举例】
将所有接口设置为抑制状态，随后激活指定接口 Vlan-interface10。
\# <Sysname> system-view [Sysname] rip 100 [Sysname-rip-100] silent-interface all [Sysname-rip-100] undo silent-interface vlan-interface 10 [Sysname-rip-100] network 131.108.0.0

##### 1.1.46 summary

summary 命令用来使能 RIP-2 自动路由聚合功能，聚合后的路由以使用自然掩码的路由形式发布，减小了路由表的规模。
undo summary 命令用来关闭 RIP-2 自动路由聚合功能，以便将所有子网路由广播出去。
【命令】
summary undo summary【缺省情况】
RIP-2 自动路由聚合功能处于使能状态。
【视图】
视图RIP【缺省用户角色】
network-admin

【使用指导】
使能 RIP-2 自动路由聚合功能可以减小路由表规模，提高大型网络的可扩展性和效率。
【举例】
\# 关闭 RIP-2 自动路由聚合功能。
<Sysname> system-view [Sysname] rip [Sysname-rip-1] undo summary【相关命令】
• rip summary-address
• rip version

##### 1.1.47 timer triggered

命令用来配置触发更新的时间间隔。
timer triggered命令用来恢复缺省情况。
undo timer triggered【命令】
timer triggered maximum-interval [ minimum-interval [ incremental-interval ] ] undo timer triggered【缺省情况】
发送触发更新的最大时间间隔为 5 秒，最小间隔为 50 毫秒，增量惩罚间隔为 200 毫秒。
【视图】
RIP 视图【缺省用户角色】
network-admin【参数】
maximum-interval：触发更新的最大间隔时间。取值范围为 1～5，单位为秒。
minimum-interval：触发更新的最小间隔时间。取值范围为 10～5000，单位为毫秒。
incremental-interval：触发更新间隔的增加时间。取值范围为 100～1000，单位为毫秒。
【使用指导】
本命令在网络变化不频繁的情况下将触发更新的时间间隔缩小到 minimum-interval，而在网络变化频繁的情况下可以进行相应惩罚，将时间间隔按照配置的惩罚增量延长，最大不超过maximum-interval。
和 配置值不允许大于 配minimum-interval incremental-interval maximum-interval置值。
【举例】
\# 配置发送触发更新的最大时间间隔为 2 秒，最小时间间隔为 100 毫秒，惩罚增量为 100 毫秒。
<Sysname> system-view

[Sysname] rip 1 [Sysname-rip-1] timer triggered 2 100 100

##### 1.1.48 timers

命令用来配置 定时器的值，可通过调节 定时器来调整路由协议的性能，以满足网timers RIP RIP络需要。
undo timers 命令用来恢复 RIP 定时器的缺省值。
【命令】
timers { garbage-collect garbage-collect-value | suppress suppress-value | timeout timeout-value | update update-value } * undo timers { garbage-collect | suppress | timeout | update } *【缺省情况】
定时器的值为 秒，Suppress 定时器的值为 秒，Timeout 定时器的值为Garbage-collect 120 120 180秒，Update 定时器的值为 30 秒。
【视图】
RIP 视图【缺省用户角色】
network-admin【参数】
garbage-collect-value：Garbage-collect 定时器的值，取值范围为 1～3600，单位为秒。
suppress-value：Suppress 定时器的值，取值范围为 0～3600，单位为秒。
timeout-value：Timeout 定时器的值，取值范围为 1～3600，单位为秒。
update-value：Update 定时器的值，取值范围为 1～3600，单位为秒。
【使用指导】
受四个定时器的控制，分别是 Update、Timeout、Suppress 和 Garbage-Collect，其中：
RIP定时器，定义了发送更新报文的时间间隔。
• Update定时器，定义了路由老化时间。如果在老化时间内没有收到关于某条路由的更新报文，
• Timeout则该条路由在路由表中的度量值将会被设置为 16。
• Suppress 定时器，定义了 RIP 路由处于抑制状态的时间段长度。当一条路由的度量值变为 16时，该路由将进入被抑制状态。在被抑制状态，只有来自同一邻居，且度量值小于 16 的路由更新才会被路由器接收，取代不可达路由。
Garbage-Collect 定时器，定义了一条路由从度量值变为 16 开始，直到它从路由表里被删除
•所经过的时间。在 时间内，RIP 以 作为度量值向外发送这条路由的更新，Garbage-Collect 16如果 Garbage-Collect 超时，该路由仍没有得到更新，则该路由将从路由表中被彻底删除。
通常情况下，无需改变各定时器的缺省值，该命令须谨慎使用。
各个定时器的值在网络中所有的路由器上必须保持一致。
Timeout 定时器的值要大于 Update 定时器的值。

【举例】
\# 分别设置 RIP 各定时器的值：其中，Update 定时器的值为 5 秒、Timeout 定时器的值为 15 秒、Suppress 定时器的值为 15 秒、Garbage-Collect 定时器的值为 30 秒。
<Sysname> system-view [Sysname] rip 100 [Sysname-rip-100] timers update 5 timeout 15 suppress 15 garbage-collect 30

##### 1.1.49 validate-source-address

命令用来使能对接收到的 RIP 路由更新报文进行源 IP 地址检查的validate-source-address功能。
命令用来关闭对接收到的 RIP 路由更新报文进行源 IP 地址undo validate-source-address检查的功能。
【命令】
validate-source-address undo validate-source-address【缺省情况】
对接收到的 RIP 路由更新报文进行源 IP 地址检查的功能处于使能状态。
【视图】
RIP 视图【缺省用户角色】
network-admin【举例】
\# 关闭对接收到的 RIP 路由更新报文进行源 IP 地址检查的功能。
<Sysname> system-view [Sysname-rip] rip 100 [Sysname-rip-100] undo validate-source-address

##### 1.1.50 version

命令用来配置全局 版本。
version RIP命令用来恢复缺省情况。
undo version【命令】
version { 1 | 2 } undo version【缺省情况】
未配置全局 RIP 版本。接口只能发送 RIP-1 广播报文，可以接收 RIP-1 广播 / 单播报文、 RIP-2 广播/组播/单播报文。
【视图】
视图RIP

【缺省用户角色】
network-admin【参数】
1：指定为 RIP-1 版本。
2：指定为 RIP-2 版本，RIP-2 报文的发送方式为组播方式。
【使用指导】
配置全局 RIP 版本时，其生效规则如下：
如果接口上配置了 RIP 版本，以接口配置的为准。
•如果接口没有配置 RIP 版本，将全局 RIP 版本配置为 1 时，接口运行的 RIP 版本为 RIP-1，
•发送 广播报文，可以接收 广播/单播报文。
RIP-1 RIP-1如果接口没有配置 版本，将全局 版本配置为 时，接口运行的 版本为 且
• RIP RIP 2 RIP RIP-2工作在组播方式，发送 RIP-2 组播报文，可以接收 RIP-2 广播/组播/单播。
【举例】
\# 指定全局 RIP 版本为 RIP-2。
<Sysname> system-view [Sysname] rip 100 [Sysname-rip-100] version 2【相关命令】
•rip version

## 04-OSPF命令

目 录配置命令

1

### OSPF

#### 1.1 OSPF配置命令

##### 1.1.1 abr-summary (OSPF area view)

命令用来配置 ABR 路由聚合。
abr-summary命令用来取消 ABR 对指定网段的路由聚合。
undo abr-summary【命令】
abr-summary ip-address { mask-length | mask } [ advertise | not-advertise ] [ cost cost-value ] undo abr-summary ip-address { mask-length | mask }【缺省情况】
ABR 不对路由进行聚合。
【视图】
OSPF 区域视图【缺省用户角色】
network-admin【参数】
ip-address：聚合路由的目的 地址。
IP mask-length：聚合路由的网络掩码长度，取值范围为 0～32。
mask：聚合路由的网络掩码，点分十进制形式。
not-advertise：是否发布这条聚合路由。缺省时发布聚合路由。
advertise | cost-value：聚合路由的开销值，取值范围为 1～16777215，缺省值为所有被聚合的路由cost中最大的开销值。
【使用指导】
本命令只适用于区域边界路由器（ABR），用来对某一个区域内的路由信息进行聚合。对于属于该聚合网段范围的路由，ABR 向其它区域只发送一条聚合后的路由。一个区域可配置多条聚合网段，这样 可对多个网段进行聚合。
OSPF当配置了 命令后，原来被聚合的路由又重新被发布。
undo abr-summary【举例】
将 区域 中两个网段 和 的路由聚合成一条聚合路由\# OSPF 1 36.42.10.0/24 36.42.110.0/24
36.42.0.0/16 向其它区域发布。
<Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] area 1 [Sysname-ospf-100-area-0.0.0.1] network 36.42.10.0 0.0.0.255 [Sysname-ospf-100-area-0.0.0.1] network 36.42.110.0 0.0.0.255

[Sysname-ospf-100-area-0.0.0.1] abr-summary 36.42.0.0 255.255.0.0

##### 1.1.2 area (OSPF view)

area 命令用来创建 OSPF 区域，并进入 OSPF 区域视图。
undo area 命令用来删除指定的 OSPF 区域。
【命令】
area area-id undo area area-id【缺省情况】
不存在 OSPF 区域。
【视图】
视图OSPF【缺省用户角色】
network-admin【参数】
area-id：区域的标识，可以是十进制整数（取值范围为 0～4294967295，系统会将其转换成 IP地址格式）或者是 IP 地址格式。
【举例】
创建 区域 并进入 区域视图。
\# OSPF 0 OSPF <Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] area 0 [Sysname-ospf-100-area-0.0.0.0]

##### 1.1.3 asbr-summary (OSPF view)

asbr-summary 命令用来配置 ASBR 路由聚合。
undo asbr-summary 命令用来取消 ASBR 对指定网段的路由聚合。
【命令】
asbr-summary ip-address { mask-length | mask } [ cost cost-value | not-advertise | nssa-only | tag tag ] * undo asbr-summary ip-address { mask-length | mask }【缺省情况】
ASBR 不对路由进行聚合。
【视图】
OSPF 视图【缺省用户角色】
network-admin

【参数】
ip-address：聚合路由的目的 IP 地址。
mask-length：聚合路由的网络掩码长度，取值范围为 0～32。
mask：聚合路由的网络掩码，点分十进制格式。
cost cost-value：聚合路由的开销值，取值范围为 1～16777214。如果未指定本参数，取所有被聚合的路由中最大的开销值作为聚合路由的开销值；如果是 Type-7 LSA 转cost-value化成的 Type-5 LSA 描述的路由匹配聚合、且是 Type2 外部路由，则 取所有被聚合cost-value的路由中最大的开销值加 1 作为聚合路由的开销值。
not-advertise：不通告聚合路由。如果未指定本参数，将通告聚合路由。
nssa-only：设置 的 比特位为不置位，即在对端路由器上不能转为 LSA。
Type-7 LSA P Type-5缺省时，Type-7 LSA 的 P 比特位被置位，即在对端路由器上可以转为 Type-5 LSA（如果本地路由器是 ABR，则会检查骨干区域是否存在 FULL 状态的邻居，当 FULL 状态的邻居存在时，产生的中 比特位不置位）。
Type-7 LSA P tag：聚合路由的标识，可以通过路由策略控制聚合路由的发布，取值范围为 0～4294967295，tag缺省值为 1。
【使用指导】
如果本地路由器是 ASBR，对引入的聚合地址范围内的 Type-5 LSA 描述的路由进行聚合；当配置了 NSSA 区域时，对引入的聚合地址范围内的 Type-7 LSA 描述的路由进行聚合。
如果本地路由器同时是 ASBR 和 ABR，并且是 NSSA 区域的转换路由器，将对由 Type-7 LSA 转化成的 进行聚合处理；如果不是 区域的转换路由器，则不进行聚合处理。
Type-5 LSA NSSA配置 命令后，对处于聚合地址范围内的外部路由，本地路由器只向邻居路由器发asbr-summary布一条聚合后的路由；配置 命令后，原来被聚合的外部路由将重新被发布。
undo asbr-summary【举例】
\# 配置 OSPF 对引入的路由进行聚合，聚合路由的标识为 2，开销值为 100。
<Sysname> system-view [Sysname] ip route-static 10.2.1.0 24 null 0 [Sysname] ip route-static 10.2.2.0 24 null 0 [Sysname] ospf 100 [Sysname-ospf-100] import-route static [Sysname-ospf-100] asbr-summary 10.2.0.0 255.255.0.0 tag 2 cost 100

##### 1.1.4 authentication-mode

authentication-mode 命令用来配置 OSPF 区域所使用的验证模式。
undo authentication-mode 命令用来取消 OSPF 区域所使用的验证模式。
【命令】
MD5/HMAC-MD5 验证模式：
authentication-mode { hmac-md5 | md5 } key-id { cipher | plain } string undo authentication-mode [ { hmac-md5 | md5 } key-id ]简单验证模式：
authentication-mode simple { cipher | plain } string

undo authentication-mode keychain 验证模式：
authentication-mode keychain keychain-name undo authentication-mode【缺省情况】
未配置区域验证模式。
【视图】
OSPF 区域视图【缺省用户角色】
network-admin【参数】
hmac-md5：HMAC-MD5 验证模式。
md5 ： MD5 验证模式。
simple：简单验证模式。
key-id：验证字标识符，取值范围为 0～255。
cipher：以密文方式设置密钥。
plain：以明文方式设置密钥，该密钥将以密文形式存储。
string：密钥字符串，区分大小写。简单验证模式下，明文密钥为 1～8 个字符的字符串；密文密钥为 33～41 个字符的字符串。MD5/HMAC-MD5 验证模式下，明文密钥为 1～16 个字符的字符串；
密文密钥为 33～53 个字符的字符串。
keychain：使用 keychain 验证方式。
keychain-name：keychain 名称，为 1～63 个字符的字符串，区分大小写。
【使用指导】
一个区域中所有路由器的验证模式和验证密码必须一致。
可指定区域下使用 验证或简单验证两种方式，但不能同时指定；使用OSPF MD5/HMAC-MD5 MD5/HMAC-MD5 验证方式时，可配置多条 MD5/HMAC-MD5 验证命令，但 key-id 是唯一的，同一 key-id 只能配置一个验证字。
修改 OSPF 区域的 MD5/HMAC-MD5 验证字的步骤如下：
• 首先在该区域配置新的 MD5/HMAC-MD5 验证字；此时若邻居设备尚未配置新的MD5/HMAC-MD5 验证字，便会触发 MD5/HMAC-MD5 验证平滑迁移过程。在这个过程中，会发送分别携带各个 验证字的多份报文，使得已配置新验证字的邻OSPF MD5/HMAC-MD5居设备和尚未配置新验证字的邻居设备都能通过验证，保持邻居关系。
• 然后在各个邻居设备上也都配置相同的新 MD5/HMAC-MD5 验证字；当本设备上收到所有邻居的携带新验证字的报文后，便会退出 MD5/HMAC-MD5 验证平滑迁移过程。
• 最后在本设备和所有邻居上都删除旧的 MD5/HMAC-MD5 验证字；建议区域下不要保留多个MD5/HMAC-MD5 验证字，每次 MD5/HMAC-MD5 验证字修改完毕后，应当及时删除旧的验证字，这样可以防止与持有旧验证字的系统继续通信、减少被攻击的可能，还可以减少验证迁移过程对系统、带宽的消耗。

在 OSPF 区域使用 keychain 验证方式时，报文的收、发过程如下：
OSPF 在发送报文前，会先从 keychain 获取当前的有效发送 key，根据该 key 的标识符、认
•证算法和认证密钥进行报文验证，如果当前不存在有效发送 key，或者该 的标识符大于key 255，OSPF 不会发送报文。
• OSPF 在收到报文后，会根据报文携带的 key 的标识符从 keychain 中获取有效接收 key，根据该 key 的认证算法和认证密钥对报文进行校验。如果报文校验失败，或者根据报文中携带的 的标识符无法从 中获取到有效接收 key，则该报文将被丢弃。
key keychain对于 keychain 认证算法和 key 的标识符的范围，OSPF 的支持情况如下：
OSPF 仅支持 MD-5、HMAC-MD5 和 HMAC-SM3 认证算法。
•
• OSPF 仅支持标识符取值范围为 0～255 的 key。
【举例】
配置 区域 使用 明文验证模式，验证字标识符为 15，验证密钥为 abc。
\# OSPF 0 MD5 <Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] area 0 [Sysname-ospf-100-area-0.0.0.0] authentication-mode md5 15 plain abc【相关命令】
• ospf authentication-mode

##### 1.1.5 bandwidth-reference (OSPF view)

命令用来配置计算链路开销时所依据的带宽参考值。
bandwidth-reference命令用来恢复缺省情况。
undo bandwidth-reference【命令】
bandwidth-reference value undo bandwidth-reference【缺省情况】
计算链路开销时所依据的带宽参考值为 100Mbps。
【视图】
OSPF 视图【缺省用户角色】
network-admin【参数】
value：计算链路开销时所依据的带宽参考值，取值范围为 1～4294967，单位为 Mbps。
【使用指导】
如果没有配置链路的开销值，OSPF 根据链路带宽来计算开销值，接口开销＝带宽参考值÷接口期望带宽（接口期望带宽通过命令 bandwidth 进行配置，具体情况请参见接口分册命令参考中的介绍）。当计算出来的开销值大于 65535 时，开销取最大值 65535；当计算出来的开销值小于 1 时，开销取最小值 1。

【举例】
\# 配置链路的带宽参考值为 1000Mbps。
<Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] bandwidth-reference 1000【相关命令】
•ospf cost

##### 1.1.6 capability default-exclusion

capability default-exclusion 命令用来配置允许将区域下的接口从标准拓扑中分离。
undo capability default-exclusion 命令用来恢复缺省情况。
【命令】
capability default-exclusion undo capability default-exclusion【缺省情况】
区域下的接口自动加入标准拓扑 base。
OSPF【视图】
OSPF 区域视图【缺省用户角色】
network-admin【使用指导】
缺省情况下，OSPF 区域下的接口会自动加入标准拓扑。本命令允许区域下的接口从标准拓扑中分离出来。
需要在本设备和邻居设备上同时配置本命令，否则会影响邻居关系的建立。
【举例】
允许 区域 下的接口从标准拓扑中分离。
\# OSPF 1 <Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] area 1 [Sysname-ospf-area-1] capability default-exclusion

##### 1.1.7 database-filter peer (OSPF view)

命令用来对发送给指定邻居的 LSA 进行过滤。
database-filter peer命令用来恢复缺省情况。
undo database-filter peer【命令】
database-filter peer ip-address { all | { ase [ acl ipv4-acl-number ] | nssa [ acl ipv4-acl-number ] | summary [ acl ipv4-acl-number ] } * } undo database-filter peer ip-address

【缺省情况】
不对发送给指定邻居的 LSA 进行过滤。
【视图】
OSPF 视图【缺省用户角色】
network-admin【参数】
ip-address：接口的网络类型为 P2MP 的邻居的 IP 地址。
all：对发送给接口的网络类型为 的邻居的所有 进行过滤（除了 LSA）。
P2MP LSA Grace ase：对发送给接口的网络类型为 的邻居的 进行过滤。
P2MP Type-5 LSA nssa：对发送给接口的网络类型为 的邻居的 进行过滤。
P2MP Type-7 LSA summary：对发送给接口的网络类型为 的邻居的 进行过滤。
P2MP Type-3 LSA ipv4-acl-number：指定的基本或高级 IPv4 ACL 编号，取值范围为 2000～3999。
acl【使用指导】
当两台路由器之间存在多条 P2MP 链路时，路由器上会存在多个接口的网络类型为 P2MP 的 OSPF邻居。不愿让某个指定邻居收到的 LSA，通过该功能可在本地将其过滤掉。
当配置的是高级 ACL（3000～3999）时，其使用规则如下：
• 使用命令 rule [ rule-id ] { deny | permit } ip source sour-addr来过滤携带指定链路状态 ID 的 LSA。
sour-wildcard
• 使用命令 rule [ rule-id ] { deny | permit } ip source sour-addr来过滤携带指定链路状态sour-wildcard destination dest-addr dest-wildcard和掩码的 LSA。
ID其中，source 用来过滤 的链路状态 ID，destination 用来过滤 的掩码，配置的掩码LSA LSA应该是连续的（当配置的掩码不连续时该过滤掩码的规则不生效）。
如果在配置该命令前邻居路由器就已经收到了将要进行过滤的 LSA，那么配置该命令后，这些 LSA仍存在于邻居路由器的 LSDB 中。
【举例】
\# 配置对发送给接口的网络类型为 P2MP 的邻居的所有 LSA 进行过滤。
<Sysname> system-view [Sysname] ospf 1 [Sysname-ospf-1] database-filter peer 121.20.20.121 all \# 配置编号为 3000 的高级 ACL 对发送给邻居 121.20.20.121 的 Type-3 LSA 进行过滤。
<Sysname> system-view [Sysname] acl advanced 3000 [Sysname-acl-ipv4-adv-3000]rule 10 deny ip source 121.20.0.0 0 destination 255.255.0.0 0 [Sysname-acl-ipv4-adv-3000] rule 100 permit ip [Sysname-acl-ipv4-adv-3000] quit [Sysname] ospf 1 [Sysname-ospf-1] database-filter peer 121.20.20.121 summary acl 3000

【相关命令】
• ospf database-filter

##### 1.1.8 default (OSPF view)

default 命令用来配置引入外部路由时的缺省参数，包括 OSPF 引入外部路由的开销、类型和标记。
undo default 命令用来取消引入外部路由时的缺省参数的配置。
【命令】
default { cost cost-value | tag tag | type type } * undo default { cost | tag | type } *【缺省情况】
引入的外部路由的度量值为 1，引入的外部路由的标记为 1，引入的外部路由类型为 2。
OSPF【视图】
OSPF 视图【缺省用户角色】
network-admin【参数】
cost-value：OSPF 引入的外部路由的缺省度量值，cost-value 的取值范围为 0～cost 16777214。
tag：外部路由的标记，tag 的取值范围为 0～4294967295。
tag type：外部路由类型，type 的取值范围为 1～2。
type【举例】
配置外部路由开销、标记和类型的缺省值分别为 10、100 和 2。
\# <Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] default cost 10 tag 100 type 2【相关命令】
• import-route

##### 1.1.9 default-cost (OSPF area view)

default-cost 命令用来配置发送到 Stub 区域或 NSSA 区域的缺省路由的开销。
undo default-cost 命令用来恢复缺省情况。
【命令】
default-cost cost-value undo default-cost【缺省情况】
发送到 Stub 区域或 NSSA 区域的缺省路由的开销为 1。

【视图】
OSPF 区域视图【缺省用户角色】
network-admin【参数】
cost-value：发送到 区域或 区域的缺省路由的开销值，取值范围为 0～16777214。
Stub NSSA【使用指导】
该命令只有在 Stub 区域的 ABR 或 NSSA 区域的 ABR/ASBR 上配置才能生效。
【举例】
\# 将区域 1 设置成 Stub 区域，配置发送到该 Stub 区域的缺省路由的开销为 20。
<Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] area 1 [Sysname-ospf-100-area-0.0.0.1] stub [Sysname-ospf-100-area-0.0.0.1] default-cost 20【相关命令】
• nssa
• stub

##### 1.1.10 default-route-advertise (OSPF view)

命令用来将缺省路由引入到 OSPF 路由区域。
default-route-advertise命令用来恢复缺省情况。
undo default-route-advertise【命令】
default-route-advertise [ [ always | permit-calculate-other ] | cost cost-value | route-policy route-policy-name | type type ] * default-route-advertise [ summary cost cost-value ] undo default-route-advertise【缺省情况】
未引入缺省路由。
【视图】
OSPF 视图【缺省用户角色】
network-admin【参数】
always：如果当前路由器的路由表中没有缺省路由，使用此参数可产生一个描述缺省路由的Type-5 LSA 发布出去。如果没有指定该关键字，仅当本地路由器的路由表中存在缺省路由时，才可以产生一个描述缺省路由的 Type-5 LSA 发布出去。

permit-calculate-other：当路由器产生并发布了一个描述缺省路由的 Type-5 LSA 时，指定此参数的路由器仍然会计算来自于其他路由器的缺省路由，未指定此参数的路由器不再计算来自其他路由器的缺省路由。当路由器没有产生一个描述缺省路由的 Type-5 LSA 时，无论是否指定此参数，路由器都会计算来自其他路由器的缺省路由。
cost-value：该缺省路由的度量值，取值范围为 0～16777214，如果没有指定，缺省路由cost的度量值将取 命令配置的值。
default cost route-policy-name：路由策略名，为 1～63 个字符的字符串，区分大小写。
route-policy只有当前路由器的路由表中存在缺省路由，并且有路由匹配 route-policy-name 指定的路由策略，才可以产生一个描述缺省路由的 Type-5 LSA 发布出去，指定的路由策略会影响 Type-5 LSA中的值。如果同时指定 参数，不论当前路由器的路由表中是否有缺省路由，只要有路由匹always配指定的路由策略，就将产生一个描述缺省路由的 发布出去，指定的路由策略会影响Type-5 LSA Type-5 LSA 中的值。
type type：该 Type-5 LSA 的类型，取值范围为 1～2，如果没有指定，Type-5 LSA 的缺省类型将取 default type 命令配置的值。
summary ：发布指定缺省路由的 Type-3 LSA。在选用该参数时，必须首先使能 VPN，否则路由不能发布。
【使用指导】
使用 命令不能引入缺省路由，如果要引入缺省路由，必须使用该命令。当本地路import-route由器的路由表中没有缺省路由时，要产生一个描述缺省路由的 Type-5 LSA 应使用 always 关键字。
default-route-advertise summary cost 命令仅在 VPN 中应用，以 Type-3 LSA 引入缺省路由，PE 路由器会将引入的缺省路由发布给 CE 路由器。
【举例】
\# 不管本地路由器的路由表中是否存在缺省路由，将产生的缺省路由引入到 OSPF 路由区域（本地路由器没有缺省路由）。
<Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] default-route-advertise always【相关命令】
• default
• import-route

##### 1.1.11 description (OSPF/OSPF area view)

命令用来配置 进程/OSPF 区域的描述信息。
description OSPF命令用来恢复缺省情况。
undo description【命令】
description text undo description【缺省情况】
未配置 OSPF 进程和区域的描述信息。

【视图】
OSPF 视图OSPF 区域视图【缺省用户角色】
network-admin【参数】
text：在 OSPF 视图下，该参数用来描述 OSPF 进程；在 OSPF 区域视图下，该参数用来描述OSPF 区域，为 1～80 个字符的字符串，区分大小写。
【使用指导】
本命令仅仅用于标识某 OSPF 进程/OSPF 区域，并无特别的意义和用途。
【举例】
\# 配置 OSPF 进程 100 的描述信息为“abc”。
<Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] description abc \# 配置 OSPF 区域 0 的描述信息为“bone area”。
<Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] area 0 [Sysname-ospf-100-area-0.0.0.0] description bone area

##### 1.1.12 discard-route

命令用来配置 路由以及 路由的优先级。
discard-route NULL0 NULL0命令用来将 路由的优先级恢复为 255。
undo discard-route NULL0【命令】
discard-route { external { preference | suppression } | internal { preference | suppression } } * undo discard-route [ external | internal ] *【缺省情况】
产生引入聚合 NULL0 路由和区域间聚合 NULL0 路由，且 NULL0 路由优先级为 255。
【视图】
视图OSPF【缺省用户角色】
network-admin【参数】
external：引入聚合 NULL0 路由。
preference：引入聚合 NULL0 路由的优先级，取值范围为 1～255。
suppression ：抑制产生引入聚合 NULL0 路由。

internal：区域间聚合 NULL0 路由。
preference：区域间聚合 NULL0 路由的优先级，取值范围为 1～255。
suppression：抑制产生区域间聚合 NULL0 路由。
【举例】
配置引入聚合路由的 路由的优先级为 100，区域间聚合 路由的优先级为 200。
\# NULL0 NULL0 <Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] discard-route external 100 internal 200

##### 1.1.13 display ospf

命令用来显示 OSPF 的进程信息。
display ospf【命令】
display ospf [ process-id ] [ verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 OSPF 的进程信息。
verbose：显示 进程的详细信息。如果未指定本参数，将显示 进程的概要信息。
OSPF OSPF【举例】
\# 显示 OSPF 的详细信息。
<Sysname> display ospf verbose OSPF Process 1 with Router ID 192.168.1.2 OSPF Protocol Information RouterID: 192.168.1.2 Router type: NSSA Route tag: 0 Multi-VPN-Instance is not enabled Ext-community type: domain ID 0x105, route type 0x8000, router ID 0x8001 Domain ID: 0.0.0.0:23 Opaque capable Originating router-LSAs with maximum metric Condition: On startup for 600 seconds, State: Inactive Advertise stub links with maximum metric in router-LSAs Advertise summary-LSAs with metric 16711680 Advertise external-LSAs with metric 16711680 ISPF is enabled

SPF-schedule-interval: 5 50 200 LSA generation interval: 5 LSA arrival interval: 1000 Transmit pacing: Interval: 20 Count: 3 Default ASE parameters: Metric: 1 Tag: 1 Type: 2 Route preference: 10 ASE route preference: 150 SPF computation count: 22 RFC 1583 compatible Graceful restart interval: 120 SNMP trap rate limit interval: 2 Count: 300 This process is currently bound to MIB Area count: 1 NSSA area count: 1 Normal areas with up interfaces: 0 NSSA areas with up interfaces: 1 Up interfaces: 1 ExChange/Loading neighbors: 0 Full neighbors:3 Area0 full neighbors: 1 Calculation trigger type: Full Current calculation type: SPF calculation Current calculation phase: Calculation area topology Process reset state: N/A Current reset type: N/A Next reset type: N/A Reset prepare message replied: -/-/-/- Reset process message replied: -/-/-/- module：
Reset phase of M-N/A, P-N/A, L-N/A, C-N/A, R-N/A Area: 0.0.0.1 (MPLS TE not enabled)
Authtype: None Area flag: NSSA 7/5 translator state: Disabled 7/5 translate stability timer interval: 0 SPF scheduled count: 5 ExChange/Loading neighbors: 0 Up interfaces: 1 Interface: 192.168.1.2 (Vlan-interface10)
Cost: 1 State: DR Type: Broadcast MTU: 1500 Priority: 1 Designated router: 192.168.1.2 Backup designated router: 192.168.1.1 Timers: Hello 10 , Dead 40 , Poll 40 , Retransmit 5 , Transmit Delay 1 FRR backup: Enabled Enabled by network configuration Packet size: 1000

表1-1 display ospf verbose 命令显示信息描述表字段 描述OSPF Process 1 with Router ID 192.168.1.2 OSPF进程号以及OSPF Router ID本路由器的Router RouterID ID路由器类型，取值为：
• ABR：表示区域边界路由器Router type • ASBR：表示自治系统边界路由器
• NSSA：表示支持 NSSA 区域
• 为空：表示非上面三种情况Route tag 与外部路由相关联的标记Multi-VPN-Instance is not enabled 当前进程不支持多VPN实例OSPF扩展团体属性类型编码。其中：
• domain ID：表示 domain ID 属性编码Ext-community type
•route type：表示 route type 属性编码
• router ID：表示 router ID 属性编码Domain ID OSPF域标识符（主标识符）
Opaque capable 使能OSPF的Opaque LSA发布接收能力Originating router-LSAs with maximum metric Router LSA中除Stublink外使用最大开销值发布Stub路由器的状态：
•Always：表示始终生效
• On startup while BGP is converging：表示 BGP 收敛Condition 前生效
•On startup while BGP is converging for XXX seconds：表示 BGP 收敛超时时间
• On startup for XXX seconds：表示重启后生效时间Stub路由器是否生效：
State • Active 表示生效
• Inactive 表示不生效Advertise stub links with maximum metric in Router LSA使用最大开销值发布router-LSAs Advertise summary-LSAs with metric Summary LSA发布使用的开销值Advertise external-LSAs with metric 外部LSA发布使用的开销值使能增量SPF计算功能ISPF is enabled SPF-schedule-interval 进行SPF计算的时间间隔LSA generation interval LSA 生成时间间隔LSA arrival interval LSA重复到达的最小时间间隔接口发送LSU报文的速率，其中：
Transmit pacing

字段 描述
• Interval 表示接口发送 LSU 报文的时间间隔
•Count 表示接口一次发送 LSU 报文的最大个数引入外部路由的缺省参数值，其中：
• Metric：表示度量值Default ASE parameters
• Tag：表示路由标记
• Type：表示路由类型Route preference OSPF协议对自治系统内部路由的优先级OSPF协议对自治系统外部路由的优先级ASE route preference SPF computation count OSPF进程的路由计算总数RFC1583 compatible 兼容RFC 1583路由选择优先规则Graceful restart interval GR重启间隔时间SNMP trap rate limit interval TRAP 发送间隔Count TRAP发送个数This process is currently bound to MIB 当前进程绑定MIB当前进程中的区域数Area count NSSA area count 当前进程中的NSSA区域数Normal areas with up interfaces 有Up接口的外部能力区域个数NSSA areas with up interfaces 有Up接口的NSSA区域个数处于Up状态的接口计数Up interfaces ExChange/Loading neighbors 处于ExChange/Loading状态的邻居数Full neighbors 处于Full状态的邻居数骨干区域中处于Full状态的邻居数Area0 full neighbors触发路由计算的类型，具体如下：
• Full：触发全部路由计算
• ：区域拓扑改变触发路由计算Area topology change
• Intra router change：增量的区域内路由器路由变化
• change：增量的 路由变化ASBR ASBR
• 7to5 translator：7 转 5 角色变化Calculation trigger type
•Full IP prefix：触发全部 IP 前缀计算
• Full intra AS：触发全部 AS 内部前缀计算
• Inc intra AS：触发增量 AS 内部前缀计算
• Full inter AS：触发全部 AS 外部前缀计算
• Inc inter AS：触发增量 AS 外部前缀计算
• N/A：未触发计算Current calculation type 当前路由计算的类型，具体如下：

字段 描述
• SPF calculation：进行区域 SPF 计算
•Intra router calculation：区域内路由器路由计算
• ASBR calculation：区域间 ASBR 路由计算
• Inc intra router：增量区域内路由器路由计算
• Inc ASBR calculation：增量区域间 ASBR 路由计算
• 7to5 translator：7 转 5 角色路由计算
• Full intra AS：进行全部 AS 内部前缀计算
• Inc intra AS：进行增量 AS 内部前缀计算
• AS：进行全部 外部前缀计算Full inter AS
• Inc inter AS：进行增量 AS 外部前缀计算
• address：转发地址计算Forward
• N/A：未触发计算当前路由计算调度运行到的阶段，具体如下：
• topology：计算区域拓扑Calculation area
• Calculation router：计算路由器路由
• AS：计算 内部路由Calculation intra AS Current calculation phase • 7to5 translator：计算 7 转 5 角色路由
•Forward address：计算转发地址
• Calculation inter AS：计算 AS 外部路由
• Calculation end：计算收尾阶段
• N/A：未触发计算进程重启状态，具体如下：
• N/A：进程未重启Process reset state
• Under reset：进程重启过程中
• Under RIB smooth：进程正在同步 RIB 路由当前进程重启类型，具体如下：
• N/A：进程未重启
• ：普通重启Normal Current reset type
• GR quit：GR 异常退出进行普通重启
• Delete：删除 进程OSPF
• VPN delete：删除 VPN即将调度进程重启类型，具体如下：
• N/A：进程未重启Next reset type • Normal：普通重启
• quit：GR 异常退出进行普通重启GR
• Delete：删除 OSPF 进程响应准备重启消息的模块，具体如下：
Reset prepare message replied
• P：表示邻居维护模块

字段 描述
• L：表示 LSDB 同步模块
•C：表示路由计算模块
• R：表示路由引入模块响应进程重启消息的模块，具体如下：
• P：表示邻居维护模块Reset process message replied • L：表示 LSDB 同步模块
• C：表示路由计算模块
• R：表示路由引入模块各模块所处重启阶段。其中M代表主控制模块，其阶段有：
• N/A：未重启
• Delete area：删除区域
• process：删除进程Delete P 代表邻居维护模块，其阶段有：
• N/A：未重启
• Delete neighbor：删除邻居
• Delete interface：删除接口
• Delete vlink：删除虚连接L代表LSDB同步模块，其阶段有：
• N/A：未重启
• Stop timer：停止计时器
• Delete ASE：删除所有 ASE LSA
• Delete ASE maps：删除 ASE LSA 的 map
• Clear process data：清除进程数据
• LSA：删除区域相关 及其Reset phase of module Delete area LSA map
• Delete area interface：删除区域下接口
• process：删除进程相关资源Delete
• Restart：重启进程相关资源C代表路由计算模块，其阶段有：
• N/A：未重启
• topology：删除区域拓扑Delete
• Delete router：删除路由器路由
• AS：删除 内部路由Delete intra AS
• Delete inter AS：删除 AS 外部路由
•Delete forward address：删除转发地址列表
• Delete advertise：删除发布源列表代表路由引入模块，其阶段有：
R
• N/A：未重启
• summary：删除 聚合路由Delete ABR ABR
• Delete ASBR summary：删除 ASBR 聚合路由

字段 描述
• Delete import：删除引入路由列举当前进程中各区域的信息。显示当前区域ID，IP地址格Area式是否开启OSPF区域的MPLS TE能力MPLS TE not enabled • MPLS TE not enabled：表示关闭
• enabled：表示开启MPLS TE区域验证模式，取值为：
• None：表示无验证Authtype • Simple：表示简单验证模式
• MD5：表示 MD5 验证模式
• Keychain：表示 验证模式Keychain区域类型：
• Normal ：普通区域
• Stub：Stub 区域Area flag
• StubNoSummary：完全 Stub 区域
• NSSA：NSSA 区域
• NSSANoSummary：完全 NSSA 区域Type-7 LSA转换为Type-5 LSA的转换者状态，取值为：
• Enabled：表示通过命令指定 Type-7 LSA 转换为Type-5 LSA 的转换者7/5 translator state •Elected：表示通过选举指定 Type-7 LSA 转换为的转换者Type-5 LSA
• Disabled：表示不是 Type-7 LSA 转换为 Type-5 LSA的转换者Type-7 LSA转换为Type-5 LSA转换稳定定时器超时时间间7/5 translate stability timer interval隔SPF scheduled Count OSPF区域的路由计算总数Interface 区域内的接口信息Cost 接口的开销值接口状态State Type 接口的网络类型MTU 接口的MTU值Priority 路由器优先级Designated router 接口所属网段的DR Backup designated router 接口所属网段的 BDR OSPF定时器的值，其中：
Timers
• Hello：表示接口发送 Hello 报文的时间间隔

字段 描述
• Dead：表示邻居的失效时间
•Poll：表示接口发送轮询 Hello 报文的时间间隔
• Retransmit：表示定接口重传 LSA 时间间隔Transmit Delay 接口对LSA的传输延迟时间是否使能接口参与LFA（Loop Free Alternate）计算：
FRR backup • Enabled：使能
• Disabled：关闭接口由网络配置使能到该区域Enabled by network configuration Simple authentication enabled 采用Simple验证模式Keychain authentication enabled, name is xx 采用keychain验证模式，keychain名称为xx MD5 authentication enabled 采用MD5/HMAC-MD5验证模式The last key is xx 最新的 MD5/HMAC-MD5 验证密钥为 xx正在进行MD5/HMAC-MD5验证平滑迁移，尚未完成The rollover is in progress, xx neighbor(s) left MD5/HMAC-MD5验证平滑迁移的邻居个数为xx Packet size 接口下配置的发送OSPF报文的最大长度

##### 1.1.14 display ospf abr-asbr

命令用来显示到 OSPF 的区域边界路由器和自治系统边界路由器的路display ospf abr-asbr由信息。
【命令】
display ospf [ process-id ] abr-asbr [ verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 OSPF 进程下到区域边界路由器和自治系统边界路由器的路由信息。
verbose：显示详细信息。如果未指定本参数，将显示概要信息。
【使用指导】
如果在 Stub 区域的路由器上执行此命令，不显示有关 ASBR 的信息。
【举例】
\# 显示到 OSPF 的区域边界路由器和自治系统边界路由器的路由概要信息。

<Sysname> display ospf abr-asbr OSPF Process 1 with Router ID 192.168.1.112 Routing Table to ABR and ASBR Topology base (MTID 0)
Type Destination Area Cost Nexthop RtType Inter 3.3.3.3 0.0.0.0 3124 10.1.1.2 ASBR Intra 2.2.2.2 0.0.0.0 1562 10.1.1.2 ABR \# 显示到 OSPF 的区域边界路由器和自治系统边界路由器的路由详细信息。
<Sysname> display ospf abr-asbr verbose OSPF Process 10 with Router ID 101.1.1.11 Routing Table to ABR and ASBR Topology base (MTID 0)
Destination: 1.1.1.1 RtType : ASBR Area : 0.0.0.1 Type : Intra Nexthop : 150.0.1.12 BkNexthop : 0.0.0.0 Interface : Vlan10 BkInterface: N/A Cost : 1000表1-2 命令显示信息描述表display ospf abr-asbr字段 描述到ABR或ASBR的路由类型，取值为：
• 表示区域内路由Type Intra
• Inter 表示区域间路由Topology （暂不支持）拓扑名称，base表示标准拓扑（暂不支持）拓扑ID，0表示标准拓扑MTID Destination ABR或ASBR的路由器ID Area 下一跳地址所在的区域 ID Cost 从本路由器到达ABR或ASBR的开销下一跳地址Nexthop BkNexthop 备份下一跳地址RtType 路由器类型，包括ABR和ASBR路由出接口Interface BkInterface 路由备份出接口

##### 1.1.15 display ospf abr-summary

display ospf abr-summary 命令用来显示 OSPF 的 ABR 聚合信息。
【命令】
display ospf [ process-id ] [ area area-id ] abr-summary [ ip-address { mask-length | mask } ] [ verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 OSPF 进程的 聚合信息。
ABR area-id：显示指定区域的 ABR 聚合相关信息。area-id 表示区域的标识，可以是十进制area整数（取值范围为 0～4294967295，系统会将其转换成 地址格式）或者是 地址格式。如果未IP IP指定本参数，将显示所有区域的信息。
ip-address：指定的聚合路由的目的 IP 地址。
mask-length：网络掩码长度，取值范围为 0～32。
mask：网络掩码，点分十进制格式。
verbose：显示 ABR 聚合的详细信息。如果未指定本参数，将显示 ABR 聚合的概要信息。
【使用指导】
如果未指定 IP 地址和掩码，将显示所有的 ABR 聚合信息。
【举例】
\# 显示 OSPF 的 ABR 聚合信息。
<Sysname> display ospf abr-summary OSPF Process 1 with Router ID 2.2.2.2 ABR Summary Addresses Topology base (MTID 0)
Area: 0.0.0.1 Total summary address count: 1 Net Mask Status Count Cost
100.0.0.0 255.0.0.0 Advertise 1 (Not Configured)
表1-3 命令显示信息描述表display ospf abr-summary字段 描述Topology （暂不支持）拓扑名称，base表示标准拓扑（暂不支持）拓扑ID，0表示标准拓扑MTID

字段 描述Area 聚合路由所在的区域Total summary address count 聚合路由的路由数聚合路由的网络地址Net Mask 聚合路由的网络掩码聚合路由的状态：
• Advertise：已发布Status
• Not-Advertise：未发布Count 被聚合的路由数聚合路由的开销Cost \# 显示 OSPF 的 ABR 聚合详细信息。
<Sysname> display ospf abr-summary verbose OSPF Process 1 with Router ID 2.2.2.2 ABR Summary Addresses Topology base (MTID 0)
Area: 0.0.0.1 Total summary address count: 1 Net : 100.0.0.0 Mask : 255.0.0.0 Status : Advertise Cost : (Not Configured)
Routes count: 1 Destination NetMask Metric
100.1.1.0 255.255.255.0 1000表1-4 display ospf abr-summary verbose 命令显示信息描述表字段 描述Topology （暂不支持）拓扑名称，base表示标准拓扑MTID （暂不支持）拓扑ID，0表示标准拓扑Destination 被聚合路由的网络地址被聚合路由的网络掩码NetMask Metric 路由的开销值

##### 1.1.16 display ospf asbr-summary

display ospf asbr-summary 命令用来显示 OSPF 的 ASBR 聚合信息。

【命令】
display ospf [ process-id ] asbr-summary [ ip-address { mask-length | mask } ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 进OSPF程的 ASBR 聚合信息。
ip-address：指定的聚合路由的目的 IP 地址。
mask-length：网络掩码长度，取值范围为 0～32。
mask：网络掩码，点分十进制格式。
【使用指导】
如果未指定 IP 地址和掩码，将显示所有的 ASBR 聚合信息。
【举例】
\# 显示 OSPF 进程 1 的 ASBR 聚合信息。
<Sysname> display ospf 1 asbr-summary OSPF Process 1 with Router ID 2.2.2.2 Summary Addresses Topology base (MTID 0)
Total summary address count: 1 Summary Address Net : 30.1.0.0 Mask : 255.255.0.0 Tag : 20 Status : Advertise Cost : 10 (Configured)
Route count : 2 Destination Net mask Proto Process Type Metric
30.1.2.0 255.255.255.0 OSPF 2 2 1
30.1.1.0 255.255.255.0 OSPF 2 2 1

表1-5 display ospf asbr-summary 命令显示信息描述表字段 描述Topology （暂不支持）拓扑名称，base表示标准拓扑（暂不支持）拓扑ID，0表示标准拓扑MTID Total summary address count 聚合路由的路由数Net 聚合路由的网络地址聚合路由的网络掩码Mask Tag 聚合路由的标记字段Status 聚合路由的发布状态Cost 聚合路由的开销被聚合的路由数Route count Destination 被聚合路由的网络地址Net mask 被聚合路由的网络掩码Proto 引入路由的协议类型Process 引入路由的协议进程号Type 外部路由类型Metric 路由的开销值

##### 1.1.17 display ospf event-log

命令用来显示 OSPF 的日志信息。
display ospf event-log【命令】
display ospf [ process-id ] event-log { lsa-flush | peer | spf }【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有进程的日志信息。
lsa-flush： LSA 老化的日志信息。
peer：邻居的日志信息。
spf：路由计算的日志信息。

【使用指导】
路由计算的日志信息是指更新到 IP 路由表的路由计数信息。
邻居的日志信息包括 OSPF 邻居状态倒退到 DOWN，以及收到 BadLSReq、SeqNumberMismatch和 1-Way 事件导致邻居状态倒退的信息。
【举例】
显示 的 老化日志信息。
\# OSPF LSA <Sysname> display ospf event-log lsa-flush OSPF Process 1 with Router ID 1.1.1.1 LSA Flush Log Date: 2013-09-22 Time: 14:47:33 Received MaxAge LSA from 10.1.1.1 Type: 1 LS ID: 2.2.2.2 AdvRtr: 2.2.2.2 Seq#: 80000001 Date: 2013-09-22 Time: 14:47:33 Flushed MaxAge LSA by the self Type: 1 LS ID: 1.1.1.1 AdvRtr: 1.1.1.1 Seq#: 80000001 Date: 2013-09-22 Time: 14:47:33 Received MaxAge LSA from 10.1.2.2 Type: 1 LS ID: 2.2.2.2 AdvRtr: 2.2.2.2 Seq#: 80000001 Date: 2013-09-22 Time: 14:47:33 Flushed MaxAge LSA by the self Type: 1 LS ID: 1.1.1.1 AdvRtr: 1.1.1.1 Seq#: 80000001表1-6 display ospf event-log lsa-flush 命令显示信息描述表字段 描述Date &Time 收到MaxAge LSA的时间Received MaxAge LSA from X.X.X.X 从源地址收到MaxAge LSA由自己发起老化，洪泛MaxAge Flushed MaxAge LSA by the self LSA Type LSA类型LS ID LSA链路状态ID AdvRtr LSA发布路由器Seq# LSA序列号\# 显示 OSPF 路由计算的日志信息。
<Sysname> display ospf event-log spf OSPF Process 1 with Router ID 1.1.1.2 SPF Log Topology base (MTID 0)
Date Time Duration Intra Inter External Reason 2012-06-27 15:28:26 0.95 1 1 10000 Intra-area LSA

2012-06-27 15:28:23 0.2 0 0 0 Area 0 full neighbor 2012-06-27 15:28:19 0 0 0 0 Intra-area LSA 2012-06-27 15:28:19 0 0 0 0 external LSA 2012-06-27 15:28:19 0.3 0 0 0 Intra-area LSA 2012-06-27 15:28:12 0 1 0 0 Intra-area LSA 2012-06-27 15:28:11 0 0 0 0 Routing policy 2012-06-27 15:28:11 0 0 0 0 Intra-area LSA表1-7 display ospf event-log spf 命令显示信息描述表字段 描述Topology （暂不支持）拓扑名称，base表示标准拓扑MTID （暂不支持）拓扑ID，0表示标准拓扑路由计算开始的时间Date/Time Duration 路由计算持续时间，单位为秒Intra 区域内路由变化的个数Inter 区域间路由变化的个数External 外部路由变化的个数路由计算的原因：
•Intra-area LSA：区域内 LSA 变化
• Inter-area LSA：区域间 LSA 变化
• External LSA：外部 LSA 变化
• Configuration：配置变化
• Area 0 full neighbor：区域 0FULL 邻居个数变化
• Area 0 up interface：区域 0UP 接口个数变化Reason
• LSDB overflow state：overflow 状态变化
• number：AS 号变化AS
• ABR summarization：ABR 聚合变化
•GR end：GR 结束
• Routing policy：路由策略变化
• Intra-area tunnel：区域内隧道变化
• Others：除上述原因之外的其他原因\# 显示 OSPF 邻居的日志信息。
<Sysname> display ospf 1 event-log peer OSPF Process 1 with Router ID 1.1.1.1 Neighbors Log Date Time Local Address Remote Address Router ID Reason 2012-12-31 12:35:45 197.168.1.1 197.168.1.2 2.2.2.2 IntPhyChange 2012-12-31 12:35:19 197.168.1.1 197.168.1.2 2.2.2.2 ConfNssaArea 2012-12-31 12:34:59 197.168.1.1 197.168.1.2 2.2.2.2 SilentInt

表1-8 display ospf event-log peer 命令显示信息描述表字段 描述Date &Time 邻居状态变化的时间建立邻居关系的本端地址Local Address Remote Address 建立邻居关系的对端地址Router ID 邻居的Router ID邻居状态变化的原因：
• ResetConnect：内存不足断连接
• IntChange：接口参数改变
• VlinkChange：虚连接参数改变
• ResetOspf：重启 OSPF 进程
• UndoOspf：删除 OSPF 进程
• UndoArea：删除 OSPF 区域
• UndoNetwork：接口去使能
• SilentInt：配置抑制接口
• IntLogChange：接口逻辑属性变化
• IntPhyChange：接口物理属性变化
• IntVliChange：接口虚连接属性变化
• VlinkDown：虚连接 Down
• DeadExpired：Dead Timer 超时
• ConfStubArea：配置 Stub 区域参数
• ConfNssaArea：配置 NSSA 区域参数Reason • AuthChange：认证类型变化
• OpaqueChange：Opaque 能力改变
• Retrans：重传过多
• LLSChange：LLS 能力变化
•OOBChange：OOB 能力变化
• GRChange：GR 能力变化
• BFDDown：BFD Down
• BadLSReq：收到 BadLSReq 事件
• SeqMismatch：收到 SeqNumberMismatch 事件
• 1-Way：收到 1-Way 事件
• LocalNoLSA：本地不存在请求的 LSA
• SameLSAReq：本地的请求列表中含有已收到的LSA
• OldLSAReq：收到的LSA的老化时间比本地请求列表中LSA的老化时间大
• DdTimerOut：定时器超时，收到 报文
• EAChange：External Attribute 位发生变化
• RecvNoDupPkt：在 Loading、Full 状态收到非重复的 报文

字段 描述
• EbitChange：E 位发生变化
•MSbitChange：主从位发生变化
• IbitChange：I 位发生变化
• MSeqNumError：主路由器收到的从路由器的序列号与期望值不一致
• SSeqNumError：从路由器收到的主路由器的序列号与期望值不一致
•RecvOpqIntf：未使能 Opaque LSA 发布接收能力，但收到的 DD 报文中含有Type9 LSA
• RecvOpqArea：未使能 Opaque LSA 发布接收能力，但收到的 DD报文中含有 Type10 LSA
• RecvOpqAs：未使能 发布接收能力，但收到的 报Opaque LSA DD文中含有 Type11 LSA
• RecvNSSA：在非 NSSA 区域，收到的 DD 报文含有 Type7 LSA
• ：收到 报文含有无效的InvalidLSA DD LSA
• RecvASE：在虚连接环境或 Stub 区域中，收到的 DD 报文含有Type5 LSA【相关命令】
•reset ospf event-log

##### 1.1.18 display ospf fast-reroute lfa-candidate

命令用来显示区域中 FRR 备份下一跳候选列display ospf fast-reroute lfa-candidate表。
【命令】
display ospf [ process-id ] [ area area-id ] fast-reroute lfa-candidate【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有进程的备份下一跳候选列表。
area-id：显示指定区域 备份下一跳候选列表。area-id 表示区域的标识，可以是十area FRR进制整数（取值范围为 0 ～ 4294967295 ，系统会将其转换成 IP 地址格式）或者是 IP 地址格式 。如果未指定本参数，将显示所有区域的信息。
【举例】
\# 显示 OSPF 的 FRR 备份下一跳候选列表。

<Sysname> display ospf 1 area 0 fast-reroute lfa-candidate OSPF Process 1 with Router ID 2.2.2.2 LFA Candidate List Topology base (MTID 0)
Area: 0.0.0.0 Candidate nexthop count: 2 NextHop IntIP Interface
10.0.1.1 10.0.1.2 Vlan10
10.0.11.1 10.0.11.2 Vlan20表1-9 display ospf fast-reroute lfa-candidate 命令显示信息描述表字段 描述Topology （暂不支持）拓扑名称，base表示标准拓扑MTID （暂不支持）拓扑ID，0表示标准拓扑Area 显示该区域的备份下一跳信息备份下一跳个数Candidate nexthop count NextHop 备份下一跳地址IntIP 出接口IP地址Interface 出接口

##### 1.1.19 display ospf graceful-restart

命令用来查看 OSPF 进程的 GR 状态信息。
display ospf graceful-restart【命令】
display ospf [ process-id ] graceful-restart [ verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 OSPF 进程的 GR 状态信息。
verbose：显示 GR 详细状态信息。如果未指定本参数，将显示 OSPF 进程的 GR 状态概要信息。
【举例】
显示 进程的 详细状态信息。
\# OSPF GR

<Sysname> display ospf graceful-restart verbose OSPF Process 1 with Router ID 1.1.1.1 Graceful Restart information Graceful Restart capability : Enable(IETF)
Graceful Restart support : Planned and unplanned,Partial Helper capability : Enable(IETF)
Helper support : Planned and unplanned(IETF),Strict LSA check Current GR state : Normal Graceful Restart period : 40 seconds Number of neighbors under Helper: 0 Number of restarting neighbors : 0 Last exit reason:
Restarter : None Helper : None Area: 0.0.0.0 Authtype: None Area flag: Normal Area up Interface count: 2 Interface: 40.4.0.1 (Vlan-interface40)
Restarter state: Normal State: P-2-P Type: PTP Last exit reason:
Restarter : None Helper : None Neighbor count of this interface: 1 Helper：0 Number of neighbors under Neighbor IP address GR state Last Helper exit reason
3.3.3.3 40.4.0.3 Normal None Virtual-link Neighbor-ID -> 4.4.4.4, Neighbor-State: Full Restarter state: Normal Interface: 20.2.0.1 (Vlink)
Transit Area：0.0.0.1 Last exit reason:
Restarter : None Helper : None Neighbor IP address GR state Last Helper exit reason
4.4.4.4 20.2.0.4 Normal Reset neighbor表1-10 display ospf graceful-restart 命令显示信息描述表字段 描述OSPF Process 1 with Router ID 1.1.1.1 OSPF 进程是 1 ， Router ID 是 1.1.1.1 的 GR 状态信息Graceful Restart information进程GR能力配置：
Graceful Restart capability
•Enable(IETF)：使能 IETF GR 能力

字段 描述
• Enable(Nonstandard)：使能非 IETF GR 能力
•Disable：关闭了 GR 能力进程GR支持模式（GR使能时才显示）：
• Planned and unplanned：支持计划和非计划 GR
• only：只支持计划性Graceful Restart support Planned GR
• Partial：支持接口级 GR
• Global：不支持接口级 GR，支持全局GR进程Helper能力配置：
• Enable(IETF)：支持作为标准 GR Helper 的能力
• Enable(Nonstandard)：支持作为非标准GR Helper的Helper capability 能力
• Enable(IETF and nonstandard)：同时支持作为标准和非标准 GR Helper 的能力
• Disable：不支持作为 GR Helper 的能力显示支持Helper的策略（Helper使能时才显示）：
• check：Helper 端支持严格的 检查Strict LSA LSA Helper support
• Planned and unplanned：支持作为计划和非计划重启的 Helper
• only：只支持作为计划 的Planned GR Helper当前OSPF进程的GR状态：
• Normal：普通状态Current GR state
• Under GR：进程正在 GR
• Under Helper：进程正在作为 GR Helper Graceful-restart period GR周期Number of neighbors under helper 处于Helper状态的邻居数量Number of restarting neighbors Helper端显示的处于重启路由器的数量上次退出原因，其中：
Last exit reason • Restarter：表示退出 Restarter 的原因
• Helper：表示退出 Helper 的原因开始列举当前进程中各区域的信息。显示当前区域ID，IP地Area址格式区域验证模式，取值为：
• None：表示无验证Authtype • Simple：表示简单验证模式
• MD5：表示 MD5 验证模式
• Keychain：表示 验证模式keychain区域类型：
Area flag
• Normal：普通区域

字段 描述
• Stub：Stub 区域
•StubNoSummary：完全 Stub 区域
• NSSA：NSSA 区域
• NSSANoSummary：完全 NSSA 区域区域下UP的接口计数Area up Interface count Interface 区域内的接口信息Restarter state 作为Restarter的状态State 接口状态Type 接口的网络类型Neighbor count of this interface 接口下的邻居Neighbor 邻居Router ID邻居IP地址IP address邻居的GR状态：
• Normal：普通状态GR state
• Under GR：进程正在 GR
• Under Helper：进程正在作为 GR Helper Last Helper exit reason 上一次作为该邻居Helper退出的原因Virtual-link Neighbor-ID Vlink的邻居Router ID Vlink和邻居的状态，包括Down、Init、2-Way、ExStart、Neighbor-State Exchange、Loading和Full Interface Vlink接口所属的出接口

##### 1.1.20 display ospf interface

命令用来显示 OSPF 的接口信息。
display ospf interface【命令】
display ospf [ process-id ] interface [ interface-type interface-number | verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator

【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 OSPF 进程的接口信息。
interface-number：接口类型和编号。显示指定接口的 OSPF 详细信息。
interface-type verbose：显示所有接口的 OSPF 详细信息。
【使用指导】
如果未指定接口或参数 verbose，将显示所有接口的 OSPF 概要信息。
【举例】
显示所有接口的 概要信息。
\# OSPF <Sysname> display ospf interface OSPF Process 1 with Router ID 192.168.1.1 Interfaces Area: 0.0.0.0 IP Address Type State Cost Pri DR BDR
192.168.1.1 PTP P-2-P 1562 1 0.0.0.0 0.0.0.0 Area: 0.0.0.1 IP Address Type State Cost Pri DR BDR
172.16.0.1 Broadcast DR 1 1 172.16.0.1 0.0.0.0表1-11 命令显示信息描述表display ospf interface字段 描述Area 接口所属的区域ID IP Address 接口IP地址（不管是否使能了流量工程）
接口的网络类型，取值为：
• PTP 表示网络类型为点对点
• 表示网络类型为点对多点Type PTMP
• Broadcast 表示网络类型为广播
• 表示网络类型为NBMA NBMA根据OSPF接口状态机确定的当前接口状态，取值为：
• DOWN 表示在接口上没有发送和接收任何路由协议的报文
• Loopback 表示路由器到网络的接口处于环回状态，不能用于正常的数据传输
• Waiting 表示接口开始发送和接收 Hello 报文，并试图去识别网络上的 DR 和 BDR State • 表示接口将每隔 的时间间隔发送 报文，并尝试和接口链路另一端P-2-P HelloInterval Hello相连的路由器建立邻接关系
• DR 表示路由器是所连网络的指定路由器
• 表示路由器是所连网络的备份指定路由器BDR
• DROther 表示路由器既不是所连网络的指定路由器，也不是所连网络的备份指定路由器

字段 描述Cost 接口开销Pri 路由器优先级接口所属网段的DR DR BDR 接口所属网段的BDR \# 显示 OSPF 指定接口 Vlan-interface10 的详细信息。
<Sysname> display ospf interface vlan-interface 10 OSPF Process 1 with Router ID 192.168.1.1 Interfaces Area: 0.0.0.0 Interface: 172.16.0.1 (Vlan-interface10)
Cost: 1 State: DR Type: Broadcast MTU: 1500 Priority: 1 Designated router: 172.16.0.1 Backup designated router: 0.0.0.0 Timers: Hello 10, Dead 40, Poll 40, Retransmit 5, Transmit Delay 1 FRR backup: Enabled Primary path detection mode: BFD ctrl Enabled by interface configuration (including secondary IP addresses)
BFD: echo MD5 authentication enabled.
The last key is 3.
The rollover is in progress, 2 neighbor(s) left.
LDP state: No-LDP LDP sync state: Achieved Packet size: 1000表1-12 display ospf interface verbose 命令显示信息描述表字段 描述Interface 接口IP地址等信息最大传输单元MTU OSPF定时器的值，其中：
• Hello：表示接口发送 Hello 报文的时间间隔Timers • Dead：表示邻居的失效时间
• Poll ：表示接口发送轮询 Hello 报文的时间间隔
• Retransmit：表示接口重传 LSA 时间间隔Transmit Delay 接口对LSA的传输延迟时间

字段 描述是否使能接口参与LFA（Loop Free Alternate）计算：
•FRR backup Enabled：使能
• Disabled：关闭主链路检测方式：
• ctrl：BFD 控制报文检测方式Primary path detection mode BFD
• BFD echo：BFD echo 报文检测方式Enabled by interface configuration (including secondary IP 接口使能OSPF，包括接口从IP地址addresses)
接口使能OSPF的BFD功能：
• ctrl：通过 控制报文方式实现 功能BFD BFD BFD
• echo：通过 BFD echo 报文方式实现 BFD 功能Simple authentication enabled 采用Simple验证模式Keychain authentication enabled,采用keychain验证模式，keychain名称为xx name is xx MD5 authentication enabled 采用MD5/HMAC-MD5验证模式The last key is xx 最新的MD5/HMAC-MD5验证字标识符为xx The rollover is in progress, xx 正在进行MD5/HMAC-MD5验证平滑迁移，尚未完成MD5/HMAC-MD5验证neighbor(s) left. 平滑迁移的邻居个数为xx LDP状态：
• Init：表示处于初始化状态，LDP 还没有上报状态LDP state • No-LDP：表示未配置 LDP
• Not ready：表示未建立 LDP 会话
• Ready：表示已建立 会话LDP LDP IGP同步状态：
• Init：表示初始化LDP sync state
• Achieved：表示已同步
• Max cost：表示保持最大开销值接口下配置的发送OSPF报文的最大长度Packet size

##### 1.1.21 display ospf lsdb

display ospf lsdb 命令用来显示 OSPF 的链路状态数据库信息。
【命令】
display ospf [ process-id ] lsdb [ brief | originate-router advertising-router-id | self-originate ] display ospf [ process-id ] lsdb { opaque-as | ase } [ link-state-id ] [ originate-router advertising-router-id | self-originate ]

display ospf [ process-id ] [ area area-id ] lsdb { asbr | network | nssa | opaque-area | opaque-link | router | summary } [ link-state-id ] [ originate-router advertising-router-id | self-originate ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 进OSPF程的链路状态数据库信息。
area area-id：显示数据库中指定区域的 LSA 信息。area-id 表示区域的标识，可以是十进制整数（取值范围为 0～4294967295，系统会将其转换成 IP 地址格式）或者是 IP 地址格式。如果未指定本参数，将显示所有区域的信息。
brief：显示数据库的概要信息。
asbr：显示数据库中 Type-4 LSA（ASBR Summary LSA）的信息。
ase：显示数据库中 Type-5 LSA（AS External LSA）的信息。
network：显示数据库中 Type-2 LSA（Network LSA）的信息。
nssa：显示数据库中 Type-7 LSA（NSSA External LSA）的信息。
opaque-area：显示数据库中 Type-10 LSA （Opaque-area LSA）的信息。
opaque-as：显示数据库中 Type-11 LSA （Opaque-AS LSA）的信息。
opaque-link：显示数据库中 Type-9 LSA（Opaque-link LSA）的信息。
router：显示数据库中 Type-1 LSA（Router LSA）的信息。
summary：显示数据库中 Type-3 LSA（Network Summary LSA）的信息。
link-state-id：链路状态 ID，IP 地址格式。
originate-router advertising-router-id：发布 LSA 报文的路由器的 Router ID。
self-originate：显示本地路由器自己产生的 LSA 的数据库信息。
【举例】
\# 显示 OSPF 的链路状态数据库信息。
<Sysname> display ospf lsdb OSPF Process 1 with Router ID 192.168.0.1 Link State Database Area: 0.0.0.0 Type LinkState ID AdvRouter Age Len Sequence Metric Router 192.168.0.2 192.168.0.2 474 36 80000004 0 Router 192.168.0.1 192.168.0.1 21 36 80000009 0 Network 192.168.0.1 192.168.0.1 321 32 80000003 0 Sum-Net 192.168.1.0 192.168.0.1 321 28 80000002 1

Sum-Net 192.168.2.0 192.168.0.2 474 28 80000002 1 Area: 0.0.0.1 Type LinkState ID AdvRouter Age Len Sequence Metric Router 192.168.0.1 192.168.0.1 21 36 80000005 0 Sum-Net 192.168.2.0 192.168.0.1 321 28 80000002 2 Sum-Net 192.168.0.0 192.168.0.1 321 28 80000002 1 Type 9 Opaque (Link-Local Scope) Database Flags: * -Vlink interface LSA Type LinkState ID AdvRouter Age Len Sequence Interfaces
*Opq-Link 3.0.0.0 7.2.2.1 8 14 80000001 10.1.1.2
*Opq-Link 3.0.0.0 7.2.2.2 8 14 80000001 20.1.1.2表1-13 display ospf lsdb 命令显示信息描述表字段 描述Area 显示该区域的LSDB信息LSA类型Type LinkState ID LSA链路状态ID AdvRouter LSA发布路由器LSA的老化时间Age Len LSA的长度Sequence LSA序列号Metric 度量值表示Vlink接口产生的Opaque
*Opq-Link LSA \# 显示进程号为 1 的 OSPF 进程的链路状态数据库中网络 LSA 的信息。
<Sysname> display ospf 1 lsdb network OSPF Process 1 with Router ID 192.168.1.1 Link State Database Area: 0.0.0.0 Type : Network LS ID : 192.168.0.2 Adv Rtr : 192.168.2.1 LS age : 922 Len : 32 Options : E Seq# : 80000003 Checksum : 0x8d1b Net mask : 255.255.255.0 Attached router 192.168.1.1 Attached router 192.168.2.1

Area: 0.0.0.1 Type : Network LS ID : 192.168.1.2 Adv Rtr : 192.168.1.2 LS age : 782 Len : 32 Options : NP Seq# : 80000003 Checksum : 0x2a77 Net mask : 255.255.255.0 Attached router 192.168.1.1 Attached router 192.168.1.2表1-14 display ospf lsdb network 命令显示信息描述表字段 描述Type LSA类型LS ID DR的IP地址发布路由器Adv Rtr LS age LSA的老化时间Len LSA的长度LSA选项，各选项含义如下：
• O：Opaque LSA 发布接受能力
• E：AS 外部 LSA 的接受能力Options • EA：外部扩展属性 LSA 的接受和转发能力
• DC：支持按需链路
• N：是否支持 NSSA 外部 LSA
• P：非纯末稍区域中的 ABR 路由器将 Type-7 LSA 转换为 Type-5 LSA 的能力Seq# LSA序列号Checksum LSA校验和Net mask 网络掩码Attached router 与DR形成了完全邻接关系的路由器的Router ID，也包括DR自身的Router ID

##### 1.1.22 display ospf nexthop

命令用来显示进程中的下一跳信息。
display ospf nexthop【命令】
display ospf [ process-id ] nexthop【视图】
任意视图

【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有进程的下一跳信息。
【举例】
\# 显示 OSPF 路由下一跳信息。
<Sysname> display ospf nexthop OSPF Process 1 with Router ID 1.1.1.2 Neighbor Nexthop Information NbrID Nexthop Interface RefCount Status
192.168.12.1 0.0.0.0 Vlan10 4 Valid
192.168.12.2 192.168.12.2 Vlan10 3 Valid
192.168.12.1 0.0.0.0 Loop100 1 Valid表1-15 display ospf nexthop 命令显示信息描述表字段 描述NbrID 邻居路由器ID Nexthop 下一跳地址Interface 出接口RefCount 该下一跳被引用次数该下一跳状态：
Status • Valid：生效
•Invalid：未生效

##### 1.1.23 display ospf non-stop-routing status

display ospf non-stop-routing status 命令用来显示 OSPF 的 NSR 阶段信息。
【命令】
display ospf [ process-id ] non-stop-routing status【视图】
任意视图【缺省用户角色】
network-admin network-operator

【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 OSPF 进程的 NSR 阶段信息。
【举例】
显示 的 阶段信息。
\# OSPF NSR <Sysname> display ospf non-stop-routing status OSPF Process 1 with Router ID 192.168.33.12 Non Stop Routing information Non Stop Routing capability : Enabled Upgrade phase : Normal表1-16 display ospf non-stop-routing status 命令显示信息描述表字段 描述是否使能NSR功能，其中：
Non Stop Routing capability • Enabled：使能 NSR
• Disabled：不使能 NSR升级的各个阶段：
• Prepare：升级准备阶段
• Restore Smooth：升级数据平滑阶段
• Preroute：路由计算预处理阶段Upgrade phase
• Calculating：路由计算阶段
• Redisting：路由引入阶段
• Original and age：LSA 生成和老化阶段
• Normal：普通状态

##### 1.1.24 display ospf peer

命令用来显示 OSPF 中各区域邻居的信息。
display ospf peer【命令】
display ospf [ process-id ] peer [ verbose ] [ interface-type interface-number ] [ neighbor-id ]【视图】
任意视图【缺省用户角色】
network-admin network-operator

【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 OSPF 进程的各区域邻居的信息。
verbose：显示 OSPF 各区域邻居的详细信息。如果未指定本参数，将显示 OSPF 进程各区域邻居的概要信息。
interface-number：接口类型和编号。如果未指定本参数，将显示所有接interface-type口的 OSPF 邻居的信息。
neighbor-id：邻居路由器的 Router ID。如果未指定本参数，将显示所有邻居路由器的 OSPF 邻居的信息。
【举例】
\# 显示 OSPF 邻居详细信息。
<Sysname> display ospf peer verbose OSPF Process 1 with Router ID 1.1.1.1 Neighbors Area 0.0.0.0 interface 1.1.1.1(Vlan-interface100)'s neighbors Router ID: 1.1.1.2 Address: 1.1.1.2 GR state: Normal State: Full Mode: Nbr is master Priority: 1 DR: 1.1.1.2 BDR: 1.1.1.1 MTU: 0 Options is 0x02 (-|-|-|-|-|-|E|-)
Dead timer due in 33 sec Neighbor is up for 02:03:35 Authentication sequence: [ 0 ] Neighbor state change count: 6 BFD status: Disabled Last Neighbor Down Event:
Router ID: 22.22.22.22 Local Address: 11.11.11.11 Remote Address: 22.22.22.22 Time: Apr 9 03:18:19 2014 Reason: Ospf_ifachange表1-17 命令显示信息描述表display ospf peer verbose字段 描述显示接口在指定区域邻居信息，其中：
Area areaID interface • areaID 表示邻居所属的区域IPAddress(InterfaceName)'s
• IPAddress 表示接口 IP 地址neighbors
• 表示接口名称InterfaceName Router ID 邻居路由器ID Address 邻居接口地址GR state GR状态，取值为：

字段 描述
• Normal：普通状态
•Restarter：正在作为 GR Restarter
• Complete：GR 完成
• Helper：正在作为 GR Helper邻居状态，取值为：
• Down 表示邻居关系的初始状态
• 表示在邻居失效时间内收到来自邻居路由器的 报文，但该Init Hello Hello数据包内没有包含自己的 ID，双向通信还没有建立起来Router
• Attempt 该状态仅对 NBMA 网络上的邻居有效，表示最近没有从邻居收到信息，但仍需作出进一步的尝试，用以与邻居联系
• 2-Way表示双向通信已经建立，在从邻居路由器收到的Hello报文中看到了State自己的 Router ID
• Exstart 表示路由器和邻居建立主/从关系、确定初始 DD 报文的序列号，为交换 DD 报文做好准备
• Exchange 表示路由器向其邻居发送描述自己 LSDB 的 DD 报文
• Loading 表示路由器向邻居发送链路状态请求报文，请求最新的 LSA
• 表示路由器与邻居路由器之间建立起完全邻接关系Full路由器在数据库同步阶段，路由器与邻居协商的主从关系，取值为：
Mode • Nbr is master 表示邻居路由器为主路由器
• Nbr is slave 表示邻居路由器为从路由器Priority 邻居路由器优先级DR 接口所属网段的DR接口所属网段的BDR BDR MTU 接口MTU的值邻居的LSA选项，各选项含义如下：
• O：Opaque 发布接受能力LSA
• E：AS 外部 LSA 的接受能力
• EA：外部扩展属性 的接受和转发能力LSA Options
• DC：支持按需链路
•N：是否支持 NSSA 外部 LSA
• P：非纯末稍区域中的 ABR 路由器将 Type-7 LSA 转换为 Type-5 LSA 的能力Dead timer due in 33 sec 邻居将在33秒后被认为不可达与邻居建立的时长02:03:35 Neighbor is up for 02:03:35 Authentication sequence 验证序列号Neighbor state change count 邻居状态发生改变的次数BFD状态，各状态含义如下：
BFD status
• Disabled：未使能 BFD

字段 描述
• Enabled (Control mode)：已使能 BFD，并处于控制模式
•Enabled (Echo mode)：已使能 BFD，并处于回应模式Last Neighbor Down Event 最后一次邻居down事件Local Address 本端IP地址Remote Address 对端IP地址邻居down的时间Time Reason 邻居down的原因\# 显示 OSPF 邻居概要信息。
<Sysname> display ospf peer OSPF Process 1 with Router ID 1.1.1.1 Neighbor Brief Information Area: 0.0.0.0 Router ID Address Pri Dead-Time State Interface
1.1.1.2 1.1.1.2 1 40 Full/DR Vlan10表1-18 display ospf peer 命令显示信息描述表字段 描述Area 邻居所属的区域Router ID 邻居路由器ID邻居接口IP地址Address Pri 邻居路由器优先级Dead-Time OSPF的邻居失效时间Interface 与邻居相连的接口State 邻居状态（Down、Init、Attempt、2-Way、Exstart、Exchange、Loading、Full）

##### 1.1.25 display ospf peer statistics

display ospf peer statistics 命令用来显示本地路由器所有 OSPF 邻居的统计信息，即处于各种状态的邻居数目。
【命令】
display ospf [ process-id ] peer statistics【视图】
任意视图

【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 OSPF 进程的邻居统计信息。
【举例】
\# 显示所有 OSPF 邻居的统计信息。
<Sysname> display ospf peer statistics OSPF Process 1 with Router ID 192.168.1.112 Neighbor Statistics Area ID Down Attempt Init 2-Way ExStart Exchange Loading Full Total
0.0.0.0 0 0 0 0 0 0 0 1 1
0.0.0.2 0 0 0 0 0 0 0 1 1 Total 0 0 0 0 0 0 0 2 2表1-19 display ospf peer statistics 命令显示信息描述表字段 描述Area ID 区域ID，显示当前路由器位于该区域所有邻居路由器的状态统计信息Down 同一个区域内状态为Down的邻居路由器数目Attempt 同一个区域内状态为Attempt的邻居路由器数目同一个区域内状态为Init的邻居路由器数目Init 2-Way 同一个区域内状态为2-Way的邻居路由器数目ExStart 同一个区域内状态为ExStart的邻居路由器数目Exchange 同一个区域内状态为Exchange的邻居路由器数目Loading 同一个区域内状态为Loading的邻居路由器数目Full 同一个区域内状态为Full的邻居路由器数目处于各种状态（Down/Attempt/Init/2-Way/ExStart/Exchange/Loading/Full）邻居路Total由器的总和

##### 1.1.26 display ospf request-queue

命令用来显示 OSPF 的请求列表信息。
display ospf request-queue【命令】
display ospf [ process-id ] request-queue [ interface-type interface-number ] [ neighbor-id ]

【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 OSPF 进程的请求列表信息。
interface-number：接口类型和编号。如果未指定本参数，将显示所有接interface-type口的请求列表信息。
neighbor-id：邻居路由器的 Router ID。如果未指定本参数，将显示所有邻居路由器的请求列表信息。
【举例】
\# 显示 OSPF 请求列表信息。
<Sysname> display ospf request-queue OSPF Process 100 with Router ID 192.168.1.59 Link State Request List The Router's Neighbor is Router ID 2.2.2.2 Address 10.1.1.2 Interface 10.1.1.1 Area 0.0.0.0 Request list:
Type LinkState ID AdvRouter Sequence Age Router 2.2.2.2 1.1.1.1 80000004 1 Network 192.168.0.1 1.1.1.1 80000003 1 Sum-Net 192.168.1.0 1.1.1.1 80000002 2表1-20 display ospf request-queue 命令显示信息描述表字段 描述The Router's Neighbor is Router ID 邻居路由器的Router ID Address 邻居接口IP地址Interface 本地接口IP地址区域ID Area Request list 请求列表信息Type LSA类型LinkState ID 链路状态ID AdvRouter 发布路由器的 Router ID Sequence LSA的序列号Age LSA的老化时间

##### 1.1.27 display ospf retrans-queue

命令用来显示 OSPF 的重传列表信息。
display ospf retrans-queue【命令】
display ospf [ process-id ] retrans-queue [ interface-type interface-number ] [ neighbor-id ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 进OSPF程的重传列表信息。
interface-number：接口类型和编号。如果未指定本参数，将显示所有接interface-type口的重传列表信息。
neighbor-id：邻居路由器的 Router ID。如果未指定本参数，将显示所有邻居路由器的重传列表信息。
【举例】
显示 重传列表信息。
\# OSPF <Sysname> display ospf retrans-queue OSPF Process 100 with Router ID 192.168.1.59 Link State Retransmission List The Router's Neighbor is Router ID 192.168.1.111 Address 111.1.1.1 Interface 111.1.1.2 Area 0.0.0.1 Retransmit list:
Type LinkState ID AdvRouter Sequence Age Router 2.2.2.2 2.2.2.2 80000004 1 Network 12.18.0.1 2.2.2.2 80000003 1 Sum-Net 12.18.1.0 2.2.2.2 80000002 2表1-21 display ospf retrans-queue 命令显示信息描述表字段 描述The Router's Neighbor is Router ID 邻居路由器ID Address 邻居接口IP地址Interface 本地接口IP地址区域ID Area

字段 描述Retransmit list 重传列表信息Type LSA类型链路状态ID LinkState ID AdvRouter 发布路由器的Router ID Sequence LSA的序列号Age LSA的老化时间

##### 1.1.28 display ospf routing

命令用来显示 OSPF 路由表的信息。
display ospf routing【命令】
display ospf [ process-id ] routing [ ip-address { mask-length | mask } ] [ interface interface-type interface-number ] [ nexthop nexthop-address ] [ verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 进OSPF程的路由表信息。
ip-address：路由的目的 IP 地址。
mask-length：网络掩码长度，取值范围为 0～32。
mask ：网络掩码，点分十进制格式。
interface interface-type interface-number ： 显 示 指 定 出 接 口 的 路 由 信 息 。
interface-type interface-number 为接口类型和编号。如果未指定本参数，将显示所有接口的路由表信息。
nexthop-address：显示指定下一跳 IP 地址的路由信息。如果未指定本参数，将显示nexthop所有的 路由表信息。
OSPF verbose：显示路由表详细信息。如果未指定本参数，将显示路由表的概要信息。
【举例】
\# 显示 OSPF 路由表的信息。
<Sysname> display ospf routing OSPF Process 1 with Router ID 192.168.1.112

Routing Table Topology base (MTID 0)
Routing for network Destination Cost Type NextHop AdvRouter Area
192.168.1.0/24 1562 Stub 192.168.1.2 192.168.1.2 0.0.0.0
172.16.0.0/16 1563 Inter 192.168.1.1 192.168.1.1 0.0.0.0 Total nets: 2 Intra area: 1 Inter area: 1 ASE: 0 NSSA: 0表1-22 display ospf routing 命令显示信息描述表字段 描述Topology （暂不支持）拓扑名称，base表示标准拓扑（暂不支持）拓扑ID，0表示标准拓扑MTID Destination 目的网络Cost 到达目的地址的开销路由类型（Intra、Transit、Stub、Inter、Type1和Type2）
Type NextHop 下一跳地址AdvRouter 发布路由器Area 区域ID区域内部、区域间、ASE和NSSA区域的路由总数Total nets Intra area 区域内部路由总数Inter area 区域间路由总数ASE OSPF区域外路由总数NSSA NSSA区域路由总数\# 显示 OSPF 路由表的详细信息。
<Sysname> display ospf routing verbose OSPF Process 2 with Router ID 192.168.1.112 Routing Table Topology base (MTID 0)
Routing for network Destination: 192.168.1.0/24 Priority: Low Type: Stub AdvRouter: 192.168.1.2 Area: 0.0.0.0 SubProtoID: 0x1 Preference: 10

NextHop: 192.168.1.2 BkNextHop: N/A IfType: Broadcast BkIfType: N/A Interface: Vlan100 BkInterface: N/A NibID: 0x1300000c Status: Normal Cost: 1562 Destination: 172.16.0.0/16 Priority: Low Type: Inter AdvRouter: 192.168.1.1 Area: 0.0.0.0 SubProtoID: 0x1 Preference: 10 NextHop: 192.168.1.1 BkNextHop: N/A IfType: Broadcast BkIfType: N/A Interface: Vlan101 BkInterface: N/A NibID: 0x1300000c Status: Normal Cost: 1563 Total nets: 2 Intra area: 2 Inter area: 0 ASE: 0 NSSA: 0表1-23 display ospf routing verbose 命令显示信息描述表字段 描述Topology （暂不支持）拓扑名称，base表示标准拓扑MTID （暂不支持）拓扑ID，0表示标准拓扑Priority 前缀优先级，取值为：Critical、High、Medium和Low路由类型（Intra-area、Transit、Stub、Inter-Area、 External和Type2 External）
Type Type1 AdvRouter 发布路由器Area 区域ID SubProtoID 子协议ID OSPF路由优先级Preference NextHop 主下一跳IP地址BkNextHop 备份下一跳IP地址路由主下一跳网络类型IfType BkIfType 路由备份下一跳网络类型Interface 路由出接口BkInterface 路由备份出接口路由下一跳信息的ID值NibID路由状态，具体如下：
• Local：该条路由在本地，未发送给路由管理模块Status
• Invalid：路由下一跳无效
• Stale：该路由下一跳较旧

字段 描述
• Normal：正常可用状态
•Delete：处于删除状态
• Host-Adv：该条路由为主机路由
• Rely：该条路由为迭代路由到达目的地址的开销Cost

##### 1.1.29 display ospf spf-tree

display ospf spf-tree 命令用来显示 OSPF 区域的最短路径树信息。
【命令】
display ospf [ process-id ] [ area area-id ] spf-tree [ verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 OSPF 进程下区域的最短路径树信息。
area area-id：显示指定 OSPF 区域的最短路径树信息。area-id 表示区域的标识，可以是十进制整数（取值范围为 0～4294967295，系统会将其转换成 IP 地址格式）或者是 IP 地址格式。如果未指定本参数，将显示所有区域的最短路径树信息。
verbose：显示 区域的最短路径树的详细信息。如果未指定本参数，将显示 区域的OSPF OSPF最短路径树的概要信息。
【举例】
\# 显示进程 1 下区域 0 的最短路径树信息。
<Sysname> display ospf 1 area 0 spf-tree OSPF Process 1 with Router ID 100.0.0.4 Flags: S-Node is on SPF tree R-Node is directly reachable I-Node or Link is init D-Node or Link is to be deleted P-Neighbor is parent A-Node is in candidate list C-Neighbor is child T-Node is tunnel destination H-Nexthop changed N-Link is a new path V-Link is involved G-Link is in change list Topology base (MTID 0)

Area: 0.0.0.0 Shortest Path Tree SpfNode Type Flag SpfLink Type Cost Flag >192.168.119.130 Network S R
-->114.114.114.111 NET2RT 0 C
-->100.0.0.4 NET2RT 0 P >114.114.114.111 Router S
-->192.168.119.130 RT2NET 65535 P >100.0.0.4 Router S
-->192.168.119.130 RT2NET 10 C表1-24 display ospf spf-tree 命令显示信息描述表字段 描述Topology （暂不支持）拓扑名称，base表示标准拓扑MTID （暂不支持）拓扑ID，0表示标准拓扑SPF节点，若节点类型为路由器，则为路由器ID；若节点类型为网络，则为该网络DR接口IP地址。其中，Type为节点类型：
• Network：表示网络节点
• Router：表示路由器节点Flag为节点标志：
• I：节点处于初始化状态SpfNode
• A：节点在候选列表上
• S：节点在 SPF 树上
• R：该节点与根节点直连
• D：该节点将被删除
• T：该节点为隧道的终点SPF链路，其值表示对端节点。其中，Cost为链路开销，Type为链路类型：
• RT2RT：表示路由器到路由器链路
• NET2RT：表示网络到路由器链路
• RT2NET：表示路由器到网络链路Flag为链路标志：
• I：链路处于初始化状态
• P：目的节点是父节点SpfLink
• C：目的节点是子节点
• D：链路将要被删除
• H：下一跳发生改变
• V：目的节点删除或者是新增节点时，链路的目的节点不在 SPF 树上或处于删除状态
• N：新增链路，并且源节点和目的节点都在 SPF 树上
• G：链路在区域变化列表中\# 显示进程 1 下区域 0 的最短路径树详细信息。
<Sysname> display ospf 1 area 0 spf-tree verbose

OSPF Process 1 with Router ID 100.0.0.4 Flags: S-Node is on SPF tree R-Node is directly reachable I-Node or Link is init D-Node or Link is to be deleted P-Neighbor is parent A-Node is in candidate list C-Neighbor is child T-Node is tunnel destination H-Nexthop changed N-Link is a new path V-Link is involved G-Link is in change list Topology base (MTID 0)
Area: 0.0.0.0 Shortest Path Tree >LsId(192.168.119.130)
AdvId : 100.0.0.4 NodeType : Network Mask : 255.255.255.0 SPFLinkCnt : 2 Distance : 10 VlinkData: 0.0.0.0 ParentLinkCnt: 1 NodeFlag: S R NextHop : 1
192.168.119.130 Interface: Vlan100 BkNextHop: 1
0.0.0.0 Interface: Vlan100
-->LinkId(114.114.114.111)
AdvId : 100.0.0.4 LinkType : NET2RT LsId : 192.168.119.130 LinkCost : 0 NextHopCnt: 1 LinkData: 0.0.0.0 LinkNewCost: 0 LinkFlag : C
-->LinkId(100.0.0.4)
AdvId : 100.0.0.4 LinkType : NET2RT LsId : 192.168.119.130 LinkCost : 0 NextHopCnt: 1 LinkData: 0.0.0.0 LinkNewCost: 0 LinkFlag : P表1-25 display ospf spf-tree verbose 命令显示信息描述表字段 描述Topology （暂不支持）拓扑名称，base表示标准拓扑MTID （暂不支持）拓扑ID，0表示标准拓扑链路状态ID LsId AdvId 通告路由器ID节点类型，其中：
• Network：表示网络节点NodeType
• Router：表示路由器节点Mask 网络掩码，若为路由器节点掩码为 0 SPF链路个数SPFLinkCnt Distance 表示到根节点的开销

字段 描述VlinkData Vlink报文的目的地址ParentLinkCnt 父链路个数节点标志：
• I：节点处于初始化状态
•A：节点在候选列表上NodeFlag • S：节点在 SPF 树上
• R：该节点与根节点直连
• D：该节点将被删除
• T：该节点为隧道的终点下一跳信息NextHop Interface 出接口BkNextHop 备份下一跳信息LinkId 链路ID链路类型，其中：
• RT2RT：表示路由器到路由器链路LinkType
• NET2RT：表示网络到路由器链路
• RT2NET：表示路由器到网络链路LinkCost 当前链路开销下一跳个数NextHopCnt LinkData 链路数据LinkNewCost 新的链路开销链路标志：
• I：链路处于初始化状态
• P：目的节点是父节点
• C：目的节点是子节点
• D ：链路将要被删除LinkFlag
• H：下一跳发生改变
• V：目的节点删除或者是新增节点时，链路的目的节点不在 SPF 树上或处于删除状态
• N：新增链路，并且源节点和目的节点都在 树上SPF
• G：链路在区域变化列表中

##### 1.1.30 display ospf statistics

命令用来显示 的统计信息。
display ospf statistics OSPF

【命令】
display ospf [ process-id ] statistics [ error | packet [ interface-type interface-number ] ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 OSPF 进程的统计信息。
error：显示错误统计信息。如果未指定本参数，将显示 OSPF 进程的报文、LSA 和路由的统计信息。
packet：显示 OSPF 的报文统计信息。
interface-number：接口类型和编号。显示指定接口的统计信息。如果未interface-type指定本参数，将显示所有接口的统计信息。
【举例】
\# 显示 OSPF 进程的统计信息。
<Sysname> display ospf statistics OSPF Process 1 with Router ID 2.2.2.2 Statistics I/O statistics Type Input Output Hello 61 122 DB Description 2 3 Link-State Req 1 1 Link-State Update 3 3 Link-State Ack 3 2 LSAs originated by this router Router : 4 Network : 0 Sum-Net : 0 Sum-Asbr: 0 External: 0 NSSA : 0 Opq-Link: 0 Opq-Area: 0 Opq-As : 0 LSAs originated: 4 LSAs received: 7

Routing table:
Intra area: 2 Inter area: 3 ASE/NSSA: 0表1-26 display ospf statistics 命令显示信息描述表字段 描述I/O statistics 收发的报文和LSA的详细统计信息Type OSPF报文类型Input 接收报文数发送报文数Output Hello OSPF Hello报文DB Description OSPF数据库描述报文Link-State Req OSPF链路状态请求报文链路状态更新报文Link-State Update OSPF Link-State Ack OSPF链路状态确认报文LSAs originated by this router 本路由器发布LSA的详细统计信息生成Type-1 LSA的数目Router Network 生成Type-2 LSA的数目Sum-Net 生成Type-3 LSA的数目Sum-Asbr 生成Type-4 LSA的数目生成Type-5 LSA的数目External NSSA 生成Type-7 LSA的数目Opq-Link 生成Type-9 LSA的数目Opq-Area 生成Type-10 LSA的数目Opq-As 生成Type-11 LSA的数目LSA originated 生成的LSA的总数LSA received 接收的LSA的总数路由表信息Routing table Intra area 区域内路由的数量Inter area 区域间路由的数量ASE/NSSA 自治系统外部/NSSA区域路由的数量\# 显示 OSPF 进程的错误统计信息。
<Sysname> display ospf statistics error OSPF Process 1 with Router ID 192.168.1.112 OSPF Packet Error Statistics

0 : Router ID confusion 0 : Bad packet 0 : Bad version 0 : Bad checksum 0 : Bad area ID 0 : Drop on unnumbered link 0 : Bad virtual link 0 : Bad authentication type 0 : Bad authentication key 0 : Packet too small 0 : Neighbor state low 0 : Transmit error 0 : Interface down 0 : Unknown neighbor 0 : HELLO: Netmask mismatch 0 : HELLO: Hello-time mismatch 0 : HELLO: Dead-time mismatch 0 : HELLO: Ebit option mismatch 0 : HELLO: Mbit option mismatch 0 : DD: MTU option mismatch 0 : DD: Unknown LSA type 0 : DD: Ebit option mismatch 0 : ACK: Bad ack 0 : ACK: Unknown LSA type 0 : REQ: Empty request 0 : REQ: Bad request 0 : UPD: LSA checksum bad 0 : UPD: Unknown LSA type 0 : UPD: Less recent LSA表1-27 display ospf statistics error 命令显示信息描述表字段 描述Router ID confusion 含有重复路由器ID的OSPF报文数Bad packet 非法的OSPF报文数错误版本号的OSPF报文数Bad version Bad checksum 校验和出错的OSPF报文数Bad area ID 非法的区域ID的OSPF报文数Drop on unnumbered link 在地址借用链路上丢弃的OSPF报文数Bad virtual link 错误的虚链路的OSPF报文数Bad authentication type 含有非法验证类型的OSPF报文数Bad authentication key 含有错误验证码的OSPF报文数报文长度太小的OSPF报文数Packet too small Neighbor state low 在低邻居状态收到的OSPF报文数Transmit error 传输出错的OSPF报文数Interface down 接口down的计数未知的邻居发来的OSPF报文数Unknown neighbor HELLO: Netmask mismatch 网络掩码不匹配的Hello报文数HELLO: Hello-time mismatch Hello定时器不匹配的Hello报文数Dead定时器不匹配的Hello报文数HELLO: Dead-time mismatch HELLO: Ebit option mismatch Option 字段 E 位不匹配的 Hello 报文数HELLO: Mbit option mismatch Option字段M位不匹配的Hello报文数DD: MTU option mismatch MTU不匹配的DD报文数

字段 描述DD: Unknown LSA type DD报文中描述未知类型LSA数目DD: Ebit option mismatch Option字段E位不匹配的DD报文数收到不匹配的ack数目ACK: Bad ack ACK: Unknown LSA type 收到LSA类型未知的ack数目REQ: Empty request 不含有任何请求信息的LSR报文数REQ: Bad request 请求错误LSA的LSR报文数LSU报文中LSA校验和出错的LSA数目UPD: LSA checksum bad UPD: Unknown LSA type LSU报文中含有未知类型LSA数目UPD: Less recent LSA LSU报文中含有不是最新的LSA数目\# 显示 OSPF 进程和接口的报文统计信息。
<Sysname> display ospf statistics packet OSPF Process 100 with Router ID 192.168.1.59 Packet Statistics Waiting to send packet count: 0 Hello DD LSR LSU ACK Total Input : 489 6 2 44 40 581 Output: 492 8 2 45 40 587 Area: 0.0.0.1 Interface: 20.1.1.1 (Vlan-interface100)
DD LSR LSU ACK Total Input : 0 0 0 0 0 Output: 0 0 0 0 0 Interface: 100.1.1.1 (Vlan-interface100)
DD LSR LSU ACK Total Input : 3 1 22 16 42 Output: 2 1 19 20 42表1-28 display ospf statistics packet 命令显示信息描述表字段 描述Waiting to send packet count 等待发送报文数Hello Hello报文DD 数据库描述报文链路状态请求报文LSR LSU 链路状态更新报文ACK 链路状态确认报文

字段 描述Total 报文总数Input 接收报文数发送报文数Output Area 区域ID Interface 接口地址和接口名【相关命令】
• reset ospf statistics

##### 1.1.31 display ospf vlink

命令用来显示 OSPF 的虚连接信息。
display ospf vlink【命令】
display ospf [ process-id ] vlink【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 OSPF 进程的虚连接信息。
【举例】
\# 显示 OSPF 的虚连接信息。
<Sysname> display ospf vlink OSPF Process 1 with Router ID 3.3.3.3 Virtual Links Virtual-link Neighbor-ID -> 2.2.2.2, Neighbor-State: Full Interface: 10.1.2.1 (Vlan-interface100)
Cost: 1562 State: P-2-P Type: Virtual Transit Area: 0.0.0.1 Timers: Hello 10 , Dead 40 , Retransmit 5 , Transmit Delay 1 MD5 authentication enabled.
The last key is 3.
The rollover is in progress, 2 neighbor(s) left.

表1-29 display ospf vlink 命令显示信息描述表字段 描述Virtual-link Neighbor-id 通过虚连接相连的邻居路由器的Router ID邻居状态，包括Down、Init、2-Way、ExStart、Exchange、Loading和Full Neighbor-State Interface 此虚连接的本端接口的IP地址和名称Cost 接口的路由开销接口状态State Type 类型：虚连接Transit Area 传输区域ID（如果当前接口为虚连接，则显示）
OSPF定时器，分别定义如下：
• Hello：表示接口发送 Hello 报文的时间间隔，单位为秒Timers
• Dead：表示邻居的失效时间，单位为秒
• Retransmit：表示接口重传 时间间隔，单位为秒LSA Transmit Delay 接口对LSA的传输延迟时间，单位为秒Simple authentication enabled 采用Simple验证模式Keychain authentication采用keychain验证模式，keychain名称为xx enabled, name is xx MD5 authentication enabled 采用MD5/HMAC-MD5验证模式The last key is xx 最新的MD5/HMAC-MD5验证字标识符为xx The rollover is in progress, xx 正在进行MD5/HMAC-MD5验证平滑迁移，尚未完成MD5验证平滑迁移的邻居neighbor(s) left 个数为xx

##### 1.1.32 display router id

命令用来显示全局 Router ID。
display router id【命令】
display router id【视图】
任意视图【缺省用户角色】
network-admin network-operator【举例】
\# 显示已配置的全局 Router ID。
<Sysname> display router id Configured router ID is 1.1.1.1

##### 1.1.33 distribute bgp-ls

distribute bgp-ls 命令用来配置允许设备将 OSPF 链路状态信息发布到 BGP。
undo distribute bgp-ls 命令用来恢复缺省情况。
【命令】
distribute bgp-ls [ strict-link-checking ] undo distribute bgp-ls【缺省情况】
不允许设备将 OSPF 链路状态信息发布到 BGP。
【视图】
视图OSPF【缺省用户角色】
network-admin【参数】
strict-link-checking：开启严格链路检查功能，即发布到 BGP 的链路信息中的本端地址与远端地址必须在同一网段。如果未指定本参数，则表示关闭严格链路检查功能，即发布到 BGP 的链路信息中的本端地址与远端地址可以不处于同一网段。本功能仅适用于 链路。
P2P【使用指导】
本功能允许设备将链路状态信息发布到 BGP，由 BGP 向外发布，以满足需要知道链路状态信息的应用的需求。OSPF 链路状态信息随链路状态的更新同步发布。
在包含等价链路的拓扑环境中，如果拓扑中每条链路的两端分别在各自的链路中处于同一网段，建议使用严格链路检查功能，以免等价链路震荡时将错误的链路信息发布到 BGP。
严格链路检查功能和前缀抑制功能不能同时开启，使用本功能前，请确保前缀抑制功能处于关闭状态。
【举例】
\# 配置允许设备将 OSPF 进程 1 的链路状态信息发布到 BGP。
<Sysname> system-view [Sysname] ospf 1 [Sysname-ospf-1] distribute bgp-ls

##### 1.1.34 dscp

dscp 命令用来配置 OSPF 发送协议报文的 DSCP 优先级。
命令用来恢复缺省情况。
undo dscp【命令】
dscp dscp-value undo dscp【缺省情况】
OSPF 发送协议报文的 DSCP 优先级为 48。

【视图】
OSPF 视图【缺省用户角色】
network-admin【参数】
dscp-value：DSCP 优先级，取值范围为 0～63。
【举例】
\# 配置 OSPF 进程 1 发送协议报文的 DSCP 优先级为 63。
<Sysname> system-view [Sysname] ospf 1 [Sysname-ospf-1] dscp 63

##### 1.1.35 enable link-local-signaling

命令用来使能 本地链路的信令能力。
enable link-local-signaling OSPF命令用来关闭 本地链路的信令能力。
undo enable link-local-signaling OSPF【命令】
enable link-local-signaling undo enable link-local-signaling【缺省情况】
OSPF 本地链路的信令能力处于关闭状态。
【视图】
OSPF 视图【缺省用户角色】
network-admin【举例】
使能 进程 的本地链路的信令能力。
\# OSPF 1 <Sysname> system-view [Sysname] ospf 1 [Sysname-ospf-1] enable link-local-signaling

##### 1.1.36 enable out-of-band-resynchronization

命令用来使能 带外同步能力。
enable out-of-band-resynchronization OSPF命令用来关闭 带外同步能力。
undo enable out-of-band-resynchronization OSPF【命令】
enable out-of-band-resynchronization undo enable out-of-band-resynchronization

【缺省情况】
OSPF 带外同步能力处于关闭状态。
【视图】
OSPF 视图【缺省用户角色】
network-admin【使用指导】
在配置本命令之前，必须先使能 OSPF 本地链路的信令能力。
【举例】
\# 使能 OSPF 进程 1 的带外同步能力。
<Sysname> system-view [Sysname] ospf 1 [Sysname-ospf-1] enable link-local-signaling [Sysname-ospf-1] enable out-of-band-resynchronization【相关命令】
• enable link-local-signaling

##### 1.1.37 event-log

event-log 命令用来配置 OSPF 的日志信息个数。
命令用来取消 的日志信息个数的配置。
undo event-log OSPF【命令】
event-log { lsa-flush | peer | spf } size count undo event-log { lsa-flush | peer | spf } size【缺省情况】
路由计算、邻居和和 LSA 老化的日志信息个数为 10。
【视图】
OSPF 视图【缺省用户角色】
network-admin【参数】
lsa-flush：LSA 老化日志信息个数。
peer：邻居日志信息个数。
spf：SPF 日志信息个数。
count：指定日志信息个数，取值范围为 0～65535。
size【举例】
\# 配置 OSPF 进程 100 的路由计算日志信息个数为 50。

<Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] event-log spf size 50

##### 1.1.38 fast-reroute (OSPF view)

命令用来配置 OSPF 快速重路由功能。
fast-reroute命令用来关闭 OSPF 快速重路由功能。
undo fast-reroute【命令】
fast-reroute { lfa [ abr-only ] | route-policy route-policy-name } undo fast-reroute【缺省情况】
OSPF 快速重路由功能处于关闭状态。
【视图】
OSPF 视图【缺省用户角色】
network-admin【参数】
lfa：为所有路由通过 LFA（Loop Free Alternate）算法选取备份下一跳信息。
abr-only：仅选取到 ABR 设备的路由作为备份下一跳。
： 为 通 过 策 略 的 路 由 指 定 备 份 下 一 跳 ，route-policy route-policy-name为路由策略名，为 1～63 个字符的字符串，区分大小写。
route-policy-name【使用指导】
OSPF 快速重路由功能和前缀无关收敛功能同时配置时，OSPF 快速重路由功能生效。
OSPF 快速重路由功能（通过 LFA 算法选取备份下一跳信息）不能与 vlink-peer 命令同时使用。
【举例】
\# 使能 OSPF 进程 1 的快速重路由功能，为所有路由通过 LFA 算法选取备份下一跳信息。
<Sysname> system-view [Sysname] ospf 1 [Sysname-ospf-1] fast-reroute lfa

##### 1.1.39 filter (OSPF area view)

filter 命令用来配置对 Type-3 LSA 进行过滤。
undo filter 命令用来取消对 Type-3 LSA 的过滤。
【命令】
filter { ipv4-acl-number | prefix-list prefix-list-name | route-policy route-policy-name } { export | import } undo filter { export | import }

【缺省情况】
不对 Type-3 LSA 进行过滤。
【视图】
OSPF 区域视图【缺省用户角色】
network-admin【参数】
ipv4-acl-number：指定的基本或高级 IPv4 ACL 编号，对进出本区域的 Type-3 LSA 进行过滤，取值范围为 2000～3999。
prefix-list-name：指定的地址前缀列表，对进出本区域的 Type-3 LSA 进行过滤，为 1～63个字符的字符串，区分大小写。
route-policy-name：指定的路由策略，对进出本区域的 Type-3 LSA 进行过滤，为 1～63 个字符的字符串，区分大小写。
export：对 ABR 向其它区域发布的 Type-3 LSA 进行过滤。
import：对 ABR 向本区域发布的 Type-3 LSA 进行过滤。
【使用指导】
此命令只在 路由器上有效，对区域内部路由器无效。
ABR【举例】
\# 根据地址前缀列表 my-prefix-list 和编号为 2000 的基本 ACL 分别对进出 OSPF 区域 1 的 Type-3 LSA 进行过滤。
<Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] area 1 [Sysname-ospf-100-area-0.0.0.1] filter prefix-list my-prefix-list import [Sysname-ospf-100-area-0.0.0.1] filter 2000 export

##### 1.1.40 filter-policy export (OSPF view)

命令用来配置 OSPF 对引入的路由信息进行过滤。
filter-policy export命令用来取消 OSPF 对引入的路由信息进行过滤。
undo filter-policy export【命令】
filter-policy { ipv4-acl-number | prefix-list prefix-list-name } export [ protocol [ process-id ] ] undo filter-policy export [ protocol [ process-id ] ]【缺省情况】
OSPF 不对引入的路由信息进行过滤。
【视图】
OSPF 视图

【缺省用户角色】
network-admin【参数】
ipv4-acl-number：用于过滤路由信息目的地址的基本或高级 IPv4 ACL 编号，取值范围为 2000～3999。
prefix-list-name：用于过滤路由信息目的地址的 地址前缀列表的名称，为 1～63 个字符的IP字符串，区分大小写。
protocol：路由协议名称，指定何种路由协议的路由信息将被过滤。如果没有指定 protocol 参数，对引入的任何一个协议产生的路由都要进行过滤。
process-id：路由协议进程号，取值范围为 1～65535。只有当 protocol 为 isis、ospf、rip时，支持该参数。
【使用指导】
当配置的是高级 ACL（3000～3999）时，其使用规则如下：
使用命令
• rule [ rule-id ] { deny | permit } ip source sour-addr sour-wildcard 来过滤指定目的地址的路由。
使用命令
• rule [ rule-id ] { deny | permit } ip source sour-addr sour-wildcard destination dest-addr dest-wildcard 来过滤指定目的地址和掩码的路由。
其中，source 用来过滤路由目的地址，destination 用来过滤路由掩码，配置的掩码应该是连续的（当配置的掩码不连续时该过滤掩码的条件不生效）。
【举例】
配置 进程 使用编号为 的基本 对引入的路由进行过滤。
\# OSPF 100 2000 ACL <Sysname> system-view [Sysname] acl basic 2000 [Sysname-acl-ipv4-basic-2000] rule deny source 192.168.10.0 0.0.0.255 [Sysname-acl-ipv4-basic-2000] quit [Sysname] ospf 100 [Sysname-ospf-100] filter-policy 2000 export配置 进程 使用编号为 的高级 对引入的路由进行过滤，只允许\# OSPF 100 3000 ACL 113.0.0.0/16通过。
<Sysname> system-view [Sysname] acl advanced 3000 [Sysname-acl-ipv4-adv-3000] rule 10 permit ip source 113.0.0.0 0 destination 255.255.0.0 0 [Sysname-acl-ipv4-adv-3000] rule 100 deny ip [Sysname-acl-ipv4-adv-3000] quit [Sysname] ospf 100 [Sysname-ospf-100] filter-policy 3000 export【相关命令】
• import-route

##### 1.1.41 filter-policy import (OSPF view)

filter-policy import 命令用来配置 OSPF 对通过接收到的 LSA 计算出来的路由信息进行过滤。
命令用来恢复缺省情况。
undo filter-policy import【命令】
filter-policy { ipv4-acl-number [ gateway prefix-list-name ] | gateway prefix-list-name | prefix-list prefix-list-name [ gateway prefix-list-name ] | route-policy route-policy-name } import undo filter-policy import【缺省情况】
OSPF 不对通过接收到的 LSA 计算出来的路由信息进行过滤。
【视图】
视图OSPF【缺省用户角色】
network-admin【参数】
ipv4-acl-number：用于过滤路由信息目的地址的基本或高级 IPv4 ACL 编号，取值范围为 2000～3999。
prefix-list-name：指定的地址前缀列表，基于要加入到路由表的路由信息的下一跳gateway进行过滤。prefix-list-name 为 1～63 个字符的字符串，区分大小写。
prefix-list-name：指定的地址前缀列表，基于目的地址对接收的路由信息进prefix-list行过滤。prefix-list-name 为 1～63 个字符的字符串，区分大小写。
route-policy-name：指定路由策略名，基于路由策略对接收的路由信息进行route-policy过滤。route-policy-name 为 1～63 个字符的字符串，区分大小写。
【使用指导】
当配置的是高级 ACL（3000～3999）或者指定的路由策略中配置的是高级 ACL 时，其使用规则如下：
使用命令
• rule [ rule-id ] { deny | permit } ip source sour-addr来过滤指定目的地址的路由。
sour-wildcard使用命令
• rule [ rule-id ] { deny | permit } ip source sour-addr sour-wildcard destination dest-addr dest-wildcard 来过滤指定目的地址和掩码的路由。
其中，source 用来过滤路由目的地址，destination 用来过滤路由掩码，配置的掩码应该是连续的（当配置的掩码不连续时该过滤掩码的条件不生效）。
【举例】
使用编号为 的基本 对接收的路由信息进行过滤。
\# 2000 ACL <Sysname> system-view [Sysname] acl basic 2000

[Sysname-acl-ipv4-basic-2000] rule deny source 192.168.10.0 0.0.0.255 [Sysname-acl-ipv4-basic-2000] quit [Sysname] ospf 100 [Sysname-ospf-100] filter-policy 2000 import \# 使用编号为 3000 的高级 ACL 对接收的路由进行过滤，只允许 113.0.0.0/16 通过。
<Sysname> system-view [Sysname] acl advanced 3000 [Sysname-acl-ipv4-adv-3000] rule 10 permit ip source 113.0.0.0 0 destination 255.255.0.0 0 [Sysname-acl-ipv4-adv-3000] rule 100 deny ip [Sysname-acl-ipv4-adv-3000] quit [Sysname] ospf 100 [Sysname-ospf-100] filter-policy 3000 import

##### 1.1.42 graceful-restart (OSPF view)

命令用来使能 协议的 能力。
graceful-restart OSPF GR命令用来关闭 协议的 能力。
undo graceful-restart OSPF GR【命令】
graceful-restart [ ietf | nonstandard ] [ global | planned-only ] * undo graceful-restart【缺省情况】
OSPF 协议的 GR 能力处于关闭状态。
【视图】
OSPF 视图【缺省用户角色】
network-admin【参数】
ietf：IETF 标准 能力选项。
GR nonstandard：非 标准 能力选项。
IETF GR：全局 GR，必须保证所有的 都存在，整个 才会完成，如果有一个global GR Helper GR GR Helper失效（比如，接口 down），则整个 GR 失败。如果未指定本参数，表示支持接口级 GR，即只要有一个 GR Helper 存在，则整个 GR 会完成。
planned-only：表示只支持计划重启。如果未指定本参数，表示计划重启和非计划重启都支持。
【使用指导】
GR 包括计划重启和非计划重启：
• 计划重启指的是手动通过命令 执行重启，或通过命令reset ospf process placement触发进程的主备倒换，在进行重启或主备倒换前 会先发送reoptimize GR Restarter Grace-LSA。
• 非计划重启指的是由于设备故障等原因进行重启或主备倒换，在进行重启或主备倒换前 GR Restarter 不会事先发送 Grace-LSA。

在使能 OSPF 协议的 IETF 标准 GR 能力前，需要先使能 OSPF 不透明链路状态发布接收能力（opaque-capability enable）。
在使能 协议的非 标准的 能力前，需要先使能 本地链路的信令能力（enable OSPF IETF GR OSPF link-local-signaling ） 和 OSPF 带 外 同 步 能 力 （enable out-of-band-resynchronization）。
如果在使能 OSPF 协议的 GR 能力时不指定可选参数 和 ietf，则nonstandard nonstandard为缺省配置。
OSPF GR 特性与 OSPF NSR 特性互斥，即 和 命令graceful-restart non-stop-routing互斥，不能同时配置。
【举例】
\# 使能 OSPF 进程 1 的 IETF 标准 GR 能力。
<Sysname> system-view [Sysname] ospf 1 [Sysname-ospf-1] opaque-capability enable [Sysname-ospf-1] graceful-restart ietf使能 进程 的非 标准 能力。
\# OSPF 1 IETF GR <Sysname> system-view [Sysname] ospf 1 [Sysname-ospf-1] enable link-local-signaling [Sysname-ospf-1] enable out-of-band-resynchronization [Sysname-ospf-1] graceful-restart nonstandard【相关命令】
• enable link-local-signaling
• enable out-of-band-resynchronization
• opaque-capability enable

##### 1.1.43 graceful-restart helper enable

graceful-restart helper enable 命令用来使能 OSPF 的 GR Helper 能力。
undo graceful-restart helper enable 命令用来关闭 OSPF 的 GR Helper 能力。
【命令】
graceful-restart helper enable [ planned-only ] undo graceful-restart helper enable【缺省情况】
OSPF 的 GR Helper 能力处于开启状态。
【视图】
视图OSPF【缺省用户角色】
network-admin

【参数】
planned-only：表示只支持计划重启。如果未指定本参数，表示计划重启和非计划重启（即异常重启）都支持。
【使用指导】
参数 只有在 标准 的时候使用。
planned-only IETF GR Helper【举例】
\# 使能 OSPF 进程 1 的 GR Helper 能力。
<Sysname> system-view [Sysname] ospf 1 [Sysname-ospf-1] graceful-restart helper enable

##### 1.1.44 graceful-restart helper strict-lsa-checking

命令用来使能 严格 检graceful-restart helper strict-lsa-checking GR Helper LSA查能力。
undo graceful-restart helper strict-lsa-checking 命令用来关闭 GR Helper 严格LSA 检查能力。
【命令】
graceful-restart helper strict-lsa-checking undo graceful-restart helper strict-lsa-checking【缺省情况】
协议的 严格 检查能力处于关闭状态。
OSPF GR Helper LSA【视图】
OSPF 视图【缺省用户角色】
network-admin【使用指导】
当检查到 GR Helper 设备的 LSA 发生变化时候，Helper 设备退出 GR Helper 模式。
【举例】
使能 进程 的 严格 检查能力。
\# OSPF 1 GR Helper LSA <Sysname> system-view [Sysname] ospf 1 [Sysname-ospf-1] graceful-restart helper strict-lsa-checking

##### 1.1.45 graceful-restart interval (OSPF view)

命令用来配置 OSPF 协议的 GR 重启间隔时间。
graceful-restart interval命令用来恢复缺省情况。
undo graceful-restart interval

【命令】
graceful-restart interval interval undo graceful-restart interval【缺省情况】
OSPF 协议的 GR 重启间隔时间为 120 秒。
【视图】
OSPF 视图【缺省用户角色】
network-admin【参数】
interval：指定 OSPF 协议的 GR 重启间隔时间（期望重启时间），取值范围为 40～1800，单位为秒。
【使用指导】
OSPF 协议的 GR 重启间隔时间不能小于 OSPF 所有接口中邻居失效时间的最大值，否则可能会造成 OSPF 协议的 GR 重启失败。
【举例】
\# 配置 OSPF 进程 1 的 GR 重启间隔时间为 100 秒。
<Sysname> system-view [Sysname] ospf 1 [Sysname-ospf-1] graceful-restart interval 100【相关命令】
• ospf timer dead

##### 1.1.46 host-advertise

host-advertise 命令用来配置并发布一条主机路由。
undo host-advertise 命令用来删除一条主机路由。
【命令】
host-advertise ip-address cost-value undo host-advertise ip-address【缺省情况】
OSPF 不发布主机路由。
【视图】
区域视图OSPF【缺省用户角色】
network-admin

【参数】
ip-address：主机 IP 地址。
cost-value：主机路由的开销值，取值范围为 1～65535。
【举例】
\# 配置发布一条路由 1.1.1.1，并设置其开销为 100。
<Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] area 0 [Sysname-ospf-100-area-0.0.0.0] host-advertise 1.1.1.1 100

##### 1.1.47 import-route (OSPF view)

import-route 命令用来配置引入外部路由信息。
命令用来取消引入外部路由信息。
undo import-route【命令】
import-route bgp [ as-number ] [allow-ibgp] [ [ cost cost-value | inherit-cost ] | nssa-only | route-policy route-policy-name | tag tag | type type ] * import-route { direct | static } [ [ cost cost-value | inherit-cost ] | nssa-only | route-policy route-policy-name | tag tag | type type ] * import-route { isis | ospf | rip } [ process-id | all-processes ] [ allow-direct | [ cost cost-value | inherit-cost ] | nssa-only | route-policy route-policy-name | tag tag | type type ] * undo import-route { bgp | direct | { isis | ospf | rip } [ process-id | all-processes ] | static }【缺省情况】
不引入外部路由信息。
【视图】
OSPF 视图【缺省用户角色】
network-admin【参数】
bgp：引入 BGP 协议的路由。
direct：引入直连路由。
isis：引入 IS-IS 协议的路由。
ospf：引入 OSPF 协议的路由。
rip：引入 RIP 协议的路由。
static：引入静态路由。

as-number：引入指定 AS 内的路由。as-number 为 AS 号，取值范围为 1～4294967295。只有当 是 时该参数可选。当 是 时，如果没有指定本参数，则引入所有protocol bgp protocol bgp的 IPv4 EBGP 路由。建议配置时指定 AS 号，否则引入的 IPv4 EBGP 路由数量过多时，会引发设备内存资源紧张等问题。
process-id：路由协议进程号，取值范围为 1～65535，缺省值为 1。
all-processes：引入指定路由协议所有进程的路由。
allow-ibgp：允许引入 IBGP 路由。import-route bgp 命令表示只引入 EBGP 路由；
命令表示将 IBGP 路由也引入，容易引起路由环路，请慎用。
import-route bgp allow-ibgp allow-direct：在引入的路由中包含使能了该协议的接口网段路由。如果未指定本参数，在引入协议路由时不会包含使能了该协议的接口网段路由。当 与allow-direct route-policy route-policy-name 参数一起使用时，需要注意路由策略中配置的匹配规则不要与接口路由信息存在冲突，否则会导致 配置失效。例如，当配置 参数引入 OSPF allow-direct allow-direct直连时，在路由策略中不要配置 匹配条件，否则，allow-direct 参数if-match route-type失效。
cost-value：路由开销值，取值范围为 0～16777214。
cost inherit-cost：指定引入外部路由时使用该路由的原有开销值。
nssa-only：设置 的 比特位不置位，即在对端路由器上不能转为 LSA。如Type-7 LSA P Type-5果未指定本参数，Type-7 LSA 的 P 比特位被置位，即在对端路由器上可以转为 Type-5 LSA（如果本地路由器是 ABR，则会检查骨干区域是否存在 FULL 状态的邻居，当 FULL 状态的邻居存在时，产生的 中 比特位不置位）。
Type-7 LSA P： 配 置 只 能 引 入 符 合 指 定 路 由 策 略 的 路 由 。
route-policy route-policy-name为路由策略名称，为 1～63 个字符的字符串，区分大小写。
route-policy-name tag：外部 中的标记，取值范围为 0～4294967295，缺省值为 1。
tag LSA type：度量值类型，取值范围为 1～2，缺省值为 2。
type【使用指导】
外部路由是指到达自治系统外部的路由，有两类：
• 第一类外部路由（Type1 External）：这类路由的可信程度较高，并且和 OSPF 自身路由的开销具有可比性，所以到第一类外部路由的开销等于本路由器到相应的 ASBR 的开销与 ASBR到该路由目的地址的开销之和。
• 第二类外部路由（Type2 External）：这类路由的可信度比较低，所以 OSPF 协议认为从 ASBR到自治系统之外的开销远远大于在自治系统之内到达 的开销。所以计算路由开销时将ASBR主要考虑前者，即到第二类外部路由的开销等于 ASBR 到该路由目的地址的开销。如果计算出开销值相等的两条路由，再考虑本路由器到相应的 ASBR 的开销。
该命令只能引入路由表中状态为 active 的路由，是否为 active 状态可以通过 display ip命令来查看。不能引入缺省路由。
routing-table protocol命令配置后，引入的路由只在 NSSA 区域产生 Type-7 LSA，不会在import-route nssa-only非 区域产生 。
NSSA Type-5 LSA如果未指定 和 参数，则引入的外部路由的开销值为 1。
cost inherit-cost

命令只能取消undo import-route { isis | ospf | rip } all-processes import-route命令的配置，不能取消{ isis | ospf | rip } all-processes import-route { isis | ospf | rip } process-id 命令的配置。
【举例】
\# 指定引入的进程号为 40 的 RIP 路由为 Type-2 外部路由，路由标记为 33，度量值为 50。
<Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] import-route rip 40 type 2 tag 33 cost 50【相关命令】
(OSPF view)
• default-route-advertise

##### 1.1.48 ispf enable (OSPF view)

命令用来使能增量 SPF 计算功能。
ispf enable命令用来关闭增量 SPF 计算功能。
undo ispf enable【命令】
ispf enable undo ispf enable【缺省情况】
增量 计算功能处于使能状态。
SPF【视图】
OSPF 视图【缺省用户角色】
network-admin【使用指导】
使能增量 SPF 计算功能后，当网络的拓扑结构发生变化影响到最短路径树的结构时，只将受影响的部分节点进行修正，而不重建整棵最短路径树。
【举例】
\# 关闭 OSPF 进程 100 的增量 SPF 计算功能。
<Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] undo ispf enable

##### 1.1.49 log-peer-change

log-peer-change 命令用来打开邻居状态变化的输出开关。
undo log-peer-change 命令用来关闭邻居状态变化的输出开关。
【命令】
log-peer-change undo log-peer-change

【缺省情况】
邻居状态变化的输出开关处于打开状态。
【视图】
OSPF 视图【缺省用户角色】
network-admin【使用指导】
打开邻接状态输出开关后，OSPF 邻居状态变化时会生成日志信息发送到设备的信息中心，通过设置信息中心的参数，最终决定日志信息的输出规则（即是否允许输出以及输出方向）。（有关信息中心参数的配置请参见“网络管理和监控配置指导”中的“信息中心”。）
【举例】
关闭 进程 的邻居状态变化的输出开关。
\# OSPF 100 <Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] undo log-peer-change

##### 1.1.50 lsa-arrival-interval

命令用来配置 OSPF LSA 重复到达的最小时间间隔。
lsa-arrival-interval命令用来恢复缺省情况。
undo lsa-arrival-interval【命令】
lsa-arrival-interval interval undo lsa-arrival-interval【缺省情况】
OSPF LSA 重复到达的最小时间间隔为 1000 毫秒。
【视图】
OSPF 视图【缺省用户角色】
network-admin【参数】
interval：OSPF 重复到达的最小时间间隔，取值范围为 0～60000，单位为毫秒。
LSA【使用指导】
如果在 interval 的时间间隔内又收到一条 LSA 类型、LS ID、生成路由器 ID 均相同的 LSA 则直接丢弃，这样就可以抑制网络频繁变化可能导致的带宽资源和路由器资源被过多占用的问题。
建议interval 小于或等于lsa-generation-interval 命令所配置的minimum-interval。
【举例】
\# 设置 OSPF LSA 重复到达的最小时间间隔为 200 毫秒。
<Sysname> system-view

[Sysname] ospf 100 [Sysname-ospf-100] lsa-arrival-interval 200【相关命令】
• lsa-generation-interval

##### 1.1.51 lsa-generation-interval

lsa-generation-interval 命令用来配置 OSPF LSA 重新生成的时间间隔。
undo lsa-generation-interval 命令用来恢复缺省情况。
【命令】
lsa-generation-interval maximum-interval [ minimum-interval [ incremental-interval ] ] undo lsa-generation-interval【缺省情况】
重新生成的最大时间间隔为 秒，最小时间间隔为 毫秒，时间间隔惩罚增量为OSPF LSA 5 50 200毫秒。
【视图】
OSPF 视图【缺省用户角色】
network-admin【参数】
maximum-interval：OSPF 重新生成的最大时间间隔，取值范围为 1～60，单位为秒。
LSA minimum-interval：OSPF 重新生成的最小时间间隔，取值范围为 10～60000，单位为毫LSA秒。
incremental-interval：OSPF LSA 重新生成的时间间隔惩罚增量，取值范围为 10～60000，单位为毫秒。
【使用指导】
通过调节 LSA 重新生成的时间间隔，可以抑制网络频繁变化可能导致的带宽资源和路由器资源被过多占用的问题。在网络变化不频繁的情况下，将 LSA重新生成时间间隔缩小到 minimum-interval，而在网络变化频繁的情况下可以进行相应惩罚，将等待时间按照配置的惩罚增量延长，最大不超过maximum-interval。
minimum-interval 和 incremental-interval 配置值不允许大于 maximum-interval 配置值。
【举例】
设置 重新生成的最大时间间隔为 秒，最小时间间隔为 毫秒，惩罚增量为 毫秒。
\# LSA 2 100 100 <Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] lsa-generation-interval 2 100 100

【相关命令】
• lsa-arrival-interval

##### 1.1.52 lsdb-overflow-interval

lsdb-overflow-interval 命令用来配置 OSPF 尝试退出 overflow 状态的定时器时间间隔。
undo lsdb-overflow-interval 命令用来恢复缺省情况。
【命令】
lsdb-overflow-interval interval undo lsdb-overflow-interval【缺省情况】
OSPF 尝试退出 overflow 状态的定时器时间间隔是 300 秒。
【视图】
视图OSPF【缺省用户角色】
network-admin【参数】
interval：OSPF 尝试退出 overflow 状态的定时器时间间隔，取值范围为 0～2147483647，单位为秒。
【使用指导】
网络中出现过多 LSA，会占用大量系统资源。当设置的 中 的最大数量达到上LSDB External LSA限时，LSDB 会进入 overflow 状态，在 overflow 状态中，不再接收 External LSA，同时删除自己生成的 External LSA，对于已经收到的 External LSA 则不会删除。这样就可以减少 LSA 从而节省系统资源。
通过调整定时器间隔，可以调整 OSPF 退出 overflow 状态的时间。
配置为 0 秒表示不启动定时器，不退出 overflow 状态。
【举例】
配置 尝试退出 的定时器间隔为 秒。
\# OSPF overflow 10 <Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] lsdb-overflow-interval 10

##### 1.1.53 lsdb-overflow-limit

命令用来配置 OSPF 的 LSDB 中 External LSA 的最大条目数。
lsdb-overflow-limit命令用来恢复缺省情况。
undo lsdb-overflow-limit【命令】
lsdb-overflow-limit number undo lsdb-overflow-limit

【缺省情况】
不对 LSDB 中 External LSA 的最大条目数进行限制。
【视图】
OSPF 视图【缺省用户角色】
network-admin【参数】
number：LSDB 中 External LSA 的最大条目数，取值范围为 1～1000000。
【举例】
\# 设置 LSDB 中 External LSA 的最大条目数为 400000。
<Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] lsdb-overflow-limit 400000

##### 1.1.54 maximum load-balancing (OSPF view)

maximum load-balancing 命令用来配置 OSPF 支持的等价路由的最大条数。
undo maximum load-balancing 命令用来恢复缺省情况。
【命令】
maximum load-balancing number undo maximum load-balancing【缺省情况】
OSPF 支持的等价路由的最大条数与系统支持最大等价路由的条数相同。
【视图】
OSPF 视图【缺省用户角色】
network-admin【参数】
number：等价路由的最大条数，当 number 取值为 1 时，相当于不进行负载分担。
【使用指导】
本命令中 number 参数的取值范围和 max-ecmp-num 命令相关。通过 max-ecmp-num 命令配置系统支持的最大等价路由条数为 m，并重启设备后，number 参数的取值范围将修改为 1～m。
【举例】
配置 支持的等价路由的最大条数为 。
\# OSPF 2 <Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] maximum load-balancing 2

【相关命令】
• max-ecmp-num（三层技术-IP 路由命令参考/IP 路由基础）

##### 1.1.55 network (OSPF area view)

network 命令用来配置 OSPF 区域所包含的网段并在指定网段的接口上使能 OSPF。
undo network 命令用来删除区域所包含的网段并关闭指定网段接口上的 OSPF 功能。
【命令】
network ip-address wildcard-mask undo network ip-address wildcard-mask【缺省情况】
接口不属于任何区域且 OSPF 功能处于关闭状态。
【视图】
区域视图OSPF【缺省用户角色】
network-admin【参数】
ip-address：接口所在的网段地址。
wildcard-mask：IP 地址掩码的反码，相当于将 IP 地址的掩码取反（0 变 1，1 变 0）。其中，“1”表示忽略 IP 地址中对应的位，“0”表示必须保留此位。（例如：子网掩码 255.0.0.0，该掩码的通配符掩码为 0.255.255.255）。
【使用指导】
该命令可以在一个区域内配置一个或多个接口。在接口上运行 OSPF 协议，此接口的主 IP 地址必须在 network 命令指定的网段范围之内。如果此接口只有从 IP 地址在 network 命令指定的网段范围之内，接口不运行 OSPF 协议。
【举例】
指定运行 协议的接口的主 地址位于网段 131.108.20.0/24，接口所在的 区域\# OSPF IP OSPF ID为 2。
<Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] area 2 [Sysname-ospf-100-area-0.0.0.2] network 131.108.20.0 0.0.0.255【相关命令】
• ospf

##### 1.1.56 non-stop-routing

命令用来使能 协议的 功能。
non-stop-routing OSPF NSR命令用来关闭 协议的 功能。
undo non-stop-routing OSPF NSR

【命令】
non-stop-routing undo non-stop-routing【缺省情况】
OSPF 协议的 NSR 功能处于关闭状态。
【视图】
OSPF 视图【缺省用户角色】
network-admin【使用指导】
各个进程的 NSR 功能是相互独立的，只对本进程生效。如果存在多个 OSPF 进程，建议在各个进程下使能 OSPF NSR 功能。
OSPF NSR 特性与 OSPF GR 特性互斥，即 non-stop-routing 和 graceful-restart 命令互斥，不能同时配置。
【举例】
在 进程 中使能 功能。
\# OSPF 100 NSR <Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] non-stop-routing

##### 1.1.57 nssa (OSPF area view)

命令用来配置一个区域为 区域。
nssa NSSA命令用来恢复缺省情况。
undo nssa【命令】
nssa [ default-route-advertise [ cost cost-value | nssa-only | route-policy route-policy-name | type type ] * | no-import-route | no-summary | suppress-fa | [ [ [ translate-always ] [ translate-ignore-checking-backbone ] ] | translate-never ] | translator-stability-interval value ] * undo nssa [ default-route-advertise [ cost | nssa-only | route-policy | type ]
* | no-import-route | no-summary | suppress-fa | [ translate-always | translate-never ] | translator-stability-interval ] *【缺省情况】
没有区域被配置为 NSSA 区域。
【视图】
区域视图OSPF【缺省用户角色】
network-admin

【参数】
default-route-advertise：该参数只用于 NSSA 区域的 ABR 或 ASBR，配置后，对于 ABR，不论本地是否存在缺省路由，都将生成一条 Type-7 LSA 向区域内发布缺省路由；对于 ASBR，只有当本地存在缺省路由时，才产生 向区域内发布缺省路由。
Type-7 LSA cost-value：该缺省路由的度量值，取值范围为 0～16777214。如果未指定本参数，缺省cost路由的度量值将取 default cost 命令配置的值。
nssa-only：设置 Type-7 LSA 的 P 比特位不置位，即在对端路由器上不能转为 Type-5 LSA。缺省时，Type-7 LSA 的 P 比特位被置位，即在对端路由器上可以转为 Type-5 LSA（如果本地路由器是 ABR，则会检查骨干区域是否存在 FULL 状态的邻居，当 FULL 状态的邻居存在时，产生的 Type-7中 比特位不置位）。
LSA P route-policy-name：路由策略名，为 1～63 个字符的字符串，区分大小写。
route-policy只有当前路由器的路由表中存在缺省路由，并且有路由匹配 route-policy-name 指定的路由策略，才可以产生一个描述缺省路由的 Type-7 LSA 发布出去，指定的路由策略会影响 Type-7 LSA中的值。
type：该 Type-7 LSA 的类型，取值范围为 1～2，如果未指定本参数，Type-7 LSA 的缺省type类型将取 命令配置的值。
default type no-import-route：该参数用于禁止将 外部路由以 的形式引入到 区域中，AS Type-7 LSA NSSA这个参数通常只用在既是 NSSA 区域的 ABR，也是 OSPF 自治系统的 ASBR 的路由器上，以保证所有外部路由信息能正确地进入 OSPF 路由域。
no-summary：该参数只用于 NSSA 区域的 ABR，配置后，ABR 只通过 Type-3 LSA 向区域内发布一条缺省路由，不再向区域内发布任何其它 Type-3 LSA（这种区域又称为 Totally NSSA 区域）。
suppress-fa：指定当 Type-7 LSA 转换为 Type-5 LSA 时，生成的 Type-5 LSA 中的 Forwarding不生效。
Address translate-always：指定 为 区域的 转换为 的转换路由器。
ABR NSSA Type-7 LSA Type-5 LSA translate-ignore-checking-backbone：选举 区域的转换路由器时，不检查骨干区NSSA域是否存在 FULL 状态的邻居。
translate-never：指定 ABR 不能将 NSSA 区域的 Type-7 LSA 转换为 Type-5 LSA。
translator-stability-interval value：当有新的设备成为 NSSA 区域的 Type-7 LSA 转换为 Type-5 LSA 的转换路由器后，原 Type-7 LSA 转换为 Type-5 LSA 的转换路由器保持转换能力的时间。value 为保持时间，取值范围为 0～900，单位为秒，缺省值为 0，即不保持。
【使用指导】
如果要将一个区域配置成 区域，则该区域中的所有路由器都必须配置该命令。
NSSA当 区 域 存 在 多 个 时 ， 如 果 在 某 个 上 指 定 了NSSA ABR ABR translate-ignore-checking-backbone 参数，则需要在 NSSA 区域的其他 ABR 上做相同的配置，否则可能会出现没有 ABR 被选举为 NSSA 区域的转换路由器，或者多个 ABR 被选举为NSSA 区域的转换路由器的情况。
【举例】
将区域 配置成 区域。
\# 1 NSSA <Sysname> system-view [Sysname] ospf 100

[Sysname-ospf-100] area 1 [Sysname-ospf-100-area-0.0.0.1] nssa【相关命令】
• default-cost (OSPF area view)

##### 1.1.58 opaque-capability enable

opaque-capability enable 命令用来使能 OSPF 的 Opaque LSA 发布接收能力。
undo opaque-capability 命令用来关闭 OSPF 的 Opaque LSA 发布接收能力。
【命令】
opaque-capability enable undo opaque-capability【缺省情况】
OSPF 的 Opaque LSA 发布接收能力处于开启状态。
【视图】
视图OSPF【缺省用户角色】
network-admin【使用指导】
使能 OSPF 的 Opaque LSA 发布接收能力后，OSPF 可以发布接收 Type9 的 Opaque LSA，接收Type10 和 Type11 的 Opaque LSA。
【举例】
关闭 的 发布接收能力。
\# OSPF Opaque LSA <Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] undo opaque-capability

##### 1.1.59 ospf

命令用来启动 OSPF，并进入 OSPF 视图。
ospf命令用来关闭 OSPF。
undo ospf【命令】
ospf [ process-id | router-id router-id | vpn-instance vpn-instance-name ] * undo ospf [ process-id ]【缺省情况】
系统没有运行 OSPF 。
【视图】
系统视图

【缺省用户角色】
network-admin【参数】
process-id：OSPF 进程号，取值范围为 1～65535，缺省值为 1。
router-id：OSPF 进程使用的 Router ID，点分十进制形式。
router-id： 指 定 OSPF 进 程 所 属 的 VPN 实 例 。
vpn-instance vpn-instance-name表示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大vpn-instance-name小写。如果未指定本参数，则表示 OSPF 位于公网中。
【使用指导】
通过指定不同的进程号，可以在一台路由器上运行多个 OSPF 进程。这种情况下，建议使用命令中的 为不同进程指定不同的 Router ID。
router-id必须先启动 OSPF 进程才能配置相关参数。
对于已启动 OSPF 的 VLAN 接口，请不要将其与 OpenFlow 实例绑定，否则会影响 OSPF 邻居关系的建立。
【举例】
启动 进程 并配置 为 10.10.10.1。
\# OSPF 100 Router ID <Sysname> system-view [Sysname] ospf 100 router-id 10.10.10.1 [Sysname-ospf-100]

##### 1.1.60 ospf area

命令用来在接口上使能 OSPF。
ospf area命令用来在接口上关闭 OSPF。
undo ospf area【命令】
ospf process-id area area-id [ exclude-subip ] undo ospf process-id area [ exclude-subip ]【缺省情况】
接口上未使能 OSPF。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
process-id：OSPF 进程号，取值范围为 1～65535。
area-id：区域的标识，可以是十进制整数（取值范围为 0～4294967295，系统会将其转换成IP地址格式）或者是 IP 地址格式。
exclude-subip：不包含从 IP 地址。如果未指定本参数，则会包含从 IP 地址。

【使用指导】
接口配置优先，接口使能 OSPF 优于命令 network 的配置。
在接口上使能 OSPF 时，如果不存在进程和区域，则创建对应的进程和区域；在接口上关闭 OSPF时，不删除已经创建的进程和区域。
【举例】
配置接口 使能 进程 1，接口所在的 区域 为 2，不包含从 地\# Vlan-interface10 OSPF OSPF ID IP址。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospf 1 area 2 exclude-subip【相关命令】
• network

##### 1.1.61 ospf authentication-mode

ospf authentication-mode 命令用来设置接口对 OSPF 报文进行验证的验证模式及验证字。
undo ospf authentication-mode 命令用来删除接口下指定的验证模式。
【命令】
MD5/HMAC-MD5 验证模式：
ospf authentication-mode { hmac-md5 | md5 } key-id { cipher | plain } string undo ospf authentication-mode { hmac-md5 | md5 } key-id简单验证模式：
ospf authentication-mode simple { cipher | plain } string undo ospf authentication-mode simple keychain 验证模式：
ospf authentication-mode keychain keychain-name undo ospf authentication-mode keychain【缺省情况】
接口不对 OSPF 报文进行验证。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
hmac-md5：HMAC-MD5 验证模式。
md5：MD5 验证模式。
simple：简单验证模式。
key-id：验证字标识符，取值范围为 1～255。

cipher：以密文方式设置密钥。
plain：以明文方式设置密钥，该密钥将以密文形式存储。
string：密钥字符串，区分大小写。简单验证模式下，明文密钥为 1～8 个字符的字符串；密文密钥为 33～41 个字符的字符串。MD5/HMAC-MD5 验证模式下，明文密钥为 1～16 个字符的字符串；
密文密钥为 33～53 个字符的字符串。
keychain：使用 keychain 验证方式。
keychain-name：keychain 名称，为 1～63 个字符的字符串，区分大小写。
【使用指导】
同一网段的接口的验证字口令必须相同，可指定使用 MD5/HMAC-MD5 验证或简单验证两种方式，但不能同时指定；使用 MD5/HMAC-MD5 验证方式时，可配置多条 MD5/HMAC-MD5 验证命令，但 是唯一的，同一 只能配置一个验证字。
key-id key-id修改接口的 验证字的步骤如下：
OSPF MD5/HMAC-MD5首先在该接口配置新的 验证字；此时若邻居设备尚未配置新的
• MD5/HMAC-MD5 MD5/HMAC-MD5 验证字，便会触发 MD5/HMAC-MD5 验证平滑迁移过程。在这个过程中，OSPF 会发送分别携带各个 MD5/HMAC-MD5 验证字的多份报文，使得已配置新验证字的邻居设备和尚未配置新验证字的邻居设备都能通过验证，保持邻居关系。
• 然后在各个邻居设备上也都配置相同的新 MD5/HMAC-MD5 验证字；当设备上收到所有邻居的携带新验证字的报文后，便会退出 验证平滑迁移过程。
MD5/HMAC-MD5最后在本设备和所有邻居上都删除旧的 验证字；建议接口下不要保留多个
• MD5/HMAC-MD5 MD5/HMAC-MD5 验证字，每次 MD5/HMAC-MD5 验证字修改完毕后，应当及时删除旧的验证字，这样可以防止与持有旧验证字的系统继续通信、减少被攻击的可能，还可以减少验证迁移过程对系统、带宽的消耗。
在使能了 OSPF 的接口下使用 keychain 验证方式时，报文的收、发过程如下：
• OSPF 在发送报文前，会先从 keychain 获取当前的有效发送 key，根据该 key 的标识符、认证算法和认证密钥进行报文验证，如果当前不存在有效发送 key，或者该 的标识符大于key 255，OSPF 不会发送报文。
• OSPF 在收到报文后，会根据报文携带的 key 的标识符从 keychain 获取有效接收 key，根据该 key 的认证算法和认证密钥对报文进行校验。如果报文校验失败，或者根据报文中携带的key 的标识符无法从 keychain 中获取到有效接收 key，则该报文将被丢弃。
对于 keychain 认证算法和 key 的标识符的范围，OSPF 的支持情况如下：
• OSPF 仅支持 MD5、HMAC-MD5 和 HMAC-SM3 认证算法。
• OSPF 仅支持标识符取值范围为 0～255 的 key。
【举例】
\# 配置接口 Vlan-interface10 采用 MD5 明文验证模式，验证字标识符为 15，验证密钥为 123456。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospf authentication-mode md5 15 plain 123456 \# 配置接口 Vlan-interface10 采用简单明文验证模式，验证密钥为 123456。
<Sysname> system-view [Sysname] interface vlan-interface 10

[Sysname-Vlan-interface10] ospf authentication-mode simple plain 123456【相关命令】
•authentication-mode

##### 1.1.62 ospf bfd enable

命令用来使能 OSPF 的 BFD 功能。
ospf bfd enable命令用来关闭 OSPF 的 BFD 功能。
undo ospf bfd enable【命令】
ospf bfd enable [ echo ] undo ospf bfd enable【缺省情况】
的 功能处于关闭状态。
OSPF BFD【视图】
接口视图【缺省用户角色】
network-admin【参数】
echo：通过 BFD echo 报文方式实现 BFD 功能。如果不指定本参数，表示通过 BFD 控制报文方式实现 功能。
BFD【举例】
\# 使能接口 Vlan-interface11 的 OSPF BFD 功能。
<Sysname> system-view [Sysname] ospf [Sysname-ospf-1] area 0 [Sysname-ospf-1-area-0.0.0.0] network 192.168.0.0 0.0.255.255 [Sysname] interface vlan-interface 11 [Sysname-Vlan-interface11] ospf bfd enable

##### 1.1.63 ospf cost (Interface view)

命令用来配置接口运行 协议所需的开销。
ospf cost OSPF命令用来恢复缺省情况。
undo ospf cost【命令】
ospf cost cost-value undo ospf cost【缺省情况】
接口按照当前的带宽自动计算接口运行 OSPF 协议所需的开销。对于 Loopback 接口，缺省值为 0。

【视图】
接口视图【缺省用户角色】
network-admin【参数】
cost-value：接口运行 协议所需的开销，Loopback 接口的取值范围为 0～65535，其他接OSPF口的取值范围为 1～65535。
【使用指导】
本命令可用来手动设置接口的开销值，否则 OSPF 会按照当前的带宽自动计算接口运行 OSPF 协议所需的开销。
【举例】
指定接口 运行 协议的开销为 65。
\# Vlan-interface10 OSPF <Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospf cost 65【相关命令】
• bandwidth-reference

##### 1.1.64 ospf database-filter

命令用来对接口出方向的 进行过滤。
ospf database-filter LSA命令用来恢复缺省情况。
undo ospf database-filter【命令】
ospf database-filter { all | { ase [ acl ipv4-acl-number ] | nssa [ acl ipv4-acl-number ] | summary [ acl ipv4-acl-number ] } * } undo ospf database-filter【缺省情况】
不对接口出方向的 LSA 进行过滤。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
all：对接口出方向的所有 LSA（除了 Grace LSA）进行过滤。
ase ：对接口出方向的 Type-5 LSA 进行过滤。
nssa：对接口出方向的 Type-7 LSA 进行过滤。
summary：对接口出方向的 Type-3 LSA 进行过滤。

ipv4-acl-number：指定基本或高级 IPv4 ACL 编号用于过滤，ipv4-acl-number 的取值acl范围为 2000～3999。
【使用指导】
当配置的是高级 ACL（3000～3999）时，其使用规则如下：
• 使用命令 rule [ rule-id ] { deny | permit } ip source sour-addr来过滤携带指定链路状态 ID 的 LSA。
sour-wildcard
• 使用命令 rule [ rule-id ] { deny | permit } ip source sour-addr来过滤携带指定链路状态sour-wildcard destination dest-addr dest-wildcard和掩码的 LSA。
ID其中，source 用来过滤 的链路状态 ID，destination 用来过滤 的掩码，配置的掩码LSA LSA应该是连续的（当配置的掩码不连续时该过滤掩码的规则不生效）。
如果在配置该命令前邻居路由器就已经收到了将要进行过滤的 LSA，那么配置该命令后，这些 LSA仍存在于邻居路由器的 LSDB 中。
【举例】
\# 配置在接口 Vlan-interface10 上对出方向的所有 LSA 进行过滤。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospf database-filter all \# 根据编号为 2000、2100 和 2200 的 ACL 分别对接口 Vlan-interface20 出方向的 Type-5、Type-7和 进行过滤。
Type-3 LSA <Sysname> system-view [Sysname] interface vlan-interface 20 [Sysname- Vlan-interface20] ospf database-filter ase acl 2000 nssa acl 2100 summary acl 2200【相关命令】
• database-filter peer (OSPF view)

##### 1.1.65 ospf dr-priority

ospf dr-priority 命令用来设置接口的 DR 优先级。
命令用来恢复缺省情况。
undo ospf dr-priority【命令】
ospf dr-priority priority undo ospf dr-priority【缺省情况】
接口的 DR 优先级为 1。
【视图】
接口视图【缺省用户角色】
network-admin

【参数】
priority：接口的 DR 优先级，取值范围为 0～255。
【使用指导】
接口的 DR 优先级决定了该接口在选举 DR/BDR 时所具有的资格，数值越大，优先级越高。优先级高的在选举权发生冲突时被首先考虑。如果一台设备的优先级为 0，则它不会被选举为 或 BDR。
DR【举例】
\# 设置接口 Vlan-interface10 在选举 DR 时的优先级为 8。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospf dr-priority 8

##### 1.1.66 ospf fast-reroute lfa-backup

命令用来使能接口参与 LFA（Loop Alternate）计算。
ospf fast-reroute lfa-backup Free命令用来禁止接口参与 计算。
undo ospf fast-reroute lfa-backup LFA【命令】
ospf fast-reroute lfa-backup undo ospf fast-reroute lfa-backup【缺省情况】
接口参与 LFA 计算，能够被选为备份接口。
【视图】
接口视图【缺省用户角色】
network-admin【使用指导】
接口使能 LFA 计算，使其有资格成为备份接口。去使能此配置后，则接口不会被选为备份接口。
【举例】
\# 禁止接口 Vlan-interface11 参与 LFA 计算。
<Sysname> system-view [Sysname] interface vlan-interface 11 [Sysname-Vlan-interface11] undo ospf fast-reroute lfa-backup

##### 1.1.67 ospf lsu-flood-control

ospf lsu-flood-control 命令用来开启 OSPF 限制 LSU 发送速率功能。
undo ospf lsu-flood-control 命令用来关闭 OSPF 限制 LSU 发送速率功能。
【命令】
ospf lsu-flood-control [ interval count ] undo ospf lsu-flood-control

【缺省情况】
OSPF 不对 LSU 的发送速率进行限制。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
interval：OSPF 发送 LSU 的时间间隔，取值范围为 10～1000，单位为毫秒，缺省值为 30。
count：OSPF 一次发送 的最大个数，取值范围为 1～1000，缺省值为 50。
LSU【使用指导】
在与邻居进行 LSDB 同步的过程中，当 OSPF 需要发送的 LSU 较多时（比如本地设备与数量较多的设备建立 OSPF 邻居关系），邻居设备会在短时间内收到大量的 LSU。邻居设备忙于处理这些突发的大量报文时，有可能将维持邻居关系的 报文丢弃，从而导致邻居关系断开。邻居关系断Hello开后，重新建立邻居关系的过程中，需要交互的 LSU 数量将会更大，上述情况会进一步恶化。
配置本命令后，在指定的时间间隔内，所有运行 OSPF 的接口发送 LSU 的最大个数不能超过限定值，即对整机发送 LSU 的速率进行限制，从而避免上述情况的发生。
调整 OSPF 对 LSU 的发送速率时，如果配置不当可能会造成路由异常等情况，请谨慎配置。通常情况下，建议使用缺省值。
【举例】
开启 限制 发送速率功能，配置 发送 的时间间隔为 毫秒，一次最多发\# OSPF LSU OSPF LSU 40送 60 个 LSU 报文。
<Sysname> system-view [Sysname] ospf lsu-flood-control 40 60

##### 1.1.68 ospf mib-binding

ospf mib-binding 命令用来配置 OSPF 进程绑定公有 MIB。
undo ospf mib-binding 命令用来恢复缺省情况。
【命令】
ospf mib-binding process-id undo ospf mib-binding【缺省情况】
MIB 绑定在进程号最小的 OSPF 进程上。
【视图】
系统视图【缺省用户角色】
network-admin

【参数】
process-id：OSPF 进程号，取值范围为 1～65535。
【使用指导】
该命令用来配置 OSPF进程绑定 MIB，用户可通过 RFC4750-OSPF.MIB 文件来读取被绑定的 OSPF进程的相关信息。对于 的私有 MIB，不管是否配置此命令，均可读取所有 进程的Comware OSPF相关信息。
如果指定的 process-id 不存在，配置 OSPF 进程绑定命令时将会提示 OSPF 进程不存在，无法完成配置。
如果配置了 OSPF 进程绑定 MIB，若删除 process-id 对应的 OSPF 进程，则同时删除 OSPF 进程绑定 MIB 配置，MIB 绑定到进程号最小的 OSPF 进程上。
【举例】
配置 进程 绑定 MIB。
\# OSPF 100 <Sysname> system-view [Sysname] ospf mib-binding 100

##### 1.1.69 ospf mtu-enable

ospf mtu-enable 命令用来配置 DD 报文中 MTU 域的值为发送该报文接口的 MTU 值。
命令用来恢复缺省情况。
undo ospf mtu-enable【命令】
ospf mtu-enable undo ospf mtu-enable【缺省情况】
接口发送的 DD 报文中 MTU 域的值为 0。
【视图】
接口视图【缺省用户角色】
network-admin【使用指导】
通过 Tunnel 建立虚连接后，不同厂商的设备接口发送的 DD 报文中 MTU 域的缺省值可能不同，为了保证一致，应该将接口发送的 DD 报文中 MTU 域的值恢复为缺省值 0。
当配置了该命令后，接收到 DD 报文时会检查报文中的 MTU 值是否大于接收接口的 MTU 值，如果大于则将报文丢弃。
【举例】
指定接口 在发送 报文时，填写 值域。
\# Vlan-interface10 DD MTU <Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospf mtu-enable

##### 1.1.70 ospf network-type

ospf network-type 命令用来配置 OSPF 接口的网络类型。
undo ospf network-type 命令用来恢复为缺省情况。
【命令】
ospf network-type { broadcast | nbma | p2mp [ unicast ] | p2p [ peer-address-check ] } undo ospf network-type【缺省情况】
接口网络类型的缺省值为广播类型。
OSPF【视图】
接口视图【缺省用户角色】
network-admin【参数】
broadcast：配置接口的网络类型为广播类型。
nbma：配置接口的网络类型为 NBMA 类型。
p2mp：配置接口的网络类型为点到多点类型。
unicast：P2MP 类型支持单播发送报文，缺省情况下是组播方式发送报文。
p2p：配置接口的网络类型为点到点类型。
peer-address-check：配置建立邻接关系必须在同一网段的检查功能，即在接收 Hello 报文时，对端的 IP 地址与当前接口必须在同一网段。
【使用指导】
如果在广播网络上有不支持组播地址的路由器，可以将接口的网络类型改为 NBMA。
接口的网络类型为 或 P2MP（unicast）时，必须使用 命令来配置邻接点。
NBMA peer如果一网段内只有两台路由器运行 协议，也可以将接口的网络类型改为点到点。
OSPF接口的网络类型为 P2MP（unicast）时，OSPF 协议在该接口上发送的报文均为单播报文。
【举例】
\# 将接口 Vlan-interface10 设置为 NBMA 类型。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospf network-type nbma【相关命令】
• ospf dr-priority

##### 1.1.71 ospf packet-size

ospf packet-size 命令用来配置接口发送 OSPF 报文的最大长度。
undo ospf packet-size 命令用来恢复缺省情况。

【命令】
ospf packet-size value undo ospf packet-size【缺省情况】
接口发送 OSPF 报文的最大长度为本接口的 IP MTU 值。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
value：配置接口发送 OSPF 报文的最大长度，取值范围为 500～10000，单位为字节。
【使用指导】
接口取 ospf packet-size 配置值和本接口 IP MTU 中的较小值作为发送 OSPF 报文的最大长度。
本命令用于需要对接口发送OSPF报文的大小进行限制的场景。例如，通过隧道建立OSPF邻居时，为避免隧道口发送的 OSPF 报文分片，可用此命令在隧道口上设置 OSPF 报文的最大长度，保证报文的最大长度+封装报文头长度≤出接口的 MTU。关于隧道的详细介绍请参见“三层技OSPF IP术-IP 业务配置指导”中的“隧道”。
【举例】
\# 配置接口 Vlan-interface10 发送 OSPF 报文的最大长度为 1000 字节。
<Sysname> system-view [Sysname] interface vlan 10 [Sysname-Vlan-interface10] ospf packet-size 1000

##### 1.1.72 ospf prefix-suppression

ospf prefix-suppression 命令用来抑制接口进行前缀发布。
undo ospf prefix-suppression 命令用来恢复缺省情况。
【命令】
ospf prefix-suppression [ disable ] undo ospf prefix-suppression【缺省情况】
不抑制接口进行前缀发布。
【视图】
接口视图【缺省用户角色】
network-admin

【参数】
disable：不抑制接口进行前缀发布。
【使用指导】
如果 OSPF 进程配置了抑制前缀发布，但某个接口不想进行抑制，此时可以配置本命令并指定参数。
disable接口配置不能抑制从地址对应的前缀。
具体内容请参见命令 中的使用指导。
prefix-suppression【举例】
抑制接口 进行前缀发布。
\# Vlan-interface10 <Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospf prefix-suppression【相关命令】
• prefix-suppression

##### 1.1.73 ospf primary-path-detect bfd

ospf primary-path-detect bfd 命令用来使能 OSPF 协议中主用链路的 BFD 检测功能。
undo ospf primary-path-detect bfd 命令用来关闭 OSPF 协议中主用链路的 BFD 检测功能。
【命令】
ospf primary-path-detect bfd { ctrl | echo } undo ospf primary-path-detect bfd【缺省情况】
协议中主用链路的 检测功能处于关闭状态。
OSPF BFD【视图】
接口视图【缺省用户角色】
network-admin【参数】
ctrl：配置通过工作于控制报文方式的 BFD 会话对主用链路进行检测。
echo：配置通过工作于 echo 报文方式的 BFD 会话对主用链路进行检测。
【使用指导】
配置本功能后，OSPF 协议的快速重路由特性和 PIC 特性中的主用链路将使用 BFD 进行检测。
【举例】
在接口 上配置 协议快速重路由特性中主用链路使能 BFD（Ctrl 方式）检\# Vlan-interface10 OSPF测功能。
<Sysname> system-view

[Sysname] ospf 1 [Sysname-ospf-1] fast-reroute lfa [Sysname-ospf-1] quit [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospf primary-path-detect bfd ctrl \# 在接口 Vlan-interface11 上配置 OSPF 协议 PIC 特性中主用链路使能 BFD（Echo 方式）检测功能。
<Sysname> system-view [Sysname] ospf 1 [Sysname-ospf-1] pic additional-path-always [Sysname-ospf-1] quit [Sysname] bfd echo-source-ip 1.1.1.1 [Sysname] interface vlan-interface 11 [Sysname-Vlan-interface11] ospf primary-path-detect bfd echo

##### 1.1.74 ospf timer dead

命令用来设置 的邻居失效时间。
ospf timer dead OSPF命令用来恢复缺省情况。
undo ospf timer dead【命令】
ospf timer dead seconds undo ospf timer dead【缺省情况】
P2P、Broadcast 类型接口的 OSPF 邻居失效的时间为 40 秒；P2MP、NBMA 类型接口的 OSPF邻居失效的时间为 120 秒。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
seconds：OSPF 邻居失效的时间，取值范围为 1～2147483647，单位为秒。
【使用指导】
OSPF 邻居的失效时间是指：在该时间间隔内，若未收到邻居的 Hello 报文，就认为该邻居已失效。
值至少应为 值的 4 倍，同一网段上的接口的 也dead seconds hello seconds dead seconds必须相同。
【举例】
\# 配置接口 Vlan-interface10 上的邻居失效时间为 60 秒。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospf timer dead 60

【相关命令】
• ospf timer hello

##### 1.1.75 ospf timer hello

ospf timer hello 命令用来配置接口发送 Hello 报文的时间间隔。
undo ospf timer hello 命令用来恢复缺省情况。
【命令】
ospf timer hello seconds undo ospf timer hello【缺省情况】
P2P、Broadcast 类型接口发送 Hello 报文的时间间隔为 10 秒；P2MP、NBMA 类型接口发送 Hello报文的时间间隔为 秒。
30【视图】
接口视图【缺省用户角色】
network-admin【参数】
seconds：接口发送 Hello 报文的时间间隔，取值范围为 1～65535，单位为秒。
【使用指导】
的值越小，发现网络拓扑改变的速度越快，对系统资源的开销也就越大。同一网段上的seconds接口的 seconds 必须相同。
【举例】
\# 配置接口 Vlan-interface10 发送 Hello 报文的时间间隔为 20 秒。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospf timer hello 20【相关命令】
•ospf timer dead

##### 1.1.76 ospf timer poll

ospf timer poll 命令用来配置在 NBMA 接口上向状态为 down 的邻居路由器发送轮询 Hello 报文的时间间隔。
命令用来恢复缺省情况。
undo ospf timer poll【命令】
ospf timer poll seconds undo ospf timer poll

【缺省情况】
在 NBMA 接口上向状态为 down 的邻居路由器发送轮询 Hello 报文的时间间隔为 120 秒。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
seconds：向状态为 down 的邻居路由器发送轮询 Hello 报文的时间间隔，取值范围为 1～2147483647，单位为秒。
【使用指导】
在 NBMA 的网络上，当邻居失效后，将按轮询时间间隔定期地发送 Hello 报文。用户可配置轮询时间间隔以指定该接口在与相邻路由器构成邻居关系之前发送 报文的时间间隔。
Hello发送轮询 报文的时间间隔至少应为发送 报文时间间隔的 倍。
Hello Hello 4【举例】
\# 配置接口上 Vlan-interface10 发送轮询 Hello 报文的时间间隔为 130 秒。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospf timer poll 130【相关命令】
• ospf timer hello

##### 1.1.77 ospf timer retransmit

ospf timer retransmit 命令用来配置接口重传 LSA 的时间间隔。
undo ospf timer retransmit 命令用来恢复缺省情况。
【命令】
ospf timer retransmit seconds undo ospf timer retransmit【缺省情况】
接口重传 LSA 的时间间隔为 5 秒。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
seconds：接口重传 LSA 的时间间隔，取值范围为 1～3600，单位为秒。

【使用指导】
当一台路由器向它的邻居发送一条 LSA 后，需要等到对方的确认报文。若在该重传 LSA 的时间间隔内未收到对方的确认报文，就会重传这条 LSA。
请合理配置接口重传 LSA 的时间间隔，避免引起不必要的重传。比如，对于低速链路，可以适当把这个时间间隔值设置大一点。
【举例】
\# 指定接口 Vlan-interface10 与邻接路由器之间传送 LSA 的重传间隔为 8 秒。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospf timer retransmit 8

##### 1.1.78 ospf trans-delay

命令用来配置接口对 的传输延迟时间。
ospf trans-delay LSA命令用来恢复缺省情况。
undo ospf trans-delay【命令】
ospf trans-delay seconds undo ospf trans-delay【缺省情况】
接口对 LSA 的传输延迟时间为 1 秒。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
seconds：接口对 LSA 的传输延迟时间，取值范围为 1～3600，单位为秒。
【使用指导】
LSA 在本路由器的 LSDB 中会随时间老化（LSA 的老化时间每秒钟加 1），但在网络的传输过程中却不会，所以有必要在发送之前在 LSA 的老化时间上增加一定的延迟时间。此配置对低速率的网络尤其重要。
【举例】
\# 指定接口 Vlan-interface10 上传送 LSA 的时延值为 3 秒。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospf trans-delay 3

##### 1.1.79 ospf ttl-security

命令用来开启接口的 功能。
ospf ttl-security OSPF GTSM命令用来关闭接口的 功能。
undo ospf ttl-security OSPF GTSM

【命令】
ospf ttl-security [ hops hop-count | disable ] undo ospf ttl-security【缺省情况】
接口的 OSPF GTSM 功能处于关闭状态。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
hops hop-count：指定接口收到 OSPF 报文并进行安全检测时，允许接收到的报文所经过的路由器的最大跳数。hop-count 表示最大跳数，取值范围为 1～254，如果未指定本参数，对于 OSPF普通邻居，缺省值为 1；对于 虚连接邻居，缺省值为 255。
OSPF disable：关闭接口的 GTSM 功能。
【使用指导】
开启 报文的 功能后。当设备在接口上收到 报文时，会判断报文的 是否在OSPF GTSM OSPF TTL 255-“hop-count”+1 到 255 之间。如果在，就上送报文；否则直接丢弃报文。从而使设备能够避免受到 CPU 利用（CPU-utilization）类型的攻击（如 CPU 过载），增强系统的安全性。
执行本命令后，设备会将发送报文的初始 TTL 设置为 255，这就要求本地设备和邻居设备上同时配置本特性，指定的 值可以不同，只要能够通过安全检测即可。
hop-count在接口视图下配置的 参数比在 OSPF 区域视图下配置的 参数的优先级高。
hops hops OSPF 区域视图下未开启 GTSM 时，undo 命令用来关闭接口的 GTSM 功ospf ttl-security能。OSPF 区域视图下已开启 时，undo 命令用来取消接口下的GTSM ospf ttl-security GTSM配置，并使区域下的 GTSM 配置在接口上生效；ospf ttl-security disable 命令用来关闭接口的 GTSM 功能。
如果区域中配置了虚连接，建议用户只在区域视图下开启 GTSM 功能，当且仅当用户已经明确知道哪些接口是用来发送和接收虚连接的 报文时，可以在所有这些接口下开启 的OSPF OSPF GTSM功能，否则可能会导致虚连接两端的路由器丢弃接收到的 OSPF 报文。
【举例】
\# 开启接口 Vlan-interface10 的 GTSM 功能，并指定最大跳数为 254。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospf ttl-security hops 254 \# 在区域视图下开启 OSPF 报文的 GTSM 功能，再在接口 Vlan-interface10 下关闭 OSPF 报文的GTSM 功能。
<Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] area 1 [Sysname-ospf-100-area-0.0.0.1] ttl-security

[Sysname-ospf-100-area-0.0.0.1] quit [Sysname-ospf-100] quit [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospf ttl-security disable【相关命令】
• (OSPF area view)
ttl-security

##### 1.1.80 peer (OSPF view)

命令用来配置 NBMA 网络或 P2MP 单播网络的邻居。
peer命令用来删除指定的 NBMA 网络或 P2MP 单播网络的邻居。
undo peer【命令】
peer ip-address [ cost cost-value | dr-priority priority ] undo peer ip-address【缺省情况】
未配置邻居。
【视图】
OSPF 视图【缺省用户角色】
network-admin【参数】
ip-address：邻居的 IP 地址。
cost-value：邻居的开销值，取值范围为 1～65535。
cost priority：邻居的优先级，取值范围为 0～255，缺省值为 1。
dr-priority【使用指导】
NBMA 网络或 P2MP 单播网络采用单播形式发送协议报文，必须手工指定邻居。
本命令设置的开销值仅用于 P2MP 链路上建立的邻居，如果没有配置开销值，去往该邻居的花费等于接口的开销值。
本命令设置的优先级仅用于表示路由器是否主动向该邻居发送 报文，并不用于实际的 选Hello DR举，ospf dr-priority 命令设置的优先级用于实际的 DR 选举。
【举例】
\# 指定邻居的 IP 地址为 1.1.1.1。
<Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] peer 1.1.1.1【相关命令】
•ospf dr-priority

##### 1.1.81 pic (OSPF view)

pic 命令用来使能前缀无关收敛功能。
undo pic 命令用来关闭前缀无关收敛功能。
【命令】
pic [ additional-path-always ] undo pic【缺省情况】
前缀无关收敛功能处于使能状态。
【视图】
视图OSPF【缺省用户角色】
network-admin【参数】
additional-path-always：支持非直连的次优路由作为备份。
【使用指导】
PIC（Prefix Independent Convergence，前缀无关收敛），即收敛时间与前缀数量无关，加快收敛速度。传统的路由计算快速收敛都与前缀数量相关，收敛时间与前缀数量成正比。OSPF 只实现区域间路由以及外部路由的前缀无关收敛。
OSPF 快速重路由功能和 PIC 同时配置时，OSPF 快速重路由功能生效。
【举例】
\# 使能 OSPF 协议的 PIC 支持非直连次优路由做备份功能。
<Sysname> system-view [Sysname] ospf 1 [Sysname-ospf-1] pic additional-path-always

##### 1.1.82 preference (OSPF view)

preference 命令用来配置 OSPF 协议的路由优先级。
undo preference 命令用来取消 OSPF 协议的路由优先级的配置。
【命令】
preference [ ase ] { preference | route-policy route-policy-name } * undo preference [ ase ]【缺省情况】
对于自治系统内部路由，OSPF 协议的路由优先级为 10；对于自治系统外部路由，OSPF 协议的路由优先级为 150。
【视图】
OSPF 视图

【缺省用户角色】
network-admin【参数】
ase：配置 OSPF 协议对自治系统外部路由的优先级。如果未指定该参数，则配置的是 OSPF 协议对自治系统内部路由的优先级。
preference：OSPF 协议的路由优先级，取值范围为 1～255。优先级的值越小，其实际的优先程度越高。
route-policy route-policy-name ： 应 用 路 由 策 略 ， 对 特 定 的 路 由 设 置 优 先 级 。
route-policy-name 是路由策略名称，为 1～63 个字符的字符串，区分大小写。
【使用指导】
由于路由器上可能同时运行多个动态路由协议，就存在各个路由协议之间路由信息共享和选择的问题，所以为每一种路由协议指定了一个缺省的优先级。在不同的路由协议发现去往同一目的地的多条路由时，优先级高的协议发现的路由将被选中以转发 IP 报文。
配置了 route-policy 参数后，如果 route-policy 中对某些匹配的路由优先级进行了修改，则这些匹配的路由取 route-policy 修改的优先级，其它路由的优先级均取 preference 命令所设的值。
【举例】
配置 协议对自治系统外部路由的优先级为 200。
\# OSPF <Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] preference ase 200配置 协议对自治系统内部路由的优先级，匹配路由策略 的路由优先级为 100，未匹配\# OSPF pre的路由优先级为 150。
<Sysname> system-view [Sysname] ip prefix-list test index 10 permit 100.1.1.0 24 [Sysname] route-policy pre permit node 10 [Sysname-route-policy-pre-10] if-match ip address prefix-list test [Sysname-route-policy-pre-10] apply preference 100 [Sysname-route-policy-pre-10] quit [Sysname] ospf 100 [Sysname-ospf-100] preference route-policy pre 150

##### 1.1.83 prefix-priority (OSPF view)

prefix-priority 命令用来使能 OSPF 的前缀按优先权快速收敛功能。
undo prefix-priority 命令用来关闭 OSPF 的前缀按优先权快速收敛功能。
【命令】
prefix-priority route-policy route-policy-name undo prefix-priority【缺省情况】
OSPF 的前缀按优先权快速收敛功能处于关闭状态。

【视图】
OSPF 视图【缺省用户角色】
network-admin【参数】
route-policy-name：应用路由策略，对特定的路由前缀设置优先权。
route-policy route-policy-name 是路由策略名称，为 1～63 个字符的字符串，区分大小写。
【使用指导】
通过策略指定优先权，不同前缀按优先权顺序下发，由高到低分为 4 个优先权（Critical、High、Medium 和 Low），如果一条路由符合多个收敛优先权的匹配规则，则这些收敛优先权中最高者当选为路由的收敛优先权。
路由的 位主机路由为 优先权，其它为 优先权。
OSPF 32 Medium Low【举例】
\# 配置通过路由策略 pre 修改特定路由前缀的优先权为 Medium。
<Sysname> system-view [Sysname] ip prefix-list test index 10 permit 100.1.1.0 24 [Sysname] route-policy pre permit node 10 [Sysname-route-policy-pre-10] if-match ip address prefix-list test [Sysname-route-policy-pre-10] apply prefix-priority medium [Sysname-route-policy-pre-10] quit [Sysname] ospf 100 [Sysname-ospf-100] prefix-priority route-policy pre

##### 1.1.84 prefix-suppression

prefix-suppression 命令用来抑制 OSPF 进程进行前缀发布。
undo prefix-suppression 命令用来恢复缺省情况。
【命令】
prefix-suppression undo prefix-suppression【缺省情况】
不抑制 OSPF 进程进行前缀发布。
【视图】
视图OSPF【缺省用户角色】
network-admin

【使用指导】
OSPF 使能网段时会将接口上匹配该网段的所有网段路由与主机路由都通过 LSA 发布，但有时候主机路由或网段路由是不希望被发布的。通过前缀抑制配置，可以减少 LSA 中携带不需要的前缀，即不发布某些网段路由和主机路由，从而提高网络安全性，加快路由收敛。
如果需要抑制前缀发布，建议整个 网络都配置本命令。
OSPF全局配置不能抑制从地址、LoopBack 接口以及处于抑制状态的接口对应的前缀。如果想对LoopBack 接 口 或 处 于 抑 制 状 态 的 接 口 进 行 抑 制 ， 可 以 通 过 配 置 接 口 前 缀 抑 制 （ ospf prefix-suppression 命令）来实现。
当使能前缀抑制时，具体情况如下：
• P2P 或 P2MP 类型网络：Type-1 LSA 中不发布接口的主地址，即 Type-1 LSA 中链路类型为3 的 Stub 链路被抑制，不生成接口路由，但其他路由信息可以正常计算，不会影响流量转发。
• 广播类型或者 NBMA 网络：DR 发布的 Type-2 LSA 的掩码字段会填成 32 位，即不生成网段路由，但其他路由信息可以正常计算，不会影响流量转发。另外，如果没有邻居，发布的Type-1 LSA 中也不发布接口的主地址，即 Type-1 LSA 中链路类型为 3 的 Stub 链路被抑制。
【举例】
\# 抑制 OSPF 进程 1 的前缀发布。
<Sysname> system-view [Sysname] ospf 1 [Sysname-ospf-1] prefix-suppression【相关命令】
• ospf prefix-suppression

##### 1.1.85 reset ospf event-log

reset ospf event-log 命令用于清除 OSPF 的日志信息。
【命令】
reset ospf [ process-id ] event-log [ lsa-flush | peer | spf ]【视图】
用户视图【缺省用户角色】
network-admin【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果未指定本参数，则清除所有 OSPF 进程的日志信息。
lsa-flush：LSA 老化日志信息个数。
peer：清除邻居的日志信息。
spf：清除路由计算的日志信息。
【使用指导】
如果未指定日志类型，则所有日志信息都被清除。

【举例】
\# 清除所有 OSPF 进程路由计算的日志信息。
<Sysname> reset ospf event-log spf【相关命令】
• display ospf event-log

##### 1.1.86 reset ospf process

reset ospf process 命令用来重启 OSPF 进程。
【命令】
reset ospf [ process-id ] process [ graceful-restart ]【视图】
用户视图【缺省用户角色】
network-admin【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果不指定该参数，则重启所有的 OSPF进程。
graceful-restart：以 GR 方式重启 OSPF 进程。
【使用指导】
使用 命令重启 OSPF，可以获得如下结果：
reset ospf process
• 可以立即清除无效的 LSA，而不必等到 LSA 超时。
• 如果改变了 Router ID，该命令的执行会导致新的 Router ID 生效。
• 方便重新选举 DR、BDR。
• 重启前的 OSPF 配置不会丢失。
执行该命令后，系统提示用户确认是否重启 OSPF 协议。
【举例】
\# 重启所有 OSPF 进程。
<Sysname> reset ospf process Reset OSPF process? [Y/N]:y

##### 1.1.87 reset ospf redistribution

命令用来重新向 OSPF 引入外部路由。
reset ospf redistribution【命令】
reset ospf [ process-id ] redistribution【视图】
用户视图

【缺省用户角色】
network-admin【参数】
process-id：OSPF 进程号，取值范围为 1～65535。如果不指定本参数，则所有 OSPF 进程都将重新引入外部路由。
【举例】
\# 重新向 OSPF 引入外部路由。
<Sysname> reset ospf redistribution

##### 1.1.88 reset ospf statistics

命令用来清除 OSPF 的统计信息。
reset ospf statistics【命令】
reset ospf [ process-id ] statistics【视图】
用户视图【缺省用户角色】
network-admin【参数】
process-id：OSPF 进程号，取值范围为 1～65535，清除指定 OSPF 进程的统计信息。
【举例】
清除所有 进程的统计信息。
\# OSPF <Sysname> reset ospf statistics【相关命令】
•display ospf statistics

##### 1.1.89 rfc1583 compatible

命令用来开启兼容 RFC 1583 的路由选择优先规则的功能。
rfc1583 compatible命令用来关闭兼容 RFC 1583 的路由选择优先规则的功能。
undo rfc1583 compatible【命令】
rfc1583 compatible undo rfc1583 compatible【缺省情况】
兼容 的路由选择优先规则的功能处于开启状态。
RFC 1583【视图】
OSPF 视图

【缺省用户角色】
network-admin【使用指导】
当有多条路径可以到达同一个外部路由时，在选择最优路由的问题上，RFC 2328 中定义的选路规则与 的有所不同，进行此配置可以兼容 中定义的规则。
RFC 1583 RFC 1583具体的选路规则如下：
当 兼容 时，所有到达 的路由优先级相同。当 不兼容
(1) RFC 2328 RFC 1583 ASBR RFC 2328 RFC 1583 时，非骨干区的区域内路由优先级最高，区域间路由与骨干区区域内路由优先级相同，优选非骨干区的区域内路由，尽量减少骨干区的负担；
(2) 若存在多条优先级相同的路由时，按开销值优选，优选开销值小的路由；
(3) 若存在多条开销值相同路由时，按路由来源区域的区域 ID 选择，优选区域 ID 大的路由。
为了避免路由环路，同一路由域内的路由器建议统一配置相同规则。
【举例】
\# 关闭兼容 RFC 1583 的路由选择规则的功能。
<Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] undo rfc1583 compatible

##### 1.1.90 router id

router id 命令用来配置全局 Router ID。
undo router id 命令用来恢复缺省情况。
【命令】
router id router-id undo router id【缺省情况】
未配置全局 Router ID。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
router-id：IPv4 地址形式的 Router ID。
【使用指导】
一些动态路由协议要求使用 Router ID ，如果在启动这些路由协议时没有指定 Router ID ，则缺省使用全局路由器 ID。
如果配置了全局路由器 ID，则使用配置的值作为 ID。如果没有配置全局路由器 ID，则按照Router下面的规则进行选择：

(1) 如果存在配置 IP 地址的 Loopback 接口，则选择 Loopback 接口地址中最大的作为 Router
ID。
如果没有配置 地址的 接口，则从其他接口的 IP地址中选择最大的作为
(2) IP Loopback Router ID
（不考虑接口的 up/down 状态）。
存在主备的情况下，系统将备份命令行配置的 Router ID 或从接口地址中选择出来的 Router ID。主
备倒换后，系统将检查从地址中选出的 Router ID 的有效性，如果无效将重新进行选择。
当且仅当被选为 Router ID 的接口 IP 地址被删除或被修改时，才触发重新选择过程，其他情况不触
发重新选择的过程。例如，以下情况不会触发 Router ID 重新选择的过程：
接口 down。
•
• 已经选取了一个非 Loopback 接口地址后又配置了一个 Loopback 接口地址。
• 配置一个更大的接口地址。
Router ID 改变之后，各协议需要通过手工执行 命令才会获取新的 Router ID。
reset
【举例】
\# 配置全局 Router ID 为 1.1.1.1。
<Sysname> system-view
[Sysname] router id 1.1.1.1

##### 1.1.91 silent-interface (OSPF view)

命令用来禁止接口收发 报文。
silent-interface OSPF命令用来取消禁止接口收发 报文的配置。
undo silent-interface OSPF【命令】
silent-interface { interface-type interface-number | all } undo silent-interface { interface-type interface-number | all }【缺省情况】
允许接口收发 OSPF 报文。
【视图】
OSPF 视图【缺省用户角色】
network-admin【参数】
interface-type interface-number：接口类型和接口号，禁止指定 OSPF 接口收发 OSPF报文。
all：禁止所有 OSPF 接口收发 OSPF 报文。
【使用指导】
如果要使 OSPF 路由信息不被某一网络中的路由器获得，可使用本命令禁止在此接口上收发 OSPF报文。

【举例】
\# 禁止接口 Vlan-interface10 收发 OSPF 报文。
<Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] silent-interface vlan-interface 10

##### 1.1.92 snmp trap rate-limit

snmp trap rate-limit 命令用来配置 OSPF 在指定时间间隔内允许输出的告警信息条数。
undo snmp trap rate-limit 命令用来恢复缺省情况。
【命令】
snmp trap rate-limit interval trap-interval count trap-number undo snmp trap rate-limit【缺省情况】
OSPF 在 10 秒内允许输出 7 条告警信息。
【视图】
视图OSPF【缺省用户角色】
network-admin【参数】
interval trap-interval：指定允许输出告警信息的时间间隔，取值范围为 2～60，单位为秒。
count trap-number：在指定时间间隔内允许输出的告警信息条数，取值范围为 0～300，为 0时表示不输出告警信息。
【举例】
\# 配置 OSPF 在 5 秒内允许输出 10 条告警信息。
<Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] snmp trap rate-limit interval 5 count 10

##### 1.1.93 snmp-agent trap enable ospf

命令用来开启 OSPF 的告警功能。
snmp-agent trap enable ospf命令用来关闭 OSPF 的告警功能。
undo snmp-agent trap enable ospf【命令】
snmp-agent trap enable ospf [ authentication-failure | bad-packet | config-error | grhelper-status-change | grrestarter-status-change | if-state-change | lsa-maxage | lsa-originate | lsdb-approaching-overflow | lsdb-overflow | neighbor-state-change | nssatranslator-status-change | retransmit | virt-authentication-failure | virt-bad-packet |

virt-config-error | virt-retransmit | virtgrhelper-status-change | virtif-state-change | virtneighbor-state-change ] * undo snmp-agent trap enable ospf [ authentication-failure | bad-packet | config-error | grhelper-status-change | grrestarter-status-change | if-state-change | lsa-maxage | lsa-originate | lsdb-approaching-overflow | lsdb-overflow | neighbor-state-change | nssatranslator-status-change | retransmit | virt-authentication-failure | virt-bad-packet | virt-config-error | virt-retransmit | virtgrhelper-status-change | virtif-state-change | virtneighbor-state-change ] *【缺省情况】
的告警功能处于开启状态。
OSPF【视图】
系统视图【缺省用户角色】
network-admin【参数】
authentication-failure：接口认证失败。
bad-packet：接收了错误报文。
config-error：接口配置错误。
grhelper-status-change：邻居 GR Helper 状态变化。
grrestarter-status-change：GR Restarter 状态变化。
if-state-change：接口状态变化。
lsa-maxage：LSA 的 max age。
lsa-originate：本地生成 LSA。
lsdb-approaching-overflow：LSDB 接近溢出。
lsdb-overflow：LSDB 溢出。
neighbor-state-change：邻居状态变化。
nssatranslator-status-change：NSSA 转换路由器状态变化。
retransmit：接口接收和转发报文。
virt-authentication-failure：虚接口认证失败。
virt-bad-packet：虚接口接收错误报文。
virt-config-error：虚接口配置错误。
virt-retransmit：虚接口接收和转发报文。
virtgrhelper-status-change：虚接口邻居 GR Helper 状态变化。
virtif-state-change：虚接口状态变化。
virtneighbor-state-change：虚接口邻居状态变化。
【举例】
关闭 的告警功能。
\# OSPF

<Sysname> system-view [Sysname] undo snmp-agent trap enable ospf

##### 1.1.94 spf-schedule-interval (OSPF view)

命令用来配置 路由计算的时间间隔。
spf-schedule-interval OSPF命令用来恢复缺省情况。
undo spf-schedule-interval【命令】
spf-schedule-interval maximum-interval [ minimum-interval [ incremental-interval ] ] undo spf-schedule-interval【缺省情况】
OSPF 路由计算的最大时间间隔为 5 秒，最小时间间隔为 50 毫秒，时间间隔惩罚增量为 200 毫秒。
【视图】
视图OSPF【缺省用户角色】
network-admin【参数】
maximum-interval：OSPF 路由计算的最大时间间隔，取值范围为 1～60，单位为秒。
minimum-interval：OSPF 路由计算的最小时间间隔，取值范围为 10～60000，单位为毫秒。
incremental-interval：OSPF 路由计算的时间间隔惩罚增量，取值范围为 10～60000，单位为毫秒。
【使用指导】
根据本地维护的 LSDB，运行 OSPF 协议的路由器通过 SPF 算法计算出以自己为根的最短路径树，并根据这一最短路径树决定到目的网络的下一跳。通过调节 SPF 的计算间隔，可以抑制网络频繁变化可能导致的带宽资源和路由器资源被过多占用的问题。
本命令在网络变化不频繁的情况下将连续路由计算的时间间隔缩小到 minimum-interval，而在网络变化频繁的情况下可以进行相应惩罚，将等待时间按照配置的惩罚增量延长，最大不超过maximum-interval。
和 配置值不允许大于 配置minimum-interval incremental-interval maximum-interval值。
【举例】
\# 设置 OSPF 路由计算最大时间间隔为 10 秒，最小时间间隔为 500 毫秒，惩罚增量为 300 毫秒。
<Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] spf-schedule-interval 10 500 300

##### 1.1.95 stub (OSPF area view)

stub 命令用来配置一个区域为 Stub 区域。

命令用来恢复缺省情况。
undo stub【命令】
stub [ default-route-advertise-always | no-summary ] * undo stub【缺省情况】
没有区域被设置为 Stub 区域。
【视图】
OSPF 区域视图【缺省用户角色】
network-admin【参数】
default-route-advertise-always：该参数只用于 区域的 ABR，配置后，ABR 向Stub Stub区域内发布缺省路由的 Type-3 LSA 时不检查骨干区域是否存在 FULL 状态的邻居。如果未指定本参数，ABR 向 Stub 区域内发布缺省路由的 Type-3 LSA 时需要检查骨干区域是否存在 FULL 状态的邻居，如果不存在 FULL 状态的邻居，则 ABR 不会向 Stub 区域内发布缺省路由的 Type-3 LSA。
no-summary：该参数只用于 Stub 区域的 ABR，配置后，ABR 只向 Stub 区域内发布一条缺省路由的 LSA，不生成任何其它 LSA（这种区域又称为 区域）。
Type-3 Type-3 Totally Stub【使用指导】
如果要将一个区域配置成 Stub 区域，则该区域中的所有路由器都必须配置此属性。
多次执行本命令，最后一次执行的命令生效。
【举例】
\# 将 OSPF 区域 1 设置为 Stub 区域。
<Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] area 1 [Sysname-ospf-100-area-0.0.0.1] stub【相关命令】
• default-cost (OSPF area view)

##### 1.1.96 stub-router (OSPF view)

stub-router 命令用来配置当前路由器为 Stub 路由器。
undo stub-router 命令用来恢复缺省情况。
【命令】
stub-router [ external-lsa [ max-metric-value ] | include-stub | on-startup { seconds | wait-for-bgp [ seconds ] } | summary-lsa [ max-metric-value ] ] * undo stub-router

【缺省情况】
当前路由器没有被配置为 Stub 路由器。
【视图】
OSPF 视图【缺省用户角色】
network-admin【参数】
external-lsa max-metric-value：路由器发布的外部 LSA 链路度量值。max-metric-value表示链路度量值，取值范围为 1～16777215，缺省值为 16711680。
include-stub：路由器发布的 Router-LSA 中，链路类型为 3 的 Stub 链路度量值将设置为最大值 65535。
seconds：在路由器重启期间，路由器作为 Stub 路由器。seconds 表示超时时间，on-startup取值范围为 5～86400，单位为秒。
seconds：在路由器重启后，等待 BGP 路由收敛期间，路由器作为 Stub 路由器。
wait-for-bgp seconds 表示超时时间，取值范围为 5～86400，单位为秒，缺省值为 600。
max-metric-value：路由器发布的 类 链路度量值。max-metric-value summary-lsa 3 LSA表示链路度量值，取值范围为 1～16777215，缺省值为 16711680。
【使用指导】
通过将当前路由器配置为 Stub 路由器，在该路由器发布的 Router-LSA 中，当链路类型取值为 3 表示连接到 网络时，链路度量值不变；当链路类型为 1、2、4 分别表示通过 链路与另一路Stub P2P由器相连、连接到传送网络、虚连接时，链路度量值将设置为最大值 65535。这样其邻居计算出这条路由的开销就会很大，如果邻居上有到这个目的地址开销更小的路由，则数据不会通过这个 Stub路由器转发。
【举例】
配置当前路由器为 路由器。
\# Stub <Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] stub-router

##### 1.1.97 transmit-pacing

命令用来配置接口发送 LSU 报文的时间间隔和一次发送 LSU 报文的最大个数。
transmit-pacing命令用来恢复缺省情况。
undo transmit-pacing【命令】
transmit-pacing interval interval count count undo transmit-pacing【缺省情况】
接口发送 LSU 报文的时间间隔为 20 毫秒，一次最多发送 3 个 LSU 报文。

【视图】
OSPF 视图【缺省用户角色】
network-admin【参数】
interval：接口发送 报文的时间间隔，interval 的取值范围为 10～1000，单interval LSU位为毫秒。当路由器上使能 OSPF 功能的接口数比较多时，建议增大该值，以控制路由器每秒钟发送 LSU 报文的总数。
count count：接口一次发送 LSU 报文的最大个数，count 的取值范围为 1～200。当路由器上使能 OSPF 功能的接口数比较多时，建议减小该值，以控制路由器每秒钟发送 LSU 报文的总数。
【举例】
配置 进程 的所有接口发送 报文的时间间隔为 毫秒，一次最多发送 个 报\# OSPF 1 LSU 30 10 LSU文。
<Sysname> system-view [Sysname] ospf 1 [Sysname-ospf-1] transmit-pacing interval 30 count 10

##### 1.1.98 ttl-security

命令用来开启区域的 功能。
ttl-security OSPF GTSM命令用来关闭区域的 功能。
undo ttl-security OSPF GTSM【命令】
ttl-security [ hops hop-count ] undo ttl-security【缺省情况】
区域的 OSPF GTSM 功能处于关闭状态。
【视图】
OSPF 区域视图【缺省用户角色】
network-admin【参数】
hops hop-count：指定接口收到 OSPF 报文并进行安全检测时，允许接收的报文所经过的路由器的最大跳数。hop-count 表示最大跳数，取值范围为 1～254，如果未指定本参数，对于 OSPF普通邻居，缺省值为 1；对于 OSPF 虚连接邻居，缺省值为 255。
【使用指导】
在 区域视图下开启 功能后，该区域中所有使能 的接口都会生效。当设备从某OSPF GTSM OSPF个接口上收到一个 OSPF 报文时，会判断报文的 TTL 是否在 255-“hop-count”+1 到 255 之间。

如果在，就上送报文；否则直接丢弃报文。从而使设备能够避免受到 CPU 利用（CPU-utilization）
类型的攻击（如 过载），增强系统的安全性。
CPU执行本命令后，设备会将发送报文的初始 设置为 255，这就要求本地设备和邻居设备上同时配TTL置本特性，指定的 hop-count 值可以不同，只要能够通过安全检测即可。
在接口视图下配置的 hops 参数的优先级高于在 OSPF 区域视图下配置的 hops 参数。
如果区域中配置了虚连接，建议用户指定 hops 参数，配置时需要考虑虚连接发送的 OSPF 报文所经过的路由器的最大跳数。同时建议用户只在区域视图下开启 GTSM 功能，当且仅当用户已经明确知道了哪些接口是用来发送和接收虚连接的 OSPF 报文时，可以在所有这些接口下开启 OSPF 的功能，否则可能会导致虚连接两端的路由器丢弃接收到的 报文。
GTSM OSPF【举例】
\# 配置在 OSPF 区域视图下开启 GTSM 功能。
<Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] area 1 [Sysname-ospf-100-area-0.0.0.1] ttl-security【相关命令】
• ospf ttl-security

##### 1.1.99 vlink-peer (OSPF area view)

命令用来创建并配置一条虚连接。
vlink-peer命令用来删除一条已有的虚连接。
undo vlink-peer【命令】
vlink-peer router-id [ dead seconds | hello seconds | { { hmac-md5 | md5 } key-id { cipher | plain } string | keychain keychain-name | simple { cipher | plain } string } | retransmit seconds | trans-delay seconds ] * undo vlink-peer router-id [ dead | hello | { hmac-md5 | md5 } key-id | keychain | retransmit | simple | trans-delay ] *【缺省情况】
不存在虚链接。
【视图】
OSPF 区域视图【缺省用户角色】
network-admin【参数】
router-id：虚连接邻居的路由器 ID。
seconds：失效时间间隔，取值范围为 1～32768，单位为秒，缺省值为 40。该值必须和与dead其建立虚连接路由器的 dead seconds 值相等，并至少为 hello seconds 值的 4 倍。

seconds：接口发送 Hello 报文的时间间隔，取值范围为 1～8192，单位为秒，缺省值为hello 10。该值必须和与其建立虚连接路由器上的 值相等。
hello seconds hmac-md5：HMAC-MD5 验证模式。
md5：MD5 验证模式。
simple：简单验证模式。
key-id：MD5/HMAC-MD5 验证字标识符，取值范围为 1～255。
cipher：以密文方式设置密钥。
plain：以明文方式设置密钥，该密钥将以密文形式存储。
string：密钥字符串，区分大小写。简单验证模式下，明文密钥为 1～8 个字符的字符串；密文密钥为 33～41 个字符的字符串。MD5/HMAC-MD5 验证模式下，明文密钥为 1～16 个字符的字符串；
密文密钥为 33～53 个字符的字符串。
keychain：使用 keychain 验证方式。
keychain-name：keychain 名称，为 1～63 个字符的字符串，区分大小写。
retransmit seconds：接口重传 LSA 报文的时间间隔，取值范围为 1～3600，单位为秒，缺省值为 5。
trans-delay seconds：接口延迟发送 LSA 报文的时间间隔，取值范围为 1～3600，单位为秒，缺省值为 1。
【使用指导】
根据 的规定，OSPF 的所有非骨干区域必须是和骨干区域保持连通的，可以使用RFC 2328 vlink-peer 命令建立逻辑上的连通性。
各参数取值规则如下：
值越小，发现网络变化的速度越快，消耗的网络资源也就越多。
• hello不能将 值设置的太小，否则将会引起不必要的重传。网络速度相对较慢的时候
• retransmit应把该值设的更大一些。
• 设置 trans-delay 值时必须考虑接口的发送延迟。
虚 连 接可 指定 使 用 MD5/HMAC-MD5 验 证 或简单 验 证两 种方 式 ，但 不能 同 时指 定； 使 用MD5/HMAC-MD5 验证方式时，可配置多条 MD5/HMAC-MD5 验证命令，但 key-id 是唯一的，同一 只能配置一个验证字。
key-id修改虚连接的 OSPF MD5/HMAC-MD5 验证字的步骤如下：
• 首先为该虚连接配置新的 MD5/HMAC-MD5 验证字；此时若邻居设备尚未配置新的验证字，便会触发 验证平滑迁移过程。在这个过程中，MD5/HMAC-MD5 MD5/HMAC-MD5 OSPF 会发送分别携带各个 MD5/HMAC-MD5 验证字的多份报文，使得无论邻居设备上是否配置了新验证字都能验证通过，保持邻居关系。
• 然后在邻居设备上也都配置相同的新 MD5/HMAC-MD5 验证字；当本设备上收到邻居的携带新验证字的报文后，便会退出 MD5/HMAC-MD5 验证平滑迁移过程。
最后在本设备和邻居上都删除旧的 MD5/HMAC-MD5 验证字；建议不要为虚连接保留多个
•验证字，每次 验证字修改完毕后，应当及时删除旧的验MD5/HMAC-MD5 MD5/HMAC-MD5证字，这样可以防止与持有旧验证字的系统继续通信、减少被攻击的可能，还可以减少验证迁移过程对系统、带宽的消耗。
在 OSPF 虚连接使用 keychain 验证方式时，报文的收、发过程如下：

OSPF 虚连接在发送报文前，会先从 keychain 获取当前的有效发送 key，根据该 key 的标识
•符、认证算法和认证密钥进行报文验证，如果当前不存在有效发送 key，或者该 的标识符key大于 255，OSPF 虚连接不会发送报文。
• OSPF虚连接在收到报文后，会根据报文携带的key的标识符从keychain中获取有效接收key，根据该 key 的认证算法和认证密钥对报文进行校验。如果报文校验失败，或者根据报文中携带的 的标识符无法从 中获取到有效接收 key，则该报文将被丢弃。
key keychain对于 认证算法和 的标识符的范围，OSPF 的支持情况如下：
keychain key OSPF 仅支持 MD-5、HMAC-MD5 和 HMAC-SM3 认证算法。
•OSPF 仅支持标识符取值范围为 0～255 的 key。
•【举例】
配置虚连接，对端路由器 为 1.1.1.1。
\# Router ID <Sysname> system-view [Sysname] ospf 100 [Sysname-ospf-100] area 2 [Sysname-ospf-100-area-0.0.0.2] vlink-peer 1.1.1.1【相关命令】
• authentication-mode
• display ospf vlink

## 05-IS-IS命令

目 录配置命令

### 1 IS-IS

1 IS-IS

#### 1.1 IS-IS配置命令

##### 1.1.1 address-family ipv4

命令用来创建 IS-IS IPv4 地址族，并进入 IS-IS IPv4 地址族视图。
address-family ipv4命令用来删除 IS-IS IPv4 地址族及 IS-IS IPv4 地址族视图下的所undo address-family ipv4有配置。
【命令】
address-family ipv4 [ unicast ] undo address-family ipv4 [ unicast ]【缺省情况】
不存在 IS-IS IPv4 地址族。
【视图】
IS-IS 视图【缺省用户角色】
network-admin【参数】
unicast：表示单播地址族。缺省为单播地址族。
【举例】
\# 创建 IS-IS IPv4 地址族，并进入 IS-IS IPv4 地址族视图。
<Sysname> system-view [Sysname] isis 100 [Sysname-isis-100] address-family ipv4 [Sysname-isis-100-ipv4]

##### 1.1.2 address-family ipv6

命令用来创建 IS-IS IPv6 地址族，并进入 IS-IS IPv6 地址族视图。
address-family ipv6命令用来删除 IS-IS IPv6 地址族及 IS-IS IPv6 地址族视图下的所undo address-family ipv6有配置。
【命令】
address-family ipv6 [ unicast ] undo address-family ipv6 [ unicast ]【缺省情况】
不存在 IS-IS IPv6 地址族。

【视图】
IS-IS 视图【缺省用户角色】
network-admin【参数】
unicast：表示单播地址族。缺省为单播地址族。
【使用指导】
配置本命令后，进程的 IPv6 被使能。
【举例】
\# 在 IS-IS 视图下，创建并进入 IS-IS IPv6 地址族视图。
<Sysname> system-view [Sysname] isis 100 [Sysname-isis-100] address-family ipv6 [Sysname-isis-100-ipv6]

##### 1.1.3 area-authentication send-only

命令用来配置对收到的 报文（包括 LSP、CSNP、area-authentication send-only Level-1 PSNP）忽略认证信息检查。
undo area-authentication send-only 命令用来恢复缺省情况。
【命令】
area-authentication send-only undo area-authentication send-only【缺省情况】
如果配置了区域验证方式和验证密钥，对收到的报文执行认证信息检查。
【视图】
IS-IS 视图【缺省用户角色】
network-admin【使用指导】
配置区域验证方式和验证密钥后，验证密钥将按照设定的方式插入到发送的 Level-1 报文（包括 LSP、CSNP、PSNP）中，并对收到的 Level-1 报文进行验证密钥的检查。当需要更改密钥时由于密钥不匹配可能导致业务发生中断。通过命令配置对收到的 Level-1 报文忽略认证信息检查可保证业务不中断，报文正常接收。
【举例】
\# 对收到报文忽略认证信息检查。
<Sysname> system-view [Sysname] isis 1

[Sysname-isis-1] area-authentication send-only【相关命令】
•area-authentication-mode
•domain-authentication send-only
•isis authentication send-only

##### 1.1.4 area-authentication-mode

area-authentication-mode 命令用来配置区域验证方式和验证密钥。
undo area-authentication-mode 命令用来恢复缺省情况。
【命令】
area-authentication-mode { { gca key-id { hmac-sha-1 | hmac-sha-224 | hmac-sha-256 | hmac-sha-384 | hmac-sha-512 } [ nonstandard ] | md5 | simple } { cipher | plain } string | keychain keychain-name } [ ip | osi ] undo area-authentication-mode【缺省情况】
未配置区域验证方式和验证密钥。
【视图】
IS-IS 视图【缺省用户角色】
network-admin【参数】
gca：GCA 验证模式（Generic Cryptographic Authentication）。
key-id：唯一标识一个认证项（SA），取值范围为 1～65535。发送方将 Key ID 放入认证 TLV 中，接收方根据报文中提取的 Key ID 选择 SA 对报文进行认证。
hmac-sha-1：支持 HMAC-SHA-1 算法。
hmac-sha-224：支持 HMAC-SHA-224 算法。
hmac-sha-256：支持 HMAC-SHA-256 算法。
hmac-sha-384：支持 HMAC-SHA-384 算法。
hmac-sha-512：支持 HMAC-SHA-512 算法。
nonstandard：非标准 验证模式。
GCA md5：MD5 验证模式。
simple：简单验证模式。
cipher：以密文方式设置密钥。
plain：以明文方式设置密钥，该密钥将以密文形式存储。
string：密钥字符串，区分大小写。明文密钥为 1～16 个字符的字符串，密文密钥为 33～53 个字符的字符串。
keychain：使用 验证模式。
keychain

keychain-name：keychain 名，为 1～63 个字符的字符串，区分大小写。
ip：检查 LSP 中 IP 的相应字段的配置内容。
osi：检查 LSP 中 OSI 的相应字段的配置内容。
【使用指导】
通过配置区域验证，可防止将从不可信任的路由器学习到的路由信息加入到本地 中。
LSDB配置区域验证方式和验证密钥后，验证密钥将按照设定的方式插入到发送的 报文（包括 LSP、Level-1 CSNP、PSNP）中，并对收到的 Level-1 报文进行验证密钥的检查。
IS-IS 的 md5 验证模式对应于 keychain 的 HMAC-MD5 认证算法，所以 keychain 内的 key 只有使用 HMAC-MD5 认证算法，才能使得 IS-IS 在使用 keychain 验证模式时能够正常工作。当 IS-IS 区域使用 keychain 验证模式时，报文的收、发过程如下：
• IS-IS 在发送 Level-1 报文前，会先从 keychain 获取当前的有效发送 key，根据该 key 的认证算法和认证密钥进行报文验证；如果当前不存在有效发送 key，或者该 的认证算法不是key HMAC-MD5，则 IS-IS 发送的 Level-1 报文中不含认证 TLV。
• IS-IS 在收到 Level-1 报文后，会从 keychain 获取当前的有效接收 key，根据各个 key 的认证算法和认证密钥对报文进行校验。如果当前不存在有效接收 key，或者使用所有的有效接收key 对报文的校验都未成功，则报文校验不通过，该报文被丢弃。
同一区域内的路由器必须配置相同的验证方式和验证密钥。
认证密钥选用 或 不受实际的网络环境影响。如果没有指定 或 参数，将检查 LSP ip osi ip osi中 的相应字段的配置内容。
OSI使用 验证模式时：
GCA不指定 参数时，为协议标准实现方式，可与友商互通；
• nonstandard指定 参数时，为私有实现方式，用于与 Comware早期采用非标准实现方式的
• nonstandard设备（无 参数）互通。
nonstandard【举例】
\# 在 IS-IS 进程 1 下配置区域采用简单明文验证模式，验证密钥为 123456。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] area-authentication-mode simple plain 123456【相关命令】
• area-authentication send-only
• domain-authentication-mode
• isis authentication-mode

##### 1.1.5 auto-cost enable

auto-cost enable 命令用来使能自动计算接口链路开销值功能。
undo auto-cost enable 命令用来关闭自动计算接口链路开销值功能。
【命令】
auto-cost enable undo auto-cost enable

【缺省情况】
自动计算接口链路开销值功能处于关闭状态。
【视图】
IS-IS 视图IS-IS IPv6 单播地址族视图【缺省用户角色】
network-admin【使用指导】
使能自动计算接口链路开销值功能后，将根据带宽参考值自动计算接口的链路度量值。当开销值的类型为 wide 或 wide-compatible 时，可以根据公式“开销=（参考值÷带宽）×10”计算接口的链路度量值。当开销值类型为其他类型时，具体情况如下：接口带宽≤10Mbps 时，值为 60；接口带宽≤100Mbps 时，值为 50；接口带宽≤155Mbps 时，值为 40；接口带宽≤622Mbps 时，值为 30；接口带宽≤2500Mbps 时，值为 20；接口带宽>2500Mbps 时，值为 10。
【举例】
\# 使能 IS-IS 进程 1 的自动计算接口链路开销值功能。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] auto-cost enable【相关命令】
•bandwidth-reference
• cost-style
• isis cost
• isis ipv6 cost

##### 1.1.6 bandwidth-reference

bandwidth-reference 命令用来配置 IS-IS 自动计算链路开销值时依据的带宽参考值。
undo bandwidth-reference 命令用来恢复缺省情况。
【命令】
bandwidth-reference value undo bandwidth-reference【缺省情况】
IS-IS 自动计算链路度量值时依据的带宽参考值为 100Mbps。
【视图】
视图IS-IS单播地址族视图IS-IS IPv6【缺省用户角色】
network-admin

【参数】
value：带宽参考值，取值范围为 1～2147483648，单位为 Mbps。
【举例】
\# 配置 IS-IS 进程 1 的带宽参考值为 200Mbps。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] bandwidth-reference 200【相关命令】
• auto-cost enable
• isis cost

##### 1.1.7 circuit-cost

命令用来全局配置 IS-IS 的链路开销值。
circuit-cost命令用来取消全局配置的 IS-IS 的链路开销值。
undo circuit-cost【命令】
cost-value circuit-cost [ level-1 | level-2 ] undo circuit-cost [ level-1 | level-2 ]【缺省情况】
未全局配置 的链路开销值。
IS-IS【视图】
IS-IS 视图IS-IS IPv6 单播地址族视图【缺省用户角色】
network-admin【参数】
cost-value：链路开销值，当指定的路径开销值类型不同时，取值范围也不同：
• 当指定的路径开销值类型为 narrow、narrow-compatible 或 时，取值范围compatible为 0～63。
当指定的路径开销值类型为 或 时，取值范围为 0～16777215。
• wide wide-compatible level-1：配置在计算 路由时使用的链路开销值。
Level-1 level-2：配置在计算 Level-2 路由时使用的链路开销值。
【使用指导】
如果不指定级别，将同时配置计算 和 路由时使用的链路开销值。
Level-1 Level-2【举例】
\# 全局配置 IS-IS 进程 1 下所有接口在计算 Level-1 路由时的链路开销值为 11。
<Sysname> system-view [Sysname] isis 1

[Sysname-isis-1] circuit-cost 11 level-1【相关命令】
•cost-style
•isis cost

##### 1.1.8 cost-style

命令用来配置 IS-IS 开销值的类型，即 IS-IS 接收和发送的报文中到达目的地路径开cost-style销值的类型。
命令用来恢复缺省情况。
undo cost-style【命令】
cost-style { narrow | wide | wide-compatible | { compatible | narrow-compatible } [ relax-spf-limit ] } undo cost-style【缺省情况】
IS-IS 开销值的类型为 narrow。
【视图】
IS-IS 视图【缺省用户角色】
network-admin【参数】
narrow：表示只可以接收和发送采用 narrow 方式（取值范围为 0～63）表示到达目的地路径开销的报文。
wide：表示只可以接收和发送采用 wide 方式（取值范围为 0～16777215）表示到达目的地路径开销的报文。
compatible：表示可以接收和发送采用 和 方式表示到达目的地路径开销的报文。
narrow wide narrow-compatible：表示可以接收采用 和 方式表示到达目的地路径开销的报文，narrow wide却只能发送采用 方式表示到达目的地路径开销的报文。
narrow wide-compatible：表示可以接收采用 和 方式表示到达目的地路径开销的报文，narrow wide却只能发送采用 wide 方式表示到达目的地路径开销的报文。
relax-spf-limit：表示允许接收到达目的地路径开销值大于 的报文。如果不指定该参数，1023则 在 收 到 开 销 值 大 于 1023 的 报 文 时 ， 将 丢 弃 。 只 有 当 指 定 了 compatible 或时该参数可选。
narrow-compatible【举例】
配置路由器可以接收采用 或 方式表示路由开销值的报文，却只能发送采用\# narrow wide narrow方式表示路由开销值的报文。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] cost-style narrow-compatible

【相关命令】
• circuit-cost
• isis cost

##### 1.1.9 default-route-advertise

default-route-advertise 命令用来配置 IS-IS 发布 Level-1 或 Level-2 级别的缺省路由，即在指定级别的 LSP 中宣告目的地为 0.0.0.0/0 的路径信息。
undo default-route-advertise 命令用来恢复缺省情况。
【命令】
default-route-advertise [ avoid-learning | [ level-1 | level-1-2 | level-2 ] | route-policy route-policy-name | tag tag ] * undo default-route-advertise【缺省情况】
IS-IS 不发布 Level-1 或 Level-2 级别的缺省路由。
【视图】
IS-IS IPv4 单播地址族视图IS-IS IPv6 单播地址族视图【缺省用户角色】
network-admin【参数】
avoid-learning：禁止学习通过 LSP 发过来的缺省路由和 ATT 位产生的缺省路由，防止出现环路。
level-1：发布 级别的缺省路由。
Level-1 level-1-2：同时发布 和 级别的缺省路由。
Level-1 Level-2 level-2：发布 级别的缺省路由。
Level-2 route-policy-name：指定路由策略名。route-policy-name 为 1～63 个route-policy字符的字符串，区分大小写。
tag tag：配置缺省路由 Tag 值，取值范围为 1～4294967295。
【使用指导】
如果不指定级别，则默认发布 Level-2 级别的缺省路由。
Level-1 缺省路由只发布给本区域的其他路由器，Level-2 缺省路由发布给所有 Level-2 和 Level-1-2路由器。
如果在路由策略视图中 level-1，则可以在 L1 LSP 中生成缺省路由；如果在路由apply isis策略视图中 level-2，则可以在 L2 LSP 中生成缺省路由；如果在路由策略视图中apply isis apply isis level-1-2，可以在 L1 LSP、L2 LSP 中各自生成缺省路由。
如果在路由策略中指定了 值，则本命令中的 值不生效。
Tag Tag

【举例】
\# 配置 IS-IS 进程 1 发布 Level-2 级别缺省路由。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] address-family ipv4 [Sysname-isis-1-ipv4] default-route-advertise

##### 1.1.10 display isis

命令用来显示 的进程信息。
display isis IS-IS【命令】
display isis [ process-id ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：IS-IS 进程号，取值范围为 1～65535，显示指定 进程的进程信息。如果未指IS-IS定本参数，将显示所有 IS-IS 进程的进程信息。
【举例】
\# 显示 IS-IS 的进程信息。
<Sysname> display isis IS-IS(1) Protocol Information Network-entity : 10.0000.0000.0001.00 IS-level : level-1-2 Cost-style : Wide Fast reroute : Disabled Preference : 15 LSP-length receive : 1497 LSP-length originate level-1 : 1497 level-2 : 1497 Maximum imported routes : 1000 Timers LSP-max-age : 1200 LSP-refresh : 900 SPF intervals : 5 50 200 IPv6 enabled Fast reroute : Disabled Preference : 15

Maximum imported routes : 1000 SPF intervals : 5 50 200表1-1 display isis 显示信息描述表字段 描述Network-entity 网络实体名称路由器类型IS-level Cost-style 开销类型是否使能快速重路由功能：
• Disabled：表示未使能Fast reroute
• LFA：表示自动选取备份下一跳
• Route-policy：表示通过路由策略来指定备份下一跳Preference 路由优先级LSP-length receive 可以接收 LSP 的最大长度LSP-length originate 生成的LSP的最大长度引入Level1/Level2的IPv4路由/IPv6路由最大条数Maximum imported routes LSP相关定时器信息，包括：
• LSP-max-age：LSP 的最大生存时间Timers
• LSP-refresh：LSP 的刷新周期
• SPF intervals：SPF 的计算时间间隔IS-IS进程支持IPv6功能IPv6 enabled

##### 1.1.11 display isis event-log graceful-restart

display isis event-log graceful-restart 命令用来显示 IS-IS GR 日志信息。
【命令】
display isis event-log graceful-restart slot slot-number【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
slot slot-number：显示指定成员设备的 IS-IS GR 日志信息，slot-number 表示设备在 IRF中的成员编号。
【举例】
\# 显示指定 slot 上 GR 的日志信息。

<Sysname> display isis event-log graceful-restart slot 1 IS-IS loginfo :
Sep 18 08:48:24 2015 slot 1 Process 1 enter GR restarting phase(Initialization).
Sep 18 08:48:24 2015 slot 1 Process 1 enter GR phase (LSDB synchronization).
Sep 18 08:48:24 2015 slot 1 Process 1 enter GR phase (TE tunnel prepare).
Sep 18 08:48:24 2015 slot 1 Process 1 enter GR phase (First SPF computation).
Sep 18 08:48:25 2015 slot 1 Process 1 enter GR phase (Redistribution).
Sep 18 08:48:25 2015 slot 1 Process 1 enter GR phase (Second SPF computation).
Sep 18 08:48:25 2015 slot 1 Process 1 enter GR phase (LSP stability).
Sep 18 08:48:25 2015 slot 1 Process 1 enter GR phase (LSP generation).
Sep 18 08:48:25 2015 slot 1 Process 1 enter GR phase (Finish).
Sep 18 08:48:25 2015 slot 1 Process 1 GR complete.
表1-2 display isis event-log graceful-restart 显示信息描述表字段 描述GR阶段：
• Initialization ：初始化
• synchronization：LSDB 同步LSDB
• TE tunnel prepare：TE 隧道计算准备阶段
• computation：第一次路由计算First SPF GR phase
• Redistribution：引入路由
• Second SPF computation：第二次路由计算
• LSP stability：准备生成 LSP
• LSP generation：LSP 生成和泛洪
• Finish：完成

##### 1.1.12 display isis event-log lsp

display isis event-log lsp 命令用来显示 IS-IS LSP 日志信息。
【命令】
display isis event-log lsp [ level-1 | level-2 ] [ process-id ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
level-1 ：显示 Level-1 的 LSP 日志信息。
level-2：显示 的 日志信息。
Level-2 LSP process-id：IS-IS 进程号，取值范围为 1～65535。如果不指定本参数，则显示所有 进程IS-IS的 LSP 日志信息。

【使用指导】
如果不指定级别，则同时显示 Level-1 和 Level-2 级别的 LSP 日志信息。
【举例】
\# 显示 IS-IS LSP 日志信息。
<Sysname> display isis event-log lsp LSP Log for IS-IS(1)
-------------------- Level-1 LSP Log
--------------- Date Time LSPID Seq Num Event
------------------------------------------------------------------------------- 2015-11-06 11:10:45 1111.1111.1111.00-00 0x0000019c LSP received 2015-11-06 09:26:40 1111.1111.1111.01-00 0x00000111 Purged LSP received 2015-11-06 09:26:28 2222.2222.2222.00-00 0x00000181 LSP generated 2015-11-06 09:26:21 2222.2222.2222.00-00 0x00000180 Purged LSP generated Level-2 SPF Log
--------------- Date Time LSPID Seq Num Event
------------------------------------------------------------------------------- 2015-11-06 11:10:45 1111.1111.1111.00-00 0x0000090d LSP received 2015-11-06 09:26:41 1111.1111.1111.01-00 0x00000101 Purged LSP received 2015-11-06 09:26:27 2222.2222.2222.00-00 0x00000171 LSP generated 2015-11-06 09:26:20 2222.2222.2222.00-00 0x00000170 Purged LSP generated表1-3 display isis event-log lsp 命令显示信息描述表字段 描述Date 记录LSP变化的日期Time 记录LSP变化的时间链路状态报文ID LSPID Seq Num LSP序列号LSP变化的事件类型：
•LSP received：接收到 LSP 报文Event • Purged LSP received：接收到 LSP 清除报文
• LSP generated：生成 LSP 报文
• Purged LSP generated：生成 LSP 清除报文【相关命令】
• reset isis event-log lsp

##### 1.1.13 display isis event-log non-stop-routing

display isis event-log non-stop-routing 命令用来显示 IS-IS NSR 日志信息。
【命令】
display isis event-log non-stop-routing slot slot-number【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
slot slot-number：显示指定成员设备的 IS-IS NSR 日志信息，slot-number 表示设备在 IRF中的成员编号。
【举例】
\# 显示指定 slot 上的 IS-IS NSR 日志信息。
<Sysname> display isis event-log non-stop-routing slot 1 IS-IS loginfo :
Sep 18 10:20:44 2015 slot 1 Enter HA Block status Sep 18 10:20:44 2015 slot 1 Exit HA Block status Sep 18 10:24:00 2015 slot 1 Process 100 enter NSR phase (Initialization).
Sep 18 10:24:00 2015 slot 1 Process 100 enter NSR phase (Smooth).
Sep 18 10:24:00 2015 slot 1 Process 100 enter NSR phase (TE tunnel prepare).
Sep 18 10:24:00 2015 slot 1 Process 100 enter NSR phase (First SPF computation).
Sep 18 10:24:00 2015 slot 1 Process 100 enter NSR phase (Redistribution).
Sep 18 10:24:00 2015 slot 1 Process 100 enter NSR phase (Second SPF computation).
Sep 18 10:24:00 2015 slot 1 Process 100 enter NSR phase (LSP stability).
Sep 18 10:24:00 2015 slot 1 Process 100 enter NSR phase (LSP generation).
Sep 18 10:24:00 2015 slot 1 Process 100 enter NSR phase (Finish).
Sep 18 10:24:00 2015 slot 1 Process 100 NSR complete.

表1-4 display isis event-log non-stop-routing 显示信息描述表字段 描述NSR阶段：
• Initialization：初始化
• Smooth：平滑
• TE tunnel prepare：TE 隧道计算准备阶段
• First SPF computation：第一次路由计算NSR phase
• Redistribution：引入路由
• Second SPF computation：第二次路由计算
• stability：准备生成LSP LSP
• LSP generation：LSP 生成和泛洪
• Finish：完成

##### 1.1.14 display isis event-log spf

display isis event-log spf 命令用来显示 IS-IS 路由计算日志信息。
【命令】
display isis event-log spf [ ipv4 | ipv6 ] [ [ level-1 | level-2 ] | verbose ] * [ process-id ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
ipv4：显示 IS-IS 的 IPv4 路由计算日志信息。
：显示 IS-IS 的 IPv6 路由计算日志信息。
ipv6 level-1：显示 Level-1 路由计算日志信息。
level-2：显示 Level-2 路由计算日志信息。
verbose：显示路由计算日志的详细信息。如果未指定本参数，将显示路由计算日志的概要信息。
process-id：IS-IS 进程号，取值范围为 1～65535，显示指定 IS-IS 进程的路由计算日志信息。
如果未指定本参数，将显示所有 IS-IS 进程的路由计算日志信息。
【使用指导】
如果不指定 和 参数，则显示公网拓扑 路由计算日志信息。
ipv4 ipv6 IPv4如果不指定级别，则同时显示 和 级别的路由计算日志信息。
Level-1 Level-2【举例】
\# 显示 IS-IS 路由计算日志的概要信息。

<Sysname> display isis event-log spf SPF Log for IS-IS(1)
-------------------- Level-1 SPF Log
--------------- Date Time Duration Count Trigger event
------------------------------------------------------------------------------- 2015-09-07 11:10:45 0 4 Interface metric changed 2015-09-07 09:26:40 0 4 LSP updated 2015-09-07 09:26:28 0 2 DIS changed 2015-09-07 09:26:21 0.001 2 LSP updated 2015-09-07 09:26:07 0.001 3 Direct route changed Level-2 SPF Log
--------------- Date Time Duration Count Trigger event
------------------------------------------------------------------------------- 2015-09-07 11:10:45 0 4 Interface metric changed 2015-09-07 09:26:40 0 4 LSP updated 2015-09-07 09:26:28 0 2 DIS changed 2015-09-07 09:26:21 0 2 LSP updated 2015-09-07 09:26:07 0 3 Direct route changed \# 显示 IS-IS 路由计算日志的详细信息。
<Sysname> display isis event-log spf verbose SPF Log for IS-IS(1)
-------------------- Level-1 SPF Log
--------------- Log date : 2015-09-07 11:10:45 Log key : 5 Trigger count : 4 Trigger event : Interface metric changed SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF nodes: 3 BSPF 0 Candidate NBRs: 1 LFA 0 LFA SPF nodes: 1 Area 0 Area addresses: 1 PRC 0 Add: 0 modify: 1 delete: 0 Last 10 routes:

1.1.1.0/24
Route summary 0 Summary route nodes: 0
Total 0
Log date : 2015-09-07 09:26:40
Log key : 4
Trigger count : 4
Trigger event : LSP updated
SPF details :
Phase Duration Description
TE tunnel ADJ 0 TE SPF nodes: 0
Topology 0 SPF nodes: 3
BSPF 0 Candidate NBRs: 1
LFA 0 LFA SPF nodes: 1
Area 0 Area addresses: 1
PRC 0 Add: 0 modify: 0 delete: 0
Route summary 0 Summary route nodes: 0
Total 0
Log date : 2015-09-07 09:26:28
Log key : 3
Trigger count : 2
Trigger event : DIS changed
SPF details :
Phase Duration Description
TE tunnel ADJ 0 TE SPF nodes: 0
Topology 0 SPF links changed: 1
BSPF 0 Candidate NBRs: 0
LFA 0 LFA SPF nodes: 0
Area 0 Area addresses: 0
PRC 0 Add: 0 modify: 0 delete: 0
Route summary 0 Summary route nodes: 0
Total 0
Log date : 2015-09-07 09:26:21
Log key : 2
Trigger count : 2
Trigger event : LSP updated
SPF details :
Phase Duration Description
TE tunnel ADJ 0 TE SPF nodes: 0
Topology 0 SPF nodes: 0
BSPF 0 Candidate NBRs: 0
LFA 0 LFA SPF nodes: 0
Area 0 Area addresses: 1
PRC 0.001 Add: 0 modify: 0 delete: 0
Route summary 0 Summary route nodes: 0
Total 0.001

Log date : 2015-09-07 09:26:07 Log key : 1 Trigger count : 3 Trigger event : Direct route changed SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF nodes: 0 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 1 PRC 0.001 Add: 1 modify: 0 delete: 0 Last 10 routes:
1.1.1.0/24 Route summary 0 Summary route nodes: 0 Total 0.001 Level-2 SPF Log
--------------- Log date : 2015-09-07 11:10:45 Log key : 5 Trigger count : 4 Trigger event : Interface metric changed SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF nodes: 3 BSPF 0 Candidate NBRs: 1 LFA 0 LFA SPF nodes: 1 Area 0 Area addresses: 1 PRC 0 Add: 0 modify: 0 delete: 0 Route summary 0 Summary route nodes: 0 Total 0 Log date : 2015-09-07 09:26:40 Log key : 4 Trigger count : 4 Trigger event : LSP updated SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF nodes: 3 BSPF 0 Candidate NBRs: 1 LFA 0 LFA SPF nodes: 1 Area 0 Area addresses: 1 PRC 0 Add: 0 modify: 0 delete: 0

Route summary 0 Summary route nodes: 0 Total 0 Log date : 2015-09-07 09:26:28 Log key : 3 Trigger count : 2 Trigger event : DIS changed SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF links changed: 1 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 0 PRC 0 Add: 0 modify: 0 delete: 0 Route summary 0 Summary route nodes: 0 Total 0 Log date : 2015-09-07 09:26:21 Log key : 2 Trigger count : 2 Trigger event : LSP updated SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF nodes: 0 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 1 PRC 0 Add: 0 modify: 0 delete: 0 Route summary 0 Summary route nodes: 0 Total 0 Log date : 2015-09-07 09:26:07 Log key : 1 Trigger count : 3 Trigger event : Direct route changed SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF nodes: 0 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 1 PRC 0 Add: 0 modify: 0 delete: 0 Route summary 0 Summary route nodes: 0 Total 0

表1-5 display isis event-log spf 命令显示信息描述表字段 描述Date 路由计算开始日期路由计算开始时间Time Duration 路由计算持续时间，单位为秒，精确到小数点后六位Count 触发当前路由计算的事件计数

字段 描述最后一次触发路由计算的事件类型：
•NextHop changed：下一跳发生变化
• DIS changed：DIS 发生变化
• Interface metric changed：接口链路开销发生变化
• SPF link changed：SPF link 发送变化
• Default route changed：缺省路由发生变化
• Summary route changed：聚合路由发生变化
• TE tunnel updated：TE 隧道更新
• changed：TE 隧道链路开销变化TE tunnel metric
• IPv6 mode changed：IPv6 分拓扑模式发生变化
• changed：FRR 配置变化FRR configuration
• Prefix priority configuration changed：前缀优先级配置变化
• Route preference changed：路由优先级配置发生变化
• ISPF configuration changed：ISPF 配置发生变化
• Import filter policy changed：接收路由信息过滤策略变化
• ECMP configuration changed：等价路由条数规格配置变化
• PIC configuration changed：PIC 配置发生变化
• changed：接口不参与 计算配置发生变化Interface LFA exclude LFA Trigger event • ATT configuration changed：ATT 配置发生变化
• SPF：GR/NSR 过程中第一次路由计算GR/NSR first
• GR over：GR 过程结束
• T3 timeout：T3 定时器超时
• Direct route changed：直连路由变化
• Logic interface changed：逻辑接口变化
• Route leakage configuration changed：路由渗透配置变化
• NSR over：NSR 过程结束
• state：协议进入过载状态Entered overload
• Exited overload state：协议离开过载状态
• changed：区域地址变化Area address
• Route policy changed：路由策略变化
•Redistributed route updated：引入路由更新
• LSP updated：LSP 更新
• MT disabled：拓扑去使能
• MT enabled：拓扑使能
• TE tunnel configuration changed：TE 隧道配置变化
• TE tunnel destination changed ： TE 隧道目的地址变化
• RIB smooth：RIB 平滑Log date 路由计算日志的生成时间Log key 路由计算日志Key

字段 描述Trigger count 触发当前路由计算的事件计数SPF details 路由计算各阶段详细信息路由计算阶段：
• TE tunnel ADJ：TE 隧道邻居发布计算阶段
•Topology：拓扑计算阶段
• BSPF：备份 SPF 计算阶段Phase
• LFA：LFA 计算阶段
• Area：区域计算阶段
• PRC：前缀计算阶段
• Route summary：路由聚合计算阶段路由计算阶段的描述信息：
• TE SPF nodes：表示 TE 隧道邻居发布计算的 SPF 节点数
• SPF nodes：表示拓扑计算的 SPF 节点数
• Candidate NBRs：表示候选邻居节点计数Description • LFA SPF nodes：表示 LFA 计算的 SPF 节点数
• Area addresses：表示区域地址计算的区域地址个数
• Add、modify 和 delete：表示前缀计算汇总信息
• Last 10 routes：表示最后计算的 10 条路由信息
• nodes：表示聚合路由计算的聚合节点数Summary route Total 路由计算各阶段持续时间总和\# 显示 IS-IS 的 IPv6 路由计算日志的概要信息。
<Sysname> display isis event-log spf ipv6 SPF Log for IS-IS(1)
-------------------- Level-1 SPF Log
--------------- Date Time Duration Count Trigger event
------------------------------------------------------------------------------- 2015-09-07 11:10:45 0 4 Interface metric changed 2015-09-07 09:26:40 0 4 LSP updated 2015-09-07 09:26:28 0 2 DIS changed 2015-09-07 09:26:21 0.001 2 LSP updated 2015-09-07 09:26:07 0.001 3 Direct route changed Level-2 SPF Log
---------------

Date Time Duration Count Trigger event
------------------------------------------------------------------------------- 2015-09-07 11:10:45 0 4 Interface metric changed 2015-09-07 09:26:40 0 4 LSP updated 2015-09-07 09:26:28 0 2 DIS changed 2015-09-07 09:26:21 0 2 LSP updated 2015-09-07 09:26:07 0 3 Direct route changed \# 显示 IS-IS 的 IPv6 路由计算日志的详细信息。
<Sysname> display isis event-log spf ipv6 verbose SPF Log for IS-IS(1)
-------------------- Level-1 SPF Log
--------------- Log date : 2015-09-07 02:18:09 Log key : 10 Trigger count : 2 Trigger event : LSP updated SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF nodes: 0 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 0 PRC 0 Add: 0 modify: 0 delete: 0 Route summary 0 Summary route nodes: 0 Total 0 Log date : 2015-09-07 02:18:09 Log key : 9 Trigger count : 2 Trigger event : NextHop changed SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0.003 SPF nodes: 3 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 1 PRC 0 Add: 0 modify: 0 delete: 0 Route summary 0 Summary route nodes: 0 Total 0.003 Log date : 2011-01-01 02:17:40 Log key : 8

Trigger count : 2 Trigger event : Logic interface changed SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF nodes: 0 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 0 PRC 0.005 Add: 1 modify: 0 delete: 0 Last 10 routes:
10::/64 Route summary 0 Summary route nodes: 0 Total 0.005 Log date : 2015-09-07 02:17:38 Log key : 7 Trigger count : 1 Trigger event : Logic interface changed SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF nodes: 0 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 0 PRC 0 Add: 0 modify: 0 delete: 0 Route summary 0 Summary route nodes: 0 Total 0 Log date : 2015-09-07 02:17:33 Log key : 6 Trigger count : 5 Trigger event : NextHop changed SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF links changed: 1 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 0 PRC 0.003 Add: 0 modify: 0 delete: 1 Last 10 routes:
3::/24 Route summary 0 Summary route nodes: 0 Total 0.003 Log date : 2015-09-07 02:17:21

Log key : 5 Trigger count : 1 Trigger event : Direct route changed SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF nodes: 0 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 0 PRC 0.006 Add: 1 modify: 0 delete: 0 Last 10 routes:
3::/24 Route summary 0 Summary route nodes: 0 Total 0.006 Log date : 2015-09-07 02:17:11 Log key : 4 Trigger count : 1 Trigger event : IPv6 mode changed SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF nodes: 3 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 1 PRC 0 Add: 0 modify: 0 delete: 0 Route summary 0 Summary route nodes: 0 Total 0 Log date : 2015-09-07 01:09:33 Log key : 3 Trigger count : 2 Trigger event : DIS changed SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0.001 SPF nodes: 3 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 1 PRC 0 Add: 0 modify: 0 delete: 0 Route summary 0 Summary route nodes: 0 Total 0.001 Log date : 2015-09-07 01:09:25 Log key : 2

Trigger count : 2 Trigger event : LSP updated SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF links changed: 1 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 1 PRC 0 Add: 0 modify: 0 delete: 0 Route summary 0 Summary route nodes: 0 Total 0 Log date : 2015-09-07 01:08:49 Log key : 1 Trigger count : 1 Trigger event : Area address changed SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF nodes: 0 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 1 PRC 0 Add: 0 modify: 0 delete: 0 Route summary 0 Summary route nodes: 0 Total 0 Level-2 SPF Log
--------------- Log date : 2015-09-07 02:18:09 Log key : 10 Trigger count : 2 Trigger event : LSP updated SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF nodes: 0 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 0 PRC 0 Add: 0 modify: 0 delete: 0 Route summary 0 Summary route nodes: 0 Total 0 Log date : 2015-09-07 02:18:09 Log key : 9

Trigger count : 2 Trigger event : NextHop changed SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0.002 SPF nodes: 3 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 1 PRC 0 Add: 0 modify: 0 delete: 0 Route summary 0.001 Summary route nodes: 0 Total 0.003 Log date : 2015-09-07 02:17:40 Log key : 8 Trigger count : 2 Trigger event : Logic interface changed SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF nodes: 0 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 0 PRC 0 Add: 0 modify: 0 delete: 0 Route summary 0 Summary route nodes: 0 Total 0 Log date : 2015-09-07 02:17:38 Log key : 7 Trigger count : 1 Trigger event : Logic interface changed SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF nodes: 0 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 0 PRC 0 Add: 0 modify: 0 delete: 0 Route summary 0 Summary route nodes: 0 Total 0 Log date : 2015-09-07 02:17:33 Log key : 6 Trigger count : 5 Trigger event : NextHop changed SPF details :

Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF links changed: 1 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 0 PRC 0.001 Add: 0 modify: 0 delete: 0 Route summary 0 Summary route nodes: 0 Total 0.001 Log date : 2015-09-07 02:17:21 Log key : 5 Trigger count : 1 Trigger event : Direct route changed SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF nodes: 0 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 0 PRC 0 Add: 0 modify: 0 delete: 0 Route summary 0 Summary route nodes: 0 Total 0 Log date : 2015-09-07 02:17:11 Log key : 4 Trigger count : 1 Trigger event : IPv6 mode changed SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0.001 SPF nodes: 3 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 1 PRC 0 Add: 0 modify: 0 delete: 0 Route summary 0 Summary route nodes: 0 Total 0.001 Log date : 2015-09-07 01:09:33 Log key : 3 Trigger count : 2 Trigger event : DIS changed SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF nodes: 3

BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 1 PRC 0 Add: 0 modify: 0 delete: 0 Route summary 0 Summary route nodes: 0 Total 0 Log date : 2015-09-07 01:09:25 Log key : 2 Trigger count : 2 Trigger event : LSP updated SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF links changed: 1 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 1 PRC 0 Add: 0 modify: 0 delete: 0 Route summary 0 Summary route nodes: 0 Total 0 Log date : 2015-09-07 01:08:49 Log key : 1 Trigger count : 1 Trigger event : Area address changed SPF details :
Phase Duration Description TE tunnel ADJ 0 TE SPF nodes: 0 Topology 0 SPF nodes: 0 BSPF 0 Candidate NBRs: 0 LFA 0 LFA SPF nodes: 0 Area 0 Area addresses: 1 PRC 0 Add: 0 modify: 0 delete: 0 Route summary 0 Summary route nodes: 0 Total 0表1-6 display isis event-log spf ipv6 命令显示信息描述表字段 描述Date 路由计算开始日期Time 路由计算开始时间Duration 路由计算持续时间，单位为秒，精确到小数点后六位触发当前路由计算的事件计数Count

字段 描述最后一次触发路由计算的事件类型：
•NextHop changed：下一跳发生变化
• DIS changed：DIS 发生变化
• Interface metric changed：接口链路开销发生变化
• Interface MTR information changed：接口 MTR 相关信息发生变化
• SPF link changed：SPF link 发送变化
• Default route changed：缺省路由发生变化
• Summary route changed：聚合路由发生变化
• updated：TE 隧道更新TE tunnel
• TE tunnel metirc changed：TE 隧道链路开销变化
• changed：IPv6 分拓扑模式发生变化IPv6 mode
• FRR configuration changed：FRR 配置变化
• Prefix priority configuration changed：前缀优先级配置变化
• Route preference changed：路由优先级配置发生变化
• ISPF configuration changed：ISPF 配置发生变化
• Import filter policy changed：接收路由信息过滤策略变化
• ECMP configuration changed：等价路由条数规格配置变化
• changed：PIC 配置发生变化PIC configuration
• Interface LFA exclude changed：接口不参与 LFA 计算配置发生变化Trigger event
• changed：ATT 配置发生变化ATT configuration
• GR/NSR first SPF：GR/NSR 过程中第一次路由计算
• GR over：GR 过程结束
• T3 timeout：T3 定时器超时
• Direct route changed：直连路由变化
• Logic interface changed：逻辑接口变化
• Route leakage configuration changed：路由渗透配置变化
• over：NSR 过程结束NSR
• Entered overload state：协议进入过载状态
• state：协议离开过载状态Exited overload
• Area address changed：区域地址变化
•Route policy changed：路由策略变化
• Redistributed route updated：引入路由更新
• LSP updated：LSP 更新
• MT disabled：拓扑去使能
• MT enabled：拓扑使能
• TE tunnel configuration changed ： TE 隧道配置变化
• TE tunnel destination changed：TE 隧道目的地址变化
• smooth：RIB 平滑RIB Log date 路由计算日志的生成时间

字段 描述Log key 路由计算日志Key Trigger count 触发当前路由计算的事件计数路由计算各阶段详细信息SPF details路由计算阶段：
• TE tunnel ADJ：TE 隧道邻居发布计算阶段
• Topology：拓扑计算阶段
• BSPF：备份 SPF 计算阶段Phase
• LFA：LFA 计算阶段
• Area：区域计算阶段
• PRC：前缀计算阶段
• Route summary：路由聚合计算阶段路由计算阶段的描述信息：
• TE SPF nodes：表示 TE 隧道邻居发布计算的 SPF 节点数
• SPF nodes：表示拓扑计算的 SPF 节点数
• NBRs：表示候选邻居节点计数Candidate Description • LFA SPF nodes：表示 LFA 计算的 SPF 节点数
• addresses：表示区域地址计算的区域地址个数Area
• Add、modify 和 delete：表示前缀计算汇总信息
• Last 10 routes：表示最后计算的 10 条路由信息
• Summary route nodes：表示聚合路由计算的聚合节点数Total 路由计算各阶段持续时间总和【相关命令】
• reset isis event-log spf

##### 1.1.15 display isis graceful-restart status

命令用来显示 协议的 状态。
display isis graceful-restart status IS-IS GR【命令】
display isis graceful-restart status [ level-1 | level-2 ] [ process-id ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
level-1：表示 级别的 状态。
Level-1 IS-IS GR

level-2：表示 Level-2 级别的 IS-IS GR 状态。
process-id：IS-IS 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 IS-IS 进程的 状态。
GR【举例】
\# 显示 IS-IS 协议的 GR 状态。
<Sysname> display isis graceful-restart status Restart information for IS-IS(1)
-------------------------------- Restart status: COMPLETE Restart phase: Finish Restart t1: 3, count 10; Restart t2: 60; Restart t3: 300 SA Bit: supported Level-1 restart information
--------------------------- Total number of interfaces: 1 Number of waiting LSPs: 0 Level-2 restart information
--------------------------- Total number of interfaces: 1 Number of waiting LSPs: 0表1-7 命令显示信息描述表display isis graceful-restart status字段 描述当前设备的Restarter状态：
• RESTARTING：保证能进行转发Restart status
• STARTING：不能保证转发
• COMPLETE：完成GR当前设备的Restart阶段：
• Initialization：初始化
• LSDB synchronization：LSDB 同步
• First SPF computation：第一次路由计算Restart phase • Redistribution：引入路由
• Second SPF computation：第二次路由计算
• stability：准备生成LSP LSP
• LSP generation：LSP 生成和泛洪
• Finish：完成Restart t1 T1 定时器的超时值，单位为秒count T1定时器的超时次数Restart t2 T2定时器的超时值，单位为秒

字段 描述Restart t3 T3定时器的超时值，单位为秒路由器是否支持SA：
SA Bit • supported：支持
• Not supported：不支持Total number of interfaces 当前Level使能的IS-IS接口数Number of waiting LSPs GR Restarter从GR Helper进行LSDB同步时，当前Level未完成同步的LSP数目

##### 1.1.16 display isis interface

display isis interface 命令用来显示 IS-IS 的接口信息。
【命令】
display isis interface [ [ interface-type interface-number ] [ verbose ] | statistics ] [ process-id ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
interface-type interface-number：显示指定接口的信息。如果未指定本参数，将显示所有接口的信息。
verbose：显示接口的详细信息。如果未指定该参数，将显示接口的概要信息。
statistics：显示接口的统计信息。
process-id：IS-IS 进程号，取值范围为 1～65535，显示与指定 IS-IS 进程相关联接口的信息。
如果未指定本参数，将显示所有 IS-IS 进程的接口信息。
【举例】
显示使能 功能接口的概要信息。
\# IS-IS <Sysname> display isis interface Interface information for IS-IS(1)
---------------------------------- Interface: Vlan-interface100 Index IPv4 state IPv6 state CircuitID MTU Type DIS 00001 Up Down 1 1497 L1/L2 No/No \# 显示使能 IS-IS 功能接口的详细信息。
<Sysname> display isis interface verbose

Interface information for IS-IS(1)
---------------------------------- Interface: Vlan-interface100 Index IPv4 state IPv6 state CircuitID MTU Type DIS 00001 Up Down 1 1497 L1/L2 No/No SNPA address : 000c-29e8-1bd5 IP address : 192.168.220.10 Secondary IP address(es) :
IPv6 link-local address :
Extended circuit ID : 1 CSNP timer value : L1 10 L2 10 Hello timer value : 10 Hello multiplier value : 3 LSP timer value : L12 33 LSP transmit-throttle count : L12 5 Cost : L1 100 L2 100 IPv6 cost : L1 10 L2 10 Priority : L1 64 L2 64 Retransmit timer value : L12 5 LDP state : L1 Init L2 No-LDP LDP sync state : L1 Init L2 Achieved MPLS TE status : L1 Disabled L2 Disabled IPv4 BFD : Disabled IPv6 BFD : Disabled IPv4 FRR LFA backup : Enabled IPv6 FRR LFA backup : Enabled IPv4 prefix-suppression : Disabled IPv6 prefix-suppression : Disabled IPv4 tag : 1 IPv6 tag : 4294967295 IPv4 primary path detection mode: BFD ctrl IPv6 primary path detection mode: BFD ctrl表1-8 display isis interface 显示信息描述表字段 描述Interface 接口类型和接口编号Index 接口索引IPv4 state IPv4状态：Up和Down IPv6状态：Up和Down IPv6 state链路ID：
CircuitID
• 0(Invalid)：表示广播类型的网络接口关联 IS-IS 进程后，IS-IS 功能未成功使能接口MTU值MTU Type 接口的链路邻接关系类型

字段 描述是否被选举为DIS：
•“--”表示不进行 DIS 选举（P2P 网络）
DIS
• “/”左侧表示是否被选举为 Level-1 的 DIS，右侧表示是否被选举为 Level-2 的 DIS SNPA address 子网连接点地址主IP地址IP address Secondary IP address(es) 从IP地址IPv6 link-local address IPv6链路本地地址Extended circuit ID 扩展链路ID，点对点链路存在该项CSNP报文发送时间间隔CSNP timer value Hello timer value Hello报文发送时间间隔Hello multiplier value Hello报文失效数目发送LSP的最小时间间隔LSP timer value LSP transmit-throttle count 每次发送LSP的数目Cost 接口的链路开销值IPv6 cost 接口的IPv6链路开销值DIS优先级Priority Retransmit timer value LSP在点到点链路上的重传时间间隔是否使能IS-IS的MPLS TE功能：
• Enabled：表示使能MPLS TE status MPLS TE
• Disabled：表示未使能 MPLS TE LDP状态：
• Init：表示处于初始化状态，LDP 还没有上报状态LDP state • No-LDP：表示未配置 LDP
• ready：表示未建立 会话Not LDP
• Ready：表示已建立 LDP 会话LDP同步状态：
• Init：表示初始化LDP sync state
• Achieved：表示已同步
• Max cost：表示保持最大开销值是否使能IS-IS的BFD功能：
•IPv4 BFD Disabled：表示未使能
• Enabled：表示使能

字段 描述是否使能IPv6 IS-IS的BFD功能：
•IPv6 BFD Disabled：表示未使能
• Enabled：表示使能是否使能IPv4的路由LFA计算功能
• Disabled：表示未使能IPv4 FRR LFA backup
• Enabled：表示使能是否使能IPv6的路由LFA计算功能IPv6 FRR LFA backup • Disabled：表示未使能
• Enabled：表示使能是否使能IS-IS的前缀抑制功能IPv4 prefix-suppression • Disabled：表示未使能
• Enabled：表示使能是否使能IPv6 IS-IS的前缀抑制功能IPv6 prefix-suppression • Disabled：表示未使能
• Enabled：表示使能IPv4 tag 接口IPv4 tag值IPv6 tag 接口IPv6 tag值
• IPv4 主链路检测方式：
IPv4 primary path detection mode • ctrl：BFD 控制报文检测方式BFD
• BFD echo：BFD echo 报文检测方式
• IPv6 主链路检测方式：
IPv6 primary path detection mode • BFD ctrl：BFD 控制报文检测方式
• BFD echo：BFD echo 报文检测方式\# 显示 IS-IS 接口的统计信息。
<Sysname> display isis interface statistics Interface statistics information for IS-IS(1)
-------------------------------------------- Type IPv4 up/down IPv6 up/down LAN 1/0 0/0 P2P 0/0 0/0表1-9 display isis interface statistics 显示信息描述表字段 描述接口类型，取值为：
Type • LAN：表示接口的网络类型为广播
• P2P：表示接口的网络类型为点对点

字段 描述IPv4 up 使能IS-IS功能且状态为up的接口数IPv4 down 使能IS-IS功能且状态为down的接口数使能IPv6 IS-IS功能且状态为up的接口数IPv6 up IPv6 down 使能IPv6 IS-IS功能且状态为down的接口数

##### 1.1.17 display isis lsdb

display isis lsdb 命令用来显示 IS-IS 的链路状态数据库信息。
【命令】
display isis lsdb [ [ level-1 | level-2 ] | local | [ lsp-id lspid | lsp-name lspname ] | verbose ] * [ process-id ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
level-1：显示 Level-1 链路状态数据库。
level-2：显示 Level-2 链路状态数据库。
local：显示当前路由器产生的 LSP 的信息。
lsp-id lspid：LSP 标识，形式为 SYSID.Pseudonode ID-fragment num，其中，SYSID 是产生该 LSP 的节点或伪节点的 SystemID，Pseudonode ID 是伪节点 ID，fragment num 是该 LSP 的分片号。
lspname：LSP 名称，形式为 Symbolic name.[Pseudo ID]-fragment num。
lsp-name verbose：显示链路状态数据库中的 LSP 的详细信息。如果未指定该参数，将显示链路状态数据库中的 的概要信息。
LSP process-id：IS-IS 进程号，取值范围为 1～65535，显示指定 进程的链路状态数据库信息。
IS-IS如果未指定本参数，将显示所有 IS-IS 进程的链路状态数据库信息。
【使用指导】
如果未指定级别，将同时显示 Level-1 和 Level-2 的链路状态数据库信息。
【举例】
\# 显示 Level-1 链路状态数据库的概要信息。
<Sysname> display isis lsdb level-1 Database information for IS-IS(1)
--------------------------------

Level-1 Link State Database
--------------------------- LSPID Seq Num Checksum Holdtime Length ATT/P/OL
------------------------------------------------------------------------------- 0000.0000.0001.00-00* 0x00000087 0xf846 1152 183 0/0/0 0000.0000.0003.00-00 0x00000005 0x4bee 520 177 0/0/0 0000.0000.0003.00-01 0x00000004 0x7245 520 45 0/0/0 0000.0000.0011.00-00 0x0000000b 0xcdf6 815 183 0/0/0
*-Self LSP, +-Self LSP(Extended), ATT-Attached, P-Partition, OL-Overload \# 显示 Level-1 链路状态数据库的详细信息。
<Sysname> display isis lsdb level-1 verbose Database information for IS-IS(1)
-------------------------------- Level-1 Link State Database
--------------------------- LSPID Seq Num Checksum Holdtime Length ATT/P/OL
------------------------------------------------------------------------------- 0000.0000.0001.00-00* 0x00000080 0x73f 1185 183 0/0/0 Source 0000.0000.0001.00 NLPID IPv4 Area address 10 IPv4 address 192.168.220.10 MT ID 0000 (-/-)
MT ID 0002 (-/-)
MT ID 0006 (-/-)
+NBR ID 0000.0000.0011.00 Cost: 100 IPv6 unicast NBR ID 6464.6464.6464.01 Cost: 10 MT ID: 2 MT NBR ID 6464.6464.6464.01 Cost: 10 MT ID: 6 +IP-Extended
192.168.220.0 255.255.255.0 Cost: 100 IPv4 unicast
1.1.1.1 255.255.255.255 Cost: 0 MT ID: 6 IPv4 unicast
10.10.10.0 255.255.255.0 Cost: 10 MT ID: 6 IPv6 unicast 1:1:1::1/128 Cost: 0 MT ID: 2 IPv6 unicast 10:10:10::/64 Cost: 10 MT ID: 2 Router ID 1.1.1.1

0000.0000.0003.00-00 0x00000005 0x4bee 887 177 0/0/0 Source 0000.0000.0003.00 NLPID IPv4 Area address 10 IPv4 address 10.10.10.10 IPv4 address 192.168.220.20 +NBR ID 0000.0000.0001.00 Cost: 10 Router ID 3.3.3.3 0000.0000.0003.00-01 0x00000004 0x7245 887 45 0/0/0 Source 0000.0000.0003.00 +IP-Extended
10.10.10.0 255.255.255.0 Cost: 10 +IP-Extended
192.168.220.0 255.255.255.0 Cost: 10
*-Self LSP, +-Self LSP(Extended), ATT-Attached, P-Partition, OL-Overload表1-10 display isis lsdb 命令显示信息描述表字段 描述LSPID 链路状态报文ID LSP序列号Seq Num Checksum LSP校验和Holdtime LSP生存时间，随着时间推移递减LSP长度Length LSP中ATT（Attach bit）、P（Partition bit）、OL（Overload bit）的置位情况，1 ATT/P/OL表示置位，0表示没有置位Source LSP生成路由器的System ID HOST NAME LSP生成路由器的动态主机名ORG ID LSP生成路由器配置的虚拟系统所对应的原始系统ID NLPID LSP生成路由器运行的网络层协议Area address LSP生成路由器的区域地址LSP生成路由器使能IS-IS功能接口的IP地址IPv4 address IPv6 address LSP生成路由器使能IPv6 IS-IS功能接口的IPv6地址LSP生成路由器支持的拓扑信息MT ID 0000 (-/-)
MT ID 0002 (-/-) 0000 表示标准拓扑， 0002 表示 IPv6 单播拓扑， 0006 表示 IPv4 单播拓扑MT ID 0006 (-/-) (-/-)，即ATT/OL NBR ID LSP生成路由器邻居的System ID

字段 描述MT NBR ID LSP生成路由器的IPv4单播拓扑邻居信息IPv6 unicast NBR ID LSP生成路由器的IPv6单播邻居信息路由器ID Router ID IP-Internal LSP生成路由器的IP内部可达地址和掩码信息IP-External LSP生成路由器的IP外部可达地址和掩码信息IP-Extended LSP生成路由器的扩展IP可达地址和掩码信息开销值Cost Auth LSP生成路由器的认证信息IPV6 LSP生成路由器的IP内部可达IPv6地址和前缀信息LSP生成路由器的IP外部可达IPv6地址和前缀信息IPV6-Ext IPv4 unicast LSP生成路由器的IPv4单播可达信息IPv6 unicast LSP生成路由器的IPv6单播内部可达信息IPv6 unicast-ext LSP生成路由器的IPv6单播外部可达信息

##### 1.1.18 display isis lsdb statistics

命令用来显示 IS-IS 链路状态数据库的统计信息。
display isis lsdb statistics【命令】
display isis lsdb statistics [ level-1 | level-2 ] [ process-id ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
level-1：显示 Level-1 的 IS-IS 链路状态数据库的统计信息。
level-2：显示 Level-2 的 IS-IS 链路状态数据库的统计信息。
process-id：IS-IS 进程号，取值范围为 1～65535，显示指定 IS-IS 进程的链路状态数据库的统计信息。如果不指定本参数，则显示所有 IS-IS 进程的链路状态数据库的统计信息。
【使用指导】
如果不指定级别，则同时显示 和 的链路状态数据库的统计信息。
Level-1 Level-2【举例】
\# 显示 IS-IS 链路状态数据库的统计信息。
<Sysname> display isis lsdb statistics

Database Statistics information for IS-IS(1)
----------------------------------------- Level-1 LSDB Statistics
----------------------- LSP source ID LSP count
-------------------------------------------------------------------------------- Total 333 1111.1111.1111.00 1 2222.2222.2222.00 256 2222.2222.2222.01 1 bbbb.bbbb.0001.00 75 Level-2 LSDB Statistics
----------------------- LSP source ID LSP count
-------------------------------------------------------------------------------- Total 663 1111.1111.1111.00 256 2222.2222.2222.00 256 2222.2222.2222.01 1 aaaa.aaaa.0001.00 75 bbbb.bbbb.0001.00 75表1-11 display isis lsdb statistics 命令显示信息描述表字段 描述LSP source ID 产生LSP的Source ID同一Source ID产生的LSP数目LSP count Total 所有的Source ID产生的LSP的总数【相关命令】
• display isis lsdb

##### 1.1.19 display isis name-table

display isis name-table 命令用来显示系统 ID 到主机名称的映射关系表。
【命令】
display isis name-table [ process-id ]【视图】
任意视图

【缺省用户角色】
network-admin network-operator【参数】
process-id：IS-IS 进程号，取值范围为 1～65535，显示指定 IS-IS 进程系统 ID 到主机名称的映射关系表。如果未指定本参数，将显示所有 进程系统 到主机名称的映射关系表。
IS-IS ID【举例】
\# 显示系统 ID 到主机名称的映射关系表。
<Sysname> display isis name-table Name table information for IS-IS(1)
----------------------------------- System ID Hostname Type Level 6789.0000.0001 RUTA DYNAMIC Level-1 6789.0000.0001 RUTA DYNAMIC Level-2 0000.0000.0041 RUTB STATIC Level-1 0000.0000.0041 RUTB STATIC Level-2 6789.0000.0001.01 DIS-A DYNAMIC Level-1 0000.0000.0041.01 DIS-B DYNAMIC Level-2表1-12 display isis name-table 命令显示信息描述表字段 描述System ID 系统ID Hostname 主机名称系统ID与主机名称映射关系的生成方式，其中：
Type • DYNAMIC：表示映射关系是动态生成的
• STATIC：表示映射关系是通过静态配置的系统ID与主机名称映射关系生效的Level Level • Level-1：表示该映射关系在 Level-1 生效
• Level-2：表示该映射关系在 Level-2 生效

##### 1.1.20 display isis non-stop-routing status

命令用来显示 IS-IS 的 NSR 状态。
display isis non-stop-routing status【命令】
display isis non-stop-routing status【视图】
任意视图【缺省用户角色】
network-admin

network-operator【举例】
显示 的 状态。
\# IS-IS NSR <Sysname> display isis non-stop-routing status Nonstop Routing information for IS-IS(1)
---------------------------------------- NSR phase: Finish表1-13 命令显示信息描述表display isis non-stop-routing status字段 描述NSR阶段：
• Initialization：初始化
• Smooth：平滑
• computation：第一次路由计算First SPF NSR phase • Redistribution：引入路由
•Second SPF computation：第二次路由计算
• LSP stability：准备生成 LSP
• LSP generation：LSP 生成和泛洪
• Finish：完成

##### 1.1.21 display isis packet

display isis packet 命令用来显示 IS-IS 报文的统计信息。
【命令】
display isis packet { csnp | hello | lsp | psnp } by-interface [ verbose ] [ interface-type interface-number ] [ process-id ] display isis packet { csnp | hello | lsp | psnp } [ verbose ] [ process-id ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
csnp：显示 CSNP 报文的统计信息。
hello：显示 Hello 报文的统计信息。
lsp：显示 LSP 报文的统计信息。
psnp：显示 PSNP 报文的统计信息。
by-interface：按接口显示报文的统计信息。

verbose：显示报文统计的详细信息。
interface-number：接口类型和编号。显示指定接口上 IS-IS 报文的统计信interface-type息。如果未指定本参数，将显示所有接口上 报文的统计信息。
IS-IS process-id：IS-IS 进程号，取值范围为 1～65535，显示指定 进程的报文统计信息。如果IS-IS未指定本参数，将显示所有 IS-IS 进程的报文统计信息。
【举例】
\# 按接口显示 hello 报文统计的详细信息。
<Sysname> display isis packet hello by-interface verbose Hello packet information for IS-IS(1)
------------------------------------- Interface: Vlan-interface10 Total output packets : 0 Total output error packets : 0 Total input packets : 0 Total input error packets : 0 Input packets with errors Bad packet length : 0 Bad header length : 0 Jumbo packet : 0 Bad protocol description : 0 Bad protocol ID : 0 Bad protocol version : 0 Unknown packet type : 0 Bad max area count : 0 Bad system ID length : 0 Bad circuit type : 0 Bad auth TLV: 0 Bad area address TLV : 0 Auth failure : 0 Excessive area addresses : 0 Bad NBR TLV : 0 Excessive auth TLVs : 0 Excessive IF Addr TLVs: 0 Excessive IF addresses : 0 Bad IF address TLV : 0 Duplicate system ID : 0 Bad TLV length : 0 Bad IP address : 0 Duplicate IP address : 0 Mismatched area address : 0 Mismatched protocol : 0 Mismatched network type : 0 Bad IPv6 address TLV : 0 Bad IPv6 address : 0 Duplicate IPv6 address: 0 Bad MT ID TLV : 0 SNPA conflict (LAN) : 0 Excessive NBR SNPAs (LAN) : 0 Mismatched level (LAN): 0 Bad 3-Way option TLV (P2P) : 0 No common MT ID (P2P) : 0 Bad circuit ID (P2P) : 0 \# 显示 hello 报文统计的详细信息。
<Sysname> display isis packet hello verbose Hello packet information for IS-IS(1)
------------------------------------- Total output packets : 0 Total output error packets : 0 Total input packets : 0 Total input error packets : 0 Input packets with errors Bad packet length : 0 Bad header length : 0

Jumbo packet : 0 Bad protocol description : 0 Bad protocol ID : 0 Bad protocol version : 0 Unknown packet type : 0 Bad max area count : 0 Bad system ID length : 0 Bad circuit type : 0 Bad auth TLV : 0 Bad area address TLV : 0 Auth failure : 0 Excessive area addresses : 0 Bad NBR TLV : 0 Excessive auth TLVs : 0 Excessive IF Addr TLVs : 0 Excessive IF addresses : 0 Bad IF address TLV : 0 Duplicate system ID : 0 Bad TLV length : 0 Bad IP address : 0 Duplicate IP address : 0 Mismatched area address : 0 Mismatched protocol : 0 Mismatched network type : 0 Bad IPv6 address TLV : 0 Bad IPv6 address : 0 Duplicate IPv6 address : 0 Bad MT ID TLV : 0 SNPA conflict (LAN) : 0 Excessive NBR SNPAs (LAN) : 0 Mismatched level (LAN) : 0 Bad 3-Way option TLV (P2P) : 0 No common MT ID (P2P) : 0 Bad circuit ID (P2P) : 0表1-14 display isis packet hello 命令显示信息描述表字段 描述Interface 报文统计信息所在接口发送报文总数Total output packets Total output packets with errors 发送报文失败总数Total input packets 接收报文总数接收报文错误总数Total input packets with errors

字段 描述接收报文错误类型：
•Bad packet length：报文长度错误
• Bad header length：报文头长度错误
• Jumbo packet：报文长度过长，即 hello 报文大于接口 MTU，或大于报文接收缓冲区
• Bad protocol description：协议描述符错误
• Bad protocol ID：协议描述符错误
• Bad protocol version：协议版本号错误
• Unknown packet type：未识别的报文类型
• Bad max area count：最大区域地址数错误
• Bad system ID length：System ID 长度错误
• type：接口类型错误Bad circuit
• Bad auth TLV：认证 TLV 错误
• TLV：区域地址 错误Bad area address TLV
• Auth failure：认证失败
• Excessive area addresses：区域地址过多
• Bad NBR TLV：邻居 TLV 错误
• Excessive auth TLVs：多个认证 TLV Input packets with errors
• Excessive IF Addr TLVs：多个接口地址 TLV
• Excessive IF addresses：过多接口地址
• TLV：接口地址 错误Bad IF address TLV
• Duplicate system ID：重复的 System ID
• length：TLV 长度错误Bad TLV
• Bad IP address：IP 地址不可用，即与本接口地址不在同一网段
• Duplicate IP address：IP 地址重复
• Mismatched area address：区域地址不匹配
• Mismatched protocol：协议不匹配
• Mismatched network type：网络类型不匹配
• Bad IPv6 address TLV：IPv6 地址 TLV 错误
• address：IPv6 地址错误Bad IPv6
• Duplicate IPv6 address：IPv6 地址重复
• (LAN)：SNPA 地址冲突SNPA conflict
• Excessive NBR SNPAs (LAN)：过多邻居 SNPA 地址
•Mismatched level (LAN)：Level 不匹配
• Bad 3-Way option TLV (P2P)：三次握手信息错误
• Bad circuit ID (P2P)：接口链路 ID 错误\# 按接口显示 LSP 报文统计的详细信息。
<Sysname> display isis packet lsp by-interface verbose

LSP packet information for IS-IS(1)
----------------------------------- Interface: Vlan-interface10 Total output packets : 0 Total output error packets : 0 Total input packets : 0 Total input error packets : 0 Input packets with errors Bad packet length : 0 Bad header length : 0 Jumbo packet : 0 SNPA conflict (LAN) : 0 Smaller than header : 0 Bad protocol description : 0 Bad protocol ID : 0 Bad protocol version : 0 Unknown packet type : 0 Bad max area count : 0 No active NBR : 0 Bad system ID length : 0 Mismatched level : 0 Illegal IS type : 0 Sequence number is 0: 0 Checksum is 0 : 0 Incorrect checksum : 0 Bad TLV length : 0 Mismatched protocol : 0 Bad auth TLV : 0 Auth failure : 0 Excessive auth TLVs : 0 Bad NBR TLV : 0 Bad extended IS TLV : 0 Bad IF address TLV : 0 Bad IPv6 IF address TLV : 0 Bad alias TLV : 0 Bad IP reachability TLV : 0 Bad MT IS TLV : 0 Bad area address TLV : 0 Bad MT ID TLV : 0 Bad MT IP TLV : 0 Bad MT IPv6 TLV : 0 Bad IPv6 reachability TLV: 0 Bad router ID TLV : 0 \# 显示 LSP 报文统计的详细信息。
<Sysname> display isis packet lsp verbose LSP packet information for IS-IS(1)
----------------------------------- Total output packets : 0 Total output error packets : 0 Total input packets : 0 Total input error packets : 0 Input packets with errors Bad packet length : 0 Bad header length : 0 Jumbo packet : 0 SNPA conflict (LAN) : 0 Smaller than header : 0 Bad protocol description : 0 Bad protocol ID : 0 Bad protocol version : 0 Unknown packet type : 0 Bad max area count : 0 No active NBR : 0 Bad system ID length : 0 Mismatched level : 0 Illegal IS type : 0 Sequence number is 0 : 0 Checksum is 0 : 0 Incorrect checksum : 0 Bad TLV length : 0 Mismatched protocol : 0 Bad auth TLV : 0 Auth failure : 0 Excessive auth TLVs : 0 Bad NBR TLV : 0 Bad extended IS TLV : 0

Bad IF address TLV : 0 Bad IPv6 IF address TLV : 0 Bad alias TLV : 0 Bad IP reachability TLV : 0 Bad MT IS TLV : 0 Bad area address TLV : 0 Bad MT ID TLV : 0 Bad MT IP TLV : 0 Bad MT IPv6 TLV : 0 Bad IPv6 reachability TLV : 0 Bad router ID TLV : 0表1-15 display isis packet lsp 命令显示信息描述表字段 描述Interface 接口的报文统计信息Total output packets 发送报文总数Total output packets with errors 发送报文失败总数接收报文总数Total input packets Total input packets with errors 接收报文错误总数

字段 描述接收报文错误类型：
•Bad packet length：报文长度错误
• Bad header length：报文头长度错误
• Jumbo packet：报文长度过长，即报文长度大于LSP可接收的最大长度
• SNPA conflict (LAN)：SNPA 地址冲突
• Smaller than header：LSP 头部长度小于固定头长度
• Bad protocol description：协议描述符错误
• Bad protocol ID：协议标识符错误
• version：协议版本错误Bad protocol
• Unknown packet type：未识别的报文类型
• count：最大区域地址数错误Bad max area
• No active NBR：收到未知邻居发来的 LSP 报文
• Bad system ID length：System ID 长度错误
• Mismatched level：Level 不匹配
• Illegal IS type：无效的 IS 类型
• Sequence number is 0：列号为 0 Input packets with errors • Checksum is 0：校验和为 0
• checksum：校验和错误Incorrect
• Bad TLV length：TLV 长度错误
• protocol：协议不匹配Mismatched
• Bad auth TLV：认证 TLV 错误
• Auth failure：认证失败
• Excessive auth TLVs：多个认证 TLV
• Bad NBR TLV：邻居 TLV 错误
• Bad extended IS TLV：扩展 IS TLV 错误
• Bad IF address TLV：接口地址 TLV 错误
• TLV：IPv6 接口地址 错误Bad IPv6 IF address TLV
• Bad alias TLV：别名 TLV 错误
• TLV：IP 可达 错误Bad IP reachability TLV
• Bad area address TLV：区域地址 TLV 错误
•Bad MT IPv6 TLV：拓扑 IPv6 TLV 错误
• Bad IPv6 reachability TLV：IPv6 可达 TLV 错误
• Bad router ID TLV：Router ID TLV 错误\# 按接口显示 CSNP 报文统计的详细信息。
<Sysname> display isis packet csnp by-interface verbose CSNP packet information for IS-IS(1)
------------------------------------

Interface: Vlan-interface10 Total output packets : 0 Total output error packets : 0 Total input packets : 0 Total input error packets : 0 Input packets with errors Bad packet length : 0 Bad header length : 0 Jumbo packet : 0 SNPA conflict (LAN) : 0 Smaller than header: 0 Bad protocol description: 0 Bad protocol ID : 0 Bad protocol version : 0 Unknown packet type: 0 Bad max area count : 0 No active NBR : 0 Bad system ID length : 0 Mismatched level : 0 Bad TLV length : 0 Auth failure : 0 Bad auth TLV : 0 Bad LSP TLV length : 0 Excessive auth TLVs : 0 Excessive LSPs : 0 Bad LSP ID : 0 \# 显示 CSNP 报文统计的详细信息。
<Sysname> display isis packet csnp verbose CSNP packet information for IS-IS(1)
------------------------------------ Total output packets : 0 Total output error packets : 0 Total input packets : 0 Total input error packets : 0 Input packets with errors Bad packet length : 0 Bad header length : 0 Jumbo packet : 0 SNPA conflict (LAN) : 0 Smaller than header : 0 Bad protocol description : 0 Bad protocol ID : 0 Bad protocol version : 0 Unknown packet type : 0 Bad max area count : 0 No active NBR : 0 Bad system ID length : 0 Mismatched level : 0 Bad TLV length : 0 Auth failure : 0 Bad auth TLV : 0 Bad LSP TLV length : 0 Excessive auth TLVs : 0 Excessive LSPs : 0 Bad LSP ID : 0表1-16 命令显示信息描述表display isis packet csnp字段 描述Interface 报文统计信息所在接口Total output packets 发送报文总数发送报文失败总数Total output packets with errors Total input packets 接收报文总数Total input packets with errors 接收报文错误总数

字段 描述接收报文错误类型：
•Bad packet length：报文长度错误
• Bad header length：报文头长度错误
• Jumbo packet：报文长度过长，即报文长度大于可接收的最大长度
• SNPA conflict (LAN)：SNPA 地址冲突
• Smaller than header：报文头部长度小于固定头长度
• Bad protocol description：协议描述符错误
• Bad protocol ID：协议标识符错误
• version：协议版本错误Bad protocol
• Unknown packet type：未识别的报文类型
• count：最大区域地址数错误Input packets with errors Bad max area
• No active NBR：收到未知邻居发来的报文
• Bad system ID length：System ID 长度错误
• Mismatched level：Level 不匹配
• Bad TLV length：TLV 长度错误
• Auth failure：认证失败
• Bad auth TLV：认证 TLV 错误
• length：LSP 长度错误Bad LSP TLV TLV
• Excessive auth TLVs：多个认证 TLV
• LSPs：过多Excessive LSP
• Bad LSP ID：LSP ID 错误按接口显示 报文统计的详细信息。
\# PSNP <Sysname> display isis packet psnp by-interface verbose PSNP packet information for IS-IS(1)
------------------------------------ Interface: Vlan-interface10 Total output packets : 0 Total output error packets : 0 Total input packets : 0 Total input error packets : 0 Input packets with errors Bad packet length : 0 Bad header length : 0 Jumbo packet : 0 SNPA conflict (LAN) : 0 Smaller than header: 0 Bad protocol description: 0 Bad protocol ID : 0 Bad protocol version : 0 Unknown packet type: 0 Bad max area count : 0 No active NBR : 0 Bad system ID length : 0 Mismatched level : 0 Bad TLV length : 0 Auth failure : 0 Bad auth TLV : 0 Bad LSP TLV length : 0 Excessive auth TLVs : 0

Excessive LSPs : 0 Bad LSP ID : 0 \# 显示 PSNP 报文统计的详细信息。
<Sysname> display isis packet psnp verbose PSNP packet information for IS-IS(1)
------------------------------------ Total output packets : 0 Total output error packets : 0 Total input packets : 0 Total input error packets : 0 Input packets with errors Bad packet length : 0 Bad header length : 0 Jumbo packet : 0 SNPA conflict (LAN) : 0 Smaller than header : 0 Bad protocol description : 0 Bad protocol ID : 0 Bad protocol version : 0 Unknown packet type : 0 Bad max area count : 0 No active NBR : 0 Bad system ID length : 0 Mismatched level : 0 Bad TLV length : 0 Auth failure : 0 Bad auth TLV : 0 Bad LSP TLV length : 0 Excessive auth TLVs : 0 Excessive LSPs : 0 Bad LSP ID : 0表1-17 display isis packet psnp 命令显示信息描述表字段 描述Interface 接口的报文统计信息Total output packets 发送报文总数Total output packets with errors 发送报文失败总数Total input packets 接收报文总数接收报文错误统计Total input packets with errors

字段 描述接收报文错误类型：
•Bad packet length：报文长度错误
• Bad packet length：报文头长度错误
• Jumbo packet：报文长度过长，即报文长度大于可接收的最大长度
• SNPA conflict (LAN)：SNPA 地址冲突
• Smaller than header：报文头部长度小于固定头长度
• Bad protocol description：协议描述符错误
• Bad protocol ID：协议标识符错误
• version：协议版本错误Bad protocol
• Unknown packet type：未识别的报文类型
• count：最大区域地址数错误Input packets with errors Bad max area
• No active NBR：收到未知邻居发来的报文
• Bad system ID length：System ID 长度错误
• Mismatched level：Level 不匹配
• Bad TLV length：TLV 长度错误
• Auth failure：认证失败
• Bad auth TLV：认证 TLV 错误
• length：LSP 长度错误Bad LSP TLV TLV
• Excessive auth TLVs：多个认证 TLV
• LSPs：过多Excessive LSP
• Bad LSP ID：LSP ID 错误【相关命令】
• reset isis packet

##### 1.1.22 display isis peer

display isis peer 命令用来显示 IS-IS 的邻居信息。
【命令】
display isis peer [ statistics | verbose ] [ process-id ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
statistics：显示 IS-IS 邻居的统计信息。
verbose：显示 邻居的详细信息。如果未指定该参数，将显示 邻居的概要信息。
IS-IS IS-IS

process-id：IS-IS 进程号，取值范围为 1～65535，显示指定 IS-IS 进程的邻居信息。如果未指定本参数，将显示所有 进程的邻居信息。
IS-IS【举例】
\# 显示 IS-IS 邻居的概要信息。
<Sysname> display isis peer Peer information for IS-IS(1)
----------------------------- System Id: 0000.0000.0001 Interface: Vlan100 Circuit Id: 0000.0000.0001.01 State: Up HoldTime: 27s Type: L1(L1L2) PRI: 64 System Id: 0000.0000.0001 Interface: Vlan100 Circuit Id: 0000.0000.0001.01 State: Up HoldTime: 27s Type: L2(L1L2) PRI: 64 \# 显示 IS-IS 邻居的详细信息。
<Sysname> display isis peer verbose Peer information for IS-IS(1)
---------------------------- System ID: 0000.1111.2222 Interface: Vlan100 Circuit Id: 0000.1111.2222.01 State: Up Holdtime: 6s Type: L1(L1L2) PRI: 64 Area address(es): 49 Peer IP address(es): 12.0.0.2 Peer local circuit ID: 1 Peer circuit SNPA address: 000c-293b-c4be Uptime: 00:05:07 Adj protocol: IPv4 Adj P2P three-way handshake: No Graceful Restart capable Restarting signal: No Suppress adjacency advertisement: No Local topology:
Remote topology:
0 2 System ID: 0000.0000.0002 Interface: Vlan101 Circuit Id: 001 State: Up HoldTime: 27s Type: L1L2 PRI: -- Area address(es): 49 Peer IP address(es): 192.168.220.30 Peer local circuit ID: 1 Peer circuit SNPA address: 000c-29fd-ed69

Uptime: 00:05:07 Adj protocol: IPv4 Adj P2P three-way handshake: Yes Peer extended circuit ID: 2 Graceful Restart capable Restarting signal: No Suppress adjacency advertisement: No表1-18 display isis peer 命令显示信息描述表字段 描述System Id 邻居的System ID Interface 与对端相连的本地IS-IS接口链路ID Circuit Id State 链路状态抑制时间，随着时间推移递减，如果在抑制时间内还没有收到邻居发送的Hello报HoldTime文，则认为邻居已经失效，如果收到了Hello报文，则抑制时间将重置为初始值链路关系类型，其中：
• L1：表示与邻居建立的链路类型为 Level-1，邻居路由器类型为 Level-1
•L2：表示与邻居建立的链路类型为 Level-2，邻居路由器类型为 Level-2 Type
• L1(L1L2)：表示与邻居建立的链路类型为 Level-1，邻居路由器类型为Level-1-2
• L2(L1L2)：表示与邻居建立的链路类型为 Level-2，邻居路由器类型为Level-1-2 PRI 邻居接口DIS优先级Area address(es) 邻居所在区域地址Peer IP address(es) 邻居接口的IP地址邻居接口的IPv6地址Peer IPv6 address(es)
Uptime 邻居关系保持时间Adj Protocol 邻接协议：IPv4或IPv6 Peer local circuit ID 邻居链路ID邻居子网连接点地址Peer circuit SNPA address Adj P2P three-way邻居是否支持P2P三次握手handshake Peer extended circuit ID 邻居接口的扩展链路ID，邻居支持三次握手时存在该项Graceful Restart capable GR Helper能力Restarting signal RR标记Suppress adjacency SA标记advertisement Local topology 本端接口支持的拓扑列表邻居接口支持的拓扑列表Remote topology

\# 显示 IS-IS 邻居的统计信息。
<Sysname> display isis peer statistics Peer Statistics information for IS-IS(1)
--------------------------------------- Type IPv4 Up/Init IPv6 Up/Init LAN Level-1 1/0 0/0 LAN Level-2 1/0 0/0 P2P 0/0 0/0表1-19 display isis peer statistics 命令显示信息描述表字段 描述邻居类型，取值为：
• LAN Level-1：表示网络类型为广播的 Level-1 邻居个数Type
• LAN Level-2：表示网络类型为广播的 Level-2 邻居个数
• P2P：表示网络类型为点对点的邻居个数IPv4 Up 状态为up的IPv4邻居个数IPv4 Init 状态为init的IPv4邻居个数状态为up的IPv6邻居个数IPv6 Up IPv6 Init 状态为init的IPv6邻居个数

##### 1.1.23 display isis redistribute

命令用来显示 引入路由的信息。
display isis redistribute IS-IS【命令】
display isis redistribute [ ipv4 [ ip-address mask-length ] | ipv6 [ ipv6-address prefix-length ] ] [ level-1 | level-2 ] [ process-id ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
ipv4：显示 IS-IS 的 IPv4 引入路由信息。缺省情况下，显示 IPv4 引入路由信息。
ip-address mask-length：显示指定目的 IP 地址和掩码长度的引入路由。
ipv6：显示 的 引入路由信息。
IS-IS IPv6： 显 示 指 定 目 的 地 址 和 掩 码 长 度 的 引 入 路 由 。
ipv6-address prefix-length IPv6 prefix-length 的取值范围为 1～128。

process-id：IS-IS 进程号，取值范围为 1～65535，显示指定 IS-IS 进程的 IPv4 路由信息。
level-1：显示 Level-1 的 IS-IS 路由信息。
level-2：显示 Level-2 的 IS-IS 路由信息。
【使用指导】
如果不指定 和 参数，将显示 引入路由信息。
ipv4 ipv6 IPv4如果不指定级别，将同时显示 和 的路由信息。
Level-1 Level-2【举例】
\# 显示 IS-IS 的 IPv4 引入路由信息。
<Sysname> display isis redistribute 1 Route information for IS-IS(1)
------------------------------ Level-1 IPv4 Redistribute Table
-------------------------------- Type IPv4 Destination IntCost ExtCost Tag State
-------------------------------------------------------------------------------- D 192.168.30.0/24 0 0 Active D 11.11.11.11/32 0 0 D 10.10.10.0/24 0 0 Type: D -Direct, I -ISIS, S -Static, O -OSPF, B -BGP, R –RIP表1-20 命令显示信息描述表display isis redistribute字段 描述Route information for IS-IS(1) 指定IS-IS进程引入路由信息Level-1 IPv4 Redistribute Table Level-1的IS-IS IPv4引入路由信息Level-2 IPv4 Redistribute Table Level-2的IS-IS IPv4引入路由信息Type 引入的路由类型IPV4 Destination IPv4目的地址路由内部Cost IntCost ExtCost 路由外部Cost Tag 引入路由发布时的Tag值State 引入路由是否为最终生效路由\# 显示 IS-IS 的 IPv6 引入路由信息。
<Sysname> display isis redistribute ipv6 1 Route information for IS-IS(1)
------------------------------

Level-1 IPv6 Redistribute Table
-------------------------------- Type : direct Destination: 12:1::/64 IntCost : 0 Tag :
State : Active Level-2 IPv6 Redistribute Table
-------------------------------- Type : direct Destination: 12:1::/64 IntCost : 0 Tag :
State : Active表1-21 display isis redistribute ipv6 命令显示信息描述表字段 描述Route information for IS-IS(1) 指定IS-IS进程引入路由信息Level-1 IPv6 Redistribute Table Level-1的IS-IS IPv6引入路由信息Level-2 IPv6 Redistribute Table Level-2的IS-IS IPv6引入路由信息引入的路由类型，包括直连、ISISv6、静态、OSPFv3、BGP4+、Type RIPng Destination IPv6目的地址内部路由Cost IntCost Tag 引入路由发布时的Tag值State 引入路由是否为最终生效路由

##### 1.1.24 display isis route

命令用来显示 IS-IS 的 IPv4 路由信息。
display isis route【命令】
display isis route [ ipv4 [ ip-address mask-length ] | ipv6 [ ipv6-address prefix-length ] ] [ [ level-1 | level-2 ] | verbose ] * [ process-id ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
ipv4：显示 的 路由信息。
IS-IS IPv4 mask-length：显示指定目的 地址和掩码长度的路由。mask-length 取值范ip-address IP围为 0～32。

ipv6：显示 IS-IS 的 IPv6 路由信息。
prefix-length：显示指定目的 IPv6 地址和前缀长度的路由。prefix-length ipv6-address取值范围为 0～128。
verbose：显示 详细的路由信息。如果未指定该参数，将显示路由信息的概要信息。
IS-IS process-id：IS-IS 进程号，取值范围为 1～65535，显示指定 进程的路由信息。如果未指IS-IS定本参数，将显示所有 IS-IS 进程的路由信息。
level-1：显示 Level-1 的 IS-IS 路由信息。
level-2：显示 Level-2 的 IS-IS 路由信息。
【使用指导】
如果未指定 ipv4 和 ipv6 参数，将显示 IPv4 路由信息。
如果未指定级别，将同时显示 Level-1 和 Level-2 的路由信息。
【举例】
\# 显示 IS-IS 的 IPv4 路由信息。
<Sysname> display isis route Route information for IS-IS(1)
----------------------------- Level-1 IPv4 Forwarding Table
----------------------------- IPv4 Destination IntCost ExtCost ExitInterface NextHop Flags
-------------------------------------------------------------------------------
8.8.8.0/24 10 NULL Vlan100 Direct D/L/-
9.9.9.0/24 20 NULL Vlan100 8.8.8.5 R/L/- Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down bit set Level-2 IPv4 Forwarding Table
----------------------------- IPv4 Destination IntCost ExtCost ExitInterface NextHop Flags
-------------------------------------------------------------------------------
8.8.8.0/24 10 NULL D/L/- Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down bit set表1-22 display isis route 命令显示信息描述表字段 描述Route information for IS-IS(1) 指定IS-IS进程路由信息Level-1 IPv4 Forwarding Table Level-1的IS-IS IPv4路由信息Level-2 IPv4 Forwarding Table Level-2的IS-IS IPv4路由信息IPv4目的地址IPv4 Destination

字段 描述IntCost 路由内部Cost ExtCost 路由外部Cost出接口ExitInterface NextHop 下一跳路由状态标志
• D：直连路由
• R：该路由是否已放到路由表中Flags
•L：是否已经通过 LSP 发布
• U：路由渗透状态标识。设置为“Up”表示可以避免由 L2 发送到 L1 的 LSP 又返回给 L2，设置为“Down”表示不可以显示 的 路由详细信息。
\# IS-IS IPv4 <Sysname> display isis route verbose Route information for IS-IS(1)
----------------------------- Level-1 IPv4 Forwarding Table
----------------------------- IPV4 Dest : 8.8.8.0/24 Int. Cost : 10 Ext. Cost : NULL Admin Tag : - Src Count : 2 Flag : D/L/- NextHop : Interface : ExitIndex :
Direct Vlan100 0x00000000 Nib ID : 0x0 IPV4 Dest : 9.9.9.0/24 Int. Cost : 20 Ext. Cost : NULL Admin Tag : - Src Count : 1 Flag : R/L/- NextHop : Interface : ExitIndex :
8.8.8.5 Vlan100 0x00000003 Nib ID : 0x0 Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down bit set Level-2 IPv4 Forwarding Table
----------------------------- IPV4 Dest : 8.8.8.0/24 Int. Cost : 10 Ext. Cost : NULL Admin Tag : - Src Count : 2 Flag : D/L/- Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down bit set

表1-23 display isis route verbose 命令显示信息描述表字段 描述Route information for IS-IS(1) 指定IS-IS进程的IPv4路由信息Level-1的IS-IS IPv4路由信息Level-1 IPv4 Forwarding Table Level-2 IPv4 Forwarding Table Level-2的IS-IS IPv4路由信息IPV4 Dest IPv4目的地址路由内部Cost Int. Cost Ext. Cost 路由外部Cost Admin Tag Tag值Src Count 发布源个数路由状态标志
• R：该路由是否已放到路由表中Flag • L：是否已经通过 发布LSP
• U：路由渗透状态标识。设置为“Up”表示可以避免由 L2 发送到 L1 的 LSP 又返回给 L2，设置为“Down”表示不可以Next Hop 下一跳出接口Interface ExitIndex 出接口索引Nib ID 路由管理分配的ID，即下一跳索引显示 的路由信息。
\# IPv6 IS-IS <Sysname> display isis route ipv6 Route information for IS-IS(1)
------------------------------ Level-1 IPv6 forwarding table
----------------------------- Destination: 2001:1:: PrefixLen: 64 Flag : R/L/- Cost : 20 Next hop : FE80::200:5EFF:FE64:8905 Interface: Vlan100 Destination: 2001:2:: PrefixLen: 64 Flag : D/L/- Cost : 10 Next hop : Direct Interface: Vlan100 Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down bit set Level-2 IPv6 forwarding table
-----------------------------

Destination: 2001:1:: PrefixLen: 64 Flag : -/-/- Cost : 20 Destination: 2001:2:: PrefixLen: 64 Flag : D/L/- Cost : 10 Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down bit set表1-24 display isis route ipv6 命令显示信息描述表字段 描述Destination IPv6目的地址前缀前缀长度PrefixLen路由信息状态标志位
• D：直连路由
• R：该路由是否已放到路由表中Flag/Flags
• L：是否已经通过 LSP 发布
• U：路由渗透状态标识，标识 Level-1 路由是否来自 Level-2。如果配置为“U”则可避免由 Level-2 发送到 Level-1 的 LSP 又返回给 Level-2 Cost 开销值Next hop 下一跳Interface 出接口\# 显示 IPv6 IS-IS 的详细路由信息。
<Sysname> display isis route ipv6 verbose Route information for IS-IS(1)
------------------------------ Level-1 IPv6 forwarding table
----------------------------- IPv6 dest : 2001:1::/64 Flag : D/L/- Cost : 10 Admin tag : - Src count : 2 Nexthop : Direct Interface : Vlan101 Nib ID : 0x0 IPv6 dest : 2001:2::/64 Flag : R/-/- Cost : 20 Admin tag : - Src count : 2 Nexthop : FE80::200:5EFF:FE64:8905 Interface : Vlan101

BkNexthop : FE80::200:5EFF:FE64:8905 BkInterface : Vlan101 Nib ID : 0x24000002 Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down bit set Level-2 IPv6 Forwarding Table
----------------------------- IPv6 dest : 2001:1::/64 Flag : D/L/- Cost : 10 Admin tag : - Src count : 2 Nexthop : - Interface : - Nib ID : - IPv6 dest : 2001:2::/64 Flag : D/L/- Cost : 10 Admin tag : - Src count : 2 Nexthop : - Interface : - Nib ID : - Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down bit set表1-25 display isis route ipv6 verbose 命令显示信息描述表字段 描述IPv6 dest IPv6目的地址和前缀信息路由信息状态标志位
•D：直连路由
• R：该路由是否已放到路由表中Flag/Flags
• L：是否已经通过 LSP 发布
• U：路由渗透状态标识，标识 Level-1 路由是否来自 Level-2。如果配置为“U”则可避免由 Level-2 发送到 Level-1 的 LSP 又返回给 Level-2 Cost 开销值Admin tag 管理标记Src count 发布源个数Nexthop 下一跳Interface 出接口备份下一跳BkNexthop BkInterface 备份出接口Nib ID 路由管理分配的ID，即下一跳索引

##### 1.1.25 display isis spf-tree

display isis spf-tree 命令用来显示 IS-IS 的 IPv4 最短路径树信息。
【命令】
display isis spf-tree [ ipv4 | ipv6 ] [ [ level-1 | level-2 ] | verbose ] * [ process-id ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
ipv4：显示 IS-IS 的 IPv4 最短路径树信息。
ipv6：显示 IS-IS 的 IPv6 最短路径树信息。
level-1：显示 Level-1 的 IS-IS 最短路径树信息。如果未指定级别，将同时显示 Level-1 和 Level-2的最短路径树信息。
level-2：显示 Level-2 的 IS-IS 最短路径树信息。如果未指定级别，将同时显示 Level-1 和 Level-2的最短路径树信息。
verbose：显示 最短路径树的详细信息。如果未指定该参数，显示 最短路径树的概要IS-IS IS-IS信息。
process-id：IS-IS 进程号，取值范围为 1～65535，显示指定 IS-IS 进程的最短路径树信息。如果未指定 IS-IS 进程号，将显示所有 IS-IS 进程的最短路径树信息。
【使用指导】
如果未指定 和 参数，将显示 IPv4 最短路径树信息。
ipv4 ipv6【举例】
显示 的 最短路径树信息。
\# IS-IS IPv4 <Sysname> display isis spf-tree Shortest Path Tree for IS-IS(1)
------------------------------- Flags: S-Node is on SPF tree T-Node is on tent list O-Node is overload R-Node is directly reachable I-Node or Link is isolated D-Node or Link is to be deleted C-Neighbor is child P-Neighbor is parent V-Link is involved N-Link is a new path L-Link is on change list U-Protocol usage is changed H-Nexthop is changed Level-1 Shortest Path Tree
--------------------------

SpfNode NodeFlag SpfLink LinkCost LinkFlag
------------------------------------------------------------------------------- 0000.0000.0032.00 S/-/-/-/-/-
-->0000.0000.0032.01 10 -/-/C/-/-/-/-/-/-
-->0000.0000.0064.00 10 -/-/C/-/-/-/-/-/- 0000.0000.0032.01 S/-/-/R/-/-
-->0000.0000.0064.00 0 -/-/C/-/-/-/-/-/-
-->0000.0000.0032.00 0 -/-/-/P/-/-/-/-/- 0000.0000.0064.00 S/-/-/R/-/-
-->0000.0000.0032.00 10 -/-/-/P/-/-/-/-/-
-->0000.0000.0032.01 10 -/-/-/P/-/-/-/-/- Level-2 Shortest Path Tree
-------------------------- SpfNode NodeFlag SpfLink LinkCost LinkFlag
------------------------------------------------------------------------------- 0000.0000.0032.00 S/-/-/-/-/-
-->0000.0000.0032.01 10 -/-/C/-/-/-/-/-/-
-->0000.0000.0064.00 10 -/-/C/-/-/-/-/-/- 0000.0000.0032.01 S/-/-/R/-/-
-->0000.0000.0064.00 0 -/-/C/-/-/-/-/-/-
-->0000.0000.0032.00 0 -/-/-/P/-/-/-/-/- 0000.0000.0064.00 S/-/-/R/-/-
-->0000.0000.0032.00 10 -/-/-/P/-/-/-/-/-
-->0000.0000.0032.01 10 -/-/-/P/-/-/-/-/- \# 显示 IS-IS 的 IPv4 最短路径树的详细信息。
<Sysname> display isis spf-tree verbose Shortest Path Tree for IS-IS(1)
------------------------------- Flags: S-Node is on SPF tree T-Node is on tent list O-Node is overload R-Node is directly reachable I-Node or Link is isolated D-Node or Link is to be deleted C-Neighbor is child P-Neighbor is parent V-Link is involved N-Link is a new path L-Link is on change list U-Protocol usage is changed H-Nexthop is changed Level-1 Shortest Path Tree
-------------------------- SpfNode : 0000.0000.0001.00 Distance : 0 TE distance : 0 NodeFlag : S/-/-/-/-/-

RelayNibID : 0x0 TE tunnel count: 0 Nexthop count : 0 SpfLink count : 1
-->0000.0000.0004.04 LinkCost : 10 LinkNewCost : 10 LinkFlag : -/-/C/-/-/-/-/-/- LinkSrcCnt : 1 Type: Adjacent Interface: N/A Cost: 10 Nexthop : N/A SpfNode : 0000.0000.0004.04 Distance : 10 TE distance : 10 NodeFlag : S/-/-/R/-/- RelayNibID : 0x14000001 TE tunnel count: 0 Nexthop count : 0 SpfLink count : 2
-->0000.0000.0001.00 LinkCost : 0 LinkNewCost : 0 LinkFlag : -/-/-/P/-/-/-/-/- LinkSrcCnt : 1 Type: Remote Interface: N/A Cost: 0 Nexthop : N/A
-->0000.0000.0004.00 LinkCost : 0 LinkNewCost : 0 LinkFlag : -/-/C/-/-/-/-/-/- LinkSrcCnt : 1 Type: Remote Interface: Vlan50 Cost: 0 Nexthop : 1.1.1.3 Level-2 Shortest Path Tree
-------------------------- SpfNode : 0000.0000.0001.00 Distance : 0 TE distance : 0 NodeFlag : S/-/-/-/-/- RelayNibID : 0x0 TE tunnel count: 0 Nexthop count : 0 SpfLink count : 1
-->0000.0000.0004.04 LinkCost : 10

LinkNewCost : 10 LinkFlag : -/-/C/-/-/-/-/-/- LinkSrcCnt : 1 Type: Adjacent Interface: N/A Cost: 10 Nexthop : N/A SpfNode : 0000.0000.0004.04 Distance : 10 TE distance : 10 NodeFlag : S/-/-/R/-/- RelayNibID : 0x0 TE tunnel count: 0 Nexthop count : 0 SpfLink count : 2
-->0000.0000.0001.00 LinkCost : 0 LinkNewCost : 0 LinkFlag : -/-/-/P/-/-/-/-/- LinkSrcCnt : 1 Type: Remote Interface: N/A Cost: 0 Nexthop : N/A
-->0000.0000.0004.00 LinkCost : 0 LinkNewCost : 0 LinkFlag : -/-/C/-/-/-/-/-/- LinkSrcCnt : 1 Type: Remote Interface: Vlan50 Cost: 0 Nexthop : 1.1.1.3表1-26 display isis spf-tree 命令显示信息描述表字段 描述SpfNode 拓扑节点ID Distance 根节点到该节点的最短距离根节点到该节点的最短距离（包含隧道Link），如果未配置隧道，则与Distance值TE distance相等节点状态标记：
•S：节点在 SPF 树上
• T：节点在候选列表上NodeFlag • O：节点处于 OverLoad
• R：节点是直连的
• I：孤立节点
• D ：节点待删除RelayNibID 节点的迭代下一跳ID Nexthop count 节点的下一跳个数

字段 描述Nexthop 节点的主用下一跳地址/链路发布源下一跳地址Interface 节点的主用下一跳出接口/链路发布源下一跳出接口节点的备份下一跳地址BkNexthop BkInterface 节点的备份下一跳出接口Neighbor 节点主用下一跳邻居节点ID BkNeighbor 节点备份下一跳邻居节点ID拓扑链路SpfLink SpfLink count 拓扑链路个数LinkCost 链路开销链路新开销LinkNewCost链路状态标记：
• I：孤立链路
• D：链路待删除
• C：目的节点是源节点的子节点
• P：目的节点是源节点的父节点LinkFlag
• V：链路受到影响
•N：新增链路
• L：链路在变化链表上
• U：链路协议类型发生变化
• H：链表下一跳发生变化LinkSrcCnt 链路发布源个数链路发布源类型：
Type • Adjacent：本地邻居维护产生
• Remote：其它节点 LSP 产生链路发布源开销Cost \# 显示 IS-IS 的 IPv6 最短路径树信息。
<Sysname> display isis spf-tree ipv6 Shortest Path Tree for IS-IS(1)
------------------------------- Flags: S-Node is on SPF tree T-Node is on tent list O-Node is overload R-Node is directly reachable I-Node or Link is isolated D-Node or Link is to be deleted C-Neighbor is child P-Neighbor is parent V-Link is involved N-Link is a new path L-Link is on change list U-Protocol usage is changed

H-Nexthop is changed Level-1 Shortest Path Tree
---------------------------------- SpfNode NodeFlag SpfLink LinkCost LinkFlag
------------------------------------------------------------------------------- 0000.0000.0032.00 S/-/-/-/-/-
-->0000.0000.0032.01 10 -/-/C/-/-/-/-/-/-
-->0000.0000.0064.00 10 -/-/C/-/-/-/-/-/- 0000.0000.0032.01 S/-/-/R/-/-
-->0000.0000.0064.00 0 -/-/C/-/-/-/-/-/-
-->0000.0000.0032.00 0 -/-/-/P/-/-/-/-/- 0000.0000.0064.00 S/-/-/R/-/-
-->0000.0000.0032.00 10 -/-/-/P/-/-/-/-/-
-->0000.0000.0032.01 10 -/-/-/P/-/-/-/-/- Level-2 Shortest Path Tree
---------------------------------- SpfNode NodeFlag SpfLink LinkCost LinkFlag
------------------------------------------------------------------------------- 0000.0000.0032.00 S/-/-/-/-/-
-->0000.0000.0032.01 10 -/-/C/-/-/-/-/-/-
-->0000.0000.0064.00 10 -/-/C/-/-/-/-/-/- 0000.0000.0032.01 S/-/-/R/-/-
-->0000.0000.0064.00 0 -/-/C/-/-/-/-/-/-
-->0000.0000.0032.00 0 -/-/-/P/-/-/-/-/- 0000.0000.0064.00 S/-/-/R/-/-
-->0000.0000.0032.00 10 -/-/-/P/-/-/-/-/-
-->0000.0000.0032.01 10 -/-/-/P/-/-/-/-/- \# 显示 IS-IS Level-1 的 IPv6 最短路径树的详细信息。
<Sysname> display isis spf-tree ipv6 level-1 verbose Shortest Path Tree for IS-IS(1)
------------------------------- Flags: S-Node is on SPF tree T-Node is on tent list O-Node is overload R-Node is directly reachable I-Node or Link is isolated D-Node or Link is to be deleted C-Neighbor is child P-Neighbor is parent V-Link is involved N-Link is a new path L-Link is on change list U-Protocol usage is changed H-Nexthop is changed Level-1 Shortest Path Tree
-------------------------- SpfNode : 0000.0000.0032.00

Distance : 0 TE distance : 0 NodeFlag : S/-/-/-/-/- RelayNibID : 0x0 TE tunnel count: 0 Nexthop count : 0 SpfLink count : 2
-->0000.0000.0032.01 LinkCost : 10 LinkNewCost : 10 LinkFlag : -/-/C/-/-/-/-/-/- LinkSrcCnt : 1 Type : Adjacent Interface: N/A Cost : 10 Nexthop : N/A
-->0000.0000.0064.00 LinkCost : 10 LinkNewCost : 10 LinkFlag : -/-/C/-/-/-/-/-/- LinkSrcCnt : 1 Type : Adjacent Interface: Tun1 Cost : 10 Nexthop : FE80::A0A:A40 SpfNode : 0000.0000.0032.01 Distance : 10 TE distance : 10 NodeFlag : S/-/-/R/-/- RelayNibID : 0x0 TE tunnel count: 0 Nexthop count : 0 SpfLink count : 2
-->0000.0000.0064.00 LinkCost : 0 LinkNewCost : 0 LinkFlag : -/-/C/-/-/-/-/-/- LinkSrcCnt : 1 Type : Adjacent Interface: Vlan2 Cost : 10 Nexthop : FE80::200:12FF:FE34:1
-->0000.0000.0032.00 LinkCost : 0 LinkNewCost : 0 LinkFlag : -/-/-/P/-/-/-/-/- LinkSrcCnt : 1 Type : Adjacent Interface: N/A Cost : 0 Nexthop : N/A SpfNode : 0000.0000.0064.00 Distance : 10 TE distance : 10

NodeFlag : S/-/-/R/-/- RelayNibID : 0x0 TE tunnel count: 0 Nexthop count : 2 Neighbor : 0000.0000.0064.00 Interface : Vlan2 NextHop : FE80::200:12FF:FE34:1 BkNeighbor: N/A BkInterface: N/A BkNextHop : N/A Neighbor : 0000.0000.0064.00 Interface : Tun1 NextHop : FE80::A0A:A40 BkNeighbor: N/A BkInterface: N/A BkNextHop : N/A SpfLink count : 2
-->0000.0000.0032.00 LinkCost : 10 LinkNewCost : 10 LinkFlag : -/-/-/P/-/-/-/-/- LinkSrcCnt : 1 Type : Remote Interface: N/A Cost : 10 Nexthop : N/A AdvMtID : 0
-->0000.0000.0064.00 LinkCost : 10 LinkNewCost : 10 LinkFlag : -/-/C/-/-/-/-/-/- LinkSrcCnt : 1 Type : Remote Interface: Tun1 Cost : 10 Nexthop : FE80::A0A:A40 AdvMtID : 0表1-27 display isis spf-tree ipv6 命令显示信息描述表字段 描述SpfNode 拓扑节点ID根节点到该节点的最短距离Distance根节点到该节点的最短距离（包含隧道Link），如果未配置隧道，则TE distance与Distance值相等节点状态标记：
• S：节点在 SPF 树上
• T：节点在候选列表上NodeFlag • O：节点处于OverLoad
• R：节点是直连的
• ：孤立节点
• D：节点待删除TE tunnel count Destination为该节点的隧道条数节点的下一跳个数Nexthop count

字段 描述NextHop 节点的主用下一跳地址/链路发布源下一跳地址从哪个拓扑学到的路由：
• 0：IPv4 单播拓扑 ID AdvMtID
• 2：IPv6 单播拓扑 ID
• 6～4094：其它拓扑Interface 节点的主用下一跳出接口/链路发布源下一跳出接口BkNextHop 节点的备份下一跳地址BkInterface 节点的备份下一跳出接口Neighbor 节点主用下一跳邻居节点ID BkNeighbor 节点备份下一跳邻居节点ID SpfLink 拓扑链路拓扑链路个数SpfLink count LinkCost 链路开销LinkNewCost 链路新开销链路状态标记：
• I：孤立链路
• D：链路待删除
• C：目的节点是源节点的子节点
• P：目的节点是源节点的父节点LinkFlag
• V：链路受到影响
• N：新增链路
• L：链路在变化链表上
• U：链路协议类型发生变化
• H：链表下一跳发生变化LinkSrcCnt 链路发布源个数链路发布源类型：
Type • Adjacent：本地邻居维护产生
• Remote：其它节点 LSP 产生Cost 链路发布源开销

##### 1.1.26 display isis statistics

命令用来显示 IS-IS 的统计信息。
display isis statistics【命令】
display isis statistics [ ipv4 | ipv6 ] [ level-1 | level-1-2 | level-2 ] [ process-id ]

【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
ipv4：显示 IS-IS 的 IPv4 统计信息。如果未指定该参数，则显示 IS-IS 的 IPv4 和 IPv6 统计信息。
ipv6：显示 IS-IS 的 IPv6 统计信息。
level-1：显示 IS-IS Level-1 的统计信息。
level-1-2：显示 IS-IS Level-1-2 的统计信息。
level-2：显示 IS-IS Level-2 的统计信息。
process-id：IS-IS 进程号，取值范围为 1～65535，显示指定 IS-IS 进程的统计信息。如果未指定本参数，将显示所有 进程的统计信息。
IS-IS【使用指导】
如果未指定级别，将同时显示 Level-1 和 Level-2 的统计信息。
【举例】
\# 显示 IS-IS 的统计信息。
<Sysname> display isis statistics Statistics information for IS-IS(1)
---------------------------------- Level-1 Statistics
------------------ MTR(base)
Learnt routes information:
Total IPv4 Learnt Routes in IPv4 Routing Table: 1 Imported routes information:
IPv4 Imported Routes:
Static: 0 Direct: 0 ISIS: 0 BGP: 0 RIP: 0 OSPF: 0 Total Number: 0 MTR(base)
Learnt routes information:
Total IPv6 Learnt Routes in IPv6 Routing Table: 0 Imported routes information:

IPv6 Imported Routes:
Static: 0 Direct: 0 ISISv6: 0 BGP4+: 0 RIPng: 0 OSPFv3: 0 Total Number: 0 Lsp information:
LSP Source ID: No. of used LSPs 7777.8888.1111 001 Level-2 Statistics
------------------ MTR(base)
Learnt routes information:
Total IPv4 Learnt Routes in IPv4 Routing Table: 0 Imported routes information:
IPv4 Imported Routes:
Static: 0 Direct: 0 ISIS: 0 BGP: 0 RIP: 0 OSPF: 0 Total Number: 0 MTR(base)
Learnt routes information:
Total IPv6 Learnt Routes in IPv6 Routing Table: 0 Imported routes information:
IPv6 Imported Routes:
Static: 0 Direct: 0 ISISv6: 0 BGP4+: 0 RIPng: 0 OSPFv3: 0 Total Number: 0 Lsp information:
LSP Source ID: No. of used LSPs 7777.8888.1111 001表1-28 display isis statistics 命令显示信息描述表字段 描述Statistics information for IS-IS(processid) 指定IS-IS进程的统计信息Level-1 Statistics Level-1路由统计信息Level-2路由统计信息Level-2 Statistics

字段 描述MTR(topo-name) 指定某个拓扑，拓扑名为base则为公网拓扑学习到的路由信息：
Total IPv4 Learnt Routes in IPv4 Routing Table：学习到的IPv4 Learnt routes information 路由信息的总数Total IPv6 Learnt Routes in IPv6 Routing Table：学习到的IPv6路由信息的总数Imported routes information 路由引入信息引入IPv4路由数量：
• Static：引入的 IPv4 静态路由数量
• Direct：引入的 直连路由数量IPv4 IPv4 Imported Routes • ISIS：从其它 IS-IS 进程引入的路由数量
• BGP：从 BGP 引入的路由数量
• RIP：从 RIP 引入的路由数量
• OSPF：从 OSPF 引入的路由数量引入IPv6路由数量：
• Static：引入的 IPv6 静态路由数量
•Direct：引入的 IPv6 直连路由数量IPv6 Imported Routes • ISISv6：从其它 IS-ISv6 进程引入的路由数量
• BGP4+：从 BGP4+引入的路由数量
• RIPng：从 RIPng 引入的路由数量
• OSPFv3：从 OSPFv3 引入的路由数量LSP信息：
Lsp information • LSP Source ID：本地生成的 LSP 的 System ID
• No. of used LSPs：本地生成的 LSP 已使用的分片数量

##### 1.1.27 display osi

display osi 命令用来显示 OSI 连接的信息。
【命令】
display osi [ slot slot-number ]【视图】
任意视图【缺省用户角色】
network-admin network-operator

【参数】
slot slot-number：显示指定成员设备的 OSI 连接的信息。slot-number 表示设备在 IRF 中的成员编号。如果未指定本参数，则显示所有成员设备的连接信息。
【举例】
显示所有 连接的信息。
\# OSI <Sysname> display osi Total OSI socket number: 2 Location: slot 0 Creator: isisd[1539] State: N/A Options: SO_FILTER Error: 0 Receiving buffer(cc/hiwat/lowat/drop/state): 0 / 1048576 / 1 / 0 / N/A Sending buffer(cc/hiwat/lowat/state): 0 / 262144 / 512 / N/A Type: 2 Enabled interfaces:
Vlan-interface100 MAC address: 0180-c200-0014 Location: slot 0 Creator: isisd[1539] State: N/A Options: SO_FILTER Error: 0 Receiving buffer(cc/hiwat/lowat/drop/state): 0 / 1048576 / 1 / 0 / N/A Sending buffer(cc/hiwat/lowat/state): 0 / 262144 / 512 / N/A Type: 2 Enabled interfaces:
Vlan-interface100 MAC address: 0180-c200-0014表1-29 命令显示信息描述表display osi字段 描述Total OSI socket number OSI socket的总数创建socket的任务名称，括号中为创建者的进程号Creator State OSI socket无状态，始终显示为N/A socket的选项，OSI socket支持以下两种：
• SO_FILTER：设置了过滤选项Options
• N/A：没有设置选项Error 影响socket连接的错误接收缓冲区信息，括号中分别为：当前使用空间、最大空间、最小空间、Receiving buffer(cc/hiwat/lowat/drop/state) 丢包数、状态

字段 描述发送缓冲区信息，括号中分别为：当前使用空间、最大空间、最小空间、Sending buffer(cc/hiwat/lowat/state)
状态IS-IS使用的socket类型为2，对应无连接的、不可靠的运输层数据包协Type议接收报文时需要匹配的入接口和组播MAC地址信息，仅以太链路层接口Enabled interfaces上收到的报文需要匹配组播MAC地址

##### 1.1.28 display osi statistics

命令用来显示 连接的报文统计信息。
display osi statistics OSI【命令】
display osi statistics [ slot slot-number ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
slot-number：显示指定成员设备的 连接的报文统计信息。slot-number 表示设备在slot OSI IRF 中的成员编号。如果未指定本参数，则显示所有成员设备的报文统计信息之和。
【举例】
\# 显示 OSI 连接的报文统计信息。
<Sysname> display osi statistics Received packets:
Total: 35 Relay received: 35 Relay forwarded: 35 Invalid service slot: 0 No matched socket: 0 Not delivered, input socket full: 0 Sent packets:
Total: 19 Relay forwarded: 19 Relay received: 19 Failed: 0

表1-30 display osi statistics 命令显示信息描述表字段 描述收到的报文的统计信息：
• Total：从链路层接收的报文总数
• Relay received：业务板从其他板中继接收的入方向报文总数，该计数不计入 Total 中
• Relay forwarded：中继转发给业务板的入方向报文数Received packets
• Invalid service slot：因为业务板不可用而被丢弃的报文数
• No matched socket：因为未匹配报文入接口、或者未匹配 MAC 地址、或者不满足连接的过滤条件而被丢弃的报文数
• full：因为 接收缓Not delivered, input socket socket冲区已满而没有向上层传送的报文数发送的报文的统计信息：
•Total：IS-IS 通过 OSI 连接发送的报文总数
• Relay forwarded：中继转发给出接口所在板的出方Sent packets 向报文数，该计数不计入 Total 中
•Relay received：出接口所在板从其他板中继接收的出方向报文总数
• Failed：发送失败的报文个数【相关命令】
• reset osi statistics

##### 1.1.29 distribute bgp-ls

distribute bgp-ls 命令用来配置允许设备将 IS-IS 链路状态信息发布到 BGP。
undo distribute bgp-ls 命令用来恢复缺省情况。
【命令】
distribute bgp-ls [ instance-id id ] [ level-1 | level-2 ] undo distribute bgp-ls [ level-1 | level-2 ]【缺省情况】
不允许设备将 IS-IS 链路状态信息发布到 BGP。
【视图】
IS-IS 视图【缺省用户角色】
network-admin

【参数】
instance-id id：实例 ID，用于区分链路状态信息，取值范围为 0～65535。如果未指定本参数，则表示实例 0。
level-1：配置允许设备将 级别的链路状态信息发布到 BGP。
level-1 level-2：配置允许设备将 级别的链路状态信息发布到 BGP。
level-2【使用指导】
本功能允许设备将链路状态信息发布到 BGP，由 BGP 向外发布，以满足需要知道链路状态信息的应用的需求。IS-IS 链路状态信息随链路状态的更新同步发布。
对于具有相同实例 的不同 进程，如果它们的链路状态信息相同，设备只会将 进程号ID IS-IS IS-IS最小的链路状态信息发布到 BGP。
如果要将不同 IS-IS 进程的相同链路状态信息发布到 BGP，需要为不同的进程指定不同的实例 ID。
如果没有指定 level-1 或 level-2 参数，设备将同时允许把 level-1 和 level-2 级别的链路状态信息发布到 BGP。
对于 undo 命令，不指定任何参数表示不允许设备将 IS-IS 链路状态信息发布到 BGP。
【举例】
\# 配置允许设备将 IS-IS 进程 1 的链路状态信息发布到 BGP。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] distribute bgp-ls

##### 1.1.30 domain-authentication send-only

命令用来配置对收到的 Level-2 报文（包括 LSP、CSNP、domain-authentication send-only PSNP）忽略认证信息检查。
命令用来恢复缺省情况。
undo domain-authentication send-only【命令】
domain-authentication send-only undo domain-authentication send-only【缺省情况】
如果配置了路由域验证方式和验证密钥，对收到的报文执行认证信息检查。
【视图】
IS-IS 视图【缺省用户角色】
network-admin【使用指导】
配置路由域验证方式和验证密钥后，验证密钥将按照设定的方式插入到发送的 报文（包括Level-2 LSP、CSNP、PSNP）中，并对收到的 Level-2 报文进行验证密钥的检查。当需要更改密钥时由于密钥不匹配可能导致业务发生中断。通过命令配置对收到的 Level-2 报文忽略认证信息检查可保证业务不中断，报文正常接收。

【举例】
\# 对收到报文忽略认证信息检查。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] domain-authentication send-only【相关命令】
•area-authentication send-only
• domain-authentication-mode
• isis authentication send-only

##### 1.1.31 domain-authentication-mode

domain-authentication-mode 命令用来配置路由域验证方式和验证密钥。
undo domain-authentication-mode 命令用来恢复缺省情况。
【命令】
domain-authentication-mode { { gca key-id { hmac-sha-1 | hmac-sha-224 | hmac-sha-256 | hmac-sha-384 | hmac-sha-512 } [ nonstandard ] | md5 | simple } { cipher | plain } string | keychain keychain-name } [ ip | osi ] undo domain-authentication-mode【缺省情况】
未配置路由域验证方式和验证密钥。
【视图】
IS-IS 视图【缺省用户角色】
network-admin【参数】
gca：GCA 验证模式（Generic Authentication）。
Cryptographic key-id：唯一标识一个认证项（SA），取值范围为 1～65535。发送方将 放入认证 中，Key ID TLV接收方根据报文中提取的 Key ID 选择 SA 对报文进行认证。
hmac-sha-1：支持 HMAC-SHA-1 算法。
hmac-sha-224：支持 HMAC-SHA-224 算法。
hmac-sha-256：支持 HMAC-SHA-256 算法。
hmac-sha-384：支持 算法。
HMAC-SHA-384 hmac-sha-512：支持 算法。
HMAC-SHA-512 nonstandard：兼容非标准 验证模式。
GCA md5：MD5 验证模式。
simple：简单验证模式。
cipher：以密文方式设置密钥。

plain：以明文方式设置密钥，该密钥将以密文形式存储。
string：密钥字符串，区分大小写。明文密钥为 1～16 个字符的字符串，密文密钥为 33～53 个字符的字符串。
keychain：使用 验证模式。
keychain keychain-name：keychain 名，为 1～63 个字符的字符串，区分大小写。
ip：检查 中 的相应字段的配置内容。
LSP IP osi：检查 LSP 中 OSI 的相应字段的配置内容。
【使用指导】
配置路由域验证方式和验证密钥后，验证密钥将按照设定的方式插入到发送的 报文（包括Level-2 LSP、CSNP、PSNP）中并对收到的 Level-2 报文进行验证密钥的检查。
IS-IS 的 md5 验证模式对应于 keychain 的 HMAC-MD5 认证算法，所以 keychain 内只有使用HMAC-MD5 认证算法，才能使得 IS-IS 使用 keychain 验证模式正常工作。当 IS-IS 路由域使用验证模式时，报文的收、发过程如下：
keychain IS-IS 在发送 Level-2 报文前，会先从 keychain 获取当前的有效发送 key，根据该 key 的认证
•算法和认证密钥进行报文验证；如果当前不存在有效发送 key，或者该 key 的认证算法不是HMAC-MD5，则 IS-IS 发送的 Level-2 报文中不含认证 TLV。
• IS-IS 在收到 Level-2 报文后，会从 keychain 获取当前的有效接收 key，根据各个 key 的认证算法和认证密钥对报文进行校验，如果当前不存在有效接收 key，或者使用所有的有效接收对报文的校验都未成功，则报文校验不通过，该报文被丢弃。
key所有骨干层（Level-2）路由器必须配置相同的验证方式和验证密钥。
认证密钥选用 或 不受实际的网络环境影响。如果没有指定 或 参数，将检查 LSP ip osi ip osi中 的相应字段的配置内容。
OSI使用 验证模式时：
GCA不指定 参数时，为协议标准实现方式，可与友商互通；
• nonstandard指定 参数时，为私有实现方式，用于与 Comware早期采用非标准实现方式的
• nonstandard设备（无 nonstandard 参数）互通。
【举例】
\# 配置路由域采用简单明文验证模式，认证密钥为 123456。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] domain-authentication-mode simple plain 123456【相关命令】
•area-authentication-mode
•domain-authentication send-only
• isis authentication-mode

##### 1.1.32 fast-reroute

fast-reroute 命令用来配置 IS-IS 支持快速重路由功能。
undo fast-reroute 命令用来关闭 IS-IS 支持快速重路由功能。

【命令】
fast-reroute { lfa | route-policy route-policy-name } undo fast-reroute【缺省情况】
IS-IS 支持快速重路由功能处于关闭状态。
【视图】
IS-IS IPv4 单播地址族视图IS-IS IPv6 单播地址族视图【缺省用户角色】
network-admin【参数】
lfa：为所有路由通过 LFA（Loop Free Alternate）算法选取备份下一跳信息。
route-policy route-policy-name：指定路由策略名，route-policy-name 为 1～63 个字符的字符串，区分大小写。为通过策略的路由指定备份下一跳信息。
【使用指导】
等价路由不支持快速重路由功能。
IS-IS 支持快速重路由通过 LFA 算法选取备份下一跳功能与 IS-IS TE 特性互斥。
【举例】
使能 进程 支持快速重路由功能，并为所有路由通过 算法选取备份下一跳信息。
\# IS-IS 1 LFA <Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] address-family ipv4 [Sysname-isis-1-ipv4] fast-reroute lfa

##### 1.1.33 filter-policy export

filter-policy export 命令用来配置 IS-IS 对引入的路由信息进行过滤。
undo filter-policy export 命令用来取消 IS-IS 对引入的路由信息进行过滤。
【命令】
filter-policy { acl-number | prefix-list prefix-list-name | route-policy route-policy-name } export [ protocol [ process-id ] ] undo filter-policy export [ protocol [ process-id ] ]【缺省情况】
IS-IS 不对引入的路由信息进行过滤。
【视图】
IS-IS IPv4 单播地址族视图IS-IS IPv6 单播地址族视图

【缺省用户角色】
network-admin【参数】
acl-number：指定访问控制列表序号，取值范围为 2000～3999，基于 ACL 对引入的路由信息进行过滤。
prefix-list-name：指定地址前缀列表名，基于目的地址对引入的路由信息进prefix-list行过滤。prefix-list-name 为 1～63 个字符的字符串，区分大小写。
route-policy route-policy-name：指定路由策略名，基于路由策略对引入的路由信息进行过滤。route-policy-name 为 1～63 个字符的字符串，区分大小写。
protocol：路由协议名称，指定过滤从哪种路由协议引入的路由信息。如果不指定该参数，将对所有引入的路由进行过滤。
process-id：路由协议进程号，取值范围为 1～65535。只有当 为 isis、ospf、rip、protocol isisv6、ospfv3、ripng 时，该参数可选，若未指定，缺省进程号为 1。
【使用指导】
某些情况下，可能要求只发布某些满足条件的路由信息，此时，可以定义 配置所filter-policy发布路由信息的过滤条件，只有通过了过滤的路由信息才能被发布。
filter-policy export 命令一般和 import-route 命令结合使用，它只对已引入的路由在发布给其他路由器时进行过滤。
当配置的是高级 ACL（3000～3999）或者指定的路由策略中配置的是高级 ACL 时，其使用规则如下：
使用命令
• rule [ rule-id ] { deny | permit } ip source sour-addr来过滤指定目的地址的路由。
sour-wildcard使用命令
• rule [ rule-id ] { deny | permit } ip source sour-addr sour-wildcard destination dest-addr dest-wildcard 来过滤指定目的地址和掩码的路由。
其中，source 用来过滤路由目的地址，destination 用来过滤路由掩码，配置的掩码应该是连续的（当配置的掩码不连续时该过滤掩码的条件不生效）。
【举例】
使用编号为 的基本 对引入的路由进行过滤。
\# 2000 ACL <Sysname> system-view [Sysname] acl basic 2000 [Sysname-acl-ipv4-basic-2000] rule deny source 192.168.10.0 0.0.0.255 [Sysname-acl-ipv4-basic-2000] quit [Sysname] isis 1 [Sysname-isis-1] address-family ipv4 [Sysname-isis-1-ipv4] filter-policy 2000 export \# 使用编号为 3000 的高级 ACL 对引入的路由进行过滤，只允许 113.0.0.0/16 通过。
<Sysname> system-view [Sysname] acl advanced 3000 [Sysname-acl-ipv4-adv-3000] rule 10 permit ip source 113.0.0.0 0 destination 255.255.0.0 0 [Sysname-acl-ipv4-adv-3000] rule 100 deny ip

[Sysname-acl-ipv4-adv-3000] quit [Sysname] isis 1 [Sysname-isis 1] address-family ipv4 [Sysname-isis-1-ipv4] filter-policy 3000 export【相关命令】
•display isis route

##### 1.1.34 filter-policy import

命令用来配置 IS-IS 对接收的路由信息进行过滤。
filter-policy import命令用来恢复缺省情况。
undo filter-policy import【命令】
filter-policy { acl-number | prefix-list prefix-list-name | route-policy route-policy-name } import undo filter-policy import【缺省情况】
IS-IS 不对接收的路由信息进行过滤。
【视图】
IS-IS IPv4 单播地址族视图IS-IS IPv6 单播地址族视图【缺省用户角色】
network-admin【参数】
acl-number：指定访问控制列表序号，取值范围为 2000～3999，基于 对接收的路由是否加ACL入 IP 路由表进行过滤。
prefix-list prefix-list-name：指定地址前缀列表名，基于目的地址对接收的路由是否加入 IP 路由表进行过滤。prefix-list-name 为 1～63 个字符的字符串，区分大小写。
route-policy route-policy-name：指定路由策略名，基于路由策略对接收的路由是否加入IP 路由表进行过滤。 为 1～63 个字符的字符串，区分大小写。
route-policy-name【使用指导】
某些情况下，可能要求只接收某些满足条件的路由信息，此时，可以定义 配置接filter-policy收路由信息的过滤条件，只有通过了过滤的路由信息才能被加入路由表。
当配置的是高级 ACL（3000～3999）或者指定的路由策略中配置的是高级 ACL 时，其使用规则如下：
• 使用命令 rule [ rule-id ] { deny | permit } ip source sour-addr来过滤指定目的地址的路由。
sour-wildcard
• 使用命令rule [ rule-id ] { deny | permit } ip source sour-addr来过滤指定目的地址和掩sour-wildcard destination dest-addr dest-wildcard码的路由。

其中，source 用来过滤路由目的地址，destination 用来过滤路由掩码，配置的掩码应该是连续的（当配置的掩码不连续时该过滤掩码的条件不生效）。
【举例】
\# 使用编号为 2000 的基本 ACL 对接收的路由信息进行过滤。
<Sysname> system-view [Sysname] acl basic 2000 [Sysname-acl-ipv4-basic-2000] rule deny source 192.168.10.0 0.0.0.255 [Sysname-acl-ipv4-basic-2000] quit [Sysname] isis 1 [Sysname-isis-1] address-family ipv4 [Sysname-isis-1-ipv4] filter-policy 2000 import使用编号为 的高级 对接收的路由信息进行过滤，只允许 通过。
\# 3000 ACL 113.0.0.0/16 <Sysname> system-view [Sysname] acl advanced 3000 [Sysname-acl-ipv4-adv-3000] rule 10 permit ip source 113.0.0.0 0 destination 255.255.0.0 0 [Sysname-acl-ipv4-adv-3000] rule 100 deny ip [Sysname-acl-ipv4-adv-3000] quit [Sysname] isis 1 [Sysname-isis 1] address-family ipv4 [Sysname-isis-1-ipv4] filter-policy 3000 import【相关命令】
• display ip routing-table（三层技术-IP 路由命令参考/IP 路由基础）

##### 1.1.35 flash-flood

flash-flood 命令用来使能 LSP 快速扩散功能。
undo flash-flood 命令用来关闭 LSP 快速扩散功能。
【命令】
flash-flood [ flood-count flooding-count | max-timer-interval flooding-interval | [ level-1 | level-2 ] ] * undo flash-flood [ level-1 | level-2 ]【缺省情况】
快速扩散功能处于关闭状态。
LSP【视图】
IS-IS 视图【缺省用户角色】
network-admin【参数】
flooding-count：在 SPF 重新计算前快速扩散 LSP 的个数，取值范围为 1～15，flood-count缺省值为 5。

flooding-interval：在 LSP 快速扩散之前的等待时间，取值范围为max-timer-interval 10～50000，单位为毫秒，缺省值为 10。
level-1：使能在 级别的快速扩散功能。
level-1 level-2：使能在 级别的快速扩散功能。
level-2【使用指导】
如果不指定级别，将同时使能 level-1 和 level-2 级别的快速扩散功能。
【举例】
\# 使能 LSP 快速扩散功能，配置发送个数 10 个，发送延时 100 毫秒。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] flash-flood flood-count 10 max-timer-interval 100

##### 1.1.36 graceful-restart

graceful-restart 命令用来使能 IS-IS 协议的 GR 能力。
undo graceful-restart 命令用来关闭 IS-IS 协议的 GR 能力。
【命令】
graceful-restart undo graceful-restart【缺省情况】
IS-IS 协议的 GR 能力处于关闭状态。
【视图】
视图IS-IS【缺省用户角色】
network-admin【使用指导】
IS-IS GR 特性与 IS-IS NSR 特性互斥，即 graceful-restart 和 non-stop-routing 命令互斥，不能同时配置。
【举例】
使能 进程 的 能力。
\# IS-IS 1 GR <Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] graceful-restart【相关命令】
• graceful-restart suppress-sa

##### 1.1.37 graceful-restart suppress-sa

命令用来配置重启时抑制 SA（Suppress-Advertisement）
graceful-restart suppress-sa位置位。

命令用来恢复缺省情况。
undo graceful-restart suppress-sa【命令】
graceful-restart suppress-sa undo graceful-restart suppress-sa【缺省情况】
SA 位处于置位状态。
【视图】
IS-IS 视图【缺省用户角色】
network-admin【使用指导】
表示抑制邻接标志位，将其置位的主要目的是避免出现路由黑洞，例如在启动或者重启时没有SA保留本地转发表，此时如果 GR Helper 将报文送到设备来进行转发将会造成严重的丢包现象，在这种情况下 GR Restarter 发送的 Hello 报文中必须将 SA 位置 1，而 GR Helper 接收到这种 SA 位被置 1 的 Hello 报文后就不会将发送该 Hello 报文的 GR Restarter 放入 LSP 扩散出去。
【举例】
配置重启时对 位进行抑制。
\# SA <Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] graceful-restart suppress-sa【相关命令】
• graceful-restart

##### 1.1.38 graceful-restart t1

graceful-restart t1 命令用来配置 T1 定时器。
命令用来恢复缺省情况。
undo graceful-restart t1【命令】
graceful-restart t1 seconds count count undo graceful-restart t1【缺省情况】
T1 定时器的超时值为 3 秒，超时次数为 10 次。
【视图】
IS-IS 视图【缺省用户角色】
network-admin

【参数】
seconds：T1 定时器的超时值，取值范围为 3～10，单位为秒。
count：T1 定时器超时次数，取值范围为 1～20。
【使用指导】
T1 定时器用来控制发送带有 RR 标志位的 Restart TLV 的次数。重启路由器发送带有 RR 标志位的TLV，如果在超时时间内收到对端回复的带有 标志的 TLV，才能正常进入Restart RA Restart GR流程；否则 GR 流程失败。
配置 GR 定时器时请遵循以下规则，否则可能会导致 GR 失败：
定时器超时值×超时次数小于 定时器的超时值。
• T1 T2定时器超时值小于 定时器的超时值。
• T2 T3【举例】
\# 配置 IS-IS 进程 1 的 T1 定时器超时值为 5 秒，超时次数为 5。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] graceful-restart t1 5 count 5【相关命令】
• graceful-restart
• graceful-restart t2
• graceful-restart t3

##### 1.1.39 graceful-restart t2

graceful-restart t2 命令用来配置 T2 定时器。
undo graceful-restart t2 命令用来恢复缺省情况。
【命令】
graceful-restart t2 seconds undo graceful-restart t2【缺省情况】
T2 定时器的超时值为 60 秒。
【视图】
视图IS-IS【缺省用户角色】
network-admin【参数】
seconds： T2 定时器的超时值，取值范围为 30 ～ 65535 ，单位为秒。

【使用指导】
T2 定时器用来控制 LSDB 同步时间。每个 LSDB 都有一个 T2 定时器，对于 Level-1-2 路由器来说，就需要有两个 T2 定时器，一个为 Level-1 的 T2 定时器，另外一个为 Level-2 的 T2 定时器。如果和 的 定时器都超时后，LSDB 同步还没有完成，则 失败。
Level-1 Level-2 T2 GR配置 定时器时请遵循以下规则，否则可能会导致 失败：
GR GR定时器超时值×超时次数小于 定时器的超时值。
• T1 T2定时器超时值小于 定时器的超时值。
• T2 T3【举例】
配置 进程 的 定时器超时值为 秒。
\# IS-IS 1 T2 50 <Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] graceful-restart t2 50【相关命令】
• graceful-restart
• graceful-restart t1
• graceful-restart t3

##### 1.1.40 graceful-restart t3

命令用来配置 定时器。
graceful-restart t3 T3命令用来恢复缺省情况。
undo graceful-restart t3【命令】
graceful-restart t3 seconds undo graceful-restart t3【缺省情况】
T3 定时器的超时值为 300 秒。
【视图】
IS-IS 视图【缺省用户角色】
network-admin【参数】
seconds：T3 定时器的超时值，取值范围为 300～65535，单位为秒。
【使用指导】
T3 定时器用来控制路由器的重启时间间隔。重启时间间隔在 IS-IS 的 Hello PDU 中设置为保持时间，这样在该路由器重启的时间内邻居不会断掉与其的邻接关系。如果 T3 定时器超时后 GR 还没有完成，则 失败。
GR配置 定时器时请遵循以下规则，否则可能会导致 失败：
GR GR定时器超时值×超时次数小于 定时器的超时值。
• T1 T2

T2 定时器超时值小于 T3 定时器的超时值。
•【举例】
配置 进程 的 定时器超时值为 秒。
\# IS-IS 1 T3 500 <Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] graceful-restart t3 500【相关命令】
• graceful-restart
• graceful-restart t1
• graceful-restart t2

##### 1.1.41 ignore-att

命令用来配置 不采用 位计算缺省路由。
ignore-att IS-IS ATT命令用来恢复缺省情况。
undo ignore-att【命令】
ignore-att undo ignore-att【缺省情况】
IS-IS 采用 ATT 位计算缺省路由。
【视图】
IS-IS 视图【缺省用户角色】
network-admin【举例】
\# 配置不采用 ATT 位计算缺省路由。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] ignore-att

##### 1.1.42 import-route

命令用来从其它路由协议或其它 进程引入路由信息。
import-route IS-IS命令用来取消从其它路由协议或其它 进程引入路由信息。
undo import-route IS-IS【命令】
IS-IS IPv4 单播地址族视图：
import-route bgp [ as-number ] [ allow-ibgp ] [ cost cost-value | cost-type { external | internal } | [ level-1 | level-1-2 | level-2 ] | route-policy route-policy-name | tag tag ] *

import-route bgp [ as-number ] [ allow-ibgp ] inherit-cost [ [ level-1 | level-1-2 | level-2 ] | route-policy route-policy-name | tag tag ] * import-route { direct | static } [ cost cost-value | cost-type { external | internal } | [ level-1 | level-1-2 | level-2 ] | route-policy route-policy-name | tag tag ] * import-route { direct | static } inherit-cost [ [ level-1 | level-1-2 | level-2 ] | route-policy route-policy-name | tag tag ] * import-route { isis | ospf | rip } [ process-id | all-processes ] [ allow-direct | cost cost-value | cost-type { external | internal } | [ level-1 | level-1-2 | level-2 ] | route-policy route-policy-name | tag tag ] * import-route { isis | ospf | rip } [ process-id | all-processes ] inherit-cost [ allow-direct | [ level-1 | level-1-2 | level-2 ] | route-policy route-policy-name | tag tag ] * undo import-route { bgp | direct | { isis | ospf | rip } [ process-id | all-processes ] | static }单播地址族视图：
IS-IS IPv6 import-route bgp4+ [ as-number ] [ allow-ibgp ] [ [ cost cost-value | inherit-cost ] | cost-type { external | internal } | [ level-1 | level-1-2 | level-2 ] | route-policy route-policy-name | tag tag ] * import-route { direct | static } [ [ cost cost-value | inherit-cost ] | cost-type { external | internal } | [ level-1 | level-1-2 | level-2 ] | route-policy route-policy-name | tag tag ] * import-route { isisv6 | ospfv3 | ripng } [ process-id ] [ allow-direct | [ cost cost-value | inherit-cost ] | cost-type { external | internal } | [ level-1 | level-1-2 | level-2 ] | route-policy route-policy-name | tag tag ] * undo import-route { bgp4+ | direct | { isisv6 | ospfv3 | ripng } [ process-id | all-processes ] | static }【缺省情况】
不引入其它协议的路由信息。
IS-IS【视图】
IS-IS IPv4 单播地址族视图IS-IS IPv6 单播地址族视图【缺省用户角色】
network-admin【参数】
bgp：引入 BGP 协议的路由。
direct：引入直连路由。
isis：引入 IS-IS 协议的路由。
ospf：引入 OSPF 协议的路由。

rip：引入 RIP 协议的路由。
static：引入静态路由。
bgp4+：引入 IPv6 BGP 协议的路由。
isisv6：引入 IPv6 IS-IS 协议的路由。
ospfv3：引入 OSPFv3 协议的路由。
ripng：引入 RIPng 协议的路由。
as-number：引入指定 AS 内的路由。as-number 为 AS 号，取值范围为 1～4294967295。当是 或 bgp4+时，如果没有指定本参数，则引入所有的 IPv4 或 IPv6 EBGP 路由。
protocol bgp建议配置时指定 号，否则引入的 路由数量过多时，会引发设备内存资源紧张等问题。
AS EBGP process-id：路由协议进程号，取值范围为 1～65535，缺省值为 1。
all-processes：引入指定路由协议所有进程的路由。
allow-ibgp：允许引入 路由。
IBGP allow-direct：在引入的路由中包含使能了该协议的接口网段路由。缺省情况下，在引入协议路由 时 不 会 包 含 使 能 了 该 协 议 的 接 口 网 段 路 由 。 当 allow-direct 与 route-policy route-policy-name 参数一起使用时，需要注意路由策略中配置的匹配规则不要与接口路由信息存在冲突，否则会导致 配置失效。例如，当配置 参数引入 OSPF allow-direct allow-direct直连时，在路由策略中不要配置 匹配条件，否则，allow-direct 参数if-match route-type失效。
cost cost-value：引入的路由的路径开销值，取值范围为 0～4261412864。
• 当路径开销值类型为 narrow、narrow-compatible 或 compatible 时，取值范围为 0～63。
• 当路径开销值类型为 wide 或 wide-compatible 时，取值范围为 0～4261412864。
cost-type { external | internal }：表示路径开销类型：internal 表示内部路由；
表示外部路由，配置路径开销类型为 后，通过 LSP 发布路由时路径开销会external external在配置的 值的基础上加上 64，从而保证内部路由优于外部路由。缺省情况下为 类cost external型。只有当开销类型为 narrow、narrow-compatible 或者 compatible 时，该参数有效。
inherit-cost：指定引入外部路由时使用该路由的原有开销值。
level-1：引入路由到 Level-1 的路由表中。
：同时引入路由到 和 的路由表中。
level-1-2 Level-1 Level-2 level-2：引入路由到 的路由表中。如果不指定引入的级别，默认为引入路由到Level-2 Level-2路由表中。
route-policy route-policy-name：路由策略名称，只有满足指定路由策略匹配条件的路由才被引入。route-policy-name 为 1～63 个字符的字符串，区分大小写。
tag tag：为引入路由配置 Tag 值，取值范围为 1～4294967295。
【使用指导】
IS-IS 将所有引入路由域中的路由当作外部路由，它们描述了应该如何选择到路由域以外目的地的路由。
指定 或 参数后，真正生效的开销值受当前开销类型的影响。当路径开销值cost inherit-cost类型为 narrow、narrow-compatible 或 compatible 时，生效的开销值范围为 0～63，超过63 的也取值为 63 ；当路径开销值类型为 wide 或 wide-compatible 时，配置值即为生效值。

该命令不能引入缺省路由。只能引入路由表中状态为 active 的路由，是否为 active 状态可以通过命令来查看。
display ip routing-table protocol和 bgp4+表示只引入 路由；import-route import-route bgp import-route EBGP bgp allow-ibgp 和 import-route bgp4+ allow-ibgp 表示将 IBGP 路由也引入，容易引起路由环路，请慎用。
如果未指定 或 参数，则引入的外部路由的开销值为 0。
cost inherit-cost undo import-route { isis | ospf | rip } all-processes/undo import-route命令只能取消{ isisv6 | ospfv3 | ripng } all-processes import-route { isis | ospf | rip } all-processes/undo import-route { isisv6 | ospfv3 | ripng } all-processes 命 令 的 配 置 ， 不 能 取 消 import-route { isis | ospf | rip } process-id/import-route 命令的配置。
{ isisv6 | ospfv3 | ripng } process-id【举例】
引入静态路由，cost 值为 15。
\# <Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] address-family ipv4 [Sysname-isis-1-ipv4] import-route static cost 15【相关命令】
•import-route limit

##### 1.1.43 import-route isis level-1 into level-2

命令用来配置将 Level-1 区域的路由信息引入import-route isis level-1 into level-2到 区域。
Level-2命令用来禁止将 区域的路由信undo import-route isis level-1 into level-2 Level-1息引入到 Level-2 区域。
【命令】
import-route isis level-1 into level-2 [ filter-policy { ipv4-acl-number | prefix-list prefix-list-name | route-policy route-policy-name } | tag tag ]
* undo import-route isis level-1 into level-2【缺省情况】
Level-1 区域的路由信息向 Level-2 区域发布。
【视图】
IS-IS IPv4 单播地址族视图【缺省用户角色】
network-admin【参数】
filter-policy：过滤策略。

ipv4-acl-number：指定访问控制列表序号，取值范围为 2000～3999，过滤从 Level-1 区域引入到 区域的路由信息。
Level-2 prefix-list-name：指定 地址前缀列表名，基于目的地址对从 区prefix-list IPv4 Level-1域引入到 Level-2 区域的路由信息进行过滤。prefix-list-name 为 1～63 个字符的字符串，区分大小写。
route-policy-name：指定路由策略名，基于路由策略从 Level-1 区域引入到route-policy区域的路由信息进行过滤。route-policy-name 为 1～63 个字符的字符串，区分大小写。
Level-2 tag：为引入路由配置 Tag 值，取值范围为 1～4294967295。
tag【使用指导】
如果要通过路由策略对从 区域引入到 区域的路由信息进行过滤，必须在Level-1 Level-2 import-route isis level-1 into level-2 命令中同时指定要应用的路由策略，否则路由过滤将不会生效；其它路由策略，如在接收或引入路由时指定的路由策略对路由渗透无效。
如果指定了过滤策略，则只有通过过滤的路由才能够被发布到 Level-2 区域中。
【举例】
\# 配置路由器从 Level-1 向 Level-2 进行路由渗透。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] address-family ipv4 [Sysname-isis-1-ipv4] import-route isis level-1 into level-2【相关命令】
•import-route
• import-route isis level-1 into level-2

##### 1.1.44 import-route isis level-2 into level-1

import-route isis level-2 into level-1 命令用来配置将 Level-2 区域的路由信息引入到 Level-1 区域。
命令用来恢复缺省情况。
undo import-route isis level-2 into level-1【命令】
ipv4-acl-number import-route isis level-2 into level-1 [ filter-policy { | prefix-list prefix-list-name | route-policy route-policy-name } | tag tag ]
* undo import-route isis level-2 into level-1【缺省情况】
Level-2 区域的路由信息不向 Level-1 区域发布。
【视图】
单播地址族视图IS-IS IPv4【缺省用户角色】
network-admin

【参数】
filter-policy：过滤策略。
ipv4-acl-number：指定访问控制列表序号，取值范围为 2000～3999，过滤从 Level-2 区域引入到 Level-1 区域的路由信息。
prefix-list-name：指定 IPv4 地址前缀列表名，基于目的地址对从 Level-2 区prefix-list域引入到 区域的路由信息进行过滤。prefix-list-name 为 1～63 个字符的字符串，区Level-1分大小写。
route-policy route-policy-name：指定路由策略名，基于路由策略从 Level-2 区域引入到Level-1 区域的路由信息进行过滤。route-policy-name 为 1～63 个字符的字符串，区分大小写。
tag tag：为引入路由配置 Tag 值，取值范围为 1～4294967295。
【使用指导】
如果要通过路由策略对从 Level-2 区域引入到 Level-1 区域的路由信息进行过滤，必须在命令中同时指定要应用的路由策略，否则路由import-route isis level-2 into level-1过滤将不会生效；其它路由策略，如在接收或引入路由时指定的路由策略对路由渗透无效。
如果指定了过滤策略，则只有通过过滤的路由才能够被发布到 Level-1 区域中。
【举例】
\# 配置路由器从 Level-2 向 Level-1 进行路由渗透。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] address-family ipv4 [Sysname-isis-1-ipv4] import-route isis level-2 into level-1【相关命令】
• import-route
• import-route isis level-1 into level-2

##### 1.1.45 import-route isisv6 level-1 into level-2

命令用来配置从 向 进行路import-route isisv6 level-1 into level-2 Level-1 Level-2由渗透。
undo import-route isisv6 level-1 into level-2 命令用来禁止从 Level-1 向 Level-2进行路由渗透。
【命令】
ipv6-acl-number import-route isisv6 level-1 into level-2 [ filter-policy { | prefix-list prefix-list-name | route-policy route-policy-name } | tag tag ] * undo import-route isisv6 level-1 into level-2【缺省情况】
从 Level-1 向 Level-2 进行路由渗透。
【视图】
IS-IS IPv6 单播地址族视图

【缺省用户角色】
network-admin【参数】
filter-policy：过滤策略。
ipv6-acl-number：IPv6 ACL 的编号，取值范围 2000～3999。
prefix-list-name：IPv6 地址前缀列表名称，prefix-list-name 为 1～63 prefix-list个字符的字符串，区分大小写。
route-policy-name：路由策略名称，route-policy-name 为 1～63 个字route-policy符的字符串，区分大小写。
tag：为引入的路由分配管理标签号，取值范围 1～4294967295。
tag【使用指导】
Level-1-2 路由器可以将它所知道的其他区域的 Level-1 区域路由信息发布给本区域的 Level-2 和Level-1-2 路由器。
【举例】
\# 设定路由器从 Level-1 向 Level-2 进行路由渗透。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] address-family ipv6 [Sysname-isis-1-ipv6] import-route isisv6 level-1 into level-2

##### 1.1.46 import-route isisv6 level-2 into level-1

import-route isisv6 level-2 into level-1 命令用来配置从 Level-2 向 Level-1 进行路由渗透。
命令用来恢复缺省情况。
undo import-route isisv6 level-2 into level-1【命令】
ipv6-acl-number import-route isisv6 level-2 into level-1 [ filter-policy { | prefix-list prefix-list-name | route-policy route-policy-name } | tag tag ] * undo import-route isisv6 level-2 into level-1【缺省情况】
不从 Level-2 向 Level-1 进行路由渗透。
【视图】
IS-IS IPv6 单播地址族视图【缺省用户角色】
network-admin【参数】
filter-policy：过滤策略。
ipv6-acl-number：IPv6 的编号，取值范围 2000～3999。
ACL

prefix-list-name：IPv6 地址前缀列表名称，prefix-list-name 为 1～63 prefix-list个字符的字符串，区分大小写。
route-policy-name：路由策略名称，route-policy-name 为 1～63 个字route-policy符的字符串，区分大小写。
tag tag：为引入的路由分配管理标签号，取值范围 1～4294967295。
【使用指导】
Level-1-2 路由器可以将它所知道的其他区域的 Level-2 区域路由信息发布给本区域的 Level-1 和Level-1-2 路由器。
【举例】
设定路由器从 向 进行路由渗透。
\# Level-2 Level-1 <Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] address-family ipv6 [Sysname-isis-1-ipv6] import-route isisv6 level-2 into level-1

##### 1.1.47 import-route limit

命令用来配置引入 Level1/Level2 的路由最大条数。
import-route limit undo import-route limit 命令用来恢复缺省情况。
【命令】
import-route limit number undo import-route limit【缺省情况】
引入 的 路由最大条数为设备 路由表的容量值。
Level1/Level2 IPv4/IPv6 IPv4/IPv6【视图】
IS-IS IPv4 单播地址族视图IS-IS IPv6 单播地址族视图【缺省用户角色】
network-admin【参数】
number：引入 Level1/Level2 的路由最大条数。对于 IPv4 IS-IS，取值范围为 1～65536；对于 IPv6 IS-IS，取值范围为 1～32768。
【举例】
\# 配置 IS-IS 进程 1 引入 Level1/Level2 的 IPv4 路由最大条数为 1000。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] address-family ipv4 [Sysname-isis-1-ipv4] import-route limit 1000

【相关命令】
• import-route

##### 1.1.48 isis

isis 命令用来启动 IS-IS，并进入 IS-IS 视图。
undo isis 命令用来关闭 IS-IS。
【命令】
isis [ process-id ] [ vpn-instance vpn-instance-name ] undo isis [ process-id ]【缺省情况】
系统没有运行 IS-IS。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
process-id：IS-IS 进程号，取值范围为 1～65535，缺省值为 1。
vpn-instance vpn-instance-name：指定 IS-IS 所属的 VPN 实例。vpn-instance-name表示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则表示 位于公网中。
IS-IS【举例】
\# 创建 IS-IS 进程 1，配置网络实体名称，其中系统 ID 为 0000.0000.0002，区域 ID 为 01.0001。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] network-entity 01.0001.0000.0000.0002.00【相关命令】
• isis enable
• network-entity

##### 1.1.49 isis authentication send-only

isis authentication send-only 命令用来配置对收到的 Hello 报文忽略认证信息检查。
undo isis authentication send-only 命令用来取消对收到的 Hello 报文忽略认证信息检查的配置。
【命令】
isis authentication send-only [ level-1 | level-2 ] undo isis authentication send-only [ level-1 | level-2 ]

【缺省情况】
如果配置了接口验证方式和验证密钥，对收到的报文执行认证信息检查。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
level-1：对收到的 Level-1 Hello 报文忽略认证信息检查。
level-2：对收到的 报文忽略认证信息检查。
Level-2 Hello【使用指导】
配置邻居关系验证方式和验证密钥后，验证密钥将会按照设定的方式封装到 Hello 报文中，并对接收到的 Hello 报文进行验证密钥的检查，通过检查才会形成邻居关系。当需要更改密钥时由于密钥不匹配可能导致邻居关系中断。通过命令配置对收到的 报文忽略认证信息检查可保证邻居关Hello系不中断，报文正常接收。
【举例】
\# 为接口 Vlan-interface10 配置对收到 Level-1 Hello 报文忽略认证信息检查。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis authentication send-only level-1【相关命令】
• area-authentication send-only
• domain-authentication send-only
• isis authentication-mode

##### 1.1.50 isis authentication-mode

isis authentication-mode 命令用来配置邻居关系验证方式和验证密钥。
undo isis authentication-mode 命令用来取消邻居关系验证方式和验证密钥的配置。
【命令】
isis authentication-mode { { gca key-id { hmac-sha-1 | hmac-sha-224 | hmac-sha-256 | hmac-sha-384 | hmac-sha-512 } [ nonstandard ] | md5 | simple } { cipher | plain } string | keychain keychain-name } [ level-1 | level-2 ] [ ip | osi ] undo isis authentication-mode [ level-1 | level-2 ]【缺省情况】
接口没有配置邻居关系验证方式和验证密钥。
【视图】
接口视图

【缺省用户角色】
network-admin【参数】
gca：GCA 验证模式（Generic Cryptographic Authentication）。
key-id：唯一标识一个认证项（SA），取值范围为 1～65535。发送方将 Key ID 放入认证 TLV 中，接收方根据报文中提取的 选择 对报文进行认证。
Key ID SA hmac-sha-1：支持 HMAC-SHA-1 算法。
hmac-sha-224：支持 HMAC-SHA-224 算法。
hmac-sha-256：支持 HMAC-SHA-256 算法。
hmac-sha-384：支持 HMAC-SHA-384 算法。
hmac-sha-512：支持 HMAC-SHA-512 算法。
nonstandard：兼容非标准 GCA 验证模式。
md5：MD5 验证模式。
simple：简单验证模式。
cipher：以密文方式设置密钥。
plain：以明文方式设置密钥，该密钥将以密文形式存储。
string：密钥字符串，区分大小写。明文密钥为 1～16 个字符的字符串，密文密钥为 33～53 个字符的字符串。
keychain：使用 keychain 验证方式。
keychain-name：keychain 名，为 1～63 个字符的字符串，区分大小写。
level-1：为 Level-1 配置认证密钥。
level-2：为 Level-2 配置认证密钥。
ip：检查 SNP、LSP 中 IP 的相应字段的配置内容。
osi：检查 SNP、LSP 中 OSI 的相应字段的配置内容。
【使用指导】
配置邻居关系验证方式和验证密钥后，验证密钥将会按照设定的方式封装到 Hello 报文中，并对接收到的 Hello 报文进行验证密钥的检查，通过检查才会形成邻居关系，否则将不会形成邻居关系。
IS-IS 的 验证模式对应于 keychain 的 HMAC-MD5 认证算法，所以 keychain 内只有使用md5认证算法，才能使得 使用 验证模式正常工作。当 在接口使用HMAC-MD5 IS-IS keychain IS-IS keychain 验证模式时，报文的收、发过程如下：
• IS-IS 在发送 Hello 报文前，会先从 keychain 获取当前的有效发送 key，根据该 key 的认证算法和认证密钥进行报文验证；如果当前不存在有效发送 key，或者该 key 的认证算法不是HMAC-MD5，则 发送的 报文中不含认证 TLV。
IS-IS Hello IS-IS 在收到 Hello 报文后，会从 keychain 获取当前的有效接收 key，根据各个 key 的认证算
•法和认证密钥对报文进行校验，如果当前不存在有效接收 key，或者使用所有的有效接收 key对报文的校验都未成功，则报文校验不通过，该报文被丢弃。
指定 level-1 或 level-2 参数时：
• 必须先使用 isis enable 命令在接口上使能 IS-IS 功能才能进行参数 level-1 和 level-2的配置。

如果没有指定 或 参数，将同时为 和 的 Hello 报文配
• level-1 level-2 level-1 level-2置验证方式及验证密钥。
两台路由器要形成邻居关系必须配置相同的验证方式和验证密钥。
认证密钥选用 或 不受实际的网络环境影响。如果没有指定 或 参数，将检查ip osi ip osi Hello报文中 OSI 的相应字段的配置内容。
使用 GCA 验证模式时：
• 不指定 nonstandard 参数时，为协议标准实现方式，可与友商互通；
• 指定 nonstandard 参数时，为私有实现方式，用于与 Comware早期采用非标准实现方式的设备（无 nonstandard 参数）互通。
【举例】
\# 为 Vlan-interface10 接口配置邻居关系采用简单明文验证模式，验证密钥为 123456。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis authentication-mode simple plain 123456【相关命令】
• area-authentication-mode
• domain-authentication-mode
•isis authentication send-only

##### 1.1.51 isis bfd enable

命令用来使能 IS-IS 的 BFD 功能。
isis bfd enable命令用来关闭 IS-IS 的 BFD 功能。
undo isis bfd enable【命令】
isis bfd enable undo isis bfd enable【缺省情况】
的 功能处于关闭状态。
IS-IS BFD【视图】
接口视图【缺省用户角色】
network-admin【举例】
\# 使能接口 Vlan-interface11 的 IS-IS BFD 功能。
<Sysname> system-view [Sysname] interface vlan-interface 11 [Sysname-Vlan-interface11] isis enable [Sysname-Vlan-interface11] isis bfd enable

##### 1.1.52 isis circuit-level

isis circuit-level 命令用来配置接口的链路邻接关系类型。
undo isis circuit-level 命令用来恢复缺省情况。
【命令】
isis circuit-level [ level-1 | level-1-2 | level-2 ] undo isis circuit-level【缺省情况】
接口既可以建立 Level-1 的邻接关系，也可以建立 Level-2 的邻接关系。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
level-1：配置本接口链路邻接关系类型为 Level-1。
level-1-2：配置本接口链路邻接关系类型为 Level-1-2。
level-2：配置本接口链路邻接关系类型为 Level-2。
【使用指导】
如果路由器类型是 Level-1（Level-2），接口的链路类型只能为 Level-1（Level-2），因此仅当路由器类型是 时，才需要通过配置接口的链路邻接关系类型来限制接口上所能建立的邻接关Level-1-2系，让接口只发送和接收 Level-1（Level-2）类型的 Hello 报文。
【举例】
\# 接口 Vlan-interface10 和同一区域内的非骨干路由器相连，配置接口的链路邻接关系类型为Level-1，禁止发送和接收 Level-2 Hello 报文。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis enable [Sysname-Vlan-interface10] isis circuit-level level-1【相关命令】
• is-level

##### 1.1.53 isis circuit-type p2p

isis circuit-type p2p 命令用来配置接口的网络类型为 P2P。
undo isis circuit-type 命令用来恢复缺省情况。
【命令】
isis circuit-type p2p undo isis circuit-type

【缺省情况】
接口网络类型根据物理接口决定。（VLAN 接口网络类型为 Broadcast。）
【视图】
接口视图【缺省用户角色】
network-admin【使用指导】
仅当接口的网络类型为广播网且只有两台路由器接入该广播网时才需要进行该项配置且两台路由器都要进行此项配置。
接口网络类型不同，其工作机制也略微不同，如：当网络类型为广播网时，需要选举 DIS、通过泛洪 CSNP 报文来实现 LSDB 同步，当网络类型为 P2P 时不需要选举 DIS，LSDB 同步机制也不同。
当只有两台路由器接入到同一个广播网时，通过将接口网络类型配置为 P2P 可以使 IS-IS 按照 P2P而不是广播网的工作机制运行，避免 选举以及 的泛洪，既可以节省网络带宽，又可以加DIS CSNP快网络的收敛速度。
【举例】
\# 配置接口 Vlan-interface10 的网络类型为 P2P。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis enable [Sysname-Vlan-interface10] isis circuit-type p2p

##### 1.1.54 isis cost

命令用来配置 接口的链路开销值。
isis cost IS-IS命令用来取消 接口的链路开销值的配置。
undo isis cost IS-IS【命令】
isis cost cost-value [ level-1 | level-2 ] undo isis cost [ level-1 | level-2 ]【缺省情况】
未配置 IS-IS 接口的链路开销值。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
cost-value：链路开销值，取值范围为 1～16777215。
level-1：配置在计算 路由时使用的链路开销值。
Level-1 level-2：配置在计算 路由时使用的链路开销值。
Level-2

【使用指导】
如果没有指定 level-1 或者 level-2，将同时配置计算 Level-1 和 Level-2 路由时使用的链路开销值。
【举例】
配置接口 在计算 路由时使用的链路开销值为 5。
\# Vlan-interface10 Level-2 <Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis cost 5 level-2【相关命令】
• auto-cost enable
• bandwidth-reference

##### 1.1.55 isis dis-name

命令用来在 上配置局域网名称来代表这个广播网中的伪节点。
isis dis-name DIS命令用来恢复缺省情况。
undo isis dis-name【命令】
isis dis-name symbolic-name undo isis dis-name【缺省情况】
未配置本地局域网名称。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
symbolic-name：本地局域网的名称，为 1～64 个字符的字符串，不区分大小写。
【使用指导】
该命令只有在使能了动态主机名映射功能的路由器上配置才能有效，在点到点链路的接口上配置无效。
【举例】
\# 配置本地局域网的名称为“LOCALAREA”。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis dis-name LOCALAREA【相关命令】
• display isis name-table
• is-name

##### 1.1.56 isis dis-priority

isis dis-priority 命令用来配置接口在不同层次的 DIS 优先级。
undo isis dis-priority 命令用来取消接口在不同层次的 DIS 优先级的配置。
【命令】
isis dis-priority priority [ level-1 | level-2 ] undo isis dis-priority [ level-1 | level-2 ]【缺省情况】
接口 Level-1 和 Level-2 级别 DIS 优先级为 64。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
priority：配置接口 DIS 优先级，取值范围为 0～127。
level-1：配置 Level-1 级别 DIS 选举优先级。
level-2：配置 Level-2 级别 DIS 选举优先级。
【使用指导】
当网络类型为广播网时，IS-IS 需要选举 DIS，Level-1 和 Level-2 的 DIS 是分别选举的，用户可以为不同级别的 选举配置不同的优先级，DIS 优先级数值越高，被选中的可能性就越大；如果两DIS台路由器 DIS 优先级相同，则 SNPA（Subnetwork Point of Attachment，子网连接点）地址（广播网络中的 SNPA 地址是 MAC 地址）最大的路由器会被选中。而且，在 IS-IS 中并没有备份 DIS 的概念，优先级为 0 的路由器也可以参与选举 DIS。
如果不指定级别，将同时配置 Level-1 和 Level-2 级别 DIS 选举优先级。
【举例】
配置接口 的 优先级为 127。
\# Vlan-interface10 Level-2 DIS <Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis dis-priority 127 level-2

##### 1.1.57 isis enable

命令用来在指定接口上使能 IS-IS 功能，并配置与该接口关联的 IS-IS 进程。
isis enable命令用来在指定接口上关闭 IS-IS 功能。
undo isis enable【命令】
isis enable [ process-id ] undo isis enable【缺省情况】
接口上的 IS-IS 功能处于关闭状态，且没有任何 IS-IS 进程与其关联。

【视图】
接口视图【缺省用户角色】
network-admin【参数】
process-id：指定与该接口关联的 进程，process-id 为 进程号，取值范围为 1～IS-IS IS-IS 65535，缺省值为 1。
【举例】
\# 创建 IS-IS 路由进程 1，并在接口 Vlan-interface10 上使能 IS-IS 功能。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] network-entity 10.0001.1010.1020.1030.00 [Sysname-isis-1] quit [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis enable 1【相关命令】
•isis
• network-entity

##### 1.1.58 isis fast-reroute lfa-backup exclude

isis fast-reroute lfa-backup exclude 命令用来禁止接口参与 LFA 计算。
undo isis fast-reroute lfa-backup exclude 命令用来恢复缺省情况。
【命令】
isis fast-reroute lfa-backup exclude undo isis fast-reroute lfa-backup exclude【缺省情况】
接口参与 LFA 计算，能够被选为备份接口。
【视图】
接口视图【缺省用户角色】
network-admin【使用指导】
接口缺省参与 LFA 计算，有资格成为备份接口。配置本功能后，接口不会被选为备份接口。
【举例】
\# 禁止接口 Vlan-interface10 参与 LFA 计算。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] network-entity 10.0001.1010.1020.1030.00

[Sysname-isis-1] quit [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis enable 1 [Sysname-Vlan-interface10] isis fast-reroute lfa-backup exclude【相关命令】
•fast-reroute

##### 1.1.59 isis ipv6 bfd enable

命令用来在使能 IPv6 IS-IS 的 BFD 功能。
isis ipv6 bfd enable命令用来关闭 IPv6 IS-IS 的 BFD 功能。
undo isis ipv6 bfd enable【命令】
isis ipv6 bfd enable undo isis ipv6 bfd enable【缺省情况】
的 功能处于关闭状态。
IPv6 IS-IS BFD【视图】
接口视图【缺省用户角色】
network-admin【举例】
\# 使能接口 Vlan-interface11 的 IPv6 IS-IS BFD 功能。
<Sysname> system-view [Sysname] interface vlan-interface 11 [Sysname-Vlan-interface11] isis ipv6 bfd enable

##### 1.1.60 isis ipv6 cost

命令用来配置接口的 IPv6 链路开销值。
isis ipv6 cost undo isis ipv6 cost 命令用来取消接口的 IPv6 链路开销值的配置。
【命令】
isis ipv6 cost cost-value [ level-1 | level-2 ] undo isis ipv6 cost [ level-1 | level-2 ]【缺省情况】
未配置接口的 链路开销值。
IPv6【视图】
接口视图【缺省用户角色】
network-admin

【参数】
cost-value：链路开销值，取值范围为 1～16777215。
level-1：配置在计算 Level-1 路由时使用的链路开销值。
level-2：配置在计算 Level-2 路由时使用的链路开销值。
【使用指导】
接口必须使能 IPv6 IS-IS 功能。
只有 IS-IS 支持 IPv6 拓扑标准模式的情况下，接口中配置的 IPv6 链路开销值才会生效。
【举例】
\# 配置接口 Vlan-interface11 的 IPv6 链路开销值为 10。
<Sysname> system-view [Sysname] isis 100 [Sysname-isis-100] address-family ipv6 unicast [Sysname-isis-100-ipv6] quit [Sysname-isis-100] quit [Sysname] interface vlan-interface 11 [Sysname-Vlan-interface11] isis ipv6 enable 100 [Sysname-Vlan-interface11] isis ipv6 cost 10

##### 1.1.61 isis ipv6 enable

命令用来使能接口上 的 能力。
isis ipv6 enable IS-IS IPv6命令用来关闭指定接口上 的 能力。
undo isis ipv6 enable IS-IS IPv6【命令】
isis ipv6 enable [ process-id ] undo isis ipv6 enable【缺省情况】
接口上 IS-IS 的 IPv6 能力处于关闭状态。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
process-id：IS-IS 进程号，取值范围 1～65535，缺省值为 1。
【举例】
\# 配置 IPv6 IS-IS，并在接口 Vlan-interface100 上使能 IS-IS 的 IPv6 能力。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] network-entity 10.0001.1010.1020.1030.00 [Sysname-isis-1] address-family ipv6 unicast [Sysname-isis-1-ipv6] quit

[Sysname-isis-1] quit [Sysname] interface vlan-interface 100 [Sysname-Vlan-interface100] ipv6 address 2002::1/64 [Sysname-Vlan-interface100] isis ipv6 enable 1

##### 1.1.62 isis ipv6 fast-reroute lfa-backup exclude

isis ipv6 fast-reroute lfa-backup exclude 命令用来禁止接口参与 LFA 计算。
undo isis ipv6 fast-reroute lfa-backup exclude 命令用来恢复缺省情况。
【命令】
isis ipv6 fast-reroute lfa-backup exclude undo isis ipv6 fast-reroute lfa-backup exclude【缺省情况】
接口参与 LFA 计算。
【视图】
接口视图【缺省用户角色】
network-admin【举例】
\# 禁止接口 Vlan-interface10 参与 LFA 计算。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] network-entity 10.0001.1010.1020.1030.00 [Sysname-isis-1] quit [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis ipv6 enable 1 [Sysname-Vlan-interface10] isis ipv6 fast-reroute lfa-backup exclude【相关命令】
• fast-reroute

##### 1.1.63 isis ipv6 prefix-suppression

isis ipv6 prefix-suppression 命令用来配置接口的前缀抑制功能。
undo isis ipv6 prefix-suppression 命令用来关闭接口的前缀抑制功能。
【命令】
isis ipv6 prefix-suppression undo isis ipv6 prefix-suppression【缺省情况】
接口的前缀抑制功能处于关闭状态。

【视图】
接口视图【缺省用户角色】
network-admin【使用指导】
缺省情况下，接口上使能 后，会在 中发布此接口的前缀，可以通过在接口上配置此命令，IS-IS LSP减少此接口的前缀在 LSP 中携带，屏蔽内部节点被发布，提高安全性，加快路由收敛。
【举例】
\# 接口 Vlan-interface10 使能前缀抑制功能。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis ipv6 prefix-suppression

##### 1.1.64 isis ipv6 primary-path-detect bfd

isis ipv6 primary-path-detect bfd 命令用来使能 IPv6 IS-IS 协议中主用链路的 BFD 检测功能。
undo isis ipv6 primary-path-detect bfd 命令用来关闭 IPv6 IS-IS 协议中主用链路的BFD 检测功能。
【命令】
isis ipv6 primary-path-detect bfd { ctrl | echo } undo isis ipv6 primary-path-detect bfd【缺省情况】
IPv6 IS-IS 协议中主用链路的 BFD 检测功能处于关闭状态。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
ctrl：配置通过工作于控制报文方式的 会话对主用链路进行检测。
BFD echo：配置通过工作于 echo 报文方式的 BFD 会话对主用链路进行检测。
【使用指导】
配置本功能后，IPv6 IS-IS 协议的快速重路由特性和 PIC 特性中的主用链路将使用 BFD 进行检测。
【举例】
\# 在接口 Vlan-interface10 上配置 IPv6 IS-IS 协议快速重路由特性中主用链路使能 BFD （ Ctrl 方式）
检测功能。
<Sysname> system-view [Sysname] isis 1

[Sysname-isis-1] address-family ipv6 [Sysname-isis-1-ipv6] fast-reroute lfa [Sysname-isis-1-ipv6] quit [Sysname-isis-1] quit [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis ipv6 primary-path-detect bfd ctrl \# 在接口 Vlan-interface11 上配置 IPv6 IS-IS 协议 PIC 特性中主用链路使能 BFD（Echo 方式）检测功能。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] pic additional-path-always [Sysname-isis-1] quit [Sysname] bfd echo-source-ipv6 1::1 [Sysname] interface vlan-interface 11 [Sysname-Vlan-interface11] isis ipv6 primary-path-detect bfd echo

##### 1.1.65 isis ipv6 tag

命令用来配置接口的 Tag 值。
isis ipv6 tag命令用来恢复缺省情况。
undo isis ipv6 tag【命令】
isis ipv6 tag tag undo isis ipv6 tag【缺省情况】
未配置接口的 值。
Tag【视图】
接口视图【缺省用户角色】
network-admin【参数】
：管理标记值，取值范围为 1～4294967295。
tag【使用指导】
只要发布可达的 地址前缀具有 属性，IS-IS 都会将 加入到该前缀的 可达信息IPv6 Tag Tag IPv6 TLV中，与 cost-style 的类型无关。
【举例】
\# 配置接口 Vlan-interface10 的 Tag 值。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis ipv6 tag 4294967295

##### 1.1.66 isis mib-binding

isis mib-binding 命令用来配置 IS-IS 进程绑定 MIB。
undo isis mib-binding 命令用来恢复缺省情况。
【命令】
isis mib-binding process-id undo isis mib-binding【缺省情况】
MIB 绑定在进程号最小的 IS-IS 进程上。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
process-id：IS-IS 进程号，取值范围为 1～65535。
【使用指导】
如果指定的 不存在，配置 IS-IS 进程绑定命令时将会提示 IS-IS 进程不存在，无法完process-id成配置。
如果配置了 进程绑定 MIB，若删除 对应的 进程，则同时删除 进程IS-IS process-id IS-IS IS-IS绑定 MIB 配置，MIB 绑定到进程号最小的 IS-IS 进程上。
【举例】
\# 配置 IS-IS 进程 100 绑定 MIB。
<Sysname> system-view [Sysname] isis mib-binding 100

##### 1.1.67 isis prefix-suppression

命令用来配置接口的前缀抑制功能。
isis prefix-suppression命令用来关闭接口的前缀抑制功能。
undo isis prefix-suppression【命令】
isis prefix-suppression undo isis prefix-suppression【缺省情况】
接口的前缀抑制功能处于关闭状态。
【视图】
接口视图【缺省用户角色】
network-admin

【使用指导】
缺省情况下，接口使能 IS-IS 后，会在 LSP 中发布此接口的前缀，可以通过在接口上配置本命令，减少此接口的前缀在 LSP 中携带，屏蔽内部节点被发布，提高安全性，加快路由收敛。
本命令对接口从地址同样生效。
【举例】
接口 使能前缀抑制功能。
\# Vlan-interface10 <Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis prefix-suppression

##### 1.1.68 isis primary-path-detect bfd

命令用来使能 IS-IS 协议中主用链路的 BFD 检测功能。
isis primary-path-detect bfd命令用来关闭 IS-IS 协议中主用链路的 BFD 检测功能。
undo isis primary-path-detect bfd【命令】
isis primary-path-detect bfd { ctrl | echo } undo isis primary-path-detect bfd【缺省情况】
IS-IS 协议中主用链路的 BFD 检测功能处于关闭状态。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
ctrl：配置通过工作于控制报文方式的 BFD 会话对主用链路进行检测。
echo：配置通过工作于 echo 报文方式的 BFD 会话对主用链路进行检测。
【使用指导】
配置本功能后，IS-IS 协议的快速重路由特性和 特性中的主用链路将使用 进行检测。
PIC BFD【举例】
\# 在接口 Vlan-interface10 上配置 IS-IS 协议快速重路由特性中主用链路使能 BFD（Ctrl 方式）检测功能。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] address-family ipv4 [Sysname-isis-1-ipv4] fast-reroute lfa [Sysname-isis-1-ipv4] quit [Sysname-isis-1] quit [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis primary-path-detect bfd ctrl \# 在接口 Vlan-interface11 上配置 IS-IS 协议 PIC 特性中主用链路使能 BFD（Echo 方式）检测功能。

<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] pic additional-path-always [Sysname-isis-1] quit [Sysname] bfd echo-source-ip 1.1.1.1 [Sysname] interface vlan-interface 11 [Sysname-Vlan-interface11] isis primary-path-detect bfd echo

##### 1.1.69 isis silent

isis silent 命令用来禁止接口发送和接收 IS-IS 报文。
undo isis silent 命令用来恢复缺省情况。
【命令】
isis silent undo isis silent【缺省情况】
接口既发送也接收 IS-IS 报文。
【视图】
接口视图【缺省用户角色】
network-admin【使用指导】
Loopback 接口视图下不支持此命令。
【举例】
\# 禁止接口 Vlan-interface10 发送和接收 IS-IS 报文。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis silent

##### 1.1.70 isis small-hello

命令用来配置接口发送不加入填充 CLV 的小型 Hello 报文。
isis small-hello undo isis small-hello 命令用来恢复缺省情况。
【命令】
isis small-hello undo isis small-hello【缺省情况】
接口发送标准 报文。
Hello【视图】
接口视图

【缺省用户角色】
network-admin【使用指导】
Loopback 接口视图下不支持此命令。
【举例】
指定接口 发送小型 报文。
\# Vlan-interface10 Hello <Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis small-hello

##### 1.1.71 isis tag

命令用来配置接口的 Tag 值。
isis tag命令用来恢复缺省情况。
undo isis tag【命令】
isis tag tag undo isis tag【缺省情况】
未配置接口的 Tag 值。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
tag：管理标记值，取值范围为 1～4294967295。
【使用指导】
当 为 wide、wide-compatible 或 时，如果发布可达的 地址前缀具有 属cost-style compatible IP Tag性，IS-IS 会将 Tag 加入到该前缀的 IP 可达信息 TLV 中。
【举例】
\# 配置接口 Vlan-interface10 的 Tag 值。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis tag 4294967295

##### 1.1.72 isis timer csnp

isis timer csnp 命令用来配置 DIS 在广播网络上发送 CSNP 报文的时间间隔。
undo isis timer csnp 命令用来取消 DIS 在广播网络上发送 CSNP 报文的时间间隔的配置。

【命令】
isis timer csnp seconds [ level-1 | level-2 ] undo isis timer csnp [ level-1 | level-2 ]【缺省情况】
DIS 在广播网络上发送 CSNP 报文的时间间隔为 10 秒。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
seconds：DIS 在广播网络上发送 CSNP 报文的时间间隔，取值范围为 1～600，单位为秒。
level-1：配置 DIS 在 Level-1 发送 CSNP 报文的时间间隔。
level-2：配置 DIS 在 Level-2 发送 CSNP 报文的时间间隔。
【使用指导】
当网络类型为广播网时，DIS 使用 CSNP 报文来进行 LSDB 同步，因此只有在被选举为 DIS 的路由器上进行该项配置才有效。
如果不指定级别，将同时配置 DIS 在 Level-1 和 Level-2 发送 CSNP 报文的时间间隔。
【举例】
配置 的 报文在 接口上的发送时间间隔为 秒。
\# Level-2 CSNP Vlan-interface10 15 <Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis timer csnp 15 level-2

##### 1.1.73 isis timer hello

命令用来配置 Hello 报文的发送时间间隔。
isis timer hello命令用来取消 Hello 报文的发送时间间隔的配置。
undo isis timer hello【命令】
isis timer hello seconds [ level-1 | level-2 ] undo isis timer hello [ level-1 | level-2 ]【缺省情况】
Hello 报文的发送时间间隔为 10 秒。
【视图】
接口视图【缺省用户角色】
network-admin

【参数】
seconds：配置 Hello 报文的发送时间间隔，取值范围为 3～255，单位为秒。
level-1：配置 Level-1 Hello 报文的发送时间间隔。
level-2：配置 Level-2 Hello 报文的发送时间间隔。
【使用指导】
如果路由器在邻居关系保持时间内（即 Hello 报文失效数目与 Hello 报文发送时间间隔的乘积）没有收到来自邻居路由器的 Hello 报文时将宣告邻居关系失效。通过设置 Hello 报文失效数目和 Hello报文的发送时间间隔，可以调整邻居关系保持时间，即邻居路由器要花多长时间能够监测到链路已经失效并重新进行路由计算。
在广播链路上，Level-1 和 Level-2 Hello 报文会分别发送，其时间间隔也要分别配置；在点到点链路中，Level-1 和 Level-2 的 Hello 报文是在同一个点到点 Hello 报文中发送，不需要分别配置发送时间间隔。
参数 和 仅在广播接口上是可配置的，而且必须先在接口上使能 功能。
level-1 level-2 IS-IS发送时间间隔越短，网络收敛更快，但也需要占用更多的系统资源；因此，需要根据实际情况指定。
如果不指定级别，将同时配置 Level-1 和 Level-2 的 Hello 报文发送时间间隔。
【举例】
配置 的 报文在 接口上的发送时间间隔为 秒。
\# Level-2 Hello Vlan-interface10 20 <Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis timer hello 20 level-2【相关命令】
• isis timer holding-multiplier

##### 1.1.74 isis timer holding-multiplier

isis timer holding-multiplier 命令用来配置 Hello 报文失效数目。
命令用来取消 报文失效数目的配置。
undo isis timer holding-multiplier Hello【命令】
isis timer holding-multiplier value [ level-1 | level-2 ] undo isis timer holding-multiplier [ level-1 | level-2 ]【缺省情况】
Hello 报文失效数目为 3。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
value：IS-IS 邻居的 Hello 报文失效数目，取值范围为 3～1000。

level-1：Level-1 的 IS-IS 邻居 Hello 报文失效数目。
level-2：Level-2 的 IS-IS 邻居 Hello 报文失效数目。
【使用指导】
报文失效数目，即宣告邻居失效前 没有收到的邻居 报文的数目。
Hello IS-IS Hello如果路由器在邻居关系保持时间内（即 报文失效数目与 报文发送时间间隔的乘积）没Hello Hello有收到来自邻居路由器的 Hello 报文时将宣告邻居关系失效。通过设置 Hello 报文失效数目和 Hello报文的发送时间间隔，可以调整邻居关系保持时间，即邻居路由器要花多长时间能够监测到链路已经失效并重新进行路由计算。
在广播链路上，Level-1 和 Level-2 Hello 报文会分别发送，Hello 报文失效数目需要分别设置；在点到点链路中，Level-1 和 的 报文是在同一个点到点 报文中发送，因此不需要指Level-2 Hello Hello定 Level-1 或 Level-2。
参数 level-1 和 level-2 仅在广播接口上是可配置的，而且必须先在接口上使能 IS-IS 功能。
如果不指定级别，将同时配置 Level-1 和 Level-2 的 Hello 报文失效数目。
Hello 报文失效数目与 Hello 报文发送时间间隔的乘积不能超过 65535。
【举例】
\# 指定接口 Vlan-interface10 上标志邻居失效的 Level-2 Hello 报文数目为 6。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis timer holding-multiplier 6【相关命令】
• isis timer hello

##### 1.1.75 isis timer lsp

isis timer lsp 命令用来配置 IS-IS 在接口上发送 LSP 的最小时间间隔以及一次最多可以发送的 LSP 报文数目。
命令用来恢复缺省情况。
undo isis timer lsp【命令】
isis timer lsp time [ count count ] undo isis timer lsp【缺省情况】
发送 LSP 的最小时间间隔为 33 毫秒，一次最多可以发送 5 个 LSP 报文。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
time：发送链路状态报文的最小时间间隔，取值范围为 1～1000，单位为毫秒。

count：一次最多发送的链路状态报文的数目，取值范围为 1～1000。
【使用指导】
当 的内容发生变化时，IS-IS 将把发生变化的 扩散出去，用户可以对 的最小发送时LSDB LSP LSP间间隔进行调节。
请合理配置 LSP 发送时间间隔，当存在大量 IS-IS 接口或大量路由时，会发送大量的 LSP 报文，导致 LSP 风暴的出现。
【举例】
\# 配置在 Vlan-interface10 接口 LSP 的发送时间间隔为 500 毫秒。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis timer lsp 500【相关命令】
• isis timer retransmit

##### 1.1.76 isis timer retransmit

命令用来配置 在点到点链路上的重传时间间隔。
isis timer retransmit LSP命令用来恢复缺省情况。
undo isis timer retransmit【命令】
isis timer retransmit seconds undo isis timer retransmit【缺省情况】
LSP 在点到点链路上的重传时间间隔为 5 秒。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
seconds：表示 报文的重传时间间隔，取值范围 1～300，单位为秒。
LSP【使用指导】
在点到点链路上，发送的 LSP 需要得到对端的应答，否则将在重传时间间隔内重新发送该 LSP；
在广播链路上，DIS 周期性广播 CSNP 来实现 LSDB 的同步，不需要进行此项配置。
【举例】
\# 在接口 Vlan-interface10 上配置 LSP 在点到点链路上的重传时间间隔为 50 秒。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] isis circuit-type p2p [Sysname-Vlan-interface10] isis timer retransmit 50

【相关命令】
• isis circuit-type p2p
• isis timer lsp

##### 1.1.77 is-level

is-level 命令用来配置路由器的 Level 级别。
undo is-level 命令用来恢复缺省情况。
【命令】
is-level { level-1 | level-1-2 | level-2 } undo is-level【缺省情况】
路由器的 Level 级别为 Level-1-2。
【视图】
视图IS-IS【缺省用户角色】
network-admin【参数】
level-1：配置路由器工作在 Level-1，它只计算区域内路由，维护 L1 的 LSDB。
level-1-2：配置路由器工作在 Level-1-2，同时参与 L1 和 L2 的路由计算，维护 L1 和 L2 两个LSDB。
level-2：配置路由器工作在 Level-2，只参加 L2 的 LSP 交换和 L2 的路由计算，维护 L2 的 LSDB。
【使用指导】
如果只有一个区域，建议用户将所有路由器的 Level 配置为 Level-1 或者 Level-2，因为没有必要让所有路由器同时维护两个完全相同的数据库。
在 网络中使用时，建议将所有的路由器都配置为 Level-2，这样有利于以后的扩展。
IP【举例】
\# 配置路由器的 Level 级别为 Level-1。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] is-level level-1

##### 1.1.78 is-name

命令用来使能动态主机名映射功能并为当前路由器配置主机名称。
is-name命令用来关闭动态主机名映射功能。
undo is-name【命令】
is-name sys-name undo is-name

【缺省情况】
动态主机名映射功能处于关闭状态，且没有为当前路由器配置主机名称。
【视图】
IS-IS 视图【缺省用户角色】
network-admin【参数】
sys-name：为本地 IS 配置的主机名称，为 1～64 个字符的字符串，不区分大小写。
【使用指导】
只有使能动态主机名映射功能后，使用 display isis lsdb 等命令才可以看到路由器的主机名而不是 System ID。
【举例】
为本地 配置主机名称。
\# IS <Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] is-name RUTA【相关命令】
• display isis name-table

##### 1.1.79 is-name map

命令用来为远端 配置 与主机名称的映射关系。
is-name map IS System ID命令用来取消为远端 配置的 与主机名称的映射关系。
undo is-name map IS System ID【命令】
is-name map sys-id map-sys-name undo is-name map sys-id【缺省情况】
没有为远端 IS 配置 System ID 与主机名称的映射关系。
【视图】
IS-IS 视图【缺省用户角色】
network-admin【参数】
sys-id：远端 的系统 或伪系统 。
IS ID ID map-sys-name：为远端 配置的主机名称，为 1～64 个字符的字符串，不区分大小写。
IS【使用指导】
每个 System ID 只能对应一个主机名称。

【举例】
\# 为远端 IS 配置静态主机名映射，远端 IS 的 System ID 为“0000.0000.0041”，为其配置的主机名称为“RUTB”。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] is-name map 0000.0000.0041 RUTB【相关命令】
• display isis name-table

##### 1.1.80 ispf enable

命令用来开启 ISPF 功能，即增量 SPF 计算功能。
ispf enable命令用来关闭 ISPF 功能。
undo ispf enable【命令】
ispf enable undo ispf enable【缺省情况】
IS-IS ISPF 功能处于使能状态。
【视图】
IS-IS 视图IS-IS IPv6 单播地址族视图【缺省用户角色】
network-admin【使用指导】
开启增量 SPF 计算功能后，当网络的拓扑结构发生变化影响到最短路径树的结构时，只将受影响的部分节点进行修正，而不重建整棵最短路径树。
【举例】
\# 开启增量 SPF 计算功能。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] ispf enable

##### 1.1.81 log-peer-change

log-peer-change 命令用来打开邻接状态变化的输出开关。
undo log-peer-change 命令用来关闭邻接状态变化的输出开关。
【命令】
log-peer-change undo log-peer-change

【缺省情况】
邻接状态变化的输出开关处于打开状态。
【视图】
IS-IS 视图【缺省用户角色】
network-admin【使用指导】
打开邻接状态输出开关后，IS-IS 邻接状态变化时会生成日志信息发送到设备的信息中心，通过设置信息中心的参数，最终决定日志信息的输出规则（即是否允许输出以及输出方向）。（有关信息中心参数的配置请参见“网络管理和监控配置指导”中的“信息中心”。）
【举例】
关闭 邻接状态变化的输出开关。
\# IS-IS <Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] undo log-peer-change

##### 1.1.82 lsp-fragments-extend

命令用来在指定 Level 上使能 IS-IS 进程的 LSP 分片扩展功能。
lsp-fragments–extend命令用来恢复缺省情况。
undo lsp-fragments–extend【命令】
lsp-fragments-extend [ level-1 | level-1-2 | level-2 ] undo lsp-fragments-extend【缺省情况】
LSP 分片扩展功能处于关闭状态。
【视图】
IS-IS 视图【缺省用户角色】
network-admin【参数】
level-1：只对 Level-1 LSP 进行分片扩展。
level-1-2：对 Level-1 LSP 和 Level-2 LSP 都进行分片扩展。
level-2：只对 Level-2 LSP 进行分片扩展。
【使用指导】
如果配置时没有指定 level-1、level-2 或 参数，IS-IS 进程运行 分片扩展功level-1-2 LSP能时，将同时对 Level-1 LSP 和 Level-2 LSP 都进行分片扩展。

【举例】
\# 使能 Level-2 的 LSP 分片扩展功能。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] lsp-fragments-extend level-2

##### 1.1.83 lsp-length originate

lsp-length originate 命令用来配置当前路由器生成的 Level-1 LSP 和 Level-2 LSP 的最大长度。
undo lsp-length originate 命令用来取消当前路由器生成的 Level-1 LSP 和 Level-2 LSP 的最大长度的配置。
【命令】
lsp-length originate size [ level-1 | level-2 ] undo lsp-length originate [ level-1 | level-2 ]【缺省情况】
生成的 Level-1 LSP 和 Level-2 LSP 的最大长度均为 1497 个字节。
【视图】
IS-IS 视图【缺省用户角色】
network-admin【参数】
size：LSP 的最大长度，取值范围为 512～16384，单位为字节。
level-1：配置 长度。
Level-1 LSP level-2：配置 Level-2 LSP 长度。
【使用指导】
如果命令中没有指定 或 Level-2，则默认为对当前 系统进行配置。
Level-1 IS-IS【举例】
\# 配置生成的 Level-2 LSP 最大长度为 1024 字节。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] lsp-length originate 1024 level-2

##### 1.1.84 lsp-length receive

lsp-length receive 命令用来配置当前路由器可以接收的 LSP 的最大长度。
undo lsp-length receive 命令用来恢复缺省情况。
【命令】
lsp-length receive size undo lsp-length receive

【缺省情况】
可以接收的 LSP 的最大长度为 1497 个字节。
【视图】
IS-IS 视图【缺省用户角色】
network-admin【参数】
size：LSP 的最大长度，取值范围为 512～16384，单位为字节。
【举例】
\# 配置接收 LSP 报文最大长度为 1024 字节。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] lsp-length receive 1024

##### 1.1.85 maximum load-balancing

maximum load-balancing 命令用来配置 IS-IS 支持的等价路由的最大条数。
undo maximum load-balancing 命令用来恢复缺省情况。
【命令】
maximum load-balancing number undo maximum load-balancing【缺省情况】
IS-IS 支持的等价路由的最大条数与系统支持最大等价路由的条数相同。
【视图】
IS-IS IPv4 单播地址族视图IS-IS IPv6 单播地址族视图【缺省用户角色】
network-admin【参数】
number：等价路由的最大条数，当 number 取值为 1 时，相当于不进行负载分担。
【使用指导】
如果通过 max-ecmp-num 命令配置系统支持最大等价路由的条数为 m，则本命令的缺省值为 m，取值范围为 1～m。
【举例】
配置 支持的等价路由的最大条数为 2。
\# IS-IS <Sysname> system-view [Sysname] isis 100 [Sysname-isis-100] address-family ipv4

[Sysname-isis-100-ipv4] maximum load-balancing 2【相关命令】
max-ecmp-num（三层技术-IP 路由命令参考/IP 路由基础）
•

##### 1.1.86 multi-topology

命令用来配置 IS-IS 支持 IPv6 拓扑。
multi-topology命令用来取消 IS-IS 支持 IPv6 拓扑。
undo multiple-topology【命令】
multi-topology [ compatible ] undo multi-topology【缺省情况】
不支持 拓扑。
IS-IS IPv6【视图】
IS-IS IPv6 地址族视图【缺省用户角色】
network-admin【参数】
compatible：支持 IPv6 拓扑兼容模式，发布 IPv6 前缀时，会向 IPv4 拓扑和 IPv6 拓扑中分别发布一份。如果未指定本参数，表示不支持 拓扑兼容模式，发布 前缀时，只会向 拓扑IPv6 IPv6 IPv6中发布一份。
【使用指导】
配置此命令之后，IS-IS 的 IPv4 和 IPv6 将分拓扑进行计算。
本命令必须在链路开销值类型为 wide、compatible 或 wide-compatible 时才能配置。
【举例】
\# 配置 IS-IS 支持 IPv6 拓扑。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] address-family ipv6 [Sysname-isis-1-ipv6] multi-topology【相关命令】
• cost-style

##### 1.1.87 network-entity

network-entity 命令用来配置 IS-IS 进程的网络实体名称（Network Entity Title，简称 NET）。
undo network-entity 命令用来删除网络实体名称。
【命令】
network-entity net

undo network-entity net【缺省情况】
未配置 NET。
【视图】
IS-IS 视图【缺省用户角色】
network-admin【参数】
net：格式为 X…X.XXXX....XXXX.00，为十六进制数。前面的“X…X”是区域地址，中间的 12个“X”是路由器的 ID，最后的“00”是 SEL。
System【使用指导】
NET 可以看作是一类特殊的 NSAP，即 SEL 为 0 的 NSAP 地址，长度为 8～20 个字节。
NET 由三部分组成：
• 区域 ID：它的长度可变的，为 1～13 个字节。
• System ID：用来在区域内唯一标识主机或路由器，它的长度固定为 6 个字节。
SEL：为 0，它的长度固定为 个字节。
• 1例如 为：ab.cdef.1234.5678.9abc.00，则其中区域 为 ab.cdef，System 为 1234.5678.9abc，NET ID ID SEL 为 00。
批 量 执 行 cost-style 、 is-level 和 network-entity 命 令 时 ， 建 议 最 后 执 行network-entity 命令，否则可能会导致配置丢失。
【举例】
\# 指定 NET 为 10.0001.1010.1020.1030.00。其中区域 ID是 10.0001，System ID是 1010.1020.1030。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] network-entity 10.0001.1010.1020.1030.00【相关命令】
• cost-style
• isis
• isis enable
• is-level

##### 1.1.88 non-stop-routing

命令用来使能 IS-IS 协议的 NSR 功能。
non-stop-routing命令用来关闭 IS-IS 协议的 NSR 功能。
undo non-stop-routing【命令】
non-stop-routing undo non-stop-routing

【缺省情况】
IS-IS 协议的 NSR 功能处于关闭状态。
【视图】
IS-IS 视图【缺省用户角色】
network-admin【使用指导】
各个进程的 NSR 功能是相互独立的，只对本进程生效。如果存在多个 IS-IS 进程，建议在各个进程下使能 IS-IS NSR 功能。
IS-IS NSR 特性与 IS-IS GR 特性互斥，即 non-stop-routing 和 graceful-restart 命令互斥，不能同时配置。
【举例】
\#在 进程 中使能 功能。
IS-IS 1 NSR <Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] non-stop-routing

##### 1.1.89 pic

命令用来使能前缀无关收敛功能。
pic命令用来关闭前缀无关收敛功能。
undo pic【命令】
pic [ additional-path-always ] undo pic【缺省情况】
前缀无关收敛功能处于使能状态。
【视图】
IS-IS 视图【缺省用户角色】
network-admin【参数】
additional-path-always：支持非直连的次优路由作为备份。
【使用指导】
PIC（Prefix Convergence，前缀无关收敛），即收敛时间与前缀数量无关，加快收敛Independent速度。传统的路由计算快速收敛都与前缀数量相关，收敛时间与前缀数量成正比。 IS-IS 只实现非直连路由的前缀无关收敛。
IS-IS 快速重路由功能和 PIC 同时配置时，IS-IS 快速重路由功能生效。

【举例】
\# 使能 IS-IS 协议的 PIC 支持非直连次优路由做备份功能。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] pic additional-path-always

##### 1.1.90 preference

preference 命令用来配置 IS-IS 协议的路由优先级。
undo preference 命令用来恢复缺省情况。
【命令】
preference { preference | route-policy route-policy-name } * undo preference【缺省情况】
IS-IS 协议的路由优先级为 15。
【视图】
单播地址族视图IS-IS IPv4单播地址族视图IS-IS IPv6【缺省用户角色】
network-admin【参数】
preference：IS-IS 协议的路由优先级，取值范围为 1～255。
route-policy route-policy-name：指定路由策略，对通过该路由策略过滤的路由指定优先级。route-policy-name 为 1～63 个字符的字符串，区分大小写。
【使用指导】
由于在一台路由器上可能同时运行多种动态路由协议，就存在各个路由协议之间路由信息共享和选择的问题。系统为每一种路由协议配置一个优先级，当不同协议都发现了到同一目的地的路由时，优先级高的协议将起决定作用。
配置了 route-policy 参数后，如果 route-policy 中对某些匹配的路由优先级进行了修改，则这些匹配的路由取 修改的优先级，其它路由的优先级均取 命令所route-policy preference设的值。
【举例】
配置 协议的路由优先级为 25。
\# IS-IS <Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] address-family ipv4 [Sysname-isis-1-ipv4] preference 25

##### 1.1.91 prefix-priority

prefix-priority 命令用来配置 IS-IS 路由收敛的优先级。
undo prefix-priority 命令用来取消 IS-IS 路由收敛的优先级的配置。
【命令】
prefix-priority { critical | high | medium } { prefix-list prefix-list-name | tag tag-value } prefix-priority route-policy route-policy-name undo prefix-priority { critical | high | medium } [ prefix-list | tag ] undo prefix-priority route-policy【缺省情况】
路由收敛的优先级为低优先级。
IS-IS【视图】
IS-IS IPv4 单播地址族视图IS-IS IPv6 单播地址族视图【缺省用户角色】
network-admin【参数】
critical：最高优先级。
high：高优先级。
medium：中优先级。
prefix-list prefix-list-name：指定地址前缀列表名，唯一标识一个地址前缀列表。
为 1～63 个字符的字符串，区分大小写。
prefix-list-name tag-value：指定要求的标记值，取值范围为 1～4294967295。
tag： 指 定 路 由 策 略 名 ， 配 置 路 由 收 敛 的 优 先 级 。
route-policy route-policy-name为 1～63 个字符的字符串，区分大小写。
route-policy-name【使用指导】
IS-IS 路由的优先级越高收敛的速度越快。
IS-IS 主机路由的优先级为中优先级。
【举例】
\# 配置前缀列表 standtest 的 IS-IS 路由收敛的优先级为高优先级。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] address-family ipv4 [Sysname-isis-1-ipv4] prefix-priority high prefix-list standtest

##### 1.1.92 reset isis all

命令用来清除 进程所有的数据结构信息。
reset isis all IS-IS

【命令】
reset isis all [ process-id ] [ graceful-restart ]【视图】
用户视图【缺省用户角色】
network-admin【参数】
process-id：IS-IS 进程号，取值范围为 1～65535，清除该 IS-IS 进程所有的数据结构信息。
graceful-restart：清除 数据之后，通过 方式来恢复。
IS-IS GR【使用指导】
如果未指定 IS-IS 进程号，将清除所有 IS-IS 进程的数据结构信息。
本命令用在某些需要立即刷新 LSP 的情况下。
【举例】
\# 清除所有 IS-IS 进程的数据结构信息。
<Sysname> reset isis all

##### 1.1.93 reset isis event-log graceful-restart

命令用来清除 的日志信息。
reset isis event-log graceful-restart IS-IS GR【命令】
reset isis event-log graceful-restart slot slot-number【视图】
用户视图【缺省用户角色】
network-admin【参数】
：清除指定成员设备的 日志信息， 表示设备在slot slot-number IS-IS GR slot-number IRF中的成员编号。
【举例】
\# 清除 GR 的日志信息。
<Sysname> reset isis event-log graceful-restart \# 清除指定 slot 上 GR 的日志信息。
<Sysname> reset isis event-log graceful-restart slot 1

##### 1.1.94 reset isis event-log lsp

命令用来清除 IS-IS LSP 日志信息。
reset isis event-log lsp

【命令】
reset isis event-log lsp [ process-id ]【视图】
用户视图【缺省用户角色】
network-admin【参数】
process-id：IS-IS 进程号，取值范围为 1～65535，清除指定进程的 LSP 日志信息。如果不指定该参数，则表示清除所有进程的 LSP 日志信息。
【举例】
\# 清除 IS-IS 进程 1 的 LSP 日志信息。
<Sysname> reset isis event-log lsp 1【相关命令】
• display isis event-log lsp

##### 1.1.95 reset isis event-log non-stop-routing

reset isis event-log non-stop-routing 命令用来清除 IS-IS NSR 的日志信息。
【命令】
reset isis event-log non-stop-routing slot slot-number【视图】
用户视图【缺省用户角色】
network-admin【参数】
slot slot-number：清除指定成员设备的 IS-IS NSR 日志信息，slot-number 表示设备在 IRF中的成员编号。
【举例】
清除指定 上 的日志信息。
\# slot NSR <Sysname> reset isis event-log non-stop-routing slot 1

##### 1.1.96 reset isis event-log spf

reset isis event-log spf 命令用来清除 IS-IS 路由计算日志信息。
【命令】
reset isis event-log spf [ process-id ]【视图】
用户视图

【缺省用户角色】
network-admin【参数】
process-id：IS-IS 进程号，取值范围为 1～65535，清除指定进程的路由计算日志信息。如果不指定该参数，则清除所有进程的路由计算日志信息。
【举例】
\# 清除进程号为 1 的 IS-IS 进程的路由计算日志信息。
<Sysname> reset isis event-log spf 1【相关命令】
• display isis event-log spf

##### 1.1.97 reset isis packet

命令用来清除 报文的统计信息。
reset isis packet IS-IS【命令】
reset isis packet [ csnp | hello | lsp | psnp ] [ interface-type interface-number ] [ process-id ]【视图】
用户视图【缺省用户角色】
network-admin【参数】
csnp：清除 CSNP 报文的统计信息。
hello：清除 hello 报文的统计信息。
lsp：清除 报文的统计信息。
LSP psnp：清除 报文的统计信息。
PSNP interface-number：清除指定接口相关报文统计信息。如果未指定本参数，interface-type将清除所有接口上 IS-IS 报文的统计信息。
process-id：IS-IS 进程号，取值范围为 1～65535，清除指定 IS-IS 进程的报文统计信息。如果未指定本参数，将清除所有 IS-IS 进程的报文统计信息。
【举例】
\# 清除所有 IS-IS 进程的报文统计信息。
<Sysname> reset isis packet【相关命令】
• display isis packet

##### 1.1.98 reset isis peer

reset isis peer 命令用来清除 IS-IS 指定邻居的数据结构信息。

【命令】
reset isis peer system-id [ process-id ]【视图】
用户视图【缺省用户角色】
network-admin【参数】
system-id：IS-IS 邻居的 System ID。
process-id：IS-IS 进程号，取值范围为 1～65535，清除指定 进程邻居的数据结构信息。
IS-IS【使用指导】
本命令用在需要重建某个特定邻居的情况下使用。
【举例】
\# 清除系统 ID 为 0000.0c11.1111 的 IS-IS 邻居的数据结构信息。
<Sysname> reset isis peer 0000.0c11.1111

##### 1.1.99 reset osi statistics

命令用来清除 连接的报文统计信息。
reset osi statistics OSI【命令】
reset osi statistics【视图】
用户视图【缺省用户角色】
network-admin【使用指导】
在某些情况下，需要统计从某个时刻开始的报文统计信息，这时必须在统计开始前清除原有的统计信息，重新进行统计。
【举例】
\# 清除 OSI 连接的报文统计信息。
<Sysname> reset osi statistics【相关命令】
• display osi statistics

##### 1.1.100 set-att

set-att 命令用来配置系统自身发布的 Level-1 LSP 的 ATT 位置位。
undo set-att 命令用来恢复缺省情况。

【命令】
set-att { always | never } undo set-att【缺省情况】
系统自身发布的 Level-1 LSP 的 ATT 位不置位。
【视图】
IS-IS 视图【缺省用户角色】
network-admin【参数】
always：保持对 Level-1 LSP 的 ATT 位置位。
never：保持对 Level-1 LSP 的 ATT 位不置位。
【举例】
\# 设置 ATT 位置位。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] set-att always

##### 1.1.101 set-overload

set-overload 命令用来配置过载标志位。
undo set-overload 命令用来恢复缺省情况。
【命令】
IS-IS 视图：
set-overload [ on-startup [ [ start-from-nbr system-id [ timeout1 [ nbr-timeout ] ] ] | timeout2 | wait-for-bgp [ timeout3 ] ] ] [ allow { external | interlevel } * ] undo set-overload单播地址族视图：
IS-IS IPv6 set-overload [ on-startup [ [ start-from-nbr system-id [ timeout1 [ nbr-timeout ] ] ] | timeout2 | wait-for-bgp+ [ timeout3 ] ] ] [ allow { external | interlevel } * ] undo set-overload【缺省情况】
未配置过载标志位。
【视图】
视图IS-IS单播地址族视图IS-IS IPv6

【缺省用户角色】
network-admin【参数】
on-startup：系统启动时将过载标志位置位。
]：从系统启动时开始计算，如start-from-nbr system-id [ timeout1 [ nbr-timeout ]果在 参数指定的时长内仍未与指定邻居建立邻接关系完毕，过载标志位将结束置位nbr-timeout状态；如果在 nbr-timeout 参数指定的时长内与指定邻居建立邻接关系完毕，过载标志位将继续保持置位状态，且从与指定邻居建立邻接关系时重新计时，在 timeout1 参数配置的时长内保持置位状态。
• system-id：指定邻居的 System ID。
• timeout1：取值范围为 5～86400 秒，缺省值为 600。
• nbr-timeout：取值范围为 5～86400 秒，缺省值为 1200。
timeout2：从系统启动时开始计算，过载标志位保持置位状态的时间长度，取值范围为 5～86400秒。缺省值为 600。
]：从系统启动时开始计算，如果在 参数指定的时长内wait-for-bgp [ timeout3 timeout3仍未收敛，过载标志位将结束置位状态。timeout3 取值范围为 5～86400 秒，缺省值为 600。
BGP ]：从系统启动时开始计算，如果在 参数指定的时长wait-for-bgp4+ [ timeout3 timeout3内 IPv6 BGP 仍未收敛，过载标志位将结束置位状态。timeout3 取值范围为 5～86400 秒，缺省值为 600。
allow：允许发布地址前缀。缺省情况下，当系统进入过载状态时不允许发布地址前缀。
external：当配置 allow 时，允许发布从其它协议学来的 IP 地址前缀。
interlevel：当配置 allow 时，允许发布从不同层次学来的 IP 地址前缀。
【使用指导】
如果没有指定 参数，IS-IS 将立即把过载标志位置位且一直保持置位状态直到用户通on-startup过 清除过载标志位。
undo set-overload如果只指定 参数，过载标志位将在系统启动时开始置位，并且在 参数指on-startup timeout2定的时长内保持置位状态。
【举例】
\# 在当前路由器上配置过载标志位。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] set-overload

##### 1.1.102 snmp context-name

snmp context-name 命令用来配置管理 IS-IS 的 SNMP 实体所使用的上下文名称。
undo snmp context-name 命令用来恢复缺省情况。
【命令】
snmp context-name context-name undo snmp context-name

【缺省情况】
未配置管理 IS-IS 的 SNMP 实体所使用的上下文名称。
【视图】
IS-IS 视图【缺省用户角色】
network-admin【参数】
context-name：管理 IS-IS 的 SNMP 实体所使用的上下文名称，为 1～32 个字符的字符串，区分大小写。
【举例】
\# 配置管理 IS-IS 进程 1 的 SNMP 实体所使用的上下文名称为 isis。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] snmp context-name isis

##### 1.1.103 snmp-agent trap enable isis

snmp-agent trap enable isis 命令用来开启 IS-IS 的告警功能。
undo snmp-agent trap enable isis 命令用来关闭 IS-IS 的告警功能。
【命令】
snmp-agent trap enable isis [ adjacency-state-change | area-mismatch | authentication | authentication-type | buffsize-mismatch | id-length-mismatch | lsdboverload-state-change | lsp-corrupt | lsp-parse-error | lsp-size-exceeded | manual-address-drop | max-seq-exceeded | maxarea-mismatch | own-lsp-purge | protocol-support | rejected-adjacency | skip-sequence-number | version-skew ] * undo snmp-agent trap enable isis [ adjacency-state-change | area-mismatch | authentication | authentication-type | buffsize-mismatch | id-length-mismatch | lsdboverload-state-change | lsp-corrupt | lsp-parse-error | lsp-size-exceeded | manual-address-drop | max-seq-exceeded | maxarea-mismatch | own-lsp-purge | protocol-support | rejected-adjacency | skip-sequence-number | version-skew ] *【缺省情况】
IS-IS 的告警功能处于开启状态。
【视图】
系统视图【缺省用户角色】
network-admin

【参数】
adjacency-state-change：IS-IS 邻居状态变化。
area-mismatch：Hello 报文区域地址不匹配。
authentication：IS-IS 报文认证失败。
authentication-type：IS-IS 报文认证类型错误。
buffsize-mismatch：LSP 报文长度和产生缓冲区大小不匹配。
id-length-mismatch：IS-IS 报文中 System ID 长度不匹配。
lsdboverload-state-change：LSDB 过载状态变化。
lsp-corrupt：LSP 在 中校验和错误。
LSDB lsp-parse-error：LSP 报文解析错误。
lsp-size-exceeded：超大的 报文导致泛洪失败。
LSP manual-address-drop：手动配置区域地址丢弃。
max-seq-exceeded：LSP 序列号超过最大序列号。
maxarea-mismatch：最大配置区域地址数不匹配。
own-lsp-purge：尝试清除本地 LSP。
protocol-support：报文协议支持类型不匹配。
rejected-adjacency：Hello 报文邻接不匹配丢弃。
skip-sequence-number：跳过已经产生过的 LSP 序列号。
version-skew：Hello 报文版本号不匹配。
【使用指导】
如果未指定任何参数，将开启 IS-IS 所有类型的告警功能。
如果配置时不存在任何 IS-IS 进程，将会提示无 IS-IS 进程，并不允许配置。
如果删除了所有配置的 IS-IS 进程，则本功能不生效。
【举例】
关闭 的告警功能。
\# IS-IS <Sysname> system-view [Sysname] undo snmp-agent trap enable isis

##### 1.1.104 summary

summary 命令用来配置一条聚合路由。
命令用来删除指定的聚合路由。
undo summary【命令】
IS-IS IPv4 单播地址族视图：
summary ip-address { mask-length | mask } [ avoid-feedback | generate_null0_route | [ level-1 | level-1-2 | level-2 ] | tag tag ] * undo summary ip-address { mask-length | mask } [ level-1 | level-1-2 | level-2 ] IS-IS IPv6 单播地址族视图：

summary ipv6-prefix prefix-length [ avoid-feedback | generate_null0_route | [ level-1 | level-1-2 | level-2 ] | tag tag ] * undo summary ipv6-prefix prefix-length [ level-1 | level-1-2 | level-2 ]【缺省情况】
不对路由进行聚合。
【视图】
IS-IS IPv4 单播地址族视图IS-IS IPv6 单播地址族视图【缺省用户角色】
network-admin【参数】
ip-address：聚合路由的目的 地址。
IP mask-length：聚合路由的网络掩码长度，取值范围为 0～32。
mask：聚合路由的网络掩码，点分十进制格式。
ipv6-prefix：IPv6 IS-IS 聚合路由前缀。
prefix-length：IPv6 IS-IS 聚合路由前缀长度，取值范围为 0～128。
avoid-feedback：避免通过路由计算学习到聚合路由。
generate_null0_route：为防止路由循环而生成 NULL0 路由。
level-1：只对引入到 Level-1 区域的路由进行聚合。
level-1-2：对引入到 Level-1 和 Level-2 区域的路由都进行聚合。
level-2：只对引入到 Level-2 区域的路由进行聚合。
tag tag：管理标记，取值范围为 1～4294967295。
【使用指导】
通过路由聚合，一方面可以减小路由表规模，还可以减少本路由器生成的 LSP 报文大小和 LSDB的规模。其中，被聚合的路由可以是 协议发现的路由，也可以是引入的外部路由。另外，聚IS-IS合后路由的开销值取所有被聚合路由中最小的开销值。
如果不输入 level 参数，则默认只对 level-2 的路由进行聚合。
路由器只对本地生成的 LSP 中的路由进行聚合。
【举例】
\# 配置一条 202.0.0.0/8 的聚合路由。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] address-family ipv4 [Sysname-isis-1-ipv4] summary 202.0.0.0 255.0.0.0

##### 1.1.105 timer lsp-generation

命令用来配置 重新生成的时间间隔。
timer lsp-generation LSP命令用来取消 重新生成的时间间隔的配置。
undo timer lsp-generation LSP

【命令】
timer lsp-generation maximum-interval [ minimum-interval [ incremental-interval ] ] [ level-1 | level-2 ] undo timer lsp-generation [ level-1 | level-2 ]【缺省情况】
重新生成的最大时间间隔为 秒，最小时间间隔为 毫秒，时间间隔惩罚增量为 毫秒。
LSP 5 50 200【视图】
IS-IS 视图【缺省用户角色】
network-admin【参数】
maximum-interval：网络拓扑变化导致 LSP 重新生成时，LSP 生成的最大时间间隔，取值范围为 1～120，单位为秒。
minimum-interval：网络拓扑变化导致 LSP 重新生成时，LSP 生成的最小时间间隔，取值范围为 10～60000，单位为毫秒。
incremental-interval：网络拓扑变化导致 重新生成时，LSP 生成的时间间隔惩罚增量，LSP取值范围为 10～60000，单位为毫秒。
level-1：配置 Level-1 LSP 生成时间间隔。
level-2：配置 Level-2 的 LSP 生成时间间隔，默认不配置级别时对 Level-1 和 Level-2 同时起作用。
【使用指导】
通过调节 LSP 重新生成的时间间隔，可以抑制网络频繁变化可能导致的占用过多带宽资源和路由器资源。LSP 重新生成的时间间隔的变化规则如下：
如果只指定了 参数，那么 重新生成的时间间隔固定为
• maximum-interval LSP maximum-interval。
• 如果未指定 incremental-interval 参数，LSP 重新生成的时间间隔最大为maximum-interval，最小为 minimum-interval。
• 如果指定了 incremental-interval 参数，那么在网络变化频繁的情况下将 LSP重新生成的时间间隔按照 incremental-interval×2 n-2 （n 为连续触发路由计算的次数）进行延长，最大不超过 maximum-interval。在网络变化不频繁的情况下将 重新生成时间间隔缩LSP小到 minimum-interval。
minimum-interval 和 incremental-interval 配置值不允许大于 maximum-interval 配置值。
【举例】
\# 配置 IS-IS LSP 重新生成的最大时间间隔为 10 秒，最小时间间隔为 100 毫秒，时间间隔惩罚增量为 毫秒。
200 <Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] timer lsp-generation 10 100 200

##### 1.1.106 timer lsp-max-age

timer lsp-max-age 命令用来配置当前路由器生成的 LSP 在 LSDB 里的最大生存时间。
undo timer lsp-max-age 命令用来恢复缺省情况。
【命令】
timer lsp-max-age seconds undo timer lsp-max-age【缺省情况】
当前路由器生成的 LSP 在 LSDB 里的最大生存时间为 1200 秒。
【视图】
视图IS-IS【缺省用户角色】
network-admin【参数】
seconds：LSP 在 LSDB 里的最大生存时间，取值范围是 1～65535，单位为秒。
【使用指导】
每个 LSP 都有一个最大生存时间，随着时间的推移最大生存时间将逐渐减小，当 LSP 的最大生存时间为 时，IS-IS 将启动清除过期 的过程。用户可根据网络规模对 的最大生存时间进行0 LSP LSP调整。
【举例】
\# 配置当前路由器生成的 LSP 在 LSDB 里的最大生存时间为 25 分钟，即 1500 秒。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] timer lsp-max-age 1500【相关命令】
•timer lsp-refresh

##### 1.1.107 timer lsp-refresh

命令用来配置 LSP 刷新周期。
timer lsp-refresh命令用来恢复缺省情况。
undo timer lsp-refresh【命令】
seconds timer lsp-refresh undo timer lsp-refresh【缺省情况】
刷新周期为 秒。
LSP 900【视图】
IS-IS 视图

【缺省用户角色】
network-admin【参数】
seconds：LSP 刷新周期，取值范围为 1～65534，单位为秒。
【使用指导】
路由器必须定时刷新自己生成的 LSP，防止 的最大生存时间减小为 0。另外，通过定时刷新LSP LSP 可以使整个区域中的 LSP 保持同步。用户可对 LSP 的刷新周期进行配置，提高 LSP 的刷新频率可以加快网络收敛速度，但是将占用更多的带宽。
timer lsp-refresh 命令配置的时间必须小于 timer lsp-max-age 命令配置的时间，以保证在 LSP 失效前进行刷新。
【举例】
配置当前系统的 刷新周期为 秒。
\# LSP 1500 <Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] timer lsp-refresh 1500【相关命令】
• timer lsp-max-age

##### 1.1.108 timer spf

命令用来配置 路由计算的时间间隔。
timer spf IS-IS命令用来恢复缺省情况。
undo timer spf【命令】
timer spf maximum-interval [ minimum-interval [ incremental-interval ] ] undo timer spf【缺省情况】
IS-IS 路由计算的最大时间间隔为 5 秒，最小时间间隔为 50 毫秒，时间间隔惩罚增量为 200 毫秒。
【视图】
IS-IS 视图IS-IS IPv6 单播地址族视图【缺省用户角色】
network-admin【参数】
maximum-interval：IS-IS 路由计算的最大时间间隔，取值范围为 1～120，单位为秒。
minimum-interval： 路由计算的最小时间间隔，取值范围为 ～ ，单位为毫秒。
IS-IS 10 60000 incremental-interval：IS-IS 路由计算的时间间隔惩罚增量，取值范围为 10～60000，单位为毫秒。

【使用指导】
根据本地维护的 LSDB，运行 IS-IS 协议的路由器通过 SPF 算法计算出以自己为根的最短路径树，并根据这一最短路径树决定到目的网络的下一跳。通过调节 SPF 的计算间隔，可以抑制网络频繁变化可能导致的占用过多带宽资源和路由器资源。
本命令在网络变化不频繁的情况下将连续路由计算的时间间隔缩小到 minimum-interval，而在网络变化频繁的情况下可以进行相应惩罚，将等待时间按照配置的惩罚增量延长，最大不超过maximum-interval。
minimum-interval 和 incremental-interval 配置值不允许大于 maximum-interval 配置值。
【举例】
配置路由器 的 路由计算的最大时间间隔为 秒，最小时间间隔为 毫秒，惩\# Sysname IS-IS 10 100罚增量为 300 毫秒。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] timer spf 10 100 300

##### 1.1.109 virtual-system

virtual-system 命令用来配置 IS-IS 进程的虚拟系统 ID。
命令用来删除虚拟系统 ID。
undo virtual-system【命令】
virtual-system virtual-system-id undo virtual-system virtual-system-id【缺省情况】
未配置 IS-IS 进程的虚拟系统 ID。
【视图】
IS-IS 视图【缺省用户角色】
network-admin【参数】
virtual-system-id：IS-IS 进程的虚拟系统 ID。
【举例】
\# 配置 IS-IS 进程 1 的虚拟系统 ID 为 2222.2222.2222。
<Sysname> system-view [Sysname] isis 1 [Sysname-isis-1] virtual-system 2222.2222.2222

## 06-BGP命令

目 录配置命令

### 1 BGP

1 BGP

#### 1.1 BGP配置命令

##### 1.1.1 additional-paths select-best

命令用来配置 Add-Path 优选路由的最大条数。
additional-paths select-best命令用来恢复缺省情况。
undo additional-paths select-best【命令】
additional-paths select-best best-number undo additional-paths select-best【缺省情况】
优选路由的最大条数为 1。
Add-Path【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图单播地址族视图BGP-VPN IPv6【缺省用户角色】
network-admin【参数】
best-number：Add-Path 优选路由的最大条数，取值范围为 2～32。
【使用指导】
本地实际优选的路由条数不能大于 best-number。
【举例】
在 单播地址族视图下，配置 优选路由的最大条数为 3。
\# BGP IPv4 Add-Path <Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] additional-paths select-best 3【相关命令】
• peer additional-paths
• peer advertise additional-paths best

##### 1.1.2 address-family ipv4

命令用来创建 BGP IPv4 单播地址族、BGP-VPN IPv4 单播地址族、BGP address-family ipv4地址族视图或 组播地址族，并进入相应地址族视图。如果 单播IPv4 RT-Filter BGP IPv4 BGP IPv4

地址族、BGP-VPN IPv4 单播地址族、BGP IPv4 RT-Filter 地址族视图或 BGP IPv4 组播地址族已经存在，则直接进入 单播地址族、BGP-VPN 单播地址族、BGP 地BGP IPv4 IPv4 IPv4 RT-Filter址族或 BGP IPv4 组播地址族视图。
undo address-family ipv4 命令用来删除 BGP IPv4 单播地址族、BGP-VPN IPv4 单播地址族、BGP IPv4 RT-Filter 地址族视图或 BGP IPv4 组播地址族，及相应地址族视图下的所有配置。
【命令】
BGP 实例视图：
address-family ipv4 [ multicast | rtfilter | unicast ] undo address-family ipv4 [ multicast | rtfilter | unicast ] BGP-VPN 实例视图：
address-family ipv4 [ unicast ] undo address-family ipv4 [ unicast ]【缺省情况】
不存在 BGP IPv4 单播地址族、BGP-VPN IPv4 单播地址族、BGP IPv4 RT-Filter 地址族视图和 BGP IPv4 组播地址族。
【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
multicast：指定 IPv4 组播地址族。
rtfilter：指定 BGP IPv4 RT-Filter 地址族。
unicast：指定 IPv4 单播地址族。如果在 BGP 实例视图下执行本命令并指定本参数，则进入 BGP单播地址族视图；如果在 实例视图下执行本命令并指定本参数，则进入IPv4 BGP-VPN BGP-VPN IPv4 单播地址族视图。
【使用指导】
BGP IPv4 单播地址族视图下的配置，只对公网 BGP IPv4 单播地址族的路由和对等体生效。
BGP-VPN IPv4 单播地址族视图下的配置，只对指定 VPN 实例内 BGP IPv4 单播地址族的路由和对等体生效。
BGP IPv4 组播地址族视图下的配置，只对 BGP IPv4 组播地址族的路由和对等体生效。
BGP IPv4 RT-Filter 地址族视图下的配置，只对 BGP IPv4 RT-Filter 地址族的路由和对等体生效。
如果没有指定 multicast、rtfilter 和 unicast 参数，则缺省为 unicast。
【举例】
\# 在 BGP 实例视图下，创建 BGP IPv4 单播地址族，并进入 BGP IPv4 单播地址族视图。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast

[Sysname-bgp-default-ipv4]

##### 1.1.3 address-family ipv6

address-family ipv6 命令用来创建 BGP IPv6 单播地址族、BGP-VPN IPv6 单播地址族或 BGP IPv6 组播地址族，并进入相应地址族视图。如果 BGP IPv6 单播地址族、BGP-VPN IPv6 单播地址族或 组播地址族已经存在，则直接进入 单播地址族、BGP-VPN 单播地BGP IPv6 BGP IPv6 IPv6址族或 BGP IPv6 组播地址族视图。
undo address-family ipv6 命令用来删除 BGP IPv6 单播地址族、BGP-VPN IPv6 单播地址族或 BGP IPv6 组播地址族，及相应地址族视图下的所有配置。
【命令】
BGP 实例视图：
address-family ipv6 [ multicast | unicast ] undo address-family ipv6 [ multicast | unicast ] BGP-VPN 实例视图：
address-family ipv6 [ unicast ] undo address-family ipv6 [ unicast ]【缺省情况】
不存在 BGP IPv6 单播地址族、BGP-VPN IPv6 单播地址族和 BGP IPv6 组播地址族。
【视图】
实例视图BGP实例视图BGP-VPN【缺省用户角色】
network-admin【参数】
unicast：指定 IPv6 单播地址族。如果在 BGP 实例视图下执行本命令并指定本参数，则进入 BGP IPv6 单播地址族视图；如果在 BGP-VPN 实例视图下执行本命令并指定本参数，则进入 BGP-VPN单播地址族视图。
IPv6 multicast：指定 IPv6 组播地址族。
【使用指导】
BGP IPv6 单播地址族视图下的配置，只对公网 BGP IPv6 单播地址族的路由和对等体生效。
单播地址族视图下的配置，只对指定 实例内 单播地址族的路由和对BGP-VPN IPv6 VPN BGP IPv6等体生效。
BGP IPv6 组播地址族视图下的配置，只对 BGP IPv6 组播地址族的路由和对等体生效。
如果没有指定 multicast 和 unicast 参数，则缺省为 unicast。
【举例】
\# 在 BGP 实例视图下，创建 BGP IPv6 单播地址族，并进入 BGP IPv6 单播地址族视图。
<Sysname> system-view [Sysname] bgp 100

[Sysname-bgp-default] address-family ipv6 unicast [Sysname-bgp-default-ipv6]

##### 1.1.4 address-family link-state

命令用来创建 地址族，并进入 地址族视图。如果address-family link-state BGP LS LS BGP LS 地址族已经存在，直接进入 BGP LS 地址族视图。
undo address-family link-state 命令用来删除 BGP LS 地址族，及相应地址族视图下的所有配置。
【命令】
address-family link-state undo address-family link-state【缺省情况】
不存在 地址族。
BGP LS【视图】
BGP 实例视图【缺省用户角色】
network-admin【使用指导】
BGP LS 地址族视图下的配置，只对公网 BGP LS 地址族的路由和对等体生效。
【举例】
在 实例视图下，创建 地址族，并进入 地址族视图。
\# BGP BGP LS BGP LS <Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family link-state [Sysname-bgp-default-ls]

##### 1.1.5 advertise-rib-active

advertise-rib-active 命令用来配置 BGP 发布 IP 路由表中的最优路由。
undo advertise-rib-active 命令用来恢复缺省情况。
【命令】
advertise-rib-active undo advertise-rib-active【缺省情况】
实例视图下，BGP 发布 路由表中的最优路由，不管该路由在 路由表中是否为最优路BGP BGP IP由；其他视图下，与 BGP 实例视图下的配置保持一致。
【视图】
BGP 实例视图BGP IPv4 单播地址族视图

BGP-VPN IPv4 单播地址族BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族【缺省用户角色】
network-admin【使用指导】
配置 advertise-rib-active 命令后可以保证发送出去的 BGP 路由在 IP 路由表中是最优的，以减少 BGP 发送的路由数量。
以下路由不受 advertise-rib-active 命令的影响：
• 通过 import-route 命令引入的路由
• 通过 network 命令发布的路由
• 通过 default-route imported 引入的缺省路由
• IPv4 组播路由
• IPv6 组播路由本命令只对配置改变后生成的路由生效。若想对配置改变前生成的路由生效，则需要通过reset bgp 命令复位 BGP 会话。
BGP 实例视图和 BGP 单播地址族视图下的配置不同时，以 BGP 单播地址族视图下的配置为准。
【举例】
\# 配置 BGP 发布 IP 路由表中的最优路由。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] advertise-rib-active

##### 1.1.6 aggregate

aggregate 命令用来在 BGP 路由表中创建一条聚合路由。
undo aggregate 命令用来删除指定的聚合路由。
【命令】
BGP IPv4 单播地址族视图/BGP-VPN IPv4 单播地址族视图/BGP IPv4 组播地址族视图：
aggregate ipv4-address { mask-length | mask } [ as-set | attribute-policy route-policy-name | detail-suppressed | origin-policy route-policy-name | suppress-policy route-policy-name ] * undo aggregate ipv4-address { mask-length | mask }单播地址族视图/BGP-VPN 单播地址族视图/BGP 组播地址族视图：
BGP IPv6 IPv6 IPv6 aggregate ipv6-address prefix-length [ as-set | attribute-policy route-policy-name | detail-suppressed | origin-policy route-policy-name | suppress-policy route-policy-name ] * undo aggregate ipv6-address prefix-length

【缺省情况】
未配置聚合路由。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图BGP IPv4 组播地址族视图BGP IPv6 组播地址族视图【缺省用户角色】
network-admin【参数】
ipv4-address：聚合路由的目的 地址。
IPv4 mask-length：聚合路由的网络掩码长度，取值范围为 0～32。
mask：聚合路由的网络掩码，点分十进制格式。
ipv6-address：聚合路由的目的 IPv6 地址。
prefix-length：聚合路由的前缀长度，取值范围为 0～128。
as-set：指定聚合路由的 AS_PATH 属性中包含所有具体路由的 AS 路径信息，该 AS_PATH 属性为 类型，即属性中的 号没有顺序要求。如果没有指定本参数，则聚合路由的AS_SET AS AS_PATH属性中不会包含具体路由的 AS 路径信息，只包含当前路由器所在的 AS 号。
attribute-policy route-policy-name：根据指定的路由策略设置聚合路由的属性。
route-policy-name 表示路由策略名称，为 1～63 个字符的字符串，区分大小写。
detail-suppressed：指定仅通告聚合路由，不通告生成该聚合路由的具体路由。如果没有指定本参数，则同时通告聚合路由和生成该聚合路由的具体路由。
route-policy-name：根据指定的路由策略选择用于聚合的源路由，即仅选择origin-policy符合路由策略的具体路由来生成聚合路由。route-policy-name 表示路由策略名称，为 1～63个字符的字符串，区分大小写。
suppress-policy route-policy-name：根据指定的路 由策略过滤具体路由，不通告通过路由策略过滤的具体路由，通告未通过路由策略过滤的具体路由。route-policy-name 表示路由策略名称，为 1～63 个字符的字符串，区分大小写。
【使用指导】
本命令用来手动聚合 路由。如果 路由表中存在属于指定的聚合路由的更具体的路由，即BGP BGP存在目的网络地址属于聚合路由的目的网络地址、且掩码长度大于聚合路由掩码长度的路由，则会在 BGP 路由表中添加该聚合路由。例如，BGP 路由表中存在目的网络地址为 10.1.1.0/24 和
10.1.2.0/24 的路由，则配置 命令后，会生成到达目的网络 10.1.0.0/16 aggregate 10.1.0.0 16的聚合路由。
如果参与聚合的具体路由所包含的 属性不同，那么聚合路由按照 Incomplete、EGP、IGP 的Origin顺序选择 Origin 属性。例如，存在 Origin 属性为 Incomplete 和 IGP 的具体路由时，聚合路由的 Origin属性为 Incomplete 。

如果参与聚合的具体路由包含不同的团体属性（或扩展团体属性）值，且聚合后的路由中不包含属性（原子聚合属性），则生成的聚合路由的团体属性（或扩展团体属性）
ATOMIC_AGGREGATE中携带所有的团体属性（或扩展团体属性）值。
本命令中各参数的用法及注意事项如 表 1-1 所示。
表1-1 参数的用法及注意事项参数 用法及注意事项如果指定了该参数，则可以通过AS_PATH属性中携带的AS号避免路由环路。当聚合的具体路由的AS路径信息较多时，如果具体路由的变化较频繁，则指定as-set参数as-set会导致聚合路由随之频繁改变，引起路由震荡。在这种情况下，不建议指定as-set参数该参数用来设置聚合路由的属性。通过peer route-policy等方式也可以实现相同的功能attribute-policy如需通过attribute-policy修改聚合路由的AS_PATH属性，则不能指定as-set参数。修改聚合路由的AS_PATH属性可能会引起环路，请谨慎使用该参数用来抑制所有具体路由的通告。如果只想对一部分具体路由进行抑制，可以使detail-suppressed用本命令中的suppress-policy参数或peer filter-policy命令该参数用来通过路由策略选择生成聚合路由的具体路由如果某条路由属于聚合路由，但是该路由没有通过路由策略的过滤，则该路由不作为聚合路由的具体路由。路由通告时，该路由不受本命令中detail-suppressed和origin-policy suppress-policy参数的控制origin-policy参数指定的路由策略中不需要配置apply子句，即便配置了apply子句，该子句也不会生效该参数用来抑制部分具体路由的通告。可以使用route-policy的if-match子句有选择地抑制一部分具体路由，其它具体路由仍被通告suppress-policy suppress-policy参数指定的路由策略中不需要配置apply子句，即便配置了apply子句，该子句也不会生效【举例】
\# 在 BGP IPv4 单播地址族视图下，配置在 BGP 路由表中创建一条聚合路由 1.1.0.0/16。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] aggregate 1.1.0.0 255.255.0.0【相关命令】
• display bgp routing-table ipv4 multicast
• display bgp routing-table ipv4 unicast
• display bgp routing-table ipv6 multicast
• display bgp routing-table ipv6 unicast
• summary automatic

##### 1.1.7 balance

balance 命令用来配置进行 BGP 负载分担的路由条数。

命令用来取消 BGP 负载分担功能。
undo balance【命令】
balance [ ebgp | eibgp | ibgp ] number undo balance [ ebgp | eibgp | ibgp ]【缺省情况】
不会进行 BGP 负载分担。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图BGP IPv4 组播地址族视图BGP IPv6 组播地址族视图【缺省用户角色】
network-admin【参数】
ebgp：为 EBGP 路由配置进行负载分担的路由条数，即只在指定数目的 EBGP 路由之间进行负载分担。
eibgp：为 和 路由配置进行负载分担的路由条数，且可以在 和 路由之间EBGP IBGP EBGP IBGP进行负载分担。
ibgp：为 IBGP 路由配置进行负载分担的路由条数，即只在指定数目的 IBGP 路由之间进行负载分担。
number：进行负载分担的 BGP 路由条数。取值为 1 时，表示不进行负载分担。
【使用指导】
BGP 与 IGP 的负载分担不同，BGP 没有明确的度量值来决定是否对路由进行负载分担。BGP 的负载分担需要通过改变 选路规则来实现。
BGP当路由同时满足如下条件时，设备根据本命令配置的进行 BGP 负载分担的路由条数，从这些路由中选择指定数目的路由进行负载分担：
属性、LOCAL_PREF 属性、和 属性完全相同。
• ORIGIN MED对 属性的要求为：
• AS_PATH如果同时配置 和 命令，或者balance as-path-neglect balance as-path-relax (cid:123)
仅配置 balance as-path-neglect 命令，则 AS_PATH 属性可以不同。
如果仅配置 balance as-path-relax 命令，则 AS_PATH 属性内容不同但长度相同的(cid:123)
路由之间能够形成 BGP 负载分担。
如果未配置 balance as-path-neglect 和 balance as-path-relax 命令，则要求(cid:123)
AS_PATH 属性也必须相同。
本命令中 参数的取值范围和 命令相关。通过 命令配置number max-ecmp-num max-ecmp-num系统支持的最大等价路由条数为 m，并重启设备后，number 参数的取值范围将修改为 1～m。

如果没有指定 ebgp、eibgp 和 参数，则表示 和 ibgp，即同时为 EBGP 路由和 IBGP ibgp ebgp路由配置进行负载分担的路由条数，但是不能在 和 路由之间进行负载分担。
EBGP IBGP执行 命令后，不能再执行 命令和balance eibgp number balance [ ebgp | ibgp ] number undo balance [ ebgp | ibgp ]命令；反之亦然。
【举例】
\# 在 BGP IPv4 单播地址族视图下，配置 BGP 负载分担的路由条数为 2 条。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] balance 2【相关命令】
• balance as-path-neglect
• max-ecmp-num（三层技术-IP 路由命令参考/IP 路由基础）

##### 1.1.8 balance as-path-neglect

balance as-path-neglect 命令用来配置不同 AS_PATH 属性的路由能够形成 BGP 负载分担。
undo balanceas-path-neglect 命令用来恢复缺省情况。
【命令】
balance as-path-neglect undo balance as-path-neglect【缺省情况】
不同 AS_PATH 属性的路由之间不能形成 BGP 负载分担。
【视图】
单播地址族视图BGP IPv4 BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图BGP IPv4 组播地址族视图BGP IPv6 组播地址族视图【缺省用户角色】
network-admin【使用指导】
执行 命令后，只是在进行负载分担时忽略 属性，要使得balance as-path-neglect AS_PATH两条或者两条以上的路由形成负载分担，还需要配置 balance 命令。
执行本命令后， BGP 向外发布的路由只携带最佳路由的路由属性，参与负载分担的路由的 AS_PATH属性丢失，因此，存在发生环路的风险。请谨慎使用本命令。

【举例】
\# 在 BGP IPv4 单播地址族视图下，配置不同 AS_PATH 属性的路由能够形成 BGP 负载分担。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] balance as-path-neglect【相关命令】
• balance

##### 1.1.9 balance as-path-relax

balance as-path-relax 命令用来配置内容不同但长度相同的 AS_PATH 属性的路由能够形成BGP 负载分担。
undo balanceas-path-relax 命令用来恢复缺省情况。
【命令】
balance as-path-relax undo balance as-path-relax【缺省情况】
内容不同但长度相同的 属性的路由不能形成 负载分担。
AS_PATH BGP【视图】
单播地址族视图BGP IPv4单播地址族视图BGP-VPN IPv4单播地址族视图BGP IPv6单播地址族视图BGP-VPN IPv6组播地址族视图BGP IPv4 BGP IPv6 组播地址族视图【缺省用户角色】
network-admin【使用指导】
执行 balance as-path-relax 命令后，要使得两条或者两条以上的路由形成负载分担，还需要配置 命令。
balance如果同时配置了命令 balance as-path-relax 和 balance as-path-neglect，则以命令的配置为准。
balance as-path-neglect执行本命令后，BGP 向外发布的路由只携带最佳路由的路由属性，参与负载分担的路由的 AS_PATH属性丢失，因此，存在发生环路的风险。请谨慎使用本命令。
【举例】
\# 在 BGP IPv4 单播地址族视图下，配置内容不同但长度相同的 AS_PATH 属性的路由能够形成 BGP负载分担。
<Sysname> system-view

[Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] balance as-path-relax

##### 1.1.10 bestroute as-path-neglect

命令用来配置 BGP 在选择最优路由时忽略 AS_PATH 属性。
bestroute as-path-neglect命令用来恢复缺省情况。
undo bestroute as-path-neglect【命令】
bestroute as-path-neglect undo bestroute as-path-neglect【缺省情况】
BGP 将 AS_PATH 属性作为选择最优路由的一个条件。
【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【举例】
\# 在 BGP 实例视图下，配置 BGP 在选择最优路由时忽略 AS_PATH 属性。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] bestroute as-path-neglect

##### 1.1.11 bestroute compare-med

命令用来配置对来自同一 AS 的路由进行 MED 排序优选。
bestroute compare-med命令用来恢复缺省情况。
undo bestroute compare-med【命令】
bestroute compare-med undo bestroute compare-med【缺省情况】
不会对来自同一 的路由进行 排序优选。
AS MED【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin

【使用指导】
缺省情况下，系统不会对来自同一 AS 的路由进行 MED 排序优选，即 BGP 选择最优路由时是将新的路由和当前 BGP 路由表中的最优路由进行比较，只要新的路由比当前 BGP 路由表中的最优路由更优，新的路由将成为最优路由，路由学习的顺序有可能会影响最优路由的选择结果。
如果执行了本命令，则路由器学习到新的路由后，首先按照路由来自的 分组，对来自同一AS AS的路由根据 MED 值的大小进行优选，选出 MED 值最小的路由，然后再对优选出来的、来自不同AS 的路由进行优选，从而避免路由优选结果的不确定性。
【举例】
\# 在 BGP 实例视图下，设置在选择最佳路由时，对来自同一 AS 的路由进行 MED 排序优选。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] bestroute compare-med

##### 1.1.12 bestroute igp-metric-ignore

命令用来配置 BGP在选择最优路由时忽略 IGP Metric的比较。
bestroute igp-metric-ignore命令用来恢复缺省情况。
undo bestroute igp-metric-ignore【命令】
bestroute igp-metric-ignore undo bestroute igp-metric-ignore【缺省情况】
在选择最优路由时会比较这些路由下一跳的 路由的 值，并优选 值最小BGP IGP Metric IGP Metric的路由。
【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【举例】
在 实例视图下，配置 在选择最优路由时忽略 的比较。
\# BGP BGP IGP Metric <Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] bestroute igp-metric-ignore

##### 1.1.13 bestroute med-confederation

命令用来配置允许比较来自同一联盟不同子自治系统邻居路bestroute med-confederation由的 属性值。
MED命令用来恢复缺省情况。
undo bestroute med-confederation

【命令】
bestroute med-confederation undo bestroute med-confederation【缺省情况】
不比较来自同一联盟不同子自治系统邻居路由的 MED 属性值。
【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【使用指导】
只有 AS_PATH 里不包含联盟体外的自治系统编号时，才会比较来自同一联盟不同子自治系统邻居路由的 MED 属性值。例如，联盟中包含的子自治系统为 65006 、 65007 和 65009 。如果存在三条路由，它们的 AS-PATH 值分别为 65006 65009、65007 65009 和 65008 65009，MED 值分别为 2、
3、1，由于第三条路由包含了联盟体外的自治系统编号，因此在选择最优路由时第一条路由将成为最优路由。
【举例】
\# 在 BGP 实例视图下，配置允许比较来自同一联盟不同子自治系统邻居路由的 MED 属性值。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] bestroute med-confederation

##### 1.1.14 bestroute origin-as-validation

bestroute origin-as-validation 命令用来配置 BGP RPKI 验证结果参与路由优选。
undo bestroute origin-as-validation 命令用来恢复缺省情况。
【命令】
bestroute origin-as-validation [ allow-invalid ] undo bestroute origin-as-validation【缺省情况】
验证结果不参与路由优选。
BGP RPKI【视图】
BGP IPv4 单播地址族视图单播地址族视图BGP-VPN IPv4单播地址族视图BGP IPv6单播地址族视图BGP-VPN IPv6【缺省用户角色】
network-admin

【参数】
allow-invalid：允许验证结果为 Invalid 的路由参与路由优选。如果未指定本参数，验证结果为Invalid 的路由不会参与路由优选。
【使用指导】
验证结果的优先级从高到低依次为 Valid、Not found、Invalid。
RPKI配置本功能后，RPKI 验证结果将参与路由优选。BGP 选择路由时首先丢弃下一跳不可达的路由，其次按照 RPKI 验证结果进行路由优选，即对于去往同一个 IP 地址（网段）的多条 BGP 路由，选择 RPKI 验证结果优先级最高的路由为最优路由。
无 BGP RPKI 验证结果的路由在与有验证结果的路由共同参与路由优选时，按 Not-found 验证结果处理。
【举例】
在 单播地址族视图下，配置 验证结果参与路由优选。
\# BGP IPv4 BGP RPKI <Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] bestroute origin-as-validation

##### 1.1.15 bestroute router-id-ignore

bestroute router-id-ignore 命令用来配置 BGP 在选择最优路由时忽略 Router ID。
undo bestroute router-id-ignore 命令用来恢复缺省情况。
【命令】
bestroute router-id-ignore undo bestroute router-id-ignore【缺省情况】
BGP 在选择最优路由时会优选 Router ID 最小的路由器发布的路由。
【视图】
实例视图BGP实例视图BGP-VPN【缺省用户角色】
network-admin【举例】
\# 在 BGP 实例视图下，配置 BGP 在选择最优路由时忽略 Router ID。
<Sysname> system-view [Sysname] bgp 1 [Sysname-bgp-default] bestroute router-id-ignore【相关命令】
•bestroute as-path-neglect
•bestroute igp-metric-ignore

##### 1.1.16 bgp

bgp 命令用来启动指定的 BGP 实例，并进入 BGP 实例视图。
undo bgp 命令用来关闭指定的 BGP 实例。
【命令】
bgp as-number [ instance instance-name ] undo bgp [ as-number [ instance instance-name ] ]【缺省情况】
没有运行 BGP，不存在 BGP 实例。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
as-number：本地 AS 号，取值范围为 1～4294967295。
instance instance-name：启动指定 BGP 实例。instance-name 表示 BGP 实例名称，为 1～31 个字符的字符串，区分大小写。如果不指定本参数，则表示启动 default 实例。
【使用指导】
路由器支持四字节 号。
AS一台 路由器上可以同时启动多个 进程，每个 进程对应一个 实例。BGP 为不BGP BGP BGP BGP同的 BGP 实例维护独立的路由表。
BGP 对 BGP 实例具有如下要求：
一个 实例下可以创建多个公网地址族，但不同 实例下不能创建相同的公网地址族
• BGP BGP（公网 IPv4 单播地址族、公网 IPv6 单播地址族）。
• 一个 BGP 实例下可以创建多个 VPN 实例，每个 VPN 实例下可以创建多个地址族，但不同BGP 实例下不能创建相同的 VPN 实例。
• BGP 不同实例的相同地址族下不能配置相同地址的邻居。
• IPv4 组播与 IPv6 组播地址族同时配置时，只能配置在一个 BGP 实例下。
• 不同 BGP 实例对应的 AS 号可以相同，不同 BGP 实例的实例名称不能相同。
【举例】
\# 启动实例 default，指定该 BGP 实例的本地 AS 号为 100，并进入 BGP 实例视图。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default]

##### 1.1.17 bgp apply-policy on-startup duration

命令用来配置设备在重启后发送应用启动策略的bgp apply-policy on-startup duration路由更新消息的时间。

命令用来恢复缺省情况。
undo bgp apply-policy on-startup duration【命令】
bgp apply-policy on-startup duration seconds undo bgp apply-policy on-startup duration【缺省情况】
设备重启后发布的是未应用启动策略的路由更新消息。
【视图】
BGP 实例视图【缺省用户角色】
network-admin【参数】
seconds：发送应用启动策略的路由更新消息的时间，取值范围为 0～3600，单位为秒。取值为0表示始终发送应用启动策略的路由更新消息。
【使用指导】
配置本命令后，在 seconds 时间内，设备将发送应用通过命令 bgp policy on-startup med配置的 MED 属性值的路由更新消息，可以保证在重启时 BGP 先优选其他邻居的所有路由信息，并向其他设备发布，以减少设备重启造成的流量丢失。
【举例】
\# 在 BGP 实例视图下，配置设备在重启后发送应用启动策略的路由更新消息的时间为 100 秒。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] bgp apply-policy on-startup duration 100【相关命令】
• bgp policy on-startup med

##### 1.1.18 bgp policy on-startup med

bgp policy on-startup med 命令用来配置启动策略中的 MED 值。
undo bgp policy on-startup med 命令用来恢复缺省情况。
【命令】
bgp policy on-startup med med-value undo bgp policy on-startup med【缺省情况】
启动策略中的 MED 值为 4294967295。
【视图】
实例视图BGP

【缺省用户角色】
network-admin【参数】
med-value：启动策略中的 MED 度量值，取值范围为 0～4294967295。
【使用指导】
对于应用启动策略的路由，在设备重启后，路由更新消息中的 值将修改为本命令配置的值。
MED【举例】
\# 在 BGP 实例视图下，配置启动策略中的 MED 值为 100。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] bgp policy on-startup med 100【相关命令】
• bgp apply-policy on-startup

##### 1.1.19 bgp update-delay on-startup

bgp update-delay on-startup 命令用来配置设备在重启后延迟发布路由更新消息。
undo bgp update-delay on-startup 命令用来恢复缺省情况。
【命令】
bgp update-delay on-startup seconds undo bgp update-delay on-startup【缺省情况】
设备重启后立刻向 BGP 邻居发布路由更新消息。
【视图】
BGP 实例视图【缺省用户角色】
network-admin【参数】
seconds：延迟发布路由更新消息的时间，取值范围为 0～3600，单位为秒。取值为 0 表示不发布路由更新消息。
【使用指导】
通过配置当前设备在重启后延迟发布路由更新消息，可以保证在重启时 BGP 先引入其他邻居的所有路由信息，然后再优选并向其他设备发布，以减少设备重启造成的流量丢失。
【举例】
\# 在 BGP 实例视图下，配置设备在重启后延迟发布路由更新消息的时间为 100 秒。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] bgp update-delay on-startup 100

【相关命令】
• bgp update-delay on-startup prefix-list

##### 1.1.20 bgp update-delay on-startup prefix-list

bgp update-delay on-startup prefix-list 命令用来配置路由策略控制 BGP 延迟发布。
undo bgp update-delay on-startup prefix-list 命令用来恢复缺省情况。
【命令】
bgp update-delay on-startup prefix-list ipv4-prefix-list-name undo bgp update-delay on-startup prefix-list【缺省情况】
未配置路由策略控制 BGP 延迟发布。
【视图】
实例视图BGP【缺省用户角色】
network-admin【参数】
ipv4-prefix-list-name：IPv4 地址前缀列表名称，为 1～63 个字符的字符串，区分大小写。
【使用指导】
配置 BGP 延迟发布后，如果需要部分路由前缀不受延迟发布控制，可以使用路由策略进行控制，通过过滤的路由不受延迟发布的影响。
目前只支持 IPv4 地址前缀列表。
【举例】
在 实例视图下，配置设备在重启后延迟发布路由更新消息的时间为 秒，配置通过\# BGP 100 IPv4地址前缀列表 aaa 过滤的路由不受延迟发布的影响。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] bgp update-delay on-startup 100 [Sysname-bgp-default] bgp update-delay on-startup prefix-list aaa【相关命令】
• bgp update-delay on-startup

##### 1.1.21 bmp server

bmp server 命令用来创建指定 BGP 监控服务器，并进入 BMP Server 视图。
命令用来删除指定的 监控服务器，及相应 视图下的所有配undo bmp server BGP BMP Server置。
【命令】
bmp server server-number

undo bmp server server-number【缺省情况】
不存在 监控服务器。
BGP【视图】
系统视图【缺省用户角色】
network-admin【参数】
server-number：BGP 监控服务器号，取值范围为 1～8。
【举例】
创建 监控服务器 5，并进入 视图。
\# BGP BMP Server <Sysname> system-view [Sysname] bmp server 5 [Sysname-bmpserver-5]

##### 1.1.22 check-origin-validation

命令用来开启 验证功能。
check-origin-validation BGP RPKI命令用来关闭 BGP RPKI 验证功能。
undo check-origin-validation【命令】
check-origin-validation undo check-origin-validation【缺省情况】
BGP RPKI 验证功能处于关闭状态。
【视图】
BGP RPKI 视图【缺省用户角色】
network-admin【使用指导】
配置本功能后，设备收到 路由时，会对 地址（网段）和源 号进行 验证。验证结BGP IP AS RPKI果有以下三种：
• Not-found：表示 ROA 数据库中不存在包含该 IP 地址（网段）的表项。
• Valid：表示 ROA 数据库中至少存在一条包含该 IP 地址（网段）的表项，且表项中的 AS 号和收到的路由的源 AS 号相同。
• Invalid ：表示 ROA 数据库中至少存在一条包含该 IP 地址（网段）的表项，但表项中的 AS 号和收到的路由的源 AS 号均不同。
用户可以使用路由策略设置 BGP RPKI 验证结果的匹配条件，从而灵活控制路由的发布与接收。

【举例】
\# 开启 BGP RPKI 验证功能。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] rpki [Sysname-bgp-default-rpki] check-origin-validation

##### 1.1.23 compare-different-as-med

命令用来配置允许比较来自不同 路由的 属性值。
compare-different-as-med AS MED命令用来恢复缺省情况。
undo compare-different-as-med【命令】
compare-different-as-med undo compare-different-as-med【缺省情况】
不允许比较来自不同 AS 路由的 MED 属性值。
【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【使用指导】
当一个 路由器通过不同的 对等体得到目的地址相同但下一跳不同的多条路由时，在其BGP EBGP它条件相同的情况下，将优先选择 MED 值较小者作为最佳路由。
除非能够确认不同的 AS 采用了同样的 IGP 和路由选择方式，否则不要使用此命令。
【举例】
\# 在 BGP 实例视图下，允许比较来自不同 AS 路由的 MED 属性值。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] compare-different-as-med

##### 1.1.24 confederation id

confederation id 命令用来配置联盟的 ID。
undo confederation id 命令用来恢复缺省情况。
【命令】
confederation id as-number undo confederation id【缺省情况】
未配置联盟的 ID。

【视图】
BGP 实例视图【缺省用户角色】
network-admin【参数】
as-number：联盟 ID，即标识联盟这一整体的自治系统号，取值范围为 1～4294967295。
【使用指导】
联盟是指将一个大的自治系统划分为几个较小的子自治系统，每个子自治系统中均保持 IBGP 全连接的状态，这些子自治系统组成一个联盟体。路由的一些关键属性（如下一跳、MED、本地优先级）
在通过每个子自治系统时没有丢弃，因此每个子自治系统之间虽然存在 EBGP 关系，但是从联盟外部来看这些子自治系统是一个整体，即一个自治系统，这个自治系统的 号就是联盟 ID。
AS采用联盟的方法既可以保证自治系统的完整性，同时还可以缓解自治系统中 连接数过多的问IBGP题。
属于同一个联盟的所有路由器上，都需要配置相同的联盟 ID。
在联盟外的 BGP 路由器看来，联盟体内路由器的 AS 号为联盟 ID。
【举例】
\# 在 BGP 实例 default 下，ID 号是 9 的联盟体由 38、39、40、41 四个子自治系统组成；对等体 10.1.1.1是子自治系统 38 中的成员；对等体 200.1.1.1 是 AS 联盟体的外部成员，属于 AS 98；对于外部成员来讲，9 号联盟体就是一个统一的自治系统，该自治系统的 号为 9。以子自治系统 为例，AS 41子自治系统中路由器的配置如下。
<Sysname> system-view [Sysname] bgp 41 [Sysname-bgp-default] confederation id 9 [Sysname-bgp-default] confederation peer-as 38 39 40 [Sysname-bgp-default] group Confed38 external [Sysname-bgp-default] peer Confed38 as-number 38 [Sysname-bgp-default] peer 10.1.1.1 group Confed38 [Sysname-bgp-default] group Remote98 external [Sysname-bgp-default] peer Remote98 as-number 98 [Sysname-bgp-default] peer 200.1.1.1 group Remote98【相关命令】
• confederation nonstandard
• confederation peer-as

##### 1.1.25 confederation nonstandard

命令用来配置设备可以与未遵循 实现联盟的路由器互confederation nonstandard RFC 3065通。
undo confederation nonstandard 命令用来恢复缺省情况。
【命令】
confederation nonstandard

undo confederation nonstandard【缺省情况】
设备不能与未遵循 实现联盟的路由器互通，只能与遵循 实现联盟的路由器互RFC 3065 RFC 3065通。
【视图】
BGP 实例视图【缺省用户角色】
network-admin【使用指导】
如果联盟中存在未遵循 的路由器，为了与其互通，保证联盟的正常建立，需要在联盟中RFC 3065所有遵循 RFC 3065 的路由器上配置本命令。
【举例】
\# 在 BGP 实例 default 下，ID 号为 100 的联盟由 64000、65000 两个子自治系统组成，在该联盟内存在未遵循 RFC 3065 实现联盟的路由器。为了保证联盟的正常建立，在遵循 RFC 3065 的路由器上配置其可以与未遵循 RFC 3065 实现联盟的路由器互通。
<Sysname> system-view [Sysname] bgp 64000 [Sysname-bgp-default] confederation id 100 [Sysname-bgp-default] confederation peer-as 65000 [Sysname-bgp-default] confederation nonstandard【相关命令】
•confederation id
• confederation peer-as

##### 1.1.26 confederation peer-as

confederation peer-as 命令用来配置联盟中的子自治系统。
undo confederation peer-as 命令用来删除联盟中的子自治系统。
【命令】
confederation peer-as as-number-list undo confederation peer-as [ as-number-list ]【缺省情况】
未配置联盟中的子自治系统。
【视图】
BGP 实例视图【缺省用户角色】
network-admin

【参数】
as-number-list：子自治系统号列表，在同一条命令中最多可配置 32 个子自治系统，表示方式为 = as-number&<1-32>。其中，as-number 为子自治系统号，取值范围为as-number-list 1～4294967295；&<1-32>表示前面的参数可以输入 1～32 次。
【使用指导】
在配置本命令之前，必须通过 confederation id 命令指定联盟 ID，否则本命令配置不成功。
执行 undo confederation peer-as 命令时，如果不指定 as-number-list 参数，则表示删除联盟中所有的子自治系统。
【举例】
\# 在 BGP 实例视图下，配置属于联盟 10 的子自治系统号为 2000 和 2001。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] confederation id 10 [Sysname-bgp-default] confederation peer-as 2000 2001【相关命令】
• confederation id
• confederation nonstandard

##### 1.1.27 dampening

dampening 命令用来配置 BGP 路由衰减。
undo dampening 命令用来恢复缺省情况。
【命令】
dampening [ half-life-reachable half-life-unreachable reuse suppress ceiling | route-policy route-policy-name ] * undo dampening【缺省情况】
未配置 路由衰减。
BGP【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图BGP IPv4 组播地址族视图组播地址族视图BGP IPv6【缺省用户角色】
network-admin

【参数】
half-life-reachable：发生振荡的可达路由的半衰期，取值范围为 1～45，单位为分钟，缺省值为 15 分钟。
half-life-unreachable：发生振荡的不可达路由的半衰期，取值范围为 1～45，单位为分钟，缺省值为 分钟。
15 reuse：路由的再使用阈值，取值范围为 1～20000，缺省值为 750。当惩罚值降低到该值以下时，此路由变为可用路由，参与路由选择。路由的再使用阈值必须小于 suppress。
suppress：路由的抑制阈值，取值范围为 1～20000，缺省值为 2000。当惩罚值超过该值时，此路由被抑制，不参与路由选择。
ceiling：惩罚值的上限，取值范围为 1001～20000，缺省值为 16000。惩罚值达到该值后，不再增加。惩罚值的上限必须大于 suppress。
： 通 过 路 由 策 略 指 定 对 哪 些 路 由 进 行 路 由 衰 减 。
route-policy route-policy-name表示路由策略名称，为 1～63 个字符的字符串，区分大小写。
route-policy-name【使用指导】
该命令只对 EBGP 路由生效，对 IBGP 路由无效。
配置本命令后，EBGP 邻居 了之后，来自该邻居的路由不会被删除，而是进行路由衰减。
down【举例】
\# 在 BGP IPv4 单播地址族视图下，配置 BGP 路由衰减，可达路由和不可达路由的半衰期均为 10分钟，路由的再使用阈值为 1000，抑制阈值为 2000，惩罚值上限为 10000。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] dampening 10 10 1000 2000 10000【相关命令】
• display bgp dampening parameter

##### 1.1.28 default local-preference

default local-preference 命令用来配置本地优先级的缺省值。
undo default local-preference 命令用来恢复缺省情况。
【命令】
default local-preference value undo default local-preference【缺省情况】
本地优先级的缺省值为 100。
【视图】
单播地址族视图BGP IPv4单播地址族视图BGP-VPN IPv4单播地址族视图BGP IPv6

BGP-VPN IPv6 单播地址族视图BGP IPv4 组播地址族视图BGP IPv6 组播地址族视图【缺省用户角色】
network-admin【参数】
value：本地优先级的缺省值，取值范围为 0～4294967295。该值越大，则优先级越高。
【使用指导】
除本命令外，还可以通过路由策略中的 apply local-preference 命令来配置 BGP 路由的本地优先级。如果未配置路由策略，则所有 BGP 路由的本地优先级均为本命令配置的值；如果配置了路由策略，则通过路由策略过滤的 路由的本地优先级为 命令配BGP apply local-preference置的值，未通过路由策略过滤的 BGP 路由的本地优先级为本命令配置的值。
【举例】
\# 在 BGP IPv4 单播地址族视图下，配置本地优先级的缺省值为 180。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] default local-preference 180【相关命令】
• apply local-preference（三层技术-IP 路由命令参考/路由策略）
• route-policy（三层技术-IP 路由命令参考/路由策略）

##### 1.1.29 default med

default med 命令用来配置 MED 的缺省值。
undo default med 命令用来恢复缺省情况。
【命令】
default med med-value undo default med【缺省情况】
MED 的缺省值为 0。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图BGP IPv4 组播地址族视图BGP IPv6 组播地址族视图

【缺省用户角色】
network-admin【参数】
med-value：MED 的缺省值，取值范围为 0～4294967295。
【使用指导】
可以通过多种方式配置 路由的 值，按照优先级从高到底的顺序依次为：
BGP MED
(1) 通过路由策略中的 命令设置的 MED 值；
apply cost
(2) 通过 命令中的 参数设置的 MED 值；
import-route med
(3) 通过 命令配置的 MED 值；
default med
(4) 学习到的 BGP 路由自身的 MED 值，或引入的 IGP 路由自身的 metric 值。
【举例】
在 单播地址族视图下，配置 的缺省值为 25。
\# BGP IPv4 MED <Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] default med 25【相关命令】
cost（三层技术-IP 路由命令参考/路由策略）
• apply
•import-route route-policy（三层技术-IP 路由命令参考/路由策略）
•

##### 1.1.30 default-route imported

命令用来允许将缺省路由引入到 BGP 路由表中。
default-route imported命令用来恢复缺省情况。
undo default-route imported【命令】
default-route imported undo default-route imported【缺省情况】
不允许将缺省路由引入到 路由表中。
BGP BGP【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图单播地址族视图BGP-VPN IPv6组播地址族视图BGP IPv4组播地址族视图BGP IPv6

【缺省用户角色】
network-admin【使用指导】
执行 命令引入 IGP 路由时，缺省情况下不会将 IGP 的缺省路由引入到 BGP 路由import-route表中。如果执行 命令的同时，执行了 命令，则import-route default-route imported IGP的缺省路由可以引入到 BGP 路由表中。
【举例】
\# 在 BGP IPv4 单播地址族视图下，配置允许将 OSPF 进程 1 的缺省路由引入到 BGP 路由表中。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] default-route imported [Sysname-bgp-default-ipv4] import-route ospf 1【相关命令】
• import-route

##### 1.1.31 default-route update-first

命令用来配置优先发送缺省路由的撤销消息。
default-route update-first命令用来恢复缺省情况。
undo default-route update-first【命令】
default-route update-first undo default-route update-first【缺省情况】
不优先发送缺省路由的撤销消息。
【视图】
BGP 实例视图【缺省用户角色】
network-admin【使用指导】
路由器向对等体发送路由撤销消息时，不会优先发送缺省路由的撤销消息。当 邻居关系BGP BGP断开时，无法保证优先撤销缺省路由，可能会造成流量中断。配置本命令后，当 BGP 邻居关系断开时，将优先发送缺省路由的撤销消息，这样可以尽快将流量切换到有效路径上，尽可能减少流量中断的时间。
【举例】
\#在 实例视图下，配置优先发送缺省路由的撤销消息。
BGP <Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] default-route update-first

##### 1.1.32 display bgp bmp server

display bgp bmp server 命令用来显示 BGP 监控服务器的信息。
【命令】
display bgp [ instance instance-name ] bmp server server-number【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
instance instance-name：显示指定 BGP 实例的信息。instance-name 表示 BGP 实例的名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示 default 实例的信息。
server-number：显示指定 BGP 监控服务器的信息，server-number 取值范围为 1～8。
【举例】
\# 显示 BGP 监控服务器 1 的信息。
<Sysname> display bgp bmp server 1 BMP server number: 1 Server address: 100.1.1.1 Server port: 6895 Client address: 100.1.1.2 Client port: 21452 BMP server state: Connected Up for 00h41m53s TCP source interface has been configured Message statistics:
Total messages sent: 15 INITIATION: 1 TERMINATION: 0 STATS-REPORT: 0 PEER-UP: 4 PEER-DOWN: 3 ROUTE-MON: 7 BMP monitor BGP peers:
10.1.1.1表1-2 display bgp bmp server 命令输出信息描述表字段 描述BMP server number BGP监控服务器号Server address 监控服务器建立 TCP 连接的地址Server port 监控服务器建立TCP连接的端口号与监控服务器建立TCP连接的本地地址Client address

字段 描述Client port 与监控服务器建立TCP连接的端口号本地与监控服务器TCP连接的状态：
BMP server current state • Connected：表示 TCP 连接已经建立
• Not connected：表示 TCP 连接未建立Up for 本地与监控服务器TCP连接的时间TCP source interface has been与监控服务器建立TCP连接的源接口configured Total messages sent BGP向监控服务器发送的报文个数INITIATION BGP向监控服务器发送INITIATION报文的个数BGP向监控服务器发送TERMINATION报文的个数TERMINATION STATS-REPORT BGP向监控服务器发送统计报文的个数PEER-UP BGP向监控服务器发送PEER-UP报文的个数PEER-DOWN BGP向监控服务器发送PEER-DOWN报文的个数BGP向监控服务器发送ROUTE-MON报文的个数ROUTE-MON BMP monitor BGP peers BGP监控服务器监控的邻居信息【相关命令】
• reset bgp bmp server statistics

##### 1.1.33 display bgp dampening parameter

命令用来显示 路由衰减参数。
display bgp dampening parameter BGP【命令】
display bgp [ instance instance-name ] dampening parameter { ipv4 | ipv6 } [ multicast | [ unicast ] [ vpn-instance vpn-instance-name ] ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
instance instance-name：显示指定 BGP 实例的信息。instance-name 表示 BGP 实例的名称，为 1 ～ 31 个字符的字符串，区分大小写。如果未指定本参数，则显示 default 实例的信息。
ipv4：显示 BGP IPv4 路由的路由衰减参数。
ipv6：显示 BGP IPv6 路由的路由衰减参数。
multicast：显示 BGP 组播路由的路由衰减参数。

unicast：显示 BGP 单播路由的路由衰减参数。
： 显 示 指 定 VPN 实 例 的 BGP 路 由 衰 减 参 数 。
vpn-instance vpn-instance-name表示 的 实例名称，为 1～31 个字符的字符串，区分大vpn-instance-name MPLS L3VPN VPN小写。如果不指定本参数，则显示公网 BGP 路由衰减参数。
【使用指导】
如果没有指定 和 参数，则缺省为 unicast。
unicast multicast【举例】
\# 显示 BGP IPv4 单播路由的路由衰减参数。
<Sysname> display bgp dampening parameter ipv4 Maximum suppression time (in seconds) : 3973 Ceiling value : 16000 Reuse value : 750 Half-life time for reachable routes (in seconds) : 900 Half-life time for unreachable routes (in seconds) : 900 Suppression threshold : 2000表1-3 命令显示信息描述表display bgp dampening parameter字段 描述最大抑制时间，即惩罚值从上限下降到再使用阈值所需要的最大时间，Maximum suppression time单位为秒惩罚值的上限Ceiling value Reuse value 再使用阈值Half-life time for reachable routes 可达路由的半衰期，单位为秒Half-life time for unreachable routes 不可达路由的半衰期，单位为秒抑制阈值Suppression threshold【相关命令】
•dampening

##### 1.1.34 display bgp group

命令用来显示 BGP 对等体组的信息。
display bgp group【命令】
display bgp [ instance instance-name ] group ipv4 [ multicast | rtfilter | [ unicast ] [ vpn-instance vpn-instance-name ] ] [ group-name group-name ] display bgp [ instance instance-name ] group ipv6 [ multicast | [ unicast ] [ vpn-instance vpn-instance-name ] ] [ group-name group-name ] display bgp [ instance instance-name ] group link-state [ group-name group-name ]

display bgp [ instance instance-name ] group l2vpn evpn [ group-name group-name ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
instance-name：显示指定 BGP 实例的信息。instance-name 表示 BGP 实例的名instance称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示 实例的信息。
default ipv4：显示 对等体组的信息。
BGP IPv4 ipv6：显示 对等体组的信息。
BGP IPv6 link-state：显示 BGP LS 对等体组的信息。
multicast：显示 BGP 组播对等体组的信息。
rtfilter：显示 BGP IPv4 RT-Filter 对等体组的信息。
unicast：显示 BGP 单播对等体组的信息。
l2vpn：显示 BGP L2VPN 对等体组的信息。
evpn：显示 BGP EVPN 对等体组的信息。
： 显 示 指 定 VPN 实 例 的 BGP 对 等 体 组 的 信 息 。
vpn-instance vpn-instance-name表示 的 实例名称，为 1～31 个字符的字符串，区分大vpn-instance-name MPLS L3VPN VPN小写。如果不指定本参数，则显示公网 BGP 对等体组的信息。
group-name：显示指定 对等体组的详细信息，group-name 为 对等体group-name BGP BGP组的名称，为 1～47 个字符的字符串，区分大小写。如果没有指定本参数，则显示指定地址族所有BGP 对等体组的简要信息。
【使用指导】
如果没有指定 unicast、multicast 参数，则缺省为 unicast。
【举例】
\# 显示所有 BGP IPv4 单播对等体组的简要信息。
<Sysname> display bgp group ipv4 BGP peer group: group1 Remote AS: 600 Type: external Members:
1.1.1.10 BGP peer group: group2 Remote AS number: not specified Type: external Members:
2.2.2.2

\# 显示 BGP IPv4 单播对等体组 group1 的详细信息。
<Sysname> display bgp group ipv4 group-name group1 BGP peer group: group1 Remote AS: 600 Type: external Maximum number of prefixes allowed: 4294967295 Threshold: 75% Configured hold time: 180 seconds Keepalive time: 60 seconds Minimum time between advertisements: 30 seconds Peer preferred value: 0 Site-of-Origin: Not specified Routing policy configured:
No routing policy is configured Members:
* - Dynamically created peer Peer AS MsgRcvd MsgSent OutQ PrefRcv Up/Down State
1.1.1.10 600 0 0 0 0 00:00:55 Established显示 单播对等体组 的详细信息。
\# BGP IPv6 group2 <Sysname> display bgp group ipv6 group-name group2 BGP peer group: group2 Remote AS: 600 Type: external Maximum number of prefixes allowed: 4294967295 Threshold: 75% Configured hold time: 180 seconds Keepalive time: 60 seconds Minimum time between advertisements: 30 seconds Peer preferred value: 0 IPsec profile name: profile001 Site-of-Origin: Not specified Routing policy configured:
No routing policy is configured Members:
* - Dynamically created peer Peer AS MsgRcvd MsgSent OutQ PrefRcv Up/Down State 2::2 600 0 0 0 0 00:00:45 Established 3::3 600 0 0 0 0 00:00:40 Established

表1-4 display bgp group 命令输出信息描述表字段 描述BGP peer group BGP对等体组名称对等体组的AS号Remote AS对等体组类型，取值包括：
Type • external：表示 EBGP 对等体组
• internal：表示 IBGP 对等体组Maximum number of prefixes allowed 允许从对等体学习的最大路由数路由器产生日志信息的阈值，即从对等体接收的路由前缀数量与允Threshold许的最大路由数的百分比达到此值时，路由器将产生日志信息Configured hold time 配置的保持时间间隔，单位为秒Keepalive time 存活时间间隔，单位为秒Minimum time between advertisements 路由发布的最小时间间隔，单位为秒为来自对等体的路由指定的首选值Peer preferred value Site-of-Origin 为对等体组指定的SoO属性值为对等体组指定的路由策略Routing policy configured如果未指定路由策略，则显示为No routing policy is configured Members 对等体组包括的对等体信息如果对等体的地址前存在“*”，则表示该对等体为动态创建的对等
* - Dynamically created peer体Peer 对等体的IPv4地址或IPv6地址AS 对等体所在的自治系统号MsgRcvd 从该对等体收到的消息数目MsgSent 向该对等体发送的消息数目OutQ 等待发往该对等体的消息数目PrefRcv 对于IPv4、IPv6地址族，表示从该对等体收到的前缀数目BGP会话处于当前状态的时长Up/Down State 该对等体的状态IPsec profile name 为BGP IPv6对等体组应用的IPsec安全框架名

##### 1.1.35 display bgp instance-info

命令用来显示所有 实例的信息。
display bgp instance-info BGP【命令】
display bgp instance-info

【视图】
任意视图【缺省用户角色】
network-admin network-operator【举例】
\# 显示所有 BGP 实例的信息。
<Sysname> display bgp instance-info Total BGP instances: 3 BGP instance name AS BGP1 100 BGP2 200 BGP3 300表1-5 display bgp instance-info 命令输出信息描述表字段 描述Total BGP instances BGP实例总数BGP instance name BGP实例名称AS BGP实例对应的AS号

##### 1.1.36 display bgp link-state

命令用来显示 BGP LS 地址族信息。
display bgp link-state【命令】
display bgp [ instance instance-name ] link-state [ ls-prefix | peer { ipv4-address | ipv6-address } { advertised | received } [ statistics ] | statistics ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
instance instance-name：显示指定 BGP 实例的信息。instance-name 表示 BGP 实例的名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示 default 实例的信息。
ls-prefix：显示指定的 LS 信息。ls-prefix 为指定的 LS 前缀。如果未指定本参数，则显示所有的 LS 信息。

ipv4-address：显示向指定对等体发布或者从指定对等体收到的 BGP LS 信息。ipv4-address为对等体的地址。
ipv6-address：显示向指定对等体发布或者从指定对等体收到的 信息。ipv6-address BGP LS为对等体的地址。
advertised：显示发布的 LS 信息。
received：显示接收的 LS 信息。
statistics：显示 LS 信息的统计个数。
【使用指导】
如果没有指定任何参数，则显示所有 BGP LS 的简要信息。
【举例】
\# 显示所有公网 BGP LS 地址族的简要信息。
<Sysname> display bgp link-state Total number of routes: 2 BGP local router ID is 1.1.2.1 Status codes: * - valid, > - best, d – dampened, h – history, s – suppressed, S – stale, i - internal, e - external a - additional-path Origin: i - IGP, e - EGP, ? - incomplete Prefix codes: E link, V node, T IP reachable route, u/U unknown, I Identifier, N local node, R remote node, L link, P prefix, L1/L2 ISIS level-1/level-2, O OSPF, D direct, S static, a area-ID, , l link-ID, t topology-ID, s ISO-ID, c confed-ID/ASN, b bgp-identifier, r router-ID, i if-address, n peer-address, o OSPF Route-type, p IP-prefix d designated router address
* >e Network : [V][O][I0x0][N[c20][b1.1.1.2][a0.0.0.0][r1.1.1.2]]/376 NextHop : 1.1.1.2 LocPrf :
PrefVal : 0 OutLabel : NULL MED :
Path/Ogn: 20i
* >e Network :
[T][O][I0x0][N[c20][b1.1.1.2][a0.0.0.0][r1.1.1.2]][P[o0x1][p1.1.1.0/24]]/480 NextHop : 1.1.1.2 LocPrf :
PrefVal : 0 OutLabel : NULL MED :
Path/Ogn: 20i表1-6 display bgp link-state 命令简要显示信息描述表字段 描述Total number of routes 路由的总数BGP local router ID 本地的路由器ID

字段 描述路由状态代码：
•
* – valid：合法路由
• > – best：优选最佳路由
• d - dampened：振荡抑制路由
• h – history：历史路由Status codes
• s – suppressed：聚合抑制路由
• S – stale：过期路由
• i – internal：内部路由
• external：外部路由e –
• a - additional-path：Add-Path 优选路由路由状态代码：
• E – link：链路描述信息
• V – node ：节点描述信息
• route：IP 可达描述信息T – IP reachable
• u/U – unknown：未知描述信息
• Identifier：标识位I –
• N – local node：本地节点
•R – remote node：远端节点
• L – link：链路
• P – prefix：前缀
• L1/L2 – ISIS level-1/level-2：IS-IS 协议的 L1 或 L2 层
• O – OSPF：OSPF 协议
• D – direct：直连协议Prefix codes • S – static：静态路由协议
• area-ID：区域标识a –
• l – link-ID：链路标识
• topology-ID：拓扑标识t –
• s – ISO-ID：ISO 标识
• c – confed-ID/ASN：联盟或自治系统号
• b – bgp-identifier：BGP LS 标识
• r – router-ID：路由器标识
• i – if-address：接口地址
• n – peer-address：邻居地址
• Route-type：OSPF 路由类型o – OSPF
• p – IP-prefix：IP 前缀
• ：指定路由器地址d – designated router address
• a - additional-path：Add-Path 优选路由路由信息的来源，取值包括：
Origin
• IGP：表示路由产生于本 内。通过 命令发布路由的路由信息i – AS network

字段 描述来源为 IGP
• e – EGP：表示路由是通过 EGP（Exterior Gateway Protocol，外部网关协议）
学到的。
• ? – incomplete：表示路由的来源无法确定。从 IGP 协议引入路由的路由信息来源为 incomplete Network LS的NLRI信息NextHop 下一跳IP地址LocPrf 本地优先级（暂不支持）路由的出标签值OutLabel MED MED（Multi-Exit-Discriminator，多出口区分）属性值路由的AS路径（AS_PATH）属性和路由信息的来源（ORIGIN）属性，其中：
• 属性记录了此路由经过的所有 AS，可以避免路由环路的出现Path/Ogn AS_PATH
• ORIGIN 属性标记了此路由如何成为 BGP 路由显示指定 前缀的 地址族的详细信息。
\# LS BGP LS <Sysname> display bgp link-state [V][O][I0x0][N[c20][b1.1.1.2][a0.0.0.0][r1.1.1.2]]/376 BGP local router ID: 1.1.1.2 Local AS number: 20 Paths: 1 available, 1 best BGP LS information of [V][O][I0x0][N[c20][b1.1.1.2][a0.0.0.0][r1.1.1.2]]/376:
Imported route.
Original nexthop: 0.0.0.0 OutLabel : NULL RxPathID : 0x0 TxPathID : 0xffffffff LS : Node flag bits: 30[EA] AS-path : (null)
Origin : igp Attribute value : pref-val 32768 State : valid, local, best IP precedence : N/A QoS local ID : N/A Traffic index : N/A表1-7 display bgp link-state 命令详细显示信息描述表字段 描述本地的AS号Local AS number路由数信息Paths
• available：有效路由数目

字段 描述
• best：最佳路由数目BGP LS information of NLRI前缀字段该路由为引入的路由Imported route路由的原始下一跳地址，如果是从BGP更新消息中获得的路由，则该地址为接收到Original nexthop的消息中的下一跳IP地址LS属性信息：
• bits：节点属性位信息，16 进制表示Node flag LS 10[A]：OSPF 的 ABR 位(cid:123)
30[E]：OSPF 的 External 位(cid:123)
• Metric：Link 或 的链路开销值Prefix RxPathID 接收到的路由的Add-Path ID值TxPathID 发送的路由的Add-Path ID值路由的AS路径（AS_PATH）属性，记录了此路由经过的所有AS，可以避免路由环AS-path路的出现BGP路由属性信息，包括：
• MED：与目的网络关联的 MED 值Attribute value • localpref：本地优先级
• pref-val：路由首选值
• pre：协议优先级路由当前状态，取值包括：
• valid：有效路由
• internal：内部路由State • external：外部路由
• local：本地产生路由
• synchronize：同步路由
• best：最佳路由IP precedence 路由的IP优先级，取值范围为0～7，N/A表示无效值QoS local ID 路由的Qos-Local-ID属性，取值范围为1～4095，N/A表示无效值流量索引值，取值范围为1～64，N/A表示无效值Traffic index

##### 1.1.37 display bgp network

display bgp network 命令用来显示通过 network 命令发布的路由信息和通过 network命令配置的 Short-cut 路由信息。
short-cut【命令】
display bgp [ instance instance-name ] network { ipv4 | ipv6 } [ multicast | [ unicast ] [ vpn-instance vpn-instance-name ] ]

【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
instance-name：显示指定 BGP 实例的信息。instance-name 表示 BGP 实例的名instance称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示 default 实例的信息。
ipv4：显示 地址族的信息。
IPv4 ipv6：显示 地址族的信息。
IPv6 multicast：显示 组播地址族的信息。
BGP unicast：显示 单播地址族的信息。
BGP vpn-instance-name：显示指定 VPN 实例的信息。vpn-instance-name 表vpn-instance示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果不指定本参数，则显示公网的信息。
【使用指导】
如果没有指定 和 参数，则缺省为 unicast。
unicast multicast【举例】
显示 单播地址族下所有通过 命令通告的路由信息和通过\# BGP IPv4 network network short-cut 命令配置的 Short-cut 路由信息。
<Sysname> display bgp network ipv4 BGP local router ID: 192.168.1.135 Local AS number: 100 Network Mask Route-policy Short-cut
20.1.1.0 255.255.255.0 No
40.1.1.0 255.255.255.0 abc No
30.1.1.0 255.255.255.0 Yes \# 显示 BGP IPv6 单播地址族下所有通过 network 命令通告的路由信息和通过 network short-cut 命令配置的 Short-cut 路由信息。
<Sysname> display bgp network ipv6 BGP local router ID: 192.168.1.135 Local AS number: 100 Network PrefixLen Route-policy Short-cut 1:: 24 No 2:: 24 No 3:: 64 policy1 No 2:: 24 Yes

表1-8 display bgp network 命令显示信息描述表字段 描述BGP local router ID 本地的路由器ID本地的AS号Local AS number Network 通过network命令发布的路由或Short-cut路由的目的网络地址Mask 目的网络地址的掩码目的网络地址的前缀长度PrefixLen Route-policy 为该路由应用的路由策略Short-cut 该路由是否为Short-cut路由，取值包括Yes和No

##### 1.1.38 display bgp non-stop-routing status

命令用来显示 的运行状态。
display bgp non-stop-routing status BGP NSR【命令】
display bgp [ instance instance-name ] non-stop-routing status【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
instance-name：显示指定 BGP 实例的信息。instance-name 表示 BGP 实例的名instance称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示 default 实例的信息。
【举例】
\# 显示 BGP NSR 的运行状态。
<Sysname> display bgp non-stop-routing status BGP NSR status: Not ready Location of preferred standby process: - TCP NSR status: Not ready表1-9 display bgp non-stop-routing status 命令显示信息描述表字段 描述BGP NSR的备份状态，取值包括：
• Ready：BGP NSR 已经将 BGP 邻居和路由信息从主进程备份到备进程。
BGP NSR status若在该状态下进行主备进程倒换，则现有路由保持不变，不会影响数据转发
• Not ready：BGP NSR 正在将 BGP 邻居和路由信息从主进程备份到备进

字段 描述程。若在该状态下进行主备进程倒换，则可能需要重新建立 BGP 会话，导致数据转发中断
• Not configured：BGP NSR 功能未开启优选备进程所在成员设备的编号Location of preferred standby process显示为“-”表示不存在备进程TCP NSR的备份状态，取值包括：
TCP NSR status • Ready：TCP 已经将 连接等信息从主进程备份到备进程NSR TCP
• Not ready：TCP NSR 正在将 TCP 连接等信息从主进程备份到备进程

##### 1.1.39 display bgp paths

命令用来显示 的路由属性信息。
display bgp paths BGP【命令】
display bgp [ instance instance-name ] paths [ as-regular-expression ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
instance-name：显示指定 BGP 实例的信息。instance-name 表示 BGP 实例的名instance称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示 实例的信息。
default as-regular-expression：显示 路径与指定正则表达式匹配的 路由属性的信息。
AS BGP as-regular-expression 表示正则表达式，为 1～256 个字符的字符串。如果不指定本参数，则显示所有的 BGP 路由属性信息。
【举例】
\# 显示所有的 BGP 路由属性信息。
<Sysname> display bgp paths RefCount MED Path/Origin 3 0 ?
2 0 100i 3 0 100i 1 0 ?
1 0 ?
1 0 ?

表1-10 display bgp paths 命令显示信息描述表字段 描述RefCount 使用该路由属性的BGP路由条数MED属性值MED路由的AS路径（AS_PATH）属性和路由信息的来源（ORIGIN）属性，其中：
• AS_PATH 属性记录了此路由经过的所有 AS，可以避免路由环路的出现
• ORIGIN 属性标记了此路由如何成为 BGP 路由，取值包括：
i：表示路由产生于本 内。通过 命令发布路由的路由信息来源AS network (cid:123)
Path/Origin为 IGP e：表示路由是通过 EGP（Exterior Gateway Protocol，外部网关协议）学(cid:123)
到的?：表示路由的来源无法确定。从 IGP 协议引入路由的路由信息来源为(cid:123)
incomplete

##### 1.1.40 display bgp peer

命令用来显示 对等体或对等体组的状态和统计信息。
display bgp peer BGP【命令】
display bgp [ instance instance-name ] peer ipv4 [ multicast | rtfilter | [ unicast ] [ vpn-instance vpn-instance-name ] ] [ ipv4-address mask-length | { ipv4-address | group-name group-name } log-info | [ ipv4-address ] verbose ] display bgp [ instance instance-name ] peer ipv6 [ multicast | [ unicast ] [ vpn-instance vpn-instance-name ] ] [ ipv6-address prefix-length | { ipv6-address | group-name group-name } log-info | [ ipv6-address ] verbose ] display bgp [ instance instance-name ] peer { ipv4 | ipv6 } [ unicast ] vpn-instance-all [ verbose ] display bgp [ instance instance-name ] peer link-state [ ipv4-address mask-length | ipv6-address prefix-length | { ipv4-address | ipv6-address | group-name group-name } log-info | [ ipv4-address | ipv6-address ] verbose ] display bgp [ instance instance-name ] peer l2vpn evpn [ ipv4-address mask-length | { ipv4-address | group-name group-name } log-info | [ ipv4-address ] verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator

【参数】
instance instance-name：显示指定 BGP 实例的信息。instance-name 表示 BGP 实例的名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示 default 实例的信息。
ipv4：显示 BGP IPv4 对等体或对等体组的信息。
ipv6：显示 BGP IPv6 对等体或对等体组的信息。
link-state：显示 BGP LS 对等体或对等体组的信息。
l2vpn：显示 BGP L2VPN 对等体或对等体组的信息。
evpn：显示 BGP EVPN 对等体或对等体组的信息。
multicast：显示 BGP 组播对等体或对等体组的信息。
rtfilter：显示 BGP IPv4 RT-Filter 对等体或对等体组的信息。
unicast：显示 BGP 单播对等体或对等体组的信息。
vpn-instance-all：显示所有 VPN 实例的 BGP 对等体信息。
vpn-instance vpn-instance-name：显示指定 VPN 实例的 BGP 对等体或对等体组的信息。
vpn-instance-name 表示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果不指定本参数，则显示公网 BGP 对等体或对等体组的信息。
mask-length：显示指定网段内的动态对等体的信息。ipv4-address 为对等ipv4-address体的 地址；mask-length 为网络掩码，取值范围为 0～32。
IPv4 ipv4-address：显示指定对等体的信息。ipv4-address 为对等体的 地址。
IPv4 prefix-length：显示指定网段内的动态对等体的信息。ipv6-address 为对ipv6-address等体的 IPv6 地址；prefix-length 为前缀长度，取值范围为 0～128。
ipv6-address：显示指定对等体的信息。ipv6-address 为对等体的 IPv6 地址。
group-name：显示指定对等体组内对等体的信息。group-name 为对等体组的名group-name称，为 1～47 个字符的字符串，区分大小写。
log-info：显示指定对等体或对等体组的日志信息。
verbose：显示对等体的详细信息。如果不指定本参数，则显示对等体的简要信息。
【使用指导】
如果没有指定任何参数，则显示指定地址族所有 BGP 对等体的简要信息。
如果没有指定 unicast 、 multicast 参数，则缺省为 unicast 。
【举例】
\# 显示所有 BGP IPv4 单播对等体的简要信息。
<Sysname> display bgp peer ipv4 BGP local router ID: 192.168.100.1 Local AS number: 100 Total number of peers: 1 Peers in established state: 1
* - Dynamically created peer Peer AS MsgRcvd MsgSent OutQ PrefRcv Up/Down State
10.2.1.2 200 13 16 0 0 00:10:34 Established

\# 查看所有 VPN 实例中 BGP IPv4 单播对等体的简要信息。
<Sysname> display bgp peer ipv4 vpn-instance-all Local AS number: 100
* - Dynamically created peer VPN instance: 1 BGP local router ID: 111.1.1.1 Total number of peers: 2 Peers in established state: 0 Peer AS MsgRcvd MsgSent OutQ PrefRcv Up/Down State
111.1.1.1 100 0 0 0 0 00:00:34 Connect
111.1.1.2 100 0 0 0 0 00:00:34 Connect VPN instance: 2 BGP local router ID: 112.1.1.1 Total number of peers: 2 Peers in established state: 0 Peer AS MsgRcvd MsgSent OutQ PrefRcv Up/Down State
112.1.1.1 100 0 0 0 0 00:00:06 Idle
112.1.1.2 100 0 0 0 0 00:00:06 Idle表1-11 命令显示信息描述表display bgp peer字段 描述BGP local router ID 本地的路由器ID Local AS number 本地的AS号对等体的总数Total number of peers Peers in established state 处于Established状态的对等体的总数
* - Dynamically created peer 如果对等体的地址前存在“*”，则表示该对等体为动态创建的对等体对等体所属的MPLS L3VPN的VPN实例名称VPN instance Peer 对等体的IPv4地址或IPv6地址AS 对等体所在的AS号MsgRcvd 从对等体接收的消息数目向对等体发送的消息数目MsgSent OutQ 等待发往对等体的消息数目对于IPv4、IPv6地址族，表示从对等体接收到的加入到本地BGP路由表中的PrefRcv前缀数目BGP会话处于当前状态的时长Up/Down State 本地路由器与该对等体之间BGP会话的当前状态

\# 显示 1.1.1.0/24 网段范围内的动态对等体信息。
<Sysname> display bgp peer ipv4 1.1.1.0 24 Type: EBGP link Dynamic address range: 1.1.1.0 24 Configured: Active Hold Time: 3 sec Keepalive Time: 1 sec Address family IPv4 Unicast: Configured Maximum allowed prefix number: 100 Threshold: 75% Minimum time between advertisements is 100 seconds Optional capabilities:
Multi-protocol extended capability has been enabled Route refresh capability has been enabled Nexthop self has been configured Keep-all-routes has been configured Send community has been configured Send extend community has been configured Default route originating has been configured Multi-hop ebgp has been enabled Peer preferred value: 100 BFD: Enabled Site-of-Origin: 1:1 Routing policy configured:
No import as-path-acl list Export as-path-acl list is: 22 No import prefix list Export prefix list is: p1 No import route policy Export route policy is: p1 No import filter-policy No export filter-policy Dynamic peers:
1.1.1.3 \# 显示 1::/64 网段范围内的动态对等体信息。
<Sysname> display bgp peer ipv6 1:: 64 Type: IBGP link Dynamic address range: 1:: 64 Configured: Active Hold Time: 180 sec Keepalive Time: 60 sec Address family IPv6 Unicast: Configured Maximum allowed prefix number: 4294967295 Threshold: 75% Minimum time between advertisements is 15 seconds Optional capabilities:
Multi-protocol extended capability has been enabled

Route refresh capability has been enabled Send community has been configured Peer preferred value: 0 Site-of-Origin: Not specified Routing policy configured:
No routing policy is configured Dynamic peers:
1::1表1-12 display bgp peer 命令显示信息描述表（动态对等体）
字段 描述本地路由器与该动态对等体之间的BGP连接类型，取值包括：
Type • IBGP link：IBGP 连接
• link：EBGP 连接EBGP Dynamic address range 动态对等体的地址范围本地配置的定时器值，包括会话保持时间间隔（Active Hold Time）和存Configured活时间间隔（Keepalive Time），单位为秒IPv4单播地址族能力Address family IPv4 Unicast Address family link-state LS地址族能力Address family IPv6 Unicast IPv6单播地址族能力Address family IPv4 Multicast IPv4组播地址族能力IPv6组播地址族能力Address family IPv6 Multicast Maximum allowed prefix number 允许从对等体学习的最大路由数路由器产生日志信息的阈值，即从对等体接收的路由数量与允许的最大Threshold路由数的百分比达到此值时，路由器将产生日志信息Minimum time between路由发布最小时间间隔，单位为秒advertisements Optional capabilities 本端支持的可选扩展能力Multi-protocol extended capability has本端支持BGP多协议扩展能力been enabled Route refresh capability has been本端支持BGP路由刷新能力enabled Nexthop self has been configured 向对等体发布路由时，将下一跳属性修改为自身的地址保存所有来自指定对等体的原始路由更新信息，不管这些路由是否通过Keep-all-routes has been configured了路由策略的过滤Send community has been configured 向对等体发布团体属性Send extend community has been向对等体发布扩展团体属性configured Default route originating has been向对等体发送缺省路由configured

字段 描述Multi-hop ebgp has been enabled 允许本地路由器同非直连网络上的邻居建立EBGP会话Peer Preferred Value 为来自对等体的路由配置的首选值是否配置通过BFD检测本地路由器和指定BGP对等体之间的链路BFD为BGP IPv6对等体应用的IPsec安全框架名IPsec profile name只有显示IPv6单播和IPv6组播地址族信息时，显示本字段Site-of-Origin 为对等体指定的SoO属性值为对等体指定的路由策略Routing policy configured如果未指定路由策略，则显示为No routing policy is configured Dynamic peers 动态对等体中包括的对等体的地址\# 显示 BGP IPv4 单播对等体 10.2.1.2 的详细信息。
<Sysname> display bgp peer ipv4 10.2.1.2 verbose Peer: 10.2.1.2 Local: 192.168.100.1 Type: EBGP link BGP version 4, remote router ID 192.168.100.2 BGP current state: Established, Up for 00h11m10s BGP current event: RecvKeepalive BGP last state: OpenConfirm Port: Local - 179 Remote - 60672 Configured: Active Hold Time: 180 sec Keepalive Time: 60 sec Received : Active Hold Time: 180 sec Negotiated: Active Hold Time: 180 sec Keepalive Time: 60 sec Peer optional capabilities:
Peer support BGP multi-protocol extended Peer support BGP route refresh capability Peer support BGP route AS4 capability Address family IPv4 Unicast: advertised and received InQ updates: 0, OutQ updates: 0 NLRI statistics:
Rcvd: UnReach NLRI 0, Reach NLRI 0 Sent: UnReach NLRI 0, Reach NLRI 0 Message statistics:
Msg type Last rcvd time/ Current rcvd count/ History rcvd count/ Last sent time Current sent count History sent count Open 10:38:50-2013.7.23 1 1 10:38:50-2013.7.23 1 1 Update 10:38:51-2013.7.23 1 1 10:38:51-2013.7.23 1 1 Notification - 0 0
- 0 0

Keepalive 10:38:50-2013.7.23 1 1 10:38:50-2013.7.23 1 1 RouteRefresh - 0 0
- 0 0 Total - 3 3
- 3 3 Maximum allowed prefix number: 4294967295 Threshold: 75% Minimum time between advertisements is 30 seconds Optional capabilities:
Multi-protocol extended capability has been enabled Route refresh capability has been enabled Peer Preferred Value: 0 GTSM has been enabled, and the maximum number of hops is 10 BFD: Enabled Site-of-Origin: Not specified Routing policy configured:
No routing policy is configured \# 显示 BGP IPv6 单播对等体 1::2 的详细信息。
<Sysname> display bgp peer ipv6 1::2 verbose Peer: 1::2 Local: 192.168.1.136 Type: EBGP link BGP version 4, remote router ID 192.168.1.135 BGP current state: Established, Up for 00h05m48s BGP current event: RecvKeepalive BGP last state: OpenConfirm Port: Local - 13184 Remote - 179 Configured: Active Hold Time: 180 sec Keepalive Time: 60 sec Received : Active Hold Time: 180 sec Negotiated: Active Hold Time: 180 sec Keepalive Time: 60 sec Peer optional capabilities:
Peer support BGP multi-protocol extended Peer support BGP route refresh capability Peer support BGP route AS4 capability Address family IPv6 Unicast: advertised and received InQ updates: 0, OutQ updates: 0 NLRI statistics:
Rcvd: UnReach NLRI 0, Reach NLRI 0 Sent: UnReach NLRI 0, Reach NLRI 3 Message statistics:
Msg type Last rcvd time/ Current rcvd count/ History rcvd count/ Last sent time Current sent count History sent count Open 18:59:15-2013.4.24 1 1

18:59:15-2013.4.24 1 2 Update - 0 0 18:59:16-2013.4.24 1 1 Notification - 0 0 18:59:15-2013.4.24 0 1 Keepalive 18:59:15-2013.4.24 1 1 18:59:15-2013.4.24 1 1 RouteRefresh - 0 0
- 0 0 Total - 2 2
- 3 5 Maximum allowed prefix number: 4294967295 Threshold: 75% Minimum time between advertisements is 30 seconds Optional capabilities:
Multi-protocol extended capability has been enabled Route refresh capability has been enabled Peer preferred value: 0 GTSM has been enabled, and the maximum number of hops is 10 BFD: Enabled IPsec profile name: profile001 Site-of-Origin: Not specified Routing policy configured:
No routing policy is configured表1-13 display bgp peer verbose 命令显示信息描述表字段 描述Peer 对等体的IPv4地址或IPv6地址本地的路由器ID Local VPN instance 对等体所属的MPLS L3VPN的VPN实例名称本地路由器与该对等体之间的BGP连接类型，取值包括：
• ： 连接Type IBGP link IBGP
• EBGP link：EBGP 连接BGP version 协议版本号对等体的路由器ID remote router ID BGP current state 本地路由器与该对等体之间BGP会话的当前状态Up for BGP会话建立的持续时间本地路由器与该对等体之间BGP会话的当前事件BGP current event BGP last state BGP会话的前一个状态Port 建立TCP连接时本地（Local）和对等体（Remote）使用的端口号Configured 本地配置的定时器值，包括会话保持时间间隔（Active Hold Time）和存

字段 描述活时间间隔（Keepalive Time），单位为秒收到的定时器值，即对等体上配置的定时器值，包括会话保持时间间隔Received（Active Hold Time），单位为秒协商后的定时器值，包括会话保持时间间隔（Active Hold Time）和存活Negotiated时间间隔（Keepalive Time），单位为秒Peer optional capabilities 对等体支持的可选扩展能力Peer support BGP multi-protocol对等体支持BGP多协议扩展能力extended Peer support BGP route refresh对等体支持BGP路由刷新能力capability Peer support BGP route AS4对等体支持四字节AS号能力capability IPv4单播地址族能力，可以接收（received）和发送（advertised）该地Address family IPv4 Unicast址族的路由LS地址族能力，可以接收（received）和发送（advertised）该地址族Address family LS的路由IPv6单播地址族能力，可以接收（received）和发送（advertised）该地Address family IPv6 Unicast址族的路由IPv4组播地址族能力，可以接收（received）和发送（advertised）该地Address family IPv4 Multicast址族的路由IPv6组播地址族能力，可以接收（received）和发送（advertised）该地Address family IPv6 Multicast址族的路由InQ updates 待处理的接收到的Update消息数目等待发送给对等体的Update消息数目OutQ updates NLRI统计信息，包括建立BGP会话后，从对等体累计接收到的可达路由NLRI statistics 数目和不可达路由数目，向对等体累计发送的可达路由数目和不可达路由数目Message statistics BGP消息统计信息Msg type BGP消息类型最近一次从对等体接收到BGP消息的时间/最近一次向对等体发送BGP Last rcvd time/Last sent time消息的时间在当前BGP会话上，从对等体接收到的BGP消息数目/在当前BGP会话Current rcvd count/Current sent count上，向对等体发送的BGP消息数目配置BGP对等体以来，累计从对等体接收到的BGP消息数目/累计向对等History rcvd count/History sent count体发送的BGP消息数目Total 接收/发送所有类型消息的总数Maximum allowed prefix number 允许从对等体学习的最大路由数路由器产生日志信息的阈值，即从对等体接收的路由数量与允许的最大Threshold路由数的百分比达到此值时，路由器将产生日志信息路由发布最小时间间隔，单位为秒Minimum time between

字段 描述advertisements Optional capabilities 本端支持的可选扩展能力Multi-protocol extended capability has本端支持BGP多协议扩展能力been enabled Route refresh capability has been本端支持BGP路由刷新能力enabled Peer Preferred Value 为来自对等体的路由配置的首选值GTSM has been enabled 本端支持BGP报文的GTSM安全检测功能the maximum number of hops 指定对等体到达本地设备的最大跳数BFD 是否配置通过BFD检测本地路由器和指定BGP对等体之间的链路为BGP IPv6对等体应用的IPsec安全框架名IPsec profile name只有显示IPv6单播和IPv6组播地址族信息时，显示本字段Site-of-Origin 为对等体指定的SoO属性值为对等体指定的路由策略Routing policy configured如果未指定路由策略，则显示为No routing policy is configured显示 单播对等体 的日志信息。
\# BGP IPv4 1.1.1.1 <Sysname> display bgp peer ipv4 1.1.1.1 log-info Peer : 1.1.1.1 Date Time State Notification Error/SubError 06-Feb-2013 22:54:42 Down Send notification with error 6/4 Cease/Administrative Reset <administrative reset>表1-14 display bgp peer log-info 命令显示信息描述表字段 描述Peer 对等体的IPv4地址或IPv6地址Date 发送或接收到Notification消息的日期发送或接收到Notification消息的时间Time本地与对等体之间BGP会话的状态，取值包括：
State • Up：表示 BGP 会话处于 Established 状态
• Down：表示 会话断开BGP Notification消息中的错误码，表明了BGP会话处于Down状态的原因Notification Error表示Notification消息差错码，指定错误类型；SubError表示Notification消息差错子码，Error/SubError指定错误类型的详细信息如果是本端发送Notification消息通知对等体邻居异常断开，则会显示邻居断开的详细原因

字段 描述（详见表1-15）
表1-15 邻居断开的详细原因列表差错码/差错子码 邻居断开的详细原因connection not synchronized：连接不同步，目前实现为收到的报文的报文头前16字节不全1/1为F 1/2 bad message length：报文长度无效type：报文的类型无效1/3 bad message
• the withdrawn length is too large：撤销信息长度过长
• the attribute length is too large：属性长度过长
• one attribute appears more than once：同一个属性在一个 Update 消息中出现了多次3/1
• the attribute length is too small ：属性长度字段不足 2 字节
• exntended length field is less than two octets：属性长度为可扩展长度，但长度字段不足 2 字节
• the length field is less than one octet：属性长度为正常长度，但长度字段不足 1 字节3/2 unrecognized well-known attribute：不支持的公认属性attribute-type attribute missed：attribute-type类型的属性丢失，attribute-type取值包括：
• ORIGIN 3/3 •AS_PATH
• LOCAL_PREF
• NEXT_HOP 3/4 attribute flags error：属性标记错误
• attribute-type attribute length error：attribute-type 类型的属性长度错误，attribute-type 取值包括：
AS_PATH (cid:123)
AS4_PATH (cid:123)
CLUSTER_LIST (cid:123)
AGGREGATOR (cid:123)
AS4_AGGREGATOR (cid:123)
ORIGIN (cid:123)
NEXT_HOP 3/5 (cid:123)
MED (cid:123)
LOCAL_PREF (cid:123)
ATOMIC_AGGREGATE (cid:123)
ORIGINATOR_ID (cid:123)
MP_REACH_NLRI (cid:123)
COMMUNITIES (cid:123)
extended communities (cid:123)
• attribute length exceeds：属性长度越界3/6 invalid ORIGIN attribute：ORIGIN属性无效

差错码/差错子码 邻居断开的详细原因3/8 invalid NEXT_HOP attribute：下一跳属性无效
• invalid nexthop length in MP_REACH_NLRI (address-family)：address-family 地址族MP_REACH_NLRI 属性的 Nexthop 长度错误，address-family 的取值包括：
4u：表示 IPv4 单播地址族(cid:123)
6u：表示 单播地址族IPv6 (cid:123)
• the length of MP_UNREACH_NLRI is too small：MP_UNREACH_NLRI 的长度小于 3 3/9字节
• exceeds：MP_REACH_NLRI 或the MP NLRI attribute length MP_UNREACH_NLRI属性长度越界
• erroneous MP NLRI attribute end position：可达或不可达前缀结束位置与报文属性结束位置不同field：网络字段无效3/10 invalid network 3/11 malformed AS_PATH：AS路径形式不对
• hold timer expiration caused by local device：本地导致 holdtimer 超时4/0
• hold timer expiration caused by peer device：对端导致 holdtimer 超时
• connection retry timer expires：ConnectRetry 定时器超时
• received：收到了 事件TCP_CR_Acked event TCP_CR_Acked 5/0
• TCP_Connection_Confirmed event received：收到了TCP_Connection_Confirmed事件5/3 open message received：收到open消息
• manualstop event received：收到 manualstop 事件6/0 • physical interface configuration changed：物理配置改变，比如接口变化
• session down event received from BFD：收到 BFD 会话 down 事件
• maximum number of prefixes reached：前缀数超过 peer route-limit 所配置的数目
• maximum number of address-family prefixes reached：address-family 地址族的前缀6/1数超过 所配置的数目，address-family 的取值包括：
peer route-limit unicast：表示 单播地址族IPv4 IPv4 (cid:123)
IPv6 unicast：表示 IPv6 单播地址族(cid:123)
6/2 configuration of peer ignore changed：配置peer ignore命令
• deleted：地址族被删除address family 6/3
• peer disabled：关闭对等体6/4 administrative reset：执行reset bgp命令或者配置改变导致BGP会话重启rejected：连接被拒绝6/5 connection 6/6 other configuration change：其他配置变化
• connection collision resolution：连接冲突6/7
• two connections exist and one uses MD5：存在两个连接，且其中一个配置了 MD5 认证

差错码/差错子码 邻居断开的详细原因
• attribute：解析属性时内存不够no memory to process the
• no memory for the route：生成路由信息时，获取不到内存
• NLRI：封装 时申请不到内存no memory to generate unreachable unreachable NLRI
• no memory to generate a message：封装报文时申请不到内存
•6/8 can’t get the VPN RD：解析前缀时获取不到 RD
• can’t get the VPN routing table：解析前缀时获取不到 VPN 路由表
• can’t get the attributes：解析前缀时获取不到属性
• entered severe memory state：进入二级门限告警
• entered critical memory state：进入三级门限告警

##### 1.1.41 display bgp peer received prefix-list

命令用来显示邻居收到的 ORF 消息中的前缀信display bgp peer received prefix-list息。
【命令】
display bgp [ instance instance-name ] peer ipv4 [ multicast | [ unicast ] [ vpn-instance vpn-instance-name ] ] ipv4-address received prefix-list display bgp [ instance instance-name ] peer ipv6 [ multicast | [ unicast ] [ vpn-instance vpn-instance-name ] ] ipv6-address received prefix-list【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
instance instance-name：显示指定 BGP 实例的信息。instance-name 表示 BGP 实例的名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示 default 实例的信息。
ipv4：显示 BGP IPv4 对等体的信息。
ipv6：显示 BGP IPv6 对等体的信息。
multicast：显示 BGP 组播对等体的信息。
unicast：显示 BGP 单播对等体的信息。
vpn-instance vpn-instance-name ： 显 示 指 定 VPN 实 例 的 BGP 对 等 体 的 信 息 。
表示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大vpn-instance-name小写。如果不指定本参数，则显示公网 对等体的信息。
BGP ipv4-address：显示指定对等体的信息。ipv4-address 为对等体的 地址。
IPv4 ipv6-address：显示指定对等体的信息。ipv6-address 为对等体的 地址。
IPv6

【举例】
\# 显示对等体 10.110.25.20 的收到的 ORF 消息中的前缀信息。
<Sysname> display bgp peer ipv4 10.110.25.20 received prefix-list ORF prefix list entries: 2 index: 10 prefix 1.1.1.0/24 ge 26 le 32 index: 20 prefix 2.1.1.0/24 ge 26 le 32表1-16 display bgp peer received prefix-list 命令显示信息描述表字段 描述ORF prefix list entries ORF地址前缀条目数index 地址前缀索引号prefix 地址前缀信息greater-equal，表示掩码长度大于或者等于ge le less-equal，表示掩码长度小于或者等于

##### 1.1.42 display bgp routing-table dampened

命令用来显示衰减的 路由信息。
display bgp routing-table dampened BGP【命令】
display bgp [ instance instance-name ] routing-table dampened { ipv4 | ipv6 } [ multicast | [ unicast ] [ vpn-instance vpn-instance-name ] ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
instance instance-name：显示指定 BGP 实例的信息。instance-name 表示 BGP 实例的名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示 default 实例的信息。
ipv4：显示衰减的 BGP IPv4 路由信息。
ipv6：显示衰减的 BGP IPv6 路由信息。
multicast：显示衰减的 BGP 组播路由信息。
unicast：显示衰减的 BGP 单播路由信息。
vpn-instance vpn-instance-name ： 显 示 指 定 VPN 实 例 内 衰 减 的 BGP 路 由 信 息 。
vpn-instance-name 表示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果不指定本参数，则显示公网衰减的 BGP 路由信息。

【使用指导】
如果没有指定 unicast 和 multicast 参数，则缺省为 unicast。
【举例】
\# 显示衰减的 BGP IPv4 单播路由信息。
<Sysname> display bgp routing-table dampened ipv4 Total number of routes: 1 BGP local router ID is 192.168.1.135 Status codes: * - valid, > - best, d - dampened, h - history s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network From Reuse Path/Ogn de 20.1.1.0/24 10.1.1.2 00:56:27 100i \# 显示衰减的 BGP IPv6 单播路由信息。
<Sysname> display bgp routing-table dampened ipv6 Total number of routes: 2 BGP local router ID is 192.168.1.135 Status codes: * - valid, > - best, d - dampened, h - history s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete de Network : 2:: PrefixLen : 64 From : 10.1.1.1 Reuse : 00:39:49 Path/Ogn: 100i de Network : 2:: PrefixLen : 64 From : 1::1 Reuse : 00:39:49 Path/Ogn: 100i表1-17 display bgp routing-table dampened 命令显示信息描述表字段 描述Total number of routes 衰减的路由总数BGP local router ID 本地的路由器ID路由状态代码：
• * – valid：合法路由Status codes
• > – best：优选最佳路由
• d - dampened：振荡抑制路由

字段 描述
• h – history：历史路由
•s – suppressed：聚合抑制路由
• S – stale：过期路由
• i – internal：内部路由
• e – external：外部路由
• a – additional-path：Add-Path 优选路由路由信息的来源，取值包括：
• i – IGP：表示路由产生于本 AS 内。通过 network 命令发布路由的路由信息来源为 IGP Origin • EGP：表示路由是通过 EGP（Exterior Protocol，外部网关协议）
e – Gateway学到的
• ? – incomplete：表示路由的来源无法确定。从 IGP 协议引入路由的路由信息来源为 incomplete Network 目的网络地址PrefixLen 目的网络地址的前缀长度From 发布该路由的BGP对等体的IP地址Reuse 路由恢复可用的时间，即还需要等待多长时间该路由将由不可用状态转为可用状态路由的AS路径（AS_PATH）属性和路由信息的来源（ORIGIN）属性，其中：
Path/Ogn • AS_PATH 属性记录了此路由经过的所有 AS，可以避免路由环路的出现
•ORIGIN 属性标记了此路由如何成为 BGP 路由【相关命令】
• dampening
• reset bgp dampening

##### 1.1.43 display bgp routing-table flap-info

命令用来显示 BGP 路由的振荡统计信息。
display bgp routing-table flap-info【命令】
display bgp [ instance instance-name ] routing-table flap-info ipv4 [ multicast | [ unicast ] [ vpn-instance vpn-instance-name ] ] [ ipv4-address [ { mask-length | mask } [ longest-match ] ] | as-path-acl as-path-acl-number ] display bgp [ instance instance-name ] routing-table flap-info ipv6 [ multicast | [ unicast ] [ vpn-instance vpn-instance-name ] ] [ ipv6-address prefix-length | as-path-acl as-path-acl-number ]【视图】
任意视图

【缺省用户角色】
network-admin network-operator【参数】
instance-name：显示指定 BGP 实例的信息。instance-name 表示 BGP 实例的名instance称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示 实例的信息。
default ipv4：显示 BGP IPv4 路由的振荡统计信息。
ipv6：显示 BGP IPv6 路由的振荡统计信息。
multicast：显示 BGP 组播路由的振荡统计信息。
unicast：显示 BGP 单播路由的振荡统计信息。
vpn-instance-name：显示指定 VPN 实例内 BGP 路由的振荡统计信息。
vpn-instance表示 的 实例名称，为 1～31 个字符的字符串，区分大vpn-instance-name MPLS L3VPN VPN小写。如果不指定本参数，则显示公网 BGP 路由的振荡统计信息。
ipv4-address：显示匹配指定目的网络地址的 BGP IPv4 单播路由或组播路由的振荡统计信息。
mask-length：目的网络地址的掩码长度，取值范围为 0～32。
mask：目的网络地址的掩码，点分十进制格式。
longest-match：指定根据如下方法判断显示哪条 单播路由或组播路由的振荡统计信BGP IPv4息：
(1) 将用户输入的网络地址和路由的掩码进行与操作；
(2) 计算结果与路由的网段地址相同，且掩码小于等于用户输入子网掩码的路由中，子网掩码最长的路由将被显示出来。
ipv6-address prefix-length：显示匹配指定目的网络地址及前缀长度的 BGP IPv6 单播路由或组播路由的振荡统计信息。prefix-length 为目的网络地址的前缀长度，取值范围为 0～128。
as-path-acl-number：显示匹配指定 AS 路径过滤列表的 BGP 路由的振荡统计as-path-acl信息。as-path-acl-number 为 路径过滤列表号，取值范围为 1～256。
AS【使用指导】
执行 display bgp routing-table flap-info ipv4 命令时：
• 如果只指定了 ipv4-address 参数，则将指定的网络地址和路由的掩码进行与操作，若计算结果与路由的网段地址相同，则显示该 BGP IPv4 单播路由或组播路由的振荡统计信息。
• 如果指定了 ipv4-address mask 或 ipv4-address mask-length 参数，没有指定参数，则显示与指定目的网络 IPv4 地址和网络掩码（或掩码长度）精确匹longest-match配的 单播路由或组播路由的振荡统计信息。
BGP IPv4如果没有指定 和 参数，则缺省为 unicast。
unicast multicast【举例】
\# 显示所有 BGP IPv4 单播路由的振荡统计信息。
<Sysname> display bgp routing-table flap-info ipv4 Total number of routes: 1

BGP local router ID is 192.168.1.135 Status codes: * - valid, > - best, d - dampened, h - history s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network From Flaps Duration Reuse Path/Ogn de 20.1.1.0/24 10.1.1.2 1 00:02:36 00:53:58 100i \# 显示所有 BGP IPv6 单播路由的振荡统计信息。
<Sysname> display bgp routing-table flap-info ipv6 Total number of routes: 2 BGP local router ID is 192.168.1.135 Status codes: * - valid, > - best, d - dampened, h - history s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete de Network : 2:: PrefixLen : 64 From : 10.1.1.1 Flaps : 5 Duration: 00:03:25 Reuse : 00:39:28 Path/Ogn: 100i de Network : 2:: PrefixLen : 64 From : 1::1 Flaps : 5 Duration: 00:03:25 Reuse : 00:39:28 Path/Ogn: 100i表1-18 命令显示信息描述表display bgp routing-table flap-info字段 描述Total number of routes 振荡路由的总数BGP local router ID 本地的路由器ID路由状态代码：
• * – valid：合法路由
• best：优选最佳路由> –
• d - dampened：振荡抑制路由
•h – history：历史路由Status codes
• s – suppressed：聚合抑制路由
• S – stale：过期路由
• i – internal ：内部路由
• e – external：外部路由
• a – additional-path：Add-Path 优选路由Origin 路由信息的来源，取值包括：

字段 描述
• i – IGP：表示路由产生于本 AS 内。通过 network 命令发布路由的路由信息来源为 IGP
• EGP：表示路由是通过 EGP（Exterior Protocol，外部网关协议）
e – Gateway学到的
• ? – incomplete：表示路由的来源无法确定。从 IGP 协议引入路由的路由信息来源为 incomplete目的网络地址Network PrefixLen 目的网络地址的前缀长度From 发布该路由的BGP对等体的IP地址路由振荡的次数，即路由从可达状态变为不可达状态，及可达路由的属性发生变化Flaps的次数Duration 路由发生振荡的持续时间Reuse 路由恢复可用的时间，即还需要等待多长时间该路由将由不可用状态转为可用状态路由的AS路径（AS_PATH）属性和路由信息的来源（ORIGIN）属性，其中：
Path/Ogn • AS_PATH 属性记录了此路由经过的所有 AS，可以避免路由环路的出现
• ORIGIN 属性标记了此路由如何成为 BGP 路由【相关命令】
• dampening
• reset bgp flap-info

##### 1.1.44 display bgp routing-table ipv4 multicast

命令用来显示 组播路由信息。
display bgp routing-table ipv4 multicast BGP IPv4【命令】
display bgp [ instance instance-name ] routing-table ipv4 multicast [ ipv4-address [ { mask-length | mask } [ longest-match ] ] | ipv4-address [ mask-length | mask ] advertise-info | as-path-acl as-path-acl-number | community-list { { basic-community-list-number | comm-list-name } [ whole-match ] | adv-community-list-number } | peer ipv4-address { advertised-routes | received-routes } [ ipv4-address [ mask-length | mask ] | statistics ] | statistics ]【视图】
任意视图【缺省用户角色】
network-admin network-operator

【参数】
instance instance-name：显示指定 BGP 实例的信息。instance-name 表示 BGP 实例的名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示 default 实例的信息。
ipv4-address：目的网络的 IPv4 地址。
mask-length：网络掩码长度，取值范围为 0～32。
mask：网络掩码，点分十进制格式。
longest-match：指定根据如下方法判断显示哪条 BGP IPv4 组播路由信息：
(1) 将用户输入的网络地址和路由的掩码进行与操作；
(2) 计算结果与路由的网段地址相同，且掩码小于等于用户输入子网掩码的路由中，子网掩码最长的路由将被显示出来。
advertise-info：显示 BGP IPv4 组播路由的通告信息。
as-path-acl-number：显示匹配指定 AS 路径过滤列表的 BGP IPv4 组播路由as-path-acl信息。as-path-acl-number 为 路径过滤列表号，取值范围为 1～256。
AS community-list：显示匹配指定 BGP 团体列表的 BGP IPv4 组播路由信息。
basic-community-list-number：基本团体列表号，取值范围为 1～99。
comm-list-name：团体属性列表名，为 1～63 个字符的字符串，区分大小写。
whole-match：精确匹配。如果指定了本参数，则只有路由的团体属性列表与指定的团体属性列表完全相同时，才显示该路由的信息；如果未指定本参数，则只要路由的团体属性列表中包含指定的团体属性列表，就显示该路由的信息。
adv-community-list-number：高级团体列表号，取值范围为 100～199。
peer ipv4-address：显示向指定对等体发布或者从指定对等体收到的 BGP IPv4 组播路由信息。
ipv4-address 为对等体的地址。
advertised-routes：显示向指定的对等体发布的路由信息。
received-routes：显示从指定的对等体接收到的路由信息。
statistics：显示路由的统计信息。
【使用指导】
如果没有指定任何参数，则显示所有 BGP IPv4 组播路由的简要信息。
如果只指定了 ipv4-address 参数，则将指定的网络地址和路由的掩码进行与操作，若计算结果与路由的网段地址相同，则显示该路由的详细信息。
如 果 指 定 了 或 参 数 ， 没 有 指 定ipv4-address mask ipv4-address mask-length参数，则显示与指定目的网络 地址和网络掩码（或掩码长度）精确匹配的longest-match IPv4 BGP IPv4 组播路由的详细信息。
【举例】
\# 显示所有 BGP IPv4 组播路由的简要信息。
<Sysname> display bgp routing-table ipv4 multicast Total number of routes: 3 BGP local router ID is 192.168.1.62 Status codes: * - valid, > - best, d - dampened, h - history

s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn
* > 5.5.5.5/32 127.0.0.1 0 32768 ?
* > 192.168.1.0 192.168.1.62 0 32768 ?
* > 192.168.1.62/32 127.0.0.1 0 32768 ?
\# 显示匹配编号为 20 的 AS 路径过滤列表的 BGP IPv4 组播路由信息。
<Sysname> display bgp routing-table ipv4 multicast as-path-acl 20 Total number of routes: 3 BGP local router ID is 192.168.1.62 Status codes: * - valid, > - best, d - dampened, h - history s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn
* > 5.5.5.5/32 127.0.0.1 0 32768 ?
* > 192.168.1.0 192.168.1.62 0 32768 ?
* > 192.168.1.62/32 127.0.0.1 0 32768 ?
\# 显示匹配 BGP 团体列表 100 的 BGP IPv4 组播路由信息。
<Sysname> display bgp routing-table ipv4 multicast community-list 100 Total number of routes: 3 BGP local router ID is 192.168.1.62 Status codes: * - valid, > - best, d - dampened, h - history s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn
* > 5.5.5.5/32 127.0.0.1 0 32768 ?
* > 192.168.1.0 192.168.1.62 0 32768 ?
* > 192.168.1.62/32 127.0.0.1 0 32768 ?
\# 显示向对等体 192.168.1.139 发布的所有 BGP IPv4 组播路由信息。
<Sysname> display bgp routing-table ipv4 multicast peer 192.168.1.139 advertised-routes Total number of routes: 2 BGP local router ID is 192.168.1.62 Status codes: * - valid, > - best, d - dampened, h - history

s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf Path/Ogn
* > 5.5.5.5/32 127.0.0.1 0 100 ?
* > 192.168.1.0 192.168.1.62 0 100 ?
\# 显示从对等体 192.168.1.139 收到的所有 BGP IPv4 组播路由信息。
<Sysname> display bgp routing-table ipv4 multicast peer 192.168.1.139 received-routes Total number of routes: 2 BGP local router ID is 192.168.1.62 Status codes: * - valid, > - best, d - dampened, h - history s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn
* >i 8.8.8.8/32 192.168.1.139 0 100 0 ?
* i 192.168.1.0 192.168.1.139 0 100 0 ?
表1-19 命令简要显示信息描述表display bgp routing-table ipv4 multicast字段 描述Total number of routes 路由总数BGP local router ID 本地的路由器ID路由状态代码：
• * – valid：合法路由
• best：普通优选最佳路由> –
• d – damped：震荡抑制路由
•h – history：历史路由Status codes
• s – suppressed：聚合抑制路由
• S – Stale：过期路由
• i – internal：内部路由
• e – external：外部路由
• a – additional-path：Add-Path 优选路由路由信息的来源，取值包括：
• i – IGP：表示路由产生于本 AS 内。通过 network 命令发布路由的路由信息来源为IGP Origin
• e – EGP：表示路由是通过 EGP（Exterior Gateway Protocol，外部网关协议）
学到的
• incomplete：表示路由的来源无法确定。从 协议引入路由的路由信息? – IGP

字段 描述来源为 incomplete目的网络地址Network NextHop 下一跳IP地址MED MED（Multi-Exit-Discriminator，多出口区分）属性值LocPrf 本地优先级PrefVal 路由首选值路由的AS路径（AS_PATH）属性和路由信息的来源（ORIGIN）属性，其中：
•Path/Ogn AS_PATH 属性记录了此路由经过的所有 AS，可以避免路由环路的出现
• ORIGIN 属性标记了此 BGP 路由如何生成的\# 显示到达目的网络 5.5.5.5/32 的 BGP IPv4 组播路由的详细信息。
<Sysname> display bgp routing-table ipv4 multicast 5.5.5.5 32 BGP local router ID: 192.168.1.139 Local AS number: 100 Paths: 1 available, 1 best BGP routing table information of 5.5.5.5/32:
From : 192.168.1.62 (192.168.1.62)
Rely nexthop : 192.168.1.62 Original nexthop: 192.168.1.62 OutLabel : NULL RxPathID : 0x0 TxPathID : 0x0 AS-path : (null)
Origin : incomplete Attribute value : MED 0, localpref 100, pref-val 0 State : valid, internal, best IP precedence : N/A QoS local ID : N/A Traffic index : N/A表1-20 display bgp routing-table ipv4 multicast 命令详细显示信息描述表字段 描述BGP local router ID 本地的路由器ID Local AS number 本地的AS号路由数信息Paths • available：有效路由数目
• best：最佳路由数目到达目的网络5.5.5.5/32的BGP路由表项信息BGP routing table information of

字段 描述
5.5.5.5/32 From 发布该路由的BGP对等体的IP地址Imported route 该路由为引入的路由路由迭代后的下一跳IP地址，如果没有迭代出下一跳地址，则显示为“not Rely Nexthop resolved”路由的原始下一跳地址，如果是从BGP更新消息中获得的路由，则该地址Original nexthop为接收到的消息中的下一跳IP地址OutLabel （暂不支持）路由的出标签值接收到的路由的Add-Path ID值RxPathID TxPathID 发送的路由的Add-Path ID值路由的AS路径（AS_PATH）属性，记录了此路由经过的所有AS，可以避AS-path免路由环路的出现路由信息的来源，取值包括：
• igp：表示路由产生于本 AS 内。通过 network 命令发布路由的路由信息来源为 IGP Origin • egp：表示路由是通过 EGP（Exterior Protocol，外部网关协Gateway议）学到的
• incomplete：表示路由的来源无法确定。从 IGP 协议引入路由的路由信息来源为 incomplete BGP路由属性信息，包括：
• MED：与目的网络关联的 MED 值Attribute value • localpref：本地优先级
• pref-val：路由首选值
• pre：协议优先级路由当前状态，取值包括：
• valid：有效路由
•internal：内部路由State • external：外部路由
• local：本地产生路由
• synchronize：同步路由
• best：最佳路由路由的IP优先级，取值范围为0～7，N/A表示无效值IP precedence QoS local ID 路由的QoS本地ID属性，取值范围为1～4095，N/A表示无效值Traffic index 流量索引值，取值范围为1～64，N/A表示无效值显示向对等体 发布的 组播路由的统计信息。
\# 192.168.1.62 BGP IPv4 <Sysname> display bgp routing-table ipv4 multicast peer 192.168.1.62 advertised-routes statistics

Advertised routes total: 2 \# 显示从对等体 192.168.1.62 收到的 BGP IPv4 组播路由的统计信息。
<Sysname> display bgp routing-table ipv4 multicast peer 192.168.1.62 received-routes statistics Received routes total: 2表1-21 命令显示信息描述表display bgp routing-table ipv4 multicast peer statistics字段 描述Advertised routes total 向指定对等体发布的路由总数Received routes total 从指定对等体收到的路由总数\# 显示 IPv4 组播的路由统计信息。
<Sysname> display bgp routing-table ipv4 multicast statistics Total number of routes: 5表1-22 display bgp routing-table ipv4 multicast statistics 命令显示信息描述表字段 描述Total number of routes 路由总数\# 显示到达目的网段 8.8.8.8/32 的 BGP IPv4 组播路由的通告信息。
<Sysname> display bgp routing-table ipv4 multicast 8.8.8.8 32 advertise-info BGP local router ID: 192.168.1.139 Local AS number: 100 Paths: 1 best BGP routing table information of 8.8.8.8/32(TxPathID:0):
Advertised to peers (1 in total):
192.168.1.62表1-23 display bgp routing-table ipv4 multicast advertise-info 命令显示信息描述表字段 描述BGP local router ID 本地的路由器ID Local AS number 本地的AS号Paths 到达指定目的网络的优选路由数目BGP routing table information of到达目的网络8.8.8.8/32的BGP路由的通告信息
8.8.8.8/32(TxPathID:0)
Advertised to peers (1 in total) 该路由已经向哪些对等体发送，以及对等体的数目

【相关命令】
• ip as-path（三层技术-IP 路由命令参考/路由策略）
• ip community-list（三层技术-IP 路由命令参考/路由策略）

##### 1.1.45 display bgp routing-table ipv4 unicast

display bgp routing-table ipv4 unicast 命令用来显示 BGP IPv4 单播路由信息。
【命令】
display bgp [ instance instance-name ] routing-table ipv4 [ unicast ] [ vpn-instance vpn-instance-name ] [ ipv4-address [ { mask-length | mask } [ longest-match ] ] | ipv4-address [ mask-length | mask ] advertise-info | as-path-acl as-path-acl-number | community-list { { basic-community-list-number | comm-list-name } [ whole-match ] | adv-community-list-number } | peer ipv4-address { advertised-routes | received-routes } [ ipv4-address [ mask-length | mask ] | statistics ] | statistics ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
instance instance-name：显示指定 BGP 实例的信息。instance-name 表示 BGP 实例的名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示 default 实例的信息。
vpn-instance vpn-instance-name：显示指定 VPN 实例的 BGP IPv4 单播路由信息。
表示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大vpn-instance-name小写。如果不指定本参数，则显示公网 单播路由信息。
BGP IPv4 ipv4-address：目的网络的 地址。
IPv4 mask-length：网络掩码长度，取值范围为 0～32。
mask：网络掩码，点分十进制格式。
longest-match：指定根据如下方法判断显示哪条 BGP IPv4 单播路由信息：
(1) 将用户输入的网络地址和路由的掩码进行与操作；
(2) 计算结果与路由的网段地址相同，且掩码小于等于用户输入子网掩码的路由中，子网掩码最长的路由将被显示出来。
advertise-info：显示 单播路由的通告信息。
BGP IPv4 as-path-acl-number：显示匹配指定 AS 路径过滤列表的 BGP IPv4 单播路由as-path-acl信息。as-path-acl-number 为 路径过滤列表号，取值范围为 1～256。
AS community-list：显示匹配指定 团体列表的 单播路由信息。
BGP BGP IPv4 basic-community-list-number：基本团体列表号，取值范围为 1～99。

comm-list-name：团体属性列表名，为 1～63 个字符的字符串，区分大小写。
whole-match：精确匹配。如果指定了本参数，则只有路由的团体属性列表与指定的团体属性列表完全相同时，才显示该路由的信息；如果未指定本参数，则只要路由的团体属性列表中包含指定的团体属性列表，就显示该路由的信息。
adv-community-list-number：高级团体列表号，取值范围为 100～199。
peer ipv4-address：显示向指定对等体发布或者从指定对等体收到的 BGP IPv4 单播路由信息。
ipv4-address 为对等体的地址。
advertised-routes：显示向指定的对等体发布的路由信息。
received-routes：显示从指定的对等体接收到的路由信息。
statistics：显示路由的统计信息。
【使用指导】
如果没有指定任何参数，则显示所有 BGP IPv4 单播路由的简要信息。
如果只指定了 参数，则将指定的网络地址和路由的掩码进行与操作，若计算结果ipv4-address与路由的网段地址相同，则显示该路由的信息。
如 果 指 定 了 或 参 数 ， 没 有 指 定ipv4-address mask ipv4-address mask-length参数，则显示与指定目的网络 地址和网络掩码（或掩码长度）精确匹配的longest-match IPv4 BGP IPv4 单播路由的信息。
执行本命令时指定 unicast 参数和不指定 unicast 参数的效果相同。
【举例】
\# 显示所有 BGP IPv4 单播路由的简要信息。
<Sysname> display bgp routing-table ipv4 Total number of routes: 4 BGP local router ID is 192.168.100.1 Status codes: * - valid, > - best, d - dampened, h - history s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn
* > 10.2.1.0/24 10.2.1.1 0 0 i e 10.2.1.2 0 0 200i
* > 192.168.1.0 192.168.1.135 0 0 i
* e 10.2.1.2 0 0 200i \# 显示匹配 AS 路径过滤列表 1 的 BGP IPv4 单播路由信息。
<Sysname> display bgp routing-table ipv4 as-path-acl 1 Total number of routes: 1 BGP local router ID is 2.2.2.2 Status codes: * - valid, > - best, d - dampened, h - history

s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn
* >e 30.1.1.0/24 20.1.1.1 0 200i \# 显示向对等体 10.2.1.2 发布的所有公网 BGP IPv4 单播路由信息。
<Sysname> display bgp routing-table ipv4 peer 10.2.1.2 advertised-routes Total number of routes: 2 BGP local router ID is 192.168.100.1 Status codes: * - valid, > - best, d - damped, h - history s - suppressed, S - Stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn
* > 10.2.1.0/24 10.2.1.1 0 0 i
* > 192.168.1.0 192.168.1.135 0 0 i \# 显示从对等体 10.2.1.2 收到的所有公网 BGP IPv4 单播路由信息。
<Sysname> display bgp routing-table ipv4 peer 10.2.1.2 received-routes Total number of routes: 2 BGP local router ID is 192.168.100.1 Status codes: * - valid, > - best, d - damped, h - history s - suppressed, S - Stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn e 10.2.1.0/24 10.2.1.2 0 0 200i
* e 192.168.1.0 10.2.1.2 0 0 200i表1-24 display bgp routing-table ipv4 unicast 命令简要显示信息描述表字段 描述路由总数Total number of routes BGP local router ID 本地的路由器ID路由状态代码：
• valid：合法路由
* –Status codes
• > – best：普通优选最佳路由
• d - dampened：震荡抑制路由

字段 描述
• h – history：历史路由
•s – suppressed：聚合抑制路由
• S – stale：过期路由
• i – internal：内部路由
• e – external：外部路由
• a – additional-path：Add-Path 优选路由路由信息的来源，取值包括：
• i – IGP：表示路由产生于本 AS 内。通过 network 命令发布路由的路由信息来源为 IGP Origin • EGP：表示路由是通过 EGP（Exterior Protocol，外部网关协议）
e – Gateway学到的
• ? – incomplete：表示路由的来源无法确定。从 IGP 协议引入路由的路由信息来源为 incomplete Network 目的网络地址NextHop 下一跳IP地址MED MED（Multi-Exit Discriminator，多出口区分）属性值LocPrf 本地优先级路由首选值PrefVal路由的AS路径（AS_PATH）属性和路由信息的来源（ORIGIN）属性，其中：
Path/Ogn • AS_PATH 属性记录了此路由经过的所有 AS，可以避免路由环路的出现
• ORIGIN 属性标记了此 BGP 路由如何生成的\# 显示到达目的网络 10.2.1.0/24 的 BGP IPv4 单播路由的详细信息。
<Sysname> display bgp routing-table ipv4 10.2.1.0 24 BGP local router ID: 192.168.100.1 Local AS number: 100 Paths: 2 available, 1 best BGP routing table information of 10.2.1.0/24:
Imported route.
Original nexthop: 10.2.1.1 OutLabel : NULL RxPathID : 0x0 TxPathID : 0x0 AS-path : (null)
Origin : igp Attribute value : MED 0, pref-val 0, pre 0 State : valid, local, best IP precedence : N/A QoS local ID : N/A

Traffic index : N/A From : 10.2.1.2 (192.168.100.2)
Rely nexthop : not resolved Original nexthop: 10.2.1.2 OutLabel : NULL RxPathID : 0x0 TxPathID : 0x0 AS-path : 200 Origin : igp Attribute value : MED 0, pref-val 0, pre 255 State : external IP precedence : N/A QoS local ID : N/A Traffic index : N/A \# 显示到达目的网络 1.1.1.1/32 的 BGP IPv4 单播路由的详细信息。
<Sysname> display bgp routing-table ipv4 1.1.1.1 32 BGP local router ID: 192.168.100.1 Local AS number: 100 Paths: 2 available, 1 best BGP routing table information of 1.1.1.1/32:
From : 10.2.1.1 (192.168.100.3)
Rely nexthop : 10.2.1.1 Original nexthop: 10.2.1.1 OutLabel : NULL RxPathID : 0x0 TxPathID : 0x0 AS-path : (null)
Origin : igp Attribute value : MED 0, pref-val 0, pre 0 State : valid, local, best IP precedence : N/A QoS local ID : N/A Traffic index : N/A Backup route.
From : 10.2.1.2 (192.168.100.2)
Rely nexthop : 10.2.1.2 Original nexthop: 10.2.1.2 OutLabel : NULL RxPathID : 0x0 TxPathID : 0x0 AS-path : 200 Origin : igp

Attribute value : MED 0, pref-val 0, pre 255 State : external IP precedence : N/A QoS local ID : N/A Traffic index : N/A表1-25 display bgp routing-table ipv4 unicast 命令详细显示信息描述表字段 描述BGP local router ID 本地的路由器ID本地的AS号Local AS number路由数信息Paths • available：有效路由数目
• best：最佳路由数目BGP routing table information of到达目的网络10.2.1.0/24的BGP路由表项信息
10.2.1.0/24 Imported route 该路由为引入的路由路由的原始下一跳地址，如果是从BGP更新消息中获得的路由，则该地址Original nexthop为接收到的消息中的下一跳IP地址OutLabel （暂不支持）路由的出标签值RxPathID 接收到的路由的Add-Path ID值发送的路由的Add-Path ID值TxPathID路由的AS路径（AS_PATH）属性，记录了此路由经过的所有AS，可以避AS-path免路由环路的出现路由信息的来源，取值包括：
• igp：表示路由产生于本 AS 内。通过 命令发布路由的路由network信息来源为 IGP Origin
• egp：表示路由是通过 EGP（Exterior Gateway Protocol，外部网关协议）学到的
• incomplete：表示路由的来源无法确定。从 IGP 协议引入路由的路由信息来源为 incomplete BGP路由属性信息，包括：
• MED：与目的网络关联的 值MED Attribute value • localpref：本地优先级
• pref-val：路由首选值
• pre：协议优先级路由当前状态，取值包括：
• valid：有效路由
• internal ：内部路由State
• external：外部路由
• local：本地产生路由
• synchronize：同步路由

字段 描述
• best：最佳路由From 发布该路由的BGP对等体的IP地址路由迭代后的下一跳IP地址，如果没有迭代出下一跳地址，则显示为“not Rely Nexthop resolved”IP precedence 路由的IP优先级，取值范围为0～7，N/A表示无效值QoS local ID 路由的QoS本地ID属性，取值范围为1～4095，N/A表示无效值流量索引值，取值范围为1～64，N/A表示无效值Traffic index Backup route 该路由为备份的路由\# 显示向对等体 10.2.1.2 发布的公网 BGP IPv4 单播路由的统计信息。
<Sysname> display bgp routing-table ipv4 peer 10.2.1.2 advertised-routes statistics Advertised routes total: 2 \# 显示从对等体 10.2.1.2 收到的公网 BGP IPv4 单播路由的统计信息。
<Sysname> display bgp routing-table ipv4 peer 10.2.1.2 received-routes statistics Received routes total: 2表1-26 display bgp routing-table ipv4 unicast peer statistics 命令显示信息描述表字段 描述Advertised routes total 向指定对等体发布的路由总数从指定对等体收到的路由总数Received routes total \# 显示 BGP IPv4 单播路由的统计信息。
<Sysname> display bgp routing-table ipv4 statistics Total number of routes: 4表1-27 命令显示信息描述表display bgp routing-table ipv4 unicast statistics字段 描述Total number of routes 路由总数显示到达目的网段 的 单播路由的通告信息。
\# 10.2.1.0/24 BGP IPv4 <Sysname> display bgp routing-table ipv4 10.2.1.0 24 advertise-info BGP local router ID: 192.168.100.1 Local AS number: 100 Paths: 1 best BGP routing table information of 10.2.1.0/24(TxPathID:0):

Advertised to peers (1 in total):
10.2.1.2表1-28 display bgp routing-table ipv4 unicast advertise-info 命令显示信息描述表字段 描述BGP local router ID 本地的路由器ID本地的AS号Local AS number Paths 到达指定目的网络的优选路由数目BGP routing table information of到达目的网络10.2.1.0/24的BGP路由的通告信息
10.2.1.0/24(TxPathID:0)
该路由已经向哪些对等体发送，以及对等体的数目Advertised to peers (1 in total)
【相关命令】
as-path（三层技术-IP 路由命令参考/路由策略）
• ip community-list（三层技术-IP 路由命令参考/路由策略）
• ip

##### 1.1.46 display bgp routing-table ipv6 multicast

命令用来显示 BGP IPv6 组播路由信息。
display bgp routing-table ipv6 multicast【命令】
display bgp [ instance instance-name ] routing-table ipv6 multicast [ ipv6-address prefix-length [ advertise-info ] | as-path-acl as-path-acl-number | community-list { { basic-community-list-number | comm-list-name } [ whole-match ] | adv-community-list-number } | peer ipv6-address { advertised-routes | received-routes } [ ipv6-address prefix-length | statistics ] | statistics ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
instance-name：显示指定 实例的信息。instance-name 表示 实例的名instance BGP BGP称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示 default 实例的信息。
ipv6-address prefix-length：显示与指定的目的网络地址和前缀长度精确匹配的 BGP IPv6组播路由信息。prefix-length 为目的网络地址的前缀长度，取值范围为 0～128。如果没有指定本参数，则显示所有 BGP IPv6 组播路由的简要信息。
advertise-info：显示 BGP IPv6 组播路由的通告信息。如果没有指定本参数，则显示 BGP IPv6组播路由表的信息。

as-path-acl-number：显示匹配指定 AS 路径过滤列表的 BGP IPv6 组播路由as-path-acl信息。as-path-acl-number 为 路径过滤列表号，取值范围为 1～256。
AS communit-list：显示匹配指定 团体列表的 组播路由信息。
BGP BGP IPv6 basic-community-list-number：基本团体列表号，取值范围为 1～99。
comm-list-name：团体属性列表名，为 1～63 个字符的字符串，区分大小写。
whole-match：精确匹配。如果指定了本参数，则只有路由的团体属性列表与指定的团体属性列表完全相同时，才显示该路由的信息；如果未指定本参数，则只要路由的团体属性列表中包含指定的团体属性列表，就显示该路由的信息。
adv-community-list-number：高级团体列表号，取值范围为 100～199。
peer：显示向指定的对等体发布或者从指定的对等体收到的 BGP IPv6 组播路由信息。
ipv6-address：对等体的 IPv6 地址。
advertised-routes：显示向指定的对等体发布的路由信息。
received-routes：显示从指定的对等体接收到的路由信息。
statistics ：显示路由的统计信息。
【举例】
\# 显示所有 BGP IPv6 组播路由的简要信息。
<Sysname> display bgp routing-table ipv6 multicast Total number of routes: 5 BGP local router ID is 192.168.1.139 Status codes: * - valid, > - best, d - dampened, h - history s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete
* > Network : 1:: PrefixLen : 64 NextHop : :: LocPrf :
PrefVal : 32768 OutLabel : NULL MED : 0 Path/Ogn: ?
* i Network : 1:: PrefixLen : 64 NextHop : 1::1 LocPrf : 100 PrefVal : 0 OutLabel : NULL MED : 0 Path/Ogn: ?
* > Network : 1::2 PrefixLen : 128 NextHop : ::1 LocPrf :
PrefVal : 32768 OutLabel : NULL MED : 0 Path/Ogn: ?

* > Network : 2::2 PrefixLen : 128
NextHop : ::1 LocPrf :
PrefVal : 32768 OutLabel : NULL
MED : 0
Path/Ogn: ?
* >i Network : 5::5 PrefixLen : 128
NextHop : 1::1 LocPrf : 100
PrefVal : 0 OutLabel : NULL
MED : 0
Path/Ogn: ?
\# 显示匹配 AS 路径过滤列表 1 的 BGP IPv6 组播路由信息。
<Sysname> display bgp routing-table ipv6 multicast as-path-acl 1
Total number of routes: 5
BGP local router ID is 192.168.1.139
Status codes: * - valid, > - best, d - dampened, h - history
s - suppressed, S - stale, i - internal, e - external
a – additional-path
Origin: i - IGP, e - EGP, ? - incomplete
* > Network : 1:: PrefixLen : 64
NextHop : :: LocPrf :
PrefVal : 32768 OutLabel : NULL
MED : 0
Path/Ogn: ?
* i Network : 1:: PrefixLen : 64
NextHop : 1::1 LocPrf : 100
PrefVal : 0 OutLabel : NULL
MED : 0
Path/Ogn: ?
* > Network : 1::2 PrefixLen : 128
NextHop : ::1 LocPrf :
PrefVal : 32768 OutLabel : NULL
MED : 0
Path/Ogn: ?
* > Network : 2::2 PrefixLen : 128
NextHop : ::1 LocPrf :
PrefVal : 32768 OutLabel : NULL
MED : 0
Path/Ogn: ?
* >i Network : 5::5 PrefixLen : 128
NextHop : 1::1 LocPrf : 100

PrefVal : 0 OutLabel : NULL MED : 0 Path/Ogn: ?
\# 显示匹配 BGP 团体列表 100 的 BGP IPv6 组播路由信息。
<Sysname> display bgp routing-table ipv6 multicast community-list 100 Total number of routes: 5 BGP local router ID is 192.168.1.139 Status codes: * - valid, > - best, d - dampened, h - history s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete
* > Network : 1:: PrefixLen : 64 NextHop : :: LocPrf :
PrefVal : 32768 OutLabel : NULL MED : 0 Path/Ogn: ?
* i Network : 1:: PrefixLen : 64 NextHop : 1::1 LocPrf : 100 PrefVal : 0 OutLabel : NULL MED : 0 Path/Ogn: ?
* > Network : 1::2 PrefixLen : 128 NextHop : ::1 LocPrf :
PrefVal : 32768 OutLabel : NULL MED : 0 Path/Ogn: ?
* > Network : 2::2 PrefixLen : 128 NextHop : ::1 LocPrf :
PrefVal : 32768 OutLabel : NULL MED : 0 Path/Ogn: ?
* >i Network : 5::5 PrefixLen : 128 NextHop : 1::1 LocPrf : 100 PrefVal : 0 OutLabel : NULL MED : 0 Path/Ogn: ?
\# 显示向对等体 1::1 发布的所有 BGP IPv6 组播路由信息。
<Sysname> display bgp routing-table ipv6 multicast peer 1::1 advertised-routes Total number of routes: 2

BGP local router ID is 192.168.1.139 Status codes: * - valid, > - best, d - dampened, h - history s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete
* > Network : 1:: PrefixLen : 64 NextHop : :: LocPrf : 100 MED : 0 OutLabel : NULL Path/Ogn: ?
* > Network : 2::2 PrefixLen : 128 NextHop : ::1 LocPrf : 100 MED : 0 OutLabel : NULL Path/Ogn: ?
\# 显示从对等体 1::1 收到的所有 BGP IPv6 组播路由信息。
<Sysname> display bgp routing-table ipv6 multicast peer 1::1 received-routes Total number of routes: 2 BGP local router ID is 192.168.1.139 Status codes: * - valid, > - best, d - dampened, h - history s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete
* i Network : 1:: PrefixLen : 64 NextHop : 1::1 LocPrf : 100 PrefVal : 0 OutLabel : NULL MED : 0 Path/Ogn: ?
* >i Network : 5::5 PrefixLen : 128 NextHop : 1::1 LocPrf : 100 PrefVal : 0 OutLabel : NULL MED : 0 Path/Ogn: ?
表1-29 display bgp routing-table ipv6 multicast 命令简要显示信息描述表字段 描述Total number of routes 路由总数BGP local router ID 本地的路由器ID路由状态代码：
• * – valid：合法路由Status codes
• > – best：普通优选最佳路由
• damped：震荡抑制路由d –

字段 描述
• h – history：历史路由
•s – suppressed：聚合抑制路由
• S – Stale：过期路由
• i – internal：内部路由
• e – external：外部路由
• a – additional-path：Add-Path 优选路由路由信息的来源，取值包括：
• i – IGP：表示路由产生于本 AS 内。通过 network 命令发布路由的路由信息来源为 IGP Origin • EGP：表示路由是通过 EGP（Exterior Protocol，外部网关协议）
e – Gateway学到的
• ? – incomplete：表示路由的来源无法确定。从 IGP 协议引入路由的路由信息来源为 incomplete Network 目的网络地址PrefixLen 目的网络地址的前缀长度NextHop 下一跳IP地址LocPrf 本地优先级路由首选值PrefVal OutLabel （暂不支持）路由的出标签值MED MED（Multi-Exit-Discriminator，多出口区分）属性值路由的AS路径（AS_PATH）属性和路由信息的来源（ORIGIN）属性，其中：
Path/Ogn • AS_PATH 属性记录了此路由经过的所有 AS，可以避免路由环路的出现
• ORIGIN 属性标记了此 BGP 路由如何生成的\# 显示到达目的网络 2::2/128 的 BGP IPv6 组播路由的详细信息。
<Sysname> display bgp routing-table ipv6 multicast 2::2 128 BGP local router ID: 192.168.1.139 Local AS number: 100 Paths: 1 available, 1 best BGP routing table information of 2::2/128:
Imported route.
Original nexthop: ::1 OutLabel : NULL RxPathID : 0x0 TxPathID : 0x0 AS-path : (null)
Origin : incomplete Attribute value : MED 0, pref-val 32768

State : valid, local, best IP precedence : N/A QoS local ID : N/A Traffic index : N/A表1-30 display bgp routing-table ipv6 multicast 命令详细显示信息描述表字段 描述BGP local router ID 本地的路由器ID Local AS number 本地的AS号路由数信息Paths • available：有效路由数目
• best：最佳路由数目BGP routing table information of到达目的网络2::2/128的BGP路由表项信息2::2/128 Imported route 该路由为引入的路由路由的原始下一跳地址，如果是从BGP更新消息中获得的路由，则该地址Original nexthop为接收到的消息中的下一跳IP地址OutLabel （暂不支持）路由的出标签值RxPathID 接收到的路由的Add-Path ID值TxPathID 发送的路由的Add-Path ID值路由的AS路径（AS_PATH）属性，记录了此路由经过的所有AS，可以避AS-path免路由环路的出现路由信息的来源，取值包括：
• igp：表示路由产生于本 AS 内。通过 network 命令发布路由的路由信息来源为 IGP Origin
• egp：表示路由是通过 EGP（Exterior Gateway Protocol，外部网关协议）学到的
•incomplete：表示路由的来源无法确定。从 IGP 协议引入路由的路由信息来源为incomplete BGP路由属性信息，包括：
• MED：与目的网络关联的 MED 值Attribute value • localpref：本地优先级
• pref-val：路由首选值
• pre：协议优先级路由当前状态，取值包括：
• valid：有效路由
• internal：内部路由State
• external ：外部路由
• local：本地产生路由
• best：最佳路由From 发布该路由的BGP对等体的IP地址

字段 描述路由迭代后的下一跳IP地址，如果没有迭代出下一跳地址，则显示为“not Rely Nexthop resolved”IP precedence 路由的IP优先级，取值范围为0～7，N/A表示无效值路由的QoS本地ID属性，取值范围为1～4095，N/A表示无效值QoS local ID Traffic index 流量索引值，取值范围为1～64，N/A表示无效值\# 显示到达目的网段 2::2/128 的 BGP IPv6 组播路由的通告信息。
<Sysname> display bgp routing-table ipv6 multicast 2::2 128 advertise-info BGP local router ID: 192.168.1.139 Local AS number: 100 Paths: 1 best BGP routing table information of 2::2/128(TxPathID:0):
Advertised to peers (1 in total):
1::1表1-31 display bgp routing-table ipv6 multicast advertise-info 命令显示信息描述表字段 描述BGP local router ID 本地的路由器ID Local AS number 本地的AS号Paths 到达指定目的网络的优选路由数目BGP routing table information of到达目的网络2::2/128的BGP路由的通告信息2::2/128(TxPathID:0)
Advertised to peers (1 in total) 该路由已经向哪些对等体发送，以及对等体的数目\# 显示向对等体 1::1 发布的 BGP IPv6 组播路由的统计信息。
<Sysname> display bgp routing-table ipv6 multicast peer 1::1 advertised-routes statistics Advertised routes total: 2显示从对等体 收到的 组播路由的统计信息。
\# 1::1 BGP IPv6 <Sysname> display bgp routing-table ipv6 multicast peer 1::1 received-routes statistics Received routes total: 2表1-32 display bgp routing-table ipv6 multicast peer statistics 命令显示信息描述表字段 描述向指定对等体发布的路由总数Advertised routes total Received routes total 从指定对等体收到的路由总数

\# 显示 BGP IPv6 组播的路由统计信息。
<Sysname> display bgp routing-table ipv6 multicast statistics Total number of routes: 5表1-33 display bgp routing-table ipv6 multicast statistics 命令显示信息描述表字段 描述Total number of routes 路由总数【相关命令】
• ip as-path（三层技术-IP 路由命令参考/路由策略）
• ip community-list（三层技术-IP 路由命令参考/路由策略）

##### 1.1.47 display bgp routing-table ipv6 unicast

命令用来显示 单播路由信息。
display bgp routing-table ipv6 unicast BGP IPv6【命令】
display bgp [ instance instance-name ] routing-table ipv6 [ unicast ] [ vpn-instance vpn-instance-name ] [ ipv6-address prefix-length [ advertise-info ] | as-path-acl as-path-acl-number | community-list { { basic-community-list-number | comm-list-name } [ whole-match ] | adv-community-list-number } | peer ipv6-address { advertised-routes | received-routes } [ ipv6-address prefix-length | statistics ] | statistics ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
instance instance-name：显示指定 BGP 实例的信息。instance-name 表示 BGP 实例的名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示 default 实例的信息。
vpn-instance-name：显示指定 VPN 实例的 BGP IPv6 单播路由信息。
vpn-instance表示 的 实例名称，为 1～31 个字符的字符串，区分大vpn-instance-name MPLS L3VPN VPN小写。如果不指定本参数，则显示公网 BGP IPv6 单播路由信息。
ipv6-address prefix-length：显示与指定的目的网络地址和前缀长度精确匹配的 BGP IPv6单播路由信息。prefix-length 为目的网络地址的前缀长度，取值范围为 0～128。如果没有指定本参数，则显示所有 BGP IPv6 单播路由的简要信息。
advertise-info：显示 BGP IPv6 单播路由的通告信息。如果没有指定本参数，则显示 BGP IPv6单播路由表的信息。

as-path-acl-number：显示匹配指定 AS 路径过滤列表的 BGP IPv6 单播路由as-path-acl信息。as-path-acl-number 为 路径过滤列表号，取值范围为 1～256。
AS communit-list：显示匹配指定 团体列表的 单播路由信息。
BGP BGP IPv6 basic-community-list-number：基本团体列表号，取值范围为 1～99。
comm-list-name：团体属性列表名，为 1～63 个字符的字符串，区分大小写。
whole-match：精确匹配。如果指定了本参数，则只有路由的团体属性列表与指定的团体属性列表完全相同时，才显示该路由的信息；如果未指定本参数，则只要路由的团体属性列表中包含指定的团体属性列表，就显示该路由的信息。
adv-community-list-number：高级团体列表号，取值范围为 100～199。
peer：显示向指定的对等体发布或者从指定的对等体收到的 BGP IPv6 单播路由信息。
ipv4-address：对等体的 IPv4 地址。
ipv6-address：对等体的 IPv6 地址。
advertised-routes：显示向指定的对等体发布的路由信息。
received-routes ：显示从指定的对等体接收到的路由信息。
statistics：显示路由的统计信息。
【使用指导】
执行本命令时指定 unicast 参数和不指定 unicast 参数的效果相同。
【举例】
\# 显示所有 BGP IPv6 单播路由的简要信息。
<Sysname> display bgp routing-table ipv6 Total number of routes: 1 BGP local router ID is 192.168.1.136 Status codes: * - valid, > - best, d - dampened, h - history s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete
* >e Network : 3:: PrefixLen : 64 NextHop : 1::2 LocPrf :
PrefVal : 0 OutLabel : NULL MED :
Path/Ogn: 100i \# 显示匹配 AS 路径过滤列表 1 的 BGP IPv6 单播路由信息。
<Sysname> display bgp routing-table ipv6 as-path-acl 1 Total number of routes: 2 BGP local router ID is 192.168.1.136 Status codes: * - valid, > - best, d - dampened, h - history s - suppressed, S - stale, i - internal, e - external a – additional-path

Origin: i - IGP, e - EGP, ? - incomplete
* >e Network : 2:: PrefixLen : 64 NextHop : 1::2 LocPrf :
PrefVal : 0 OutLabel : NULL MED :
Path/Ogn: 100i
* >e Network : 3:: PrefixLen : 64 NextHop : 1::2 LocPrf :
PrefVal : 0 OutLabel : NULL MED :
Path/Ogn: 100i \# 显示匹配 BGP 团体列表 100 的 BGP IPv6 单播路由信息。
<Sysname> display bgp routing-table ipv6 community-list 100 Total number of routes: 2 BGP local router ID is 192.168.1.136 Status codes: * - valid, > - best, d - dampened, h - history s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete
* >e Network : 2:: PrefixLen : 64 NextHop : 1::2 LocPrf :
PrefVal : 0 OutLabel : NULL MED :
Path/Ogn: 100i
* >e Network : 3:: PrefixLen : 64 NextHop : 1::2 LocPrf :
PrefVal : 0 OutLabel : NULL MED :
Path/Ogn: 100i \# 显示向对等体 1::1 发布的所有 BGP IPv6 单播路由信息。
<Sysname> display bgp routing-table ipv6 peer 1::1 advertised-routes Total number of routes: 1 BGP local router ID is 192.168.1.136 Status codes: * - valid, > - best, d - dampened, h - history s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete
* > Network : 2:: PrefixLen : 64 NextHop : :: LocPrf :

MED : 0 OutLabel : NULL Path/Ogn: i \# 显示从对等体 1::1 收到的所有 BGP IPv6 单播路由信息。
<Sysname> display bgp routing-table ipv6 peer 1::1 received-routes Total number of routes: 1 BGP local router ID is 192.168.1.135 Status codes: * - valid, > - best, d - dampened, h - history s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete
* >e Network : 2:: PrefixLen : 64 NextHop : ::FFFF:10.1.1.1 LocPrf :
PrefVal : 0 OutLabel : NULL MED : 0 Path/Ogn: 100i表1-34 display bgp routing-table ipv6 unicast 命令简要显示信息描述表字段 描述Total number of routes 路由总数BGP local router ID 本地的路由器ID路由状态代码：
•
* – valid：合法路由
• > – best：普通优选最佳路由
• d - dampened：震荡抑制路由
• h – history：历史路由Status codes
• s – suppressed：聚合抑制路由
• S – stale：过期路由
• i – internal：内部路由
• external：外部路由e –
• a – additional-path：Add-Path 优选路由路由信息的来源，取值包括：
• i – IGP：表示路由产生于本 AS 内。通过 命令发布路由的路由信息network来源为 IGP Origin
• e – EGP：表示路由是通过 EGP（Exterior Gateway Protocol，外部网关协议）
学到的
• ? – incomplete：表示路由的来源无法确定。从 IGP 协议引入路由的路由信息来源为 incomplete Network 目的网络地址目的网络地址的前缀长度PrefixLen NextHop 下一跳IP地址

字段 描述LocPrf 本地优先级PrefVal 路由首选值（暂不支持）路由的出标签值OutLabel MED MED（Multi-Exit Discriminator，多出口区分）属性值路由的AS路径（AS_PATH）属性和路由信息的来源（ORIGIN）属性，其中：
• 属性记录了此路由经过的所有 AS，可以避免路由环路的出现Path/Ogn AS_PATH
• ORIGIN 属性标记了此 BGP 路由如何生成的显示到达目的网络 的 单播路由的详细信息。
\# 2::/64 BGP IPv6 <Sysname> display bgp routing-table ipv6 2:: 64 BGP local router ID: 192.168.1.135 Local AS number: 200 Paths: 2 available, 1 best BGP routing table information of 2::/64:
From : 10.1.1.1 (192.168.1.136)
Rely nexthop : ::FFFF:10.1.1.1 Original nexthop: ::FFFF:10.1.1.1 OutLabel : NULL RxPathID : 0x0 TxPathID : 0x0 AS-path : 100 Origin : igp Attribute value : MED 0, pref-val 0 State : valid, external, best IP precedence : N/A QoS local ID : N/A Traffic index : N/A Backup route.
From : 1::1 (192.168.1.136)
Rely nexthop : 1::1 Original nexthop: 1::1 OutLabel : NULL RxPathID : 0x0 TxPathID : 0x0 AS-path : 100 Origin : igp Attribute value : MED 0, pref-val 0 State : valid, external IP precedence : N/A QoS local ID : N/A

Traffic index : N/A表1-35 display bgp routing-table ipv6 unicast 命令详细显示信息描述表字段 描述BGP local router ID 本地的路由器ID Local AS number 本地的AS号路由数信息Paths • available：有效路由数目
• best：最佳路由数目BGP routing table information of到达目的网络2::/64的BGP路由表项信息2::/64 Imported route 该路由为引入的路由路由的原始下一跳地址，如果是从BGP更新消息中获得的路由，则该地址Original nexthop为接收到的消息中的下一跳IP地址OutLabel （暂不支持）路由的出标签值RxPathID 接收到的路由的Add-Path ID值TxPathID 发送的路由的Add-Path ID值路由的AS路径（AS_PATH）属性，记录了此路由经过的所有AS，可以避AS-path免路由环路的出现路由信息的来源，取值包括：
• igp：表示路由产生于本 AS 内。通过 network 命令发布路由的路由信息来源为 IGP Origin
• egp：表示路由是通过 EGP（Exterior Gateway Protocol，外部网关协议）学到的
•incomplete：表示路由的来源无法确定。从 IGP 协议引入路由的路由信息来源为incomplete BGP路由属性信息，包括：
• MED：与目的网络关联的 MED 值Attribute value • localpref：本地优先级
• pref-val：路由首选值
• pre：协议优先级路由当前状态，取值包括：
• valid：有效路由
• internal：内部路由State
• external：外部路由
• local：本地产生路由
• best：最佳路由From 发布该路由的BGP对等体的IP地址路由迭代后的下一跳IP地址，如果没有迭代出下一跳地址，则显示为“not Rely Nexthop resolved”

字段 描述IP precedence 路由的IP优先级，取值范围为0～7，N/A表示无效值QoS local ID 路由的QoS本地ID属性，取值范围为1～4095，N/A表示无效值流量索引值，取值范围为1～64，N/A表示无效值Traffic index Backup route 该路由为备份的路由\# 显示到达目的网段 2::/64 的 BGP IPv6 单播路由的通告信息。
<Sysname> display bgp routing-table ipv6 2:: 64 advertise-info BGP local router ID: 192.168.1.136 Local AS number: 100 Paths: 1 best BGP routing table information of 2::/64(TxPathID:0):
Advertised to peers (2 in total):
10.1.1.2 1::2表1-36 display bgp routing-table ipv6 unicast advertise-info 命令显示信息描述表字段 描述BGP local router ID 本地的路由器ID Local AS number 本地的AS号到达指定目的网络的优选路由数目Paths BGP routing table information of到达目的网络2::/64的BGP路由的通告信息2::/64(TxPathID:0)
Advertised to peers (2 in total) 该路由已经向哪些对等体发送，以及对等体的数目显示向对等体 发布的 单播路由的统计信息。
\# 1::1 BGP IPv6 <Sysname> display bgp routing-table ipv6 peer 1::1 advertised-routes statistics Advertised routes total: 1显示从对等体 收到的 单播路由的统计信息。
\# 1::1 BGP IPv6 <Sysname> display bgp routing-table ipv6 peer 1::1 received-routes statistics Received routes total: 1表1-37 display bgp routing-table ipv6 unicast peer statistics 命令显示信息描述表字段 描述Advertised routes total 向指定对等体发布的路由总数Received routes total 从指定对等体收到的路由总数

\# 显示 BGP IPv6 单播路由的统计信息。
<Sysname> display bgp routing-table ipv6 statistics Total number of routes: 4表1-38 display bgp routing-table ipv6 unicast statistics 命令显示信息描述表字段 描述Total number of routes 路由总数【相关命令】
• ip as-path（三层技术-IP 路由命令参考/路由策略）
• ip community-list（三层技术-IP 路由命令参考/路由策略）

##### 1.1.48 display bgp rpki server

display bgp rpki table 命令用来显示与 RPKI 服务器连接的相关信息。
【命令】
display bgp [ instance instance-name ] rpki server [ [ vpn-instance vpn-instance-name ] ipv4-address ] display bgp [ instance instance-name ] rpki server [ [ vpn-instance vpn-instance-name ] ipv6-address ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
：显示指定 BGP 实例的信息。 表示 BGP 实例的名instance instance-name instance-name称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示 实例的信息。
default vpn-instance-name：显示指定 实例内与 服务器的连接状态信息。
vpn-instance VPN RPKI vpn-instance-name 表示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果不指定本参数，则显示公网中路由器与 RPKI 服务器的连接状态信息。
ipv4-address：RPKI 服务器的 IPv4 地址。
ipv6-address：RPKI 服务器的 IPv6 地址。
【举例】
\# 显示与 RPKI 服务器连接的简要信息。
<Sysname> display bgp rpki server Server VPN-index Port State Time ROAs(IPv4/IPv6)
1.1.1.2 0 1234 Establish 00:05:51 1/0

2.2.2.2 0 1234 Establish 00:06:07 3/1
表1-39 display bgp rpki server 命令显示简要信息描述表
字段 描述
Server RPKI服务器的IP地址
VPN-index VPN索引
RPKI服务使用的端口号
Port
与RPKI服务器的连接状态：
• Establish：表示与 RPKI 服务器已建立连接
State
• Connect：表示正在尝试与 RPKI 服务器进行连接
• Shutdown：表示未与 RPKI 服务器建立连接
RPKI连接当前状态持续的时长
Time
ROAs(IPv4/IPv6) 获得的IPv4/IPv6的ROA条目数量
\# 显示路由器与 RPKI 服务器连接的详细信息。
<Sysname> display bgp rpki server 2.2.2.1
RPKI Cache-Server 2.2.2.1
Port: TCP port 1234
Local addr: 2.2.2.2, Local port: 14342
Connect state: Establish
Total byte Rx: 72
Total byte Tx: 8
Session ID: 1
Serial number: 1
Last PDU type 7, Time: 00:00:15
Last disconnect reason: Response timer expired
表1-40 display bgp rpki server 命令显示详细信息描述表
字段 描述
RPKI Cache-Server RPKI服务器的IP地址
Port RPKI 服务器上使用的端口号
与RPKI服务器连接的本地IP地址
Local addr
Local port 与RPKI服务器连接的本地端口号
与RPKI服务器的连接状态：
• Establish：表示和 服务器的连接已建立
RPKI
Connect state
• Connect：表示正在尝试与 RPKI 服务器进行连接
• Shutdown：表示未与 RPKI 服务器建立连接
Total byte Rx 收到报文的总字节数
Total byte Tx 发送报文的总字节数
Session ID RPKI服务器分配的会话ID

字段 描述Serial number RPKI服务器分配的序列号Last PDU Type 最后一次收到的PDU报文的类型RPKI连接当前状态持续的时长Time RPKI连接上次中断的原因：
• Confingure reset：用户更改与 RPKI 服务器建立连接的端口或执行 reset bgp rpki server 命令
• Receive error report PDU：收到服务器发送的 Error report 报文
• Response timer expired：响应时间超时Last disconnect reason
• Receive error PDU：收到错误报文
• TCP connect failed：TCP 连接断开
• port：未配置 服务端口Shutdown BGP RPKI
• Not enough memory：内存不足
• PDU：收到 服务器发送的 报文Receive cache reset RPKI reset

##### 1.1.49 display bgp rpki table

display bgp rpki table 命令用来显示从 RPKI 服务器获得的 ROA 信息。
【命令】
display bgp [ instance instance-name ] rpki table ipv4 [ ipv4-address min min-length max max-lenth ] display bgp [ instance instance-name ] rpki table ipv6 [ ipv6-address min min-length max max-lenth ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
instance-name：显示指定 实例的信息。instance-name 表示 实例的名instance BGP BGP称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示 default 实例的信息。
ipv4：显示 IPv4 地址前缀的 ROA 信息。
ipv4-address：显示指定 地址的 信息。如果不指定本参数，则显示所有 地址的IPv4 ROA IPv4 ROA 信息。
ipv6：显示 IPv6 地址前缀的 ROA 信息。
ipv6-address：显示指定 IPv6 地址的 ROA 信息。如果不指定本参数，则显示所有 IPv6 地址的ROA 信息。

min-length：ROA 信息中的最小前缀长度。对于 IPv4 地址的 ROA 信息，最小前缀长度的取值范围为 0～32；对于 地址前缀的 信息最小前缀长度的取值范围为 0～128。
IPv6 ROA max-length：ROA 信息中的最大前缀长度。对于 地址的 信息，最大前缀长度的取值IPv4 ROA范围为 0～32；对于 IPv6 地址前缀的 ROA 信息最大前缀长度的取值范围为 0～128。
【举例】
\# 显示 IPv4 地址前缀的 ROA 简要信息。
<Sysname> display bgp rpki table ipv4 Total number of entries: 4 Status codes: S - stale, U - used Network Mask-range Origin-AS Server Status
1.2.3.4 8-32 100 1.1.1.2 U
5.2.3.4 8-32 100 2.2.2.2 U
6.6.6.6 8-32 100 2.2.2.2 U
7.7.7.7 8-32 20 2.2.2.2 U表1-41 display bgp rpki table 命令显示简要信息描述表字段 描述Total number of entries ROA条目总数网络地址Network Mask-range 掩码范围Origin-AS 路由源AS号Server RPKI服务器的IP地址ROA消息的状态：
Status • U：可正常使用状态
• S：老化状态\# 显示 IPv4 地址前缀的 ROA 详细信息。
<Sysname> display bgp rpki table ipv4 5.2.3.4 min 8 max 32 RPKI ROA entry for 5.2.3.4/8-32 Origin-AS: 100 from 2.2.2.1, used表1-42 display bgp rpki table 命令显示详细信息描述表字段 描述RPKI ROA entry for 5.2.3.4/8-32 IP地址为5.2.3.4、前缀范围为8-32的路由源认证信息

字段 描述路由源信息：
•AS 号
• RPKI 服务器 IP 地址Origin-AS
• ROA 的状态：
used：合法的 ROA (cid:123)
stale：老化的 ROA (cid:123)

##### 1.1.50 display bgp update-group

命令用来显示 打包组的相关信息。
display bgp update-group BGP【命令】
display bgp [ instance instance-name ] update-group ipv4 [ multicast | rtfilter | [ unicast ] [ vpn-instance vpn-instance-name ] ] [ ipv4-address ] display bgp [ instance instance-name ] update-group ipv6 [ multicast | [ unicast ] [ vpn-instance vpn-instance-name ] ] [ ipv6-address ] display bgp [ instance instance-name ] update-group link-state [ ipv4-address | ipv6-address ] display bgp [ instance instance-name ] update-group l2vpn evpn [ ipv4-address ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
instance-name：显示指定 实例的信息。instance-name 表示 实例的名instance BGP BGP称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示 default 实例的信息。
ipv4：显示 BGP IPv4 地址族的打包组信息。
ipv6：显示 BGP IPv6 地址族的打包组信息。
link-state：显示 地址族的打包组信息。
BGP LS l2vpn：显示 地址族的打包组信息。
BGP L2VPN evpn：显示 地址族的打包组信息。
BGP EVPN multicast：显示 组播地址族的打包组信息。
BGP rtfilter：显示 BGP IPv4 RT-Filter 地址族的打包组信息。
unicast：显示 BGP 单播地址族的打包组信息。

vpn-instance-name：显示指定 VPN 实例内的 BGP 打包组相关信息。
vpn-instance表示 的 实例名称，为 1～31 个字符的字符串，区分大vpn-instance-name MPLS L3VPN VPN小写。如果不指定本参数，则显示公网 BGP 打包组相关信息。
ipv4-address：显示指定对等体所在打包组的信息。ipv4-address 为对等体的 IPv4 地址。
ipv6-address：显示指定对等体所在打包组的信息。ipv6-address 为对等体的 IPv6 地址。
【使用指导】
按组打包技术是指将出口策略相同的对等体归为一组，形成一个打包组，设备向打包组中的对等体发布路由时，统一对路由进行策略过滤，并构造路由更新报文（即打包），以避免重复地进行策略过滤和构造报文。
实现按组打包后，每条路由前缀信息只需要经过一次策略过滤并打包一次，然后发布给打包组内的所有对等体。例如，如果不采用按组打包，1000 条路由向 1000 个对等体发布时，需要匹配 1000×1000 次策略，并进行 1000×1000 次打包处理；如果采用按组打包，1000 个对等体的出口策略相同（如数据中心组网中）时，只需要匹配 1000×1 次策略，并进行 1000×1 次打包处理，打包效率提高了 1000 倍。
如果没有指定任何参数，则显示指定地址族公网所有 BGP 打包组信息。
如果没有指定 和 参数，则缺省为 unicast。
unicast multicast【举例】
\# 显示 BGP IPv4 单播地址族的所有打包组信息。
<Sysname> display bgp update-group ipv4 Update-group ID: 0 Type: EBGP link 4-byte AS number: Supported Site-of-Origin: Not specified Minimum time between advertisements: 30 seconds OutQ: 0 Members: 1
99.1.1.1表1-43 display bgp update-group 命令显示信息描述表字段 描述打包组ID Update-group ID打包组中对等体的BGP连接类型，取值包括：
• IBGP link：IBGP 连接Type • EBGP link：EBGP 连接
• Confed IBGP link：联盟 IBGP 连接
• Confed EBGP link：联盟 EBGP 连接Label capability: Supported （暂不支持）打包组中的对等体具有交换带标签路由的能力没有为打包组中的对等体使能4字节AS号抑制功能，即打包组中的对4-byte AS number: Supported等体支持4字节AS号为打包组中的对等体使能4字节AS号抑制功能4-byte AS number: Suppressed

字段 描述Fake AS 为打包组中的对等体配置了虚拟的本地自治系统号number向打包组中的对等体发送BGP更新消息时只携带公有AS号，不携带私有AS号取值为Yes时，如果对等体的AS号为私有AS号，则AS号作为打包组Public-AS-Only: Yes的分组条件；如果对等体的AS号为公有AS号，则AS号不作为打包组的分组条件取值为No时，对等体的AS号不作为打包组的分组条件Substitute-AS: Yes 用本地AS号替换AS_PATH属性里打包组中对等体的AS号Site-of-Origin 为打包组中的对等体指定的SoO属性值Minimum time between advertisements:
向打包组中对等体发布同一路由的最小时间间隔，单位为秒number seconds Advertising community: Yes 向打包组中的对等体发布团体属性打包组中的对等体是路由反射器的客户机Route-reflect client: Yes Advertising extended community: Yes 向打包组中的对等体发布扩展团体属性为打包组中的对等体设置了基于AS路径过滤列表的BGP路由出方Export AS-path-ACL向过滤策略为打包组中的对等体设置了基于地址前缀列表的BGP路由出方向过Export prefix list滤策略Export route policy 对发布给打包组中对等体的路由应用了路由策略Export filter-policy 为打包组中的对等体设置了基于ACL的BGP路由出发向过滤策略OutQ 等待发往打包组中对等体的前缀数目Members 打包组中对等体的数目及对等体的地址Nesting VPN 打包组中的对等体使能了嵌套VPN功能Nexthop invariable: Yes 向打包组中的对等体发布路由时不改变下一跳打包组中的对等体为UPE UPE: Yes UPE export route policy 为打包组中的UPE对等体应用了出方向路由策略

##### 1.1.51 domain-distinguisher

domain-distinguisher 命令用来配置 BGP LS 信息的 AS 号和 Router ID。
undo domain-distinguisher 命令用来恢复缺省情况。
【命令】
domain-distinguisher as-number:router-id undo domain-distinguisher【缺省情况】
使用本 BGP 进程的 AS 号和 Router ID。

【视图】
BGP LS 地址族视图【缺省用户角色】
network-admin【参数】
as-number:router-id：LS 信息的 号和 ID。as-number 为 号，取值范围为 1～AS Router AS 4294967295；router-id 用 IP 地址的形式标识。
【举例】
\# 配置 BGP LS 信息的 AS 号为 65009，Router ID 为 1.1.1.1。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family link-state [Sysname-bgp-default-ls] domain-distinguisher 65009:1.1.1.1

##### 1.1.52 ebgp-interface-sensitive

命令用来使能直连 会话快速复位功能。
ebgp-interface-sensitive EBGP命令用来关闭直连 会话快速复位功能。
undo ebgp-interface-sensitive EBGP【命令】
ebgp-interface-sensitive undo ebgp-interface-sensitive【缺省情况】
直连 EBGP 会话快速复位功能处于使能状态。
【视图】
BGP 实例视图【缺省用户角色】
network-admin【使用指导】
如果使能了本功能，则连接直连 对等体的链路 后，本地路由器会立即断开与 对EBGP down EBGP等体的会话，并重新与该对等体建立 EBGP 会话。从而，实现快速发现链路故障，快速重建会话。
如果没有使能本功能，则连接直连 EBGP 对等体的链路 down 后，本地路由器不会立即断开与 EBGP对等体的会话，而是等待会话保持时间（Holdtime）超时后，才断开该会话。没有使能本功能时，链路震荡不会影响 EBGP 会话的状态。
ipv4-address 只有与直连的 EBGP 对等体之间的会话支持本功能。
【举例】
使能直连 会话快速复位功能。
\# EBGP <Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] ebgp-interface-sensitive

##### 1.1.53 fast-reroute route-policy

fast-reroute route-policy 命令用来在当前 BGP 地址族视图下指定快速重路由引用的路由策略。
命令用来恢复缺省情况。
undo fast-reroute route-policy【命令】
fast-reroute route-policy route-policy-name undo fast-reroute route-policy【缺省情况】
快速重路由未引用任何路由策略。
BGP【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图【缺省用户角色】
network-admin【参数】
route-policy-name：路由策略名称，为 1～63 个字符的字符串，区分大小写。
【使用指导】
开启 BGP 快速重路由功能的方法有如下两种：
在 BGP 地址族视图下执行 命令开启当前地址族的 BGP 快速重路由功能。采用这种方法
• pic时，BGP 会为当前地址族的所有 路由自动计算备份下一跳，即只要从不同 对等体BGP BGP学习到了到达同一目的网络的路由，且这些路由不等价，就会生成主备两条路由。
• 在 BGP 地址族视图下执行 fast-reroute route-policy 命令指定快速重路由引用的路由策略，并在引用的路由策略中，通过apply [ ipv6 ] fast-reroute命令指定备份下一跳的地址。采用这种方式时，只有为主路由计算出的backup-nexthop备份下一跳地址与指定的地址相同时，才会为其生成备份下一跳；否则，不会为主路由生成备份下一跳。在引用的路由策略中，还可以配置 if-match 子句，用来决定哪些路由可以进行快速重路由保护，BGP 只会为通过 子句过滤的路由生成备份下一跳。
if-match引用路由策略方式的优先级高于通过 命令开启 BGP 快速重路由方式。
pic【举例】
在 单播地址族下，指定 快速重路由引用的路由策略为 frr-policy。
\# BGP IPv4 BGP <Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 [Sysname-bgp-default-ipv4] fast-reroute route-policy frr-policy

【相关命令】
• apply fast-reroute（三层技术-IP 路由命令参考/路由策略）
• apply ipv6 fast-reroute（三层技术-IP 路由命令参考/路由策略）
• pic
• route-policy（三层技术-IP 路由命令参考/路由策略）

##### 1.1.54 filter-policy export

filter-policy export 命令用来配置对发布的路由信息进行过滤。
命令用来取消对发布的路由信息进行过滤。
undo filter-policy export【命令】
BGP IPv4 单播地址族视图/BGP-VPN IPv4 单播地址族视图/BGP IPv4 组播地址族视图：
filter-policy { ipv4-acl-number | name ipv4-acl-name | prefix-list ipv4-prefix-list-name } export [ direct | { isis | ospf | rip } process-id | static ] undo filter-policy export [ direct | { isis | ospf | rip } process-id | static ] BGP IPv6 单播地址族视图/BGP-VPN IPv6 单播地址族视图/BGP IPv6 组播地址族视图：
filter-policy { ipv6-acl-number | name ipv6-acl-name | prefix-list ipv6-prefix-list-name } export [ direct | { isisv6 | ospfv3 | ripng } process-id | static ] undo filter-policy export [ direct | { isisv6 | ospfv3 | ripng } process-id | static ]【缺省情况】
不对发布的路由信息进行过滤。
【视图】
单播地址族视图BGP IPv4单播地址族视图BGP-VPN IPv4单播地址族视图BGP IPv6 BGP-VPN IPv6 单播地址族视图BGP IPv4 组播地址族视图BGP IPv6 组播地址族视图【缺省用户角色】
network-admin【参数】
ipv4-acl-number：指定用于匹配路由信息目的网络地址的访问列表号，取值范围为 2000～3999。
ipv6-acl-number：指定用于匹配路由信息目的网络地址的 IPv6 ACL 编号，取值范围为 2000～3999。

ipv4-acl-name：指定用于匹配路由信息目的网络地址的访问列表名称，ipv4-acl-name name表示 的名称，为 1～63 个字符的字符串，不区分大小写，必须以英文字母开头。为避免混淆，ACL ACL 的名称不允许使用英文单词 all。
name ipv6-acl-name：指定用于匹配路由信息目的网络地址的访问列表名称，ipv6-acl-name表示 ACL 的名称，为 1～63 个字符的字符串，不区分大小写，必须以英文字母开头。为避免混淆，的名称不允许使用英文单词 all。
ACL ipv4-prefix-list-name：指定用于匹配路由信息目的网络地址的 IPv4 地址前prefix-list缀列表。ipv4-prefix-list-name 表示 IPv4 地址前缀列表名称，为 1～63 个字符的字符串，区分大小写。
prefix-list ipv6-prefix-list-name：指定用于匹配路由信息目的网络地址的 IPv6 地址前缀列表。ipv6-prefix-list-name 表示 IPv6 地址前缀列表名称，为 1～63 个字符的字符串，区分大小写。
direct：对引入的直连路由进行过滤。
isis：对从 ISIS 协议引入的路由进行过滤。
isisv6：对从 IPv6 ISIS 协议引入的路由进行过滤。
ospf：对从 OSPF 协议引入的路由进行过滤。
ospfv3：对从 OSPFv3 协议引入的路由进行过滤。
rip：对从 RIP 协议引入的路由进行过滤。
ripng：对从 RIPng 路由协议引入的路由进行过滤。
static：对引入的静态路由进行过滤。
process-id：路由协议的进程号，取值范围为 1～65535。
【使用指导】
如果指定了路由协议参数（direct、isis 等），则只对从这种协议引入到 BGP 的路由进行过滤，其他 路由不受影响。如果没有指定路由协议参数，则对所有 路由都进行过滤，包括从BGP BGP IGP引入的路由、使用 network 命令发布的路由、从 BGP 对等体学习的路由等。
通过基本 ACL（2000～2999）对发布的路由信息进行过滤时，如果配置了 rule [ rule-id ] { deny | permit } source source-address source-wildcard 命令，则只要路由的目的网络地址与 命令中的 匹配，则该路由与 命令rule source-address source-wildcard rule配置的规则匹配，不会再比较路由的目的网络地址掩码。
通过高级 ACL（3000～3999）对发布的路由信息进行过滤时：
命令
• rule [ rule-id ] { deny | permit } ip source sour-addr sour-wildcard配置的规则用来过滤指定目的网络地址的路由；
• rule [ rule-id ] { deny | permit } ip source sour-addr sour-wildcard destination dest-addr dest-wildcard 命令配置的规则用来过滤指定目的网络地址和掩码的路由。其中 用来过滤路由目的网络地址，source sour-addr sour-wildcard用来过滤路由掩码。destination destination dest-addr dest-wildcard dest-addr dest-wildcard 指定的掩码应该是连续的，如果指定的掩码不连续，则该过滤掩码的条件不生效。

【举例】
\# 在 BGP IPv4 单播地址族视图下，使用编号为 2000 的 IPv4 基本 ACL 对 BGP 发布的所有路由进行过滤。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] filter-policy 2000 export【相关命令】
• filter-policy import
• peer as-path-acl
• peer filter-policy
• peer prefix-list
• peer route-policy

##### 1.1.55 filter-policy import

filter-policy import 命令用来配置对接收的路由信息进行过滤。
undo filter-policy import 命令用来恢复缺省情况。
【命令】
BGP IPv4 单播地址族视图/BGP-VPN IPv4 单播地址族视图/BGP IPv4 组播地址族视图：
filter-policy { ipv4-acl-number | name ipv4-acl-name | prefix-list ipv4-prefix-list-name } import undo filter-policy import BGP IPv6 单播地址族视图/BGP-VPN IPv6 单播地址族视图/BGP IPv6 组播地址族视图：
filter-policy { ipv6-acl-number | name ipv6-acl-name | prefix-list ipv6-prefix-list-name } import undo filter-policy import【缺省情况】
不对接收的路由信息进行过滤。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图组播地址族视图BGP IPv4组播地址族视图BGP IPv6【缺省用户角色】
network-admin

【参数】
ipv4-acl-number：指定用于匹配路由信息目的网络地址的访问列表号，取值范围为 2000～3999。
ipv6-acl-number：指定用于匹配路由信息目的网络地址的 IPv6 访问列表号，取值范围为 2000～3999。
ipv4-acl-name：指定用于匹配路由信息目的网络地址的访问列表名称，ipv4-acl-name name表示 地址 的名称，为 1～63 个字符的字符串，不区分大小写，必须以英文字母开头。为IPv4 ACL避免混淆，ACL 的名称不允许使用英文单词 all。
name ipv6-acl-name：指定用于匹配路由信息目的网络地址的访问列表名称，ipv6-acl-name表示 IPv6 地址 ACL 的名称，为 1～63 个字符的字符串，不区分大小写，必须以英文字母开头。为避免混淆，ACL 的名称不允许使用英文单词 all。
ipv4-prefix-list-name：指定用于匹配路由信息目的网络地址的 IPv4 地址前prefix-list缀列表。prefix-list-name 表示 地址前缀列表名称，为 1～63 个字符的字符串，区分大IPv4小写。
prefix-list ipv6-prefix-list-name：指定用于匹配路由信息目的网络地址的 IPv6 地址前缀列表。ipv6-prefix-name 表示 IPv6 地址前缀列表名称，为 1～63 个字符的字符串，区分大小写。
【使用指导】
通过基本 ACL（2000～2999）对接收的路由信息进行过滤时，如果配置了rule [ rule-id ] { deny | permit } source source-address source-wildcard 命令，则只要路由的目的网络地址与 rule 命令中的 source-address source-wildcard 匹配，则该路由与 rule 命令配置的规则匹配，不会再比较路由的目的网络地址掩码。
通过高级 ACL（3000～3999）对接收的路由信息进行过滤时：
• 命令rule [ rule-id ] { deny | permit } ip source sour-addr sour-wildcard配置的规则用来过滤指定目的网络地址的路由；
• rule [ rule-id ] { deny | permit } ip source sour-addr sour-wildcard destination dest-addr dest-wildcard 命令配置的规则用来过滤指定目的网络地址和掩码的路由。其中 source sour-addr sour-wildcard 用来过滤路由目的网络地址，用来过滤路由掩码。destination destination dest-addr dest-wildcard指定的掩码应该是连续的，如果指定的掩码不连续，则该过dest-addr dest-wildcard滤掩码的条件不生效。
【举例】
\# 在 BGP IPv4 单播地址族视图下，使用编号为 2000 的 IPv4 基本 ACL 对 BGP 接收的路由进行过滤。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] filter-policy 2000 import【相关命令】
•filter-policy export
•peer as-path-acl

• peer filter-policy
•
peer prefix-list
•
peer route-policy

##### 1.1.56 flush suboptimal-route

命令用来开启 BGP 次优路由下刷 RIB 功能。
flush suboptimal-route undo flush suboptimal-route 命令用来关闭 BGP 次优路由下刷 RIB 功能。
【命令】
flush suboptimal-route undo flush suboptimal-route【缺省情况】
次优路由下刷 功能处于关闭状态，即只有 最优路由可以下刷到 RIB。
BGP RIB BGP【视图】
BGP 实例视图【缺省用户角色】
network-admin【使用指导】
开启 BGP 次优路由下刷 RIB 功能后，当 BGP 路由表中最优路由为通过 命令生成或network命令引入的路由，次优路由为从 对等体收到的路由时，次优路由会下刷到import-route BGP RIB 表项中。在某些组网情况下，执行本命令下刷到达同一目的网络次优路由到 RIB 后，当最优路由发生故障时，系统可以快速切换到次优路由。例如，设备有一条到达 1.1.1.0/24 网络的静态路由，其优先级高于 BGP 路由，BGP 本地引入该静态路由同时从对等体收到到达该网段的路由，执行本命令 将从对等体收到的路由做为次优路由下刷到 RIB，这时如果开启协议间的 功能，当BGP FRR静态路由发生故障时，本地引入的静态路由不可达，系统可以快速切换到 BGP 次优路由，从而大大缩短了流量中断时间。
协议间的 FRR 功能的详细介绍，请参见“三层技术-IP 路由配置指导”中的“IP 路由基础”。
【举例】
\# 开启次优路由下刷 RIB 功能。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] flush suboptimal-route

##### 1.1.57 graceful-restart

命令用来使能 BGP 协议的 GR 能力。
graceful-restart命令用来关闭 BGP 协议的 GR 能力。
undo graceful-restart【命令】
graceful-restart undo graceful-restart

【缺省情况】
BGP 协议的 GR 能力处于关闭状态。
【视图】
BGP 实例视图【缺省用户角色】
network-admin【使用指导】
BGP GR（Graceful Restart，平滑重启）是一种在主备倒换或 BGP 协议重启时保证转发业务不中断的机制。
BGP 对等体之间通过 Open 消息交互 GR 能力。只有双方都具有 GR 能力时，建立起的 BGP 会话才具备 GR 能力。
执行本命令后，设备会重新建立 BGP 会话。
【举例】
\# 使能 GR 能力。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] graceful-restart【相关命令】
• graceful-restart timer purge-time
• graceful-restart timer restart
• graceful-restart timer wait-for-rib

##### 1.1.58 graceful-restart timer purge-time

命令用来配置 BGP GR 过程中等待通知 RIB（Routing graceful-restart timer purge-time Information Base，路由信息库）老化失效表项的时间。
命令用来恢复缺省情况。
undo graceful-restart timer purge-time【命令】
graceful-restart timer purge-time timer undo graceful-restart timer purge-time【缺省情况】
BGP GR 过程中等待通知 RIB 老化失效表项的时间为 480 秒。
【视图】
BGP 实例视图【缺省用户角色】
network-admin【参数】
timer ：BGP GR 过程中等待通知 RIB 老化失效表项的时间，取值范围为 1～6000，单位为秒。

【使用指导】
GR Restarter 发生主备倒换或 BGP 协议重启时，会启动 RIB 路由老化定时器，该定时器的值由本命令来配置。如果在 RIB 路由老化定时器超时时没有完成 BGP 路由信息的交互，则 GR Restarter会强制退出 过程，根据已经学习到的 路由信息更新 表项，删除老化的 表项。
GR BGP RIB RIB在配置本命令之前，必须先使能 协议的 能力。
BGP GR路由数量较多时，如果本命令配置的值过小，在 路由老化定时器超时前 和BGP RIB GR Restarter GR Helper 无法完成路由交互，则可能会导致流量中断。请根据实际情况，合理调整 RIB 路由老化定时器的值。
本命令配置的值建议大于 graceful-restart timer wait-for-rib 命令配置的值，小于命令配置的值。
protocol lifetime【举例】
配置 过程中等待通知 老化失效表项的时间为 秒。
\# BGP GR RIB 300 <Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] graceful-restart [Sysname-bgp-default] graceful-restart timer purge-time 300【相关命令】
• graceful-restart
•graceful-restart timer restart
•graceful-restart timer wait-for-rib
• lifetime（三层技术-IP 路由命令参考/IP 路由基础）
protocol

##### 1.1.59 graceful-restart timer restart

命令用来配置对端等待重建 BGP 会话的时间。
graceful-restart timer restart undo graceful-restart timer restart 命令用来恢复缺省情况。
【命令】
graceful-restart timer restart timer undo graceful-restart timer restart【缺省情况】
对端等待重建 会话的时间为 秒。
BGP 150【视图】
BGP 实例视图【缺省用户角色】
network-admin【参数】
timer：对端等待重建 BGP 会话的最大时间，取值范围为 3～600，单位为秒。

【使用指导】
GR Restarter通过 Open消息将本端配置的对端等待重建 BGP会话的最大时间通告给 GR Helper。
GR Helper 发现 GR Restarter 进行主备倒换或 BGP 协议重启后，保留从该 GR Restarter 学习到的路由，并对这些路由进行失效标记。GR 等待 与其重建 会话。如果在Helper GR Restarter BGP GR Restarter 通告的时间内，没有重建 BGP 会话，则删除标记为失效的路由。
在配置本命令之前，必须先使能 BGP 协议的 GR 能力。
执行本命令后，配置的时间不会立即生效，只有重建 BGP 会话后才会生效。
【举例】
\# 配置对端等待重建 BGP 会话的最大时间为 300 秒。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] graceful-restart [Sysname-bgp-default] graceful-restart timer restart 300【相关命令】
• graceful-restart
• graceful-restart timer purge-time
• graceful-restart timer wait-for-rib

##### 1.1.60 graceful-restart timer wait-for-rib

命令用来配置本端等待 标记的时间。
graceful-restart timer wait-for-rib End-Of-RIB命令用来恢复缺省情况。
undo graceful-restart timer wait-for-rib【命令】
graceful-restart timer wait-for-rib timer undo graceful-restart timer wait-for-rib【缺省情况】
本端等待 End-Of-RIB 标记的时间为 600 秒。
【视图】
BGP 实例视图【缺省用户角色】
network-admin【参数】
timer：本端等待 End-Of-RIB 标记的时间，取值范围为 3～3600，单位为秒。
【使用指导】
本端配置的等待 End-Of-RIB 标记的时间不会通告给对端，只用来控制本端路由信息交互的时间，即 GR Restarter 上配置的时间只用来控制 GR Restarter 从 GR Helper 接收路由更新的时间，GR上配置的时间只用来控制 从 接收路由更新的时间。
Helper GR Helper GR Restarter主备倒换或 协议重启完成，并与 重新建立 会话后，GR GR Restarter BGP GR Helper BGP Restarter和 GR Helper 应在本命令指定的时间内收到 End-Of-RIB 标记，即在本命令指定的时间内完成路由

信息的交互。当路由信息的数量较多时，建议将本端等待 End-Of-RIB 标记的时间调大，以保证完成所有路由信息的交互。
通过本命令可以控制路由收敛的速度。本命令配置的值越小，路由收敛速度越快，但可能会导致接收的路由信息不完整。
在配置本命令之前，必须先使能 BGP 协议的 GR 能力。
【举例】
\# 配置本端等待 End-Of-RIB 标记的时间为 100 秒。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] graceful-restart [Sysname-bgp-default] graceful-restart timer wait-for-rib 100【相关命令】
• graceful-restart
• graceful-restart timer purge-time
• graceful-restart timer restart

##### 1.1.61 group

group 命令用来创建一个对等体组。
undo group 命令用来删除指定的对等体组。
【命令】
group group-name [ external | internal ] undo group group-name【缺省情况】
不存在对等体组。
【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。
external：创建 EBGP 对等体组。
internal：创建 对等体组。
IBGP【使用指导】
在大规模 BGP 网络中，对等体的数量很多，其中很多对等体具有相同的策略，在配置时会重复使用一些命令。此时，利用对等体组可以简化配置。

对等体组是具有某些相同属性的对等体的集合。当一个对等体加入对等体组中时，此对等体将获得与所在对等体组相同的配置。当对等体组的配置改变时，组内成员的配置也相应改变。
如果没有指定 和 参数，则创建的是 对等体组。
internal external IBGP如果分别对对等体组和对等体组中的对等体进行了某项 配置，则以最后一次配置为准。
BGP通过本命令创建对等体组后，还需要执行 命令，本地路由器才具有与指定对等体组peer enable交换相应地址族路由信息的能力。
【举例】
\# 在 BGP 实例视图下，创建一个 EBGP 对等体组 test，其 AS 号为 200，并在 test 中添加 EBGP对等体 10.1.1.1 和 10.1.2.1。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] group test external [Sysname-bgp-default] peer test as-number 200 [Sysname-bgp-default] peer 10.1.1.1 group test [Sysname-bgp-default] peer 10.1.2.1 group test【相关命令】
• display bgp group
• peer enable

##### 1.1.62 ignore all-peers

命令用来禁止与所有对等体/对等体组建立会话。
ignore all-peers命令用来恢复缺省情况。
undo ignore all-peers【命令】
ignore all-peers [ graceful graceful-time { community { community-number | aa:nn } | local-preference preference | med med } * ] undo ignore all-peers【缺省情况】
允许与所有 BGP 对等体/对等体组建立会话。
【视图】
BGP 实例视图【缺省用户角色】
network-admin【参数】
graceful graceful-time：配置 BGP 邻居等待断开的时间，graceful-time 表示邻居等待断开的时间，取值范围为 60～65535。如果不指定本参数，则表示立即断开与指定对等体/对等体组的会话。
}：指定向对等体/对等体组发送路由的团体属性，community { community-number | aa:nn表示团体序号，取值范围为 1～4294967295；aa:nn 表示团体号，aa 和community-number nn

的取值范围为 0～65535。如果不指定本参数，则表示不修改向对等体/对等体组发送路由的团体属性。
preference：指定 路由的本地优先级，取值范围为 0～4294967295。
local-preference BGP该值越大，则优先级越高。如果不指定本参数，则表示不修改路由的本地优先级。
med med：指定路由的 MED 值，取值范围为 0～4294967295。该值越小，则优先级越高。如果不指定本参数，则表示不修改路由的 MED 值。
【使用指导】
由于网络升级维护等原因，需要暂时断开与所有对等体/对等体组的 BGP 会话时，可以通过ignore命令禁止与所有对等体/对等体组建立 会话。当网络恢复后，通过执行all-peers BGP undo ignore all-peers 命令恢复与所有对等体/对等体组的 BGP 会话。这样，网络管理员在网络升级维护过程中，无需删除并重新进行对等体/对等体组相关配置，减少了网络维护的工作量。
如果本设备和对等体/对等体组的会话已经建立，则执行 命令后，会断开本ignore all-peers设备和对等体/对等体组的会话，并且清除所有路由信息。
如果执行 命令时指定 参数，则执行该命令之后，设备会启动等ignore all-peers graceful待邻居关系断开定时器，同时，向所有对等体/对等体组重新发送本设备上全部的路由。这些路由的属性受 ignore all-peers 命令的控制。用户可以通过该命令降低重新发布路由的优先级，使得邻居路由器优选从其他邻居学到的路由，从而避免定时器超时、邻居关系断开时造成流量中断。
如果同时配置本命令和 命令，则针对同一对等体/对等体组，以 命peer ignore peer ignore令的配置为准。
【举例】
\# 在 BGP 实例视图下，配置等待 60 秒之后断开与所有邻居的 BGP 会话，并指定向所有对等体发送路由的团体属性为 1:1，本地优先级为 200。
<Sysname> system-view [Sysname] bgp 1 [Sysname-bgp-default] ignore all-peers graceful 60 community 1:1 local-preference 200【相关命令】
•peer ignore

##### 1.1.63 ignore-first-as

ignore-first-as 命令用来配置不检测 EBGP 路由的第一个 AS 号。
undo ignore-first-as 命令用来恢复缺省情况。
【命令】
ignore-first-as undo ignore-first-as【缺省情况】
从 邻居学到路由后，会检测路由的第一个 号。如果此 号不是 对等体的 号，EBGP AS AS EBGP AS且不是私有 AS 号，则断开与该对等体的 BGP 会话。
【视图】
BGP 实例视图

【缺省用户角色】
network-admin【举例】
\# 配置不检测 EBGP 路由的第一个 AS 号。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] ignore-first-as

##### 1.1.64 import-route

import-route 命令用来将 IGP 路由协议的路由信息引入到 BGP 路由表中，以便通过 BGP 发布引入的路由信息。
命令用来取消引入 IGP 路由协议的路由信息。
undo import-route【命令】
单播地址族视图/BGP-VPN 单播地址族视图/BGP 组播地址族视图：
BGP IPv4 IPv4 IPv4 import-route { isis | ospf | rip } [ { process-id | all-processes } [ allow-direct | med med-value | route-policy route-policy-name ] * ] import-route { direct | static } [ med med-value | route-policy route-policy-name ] undo import-route { direct | { isis | ospf | rip } [ process-id | all-processes ] | static } BGP IPv6 单播地址族视图/BGP-VPN IPv6 单播地址族视图/BGP IPv6 组播地址族视图：
import-route { isisv6 | ospfv3 | ripng } [ { process-id | all-processes } [ allow-direct | med med-value | route-policy route-policy-name ] * ] import-route { direct | static } [ med med-value | route-policy route-policy-name ] undo import-route { direct | { isisv6 | ospfv3 | ripng } [ process-id | all-processes ] | static }【缺省情况】
BGP 不会引入 IGP 路由协议的路由信息。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图BGP IPv4 组播地址族视图BGP IPv6 组播地址族视图【缺省用户角色】
network-admin

【参数】
direct：引入直连路由。
isis：引入 ISIS 协议的路由。
isisv6：引入 IPv6 ISIS 协议的路由。
ospf：引入 OSPF 协议的路由。
ospfv3：引入 OSPFv3 协议的路由。
rip：引入 RIP 协议的路由。
ripng：引入 RIPng 协议的路由。
static：引入静态路由。
process-id：路由协议的进程号，取值范围为 1～65535，缺省值为 1。对于 路由，当协议IPv4为 isis、ospf 或 rip 时，可以指定该参数；对于 IPv6 路由，当协议为 isisv6、ospfv3 或 ripng时，可以指定该参数。
all-processes：引入指定路由协议所有进程的路由。
allow-direct：指定引入 IGP 路由协议的路由时，同时引入使能了该协议的接口网段路由。如果不指定本参数，则在引入协议路由时不会引入使能了该协议的接口网段路由。当allow-direct与 参数一起使用时，需要注意路由策略中配置的匹配规则route-policy route-policy-name不 要 与 接 口 路 由 信 息 存 在 冲 突 ， 否 则 会 导 致 allow-direct 配 置 失 效 。 例 如 ， 当 配 置参数引入 OSPF 路由时，在路由策略中不要配置 匹配条allow-direct if-match route-type件，否则，allow-direct 参数失效。
med-value：指定引入路由的 度量值，取值范围为 0～4294967295。如果没有指定med MED MED 度量值，则被引入路由的 metric 值将作为引入 BGP 之后路由的 MED 值。
route-policy-name：对引入的路由应用路由策略，以便过滤引入的路由或设route-policy置引入后路由的属性。route-policy-name 表示路由策略名称，为 1～63 个字符的字符串，区分大小写。
【使用指导】
通过 命令引入指定 路由协议的路由时，不会引入该协议的缺省路由。只有同import-route IGP时执行 default-route imported 命令，才会引入该协议的缺省路由。
只能引入路由表中状态为 active 的路由。可以通过 display ip routing-table protocol命令或 display ipv6 routing-table protocol 命令来查看路由的状态是否为 active。
通过 import-route 命令引入到 BGP 路由表中的路由的 ORIGIN 属性为 incomplete。
【举例】
\# 在 BGP IPv4 单播地址族视图下，引入 RIP 进程 1 的路由，并指定引入后 BGP 路由的 MED 值为100。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] import-route rip 1 med 100【相关命令】
protocol（三层技术-IP 路由命令参考/IP 路由基础）
• display ip routing-table

protocol（三层技术-IP 路由命令参考/IP 路由基础）
• display ipv6 routing-table

##### 1.1.65 ip vpn-instance (BGP instance view)

命令用来创建 BGP-VPN 实例，并进入 BGP-VPN 实例视图。如果指定的ip vpn-instance实例已经存在，则直接进入 实例视图。
BGP-VPN BGP-VPN命令用来删除 实例，及该视图下的所有配置。
undo ip vpn-instance BGP-VPN【命令】
ip vpn-instance vpn-instance-name undo ip vpn-instance vpn-instance-name【缺省情况】
不存在 BGP-VPN 实例。
【视图】
BGP 实例视图【缺省用户角色】
network-admin【参数】
vpn-instance-name：VPN 实例名称，为 1～31 个字符的字符串，区分大小写。
【使用指导】
在 BGP-VPN 实例视图下配置 BGP 对等体后，从该对等体学习到的 BGP 路由将被添加到指定 VPN实例的路由表中。
通常在 PE 设备和 MCE 设备上执行本命令及 BGP-VPN 实例视图下的命令，以实现将不同 Site 的路由学习到不同的 VPN 实例，保证 VPN 实例之间路由隔离。
在执行本命令前，必须通过系统视图下的 命令创建 VPN 实例，并通过ip vpn-instance命令配置该 实例的路由标识符。
route-distinguisher VPN【举例】
\# 为 VPN 实例 vpn1 创建 BGP-VPN 实例，并进入 BGP-VPN 实例视图。
<Sysname> system-view [Sysname] ip vpn-instance vpn1 [Sysname-vpn-instance-vpn1] route-distinguisher 100:1 [Sysname-vpn-instance-vpn1] quit [Sysname] bgp 100 [Sysname-bgp-default] ip vpn-instance vpn1 [Sysname-bgp-default-vpn1]【相关命令】
• ip vpn-instance (system-view) （ MCE 命令参考 /MCE ）
route-distinguisher（MCE 命令参考/MCE）
•

##### 1.1.66 log-peer-change

log-peer-change 命令用来全局使能 BGP 日志记录功能。
undo log-peer-change 命令用来全局关闭 BGP 日志记录功能。
【命令】
log-peer-change undo log-peer-change【缺省情况】
全局 BGP 日志记录功能处于开启状态。
【视图】
实例视图BGP【缺省用户角色】
network-admin【使用指导】
通过 log-peer-change 命令全局使能 BGP 日志记录功能，并执行 peer log-change 命令使能与指定对等体/对等体组之间 BGP 会话的日志记录功能后，与该对等体/对等体组之间 BGP 会话建立以及断开时会生成日志信息，通过 命令或display bgp peer ipv4 unicast log-info display bgp peer ipv6 unicast log-info 命令可以查看记录的日志信息。生成的日志信息还将被发送到设备的信息中心，通过设置信息中心的参数，决定日志信息的输出规则（即是否允许输出以及输出方向）。（有关信息中心参数的配置请参见“网络管理和监控配置指导”中的“信息中心”。）
如果全局关闭 BGP 日志记录功能，或关闭与指定对等体/对等体组之间 BGP 会话的日志记录功能，则 BGP 会话建立或断开时不会生成日志信息。
【举例】
\# 全局使能 BGP 日志记录功能。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] log-peer-change【相关命令】
• display bgp peer
• peer log-change

##### 1.1.67 log-route-flap

命令用来使能 BGP 的路由抖动日志记录功能。
log-route-flap命令用来恢复缺省情况。
undo log-route-flap【命令】
log-route-flap monitor-time monitor-count [ log-count-limit | route-policy route-policy-name ] *

undo log-route-flap【缺省情况】
的路由抖动日志记录功能处于关闭状态。
BGP【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图组播地址族视图BGP IPv4组播地址族视图BGP IPv6【缺省用户角色】
network-admin【参数】
monitor-time：输出路由抖动日志的监控周期，取值范围为 1～600，单位为分钟。
monitor-count：在监控周期内触发输出日志的路由抖动次数门限，取值范围为 2～8。
log-count-limit：一分钟内最大允许输出的路由抖动日志条数，取值范围为 1～600，缺省值为 200。
route-policy-name：通过路由策略指定对哪些路由进行路由抖动跟踪。
route-policy表示路由策略名称，为 1～63 个字符的字符串，区分大小写。
route-policy-name【使用指导】
使能 BGP 的路由抖动日志记录功能后，当路由发生抖动并满足日志输出条件时会生成路由抖动日志信息。生成的日志信息还将被发送到设备的信息中心，通过设置信息中心的参数，决定日志信息的输出规则（即是否允许输出以及输出方向）。（有关信息中心参数的配置请参见“网络管理和监控配置指导”中的“信息中心”。）
本命令只对配置所在地址族下来自 邻居的路由生效。
BGP【举例】
\# 在 BGP IPv4 单播地址族视图下，使能路由抖动日志记录功能，设置监控周期为 10 分钟，路由抖动次数门限值为 5 次，一分钟内最大允许输出的路由抖动日志条数为 100。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] log-route-flap 10 5 100

##### 1.1.68 network

命令用来配置 发布的本地网段路由，即将本地路由表中指定网段的路由添加到network BGP BGP路由表中，并发布给对等体。
undo network 命令用来删除指定的 BGP 发布的本地网段路由。

【命令】
BGP IPv4 单播地址族视图/BGP-VPN IPv4 单播地址族视图/BGP IPv4 组播地址族视图：
network ipv4-address [ mask-length | mask ] [ route-policy route-policy-name ] undo network ipv4-address [ mask-length | mask ] BGP IPv6 单播地址族视图/BGP-VPN IPv6 单播地址族视图/BGP IPv6 组播地址族视图：
network ipv6-address prefix-length [ route-policy route-policy-name ] undo network ipv6-address prefix-length【缺省情况】
BGP 不发布本地的网段路由。
【视图】
单播地址族视图BGP IPv4单播地址族视图BGP-VPN IPv4 BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图BGP IPv4 组播地址族视图BGP IPv6 组播地址族视图【缺省用户角色】
network-admin【参数】
ipv4-address：目的网络的 IPv4 地址。如果没有指定 mask 和 mask-length 参数，则采用自然掩码。
mask-length：网络掩码长度，取值范围为 0～32。
mask：网络掩码，点分十进制格式。
ipv6-address：目的网络的 IPv6 地址。
prefix-length：目的网络地址的前缀长度，取值范围为 0～128。
route-policy route-policy-name：为指定网段的路由应用路由策略，通过路由策略设置路由属性或过滤路由。route-policy-name 表示路由策略名称，为 1～63 个字符的字符串，区分大小写。
【使用指导】
命令指定的网段路由必须存在于本地的 路由表中，且处于 状态，否则无法将该network IP Active网段路由添加到 BGP 路由表中。
使用 network 命令添加到 BGP 路由表中的网段路由的 ORIGIN 属性为 IGP。
执行 undo network 命令时指定的掩码、掩码长度或前缀长度必须与执行 network 命令时指定的掩码、掩码长度或前缀长度相同，否则无法删除配置。

【举例】
\# 在 BGP IPv4 单播地址族视图下，将本地路由表中到达 10.0.0.0/16 网段的路由添加到 BGP 路由表中。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] network 10.0.0.0 255.255.0.0

##### 1.1.69 network short-cut

network short-cut 命令用来提高接收到的指定 EBGP 路由的路由优先级，该 EBGP 路由称为Short-cut 路由。
undo network short-cut 命令用来取消该配置。
【命令】
BGP IPv4 单播地址族视图/BGP-VPN IPv4 单播地址族视图/BGP IPv4 组播地址族视图：
network ipv4-address [ mask-length | mask ] short-cut undo network ipv4-address [ mask-length | mask ] short-cut BGP IPv6 单播地址族视图/BGP-VPN IPv6 单播地址族视图/BGP IPv6 组播地址族视图：
network ipv6-address prefix-length short-cut undo network ipv6-address prefix-length short-cut【缺省情况】
接收到的 EBGP 路由的路由优先级为 255。
【视图】
单播地址族视图BGP IPv4单播地址族视图BGP-VPN IPv4 BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图BGP IPv4 组播地址族视图BGP IPv6 组播地址族视图【缺省用户角色】
network-admin【参数】
ipv4-address：目的网络的 IPv4 地址。如果没有指定 mask 和 mask-length 参数，则采用自然掩码。
mask-length：网络掩码长度，取值范围为 0～32。
mask ：网络掩码，点分十进制格式。
ipv6-address：目的网络的 IPv6 地址。
prefix-length：目的网络地址的前缀长度，取值范围为 0～128。

【使用指导】
对于相同的目的地，不同的路由协议、直连路由和静态路由可能会发现不同的路由，但这些路由并不都是最优的。为了判断最优路由，各路由协议、直连路由和静态路由都被赋予了一个优先级，具有较高优先级的路由协议发现的路由将成为最优路由。
缺省情况下，EBGP 路由的优先级低于本地产生的 路由的优先级。设备上存在到达某一目的BGP网络的 EBGP路由和本地产生的 BGP路由时，不会选择 EBGP路由。通过执行 network shortcut命令，可以使得指定 EBGP 路由的优先级与本地产生的 BGP 路由的优先级相同，从而提高该 EBGP路由成为最佳路由的可能性。
用户可以通过 命令修改 EBGP 路由和本地产生的 BGP 路由的优先级。
preference【举例】
在 单播地址族视图下，配置提高 路由 的路由优先级。
\# BGP IPv4 EBGP 10.0.0.0/16 <Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] network 10.0.0.0 255.255.0.0 short-cut【相关命令】
• preference

##### 1.1.70 non-stop-routing

命令用来开启 BGP NSR 功能。
non-stop-routing命令用来关闭 BGP NSR 功能。
undo non-stop-routing【命令】
non-stop-routing undo non-stop-routing【缺省情况】
BGP NSR 功能处于关闭状态。
【视图】
BGP 实例视图【缺省用户角色】
network-admin【使用指导】
BGP NSR（Nonstop Routing，不间断路由）是一种通过在 BGP 协议主备进程之间备份必要的协议状态和数据（如 BGP 邻居信息和路由信息），使得 BGP 协议的主进程中断时，备份进程能够无缝地接管主进程的工作，从而确保对等体感知不到 BGP 协议中断，保持 BGP 路由，并保证转发不会中断的技术。
【举例】
开启 功能。
\# BGP NSR <Sysname> system-view

[Sysname] bgp 100 [Sysname-bgp-default] non-stop-routing【相关命令】
• display bgp non-stop-routing status

##### 1.1.71 passwords

passwords 命令用来指定与 RPKI 服务器连接的 MD5 认证密码。
undo passwords 命令用来恢复缺省情况。
【命令】
passwords { cipher | simple } string undo passwords【缺省情况】
未配置与 RPKI 服务器连接的 MD5 认证密码。
【视图】
服务器视图BGP RPKI【缺省用户角色】
network-admin【参数】
cipher：以密文方式设置密钥。
simple：以明文方式设置密钥，该密钥将以密文形式存储。
string：密钥字符串，区分大小写。密文密钥为 33～137 个字符的字符串，明文密钥为 1～80 个字符的字符串。
【使用指导】
与 RPKI 服务器连接使用 MD5 认证密码，可以在以下两方面提高 BGP 的安全性：
与 RPKI 服务器建立 TCP 连接时进行 MD5 认证，只有服务器和客户端的密钥相同时，才能建
•立 连接，从而避免与非法的服务器建立 连接。
TCP TCP传递 报文时，对 报文进行 运算，从而保证 报文不会
• BGP RPKI BGP RPKI MD5 BGP RPKI被篡改。
【举例】
\# 在 BGP RPKI 服务器视图下，指定与 RPKI 服务器连接的 MD5 认证密码为 123456。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] rpki [Sysname-bgp-default-rpki] server tcp 1.1.1.1 [Sysname-bgp-default-rpki-server] passwords simple 123456

##### 1.1.72 peer additional-paths

命令用来配置 Add-Path 功能。
peer additional-paths

命令用来取消该配置。
undo peer additional-paths【命令】
单播地址族视图/BGP-VPN 单播地址族视图：
BGP IPv4 IPv4 peer { group-name | ipv4-address [ mask-length ] } additional-paths { receive | send } * undo peer { group-name | ipv4-address [ mask-length ] } additional-paths { receive | send } * BGP IPv6 单播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } additional-paths { receive | send } * undo peer { group-name | ipv6-address [ prefix-length ] } additional-paths { receive | send } *单播地址族视图：
BGP-VPN IPv6 peer { group-name | ipv6-address [ prefix-length ] } additional-paths { receive | send } * undo peer { group-name | ipv6-address [ prefix-length ] } additional-paths { receive | send } *【缺省情况】
未配置 Add-Path 功能。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
receive：接收能力。
send：发送能力。

【使用指导】
Add-Path 能力包括接收和发送两种。为了让对等体间的 Add-Path 能力协商成功，必须一端使能接收能力，另一端使能发送能力。
【举例】
在 单播地址族视图下，使能与对等体 的 接收能力。
\# BGP IPv4 1.1.1.1 Add-Path <Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] peer 1.1.1.1 additional-paths receive

##### 1.1.73 peer advertise additional-paths best

peer advertise additional-paths best 命令用来配置向指定对等体/对等体组发送的Add-Path 优选路由的最大条数。
命令用来取消该配置。
undo peer advertise additional-paths best【命令】
单播地址族视图/BGP-VPN 单播地址族视图：
BGP IPv4 IPv4 peer { group-name | ipv4-address [ mask-length ] } advertise additional-paths best number undo peer { group-name | ipv4-address [ mask-length ] } advertise additional-paths best BGP IPv6 单播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } advertise additional-paths best number undo peer { group-name | ipv6-address [ prefix-length ] } advertise additional-paths best BGP-VPN IPv6 单播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } advertise additional-paths best number undo peer { group-name | ipv6-address [ prefix-length ] } advertise additional-paths best【缺省情况】
向指定对等体/对等体组发送的 Add-Path 优选路由的最大条数为 1。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图【缺省用户角色】
network-admin

【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 地址。指定的对等体必须已经创建。
IPv6 prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
number：发送 优选路由的数量，取值范围为 2～32。
Add-Path【使用指导】
当发送的 Add-Path 优选路由的条数大于本地实际优选的路由条数时，以本地实际优选的路由条数为准。
【举例】
\#在 BGP IPv4 单播地址族视图下，配置向对等体 1.1.1.1 发送 Add-Path 优选路由的最大条数为 3。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] peer 1.1.1.1 advertise additional-paths best 3【相关命令】
•additional-paths select-best
• peer additional-paths

##### 1.1.74 peer advertise origin-as-validation

peer advertise origin-as-validation 命令用来配置向对等体/对等体组发送 BGP RPKI验证结果。
命令用来恢复缺省情况。
undo peer advertise origin-as-validation【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } advertise origin-as-validation undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } advertise origin-as-validation【缺省情况】
不会向对等体/对等体组发送 BGP RPKI 验证结果。
【视图】
单播地址族视图BGP IPv4单播地址族视图BGP-VPN IPv4单播地址族视图BGP IPv6

BGP-VPN IPv6 单播地址族视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
【使用指导】
源 AS 验证结果以扩展团体属性的方式传递，要使本配置生效，请先配置向对等体/对等体组发布扩展团体属性。
目前，设备仅支持向 IBGP 对等体/对等体组发送 BGP RPKI 验证结果。
【举例】
\# 在 BGP IPv4 单播地址族视图下，配置允许向对等体组 test 发送 BGP RPKI 验证结果。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] peer test advertise-ext-community [Sysname-bgp-default-ipv4] peer test advertise origin-as-validation

##### 1.1.75 peer advertise-community

命令用来配置向对等体/对等体组发布团体属性。
peer advertise-community命令用来取消向对等体/对等体组发布团体属性。
undo peer advertise-community【命令】
单播地址族视图/BGP-VPN 单播地址族视图/BGP 地址族视图/BGP 组播BGP IPv4 IPv4 EVPN IPv4地址族视图：
peer { group-name | ipv4-address [ mask-length ] } advertise-community undo peer { group-name | ipv4-address [ mask-length ] } advertise-community BGP IPv6 单播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } advertise-community undo peer { group-name | ipv6-address [ prefix-length ] } advertise-community组播地址族视图/BGP-VPN 单播地址族视图：
BGP IPv6 IPv6 peer { group-name | ipv6-address [ prefix-length ] } advertise-community undo peer { group-name | ipv6-address [ prefix-length ] } advertise-community

【缺省情况】
不向对等体/对等体组发布团体属性。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图BGP EVPN 地址族视图BGP IPv4 组播地址族视图BGP IPv6 组播地址族视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 地址。指定的对等体必须已经创建。
IPv4 mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
【使用指导】
团体属性是跟随路由一起发送出去的一组特殊数据。根据需要，一条路由可以携带一个或多个团体属性值（每个团体属性值用一个四字节的整数表示）。接收到该路由的路由器就可以根据团体属性值对路由作出适当的处理（比如决定是否发布该路由、在什么范围发布等），从而能够简化路由策略的应用和降低维护管理的难度。
执行 peer advertise-community 命令后，本地路由器向对等体/对等体组发布的路由中将可以携带团体属性；执行 命令后，如果接收到的路由中携带团undo peer advertise-community体属性，则本地路由器删除该团体属性后，再将路由发布给对等体/对等体组。
【举例】
\# 在 BGP IPv4 单播地址族视图下，配置允许向对等体组 test 发布团体属性。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] peer test advertise-community【相关命令】
• apply community（三层技术-IP 路由命令参考/路由策略）
• if-match community（三层技术-IP 路由命令参考/路由策略）

community-list（三层技术-IP 路由命令参考/路由策略）
• ip

##### 1.1.76 peer advertise-ext-community

命令用来配置向对等体/对等体组发布扩展团体属性。
peer advertise-ext-community命令用来取消向对等体/对等体组发布扩展团体属性。
undo peer advertise-ext-community【命令】
单播地址族视图/BGP-VPN 单播地址族视图/BGP 组播地址族视图：
BGP IPv4 IPv4 IPv4 peer { group-name | ipv4-address [ mask-length ] } advertise-ext-community undo peer { group-name | ipv4-address [ mask-length ] } advertise-ext-community单播地址族视图：
BGP IPv6 peer { group-name | ipv6-address [ prefix-length ] } advertise-ext-community undo peer { group-name | ipv6-address [ prefix-length ] } advertise-ext-community BGP-VPN IPv6 单播地址族视图/BGP IPv6 组播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } advertise-ext-community undo peer { group-name | ipv6-address [ prefix-length ] } advertise-ext-community【缺省情况】
不向对等体/对等体组发布扩展团体属性。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图BGP IPv4 组播地址族视图BGP IPv6 组播地址族视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。

prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
【使用指导】
随着团体属性的应用日益广泛，原有四字节的团体属性无法满足用户的需求。因此，BGP 定义了新的路由属性——扩展团体属性。扩展团体属性与团体属性有如下不同：
• 扩展团体属性为八字节，提供了更多的属性值。
• 扩展团体属性可以划分类型。在不同的组网应用中，可以使用不同类型的扩展团体属性对路由进行过滤和控制。与不区分类型、统一使用同一个属性值空间的团体属性相比，扩展团体属性的配置和管理更为简单。
执行 命令后，本地路由器向对等体/对等体组发布的路由中peer advertise-ext-community将可以携带扩展团体属性；执行 undo peer advertise-ext-community 命令后，如果接收到的路由中携带扩展团体属性，则本地路由器删除该扩展团体属性后，再将路由发布给对等体/对等体组。
【举例】
\# 在 BGP IPv4 单播地址族视图下，配置允许向对等体组 test 发布扩展团体属性。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] peer test advertise-ext-community【相关命令】
extcommunity（三层技术-IP 路由命令参考/路由策略）
• apply extcommunity（三层技术-IP 路由命令参考/路由策略）
• if-match extcommunity-list（三层技术-IP 路由命令参考/路由策略）
• ip

##### 1.1.77 peer allow-as-loop

命令用来配置对于从对等体/对等体组接收的路由，允许本地 AS 号在接收peer allow-as-loop路由的 属性中出现，并配置允许出现的次数。
AS_PATH命令用来取消该配置。
undo peer allow-as-loop【命令】
BGP IPv4 单播地址族视图/BGP-VPN IPv4 单播地址族视图/BGP EVPN 地址族视图/BGP IPv4 组播地址族视图：
peer { group-name | ipv4-address [ mask-length ] } allow-as-loop [ number ] undo peer { group-name | ipv4-address [ mask-length ] } allow-as-loop BGP IPv6 单播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } allow-as-loop [ number ] undo peer { group-name | ipv6-address [ prefix-length ] } a llow-as-loop BGP-VPN IPv6 单播地址族视图/BGP IPv6 组播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } allow-as-loop [ number ] undo peer { group-name | ipv6-address [ prefix-length ] } allow-as-loop

【缺省情况】
不允许本地 AS 号在接收路由的 AS_PATH 属性中出现。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图BGP EVPN 地址族视图BGP IPv4 组播地址族视图BGP IPv6 组播地址族视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 地址。指定的对等体必须已经创建。
IPv4 mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
number：允许本地 AS 号出现的次数，取值范围为 1～10，缺省值为 1。如果本地 AS 号出现的次数大于此值，则认为出现环路，丢弃该路由。
【使用指导】
缺省情况下，BGP 不会接受 属性中已包含本地 号的路由，以避免形成路由环路。但AS_PATH AS是，在某些特殊的组网环境下，需要允许本地 AS 号在接收路由的 AS_PATH 属性中出现，否则无法正确发布路由。
【举例】
\# 在 BGP IPv4 单播地址族视图下，配置从对等体组 test 接收路由时，允许本地 AS 号在接收路由的 属性中出现，允许出现次数为 次。
AS_PATH 2 <Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] peer test allow-as-loop 2

##### 1.1.78 peer as-number (for a BGP peer group)

命令用来指定对等体组的 AS 号。
peer as-number undo peer as-number 命令用来删除指定对等体组的 AS 号。

【命令】
peer group-name as-number as-number undo peer group-name as-number【缺省情况】
未指定对等体组的 AS 号。
【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
as-number：对等体组的 AS 号，取值范围为 1～4294967295。
【使用指导】
只有当对等体组中不包含对等体时，才允许为对等体组配置 AS 号。
为对等体组配置 AS 号后，需要加入该对等体组的对等体的 AS 号必须与对等体组的 AS 号相同。
如果没有指定对等体组的 AS 号，则加入该对等体组的对等体保留自己的 AS 号，即对等体组中对等体的 号可以相同，也可以不同。
AS【举例】
\# 在 BGP 实例视图下，指定对等体组 test 的 AS 号为 100。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer test as-number 100【相关命令】
• peer group

##### 1.1.79 peer as-number (for a BGP peer)

peer as-number 命令用来创建 BGP 对等体，并指定对等体的 AS 号。
undo peer 命令用来删除指定的 BGP 对等体。
【命令】
peer { ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } as-number as-number undo peer { ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] }【缺省情况】
不存在 对等体。
BGP

【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
ipv4-address：对等体的 IPv4 地址。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 地址。
IPv6 prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
as-number：对等体的 AS 号，取值范围为 1～4294967295。如果对等体的 AS 号与本地路由器的AS 号相同，则该对等体为 IBGP 对等体；如果对等体的 AS 号与本地路由器的 AS 号不同，则该对等体为 EBGP 对等体。
【使用指导】
除了本命令外，还可以通过 命令创建对等体。执行 命令创建对等体的peer group peer group同时，还可以将对等体加入对等体组。
不能通过重复执行 peer as-number 命令修改对等体的 AS 号。只能先删除对等体，再为对等体配置新的 AS 号。
通过本命令创建对等体后，还需要执行 peer enable 命令，本地路由器才具有与指定对等体交换相应地址族路由信息的能力。
配置动态对等体时，设备和邻居只能有一端配置网段地址，另一端必须配置实际 IP 地址。
【举例】
在 实例视图下，创建 对等体 1.1.1.1，指定对等体的 号为 100。
\# BGP BGP AS <Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer 1.1.1.1 as-number 100【相关命令】
• display bgp peer
• peer enable
• peer group

##### 1.1.80 peer as-path-acl

命令用来为对等体/对等体组设置基于 路径过滤列表的 路由过滤策peer as-path-acl AS BGP略。
undo peer as-path-acl 命令用来删除为指定对等体/对等体组设置的基于 AS 路径过滤列表的BGP 路由过滤策略。

【命令】
BGP IPv4 单播地址族视图/BGP-VPN IPv4 单播地址族视图/BGP IPv4 组播地址族视图：
peer { group-name | ipv4-address [ mask-length ] } as-path-acl as-path-acl-number { export | import } undo peer { group-name | ipv4-address [ mask-length ] } as-path-acl [ as-path-acl-number ] { export | import } BGP IPv6 单播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } as-path-acl as-path-acl-number { export | import } undo peer { group-name | ipv6-address [ prefix-length ] } as-path-acl [ as-path-acl-number ] { export | import } BGP-VPN IPv6 单播地址族视图/BGP IPv6 组播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } as-path-acl as-path-acl-number { export | import } undo peer { group-name | ipv6-address [ prefix-length ] } as-path-acl [ as-path-acl-number ] { export | import }【缺省情况】
未配置基于 路径过滤列表的 路由过滤策略。
AS BGP【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图单播地址族视图BGP IPv6单播地址族视图BGP-VPN IPv6组播地址族视图BGP IPv4组播地址族视图BGP IPv6【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0 ～ 128 。如果指定本参数，则表示指定网段内的动态对等体。
as-path-acl-number：AS 路径过滤列表号，取值范围为 1～256。
export：对向指定对等体/对等体组发布的路由应用过滤策略。

import：对从指定对等体/对等体组接收的路由应用过滤策略。
【使用指导】
配置 命令时需要同时在系统视图下通过 命令配置对应的peer as-path-acl ip as-path AS路径过滤列表。如果本命令中指定的 AS 路径过滤列表尚未创建，则所有路由均通过过滤。
【举例】
\# 在 BGP IPv4 单播地址族视图下，配置利用编号为 1 的 AS 路径过滤列表过滤向对等体组 test 发布的路由。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] peer test as-path-acl 1 export【相关命令】
•filter-policy export
•filter-policy import
• as-path（三层技术-IP 路由命令参考/路由策略）
ip
• peer filter-policy
• peer prefix-list
• peer route-policy

##### 1.1.81 peer bfd

peer bfd 命令用来配置通过 BFD 检测本地路由器和指定 BGP 对等体/对等体组之间的链路。
undo peer bfd 命令用来取消该配置。
【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } bfd [ multi-hop | single-hop ] undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } bfd【缺省情况】
不使用 BFD 检测本地路由器和 BGP 对等体/对等体组之间的链路。
【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address ：对等体的 IPv4 地址。指定的对等体必须已经创建。

mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 地址。指定的对等体必须已经创建。
IPv6 prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
multi-hop：采用 BFD 多跳检测方式。
single-hop：采用 BFD 单跳检测方式。
【使用指导】
如果没有指定 multi-hop 和 single-hop 参数，则：
• 采用 BFD 多跳方式检测本地路由器和指定 IBGP 对等体/对等体组之间的链路。
• 如果采用直连的物理接口建立 EBGP 会话，且未配置 peer ebgp-max-hop 命令，则采用BFD 单跳方式检测本地路由器和指定 EBGP 对等体/对等体组之间的链路；否则，采用 BFD多跳方式检测。
BFD 多跳和单跳检测方式的详细介绍，请参见“可靠性配置指导”中的“BFD”。
配置 BGP GR 功能后，请慎用 BGP 与 BFD 联动功能。因为当链路故障时，系统可能还没来得及启用 处理流程，BFD 已经检测到链路故障，从而导致 失败。如果设备上同时配置了GR GR BGP GR和 BGP BFD，则在 BGP GR 期间请勿去使能 BGP BFD，否则可能导致 GR 失败。
本地路由器和 BGP 对等体采用的 BFD 检测方式（单跳或多跳）必须相同，否则无法建立 BFD 会话。
【举例】
\# 在 BGP 实例视图下，配置通过 BFD 检测本地路由器和 BGP 对等体组 test 之间的链路。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer test bfd【相关命令】
• display bgp peer session（可靠性命令参考/BFD）
• display bfd

##### 1.1.82 peer bmp server

命令用来配置 监控对等体/对等体组。
peer bmp server BMP Server命令用来取消该配置。
undo peer bmp server【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } bmp server server-number-list undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } bmp server【缺省情况】
未配置 BMP Server 监控对等体/对等体组。

【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 地址。指定的对等体必须已经创建。
IP mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
server-number-list：BGP 监控服务器列表，在同一条命令中最多可配置 8 个 BGP 监控服务器，表示方式为 = server-number&<1-8>。其中，server-number server-number-list为 监控服务器，取值范围为 1～8；&<1-8>表示前面的参数可以输入 1～8 次。
BGP【使用指导】
在配置本命令之前，必须通过 bmp server 命令创建 BGP 监控服务器。
对于同一个对等体/对等体组，如果执行多次命令，最后一次配置生效。
【举例】
\# 在 BGP 实例视图下，使能 BMP Server 1 监控对等体 1.1.1.1。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer 1.1.1.1 bmp server 1【相关命令】
•bmp server

##### 1.1.83 peer capability-advertise conventional

peer capability-advertise conventional 命令用来关闭本地路由器与指定对等体/对等体组的 BGP 路由刷新、多协议扩展和 4 字节 AS 号功能。
命令用来使能本地路由器与指定对等体undo peer capability-advertise conventional /对等体组的 路由刷新、多协议扩展和 字节 号功能。
BGP 4 AS【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } capability-advertise conventional undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } capability-advertise conventional

【缺省情况】
BGP 路由刷新、多协议扩展和 4 字节 AS 号功能处于使能状态。
【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
【使用指导】
路由刷新功能是指发送和接收 消息的能力，它用来实现 会话的软复位。
Route-refresh BGP多协议扩展功能是指发送和接收多协议扩展的 消息的能力，它用来实现通过 发布不同Update BGP协议的路由信息，如 IPv6 路由信息。
4 字节 AS 号功能是指设备支持 4 字节的 AS 号，即 AS 号取值占用 4 字节，取值范围为 1～4294967295。
如果同时执行了本命令和 peer capability-advertise route-refresh 命令，最后一次执行的命令生效。
【举例】
在 实例视图下，关闭本地路由器与对等体 的 路由刷新、多协议扩展和 字节\# BGP 1.1.1.1 BGP 4 AS 号功能。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer 1.1.1.1 as-number 100 [Sysname-bgp-default] peer 1.1.1.1 capability-advertise conventional【相关命令】
• display bgp peer
• peer capability-advertise route-refresh

##### 1.1.84 peer capability-advertise orf non-standard

命令用来开启 邻居协商的非标准peer capability-advertise orf non-standard BGP ORF 能力。

命令用来关闭 BGP 邻居协商的非undo peer capability-advertise orf non-standard标准 能力。
ORF【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } capability-advertise orf non-standard undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } capability-advertise orf non-standard【缺省情况】
邻居协商的非标准 能力处于关闭状态。
BGP ORF【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 地址。指定的对等体必须已经创建。
IPv4 mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
【使用指导】
和采用非标准 ORF 的友商设备互通时需要配置本命令。
【举例】
\# 开启邻居 1.1.1.1 的非标准 ORF 能力。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer 1.1.1.1 capability-advertise orf non-standard【相关命令】
• peer capability-advertise orf prefix-list

##### 1.1.85 peer capability-advertise orf prefix-list

命令用来开启 邻居协商的 能力。
peer capability-advertise orf prefix-list BGP ORF命令用来关闭 邻居协商的undo peer capability-advertise orf prefix-list BGP ORF能力。

【命令】
BGP IPv4 单播地址族视图/BGP-VPN IPv4 单播地址族视图/BGP IPv4 组播地址族视图：
peer { group-name | ipv4-address [ mask-length ] } capability-advertise orf prefix-list { both | receive | send } undo peer { group-name | ipv4-address [ mask-length ] } capability-advertise orf prefix-list { both | receive | send } BGP IPv6 单播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } capability-advertise orf prefix-list { both | receive | send } undo peer { group-name | ipv6-address [ prefix-length ] } capability-advertise orf prefix-list { both | receive | send } BGP-VPN IPv6 单播地址族视图/BGP IPv6 组播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } capability-advertise orf prefix-list { both | receive | send } undo peer { group-name | ipv6-address [ prefix-length ] } capability-advertise orf prefix-list { both | receive | send }【缺省情况】
邻居协商的 能力处于关闭状态。
BGP ORF【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图单播地址族视图BGP IPv6单播地址族视图BGP-VPN IPv6组播地址族视图BGP IPv4组播地址族视图BGP IPv6【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0 ～ 128 。如果指定本参数，则表示指定网段内的动态对等体。
both：支持发送和接收携带 信息的 报文。
ORF Route-refresh receive：支持接收携带 信息的 报文。
ORF Route-refresh

send：支持发送携带 ORF 信息的 Route-refresh 报文。
【使用指导】
使能 能力后，本设备和对端会通过 报文进行 能力协商。协商成功后，就能解析对ORF Open ORF端发送的携带了标准 ORF 信息的 Route-refresh 报文或者给对端发送携带标准 ORF 信息的Route-refresh 报 文 。 如 果 要 进 行 非 标 准 ORF 能 力 协 商 ， 还 需 要 配 置 命 令peer non-standard。
capability-advertise orf【举例】
\# 开启对等体 1.1.1.1 的 ORF 能力。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 [Sysname-bgp-default-ipv4] peer 1.1.1.1 capability-advertise orf prefix-list both【相关命令】
• peer capability-advertise orf non-standard

##### 1.1.86 peer capability-advertise route-refresh

命令用来使能本地路由器与指定对等体/对等peer capability-advertise route-refresh体组的 BGP 路由刷新功能。
undo peer capability-advertise route-refresh 命令用来关闭本地路由器与指定对等体/对等体组的 BGP 路由刷新功能。
【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } capability-advertise route-refresh undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } capability-advertise route-refresh【缺省情况】
BGP 路由刷新功能处于使能状态。
【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。

ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
【使用指导】
路由刷新（Route-refresh）功能是指发送和接收 Route-refresh 消息的能力。
路由刷新功能用来实现 BGP 会话的软复位：如果 BGP 的路由策略发生了变化，则本地路由器会向BGP 对等体发送 Route-refresh 消息，收到此消息的对等体将其路由信息重新发给本地路由器，本地路由器根据新的路由策略对接收到的路由信息进行过滤。从而，实现在不中断 BGP 会话的情况下，对 路由表进行更新，使新的路由策略生效。
BGP只有本地路由器和对等体都支持路由刷新功能时，本地路由器和对等体之间建立的 会话才具BGP有路由刷新能力。
如果同时执行了本命令和 peer capability-advertise conventional 命令，最后一次执行的命令生效。
【举例】
\# 在 BGP 实例视图下，使能本地路由器与对等体 1.1.1.1 的 BGP 路由刷新功能。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer 1.1.1.1 as-number 100 [Sysname-bgp-default] peer 1.1.1.1 capability-advertise route-refresh【相关命令】
•display bgp peer
• peer capability-advertise conventional
• peer keep-all-routes
• refresh bgp

##### 1.1.87 peer capability-advertise suppress-4-byte-as

peer capability-advertise suppress-4-byte-as 命令用来使能 4 字节 AS 号抑制功能。
undo peer capability-advertise suppress-4-byte-as 命令用来关闭 4 字节 AS 号抑制功能。
【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } capability-advertise suppress-4-byte-as undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } capability-advertise suppress-4-byte-as【缺省情况】
4 字节 AS 号抑制功能处于关闭状态。
【视图】
实例视图BGP

BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
【使用指导】
设备支持 4 字节的 AS 号，即 AS 号取值占用 4 字节，取值范围为 1～4294967295。缺省情况下，设备在与对端设备建立 BGP 会话时，通过 Open 消息通告对端设备本端支持 4 字节的 AS 号。如果对端设备不支持 4 字节 AS 号（只支持 2 字节 AS 号），则会导致会话协商失败。此时，在本端与对端设备之间使能 字节 号抑制功能，可以使得本端设备通过 消息向对端设备谎称自己不4 AS Open支持 4 字节的 AS 号，从而确保本端和对端设备之间可以成功建立 BGP 会话。
如果对端设备支持 4 字节 AS 号，请不要使能 4 字节 AS 号抑制功能，否则会导致 BGP 会话无法建立。
【举例】
\# 在 BGP 实例视图下，使能本地路由器与对等体 1.1.1.1 的 4 字节 AS 号抑制功能。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer 1.1.1.1 as-number 100 [Sysname-bgp-default] peer 1.1.1.1 capability-advertise suppress-4-byte-as【相关命令】
•display bgp peer

##### 1.1.88 peer connect-interface

peer connect-interface 命令用来指定与对等体/对等体组创建 BGP 会话时建立 TCP 连接使用的源接口，即采用指定源接口的 IPv4 地址/IPv6 地址与对等体/对等体组建立 TCP 连接。
命令用来取消该配置。
undo peer connect-interface【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } connect-interface interface-type interface-number undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } connect-interface

【缺省情况】
BGP 使用到达 BGP 对等体的最佳路由出接口的主 IPv4 地址或 IPv6 地址与对等体/对等体组建立TCP 连接。
【视图】
实例视图BGP实例视图BGP-VPN【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等mask-length体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
interface-number：接口类型和接口编号。
interface-type【使用指导】
本命令的作用与 peer source-address 命令的作用类似：peer source-address 命令直接指定建立 TCP 连接的源地址；本命令通过指定源接口，间接指定建立 TCP 连接的源地址。在一台BGP 路由器上如果同时执行本命令和 命令，则后执行的配置覆盖之前的peer source-address配置。
在如下场合需要通过本命令或 命令指定建立 连接使用的源接口或源peer source-address TCP地址：
• 当指定的对等体的 IPv4 地址/IPv6 地址不是本地路由器与对等体之间直连接口的 IPv4 地址/IPv6 地址时，需要在对等体上通过本配置将建立 TCP 连接使用的源接口指定为对等体 IPv4地址/IPv6 地址所在的接口或者指定 TCP 连接的源地址为对等体 IP 地址/IPv6 地址。
当通过 IPv6 链路本地地址创建对等体或向对等体组中添加指定的对等体时，必须使用直连接
•口建立对等关系，且必须通过 命令将本地直连出接口指定为建peer connect-interface立 TCP 连接使用的源接口。
• 当建立 BGP 连接的路由器之间存在冗余链路时，如果路由器上的一个接口发生故障，链路状态变为 down，建立 TCP 连接的源地址可能会随之发生变化，导致 BGP 需要重新建立 TCP连接，造成网络震荡。为了避免该情况的发生，建议网络管理员将建立 TCP 连接所使用的源地址配置为 Loopback 接口的地址，或将源接口配置为 Loopback 接口，以提高 TCP 连接的可靠性和稳定性。
• 当 BGP 对等体之间同时建立多条 BGP 会话时，如果没有明确指定建立 TCP 连接的源地址，可能会导致根据最优路由选择 TCP 连接源地址错误，并影响 BGP 会话的建立。如果多条 BGP会话基于不同接口的 地址建立，则建议用户在配置 对等体时，通过配置源接口或源IP BGP

地址明确指定每个 BGP 会话的 TCP 连接源地址；如果多条 BGP 会话基于同一接口的不同 IP地址建立，则建议用户通过配置源地址，明确指定每个 会话的 连接源地址。
BGP TCP本地路由器源接口的地址和对等体源接口的地址之间必须路由可达。
对于 邻居，如果通过 命令指定的接口为物理接口，则当该接IBGP peer connect-interface口发生故障、链路状态变为 down 时，IBGP 邻居关系会立即断开，从而加快路由收敛。
如果在 EBGP 对等体上指定非直连接口作为源接口，则需要配置 peer ebgp-max-hop 命令允许本地路由器同非直连网络上的邻居建立 EBGP 连接。
如果接口上存在多个 IPv4 地址，则建立 TCP 连接时使用接口的主 IPv4 地址；如果接口上存在多个IPv6 地址，则设备根据内部定义的原则从中选择一个 IPv6 地址作为 TCP 连接的源地址。源 IPv6地址的选择具有不确定性，因此，在这种情况下，建议用户通过 命令明peer source-address确指定 TCP 连接的源 IPv6 地址。
不能通过本命令指定建立 TCP 连接的源接口为 VT（Virtual Template，虚拟模板）接口，因为 VT口只能作为模板口并不处理相关业务。
【举例】
\# 在 BGP 实例视图下，配置与对等体组 test 创建 BGP 会话时，使用接口 Loopback0 作为建立 TCP连接的源接口。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer test connect-interface loopback 0【相关命令】
• peer ebgp-max-hop
• peer source-address

##### 1.1.89 peer default-route-advertise

peer default-route-advertise 命令用来向对等体/对等体组发送缺省路由。
命令用来取消向指定对等体/对等体组发送缺省路由。
undo peer default-route-advertise【命令】
BGP IPv4 单播地址族视图/BGP-VPN IPv4 单播地址族视图/BGP IPv4 组播地址族视图：
peer { group-name | ipv4-address [ mask-length ] } default-route-advertise [ route-policy route-policy-name ] undo peer { group-name | ipv4-address [ mask-length ] } default-route-advertise BGP IPv6 单播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } default-route-advertise [ route-policy route-policy-name ] undo peer { group-name | ipv6-address [ prefix-length ] } default-route-advertise BGP-VPN IPv6 单播地址族视图/BGP IPv6 组播地址族视图：

peer { group-name | ipv6-address [ prefix-length ] } default-route-advertise [ route-policy route-policy-name ] undo peer { group-name | ipv6-address [ prefix-length ] } default-route-advertise BGP IPv4 RT-Filter 地址族视图：
peer { group-name | ipv4-address [ mask-length ] } default-route-advertise [ route-policy route-policy-name ] undo peer { group-name | ipv4-address [ mask-length ] } default-route-advertise【缺省情况】
不向对等体/对等体组发送缺省路由。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图单播地址族视图BGP-VPN IPv6组播地址族视图BGP IPv4组播地址族视图BGP IPv6地址族视图BGP IPv4 RT-Filter【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
route-policy-name：为发布的缺省路由应用路由策略，以便修改路由的属性route-policy等。route-policy-name 表示路由策略名称，为 1～63 个字符的字符串，区分大小写。如果不指定本参数，则表示没有为发布的缺省路由应用路由策略。
vpn-instance vpn-instance-name：向对等体或对等体组发布指定 VPN 实例的缺省路由。
表示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大vpn-instance-name小写。

【使用指导】
如果配置了 peer default-route-advertise 命令，则本地路由器会向指定的对等体/对等体组发布一条下一跳为自身的缺省路由。在本地路由器的路由表中不需要存在缺省路由。
【举例】
在 单播地址族视图下，设置向对等体组 发布缺省路由。
\# BGP IPv4 test <Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] peer test default-route-advertise

##### 1.1.90 peer description

peer description 命令用来配置对等体/对等体组的描述信息。
undo peer description 命令用来删除指定对等体/对等体组的描述信息。
【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } description text undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } description【缺省情况】
对等体/对等体组没有描述信息。
【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
text：对等体的描述信息，为 1 ～ 79 个字符的字符串，区分大小写。
【举例】
在 实例视图下，配置对等体组 的描述信息为 ISP1。
\# BGP test <Sysname> system-view

[Sysname] bgp 100 [Sysname-bgp-default] peer test description ISP1

##### 1.1.91 peer dscp

命令用来配置 发送协议报文的 优先级。
peer dscp BGP DSCP命令用来取消该配置。
undo peer dscp【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } dscp dscp-value undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } dscp【缺省情况】
发送协议报文的 优先级为 48。
BGP DSCP【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 地址。指定的对等体必须已经创建。
IPv4 mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 地址。指定的对等体必须已经创建。
IPv6 prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
dscp-value：发送的 BGP 报文的 DSCP 优先级，取值范围为 0～63。
【使用指导】
DSCP（Differentiated Services Code Point，差分服务编码点）携带在 IP 报文中的 ToS 字段，用来体现报文自身的优先等级，决定报文传输的优先程度。值越大，DSCP 优先级越高。
【举例】
在 实例视图下，配置 向对等体组 发送协议报文的 优先级为 10。
\# BGP BGP test DSCP <Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer test dscp 10

##### 1.1.92 peer ebgp-max-hop

peer ebgp-max-hop 命令用来配置允许本地路由器同非直连网络上的邻居建立 EBGP 会话，同时指定允许的最大跳数。
命令用来禁止本地路由器同非直连网络上的指定邻居建立 EBGP 会undo peer ebgp-max-hop话的配置。
【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } ebgp-max-hop [ hop-count ] undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } ebgp-max-hop【缺省情况】
不允许同非直连网络上的邻居建立 会话。
EBGP【视图】
BGP 实例视图实例视图BGP-VPN【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 地址。指定的对等体必须已经创建。
IPv6 prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
hop-count：最大路由器跳数，取值范围为 1～255，缺省值为 64。
【使用指导】
当前路由器要与另外一个路由器建立 EBGP 会话，它们之间必须具有直连的物理链路，且必须使用直连接口建立会话。如果不满足这一要求，则必须使用 命令允许它们经过peer ebgp-max-hop多跳建立 会话。
EBGP本命令只对配置改变后收到的路由生效。对于配置改变之前的路由，需要执行 命令refresh bgp重新刷新路由后才能生效。
执行 peer ttl-security 命令后，只要本地设备和指定的对等体通过了 GTSM 检查，就允许在二者之间建立 EBGP 会话，不管二者之间的跳数是否超过 peer ebgp-max-hop 命令指定的跳数范围。

【举例】
\# 在 BGP 实例视图下，配置允许同非直连网络上的 EBGP 对等体组 test 建立会话，允许的最大跳数为缺省值 64。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer test ebgp-max-hop【相关命令】
• peer ttl-security

##### 1.1.93 peer enable

命令用来允许本地路由器与指定对等体/对等体组交换路由信息。
peer enable命令用来禁止本地路由器与指定对等体/对等体组交换路由信息。
undo peer enable【命令】
单播地址族视图/BGP-VPN 单播地址族视图/BGP 地址族视图/BGP 组播BGP IPv4 IPv4 EVPN IPv4地址族视图/BGP IPv4 RT-Filter 地址族视图：
peer { group-name | ipv4-address [ mask-length ] } enable undo peer { group-name | ipv4-address [ mask-length ] } enable BGP IPv6 单播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } enable undo peer { group-name | ipv6-address [ prefix-length ] } enable地址族视图：
BGP LS peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } enable undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } enable BGP-VPN IPv6 单播地址族视图/BGP IPv6 组播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } enable undo peer { group-name | ipv6-address [ prefix-length ] } enable【缺省情况】
本地路由器不能与对等体/对等体组交换路由信息。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP LS 地址族视图BGP-VPN IPv6 单播地址族视图BGP EVPN 地址族视图BGP IPv4 组播地址族视图

BGP IPv6 组播地址族视图BGP IPv4 RT-Filter 地址族视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
【使用指导】
在不同的视图下执行 命令，可以使能本地路由器与指定对等体交换不同地址族路由peer enable信息的能力：
• BGP IPv4 单播地址族视图下，使能的是交换 IPv4 单播路由信息的能力，并且学习到的路由将添加到公网 BGP 路由表中。
• BGP-VPN IPv4 单播地址族视图下，使能的是交换 IPv4 单播路由信息的能力，并且学习到的路由将添加到指定 实例的 路由表中。
VPN BGP BGP IPv6 单播地址族视图下，使能的是交换 IPv6 单播路由信息的能力，并且学习到的路由
•将添加到公网 路由表中。
IPv6 BGP单播地址族视图下，使能的是交换 单播路由信息的能力，并且学习到的
• BGP-VPN IPv6 IPv6路由将添加到指定 VPN 实例的 IPv6 BGP 路由表中。
• BGP IPv4 组播地址族视图下，使能的是交换用于 RPF 检查的 IPv4 单播路由信息的能力。RPF检查的详细介绍，请参见“IP 组播配置指导”中的“组播路由与转发”。
• BGP IPv6 组播地址族视图下，使能的是交换用于 RPF 检查的 IPv6 单播路由信息的能力。RPF检查的详细介绍，请参见“IP 组播配置指导”中的“IPv6 组播路由与转发”。
BGP IPv4 RT-Filter 地址族视图下，使能的是交换 IPv4 RT-Filter 路由信息的能力。MPLS
•组网中，可以在 设备的 地址族视图下执行本命令。
L3VPN PE BGP IPv4 RT-Filter如果在某个视图下执行了 命令，则本地路由器与指定对等体之间不再交换对undo peer enable应地址族的路由信息。
【举例】
\# 在 BGP IPv4 单播地址族视图下，使能本地路由器与对等体 1.1.1.1 交换 IPv4 单播路由信息的能力。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] peer 1.1.1.1 enable

【相关命令】
• display bgp peer

##### 1.1.94 peer fake-as

peer fake-as 命令用来为对等体/对等体组指定一个虚拟的本地自治系统号。
undo peer fake-as 命令用来删除为指定对等体/对等体组配置的虚拟的本地自治系统号。
【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } fake-as as-number undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } fake-as【缺省情况】
对等体/对等体组未配置虚拟的本地自治系统号。
【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
as-number：本地自治系统号，取值范围为 1～4294967295。
【使用指导】
进行系统移植时，例如，Router A 原来位于 AS 2，现在将它移植到 AS 3 里，网络管理员需要在的所有 对等体上修改 的 号。通过在 上为 对等体/对等Router A EBGP Router A AS Router A EBGP体组配置一个虚拟的本地自治系统号 2，可以将本地真实的 AS 号 3 隐藏起来。在 EBGP 对等体看来 Router A 始终位于 AS 2，不需要改变 EBGP 对等体上的配置。
peer fake-as 命令只适用于 EBGP 对等体和对等体组。
如果在本地路由器上执行了 peer fake-as 命令，则在指定的对等体上需要将本地路由器的 AS号配置为本命令中指定的虚拟本地自治系统号。

【举例】
\# 在 BGP 实例视图下，为对等体组 test 指定虚拟的本地自治系统号为 200。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer test fake-as 200

##### 1.1.95 peer filter-policy

peer filter-policy 命令用来为对等体/对等体组设置基于 ACL 的 BGP 路由过滤策略。
undo peer filter-policy 命令用来删除为指定对等体/对等体组设置基于 ACL 的 BGP 路由过滤策略。
【命令】
BGP IPv4 单播地址族视图/BGP-VPN IPv4 单播地址族视图/BGP IPv4 组播地址族视图：
peer { group-name | ipv4-address [ mask-length ] } filter-policy { ipv4-acl-number | name ipv4-acl-name } { export | import } undo peer { group-name | ipv4-address [ mask-length ] } filter-policy [ ipv4-acl-number | name ipv4-acl-name ] { export | import } BGP IPv6 单播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } filter-policy { ipv6-acl-number | name ipv6-acl-name } { export | import } undo peer { group-name | ipv6-address [ prefix-length ] } filter-policy [ ipv4-acl-number | name ipv4-acl-name ] { export | import } BGP-VPN IPv6 单播地址族视图/BGP IPv6 组播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } filter-policy { ipv6-acl-number | name ipv6-acl-name } { export | import } undo peer { group-name | ipv6-address [ prefix-length ] } filter-policy [ ipv4-acl-number | name ipv4-acl-name ] { export | import }【缺省情况】
未配置基于 ACL 的 BGP 路由过滤策略。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图BGP IPv4 组播地址族视图BGP IPv6 组播地址族视图【缺省用户角色】
network-admin

【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 地址。指定的对等体必须已经创建。
IPv6 prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
ipv4-acl-number：访问控制列表号，取值范围为 2000～3999。
ipv4-acl-name：指定用于匹配路由信息目的网络地址的访问列表名称，ipv4-acl-name name表示 ACL 的名称，为 1～63 个字符的字符串，不区分大小写，必须以英文字母开头。为避免混淆，ACL 的名称不允许使用英文单词 all。
ipv6-acl-number：IPv6 访问控制列表号，取值范围为 2000～3999。
name ipv6-acl-name：指定用于匹配路由信息目的网络地址的访问列表名称，ipv6-acl-name表示 ACL 的名称，为 1～63 个字符的字符串，不区分大小写，必须以英文字母开头。为避免混淆，的名称不允许使用英文单词 all。
ACL export：对向指定对等体/对等体组发布的路由应用过滤策略。
import：对从指定对等体/对等体组接收的路由应用过滤策略。
【使用指导】
配置 peer filter-policy 命令时需要同时在系统视图下通过 acl 命令配置对应的 ACL。如果本命令中指定的 ACL 尚未创建，则所有路由均通过过滤。
通过基本 ACL（2000～2999）对 BGP 路由信息进行过滤时，如果配置了 rule [ rule-id ] { deny命令，则只要路由的目的网络地址| permit } source source-address source-wildcard与 命令中的 匹配，则该路由与 命令配置的rule source-address source-wildcard rule规则匹配，不会再比较路由的目的网络地址掩码。
通过高级 ACL（3000～3999）对 BGP 路由信息进行过滤时，rule [ rule-id ] { deny | permit } ip source sour-addr sour-wildcard 命令配置的规则用来过滤指定目的网络地址的路由；
rule [ rule-id ] { deny | permit } ip source sour-add r sour-wildcard命令配置的规则用来过滤指定目的网络地址和掩码destination dest-addr dest-wildcard的路由，其中 source sour-addr sour-wildcard 用来过滤路由目的网络地址，destination用来过滤路由掩码。destination dest-addr dest-wildcard dest-addr dest-wildcard指定的掩码应该是连续的。如果指定的掩码不连续，则该过滤掩码的条件不生效。
【举例】
\# 在 BGP IPv4 单播地址族视图下，配置利用编号为 2000 的访问控制列表过滤向对等体组 test 发布的路由。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] peer test filter-policy 2000 export

【相关命令】
• acl（ACL 和 QoS 命令参考/ACL）
• filter-policy export
• filter-policy import
• peer as-path-acl
• peer prefix-list
• peer route-policy

##### 1.1.96 peer group

命令用来向对等体组中添加指定的对等体。
peer group命令用来从对等体组中删除指定的对等体。
undo peer group【命令】
peer { ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } group group-name [ as-number as-number ] undo peer { ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } group group-name【缺省情况】
对等体组中不存在任何对等体。
【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
ipv4-address：对等体的 IPv4 地址。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
as-number as-number：对等体的 AS 号，取值范围为 1～4294967295。
【使用指导】
可以通过以下方式将对等体加入对等体组：
(1) 先通过 peer as-number 命令创建对等体并指定对等体的 AS 号，再通过 peer group 命令将其加入对等体组。采用这种方式时，需要注意：

执行 命令时可以指定 参数，指定的 参数，必须与
• peer group as-number as-number命令中配置的对等体 号相同。
peer as-number AS如果通过 命令指定了对等体组的 号，则对等体的 号必须与对等体
• peer as-number AS AS组的 AS 号相同，否则无法将对等体加入对等体组。
• 如果将对等体加入 IBGP 对等体组，则该对等体必须是 IBGP 对等体。
(2) 通过 peer group 命令创建对等体的同时，将其加入对等体组。采用这种方式时，需要注意：
• 如果通过 peer as-number 命令指定了对等体组的 AS 号，则执行 peer group 命令时无需指定 as-number 参数，对等体的 AS 号为该对等体组的 AS 号。执行 peer group 命令时如果指定了 参数，则 参数必须与对等体组的 AS 号相同。
as-number as-number
• 如果没有指定对等体组的 AS 号，且该对等体组为 EBGP 对等体组，则执行 命peer group令时必须指定 参数。
as-number如果没有指定对等体组的 号，且该对等体组为 对等体组，则执行 命
• AS IBGP peer group令时无需指定 as-number 参数，对等体的 AS 号为本地 AS 号。执行 peer group 命令时如果指定了 as-number 参数，则 as-number 参数必须与本地 AS 号相同。
如果通过 peer as-number 命令指定了对等体组的 AS 号，则只有与该对等体组 AS 号相同的对等体才能加入该对等体组，即对等体组中所有对等体的 AS 号均相同；如果没有指定对等体组的 AS号，则加入该对等体组的对等体保留自己的 号，即对等体组中对等体的 号可以相同，也可AS AS以不同。
通过本命令将对等体加入对等体组后，还需要执行 peer enable 命令，本地路由器才具有与指定对等体组交换相应地址族路由信息的能力。
【举例】
\# 在 BGP 实例视图下，将 IPv4 地址为 10.1.1.1 的对等体加入到 EBGP 对等体组 test。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] group test external [Sysname-bgp-default] peer 10.1.1.1 group test as-number 2004【相关命令】
•group
• peer as-number
• peer enable

##### 1.1.97 peer ignore

peer ignore 命令用来禁止与指定对等体/对等体组建立会话。
undo peer ignore 命令用来允许与指定的对等体/对等体组建立会话。
【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } ignore [ graceful graceful-time { community { community-number | aa:nn } | local-preference preference | med med } * ] undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } ignore

【缺省情况】
允许与 BGP 对等体/对等体组建立会话。
【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
graceful-time：配置 BGP 邻居等待断开的时间，graceful-time 表示邻居等待graceful断开的时间，取值范围为 60～65535。如果不指定本参数，则表示立即断开与指定对等体/对等体组的会话。
community { community-number | aa:nn }：指定向对等体/对等体组发送路由的团体属性，community-number 表示团体序号，取值范围为 1～4294967295；aa:nn 表示团体号，aa 和 nn的取值范围为 0～65535。如果不指定本参数，则表示不修改向对等体/对等体组发送路由的团体属性preference：指定 路由的本地优先级，取值范围为 0～4294967295。
local-preference BGP该值越大，则优先级越高。如果不指定本参数，则表示不修改路由的本地优先级。
med med：指定路由的 MED 值，取值范围为 0～4294967295。该值越小，则优先级越高。如果不指定本参数，则表示不修改路由的 MED 值。
【使用指导】
由于网络升级维护等原因，需要暂时断开与某个对等体/对等体组的 BGP 会话时，可以通过peer命令禁止与该对等体/对等体组建立会话。当网络恢复后，通过执行ignore undo peer ignore命令恢复与对等体/对等体组的会话。这样，网络管理员无需删除并重新进行对等体/对等体组相关配置，减少了网络维护的工作量。
如果本设备和对等体的会话已经建立，则执行 peer ignore 命令后，会停止该会话，并且清除所有相关路由信息；如果本设备和对等体组的会话已经建立，则执行 命令后，会终止peer ignore与对等体组内所有对等体之间的会话，并且清除所有相关路由信息。
如果执行 命令时指定 参数，则执行该命令之后，设备会启动等待邻居peer ignore graceful关系断开定时器，同时，按照如下规则重新发布路由信息：
• 向指定的对等体/对等体组发送本设备上全部的路由。
• 向其他的 IBGP 对等体/对等体组发送来自指定对等体/对等体组的路由。

这些发布路由的属性受 命令的控制，用户可以通过本命令降低重新发布路由的优先peer ignore级，使得邻居路由器优选从其他邻居学到的路由，从而避免当定时器超时、邻居关系断开时，造成流量的中断。
如果同时配置本命令和 ignore all-peers 命令，则针对同一对等体/对等体组的配置，则以 peer命令执行结果为准。
ignore【举例】
在 实例视图下，禁止与对等体 建立会话。
\# BGP 1.1.1.1 <Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer 1.1.1.1 ignore \# 在 BGP 实例视图下，配置等待 60 秒之后断开与对等体 1.1.1.1 的邻居关系，并指定向对等体发送路由的团体属性为 1:1，本地优先级为 200。
1.1.1.1 <Sysname> system-view [Sysname] bgp 1 [Sysname-bgp-default] peer 1.1.1.1 ignore graceful 60 community 1:1 local-preference 200【相关命令】
• ignore all-peers

##### 1.1.98 peer ignore-originatorid

peer ignore-originatorid 命令用来配置忽略 BGP 路由的 ORIGINATOR_ID 属性。
undo peer ignore-originatorid 命令用来取消该配置。
【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } ignore-originatorid undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } ignore-originatorid【缺省情况】
BGP 路由器不会忽略 BGP 路由的 ORIGINATOR_ID 属性。
【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 地址。指定的对等体必须已经创建。
IPv4 mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。

ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
【使用指导】
请谨慎使用本命令。如果无法确保执行本命令后网络中不会产生环路，请不要执行本命令。
路由反射器从某个对等体接收到路由后，在反射该路由之前为其添加 ORIGINATOR_ID 属性，标识该路由在本 AS 内的起源。ORIGINATOR_ID 属性的值为该对等体的 Router ID。BGP 路由器接收到路由后，将路由中的 ORIGINATOR_ID 属性值与本地的 Router ID 进行比较，如果二者相同则丢弃该路由，从而避免路由环路。
在某些特殊的组网中（如防火墙组网），如果需要接收 属性值与本地ORIGINATOR_ID Router ID相同的路由，则需要执行本命令忽略 BGP 路由的 ORIGINATOR_ID 属性。
执行本命令后，BGP 路由的 CLUSTER_LIST 属性也会被忽略。
【举例】
\# 在 BGP 实例视图下，配置忽略从对等体 1.1.1.1 收到 BGP 路由的 ORIGINATOR_ID 属性。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer 1.1.1.1 ignore-originatorid

##### 1.1.99 peer ipsec-profile

peer ipsec-profile 命令用来为 IPv6 BGP 对等体/对等体组应用 IPsec 安全框架。
undo peer ipsec-profile 命令用来取消为指定的 IPv6 BGP 对等体/对等体组应用 IPsec 安全框架。
【命令】
peer { group-name | ipv6-address [ prefix-length ] } ipsec-profile profile-name undo peer { group-name | ipv6-address [ prefix-length ] } ipsec-profile【缺省情况】
没有为 IPv6 BGP 对等体/对等体组应用 IPsec 安全框架。
【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 ～ 个字符的字符串，区分大小写。指定的对等体组必须已1 47经创建。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。

prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
profile-name：IPsec 安全框架名称，为 1～63 个字符的字符串，区分大小写。
【使用指导】
为了避免路由信息外泄或者非法者对设备进行恶意攻击，可以利用 IPsec 安全隧道对 IPv6 BGP 报文进行保护。通过 IPsec 提供的数据机密性、完整性、数据源认证等功能，确保 IPv6 BGP 报文不会被侦听或恶意篡改，并避免非法者构造 报文对设备进行攻击。
IPv6 BGP在互为 IPv6 BGP 邻居的两台设备上都配置通过 IPsec 保护 IPv6 BGP 报文后，一端设备在发送 IPv6报文时通过 对报文进行加封装，另一端设备接收到报文后，通过 对报文进行解封BGP IPsec IPsec装。如果解封装成功，则接收该报文，正常建立 IPv6 BGP 对等体关系或学习 IPv6 BGP 路由；如果设备接收到不受 IPsec 保护的 IPv6 BGP 报文，或 IPv6 BGP 报文解封装失败，则会丢弃该报文。
配置通过 IPsec 保护 IPv6 BGP 报文包括如下步骤：
(1) 配置 IPsec 安全提议。
(2) 配置手工方式的 IPsec 安全框架。
(3) 通过本命令为 IPv6 BGP 对等体/对等体组应用 IPsec 安全框架。
IPsec 安全提议和 IPsec 安全框架的详细介绍，请参见“安全配置指导”中的“IPsec”。
本命令应用的 IPsec 安全框架必须是手工方式的 IPsec 安全框架。
如果在一台设备上配置了通过 IPsec 保护 IPv6 BGP 报文功能，那么在它的 IPv6 BGP 对等体上也必须配置该功能。否则，会导致 IPv6 BGP 报文无法正常接收。
【举例】
\# 在 BGP 实例视图下，为对等体组 test 应用安全框架 profile001。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer test ipsec-profile profile001【相关命令】
• display bgp group
• display bgp peer

##### 1.1.100 peer keep-all-routes

命令用来保存所有来自指定对等体/对等体组的原始路由更新信息，不peer keep-all-routes管这些路由是否通过了路由策略的过滤。
命令用来取消该配置。
undo peer keep-all-routes【命令】
BGP IPv4 单播地址族视图/BGP-VPN IPv4 单播地址族视图/BGP IPv4 组播地址族视图：
peer { group-name | ipv4-address [ mask-length ] } keep-all-routes undo peer { group-name | ipv4-address [ mask-length ] } keep-all-routes BGP IPv6 单播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } keep-all-routes undo peer { group-name | ipv6-address [ prefix-length ] } keep-all-routes

BGP-VPN IPv6 单播地址族视图/BGP IPv6 组播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } keep-all-routes undo peer { group-name | ipv6-address [ prefix-length ] } keep-all-routes【缺省情况】
不保存来自对等体/对等体组的原始路由更新信息。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图单播地址族视图BGP IPv6单播地址族视图BGP-VPN IPv6组播地址族视图BGP IPv4组播地址族视图BGP IPv6【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
【使用指导】
如果本地路由器和对等体不都支持路由刷新功能，那么要实现 BGP 会话的软复位，则需要通过配置本命令将从对等体/对等体组接收的所有原始路由更新信息保存在本地，当选路策略发生改变后，对保存在本地的所有路由使用新的路由策略重新进行过滤，以实现在不中断 会话的情况下，BGP对 BGP 路由表进行更新，并应用新的选路策略。
【举例】
\# 在 BGP IPv4 单播地址族视图下，保存所有来自对等体 1.1.1.1 的路由更新信息。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] peer 1.1.1.1 keep-all-routes【相关命令】
• peer capability-advertise route-refresh
• refresh bgp

##### 1.1.101 peer keychain

peer keychain 命令用来配置 BGP 对等体/对等体组建立 TCP 连接时的 keychain 认证。
undo peer keychain 命令用来取消指定 BGP 对等体/对等体组建立 TCP 连接时的 keychain 认证。
【命令】
peer { group-name | ip-address [ mask-length ] | ipv6-address [ prefix-length ] } keychain keychain-name undo peer { group-name | ip-address [ mask-length ] | ipv6-address [ prefix-length ] } keychain【缺省情况】
不进行 BGP 的 keychain 认证。
【视图】
实例视图BGP BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ip-address：对等体的 IP 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
keychain-name：keychain 名，为 1～63 个字符的字符串，区分大小写。指定的 必须keychain已经创建。
【使用指导】
配置 keychain 认证可以提高 TCP 连接的安全性。BGP 对等体两端必须都配置 keychain 认证，且配置的 keychain 必须使用相同的认证算法和密码，才能正常建立 TCP 连接，交互 BGP 消息。
对于 keychain 认证算法和 key 的标识符的范围，BGP 的支持情况如下：
• BGP 支持 HMAC-MD5 和 MD5、HMAC-SM3 和 SM3 认证算法，通过命令进行配置。
authentication-algorithm BGP 仅支持标识符取值范围为 0～63 的 key，通过 命令进行配置。
• key命令 和 互斥，不能同时配置。
peer keychain peer password【举例】
在 实例视图下，使 地址为 的对等体使用名为 的 认证。
\# BGP IP 10.1.1.1 abc keychain

<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer 10.1.1.1 as-number 100 [Sysname-bgp-default] peer 10.1.1.1 keychain abc【相关命令】
authentication-algorithm（安全命令参考/keychain）
•
• key（安全命令参考/keychain）

##### 1.1.102 peer log-change

命令用来使能与指定对等体/对等体组之间 BGP 会话的日志记录功能。
peer log-change undo peer log-change 命令用来关闭与指定对等体/对等体组之间 BGP 会话的日志记录功能。
【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } log-change undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } log-change【缺省情况】
与所有对等体/对等体组之间 BGP 会话的日志记录功能均处于开启状态。
【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
【使用指导】
通过 命令全局使能 日志记录功能，并执行本命令后，与指定对等体/对等log-peer-change BGP体组之间 BGP 会话建立以及断开时会生成日志信息，通过 display bgp peer ipv4 unicast命令或 命令可以查看记录的日志log-info display bgp peer ipv6 unicast log-info信息。生成的日志信息还将被发送到设备的信息中心，通过设置信息中心的参数，决定日志信息的

输出规则（即是否允许输出以及输出方向）。（有关信息中心参数的配置请参见“网络管理和监控配置指导”中的“信息中心”。）
如果全局关闭 日志记录功能，或关闭与指定对等体/对等体组之间 会话的日志记录功能，BGP BGP则 BGP 会话建立或断开时不会生成日志信息。
【举例】
\# 在 BGP 实例视图下，使能与对等体 1.1.1.1 之间 BGP 会话的日志记录功能。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer 1.1.1.1 as-number 200 [Sysname-bgp-default] peer 1.1.1.1 log-change【相关命令】
• display bgp peer
• log-peer-change

##### 1.1.103 peer low-memory-exempt

peer low-memory-exempt 命令用来配置系统进入二级内存门限告警状态后，不断开与指定EBGP 对等体/对等体组之间的会话。
undo peer low-memory-exempt 命令用来取消该配置。
【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } low-memory-exempt undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } low-memory-exempt【缺省情况】
系统在二级内存门限告警状态下，会周期性地选择 EBGP 对等体，并断开与该对等体之间的 BGP会话。
【视图】
实例视图BGP实例视图BGP-VPN【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 地址。指定的对等体必须已经创建。
IPv6

prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
【使用指导】
当系统进入二级内存门限告警状态后，BGP 会周期性地选择一个 EBGP 对等体，断开与该对等体之间的 BGP 会话，直到系统内存恢复为止。用户可以通过本命令来避免在二级内存门限告警状态下，断开与指定 对等体/对等体组之间的 会话，以达到对特定 对等体/对等体组EBGP BGP EBGP进行保护的目的。关于内存门限告警的详细介绍，请参见“基础配置指导”中的“设备管理”。
【举例】
\# 在 BGP 实例视图下，配置系统进入二级内存门限告警状态后，不断开与 EBGP 对等体 1.1.1.1 之间的会话。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer 1.1.1.1 as-number 200 [Sysname-bgp-default] peer 1.1.1.1 low-memory-exempt

##### 1.1.104 peer next-hop-local

peer next-hop-local 命令用来配置向对等体/对等体组发布路由时，将下一跳属性修改为自身的地址。
undo peer next-hop-local 命令用来取消该配置。
【命令】
BGP IPv4 单播地址族视图/BGP-VPN IPv4 单播地址族视图/BGP EVPN 地址族视图/BGP IPv4 组播地址族视图：
peer { group-name | ipv4-address [ mask-length ] } next-hop-local undo peer { group-name | ipv4-address [ mask-length ] } next-hop-local BGP IPv6 单播地址族视图/BGP-VPN IPv6 单播地址族视图/BGP IPv6 组播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } next-hop-local undo peer { group-name | ipv6-address [ prefix-length ] } next-hop-local【缺省情况】
向 对等体 对等体组发布的所有路由时，都将下一跳属性修改为自身的地址；对于其他地址EBGP /族的路由，向 IBGP 对等体/对等体组发布 EBGP 路由时，不修改下一跳属性。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图BGP EVPN 地址族视图BGP IPv4 组播地址族视图BGP IPv6 组播地址族视图

【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 地址。指定的对等体必须已经创建。
IPv4 mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 地址。指定的对等体必须已经创建。
IPv6 prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
【使用指导】
缺省情况下，路由器向 IBGP 对等体/对等体组发布路由时，不修改下一跳属性。但有的时候为了保证 IBGP 对等体能够找到下一跳，可以通过本命令将下一跳属性修改为自身的地址。
【举例】
在 单播地址族视图下，配置向对等体组 发布 路由时，将下一跳属性修改为自\# BGP IPv4 test BGP身的地址。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] peer test next-hop-local

##### 1.1.105 peer nexthop-recursive-policy disable

命令用来配置从对等体/对等体组学到的路由不peer nexthop-recursive-policy disable受迭代策略控制。
undo peer nexthop-recursive-policy disable 命令用来取消从对等体/对等体组学到的路由不受迭代策略控制的配置。
【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } nexthop-recursive-policy disable undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } nexthop-recursive-policy disable【缺省情况】
从对等体/对等体组学到的路由受迭代策略控制。
【视图】
BGP 实例视图BGP-VPN 实例视图

【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 地址。指定的对等体必须已经创建。
IPv4 mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 地址。指定的对等体必须已经创建。
IPv6 prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
【使用指导】
通过 protocol nexthop recursive-lookup 命令配置 BGP 路由按照路由策略进行迭代下一跳查找后，可以防止路由变化时的流量丢失，从对等体学到的所有路由都会受迭代策略控制。但在某些组网环境中，不希望来自特定对等体的路由受迭代策略控制（比如直连 EBGP）时，可以配置本命令。
【举例】
\# 在 BGP 实例 default 的 BGP 实例视图下，配置从 BGP 对等体 1.1.1.1 收到的路由不受迭代策略控制。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer 1.1.1.1 as-number 200 [Sysname-bgp-default] peer 1.1.1.1 nexthop-recursive-policy disable【相关命令】
recursive-lookup（三层技术-IP 路由命令参考/IP 路由基础）
• protocol nexthop

##### 1.1.106 peer password

命令用来为指定对等体/对等体组配置 BGP 的 MD5 认证。
peer password命令用来取消为指定对等体/对等体组配置 BGP 的 MD5 认证。
undo peer password【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } password { cipher | simple } password undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } password【缺省情况】
不进行 BGP 的 MD5 认证。
【视图】
实例视图BGP

BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
cipher：以密文方式设置密钥。
simple：以明文方式设置密钥，该密钥将以密文形式存储。
password：密钥字符串，区分大小写。密文密钥为 33～137 个字符的字符串，明文密钥为 1～80个字符的字符串。
【使用指导】
通过为 BGP 对等体配置 BGP 的 MD5 认证，可以在以下两方面提高 BGP 的安全性：
• 为 BGP 建立 TCP 连接时进行 MD5 认证，只有两台路由器配置的密钥相同时，才能建立 TCP连接，从而避免与非法的 BGP 路由器建立 TCP 连接。
• 传递 BGP 报文时，对封装 BGP 报文的 TCP 报文段进行 MD5 运算，从而保证 BGP 报文不会被篡改。
命令 和 互斥，不能同时配置。
peer password peer keychain【举例】
在 实例视图下，配置本地路由器 与对等体 之间的 会话使用\# BGP 10.1.100.1 10.1.100.2 BGP MD5认证，密钥为明文字符串 aabbcc。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer 10.1.100.2 password simple aabbcc

##### 1.1.107 peer preferred-value

命令用来为从指定对等体/对等体组接收的路由分配首选值。
peer preferred-value命令用来取消该配置。
undo peer preferred-value【命令】
BGP IPv4 单播地址族视图/BGP-VPN IPv4 单播地址族视图/BGP IPv4 组播地址族视图/BGP IPv4 RT-Filter 地址族视图：
peer { group-name | ipv4-address [ mask-length ] } preferred-value value undo peer { group-name | ipv4-address [ mask-length ] } preferred-value

BGP IPv6 单播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } preferred-value value undo peer { group-name | ipv6-address [ prefix-length ] } preferred-value BGP-VPN IPv6 单播地址族视图/BGP IPv6 组播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } preferred-value value undo peer { group-name | ipv6-address [ prefix-length ] } preferred-value【缺省情况】
从对等体/对等体组接收的路由的首选值为 0。
【视图】
单播地址族视图BGP IPv4单播地址族视图BGP-VPN IPv4单播地址族视图BGP IPv6单播地址族视图BGP-VPN IPv6 BGP IPv4 组播地址族视图BGP IPv6 组播地址族视图BGP IPv4 RT-Filter 地址族视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
value：为路由分配的首选值，取值范围为 0～65535。
【使用指导】
当从不同对等体都学习到了到达同一目的网络的路由时，可以使用本命令为从不同对等体学习的路由分配不同的首选值，首选值最大的路由将优先被选作最优路由，从而达到控制 BGP 路径选择的目的。
路由首选值只用于本地路由器的路由选择，不会通告给对等体，只具有本地意义。
既可以通过本命令配置路由的首选值，也可以通过路由策略中的 apply preferred-value 命令为路由配置首选值。如果同时配置了二者，则优先选择路由策略中配置的首选值。只有当路由策略中未配置首选值，或未配置路由策略时，才会选取 命令设置的值。
peer preferred-value

【举例】
\# 在 BGP IPv4 单播地址族视图下，配置来自对等体 1.1.1.1 的路由的首选值为 50。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] peer 1.1.1.1 preferred-value 50【相关命令】
• apply preferred-value（三层技术-IP 路由命令参考/路由策略）
• route-policy（三层技术-IP 路由命令参考/路由策略）

##### 1.1.108 peer prefix-list

peer prefix-list 命令用来为对等体/对等体组设置基于地址前缀列表的 BGP 路由过滤策略。
命令用来删除为指定对等体/对等体组设置基于地址前缀列表的undo peer prefix-list BGP路由过滤策略。
【命令】
BGP IPv4 单播地址族视图/BGP-VPN IPv4 单播地址族视图/BGP IPv4 组播地址族视图：
peer { group-name | ipv4-address [ mask-length ] } prefix-list ipv4-prefix-list-name { export | import } undo peer { group-name | ipv4-address [ mask-length ] } prefix-list [ ipv4-prefix-list-name ] { export | import }单播地址族视图：
BGP IPv6 peer { group-name | ipv6-address [ prefix-length ] } prefix-list ipv6-prefix-list-name { export | import } undo peer { group-name | ipv6-address [ prefix-length ] } prefix-list [ ipv6-prefix-list-name ] { export | import } BGP-VPN IPv6 单播地址族视图/BGP IPv6 组播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } prefix-list ipv6-prefix-list-name { export | import } undo peer { group-name | ipv6-address [ prefix-length ] } prefix-list [ ipv6-prefix-list-name ] { export | import }【缺省情况】
未配置基于地址前缀列表的 BGP 路由过滤策略。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图BGP IPv4 组播地址族视图BGP IPv6 组播地址族视图

【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 地址。指定的对等体必须已经创建。
IPv4 mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 地址。指定的对等体必须已经创建。
IPv6 prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
ipv4-prefix-list-name：IPv4 地址前缀列表名称，为 1～63 个字符的字符串，区分大小写。
ipv6-prefix-list-name：IPv6 地址前缀列表名称，为 1～63 个字符的字符串，区分大小写。
export：对向指定对等体/对等体组发布的路由应用过滤策略。
import：对从指定对等体/对等体组接收的路由应用过滤策略。
【使用指导】
配置 peer prefix-list 命令时需要同时在系统视图下通过 ip prefix-list 命令配置对应的IPv4 地址前缀列表或通过 命令配置对应的 IPv6 地址前缀列表。如果本命令ipv6 prefix-list中指定的 地址前缀列表/IPv6 地址前缀列表尚未创建，则所有路由均通过过滤。
IPv4【举例】
\# 在 BGP IPv4 单播地址族视图下，配置利用 IPv4 地址前缀列表 list1 过滤向对等体组 test 发布的路由。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] peer test prefix-list list1 export【相关命令】
• filter-policy export
• filter-policy import
• ip prefix-list（三层技术-IP 路由命令参考/路由策略）
• ipv6 prefix-list（三层技术-IP 路由命令参考/路由策略）
• peer as-path-acl
• peer filter-policy
• peer route-policy

##### 1.1.109 peer public-as-only

命令用来配置向指定 对等体/对等体组发送 更新消息时只携peer public-as-only EBGP BGP带公有 AS 号，不携带私有 AS 号。
undo peer public-as-only 命令用来取消该配置。

【命令】
BGP IPv4 单播地址族视图/BGP-VPN IPv4 单播地址族视图/BGP IPv4 组播地址族视图：
peer { group-name | ipv4-address [ mask-length ] } public-as-only undo peer { group-name | ipv4-address [ mask-length ] } public-as-only BGP IPv6 单播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } public-as-only undo peer { group-name | ipv6-address [ prefix-length ] } public-as-only BGP-VPN IPv6 单播地址族视图/BGP IPv6 组播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } public-as-only undo peer { group-name | ipv6-address [ prefix-length ] } public-as-only【缺省情况】
向 EBGP 对等体/对等体组发送 BGP 更新消息时，既可以携带公有 AS 号，又可以携带私有 AS 号。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图BGP IPv4 组播地址族视图BGP IPv6 组播地址族视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 地址。指定的对等体必须已经创建。
IPv4 mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
【使用指导】
私有 AS 号是内部使用的 AS 号，范围为 64512～65535。私有 AS 号主要用于测试网络，一般情况下不需要在公共网络中传播。
执行本命令后：
如果向 EBGP 对等体/对等体组发送的 BGP 更新消息中 AS_PATH 属性只包括私有 AS 号，则
•删除私有 号后，将 更新消息发送给对等体/对等体组。
AS BGP

如果 AS_PATH 属性中同时带有公有 AS 号和私有 AS 号，则本命令不生效，即不删除私有 AS
•号，直接将 更新消息发送给对等体/对等体组。
BGP如果 属性中包括对等体/对等体组的 号，则本命令不生效，即不删除私有 号，
• AS_PATH AS AS直接将 BGP 更新消息发送给对等体/对等体组。
本命令只适用于 EBGP 对等体和对等体组。
【举例】
\# 在 BGP IPv4 单播地址族视图下，配置向 EBGP 对等体组 test 发送 BGP 更新消息时只携带公有AS 号，不携带私有 AS 号。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] peer test public-as-only

##### 1.1.110 peer reflect-client

peer reflect-client 命令用来配置本机作为路由反射器，对等体/对等体组作为路由反射器的客户机。
命令用来取消该配置。
undo peer reflect-client【命令】
BGP IPv4 单播地址族视图/BGP-VPN IPv4 单播地址族视图/BGP EVPN 地址族视图/BGP IPv4 组播地址族视图/BGP 地址族视图：
IPv4 RT-Filter peer { group-name | ipv4-address [ mask-length ] } reflect-client undo peer { group-name | ipv4-address [ mask-length ] } reflect-client单播地址族视图：
BGP IPv6 peer { group-name | ipv6-address [ prefix-length ] } reflect-client undo peer { group-name | ipv6-address [ prefix-length ] } reflect-client BGP LS 地址族视图：
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } reflect-client undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } reflect-client BGP IPv6 组播地址族视图/BGP-VPN IPv6 单播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } reflect-client undo peer { group-name | ipv6-address [ prefix-length ] } reflect-client【缺省情况】
未配置路由反射器及其客户机。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图

BGP LS 地址族视图BGP-VPN IPv6 单播地址族视图BGP EVPN 地址族视图BGP IPv4 组播地址族视图BGP IPv6 组播地址族视图BGP IPv4 RT-Filter 地址族视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
【使用指导】
路由反射用来解决 对等体需要全连接的问题。在一个 内，一台路由器作为 RR（Route IBGP AS Reflector，路由反射器），其它路由器作为客户机（Client）与路由反射器建立 IBGP 连接。路由反射器在客户机之间传递（反射）路由信息，而客户机之间不需要建立 BGP 连接。
【举例】
\# 在 BGP IPv4 单播地址族视图下，配置本地设备作为路由反射器，IBGP 对等体组 test 作为路由反射器的客户机。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] peer test reflect-client【相关命令】
• reflect between-clients
• reflector cluster-id

##### 1.1.111 peer route-limit

命令用来设置允许从指定对等体/对等体组收到的路由数量。
peer route-limit命令用来取消该配置。
undo peer route-limit【命令】
单播地址族视图/BGP-VPN 单播地址族视图/BGP 组播地址族视图：
BGP IPv4 IPv4 IPv4

peer { group-name | ipv4-address [ mask-length ] } route-limit prefix-number [ { alert-only | discard | reconnect reconnect-time } | percentage-value ] * undo peer { group-name | ipv4-address [ mask-length ] } route-limit单播地址族视图：
BGP IPv6 peer { group-name | ipv6-address [ prefix-length ] } route-limit prefix-number [ { alert-only | discard | reconnect reconnect-time } | percentage-value ] * undo peer { group-name | ipv6-address [ prefix-length ] } route-limit BGP-VPN IPv6 单播地址族视图/BGP IPv6 组播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } route-limit prefix-number [ { alert-only | discard | reconnect reconnect-time } | percentage-value ] * undo peer { group-name | ipv6-address [ prefix-length ] } route-limit【缺省情况】
不限制从对等体/对等体组接收的路由数量。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图BGP IPv4 组播地址族视图组播地址族视图BGP IPv6【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 地址。指定的对等体必须已经创建。
IPv6 prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
prefix-number：允许路由器接收的路由的数量，取值范围为 1～4294967295。如果没有指定alert-only、discard 和 reconnect 参数，则从指定对等体 / 对等体组接收的路由的数量大于prefix-number 值时，路由器自动断开与指定对等体/对等体组的会话。对于 BGP 动态对等体，本地设备不会尝试与其重新建立会话，但是接收到对等体的 会话建立请求后会接受该请求；
BGP对于其他非 BGP 动态对等体，本地设备不会尝试与其重新建立会话，可以通过 reset bgp 命令重启 BGP 会话，使得本地设备与对等体重新建立 BGP 会话。

alert-only：如果路由器从指定对等体/对等体组接收的路由的数量大于 prefix-number 值，仅打印日志信息，路由器保持与指定对等体/对等体组的会话，并可以继续接收路由。
discard：如果路由器从指定对等体/对等体组接收的路由的数量大于 值，路由prefix-number器保持与指定对等体/对等体组的会话，但丢弃超出限制的路由，并打印日志信息。从指定对等体/对等体组接收的路由数量小于 prefix-number 后，路由器可以继续接收路由。如果用户想恢复之前丢弃的路由，则需要执行 命令请求对等体/对等体组重新发布路由。
refresh bgp import reconnect-time：如果路由器从指定对等体/ 对等体组接收的路由的数量大于reconnect prefix-number 值 ， 则 等 待 指 定 的 时 间 间 隔 后 重 新 与 对 等 体/ 对 等 体 组 建 立 会 话 。
reconnect-time 为路由器与指定对等体/对等体组重建会话的时间间隔，取值范围为 1～65535，单位为秒。对于 BGP 动态对等体，本参数不会生效。
： 配 置 路 由 器 产 生 日 志 信 息 的 阈 值 （ 即 路 由 器 接 收 的 路 由 数 量 与percentage-value的百分比达到 时，路由器将产生日志信息），取值范围为 1～prefix-number percentage-value 100，缺省值为 75。
【举例】
\# 在 BGP IPv4 单播地址族视图下，设置允许从对等体 1.1.1.1 收到的路由数量为 10000。如果从对等体 1.1.1.1 收到的路由数量超过 10000，则断开与该对等体的会话。
<Sysname> system-view [Sysname] bgp 109 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] peer 1.1.1.1 route-limit 10000

##### 1.1.112 peer route-policy

peer route-policy 命令用来对来自对等体/对等体组的路由或发布给对等体/对等体组的路由应用路由策略，以便对路由进行过滤、修改路由的属性等。
undo peer route-policy 命令用来取消该配置。
【命令】
BGP IPv4 单播地址族视图/BGP-VPN IPv4 单播地址族视图/BGP EVPN 地址族视图/BGP IPv4 组播地址族视图：
peer { group-name | ipv4-address [ mask-length ] } route-policy route-policy-name { export | import } undo peer { group-name | ipv4-address [ mask-length ] } route-policy [ route-policy-name ] { export | import } BGP IPv6 单播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } route-policy route-policy-name { export | import } undo peer { group-name | ipv6-address [ prefix-length ] } route-policy [ route-policy-name ] { export | import }单播地址族视图/BGP 组播地址族视图：
BGP-VPN IPv6 IPv6 peer { group-name | ipv6-address [ prefix-length ] } route-policy route-policy-name { export | import }

undo peer { group-name | ipv6-address [ prefix-length ] } [ route-policy-name ] route-policy { export | import }【缺省情况】
没有为对等体/对等体组指定路由策略。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图BGP EVPN 地址族视图BGP IPv4 组播地址族视图BGP IPv6 组播地址族视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 地址。指定的对等体必须已经创建。
IPv4 mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
route-policy-name：路由策略名称，为 1～63 个字符的字符串，区分大小写。
export：对向对等体/对等体组发布的路由应用路由策略。
import：对从对等体/对等体组接收的路由应用路由策略。
【使用指导】
配置 peer route-policy 命令时需要同时在系统视图下通过 route-policy 命令配置对应的路由策略。如果本命令中指定的路由策略尚未创建，则所有路由均通过过滤。
如果在本命令指定的路由策略中配置了 命令，则在路由过滤时忽略此匹配if-match interface规则，认为所有路由均通过该规则。
【举例】
\# 在 BGP IPv4 单播地址族视图下，配置对向对等体组 test 发布的路由应用名为 test-policy 的路由策略。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] peer test route-policy test-policy export

【相关命令】
• filter-policy export
• filter-policy import
• peer as-path-acl
• peer filter-policy
• peer prefix-list
• route-policy（三层技术-IP 路由命令参考/路由策略）

##### 1.1.113 peer route-update-interval

命令用来配置向指定对等体/对等体组发布同一路由的时间间隔。
peer route-update-interval命令用来取消该配置。
undo peer route-update-interval【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } route-update-interval interval undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } route-update-interval【缺省情况】
向 对等体发布同一路由的时间间隔为 秒，向 对等体发布同一路由的时间间隔为IBGP 15 EBGP 30秒。
【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
interval：发布同一路由的最小时间间隔，取值范围为 0～600，单位为秒。

【使用指导】
BGP 路由发生变化时，BGP 路由器会发送 Update 消息通知对等体。如果同一路由频繁变化，BGP路由器会频繁发送 Update 消息更新路由，导致路由震荡。通过本命令指定向对等体/对等体组发布同一路由的时间间隔，可以避免每次路由变化都发送 消息，避免路由震荡。
Update【举例】
\# 在 BGP 实例视图下，配置向对等体组 test 发布同一路由的时间间隔为 10 秒。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer test as-number 100 [Sysname-bgp-default] peer test route-update-interval 10

##### 1.1.114 peer soo

命令用来为对等体/对等体组配置 SoO（Site of Origin，源站点）属性。
peer soo命令用来取消为指定对等体/对等体组配置的 SoO 属性。
undo peer soo【命令】
单播地址族视图/BGP-VPN 单播地址族视图/BGP 组播地址族视图：
BGP IPv4 IPv4 IPv4 peer { group-name | ipv4-address [ mask-length ] } soo site-of-origin undo peer { group-name | ipv4-address [ mask-length ] } soo BGP IPv6 单播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } soo site-of-origin undo peer { group-name | ipv6-address [ prefix-length ] } soo BGP-VPN IPv6 单播地址族视图/BGP IPv6 组播地址族视图：
peer { group-name | ipv6-address [ prefix-length ] } soo site-of-origin undo peer { group-name | ipv6-address [ prefix-length ] } soo【缺省情况】
没有为 BGP 对等体/对等体组配置 SoO 属性。
【视图】
单播地址族视图BGP IPv4单播地址族视图BGP-VPN IPv4单播地址族视图BGP IPv6单播地址族视图BGP-VPN IPv6 BGP IPv4 组播地址族视图BGP IPv6 组播地址族视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。

ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 地址。指定的对等体必须已经创建。
IPv6 prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
site-of-origin：SoO 扩展团体属性，为 3～21 个字符的字符串。site-of-origin 有三种形式：
• 16 位自治系统号:32 位用户自定义数，例如：101:3。
• 32 位 IP 地址:16 位用户自定义数，例如：192.168.122.15:1。
• 32 位自治系统号:16 位用户自定义数，其中的自治系统号最小值为 65536。例如：65536:1。
【使用指导】
SoO 扩展团体属性用来标识路由的原始站点。路由器不会将带有 SoO 属性的路由发布给该 SoO 标识的站点，确保来自某个站点的路由不会再被发布到该站点，从而避免路由环路。在 AS 路径信息丢失时，可以通过 SoO 属性来避免发生环路。
使用不同接口连接同一站点的多个 时，如果配置了 的 号替换功能，则会导致路由PE CE BGP AS环路。这种情况下，需要在 PE 上通过本命令为从同一站点不同 CE 学习到的路由添加相同的 SoO属性，且 PE 向 CE 发布路由时检查 SoO 属性，如果路由的 SoO 属性与为 CE 配置的 SoO 属性相同，则不将该路由发布给 CE，从而避免路由环路。
【举例】
\# 在 BGP IPv4 单播地址族视图下，为对等体 1.1.1.1 配置 SoO 属性为 100:1。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 [Sysname-bgp-default-ipv4] peer 1.1.1.1 soo 100:1【相关命令】
• peer substitute-as

##### 1.1.115 peer source-address

命令用来指定与对等体/对等体组创建 会话时建立 连接使用的peer source-address BGP TCP源 IPv4 地址/IPv6 地址。
undo peer source-address 命令用来取消该配置。
【命令】
peer ipv4-address [ mask-length ] source-address source-ipv4-address peer ipv6-address [ prefix-length ] source-address source-ipv6-address undo peer { ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } source-address peer group-name source-address { source-ipv4-address | source-ipv6-address }
*

undo peer group-name source-address [ source-ipv4-address | source-ipv6-address ]【缺省情况】
BGP 使用到达 BGP 对等体的最佳路由出接口的主 IPv4 地址或 IPv6 地址与对等体/对等体组建立TCP 连接。
【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
source-ipv4-address：源 IPv4 地址。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
source-ipv6-address：源 IPv6 地址。
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
【使用指导】
本命令的作用与 命令的作用类似：本命令直接指定建立 连接的peer connect-interface TCP源地址；peer connect-interface 命令通过指定源接口，间接指定建立 TCP 连接的源地址。
在一台 BGP 路由器上如果同时执行本命令和 命令，则后执行的配置peer connect-interface覆盖之前的配置。
在如下场合需要通过本命令或peer 命令指定建立TCP连接使用的源地址：
connect-interface当指定的对等体的 IPv4 地址/IPv6 地址不是本地路由器与对等体之间直连接口的 IPv4 地址
•地址时，需要在对等体上通过本配置将建立 连接使用的源接口指定为对等体/IPv6 TCP IPv4地址/IPv6 地址所在的接口或者指定 TCP 连接的源地址为对等体 IP 地址/IPv6 地址。
• 当通过 IPv6 链路本地地址创建对等体或向对等体组中添加指定的对等体时，必须使用直连接口建立对等关系，且必须通过 命令将本地直连出接口指定为建peer connect-interface立 连接使用的源接口。
TCP当建立 BGP 连接的路由器之间存在冗余链路时，如果路由器上的一个接口发生故障，链路状
•态变为 down，建立 TCP 连接的源地址可能会随之发生变化，导致 BGP 需要重新建立 TCP连接，造成网络震荡。为了避免该情况的发生，建议网络管理员将建立 TCP 连接所使用的源地址配置为 Loopback 接口的地址，或将源接口配置为 Loopback 接口，以提高 TCP 连接的可靠性和稳定性。

当 BGP 对等体之间同时建立多条 BGP 会话时，如果没有明确指定建立 TCP 连接的源地址，
•可能会导致根据最优路由选择 连接源地址错误，并影响 会话的建立。如果多条TCP BGP BGP会话基于不同接口的 IP 地址建立，则建议用户在配置 BGP 对等体时，通过配置源接口或源地址明确指定每个 BGP 会话的 TCP 连接源地址；如果多条 BGP 会话基于同一接口的不同 IP地址建立，则建议用户通过配置源地址，明确指定每个 会话的 连接源地址。
BGP TCP本地路由器的源地址和对等体的源地址之间必须路由可达。
如果在 EBGP 对等体上指定非直连接口的地址作为源地址，则需要配置 命peer ebgp-max-hop令允许本地路由器同非直连网络上的邻居建立 EBGP 连接。
可以为 对等体组同时指定 和 参数。本BGP source-ipv4-address source-ipv6-address地路由器与对等体组中 IPv4 地址的对等体建立 BGP 会话时，采用 source-ipv4-address 作为TCP 连接的源 IPv4 地址；本地路由器与对等体组中 IPv6 地址的对等体建立 BGP 会话时，采用作为 连接的源 地址。
source-ipv6-address TCP IPv6【举例】
\# 在 BGP 实例视图下，配置与对等体组 test 创建 BGP 会话时，TCP 连接的源地址为 1.1.1.1。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer test source-address 1.1.1.1【相关命令】
• peer connect-interface
• peer ebgp-max-hop

##### 1.1.116 peer substitute-as

peer substitute-as 命令用来配置用本地 AS 号替换 AS_PATH 属性中指定对等体/对等体组的AS 号。
undo peer substitute-as 命令用来取消该配置。
【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } substitute-as undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } substitute-as【缺省情况】
不会用本地 AS 号替换 AS_PATH 属性中指定对等体/对等体组的 AS 号。
【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin

【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 地址。指定的对等体必须已经创建。
IPv6 prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
【使用指导】
如果物理位置不同的 CE 复用相同的 AS 号，则需要在 PE 上配置 BGP 的 AS 号替换功能，将AS_PATH 属性中 CE 的 AS 号替换为 PE 本地的 AS 号，以保证私网路由能够正确发布。
【举例】
\# 在 BGP 实例视图下，配置用本地 AS 号替换对等体 1.1.1.1 的 AS 号。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer 1.1.1.1 substitute-as【相关命令】
• peer soo

##### 1.1.117 peer timer

命令用来配置本地路由器与指定对等体/对等体组之间 会话的存活时间间隔和保peer timer BGP持时间。
undo peer timer 命令用来取消该配置。
【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } timer keepalive keepalive hold holdtime undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } timer【缺省情况】
本地路由器与指定对等体/对等体组之间 BGP 会话的存活时间间隔为 60 秒，保持时间为 180 秒。
【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin

【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 地址。指定的对等体必须已经创建。
IPv6 prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
keepalive：指定存活时间间隔。keepalive 的取值范围为 0～21845，单位为秒。
keepalive holdtime：指定保持时间。holdtime 的取值范围为 或 3～65535，单位为秒。保持时hold 0间必须大于或等于存活时间的三倍。
【使用指导】
当对等体间建立了 BGP 会话后，它们定时向对端发送 Keepalive 消息，以防止路由器认为 BGP 会话已中断。Keepalive 消息的发送时间间隔称为存活时间间隔。
若路由器在设定的会话保持时间（Holdtime）内未收到对端的 Keepalive 消息或 Update 消息，则认为此 会话已中断，从而断开此 会话。
BGP BGP使用该命令配置的定时器比使用 命令配置的定时器优先级高。
timer如果当前路由器上配置的保持时间与对端设备（对等体）上配置的保持时间不一致，则数值较小者作为协商后的保持时间。
保持时间为 0 时，不向该对等体发送 keepalive 消息，与该对等体之间的会话永远不会超时断开；
当保持时间和存活时间间隔都不为 0 时，将协商的保持时间的三分之一与配置的存活时间间隔比较，取最小值作为存活时间间隔。
配置该命令后，不会马上断开会话，而是等到其他条件触发会话重建（如复位 BGP 会话）时，再以配置的保持时间协商建立会话。
【举例】
\# 在 BGP 实例视图下，配置本地路由器与对等体组 test 之间 BGP 会话的存活时间间隔与保持时间分别为 60 秒和 180 秒。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer test timer keepalive 60 hold 180【相关命令】
•display bgp peer
•timer

##### 1.1.118 peer timer connect-retry

peer timer connect-retry 命令用来配置本地路由器与指定对等体/对等体组之间重新建立BGP 会话的时间间隔。
命令用来取消该配置。
undo peer timer connect-retry

【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } timer connect-retry retry-time undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } timer connect-retry【缺省情况】
本地路由器与指定对等体/对等体组之间重新建立 BGP 会话的时间间隔为 32 秒。
【视图】
BGP 视图BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 地址。指定的对等体必须已经创建。
IPv4 mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
retry-time：指定重新建立 BGP 会话的时间间隔，取值范围为 1～65535，单位为秒。
【使用指导】
如果要加快本地路由器与指定对等体/ 对等体组之间重新建立 BGP 会话的速度，可以将的值调小，便于路由快速收敛。如果 会话反复 up/down，可以将retry-time BGP retry-time的值调大，从而减轻路由振荡。
使用本命令配置的定时器比使用 timer connect-retry 命令配置的定时器优先级高。
【举例】
\# 在 BGP 实例视图下，配置本地路由器与对等体 1.1.1.1 之间重新建立 BGP 会话的时间间隔为 30秒。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer 1.1.1.1 timer connect-retry 30【相关命令】
• timer connect-retry

##### 1.1.119 peer ttl-security

peer ttl-security 命令用来使能对等体/对等体组的 BGP GTSM（Generalized TTL Security Mechanism，通用 TTL 安全保护机制）功能。
命令用来关闭指定对等体/对等体组的 BGP GTSM 功能。
undo peer ttl-security【命令】
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } ttl-security hops hop-count undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } ttl-security hops【缺省情况】
BGP GTSM 功能处于关闭状态。
【视图】
实例视图BGP BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
group-name：对等体组的名称，为 1～47 个字符的字符串，区分大小写。指定的对等体组必须已经创建。
ipv4-address：对等体的 IPv4 地址。指定的对等体必须已经创建。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：对等体的 IPv6 地址。指定的对等体必须已经创建。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
hop-count：指定本地设备到达指定对等体的最大跳数。hop-count 表示最大跳数，取值hops范围为 1～254。
【使用指导】
执行本命令为对等体/对等体组使能 BGP 报文的 GTSM 安全检测功能后，当设备收到指定对等体发送的 BGP 报文时，会判断报文的 TTL 是否在 255-“hop-count”+1 到 255 之间。如果在，则上送 处理；如果不在，则直接丢弃报文。从而，使设备能够避免受到 利用（CPU-utilization）
CPU CPU类型的攻击（如 CPU 过载），增强系统的安全性。
执行本命令后，设备会将发送报文的初始 TTL 设置为 255。
配置本命令后，只要本地设备和指定的对等体通过了 GTSM 检查，就允许在二者之间建立 EBGP会话，不管二者之间的跳数是否超过 peer ebgp-max-hop 命令指定的跳数范围。
使用 BGP GTSM 功能时，要求本设备和对等体设备上同时配置本特性，指定的 hop-count 值可以不同，只要能够满足合法性检查即可。

【举例】
\# 在 BGP 实例视图下，为已经创建的对等体组 test 使能 BGP GTSM 功能，并指定对等体组中的对等体到达本地设备的最大跳数为 1。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] peer test ttl-security hops 1【相关命令】
• peer ebgp-max-hop

##### 1.1.120 pic

命令用来开启当前地址族的 BGP 快速重路由功能。
pic命令用来关闭当前地址族的 BGP 快速重路由功能。
undo pic【命令】
pic undo pic【缺省情况】
BGP 快速重路由功能处于关闭状态。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP-VPN IPv6 单播地址族视图【缺省用户角色】
network-admin【使用指导】
FRR（Fast Reroute，快速重路由）功能用来在双归属的组网环境下，通过为流量转发的主路由指定备份下一跳，并通过 ARP（IPv4 组网）、BFD（IPv4 组网）或 ND（IPv6 组网）检测主路由的状态，实现主路由出现故障时，将流量迅速切换到备份路径，大大缩短了故障恢复时间。
通过本命令开启当前地址族的 BGP 快速重路由功能后，BGP 会为当前地址族的所有 BGP 路由自动计算备份下一跳，即只要从不同 BGP 对等体学习到了到达同一目的网络的路由，且这些路由不等价，就会生成主备两条路由。
除了执行本命令外，执行 命令指定 BGP 快速重路由引用的路由fast-reroute route-policy策略，也可以开启快速重路由功能。该方式的优先级高于本命令。路由策略的详细介绍，请参见“三层技术-IP 路由配置指导”中的“路由策略”。
在某些组网情况下，执行 pic 命令为所有 BGP 路由生成备份下一跳后，可能会导致路由环路，请谨慎使用本命令。
【举例】
\# 开启 IPv4 单播地址族的 BGP 快速重路由功能。

<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] pic【相关命令】
•fast-reroute route-policy

##### 1.1.121 port

命令用来配置与 RPKI 服务器建立连接的端口号。
port命令用来恢复缺省情况。
undo port【命令】
port port-number undo port【缺省情况】
未配置与 服务器建立连接的端口号。
RPKI【视图】
BGP RPKI 服务器视图【缺省用户角色】
network-admin【参数】
port-number：与 RPKI 服务器建立连接的端口号，取值范围为 1～65535。
【使用指导】
配置 服务器的地址、与 服务器建立连接的端口号之后，设备会自动和 服务器建立RPKI RPKI RPKI RPKI 连接，用于交互 ROA 信息。该端口号必须与 RPKI 服务器上使用的端口号保持一致。
修改与 RPKI 服务器建立连接使用的端口号时，连接会暂时断开，后续会自动重新建立连接。
【举例】
\# 在 BGP RPKI 服务器视图下，配置与 RPKI 服务器建立连接的端口号为 1234。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] rpki [Sysname-bgp-default-rpki] server tcp 1.1.1.1 [Sysname-bgp-default-rpki-server] port 1234【使用指导】
• server tcp

##### 1.1.122 preference

命令用来配置 路由的优先级。
preference BGP命令用来恢复缺省情况。
undo preference

【命令】
preference { external-preference internal-preference local-preference | route-policy route-policy-name } undo preference【缺省情况】
路由的优先级为 255，IBGP 路由的优先级为 255，本地产生的 路由的优先级为 130。
EBGP BGP【视图】
BGP IPv4 单播地址族视图单播地址族视图BGP-VPN IPv4单播地址族视图BGP IPv6单播地址族视图BGP-VPN IPv6组播地址族视图BGP IPv4组播地址族视图BGP IPv6【缺省用户角色】
network-admin【参数】
external-preference：EBGP 路由（从 EBGP 对等体学来的路由）的优先级，取值范围为 1～255。
internal-preference：IBGP 路由（从 IBGP 对等体学来的路由）的优先级，取值范围为 1～255。
local-preference：本地产生的 BGP 路由的优先级，取值范围为 1～255。
route-policy-name：根据路由策略设置路由的优先级。route-policy-name route-policy表示路由策略名称，为 1～63 个字符的字符串，区分大小写。指定本参数后，可以为通过路由策略中匹配条件过滤的特定路由设置优先级，没有通过过滤的路由使用缺省的优先级。
【使用指导】
对于相同的目的地，不同的路由协议、直连路由和静态路由可能会发现不同的路由，但这些路由并不都是最优的。为了判断最优路由，各路由协议、直连路由和静态路由都被赋予了一个优先级，具有较高优先级的路由协议发现的路由将成为最优路由。
本命令用来设置 路由的优先级，以改变 路由被选为最优路由的可能性。
BGP BGP根据路由策略设置路由的优先级时，需要在指定的路由策略中通过 命令配置apply preference路由的优先级。如果没有在路由策略中配置 apply preference 命令，则通过匹配规则过滤的路由使用缺省的优先级。
【举例】
\# 在 BGP IPv4 单播地址族视图下，配置 EBGP 路由、IBGP 路由和本地产生的 BGP 路由的优先级分别为 20 、 20 和 200 。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast

[Sysname-bgp-default-ipv4] preference 20 20 200

##### 1.1.123 primary-path-detect bfd

primary-path-detect bfd 命令用来配置 BGP 快速重路由通过 BFD 会话检测主路由的下一跳是否可达。
命令用来恢复缺省情况。
undo primary-path-detect bfd【命令】
primary-path-detect bfd echo undo primary-path-detect bfd【缺省情况】
快速重路由通过 检测主路由的下一跳是否可达。
BGP ARP【视图】
BGP 实例视图【缺省用户角色】
network-admin【参数】
echo：配置通过 Echo 方式的 BFD 会话检测主路由的下一跳是否可达。
【举例】
在 实例视图下，配置 快速重路由通过 方式的 会话检测主路由的下一跳是否\# BGP BGP Echo BFD可达。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] primary-path-detect bfd echo【相关命令】
• fast-reroute route-policy
• pic

##### 1.1.124 purge-time

purge-time 命令用来配置 ROA 信息的老化时间。
undo purge-time 命令用来恢复缺省情况。
【命令】
purge-time purge-time undo purge-time【缺省情况】
ROA 信息的老化时间为 60 秒。
【视图】
服务器视图BGP RPKI

【缺省用户角色】
network-admin【参数】
purge-time：BGP RPKI ROA 信息老化时间，取值范围为 30～360，单位为秒。
【使用指导】
与 服务器的连接断开后（不包括用户执行 命令关闭接口引起的连接断开），路由RPKI shutdown器会尝试与 RPKI 服务器重新建立连接，并将从该服务器获得的 ROA 信息置为老化状态，路由器将执行如下操作：
• 如果老化时间内，路由器重新与 RPKI 服务器建立连接，则解除 ROA 信息的老化状态。
• 如果直到老化时间超时，路由器与 RPKI 服务器仍然无法重新建立连接，则删除该 ROA 信息。
【举例】
\# 配置 BGP RPKI ROA 信息的老化时间为 150 秒。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] rpki [Sysname-bgp-default-rpki] server tcp 1.1.1.1 [Sysname-bgp-default-rpki-server] purge-time 150

##### 1.1.125 reflect between-clients

命令用来允许路由反射器在客户机之间反射路由。
reflect between-clients命令用来禁止路由反射器在客户机之间反射路由。
undo reflect between-clients【命令】
reflect between-clients undo reflect between-clients【缺省情况】
允许路由反射器在客户机之间反射路由。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP LS 地址族视图BGP-VPN IPv6 单播地址族视图BGP EVPN 地址族视图BGP IPv4 组播地址族视图组播地址族视图BGP IPv6地址族视图BGP IPv4 RT-Filter【缺省用户角色】
network-admin

【使用指导】
如果配置了路由反射器后，由于组网需要在路由反射器的客户机之间建立了全连接，则客户机之间可以直接交换路由信息，客户机到客户机之间的路由反射是没有必要的。此时，不需要修改网络配置或改变网络拓扑，只需在路由反射器上通过本命令禁止其在客户机之间反射路由，就可以避免路由反射，减少占用的带宽资源。
禁止客户机之间的路由反射后，客户机到非客户机之间的路由仍然可以被反射。
【举例】
\# 在 BGP IPv4 单播地址族视图下，禁止路由反射器在客户机之间反射路由。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] undo reflect between-clients【相关命令】
• peer reflect-client
• reflector cluster-id

##### 1.1.126 reflector cluster-id

reflector cluster-id 命令用来配置路由反射器的集群 ID。
undo reflector cluster-id 命令用来恢复缺省情况。
【命令】
reflector cluster-id { cluster-id | ipv4-address } undo reflector cluster-id【缺省情况】
每个路由反射器都使用自己的 Router ID 作为集群 ID。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv6 单播地址族视图BGP LS 地址族视图BGP-VPN IPv6 单播地址族视图BGP EVPN 地址族视图BGP IPv4 组播地址族视图BGP IPv6 组播地址族视图BGP IPv4 RT-Filter 地址族视图【缺省用户角色】
network-admin

【参数】
cluster-id：指定数值形式的集群 ID，取值范围为 1～4294967295。
ipv4-address：指定点分十进制地址形式的集群 ID。
【使用指导】
路由反射器及其客户机形成了一个集群。通常情况下，一个集群中只有一个路由反射器，该反射器的 就作为集群 ID，用于识别该群。
Router ID为了提高网络的可靠性、避免单点故障，一个集群中可以设置多个路由反射器。此时，应使用本命令为集群中所有路由反射器配置相同的集群 ID，以便集群具有统一的标识，避免路由环路的产生。
配置的集群 不要与客户机的 相同。
ID Router ID【举例】
\# 在 BGP IPv4 单播地址族视图下，本地路由器是集群中的路由反射器之一，在本地路由器上配置集群 ID 为 80。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] reflector cluster-id 80【相关命令】
• peer reflect-client
• reflect between-clients

##### 1.1.127 refresh bgp

refresh bgp 命令用来手工对 BGP 会话进行软复位。
【命令】
refresh bgp [ instance instance-name ] { ipv4-address [ mask-length ] | all | external | group group-name | internal } { export | import } ipv4 [ multicast | rtfilter | [ unicast ] [ vpn-instance vpn-instance-name ] ] refresh bgp [ instance instance-name ] { ipv6-address [ prefix-length ] | all | external | group group-name | internal } { export | import } ipv6 [ multicast | [ unicast ] [ vpn-instance vpn-instance-name ] ] refresh bgp ipv4-address [ mask-length ] { export | import } ipv6 [ unicast ] refresh bgp [ instance instance-name ] { ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] | all | external | group group-name | internal } { export | import } link-state refresh bgp [ instance instance-name ] { ipv4-address [ mask-length ] | all | external | group group-name | internal } { export | import } l2vpn evpn【视图】
用户视图【缺省用户角色】
network-admin

【参数】
instance instance-name：软复位指定 BGP 实例内的 BGP 会话。instance-name 表示 BGP实例名称，为 1～31 个字符的字符串，区分大小写。如果不指定本参数，则表示软复位 BGP 实例内的 会话。
default BGP ipv4-address：软复位与指定对等体的 会话。ipv4-address 为对等体的 地址。
BGP IPv4 mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：软复位与指定对等体的 BGP 会话。ipv6-address 为对等体的 IPv6 地址。
prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
all：软复位指定地址族下的所有 BGP 会话。
external：软复位指定地址族下的所有 EBGP 会话。
group group-name：软复位与指定对等体组中对等体的 BGP 会话。group-name 表示对等体组的名称，为 1～47 个字符的字符串，区分大小写。
internal：软复位指定地址族下的所有 IBGP 会话。
export：触发出方向的软复位，即采用新的配置对向对等体发布的路由进行过滤。
import：触发入方向的软复位，即采用新的配置对从对等体接收的路由进行过滤。
ipv4：软复位 IPv4 地址族下的 BGP 会话。
ipv6：软复位 IPv6 地址族下的 BGP 会话。
link-state：软复位 LS 地址族下的 BGP 会话。
multicast：软复位组播地址族下的 BGP 会话。
rtfilter：软复位 地址族下的 会话。
IPv4 RT-Filter BGP unicast：软复位单播地址族下的 会话。
BGP l2vpn：软复位 地址族下的 会话。
L2VPN BGP evpn：软复位 地址族下的 会话。
EVPN BGP vpn-instance-name：软复位指定 实例内指定地址族下的 会话。
vpn-instance VPN BGP vpn-instance-name 表示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果不指定本参数，则软复位公网指定地址族下的 BGP 会话。
【使用指导】
软复位 BGP 会话是指在不断开 BGP 邻居关系的情况下，更新 BGP 路由信息，使新的配置生效。
选路策略发生改变后，如果指定了 参数，则会触发本地路由器根据新的路由发布策略过滤export路由信息，并将通过过滤的路由信息发送给 对等体；如果指定了 参数，则本地路由BGP import器会向 BGP 对等体发送 Route-refresh 消息，收到 Route-refresh 消息的对等体将其路由信息重新发给本地路由器，以便本地路由器根据新的路由策略对接收到的路由信息进行过滤。
执行本命令软复位 BGP 会话时，要求当前路由器和对等体都支持 Route-refresh 功能，否则本命令不会生效。
配置 命令后，执行 命令不会生效。
peer keep-all-routes refresh bgp import如果没有指定 和 参数，则缺省为 unicast。
unicast multicast

【举例】
\# 手工对所有 IPv4 单播地址族下的 BGP 会话进行入方向的软复位。
<Sysname> refresh bgp all import ipv4【相关命令】
• peer capability-advertise route-refresh
• peer keep-all-routes

##### 1.1.128 refresh-time

refresh-time 命令用来配置 RPKI 连接的检测周期。
命令用来恢复缺省情况。
undo refresh-time【命令】
refresh-time refresh-time undo refresh-time【缺省情况】
RPKI 连接的检测周期为 600 秒。
【视图】
BGP RPKI 服务器视图【缺省用户角色】
network-admin【参数】
refresh-time：RPKI 连接的检测周期，取值范围为 15～3600，单位为秒。
【使用指导】
设备会按周期检测与 RPKI 服务器的连接是否正常，如果直到响应时间超时仍然没有收到 RPKI 服务器的响应，则认为与 RPKI 服务器的连接已经断开。
【举例】
配置 服务器连接检测周期为 秒。
\# BGP RPKI 15 <Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] rpki [Sysname-bgp-default-rpki] server tcp 1.1.1.1 [Sysname-bgp-default-rpki-server] refresh-time 15【相关命令】
• response-time

##### 1.1.129 reset bgp

reset bgp 命令用来复位指定地址族下的 BGP 会话。

【命令】
reset bgp [ instance instance-name ] { as-number | ipv4-address [ mask-length ] | all | external | group group-name | internal } ipv4 [ multicast | rtfilter | [ unicast ] [ vpn-instance vpn-instance-name ] ] reset bgp [ instance instance-name ] { as-number | ipv6-address [ prefix-length ] | all | external | group group-name | internal } ipv6 [ multicast | [ unicast ] [ vpn-instance vpn-instance-name ] ] reset bgp [ instance instance-name ] { as-number | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] | all | external | group group-name | internal } link-state reset bgp [ instance instance-name ] { as-number | ipv4-address [ mask-length ] | all | external | group group-name | internal } l2vpn evpn【视图】
用户视图【缺省用户角色】
network-admin【参数】
instance-name：复位指定 实例内的 会话。instance-name 表示instance BGP BGP BGP实例名称，为 1～31 个字符的字符串，区分大小写。如果不指定本参数，则表示复位 BGP 实例 default内的 BGP 会话。
as-number：复位与指定自治系统内对等体的 BGP 会话。as-number 为自治系统号，取值范围为 1～4294967295。
ipv4-address：复位与指定对等体的 BGP 会话。ipv4-address 为对等体的 IPv4 地址。
mask-length：网络掩码，取值范围为 0～32。如果指定本参数，则表示指定网段内的动态对等体。
ipv6-address：复位与指定对等体的 会话。ipv6-address 为对等体的 地址。
BGP IPv6 prefix-length：前缀长度，取值范围为 0～128。如果指定本参数，则表示指定网段内的动态对等体。
all：复位指定地址族下的所有 会话。
BGP external：复位指定地址族下的所有 会话。
EBGP group-name：复位与指定对等体组中对等体的 会话。group-name 表示对等体组group BGP的名称，为 1～47 个字符的字符串，区分大小写。
internal：复位指定地址族下的所有 IBGP 会话。
ipv4：复位 IPv4 地址族下的 BGP 会话。
ipv6：复位 地址族下的 会话。
IPv6 BGP：复位 地址族下的 会话。
link-state LS BGP multicast：复位组播地址族下的 会话。
BGP rtfilter：复位 地址族下的 会话。
IPv4 RT-Filter BGP unicast：复位单播地址族下的 会话。
BGP

l2vpn：复位 L2VPN 地址族下的 BGP 会话。
evpn：复位 EVPN 地址族下的 BGP 会话。
vpn-instance-name：复位指定 VPN 实例内指定地址族下的 BGP 会话。
vpn-instance表示 的 实例名称，为 1～31 个字符的字符串，区分大vpn-instance-name MPLS L3VPN VPN小写。如果不指定本参数，则复位公网指定地址族下的 BGP 会话。
【使用指导】
BGP 的选路策略改变后，为了使新的策略生效，可以复位 BGP 会话，即删除并重新建立 BGP 会话，以便重新发布路由信息，并应用新的策略对路由信息进行过滤。复位 BGP 会话时，会造成短暂的 会话中断。
BGP如果没有指定 和 参数，则缺省为 unicast。
unicast multicast【举例】
\# 复位公网 IPv4 单播地址族下的所有 BGP 会话。
<Sysname> reset bgp all ipv4

##### 1.1.130 reset bgp all

命令用来复位所有 BGP 会话。
reset bgp all【命令】
reset bgp [ instance instance-name ] all【视图】
用户视图【缺省用户角色】
network-admin【参数】
instance-name：复位指定 BGP 实例内的 BGP 会话。instance-name 表示 BGP instance实例名称，为 1～31 个字符的字符串，区分大小写。如果不指定本参数，则表示复位 实例BGP default内的 BGP 会话。
【使用指导】
BGP 的选路策略改变后，为了使新的策略生效，可以复位 BGP 会话，即删除并重新建立 BGP 会话，以便重新发布路由信息，并应用新的策略对路由信息进行过滤。复位 BGP 会话时，会造成短暂的 BGP 会话中断。
【举例】
\# 复位所有 BGP 会话。
<Sysname> reset bgp all

##### 1.1.131 reset bgp bmp server statistics

命令用来清除 监控服务器记录的报文统计信息。
reset bgp bmp server statistics BMP

【命令】
reset bgp [ instance instance-name ] bmp server server-number statistics【视图】
用户视图【缺省用户角色】
network-admin【参数】
instance instance-name：清除指定 BGP 实例下 BMP Server 记录的报文统计信息。
instance-name 表示 BGP 实例的名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则清除 default 实例下 BMP Server 记录的报文统计信息。
server-number：BGP 监控服务器号，取值范围为 1～8。
【举例】
清除 记录的报文统计信息。
\# BMP Server 1 <Sysname> reset bgp bmp server 1 statistics【相关命令】
•display bgp bmp server

##### 1.1.132 reset bgp dampening

命令用来清除 BGP 路由的衰减信息，并解除对 BGP 路由的抑制。
reset bgp dampening【命令】
reset bgp [ instance instance-name ] dampening ipv4 [ multicast | [ unicast ] [ vpn-instance vpn-instance-name ] ] [ ipv4-address [ mask-length | mask ] ] reset bgp [ instance instance-name ] dampening ipv6 [ multicast | [ unicast ] [ vpn-instance vpn-instance-name ] ] [ ipv6-address prefix-length ]【视图】
用户视图【缺省用户角色】
network-admin【参数】
instance-name：清除指定 实例的 路由衰减信息，并解除对指定 实instance BGP BGP BGP例的 BGP 路由的抑制。instance-name 表示 BGP 实例名称，为 1～31 个字符的字符串，区分大小写。如果不指定本参数，则表示 default 实例。
ipv4：清除 BGP IPv4 路由的衰减信息，并解除对 BGP IPv4 路由的抑制。
ipv6：清除 BGP IPv6 路由的衰减信息，并解除对 BGP IPv6 路由的抑制。
multicast：清除 BGP 组播路由的衰减信息，并解除对 BGP 组播路由的抑制。
unicast：清除 BGP 单播路由的衰减信息，并解除对 BGP 单播路由的抑制。

vpn-instance-name：清除指定 VPN 实例内 BGP 路由的衰减信息，并解除对vpn-instance路由的抑制。vpn-instance-name 表示 的 实例名称，为 1～31 个字符BGP MPLS L3VPN VPN的字符串，区分大小写。如果不指定本参数，则清除公网 BGP 路由的衰减信息，并解除对 BGP 路由的抑制。
ipv4-address：清除匹配指定目的网络 IPv4 地址的 BGP 路由的衰减信息，并解除对该路由的抑制。如果不指定本参数，则清除所有 路由的衰减信息，并解除对所有 路由的抑制。
BGP BGP mask-length：目的网络 地址的掩码长度，取值范围为 0～32。
IPv4 mask：目的网络 IPv4 地址的掩码，点分十进制格式。
ipv6-address：清除匹配指定目的网络 IPv6 地址的 BGP 路由的衰减信息，并解除对该路由的抑制。如果不指定本参数，则清除所有 路由的衰减信息，并解除对所有 路由的抑制。
BGP BGP prefix-length：目的网络 地址的前缀长度，取值范围为 0～128。
IPv6【使用指导】
执行 reset bgp dampening ipv4 命令时：
• 如果只指定了 ipv4-address 参数，则将指定的网络地址和路由的掩码进行与操作，若计算结果与路由的网段地址相同，则清除该 BGP IPv4 单播路由或组播路由的衰减信息，并解除对该路由的抑制。
• 如果指定了 或 参数，则清除与指定ipv4-address mask ipv4-address mask-length目的网络 地址和网络掩码（或掩码长度）精确匹配的 单播路由或组播路由的IPv4 BGP IPv4衰减信息，并解除对该路由的抑制。
如果没有指定 unicast 和 multicast 参数，则缺省为 unicast。
【举例】
\# 清除到达网络 20.1.0.0/16 的 BGP IPv4 单播路由的衰减信息，并解除对该路由的抑制。
<Sysname> reset bgp dampening ipv4 20.1.0.0 255.255.0.0【相关命令】
• dampening
• display bgp routing-table dampened

##### 1.1.133 reset bgp flap-info

reset bgp flap-info 命令用来清除 BGP 路由的振荡统计信息。
【命令】
reset bgp [ instance instance-name ] flap-info ipv4 [ multicast | [ unicast ] [ vpn-instance vpn-instance-name ] ] [ ipv4-address [ mask-length | mask ] | as-path-acl as-path-acl-number | peer ipv4-address [ mask-length ] ] reset bgp [ instance instance-name ] flap-info ipv6 [ multicast | [ unicast ] [ vpn-instance vpn-instance-name ] ] [ ipv6-address prefix-length | as-path-acl as-path-acl-number | peer ipv6-address [ prefix-length ] ]【视图】
用户视图

【缺省用户角色】
network-admin【参数】
instance-name：清除指定 BGP 实例的 BGP 路由振荡统计信息。instance-name instance表示 实例名称，为 1～31 个字符的字符串，区分大小写。如果不指定本参数，则表示清除BGP default实例的 BGP 路由振荡统计信息。
ipv4：清除 BGP IPv4 路由的振荡统计信息。
ipv6：清除 BGP IPv6 路由的振荡统计信息。
multicast：清除 组播路由的振荡统计信息。
BGP unicast：清除 单播路由的振荡统计信息。
BGP vpn-instance-name：清除指定 实例内 路由的振荡统计信息。
vpn-instance VPN BGP vpn-instance-name 表示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果不指定本参数，则清除公网 BGP 路由的振荡统计信息。
ipv4-address：清除匹配指定目的网络 IPv4 地址的 BGP 路由的振荡统计信息。
mask-length：目的网络 IPv4 地址的掩码长度，取值范围为 0～32。
mask：目的网络 IPv4 地址的掩码，点分十进制格式。
ipv6-address：清除匹配指定目的网络 IPv6 地址的 BGP 路由的振荡统计信息。
prefix-length：目的网络 IPv6 地址的前缀长度，取值范围为 0～128。
as-path-acl as-path-acl-number：清除匹配指定 AS 路径过滤列表的 BGP 路由的振荡统计信息。as-path-acl-number 为 AS 路径过滤列表号，取值范围为 1～256。
peer ipv4-address [ mask-length ]：清除从指定 BGP 对等体学习到的 BGP 路由的振荡统计信息。ipv4-address 为 BGP 对等体的 IPv4 地址。mask-length 为网络掩码，取值范围为 0～32，如果指定本参数，则表示指定网段内的动态对等体。
]：清除从指定 对等体学习到的 路由的振peer ipv6-address [ prefix-length BGP BGP荡统计信息。ipv6-address 为对等体的 IPv6 地址。prefix-length 为前缀长度，取值范围为0～128，如果指定本参数，则表示指定网段内的动态对等体。
【使用指导】
执行 命令时：
reset bgp flap-info ipv4如果只指定了 参数，则将指定的网络地址和路由的掩码进行与操作，若计算
• ipv4-address结果与路由的网段地址相同，则清除该 单播路由或组播路由的振荡统计信息。
BGP IPv4如果指定了 或 参数，则清除与指定
• ipv4-address mask ipv4-address mask-length目的网络 IPv4 地址和网络掩码（或掩码长度）精确匹配的 BGP IPv4 单播路由或组播路由的振荡统计信息。
如果没有指定 unicast 和 multicast 参数，则缺省为 unicast。
【举例】
\# 清除到达网络 20.1.0.0/16 的 BGP IPv4 单播路由的振荡统计信息。
<Sysname> reset bgp flap-info ipv4 20.1.0.0 16【相关命令】
• dampening

• display bgp routing-table flap-info

##### 1.1.134 reset bgp rpki server

命令用来复位 BGP RPKI 会话。
reset bgp rpki server【命令】
reset bgp [ instance instance-name ] rpki server [ vpn-instance vpn-instance-name ] tcp { ipv4 address | ipv6 address }【视图】
用户视图【缺省用户角色】
network-admin【参数】
instance-name：复位指定 实例内的 会话。instance-name 表示instance BGP RPKI BGP实例名称，为 1～31 个字符的字符串，区分大小写。如果不指定本参数，则表示复位 BGP 实例 default内的 RPKI 会话。
vpn-instance vpn-instance-name ： 复 位 指 定 VPN 实 例 内 的 BGP RPKI 会 话 。
表示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大vpn-instance-name小写。如果不指定本参数，则复位公网 会话。
BGP RPKI ipv4-address：BGP 服务器的 地址。
RPKI IPv4 ipv6-address：BGP 服务器的 地址。
RPKI IPv6【使用指导】
配置本命令后，设备将删除并重新建立指定的 BGP RPKI 会话，会造成 BGP RPKI 会话短暂中断。
【举例】
\# 复位与 RPKI 服务器 2.2.2.1 之间的 BGP RPKI 会话。
<Sysname> reset bgp rpki server tcp 2.2.2.1

##### 1.1.135 response-time

命令用来配置 服务器的响应等待时间。
response-time RPKI命令用来恢复缺省情况。
undo response-time【命令】
response-time response-time undo response-time【缺省情况】
等待 RPKI 服务器响应的时间为 30 秒。
【视图】
BGP RPKI 服务器视图

【缺省用户角色】
network-admin【参数】
response-time：等待 BGP RPKI 服务器响应的时间，取值范围 15～3600，单位秒。
【使用指导】
路由器会根据刷新时间间隔检测与 服务器的连接关系，如果在响应时间内没有收到服务器的RPKI回应，路由器与 RPKI 服务器的连接断开。
【举例】
\# 配置等待 BGP RPKI 服务器响应的时间为 15 秒。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] rpki [Sysname-bgp-default-rpki] server tcp 1.1.1.1 [Sysname-bgp-default-rpki-server] response-time 15【相关命令】
• refresh-time

##### 1.1.136 route-mode adj-rib-out

命令用来配置将本地设备发送给监控对等体/对等体组的路由信息发route-mode adj-rib-out送给监控服务器。
命令用来恢复缺省情况。
undo route-mode adj-rib-out【命令】
route-mode adj-rib-out undo route-mode adj-rib-out【缺省情况】
不会将本地设备发送给监控对等体/对等体组的路由信息发送给监控服务器。
【视图】
BMP Server 视图【缺省用户角色】
network-admin【使用指导】
当 BGP 与监控服务器的 TCP 连接建立后，如果执行了本命令，则本地设备向监控对等体/对等体组发送的路由信息会同时发送给监控服务器。
【举例】
\# 配置将本地设备发送给监控对等体/对等体组的路由信息发送给监控服务器。
<Sysname> system-view [Sysname] bmp server 5 [Sysname-bmpserver-5] route-mode adj-rib-out

##### 1.1.137 route-mode loc-rib

route-mode loc-rib 命令用来配置向监控服务器发送 BGP 优选后的路由信息。
undo route-mode loc-rib 命令用来恢复缺省情况。
【命令】
route-mode loc-rib undo route-mode loc-rib【缺省情况】
不向监控服务器发送 BGP 优选后的最优路由信息。
【视图】
视图BMP Server【缺省用户角色】
network-admin【使用指导】
当 BGP 与监控服务器的 TCP 连接建立后，如果执行了本命令，则会向给监控服务器发送 BGP 优选后的最优路由信息。
目前，仅支持向监控服务器发送 IPv4 单播和 BGP-VPN IPv4 单播路由。
【举例】
配置向监控服务器发送 优选后的路由信息。
\# BGP <Sysname> system-view [Sysname] bmp server 5 [Sysname-bmpserver-5] route-mode loc-rib

##### 1.1.138 router id

命令用来配置全局 Router ID。
router id命令用来恢复缺省情况。
undo router id【命令】
router id router-id undo router id【缺省情况】
未配置全局 Router ID。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
router-id：全局 ID，用 地址的形式标识。
Router IP

【使用指导】
一些动态路由协议要求使用 Router ID，如果在启动这些路由协议时没有指定 Router ID，则缺省使用全局 Router ID。
如果配置了全局 Router ID，则使用配置的值作为 Router ID。如果未配置全局 Router ID，则按照下面的规则进行选择：
如果存在配置 地址的 接口，则选择 接口地址中最大的作为
(1) IP Loopback Loopback Router ID。
(2) 如果未配置 IP 地址的 Loopback 接口，则从其他接口的 IP 地址中选择最大的作为 Router ID（不考虑接口的 up/down 状态）。
(3) 如果所有接口上都未配置 IP 地址，则 Router ID 为 0.0.0.0。
存在主备的情况下，系统将备份命令行配置的 Router ID 或从接口地址中选择出来的 Router ID。主备倒换后，系统将检查从地址中选出的 Router ID 的有效性，如果无效将重新进行选择。
当且仅当被选为 Router ID 的接口 IP 地址被删除或被修改时，才触发重新选择过程，其他情况（例如：接口 down；已经选取了一个非 Loopback 接口地址后又配置了一个 Loopback 接口地址；配置一个更大的接口地址等）不触发重新选择的过程。
全局 改变后，执行 命令重启 会话，不会改变 路由器的 ID。只Router ID reset BGP BGP Router能在 BGP 实例视图下通过 Router ID 命令改变 BGP 路由器的 Router ID。
【举例】
\# 配置全局 Router ID 为 1.1.1.1。
<Sysname> system-view [Sysname] router id 1.1.1.1【相关命令】
• router-id (BGP instance view)
• router-id (BGP-VPN instance view)

##### 1.1.139 route-rate-limit

命令用来配置 新增路由的发布速率。
route-rate-limit BGP命令用来恢复缺省情况。
undo route-rate-limit【命令】
route-rate-limit rate undo route-rate-limit【缺省情况】
不限制 BGP 新增路由的发布速率。
【视图】
BGP 实例视图【缺省用户角色】
network-admin

【参数】
rate：发布新增路由的速率，取值范围为 0～4294967595，单位为条/秒。取值为 0 时，表示不发布新增路由。
【使用指导】
网络中新增路由数量较大时，如果在短时间内发布大量路由，可能会导致 对等体已接收到新BGP增路由并添加对应的转发表项，本地设备上的转发表项却尚未添加，从而导致流量转发失败。请根据设备的性能合理配置 BGP 发送新增路由的速率，如果设备的性能较高，可以将 BGP 发送新增路由的速率适当调大；如果设备的性能一般，建议将 BGP 发送新增路由的速率适当调小。
当网络发生震荡时，建议不要将 BGP 新增路由发布速率配置为 0 或过小，否则可能会导致失效路由无法及时撤销。
目前，仅支持对新增 单播和 单播路由的发送速率进行限制。
IPv4 IPv6【举例】
\# 在 BGP 实例视图下，配置 BGP 新增路由发布速率为 1000 条/秒。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] route-rate-limit 1000

##### 1.1.140 router-id (BGP instance view)

命令用来为指定的 实例配置 路由器的 ID。
router-id BGP BGP Router命令用来恢复缺省情况。
undo router-id【命令】
router-id router-id undo router-id【缺省情况】
未配置 BGP 路由器在 BGP 实例内的 Router ID，为系统视图下通过 router id 命令配置的全局Router ID。
【视图】
实例视图BGP【缺省用户角色】
network-admin【参数】
router-id：BGP 路由器的 Router ID，用 IP 地址的形式标识。
【使用指导】
如果要在 BGP 实例下运行 BGP 协议，则必须为 BGP 实例指定 Router ID。它是一个 32 比特无符号整数，是一台路由器在自治系统中的唯一标识。
路由器的 一旦确定为非零值后不会随着系统视图下 命令配置的改变而BGP Router ID router id改变。只能在 BGP 实例视图下通过 router-id 命令改变 BGP 路由器的 Router ID。
为了增加网络的可靠性，建议将 Router ID 手工配置为 Loopback 接口的 IP 地址。

在同一个视图下多次执行本命令，最后一次执行的命令生效。
不同 BGP 实例的 Router ID 可以相同。
【举例】
在 实例视图下，指定 路由器的 为 1.1.1.1。
\# BGP BGP Router ID <Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] router-id 1.1.1.1【相关命令】
• router id
• router-id (BGP-VPN instance view)

##### 1.1.141 router-id (BGP-VPN instance view)

命令用来为指定的 实例配置 路由器的 ID。
router-id VPN BGP Router命令用来恢复缺省情况。
undo router-id【命令】
router-id { router-id | auto-select } undo router-id【缺省情况】
未配置 BGP 路由器在 VPN 实例内的 Router ID。如果在 BGP 实例视图下执行了 router-id 命令，则 BGP 路由器在 VPN 实例内的 Router ID 为该命令配置的 Router ID；否则，为系统视图下通过命令配置的全局 ID。
router id Router【视图】
BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
：BGP 路由器的 Router ID，用 IP 地址的形式标识。
router-id auto-select：自动选取该 VPN 实例内 BGP 路由器的 Router ID。
【使用指导】
一个BGP实例如果要在某个VPN实例内运行BGP协议，则必须为其指定在该VPN实例内的Router ID。Router ID 是一个 32 比特无符号整数，是一台路由器在自治系统中的唯一标识。
执行 命令后，该 实例内 路由器的 选取原则为：
router-id auto-select VPN BGP Router ID如果存在属于当前 实例、且已配置 地址的 接口，则选择 接口地
(1) VPN IP Loopback Loopback址中最大的作为 Router ID。
(2) 如果不存在满足上述条件的 Loopback 接口，则从其他属于当前 VPN 实例的接口中，选择最大的接口 IP 地址作为 Router ID（不考虑接口的 up/down 状态）。
(3) 如果不存在属于当前 VPN 实例的接口地址，则 Router ID 为 0.0.0.0。

当前 VPN 实例内 BGP 路由器的 Router ID 一旦确定为非零值，即使存在满足选取原则的更优的接口地址，系统也不会重新选择 ID。
Router为了增加网络的可靠性，建议将 手工配置为 接口的 地址。
Router ID Loopback IP在同一台设备上，可以为不同的 实例指定不同的 ID。
VPN Router在同一个视图下多次执行本命令，最后一次执行的命令生效。
【举例】
\# 在 BGP-VPN 实例视图下，指定 VPN 实例 vpn1 内 BGP 路由器的 Router ID 为 1.1.1.1。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] ip vpn-instance vpn1 [Sysname-bgp-default-vpn1] router-id 1.1.1.1【相关命令】
• router id
• router-id (BGP instance view)

##### 1.1.142 rpki

命令用来使能 功能，并进入 视图。
rpki RPKI BGP RPKI命令用来删除 视图下的所有配置。
undo rpki BGP RPKI【命令】
rpki undo rpki【视图】
BGP 视图【缺省用户角色】
network-admin【举例】
\# 使能 RPKI 功能，并进入 BGP RPKI 视图。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] rpki [Sysname-bgp-default-rpki]

##### 1.1.143 server

server 命令用来配置监控服务器的 IP 地址和端口号。
undo server 命令用来删除监控服务器的 IP 地址和端口号。
【命令】
server address ipv4-address port port-number undo server

【缺省情况】
未配置监控服务器的连接地址和端口号。
【视图】
BMP Server 视图【缺省用户角色】
network-admin【参数】
ipv4-address：监控服务器的 IP 地址。
port-number：监控服务器的端口号，取值范围为 1～65535。
【使用指导】
配置了监控服务器的连接地址和端口号后，客户端会向监控服务器发起 TCP 连接，TCP 连接建立后客户端向监控服务器发送 BMP 报文。
【举例】
\# 配置监控服务器 5 的 IP 地址为 100.1.1.1，端口号为 8888。
<Sysname> system-view [Sysname] bmp server 5 [Sysname-bmpserver-5] server address 100.1.1.1 port 8888

##### 1.1.144 server connect-interface

命令用来配置本地设备与监控服务器之间 TCP 连接的源接口。
server connect-interface命令用来恢复缺省情况。
undo server connect-interface【命令】
server connect-interface interface-type interface-number undo server connect-interface【缺省情况】
使用到达监控服务器的最佳路由出接口的地址建立 连接。
BGP TCP【视图】
BMP Server 视图【缺省用户角色】
network-admin【参数】
interface-number：接口类型和接口编号。
interface-type【使用指导】
配置本命令后，BGP 使用源接口的地址作为与监控服务器建立 连接的源地址。
TCP

不能通过本命令指定建立 TCP 连接的源接口为 VT（Virtual Template，虚拟模板）接口，因为 VT口只能作为模板口并不处理相关业务。
【举例】
配置监控服务器 的 地址为 100.1.1.1、端口号为 8888，同时配置使用接口 作为\# 5 IP Loopback0与监控服务器 5 建立 TCP 连接的源接口。
<Sysname> system-view [Sysname] bmp server 5 [Sysname-bmpserver-5] server address 100.1.1.1 port 8888 [Sysname-bmpserver-5] server connect-interface loopback0

##### 1.1.145 server tcp

命令用来指定 BGP RPKI 服务器地址，并进入 RPKI 服务器视图。
server tcp命令用来取消该配置。
undo server tcp【命令】
server [ vpn-instance vpn-instance-name ] tcp { ipv4-address | ipv6-address } undo server [ vpn-instance vpn-instance-name ] tcp { ipv4-address | ipv6-address }【缺省情况】
未配置 RPKI 的服务器地址。
【视图】
BGP RPKI 视图【缺省用户角色】
network-admin【参数】
vpn-instance vpn-instance-name ： 指 定 BGP RPKI 服 务 器 所 属 的 VPN 实 例 。
vpn-instance-name 表示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则表示 BGP RPKI 服务器位于公网中。
ipv4-address：RPKI 服务器的 IPv4 地址。
ipv6-address：RPKI 服务器的 IPv6 地址。
【使用指导】
重复执行本命令，可以指定多个 RPKI 服务器地址，与多个 RPKI 服务器建立连接。
执行 命令，将删除 RPKI 服务器视图下的所有配置。
undo server【举例】
指定 服务器地址为 1.1.1.1，并进入 服务器视图。
\# BGP RPKI RPKI <Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] rpki

[Sysname-bgp-default-rpki] server tcp 1.1.1.1 [Sysname-bgp-default-rpki-server]

##### 1.1.146 snmp context-name

命令用来配置 实例的 上下文。
snmp context-name BGP SNMP命令用来恢复缺省情况。
undo snmp context-name【命令】
snmp context-name context-name undo snmp context-name【缺省情况】
未配置 BGP 实例的 SNMP 上下文。
【视图】
BGP 实例视图【缺省用户角色】
network-admin【参数】
context-name：SNMP 上下文名称，为 1～32 个字符的字符串，区分大小写。
【使用指导】
通过 MIB（Management Information Base，管理信息库）节点对 BGP 进行管理时，BGP 无法获知被管理的节点属于哪个 BGP 实例。为不同的 BGP 实例配置不同的 SNMP 上下文可以解决上述问题。
设备接收到 报文后，根据报文中携带的上下文（对于 SNMPv3）或团体名称（对于SNMP SNMPv1/v2c），判断如何进行处理：
• 对于 SNMPv3 报文：
如果报文中不携带上下文，且没有为 实例配置 上下文，则对default SNMP BGP default (cid:123)
实例的 MIB 节点进行相应处理。
如果报文中携带上下文，设备上存在对应的 SNMP 上下文（通过系统视图下的(cid:123)
命令创建），且该上下文与为某一个 BGP 实例配置的上下文相同，snmp-agent context则对该 实例的 节点进行相应处理。
BGP MIB其他情况下，不允许对任何 MIB 节点进行处理。
(cid:123)
对于 SNMPv1/v2c 报文：
•如果设备上没有通过系统视图下的 命令将报文中的团体snmp-agent community-map (cid:123)
名映射为 上下文，且没有为 实例配置 上下文，则对 实SNMP default SNMP BGP default例的 MIB 节点进行相应处理。
如果设备上将团体名映射为 SNMP 上下文，设备上存在对应的 SNMP 上下文，且该上下(cid:123)
文与为某一个 BGP 实例配置的上下文相同，则对该 BGP 实例的 MIB 节点进行相应处理。
其他情况下，不允许对任何 MIB 节点进行处理。
(cid:123)
SNMP 上下文和团体名的详细介绍，请参见“网络管理和监控配置指导”中的“SNMP”。

为不同 BGP 实例配置的 SNMP 上下文不能相同。
在同一个 BGP 实例下多次执行本命令，最后一次执行的命令生效。
【举例】
配置 实例 的 上下文为 bgp-abc。
\# BGP abc SNMP <Sysname> system-view [Sysname] bgp 100 instance abc [Sysname-bgp-abc] snmp context-name bgp-abc【相关命令】
• snmp-agent context（网络管理和监控命令参考/SNMP）
• snmp-agent community-map（网络管理和监控命令参考/SNMP）

##### 1.1.147 snmp-agent trap enable bgp

命令用来开启 模块的告警功能。
snmp-agent trap enable bgp BGP命令用来关闭 模块的告警功能。
undo snmp-agent trap enable bgp BGP【命令】
snmp-agent trap enable bgp [ instance instance-name ] undo snmp-agent trap enable bgp [ instance instance-name ]【缺省情况】
BGP 模块的告警功能处于开启状态。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
instance instance-name：开启指定 BGP 实例的告警功能。instance-name 表示 BGP 实例名称，为 1～31 个字符的字符串，区分大小写。如果不指定本参数，则表示开启 default 实例的BGP 告警功能。
【使用指导】
开启 模块的告警功能后，当 的邻居状态变化时 会产生 中规定的告警信BGP BGP BGP RFC 4273息，该信息包含邻居地址、最近一次出现错误的错误码和错误子码、当前的邻居状态。生成的告警信息将发送到设备的 SNMP 模块，通过设置 SNMP 中告警信息的发送参数，来决定告警信息输出的相关属性。
有关告警信息的详细介绍，请参见“网络管理和监控配置指导”中的“SNMP”。
【举例】
开启 告警功能。
\# BGP <Sysname> system-view [Sysname] snmp-agent trap enable bgp

##### 1.1.148 statistics-interval

statistics-interval 命令用来配置 BGP 向监控服务器发送统计信息的周期。
undo statistics-interval 命令用来恢复缺省情况。
【命令】
statistics-interval value undo statistics-interval【缺省情况】
不向监控服务器发送统计信息。
【视图】
视图BMP Server【缺省用户角色】
network-admin【参数】
value：配置 BGP 向监控服务器发送统计信息的周期，取值范围为 1～3600，单位为秒。
【使用指导】
当 BGP 与监控服务器的 TCP 连接建立后，周期性发送统计信息。
【举例】
配置 向监控服务器发送统计信息的周期为 秒。
\# BGP 5 <Sysname> system-view [Sysname] bmp server 5 [Sysname-bmpserver-5] statistics-interval 5

##### 1.1.149 summary automatic

命令用来配置对引入的 IGP 子网路由进行自动聚合。
summary automatic命令用来恢复缺省情况。
undo summary automatic【命令】
summary automatic undo summary automatic【缺省情况】
不对引入的 IGP 子网路由进行自动聚合。
【视图】
BGP IPv4 单播地址族视图BGP-VPN IPv4 单播地址族视图BGP IPv4 组播地址族视图【缺省用户角色】
network-admin

【使用指导】
配置 summary automatic 命令后，BGP 将对通过 import-route 命令引入的 IGP 子网路由进行聚合，从而减少路由信息的数量。
自动聚合生成的路由可以参与手动聚合。
自动聚合生成的路由不会加入到 IP 路由表中。
【举例】
\# 在 BGP IPv4 单播地址族视图下，对引入的 IGP 子网路由进行自动聚合。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] address-family ipv4 unicast [Sysname-bgp-default-ipv4] summary automatic【相关命令】
•aggregate
•import-route

##### 1.1.150 timer

命令用来配置 BGP 会话的存活时间间隔和保持时间。
timer undo timer 命令用来恢复缺省情况。
【命令】
timer keepalive keepalive hold holdtime undo timer【缺省情况】
会话的存活时间间隔为 秒，保持时间为 秒。
BGP 60 180【视图】
BGP 实例视图BGP-VPN 实例视图【缺省用户角色】
network-admin【参数】
keepalive：指定 BGP 会话的存活时间间隔。keepalive 取值范围为 0～21845，keepalive单位为秒。
holdtime：指定 BGP 会话的保持时间。holdtime 取值范围为 0 或 3～65535，单位为秒。
hold保持时间必须大于或等于存活时间的三倍。
【使用指导】
当对等体间建立了 BGP 会话后，它们定时向对端发送 Keepalive 消息，以防止路由器认为 BGP 会话已中断。Keepalive 消息的发送时间间隔称为存活时间间隔。

若路由器在设定的会话保持时间（Holdtime）内未收到对端的 Keepalive 消息或 Update 消息，则认为此 会话已中断，从而断开此 会话。
BGP BGP命令用来配置本地路由器与所有对等体之间 会话的存活时间间隔和保持时间；peer timer BGP timer 命令用来配置本地路由器与指定对等体之间 BGP 会话的存活时间间隔和保持时间。如果同时配置了二者，则使用 命令配置的定时器比使用 命令配置的定时器优先级要timer peer timer低。
如果当前路由器上配置的保持时间与对端设备（对等体）上配置的保持时间不一致，则数值较小者作为协商后的保持时间。
保持时间为 时，不向该对等体发送 消息，与该对等体之间的会话永远不会超时断开；
0 Keepalive当保持时间和存活时间间隔都不为 0 时，将协商的保持时间的三分之一与配置的存活时间间隔比较，取最小值作为存活时间间隔。
配置 命令后，不会影响已建立的 BGP 会话，只对新建立的会话生效。
timer配置 timer 命令后，不会马上断开会话，而是等到其他条件触发会话重建（如复位 BGP 会话）时，再以配置的保持时间协商建立会话。
【举例】
在 实例视图下，配置 会话的存活时间间隔和保持时间分别为 秒和 秒。
\# BGP BGP 60 180 <Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] timer keepalive 60 hold 180【相关命令】
• display bgp peer
• peer timer

##### 1.1.151 timer connect-retry

timer connect-retry 命令用来配置本地路由器与所有对等体/对等体组之间重新建立 BGP 会话的时间间隔。
undo timer connect-retry 命令用来恢复缺省情况。
【命令】
timer connect-retry retry-time undo timer connect-retry【缺省情况】
本地路由器与所有对等体/对等体组之间重新建立 BGP 会话的时间间隔为 32 秒。
【视图】
视图BGP实例视图BGP-VPN【缺省用户角色】
network-admin

【参数】
retry-time：指定重新建立 BGP 会话的时间间隔，取值范围为 1～65535，单位为秒。
【使用指导】
如果要加快本地路由器与指定对等体/ 对等体组之间重新建立 BGP 会话的速度，可以将的值调小，便于路由快速收敛。如果 会话反复 up/down，可以将retry-time BGP retry-time的值调大，从而减轻路由振荡。
使用本命令配置的定时器比使用 peer timer connect-retry 命令配置的定时器优先级要低。
【举例】
\# 在 BGP 实例视图下，配置本地路由器与所有对等体之间重新建立 BGP 会话的时间间隔为 30 秒。
<Sysname> system-view [Sysname] bgp 100 [Sysname-bgp-default] timer connect-retry 30【相关命令】
•peer timer connect-retry

##### 1.1.152 update-first route-policy

update-first route-policy 命令用来配置优先发送指定路由的撤销消息。
undo update-first route-policy 命令用来恢复缺省情况。
【命令】
update-first route-policy route-policy-name undo update-first route-policy【缺省情况】
不支持优先发送指定路由的撤销消息。
【视图】
BGP IPv4 单播地址族视图单播地址族视图BGP-VPN IPv4单播地址族视图BGP IPv6单播地址族视图BGP-VPN IPv6组播地址族视图BGP IPv4组播地址族视图BGP IPv6【缺省用户角色】
network-admin【参数】
route-policy-name：路由策略名称，为 1 ～ 63 个字符的字符串，区分大小写。
【使用指导】
当 BGP 路由器需要撤销大量路由时，撤销所有的路由会耗费一定时间，导致有些流量不能快速切换到有效路径。对于某些重要的、不希望长时间中断的流量，可以通过本配置，确保 路由器BGP

优先发送这些路由的撤销消息，以便将指定流量快速地切换到有效路径上，最大限度地减少流量中断时间。
【举例】
\# 在 BGP IPv4 单播地址族视图下，配置通过路由策略 test-policy 的路由能够被优先撤销。
<Sysname> system-view [Sysname] bgp 1 [Sysname-bgp-default] address-family ipv4 [Sysname-bgp-default-ipv4] update-first route-policy test-policy【相关命令】
• default-route update-first
• route-policy（三层技术-IP 路由命令参考/路由策略）

## 07-策略路由命令

目 录策略路由配置命令

### 1 策略路由

1策略路由

#### 1.1 策略路由配置命令

##### 1.1.1 apply next-hop

命令用来设置报文转发的下一跳。
apply next-hop命令用来取消报文转发下一跳的设置。
undo apply next-hop【命令】
apply next-hop [ vpn-instance vpn-instance-name ] { ip-address [ direct ] [ track track-entry-number ] }&<1-2> undo apply next-hop [ [ vpn-instance vpn-instance-name ] ip-address&<1-2> ]【缺省情况】
未设置报文转发的下一跳。
【视图】
策略节点视图【缺省用户角色】
network-admin【参数】
vpn-instance vpn-instance-name：下一跳所在的 VPN 实例。vpn-instance-name 表示MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。指定的 VPN 实例必须已经存在。
ip-address：下一跳 地址。如果未指定 参数，表示指定的是公网下一跳。
IP vpn-instance direct：指定当前下一跳生效的条件为直连下一跳。
track-entry-number：指定 Track 项的序号，track-entry-number 取值范围为 1～track 1024。
&<1-2>：表示前面的参数最多可以输入 次。
2【使用指导】
用户可以同时配置多个下一跳（通过一次或多次配置本命令实现），起到主备的作用。
配置 undo 命令时，如果指定了下一跳 IP 地址，将取消已配置的该下一跳；如果未指定下一跳 IP地址，将取消已配置的所有下一跳。
【举例】
\# 设置报文的直连下一跳为 1.1.1.1。
<Sysname> system-view [Sysname] policy-based-route aa permit node 11 [Sysname-pbr-aa-11] apply next-hop 1.1.1.1 direct

##### 1.1.2 apply service-chain

apply service-chain 命令用来设置报文的服务链规则。
undo apply service-chain 命令用来恢复缺省情况。
【命令】
apply service-chain path-id service-path-id [ path-index service-patch-index ] undo apply service-chain【缺省情况】
未设置报文的服务链规则。
【视图】
策略节点视图【缺省用户角色】
network-admin【参数】
service-path-id：服务链编号，取值范围为 1～16777215。服务链编号用来唯一确path-id定一条服务链。
service-path-index：服务链节点索引，取值范围 1～255。本参数用来区分一path-index个服务链节点收到来自不同设备的报文。如果只有一台设备向某个服务链节点发送报文，则不需要配置本参数。
【举例】
\# 设置报文中的服务链编号为 1，服务链节点索引为 10。
<Sysname> system-view [Sysname] policy-based-route aa permit node 5 [Sysname-pbr-aa-5] apply service-chain path-id 1 path-index 10

##### 1.1.3 description

命令用来配置当前策略节点的描述信息。
description命令用来恢复缺省情况。
undo description【命令】
description text undo description【缺省情况】
未配置策略节点的描述信息。
【视图】
策略节点视图

【缺省用户角色】
network-admin【参数】
text：策略节点的描述信息，为 1～127 个字符的字符串，区分大小写。
【举例】
配置策略节点的描述信息为“Officeuse”。
\# <Sysname> system-view [Sysname] policy-based-route 1 permit node 1 [Sysname-pbr-1-1] description Officeuse

##### 1.1.4 display ip policy-based-route

命令用来显示已经配置的策略。
display ip policy-based-route【命令】
display ip policy-based-route [ policy policy-name ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
policy-name：显示指定的策略。policy-name 表示策略名，唯一标识一个策略，为policy 1～19 个字符的字符串，区分大小写。如果未指定本参数，则显示所有已经配置的策略。
【举例】
\# 显示所有已经配置的策略。
<Sysname> display ip policy-based-route Policy name: aaa node 1 permit:
if-match acl 2000 apply next-hop 1.1.1.1表1-1 display ip policy-based-route 命令显示信息描述表字段 描述Policy name 策略名node 1 permit 节点1的匹配模式为允许满足ACL的报文被匹配if-match acl apply next-hop 为匹配的报文指定下一跳

【相关命令】
• policy-based-route

##### 1.1.5 display ip policy-based-route interface

display ip policy-based-route interface 命令用来显示接口下转发策略路由的配置信息和统计信息。
【命令】
display ip policy-based-route interface interface-type interface-number [ slot slot-number ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
interface-number：用来指定接口的类型和编号。
interface-type slot-number：显示指定成员设备上的信息。slot-number 表示设备在 IRF 中的成员编slot号。如果未指定本参数，将显示主设备上的信息。
【举例】
\# 显示 VLAN 接口 2 下转发策略路由的配置信息和统计信息。
<Sysname> display ip policy-based-route interface vlan-interface 2 Policy based routing information for interface Vlan-interface2:
Policy name: aaa node 0 deny:
Matched: 0 node 1 permit:
if-match acl 3999 Matched: 0 node 2 permit:
if-match acl 2000 apply next-hop 2.2.2.2 Matched: 0 node 5 permit:
if-match acl 3101 apply next-hop 1.1.1.1 Matched: 0 Total matched: 0 <Sysname> display ip policy-based-route interface vlan-interface 2 Policy based routing information for interface Vlan-interface2:
Policy name: aaa node 0 deny:
Matched: 0

node 1 permit:
if-match acl 3999 Matched: 0 node 2 permit:
if-match acl 2000 apply next-hop 2.2.2.2 Matched: 0 node 5 permit:
if-match acl 3101 apply next-hop 1.1.1.1 Matched: 0 Total matched: 0表1-2 display ip policy-based-route interface 命令显示信息描述表字段 描述接口下转发策略路由的配置信息和统计信息（failed表示策略下发驱动失败）
Policy based routing information for interface XXXX(failed)
对于设备上的全局口（如 VLAN 接口）和物理口，只有指定 slot 后，才会显示括号内的信息。
Policy name 策略名节点的匹配模式为允许（permit）/拒绝（deny）（not support表示设备不支持该节点设置的规则；no resource表示设备的ACL等资源不足，为该节点分配ACL等资源失败）
node 0 deny(not support)
node 2 permit(no resource)
对于设备上的全局口（如 VLAN 接口）和物理口，只有指定 slot 后，才会显示括号内的信息。
满足ACL的报文被匹配if-match acl apply next-hop 为匹配的报文指定下一跳节点匹配成功的次数（no statistics resource表示统计资源不足）
Matched: 0 (no statistics resource)
对于设备上的全局口（如 VLAN 接口）和物理口，只有指定 slot 后，才会显示括号内的信息。
策略所有节点匹配成功的次数Total matched【相关命令】
•reset ip policy-based-route statistics

##### 1.1.6 display ip policy-based-route local

命令用来显示本地策略路由的配置信息和统计信息。
display ip policy-based-route local

【命令】
display ip policy-based-route local [ slot slot-number ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
slot-number：显示指定成员设备上本地策略路由的配置信息和统计信息。slot-number slot表示设备在 IRF 中的成员编号。如果未指定本参数，将显示主设备上本地策略路由的配置信息和统计信息。
【举例】
显示本地策略路由的配置信息和统计信息。
\# <Sysname> display ip policy-based-route local Policy based routing information for local:
Policy name: aaa node 0 deny:
Matched: 0 node 1 permit:
if-match acl 3999 Matched: 0 node 2 permit:
if-match acl 2000 apply next-hop 2.2.2.2 Matched: 0 node 5 permit:
if-match acl 3101 apply next-hop 1.1.1.1 Matched: 0 Total matched: 0表1-3 display ip policy-based-route local 命令显示信息描述表字段 描述Policy based routing information for local 本地策略路由的配置信息和统计信息策略名Policy name node 0 deny/node 2 permit 节点的匹配模式为允许（permit）/拒绝（deny）
if-match acl 满足ACL的报文被匹配为匹配的报文指定下一跳apply next-hop Matched: 0 节点匹配成功的次数Total matched 策略所有节点匹配成功的次数

【相关命令】
• reset ip policy-based-route statistics

##### 1.1.7 display ip policy-based-route setup

命令用来显示已经应用的策略路由信息。
display ip policy-based-route setup【命令】
display ip policy-based-route setup【视图】
任意视图【缺省用户角色】
network-admin network-operator【举例】
\# 显示已经应用的策略路由信息。
<Sysname> display ip policy-based-route setup Policy name Type Interface pr01 Forward Vlan-interface2 aaa Local N/A表1-4 命令显示信息描述表display ip policy-based-route setup字段 描述Policy name 策略名开启策略路由类型，取值为Type • Forward：转发策略类型
• Local：本地策略路由类型应用策略的接口Interface【相关命令】
•ip policy-based-route

##### 1.1.8 if-match acl

命令用来设置 ACL 匹配规则。
if-match acl命令用来恢复缺省情况。
undo if-match acl【命令】
if-match acl { acl-number | name acl-name } undo if-match acl

【缺省情况】
未设置 ACL 匹配规则。
【视图】
策略节点视图【缺省用户角色】
network-admin【参数】
acl-number：访问控制列表号，取值范围为 2000～3999。其中：
基本 ACL，acl-number 取值范围为 2000～2999；
•高级 ACL，acl-number 取值范围为 3000～3999。
•acl-name：指定 的名称。acl-name 表示 的名称，为 1～63 个字符的字符串，name ACL ACL不区分大小写，必须以英文字母 a～z 或 A～Z 开头。为避免混淆，ACL 的名称不允许使用英文单词 all。只有指定基本 ACL 或高级 ACL 的 acl-name 才生效。
【举例】
\# 设置满足 ACL 2011 的报文被匹配。
<Sysname> system-view [Sysname] policy-based-route aa permit node 11 [Sysname-pbr-aa-11] if-match acl 2011 \# 设置满足 ACL 名称为 aaa 的报文被匹配。
<Sysname> system-view [Sysname] policy-based-route aa permit node 11 [Sysname-pbr-aa-11] if-match acl name aaa

##### 1.1.9 if-match service-chain

命令用来设置服务链匹配规则。
if-match service-chain命令用来恢复缺省情况。
undo if-match service-chain【命令】
if-match service-chain { path-id service-path-id [ path-index service-patch-index ] } undo if-match service-chain [ path-id service-path-id ] ]【缺省情况】
未配置服务链匹配规则。
【视图】
策略节点视图【缺省用户角色】
network-admin

【参数】
path-id service-path-id：服务链编号，取值范围为 1～16777215。服务链编号用来唯一确定一条服务链。
service-path-index：服务链节点索引，取值范围 1～255。本参数用来区分一path-index个服务链节点收到的来自不同设备的报文。如果只有一台设备向某个服务链节点发送报文，则不需要配置本参数。
【举例】
\# 设置服务链匹配规则，匹配服务链编号为 1，服务链节点索引为 10 的报文。
<Sysname> system-view [Sysname] policy-based-route aa permit node 5 [Sysname-pbr-aa-5] if-match service-chain path-id 1 path-index 10

##### 1.1.10 ip local policy-based-route

ip local policy-based-route 命令用来对本地报文应用策略。
undo ip local policy-based-route 命令用来恢复缺省情况。
【命令】
ip local policy-based-route policy-name undo ip local policy-based-route【缺省情况】
未对本地报文应用策略。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
policy-name：策略名，唯一标识一个策略，为 1～19 个字符的字符串，区分大小写。该策略必须已经存在。
【使用指导】
对本地报文只能应用一个策略，应用新的策略前必须删除本地原来已经应用的策略。
对本地报文应用的策略将对本地产生的所有报文（除了本地发送给自己的报文）进行匹配。若无特殊需求，建议用户不要配置本地策略路由。
【举例】
\# 对本地报文应用策略 aaa。
<Sysname> system-view [Sysname] ip local policy-based-route aaa【相关命令】
• display ip policy-based-route setup

• policy-based-route

##### 1.1.11 ip policy-based-route

命令用来对接口转发的报文应用策略。
ip policy-based-route命令用来恢复缺省情况。
undo ip policy-based-route【命令】
ip policy-based-route policy-name undo ip policy-based-route【缺省情况】
未对接口转发的报文应用策略。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
policy-name：策略名，唯一标识一个策略，为 1～19 个字符的字符串，区分大小写。该策略必须已经存在。
【举例】
\# 对 VLAN 接口 2 转发的报文应用策略 aaa。
<Sysname> system-view [Sysname] interface vlan-interface 2 [Sysname-Vlan-interface2] ip policy-based-route aaa【相关命令】
• display ip policy-based-route setup
• policy-based-route

##### 1.1.12 policy-based-route

policy-based-route 命令用来创建策略节点，并进入策略节点视图。如果指定的策略节点已创建，则该命令直接用来进入该策略节点的视图。
命令用来删除已创建的策略或策略节点。
undo policy-based-route【命令】
policy-based-route policy-name [ deny | permit ] node node-number undo policy-based-route policy-name [ deny | node node-number | permit ]【缺省情况】
不存在策略节点。
【视图】
系统视图

【缺省用户角色】
network-admin【参数】
policy-name：策略名，唯一标识一个策略，为 1～19 个字符的字符串，区分大小写。
deny：指定策略节点的匹配模式为拒绝模式。
permit：指定策略节点的匹配模式为允许模式。缺省匹配模式为 permit。
node node-number：策略节点编号。节点编号越小优先级越高，先对优先级高的节点进行匹配操作。node-number 的取值范围为 0～255。
【使用指导】
删除策略之前，必须先取消该策略在所有接口或者本地上的应用，否则删除失败。
配置 命令时，如果指定了策略节点，将删除指定的节点；如果指定了节点模式，将按模式删undo除策略内所有与该模式匹配的所有节点；如果两者都未指定，将删除整个策略。
【举例】
\# 创建一个策略 policy1，其节点序列号为 10，匹配模式为 permit，并进入策略节点视图。
<Sysname> system-view [Sysname] policy-based-route policy1 permit node 10 [Sysname-pbr-policy1-10]【相关命令】
•display ip policy-based-route

##### 1.1.13 reset ip policy-based-route statistics

命令用来清除策略路由的统计信息。
reset ip policy-based-route statistics【命令】
reset ip policy-based-route statistics [ policy policy-name ]【视图】
用户视图【缺省用户角色】
network-admin【参数】
policy policy-name：清除指定策略的统计信息。policy-name 表示策略名，唯一标识一个策略，为 1～19 个字符的字符串，区分大小写。如果未指定本参数，则清除所有策略路由的统计信息。
【举例】
\# 清除所有配置策略的统计信息。
<Sysname> reset ip policy-based-route statistics【相关命令】
• display ip policy-based-route egress interface

• display ip policy-based-route interface
•
display ip policy-based-route local

## 08-IPv6静态路由命令

目 录静态路由配置命令

### 1 IPv6静态路由

#### 1.1 IPv6静态路由配置命令

##### 1.1.1 delete ipv6 static-routes all

命令用来删除所有 静态路由。
delete ipv6 static-routes all IPv6【命令】
delete ipv6 [ vpn-instance vpn-instance-name ] static-routes all【视图】
系统视图【缺省用户角色】
network-admin【参数】
： 删 除 指 定 的 所 有 静 态 路 由 。
vpn-instance vpn-instance-name VPN IPv6 vpn-instance-name 表示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果不指定该参数，则删除公网实例下的所有 IPv6 静态路由。
【使用指导】
使用本命令删除 IPv6 静态路由时，系统会提示确认，确认后才会删除所配置的所有 IPv6 静态路由。
【举例】
删除所有 静态路由。
\# IPv6 <Sysname> system-view [Sysname] delete ipv6 static-routes all This will erase all IPv6 static routes and their configurations, you must reconf igure all static routes.
Are you sure?[Y/N]:y【相关命令】
• ipv6 route-static

##### 1.1.2 display ipv6 route-static nib

display ipv6 route-static nib 命令用来显示 IPv6 静态路由下一跳信息。
【命令】
display ipv6 route-static nib [ nib-id ] [ verbose ]【视图】
任意视图【缺省用户角色】
network-admin

network-operator【参数】
nib-id：路由邻居 值，取值范围为十六进制数 1～ffffffff。
ID verbose：显示详细信息。如果未指定本参数，则显示概要信息。
【举例】
\# 显示 IPv6 静态路由邻居信息与下一跳信息。
<Sysname> display ipv6 route-static nib Total number of nexthop(s): 35 NibID: 0x21000000 Sequence: 0 Type: 0x41 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: 2::3 IFIndex: 0x0 LocalAddr: ::
TopoNthp: Invalid ExtType: 0x0 NibID: 0x21000001 Sequence: 1 Type: 0x41 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: 3::4 IFIndex: 0x0 LocalAddr: ::
TopoNthp: Invalid ExtType: 0x0表1-1 display ipv6 route-static nib 命令显示信息描述表字段 描述Total number of nexthop(s) 总的NIB个数ID号NibID NIB Sequence NIB序列号Type NIB类型Flushed 是否下刷FIB UserKey0 NIB协议保留数据1 UserKey1 NIB协议保留数据2 VrfNthp 下一跳所在VPN索引，显示为0表示公网下一跳信息Nexthop IFIndex 接口索引LocalAddr 本地接口地址（暂不支持）下一跳所在拓扑索引，显示为0表示公网拓扑（目前IPv6不支持子拓TopoNthp扑，显示为Invalid）

字段 描述ExtType NIB扩展类型\# 显示 IPv6 静态路由邻居与下一跳的详细信息。
<Sysname> display ipv6 route-static nib verbose Total number of nexthop(s): 35 NibID: 0x21000000 Sequence: 0 Type: 0x41 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: 2::3 IFIndex: 0x0 LocalAddr: ::
TopoNthp: Invalid ExtType: 0x0 RefCnt: 1 FlushRefCnt: 0 Flag: 0x12 Version: 1 1 nexthop(s):
PrefixIndex: 0 OrigNexthop: 2::3 RelyDepth: 2 RealNexthop: ::
Interface: NULL0 LocalAddr: ::
TunnelCnt: 0 Vrf: default-vrf TunnelID: N/A Topology:
Weight: 0 NibID: 0x21000001 Sequence: 1 Type: 0x41 Flushed: Yes UserKey0: 0x0 VrfNthp: 0 UserKey1: 0x0 Nexthop: 3::4 IFIndex: 0x0 LocalAddr: ::
TopoNthp: Invalid ExtType: 0x0 RefCnt: 1 FlushRefCnt: 0 Flag: 0x12 Version: 1 1 nexthop(s):
PrefixIndex: 0 OrigNexthop: 3::4 RelyDepth: 1 RealNexthop: ::
Interface: Vlan11 LocalAddr: ::
TunnelCnt: 0 Vrf: default-vrf TunnelID: N/A Topology:
Weight: 0表1-2 display ipv6 route-static nib verbose 命令显示信息描述表字段 描述x nexthop(s) 下一跳具体值（前面数值表示下一跳个数）
PrefixIndex 等价时下一跳序号Vrf VPN实例名，显示为default-vrf表示公网

字段 描述OrigNexthop 原始下一跳RealNexthop 真实下一跳出接口Interface localAddr 本地接口地址RelyDepth 迭代深度TunnelCnt 迭代到隧道的个数迭代到隧道的ID TunnelID（暂不支持）拓扑名称，显示为base表示公网拓扑（目前IPv6不支持子拓扑，显示Topology为空）
Weight 等价路由各路由的权重，取值为0表示不是等价路由下一跳信息的引用计数RefCnt FlushRefCnt 下一跳信息的下刷引用计数Flag 下一跳信息的标志位Version 下一跳信息的版本号ExtType NIB扩展类型

##### 1.1.3 display ipv6 route-static routing-table

display ipv6 route-static routing-table 命令用来显示 IPv6 静态路由表信息。
【命令】
display ipv6 route-static routing-table [ vpn-instance vpn-instance-name ] [ ipv6-address prefix-length ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
vpn-instance vpn-instance-name：显示指定 VPN 的信息。vpn-instance-name 表示MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则显示公网的信息。
：目的 地址。
ipv6-address IPv6 prefix-length：前缀长度，取值范围为 0～128。

【举例】
\# 显示 IPv6 静态路由表信息。
<Sysname> display ipv6 route-static routing-table Total number of routes: 5 Status: * - valid
*Destination: 1::1/128 NibID: 0x21000000 NextHop: 2::2 MainNibID: N/A BkNextHop: N/A BkNibID: N/A Interface: Vlan-interface11 TableID: 0xa BkInterface: N/A Flag: 0x80d0a BfdSrcIp: N/A DbIndex: 0x3 BfdIfIndex: 0x0 Type: Normal BfdVrfIndex: 0 TrackIndex: 0xffffffff Label: NULL Preference: 60 vrfIndexDst: 0 BfdMode: N/A vrfIndexNH: 0 Permanent: 0 Tag: 0
*Destination: 1::1234/128 NibID: 0x21000000 NextHop: 2::2 MainNibID: N/A BkNextHop: N/A BkNibID: N/A Interface: NULL0 TableID: 0xa BkInterface: N/A Flag: 0x80d0a BfdSrcIp: N/A DbIndex: 0x1 BfdIfIndex: 0x0 Type: Normal BfdVrfIndex: 0 TrackIndex: 0xffffffff Label: NULL Preference: 60 vrfIndexDst: 0 BfdMode: N/A vrfIndexNH: 0 Permanent: 0 Tag: 0表1-3 display ipv6 route-static routing-table 命令显示信息描述表字段 描述Total number of routes 总的路由条数Destination 目的地址/掩码NibID 下一跳信息ID FRR静态路由主下一跳信息ID MainNibID BkNibID FRR 静态路由备下一跳信息 ID NextHop 此路由的下一跳地址此路由的备份下一跳地址BkNextHop

字段 描述Interface 出接口，即到该目的网段的数据包将从此接口发出BkInterface 备份出接口路由所在的表ID TableID Flag 路由标志位DbIndex 路由所在DB的DB索引路由类型：
• Normal：普通类型的静态路由Type
• DHCP：DHCP 类型的静态路由
• NAT：NAT 类型的静态路由BfdSrcIp BFD非直连会话源地址BfdIfIndex BFD使用的接口索引BFD所在VPN索引，显示为0表示公网BfdVrfIndex BFD模式：
• N/A：未配置 BFD 会话BfdMode
• Ctrl：控制报文方式的 BFD 会话
• Echo：echo 报文方式的 BFD 会话TrackIndex NQA Track索引Label 标签Preference 路由优先级vrfIndexDst 目的所在VPN，显示为0表示公网下一跳所在VPN，显示为0表示公网vrfIndexNH Permanent 永久静态路由标志（1表示永久静态路由）
Tag 路由标记

##### 1.1.4 ipv6 route-static

命令用来配置 静态路由。
ipv6 route-static IPv6命令用来删除指定的 IPv6 静态路由。
undo ipv6 route-static【命令】
ipv6 route-static ipv6-address prefix-length { interface-type interface-number [ next-hop-address ] [ bfd { control-packet | echo-packet } [ bfd-source ipv6-address ] | permanent ] | [ vpn-instance d-vpn-instance-name ] next-hop-address [ bfd control-packet bfd-source ipv6-address | permanent ] } [ preference preference ] [ tag tag-value ] [ description text ]

ipv6 route-static vpn-instance s-vpn-instance-name ipv6-address prefix-length { interface-type interface-number [ next-hop-address ] [ bfd { control-packet | echo-packet } [ bfd-source ipv6-address ] | permanent ] | next-hop-address [ public ] [ bfd control-packet bfd-source ipv6-address | permanent ] | vpn-instance d-vpn-instance-name next-hop-address [ bfd control-packet bfd-source ipv6-address | permanent ] } [ preference preference ] [ tag tag-value ] [ description text ] undo ipv6 route-static vpn-instance s-vpn-instance-name ipv6-address prefix-length [ interface-type interface-number [ next-hop-address ] | next-hop-address [ public ] | vpn-instance d-vpn-instance-name next-hop-address ] [ preference preference ]【缺省情况】
未配置 IPv6 静态路由。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
ipv6-address prefix-length：IPv6 地址及前缀长度。
interface-type interface-number：路由出接口的类型和编号。对于接口类型为非 P2P 接口（包括 NBMA 类型接口或广播类型接口），必须指定下一跳地址。
next-hop-address：下一跳 IPv6 地址。
bfd：使能 BFD（Bidirectional Forwarding Detection，双向转发检测）功能，对静态路由下一跳的可达性进行快速检测。
control-packet：通过 BFD 控制报文方式实现 BFD 功能。
ipv6-address：BFD 源 IPv6 地址。
bfd-source echo-packet：通过 BFD echo 报文方式实现 BFD 功能。
permanent ：指定为永久 IPv6 静态路由。即使在出接口 down 时，配置的永久 IPv6 静态路由仍然保持 active 状态。
public：指定静态路由下一跳处于公网实例。
d-vpn-instance-name：指定目的 VPN。d-vpn-instance-name 表示 MPLS vpn-instance的 实例名称，为 1～31 个字符的字符串，区分大小写。如果指定目的 VPN，IPv6 静L3VPN VPN态路由将根据配置的下一跳 IPv6 地址在目的 VPN 中查找出接口。
preference preference：路由的优先级，取值范围为 1～255，缺省值为 60。
tag-value：静态路由 值，用于标识该条静态路由，以便在路由策略中根据 对路由tag Tag Tag进行灵活的控制。 tag-value 的取值范围为 1 ～ 4294967295 ，缺省值为 0 。关于路由策略的详细信息，请参见“三层技术-IP 路由配置指导”中的“路由策略”。
text：静态路由描述信息。text 为 1～60 个字符的字符串，除“?”外，可以包description含空格等特殊字符。

s-vpn-instance-name：指定源 VPN。s-vpn-instance-name 表示 MPLS vpn-instance的 实例名称，为 1～31 个字符的字符串，区分大小写。每个 都有自己的路由表，L3VPN VPN VPN配置的 IPv6 静态路由将被加入指定 VPN 的路由表。
【使用指导】
如果配置的 IPv6 静态路由指定目的地址为::/0（前缀长度为 0），则表示配置了一条 IPv6 缺省路由。
如果报文的目的地址无法匹配路由表中的任何一项，设备将选择 缺省路由来转发 报文。
IPv6 IPv6在配置静态路由时，可以指定出接口（interface-type interface-number），也可指定下一跳地址（next-hop-address），具体采用哪种方法，需要根据实际情况而定：
如果出接口类型为广播或者 类型，必须指定下一跳地址。
• NBMA如果出接口类型为点到点类型，配置时可以只指定出接口，不指定下一跳地址。这样，即使
•对端地址发生了变化也无须改变配置。
配置 IPv6 静态路由与 BFD 联动时，需要注意的是：
• 对于直连下一跳，当指定的出接口类型为非 P2P 接口时，建议用户通过 bfd-source 命令指定 BFD 源 IPv6 地址，该地址必须为出接口的 IPv6 地址，且与下一跳 IPv6 地址处在同一网段。
如果下一跳 IPv6 地址指定的是链路本地地址，本参数也必须是链路本地地址。
对于直连下一跳或者非直连下一跳，如果要指定 BFD 源 IPv6 地址，那么下一跳 IPv6 地址和
•源 地址必须成对配置，即本端指定的下一跳 地址是对端的 源 地址，BFD IPv6 IPv6 BFD IPv6本端指定的 BFD 源 IPv6 地址是对端的下一跳 IPv6 地址。
配置 IPv6 静态路由时需要注意的是：
• 路由振荡时，使能 BFD 检测功能可能会加剧振荡，需谨慎使用。关于 BFD 的详细介绍，请参考“可靠性配置指导”中的“BFD”。
• 配置 BFD echo 报文方式时，下一跳 IPv6 地址必须为全球单播地址。
• 参数 permanent 不能和 bfd 一起进行配置。
【举例】
\# 配置 IPv6 静态路由，该路由的目的地址为 1:1:2::/64，下一跳地址为 1:1:3::1。
<Sysname> system-view [Sysname] ipv6 route-static 1:1:2:: 64 1:1:3::1【相关命令】
• display ipv6 routing-table protocol（三层技术-IP 路由命令参考/IP 路由基础）

##### 1.1.5 ipv6 route-static default-preference

命令用来配置 静态路由的缺省优先级。
ipv6 route-static default-preference IPv6命令用来恢复缺省情况。
undo ipv6 route-static default-preference【命令】
ipv6 route-static default-preference default-preference undo ipv6 route-static default-preference【缺省情况】
IPv6 静态路由的缺省优先级为 60。

【视图】
系统视图【缺省用户角色】
network-admin【参数】
default-preference：IPv6 静态路由缺省优先级的值，取值范围为 1～255。
【使用指导】
如果在配置 IPv6 静态路由时没有指定优先级，就会使用缺省优先级。
重新配置缺省优先级后，新设置的缺省优先级仅对新增的 静态路由有效。
IPv6【举例】
\# 配置 IPv6 静态路由的缺省优先级为 120。
<Sysname> system-view [Sysname] ipv6 route-static default-preference 120【相关命令】
protocol（三层技术-IP 路由命令参考/IP 路由基础）
• display ipv6 routing-table

## 09-RIPng命令

目 录配置命令

### 1 RIPng

1 RIPng

#### 1.1 RIPng配置命令

##### 1.1.1 checkzero

命令用来使能 RIPng 报文的零域检查功能。
checkzero命令用来关闭零域检查功能。
undo checkzero【命令】
checkzero undo checkzero【缺省情况】
报文的零域检查功能处于使能状态。
RIPng【视图】
RIPng 视图【缺省用户角色】
network-admin【使用指导】
RIPng 报文头部中的一些字段必须配置为 0，也称为零域。使能 RIPng 报文的零域检查后，如果报文头部零域中的值不为零，这些报文将被丢弃，不做处理。
【举例】
\# 关闭进程号为 100 的 RIPng 进程对 RIPng 报文的零域检查功能。
<Sysname> system-view [Sysname] ripng 100 [Sysname-ripng-100] undo checkzero

##### 1.1.2 default cost

命令用来配置引入路由的缺省度量值。
default cost命令用来恢复缺省情况。
undo default cost【命令】
default cost cost-value undo default cost【缺省情况】
引入路由的缺省度量值为 0 。
【视图】
RIPng 视图

【缺省用户角色】
network-admin【参数】
cost-value：引入路由的缺省度量值，取值范围为 0～16。
【使用指导】
当使用 命令从其它协议引入路由时，如果不指定具体的度量值，则引入路由的度import-route量值为 default cost 所指定的值。
【举例】
\# 配置引入路由的缺省度量值为 2。
<Sysname> system-view [Sysname] ripng 100 [Sysname-ripng-100] default cost 2【相关命令】
•import-route

##### 1.1.3 display ripng

display ripng 命令用来显示指定 RIPng 进程的当前运行状态及配置信息。
【命令】
display ripng [ process-id ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：RIPng 进程号，取值范围为 1～65535。如果未指定本参数，则显示所有已配置的RIPng 进程的信息。
【举例】
显示所有已配置的 进程的当前运行状态及配置信息。
\# RIPng <Sysname> display ripng Public VPN-instance name:
RIPng process: 1 Preference: 100 Routing policy: abc Fast-reroute:
Routing policy: abc Checkzero: Enabled Default cost: 0

Maximum number of load balanced routes: 6 Update time : 30 secs Timeout time : 180 secs Suppress time : 120 secs Garbage-collect time : 120 secs Update output delay: 20(ms) Output count: 3 Graceful-restart interval: 60 secs Triggered Interval : 5 50 200 Number of periodic updates sent: 256 Number of trigger updates sent: 1表1-1 display ripng 命令显示信息描述表字段 描述Public VPN-instance name RIPng进程运行在公网实例下RIPng进程应用于指定VPN实例Private VPN-instance name RIPng Process RIPng进程号Preference RIPng路由优先级路由策略Routing policy Fast-reroute RIPng快速重路由RIPng报文头部的零域检查功能：Enabled表示使能，Disabled表示未Checkzero使能Default cost 引入路由的缺省度量值Maximum number of load balanced等价路由的最大数目routes Update time Update定时器的值，单位为秒Timeout time Timeout定时器的值，单位为秒Suppress定时器的值，单位为秒Suppress time Garbage-collect time Garbage-Collect定时器的值，单位为秒Update output delay 接口发送RIPng报文的时间间隔，单位为毫秒Output count 接口一次发送RIPng报文的最大个数重启间隔时间，单位为秒Graceful-restart interval GR Triggered Interval 发送触发更新的时间间隔Number of periodic updates sent 定时发送的RIPng更新报文的统计数量Number of trigger updates sent 触发发送的RIPng更新报文的统计数量

##### 1.1.4 display ripng database

display ripng database 命令用来显示指定 RIPng 进程发布数据库的所有激活路由。
【命令】
display ripng process-id database [ ipv6-address prefix-length ]

【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：RIPng 进程号，取值范围为 1～65535。
prefix-length：显示指定 IPv6 地址的激活路由信息。ipv6-address 表示ipv6-address地址；prefix-length 表示 地址前缀长度，取值范围为 0～128。
IPv6 IPv6【举例】
\# 显示进程号为 1 的 RIPng 进程发布数据库中的激活路由。
<Sysname> display ripng 1 database 1::/64, cost 0, RIPng-interface 10::/32, cost 0, imported 2::2/128, via FE80::20C:29FF:FE7A:E3E4, cost 1表1-2 display ripng database 命令显示信息描述表字段 描述度量值cost RIPng-interface 从使能RIPng协议的接口学来的路由imported 表示该条路由是从其它路由协议引入的via 下一跳IPv6地址

##### 1.1.5 display ripng graceful-restart

display ripng graceful-restart 命令用来显示 RIPng 进程的 GR 状态信息。
【命令】
display ripng [ process-id ] graceful-restart【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：RIPng 进程号，取值范围为 1～65535。

【举例】
\# 显示 RIPng 1 进程的 GR 状态信息。
<Sysname> display ripng 1 graceful-restart RIPng process: 1 Graceful Restart capability : Enabled Current GR state : Normal Graceful Restart period : 60 seconds Graceful Restart remaining time: 0 seconds表1-3 命令显示信息描述表display ripng graceful-restart字段 描述RIPng process RIPng进程号GR使能状态Graceful Restart capability • Enabled：使能了 GR 能力
• Disabled：关闭了 GR 能力当前GR所处状态Current GR state • Under GR：进程正在 GR
• Normal：普通状态Graceful Restart period GR间隔Graceful Restart remaining time GR结束剩余时间

##### 1.1.6 display ripng interface

命令用来显示指定 进程的接口信息。
display ripng interface RIPng【命令】
display ripng process-id interface [ interface-type interface-number ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：RIPng 进程号，取值范围为 1～65535。
interface-number：接口类型和编号。如果未指定本参数，则显示指定 RIPng interface-type进程的所有接口信息。
【举例】
\# 显示 RIPng 进程 1 的接口信息。
<Sysname> display ripng 1 interface Total: 1

Interface: Vlan-interface100 Link-local address: FE80::20C:29FF:FEC8:B4DD Split-horizon: On Poison-reverse: Off MetricIn: 0 MetricOut: 1 Default route: Off Update output delay: 20 (ms) Output count: 3 Primary path detection mode: BFD echo Summary address:
1::/16表1-4 display ripng interface 命令显示信息描述表字段 意义Total 运行RIPng协议的接口总数Interface 运行RIPng协议的接口的名称运行RIPng协议的接口的链路本地地址Link-local address Split-horizon 是否使能了水平分割（On表示使能，Off表示关闭）
Poison-reverse 是否使能了毒性逆转（On表示使能，Off表示关闭）
MetricIn/MetricOut 接收/发送路由时添加的附加度量值是否配置了发布缺省路由以及发布缺省路由的模式/取消发布缺省路由/缺省路由处于garbage-collect时间：
• 配置了发布缺省路由：此时从接口发布缺省路由的模式有两种Only/Originate。Only 表示从接口只发布缺省路由，Originate 表示同时发布缺省路由和其他 路由。处于这种状态时，路由器相应的显示：
RIPng Only，或者Default route: Default route: Originate Default route
• 取消发布缺省路由：表示当前没有配置发布缺省路由或者是取消发布默认路由后 garbage-collect 已经超时，此时接口不发送 RIPng 的缺省路由。
处于这种状态时，路由器显示：Default route: Off
• 缺省路由正处于garbage-collect时间：取消发布缺省路由配置后，缺省路由会进入 garbage-collect 状态，此时从接口发送 metric 为 16 的缺省路由。处于这种状态时，路由器显示：Default route: In garbage-collection status (xs)
Update output delay 接口发送 RIPng 报文的时间间隔，单位为毫秒Output count 接口一次发送RIPng报文的最大个数Default route cost RIPng接口下配置发布缺省路由的cost值主链路检测方式：
Primary path detection mode BFD echo：BFD echo报文检测方式在接口配置的聚合的IPv6地址以及被聚合的路由的IPv6前缀Summary address

##### 1.1.7 display ripng neighbor

display ripng neighbor 命令用来显示 RIPng 进程的邻居信息。

【命令】
display ripng process-id neighbor [ interface-type interface-number ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：RIPng 进程号，取值范围为 1～65535。
interface-number：接口类型和编号。如果未指定本参数，将显示interface-type RIPng的所有邻居信息。
【举例】
\# 显示 RIPng 进程 1 的邻居信息。
<Sysname> display ripng 1 neighbor Neighbor Address: FE80::230:FF:FE00:0 Interface : Vlan-interface1 Version : RIPng version 1 Last update: 00h00m27s Bad packets: 0 Bad routes : 0表1-5 display ripng neighbor 命令显示信息描述表字段 描述Neighbor Address 邻居接口的链路本地地址Interface 邻居接口名称Version 收到邻居RIPng报文的版本上次收到邻居更新报文距离现在时间Last update

##### 1.1.8 display ripng non-stop-routing

display ripng non-stop-routing 命令用来显示 RIPng 进程的 NSR 状态信息。
【命令】
display ripng [ process-id ] non-stop-routing【视图】
任意视图【缺省用户角色】
network-admin network-operator

【参数】
process-id：RIPng 进程号，取值范围为 1～65535。
【举例】
\# 显示 RIPng 1 进程的 NSR 状态信息。
<Sysname> display ripng 1 non-stop-routing RIPng process: 1 Nonstop Routing capability: Enabled Current NSR state : Finish表1-6 命令显示信息描述表display ripng non-stop-routing字段 描述RIPng process RIPng进程号NSR使能状态：
Nonstop Routing capability • Enabled：使能 NSR
• Disabled：不使能 NSR当前NSR所处状态：
• Initialization：初始准备
• Smooth：数据平滑Current NSR state
• Advertising：发布路由
• Redistribution：路由引入处理
• Finish：完成

##### 1.1.9 display ripng route

命令用来显示指定 进程的路由信息。
display ripng route RIPng【命令】
display ripng process-id route [ ipv6-address prefix-length [ verbose ] | peer ipv6-address | statistics ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：RIPng 进程号，取值范围为 1～65535。
ipv6-address prefix-length：显示指定 IPv6 地址的路由信息。ipv6-address 表示 IPv6地址；prefix-length 表示 IPv6 地址前缀长度，取值范围为 0～128。

verbose：显示当前 RIPng 路由表中的指定前缀路由的所有路由信息。如果未指定本参数，则只显示指定 目的地址和前缀的最优 路由。
IPv6 RIPng ipv6-address：显示从指定邻居学到的所有路由信息。
peer statistics：显示路由的统计信息。路由的统计信息包括路由总数目，各个邻居的路由数目。
【举例】
\# 显示进程号为 1 的 RIPng 进程的路由信息。
<Sysname> display ripng 1 route Route Flags: A - Aging, S - Suppressed, G - Garbage-collect, D – Direct O - Optimal, F - Flush to RIB
---------------------------------------------------------------- Peer FE80::20C:29FF:FED4:7171 on Vlan-interface100 Destination 4::4/128, via FE80::20C:29FF:FED4:7171, cost 1, tag 0, AOF, 5 secs Local route Destination 3::3/128, via ::, cost 0, tag 0, DOF Destination 6::/64, via ::, cost 0, tag 0, DOF显示进程号为 的 进程中指定地址 的所有路由信息。
\# 1 RIPng 3::3/128 <Sysname> display ripng 1 route 3::3 128 verbose Route Flags: A - Aging, S - Suppressed, G - Garbage-collect, D – Direct O - Optimal, F - Flush to RIB
---------------------------------------------------------------- Peer FE80::4283:59FF:FE97:205 on Vlan-interface100 Destination 3::3/128, via FE80::4283:59FF:FE97:205, cost 1, tag 0, AOF, 28 secs表1-7 display ripng route 命令显示信息描述表字段 描述A - Aging 此路由项处于老化状态S - Suppressed 此路由项处于抑制状态此路由项处于Garbage-collect状态G - Garbage-collect D - Direct 此路由项是RIPng生成的直连路由Local route RIPng本地生成的直连路由O - Optimal 此路由项处于最优路由状态F - Flush to RIB 此路由项已经被下刷到RIB Peer 与接口相连的邻居Destination 目的 IPv6 地址下一跳IPv6地址via cost 度量值

字段 描述tag 路由标签secs 此路由项处于某种状态的时间\# 显示进程号为 1 的 RIPng 进程路由信息的统计计数。
<Sysname> display ripng 1 route statistics Peer Optimal/Aging Garbage FE80::20C:29FF:FED4:7171 1/2 0 Local 2/0 0 total 3/2 0表1-8 display ripng route statistics 命令显示信息描述表字段 描述RIPng邻居IPv6地址Peer Optimal 路由信息中处于最优路由状态的路由条数Aging 路由信息中处于老化状态的路由条数Garbage 路由信息中处于Garbage-collection状态的路由条数RIPng本地生成的直连路由条数的总和Local total 从所有RIPng邻居学习到的路由条数的总和

##### 1.1.10 enable ipsec-profile

命令用来在 进程应用 安全框架。
enable ipsec-profile RIPng IPsec命令用来取消在 进程应用的 安全框架。
undo enable ipsec-profile RIPng IPsec【命令】
enable ipsec-profile profile-name undo enable ipsec-profile【缺省情况】
RIPng 没有应用 IPsec 安全框架。
【视图】
RIPng 视图【缺省用户角色】
network-admin【参数】
profile-name：安全框架名称，为 1～63 个字符的字符串，不区分大小写。
【使用指导】
本命令应结合 IPsec安全框架使用，IPsec安全框架的具体情况请参见“安全配置指导”中的“IPsec”。

【举例】
\# 配置 RIPng 进程 1 的 IPsec 安全框架为 profile001。
<Sysname> system-view [Sysname] ripng 1 [Sysname-ripng-1] enable ipsec-profile profile001

##### 1.1.11 fast-reroute

fast-reroute 命令用来配置 RIPng 快速重路由功能。
undo fast-reroute 命令用来关闭 RIPng 快速重路由功能。
【命令】
fast-reroute route-policy route-policy-name undo fast-reroute【缺省情况】
RIPng 快速重路由功能处于关闭状态。
【视图】
视图RIPng【缺省用户角色】
network-admin【参数】
route-policy route-policy-name ： 为 通 过 策 略 的 路 由 指 定 备 份 下 一 跳 。
为路由策略名，为 1～63 个字符的字符串，区分大小写。
route-policy-name【使用指导】
快速重路由功能只适合在主链路三层接口 up，主链路由双通变为单通或者不通的情况下使用。
RIPng在主链路三层接口 down 的情况下，本功能不可用。单通现象，即一条链路上的两端，有且只有一端可以收到另一端发来的报文，此链路称为单向链路。
RIPng 快速重路由功能仅对非迭代 RIPng 路由（即从直连邻居学到 RIPng 路由）有效。
等价路由不支持快速重路由功能。
【举例】
\# 配置对通过策略 frr 的路由指定备份下一跳信息。
<Sysname> system-view [Sysname] ipv6 prefix-list abc index 10 permit 100:: 64 [Sysname] route-policy frr permit node 10 [Sysname-route-policy-frr-10] if-match ipv6 address prefix-list abc [Sysname-route-policy-frr-10] apply ipv6 fast-reroute backup-interface vlan-interface 1 backup-nexthop FE80::8 [Sysname-route-policy-frr-10] quit [Sysname] ripng 100 [Sysname-ripng-100] fast-reroute route-policy frr

##### 1.1.12 filter-policy export

filter-policy export 命令用来配置 RIPng 对发布的路由信息进行过滤。
undo filter-policy export 命令用来取消 RIPng 对发布的路由信息进行过滤。
【命令】
filter-policy { ipv6-acl-number | prefix-list prefix-list-name } export [ protocol [ process-id ] ] undo filter-policy export [ protocol [ process-id ] ]【缺省情况】
不对发布的路由信息进行过滤。
RIPng【视图】
RIPng 视图【缺省用户角色】
network-admin【参数】
ipv6-acl-number：指定的基本或高级 IPv6 ACL 编号，用于对发布的路由信息进行过滤，取值范围为 2000～3999。
prefix-list-name：指定用于过滤发布路由信息的 地址前缀列表名称。
prefix-list IPv6 prefix-list-name 为 1～63 个字符的字符串。
protocol：被过滤路由信息的路由协议。
process-id：被过滤路由信息的路由协议的进程号，取值范围为 1～65535。仅当路由协议为 ripng、ospfv3、isisv6 时需要指定进程号，若未指定，缺省进程号为 1。
【使用指导】
如果指定 参数，则只对从指定路由协议引入的路由信息进行过滤；否则将对所有要发布protocol的路由信息进行过滤。
当配置的是高级 ACL（3000～3999）时，其使用规则如下：
使用命令 来
• rule [ rule-id ] { deny | permit } ipv6 source sour sour-prefix过滤指定目的地址的路由。
使用命令
• rule [ rule-id ] { deny | permit } ipv6 source sour sour-prefix destination dest dest-prefix 来过滤指定目的地址和前缀的路由。
其中，source 用来过滤路由目的地址，destination 用来过滤路由前缀，配置的前缀应该是连续的（当配置的前缀不连续时该过滤前缀的条件不生效）。
【举例】
用地址前缀列表过滤发布的 更新报文。
\# RIPng <Sysname> system-view [Sysname] ipv6 prefix-list abc index 10 permit 100:1:: 32 [Sysname] ripng 100 [Sysname-ripng-100] filter-policy prefix-list abc export \# 用编号为 3000 的 IPv6 高级 ACL 对发布的路由进行过滤，只允许 2001::1/128 通过。

<Sysname> system-view [Sysname] acl ipv6 advanced 3000 [Sysname-acl-ipv6-adv-3000] rule 10 permit ipv6 source 2001::1 128 destination ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff 128 [Sysname-acl-ipv6-adv-3000] rule 100 deny ipv6 [Sysname-acl-ipv6-adv-3000] quit [Sysname] ripng 100 [Sysname-ripng-100] filter-policy 3000 export

##### 1.1.13 filter-policy import

filter-policy import 命令用来配置 RIPng 对接收的路由信息进行过滤。
undo filter-policy import 命令用来恢复缺省情况。
【命令】
filter-policy { ipv6-acl-number | prefix-list prefix-list-name } import undo filter-policy import【缺省情况】
RIPng 不对接收的路由信息进行过滤。
【视图】
视图RIPng【缺省用户角色】
network-admin【参数】
ipv6-acl-number：用于过滤接收的路由信息的 IPv6 ACL 编号，取值范围为 2000～3999。
prefix-list prefix-list-name：指定用于过滤接收路由信息的 IPv6 地址前缀列表名称。
为 1～63 个字符的字符串。
prefix-list-name【使用指导】
当配置的是高级 ACL（3000～3999）时，其使用规则如下：
使用命令 来
• rule [ rule-id ] { deny | permit } ipv6 source sour sour-prefix过滤指定目的地址的路由。
• 使用命令 rule [ rule-id ] { deny | permit } ipv6 source sour sour-prefix destination dest dest-prefix 来过滤指定目的地址和前缀的路由。
其中，source 用来过滤路由目的地址，destination 用来过滤路由前缀，配置的前缀应该是连续的（当配置的前缀不连续时该过滤前缀的条件不生效）。
【举例】
用地址前缀列表过滤收到的 更新报文。
\# RIPng <Sysname> system-view [Sysname] ipv6 prefix-list abc index 10 permit 100:1:: 32 [Sysname] ripng 100 [Sysname-ripng-100] filter-policy prefix-list abc import \# 使用编号为 3000 的 IPv6 高级 ACL 对接收的路由进行过滤，只允许 2001::1/128 通过。

<Sysname> system-view [Sysname] acl ipv6 advanced 3000 [Sysname-acl-ipv6-adv-3000] rule 10 permit ipv6 source 2001::1 128 destination ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff 128 [Sysname-acl-ipv6-adv-3000] rule 100 deny ipv6 [Sysname-acl-ipv6-adv-3000] quit [Sysname] ripng 100 [Sysname-ripng-100] filter-policy 3000 import

##### 1.1.14 graceful-restart

graceful-restart 命令用来使能 RIPng 协议的 GR 能力。
undo graceful-restart 命令用来关闭 RIPng 协议的 GR 能力。
【命令】
graceful-restart undo graceful-restart【缺省情况】
RIPng 协议的 GR 能力处于关闭状态。
【视图】
视图RIPng【缺省用户角色】
network-admin【使用指导】
RIPng GR 特性与 RIPng NSR 特性互斥，即 graceful-restart 和 non-stop-routing 命令互斥，不能同时配置。
【举例】
使能 进程 的 能力。
\# RIPng 1 GR <Sysname> system-view [Sysname] ripng 1 [Sysname-ripng-1] graceful-restart

##### 1.1.15 graceful-restart interval

命令用来配置 协议的 重启间隔时间。
graceful-restart interval RIPng GR命令用来恢复缺省情况。
undo graceful-restart interval【命令】
graceful-restart interval interval undo graceful-restart interval【缺省情况】
RIPng 协议的 GR 重启间隔时间为 60 秒。

【视图】
RIPng 视图【缺省用户角色】
network-admin【参数】
interval：指定 协议的 重启间隔时间（期望重启时间），取值范围为 5～360，单位为RIPng GR秒。
【举例】
\# 配置 RIPng 进程 1 平滑重启间隔时间为 200 秒。
<Sysname> system-view [Sysname] ripng 1 [Sysname-ripng-1] graceful-restart interval 200

##### 1.1.16 import-route

import-route 命令用来从其它路由协议引入路由。
undo import-route 命令用来取消引入的外部路由信息。
【命令】
import-route bgp4+ [ as-number ] [ allow-ibgp ] [ cost cost-value | route-policy route-policy-name ] * undo import-route bgp4+ import-route { direct | static } [ cost cost-value | route-policy route-policy-name ] * undo import-route { direct | static } import-route { isisv6 | ospfv3 | ripng } [ process-id ] [ allow-direct | cost cost-value | route-policy route-policy-name ] * undo import-route { isisv6 | ospfv3 | ripng } [ process-id ]【缺省情况】
RIPng 不引入其它路由。
【视图】
RIPng 视图【缺省用户角色】
network-admin【参数】
bgp4+：引入 BGP4+协议的路由。
direct：引入直连路由。
isisv6：引入 协议的路由。
IPv6 IS-IS ospfv3：引入 OSPFv3 协议的路由。

ripng：引入其他 RIPng 进程的路由。
static：引入静态路由。
as-number：引入指定 AS 内的路由。as-number 为 AS 号，取值范围为 1～4294967295。如果没有指定本参数，则引入所有的 路由。建议配置时指定 号，否则引入的IPv6 EBGP AS IPv6 EBGP路由数量过多时，会引发设备内存资源紧张等问题。
process-id：IS-ISv6、OSPFv3 或 RIPng 路由协议的进程号，取值范围为 1～65535，缺省值为1。
allow-ibgp ： 允 许 引 入 IBGP 路 由 。 import-route bgp4+ 表 示 只 引 入 EBGP 路 由 ，表示也将 IBGP 路由引入，容易引起路由环路，请慎用。
import-route bgp4+ allow-ibgp allow-direct：在引入的路由中包含使能了该协议的接口网段路由。如果未指定本参数，在引入协议路由时不会包含使能了该协议的接口网段路由。当 与allow-direct route-policy route-policy-name 参数一起使用时，需要注意路由策略中配置的匹配规则不要与接口路由信息存在冲突，否则会导致 allow-direct 配置失效。例如，当配置 allow-direct 参数引入OSPFv3直连时，在路由策略中不要配置if-match 匹配条件，否则，allow-direct route-type参数失效。
cost-value：所要引入路由的度量值，取值范围为 0～16。如果没有指定度量值，则使用cost缺省度量值 0。
route-policy route-policy-name：路由策略名称，route-policy-name 为 1～63 个字符的字符串，区分大小写。
【使用指导】
只 能 引 入 路 由 表 中 状 态 为 active 的 路 由 ， 是 否 为 active 状 态 可 以 通 过display ipv6命令来查看。
routing-table protocol【举例】
\# 引入 IPv6 IS-IS 协议（进程号 7）的路由信息，并将其度量值设置为 7。
<Sysname> system-view [Sysname] ripng 100 [Sysname-ripng-100] import-route isisv6 7 cost 7

##### 1.1.17 maximum load-balancing

maximum load-balancing 命令用来配置 RIPng 最大等价路由条数。
undo maximum load-balancing 命令用来恢复缺省情况。
【命令】
maximum load-balancing number undo maximum load-balancing【缺省情况】
RIPng 支持的等价路由的最大条数与系统支持最大等价路由的条数相同。
【视图】
RIPng 视图

【缺省用户角色】
network-admin【参数】
number：等价路由的最大条数，当 取值为 1 时，相当于不进行负载分担。取值范围为 1～number m。m 为系统支持的最大等价路由条数。m 的取值为 和 命令取值中的最小值，64 max-ecmp-num通过 max-ecmp-num 命令对 m 进行修改，那么修改的 m 取值在设备重启后生效。
【使用指导】
通过配置 max-ecmp-num 命令，对系统支持最大等价路由的条数进行修改，导致当前 RIPng 支持的等价路由的最大条数大于 命令的取值，那么设备重启后，RIPng 支持的等价路max-ecmp-num由的最大条数自动修改为 的取值。
max-ecmp-num【举例】
\# 配置 RIPng 最大等价路由条数为 2。
<Sysname> system-view [Sysname] ripng 100 [Sysname-ripng-100] maximum load-balancing 2【相关命令】
• max-ecmp-num（三层技术-IP 路由命令参考/IP 路由基础）

##### 1.1.18 non-stop-routing

non-stop-routing 命令用来使能 RIPng 协议的 NSR 功能。
undo non-stop-routing 命令用来关闭 RIPng 协议的 NSR 功能。
【命令】
non-stop-routing undo non-stop-routing【缺省情况】
RIPng 协议的 NSR 功能处于关闭状态。
【视图】
视图RIPng【缺省用户角色】
network-admin【使用指导】
各个进程的 NSR 功能是相互独立的，只对本进程生效。如果存在多个 RIPng 进程，建议在各个进程下使能 RIPng NSR 功能。
RIPng NSR 特性与 RIPng GR 特性互斥，即 和 命令non-stop-routing graceful-restart互斥，不能同时配置。
【举例】
\# 配置 RIPng 进程 1 使能 NSR 功能。

<Sysname> system-view [Sysname] ripng 1 [Sysname-ripng-1] non-stop-routing

##### 1.1.19 output-delay

用来配置 RIPng 报文的发送速率。
output-delay命令用来恢复缺省情况。
undo output-delay【命令】
output-delay time count count undo output-delay【缺省情况】
发送 RIPng 报文的时间间隔为 20 毫秒，一次最多发送 3 个 RIPng 报文。
【视图】
RIPng 视图【缺省用户角色】
network-admin【参数】
time：发送 RIPng 报文的时间间隔，取值范围为 10～100，单位为毫秒。
count：一次发送 RIPng 报文的最大个数，取值范围为 1～30。
【使用指导】
如果全局和接口都进行了配置，以接口的配置为准。
【举例】
\# 配置 RIPng 进程 1 发送 RIPng 报文的时间间隔为 60 毫秒，一次最多发送 10 个 RIPng 报文。
<Sysname> system-view [Sysname] ripng 1 [Sysname-ripng-1] output-delay 60 count 10【相关命令】
• ripng output-delay

##### 1.1.20 preference

preference 命令用来配置 RIPng 路由的优先级。
undo preference 命令用来恢复缺省情况。
【命令】
preference { preference | route-policy route-policy-name } * undo preference【缺省情况】
RIPng 路由优先级的值为 100。

【视图】
RIPng 视图【缺省用户角色】
network-admin【参数】
preference：RIPng 路由优先级的值，取值范围为 1～255。取值越小，优先级越高。
route-policy-name：路由策略名称，route-policy-name 为 1～63 个字符route-policy的字符串，区分大小写。对满足特定条件的路由设置优先级。
【使用指导】
通过指定 route-policy 参数，可应用路由策略对特定的路由设置优先级：
• 如果在路由策略中已经设置了匹配路由的优先级，则匹配路由取路由策略设置的优先级，其它路由取 命令所设优先级。
preference
• 如果在路由策略中没有设置匹配路由的优先级，则所有路由都取 preference 命令所设优先级。
【举例】
配置 路由的优先级为 120。
\# RIPng <Sysname> system-view [Sysname] ripng 100 [Sysname-ripng-100] preference 120

##### 1.1.21 reset ripng process

命令用来重启指定 进程。
reset ripng process RIPng【命令】
reset ripng process-id process【视图】
用户视图【缺省用户角色】
network-admin【参数】
process-id：RIPng 进程号，取值范围为 1～65535。
【使用指导】
执行该命令后，系统提示用户确认是否重启 RIPng 协议。
【举例】
\# 重启进程号为 100 的 RIPng 进程。
<Sysname> reset ripng 100 process Reset RIPng process? [Y/N]:y

##### 1.1.22 reset ripng statistics

reset ripng statistics 命令用来清除 RIPng 进程的统计信息。
【命令】
reset ripng process-id statistics【视图】
用户视图【缺省用户角色】
network-admin network-operator【参数】
process-id：RIPng 进程号，取值范围为 1～65535。
【举例】
\# 清除进程号为 100 的 RIPng 进程的统计信息。
<Sysname> reset ripng 100 statistics

##### 1.1.23 ripng

命令用来启动 RIPng，并进入 视图。
ripng RIPng命令用来关闭 RIPng。
undo ripng【命令】
ripng [ process-id ] [ vpn-instance vpn-instance-name ] undo ripng [ process-id ]【缺省情况】
系统没有运行 RIPng。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
process-id：RIPng 进程号，取值范围为 1～65535，缺省值为 1。
vpn-instance-name：指定 所属的 实例。vpn-instance-name vpn-instance RIPng VPN表示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则表示 RIPng 位于公网中。
【使用指导】
必须先创建 进程，才能配置 的各种全局性参数，而配置与接口相关的参数时，可以RIPng RIPng不受这个限制。
停止运行 RIPng 进程后，原来配置的接口参数也同时失效。

【举例】
\# 创建 RIPng 进程 100 并进入其视图。
<Sysname> system-view [Sysname] ripng 100 [Sysname-ripng-100]

##### 1.1.24 ripng default-route

ripng default-route 命令用来以指定度量值向 RIPng 邻居发布一条缺省路由。
undo ripng default-route 命令用来禁止发布 RIPng 缺省路由和转发 IPv6 缺省路由。
【命令】
ripng default-route { only | originate } [ cost cost-value | route-policy route-policy-name ] * undo ripng default-route【缺省情况】
进程不发布缺省路由。
RIPng【视图】
接口视图【缺省用户角色】
network-admin【参数】
only：只发布 IPv6 缺省路由（::/0），抑制其它路由的发布。
originate：发布 IPv6 缺省路由（::/0），但不影响其它路由的发布。
cost-value：发布缺省路由的度量值，取值范围为 1～15，缺省值为 1。
route-policy route-policy-name：路由策略名称，route-policy-name 为 1～63 个字符的字符串，区分大小写。只有当前路由器的路由表中有路由匹配 指定的route-policy-name路由策略时，才发送缺省路由。
【使用指导】
通过该命令的设置，生成的 RIPng 缺省路由将强制通过指定接口的路由更新报文发布出去。该 IPv6缺省路由的发布不考虑其是否已经存在于 IPv6 路由表中。
配置发布缺省路由的 RIPng 接口不接收来自 RIPng 邻居的缺省路由。
【举例】
\# 在接口 Vlan-interface100 上配置 RIPng 只将缺省路由以更新报文的形式从接口发布。
<Sysname> system-view [Sysname] interface vlan-interface 100 [Sysname-Vlan-interface100] ripng default-route only \# 在接口Vlan-interface101上配置RIPng将缺省路由同其它路由一起以更新报文的形式从接口发布。
<Sysname> system-view [Sysname] interface vlan-interface 101 [Sysname-Vlan-interface101] ripng default-route originate

##### 1.1.25 ripng enable

ripng enable 命令用来在接口上使能 RIPng 功能。
undo ripng enable 命令用来在接口上关闭 RIPng 功能。
【命令】
ripng process-id enable undo ripng enable【缺省情况】
接口上的 RIPng 功能处于关闭状态。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
process-id：RIPng 进程号，取值范围为 1～65535。
【举例】
\# 在接口 Vlan-interface100 上使能 RIPng 100。
<Sysname> system-view [Sysname] interface vlan-interface 100 [Sysname-Vlan-interface100] ripng 100 enable

##### 1.1.26 ripng ipsec-profile

命令用来在 RIPng 接口上应用安全框架。
ripng ipsec-profile undo ripng ipsec-profile 命令用来取消 RIPng 接口上应用的安全框架。
【命令】
ripng ipsec-profile profile-name undo ripng ipsec-profile【缺省情况】
接口没有应用安全框架。
RIPng【视图】
接口视图【缺省用户角色】
network-admin【参数】
profile-name：安全框架名称，为 1～63 个字符的字符串，不区分大小写。

【使用指导】
本命令应结合 IPsec安全框架使用，IPsec安全框架的具体情况请参见“安全配置指导”中的“IPsec”。
【举例】
\# 配置接口 Vlan-interface100 应用的 IPsec 安全框架为 profile001。
<Sysname> system-view [Sysname] interface vlan-interface 100 [Sysname-Vlan-interface100] ripng ipsec-profile profile001

##### 1.1.27 ripng metricin

ripng metricin 命令用来配置接口接收 RIPng 路由时的附加度量值。
undo ripng metricin 命令用来恢复缺省情况。
【命令】
ripng metricin value undo ripng metricin【缺省情况】
接口接收 路由时的附加度量值为 0。
RIPng【视图】
接口视图【缺省用户角色】
network-admin【参数】
value：接收附加度量值，取值范围为 0～16。
【举例】
\# 指定接口 Vlan-interface100 在接收 RIPng 路由时添加的附加度量值为 12。
<Sysname> system-view [Sysname] interface vlan-interface 100 [Sysname-Vlan-interface100] ripng metricin 12

##### 1.1.28 ripng metricout

命令用来配置接口发送 RIPng 路由时的附加度量值。
ripng metricout命令用来恢复缺省情况。
undo ripng metricout【命令】
ripng metricout value undo ripng metricout【缺省情况】
接口发送 路由时的附加度量值为 1。
RIPng

【视图】
接口视图【缺省用户角色】
network-admin【参数】
value：发送附加度量值，取值范围为 1～16。
【举例】
\# 设置接口 Vlan-interface100 发送 RIPng 路由时添加的附加度量值为 12。
<Sysname> system-view [Sysname] interface vlan-interface 100 [Sysname-Vlan-interface100] ripng metricout 12

##### 1.1.29 ripng output-delay

命令用来配置接口下 报文的发送速率。
ripng output-delay RIPng命令用来恢复缺省情况。
undo ripng output-delay【命令】
ripng output-delay time count count undo ripng output-delay【缺省情况】
RIPng 报文的发包速率由进程全局的配置决定。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
time：接口发送 报文的时间间隔，取值范围为 10～100，单位为毫秒。
RIP count：接口一次发送 报文的最大个数，取值范围为 1～30。
RIPng【使用指导】
如果全局和接口都进行了配置，以接口的配置为准。
【举例】
\# 在接口 Vlan-interface100 配置发送 RIPng 报文的时间间隔为 30 毫秒，一次最多发送 6 个 RIPng报文。
<Sysname> system-view [Sysname] interface vlan-interface 100 [Sysname-Vlan-interface100] ripng output-delay 30 count 6【相关命令】
• output-delay

##### 1.1.30 ripng poison-reverse

ripng poison-reverse 命令用来使能毒性逆转功能。
undo ripng poison-reverse 命令用来关闭毒性逆转功能。
【命令】
ripng poison-reverse undo ripng poison-reverse【缺省情况】
毒性逆转功能处于关闭状态。
【视图】
接口视图【缺省用户角色】
network-admin【举例】
\# 在接口 Vlan-interface100 上配置对 RIPng 更新报文进行毒性逆转。
<Sysname> system-view [Sysname] interface vlan-interface 100 [Sysname-Vlan-interface100] ripng poison-reverse

##### 1.1.31 ripng primary-path-detect bfd echo

ripng primary-path-detect bfd echo 命令用来使能 RIPng 协议中主用链路的 BFD（Echo方式）检测功能。
命令用来关闭 RIPng 协议中主用链路的 BFD（Echo undo ripng primary-path-detect bfd方式）检测功能。
【命令】
ripng primary-path-detect bfd echo undo ripng primary-path-detect bfd【缺省情况】
RIPng 协议中主用链路的 BFD（Echo 方式）检测功能处于关闭状态。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
echo：配置通过工作于 报文方式的 会话对主用链路进行检测。
echo BFD【使用指导】
配置本功能后，RIPng 协议的快速重路由特性中的主用链路将使用 BFD 进行检测。

【举例】
\# 在接口 Vlan-interface10 上配置 RIPng 协议快速重路由特性中主用链路使能 BFD（Echo 方式）
检测功能。
<Sysname> system-view [Sysname] ripng 1 [Sysname-ripng-1] fast-reroute route-policy frr [Sysname-ripng-1] quit [Sysname] bfd echo-source-ipv6 1::1 [Sysname] interface vlan-interface 11 [Sysname-Vlan-interface11] ripng primary-path-detect bfd echo

##### 1.1.32 ripng split-horizon

ripng split-horizon 命令用来使能水平分割功能。
undo ripng split-horizon 命令用来关闭水平分割。
【命令】
ripng split-horizon undo ripng split-horizon【缺省情况】
水平分割功能处于使能状态。
【视图】
接口视图【缺省用户角色】
network-admin【使用指导】
通常情况下，为了防止路由环路的出现，水平分割都是必要的，因此，建议不要关闭水平分割。只是在某些特殊情况下，为保证协议的正确执行，需要关闭水平分割。在关闭水平分割时一定要确认是否必要。
如果同时使能了水平分割和毒性逆转，则只有毒性逆转功能生效。
【举例】
在接口 上配置水平分割。
\# Vlan-interface100 <Sysname> system-view [Sysname] interface vlan-interface 100 [Sysname-Vlan-interface100] ripng split-horizon

##### 1.1.33 ripng summary-address

命令用来配置 在接口发布聚合的 地址，并指定被聚合的ripng summary-address RIPng IPv6路由的 IPv6 前缀。
undo ripng summary-address 命令用来禁止 RIPng 路由器发布聚合的 IPv6 地址。

【命令】
ripng summary-address ipv6-address prefix-length undo ripng summary-address ipv6-address prefix-length【缺省情况】
未配置 RIPng 在接口发布聚合的 IPv6 地址。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
ipv6-address：聚合路由的目的 IPv6 地址。
prefix-length：聚合路由的目的 IPv6 地址前缀长度，取值范围为 0～128。它指定地址中有多少连续的位组成 IPv6 网络前缀，即 IPv6 地址中的网络地址部分。
【使用指导】
如果一条路由的前缀和前缀长度与定义的 IPv6 前缀匹配，则这个自定义的 IPv6 前缀将取代原来的路由被发布出去。这样，多条路由将由一条路由所代替，而且，这条路由的度量值是原多条路由中最低的。
【举例】
\# 在接口 Vlan-interface100 上配置 IPv6 地址 2001:200::3EFF:FE11:6770，其前缀长度为 64 位。
通过 聚合为 地址前缀 2001:200::/35。
RIPng IPv6 <Sysname> system-view [Sysname] interface vlan-interface 100 [Sysname-Vlan-interface100] ipv6 address 2001:200::3EFF:FE11:6770/64 [Sysname-Vlan-interface100] ripng summary-address 2001:200:: 35

##### 1.1.34 timer triggered

timer triggered 命令用来配置触发更新的时间间隔。
undo timer triggered 命令用来恢复缺省情况。
【命令】
timer triggered maximum-interval [ minimum-interval [ incremental-interval ] ] undo timer triggered【缺省情况】
发送触发更新的最大时间间隔为 秒，最小间隔为 毫秒，增量惩罚间隔为 毫秒。
5 50 200【视图】
RIPng 视图

【缺省用户角色】
network-admin【参数】
maximum-interval：触发更新的最大间隔时间。取值范围为 1～5，单位为秒。
minimum-interval：触发更新的最小间隔时间。取值范围为 10～5000，单位为毫秒。
incremental-interval：触发更新间隔的增加时间。取值范围为 100～1000，单位为毫秒。
【使用指导】
本命令在网络变化不频繁的情况下将触发更新的时间间隔缩小到 minimum-interval，而在网络变化频繁的情况下可以进行相应惩罚，将时间间隔按照配置的惩罚增量延长，最大不超过maximum-interval。
minimum-interval 和 incremental-interval 配置值不允许大于 maximum-interval 配置值。
【举例】
\# 配置发送触发更新的最大时间间隔为 2 秒，最小时间间隔为 100 毫秒，惩罚增量为 100 毫秒。
<Sysname> system-view [Sysname] ripng 100 [Sysname-ripng-100] timer triggered 2 100 100

##### 1.1.35 timers

命令用来配置 RIPng 定时器的值。
timers命令用来恢复 RIPng 定时器的缺省值。
undo timers【命令】
timers { garbage-collect garbage-collect-value | suppress suppress-value | timeout timeout-value | update update-value } * undo timers { garbage-collect | suppress | timeout | update } *【缺省情况】
Garbage-collect 定时器的值为 120 秒，Suppress 定时器的值为 120 秒，Timeout 定时器的值为 180秒，Update 定时器的值为 30 秒。
【视图】
视图RIPng【缺省用户角色】
network-admin【参数】
garbage-collect-value：Garbage-collect 定时器的值，取值范围为 1～86400，单位为秒。
suppress-value：Suppress 定时器的值，取值范围为 0～86400，单位为秒。
timeout-value：Timeout 定时器的值，取值范围为 1～86400，单位为秒。
update-value：Update 定时器的值，取值范围为 1～86400，单位为秒。

【使用指导】
RIPng 受四个定时器的控制，分别是 Update、Timeout、Suppress 和 Garbage-Collect，其中：
• Update 定时器，定义了发送更新报文的时间间隔。
• Timeout 定时器，定义了路由老化时间。如果在老化时间内没有收到关于某条路由的更新报文，则该条路由在路由表中的度量值将会被设置为 16。
• Suppress 定时器，定义了 RIPng 路由处于抑制状态的时间段长度。当一条路由的度量值变为时，该路由将进入被抑制状态。在被抑制状态，只有来自同一邻居，且度量值小于 的路16 16由更新才会被路由器接收，取代不可达路由。
定时器，定义了一条路由从度量值变为 开始，直到它从路由表里被删除
• Garbage-Collect 16所经过的时间。在 Garbage-Collect 时间内，RIPng 以 16 作为度量值向外发送这条路由的更新，如果 Garbage-Collect 超时，该路由仍没有得到更新，则该路由将从路由表中被彻底删除。
通常情况下，无需改变各定时器的缺省值，该命令须谨慎使用。
各个定时器的值在网络中所有的路由器上必须保持一致。
【举例】
分别设置 进程 各定时器的值：其中，Update 定时器的值为 秒、Timeout 定时器的值为\# RIPng 1 5 15 秒、Suppress 定时器的值为 15 秒、Garbage-Collect 定时器的值为 30 秒。
<Sysname> system-view [Sysname] ripng 1 [Sysname-ripng-1] timers update 5 timeout 15 suppress 15 garbage-collect 30

## 10-OSPFv3命令

目 录配置命令

### 1 OSPFv3

1 OSPFv3

#### 1.1 OSPFv3配置命令

##### 1.1.1 abr-summary (OSPFv3 area view)

命令用来配置 ABR 路由聚合。
abr-summary命令用来取消 ABR 对指定网段的路由聚合。
undo abr-summary【命令】
abr-summary ipv6-address prefix-length [ not-advertise ] [ cost cost-value ] undo abr-summary ipv6-address prefix-length【缺省情况】
不对路由进行聚合。
ABR【视图】
OSPFv3 区域视图【缺省用户角色】
network-admin【参数】
ipv6-address：聚合路由的目的 IPv6 地址。
prefix-length：聚合路由的目的 IPv6 地址前缀长度，取值范围为 0～128。它指定地址中有多少连续的位组成 网络前缀，即 地址中的网络地址部分。
IPv6 IPv6 not-advertise：不通告聚合的 IPv6 路由。如果未指定本参数，则通告聚合的 IPv6 路由。
cost-value：聚合路由的开销值，取值范围为 1～16777215，缺省值为所有被聚合的路由cost中最大的开销值。
【使用指导】
本命令只适用于 ABR，用来对当前区域进行路由聚合。对于落入该聚合网段的路由，ABR 向其它区域只发送一条聚合后的路由。一个区域可配置多条聚合网段，这样 OSPFv3 可对多个网段进行聚合。
当配置了 命令后，原来被聚合的路由将重新被发布。
undo abr-summary【举例】
将 区域 中两条路由 2000:1:1:1::/64、2000:1:1:2::/64 的路由聚合成一条前缀\# OSPFv3 1 2000:1:1::/48 向其它区域发送。
<Sysname> system-view [Sysname] ospfv3 1 [Sysname-ospfv3-1] area 1 [Sysname-ospfv3-1-area-0.0.0.1] abr-summary 2000:1:1:: 48

##### 1.1.2 area

area 命令用来创建 OSPFv3 区域，并进入区域视图。
undo area 命令用来删除指定的 OSPFv3 区域。
【命令】
area area-id undo area area-id【缺省情况】
不存在 OSPFv3 区域。
【视图】
视图OSPFv3【缺省用户角色】
network-admin【参数】
area-id：区域的标识，可以是十进制整数（取值范围为 0～4294967295，系统会将其处理成 IPv4地址格式）或 IPv4 地址格式。
【举例】
进入 区域 视图。
\# OSPFv3 0 <Sysname> system-view [Sysname] ospfv3 1 [Sysname-ospfv3-1] area 0 [Sysname-ospfv3-1-area-0.0.0.0]

##### 1.1.3 asbr-summary (OSPFv3 view)

asbr-summary 命令用来配置 ASBR 路由聚合。
undo asbr-summary 命令用来取消 ASBR 对指定网段的路由聚合。
【命令】
asbr-summary ipv6-address prefix-length [ cost cost-value | not-advertise | nssa-only | tag tag ] * undo asbr-summary ipv6-address prefix-length【缺省情况】
ASBR 不对引入的路由进行聚合。
【视图】
OSPFv3 视图【缺省用户角色】
network-admin

【参数】
ipv6-address：聚合路由的目的 IPv6 地址。
prefix-length：聚合路由的目的 IPv6 地址前缀长度，取值范围为 0～128。它指定地址中有多少连续的位组成 IPv6 网络前缀，即 IPv6 地址中的网络地址部分。
cost-value：聚合路由的开销，取值范围为 1～16777214。如果未指定本参数，cost-value cost取所有被聚合的路由中最大的开销值作为聚合路由的开销；如果是 转化成的Type-7 LSA Type-5 LSA 描述的路由匹配聚合、且是 Type2 外部路由，则 cost-value 取所有被聚合的路由中最大的开销值加 1 作为聚合路由的开销。
not-advertise：不通告聚合路由。如果未指定本参数，将通告聚合路由。
nssa-only：设置 Type-7 LSA 的 P 比特位为不置位，即在对端路由器上不能转为 Type-5 LSA。
缺省时，Type-7 LSA 的 P 比特位被置位，即在对端路由器上可以转为 Type-5 LSA（如果本地路由器是 ABR，则会检查骨干区域是否存在 状态的邻居，当 状态的邻居存在时，产生的FULL FULL Type-7 LSA 中 P 比特位不置位）。
tag tag：聚合路由的标记，取值范围为 0～4294967295。
【使用指导】
如果本地路由器是 ASBR，对引入的聚合地址范围内的 Type-5 LSA 描述的路由进行聚合；当配置了 NSSA 区域时，对引入的聚合地址范围内的 Type-7 LSA 描述的路由进行聚合。
如果本地路由器同时是 ASBR 和 ABR，并且是 NSSA 区域的转换路由器，则对由 Type-7 LSA 转化成的 描述的路由进行聚合处理；如果不是 区域的转换路由器，则不进行聚合处Type-5 LSA NSSA理。
配置 asbr-summary 命令后，对处于聚合地址范围内的外部路由，本地路由器只向邻居路由器发布一条聚合后的路由；配置 undo asbr-summary 命令后，原来被聚合的外部路由将重新被发布。
【举例】
\# 配置 OSPFv3 进程 1 对引入的路由进行聚合，聚合路由为 2000::/16，开销值为 100，标记为 2。
<Sysname> system-view [Sysname] ospfv3 1 [Sysname-ospfv3-1] asbr-summary 2000:: 16 cost 100 tag 2

##### 1.1.4 authentication-mode

authentication-mode 命令用来设置 OSPFv3 区域使用的验证模式。
undo authentication-mode 命令用来恢复缺省情况。
【命令】
authentication-mode keychain keychain-name undo authentication-mode【缺省情况】
未配置区域验证模式。
【视图】
OSPFv3 区域视图

【缺省用户角色】
network-admin【参数】
keychain：使用 keychain 验证模式。
keychain-name：keychain 名称，为 1～63 个字符的字符串，区分大小写。
【使用指导】
接口视图下配置的验证模式，其优先级高于 OSPFv3 区域视图下配置的验证模式。
在 OSPFv3 区域使用 keychain 验证模式时，本区域的 OSPFv3 报文验证过程如下：
OSPFv3 在发送报文前，会先从 keychain 获取当前的有效发送 key，根据该 key 的标识符、
•认证算法和认证密钥进行报文验证。如果当前不存在有效发送 key，OSPFv3 不会发送报文。
在收到报文后，会根据报文携带的 的标识符从 中获取有效接收 key，
• OSPFv3 key keychain根据该 key 的认证算法和认证密钥对报文进行校验。如果报文校验失败，或者根据报文中携带的 key 的标识符无法从 keychain 中获取到有效接收 key，则该报文将被丢弃。
对于 keychain 认证算法和 key 的标识符的范围，OSPFv3 的支持情况如下：
• OSPFv3 仅支持 HMAC-SHA-256 和 HMAC-SM3 认证算法。
• OSPFv3 仅支持标识符取值范围为 0～65535 的 key。
【举例】
\# 配置 OSPFv3 区域 1 使用 keychain 验证模式，keychain 名为 test。
<Sysname> system-view [Sysname] ospfv3 1 [Sysname-ospfv3-1] area 1 [Sysname-ospfv3-1-area-0.0.0.1] authentication-mode keychain test

##### 1.1.5 bandwidth-reference (OSPFv3 view)

bandwidth-reference 命令用来配置计算链路开销时所依据的带宽参考值。
undo bandwidth-reference 命令用来恢复缺省情况。
【命令】
bandwidth-reference value undo bandwidth-reference【缺省情况】
计算链路开销时所依据的带宽参考值为 100Mbps。
【视图】
OSPFv3 视图【缺省用户角色】
network-admin【参数】
value：计算链路开销时所依据的带宽参考值，取值范围为 1～4294967，单位为 Mbps。

【使用指导】
OSPFv3 有两种方式来配置接口的开销值，第一种方法是在接口视图下直接配置开销值；第二种方法是配置接口的带宽参考值，OSPFv3 根据带宽参考值自动计算接口的开销值，计算公式为：接口开销＝带宽参考值÷接口带宽，当计算出来的开销值大于 65535，开销取最大值 65535；当计算出来的开销值小于 1 时，开销取最小值 1。
如果没有在接口视图下显式的配置此接口的开销值，OSPFv3 会根据该接口的带宽自动计算其开销值。
【举例】
\# 配置计算链路开销时所依据的带宽参考值为 1000Mbps。
<Sysname> system-view [Sysname] ospfv3 1 [Sysname-ospfv3-1] bandwidth-reference 1000

##### 1.1.6 default tag

命令用来配置引入外部路由的全局标记。
default tag命令用来恢复缺省情况。
undo default tag【命令】
default tag tag undo default tag【缺省情况】
引入外部路由的全局标记为 1。
【视图】
OSPFv3 视图【缺省用户角色】
network-admin【参数】
tag：外部路由的全局标记，取值范围为 0～4294967295。
【使用指导】
如果在配置 和 命令时没有指定标记，则缺省使用default-route-advertise import-route本命令配置的全局标记。
【举例】
\# 配置 OSPFv3 引入外部路由的标记为 2。
<Sysname> system-view [Sysname] ospfv3 1 [Sysname-ospfv3-1] default tag 2【相关命令】
• (OSPFv3 view)
default-route-advertise
• import-route

##### 1.1.7 default-cost (OSPFv3 area view)

default-cost 命令用来配置发送到 Stub 区域或 NSSA 区域的缺省路由的开销。
undo default-cost 命令用来恢复缺省情况。
【命令】
default-cost cost undo default-cost【缺省情况】
发送到 Stub 区域或 NSSA 区域的缺省路由的开销为 1。
【视图】
区域视图OSPFv3【缺省用户角色】
network-admin【参数】
cost：发送到 Stub 区域或 NSSA 区域的缺省路由的开销，取值范围为 0～16777214。
【使用指导】
该命令只有在 Stub 区域的 ABR 或 NSSA 区域的 ABR/ASBR 上配置才能生效。
【举例】
将 区域 设置为 区域，使发送到该 区域的缺省路由开销为 60。
\# OSPFv3 1 Stub Stub <Sysname> system-view [Sysname] ospfv3 1 [Sysname-ospfv3-1] area 1 [Sysname-ospfv3-1-area-0.0.0.1] stub [Sysname-ospfv3-1-area-0.0.0.1] default-cost 60【相关命令】
• nssa (OSPFv3 area view)
• stub (OSPFv3 area view)

##### 1.1.8 default-route-advertise (OSPFv3 view)

default-route-advertise 命令用来将缺省路由引入到 OSPFv3 路由区域。
undo default-route-advertise 命令用来恢复缺省情况。
【命令】
default-route-advertise [ [ always | permit-calculate-other ] | cost cost-value | route-policy route-policy-name | tag tag | type type ] * undo default-route-advertise【缺省情况】
未引入缺省路由。

【视图】
OSPFv3 视图【缺省用户角色】
network-admin【参数】
always：如果当前路由器的路由表中没有缺省路由，使用此参数可产生一个描述缺省路由的AS-external-LSA 发布出去。如果没有指定该关键字，仅当本地路由器的路由表中存在缺省路由时，才可以产生一个描述缺省路由的 AS-external-LSA 发布出去。
permit-calculate-other：当路由器产生并发布了一个描述缺省路由的 AS-external-LSA 时，指定此参数的路由器仍然会计算来自于其他路由器的缺省路由，未指定此参数的路由器不再计算来自其他路由器的缺省路由。当路由器没有产生一个描述缺省路由的 时，无论是否AS-external-LSA指定此参数，路由器都会计算来自其他路由器的缺省路由。
cost cost-value：该缺省路由的度量值，取值范围为 0～16777214，缺省值为 1。
route-policy route-policy-name：路由策略名，为 1～63 个字符的字符串，区分大小写。
只有当前路由器的路由表中存在缺省路由，并且有路由匹配 route-policy-name 指定的路由策略，才可以产生一个描述缺省路由的 AS-external-LSA 发布出去，指定的路由策略会影响中的值。如果同时指定 参数，不论当前路由器的路由表中是否有缺省路AS-external-LSA always由，只要有路由匹配指定的路由策略，就将产生一个描述缺省路由的 AS-external-LSA 发布出去，指定的路由策略会影响 AS-external-LSA 中的值。
tag tag：外部路由的标记，取值范围为 0～4294967295。如果未指定本参数，将根据 default tag命令的配置进行取值。
type：该 AS-external-LSA 的类型，取值范围为 1～2，缺省值为 2。
type【使用指导】
使用 命令不能引入缺省路由，如果要引入缺省路由，必须使用本命令。当本地路import-route由器的路由表中没有缺省路由时，要产生一个描述缺省路由的 AS-external-LSA 应使用 always 关键字。
【举例】
\# 将产生的缺省路由引入到 OSPFv3 自治系统中（本地路由器没有缺省路由）。
<Sysname> system-view [Sysname] ospfv3 1 [Sysname-ospfv3-1] default-route-advertise always【相关命令】
• import-route (OSPFv3 area view)

##### 1.1.9 display ospfv3

命令用来显示 的进程信息。
display ospfv3 OSPFv3【命令】
display ospfv3 [ process-id ] [ verbose ]

【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPFv3 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 OSPFv3进程的概要信息。
verbose：显示 进程的详细信息。如果未指定本参数，将显示 进程的概要信息。
OSPFv3 OSPFv3【举例】
\# 显示所有 OSPFv3 进程的详细信息。
<Sysname> display ospfv3 verbose OSPFv3 Process 1 with Router ID 1.1.1.1 RouterID: 1.1.1.1 Router type: ABR ASBR NSSA Route tag: 0 Route tag check: Disabled Multi-VPN-Instance: Disabled Type value of extended community attributes:
Domain ID : 0x0005 Route type: 0x0306 Router ID : 0x0107 Domain-id: 0.0.0.0 DN-bit check: Enabled DN-bit set: Enabled Originating router-LSAs with maximum metric Condition: On startup for 600 seconds, State: Inactive Advertise summary-LSAs with metric 16711680 Advertise external-LSAs with metric 16711680 Advertise intra-area-prefix-LSAs with maximum metric SPF-schedule-interval: 5 50 200 LSA generation interval: 5 LSA arrival interval: 1000 Transmit pacing: Interval: 20 Count: 3 Default ASE parameters: Tag: 1 Route preference: 10 ASE route preference: 150 FRR backup mode: LFA SPF calculation count: 0 External LSA count: 0 LSA originated count: 0 LSA received count: 0 SNMP trap rate limit interval: 10 Count: 7 Area count: 2 Stub area count: 0 NSSA area count: 1

ExChange/Loading neighbors: 0 Max equal cost paths: 32 Up interfaces: 1 Full neighbors: 1 Normal areas with up interfaces: 1 Calculation trigger type: Full Current calculation type: SPF calculation Current calculation phase: Calculation area topology Redistribute timer: Off Redistribute schedule type: RIB Redistribute route count: 0 Process reset state: N/A Current reset type: N/A Next reset type: N/A Reset prepare message replied: -/-/-/- Reset process message replied: -/-/-/- Reset phase of module:
M-N/A, P-N/A, S-N/A, C-N/A, R-N/A Area: 0.0.0.0 Area flag: Normal SPF scheduled count: 0 ExChange/Loading neighbors: 0 LSA count: 0 Up interfaces: 0 MTU: 1440 Default cost: 1 Created by Vlink Process reset state: N/A Current reset type: N/A Reset prepare message replied: -/-/-/- Reset process message replied: -/-/-/- Reset phase of module:
M-N/A, P-N/A, S-N/A, C-N/A, R-N/A Area: 0.0.0.2 Area flag: Normal SPF scheduled count: 0 ExChange/Loading neighbors: 0 LSA count: 0 IPsec profile name: Profile000 Keychain authentication: Enabled (test)
Up interfaces: 1 MTU: 1500 Default cost: 1 Process reset state: N/A Current reset type: N/A Reset prepare message replied: -/-/-/-

Reset process message replied: -/-/-/- Reset phase of module:
M-N/A, P-N/A, S-N/A, C-N/A, R-N/A Area: 0.0.0.3 Area flag: NSSA 7/5 translator state: Disabled 7/5 translate stability timer interval: 0 SPF Scheduled Count: 0 ExChange/Loading neighbors: 0 LSA Count: 0 Up interfaces: 0 MTU: 1440 Default cost: 1 Process reset flag: N/A Current reset type: N/A Reset prepare message replied: -/-/-/- Reset process message replied: -/-/-/- Reset phase of module:
M-N/A, P-N/A, S-N/A, C-N/A, R-N/A表1-1 display ospfv3 verbose 命令显示信息描述表字段 描述OSPFv3 Process 1 with Router ID 1.1.1.1 OSPFv3进程是1，Router ID是1.1.1.1本路由器的Router RouterID ID路由器类型，取值为：
• ABR 表示区域边界路由器Router type • ASBR 表示自治系统边界路由器
• NSSA 表示支持 NSSA 区域为空表示非上面三种情况Route tag 当前进程引入外部路由的缺省标记当前进程是否使能检查OSPFv3 LSA的标记Route tag check当前进程对PE、多VPN实例的支持情况：
• Multi-VPN-Instance：Disabled 表示不支持多 VPN 实例Multi-VPN-Instance
• Multi-VPN-instance：Enabled 表示支持多 VPN 实例
• PE Router, Multi-VPN-Instance：Enabled 表示为 PE Type value of extended community OSPFv3扩展团体属性的类型编码attributes Domain-id OSPFv3域标识符DN-bit check 当前进程是否使能检查 OSPFv3 LSA 的 DN 位DN-bit set 当前进程是否使能设置OSPFv3 LSA的DN位

字段 描述Originating router-LSAs with maximum metric/Originating router-LSAs with R-bit Router LSA中使用最大开销值发布/Router LSA中清除R-bit clear Stub路由器的状态：
• Always 代表始终生效Condition • On startup while BGP is converging for XXX seconds 代表BGP 收敛超时时间
• On startup for XXX seconds 代表重启后生效时间Stub路由器是否生效：
State • Active 表示生效
•Inactive 表示不生效Advertise summary-LSAs with metric Summary LSA发布使用的开销值Advertise external-LSAs with metric 外部LSA发布使用的开销值Advertise intra-area-prefix-LSAs with Intra-area-prefix-LSA发布使用的开销值maximum metric进行SPF计算的时间间隔SPF-schedule-interval LSA generation interval LSA生成时间间隔LSA arrival interval LSA重复到达的最小时间间隔接口发送LSU报文的速率，其中：
Transmit pacing • Interval 表示接口发送 LSU 报文的时间间隔
• Count 表示接口一次发送 LSU 报文的最大个数引入外部路由的缺省参数值，其中Tag代表路由标记Default ASE parameters Route preference 内部路由优先级ASE route preference 外部路由优先级指定快速重路由的备份下一跳地址的方式：
• LFA： 为所有路由通过 LFA（Loop Free Alternate）算法选取备份下一跳信息。如果显示为 LFA ABR-only，则表示只有到FRR backup mode ABR 设备的路由才能够通过 LFA 算法被选取为备份路径。
• route-policy-name：为通过策略的路由指定备份route-policy下一跳，route-policy-name 为路由策略名SPF calculation count OSPFv3进程的路由计算总数外部LSA数目，其中：
• Count：LSA 数目External LSA count
• checksum Sum：校验和LSA originated count 产生的LSA数目接收的LSA数目LSA received count SNMP trap rate limit interval: 10 Count: 7 OSPFv3在10内秒允许输出7条告警信息Area count 区域总数目

字段 描述Stub area count Stub区域数目NSSA area count NSSA区域数目处于ExChange/Loading状态的邻居数ExChange/Loading neighbors触发路由计算的类型，具体如下：
• Full：触发全部路由计算
• Area topology change：区域拓扑改变触发路由计算
• Intra router change：增量的区域内路由器路由变化
• change：增量的 路由变化ASBR ASBR
• Full IP prefix：触发全部 IP 前缀计算Calculation trigger type
• AS：触发全部 内部前缀计算Full intra AS
• Inc intra AS：触发增量 AS 内部前缀计算
• Full inter AS：触发全部 AS 外部前缀计算
• Inc inter AS：触发增量 AS 外部前缀计算
• Nexthop calculation：触发下一跳计算
• N/A：未触发计算当前路由计算的类型，具体如下：
• calculation：进行区域 计算SPF SPF
• Intra router calculation：区域内路由器路由计算
• ASBR calculation：区域间 ASBR 路由计算
• Inc intra router：增量区域内路由器路由计算Current calculation type • Inc ASBR calculation：增量区域间 ASBR 路由计算
• Full intra AS：进行全部 AS 内部前缀计算
• Inc intra AS：进行增量 AS 内部前缀计算
• AS：进行全部 外部前缀计算Full inter AS
• Inc inter AS：进行增量 AS 外部前缀计算
• N/A：未触发计算当前路由计算调度运行到的阶段，具体如下：
• Calculation area topology：计算区域拓扑
• Calculation router：计算路由器路由
• Calculation intra AS：计算 AS 内部路由Current calculation phase
• ASBR：计算 路由Calculation ASBR
• Calculation inter AS：计算 AS 外部路由
• end：计算收尾阶段Calculation
• N/A：未触发计算引入路由定时器，其中：
• Off： 关闭Redistribute timer
• On：开启

字段 描述引入路由调度类型，其中：
•RIB： 触发遍历 RIB 表进行引入Redistribute schedule type
• Self： 触发遍历自身引入表进行引入N/A：未触发引入Redistribute route count 引入路由计数进程重启状态标志，具体如下：
• N/A：进程未重启Process reset state
• Under reset：进程正在重启
• smooth：进程正在同步 路由Under RIB RIB当前进程重启类型，具体如下：
• N/A：进程未重启
• GR quit：GR 异常退出进行普通重启Current reset type
• Delete：删除 OSPFv3 进程
• router-id：删除Undo Router-id
• Set router-id：设置 Router-id即将调度进程重启类型，具体如下：
• N/A：进程未重启
• GR quit：GR 异常退出进行普通重启Next reset type
• Delete：删除 OSPFv3 进程
• Undo router-id：删除 Router-id
• router-id：设置Set Router-id响应准备重启消息的模块，具体如下：
• P 代表邻居维护模块Reset prepare message replied • S 代表 LSDB 同步模块
• C 代表路由计算模块
• R 代表路由引入模块响应进程重启消息的模块，具体如下：
• P 代表邻居维护模块Reset process message replied • S 代表 LSDB 同步模块
• C 代表路由计算模块
• R 代表路由引入模块

字段 描述各模块所处重启阶段。其中M代表主控制模块，P代表邻居维护模块，S代表LSDB同步模块，其阶段有：
• N/A：未重启
• Delete ASE：删除所有 ASE LSA
•Delete area LSA：删除区域相关 LSA
• Delete area IF：删除区域下接口
• C 代表路由计算模块，其阶段有：
• N/A：未重启Reset phase of module
• Delete topology：删除区域拓扑
• Delete router：删除路由器路由
• Delete intra AS：删除 AS 内部路由
• AS：删除 外部路由Delete inter AS
• Delete ASBR：删除 ASBR 路由
• 代表路由引入模块，其阶段有：
R
• N/A：未重启
• Delete import：删除引入路由区域信息Area Area flag 区域类型SPF scheduled count OSPF区域的路由计算总数LSA数目，其中：
LSA count • Count：LSA 数目
• checksum Sum：校验和IPsec安全框架名IPsec profile name Keychain authentication: Enabled (test) OSPFv3区域采用keychain验证模式，keychain名称为test MTU 区域的MTU值路由的缺省开销值Default cost Created by Vlink 区域由 Vlink 创建Type-7 LSA转换为Type-5 LSA的转换者状态，取值为：
• Enabled：表示本设备是通过命令指定的 转换为Type-7 LSA的转换者Type-5 LSA 7/5 translator state
• Elected：表示本设备是通过选举指定的 Type-7 LSA 转换为Type-5 LSA 的转换者
• Disabled：表示本设备不是 转换为Type-7 LSA Type-5 LSA的转换者Type-7 LSA 转换为 Type-5 LSA 转换稳定定时器的超时时间间隔，7/5 translate stability timer interval单位为秒

##### 1.1.10 display ospfv3 abr-asbr

display ospfv3 abr-asbr 命令用来显示到 OSPFv3 的区域边界路由器和自治系统边界路由器的路由信息。
【命令】
display ospfv3 [ process-id ] abr-asbr【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPFv3 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 OSPFv3进程下到区域边界路由器和自治系统边界路由器的路由信息。
【举例】
显示所有 进程的 和 路由。
\# OSPFv3 ABR ASBR <Sysname> display ospfv3 abr-asbr OSPFv3 Process 1 with Router ID 1.1.1.1 Destination : 1.1.1.2 Rtr Type : ABR Area : 0.0.0.0 Path Type: Intra Interface : Vlan102 BkInterface: Vlan101 NextHop : FE80:1:1::1 BkNexthop : FE80:1:2::2 Cost : 1 Destination : 1.1.1.3 Rtr Type : ASBR Area : 0.0.0.0 Path Type: Intra Interface : Vlan103 BkInterface: Vlan104 NextHop : FE80:2:1::1 BkNexthop : FE80:1:2::4 Cost : 1表1-2 命令显示信息描述表display ospfv3 abr-asbr字段 描述OSPFv3 Process 1 with Router ID 1.1.1.1 OSPFv3进程是1，Router ID是1.1.1.1 Destination ABR或ASBR的路由器ID Rtr Type 路由器类型，包括ABR和ASBR Area 下一跳地址所在的区域ID

字段 描述到ABR或ASBR的路由类型，取值为：
•Path Type Intra 表示区域内路由
• Inter 表示区域间路由Interface 路由出接口NextHop 下一跳地址BkInterface 备份出接口BkNextHop 备份下一跳地址Cost 从本路由器到达ABR或ASBR的开销

##### 1.1.11 display ospfv3 abr-summary

命令用来显示 OSPFv3 的 ABR 聚合信息。
display ospfv3 abr-summary【命令】
display ospfv3 [ process-id ] [ area area-id ] abr-summary [ ipv6-address prefix-length ] [ verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：当前的聚合配置所在进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 OSPFv3 进程的 ABR 聚合信息。
area-id：显示位于指定区域的 聚合信息。如果未指定本参数，将显示所有区域的area ABR ABR聚合信息。area-id 为区域的标识，可以是十进制整数（取值范围为 0～4294967295，系统会将其处理成 IPv4 地址格式）或 IPv4 地址格式。
prefix-length：显示指定 IPv6 地址的 ABR 聚合信息。ipv6-address 表示ipv6-address地址前缀；prefix-length 表示 地址前缀长度，取值范围为 0～128。如果未指定本参IPv6 IPv6数，将显示所有 ABR 聚合信息。
verbose：显示 ABR 聚合详细信息。如果未指定本参数，将显示 ABR 聚合的概要信息。
【举例】
\# 显示 OSPFv3 进程 1 的 ABR 聚合信息。
<Sysname> display ospfv3 1 abr-summary OSPFv3 Process 1 with Router ID 2.2.2.2 Area: 1.1.1.1

Total summary addresses: 1 Prefix : 1000:4::/32 Status : Advertise NULL0 : Active Cost : 1 (Configured)
Routes count: 2表1-3 display ospfv3 abr-summary 命令显示信息描述表字段 描述Area 聚合路由所在的区域Total summary addresses 聚合路由的路由数聚合路由的地址前缀Prefix聚合路由的状态：
Status • Advertise：已发布
• Not-advertise：未发布NULL0路由：
• Active：激活NULL0
• Inactive：未激活聚合路由的开销Cost • Configured：配置的聚合开销
• Not Configured：未配置聚合开销Routes count 被聚合的路由数\# 显示 OSPFv3 进程 1 的 ABR 聚合详细信息。
<Sysname> display ospfv3 1 abr-summary verbose OSPFv3 Process 1 with Router ID 2.2.2.2 Area: 1.1.1.1 Total summary addresses: 1 Prefix : 1000:4::/32 Status : Advertise NULL0 : Active Cost : 1 (Configured)
Routes count: 2 Destination Metric 1000:4:10:3::/96 1 1000:4:11:3::/96 1

表1-4 display ospfv3 abr-summary verbose 命令显示信息描述表字段 描述Destination 被聚合路由的目的地址路由的开销值Metric

##### 1.1.12 display ospfv3 asbr-summary

命令用来显示 的 聚合信息。
display ospfv3 asbr-summary OSPFv3 ASBR【命令】
display ospfv3 [ process-id ] asbr-summary [ ipv6-address prefix-length ] [ verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：当前的聚合配置所在进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 OSPFv3 进程的 ASBR 聚合信息。
ipv6-address prefix-length：显示指定 IPv6 地址的 ASBR 聚合信息。ipv6-address 表示 IPv6 地址前缀；prefix-length 表示 IPv6 地址前缀长度，取值范围为 0～128。如果未指定本参数，将显示所有 聚合信息。
ASBR verbose：显示 聚合详细信息。如果未指定本参数，将显示 聚合的概要信息。
ASBR ASBR【举例】
\# 显示 OSPFv3 进程 1 的 ASBR 聚合信息。
<Sysname> display ospfv3 1 asbr-summary OSPFv3 Process 1 with Router ID 2.2.2.2 Total summary addresses: 1 Prefix : 1000:4::/32 Status : Advertise NULL0 : Active Cost : 1 (Configured)
Tag : (Not configured)
Nssa-only : (Not configured)
Routes count: 2

表1-5 display ospfv3 asbr-summary 命令显示信息描述表字段 描述Total summary addresses 聚合路由的路由数聚合路由的地址前缀和前缀长度Prefix聚合路由的状态：
Status • Advertise：已发布
• Not-advertise：未发布NULL0路由：
• Active：激活NULL0
• Inactive：未激活聚合路由的开销：
Cost • Configured：配置的聚合开销
• Not configured：未配置聚合开销聚合路由的标记：
Tag • Configured：配置的聚合标记
• Not configured：未配置聚合标记是否配置Nssa-only：
Nssa-only • Configured：配置了 Nssa-only
• configured：未配置Not Nssa-only Routes count 被聚合的路由数\# 显示 OSPFv3 进程 1 的 ASBR 聚合详细信息。
<Sysname> display ospfv3 1 asbr-summary verbose OSPFv3 Process 1 with Router ID 2.2.2.2 Total summary addresses: 1 Prefix : 1000:4::/32 Status : Advertise NULL0 : Active Cost : 1 (Configured)
Tag : (Not configured)
Nssa-only : (Not configured)
Routes count: 2 Destination Protocol Process Type Metric 1000:4:10:3::/96 Static 0 2 1 1000:4:11:3::/96 Static 0 2 1

表1-6 display ospfv3 asbr-summary verbose 命令显示信息描述表字段 描述Destination 被聚合路由的前缀和前缀长度被聚合路由的协议类型Protocol Process 被聚合路由的协议进程ID Type 被聚合路由的类型被聚合路由的开销Metric

##### 1.1.13 display ospfv3 event-log

display ospfv3 event-log 命令用来显示 OSPFv3 的日志信息。
【命令】
display ospfv3 [ process-id ] event-log { lsa-flush | peer | spf }【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPFv3 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有进程的日志信息。
lsa-flush：LSA 老化的日志信息。
peer：邻居的日志信息。
spf：路由计算的日志信息。
【使用指导】
路由计算的日志信息是指更新到 IPv6 路由表的路由计数信息。
邻居的日志信息包括OSPFv3邻居状态倒退到DOWN，以及收到BadLSReq、SeqNumberMismatch和 1-Way 事件导致邻居状态倒退的信息。
【举例】
显示 进程 的 老化日志信息。
\# OSPFv3 1 LSA <Sysname>display ospfv3 1 event-log lsa-flush OSPFv3 Process 1 with Router ID 1.3.3.3 2014-09-02 07:55:25 Received MaxAge LSA from 1.1.1.1 Type: 3 LS ID: 0.0.0.2 AdvRtr: 1.1.1.1 Seq#: 80000001 2014-09-02 07:55:22 Flushed MaxAge LSA by itself

Type: 3 LS ID: 0.0.0.2 AdvRtr: 1.3.3.3 Seq#: 80000001 2014-09-02 07:55:07 Flushed MaxAge LSA by itself Type: 3 LS ID: 0.0.0.40 AdvRtr: 1.3.3.3 Seq#: 80000001 2014-09-02 07:55:07 Flushed MaxAge LSA by itself Type: 3 LS ID: 0.0.0.39 AdvRtr: 1.3.3.3 Seq#: 80000001表1-7 display ospfv3 event-log lsa-flush 命令显示信息描述表字段 描述Received MaxAge LSA from X.X.X.X 从Router ID为X.X.X.X的源收到MaxAge LSA Flushed MaxAge LSA by itself 自身发起的老化，洪泛MaxAge LSA LSA类型Type LS ID LSA链路状态ID AdvRtr 发布 LSA 的路由器，用 Router ID 表示Seq# LSA序列号\# 显示 OSPFv3 进程 1 的路由计算的日志信息。
<Sysname>display ospfv3 1 event-log spf OSPFv3 Process 1 with Router ID 1.3.3.3 Date Time Duration Intra Inter External Reason 2014-09-02 07:55:30 0.258827 0 0 0 Intra-area LSA 2014-09-02 07:55:30 0.679 0 0 0 Intra-area LSA 2014-09-02 07:55:30 0.51576 0 0 0 Intra-area LSA 2014-09-02 07:55:30 0.372 0 0 0 Intra-area LSA 2014-09-02 07:55:25 4.948353 0 0 0 Intra-area LSA 2014-09-02 07:55:25 0.5288 0 0 0 Area 0 full neighbor 2014-09-02 07:55:21 1.66013 0 0 0 Intra-area LSA 2014-09-02 07:55:20 0.450905 0 0 0 Intra-area LSA 2014-09-02 07:55:15 0.253688 0 0 0 Interface state change 2014-09-02 07:55:15 0.5693 0 0 0 Intra-area LSA表1-8 display ospfv3 event-log spf 命令显示信息描述表字段 描述路由计算开始的日期，单位为YYYY-MM-DD，其中YYYY为年，MM为月，DD为Date日Time 路由计算开始的时间，单位为hh:mm:ss，其中hh为小时，mm为分钟，ss为秒路由计算持续时间，单位为秒Duration Intra 区域内路由变化的个数Inter 区域间路由变化的个数

字段 描述External 外部路由变化的个数路由计算的原因：
• Intra-area LSA：区域内 LSA 变化
• Inter-area LSA：区域间 LSA 变化
• LSA：外部 变化External LSA
• Configuration：配置变化
• neighbor：区域 邻居个数变化Area 0 full 0 FULL Reason • Area 0 up interface：区域 0 UP 接口个数变化
• AS number：AS 号变化
• ABR summarization：ABR 聚合变化
• GR end：GR 结束
• Routing policy：路由策略变化
• Intra-area tunnel ：区域内隧道变化
• Others： 除上述原因之外的其他原因\# 显示 OSPFv3 进程 1 的邻居的日志信息。
<Sysname> display ospfv3 1 event-log peer OSPFv3 Process 1 with Router ID 1.1.1.1 Date Time Router ID Reason InstID Interface 2014-09-02 16:39:13 1.3.3.3 IntPhyChange 0 Vlan101 2014-09-02 16:36:46 1.3.3.3 IntPhyChange 0 Vlan101 2014-09-02 16:34:49 1.3.3.3 BFDDown 0 Vlan101 2014-09-02 10:08:45 1.3.3.3 DeadExpired 0 Vlan102 2014-09-02 10:08:39 1.3.3.3 DeadExpired 0 VLINK1 2014-09-02 10:08:08 1.3.3.3 BFDDown 0 Vlan101表1-9 display ospfv3 event-log peer 命令显示信息描述表字段 描述邻居状态变化的日期，单位为YYYY-MM-DD，其中YYYY为年，MM为月，Date DD为日邻居状态变化的时间，单位为hh:mm:ss，其中hh为小时，mm为分钟，ss Time为秒邻居的Router Router ID ID

字段 描述邻居状态变化的原因：
•ResetConnect：内存不足，邻居关系中断
• IntChange：接口参数改变
• ResetOspfv3：重启 OSPFv3 进程
• UndoOspfv3：删除 OSPFv3 进程
• UndoArea：删除 OSPFv3 区域
• UndoInt：接口去使能
• IntLogChange：接口逻辑属性变化
• IntPhyChange：接口物理属性变化Reason • DeadExpired：Dead Timer 超时
• Retrans：重传过多
• BFDDown：BFD Down
• SilentInt：配置抑制接口
• ConfStubArea：配置 Stub 区域参数
• ConfNssaArea：配置 NSSA 区域参数
• VlinkDown：虚连接 Down
• BadLSReq：收到 BadLSReq 事件
• SeqMismatch：收到 事件SeqNumberMismatch
• 1-Way：收到 1-Way 事件InstID 接口所属的实例ID接口名称Interface

##### 1.1.14 display ospfv3 graceful-restart

display ospfv3 graceful-restart 命令用来显示 OSPFv3 进程的 GR 状态信息。
【命令】
display ospfv3 [ process-id ] graceful-restart [ verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id： OSPFv3 进程号，取值范围为 1 ～ 65535 。如果未指定本参数，将显示所有 OSPFv3进程的 GR 状态信息。
verbose：显示 GR 详细状态信息。如果未指定本参数，将显示 OSPFv3 进程的 GR 状态概要信息。

【举例】
\# 显示所有 OSPFv3 进程的 GR 状态信息（Restarter）。
<Sysname> display ospfv3 graceful-restart OSPFv3 Process 1 with Router ID 3.3.3.3 Graceful-restart capability : Enable Graceful-restart support : Planned and unplanned, Partial Helper capability : Enable Helper support : Planned and unplanned Current GR state : Normal Graceful-restart period : 120 seconds Number of neighbors under helper: 0 Number of restarting neighbors : 0 Last exit reason:
Restarter: None Helper : None表1-10 命令显示信息描述表display ospfv3 graceful-restart字段 描述OSPFv3 Process 1 with Router ID 3.3.3.3 OSPFv3进程是1，Router ID是3.3.3.3的GR状态信息是否使能OSPFv3协议的GR能力Graceful-restart capability • Enable：使能
• Disable：未使能进程GR支持模式（GR使能时才显示）：
• Planned and unplanned：支持计划和非计划 GR
• only：只支持计划性Graceful-restart support Planned GR
• Partial：支持接口级 GR
• Global：不支持接口级 GR，支持全局 GR是否使能OSPFv3协议的GR Helper能力Helper capability • Enable：使能
• ：未使能Disable显示Helper的支持模式（Helper使能时才显示）：
• Strict LSA check：Helper 端支持严格的 LSA 检查Helper support
• Planned and unplanned：支持作为计划和非计划 GR 的Helper
• Planned only：只支持作为计划 GR 的 Helper当前GR的状态，其状态有如下几种：
•Normal：表示正处在非 GR 的正常状态Current GR state
• Under GR：表示正在 GR 过程中，自身作为 Restarter
• Under Helper：表示正在 GR 过程中，自身作为 Helper GR重启间隔时间Graceful-restart period

字段 描述Number of neighbors under helper 处于GR Helper模式的邻居个数Number of restarting neighbors 处于GR Restarter模式的邻居个数上次退出原因，其中：
• Restarter：表示退出 Restarter 的原因None：无(cid:123)
Completed：GR 完成(cid:123)
Interval timer is fired：GR 定时器超时(cid:123)
Interface state change：接口状态变化(cid:123)
Received 1-way hello：收到邻居的 1-way Hello 报文(cid:123)
neighbor：邻居发生 操作Reset Reset (cid:123)
DR or BDR change：DR 或 BDR 发生变化(cid:123)
Last exit reason
• Helper：表示退出 Helper 的原因None：无(cid:123)
Completed：GR 完成(cid:123)
Received 1-way hello：收到邻居的 1-way Hello 报文(cid:123)
Grace Period timer is fired：GR 定时器超时(cid:123)
Lsa check failed：LSA 检查未通过(cid:123)
neighbor：邻居发生 操作Reset Reset (cid:123)
Received MAXAGE gracelsa but neighbor is not full：收(cid:123)
到到达老化时间的 Grace LSA，但邻居状态未达到 FULL状态\# 显示 OSPFv3 进程的 GR 详细状态信息（Restarter）。
<Sysname> display ospfv3 graceful-restart verbose OSPFv3 Process 1 with Router ID 3.3.3.3 Graceful-restart capability : Enable Graceful-restart support : Planned and unplanned, Partial Helper capability : Enable Helper support : Planned and unplanned Current GR state : Normal Graceful-restart period : 120 seconds Number of neighbors under helper: 0 Number of restarting neighbors : 0 Last exit reason:
Restarter: None Helper : None Area: 0.0.0.0 Area flag: Normal Area up interface count: 1

Virtual-link Neighbor-ID: 100.1.1.1, Neighbor-state: Full Restarter state: Normal State: P-2-P Type: Virtual Interface: 6696 (Vlan-interface200), Instance-ID: 0 Local IPv6 address: 200:1:FFFF::1 Remote IPv6 address: 201:FFFF::2 Transit area: 0.0.0.1 Last exit reason:
Restarter: None Helper : None Neighbor GR state Last helper exit reason
100.1.1.1 Normal None Area: 0.0.0.1 Area flag: Transit Area up interface count: 3 Interface: 5506 (Vlan-interface3), Instance-ID: 0 Restarter state: Normal State: DR Type: Broadcast Last exit reason:
Restarter: None Helper : None Neighbor count of this interface: 0 Number of neighbors under helper: 0 Interface: 6696 (Vlan-interface200), Instance-ID: 0 Restarter state: Normal State: DR Type: Broadcast Last exit reason:
Restarter: None Helper : None Neighbor count of this interface: 1 Number of neighbors under helper: 0 Neighbor GR state Last helper exit reason
100.1.1.1 Normal None Area: 0.0.0.5 Area flag: NSSANoSummaryNoImportRoute 7/5 translator state: Disabled 7/5 translate stability timer interval: 0 Area up interface count: 0表1-11 display ospfv3 graceful-restart 命令显示信息描述表字段 描述Area 区域信息

字段 描述区域类型：
•Normal：普通区域
• Transit：传输区
• Stub：Stub 区域Area flag • StubNoSummary：完全 Stub 区域
• NSSA：NSSA 区域
• NSSANoSummary：完全 NSSA 区域
• NSSANoSummaryNoImportRoute：完全 NSSA 区域，配置了 no-import-route 参数LSA转换为Type-5 LSA的转换者状态，取值为：
Type-7
• Enabled：表示通过命令指定 Type-7 LSA转换为 Type-5 LSA的转换者7/5 translator state • Elected：表示通过选举指定 转换为Type-7 LSA Type-5 LSA的转换者
• Disabled：表示不是 Type-7 LSA 转换为 Type-5 LSA 的转换者Type-7 LSA转换为Type-5 LSA转换稳定定时器的超时时间，单位7/5 translate stability timer interval为秒Area up interface count 区域下up的接口计数Interface 区域内的普通接口，以及虚连接所属的出接口Instance-ID 接口实例ID Restarter state 作为Restarter的状态State 接口状态Type 接口的网络类型接口下的邻居个数Neighbor count of this interface Neighbor 邻居Router ID邻居的GR状态：
• Normal：普通状态GR state
• Under GR：进程正在 GR
• Under Helper：进程正在作为 GR Helper Last helper exit reason 上一次作为该邻居Helper退出的原因Virtual-link Neighbor-ID 虚连接的邻居Router ID虚连接和邻居的状态，包括Down、Init、2-Way、ExStart、Exchange、Neighbor-State Loading和Full本地 地址Local IPv6 address IPv6 Remote IPv6 address 对端IPv6地址Transit area 传输区域ID

##### 1.1.15 display ospfv3 interface

命令用来显示 OSPFv3 的接口信息。
display ospfv3 interface【命令】
display ospfv3 [ process-id ] interface [ interface-type interface-number | verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPFv3 进程号，取值范围为 1～65535。
interface-number：接口类型和接口编号。显示指定接口的详细信息。
interface-type verbose：显示所有接口的详细信息。
【使用指导】
如果未指定 进程号，将显示所有 进程的接口概要信息。
OSPFv3 OSPFv3如果未指定接口或参数 verbose，将显示所有接口的概要信息。
【举例】
\# 显示运行 OSPFv3 的接口 Vlan-interface1 的信息。
<Sysname> display ospfv3 interface vlan-interface 1 OSPFv3 Process 1 with Router ID 1.1.1.1 Area: 0.0.0.0
------------------------------------------------------------------------- Vlan-interface1 is up, line protocol is up Interface ID 65697 Instance ID 0 IPv6 prefixes FE80::200:12FF:FE34:1 (Link-Local address)
2001::1 Cost: 1 State: BDR Type: Broadcast MTU: 1500 Priority: 1 Designated router: 2.2.2.2 Backup designated router: 1.1.1.1 Timers: Hello 10, Dead 40, Poll 40, Retransmit 5, Transmit delay 1 FRR backup: Enabled Neighbor count is 1, Adjacent neighbor count is 1 Primary path detection mode: BFD echo IPsec profile name: profile001

Keychain authentication: Enabled (test), inherited Exchanging/Loading neighbors: 0 Wait timer: Off, LsAck timer: Off Prefix-suppression is enabled表1-12 display ospfv3 interface 命令显示信息描述表字段 描述Area 接口所属的区域ID Interface ID 接口ID实例ID Instance ID IPv6 prefixes IPv6前缀Cost 接口开销根据OSPFv3接口状态机确定的当前接口状态，取值为：
• Down：表示在接口上没有发送和接收任何路由协议的报文
• Waiting：表示接口开始发送和接收 Hello 报文，并试图去识别网络上的 DR 和 BDR
• P-2-P：表示接口将每隔 HelloInterval 的时间间隔发送 Hello 报文，并State尝试和接口链路另一端相连的路由器建立邻接关系
•DR：表示路由器是所连网络的指定路由器
• BDR：表示路由器是所连网络的备份指定路由器
• DROther：表示路由器既不是所连网络的指定路由器，也不是所连网络的备份指定路由器接口的网络类型，取值为：
• PTP：表示网络类型为点对点
• PTMP：表示网络类型为点对多点Type
• Broadcast：表示网络类型为广播
• NBMA：表示网络类型为NBMA MTU 接口MTU的值Priority 接口的DR优先级Designated router 本链路上的DR本链路上的BDR Backup designated router配置的OSPFv3定时器，分别定义如下：
• Hello：表示接口发送 Hello 报文的时间间隔，单位为秒Timers • Dead：表示邻居的失效时间，单位为秒
• Poll：表示 NBMA 网络上发送轮询 Hello 报文的时间间隔，单位为秒
• Retransmit：表示接口重传 LSA 的时间间隔，单位为秒Transmit Delay 接口对 LSA 的传输延迟时间，单位为秒是否使能接口参与LFA（Loop Free Alternate）计算：
FRR backup • Enabled：使能
• Disabled：关闭

字段 描述Neighbor count 接口的邻居数目主链路检测方式：
Primary path detection mode • BFD ctrl：BFD 控制报文检测方式
• BFD echo：BFD echo 报文检测方式Adjacent neighbor count 接口的邻接数目IPsec profile name IPsec安全框架名Keychain authentication: Enabled OSPFv3接口采用keychain验证模式，keychain名称为test，inherited表示(test), inherited 接口继承的是其所属区域下配置的keychain验证模式Exchanging/Loading neighbors 处于Exchanging或Loading状态的邻居个数等待定时器，其中：
Wait timer • Off：关闭
• On：开启报文确认定时器，其中：
LsAck timer • Off：关闭
• On：开启Prefix-suppression is enabled 接口处于前缀抑制

##### 1.1.16 display ospfv3 lsdb

命令用来显示 的链路状态数据库信息。
display ospfv3 lsdb OSPFv3【命令】
display ospfv3 [ process-id ] lsdb [ { external | grace | inter-prefix | inter-router | intra-prefix | link | network | nssa | router | unknown [ type ] } [ link-state-id ] [ originate-router router-id | self-originate ] | statistics | total | verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPFv3 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 OSPFv3进程的链路状态数据库信息。
external：显示链路状态数据库中 LSA（AS LSA）的信息。
Type-5 External grace：显示链路状态数据库中 LSA（Grace LSA）的信息。
Type-11 inter-prefix：显示链路状态数据库中 Type-3 LSA（Inter-Area-Prefix LSA）的信息。

inter-router：显示链路状态数据库中 Type-4 LSA（Inter-Area-Router LSA）的信息。
intra-prefix：显示链路状态数据库中 Type-9 LSA（Intra-Area-Prefix LSA）的信息。
link：显示链路状态数据库中 Type-8 LSA（Link LSA）的信息。
network：显示链路状态数据库中 Type-2 LSA（Network LSA）的信息。
nssa：显示链路状态数据库中 Type-7 LSA（NSSA LSA）的信息。
router：显示链路状态数据库中 Type-1 LSA（Router LSA）的信息。
unknown：显示链路状态数据库中未知类型 LSA 的信息。
type：LSA 类型，取值范围为十六进制数 0～ffff。如果未指定本参数，将显示所有未知类型 LSA的信息。
link-state-id：链路状态 ID，IPv4 地址形式。
router-id：发布该 LSA 的路由器的 Router ID。
originate-router self-originate：显示本地路由器自己产生的 LSA 的链路状态数据库信息。
statistics：显示链路状态数据库中 LSA 的统计信息。
total：显示链路状态数据库中各种 LSA 的总数。
verbose：显示详细信息。如果未指定本参数，将显示概要信息。
【举例】
\# 显示 OSPFv3 的链路状态数据库信息。
<Sysname> display ospfv3 lsdb OSPFv3 Process 1 with Router ID 1.1.1.1 Link-LSA (Interface Vlan-interface100)
------------------------------------------------------------------------- Link state ID Origin router Age SeqNumber Checksum Prefix
0.15.0.8 2.2.2.2 0691 0x80000041 0x8315 1
0.0.0.3 1.1.1.1 0623 0x80000001 0x0fee 1 Router-LSA (Area 0.0.0.1)
------------------------------------------------------------------------- Link state ID Origin router Age SeqNumber Checksum Link
0.0.0.0 1.1.1.1 0013 0x80000068 0x5d5f 2
0.0.0.0 2.2.2.2 0024 0x800000ea 0x1e22 0 Network-LSA (Area 0.0.0.1)
------------------------------------------------------------------------- Link state ID Origin router Age SeqNumber Checksum
0.15.0.8 2.2.2.2 0019 0x80000007 0x599e Intra-Area-Prefix-LSA (Area 0.0.0.1)
------------------------------------------------------------------------- Link state ID Origin router Age SeqNumber Checksum Prefix Reference
0.0.0.2 2.2.2.2 3600 0x80000002 0x2eed 2 Network-LSA
0.0.0.1 2.2.2.2 0018 0x80000001 0x1478 1 Network-LSA

表1-13 display ospfv3 lsdb 命令显示信息描述表字段 描述Link state ID 链路状态ID产生LSA的路由器Origin router Age LSA老化时间SeqNumber LSA序列号LSA校验和Checksum Prefix 前缀数目Link 链路数目Reference 引用的LSA类型\# 显示 OSPFv3 链路状态数据库中 Link-LSA 的信息。
<Sysname> display ospfv3 lsdb link OSPFv3 Process 1 with Router ID 1.1.1.1 Link-LSA (Interface Vlan-interface100)
------------------------------------------------------------------------- LS age : 833 LS type : Link-LSA Link state ID : 0.15.0.8 Originating router: 2.2.2.2 LS seq number : 0x80000041 Checksum : 0x8315 Length : 56 Priority : 1 Options : 0x000013 (-|R|-|x|E|V6)
Link-Local address: fe80::200:5eff:fe00:100 Number of prefixes: 1 Prefix : 1001::/64 Prefix options: 0 (-|-|x|-|-)
表1-14 display ospfv3 lsdb link 命令显示信息描述表字段 描述LS age LSA老化时间LS type LSA类型Link state ID 链路状态ID Originating router 产生LSA的路由器LS seq number LSA序列号Checksum LSA校验和LSA长度Length

字段 描述Priority 路由器优先级Options 选项链路本地地址Link-Local address Number of prefixes 前缀的数目Prefix 地址前缀Prefix options 前缀选项\# 显示 OSPFv3 链路状态数据库中 LSA 的统计信息。
<System> display ospfv3 lsdb statistics OSPFv3 Process 1 with Router ID 1.1.1.1
------------------------------------------------------------------------- Area ID Router Network IntePre InteRou IntraPre NSSA
0.0.0.1 2 0 0 0 2 0
0.0.0.3 1 0 0 0 1 1 Total 3 0 0 0 3 1
------------------------------------------------------------------------- Link Grace ASE Total 4 0 0表1-15 display ospfv3 lsdb statistics 命令显示信息描述表字段 描述区域ID，显示该区域各类LSA的总数Area ID Router Type-1 LSA的数目Network Type-2 LSA的数目IntePre Type-3 LSA的数目InteRou Type-4 LSA的数目IntraPre Type-9 LSA 的数目NSSA Type-7 LSA的数目LSA的数目Link Type-8 Grace Type-11 LSA的数目ASE Type-5 LSA的数目Total 不同区域相同类型LSA的总数\# 显示 OSPFv3 的链路状态数据库的详细信息。
<Sysname> display ospfv3 lsdb verbose OSPFv3 Process 1 with Router ID 1.1.1.1

Link-LSA (Interface Vlan-interface100)
------------------------------------------------------------------------- Link state ID Origin router Age SeqNumber Checksum Prefix
0.15.0.8 2.2.2.2 0691 0x80000041 0x8315 1 SendCnt: 0 RxmtCnt: 0 Status: Stale
0.0.0.3 1.1.1.1 0623 0x80000001 0x0fee 1 SendCnt: 0 RxmtCnt: 0 Status: Stale Router-LSA (Area 0.0.0.1)
------------------------------------------------------------------------- Link state ID Origin router Age SeqNumber Checksum Link
0.0.0.0 1.1.1.1 0013 0x80000068 0x5d5f 2 SendCnt: 0 RxmtCnt: 0 Status: Stale
0.0.0.0 2.2.2.2 0024 0x800000ea 0x1e22 0 SendCnt: 0 RxmtCnt: 0 Status: Stale Network-LSA (Area 0.0.0.1)
------------------------------------------------------------------------- Link state ID Origin router Age SeqNumber Checksum
0.15.0.8 2.2.2.2 0019 0x80000007 0x599e SendCnt: 0 RxmtCnt: 0 Status: Stale Intra-Area-Prefix-LSA (Area 0.0.0.1)
------------------------------------------------------------------------- Link state ID Origin router Age SeqNumber Checksum Prefix Reference
0.0.0.2 2.2.2.2 3600 0x80000002 0x2eed 2 Network-LSA SendCnt: 0 RxmtCnt: 0 Status: Stale
0.0.0.1 2.2.2.2 0018 0x80000001 0x1478 1 Network-LSA SendCnt: 0 RxmtCnt: 0 Status: Stale表1-16 display ospfv3 lsdb verbose 命令显示信息描述表字段 描述SendCnt 待发送该LSA的接口数目RxmtCnt 该 LSA 在重传列表中的数目LSA所处的状态：
• Normal：正常状态
• Delayed：延迟生成的 LSA Status
• routed：Maxage 的 且已经经过拓扑前缀处理Maxage LSA
• Self originated：收到自己产生的 LSA
• Stale：GR 过程中收到自己产生的LSA

##### 1.1.17 display ospfv3 nexthop

display ospfv3 nexthop 命令用来显示 OSPFv3 的路由下一跳信息。

【命令】
display ospfv3 [ process-id ] nexthop【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPFv3 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有OSPFv3进程的下一跳信息。
【举例】
\# 显示 OSPFv3 进程 1 的路由下一跳信息。
<Sysname> display ospfv3 1 nexthop OSPFv3 Process 1 with Router ID 1.1.1.1 Nexthop : FE80::20C:29FF:FED7:F308 Interface: Vlan102 RefCount: 4 Status : Valid NbrID : 1.1.1.1 NbrIntID : 21 Nexthop : FE80::20C:29FF:FED7:F312 Interface: Vlan103 RefCount: 3 Status : Valid NbrID : 1.1.1.1 NbrIntID : 38表1-17 display ospfv3 nexthop 命令显示信息描述表字段 描述下一跳地址Nexthop Interface 出接口名RefCount 下一跳引用计数该下一跳的状态：
Status • Valid：有效
• Invalid：无效邻居路由器ID NbrID NbrIntID 邻居的接口ID

##### 1.1.18 display ospfv3 non-stop-routing

命令用来显示 进程的 状态信息。
display ospfv3 non-stop-routing OSPFv3 NSR

【命令】
display ospfv3 [ process-id ] non-stop-routing【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPFv3 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有OSPFv3进程的 NSR 状态信息。
【举例】
\# 显示所有 OSPFv3 进程的 NSR 状态信息。
<Sysname> display ospfv3 non-stop-routing OSPFv3 Process 1 with Router ID 3.3.3.3 Nonstop Routing capability: Enabled Upgrade phase : Normal表1-18 display ospfv3 non-stop-routing 命令显示信息描述表字段 描述是否使能OSPFv3协议的NSR能力
•Nonstop Routing capability Enabled：使能
• Disabled：未使能NSR的各个阶段，有如下几种：
• Normal：普通状态
• Preparation：准备阶段
• Smooth：数据平滑阶段Upgrade phase
• Precalculation ：路由计算预处理阶段
• Calculation：路由计算阶段
• Redistribution：路由引入阶段

##### 1.1.19 display ospfv3 peer

display ospfv3 peer 命令用来显示 OSPFv3 的邻居信息。
【命令】
display ospfv3 [ process-id ] [ area area-id ] peer [ [ interface-type interface-number ] [ verbose ] | peer-router-id | statistics ]

【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPFv3 进程号，取值范围为 1～65535。如果不指定本参数，则显示所有 OSPFv3进程的邻居信息。
area-id：显示位于指定区域的邻居信息。area-id 为区域的标识，可以是十进制整数（取area值范围为 0～4294967295，系统会将其处理成 IPv4 地址格式）或 IPv4 地址格式。如果不指定本参数，则显示所有区域的邻居信息。
interface-number：接口类型和接口编号。
interface-type verbose：显示邻居的详细信息。
peer-router-id：显示指定邻居的信息。
statistics：显示 OSPFv3 邻居的统计信息。
【使用指导】
如果接口参数、邻居 Router ID 参数都不输入，则显示所有接口的邻居信息。
【举例】
显示 进程 的邻居信息。
\# OSPFv3 1 <Sysname> display ospfv3 1 peer vlan-interface 1 OSPFv3 Process 1 with Router ID 1.1.1.1 Area: 0.0.0.1
------------------------------------------------------------------------- Router ID Pri State Dead-Time InstID Interface
2.2.2.2 1 Init/ - 00:00:36 0 Vlan1表1-19 命令显示信息描述表display ospfv3 peer字段 描述Router ID 邻居ID邻居路由器优先级Pri State 邻居状态Dead-Time 邻居路由器的失效时间InstID 实例ID Interface 和邻居相连的接口\# 显示接口上的 OSPFv3 进程 1 的邻居详细信息。
<Sysname> display ospfv3 1 peer vlan-interface 1 verbose

OSPFv3 Process 1 with Router ID 1.1.1.1 Area 0.0.0.1 interface Vlan1's neighbors Router ID: 2.2.2.2 Address: FE80::200:5EFF:FE00:100 State: ExStart Mode: None Priority: 1 DR: 2.2.2.2 BDR: None MTU: 1500 Options is 0x000413 (AT|-|-|-|-|-|R|-|x|E|V6)
Dead timer due in 00:00:33 Neighbor is up for 00:24:19 Authentication sequence: (high) 0, (low) 59755 Neighbor state change count: 205 Database Summary List 0 Link State Request List 0 Link State Retransmission List 0 Neighbor interface ID: 8037 GR state: Normal Grace period: 0 Grace period timer: Off DD Rxmt Timer: Off LS Rxmt Timer: On表1-20 display ospfv3 peer verbose 命令显示信息描述表字段 描述Router ID 邻居的Router ID Address 接口链路本地地址邻居状态State路由器在数据库同步阶段，路由器与邻居协商的主从关系，取值为：
Mode • Nbr is master：邻居路由器为主路由器
• Nbr is slave：邻居路由器为从路由器Priority 邻居路由器优先级DR 接口所属网段的DR接口所属网段的BDR BDR MTU 接口MTU的值邻居的LSA选项，各选项含义如下：
• AT：报文是否带验证字段
• DC：支持按需链路
• R：是否为活跃路由器Options
• N：是否支持 NSSA 外部 LSA
• x：保留
• E：AS 外部 LSA 的接受能力
• V6：是否参与 IPv6 路由计算Dead定时器距离超时的剩余时间，单位为hh:mm:ss，其中hh为小时，mm Dead timer due in hh:mm:ss为分钟，ss为秒。Dead定时器超时后，认为该邻居已失效

字段 描述邻居关系建立的时长，单位为hh:mm:ss，其中hh为小时，mm为分钟，ss Neighbor is up for hh:mm:ss为秒Authentication sequence: (high) 0,接收到的报文中的验证序列号，高32位的值为0，低32位的值为59755 (low) 59755邻居状态发生改变的次数Neighbor state change count Database Summary List 需要DD报文发送的LSA个数Link State Request List 链路状态请求列表中LSA个数链路状态重传列表中LSA个数Link State Retransmission List Neighbor interface ID 邻居的接口ID GR状态，取值为：
• Normal：普通状态GR state • Doing GR：正在作为 GR Restarter
• Complete GR：GR 完成
• Helper：正在作为 GR Helper Grace period 发送Grace LSA的间隔发送Grace LSA的间隔定时器，其中：
Grace period timer • Off： 关闭
• On：开启DD报文重传定时器，其中：
DD Rxmt Timer • Off： 关闭
•On：开启LSU报文重传定时器，其中：
LS Rxmt Timer • Off： 关闭
• On：开启\# 显示所有 OSPFv3 邻居的统计信息。
<Sysname> display ospfv3 peer statistics OSPFv3 Process 1 with Router ID 1.1.1.1
------------------------------------------------------------------------- Area ID Down Attempt Init 2-Way ExStart Exchange Loading Full Total
0.0.0.0 0 0 0 0 0 0 0 1 1 Total 0 0 0 0 0 0 0 1 1表1-21 display ospfv3 peer statistics 命令显示信息描述表字段 描述区域标识Area ID该状态为OSPFv3建立邻居关系的初始化状态，表示OSPFv3路由器在一定时间之内没Down有收到从某一邻居路由器发送来的信息

字段 描述该状态仅对NBMA网络上的邻居有效，表示最近没有从邻居收到信息，但仍需作出进Attempt一步的尝试，用以与邻居联系此状态表示OSPFv3路由器已经接收到邻居路由器发送来的Hello数据包，但该Hello数Init据包内没有包含自己的Router ID，还没有建立起双方的双向通信此状态表示OSPFv3路由器与邻居路由器的双向通信已经建立。DR及BDR的选择是在2-Way这个状态（或更高的状态）完成的ExStart 在此状态，路由器要确定邻居双方的主从关系并决定初始的DD报文的序列号Exchange 在此状态，OSPFv3路由器向其邻居路由器发送DD报文来交换链路状态信息Loading 在此状态，OSPFv3路由器向邻居路由器发送LSR报文，请求最新的链路状态信息在此状态，建立起邻居关系的路由器之间已经完成了数据库同步的工作，它们的链路Full状态数据库已经一致Total 所有区域中处于相同状态的邻居数目的总和

##### 1.1.20 display ospfv3 request-queue

命令用来显示 OSPFv3 请求列表的信息。
display ospfv3 request-queue【命令】
display ospfv3 [ process-id ] [ area area-id ] request-queue [ interface-type interface-number ] [ neighbor-id ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
：OSPFv3 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 OSPFv3 process-id进程的请求列表信息。
area-id：显示位于指定区域的信息。area-id 为区域的标识，可以是十进制整数（取值area范围为 0～4294967295，系统会将其处理成 IPv4 地址格式）或 IPv4 地址格式。如果未指定本参数，将显示所有 OSPFv3 区域的请求列表信息。
interface-type interface-number：接口类型和编号。如果未指定本参数，将显示所有接口的请求列表信息。
neighbor-id：邻居路由器的 Router ID。如果未指定本参数，将显示所有邻居路由器的请求列表信息。
【举例】
\# 显示 OSPFv3 请求列表的信息。
<Sysname> display ospfv3 request-queue

OSPFv3 Process 1 with Router ID 1.1.1.1 Area: 0.0.0.0 Interface Vlan-interface100
------------------------------------------------------------------------- Nbr-ID 1.3.3.3 Request List Type LinkState ID AdvRouter SeqNum Age CkSum 0x4005 0.0.34.127 1.3.3.3 0x80000001 0027 0x274d 0x4005 0.0.34.128 1.3.3.3 0x80000001 0027 0x2d45 0x4005 0.0.34.129 1.3.3.3 0x80000001 0027 0x333d 0x4005 0.0.34.130 1.3.3.3 0x80000001 0027 0x3935表1-22 display ospfv3 request-queue 命令显示信息描述表字段 描述Area 区域ID Interface 接口类型和序号Nbr-ID 邻居ID请求列表信息Request List Type LSA类型LinkState ID 链路状态标示符AdvRouter 通告路由器LSA序列号SeqNum Age LSA老化时间CkSum 校验和

##### 1.1.21 display ospfv3 retrans-queue

命令用来显示 OSPFv3 重传列表的信息。
display ospfv3 retrans-queue【命令】
display ospfv3 [ process-id ] [ area area-id ] retrans-queue [ interface-type interface-number ] [ neighbor-id ]【视图】
任意视图【缺省用户角色】
network-admin network-operator

【参数】
process-id：OSPFv3 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 OSPFv3进程的重传列表信息。
area-id：显示位于指定区域的信息。area-id 为区域的标识，可以是十进制整数（取值area范围为 0～4294967295，系统会将其处理成 地址格式）或 地址格式。如果未指定本参数，IPv4 IPv4将显示所有 OSPFv3 区域的重传列表信息。
interface-type interface-number：接口类型和编号。如果未指定本参数，将显示所有接口的重传列表信息。
neighbor-id：邻居路由器的 Router ID。如果未指定本参数，将显示所有邻居路由器的重传列表信息。
【举例】
显示 重传列表的信息。
\# OSPFv3 <Sysname> display ospfv3 retrans-queue OSPFv3 Process 1 with Router ID 1.1.1.1 Area: 0.0.0.0 Interface Vlan-interface100
------------------------------------------------------------------------- Nbr-ID 1.2.2.2 Retransmit List Type LinkState ID AdvRouter SeqNum Age CkSum 0x2009 0.0.0.0 1.3.3.3 0x80000001 3600 0x49fb表1-23 display ospfv3 retrans-queue 命令显示信息描述表字段 描述Area 区域ID Interface 接口类型和序号邻居ID Nbr-ID Retransmit List 重传列表信息Type LSA类型LinkState ID 链路状态标示符通告路由器AdvRouter SeqNum LSA序列号Age LSA老化时间校验和CkSum

##### 1.1.22 display ospfv3 routing

display ospfv3 routing 命令用来显示 OSPFv3 路由表的信息。

【命令】
display ospfv3 [ process-id ] routing [ ipv6-address prefix-length ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPFv3 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有OSPFv3进程的路由表信息。
ipv6-address prefix-length：显示指定 IPv6 地址的 OSPFv3 路由表的信息。ipv6-address表示 IPv6 地址前缀；prefix-length 表示 IPv6 地址前缀长度，取值范围为 0～128。
【举例】
\# 显示 OSPFv3 路由表的信息。
<Sysname> display ospfv3 routing OSPFv3 Process 1 with Router ID 9.9.9.9
------------------------------------------------------------------------- I - Intra area route, E1 - Type 1 external route, N1 - Type 1 NSSA route IA - Inter area route, E2 - Type 2 external route, N2 - Type 2 NSSA route
* - Selected route
*Destination: 1::/64 Type : IA Area : 0.0.0.1 AdvRouter : 2.2.2.2 Preference : 10 NibID : 0x23000003 Cost : 2 Interface : Vlan10 BkInterface: N/A Nexthop : FE80::6AC7:45FF:FE5C:206 BkNexthop : N/A Status : Rely
*Destination: 23::/64 Type : I Area : 0.0.0.1 AdvRouter : 3.3.3.3 Preference : 10 NibID : 0x23000001 Cost : 1 Interface : Vlan10 BkInterface: N/A Nexthop : ::
BkNexthop : N/A Status : Direct
*Destination: 8::/64 Type : E2 Tag : 1 AdvRouter : 1.1.1.1 Preference : 150 NibID : 0x23000004 Cost : 1

Interface : Vlan10 BkInterface: N/A Nexthop : FE80::6AC7:45FF:FE5C:206 BkNexthop : N/A Status : Rely Total: 3 Intra area: 3 Inter area: 0 ASE: 0 NSSA: 0表1-24 display ospfv3 routing 命令显示信息描述表字段 描述Destination 目的网段Type 路由类型区域ID Area AdvRouter 发布LSA的路由器，用Router ID表示Preference 路由优先级NibID 路由下一跳信息的ID值Cost 路由开销值Interface 出接口BkInterface 备份下一跳出接口下一跳地址Nexthop BkNexthop 备份下一跳地址路由状态，具体如下：
• Local：该条路由在本地，未发送给路由管理模块
• Invalid：路由下一跳无效
•Stale：该路由下一跳较旧Status
• Normal：正常可用状态
• Delete：处于删除状态
• Direct：该条路由为直连路由
• Rely：该条路由为迭代路由出接口Interface AdvRouter 发布路由器Area 区域ID Tag 外部路由标记路由优先级Preference Total 路由总数目Intra area 区域内路由数目Inter area 区域间路由数目ASE 5类外部路由数目

字段 描述NSSA 7类外部路由数目

##### 1.1.23 display ospfv3 spf-tree

命令用来显示 区域的最短路径树信息。
display ospfv3 spf-tree OSPFv3【命令】
display ospfv3 [ process-id ] [ area area-id ] spf-tree [ verbose ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPFv3 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有OSPFv3进程下区域的最短路径树信息。
area-id：显示指定区域的最短路径树信息。如果未指定本参数，将显示所有区域的最短路area径树信息。area-id 为区域的标识，可以是十进制整数（取值范围为 0～4294967295，系统会将其处理成 IPv4 地址格式）或 IPv4 地址格式。
verbose：显示 OSPFv3 区域的最短路径树的详细信息。如果未指定本参数，将显示 OSPFv3 区域的最短路径树的概要信息。
【举例】
\# 显示 OSPFv3 进程 1 下区域 0 的最短路径树信息。
<Sysname> display ospfv3 1 area 0 spf-tree OSPFv3 Process 1 with Router ID 1.1.1.1 Flags: S-Node is on SPF tree R-Node is directly reachable I-Node or Link is init D-Node or Link is to be deleted P-Neighbor is parent A-Node is in candidate list C-Neighbor is child H-Nexthop changed N-Link is a new path V-Link is involved Area: 0.0.0.0 Shortest Path Tree SPFNode Type Flag SPFLink Type Cost Flag >1.1.1.1 Router S R
-->2.2.2.2 RT2RT 1 C
-->2.2.2.2 RT2RT 1 P

表1-25 display ospfv3 spf-tree 命令显示信息描述表字段 描述SPF节点，以宣告路由器ID作为标识，其中，Type为节点类型：
• Network：网络节点
• Router：路由器节点
• Flag 为节点标志：
SPFNode • I：节点处于初始化状态
• T：节点在候选列表上
• S：节点在 SPF 树上
• R：该节点与根节点直连
• D：该节点将被删除SPF链路，以宣告路由器ID作为标识，其中，Type为链路类型：
• RT2RT：表示路由器到路由器链路
• NET2RT：表示网络到路由器链路
• RT2NET：表示路由器到网络链路
• Cost 为链路花费，Flag 为链路标志：
• I：链路处于初始化状态SPFLink • P：目的节点是父节点
• C：目的节点是子节点
• D：链路将要被删除
• H：下一跳发生改变
• V：目的节点删除或者是新增节点时，链路的目的节点不在 SPF 树上或处于删除状态
• N：新增链路，并且源节点和目的节点都在 SPF 树上
• L：链路在区域变化列表中\# 显示 OSPFv3 进程 1 下区域 0 的最短路径树详细信息。
<Sysname> display ospfv3 1 area 0 spf-tree verbose OSPFv3 Process 1 with Router ID 1.1.1.1 Flags: S-Node is on SPF tree R-Node is directly reachable I-Node or Link is init D-Node or Link is to be deleted P-Neighbor is parent A-Node is in candidate list C-Neighbor is child H-Nexthop changed N-Link is a new path V-Link is involved Area: 0.0.0.0 Shortest Path Tree >SPFNode[0] AdvID : 1.1.1.1 LsID : 0.0.0.0 NodeType : Router Distance : 1 NodeFlag : S R

Nexthop count: 1
-->NbrID : 1.1.1.1 NbrIntID : 21 Interface : Vlan102 NhFlag : Valid BkInterface: Vlan103 RefCount : 4 Nexthop : FE80::20C:29FF:FED7:F308 BkNexthop : FE80::4 SPFLink count: 1
-->AdvID : 1.1.1.1 LsID : 0.0.0.0 IntID : 232 NbrIntID : 465 NbrID : 2.2.2.2 LinkType : RT2RT LinkCost : 1 LinkNewCost: 1 LinkFlag : C NexthopCnt : 0 ParentLink count: 1
-->AdvID : 1.1.1.1 LsID : 0.0.0.0 IntID : 215 NbrIntID : 466 NbrID : 2.2.2.2 LinkType : RT2RT LinkCost : 1 LinkNewCost: 1 LinkFlag : P NexthopCnt : 0表1-26 display ospfv3 spf-tree verbose 命令显示信息描述表字段 描述SPFNode SPF节点AdvID 通告路由器ID LsID 链路状态ID节点类型NodeType Distance 到根节点的开销NodeFlag 节点标志Nexthop count 下一跳计数邻居路由器ID NbrID NbrIntID 邻居的接口ID Interface 出接口下一跳标志：
NhFlag Valid：有效Invalid：无效BkInterface 备份下一跳出接口下一跳的引用计数RefCount Nexthop 下一跳地址BkNexthop 备份下一跳地址SPFLink count SPF链路计数IntID 接口ID

字段 描述链路类型：
•RT2RT：表示路由器到路由器链路LinkType
• NET2RT：表示网络到路由器链路
• RT2NET：表示路由器到网络链路当前链路花费LinkCost LinkNewCost 新的链路花费链路标志：
• I：链路处于初始化状态
• P：目的节点是父节点
• C：目的节点是子节点
• D：链路将要被删除LinkFlag
• H：下一跳发生改变
• V：目的节点删除或者是新增节点时，链路的目的节点不在 SPF 树上或处于删除状态
• N：新增链路，并且源节点和目的节点都在 SPF 树上
• L：链路在区域变化列表中NexthopCnt 下一跳个数ParentLink count 父链路计数

##### 1.1.24 display ospfv3 statistics

display ospfv3 statistics 命令用来显示 OSPFv3 的统计信息。
【命令】
display ospfv3 [ process-id ] statistics [ error | packet [ interface-type interface-number ] ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPFv3 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有 OSPFv3进程的统计信息。
error：显示错误统计信息。如果未指定本参数，将显示 进程的报文、LSA 和路由的统计OSPFv3信息。
packet：显示 OSPFv3 的报文统计信息。

interface-number：接口类型和编号。显示指定接口的统计信息。如果未interface-type指定本参数，将显示所有接口的统计信息。
【举例】
\# 显示 OSPFv3 的统计信息。
<Sysname> display ospfv3 statistics OSPFv3 Process 1 with Router ID 1.1.1.1 Packet Statistics
---------------------------------------------------------- Type Recv Send Hello 1746 1284 DB Description 505 941 Ls Req 252 136 Ls Upd 851 1553 Ls Ack 416 450 Local Originated LSAs Statistics
---------------------------------------------------------- Type Count Router-LSA 192 Network-LSA 0 Inter-Area-Prefix-LSA 0 Inter-Area-Router-LSA 0 AS-external-LSA 0 NSSA-LSA 0 Link-LSA 10 Intra-Area-Prefix-LSA 112 Grace-LSA 0 Unknown-LSA 0 Total 314 Routes Statistics
---------------------------------------------------------- Type Count Intra Area 0 Inter Area 0 ASE 0 NSSA 0表1-27 display ospfv3 statistics 命令显示信息描述表字段 描述收发报文统计Packet Statistics Hello Hello报文DB Description 数据库描述报文Ls Req 链路状态请求报文

字段 描述Ls Upd 链路状态更新报文Ls Ack 链路状态确认报文生成的LSA统计Local Originated LSAs Statistics Router-LSA Type-1 LSA的数目Network-LSA Type-2 LSA的数目Inter-Area-Prefix-LSA Type-3 LSA的数目LSA的数目Inter-Area-Router-LSA Type-4 AS-external-LSA Type-5 LSA的数目NSSA-LSA Type-7 LSA的数目LSA的数目Link-LSA Type-8 Intra-Area-Prefix-LSA Type-9 LSA的数目Grace-LSA Type-11 LSA的数目Unknown-LSA Unknown-LSA数目总数目Total Routes Statistics 路由计数Intra Area 区域内路由Inter Area 区域间路由ASE 5类外部路由NSSA 7类外部路由显示 进程的错误统计信息。
\# OSPFv3 <sysname> display ospfv3 statistics error OSPFv3 Process 1 with Router ID 1.1.1.1 0 : Transmit error 0 : Neighbor state low 0 : Packet too small 0 : Bad version 0 : Bad checksum 0 : Unknown neighbor 0 : Bad area ID 0 : Bad packet 0 : Packet dest error 0 : Inactive area packet 0 : Router ID confusion 0 : Bad virtual link 0 : HELLO: Hello-time mismatch 0 : HELLO: Dead-time mismatch 0 : HELLO: Ebit option mismatch 0 : DD: Ebit option mismatch 0 : DD: Unknown LSA type 0 : DD: MTU option mismatch 0 : REQ: Empty request 0 : REQ: Bad request 0 : UPD: LSA checksum bad 0 : UPD: Unknown LSA type 0 : UPD: Less recent LSA 0 : UPD: LSA length bad 0 : UPD: LSA AdvRtr id bad 0 : ACK: Bad ack packet

0 : ACK: Invalid ack 0 : Interface down 0 : Multicast incapable 0 : Authentication failure 0 : AuthSeqNumber error表1-28 display ospfv3 statistics error 命令显示信息描述表字段 描述Transmit error 发送出错的OSPFv3报文数Neighbor state low 在低邻居状态收到的OSPFv3报文数Packet too small 报文长度太小的OSPFv3报文数错误版本号的OSPFv3报文数Bad version Bad checksum 校验和出错的OSPFv3报文数Unknown neighbor 未知的邻居发来的OSPFv3报文数Bad area ID 非法的区域ID的OSPFv3报文数非法的 报文数Bad packet OSPFv3 Packet dest error 目的地址错误的OSPFv3报文数Inactive area packet 非活动区域中接收到的报文数含有重复路由器ID的OSPFv3报文数Router ID confusion Bad virtual link 错误的虚链路的OSPFv3报文数HELLO: Hello-time mismatch Hello定时器不匹配的Hello报文数HELLO: Dead-time mismatch Dead定时器不匹配的Hello报文数Option字段E位不匹配的Hello报文数HELLO: Ebit option mismatch DD: Ebit option mismatch Option字段E位不匹配的DD报文数DD: Unknown LSA type DD报文中含有未知类型LSA的数目DD: MTU option mismatch MTU不匹配的DD报文数REQ: Empty request 不含有任何请求信息的LSR报文数REQ: Bad request 请求错误LSA的LSR报文数UPD: LSA checksum bad LSU报文中含有错误校验和LSA的数目LSU报文中含有未知类型LSA的数目UPD: Unknown LSA type UPD: Less recent LSA LSU报文中含有不是最新LSA的数目UPD: LSA length bad LSU报文中含有错误长度LSA的数目UPD: LSA AdvRtr id bad LSU报文中含有错误宣告路由器LSA的数目对LSU报文错误确认的ack报文数ACK: Bad ack packet ACK: Invalid ack LSAck 报文中无效确认 ack 的数目Interface down 接口down计数Multicast incapable 加入组播组出错计数

字段 描述Authentication failure 接收到的报文验证失败AuthSeqNumber error 接收到的报文验证序列号错误\# 显示 OSPFv3 进程和接口的报文统计信息。
<Sysname> display ospfv3 statistics packet OSPFv3 Process 1 with Router ID 1.1.1.1 Hello DD LSR LSU ACK Total Input : 8727 128 28 1584 929 11396 Output: 8757 159 86 987 1513 11502 Area: 0.0.0.0 Area: 0.0.0.1 Interface: Vlan-interface101 DD LSR LSU ACK Total Input : 16 0 45 7 68 Output: 17 1 7 44 69 Interface: Vlan-interface102 DD LSR LSU ACK Total Input : 41 13 720 719 1493 Output: 54 41 750 713 1558表1-29 命令显示信息描述表display ospfv3 statistics packet字段 描述Hello Hello报文DD 数据库描述报文LSR 链路状态请求报文LSU 链路状态更新报文ACK 链路状态确认报文报文总数Total Input 接收报文数Output 发送报文数Area 区域ID接口名称Interface

##### 1.1.25 display ospfv3 vlink

display ospfv3 vlink 命令用来显示 OSPFv3 的虚连接信息。

【命令】
display ospfv3 [ process-id ] vlink【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
process-id：OSPFv3 进程号，取值范围为 1～65535。如果未指定本参数，将显示所有OSPFv3进程的虚连接信息。
【举例】
\# 显示 OSPFv3 的虚连接信息。
<Sysname> display ospfv3 vlink OSPFv3 Process 1 with Router ID 1.1.1.1 Virtual-link Neighbor-ID: 12.2.2.2, Neighbor-state: Full Interface: 2348 (Vlan-interface12), Instance-ID: 0 Local IPv6 address: 3:3333::12 Remote IPv6 address: 2:2222::12 Cost: 1 State: P-2-P Type: Virtual Transit area: 0.0.0.1 Timers: Hello 10, Dead 40, Retransmit 5, Transmit delay 1 IPsec profile name: profile001 Keychain authentication: Enabled (test), inherited表1-30 命令显示信息描述表display ospfv3 vlink字段 描述Virtual-link Neighbor-ID 通过虚连接相连的邻居路由器的Router ID邻居状态，包括Down、Init、2-Way、ExStart、Exchange、Loading和Full Neighbor-state Interface 此虚连接的本端接口的端口号和名称Instance-ID 实例ID Local IPv6 address 本地IPv6地址Remote IPv6 address 对端IPv6地址Cost 接口的路由开销State 接口状态类型：虚连接Type Transit area 传输区域ID（如果当前接口为虚连接，则显示）

字段 描述OSPFv3定时器，分别定义如下：
•Hello：表示接口发送 Hello 报文的时间间隔，单位为秒Timers
• Dead：表示邻居的失效时间，单位为秒
• Retransmit：表示接口重传 LSA 时间间隔，单位为秒接口对LSA的传输延迟时间，单位为秒Transmit delay IPsec profile name IPsec安全框架名Keychain authentication:
OSPFv3虚连接采用keychain验证模式，keychain名称为test，inherited表示Enabled (test), inherited虚连接继承的是骨干区域下配置的keychain验证模式

##### 1.1.26 enable ipsec-profile

命令用来在 OSPFv3 区域应用 IPsec 安全框架。
enable ipsec-profile undo enable ipsec-profile 命令用来取消在 OSPFv3 区域应用的 IPsec 安全框架。
【命令】
enable ipsec-profile profile-name undo enable ipsec-profile【缺省情况】
区域没有应用 安全框架。
OSPFv3 IPsec【视图】
OSPFv3 区域视图【缺省用户角色】
network-admin【参数】
profile-name：IPsec 安全框架名称，为 1～63 个字符的字符串，不区分大小写。
【使用指导】
本命令应结合 IPsec安全框架使用，IPsec安全框架的具体情况请参见“安全配置指导”中的“IPsec”。
【举例】
\# 配置 OSPFv3 进程 1 区域 0 的安全框架为 profile001。
<Sysname> system-view [Sysname] ospfv3 1 [Sysname-ospfv3-1] area 0 [Sysname-ospfv3-1-area-0.0.0.0] enable ipsec-profile profile001

##### 1.1.27 event-log

命令用来配置保存 OSPFv3 的日志信息的最大个数。
event-log

命令用来取消保存 OSPFv3 的日志信息的最大个数的配置。
undo event-log【命令】
event-log { lsa-flush | peer | spf } size count undo event-log { lsa-flush | peer | spf } size【缺省情况】
保存的路由计算、邻居和 LSA 老化的日志信息个数均为 10 个。
【视图】
OSPFv3 视图【缺省用户角色】
network-admin【参数】
lsa-flush：LSA 老化日志信息个数。
peer：邻居日志信息个数。
spf：SPF 日志信息个数。
count：日志信息个数，取值范围为 0～65535。
【举例】
配置保存 进程 的路由计算日志信息的最大个数为 50。
\# OSPFv3 100 <Sysname> system-view [Sysname] ospfv3 100 [Sysname-ospfv3-100] event-log spf size 50

##### 1.1.28 fast-reroute (OSPFv3 view)

命令用来配置 快速重路由功能。
fast-reroute OSPFv3命令用来关闭 OSPFv3 快速重路由功能。
undo fast-reroute【命令】
fast-reroute { lfa [ abr-only ] | route-policy route-policy-name } undo fast-reroute【缺省情况】
OSPFv3 快速重路由功能处于关闭状态。
【视图】
OSPFv3 视图【缺省用户角色】
network-admin【参数】
lfa：为所有路由通过 LFA（Loop Alternate）算法选取备份下一跳信息。
Free abr-only：仅选取到 设备的路由作为备份下一跳。
ABR

： 为 通 过 策 略 的 路 由 指 定 备 份 下 一 跳 ，route-policy route-policy-name为路由策略名，为 1～63 个字符的字符串，区分大小写。
route-policy-name【使用指导】
OSPFv3 快速重路由功能（通过 LFA 算法选取备份下一跳信息）使能后，不能配置 vlink-peer命令。
【举例】
\# 使能 OSPFv3 进程 1 的快速重路由功能，为所有路由通过 LFA 算法选取备份下一跳信息。
<Sysname> system-view [Sysname] ospfv3 1 [Sysname-ospfv3-1] fast-reroute lfa

##### 1.1.29 filter (OSPFv3 area view)

命令用来配置对 Inter-Area-Prefix-LSA 进行过滤。
filter命令用来取消对 Inter-Area-Prefix-LSA 进行过滤。
undo filter【命令】
filter { ipv6-acl-number | prefix-list prefix-list-name | route-policy route-policy-name } { export | import } undo filter { export | import }【缺省情况】
不对 Inter-Area-Prefix-LSA 进行过滤。
【视图】
OSPFv3 区域视图【缺省用户角色】
network-admin【参数】
ipv6-acl-number：指定的基本或高级 编号，对进出本区域的IPv6 ACL Inter-Area-Prefix-LSA进行过滤，取值范围为 2000～3999。
prefix-list-name：指定的 IPv6 地址前缀列表，对进出本区域的 Inter-Area-Prefix-LSA 进行过滤，为 1～63 个字符的字符串，区分大小写。
route-policy-name：指定的路由策略，对进出本区域的 Inter-Area-Prefix-LSA 进行过滤，为 1～63 个字符的字符串，区分大小写。
export：对 ABR 向其它区域发布的 Inter-Area-Prefix-LSA 进行过滤。
import：对 ABR 向本区域发布的 Inter-Area-Prefix-LSA 进行过滤。
【使用指导】
此命令只在 路由器上有效，对区域内部路由器无效。
ABR

【举例】
\# 根据 IPv6 地址前缀列表 my-prefix-list 和编号为 2000 的 IPv6 基本 ACL 分别对进出 OSPFv3 区域1 的 Inter-Area-Prefix-LSA 进行过滤。
<Sysname> system-view [Sysname] ospfv3 1 [Sysname-ospfv3-1] area 1 [Sysname-ospfv3-1-area-0.0.0.1] filter prefix-list my-prefix-list import [Sysname-ospfv3-1-area-0.0.0.1] filter 2000 export

##### 1.1.30 filter-policy export (OSPFv3 view)

命令用来配置对引入的路由信息进行过滤。
filter-policy export命令用来取消对引入的路由信息进行过滤。
undo filter-policy export【命令】
filter-policy { ipv6-acl-number | prefix-list prefix-list-name } export [ bgp4+ | direct | { isisv6 | ospfv3 | ripng } [ process-id ] | static ] undo filter-policy export [ bgp4+ | direct | { isisv6 | ospfv3 | ripng } [ process-id ] | static ]【缺省情况】
不对引入的路由信息进行过滤。
【视图】
视图OSPFv3【缺省用户角色】
network-admin【参数】
ipv6-acl-number：用于过滤路由信息目的地址的基本或高级 IPv6 ACL 编号，取值范围为 2000～3999。
prefix-list-name：用于过滤路由信息目的地址的 IPv6 地址前缀列表的名称，为 1～63 个字符的字符串，区分大小写。
bgp4+：对引入的 路由进行过滤。
IPv6 BGP direct：对引入的直连路由进行过滤。
isisv6：对引入的 路由进行过滤。
IPv6 IS-IS ospfv3：对引入的 路由进行过滤。
OSPFv3 ripng：对引入的 RIP 路由进行过滤。
process-id：路由协议进程号，取值范围为 1～65535，缺省值为 1。
static：对引入的静态路由进行过滤。
【使用指导】
当配置的是高级 ACL（3000～3999）时，其使用规则如下：

使用命令
• rule [ rule-id ] { deny | permit } ipv6 source sour-addr来过滤指定目的地址的路由。
sour-prefix使用命令
• rule [ rule-id ] { deny | permit } ipv6 source sour-addr sour-prefix destination dest-addr dest-prefix 来过滤指定目的地址和掩码的路由。
其中，source 用来过滤路由目的地址，destination 用来过滤路由前缀，配置的前缀应该是连续的（当配置的前缀不连续时该过滤前缀的条件不生效）。
命令只对本设备使用 引入的路由起作用。如果没有配filter-policy export import-route置import-route 命令来引入其它外部路由（包括不同进程的OSPFv3路由），则filter-policy export 命令无效。
如果没有指定路由协议，将对引入的任何一个协议产生的路由都要进行过滤。
【举例】
\# 根据 IPv6 地址前缀列表 abc 对引入的路由信息进行过滤。
<Sysname> system-view [Sysname] ipv6 prefix-list abc permit 2002:1:: 64 [Sysname] ospfv3 [Sysname-ospfv3-1] filter-policy prefix-list abc export \# 使用编号为 3000 的 IPv6 高级 ACL 对引入的路由进行过滤，只允许 2001::1/128 通过。
<Sysname> system-view [Sysname] acl ipv6 advanced 3000 [Sysname-acl-ipv6-adv-3000] rule 10 permit ipv6 source 2001::1 128 destination ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff 128 [Sysname-acl-ipv6-adv-3000] rule 100 deny ipv6 [Sysname-acl-ipv6-adv-3000] quit [Sysname] ospfv3 [Sysname-ospfv3-1] filter-policy 3000 export

##### 1.1.31 filter-policy import (OSPFv3 view)

命令用来过滤通过接收到的 LSA 计算出来的路由信息。
filter-policy import命令用来恢复缺省情况。
undo filter-policy import【命令】
filter-policy { ipv6-acl-number [ gateway prefix-list-name ] | prefix-list prefix-list-name [ gateway prefix-list-name ] | gateway prefix-list-name | route-policy route-policy-name } import undo filter-policy import【缺省情况】
不对通过接收到的 LSA 计算出来的路由信息进行过滤。
【视图】
视图OSPFv3

【缺省用户角色】
network-admin【参数】
ipv6-acl-number：用于过滤路由信息目的地址的基本或高级 IPv6 ACL 编号，取值范围为 2000～3999。
prefix-list-name：指定的 地址前缀列表，基于要加入到路由表的路由信息的gateway IPv6下一跳进行过滤。prefix-list-name 为 1～63 个字符的字符串，区分大小写。如果未指定本参数，则不会基于要加入到路由表的路由信息的下一跳进行过滤。
prefix-list prefix-list-name：指定的地址前缀列表，基于目的地址对接收的路由信息进行过滤。prefix-list-name 为 1～63 个字符的字符串，区分大小写。
route-policy-name：指定路由策略名，基于路由策略对接收的路由信息进行route-policy过滤。route-policy-name 为 1～63 个字符的字符串，区分大小写。
【使用指导】
当配置的是高级 ACL（3000～3999）或者指定的路由策略中配置的是高级 ACL 时，其使用规则如下：
• 使用命令 rule [ rule-id ] { deny | permit } ip source sour-addr sour-prefix来过滤指定目的地址的路由。
• 使用命令rule [ rule-id ] { deny | permit } ip source sour-addr sour-prefix来过滤指定目的地址和前缀的路由。
destination dest-addr dest-prefix其中，source 用来过滤路由目的地址，destination 用来过滤路由前缀，配置的前缀应该是连续的（当配置的前缀不连续时该过滤前缀的条件不生效）。
命令只对 计算出来的路由进行过滤，没有通过过滤的路由将filter-policy import OSPFv3不被加入路由表中，从而不能指导报文转发。
【举例】
\# 根据 IPv6 地址前缀列表 abc 对接收的路由信息进行过滤。
<Sysname> system-view [Sysname] ipv6 prefix-list abc permit 2002:1:: 64 [Sysname] ospfv3 [Sysname-ospfv3-1] filter-policy prefix-list abc import \# 使用编号为 3000 的 IPv6 高级 ACL 对接收的路由进行过滤，只允许 2001::1/128 通过。
<Sysname> system-view [Sysname] acl ipv6 advanced 3000 [Sysname-acl-ipv6-adv-3000] rule 10 permit ipv6 source 2001::1 128 destination ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff 128 [Sysname-acl-ipv6-adv-3000] rule 100 deny ipv6 [Sysname-acl-ipv6-adv-3000] quit [Sysname] ospfv3 [Sysname-ospfv3-1] filter-policy 3000 import

##### 1.1.32 graceful-restart enable

命令用来使能 OSPFv3 协议的 GR 能力。
graceful-restart enable

命令用来关闭 OSPFv3 协议的 GR 能力。
undo graceful-restart enable【命令】
graceful-restart enable [ global | planned-only ] * undo graceful-restart enable【缺省情况】
OSPFv3 的 GR 能力处于关闭状态。
【视图】
OSPFv3 视图【缺省用户角色】
network-admin【参数】
global：全局 GR，必须保证所有的 都存在，整个 才会完成，如果有一个GR Helper GR GR Helper失效（比如，接口 down），则整个 GR 失败。如果未指定本参数，表示支持接口级 GR，即只要有一个 GR Helper 存在，则整个 GR 会完成。
planned-only：表示只支持计划重启。如果未指定本参数，表示计划重启和非计划重启都支持。
【使用指导】
GR 包括计划重启和非计划重启：
• 计划重启指的是手动通过命令执行重启或主备倒换，在进行重启或主备倒换前 GR Restarter会先发送 Grace-LSA。
非计划 指的是由于设备故障等原因进行重启或主备倒换，在进行重启或主备倒换前
• GR GR Restarter 不会事先发送 Grace-LSA。
和 命令互斥，不能同时配置。
graceful-restart enable non-stop-routing支持 的 能力的设备主备倒换后，为了实现设备转发业务的不中断，它必须OSPFv3 GR Restarter完成下列两项任务：
• 重启过程 GR Restarter 转发表项保持稳定；
• 重启流程结束后重建所有邻居关系，重新获取完整的网络拓扑信息。
【举例】
\# 使能 OSPFv3 进程 1 的 GR 能力。
<Sysname> system-view [Sysname] ospfv3 1 [Sysname-ospfv3-1] graceful-restart enable【相关命令】
•graceful-restart helper enable

##### 1.1.33 graceful-restart helper enable

命令用来使能 OSPFv3 的 GR Helper 能力。
graceful-restart helper enable undo graceful-restart helper enable 命令用来关闭 OSPFv3 的 GR Helper 能力。

【命令】
graceful-restart helper enable [ planned-only ] undo graceful-restart helper enable【缺省情况】
OSPFv3 的 GR Helper 能力处于开启状态。
【视图】
OSPFv3 视图【缺省用户角色】
network-admin【参数】
planned-only：表示只支持计划重启。如果未指定本参数，表示计划重启和非计划重启（即异常重启）都支持。
【使用指导】
收到 Grace-LSA 后，如果支持 GR Helper 能力则进入 Helper 模式（此时该邻居称为 GR Helper）。
在 GR Restarter 重新建立邻居的时候，GR Helper 帮助 GR Restarter 进行 LSDB 的同步。
【举例】
\# 使能 OSPFv3 进程 1 的 GR Helper 能力。
<Sysname> system-view [Sysname] ospfv3 1 [Sysname-ospfv3-1] graceful-restart helper enable【相关命令】
• graceful-restart enable

##### 1.1.34 graceful-restart helper strict-lsa-checking

graceful-restart helper strict-lsa-checking 命令用来使能 GR Helper 严格 LSA 检查能力。
命令用来关闭 GR Helper 严格undo graceful-restart helper strict-lsa-checking检查能力。
LSA【命令】
graceful-restart helper strict-lsa-checking undo graceful-restart helper strict-lsa-checking【缺省情况】
GR Helper 严格 LSA 检查能力处于关闭状态。
【视图】
OSPFv3 视图【缺省用户角色】
network-admin

【使用指导】
使能 GR Helper 严格 LSA 检查能力，当检查到 GR Helper 设备的 LSA 发生变化时候，Helper 设备退出 GR Helper 模式。
【举例】
使能 进程 的 严格 检查能力。
\# OSPFv3 1 GR Helper LSA <Sysname> system-view [Sysname] ospfv3 1 [Sysname-ospfv3-1] graceful-restart helper strict-lsa-checking【相关命令】
• graceful-restart helper enable

##### 1.1.35 graceful-restart interval

命令用来配置 协议的 重启间隔时间。
graceful-restart interval OSPFv3 GR命令用来恢复缺省情况。
undo graceful-restart interval【命令】
graceful-restart interval interval undo graceful-restart interval【缺省情况】
OSPFv3 协议的 GR 重启间隔时间为 120 秒。
【视图】
OSPFv3 视图【缺省用户角色】
network-admin【参数】
interval：指定 OSPFv3 协议的 GR 重启间隔时间（期望重启时间），取值范围为 40～1800，单位为秒。
【使用指导】
配置此命令的用户需要确保配置的 GR 重启间隔不小于 OSPFv3 所有接口的邻居失效时间的最大值，否则可能造成 重启失败。
GR【举例】
\# 配置 OSPFv3 进程 1 的 GR 重启间隔时间为 100 秒。
<Sysname> system-view [Sysname] ospfv3 1 [Sysname-ospfv3-1] graceful-restart interval 100【相关命令】
• ospfv3 timer dead

##### 1.1.36 import-route (OSPFv3 view)

import-route 命令用来配置引入外部路由信息。
undo import-route 命令用来取消引入外部路由信息。
【命令】
import-route bgp4+ [ as-number ] [ allow-ibgp ] [ [ cost cost-value | inherit-cost ] | nssa-only | route-policy route-policy-name | tag tag | type type ] * import-route { direct | static } [ [ cost cost-value | inherit-cost ] | nssa-only | route-policy route-policy-name | tag tag | type type ] * import-route { isisv6 | ospfv3 | ripng } [ process-id | all-processes ] [ allow-direct | [ cost cost-value | inherit-cost ] | nssa-only | route-policy route-policy-name | tag tag | type type ] * undo import-route { bgp4+ | direct | { isisv6 | ospfv3 | ripng } [ process-id | all-processes ] | static }【缺省情况】
不引入外部路由信息。
【视图】
OSPFv3 视图【缺省用户角色】
network-admin【参数】
bgp4+：引入 协议的路由。
IPv6 BGP direct：引入直连路由。
static：引入静态路由。
isisv6：引入 协议的路由。
IPv6 IS-IS ospfv3：引入 OSPFv3 协议的路由。
ripng：引入 RIPng 协议的路由。
as-number：引入指定 AS 内的路由。as-number 为 AS 号，取值范围为 1～4294967295。如果没有指定本参数，则引入所有的 路由。建议配置时指定 号，否则引入的IPv6 EBGP AS IPv6 EBGP路由数量过多时，会引发设备内存资源紧张等问题。
process-id：路由协议进程号，取值范围为 1～65535，缺省值为 1。
all-processes：引入指定路由协议所有进程的路由。
allow-ibgp ： 允 许 引 入 IBGP 路 由 。 import-route bgp4+ 表 示 只 引 入 EBGP 路 由 ；
import-route bgp4+ allow-ibgp 表示将 IBGP 路由也引入，容易引起路由环路，请慎用。
allow-direct：在引入的路由中包含使能了该协议的接口网段路由。如果未指定本参数，在引入协议路由时不会包含使能了该协议的接口网段路由。当 与allow-direct route-policy参数一起使用时，需要注意路由策略中配置的匹配规则不要与接口路由信route-policy-name息存在冲突，否则会导致 allow-direct 配置失效。例如，当配置 allow-direct 参数引入

OSPFv3直连时，在路由策略中不要配置if-match 匹配条件，否则，allow-direct route-type参数失效。
cost-value：路由开销值，取值范围为 0～16777214。
cost inherit-cost：指定引入外部路由时使用路由的原有开销值。
nssa-only：设置 的 比特位不置位，即在对端路由器上不能转为 LSA。如Type-7 LSA P Type-5果未指定本参数，Type-7 LSA 的 P 比特位被置位，即在对端路由器上可以转为 Type-5 LSA（如果本地路由器是 ABR，则会检查骨干区域是否存在 FULL 状态的邻居，当 FULL 状态的邻居存在时，产生的 Type-7 LSA 中 P 比特位不置位）。
： 配 置 只 能 引 入 符 合 指 定 路 由 策 略 的 路 由 。
route-policy route-policy-name为路由策略名称，为 1～63 个字符的字符串，区分大小写。
route-policy-name tag：外部 中的标记，取值范围为 0～4294967295。如果未指定本参数，将根据tag LSA default tag 命令的配置进行取值。
type type：度量值类型，取值范围为 1～2，缺省值为 2。
【使用指导】
外部路由是指到达自治系统外部的路由，有两类：
• 第一类外部路由（Type1 External）：这类路由的可信程度较高，并且和 OSPFv3 自身路由的开销具有可比性，所以到第一类外部路由的开销等于本路由器到相应的 ASBR 的开销与 ASBR到该路由目的地址的开销之和。
第二类外部路由（Type2 External）：这类路由的可信度比较低，所以OSPFv3协议认为从ASBR
•到自治系统之外的开销远远大于在自治系统之内到达 ASBR 的开销。所以计算路由开销时将主要考虑前者，即到第二类外部路由的开销等于 ASBR 到该路由目的地址的开销。如果计算出开销值相等的两条路由，再考虑本路由器到相应的 ASBR 的开销。
该命令不能引入缺省路由。
如果未指定 和 参数，则引入的外部路由的开销值为 1。
cost inherit-cost命令配置后，引入的路由只在 NSSA 区域产生 Type-7 LSA，不会在import-route nssa-only非 区域产生 LSA。
NSSA Type-5【举例】
\# 指定引入进程号为 10 的 RIPng 路由为第二类路由，路由开销值为 50。
<Sysname> system-view [Sysname] ospfv3 [Sysname-ospfv3-1] import-route ripng 10 type 2 cost 50进程 引入 进程 发现的路由。
\# OSPFv3 100 OSPFv3 160 <Sysname> system-view [Sysname] ospfv3 100 [Sysname-ospfv3-100] import-route ospfv3 160【相关命令】
• default-route-advertise (OSPFv3 view)

##### 1.1.37 log-peer-change

log-peer-change 命令用来打开邻居状态变化的输出开关。

命令用来关闭邻居状态变化的输出开关。
undo log-peer-change【命令】
log-peer-change undo log-peer-change【缺省情况】
邻居状态变化的输出开关处于打开状态。
【视图】
OSPFv3 视图【缺省用户角色】
network-admin【使用指导】
打开邻居状态输出开关后，OSPFv3 邻居状态变化时会生成日志信息发送到设备的信息中心，通过设置信息中心的参数，最终决定日志信息的输出规则（即是否允许输出以及输出方向）。（有关信息中心参数的配置请参见“网络管理和监控配置指导”中的“信息中心”。）
【举例】
\# 关闭 OSPFv3 进程 100 的邻居状态变化的输出开关。
<Sysname> system-view [Sysname] ospfv3 100 [Sysname-ospfv3-100] undo log-peer-change

##### 1.1.38 lsa-generation-interval

命令用来配置 OSPFv3 LSA 重新生成的时间间隔。
lsa-generation-interval命令用来恢复缺省情况。
undo lsa-generation-interval【命令】
lsa-generation-interval maximum-interval [ minimum-interval [ incremental-interval ] ] undo lsa-generation-interval【缺省情况】
OSPFv3 LSA 重新生成的最大时间间隔为 5 秒，最小时间间隔为 0 毫秒，时间间隔惩罚增量为 0 毫秒。
【视图】
OSPFv3 视图【缺省用户角色】
network-admin【参数】
maximum-interval：OSPFv3 LSA 重新生成的最大时间间隔，取值范围为 1～60，单位为秒。

minimum-interval：OSPFv3 LSA 重新生成的最小时间间隔，取值范围为 10～60000，单位为毫秒。取值为 毫秒时表示不对 重新生成的最小时间间隔进行限制。
0 OSPFv3 LSA incremental-interval：OSPFv3 重新生成的时间间隔惩罚增量，取值范围为 10～60000，LSA单位为毫秒。
【使用指导】
通过调节 LSA 重新生成的时间间隔，可以抑制网络频繁变化可能导致的带宽资源和路由器资源被过多占用的问题。在网络变化不频繁的情况下，将 LSA重新生成时间间隔缩小到 minimum-interval，而在网络变化频繁的情况下可以进行相应惩罚，将等待时间按照配置的惩罚增量延长，最大不超过maximum-interval。
minimum-interval 和 incremental-interval 配置值不允许大于 maximum-interval 配置值。
【举例】
设置 重新生成的最大时间间隔为 秒，最小时间间隔为 毫秒，惩罚增量为 毫秒。
\# LSA 2 100 100 <Sysname> system-view [Sysname] ospfv3 100 [Sysname-ospfv3-100] lsa-generation-interval 2 100 100【相关命令】
• lsa-arrival-interval

##### 1.1.39 maximum load-balancing (OSPFv3 view)

命令用来配置 支持的等价路由的最大条数。
maximum load-balancing OSPFv3命令用来恢复缺省情况。
undo maximum load-balancing【命令】
maximum load-balancing number undo maximum load-balancing【缺省情况】
OSPFv3 支持的等价路由的最大条数与系统支持最大等价路由的条数相同。
【视图】
OSPFv3 视图【缺省用户角色】
network-admin【参数】
number：等价路由的最大条数，当 取值为 时，相当于不进行负载分担。
number 1【使用指导】
本命令中 number 参数的取值范围和 max-ecmp-num 命令相关。通过 max-ecmp-num 命令配置系统支持的最大等价路由条数为 m，并重启设备后，number 参数的取值范围将修改为 1～m。

【举例】
\# 配置 OSPFv3 支持的等价路由的最大条数为 2。
<Sysname> system-view [Sysname] ospfv3 100 [Sysname-ospfv3-100] maximum load-balancing 2【相关命令】
• max-ecmp-num（三层技术-IP 路由命令参考/IP 路由基础）

##### 1.1.40 non-stop-routing

non-stop-routing 命令用来使能 OSPFv3 协议的 NSR 能力。
undo non-stop-routing 命令用来关闭 OSPFv3 协议的 NSR 能力。
【命令】
non-stop-routing undo non-stop-routing【缺省情况】
的 能力处于关闭状态。
OSPFv3 NSR【视图】
OSPFv3 视图【缺省用户角色】
network-admin【使用指导】
各个进程的 NSR 功能是相互独立的，只对本进程生效。如果存在多个 OSPFv3 进程，建议在各个进程下使能 功能。
OSPFv3 NSR和 命令互斥，不能同时配置。
non-stop-routing graceful-restart enable【举例】
使能 进程 的 能力。
\# OSPFv3 100 NSR <Sysname> system-view [Sysname] ospfv3 100 [Sysname-ospfv3-100] non-stop-routing

##### 1.1.41 nssa (OSPFv3 area view)

命令用来配置一个区域为 区域。
nssa NSSA命令用来恢复缺省情况。
undo nssa【命令】
nssa [ default-route-advertise [ cost cost-value | nssa-only | route-policy route-policy-name | tag tag | type type ] * | no-import-route | no-summary | [ translate-always | translate-never ] | suppress-fa | translator-stability-interval value ] *

undo nssa【缺省情况】
没有区域被配置为 区域。
NSSA【视图】
OSPFv3 区域视图【缺省用户角色】
network-admin【参数】
default-route-advertise：该参数只用于 NSSA 区域的 ABR 或 ASBR，配置后，对于 ABR，不论本地是否存在缺省路由，都将生成一条 向区域内发布缺省路由；对于 ASBR，只Type-7 LSA有当本地存在缺省路由时，才产生 Type-7 LSA 向区域内发布缺省路由。
cost cost-value：该缺省路由的度量值，取值范围为 0～16777214。如果未指定本参数，缺省路由的度量值将取 default-cost 命令配置的值。
nssa-only：设置 Type-7 LSA 的 P 比特位不置位，即在对端路由器上不能转为 Type-5 LSA，对端路由器不能引入 Type-7 LSA 产生的外部路由。如果未指定本参数，Type-7 LSA 的 P 比特位被置位，即在对端路由器上可以转为 LSA，对端路由器可以引入 产生的外部路由（如Type-5 Type-7 LSA果本地路由器是 ABR，则会检查骨干区域是否存在 FULL 状态的邻居，当 FULL 状态的邻居存在时，产生的 Type-7 LSA 中 P 比特位不置位）。
route-policy-name：路由策略名，为 1～63 个字符的字符串，区分大小写。
route-policy只有 指定的路由策略匹配时，才可以产生一个描述缺省路由的route-policy-name Type-7 LSA发布出去，指定的路由策略会影响 Type-7 LSA 中的属性。
tag：缺省路由的标识，取值范围为 0～4294967295。
tag type：该 的类型，取值范围为 1～2，缺省类型为 2。
type NSSA LSA no-import-route：该参数用于禁止将 外部路由以 的形式引入到 区域中，AS Type-7 LSA NSSA这个参数通常只用在既是 NSSA 区域的 ABR，也是 OSPFv3 自治系统的 ASBR 的路由器上，以保证所有外部路由信息能正确地进入 OSPFv3 路由域。
no-summary：该参数只用于 NSSA 区域的 ABR，配置后，NSSA ABR 只通过 Type-3 LSA 向区域内发布一条缺省路由，不再向区域内发布任何其它 Type-3 LSA（这种区域又称为 Totally NSSA 区域）。
translate-always：指定 为 区域的 转换为 的转换路由器。
ABR NSSA Type-7 LSA Type-5 LSA translate-never：指定 不能将 区域的 转换为 LSA。
ABR NSSA Type-7 LSA Type-5 suppress-fa：指定当 转换为 时，生成的 不携带Type-7 LSA Type-5 LSA Type-5 LSA Forwarding Address。
translator-stability-interval value：当有新的设备成为 NSSA 区域的 Type-7 LSA 转换为 Type-5 LSA 的转换路由器后，原 Type-7 LSA 转换为 Type-5 LSA 的转换路由器保持转换能力的时间。 为保持时间，取值范围为 0 ～ 900 ，单位为秒，缺省值为 0 ，即不保持。
value【使用指导】
如果要将一个区域配置成 区域，则该区域中的所有路由器都必须配置本命令。
NSSA

【举例】
\# 将区域 1 配置成 NSSA 区域。
<Sysname> system-view [Sysname] ospfv3 120 [Sysname-ospfv3-120] area 1 [Sysname-ospfv3-120-area-0.0.0.1] nssa【相关命令】
• default-cost (OSPFv3 area view)

##### 1.1.42 ospfv3

ospfv3 命令用来启动 OSPFv3 进程，并进入 OSPFv3 视图。
undo ospfv3 命令用来关闭指定的 OSPFv3 进程。
【命令】
ospfv3 [ process-id | vpn-instance vpn-instance-name ] * undo ospfv3 [ process-id ]【缺省情况】
系统没有运行 OSPFv3 进程。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
process-id：OSPFv3 进程号，取值范围为 1～65535，缺省值为 1。
vpn-instance vpn-instance-name ： 指 定 OSPFv3 进 程 所 属 的 VPN 实 例 。
vpn-instance-name 表示 MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。如果未指定本参数，则表示 OSPFv3 位于公网中。
【使用指导】
只有在 视图下配置了 ID，OSPFv3 进程才能正常运行，否则只能看到该进程，但OSPFv3 Router无法生成 LSA。
【举例】
\# 启动进程号为 120 的 OSPFv3 进程并配置路由器的 Router ID 为 1.1.1.1。
<Sysname> system-view [Sysname] ospfv3 120 [Sysname-ospfv3-120] router-id 1.1.1.1【相关命令】
•router-id

##### 1.1.43 ospfv3 area

ospfv3 area 命令用来在接口上使能 OSPFv3 功能，并指定其所属区域。
undo ospfv3 area 命令用来在指定接口上关闭 OSPFv3 功能。
【命令】
ospfv3 process-id area area-id [ instance instance-id ] undo ospfv3 process-id area area-id [ instance instance-id ]【缺省情况】
接口上的 OSPFv3 功能处于关闭状态。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
process-id：OSPFv3 进程号，取值范围为 1～65535。
area-id：区域的标识，可以是十进制整数（取值范围为 0～4294967295，系统会将其处理成 IPv4地址格式）或 IPv4 地址格式。
instance-id：接口所属的实例 ID，取值范围为 0～255，缺省值为 0。
【举例】
在接口 上启动 实例 的运行，并使能到 中。
\# Vlan-interface10 OSPFv3 1 Area 1 <Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospfv3 1 area 1 instance 1

##### 1.1.44 ospfv3 authentication-mode

命令用来设置接口上的 OSPFv3 报文的验证模式。
ospfv3 authentication-mode命令用来取消接口上的 OSPFv3 报文的验证模式的配置。
undo ospfv3 authentication-mode【命令】
ospfv3 authentication-mode keychain keychain-name [ instance instance-id ] undo ospfv3 authentication-mode [ instance instance-id ]【缺省情况】
接口不对 OSPFv3 报文进行验证。
【视图】
接口视图【缺省用户角色】
network-admin

【参数】
keychain：使用 keychain 验证模式。
keychain-name：keychain 名称，为 1～63 个字符的字符串，区分大小写。
instance instance-id：接口所属的实例 ID，取值范围为 0～255，缺省值为 0。
【使用指导】
在使能了 OSPFv3 的接口上使用 keychain 验证模式时，报文的收、发过程如下：
OSPFv3 在发送报文前，会先从 keychain 获取当前的有效发送 key，根据该 key 的标识符、认证算法和认证密钥进行报文验证。如果当前不存在有效发送 key，或者该 key 的标识符大于 65535，不会发送报文。
OSPFv3在收到报文后，会根据报文携带的 的标识符从 中获取有效接收 key，
• OSPFv3 key keychain根据该 key 的认证算法和认证密钥对报文进行校验。如果报文校验失败，或者根据报文中携带的 key 的标识符无法从 keychain 中获取到有效接收 key，则该报文将被丢弃。
对于 keychain 认证算法和 key 的标识符的范围，OSPFv3 的支持情况如下：
• OSPFv3 仅支持 HMAC-SHA-256 认证算法。
• OSPFv3 仅支持标识符取值范围为 0～65535 的 key。
【举例】
\# 配置接口 Ten-GigabitEthernet1/0/1 上 OSPFv3 使用 keychain 验证模式，keychain 名为 test。
<Sysname> system-view [Sysname] interface ten-gigabitethernet 1/0/1 [Sysname-Ten-GigabitEthernet1/0/1] ospfv3 authentication-mode keychain test

##### 1.1.45 ospfv3 bfd enable

命令用来在运行 OSPFv3 的接口下使能 BFD 功能。
ospfv3 bfd enable undo ospfv3 bfd enable 命令用来在运行 OSPFv3 的接口下关闭 BFD 功能。
【命令】
ospfv3 bfd enable [ instance instance-id ] undo ospfv3 bfd enable [ instance instance-id ]【缺省情况】
运行 的接口的 功能处于关闭状态。
OSPFv3 BFD【视图】
接口视图【缺省用户角色】
network-admin【参数】
instance-id：接口所属的实例 ID，取值范围为 0～255，缺省值为 0。

【使用指导】
BFD（Bidirectional Forwarding Detection，双向转发检测）能够为 OSPFv3 邻居之间的链路提供快速检测功能。当邻居之间的链路出现故障时，加快 OSPFv3 协议的收敛速度。
OSPFv3 通过 BFD 控制报文实现 BFD 功能。
【举例】
使能接口 的 实例 的 功能。
\# Vlan-interface11 OSPFv3 1 BFD <Sysname> system-view [Sysname] interface vlan-interface 11 [Sysname-Vlan-interface11] ospfv3 bfd enable instance 1

##### 1.1.46 ospfv3 cost

命令用来配置运行不同 OSPFv3 实例的接口的开销值。
ospfv3 cost命令用来取消运行不同 OSPFv3 实例的接口的开销值的配置。
undo ospfv3 cost【命令】
cost-value ospfv3 cost [ instance instance-id ] undo ospfv3 cost [ instance instance-id ]【缺省情况】
路由器接口按照带宽自动计算运行 OSPFv3 协议所需的开销；对于 VLAN 接口，缺省值为 1；对于Loopback 接口，缺省值为 0。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
cost-value：接口运行 OSPFv3 协议的路由开销，Loopback 接口的取值范围为 0～65535，其他接口的取值范围为 1～65535。
instance-id：接口所属的实例 ID，取值范围为 0～255，缺省值为 0。
【举例】
\# 指定运行 OSPFv3 实例 1 的接口 Vlan-interface10 的开销为 33。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospfv3 cost 33 instance 1

##### 1.1.47 ospfv3 dr-priority

ospfv3 dr-priority 命令用来配置运行不同 OSPFv3 实例的接口的 DR 优先级。
undo ospfv3 dr-priority 命令用来取消运行不同 OSPFv3 实例的接口的 DR 优先级的配置。
【命令】
ospfv3 dr-priority priority [ instance instance-id ]

undo ospfv3 dr-priority [ instance instance-id ]【缺省情况】
接口的 优先级为 1。
DR【视图】
接口视图【缺省用户角色】
network-admin【参数】
priority：接口的 DR 优先级，取值范围为 0～255。
instance-id：接口所属的实例 ID，取值范围为 0～255，缺省值为 0。
instance【使用指导】
接口的 优先级决定了该接口在选举 时所具有的资格，优先级高的在选举时被首先考虑。
DR DR/BDR【举例】
\# 设置运行 OSPFv3 实例 1 的接口 Vlan-interface10 在选举 DR/BDR 时的优先级为 8。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospfv3 dr-priority 8 instance 1

##### 1.1.48 ospfv3 fast-reroute lfa-backup exclude

命令用来禁止接口参与 LFA（Loop ospfv3 fast-reroute lfa-backup exclude Free Alternate）计算。
undo ospfv3 fast-reroute lfa-backup exclude 命令用来取消禁止接口参与 LFA 计算配置的配置。
【命令】
ospfv3 fast-reroute lfa-backup exclude [ instance instance-id ] undo ospfv3 fast-reroute lfa-backup exclude [ instance instance-id ]【缺省情况】
接口参与 计算。
LFA【视图】
接口视图【缺省用户角色】
network-admin【参数】
instance-id：接口所属的实例 ID，取值范围为 0～255，缺省值为 0。
instance【使用指导】
接口缺省参与 计算，有资格成为备份接口。配置本功能后，接口不会被选为备份接口。
LFA

【举例】
\# 禁止接口 Vlan-interface11 参与 LFA 计算。
<Sysname> system-view [Sysname] interface vlan-interface 11 [Sysname-Vlan-interface11] ospfv3 fast-reroute lfa-backup exclude

##### 1.1.49 ospfv3 ipsec-profile

ospfv3 ipsec-profile 命令用来在 OSPFv3 接口上应用 IPsec 安全框架。
undo ospfv3 ipsec-profile 命令用来取消 OSPFv3 接口上应用的 IPsec 安全框架。
【命令】
ospfv3 ipsec-profile profile-name [ instance instance-id ] undo ospfv3 ipsec-profile [ instance instance-id ]【缺省情况】
OSPFv3 接口没有应用 IPsec 安全框架。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
profile-name：IPsec 安全框架名称，为 1～63 个字符的字符串，不区分大小写。
instance instance-id：接口所属的实例 ID，取值范围为 0～255，缺省值为 0。
【使用指导】
本命令应结合 IPsec安全框架使用，IPsec安全框架的具体情况请参见“安全配置指导”中的“IPsec”。
【举例】
\# 配置 OSPFv3 接口 Vlan-interface10 上应用的 IPsec 安全框架为 profile001。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospfv3 ipsec-profile profile001

##### 1.1.50 ospfv3 mib-binding

命令用来配置 OSPFv3 进程绑定 MIB。
ospfv3 mib-binding命令用来恢复缺省情况。
undo ospfv3 mib-binding【命令】
ospfv3 mib-binding process-id undo ospfv3 mib-binding【缺省情况】
绑定在进程号最小的 进程上。
MIB OSPFv3

【视图】
系统视图【缺省用户角色】
network-admin【参数】
process-id：OSPFv3 进程号，取值范围为 1～65535。
【使用指导】
如果指定的 process-id 不存在，配置 OSPFv3 进程绑定命令时将会提示 OSPFv3 进程不存在，无法完成配置。
如果配置了 OSPFv3 进程绑定 MIB，若删除 process-id 对应的 OSPFv3 进程，则同时删除OSPFv3 进程绑定 MIB 配置，MIB 绑定到进程号最小的 OSPFv3 进程上。
【举例】
配置 进程 绑定 MIB。
\# OSPFv3 100 <Sysname> system-view [Sysname] ospfv3 mib-binding 100

##### 1.1.51 ospfv3 mtu-ignore

命令用来配置接口在进行 报文交换时忽略 检查。
ospfv3 mtu-ignore DD MTU命令用来取消接口在进行 报文交换时忽略 检查的配置。
undo ospfv3 mtu-ignore DD MTU【命令】
ospfv3 mtu-ignore [ instance instance-id ] undo ospfv3 mtu-ignore [ instance instance-id ]【缺省情况】
接口在进行 DD 报文交换时执行 MTU 检查。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
instance instance-id：接口所属的实例 ID，取值范围为 0～255，缺省值为 0。
【使用指导】
双方的接口 MTU 必须相同才能建立邻居关系。
【举例】
\# 配置运行 OSPFv3 实例 1 的接口 Vlan-interface10 在进行 DD 报文交换时忽略 MTU 检查。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospfv3 mtu-ignore instance 1

##### 1.1.52 ospfv3 network-type

ospfv3 network-type 命令用来配置 OSPFv3 接口的网络类型。
undo ospfv3 network-type 命令用来取消 OSPFv3 接口的网络类型的配置。
【命令】
ospfv3 network-type { broadcast | nbma | p2mp [ unicast ] | p2p } [ instance instance-id ] undo ospfv3 network-type [ instance instance-id ]【缺省情况】
接口网络类型的缺省值为广播类型。
OSPFv3【视图】
接口视图【缺省用户角色】
network-admin【参数】
broadcast：配置接口的网络类型为广播类型。
nbma：配置接口的网络类型为 NBMA 类型。
p2mp：配置接口的网络类型为点到多点类型。
unicast：P2MP 类型支持单播发送报文，缺省情况下是组播方式发送报文。
p2p：配置接口的网络类型为点到点类型。
instance-id：接口所属的实例 ID，取值范围为 0～255，缺省值为 0。
【使用指导】
如果在广播网络上有不支持组播地址的路由器，可以将接口的网络类型改为 NBMA。
接口的网络类型为 NBMA 或 P2MP（unicast）时，必须使用 peer 命令来配置邻接点。
接口的网络类型为 P2MP（unicast）时，OSPFv3 协议在该接口上发送的报文均为单播报文。
【举例】
设置运行 的接口 网络类型为 NBMA。
\# OSPFv3 Vlan-interface20 <Sysname> system-view [Sysname] interface vlan-interface 20 [Sysname-Vlan-interface20] ospfv3 network-type nbma【相关命令】
• ospfv3 dr-priority

##### 1.1.53 ospfv3 peer

命令用来指定邻居接口的链路本地地址，并指定该邻居是否有选举权。
ospfv3 peer命令用来取消指定邻居接口的链路本地地址的配置。
undo ospfv3 peer

【命令】
ospfv3 peer ipv6-address [ cost cost-value | dr-priority priority ] [ instance instance-id ] undo ospfv3 peer ipv6-address [ instance instance-id ]【缺省情况】
未指定邻居接口的链路本地地址。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
ipv6-address：邻居的链路本地地址。
cost cost-value：表示网络邻居的开销，取值范围为 1～65535。
dr-priority priority：表示网络邻居的优先级，取值范围为 0～255，缺省值为 1。
instance instance-id：接口所属的实例 ID，取值范围为 0～255，缺省值为 0。
【使用指导】
当路由器的接口类型为如下网络类型时，需要为其指定相邻路由器 IP 地址：
• NBMA 网络
• P2MP 网络（仅当接口选择单播形式发送报文时，需要此配置）
由于无法通过广播 Hello 报文的形式发现相邻路由器，必须手工指定相邻路由器的本地链路地址。
对于 NBMA 网络，可以指定该相邻路由器是否有选举权等。
【举例】
在运行 协议的接口 上指定邻居的链路本地地址为 FE80::1111。
\# OSPFv3 Vlan-interface10 <Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospfv3 peer fe80::1111

##### 1.1.54 ospfv3 prefix-suppression

命令用来抑制接口进行前缀发布。
ospfv3 prefix-suppression命令用来取消抑制接口进行前缀发布的配置。
undo ospfv3 prefix-suppression【命令】
ospfv3 prefix-suppression [ disable ] [ instance instance-id ] undo ospfv3 prefix-suppression [ instance instance-id ]【缺省情况】
不抑制接口进行前缀发布。
【视图】
接口视图

【缺省用户角色】
network-admin【参数】
disable：不抑制接口进行前缀发布。
instance-id：接口所属的实例 ID，取值范围为 0～255，缺省值为 0。
instance【使用指导】
如果 OSPFv3 进程配置了抑制前缀发布，但某个接口不想进行抑制，此时可以配置本命令并指定disable 参数。
【举例】
\# 抑制接口 Vlan-interface10 进行前缀发布。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospfv3 prefix-suppression【相关命令】
prefix-suppression

##### 1.1.55 ospfv3 primary-path-detect bfd

ospfv3 primary-path-detect bfd 命令用来使能 OSPFv3协议中主用链路的 BFD检测功能。
undo ospfv3 primary-path-detect bfd 命令用来关闭 OSPFv3 协议中主用链路的 BFD 检测功能。
【命令】
ospfv3 primary-path-detect bfd { ctrl | echo } [ instance instance-id ] undo ospfv3 primary-path-detect bfd [ instance instance-id ]【缺省情况】
OSPFv3 协议中主用链路的 BFD 检测功能处于关闭状态。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
ctrl：配置通过工作于控制报文方式的 BFD 会话对主用链路进行检测。
echo：配置通过工作于 echo 报文方式的 BFD 会话对主用链路进行检测。
instance-id：接口所属的实例 ID，取值范围为 0～255，缺省值为 0。
instance【使用指导】
配置本功能后，OSPFv3 协议的快速重路由特性中的主用链路将使用 进行检测。
BFD

【举例】
\# 在接口 Vlan-interface10 上配置 OSPFv3 协议快速重路由特性中主用链路使能 BFD（Echo 方式）
检测功能。
<Sysname> system-view [Sysname] ospfv3 1 [Sysname-ospfv3-1] fast-reroute lfa [Sysname-ospfv3-1] quit [Sysname] bfd echo-source-ipv6 1::1 [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospfv3 primary-path-detect bfd echo

##### 1.1.56 ospfv3 timer dead

ospfv3 timer dead 命令用来配置 OSPFv3 的邻居失效时间。
undo ospfv3 timer dead 命令用来取消 OSPFv3 的邻居失效时间的配置。
【命令】
ospfv3 timer dead seconds [ instance instance-id ] undo ospfv3 timer dead [ instance instance-id ]【缺省情况】
P2P、Broadcast 类型接口的 OSPFv3 邻居失效的时间为 40 秒；P2MP、NBMA 类型接口的 OSPFv3邻居失效的时间为 秒。
120【视图】
接口视图【缺省用户角色】
network-admin【参数】
seconds：OSPFv3 邻居失效的时间，取值范围为 1～65535，单位为秒。
instance-id：接口所属的实例 ID，取值范围为 0～255，缺省值为 0。
instance【使用指导】
OSPFv3 邻居的失效时间是指：在该时间间隔内，若未收到邻居的 Hello 报文，就认为该邻居已失效。dead 值至少应为 值的 倍，同一网段上的接口的seconds hello seconds 4 dead seconds也必须相同。
【举例】
\# 配置接口 Vlan-interface10 上的邻居失效时间为 60 秒。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospfv3 timer dead 60【相关命令】
• ospfv3 timer hello

##### 1.1.57 ospfv3 timer hello

ospfv3 timer hello 命令用来配置接口发送 Hello 报文的时间间隔。
undo ospfv3 timer hello 命令用来取消接口发送 Hello 报文的时间间隔的配置。
【命令】
ospfv3 timer hello seconds [ instance instance-id ] undo ospfv3 timer hello [ instance instance-id ]【缺省情况】
P2P、Broadcast 类型接口发送 Hello 报文的时间间隔为 10 秒；P2MP、NBMA 类型接口发送 Hello报文的时间间隔为 秒。
30【视图】
接口视图【缺省用户角色】
network-admin【参数】
seconds：接口发送 Hello 报文的时间间隔，取值范围为 1～65535，单位为秒。
instance-id：接口所属的实例 ID，取值范围为 0～255，缺省值为 0。
instance【使用指导】
的值越小，发现网络拓扑改变的速度越快，对系统资源的开销也就越大。同一网段上的seconds接口的 seconds 必须相同。
【举例】
\# 配置接口 Vlan-interface10 发送 Hello 报文的时间间隔为 20 秒。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospfv3 timer hello 20【相关命令】
•ospfv3 timer dead

##### 1.1.58 ospfv3 timer poll

命令用来配置在 NBMA 接口上向状态为 down 的邻居路由器发送轮询 Hello ospfv3 timer poll报文的时间间隔。
命令用来取消在 NBMA 接口上向状态为 down 的邻居路由器发送轮undo ospfv3 timer poll询 报文的时间间隔的配置。
Hello【命令】
ospfv3 timer poll seconds [ instance instance-id ] undo ospfv3 timer poll [ instance instance-id ]

【缺省情况】
在 NBMA 接口上向状态为 down 的邻居路由器发送轮询 Hello 报文的时间间隔为 120 秒。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
seconds：向状态为 down 的邻居路由器发送轮询 Hello 报文的时间间隔，取值范围为 1～65535，单位为秒。
instance instance-id：接口所属的实例 ID，取值范围为 0～255，缺省值为 0。
【使用指导】
在 NBMA 的网络上，当邻居失效后，将按轮询时间间隔定期地发送 Hello 报文。用户可配置轮询时间间隔以指定该接口在与相邻路由器构成邻居关系之前发送 报文的时间间隔。
Hello发送轮询 Hello 报文的时间间隔至少应为发送 Hello 报文时间间隔的 4 倍。
【举例】
配置接口 发送轮询 报文的时间间隔为 秒。
\# Vlan-interface10 Hello 120 <Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospfv3 timer poll 120【相关命令】
• ospfv3 timer hello

##### 1.1.59 ospfv3 timer retransmit

ospfv3 timer retransmit 命令用来配置接口重传 LSA 的时间间隔。
undo ospfv3 timer retransmit 命令用来取消接口重传 LSA 的时间间隔的配置。
【命令】
ospfv3 timer retransmit seconds [ instance instance-id ] undo ospfv3 timer retransmit [ instance instance-id ]【缺省情况】
接口重传 LSA 的时间间隔为 5 秒。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
seconds：接口重传 LSA 的时间间隔，取值范围为 1～3600，单位为秒。

instance-id：接口所属的实例 ID，取值范围为 0～255，缺省值为 0。
instance【使用指导】
当一台路由器向它的邻居发送一条 后，需要等到对方的确认报文。若在该重传 的时间间LSA LSA隔内未收到对方的确认报文，就会重传这条 LSA。
相邻路由器重传 LSA 时间间隔的值不要设置得太小，否则将会引起不必要的重传。
【举例】
\# 指定运行 OSPFv3 实例 1 的接口 Vlan-interface10 重传 LSA 的时间间隔为 12 秒。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospfv3 timer retransmit 12 instance 1

##### 1.1.60 ospfv3 trans-delay

ospfv3 trans-delay 命令用来配置接口对 LSA 的传输延迟时间。
undo ospfv3 trans-delay 命令用来取消接口对 LSA 的传输延迟时间的配置。
【命令】
ospfv3 trans-delay seconds [ instance instance-id ] undo ospfv3 trans-delay [ instance instance-id ]【缺省情况】
接口对 LSA 的传输延迟时间为 1 秒。
【视图】
接口视图【缺省用户角色】
network-admin【参数】
seconds：接口对 LSA 的传输延迟时间，取值范围为 1～3600，单位为秒。
instance instance-id：接口所属的实例 ID，取值范围为 0～255，缺省值为 0。
【使用指导】
LSA 在本路由器的 LSDB 中会随时间老化（LSA 的老化时间每秒钟加 1），但在网络的传输过程中却不会，所以有必要在发送之前在 的老化时间上增加一定的延迟时间。此配置对低速率的网络LSA尤其重要。
【举例】
\# 指定运行 OSPFv3 实例 1 的接口 Vlan-interface10 洪泛 LSA 的时延值为 3 秒。
<Sysname> system-view [Sysname] interface vlan-interface 10 [Sysname-Vlan-interface10] ospfv3 trans-delay 3 instance 1

##### 1.1.61 preference

preference 命令用来配置 OSPFv3 协议的路由优先级。

命令用来取消 OSPFv3 协议的路由优先级的配置。
undo preference【命令】
preference [ ase ] { preference | route-policy route-policy-name } * undo preference [ ase ]【缺省情况】
对于自治系统内部路由，OSPFv3 协议的路由优先级为 10；对于自治系统外部路由，OSPFv3 协议的路由优先级为 150。
【视图】
OSPFv3 视图【缺省用户角色】
network-admin【参数】
ase：配置 OSPFv3 协议对自治系统外部路由的优先级。如果未指定该参数，则配置的是 OSPFv3协议对自治系统内部路由的优先级。
preference：OSPFv3 路由的优先级，取值范围为 1～255。优先级的值越小，其实际的优先程度越高。
： 应 用 路 由 策 略 ， 对 特 定 的 路 由 设 置 优 先 级 。
route-policy route-policy-name是路由策略名称，为 1～63 个字符的字符串，区分大小写。
route-policy-name【使用指导】
由于路由器上可能同时运行多个动态路由协议，就存在各个路由协议之间路由信息共享和选择的问题，所以为每一种路由协议指定了一个缺省的优先级。在不同的路由协议发现去往同一目的地的多条路由时，优先级高的协议发现的路由将被选中以转发 IPv6 报文。
【举例】
配置 协议路由的优先级为 150。
\# OSPFv3 <Sysname> system-view [Sysname] ospfv3 [Sysname-ospfv3-1] preference 150

##### 1.1.62 prefix-suppression

命令用来抑制 进程进行前缀发布。
prefix-suppression OSPFv3命令用来恢复缺省情况。
undo prefix-suppression【命令】
prefix-suppression undo prefix-suppression【缺省情况】
不抑制 OSPFv3 进程进行前缀发布。

【视图】
OSPFv3 视图【缺省用户角色】
network-admin【使用指导】
接口使能 后，会将接口下的所有网段路由都通过 发布，但有时候网段路由是不希望OSPFv3 LSA被发布的。通过前缀抑制配置，可以减少 LSA 中携带不需要的前缀，即不发布某些网段路由，从而提高网络安全性，加快路由收敛。
全局配置前缀抑制不能抑制 LoopBack 接口和处于 silent-interface 状态接口对应的前缀。如果想对Loopback 接口或处于 silent-interface 状态接口进行抑制，可以通过接口下配置前缀抑制（ospfv3命令）来实现。
prefix-suppression当使能前缀抑制时，具体处理如下：
中不发布处于抑制的接口前缀信息。
• Type-8 LSA对于广播网/NBMA 网络，DR 在生成 Type-9 LSA 引用 Type-2 LSA 时，不发布处于抑制的接
•口前缀信息。
对于 网络，生成 引用 时，不发布处于抑制的接口前缀信
• P2P/P2MP Type-9 LSA Type-1 LSA息。
【举例】
\# 抑制 OSPFv3 进程 100 的前缀发布。
<Sysname> system-view [Sysname] ospfv3 100 [Sysname-ospfv3-100] prefix-suppression【相关命令】
ospfv3 prefix-suppression

##### 1.1.63 reset ospfv3 event-log

命令用于清除 OSPFv3 的日志信息。
reset ospfv3 event-log【命令】
reset ospfv3 [ process-id ] event-log [ lsa-flush | peer | spf ]【视图】
用户视图【缺省用户角色】
network-admin【参数】
process-id：OSPFv3 进程号，取值范围为 1～65535。如果未指定本参数，则清除所有 OSPFv3进程的日志信息。
lsa-flush：清除 LSA 老化日志信息。

peer：清除邻居的日志信息。
spf：清除路由计算的日志信息。
【使用指导】
如果未指定日志类型，则所有日志信息都被清除。
【举例】
\# 清除所有 OSPFv3 进程路由计算的日志信息。
<Sysname> reset ospfv3 event-log spf【相关命令】
• display ospfv3 event-log

##### 1.1.64 reset ospfv3 process

命令用来重启 进程。
reset ospfv3 process OSPFv3【命令】
reset ospfv3 [ process-id ] process [ graceful-restart ]【视图】
用户视图【缺省用户角色】
network-admin【参数】
process-id：OSPFv3 进程号，取值范围为 1～65535。如果未指定本参数，则重启所有OSPFv3进程。
graceful-restart：以 GR 方式重启 OSPFv3 进程。
【使用指导】
使用 reset ospfv3 process 命令重启 OSPFv3，可以获得如下结果：
• 可以立即清除无效的 LSA，而不必等到 LSA 超时。
• 方便重新选举 DR、BDR。
• 重启前的 OSPFv3 配置不会丢失。
执行该命令后，系统提示用户确认是否重启 OSPFv3 协议。
【举例】
\# 重启所有 OSPFv3 进程。
<Sysname> reset ospfv3 process Reset OSPFv3 process? [Y/N]:y

##### 1.1.65 reset ospfv3 redistribution

命令用来重新向 OSPFv3 引入外部路由。
reset ospfv3 redistribution【命令】
reset ospfv3 [ process-id ] redistribution

【视图】
用户视图【缺省用户角色】
network-admin【参数】
process-id：OSPFv3 进程号，取值范围为 1～65535。如果未指定本参数，所有 进程OSPFv3都将重新引入外部路由。
【举例】
\# 重新向 OSPFv3 引入外部路由。
<Sysname> reset ospfv3 redistribution

##### 1.1.66 reset ospfv3 statistics

命令用来清除 的统计信息。
reset ospfv3 statistics OSPFv3【命令】
reset ospfv3 [ process-id ] statistics【视图】
用户视图【缺省用户角色】
network-admin【参数】
process-id：OSPFv3 进程号，取值范围为 1～65535。如果未指定本参数，则清除所有OSPFv3进程的统计信息。
【举例】
\# 清除所有 OSPFv3 进程的统计信息。
<Sysname> reset ospfv3 statistics

##### 1.1.67 router-id

命令用来配置运行 协议的路由器的 ID。
router-id OSPFv3 Router命令用来恢复缺省情况。
undo router-id【命令】
router-id router-id undo router-id【缺省情况】
运行 OSPFv3 协议的路由器没有 Router ID。
【视图】
OSPFv3 视图

【缺省用户角色】
network-admin【参数】
router-id：路由器标识符，IPv4 地址格式。
【使用指导】
是一台运行 协议的路由器在自治系统中的唯一标识。如果用户没有指定路由器Router ID OSPFv3的 Router ID，则 OSPFv3 进程无法运行。
同一台设备上以及同一自治系统中不同的 OSPFv3 进程，必须为其指定不同的 Router ID。
【举例】
\# 设置 OSPFv3 进程 1 的 Router ID 为 10.1.1.3。
<Sysname> system-view [Sysname] ospfv3 1 [Sysname-ospfv3-1] router-id 10.1.1.3【相关命令】
• ospfv3

##### 1.1.68 silent-interface (OSPFv3 view)

silent-interface 命令用来禁止接口收发 OSPFv3 报文。
undo silent-interface 命令用来取消禁止接口收发 OSPFv3 报文的配置。
【命令】
silent-interface { interface-type interface-number | all } undo silent-interface { interface-type interface-number | all }【缺省情况】
允许接口收发 OSPFv3 报文。
【视图】
视图OSPFv3【缺省用户角色】
network-admin【参数】
interface-number：接口类型和接口号，禁止指定 OSPFv3 接口收发interface-type OSPFv3 报文。
all：禁止所有 OSPFv3 接口收发 OSPFv3 报文。
【使用指导】
不同的进程可以对同一接口禁止收发 报文，但 命令只对本进程已经OSPFv3 silent-interface使能的 OSPFv3 接口起作用，对其它进程的接口不起作用。

【举例】
\# 禁止接口 Vlan-interface10 在 OSPFv3 进程 100 和 200 中收发 OSPFv3 报文。
<Sysname> system-view [Sysname] ospfv3 100 [Sysname-ospfv3-100] router-id 10.100.1.9 [Sysname-ospfv3-100] silent-interface vlan-interface 10 [Sysname-ospfv3-100] quit [Sysname] ospfv3 200 [Sysname-ospfv3-200] router-id 20.100.1.9 [Sysname-ospfv3-200] silent-interface vlan-interface 10

##### 1.1.69 snmp context-name

命令用来创建一个管理 OSPFv3 的 SNMP 实体所使用的上下文名称。
snmp context-name命令用来恢复缺省情况。
undo snmp context-name【命令】
snmp context-name context-name undo snmp context-name【缺省情况】
不存在管理 的 实体所使用的上下文名称。
OSPFv3 SNMP【视图】
OSPFv3 视图【缺省用户角色】
network-admin【参数】
context-name：管理 OSPFv3 的 SNMP 实体所使用的上下文名称，为 1～32 个字符的字符串，区分大小写。
【使用指导】
OSPFv3 使用 MIB（Management Information Base，管理信息库）为 NMS（Network Management System，网络管理系统）提供对 OSPFv3 实例的管理，但标准 OSPFv3 MIB 中定义的 MIB 为单实例管理对象，无法对多个 OSPFv3 实例进行管理。因此，参考 RFC 4750 中对 OSPF 多实例的管理方法，为管理 的 实体定义一个上下文名称，以此来区分不同的 实例，OSPFv3 SNMP OSPFv3实现对多个 OSPFv3 实例进行管理。由于上下文名称只是 SNMPv3 独有的概念，对于 SNMPv1/v2c，会将团体名映射为上下文名称以对不同协议进行区分。
【举例】
配置管理 进程 的 实体所使用的上下文名称为 mib。
\# OSPFv3 1 SNMP <Sysname> system-view [Sysname] ospfv3 1 [Sysname-ospfv3-1] snmp context-name mib

##### 1.1.70 snmp trap rate-limit

snmp trap rate-limit 命令用来配置 OSPFv3 在指定时间间隔内允许输出的告警信息条数。
undo snmp trap rate-limit 命令用来恢复缺省情况。
【命令】
snmp trap rate-limit interval trap-interval count trap-number undo snmp trap rate-limit【缺省情况】
OSPFv3 在 10 内秒允许输出 7 条告警信息。
【视图】
视图OSPFv3【缺省用户角色】
network-admin【参数】
interval trap-interval：指定时间间隔，取值范围为 2～60，单位为秒。
count trap-number：在指定时间间隔内允许输出的告警信息条数，取值范围为 0～300，为 0时表示不输出告警信息。
【举例】
配置 在 秒内允许输出 条告警信息。
\# OSPFv3 5 10 <Sysname> system-view [Sysname] ospfv3 100 [Sysname-ospfv3-100] snmp trap rate-limit interval 5 count 10

##### 1.1.71 snmp-agent trap enable ospfv3

命令用来开启 OSPFv3 的告警功能。
snmp-agent trap enable ospfv3命令用来关闭 OSPFv3 的告警功能。
undo snmp-agent trap enable ospfv3【命令】
snmp-agent trap enable ospfv3 [ grrestarter-status-change | grhelper-status-change | if-state-change | if-cfg-error | if-bad-pkt | neighbor-state-change | nssatranslator-status-change | virtif-bad-pkt | virtif-cfg-error | virtif-state-change | virtgrhelper-status-change | virtneighbor-state-change ] * undo snmp-agent trap enable ospfv3 [ grrestarter-status-change | grhelper-status-change | if-state-change | if-cfg-error | if-bad-pkt | neighbor-state-change | nssatranslator-status-change | virtif-bad-pkt | virtif-cfg-error | virtif-state-change | virtgrhelper-status-change | virtneighbor-state-change] *

【缺省情况】
OSPFv3 的告警功能处于开启状态。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
grrestarter-status-change：GR Restarter 状态变化。
grhelper-status-change：邻居 状态变化。
GR Helper if-state-change：接口状态变化。
if-cfg-error：接口配置错误。
if-bad-pkt：接口接收了错误报文。
neighbor-state-change：邻居状态变化。
nssatranslator-status-change：NSSA 转换路由器状态变化。
virtif-bad-pkt：虚接口接收错误报文。
virt-cfg-error：虚接口配置错误。
virtif-state-change：虚接口状态变化。
virtgrhelper-status-change：虚接口邻居 GR Helper 状态变化。
virtneighbor-state-change：虚接口邻居状态变化。
【举例】
\# 关闭 OSPFv3 的告警功能。
<Sysname> system-view [Sysname] undo snmp-agent trap enable ospfv3

##### 1.1.72 spf-schedule-interval

命令用来配置 路由计算的时间间隔。
spf-schedule-interval OSPFv3命令用来恢复缺省情况。
undo spf-schedule-interval【命令】
spf-schedule-interval maximum-interval [ minimum-interval [ incremental-interval ] ] undo spf-schedule-interval【缺省情况】
OSPFv3 路由计算的最大时间间隔为 5 秒，最小时间间隔为 50 毫秒，时间间隔惩罚增量为 200 毫秒。
【视图】
OSPFv3 视图

【缺省用户角色】
network-admin【参数】
maximum-interval：OSPFv3 路由计算的最大时间间隔，取值范围为 1～60，单位为秒。
minimum-interval：OSPFv3 路由计算的最小时间间隔，取值范围为 10～60000，单位为毫秒。
incremental-interval：OSPFv3 路由计算的时间间隔惩罚增量，取值范围为 10～60000，单位为毫秒。
【使用指导】
根据本地维护的 LSDB，运行 协议的路由器通过 算法计算出以自己为根的最短路径OSPFv3 SPF树，并根据这一最短路径树决定到目的网络的下一跳。通过调节 SPF 的计算间隔，可以抑制网络频繁变化可能导致的带宽资源和路由器资源被过多占用的问题。
本命令在网络变化不频繁的情况下将连续路由计算的时间间隔缩小到 minimum-interval，而在网络变化频繁的情况下可以进行相应惩罚，将等待时间按照配置的惩罚增量延长，最大不超过maximum-interval。
minimum-interval 和 incremental-interval 配置值不允许大于 maximum-interval 配置值。
【举例】
\# 设置 OSPFv3 路由计算最大时间间隔为 10 秒，最小时间间隔为 500 毫秒，惩罚增量为 300 毫秒。
<Sysname> system-view [Sysname] ospfv3 100 [Sysname-ospfv3-100] spf-schedule-interval 10 500 300

##### 1.1.73 stub (OSPFv3 area view)

stub 命令用来配置一个区域为 Stub 区域。
undo stub 命令用来恢复缺省情况。
【命令】
stub [ default-route-advertise-always | no-summary ] * undo stub【缺省情况】
没有区域被设置为 区域。
Stub【视图】
OSPFv3 区域视图【缺省用户角色】
network-admin【参数】
default-route-advertise-always：该参数用于设置总是通告默认路由。

no-summary：该参数只用于 Stub 区域的 ABR，配置后 ABR 只向区域内发布一条缺省路由的。 这 种 既 没 有 ， 也 没 有 其 它 、Inter-Area-Prefix-LSA AS-external-LSA Inter-Area-Prefix-LSA Inter-Area-Router-LSA 的 Stub 区域，又称为 Totally Stub 区域。
【使用指导】
如果需要在 ABR 上取消配置 no-summary 参数，可以通过重新执行 stub 命令覆盖之前配置即可。
如果要将一个区域配置成 Stub 区域，则该区域中的所有路由器都必须配置此属性。
【举例】
\# 将 OSPFv3 区域 1 设置为 Stub 区域。
<Sysname> system-view [Sysname] ospfv3 1 [Sysname-ospfv3-1] area 1 [Sysname-ospfv3-1-area-0.0.0.1] stub【相关命令】
• (OSPFv3 area view)
default-cost

##### 1.1.74 stub-router

命令用来配置当前路由器为 Stub 路由器。
stub-router undo stub-router 命令用来恢复缺省情况。
【命令】
stub-router r-bit [ include-stub | on-startup { seconds | wait-for-bgp [ seconds ] } ] * stub-router max-metric [ external-lsa [ max-metric-value ] | summary-lsa [ max-metric-value ] | include-stub | on-startup { seconds | wait-for-bgp [ seconds ] } ] * undo stub-router【缺省情况】
当前路由器没有被配置为 Stub 路由器。
【视图】
视图OSPFv3【缺省用户角色】
network-admin【参数】
r-bit：路由器发布的 Type-1 LSA 中，options 域的 R-bit 将清除。
max-metric：路由器发布的 Type-1 LSA 的链路度量值将设置为最大值 65535。
external-lsa max-metric-value ：路由器发布的外部 LSA 链路度量值。 max-metric-value表示链路度量值，取值范围为 1～16777215，缺省值为 16711680。
max-metric-value：路由器发布的 Type-3 LSA 和 Type-4 LSA 链路度量值。
summary-lsa表示链路度量值，取值范围为 1～16777215，缺省值为 16711680。
max-metric-value

include-stub：路由器发布的引用 Type-1 LSA 的 Type-9 LSA 中，链路度量值将设置为最大值65535。
seconds：在路由器重启期间，路由器作为 路由器。seconds 表示超时时间，on-startup Stub取值范围为 5～86400，单位为秒。
wait-for-bgp seconds：在路由器重启后，等待 BGP 路由收敛期间，路由器作为 Stub 路由器。
表示超时时间，取值范围为 5～86400，单位为秒，缺省值为 600 秒。
seconds【使用指导】
将当前路由器配置为 Stub 路由器的功能，可通过 R-bit 和 max-metric 两种模式来实现：
R-bit 模式：通过清除该路由器发布 Type-1 LSA 中 options 域的 R-bit，使其他路由器不通过
•该路由器来转发数据。
模式：该路由器发布的 的链路度量值将设为最大值 65535，这样其邻
• max-metric Type-1 LSA居计算出这条路由的开销就会很大，如果邻居上有到这个目的地址开销更小的路由，则数据不会通过这个 Stub 路由器转发。
【举例】
\# 配置当前路由器为 Stub 路由器。
<Sysname> system-view [Sysname] ospfv3 100 [Sysname-ospfv3-100] stub-router r-bit

##### 1.1.75 transmit-pacing

用来配置接口发送 LSU 报文的时间间隔和一次发送 LSU 报文的最大个数。
transmit-pacing命令用来恢复缺省情况。
undo transmit-pacing【命令】
transmit-pacing interval interval count count undo transmit-pacing【缺省情况】
接口发送 报文的时间间隔为 毫秒，一次最多发送 个 报文。
LSU 20 3 LSU【视图】
OSPFv3 视图【缺省用户角色】
network-admin【参数】
interval：接口发送 LSU 报文的时间间隔，interval 的取值范围为 10～1000，单interval位为毫秒。当路由器上使能 功能的接口数比较多时，建议增大该值，以控制路由器每秒钟OSPFv3发送 LSU 报文的总数。
count count：接口一次发送 LSU 报文的最大个数，count 的取值范围为 1～200。当路由器上使能 OSPFv3 功能的接口数比较多时，建议减小该值，以控制路由器每秒钟发送 LSU 报文的总数。

【举例】
\# 配置 OSPFv3 进程 1 的所有接口发送 LSU 报文的时间间隔为 30 毫秒，一次最多发送 10 个 LSU报文。
<Sysname> system-view [Sysname] ospfv3 1 [Sysname-ospfv3-1] transmit-pacing interval 30 count 10

##### 1.1.76 vlink-peer (OSPFv3 area view)

命令用来创建并配置一条虚连接。
vlink-peer undo vlink-peer 命令用来删除一条已有的虚连接。
【命令】
vlink-peer router-id [ dead seconds | hello seconds | instance instance-id | ipsec-profile profile-name | keychain keychain-name | retransmit seconds | trans-delay seconds ] * undo vlink-peer router-id [ dead | hello | ipsec-profile | keychain | retransmit | trans-delay ] *【缺省情况】
不存在虚连接。
【视图】
区域视图OSPFv3【缺省用户角色】
network-admin【参数】
router-id：虚连接邻居的路由器 ID。
dead seconds：失效时间间隔，取值范围为 1～32768，单位为秒，缺省值为 40 秒。该值必须和与其建立虚连接路由器的 值相等，并至少为 值的 4 倍。
dead seconds hello seconds seconds：接口发送 Hello 报文的时间间隔，取值范围为 1～8192，单位为秒，缺省值为hello秒。该值必须和与其建立虚连接路由器上的 值相等。
10 hello seconds instance-id：设置虚连接的实例 ID，取值范围为 0～255，缺省值为 0。
instance profile-name：应用 IPsec 安全框架。profile-name 为 IPsec 安全框架名ipsec-profile称，为 1～63 个字符的字符串，不区分大小写。IPsec 安全框架的具体情况请参见“安全配置指导”中的“IPsec”。
keychain：使用 keychain 验证模式。
keychain-name：keychain 名称，为 1～63 个字符的字符串，区分大小写。
retransmit seconds：接口重传 LSA 报文的时间间隔，取值范围为 1～3600，单位为秒，缺省值为 5。
trans-delay seconds：接口延迟发送 LSA 报文的时间间隔，取值范围为 1～3600，单位为秒，缺省值为 1。

【使用指导】
对于没有和骨干区域直接相连的非骨干区域，或者不连续的骨干区域来说，可以使用 vlink-peer命令建立逻辑上的连通性。在某种程度上，可以将虚连接看作一个普通的使能了 OSPFv3 的接口，因为在其上配置的 hello、dead、retransmit 和 等参数的原理是类似的。
trans-delay虚连接的两端必须是 ABR，vlink-peer 命令必须在两端同时配置才可生效。
各参数取值规则如下：
值越小，发现网络变化的速度越快，消耗的网络资源也就越多。
• hello不能将 值设置的太小，否则将会引起不必要的重传。网络速度相对较慢的时候
• retransmit应把该值设的更大一些。
设置 值时必须考虑接口的发送延迟。
• trans-delay在OSPFv3虚连接下配置的验证模式，其优先级高于在骨干区域下配置的验证模式。只有在OSPFv3虚连接下未配置验证模式时，骨干区域下配置的验证模式才会对该虚连接生效。
在 OSPFv3 虚连接使用 keychain 验证模式时，报文的收、发过程如下：
• OSPFv3 在发送报文前，会先从 keychain 获取当前的有效发送 key，根据该 key 的标识符、认证算法和认证密钥进行报文验证。如果当前不存在有效发送 key，OSPFv3 不会发送报文。
• OSPFv3 在收到报文后，会根据报文携带的 key 的标识符从 keychain 中获取有效接收 key，根据该 key 的认证算法和认证密钥对报文进行校验。如果报文校验失败，或者根据报文中携带的 的标识符无法从 中获取到有效接收 key，则该报文将被丢弃。
key keychain对于 认证算法和 的标识符的范围，OSPFv3 的支持情况如下：
keychain key仅支持 认证算法。
• OSPFv3 HMAC-SHA-256 OSPFv3 仅支持标识符取值范围为 0～65535 的 key。
•【举例】
创建一条到 的虚连接。
\# 10.10.0.3 <Sysname> system-view [Sysname] ospfv3 1 [Sysname-ospfv3-1] area 1 [Sysname-ospfv3-1-area-0.0.0.1] vlink-peer 10.10.0.3【相关命令】
• display ospfv3 vlink

## 11-IPv6策略路由命令

目 录策略路由配置命令

### 1 IPv6策略路由

#### 1.1 IPv6策略路由配置命令

##### 1.1.1 apply next-hop

命令用来设置报文转发的下一跳。
apply next-hop命令用来取消报文转发下一跳的设置。
undo apply next-hop【命令】
apply next-hop [ vpn-instance vpn-instance-name ] { ipv6-address [ direct ] [ track track-entry-number ] } &<1-2> undo apply next-hop [ [ vpn-instance vpn-instance-name ] ipv6-address&<1-2> ]【缺省情况】
未设置报文转发的下一跳。
【视图】
IPv6 策略节点视图【缺省用户角色】
network-admin【参数】
vpn-instance-name：下一跳所在的 VPN 实例。vpn-instance-name 表示vpn-instance的 实例名称，为 1～31 个字符的字符串，区分大小写。指定的 实例必须MPLS L3VPN VPN VPN已经存在。
ipv6-address：下一跳 IPv6 地址。如果未指定 vpn-instance 参数，表示指定的是公网下一跳。
direct：指定当前下一跳生效的条件为直连下一跳。
track track-entry-number：指 定 Track 项的序号， track-entry-number 取值范围为 1～1024。
&<1-2>：表示前面的参数最多可以输入 2 次。
【使用指导】
用户可以同时配置多个下一跳（通过一次或多次配置本命令实现），起到主备的作用。
配置 命令时，如果指定了下一跳 IPv6 地址，将取消已配置的该下一跳；如果未指定下一跳undo IPv6 地址，将取消已配置的所有下一跳。
【举例】
\# 设置报文转发的下一跳为 1::1。
<Sysname> system-view [Sysname] ipv6 policy-based-route aa permit node 11

[Sysname-pbr6-aa-11] apply next-hop 1::1

##### 1.1.2 description

description 命令用来配置当前 IPv6 策略节点的描述信息。
undo description 命令用来恢复缺省情况。
【命令】
description text undo description【缺省情况】
未配置 IPv6 策略节点的描述信息。
【视图】
策略节点视图IPv6【缺省用户角色】
network-admin【参数】
text：IPv6 策略节点的描述信息，为 1～127 个字符的字符串，区分大小写。
【举例】
\# 配置 IPv6 策略节点的描述信息为“Officeuse”。
<Sysname> system-view [Sysname] ipv6 policy-based-route 1 permit node 1 [Sysname-pbr6-1-1] description Officeuse

##### 1.1.3 display ipv6 policy-based-route

命令用来显示已经配置的 IPv6 策略。
display ipv6 policy-based-route【命令】
display ipv6 policy-based-route [ policy policy-name ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
policy policy-name：显示指定的 IPv6 策略。policy-name 表示策略名，唯一标识一个 IPv6策略，为 1 ～ 19 个字符的字符串，区分大小写。如果未指定本参数，则显示所有已经配置的 IPv6策略。
【举例】
\# 显示所有已经配置的 IPv6 策略。

<Sysname> display ipv6 policy-based-route Policy name: aaa node 1 permit:
if-match acl 2000 apply next-hop 1000::1表1-1 display ipv6 policy-based-route 命令显示信息描述表字段 描述Policy name 策略名节点1的匹配模式为允许node 1 permit if-match acl 满足ACL的报文被匹配apply next-hop 为匹配的报文指定下一跳【相关命令】
• ipv6 policy-based-route (system view)

##### 1.1.4 display ipv6 policy-based-route interface

命令用来显示接口下 转发策略路由的display ipv6 policy-based-route interface IPv6配置信息和统计信息。
【命令】
display ipv6 policy-based-route interface interface-type interface-number [ slot slot-number ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
interface-type interface-number：用来指定接口的类型和编号。
slot slot-number：显示指定成员设备上 IPv6 转发策略路由的配置信息和统计信息。
表示设备在 IRF 中的成员编号。如果未指定本参数，将显示主设备上 IPv6 转发策slot-number略路由的配置信息和统计信息。
【举例】
\# 显示 VLAN 接口 2 下 IPv6 转发策略路由的配置信息和统计信息。
<Sysname> display ipv6 policy-based-route interface vlan-interface 2 Policy based routing information for interface Vlan-inerface2(failed):
Policy name: aaa node 0 deny:
Matched: 0

node 1 permit:
if-match acl 3999 Matched: 0 node 2 permit:
if-match acl 2000 apply next-hop 1000::1 Matched: 0 node 5 permit:
if-match acl 3101 apply next-hop 1000::1 Matched: 0 Total matched: 0 <Sysname> display ipv6 policy-based-route interface Vlan-inerface2 Policy based routing information for interface Vlan-inerface2:
Policy name: aaa node 0 deny(not support):
Matched: 0 node 1 permit:
if-match acl 3999 Matched: 0 node 2 permit(no resource):
if-match acl 2000 apply next-hop 1000::1 Matched: 0 node 5 permit:
if-match acl 3101 apply next-hop 1000::1 Matched: 0 (no statistics resource)
Total matched: 0表1-2 display ipv6 policy-based-route interface 命令显示信息描述表字段 描述接口下IPv6转发策略路由的配置信息和统计信息（failed表示策略下发驱动失败）
Policy based routing information for interface XXXX (failed)
对于设备上的全局口（如 VLAN 接口）和物理口，只有指定 slot 后，才会显示括号内的信息。
Policy name 策略名节点的匹配模式为允许（permit）/拒绝（deny）（not support表示设备不支持该节点设置的规则；no resource表示设备的ACL等资源不足，为该节点分配ACL等资源失败）
node 0 deny(not support)
node 2 permit(no resource)
对于设备上的全局口（如 VLAN 接口）和物理口，只有指定 slot 后，才会显示括号内的信息。
if-match acl 满足ACL的报文被匹配

字段 描述apply next-hop 为匹配的报文指定下一跳节点匹配成功的次数（no statistics resource表示统计资源不足）
Matched: 0 (no statistics resource)
对于设备上的全局口（如 VLAN 接口）和物理口，只有指定 slot 后，才会显示括号内的信息。
Total matched 策略所有节点匹配成功的次数【相关命令】
• reset ipv6 policy-based-route statistics

##### 1.1.5 display ipv6 policy-based-route local

display ipv6 policy-based-route local 命令用来显示 IPv6 本地策略路由的配置信息和统计信息。
【命令】
display ipv6 policy-based-route local [ slot slot-number ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
slot slot-number：显示指定成员设备上 IPv6 本地策略路由的配置信息和统计信息。
表示设备在 IRF 中的成员编号。如果未指定本参数，将显示主设备上 IPv6 本地策slot-number略路由的配置信息和统计信息。
【举例】
\# 显示 IPv6 本地策略路由的配置信息和统计信息。
<Sysname> display ipv6 policy-based-route local Policy based routing information for local:
Policy name: aaa node 0 deny:
Matched: 0 node 1 permit:
if-match acl 3999 Matched: 0 node 2 permit:
if-match acl 2000 apply next-hop 1::1 Matched: 0

node 5 permit:
if-match acl 3101 apply next-hop 2::2 Matched: 0 Total matched: 0表1-3 display ipv6 policy-based-route local 命令显示信息描述表字段 描述Policy based routing information for local IPv6本地策略路由的配置信息和统计信息策略名Policy name node 0 deny/node 2 permit 节点的匹配模式为允许（permit）/拒绝（deny）
if-match acl 满足ACL的报文被匹配为匹配的报文指定下一跳apply next-hop Matched: 0 节点匹配成功的次数Total matched 策略所有节点匹配成功的次数【相关命令】
• reset ipv6 policy-based-route statistics

##### 1.1.6 display ipv6 policy-based-route setup

display ipv6 policy-based-route setup 命令用来显示已经应用的 IPv6 策略路由信息。
【命令】
display ipv6 policy-based-route setup【视图】
任意视图【缺省用户角色】
network-admin network-operator【举例】
显示已经应用的 策略路由信息。
\# IPv6 <Sysname> display ipv6 policy-based-route setup Policy name Type Interface pr01 Forward Vlan-interface 2 pr02 Local N/A表1-4 display ipv6 policy-based-route setup 命令显示信息描述表字段 描述Policy name 策略名

字段 描述开启策略路由类型，取值为
•Type Forward：转发策略类型
• Local：本地策略路由类型Interface 应用策略的接口【相关命令】
• ipv6 policy-based-route (interface view)

##### 1.1.7 if-match acl

命令用来设置 匹配规则。
if-match acl ACL命令用来恢复缺省情况。
undo if-match acl【命令】
if-match acl { ipv6-acl-number | name ipv6-acl-name } undo if-match acl【缺省情况】
未设置 ACL 匹配规则。
【视图】
IPv6 策略节点视图【缺省用户角色】
network-admin【参数】
ipv6-acl-number：访问控制列表号，取值范围为 2000～3999。其中：
基本 ACL，ipv6-acl-number 取值范围为 2000～2999；
• IPv6高级 ACL，ipv6-acl-number 取值范围为 3000～3999。
• IPv6：指定 的名称。 表示 的名称，为 1～name ipv6-acl-name IPv6 ACL ipv6-acl-name IPv6 ACL 63 个字符的字符串，不区分大小写，必须以英文字母 a～z 或 A～Z 开头。为避免混淆，IPv6 ACL的名称不允许使用英文单词 all。只有指定 IPv6 基本 ACL 或 IPv6 高级 ACL 的 acl-name 才生效。
【举例】
\# 设置满足 ACL 2000 的报文被匹配。
<Sysname> system-view [Sysname] ipv6 policy-based-route aa permit node 10 [Sysname-pbr6-aa-10] if-match acl 2000 \# 设置满足 ACL 名称为 aaa 的报文被匹配。
<Sysname> system-view [Sysname] ipv6 policy-based-route aa permit node 10 [Sysname-pbr6-aa-10] if-match acl name aaa

##### 1.1.8 ipv6 local policy-based-route

ipv6 local policy-based-route 命令用来对本地报文应用 IPv6 策略。
undo ipv6 local policy-based-route 命令用来恢复缺省情况。
【命令】
ipv6 local policy-based-route policy-name undo ipv6 local policy-based-route【缺省情况】
未对本地报文应用 IPv6 策略。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
policy-name：策略名，唯一标识一个 IPv6 策略，为 1～19 个字符的字符串，区分大小写。该 IPv6策略必须已经存在。
【使用指导】
对本地报文只能应用一个 策略。应用新的 策略前必须删除本地原来已经应用的 策略。
IPv6 IPv6 IPv6对本地报文应用的 策略将对本地产生的所有 报文（除了本地发送给自己的报文）进行匹IPv6 IPv6配。若无特殊需求，建议用户不要配置本地策略路由。
【举例】
\# 对本地报文应用 IPv6 策略 aaa。
<Sysname> system-view [Sysname] ipv6 local policy-based-route aaa【相关命令】
• display ipv6 policy-based-route setup
• ipv6 policy-based-route (system view)
• ipv6 policy-based-route apply

##### 1.1.9 ipv6 policy-based-route (interface view)

命令用来对接口转发的报文应用 IPv6 策略。
ipv6 policy-based-route命令用来恢复缺省情况。
undo ipv6 policy-based-route【命令】
ipv6 policy-based-route policy-name undo ipv6 policy-based-route【缺省情况】
未对接口转发的报文应用 IPv6 策略。

【视图】
接口视图【缺省用户角色】
network-admin【参数】
policy-name：策略名，唯一标识一个 策略，为 1～19 个字符的字符串，区分大小写。该IPv6 IPv6策略必须已经存在。
【举例】
\# 对 VLAN 接口 2 转发的报文应用 IPv6 策略 aaa。
<Sysname> system-view [Sysname] interface vlan-interface 2 [Sysname-Vlan-interface2] ipv6 policy-based-route aaa【相关命令】
•display ipv6 policy-based-route setup
• ipv6 policy-based-route (system view)

##### 1.1.10 ipv6 policy-based-route (system view)

ipv6 policy-based-route 命令用来创建 IPv6 策略节点，并进入 IPv6 策略节点视图。如果指定的 IPv6 策略节点已创建，则该命令直接用来进入该 IPv6 策略节点的视图。
命令用来删除已创建的 IPv6 策略或 IPv6 策略节点。
undo ipv6 policy-based-route【命令】
ipv6 policy-based-route policy-name [ deny | permit ] node node-number undo ipv6 policy-based-route policy-name [ deny | node node-number | permit ]【缺省情况】
不存在 IPv6 策略节点。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
policy-name：策略名，唯一标识一个 IPv6 策略，为 1～19 个字符的字符串，区分大小写。
deny：指定节点的匹配模式为拒绝模式。
permit：指定节点的匹配模式为允许模式。缺省匹配模式为 permit。
node-number： IPv6 策略节点。节点编号越小优先级越高，先对优先级高的节点进行匹配node操作。node-number 的取值范围为 0～255。
【使用指导】
删除 IPv6 策略之前，必须先取消该 IPv6 策略在所有接口上的应用，否则删除失败。

配置 命令时，如果指定了策略节点，将删除指定的节点；如果指定了节点模式，将按模式删undo除策略内所有与该模式匹配的所有节点；如果两者都未指定，将删除整个策略。
【举例】
\# 配置一个 IPv6 策略 aaa，其节点序列号为 10，匹配模式为 permit，并进入 IPv6 策略节点视图。
<Sysname> system-view [Sysname] ipv6 policy-based-route aaa permit node 10 [Sysname-pbr6-aaa-10]【相关命令】
• display ipv6 policy-based-route

##### 1.1.11 reset ipv6 policy-based-route statistics

reset ipv6 policy-based-route statistics 命令用来清除 IPv6 策略路由的统计信息。
【命令】
reset ipv6 policy-based-route statistics [ policy policy-name ]【视图】
用户视图【缺省用户角色】
network-admin【参数】
policy policy-name：清除指定 IPv6 策略的统计信息。policy-name 表示策略名，唯一标识一个 IPv6 策略，为 1～19 个字符的字符串，区分大小写。如果未指定本参数，则清除所有策略路由的统计信息。
【举例】
\# 清除所有配置 IPv6 策略的统计信息。
<Sysname> reset ipv6 policy-based-route statistics【相关命令】
• display ipv6 policy-based-route interface
• display ipv6 policy-based-route local

## 12-路由策略命令

目 录路由策略公共配置命令

### 1 路由策略

1路由策略

#### 1.1 路由策略公共配置命令

##### 1.1.1 apply as-path

命令用来配置 路由信息 属性。
apply as-path BGP AS_PATH命令用来恢复缺省情况。
undo apply as-path【命令】
apply as-path as-number&<1-32> [ replace ] undo apply as-path【缺省情况】
未配置 BGP 路由信息的 AS_PATH 属性。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
as-number&<1-32>：自治系统号，取值范围为 1～4294967295。&<1-32>表示前面的参数可以输入 1～32 次。
replace：替换原有 AS 号。如果未指定本参数，则在原 AS 路径前加入 AS 号。
【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。如果路由信息匹配已存在的编号为 的 路径访问列表，那么在原 路径前加入 号 200。
1 AS AS AS <Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match as-path 1 [Sysname-route-policy-policy1-10] apply as-path 200【相关命令】
•display ip as-path
•if-match as-path
•ip as-path

##### 1.1.2 apply comm-list delete

命令用来删除 BGP 路由信息的团体属性。
apply comm-list delete undo apply comm-list 命令用来恢复缺省情况。

【命令】
apply comm-list { comm-list-number | comm-list-name } delete undo apply comm-list【缺省情况】
没有删除 BGP 路由信息的团体属性。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
comm-list-number：团体属性列表号。
• 基本团体属性列表号的取值范围为 1～99；
• 高级团体属性列表号的取值范围为 100～199。
comm-list-name：团体属性列表名，为 1～63 个不全为数字的字符串，区分大小写。
【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。删除已存在的团体属性列表 1 中指定的 BGP 路由信息的团体属性。
<Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] apply comm-list 1 delete【相关命令】
• ip community-list

##### 1.1.3 apply community

命令用来配置 BGP 路由信息的团体属性。
apply community命令用来取消 BGP 路由信息的团体属性配置。
undo apply community【命令】
apply community { none | additive | { community-number&<1-32> | aa:nn&<1-32> | internet | no-advertise | no-export | no-export-subconfed } * [ additive ] } undo apply community [ none | additive | { community-number&<1-32> | aa:nn&<1-32> | internet | no-advertise | no-export | no-export-subconfed }
* [ additive ] ]【缺省情况】
未配置 路由信息的团体属性。
BGP【视图】
路由策略视图

【缺省用户角色】
network-admin【参数】
none：删除路由的团体属性。
community-number&<1-32>：团体序号，取值范围为 1～4294967295。&<1-32>表示前面的参数可以输入 1～32 次。
aa:nn&<1-32>：团体号，aa 和 的取值范围为 0～65535。&<1-32>表示前面的参数可以输入nn 1～32 次。
internet：预定义的团体属性。缺省情况下，所有的路由都具有 团体属性，可以被通internet告给所有的 BGP 对等体。
no-advertise：具有此属性的路由在收到后，不能被通告给任何其他的 BGP 对等体。
no-export：具有此属性的路由在收到后，不能被发布到本地 AS 之外。如果使用了联盟，则不能被发布到联盟之外，但可以发布给联盟中的其他子 AS。
no-export-subconfed：具有此属性的路由在收到后，不能被发布到本地 AS 之外，也不能发布到联盟中的其他子 AS。
additive：附加至原有路由的团体属性。
【举例】
创建一个名为 的路由策略，其节点序列号为 16，匹配模式为 permit。配置\# setcommunity BGP路由的团体属性为 no-export。
<Sysname> system-view [Sysname] route-policy setcommunity permit node 16 [Sysname-route-policy-setcommunity-16] apply community no-export【相关命令】
• if-match community
• ip community-list

##### 1.1.4 apply cost

apply cost 命令用来配置路由信息的路由开销。
undo apply cost 命令用来恢复缺省情况。
【命令】
apply cost [ + | - ] cost-value undo apply cost【缺省情况】
未配置路由信息的路由开销。
【视图】
路由策略视图【缺省用户角色】
network-admin

【参数】
+：增加开销值。
-：减少开销值。
cost-value：指定路由信息的路由开销，取值范围为 0～4294967295。
【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。如果匹配 OSPF 外部路由，那么设置该路由的路由开销为 120。
<Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match route-type external-type1or2 [Sysname-route-policy-policy1-10] apply cost 120

##### 1.1.5 apply cost-type

apply cost-type 命令用来配置路由信息的路由开销类型。
undo apply cost-type 命令用来恢复缺省情况。
【命令】
apply cost-type { external | internal | type-1 | type-2 } undo apply cost-type【缺省情况】
未配置路由开销类型。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
external：IS-IS 外部路由。
internal：IS-IS 内部路由或者设置 BGP 路由的 MED 值为下一跳的 IGP 度量值。
type-1：OSPF 的外部 Type-1 路由。
type-2：OSPF 的外部 Type-2 路由。
【使用指导】
apply cost-type internal 命令的作用：
• 应用于 IS-IS 路由：设置路由类型为 IS-IS 内部路由。
• 应用于 BGP 路由：路由器从 IBGP 对等体学到的路由在通告给 EBGP 对等体时，如果配置命令，则路由器会将向 EBGP 对等体通告的路由的 MED 值apply cost-type internal设置为该路由的下一跳的 度量值。
IGP

【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。如果匹配标记域为8 的路由，那么设置该路由的路由开销类型为 OSPF 的外部 Type-1 路由。
<Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match tag 8 [Sysname-route-policy-policy1-10] apply cost-type type-1

##### 1.1.6 apply extcommunity rt

apply extcommunity rt 命令用来配置 BGP 路由的 RT 扩展团体属性。
undo apply extcommunity rt 命令用来取消 BGP 路由的 RT 扩展团体属性配置。
【命令】
apply extcommunity { rt route-target }&<1-32> [ additive ] undo apply extcommunity [ { rt route-target }&<1-32> ]【缺省情况】
未配置 BGP 路由的 RT 扩展团体属性。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
{ rt route-target }&<1-32>：指定的 RT（Route Target，路由目标）扩展团体属性，为 3～21 个字符的字符串。&<1-32>表示前面的参数可以输入 1～32 次。
有三种形式，分别如下：
route-target
• 16 位自治系统号:32 位用户自定义数，例如：101:3。其中，自治系统号取值范围为 0～65535，用户自定义数取值范围为 0～4294967295。
32 位 IP 地址:16 位用户自定义数，例如：192.168.122.15:1。其中，用户自定义数取值范围
•为 0～65535。
位自治系统号:16 位用户自定义数，例如：70000:3。其中，自治系统号取值范围为 65536～
• 32 4294967295，用户自定义数取值范围为 0～65535。
additive：允许增加到已有的扩展团体中。
【使用指导】
执行 undo 命令时，如果未指定任何参数，则会删除所有的扩展团体属性。
【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10 ，匹配模式为 permit 。如果匹配已存在的编号为 的 路径访问列表，那么为 指定 扩展团体属性为 100:2，并允许将 扩展团1 AS BGP RT RT体属性增加到已有的扩展团体属性列表中。
<Sysname> system-view

[Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match as-path 1 [Sysname-route-policy-policy1-10] apply extcommunity rt 100:2 additive

##### 1.1.7 apply extcommunity soo

命令用来配置 BGP 路由的 SoO（Site of Origin，源站点）扩展团体apply extcommunity soo属性。
命令用来取消该配置。
undo apply extcommunity soo【命令】
apply extcommunity soo site-of-origin&<1-32> [ additive ] undo apply extcommunity [ soo ]【缺省情况】
未配置 BGP 路由的 SoO 扩展团体属性。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
site-of-origin&<1-32>：SoO 扩展团体属性，为 3～21 个字符的字符串。&<1-32>表示前面的参数可以输入 1～32 次。site-of-origin 有三种形式，分别如下：
• 16 位自治系统号:32 位用户自定义数，例如：101:3。其中，自治系统号取值范围为 0～65535，用户自定义数取值范围为 0～4294967295。
• 32 位 IP 地址:16 位用户自定义数，例如：192.168.122.15:1。其中，用户自定义数取值范围为 0～65535。
32 位自治系统号:16 位用户自定义数，例如：70000:3。其中，自治系统号取值范围为 65536～
•4294967295，用户自定义数取值范围为 0～65535。
additive：表示允许将 扩展团体属性增加到已有的扩展团体属性列表中。如果未配置本参数，SoO则表示替换已有的 SoO 扩展团体属性。
【使用指导】
执行 undo 命令时，如果未指定任何参数，则会删除所有的扩展团体属性。
【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。如果匹配已存在的编号为 的 路径访问列表，那么为 指定 扩展团体属性为 1:100，并允许将 扩展1 AS BGP SoO SoO团体属性增加到已有的扩展团体属性列表中。
<Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match as-path 1 [Sysname-route-policy-policy1-10] apply extcommunity soo 1:100 additive

##### 1.1.8 apply ip-precedence

apply ip-precedence 命令用来配置路由的 IP 优先级。
undo apply ip-precedence 命令用来恢复缺省情况。
【命令】
apply ip-precedence { value | clear } undo apply ip-precedence【缺省情况】
未配置路由的 IP 优先级。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
value：路由的 IP 优先级，取值范围是 0～7。
clear：清除路由的 IP 优先级。
【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。如果匹配前缀列表号 的路由，那么配置路由的 优先级为 3。
100 IP <Sysname> system-view [Sysname] ip prefix-list 100 permit 192.168.10.1 24 [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match ip address prefix-list 100 [Sysname-route-policy-policy1-10] apply ip-precedence 3

##### 1.1.9 apply isis

apply isis 命令用来配置引入路由到 IS-IS 某个级别的区域。
命令用来恢复缺省情况。
undo apply isis【命令】
apply isis { level-1 | level-1-2 | level-2 } undo apply isis【缺省情况】
未配置引入路由到 IS-IS 某个级别的区域。
【视图】
路由策略视图【缺省用户角色】
network-admin

【参数】
level-1：引入路由到 IS-IS 的 Level-1 区域。
level-1-2：引入路由到 IS-IS 的 Level-1 和 Level-2 区域。
level-2：引入路由到 IS-IS 的 Level-2 区域。
【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。如果匹配标记域为的路由，那么引入路由到 的 区域。
8 IS-IS Level-2 <Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match tag 8 [Sysname-route-policy-policy1-10] apply isis level-2

##### 1.1.10 apply l3-vni

apply l3-vni 命令用来配置 L3VNI。
undo apply l3-vni 命令用来恢复缺省情况。
【命令】
apply l3-vni vxlan-id undo apply l3-vni【缺省情况】
未配置 L3VNI。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
vxlan-id：L3VNI，取值范围为 0～16777215。
【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。如果匹配 L3VNI 值为 的 路由，那么配置路由的 值为 6。
8 BGP EVPN L3VNI <Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match l3-vni 8 [Sysname-route-policy-policy1-10] apply l3-vni 6

##### 1.1.11 apply local-preference

apply local-preference 命令用来配置 BGP 路由信息的本地优先级。
undo apply local-preference 命令用来恢复缺省情况。

【命令】
apply local-preference preference undo apply local-preference【缺省情况】
未配置 BGP 路由信息的本地优先级。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
preference：BGP 路由信息的本地优先级，取值范围为 0～4294967295。
【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。如果匹配已存在的编号为 1 的 AS 路径访问列表，那么配置该 BGP 路由的本地优先级为 130。
<Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match as-path 1 [Sysname-route-policy-policy1-10] apply local-preference 130

##### 1.1.12 apply origin

apply origin 命令用来配置 BGP 路由信息的 ORIGIN 属性。
undo apply origin 命令用来恢复缺省情况。
【命令】
apply origin { egp as-number | igp | incomplete } undo apply origin【缺省情况】
未配置 BGP 路由信息的 ORIGIN 属性。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
egp as-number：设定 BGP 路由信息的来源为外部路由。as-number 表示指定外部路由的自治系统号，取值范围为 1 ～ 4294967295 。
igp：设定 BGP 路由信息的来源为内部路由。
incomplete：设定 BGP 路由信息的来源为未知来源。

【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。如果匹配已存在的编号为 1 的 AS 路径访问列表，那么设置该 BGP 路由的路由源为 IGP。
<Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match as-path 1 [Sysname-route-policy-policy1-10] apply origin igp

##### 1.1.13 apply preference

apply preference 命令用来配置路由协议的优先级。
undo apply preference 命令用来恢复缺省情况。
【命令】
apply preference preference undo apply preference【缺省情况】
未配置路由协议的优先级。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
preference：路由的优先级，取值范围为 1～255。
【使用指导】
如果路由协议已经用命令 配置了优先级，再用 命令修改路由preference apply preference协议的优先级，则这些匹配策略的路由采用 命令修改的优先级，其它路由的apply preference优先级均采用 preference 命令所设的值。
【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。如果匹配 OSPF 外部路由，那么设置该路由协议的优先级为 90。
<Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match route-type external-type1or2 [Sysname-route-policy-policy1-10] apply preference 90

##### 1.1.14 apply preferred-value

apply preferred-value 命令用来配置 BGP 路由信息的首选值。
undo apply preferred-value 命令恢复缺省情况。

【命令】
apply preferred-value preferred-value undo apply preferred-value【缺省情况】
未配置 BGP 路由信息的首选值。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
preferred-value：首选值，取值范围为 0～65535。
【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。如果匹配已存在的编号为 1 的 AS 路径访问列表，那么设置该 BGP 路由的首选值为 66。
<Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match as-path 1 [Sysname-route-policy-policy1-10] apply preferred-value 66

##### 1.1.15 apply prefix-priority

apply prefix-priority 命令用来配置路由的收敛优先级。
undo apply prefix-priority 命令用来恢复缺省情况。
【命令】
apply prefix-priority { critical | high | medium } undo apply prefix-priority【缺省情况】
未配置路由的收敛优先级，即路由的收敛优先级为低（Low）。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
critical：路由的收敛优先级为关键。
high：路由的收敛优先级为高。
medium：路由的收敛优先级中。

【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。如果匹配已存在的地址前缀列表 abc，那么设置该路由的收敛优先级为关键。
<Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match ip address prefix-list abc [Sysname-route-policy-policy1-10] apply prefix-priority critical

##### 1.1.16 apply tag

apply tag 命令用来配置 IGP 路由信息的标记。
undo apply tag 命令用来恢复缺省情况。
【命令】
apply tag tag-value undo apply tag【缺省情况】
未配置 IGP 路由信息的标记。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
tag-value：指定路由信息的标记值，取值范围为 0～4294967295。
【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。配置 IGP 路由信息的标记为 100。
<Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] apply tag 100

##### 1.1.17 apply traffic-index

命令用来配置 BGP 路由信息的流量索引。
apply traffic-index命令用来恢复缺省情况。
undo apply traffic-index【命令】
apply traffic-index { value | clear } undo apply traffic-index【缺省情况】
未配置 路由信息的流量索引。
BGP

【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
value：流量索引值，取值范围为 1～64。
clear：清除路由的流量索引值。
【举例】
创建一个名为 的路由策略，其节点序列号为 10，匹配模式为 permit。如果匹配扩展团体\# policy1列表号 100 的 BGP 路由，那么配置路由的流量索引值为 6。
<Sysname> system-view [Sysname] ip extcommunity-list 100 permit rt 100:100 [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match extcommunity 100 [Sysname-route-policy-policy1-10] apply traffic-index 6

##### 1.1.18 continue

命令用来配置下一个执行节点。
continue undo continue 命令用来恢复缺省情况。
【命令】
continue [ node-number ] undo continue【缺省情况】
未配置下一个执行节点。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
node-number：标识本命令会跳转到的节点索引，取值范围为 0～65535。
【使用指导】
下一个执行节点序列号必须大于当前节点序列号。
【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10 ，匹配模式为 permit 。定义 continue 子句，配置下一个执行节点序列号为 20。
<Sysname> system-view [Sysname] route-policy policy1 permit node 10

[Sysname-route-policy-policy1-10] continue 20

##### 1.1.19 display ip as-path

display ip as-path 命令用来显示 BGP AS 路径过滤列表信息。
【命令】
display ip as-path [ as-path-number ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
as-path-number：AS 路径过滤列表号，取值范围为 1～256。如果未指定本参数，将显示所有已配置的 BGP AS 路径过滤列表信息。
【举例】
\# 显示列表号为 1 的 BGP AS 路径列表信息。
<Sysname> display ip as-path 1 ListID Mode Expression 1 Permit 2表1-1 display ip as-path 命令显示信息描述表字段 描述ListID AS路径列表号匹配模式，有两种取值：
• Permit：表示允许Mode
• Deny：表示拒绝Expression 匹配的AS路径正则表达式

##### 1.1.20 display ip community-list

命令用来显示 BGP 团体属性列表信息。
display ip community-list【命令】
display ip community-list [ basic-community-list-number | adv-community-list-number | name comm-list-name ]【视图】
任意视图【缺省用户角色】
network-admin

network-operator【参数】
basic-community-list-number：为基本团体属性列表号，取值范围为 1～99。
adv-community-list-number：为高级团体属性列表号，取值范围为 100～199。
comm-list-name：团体属性列表名，为 1～63 个不全为数字的字符串，区分大小写。
name【使用指导】
如果未指定团体属性列表号或团体属性列表名，将显示所有已配置的 BGP 团体属性列表信息。
【举例】
\# 显示所有的 BGP 团体属性列表信息。
<Sysname> display ip community-list Community List Basic aaa Permit Community List Advanced bbb Permit 3333表1-2 display ip community-list 命令显示信息描述表字段 描述Community List Basic 基本团体属性列表Community List Advanced 高级团体属性列表匹配模式，有两种取值：
permit • Permit：表示允许
• Deny：表示拒绝

##### 1.1.21 display ip extcommunity-list

命令用来显示 BGP 扩展团体属性列表信息。
display ip extcommunity-list【命令】
display ip extcommunity-list [ ext-comm-list-number ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
ext-comm-list-number：扩展团体属性列表号，取值范围为 1 ～ 199 。如果未指定本参数，将显示所有已配置的 扩展团体属性列表信息。
BGP【举例】
显示列表号为 的 扩展团体属性列表信息。
\# 1 BGP

<Sysname> display ip extcommunity-list 1 Extended Community List Number 1 Permit rt: 9:6 Permit soo: 9:6表1-3 display ip extcommunity-list 命令显示信息描述表字段 描述Extended Community List扩展团体属性列表Number匹配模式，有两种取值：
permit • Permit：表示允许
• Deny：表示拒绝RT（Route Target，路由目标）扩展团体属性rt soo SoO（Site of Origin，源站点）扩展团体属性

##### 1.1.22 display route-policy

display route-policy 命令用来显示配置的路由策略信息。
【命令】
display route-policy [ name route-policy-name ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
route-policy-name：指定显示的路由策略名，为 1～63 个字符的字符串，区分大小写。
name如果未指定本参数，将显示所有已配置的路由策略信息。
【举例】
\# 显示名为 policy1 的路由策略信息。
<Sysname> display route-policy name policy1 Route-policy: policy1 Permit : 1 if-match cost 10 continue: next node 11 apply preference 10表 1-4 display route-policy 命令显示信息描述表字段 描述Route-policy 路由策略名称

字段 描述匹配模式，有两种取值：
•permit Permit：表示允许
• Deny：表示拒绝if-match if-match子句，配置的匹配条件continue continue字句，配置下一个执行节点apply apply子句，如满足匹配条件，则要执行的动作

##### 1.1.23 if-match as-path

if-match as-path 命令用来配置 BGP 路由信息的 AS 路径域的匹配条件。
undo if-match as-path 命令用来取消 BGP 路由信息的 AS 路径域的匹配条件的配置。
【命令】
if-match as-path as-path-number&<1-32> undo if-match as-path [ as-path-number&<1-32> ]【缺省情况】
未配置 BGP 路由信息的 AS 路径域的匹配条件。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
as-path-number&<1-32>：为 AS 路径过滤列表号，取值范围为 1～256。&<1-32>表示前面的参数可以输入 1～32 次。
【举例】
\# 首先配置一个编号为 2 的 as-path，允许自治系统号包含 200 和 300 的路由信息通过。然后创建一个名为 test 的路由策略，该路由策略编号为 10 的节点定义了一条 if-match 子句，它引用的是先前定义的 as-path。
<Sysname> system-view [Sysname] ip as-path 2 permit _*200.*300 [Sysname] route-policy test permit node 10 [Sysname-route-policy-policy1-10] if-match as-path 2【相关命令】
• apply as-path
• ip as-path

##### 1.1.24 if-match community

if-match community 命令用来配置 BGP 路由信息的团体属性的匹配条件。
undo if-match community 命令用来取消 BGP 路由信息的团体属性的匹配条件的配置。
【命令】
if-match community { { basic-community-list-number | name comm-list-name } [ whole-match ] | adv-community-list-number }&<1-32> undo if-match community [ { basic-community-list-number | name comm-list-name } [ whole-match ] | adv-community-list-number ]&<1-32>【缺省情况】
未配置 BGP 路由信息的团体属性的匹配条件。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
basic-community-list-number：为基本团体属性列表号，取值范围为 1～99。
adv-community-list-number：为高级团体属性列表号，取值范围为 100～199。
comm-list-name：团体属性列表名，为 1～63 个不全为数字的字符串，区分大小写。
whole-match：为确切匹配，即所有团体而且仅有这些团体必须出现。
&<1-32>：表示前面的参数可以输入 1～32 次。
【举例】
首先配置一个编号为 的 community-list，允许包含团体号 和 的路由信息。然后创建一\# 1 100 200个名为 test 的路由策略，该路由策略编号为 10 的节点定义了一条 if-match 子句，它引用的是先前定义的 community-list。
<Sysname> system-view [Sysname] ip community-list 1 permit 100 200 [Sysname] route-policy test permit node 10 [Sysname-route-policy-test-10] if-match community 1【相关命令】
• apply community
• ip community-list

##### 1.1.25 if-match cost

if-match cost 命令用来配置路由信息的路由开销的匹配条件。
undo if-match cost 命令用来恢复缺省情况。
【命令】
if-match cost cost-value

undo if-match cost【缺省情况】
未配置路由信息的路由开销的匹配条件。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
cost-value：路由开销，取值范围为 0～4294967295。
【举例】
创建一个名为 的路由策略，其节点序列号为 10，匹配模式为 permit。定义一条\# policy1 if-match子句，允许路由开销为 8 的路由信息通过。
<Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match cost 8

##### 1.1.26 if-match extcommunity

if-match extcommunity 命令用来配置 BGP 路由信息的扩展团体属性的匹配条件。
命令用来取消 路由信息的扩展团体属性的匹配条件的配undo if-match extcommunity BGP置。
【命令】
if-match extcommunity ext-comm-list-number&<1-32> undo if-match extcommunity [ ext-comm-list-number&<1-32> ]【缺省情况】
未配置 BGP 路由信息的扩展团体属性的匹配条件。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
ext-comm-list-number&<1-32>：扩展团体属性列表号，取值范围为 1～199。&<1-32>表示前面的参数可以输入 1～32 次。
【举例】
创建一个名为 的路由策略，其节点序列号为 10，匹配模式为 permit。定义一条\# policy1 if-match子句，匹配已存在的扩展团体列表号 100 和 150 定义的扩展团体属性的路由。
<Sysname> system-view [Sysname] ip extcommunity-list 100 permit rt 100:100

[Sysname] ip extcommunity-list 150 permit rt 150:150 [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match extcommunity 100 150【相关命令】
• apply extcommunity
• ip extcommunity-list

##### 1.1.27 if-match interface

命令用来配置路由信息的出接口的匹配条件。
if-match interface命令用来取消路由信息的出接口的匹配条件的配置。
undo if-match interface【命令】
if-match interface { interface-type interface-number }&<1-16> undo if-match interface [ interface-type interface-number ]&<1-16>【缺省情况】
未配置路由信息的出接口的匹配条件。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
interface-number：指定接口类型和编号。
interface-type &<1-16>：表示前面的参数可以输入 1～16 次。
【使用指导】
将路由策略应用到 BGP 时，BGP 协议不支持配置路由信息的出接口的匹配条件。
【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。定义一条 if-match子句，匹配出接口为 Vlan-interface1 的路由信息。
<Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match interface vlan-interface 1

##### 1.1.28 if-match l3-vni

命令用来配置 L3VNI 的匹配条件。
if-match l3-vni undo if-match l3-vni 命令用来恢复缺省情况。
【命令】
if-match l3-vni vxlan-id undo if-match l3-vni

【缺省情况】
未配置 L3VNI 的匹配条件。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
vxlan-id：L3VNI，取值范围为 0～16777215。
【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。定义一条 if-match子句，匹配 L3VNI 值为 8 的 BGP EVPN 路由。
<Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match l3-vni 8

##### 1.1.29 if-match local-preference

if-match local-preference 命令用来配置 BGP 路由信息的本地优先级的匹配条件。
undo if-match local-preference 命令用来恢复缺省情况。
【命令】
if-match local-preference preference undo if-match local-preference【缺省情况】
未配置 路由信息的本地优先级的匹配条件。
BGP【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
preference：BGP 路由信息的本地优先级，取值范围为 0～4294967295。
【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。定义一条 if-match子句，允许 BGP 路由信息的本地优先级为 2 的路由信息通过。
<Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match local-preference 2

##### 1.1.30 if-match route-type

if-match route-type 命令用来配置路由信息类型的匹配条件。
undo if-match route-type 命令用来取消路由信息类型的匹配条件的配置。
【命令】
if-match route-type { bgp-evpn-imet | bgp-evpn-ip-prefix | bgp-evpn-mac-ip external-type1 | | external-type1or2 | external-type2 | internal | is-is-level-1 | is-is-level-2 | nssa-external-type1 | nssa-external-type1or2 | nssa-external-type2 } * undo if-match route-type [ bgp-evpn-imet | bgp-evpn-ip-prefix | bgp-evpn-mac-ip | external-type1 | external-type1or2 | external-type2 | internal | is-is-level-1 | is-is-level-2 | nssa-external-type1 | nssa-external-type1or2 | nssa-external-type2 ] *【缺省情况】
未配置路由信息的类型的匹配条件。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
bgp-evpn-imet：BGP EVPN 的 IMET（Inclusive Multicast Ethernet Tag Route，包含性组播以太网标签路由）路由。
bgp-evpn-ip-prefix：BGP EVPN 的 IP 前缀路由。
bgp-evpn-mac-ip：BGP EVPN 的 MAC/IP 发布路由。
external-type1：OSPF Type1 的外部路由。
external-type1or2：OSPF 外部路由。
external-type2：OSPF Type2 的外部路由。
internal：内部路由（包括 OSPF 区域间和区域内路由）。
is-is-level-1：IS-IS 的 路由。
Level-1 is-is-level-2：IS-IS 的 路由。
Level-2 nssa-external-type1：OSPF 的外部路由。
NSSA Type1 nssa-external-type1or2：OSPF 的外部路由。
NSSA nssa-external-type2：OSPF 的外部路由。
NSSA Type2【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10 ，匹配模式为 permit 。定义一条 if-match子句，匹配 internal 类型的路由。
<Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match route-type internal

##### 1.1.31 if-match rpki

if-match rpki 命令用来配置 BGP RPKI 验证结果的匹配条件。
undo if-match rpki 命令用来恢复缺省情况。
【命令】
if-match rpki { invalid | not-found | valid } undo if-match rpki【缺省情况】
未配置 BGP RPKI 验证结果的匹配条件。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
invalid：匹配 BGP RPKI 验证结果为 Invalid 的路由。
not-found：匹配 BGP RPKI 验证结果为 Not-found 的路由。
valid：匹配 BGP RPKI 验证结果为 Valid 的路由。
【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。定义一条 if-match子句，允许 验证结果为 的路由信息通过。
BGP RPKI Valid <Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match rpki valid

##### 1.1.32 if-match tag

命令用来配置 IGP 路由信息标记的匹配条件。
if-match tag命令用来恢复缺省情况。
undo if-match tag【命令】
tag-value if-match tag undo if-match tag【缺省情况】
未配置 IGP 路由信息标记的匹配条件。
【视图】
路由策略视图【缺省用户角色】
network-admin

【参数】
tag-value：指定要求的标记值，取值范围为 0～4294967295。
【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。定义一条 if-match子句，匹配标记为 的 路由信息。
8 IGP <Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match tag 8

##### 1.1.33 ip as-path

命令用来配置一个 AS 路径过滤列表。
ip as-path命令用来删除指定的 AS 路径过滤列表。
undo ip as-path【命令】
ip as-path as-path-number { deny | permit } regular-expression undo ip as-path as-path-number [ regular-expression | deny | permit ]【缺省情况】
不存在 AS 路径过滤列表。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
as-path-number：指定的 路径过滤列表号，取值范围为 1～256。
AS deny：指定 AS 路径过滤列表的匹配模式为拒绝模式。
permit：指定 AS 路径过滤列表的匹配模式为允许模式。
regular-expression：AS 路径正则表达式，为 1～63 个字符的字符串。
【使用指导】
协议的路由信息中，包含一个 路径域，在 协议交换路由信息的过程中，该路由所经BGP AS BGP过的所有 AS 都会记录在这个域中。例如^200.*100$，表示匹配所有 AS 200 开始、以 AS 100 结束的 AS 路径域。AS 路径正则表达式所用到的特殊字符及其含义，请参见“基础配置指导”中的“CLI”。
【举例】
\# 配置序号为 1 的 AS 路径过滤列表，允许 AS_PATH 以 10 开头的路由信息通过。
<Sysname> system-view [Sysname] ip as-path 1 permit ^10【相关命令】
• apply as-path
• display ip as-path

• if-match as-path

##### 1.1.34 ip community-list

命令用来配置一个团体属性列表。
ip community-list命令用来删除指定的团体属性列表。
undo ip community-list【命令】
ip community-list { basic-comm-list-num | basic basic-comm-list-name } { deny | permit } [ community-number&<1-32> | aa:nn&<1-32> ] [ internet | no-advertise | no-export | no-export-subconfed ] * undo ip community-list { basic-comm-list-num | basic basic-comm-list-name } [ deny | permit ] [ community-number&<1-32> | aa:nn&<1-32> ] [ internet | no-advertise | no-export | no-export-subconfed ] * ip community-list { adv-comm-list-num | advanced adv-comm-list-name } { deny | permit } regular-expression undo ip community-list { adv-comm-list-num | advanced adv-comm-list-name } [ deny | permit ] [ regular-expression ]【缺省情况】
不存在团体属性列表。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
basic-comm-list-num：基本团体属性列表号，取值范围为 1～99。
basic basic-comm-list-name：标识基本团体属性名称。basic-comm-list-name 为 1～63 个不全为数字的字符串，区分大小写。
advanced adv-comm-list-name：标识高级团体属性名称。adv-comm-list-name 为 1～63个不全为数字的字符串，区分大小写。
adv-comm-list-num：高级团体属性列表号，取值范围为 100～199。
regular-expression：指定高级团体属性的正则表达式，为 1～63 个字符的字符串。有关正则表达式的详细介绍，请参见“基础配置指导”中的“CLI”。
deny：指定团体属性列表的匹配模式为拒绝模式。
permit：指定团体属性列表的匹配模式为允许模式。
community-number&<1-32>：团体序号，取值范围为 1～4294967295。&<1-32>表示前面的参数可以输入 1 ～ 32 次。
aa:nn&<1-32>：团体号，aa 和 的取值范围为 0～65535。&<1-32>表示前面的参数可以输入nn 1～32 次。

internet：预定义的团体属性。缺省情况下，所有的路由都具有 团体属性，可以被通internet告给所有的 对等体。
BGP no-advertise：具有此属性的路由在收到后，不能被通告给任何其他的 对等体。
BGP no-export：具有此属性的路由在收到后，不能被发布到本地 之外。如果使用了联盟，则不能AS被发布到联盟之外，但可以发布给联盟中的其他子 AS。
no-export-subconfed：具有此属性的路由在收到后，不能被发布到本地 AS 之外，也不能发布到联盟中的其他子 AS。
【举例】
\# 配置序号为 1 的基本团体属性列表，允许 团体属性的路由信息通过。
internet <Sysname> system-view [Sysname] ip community-list 1 permit internet配置序号为 的高级团体属性列表，允许团体属性内容以“10”开头的路由信息通过。
\# 100 <Sysname> system-view [Sysname] ip community-list 100 permit ^10【相关命令】
• apply comm-list delete
• apply community
• display ip community-list
• if-match community

##### 1.1.35 ip extcommunity-list

ip extcommunity-list 命令用来配置一个扩展团体属性列表。
undo ip extcommunity-list 命令用来删除指定的扩展团体属性列表。
【命令】
ip extcommunity-list ext-comm-list-number { deny | permit } { rt route-target | soo site-of-origin }&<1-32> undo ip extcommunity-list ext-comm-list-number [ { deny | permit } [ rt route-target | soo site-of-origin ]&<1-32> ]【缺省情况】
不存在扩展团体属性列表。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
ext-comm-list-number：扩展团体属性列表号，取值范围为 1～199。
deny：指定扩展团体属性列表的匹配模式为拒绝模式。
permit：指定扩展团体属性列表的匹配模式为允许模式。

route-target：指定的 RT（Route Target，路由目标）扩展团体属性，为 3～21 个字符的字rt符串。&<1-32>表示前面的参数可以输入 1～32 次。
site-of-origin：指定的 SoO（Site Origin，源站点）扩展团体属性，为 3～21 个字符soo of的字符串。&<1-32>表示前面的参数可以输入 1～32 次。
route-target 和 site-of-origin 有三种形式，分别如下：
• 16 位自治系统号:32 位用户自定义数，例如：101:3。其中，自治系统号取值范围为 0～65535，用户自定义数取值范围为 0～4294967295。
• 32 位 IP 地址:16 位用户自定义数，例如：192.168.122.15:1。其中，用户自定义数取值范围为 0～65535。
• 32 位自治系统号:16 位用户自定义数，例如：70000:3。其中，自治系统号取值范围为 65536～4294967295，用户自定义数取值范围为 0～65535。
【举例】
\# 配置序号为 1 的扩展团体属性列表，允许 RT 为 200:200 的路由信息通过。
<Sysname> system-view [Sysname] ip extcommunity-list 1 permit rt 200:200 \# 配置序号为 2 的扩展团体属性列表，允许 SoO 为 100:100 的路由信息通过。
<Sysname> system-view [Sysname] ip extcommunity-list 2 permit soo 100:100【相关命令】
• apply extcommunity
• display ip extcommunity-list
• if-match extcommunity

##### 1.1.36 route-policy

命令用来创建路由策略，并进入该路由策略视图。如果指定的路由策略已经存在，route-policy则直接进入该路由策略视图。
命令用来删除指定的路由策略。
undo route-policy【命令】
route-policy route-policy-name { deny | permit } node node-number undo route-policy route-policy-name [ deny | permit ] [ node node-number ]【缺省情况】
不存在路由策略。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
route-policy-name：指定路由策略名，为 1～63 个字符的字符串，区分大小写。

deny：指定所定义的路由策略节点的匹配模式为拒绝模式。当路由项满足该节点的所有 if-match子句时被拒绝通过该节点的过滤，并且不会进行下一个节点的匹配；如果路由项不满足该节点的if-match 子句，将进入下一个节点继续匹配。
permit：指定所定义的路由策略节点的匹配模式为允许模式。当路由项满足该节点的所有 if-match子句时被允许通过该节点的过滤并执行该节点的 apply 子句，如路由项不满足该节点的 if-match 子句，将继续匹配该路由策略的下一个节点。
node-number：标识路由策略中的一个节点索引，当该路由策略用于路由信息过滤时，node node-number 小的节点先被匹配，取值范围为 0～65535。
【使用指导】
路由策略用于路由信息过滤。一个路由策略由若干节点组成，每一节点由一些 if-match 子句和 apply子句组成。if-match 子句定义该节点的匹配规则，apply 子句定义通过该节点过滤后进行的动作。节点的 子句之间的过滤关系是“与”的关系，即必须满足该节点的所有 子句。路由if-match if-match策略节点之间的过滤关系是“或”的关系，即通过一个节点的过滤就意味着通过该路由策略的过滤。
若没有通过任一节点的过滤，则表示没有通过该路由策略的过滤。
【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit，并进入路由策略视图。
<Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10]【相关命令】
• display route-policy

#### 1.2 IPv4路由策略配置命令

##### 1.2.1 apply fast-reroute

命令用来配置快速重路由备份。
apply fast-reroute命令用来恢复缺省情况。
undo apply fast-reroute【命令】
apply fast-reroute { backup-interface interface-type interface-number [ backup-nexthop ip-address ] | backup-nexthop ip-address } undo apply fast-reroute【缺省情况】
未配置快速重路由备份。
【视图】
路由策略视图【缺省用户角色】
network-admin

【参数】
backup-interface interface-type interface-number：备份出接口。对于备份出接口为非 P2P 类型的接口时（包括 NBMA 类型接口或广播类型接口），必须同时指定其对应的备份下一跳地址。interface-type 为指定的接口类型和编号。
interface-number ip-address：备份下一跳地址。
backup-nexthop【举例】
\# 创建一个名为 policy1 的路由策略，为到达目的地 100.1.1.0/24 的路由配置备份出接口为Vlan-interface1，备份下一跳地址为 193.1.1.8。
<Sysname> system-view [Sysname] ip prefix-list abc index 10 permit 100.1.1.0 24 [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match ip address prefix-list abc [Sysname-route-policy-policy1-10] apply fast-reroute backup-interface vlan-interface 1 backup-nexthop 193.1.1.8

##### 1.2.2 apply ip-address next-hop

命令用来配置 IPv4 路由信息的下一跳地址。
apply ip-address next-hop命令用来恢复缺省情况。
undo apply ip-address next-hop【命令】
apply ip-address next-hop ip-address [ public | vpn-instance vpn-instance-name ] undo apply ip-address next-hop【缺省情况】
未配置 IPv4 路由信息的下一跳地址。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
ip-address：下一跳 地址。
IP public：指定公网。
vpn-instance-name：指定 实例的信息。vpn-instance-name 表示vpn-instance VPN MPLS L3VPN 的 VPN 实例名称，为 1～31 个字符的字符串，区分大小写。
【使用指导】
当引入路由时，使用本命令设置下一跳地址无效。
如果未指定参数 public 或 vpn-instance vpn-instance-name，则表示下一跳地址为公网地址。

【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。如果匹配前缀列表号 100 的路由，那么设置路由信息的下一跳地址为 193.1.1.8。
<Sysname> system-view [Sysname] ip prefix-list 100 permit 192.168.10.1 24 [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match ip address prefix-list 100 [Sysname-route-policy-policy1-10] apply ip-address next-hop 193.1.1.8

##### 1.2.3 display ip prefix-list

命令用来显示 地址前缀列表的统计信息。
display ip prefix-list IPv4【命令】
display ip prefix-list [ name prefix-list-name ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
prefix-list-name：指定显示的地址前缀列表名，为 1～63 个字符的字符串，区分大小写。
name如果未指定本参数，将显示所有已配置的地址前缀列表的统计信息。
【举例】
\# 显示名为 abc 的地址前缀列表的统计信息。
<Sysname> display ip prefix-list name abc Prefix-list: abc Permitted 0 Denied 0 index: 10 Deny 6.6.6.0/24 ge 26 le 28表1-5 display ip prefix-list 命令显示信息描述表字段 描述Prefix-list 地址前缀列表的名称Permitted 符合匹配条件的路由个数不符合匹配条件的路由个数Denied index 地址前缀列表的内部序列号匹配模式，有两种取值：
• Permit：表示允许deny
• Deny：表示拒绝
6.6.6.0/24 匹配的IP地址和掩码长度

字段 描述ge 即greater-equal，匹配的IP地址掩码长度的下限值le 即less-equal，匹配的IP地址掩码长度的上限值【相关命令】
• ip prefix-list
• reset ip prefix-list

##### 1.2.4 if-match ip

命令用来配置 的路由信息的匹配条件。
if-match ip IPv4命令用来取消 IPv4 的路由信息的匹配条件的配置。
undo if-match ip【命令】
if-match ip { address | next-hop | route-source } { acl ipv4-acl-number | prefix-list prefix-list-name } undo if-match ip { address | next-hop | route-source } [ acl | prefix-list ]【缺省情况】
未配置 IPv4 的路由信息的匹配条件。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
address：匹配 IPv4 路由信息的目的地址。
next-hop：匹配下一跳地址。
route-source：匹配路由发布的源地址。仅对 BGP 路由有效，对 IGP 路由无效，其识别匹配的是 IP 路由表详细信息中的 "Neighbor" 字段。
acl ipv4-acl-number：指定用于过滤的 ACL 号。对于 address，ipv4-acl-number 的取值范围为 2000～3999；对于 和 route-source，ipv4-acl-number 的取值范围为next-hop 2000～2999。
prefix-list-name：指定用于过滤的地址前缀列表名称，为 1～63 个字符的字prefix-list符串，区分大小写。
【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。定义一个 if-match子句，允许下一跳地址匹配已存在的地址前缀列表 p1 的路由信息通过。
<Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match ip next-hop prefix-list p1

##### 1.2.5 ip prefix-list

ip prefix-list 命令用来配置一个 IPv4 地址前缀列表或表项。
undo ip prefix-list 命令用来删除指定的 IPv4 地址前缀列表或其某个表项。
【命令】
ip prefix-list prefix-list-name [ index index-number ] { deny | permit } ip-address mask-length [ greater-equal min-mask-length ] [ less-equal max-mask-length ] undo ip prefix-list prefix-list-name [ index index-number ]【缺省情况】
不存在 IPv4 地址前缀列表。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
prefix-list-name：指定 地址前缀列表名，为 1～63 个字符的字符串，区分大小写。
IPv4 index-number：标识 地址前缀列表中的一条表项，index-number 小的表项先被匹配，取IPv4值范围为 1～65535。如果未指定本参数，该序号值按照配置先后顺序依次递增，每次加 10，第一个序号值为 10。
deny：指定所定义的 IPv4 地址前缀列表表项的匹配模式为拒绝模式。在该模式下，如果过滤的 IPv4地址在定义的范围内，则不能通过过滤，并且不进行下一节点的匹配；否则，进行下一节点的匹配。
permit：指定所定义的 IPv4 地址前缀列表表项的匹配模式为允许模式。在该模式下，如果过滤的地址在定义的范围内，则通过过滤，不进行下一个节点的匹配；否则，进行下一节点的匹配。
IPv4 mask-length：指定 地址前缀和前缀长度，mask-length 的取值范围为 0～ip-address IPv4 32。
greater-equal min-mask-length、less-equal max-mask-length：如果 IPv4 地址和前缀长度都已匹配，则使用该参数来指定地址前缀长度范围。 greater-equal 表示大于等于，表示小于等于。前缀长度范围可以表达为 <= <= less-equal mask-length min-mask-length。 如 果 只 指 定 时 ， 则 前 缀 长 度 范 围 为max-mask-length <= 32 min-mask-length [ min-mask-length ， 32 ] ； 如 果 只 指 定 max-mask-length 时 ， 则 前 缀 长 度 范 围 为， ； 如 果 二 者 都 指 定 ， 则 前 缀 长 度 范 围 为[ mask-length max-mask-length ] min-mask-length，max-mask-length ]。
[【使用指导】
IPv4 地址前缀列表用于 IPv4 地址的过滤。一个 IPv4 地址前缀列表可以有若干条表项，每一表项指定一个地址前缀范围。表项之间的过滤关系是“或”的关系，即通过一条表项的过滤就意味着通过该 IPv4 地址前缀列表的过滤。若没有通过任一表项的过滤，则不能通过该 IPv4 地址前缀列表的过滤。

如果将 指定为 0.0.0.0 0，则只匹配缺省路由。如果需要匹配所有路ip-address mask-length由，则应配置为 32。
0.0.0.0 0 less-equal【举例】
\# 定义一条名为 p1 的 IPv4 地址前缀列表，只允许 10.0.0.0/8 网段的，掩码长度为 17 或 18 的路由通过。
<Sysname> system-view [Sysname] ip prefix-list p1 permit 10.0.0.0 8 greater-equal 17 less-equal 18【相关命令】
• display ip prefix-list
• reset ip prefix-list

##### 1.2.6 reset ip prefix-list

命令用来清除 地址前缀列表的统计信息。
reset ip prefix-list IPv4【命令】
reset ip prefix-list [ prefix-list-name ]【视图】
用户视图【缺省用户角色】
network-admin【参数】
prefix-list-name：指定地址前缀列表的名称，为 1～63 个字符的字符串，区分大小写。如果未指定本参数，将清除所有的 IPv4 地址前缀列表的统计信息。
【举例】
\# 清除 IPv4 地址前缀列表 abc 的统计信息。
<Sysname> reset ip prefix-list abc【相关命令】
• display ip prefix-list
• ip prefix-list

#### 1.3 IPv6路由策略配置命令

##### 1.3.1 apply ipv6 fast-reroute

命令用来配置快速重路由备份。
apply ipv6 fast-reroute命令用来恢复缺省情况。
undo apply ipv6 fast-reroute【命令】
apply ipv6 fast-reroute { backup-interface interface-type interface-number [ backup-nexthop ipv6-address ] | backup-nexthop ipv6-address }

undo apply ipv6 fast-reroute【缺省情况】
未配置快速重路由备份。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
interface-number：备份出接口。对于备份出接口backup-interface interface-type为非 类型的接口时（包括 类型接口或广播类型接口），必须同时指定其对应的备份下一P2P NBMA跳地址。interface-type interface-number 为指定的接口类型和编号。
backup-nexthop ipv6-address：备份下一跳 IPv6 地址。
【举例】
\# 创建一个名为 policy1 的路由策略，为到达目的地 100::1/64 的路由配置备份下一跳地址为 1::1/64。
<Sysname> system-view [Sysname] ipv6 prefix-list abc index 10 permit 100::1 64 [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match ipv6 address prefix-list abc [Sysname-route-policy-policy1-10] apply ipv6 fast-reroute backup-nexthop 1::1

##### 1.3.2 apply ipv6 next-hop

命令用来配置 IPv6 路由信息的下一跳地址。
apply ipv6 next-hop命令用来恢复缺省情况。
undo apply ipv6 next-hop【命令】
apply ipv6 next-hop ipv6-address undo apply ipv6 next-hop【缺省情况】
未配置 路由信息的下一跳地址。
IPv6【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
ipv6-address：指定下一跳 IPv6 地址。
【使用指导】
引入路由时，使用 命令设置下一跳地址无效。
apply ipv6 next-hop

【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。如果匹配前缀列表号 100 的路由，那么设置路由信息的下一跳地址为 3ffe:506::1。
<Sysname> system-view [Sysname] ipv6 prefix-list 100 permit 2::2 64 [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match ipv6 address prefix-list 100 [Sysname-route-policy-policy1-10] apply ipv6 next-hop 3ffe:506::1

##### 1.3.3 display ipv6 prefix-list

命令用来显示 地址前缀列表的统计信息。
display ipv6 prefix-list IPv6【命令】
display ipv6 prefix-list [ name prefix-list-name ]【视图】
任意视图【缺省用户角色】
network-admin network-operator【参数】
prefix-list-name：指定 IPv6 地址前缀列表的名称，为 1～63 个字符的字符串，区分大name小写。如果未指定本参数，将显示所有配置的 地址前缀列表的统计信息。
IPv6【举例】
\# 显示所有 IPv6 地址前缀列表的统计信息。
<Sysname> display ipv6 prefix-list Prefix-list6: 666 Permitted 0 Denied 0 index: 10 Permit 6::/64 ge 66 le 88表1-6 display ipv6 prefix-list 命令显示信息描述表字段 描述Prefix-list6 IPv6地址前缀列表的名称Permitted 符合匹配条件的路由个数不符合匹配条件的路由个数Denied index 地址前缀列表的内部序列号匹配模式，有两种取值：
• Permit：表示允许permit
• Deny：表示拒绝6::/64 匹配的IPv6地址和前缀长度

字段 描述ge 即greater-equal，匹配的IPv6前缀长度的下限值le 即less-equal，匹配的IPv6前缀长度的上限值【相关命令】
• ipv6 prefix-list
• reset ipv6 prefix-list

##### 1.3.4 if-match ipv6

命令用来配置 的路由信息的匹配条件。
if-match ipv6 IPv6命令用来取消 IPv6 的路由信息的匹配条件的配置。
undo if-match ipv6【命令】
if-match ipv6 { address | next-hop | route-source } { acl ipv6-acl-number | prefix-list prefix-list-name } undo if-match ipv6 { address | next-hop | route-source } [ acl | prefix-list ]【缺省情况】
未配置 IPv6 的路由信息的匹配条件。
【视图】
路由策略视图【缺省用户角色】
network-admin【参数】
address：匹配 IPv6 路由信息的目的地址。
next-hop：匹配 IPv6 路由信息的下一跳。
route-source：匹配 IPv6 路由信息的源地址。
：指定用于过滤的 号。对于 ，acl ipv6-acl-number IPv6 ACL address ipv6-acl-number的取值范围为 2000～3999；对于 next-hop 和 route-source，ipv6-acl-number 的取值范围为 2000～2999。
prefix-list-name：指定用于过滤的 IPv6 地址前缀列表的名称，为 1～63 个字prefix-list符的字符串，区分大小写。
【举例】
\# 创建一个名为 policy1 的路由策略，其节点序列号为 10，匹配模式为 permit。定义一条 if-match子句，允许下一跳地址匹配已存在的 IPv6 地址前缀列表 p1 的路由信息通过。
<Sysname> system-view [Sysname] route-policy policy1 permit node 10 [Sysname-route-policy-policy1-10] if-match ipv6 next-hop prefix-list p1

##### 1.3.5 ipv6 prefix-list

ipv6 prefix-list 命令用来配置 IPv6 地址前缀列表或表项。
undo ipv6 prefix-list 命令用来删除指定的 IPv6 地址前缀列表或其中某个表项。
【命令】
ipv6 prefix-list prefix-list-name [ index index-number ] { deny | permit } ipv6-address { prefix-length [ greater-equal min-prefix-length ] [ less-equal max-prefix-length ] | inverse inverse-prefix-length } undo ipv6 prefix-list prefix-list-name [ index index-number ]【缺省情况】
不存在 IPv6 地址前缀列表。
【视图】
系统视图【缺省用户角色】
network-admin【参数】
prefix-list-name：指定 地址前缀列表名，为 1～63 个字符的字符串，区分大小写。
IPv6 index-number：标识 地址前缀列表中的一条表项，index-number 小的表项先被匹配，取IPv6值范围为 1～65535。如果未指定本参数，该序号值按照配置先后顺序依次递增，每次加 10，第一个序号值为 10。
deny：指定所定义的 IPv6 地址前缀列表表项的匹配模式为拒绝模式。在该模式下，如果过滤的 IPv6地址在定义的范围内，则不能通过过滤，并且不进行下一节点的匹配；否则，进行下一节点的匹配。
permit：指定所定义的 IPv6 地址前缀列表表项的匹配模式为允许模式。在该模式下，如果过滤的地址在定义的范围内，则通过过滤，不进行下一个节点的匹配；否则，进行下一节点的匹配。
IPv6 ipv6-address：指定 地址。
IPv6 prefix-length：指定前缀长度，取值范围为 0～128。
min-prefix-length、less-equal max-prefix-length：如果 IPv6 地greater-equal址和前缀长度都已匹配，则使用该参数来指定地址前缀长度范围。 greater-equal 表示大于等于，less-equal 表 示 小 于 等 于 。 前 缀 长 度 范 围 可 以 表 达 为 prefix-length <= <= <= 128。如果只指定了 min-prefix-length，min-prefix-length max-prefix-length则前缀范围为[ min-prefix-length，128 ]；如果只指定了 max-prefix-length，则前缀范围 为[ prefix-length ， max-prefix-length ] ； 如 果 二 者 都 指 定 ， 则 前 缀 范 围 为min-prefix-length，max-prefix-length ]。
[ inverse inverse-prefix-length：指定反向前缀长度，即与指定的 IPv6 地址前缀从最低位开始需要匹配的位数。inverse-prefix-length 的取值范围为 1～128。
【使用指导】
地址前缀列表用于 地址过滤。一个 地址前缀列表可包含多个表项，一个表项指定一IPv6 IPv6 IPv6个地址前缀范围。表项之间的过滤关系是“或”，即通过一个表项就可通过该 IPv6 地址前缀列表的过滤。没有通过任何一个表项的过滤就意味着没有通过该 IPv6 地址前缀列表的过滤。

如果将 指定为:: 0，则只匹配缺省路由。如果需要匹配所有路ipv6-address prefix-length由，则应配置为:: 128。
0 less-equal【举例】
\# 配置一条 IPv6 地址前缀列表，允许前缀长度在 32 位到 64 位之间的 IPv6 地址通过。
<Sysname> system-view [Sysname] ipv6 prefix-list abc permit :: 0 greater-equal 32 less-equal 64 \# 配置一条 IPv6 地址前缀列表，拒绝地址前缀为 3FFE:D00::/32，前缀长度大于等于 32 位的 IPv6地址通过。
<Sysname> system-view [Sysname] ipv6 prefix-list abc deny 3FFE:D00:: 32 less-equal 128【相关命令】
• display ipv6 prefix-list
• reset ipv6 prefix-list

##### 1.3.6 reset ipv6 prefix-list

reset ipv6 prefix-list 命令用来清除 IPv6 地址前缀列表的统计信息。
【命令】
reset ipv6 prefix-list [ prefix-list-name ]【视图】
用户视图【缺省用户角色】
network-admin【参数】
prefix-list-name：指定地址前缀列表的名称，为 1～63 个字符的字符串，区分大小写。如果未指定本参数，将清除所有的 IPv6 地址前缀列表的统计信息。
【举例】
\# 清除指定 IPv6 地址前缀列表的统计信息。
<Sysname> reset ipv6 prefix-list abc【相关命令】
•display ipv6 prefix-list
• ipv6 prefix-list
