# H3C R1110 三层技术-IP路由配置指导

H3C S6520X-EI & S6520X-HI系列以太网交换机三层技术-IP 路由配置指导新华三技术有限公司http://www.h3c.com资料版本：6W100-20180821产品版本：Release 1110

未经本公司书面许可，任何单位和个人不得擅自摘抄、复制本书内容的部分或全部，并不得以任何形式传播。
H3C、 、H3CS、H3CIE、H3CNE、Aolynk、 、H Care、 、IRF、NetPilot、Netflow、SecEngine、SecPath、SecCenter、SecBlade、Comware、ITCMM、HUASAN、华三均为新华三技术有限公司的商标。对于本手册中出现的其它公司的商标、产品标识及商品名称，由各自权利人拥有。
由于产品版本升级或其他原因，本手册内容有可能变更。H3C 保留在没有任何通知或者提示的情况下对本手册的内容进行修改的权利。本手册仅作为使用指导，H3C 尽全力在本手册中提供准确的信息，但是 H3C 并不确保手册内容完全没有错误，本手册中的所有陈述、信息和建议也不构成任何明示或暗示的担保。

## 00-前言

前 言本配置指导主要介绍路由协议的原理和配置，包括 IPv4、IPv6 网络的各种路由学习技术，以及影响路由选择或者路由表生成的策略。
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

## 01-IP路由基础配置

目 录路由简介路由迭代配置路由在 中的最大存活时间配置路由的 功能配置设备支持的最大激活路由前缀数

### 1 IP路由基础

1 IP路由基础本手册仅介绍单播路由协议，组播路由协议请参见“IP 组播配置指导”。

#### 1.1 IP路由简介

在网络中路由器根据所收到的报文的目的地址选择一条合适的路径，并将报文转发到下一个路由器。
路径中最后一个路由器负责将报文转发给目的主机。路由就是报文在转发过程中的路径信息，用来指导报文转发。

##### 1.1.1 路由表

RIB（Routing Information Base，路由信息库），是一个集中管理路由信息的数据库，包含路由表信息以及路由周边信息（路由迭代信息、路由共享信息以及路由扩展信息）等。
路由器通过对路由表进行优选，把优选路由下发到 FIB（Forwarding Base，转发信息Information库）表中，通过 FIB 表指导报文转发。FIB 表中每条转发项都指明了要到达某子网或某主机的报文应通过路由器的哪个物理接口发送，就可以到达该路径的下一个路由器，或者不需再经过别的路由器便可传送到直接相连的网络中的目的主机。FIB 表的具体内容，请参见“三层技术-IP 业务配置指导”中的“IP 转发基础”。

##### 1.1.2 路由分类

表1-1 路由分类分类标准 具体分类
• 直连路由：链路层协议发现的路由，也称为接口路由
• 静态路由：网络管理员手工配置的路由。静态路由配置方便，对系统要求低，适用根据来源不同 于拓扑结构简单并且稳定的小型网络。其缺点是每当网络拓扑结构发生变化，都需要手工重新配置，不能自动适应
• 动态路由：路由协议发现的路由根据路由目的地的不 • 网段路由：目的地为网段，子网掩码长度小于 32 位同
• 主机路由：目的地为主机，子网掩码长度为 32 位
• 直接路由：目的地所在网络与路由器直接相连根据目的地与该路由器是否直接相连
• 间接路由：目的地所在网络与路由器非直接相连

##### 1.1.3 路由协议分类

路由协议有自己的路由算法，能够自动适应网络拓扑的变化，适用于具有一定规模的网络拓扑。其缺点是配置比较复杂，对系统的要求高于静态路由，并占用一定的网络资源。
对路由协议的分类可采用以下不同标准。

表1-2 路由协议分类分类标准 具体分类
• IGP（Interior Gateway Protocol，内部网关协议）：在一个自治系统内部运行，常见的 IGP 协议包括 RIP、OSPF 和 IS-IS根据作用范围
• EGP（Exterior Protocol，外部网关协议）：运行于不同自治系统之间，Gateway BGP 是目前最常用的 EGP
• 距离矢量（Distance-Vector）协议：包括 和 BGP。其中，BGP 也被称为路径RIP矢量协议（Path-Vector）
根据使用算法
• 链路状态（Link-State）协议：包括 OSPF 和 IS-IS
• 单播路由协议：包括 RIP、OSPF、BGP 和 IS-IS 等根据目的地址类型
• 组播路由协议：包括 PIM-SM、PIM-DM 等
• 路由协议：包括 RIP、OSPF、BGP 和 等IPv4 IS-IS根据IP协议版本
• IPv6 路由协议：包括 RIPng、OSPFv3、IPv6 BGP 和 IPv6 IS-IS 等AS（Autonomous System，自治系统）是拥有同一选路策略，并在同一技术管理部门下运行的一组路由器。

##### 1.1.4 路由优先级

对于相同的目的地，不同的路由协议、直连路由和静态路由可能会发现不同的路由，但这些路由并不都是最优的。为了判断最优路由，各路由协议、直连路由和静态路由都被赋予了一个优先级，具有较高优先级的路由协议发现的路由将成为最优路由。
除直连路由外，各路由协议的优先级都可由用户手工进行配置。另外，每条静态路由的优先级都可以不相同。缺省的路由优先级如 表 1-3 所示，数值越小表明优先级越高。
表1-3 缺省的路由优先级路由协议或路由种类 缺省的路由优先级DIRECT（直连路由） 0组播静态路由 1 OSPF 10 IS-IS 15单播静态路由 60 RIP 100 OSPF ASE 150 OSPF NSSA 150 IBGP 255 EBGP 255 UNKNOWN（来自不可信源端的路由） 256

##### 1.1.5 负载分担

对同一路由协议来说，允许配置多条目的地相同且开销也相同的路由。当到同一目的地的路由中，没有更高优先级的路由时，这几条路由都被采纳，在转发去往该目的地的报文时，依次通过各条路径发送，从而实现网络的负载分担。
目前支持负载分担有静态路由/IPv6 静态路由、RIP/RIPng、OSPF/OSPFv3、BGP/IPv6 BGP 和IS-IS/IPv6 IS-IS。

##### 1.1.6 路由备份

使用路由备份可以提高网络的可靠性。用户可根据实际情况，配置到同一目的地的多条路由，其中优先级最高的一条路由作为主路由，其余优先级较低的路由作为备份路由。
正常情况下，路由器采用主路由转发数据。当链路出现故障时，主路由变为非激活状态，路由器选择备份路由中优先级最高的转发数据，实现从主路由到备份路由的切换；当链路恢复正常时，路由器重新选择路由，由于主路由的优先级最高，路由器选择主路由来发送数据，实现从备份路由到主路由的切换。

##### 1.1.7 路由迭代

对于 BGP 路由（直连 EBGP 路由除外）和静态路由（配置了下一跳）以及多跳 RIP 路由而言，其所携带的下一跳信息可能并不是直接可达，需要找到到达下一跳的直连出接口。路由迭代的过程就是通过路由的下一跳信息来找到直连出接口的过程。
而对于 OSPF 和 IS-IS 等链路状态路由协议而言，其下一跳是直接在路由计算时得到的，不需要进行路由迭代。
路由迭代信息记录并保存路由迭代的结果，包括依赖路由的概要信息、迭代路径、迭代深度等。

##### 1.1.8 路由共享

由于各路由协议采用的路由算法不同，不同的路由协议可能会发现不同的路由。如果网络规模较大，当使用多种路由协议时，往往需要在不同的路由协议间能够共享各自发现的路由。
各路由协议都可以引入其它路由协议的路由、直连路由和静态路由，具体内容请参见本手册中各路由协议模块有关引入外部路由的描述。
路由共享信息记录了路由协议之间的引入关系。

##### 1.1.9 路由扩展

路由扩展属性主要是指 路由的扩展团体属性以及 路由的区域 ID、路由类型和BGP OSPF Router ID等。同路由共享一样，路由协议可以引入其它路由协议的路由扩展属性。
路由扩展信息记录了各路由协议的路由扩展属性以及路由协议扩展属性之间的引入关系。

#### 1.2 配置路由和标签在RIB中的最大存活时间

##### 1. 功能简介

当协议路由表项较多或协议 时间较长时，由于协议收敛速度较慢，可能会出现协议路由表项提GR前老化的问题。通过调节路由和标签在 RIB 中的最大存活时间，可以解决上面的问题。

##### 2. 配置限制和指导

该配置在下一次协议进程倒换或者 RIB 进程倒换时才生效。

##### 3. 配置步骤（IPv4）

(1) 进入系统视图。
system-view
(2) 进入 RIB 视图。
rib
(3) 创建 RIB IPv4 地址族，并进入 RIB IPv4 地址族视图。
address-family ipv4
(4) 配置 IPv4 路由和标签在 RIB 中的最大存活时间。
protocol protocol [ instance instance-name ] lifetime seconds
缺省情况下，IPv4 路由和标签在 RIB 中的最大存活时间为 480 秒。

##### 4. 配置步骤（IPv6）

(1) 进入系统视图。
system-view
(2) 进入 RIB 视图。
rib
(3) 创建 RIB IPv6 地址族，并进入 RIB IPv6 地址族视图。
address-family ipv6
(4) 配置 IPv6 路由和标签在 RIB 中的最大存活时间。
protocol protocol [ instance instance-name ] lifetime seconds
缺省情况下，IPv6 路由和标签在 中的最大存活时间为 秒。
RIB 480

#### 1.3 配置路由在FIB中的最大存活时间

##### 1. 功能简介

当协议进程倒换或 RIB 进程倒换后，如果协议进程没有配置 GR 或 NSR，需要多保留一段时间 FIB表项；如果协议进程配置了 GR 或 NSR，需要立刻删除 FIB 表项，避免 FIB 表项长时间存在导致问题。通过调节路由在 中的最大存活时间，可以解决上面的问题。
FIB

##### 2. 配置步骤（IPv4）

(1) 进入系统视图。
system-view
(2) 进入 RIB 视图。

rib
(3) 创建 RIB IPv4 地址族，并进入 RIB IPv4 地址族视图。
address-family ipv4
(4) 配置 IPv4 路由在 FIB 中的最大存活时间。
fib lifetime seconds缺省情况下，IPv4 路由在 FIB 中的最大存活时间为 600 秒。

##### 3. 配置步骤（IPv6）

(1) 进入系统视图。
system-view
(2) 进入 RIB 视图。
rib
(3) 创建 RIB IPv6 地址族，并进入 RIB IPv6 地址族视图。
address-family ipv6
(4) 配置 IPv6 路由在 FIB 中的最大存活时间。
fib lifetime seconds
缺省情况下，IPv6 路由在 FIB 中的最大存活时间为 600 秒。

#### 1.4 配置RIB向FIB下发路由时会携带属性消息

##### 1. 功能简介

配置本功能后，RIB 向 FIB 下刷路由时会携带属性消息。

##### 2. 配置步骤

进入系统视图。
(1)
system-view进入 视图。
(2) RIB rib
(3) 创建 RIB IPv4 地址族，并进入 RIB IPv4 地址族视图。
address-family ipv4
(4) 配置 RIB 向 FIB 下发路由时携带属性消息。
flush route-attribute protocol缺省情况下，RIB 向 FIB 下发路由时不携带属性消息。

#### 1.5 配置系统支持最大等价路由的条数

##### 1. 配置限制和指导

该配置在设备重启后才能生效，进行设备重启前请评估重启对网络造成的影响，做好相关准备工作。

##### 2. 配置步骤（IPv4）

(1) 进入系统视图。

##### 1. 功能简介

system-view
(2) 配置系统支持最大等价路由的条数。
max-ecmp-num number缺省情况下，系统支持的最大等价路由条数为 8。

#### 1.6 配置路由的NSR功能

##### 1. 功能简介

NSR（Nonstop Routing，不间断路由）将路由信息从主进程备份到备进程，在设备发生主备倒换时保证路由信息不丢失，解决了主备倒换期间引发的路由震荡问题，保证转发业务不中断。
路由 NSR 相对于路由协议 NSR 功能，主备倒换时路由收敛速度更快。

##### 2. 配置限制和指导

配置本功能的同时，请配置协议的 GR 或 NSR 功能，否则可能导致路由老化和流量中断。

##### 3. 配置步骤（IPv4）

(1) 进入系统视图。
system-view
(2) 进入 RIB 视图。
rib
(3) 创建 RIB IPv4 地址族，并进入 RIB IPv4 地址族视图。
address-family ipv4
(4) 配置 IPv4 路由的 NSR 功能。
non-stop-routing
缺省情况下，IPv4 路由的 NSR 功能处于关闭状态。

##### 4. 配置步骤（IPv6）

(1) 进入系统视图。
system-view
(2) 进入 RIB 视图。
rib
(3) 创建 RIB IPv6 地址族，并进入 RIB IPv6 地址族视图。
address-family ipv6
(4) 配置 IPv6 路由的 NSR 功能。
non-stop-routing
缺省情况下，IPv6 路由的 NSR 功能处于关闭状态。

#### 1.7 配置路由不同协议间快速重路由功能

功能简介
1.
当 RIB 表中存在去往同一目的地的多条路由时，路由器会将优先级较高的路由下发到 FIB 表，当该路由的下一跳不可达时，数据流量将会被中断，路由器会重新进行路由优选，优选完毕后，使用新

的最优路由来指导报文转发。例如，去往同一个目的地存在一条静态路由和一条 OSPF 路由，缺省情况 路由会作为最优路由下发到 表。当 路由的下一跳不可达时，数据流量将会被OSPF FIB OSPF中断。
通过配置不同协议间快速重路由功能，可以将静态路由的下一跳作为备份下一跳。当路由器检测到网络故障时，将使用备份下一跳替换失效下一跳，通过备份下一跳来指导报文的转发，从而大大缩短了流量中断的时间。

##### 2. 配置限制和指导

使用不同协议间的快速重路由功能生成备份下一跳时可能会造成环路。

##### 3. 配置步骤（IPv4）

(1) 进入系统视图。
system-view
(2) 进入 RIB 视图。
rib
(3) 创建 RIB IPv4 地址族，并进入 RIB IPv4 地址族视图。
address-family ipv4
配置 路由不同协议间快速重路由功能。
(4) IPv4
inter-protocol fast-reroute [ vpn-instance vpn-instance-name ]
缺省情况下，不同协议间快速重路由处于关闭状态。
不指定 时，开启公网的不同协议间快速重路由功能。
VPN

##### 4. 配置步骤（IPv6）

(1) 进入系统视图。
system-view
进入 视图。
(2) RIB
rib
创建 地址族，并进入 地址族视图。
(3) RIB IPv6 RIB IPv6
address-family ipv6
(4) 配置 IPv6 路由不同协议间快速重路由功能。
inter-protocol fast-reroute [ vpn-instance vpn-instance-name ]
缺省情况下，不同协议间快速重路由处于关闭状态。
不指定 VPN 时，开启公网的不同协议间快速重路由功能。

#### 1.8 配置路由快速切换功能

##### 1. 功能简介

在未开启本功能的情况下，当某个物理接口为大量路由（包括等价路由和主备路由的主路由）连接下一跳的出接口时，如果该接口所在的链路故障时，设备需要先删除失效链路对应的所有 ARP/ND表项，然后通知 FIB 删除失效的 FIB 表项，处理时间过长，流量无法快速切换到可用路径。通过开启本功能，当接口所在的链路故障时，设备直接通知 删除失效的 表项，以加快路由的切换、FIB FIB缩短流量中断的时间。

##### 1. 功能简介

##### 2. 配置步骤（IPv4）

(1) 进入系统视图。
system-view
(2) 配置开启 IPv4 路由快速切换功能。
ip route fast-switchover enable
缺省情况下，IPv4 路由快速切换功能处于关闭状态。

##### 3. 配置步骤（IPv6）

(1) 进入系统视图。
system-view
(2) 配置开启 IPv6 路由快速切换功能。
ipv6 route fast-switchover enable
缺省情况下，IPv6 路由快速切换功能处于关闭状态。

#### 1.9 配置路由按照路由策略进行迭代下一跳查找

功能简介
1.
通过配置按路由策略迭代下一跳，可以对路由迭代的结果进行控制。例如：当路由发生变化时，路由管理需要对非直连的下一跳重新进行迭代。如果不对迭代的结果路由进行任何限制，则路由管理可能会将下一跳迭代到一个错误的转发路径上，从而造成流量丢失。此时，可以通过配置本功能，将错误的依赖路由过滤掉，使路由迭代到通过路由策略过滤的指定依赖路由上。

##### 2. 配置限制和指导

配置路由策略时，如果配置了 apply 子句，apply 子句不会生效。
配置路由策略时，请确保至少有一个正确的依赖路由能够通过该策略的过滤，否则可能导致相关路由不可达，无法正确指导转发。

##### 3. 配置步骤（IPv4）

(1) 进入系统视图。
system-view
进入 视图。
(2) RIB
rib
创建 地址族，并进入 地址族视图。
(3) RIB IPv4 RIB IPv4
address-family ipv4
配置路由按照路由策略进行迭代下一跳查找。
(4)
protocol protocol nexthop recursive-lookup route-policy
route-policy-name
缺省情况下，未配置路由按路由策略进行下一跳迭代查找。

##### 4. 配置步骤（IPv6）

(1) 进入系统视图。
system-view

(2) 进入 RIB 视图。
rib
(3) 创建 RIB IPv6 地址族，并进入 RIB IPv6 地址族视图。
address-family ipv6
(4) 配置路由按照路由策略进行迭代下一跳查找。
protocol protocol nexthop recursive-lookup route-policy
route-policy-name
缺省情况下，未配置路由按路由策略进行下一跳迭代查找。

#### 1.10 配置设备支持的最大激活路由前缀数

##### 1. 功能简介

配置设备支持的最大 IPv4/IPv6 激活路由前缀数后，当设备上的 IPv4/IPv6 激活路由前缀数超过最大支持的激活路由前缀数目时，可以继续激活新的路由前缀，但会产生一条日志信息提示用户，以便用户及时执行必要的操作，以免 IPv4/IPv6 激活路由前缀占用过多的资源。

##### 2. 配置步骤（IPv4）

进入系统视图。
(1)
system-view进入 视图。
(2) RIB rib
(3) 创建 RIB IPv4 地址族，并进入 RIB IPv4 地址族视图。
address-family ipv4
(4) 配置最大 IPv4 激活路由前缀数。
routing-table limit number simply-alert缺省情况下，不限制设备支持的最大 IPv4 激活路由前缀数。
RIB IPv4 地址族视图下的配置用于控制公网和所有 VPN 实例内 IPv4 激活路由的总数。

##### 3. 配置步骤（IPv6）

(1) 进入系统视图。
system-view
(2) 进入 RIB 视图。
rib
(3) 创建 RIB IPv6 地址族，并进入 RIB IPv6 地址族视图。
address-family ipv6
(4) 配置最大 IPv6 激活路由前缀数。
routing-table limit number simply-alert
缺省情况下，不限制设备支持的最大 IPv6 激活路由前缀数。
RIB IPv6 地址族视图下的配置用于控制公网和所有 VPN 实例内 IPv6 激活路由的总数。

#### 1.11 路由表显示和维护

在任意视图下执行 display 命令可以显示路由表信息。在用户视图下执行 reset 命令可以清除路由表的统计信息。
表1-4 路由表显示和维护操作 命令display ip routing-table [ all-vpn-instance | vpn-instance vpn-instance-name ] [ verbose ]显示路由表的信息display ip routing-table [ all-routes ]显示通过指定基本访问控制列 display ip routing-table vpn-instance [ vpn-instance-name ]表过滤的路由信息 acl ipv4-acl-number [ verbose ] display ip routing-table [ vpn-instance vpn-instance-name ]显示指定目的地址的路由ip-address [ mask-length | mask ] [ longer-match ] [ verbose ]显示指定目的地址范围内的路 display ip routing-table [ vpn-instance vpn-instance-name ]由 ip-address1 to ip-address2 [ verbose ]显示通过指定前缀列表过滤的 display ip routing-table [ vpn-instance vpn-instance-name ]路由信息 prefix-list prefix-list-name [ verbose ]显示指定协议生成或发现的路 display ip routing-table [ vpn-instance vpn-instance-name ] protocol protocol [ inactive | verbose ]由信息显示路由表中的综合路由统计display ip routing-table [ all-routes | all-vpn-instance |信息 vpn-instance vpn-instance-name ] statistics display ip routing-table [ vpn-instance vpn-instance-name ]显示路由表的概要信息summary显示IPv6 RIB的路由属性信息 display ipv6 rib attribute [ attribute-id ]显示IPv6 RIB的GR状态信息 display ipv6 rib graceful-restart display ipv6 rib nib [ self-originated ] [ nib-id ] [ verbose ]显示IPv6 RIB的下一跳信息display ipv6 rib nib protocol verbose protocol [ ]显示IPv6直连路由下一跳信息 display ipv6 route-direct nib [ nib-id ] [ verbose ] display ipv6 routing-table [ all-vpn-instance | vpn-instance vpn-instance-name ] [ verbose ]显示IPv6路由表的信息display ipv6 routing-table [ all-routes ]显示通过指定基本IPv6 ACL过 display ipv6 routing-table [ vpn-instance滤的IPv6路由信息 vpn-instance-name ] acl ipv6-acl-number [ verbose ] display ipv6 routing-table [ vpn-instance显示指定目的地址的IPv6路由vpn-instance-name ] ipv6-address [ prefix-length ]信息[ longer-match ] [ verbose ] display ipv6 routing-table vpn-instance [显示指定目的地址范围内的vpn-instance-name ] ipv6-address1 to ipv6-address2 IPv6路由信息[ verbose ] display ipv6 routing-table vpn-instance [显示通过指定前缀列表过滤的vpn-instance-name ] prefix-list prefix-list-name IPv6路由信息[ verbose ] display ipv6 routing-table [ vpn-instance显示指定协议生成或发现的vpn-instance-name ] protocol protocol [ inactive | verbose ]

操作 命令IPv6路由信息显示IPv6路由表中的综合路由display ipv6 routing-table [ all-routes | all-vpn-instance统计信息 | vpn-instance vpn-instance-name ] statistics display ipv6 routing-table [ vpn-instance显示IPv6路由表的概要信息vpn-instance-name ] summary显示系统支持IPv4最大等价路display max-ecmp-num由的条数显示RIB的路由属性信息 display rib attribute [ attribute-id ]显示RIB的GR状态信息 display rib graceful-restart display rib nib [ self-originated ] [ nib-id ] [ verbose ]显示RIB的下一跳信息display rib nib protocol protocol [ verbose ]显示直连路由下一跳信息 display route-direct nib [ nib-id ] [ verbose ] reset ip routing-table statistics protocol [ vpn-instance vpn-instance-name ] { protocol | all }清除路由表中的综合路由统计信息 reset ip routing-table [ all-routes | all-vpn-instance ] statistics protocol { protocol | all } reset ipv6 routing-table statistics protocol [ vpn-instance vpn-instance-name ] { protocol | all }清除IPv6路由表中的综合路由统计信息 reset ipv6 routing-table [ all-routes | all-vpn-instance ] statistics protocol { protocol | all }

## 02-静态路由配置

目 录静态路由简介配置单跳检测配置手工指定备份下一跳静态路由显示和维护静态路由与 联动（非直连）配置举例

### 1 静态路由

1静态路由

#### 1.1 静态路由简介

静态路由是一种特殊的路由，由管理员手工配置。当网络结构比较简单时，只需配置静态路由就可以使网络正常工作。
静态路由不能自动适应网络拓扑结构的变化。当网络发生故障或者拓扑发生变化后，必须由网络管理员手工修改配置。

#### 1.2 配置静态路由

(1) 进入系统视图。
system-view
(2) 配置静态路由。
（公网）
ip route-static dest-address { mask-length | mask } { interface-type
interface-number [ next-hop-address ] | next-hop-address
[ recursive-lookup host-route ] | vpn-instance d-vpn-instance-name
next-hop-address [ recursive-lookup host-route ] } [ permanent | track
track-entry-number ] [ preference preference ] [ tag tag-value ]
[ description text ]
缺省情况下，未配置静态路由。
通过在 模块和静态路由之间建立联动，可以实现静态路由可达性的实时判断。关于
Track Track
的详细介绍，请参见“可靠性配置指导”中的“Track”。
（VPN 网络）
ip route-static vpn-instance s-vpn-instance-name dest-address
{ mask-length | mask } { interface-type interface-number
[ next-hop-address ] | next-hop-address [ recursive-lookup host-route ]
[ public ] | vpn-instance d-vpn-instance-name next-hop-address
[ recursive-lookup host-route ] } [ permanent | track track-entry-number ]
[ preference preference ] [ tag tag-value ] [ description text ]
缺省情况下，未配置静态路由。
通过在 Track 模块和静态路由之间建立联动，可以实现静态路由可达性的实时判断。关于 Track
的详细介绍，请参见“可靠性配置指导”中的“Track”。
(3) （可选）配置静态路由向下一跳定时发送 ARP。
ip route-static arp-request interval interval
缺省情况下，静态路由不发送 ARP request。
(4) （可选）配置静态路由的缺省优先级。
ip route-static default-preference default-preference

##### 2. 配置步骤

缺省情况下，静态路由的缺省优先级为 60。

#### 1.3 配置静态路由配置组

##### 1. 功能简介

当配置多条静态路由时，如果只是前缀不同，每条静态路由都要配置一遍命令，比较繁琐。可以配置静态路由配置组，对静态路由进行批量配置，节省配置工作量。
按配置组配置静态路由时，配置组下的所有前缀会应用相同的下一跳、出接口信息。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 创建静态路由配置组，并进入静态路由配置组视图。
ip route-static-group group-name缺省情况下，未配置静态路由配置组。
(3) 在静态路由配置组中增加前缀。
prefix dest-address { mask-length | mask }缺省情况下，静态路由配置组中未配置前缀。
(4) 退回系统视图。
quit
(5) 配置静态路由。
（公网）
ip route-static group group-name { interface-type interface-number [ next-hop-address ] | next-hop-address [ recursive-lookup host-route ] | vpn-instance d-vpn-instance-name next-hop-address [ recursive-lookup host-route ] } [ permanent | track track-entry-number ] [ preference preference ] [ tag tag-value ] [ description text ]（VPN 网络）
ip route-static vpn-instance s-vpn-instance-name group group-name { interface-type interface-number [ next-hop-address ] | next-hop-address [ recursive-lookup host-route ] [ public ] | vpn-instance d-vpn-instance-name next-hop-address [ recursive-lookup host-route ] } [ permanent | track track-entry-number ] [ preference preference ] [ tag tag-value ] [ description text ]缺省情况下，未配置静态路由。

#### 1.4 配置静态路由删除

##### 1. 功能简介

使用 undo ip route-static 命令可以删除一条静态路由，而使用 delete static-routes all 命令可以删除包括缺省路由在内的所有静态路由。

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 删除所有静态路由。
（公网）
delete static-routes all
（VPN 网络）
delete vpn-instance vpn-instance-name static-routes all

#### 1.5 配置静态路由与BFD联动

路由振荡时，使能 BFD 功能可能会加剧振荡，请谨慎使用。

##### 1.5.1 功能简介

BFD（Bidirectional Detection，双向转发检测）提供了一个通用的、标准化的、介质无Forwarding关、协议无关的快速故障检测机制，可以为上层协议（如路由协议等）统一地快速检测两台路由器间双向转发路径的故障。
关于 BFD 的详细介绍，请参见“可靠性配置指导”中的“BFD”。

##### 1.5.2 配置双向检测

###### 1. 功能简介

双向检测，即本端和对端需要同时进行配置，通过控制报文检测两个方向上的链路状态，实现毫秒级别的链路故障检测。
双向检测支持直连下一跳和非直连下一跳。
• 直连下一跳是指下一跳和本端是直连的，配置时必须指定出接口和下一跳。
• 非直连下一跳是指下一跳和本端不是直连的，中间还有其它设备。配置时必须指定下一跳和源 地址。
BFD IP

###### 2. 配置直连下一跳双向检测

(1) 进入系统视图。
system-view
配置静态路由与 联动。
(2) BFD
（公网）
ip route-static dest-address { mask-length | mask } interface-type
interface-number next-hop-address bfd control-packet [ preference
preference ] [ tag tag-value ] [ description text ]
（ VPN 网络）

ip route-static vpn-instance s-vpn-instance-name dest-address { mask-length | mask } interface-type interface-number next-hop-address bfd control-packet [ preference preference ] [ tag tag-value ] [ description text ]缺省情况下，未配置静态路由与 BFD 联动。

###### 3. 配置非直连下一跳双向检测

(1) 进入系统视图。
system-view
(2) 配置静态路由与 BFD 联动。
（公网）
ip route-static dest-address { mask-length | mask } { next-hop-address
bfd control-packet bfd-source ip-address | vpn-instance
d-vpn-instance-name next-hop-address bfd control-packet bfd-source
ip-address } [ preference preference ] [ tag tag-value ] [ description
text ]
（VPN 网络）
ip route-static vpn-instance s-vpn-instance-name dest-address
{ mask-length | mask } { next-hop-address bfd control-packet bfd-source
ip-address | vpn-instance d-vpn-instance-name next-hop-address bfd
control-packet bfd-source ip-address } [ preference preference ] [ tag
tag-value ] [ description text ]
缺省情况下，未配置静态路由与 BFD 联动。

##### 1.5.3 配置单跳检测

###### 1. 功能简介

单跳检测，即只需要本端进行配置，通过 echo 报文检测链路的状态。echo 报文的目的地址为本端接口地址，发送给下一跳设备后会直接转发回本端。这里所说的“单跳”是 IP 的一跳。
静态路由的出接口为处于 状态时，不能使用 进行检测。
SPOOFING BFD

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置 echo 报文的源 IP 地址。
bfd echo-source-ip ip-address
缺省情况下，未配置 echo 报文的源 IP 地址。
本命令的详细情况请参见“可靠性命令参考”中的“BFD”。
配置静态路由与 联动。
(3) BFD
（公网）

ip route-static dest-address { mask-length | mask } interface-type interface-number next-hop-address bfd echo-packet [ preference preference ] [ tag tag-value ] [ description text ]（VPN 网络）
ip route-static vpn-instance s-vpn-instance-name dest-address { mask-length | mask } interface-type interface-number next-hop-address bfd echo-packet [ preference preference ] [ tag tag-value ] [ description text ]缺省情况下，未配置静态路由与 联动。
BFD

#### 1.6 配置静态路由快速重路由功能

##### 1.6.1 功能简介

当网络中的链路或某台路由器发生故障时，需要通过故障链路或故障路由器传输才能到达目的地的报文将会丢失或产生路由环路，数据流量将会被中断。
为了尽可能避免网络故障导致的流量中断，网络管理员可以根据需要配置静态路由快速重路由功能。
图1-1 静态路由快速重路由功能示意图如 图 1-1 所示，通过配置快速重路由功能，网络管理员可以为路由指定备份下一跳，也可以在存在低优先级静态路由的情况下，使能自动快速重路由功能，查找满足条件的低优先级路由的下一跳作为主路由的备份下一跳，当路由器检测到网络故障时，路由器会使用事先配置好的备份下一跳替换失效下一跳，通过备份下一跳来指导报文的转发，从而避免了流量中断。

##### 1.6.2 配置限制和指导

静态路由快速重路由功能不能与静态路由 BFD 功能同时使用。
等价路由不支持配置静态路由快速重路由功能。
配置本功能后，当主链路三层接口 up，主链路由双通变为单通或者不通时，设备会将流量快速地切换到备份路径上转发；当主链路三层接口 down 时，设备会暂时将流量快速地切换到备份路径上转发。同时，设备会重新查找到达目的地址的路由，并将流量切换到查找到的新的路径。如果没有查找到路由，则流量转发会中断。因此，除本配置创建的静态路由外，设备上还需要存在一条到达目的地址的路由。单通现象，即一条链路上的两端，有且只有一端可以收到另一端发来的报文，此链路称为单向链路。

##### 1.6.3 配置手工指定备份下一跳

###### 1. 配置限制和指导

静态路由配置的备份出接口拔出或者删除时，配置的路由会失效。备份出接口和下一跳不能直接修改，且不能和主出接口和下一跳相同。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
配置静态路由快速重路由功能。
(2)
（公网）
ip route-static dest-address { mask-length | mask } interface-type
interface-number [ next-hop-address [ backup-interface interface-type
interface-number [ backup-nexthop backup-nexthop-address ] ] ]
[ permanent ] [ preference preference ] [ tag tag-value ] [ description
text ]
（VPN 网络）
ip route-static vpn-instance s-vpn-instance-name dest-address
{ mask-length | mask } interface-type interface-number
[ next-hop-address [ backup-interface interface-type interface-number
[ backup-nexthop backup-nexthop-address ] ] ] [ permanent ] [ preference
preference ] [ tag tag-value ] [ description text ]
缺省情况下，静态路由快速重路由功能处于关闭状态。

##### 1.6.4 配置自动查找备份下一跳

(1) 进入系统视图。
system-view
(2) 配置静态路由自动快速重路由功能。
ip route-static fast-reroute auto
缺省情况下，静态路由自动快速重路由功能处于关闭状态。

##### 1.6.5 配置静态路由快速重路由支持BFD检测功能

###### 1. 功能简介

缺省情况下，静态路由通过 ARP 检测主路由的下一跳是否可达。配置本功能后，将使用 BFD（Echo方式）检测主路由的下一跳是否可达，这种方式可以更快地检测到链路故障。

###### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 配置 BFD Echo 报文源地址。
bfd echo-source-ip ip-address

###### 1. 组网需求

缺省情况下，未配置 BFD Echo 报文源地址。
echo 报文的源 IP 地址用户可以任意指定。建议配置 echo 报文的源 IP 地址不属于该设备任何一个接口所在网段。
本命令的详细情况请参见“可靠性命令参考”中的“BFD”。
使能静态路由中主用链路的 BFD（Echo 方式）检测功能。
(3)
ip route-static primary-path-detect bfd echo缺省情况下，静态路由中主用链路的 BFD（Echo 方式）检测功能处于关闭状态。

#### 1.7 静态路由显示和维护

在完成上述配置后，在任意视图下执行 display 命令查看静态路由配置的运行情况并检验配置结果。
表1-1 静态路由显示和维护操作 命令查看静态路由表信息（本命令的详细情况display ip routing-table protocol static [ inactive |请参见“三层技术-IP路由命令参考”中的verbose ]“IP路由基础”）
显示静态路由下一跳信息 display route-static nib [ nib-id ] [ verbose ] display route-static routing-table [ vpn-instance显示静态路由表信息 vpn-instance-name ] [ ip-address { mask-length | mask } ]

#### 1.8 静态路由典型配置举例

##### 1.8.1 静态路由基本功能配置举例

组网需求
1.
交换机各接口及主机的IP地址和掩码如 图 1-2 所示。要求采用静态路由，使图中任意两台主机之间都能互通。

###### 2. 组网图

图1-2 静态路由基本功能配置组网图

###### 3. 配置步骤

配置各接口的 地址（略）
(1) IP配置静态路由
(2)
在 上配置缺省路由。
\# Switch A <SwitchA> system-view [SwitchA] ip route-static 0.0.0.0 0.0.0.0 1.1.4.2 \# 在 Switch B 上配置两条静态路由。
<SwitchB> system-view [SwitchB] ip route-static 1.1.2.0 255.255.255.0 1.1.4.1 [SwitchB] ip route-static 1.1.3.0 255.255.255.0 1.1.5.6 \# 在 Switch C 上配置缺省路由。
<SwitchC> system-view [SwitchC] ip route-static 0.0.0.0 0.0.0.0 1.1.5.5
(3) 配置主机配置 Host A 的缺省网关为 1.1.2.3，Host B 的缺省网关为 1.1.6.1，Host C 的缺省网关为
1.1.3.1 ，具体配置过程略。

###### 4. 验证配置

查看 的静态路由信息。
\# Switch A [SwitchA] display ip routing-table protocol static Summary Count : 1 Static Routing table Status : <Active> Summary Count : 1 Destination/Mask Proto Pre Cost NextHop Interface
0.0.0.0/0 Static 60 0 1.1.4.2 Vlan500

Static Routing table Status : <Inactive> Summary Count : 0 \# 查看 Switch B 的静态路由信息。
[SwitchB] display ip routing-table protocol static Summary Count : 2 Static Routing table Status : <Active> Summary Count : 2 Destination/Mask Proto Pre Cost NextHop Interface
1.1.2.0/24 Static 60 0 1.1.4.1 Vlan500
1.1.3.0/24 Static 60 0 1.1.5.6 Vlan600 Static Routing table Status : <Inactive> Summary Count : 0 \# 在 Host B 上使用 ping 命令验证 Host A 是否可达（假定主机安装的操作系统为 Windows XP）。
C:\Documents and Settings\Administrator>ping 1.1.2.2 Pinging 1.1.2.2 with 32 bytes of data:
Reply from 1.1.2.2: bytes=32 time=1ms TTL=126 Reply from 1.1.2.2: bytes=32 time=1ms TTL=126 Reply from 1.1.2.2: bytes=32 time=1ms TTL=126 Reply from 1.1.2.2: bytes=32 time=1ms TTL=126 Ping statistics for 1.1.2.2:
Packets: Sent = 4, Received = 4, Lost = 0 (0% loss), Approximate round trip times in milli-seconds:
Minimum = 1ms, Maximum = 1ms, Average = 1ms \# 在 Host B 上使用 tracert 命令验证 Host A 是否可达。
C:\Documents and Settings\Administrator>tracert 1.1.2.2 Tracing route to 1.1.2.2 over a maximum of 30 hops 1 <1 ms <1 ms <1 ms 1.1.6.1 2 <1 ms <1 ms <1 ms 1.1.4.1 3 1 ms <1 ms <1 ms 1.1.2.2 Trace complete.

##### 1.8.2 静态路由与BFD联动（直连）配置举例

###### 1. 组网需求

• 在 Switch A 上配置静态路由可以到达 120.1.1.0/24 网段，在 Switch B 上配置静态路由可以到
达 121.1.1.0/24 网段，并都使能 BFD 检测功能。
在 Switch C 上配置静态路由可以到达 120.1.1.0/24 网段和 121.1.1.0/24 网段。
•

当 Switch A 和 Switch B 通过 L2 Switch 通信的链路出现故障时，BFD 能够快速感知，并且切
•换到 进行通信。
Switch C

###### 2. 组网图

图1-3 静态路由与 BFD 联动（直连）配置组网图

| 接口 I | P地址 | 设备 | 接口 |
|---|---|---|---|
| Vlan-int10 1 | 2.1.1.1/24 | Switch B | Vlan-int10 |
| Vlan-int11 1 | 0.1.1.102/24 |  | Vlan-int13 |
| Vlan-int11 1 | 0.1.1.100/24 |  |  |
| Vlan-int13 1 | 3.1.1.2/24 |  |  |

设备 IP 地址Switch A 12.1.1.2/24
13.1.1.1/24 Switch C

###### 3. 配置步骤

配置各接口的 地址（略）
(1) IP配置静态路由和
(2) BFD在 上配置静态路由，并使能 检测功能，使用双向检测方式。
\# Switch A BFD <SwitchA> system-view [SwitchA] interface vlan-interface 10 [SwitchA-vlan-interface10] bfd min-transmit-interval 500 [SwitchA-vlan-interface10] bfd min-receive-interval 500 [SwitchA-vlan-interface10] bfd detect-multiplier 9 [SwitchA-vlan-interface10] quit [SwitchA] ip route-static 120.1.1.0 24 vlan-interface 10 12.1.1.2 bfd control-packet [SwitchA] ip route-static 120.1.1.0 24 vlan-interface 11 10.1.1.100 preference 65 [SwitchA] quit在 上配置静态路由，并使能 检测功能，使用双向检测方式。
\# Switch B BFD <SwitchB> system-view [SwitchB] interface vlan-interface 10 [SwitchB-vlan-interface10] bfd min-transmit-interval 500 [SwitchB-vlan-interface10] bfd min-receive-interval 500 [SwitchB-vlan-interface10] bfd detect-multiplier 9 [SwitchB-vlan-interface10] quit [SwitchB] ip route-static 121.1.1.0 24 vlan-interface 10 12.1.1.1 bfd control-packet [SwitchB] ip route-static 121.1.1.0 24 vlan-interface 13 13.1.1.2 preference 65 [SwitchB] quit在 上配置静态路由。
\# Switch C

<SwitchC> system-view [SwitchC] ip route-static 120.1.1.0 24 13.1.1.1 [SwitchC] ip route-static 121.1.1.0 24 10.1.1.102

###### 4. 验证配置

下面以 为例，Switch 和 类似，不再赘述。
Switch A B Switch A查看 会话，可以看到 会话已经创建。
\# BFD BFD <SwitchA> display bfd session Total Session Num: 1 Up Session Num: 1 Init Mode: Active IPv4 Session Working Under Ctrl Mode:
LD/RD SourceAddr DestAddr State Holdtime Interface 4/7 12.1.1.1 12.1.1.2 Up 2000ms Vlan10 \# 查看静态路由，可以看到 Switch A 经过 L2 Switch 到达 Switch B。
<SwitchA> display ip routing-table protocol static Summary Count : 1 Static Routing table Status : <Active> Summary Count : 1 Destination/Mask Proto Pre Cost NextHop Interface
120.1.1.0/24 Static 60 0 12.1.1.2 Vlan10 Static Routing table Status : <Inactive> Summary Count : 0当 Switch A 和 Switch B 通过 L2 Switch 通信的链路出现故障时：
\# 查看静态路由，可以看到 Switch A 经过 Switch C 到达 Switch B。
<SwitchA> display ip routing-table protocol static Summary Count : 1 Static Routing table Status : <Active> Summary Count : 1 Destination/Mask Proto Pre Cost NextHop Interface
120.1.1.0/24 Static 65 0 10.1.1.100 Vlan11 Static Routing table Status : <Inactive> Summary Count : 0

###### 1. 组网需求

##### 1.8.3 静态路由与BFD联动（非直连）配置举例

组网需求
1.
• 在 Switch A 上配置静态路由可以到达 120.1.1.0/24 网段，在 Switch B 上配置静态路由可以到达 网段，并都使能 检测功能。
121.1.1.0/24 BFD在 Switch C 和 Switch D 上配置静态路由可以到达 120.1.1.0/24 网段和 121.1.1.0/24 网段。
•Switch A 存在到 Switch B 的接口 Loopback1（2.2.2.9/32）的路由，出接口为 Vlan-interface10；
•存在到 的接口 Loopback1（1.1.1.9/32）的路由，出接口为 Vlan-interface12；
Switch B Switch A Switch D 存在到 1.1.1.9/32 的路由，出接口为 Vlan-interface10，存在到 2.2.2.9/32 的路由，出接口为 Vlan-interface12。
• 当 Switch A 和 Switch B 通过 Switch D 通信的链路出现故障时，BFD 能够快速感知，并且切换到 进行通信。
Switch C

###### 2. 组网图

图1-4 静态路由与 联动（非直连）配置组网图BFD

| 接口 | IP地址 | 设备 | 接口 |
|---|---|---|---|
| Vlan-int10 | 12.1.1.1/24 | Switch B | Vlan-int12 |
| Vlan-int11 | 10.1.1.102/24 |  | Vlan-int13 |
| Loop1 | 1.1.1.9/32 |  | Loop1 |
| Vlan-int11 | 10.1.1.100/24 | Switch D | Vlan-int10 |
| Vlan-int13 | 13.1.1.2/24 |  | Vlan-int12 |

设备 接口 IP地址Switch A Vlan-int10 11.1.1.1/24 Vlan-int11 13.1.1.1/24 Loop1 2.2.2.9/32 Switch C Vlan-int11 12.1.1.2/24 Vlan-int13 11.1.1.2/24

###### 3. 配置步骤

配置各接口的 地址（略）
(1) IP配置静态路由和
(2) BFD在 上配置静态路由，并使能 检测功能，使用双向检测方式。
\# Switch A BFD <SwitchA> system-view [SwitchA] bfd multi-hop min-transmit-interval 500 [SwitchA] bfd multi-hop min-receive-interval 500 [SwitchA] bfd multi-hop detect-multiplier 9 [SwitchA] ip route-static 120.1.1.0 24 2.2.2.9 bfd control-packet bfd-source 1.1.1.9 [SwitchA] ip route-static 120.1.1.0 24 vlan-interface 11 10.1.1.100 preference 65 [SwitchA] quit

###### 4. 验证配置

\# 在 Switch B 上配置静态路由，并使能 BFD 检测功能，使用双向检测方式。
<SwitchB> system-view [SwitchB] bfd multi-hop min-transmit-interval 500 [SwitchB] bfd multi-hop min-receive-interval 500 [SwitchB] bfd multi-hop detect-multiplier 9 [SwitchB] ip route-static 121.1.1.0 24 1.1.1.9 bfd control-packet bfd-source 2.2.2.9 [SwitchB] ip route-static 121.1.1.0 24 vlan-interface 13 13.1.1.2 preference 65 [SwitchB] quit \# 在 Switch C 上配置静态路由。
<SwitchC> system-view [SwitchC] ip route-static 120.1.1.0 24 13.1.1.1 [SwitchC] ip route-static 121.1.1.0 24 10.1.1.102 \# 在 Switch D 上配置静态路由。
<SwitchD> system-view [SwitchD] ip route-static 120.1.1.0 24 11.1.1.1 [SwitchD] ip route-static 121.1.1.0 24 12.1.1.1验证配置
4.
下面以 Switch A 为例，Switch B 和 Switch A 类似，不再赘述。
\# 查看 BFD 会话，可以看到 BFD 会话已经创建。
<SwitchA> display bfd session Total Session Num: 1 Up Session Num: 1 Init Mode: Active IPv4 Session Working Under Ctrl Mode:
LD/RD SourceAddr DestAddr State Holdtime Interface 4/7 1.1.1.9 2.2.2.9 Up 2000ms N/A \# 查看静态路由，可以看到 Switch A 经过 Switch D 到达 Switch B。
<SwitchA> display ip routing-table protocol static Summary Count : 1 Static Routing table Status : <Active> Summary Count : 1 Destination/Mask Proto Pre Cost NextHop Interface
120.1.1.0/24 Static 60 0 12.1.1.2 Vlan10 Static Routing table Status : <Inactive> Summary Count : 0当 Switch A 和 Switch B 通过 Switch D 通信的链路出现故障时：
\# 查看静态路由，可以看到 Switch A 经过 Switch C 到达 Switch B 。
<SwitchA> display ip routing-table protocol static Summary Count : 1

Static Routing table Status : <Active> Summary Count : 1 Destination/Mask Proto Pre Cost NextHop Interface
120.1.1.0/24 Static 65 0 10.1.1.100 Vlan11 Static Routing table Status : <Inactive> Summary Count : 0

##### 1.8.4 静态路由快速重路由配置举例

###### 1. 组网需求

如 图 1-5 所示，Switch A、Switch B和Switch C通过静态路由实现网络互连。要求当Switch A和Switch B之间的链路A出现单通故障时，业务可以快速切换到链路B上。

###### 2. 组网图

图1-5 静态路由快速重路由配置组网图

| 接口 | IP地址 | 设备 | 接口 |
|---|---|---|---|
| Vlan-int100 | 12.12.12.1/24 | Switch B | Vlan-int101 |
| Vlan-int200 | 13.13.13.1/24 |  | Vlan-int200 |
| Loop0 | 1.1.1.1/32 |  | Loop0 |
| Vlan-int100 | 12.12.12.2/24 |  |  |
| Vlan-int101 | 24.24.24.2/24 |  |  |

设备 IP地址Switch A 24.24.24.4/24
13.13.13.2/24
4.4.4.4/32 Switch C

###### 3. 配置步骤

配置各接口的 地址（略）
(1) IP配置链路 上的静态路由快速重路由
(2) A静态路由支持快速重路由配置有两种方法，可以任选一种方法一：配置静态路由快速重路由功能（手工指定备份下一跳）
在 上配置静态路由，并指定备份出接口和下一跳。
\# Switch A <SwitchA> system-view [SwitchA] ip route-static 4.4.4.4 32 vlan-interface 200 13.13.13.2 backup-interface vlan-interface 100 backup-nexthop 12.12.12.2 \# 在 Switch B 上配置静态路由，并指定备份出接口和下一跳。
<SwitchB> system-view

[SwitchB] ip route-static 1.1.1.1 32 vlan-interface 200 13.13.13.1 backup-interface vlan-interface 101 backup-nexthop 24.24.24.2方法二：配置静态路由快速重路由功能（自动查找备份下一跳）
\# 在 Switch A 上配置静态路由，并配置静态路由自动快速重路由功能。
<SwitchA> system-view [SwitchA] ip route-static 4.4.4.4 32 vlan-interface 200 13.13.13.2 [SwitchA] ip route-static 4.4.4.4 32 vlan-interface 100 12.12.12.2 preference 70 [SwitchA] ip route-static fast-reroute auto在 上配置静态路由，并配置静态路由自动快速重路由功能。
\# Switch B <SwitchB> system-view [SwitchB] ip route-static 1.1.1.1 32 vlan-interface 200 13.13.13.1 [SwitchB] ip route-static 1.1.1.1 32 vlan-interface 101 24.24.24.2 preference 70 [SwitchB] ip route-static fast-reroute auto
(3) 配置链路 B 上的静态路由\# 在 Switch C 上配置静态路由。
<SwitchC> system-view [SwitchC] ip route-static 4.4.4.4 32 vlan-interface 101 24.24.24.4 [SwitchC] ip route-static 1.1.1.1 32 vlan-interface 100 12.12.12.1

###### 4. 验证配置

\# 在 Switch A 上查看 4.4.4.4/32 路由，可以看到备份下一跳信息。
[SwitchA] display ip routing-table 4.4.4.4 verbose Summary Count : 1 Destination: 4.4.4.4/32 Protocol: Static Process ID: 0 SubProtID: 0x0 Age: 04h20m37s Cost: 0 Preference: 60 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0x2 OrigAs: 0 NibID: 0x26000002 LastAs: 0 AttrID: 0xffffffff Neighbor: 0.0.0.0 Flags: 0x1008c OrigNextHop: 13.13.13.2 Label: NULL RealNextHop: 13.13.13.2 BkLabel: NULL BkNextHop: 12.12.12.2 Tunnel ID: Invalid Interface: Vlan-interface200 BkTunnel ID: Invalid BkInterface: Vlan-interface100 FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A \# 在 Switch B 上查看 1.1.1.1/32 路由，可以看到备份下一跳信息。
[SwitchB] display ip routing-table 1.1.1.1 verbose Summary Count : 1

Destination: 1.1.1.1/32 Protocol: Static Process ID: 0 SubProtID: 0x0 Age: 04h20m37s Cost: 0 Preference: 60 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0x2 OrigAs: 0 NibID: 0x26000002 LastAs: 0 AttrID: 0xffffffff Neighbor: 0.0.0.0 Flags: 0x1008c OrigNextHop: 13.13.13.1 Label: NULL RealNextHop: 13.13.13.1 BkLabel: NULL BkNextHop: 24.24.24.2 Tunnel ID: Invalid Interface: Vlan-interface200 BkTunnel ID: Invalid BkInterface: Vlan-interface101 FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A

### 2 缺省路由

2缺省路由缺省路由是在路由器没有找到匹配的路由表项时使用的路由。
如果报文的目的地不在路由表中且没有配置缺省路由，那么该报文将被丢弃，将向源端返回一个ICMP 报文报告该目的地址或网络不可达。
缺省路由有两种生成方式：
• 第一种是网络管理员手工配置。配置请参见“1.2 配置静态路由”，将目的地址与掩码配置为全零（0.0.0.0 0.0.0.0）。
• 第二种是动态路由协议生成（如 OSPF、IS-IS 和 RIP），由路由能力比较强的路由器将缺省路由发布给其它路由器，其它路由器在自己的路由表里生成指向那台路由器的缺省路由。配置请参见各个路由协议手册。

## 03-RIP配置

目 录简介配置任务简介配置接口的工作状态配置 的路由信息控制配置 发布缺省路由配置 引入外部路由配置RIP最大等价路由条数配置 报文的最大长度

配置RIP配置 报文单跳检测配置 快速重路由功能配置RIP快速重路由支持BFD检测功能基本功能配置举例与 联动配置举例（指定目的地址的 报文单跳检测）
1

### RIP

#### 1.1 RIP简介

RIP（Routing Protocol，路由信息协议）是一种基于距离矢量（Distance-Vector）算法Information的内部网关协议（Interior Gateway Protocol，IGP），它通过 UDP 报文进行路由信息的交换，使用的端口号为 520。RIP 适用于小型网络。

##### 1.1.1 RIP的路由度量值

使用跳数来衡量到达目的地址的距离，跳数称为度量值。在 中，路由器到与它直接相连网RIP RIP络的跳数为 0，通过一个路由器可达的网络的跳数为 1，其余依此类推。为限制收敛时间，RIP 规定度量值取 0～15 之间的整数，大于或等于 16 的跳数被定义为无穷大，即目的网络或主机不可达。
由于这个限制，使得 RIP 不适合应用于大型网络。

##### 1.1.2 RIP的路由数据库

每个运行 RIP 的路由器管理一个路由数据库，该路由数据库包含了到所有可达目的地的路由项，这些路由项包含下列信息：
• 目的地址：主机或网络的地址。
• 下一跳地址：为到达目的地，需要经过的相邻路由器的接口 IP 地址。
• 出接口：本路由器转发报文的出接口。
• 度量值：本路由器到达目的地的开销。
• 路由时间：从路由项最后一次被更新到现在所经过的时间，路由项每次被更新时，路由时间重置为 0。
• 路由标记（Route Tag）：用于标识外部路由，在路由策略中可根据路由标记对路由信息进行灵活的控制。关于路由策略的详细信息，请参见“三层技术-IP 路由配置指导”中的“路由策略”。

##### 1.1.3 RIP的运行过程

RIP 的运行过程如下：
(1) 路由器启动 RIP 后，便会向相邻的路由器发送请求报文（Request message），相邻的 RIP路由器收到请求报文后，响应该请求，回送包含本地路由表信息的响应报文（Response message）。
路由器收到响应报文后，更新本地路由表，同时向相邻路由器发送触发更新报文，通告路由
(2)
更新信息。相邻路由器收到触发更新报文后，又向其各自的相邻路由器发送触发更新报文。
在一连串的触发更新广播后，各路由器都能得到并保持最新的路由信息。
(3) 路由器周期性向相邻路由器发送本地路由表，运行 RIP 协议的相邻路由器在收到报文后，对本地路由进行维护，选择一条最佳路由，再向其各自相邻网络发送更新信息，使更新的路由最终能达到全局有效。同时，RIP 采用老化机制对超时的路由进行老化处理，以保证路由的实时性和有效性。

##### 1.1.4 RIP防止路由环路的机制

协议向邻居通告的是自己的路由表，有可能会发生路由环路，可以通过以下机制来避免：
RIP计数到无穷（Counting infinity）：将度量值等于 的路由定义为不可达（infinity）。在路
• to 16由环路发生时，某条路由的度量值将会增加到 16 ，该路由被认为不可达。
• 触发更新（Triggered Updates）：RIP 通过触发更新来避免在多个路由器之间形成路由环路的可能，而且可以加速网络的收敛速度。一旦某条路由的度量值发生了变化，就立刻向邻居路由器发布更新报文，而不是等到更新周期的到来。

水平分割（Split Horizon）：RIP 从某个接口学到的路由，不会从该接口再发回给邻居路由器。
•这样不但减少了带宽消耗，还可以防止路由环路。
毒性逆转（Poison Reverse）：RIP 从某个接口学到路由后，将该路由的度量值设置为 16（不
•可达），并从原接口发回邻居路由器。利用这种方式，可以清除对方路由表中的无用信息。

##### 1.1.5 RIP的版本

RIP 有两个版本：RIP-1 和 RIP-2。
RIP-1 是有类别路由协议（Classful Routing Protocol），它只支持以广播方式发布协议报文。RIP-1的协议报文无法携带掩码信息，它只能识别 A、B、C 类这样的自然网段的路由，因此 不支RIP-1持不连续子网（Discontiguous Subnet）。
RIP-2 是一种无类别路由协议（Classless Routing Protocol），与 RIP-1 相比，它有以下优势：
• 支持路由标记，在路由策略中可根据路由标记对路由进行灵活的控制。
• 报文中携带掩码信息，支持路由聚合和 CIDR（Classless Inter-Domain Routing，无类域间路由）。
• 支持指定下一跳，在广播网上可以选择到最优下一跳地址。
• 支持组播路由发送更新报文，只有 RIP-2 路由器才能收到更新报文，减少资源消耗。
• 支持对协议报文进行验证，并提供明文验证和 MD5 验证两种方式，增强安全性。
RIP-2 有两种报文传送方式：广播方式和组播方式，缺省将采用组播方式发送报文，使用的组播地址为 224.0.0.9。当接口运行 RIP-2 广播方式时，也可接收 RIP-1 的报文。

##### 1.1.6 协议规范

与 相关的协议规范有：
RIP 1058：Routing
• RFC Information Protocol 1723：RIP
• RFC Version 2 - Carrying Additional Information RFC 1721：RIP Version 2 Protocol Analysis
•RFC 1722：RIP Version 2 Protocol Applicability Statement
•RFC 1724：RIP Version 2 MIB Extension
•RFC 2082：RIP-2 MD5 Authentication
•
• RFC 2091：Triggered Extensions to RIP to Support Demand Circuits
• RFC 2453：RIP Version 2

#### 1.2 RIP配置任务简介

RIP 配置任务如下：
(1) 配置RIP的基本功能
a. 启动 RIP
b. （可选）配置接口的工作状态
c. （可选）配置RIP版本
d. 配置RIP邻居

如果在不支持广播或组播报文的链路上运行 RIP，则必须手工指定 RIP 的邻居。
(2) （可选）配置RIP的路由信息控制配置接口附加度量值(cid:123)
配置RIP-2 路由聚合(cid:123)
禁止RIP接收主机路由(cid:123)
配置RIP发布缺省路由(cid:123)
配置RIP对接收/发布的路由进行过滤(cid:123)
配置RIP协议优先级(cid:123)
配置RIP引入外部路由(cid:123)
(3) （可选）调整和优化RIP网络配置RIP定时器(cid:123)
配置水平分割和毒性逆转(cid:123)
配置RIP最大等价路由条数(cid:123)
配置RIP触发更新的时间间隔(cid:123)
配置RIP报文的发送速率(cid:123)
配置RIP报文的最大长度(cid:123)
配置RIP发送协议报文的DSCP优先级(cid:123)
（可选）配置RIP网管功能
(4)
（可选）提高 的可靠性
(5) RIP配置RIP GR (cid:123)
配置RIP NSR (cid:123)
配置RIP与BFD联动(cid:123)
配置RIP快速重路由功能(cid:123)
(6) （可选）提高RIP的安全性配置RIP-1 报文的零域检查(cid:123)
配置源地址检查(cid:123)
配置RIP-2 报文的认证方式(cid:123)

#### 1.3 配置RIP的基本功能

##### 1.3.1 配置限制和指导

目前，系统支持 RIP 多进程。当在一台路由器上启动多个 RIP 进程时，需要指定不同的进程号。
RIP 进程号是本地概念，不影响与其它路由器之间的报文交换。因此，不同的路由器之间，即使进程号不同也可以进行报文交换。

###### 1. 功能简介

##### 1.3.2 启动RIP

功能简介
1.
RIP 只在指定网段的接口上运行，指定网段的同时可以配置反码；对于不在指定网段上的接口，RIP既不在它上面接收和发送路由，也不将它的接口路由发布出去。因此，RIP 启动后必须指定其工作网段。

###### 2. 配置限制和指导

• 启动 RIP 前在接口视图下配置了 RIP 相关命令，这些配置只有在 RIP 启动后才会生效。
• RIP 不支持将同一物理接口下的不同网段使能到不同的 RIP 进程中。
• RIP 不支持在同一物理接口下使能多个 RIP 进程。
• 在指定接口上使能 RIP 的优先级高于在指定网段上使能 RIP。

###### 3. 在指定网段上使能RIP

(1) 进入系统视图。
system-view
(2) 启动 RIP，并进入 RIP 视图。
rip [ process-id ] [ vpn-instance vpn-instance-name ]
缺省情况下，系统没有启动 RIP。
(3) 在指定网段上使能 RIP。
network network-address [ wildcard-mask ]
缺省情况下，没有网段使能 RIP。
在单进程情况下，可以使用 命令在所有接口上使能 RIP。在多进程情况下，
network 0.0.0.0
无法使用 network 0.0.0.0 命令。

###### 4. 在指定接口上使能RIP

(1) 进入系统视图。
system-view
(2) 启动 RIP，并进入 RIP 视图。
rip [ process-id ] [ vpn-instance vpn-instance-name ]
缺省情况下，系统没有启动 RIP 。
(3) 退回系统视图。
quit
(4) 进入接口视图。
interface interface-type interface-number
(5) 在指定接口上使能 RIP。
rip process-id enable [ exclude-subip ]
缺省情况下，接口上没有使能 。
RIP

###### 1. 功能简介

##### 1.3.3 配置接口的工作状态

功能简介
1.
可对接口的工作状态进行配置，具体包括：
• 配置接口工作在抑制状态，即接口只接收 RIP 报文而不发送 RIP 报文。
• 配置禁止接口接收 RIP 报文。
• 配置禁止接口发送 RIP 报文。

###### 2. 配置限制和指导

silent-interface 命令用来抑制接口，使其只接收 RIP 报文，更新自己的路由表，但不发送报文。命令 比命令 和 的优先级都高。
RIP silent-interface rip input rip output silent-interface all 表示抑制所有接口，在配置该命令后，所有接口都被抑制，rip input和 rip output 将不会生效。

###### 3. 配置接口工作在抑制状态

(1) 进入系统视图。
system-view
(2) 进入 RIP 视图。
rip [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 配置抑制接口。
silent-interface { interface-type interface-number | all }
缺省情况下，允许所有接口发送路由更新报文。
若抑制接口收到非知名端口的单播请求，会发送响应报文。

###### 4. 配置禁止接口接收RIP报文

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置禁止接口接收 RIP 报文。
undo rip input
缺省情况下，允许接口接收 RIP 报文。

###### 5. 配置禁止接口发送RIP报文

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置禁止接口发送 RIP 报文。
undo rip output
缺省情况下，允许接口发送 RIP 报文。

###### 1. 功能简介

###### 3. 配置步骤

##### 1.3.4 配置RIP版本

功能简介
1.
用户可以在 RIP 视图下配置 RIP 版本，也可在接口上配置 RIP 版本：
• 当全局和接口都没有进行 RIP 版本配置时，接口发送 RIP-1 广播报文，可以接收 RIP-1 广播/单播报文、RIP-2 广播/组播/单播报文。
如果接口上配置了 RIP 版本，以接口配置的为准；如果接口没有进行 RIP 版本配置，接口运
•行的 版本将以全局配置的版本为准。
RIP

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置 RIP 版本。
请依次执行以下命令在 RIP 视图下配置 RIP 版本。
(cid:123)
rip [ process-id ] [ vpn-instance vpn-instance-name ]
version { 1 | 2 }
缺省情况下，未配置全局 版本。接口只能发送 广播报文，可以接收 广播
RIP RIP-1 RIP-1
/单播报文、RIP-2 广播/组播/单播报文。
请依次执行以下命令在接口视图下配置 RIP 版本。
(cid:123)
interface interface-type interface-number
rip version { 1 | 2 [ broadcast | multicast ] }
缺省情况下，未配置接口运行的 版本。接口只能发送 广播报文，可以接收
RIP RIP-1 RIP-1
广播/单播报文、RIP-2 广播/组播/单播报文。

##### 1.3.5 配置RIP邻居

###### 1. 功能简介

通常情况下，RIP 使用广播或组播地址发送报文，如果在不支持广播或组播报文的链路上运行 RIP，则必须手工指定 RIP 的邻居。

###### 2. 配置限制和指导

当 邻居与当前设备直连时不推荐使用 命令，因为这样可能会造成对端同时RIP peer ip-address收到同一路由信息的组播（或广播）和单播两种形式的报文。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 进入 RIP 视图。
rip [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 配置 RIP 邻居。
peer ip-address缺省情况下，RIP 不向任何定点地址发送单播更新报文。

###### 2. 配置步骤

##### 1.4.2 配置RIP-2路由聚合

(4) 关闭对接收到的 RIP 路由更新报文进行源 IP 地址检查的功能。
undo validate-source-address
缺省情况下，对接收到的 RIP 路由更新报文进行源 IP 地址检查的功能处于使能状态。
当指定的邻居和本地路由器非直接连接，则必须关闭对更新报文的源地址进行检查的功能。

#### 1.4 配置RIP的路由信息控制

##### 1.4.1 配置接口附加度量值

###### 1. 功能简介

附加度量值是在 RIP 路由原来度量值的基础上所增加的度量值（跳数），包括发送附加度量值和接收附加度量值。
• 发送附加度量值：不会改变路由表中的路由度量值，仅当接口发送 RIP 路由信息时才会添加到发送路由上。
接收附加度量值：会影响接收到的路由度量值，接口接收到一条合法的 RIP 路由时，在将其
•加入路由表前会把度量值附加到该路由上，当附加度量值与原路由度量值之和大于 时，该16条路由的度量值取 16。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置接口接收 RIP 路由时的附加度量值。
rip metricin [ route-policy route-policy-name ] value缺省情况下，接口接收 RIP 路由时的附加路由度量值为 0。
(4) 配置接口发送 RIP 路由时的附加度量值。
rip metricout [ route-policy route-policy-name ] value缺省情况下，接口发送 路由时的附加路由度量值为 1。
RIP配置 路由聚合
1.4.2 RIP-2

###### 1. 功能简介

路由聚合是指路由器把同一自然网段内的连续子网的路由聚合成一条路由向外发送，如路由表里有
10.1.1.0/24、10.1.2.0/24、10.1.3.0/24 三条路由，可以通过配置把它们聚合成一条路由 10.1.0.0/16向外发送，这样邻居路由器只接收到一条路由 10.1.0.0/16，从而减少了路由表的规模，以及网络上的传输流量。
通过配置路由聚合，可以提高网络的可扩展性以及路由器的处理速度。
将多条路由聚合成一条路由时，聚合路由的 值将取所有路由 的最小值。
RIP-2 Metric Metric在 RIP-2 中，有两种路由聚合方式：自动路由聚合和手工配置聚合路由。

自动路由聚合是指 RIP-2 将同一自然网段内的不同子网的路由聚合成一条自然掩码的路由向
•外发送，例如，假设路由表里有 10.1.1.0/24、10.1.2.0/24、10.1.3.0/24 三条路由，使能RIP-2自动路由聚合功能后，这三条路由聚合成一条自然掩码的路由 10.0.0.0/8 向外发送。
• 手工路由聚合是指用户可在指定接口配置 RIP-2 发布一条聚合路由。如果路由落入聚合路由网段内，则 RIP-2 不发布该路由，只发布配置的聚合路由。例如，假设路由表里有 10.1.1.0/24、
10.1.2.0/24、10.1.3.0/24 三条子网连续的路由，在接口 配置发布一Ten-GigabitEthernet1/0/1条聚合路由 10.1.0.0/16 后，这三条路由聚合成一条路由 10.1.0.0/16 向外发送。缺省情况下，RIP-2 的路由将按照自然掩码自动聚合，如果用户在指定接口配置发布一条聚合路由，则必须先关闭自动聚合功能。

###### 2. 配置限制和指导

路由聚合在某些情况会产生路由环路，所以在路由聚合时需要配置出接口为 的黑洞路由。
NULL0报文匹配到黑洞路由时，直接丢弃该报文，避免产生环路。

###### 3. 自动路由聚合

(1) 进入系统视图。
system-view
(2) 进入 RIP 视图。
rip [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 使能 RIP-2 自动路由聚合功能。
summary
缺省情况下，RIP-2 自动路由聚合功能处于使能状态。
如果路由表里的路由子网不连续，则需要取消自动路由聚合功能，使得 RIP-2 能够向外发布
子网路由和主机路由。

###### 4. 手工配置聚合路由

(1) 进入系统视图。
system-view
(2) 进入 RIP 视图。
rip [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 关闭 RIP-2 自动路由聚合功能。
undo summary
缺省情况下，RIP-2 自动路由聚合功能处于使能状态。
(4) 退回系统视图。
quit
(5) 进入接口视图。
interface interface-type interface-number
(6) 配置发布一条聚合路由。
rip summary-address ip-address { mask-length | mask }
缺省情况下，未配置聚合路由。

###### 1. 功能简介

##### 1.4.3 禁止RIP接收主机路由

功能简介
1.
在某些特殊情况下，路由器会收到大量来自同一网段的主机路由。这些路由对于路由寻址没有多少作用，却占用了大量的资源，此时可配置 禁止接收主机路由，以节省网络资源。功能仅对RIP RIPv2报文携带的路由有效，对 RIPv1 报文携带的路由无效。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 RIP 视图。
rip [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 禁止 RIP 接收主机路由。
undo host-route
缺省情况下，允许 RIP 接收主机路由。

##### 1.4.4 配置RIP发布缺省路由

###### 1. 功能简介

用户可以配置 RIP 以指定度量值向邻居发布一条缺省路由。
• 用户可以在 RIP 视图下配置 RIP 进程的所有接口向邻居发布缺省路由，也可以在接口下配置指定 RIP 接口向邻居发布缺省路由。
• 如果接口没有进行发布缺省路由的相关配置，则以 RIP 进程下的配置为准，否则将以接口配置为准。
• 如果 RIP 进程配置了发布缺省路由，但希望该进程下的某个接口不发送缺省路由（只发布普通路由），可以通过在接口下配置 rip default-route no-originate 命令实现。
配置发布缺省路由的 RIP 路由器不接收来自 RIP 邻居的缺省路由。

###### 2. 配置步骤

进入系统视图。
(1)
system-view配置 发布缺省路由。
(2) RIP请依次执行以下命令在 视图下配置发布缺省路由。
RIP (cid:123)
rip [ process-id ] [ vpn-instance vpn-instance-name ] default-route { only | originate } [ cost cost-value | route-policy route-policy-name ] *缺省情况下，RIP 不向邻居发送缺省路由。
请依次执行以下命令在接口视图下配置发布缺省路由。
(cid:123)
interface interface-type interface-number rip default-route { { only | originate } [ cost cost-value | route-policy route-policy-name ] * | no-originate }

缺省情况下，RIP 接口是否发布缺省路由以 RIP 进程配置的为准。

##### 1.4.5 配置RIP对接收/发布的路由进行过滤

###### 1. 功能简介

路由过滤就是通过指定访问控制列表或 地址前缀列表，配置入口或出口过滤策略，对接收和发布IP的路由进行过滤。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 RIP 视图。
rip [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 对接收的路由信息进行过滤。
filter-policy { ipv4-acl-number | gateway prefix-list-name | prefix-list
prefix-list-name [ gateway prefix-list-name ] } import [ interface-type
interface-number ]
缺省情况下，RIP 不对接收的路由信息进行过滤。
本命令对从邻居收到的 RIP 路由进行过滤，没有通过过滤的路由将不被加入路由表，也不向
邻居发布该路由。
对发布的路由信息进行过滤。
(4)
filter-policy { ipv4-acl-number | prefix-list prefix-list-name } export
[ protocol [ process-id ] | interface-type interface-number ]
缺省情况下，RIP 不对发布的路由信息进行过滤。
本命令对本机所有路由的发布进行过滤，包括使用import-route 引入的路由和从邻居学到
的 RIP 路由。

##### 1.4.6 配置RIP协议优先级

###### 1. 功能简介

在路由器中可能会运行多个 IGP 路由协议，如果想让 RIP 路由具有比从其它路由协议学来的路由更高的优先级，需要配置小的优先级值。优先级的高低将最后决定 IP 路由表中的路由是通过哪种路由算法获取的最佳路由。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
进入 视图。
(2) RIP
rip [ process-id ] [ vpn-instance vpn-instance-name ]
配置 路由的优先级。
(3) RIP
preference { preference | route-policy route-policy-name } *
缺省情况下，RIP 路由的优先级为 100。

###### 1. 功能简介

##### 1.4.7 配置RIP引入外部路由

功能简介
1.
如果在路由器上不仅运行 RIP，还运行着其它路由协议，可以配置 RIP 引入其它协议生成的路由，如 OSPF、IS-IS、BGP、静态路由或者直连路由。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
进入 视图。
(2) RIP
rip [ process-id ] [ vpn-instance vpn-instance-name ]
引入外部路由。
(3)
配置 引入 BGP 协议的路由。
RIP
(cid:123)
import-route bgp [ as-number ] [ allow-ibgp ] [ cost cost-value |
route-policy route-policy-name | tag tag ] *
配置 引入直连或静态路由。
RIP
(cid:123)
import-route { direct | static } [ cost cost-value | route-policy
route-policy-name | tag tag ] *
配置 RIP 引入 isis、ospf 协议或其他 rip 进程的路由。
(cid:123)
import-route { isis | ospf | rip } [ process-id | all-processes ]
[ allow-direct | cost cost-value | route-policy route-policy-name |
tag tag ] *
缺省情况下，RIP 不引入其它路由。
只能引入路由表中状态为 active 的路由，是否为 active 状态可以通过 display ip
命令来查看。
routing-table protocol
（可选）配置引入路由的缺省度量值。
(4)
default cost cost-value
缺省情况下，引入路由的缺省度量值为 0。

#### 1.5 调整和优化RIP网络

##### 1.5.1 配置RIP定时器

###### 1. 功能简介

通过调整 RIP 定时器可以改变 RIP 网络的收敛速度。
RIP 受四个定时器的控制，分别是 Update、Timeout、Suppress 和 Garbage-Collect。
• Update 定时器：定义了发送路由更新的时间间隔。
• Timeout 定时器：定义了路由老化时间。如果在老化时间内没有收到关于某条路由的更新报文，则该条路由在路由表中的度量值将会被设置为 16。

###### 3. 配置步骤

Suppress 定时器：定义了 RIP 路由处于抑制状态的时长。当一条路由的度量值变为 16 时，
•该路由将进入抑制状态。在被抑制状态，只有来自同一邻居且度量值小于 的路由更新才会16被路由器接收，取代不可达路由。
• Garbage-Collect 定时器：定义了一条路由从度量值变为 16 开始，直到它从路由表里被删除所经过的时间。在 Garbage-Collect 时间内，RIP 以 16 作为度量值向外发送这条路由的更新，如果 超时，该路由仍没有得到更新，则该路由将从路由表中被彻底删除。
Garbage-Collect

###### 2. 配置限制和指导

定时器值的调整应考虑网络的性能，并在所有运行 RIP 的路由器上进行统一配置，以免增加不必要的网络流量或引起网络路由震荡。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 进入 RIP 视图。
rip [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 配置 RIP 定时器的值。
timers { garbage-collect garbage-collect-value | suppress suppress-value | timeout timeout-value | update update-value } *缺省情况下，Garbage-collect 定时器的值为 120 秒，Suppress 定时器的值为 120 秒，定时器的值为 秒，Update 定时器的值为 秒。
Timeout 180 30

##### 1.5.2 配置水平分割和毒性逆转

###### 1. 功能简介

通过配置水平分割或毒性逆转功能可以防止路由环路。
配置水平分割可以使得从一个接口学到的路由不能通过此接口向外发布，用于避免相邻路由
•器间的路由环路。
• 配置毒性逆转后，从一个接口学到的路由还可以从这个接口向外发布，但这些路由的度量值会设置为 16（即不可达），可以用于避免相邻路由器间的路由环路。

###### 2. 配置限制和指导

如果同时配置了水平分割和毒性逆转，则只有毒性逆转功能生效。

###### 3. 配置水平分割

进入系统视图。
(1)
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 使能水平分割功能。
rip split-horizon缺省情况下，水平分割功能处于使能状态。

###### 4. 配置毒性逆转

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 使能毒性逆转功能。
rip poison-reverse
缺省情况下，毒性逆转功能处于关闭状态。

##### 1.5.3 配置RIP最大等价路由条数

###### 1. 功能简介

通过配置 RIP 最大等价路由条数，可以使用多条等价路由对 RIP 网络进行负载分担。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 RIP 视图。
rip [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 配置 RIP 最大等价路由条数。
maximum load-balancing number
缺省情况下，RIP 支持的等价路由的最大条数与系统支持最大等价路由的条数相同。

##### 1.5.4 配置RIP触发更新的时间间隔

###### 1. 功能简介

RIP 路由信息变化后将以触发更新的方式通知邻居设备，加速邻居设备的路由收敛。如果路由信息频繁变化，且每次变化都立即发送触发更新，将会占用大量系统资源，并影响路由器的效率。通过调节触发更新的时间间隔，可以抑制由于路由信息频繁变化带来的影响。本命令在路由信息变化不频繁的情况下将连续触发更新的时间间隔缩小到 minimum-interval，而在路由信息变化频繁的n-2情况下可以进行相应惩罚，增加 incremental-interval×2 （n 为连续触发更新的次数），将等待时间按照配置的惩罚增量延长，最大不超过 maximum-interval。

###### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入 RIP 视图。
rip [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 配置 RIP 触发更新的时间间隔。
timer triggered maximum-interval [ minimum-interval [ incremental-interval ] ]

###### 2. 配置步骤

缺省情况下，发送触发更新的最大时间间隔为 5 秒，最小间隔为 50 毫秒，增量惩罚间隔为 200毫秒。

##### 1.5.5 配置RIP报文的发送速率

###### 1. 功能简介

RIP 周期性地将路由信息放在 RIP 报文中向邻居发送。
如果路由表里的路由条目数量很多，同时发送大量 RIP 协议报文有可能会对当前设备和网络带宽带来冲击；因此，路由器将 RIP 协议报文分为多个批次进行发送，并且对 RIP 接口每次允许发送的RIP 协议报文最大个数做出限制。
用户可根据需要配置接口发送 RIP 报文的时间间隔以及接口一次发送 RIP 报文的最大个数。

###### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 配置 RIP 报文的发送速率。
请依次执行以下命令在 RIP 视图下配置所有接口的 RIP 报文发送速率。
(cid:123)
rip [ process-id ] [ vpn-instance vpn-instance-name ]配置 RIP 报文的发送速率。
output-delay time count count缺省情况下，接口发送 RIP 报文的时间间隔为 20 毫秒，一次最多发送 3 个 RIP 报文。
请依次执行以下命令在接口视图下配置某个接口的 RIP 报文发送速率。
(cid:123)
interface interface-type interface-number配置 RIP 报文的发送速率。
rip output-delay time count count缺省情况下，接口发送 RIP 报文的速率以 RIP 进程配置的为准。

##### 1.5.6 配置RIP报文的最大长度

###### 1. 功能简介

RIP 周期性地将路由信息放在 RIP 报文中向邻居发送，根据 RIP 报文的最大长度来计算报文中发送的最大路由数。通过设置 RIP 报文的最大长度，可以合理利用链路带宽。
在配置认证的情况下，如果配置不当可能会造成报文无法发送，建议用户按照下面进行配置：
• 简单验证方式时，RIP 报文的最大长度不小于 52 字节；
• MD5 验证方式（使用 RFC 2453 规定的报文格式）时，RIP 报文的最大长度不小于 56 字节；
• MD5 验证方式（使用 RFC 2082 规定的报文格式）时，RIP 报文的最大长度不小于 72 字节。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number

##### 2. 配置步骤

(3) 配置 RIP 报文的最大长度。
rip max-packet-length value
缺省情况下，接口发送 RIP 报文的最大长度为 512 字节。

##### 1.5.7 配置RIP发送协议报文的DSCP优先级

###### 1. 功能简介

DSCP 优先级用来体现报文自身的优先等级，决定报文传输的优先程度。通过本配置可以指定 RIP发送协议报文的 优先级。
DSCP

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 RIP 视图。
rip [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 配置 RIP 发送协议报文的 DSCP 优先级。
dscp dscp-value
缺省情况下，RIP 发送协议报文的 优先级为 48。
DSCP

#### 1.6 配置RIP网管功能

##### 1. 功能简介

配置 RIP 进程绑定 MIB 功能后，可以通过网管软件对指定的 RIP 进程进行管理。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 配置 RIP 进程绑定 MIB。
rip mib-binding process-id缺省情况下，MIB 绑定在进程号最小的 RIP 进程上。

#### 1.7 配置RIP GR

##### 1. 功能简介

GR（Graceful Restart，平滑重启）是一种在协议重启或主备倒换时 RIP 进行平滑重启，保证转发业务不中断的机制。
有两个角色：
GR Restarter：发生协议重启或主备倒换事件且具有 能力的设备。
• GR GR：和 具有邻居关系，协助完成 流程的设备。
• GR Helper GR Restarter GR在普通的路由协议重启的情况下，路由器需要重新学习 路由，并更新 表，此时会引起网络RIP FIB暂时的中断，基于 RIP 的 GR 可以解决这个问题。

##### 1. 功能简介

应用了 GR 特性的设备向外发送 RIP 全部路由表请求报文，重新从邻居处学习 RIP 路由，在此期间表不变化。在路由协议重启完毕后，设备将重新学到的 路由下刷给 表，使该设备的路FIB RIP FIB由信息恢复到重启前的状态。
本配置在 GR Restarter 上进行，启动了 RIP 的设备缺省就是 GR Helper。

##### 2. 配置限制和指导

设备充当 GR Restarter 后不能再配置 RIP NSR 功能。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 RIP 视图。
rip [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 使能 RIP 协议的 GR 能力。
graceful-restart
缺省情况下，RIP 协议的 GR 能力处于关闭状态。
(4) （可选）配置 RIP 协议的 GR 重启间隔时间。
graceful-restart interval interval
缺省情况下，RIP 协议的 GR 重启间隔时间为 60 秒。

#### 1.8 配置RIP NSR

功能简介
1.
NSR（Nonstop Routing，不间断路由）通过将 RIP 路由信息从主进程备份到备进程，使设备在发生主备倒换时新主进程可以无缝完成路由的重新生成、下刷，邻接关系不会发生中断，从而避免了主备倒换对转发业务的影响。
GR 特性需要周边设备配合才能完成路由信息的恢复，在网络应用中有一定的限制。NSR 特性不需要周边设备的配合，网络应用更加广泛。

##### 2. 配置限制和指导

设备配置了 RIP NSR 功能后不能再充当 GR Restarter。

##### 3. 配置步骤

进入系统视图。
(1)
system-view进入 视图。
(2) RIP rip [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 使能 RIP NSR 功能。
non-stop-routing缺省情况下，RIP NSR 功能处于关闭状态。
各个进程的 NSR 功能是相互独立的，只对本进程生效。如果存在多个 RIP 进程，建议在各个进程下使能 功能。
RIP NSR

#### 1.9 配置RIP与BFD联动

##### 1.9.1 功能简介

RIP 协议依赖周期性发送路由更新请求作为检测机制，当在指定时间内没有收到路由更新回应时，认为此条路由不再生效，这种方式不能快速响应链路故障。使用 BFD（Bidirectional Forwarding Detection，双向转发检测）检测到链路故障时，RIP 能快速撤销失效路由，减少对其他业务的影响。
关于 BFD 的介绍和基本功能配置，请参见“可靠性配置指导”中的“BFD”。
目前 RIP 支持 BFD 提供了下面几种检测方式：
• echo 报文单跳检测方式：直连邻居使用。在对端有 RIP 路由发送时才能建立 BFD 会话。
• 指定目的地址的 echo 报文单跳检测方式：直连邻居使用，并且在接口上直接指定 RIP 邻居的IP 地址。当该接口使能了 RIP 功能，会建立到指定目的 IP 地址的 BFD 会话。在链路出现单通故障时，本特性可以加快路由收敛速度。链路出现故障时，本端设备不再从该接口收发任何 报文，链路恢复后，接口将继续发送 报文。
RIP RIP报文双向检测方式：非直连邻居使用。当两端互有 路由发送时，且使能 的接
• control RIP BFD口与接收接口为同一接口，邻居之间才能建立 BFD 会话。

##### 1.9.2 配置限制和指导

rip bfd enable 命令与 rip bfd enable destination 命令互斥，不能同时使用。

##### 1.9.3 配置echo报文单跳检测

(1) 进入系统视图。
system-view
(2) 配置 echo 报文源地址。
bfd echo-source-ip ip-address
缺省情况下，未配置 报文源地址。
echo
进入接口视图。
(3)
interface interface-type interface-number
(4) 使能 RIP 的 BFD 功能。
rip bfd enable
缺省情况下，RIP 的 BFD 功能处于关闭状态。

##### 1.9.4 配置指定目的地址的echo报文单跳检测

###### 1. 配置限制和指导

本特性只检测本端到 RIP 直连邻居的链路的连通状况。配置本特性时，指定的目的地址只能是 RIP直连邻居的 IP 地址。

###### 2. 配置步骤

(1) 进入系统视图。
system-view

(2) 配置 echo 报文源地址。
bfd echo-source-ip ip-address
缺省情况下，未配置 echo 报文源地址。
(3) 进入接口视图。
interface interface-type interface-number
(4) 使能 RIP 指定目的地址的 BFD 功能。
rip bfd enable destination ip-address
缺省情况下，RIP 的 BFD 功能处于关闭状态。

##### 1.9.5 配置control报文双向检测

进入系统视图。
(1)
system-view
(2) 进入 RIP 视图。
rip [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 配置 RIP 邻居。
peer ip-address缺省情况下，RIP 不向任何定点地址发送更新报文。
由于 peer 命令与邻居之间没有对应关系，undo peer 操作并不能立刻删除邻居，因此不能立刻删除 会话。
BFD
(4) 进入接口视图。
interface interface-type interface-number
(5) 使能 RIP 的 BFD 功能。
rip bfd enable缺省情况下，RIP 的 BFD 功能处于关闭状态。

#### 1.10 配置RIP快速重路由功能

##### 1.10.1 功能简介

当 RIP 网络中的链路或某台路由器发生故障时，数据流量将会被中断，直到 RIP 根据新的拓扑网络路由收敛完毕后，被中断的流量才能恢复正常的传输。
为了尽可能缩短网络故障导致的流量中断时间，网络管理员可以根据需要配置RIP快速重路由功能。
图1-1 RIP 快速重路由功能示意图

###### 1. 功能简介

如 图 1-1 所示，通过在Router B上配置快速重路由功能，RIP可以为路由指定备份下一跳，当Router B检测到网络故障时，RIP会使用事先获取好的备份下一跳替换失效下一跳，通过备份下一跳来指导报文的转发，从而大大缩短了流量中断时间。在使用备份下一跳指导报文转发的同时，RIP会根据变化后的网络拓扑重新计算路由，网络收敛完毕后，使用新计算出来的最优路由来指导报文转发。

##### 1.10.2 配置限制和指导

本功能只适合在主链路三层接口 up，主链路由双通变为单通或者不通的情况下使用。在主链路三层接口 down 的情况下，本功能不可用。
单通现象，即一条链路上的两端，有且只有一端可以收到另一端发来的报文，此链路称为单向链路。
RIP 快速重路由功能仅对非迭代 RIP 路由（即从直连邻居学到 RIP 路由）有效。
等价路由不支持快速重路由功能。

##### 1.10.3 开启RIP快速重路由功能

(1) 进入系统视图。
system-view
(2) 配置路由策略。
在路由策略中通过 apply fast-reroute backup-interface 命令在路由策略中指定备
份下一跳。
详细配置请参见“三层技术-IP 路由配置指导”中的“路由策略”。
(3) 进入 RIP 视图。
rip [ process-id ] [ vpn-instance vpn-instance-name ]
(4) 开启 RIP 快速重路由功能。
fast-reroute route-policy route-policy-name
缺省情况下，RIP 快速重路由功能处于关闭状态。

##### 1.10.4 配置RIP快速重路由支持BFD检测功能

功能简介
1.
RIP 协议的快速重路由特性中，主用链路缺省不使用 BFD 进行链路故障检测。配置本功能后，将使用 进行检测，可以加快 协议的收敛速度。
BFD RIP

###### 2. 配置步骤

(1) 进入系统视图。
system-view
配置 报文源地址。
(2) BFD Echo
bfd echo-source-ip ip-address
缺省情况下，未配置 报文源地址。
BFD Echo
报文的源 地址用户可以任意指定。建议配置 报文的源 地址不属于该设备任何
echo IP echo IP
一个接口所在网段。
本命令的详细情况请参见“可靠性命令参考”中的“BFD”。

###### 1. 功能简介

(3) 进入接口视图。
interface interface-type interface-number
(4) 使能 RIP 协议中主用链路的 BFD（Echo 方式）检测功能。
rip primary-path-detect bfd echo
缺省情况下，RIP 协议中主用链路的 BFD（Echo 方式）检测功能处于关闭状态。

#### 1.11 提高RIP的安全性

##### 1.11.1 配置RIP-1报文的零域检查

###### 1. 功能简介

RIP-1 报文中的有些字段必须为零，称之为零域。用户可配置 RIP-1 在接收报文时对零域进行检查，零域值不为零的 RIP-1 报文将不被处理。如果用户能确保所有报文都是可信任的，则可以不进行该项检查，以节省 CPU 处理时间。
由于 RIP-2 的报文没有零域，此项配置对 RIP-2 无效。

###### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入 RIP 视图。
rip [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 使能 RIP-1 报文的零域检查功能。
checkzero缺省情况下，RIP-1 报文的零域检查功能处于使能状态。

##### 1.11.2 配置源地址检查

功能简介
1.
通过配置对接收到的 RIP 路由更新报文进行源 IP 地址检查：
• 对于在接口上接收的报文，RIP将检查该报文源地址和接收接口的IP地址是否处于同一网段，如果不在同一网段则丢弃该报文。
对于 接口上接收的报文，RIP 检查该报文的源地址是否是对端接口的 地址，如果不是
• PPP IP则丢弃该报文。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 RIP 视图。
rip [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 使能对接收到的 RIP 路由更新报文进行源 IP 地址检查功能。
validate-source-address
缺省情况下，对接收到的 RIP 路由更新报文进行源 IP 地址检查功能处于使能状态。

###### 1. 功能简介

##### 1.11.3 配置RIP-2报文的认证方式

功能简介
1.
在安全性要求较高的网络环境中，可以通过配置报文的认证方式来对 RIP-2 报文进行有效性检查和验证。
RIP-2 支持两种认证方式：简单认证和 MD5 认证。

###### 2. 配置步骤

进入系统视图。
(1)
system-view进入接口视图。
(2)
interface interface-type interface-number配置 报文的验证方式。
(3) RIP-2 rip authentication-mode { md5 { rfc2082 { cipher | plain } string key-id | rfc2453 { cipher | plain } string } | simple { cipher | plain } string }缺省情况下，未配置 的验证方式。
RIP-2当 的版本为 时，虽然在接口视图下仍然可以配置验证方式，但由于 不支持RIP RIP-1 RIP-1认证，因此该配置不会生效。

#### 1.12 RIP显示和维护

在完成上述配置后，在任意视图下执行 命令可以显示配置后 的运行情况，通过查看display RIP显示信息验证配置的效果。
在用户视图下执行 reset 命令可以重启 RIP 进程或清除指定 RIP 进程的统计信息。
表1-1 显示和维护RIP操作 命令显示RIP的当前运行状态及配置信息 display rip [ process-id ]显示RIP进程的GR状态信息 display rip [ process-id ] graceful-restart显示RIP进程的NSR状态信息 display rip [ process-id ] non-stop-routing display rip process-id database [ ip-address显示RIP数据库的激活路由{ mask-length | mask } ] display rip process-id interface [ interface-type显示RIP的接口信息interface-number ] display rip process-id neighbor [ interface-type显示RIP进程的邻居信息interface-number ] display rip process-id route [ ip-address { mask-length显示RIP的路由信息| mask } [ verbose ] | peer ip-address | statistics ]重启指定 进程 reset rip process-id process RIP清除RIP进程的统计信息 reset rip process-id statistics

###### 2. 组网图

###### 3. 配置步骤

#### 1.13 RIP典型配置举例

##### 1.13.1 RIP基本功能配置举例

###### 1. 组网需求

• 在 Switch A 和 Switch B 的所有接口上使能 RIP，并使用 RIP-2 进行网络互连。
在 上配置路由出策略，向 发布的路由中过滤掉 10.2.1.0/24；Switch 上
• Switch B Switch A B
配置入策略，使得 Switch B 只接收路由 2.1.1.0/24。
组网图
2.
图1-2 RIP 基本功能配置组网图
配置步骤
3.
(1) 配置各接口的 IP 地址（略）
(2) 配置 RIP 基本功能
\# 配置 Switch A，在指定网段上使能 RIP。
<SwitchA> system-view
[SwitchA] rip
[SwitchA-rip-1] network 1.0.0.0
[SwitchA-rip-1] network 2.0.0.0
[SwitchA-rip-1] network 3.0.0.0
[SwitchA-rip-1] quit
\# 配置 Switch B，在指定接口上使能 RIP。
<SwitchB> system-view
[SwitchB] rip
[SwitchB-rip-1] quit
[SwitchB] interface vlan-interface 100
[SwitchB-Vlan-interface100] rip 1 enable
[SwitchB-Vlan-interface100] quit
[SwitchB] interface vlan-interface 101
[SwitchB-Vlan-interface101] rip 1 enable
[SwitchB-Vlan-interface101] quit
[SwitchB] interface vlan-interface 102
[SwitchB-Vlan-interface102] rip 1 enable
[SwitchB-Vlan-interface102] quit
\# 查看 Switch A 的 RIP 路由表。
[SwitchA] display rip 1 route
Route Flags: R - RIP, T - TRIP
P - Permanent, A - Aging, S - Suppressed, G - Garbage-collect

D - Direct, O - Optimal, F - Flush to RIB
---------------------------------------------------------------------------- Peer 1.1.1.2 on Vlan-interface100 Destination/Mask Nexthop Cost Tag Flags Sec
10.0.0.0/8 1.1.1.2 1 0 RAOF 11 Local route Destination/Mask Nexthop Cost Tag Flags Sec
1.1.1.0/24 0.0.0.0 0 0 RDOF -
2.1.1.0/24 0.0.0.0 0 0 RDOF -
3.1.1.0/24 0.0.0.0 0 0 RDOF -从路由表中可以看出，RIP-1 发布的路由信息使用的是自然掩码。
(3) 配置 RIP 的版本\# 在 Switch A 上配置 RIP-2。
[SwitchA] rip [SwitchA-rip-1] version 2 [SwitchA-rip-1] undo summary [SwitchA-rip-1] quit在 上配置 RIP-2。
\# Switch B [SwitchB] rip [SwitchB-rip-1] version 2 [SwitchB-rip-1] undo summary [SwitchB-rip-1] quit \# 查看 Switch A 的 RIP 路由表。
[SwitchA] display rip 1 route Route Flags: R - RIP, T - TRIP P - Permanent, A - Aging, S - Suppressed, G - Garbage-collect D - Direct, O - Optimal, F - Flush to RIB
---------------------------------------------------------------------------- Peer 1.1.1.2 on Vlan-interface100 Destination/Mask Nexthop Cost Tag Flags Sec
10.0.0.0/8 1.1.1.2 1 0 RAOF 50
10.2.1.0/24 1.1.1.2 1 0 RAOF 16
10.1.1.0/24 1.1.1.2 1 0 RAOF 16 Local route Destination/Mask Nexthop Cost Tag Flags Sec
1.1.1.0/24 0.0.0.0 0 0 RDOF -
2.1.1.0/24 0.0.0.0 0 0 RDOF -
3.1.1.0/24 0.0.0.0 0 0 RDOF -从路由表中可以看出，RIP-2 发布的路由中带有更为精确的子网掩码信息。
由于 路由信息的老化时间较长，所以在配置 版本后的一段时间里，路由表中可能RIP RIP-2还会存在 RIP-1 的路由信息。

\# 查看 Switch B 的路由表信息。
[SwitchB] display rip 1 route Route Flags: R - RIP, T - TRIP P - Permanent, A - Aging, S - Suppressed, G - Garbage-collect D - Direct, O - Optimal, F - Flush to RIB
---------------------------------------------------------------------------- Peer 1.1.1.1 on Vlan-interface100 Destination/Mask Nexthop Cost Tag Flags Sec
2.1.1.0/24 1.1.1.1 1 0 RAOF 19
3.1.1.0/24 1.1.1.1 1 0 RAOF 19 Local route Destination/Mask Nexthop Cost Tag Flags Sec
1.1.1.0/24 0.0.0.0 0 0 RDOF -
10.1.1.0/24 0.0.0.0 0 0 RDOF -
10.2.1.0/24 0.0.0.0 0 0 RDOF -配置 路由过滤
(4) RIP在 配置地址前缀列表。
\# Switch B [SwitchB] ip prefix-list aaa index 10 permit 2.1.1.0 24 [SwitchB] ip prefix-list bbb index 10 deny 10.2.1.0 24 [SwitchB] ip prefix-list bbb index 11 permit 0.0.0.0 0 less-equal 32 [SwitchB] rip 1 [SwitchB-rip-1] filter-policy prefix-list aaa import [SwitchB-rip-1] filter-policy prefix-list bbb export [SwitchB-rip-1] quit \# 查看路由过滤后 Switch A 的路由信息。
[SwitchA] display rip 1 route Route Flags: R - RIP, T - TRIP P - Permanent, A - Aging, S - Suppressed, G - Garbage-collect
---------------------------------------------------------------------------- Peer 1.1.1.2 on Vlan-interface100 Destination/Mask Nexthop Cost Tag Flags Sec
10.1.1.0/24 1.1.1.2 1 0 RAOF 19 Local route Destination/Mask Nexthop Cost Tag Flags Sec
1.1.1.0/24 0.0.0.0 0 0 RDOF -
2.1.1.0/24 0.0.0.0 0 0 RDOF -
3.1.1.0/24 0.0.0.0 0 0 RDOF - \# 查看 Switch B 的路由表信息。
[SwitchB] display rip 1 route Route Flags: R - RIP, T - TRIP P - Permanent, A - Aging, S - Suppressed, G - Garbage-collect D - Direct, O - Optimal, F - Flush to RIB
---------------------------------------------------------------------------- Peer 1.1.1.1 on Vlan-interface100 Destination/Mask Nexthop Cost Tag Flags Sec
2.1.1.0/24 1.1.1.1 1 0 RAOF 19 Local route

###### 1. 组网需求

###### 2. 组网图

Destination/Mask Nexthop Cost Tag Flags Sec
1.1.1.0/24 0.0.0.0 0 0 RDOF -
10.1.1.0/24 0.0.0.0 0 0 RDOF -
10.2.1.0/24 0.0.0.0 0 0 RDOF -

##### 1.13.2 RIP引入外部路由配置举例

组网需求
1.
• Switch B 上运行两个 RIP 进程：RIP 100 和 RIP 200。Switch B 通过 RIP 100 和 Switch A 交换路由信息，通过 和 交换路由信息。
RIP 200 Switch C在 Switch B 上配置 RIP 进程 200 引入外部路由，引入直连路由和 RIP 进程 100 的路由，使得
•Switch C 能够学习到达 10.2.1.0/24 和 11.1.1.0/24 的路由，但 Switch A 不能学习到达
12.3.1.0/24 和 16.4.1.0/24 的路由。
组网图
2.
图1-3 RIP 引入外部路由配置组网图

###### 3. 配置步骤

配置各接口的 地址（略）
(1) IP
(2) 配置 RIP 基本功能\# 在 Switch A 上启动 RIP 进程 100，并配置 RIP 版本号为 2。
<SwitchA> system-view [SwitchA] rip 100 [SwitchA-rip-100] network 10.0.0.0 [SwitchA-rip-100] network 11.0.0.0 [SwitchA-rip-100] version 2 [SwitchA-rip-100] undo summary [SwitchA-rip-100] quit \# 在 Switch B 上启动两个 RIP 进程，进程号分别为 100 和 200，并配置 RIP 版本号为 2。
<SwitchB> system-view [SwitchB] rip 100 [SwitchB-rip-100] network 11.0.0.0 [SwitchB-rip-100] version 2 [SwitchB-rip-100] undo summary [SwitchB-rip-100] quit [SwitchB] rip 200 [SwitchB-rip-200] network 12.0.0.0 [SwitchB-rip-200] version 2 [SwitchB-rip-200] undo summary

[SwitchB-rip-200] quit \# 在 Switch C 上启动 RIP 进程 200，并配置 RIP 版本号为 2。
<SwitchC> system-view [SwitchC] rip 200 [SwitchC-rip-200] network 12.0.0.0 [SwitchC-rip-200] network 16.0.0.0 [SwitchC-rip-200] version 2 [SwitchC-rip-200] undo summary [SwitchC-rip-200] quit查看 的路由表信息。
\# Switch C [SwitchC] display ip routing-table Destinations : 13 Routes : 13 Destination/Mask Proto Pre Cost NextHop Interface
0.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
12.3.1.0/24 Direct 0 0 12.3.1.2 Vlan200
12.3.1.0/32 Direct 0 0 12.3.1.2 Vlan200
12.3.1.2/32 Direct 0 0 127.0.0.1 InLoop0
12.3.1.255/32 Direct 0 0 12.3.1.2 Vlan200
16.4.1.0/24 Direct 0 0 16.4.1.1 Vlan400
16.4.1.0/32 Direct 0 0 16.4.1.1 Vlan400
16.4.1.1/32 Direct 0 0 127.0.0.1 InLoop0
16.4.1.255/32 Direct 0 0 16.4.1.1 Vlan400
127.0.0.0/8 Direct 0 0 127.0.0.1 InLoop0
127.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
127.0.0.1/32 Direct 0 0 127.0.0.1 InLoop0
127.255.255.255/32 Direct 0 0 127.0.0.1 InLoop0配置 引入外部路由
(3) RIP在 配置 进程 引入外部路由，引入直连路由和 进程 的路由。
\# Switch B RIP 200 RIP 100 [SwitchB] rip 200 [SwitchB-rip-200] import-route rip 100 [SwitchB-rip-200] import-route direct [SwitchB-rip-200] quit \# 查看路由引入后 Switch C 的路由表信息。
[SwitchC] display ip routing-table Destinations : 15 Routes : 15 Destination/Mask Proto Pre Cost NextHop Interface
0.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
10.2.1.0/24 RIP 100 1 12.3.1.1 Vlan200
11.1.1.0/24 RIP 100 1 12.3.1.1 Vlan200
12.3.1.0/24 Direct 0 0 12.3.1.2 Vlan200
12.3.1.0/32 Direct 0 0 12.3.1.2 Vlan200
12.3.1.2/32 Direct 0 0 127.0.0.1 InLoop0
12.3.1.255/32 Direct 0 0 12.3.1.2 Vlan200

16.4.1.0/24 Direct 0 0 16.4.1.1 Vlan400
16.4.1.0/32 Direct 0 0 16.4.1.1 Vlan400
16.4.1.1/32 Direct 0 0 127.0.0.1 InLoop0
16.4.1.255/32 Direct 0 0 16.4.1.1 Vlan400
127.0.0.0/8 Direct 0 0 127.0.0.1 InLoop0
127.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
127.0.0.1/32 Direct 0 0 127.0.0.1 InLoop0
127.255.255.255/32 Direct 0 0 127.0.0.1 InLoop0

##### 1.13.3 RIP接口附加度量值配置举例

###### 1. 组网需求

• 在 Switch A、Switch B、Switch C、Switch D 和 Switch E 的所有接口上使能 RIP，并使用
RIP-2 进行网络互连。
• Switch A 有两条链路可以到达 Switch D，其中，通过 Switch B 到达 Switch D 的链路比通过
Switch C 到达 Switch D 的链路更加稳定。通过在 Switch A 的 Vlan-interface200 上配置接口
接收 路由的附加度量值，使得 优选从 学到的 网段的路由。
RIP Switch A Switch B 1.1.5.0/24

###### 2. 组网图

图1-4 RIP 接口附加度量值配置组网图

###### 3. 配置步骤

配置各接口的地址（略）
(1)
配置 基本功能
(2) RIP配置 A。
\# Switch <SwitchA> system-view [SwitchA] rip 1 [SwitchA-rip-1] network 1.0.0.0 [SwitchA-rip-1] version 2 [SwitchA-rip-1] undo summary [SwitchA-rip-1] quit配置 B。
\# Switch <SwitchB> system-view [SwitchB] rip 1 [SwitchB-rip-1] network 1.0.0.0 [SwitchB-rip-1] version 2

[SwitchB-rip-1] undo summary \# 配置 Switch C。
<SwitchC> system-view [SwitchB] rip 1 [SwitchC-rip-1] network 1.0.0.0 [SwitchC-rip-1] version 2 [SwitchC-rip-1] undo summary \# 配置 Switch D。
<SwitchD> system-view [SwitchD] rip 1 [SwitchD-rip-1] network 1.0.0.0 [SwitchD-rip-1] version 2 [SwitchD-rip-1] undo summary配置 E。
\# Switch <SwitchE> system-view [SwitchE] rip 1 [SwitchE-rip-1] network 1.0.0.0 [SwitchE-rip-1] version 2 [SwitchE-rip-1] undo summary \# 在 Switch A 上查看 RIP 数据库的所有激活路由。
[SwitchA] display rip 1 database
1.0.0.0/8, auto-summary
1.1.1.0/24, cost 0, nexthop 1.1.1.1, RIP-interface
1.1.2.0/24, cost 0, nexthop 1.1.2.1, RIP-interface
1.1.3.0/24, cost 1, nexthop 1.1.1.2
1.1.4.0/24, cost 1, nexthop 1.1.2.2
1.1.5.0/24, cost 2, nexthop 1.1.1.2
1.1.5.0/24, cost 2, nexthop 1.1.2.2可以看到，到达网段 1.1.5.0/24 有两条 RIP 路由，下一跳分别是 Switch B（IP 地址为 1.1.1.2）
和 C（IP 地址为 1.1.2.2），cost 值都是 2。
Switch
(3) 配置 RIP 接口附加度量值\# 在 Switch A 上配置接口 Vlan-interface200 接收 RIP 路由时的附加度量值为 3。
[SwitchA] interface vlan-interface 200 [SwitchA-Vlan-interface200] rip metricin 3在 上查看 数据库的所有激活路由。
\# Switch A RIP [SwitchA-Vlan-interface200] display rip 1 database
1.0.0.0/8, auto-summary
1.1.1.0/24, cost 0, nexthop 1.1.1.1, RIP-interface
1.1.2.0/24, cost 0, nexthop 1.1.2.1, RIP-interface
1.1.3.0/24, cost 1, nexthop 1.1.1.2
1.1.4.0/24, cost 2, nexthop 1.1.1.2
1.1.5.0/24, cost 2, nexthop 1.1.1.2可以看到，到达网段 1.1.5.0/24 的 RIP 路由仅有一条，下一跳是 Switch B（IP 地址为 1.1.1.2），值为 2。
cost

###### 1. 组网需求

###### 3. 配置步骤

##### 1.13.4 RIP发布聚合路由配置举例

组网需求
1.
• Switch A、Switch B 运行 OSPF，Switch D 运行 RIP，Switch C 同时运行 OSPF 和 RIP。
• 在 Switch C上配置 RIP进程引入 OSPF路由，使 Switch D有到达 10.1.1.0/24、10.2.1.0/24、
10.5.1.0/24 和 10.6.1.0/24 网段的路由。
为了减小 Switch D 的路由表规模，在 Switch C 上配置路由聚合，只发布聚合后的路由
•
10.0.0.0/8。

###### 2. 组网图

图1-5 RIP 发布聚合路由配置组网图Vlan-int500 Vlan-int200
10.6.1.2/24
10.1.1.1/24 Switch B Vlan-int200
10.1.1.2/24 OSPF Vlan-int100 Vlan-int600 Vlan-int300 10.2.1.2/24 10.5.1.2/24
11.3.1.1/24 Vlan-int100
10.2.1.1/24 Switch C Switch A RIP Vlan-int400
11.4.1.2/24 Vlan-int300
11.3.1.2/24 Switch D配置步骤
3.
(1) 配置各接口的地址（略）
(2) 配置 OSPF 基本功能\# 配置 Switch A。
<SwitchA> system-view [SwitchA] ospf [SwitchA-ospf-1] area 0 [SwitchA-ospf-1-area-0.0.0.0] network 10.5.1.0 0.0.0.255 [SwitchA-ospf-1-area-0.0.0.0] network 10.2.1.0 0.0.0.255 [SwitchA-ospf-1-area-0.0.0.0] quit \# 配置 Switch B。
<SwitchB> system-view [SwitchB] ospf [SwitchB-ospf-1] area 0 [SwitchB-ospf-1-area-0.0.0.0] network 10.1.1.0 0.0.0.255 [SwitchB-ospf-1-area-0.0.0.0] network 10.6.1.0 0.0.0.255 [SwitchB-ospf-1-area-0.0.0.0] quit \# 配置 Switch C 。
<SwitchC> system-view [SwitchC] ospf [SwitchC-ospf-1] area 0

[SwitchC-ospf-1-area-0.0.0.0] network 10.1.1.0 0.0.0.255 [SwitchC-ospf-1-area-0.0.0.0] network 10.2.1.0 0.0.0.255 [SwitchC-ospf-1-area-0.0.0.0] quit [SwitchC-ospf-1] quit
(3) 配置 RIP 基本功能\# 配置 Switch C。
[SwitchC] rip 1 [SwitchC-rip-1] network 11.3.1.0 [SwitchC-rip-1] version 2 [SwitchC-rip-1] undo summary配置 D。
\# Switch <SwitchD> system-view [SwitchD] rip 1 [SwitchD-rip-1] network 11.0.0.0 [SwitchD-rip-1] version 2 [SwitchD-rip-1] undo summary [SwitchD-rip-1] quit在 上配置 引入外部路由，引入 进程 的路由和直连路由。
\# Switch C RIP OSPF 1 [SwitchC-rip-1] import-route direct [SwitchC-rip-1] import-route ospf 1 [SwitchC-rip-1] quit查看 的路由表信息。
\# Switch D [SwitchD] display ip routing-table Destinations : 15 Routes : 15 Destination/Mask Proto Pre Cost NextHop Interface
0.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
10.1.1.0/24 RIP 100 1 11.3.1.1 Vlan300
10.2.1.0/24 RIP 100 1 11.3.1.1 Vlan300
10.5.1.0/24 RIP 100 1 11.3.1.1 Vlan300
10.6.1.0/24 RIP 100 1 11.3.1.1 Vlan300
11.3.1.0/24 Direct 0 0 11.3.1.2 Vlan300
11.3.1.0/32 Direct 0 0 11.3.1.2 Vlan300
11.3.1.2/32 Direct 0 0 127.0.0.1 InLoop0
11.4.1.0/24 Direct 0 0 11.4.1.2 Vlan400
11.4.1.0/32 Direct 0 0 11.4.1.2 Vlan400
11.4.1.2/32 Direct 0 0 127.0.0.1 InLoop0
127.0.0.0/8 Direct 0 0 127.0.0.1 InLoop0
127.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
127.0.0.1/32 Direct 0 0 127.0.0.1 InLoop0
127.255.255.255/32 Direct 0 0 127.0.0.1 InLoop0
(4) 在 Switch C 上配置路由聚合，只发布聚合路由 10.0.0.0/8 。
[SwitchC] interface vlan-interface 300 [SwitchC-Vlan-interface300] rip summary-address 10.0.0.0 8 \# 查看 Switch D 的路由表信息。
[SwitchD] display ip routing-table

###### 1. 组网需求

Destinations : 12 Routes : 12 Destination/Mask Proto Pre Cost NextHop Interface
0.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
10.0.0.0/8 RIP 100 1 11.3.1.1 Vlan300
11.3.1.0/24 Direct 0 0 11.3.1.2 Vlan300
11.3.1.0/32 Direct 0 0 11.3.1.2 Vlan300
11.3.1.2/32 Direct 0 0 127.0.0.1 InLoop0
11.4.1.0/24 Direct 0 0 11.4.1.2 Vlan400
11.4.1.0/32 Direct 0 0 11.4.1.2 Vlan400
11.4.1.2/32 Direct 0 0 127.0.0.1 InLoop0
127.0.0.0/8 Direct 0 0 127.0.0.1 InLoop0
127.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
127.0.0.1/32 Direct 0 0 127.0.0.1 InLoop0
127.255.255.255/32 Direct 0 0 127.0.0.1 InLoop0

##### 1.13.5 RIP GR配置举例

组网需求
1.
• Switch A、Switch B 和 Switch C 通过 RIPv2 协议实现网络互连。
• Switch A 作为 GR Restarter，Switch B 和 Switch C 作为 GR Helper 并且通过 GR 机制与Switch A 保持同步。

###### 2. 组网图

图1-6 配置组网图RIP GR Router ID: 1.1.1.1 GR restarter Switch A Vlan-int100
192.1.1.1/24 Vlan-int100 Vlan-int100
192.1.1.2/24 192.1.1.3/24 Switch B Switch C GR helper GR helper Router ID: 2.2.2.2 Router ID: 3.3.3.3

###### 3. 配置步骤

(1) 配置各路由器接口的 IP 地址和 RIP 协议
请按照上面组网图配置各接口的 地址和子网掩码，具体配置过程略。
IP
配置各路由器之间采用 协议进行互连，确保 A、Switch 和 之间能够
RIPv2 Switch B Switch C
在网络层互通，并且各路由器之间能够借助 RIPv2 协议实现动态路由更新。
(2) 配置 RIP GR
\# 使能 Switch A 的 RIP GR 功能。
<SwitchA> system-view

###### 1. 组网需求

###### 3. 配置步骤

###### 4. 验证配置

[SwitchA] rip [SwitchA-rip-1] graceful-restart

###### 4. 验证配置

\# 在 Switch A 上触发协议重启或主备倒换后，查看 RIP 的 GR 状态。
<SwitchA> display rip graceful-restart RIP process: 1 Graceful Restart capability : Enabled Current GR state : Normal Graceful Restart period : 60 seconds Graceful Restart remaining time : 0 seconds

##### 1.13.6 RIP NSR配置举例

组网需求
1.
Switch S、Switch A、Switch B 通过 RIPv2 协议实现网络互连。要求对 Switch S 进行主备倒换时，Switch A 和 Switch B 到 Switch S 的邻居没有中断， Switch A 到 Switch B 的流量没有中断。

###### 2. 组网图

图1-7 配置组网图RIP NSR配置步骤
3.
(1) 配置各接口的 IP 地址和 RIP 协议请按照上面组网图配置各接口的 IP 地址和子网掩码，具体配置过程略。
配置各交换机之间采用 RIPv2 协议进行互连，确保 Switch S、Switch A 和 Switch B 之间能够在网络层互通，并且各路由器之间能够借助 协议实现动态路由更新。
RIPv2
(2) 配置 RIP NSR \# 使能 Switch S 的 RIP NSR 功能。
<SwitchS> system-view [SwitchS] rip 100 [SwitchS-rip-100] non-stop-routing [SwitchS-rip-100] quit验证配置
4.
\# Switch S 进行主备倒换。
[SwitchS] placement reoptimize Predicted changes to the placement Program Current location New location
--------------------------------------------------------------------- lb 0/0 0/0 lsm 0/0 0/0

slsp 0/0 0/0 rib6 0/0 0/0 routepolicy 0/0 0/0 rib 0/0 0/0 staticroute6 0/0 0/0 staticroute 0/0 0/0 eviisis 0/0 0/0 ospf 0/0 1/0 Continue? [y/n]:y Re-optimization of the placement start. You will be notified on completion Re-optimization of the placement complete. Use 'display placement' to view the new placement \# 查看 Switch A 上 RIP 协议的邻居和路由。
[SwitchA] display rip 1 neighbor Neighbor Address: 12.12.12.2 Interface : Vlan-interface200 Version : RIPv2 Last update: 00h00m13s Relay nbr : No BFD session: None Bad packets: 0 Bad routes : 0 [SwitchA] display rip 1 route Route Flags: R - RIP, T - TRIP P - Permanent, A - Aging, S - Suppressed, G - Garbage-collect D - Direct, O - Optimal, F - Flush to RIB
---------------------------------------------------------------------------- Peer 12.12.12.2 on Vlan-interface200 Destination/Mask Nexthop Cost Tag Flags Sec
14.0.0.0/8 12.12.12.2 1 0 RAOF 16
44.0.0.0/8 12.12.12.2 2 0 RAOF 16 Local route Destination/Mask Nexthop Cost Tag Flags Sec
12.12.12.0/24 0.0.0.0 0 0 RDOF -
22.22.22.22/32 0.0.0.0 0 0 RDOF - \# 查看 Switch B 上 RIP 协议的邻居和路由。
[SwitchB] display rip 1 neighbor Neighbor Address: 14.14.14.2 Interface : Vlan-interface200 Version : RIPv2 Last update: 00h00m32s Relay nbr : No BFD session: None Bad packets: 0 Bad routes : 0 [SwitchB] display rip 1 route Route Flags: R - RIP, T - TRIP P - Permanent, A - Aging, S - Suppressed, G - Garbage-collect D - Direct, O - Optimal, F - Flush to RIB
---------------------------------------------------------------------------- Peer 14.14.14.2 on Vlan-interface200 Destination/Mask Nexthop Cost Tag Flags Sec
12.0.0.0/8 14.14.14.2 1 0 RAOF 1
22.0.0.0/8 14.14.14.2 2 0 RAOF 1 Local route

Destination/Mask Nexthop Cost Tag Flags Sec
44.44.44.44/32 0.0.0.0 0 0 RDOF -
14.14.14.0/24 0.0.0.0 0 0 RDOF -通过上面信息可以看出在 Switch S 发生主备倒换的时候，Switch A 和 Switch B 的邻居和路由信息保持不变，从 到 的流量转发没有受到主备倒换的影响。
Switch A Switch B

##### 1.13.7 RIP与BFD联动配置举例（echo报文单跳检测）

###### 1. 组网需求

• Switch A、Switch C通过二层交换机互连，它们的接口Vlan-interface100都运行RIP进程1。
并且 Switch A 的接口 Vlan-interface100 上还使能了 BFD 检测功能。
• Switch A 通过 Switch B 与 Switch C 互连，Switch A 的接口 Vlan-interface200 运行 RIP 进程
2。Switch C 的接口 Vlan-interface300、Switch B 的接口 Vlan-interface200 和
上都运行 进程 1。
Vlan-interface300 RIP
上配置静态路由，并且将静态路由引入在 进程中，使 有路由发送至
• Switch C RIP Switch C
Switch A。Switch A 上学习到 Switch C 发送的静态路由，出接口为与二层交换机相连的接
口。
• 在 Switch C 和二层交换机之间的链路发生故障后，BFD 能够快速检测链路中断并通告 RIP 协
议。RIP 协议响应 BFD 会话 down，删除与 Switch C 的邻居，并删除从 Switch C 学习的路由。
上学习到 上发送的静态路由，出接口为与 相连的接口。
Switch A Switch C Switch B

###### 2. 组网图

图1-8 RIP 与 BFD 联动配置组网图（echo 报文单跳检测）

###### 3. 配置步骤

配置各接口的 地址（略）
(1) IP
(2) 配置 RIP 基本功能\# 配置 Switch A 。
<SwitchA> system-view [SwitchA] rip 1 [SwitchA-rip-1] version 2 [SwitchA-rip-1] undo summary

[SwitchA-rip-1] network 192.168.1.0 [SwitchA-rip-1] quit [SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] rip bfd enable [SwitchA-Vlan-interface100] quit [SwitchA] rip 2 [SwitchA-rip-2] version 2 [SwitchA-rip-2] undo summary [SwitchA-rip-2] network 192.168.2.0 [SwitchA-rip-2] quit \# 配置 Switch B。
<SwitchB> system-view [SwitchB] rip 1 [SwitchB-rip-1] version 2 [SwitchB-rip-1] undo summary [SwitchB-rip-1] network 192.168.2.0 [SwitchB-rip-1] network 192.168.3.0 [SwitchB-rip-1] quit配置 C。
\# Switch <SwitchC> system-view [SwitchC] rip 1 [SwitchC-rip-1] version 2 [SwitchC-rip-1] undo summary [SwitchC-rip-1] network 192.168.1.0 [SwitchC-rip-1] network 192.168.3.0 [SwitchC-rip-1] import-route static [SwitchC-rip-1] quit
(3) 配置 BFD 参数\# 配置 Switch A。
[SwitchA] bfd echo-source-ip 11.11.11.11 [SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] bfd min-echo-receive-interval 500 [SwitchA-Vlan-interface100] bfd detect-multiplier 7 [SwitchA-Vlan-interface100] quit [SwitchA] quit
(4) Switch C 配置静态路由[SwitchC] ip route-static 120.1.1.1 24 null 0

###### 4. 验证配置

\# 查看 Switch A 的 BFD 信息。
<SwitchA> display bfd session Total Session Num: 1 Up Session Num: 1 Init Mode: Active IPv4 Session Working Under Echo Mode:
LD SourceAddr DestAddr State Holdtime Interface

4 192.168.1.1 192.168.1.2 Up 2000ms Vlan100 \# 查看 Switch A 上学到的路由 120.1.1.0/24，可以看到 Switch A 经过 L2 Switch 到达 Switch C。
<SwitchA> display ip routing-table 120.1.1.0 24 Summary count : 1 Destination/Mask Proto Pre Cost NextHop Interface
120.1.1.0/24 RIP 100 1 192.168.1.2 Vlan-interface100当 Switch C 和二层交换机之间的链路发生故障时：
\# 查看 Switch A 上学到的路由 120.1.1.0/24，可以看到 Switch A 经过 Switch B 到达 Switch C。
<SwitchA> display ip routing-table 120.1.1.0 24 Summary count : 1 Destination/Mask Proto Pre Cost NextHop Interface
120.1.1.0/24 RIP 100 1 192.168.2.2 Vlan-interface200

##### 1.13.8 RIP与BFD联动配置举例（指定目的地址的echo报文单跳检测）

###### 1. 组网需求

• Switch A 和 Switch B 互连，Switch A 的接口 Vlan-interface100 和 Switch B 的接口
Vlan-interface100 都运行 RIP 进程 1。Switch A 的接口 Vlan-interface100 上使能了 BFD 检测
功能，指定目的地址为 的接口 的地址。
Switch B Vlan-interface100
与 互连，它们的接口 都运行 进程 1。
• Switch B Switch C Vlan-interface200 RIP
和 上配置静态路由，并都将静态路由引入 进程中，其中 引入
• Switch A Switch C RIP Switch A
路由的 cost 值比 Switch C 引入的 cost 值小，这样，当 Switch B 上学习到 Switch A 和 Switch
C 发送的路由后，会优选 Switch A 的路由，出接口为与 Switch A 连接的接口。
• 在 Switch A 和 Switch B 之间的链路发生单通故障（从 Switch A 到 Switch B 方向报文是通的，
但是从 Switch B 到 Switch A 方向的链路不通）后，Switch A 上 BFD 能够快速检测链路故障
并通告RIP协议。Switch A上的RIP协议响应BFD会话down，删除从接口Vlan-interface100
学习到的邻居和路由，并不再从该接口接收和发送 RIP 报文。Switch B 上在学自 Switch A 的
路由老化后，会优选 Switch C 发送的静态路由，出接口为与 Switch C 连接的接口。

###### 2. 组网图

图1-9 RIP 与 BFD 联动配置组网图（指定目的地址的 echo 报文单跳检测）

###### 3. 配置步骤

配置各接口的 地址（略）
(1) IP配置 基本功能并且在接口上使能
(2) RIP BFD配置 A。
\# Switch <SwitchA> system-view [SwitchA] rip 1 [SwitchA-rip-1] network 192.168.2.0 [SwitchA-rip-1] import-route static [SwitchA-rip-1] quit [SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] rip bfd enable destination 192.168.2.2 [SwitchA-Vlan-interface100] quit \# 配置 Switch B。
<SwitchB> system-view [SwitchB] rip 1 [SwitchB-rip-1] network 192.168.2.0 [SwitchB-rip-1] network 192.168.3.0 [SwitchB-rip-1] quit \# 配置 Switch C。
<SwitchC> system-view [SwitchC] rip 1 [SwitchC-rip-1] network 192.168.3.0 [SwitchC-rip-1] import-route static cost 3 [SwitchC-rip-1] quit
(3) 配置接口 BFD 参数\# 配置 Switch A。
[SwitchA] bfd echo-source-ip 11.11.11.11 [SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] bfd min-echo-receive-interval 500

[SwitchA-Vlan-interface100] return
(4) 配置静态路由\# 配置 Switch A。
[SwitchA] ip route-static 100.1.1.0 24 null 0配置 C。
\# Switch [SwitchC] ip route-static 100.1.1.0 24 null 0

###### 4. 验证配置

显示 的 信息。
\# Switch A BFD <SwitchA> display bfd session Total Session Num: 1 Up Session Num: 1 Init Mode: Active IPv4 session working under Echo mode:
LD SourceAddr DestAddr State Holdtime Interface 3 192.168.2.1 192.168.2.2 Up 2000ms vlan100 \# 显示 Switch B 上学到的路由 100.1.1.0/24。
<SwitchB> display ip routing-table 100.1.1.0 24 verbose Summary Count : 1 Destination: 100.1.1.0/24 Protocol: RIP Process ID: 1 SubProtID: 0x1 Age: 00h02m47s Cost: 1 Preference: 100 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0x2 OrigAs: 0 NibID: 0x12000002 LastAs: 0 AttrID: 0xffffffff Neighbor: 192.168.2.1 Flags: 0x1008c OrigNextHop: 192.168.2.1 Label: NULL RealNextHop: 192.168.2.1 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: vlan-interface 100 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0当 Switch A 和 Switch B 之间的链路发生故障时：
\# 显示 Switch B 上学到的路由 100.1.1.0/24。
<SwitchB> display ip routing-table 100.1.1.0 24 verbose Summary Count : 1 Destination: 100.1.1.0/24

Protocol: RIP Process ID: 1 SubProtID: 0x1 Age: 00h21m23s Cost: 4 Preference: 100 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0x2 OrigAs: 0 NibID: 0x12000002 LastAs: 0 AttrID: 0xffffffff Neighbor: 192.168.3.2 Flags: 0x1008c OrigNextHop: 192.168.3.2 Label: NULL RealNextHop: 192.168.3.2 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: vlan-interface 200 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0

##### 1.13.9 RIP与BFD联动配置举例（control报文双向检测）

###### 1. 组网需求

• Switch A 通过 Switch B 与 Switch C 互连。Switch A 的接口 Vlan-interface100 和 Switch C 的
接口 Vlan-interface200 上都运行 RIP 进程 1。分别在 Switch A 和 Switch C 上配置到达对端的
静态路由，并在 Switch A 的接口 Vlan-interface100 和 Switch C 的接口 Vlan-interface200 上
并使能 BFD 检测功能。
通过 与 互连。Switch 的接口 运行 进程
• Switch A Switch D Switch C A Vlan-interface300 RIP
2。Switch C 的接口 Vlan-interface400、Switch D 的接口 Vlan-interface300 和
Vlan-interface400 上运行 RIP 进程 1。
• 为使 Switch A 与 Switch C 互有路由发送，在 Switch A 与 Switch C 上将到达对端的静态路由
引入 协议中。Switch 与 之间建立 会话。Switch 上学习到 发
RIP A Switch C BFD A Switch C
送的静态路由，出接口为与 Switch B 连接的接口。
• 在 Switch B 与 Switch C 之间的链路发生故障后，BFD 能够快速检测链路中断并通告 RIP 协
议。RIP 协议响应 BFD 会话 down，删除与 Switch C 的邻居，并删除从 Switch C 学习的路由。
Switch A 上学习到 Switch C 发送的静态路由，出接口为与 Switch D 连接的接口。

###### 2. 组网图

图1-10 RIP 与 BFD 联动配置组网图（control 报文双向检测）

| 接口 | IP地址 | 设备 | 接口 |
|---|---|---|---|
| Vlan-int300 | 192.168.3.1/24 | Switch B | Vlan-int100 |
| Vlan-int100 | 192.168.1.1/24 |  | Vlan-int200 |
| Vlan-int200 | 192.168.2.2/24 | Switch D | Vlan-int300 |
| Vlan-int400 | 192.168.4.2/24 |  | Vlan-int400 |

设备 IP地址Switch A 192.168.1.2/24
192.168.2.1/24 Switch C 192.168.3.2/24
192.168.4.1/24

###### 3. 配置步骤

配置各接口的 地址（略）
(1) IP配置 基本功能，并引入静态路由，使 与 互有路由发送
(2) RIP Switch A Switch C配置 A。
\# Switch <SwitchA> system-view [SwitchA] rip 1 [SwitchA-rip-1] version 2 [SwitchA-rip-1] undo summary [SwitchA-rip-1] network 192.168.1.0 [SwitchA-rip-1] network 101.1.1.0 [SwitchA-rip-1] peer 192.168.2.2 [SwitchA-rip-1] undo validate-source-address [SwitchA-rip-1] import-route static [SwitchA-rip-1] quit [SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] rip bfd enable [SwitchA-Vlan-interface100] quit [SwitchA] rip 2 [SwitchA-rip-2] version 2 [SwitchA-rip-2] undo summary [SwitchA-rip-2] network 192.168.3.0 [SwitchA-rip-2] quit配置 C。
\# Switch

<SwitchC> system-view [SwitchC] rip 1 [SwitchC-rip-1] version 2 [SwitchC-rip-1] undo summary [SwitchC-rip-1] network 192.168.2.0 [SwitchC-rip-1] network 192.168.4.0 [SwitchC-rip-1] network 100.1.1.0 [SwitchC-rip-1] peer 192.168.1.1 [SwitchC-rip-1] undo validate-source-address [SwitchC-rip-1] import-route static [SwitchC-rip-1] quit [SwitchC] interface vlan-interface 200 [SwitchC-Vlan-interface200] rip bfd enable [SwitchC-Vlan-interface200] quit \# 配置 Switch D。
<SwitchD> system-view [SwitchD] rip 1 [SwitchD-rip-1] version 2 [SwitchD-rip-1] undo summary [SwitchD-rip-1] network 192.168.3.0 [SwitchD-rip-1] network 192.168.4.0配置 参数
(3) BFD配置 A。
\# Switch [SwitchA] bfd session init-mode active [SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] bfd min-transmit-interval 500 [SwitchA-Vlan-interface100] bfd min-receive-interval 500 [SwitchA-Vlan-interface100] bfd detect-multiplier 7 [SwitchA-Vlan-interface100] quit配置 C。
\# Switch [SwitchC] bfd session init-mode active [SwitchC] interface vlan-interface 200 [SwitchC-Vlan-interface200] bfd min-transmit-interval 500 [SwitchC-Vlan-interface200] bfd min-receive-interval 500 [SwitchC-Vlan-interface200] bfd detect-multiplier 7 [SwitchC-Vlan-interface200] quit配置静态路由
(4)
配置 A。
\# Switch [SwitchA] ip route-static 192.168.2.0 24 vlan-interface 100 192.168.1.2 [SwitchA] quit \# 配置 Switch C。
[SwitchC] ip route-static 192.168.1.0 24 vlan-interface 200 192.168.2.1

###### 4. 验证配置

显示 的 信息。
\# Switch A BFD <SwitchA> display bfd session

Total Session Num: 1 Up Session Num: 1 Init Mode: Active IPv4 session working under Ctrl mode:
LD/RD SourceAddr DestAddr State Holdtime Interface 513/513 192.168.1.1 192.168.2.2 Up 1700ms vlan100 \# 显示 Switch A 上学到的路由 100.1.1.0/24，可以看到 Switch A 经过 Switch B 到达 Switch C。
<SwitchA> display ip routing-table 100.1.1.0 24 Summary count : 1 Destination/Mask Proto Pre Cost NextHop Interface
100.1.1.0/24 RIP 100 1 192.168.2.2 vlan-interface 100 Switch B 和 Switch C 之间的链路发生故障后：
\# 显示 Switch A 上学到的路由 100.1.1.0/24，可以看到 Switch A 经过 Switch D 到达 Switch C。
<SwitchA> display ip routing-table 100.1.1.0 24 Summary count : 1 Destination/Mask Proto Pre Cost NextHop Interface
100.1.1.0/24 RIP 100 2 192.168.3.2 vlan-interface 300

##### 1.13.10 RIP快速重路由配置举例

###### 1. 组网需求

Switch A、Switch B 和 Switch C 通过 RIPv2 协议实现网络互连。要求当 Switch A 和 Switch B 之间的链路出现单通故障时，业务可以快速切换到链路 上。
B

###### 2. 组网图

图1-11 RIP 快速重路由配置组网图Switch C 100 V l an n t - i n
- i t 101 an V l Link B 100 V l an n t
- i - i n an t 101 V l Link A Loop0 Loop0 Vlan-int200 Vlan-int200 Switch A Switch B

| 接口 | IP地址 | 设备 | 接口 |
|---|---|---|---|
| Vlan-int100 | 12.12.12.1/24 | Switch B | Vlan-int101 |
| Vlan-int200 | 13.13.13.1/24 |  | Vlan-int200 |
| Loop0 | 1.1.1.1/32 |  | Loop0 |
| Vlan-int100 | 12.12.12.2/24 |  |  |
| Vlan-int101 | 24.24.24.2/24 |  |  |

设备 IP地址Switch A 24.24.24.4/24
13.13.13.2/24
4.4.4.4/32 Switch C

###### 4. 验证配置

###### 3. 配置步骤

(1) 配置各交换机接口的 IP 地址和 RIPv2 协议
请按照上面组网图配置各接口的 IP 地址和子网掩码，具体配置过程略。
配置各路由器之间采用 RIPv2 协议进行互连，确保 Switch A、Switch B 和 Switch C 之间能够
在网络层互通，并且各路由器之间能够借助 RIPv2 协议实现动态路由更新。
具体配置过程略。
(2) 配置 RIP 快速重路由
\# 配置 Switch A。
<SwitchA> system-view
[SwitchA] ip prefix-list abc index 10 permit 4.4.4.4 32
[SwitchA] route-policy frr permit node 10
[SwitchA-route-policy-frr-10] if-match ip address prefix-list abc
[SwitchA-route-policy-frr-10] apply fast-reroute backup-interface vlan-interface 100
backup-nexthop 12.12.12.2
[SwitchA-route-policy-frr-10] quit
[SwitchA] rip 1
[SwitchA-rip-1] fast-reroute route-policy frr
[SwitchA-rip-1] quit
\# 配置 Switch B。
<SwitchB> system-view
[SwitchB] ip prefix-list abc index 10 permit 1.1.1.1 32
[SwitchB] route-policy frr permit node 10
[SwitchB-route-policy-frr-10] if-match ip address prefix-list abc
[SwitchB-route-policy-frr-10] apply fast-reroute backup-interface vlan-interface 101
backup-nexthop 24.24.24.2
[SwitchB-route-policy-frr-10] quit
[SwitchB] rip 1
[SwitchB-rip-1] fast-reroute route-policy frr
[SwitchB-rip-1] quit
验证配置
4.
\# 在 Switch A 上查看 4.4.4.4/32 路由，可以看到备份下一跳信息：
[SwitchA] display ip routing-table 4.4.4.4 verbose
Summary Count : 1
Destination: 4.4.4.4/32
Protocol: RIP
Process ID: 1
SubProtID: 0x1 Age: 04h20m37s
Cost: 1 Preference: 100
IpPre: N/A QosLocalID: N/A
Tag: 0 State: Active Adv
OrigTblID: 0x0 OrigVrf: default-vrf
TableID: 0x2 OrigAs: 0
NibID: 0x26000002 LastAs: 0

AttrID: 0xffffffff Neighbor: 13.13.13.2 Flags: 0x1008c OrigNextHop: 13.13.13.2 Label: NULL RealNextHop: 13.13.13.2 BkLabel: NULL BkNextHop: 12.12.12.2 Tunnel ID: Invalid Interface: Vlan-interface200 BkTunnel ID: Invalid BkInterface: Vlan-interface100 FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0 \# 在 Switch B 上查看 1.1.1.1/32 路由，可以看到备份下一跳信息：
[SwitchB] display ip routing-table 1.1.1.1 verbose Summary Count : 1 Destination: 1.1.1.1/32 Protocol: RIP Process ID: 1 SubProtID: 0x1 Age: 04h20m37s Cost: 1 Preference: 100 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0x2 OrigAs: 0 NibID: 0x26000002 LastAs: 0 AttrID: 0xffffffff Neighbor: 13.13.13.1 Flags: 0x1008c OrigNextHop: 13.13.13.1 Label: NULL RealNextHop: 13.13.13.1 BkLabel: NULL BkNextHop: 24.24.24.2 Tunnel ID: Invalid Interface: Vlan-interface200 BkTunnel ID: Invalid BkInterface: Vlan-interface101 FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0

## 04-OSPF配置

目 录简介路由器协议规范配置 基本功能配置 特殊区域配置 区域配置OSPF接口网络类型为广播配置 接口网络类型为

配置对引入的外部路由信息进行路由聚合配置 最大等价路由条数配置 引入外部路由配置OSPF定时器配置 尝试退出 状态的定时器时间间隔控制 的生成、发布与接收配置OSPF的前缀按优先权收敛功能

配置兼容RFC 的外部路由选择规则配置配置echo报文单跳检测配置 快速重路由支持 检测功能（ 方式）
配置限制和指导OSPF显示和维护

OSPF发布聚合路由配置举例虚连接配置举例与 联动配置举例OSPF路由信息不正确

### 1 OSPF

1 OSPF

#### 1.1 OSPF简介

OSPF（Open First，开放最短路径优先）是 IETF（Internet Force，Shortest Path Engineering Task互联网工程任务组）组织开发的一个基于链路状态的内部网关协议。目前针对 IPv4 协议使用的是OSPF Version 2。下文中所提到的 OSPF 均指 OSPF Version 2。

##### 1.1.1 OSPF的特点

具有如下特点：
OSPF适应范围广：支持各种规模的网络，最多可支持几百台路由器。
•快速收敛：在网络的拓扑结构发生变化后立即发送更新报文，使这一变化在自治系统中同步。
•无自环：由于 根据收集到的链路状态用最短路径树算法计算路由，从算法本身保证了
• OSPF不会生成自环路由。
• 区域划分：允许自治系统的网络被划分成区域来管理。路由器链路状态数据库的减小降低了内存的消耗和 CPU 的负担；区域间传送路由信息的减少降低了网络带宽的占用。
• 等价路由：支持到同一目的地址的多条等价路由。
• 路由分级：使用 4 类不同的路由，按优先顺序来说分别是：区域内路由、区域间路由、第一类外部路由、第二类外部路由。
• 支持验证：支持基于区域和接口的报文验证，以保证报文交互和路由计算的安全性。
• 组播发送：在某些类型的链路上以组播地址发送协议报文，减少对其他设备的干扰。

##### 1.1.2 OSPF报文类型

协议报文直接封装为 报文，协议号为 89。
OSPF IP有五种类型的协议报文：
OSPF报文：周期性发送，用来发现和维持 邻居关系，以及进行 DR（Designated
• Hello OSPF Router，指定路由器）/BDR（Backup Designated Router，备份指定路由器）的选举。
• DD（Database Description，数据库描述）报文：描述了本地 LSDB（Link State DataBase，链路状态数据库）中每一条 LSA（Link State Advertisement，链路状态通告）的摘要信息，用于两台路由器进行数据库同步。
• LSR（Link State Request，链路状态请求）报文：向对方请求所需的 LSA。两台路由器互相交换 报文之后，得知对端的路由器有哪些 是本地的 所缺少的，这时需要发送DD LSA LSDB LSR 报文向对方请求所需的 LSA。
• LSU（Link State Update，链路状态更新）报文：向对方发送其所需要的 LSA。
（ ，链路状态确认）报文：用来对收到的 进行确认。
• LSAck Link State Acknowledgment LSA

##### 1.1.3 LSA类型

OSPF 中对链路状态信息的描述都是封装在 LSA 中发布出去，常用的 LSA 有以下几种类型：

Router LSA（Type-1）：由每个路由器产生，描述路由器的链路状态和开销，在其始发的区域
•内传播。
LSA（Type-2）：由 产生，描述本网段所有路由器的链路状态，在其始发的区域
• Network DR内传播。
• Network Summary LSA（Type-3）：由 ABR（Area Border Router，区域边界路由器）产生，描述区域内某个网段的路由，并通告给其他区域。
• ASBR Summary LSA（Type-4）：由 ABR 产生，描述到 ASBR（Autonomous System Boundary Router，自治系统边界路由器）的路由，通告给相关区域。
AS External LSA（Type-5）：由 ASBR 产生，描述到 AS（Autonomous System，自治系统）
•外部的路由，通告到所有的区域（除了 区域和 区域）。
Stub NSSA LSA（Type-7）：由 NSSA（Not-So-Stubby Area）区域内的 产生，描
• NSSA External ASBR述到 AS 外部的路由，仅在 NSSA 区域内传播。
• Opaque LSA：用于 OSPF 的扩展通用机制，目前有 Type-9、Type-10 和 Type-11 三种。其中，Type-9 LSA 仅在本地链路范围进行泛洪，用于支持 GR（Graceful Restart，平滑重启）
的 Grace LSA 就是 Type-9 的一种类型；Type-10 LSA 仅在区域范围进行泛洪；Type-11 LSA可以在一个自治系统范围进行泛洪。

##### 1.1.4 OSPF区域

###### 1. 区域划分

随着网络规模日益扩大，当一个大型网络中的路由器都运行 OSPF 协议时，LSDB 会占用大量的存储空间，并使得运行 SPF（Shortest Path First，最短路径优先）算法的复杂度增加，导致 CPU 负担加重。
在网络规模增大之后，拓扑结构发生变化的概率也增大，网络会经常处于“振荡”之中，造成网络中会有大量的 协议报文在传递，降低了网络的带宽利用率。更为严重的是，每一次变化都会OSPF导致网络中所有的路由器重新进行路由计算。
OSPF协议通过将自治系统划分成不同的区域来解决上述问题。区域是从逻辑上将路由器划分为不同的组，每个组用区域号来标识。如 图 1-1 所示。

图1-1 OSPF 区域划分Area 4 Area 1 Area 0 Area 2 Area 3区域的边界是路由器，而不是链路。一个路由器可以属于不同的区域，但是一个网段（链路）只能属于一个区域，或者说每个运行 的接口必须指明属于哪一个区域。划分区域后，可以在区域OSPF边界路由器上进行路由聚合，以减少通告到其他区域的 LSA 数量，还可以将网络拓扑变化带来的影响最小化。

###### 2. 骨干区域（Backbone Area）

OSPF 划分区域之后，并非所有的区域都是平等的关系。其中有一个区域是与众不同的，它的区域号是 0，通常被称为骨干区域。骨干区域负责区域之间的路由，非骨干区域之间的路由信息必须通过骨干区域来转发。对此，OSPF 有两个规定：
• 所有非骨干区域必须与骨干区域保持连通；
• 骨干区域自身也必须保持连通。
在实际应用中，可能会因为各方面条件的限制，无法满足上面的要求。这时可以通过配置 虚OSPF连接予以解决。

###### 3. 虚连接（Virtual Link）

虚连接是指在两台 ABR 之间通过一个非骨干区域建立的一条逻辑上的连接通道。它的两端必须是ABR，而且必须在两端同时配置方可生效。为虚连接两端提供一条非骨干区域内部路由的区域称为传输区（Transit Area）。
在 图 1-2中，Area2与骨干区域之间没有直接相连的物理链路，但可以在ABR上配置虚连接，使Area2通过一条逻辑链路与骨干区域保持连通。

图1-2 虚连接示意图之一虚连接的另外一个应用是提供冗余的备份链路，当骨干区域因链路故障不能保持连通时，通过虚连接仍然可以保证骨干区域在逻辑上的连通性。如 图 1-3 所示。
图1-3 虚连接示意图之二Area 1 Virtual link R1 R2 Area 0虚连接相当于在两个 ABR 之间形成了一个点到点的连接，因此，在这个连接上，和物理接口一样可以配置接口的各参数，如发送 Hello 报文间隔等。
两台 ABR 之间直接传递 OSPF 报文信息，它们之间的 OSPF 路由器只是起到一个转发报文的作用。
由于协议报文的目的地址不是中间这些路由器，所以这些报文对于它们而言是透明的，只是当作普通的 报文来转发。
IP

###### 4. Stub区域和Totally Stub区域

Stub 区域是一些特定的区域，该区域的 ABR 会将区域间的路由信息传递到本区域，但不会引入自治系统外部路由，区域中路由器的路由表规模以及 LSA 数量都会大大减少。为保证到自治系统外的路由依旧可达，该区域的 ABR 将生成一条缺省路由 Type-3 LSA，发布给本区域中的其他非 ABR路由器。
为了进一步减少 区域中路由器的路由表规模以及 数量，可以将区域配置为Stub LSA Totally Stub（完全 Stub）区域，该区域的 ABR 不会将区域间的路由信息和自治系统外部路由信息传递到本区域。为保证到本自治系统的其他区域和自治系统外的路由依旧可达，该区域的 ABR 将生成一条缺省路由 Type-3 LSA，发布给本区域中的其他非 ABR 路由器。

###### 5. NSSA区域和Totally NSSA区域

NSSA（Not-So-Stubby Area）区域是 区域的变形，与 区域的区别在于 区域允许Stub Stub NSSA引入自治系统外部路由，由 ASBR 发布 Type-7 LSA 通告给本区域。当 Type-7 LSA 到达 NSSA 的ABR 时，由 ABR 将 Type-7 LSA 转换成 Type-5 LSA，传播到其他区域。

###### 4. 自治系统边界路由器ASBR

可以将区域配置为 Totally NSSA（完全 NSSA）区域，该区域的 ABR 不会将区域间的路由信息传递到本区域。为保证到本自治系统的其他区域的路由依旧可达，该区域的 将生成一条缺省路ABR由 Type-3 LSA，发布给本区域中的其他非 ABR 路由器。
如 图 1-4 所示，运行OSPF协议的自治系统包括 3 个区域：区域 0、区域 1 和区域 2，另外两个自治系统运行RIP协议。区域 1 被定义为NSSA区域，区域 1 接收的RIP路由传播到NSSA ASBR后，由NSSA ASBR产生Type-7 LSA在区域 内传播，当Type-7 LSA到达NSSA ABR后，转换成Type-5 1 LSA传播到区域 0 和区域 2。
另一方面，运行 RIP 的自治系统的 RIP 路由通过区域 2 的 ASBR 产生 Type-5 LSA 在 OSPF 自治系统中传播。但由于区域 1 是 NSSA 区域，所以 Type-5 LSA 不会到达区域 1。
图1-4 区域NSSA

##### 1.1.5 路由器类型

OSPF 路由器根据在 AS 中的不同位置，可以分为以下四类：

###### 1. 区域内路由器（Internal Router）

该类路由器的所有接口都属于同一个 OSPF 区域。

###### 2. 区域边界路由器ABR

该类路由器可以同时属于两个以上的区域，但其中一个必须是骨干区域。ABR 用来连接骨干区域和非骨干区域，它与骨干区域之间既可以是物理连接，也可以是逻辑上的连接。

###### 3. 骨干路由器（Backbone Router）

该类路由器至少有一个接口属于骨干区域。因此，所有的 ABR 和位于 Area0 的内部路由器都是骨干路由器。
自治系统边界路由器
4. ASBR与其他 AS 交换路由信息的路由器称为 ASBR。ASBR 并不一定位于 AS 的边界，它有可能是区域内路由器，也有可能是 ABR。只要一台 路由器引入了外部路由的信息，它就成为 ASBR。
OSPF

图1-5 OSPF 路由器的类型RIP IS-IS ASBR Area 1 Area 4 Backbone router Internal router Area 0 ABR Area 3 Area 2

##### 1.1.6 路由类型

OSPF 将路由分为四类，按照优先级从高到低的顺序依次为：
• 区域内路由（Intra Area）
• 区域间路由（Inter Area）
• 第一类外部路由（Type1 External）：这类路由的可信程度较高，并且和 OSPF 自身路由的开销具有可比性，所以到第一类外部路由的开销等于本路由器到相应的 ASBR 的开销与 ASBR到该路由目的地址的开销之和。
第二类外部路由（Type2 External）：这类路由的可信度比较低，所以 OSPF 协议认为从 ASBR
•到自治系统之外的开销远远大于在自治系统之内到达 的开销。所以计算路由开销时将ASBR主要考虑前者，即到第二类外部路由的开销等于 ASBR 到该路由目的地址的开销。如果计算出开销值相等的两条路由，再考虑本路由器到相应的 ASBR 的开销。
区域内和区域间路由描述的是 AS 内部的网络结构，外部路由则描述了应该如何选择到 AS 以外目的地址的路由。

##### 1.1.7 路由器ID

路由器 ID——即 Router ID，用来在一个自治系统中唯一地标识一台路由器，一台路由器如果要运行 OSPF 协议，则必须存在 Router ID。Router ID 的获取方式有以下两种：

###### 1. 手工指定Router ID

用户可以在创建 OSPF 进程的时候指定 Router ID，配置时，必须保证自治系统中任意两台路由器的 ID 都不相同。通常的做法是将路由器的 ID 配置为与该路由器某个接口的 IP 地址一致。

###### 2. 使用全局Router ID

如果在创建 OSPF 进程的时候没有指定 Router ID，则缺省使用全局 Router ID。建议用户在创建OSPF 进程的时候手工指定 Router ID，或者选择自动获取 Router ID。

##### 1.1.8 OSPF路由的计算过程

同一个区域内，OSPF 路由的计算过程可简单描述如下：
• 每台 OSPF 路由器根据自己周围的网络拓扑结构生成 LSA，并通过更新报文将 LSA 发送给网络中的其它 OSPF 路由器。
• 每台 OSPF 路由器都会收集其它路由器通告的 LSA，所有的 LSA 放在一起便组成了 LSDB。
LSA 是对路由器周围网络拓扑结构的描述，LSDB 则是对整个自治系统的网络拓扑结构的描述。
• OSPF 路由器将 LSDB 转换成一张带权的有向图，这张图便是对整个网络拓扑结构的真实反映。各个路由器得到的有向图是完全相同的。
每台路由器根据有向图，使用 SPF 算法计算出一棵以自己为根的最短路径树，这棵树给出了
•到自治系统中各节点的路由。

##### 1.1.9 OSPF的网络类型

OSPF 根据链路层协议类型将网络分为下列四种类型：
• 广播（Broadcast）类型：当链路层协议是 Ethernet、FDDI 时，缺省情况下，OSPF 认为网络类型是 Broadcast。在该类型的网络中，通常以组播形式（OSPF 路由器的预留 IP 组播地址是 224.0.0.5；OSPF DR/BDR 的预留 IP 组播地址是 224.0.0.6）发送 Hello 报文、LSU 报文和 LSAck 报文；以单播形式发送 DD 报文和 LSR 报文。
• NBMA（Non-Broadcast Multi-Access，非广播多路访问）类型：当链路层协议是帧中继、ATM或 X.25 时，缺省情况下，OSPF 认为网络类型是 NBMA。在该类型的网络中，以单播形式发送协议报文。
P2MP（Point-to-MultiPoint，点到多点）类型：没有一种链路层协议会被缺省的认为是 P2MP
•类型。P2MP 必须是由其他的网络类型强制更改的，常用做法是将 NBMA 网络改为 P2MP 网络。在该类型的网络中，缺省情况下，以组播形式（224.0.0.5）发送协议报文。可以根据用户需要，以单播形式发送协议报文。
• P2P （ Point-to-Point ，点到点）类型：当链路层协议是 PPP 、 HDLC 时，缺省情况下， OSPF认为网络类型是 P2P。在该类型的网络中，以组播形式（224.0.0.5）发送协议报文。
与 网络之间的区别如下：
NBMA P2MP NBMA 网络是全连通的；P2MP 网络并不需要一定是全连通的。
•NBMA 网络中需要选举 DR 与 BDR；P2MP 网络中没有 DR 与 BDR。
•NBMA 网络采用单播发送报文，需要手工配置邻居；P2MP 网络采用组播方式发送报文，通
•过配置也可以采用单播发送报文。

##### 1.1.10 DR/BDR

###### 1. DR/BDR简介

在广播网和 网络中，任意两台路由器之间都要交换路由信息。如果网络中有 台路由器，则NBMA n需要建立 n（n-1）/2 个邻接关系。这使得任何一台路由器的路由变化都会导致多次传递，浪费了带宽资源。为解决这一问题，OSPF 提出了 DR 的概念，所有路由器只将信息发送给 DR，由 DR 将网络链路状态发送出去。
另外，OSPF 提出了 BDR 的概念。BDR 是对 DR 的一个备份，在选举 DR 的同时也选举 BDR，BDR也和本网段内的所有路由器建立邻接关系并交换路由信息。当 DR 失效后，BDR 会立即成为新的DR。
OSPF 网络中，既不是 DR 也不是 BDR 的路由器为 DR Other。DR Other 仅与 DR 和 BDR 建立邻接关系，DR Other 之间不交换任何路由信息。这样就减少了广播网和 NBMA 网络上各路由器之间邻接关系的数量，同时减少网络流量，节约了带宽资源。
如 图 所示，进行DR/BDR选举后，5 台路由器之间只需要建立 个邻接关系就可以了。
1-6 7图1-6 DR 和 BDR 示意图在 OSPF 中，邻居（ Neighbor ）和邻接（ Adjacency ）是两个不同的概念。路由器启动后，会通过接口向外发送 报文，收到 报文的路由器会检查报文中所定义的参数，如果双方一致就Hello Hello会形成邻居关系。只有当双方成功交换 DD 报文，交换 LSA 并达到 LSDB 同步之后，才形成邻接关系。

###### 2. DR/BDR选举过程

DR/BDR是由同一网段中所有的路由器根据路由器优先级和Router ID通过Hello报文选举出来的，只有优先级大于 0 的路由器才具有选举资格。
进行 DR/BDR 选举时每台路由器将自己选出的 DR 写入 Hello 报文中，发给网段上每台运行 OSPF协议的路由器。当处于同一网段的两台路由器同时宣布自己是 时，路由器优先级高者胜出。如DR果优先级相等，则 Router ID 大者胜出。

需要注意的是：
只有在广播或 NBMA 网络中才会选举 DR；在 P2P 或 P2MP 网络中不需要选举 DR。
•DR 是某个网段中的概念，是针对路由器的接口而言的。某台路由器在一个接口上可能是 DR，
•在另一个接口上有可能是 BDR，或者是 Other。
DR选举完毕后，即使网络中加入一台具有更高优先级的路由器，也不会重新进行选举，
• DR/BDR替换该网段中已经存在的 DR/BDR 成为新的 DR/BDR。DR 并不一定就是路由器优先级最高的路由器接口；同理，BDR 也并不一定就是路由器优先级次高的路由器接口。

##### 1.1.11 协议规范

与 相关的协议规范有：
OSPF 1245：OSPF
• RFC protocol analysis 1246：Experience
• RFC with the OSPF protocol RFC 1370：Applicability Statement for OSPF
•RFC 1403：BGP OSPF Interaction
•RFC 1745：BGP4/IDRP for IP---OSPF Interaction
•
• RFC 1765：OSPF Database Overflow
• RFC 1793：Extending OSPF to Support Demand Circuits
• RFC 2154：OSPF with Digital Signatures
• RFC 2328：OSPF Version 2
• RFC 3101：OSPF Not-So-Stubby Area (NSSA) Option
• RFC 3166：Request to Move RFC 1403 to Historic Status
• RFC 3509：Alternative Implementations of OSPF Area Border Routers
• RFC 4167：Graceful OSPF Restart Implementation Report
• RFC 4577：OSPF as the Provider/Customer Edge Protocol for BGP/MPLS IP Virtual Private Networks (VPNs)
• RFC 4750：OSPF Version 2 Management Information Base
• RFC 4811：OSPF Out-of-Band LSDB Resynchronization
• RFC 4812：OSPF Restart Signaling
• RFC 5088：OSPF Protocol Extensions for Path Computation Element (PCE) Discovery
• RFC 5250：The OSPF Opaque LSA Option
• RFC 5613：OSPF Link-Local Signaling
• RFC 5642：Dynamic Hostname Exchange Mechanism for OSPF
• RFC 5709：OSPFv2 HMAC-SHA Cryptographic Authentication
• RFC 6571：Loop-Free Alternate (LFA) Applicability in Service Provider (SP) Networks 6860：Hiding
• RFC Transit-Only Networks in OSPF 6987：OSPF
• RFC Stub Router Advertisement

#### 1.2 OSPF配置限制和指导

无论是哪种类型的路由器，都必须先使能 OSPF，否则 OSPF 协议将无法正常运行。在进行各项配置的时候应该先做好网络规划，错误的配置可能会导致相邻路由器之间无法相互传递信息，甚至导致路由信息的阻塞或者产生路由环路。

#### 1.3 OSPF配置任务简介

OSPF 配置任务如下：
(1) 配置OSPF基本功能启动OSPF进程(cid:123)
配置OSPF区域(cid:123)
使能OSPF功能(cid:123)
(2) （可选）配置OSPF特殊区域配置Stub区域(cid:123)
配置NSSA区域(cid:123)
配置虚连接(cid:123)
(3) （可选）配置OSPF的网络类型配置OSPF接口网络类型为广播(cid:123)
配置OSPF接口网络类型为NBMA (cid:123)
配置OSPF接口网络类型为P2MP (cid:123)
配置OSPF接口网络类型为P2P (cid:123)
（可选）配置OSPF的路由信息控制
(4)
配置OSPF区域间路由聚合(cid:123)
配置对引入的外部路由信息进行路由聚合(cid:123)
配置OSPF对通过接收到的LSA计算出来的路由信息进行过滤(cid:123)
配置过滤Type-3 LSA (cid:123)
配置OSPF接口的开销值(cid:123)
配置 OSPF 最大等价路由条数(cid:123)
配置OSPF协议的优先级(cid:123)
配置NULL0 路由(cid:123)
配置OSPF引入外部路由(cid:123)
配置OSPF引入缺省路由(cid:123)
配置发布一条主机路由(cid:123)
配置允许设备将OSPF链路状态信息发布到BGP (cid:123)
(5) （可选）配置 OSPF 定时器配置OSPF报文定时器(cid:123)
配置接口传送LSA的延迟时间(cid:123)
配置OSPF路由计算的时间间隔(cid:123)

配置LSA重复到达的最小时间间隔(cid:123)
配置LSA重新生成的时间间隔(cid:123)
配置OSPF尝试退出overflow状态的定时器时间间隔(cid:123)
(6) （可选）配置OSPF报文相关功能禁止接口收发OSPF报文(cid:123)
配置DD报文中的MTU (cid:123)
配置OSPF发送协议报文的DSCP优先级(cid:123)
配置接口发送OSPF报文的最大长度(cid:123)
配置发送LSU报文的速率(cid:123)
(7) （可选）控制LSA的生成、发布与接收配置LSDB中External LSA的最大数量(cid:123)
过滤接口出方向的LSA (cid:123)
过滤发送给指定邻居的LSA (cid:123)
(8) （可选）加快OSPF路由收敛速度配置ISPF (cid:123)
配置前缀抑制(cid:123)
配置OSPF的前缀按优先权收敛功能(cid:123)
配置PIC (cid:123)
（可选）配置OSPF高级功能
(9)
配置Stub路由器(cid:123)
配置兼容RFC 1583 的外部路由选择规则(cid:123)
(10) （可选）提高 OSPF 网络的可靠性配置OSPF GR (cid:123)
配置OSPF NSR (cid:123)
配置OSPF与BFD联动(cid:123)
配置OSPF快速重路由(cid:123)
(11) （可选）配置 OSPF 安全功能配置 OSPF 验证(cid:123)
配置OSPF GTSM功能(cid:123)
(12) （可选）配置OSPF日志和告警功能配置邻居状态变化的输出开关(cid:123)
配置OSPF的日志功能(cid:123)
配置OSPF网管功能(cid:123)

#### 1.4 配置OSPF基本功能

##### 1.4.1 启动OSPF进程

(1) 进入系统视图。

system-view
(2) （可选）配置全局 Router ID。
router id router-id缺省情况下，未配置全局 Router ID。
未配置全局路由器 ID 时，按照下面的规则进行选择：
如果存在配置 IP 地址的 Loopback 接口，则选择 Loopback 接口地址中最大的作为 Router (cid:123)
ID。
如果没有配置IP地址的Loopback接口，则从其他接口的IP地址中选择最大的作为Router (cid:123)
ID（不考虑接口的 状态）。
up/down进入 视图。
(3) OSPF ospf [ process-id | router-id router-id | vpn-instance vpn-instance-name ] *缺省情况下，系统没有运行 OSPF。
(4) （可选）配置 OSPF 进程描述。
description text缺省情况下，未配置进程描述。
建议用户为每个 进程配置进程描述信息，帮助识别进程的用途，以便于记忆和管理。
OSPF

##### 1.4.2 配置OSPF区域

(1) 进入系统视图。
system-view
(2) （可选）配置全局 Router ID。
router id router-id
缺省情况下，未配置全局 Router ID。
(3) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
缺省情况下，系统没有运行 OSPF。
(4) （可选）配置 OSPF 进程描述。
description text
缺省情况下，未配置进程描述。
建议用户为每个 OSPF 进程配置进程描述信息，帮助识别进程的用途，以便于记忆和管理。
(5) 创建 OSPF 区域，并进入 OSPF 区域。
area area-id
（可选）配置区域描述。
(6)
description text
缺省情况下，未配置区域描述。
建议用户为每个区域配置区域描述信息，帮助识别区域的用途，以便于记忆和管理。

(7) （可选）配置允许将区域下的接口从标准拓扑中分离。
capability default-exclusion
缺省情况下，OSPF 区域下的接口自动加入标准拓扑 base。
需要在本设备和邻居设备上同时配置本命令，否则会影响邻居关系的建立。

##### 1.4.3 使能OSPF功能

###### 1. 功能简介

要在路由器上使能 OSPF 功能，必须先创建 OSPF 进程、指定该进程关联的区域以及区域包括的网段；对于当前路由器来说，如果某个路由器的接口 地址落在某个区域的网段内，则该接口属于这IP个区域并使能了 OSPF 功能，OSPF 将把这个接口的直连路由宣告出去。
OSPF 支持多进程，即可以在一台路由器上通过为不同的 OSPF 进程指定不同的进程号来启动多个OSPF 进程。OSPF 进程号是本地概念，不影响与其它路由器之间的报文交换。因此，不同的路由器之间，即使进程号不同也可以进行报文交换。
OSPF 支持多实例，即可以指定 OSPF 进程所属的 VPN 。如果未指定 VPN ，则表示 OSPF 位于公网中。VPN 的相关内容请参见“MCE 配置指导”中的“MCE”。

###### 2. 配置限制和指导

可以在指定接口上使能 OSPF，或者在指定网段上使能 OSPF。在指定接口上使能 OSPF 的优先级高于在指定网段上使能 OSPF。
在接口上使能 OSPF 时，如果不存在进程和区域，则创建对应的进程和区域；在接口上关闭 OSPF时，不删除已经创建的进程和区域。

###### 3. 在指定网段上使能OSPF

进入系统视图。
(1)
system-view进入 视图。
(2) OSPF ospf [ process-id | router-id router-id | vpn-instance vpn-instance-name ] *
(3) 进入 OSPF 区域视图。
area area-id配置区域所包含的网段并在指定网段的接口上使能 OSPF。
(4)
network ip-address wildcard-mask缺省情况下，接口不属于任何区域且 功能处于关闭状态。
OSPF一个网段只能属于一个区域。

###### 4. 在指定接口上使能OSPF

(1) 进入系统视图。
system-view
进入接口视图。
(2)
interface interface-type interface-number
配置接口使能 OSPF。
(3)

ospf process-id area area-id [ exclude-subip ]缺省情况下，未配置接口使能 OSPF。

#### 1.5 配置OSPF特殊区域

##### 1.5.1 功能简介

网络管理员对整个网络划分区域完毕后，可以根据组网需要进一步将区域配置成 Stub 区域或 NSSA区域。
当非骨干区域不能与骨干区域保持连通，或者骨干区域因为各方面条件的限制无法保持连通时，可以通过配置 OSPF 虚连接予以解决。

##### 1.5.2 配置Stub区域

###### 1. 功能简介

对于位于 AS 边缘的一些非骨干区域，我们可以在该区域的所有路由器上配置 stub 命令，把该区域配置为 Stub 区域。这样，描述自治系统外部路由的 Type-5 LSA 不会在 Stub 区域里泛洪，减小了路由表的规模。ABR 生成一条缺省路由，所有到达自治系统外部的报文都交给 进行转发。
ABR如果想进一步减少 Stub 区域路由表规模以及路由信息传递的数量，那么在 ABR 上配置 stub 命令时指定 no-summary 参数，可以将该区域配置为 Totally Stub 区域。这样，自治系统外部路由和区域间的路由信息都不会传递到本区域，所有目的地是自治系统外和区域外的报文都交给 ABR 进行转发。
Stub 区域和 Totally Stub 区域内不能存在 ASBR，即自治系统外部的路由不能在本区域内传播。

###### 2. 配置限制和指导

骨干区域不能配置成 区域或 区域。
Stub Totally Stub如果要将一个区域配置成 Stub 区域，则该区域中的所有路由器必须都要配置 stub 命令。
如果要将一个区域配置成 Totally Stub 区域，该区域中的所有路由器必须配置 stub 命令，该区域的 路由器需要配置 命令。
ABR stub no-summary

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(3) 进入 OSPF 区域视图。
area area-id
(4) 配置当前区域为 Stub 区域。
stub [ default-route-advertise-always | no-summary ] *
缺省情况下，没有区域被设置为 Stub 区域。
(5) （可选）配置 ABR 发送到 Stub 区域缺省路由的开销。

default-cost cost-value缺省情况下，ABR 发送到 Stub 区域缺省路由的开销为 1。
本命令只有在 Stub 区域和 Totally Stub 区域的 ABR 上配置才能生效。

##### 1.5.3 配置NSSA区域

###### 1. 功能简介

Stub 区域不能引入外部路由，为了在允许将自治系统外部路由通告到 OSPF 路由域内部的同时，保持其余部分的 区域的特征，网络管理员可以将区域配置为 区域。NSSA 区域也是位Stub NSSA于 AS 边缘的非骨干区域。
配置 nssa 命令时指定 no-summary 参数可以将该区域配置为 Totally NSSA 区域，该区域的 ABR不会将区域间的路由信息传递到本区域。

###### 2. 配置限制和指导

骨干区域不能配置成 NSSA 区域或 Totally NSSA 区域。
如果要将一个区域配置成 NSSA 区域，则该区域中的所有路由器必须都要配置 nssa 命令。
如果要将一个区域配置成 Totally NSSA 区域，该区域中的所有路由器必须配置 nssa 命令，该区域的 路由器需要配置 命令。
ABR nssa no-summary

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(3) 进入 OSPF 区域视图。
area area-id
(4) 配置当前区域为 NSSA 区域。
nssa [ default-route-advertise [ cost cost-value | nssa-only |
route-policy route-policy-name | type type ] * | no-import-route |
no-summary | suppress-fa | [ [ [ translate-always ]
[ translate-ignore-checking-backbone ] ] | translate-never ] |
translator-stability-interval value ] *
缺省情况下，没有区域被设置为 NSSA 区域。
(5) （可选）配置发送到 NSSA 区域缺省路由的开销。
default-cost cost-value
缺省情况下，发送到 NSSA 区域的缺省路由的开销为 1。
本命令只有在 区域和 区域的 上配置才能生效。
NSSA Totally NSSA ABR/ASBR

###### 1. 功能简介

###### 3. 配置步骤

##### 1.5.4 配置虚连接

功能简介
1.
在划分区域之后，非骨干区域之间的 OSPF 路由更新是通过骨干区域来完成交换的。对此，OSPF要求所有非骨干区域必须与骨干区域保持连通，并且骨干区域自身也要保持连通。
但在实际应用中，可能会因为各方面条件的限制，无法满足这个要求。这时可以通过在 ABR 上配置 OSPF 虚连接予以解决。

###### 2. 配置限制和指导

虚连接不能穿过 Stub 区域和 Totally Stub 区域；虚连接不能穿过 NSSA 区域和 Totally NSSA 区域。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance vpn-instance-name ] *
(3) 进入 OSPF 区域视图。
area area-id
(4) 创建并配置虚连接。
vlink-peer router-id [ dead seconds | hello seconds | { { hmac-md5 | md5 } key-id { cipher | plain } string | keychain keychain-name | simple { cipher | plain } string } | retransmit seconds | trans-delay seconds ] *为使虚连接生效，在虚连接的两端都需配置此命令，并且两端配置的 hello、dead 参数必须一致。

#### 1.6 配置OSPF的网络类型

##### 1.6.1 配置限制和指导

OSPF 的网络类型有四种：广播、NBMA、P2MP 和 P2P。用户可以根据需要更改接口的网络类型，例如：
• 当广播网络中有部分路由器不支持组播时，可以将网络类型更改为 NBMA。
• 如果一网段内只有两台路由器运行 OSPF 协议，也可将接口类型配置为 P2P，节省网络开销。
如果接口配置为广播、NBMA 或者 P2MP 网络类型，只有双方接口在同一网段才能建立邻居关系。

##### 1.6.2 配置OSPF接口网络类型为广播

进入系统视图。
(1)
system-view
(2) 进入接口视图。
interface interface-type interface-number

(3) 配置 OSPF 接口网络类型为广播。
ospf network-type broadcast
缺省情况下，接口的网络类型为广播类型。
(4) （可选）配置 OSPF 接口的路由器优先级。
ospf dr-priority priority
缺省情况下，接口的路由器优先级为 1。

##### 1.6.3 配置OSPF接口网络类型为NBMA

###### 1. 配置限制和指导

把接口类型配置为 NBMA 后，由于无法通过广播 Hello 报文的形式动态发现相邻路由器，必须手工为接口指定相邻接口的 地址、该相邻接口是否有选举权等（dr-priority 参数的值仅表示路由IP器是否具有 DR 选举权，为 0 表示不具有 DR 选举权，大于 0 时表示具有 DR 选举权）。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置 OSPF 接口的网络类型为 NBMA。
ospf network-type nbma
缺省情况下，接口的网络类型为广播类型。
（可选）配置 接口的路由器优先级。
(4) OSPF
ospf dr-priority priority
缺省情况下，接口的路由器优先级为 1。
本命令设置的优先级用于实际的 选举。
DR
退回系统视图。
(5)
quit
(6) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
配置 网络的邻居。
(7) NBMA
peer ip-address [ dr-priority priority ]
缺省情况下，未配置邻居。
如果在配置邻居时将优先级指定为 0，则本地路由器认为该邻居不具备选举权，不向该邻居
发送 Hello 报文。本地路由器是 DR 或 BDR 的情况除外。

##### 1.6.4 配置OSPF接口网络类型为P2MP

(1) 进入系统视图。
system-view

###### 1. 功能简介

(2) 进入接口视图。
interface interface-type interface-number
(3) 配置 OSPF 接口的网络类型为 P2MP。
ospf network-type p2mp [ unicast ]
缺省情况下，接口的网络类型为广播类型。
(4) 退回系统视图。
quit
(5) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(6) 配置 P2MP 单播网络的邻居。
peer ip-address [ cost cost-value ]
缺省情况下，未配置邻居。
如果接口类型为 P2MP 单播，必须配置本命令。

##### 1.6.5 配置OSPF接口网络类型为P2P

进入系统视图。
(1)
system-view进入接口视图。
(2)
interface interface-type interface-number
(3) 配置 OSPF 接口的网络类型为 P2P。
ospf network-type p2p [ peer-address-check ]缺省情况下，接口的网络类型为广播类型。

#### 1.7 配置OSPF的路由信息控制

通过本节的配置，可以控制 OSPF 的路由信息的发布与接收，并引入路由信息。

##### 1.7.1 配置OSPF区域间路由聚合

功能简介
1.
OSPF 区域间路由聚合是指 ABR 将具有相同前缀的路由信息聚合，只发布一条路由到其它区域。
AS 被划分成不同的区域后，每一个区域通过 OSPF 区域边界路由器（ABR）相连，区域间可以通过路由聚合来减少路由信息，减小路由表的规模，提高路由器的运算速度。
ABR 在计算出一个区域的区域内路由之后，根据聚合相关设置，将其中多条 OSPF 路由聚合成一条发送到区域之外。例如，某个区域内有三条区域内路由 19.1.1.0/24，19.1.2.0/24，19.1.3.0/24，如果在 ABR 上配置了路由聚合，将三条路由聚合成一条 19.1.0.0/16 ，则 ABR 就只生成一条聚合后的 Type-3 LSA，并发布给其它区域的路由器，这样既可以减少其它区域中 LSDB 的规模，也减小了因为网络拓扑变化带来的影响。

###### 1. 功能简介

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(3) 进入 OSPF 区域视图。
area area-id
(4) 配置 ABR 路由聚合。
abr-summary ip-address { mask-length | mask } [ advertise | not-advertise ]
[ cost cost-value ]
缺省情况下，ABR 不对路由进行聚合。

##### 1.7.2 配置对引入的外部路由信息进行路由聚合

功能简介
1.
ASBR 引入外部路由后，每一条路由都会放在单独的一条 Type-5 LSA 中向外宣告；通过配置路由聚合，路由器只把聚合后的路由放在 中向外宣告，减少了 中 的数量。
Type-5 LSA LSDB LSA在 上配置路由聚合后，将对聚合地址范围内的 进行聚合；如果 在ASBR Type-5 LSA ASBR NSSA区域里面，将对聚合地址范围内的 Type-7 LSA 进行聚合。

###### 2. 配置限制和指导

如果本地路由器同时是 ASBR 和 ABR，并且是 NSSA 区域的转换路由器，将对由 Type-7 LSA 转化成的 Type-5 LSA 进行聚合处理；如果不是 NSSA 区域的转换路由器，则不进行聚合处理。

###### 3. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance vpn-instance-name ] *配置 路由聚合。
(3) ASBR asbr-summary ip-address { mask-length | mask } [ cost cost-value | not-advertise | nssa-only | tag tag ] *缺省情况下，ASBR 不对路由进行聚合。

##### 1.7.3 配置OSPF对通过接收到的LSA计算出来的路由信息进行过滤

###### 1. 功能简介

OSPF 是基于链路状态的动态路由协议，路由信息是根据接收到的 LSA 计算出来的，可以对通过接收到的 LSA 计算出来的 OSPF 路由信息进行过滤。

一共有四种过滤方式：
基于要加入到路由表的路由信息的目的地址进行过滤，可以通过配置访问控制列表或 IP 地址
•前缀列表来指定过滤条件；
基于要加入到路由表的路由信息的下一跳进行过滤，可以通过在命令中配置 参数来
• gateway指定过滤条件；
• 基于要加入到路由表的路由信息的目的地址和下一跳进行过滤，可以通过配置访问控制列表或 IP 地址前缀列表指定过滤目的地址的条件，同时配置 gateway 参数来指定过滤下一跳的条件；
基于路由策略对要加入到路由表的路由信息进行过滤，可以通过在命令中配置
•参数来指定过滤条件。
route-policy

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(3) 配置 OSPF 对通过接收到的 LSA 计算出来的路由信息进行过滤。
filter-policy { ipv4-acl-number [ gateway prefix-list-name ] | gateway
prefix-list-name | prefix-list prefix-list-name [ gateway
prefix-list-name ] | route-policy route-policy-name } import
缺省情况下，OSPF 不对通过接收到的 LSA 计算出来的路由信息进行过滤。

##### 1.7.4 配置过滤Type-3 LSA

###### 1. 功能简介

通过在 上配置 过滤，可以对进入 所在区域或 向其它区域发布的ABR Type-3 LSA ABR ABR Type-3 LSA 进行过滤。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(3) 进入 OSPF 区域视图。
area area-id
(4) 配置对 Type-3 LSA 进行过滤。
filter { ipv4-acl-number | prefix-list prefix-list-name | route-policy
route-policy-name } { export | import }
缺省情况下，不对 Type-3 LSA 进行过滤。

###### 1. 功能简介

##### 1.7.5 配置OSPF接口的开销值

功能简介
1.
OSPF 有两种方式来配置接口的开销值：
• 在接口视图下直接配置开销值；
• 配置接口的带宽参考值，OSPF 根据带宽参考值自动计算接口的开销值，计算公式为：接口开销＝带宽参考值÷接口期望带宽（接口期望带宽通过命令 bandwidth 进行配置，具体情况请参见接口分册命令参考中的介绍）。当计算出来的开销值大于 65535时，开销取最大值 65535；
当计算出来的开销值小于 1 时，开销取最小值 1。

###### 2. 配置接口的开销值

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 设置 OSPF 接口的开销值。
ospf cost cost-value
缺省情况下，接口按照当前的带宽自动计算接口运行 OSPF协议所需的开销。对于 Loopback
接口，缺省值为 0。

###### 3. 配置带宽参考值

(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
配置带宽参考值。
(3)
bandwidth-reference value
缺省情况下，带宽参考值为 100Mbps。

##### 1.7.6 配置OSPF最大等价路由条数

###### 1. 功能简介

如果到一个目的地有几条开销相同的路径，可以实现等价路由负载分担，IP 报文在这几个链路上负载分担，以提高链路利用率。该配置用以设置 OSPF 协议的最大等价路由条数。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *

###### 2. 配置步骤

(3) 配置 OSPF 最大等价路由条数。
maximum load-balancing number
缺省情况下，OSPF 支持的等价路由的最大条数与系统支持最大等价路由的条数相同。

##### 1.7.7 配置OSPF协议的优先级

###### 1. 功能简介

由于路由器上可能同时运行多个动态路由协议，就存在各个路由协议之间路由信息共享和选择的问题。系统为每一种路由协议设置一个优先级，在不同协议发现同一条路由时，优先级高的路由将被优先选择。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance vpn-instance-name ] *
(3) 配置 OSPF 协议的路由优先级。
preference [ ase ] { preference | route-policy route-policy-name } *缺省情况下，OSPF 协议对自治系统内部路由的优先级为 10，对自治系统外部路由的优先级为 150。

##### 1.7.8 配置NULL0路由

###### 1. 功能简介

本命令用来配置是否产生 路由以及产生 路由的优先级。
NULL0 NULL0

###### 2. 配置步骤

(1) 进入系统视图。
system-view
进入 视图。
(2) OSPF
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(3) 配置 NULL0 路由以及 NULL0 路由的优先级。
discard-route { external { preference | suppression } | internal
{ preference | suppression } } *
缺省情况下，产生引入聚合 NULL0 路由和区域间聚合 NULL0 路由，且 NULL0 路由优先级为
255。

###### 1. 功能简介

##### 1.7.9 配置OSPF引入外部路由

功能简介
1.
如果在路由器上不仅运行 OSPF，还运行着其它路由协议，可以配置 OSPF 引入其它协议生成的路由，将这些路由信息通过 或 向外宣告。
Type5 LSA Type7 LSA OSPF 还可以对引入的路由进行过滤，只将满足过滤条件的外部路由转换为 Type5 LSA 或 Type7 LSA 发布出去。

###### 2. 配置限制和指导

只 能 引 入 路 由 表 中 状 态 为 active 的 路 由 ， 是 否 为 active 状 态 可 以 通 过 display ip routing-table protocol 命令来查看。

###### 3. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance vpn-instance-name ] *配置 引入外部路由。
(3) OSPF import-route bgp [ as-number ] [ allow-ibgp ] [ [ cost cost-value | inherit-cost ] | nssa-only | route-policy route-policy-name | tag tag | type type ] * import-route { direct | static } [ [ cost cost-value | inherit-cost ] | nssa-only | route-policy route-policy-name | tag tag | type type ] * import-route { isis | ospf | rip } [ process-id | all-processes ] [ allow-direct | [ cost cost-value | inherit-cost ] | nssa-only | route-policy route-policy-name | tag tag | type type ] *缺省情况下，不引入外部路由。
执行 import-route 命令引入 BGP 路由时，未指定 allow-ibgp 参数表示只引入 EBGP路由；指定 allow-ibgp 参数表示将 IBGP 路由也引入，容易引起路由环路，请慎用。
(4) （可选）配置对引入的路由进行过滤。
filter-policy { ipv4-acl-number | prefix-list prefix-list-name } export [ protocol [ process-id ] ]缺省情况下，不对引入的路由信息进行过滤。
(5) 配置路由引入时的参数缺省值（开销、标记、类型）。
default { cost cost-value | tag tag | type type } *缺省情况下，OSPF 引入的路由的度量值为 1，引入的路由的标记为 1，引入的路由类型为2。

###### 1. 功能简介

##### 1.7.10 配置OSPF引入缺省路由

功能简介
1.
OSPF 不能通过 import-route 命令从其它协议引入缺省路由，如果想把缺省路由引入到 OSPF路由区域，必须执行本配置。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
进入 视图。
(2) OSPF
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(3) 配置 OSPF 引入缺省路由。
default-route-advertise [ [always | permit-calculate-other ] | cost
cost-value | route-policy route-policy-name | type type ] *
default-route-advertise [ summary cost cost-value ]
缺省情况下，不引入缺省路由。
default-route-advertise summary cost 命令仅在 VPN 中应用，以 Type-3 LSA 引
入缺省路由，PE 路由器会将引入的缺省路由发布给 CE 路由器。
(4) 配置路由引入时的参数缺省值（开销、标记、类型）。
default { cost cost-value | tag tag | type type } *
缺省情况下，OSPF 引入的路由的度量值为 1，引入的路由的标记为 1，引入的路由类型为
2。

##### 1.7.11 配置发布一条主机路由

(1) 进入系统视图。
system-view
进入 视图。
(2) OSPF
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(3) 进入 OSPF 区域视图。
area area-id
(4) 配置并发布一条主机路由。
host-advertise ip-address cost
缺省情况下，OSPF 不发布所包含网段之外的主机路由。

###### 1. 功能简介

##### 1.7.12 配置允许设备将OSPF链路状态信息发布到BGP

功能简介
1.
本功能允许设备将链路状态信息发布到 BGP，由 BGP 向外发布，以满足需要知道链路状态信息的应用的需求。BGP 的相关内容请参见“三层技术-IP 路由配置指导”中的“BGP”。
LS

###### 2. 配置步骤

(1) 进入系统视图。
system-view
进入 视图。
(2) OSPF
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(3) 配置允许设备将 OSPF 链路状态信息发布到 BGP。
distribute bgp-ls [ strict-link-checking ]
缺省情况下，不允许设备将 OSPF 链路状态信息发布到 BGP。

#### 1.8 配置OSPF定时器

##### 1.8.1 功能简介

通过改变 的报文定时器，可以调整 网络的收敛速度以及协议报文带来的网络负荷。在OSPF OSPF一些低速链路上，需要考虑接口传送 LSA 的延迟时间。

##### 1.8.2 配置OSPF报文定时器

###### 1. 功能简介

用户可以在接口上配置下列 OSPF 报文定时器：
• Hello 定时器：接口向邻居发送 Hello 报文的时间间隔，OSPF 邻居之间的 Hello 定时器的值要保持一致。
• Poll 定时器：在 NBMA 网络中，路由器向状态为 down 的邻居路由器发送轮询 Hello 报文的时间间隔。
邻居失效时间：在邻居失效时间内，如果接口还没有收到邻居发送的 Hello 报文，路由器就会
•宣告该邻居无效。
接口重传 的时间间隔：路由器向它的邻居通告一条 后，需要对方进行确认。若在重
• LSA LSA传间隔时间内没有收到对方的确认报文，就会向邻居重传这条 LSA。

###### 2. 配置限制和指导

Hello 报文中包含 Hello 定时器和邻居失效时间，对于不同的网络类型，Hello 定时器和邻居失效时间的缺省值不同。修改网络类型时，Hello 定时器和邻居失效时间将恢复为对应网络类型下的缺省值。请确保邻居路由器两端的 Hello 定时器和邻居失效时间的值保持一致，否则将影响 OSPF 邻居关系的建立。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置 Hello 定时器。
ospf timer hello seconds
缺省情况下，P2P、Broadcast 类型接口发送 Hello 报文的时间间隔为 10 秒，P2MP、NBMA
类型接口发送 Hello 报文的时间间隔为 30 秒。
(4) 配置 Poll 定时器。
ospf timer poll seconds
缺省情况下，发送轮询 Hello 报文的时间间隔为 120 秒。
轮询 Hello 报文的时间间隔至少应为 Hello 时间间隔的 4 倍。
(5) 配置邻居失效时间。
ospf timer dead seconds
缺省情况下，P2P、Broadcast 类型接口的 邻居失效时间为 秒，P2MP、NBMA 类
OSPF 40
型接口的 OSPF 邻居失效时间为 120 秒。
邻居失效时间应至少为 Hello 时间间隔的 4 倍。
(6) 配置接口重传 LSA 的时间间隔。
ospf timer retransmit seconds
缺省情况下，时间间隔为 5 秒。
相邻路由器重传 时间间隔的值不要设置得太小，否则将会引起不必要的重传。通常应该
LSA
大于一个报文在两台路由器之间传送一个来回的时间。

##### 1.8.3 配置接口传送LSA的延迟时间

###### 1. 功能简介

考虑到 OSPF 报文在链路上传送时也需要花费时间，所以 LSA 的老化时间（age）在传送之前要增加一定的延迟时间，在低速链路上需要对该项配置进行重点考虑。

###### 2. 配置步骤

进入系统视图。
(1)
system-view进入接口视图。
(2)
interface interface-type interface-number
(3) 配置接口传送 LSA 的延迟时间。
ospf trans-delay seconds缺省情况下，接口传送 LSA 的延迟时间为 1 秒。

###### 1. 功能简介

##### 1.8.4 配置OSPF路由计算的时间间隔

功能简介
1.
当 OSPF 的 LSDB 发生改变时，需要重新计算最短路径。如果网络频繁变化，且每次变化都立即计算最短路径，将会占用大量系统资源，并影响路由器的效率。通过调节路由计算的时间间隔，可以抑制由于网络频繁变化带来的影响。
本命令在网络变化不频繁的情况下将连续路由计算的时间间隔缩小到 minimum-interval，而在网络变化频繁的情况下可以进行相应惩罚，将等待时间按照配置的惩罚增量延长，增加incremental-interval × 2 n-2 （ n 为 连 续 触 发 路 由 计 算 的 次 数 ）， 最 大 不 超 过maximum-interval。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(3) 配置 OSPF 路由计算的时间间隔。
spf-schedule-interval maximum-interval [ minimum-interval
[ incremental-interval ] ]
缺省情况下，OSPF 路由计算的最大时间间隔为 5 秒，最小时间间隔为 50 毫秒，时间间隔惩
罚增量为 200 毫秒。

##### 1.8.5 配置LSA重复到达的最小时间间隔

###### 1. 功能简介

如果在重复到达的最小时间间隔内连续收到一条 LSA 类型、LS ID、生成路由器 ID 均相同的 LSA则直接丢弃，这样就可以抑制网络频繁变化可能导致的带宽资源和路由器资源被过多占用的问题。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(3) 配置 LSA 重复到达的最小时间间隔。
lsa-arrival-interval interval
缺省情况下，OSPF LSA 重复到达的最小时间间隔为 1000 毫秒。

###### 1. 功能简介

###### 2. 配置步骤

##### 1.8.6 配置LSA重新生成的时间间隔

功能简介
1.
通过调节 LSA 重新生成的时间间隔，可以抑制网络频繁变化可能导致的带宽资源和路由器资源被过多占用的问题。
本命令在网络变化不频繁的情况下将 LSA 重新生成时间间隔缩小到 minimum-interval，而在网n-2络变化频繁的情况下可以进行相应惩罚，增加 incremental-interval×2 （n 为连续触发路由计算的次数），将等待时间按照配置的惩罚增量延长，最大不超过 maximum-interval。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance vpn-instance-name ] *
(3) 配置 LSA 重新生成的时间间隔。
lsa-generation-interval maximum-interval [ minimum-interval [ incremental-interval ] ]缺省情况下，最大时间间隔为 秒，最小时间间隔为 毫秒，惩罚增量为 毫秒。
5 50 200

##### 1.8.7 配置OSPF尝试退出overflow状态的定时器时间间隔

###### 1. 功能简介

网络中出现过多 LSA，会占用大量系统资源。当设置的 中 的最大数量达到上LSDB External LSA限时，LSDB 会进入 overflow 状态，在 overflow 状态中，不再接收 External LSA，同时删除自己生成的 External LSA，对于已经收到的 External LSA 则不会删除。这样就可以减少 LSA 从而节省系统资源。
通过配置可以调整 OSPF 退出 overflow 状态的时间。

###### 2. 配置步骤

进入系统视图。
(1)
system-view进入 视图。
(2) OSPF ospf [ process-id | router-id router-id | vpn-instance vpn-instance-name ] *
(3) 配置 OSPF 尝试退出 overflow 状态的定时器时间间隔。
lsdb-overflow-interval interval缺省情况下，OSPF 尝试退出 定时器间隔是 秒，配置为 时，表示不退出overflow 300 0 Overflow 状态。

###### 2. 配置步骤

#### 1.9 配置OSPF报文相关功能

##### 1.9.1 禁止接口收发OSPF报文

###### 1. 功能简介

如果要使 OSPF 路由信息不被某一网络中的路由器获得，可以禁止接口收发 OSPF 报文。
将运行 协议的接口指定为 状态后，该接口的直连路由仍可以由同一路由器的其它接口OSPF Silent通过 Router LSA 发布出去，但 OSPF 报文将被阻塞，接口上无法建立邻居关系。这样可以增强 OSPF的组网适应能力，减少系统资源的消耗。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
禁止接口收发 报文。
(3) OSPF
silent-interface { interface-type interface-number | all }
缺省情况下，允许接口收发 OSPF 报文。
不同的进程可以对同一接口禁止收发 OSPF 报文，但本命令只对本进程已经使能的 OSPF 接
口起作用，对其它进程的接口不起作用。

##### 1.9.2 配置DD报文中的MTU

###### 1. 功能简介

一般情况下，接口发送 DD 报文时不使用接口的实际 MTU 值，而是用 0 代替。进行此配置后，将使用接口的实际 MTU 值填写 DD 报文 Interface MTU 字段。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置 DD 报文中 MTU 域的值为发送该报文接口的 MTU 值。
ospf mtu-enable缺省情况下，接口发送的 DD 报文中 MTU 域的值为 0。

##### 1.9.3 配置OSPF发送协议报文的DSCP优先级

###### 1. 功能简介

DSCP 优先级用来体现报文自身的优先等级，决定报文传输的优先程度。通过本配置可以指定 OSPF发送协议报文的 DSCP 优先级。

###### 2. 配置步骤

###### 1. 功能简介

###### 2. 配置步骤

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(3) 配置 OSPF 发送协议报文的 DSCP 优先级。
dscp dscp-value
缺省情况下，OSPF 发送协议报文的 DSCP 优先级值为 48。

##### 1.9.4 配置接口发送OSPF报文的最大长度

功能简介
1.
本功能用于需要对接口发送OSPF报文的大小进行限制的场景。例如，通过隧道建立OSPF邻居时，为避免隧道口发送的 OSPF 报文分片，可用此命令在隧道口上设置 OSPF 报文的最大长度，保证报文的最大长度+封装报文头长度≤隧道出接口的 MTU。关于隧道的详细介绍请参见“三OSPF IP层技术-IP 业务配置指导”中的“隧道”。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置接口发送 OSPF 报文的最大长度。
ospf packet-size value缺省情况下，接口发送 OSPF 报文的最大长度为本接口的 IP MTU 值。

##### 1.9.5 配置发送LSU报文的速率

###### 1. 功能简介

在与邻居进行 LSDB 同步的过程中，需要发送大量的 LSU 报文时，邻居设备会在短时间内收到大量的 LSU 报文，处理这些突发的大量 LSU 报文时，可能会出现如下情况：
• 占用较多的系统资源，导致邻居设备性能下降。
• 邻居设备可能会将维持邻居关系的 Hello 报文丢弃，导致邻居关系断开。重新建立邻居关系的过程中，需要交互的 LSU 数量将会更大，从而加剧设备性能的下降。
配置本功能后，路由器将 LSU 报文分为多个批次进行发送，对 OSPF 接口每次允许发送的 LSU 报文的最大个数做出限制；同时，在指定的时间间隔内，所有运行 的接口发送 的最大个OSPF LSU数不能超过限定值，即对整机发送 LSU 的速率进行限制，从而避免上述情况的发生。
配置步骤
2.
(1) 进入系统视图。
system-view

(2) 开启 OSPF 限制 LSU 发送速率功能。
ospf lsu-flood-control [ interval count ]
缺省情况下，OSPF 不对 LSU 的发送速率进行限制。
调整 OSPF 对 LSU 的发送速率时，如果配置不当可能会造成路由异常等情况，请谨慎配置。
通常情况下，建议使用缺省值。
进入 视图。
(3) OSPF
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
（可选）配置接口发送 报文的时间间隔和一次发送 报文的最大个数。
(4) LSU LSU
transmit-pacing interval interval count count
缺省情况下，OSPF接口发送 LSU报文的时间间隔为 20毫秒，一次最多发送 3个 LSU报文。
用户可根据需要配置 接口发送 报文的时间间隔以及接口一次发送 报文的最
OSPF LSU LSU
大个数。

#### 1.10 控制LSA的生成、发布与接收

##### 1.10.1 配置LSDB中External LSA的最大数量

(1) 进入系统视图。
system-view
进入 视图。
(2) OSPF
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(3) 配置 LSDB 中 External LSA 的最大数量。
lsdb-overflow-limit number
缺省情况下，不对 LSDB 中 External LSA 的最大条目数进行限制。

##### 1.10.2 过滤接口出方向的LSA

###### 1. 功能简介

通过该功能，不希望让邻居接收到的 LSA 可在本端接口出方向上被过滤掉，从而减小邻居 LSDB的规模，并节省带宽。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置过滤接口出方向的 LSA。
ospf database-filter { all | { ase [ acl ipv4-acl-number ] | nssa [ acl
ipv4-acl-number ] | summary [ acl ipv4-acl-number ] } * }

缺省情况下，不对接口出方向的 LSA 进行过滤。

##### 1.10.3 过滤发送给指定邻居的LSA

###### 1. 功能简介

在 网络中，一台路由器可以有多个接口的网络类型为 的 邻居。当两台路由器P2MP P2MP OSPF之间存在多条 P2MP 链路时，不希望让某个指定邻居收到的 LSA，通过该功能可在本地被过滤掉。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(3) 配置过滤发送给接口的网络类型为 P2MP 的邻居的 LSA。
database-filter peer ip-address { all | { ase [ acl ipv4-acl-number ] |
nssa [ acl ipv4-acl-number ] | summary [ acl ipv4-acl-number ] } * }
缺省情况下，不对发送给接口的网络类型为 P2MP 的邻居的 LSA 进行过滤。

#### 1.11 加快OSPF路由收敛速度

##### 1.11.1 配置ISPF

###### 1. 功能简介

ISPF（Incremental Shortest Path First，增量最短路径优先）是对 OSPF 中最短路径树的增量计算，当网络的拓扑结构发生变化，即影响到最短路径树的结构时，只对受影响的部分节点进行重新计算拓扑结构，只对最短路径树中受影响的部分进行修正，而不需要重建整棵最短路径树。

###### 2. 配置步骤

进入系统视图。
(1)
system-view进入 视图。
(2) OSPF ospf [ process-id | router-id router-id | vpn-instance vpn-instance-name ] *
(3) 开启增量 SPF 计算功能。
ispf enable缺省情况下，增量 计算功能处于使能状态。
SPF

###### 1. 功能简介

##### 1.11.2 配置前缀抑制

功能简介
1.
OSPF 使能网段时会将接口上匹配该网段的所有网段路由与主机路由都通过 LSA 发布，但有些时候主机路由或网段路由是不希望被发布的。通过前缀抑制配置，可以减少 中携带不需要的前缀，LSA即不发布某些网段路由和主机路由，从而提高网络安全性，加快路由收敛。
当使能前缀抑制时，具体情况如下：
或 类型网络：Type-1 中不发布接口的主地址，即 中链路类型为
• P2P P2MP LSA Type-1 LSA 3 的 Stub 链路被抑制，不生成接口路由，但其他路由信息可以正常计算，不会影响流量转发。
• 广播类型或者 NBMA 网络：DR 发布的 Type-2 LSA 的掩码字段会填成 32 位，即不生成网段路由，但其他路由信息可以正常计算，不会影响流量转发。另外，如果没有邻居，发布的 Type-1中也不发布接口的主地址，即 中链路类型为 的 链路被抑制。
LSA Type-1 LSA 3 Stub

###### 2. 配置限制和指导

如果需要抑制前缀发布，建议整个 OSPF 网络都配置本命令。

###### 3. 配置全局前缀抑制

(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(3) 配置前缀抑制功能。
prefix-suppression
缺省情况下，不抑制 OSPF 进程进行前缀发布。
不能抑制从地址、LoopBack 接口以及处于抑制状态的接口对应的前缀。

###### 4. 配置接口前缀抑制

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置接口的前缀抑制功能。
ospf prefix-suppression [ disable ]
缺省情况下，不抑制接口进行前缀发布。
不能抑制从地址对应的前缀。

###### 1. 功能简介

##### 1.11.3 配置OSPF的前缀按优先权收敛功能

功能简介
1.
通过策略指定优先权，不同前缀按优先权顺序下发，由高到低分为 4 个优先权（Critical、High、和 Low），如果一条路由符合多个收敛优先权的匹配规则，则这些收敛优先权中最高者当选Medium为路由的收敛优先权。
OSPF 路由的 32 位主机路由为 Medium 优先权，其它为 Low 优先权。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(3) 使能 OSPF 的前缀按优先权快速收敛功能。
prefix-priority route-policy route-policy-name
缺省情况下，OSPF 的前缀按优先权快速收敛功能处于关闭状态。

##### 1.11.4 配置PIC

###### 1. 功能简介

PIC（Prefix Independent Convergence，前缀无关收敛），即收敛时间与前缀数量无关，该功能可以加快收敛速度。传统的路由计算快速收敛都与前缀数量相关，收敛时间与前缀数量成正比。

###### 2. 配置限制和指导

和 快速重路由功能同时配置时，OSPF 快速重路由功能生效。
PIC OSPF目前只支持区域间路由以及外部路由的 功能。
PIC

###### 3. 使能PIC功能

(1) 进入系统视图。
system-view
进入 视图。
(2) OSPF
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(3) 使能 PIC 功能。
pic [ additional-path-always ]
缺省情况下，前缀无关收敛功能处于使能状态。

###### 4. 配置PIC支持BFD检测功能（Ctrl方式）

(1) 进入系统视图。
system-view
(2) 进入接口视图。

###### 1. 功能简介

###### 2. 配置步骤

interface interface-type interface-number
(3) 使能 OSPF 协议中主用链路的 BFD（Ctrl 方式）检测功能。
ospf primary-path-detect bfd ctrl缺省情况下，OSPF 协议中主用链路的 BFD（Ctrl 方式）检测功能处于关闭状态。
配置本功能后，可以加快 OSPF 协议的收敛速度。使用 control 报文双向检测方式时，需要建立 邻居的两端设备均支持 配置。
OSPF BFD

###### 5. 配置PIC支持BFD检测功能（Echo方式）

(1) 进入系统视图。
system-view
配置 报文源地址。
(2) BFD Echo
bfd echo-source-ip ip-address
缺省情况下，未配置 报文源地址。
BFD Echo
报文的源 地址用户可以任意指定。建议配置 报文的源 地址不属于该设备任何
echo IP echo IP
一个接口所在网段。
本命令的详细情况请参见“可靠性命令参考”中的“BFD”。
进入接口视图。
(3)
interface interface-type interface-number
使能 协议中主用链路的 BFD（Echo 方式）检测功能。
(4) OSPF
ospf primary-path-detect bfd echo
缺省情况下，OSPF 协议中主用链路的 BFD（Echo 方式）检测功能处于关闭状态。
配置本功能后，可以加快 OSPF 协议的收敛速度。使用 echo 报文单跳检测方式时，仅需要一
端设备支持 配置。
BFD

#### 1.12 配置OSPF高级功能

##### 1.12.1 配置Stub路由器

功能简介
1.
Stub 路由器用来控制流量，它告知其他 OSPF 路由器不要使用这个 Stub 路由器来转发数据，但可以拥有一个到 路由器的路由。
Stub通过将当前路由器配置为 路由器，在该路由器发布的 中，当链路类型取值为 表Stub Router LSA 3示连接到 Stub 网络时，链路度量值不变；当链路类型为 1、2、4 分别表示通过 P2P 链路与另一路由器相连、连接到传送网络、虚连接时，链路度量值将设置为最大值 65535。通过增加include-stub 参数可以将路由器发布的 Router LSA 中，链路类型为 3 的 Stub 链路度量值设置为最大值 65535。这样其邻居计算出这条路由的开销就会很大，如果邻居上有到这个目的地址开销更小的路由，则数据不会通过这个 Stub 路由器转发。
配置步骤
2.
(1) 进入系统视图。
system-view

###### 1. 功能简介

###### 3. 配置步骤

(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
配置当前路由器为 路由器。
(3) Stub
stub-router [ external-lsa [ max-metric-value ] | include-stub |
on-startup { seconds | wait-for-bgp [ seconds ] } | summary-lsa
[ max-metric-value ] ] *
缺省情况下，当前路由器没有被配置为 Stub 路由器。
Stub 路由器与 Stub 区域无关。

##### 1.12.2 配置兼容RFC 1583的外部路由选择规则

功能简介
1.
当有多条路径可以到达同一个外部路由时，在选择最优路由的问题上，RFC 2328 中定义的选路规则与 RFC 1583 的有所不同，进行此配置可以兼容 RFC 1583 中定义的规则。
具体的选路规则如下：
(1) 当 RFC 2328 兼容 RFC 1583 时，所有到达 ASBR 的路由优先级相同。当 RFC 2328 不兼容时，非骨干区的区域内路由优先级最高，区域间路由与骨干区区域内路由优先级RFC 1583相同，优选非骨干区的区域内路由，尽量减少骨干区的负担；
(2) 若存在多条优先级相同的路由时，按开销值优选，优选开销值小的路由；
(3) 若存在多条开销值相同路由时，按路由来源区域的区域 ID 选择，优选区域 ID 大的路由。

###### 2. 配置限制和指导

为了避免路由环路，同一路由域内的路由器建议统一配置相同选择规则。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance vpn-instance-name ] *
(3) 配置兼容 RFC 1583 的外部路由选择规则。
rfc1583 compatible缺省情况下，兼容 RFC 1583 的路由选择优先规则的功能处于开启状态。

#### 1.13 配置OSPF GR

##### 1.13.1 功能简介

GR（Graceful Restart，平滑重启）是一种通过备份 OSPF 配置信息，在协议重启或主备倒换时OSPF 进行平滑重启，从邻居那里获得邻居关系，并对 LSDB 进行同步，从而保证转发业务不中断的机制。

###### 1. 配置IETF标准GR Restarter

###### 2. 配置非IETF标准GR Restarter

GR 有两个角色：
GR Restarter：发生协议重启或主备倒换事件且具有 GR 能力的设备。
•GR Helper：和 GR Restarter 具有邻居关系，协助完成 GR 流程的设备。
•目前有两种方式实现 OSPF GR 技术：
• 一种是基于 IETF 标准，GR Restarter 通过向 GR Helper 发送一种称为 Grace LSA 的 9 类来控制 的交互过程。
Opaque LSA GR另外一种是非 IETF 标准，GR Restarter 与 GR Helper 之间是通过相互发送携带 LLS 与 OOB
•扩展信息的 OSPF 报文来完成 GR 的交互过程。
一台设备可以同时充当 和 Helper。
GR Restarter GR

##### 1.13.2 配置限制和指导

设备充当 GR Restarter 后不能再配置 OSPF NSR 功能。

##### 1.13.3 配置GR Restarter

配置IETF标准GR
1. Restarter
(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance vpn-instance-name ] *
(3) 使能 Opaque LSA 发布接收能力。
opaque-capability enable缺省情况下，OSPF 的 Opaque LSA 发布接收能力处于开启状态。
(4) 使能 OSPF 协议的 IETF 标准 GR 能力。
graceful-restart ietf [ global | planned-only ] *缺省情况下，OSPF 协议的 IETF 标准 GR 能力处于关闭状态。
(5) （可选）配置 OSPF 协议的 GR 重启间隔时间。
graceful-restart interval interval缺省情况下，OSPF 协议的 GR 重启间隔时间为 120 秒。
配置非IETF标准GR
2. Restarter
(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance vpn-instance-name ] *
(3) 使能 OSPF 本地链路信令能力。
enable link-local-signaling

###### 2. 配置非IETF标准GR Helper

缺省情况下，OSPF 本地链路信令能力处于关闭状态。
(4) 使能 OSPF 带外同步能力。
enable out-of-band-resynchronization缺省情况下，OSPF 带外同步能力处于关闭状态。
(5) 使能 OSPF 协议的非 IETF 标准 GR 能力。
graceful-restart [ nonstandard ] [ global | planned-only ] *缺省情况下，OSPF 协议的非 IETF 标准 GR 能力处于关闭状态。
(6) （可选）配置 OSPF 协议的 GR 重启间隔时间。
graceful-restart interval interval缺省情况下，OSPF 协议的 GR 重启间隔时间为 120 秒。

##### 1.13.4 配置GR Helper

###### 1. 配置IETF标准GR Helper

(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(3) 使能 Opaque LSA 发布接收能力。
opaque-capability enable
缺省情况下，OSPF 的 Opaque LSA 发布接收能力处于开启状态。
(4) 使能 GR Helper 能力。
graceful-restart helper enable [ planned-only ]
缺省情况下，OSPF 的 GR Helper 能力处于开启状态。
(5) （可选）配置 GR Helper 严格检查 LSA 能力。
graceful-restart helper strict-lsa-checking
缺省情况下，OSPF 协议的 GR Helper 严格 LSA 检查能力处于关闭状态。
执行本配置后，当检查到 设备的 发生变化时， 设备退出
GR Helper LSA Helper GR Helper
模式。
配置非IETF标准GR
2. Helper
(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(3) 使能 OSPF 本地链路信令能力。
enable link-local-signaling

#### 1.14 配置OSPF NSR

##### 1. 功能简介

##### 3. 配置步骤

缺省情况下，OSPF 本地链路信令能力处于关闭状态。
(4) 使能 OSPF 带外同步能力。
enable out-of-band-resynchronization缺省情况下，OSPF 带外同步能力处于关闭状态。
(5) 使能 GR Helper 能力。
graceful-restart helper enable缺省情况下，OSPF 的 GR Helper 能力处于开启状态。
(6) （可选）配置 GR Helper 严格检查 LSA 能力。
graceful-restart helper strict-lsa-checking缺省情况下，OSPF 协议的 GR Helper 严格 LSA 检查能力处于关闭状态。
执行本配置后，当检查到 GR Helper 设备的 LSA 发生变化时，Helper 设备退出 GR Helper模式。

##### 1.13.5 以GR方式重启OSPF进程

功能简介
1.
设备进行主备倒换或者进行如下操作均可以以 GR 方式重启 OSPF 进程。

###### 2. 配置步骤

请在用户视图下执行本命令，以 方式重启 进程。
GR OSPF reset ospf [ process-id ] process graceful-restart配置OSPF
1.14 NSR

###### 1. 功能简介

NSR（Nonstop Routing，不间断路由）通过将 OSPF 链路状态信息从主进程备份到备进程，使设备在发生主备倒换时可以自行完成链路状态的恢复和路由的重新生成，邻接关系不会发生中断，从而避免了主备倒换对转发业务的影响。
GR 特性需要周边设备配合才能完成路由信息的恢复，在网络应用中有一定的限制。NSR 特性不需要周边设备的配合，网络应用更加广泛。

##### 2. 配置限制和指导

设备配置了 GR NSR 功能后不能再充当 GR Restarter。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance vpn-instance-name ] *
(3) 使能 OSPF NSR 功能。
non-stop-routing

缺省情况下，OSPF NSR 功能处于关闭状态。
各个进程的 NSR 功能是相互独立的，只对本进程生效。如果存在多个 OSPF 进程，建议在各个进程下使能 功能。
OSPF NSR

#### 1.15 配置OSPF与BFD联动

##### 1.15.1 功能简介

BFD（Bidirectional Detection，双向转发检测）能够为 邻居之间的链路提供快速Forwarding OSPF检测功能。当邻居之间的链路出现故障时，加快 OSPF 协议的收敛速度。关于 BFD 的介绍和基本功能配置，请参见“可靠性配置指导”中的“BFD”。
OSPF 使用 BFD 来进行快速故障检测时，提供两种检测方式：
• control 报文双向检测：需要建立 OSPF 邻居的两端设备均支持 BFD 配置。
• echo 报文单跳检测：仅需要一端设备支持 BFD 配置。

##### 1.15.2 control报文双向检测

进入系统视图。
(1)
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 使能 OSPF 的 BFD 功能。
ospf bfd enable缺省情况下，OSPF 的 BFD 功能处于关闭状态。
创建 BFD 会话的通信双方必须处于特定区域的同一网段。

##### 1.15.3 echo报文单跳检测

进入系统视图。
(1)
system-view配置 报文源地址。
(2) echo bfd echo-source-ip ip-address缺省情况下，未配置 echo 报文源地址。
echo 报文的源 IP 地址用户可以任意指定。建议配置 echo 报文的源 IP 地址不属于该设备任何一个接口所在网段。
本命令的详细情况请参见“可靠性命令参考”中的“BFD”。
进入接口视图。
(3)
interface interface-type interface-number
(4) 使能 OSPF 的 BFD 功能。
ospf bfd enable echo缺省情况下，OSPF 的 BFD 功能处于关闭状态。

#### 1.16 配置OSPF快速重路由

##### 1.16.1 功能简介

当 OSPF 网络中的链路或某台路由器发生故障时，需要通过故障链路或故障路由器传输才能到达目的地的报文将会丢失或产生路由环路，数据流量将会被中断，直到 OSPF 根据新的拓扑网络路由收敛完毕后，被中断的流量才能恢复正常的传输。
为了尽可能缩短网络故障导致的流量中断时间，网络管理员可以根据需要配置 快速重路由功OSPF能。
图1-7 快速重路由功能示意图OSPF如 图 1-7 所示，通过在Router B上使能快速重路由功能，OSPF将为路由计算或指定备份下一跳，当Router B检测到网络故障时，OSPF会使用事先获取的备份下一跳替换失效下一跳，通过备份下一跳来指导报文的转发，从而大大缩短了流量中断时间。在使用备份下一跳指导报文转发的同时，OSPF会根据变化后的网络拓扑重新计算最短路径，网络收敛完毕后，使用新计算出来的最优路由来指导报文转发。
网络管理员可以配置给所有 路由通过 LFA（Loop Alternate）算法选取备份下一跳，也OSPF Free可以在路由策略中指定备份下一跳，为符合过滤条件的路由指定备份下一跳。

##### 1.16.2 配置限制和指导

OSPF 快速重路由功能和 PIC 同时配置时，OSPF 快速重路由功能生效。

##### 1.16.3 配置通过LFA算法选取备份下一跳信息

###### 1. 配置限制和指导

OSPF 快速重路由功能（通过 LFA 算法选取备份下一跳信息）不能与 vlink-peer 命令同时使用。

###### 2. 配置步骤

进入系统视图。
(1)
system-view进入接口视图。
(2)
interface interface-type interface-number
(3) （可选）配置接口参与 LFA 计算。
ospf fast-reroute lfa-backup缺省情况下，接口参与 LFA 计算，能够被选为备份接口。

(4) 退回系统视图。
quit
(5) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
配置 快速重路由功能（通过 算法选取备份下一跳信息）。
(6) OSPF LFA
fast-reroute lfa [ abr-only ]
缺省情况下，OSPF 快速重路由功能处于关闭状态。
abr-only 表示仅选取到 ABR 设备的路由作为备份下一跳。

##### 1.16.4 配置通过路由策略指定备份下一跳

###### 1. 功能简介

网络管理员可以通过 apply fast-reroute backup-interface 命令在路由策略中指定备份下 一 跳 ， 为 符 合 过 滤 条 件 的 路 由 指 定 备 份 下 一 跳 ， 关 于apply fast-reroute backup-interface 命令以及路由策略的相关配置，请参见“三层技术-IP 路由配置指导”中的“路由策略”。

###### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance vpn-instance-name ] *配置 快速重路由功能（通过路由策略指定备份下一跳）。
(3) OSPF fast-reroute route-policy route-policy-name缺省情况下，OSPF 快速重路由功能处于关闭状态。

##### 1.16.5 配置OSPF快速重路由支持BFD检测功能（Ctrl方式）

###### 1. 功能简介

协议的快速重路由特性中，主用链路缺省不使用 进行链路故障检测。配置本功能后，将OSPF BFD使用 BFD 进行检测，可以加快 OSPF 协议的收敛速度。使用 control 报文双向检测方式时，需要建立 OSPF 邻居的两端设备均支持 BFD 配置。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 使能 OSPF 协议中主用链路的 BFD（Ctrl 方式）检测功能。
ospf primary-path-detect bfd ctrl

###### 2. 配置步骤

缺省情况下，OSPF 协议中主用链路的 BFD 检测功能（Ctrl 方式）处于关闭状态。

##### 1.16.6 配置OSPF快速重路由支持BFD检测功能（Echo方式）

###### 1. 功能简介

协议的快速重路由特性中，主用链路缺省不使用 进行链路故障检测。配置本功能后，将OSPF BFD使用 BFD 进行检测，可以加快 OSPF 协议的收敛速度。使用 echo 报文单跳检测方式时，仅需要一端设备支持 BFD 配置。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 配置 BFD Echo 报文源地址。
bfd echo-source-ip ip-address缺省情况下，未配置 BFD Echo 报文源地址。
echo 报文的源 IP 地址用户可以任意指定。建议配置 echo 报文的源 IP 地址不属于该设备任何一个接口所在网段。
本命令的详细情况请参见“可靠性命令参考”中的“BFD”。
(3) 进入接口视图。
interface interface-type interface-number
(4) 使能 OSPF 协议中主用链路的 BFD（Echo 方式）检测功能。
ospf primary-path-detect bfd echo缺省情况下，OSPF 协议中主用链路的 BFD（Echo 方式）检测功能处于关闭状态。

#### 1.17 配置OSPF验证

##### 1.17.1 功能简介

从安全性角度来考虑，为了避免路由信息外泄或者 OSPF 路由器受到恶意攻击，OSPF 提供报文验证功能。
OSPF 路由器建立邻居关系时，在发送的报文中会携带配置好的口令，接收报文时进行验证，只有通过验证的报文才能接收，否则将不会接收报文，不能正常建立邻居。
如果区域验证和接口验证都进行了配置，以接口验证的配置为准。

##### 1.17.2 配置区域验证

(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(3) 进入 OSPF 区域视图。

area area-id
(4) 配置 OSPF 区域的验证模式。请选择其中一项进行配置。
配置 OSPF 区域使用 HMAC-MD5/MD5 验证模式。
(cid:123)
authentication-mode { hmac-md5 | md5 } key-id { cipher | plain } string配置 OSPF 区域使用简单验证模式。
(cid:123)
authentication-mode simple { cipher | plain } string配置 OSPF 区域使用 keychain 验证模式。
(cid:123)
authentication-mode keychain keychain-name关于 keychain 功能的介绍，请参见“安全配置指导”中的“keychain”。
缺省情况下，未配置区域验证模式。
一个区域中所有路由器的验证模式和验证密钥必须一致。

##### 1.17.3 配置接口验证

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置 OSPF 接口的验证模式。请选择其中一项进行配置。
配置 OSPF 区域使用 HMAC-MD5/MD5 验证模式。
(cid:123)
ospf authentication-mode { hmac-md5 | md5 } key-id { cipher | plain }
string
配置 OSPF 区域使用简单验证模式。
(cid:123)
ospf authentication-mode simple { cipher | plain } string
配置 OSPF 区域使用 keychain 验证模式。
(cid:123)
ospf authentication-mode keychain keychain-name
关于 keychain 功能的介绍，请参见“安全配置指导”中的“keychain”。
缺省情况下，接口不对 OSPF 报文进行验证。
邻居路由器两端接口的验证模式和验证密钥必须一致。

#### 1.18 配置OSPF GTSM功能

##### 1.18.1 功能简介

GTSM（Generalized TTL Security Mechanism，通用 TTL 安全保护机制）是一种简单易行的、对基于 IP 协议的上层业务进行保护的安全机制。开启 OSPF 报文的 GTSM 功能后，当设备收到来自普通邻居或虚连接邻居的报文时，会判断报文的 是否在 255-“hop-count”+1 到OSPF TTL 255之间。如果在，就上送报文；如果不在，则直接丢弃报文。以使设备避免受到 CPU 利用（CPU-utilization）等类型的攻击（如 CPU 过载），增强系统的安全性。

开启 GTSM 功能的方式有两种：一种是在 OSPF 区域视图下开启，另一种是在接口视图下开启。
在 区域视图下开启 功能会对该区域中所有使能 的接口生效；接口视图下开启OSPF GTSM OSPF GTSM 功能只对当前接口生效。在接口视图下配置的 hops 参数的优先级高于在 OSPF 区域视图下配置的 hops 参数。

##### 1.18.2 配置限制和指导

开启 OSPF GTSM 功能时，要求本设备和邻居设备上同时配置本特性，指定的 hop-count 值可以不同，只要能够满足合法性检查即可。

##### 1.18.3 配置区域GTSM功能

###### 1. 配置限制和指导

该命令对区域中所有使能 OSPF 的接口都会生效，并且只会对来自 OSPF 普通邻居和虚连接邻居的报文进行安全检测。

###### 2. 配置步骤

进入系统视图。
(1)
system-view进入 视图。
(2) OSPF ospf [ process-id | router-id router-id | vpn-instance vpn-instance-name ] *
(3) 进入 OSPF 区域视图。
area area-id开启区域的 功能。
(4) OSPF GTSM ttl-security [ hops hop-count ]缺省情况下，区域的 功能处于关闭状态。
OSPF GTSM

##### 1.18.4 配置接口GTSM功能

###### 1. 配置限制和指导

该命令只对当前接口生效，并且只会对来自 普通邻居和虚连接邻居的报文进行安全检测。
OSPF

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
配置开启接口的 功能。
(3) OSPF GTSM
ospf ttl-security [ hops hop-count | disable ]
缺省情况下，接口的 功能处于关闭状态。
OSPF GTSM

#### 1.19 配置OSPF日志和告警功能

##### 1.19.1 配置邻居状态变化的输出开关

###### 1. 功能简介

打开邻居状态变化的输出开关后，OSPF 邻居状态变化时会生成日志信息发送到设备的信息中心，通过设置信息中心的参数，最终决定日志信息的输出规则（即是否允许输出以及输出方向）。（有关信息中心参数的配置请参见“网络管理和监控配置指导”中的“信息中心”。）

###### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance vpn-instance-name ] *打开邻居状态变化的输出开关。
(3)
log-peer-change缺省情况下，邻居状态变化的输出开关处于打开状态。

##### 1.19.2 配置OSPF的日志功能

###### 1. 功能简介

的日志信息包括路由计算、邻居、路由、LSA 老化、生成和接收 的日志信息。
OSPF LSA

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPF 视图。
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
(3) 配置 OSPF 的日志信息个数。
event-log { lsa-flush | peer | spf } size count
缺省情况下，路由计算、邻居和 LSA 老化的日志信息个数为 10。

##### 1.19.3 配置OSPF网管功能

###### 1. 功能简介

配置 OSPF 进程绑定 MIB 功能后，可以通过网管软件对指定的 OSPF 进程进行管理。
开启 OSPF 模块的告警功能后，该模块会生成告警信息，用于报告该模块的重要事件。生成的告警信息将发送到设备的 SNMP 模块，通过设置 SNMP 中告警信息的发送参数，来决定告警信息输出的相关属性。（有关告警信息的详细介绍，请参见“网络管理和监控配置指导”中的“SNMP”。）

通过调整 OSPF 在指定时间间隔内允许输出的告警信息条数，可以避免网络出现大量告警信息时对资源的消耗。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置 OSPF 进程绑定公有 MIB。
ospf mib-binding process-id
缺省情况下，MIB 绑定在进程号最小的 OSPF 进程上。
开启 的告警功能。
(3) OSPF
snmp-agent trap enable ospf [ authentication-failure | bad-packet |
config-error | grhelper-status-change | grrestarter-status-change |
if-state-change | lsa-maxage | lsa-originate |
lsdb-approaching-overflow | lsdb-overflow | neighbor-state-change |
nssatranslator-status-change | retransmit |
virt-authentication-failure | virt-bad-packet | virt-config-error |
virt-retransmit | virtgrhelper-status-change | virtif-state-change |
virtneighbor-state-change ] *
缺省情况下，OSPF 的告警功能处于开启状态。
进入 视图。
(4) OSPF
ospf [ process-id | router-id router-id | vpn-instance
vpn-instance-name ] *
配置 在指定时间间隔内允许输出的告警信息条数。
(5) OSPF
snmp trap rate-limit interval trap-interval count trap-number
缺省情况下，OSPF 在 秒内允许输出 条告警信息。
10 7

#### 1.20 OSPF显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 OSPF 的运行情况，通过查看显示信息验证配置的效果。
在用户视图下执行 命令可以清除 的统计信息、重启 进程或重新向 引入reset OSPF OSPF OSPF外部路由。
表1-1 显示和维护OSPF操作 命令display ospf [ process-id ] [ area area-id ] abr-summary显示OSPF的ABR聚合信息[ ip-address { mask-length | mask } ] [ verbose ]显示区域中FRR备份下一跳候 display ospf [ process-id ] [ area area-id ] fast-reroute选列表 lfa-candidate display ospf [ process-id ] [ area area-id ] spf-tree显示OSPF区域中的拓扑信息[ verbose ] display ospf [ process-id ] [ verbose ]显示OSPF的进程信息

操作 命令显示OSPF ABR及ASBR信息 display ospf [ process-id ] abr-asbr [ verbose ] display ospf [ process-id ] asbr-summary [ ip-address显示OSPF的ASBR聚合信息{ mask-length | mask } ]显示OSPF的日志信息 display ospf [ process-id ] event-log { lsa-flush | peer | spf }显示OSPF进程的GR状态信息 display ospf [ process-id ] graceful-restart [ verbose ] display ospf [ process-id ] interface [ interface-type显示OSPF接口信息interface-number | verbose ] display ospf [ process-id ] [ area area-id ] lsdb { asbr | network | nssa | opaque-area | opaque-link | router | summary } [ link-state-id ] [ originate-router advertising-router-id | self-originate ]显示OSPF的LSDB信息 display ospf [ process-id ] lsdb [ brief | originate-router advertising-router-id | self-originate ] display ospf [ process-id ] lsdb { ase | opaque-as ase } [ link-state-id ] [ originate-router advertising-router-id | self-originate ]显示进程中的下一跳信息 display ospf [ process-id ] nexthop显示OSPF的NSR阶段信息 display ospf [ process-id ] non-stop-routing status display ospf [ process-id ] peer [ verbose ] [ interface-type显示OSPF邻居的信息interface-number ] [ neighbor-id ]显示OSPF各区域邻居的统计display ospf [ process-id ] peer statistics信息display ospf [ process-id ] request-queue [ interface-type显示OSPF请求列表interface-number ] [ neighbor-id ] display ospf retrans-queue [ process-id ] [ interface-type显示OSPF重传列表interface-number ] [ neighbor-id ] display ospf [ process-id ] routing [ ip-address { mask-length interface显示OSPF路由表的信息 | mask } ] [ interface-type interface-number ] [ nexthop nexthop-address ] [ verbose ] display ospf [ process-id ] statistics [ error | packet显示OSPF的统计信息[ interface-type interface-number ] ]显示OSPF虚连接信息 display ospf [ process-id ] vlink显示全局Router ID display router id reset ospf [ process-id ] event-log [ lsa-flush | peer | spf ]清除OSPF的日志信息重启OSPF进程 reset ospf [ process-id ] process [ graceful-restart ]重新向OSPF引入外部路由 reset ospf [ process-id ] redistribution清除OSPF的统计信息 reset ospf [ process-id ] statistics

#### 1.21 OSPF典型配置举例

##### 1.21.1 OSPF基本功能配置举例

###### 1. 组网需求

• 所有的交换机都运行 OSPF，并将整个自治系统划分为 3 个区域。
其中 和 作为 来转发区域之间的路由。
• Switch A Switch B ABR
配置完成后，每台交换机都应学到 内的到所有网段的路由。
• AS

###### 2. 组网图

图1-8 OSPF 基本功能配置组网图Switch A Area 0 Switch B Vlan-int100
10.1.1.1/24 Vlan-int100 Vlan-int200 Vlan-int200 10.1.1.2/24
10.3.1.1/24
10.2.1.1/24 Vlan-int200 Area 1 Vlan-int200 Area 2
10.3.1.2/24
10.2.1.2/24 Vlan-int300 Vlan-int300
10.4.1.1/24
10.5.1.1/24 Switch C Switch D

###### 3. 配置步骤

(1) 配置各接口的 IP 地址（略）
(2) 配置 OSPF 基本配置
\# 配置 Switch A。
<SwitchA> system-view
[SwitchA] router id 10.2.1.1
[SwitchA] ospf
[SwitchA-ospf-1] area 0
[SwitchA-ospf-1-area-0.0.0.0] network 10.1.1.0 0.0.0.255
[SwitchA-ospf-1-area-0.0.0.0] quit
[SwitchA-ospf-1] area 1
[SwitchA-ospf-1-area-0.0.0.1] network 10.2.1.0 0.0.0.255
[SwitchA-ospf-1-area-0.0.0.1] quit
[SwitchA-ospf-1] quit
\# 配置 Switch B。
<SwitchB> system-view
[SwitchB] router id 10.3.1.1
[SwitchB] ospf
[SwitchB-ospf-1] area 0
[SwitchB-ospf-1-area-0.0.0.0] network 10.1.1.0 0.0.0.255
[SwitchB-ospf-1-area-0.0.0.0] quit
[SwitchB-ospf-1] area 2

###### 4. 验证配置

[SwitchB-ospf-1-area-0.0.0.2] network 10.3.1.0 0.0.0.255 [SwitchB-ospf-1-area-0.0.0.2] quit [SwitchB-ospf-1] quit \# 配置 Switch C。
<SwitchC> system-view [SwitchC] router id 10.4.1.1 [SwitchC] ospf [SwitchC-ospf-1] area 1 [SwitchC-ospf-1-area-0.0.0.1] network 10.2.1.0 0.0.0.255 [SwitchC-ospf-1-area-0.0.0.1] network 10.4.1.0 0.0.0.255 [SwitchC-ospf-1-area-0.0.0.1] quit [SwitchC-ospf-1] quit配置 D。
\# Switch <SwitchD> system-view [SwitchD] router id 10.5.1.1 [SwitchD] ospf [SwitchD-ospf-1] area 2 [SwitchD-ospf-1-area-0.0.0.2] network 10.3.1.0 0.0.0.255 [SwitchD-ospf-1-area-0.0.0.2] network 10.5.1.0 0.0.0.255 [SwitchD-ospf-1-area-0.0.0.2] quit [SwitchD-ospf-1] quit验证配置
4.
\# 查看 Switch A 的 OSPF 邻居。
[SwitchA] display ospf peer verbose OSPF Process 1 with Router ID 10.2.1.1 Neighbors Area 0.0.0.0 interface 10.1.1.1(Vlan-interface100)'s neighbors Router ID: 10.3.1.1 Address: 10.1.1.2 GR State: Normal State: Full Mode: Nbr is master Priority: 1 DR: 10.1.1.1 BDR: 10.1.1.2 MTU: 0 Options is 0x02 (-|-|-|-|-|-|E|-)
Dead timer due in 37 sec Neighbor is up for 06:03:59 Authentication Sequence: [ 0 ] Neighbor state change count: 5 Area 0.0.0.1 interface 10.2.1.1(Vlan-interface200)'s neighbors Router ID: 10.4.1.1 Address: 10.2.1.2 GR State: Normal State: Full Mode: Nbr is master Priority: 1 DR: 10.2.1.1 BDR: 10.2.1.2 MTU: 0 Options is 0x02 (-|-|-|-|-|-|E|-)
Dead timer due in 32 sec Neighbor is up for 06:03:12 Authentication Sequence: [ 0 ] Neighbor state change count: 5

\# 查看 Switch A 的 OSPF 路由信息。
[SwitchA] display ospf routing OSPF Process 1 with Router ID 10.2.1.1 Routing Table Topology base (MTID 0)
Routing for network Destination Cost Type NextHop AdvRouter Area
10.2.1.0/24 1 Transit 10.2.1.1 10.2.1.1 0.0.0.1
10.3.1.0/24 2 Inter 10.1.1.2 10.3.1.1 0.0.0.0
10.4.1.0/24 2 Stub 10.2.1.2 10.4.1.1 0.0.0.1
10.5.1.0/24 3 Inter 10.1.1.2 10.3.1.1 0.0.0.0
10.1.1.0/24 1 Transit 10.1.1.1 10.2.1.1 0.0.0.0 Total nets: 5 Intra area: 3 Inter area: 2 ASE: 0 NSSA: 0查看 的 路由信息。
\# Switch D OSPF [SwitchD] display ospf routing OSPF Process 1 with Router ID 10.5.1.1 Routing Table Topology base (MTID 0)
Routing for network Destination Cost Type NextHop AdvRouter Area
10.2.1.0/24 3 Inter 10.3.1.1 10.3.1.1 0.0.0.2
10.3.1.0/24 1 Transit 10.3.1.2 10.3.1.1 0.0.0.2
10.4.1.0/24 4 Inter 10.3.1.1 10.3.1.1 0.0.0.2
10.5.1.0/24 1 Stub 10.5.1.1 10.5.1.1 0.0.0.2
10.1.1.0/24 2 Inter 10.3.1.1 10.3.1.1 0.0.0.2 Total nets: 5 Intra area: 2 Inter area: 3 ASE: 0 NSSA: 0 \# 在 Switch D 上使用 Ping 进行测试连通性。
[SwitchD] ping 10.4.1.1 Ping 10.4.1.1 (10.4.1.1): 56 data bytes, press CTRL_C to break 56 bytes from 10.4.1.1: icmp_seq=0 ttl=253 time=1.549 ms 56 bytes from 10.4.1.1: icmp_seq=1 ttl=253 time=1.539 ms 56 bytes from 10.4.1.1: icmp_seq=2 ttl=253 time=0.779 ms 56 bytes from 10.4.1.1: icmp_seq=3 ttl=253 time=1.702 ms 56 bytes from 10.4.1.1: icmp_seq=4 ttl=253 time=1.471 ms
--- Ping statistics for 10.4.1.1 --- 5 packet(s) transmitted, 5 packet(s) received, 0.0% packet loss

###### 1. 组网需求

###### 4. 验证配置

round-trip min/avg/max/std-dev = 0.779/1.408/1.702/0.323 ms

##### 1.21.2 OSPF引入自治系统外部路由配置举例

组网需求
1.
• 所有的交换机都运行 OSPF，整个自治系统划分为 3 个区域。
• 其中 Switch A 和 Switch B 作为 ABR 来转发区域之间的路由。
• 在 Switch C 上配置为 ASBR 引入外部路由（静态路由），且路由信息可正确的在 AS 内传播。

###### 2. 组网图

图1-9 OSPF 引入自治系统外部路由配置组网图

###### 3. 配置步骤

(1) 配置各接口的 IP 地址（略）
(2) 配置OSPF（同前例“1.21.1 OSPF基本功能配置举例”）
(3) 配置引入自治系统外部路由
\# 在 Switch C 上配置一条到目的网段 3.1.2.0/24 的静态路由。
<SwitchC> system-view
[SwitchC] ip route-static 3.1.2.1 24 10.4.1.2
在 上配置 引入静态路由。
\# Switch C OSPF
[SwitchC] ospf 1
[SwitchC-ospf-1] import-route static
验证配置
4.
\# 查看 Switch D 的 ABR/ASBR 信息。
<SwitchD> display ospf abr-asbr
OSPF Process 1 with Router ID 10.5.1.1
Routing Table to ABR and ASBR
Topology base (MTID 0)
Type Destination Area Cost Nexthop RtType
Intra 10.3.1.1 0.0.0.2 10 10.3.1.1 ABR
Inter 10.4.1.1 0.0.0.2 22 10.3.1.1 ASBR

\# 查看 Switch D 的 OSPF 路由表。
<SwitchD> display ospf routing OSPF Process 1 with Router ID 10.5.1.1 Routing Table Topology base (MTID 0)
Routing for network Destination Cost Type NextHop AdvRouter Area
10.2.1.0/24 22 Inter 10.3.1.1 10.3.1.1 0.0.0.2
10.3.1.0/24 10 Transit 10.3.1.2 10.3.1.1 0.0.0.2
10.4.1.0/24 25 Inter 10.3.1.1 10.3.1.1 0.0.0.2
10.5.1.0/24 10 Stub 10.5.1.1 10.5.1.1 0.0.0.2
10.1.1.0/24 12 Inter 10.3.1.1 10.3.1.1 0.0.0.2 Routing for ASEs Destination Cost Type Tag NextHop AdvRouter
3.1.2.0/24 1 Type2 1 10.3.1.1 10.4.1.1 Total nets: 6 Intra area: 2 Inter area: 3 ASE: 1 NSSA: 0

##### 1.21.3 OSPF发布聚合路由配置举例

###### 1. 组网需求

和 位于 内，AS 内使用 作为 协议。
• Switch A Switch B AS 200 200 OSPF IGP Switch C、Switch D 和 Switch E 位于 AS 100 内，AS 100 内使用 OSPF 作为 IGP 协议。
•Switch B 和 Switch C 之间建立 EBGP 连接，配置 BGP 引入 OSPF 和直连路由，配置 OSPF
•进程引入 路由。
BGP为了减小 的路由表规模，在 上配置路由聚合，只发布聚合后的路由
• Switch A Switch B
10.0.0.0/8。

###### 2. 组网图

图1-10 OSPF 发布聚合路由配置组网图Vlan-int600 Vlan-int500
10.4.1.1/24
10.3.1.1/24 Vlan-int400 Vlan-int300
10.1.1.1/24 10.2.1.2/24 Switch E Switch D Vlan-int300 Vlan-int400
10.2.1.1/24
10.1.1.2/24 Switch C AS 100 Vlan-int200
11.1.1.2/24 EBGP Vlan-int200
11.1.1.1/24 Switch B Vlan-int100
11.2.1.1/24 Vlan-int100
11.2.1.2/24 AS 200 Switch A

###### 3. 配置步骤

(1) 配置接口的 IP 地址（略）
(2) 配置 OSPF
配置 A。
\# Switch
<SwitchA> system-view
[SwitchA] router id 11.2.1.2
[SwitchA] ospf
[SwitchA-ospf-1] area 0
[SwitchA-ospf-1-area-0.0.0.0] network 11.2.1.0 0.0.0.255
[SwitchA-ospf-1-area-0.0.0.0] quit
[SwitchA-ospf-1] quit
\# 配置 Switch B。
<SwitchB> system-view
[SwitchB] router id 11.2.1.1
[SwitchB] ospf
[SwitchB-ospf-1] area 0
[SwitchB-ospf-1-area-0.0.0.0] network 11.2.1.0 0.0.0.255
[SwitchB-ospf-1-area-0.0.0.0] quit
[SwitchB-ospf-1] quit
\# 配置 Switch C。
<SwitchC> system-view
[SwitchC] router id 11.1.1.2
[SwitchC] ospf
[SwitchC-ospf-1] area 0
[SwitchC-ospf-1-area-0.0.0.0] network 10.1.1.0 0.0.0.255

[SwitchC-ospf-1-area-0.0.0.0] network 10.2.1.0 0.0.0.255 [SwitchC-ospf-1-area-0.0.0.0] quit [SwitchC-ospf-1] quit \# 配置 Switch D。
<SwitchD> system-view [SwitchD] router id 10.3.1.1 [SwitchD] ospf [SwitchD-ospf-1] area 0 [SwitchD-ospf-1-area-0.0.0.0] network 10.1.1.0 0.0.0.255 [SwitchD-ospf-1-area-0.0.0.0] network 10.3.1.0 0.0.0.255 [SwitchD-ospf-1-area-0.0.0.0] quit [SwitchD-ospf-1] quit配置 E。
\# Switch <SwitchE> system-view [SwitchE] router id 10.4.1.1 [SwitchE] ospf [SwitchE-ospf-1] area 0 [SwitchE-ospf-1-area-0.0.0.0] network 10.2.1.0 0.0.0.255 [SwitchE-ospf-1-area-0.0.0.0] network 10.4.1.0 0.0.0.255 [SwitchE-ospf-1-area-0.0.0.0] quit [SwitchE-ospf-1] quit
(3) 配置 BGP，引入 OSPF 和直连路由\# 配置 Switch B。
[SwitchB] bgp 200 [SwitchB-bgp-default] peer 11.1.1.2 as 100 [SwitchB-bgp-default] address-family ipv4 unicast [SwitchB-bgp-default-ipv4] peer 11.1.1.2 enable [SwitchB-bgp-default-ipv4] import-route ospf [SwitchB-bgp-default-ipv4] import-route direct [SwitchB-bgp-default-ipv4] quit [SwitchB-bgp-default] quit \# 配置 Switch C。
[SwitchC] bgp 100 [SwitchC-bgp-default] peer 11.1.1.1 as 200 [SwitchC-bgp-default] address-family ipv4 unicast [SwitchC-bgp-default] peer 11.1.1.1 enable [SwitchC-bgp-default-ipv4] import-route ospf [SwitchC-bgp-default-ipv4] import-route direct [SwitchC-bgp-default-ipv4] quit [SwitchC-bgp-default] quit在 和 上配置 引入 路由
(4) Switch B Switch C OSPF BGP \# 在 Switch B 上配置 OSPF 引入 BGP 路由。
[SwitchB] ospf [SwitchB-ospf-1] import-route bgp \# 在 Switch C 上配置 OSPF 引入 BGP 路由。
[SwitchC] ospf

[SwitchC-ospf-1] import-route bgp \# 查看 SwitchA 的路由表信息。
[SwitchA] display ip routing-table Destinations : 16 Routes : 16 Destination/Mask Proto Pre Cost NextHop Interface
0.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
10.1.1.0/24 O_ASE2 150 1 11.2.1.1 Vlan100
10.2.1.0/24 O_ASE2 150 1 11.2.1.1 Vlan100
10.3.1.0/24 O_ASE2 150 1 11.2.1.1 Vlan100
10.4.1.0/24 O_ASE2 150 1 11.2.1.1 Vlan100
11.2.1.0/24 Direct 0 0 11.2.1.2 Vlan100
11.2.1.0/32 Direct 0 0 11.2.1.2 Vlan100
11.2.1.2/32 Direct 0 0 127.0.0.1 InLoop0
11.2.1.255/32 Direct 0 0 11.2.1.2 Vlan100
127.0.0.0/8 Direct 0 0 127.0.0.1 InLoop0
127.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
127.0.0.1/32 Direct 0 0 127.0.0.1 InLoop0
127.255.255.255/32 Direct 0 0 127.0.0.1 InLoop0
224.0.0.0/4 Direct 0 0 0.0.0.0 NULL0
224.0.0.0/24 Direct 0 0 0.0.0.0 NULL0
255.255.255.255/32 Direct 0 0 127.0.0.1 InLoop0在 上配置路由聚合，只发布聚合路由 10.0.0.0/8。
(5) Switch B [SwitchB-ospf-1] asbr-summary 10.0.0.0 8 \# 查看 Switch A 的路由表信息。
[SwitchA] display ip routing-table Destinations : 13 Routes : 13 Destination/Mask Proto Pre Cost NextHop Interface
0.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
10.0.0.0/8 O_ASE2 150 2 11.2.1.1 Vlan100
11.2.1.0/24 Direct 0 0 11.2.1.2 Vlan100
11.2.1.0/32 Direct 0 0 11.2.1.2 Vlan100
11.2.1.2/32 Direct 0 0 127.0.0.1 InLoop0
11.2.1.255/32 Direct 0 0 11.2.1.2 Vlan100
127.0.0.0/8 Direct 0 0 127.0.0.1 InLoop0
127.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
127.0.0.1/32 Direct 0 0 127.0.0.1 InLoop0
127.255.255.255/32 Direct 0 0 127.0.0.1 InLoop0
224.0.0.0/4 Direct 0 0 0.0.0.0 NULL0
224.0.0.0/24 Direct 0 0 0.0.0.0 NULL0
255.255.255.255/32 Direct 0 0 127.0.0.1 InLoop0可以看出，路由 10.1.1.0/24、10.2.1.0/24、10.3.1.0/24、10.4.1.0/24 已经聚合为一条路由
10.0.0.0/8。

###### 1. 组网需求

##### 1.21.4 OSPF Stub区域配置举例

组网需求
1.
• 所有的交换机都运行 OSPF，整个自治系统划分为 3 个区域。
• 其中 Switch A 和 Switch B 作为 ABR 来转发区域之间的路由，Switch D 作为 ASBR 引入了外部路由（静态路由）。
要求将 Area1 配置为 Stub 区域，减少通告到此区域内的 LSA 数量，但不影响路由的可达性。
•

###### 2. 组网图

图1-11 区域配置组网图OSPF Stub Switch A Area 0 Switch B Vlan-int100
10.1.1.1/24 Vlan-int100 Vlan-int200 10.1.1.2/24 Vlan-int200
10.2.1.1/24 10.3.1.1/24 Vlan-int200 Vlan-int200 Area 1 Area 2
10.3.1.2/24
10.2.1.2/24 Stub ASBR Vlan-int300 Vlan-int300
10.4.1.1/24 Switch C 10.5.1.1/24 Switch D

###### 3. 配置步骤

配置接口的 地址（略）
(1) IP配置OSPF（同前例“1.21.1 OSPF基本功能配置举例”）
(2)
配置 引入静态路由
(3) Switch D <SwitchD> system-view [SwitchD] ip route-static 3.1.2.1 24 10.5.1.2 [SwitchD] ospf [SwitchD-ospf-1] import-route static [SwitchD-ospf-1] quit \# 查看 Switch C 的 ABR/ASBR 信息。
<SwitchC> display ospf abr-asbr OSPF Process 1 with Router ID 10.4.1.1 Routing Table to ABR and ASBR Topology base (MTID 0)
Type Destination Area Cost Nexthop RtType Intra 10.2.1.1 0.0.0.1 3 10.2.1.1 ABR Inter 10.5.1.1 0.0.0.1 7 10.2.1.1 ASBR查看 的 路由表，可以看到路由表中存在 外部的路由。
\# Switch C OSPF AS <SwitchC> display ospf routing

OSPF Process 1 with Router ID 10.4.1.1 Routing Table Topology base (MTID 0)
Routing for network Destination Cost Type NextHop AdvRouter Area
10.2.1.0/24 3 Transit 0.0.0.0 10.2.1.1 0.0.0.1
10.3.1.0/24 7 Inter 10.2.1.1 10.2.1.1 0.0.0.1
10.4.1.0/24 3 Stub 10.4.1.1 10.4.1.1 0.0.0.1
10.5.1.0/24 17 Inter 10.2.1.1 10.2.1.1 0.0.0.1
10.1.1.0/24 5 Inter 10.2.1.1 10.2.1.1 0.0.0.1 Routing for ASEs Destination Cost Type Tag NextHop AdvRouter
3.1.2.0/24 1 Type2 1 10.2.1.1 10.5.1.1 Total nets: 6 Intra area: 2 Inter area: 3 ASE: 1 NSSA: 0
(4) 配置 Area1 为 Stub 区域\# 配置 Switch A。
<SwitchA> system-view [SwitchA] ospf [SwitchA-ospf-1] area 1 [SwitchA-ospf-1-area-0.0.0.1] stub [SwitchA-ospf-1-area-0.0.0.1] quit [SwitchA-ospf-1] quit \# 配置 Switch C。
<SwitchC> system-view [SwitchC] ospf [SwitchC-ospf-1] area 1 [SwitchC-ospf-1-area-0.0.0.1] stub [SwitchC-ospf-1-area-0.0.0.1] quit [SwitchC-ospf-1] quit \# 查看Switch C的OSPF路由表，已经看不到AS外部的路由，取而代之的是一条缺省路由。
[SwitchC] display ospf routing OSPF Process 1 with Router ID 10.4.1.1 Routing Table Topology base (MTID 0)
Routing for network Destination Cost Type NextHop AdvRouter Area
0.0.0.0/0 4 Inter 10.2.1.1 10.2.1.1 0.0.0.1
10.2.1.0/24 3 Transit 0.0.0.0 10.2.1.1 0.0.0.1
10.3.1.0/24 7 Inter 10.2.1.1 10.2.1.1 0.0.0.1

10.4.1.0/24 3 Stub 10.4.1.1 10.4.1.1 0.0.0.1
10.5.1.0/24 17 Inter 10.2.1.1 10.2.1.1 0.0.0.1
10.1.1.0/24 5 Inter 10.2.1.1 10.2.1.1 0.0.0.1
Total nets: 6
Intra area: 2 Inter area: 4 ASE: 0 NSSA: 0
\# 配置 Area1 为 Totally Stub 区域。
[SwitchA] ospf
[SwitchA-ospf-1] area 1
[SwitchA-ospf-1-area-0.0.0.1] stub no-summary
[SwitchA-ospf-1-area-0.0.0.1] quit
[SwitchA-ospf-1] quit
查看 的 路由表，可以看到路由表项进一步减少，只保留了一条通往区域外
\# Switch C OSPF
部的缺省路由。
[SwitchC] display ospf routing
OSPF Process 1 with Router ID 10.4.1.1
Routing Table
Topology base (MTID 0)
Routing for network
Destination Cost Type NextHop AdvRouter Area
0.0.0.0/0 4 Inter 10.2.1.1 10.2.1.1 0.0.0.1
10.2.1.0/24 3 Transit 0.0.0.0 10.4.1.1 0.0.0.1
10.4.1.0/24 3 Stub 10.4.1.1 10.4.1.1 0.0.0.1
Total nets: 3
Intra area: 2 Inter area: 1 ASE: 0 NSSA: 0

##### 1.21.5 OSPF NSSA区域配置举例

###### 1. 组网需求

• 所有的交换机都运行 OSPF，整个自治系统划分为 3 个区域。
• 其中 Switch A 和 Switch B 作为 ABR 来转发区域之间的路由。
• 要求将 Area1 配置为 NSSA 区域，同时将 Switch C 配置为 ASBR 引入外部路由（静态路由），
且路由信息可正确的在 AS 内传播。

###### 3. 配置步骤

###### 2. 组网图

图1-12 OSPF NSSA 区域配置组网图配置步骤
3.
(1) 配置各接口的 IP 地址（略）
(2) 配置OSPF（同前例“1.21.1 OSPF基本功能配置举例”）
(3) 配置 Area1 区域为 NSSA 区域\# 配置 Switch A。
<SwitchA> system-view [SwitchA] ospf [SwitchA-ospf-1] area 1 [SwitchA-ospf-1-area-0.0.0.1] nssa [SwitchA-ospf-1-area-0.0.0.0] quit [SwitchA-ospf-1] quit \# 配置 Switch C。
<SwitchC> system-view [SwitchC] ospf [SwitchC-ospf-1] area 1 [SwitchC-ospf-1-area-0.0.0.1] nssa [SwitchC-ospf-1-area-0.0.0.1] quit [SwitchC-ospf-1] quit \# 查看 Switch C 的 OSPF 路由表。
[SwitchC] display ospf routing OSPF Process 1 with Router ID 10.4.1.1 Routing Table Topology base (MTID 0)
Routing for network Destination Cost Type NextHop AdvRouter Area
10.2.1.0/24 3 Transit 10.2.1.2 10.4.1.1 0.0.0.1
10.3.1.0/24 7 Inter 10.2.1.1 10.2.1.1 0.0.0.1
10.4.1.0/24 3 Stub 10.4.1.1 10.4.1.1 0.0.0.1

10.5.1.0/24 17 Inter 10.2.1.1 10.2.1.1 0.0.0.1
10.1.1.0/24 5 Inter 10.2.1.1 10.2.1.1 0.0.0.1
Total nets: 5
Intra area: 2 Inter area: 3 ASE: 0 NSSA: 0
(4) 配置 Switch C 引入静态路由
[SwitchC] ip route-static 3.1.3.1 24 10.4.1.2
[SwitchC] ospf
[SwitchC-ospf-1] import-route static
[SwitchC-ospf-1] quit
\# 查看 Switch D 的 OSPF 路由表，可以看到 NSSA 区域引入了一条 AS 外部路由。
<SwitchD> display ospf routing
Topology base (MTID 0)
OSPF Process 1 with Router ID 10.5.1.1
Routing Table
Routing for network
Destination Cost Type NextHop AdvRouter Area
10.2.1.0/24 22 Inter 10.3.1.1 10.3.1.1 0.0.0.2
10.3.1.0/24 10 Transit 10.3.1.2 10.3.1.1 0.0.0.2
10.4.1.0/24 25 Inter 10.3.1.1 10.3.1.1 0.0.0.2
10.5.1.0/24 10 Stub 10.5.1.1 10.5.1.1 0.0.0.2
10.1.1.0/24 12 Inter 10.3.1.1 10.3.1.1 0.0.0.2
Routing for ASEs
Destination Cost Type Tag NextHop AdvRouter
3.1.3.0/24 1 Type2 1 10.3.1.1 10.2.1.1
Total nets: 6
Intra area: 2 Inter area: 3 ASE: 1 NSSA: 0

##### 1.21.6 OSPF的DR选择配置举例

###### 1. 组网需求

Switch A、Switch B、Switch C、Switch D 在同一网段，运行 OSPF 协议；
•配置 Switch A 为 DR，Switch C 为 BDR。
•

图1-13 OSPF 的 DR 选择配置组网图Switch A Switch B Vlan-int1 Vlan-int1
192.168.1.1/24 192.168.1.2/24 Vlan-int1 Vlan-int1
192.168.1.3/24 192.168.1.4/24 Switch C Switch D

###### 2. 配置思路

配置各接口的 地址
(1) IP
(2) 配置 OSPF 基本功能
(3) 改变交换机接口的路由器优先级使 Switch A 成为 DR，Switch C 成为 BDR。

###### 3. 配置步骤

配置各接口的 地址（略）
(1) IP配置 基本功能
(2) OSPF配置 A。
\# Switch <SwitchA> system-view [SwitchA] router id 1.1.1.1 [SwitchA] ospf [SwitchA-ospf-1] area 0 [SwitchA-ospf-1-area-0.0.0.0] network 192.168.1.0 0.0.0.255 [SwitchA-ospf-1-area-0.0.0.0] quit [SwitchA-ospf-1] quit \# 配置 Switch B。
<SwitchB> system-view [SwitchB] router id 2.2.2.2 [SwitchB] ospf [SwitchB-ospf-1] area 0 [SwitchB-ospf-1-area-0.0.0.0] network 192.168.1.0 0.0.0.255 [SwitchB-ospf-1-area-0.0.0.0] quit [SwitchB-ospf-1] quit \# 配置 Switch C。
<SwitchC> system-view [SwitchC] router id 3.3.3.3 [SwitchC] ospf [SwitchC-ospf-1] area 0 [SwitchC-ospf-1-area-0.0.0.0] network 192.168.1.0 0.0.0.255 [SwitchC-ospf-1-area-0.0.0.0] quit [SwitchC-ospf-1] quit

\# 配置 Switch D。
<SwitchD> system-view [SwitchD] router id 4.4.4.4 [SwitchD] ospf [SwitchD-ospf-1] area 0 [SwitchD-ospf-1-area-0.0.0.0] network 192.168.1.0 0.0.0.255 [SwitchD-ospf-1-area-0.0.0.0] quit [SwitchD-ospf-1] quit \# 查看 Switch A 的邻居信息。
[SwitchA] display ospf peer verbose OSPF Process 1 with Router ID 1.1.1.1 Neighbors Area 0.0.0.0 interface 192.168.1.1(Vlan-interface1)'s neighbors Router ID: 2.2.2.2 Address: 192.168.1.2 GR State: Normal State: 2-Way Mode: None Priority: 1 DR: 192.168.1.4 BDR: 192.168.1.3 MTU: 0 Options is 0x02 (-|-|-|-|-|-|E|-)
Dead timer due in 38 sec Neighbor is up for 00:01:31 Authentication Sequence: [ 0 ] Neighbor state change count: 6 BFD status: Disabled Router ID: 3.3.3.3 Address: 192.168.1.3 GR State: Normal State: Full Mode: Nbr is master Priority: 1 DR: 192.168.1.4 BDR: 192.168.1.3 MTU: 0 Options is 0x02 (-|-|-|-|-|-|E|-)
Dead timer due in 31 sec Neighbor is up for 00:01:28 Authentication Sequence: [ 0 ] Neighbor state change count: 6 BFD status: Disabled Router ID: 4.4.4.4 Address: 192.168.1.4 GR State: Normal State: Full Mode: Nbr is master Priority: 1 DR: 192.168.1.4 BDR: 192.168.1.3 MTU: 0 Options is 0x02 (-|-|-|-|-|-|E|-)
Dead timer due in 31 sec Neighbor is up for 00:01:28 Authentication Sequence: [ 0 ] Neighbor state change count: 6 BFD status: Disabled可以看到 Switch D 为 DR，Switch C 为 BDR。
(3) 配置接口上的路由器优先级\# 配置 Switch A。

[SwitchA] interface vlan-interface 1 [SwitchA-Vlan-interface1] ospf dr-priority 100 [SwitchA-Vlan-interface1] quit \# 配置 Switch B。
[SwitchB] interface vlan-interface 1 [SwitchB-Vlan-interface1] ospf dr-priority 0 [SwitchB-Vlan-interface1] quit \# 配置 Switch C。
[SwitchC] interface vlan-interface 1 [SwitchC-Vlan-interface1] ospf dr-priority 2 [SwitchC-Vlan-interface1] quit \# 查看 Switch D 的邻居信息。
<SwitchD> display ospf peer verbose OSPF Process 1 with Router ID 4.4.4.4 Neighbors Area 0.0.0.0 interface 192.168.1.4(Vlan-interface1)'s neighbors Router ID: 1.1.1.1 Address: 192.168.1.1 GR State: Normal State: Full Mode:Nbr is slave Priority: 100 DR: 192.168.1.4 BDR: 192.168.1.3 MTU: 0 Options is 0x02 (-|-|-|-|-|-|E|-)
Dead timer due in 31 sec Neighbor is up for 00:11:17 Authentication Sequence: [ 0 ] Neighbor state change count: 6 BFD status: Disabled Router ID: 2.2.2.2 Address: 192.168.1.2 GR State: Normal State: Full Mode:Nbr is slave Priority: 0 DR: 192.168.1.4 BDR: 192.168.1.3 MTU: 0 Options is 0x02 (-|-|-|-|-|-|E|-)
Dead timer due in 35 sec Neighbor is up for 00:11:19 Authentication Sequence: [ 0 ] Neighbor state change count: 6 BFD status: Disabled Router ID: 3.3.3.3 Address: 192.168.1.3 GR State: Normal State: Full Mode:Nbr is slave Priority: 2 DR: 192.168.1.4 BDR: 192.168.1.3 MTU: 0 Options is 0x02 (-|-|-|-|-|-|E|-)
Dead timer due in 33 sec Neighbor is up for 00:11:15 Authentication Sequence: [ 0 ] Neighbor state change count: 6 BFD status: Disabled

可以看到，网络中 DR/BDR 并没有改变。
网络中 DR/BDR 已经存在的情况下，接口上的路由器优先级的配置并不会立即生效。
(4) 重启 OSPF 进程\# 重启 Switch D 的进程。
<SwitchD> reset ospf 1 process Warning : Reset OSPF process? [Y/N]:y \# 查看 Switch D 的邻居信息。
<SwitchD> display ospf peer verbose OSPF Process 1 with Router ID 4.4.4.4 Neighbors Area 0.0.0.0 interface 192.168.1.4(Vlan-interface1)'s neighbors Router ID: 1.1.1.1 Address: 192.168.1.1 GR State: Normal State: Full Mode: Nbr is slave Priority: 100 DR: 192.168.1.1 BDR: 192.168.1.3 MTU: 0 Options is 0x02 (-|-|-|-|-|-|E|-)
Dead timer due in 39 sec Neighbor is up for 00:01:40 Authentication Sequence: [ 0 ] Neighbor state change count: 6 BFD status: Disabled Router ID: 2.2.2.2 Address: 192.168.1.2 GR State: Normal State: 2-Way Mode: None Priority: 0 DR: 192.168.1.1 BDR: 192.168.1.3 MTU: 0 Options is 0x02 (-|-|-|-|-|-|E|-)
Dead timer due in 35 sec Neighbor is up for 00:01:44 Authentication Sequence: [ 0 ] Neighbor state change count: 6 BFD status: Disabled Router ID: 3.3.3.3 Address: 192.168.1.3 GR State: Normal State: Full Mode: Nbr is slave Priority: 2 DR: 192.168.1.1 BDR: 192.168.1.3 MTU: 0 Options is 0x02 (-|-|-|-|-|-|E|-)
Dead timer due in 39 sec Neighbor is up for 00:01:41 Authentication Sequence: [ 0 ] Neighbor state change count: 6 BFD status: Disabled

可以看到 Switch A 成为 DR，Switch C 为 BDR。
• 如果邻居的状态是 Full，这说明它和邻居之间形成了邻接关系；
• 如果邻居的状态是 2-Way，则说明它们都不是 DR 或 BDR，两者之间不需要交换 LSA。
\# 查看 OSPF 接口的状态。
[SwitchA] display ospf interface OSPF Process 1 with Router ID 1.1.1.1 Interfaces Area: 0.0.0.0 IP Address Type State Cost Pri DR BDR
192.168.1.1 Broadcast DR 1 100 192.168.1.1 192.168.1.3 [SwitchB] display ospf interface OSPF Process 1 with Router ID 2.2.2.2 Interfaces Area: 0.0.0.0 IP Address Type State Cost Pri DR BDR
192.168.1.2 Broadcast DROther 1 0 192.168.1.1 192.168.1.3如果 OSPF 接口的状态是 DROther，则说明它既不是 DR，也不是 BDR。

##### 1.21.7 OSPF虚连接配置举例

###### 1. 组网需求

与 没有直接相连。Area 被用作传输区域（Transit Area）来连接 和
• Area 2 Area 0 1 Area 2 Area 0。Switch B 和 Switch C 之间配置一条虚连接。
• 配置完成后，Switch B 能够学到 Area 2 中的路由。

###### 2. 组网图

图1-14 OSPF 虚链路配置组网图

###### 3. 配置步骤

(1) 配置各接口的 IP 地址（略）
(2) 配置 OSPF 基本功能
\# 配置 Switch A。
<SwitchA> system-view
[SwitchA] ospf 1 router-id 1.1.1.1
[SwitchA-ospf-1] area 0
[SwitchA-ospf-1-area-0.0.0.0] network 10.1.1.0 0.0.0.255
[SwitchA-ospf-1-area-0.0.0.0] quit
[SwitchA-ospf-1] quit
配置 B。
\# Switch
<SwitchB> system-view
[SwitchB] ospf 1 router-id 2.2.2.2
[SwitchB-ospf-1] area 0
[SwitchB-ospf-1-area-0.0.0.0] network 10.1.1.0 0.0.0.255
[SwitchB-ospf-1-area-0.0.0.0] quit
[SwitchB-ospf-1] area 1
[SwitchB–ospf-1-area-0.0.0.1] network 10.2.1.0 0.0.0.255
[SwitchB–ospf-1-area-0.0.0.1] quit
[SwitchB-ospf-1] quit
配置 C。
\# Switch
<SwitchC> system-view
[SwitchC] ospf 1 router-id 3.3.3.3
[SwitchC-ospf-1] area 1
[SwitchC-ospf-1-area-0.0.0.1] network 10.2.1.0 0.0.0.255
[SwitchC-ospf-1-area-0.0.0.1] quit
[SwitchC-ospf-1] area 2
[SwitchC–ospf-1-area-0.0.0.2] network 10.3.1.0 0.0.0.255
[SwitchC–ospf-1-area-0.0.0.2] quit
[SwitchC-ospf-1] quit
配置 D。
\# Switch
<SwitchD> system-view

[SwitchD] ospf 1 router-id 4.4.4.4 [SwitchD-ospf-1] area 2 [SwitchD-ospf-1-area-0.0.0.2] network 10.3.1.0 0.0.0.255 [SwitchD-ospf-1-area-0.0.0.2] quit [SwitchD-ospf-1] quit \# 查看 Switch B 的 OSPF 路由表。
[SwitchB] display ospf routing OSPF Process 1 with Router ID 2.2.2.2 Routing Table Topology base (MTID 0)
Routing for network Destination Cost Type NextHop AdvRouter Area
10.2.1.0/24 2 Transit 10.2.1.1 3.3.3.3 0.0.0.1
10.1.1.0/24 2 Transit 10.1.1.2 2.2.2.2 0.0.0.0 Total nets: 2 Intra area: 2 Inter area: 0 ASE: 0 NSSA: 0由于 Area 0 没有与 Area 2 直接相连，所以 Switch B 的路由表中没有 Area 2 的路由。
(3) 配置虚连接\# 配置 Switch B。
[SwitchB] ospf [SwitchB-ospf-1] area 1 [SwitchB-ospf-1-area-0.0.0.1] vlink-peer 3.3.3.3 [SwitchB-ospf-1-area-0.0.0.1] quit [SwitchB-ospf-1] quit \# 配置 Switch C。
[SwitchC] ospf 1 [SwitchC-ospf-1] area 1 [SwitchC-ospf-1-area-0.0.0.1] vlink-peer 2.2.2.2 [SwitchC-ospf-1-area-0.0.0.1] quit [SwitchC-ospf-1] quit \# 查看 Switch B 的 OSPF 路由表。
[SwitchB] display ospf routing OSPF Process 1 with Router ID 2.2.2.2 Routing Table Topology base (MTID 0)
Routing for network

###### 1. 组网需求

Destination Cost Type NextHop AdvRouter Area
10.2.1.0/24 2 Transit 10.2.1.1 3.3.3.3 0.0.0.1
10.3.1.0/24 5 Inter 10.2.1.2 3.3.3.3 0.0.0.0
10.1.1.0/24 2 Transit 10.1.1.2 2.2.2.2 0.0.0.0 Total nets: 3 Intra area: 2 Inter area: 1 ASE: 0 NSSA: 0可以看到，Switch B 已经学到了 Area 2 的路由 10.3.1.0/24。

##### 1.21.8 OSPF GR配置举例

组网需求
1.
• Switch A、Switch B 和 Switch C 既属于同一自治系统，也属于同一 OSPF 域，通过 OSPF 协议实现网络互连，并提供 GR 机制。
Switch A 作为非 IETF 标准 GR Restarter，Switch B 和 Switch C 作为 GR Helper 并且通过
•机制与 保持带外同步。
GR Switch A

###### 2. 组网图

图1-15 OSPF GR 配置组网图Router ID: 1.1.1.1 GR restarter Switch A Vlan-int100
192.1.1.1/24 Vlan-int100 Vlan-int100
192.1.1.2/24 192.1.1.3/24 Switch B Switch C GR helper GR helper Router ID: 3.3.3.3 Router ID: 2.2.2.2

###### 3. 配置步骤

(1) 配置各接口的 IP 地址（略）
(2) 配置 OSPF 基本功能
\# 配置 Switch A。
<SwitchA> system-view
[SwitchA] router id 1.1.1.1
[SwitchA] ospf 100
[SwitchA-ospf-100] area 0
[SwitchA-ospf-100-area-0.0.0.0] network 192.1.1.0 0.0.0.255
[SwitchA-ospf-100-area-0.0.0.0] quit
[SwitchA-ospf-1] quit
配置 B。
\# Switch
<SwitchB> system-view
[SwitchB] router id 2.2.2.2
[SwitchB] ospf 100

[SwitchB-ospf-100] area 0 [SwitchB-ospf-100-area-0.0.0.0] network 192.1.1.0 0.0.0.255 [SwitchB-ospf-100-area-0.0.0.0] quit [SwitchB-ospf-1] quit \# 配置 Switch C。
<SwitchC> system-view [SwitchC] router id 3.3.3.3 [SwitchC] ospf 100 [SwitchC-ospf-100] area 0 [SwitchC-ospf-100-area-0.0.0.0] network 192.1.1.0 0.0.0.255 [SwitchC-ospf-100-area-0.0.0.0] quit [SwitchC-ospf-1] quit配置
(3) OSPF GR配置 作为非 标准 Restarter，即使能 进程 的本地链路信令能\# Switch A IETF GR OSPF 100力、OSPF 带外同步能力和非 IETF 标准 GR 能力。
[SwitchA-ospf-100] enable link-local-signaling [SwitchA-ospf-100] enable out-of-band-resynchronization [SwitchA-ospf-100] graceful-restart [SwitchA-ospf-100] quit配置 作为 Helper，即使能 进程 的本地链路信令能力和 带外\# Switch B GR OSPF 100 OSPF同步能力。
[SwitchB-ospf-100] enable link-local-signaling [SwitchB-ospf-100] enable out-of-band-resynchronization \# 配置 Switch C 作为 GR Helper，即使能 OSPF 进程 100 的本地链路信令能力和 OSPF 带外同步能力。
[SwitchC-ospf-100] enable link-local-signaling [SwitchC-ospf-100] enable out-of-band-resynchronization

###### 4. 验证配置

\# 打开 Switch A 的 OSPF 平滑启动事件调试信息开关。在 Switch A 上以 GR 方式重启 OSPF 进程。
<SwitchA> debugging ospf event graceful-restart <SwitchA> terminal monitor <SwitchA> terminal logging level 7 <SwitchA> reset ospf 100 process graceful-restart Reset OSPF process? [Y/N]:y %Oct 21 15:29:28:727 2011 SwitchA OSPF/5/OSPF_NBR_CHG: OSPF 100 Neighbor
192.1.1.2(Vlan-interface100) from Full to Down.
%Oct 21 15:29:28:729 2011 SwitchA OSPF/5/OSPF_NBR_CHG: OSPF 100 Neighbor
192.1.1.3(Vlan-interface100) from Full to Down.
*Oct 21 15:29:28:735 2011 SwitchA OSPF/7/DEBUG:
OSPF 100 nonstandard GR Started for OSPF Router
*Oct 21 15:29:28:735 2011 SwitchA OSPF/7/DEBUG:
OSPF 100 created GR wait timer,timeout interval is 40(s).
*Oct 21 15:29:28:735 2011 SwitchA OSPF/7/DEBUG:
OSPF 100 created GR Interval timer,timeout interval is 120(s).
*Oct 21 15:29:28:758 2011 SwitchA OSPF/7/DEBUG:
OSPF 100 created OOB Progress timer for neighbor 192.1.1.3.

###### 2. 组网图

*Oct 21 15:29:28:766 2011 SwitchA OSPF/7/DEBUG:
OSPF 100 created OOB Progress timer for neighbor 192.1.1.2.
%Oct 21 15:29:29:902 2011 SwitchA OSPF/5/OSPF_NBR_CHG: OSPF 100 Neighbor
192.1.1.2(Vlan-interface100) from Loading to Full.
*Oct 21 15:29:29:902 2011 SwitchA OSPF/7/DEBUG:
OSPF 100 deleted OOB Progress timer for neighbor 192.1.1.2.
%Oct 21 15:29:30:897 2011 SwitchA OSPF/5/OSPF_NBR_CHG: OSPF 100 Neighbor
192.1.1.3(Vlan-interface100) from Loading to Full.
*Oct 21 15:29:30:897 2011 SwitchA OSPF/7/DEBUG:
OSPF 100 deleted OOB Progress timer for neighbor 192.1.1.3.
*Oct 21 15:29:30:911 2011 SwitchA OSPF/7/DEBUG:
OSPF GR: Process 100 Exit Restart,Reason : DR or BDR change,for neighbor : 192.1.1.3.
*Oct 21 15:29:30:911 2011 SwitchA OSPF/7/DEBUG:
OSPF 100 deleted GR Interval timer.
*Oct 21 15:29:30:912 2011 SwitchA OSPF/7/DEBUG:
OSPF 100 deleted GR wait timer.
%Oct 21 15:29:30:920 2011 SwitchA OSPF/5/OSPF_NBR_CHG: OSPF 100 Neighbor
192.1.1.2(Vlan-interface100) from Full to Down.
%Oct 21 15:29:30:921 2011 SwitchA OSPF/5/OSPF_NBR_CHG: OSPF 100 Neighbor
192.1.1.3(Vlan-interface100) from Full to Down.
%Oct 21 15:29:33:815 2011 SwitchA OSPF/5/OSPF_NBR_CHG: OSPF 100 Neighbor
192.1.1.3(Vlan-interface100) from Loading to Full.
%Oct 21 15:29:35:578 2011 SwitchA OSPF/5/OSPF_NBR_CHG: OSPF 100 Neighbor
192.1.1.2(Vlan-interface100) from Loading to Full.
从上面的信息可以看出 Switch A 完成了 GR。

##### 1.21.9 OSPF NSR配置举例

###### 1. 组网需求

S、Switch A、Switch 属于同一 区域，通过 协议实现网络互连。要求对
Switch B OSPF OSPF Switch
S 进行主备倒换时，Switch A 和 Switch B 到 Switch S 的邻居没有中断，Switch A 到 Switch B 的流
量没有中断。
组网图
2.
图1-16 OSPF NSR 配置组网图
Loop 0 Loop 0
22.22.22.22/32 Switch S 44.44.44.44/32
Vlan-int100 Vlan-int200
12.12.12.1/24 14.14.14.1/24
Vlan-int100 Vlan-int200
12.12.12.2/24 14.14.14.2/24
Switch B
Switch A

###### 3. 配置步骤

(1) 配置各路由器接口的 IP 地址和 OSPF 协议
请按照上面组网图配置各接口的 IP 地址和子网掩码，具体配置过程略。

配置各交换机之间采用 OSPF 协议进行互连，确保 Switch S、Switch A 和 Switch B 之间能够在网络层互通，并且各交换机之间能够借助 协议实现动态路由更新。具体配置过程OSPF略。
(2) 配置 OSPF NSR \# 使能 Switch S 的 OSPF NSR 功能。
<SwitchS> system-view [SwitchS] ospf 100 [SwitchS-ospf-100] non-stop-routing [SwitchS-ospf-100] quit

###### 4. 验证配置

\# Switch S 进行主备倒换。
[SwitchS] placement reoptimize Predicted changes to the placement Program Current location New location
--------------------------------------------------------------------- rib 0/0 0/0 staticroute 0/0 0/0 ospf 0/0 1/0 Continue? [y/n]:y Re-optimization of the placement start. You will be notified on completion.
Re-optimization of the placement complete. Use 'display placement' to view the new placement.
\# 查看 Switch A 上 OSPF 协议的邻居和路由。
<SwitchA> display ospf peer OSPF Process 1 with Router ID 2.2.2.1 Neighbor Brief Information Area: 0.0.0.0 Router ID Address Pri Dead-Time State Interface
3.3.3.1 12.12.12.2 1 37 Full/BDR Vlan100 <SwitchA> display ospf routing OSPF Process 1 with Router ID 2.2.2.1 Routing Table Topology base (MTID 0)
Routing for network Destination Cost Type NextHop AdvRouter Area
44.44.44.44/32 2 Stub 12.12.12.2 4.4.4.1 0.0.0.0
14.14.14.0/24 2 Transit 12.12.12.2 4.4.4.1 0.0.0.0
22.22.22.22/32 0 Stub 22.22.22.22 2.2.2.1 0.0.0.0
12.12.12.0/24 1 Transit 12.12.12.1 2.2.2.1 0.0.0.0 Total nets: 4 Intra area: 4 Inter area: 0 ASE: 0 NSSA: 0

\# 查看 Switch B 上 OSPF 协议的邻居和路由。
<SwitchB> display ospf peer OSPF Process 1 with Router ID 4.4.4.1 Neighbor Brief Information Area: 0.0.0.0 Router ID Address Pri Dead-Time State Interface
3.3.3.1 14.14.14.2 1 39 Full/BDR Vlan200 <SwitchB> display ospf routing OSPF Process 1 with Router ID 4.4.4.1 Routing Table Topology base (MTID 0)
Routing for network Destination Cost Type NextHop AdvRouter Area
44.44.44.44/32 0 Stub 44.44.44.44 4.4.4.1 0.0.0.0
14.14.14.0/24 1 Transit 14.14.14.1 4.4.4.1 0.0.0.0
22.22.22.22/32 2 Stub 14.14.14.2 2.2.2.1 0.0.0.0
12.12.12.0/24 2 Transit 14.14.14.2 2.2.2.1 0.0.0.0 Total nets: 4 Intra area: 4 Inter area: 0 ASE: 0 NSSA: 0通过上面信息可以看出在 Switch S 发生主备倒换的时候，Switch A 和 Switch B 的邻居和路由信息保持不变，从 到 的流量转发没有受到主备倒换的影响。
Switch A Switch B

##### 1.21.10 OSPF与BFD联动配置举例

###### 1. 组网需求

• Switch A、Switch B 和 Switch C 上运行 OSPF，网络层相互可达。
当 和 通过 通信的链路出现故障时 能够快速感知通告
• Switch A Switch B L2 Switch BFD OSPF
协议，并且切换到 Switch C 进行通信。

###### 3. 配置步骤

###### 2. 组网图

图1-17 OSPF 与 BFD 联动配置组网图

| 接口 | IP地址 | 设备 | 接口 |
|---|---|---|---|
| Vlan-int10 | 192.168.0.102/24 | Switch B | Vlan-int10 |
| Vlan-int11 | 10.1.1.102/24 |  | Vlan-int13 |
| Loop0 | 121.1.1.1/32 |  | Loop0 |
| Vlan-int11 | 10.1.1.100/24 |  |  |
| Vlan-int13 | 13.1.1.2/24 |  |  |

设备 IP地址Switch A 192.168.0.100/24
13.1.1.1/24
120.1.1.1/32 Switch C配置步骤
3.
(1) 配置各接口的 IP 地址（略）
(2) 配置 OSPF 基本功能\# 配置 Switch A。
<SwitchA> system-view [SwitchA] ospf [SwitchA-ospf-1] area 0 [SwitchA-ospf-1-area-0.0.0.0] network 192.168.0.0 0.0.0.255 [SwitchA-ospf-1-area-0.0.0.0] network 10.1.1.0 0.0.0.255 [SwitchA-ospf-1-area-0.0.0.0] network 121.1.1.1 0.0.0.0 [SwitchA-ospf-1-area-0.0.0.0] quit [SwitchA-ospf-1] quit \# 配置 Switch B。
<SwitchB> system-view [SwitchB] ospf [SwitchB-ospf-1] area 0 [SwitchB-ospf-1-area-0.0.0.0] network 192.168.0.0 0.0.0.255 [SwitchB-ospf-1-area-0.0.0.0] network 13.1.1.0 0.0.0.255 [SwitchB-ospf-1-area-0.0.0.0] network 120.1.1.1 0.0.0.0 [SwitchB-ospf-1-area-0.0.0.0] quit [SwitchB-ospf-1] quit配置 C。
\# Switch <SwitchC> system-view

[SwitchC] ospf [SwitchC-ospf-1] area 0 [SwitchC-ospf-1-area-0.0.0.0] network 10.1.1.0 0.0.0.255 [SwitchC-ospf-1-area-0.0.0.0] network 13.1.1.0 0.0.0.255 [SwitchC-ospf-1-area-0.0.0.0] quit [SwitchC-ospf-1] quit
(3) 配置 BFD 功能\# 在 Switch A 上使能 BFD 检测功能，并配置 BFD 参数。
[SwitchA] bfd session init-mode active [SwitchA] interface vlan-interface 10 [SwitchA-Vlan-interface10] ospf bfd enable [SwitchA-Vlan-interface10] bfd min-transmit-interval 500 [SwitchA-Vlan-interface10] bfd min-receive-interval 500 [SwitchA-Vlan-interface10] bfd detect-multiplier 7 [SwitchA-Vlan-interface10] quit \# 在 Switch B 上使能 BFD 检测功能，并配置 BFD 参数。
[SwitchB] bfd session init-mode active [SwitchB] interface vlan-interface 10 [SwitchB-Vlan-interface10] ospf bfd enable [SwitchB-Vlan-interface10] bfd min-transmit-interval 500 [SwitchB-Vlan-interface10] bfd min-receive-interval 500 [SwitchB-Vlan-interface10] bfd detect-multiplier 6 [SwitchB-Vlan-interface10] quit

###### 4. 验证配置

下面以 Switch A 为例，Switch B 和 Switch A 类似，不再赘述。
\# 显示 Switch A 的 BFD 信息。
<SwitchA> display bfd session Total Session Num: 1 Up Session Num: 1 Init Mode: Active IPv4 session working in ctrl packet mode:
LD/RD SourceAddr DestAddr State Holdtime Interface 3/1 192.168.0.102 192.168.0.100 Up 1700ms Vlan10 \# 在 Switch A 上查看 120.1.1.1/32 的路由信息，可以看出 Switch A 和 Switch B 是通过 L2 Switch进行通信的。
<SwitchA> display ip routing-table 120.1.1.1 verbose Summary Count : 1 Destination: 120.1.1.1/32 Protocol: O_INTRA Process ID: 1 SubProtID: 0x1 Age: 04h20m37s Cost: 1 Preference: 10 IpPre: N/A QosLocalID: N/A

Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0x2 OrigAs: 0 NibID: 0x26000002 LastAs: 0 AttrID: 0xffffffff Neighbor: 0.0.0.0 Flags: 0x1008c OrigNextHop: 192.168.0.100 Label: NULL RealNextHop: 192.168.0.100 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: Vlan-interface10 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0当 Switch A 和 Switch B 通过 L2 Switch 通信的链路出现故障时：
\# 在 Switch A 上查看 120.1.1.1/32 的路由信息，可以看出 Switch A 和 Switch B 已经切换到 Switch进行通信。
C <SwitchA> display ip routing-table 120.1.1.1 verbose Summary Count : 1 Destination: 120.1.1.1/32 Protocol: O_INTRA Process ID: 1 SubProtID: 0x1 Age: 04h20m37s Cost: 2 Preference: 10 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0x2 OrigAs: 0 NibID: 0x26000002 LastAs: 0 AttrID: 0xffffffff Neighbor: 0.0.0.0 Flags: 0x1008c OrigNextHop: 10.1.1.100 Label: NULL RealNextHop: 10.1.1.100 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: Vlan-interface11 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0

##### 1.21.11 OSPF快速重路由配置举例

###### 1. 组网需求

如 图 1-18 所示，Switch A、Switch B和Switch C属于同一OSPF区域，通过OSPF协议实现网络互连。要求当Switch A和Switch B之间的链路出现故障时，业务可以快速切换到链路B上。

###### 3. 配置步骤

###### 2. 组网图

图1-18 OSPF 快速重路由配置组网图Switch C 100 V l an n t - i
- i n t an 101 V l Link B V l t an
- i n - i an n t V l Link A 101 Loop0 Loop0 Vlan-int200 Vlan-int200 Switch A Switch B

| 接口 | IP地址 | 设备 | 接口 |
|---|---|---|---|
| Vlan-int100 | 12.12.12.1/24 | Switch B | Vlan-int101 |
| Vlan-int200 | 13.13.13.1/24 |  | Vlan-int200 |
| Loop0 | 1.1.1.1/32 |  | Loop0 |
| Vlan-int100 | 12.12.12.2/24 |  |  |
| Vlan-int101 | 24.24.24.2/24 |  |  |

设备 IP地址Switch A 24.24.24.4/24
13.13.13.2/24
4.4.4.4/32 Switch C配置步骤
3.
(1) 配置各交换机接口的 IP 地址和 OSPF 协议请按照上面组网图配置各接口的 IP 地址和子网掩码，具体配置过程略。
配置各交换机之间采用 OSPF 协议进行互连，确保 Switch A、Switch B 和 Switch C 之间能够在网络层互通，并且各交换机之间能够借助 协议实现动态路由更新。
OSPF具体配置过程略。
(2) 配置 OSPF 快速重路由OSPF 支持快速重路由配置有两种配置方法，可以任选一种。
方法一：使能 Switch A 和 Switch B 的 OSPF 快速重路由功能（通过 LFA 算法选取备份下一跳信息）
配置 A。
\# Switch <SwitchA> system-view [SwitchA] ospf 1 [SwitchA-ospf-1] fast-reroute lfa [SwitchA-ospf-1] quit \# 配置 Switch B。
<SwitchB> system-view [SwitchB] ospf 1 [SwitchB-ospf-1] fast-reroute lfa [SwitchB-ospf-1] quit方法二：使能 Switch A 和 Switch B 的 OSPF 快速重路由功能（通过路由策略指定备份下一跳）
\# 配置 Switch A。
<SwitchA> system-view [SwitchA] ip prefix-list abc index 10 permit 4.4.4.4 32

###### 4. 验证配置

[SwitchA] route-policy frr permit node 10 [SwitchA-route-policy-frr-10] if-match ip address prefix-list abc [SwitchA-route-policy-frr-10] apply fast-reroute backup-interface vlan-interface 100 backup-nexthop 12.12.12.2 [SwitchA-route-policy-frr-10] quit [SwitchA] ospf 1 [SwitchA-ospf-1] fast-reroute route-policy frr [SwitchA-ospf-1] quit \# 配置 Switch B。
<SwitchB> system-view [SwitchB] ip prefix-list abc index 10 permit 1.1.1.1 32 [SwitchB] route-policy frr permit node 10 [SwitchB-route-policy-frr-10] if-match ip address prefix-list abc [SwitchB-route-policy-frr-10] apply fast-reroute backup-interface vlan-interface 101 backup-nexthop 24.24.24.2 [SwitchB-route-policy-frr-10] quit [SwitchB] ospf 1 [SwitchB-ospf-1] fast-reroute route-policy frr [SwitchB-ospf-1] quit验证配置
4.
\# 在 Switch A 上查看 4.4.4.4/32 网段路由，可以看到备份下一跳信息。
[SwitchA] display ip routing-table 4.4.4.4 verbose Summary Count : 1 Destination: 4.4.4.4/32 Protocol: O_INTRA Process ID: 1 SubProtID: 0x1 Age: 04h20m37s Cost: 1 Preference: 10 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0x2 OrigAs: 0 NibID: 0x26000002 LastAs: 0 AttrID: 0xffffffff Neighbor: 0.0.0.0 Flags: 0x1008c OrigNextHop: 13.13.13.2 Label: NULL RealNextHop: 13.13.13.2 BkLabel: NULL BkNextHop: 12.12.12.2 Tunnel ID: Invalid Interface: Vlan-interface200 BkTunnel ID: Invalid BkInterface: Vlan-interface100 FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0 \# 在 Switch B 上查看 1.1.1.1/32 网段路由，可以看到备份下一跳信息。
[SwitchB] display ip routing-table 1.1.1.1 verbose Summary Count : 1

Destination: 1.1.1.1/32 Protocol: O_INTRA Process ID: 1 SubProtID: 0x1 Age: 04h20m37s Cost: 1 Preference: 10 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0x2 OrigAs: 0 NibID: 0x26000002 LastAs: 0 AttrID: 0xffffffff Neighbor: 0.0.0.0 Flags: 0x1008c OrigNextHop: 13.13.13.1 Label: NULL RealNextHop: 13.13.13.1 BkLabel: NULL BkNextHop: 24.24.24.2 Tunnel ID: Invalid Interface: Vlan-interface200 BkTunnel ID: Invalid BkInterface: Vlan-interface101 FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0

#### 1.22 常见配置错误举例

##### 1.22.1 OSPF邻居无法建立

###### 1. 故障现象

OSPF 邻居无法建立。

###### 2. 分析

如果物理连接和下层协议正常，则检查接口上配置的 OSPF 参数，必须保证与相邻路由器的参数一致，区域号相同，网段与掩码也必须一致（点到点与虚连接的网段与掩码可以不同）。

###### 3. 处理过程

(1) 使用 display ospf peer 命令查看 OSPF 邻居状态。
(2) 使用 display ospf interface 命令查看 OSPF 接口的信息。
(3) 检查物理连接及下层协议是否正常运行，可通过 ping 命令测试。若从本地路由器 Ping 对端
路由器不通，则表明物理连接和下层协议有问题。
检查 定时器，在同一接口上邻居失效时间应至少为 报文发送时间间隔的 倍。
(4) OSPF Hello 4
如果是 网络，则应该使用 命令手工指定邻居。
(5) NBMA peer ip-address
如果网络类型为广播网或 NBMA，则至少有一个接口的路由器优先级大于零。
(6)

##### 1.22.2 OSPF路由信息不正确

###### 1. 故障现象

不能发现其他区域的路由。
OSPF

###### 2. 分析

应保证骨干区域与所有的区域相连接。若一台路由器配置了两个以上的区域，则至少有一个区域应与骨干区域相连。骨干区域不能配置成 Stub 区域。
在 Stub 区域内的路由器不能接收外部 AS 的路由。如果一个区域配置成 Stub 区域，则与这个区域相连的所有路由器都应将此区域配置成 区域。
Stub

###### 3. 处理过程

(1) 使用 display ospf peer 命令查看 OSPF 邻居状态。
(2) 使用 display ospf interface 命令查看 OSPF 接口的信息。
使用 查看 的信息是否完整。
(3) display ospf lsdb LSDB
使用 命令查看区域是否配
(4) display current-configuration configuration ospf
置正确。若配置了两个以上的区域，则至少有一个区域与骨干区域相连。
(5) 如果某区域是 Stub 区域，则该区域中的所有路由器都要配置 stub 命令；如果某区域是 NSSA
区域，则该区域中的所有路由器都要配置 nssa 命令。
(6) 如果配置了虚连接，使用 display ospf vlink 命令查看 OSPF 虚连接是否正常。

## 05-IS-IS配置

目 录简介的网络类型协议规范配置 基本功能配置接口网络类型配置 链路开销配置IS-IS发布缺省路由配置 对引入的路由信息进行过滤

配置Hello报文发送时间间隔配置 发送时间间隔配置接口的 优先级配置接口发送小型Hello报文配置 连接位配置前缀抑制配置IS-IS

IS-IS显示和维护基本功能配置举例验证配置举例IS-IS快速重路由配置举例

### 1 IS-IS

1 IS-IS

#### 1.1 IS-IS简介

属于 IGP（Interior Protocol，内部网关协议），用于自治系统内部。IS-IS 是一种链IS-IS Gateway路状态协议，使用 SPF（Shortest Path First，最短路径优先）算法进行路由计算。

##### 1.1.1 IS-IS基本术语

IS（Intermediate System）：中间系统。相当于 TCP/IP 中的路由器，是 IS-IS 协议中生成路
•由和传播路由信息的基本单元。在下文中 和路由器具有相同的含义。
IS ES（End System）：终端系统。相当于 中的主机系统。ES 不参与 路由协议的
• TCP/IP IS-IS处理，ISO 使用专门的 ES-IS 协议定义终端系统与中间系统间的通信。
• RD （ Routing Domain ）：路由域。在一个路由域中多个 IS 通过相同的路由协议来交换路由信息。
• Area：区域，路由域的细分单元，IS-IS 允许将整个路由域分为多个区域。
• LSDB（Link State DataBase）：链路状态数据库。网络内所有链路的状态组成了链路状态数据库，在每一个 IS 中都至少有一个 LSDB。IS 使用 SPF 算法，利用 LSDB 来生成自己的路由。
• LSPDU（Link State Protocol Data Unit）：链路状态协议数据单元，简称 LSP。在 IS-IS 中，每一个 都会生成 LSP，此 包含了本 的所有链路状态信息。
IS LSP IS NPDU（Network Unit）：网络协议数据单元，是 中的网络层协议报文，
• Protocol Data OSI相当于 TCP/IP 中的 IP 报文。
• DIS（Designated IS）：广播网络上选举的指定中间系统，也可以称为指定 IS。
NSAP（Network Point）：网络服务接入点，即 中网络层的地址，用来
• Service Access OSI标识一个抽象的网络服务访问点，描述 OSI 模型的网络地址结构。

##### 1.1.2 IS-IS地址

如 图 1-1 所示，NSAP由IDP（Initial Domain Part）和DSP（Domain Specific Part）组成。IDP相当于 IP 地址中的主网络号， DSP 相当于 IP 地址中的子网号和主机地址。
部分是 规定的，它由 AF（I Identifier）和 ID（I Identifier）
IDP ISO Authority and Format Initial Domain两部分组成：
• AFI 表示地址分配机构和地址格式。
• IDI 用来标识域。
DSP 由 HO-DSP（High Order Part of DSP）、SystemID 和 SEL 三个部分组成：
• HO-DSP 用来分割区域。
用来区分主机。
• SystemID有时也写成 N-SEL（NSAP Selector），它的作用类似 中的“协议标识符”，用于指示
• SEL IP服务类型，不同的传输协议对应不同的 SEL。
IDP 和 DSP 的长度都是可变的，NSAP 总长最多是 20 个字节，最少 8 个字节。

图1-1 IS-IS 协议的地址结构示意图IS-IS 地址结构由以下三部分组成：
• 区域地址和 中的 一起，既能够标识路由域，也能够标识路由域中的区域，被称为区域地IDP DSP HO-DSP址。两个不同的路由域中不允许有相同的区域地址。
一般情况下，一台路由器只需要配置一个区域地址，且同一区域中所有节点的区域地址都要相同。
为了支持区域的平滑合并、分割及转换，一台路由器最多可配置 3 个区域地址。
• System ID System ID 用来在区域内唯一标识主机或路由器。它的长度固定为 48 比特。
在实际应用中，一般使用 Router ID 与 System ID 进行对应。假设一台路由器使用接口 Loopback0的 IP 地址 168.10.1.1 作为 Router ID，则它在 IS-IS 使用的 System ID 可通过如下方法转换得到：
将 IP 地址 168.10.1.1 的每一部分都扩展为 3 位，不足 3 位的在前面补 0；
(cid:123)
将扩展后的地址 168.010.001.001 重新划分为 3 部分，每部分由 4 位数字组成，得到的(cid:123)
就是 ID。
1680.1000.1001 System实际 的指定可以有不同的方法，但要保证能够唯一标识主机或路由器。
System ID
• SEL SEL 用于指示服务类型，不同的传输协议对应不同的 SEL。它的长度固定为 8 比特。在 IP 中，SEL均为 00。

##### 1.1.3 NET

NET（Network Title，网络实体名称）指示的是 本身的网络层信息，不包括传输层信息，Entity IS可以看作是一类特殊的 NSAP，即 SEL 为 0 的 NSAP 地址。因此，NET 的长度与 NSAP 的相同，为 8～20 个字节。
NET 由三部分组成：
• 区域 ID：它的长度可变的，为 1～13 个字节。
• System ID：用来在区域内唯一标识主机或路由器，它的长度固定为 6 个字节。
• SEL：为 0，它的长度固定为 1 个字节。
例如 NET 为：ab.cdef.1234.5678.9abc.00，则其中区域 ID 为 ab.cdef，System ID 为 1234.5678.9abc，SEL 为 00。
通常情况下，一台路由器配置一个 NET 即可，当区域需要重新划分时，例如将多个区域合并，或者将一个区域划分为多个区域，这种情况下配置多个 NET 可以在重新配置时仍然能够保证路由的正确性。由于一台路由器最多可配置 个区域地址，所以最多也只能配置 个 NET。在配置多个3 3 NET 时，必须保证它们的 System ID 都相同。

##### 1.1.4 IS-IS区域

为了支持大规模的路由网络，IS-IS 在路由域内采用两级的分层结构。一个大的路由域通常被分成多个区域（Areas）。一般来说，我们将 Level-1 路由器部署在区域内，Level-2 路由器部署在区域间，Level-1-2 路由器部署在 Level-1 路由器和 Level-2 路由器的中间。

###### 1. Level-1路由器

Level-1 路由器负责区域内的路由，它只与属于同一区域的 Level-1 和 Level-1-2 路由器形成邻居关系，维护一个 的 LSDB，该 包含本区域的路由信息，到区域外的报文转发给最近的Level-1 LSDB Level-1-2 路由器。
属于不同区域的 Level-1 路由器不能形成邻居关系。

###### 2. Level-2路由器

Level-2 路由器负责区域间的路由，可以与同一区域或者其它区域的 Level-2 和 Level-1-2 路由器形成邻居关系，维护一个 Level-2 的 LSDB，该 LSDB 包含区域间的路由信息。所有 Level-2 路由器和 Level-1-2 路由器组成路由域的骨干网，负责在不同区域间通信，骨干网必须是物理连续的。
路由器是否形成邻居关系与区域无关。
Level-2

###### 3. Level-1-2路由器

同时属于 Level-1和 Level-2的路由器称为 Level-1-2路由器，可以与同一区域的 Level-1和 Level-1-2路由器形成 Level-1 邻居关系，也可以与同一区域或者其他区域的 Level-2 和 Level-1-2 路由器形成的邻居关系。Level-1 路由器必须通过 路由器才能连接至其他区域。Level-1-2 路Level-2 Level-1-2由器维护两个 LSDB，Level-1 的 LSDB 用于区域内路由，Level-2 的 LSDB 用于区域间路由。

##### 1.1.5 IS-IS拓扑结构

图 1-2 为一个运行IS-IS协议的网络，其中Area 1 是骨干区域，该区域中的所有路由器均是Level-2路由器。另外 个区域为非骨干区域，它们都通过Level-1-2 路由器与骨干路由器相连。
4

图1-2 IS-IS 拓扑结构图之一Area 3 Area 2 L1/L2 L1/L2 L2 L1 L2 Area 1 L2 L2 Area 5 L1/L2 L1 L1/L2 Area 4 L1 L1 L1 L1图 是IS-IS的另外一种拓扑结构图。在这个拓扑中，并没有规定哪个区域是骨干区域。所有Level-2 1-3路由器和Level-1-2 路由器构成了IS-IS的骨干网，它们可以属于不同的区域，但必须是物理连续的。
IS-IS的骨干网（Backbone）指的不是一个特定的区域。
图1-3 拓扑结构图之二IS-IS Area 1 L2 L1 Area 4 Area 2 L1/L2 L1 L1/L2 L1 Area 3 L2 IS-IS不论是Level-1还是 Level-2路由，都采用 SPF算法，分别生成最短路径树（Shortest Path Tree，SPT）。

##### 1.1.6 路由渗透

通常情况下，区域内的路由通过 的路由器进行管理。所有的 路由器和 路Level-1 Level-2 Level-1-2由器构成一个 Level-2 区域。因此，一个 IS-IS 的路由域可以包含多个 Level-1 区域，但只有一个Level-2 区域。
Level-1 区域必须且只能与 Level-2 区域相连，不同的 Level-1 区域之间并不相连。
Level-1 区域内的路由信息通过 Level-1-2 路由器发布到 Level-2 区域，因此，Level-2 路由器知道整个 IS-IS 路由域的路由信息。但是，在缺省情况下，Level-2 路由器并不将自己知道的其它 Level-1区域以及 区域的路由信息发布到 区域。这样，Level-1 路由器将不了解本区域以外Level-2 Level-1的路由信息，Level-1 路由器只将去往其它区域的报文发送到最近的 Level-1-2 路由器，所以可能导致对本区域之外的目的地址无法选择最佳的路由。
为解决上述问题，IS-IS 提供了路由渗透功能，使 Level-1-2 路由器可以将己知的其它 Level-1 区域以及 Level-2 区域的路由信息发布到指定的 Level-1 区域。

##### 1.1.7 IS-IS的网络类型

IS-IS 只支持两种类型的网络，根据物理链路不同可分为：
• 广播链路：如 Ethernet、Token-Ring 等。
• 点到点链路：如 PPP、HDLC 等。
不能在点到多点（Point-to-MultiPoint，P2MP）链路上运行。
IS-IS

##### 1.1.8 DIS和伪节点

在广播网络中，IS-IS 需要在所有的路由器中选举一个路由器作为 DIS。
和 的 是分别选举的，用户可以为不同级别的 选举设置不同的优先级。DIS Level-1 Level-2 DIS DIS优先级数值越高，被选中的可能性就越大。如果优先级最高的路由器有多台，则其中 SNPA（Subnetwork Point of Attachment，子网连接点）地址（广播网络中的 SNPA 地址是 MAC 地址）
最大的路由器会被选中。不同级别的 可以是同一台路由器，也可以是不同的路由器。
DIS与 的不同点：
OSPF优先级为 0 的路由器也参与 DIS 的选举；
•当有新的路由器加入，并符合成为 DIS 的条件时，这个路由器会被选中成为新的 DIS，此更
•改会引起一组新的 泛洪。
LSP在IS-IS广播网中，同一网段上的同一级别的路由器之间都会形成邻接关系，包括所有的非DIS路由器之间也会形成邻接关系。如 图 1-4 所示。

图1-4 IS-IS 广播网的 DIS 和邻接关系L1/L2 L1/L2 L2 adjacencies L1 L2 L1 adjacencies DIS DIS用来创建和更新伪节点（Pseudonodes），并负责生成伪节点的 LSP，用来描述这个网络上有DIS哪些路由器。
伪节点是用来模拟广播网络的一个虚拟节点，并非真实的路由器。在 IS-IS 中，伪节点用 DIS 的System ID 和一个字节的 Circuit ID（非 0 值）标识。
使用伪节点可以简化网络拓扑，减少 SPF 的资源消耗。
IS-IS 广播网络上所有的路由器之间都形成邻接关系，但 LSDB 的同步仍然依靠 DIS 来保证。

##### 1.1.9 IS-IS报文

###### 1. PDU

IS-IS报文是直接封装在数据链路层的帧结构中的。PDU（Protocol Unit，协议数据单元）可Data以分为两个部分，报文头和变长字段部分。其中报文头又可分为通用报头和专用报头。对于所有PDU来说，通用报头都是相同的，但专用报头根据PDU类型不同而有所差别，如 图 1-5 所示。
图1-5 格式PDU表1-1 PDU 类型对应关系表

| 类型值 | PDU 类型 |  |  | 简称 |  |
|---|---|---|---|---|---|
|  | evel-1 LAN IS-IS Hello PDU |  |  |  |  |
|  | evel-2 LAN IS-IS Hello PDU |  |  |  |  |
|  | oint-to-Point IS-IS Hello PDU |  |  |  |  |
|  | evel-1 Link State PDU |  |  |  |  |
|  | evel-2 Link State PDU |  |  |  |  |

###### 3. LSP报文

| 类型值 |  |  | PDU 类型 |  |  | 简称 |  |
|---|---|---|---|---|---|---|---|
|  |  | Level-1 Complete Sequence Numbers PDU |  |  |  |  |  |
|  |  | Level-2 Complete Sequence Numbers PDU |  |  |  |  |  |
|  |  | Level-1 Partial Sequence Numbers PDU |  |  |  |  |  |
|  |  | Level-2 Partial Sequence Numbers PDU |  |  |  |  |  |

###### 2. Hello报文

Hello 报文：用于建立和维持邻居关系，也称为 IIH（IS-to-IS Hello PDUs）。其中，广播网中的 Level-1路由器使用 IIH，广播网中的 路由器使用 IIH，点到点网络中的路Level-1 LAN Level-2 Level-2 LAN由器则使用 P2P IIH。
LSP报文
3.
LSP 报文：用于交换链路状态信息。LSP 分为两种：Level-1 LSP 和 Level-2 LSP。Level-1 路由器传送 Level-1 LSP ， Level-2 路由器传送 Level-2 LSP ， Level-1-2 路由器则可传送以上两种 LSP 。

###### 4. SNP报文

SNP（Sequence PDU，时序报文）通过描述全部或部分数据库中的 来同步 LSDB，Number LSP从而维护 LSDB 的完整和同步。
SNP 包括 CSNP（Complete Sequence Number PDU，全时序报文）和 PSNP（Partial Sequence Number PDU，部分时序报文），进一步又可分为 Level-1 CSNP、Level-2 CSNP、Level-1 PSNP和 Level-2 PSNP。
CSNP 包括 LSDB 中所有 LSP 的概要信息，从而可以在相邻路由器间保持 LSDB 的同步。在广播网络上，CSNP 由 定期发送（缺省的发送周期为 秒）；在点到点链路上，CSNP 只在第一次DIS 10建立邻接关系时发送。
PSNP只列举最近收到的一个或多个 LSP的序列号，它能够一次对多个 LSP进行确认。当发现 LSDB不同步时，也用 PSNP 来请求邻居发送新的 LSP。

###### 5. CLV

PDU中的变长字段部分是多个CLV（Code-Length-Value）三元组。其格式如 图 1-6 所示：
图1-6 CLV 格式不同PDU类型所包含的CLV是不同的，如 表 1-2 所示。
表1-2 PDU 类型和包含的 CLV 名称

| CLV Code |  |  | 名称 |  |  | 所应用的 PDU 类型 |  |
|---|---|---|---|---|---|---|---|
|  |  | Area Addresses |  |  |  |  |  |
|  |  | IS Neighbors（LSP） |  |  |  |  |  |

|  | CLV Code |  |  | 名称 |  |  | 所应用的 PDU 类型 |  |
|---|---|---|---|---|---|---|---|---|
|  |  |  | Partition Designated Level-2 IS |  |  |  |  |  |
|  |  |  | IS Neighbors（MAC Address） |  |  |  |  |  |
|  |  |  | IS Neighbors（SNPA Address） |  |  |  |  |  |
|  |  |  | Padding |  |  |  |  |  |
|  |  |  | LSP Entries |  |  |  |  |  |
|  |  |  | Authentication Information |  |  |  |  |  |
|  |  |  | IP Internal Reachability Information |  |  |  |  |  |
|  |  |  | Protocols Supported |  |  |  |  |  |
|  |  |  | IP External Reachability Information |  |  |  |  |  |
|  |  |  | Inter-Domain Routing Protocol Information |  |  |  |  |  |
|  |  |  | IP Interface Address |  |  |  |  |  |
|  |  |  | MT-ISN |  |  |  |  |  |
|  |  |  | M-Topologies |  |  |  |  |  |
|  |  |  | MT IP. Reach |  |  |  |  |  |
|  |  |  | MT IPv6 IP. Reach |  |  |  |  |  |

其中，Code 值从 1 到 10 的 CLV 在 ISO 10589 中定义（有 2 类未在上表中列出），128 到 132 的CLV 在 RFC 1195 中定义，多拓扑相关 CLV 在 RFC 5120 中定义。

##### 1.1.10 IPv6 IS-IS

IS-IS（Intermediate System-to-Intermediate System，中间系统到中间系统）支持多种网络层协议，其中包括 IPv6 协议，支持 IPv6 协议的 IS-IS 路由协议又称为 IPv6 IS-IS 动态路由协议。
IETF 中规定了 IS-IS 为支持 IPv6 所新增的内容，主要是新添加的支持 IPv6 协议的两个 TLV（Type-Length-Values）和一个新的 NLPID（Network Identifier，网络层协议标识Layer Protocol符）。
TLV 是 LSP （ Link State PDU ，链路状态协议数据单元）中的一个可变长字段值。新增的两个 TLV分别是：
• IPv6 Reachability：类型值为 236（0xEC），通过定义路由信息前缀、度量值等信息来说明网络的可达性。
• IPv6 Interface Address：类型值为 232（0xE8），它对应于 IPv4 中的“IP Interface Address”TLV，只不过把原来的 比特的 地址改为 比特的 地址。
32 IPv4 128 IPv6 NLPID 是标识网络层协议报文的一个 8 比特字段，IPv6 的 NLPID 值固定为 142（0x8E）。

##### 1.1.11 协议规范

与 IS-IS 相关的协议规范有：
• ISO 8348：Ad2 Network Services Access Points

ISO 9542：ES-IS Routing Protocol
•ISO 10589：ISO IS-IS Routing Protocol
•RFC 1195：Use of OSI IS-IS for Routing in TCP/IP and Dual Environments
•
• RFC 3277：IS-IS Transient Blackhole Avoidance
• RFC 3358：Optional Checksums in ISIS
• RFC 3359：Reserved Type, Length and Value (TLV) Codepoints in Intermediate System to Intermediate System RFC 3563：Cooperative Agreement Between the ISOC/IETF and ISO/IEC Joint Technical
•Committee 1/Sub Committee 6 (JTC1/SC6) on IS-IS Routing Protocol Development 3719：Recommendations
• RFC for Interoperable Networks using Intermediate System to Intermediate System (IS-IS)
• RFC 3787：Recommendations for Interoperable IP Networks using Intermediate System to Intermediate System (IS-IS)
• RFC 4444：Management Information Base for Intermediate System to Intermediate System (IS-IS)
RFC 5029：Definition of an IS-IS Link Attribute Sub-TLV
•
• RFC 5089：IS-IS Protocol Extensions for Path Computation Element (PCE) Discovery
• RFC 5120：Multi Topology (MT) Routing in Intermediate System to Intermediate Systems (IS-ISs)
5130：A
• RFC Policy Control Mechanism in IS-IS Using Administrative Tags RFC 5301：Dynamic Hostname Exchange Mechanism for IS-IS
•RFC 5302：Domain-Wide Prefix Distribution with Two-Level IS-IS
•RFC 5303：Three-Way Handshake for IS-IS Point-to-Point Adjacencies
•
• RFC 5304：IS-IS Cryptographic Authentication
• RFC 5306：Restart Signaling for IS-IS
• RFC 5308：Routing IPv6 with IS-IS
• RFC 5310：IS-IS Generic Cryptographic Authentication
• RFC 5311：Simplified Extension of Link State PDU (LSP) Space for IS-IS
• RFC 6165：Extensions to IS-IS for Layer-2 Systems
• RFC 6213：IS-IS BFD-Enabled TLV
• RFC 6232：Purge Originator Identification TLV for IS-IS
• RFC 6233：IS-IS Registry Extension for Purges
• RFC 6329：IS-IS Extensions Supporting IEEE 802.1aq Shortest Path Bridging
• RFC 6571：Loop-Free Alternate (LFA) Applicability in Service Provider (SP) Networks
• RFC 6823：Advertising Generic Information in IS-IS：
• RFC 7142 OSI IS-IS Intra-domain Routing Protocol 7356：IS-IS
• RFC Flooding Scope Link State PDUs (LSPs)
7370：Updates
• RFC to the IS-IS TLV Codepoints Registry 7602：IS-IS
• RFC Extended Sequence Number TLV

RFC 7645：The Keying and Authentication for Routing Protocol (KARP) IS-IS Security
•Analysis 7775：IS-IS
• RFC Route Preference for Extended IP and IPv6 Reachability 7794：IS-IS
• RFC Prefix Attributes for Extended IPv4 and IPv6 Reachability 7813：IS-IS
• RFC Path Control and Reservation 7917：Advertising
• RFC Node Administrative Tags in IS-IS RFC 7981：IS-IS Extensions for Advertising Router Information
•RFC 7987：IS-IS Minimum Remaining Lifetime
•

#### 1.2 IPv4 IS-IS配置任务简介

IPv4 IS-IS 配置任务如下：
(1) 配置IS-IS基本功能
a. 使能IPv4 IS-IS功能
b. （可选）配置路由器的Level级别和接口的链路邻接关系类型
c. （可选）配置接口网络类型
(2) （可选）配置IS-IS路由信息控制配置IS-IS链路开销(cid:123)
配置IS-IS路由优先级(cid:123)
配置IS-IS最大等价路由条数(cid:123)
配置IS-IS路由聚合(cid:123)
配置IS-IS发布缺省路由(cid:123)
配置IS-IS引入外部路由(cid:123)
配置IS-IS对接收的路由是否加入IP路由表进行过滤(cid:123)
配置IS-IS对引入的路由信息进行过滤(cid:123)
配置IS-IS路由渗透(cid:123)
配置允许设备将IS-IS链路状态信息发布到BGP (cid:123)
(3) （可选）配置IS-IS定时器配置 Hello 报文发送时间间隔(cid:123)
配置CSNP报文发送时间间隔(cid:123)
配置LSP最大生存时间(cid:123)
配置LSP刷新周期和LSP重新生成的时间间隔(cid:123)
配置LSP发送时间间隔(cid:123)
配置SPF参数(cid:123)
(4) （可选）配置IS-IS报文相关功能配置接口的 DIS 优先级(cid:123)
配置接口的Tag值(cid:123)
配置Hello报文失效数目(cid:123)
禁止接口发送和接收IS-IS报文(cid:123)

配置接口发送小型Hello报文(cid:123)
配置LSP报文长度(cid:123)
配置LSP快速扩散功能(cid:123)
配置LSP分片扩展功能(cid:123)
(5) （可选）配置IS-IS高级功能配置路由收敛的优先级(cid:123)
配置LSDB过载标志位(cid:123)
配置ATT连接位(cid:123)
配置IS-IS主机名映射(cid:123)
(6) （可选）配置IS-IS日志和告警功能配置邻接状态变化的输出开关(cid:123)
配置IS-IS网管功能(cid:123)
(7) （可选）配置IS-IS快速收敛配置ISPF (cid:123)
配置前缀抑制(cid:123)
配置PIC (cid:123)
（可选）提高IS-IS网络的安全性
(8)
配置邻居关系验证(cid:123)
配置区域验证(cid:123)
配置路由域验证(cid:123)
(9) （可选）提高IS-IS网络的可靠性配置IS-IS GR (cid:123)
配置IS-IS NSR (cid:123)
配置IS-IS与BFD联动(cid:123)
配置IS-IS快速重路由(cid:123)

#### 1.3 IPv6 IS-IS配置任务简介

IPv4 IS-IS 配置任务如下：
(1) 配置IS-IS基本功能
a. 使能IPv6 IS-IS功能
b. （可选）配置路由器的Level级别和接口的链路邻接关系类型
c. （可选）配置接口网络类型
(2) （可选）配置IS-IS支持IPv6 单播拓扑（可选）配置IS-IS路由信息控制
(3)
配置 链路开销IS-IS (cid:123)
配置IS-IS路由优先级(cid:123)
配置IS-IS最大等价路由条数(cid:123)
配置IS-IS路由聚合(cid:123)

配置IS-IS发布缺省路由(cid:123)
配置IS-IS引入外部路由(cid:123)
配置IS-IS对接收的路由是否加入IP路由表进行过滤(cid:123)
配置IS-IS对引入的路由信息进行过滤(cid:123)
配置IS-IS路由渗透(cid:123)
配置允许设备将IS-IS链路状态信息发布到BGP (cid:123)
(4) （可选）配置IS-IS定时器配置Hello报文发送时间间隔(cid:123)
配置CSNP报文发送时间间隔(cid:123)
配置LSP最大生存时间(cid:123)
配置LSP刷新周期和LSP重新生成的时间间隔(cid:123)
配置LSP发送时间间隔(cid:123)
配置SPF参数(cid:123)
(5) （可选）配置IS-IS报文相关功能配置接口的DIS优先级(cid:123)
配置接口的Tag值(cid:123)
配置Hello报文失效数目(cid:123)
禁止接口发送和接收IS-IS报文(cid:123)
配置接口发送小型Hello报文(cid:123)
配置LSP报文长度(cid:123)
配置LSP快速扩散功能(cid:123)
配置LSP分片扩展功能(cid:123)
(6) （可选）配置IS-IS高级功能配置路由收敛的优先级(cid:123)
配置LSDB过载标志位(cid:123)
配置ATT连接位(cid:123)
配置IS-IS主机名映射(cid:123)
(7) （可选）配置 IS-IS 日志和告警功能配置邻接状态变化的输出开关(cid:123)
配置IS-IS网管功能(cid:123)
(8) （可选）配置IS-IS快速收敛配置ISPF (cid:123)
配置前缀抑制(cid:123)
配置PIC (cid:123)
(9) （可选）提高 IS-IS 网络的安全性配置邻居关系验证(cid:123)
配置区域验证(cid:123)
配置路由域验证(cid:123)

(10) （可选）提高IS-IS网络的可靠性
配置IS-IS GR
(cid:123)
配置IS-IS NSR
(cid:123)
配置IS-IS与BFD联动
(cid:123)
配置IS-IS快速重路由
(cid:123)

#### 1.4 配置IS-IS基本功能

##### 1.4.1 使能IPv4 IS-IS功能

(1) 进入系统视图。
system-view
(2) 启动 IS-IS，并进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
缺省情况下，系统没有运行 IS-IS。
(3) 配置网络实体名称。
network-entity net
缺省情况下，未配置 NET。
(4) 退回系统视图。
quit
进入接口视图。
(5)
interface interface-type interface-number
配置指定接口上使能 功能。
(6) IS-IS
isis enable [ process-id ]
缺省情况下，接口上的 功能处于关闭状态，且没有任何 进程与其关联。
IS-IS IS-IS

##### 1.4.2 使能IPv6 IS-IS功能

(1) 进入系统视图。
system-view
(2) 启动 IS-IS 路由进程，进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
缺省情况下，系统没有运行 IS-IS。
配置网络实体名称（NET）。
(3)
network-entity net
缺省情况下，未配置 NET。
创建并进入 地址族视图。
(4) IPv6
address-family ipv6 [ unicast ]
(5) 退回 IS-IS 视图。
quit

###### 1. 功能简介

(6) 退回系统视图。
quit
(7) 进入接口视图。
interface interface-type interface-number
(8) 使能接口 IS-IS 路由进程的 IPv6 能力并指定要关联的 IS-IS 进程号。
isis ipv6 enable [ process-id ]
缺省情况下，接口上 IS-IS 的 IPv6 能力处于关闭状态。

##### 1.4.3 配置路由器的Level级别和接口的链路邻接关系类型

功能简介
1.
建议用户在配置 IS-IS 时配置路由器类型：
• 如果只有一个区域，建议用户将所有路由器设置为 Level-1 或者 Level-2，因为没有必要让所有路由器同时维护两个完全相同的 LSDB。
在 IP 网络中使用时，建议将所有的路由器都设置为 Level-2，这样有利于以后的扩展。
•当路由器类型是 Level-1（Level-2）时，接口的链路邻接类型只能为 Level-1（Level-2），当路由器类型是 时，接口的链路邻接类型缺省为 Level-1-2，当路由器只需要与对端建立Level-1-2 Level-1（Level-2）的邻接关系时，可以将接口的链路邻接类型配置为 Level-1（Level-2）来限制接口上所能建立的邻接关系，如 Level-1的接口只能建立 Level-1的邻接关系，Level-2的接口只能建立 Level-2的邻接关系，让接口只发送和接收 Level-1（Level-2）类型的 报文，既减少了路由器的处理Hello时间又节省了带宽。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 配置路由器的 Level 级别。
is-level { level-1 | level-1-2 | level-2 }
缺省情况下，路由器的 级别为 。
Level Level-1-2
退回系统视图。
(4)
quit
进入接口视图。
(5)
interface interface-type interface-number
(6) 配置接口的链路邻接关系类型。
isis circuit-level [ level-1 | level-1-2 | level-2 ]
缺省情况下，接口既可以建立 Level-1 的邻接关系，也可以建立 Level-2 的邻接关系。

###### 1. 功能简介

##### 1. 功能简介

##### 1.4.4 配置接口网络类型

功能简介
1.
接口网络类型不同，其工作机制也略微不同，如：当网络类型为广播网时，需要选举 DIS、通过泛洪 报文来实现 同步；当网络类型为 时，不需要选举 DIS，LSDB 同步机制也不CSNP LSDB P2P同。
当只有两台路由器接入到同一个广播网时，通过将接口网络类型配置为 P2P 可以使 IS-IS 按照 P2P而不是广播网的工作机制运行，避免 DIS 选举以及 CSNP 的泛洪，既可以节省网络带宽，又可以加快网络的收敛速度。

###### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置接口的网络类型为 P2P。
isis circuit-type p2p缺省情况下，路由器接口网络类型根据物理接口决定，交换机 VLAN 接口网络类型为Broadcast。
仅当接口的网络类型为广播网，且只有两台路由器接入该广播网时才需要进行该项配置，并且两台路由器都要进行此项配置。

#### 1.5 配置IS-IS支持IPv6单播拓扑

功能简介
1.
IPv6 IS-IS 和 IPv4 IS-IS 使用同样的最短路径进行路由计算，IPv4 和 IPv6 的混合拓扑被看成是一个集成的拓扑，这就要求所有 IPv4 和 IPv6 的拓扑信息必须一致。但是 IPv4 和 IPv6 协议在网络中的部署可能不一致，IPv4 和 IPv6 的拓扑信息可能不同。当一些路由器和链路不支持 IPv6 协议时，支持双协议栈的路由器因为无法感知到这些路由器和链路不支持 IPv6，仍然会把 IPv6 报文转发给它们，这就导致 IPv6 报文由于无法转发而被丢弃。
IS-IS MTR （ Multi-Topology Routing ，多拓扑路由）的功能之一就是实现 IS-IS 支持 IPv6 单播拓扑，即 和 分拓扑计算，从而解决上面的问题。
IPv4 IPv6

图1-7 IS-IS 支持 IPv6 单播拓扑功能示意图Router A Router B IPv6 IPv6 IPv6 IPv4 36 3 IPv6 IPv4 IPv4 IPv4 Router D Router C如 图 所示，图中的数值表示对应链路上的开销值；Router A、Router B和Router D支持IPv4 和1-7 IPv6 双协议栈；Router C只支持IPv4 协议，不能转发IPv6 报文。
在 Router A、Router B、Router C、Router D 上都配置 IS-IS 支持 IPv6 单播拓扑，所有的路由器对于 IPv4、IPv6 都分为两个拓扑进行计算，则 Router A 能够感知到 Router B 和 Router C 之间，Router C 和 Router D 之间的链路不支持 IPv6，即不会将到达 Router D 的 IPv6 报文转发给 Router而造成报文丢弃。
B

##### 2. 配置限制和指导

当 IS-IS 网络中同时存在 IPv4 和 IPv6 拓扑时，建议用户配置此功能，否则可能导致路由计算错误。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 配置 IS-IS 开销值的类型。
cost-style { compatible | wide | wide-compatible }
缺省情况下，IS-IS 只收发采用 narrow 方式的报文。
进入 地址族视图。
(4) IPv6
address-family ipv6 [ unicast ]
配置 支持 单播拓扑。
(5) IS-IS IPv6
multi-topology [ compatible ]
缺省情况下，IS-IS 不支持 单播拓扑。
IPv6

#### 1.6 配置IS-IS路由信息控制

##### 1.6.1 配置IS-IS链路开销

###### 1. 功能简介

IS-IS 有三种方式来配置接口的链路开销值，按照选择顺序依次为：

在接口视图下为指定接口配置的链路开销值。
•在系统视图下全局配置的链路开销值，该配置将对该 IS-IS 进程关联的接口同时生效。
•
• 自动计算开销值：将根据带宽参考值自动计算接口的链路开销值。当开销值的类型为 wide或 时，可以根据公式“开销=（带宽参考值÷接口期望带宽）×10”计wide-compatible算接口的链路开销值，取值范围为 1～16777214。当开销值类型为其他类型时，具体情况如下：接口带宽≤10Mbps 时，值为 60；接口带宽≤100Mbps 时，值为 50；接口带宽≤155Mbps时，值为 40；接口带宽≤622Mbps 时，值为 30；接口带宽≤2500Mbps 时，值为 20；接口带宽>2500Mbps 时，值为 10。接口期望带宽通过命令 bandwidth 进行配置。
如果没有采用上述三种方式中的任一种进行开销值的配置，接口的链路开销值将取系统设置的缺省值 10。

###### 2. 配置IPv4 IS-IS接口的链路开销值

(1) 进入系统视图。
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) （可选）配置 IS-IS 开销值的类型。
cost-style { narrow | wide | wide-compatible | { compatible |
narrow-compatible } [ relax-spf-limit ] }
缺省情况下，IS-IS 开销值的类型为 narrow。
(4) 退回系统视图。
quit
(5) 进入接口视图。
interface interface-type interface-number
(6) 配置 IS-IS 接口的链路开销值。
isis cost cost-value [ level-1 | level-2 ]
缺省情况下，未配置 IS-IS 接口的链路开销值。

###### 3. 全局配置IPv4 IS-IS链路开销值

(1) 进入系统视图。
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 全局配置 IS-IS 的链路开销值。
circuit-cost cost-value [ level-1 | level-2 ]
缺省情况下，未全局配置 IS-IS 的链路开销值。

###### 4. 配置IPv4 IS-IS自动计算链路开销值

(1) 进入系统视图。
system-view
(2) 进入 IS-IS 视图。

isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 使能自动计算接口链路开销值功能。
auto-cost enable缺省情况下，自动计算接口链路开销值功能处于关闭状态。
(4) （可选）配置 IS-IS 自动计算链路开销值时依据的带宽参考值。
bandwidth-reference value缺省情况下，带宽参考值为 100Mbps。

###### 5. 配置IPv6 IS-IS接口的链路开销值

(1) 进入系统视图。
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) （可选）配置 IS-IS 开销值的类型。
cost-style { narrow | wide | wide-compatible | { compatible |
narrow-compatible } [ relax-spf-limit ] }
缺省情况下，IS-IS 只收发采用 narrow 方式的报文。
(4) 进入 IPv6 地址族视图。
address-family ipv6 [ unicast ]
(5) 退回 IS-IS 视图。
quit
(6) 退回系统视图。
quit
(7) 进入接口视图。
interface interface-type interface-number
(8) 使能接口 IS-IS 的 IPv6 能力。
isis ipv6 enable [ process-id ]
缺省情况下，接口上 IS-IS 的 IPv6 能力处于关闭状态。
(9) 配置接口的 IPv6 链路开销值。
isis ipv6 cost cost-value [ level-1 | level-2 ]
缺省情况下，未配置接口的 链路开销值。
IPv6

###### 6. 全局配置IPv6 IS-IS链路开销值

(1) 进入系统视图。
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
进入 地址族视图。
(3) IPv6
address-family ipv6 [ unicast ]
全局配置 的链路开销值。
(4) IPv6 IS-IS

circuit-cost cost-value [ level-1 | level-2 ]缺省情况下，未全局配置 IPv6 IS-IS 的链路开销值。

###### 7. 配置IPv6 IS-IS自动计算链路开销值

进入系统视图。
(1)
system-view进入 视图。
(2) IS-IS isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 配置 IS-IS 开销值的类型。
cost-style { wide | wide-compatible }缺省情况下，IS-IS 只收发采用 narrow 方式的报文。
(4) 进入 IPv6 地址族视图。
address-family ipv6 [ unicast ]
(5) 使能自动计算接口链路开销值功能。
auto-cost enable缺省情况下，自动计算接口链路开销值功能处于关闭状态。
(6) （可选）配置 IPv6 IS-IS 自动计算链路开销值时依据的带宽参考值。
bandwidth-reference value缺省情况下，带宽参考值为 100Mbps。

##### 1.6.2 配置IS-IS路由优先级

###### 1. 功能简介

一台路由器可同时运行多个路由协议，当多个路由协议都发现到同一目的地的路由时，将选用高优先级路由协议所发现的路由。
以下配置用来为 IS-IS 路由设置优先级，使用路由策略可以为特定的路由设置特定的优先级，路由策略的相关知识请参见“三层技术-IP 路由配置指导”中的“路由策略”。

###### 2. 配置IPv4 IS-IS路由优先级

(1) 进入系统视图。
system-view
请依次执行以下命令进入 单播地址族视图。
(2) IS-IS IPv4
isis [ process-id ] [ vpn-instance vpn-instance-name ]
address-family ipv4 [ unicast ]
配置 协议的路由优先级。
(3) IS-IS
preference { preference | route-policy route-policy-name } *
缺省情况下，IPv4 IS-IS 协议的路由优先级为 15。

###### 3. 配置IPv6 IS-IS路由优先级

进入系统视图。
(1)
system-view

###### 1. 功能简介

(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 进入 IS-IS IPv6 地址族视图。
address-family ipv6 [ unicast ]
(4) 配置 IPv6 IS-IS 路由优先级。
preference { route-policy route-policy-name | preference } *
缺省情况下，IPv6 IS-IS 路由优先级为 15。

##### 1.6.3 配置IS-IS最大等价路由条数

功能简介
1.
如果到一个目的地有几条开销相同的路径，可以通过等价路由负载分担来提高链路利用率。该配置用以设置 协议的最大等价路由条数。
IS-IS

###### 2. 配置IPv4 IS-IS最大等价路由条数

(1) 进入系统视图。
system-view
请依次执行以下命令进入 单播地址族视图。
(2) IS-IS IPv4
isis [ process-id ] [ vpn-instance vpn-instance-name ]
address-family ipv4 [ unicast ]
配置在负载分担方式下 最大等价路由条数。
(3) IS-IS
maximum load-balancing number
缺省情况下，IPv4 IS-IS 支持的等价路由的最大条数与系统支持的最大等价路由的条数相
同。

###### 3. 配置IPv6 IS-IS最大等价路由条数

(1) 进入系统视图。
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
进入 地址族视图。
(3) IS-IS IPv6
address-family ipv6 [ unicast ]
配置在负载分担方式下 等价路由的最大数量。
(4) IPv6 IS-IS
maximum load-balancing number
缺省情况下，IPv6 可用的等价路由最大条数与系统支持的最大等价路由的条数相同。
IS-IS

##### 1.6.4 配置IS-IS路由聚合

###### 1. 功能简介

通过配置路由聚合，可以减小路由表规模，还可以减少本路由器生成的 报文大小和 的LSP LSDB规模。其中，被聚合的路由可以是 IS-IS 协议发现的路由，也可以是引入的外部路由。

路由器只对本地生成的 LSP 中的路由进行聚合。

###### 2. 配置IPv4 IS-IS路由聚合

进入系统视图。
(1)
system-view请依次执行以下命令进入 单播地址族视图。
(2) IS-IS IPv4 isis [ process-id ] [ vpn-instance vpn-instance-name ] address-family ipv4 [ unicast ]
(3) 配置聚合路由。
summary ip-address { mask-length | mask } [ avoid-feedback | generate_null0_route | [ level-1 | level-1-2 | level-2 ] | tag tag ] *缺省情况下，不对路由进行聚合。
聚合后路由的开销值取所有被聚合路由中最小的开销值。

###### 3. 配置IPv6 IS-IS路由聚合

(1) 进入系统视图。
system-view
进入 视图。
(2) IS-IS
isis [ process-id ] [ vpn-instance vpn-instance-name ]
进入 地址族视图。
(3) IS-IS IPv6
address-family ipv6 [ unicast ]
配置 聚合路由。
(4) IPv6 IS-IS
summary ipv6-prefix prefix-length [ avoid-feedback |
generate_null0_route | [ level-1 | level-1-2 | level-2 ] | tag tag ] *
缺省情况下，未配置 聚合路由。
IPv6 IS-IS

##### 1.6.5 配置IS-IS发布缺省路由

###### 1. 功能简介

对于运行 IS-IS 的路由器来说，无法引入缺省路由，因此也无法通过将目的地为 0.0.0.0/0 的路径信息（即缺省路由）通过 LSP 发布给其它路由器，可以通过配置发布一条缺省路由，将目的地为
0.0.0.0/0 的路径信息通过 LSP 发布出去，其它同级别的路由器中将在自己的路由表中新增一条缺省路由。

###### 2. 配置IPv4 IS-IS发布缺省路由

(1) 进入系统视图。
system-view
(2) 请依次执行以下命令进入 IS-IS IPv4 单播地址族视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
address-family ipv4 [ unicast ]
配置 发布 或 级别的缺省路由。
(3) IS-IS Level-1 Level-2

default-route-advertise [ [ level-1 | level-1-2 | level-2 ] | route-policy route-policy-name ] *缺省情况下，IPv4 不发布 或 级别的缺省路由。
IS-IS Level-1 Level-2产生的缺省路由只被发布到同级别的路由器。

###### 3. 配置IPv6 IS-IS发布缺省路由

(1) 进入系统视图。
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
进入 地址族视图。
(3) IS-IS IPv6
address-family ipv6 [ unicast ]
配置 发布缺省路由。
(4) IPv6 IS-IS
default-route-advertise [ avoid-learning | [ level-1 | level-1-2 |
level-2 ] | route-policy route-policy-name | tag tag ] *
缺省情况下，不生成 IPv6 IS-IS 缺省路由。

##### 1.6.6 配置IS-IS引入外部路由

###### 1. 功能简介

IS-IS 将其它路由协议发现的路由当作外部路由处理。在引入其它协议路由时，可指定引入路由的缺省开销。还可以通过配置对引入路由进行过滤。
在实际组网环境中，每台路由器的性能即处理能力不同，如果在处理能力强的高端设备上引入大量外部路由，那么可能会对网络上其它低端设备的性能造成较大的冲击，网络管理员可以通过配置支持的最大引入路由条数，限制引入外部路由的条数，从而最终限制发布路由的数量。

###### 2. 配置限制和指导

只 能 引 入 路 由 表 中 状 态 为 active 的 路 由 ， 是 否 为 active 状 态 可 以 通 过 display ip routing-table protocol 命令来查看。

###### 3. 配置IPv4 IS-IS引入外部路由

(1) 进入系统视图。
system-view
(2) 请依次执行以下命令进入 IS-IS IPv4 单播地址族视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
address-family ipv4 [ unicast ]
(3) 从其它路由协议或其它 IS-IS 进程引入路由信息。
import-route bgp [ as-number ] [ allow-ibgp ] [ cost cost-value |
cost-type { external | internal } | [ level-1 | level-1-2 | level-2 ] |
route-policy route-policy-name | tag tag ] *
import-route bgp [ as-number ] [ allow- ibgp ] inherit-cost [ [ level-1 |
level-1-2 | level-2 ] | route-policy route-policy-name | tag tag ] *

import-route { direct | static } [ cost cost-value | cost-type { external | internal } | [ level-1 | level-1-2 | level-2 ] | route-policy route-policy-name | tag tag ] * import-route { direct | static } inherit-cost [ [ level-1 | level-1-2 | level-2 ] | route-policy route-policy-name | tag tag ] * import-route { isis | ospf | rip } [ process-id | all-processes ] [ allow-direct | cost cost-value | cost-type { external | internal } | [ level-1 | level-1-2 | level-2 ] | route-policy route-policy-name | tag tag ] * import-route { isis | ospf | rip } [ process-id | all-processes ] inherit-cost [ allow-direct | [ level-1 | level-1-2 | level-2 ] | route-policy route-policy-name | tag tag ] *缺省情况下，IPv4 不从其它路由协议或其它 进程引入路由信息。
IS-IS IS-IS
(4) （可选）配置引入 Level1/Level2 的 IPv4 路由最大条数。
import-route limit number引入 Level1/Level2 的 IPv4 路由最大条数为设备 IPv4 路由表的容量值。

###### 4. 配置IPv6 IS-IS引入外部路由

进入系统视图。
(1)
system-view进入 视图。
(2) IS-IS isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 进入 IS-IS IPv6 地址族视图。
address-family ipv6 [ unicast ]
(4) 配置 IPv6 IS-IS 引入外部路由信息。
import-route bgp4+ [ as-number ] [ allow-ibgp ] [ [ cost cost-value | inherit-cost ] | cost-type { external | internal } | [ level-1 | level-1-2 | level-2 ] | route-policy route-policy-name | tag tag ] * import-route { direct | static } [ [ cost cost-value | inherit-cost ] | cost-type { external | internal } | [ level-1 | level-1-2 | level-2 ] | route-policy route-policy-name | tag tag ] * import-route { isisv6 | ospfv3 | ripng } [ process-id ] [ allow-direct | [ cost cost-value | inherit-cost ] | cost-type { external | internal } | [ level-1 | level-1-2 | level-2 ] | route-policy route-policy-name | tag tag ] *缺省情况下，IPv6 IS-IS 不引入外部路由信息。
(5) （可选）配置引入 Level1/Level2 的 IPv6 路由最大条数。
import-route limit number引入 Level1/Level2 的 IPv6 路由最大条数为设备 IPv6 路由表的容量值。

###### 1. 功能简介

##### 1.6.7 配置IS-IS对接收的路由是否加入IP路由表进行过滤

功能简介
1.
运行 IS-IS 的路由器会把从邻居收到的 LSP 保存到自己维护的链路状态数据库中，使用 SPF 算法计算出以自己为根的最短路径树，并把计算好的路由信息加入到 路由表中，最终把最优路由IS-IS加入到 IP 路由表中。
通过 ACL、IP 地址前缀列表或路由策略可以对将要加入到 IP 路由表中的路由进行过滤，满足条件则加入到 IP 路由表中，否则将不能加入到 IP 路由表中。没有加入 IP 路由表的路由仍然在 IS-IS 路由表中，可以通过 LSP 发布出去。

###### 2. 配置IPv4 IS-IS对接收的路由是否加入IP路由表进行过滤

进入系统视图。
(1)
system-view
(2) 请依次执行以下命令进入 IS-IS IPv4 单播地址族视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ] address-family ipv4 [ unicast ]
(3) 配置 IS-IS 对接收的路由信息进行过滤。
filter-policy { ipv4-acl-number | prefix-list prefix-list-name | route-policy route-policy-name } import缺省情况下，IPv4 不对接收的路由信息进行过滤。
IS-IS

###### 3. 配置IPv6 IS-IS对接收的路由是否加入IPv6路由表进行过滤

进入系统视图。
(1)
system-view进入 视图。
(2) IS-IS isis [ process-id ] [ vpn-instance vpn-instance-name ]进入 地址族视图。
(3) IS-IS IPv6 address-family ipv6 [ unicast ]
(4) 配置 IPv6 IS-IS 对接收的路由进行过滤。
filter-policy { ipv6-acl-number | prefix-list prefix-list-name | route-policy route-policy-name } import缺省情况下，IPv6 不对接收的路由进行过滤。
IS-IS

##### 1.6.8 配置IS-IS对引入的路由信息进行过滤

###### 1. 功能简介

可以从其它路由协议或其它 进程引入路由信息，把它直接加入到 的路由表中并通IS-IS IS-IS IS-IS过 LSP 发布出去。
通过 ACL、IP 地址前缀列表或路由策略可以对引入的路由信息进行过滤，满足条件加入到 IS-IS 路由表中，否则将不能加入到 IS-IS 路由表中。没有加入 IS-IS 路由表的路由将不会通过 LSP 发布出去。

###### 2. 配置限制和指导

本命令一般和 import-route 命令结合使用。

###### 3. 配置IPv4 IS-IS对引入的路由信息进行过滤

(1) 进入系统视图。
system-view
(2) 请依次执行以下命令进入 IS-IS IPv4 单播地址族视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
address-family ipv4 [ unicast ]
(3) 配置 IS-IS 对引入的路由信息进行过滤。
filter-policy { ipv4-acl-number | prefix-list prefix-list-name |
route-policy route-policy-name } export [ protocol [ process-id ] ]
缺省情况下，IPv4 IS-IS 不对引入的路由信息进行过滤。

###### 4. 配置IPv6 IS-IS对引入的路由信息进行过滤

(1) 进入系统视图。
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 进入 IS-IS IPv6 地址族视图。
address-family ipv6 [ unicast ]
(4) 配置 IPv6 IS-IS 对引入的路由进行过滤。
filter-policy { ipv6-acl-number | prefix-list prefix-list-name |
route-policy route-policy-name } export [ protocol [ process-id ] ]
缺省情况下，IPv6 IS-IS 不对引入的路由信息进行过滤。

##### 1.6.9 配置IS-IS路由渗透

###### 1. 功能简介

通过 IS-IS 路由渗透功能（Level-2 to Level-1），可以将 Level-2 级别的路由信息和其他区域的 Level-1级别的路由信息渗透到 区域。
Level-1通过控制 路由渗透（Level-1 Level-2），可以控制 区域的 路由信息不向IS-IS to Level-1 IS-IS Level-2渗透，达到有效控制 Level-2 级别的路由信息的目的。

###### 2. 配置IPv4 IS-IS路由渗透

(1) 进入系统视图。
system-view
(2) 请依次执行以下命令进入 IS-IS IPv4 单播地址族视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
address-family ipv4 [ unicast ]
(3) 配置将 Level-1 区域的路由信息引入到 Level-2 区域。

###### 1. 功能简介

import-route isis level-1 into level-2 [ filter-policy { ipv4-acl-number | prefix-list prefix-list-name | route-policy route-policy-name } | tag tag ] *缺省情况下，Level-1 区域的路由信息向 Level-2 区域发布。
(4) 配置将 Level-2 区域的路由信息引入到 Level-1 区域。
import-route isis level-2 into level-1 [ filter-policy { ipv4-acl-number | prefix-list prefix-list-name | route-policy route-policy-name } | tag tag ] *缺省情况下，Level-2 区域的路由信息不向 Level-1 区域发布。

###### 3. 配置IPv6 IS-IS路由渗透

进入系统视图。
(1)
system-view进入 视图。
(2) IS-IS isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 进入 IS-IS IPv6 地址族视图。
address-family ipv6 [ unicast ]
(4) 配置从 Level-2 向 Level-1 进行路由渗透。
import-route isisv6 level-2 into level-1 [ filter-policy { ipv6-acl-number | prefix-list prefix-list-name | route-policy route-policy-name } | tag tag ] *缺省情况下，不从 Level-2 向 Level-1 进行路由渗透。
配置从 向 进行路由渗透。
(5) Level-1 Level-2 import-route isisv6 level-1 into level-2 [ filter-policy { ipv6-acl-number | prefix-list prefix-list-name | route-policy route-policy-name } | tag tag ] *缺省情况下，从 Level-1 向 Level-2 进行路由渗透。

##### 1.6.10 配置允许设备将IS-IS链路状态信息发布到BGP

功能简介
1.
本功能允许设备将链路状态信息发布到 BGP，由 BGP 向外发布，以满足需要知道链路状态信息的应用的需求。BGP 的相关内容请参见“三层技术-IP 路由配置指导”中的“BGP”。
LS

###### 2. 配置步骤

(1) 进入系统视图。
system-view
进入 视图。
(2) IS-IS
isis [ process-id ] [ vpn-instance vpn-instance-name ]
配置允许设备将 链路状态信息发布到 BGP。
(3) IS-IS
distribute bgp-ls [ instance-id id ] [ level-1 | level-2 ]

###### 3. 配置步骤

缺省情况下，不允许设备将 IS-IS 链路状态信息发布到 BGP。

#### 1.7 配置IS-IS定时器

##### 1.7.1 配置Hello报文发送时间间隔

###### 1. 功能简介

如果路由器在邻居关系保持时间内（即 Hello 报文失效数目与 Hello 报文发送时间间隔的乘积）没有收到来自邻居路由器的 Hello 报文时将宣告邻居关系失效。通过设置 Hello 报文失效数目和 Hello报文的发送时间间隔，可以调整邻居关系保持时间，即邻居路由器要花多长时间能够监测到链路已经失效并重新进行路由计算。

###### 2. 配置限制和指导

DIS 发送 Hello 报文的时间间隔是 isis timer hello 设置的时间的 1/3。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置 Hello 报文的发送时间间隔。
isis timer hello seconds [ level-1 | level-2 ]缺省情况下，Hello 报文的发送时间间隔为 10 秒。

##### 1.7.2 配置CSNP报文发送时间间隔

###### 1. 功能简介

当网络类型为广播网时，DIS 使用 CSNP 报文来进行 LSDB 同步，因此只有在被选举为 DIS 的路由器上进行该项配置才有效。

###### 2. 配置步骤

进入系统视图。
(1)
system-view进入接口视图。
(2)
interface interface-type interface-number
(3) 配置 DIS 在广播网络上发送 CSNP 报文的时间间隔。
isis timer csnp seconds [ level-1 | level-2 ]缺省情况下，CSNP 报文的发送时间间隔为 10 秒。

###### 1. 功能简介

##### 1.7.3 配置LSP最大生存时间

功能简介
1.
每个 LSP 都有一个最大生存时间，随着时间的推移最大生存时间将逐渐减小，当 LSP 的最大生存时间为 时，IS-IS 将启动清除过期 的过程。用户可根据网络规模对 的最大生存时间进行0 LSP LSP调整。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 配置 LSP 最大生存时间。
timer lsp-max-age seconds
缺省情况下，LSP 最大生存时间为 1200 秒。

##### 1.7.4 配置LSP刷新周期和LSP重新生成的时间间隔

###### 1. 功能简介

路由器必须定时刷新自己生成的 LSP，防止 LSP 的最大生存时间减小为 0。另外，通过定时刷新LSP 可以使整个区域中的 LSP 保持同步。用户可对 LSP 的刷新周期进行配置，提高 LSP 的刷新频率可以加快网络收敛速度，但是将占用更多的带宽。
除了定时刷新可以重新生成 LSP 外，当网络拓扑发生变化，如邻居路由器 up 或 down，接口 Metric值、System 或区域地址发生变化等，将触发路由器重新生成 LSP。为了防止网络拓扑频繁变化ID而导致 LSP 频繁重新生成，用户可配置 LSP 生成时间间隔，以抑制网络变化频繁导致占用过多的带宽资源和路由器资源。

###### 2. 配置限制和指导

LSP 重新生成的时间间隔的变化规则如下：
如果只指定了 maximum-interval 参数，那么 LSP 重新生成的时间间隔固定为
•maximum-interval。
如果未指定 参数，LSP 重新生成的时间间隔最大为
• incremental-interval maximum-interval，最小为 minimum-interval。
• 如果指定了 incremental-interval 参数，那么在网络变化频繁的情况下将 LSP重新生成n-2的时间间隔按照 incremental-interval×2 （n 为连续触发路由计算的次数）进行延长，最大不超过 maximum-interval。在网络变化不频繁的情况下将 LSP 重新生成时间间隔缩小到 minimum-interval。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]

(3) 配置 LSP 刷新周期。
timer lsp-refresh seconds
缺省情况下，LSP 刷新周期为 900 秒。
(4) 配置 LSP 重新生成的时间间隔。
timer lsp-generation maximum-interval [ minimum-interval
[ incremental-interval ] ] [ level-1 | level-2 ]
缺省情况下，LSP 重新生成的最大时间间隔为 5 秒，最小时间间隔为 50 毫秒，时间间隔惩罚
增量为 200 毫秒。

##### 1.7.5 配置LSP发送时间间隔

###### 1. 功能简介

当 LSDB 的内容发生变化时，IS-IS 将把发生变化的 LSP 扩散出去，用户可以对 LSP 的最小发送时间间隔进行调节。
请合理配置 LSP 发送时间间隔，当存在大量 IS-IS 接口或大量路由时，会发送大量的 LSP 报文，导致 LSP 风暴的出现。
在点到点链路上，发送的 LSP 需要得到对端的应答，否则将在指定的时间间隔内重新发送该 LSP，重传时间间隔决定了当一个 在 链路上丢失时它被重传需要等待的时间。
LSP P2P

###### 2. 配置步骤

(1) 进入系统视图。
system-view
进入接口视图。
(2)
interface interface-type interface-number
配置发送 的最小时间间隔以及一次最多可以发送的 报文数目。
(3) LSP LSP
isis timer lsp time [ count count ]
缺省情况下，LSP 的发送最小时间间隔为 毫秒，一次最多可以发送 个 报文。
33 5 LSP
(4) 配置 LSP 在点到点链路上的重传时间间隔。
isis timer retransmit seconds
缺省情况下， LSP 在点到点链路上的重传时间间隔为 5 秒。

##### 1.7.6 配置SPF参数

###### 1. 功能简介

根据本地维护的 LSDB，运行 IS-IS 协议的路由器通过 SPF 算法计算出以自己为根的最短路径树，并根据这一最短路径树决定到目的网络的下一跳。通过调节 SPF 的计算间隔，可以抑制网络频繁变化可能导致的占用过多带宽资源和路由器资源。
本命令在网络变化不频繁的情况下将连续路由计算的时间间隔缩小到 minimum-interval，而在网络变化频繁的情况下可以进行相应惩罚，增加 incremental-interval ×2 n-2 （n 为连续触发路由计算的次数），将等待时间按照配置的惩罚增量延长，最大不超过 。
maximum-interval

###### 2. 配置IPv4 SPF参数

(1) 进入系统视图。
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 配置 IPv4 IS-IS 路由计算时间间隔。
timer spf maximum-interval [ minimum-interval [ incremental-interval ] ]
缺省情况下，IPv4 IS-IS 路由计算的最大时间间隔为 5 秒，最小时间间隔为 50 毫秒，时间间
隔惩罚增量为 200 毫秒。

###### 3. 配置IPv6 SPF参数

(1) 进入系统视图。
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 进入 IPv6 地址族视图。
address-family ipv6 [ unicast ]
(4) 配置 IPv6 IS-IS 路由计算的时间间隔。
timer spf maximum-interval [ minimum-interval [ incremental-interval ] ]
缺省情况下，IPv6 IS-IS 路由计算的最大时间间隔为 5 秒，最小时间间隔为 50 毫秒，时间间
隔惩罚增量为 200 毫秒。

#### 1.8 配置IS-IS报文相关功能

##### 1.8.1 配置接口的DIS优先级

###### 1. 功能简介

在广播网络中，IS-IS 需要在所有的路由器中选举一个路由器作为 DIS。
对于 IS-IS，Level-1 和 的 是分别选举的，可以为不同级别的 选举设置不同的优先Level-2 DIS DIS级。优先级数值越高，被选中的可能性就越大。如果所有路由器的 DIS 优先级相同，将会选择 MAC地址最大的路由器作为 DIS。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置接口的 DIS 优先级。
isis dis-priority priority [ level-1 | level-2 ]
缺省情况下，接口的 DIS 优先级为 64。

###### 1. 功能简介

###### 2. 配置步骤

##### 1.8.2 配置接口的Tag值

功能简介
1.
当 cost-sytle 为 wide、wide-compatible 或 compatible 时，如果发布可达的 IP 地址前缀具有 属性，IS-IS 会将 加入到该前缀的 可达信息 中。
tag tag IP TLV

###### 2. 配置IPv4 IS-IS接口的Tag值

(1) 进入系统视图。
system-view
进入接口视图。
(2)
interface interface-type interface-number
配置接口的 值。
(3) Tag
isis tag tag
缺省情况下，未配置接口的 Tag 值。

###### 3. 配置IPv6 IS-IS接口的Tag值

进入系统视图。
(1)
system-view进入接口视图。
(2)
interface interface-type interface-number配置接口的 值。
(3) Tag isis ipv6 tag tag缺省情况下，未配置接口的 Tag 值。
只要发布可达的 IPv6 地址前缀具有 tag 属性，不管 IS-IScost-style 的类型为何，IPv6 IS-IS都会将 加入到该前缀的 可达信息 中。
tag IPv6 TLV

##### 1.8.3 配置Hello报文失效数目

###### 1. 功能简介

报文失效数目，即宣告邻居失效前 没有收到的邻居 报文的数目。
Hello IS-IS Hello如果路由器在邻居关系保持时间内（即 报文失效数目与 报文发送时间间隔的乘积）没Hello Hello有收到来自邻居路由器的 Hello 报文时将宣告邻居关系失效。通过设置 Hello 报文失效数目和 Hello报文的发送时间间隔，可以调整邻居关系保持时间，即邻居路由器要花多长时间能够监测到链路已经失效并重新进行路由计算。
在广播链路上，Level-1 和 Level-2 Hello 报文会分别发送，Hello 报文失效数目需要分别设置；在点到点链路中，Level-1 和 Level-2 的 Hello 报文是在同一个点到点 Hello 报文中发送，因此不需要指定 Level-1 或 Level-2。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入接口视图。

###### 2. 配置步骤

###### 2. 配置步骤

interface interface-type interface-number
(3) 配置 Hello 报文失效数目。
isis timer holding-multiplier value [ level-1 | level-2 ]缺省情况下，Hello 报文失效数目为 3。

##### 1.8.4 禁止接口发送和接收IS-IS报文

###### 1. 功能简介

通过禁止接口发送和接收 IS-IS 报文，禁止了该接口与相邻路由器建立邻居关系，但仍然可以把该接口直连网络的路由信息放在 中从其它接口宣告出去。由于不用建立邻居关系，可以节省带宽LSP和路由器处理时间，同时，其它路由器也可以知道到达该接口直连网络的路由信息。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 禁止接口发送和接收 IS-IS 报文。
isis silent缺省情况下，接口既发送也接收 IS-IS 报文。

##### 1.8.5 配置接口发送小型Hello报文

###### 1. 功能简介

IS-IS 协议报文直接封装在链路层报文头后面，无法实现协议报文在 IP 层的自动分片。因此，运行IS-IS 的路由器与对端路由器建立邻居关系时，会发送达到链路 MTU 大小的 Hello 报文，双方进行大小的通信协商，来保证建立邻居双方接口 的一致性，从而避免双方 大小不一致MTU MTU MTU导致较小的 PDU 可以通过，但是较大的 PDU 无法通过。
当邻居路由器双方 MTU 大小一样的时候，为了避免发送过大的 Hello 报文浪费带宽，可以配置接口发送不加入填充 CLV 的小型 Hello 报文。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置接口发送不加入填充 CLV 的小型 Hello 报文。
isis small-hello缺省情况下，接口发送标准 Hello 报文。

###### 1. 功能简介

###### 1. 功能简介

##### 1.8.6 配置LSP报文长度

功能简介
1.
IS-IS 协议报文直接封装在链路层报文头后面，无法实现协议报文在 IP 层的自动分片。
为了不影响 LSP 的正常扩散，要求同一区域内所有 IS-IS 路由器生成 LSP 报文的最大长度不能超过该区域内所有路由器 IS-IS 接口 MTU 的最小值。
如果 IS-IS 运行的区域中各 IS-IS 接口的 MTU 值不一致，建议用户对 IS-IS 生成 LSP 报文的最大长度进行配置，将同一区域内所有 路由器生成 报文的最大长度配置为该区域内所有路由器IS-IS LSP IS-IS 接口 MTU 的最小值。如果不进行配置，系统将根据当前设备 IS-IS 接口最小 MTU 值的变化而自动重启 IS-IS 进程动态调整生成 LSP 报文的最大长度，会在一定程度上影响业务的正常运行。

###### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 配置生成的 Level-1 LSP 和 Level-2 LSP 的最大长度。
lsp-length originate size [ level-1 | level-2 ]缺省情况下，生成的 Level-1 LSP 和 Level-2 LSP 的最大长度为 1497 字节。
(4) 配置可以接收 LSP 的最大长度。
lsp-length receive size缺省情况下，接收的 LSP 报文的最大长度为 1497 字节。

##### 1.8.7 配置LSP快速扩散功能

功能简介
1.
通过使能 LSP 快速扩散功能，当 LSP 发生变化而导致 SPF 重新计算时，在 SPF 重新计算前，把导致 SPF 重新计算的 LSP 快速扩散出去，将大大缩短路由器之间由于进行 LSP 同步而导致 LSDB不一致的时间，提高全网的快速收敛性能。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 配置 LSP 快速扩散功能。
flash-flood [ flood-count flooding-count | max-timer-interval
flooding-interval | [ level-1 | level-2 ] ] *
缺省情况下，LSP 快速扩散功能处于关闭状态。

##### 1.8.8 配置LSP分片扩展功能

进入系统视图。
(1)
system-view进入 视图。
(2) IS-IS isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 使能 IS-IS 进程的 LSP 分片扩展功能。
lsp-fragments-extend [ level-1 | level-1-2 | level-2 ]缺省情况下，LSP 分片扩展功能处于关闭状态。
使能分片扩展功能后，使能该 IS-IS 进程的所有接口的 MTU 不能小于 512，否则 LSP 分片扩展功能将不会生效。
配置 进程的虚拟系统 ID。
(4) IS-IS virtual-system virtual-system-id缺省情况下，未配置 IS-IS 进程的虚拟系统 ID。
为了使路由器生成扩展 LSP 分片，应至少配置一个虚拟 System ID。

#### 1.9 配置IS-IS高级功能

##### 1.9.1 配置路由收敛的优先级

###### 1. 功能简介

IS-IS 协议中，当网络拓扑发生变化时，路由要重新收敛。IS-IS 路由收敛的优先级由高到低包括：
• critical：最高优先级。
• high：高优先级。
• medium：中优先级。
• 低优先级：缺省优先级。只有主机路由的缺省优先级为中优先级。
路由收敛的优先级越高收敛的速度越快。
IS-IS

###### 2. 配置IPv4 IS-IS路由收敛的优先级

(1) 进入系统视图。
system-view
(2) 请依次执行以下命令进入 IS-IS IPv4 单播地址族视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
address-family ipv4 [ unicast ]
配置 路由收敛的优先级。请选择其中一项进行配置。
(3) IPv4 IS-IS
配置指定前缀列表的 路由收敛的优先级。
IPv4 IS-IS
(cid:123)
prefix-priority { critical | high | medium } { prefix-list
prefix-list-name | tag tag-value }
通过路由策略指定 IPv4 IS-IS 路由收敛的优先级。
(cid:123)
prefix-priority route-policy route-policy-name

缺省情况下，IPv4 IS-IS 路由收敛的优先级为低优先级。

###### 3. 配置IPv6 IS-IS路由收敛的优先级

进入系统视图。
(1)
system-view进入 视图。
(2) IS-IS isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 进入 IPv6 地址族视图。
address-family ipv6 [ unicast ]
(4) 配置 IPv6 IS-IS 路由收敛的优先级。
prefix-priority { critical | high | medium } { prefix-list prefix-list-name | tag tag-value } prefix-priority route-policy route-policy-name缺省情况下，IPv6 路由收敛的优先级为低优先级。
IS-IS

##### 1.9.2 配置LSDB过载标志位

###### 1. 功能简介

通过配置 过载标志位，IS-IS 将在其发送的 报文中把 位置位，以通知其它路由器当LSDB LSP OL前路由器发生了问题，无法正确的执行路由选择和报文转发。
当运行 IS-IS 的路由器因为内存不足或其它原因无法记录完整的 LSDB 时，将会导致区域路由的计算错误，在故障排除过程中，通过给怀疑有问题的路由器设置过载标志位，可以将其从 IS-IS 网络中暂时隔离，便于进行故障定位。

###### 2. 配置IPv4 LSDB过载标志位

进入系统视图。
(1)
system-view进入 视图。
(2) IS-IS isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 配置过载标志位。
set-overload [ on-startup [ [ start-from-nbr system-id [ timeout1 [ nbr-timeout ] ] ] | timeout2 | wait-for-bgp [ timeout3 ] ] ] [ allow { external | interlevel } * ]缺省情况下，未配置过载标志位。

###### 3. 配置IPv6 LSDB过载标志位

(1) 进入系统视图。
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 进入 IPv6 地址族视图。
address-family ipv6 [ unicast ]

(4) 配置 IPv6 拓扑的 LSDB 过载标志位。
set-overload [ on-startup [ [ start-from-nbr system-id [ timeout1
[ nbr-timeout ] ] ] | timeout2 | wait-for-bgp4+ [ timeout3 ] ] ] [ allow
{ external | interlevel } * ]
缺省情况下，未配置过载标志位。

##### 1.9.3 配置ATT连接位

###### 1. 功能简介

ATT 连接位由 L1/L2 路由器产生，但仅与 L1 LSP 有关，表示产生此 LSP 的路由器（L1/L2 路由器）
与多个区域相连接。当 L1 路由器收到 L1/L2 路由器发送的 ATT 位置 1 的 L1 LSP 时，会产生一条指向 路由器的缺省路由。
L1/L2

###### 2. 配置IS-IS不采用ATT位计算缺省路由

(1) 进入系统视图。
system-view
进入 视图。
(2) IS-IS
isis [ process-id ] [ vpn-instance vpn-instance-name ]
配置 不采用 位计算缺省路由。
(3) IS-IS ATT
ignore-att
缺省情况下，IS-IS 采用 位计算缺省路由。
ATT

###### 3. 设置系统自身发布的Level-1 LSP的ATT位

进入系统视图。
(1)
system-view进入 视图。
(2) IS-IS isis [ process-id ] [ vpn-instance vpn-instance-name ]配置系统自身发布的 的 位置位。
(3) Level-1 LSP ATT set-att { always | never }缺省情况下，系统自身发布的 Level-1 LSP 的 ATT 位不置位。只有当 L1/L2 路由器收到来自其他区域的 时，才会发送 位置位的 。
LSP ATT Level-1 LSP

##### 1.9.4 配置IS-IS主机名映射

###### 1. 功能简介

IS-IS 用 System ID 来在区域内唯一标识主机或路由器，System ID 长度固定为 6 字节。当网络管理员检查 IS-IS 邻居关系的状态、IS-IS 路由表以及 LSDB 中的内容时，十六进制表示的 System ID 以及 LSP 标识符不够直观，查看也不方便。
主机名映射提供了一种将 System ID 映射到主机名的服务，运行 IS-IS 的路由器维护一个主机名到的映射关系表，在维护和管理以及网络故障诊断时，使用主机名比使用 会更System ID System ID直观，也更容易记忆。
可以通过静态配置和动态生成两种方式生成和维护此关系映射表：

静态配置，要求网络中的每一台路由器为其它路由器配置 System ID 和主机名的映射关系。
•当网络中路由器数目增多时，网络中每新增一台路由器或修改某台路由器的主机名映射关系，其它路由器都要做相应配置，增加了维护工作量。
• 动态生成，IS-IS 网络中的每台路由器只需要在本机上配置自己的主机名称即可，配置的主机名称将通过动态主机名 CLV 发布出去，最后 IS-IS 网络中使能动态主机名映射功能的路由器都将收集到其它路由器 与主机名称的映射关系并生成映射表。同时还可以为广播System ID网中的 DIS 配置局域网名称来代表这个广播网中的伪节点，便于网络管理员查看 LSDB 内容时判断 LSP 是由哪个 DIS 产生的。

###### 2. 配置限制和指导

只有使能动态主机名映射功能后，使用 display isis lsdb 等命令才可以看到路由器的主机名而不是 ID。
System倘若网络中的一台路由器使能了动态主机名映射功能且在当前路由器也通过静态方式为那台路由器配置了主机名，动态配置的主机名将覆盖当前路由器为其静态配置的主机名称。

###### 3. 配置IS-IS静态主机名映射

(1) 进入系统视图。
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 为远端 IS 配置 System ID 与主机名称的映射关系。
is-name map sys-id map-sys-name
缺省情况下，没有为远端 IS 配置 System ID 与主机名称的映射关系。
每个 只能对应一个主机名称。
System ID

###### 4. 配置IS-IS动态主机名映射

(1) 进入系统视图。
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 使能动态主机名映射功能并为当前路由器配置主机名称。
is-name sys-name
缺省情况下，动态主机名映射功能处于关闭状态且没有为当前路由器配置主机名称。
退回系统视图。
(4)
quit
进入接口视图。
(5)
interface interface-type interface-number
(6) 配置本地局域网名称。
isis dis-name symbolic-name
缺省情况下，未配置本地局域网名称。
该命令只有在使能了动态主机名进程的路由器上有效。该命令在点到点链路的接口上无效。

###### 1. 功能简介

#### 1.10 配置IS-IS日志和告警功能

##### 1.10.1 配置邻接状态变化的输出开关

###### 1. 功能简介

打开邻接状态输出开关后，IS-IS 邻接状态变化时会生成日志信息发送到设备的信息中心，通过设置信息中心的参数，最终决定日志信息的输出规则（即是否允许输出以及输出方向）。（有关信息中心参数的配置请参见“网络管理和监控配置指导”中的“信息中心”。）

###### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 打开邻接状态变化的输出开关。
log-peer-change缺省情况下，邻接状态变化的输出开关处于打开状态。

##### 1.10.2 配置IS-IS网管功能

功能简介
1.
配置 IS-IS 进程绑定 MIB 功能后，可以通过网管软件对指定的 IS-IS 进程进行管理。
开启 IS-IS 模块的告警功能后，该模块会生成告警信息，用于报告该模块的重要事件。生成的告警信息将发送到设备的 模块，通过设置 中告警信息的发送参数，来决定告警信息输出SNMP SNMP的相关属性。（有关告警信息的详细介绍，请参见“网络管理和监控配置指导”中的“SNMP”。）

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置 IS-IS 进程绑定 MIB。
isis mib-binding process-id
缺省情况下，MIB 绑定在进程号最小的 IS-IS 进程上。
(3) 开启 IS-IS 的告警功能。
snmp-agent trap enable isis [ adjacency-state-change | area-mismatch |
authentication | authentication-type | buffsize-mismatch |
id-length-mismatch | lsdboverload-state-change | lsp-corrupt |
lsp-parse-error | lsp-size-exceeded | manual-address-drop |
max-seq-exceeded | maxarea-mismatch | own-lsp-purge | protocol-support
| rejected-adjacency | skip-sequence-number | version-skew ] *
缺省情况下，IS-IS 的告警功能处于开启状态。
(4) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]

###### 1. 功能简介

(5) 配置管理 IS-IS 的 SNMP 实体所使用的上下文名称。
snmp context-name context-name
缺省情况下，未配置管理 IS-IS 的 SNMP 实体所使用的上下文名称。

#### 1.11 配置IS-IS快速收敛

##### 1.11.1 配置ISPF

###### 1. 功能简介

ISPF（Incremental Shortest Path First，增量最短路径优先）计算是对 IS-IS 中最短路径树的增量计算，当网络的拓扑结构发生变化，即影响到最短路径树的结构时，只对受影响的部分节点进行重新计算拓扑结构，对最短路径树中受影响的部分进行修正，而不需要重建整棵最短路径树。

###### 2. 配置IPv4 IS-IS ISPF

进入系统视图。
(1)
system-view进入 视图。
(2) IS-IS isis [ process-id ] [ vpn-instance vpn-instance-name ]使能 功能。
(3) IPv4 IS-IS ISPF ispf enable缺省情况下，IPv4 IS-IS ISPF 功能处于开启状态。

###### 3. 配置IPv6 IS-IS ISPF

进入系统视图。
(1)
system-view进入 视图。
(2) IS-IS isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 进入 IPv6 地址族视图。
address-family ipv6 [ unicast ]
(4) 使能 IPv6 IS-IS ISPF 功能。
ispf enable缺省情况下，IPv6 IS-IS ISPF 功能处于开启状态。

##### 1.11.2 配置前缀抑制

功能简介
1.
接口上配置本功能后，设备将禁止在 LSP 中携带此接口的前缀，屏蔽内部节点，提高安全性，加快路由收敛。

###### 2. 配置IPv4 IS-IS前缀抑制

(1) 进入系统视图。
system-view

###### 1. 功能简介

(2) 进入接口视图。
interface interface-type interface-number
(3) 配置接口的前缀抑制功能。
isis prefix-suppression
缺省情况下，未配置接口的前缀抑制功能。
本命令对接口从地址同样生效。

###### 3. 配置IPv6 IS-IS前缀抑制

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置接口的前缀抑制功能。
isis ipv6 prefix-suppression
缺省情况下，未配置接口的前缀抑制功能。

##### 1.11.3 配置PIC

功能简介
1.
PIC（Prefix Independent Convergence，前缀无关收敛），即收敛时间与前缀数量无关，加快收敛速度。传统的路由计算快速收敛都与前缀数量相关，收敛时间与前缀数量成正比。

###### 2. 配置限制和指导

和 快速重路由功能同时配置时，IS-IS 快速重路由功能生效。
PIC IS-IS邻居发送的 才会进行 PIC。
LSP

###### 3. 使能PIC

(1) 进入系统视图。
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
使能前缀无关收敛功能。
(3)
pic [ additional-path-always ]
缺省情况下，前缀无关收敛功能处于使能状态。

###### 4. 配置PIC支持BFD检测功能（Ctrl方式）

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
使能 协议中主用链路的 BFD（Ctrl 方式）检测功能。
(3) IS-IS
isis primary-path-detect bfd ctrl

缺省情况下，IS-IS 协议中主用链路的 BFD（Ctrl 方式）检测功能处于关闭状态。
配置本功能后，可以加快 IS-IS 协议的收敛速度。使用 control 报文双向检测方式时，需要建立 邻居的两端设备均支持 配置。
IS-IS BFD

###### 5. 配置PIC支持BFD检测功能（Echo方式）

(1) 进入系统视图。
system-view
(2) 配置 BFD Echo 报文源地址。
bfd echo-source-ip ip-address
缺省情况下，未配置 报文源地址。
BFD Echo
报文的源 地址用户可以任意指定。建议配置 报文的源 地址不属于该设备任何
echo IP echo IP
一个接口所在网段。
本命令的详细情况请参见“可靠性命令参考”中的“BFD”。
(3) 进入接口视图。
interface interface-type interface-number
(4) 使能 IS-IS 协议中主用链路的 BFD（Echo 方式）检测功能。
isis primary-path-detect bfd echo
缺省情况下，IS-IS 协议中主用链路的 BFD（Echo 方式）检测功能处于关闭状态。
配置本功能后，可以加快 协议的收敛速度。使用 报文单跳检测方式时，仅需要一
IS-IS echo
端设备支持 BFD 配置。

#### 1.12 提高IS-IS网络的安全性

在安全性要求较高的网络中，可以通过配置 验证来提高 网络的安全性。IS-IS 验证特性IS-IS IS-IS分为邻居关系的验证和区域或路由域的验证。

##### 1.12.1 配置邻居关系验证

###### 1. 功能简介

配置邻居关系验证后，验证密钥将会按照设定的方式封装到 Hello 报文中，并对接收到的 Hello 报文进行验证密钥的检查，通过检查才会形成邻居关系，否则将不会形成邻居关系，用以确认邻居的正确性和有效性，防止与无法信任的路由器形成邻居。
两台路由器要形成邻居关系必须配置相同的验证方式和验证密钥。
切换密钥时可以通过配置发送报文携带验证信息，接收报文时不进行验证，实现认证密钥无缝切换。

###### 2. 配置步骤

进入系统视图。
(1)
system-view进入接口视图。
(2)
interface interface-type interface-number配置邻居关系验证方式和验证密钥。
(3)

###### 1. 功能简介

isis authentication-mode { { gca key-id { hmac-sha-1 | hmac-sha-224 | hmac-sha-256 | hmac-sha-384 | hmac-sha-512 } [ nonstandard ] | md5 | simple } { cipher | plain } string | keychain keychain-name } [ level-1 | level-2 ] [ ip | osi ]缺省情况下，接口没有配置邻居关系验证方式和验证密钥。
(4) （可选）配置对收到的 Hello 报文忽略认证信息检查。
isis authentication send-only [ level-1 | level-2 ]缺省情况下，如果配置了接口验证方式和验证密钥，对收到的报文执行认证信息检查。

##### 1.12.2 配置区域验证

功能简介
1.
通过配置区域验证，可以防止将从不可信任的路由器学习到的路由信息加入到本地 Level-1 的 LSDB中。
配置区域验证后，验证密钥将会按照设定的方式封装到 Level-1 报文（ LSP 、 CSNP 、 PSNP ）中，并对收到的 报文进行验证密钥的检查。
Level-1同一区域内的路由器必须配置相同的验证方式和验证密钥。
切换密钥时可以通过配置发送报文携带验证信息，接收报文时不进行验证，实现认证密钥无缝切换。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
进入 视图。
(2) IS-IS
isis [ process-id ] [ vpn-instance vpn-instance-name ]
配置区域验证方式和验证密钥。
(3)
area-authentication-mode { { gca key-id { hmac-sha-1 | hmac-sha-224 |
hmac-sha-256 | hmac-sha-384 | hmac-sha-512 } [ nonstandard ] | md5 |
simple } { cipher | plain } string | keychain keychain-name } [ ip | osi ]
缺省情况下，系统没有配置区域验证方式和验证密钥。
(4) （可选）配置对收到的 Level-1 报文（包括 LSP、CSNP、PSNP）忽略认证信息检查。
area-authentication send-only
缺省情况下，如果配置了区域验证方式和验证密钥，对收到的报文执行认证信息检查。

##### 1.12.3 配置路由域验证

###### 1. 功能简介

通过配置路由域验证，可以防止将不可信的路由信息注入当前路由域。
配置路由域验证后，验证密钥将会按照设定的方式封装到 Level-2 报文（ LSP 、 CSNP 、 PSNP ）中，并对收到的 Level-2 报文进行验证密钥的检查。
所有骨干层（Level-2）路由器必须配置相同的验证方式和验证密钥。
切换密钥时可以通过配置发送报文携带验证信息，接收报文时不进行验证，实现认证密钥无缝切换。

##### 1.13.1 配置IS-IS GR

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 配置路由域验证方式和验证密钥。
domain-authentication-mode { { gca key-id { hmac-sha-1 | hmac-sha-224 |
hmac-sha-256 | hmac-sha-384 | hmac-sha-512 } [ nonstandard ] | md5 |
simple } { cipher | plain } string | keychain keychain-name } [ ip | osi ]
缺省情况下，系统未配置路由域验证方式和验证密钥。
(4) （可选）配置对收到的 Level-2 报文（包括 LSP、CSNP、PSNP）忽略认证信息检查。
domain-authentication send-only
缺省情况下，如果配置了路由域验证方式和验证密钥，对收到的报文执行认证信息检查。

#### 1.13 提高IS-IS网络的可靠性

配置IS-IS
1.13.1 GR

###### 1. 功能简介

GR（Graceful Restart，平滑重启）是一种通过备份 IS-IS 配置信息，在协议重启或主备倒换时 IS-IS进行平滑重启，保持邻接关系，并对 LSDB 进行同步，从而保证转发业务不中断的机制。
GR 有两个角色：
• GR Restarter：发生协议重启或主备倒换事件且具有 GR 能力的设备。
• GR Helper：和 GR Restarter 具有邻居关系，协助完成 GR 流程的设备。
只需要在作为 GR Restarter 的设备上进行以下配置，设备缺省都是 GR Helper。
T1、T2 和 T3 定时器用来控制 GR 流程，分别如下：
• T1 定时器：用来控制发送带有 RR 标志位的 Restart TLV 的次数。重启路由器发送带有 RR 标志位的 Restart TLV，如果在超时时间内收到对端回复的带有 RA 标志的 Restart TLV，才能正常进入 GR 流程；否则 GR 流程失败。
• T2 定时器：用来控制 LSDB 同步时间。每个 LSDB 都有一个 T2 定时器，对于 Level-1-2 路由器来说，就需要有两个 定时器，一个为 的 定时器，另外一个为 的T2 Level-1 T2 Level-2 T2定时器。如果 Level-1 和 Level-2 的 T2 定时器都超时，LSDB 同步还没有完成，则 GR 失败。
• T3 定时器：用来控制路由器的重启时间间隔。重启时间间隔在 IS-IS 的 Hello PDU 中设置为保持时间，这样在该路由器重启的时间内邻居不会断掉与其的邻接关系。如果 T3 定时器超时后 GR 还没有完成，则 GR 失败。

###### 2. 配置限制和指导

配置 定时器时请遵循以下规则，否则可能会导致 失败：
GR GR定时器超时值×超时次数小于 定时器的超时值。
• T1 T2 T2 定时器超时值小于 T3 定时器的超时值。
•IS-IS GR 特性与 IS-IS NSR 特性互斥，不能同时配置。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 使能 IS-IS 路由进程，进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 使能 IS-IS 协议的 GR 能力。
graceful-restart
缺省情况下，IS-IS 协议的 GR 能力处于关闭状态。
（可选）配置重启时抑制 位。
(4) SA
graceful-restart suppress-sa
缺省情况下，重启时不抑制 位。
SA
配置重启时抑制 SA（Suppress-Advertisement）位，即在重启路由器的 中设置抑
Hello PDU
制发布 SA 位，重启路由器的邻居将继续发布该邻接关系。
(5) （可选）配置 T1 定时器。
graceful-restart t1 seconds count count
缺省情况下，T1 定时器的超时值为 秒，超时次数为 次。
3 10
（可选）配置 定时器。
(6) T2
graceful-restart t2 seconds
缺省情况下，T2 定时器的超时值为 秒。
60
（可选）配置 定时器。
(7) T3
graceful-restart t3 seconds
缺省情况下，T3 定时器的超时值为 300 秒。

##### 1.13.2 配置IS-IS NSR

###### 1. 功能简介

GR 特性存在一些缺陷，如主备倒换期间需要周边设备配合才能完成路由信息的恢复，在网络应用中有一定的限制；而且在主备倒换后 IS-IS 进程重新学习所有的路由，如果在主备倒换期间拓扑发生变化，删除的路由不能及时更新，容易造成黑洞路由。
NSR 就是为了解决 GR 特性的一些缺陷和使用场景限制而实现的一种新特性。NSR 将 IS-IS 链路状态信息从主进程备份到备进程，在发生主备倒换时不需要周边设备配合就可以完成链路状态的恢复和路由的重新生成。

###### 2. 配置限制和指导

IS-IS NSR 特性与 IS-IS GR 特性互斥，不能同时配置。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]

###### 1. 功能简介

(3) 使能 IS-IS NSR 功能。
non-stop-routing
缺省情况下，IS-IS NSR 功能处于关闭状态。
各个进程的 NSR 功能是相互独立的，只对本进程生效。如果存在多个 IS-IS 进程，建议在各
个进程下使能 功能。
IS-IS NSR

##### 1.13.3 配置IS-IS与BFD联动

###### 1. 功能简介

BFD（Bidirectional Detection，双向转发检测）能够为 邻居之间的链路提供快速Forwarding IS-IS检测功能。当邻居之间的链路出现故障时，BFD 能够快速检测到该故障，以加快 IS-IS 协议的收敛速度。关于 BFD 的介绍和基本功能配置，请参见“可靠性配置指导”中的“BFD”。

###### 2. 配置IPv4 IS-IS与BFD联动

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 指定接口上使能 BFD。
isis bfd enable
缺省情况下，IPv4 IS-IS 的 BFD 功能处于关闭状态。

###### 3. 配置IPv6 IS-IS与BFD联动

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 在指定接口上使能 IPv6 IS-IS BFD。
isis ipv6 bfd enable
缺省情况下，IPv6 IS-IS 的 BFD 功能处于关闭状态。

##### 1.13.4 配置IS-IS快速重路由

功能简介
1.
当 IS-IS 网络中的链路或某台路由器发生故障时，需要通过故障链路或故障路由器传输才能到达目的地的报文将会丢失或产生路由环路，数据流量将会中断，直到 IS-IS 根据新的拓扑网络路由收敛完毕后，被中断的流量才能恢复正常的传输。
为了尽可能缩短网络故障导致的流量中断时间，网络管理员可以配置 快速重路由功能。
IS-IS

图1-8 IS-IS 快速重路由功能示意图如 图 1-8 所示，通过在Router B上使能快速重路由功能，IS-IS将为路由计算或指定备份下一跳，当B检测到网络故障时，IS-IS会使用事先获取的备份下一跳替换失效下一跳，通过备份下一跳Router来指导报文的转发，从而大大缩短了流量中断时间。在使用备份下一跳指导报文转发的同时，IS-IS会根据变化后的网络拓扑重新计算最短路径，网络收敛完毕后，使用新计算出来的最优路由来指导报文转发。
网络管理员可以配置给所有 IS-IS 路由通过 LFA（Loop Free Alternate）算法选取备份下一跳，也可以在路由策略中指定备份下一跳，为符合过滤条件的路由指定备份下一跳。

###### 2. 配置限制和指导

IS-IS 快速重路由通过 LFA（Loop Free Alternate）算法选取备份下一跳功能与 IS-IS TE 特性互斥。

###### 3. 配置通过LFA算法选取IPv4 IS-IS的备份下一跳信息

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) （可选）禁止接口参与 LFA 计算。
isis fast-reroute lfa-backup exclude
缺省情况下，接口参与 LFA 计算，能够被选为备份接口。
(4) 退回系统视图。
quit
(5) 请依次执行以下命令进入 IS-IS IPv4 单播地址族视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
address-family ipv4 [ unicast ]
配置 支持快速重路由功能（通过 算法选取备份下一跳信息）。
(6) IS-IS LFA
fast-reroute lfa
缺省情况下，IS-IS 支持快速重路由功能处于关闭状态。

###### 4. 配置通过路由策略指定IPv4 IS-IS的备份下一跳

(1) 进入系统视图。
system-view
进入接口视图。
(2)
interface interface-type interface-number

(3) （可选）禁止接口参与 LFA 计算。
isis fast-reroute lfa-backup exclude
缺省情况下，接口参与 LFA 计算，能够被选为备份接口。
(4) 退回系统视图。
quit
(5) 请依次执行以下命令进入 IS-IS IPv4 单播地址族视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
address-family ipv4 [ unicast ]
(6) 配置 IS-IS 支持快速重路由功能（通过路由策略指定备份下一跳）。
创建路由策略，并通过 apply fast-reroute backup-interface 命令在路由策略中
(cid:123)
指定备份下一跳。
apply fast-reroute backup-interface 命令以及路由策略的相关配置，请参见
“三层技术-IP 路由配置指导”中的“路由策略”。
配置 IS-IS 支持快速重路由功能。
(cid:123)
fast-reroute route-policy route-policy-name
缺省情况下，IPv4 IS-IS 支持快速重路由功能处于关闭状态。

###### 5. 配置IPv4 IS-IS快速重路由支持BFD检测功能（Ctrl方式）

进入系统视图。
(1)
system-view进入接口视图。
(2)
interface interface-type interface-number
(3) 使能 IS-IS 协议中主用链路的 BFD（Ctrl 方式）检测功能。
isis primary-path-detect bfd ctrl缺省情况下，IPv4 IS-IS 协议中主用链路的 BFD（Ctrl 方式）检测功能处于关闭状态。
配置本功能后，可以加快 IS-IS 协议的收敛速度。使用 control 报文双向检测方式时，需要建立 邻居的两端设备均支持 配置。
IS-IS BFD

###### 6. 配置IPv4 IS-IS快速重路由支持BFD检测功能（Echo方式）

(1) 进入系统视图。
system-view
配置 报文源地址。
(2) BFD Echo
bfd echo-source-ip ip-address
缺省情况下，未配置 报文源地址。
BFD Echo
报文的源 地址用户可以任意指定。建议配置 报文的源 地址不属于该设备任何
echo IP echo IP
一个接口所在网段。
本命令的详细情况请参见“可靠性命令参考”中的“ BFD ”。
进入接口视图。
(3)
interface interface-type interface-number
使能 协议中主用链路的 BFD（Echo 方式）检测功能。
(4) IS-IS

isis primary-path-detect bfd echo缺省情况下，IPv4 IS-IS 协议中主用链路的 BFD（Echo 方式）检测功能处于关闭状态。
配置本功能后，可以加快 IS-IS 协议的收敛速度。使用 echo 报文单跳检测方式时，仅需要一端设备支持 配置。
BFD

###### 7. 配置通过LFA算法选取IPv6 IS-IS的备份下一跳信息

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
（可选）禁止接口参与 计算。
(3) LFA
isis ipv6 fast-reroute lfa-backup exclude
缺省情况下，接口参与 计算，能够被选为备份接口。
LFA
退回系统视图。
(4)
quit
(5) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
(6) 进入 IS-IS IPv6 地址族视图。
address-family ipv6 [ unicast ]
(7) 配置 IPv6 IS-IS 支持快速重路由功能（通过 LFA 算法选取备份下一跳信息）。
fast-reroute lfa
缺省情况下，IPv6 IS-IS 支持快速重路由功能处于关闭状态。

###### 8. 配置通过路由策略指定IPv6 IS-IS的备份下一跳

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) （可选）禁止接口参与 LFA 计算。
isis ipv6 fast-reroute lfa-backup exclude
缺省情况下，接口参与 LFA 计算，能够被选为备份接口。
(4) 退回系统视图。
quit
(5) 进入 IS-IS 视图。
isis [ process-id ] [ vpn-instance vpn-instance-name ]
(6) 进入 IS-IS IPv6 地址族视图。
address-family ipv6 [ unicast ]
配置 支持快速重路由功能（通过路由策略指定备份下一跳）。
(7) IPv6 IS-IS
创建路由策略，并通过 命令在路由
apply ipv6 fast-reroute backup-interface
(cid:123)
策略中指定备份下一跳。

apply ipv6 fast-reroute backup-interface 命令以及路由策略的相关配置，请参见“三层技术-IP 路由配置指导”中的“路由策略”。
配置 支持快速重路由功能。
IPv6 IS-IS (cid:123)
fast-reroute route-policy route-policy-name缺省情况下，IPv6 快速重路由功能处于关闭状态。
IS-IS

###### 9. 配置IPv6 IS-IS快速重路由支持BFD检测功能（Ctrl方式）

(1) 进入系统视图。
system-view
进入接口视图。
(2)
interface interface-type interface-number
使能 协议中主用链路的 检测功能。
(3) IPv6 IS-IS BFD
isis ipv6 primary-path-detect bfd ctrl
配置本功能后，可以加快 协议的收敛速度。使用 报文双向检测方式时，需
IPv6 IS-IS control
要建立 IPv6 IS-IS 邻居的两端设备均支持 BFD 配置。

###### 10. 配置IPv6 IS-IS快速重路由支持BFD检测功能（Echo方式）

(1) 进入系统视图。
system-view
(2) 配置 BFD Echo 报文源地址。
bfd echo-source-ipv6 ip-address
缺省情况下，未配置 BFD Echo 报文源地址。
echo 报文的源 IPv6 地址用户可以任意指定。建议配置 echo 报文的源 IP 地址不属于该设备任
何一个接口所在网段。
本命令的详细情况请参见“可靠性命令参考”中的“BFD”。
(3) 进入接口视图。
interface interface-type interface-number
(4) 使能 IPv6 IS-IS 协议中主用链路的 BFD 检测功能。
isis ipv6 primary-path-detect bfd echo
缺省情况下， IPv6 IS-IS 协议中主用链路的 BFD 检测功能（ Echo 方式）处于关闭状态。
配置本功能后，可以加 快 协议的收敛速度。使用 报文单跳检测方式时，仅需
IPv6 IS-IS echo
要一端设备支持 BFD 配置。

#### 1.14 IS-IS显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 IS-IS 的运行情况，用户可以通过查看显示信息验证配置的效果。
在用户视图下执行 reset 命令可以清除 IS-IS 进程所有的数据结构信息。

##### 1.14.1 IPv4 IS-IS显示和维护

表1-3 显示和维护IPv4 IS-IS操作 命令显示IS-IS的进程信息 display isis [ process-id ] display isis event-log graceful-restart slot显示IS-IS GR日志信息slot-number display isis event-log lsp [ level-1 | level-2 ] *显示IS-IS LSP日志信息[ process-id ] display isis event-log slot non-stop-routing显示IS-IS NSR日志信息slot-number display isis event-log spf [ ipv4 ] [ [ level-1 | level-2 ]显示IS-IS的IPv4路由计算日志信息| verbose ] * [ process-id ] display isis graceful-restart status [ level-1 |显示IS-IS协议的GR状态level-2 ] [ process-id ] display isis interface [ [ interface-type显示IS-IS的接口信息 interface-number ] [ verbose ] | statistics ] [ process-id ] display isis lsdb [ [ level-1 | level-2 ] | local | lsp-id显示IS-IS的链路状态数据库信息lspid | [ lsp-name lspname ] | verbose ] * [ process-id ]显示IS-IS链路状态数据库的统计信 display isis lsdb statistics [ level-1 | level-2 ]息 [ process-id ]显示系统ID到主机名称的映射关系display isis name-table [ process-id ]表display isis non-stop-routing status显示IS-IS的NSR状态display isis packet { csnp | hello | lsp | psnp } [ verbose ]显示IS-IS报文的统计信息[ interface-type interface-number ] [ process-id ]显示IS-IS的邻居信息 display isis peer [ statistics | verbose ] [ process-id ] display isis redistribute [ ipv4 [ ip-address显示IS-IS引入的IPv4路由信息mask-lengh ] ] [ level-1 | level-2 ] [ process-id ] display isis route [ ipv4 [ ip-address mask-length ] ]显示IS-IS的IPv4路由信息[ [ level-1 | level-2 ] | verbose ] * [ process-id ] display isis spf-tree [ ipv4 ] [ [ level-1 | level-2 ] |显示IS-IS的IPv4拓扑信息verbose ] * [ process-id ] display isis statistics [ ipv4 ] [ level-1 | level-1-2 |显示IS-IS的IPv4统计信息level-2 ] [ process-id ]显示OSI连接的信息 display osi [ slot slot-number ]显示OSI连接的报文统计信息 display osi statistics [ slot slot-number ] reset isis all graceful-restart清除IS-IS进程所有的数据结构信息 [ process-id ] [ ] reset isis event-log graceful-restart slot slot-number清除IS-IS GR的日志信息reset isis event-log graceful-restart chassis chassis-number slot slot-number

操作 命令清除IS-IS LSP日志信息 reset isis event-log lsp [ process-id ]清除IS-IS NSR的日志信息 reset isis event-log non-stop-routing slot slot-number清除IS-IS路由计算日志信息 reset isis event-log spf [ process-id ] reset isis packet [ csnp | hello | lsp | psnp ]清除IS-IS报文的统计信息 by-interface [ interface-type interface-number ] [ process-id ]清除IS-IS指定邻居的数据结构信息 reset isis peer system-id [ process-id ]清除OSI连接的报文统计信息 reset osi statistics

##### 1.14.2 IPv6 IS-IS显示和维护

表1-4 IPv6 IS-IS 显示和维护操作 命令显示IS-IS的进程信息 display isis [ process-id ] display isis event-log lsp [ level-1 | level-2 ] *显示IS-IS LSP日志信息[ process-id ] display isis event-log spf ipv6 [ [ level-1 | level-2 ] |显示IS-IS的IPv6路由计算日志信息verbose ] * [ process-id ] display isis interface [ [ interface-type显示IS-IS的接口信息 interface-number ] [ verbose ] | statistics ] [ process-id ] display isis lsdb [ [ level-1 | level-2 ] | local | lsp-id显示IS-IS的链路状态数据库信息lspid | [ lsp-name lspname ] | verbose ] * [ process-id ]显示IS-IS链路状态数据库的统计信 display isis lsdb statistics [ level-1 | level-2 ]息 [ process-id ]显示系统ID到主机名称的映射关系display isis name-table [ process-id ]表display isis packet { csnp | hello | lsp | psnp } [ verbose ]显示IS-IS报文的统计信息[ interface-type interface-number ] [ process-id ]显示IS-IS的邻居信息 display isis peer [ statistics | verbose ] [ process-id ] display isis redistribute ipv6 [ ipv6-address显示IS-IS引入的IPv6路由信息mask-length ] [ level-1 | level-2 ] [ process-id ] display isis route ipv6 [ ipv6-address ] [ [ level-1 |显示IS-IS的IPv6路由信息level-2 ] | verbose ] * [ process-id ] display isis spf-tree ipv6 [ [ level-1 | level-2 ] |显示IS-IS的IPv6拓扑信息verbose ] * [ process-id ] display isis statistics ipv6 [ level-1 | level-1-2 |显示 IS-IS 的 IPv6 统计信息level-2 ] [ process-id ]显示OSI连接的信息 display osi [ slot slot-number ]显示OSI连接的报文统计信息 display osi statistics [ slot slot-number ]

###### 1. 组网需求

操作 命令清除IS-IS进程所有的数据结构信息 reset isis all [ process-id ] [ graceful-restart ]清除IS-IS LSP日志信息 reset isis event-log lsp [ process-id ]清除IS-IS路由计算日志信息 reset isis event-log spf [ process-id ] reset isis packet [ csnp | hello | lsp | psnp ]清除IS-IS报文的统计信息 by-interface [ interface-type interface-number ] [ process-id ]清除IS-IS指定邻居的数据结构信息 reset isis peer system-id [ process-id ]清除OSI连接的报文统计信息 reset osi statistics

#### 1.15 IS-IS典型配置举例

##### 1.15.1 IS-IS基本功能配置举例

组网需求
1.
如 图 1-9 所示，Switch A、Switch B、Switch C和Switch D属于同一自治系统，要求它们之间通过IS-IS协议达到IP网络互连的目的。
Switch A 和 Switch B 为 Level-1 交换机，Switch D 为 Level-2 交换机，Switch C 作为 Level-1-2 交换机将两个区域相连。Switch A、Switch B 和 Switch C 的区域号为 10，Switch D 的区域号为 20。

###### 2. 组网图

图1-9 IS-IS 基本功能配置组网图Switch A L1 Vlan-int100
10.1.1.2/24 Vlan-int100 Vlan-int300 Vlan-int100
10.1.1.1/24
192.168.0.1/24 172.16.1.1/16 Vlan-int300 Vlan-int200
192.168.0.2/24
10.1.2.1/24 Switch D Switch C L1/L2 L2 Vlan-int200 Area 20
10.1.2.2/24 Switch B Area 10 L1

###### 3. 配置步骤

配置各接口的 地址（略）
(1) IP配置
(2) IS-IS配置 A。
\# Switch <SwitchA> system-view [SwitchA] isis 1

[SwitchA-isis-1] is-level level-1 [SwitchA-isis-1] network-entity 10.0000.0000.0001.00 [SwitchA-isis-1] quit [SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] isis enable 1 [SwitchA-Vlan-interface100] quit \# 配置 Switch B。
<SwitchB> system-view [SwitchB] isis 1 [SwitchB-isis-1] is-level level-1 [SwitchB-isis-1] network-entity 10.0000.0000.0002.00 [SwitchB-isis-1] quit [SwitchB] interface vlan-interface 200 [SwitchB-Vlan-interface200] isis enable 1 [SwitchB-Vlan-interface200] quit配置 C。
\# Switch <SwitchC> system-view [SwitchC] isis 1 [SwitchC-isis-1] network-entity 10.0000.0000.0003.00 [SwitchC-isis-1] quit [SwitchC] interface vlan-interface 100 [SwitchC-Vlan-interface100] isis enable 1 [SwitchC-Vlan-interface100] quit [SwitchC] interface vlan-interface 200 [SwitchC-Vlan-interface200] isis enable 1 [SwitchC-Vlan-interface200] quit [SwitchC] interface vlan-interface 300 [SwitchC-Vlan-interface300] isis enable 1 [SwitchC-Vlan-interface300] quit \# 配置 Switch D。
<SwitchD> system-view [SwitchD] isis 1 [SwitchD-isis-1] is-level level-2 [SwitchD-isis-1] network-entity 20.0000.0000.0004.00 [SwitchD-isis-1] quit [SwitchD] interface vlan-interface 100 [SwitchD-Vlan-interface100] isis enable 1 [SwitchD-Vlan-interface100] quit [SwitchD] interface vlan-interface 300 [SwitchD-Vlan-interface300] isis enable 1 [SwitchD-Vlan-interface300] quit

###### 4. 验证配置

\# 显示各交换机的 IS-IS LSDB 信息，查看 LSP 是否完整。
[SwitchA] display isis lsdb Database information for IS-IS(1)
---------------------------------

Level-1 Link State Database
--------------------------- LSPID Seq Num Checksum Holdtime Length ATT/P/OL
-------------------------------------------------------------------------- 0000.0000.0001.00-00* 0x00000004 0xdf5e 1096 68 0/0/0 0000.0000.0002.00-00 0x00000004 0xee4d 1102 68 0/0/0 0000.0000.0002.01-00 0x00000001 0xdaaf 1102 55 0/0/0 0000.0000.0003.00-00 0x00000009 0xcaa3 1161 111 1/0/0 0000.0000.0003.01-00 0x00000001 0xadda 1112 55 0/0/0
*-Self LSP, +-Self LSP(Extended), ATT-Attached, P-Partition, OL-Overload [SwitchB] display isis lsdb Database information for IS-IS(1)
--------------------------------- Level-1 Link State Database
--------------------------- LSPID Seq Num Checksum Holdtime Length ATT/P/OL
-------------------------------------------------------------------------- 0000.0000.0001.00-00 0x00000006 0xdb60 988 68 0/0/0 0000.0000.0002.00-00* 0x00000008 0xe651 1189 68 0/0/0 0000.0000.0002.01-00* 0x00000005 0xd2b3 1188 55 0/0/0 0000.0000.0003.00-00 0x00000014 0x194a 1190 111 1/0/0 0000.0000.0003.01-00 0x00000002 0xabdb 995 55 0/0/0
*-Self LSP, +-Self LSP(Extended), ATT-Attached, P-Partition, OL-Overload [SwitchC] display isis lsdb Database information for IS-IS(1)
--------------------------------- Level-1 Link State Database
--------------------------- LSPID Seq Num Checksum Holdtime Length ATT/P/OL
-------------------------------------------------------------------------- 0000.0000.0001.00-00 0x00000006 0xdb60 847 68 0/0/0 0000.0000.0002.00-00 0x00000008 0xe651 1053 68 0/0/0 0000.0000.0002.01-00 0x00000005 0xd2b3 1052 55 0/0/0 0000.0000.0003.00-00* 0x00000014 0x194a 1051 111 1/0/0 0000.0000.0003.01-00* 0x00000002 0xabdb 854 55 0/0/0
*-Self LSP, +-Self LSP(Extended), ATT-Attached, P-Partition, OL-Overload

Level-2 Link State Database
--------------------------- LSPID Seq Num Checksum Holdtime Length ATT/P/OL
-------------------------------------------------------------------------- 0000.0000.0003.00-00* 0x00000012 0xc93c 842 100 0/0/0 0000.0000.0004.00-00 0x00000026 0x331 1173 84 0/0/0 0000.0000.0004.01-00 0x00000001 0xee95 668 55 0/0/0
*-Self LSP, +-Self LSP(Extended), ATT-Attached, P-Partition, OL-Overload [SwitchD] display isis lsdb Database information for IS-IS(1)
--------------------------------- Level-2 Link State Database
--------------------------- LSPID Seq Num Checksum Holdtime Length ATT/P/OL
------------------------------------------------------------------------------- 0000.0000.0003.00-00 0x00000013 0xc73d 1003 100 0/0/0 0000.0000.0004.00-00* 0x0000003c 0xd647 1194 84 0/0/0 0000.0000.0004.01-00* 0x00000002 0xec96 1007 55 0/0/0
*-Self LSP, +-Self LSP(Extended), ATT-Attached, P-Partition, OL-Overload \# 显示各交换机的 IS-IS 路由信息。Level-1 交换机的路由表中应该有一条缺省路由，且下一跳为Level-1-2 交换机，Level-2 交换机的路由表中应该有所有 Level-1 和 Level-2 的路由。
[SwitchA] display isis route Route information for IS-IS(1)
------------------------------ Level-1 IPv4 Forwarding Table
----------------------------- IPv4 Destination IntCost ExtCost ExitInterface NextHop Flags
-------------------------------------------------------------------------------
10.1.1.0/24 10 NULL Vlan100 Direct D/L/-
10.1.2.0/24 20 NULL Vlan100 10.1.1.1 R/-/-
192.168.0.0/24 20 NULL Vlan100 10.1.1.1 R/-/-
0.0.0.0/0 10 NULL Vlan100 10.1.1.1 R/-/- Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down Bit Set [SwitchC] display isis route Route information for IS-IS(1)
------------------------------

Level-1 IPv4 Forwarding Table
----------------------------- IPv4 Destination IntCost ExtCost ExitInterface NextHop Flags
-------------------------------------------------------------------------------
192.168.0.0/24 10 NULL Vlan300 Direct D/L/-
10.1.1.0/24 10 NULL Vlan100 Direct D/L/-
10.1.2.0/24 10 NULL Vlan200 Direct D/L/- Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down Bit Set Level-2 IPv4 Forwarding Table
----------------------------- IPv4 Destination IntCost ExtCost ExitInterface NextHop Flags
-------------------------------------------------------------------------------
192.168.0.0/24 10 NULL D/L/-
10.1.1.0/24 10 NULL D/L/-
10.1.2.0/24 10 NULL D/L/-
172.16.0.0/16 20 NULL Vlan300 192.168.0.2 R/-/- Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down Bit Set [SwitchD] display isis route Route information for IS-IS(1)
------------------------------ Level-2 IPv4 Forwarding Table
----------------------------- IPv4 Destination IntCost ExtCost ExitInterface NextHop Flags
-------------------------------------------------------------------------------
192.168.0.0/24 10 NULL Vlan300 Direct D/L/-
10.1.1.0/24 20 NULL Vlan300 192.168.0.1 R/-/-
10.1.2.0/24 20 NULL Vlan300 192.168.0.1 R/-/-
172.16.0.0/16 10 NULL Vlan100 Direct D/L/- Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down Bit Set

##### 1.15.2 IS-IS的DIS选择配置举例

###### 1. 组网需求

如 图 1-10 所示，Switch A、Switch B、Switch C和Switch D都运行IS-IS路由协议以实现互连，它们属于同一区域 10 ，网络类型为广播网（以太网）。
Switch A 和 Switch B 是 Level-1-2 交换机，Switch C 为 Level-1 交换机，Switch D 为 Level-2 交换机。要求通过改变接口的 DIS 优先级，将 Switch A 配置为 Level-1-2 的 DIS。

###### 2. 组网图

图1-10 IS-IS 的 DIS 选择配置组网图

###### 3. 配置步骤

配置各接口的 地址（略）
(1) IP配置
(2) IS-IS配置 A。
\# Switch <SwitchA> system-view [SwitchA] isis 1 [SwitchA-isis-1] network-entity 10.0000.0000.0001.00 [SwitchA-isis-1] quit [SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] isis enable 1 [SwitchA-Vlan-interface100] quit \# 配置 Switch B。
<SwitchB> system-view [SwitchB] isis 1 [SwitchB-isis-1] network-entity 10.0000.0000.0002.00 [SwitchB-isis-1] quit [SwitchB] interface vlan-interface 100 [SwitchB-Vlan-interface100] isis enable 1 [SwitchB-Vlan-interface100] quit \# 配置 Switch C。
<SwitchC> system-view [SwitchC] isis 1 [SwitchC-isis-1] network-entity 10.0000.0000.0003.00 [SwitchC-isis-1] is-level level-1 [SwitchC-isis-1] quit [SwitchC] interface vlan-interface 100 [SwitchC-Vlan-interface100] isis enable 1 [SwitchC-Vlan-interface100] quit \# 配置 Switch D。
<SwitchD> system-view

[SwitchD] isis 1 [SwitchD-isis-1] network-entity 10.0000.0000.0004.00 [SwitchD-isis-1] is-level level-2 [SwitchD-isis-1] quit [SwitchD] interface vlan-interface 100 [SwitchD-Vlan-interface100] isis enable 1 [SwitchD-Vlan-interface100] quit \# 查看 Switch A 的 IS-IS 邻居信息。
[SwitchA] display isis peer Peer information for IS-IS(1)
---------------------------- System Id: 0000.0000.0002 Interface: Vlan-interface100 Circuit Id: 0000.0000.0003.01 State: Up HoldTime: 21s Type: L1(L1L2) PRI: 64 System Id: 0000.0000.0003 Interface: Vlan-interface100 Circuit Id: 0000.0000.0003.01 State: Up HoldTime: 27s Type: L1 PRI: 64 System Id: 0000.0000.0002 Interface: Vlan-interface100 Circuit Id: 0000.0000.0004.01 State: Up HoldTime: 28s Type: L2(L1L2) PRI: 64 System Id: 0000.0000.0004 Interface: Vlan-interface100 Circuit Id: 0000.0000.0004.01 State: Up HoldTime: 30s Type: L2 PRI: 64显示 的 接口信息。
\# Switch A IS-IS [SwitchA] display isis interface Interface information for IS-IS(1)
---------------------------------- Interface: Vlan-interface100 Index IPv4.State IPv6.State CircuitID MTU Type DIS 00001 Up Down 1 1497 L1/L2 No/No \# 显示 Switch C 的 IS-IS 接口信息。
[SwitchC] display isis interface Interface information for IS-IS(1)
---------------------------------- Interface: Vlan-interface100 Index IPv4.State IPv6.State CircuitID MTU Type DIS 00001 Up Down 1 1497 L1/L2 Yes/No \# 显示 Switch D 的 IS-IS 接口信息。
[SwitchD] display isis interface

Interface information for IS-IS(1)
---------------------------------- Interface: Vlan-interface100 Index IPv4.State IPv6.State CircuitID MTU Type DIS 00001 Up Down 1 1497 L1/L2 No/Yes从接口信息中可以看到，在使用缺省 DIS 优先级的情况下，Switch C 为 Level-1 的 DIS，Switch D 为 Level-2 的 DIS。Level-1 和 Level-2 的伪节点分别是 0000.0000.0003.01 和0000.0000.0004.01。
配置 的 优先级。
\# Switch A DIS [SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] isis dis-priority 100 [SwitchA-Vlan-interface100] quit查看 的 邻居信息。
\# Switch A IS-IS [SwitchA] display isis peer Peer information for IS-IS(1)
---------------------------- System Id: 0000.0000.0002 Interface: Vlan-interface100 Circuit Id: 0000.0000.0001.01 State: Up HoldTime: 21s Type: L1(L1L2) PRI: 64 System Id: 0000.0000.0003 Interface: Vlan-interface100 Circuit Id: 0000.0000.0001.01 State: Up HoldTime: 27s Type: L1 PRI: 64 System Id: 0000.0000.0002 Interface: Vlan-interface100 Circuit Id: 0000.0000.0001.01 State: Up HoldTime: 28s Type: L2(L1L2) PRI: 64 System Id: 0000.0000.0004 Interface: Vlan-interface100 Circuit Id: 0000.0000.0001.01 State: Up HoldTime: 30s Type: L2 PRI: 64 \# 查看 Switch A 的 IS-IS 接口信息。
[SwitchA] display isis interface Interface information for IS-IS(1)
---------------------------------- Interface: Vlan-interface100 Index IPv4.State IPv6.State CircuitID MTU Type DIS 00001 Up Down 1 1497 L1/L2 Yes/Yes从上述信息中可以看到，在改变 IS-IS 接口的 DIS 优先级后，Switch A 立即成为 Level-1-2 的DR（DIS），且伪节点是 0000.0000.0001.01。

\# 显示 Switch C 的 IS-IS 邻居和接口信息。
[SwitchC] display isis peer Peer information for IS-IS(1)
---------------------------- System Id: 0000.0000.0002 Interface: Vlan-interface100 Circuit Id: 0000.0000.0001.01 State: Up HoldTime: 25s Type: L1 PRI: 64 System Id: 0000.0000.0001 Interface: Vlan-interface100 Circuit Id: 0000.0000.0001.01 State: Up HoldTime: 7s Type: L1 PRI: 100 [SwitchC] display isis interface Interface information for IS-IS(1)
---------------------------------- Interface: Vlan-interface100 Index IPv4.State IPv6.State CircuitID MTU Type DIS 00001 Up Down 1 1497 L1/L2 No/No \# 显示 Switch D 的 IS-IS 邻居和接口信息。
[SwitchD] display isis peer Peer information for IS-IS(1)
---------------------------- System Id: 0000.0000.0001 Interface: Vlan-interface100 Circuit Id: 0000.0000.0001.01 State: Up HoldTime: 9s Type: L2 PRI: 100 System Id: 0000.0000.0002 Interface: Vlan-interface100 Circuit Id: 0000.0000.0001.01 State: Up HoldTime: 28s Type: L2 PRI: 64 [SwitchD] display isis interface Interface information for IS-IS(1)
---------------------------------- Interface: Vlan-interface100 Index IPv4.State IPv6.State CircuitID MTU Type DIS 00001 Up Down 1 1497 L1/L2 No/No

##### 1.15.3 IS-IS引入外部路由配置举例

###### 1. 组网需求

如 图 1-11 所示：
• Switch A、Switch B、Switch C 和 Switch D 属于同一自治系统，要求它们之间通过 IS-IS 协议达到 IP 网络互连的目的。

###### 2. 组网图

Switch A和Switch B为 Level-1路由器，Switch D为 Level-2路由器，Switch C作为 Level-1-2
•路由器将两个区域相连。Switch A、Switch 和 的区域号为 10，Switch 的区域号B Switch C D为 20。
• 在 Switch D 的 IS-IS 进程中引入 RIP 路由。
组网图
2.
图1-11 IS-IS 引入外部路由配置组网图

###### 3. 配置步骤

(1) 配置各接口的 IP 地址（略）
(2) 配置 IS-IS 基本功能
配置 A。
\# Switch
<SwitchA> system-view
[SwitchA] isis 1
[SwitchA-isis-1] is-level level-1
[SwitchA-isis-1] network-entity 10.0000.0000.0001.00
[SwitchA-isis-1] quit
[SwitchA] interface vlan-interface 100
[SwitchA-Vlan-interface100] isis enable 1
[SwitchA-Vlan-interface100] quit
\# 配置 Switch B。
<SwitchB> system-view
[SwitchB] isis 1
[SwitchB-isis-1] is-level level-1
[SwitchB-isis-1] network-entity 10.0000.0000.0002.00
[SwitchB-isis-1] quit
[SwitchB] interface vlan-interface 200
[SwitchB-Vlan-interface200] isis enable 1
[SwitchB-Vlan-interface200] quit
\# 配置 Switch C。
<SwitchC> system-view
[SwitchC] isis 1
[SwitchC-isis-1] network-entity 10.0000.0000.0003.00

[SwitchC-isis-1] quit [SwitchC] interface vlan-interface 200 [SwitchC-Vlan-interface200] isis enable 1 [SwitchC-Vlan-interface200] quit [SwitchC] interface vlan-interface 100 [SwitchC-Vlan-interface100] isis enable 1 [SwitchC-Vlan-interface100] quit [SwitchC] interface vlan-interface 300 [SwitchC-Vlan-interface300] isis enable 1 [SwitchC-Vlan-interface300] quit \# 配置 Switch D。
<SwitchD> system-view [SwitchD] isis 1 [SwitchD-isis-1] is-level level-2 [SwitchD-isis-1] network-entity 20.0000.0000.0004.00 [SwitchD-isis-1] quit [SwitchD] interface interface vlan-interface 300 [SwitchD-Vlan-interface300] isis enable 1 [SwitchD-Vlan-interface300] quit [SwitchD] interface interface vlan-interface 400 [SwitchD-Vlan-interface400] isis enable 1 [SwitchD-Vlan-interface400] quit \# 显示各路由器的 IS-IS 路由信息。
[SwitchA] display isis route Route information for IS-IS(1)
------------------------------ Level-1 IPv4 Forwarding Table
----------------------------- IPv4 Destination IntCost ExtCost ExitInterface NextHop Flags
-------------------------------------------------------------------------------
10.1.1.0/24 10 NULL VLAN100 Direct D/L/-
10.1.2.0/24 20 NULL VLAN100 10.1.1.1 R/-/-
192.168.0.0/24 20 NULL VLAN100 10.1.1.1 R/-/-
0.0.0.0/0 10 NULL VLAN100 10.1.1.1 R/-/- Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down Bit Set [SwitchC] display isis route Route information for IS-IS(1)
------------------------------ Level-1 IPv4 Forwarding Table
----------------------------- IPv4 Destination IntCost ExtCost ExitInterface NextHop Flags

-------------------------------------------------------------------------------
10.1.1.0/24 10 NULL VLAN100 Direct D/L/-
10.1.2.0/24 10 NULL VLAN200 Direct D/L/-
192.168.0.0/24 10 NULL VLAN300 Direct D/L/-
Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down Bit Set
Level-2 IPv4 Forwarding Table
-----------------------------
IPv4 Destination IntCost ExtCost ExitInterface NextHop Flags
-------------------------------------------------------------------------------
10.1.1.0/24 10 NULL D/L/-
10.1.2.0/24 10 NULL D/L/-
192.168.0.0/24 10 NULL D/L/-
Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down Bit Set
[SwitchD] display isis route
Route information for IS-IS(1)
------------------------------
Level-2 IPv4 Forwarding Table
-----------------------------
IPv4 Destination IntCost ExtCost ExitInterface NextHop Flags
-------------------------------------------------------------------------------
192.168.0.0/24 10 NULL VLAN300 Direct D/L/-
10.1.1.0/24 20 NULL VLAN300 192.168.0.1 R/-/-
10.1.2.0/24 20 NULL VLAN300 192.168.0.1 R/-/-
Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down Bit Set
(3) 在 Switch D 和 Switch E 之间运行 RIPv2，在 Switch D 上配置 IS-IS 进程引入 RIP 路由。
在 上配置 RIPv2。
\# Switch D
[SwitchD] rip 1
[SwitchD-rip-1] network 10.0.0.0
[SwitchD-rip-1] version 2
[SwitchD-rip-1] undo summary
\# 在 Switch E 上配置 RIPv2。
[SwitchE] rip 1
[SwitchE-rip-1] network 10.0.0.0
[SwitchE-rip-1] version 2
[SwitchE-rip-1] undo summary
\# 在 Switch D 上配置 IS-IS 进程引入 RIP 进程的路由。
[SwitchD-rip-1] quit
[SwitchD] isis 1
[SwitchD–isis-1] address-family ipv4

[SwitchD–isis-1-ipv4] import-route rip level-2 \# 显示 Switch C 的 IS-IS 路由信息。
[SwitchC] display isis route Route information for IS-IS(1)
------------------------------ Level-1 IPv4 Forwarding Table
----------------------------- IPv4 Destination IntCost ExtCost ExitInterface NextHop Flags
-------------------------------------------------------------------------------
10.1.1.0/24 10 NULL VLAN100 Direct D/L/-
10.1.2.0/24 10 NULL VLAN200 Direct D/L/-
192.168.0.0/24 10 NULL VLAN300 Direct D/L/- Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down Bit Set Level-2 IPv4 Forwarding Table
----------------------------- IPv4 Destination IntCost ExtCost ExitInterface NextHop Flags
-------------------------------------------------------------------------------
10.1.1.0/24 10 NULL D/L/-
10.1.2.0/24 10 NULL D/L/-
192.168.0.0/24 10 NULL D/L/-
10.1.4.0/24 20 NULL VLAN300 192.168.0.2 R/L/-
10.1.5.0/24 10 0 VLAN300 192.168.0.2 R/L/-
10.1.6.0/24 10 0 VLAN300 192.168.0.2 R/L/- Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down Bit Set

##### 1.15.4 IS-IS验证配置举例

###### 1. 组网需求

如 图 所示，Switch A、Switch B、Switch C和Switch D属于同一路由域，要求它们之间通过IS-IS 1-12协议达到IP网络互连的目的。
其中，Switch A、Switch B 和 Switch C 属于同一个区域，区域号为 10，Switch D 属于另外一个区域，区域号为 20。
在区域 10 内配置区域验证，防止不可信任的路由信息加入到区域 10 的 LSDB 中；在 Switch C 和Switch D 上配置路由域验证，防止将不可信的路由信息注入当前路由域；分别在 Switch A、Switch
B、Switch 和 上配置邻居关系验证。
C Switch D

###### 2. 组网图

图1-12 IS-IS 验证配置举例图

###### 3. 配置步骤

配置各接口的 地址（略）
(1) IP配置 基本功能
(2) IS-IS配置 A。
\# Switch <SwitchA> system-view [SwitchA] isis 1 [SwitchA-isis-1] network-entity 10.0000.0000.0001.00 [SwitchA-isis-1] quit [SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] isis enable 1 [SwitchA-Vlan-interface100] quit \# 配置 Switch B。
<SwitchB> system-view [SwitchB] isis 1 [SwitchB-isis-1] network-entity 10.0000.0000.0002.00 [SwitchB-isis-1] quit [SwitchB] interface vlan-interface 200 [SwitchB-Vlan-interface200] isis enable 1 [RouterB--Vlan-interface200] quit \# 配置 Switch C。
<SwitchC> system-view [SwitchC] isis 1 [SwitchC-isis-1] network-entity 10.0000.0000.0003.00 [SwitchC-isis-1] quit [SwitchC] interface vlan-interface 200 [SwitchC-Vlan-interface200] isis enable 1 [SwitchC-Vlan-interface200] quit [SwitchC] interface vlan-interface 300 [SwitchC-Vlan-interface300] isis enable 1 [SwitchC-Vlan-interface300] quit

[SwitchC] interface vlan-interface 300 [SwitchC-Vlan-interface300] isis enable 1 [SwitchC-Vlan-interface300] quit \# 配置 Switch D。
<SwitchD> system-view [SwitchD] isis 1 [SwitchD-isis-1] network-entity 20.0000.0000.0001.00 [SwitchD-isis-1] quit [SwitchD] interface vlan-interface 300 [SwitchD-Vlan-interface300] isis enable 1 [SwitchD-Vlan-interface300] quit
(3) 在 Switch A、Switch B、Switch C 和 Switch D 之间建立邻居关系验证\# 分别在 Switch A 的 Vlan-interface100、Switch C 的 Vlan-interface100 配置邻居关系验证，验证方式为 MD5 明文，验证密钥为“eRg”。
[SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] isis authentication-mode md5 plain eRg [SwitchA-Vlan-interface100] quit [SwitchC] interface vlan-interface 100 [SwitchC-Vlan-interface100] isis authentication-mode md5 plain eRg [SwitchC-Vlan-interface100] quit \# 分别在 Switch B 的 Vlan-interface200、Switch C 的 Vlan-interface200 上配置邻居关系验证，验证方式为 明文，验证密钥为“t5Hr”。
MD5 [SwitchB] interface vlan-interface 200 [SwitchB-Vlan-interface200] isis authentication-mode md5 plain t5Hr [SwitchB-Vlan-interface200] quit [SwitchC] interface vlan-interface 200 [SwitchC-Vlan-interface200] isis authentication-mode md5 plain t5Hr [SwitchC-Vlan-interface200] quit \# 分别在 Switch C 的 Vlan-interface300、Switch D 的 Vlan-interface300 配置邻居关系验证，验证方式为 MD5 明文，验证密钥为“hSec”。
[SwitchC] interface vlan-interface 300 [SwitchC-Vlan-interface300] isis authentication-mode md5 plain hSec [SwitchC-Vlan-interface300] quit [SwitchD] interface vlan-interface 300 [SwitchD-Vlan-interface300] isis authentication-mode md5 plain hSec [SwitchD-Vlan-interface300] quit在 A、Switch 和 上配置区域验证，验证方式为 明文验证，验证密钥
(4) Switch B Switch C MD5为“10Sec”。
[SwitchA] isis 1 [SwitchA-isis-1] area-authentication-mode md5 plain 10Sec [SwitchA-isis-1] quit [SwitchB] isis 1 [SwitchB-isis-1] area-authentication-mode md5 plain 10Sec [SwitchB-isis-1] quit [SwitchC] isis 1 [SwitchC-isis-1] area-authentication-mode md5 plain 10Sec

###### 2. 组网图

###### 3. 配置步骤

[SwitchC-isis-1] quit
(5) 在 Switch C 和 Switch D 上配置路由域验证，验证方式为 MD5 明文验证，验证密钥为“1020Sec”。
[SwitchC] isis 1 [SwitchC-isis-1] domain-authentication-mode md5 plain 1020Sec [SwitchC-isis-1] quit [SwitchD] isis 1 [SwitchD-isis-1] domain-authentication-mode md5 plain 1020Sec

##### 1.15.5 IS-IS GR配置举例

###### 1. 组网需求

如 图 1-13 所示，Switch A、Switch B和Switch C属于同一域。这三台交换机都运行IS-IS协议以实现路由互连。
组网图
2.
图1-13 IS-IS GR 配置组网图配置步骤
3.
(1) 配置各交换机接口的 IP 地址和 IS-IS 协议请按照 图 1-13 配置各接口的IP地址和子网掩码，具体配置过程略。
配置各交换机之间采用 IS-IS 协议进行互连，确保 Switch A、Switch B 和 Switch C 之间能够在网络层互通，并且各交换机之间能够借助 IS-IS协议实现动态路由更新，具体配置过程略。
(2) 配置 IS-IS GR \# 使能 Switch A 的 IS-IS 协议的 GR 能力。
<SwitchA> system-view [SwitchA] isis 1 [SwitchA-isis-1] graceful-restart [SwitchA-isis-1] return

###### 4. 验证配置

\# 重启 Switch A 的 IS-IS 进程。
<SwitchA> reset isis all 1 graceful-restart Reset IS-IS process? [Y/N]:y \# 查看 Switch A 上 IS-IS 协议的 GR 状态。
<SwitchA> display isis graceful-restart status

Restart information for IS-IS(1)
-------------------------------- Restart status: COMPLETE Restart phase: Finish Restart t1: 3, count 10; Restart t2: 60; Restart t3: 300 SA Bit: supported Level-1 restart information
--------------------------- Total number of interfaces: 1 Number of waiting LSPs: 0 Level-2 restart information
--------------------------- Total number of interfaces: 1 Number of waiting LSPs: 0

##### 1.15.6 IS-IS NSR配置举例

###### 1. 组网需求

如 图 1-14 所示，Switch S、Switch A、Switch B属于同一IS-IS区域，通过IS-IS协议实现网络互连。
要求对Switch S进行主备倒换时，Switch A和Switch B到Switch S的邻居没有中断，Switch A到Switch B的流量没有中断。

###### 2. 组网图

图1-14 配置组网图IS-IS NSR

###### 3. 配置步骤

(1) 配置各路由器接口的 IP 地址和 IS-IS 协议
请按照 图 1-14 配置各接口的IP地址和子网掩码，具体配置过程略。
配置各路由器之间采用 IS-IS 协议进行互连，确保 Switch S、Switch A 和 Switch B 之间能够
在网络层互通，并且各路由器之间能够借助 IS-IS协议实现动态路由更新。具体配置过程略。
配置
(2) IS-IS NSR
\# 使能 Switch A 的 IS-IS NSR 功能。
<SwitchS> system-view
[SwitchS] isis 1
[SwitchS-isis-1] non-stop-routing
[SwitchS-isis-1] return

###### 4. 验证配置

\# Switch S 进行主备倒换。
<SwitchS> system-view [SwitchS] placement reoptimize Predicted changes to the placement Program Current location New location
--------------------------------------------------------------------- rib 0/0 0/0 staticroute 0/0 0/0 rib6 0/0 0/0 staticroute6 0/0 0/0 isis 0/0 0/0 Continue? [y/n]:y Re-optimization of the placement start. You will be notified on completion Re-optimization of the placement complete. Use 'display placement' to view the n ew placement \# 查看 Switch A 上 IS-IS 协议的邻居和路由。
<SwitchA> display isis peer Peer information for IS-IS(1)
---------------------------- System Id: 0000.0000.0001 Interface: vlan100 Circuit Id: 0000.0000.0001.01 State: Up HoldTime: 25s Type: L1(L1L2) PRI: 64 System Id: 0000.0000.0001 Interface: vlan100 Circuit Id: 0000.0000.0001.01 State: Up HoldTime: 27s Type: L2(L1L2) PRI: 64 <SwitchA> display isis route Route information for IS-IS(1)
----------------------------- Level-1 IPv4 Forwarding Table
----------------------------- IPv4 Destination IntCost ExtCost ExitInterface NextHop Flags
-------------------------------------------------------------------------------
12.12.12.0/24 10 NULL vlan100 Direct D/L/-
22.22.22.22/32 10 NULL Loop0 Direct D/-/-
14.14.14.0/32 10 NULL vlan100 12.12.12.2 R/L/-
44.44.44.44/32 10 NULL vlan100 12.12.12.2 R/L/- Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down Bit Set Level-2 IPv4 Forwarding Table

-----------------------------
IPv4 Destination IntCost ExtCost ExitInterface NextHop Flags
-------------------------------------------------------------------------------
12.12.12.0/24 10 NULL vlan100 Direct D/L/-
22.22.22.22/32 10 NULL Loop0 Direct D/-/-
14.14.14.0/32 10 NULL
44.44.44.44/32 10 NULL
Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down Bit Set
\# 查看 Switch B 上 IS-IS 协议的邻居和路由。
<SwitchB> display isis peer
Peer information for IS-IS(1)
----------------------------
System Id: 0000.0000.0001
Interface: vlan200 Circuit Id: 0000.0000.0001.01
State: Up HoldTime: 25s Type: L1(L1L2) PRI: 64
System Id: 0000.0000.0001
Interface: vlan200 Circuit Id: 0000.0000.0001.01
State: Up HoldTime: 27s Type: L2(L1L2) PRI: 64
<SwitchB> display isis route
Route information for IS-IS(1)
-----------------------------
Level-1 IPv4 Forwarding Table
-----------------------------
IPv4 Destination IntCost ExtCost ExitInterface NextHop Flags
-------------------------------------------------------------------------------
14.14.14.0/24 10 NULL vlan200 Direct D/L/-
44.44.44.44/32 10 NULL Loop0 Direct D/-/-
12.12.12.0/32 10 NULL vlan200 14.14.14.4 R/L/-
22.22.22.22/32 10 NULL vlan200 14.14.14.4 R/L/-
Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down Bit Set
Level-2 IPv4 Forwarding Table
-----------------------------
IPv4 Destination IntCost ExtCost ExitInterface NextHop Flags
-------------------------------------------------------------------------------
14.14.14.0/24 10 NULL vlan200 Direct D/L/-
44.44.44.44/32 10 NULL Loop0 Direct D/-/-
12.12.12.0/32 10 NULL

###### 2. 组网图

22.22.22.22/32 10 NULL
Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down Bit Set
通过上面信息可以看出 Switch A 和 Switch B 的邻居和路由信息保持不变，即 NSR 特性使周边设备
无法感知 的主备倒换。
Switch S

##### 1.15.7 IS-IS与BFD联动配置举例

###### 1. 组网需求

• Switch A、Switch B 和 Switch C 上运行 IS-IS，网络层相互可达。
• 当 Switch A 和 Switch B 通过 L2 Switch 通信的链路出现故障时 BFD 能够快速感知通告 IS-IS
协议，并且切换到 Switch C 进行通信。
组网图
2.
图1-15 IS-IS 与 BFD 联动配置组网图

| 接口 | IP地址 | 设备 | 接口 |
|---|---|---|---|
| Vlan-int10 | 10.1.0.102/24 | Switch B | Vlan-int10 |
| Vlan-int11 | 11.1.1.1/24 |  | Vlan-int13 |
| Loop0 | 121.1.1.1/32 |  | Loop0 |
| Vlan-int11 | 11.1.1.2/24 |  |  |
| Vlan-int13 | 13.1.1.2/24 |  |  |

设备 IP地址Switch A 10.1.0.100/24
13.1.1.1/24
120.1.1.1/32 Switch C

###### 3. 配置步骤

(1) 配置各接口的 IP 地址（略）
(2) 配置 IS-IS 基本功能
\# 配置 Switch A。
<SwitchA> system-view
[SwitchA] isis
[SwitchA-isis-1] network-entity 10.0000.0000.0001.00
[SwitchA-isis-1] quit
[SwitchA] interface loopback 0
[SwitchA-LoopBack0] isis enable

[SwitchA-LoopBack0] quit [SwitchA] interface vlan-interface 10 [SwitchA-Vlan-interface10] isis enable [SwitchA-Vlan-interface10] quit [SwitchA] interface vlan-interface 11 [SwitchA-Vlan-interface11] isis enable [SwitchA-Vlan-interface11] quit \# 配置 Switch B。
<SwitchB> system-view [SwitchB] isis [SwitchB-isis-1] network-entity 10.0000.0000.0002.00 [SwitchB-isis-1] quit [SwitchB] interface loopback 0 [SwitchB-LoopBack0] isis enable [SwitchB-LoopBack0] quit [SwitchB] interface vlan-interface 10 [SwitchB-Vlan-interface10] isis enable [SwitchB-Vlan-interface10] quit [SwitchB] interface vlan-interface 13 [SwitchB-Vlan-interface13] isis enable [SwitchB-Vlan-interface13] quit配置 C。
\# Switch <SwitchC> system-view [SwitchC] isis [SwitchC-isis-1] network-entity 10.0000.0000.0003.00 [SwitchC-isis-1] quit [SwitchC] interface vlan-interface 11 [SwitchC-Vlan-interface11] isis enable [SwitchC-Vlan-interface11] quit [SwitchC] interface vlan-interface 13 [SwitchC-Vlan-interface13] isis enable [SwitchC-Vlan-interface13] quit
(3) 配置 BFD 功能\# 在 Switch A 上使能 BFD 检测功能，并配置 BFD 参数。
[SwitchA] bfd session init-mode passive [SwitchA] interface vlan-interface 10 [SwitchA-Vlan-interface10] isis bfd enable [SwitchA-Vlan-interface10] bfd min-receive-interval 500 [SwitchA-Vlan-interface10] bfd min-transmit-interval 500 [SwitchA-Vlan-interface10] bfd detect-multiplier 7 \# 在 Switch B 上使能 BFD 检测功能，并配置 BFD 参数。
[SwitchB] bfd session init-mode active [SwitchB] interface vlan-interface 10 [SwitchB-Vlan-interface10] isis bfd enable [SwitchB-Vlan-interface10] bfd min-receive-interval 500 [SwitchB-Vlan-interface10] bfd min-transmit-interval 500 [SwitchB-Vlan-interface10] bfd detect-multiplier 8

[SwitchB-Vlan-interface10] return

###### 4. 验证配置

下面以 Switch A 为例，Switch B 和 Switch A 类似，不再赘述。
\# 显示 Switch A 的 BFD 信息。
<SwitchA> display bfd session Total Session Num: 1 Up Session Num: 1 Init Mode: Active IPv4 session working in ctrl packet mode:
LD/RD SourceAddr DestAddr State Holdtime Interface 3/1 192.168.0.102 192.168.0.100 Up 1700ms Vlan10在 上查看 的路由信息，可以看出 和 是通过\# Switch A 120.1.1.1/32 Switch A Switch B L2 Switch进行通信的。
<SwitchA> display ip routing-table 120.1.1.1 verbose Summary Count : 1 Destination: 120.1.1.1/32 Protocol: IS_L1 Process ID: 1 SubProtID: 0x1 Age: 04h20m37s Cost: 10 Preference: 10 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0x2 OrigAs: 0 NibID: 0x26000002 LastAs: 0 AttrID: 0xffffffff Neighbor: 0.0.0.0 Flags: 0x1008c OrigNextHop: 192.168.0.100 Label: NULL RealNextHop: 192.168.0.100 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: Vlan-interface10 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0当 和 通过 通信的链路出现故障时：
Switch A Switch B L2 Switch \# 在 Switch A 上查看 120.1.1.1/32 的路由信息，可以看出 Switch A 和 Switch B 已经切换到 Switch C 进行通信。
<SwitchA> display ip routing-table 120.1.1.1 verbose Summary Count : 1 Destination: 120.1.1.1/32 Protocol: IS_L1 Process ID: 1

SubProtID: 0x1 Age: 04h20m37s Cost: 20 Preference: 10 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0x2 OrigAs: 0 NibID: 0x26000002 LastAs: 0 AttrID: 0xffffffff Neighbor: 0.0.0.0 Flags: 0x1008c OrigNextHop: 10.1.1.100 Label: NULL RealNextHop: 10.1.1.100 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: Vlan-interface11 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0

##### 1.15.8 IS-IS快速重路由配置举例

###### 1. 组网需求

如 图 所示，Switch A、Switch B和Switch C属于同一IS-IS路由域，通过IS-IS协议实现网络互1-16连。要求当Switch A和Switch B之间的链路出现故障时，业务可以快速切换到链路B上。

###### 2. 组网图

图1-16 IS-IS 快速重路由配置组网图

| 接口 | IP地址 | 设备 | 接口 |
|---|---|---|---|
| Vlan-int100 | 12.12.12.1/24 | Switch B | Vlan-int101 |
| Vlan-int200 | 13.13.13.1/24 |  | Vlan-int200 |
| Loop0 | 1.1.1.1/32 |  | Loop0 |
| Vlan-int100 | 12.12.12.2/24 |  |  |
| Vlan-int101 | 24.24.24.2/24 |  |  |

设备 IP地址Switch A 24.24.24.4/24
13.13.13.2/24
4.4.4.4/32 Switch C

###### 3. 配置步骤

(1) 配置各交换机接口的 IP 地址和 IS-IS 协议
请按照 图 1-13 配置各接口的IP地址和子网掩码，具体配置过程略。
配置各交换机之间采用 IS-IS 协议进行互连，确保 Switch A、Switch B 和 Switch C 之间能够
在网络层互通，并且各交换机之间能够借助 协议实现动态路由更新。
IS-IS

具体配置过程略。
(2) 配置 IS-IS 快速重路由IS-IS 支持快速重路由配置有两种配置方法，一种是通过 LFA（Loop Free Alternate）算法选取备份下一跳，另一种是在路由策略中指定备份下一跳，两种方法任选一种。
方法一：使能 和 的 协议的自动计算快速重路由能力Switch A Switch B IS-IS配置 A。
\# Switch <SwitchA> system-view [SwitchA] isis 1 [SwitchA-isis-1] address-family ipv4 [SwitchA-isis-1-ipv4] fast-reroute lfa [SwitchA-isis-1-ipv4] quit [SwitchA-isis-1] quit \# 配置 Switch B。
<SwitchB> system-view [SwitchB] isis 1 [SwitchB-isis-1] address-family ipv4 [SwitchB-isis-1-ipv4] fast-reroute lfa [SwitchB-isis-1-ipv4] quit [SwitchB-isis-1] quit方法二：使能 Switch A 和 Switch B 的 IS-IS 协议的指定路由策略快速重路由能力\# 配置 Switch A。
<SwitchA> system-view [SwitchA] ip prefix-list abc index 10 permit 4.4.4.4 32 [SwitchA] route-policy frr permit node 10 [SwitchA-route-policy-frr-10] if-match ip address prefix-list abc [SwitchA-route-policy-frr-10] apply fast-reroute backup-interface vlan-interface 100 backup-nexthop 12.12.12.2 [SwitchA-route-policy-frr-10] quit [SwitchA] isis 1 [SwitchA-isis-1] address-family ipv4 [SwitchA-isis-1-ipv4] fast-reroute route-policy frr [SwitchA-isis-1-ipv4] quit [SwitchA-isis-1] quit配置 B。
\# Switch <SwitchB> system-view [SwitchB] ip prefix-list abc index 10 permit 1.1.1.1 32 [SwitchB] route-policy frr permit node 10 [SwitchB-route-policy-frr-10] if-match ip address prefix-list abc [SwitchB-route-policy-frr-10] apply fast-reroute backup-interface vlan-interface 101 backup-nexthop 24.24.24.2 [SwitchB-route-policy-frr-10] quit [SwitchB] isis 1 [SwitchB-isis-1] address-family ipv4 [SwitchB-isis-1-ipv4] fast-reroute route-policy frr [SwitchB-isis-1-ipv4] quit [SwitchB-isis-1] quit

###### 4. 验证配置

\# 在 Switch A 上查看 4.4.4.4/32 路由，可以看到备份下一跳信息。
[SwitchS] display ip routing-table 4.4.4.4 verbose Summary Count : 1 Destination: 4.4.4.4/32 Protocol: IS_L1 Process ID: 1 SubProtID: 0x1 Age: 04h20m37s Cost: 10 Preference: 10 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0x2 OrigAs: 0 NibID: 0x26000002 LastAs: 0 AttrID: 0xffffffff Neighbor: 0.0.0.0 Flags: 0x1008c OrigNextHop: 13.13.13.2 Label: NULL RealNextHop: 13.13.13.2 BkLabel: NULL BkNextHop: 12.12.12.2 Tunnel ID: Invalid Interface: Vlan-interface200 BkTunnel ID: Invalid BkInterface: Vlan-interface100 FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0在 上查看 路由，可以看到备份下一跳信息。
\# Switch B 1.1.1.1/32 [SwitchD] display ip routing-table 1.1.1.1 verbose Summary Count : 1 Destination: 1.1.1.1/32 Protocol: IS_L1 Process ID: 1 SubProtID: 0x1 Age: 04h20m37s Cost: 10 Preference: 10 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0x2 OrigAs: 0 NibID: 0x26000002 LastAs: 0 AttrID: 0xffffffff Neighbor: 0.0.0.0 Flags: 0x1008c OrigNextHop: 13.13.13.1 Label: NULL RealNextHop: 13.13.13.1 BkLabel: NULL BkNextHop: 24.24.24.2 Tunnel ID: Invalid Interface: Vlan-interface200 BkTunnel ID: Invalid BkInterface: Vlan-interface101 FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0

###### 3. 配置步骤

#### 1.16 IPv6 IS-IS典型配置举例

##### 1.16.1 IPv6 IS-IS基本组网配置举例

###### 1. 组网需求

如下图所示，Switch A、Switch B、Switch C 和 Switch D 属于同一自治系统，所有交换机已使能了IPv6 能力，要求它们之间通过 IPv6 IS-IS 协议达到 IPv6 网络互连的目的。
其中 Switch A 和 Switch B 是 Level-1 交换机，Switch D 是 Level-2 交换机，Switch C 是 Level-1-2交换机。Switch A、Switch B 和 Switch C 属于区域 10，而 Switch D 属于区域 20。

###### 2. 组网图

图1-17 IPv6 IS-IS 基本配置组网图配置步骤
3.
(1) 配置各接口的 IPv6 地址（略）
(2) 配置 IPv6 IS-IS \# 配置 Switch A。
<SwitchA> system-view [SwitchA] isis 1 [SwitchA-isis-1] is-level level-1 [SwitchA-isis-1] network-entity 10.0000.0000.0001.00 [SwitchA-isis-1] address-family ipv6 [SwitchA-isis-1-ipv6] quit [SwitchA-isis-1] quit [SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] isis ipv6 enable 1 [SwitchA-Vlan-interface100] quit配置 B。
\# Switch <SwitchB> system-view [SwitchB] isis 1 [SwitchB-isis-1] is-level level-1 [SwitchB-isis-1] network-entity 10.0000.0000.0002.00

###### 4. 验证配置

[SwitchB-isis-1] address-family ipv6 [SwitchB-isis-1-ipv6] quit [SwitchB-isis-1] quit [SwitchB] interface vlan-interface 200 [SwitchB-Vlan-interface200] isis ipv6 enable 1 [SwitchB-Vlan-interface200] quit \# 配置 Switch C。
<SwitchC> system-view [SwitchC] isis 1 [SwitchC-isis-1] network-entity 10.0000.0000.0003.00 [SwitchC-isis-1] address-family ipv6 [SwitchC-isis-1-ipv6] quit [SwitchC-isis-1] quit [SwitchC] interface vlan-interface 100 [SwitchC-Vlan-interface100] isis ipv6 enable 1 [SwitchC-Vlan-interface100] quit [SwitchC] interface vlan-interface 200 [SwitchC-Vlan-interface200] isis ipv6 enable 1 [SwitchC-Vlan-interface200] quit [SwitchC] interface vlan-interface 300 [SwitchC-Vlan-interface300] isis ipv6 enable 1 [SwitchC-Vlan-interface300] quit \# 配置 Switch D。
<SwitchD> system-view [SwitchD] isis 1 [SwitchD-isis-1] is-level level-2 [SwitchD-isis-1] network-entity 20.0000.0000.0004.00 [SwitchD-isis-1] address-family ipv6 [SwitchD-isis-1-ipv6] quit [SwitchD-isis-1] quit [SwitchD] interface vlan-interface 300 [SwitchD-Vlan-interface300] isis ipv6 enable 1 [SwitchD-Vlan-interface300] quit [SwitchD] interface vlan-interface 301 [SwitchD-Vlan-interface301] isis ipv6 enable 1 [SwitchD-Vlan-interface301] quit验证配置
4.
\# 查看 Switch A 的 IPv6 IS-IS 路由表。
[SwitchA] display isis route ipv6 Route information for IS-IS(1)
------------------------------ Level-1 IPv6 Forwarding Table
----------------------------- Destination : :: PrefixLen: 0

Flag : R/-/- Cost : 10 Next Hop : FE80::200:FF:FE0F:4 Interface: Vlan100 Destination : 2001:1:: PrefixLen: 64 Flag : D/L/- Cost : 10 Next Hop : Direct Interface: Vlan100 Destination : 2001:2:: PrefixLen: 64 Flag : R/-/- Cost : 20 Next Hop : FE80::200:FF:FE0F:4 Interface: Vlan100 Destination : 2001:3:: PrefixLen: 64 Flag : R/-/- Cost : 20 Next Hop : FE80::200:FF:FE0F:4 Interface: Vlan100 Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down Bit Set \# 查看 Switch B 的 IPv6 IS-IS 路由表。
[SwitchB] display isis route ipv6 Route information for IS-IS(1)
------------------------------ Level-1 IPv6 Forwarding Table
----------------------------- Destination : :: PrefixLen: 0 Flag : R/-/- Cost : 10 Next Hop : FE80::200:FF:FE0F:4 Interface: Vlan200 Destination : 2001:1:: PrefixLen: 64 Flag : D/L/- Cost : 10 Next Hop : FE80::200:FF:FE0F:4 Interface: Vlan200 Destination : 2001:2:: PrefixLen: 64 Flag : R/-/- Cost : 20 Next Hop : Direct Interface: Vlan200 Destination : 2001:3:: PrefixLen: 64 Flag : R/-/- Cost : 20 Next Hop : FE80::200:FF:FE0F:4 Interface: Vlan200 Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down Bit Set查看 的 路由表。
\# Switch C IPv6 IS-IS [SwitchC] display isis route ipv6 Route information for IS-IS(1)
------------------------------

Level-1 IPv6 Forwarding Table
----------------------------- Destination : 2001:1:: PrefixLen: 64 Flag : D/L/- Cost : 10 Next Hop : Direct Interface: Vlan100 Destination : 2001:2:: PrefixLen: 64 Flag : D/L/- Cost : 10 Next Hop : Direct Interface: Vlan200 Destination : 2001:3:: PrefixLen: 64 Flag : D/L/- Cost : 10 Next Hop : Direct Interface: Vlan300 Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down Bit Set Level-2 IPv6 Forwarding Table
----------------------------- Destination : 2001:1:: PrefixLen: 64 Flag : D/L/- Cost : 10 Next Hop : Direct Interface: Vlan100 Destination : 2001:2:: PrefixLen: 64 Flag : D/L/- Cost : 10 Next Hop : Direct Interface: Vlan200 Destination : 2001:3:: PrefixLen: 64 Flag : D/L/- Cost : 10 Next Hop : Direct Interface: Vlan300 Destination : 2001:4::1 PrefixLen: 64 Flag : R/-/- Cost : 10 Next Hop : FE80::20F:E2FF:FE3E:FA3D Interface: Vlan300 Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down Bit Set \# 查看 Switch D 的 IPv6 IS-IS 路由表。
[SwitchD] display isis route ipv6 Route information for IS-IS(1)
------------------------------ Level-2 IPv6 Forwarding Table
----------------------------- Destination : 2001:1:: PrefixLen: 64 Flag : R/-/- Cost : 20

##### 1.16.2 IPv6 IS-IS与BFD联动配置举例

###### 3. 配置步骤

Next Hop : FE80::200:FF:FE0F:4 Interface: Vlan300 Destination : 2001:2:: PrefixLen: 64 Flag : R/-/- Cost : 20 Next Hop : FE80::200:FF:FE0F:4 Interface: Vlan300 Destination : 2001:3:: PrefixLen: 64 Flag : D/L/- Cost : 10 Next Hop : Direct Interface: Vlan300 Destination : 2001:4::1 PrefixLen: 64 Flag : D/L/- Cost : 0 Next Hop : Direct Interface: Loop1 Flags: D-Direct, R-Added to Rib, L-Advertised in LSPs, U-Up/Down Bit Set与 联动配置举例
1.16.2 IPv6 IS-IS BFD

###### 1. 组网需求

A、Switch 通过二层交换机互连，并且在双方接口上使能 应用，之间运行
• Switch B BFD IPv6
IS-IS，网络层相互可达。
• 当 Switch B和二层交换机之间的链路出现故障后，BFD能够快速检测并通告 IPv6 IS-IS协议。

###### 2. 组网图

图1-18 IPv6 IS-IS 与 BFD 联动配置组网图

| 接口 | IPv6地址 | 设备 | 接口 |
|---|---|---|---|
| Vlan-int10 | 2001::1/64 | Switch B | Vlan-int10 |
| Vlan-int11 | 2001:2::1/64 |  | Vlan-int13 |
| Vlan-int11 | 2001:2::2/64 |  |  |
| Vlan-int13 | 2001:3::1/64 |  |  |

设备 IPv6地址Switch A 2001::2/64 2001:3::2/64 Switch C配置步骤
3.
(1) 配置各接口的 IPv6 地址（略）

(2) 配置 IPv6 IS-IS
\# 配置 Switch A。
<SwitchA> system-view
[SwitchA] isis 1
[SwitchA-isis-1] is-level level-1
[SwitchA-isis-1] network-entity 10.0000.0000.0001.00
[SwitchA-isis-1] address-family ipv6
[SwitchA-isis-1-ipv6] quit
[SwitchA-isis-1] quit
[SwitchA] interface vlan-interface 10
[SwitchA-Vlan-interface10] isis ipv6 enable 1
[SwitchA-Vlan-interface10] quit
[SwitchA] interface vlan-interface 11
[SwitchA-Vlan-interface11] isis ipv6 enable 1
[SwitchA-Vlan-interface11] quit
\# 配置 Switch B。
<SwitchB> system-view
[SwitchB] isis 1
[SwitchB-isis-1] is-level level-1
[SwitchB-isis-1] network-entity 10.0000.0000.0002.00
[SwitchB-isis-1] address-family ipv6
[SwitchB-isis-1-ipv6] quit
[SwitchB-isis-1] quit
[SwitchB] interface vlan-interface 10
[SwitchB-Vlan-interface10] isis ipv6 enable 1
[SwitchB-Vlan-interface10] quit
[SwitchB] interface vlan-interface 13
[SwitchB-Vlan-interface13] isis ipv6 enable 1
[SwitchB-Vlan-interface13] quit
配置 C。
\# Switch
<SwitchC> system-view
[SwitchC] isis 1
[SwitchC-isis-1] network-entity 10.0000.0000.0003.00
[SwitchC-isis-1] address-family ipv6
[SwitchC-isis-1-ipv6] quit
[SwitchC-isis-1] quit
[SwitchC] interface vlan-interface 11
[SwitchC-Vlan-interface11] isis ipv6 enable 1
[SwitchC-Vlan-interface11] quit
[SwitchC] interface vlan-interface 13
[SwitchC-Vlan-interface13] isis ipv6 enable 1
[SwitchC-Vlan-interface13] quit
配置 功能
(3) BFD
在 上使能 功能，并配置 参数。
\# Switch A IPv6 IS-IS BFD BFD
[SwitchA] bfd session init-mode active
[SwitchA] interface vlan-interface 10
[SwitchA-Vlan-interface10] isis ipv6 bfd enable

###### 4. 验证配置

[SwitchA-Vlan-interface10] bfd min-transmit-interval 500 [SwitchA-Vlan-interface10] bfd min-receive-interval 500 [SwitchA-Vlan-interface10] bfd detect-multiplier 7 [SwitchA-Vlan-interface10] return \# 在 Switch B 上使能 IPv6 IS-IS BFD 功能，并配置 BFD 参数。
[SwitchB] bfd session init-mode active [SwitchB] interface vlan-interface 10 [SwitchB-Vlan-interface10] isis ipv6 bfd enable [SwitchB-Vlan-interface10] bfd min-transmit-interval 500 [SwitchB-Vlan-interface10] bfd min-receive-interval 500 [SwitchB-Vlan-interface10] bfd detect-multiplier 6验证配置
4.
下面以 Switch A 为例，Switch B 和 Switch A 类似，不再赘述。
\# 显示 Switch A 的 BFD 信息。
<SwitchA> display bfd session Total Session Num: 1 Init Mode: Active IPv6 session working in ctrl packet mode:
Local Discr: 1441 Remote Discr: 1450 Source IP: FE80::20F:FF:FE00:1202（Switch A 接口 Vlan-interface10 的链路本地地址）
Destination IP: FE80::20F:FF:FE00:1200（Switch B 接口 Vlan-interface10 的链路本地地址）
Session State: Up Interface: Vlan10 Hold Time: 2319ms在 上查看 的路由信息，可以看出 和 是通过\# Switch A 2001:4::0/64 Switch A Switch B L2 Switch进行通信的。
<SwitchA> display ipv6 routing-table 2001:4::0 64 Summary Count : 1 Destination: 2001:4::/64 Protocol : IS_L1 NextHop : FE80::20F:FF:FE00:1200 Preference: 15 Interface : Vlan10 Cost : 10当 Switch A 和 Switch B 通过 L2 Switch 通信的链路出现故障时：
\# 在 Switch A 上查看 2001:4::0/64 的路由信息，可以看出 Switch A 和 Switch B 已经切换到 Switch进行通信。
C <SwitchA> display ipv6 routing-table 2001:4::0 64 Summary Count : 1 Destination: 2001:4::/64 Protocol : IS_L1 NextHop : FE80::BAAF:67FF:FE27:DCD0 Preference: 15 Interface : Vlan11 Cost : 20

###### 1. 组网需求

##### 1.16.3 IPv6 IS-IS快速重路由配置举例

组网需求
1.
如 图 1-19 所示，Switch A、Switch B和Switch C属于同一IS-IS区域，通过IPv6 IS-IS协议实现网络互连。要求当Switch A和Switch B之间的链路出现故障时，业务可以快速切换到链路B上。

###### 2. 组网图

图1-19 IPv6 IS-IS 快速重路由配置组网图

| 接口 | IP地址 | 设备 | 接口 |
|---|---|---|---|
| Vlan-int100 | 1::1/64 | Switch B | Vlan-int101 |
| Vlan-int200 | 2::1/64 |  | Vlan-int200 |
| Loop0 | 10::1/128 |  | Loop0 |
| Vlan-int100 | 1::2/64 |  |  |
| Vlan-int101 | 3::2/64 |  |  |

设备 IP地址Switch A 3::1/64 2::2/64 20::1/128 Switch C

###### 3. 配置步骤

(1) 配置各交换机接口的 IP 地址和 IPv6 IS-IS 协议
请按照上面组网图配置各接口的 IP 地址和子网掩码，具体配置过程略。
配置各交换机之间采用 IPv6 IS-IS 协议进行互连，确保 Switch A、Switch B 和 Switch C 之间
能够在网络层互通，并且各交换机之间能够借助 IPv6 IS-IS 协议实现动态路由更新。
具体配置过程略。
(2) 配置 IPv6 IS-IS 快速重路由
IPv6 IS-IS 支持快速重路由的配置方法有两种，一种是通过 LFA 算法选取备份下一跳，另一
种是在路由策略中指定备份下一跳，两种方法任选一种。
方法一：使能 Switch A 和 Switch B 的 IPv6 IS-IS 快速重路由功能（通过 LFA 算法选取备份
下一跳信息）
配置 A。
\# Switch
<SwitchA> system-view
[SwitchA] isis 1
[SwitchA-isis-1] address-family ipv6
[SwitchA-isis-1-ipv6] fast-reroute lfa
\# 配置 Switch B。
<SwitchB> system-view
[SwitchB] isis 1

[SwitchB-isis-1] address-family ipv6 [SwitchB-isis-1-ipv6] fast-reroute lfa方法二：使能 Switch A 和 Switch B 的 IPv6 IS-IS 快速重路由功能（通过路由策略指定备份下一跳）
\# 配置 Switch A。
<SwitchA> system-view [SwitchA] ipv6 prefix-list abc index 10 permit 20::1 128 [SwitchA] route-policy frr permit node 10 [SwitchA-route-policy-frr-10] if-match ipv6 address prefix-list abc [SwitchA-route-policy-frr-10] apply ipv6 fast-reroute backup-interface vlan-interface 100 backup-nexthop 1::2 [SwitchA-route-policy-frr-10] quit [SwitchA] isis 1 [SwitchA-isis-1] address-family ipv6 [SwitchA-isis-1-ipv6] fast-reroute route-policy frr [SwitchA-isis-1-ipv6] quit [SwitchA-isis-1] quit \# 配置 Switch B。
<SwitchB> system-view [SwitchB] ipv6 prefix-list abc index 10 permit 10::1 128 [SwitchB] route-policy frr permit node 10 [SwitchB-route-policy-frr-10] if-match ipv6 address prefix-list abc [SwitchB-route-policy-frr-10] apply ipv6 fast-reroute backup-interface vlan-interface 101 backup-nexthop 3::2 [SwitchB-route-policy-frr-10] quit [SwitchB] isis 1 [SwitchB-isis-1] address-family ipv6 [SwitchB-isis-1-ipv6] fast-reroute route-policy frr [SwitchB-isis-1-ipv6] quit [SwitchB-isis-1] quit

###### 4. 验证配置

\# 在 Switch A 上查看 20::1/128 的路由信息，可以看到备份下一跳信息。
[SwitchA] display ipv6 routing-table 20::1 128 verbose Summary count : 1 Destination: 20::1/128 Protocol: IS_L1 Process ID: 1 SubProtID: 0x1 Age: 00h27m45s Cost: 10 Preference: 15 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0xa OrigVrf: default-vrf TableID: 0xa OrigAs: 0 NibID: 0x24000005 LastAs: 0 AttrID: 0xffffffff Neighbor: ::

Flags: 0x10041 OrigNextHop: FE80::34CD:9FF:FE2F:D02 Label: NULL RealNextHop: FE80::34CD:9FF:FE2F:D02 BkLabel: NULL BkNextHop: FE80::7685:45FF:FEAD:102 Tunnel ID: Invalid Interface: Vlan-interface200 BkTunnel ID: Invalid BkInterface: Vlan-interface100 FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0 \# 在 Switch B 上查看 10::1/128 的路由信息，可以看到备份下一跳信息。
[SwitchB] display ipv6 routing-table 10::1 128 verbose Summary count : 1 Destination: 10::1/128 Protocol: IS_L1 Process ID: 1 SubProtID: 0x1 Age: 00h33m23s Cost: 10 Preference: 15 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0xa OrigVrf: default-vrf TableID: 0xa OrigAs: 0 NibID: 0x24000006 LastAs: 0 AttrID: 0xffffffff Neighbor: ::
Flags: 0x10041 OrigNextHop: FE80::34CC:E8FF:FE5B:C02 Label: NULL RealNextHop: FE80::34CC:E8FF:FE5B:C02 BkLabel: NULL BkNextHop: FE80::7685:45FF:FEAD:102 Tunnel ID: Invalid Interface: Vlan-interface200 BkTunnel ID: Invalid BkInterface: Vlan-interface101 FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0

## 06-BGP配置

目 录的特点大规模 网络所遇问题的解决方法协议规范搭建基本BGP网络搭建基本 网络配置任务简介（ 单播 组播）
动态创建 对等体配置BGP路由聚合

配置优先发送指定路由的撤销消息配置设备启动时为 路由应用启动策略配置 路由信息的接收策略配置重新建立BGP会话的时间间隔显示路由聚合配置大规模BGP网络的配置任务简介

配置BGP路由反射功能简介大规模 网络显示和维护
3.7.3 3-15控制BGP路径的选择允许本地 号出现的次数配置发送 更新消息时 属性中不携带私有 号功能简介配置允许比较来自同一联盟不同子自治系统邻居路由的MED属性值控制BGP路径的选择显示和维护

开启 能力开启 邻居协商的 能力功能简介通过 功能实现 软复位（ 单播 组播）
配置复位BGP会话

配置 的 认证功能简介配置向对等体/对等体组发送BGP RPKI验证结果配置7配置 与 联动通过引用路由策略的方式开启BGP快速重路由功能（IPv4 单播）
提高BGP网络的可靠性显示和维护BGP与BFD联动配置

BGP与BFD联动配置BGP扩展功能配置显示BGP

### 1 BGP概述

1 BGP概述BGP（Border Protocol，边界网关协议）是一种既可以用于不同 AS（Autonomous System，Gateway自治系统）之间，又可以用于同一 AS 内部的动态路由协议。当 BGP 运行于同一 AS 内部时，被称为 IBGP（Internal BGP）；当 BGP 运行于不同 AS 之间时，称为 EBGP（External BGP）。AS 是拥有同一选路策略，属于同一技术管理部门的一组路由器。当前使用的 BGP 版本是 BGP-4。

#### 1.1 BGP的特点

BGP 具有如下特点：
• BGP 是一种 EGP（Exterior Gateway Protocol，外部网关协议），与 OSPF、RIP 等 IGP（Interior Gateway Protocol，内部网关协议）不同，其着眼点不在于发现和计算路由，而在于控制路由的传播和选择最佳路由。
使用 作为其传输层协议（端口号 179），提高了协议的可靠性。
• BGP TCP是一种路径矢量（Path-Vector）路由协议，它采用到达目的地址所经过的 列表来衡
• BGP AS量到达目的地址的距离。
• BGP 支持 CIDR（Classless Inter-Domain Routing，无类域间路由）。
• 路由更新时，BGP 只发送更新的路由，大大减少了 BGP 传播路由所占用的带宽，适用于在Internet 上传播大量的路由信息。
• BGP 路由通过携带 AS 路径信息彻底解决路由环路问题。
• BGP 提供了丰富的路由策略，能够对路由实现灵活的过滤和选择。
• BGP 易于扩展，能够适应网络新的发展。

#### 1.2 BGP发言者和BGP对等体

运行 BGP 协议的路由器称为 BGP 发言者。BGP 发言者接收或产生路由信息，并将路由信息发布给其它 BGP 发言者。
相互之间存在 TCP 连接、相互交换路由信息的 BGP 发言者互为 BGP 对等体。根据对等体所在的AS ，对等体分为以下几种：
• IBGP 对等体：对等体与本地路由器位于同一 AS。
• EBGP 对等体：对等体与本地路由器位于不同 AS。

#### 1.3 BGP的消息类型

BGP 定义了以下几种消息类型：
• Open：TCP 连接建立后发送的第一个消息，用于在 BGP 对等体之间建立会话。
• Update ：用于在对等体之间交换路由信息。一条 Update 消息可以发布具有相同路径属性的多条可达路由，也可以同时撤销多条不可达路由。
• Keepalive：BGP 周期性地向对等体发送 Keepalive 消息，以保持会话的有效性。
• Route-refresh：用来要求对等体重新发送指定地址族的路由信息。

#### BGP的路由属性

##### 源（ORIGIN）属性

Notification：当 BGP 检测到错误状态时，就向对等体发出 Notification 消息，之后 BGP 会话
•会立即中断。
1.4 BGP的路由属性路由属性是跟随路由一起发布出去的一组参数。它对特定的路由进行了进一步的描述，使得路BGP由接收者能够根据路由属性值对路由进行过滤和选择。下面将介绍几种常见的路由属性。
1. 源（ORIGIN）属性ORIGIN 属性定义了路由信息的来源，标记一条 BGP 路由是怎么生成的。它有以下三种类型：
• IGP：优先级最高，表示路由产生于本 AS 内。
• EGP：优先级次之，表示路由通过 EGP 学到。
• Incomplete：优先级最低，表示路由的来源无法确定。例如，从其它路由协议引入的路由信息。

##### 2. AS路径（AS_PATH）属性

AS_PATH 属性记录了某条路由从本地到目的地址所要经过的所有 AS 号。当 BGP 路由器将一条路由通告到其他 时，会把本地 号添加在 列表中。收到此路由的 路由器根据AS AS AS_PATH BGP AS_PATH 属性就可以知道到达目的地址所要经过的 AS。
AS_PATH 属性有以下两种类型：
• AS_SEQUENCE：AS号按照一定的顺序排列。如 图 1-1 所示，离本地AS最近的相邻AS号排在前面，其他AS号按顺序依次排列。
• AS_SET：AS 号只是经过的 AS 的简单罗列，没有顺序要求。
图1-1 属性AS_PATH AS_PATH 属性具有如下用途：

避免路由环路的形成：缺省情况下，如果 BGP 路由器接收到的路由的 AS_PATH 属性中已经
•包含了本地的 号，则 路由器认为出现路由环路，不会接受该路由。
AS BGP影响路由的选择：在其他因素相同的情况下，BGP会优先选择路径较短的路由。比如在 图
• 1-1中，AS 50 中的BGP路由器会选择经过AS 40 的路径作为到目的地址 8.0.0.0 的最优路由。用户可以使用路由策略来人为地增加AS路径的长度，以便更为灵活地控制BGP路径的选择。路由策略的详细介绍，请参见“三层技术-IP路由配置指导”中的“路由策略”。
对路由进行过滤：通过配置 AS 路径过滤列表，可以针对 AS_PATH 属性中所包含的 AS 号来
•对路由进行过滤。AS 路径过滤列表的详细介绍，请参见“三层技术-IP 路由配置指导”中的“路由策略”。

##### 3. 下一跳（NEXT_HOP）属性

BGP的NEXT_HOP属性取值不一定是邻居路由器的IP地址。如 图 1-2 所示，NEXT_HOP属性取值情况分为几种：
发言者把自己产生的路由发给所有邻居时，将该路由信息的 属性设置为自
• BGP NEXT_HOP己与对端连接的接口地址；
• BGP 发言者把接收到的路由发送给 EBGP 对等体时，将该路由信息的 NEXT_HOP 属性设置为自己与对端连接的接口地址；
• BGP发言者把从EBGP邻居得到的路由发给IBGP邻居时，并不改变该路由信息的NEXT_HOP属性。如果配置了负载分担，等价路由被发给IBGP邻居时则会修改NEXT_HOP属性。关于“负载分担”的概念请参见“1.7 BGP负载分担”。
图1-2 NEXT_HOP 属性D = 8.0.0.0 Next_hop = 1.1.1.1 AS 100 AS 200
1.1.1.1/24 EBGP
1.1.2.1/24
8.0.0.0 EBGP D = 8.0.0.0 Next_hop = 1.1.2.1 AS 300 IBGP D = 8.0.0.0 Next_hop = 1.1.2.1

##### 4. MED（Multi-Exit Discriminator，多出口区分）属性

MED 属性仅在相邻两个 AS 之间交换，收到此属性的 AS 不会再将其通告给其它 AS。
MED属性相当于IGP使用的度量值（metrics），它用于判断流量进入AS时的最佳路由。当一个BGP路由器通过不同的 EBGP 对等体得到目的地址相同但下一跳不同的多条路由时，在其它条件相同的情况下，将优先选择MED值较小者作为最佳路由。如 图 所示，从AS 到AS 的流量将选择1-3 10 20 Router B作为入口。

图1-3 MED 属性通常情况下，BGP 只比较来自同一个 AS 的路由的 MED 属性值。在某些特殊的应用中，用户也可以通过配置 compare-different-as-med 命令，强制 BGP 比较来自不同 AS 的路由的 MED 属性值。

##### 5. 本地优先（LOCAL_PREF）属性

LOCAL_PREF 属性仅在 IBGP 对等体之间交换，不通告给其他 AS。它表明 BGP 路由器的优先级。
LOCAL_PREF属性用于判断流量离开AS时的最佳路由。当BGP路由器通过不同的IBGP对等体得到目的地址相同但下一跳不同的多条路由时，将优先选择LOCAL_PREF属性值较高的路由。如 图 1-4所示，从AS 到AS 的流量将选择Router C作为出口。
20 10

图1-4 LOCAL_PREF 属性Local_pref = 100 Router B
8.0.0.0 D = 8.0.0.0 EBGP IBGP Next_hop = 2.1.1.1
2.1.1.1 Local_pref = 100 Router A IBGP Router D D = 8.0.0.0
3.1.1.1 Next_hop = 3.1.1.1 EBGP IBGP Local_pref = 200 AS 10 Router C AS 20 Local_pref = 200

##### 6. 团体（COMMUNITY）属性

将具有相同特征的路由归为一组，称为一个团体，通过在路由中携带团体属性标识路由所属的BGP团体。团体没有物理上的边界，不同 AS 的路由可以属于同一个团体。
根据需要，一条路由可以携带一个或多个团体属性值（每个团体属性值用一个四字节的整数表示）。
接收到该路由的路由器可以通过比较团体属性值对路由作出适当的处理（比如决定是否发布该路由、在什么范围发布等），而不需要匹配复杂的过滤规则（如 ACL），从而简化路由策略的应用和降低维护管理的难度。
公认的团体属性有：
INTERNET：缺省情况下，所有的路由都属于 INTERNET 团体。具有此属性的路由可以被通
•告给所有的 BGP 对等体。
NO_EXPORT：具有此属性的路由在收到后，不能被发布到本地AS之外。如果使用了联盟，
•则不能被发布到联盟之外，但可以发布给联盟中的其他子 AS （关于联盟的定义请参见“ 1.8 6.
联盟”）。
• NO_ADVERTISE：具有此属性的路由被接收后，不能被通告给任何其他的 BGP 对等体。
• NO_EXPORT_SUBCONFED：具有此属性的路由被接收后，不能被发布到本地 AS 之外，也不能发布到联盟中的其他子 AS。
除了公认的团体属性外，用户还可以使用团体属性列表自定义团体属性，以便更为灵活地控制路由策略。

##### 7. 扩展团体属性

随着团体属性的应用日益广泛，原有四字节的团体属性无法满足用户的需求。因此，BGP 定义了新的路由属性——扩展团体属性。扩展团体属性与团体属性有如下不同：
• 扩展团体属性为八字节，提供了更多的属性值。

扩展团体属性可以划分类型。在不同的组网应用中，可以使用不同类型的扩展团体属性对路
•由进行过滤和控制。与不区分类型、统一使用同一个属性值空间的团体属性相比，扩展团体属性的配置和管理更为简单。
目前，设备支持的扩展团体属性有 VPN Target 属性和 SoO（Site of Origin，源站点）属性。VPN Target属性的详细介绍，请参见“MCE 配置指导”中的“MCE”。
SoO 扩展团体属性用来标识路由的原始站点。路由器不会将带有 SoO 属性的路由发布给该 SoO 标识的站点，确保来自某个站点的路由不会再被发布到该站点，从而避免路由环路。在 AS 路径信息丢失时，可以通过 SoO 属性来避免发生环路。
属性有三种格式：
SoO位自治系统号:32 位用户自定义数，例如：101:3。
• 16位 地址:16 位用户自定义数，例如：192.168.122.15:1。
• 32 IP位自治系统号:16 位用户自定义数，其中的自治系统号最小值为 65536。例如：65536:1。
• 32

#### 1.5 BGP的选路规则

目前，BGP 选择路由的过程为：
(1) 丢弃下一跳（NEXT_HOP）不可达的路由；
(2) 优选首选值（Preferred-value）最大的路由；
(3) 优选本地优先级（LOCAL_PREF）最高的路由；
(4) 依次选择 network 命令生成的路由、import-route 命令引入的路由、聚合路由；
(5) 优选 AS 路径（AS_PATH）最短的路由；
(6) 依次选择 ORIGIN 类型为 IGP、EGP、Incomplete 的路由；
(7) 优选 MED 值最低的路由；
(8) 依次选择从 EBGP、联盟 EBGP、联盟 IBGP、IBGP 学来的路由；
(9) 优选 IGP Metric 值最小的路由；
(10) 优选迭代深度值小的路由；
(11) 如果当前的最优路由为 EBGP 路由，则 BGP 路由器收到来自不同的 EBGP 邻居的路由后，不会改变最优路由；
(12) 优选 Router ID 最小的路由器发布的路由。如果路由包含 RR 属性，那么在路由选择过程中，就用 ORIGINATOR_ID 来替代 Router ID；
(13) 优选 CLUSTER_LIST 长度最短的路由；
(14) 优选 IP 地址最小的对等体发布的路由。
• CLUSTER_ID 为路由反射器的集群 ID，CLUSTER_LIST 由 CLUSTER_ID 序列组成，路由反射器将自己的 CLUSTER_ID 加入 CLUSTER_LIST 中。若路由反射器收到路由中的包含自己的 ，则丢弃该路由，从而避免集群内发生环路。
CLUSTER_LIST CLUSTER_ID如果配置了负载分担，并且有多条到达同一目的地的路由，则根据配置的路由条数选择多条路
•由进行负载分担。

#### 1.6 BGP发布路由的策略

BGP 发布路由时采用如下策略：
• 存在多条有效路由时，BGP 发言者只将最优路由发布给对等体。如果配置了advertise-rib-active 命令，则 BGP 发布 IP 路由表中的最优路由；否则，发布 BGP 路由表中的最优路由。
BGP 发言者只把自己使用的路由发布给对等体。
•BGP 发言者会将从 EBGP 获得的路由发布给它的所有 BGP 对等体（包括 EBGP 对等体和
•对等体）。
IBGP发言者会将从 获得的路由发布给它的 对等体，但不会发布给它的 对
• BGP IBGP EBGP IBGP等体。
• 会话一旦建立，BGP 发言者将把满足上述条件的所有 BGP 路由发布给新对等体。之后，BGP发言者只在路由变化时，向对等体发布更新的路由。

#### 1.7 BGP负载分担

BGP 可以通过如下两种方式实现负载分担：
• 基于迭代路由实现负载分担
• 通过改变 BGP 选路规则实现负载分担

##### 1. 基于迭代路由实现BGP负载分担

由于 BGP 协议本身的特殊性，它产生的路由的下一跳地址可能不是当前路由器直接相连的邻居。
常见的一个原因是：IBGP 之间发布路由信息时不改变下一跳。这种情况下，为了能够将报文正确转发出去，路由器必须先找到一个直接可达的地址（查找 建立的路由表项），通过这个地址到IGP达路由表中指示的下一跳。在上述过程中，去往直接可达地址的路由被称为依赖路由，BGP 路由依赖于这些路由指导报文转发。根据下一跳地址找到依赖路由的过程就是路由迭代。
目前系统支持基于迭代的 BGP 负载分担，即如果依赖路由本身是负载分担的（假设有三个下一跳地址），则 BGP 也会生成与依赖路由数量相同的下一跳地址来指导报文转发。需要说明的是，基于迭代的 负载分担并不需要命令配置，这一特性在系统上始终启用。
BGP

##### 2. 通过改变BGP选路规则实现负载分担

在实现方法上，BGP 的负载分担与 IGP 的负载分担有所不同：
• IGP（如 RIP、OSPF）是通过协议定义的路由算法，对到达同一目的地址的不同路由，根据计算结果，将度量值（metric）相等的路由进行负载分担，选择的标准很明确（按 metric）。
• BGP 本身并没有路由计算的算法，它只是一个选路的路由协议，因此，不能根据一个明确的度量值决定是否对路由进行负载分担，但 BGP 有丰富的选路规则，可以在对路由进行一定的选择后，有条件地进行负载分担，也就是将负载分担加入到 的选路规则中去。
BGP采用本方式进行负载分担时，BGP不再按照“1.5 BGP的选路规则”中的规则选择路由，当路由同时满足如下条件时，即在这些路由间进行负载分担：
• ORIGIN 属性、LOCAL_PREF 属性、和 MED 属性完全相同。
• 对 AS_PATH 属性的要求为：

如果同时配置 balance as-path-neglect 和 balance as-path-relax 命令，或者(cid:123)
仅配置 命令，则 属性可以不同。
balance as-path-neglect AS_PATH如果仅配置 命令，则 属性内容不同但长度相同的balance as-path-relax AS_PATH (cid:123)
路由之间能够形成 BGP 负载分担。
如果未配置 balance as-path-neglect 和 balance as-path-relax 命令，则要求(cid:123)
AS_PATH 属性也必须相同。
图1-5 BGP 负载分担示意图Router A Router D Router C AS 200 AS 100
9.0.0.0/24 Router B Router E在 图 1-5 中，Router A和Router B是Router C的IBGP对等体。当Router D和Router E同时向Router C通告到达同一目的地的路由时，如果用户在Router C上配置了进行负载分担的BGP路由条数为 2，则当这两条路由满足负载分担条件时，Router C就把这两条路由同时加入到转发表中，实现BGP路由的负载分担。Router C只向Router A和Router B转发一次该路由，该路由的属性按照如下方法确定：
如果未配置 balance as-path-neglect 和 balance as-path-relax 命令，形成负载
•分担的路由的 AS_PATH 属性相同，则发布路由的 AS_PATH 属性就为该值；如果配置了balance as-path-neglect 或 balance as-path-relax 命令，形成负载分担的路由的 AS_PATH 属性不同，则发布路由的 AS_PATH 属性为最佳路由的 AS_PATH 属性。
• NEXT_HOP 属性改变为 Router C 的地址，而不是原来的 EBGP 对等体地址。
• 其它的 BGP 路由属性为最佳路由的属性。
BGP 负载分担特性适用于 EBGP、IBGP 以及联盟之间。

#### 1.8 大规模BGP网络所遇问题的解决方法

在大规模 网络中，对等体的数目众多，路由表庞大，配置和维护极为不便。通过如下方法，BGP可以降低管理难度，提高路由发布效率。

##### 3. 对等体组

##### 1. 路由聚合

在大规模的网络中，BGP 路由表十分庞大，使用路由聚合（Routes Aggregation）可以大大减小BGP 路由表的规模。
路由聚合实际上是将多条路由合并的过程。这样 BGP 在向对等体通告路由时，可以只通告聚合后的路由，而不是将所有的具体路由都通告出去。
目前系统支持自动聚合和手动聚合方式。使用后者还可以控制聚合路由的属性，以及决定是否发布具体路由。

##### 2. 路由衰减

路由发生变化时，路由协议会向邻居发布路由更新，收到路由更新的路由器需要重新计算路由并修改路由表。如果发生路由振荡，即路由不稳定，路由表中的某条路由反复消失和重现，则会消耗大量的带宽资源和 资源，严重时会影响到网络的正常工作。
CPU在多数情况下，BGP 协议都应用于复杂的网络环境中，路由变化十分频繁。为了防止持续的路由振荡带来的不利影响，BGP 使用衰减来抑制不稳定的路由。
BGP 衰减使用惩罚值来衡量一条路由的稳定性，惩罚值越高说明路由越不稳定。如 图 1-6 所示，路由每次从可达状态变为不可达状态，或者可达路由的属性每次发生变化时，BGP给此路由增加一定的惩罚值（系统固定为 1000，不可修改）。当惩罚值超过抑制阈值时，此路由被抑制，不参与路由选择。惩罚值达到设置的上限后，不再继续增加。
发生振荡的路由如果没有再次振荡，则路由的惩罚值会逐渐减少。每经过一段时间，惩罚值便会减少一半，这个时间称为半衰期（Half-life）。当惩罚值低于再使用阈值时，此路由变为可用路由，参与路由选择。
图1-6 BGP 路由衰减示意图对等体组
3.
在大规模 BGP 网络中，对等体的数量很多，其中很多对等体具有相同的策略，在配置时会重复使用一些命令。此时，将这些对等体加入一个对等体组，可以简化配置。

对等体组是具有某些相同属性的对等体的集合。当一个对等体加入对等体组时，此对等体将获得与所在对等体组相同的配置。当对等体组的配置改变时，组内成员的配置也相应改变。

##### 4. 团体

在大规模的网络中，如果通过地址前缀列表、ACL、AS_PATH等实现对路由的控制，不仅配置复杂，而且不方便维护。利用团体属性和扩展团体属性，可以提高路由策略配置的灵活度，简化路由策略的管理，从而降低维护管理的难度。团体属性和扩展团体属性的介绍请参见“1.4 BGP的路由属性”。

##### 5. 路由反射器

为保证 IBGP 对等体之间的连通性，需要在 IBGP 对等体之间建立全连接关系。假设在一个 AS 内部有 n 台路由器，那么应该建立的 IBGP 连接数就为 n(n-1)/2。当 IBGP 对等体数目很多时，对网络资源和 CPU 资源的消耗都很大。
利用路由反射可以解决这一问题。在一个 AS 内，其中一台路由器作为 RR（Route Reflector，路由反射器），作为客户机（Client）的路由器与路由反射器之间建立 连接。路由反射器从客户IBGP机接收到路由后，将其传递（反射）给所有其他的客户机，从而保证客户机之间不需要建立 BGP连接，就可以学习到彼此的路由。
既不是路由反射器也不是客户机的BGP路由器被称为非客户机（Non-client）。非客户机与路由反射器之间，以及所有的非客户机之间仍然必须建立全连接关系。其示意图如 图 1-7 所示。
图1-7 路由反射器示意图路由反射器及其客户机形成了一个集群。通常情况下，一个集群中只有一个路由反射器，该反射器的Router ID就作为集群ID，用于识别该群。如 图 所示，为了提高网络的可靠性、避免单点故1-8障，一个集群中可以设置多个路由反射器。此时，集群中所有路由反射器上都需要配置相同的集群ID，以便集群具有统一的标识，避免路由环路的产生。

图1-8 多路由反射器Route reflector1 Route reflector2 IBGP Cluster IBGP IBGP IBGP Client Client Client AS 65000如果配置了路由反射器后，由于组网需要在路由反射器的客户机之间又建立了全连接，则客户机之间可以直接交换路由信息，客户机到客户机之间的路由反射是没有必要的。此时，不需要修改网络配置或改变网络拓扑，只需在路由反射器上通过相关命令禁止其在客户机之间反射路由，就可以避免路由反射，减少占用的带宽资源。
禁止客户机之间的路由反射后，客户机到非客户机之间的路由仍然可以被反射。

##### 6. 联盟

联盟（Confederation）是处理自治系统内部的IBGP网络连接激增的另一种方法，它将一个自治系统划分为若干个子自治系统，每个子自治系统内部的IBGP对等体建立全连接关系，子自治系统之间建立联盟内部EBGP连接关系。其示意图如 图 1-9 所示。

图1-9 联盟示意图在不属于联盟的 发言者看来，属于同一个联盟的多个子自治系统是一个整体，外界不需要了BGP解内部的子自治系统情况，联盟 ID 就是标识联盟这一整体的自治系统号，如上图中的 AS 200 就是联盟 ID。
联盟的缺陷是从非联盟方案向联盟方案转变时，要求路由器重新进行配置，逻辑拓扑也要改变。
在大型 BGP 网络中，路由反射器和联盟可以被同时使用。

#### 1.9 MP-BGP

##### 1. MP-BGP支持的协议

BGP-4 只能传递 IPv4 单播的路由信息，不能传递其它网络层协议（如 IPv6 等）的路由信息。
为了提供对多种网络层协议的支持，IETF 对 进行了扩展，形成 MP-BGP（Multiprotocol BGP-4 Border Gateway Protocol，多协议边界网关协议）。MP-BGP 可以为多种网络层协议传递路由信息。
• IPv6 单播通过 MP-BGP 发布和维护 IPv6 单播路由前缀信息。
• IPv4 组播/IPv6 组播组播路由协议 PIM（Protocol Independent Multicast，协议无关组播）根据单播静态路由或者任意单播路由协议（包括 RIP、OSPF、IS-IS、BGP 等）所生成的单播路由表进行 RPF（Reverse Path Forwarding，逆向路径转发）检查，以创建组播路由表项，从而进行组播报文的转发。组播转发路径与单播转发路径是一致的。但是，在某些情况下，组播网络拓扑和单播网络拓扑有可能不同；有些用户希望组播转发路径不同于单播转发路径，以便分别对组播流量和单播流量进行管理和控制。
MP-BGP 对 IPv4 组播 /IPv6 组播的扩展，称为 MBGP （ Multicast BGP ，组播 BGP ），它通过 MP-BGP 传递用于 RPF 检查的路由信息，并将该信息保存在独立的组播 BGP 路由表中，以实现单播转发和组播转发的隔离，使得组播转发路径可以不同于单播转发路径。
有关组播、PIM 和 检查的详细介绍，请参见“IP 组播配置指导”。
RPF

##### 3. 地址族

• EVPN
通过 MP-BGP 发布和维护 EVPN 路由信息，以实现自动发现 VTEP、自动建立和关联 VXLAN
隧道、通告 地址和 信息。详细介绍请参见“EVPN 配置指导”中的“EVPN”。
MAC ARP

##### 2. MP-BGP的扩展属性

路由信息中与网络层协议相关的关键信息包括路由前缀和下一跳地址。BGP-4 通过 Update 消息中的 NLRI（Network Layer Reachability Information，网络层可达性信息）字段携带可达路由的前缀信息，Withdrawn Routes 字段携带不可达路由的前缀信息，NEXT_HOP 属性携带下一跳地址信息。
NLRI 字段、Withdrawn Routes 字段和 NEXT_HOP 属性不易于扩展，无法携带多种网络层协议的信息。
为实现对多种网络层协议的支持，MP-BGP 定义了两个新的路径属性：
• MP_REACH_NLRI（Multiprotocol Reachable NLRI，多协议可达 NLRI）：用于携带多种网络层协议的可达路由前缀及下一跳地址信息，以便向邻居发布该路由。
• MP_UNREACH_NLRI（Multiprotocol Unreachable NLRI，多协议不可达 NLRI）：用于携带多种网络层协议的不可达路由前缀信息，以便撤销该路由。
MP-BGP 通过上述两个路径属性传递不同网络层协议的可达路由和不可达路由信息。不支持的 发言者接收到带有这两个属性的 消息后，忽略这两个属性，不把它们传MP-BGP BGP Update递给其它邻居。
地址族
3.
MP-BGP 采用地址族（Address Family）和子地址族（Subsequent Address Family）来区分属性、MP_UNREACH_NLRI 属性中携带路由信息所属的网络层协议。例如，MP_REACH_NLRI如果 MP_REACH_NLRI 属性中 AFI（Address Family Identifier，地址族标识符）为 2、SAFI（Subsequent Address Family Identifier，子地址族标识符）为 1，则表示该属性中携带的是 IPv6单播路由信息。关于地址族的一些取值可以参考 RFC 1700。

#### 1.10 BGP多进程

一台 BGP 路由器上可以同时启动多个 BGP 进程，每个 BGP 进程对应一个 BGP 实例。BGP 为不同的 BGP 实例维护独立的路由表。

#### 1.11 BGP相关视图介绍

设备为 BGP 定义了多种视图，分别用来管理不同 BGP 实例、不同地址族及不同 VPN 实例的路由信息。BGP 支持 VPN 多实例，可以为不同的 VPN 实例维护独立的路由表。
大多数BGP配置命令可以在多个视图下执行，不同视图下命令的作用范围有所不同，详细介绍如 表所示。
1-1表1-1 BGP 相关视图介绍

|  | 视图名称 |  |  | 进入视图方法 |  |  | 说明 |  |
|---|---|---|---|---|---|---|---|---|
|  |  |  | <Sysname> system-view [Sysname] bgp 100 instance abc [Sysname-bgp-abc] |  |  |  |  |  |

|  | 视图名称 |  |  | 进入视图方法 |  |  | 说明 |  |
|---|---|---|---|---|---|---|---|---|
|  |  |  | <Sysname> system-view [Sysname] bgp 100 instance abc [Sysname-bgp-abc] address-family ipv4 unicast [Sysname-bgp-abc-ipv4] |  |  |  |  |  |
|  |  |  | <Sysname> system-view [Sysname] bgp 100 instance abc [Sysname-bgp-abc] address-family ipv6 unicast [Sysname-bgp-abc-ipv6] |  |  |  |  |  |
|  |  |  | <Sysname> system-view [Sysname] bgp 100 instance abc [Sysname-bgp-abc] address-family ipv4 multicast [Sysname-bgp-abc-mul-ipv4] |  |  |  |  |  |
|  |  |  | <Sysname> system-view [Sysname] bgp 100 instance abc [Sysname-bgp-abc] address-family ipv6 multicast [Sysname-bgp-abc-mul-ipv6] |  |  |  |  |  |
|  |  |  | <Sysname> system-view [Sysname] bgp 100 instance abc [Sysname-bgp-abc] address-family l2vpn evpn [Sysname-bgp-abc-evpn] |  |  |  |  |  |
|  |  |  | <Sysname> system-view [Sysname] bgp 100 instance abc [Sysname-bgp-abc] ip vpn-instance vpn1 [Sysname-bgp-abc-vpn1] |  |  |  |  |  |
|  |  |  | <Sysname> system-view [Sysname] bgp 100 instance abc [Sysname-bgp-abc] ip vpn-instance vpn1 [Sysname-bgp-abc-vpn1] address-family ipv4 unicast [Sysname-bgp-abc-ipv4-vpn1] |  |  |  |  |  |
|  |  |  | <Sysname> system-view [Sysname] bgp 100 instance abc [Sysname-bgp-abc] ip vpn-instance vpn1 [Sysname-bgp-abc-vpn1] address-family ipv6 unicast [Sysname-bgp-abc-ipv6-vpn1] |  |  |  |  |  |
|  |  |  | <Sysname> system-view [Sysname] bgp 100 instance abc [Sysname-bgp-abc] address-family link-state [Sysname-bgp-abc-ls] |  |  |  |  |  |

#### 1.12 协议规范

与 相关的协议规范有：
BGP RFC 1700：ASSIGNED NUMBERS
•

RFC 1997：BGP Communities Attribute
•RFC 2439：BGP Route Flap Damping
•RFC 2545：Use of BGP-4 Multiprotocol Extensions for IPv6 Inter-Domain Routing
•
• RFC 2918：Route Refresh Capability for BGP-4
• RFC 4271：A Border Gateway Protocol 4 (BGP-4)
• RFC 4275：BGP-4 MIB Implementation Survey
• RFC 4277：Experience with the BGP-4 Protocol
• RFC 4360：BGP Extended Communities Attribute
• RFC 4451：BGP MULTI_EXIT_DISC (MED) Consideration
• RFC 4456：BGP Route Reflection: An Alternative to Full Mesh Internal BGP
• RFC 4486：Subcodes for BGP Cease Notification Message
• RFC 4724：Graceful Restart Mechanism for BGP
• RFC 4760：Multiprotocol Extensions for BGP-4
• RFC 5004：Avoid BGP Best Path Transitions from One External to Another
• RFC 5065：Autonomous System Confederations for BGP 5082：The
• RFC Generalized TTL Security Mechanism (GTSM)
5291：Outbound
• RFC Route Filtering Capability for BGP-4 5292：Address-Prefix-Based
• RFC Outbound Route Filter for BGP-4 5492：Capabilities
• RFC Advertisement with BGP-4 5668：4-Octet
• RFC AS Specific BGP Extended Community RFC 6198：Requirements for the Graceful Shutdown of BGP Sessions
•RFC 6793：BGP Support for Four-Octet Autonomous System (AS) Number Space
•RFC 7752：North-Bound Distribution of Link-State and Traffic Engineering (TE) Information
•Using BGP 7854：BGP
• RFC Monitoring Protocol (BMP)
7911：Advertisement
• RFC of Multiple Paths in BGP

### 2 搭建基本BGP网络

#### 2.1 BGP配置限制和指导

BGP 对 BGP 实例具有如下要求：
• 一个 BGP 实例下可以创建多个公网地址族，但不同 BGP 实例下不能创建相同的公网地址族（公网 IPv4 单播地址族、公网 IPv6 单播地址族除外）。
• 一个 BGP 实例下可以创建多个 VPN 实例，每个 VPN 实例下可以创建多个地址族，但不同实例下不能创建相同的 实例。
BGP VPN不同实例的相同地址族不能配置相同地址的邻居。
• BGP不同 BGP 实例对应的 AS 号可以相同，不同 BGP 实例的实例名称不能相同。
•

#### 2.2 搭建基本BGP网络配置任务简介（IPv4单播/IPv4组播）

IPv4 单播/IPv4 组播的 BGP 配置任务如下：
(1) 配置BGP基本功能
a. 启动BGP
b. 手工创建BGP对等体
c. 动态创建BGP对等体
d. 配置IBGP对等体组在大规模的 BGP 网络中可通过配置 BGP 对等体组简化配置。
e. 配置EBGP对等体组在大规模的 BGP 网络中可通过配置 BGP 对等体组简化配置。
f. （可选）配置建立TCP连接使用的源地址
(2) 生成BGP路由信息请至少选择其中一项任务进行配置：
配置BGP发布本地网段路由(cid:123)
配置 引入 路由协议的路由BGP IGP (cid:123)
（可选）配置BGP路由聚合(cid:123)
（可选）配置向对等体/对等体组发送缺省路由(cid:123)
(3) （可选）控制BGP路由信息的发布配置发布IP路由表中的最优路由(cid:123)
IPv4 组播不支持配置发布 IP 路由表中的最优路由。
配置优先发送缺省路由的撤销消息(cid:123)
配置优先发送指定路由的撤销消息(cid:123)
配置BGP路由信息的发布策略(cid:123)
配置BGP新增路由发布速率(cid:123)
仅 IPv4 单播支持本配置。

配置BGP延迟发布(cid:123)
配置设备启动时为BGP路由应用启动策略(cid:123)
(4) （可选）控制BGP路由信息的接收限制从BGP对等体/对等体组接收的路由数量(cid:123)
配置BGP路由信息的接收策略(cid:123)
配置SoO属性(cid:123)
(5) （可选）配置BGP定时器配置BGP会话的存活时间间隔与保持时间(cid:123)
配置重新建立BGP会话的时间间隔(cid:123)
配置发布同一路由的时间间隔(cid:123)
(6) （可选）配置BGP日志和告警功能使能BGP日志功能(cid:123)
使能BGP的路由抖动日志记录功能(cid:123)
配置BGP网管功能(cid:123)

#### 2.3 搭建基本BGP网络配置任务简介（IPv6单播/IPv6组播）

单播/IPv6 组播的 配置任务如下：
IPv6 BGP配置BGP基本功能
(1)
a. 启动BGP
b. 手工创建BGP对等体
c. 动态创建BGP对等体
d. 配置IBGP对等体组在大规模的 BGP 网络中可通过配置 BGP 对等体组简化配置。
e. 配置EBGP对等体组在大规模的 BGP 网络中可通过配置 BGP 对等体组简化配置。
f. （可选）配置建立TCP连接使用的源地址
(2) 生成BGP路由信息请至少选择其中一项任务进行配置：
配置BGP发布本地网段路由(cid:123)
配置BGP引入IGP路由协议的路由(cid:123)
（可选）配置BGP路由聚合(cid:123)
（可选）配置向对等体/对等体组发送缺省路由(cid:123)
(3) （可选）控制BGP路由信息的发布配置发布IP路由表中的最优路由(cid:123)
组播不支持配置发布 路由表中的最优路由。
IPv6 IP配置优先发送缺省路由的撤销消息(cid:123)
配置优先发送指定路由的撤销消息(cid:123)
配置BGP路由信息的发布策略(cid:123)

###### 2. 配置步骤

配置BGP新增路由发布速率(cid:123)
仅 IPv6 单播支持本配置。
配置BGP延迟发布(cid:123)
配置设备启动时为BGP路由应用启动策略(cid:123)
(4) （可选）控制BGP路由信息的接收限制从BGP对等体/对等体组接收的路由数量(cid:123)
配置BGP路由信息的接收策略(cid:123)
配置SoO属性(cid:123)
(5) （可选）配置BGP定时器配置BGP会话的存活时间间隔与保持时间(cid:123)
配置发布同一路由的时间间隔(cid:123)
(6) （可选）配置BGP日志和告警功能使能BGP日志功能(cid:123)
使能BGP的路由抖动日志记录功能(cid:123)
配置BGP网管功能(cid:123)

#### 2.4 配置BGP基本功能

##### 2.4.1 启动BGP

###### 1. 配置限制和指导

如果要在 BGP 实例下运行 BGP 协议，则必须为 BGP 实例指定 Router ID。Router ID 用来在一个自治系统中唯一的标识一台路由器。
用户可以在启动 实例进入 实例视图后指定该实例的 ID。不同 实例的
• BGP BGP Router BGP Router ID 可以相同。配置时，必须保证自治系统中任意两台路由器的 Router ID 都不相同。
通常的做法是将路由器的 Router ID 配置为与该路由器某个接口的 IP 地址一致，为了增加网络的可靠性，建议将 Router ID 配置为 Loopback 接口的 IP 地址。
如果没有在 BGP 实例视图下配置 Router ID，则该实例使用全局 Router ID。
•
• BGP 实例的 Router ID 一旦确定为非零值后不会随着系统视图下 router id 命令配置的改变而改变。只能在 实例视图下通过 命令改变 的 ID。
BGP router-id BGP Router如果是在 实例视图下配置的 ID，则 所在接口被删除时路由器不会重新
• BGP Router Router ID选择 Router ID，只有在 BGP 实例视图下使用 undo router-id 命令删除手工配置的 Router ID 后，路由器才会重新选择 Router ID。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 配置全局 Router ID 。
router id router-id缺省情况下，未配置全局 Router ID。
如果未配置全局 Router ID ，则按照下面的规则进行选择：

如果存在配置 IP 地址的 Loopback 接口，则选择 Loopback 接口地址中最大的作为 Router (cid:123)
ID。
如果所有 接口都未配置 地址，则从其他接口的 地址中选择最大的作为Loopback IP IP (cid:123)
Router ID（不考虑接口的 up/down 状态）。
(3) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]缺省情况下，没有运行 BGP，不存在 BGP 实例。
(4) （可选）为指定的 BGP 实例配置路由器的 Router ID。
router-id router-id缺省情况下，未配置 路由器在 实例内的 ID，为系统视图下通过BGP BGP Router router id命令配置的全局 Router ID。
(5) （可选）进入 BGP-VPN 实例视图。
ip vpn-instance vpn-instance-name进入 BGP-VPN 实例视图时，指定的 VPN 实例必须已经创建，且 VPN 实例内必须配置 RD（Route Distinguisher，路由标识符）。
(6) （可选）为指定的 VPN 实例配置路由器的 Router ID。
router-id { router-id | auto-select }缺省情况下，未配置 BGP 路由器在 VPN 实例内的 Router ID。
如果在 BGP 实例视图下执行了 router-id 命令，则 BGP 路由器在 VPN 实例内的 Router ID为该命令配置的 Router ID；否则，为系统视图下由 router id 命令配置的全局 Router ID。

##### 2.4.2 手工创建BGP对等体

###### 1. 配置限制和指导

当通过 IPv6 链路本地地址创建对等体或向对等体组中添加指定的对等体时，必须使用直连接口建立对等关系，且必须通过 peer connect-interface 命令将本地直连出接口指定为建立 连TCP接使用的源接口。

###### 2. 配置步骤（IPv4单播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
创建 对等体，并指定对等体的 号。
(3) IPv4 BGP AS
peer ipv4-address as-number as-number
（可选）配置对等体的描述信息。
(4)

peer ipv4-address description text缺省情况下，对等体没有描述信息。
(5) 创建 BGP IPv4 单播地址族或 BGP-VPN IPv4 单播地址族，并进入相应地址族视图。
address-family ipv4 [ unicast ]
(6) 允许本地路由器与指定对等体交换 IPv4 单播路由信息。
peer ipv4-address enable缺省情况下，本地路由器不能与对等体交换 IPv4 单播路由信息。

###### 3. 配置步骤（IPv6单播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
(3) 创建 IPv6 BGP 对等体，并指定对等体的 AS 号。
peer ipv6-address as-number as-number
(4) （可选）配置对等体的描述信息。
peer ipv6-address description text
缺省情况下，对等体没有描述信息。
创建 单播地址族或 单播地址族，并进入相应地址族视图。
(5) BGP IPv6 BGP-VPN IPv6
address-family ipv6 [ unicast ]
允许本地路由器与指定对等体交换 单播路由信息。
(6) IPv6
peer ipv6-address enable
缺省情况下，本地路由器不能与对等体/对等体组交换 单播路由信息。
IPv6

###### 4. 配置步骤（IPv4组播）

(1) 进入系统视图。
system-view
进入 实例视图。
(2) BGP
bgp as-number [ instance instance-name ]
创建 对等体，并指定对等体的 号。
(3) IPv4 BGP AS
peer ipv4-address as-number as-number
(4) （可选）配置对等体的描述信息。
peer ipv4-address description text
缺省情况下，对等体没有描述信息。
(5) 创建 BGP IPv4 组播地址族，并进入 BGP IPv4 组播地址族视图。
address-family ipv4 multicast

(6) 允许本地路由器与指定对等体交换用于 RPF 检查的 IPv4 单播路由信息。
peer ipv4-address enable
缺省情况下，本地路由器不能与对等体交换用于 RPF 检查的 IPv4 单播路由信息。

###### 5. 配置步骤（IPv6组播）

进入系统视图。
(1)
system-view
(2) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
(3) 创建 IPv6 BGP 对等体，并指定对等体的 AS 号。
peer ipv6-address as-number as-number
(4) （可选）配置对等体的描述信息。
peer ipv6-address description text缺省情况下，对等体没有描述信息。
(5) 创建 BGP IPv6 组播地址族，并进入 BGP IPv6 组播地址族视图。
address-family ipv6 multicast
(6) 允许本地路由器与指定对等体交换用于 RPF 检查的 IPv6 单播路由信息。
peer ipv6-address enable缺省情况下，本地路由器不能与对等体/对等体组交换用于 RPF 检查的 IPv6 单播路由信息。

##### 2.4.3 动态创建BGP对等体

###### 1. 功能简介

设备需要和大量的邻居建立对等体关系时，如果逐个配置对等体关系，则配置工作量大，新增或者删除对等体的维护、升级工作难度较大，且容易出错。
如果设备的邻居位于同一个网段内，则可以通过 BGP 动态对等体功能简化配置。在设备上简单地配置一个网段地址内的邻居作为动态对等体，就可以接受来自该网段内的所有邻居的连接请求，并与其建立对等体关系。只有当邻居发起连接请求时，本地才会维护与该邻居的对等体关系；否则，不维护对等体关系。BGP 动态对等体功能既简化了配置，又大大降低了维护和升级成本。

###### 2. 配置限制和指导

配置动态对等体时，设备和邻居只能有一端配置网段地址，另一端必须配置实际 IP 地址。
当通过 IPv6 链路本地地址创建对等体或向对等体组中添加指定的对等体时，必须使用直连接口建立对等关系，且必须通过 命令将本地直连出接口指定为建立 连peer connect-interface TCP接使用的源接口。

###### 3. 配置步骤（IPv4单播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]

请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(3) 创建 IPv4 BGP 动态对等体，并指定对等体的 AS 号。
peer ipv4-address mask-length as-number as-number
(4) （可选）配置对等体的描述信息。
peer ipv4-address mask-length description text缺省情况下，动态对等体没有描述信息。
(5) 创建 BGP IPv4 单播地址族或 BGP-VPN IPv4 单播地址族，并进入相应地址族视图。
address-family ipv4 [ unicast ]
(6) 允许本地路由器与指定动态对等体交换 IPv4 单播路由信息。
peer ipv4-address mask-length enable缺省情况下，本地路由器不能与动态对等体交换 IPv4 单播路由信息。

###### 4. 配置步骤（IPv6单播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
创建 动态对等体，并指定对等体的 号。
(3) IPv6 BGP AS
peer ipv6-address prefix-length as-number as-number
（可选）配置动态对等体的描述信息。
(4)
peer ipv6-address prefix-length description text
缺省情况下，动态对等体没有描述信息。
(5) 创建 BGP IPv6 单播地址族或 BGP-VPN IPv6 单播地址族，并进入相应地址族视图。
address-family ipv6 [ unicast ]
(6) 允许本地路由器与指定动态对等体交换 IPv6 单播路由信息。
peer ipv6-address prefix-length enable
缺省情况下，本地路由器不能与动态对等体交换 IPv6 单播路由信息。

###### 5. 配置步骤（IPv4组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]

(3) 创建 IPv4 BGP 动态对等体，并指定对等体的 AS 号。
peer ipv4-address mask-length as-number as-number
(4) （可选）配置动态对等体的描述信息。
peer ipv4-address mask-length description text
缺省情况下，对等体没有描述信息。
(5) 创建 BGP IPv4 组播地址族，并进入 BGP IPv4 组播地址族视图。
address-family ipv4 multicast
(6) 允许本地路由器与指定动态对等体交换用于 RPF 检查的 IPv4 单播路由信息。
peer ipv4-address mask-length enable
缺省情况下，本地路由器不能与动态对等体交换用于 RPF 检查的 IPv4 单播路由信息。

###### 6. 配置步骤（IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
(3) 创建 IPv6 BGP 动态对等体，并指定动态对等体的 AS 号。
peer ipv6-address prefix-length as-number as-number
(4) （可选）配置动态对等体的描述信息。
peer ipv6-address prefix-length description text
缺省情况下，对等体没有描述信息。
(5) 创建 BGP IPv6 组播地址族，并进入 BGP IPv6 组播地址族视图。
address-family ipv6 multicast
允许本地路由器与指定动态对等体交换用于 检查的 单播路由信息。
(6) RPF IPv6
peer ipv6-address prefix-length enable
缺省情况下，本地路由器不能与动态对等体/对等体组交换用于 检查的 单播路由信
RPF IPv6
息。

##### 2.4.4 配置IBGP对等体组

###### 1. 功能简介

IBGP 对等体组是指对等体组中的对等体与当前路由器位于同一 AS。
创建 IBGP 对等体组后，系统在将对等体加入 IBGP 对等体组时，会自动在 BGP 实例视图下创建该对等体，并设置其 AS 号为本地 AS 号。

###### 2. 配置限制和指导

当通过 IPv6 链路本地地址创建对等体或向对等体组中添加指定的对等体时，必须使用直连接口建立对等关系，且必须通过 命令将本地直连出接口指定为建立 连peer connect-interface TCP接使用的源接口。
如果分别对对等体组和对等体组中的对等体进行了某项 BGP 配置，则以最后一次配置为准。

###### 3. 配置步骤（IPv4单播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
创建 对等体组。
(3) IBGP
group group-name [ internal ]
向对等体组中添加指定的 对等体。
(4) IPv4 BGP
peer ipv4-address [ mask-length ] group group-name [ as-number
as-number ]
参数可选可不选，如果选择则必须和本地的 号一致。
as-number as-number AS
（可选）配置对等体组的描述信息。
(5)
peer group-name description text
缺省情况下，对等体组没有描述信息。
创建 单播地址族或 单播地址族，并进入相应地址族视图。
(6) BGP IPv4 BGP-VPN IPv4
address-family ipv4 [ unicast ]
(7) 允许本地路由器与指定对等体组中的对等体交换 IPv4 单播路由信息。
peer group-name enable
缺省情况下，本地路由器不能与对等体交换 IPv4 单播路由信息。

###### 4. 配置步骤（IPv4组播）

进入系统视图。
(1)
system-view
(2) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
(3) 创建 IBGP 对等体组。
group group-name [ internal ]
(4) 向对等体组中添加指定的 IPv4 BGP 对等体。
peer ipv4-address [ mask-length ] group group-name [ as-number as-number ] as-number as-number 参数可选可不选，如果选择则必须和本地的 AS 号一致。
(5) （可选）配置对等体组的描述信息。
peer group-name description text缺省情况下，对等体组没有描述信息。
(6) 创建 BGP IPv4 组播地址族，并进入 BGP IPv4 组播地址族视图。

address-family ipv4 multicast
(7) 允许本地路由器与指定对等体组中的对等体交换用于 RPF 检查的 IPv4 单播路由信息。
peer group-name enable缺省情况下，本地路由器不能与对等体交换用于 RPF 检查的 IPv4 单播路由信息。

###### 5. 配置步骤（IPv6单播）

进入系统视图。
(1)
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(3) 创建 IBGP 对等体组。
group group-name [ internal ]
(4) 向对等体组中添加指定的 IPv6 BGP 对等体。
peer ipv6-address [ prefix-length ] group group-name [ as-number as-number ] as-number as-number 参数可选可不选，如果选择则必须和本地的 AS 号一致。
(5) （可选）配置对等体组的描述信息。
peer group-name description text缺省情况下，对等体组没有描述信息。
(6) 创建 BGP IPv6 单播地址族或 BGP-VPN IPv6 单播地址族，并进入相应地址族视图。
address-family ipv6 [ unicast ]
(7) 允许本地路由器与指定对等体组中的对等体交换 IPv6 单播路由信息。
peer group-name enable缺省情况下，本地路由器不能与对等体交换 IPv6 单播路由信息。

###### 6. 配置步骤（IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
(3) 创建 IBGP 对等体组。
group group-name [ internal ]
(4) 向对等体组中添加指定的 IPv6 BGP 对等体。
peer ipv6-address [ prefix-length ] group group-name [ as-number
as-number ]
as-number as-number 参数可选可不选，如果选择则必须和本地的 AS 号一致。

###### 1. 功能简介

(5) （可选）配置对等体组的描述信息。
peer group-name description text
缺省情况下，对等体组没有描述信息。
(6) 创建 BGP IPv6 组播地址族，并进入 BGP IPv6 组播地址族视图。
address-family ipv6 multicast
(7) 允许本地路由器与指定对等体组中的对等体交换用于 RPF 检查的 IPv6 单播路由信息。
peer group-name enable
缺省情况下，本地路由器不能与对等体交换用于 RPF 检查的 IPv6 单播路由信息。

##### 2.4.5 配置EBGP对等体组

功能简介
1.
EBGP 对等体组是指对等体组中的对等体与当前路由器位于不同 AS。
根据对等体组中的对等体是否属于同一个外部 AS，EBGP 对等体组又可以分为纯 EBGP 对等体组和混合 EBGP 对等体组。如果对等体组中的对等体属于同一个外部 AS，该对等体组就是纯 EBGP对等体组；如果对等体组中的对等体属于不同外部 AS，该对等体组就是混合 对等体组。
EBGP

###### 2. 配置限制和指导

用户有三种方式配置 EBGP 对等体组：
• 第一种方式是创建对等体组后，先指定对等体组的 AS 号，再将对等体加入到对等体组中，该方式下加入的对等体具有相同的 AS 号，均为对等体组的 AS 号。对等体加入对等体组之前可以配置 AS 号，且为对等体配置的 AS 号必须与对等体组的 AS 号相同。
第二种方式是创建对等体组后，先配置对等体的 AS 号，再将对等体加入对等体组中。该方式
•下，对等体组中对等体的 号可以相同也可以不同。
AS第三种方式是创建对等体组后，将对等体加入对等体组的同时指定 号。该方式下，对等体
• AS组中对等体的 AS 号可以相同也可以不同。
如果分别对对等体组和对等体组中的对等体进行了某项 BGP 配置，则以最后一次配置为准。

###### 3. 配置EBGP对等体组方式一（IPv4单播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
创建 对等体组。
(3) EBGP
group group-name external
指定对等体组的 号。
(4) AS
peer group-name as-number as-number

缺省情况下，未指定对等体组的 AS 号。
如果对等体组中已经存在对等体，则不能改变该对等体组的 AS 号，也不能使用 undo 命令删除已指定的 号。
AS向对等体组中添加指定的 对等体。
(5) IPv4 BGP peer ipv4-address [ mask-length ] group group-name [ as-number as-number ] as-number as-number 参数可选可不选，如果选择则必须和 peer group-name as-number as-number 命令中配置的一致。
(6) （可选）配置对等体组的描述信息。
peer group-name description text缺省情况下，对等体组没有描述信息。
(7) 创建 BGP IPv4 单播地址族或 BGP-VPN IPv4 单播地址族，并进入相应地址族视图。
address-family ipv4 [ unicast ]
(8) 允许本地路由器与指定对等体组中的对等体交换 IPv4 单播路由信息。
peer group-name enable缺省情况下，本地路由器不能与对等体交换 单播路由信息。
IPv4

###### 4. 配置EBGP对等体组方式二（IPv4单播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 实例视图。
BGP-VPN
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
创建 对等体组。
(3) EBGP
group group-name external
(4) 创建 IPv4 BGP 对等体，并指定对等体的 AS 号。
peer ipv4-address [ mask-length ] as-number as-number
(5) 向对等体组中添加指定的 IPv4 BGP 对等体。
peer ipv4-address [ mask-length ] group group-name [ as-number
as-number ]
as-number as-number 参数可选可不选，如果选择则必须和 peer ipv4-address
[ mask-length ] as-number as-number 命令中配置的一致。
(6) （可选）配置对等体组的描述信息。
peer group-name description text
缺省情况下，对等体组没有描述信息。
创建 单播地址族或 单播地址族，并进入相应地址族视图。
(7) BGP IPv4 BGP-VPN IPv4

address-family ipv4 [ unicast ]
(8) 允许本地路由器与指定对等体组中的对等体交换 IPv4 单播路由信息。
peer group-name enable缺省情况下，本地路由器不能与对等体交换 IPv4 单播路由信息。

###### 5. 配置EBGP对等体组方式三（IPv4单播）

进入系统视图。
(1)
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(3) 创建 EBGP 对等体组。
group group-name external
(4) 向对等体组中添加指定的对等体。
peer ipv4-address [ mask-length ] group group-name as-number as-number
(5) （可选）配置对等体组的描述信息。
peer group-name description text缺省情况下，对等体组没有描述信息。
(6) 创建 BGP IPv4 单播地址族或 BGP-VPN IPv4 单播地址族，并进入相应地址族视图。
address-family ipv4 [ unicast ]允许本地路由器与指定对等体组中的对等体交换 单播路由信息。
(7) IPv4 peer group-name enable缺省情况下，本地路由器不能与对等体交换 单播路由信息。
IPv4

###### 6. 配置EBGP对等体组方式一（IPv4组播）

(1) 进入系统视图。
system-view
进入 实例视图。
(2) BGP
bgp as-number [ instance instance-name ]
创建 对等体组。
(3) EBGP
group group-name external
指定对等体组的 号。
(4) AS
peer group-name as-number as-number
缺省情况下，未指定对等体组的 AS 号。
如果对等体组中已经存在对等体，则不能改变该对等体组的 AS 号，也不能使用 undo 命令删
除已指定的 号。
AS
向对等体组中添加指定的 对等体。
(5) IPv4 BGP

peer ipv4-address [ mask-length ] group group-name [ as-number as-number ]参数可选可不选，如果选择则必须和as-number as-number peer group-name as-number as-number 命令中配置的一致。
(6) （可选）配置对等体组的描述信息。
peer group-name description text缺省情况下，对等体组没有描述信息。
(7) 创建 BGP IPv4 组播地址族，并进入 BGP IPv4 组播地址族视图。
address-family ipv4 multicast允许本地路由器与指定对等体组中的对等体交换用于 检查的 单播路由信息。
(8) RPF IPv4 peer group-name enable缺省情况下，本地路由器不能与对等体交换用于 检查的 单播路由信息。
RPF IPv4

###### 7. 配置EBGP对等体组方式二（IPv4组播）

(1) 进入系统视图。
system-view
进入 实例视图。
(2) BGP
bgp as-number [ instance instance-name ]
创建 对等体组。
(3) EBGP
group group-name external
创建 对等体，并指定对等体的 号。
(4) IPv4 BGP AS
peer ipv4-address [ mask-length ] as-number as-number
(5) 向对等体组中添加指定的 IPv4 BGP 对等体。
peer ipv4-address [ mask-length ] group group-name [ as-number
as-number ]
参数可选可不选，如果选择则必须和
as-number as-number peer ipv4-address
[ mask-length ] as-number as-number 命令中配置的一致。
(6) （可选）配置对等体组的描述信息。
peer group-name description text
缺省情况下，对等体组没有描述信息。
创建 组播地址族，并进入 组播地址族视图。
(7) BGP IPv4 BGP IPv4
address-family ipv4 multicast
允许本地路由器与指定对等体组中的对等体交换用于 检查的 单播路由信息。
(8) RPF IPv4
peer group-name enable
缺省情况下，本地路由器不能与对等体交换用于 RPF 检查的 IPv4 单播路由信息。

###### 8. 配置EBGP对等体组方式三（IPv4组播）

进入系统视图。
(1)
system-view进入 实例视图。
(2) BGP

bgp as-number [ instance instance-name ]
(3) 创建 EBGP 对等体组。
group group-name external
(4) 向对等体组中添加指定的对等体。
peer ipv4-address [ mask-length ] group group-name as-number as-number
(5) （可选）配置对等体组的描述信息。
peer group-name description text缺省情况下，对等体组没有描述信息。
(6) 创建 BGP IPv4 组播地址族，并进入 BGP IPv4 组播地址族视图。
address-family ipv4 multicast
(7) 允许本地路由器与指定对等体组中的对等体交换用于 RPF 检查的 IPv4 单播路由信息。
peer group-name enable缺省情况下，本地路由器不能与对等体交换用于 RPF 检查的 IPv4 单播路由信息。

###### 9. 配置EBGP对等体组方式一（IPv6单播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
创建 对等体组。
(3) EBGP
group group-name external
指定对等体组的 号。
(4) AS
peer group-name as-number as-number
缺省情况下，未指定对等体组的 AS 号。
如果对等体组中已经存在对等体，则不能改变该对等体组的 AS 号，也不能使用 undo 命令删
除已指定的 号。
AS
向对等体组中添加指定的 对等体。
(5) IPv6 BGP
peer ipv6-address [ prefix-length ] group group-name [ as-number
as-number ]
as-number as-number 参数可选可不选，如果选择则必须和 peer group-name
as-number as-number 命令中配置的一致。
(6) （可选）配置对等体组的描述信息。
peer group-name description text
缺省情况下，对等体组没有描述信息。
(7) 创建 BGP IPv6 单播地址族或 BGP-VPN IPv6 单播地址族，并进入相应地址族视图。

address-family ipv6 [ unicast ]
(8) 允许本地路由器与指定对等体组中的对等体交换 IPv6 单播路由信息。
peer group-name enable缺省情况下，本地路由器不能与对等体交换 IPv6 单播路由信息。

###### 10. 配置EBGP对等体组方式二（IPv6单播）

进入系统视图。
(1)
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(3) 创建 EBGP 对等体组。
group group-name external
(4) 创建 IPv6 BGP 对等体，并指定对等体的 AS 号。
peer ipv6-address [ prefix-length ] as-number as-number
(5) 向对等体组中添加指定的 IPv6 BGP 对等体。
peer ipv6-address [ prefix-length ] group group-name [ as-number as-number ] as-number as-number 参数可选可不选，如果选择则必须和 peer ipv6-address [ prefix-length ] as-number as-number 命令中配置的一致。
(6) （可选）配置对等体组的描述信息。
peer group-name description text缺省情况下，对等体组没有描述信息。
(7) 创建 BGP IPv6 单播地址族或 BGP-VPN IPv6 单播地址族，并进入相应地址族视图。
address-family ipv6 [ unicast ]
(8) 允许本地路由器与指定对等体组中的对等体交换 IPv6 单播路由信息。
peer group-name enable缺省情况下，本地路由器不能与对等体交换 IPv6 单播路由信息。

###### 11. 配置EBGP对等体组方式三（IPv6单播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]

ip vpn-instance vpn-instance-name
(3) 创建 EBGP 对等体组。
group group-name external
(4) 向对等体组中添加指定的 IPv6 BGP 对等体。
peer ipv6-address [ prefix-length ] group group-name as-number as-number
(5) （可选）配置对等体组的描述信息。
peer group-name description text缺省情况下，对等体组没有描述信息。
(6) 创建 BGP IPv6 单播地址族或 BGP-VPN IPv6 单播地址族，并进入相应地址族视图。
address-family ipv6 [ unicast ]
(7) 允许本地路由器与指定对等体组中的对等体交换 IPv6 单播路由信息。
peer group-name enable缺省情况下，本地路由器不能与对等体交换 IPv6 单播路由信息。

###### 12. 配置EBGP对等体组方式一（IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
(3) 创建 EBGP 对等体组。
group group-name external
(4) 指定对等体组的 AS 号。
peer group-name as-number as-number
缺省情况下，未指定对等体组的 号。
AS
如果对等体组中已经存在对等体，则不能改变该对等体组的 号，也不能使用 命令删
AS undo
除已指定的 AS 号。
(5) 向对等体组中添加指定的 IPv6 BGP 对等体。
peer ipv6-address [ prefix-length ] group group-name [ as-number
as-number ]
as-number as-number 参数可选可不选，如果选择则必须和 peer group-name
as-number as-number 命令中配置的一致。
(6) （可选）配置对等体组的描述信息。
peer group-name description text
缺省情况下，对等体组没有描述信息。
(7) 创建 BGP IPv6 组播地址族，并进入 BGP IPv6 组播地址族视图。
address-family ipv6 multicast
(8) 允许本地路由器与指定对等体组中的对等体交换用于 RPF 检查的 IPv6 单播路由信息。
peer group-name enable
缺省情况下，本地路由器不能与对等体交换用于 RPF 检查的 IPv6 单播路由信息。

###### 13. 配置EBGP对等体组方式二（IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
(3) 创建 EBGP 对等体组。
group group-name external
(4) 创建 IPv6 BGP 对等体，并指定对等体的 AS 号。
peer ipv6-address [ prefix-length ] as-number as-number
向对等体组中添加指定的 对等体。
(5) IPv6 BGP
peer ipv6-address [ prefix-length ] group group-name [ as-number
as-number ]
as-number as-number 参数可选可不选，如果选择则必须和 peer ipv6-address
[ prefix-length ] as-number as-number 命令中配置的一致。
(6) （可选）配置对等体组的描述信息。
peer group-name description text
缺省情况下，对等体组没有描述信息。
(7) 创建 BGP IPv6 组播地址族，并进入 BGP IPv6 组播地址族视图。
address-family ipv6 multicast
(8) 允许本地路由器与指定对等体组中的对等体交换用于 RPF 检查的 IPv6 单播路由信息。
peer group-name enable
缺省情况下，本地路由器不能与对等体交换用于 检查的 单播路由信息。
RPF IPv6

###### 14. 配置EBGP对等体组方式三（IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
(3) 创建 EBGP 对等体组。
group group-name external
向对等体组中添加指定的 对等体。
(4) IPv6 BGP
peer ipv6-address [ prefix-length ] group group-name as-number as-number
（可选）配置对等体组的描述信息。
(5)
peer group-name description text
缺省情况下，对等体组没有描述信息。
(6) 创建 BGP IPv6 组播地址族，并进入 BGP IPv6 组播地址族视图。
address-family ipv6 multicast
(7) 允许本地路由器与指定对等体组中的对等体交换用于 RPF 检查的 IPv6 单播路由信息。
peer group-name enable

缺省情况下，本地路由器不能与对等体交换用于 RPF 检查的 IPv6 单播路由信息。

##### 2.4.6 配置建立TCP连接使用的源地址

###### 1. 功能简介

使用 作为其传输层协议。在如下场合需要通过本配置指定建立 连接使用的源地址或BGP TCP TCP源接口（即采用指定源接口的 IP 地址/IPv6 地址与对等体/对等体组建立 TCP 连接）：
• 当指定对等体的 IP 地址/IPv6 地址不是本地路由器与对等体之间直连接口的 IP 地址/IPv6 地址时，需要在对等体上通过本配置指定建立 TCP 连接的源接口为对等体 IP 地址/IPv6 地址所在的接口或者指定 TCP 连接的源地址为对等体 IP 地址/IPv6 地址。
• 当通过 IPv6 链路本地地址创建对等体或向对等体组中添加指定的对等体时，必须使用直连接口建立对等关系，且必须通过 命令将本地直连出接口指定为建peer connect-interface立 TCP 连接使用的源接口。
• 当建立 BGP 会话的路由器之间存在冗余链路时，如果路由器上的一个接口发生故障，链路状态变为 down ，建立 TCP 连接的源地址可能会随之发生变化，导致 BGP 需要重新建立 TCP连接，造成网络震荡。为了避免该情况的发生，建议网络管理员将建立 TCP 连接所使用的源地址配置为 接口的地址，或将源接口配置为 接口，以提高 连接的Loopback Loopback TCP可靠性和稳定性。
• 当 BGP 对等体之间同时建立多条 BGP 会话时，如果没有明确指定建立 TCP 连接的源地址，可能会导致根据最优路由选择 TCP 连接源地址错误，并影响 BGP 会话的建立。如果多条 BGP会话基于不同接口的 IP 地址建立，则建议用户在配置 BGP 对等体时，通过配置源接口或源地址明确指定每个 会话的 连接源地址；如果多条 会话基于同一接口的不同BGP TCP BGP IP地址建立，则建议用户通过配置源地址，明确指定每个 BGP 会话的 TCP 连接源地址。

###### 2. 配置限制和指导

对于 IBGP 邻居，如果通过 peer connect-interface 命令指定的接口为物理接口，则当该接口发生故障、链路状态变为 时，IBGP 邻居关系会立即断开，从而加快路由收敛。
down

###### 3. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
进入 实例视图或 实例视图。
(2) BGP BGP-VPN
进入 实例视图。
BGP
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 实例视图。
BGP-VPN
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
(3) 指定与 IPv4 对等体/对等体组创建 BGP 会话时建立 TCP 连接使用的源地址或源接口。
指定与 IPv4 对等体 / 对等体组创建 BGP 会话时建立 TCP 连接使用的源地址。
(cid:123)
peer { group-name | ipv4-address [ mask-length ] } source-address
source-ipv4-address
指定与 对等体/对等体组创建 会话时建立 连接使用的源接口。
IPv4 BGP TCP
(cid:123)

peer { group-name | ipv4-address [ mask-length ] } connect-interface interface-type interface-number缺省情况下，BGP 使用到达 对等体的最佳路由出接口的主 地址与对等体/对等体组BGP IPv4建立 TCP 连接。

###### 4. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
(3) 指定与 IPv6 对等体/对等体组创建 BGP 会话时建立 TCP 连接使用的源地址或源接口。
指定与 IPv6 对等体/对等体组创建 BGP 会话时建立 TCP 连接使用的源地址。
(cid:123)
peer { group-name | ipv6-address [ prefix-length ] } source-address
source-ipv6-address
指定与 IPv6 对等体/对等体组创建 BGP 会话时建立 TCP 连接使用的源接口。
(cid:123)
peer { group-name | ipv6-address [ prefix-length ] } connect-interface
interface-type interface-number
缺省情况下，BGP 使用到达 BGP 对等体的最佳路由出接口的 IPv6 地址与对等体/对等体组建
立 TCP 连接。

#### 2.5 生成BGP路由信息

##### 2.5.1 配置BGP发布本地网段路由

###### 1. 功能简介

通过本配置可以将本地路由表中指定网段的路由添加到 BGP 路由表中，以便通过 BGP 发布该网段路由。通过该种方式发布的路由的 ORIGIN 属性为 IGP。网络管理员还可以通过使用路由策略更为灵活地控制所发布的路由。
本配置中指定的网段路由必须存在于本地的 IP 路由表中，且处于 Active 状态，否则无法将该网段路由添加到 BGP 路由表中。

###### 2. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv4 单播地址族视图、BGP-VPN IPv4 单播地址族视图或 BGP IPv4 组播地址族视
图。
请依次执行以下命令进入 BGP IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]

address-family ipv4 [ unicast ]请依次执行以下命令进入 BGP-VPN IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv4 [ unicast ]请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv4 multicast
(3) 配置 BGP 发布的本地网段路由。
network ipv4-address [ mask-length | mask ] [ route-policy route-policy-name ]缺省情况下，BGP 不发布本地的网段路由。

###### 3. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv6 单播地址族视图、BGP-VPN IPv6 单播地址族视图或 BGP IPv6 组播地址族视
图。
请依次执行以下命令进入 单播地址族视图。
BGP IPv6
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv6 [ unicast ]
请依次执行以下命令进入 BGP IPv6 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 multicast
(3) 配置 BGP 发布的本地网段路由。
network ipv6-address prefix-length [ route-policy route-policy-name ]
缺省情况下，BGP 不发布本地的网段路由。

##### 2.5.2 配置BGP引入IGP路由协议的路由

###### 1. 功能简介

BGP 可以向邻居 AS 发送本地 AS 内部网络的路由信息，但 BGP 不是自己去发现 AS 内部的路由信息，而是将 IGP 路由协议的路由信息引入到 BGP 路由表中，并发布给对等体。在引入 IGP 路由协议的路由时，可以针对不同的路由协议来对路由信息进行过滤。
缺省情况下，BGP 引入 路由协议的路由时，不会引入该协议的缺省路由。用户可以通过配置，IGP指定 BGP 引入 IGP 路由协议的路由时，允许将缺省路由引入到 BGP 路由表中。

通过引入方式发布的路由的 ORIGIN 属性为 Incomplete。
只 能 引 入 路 由 表 中 状 态 为 active 的 路 由 ， 是 否 为 active 状 态 可 以 通 过 display ip命令或 命令来查看。
routing-table protocol display ipv6 routing-table protocol这两条命令的详细介绍，请参见“三层技术-IP 路由命令参考”中的“IP 路由基础”。

###### 2. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv4 单播地址族视图、BGP-VPN IPv4 单播地址族视图或 BGP IPv4 组播地址族视
图。
请依次执行以下命令进入 BGP IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 multicast
(3) 将 IGP 路由协议的路由信息引入到 BGP 路由表中。
引入 isis、ospf、rip 协议的路由。
(cid:123)
import-route { isis | ospf | rip } [ { process-id | all-processes }
[ allow-direct | med med-value | route-policy route-policy-name ] * ]
引入直连或静态路由。
(cid:123)
import-route { direct | static } [ med med-value | route-policy
route-policy-name ]
缺省情况下，BGP 不会引入 IGP 路由协议的路由信息。
(4) （可选）允许将缺省路由引入到 BGP 路由表中。
default-route imported
缺省情况下，BGP 不允许将缺省路由引入到 BGP 路由表中。

###### 3. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv6 单播地址族视图、BGP-VPN IPv6 单播地址族视图或 BGP IPv6 组播地址族视
图。
请依次执行以下命令进入 BGP IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 [ unicast ]

###### 1. 功能简介

###### 3. 配置路由自动聚合（IPv4单播/IPv4组播）

请依次执行以下命令进入 BGP-VPN IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv6 [ unicast ]请依次执行以下命令进入 BGP IPv6 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 multicast
(3) 将 IGP 路由协议的路由信息引入到 IPv6 BGP 路由表中。
引入 isisv6、ospfv3、ripng 协议的路由。
(cid:123)
import-route { isisv6 | ospfv3 | ripng } [ { process-id | all-processes } [ allow-direct | med med-value | route-policy route-policy-name ] * ]引入直连或静态路由。
(cid:123)
import-route { direct | static } [ med med-value | route-policy route-policy-name ]缺省情况下，BGP 不会引入 IGP 路由协议的路由信息。
(4) （可选）允许将缺省路由引入到 IPv6 BGP 路由表中。
default-route imported缺省情况下，BGP 不允许将缺省路由引入到 IPv6 BGP 路由表中。

##### 2.5.3 配置BGP路由聚合

功能简介
1.
在中型或大型 BGP 网络中，在向对等体发布路由信息时，可以配置路由聚合，减少发布的路由数量，并减小路由表的规模。IPv4 支持自动聚合和手动聚合两种聚合方式，同时配置时，手动BGP聚合的优先级高于自动聚合的优先级。IPv6 BGP 只支持手动聚合。
配置自动聚合功能后，BGP 将对通过 import-route 命令引入的 IGP 子网路由进行聚合，不再发布子网路由，而是发布聚合的自然网段的路由。
自动聚合是按照自然网段进行聚合，而且只能对 IGP 引入的子网路由进行聚合。通过配置手动聚合，用户可以同时对从 IGP 路由协议引入的子网路由和用 network 命令发布的路由进行聚合，而且还可以根据需要定义聚合路由的子网掩码长度。

###### 2. 配置限制和指导

BGP 路由表中创建的聚合路由的出接口为 Null0 接口，聚合后可以减少向 BGP 对等体发布的路由数目。在使用中应注意不要使这条聚合路由成为本设备的优选路由，否则会导致报文转发失败。如果聚合路由的子网掩码长度和被聚合的某一条具体路由完全相同，且聚合路由优先级高于具体路由，则聚合路由会成为优选路由，这种情况下需要通过修改路由优先级等方式，来确保优选的路由为具体路由。
配置路由自动聚合（ 单播 组播）
3. IP v4 /IPv4
(1) 进入系统视图。
system-view

(2) 进入 BGP IPv4 单播地址族视图、BGP-VPN IPv4 单播地址族视图或 BGP IPv4 组播地址族视
图。
请依次执行以下命令进入 单播地址族视图。
BGP IPv4
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 [ unicast ]
请依次执行以下命令进入 单播地址族视图。
BGP-VPN IPv4
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 multicast
(3) 配置对引入的子网路由进行自动聚合。
summary automatic
缺省情况下，不对引入的子网路由进行自动聚合。

###### 4. 配置路由手动聚合（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv4 单播地址族视图、BGP-VPN IPv4 单播地址族视图或 BGP IPv4 组播地址族视
图。
请依次执行以下命令进入 BGP IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 multicast
(3) 在 BGP 路由表中创建一条聚合路由。
aggregate ipv4-address { mask-length | mask } [ as-set | attribute-policy
route-policy-name | detail-suppressed | origin-policy
route-policy-name | suppress-policy route-policy-name ] *
缺省情况下，未配置聚合路由。

###### 5. 配置路由手动聚合（IPv6单播/IPv6组播）

进入系统视图。
(1)
system-view

(2) 进入 BGP IPv6 单播地址族视图、BGP-VPN IPv6 单播地址族视图或 BGP IPv6 组播地址族视
图。
请依次执行以下命令进入 单播地址族视图。
BGP IPv6
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 [ unicast ]
请依次执行以下命令进入 单播地址族视图。
BGP-VPN IPv6
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv6 [ unicast ]
请依次执行以下命令进入 BGP IPv6 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 multicast
(3) 在 IPv6 BGP 路由表中创建一条聚合路由。
aggregate ipv6-address prefix-length [ as-set | attribute-policy
route-policy-name | detail-suppressed | origin-policy
route-policy-name | suppress-policy route-policy-name ] *
缺省情况下，未配置聚合路由。

##### 2.5.4 配置向对等体/对等体组发送缺省路由

###### 1. 功能简介

执行本配置后，设备将向指定对等体/对等体组发布一条下一跳地址为本地地址的缺省路由。

###### 2. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv4 单播地址族视图、BGP-VPN IPv4 单播地址族视图或 BGP IPv4 组播地址族视
图。
请依次执行以下命令进入 BGP IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 multicast
向对等体/对等体组发送缺省路由。
(3)

###### 1. 功能简介

peer { group-name | ipv4-address [ mask-length ] } default-route-advertise [ route-policy route-policy-name ]缺省情况下，不向对等体/对等体组发送缺省路由。

###### 3. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv6 单播地址族视图、BGP-VPN IPv6 单播地址族视图或 BGP IPv6 组播地址族视
图。
请依次执行以下命令进入 BGP IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv6 [ unicast ]
请依次执行以下命令进入 组播地址族视图。
BGP IPv6
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 multicast
向对等体/对等体组发送缺省路由。
(3)
peer { group-name | ipv6-address [ prefix-length ] }
default-route-advertise [ route-policy route-policy-name ]
缺省情况下，不向对等体/对等体组发送缺省路由。

#### 2.6 控制BGP路由信息的发布

##### 2.6.1 配置发布IP路由表中的最优路由

功能简介
1.
缺省情况下， BGP 发布 BGP 路由表中的最优路由，不管该路由在 IP 路由表中是否为最优路由。通过本配置可以保证 发送出去的路由是 路由表中的最优路由，以减少 发送的路由数量。
BGP IP BGP

###### 2. 配置步骤（IPv4单播）

(1) 进入系统视图。
system-view
进入 实例视图。
(2) BGP
bgp as-number [ instance instance-name ]
全局配置发布 路由表中的最优路由。
(3) IP
advertise-rib-active
缺省情况下，BGP 发布 路由表中的最优路由。
BGP
(4) 进入 BGP IPv4 单播地址族视图或 BGP-VPN IPv4 单播地址族视图。

请执行以下命令进入 BGP IPv4 单播地址族视图。
(cid:123)
address-family ipv4 [ unicast ]请依次执行以下命令进入 BGP-VPN IPv4 单播地址族视图。
(cid:123)
ip vpn-instance vpn-instance-name address-family ipv4 [ unicast ]
(5) 在指定地址族视图下，配置发布 IP 路由表中的最优路由。
advertise-rib-active缺省情况下，与 BGP 实例视图下的配置保持一致。

###### 3. 配置步骤（IPv6单播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
(3) 全局配置发布 IPv6 路由表中的最优路由。
advertise-rib-active
缺省情况下，BGP 发布 BGP 路由表中的最优路由。
(4) 进入 BGP IPv6 单播地址族视图或 BGP-VPN IPv6 单播地址族视图。
进入 BGP IPv6 单播地址族视图。
(cid:123)
address-family ipv6 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv6 单播地址族视图。
(cid:123)
ip vpn-instance vpn-instance-name
address-family ipv6 [ unicast ]
在指定地址族视图下，配置发布 路由表中的最优路由。
(5) IPv6
advertise-rib-active
缺省情况下，与 实例视图下的配置保持一致。
BGP

##### 2.6.2 配置优先发送缺省路由的撤销消息

###### 1. 功能简介

路由器向对等体发送路由撤销消息时，不会优先发送缺省路由的撤销消息。当 邻居关系BGP BGP断开时，无法保证优先撤销缺省路由，如果需要撤销的路由数量较多，那么较长时间后才能撤销缺省路由，造成流量中断时间较长。通过配置本功能，BGP 路由器会优先发送缺省路由的撤销消息，在 邻居关系断开时，最大限度地减少流量中断时间。
BGP

###### 2. 配置步骤

(1) 进入系统视图。
system-view
进入 实例视图。
(2) BGP
bgp as-number [ instance instance-name ]
配置优先发送缺省路由的撤销消息。
(3)

###### 3. 配置步骤（IPv6单播/IPv6组播）

default-route update-first缺省情况下，不优先发送缺省路由的撤销消息。

##### 2.6.3 配置优先发送指定路由的撤销消息

###### 1. 功能简介

当 BGP 路由器需要撤销大量路由时，撤销所有的路由会耗费一定时间，导致有些流量不能快速切换到有效路径。对于某些重要的、不希望长时间中断的流量，可以通过本配置，确保 BGP 路由器优先发送这些路由的撤销消息，以便将指定流量快速地切换到有效路径上，最大限度地减少流量中断时间。

###### 2. 配置步骤（IPv4单播/IPv4组播）

进入系统视图。
(1)
system-view
(2) 进入 BGP IPv4 单播地址族视图、BGP-VPN IPv4 单播地址族视图或 BGP IPv4 组播地址族视图。
请依次执行以下命令进入 单播地址族视图。
BGP IPv4 (cid:123)
bgp as-number [ instance instance-name ] address-family ipv4 [ unicast ]请依次执行以下命令进入 单播地址族视图。
BGP-VPN IPv4 (cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv4 [ unicast ]请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv4 multicast
(3) 配置优先发送指定路由的撤销消息。
update-first route-policy route-policy-name缺省情况下，不支持优先发送指定路由的撤销消息。
配置步骤（ 单播 组播）
3. IP v6 /IPv6
(1) 进入系统视图。
system-view
(2) 进入 BGP IPv6 单播地址族视图、BGP-VPN IPv6 单播地址族视图或 BGP IPv6 组播地址族视图。
请依次执行以下命令进入 BGP IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 [ unicast ]请依次执行以下命令进入 BGP-VPN IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name

address-family ipv6 [ unicast ]请依次执行以下命令进入 BGP IPv6 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 multicast
(3) 配置优先发送指定路由的撤销消息。
update-first route-policy route-policy-name缺省情况下，不支持优先发送指定路由的撤销消息。

##### 2.6.4 配置BGP路由信息的发布策略

###### 1. 发布策略配置方式简介

可以通过以下几种方式配置 BGP 路由信息的发布策略：
• 使用访问控制列表或地址前缀列表对向所有对等体发布的路由信息进行过滤。
• 向指定对等体或对等体组发布路由时，使用路由策略、访问控制列表、AS 路径过滤列表或地址前缀列表对发布给该对等体或对等体组的路由信息进行过滤。
用户可以根据需求选择过滤策略。如果同时配置了几种过滤策略，则按照如下顺序过滤发布的路由信息：
filter-policy export
•peer filter-policy export
•peer as-path-acl export
•peer prefix-list export
•
• peer route-policy export只有通过前面的过滤策略，才能继续执行后面的过滤策略；只有通过所有配置的过滤策略后，路由信息才能被发布。

###### 2. 配置准备

配置 BGP 路由信息的发布/接收策略前，根据采取的策略，需要配置下列过滤器：
• 访问控制列表，详细配置过程请参见“ACL 和 QoS 配置指导”中的“ACL”。
• 地址前缀列表，详细配置过程请参见“三层技术-IP 路由配置指导”中的“路由策略”。
路由策略，详细配置过程请参见“三层技术 路由配置指导”中的“路由策略”。
• -IP路径过滤列表，详细配置过程请参见“三层技术-IP 路由配置指导”中的“路由策略”。
• AS

###### 3. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv4 单播地址族视图、BGP-VPN IPv4 单播地址族视图或 BGP IPv4 组播地址族视
图。
请依次执行以下命令进入 BGP IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv4 单播地址族视图。
(cid:123)

bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv4 [ unicast ]请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv4 multicast
(3) 配置 BGP 路由信息的发布策略。请至少选择其中一项进行配置。
对向所有对等体发布的路由信息进行过滤。
(cid:123)
filter-policy { ipv4-acl-number | name ipv4-acl-name | prefix-list ipv4-prefix-list-name } export [ direct | { isis | ospf | rip } process-id | static ]为对等体/对等体组设置基于路由策略的路由发布过滤策略。
(cid:123)
peer { group-name | ipv4-address [ mask-length ] } route-policy route-policy-name export为对等体/对等体组设置基于 ACL 的路由发布过滤策略。
(cid:123)
peer { group-name | ipv4-address [ mask-length ] } filter-policy { ipv4-acl-number | name ipv4-acl-name } export为对等体/对等体组设置基于 AS 路径过滤列表的路由发布过滤策略。
(cid:123)
peer { group-name | ipv4-address [ mask-length ] } as-path-acl as-path-acl-number export为对等体/对等体组设置基于 IPv4 地址前缀列表的路由发布过滤策略。
(cid:123)
peer { group-name | ipv4-address [ mask-length ] } prefix-list ipv4-prefix-list-name export缺省情况下，不对发布的路由信息进行过滤。

###### 4. 配置步骤（IPv6单播/IPv6组播）

进入系统视图。
(1)
system-view
(2) 进入 BGP IPv6 单播地址族视图、BGP-VPN IPv6 单播地址族视图或 BGP IPv6 组播地址族视图。
请依次执行以下命令进入 单播地址族视图。
BGP IPv6 (cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 [ unicast ]请依次执行以下命令进入 单播地址族视图。
BGP-VPN IPv6 (cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv6 [ unicast ]请依次执行以下命令进入 BGP IPv6 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 multicast

###### 3. 配置步骤

(3) 配置 BGP 路由信息的发布策略。请至少选择其中一项进行配置。
对向所有 IPv6 BGP 对等体发布的路由信息进行过滤。
(cid:123)
filter-policy { ipv6-acl-number | name ipv6-acl-name | prefix-list
ipv6-prefix-list-name } export [ direct | { isisv6 | ospfv3 | ripng }
process-id | static ]
为对等体/对等体组设置基于路由策略的路由发布过滤策略。
(cid:123)
peer { group-name | ipv6-address [ prefix-length ] } route-policy
route-policy-name export
为对等体/对等体组设置基于 ACL 的路由发布过滤策略。
(cid:123)
peer { group-name | ipv6-address [ prefix-length ] } filter-policy
{ ipv6-acl-number | name ipv6-acl-name } export
为对等体/对等体组设置基于 AS 路径过滤列表的路由发布过滤策略。
(cid:123)
peer { group-name | ipv6-address [ prefix-length ] } as-path-acl
as-path-acl-number export
为对等体/对等体组设置基于 IPv6 地址前缀列表的路由发布过滤策略。
(cid:123)
peer { group-name | ipv6-address [ prefix-length ] } prefix-list
ipv6-prefix-list-name export
缺省情况下，不对发布的路由信息进行过滤。

##### 2.6.5 配置BGP新增路由发布速率

###### 1. 功能简介

网络中新增路由数量较大时，如果在短时间内发布大量路由，可能会导致 对等体已接收到新BGP增路由并添加对应的转发表项，本地设备上的转发表项却尚未添加，从而导致流量转发失败。通过本功能合理地配置 BGP 发送新增路由的速率可以避免上述情况发生。

###### 2. 配置限制和指导

请根据设备的性能合理配置 BGP 发送新增路由的速率，如果设备的性能较高，可以将 BGP 发送新增路由的速率适当调大；如果设备的性能一般，建议将 BGP 发送新增路由的速率适当调小。
当网络发生震荡时，建议不要将 新增路由发布速率配置为 或过小，否则可能会导致失效路BGP 0由无法及时撤销。
目前，仅支持对新增 IPv4 单播和 IPv6 单播路由的发送速率进行限制。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
(3) 配置 BGP 新增路由发布速率。
route-rate-limit rate缺省情况下，不限制 BGP 发送新增路由的发布速率。

###### 3. 配置步骤

###### 1. 功能简介

##### 2.6.6 配置BGP延迟发布

功能简介
1.
通过配置当前设备在重启后延迟发布路由更新消息，可以保证在重启时 BGP 先引入其他邻居的所有路由信息，然后再优选并向其他设备发布，以减少设备重启造成的流量丢失。

###### 2. 配置限制和指导

配置 BGP 延迟发布后，如果需要部分路由前缀不受延迟发布控制，可以使用前缀列表进行控制，通过前缀列表过滤的路由不受延迟发布的影响。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
(3) 配置设备在重启后延迟发布路由更新消息。
bgp update-delay on-startup seconds缺省情况下，设备重启后立刻向 BGP 邻居发布路由更新消息。
(4) （可选）配置通过前缀列表控制 BGP 延迟发布。
bgp update-delay on-startup prefix-list ipv4-prefix-list-name缺省情况下，未配置通过前缀列表控制 BGP 延迟发布。

##### 2.6.7 配置设备启动时为BGP路由应用启动策略

###### 1. 功能简介

设备在启动时，通过为 BGP 路由应用启动策略，修改发送的 BGP 路由的属性值，使得接收端优选其他设备发送的路由，可以减少设备重启造成的流量丢失。
如 图 2-1 所示，Router B重启过程中，在路由没有完全收敛之前对外发布路由更新消息，可能会导致Router A通过Router B去往目的地的流量丢失。配置本功能后，在RouterB重启过程中，发送应用通过命令bgp med配置的MED属性值的路由更新消息，即修改路由更新policy on-startup消息中携带的属性值，使RouterA优选RouterC作为去往目的地的路由，从而减少设备重启造成的流量丢失。

图2-1 设备启动时为 BGP 路由应用启动策略示意图

###### 2. 配置步骤

(1) 进入系统视图。
system-view
进入 实例视图。
(2) BGP
bgp as-number [ instance instance-name ]
配置设备在重启后发送应用启动策略的路由更新消息的时间。
(3)
bgp apply-policy on-startup duration seconds
缺省情况下，设备重启后发布未应用启动策略的路由更新消息。
(4) 配置启动策略中的 MED 值。
bgp policy on-startup med med-value
缺省情况下，启动策略中的 MED 值为 4294967295。

#### 2.7 控制BGP路由信息的接收

##### 2.7.1 限制从BGP对等体/对等体组接收的路由数量

###### 1. 功能简介

通过本配置可以避免攻击者向路由器发送大量的 BGP 路由，对路由器进行攻击。
当路由器从指定对等体/对等体组接收的路由数量超过指定的最大值时，可以选择以下处理方式：
• 路由器中断与该对等体/对等体组的 BGP 会话，不再尝试重建会话。
• 路由器保持与该对等体/对等体组的 BGP 会话，可以继续接收路由，仅打印日志信息。
路由器保持与该对等体/对等体组的 会话，丢弃超出限制的路由，并打印日志信息。
• BGP路由器中断与该对等体/对等体组的 会话，经过指定的时间后自动与对等体/对等体组重
• BGP建会话。
执行本配置任务时，还可以指定路由器产生日志信息的阈值，即路由器接收的路由数量与配置的最大值的百分比达到指定的阈值时，路由器将产生日志信息。

###### 2. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。

system-view
(2) 进入 BGP IPv4 单播地址族视图、BGP-VPN IPv4 单播地址族视图或 BGP IPv4 组播地址族视图。
请依次执行以下命令进入 单播地址族视图。
BGP IPv4 (cid:123)
bgp as-number [ instance instance-name ] address-family ipv4 [ unicast ]请依次执行以下命令进入 BGP-VPN IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv4 [ unicast ]请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv4 multicast
(3) 配置允许从对等体/对等体组接收的路由的最大数量。
peer { group-name | ipv4-address [ mask-length ] } route-limit prefix-number [ { alert-only | discard | reconnect reconnect-time } | percentage-value ] *缺省情况下，不限制从对等体/对等体组接收的路由数量。

###### 3. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
进入 单播地址族视图、BGP-VPN 单播地址族视图或 组播地址族视
(2) BGP IPv6 IPv6 BGP IPv6
图。
请依次执行以下命令进入 BGP IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv6 [ unicast ]
请依次执行以下命令进入 组播地址族视图。
BGP IPv6
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 multicast
(3) 配置允许从对等体/对等体组接收的路由的最大数量。
peer { group-name | ipv6-address [ prefix-length ] } route-limit
prefix-number [ { alert-only | discard | reconnect reconnect-time } |
percentage-value ] *
缺省情况下，不限制从对等体/对等体组接收的路由数量。

##### 2.7.2 配置BGP路由信息的接收策略

###### 1. 接收策略配置方式简介

可以通过以下几种方式配置 BGP 路由信息的接收策略：
• 使用访问控制列表或地址前缀列表对从所有对等体接收的路由信息进行过滤。
• 从指定对等体或对等体组接收路由时，使用路由策略、访问控制列表、AS 路径过滤列表或地址前缀列表对从该对等体或对等体组接收的路由信息进行过滤。
用户可以根据需求选择过滤策略。如果同时配置了几种过滤策略，则按照如下顺序过滤接收的路由：
• filter-policy import
• peer filter-policy import
• peer as-path-acl import
• peer prefix-list import
• peer route-policy import只有通过前面的过滤策略，才能继续执行后面的过滤策略；只有通过所有配置的过滤策略后，路由信息才能被接收。

###### 2. 配置准备

配置 路由信息的发布/接收策略前，根据采取的策略，需要配置下列过滤器：
BGP访问控制列表，详细配置过程请参见“ACL 和 配置指导”中的“ACL”。
• QoS地址前缀列表，详细配置过程请参见“三层技术-IP 路由配置指导”中的“路由策略”。
•路由策略，详细配置过程请参见“三层技术-IP 路由配置指导”中的“路由策略”。
•AS 路径过滤列表，详细配置过程请参见“三层技术-IP 路由配置指导”中的“路由策略”。
•

###### 3. 配置步骤（IPv4单播/IPv4组播）

进入系统视图。
(1)
system-view进入 单播地址族视图、BGP-VPN 单播地址族视图或 组播地址族视
(2) BGP IPv4 IPv4 BGP IPv4图。
请依次执行以下命令进入 BGP IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv4 [ unicast ]请依次执行以下命令进入 单播地址族视图。
BGP-VPN IPv4 (cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv4 [ unicast ]请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv4 multicast
(3) 配置 BGP 路由信息的接收策略。请至少选择其中一项进行配置。
对从所有对等体接收的路由信息进行过滤。
(cid:123)

filter-policy { ipv4-acl-number | name ipv4-acl-name | prefix-list ipv4-prefix-list-name } import为对等体/对等体组设置基于路由策略的路由接收过滤策略。
(cid:123)
peer { group-name | ipv4-address [ mask-length ] } route-policy route-policy-name import为对等体/对等体组设置基于 ACL 的路由接收过滤策略。
(cid:123)
peer { group-name | ipv4-address [ mask-length ] } filter-policy { ipv4-acl-number | name ipv4-acl-name } import为对等体/对等体组设置基于 AS 路径过滤列表的路由接收过滤策略。
(cid:123)
peer { group-name | ipv4-address [ mask-length ] } as-path-acl as-path-acl-number import为对等体/对等体组设置基于 IPv4 地址前缀列表的路由接收过滤策略。
(cid:123)
peer { group-name | ipv4-address [ mask-length ] } prefix-list ipv4-prefix-list-name import缺省情况下，不对接收的路由信息进行过滤。

###### 4. 配置步骤（IPv6单播/IPv6组播）

进入系统视图。
(1)
system-view进入 单播地址族视图、BGP-VPN 单播地址族视图或 组播地址族视
(2) BGP IPv6 IPv6 BGP IPv6图。
请依次执行以下命令进入 BGP IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 [ unicast ]请依次执行以下命令进入 单播地址族视图。
BGP-VPN IPv6 (cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv6 [ unicast ]请依次执行以下命令进入 BGP IPv6 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 multicast
(3) 配置 BGP 路由信息的接收策略。请至少选择其中一项进行配置。
对从所有 IPv6 BGP 对等体接收的路由信息进行过滤。
(cid:123)
filter-policy { ipv6-acl-number | name ipv6-acl-name | prefix-list ipv6-prefix-list-name } import为对等体/对等体组设置基于路由策略的路由接收过滤策略。
(cid:123)
peer { group-name | ipv6-address [ prefix-length ] } route-policy route-policy-name import为对等体/对等体组设置基于 的路由接收过滤策略。
ACL (cid:123)

###### 1. 功能简介

peer { group-name | ipv6-address [ prefix-length ] } filter-policy { ipv6-acl-number | name ipv6-acl-name } import为对等体/对等体组设置基于 路径过滤列表的路由接收过滤策略。
AS (cid:123)
peer { group-name | ipv6-address [ prefix-length ] } as-path-acl as-path-acl-number import为对等体/对等体组设置基于 IPv6 地址前缀列表的路由接收过滤策略。
(cid:123)
peer { group-name | ipv6-address [ prefix-length ] } prefix-list ipv6-prefix-list-name import缺省情况下，不对接收的路由信息进行过滤。

##### 2.7.3 配置SoO属性

功能简介
1.
为 BGP 对等体/对等体组配置 SoO 属性后，从该 BGP 对等体/对等体组接收路由时设备会为路由增加 SoO 属性，并且向该 BGP 对等体 / 对等体组发布路由时设备会检查路由的 SoO 属性，如果路由中携带的 属性与为对等体/对等体组配置的 属性相同，则不会将该路由发布给对等体/对SoO SoO等体组，从而避免路由环路。

###### 2. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv4 单播地址族视图、BGP-VPN IPv4 单播地址族视图或 BGP IPv4 组播地址族视
图。
请依次执行以下命令进入 BGP IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 multicast
(3) 为 BGP 对等体/对等体组配置 SoO 属性。
peer { group-name | ipv4-address [ mask-length ] } soo site-of-origin
缺省情况下，没有为 BGP 对等体/对等体组配置 SoO 属性。

###### 3. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view

(2) 进入 BGP IPv6 单播地址族视图、BGP-VPN IPv6 单播地址族视图或 BGP IPv6 组播地址族视
图。
请依次执行以下命令进入 单播地址族视图。
BGP IPv6
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 [ unicast ]
请依次执行以下命令进入 单播地址族视图。
BGP-VPN IPv6
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv6 [ unicast ]
请依次执行以下命令进入 BGP IPv6 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 multicast
(3) 为 BGP 对等体/对等体组配置 SoO 属性。
peer { group-name | ipv6-address [ prefix-length ] } soo site-of-origin
缺省情况下，没有为 BGP 对等体/对等体组配置 SoO 属性。

#### 2.8 配置BGP定时器

##### 2.8.1 配置BGP会话的存活时间间隔与保持时间

###### 1. 功能简介

当对等体间建立了 会话后，它们定时向对端发送 消息，以防止路由器认为 会BGP Keepalive BGP话已中断。Keepalive 消息的发送时间间隔称为存活时间间隔。
若路由器在设定的会话保持时间（Holdtime）内未收到对端的 Keepalive 消息或 Update 消息，则认为此 BGP 会话已中断，从而断开此 BGP 会话。
用户可以全局配置当前路由器上所有 BGP 会话的存活时间间隔与保持时间，也可以配置与指定对等体/对等体组建立的 BGP 会话的存活时间间隔和保持时间。如果同时配置了两者，则为指定对等体/对等体组配置的值具有较高的优先级。
存活时间间隔、会话保持时间的协商及计算方法如下：
如果当前路由器上配置的保持时间与对端设备（对等体）上配置的保持时间不一致，则数值
•较小者作为协商后的保持时间。协商的保持时间为 0 时，不向对等体发送 Keepalive 消息，与对等体之间的会话永远不会超时断开。
• 存活时间间隔不为 0 时，将协商的保持时间的三分之一与配置的存活时间间隔比较，取最小值作为存活时间间隔。

###### 2. 配置限制和指导

配置的保持时间必须大于或等于存活时间的三倍。

###### 3. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view

(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
(3) 配置 BGP 会话的存活时间间隔和保持时间。请至少选择其中一项进行配置。
配置所有 BGP 会话的存活时间间隔和保持时间。
(cid:123)
timer keepalive keepalive hold holdtime
配置本命令后，不会影响已建立的 BGP 会话，只对新建立的会话生效。
配置本地路由器与指定对等体/对等体组之间 BGP 会话的存活时间间隔和保持时间。
(cid:123)
peer { group-name | ipv4-address [ mask-length ] } timer keepalive
keepalive hold holdtime
缺省情况下，BGP 会话的存活时间间隔为 60 秒，保持时间为 180 秒。
配置 timer 或 peer timer 命令后，不会马上断开会话，而是等到其他条件触发会话重建
（如复位 BGP 会话）时，再以配置的保持时间协商建立会话。

###### 4. 配置步骤（IPv6单播/IPv6组播）

进入系统视图。
(1)
system-view进入 实例视图或 实例视图。
(2) BGP BGP-VPN进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(3) 配置 BGP 会话的存活时间间隔和保持时间。请至少选择其中一项进行配置。
配置所有 BGP 会话的存活时间间隔和保持时间。
(cid:123)
timer keepalive keepalive hold holdtime配置本命令后，不会影响已建立的 BGP 会话，只对新建立的会话生效。
配置本地路由器与指定 IPv6 BGP 对等体/对等体组之间 BGP 会话的存活时间间隔和保持(cid:123)
时间。
peer { group-name | ipv6-address [ prefix-length ] } timer keepalive keepalive hold holdtime缺省情况下，BGP 会话的存活时间间隔为 60 秒，保持时间为 180 秒。
配置 timer 或 peer timer 命令后，不会马上断开会话，而是等到其他条件触发会话重建（如复位 会话）时，再以配置的保持时间协商建立会话。
BGP

###### 1. 功能简介

##### 2.8.2 配置重新建立BGP会话的时间间隔

功能简介
1.
通过配置本功能可以控制重新建立 BGP 会话的速度：
• 当邻居关系建立失败，可以将定时器时间间隔的值调小，从而加快 BGP 会话建立的速度，便于路由快速收敛。
当邻居关系震荡时，可以将定时器时间间隔的值调大，从而减轻路由震荡。
•

###### 2. 配置限制和指导

配置本地路由器与指定对等体/对等体组之间重新建立 会话的时间间隔比配置本地路由器与所BGP有对等体之间重新建立 BGP 会话的时间间隔的优先级高。

###### 3. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
(3) 配置本地路由器与对等体之间重新建立 BGP 会话的时间间隔。请选择其中一项进行配置。
配置本地路由器与所有对等体之间重新建立 会话的时间间隔。
BGP
(cid:123)
timer connect-retry retry-time
配置本地路由器与指定对等体/对等体组之间重新建立 会话的时间间隔。
BGP
(cid:123)
peer { group-name | ipv4-address [ mask-length ] } timer connect-retry
retry-time
缺省情况下，本地路由器与对等体/对等体组之间重新建立 BGP 会话的时间间隔为 32 秒。

###### 4. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
配置本地路由器与对等体之间重新建立 会话的时间间隔。请选择其中一项进行配置。
(3) BGP
配置本地路由器与所有对等体之间重新建立 会话的时间间隔。
BGP
(cid:123)
timer connect-retry retry-time

配置本地路由器与指定 IPv6 BGP 对等体/对等体组之间重新建立 BGP 会话的时间间隔。
(cid:123)
peer { group-name | ipv6-address [ prefix-length ] } timer connect-retry retry-time缺省情况下，本地路由器与对等体/对等体组之间重新建立 会话的时间间隔为 秒。
BGP 32

##### 2.8.3 配置发布同一路由的时间间隔

###### 1. 功能简介

路由发生变化时，BGP 路由器会发送 消息通知对等体。如果同一路由频繁变化，BGP BGP Update路由器会频繁发送 Update 消息更新路由，导致路由震荡。通过本配置指定向对等体/对等体组发布同一路由更新的时间间隔，可以避免每次路由变化都发送 Update 消息，避免路由震荡。对于需要撤销的路由，BGP 路由器会立即向邻居发送路由撤销消息，不受本配置的控制。

###### 2. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
进入 实例视图或 实例视图。
(2) BGP BGP-VPN
进入 实例视图。
BGP
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 实例视图。
BGP-VPN
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
(3) 配置向指定对等体/对等体组发布同一路由的时间间隔。
peer { group-name | ipv4-address [ mask-length ] } route-update-interval
interval
缺省情况下，向 对等体发布同一路由的时间间隔为 秒，向 对等体发布同一路
IBGP 15 EBGP
由的时间间隔为 30 秒。

###### 3. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
配置向指定 对等体 对等体组发布同一路由的时间间隔。
(3) IPv6 BGP /
peer { group-name | ipv6-address [ prefix-length ] }
route-update-interval interval

###### 1. 功能简介

缺省情况下，向 IBGP 对等体发布同一路由的时间间隔为 15 秒，向 EBGP 对等体发布同一路由的时间间隔为 秒。
30

#### 2.9 配置BGP日志和告警功能

##### 2.9.1 使能BGP日志功能

功能简介
1.
全局使能 BGP 日志记录功能，并使能与指定对等体/对等体组之间 BGP 会话的日志记录功能后，与该对等体/对等体组之间的 会话建立以及断开时会生成日志信息，通过BGP display bgp peer ipv4 unicast log-info 命令或 display bgp peer ipv6 unicast log-info 命令可以查看记录的日志信息。生成的日志信息还将被发送到设备的信息中心，通过设置信息中心的参数，决定日志信息的输出规则（即是否允许输出以及输出方向）。
有关信息中心参数的配置请参见“网络管理和监控配置指导”中的“信息中心”。

###### 2. 配置步骤（IPv4单播/IPv4组播）

进入系统视图。
(1)
system-view进入 实例视图。
(2) BGP bgp as-number [ instance instance-name ]
(3) 全局使能 BGP 日志记录功能。
log-peer-change缺省情况下，全局 BGP 日志记录功能处于开启状态。
(4) （可选）进入 BGP-VPN 实例视图。
ip vpn-instance vpn-instance-name
(5) 使能与指定对等体/对等体组之间 BGP 会话的日志记录功能。
peer { group-name | ipv4-address [ mask-length ] } log-change缺省情况下，与所有对等体/对等体组之间 BGP 会话的日志记录功能均处于开启状态。

###### 3. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
(3) 全局使能 BGP 日志记录功能。
log-peer-change
缺省情况下，全局 BGP 日志记录功能处于开启状态。
(4) （可选）进入 BGP-VPN 实例视图。
ip vpn-instance vpn-instance-name
(5) 使能与指定对等体/对等体组之间 BGP 会话的日志记录功能。
peer { group-name | ipv6-address [ prefix-length ] } log-change

###### 3. 配置步骤（IPv6单播/IPv6组播）

缺省情况下，与所有对等体/对等体组之间 BGP 会话的日志记录功能均处于开启状态。

##### 2.9.2 使能BGP的路由抖动日志记录功能

###### 1. 功能简介

使能 对应地址族的路由抖动日志记录功能后，当该地址族的路由发生抖动并满足日志输出条BGP件时会生成路由抖动日志信息。生成的日志信息还将被发送到设备的信息中心，通过设置信息中心的参数，决定日志信息的输出规则（即是否允许输出以及输出方向）。
有关信息中心参数的配置请参见“网络管理和监控配置指导”中的“信息中心”。

###### 2. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv4 单播地址族视图、BGP-VPN IPv4 单播地址族视图或 BGP IPv4 组播地址族视
图。
请依次执行以下命令进入 BGP IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 multicast
(3) 使能 BGP 的路由抖动日志记录功能。
log-route-flap monitor-time monitor-count [ log-count-limit |
route-policy route-policy-name ] *
缺省情况下，BGP 的路由抖动日志记录功能处于关闭状态。
配置步骤（ 单播 组播）
3. IP v6 /IPv6
(1) 进入系统视图。
system-view
(2) 进入 BGP IPv6 单播地址族视图、BGP-VPN IPv6 单播地址族视图或 BGP IPv6 组播地址族视
图。
请依次执行以下命令进入 BGP IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name

address-family ipv6 [ unicast ]请依次执行以下命令进入 BGP IPv6 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 multicast
(3) 使能 BGP 的路由抖动日志记录功能。
log-route-flap monitor-time monitor-count [ log-count-limit | route-policy route-policy-name ] *缺省情况下，BGP 的路由抖动日志记录功能处于关闭状态。

##### 2.9.3 配置BGP网管功能

###### 1. 功能简介

开启 模块的告警功能后，当 的邻居状态变化时 会产生 中规定的告警信BGP BGP BGP RFC 4273息，该信息包含邻居地址、最近一次出现错误的错误码和错误子码、当前的邻居状态。生成的告警信息将发送到设备的 SNMP 模块，通过设置 SNMP 中告警信息的发送参数，来决定告警信息输出的相关属性。
通过 MIB（Management Information Base，管理信息库）节点对 BGP 进行管理时，BGP 无法获知被管理的节点属于哪个 实例。为不同的 实例配置不同的 上下文可以解决上述BGP BGP SNMP问题。
设备接收到 SNMP 报文后，根据报文中携带的上下文（对于 SNMPv3）或团体名称（对于SNMPv1/v2c），判断如何进行处理：
• 对于 SNMPv3 报文：
如果报文中不携带上下文，且没有为 default 实例配置 SNMP 上下文，则对 BGP default (cid:123)
实例的 MIB 节点进行相应处理。
如果报文中携带上下文，设备上存在对应的 SNMP 上下文（通过系统视图下的(cid:123)
snmp-agent context 命令创建），且该上下文与为某一个 实例配置的上下文相同，BGP则对该 BGP 实例的 MIB 节点进行相应处理。
其他情况下，不允许对任何 MIB 节点进行处理。
(cid:123)
对于 报文：
• SNMPv1/v2c如果设备上没有通过系统视图下的 命令将报文中的团体snmp-agent community-map (cid:123)
名映射为 SNMP 上下文，且没有为 default 实例配置 SNMP 上下文，则对 BGP default 实例的 MIB 节点进行相应处理。
如果设备上将团体名映射为 SNMP 上下文，设备上存在对应的 SNMP 上下文，且该上下(cid:123)
文与为某一个 BGP 实例配置的上下文相同，则对该 BGP 实例的 MIB 节点进行相应处理。
其他情况下，不允许对任何 MIB 节点进行处理。
(cid:123)
有关告警信息的详细和 SNMP 上下文和团体名的详细介绍，请参见“网络管理和监控配置指导”中的“SNMP”。

###### 2. 配置步骤

(1) 进入系统视图。
system-view

(2) 开启 BGP 模块的告警功能。
snmp-agent trap enable bgp [ instance instance-name ]
缺省情况下，BGP 模块的告警功能处于开启状态。
(3) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
(4) 配置 BGP 实例的 SNMP 上下文。
snmp context-name context-name
缺省情况下，未配置 BGP 实例的 SNMP 上下文。

#### 2.10 搭建基本BGP网络显示和维护

##### 2.10.1 显示BGP

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 BGP 的运行情况，通过查看显示信息验证配置的效果。

###### 1. 搭建基本BGP网络配置显示（IPv4单播）

表2-1 搭建基本 网络配置显示（IPv4 单播）
BGP操作 命令display bgp [ instance instance-name ] group ipv4显示BGP IPv4单播对等体组的信息 [ unicast ] [ vpn-instance vpn-instance-name ] [ group-name group-name ]显示通过network命令发布的路由信息和display bgp [ instance instance-name ] network ipv4通过network short-cut命令配置的[ unicast ] [ vpn-instance vpn-instance-name ] Short-cut路由信息display bgp [ instance instance-name ] peer ipv4 [ unicast ] [ vpn-instance vpn-instance-name ] [ ipv4-address mask-length | { ipv4-address |显示BGP IPv4单播对等体或对等体组的状group-name group-name } log-info | [ ipv4-address ]态和统计信息 verbose ] display bgp [ instance instance-name ] peer ipv4 [ unicast ] vpn-instance-all [ verbose ] display bgp [ instance instance-name ] routing-table flap-info ipv4 [ unicast ]显示BGP IPv4单播路由的震荡统计信息 [ vpn-instance vpn-instance-name ] [ ipv4-address [ { mask-length | mask } [ longest-match ] ] | as-path-acl as-path-acl-number ] display bgp [ instance instance-name ] routing-table ipv4 [ unicast ] [ vpn-instance vpn-instance-name ] [ ipv4-address [ { mask-length | mask } [ longest-match ] ] | ipv4-address [ mask-length | mask ] advertise-info | as-path-acl显示BGP IPv4单播路由信息 as-path-acl-number | community-list { { basic-community-list-number | comm-list-name } [ whole-match ] | adv-community-list-number } | peer ipv4-address { advertised-routes | received-routes } [ ipv4-address [ mask-length | mask ] | statistics ] | statistics ] display bgp [ instance instance-name ] update-group显示BGP IPv4单播地址族下打包组的相关ipv4 [ unicast ] [ vpn-instance vpn-instance-name ]

操作 命令[ ipv4-address ]信息显示所有BGP实例的信息 display bgp instance-info

###### 2. 搭建基本BGP网络配置显示（IPv6单播）

表2-2 搭建基本 BGP 网络配置显示（IPv6 单播）
操作 命令display bgp [ instance instance-name ] group ipv6显示BGP IPv6单播对等体组的信息 [ unicast ] [ vpn-instance vpn-instance-name ] [ group-name group-name ]显示通过network命令发布的路由信息和display bgp [ instance instance-name ] network ipv6通过network short-cut命令配置的[ unicast ] [ vpn-instance vpn-instance-name ] Short-cut路由信息display bgp [ instance instance-name ] peer ipv6 [ unicast ] [ vpn-instance vpn-instance-name ] [ ipv6-address prefix-length | { ipv6-address | group-name group-name } log-info | [ ipv6-address ] verbose ]显示BGP IPv6单播对等体或对等体组的状态和统计信息 display bgp [ instance instance-name ] peer ipv6 [ unicast ] [ ipv4-address mask-length | ipv4-address log-info | [ ipv4-address ] verbose ] display bgp [ instance instance-name ] peer ipv6 [ unicast ] vpn-instance-all [ verbose ] display bgp [ instance instance-name ] routing-table flap-info ipv6 [ unicast ]显示BGP IPv6单播路由的震荡统计信息[ vpn-instance vpn-instance-name ] [ ipv6-address prefix-length | as-path-acl as-path-acl-number ] display bgp [ instance instance-name ] routing-table ipv6 [ unicast ] [ vpn-instance vpn-instance-name ] [ ipv6-address prefix-length [ advertise-info ] | as-path-acl as-path-acl-number | community-list { { basic-community-list-number | comm-list-name } [ whole-match ] | adv-community-list-number } | peer ipv6-address显示BGP IPv6单播路由信息{ advertised-routes | received-routes } [ ipv6-address prefix-length | statistics ] | statistics ] display bgp [ instance instance-name ] routing-table ipv6 [ unicast ] peer ipv4-address { advertised-routes | received-routes } [ ipv6-address prefix-length | statistics ] display bgp [ instance instance-name ] update-group ipv6 [ unicast ] [ ipv4-address | ipv6-address ]显示BGP IPv6单播地址族下打包组的相关display bgp [ instance instance-name ] update-group信息ipv6 [ unicast ] vpn-instance vpn-instance-name [ ipv6-address ]显示所有 BGP 实例的信息 display bgp instance-info

###### 3. 搭建基本BGP网络配置显示（IPv4组播）

表2-3 搭建基本 BGP 网络配置显示（IPv4 组播）
操作 命令display bgp [ instance instance-name ] group ipv4显示BGP IPv4组播对等体组的信息multicast [ group-name group-name ]显示通过network命令发布的路由信息和display bgp [ instance instance-name ] network ipv4通过network short-cut命令配置的multicast Short-cut路由信息display bgp [ instance instance-name ] paths显示BGP的路由属性信息[ as-regular-expression ] display bgp [ instance instance-name ] peer ipv4显示BGP IPv4组播对等体或对等体组的状 multicast [ ipv4-address mask-length | { ipv4-address | group-name group-name } log-info |态和统计信息[ ipv4-address ] verbose ] display bgp [ instance instance-name ] routing-table flap-info ipv4 multicast显示BGP IPv4组播路由的震荡统计信息 [ ipv4-address [ { mask-length | mask } [ longest-match ] ] | as-path-acl as-path-acl-number ] display bgp [ instance instance-name ] routing-table ipv4 multicast [ ipv4-address [ { mask-length | mask } [ longest-match ] ] | ipv4-address [ mask-length | mask ] advertise-info as-path-acl community-list | as-path-acl-number |显示BGP IPv4组播路由信息{ { basic-community-list-number | comm-list-name } [ whole-match ] | adv-community-list-number } | peer ipv4-address { advertised-routes | received-routes } [ ipv4-address [ mask-length | mask ] | statistics ] | statistics ]显示BGP IPv4组播地址族下打包组的相关 display bgp [ instance instance-name ] update-group信息 ipv4 multicast [ ipv4-address ]显示所有BGP实例的信息 display bgp instance-info

###### 4. 搭建基本BGP网络配置显示（IPv6组播）

表2-4 搭建基本 网络配置显示（IPv6 组播）
BGP操作 命令display bgp [ instance instance-name ] group ipv6显示BGP IPv6组播对等体组的信息multicast [ group-name group-name ]显示通过network命令发布的路由信息和display bgp [ instance instance-name ] network ipv6通过network short-cut命令配置的multicast Short-cut路由信息display bgp [ instance instance-name ] paths显示BGP的路由属性信息[ as-regular-expression ] display bgp [ instance instance-name ] peer ipv6显示BGP IPv6组播对等体或对等体组的状multicast [ ipv6-address prefix-length |态和统计信息 { ipv6-address | group-name group-name } log-info | [ ipv6-address ] verbose ]

##### 2.10.3 清除BGP信息

操作 命令display bgp [ instance instance-name ] routing-table flap-info ipv6 multicast显示BGP IPv6组播路由的震荡统计信息[ ipv6-address prefix-length | as-path-acl as-path-acl-number ] display bgp [ instance instance-name ] routing-table ipv6 multicast [ ipv6-address prefix-length [ advertise-info ] | as-path-acl as-path-acl-number | community-list显示BGP IPv6组播路由信息 { { basic-community-list-number | comm-list-name } [ whole-match ] | adv-community-list-number } | peer ipv6-address { advertised-routes | received-routes } [ ipv6-address prefix-length | statistics ] | statistics ]显示BGP IPv6组播地址族下打包组的相关 display bgp [ instance instance-name ] update-group ipv6 multicast [ ipv6-address ]信息显示所有BGP实例的信息 display bgp instance-info

##### 2.10.2 复位BGP会话

当 路由策略或协议发生变化后，如果需要通过复位 会话使新的配置生效，请在用户视图BGP BGP下进行下列配置。
表2-5 复位 会话BGP操作 命令reset bgp [ instance instance-name ] { as-number | ipv4-address [ mask-length ] | all | external | group复位IPv4单播地址族下的BGP会话group-name | internal } ipv4 [ unicast ] [ vpn-instance vpn-instance-name ] reset bgp [ instance instance-name ] { as-number |复位IPv4组播地址族下的BGP会话 ipv4-address [ mask-length ] | all | external | group group-name | internal } ipv4 multicast reset bgp [ instance instance-name ] { as-number | ipv6-address [ prefix-length ] | all | external | group group-name | internal } ipv6 [ unicast ]复位IPv6单播地址族下的BGP会话[ vpn-instance vpn-instance-name ] reset bgp ipv4-address [ mask-length ] ipv6 [ unicast ] reset bgp [ instance instance-name ] { as-number |复位IPv6组播地址族下的BGP会话 ipv6-address [ prefix-length ] | all | external | group group-name | internal } ipv6 multicast复位所有BGP会话 reset bgp [ instance instance-name ] all清除 信息
2.10.3 BGP在用户视图下，执行 reset 命令可以清除 BGP 相关统计信息。

###### 2. 组网图

表2-6 清除 BGP 信息操作 命令reset bgp [ instance instance-name ] flap-info ipv4 [ unicast ] [ vpn-instance vpn-instance-name ]清除BGP IPv4单播路由的振荡统计信息 [ ipv4-address [ mask-length | mask ] | as-path-acl as-path-acl-number | peer ipv4-address [ mask-length ] ] reset bgp [ instance instance-name ] flap-info ipv4 multicast [ ipv4-address [ mask-length | mask ] |清除BGP IPv4组播路由的振荡统计信息as-path-acl as-path-acl-number | peer ipv4-address [ mask-length ] ] reset bgp instance flap-info ipv6 [ instance-name ] [ unicast ] [ vpn-instance vpn-instance-name ]清除BGP IPv6单播路由的振荡统计信息 [ ipv6-address prefix-length | as-path-acl as-path-acl-number | peer ipv6-address [ prefix-length ] ] reset bgp [ instance instance-name ] flap-info ipv6 multicast [ ipv6-address prefix-length |清除 BGP IPv6 组播路由的振荡统计信息as-path-acl as-path-acl-number | peer ipv6-address [ prefix-length ] ]

#### 2.11 搭建基本IPv4 BGP网络典型配置举例

##### 2.11.1 BGP基本配置

###### 1. 组网需求

如 图 所示，所有交换机均运行BGP协议。要求Switch A和Switch B之间建立EBGP连接，Switch 2-2 B和Switch C之间建立IBGP连接，使得Switch C能够访问Switch A直连的 8.1.1.0/24 网段。
组网图
2.
图2-2 BGP 基本配置组网图

###### 3. 配置步骤

配置各接口的 地址（略）
(1) IP配置 连接
(2) IBGP为了防止端口状态不稳定引起路由震荡，本举例使用 接口来创建 对等体。
Loopback IBGP (cid:123)

使用 Loopback 接口创建 IBGP 对等体时，因为 Loopback 接口不是两对等体实际连接的接(cid:123)
口，所以，必须使用 命令将 接口配置为 连peer connect-interface Loopback BGP接的源接口。
在 AS 65009 内部，使用 OSPF 协议，保证 Switch B 到 Switch C 的 Loopback 接口路由可(cid:123)
达， Switch C 到 Switch B 的 Loopback 接口路由可达。
\# 配置 Switch B。
<SwitchB> system-view [SwitchB] bgp 65009 [SwitchB-bgp-default] router-id 2.2.2.2 [SwitchB-bgp-default] peer 3.3.3.3 as-number 65009 [SwitchB-bgp-default] peer 3.3.3.3 connect-interface loopback 0 [SwitchB-bgp-default] address-family ipv4 unicast [SwitchB-bgp-default-ipv4] peer 3.3.3.3 enable [SwitchB-bgp-default-ipv4] quit [SwitchB-bgp-default] quit [SwitchB] ospf 1 [SwitchB-ospf-1] area 0 [SwitchB-ospf-1-area-0.0.0.0] network 2.2.2.2 0.0.0.0 [SwitchB-ospf-1-area-0.0.0.0] network 9.1.1.0 0.0.0.255 [SwitchB-ospf-1-area-0.0.0.0] quit [SwitchB-ospf-1] quit \# 配置 Switch C。
<SwitchC> system-view [SwitchC] bgp 65009 [SwitchC-bgp-default] router-id 3.3.3.3 [SwitchC-bgp-default] peer 2.2.2.2 as-number 65009 [SwitchC-bgp-default] peer 2.2.2.2 connect-interface loopback 0 [SwitchC-bgp-default] address-family ipv4 unicast [SwitchC-bgp-default-ipv4] peer 2.2.2.2 enable [SwitchC-bgp-default-ipv4] quit [SwitchC-bgp-default] quit [SwitchC] ospf 1 [SwitchC-ospf-1] area 0 [SwitchC-ospf-1-area-0.0.0.0] network 3.3.3.3 0.0.0.0 [SwitchC-ospf-1-area-0.0.0.0] network 9.1.1.0 0.0.0.255 [SwitchC-ospf-1-area-0.0.0.0] quit [SwitchC-ospf-1] quit [SwitchC] display bgp peer ipv4 BGP local router ID : 3.3.3.3 Local AS number : 65009 Total number of peers : 1 Peers in established state : 1
* - Dynamically created peer Peer AS MsgRcvd MsgSent OutQ PrefRcv Up/Down State
2.2.2.2 65009 2 2 0 0 00:00:13 Established

以上显示信息表明 Switch B 和 Switch C 之间的 IBGP 连接已经建立。
(3) 配置 EBGP 连接EBGP 邻居关系的两台路由器（通常属于两个不同运营商），处于不同的 AS 域，对端的(cid:123)
接口一般路由不可达，所以一般使用直连地址建立 邻居。
Loopback EBGP因为要求 C能够访问 A直连的 网段，所以，建立 连接后，Switch Switch 8.1.1.0/24 EBGP (cid:123)
需要将 8.1.1.0/24 网段路由通告到 BGP 路由表中。
\# 配置 Switch A。
<SwitchA> system-view [SwitchA] bgp 65008 [SwitchA-bgp-default] router-id 1.1.1.1 [SwitchA-bgp-default] peer 3.1.1.1 as-number 65009 [SwitchA-bgp-default] address-family ipv4 unicast [SwitchA-bgp-default-ipv4] peer 3.1.1.1 enable [SwitchA-bgp-default-ipv4] network 8.1.1.0 24 [SwitchA-bgp-default-ipv4] quit [SwitchA-bgp-default] quit \# 配置 Switch B。
[SwitchB] bgp 65009 [SwitchB-bgp-default] peer 3.1.1.2 as-number 65008 [SwitchB-bgp-default] address-family ipv4 unicast [SwitchB-bgp-default-ipv4] peer 3.1.1.2 enable [SwitchB-bgp-default-ipv4] quit [SwitchB-bgp-default] quit查看 的 对等体的连接状态。
\# Switch B BGP [SwitchB] display bgp peer ipv4 BGP local router ID : 2.2.2.2 Local AS number : 65009 Total number of peers : 2 Peers in established state : 2
* - Dynamically created peer Peer AS MsgRcvd MsgSent OutQ PrefRcv Up/Down State
3.3.3.3 65009 4 4 0 0 00:02:49 Established
3.1.1.2 65008 2 2 0 0 00:00:05 Established可以看出，Switch B 与 Switch C、Switch B 与 Switch A 之间的 BGP 连接均已建立。
\# 查看 Switch A 的 BGP 路由表。
[SwitchA] display bgp routing-table ipv4 Total number of routes: 1 BGP local router ID is 1.1.1.1 Status codes: * - valid, > - best, d - dampened, h - history, s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete

Network NextHop MED LocPrf PrefVal Path/Ogn
* > 8.1.1.0/24 8.1.1.1 0 32768 i \# 显示 Switch B 的 BGP 路由表。
[SwitchB] display bgp routing-table ipv4 Total number of routes: 1 BGP local router ID is 2.2.2.2 Status codes: * - valid, > - best, d - dampened, h - history, s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn
* >e 8.1.1.0/24 3.1.1.2 0 0 65008i显示 的 路由表。
\# Switch C BGP [SwitchC] display bgp routing-table ipv4 Total number of routes: 1 BGP local router ID is 3.3.3.3 Status codes: * - valid, > - best, d - dampened, h - history, s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn i 8.1.1.0/24 3.1.1.2 0 100 0 65008i从路由表可以看出，Switch A 没有学到 AS 65009 内部的任何路由，Switch C 虽然学到了 AS中的 的路由，但因为下一跳 不可达，所以也不是有效路由。
65008 8.1.1.0 3.1.1.2配置 引入直连路由
(4) BGP在 上配置 引入直连路由，以便 能够获取到网段 的路由，Switch B BGP Switch A 9.1.1.0/24 Switch C 能够获取到网段 3.1.1.0/24 的路由。
\# 配置 Switch B。
[SwitchB] bgp 65009 [SwitchB-bgp-default] address-family ipv4 unicast [SwitchB-bgp-default-ipv4] import-route direct [SwitchB-bgp-default-ipv4] quit [SwitchB-bgp-default] quit \# 显示 Switch A 的 BGP 路由表。
[SwitchA] display bgp routing-table ipv4

Total number of routes: 4 BGP local router ID is 1.1.1.1 Status codes: * - valid, > - best, d - dampened, h - history, s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn
* >e 2.2.2.2/32 3.1.1.1 0 0 65009?
* >e 3.1.1.0/24 3.1.1.1 0 0 65009?
* > 8.1.1.0/24 8.1.1.1 0 32768 i
* >e 9.1.1.0/24 3.1.1.1 0 0 65009?
以上显示信息表明，在 Switch B 上引入直连路由后，Switch A 新增了到达 2.2.2.2/32 和
9.1.1.0/24 的两条路由。
\# 显示 Switch C 的 BGP 路由表。
[SwitchC] display bgp routing-table ipv4 Total number of routes: 4 BGP local router ID is 3.3.3.3 Status codes: * - valid, > - best, d - dampened, h - history, s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn
* >i 2.2.2.2/32 2.2.2.2 0 100 0 ?
* >i 3.1.1.0/24 2.2.2.2 0 100 0 ?
* >i 8.1.1.0/24 3.1.1.2 0 100 0 65008i
* >i 9.1.1.0/24 2.2.2.2 0 100 0 ?
以上显示信息表明，到 的路由变为有效路由，下一跳为 的地址。
8.1.1.0 Switch A

###### 4. 验证配置

\# 使用 Ping 进行验证。
[SwitchC] ping 8.1.1.1 Ping 8.1.1.1 (8.1.1.1): 56 data bytes, press CTRL_C to break 56 bytes from 8.1.1.1: icmp_seq=0 ttl=254 time=10.000 ms 56 bytes from 8.1.1.1: icmp_seq=1 ttl=254 time=4.000 ms 56 bytes from 8.1.1.1: icmp_seq=2 ttl=254 time=4.000 ms 56 bytes from 8.1.1.1: icmp_seq=3 ttl=254 time=3.000 ms 56 bytes from 8.1.1.1: icmp_seq=4 ttl=254 time=3.000 ms
--- Ping statistics for 8.1.1.1 --- 5 packet(s) transmitted, 5 packet(s) received, 0.0% packet loss round-trip min/avg/max/std-dev = 3.000/4.800/10.000/2.638 ms

###### 1. 组网需求

###### 3. 配置步骤

##### 2.11.2 BGP与IGP交互配置

组网需求
1.
公司 A 的所有设备在 AS 65008 内，公司 B 的所有设备在 AS 65009 内，AS 65008 和 AS 65009通过设备 和 相连。
Switch A Switch B现要求实现 Switch A 能够访问 AS 65009 内的网段 9.1.2.0/24，Switch C 能够访问 AS 65008 内的网段 8.1.1.0/24。

###### 2. 组网图

图2-3 BGP 与 IGP 交互配置组网图配置步骤
3.
(1) 配置各接口的 IP 地址（略）
(2) 配置 OSPF在 AS 65009 内配置 OSPF，使得 Switch B 能获取到到 9.1.2.0/24 网段的路由。
\# 配置 Switch B。
<SwitchB> system-view [SwitchB] ospf 1 [SwitchB-ospf-1] area 0 [SwitchB-ospf-1-area-0.0.0.0] network 2.2.2.2 0.0.0.0 [SwitchB-ospf-1-area-0.0.0.0] network 9.1.1.0 0.0.0.255 [SwitchB-ospf-1-area-0.0.0.0] quit [SwitchB-ospf-1] quit配置 C。
\# Switch <SwitchC> system-view [SwitchC] ospf 1 [SwitchC-ospf-1] import-route direct [SwitchC-ospf-1] area 0 [SwitchC-ospf-1-area-0.0.0.0] network 9.1.1.0 0.0.0.255 [SwitchC-ospf-1-area-0.0.0.0] quit [SwitchC-ospf-1] quit
(3) 配置 EBGP 连接配置 EBGP 连接，并在 Switch A 上将 8.1.1.0/24 网段通告到 BGP 路由表中，以便 Switch B获取到网段 的路由。
8.1.1.0/24 \# 配置 Switch A。
<SwitchA> system-view [SwitchA] bgp 65008

[SwitchA-bgp-default] router-id 1.1.1.1 [SwitchA-bgp-default] peer 3.1.1.1 as-number 65009 [SwitchA-bgp-default] address-family ipv4 unicast [SwitchA-bgp-default-ipv4] peer 3.1.1.1 enable [SwitchA-bgp-default-ipv4] network 8.1.1.0 24 [SwitchA-bgp-default-ipv4] quit [SwitchA-bgp-default] quit \# 配置 Switch B。
[SwitchB] bgp 65009 [SwitchB-bgp-default] router-id 2.2.2.2 [SwitchB-bgp-default] peer 3.1.1.2 as-number 65008 [SwitchB-bgp-default] address-family ipv4 unicast [SwitchB-bgp-default-ipv4] peer 3.1.1.2 enable
(4) 配置 BGP 与 IGP 交互在 Switch B 上配置 BGP 引入 OSPF 路由，以便 Switch A 能够获取到到 9.1.2.0/24 网段的(cid:123)
路由。
在 上配置 引入 路由，以便 能够获取到到 网段的Switch B OSPF BGP Switch C 8.1.1.0/24 (cid:123)
路由。
\# 在 Switch B 上配置 BGP 和 OSPF 互相引入路由。
[SwitchB-bgp-default-ipv4] import-route ospf 1 [SwitchB-bgp-default-ipv4] quit [SwitchB-bgp-default] quit [SwitchB] ospf 1 [SwitchB-ospf-1] import-route bgp [SwitchB-ospf-1] quit \# 查看 Switch A 的 BGP 路由表。
[SwitchA] display bgp routing-table ipv4 Total number of routes: 3 BGP local router ID is 1.1.1.1 Status codes: * - valid, > - best, d - dampened, h - history, s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn
* >e 3.3.3.3/32 3.1.1.1 1 0 65009?
* > 8.1.1.0/24 8.1.1.1 0 32768 i
* >e 9.1.2.0/24 3.1.1.1 1 0 65009?
查看 的 路由表。
\# SwitchC OSPF [SwitchC] display ospf routing OSPF Process 1 with Router ID 3.3.3.3 Routing Tables

Routing for Network Destination Cost Type NextHop AdvRouter Area
9.1.1.0/24 1 Transit 9.1.1.2 3.3.3.3 0.0.0.0
2.2.2.2/32 1 Stub 9.1.1.1 2.2.2.2 0.0.0.0 Routing for ASEs Destination Cost Type Tag NextHop AdvRouter
8.1.1.0/24 1 Type2 1 9.1.1.1 2.2.2.2 Total Nets: 3 Intra Area: 2 Inter Area: 0 ASE: 1 NSSA: 0

###### 4. 验证配置

使用 进行验证。
\# Ping [SwitchA] ping -a 8.1.1.1 9.1.2.1 Ping 9.1.2.1 (9.1.2.1) from 8.1.1.1: 56 data bytes, press CTRL_C to break 56 bytes from 9.1.2.1: icmp_seq=0 ttl=254 time=10.000 ms 56 bytes from 9.1.2.1: icmp_seq=1 ttl=254 time=12.000 ms 56 bytes from 9.1.2.1: icmp_seq=2 ttl=254 time=2.000 ms 56 bytes from 9.1.2.1: icmp_seq=3 ttl=254 time=7.000 ms 56 bytes from 9.1.2.1: icmp_seq=4 ttl=254 time=9.000 ms
--- Ping statistics for 9.1.2.1 --- 5 packet(s) transmitted, 5 packet(s) received, 0.0% packet loss round-trip min/avg/max/std-dev = 2.000/8.000/12.000/3.406 ms [SwitchC] ping -a 9.1.2.1 8.1.1.1 Ping 8.1.1.1 (8.1.1.1) from 9.1.2.1: 56 data bytes, press CTRL_C to break 56 bytes from 8.1.1.1: icmp_seq=0 ttl=254 time=9.000 ms 56 bytes from 8.1.1.1: icmp_seq=1 ttl=254 time=4.000 ms 56 bytes from 8.1.1.1: icmp_seq=2 ttl=254 time=3.000 ms 56 bytes from 8.1.1.1: icmp_seq=3 ttl=254 time=3.000 ms 56 bytes from 8.1.1.1: icmp_seq=4 ttl=254 time=3.000 ms
--- Ping statistics for 8.1.1.1 --- 5 packet(s) transmitted, 5 packet(s) received, 0.0% packet loss round-trip min/avg/max/std-dev = 3.000/4.400/9.000/2.332 ms

##### 2.11.3 BGP动态对等体配置

###### 1. 组网需求

所有交换机均运行 BGP 协议。Switch A 需要分别与 Switch B、Switch C 和 Switch D 建立 IBGP 连接。在 Switch A 上配置 BGP 动态对等体，以简化配置。
配置 作为路由反射器，在 、 和 之间反射路由。
Switch A Switch B Switch C Switch D

###### 2. 组网图

图2-4 BGP 动态对等体配置组网图AS 200 Vlan-int10
10.1.1.2/24 Switch B Vlan-int10
10.1.1.1/24 Vlan-int9 Vlan-int20
9.1.1.1
10.1.2.1/24 Switch A Vlan-int20
10.1.2.2/24 Vlan-int30 Switch C S2/1
10.1.3.1/24 Switch D Vlan-int30
10.1.3.2/24

###### 3. 配置步骤

配置各接口的 地址（略）
(1) IP配置 连接
(2) IBGP \# 在 Switch A 上配置 BGP 动态对等体。
<SwitchA> system-view [SwitchA] bgp 200 [SwitchA-bgp-default] router-id 1.1.1.1 [SwitchA-bgp-default] peer 10.1.0.0 16 as-number 200 [SwitchA-bgp-default] address-family ipv4 [SwitchA-bgp-default-ipv4] peer 10.1.0.0 16 enable \# 在 Switch B 上配置与 Switch A 建立 IBGP 连接。
<SwitchB> system-view [SwitchB] bgp 200 [SwitchB-bgp-default] router-id 2.2.2.2 [SwitchB-bgp-default] peer 10.1.1.1 as-number 200 [SwitchB-bgp-default] address-family ipv4 [SwitchB-bgp-default-ipv4] peer 10.1.1.1 enable \# 在 Switch C 上配置与 Switch A 建立 IBGP 连接。
<SwitchC> system-view [SwitchC] bgp 200 [SwitchC-bgp-default] router-id 3.3.3.3 [SwitchC-bgp-default] peer 10.1.2.1 as-number 200 [SwitchC-bgp-default] address-family ipv4 [SwitchC-bgp-default-ipv4] peer 10.1.2.1 enable \# 在 Switch D 上配置与 Switch A 建立 IBGP 连接。
<SwitchD> system-view

[SwitchD] bgp 200 [SwitchD-bgp-default] router-id 4.4.4.4 [SwitchD-bgp-default] peer 10.1.3.1 as-number 200 [SwitchD-bgp-default] address-family ipv4 [SwitchD-bgp-default-ipv4] peer 10.1.3.1 enable \# 查看 Switch A 的 BGP 对等体的连接状态。
[SwitchA] display bgp peer ipv4 BGP local router ID : 1.1.1.1 Local AS number : 200 Total number of peers : 3 Peers in established state : 3
* - Dynamically created peer Peer AS MsgRcvd MsgSent OutQ PrefRcv Up/Down State
*10.1.1.2 200 7 10 0 0 00:06:09 Established
*10.1.2.2 200 7 10 0 0 00:06:09 Established
*10.1.3.2 200 7 10 0 0 00:06:09 Established以上显示信息表明 Switch A 与 Switch B、Switch C 和 Switch D 之间的 IBGP 连接已经建立。
(3) 配置路由反射器\# 配置 Switch A 作为路由反射器，将网段 10.1.0.0/16 中的对等体作为路由反射的客户机。
[SwitchA-bgp-default-ipv4] peer 10.1.0.0 16 reflect-client
(4) 配置发布网段路由\# 在 Switch C 上配置发布网段路由 9.1.1.0/24。
[SwitchC-bgp-default-ipv4] network 9.1.1.0 24

###### 4. 验证配置

\# 在 Switch A、Switch B 和 Switch D 上查看 BGP 路由表，可以看到均已学习到路由 9.1.1.0/24。
以 Switch A 为例：
[SwitchA-bgp-default] display bgp routing-table ipv4 Total Number of Routes: 1 BGP Local router ID is 1.1.1.1 Status codes: * - valid, > - best, d - dampened, h - history, s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn
* i 9.1.1.0/24 10.1.2.2 0 100 0 ?

###### 1. 组网需求

###### 2. 组网图

###### 3. 配置步骤

##### 2.11.4 BGP路由聚合配置

组网需求
1.
通过在边界设备 Switch C 和外部网络设备 Switch D 之间建立 EBGP 连接，实现公司内部网络与外部网络的互通。
在公司内部，核心层设备 Switch B 与汇聚层设备 Switch A 之间配置静态路由，Switch B 与 Switch C 之间配置 OSPF，并在 OSPF 路由中引入静态路由，以实现公司内部网络的互通。
公司内部网络包括三个网段：192.168.64.0/24、192.168.74.0/24 和 192.168.99.0/24。在Switch C上配置路由聚合，将这三个网段的路由聚合为一条路由，以减少通过 BGP 发布的路由数量。
组网图
2.
图2-5 BGP 路由聚合组网图配置步骤
3.
(1) 配置各接口的 IP 地址（略）
(2) 在 Switch A 和 Switch B 之间配置静态路由\# 在 Switch A 上配置缺省路由，下一跳为 Switch B。
<SwitchA> system-view [SwitchA] ip route-static 0.0.0.0 0 192.168.212.1 \# 在 Switch B 上配置静态路由，到达目的网络 192.168.64.0/24、192.168.74.0/24 和的路由下一跳均为 A。
192.168.99.0/24 Switch <SwitchB> system-view [SwitchB] ip route-static 192.168.64.0 24 192.168.212.161 [SwitchB] ip route-static 192.168.74.0 24 192.168.212.161 [SwitchB] ip route-static 192.168.99.0 24 192.168.212.161
(3) 在 Switch B 和 Switch C 之间配置 OSPF，并引入静态路由\# 在 Switch B 上配置 OSPF 发布本地网段路由，并引入静态路由。
[SwitchB] ospf [SwitchB-ospf-1] area 0 [SwitchB-ospf-1-area-0.0.0.0] network 172.17.100.0 0.0.0.255 [SwitchB-ospf-1-area-0.0.0.0] quit

[SwitchB-ospf-1] import-route static [SwitchB-ospf-1] quit \# 在 Switch C 上配置 OSPF 发布本地网段路由。
[SwitchC] ospf [SwitchC-ospf-1] area 0 [SwitchC-ospf-1-area-0.0.0.0] network 172.17.100.0 0.0.0.255 [SwitchC-ospf-1-area-0.0.0.0] network 10.220.2.0 0.0.0.255 [SwitchC-ospf-1-area-0.0.0.0] quit [SwitchC-ospf-1] quit在 上查看路由表信息，可以看到 通过 学习到了到达\# Switch C Switch C OSPF
192.168.64.0/24、192.168.74.0/24 和 192.168.99.0/24 网段的路由。
[SwitchC] display ip routing-table protocol ospf Summary count : 5 OSPF Routing table Status : <Active> Summary count : 3 Destination/Mask Proto Pre Cost NextHop Interface
192.168.64.0/24 OSPF 150 1 172.17.100.1 Vlan100
192.168.74.0/24 OSPF 150 1 172.17.100.1 Vlan100
192.168.99.0/24 OSPF 150 1 172.17.100.1 Vlan100 OSPF Routing table Status : <Inactive> Summary count : 2 Destination/Mask Proto Pre Cost NextHop Interface
10.220.2.0/24 OSPF 10 1 10.220.2.16 Vlan200
172.17.100.0/24 OSPF 10 1 172.17.100.2 Vlan100
(4) 在 Switch C 和 Switch D 之间配置 BGP，并引入 OSPF 路由\# 在 Switch C 上配置 Switch D 为其 EBGP 对等体，并引入 OSPF 路由。
[SwitchC] bgp 65106 [SwitchC-bgp-default] router-id 3.3.3.3 [SwitchC-bgp-default] peer 10.220.2.217 as-number 64631 [SwitchC-bgp-default] address-family ipv4 unicast [SwitchC-bgp-default-ipv4] peer 10.220.2.217 enable [SwitchC-bgp-default-ipv4] import-route ospf \# 在 Switch D 上配置 Switch C 为其 EBGP 对等体。
[SwitchD] bgp 64631 [SwitchD-bgp-default] router-id 4.4.4.4 [SwitchD-bgp-default] peer 10.220.2.16 as-number 65106 [SwitchD-bgp-default] address-family ipv4 unicast [SwitchD-bgp-default-ipv4] peer 10.220.2.16 enable [SwitchD-bgp-default-ipv4] quit [SwitchD-bgp-default] quit \# 在 Switch D 上查看路由表信息，可以看到 Switch D 通过 BGP 学习到了到达
192.168.64.0/24、192.168.74.0/24 和 192.168.99.0/24 三个网段的路由。

[SwitchD] display ip routing-table protocol bgp Summary count : 3 BGP Routing table Status : <Active> Summary count : 3 Destination/Mask Proto Pre Cost NextHop Interface
192.168.64.0/24 BGP 255 1 10.220.2.16 Vlan200
192.168.74.0/24 BGP 255 1 10.220.2.16 Vlan200
192.168.99.0/24 BGP 255 1 10.220.2.16 Vlan200 BGP Routing table Status : <Inactive> Summary count : 0完成上述配置后，在 Switch D 上可以 ping 通 192.168.64.0/24、192.168.74.0/24 和
192.168.99.0/24 网段内的主机。
(5) 在 Switch C 上配置路由聚合\# 在 Switch C 上将路由 192.168.64.0/24、192.168.74.0/24 和 192.168.99.0/24 聚合为
192.168.64.0/18，并抑制发布具体路由。
[SwitchC-bgp-default-ipv4] aggregate 192.168.64.0 18 detail-suppressed [SwitchC-bgp-default-ipv4] quit [SwitchC-bgp-default] quit

###### 4. 验证配置

\# 在 Switch C 上查看路由表信息，可以看到 Switch C 上产生了一条聚合路由 192.168.64.0/18，该聚合路由的出接口为 Null0。
[SwitchC] display ip routing-table | include 192.168
192.168.64.0/18 BGP 130 0 127.0.0.1 NULL0
192.168.64.0/24 OSPF 150 1 172.17.100.1 Vlan100
192.168.74.0/24 OSPF 150 1 172.17.100.1 Vlan100
192.168.99.0/24 OSPF 150 1 172.17.100.1 Vlan100 \# 在 Switch D 上查看路由表信息，可以看到 Switch D 上到达公司内部三个网络的路由聚合为一条路由 192.168.64.0/18。
[SwitchD] display ip routing-table protocol bgp Summary count : 1 BGP Routing table Status : <Active> Summary count : 1 Destination/Mask Proto Pre Cost NextHop Interface
192.168.64.0/18 BGP 255 0 10.220.2.16 Vlan200 BGP Routing table Status : <Inactive> Summary count : 0完成上述配置后，成功实现了路由聚合。并且，在 Switch D 上可以 ping 通 192.168.64.0/24、和 网段内的主机。
192.168.74.0/24 192.168.99.0/24

###### 1. 组网需求

###### 2. 组网图

##### 2.11.5 MBGP配置

组网需求
1.
• 网络中存在两个自治系统：PIM-SM 1 属于 AS 100，PIM-SM 2 属于 AS 200。各 AS 内部采用 交换路由信息，AS 之间采用 交换用于 检查的 单播路由信息。
OSPF MBGP RPF IPv4组播源属于 AS 100 内的 PIM-SM 1，接收者则属于 AS 200 内的 PIM-SM 2。
•将 Switch A 和 Switch B 各自的 Loopback0 接口分别配置为各自 PIM-SM 域的 C-BSR 和
•C-RP。
在 与 之间通过 建立 MSDP（Multicast Protocol，
• Switch A Switch B MBGP Source Discovery组播源发现协议）对等体关系。
组网图
2.
图2-6 MBGP 配置组网图AS 100 AS 200 Loop0 Loop0 Vlan-int101 Vlan-int101 Switch B Switch A Receiver Vlan-int100 3 l a 0 n
- 1 i n t n i t 1 n - 0 a V l 0 V 0 1 0 n t l a 2 i n t
- - n Source n i n - i a n V l t 1 a Switch D 0 l 2 V Vlan-int104 Switch C Vlan-int104 PIM-SM 1 Loop0 Loop0 PIM-SM 2 MBGP peers

| 接口 | IP地址 | 设备 | 接口 |
|---|---|---|---|
| - | 10.110.1.100/24 | Switch C | Vlan-int200 |
| Vlan-int100 | 10.110.1.1/24 |  | Vlan-int102 |
| Vlan-int101 | 192.168.1.1/24 |  | Vlan-int104 |
| Loop0 | 1.1.1.1/32 |  | Loop0 |
| Vlan-int101 | 192.168.1.2/24 | Switch D | Vlan-int103 |
| Vlan-int102 | 192.168.2.1/24 |  | Vlan-int104 |
| Vlan-int103 | 192.168.3.1/24 |  | Loop0 |
| Loop0 | 2.2.2.2/32 |  |  |

设备 IP地址Source 10.110.2.1/24 Switch A 192.168.2.2/24
192.168.4.1/24
3.3.3.3/32 Switch B 192.168.3.2/24
192.168.4.2/24
4.4.4.4/32

###### 3. 配置步骤

(1) 配置各交换机接口的 IP 地址和单播路由协议
• 请按照 图 2-6 配置各接口的IP地址和子网掩码，具体配置过程略。

配置 AS 200 内的各交换机之间采用 OSPF 路由协议交换路由信息（AS 内各路由器使用的
•进程号为 1），确保各 内部在网络层互通，能学到彼此 接口的路由，具体OSPF AS Loopback配置过程略。
(2) 使能 IP 组播路由，使能 PIM-SM 和 IGMP，并配置 BSR 的服务边界\# 在 Switch A 上使能 IP 组播路由，在各接口上使能 PIM-SM。
<SwitchA> system-view [SwitchA] multicast routing [SwitchA-mrib] quit [SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] pim sm [SwitchA-Vlan-interface100] quit [SwitchA] interface vlan-interface 101 [SwitchA-Vlan-interface101] pim sm [SwitchA-Vlan-interface101] quit Switch B 和 Switch D 上的配置与 Switch A 相似，配置过程略。
\# 在 Switch C 上使能 IP 组播路由，在各接口上使能 PIM-SM，并在主机侧接口Vlan-interface200 上使能 IGMP。
<SwitchC> system-view [SwitchC] multicast routing [SwitchA-mrib] quit [SwitchC] interface vlan-interface 102 [SwitchC-Vlan-interface102] pim sm [SwitchC-Vlan-interface102] quit [SwitchC] interface vlan-interface 104 [SwitchC-Vlan-interface104] pim sm [SwitchC-Vlan-interface104] quit [SwitchC] interface vlan-interface 200 [SwitchC-Vlan-interface200] pim sm [SwitchC-Vlan-interface200] igmp enable [SwitchC-Vlan-interface200] quit在 上配置 的服务边界。
\# Switch A BSR [SwitchA] interface vlan-interface 101 [SwitchA-Vlan-interface101] pim bsr-boundary [SwitchA-Vlan-interface101] quit在 上配置 的服务边界。
\# Switch B BSR [SwitchB] interface vlan-interface 101 [SwitchB-Vlan-interface101] pim bsr-boundary [SwitchB-Vlan-interface101] quit配置 接口和 C-BSR、C-RP 的位置
(3) Loopback0在 上配置 接口和 C-BSR、C-RP 的位置。
\# Switch A Loopback0 [SwitchA] interface loopback 0 [SwitchA-LoopBack0] ip address 1.1.1.1 32 [SwitchA-LoopBack0] pim sm [SwitchA-LoopBack0] quit [SwitchA] pim [SwitchA-pim] c-bsr 1.1.1.1

###### 4. 验证配置

[SwitchA-pim] c-rp 1.1.1.1 [SwitchA-pim] quit \# 在 Switch B 上配置 Loopback0 接口和 C-BSR、C-RP 的位置。
[SwitchB] interface loopback 0 [SwitchB-LoopBack0] ip address 2.2.2.2 32 [SwitchB-LoopBack0] pim sm [SwitchB-LoopBack0] quit [SwitchB] pim [SwitchB-pim] c-bsr 2.2.2.2 [SwitchB-pim] c-rp 2.2.2.2 [SwitchB-pim] quit
(4) 配置 BGP 协议，建立 BGP IPv4 组播对等体，并引入路由\# 在 Switch A 上配置其与 Switch B 建立 EBGP 会话，使能 Switch A 与 Switch B 交换用于RPF 检查的 IPv4 单播路由的能力，并引入直连路由。
[SwitchA] bgp 100 [SwitchA-bgp-default] router-id 1.1.1.1 [SwitchA-bgp-default] peer 192.168.1.2 as-number 200 [SwitchA-bgp-default] address-family ipv4 multicast [SwitchA-bgp-default-mul-ipv4] peer 192.168.1.2 enable [SwitchA-bgp-default-mul-ipv4] import-route direct [SwitchA-bgp-default-mul-ipv4] quit [SwitchA-bgp-default] quit在 上配置其与 建立 会话，使能 与 交换用于\# Switch B Switch A EBGP Switch A Switch B RPF 检查的 IPv4 单播路由的能力，并引入 OSPF 路由。
[SwitchB] bgp 200 [SwitchB-bgp-default] router-id 2.2.2.2 [SwitchB-bgp-default] peer 192.168.1.1 as-number 100 [SwitchB-bgp-default] address-family ipv4 multicast [SwitchB-bgp-default-mul-ipv4] peer 192.168.1.1 enable [SwitchB-bgp-default-mul-ipv4] import-route ospf 1 [SwitchB-bgp-default-mul-ipv4] quit [SwitchB-bgp-default] quit
(5) 配置 MSDP 对等体\# 在 Switch A 上配置 MSDP 对等体。
[SwitchA] msdp [SwitchA-msdp] peer 192.168.1.2 connect-interface vlan-interface 101 [SwitchA-msdp] quit \# 在 Switch B 上配置 MSDP 对等体。
[SwitchB] msdp [SwitchB-msdp] peer 192.168.1.1 connect-interface vlan-interface 101 [SwitchB-msdp] quit验证配置
4.
\# 执行 display bgp peer ipv4 multicast 命令查看 BGP IPv4 组播对等体。以 Switch B 为例：
[SwitchB] display bgp peer ipv4 multicast

###### 1. 组网需求

###### 2. 组网图

BGP local router ID : 2.2.2.2 Local AS number : 200 Total number of peers : 3 Peers in established state : 3 Peer AS MsgRcvd MsgSent OutQ PrefRcv Up/Down State
192.168.1.1 100 56 56 0 0 00:40:54 Established \# 执行 display msdp brief 命令查看路由器之间 MSDP 对等体的建立情况。以 Switch B 为例：
[SwitchB] display msdp brief Configured Established Listen Connect Shutdown Disabled 1 1 0 0 0 0 Peer address State Up/Down time AS SA count Reset count
192.168.1.1 Established 00:07:17 100 1 0

#### 2.12 搭建基本IPv6 BGP网络典型配置举例

##### 2.12.1 IPv6 BGP基本配置

组网需求
1.
如 图 2-7 所示，所有交换机均运行IPv6 BGP协议。Switch A位于AS 65008；Switch B和Switch C位于AS 65009。要求Switch A和Switch B之间建立EBGP连接，Switch B和Switch C之间建立IBGP连接，使得Switch C能够访问Switch A直连的 50::/64 网段。
组网图
2.
图2-7 IPv6 BGP 基本配置组网图

###### 3. 配置步骤

配置各接口的 地址及 接口的 地址（略）
(1) IPv6 Loopback IPv4配置 连接
(2) IBGP配置 B。
\# Switch <SwitchB> system-view [SwitchB] bgp 65009 [SwitchB-bgp-default] router-id 2.2.2.2 [SwitchB-bgp-default] peer 9::2 as-number 65009 [SwitchB-bgp-default] address-family ipv6 [SwitchB-bgp-default-ipv6] peer 9::2 enable

###### 4. 验证配置

[SwitchB-bgp-default-ipv6] quit \# 配置 Switch C。
<SwitchC> system-view [SwitchC] bgp 65009 [SwitchC-bgp-default] router-id 3.3.3.3 [SwitchC-bgp-default] peer 9::1 as-number 65009 [SwitchC-bgp-default] address-family ipv6 [SwitchC-bgp-default-ipv6] peer 9::1 enable
(3) 配置 EBGP 连接\# 配置 Switch A。
<SwitchA> system-view [SwitchA] bgp 65008 [SwitchA-bgp-default] router-id 1.1.1.1 [SwitchA-bgp-default] peer 10::1 as-number 65009 [SwitchA-bgp-default] address-family ipv6 [SwitchA-bgp-default-ipv6] peer 10::1 enable \# 配置 Switch B。
[SwitchB-bgp-default] peer 10::2 as-number 65008 [SwitchB-bgp-default] address-family ipv6 [SwitchB-bgp-default-ipv6] peer 10::2 enable
(4) 配置通过 IPv6 BGP 发布的网段路由\# 配置 Switch A。
[SwitchA-bgp-default-ipv6] network 10:: 64 [SwitchA-bgp-default-ipv6] network 50:: 64 [SwitchA-bgp-default-ipv6] quit [SwitchA-bgp-default] quit \# 配置 Switch B。
[SwitchB-bgp-default-ipv6] network 10:: 64 [SwitchB-bgp-default-ipv6] network 9:: 64 [SwitchB-bgp-default-ipv6] quit [SwitchB-bgp-default] quit \# 配置 Switch C。
[SwitchC-bgp-default-ipv6] network 9:: 64 [SwitchC-bgp-default-ipv6] quit [SwitchC-bgp-default] quit验证配置
4.
\# 在 Switch B 上查看 IPv6 BGP 对等体的信息。可以看出，Switch A 和 Switch B 之间建立了 EBGP连接，Switch 和 之间建立了 连接。
B Switch C IBGP [SwitchB] display bgp peer ipv6 BGP local router ID: 2.2.2.2 Local AS number: 65009 Total number of peers: 2 Peers in established state: 2
* - Dynamically created peer

Peer AS MsgRcvd MsgSent OutQ PrefRcv Up/Down State 9::2 65009 41 43 0 1 00:29:00 Established 10::2 65008 38 38 0 2 00:27:20 Established \# 在 Switch A 上查看 IPv6 BGP 路由表信息。可以看出，Switch A 学习到了 AS 65009 内的路由信息。
[SwitchA] display bgp routing-table ipv6 Total number of routes: 4 BGP local router ID is 1.1.1.1 Status codes: * - valid, > - best, d - dampened, h - history, s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete
* >e Network : 9:: PrefixLen : 64 NextHop : 10::1 LocPrf :
PrefVal : 0 OutLabel : NULL MED : 0 Path/Ogn: 65009i
* > Network : 10:: PrefixLen : 64 NextHop : :: LocPrf :
PrefVal : 32768 OutLabel : NULL MED : 0 Path/Ogn: i
* e Network : 10:: PrefixLen : 64 NextHop : 10::1 LocPrf :
PrefVal : 0 OutLabel : NULL MED : 0 Path/Ogn: 65009i
* > Network : 50:: PrefixLen : 64 NextHop : :: LocPrf :
PrefVal : 32768 OutLabel : NULL MED : 0 Path/Ogn: i \# 在 Switch C 上查看 IPv6 BGP 路由表信息。可以看出，Switch C 学习到了到达 50::/64 网段的路由。
[SwitchC] display bgp routing-table ipv6 Total number of routes: 4 BGP local router ID is 3.3.3.3 Status codes: * - valid, > - best, d - dampened, h - history, s - suppressed, S - stale, i - internal, e - external

a – additional-path Origin: i - IGP, e - EGP, ? - incomplete
* > Network : 9:: PrefixLen : 64 NextHop : :: LocPrf :
PrefVal : 32768 OutLabel : NULL MED : 0 Path/Ogn: i
* i Network : 9:: PrefixLen : 64 NextHop : 9::1 LocPrf : 100 PrefVal : 0 OutLabel : NULL MED : 0 Path/Ogn: i
* >i Network : 10:: PrefixLen : 64 NextHop : 9::1 LocPrf : 100 PrefVal : 0 OutLabel : NULL MED : 0 Path/Ogn: i
* >i Network : 50:: PrefixLen : 64 NextHop : 10::2 LocPrf : 100 PrefVal : 0 OutLabel : NULL MED : 0 Path/Ogn: 65008i \# 在 Switch C 上可以 ping 通 50::/64 网段内的主机。（略）

##### 2.12.2 IPv6 MBGP配置

###### 1. 组网需求

• 网络中存在两个自治系统：IPv6 PIM-SM 1 属于 AS 100，IPv6 PIM-SM 2 属于 AS 200。各
AS 内部采用 OSPFv3 交换路由信息，AS 之间采用 IPv6 MBGP 交换用于 RPF 检查的 IPv6
单播路由信息。
IPv6 组播源属于 AS 100 内的 IPv6 PIM-SM 1，接收者则属于 AS 200 内的 IPv6 PIM-SM 2。
•
在 Switch A 和 Switch B 上使能 Anycast-RP 功能。
•

###### 2. 组网图

图2-8 IPv6 MBGP 配置组网图l a 0 n 1 - i n t n t 1
- i n 0 a 2 V l 0 V 0 1 0 t l a 2 n n t
- i n n - i i a n n - V l t 1 a V l

| 接口 | IP地址 | 设备 | 接口 |
|---|---|---|---|
| - | 1002::100/64 | Switch B | Vlan-int101 |
| Vlan-int100 | 1002::1/64 |  | Vlan-int102 |
| Vlan-int101 | 1001::1/64 |  | Vlan-int103 |
| Loop0 | 1:1::1/128 |  | Loop0 |
| Loop1 | 1:1::2/128 |  | Loop1 |
| Vlan-int200 | 3002::1/64 | Switch D | Vlan-int103 |
| Vlan-int102 | 2001::2/64 |  | Vlan-int104 |
| Vlan-int104 | 3001::1/64 |  |  |

设备 IP地址Source 1001::2/64 Switch A 2001::1/64 2002::1/64 1:1::1/128 2:2::2/128 Switch C 2002::2/64 3001::2/64

###### 3. 配置步骤

配置 地址和 单播路由协议
(1) IPv6 IPv6按照 图 配置各接口的IPv6 地址和前缀长度，具体配置过程略。
2-8配置 AS 200 内的各交换机之间采用 OSPFv3 路由协议交换路由信息（AS 内各交换机使用的进程号为 1），确保各 内部在网络层互通，具体配置过程略。
OSPFv3 AS使能 组播路由，使能 和 MLD，并配置 的服务边界
(2) IPv6 IPv6 PIM-SM BSR在 上使能 组播路由，在各接口上使能 PIM-SM。
\# Switch A IPv6 IPv6 <SwitchA> system-view [SwitchA] ipv6 multicast routing [SwitchA-mrib6] quit [SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] ipv6 pim sm [SwitchA-Vlan-interface100] quit [SwitchA] interface vlan-interface 101 [SwitchA-Vlan-interface101] ipv6 pim sm [SwitchA-Vlan-interface101] quit [SwitchA] interface loopback 0

[SwitchA-LoopBack0] ipv6 pim sm [SwitchA-LoopBack0] quit Switch B 和 Switch D 上的配置与 Switch A 相似，配置过程略。
在 上使能 组播路由，在各接口上使能 PIM-SM，并在主机侧接口\# Switch C IPv6 IPv6 Vlan-interface200 上使能 MLD。
<SwitchC> system-view [SwitchC] ipv6 multicast routing [SwitchC-mrib6] quit [SwitchC] interface vlan-interface 102 [SwitchC-Vlan-interface102] ipv6 pim sm [SwitchC-Vlan-interface102] quit [SwitchC] interface vlan-interface 104 [SwitchC-Vlan-interface104] ipv6 pim sm [SwitchC-Vlan-interface104] quit [SwitchC] interface vlan-interface 200 [SwitchC-Vlan-interface200] ipv6 pim sm [SwitchC-Vlan-interface200] mld enable [SwitchC-Vlan-interface200] quit在 上配置 的服务边界。
\# Switch A BSR [SwitchA] interface vlan-interface 101 [SwitchA-Vlan-interface101] ipv6 pim bsr-boundary [SwitchA-Vlan-interface101] quit在 上配置 的服务边界。
\# Switch B BSR [SwitchB] interface vlan-interface 101 [SwitchB-Vlan-interface101] ipv6 pim bsr-boundary [SwitchB-Vlan-interface101] quit使能 功能，并指定 和
(3) Anycast-RP C-BSR C-RP \# 配置 Switch A。
[SwitchA] ipv6 pim [SwitchA-pim6] anycast-rp 1:1::1 1:1::2 [SwitchA-pim6] anycast-rp 1:1::1 2:2::2 [SwitchA-pim6] c-bsr 1:1::1 [SwitchA-pim6] c-rp 1:1::1 [SwitchA-pim6] quit \# 配置 Switch B。
[SwitchB] ipv6 pim [SwitchB-pim6] anycast-rp 1:1::1 1:1::2 [SwitchB-pim6] anycast-rp 1:1::1 2:2::2 [SwitchB-pim6] c-bsr 1:1::1 [SwitchB-pim6] c-rp 1:1::1 [SwitchB-pim6] quit
(4) 配置 BGP 协议，建立 BGP IPv6 组播对等体，并引入路由\# 在 Switch A 上配置其与 Switch B 建立 EBGP 会话，使能 Switch A 与 Switch B 交换用于检查的 单播路由的能力，并引入直连路由。
RPF IPv6 [SwitchA] bgp 100 [SwitchA-bgp-default] router-id 1.1.1.1

[SwitchA-bgp-default] peer 1001::2 as-number 200 [SwitchA-bgp-default] address-family ipv6 multicast [SwitchA-bgp-default-mul-ipv6] peer 1001::2 enable [SwitchA-bgp-default-mul-ipv6] import-route direct [SwitchA-bgp-default-mul-ipv6] quit \# 在 Switch B 上配置其与 Switch A 建立 EBGP 会话，使能 Switch A 与 Switch B 交换用于RPF 检查的 IPv6 单播路由的能力，并引入 OSPFv3 路由。
[SwitchB] bgp 200 [SwitchB-bgp-default] router-id 2.2.2.2 [SwitchB-bgp-default] peer 1001::1 as-number 100 [SwitchB-bgp-default] address-family ipv6 multicast [SwitchB-bgp-default-mul-ipv6] peer 1001::1 enable [SwitchB-bgp-default-mul-ipv6] import-route ospfv3 1 [SwitchB-bgp-default-mul-ipv6] quit在 和 之间建立 单播对等体，并引入路由，以便在不同域的两个
(5) Switch A Switch B BGP IPv6 RP 之间转发注册报文\# 在 Switch A 上使能与 Switch B 交换 IPv6 单播路由的能力，并引入直连路由。
[SwitchA-bgp-default] address-family ipv6 unicast [SwitchA-bgp-default-ipv6] peer 1001::2 enable [SwitchA-bgp-default-ipv6] import-route direct [SwitchA-bgp-default-ipv6] quit [SwitchA-bgp-default] quit \# 在 Switch B 上使能与 Switch A 交换 IPv6 单播路由的能力，并引入直连路由。
[SwitchB-bgp-default] address-family ipv6 unicast [SwitchB-bgp-default-ipv6] peer 1001::1 enable [SwitchB-bgp-default-ipv6] import-route direct [SwitchB-bgp-default-ipv6] quit [SwitchB-bgp-default] quit

###### 4. 验证配置

\# 执行 display bgp peer ipv6 multicast 命令查看 BGP IPv6 组播对等体。以 Switch B 为例：
[SwitchB] display bgp peer ipv6 multicast BGP local router ID : 2.2.2.2 Local AS number : 200 Total number of peers : 3 Peers in established state : 3 Peer AS MsgRcvd MsgSent OutQ PrefRcv Up/Down State 1001::1 100 56 56 0 0 00:40:54 Established \# 执行 display ipv6 multicast rpf-info 命令查看组播源的 RPF 信息。以 Switch B 为例：
[SwitchB] display ipv6 multicast rpf-info 1002::1 RPF information about source 1002::1:
RPF interface: Vlan-interface101, RPF neighbor: 1001::1 Referenced prefix/prefix length: 1002::/64 Referenced route type: mbgp

Route selection rule: preference-preferred Load splitting rule: disable

#### 2.13 BGP常见错误配置举例

##### 2.13.1 连接无法进入Established状态

###### 1. 故障现象

使用 display bgp peer ipv4 unicast 命令或 display bgp peer ipv6 unicast 命令查看 BGP 对等体的信息，发现与对端的连接无法进入 Established 状态。

###### 2. 故障分析

邻居的建立需要能够使用 端口建立 会话，以及能够正确交换 消息。
BGP 179 TCP Open

###### 3. 故障处理

(1) 执行 display current-configuration 命令查看当前配置，检查邻居的 AS 号配置是否
正确。
(2) 执行 display bgp peer ipv4 unicast 命令或 display bgp peer ipv6 unicast
命令检查邻居的 IP 地址/IPv6 地址是否正确。
(3) 如果使用 Loopback 接口，检查是否配置了 peer connect-interface 命令。
(4) 如果是物理上非直连的 EBGP 邻居，检查是否配置了 peer ebgp-max-hop 命令。
(5) 如果配置了 peer ttl-security hops 命令，请检查对端是否也配置了该命令，且保证双
方配置的 hop-count 不小于两台设备实际需要经过的跳数。
(6) 检查路由表中是否存在到邻居的可用路由。
(7) 使用 ping 命令检查链路是否畅通。
(8) 使用 display tcp verbose 命令或 display ipv6 tcp verbose 命令检查 TCP 连接
是否正常。
检查是否配置了禁止 端口 的 ACL。
(9) TCP 179

##### 1. 功能简介

### 3 大规模BGP网络

#### 3.1 大规模BGP网络的配置任务简介

大规模 BGP 网络配置任务如下：
• 配置BGP路由衰减
• 配置BGP团体
• 配置BGP路由反射
• 配置BGP联盟BGP联盟基本配置(cid:123)
（可选）配置联盟兼容性(cid:123)

#### 3.2 配置BGP路由衰减

功能简介
1.
通过配置 BGP 路由衰减，可以抑制不稳定的路由信息，不允许这类路由参与路由选择。

##### 2. 配置限制和指导

本配置只对 EBGP 路由生效，对 IBGP 路由无效。
配置本功能后，EBGP 邻居 down 了之后，来自该邻居的路由不会被删除，而是进行路由衰减。

##### 3. 配置步骤（IPv4单播/IPv4组播）

进入系统视图。
(1)
system-view进入 单播地址族视图、BGP-VPN 单播地址族视图或 组播地址族视
(2) BGP IPv4 IPv4 BGP IPv4图。
请依次执行以下命令进入 BGP IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv4 [ unicast ]请依次执行以下命令进入 单播地址族视图。
BGP-VPN IPv4 (cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv4 [ unicast ]请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv4 multicast
(3) 配置 BGP 路由衰减。
dampening [ half-life-reachable half-life-unreachable reuse suppress ceiling | route-policy route-policy-name ] *

缺省情况下，未配置 BGP 路由衰减。

##### 4. 配置步骤（IPv6单播/IPv6组播）

进入系统视图。
(1)
system-view进入 单播地址族视图、BGP-VPN 单播地址族视图或 组播地址族视
(2) BGP IPv6 IPv6 BGP IPv6图。
请依次执行以下命令进入 BGP IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 [ unicast ]请依次执行以下命令进入 单播地址族视图。
BGP-VPN IPv6 (cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv6 [ unicast ]请依次执行以下命令进入 BGP IPv6 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 multicast
(3) 配置 IPv6 BGP 路由衰减。
dampening [ half-life-reachable half-life-unreachable reuse suppress ceiling | route-policy route-policy-name ] *缺省情况下，未配置 路由衰减。
IPv6 BGP

#### 3.3 配置BGP团体

##### 1. 功能简介

缺省情况下，本地路由器不向对等体/对等体组发布团体属性和扩展团体属性。如果接收到的路由中携带团体属性或扩展团体属性，则本地路由器删除该团体属性或扩展团体属性后，再将路由发布给对等体/对等体组。
通过本配置可以允许本地路由器在向对等体发布路由时携带团体属性或扩展团体属性，以便根据团体属性或扩展团体属性对路由进行过滤和控制。本配置和路由策略配合使用，可以灵活地控制路由中携带的团体属性和扩展团体属性值，例如在路由中添加团体属性或扩展团体属性、修改路由中原有的团体属性或扩展团体属性值。路由策略的详细介绍，请参见“三层技术-IP 路由配置指导”中的“路由策略”。

##### 2. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
进入 单播地址族视图、 单播地址族视图或 组播地址族视
(2) BGP IPv4 BGP-VPN IPv4 BGP IPv4
图。
请依次执行以下命令进入 BGP IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]

address-family ipv4 [ unicast ]请依次执行以下命令进入 BGP-VPN IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv4 [ unicast ]请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv4 multicast
(3) 配置向对等体/对等体组发布团体属性。
peer { group-name | ipv4-address [ mask-length ] } advertise-community缺省情况下，不向对等体/对等体组发布团体属性。
(4) 配置向对等体/对等体组发布扩展团体属性。
peer { group-name | ipv4-address [ mask-length ] } advertise-ext-community缺省情况下，不向对等体/对等体组发布扩展团体属性。
(5) （可选）对发布给对等体/对等体组的路由指定路由策略。
peer { group-name | ipv4-address [ mask-length ] } route-policy route-policy-name export缺省情况下，不指定对等体/对等体组的路由策略。

##### 3. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv6 单播地址族视图、BGP-VPN IPv6 单播地址族视图或 BGP IPv6 组播地址族视
图。
请依次执行以下命令进入 单播地址族视图。
BGP IPv6
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv6 [ unicast ]
请依次执行以下命令进入 BGP IPv6 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 multicast
(3) 配置向对等体 / 对等体组发布团体属性。
peer { group-name | ipv6-address [ prefix-length ] } advertise-community
缺省情况下，不向 IPv6 BGP 对等体/对等体组发布团体属性。
(4) 配置向对等体/对等体组发布扩展团体属性。

peer { group-name | ipv6-address [ prefix-length ] } advertise-ext-community缺省情况下，不向 对等体/对等体组发布扩展团体属性。
IPv6 BGP（可选）对发布给 对等体/对等体组的路由指定路由策略。
(5) IPv6 BGP peer { group-name | ipv6-address [ prefix-length ] } route-policy route-policy-name export缺省情况下，不指定对等体/对等体组的路由策略。

#### 3.4 配置BGP路由反射

##### 3.4.1 配置BGP路由反射器

###### 1. 功能简介

如果同一个 AS 内有多个 BGP 路由器，为了减少在同一 AS 内建立的 IBGP 连接数，可以把几个路由器划分为一个集群，将其中的一台路由器配置为路由反射器，其它路由器作为客户机，通BGP过路由反射器在客户机之间反射路由。
为了增加网络的可靠性和防止单点故障，可以在一个集群中配置一个以上的路由反射器，这时，网络管理员必须给位于相同集群中的每个路由反射器配置相同的集群 ID，以避免路由环路。

###### 2. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv4 单播地址族视图、BGP-VPN IPv4 单播地址族视图或 BGP IPv4 组播地址族视
图。
请依次执行以下命令进入 单播地址族视图。
BGP IPv4
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 multicast
(3) 配置本机作为路由反射器，对等体/对等体组作为路由反射器的客户机。
peer { group-name | ipv4-address [ mask-length ] } reflect-client
缺省情况下，未配置路由反射器及其客户机。
(4) （可选）允许路由反射器在客户机之间反射路由。
reflect between-clients
缺省情况下，允许路由反射器在客户机之间反射路由。

###### 3. 配置步骤（IPv4单播/IPv4组播）

(5) （可选）配置路由反射器的集群 ID。
reflector cluster-id { cluster-id | ipv4-address }
缺省情况下，每个路由反射器都使用自己的 Router ID 作为集群 ID。

###### 3. 配置步骤（IPv6单播/IPv6组播）

进入系统视图。
(1)
system-view
(2) 进入 BGP IPv6 单播地址族视图或 BGP IPv6 组播地址族视图。
请依次执行以下命令进入 BGP IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 [ unicast ]请依次执行以下命令进入 BGP IPv6 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 multicast
(3) 配置本机作为路由反射器，对等体/对等体组作为路由反射器的客户机。
peer { group-name | ipv6-address [ prefix-length ] } reflect-client缺省情况下，未配置路由反射器及其客户机。
(4) （可选）允许路由反射器在客户机之间反射路由。
reflect between-clients缺省情况下，允许路由反射器在客户机之间反射路由。
(5) （可选）配置路由反射器的集群 ID。
reflector cluster-id { cluster-id | ipv4-address }缺省情况下，每个路由反射器都使用自己的 作为集群 ID。
Router ID

##### 3.4.2 配置忽略BGP路由的ORIGINATOR_ID属性

###### 1. 功能简介

路由反射器从某个对等体接收到路由后，在反射该路由之前为其添加 ORIGINATOR_ID 属性，标识该路由在本 AS 内的起源。ORIGINATOR_ID 属性的值为该对等体的 Router ID。BGP 路由器接收到路由后，将路由中的 ORIGINATOR_ID 属性值与本地的 Router ID 进行比较，如果二者相同则丢弃该路由，从而避免路由环路。
在某些特殊的组网中（如防火墙组网），如果需要接收 属性值与本地ORIGINATOR_ID Router ID相同的路由，则需要通过本配置忽略 BGP 路由的 ORIGINATOR_ID 属性。

###### 2. 配置限制和指导

请谨慎使用本命令。如果无法确保执行本命令后网络中不会产生环路，请不要执行本命令。
执行本命令后，BGP 路由的 CLUSTER_LIST 属性也会被忽略。
配置步骤（ 单播 组播）
3. IPv4 /IPv4
(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。

进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(3) 配置忽略 BGP 路由的 ORIGINATOR_ID 属性。
peer { group-name | ipv4-address [ mask-length ] } ignore-originatorid缺省情况下，BGP 路由器不会忽略 BGP 路由的 ORIGINATOR_ID 属性。

###### 4. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
(3) 配置忽略 BGP 路由的 ORIGINATOR_ID 属性。
peer { group-name | ipv6-address [ prefix-length ] } ignore-originatorid
缺省情况下，BGP 路由器不会忽略 BGP 路由的 ORIGINATOR_ID 属性。

#### 3.5 配置BGP联盟

##### 3.5.1 功能简介

联盟是处理 AS 内部的 IBGP 网络连接激增的另一种方法，它将一个自治系统划分为若干个子自治系统，每个子自治系统内部的 IBGP 对等体建立全连接关系，子自治系统之间建立 EBGP 连接关系。

##### 3.5.2 BGP联盟基本配置

进入系统视图。
(1)
system-view
(2) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
(3) 配置联盟的 ID。
confederation id as-number缺省情况下，未配置联盟的 ID 。
在不属于联盟的 BGP 发言者看来，属于同一个联盟的多个子自治系统是一个整体，联盟 ID就是标识联盟这一整体的自治系统号。
(4) 配置联盟中的子自治系统。

confederation peer-as as-number-list缺省情况下，未配置联盟中的子自治系统。一个联盟最多可包括 32 个子自治系统，配置属于联盟的子自治系统时使用的 仅在联盟内部有效。
as-number如果路由器与联盟中的其它子自治系统建立 邻居关系，需要在该路由器上指定该联盟EBGP体中除了自己还包含哪些子自治系统。

##### 3.5.3 配置联盟兼容性

###### 1. 功能简介

如果其他路由器的联盟实现机制不同于 RFC 3065 标准，可以通过如下配置与未采用 RFC 3065 配置的 AS 联盟兼容。

###### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
(3) 配置设备可以与未遵循 RFC 3065 实现联盟的路由器互通。
confederation nonstandard缺省情况下，设备不能与未遵循 RFC 3065 实现联盟的路由器互通。

#### 3.6 大规模BGP网络显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 BGP 的运行情况，通过查看显示信息验证配置的效果。

##### 1. 大规模BGP网络配置显示（IPv4单播）

表3-1 大规模 BGP 网络配置显示（IPv4 单播）
操作 命令display bgp [ instance instance-name ] dampening显示BGP IPv4单播路由的路由衰减参数 parameter ipv4 [ unicast ] [ vpn-instance vpn-instance-name ] display bgp [ instance instance-name ] group ipv4显示BGP IPv4单播对等体组的信息 [ unicast ] [ vpn-instance vpn-instance-name ] [ group-name group-name ] display bgp [ instance instance-name ] peer ipv4 [ unicast ] [ vpn-instance vpn-instance-name ]显示BGP IPv4单播对等体或对等体组的状[ ipv4-address mask-length | { ipv4-address |态和统计信息group-name group-name } log-info | [ ipv4-address ] verbose ] display bgp [ instance instance-name ]显示衰减的 BGP IPv4 单播路由信息 routing-table dampened ipv4 [ unicast ] [ vpn-instance vpn-instance-name ] display bgp [ instance instance-name ] routing-table flap-info ipv4 [ unicast ]显示BGP IPv4单播路由的震荡统计信息[ vpn-instance vpn-instance-name ] [ ipv4-address [ { mask-length | mask } [ longest-match ] ] |

操作 命令as-path-acl as-path-acl-number ]

##### 2. 大规模BGP网络配置显示（IPv6单播）

表3-2 大规模 BGP 网络配置显示（IPv6 单播）
操作 命令display bgp [ instance instance-name ] dampening显示BGP IPv6单播路由的路由衰减参数 parameter ipv6 [ unicast ] [ vpn-instance vpn-instance-name ] display bgp [ instance instance-name ] group ipv6显示BGP IPv6单播对等体组的信息 [ unicast ] [ vpn-instance vpn-instance-name ] [ group-name group-name ] display bgp [ instance instance-name ] peer ipv6 [ unicast ] [ vpn-instance vpn-instance-name ] [ ipv6-address prefix-length | { ipv6-address | group-name group-name } log-info | [ ipv6-address ]显示 BGP IPv6 单播对等体或对等体组的状verbose ]态和统计信息display bgp [ instance instance-name ] peer ipv6 [ unicast ] [ ipv4-address mask-length | ipv4-address log-info | [ ipv4-address ] verbose ] display bgp [ instance instance-name ]显示衰减的BGP IPv6单播路由信息 routing-table dampened ipv6 [ unicast ] [ vpn-instance vpn-instance-name ] display bgp [ instance instance-name ] routing-table flap-info ipv6 [ unicast ]显示BGP IPv6单播路由的震荡统计信息[ vpn-instance vpn-instance-name ] [ ipv6-address prefix-length | as-path-acl as-path-acl-number ]

##### 3. 大规模BGP网络配置显示（IPv4组播）

表3-3 大规模 BGP 网络配置显示（IPv4 组播）
操作 命令display bgp [ instance instance-name ] group ipv4显示BGP IPv4组播对等体组的信息multicast [ group-name group-name ] display bgp [ instance instance-name ] peer ipv4显示BGP IPv4组播对等体或对等体组的状 multicast [ ipv4-address mask-length |态和统计信息 { ipv4-address | group-name group-name } log-info | [ ipv4-address ] verbose ] display bgp [ instance instance-name ]显示衰减的BGP IPv4组播路由信息routing-table dampened ipv4 multicast display bgp [ instance instance-name ] routing-table flap-info ipv4 multicast显示BGP IPv4组播路由的震荡统计信息 [ ipv4-address [ { mask-length | mask } [ longest-match ] ] | as-path-acl as-path-acl-number ] display bgp [ instance instance-name ] dampening显示BGP IPv4组播路由的路由衰减参数parameter ipv4 multicast

##### 4. 大规模BGP网络配置显示（IPv6组播）

表3-4 大规模 BGP 网络配置显示（IPv6 组播）
操作 命令display bgp [ instance instance-name ] group ipv6显示BGP IPv6组播对等体组的信息multicast [ group-name group-name ] display bgp instance peer ipv6 [ instance-name ]显示BGP IPv6组播对等体或对等体组的状 multicast [ ipv6-address prefix-length | { ipv6-address | group-name group-name } log-info |态和统计信息[ ipv6-address ] verbose ] display bgp [ instance instance-name ]显示衰减的BGP IPv6组播路由信息routing-table dampened ipv6 multicast display bgp [ instance instance-name ] routing-table flap-info ipv6 multicast显示BGP IPv6组播路由的震荡统计信息[ ipv6-address prefix-length | as-path-acl as-path-acl-number ] display bgp [ instance instance-name ] dampening显示 BGP IPv6 组播路由的路由衰减参数parameter ipv6 multicast

#### 3.7 配置大规模BGP网络典型配置举例

##### 3.7.1 BGP团体配置

###### 1. 组网需求

分别与 A、Switch 之间建立 连接。
Switch B Switch C EBGP通过在 上配置 团体属性，使得 发布到 中的路由，不会再被Switch A NO_EXPORT AS 10 AS 20 AS 20 发布到其他 AS。

###### 2. 组网图

图3-1 BGP 团体组网图

###### 3. 配置步骤

(1) 配置各接口的 IP 地址（略）
(2) 配置 EBGP

\# 配置 Switch A。
<SwitchA> system-view [SwitchA] bgp 10 [SwitchA-bgp-default] router-id 1.1.1.1 [SwitchA-bgp-default] peer 200.1.2.2 as-number 20 [SwitchA-bgp-default] address-family ipv4 unicast [SwitchA-bgp-default-ipv4] peer 200.1.2.2 enable [SwitchA-bgp-default-ipv4] network 9.1.1.0 255.255.255.0 [SwitchA-bgp-default] quit配置 B。
\# Switch <SwitchB> system-view [SwitchB] bgp 20 [SwitchB-bgp-default] router-id 2.2.2.2 [SwitchB-bgp-default] peer 200.1.2.1 as-number 10 [SwitchB-bgp-default] peer 200.1.3.2 as-number 30 [SwitchB-bgp-default] address-family ipv4 unicast [SwitchB-bgp-default-ipv4] peer 200.1.2.1 enable [SwitchB-bgp-default-ipv4] peer 200.1.3.2 enable [SwitchB-bgp-default-ipv4] quit [SwitchB-bgp-default] quit \# 配置 Switch C。
<SwitchC> system-view [SwitchC] bgp 30 [SwitchC-bgp-default] router-id 3.3.3.3 [SwitchC-bgp-default] peer 200.1.3.1 as-number 20 [SwitchC-bgp-default] address-family ipv4 unicast [SwitchC-bgp-default-ipv4] peer 200.1.3.1 enable [SwitchC-bgp-default-ipv4] quit [SwitchC-bgp-default] quit查看 的路由表。
\# Switch B [SwitchB] display bgp routing-table ipv4 9.1.1.0 BGP local router ID: 2.2.2.2 Local AS number: 20 Paths: 1 available, 1 best BGP routing table information of 9.1.1.0/24:
From : 200.1.2.1 (1.1.1.1)
Rely nexthop : 200.1.2.1 Original nexthop: 200.1.2.1 OutLabel : NULL RxPathID : 0x0 TxPathID : 0x0 AS-path : 10 Origin : igp Attribute value : pref-val 0

State : valid, external, best IP precedence : N/A QoS local ID : N/A Traffic index : N/A \# 查看 Switch B 的路由发送信息。
[SwitchB] display bgp routing-table ipv4 9.1.1.0 advertise-info BGP local router ID: 2.2.2.2 Local AS number: 20 Paths: 1 best BGP routing table information of 9.1.1.0/24(TxPathID:0):
Advertised to peers (1 in total):
200.1.3.2可以看出，Switch 能够把到达目的地址 的路由通过 发布出去。
B 9.1.1.0/24 BGP查看 的 路由表。
\# Switch C BGP [SwitchC] display bgp routing-table ipv4 Total number of routes: 1 BGP local router ID is 3.3.3.3 Status codes: * - valid, > - best, d - dampened, h - history, s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn
* >e 9.1.1.0/24 200.1.3.1 0 20 10i可以看出，Switch C 从 Switch B 那里学到了目的地址为 9.1.1.0/24 的路由。
(3) 配置 BGP 团体属性\# 配置路由策略。
[SwitchA] route-policy comm_policy permit node 0 [SwitchA-route-policy-comm_policy-0] apply community no-export [SwitchA-route-policy-comm_policy-0] quit \# 应用路由策略。
[SwitchA] bgp 10 [SwitchA-bgp-default] address-family ipv4 unicast [SwitchA-bgp-default-ipv4] peer 200.1.2.2 route-policy comm_policy export [SwitchA-bgp-default-ipv4] peer 200.1.2.2 advertise-community

###### 4. 验证配置

\# 查看 Switch B 的路由表。
[SwitchB] display bgp routing-table ipv4 9.1.1.0 BGP local router ID: 2.2.2.2

Local AS number: 20 Paths: 1 available, 1 best BGP routing table information of 9.1.1.0/24:
From : 200.1.2.1 (1.1.1.1)
Rely nexthop : 200.1.2.1 Original nexthop: 200.1.2.1 OutLabel : NULL RxPathID : 0x0 TxPathID : 0x0 Community : No-Export AS-path : 10 Origin : igp Attribute value : pref-val 0 State : valid, external, best IP precedence : N/A QoS local ID : N/A Traffic index : N/A \# 查看 Switch B 的路由发送信息。
[SwitchB] display bgp routing-table ipv4 9.1.1.0 advertise-info BGP local router ID: 2.2.2.2 Local AS number: 20 Paths: 1 best BGP routing table information of 9.1.1.0/24(TxPathID:0):
Not advertised to any peers yet \# 查看 Switch C 的 BGP 路由表。
[SwitchC] display bgp routing-table ipv4 Total number of routes: 0在 Switch B 的 BGP 路由表中可以看到配置的团体属性，Switch B 不会通过 BGP 将到达目的地址
9.1.1.0/24 的路由发布出去。

##### 3.7.2 BGP路由反射器配置

###### 1. 组网需求

所有交换机运行 BGP 协议，Switch A 与 Switch B 建立 EBGP 连接，Switch C 与 Switch B 和 Switch之间建立 连接。
D IBGP作为路由反射器，Switch 和 为 的客户机。
Switch C B Switch D Switch C能够通过 学到路由 。
Switch D Switch C 20.0.0.0/8

###### 2. 组网图

图3-2 配置 BGP 路由反射器的组网图

###### 3. 配置步骤

(1) 配置各接口的 IP 地址，并在 AS 200 内配置 OSPF（略）
(2) 配置 BGP 连接
\# 配置 Switch A。
<SwitchA> system-view
[SwitchA] bgp 100
[SwitchA-bgp-default] router-id 1.1.1.1
[SwitchA-bgp-default] peer 192.1.1.2 as-number 200
[SwitchA-bgp-default] address-family ipv4 unicast
[SwitchA-bgp-default-ipv4] peer 192.1.1.2 enable
\# 通告 20.0.0.0/8 网段路由到 BGP 路由表中。
[SwitchA-bgp-default-ipv4] network 20.0.0.0
[SwitchA-bgp-default-ipv4] quit
[SwitchA-bgp-default] quit
\# 配置 Switch B。
<SwitchB> system-view
[SwitchB] bgp 200
[SwitchB-bgp-default] router-id 2.2.2.2
[SwitchB-bgp-default] peer 192.1.1.1 as-number 100
[SwitchB-bgp-default] peer 193.1.1.1 as-number 200
[SwitchB-bgp-default] address-family ipv4 unicast
[SwitchB-bgp-default-ipv4] peer 192.1.1.1 enable
[SwitchB-bgp-default-ipv4] peer 193.1.1.1 enable
[SwitchB-bgp-default-ipv4] peer 193.1.1.1 next-hop-local
[SwitchB-bgp-default-ipv4] quit
[SwitchB-bgp-default] quit
配置 。
\# Switch C
<SwitchC> system-view
[SwitchC] bgp 200
[SwitchC-bgp-default] router-id 3.3.3.3
[SwitchC-bgp-default] peer 193.1.1.2 as-number 200

[SwitchC-bgp-default] peer 194.1.1.2 as-number 200 [SwitchC-bgp-default] address-family ipv4 unicast [SwitchC-bgp-default-ipv4] peer 193.1.1.2 enable [SwitchC-bgp-default-ipv4] peer 194.1.1.2 enable [SwitchC-bgp-default-ipv4] quit [SwitchC-bgp-default] quit \# 配置 Switch D。
<SwitchD> system-view [SwitchD] bgp 200 [SwitchD-bgp-default] router-id 4.4.4.4 [SwitchD-bgp-default] peer 194.1.1.1 as-number 200 [SwitchD-bgp-default] address-family ipv4 unicast [SwitchD-bgp-default-ipv4] peer 194.1.1.1 enable [SwitchD-bgp-default-ipv4] quit [SwitchD-bgp-default] quit配置路由反射器
(3)
配置 C。
\# Switch [SwitchC] bgp 200 [SwitchC-bgp-default] address-family ipv4 unicast [SwitchC-bgp-default-ipv4] peer 193.1.1.2 reflect-client [SwitchC-bgp-default-ipv4] peer 194.1.1.2 reflect-client [SwitchC-bgp-default-ipv4] quit [SwitchC-bgp-default] quit

###### 4. 验证配置

\# 查看 Switch B 的 BGP 路由表。
[SwitchB] display bgp routing-table ipv4 Total number of routes: 1 BGP local router ID is 2.2.2.2 Status codes: * - valid, > - best, d - dampened, h - history, s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn
* >e 20.0.0.0 192.1.1.1 0 0 100i查看 的 路由表。
\# Switch D BGP [SwitchD] display bgp routing-table ipv4 Total number of routes: 1 BGP local router ID is 4.4.4.4 Status codes: * - valid, > - best, d - dampened, h - history, s - suppressed, S - stale, i - internal, e - external a – additional-path

Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn
* >i 20.0.0.0 193.1.1.2 0 100 0 100i可以看出，Switch D 从 Switch C 已经学到了 20.0.0.0/8 路由。

##### 3.7.3 BGP联盟配置

###### 1. 组网需求

AS 200 中有多台 BGP 交换机，为了减少 IBGP 的连接数，现将他们划分为 3 个子自治系统：AS 65001、AS 65002 和 AS 65003。其中 AS 65001 内的三台交换机建立 IBGP 全连接。

###### 2. 组网图

图3-3 配置联盟组网图n t
- i n t na i an - V l V l

| 接口 | IP地址 | 设备 | 接口 |
|---|---|---|---|
| Vlan-int100 | 200.1.1.1/24 | Switch D | Vlan-int200 |
| Vlan-int200 | 10.1.1.1/24 |  | Vlan-int400 |
| Vlan-int300 | 10.1.2.1/24 | Switch E | Vlan-int200 |
| Vlan-int400 | 10.1.3.1/24 |  | Vlan-int500 |
| Vlan-int500 | 10.1.4.1/24 | Switch F | Vlan-int100 |
| Vlan-int200 | 10.1.1.2/24 |  | Vlan-int600 |
| Vlan-int300 | 10.1.2.2/24 |  |  |

设备 IP地址Switch A 10.1.5.1/24
10.1.3.2/24
10.1.5.2/24
10.1.4.2/24
200.1.1.2/24 Switch B 9.1.1.1/24 Switch C

###### 3. 配置步骤

(1) 配置各接口的 IP 地址（略）
(2) 配置 BGP 联盟
\# 配置 Switch A 。
<SwitchA> system-view
[SwitchA] bgp 65001
[SwitchA-bgp-default] router-id 1.1.1.1
[SwitchA-bgp-default] confederation id 200

[SwitchA-bgp-default] confederation peer-as 65002 65003 [SwitchA-bgp-default] peer 10.1.1.2 as-number 65002 [SwitchA-bgp-default] peer 10.1.2.2 as-number 65003 [SwitchA-bgp-default] address-family ipv4 unicast [SwitchA-bgp-default-ipv4] peer 10.1.1.2 enable [SwitchA-bgp-default-ipv4] peer 10.1.2.2 enable [SwitchA-bgp-default-ipv4] peer 10.1.1.2 next-hop-local [SwitchA-bgp-default-ipv4] peer 10.1.2.2 next-hop-local [SwitchA-bgp-default-ipv4] quit [SwitchA-bgp-default] quit \# 配置 Switch B。
<SwitchB> system-view [SwitchB] bgp 65002 [SwitchB-bgp-default] router-id 2.2.2.2 [SwitchB-bgp-default] confederation id 200 [SwitchB-bgp-default] confederation peer-as 65001 65003 [SwitchB-bgp-default] peer 10.1.1.1 as-number 65001 [SwitchB-bgp-default] address-family ipv4 unicast [SwitchB-bgp-default-ipv4] peer 10.1.1.1 enable [SwitchB-bgp-default-ipv4] quit [SwitchB-bgp-default] quit配置 C。
\# Switch <SwitchC> system-view [SwitchC] bgp 65003 [SwitchC-bgp-default] router-id 3.3.3.3 [SwitchC-bgp-default] confederation id 200 [SwitchC-bgp-default] confederation peer-as 65001 65002 [SwitchC-bgp-default] peer 10.1.2.1 as-number 65001 [SwitchC-bgp-default] address-family ipv4 unicast [SwitchC-bgp-default-ipv4] peer 10.1.2.1 enable [SwitchC-bgp-default-ipv4] quit [SwitchC-bgp-default] quit
(3) 配置 AS 65001 内的 IBGP 连接\# 配置 Switch A。
[SwitchA] bgp 65001 [SwitchA-bgp-default] peer 10.1.3.2 as-number 65001 [SwitchA-bgp-default] peer 10.1.4.2 as-number 65001 [SwitchA-bgp-default] address-family ipv4 unicast [SwitchA-bgp-default-ipv4] peer 10.1.3.2 enable [SwitchA-bgp-default-ipv4] peer 10.1.4.2 enable [SwitchA-bgp-default-ipv4] peer 10.1.3.2 next-hop-local [SwitchA-bgp-default-ipv4] peer 10.1.4.2 next-hop-local [SwitchA-bgp-default-ipv4] quit [SwitchA-bgp-default] quit \# 配置 Switch D。
<SwitchD> system-view [SwitchD] bgp 65001

[SwitchD-bgp-default] router-id 4.4.4.4 [SwitchD-bgp-default] confederation id 200 [SwitchD-bgp-default] peer 10.1.3.1 as-number 65001 [SwitchD-bgp-default] peer 10.1.5.2 as-number 65001 [SwitchD-bgp-default] address-family ipv4 unicast [SwitchD-bgp-default-ipv4] peer 10.1.3.1 enable [SwitchD-bgp-default-ipv4] peer 10.1.5.2 enable [SwitchD-bgp-default-ipv4] quit [SwitchD-bgp-default] quit \# 配置 Switch E。
<SwitchE> system-view [SwitchE] bgp 65001 [SwitchE-bgp-default] router-id 5.5.5.5 [SwitchE-bgp-default] confederation id 200 [SwitchE-bgp-default] peer 10.1.4.1 as-number 65001 [SwitchE-bgp-default] peer 10.1.5.1 as-number 65001 [SwitchE-bgp-default] address-family ipv4 unicast [SwitchE-bgp-default-ipv4] peer 10.1.4.1 enable [SwitchE-bgp-default-ipv4] peer 10.1.5.1 enable [SwitchE-bgp-default-ipv4] quit [SwitchE-bgp-default] quit配置 和 之间的 连接
(4) AS 100 AS 200 EBGP配置 A。
\# Switch [SwitchA] bgp 65001 [SwitchA-bgp-default] peer 200.1.1.2 as-number 100 [SwitchA-bgp-default] address-family ipv4 unicast [SwitchA-bgp-default-ipv4] peer 200.1.1.2 enable [SwitchA-bgp-default-ipv4] quit [SwitchA-bgp-default] quit配置 F。
\# Switch <SwitchF> system-view [SwitchF] bgp 100 [SwitchF-bgp-default] router-id 6.6.6.6 [SwitchF-bgp-default] peer 200.1.1.1 as-number 200 [SwitchF-bgp-default] address-family ipv4 unicast [SwitchF-bgp-default-ipv4] peer 200.1.1.1 enable [SwitchF-bgp-default-ipv4] network 9.1.1.0 255.255.255.0 [SwitchF-bgp-default-ipv4] quit [SwitchF-bgp-default] quit

###### 4. 验证配置

\# 查看 Switch B 的 BGP 路由表。Switch C 的 BGP 路由表与此类似。
[SwitchB] display bgp routing-table ipv4 Total number of routes: 1 BGP local router ID is 2.2.2.2 Status codes: * - valid, > - best, d - dampened, h - history,

s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn
* >i 9.1.1.0/24 10.1.1.1 0 100 0 (65001)
100i [SwitchB] display bgp routing-table ipv4 9.1.1.0 BGP local router ID: 2.2.2.2 Local AS number: 65002 Paths: 1 available, 1 best BGP routing table information of 9.1.1.0/24:
From : 10.1.1.1 (1.1.1.1)
Rely nexthop : 10.1.1.1 Original nexthop: 10.1.1.1 OutLabel : NULL RxPathID : 0x0 TxPathID : 0x0 AS-path : (65001) 100 Origin : igp Attribute value : MED 0, localpref 100, pref-val 0, pre 255 State : valid, external-confed, best IP precedence : N/A QoS local ID : N/A Traffic index : N/A \# 查看 Switch D 的 BGP 路由表。
[SwitchD] display bgp routing-table ipv4 Total number of routes: 1 BGP local router ID is 4.4.4.4 Status codes: * - valid, > - best, d - dampened, h - history, s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn
* >i 9.1.1.0/24 10.1.3.1 0 100 0 100i [SwitchD] display bgp routing-table ipv4 9.1.1.0 BGP local router ID: 4.4.4.4 Local AS number: 65001

Paths: 1 available, 1 best BGP routing table information of 9.1.1.0/24:
From : 10.1.3.1 (1.1.1.1)
Rely nexthop : 10.1.3.1 Original nexthop: 10.1.3.1 OutLabel : NULL RxPathID : 0x0 TxPathID : 0x0 AS-path : 100 Origin : igp Attribute value : MED 0, localpref 100, pref-val 0, pre 255 State : valid, internal-confed, best IP precedence : N/A QoS local ID : N/A Traffic index : N/A通过以上显示信息可以看出：
• Switch F 只需要和 Switch A 建立 EBGP 连接，而不需要和 Switch B、Switch C 建立连接，同样可以通过联盟将路由信息传递给 Switch B 和 Switch C。
• Switch B 和 Switch D 在同一个联盟里，但是属于不同的子自治系统，它们都是通过 Switch A来获取外部路由信息，生成的 路由表项也是一致的，等效于在同一个自治系统内，但是BGP又不需要物理上全连接。

### 4 控制BGP路径的选择

#### 4.1 控制BGP路径的选择配置任务简介

BGP 具有很多路由属性，通过配置这些属性可以控制 BGP 路径的选择。
控制 BGP 路径选择的配置任务如下：
(1) 配置BGP的路由优先级
(2) 配置NEXT_HOP属性
(3) 为接收路由分配首选值
(4) 配置本地优先级的缺省值
(5) 配置AS_PATH属性允许本地AS号出现的次数(cid:123)
配置BGP在选择最优路由时忽略AS_PATH属性(cid:123)
为对等体/对等体组指定一个虚拟的自治系统号(cid:123)
配置AS号替换功能(cid:123)
配置发送BGP更新消息时AS_PATH属性中不携带私有AS号(cid:123)
配置不检测EBGP路由的第一个AS号(cid:123)
(6) 配置MED属性配置MED缺省值(cid:123)
配置允许比较来自不同AS路由的MED属性值(cid:123)
配置对来自同一AS的路由进行MED排序优选(cid:123)
配置允许比较来自同一联盟不同子自治系统邻居路由的MED属性值(cid:123)
(7) 配置BGP在选择最优路由时忽略IGP Metric的比较
(8) 配置BGP在选择最优路由时忽略Router ID

#### 4.2 配置BGP的路由优先级

##### 1. 功能简介

路由器上可能同时运行多个动态路由协议，存在各个路由协议之间路由信息共享和选择的问题。系统为每一种路由协议设置一个优先级，在不同协议发现同一条路由时，优先级高的路由将被优先选择。
用户可以通过 preference 命令修改 EBGP 路由、IBGP 路由以及本地产生的 BGP 路由的优先级，或应用路由策略为通过匹配规则过滤的特定路由配置优先级，没有通过过滤的路由使用缺省优先级。
缺省情况下，EBGP 路由的优先级低于本地产生的 BGP 路由的优先级。设备上存在到达某一目的网络的 路由和本地产生的 路由时，不会选择 路由。通过执行EBGP BGP EBGP network short-cut 命令将一条 EBGP 路由配置成 short-cut，可以使得指定 EBGP 路由的优先级与本地产生的 BGP 路由的优先级相同，从而提高该 EBGP 路由成为最佳路由的可能性。

##### 2. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv4 单播地址族视图、BGP-VPN IPv4 单播地址族视图或 BGP IPv4 组播地址族视
图。
请依次执行以下命令进入 BGP IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 multicast
配置 路由的优先级。
(3) BGP
preference { external-preference internal-preference local-preference
| route-policy route-policy-name }
缺省情况下，EBGP 路由的优先级为 255，IBGP 路由的优先级为 255，本地产生的 BGP 路
由的优先级为 130。
(4) （可选）提高接收到的指定 EBGP 路由的路由优先级。
network ipv4-address [ mask-length | mask ] short-cut
缺省情况下，接收到的 EBGP 路由的路由优先级为 255。

##### 3. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv6 单播地址族视图、BGP-VPN IPv6 单播地址族视图或 BGP IPv6 组播地址族视
图。
请依次执行以下命令进入 BGP IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv6 [ unicast ]
请依次执行以下命令进入 BGP IPv6 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 multicast

##### 1. 功能简介

(3) 配置 BGP 路由的优先级。
preference { external-preference internal-preference local-preference
| route-policy route-policy-name }
缺省情况下，EBGP 路由的优先级为 255，IBGP 路由的优先级为 255，本地产生的 路
BGP
由的优先级为 130。
(4) （可选）提高接收到的指定 EBGP 路由的路由优先级。
network ipv6-address prefix-length short-cut
(5) 缺省情况下，接收到的 EBGP 路由的路由优先级为 255。

#### 4.3 配置NEXT_HOP属性

功能简介
1.
缺省情况下，路由器向 IBGP 对等体/对等体组发布路由时，不将自身地址作为下一跳，但有的时候为了保证 IBGP 邻居能够找到下一跳，可以配置将自身地址作为下一跳。以下图为例，Router A 与建立 邻居关系，Router 与 建立 邻居关系，Router 在向Router B EBGP B Router C IBGP B Router C 发布从 Router A 学到的 BGP 路由时，如果 Router C 上没有到达 1.1.1.1/24 的路由，可以在 Router B 上配置 peer next-hop-local 命令将 3.1.1.1/24 作为下一跳，这样，Router C 就能找到下一跳。
图4-1 配置 BGP NEXT_HOP 属性应用组网图一在一些比较特殊的组网环境中（即两个 BGP 连接在同一网段的广播网），路由器向 EBGP 对等体/对等体组发布路由时不会将自身地址作为下一跳，以下图为例：Router A 与 Router B 建立 EBGP邻居关系，Router B与 Router C建立 IBGP邻居关系，两个 BGP连接都位于同一个广播网 1.1.1.0/24中，Router 向 发布 路由时不会将自身地址 作为下一跳，但如果用户B Router A EBGP 1.1.1.2/24有需要，也可以通过配置 peer next-hop-local 命令实现将自身地址 1.1.1.2/24 作为下一跳。
图4-2 配置 属性应用组网图二BGP NEXT_HOP

##### 2. 配置限制和指导

如果配置了 BGP 负载分担，则不论是否配置了 peer next-hop-local 命令，本地路由器向 IBGP对等体/对等体组发布路由时都先将下一跳地址改变为自身地址。

##### 3. 配置步骤（IPv4单播/IPv4组播）

进入系统视图。
(1)
system-view
(2) 进入 BGP IPv4 单播地址族视图、BGP-VPN IPv4 单播地址族视图或 BGP IPv4 组播地址族视图。
请依次执行以下命令进入 单播地址族视图。
BGP IPv4 (cid:123)
bgp as-number [ instance instance-name ] address-family ipv4 [ unicast ]请依次执行以下命令进入 单播地址族视图。
BGP-VPN IPv4 (cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv4 [ unicast ]请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv4 multicast
(3) 配置向对等体/对等体组发布路由时，将下一跳属性修改为自身的地址。
peer { group-name | ipv4-address [ mask-length ] } next-hop-local缺省情况下，向 EBGP 对等体/对等体组发布路由时，将下一跳属性修改为自身的地址；向 IBGP对等体/对等体组发布路由时，不修改下一跳属性。

##### 4. 配置步骤（IPv6单播/IPv6组播）

进入系统视图。
(1)
system-view进入 单播地址族视图、BGP-VPN 单播地址族视图或 组播地址族视
(2) BGP IPv6 IPv6 BGP IPv6图。
请依次执行以下命令进入 BGP IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 [ unicast ]请依次执行以下命令进入 单播地址族视图。
BGP-VPN IPv6 (cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv6 [ unicast ]请依次执行以下命令进入 BGP IPv6 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 multicast
(3) 配置向对等体/对等体组发布路由时，将下一跳属性修改为自身的地址。

peer { group-name | ipv6-address [ prefix-length ] } next-hop-local
(4) 缺省情况下，向 EBGP 对等体/对等体组发布路由时，将下一跳属性修改为自身的地址；向 IBGP对等体/对等体组发布路由时，不修改下一跳属性。

#### 4.4 为接收路由分配首选值

##### 1. 功能简介

BGP 选择路由时首先丢弃下一跳不可达的路由，其次优选 Preferred-value 值最大的路由。通过本配置，可以修改路由的 Preferred-value，以便控制 BGP 路径的选择。
缺省情况下，从对等体/对等体组学到的路由的首选值为 0，网络管理员可以为从某个对等体/对等体组接收的路由配置首选值，从而提高从指定对等体/对等体组学到的路由的优先级。

##### 2. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
进入 单播地址族视图、BGP-VPN 单播地址族视图或 组播地址族视
(2) BGP IPv4 IPv4 BGP IPv4
图。
请依次执行以下命令进入 BGP IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv4 [ unicast ]
请依次执行以下命令进入 组播地址族视图。
BGP IPv4
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 multicast
(3) 为从对等体/对等体组接收的路由分配首选值。
peer { group-name | ipv4-address [ mask-length ] } preferred-value value
缺省情况下，从对等体 / 对等体组接收的路由的首选值为 0 。

##### 3. 配置步骤（IPv6单播/IPv6组播）

进入系统视图。
(1)
system-view
(2) 进入 BGP IPv6 单播地址族视图、BGP-VPN IPv6 单播地址族视图或 BGP IPv6 组播地址族视图。
请依次执行以下命令进入 单播地址族视图。
BGP IPv6 (cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 [ unicast ]请依次执行以下命令进入 单播地址族视图。
BGP-VPN IPv6 (cid:123)
bgp as-number [ instance instance-name ]

ip vpn-instance vpn-instance-name address-family ipv6 [ unicast ]请依次执行以下命令进入 BGP IPv6 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 multicast
(3) 为从 IPv6 BGP 对等体/对等体组接收的路由分配首选值。
peer { group-name | ipv6-address [ prefix-length ] } preferred-value value缺省情况下，从 IPv6 BGP 对等体/对等体组接收的路由的首选值为 0。

#### 4.5 配置本地优先级的缺省值

##### 1. 功能简介

本地优先级用来判断流量离开 AS 时的最佳路由。当 BGP 路由器通过不同的 IBGP 对等体得到目的地址相同但下一跳不同的多条路由时，将优先选择本地优先级较高的路由。
用户可以通过本配置改变 BGP 路由器向 IBGP 对等体发送的路由本地优先级的缺省值。

##### 2. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv4 单播地址族视图、BGP-VPN IPv4 单播地址族视图或 BGP IPv4 组播地址族视
图。
请依次执行以下命令进入 BGP IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 multicast
(3) 配置本地优先级的缺省值。
default local-preference value
缺省情况下，本地优先级的缺省值为 100。

##### 3. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv6 单播地址族视图、BGP-VPN IPv6 单播地址族视图或 BGP IPv6 组播地址族视
图。

请依次执行以下命令进入 BGP IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 [ unicast ]请依次执行以下命令进入 BGP-VPN IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv6 [ unicast ]请依次执行以下命令进入 BGP IPv6 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 multicast
(3) 配置本地优先级的缺省值。
default local-preference value缺省情况下，本地优先级的缺省值为 100。

#### 4.6 配置AS_PATH属性

##### 4.6.1 允许本地AS号出现的次数

###### 1. 功能简介

通常情况下，BGP 会检查对等体发来的路由的 AS_PATH 属性，如果其中已存在本地 AS 号，则会忽略此路由，以免形成路由环路。
BGP但是，在某些特殊的组网环境下，需要允许本地 号在接收路由的 属性中出现，否则AS AS_PATH无法正确发布路由。通过本配置，可以允许本地 AS 号在所接收的路由的 AS_PATH 属性中出现，并可同时配置允许出现的次数。

###### 2. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv4 单播地址族视图、BGP-VPN IPv4 单播地址族视图或 BGP IPv4 组播地址族视
图。
请依次执行以下命令进入 单播地址族视图。
BGP IPv4
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 multicast

###### 1. 功能简介

(3) 配置允许本地 AS 号在对等体/对等体组接收路由的 AS_PATH 属性中出现，并配置允许出现
的次数。
peer { group-name | ipv4-address [ mask-length ] } allow-as-loop
[ number ]
缺省情况下，不允许本地 AS 号在接收路由的 AS_PATH 属性中出现。

###### 3. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv6 单播地址族视图、BGP-VPN IPv6 单播地址族视图或 BGP IPv6 组播地址族视
图。
请依次执行以下命令进入 BGP IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv6 [ unicast ]
请依次执行以下命令进入 BGP IPv6 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 multicast
(3) 配置允许本地 AS 号在对等体/对等体组接收路由的 AS_PATH 属性中出现，并配置允许出现
的次数。
peer { group-name | ipv6-address [ prefix-length ] } allow-as-loop
[ number ]
缺省情况下，不允许本地 AS 号在接收路由的 AS_PATH 属性中出现。

##### 4.6.2 配置BGP在选择最优路由时忽略AS_PATH属性

功能简介
1.
路由器在选择最优路由时会优选 AS 路径最短的路由，通过如下配置 BGP 在选择最优路由时会忽略属性。
AS_PATH

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 实例视图。
BGP
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 实例视图。
BGP-VPN
(cid:123)
bgp as-number [ instance instance-name ]

ip vpn-instance vpn-instance-name
(3) 配置 BGP 在选择最优路由时忽略 AS_PATH 属性。
bestroute as-path-neglect缺省情况下，BGP 将 AS_PATH 属性作为选择最优路由的一个条件。

##### 4.6.3 为对等体/对等体组指定一个虚拟的自治系统号

###### 1. 功能简介

进行系统移植时，例如，Router A 原来位于 AS 2，现在将它移植到 AS 3 里，网络管理员需要在的所有 对等体上修改 所在的 号。通过在 上为 对等体Router A EBGP Router A AS Router A EBGP /对等体组配置一个虚拟的本地自治系统号 2，可以将本地真实的 AS 号 3 隐藏起来。在 EBGP 对等体看来 Router A 始终位于 AS 2，不需要改变 EBGP 对等体上的配置。

###### 2. 配置限制和指导

本功能只适用于 EBGP 对等体和对等体组。

###### 3. 配置步骤（IPv4单播/IPv4组播）

进入系统视图。
(1)
system-view进入 实例视图或 实例视图。
(2) BGP BGP-VPN进入 实例视图。
BGP (cid:123)
bgp as-number [ instance instance-name ]请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(3) 为对等体/对等体组指定一个虚拟的本地自治系统号。
peer { group-name | ipv4-address [ mask-length ] } fake-as as-number缺省情况下，对等体/对等体组未配置虚拟的本地自治系统号。

###### 4. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
(3) 为对等体/对等体组指定一个虚拟的本地自治系统号。
peer { group-name | ipv6-address [ prefix-length ] } fake-as as-number
缺省情况下，对等体/对等体组未配置虚拟的本地自治系统号。

###### 1. 功能简介

###### 1. 功能简介

##### 4.6.4 配置AS号替换功能

功能简介
1.
在某些特殊组网中，如果 PE 和 CE 之间运行 EBGP，由于 BGP 使用 AS 号检测路由环路，为保证路由信息的正确发送，需要为物理位置不同的站点分配不同的 号。
AS如果物理位置不同的 CE 复用相同的 AS 号，则需要在 PE 上配置 BGP 的 AS 号替换功能。当 PE向指定对等体（CE）发布路由时，如果路由的 AS_PATH 中存在 CE 所在的 AS 号，则 PE 将该 AS号替换成 PE 的 AS 号后，再发布该路由，以保证私网路由能够正确发布。

###### 2. 配置限制和指导

本配置仅用于特定的组网环境。通常情况下，建议不要使用本配置，否则可能会引起路由环路。

###### 3. 配置步骤（IPv4单播/IPv4组播）

进入系统视图。
(1)
system-view
(2) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
(3) 配置用本地 AS 号替换 AS_PATH 属性中指定对等体/对等体组的 AS 号。
peer { group-name | ipv4-address [ mask-length ] } substitute-as缺省情况下，不会用本地 AS 号替换 AS_PATH 属性中指定对等体/对等体组的 AS 号。

###### 4. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
(3) 配置用本地 AS 号替换 AS_PATH 属性中指定对等体/对等体组的 AS 号。
peer { group-name | ipv6-address [ prefix-length ] } substitute-as
缺省情况下，不会用本地 AS 号替换 AS_PATH 属性中指定对等体/对等体组的 AS 号。

##### 4.6.5 配置发送BGP更新消息时AS_PATH属性中不携带私有AS号

功能简介
1.
私有 AS 号是内部使用的 AS 号，范围为 64512～65535。私有 AS 号主要用于测试网络，一般情况下不需要在公共网络中传播。
通过本配置，可以指定如果向 EBGP 对等体/对等体组发送的 BGP 更新消息中 AS_PATH 属性只包括私有 AS 号，则删除私有 AS 号后，将 BGP 更新消息发送给对等体/对等体组。

###### 2. 配置限制和指导

本命令只适用于 EBGP 对等体和对等体组。

###### 3. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view

(2) 进入 BGP IPv4 单播地址族视图、BGP-VPN IPv4 单播地址族视图或 BGP IPv4 组播地址族视
图。
请依次执行以下命令进入 单播地址族视图。
BGP IPv4
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 [ unicast ]
请依次执行以下命令进入 单播地址族视图。
BGP-VPN IPv4
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 multicast
(3) 配置向指定 EBGP 对等体/对等体组发送 BGP 更新消息时只携带公有 AS 号，不携带私有 AS
号。
peer { group-name | ipv4-address [ mask-length ] } public-as-only
缺省情况下，向 EBGP 对等体/对等体组发送 BGP 更新消息时，既可以携带公有 AS 号，又可
以携带私有 号。
AS

###### 4. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv6 单播地址族视图、BGP-VPN IPv6 单播地址族视图或 BGP IPv6 组播地址族视
图。
请依次执行以下命令进入 BGP IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv6 [ unicast ]
请依次执行以下命令进入 组播地址族视图。
BGP IPv6
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 multicast
配置向指定 对等体/对等体组发送 更新消息时只携带公有 号，不携带私有
(3) EBGP BGP AS AS
号。
peer { group-name | ipv6-address [ prefix-length ] } public-as-only
缺省情况下，向 对等体/对等体组发送 更新消息时，既可以携带公有 号，又可
EBGP BGP AS
以携带私有 AS 号。
本命令只适用于 EBGP 对等体和对等体组。

###### 1. 功能简介

##### 4.6.6 配置不检测EBGP路由的第一个AS号

功能简介
1.
缺省情况下，从 EBGP 邻居学到路由后，会检测路由的第一个 AS 号。如果此 AS 号不是 EBGP 对等体的 号，且不是私有 号，则断开与该对等体的 会话。
AS AS BGP通过本配置，可以忽略对 EBGP 路由第一个 AS 号的检测。

###### 2. 配置步骤

进入系统视图。
(1)
system-view进入 实例视图。
(2) BGP bgp as-number [ instance instance-name ]配置不检测 路由的第一个 号。
(3) EBGP AS ignore-first-as缺省情况下，从 EBGP 邻居学到路由后，会检测路由的第一个 AS 号。

#### 4.7 配置MED属性

##### 4.7.1 功能简介

MED 用来判断流量进入 AS 时的最佳路由。当一个 BGP 路由器通过不同的 EBGP 对等体得到目的地址相同但下一跳不同的多条路由时，在其它条件相同的情况下，将优先选择 属性值较小者MED作为最佳路由。

##### 4.7.2 配置MED缺省值

###### 1. 配置MED缺省值（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv4 单播地址族视图、BGP-VPN IPv4 单播地址族视图或 BGP IPv4 组播地址族视
图。
请依次执行以下命令进入 BGP IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 multicast

###### 1. 功能简介

(3) 配置 MED 的缺省值。
default med med-value
缺省情况下，MED 的缺省值为 0。

###### 2. 配置MED缺省值（IPv6单播/IPv6组播）

进入系统视图。
(1)
system-view
(2) 进入 BGP IPv6 单播地址族视图、BGP-VPN IPv6 单播地址族视图或 BGP IPv6 组播地址族视图。
请依次执行以下命令进入 单播地址族视图。
BGP IPv6 (cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 [ unicast ]请依次执行以下命令进入 单播地址族视图。
BGP-VPN IPv6 (cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv6 [ unicast ]请依次执行以下命令进入 BGP IPv6 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 multicast
(3) 配置 MED 的缺省值。
default med med-value缺省情况下，MED 的缺省值为 0。

##### 4.7.3 配置允许比较来自不同AS路由的MED属性值

功能简介
1.
缺省情况下，BGP 只比较来自同一个 AS 的路由的 MED 属性值。通过配置本功能，可以强制 BGP比较来自不同 AS 的路由的 MED 属性值。

###### 2. 配置步骤

进入系统视图。
(1)
system-view进入 实例视图或 实例视图。
(2) BGP BGP-VPN进入 实例视图。
BGP (cid:123)
bgp as-number [ instance instance-name ]请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(3) 配置允许比较来自不同 AS 路由的 MED 属性值。
compare-different-as-med

缺省情况下，不允许比较来自不同 AS 路由的 MED 属性值，只比较来自同一个 AS 的路由的属性值。
MED

##### 4.7.4 配置对来自同一AS的路由进行MED排序优选

###### 1. 功能简介

缺省情况下，BGP 选择最优路由时是将新的路由和当前 BGP 路由表中的最优路由进行比较，只要新的路由比当前 BGP 路由表中的最优路由更优，新的路由将成为最优路由，路由学习的顺序有可能会影响最优路由的选择结果。
图4-3 MED 排序优选示意图（以 IPv4 为例）
如 图 4-3 所示，Device D和Device A、Device B、Device C之间建立非直连EBGP邻居，通过OSPF学习到邻居地址 1.1.1.1/32、2.2.2.2/32、3.3.3.3/32（设置不同的开销值）。在Device D上查看IP路由表信息：
Destination/Mask Proto Pre Cost NextHop Interface
1.1.1.1/32 O_INTRA 10 10 11.1.1.2 Interface D1
2.2.2.2/32 O_INTRA 10 20 12.1.1.2 Interface D2
3.3.3.3/32 O_INTRA 10 30 13.1.1.2 Interface D3当 分别从 和 学习到到达网段 的路由时，由于来自Device D Device A Device B 10.0.0.0 Device B的路由的下一跳 Metric 值（即下一跳在 IP 路由表中的 Cost 值）较小，因此，从 Device B 学来的路由被选为最优路由。在 Device D 上查看 BGP 路由表信息：
Network NextHop MED LocPrf PrefVal Path/Ogn
*>e 10.0.0.0 2.2.2.2 50 0 300 400e
* e 3.3.3.3 50 0 200 400e当 Device D 再从 Device C 学习到到达 10.0.0.0 网段的路由时，它只和当前路由表的最优路由进行比较。由于 Device C 和 Device B 位于不同的 AS，选择路由时不会比较 MED 值，而来自 Device C的路由的下一跳 Metric 值更小，相对更优，它将成为最优路由。在 Device D 上查看 BGP 路由表信息：

###### 2. 配置步骤

Network NextHop MED LocPrf PrefVal Path/Ogn
*>e 10.0.0.0 1.1.1.1 60 0 200 400e
* e 10.0.0.0 2.2.2.2 50 0 300 400e
* e 3.3.3.3 50 0 200 400e但是如果将这条路由与从 Device A 学习到的路由进行比较，那么由于两条路由来自同一个 AS，且从 Device C 学习到的路由 MED 值更大，则从 Device C 学习到的路由应该视为无效路由。
在 Device D 上配置 bestroute compare-med 命令后，Device D 学习到新的路由时，会首先按照路由来自的 分组，对来自同一 的路由根据 值的大小进行优选，选出 值最小的AS AS MED MED路由，然后再对优选出来的、来自不同 AS 的路由进行优选，从而避免路由优选结果的不确定性。
配置对来自同一 AS 的路由进行 MED 排序优选后，从 Device B 学习到的到达 10.0.0.0 网段的路由将成为最优路由。在 Device D 上查看 BGP 路由表信息：
Network NextHop MED LocPrf PrefVal Path/Ogn
*>e 10.0.0.0 2.2.2.2 50 0 300 400e
* e 3.3.3.3 50 0 200 400e
* e 1.1.1.1 60 0 200 400e

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
(3) 配置对来自同一 AS 的路由进行 MED 排序优选。
bestroute compare-med
缺省情况下，不会对来自同一 AS 的路由进行 MED 排序优选。

##### 4.7.5 配置允许比较来自同一联盟不同子自治系统邻居路由的MED属性值

###### 1. 功能简介

只有 AS_PATH 里不包含联盟体外的自治系统编号时，才会比较来自同一联盟不同子自治系统邻居路由的 MED 属性值。例如，联盟中包含的子自治系统为 65006、65007 和 65009。如果存在三条路由，它们的 值分别为 65009、65007 和 65009，MED 值分别为 2、AS-PATH 65006 65009 65008
3、1，由于第三条路由包含了联盟体外的自治系统编号，因此在选择最优路由时第一条路由将成为最优路由。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)

##### 1. 功能简介

##### 2. 配置步骤

bgp as-number [ instance instance-name ]请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(3) 配置允许比较来自同一联盟不同子自治系统邻居路由的 MED 属性值。
bestroute med-confederation缺省情况下，不比较来自同一联盟不同子自治系统邻居路由的 MED 属性值。

#### 4.8 配置BGP在选择最优路由时忽略IGP Metric的比较

##### 1. 功能简介

从多个邻居收到多条相同前缀但不同路径的路由时，BGP 需要选择到达该前缀的最佳路由来指导报文转发。缺省情况下，BGP 会比较这些路由下一跳的 IGP 路由的 Metric 值，并优选 IGP Metric 值最小的路由。
配置了本功能后，BGP 在选择最优路由时忽略 IGP Metric 的比较。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(3) 配置 BGP 在选择最优路由时忽略 IGP Metric 的比较。
bestroute igp-metric-ignore缺省情况下，BGP 将 IGP Metric 作为选择最优路由的一个条件。

#### 4.9 配置BGP在选择最优路由时忽略Router ID

功能简介
1.
路由器在选择最优路由时会优选 Router ID 最小的路由器发布的路由。执行本配置后，BGP 在选择最优路由时会忽略 Router ID 的比较。

##### 2. 配置步骤

进入系统视图。
(1)
system-view进入 实例视图或 实例视图。
(2) BGP BGP-VPN进入 实例视图。
BGP (cid:123)
bgp as-number [ instance instance-name ]

请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(3) 配置 BGP 在选择最优路由时忽略 Router ID。
bestroute router-id-ignore缺省情况下，BGP 在选择最优路由时会优选 Router ID 最小的路由器发布的路由。

#### 4.10 控制BGP路径的选择显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 BGP 的运行情况，通过查看显示信息验证配置的效果。

##### 1. 控制BGP路径的选择配置显示（IPv4单播）

表4-1 控制 BGP 路径的选择配置显示（IPv4 单播）
操作 命令display bgp [ instance instance-name ] paths显示BGP的路由属性信息[ as-regular-expression ]

##### 2. 控制BGP路径的选择配置显示（IPv6单播）

表4-2 控制 路径的选择配置显示（IPv6 单播）
BGP操作 命令display bgp [ instance instance-name ] paths显示BGP的路由属性信息[ as-regular-expression ]

##### 3. 控制BGP路径的选择配置显示（IPv4组播）

表4-3 控制 路径的选择配置显示（IPv4 组播）
BGP操作 命令display bgp [ instance instance-name ] paths显示BGP的路由属性信息[ as-regular-expression ]

##### 4. 控制BGP路径的选择配置显示（IPv6组播）

表4-4 控制 路径的选择配置显示（IPv6 组播）
BGP操作 命令display bgp [ instance instance-name ] paths显示BGP的路由属性信息[ as-regular-expression ]

###### 2. 组网图

#### 4.11 控制BGP路径的选择典型配置举例

##### 4.11.1 BGP路径选择配置

###### 1. 组网需求

所有路由器都运行 BGP 协议。Switch A 与 Switch B 和 Switch C 之间运行 EBGP；Switch D 与 Switch B 和 Switch C 之间运行 IBGP。
AS 200 中运行 OSPF 协议。
配置路由策略，使得 Switch D 优选从 Switch C 学到的 1.0.0.0/8 路由。
组网图
2.
图4-4 配置 BGP 路径选择的组网图

| 接口 | IP地址 | 设备 | 接口 |
|---|---|---|---|
| Vlan-int101 | 1.0.0.1/8 | Switch D | Vlan-int400 |
| Vlan-int100 | 192.1.1.1/24 |  | Vlan-int300 |
| Vlan-int200 | 193.1.1.1/24 | Switch C | Vlan-int400 |
| Vlan-int100 | 192.1.1.2/24 |  | Vlan-int200 |
| Vlan-int300 | 194.1.1.2/24 |  |  |

设备 IP地址Switch A 195.1.1.1/24
194.1.1.1/24
195.1.1.2/24 Switch B 193.1.1.2/24

###### 3. 配置步骤

(1) 配置各接口的 IP 地址（略）
(2) 配置 Switch B、Switch C 和 Switch D 之间运行 OSPF 协议
\# 配置 Switch B。
<SwitchB> system-view
[SwitchB] ospf
[SwitchB-ospf] area 0
[SwitchB-ospf-1-area-0.0.0.0] network 192.1.1.0 0.0.0.255
[SwitchB-ospf-1-area-0.0.0.0] network 194.1.1.0 0.0.0.255
[SwitchB-ospf-1-area-0.0.0.0] quit
[SwitchB-ospf-1] quit
配置 C。
\# Switch
<SwitchC> system-view
[SwitchC] ospf

[SwitchC-ospf] area 0 [SwitchC-ospf-1-area-0.0.0.0] network 193.1.1.0 0.0.0.255 [SwitchC-ospf-1-area-0.0.0.0] network 195.1.1.0 0.0.0.255 [SwitchC-ospf-1-area-0.0.0.0] quit [SwitchC-ospf-1] quit \# 配置 Switch D。
<SwitchD> system-view [SwitchD] ospf [SwitchD-ospf] area 0 [SwitchD-ospf-1-area-0.0.0.0] network 194.1.1.0 0.0.0.255 [SwitchD-ospf-1-area-0.0.0.0] network 195.1.1.0 0.0.0.255 [SwitchD-ospf-1-area-0.0.0.0] quit [SwitchD-ospf-1] quit
(3) 配置 BGP 连接\# 配置 Switch A。
<SwitchA> system-view [SwitchA] bgp 100 [SwitchA-bgp-default] peer 192.1.1.2 as-number 200 [SwitchA-bgp-default] peer 193.1.1.2 as-number 200 [SwitchA-bgp-default] address-family ipv4 unicast [SwitchA-bgp-default-ipv4] peer 192.1.1.2 enable [SwitchA-bgp-default-ipv4] peer 193.1.1.2 enable \# 将 1.0.0.0/8 网段通告到 Switch A 的 BGP 路由表中。
[SwitchA-bgp-default-ipv4] network 1.0.0.0 8 [SwitchA-bgp-default-ipv4] quit [SwitchA-bgp-default] quit \# 配置 Switch B。
[SwitchB] bgp 200 [SwitchB-bgp-default] peer 192.1.1.1 as-number 100 [SwitchB-bgp-default] peer 194.1.1.1 as-number 200 [SwitchB-bgp-default] address-family ipv4 unicast [SwitchB-bgp-default-ipv4] peer 192.1.1.1 enable [SwitchB-bgp-default-ipv4] peer 194.1.1.1 enable [SwitchB-bgp-default-ipv4] quit [SwitchB-bgp-default] quit \# 配置 Switch C。
[SwitchC] bgp 200 [SwitchC-bgp-default] peer 193.1.1.1 as-number 100 [SwitchC-bgp-default] peer 195.1.1.1 as-number 200 [SwitchC-bgp-default] address-family ipv4 unicast [SwitchC-bgp-default-ipv4] peer 193.1.1.1 enable [SwitchC-bgp-default-ipv4] peer 195.1.1.1 enable [SwitchC-bgp-default-ipv4] quit [SwitchC-bgp-default] quit \# 配置 Switch D。
[SwitchD] bgp 200 [SwitchD-bgp-default] peer 194.1.1.2 as-number 200

[SwitchD-bgp-default] peer 195.1.1.2 as-number 200 [SwitchD-bgp-default] address-family ipv4 unicast [SwitchD-bgp-default-ipv4] peer 194.1.1.2 enable [SwitchD-bgp-default-ipv4] peer 195.1.1.2 enable [SwitchD-bgp-default-ipv4] quit [SwitchD-bgp-default] quit
(4) 通过配置本地优先级，使得 Switch D 优选从 Switch C 学到的路由。
\# 在 Switch C 上定义编号为 2000 的 IPv4 基本 ACL，允许 1.0.0.0/8 路由通过。
[SwitchC] acl basic 2000 [SwitchC-acl-ipv4-basic-2000] rule permit source 1.0.0.0 0.255.255.255 [SwitchC-acl-ipv4-basic-2000] quit \# 在 Switch C 上定义名为 localpref 的 Route-policy，设置路由 1.0.0.0/8 的本地优先级为 200（缺省的本地优先级为 100）。
[SwitchC] route-policy localpref permit node 10 [SwitchC-route-policy-localpref-10] if-match ip address acl 2000 [SwitchC-route-policy-localpref-10] apply local-preference 200 [SwitchC-route-policy-localpref-10] quit \# 为从 BGP 对等体 193.1.1.1 的路由应用名为 localpref 的 Route-policy。
[SwitchC] bgp 200 [SwitchC-bgp-default] address-family ipv4 unicast [SwitchC-bgp-default-ipv4] peer 193.1.1.1 route-policy localpref import [SwitchC-bgp-default-ipv4] quit [SwitchC-bgp-default] quit查看 的 路由表。
\# Switch D BGP [SwitchD] display bgp routing-table ipv4 Total number of routes: 2 BGP local router ID is 195.1.1.1 Status codes: * - valid, > - best, d - dampened, h - history, s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn
* >i 1.0.0.0 193.1.1.1 200 0 100i
* i 192.1.1.1 100 0 100i可以看到，Switch D 从 Switch C 学到 1.0.0.0/8 的路由是最优的。

### 5 调整和优化BGP网络

#### 5.1 调整和优化BGP网络配置任务简介

调整和优化 BGP 网络配置任务如下：
• 调整和优化 EBGP 会话的建立与复位配置允许同非直连邻居建立EBGP会话(cid:123)
使能直连EBGP会话快速复位功能(cid:123)
• 开启BGP ORF能力
• 调整 BGP 会话的建立、中断与软复位使能 4 字节AS号抑制功能(cid:123)
禁止与对等体/对等体组建立会话(cid:123)
配置BGP软复位(cid:123)
配置BGP负载分担
•配置BGP
• Add-Path配置系统进入二级内存门限告警状态后不断开EBGP对等体
•配置BGP发送协议报文的DSCP优先级
•配置从对等体/对等体组学到的路由不受迭代策略控制
•开启BGP次优路由下刷RIB功能
•

#### 5.2 配置允许同非直连邻居建立EBGP会话

##### 1. 功能简介

当前路由器要与另外一个路由器建立 EBGP 会话，它们之间必须具有直连的物理链路，且必须使用直连接口建立会话。如果不满足这一要求，则必须使用 peer ebgp-max-hop 命令允许它们经过多跳建立 EBGP 会话。

##### 2. 配置限制和指导

配置 功能后，只要本地设备和指定的对等体通过了 检查，就允许在二者之间建BGP GTSM GTSM立 EBGP 会话，不管二者之间的跳数是否超过 peer ebgp-max-hop 命令指定的跳数范围。

##### 3. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name

(3) 配置允许本地路由器同非直连网络上的邻居建立 EBGP 会话，同时指定允许的最大跳数。
peer { group-name | ipv4-address [ mask-length ] } ebgp-max-hop
[ hop-count ]
缺省情况下，不允许同非直连网络上的邻居建立 会话。
EBGP

##### 4. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 实例视图。
BGP
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 实例视图。
BGP-VPN
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
(3) 配置允许本地路由器同非直连网络上的邻居建立 EBGP 会话，同时指定允许的最大跳数。
peer { group-name | ipv6-address [ prefix-length ] } ebgp-max-hop
[ hop-count ]
缺省情况下，不允许同非直连网络上的邻居建立 会话。
EBGP

#### 5.3 使能直连EBGP会话快速复位功能

##### 1. 功能简介

缺省情况下，连接直连 EBGP 对等体的链路 down 后，本地路由器不会立即断开与 EBGP 对等体的会话，而是等待会话保持时间（Holdtime）超时后，才断开该会话。没有使能本功能时，链路震荡不会影响 会话的状态。
EBGP如果使能了本功能，则连接直连 对等体的链路 后，本地路由器会立即断开与 对EBGP down EBGP等体的会话，并重新与该对等体建立 EBGP 会话，从而实现快速发现链路故障，快速重建会话。

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
(3) 使能直连 EBGP 会话快速复位功能。
ebgp-interface-sensitive
缺省情况下，直连 EBGP 会话快速复位功能处于使能状态。

#### 5.4 开启BGP ORF能力

##### 5.4.1 功能简介

BGP ORF（Outbound Route Filtering，输出路由过滤）功能是指将 ORF 信息（本地的路由接收策略信息）通过 Route-refresh 消息发送给对等体，当对等体需要向本地发送 Update 更新消息时，不仅要利用对等体上的路由策略对路由进行过滤，还需要利用接收到的路由接收策略对路由进行过滤，只有通过策略过滤的路由信息才会发给本地，以达到减少 BGP 邻居间 Update 更新消息的交互，节省网络资源的目的。

##### 5.4.2 配置限制和指导

使能 能力后，本地和 对等体会通过 消息协商 能力（即收发的消息里是BGP ORF BGP Open ORF否允许携带 ORF 信息，如果允许携带，是否可以携带非标准的 ORF 信息），当协商完毕并成功建立 BGP 会话后，可以通过特殊的 Route-refresh 消息交互 ORF 信息。
本地和 BGP 对等体都需要执行本配置，且需要保证一端能够发送携带 ORF 信息的 Route-refresh报文，另一端能够接收携带 信息的 报文，才能保证 能力协商成功。
ORF Route-refresh ORF

##### 5.4.3 开启BGP邻居协商的ORF能力

###### 1. 配置步骤（IPv4单播/IPv4组播）

进入系统视图。
(1)
system-view进入 单播地址族视图、BGP-VPN 单播地址族视图或 组播地址族视
(2) BGP IPv4 IPv4 BGP IPv4图。
请依次执行以下命令进入 BGP IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv4 [ unicast ]请依次执行以下命令进入 单播地址族视图。
BGP-VPN IPv4 (cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv4 [ unicast ]请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv4 multicast
(3) 开启 BGP 邻居协商的 ORF 能力。
peer { group-name | ipv4-address [ mask-length ] } capability-advertise orf prefix-list { both | receive | send }缺省情况下，BGP 邻居协商的 ORF 能力处于关闭状态。

###### 2. 配置步骤（IPv6单播/IPv6组播）

进入系统视图。
(1)

system-view
(2) 进入 BGP IPv6 单播地址族视图、BGP-VPN IPv6 单播地址族视图或 BGP IPv6 组播地址族视图。
请依次执行以下命令进入 单播地址族视图。
BGP IPv6 (cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 [ unicast ]请依次执行以下命令进入 BGP-VPN IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv6 [ unicast ]请依次执行以下命令进入 BGP IPv6 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 multicast
(3) 开启 BGP 邻居协商的 ORF 能力。
peer { group-name | ipv6-address [ prefix-length ] } capability-advertise orf prefix-list { both | receive | send }缺省情况下，BGP 邻居协商的 ORF 能力处于关闭状态。

##### 5.4.4 开启BGP邻居协商的非标准ORF能力

###### 1. 功能简介

和采用非标准 ORF 的友商设备互通时需要执行本配置。

###### 2. 配置步骤

进入系统视图。
(1)
system-view进入 实例视图或 实例视图。
(2) BGP BGP-VPN进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(3) 开启 BGP 邻居协商的非标准 ORF 能力。
peer { group-name | ip-address [ mask-length ] | ipv6-address [ prefix-length ] } capability-advertise orf non-standard缺省情况下，BGP 邻居协商的非标准 ORF 能力处于关闭状态。

#### 5.5 使能4字节AS号抑制功能

##### 1. 功能简介

设备支持 字节的 号，即 号取值占用 字节，取值范围为 1～4294967295。缺省情况下，4 AS AS 4设备在与对端设备建立 BGP 会话时，通过 Open 消息通告对端设备本端支持 4 字节的 AS 号。如果对端设备不支持 4 字节 AS 号（只支持 2 字节 AS 号），则会导致会话协商失败。此时，在本端与对端设备之间使能 4 字节 AS 号抑制功能，可以使得本端设备通过 Open 消息向对端设备谎称自己不支持 字节的 号，从而确保本端和对端设备之间可以成功建立 会话。
4 AS BGP

##### 2. 配置限制和指导

如果对端设备支持 4 字节 AS 号，请不要使能 4 字节 AS 号抑制功能，否则会导致 BGP 会话无法建立。

##### 3. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
(3) 使能 4 字节 AS 号抑制功能。
peer { group-name | ipv4-address [ mask-length ] } capability-advertise
suppress-4-byte-as
缺省情况下， 4 字节 AS 号抑制功能处于关闭状态。

##### 4. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
(3) 使能 4 字节 AS 号抑制功能。
peer { group-name | ipv6-address [ prefix-length ] }
capability-advertise suppress-4-byte-as
缺省情况下，4 字节 AS 号抑制功能处于关闭状态。

#### 5.6 禁止与对等体/对等体组建立会话

##### 5.6.1 功能简介

由于网络升级维护等原因，需要暂时断开与对等体/对等体组的 BGP 会话时，可以通过本配置禁止与对等体/对等体组建立会话。当网络恢复后，取消本配置以恢复与对等体/对等体组的会话。这样，网络管理员无需删除并重新进行对等体/对等体组相关配置，减少了网络维护的工作量。
设备可以通过以下两种方式禁止与对等体/对等体组建立会话：
仅禁止与指定对等体/对等体组建立会话。
•禁止与所有对等体建立会话。
•执行本配置时，如果可以指定了 graceful 参数，则设备会启动等待邻居关系断开定时器，并重新发布路由信息。不同方式下，发布的路由信息有所不同：
仅禁止与指定对等体/对等体组建立会话：
•向指定的对等体/对等体组发送本设备上全部的路由。
(cid:123)
向其他的 对等体/对等体组发送来自指定对等体/对等体组的路由。
IBGP (cid:123)
禁止与所有对等体建立会话：向所有对等体/对等体组重新发送本设备上全部的路由。
•执行本配置还可以配置这些路由的属性，以降低重新发布路由的优先级，使得邻居路由器优选从其他邻居学到的路由，从而避免当定时器超时、邻居关系断开时造成流量的中断。

##### 5.6.2 配置限制和指导

如果本设备和对等体/对等体组的会话已经建立，则执行 ignore all-peers 或 peer ignore命令后，会断开 会话，并且清除所有相关路由信息。
BGP如果同时配置 ignore all-peers 和 peer ignore 命令，则针对同一对等体/对等体组，以 peer ignore 命令的配置为准。

##### 5.6.3 禁止与指定对等体/对等体组建立会话（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
(3) 禁止与对等体/对等体组建立会话。
peer { group-name | ipv4-address [ mask-length ] } ignore [ graceful
graceful-time { community { community-number | aa:nn } | local-preference
preference | med med } * ]
缺省情况下，允许与 BGP 对等体/对等体组建立会话。

##### 5.6.4 禁止与指定对等体/对等体组建立会话（IPv6单播/IPv6组播）

进入系统视图。
(1)
system-view进入 实例视图或 实例视图。
(2) BGP BGP-VPN进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(3) 禁止与 IPv6 BGP 对等体/对等体组建立会话。
peer { group-name | ipv6-address [ prefix-length ] } ignore [ graceful graceful-time { community { community-number | aa:nn } | local-preference preference | med med } * ]缺省情况下，允许与 对等体/对等体组建立会话。
BGP

##### 5.6.5 禁止与所有对等体/对等体组建立会话

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
(3) 禁止与所有对等体/对等体组建立会话。
ignore all-peers [ graceful graceful-time { community
{ community-number | aa:nn } | local-preference preference | med med }
* ]
缺省情况下，允许与 BGP 对等体/对等体组建立会话。

#### 5.7 配置BGP软复位

##### 5.7.1 功能简介

BGP 的选路策略改变，即影响 BGP 路由选择的配置（如路由首选值等）发生变化后，为了使新的策略生效，必须复位 会话，即删除并重新建立 会话，以便重新发布路由信息，并应用新BGP BGP的策略对路由信息进行过滤。复位 BGP 会话时，会造成短暂的 BGP 会话中断。
通过 BGP 软复位，可以实现在不中断 BGP 会话的情况下，对 BGP 路由表进行更新，并应用新的选路策略。
BGP 软复位的方法有以下三种：
• 通过 Route-refresh 功能实现 BGP 软复位：如果 BGP 的选路策略发生了变化，则本地路由器会向 BGP 对等体发送 Route-refresh 消息，收到此消息的对等体将其路由信息重新发给本地路由器，本地路由器根据新的路由策略对接收到的路由信息进行过滤。采用这种方式时，要求当前路由器和对等体都支持 Route-refresh 功能。

通过将所有路由更新信息保存在本地的方式实现 BGP 软复位：将从对等体接收的所有原始路
•由更新信息保存在本地，当选路策略发生改变后，对保存在本地的所有路由使用新的路由策略重新进行过滤。采用这种方式时，不要求当前路由器和对等体都支持 Route-refresh 功能，但是保存路由更新需要占用较多的内存资源。
• 手工软复位 BGP 会话：执行 refresh bgp 命令手工触发本地路由器将本地路由信息发送给对等体或向 对等体发送 消息，收到 消息的对等体将BGP BGP Route-refresh Route-refresh其路由信息重新发给本地路由器，以便本地路由器根据新的路由策略对接收到的路由信息进行过滤。采用这种方式时，要求当前路由器和对等体都支持 Route-refresh 功能。

##### 5.7.2 通过Route-refresh功能实现BGP软复位（IPv4单播/IPv4组播）

进入系统视图。
(1)
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(3) 通过 Route-refresh 功能实现 BGP 软复位。请选择其中一项进行配置。
使能本地路由器与指定对等体/对等体组的 BGP 路由刷新功能。
(cid:123)
peer { group-name | ipv4-address [ mask-length ] } capability-advertise route-refresh使能本地路由器与指定 BGP 对等体/对等体组的 BGP 路由刷新、多协议扩展和 4 字节 AS (cid:123)
号功能。
undo peer { group-name | ipv4-address [ mask-length ] } capability-advertise conventional缺省情况下，BGP 路由刷新、多协议扩展和 4 字节 AS 号功能处于使能状态。

##### 5.7.3 通过Route-refresh功能实现BGP软复位（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
(3) 通过 Route-refresh 功能实现 BGP 软复位。请选择其中一项进行配置。
使能本地路由器与指定 IPv6 BGP 对等体/对等体组的 BGP 路由刷新功能。
(cid:123)

peer { group-name | ipv6-address [ prefix-length ] } capability-advertise route-refresh使能本地路由器与指定 对等体/对等体组的 路由刷新、多协议扩展和 字IPv6 BGP BGP 4 (cid:123)
节 AS 号功能。
undo peer { group-name | ipv6-address [ prefix-length ] } capability-advertise conventional缺省情况下，BGP 路由刷新、多协议扩展和 4 字节 AS 号功能处于使能状态。

##### 5.7.4 通过将所有路由更新信息保存在本地实现BGP软复位（IPv4单播/IPv4组播）

进入系统视图。
(1)
system-view进入 单播地址族视图、BGP-VPN 单播地址族视图或 组播地址族视
(2) BGP IPv4 IPv4 BGP IPv4图。
请依次执行以下命令进入 BGP IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv4 [ unicast ]请依次执行以下命令进入 单播地址族视图。
BGP-VPN IPv4 (cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv4 [ unicast ]请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv4 multicast
(3) 保存所有来自指定对等体/对等体组的原始路由更新信息。
peer { group-name | ipv4-address [ mask-length ] } keep-all-routes缺省情况下，不保存来自对等体/对等体组的原始路由更新信息。
本命令只对执行该命令后接收到的路由生效。

##### 5.7.5 通过将所有路由更新信息保存在本地实现BGP软复位（IPv6单播/IPv6组播）

进入系统视图。
(1)
system-view
(2) 进入 BGP IPv6 单播地址族视图、BGP-VPN IPv6 单播地址族视图或 BGP IPv6 组播地址族视图。
请依次执行以下命令进入 单播地址族视图。
BGP IPv6 (cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 [ unicast ]请依次执行以下命令进入 单播地址族视图。
BGP-VPN IPv6 (cid:123)
bgp as-number [ instance instance-name ]

ip vpn-instance vpn-instance-name address-family ipv6 [ unicast ]请依次执行以下命令进入 BGP IPv6 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 multicast
(3) 保存所有来自指定 IPv6 BGP 对等体/对等体组的原始路由更新信息。
peer { group-name | ipv6-address [ prefix-length ] } keep-all-routes缺省情况下，不保存来自对等体/对等体组的原始路由更新信息。
本命令只对执行该命令后接收到的路由生效。

##### 5.7.6 手工软复位BGP会话（IPv4单播/IPv4组播）

进入系统视图。
(1)
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(3) 配置 Route-refresh 功能。请选择其中一项进行配置。
使能本地路由器与指定对等体/对等体组的 BGP 路由刷新功能。
(cid:123)
peer { group-name | ipv4-address [ mask-length ] } capability-advertise route-refresh使能本地路由器与指定 BGP 对等体/对等体组的 BGP 路由刷新、多协议扩展和 4 字节 AS (cid:123)
号功能。
undo peer { group-name | ipv4-address [ mask-length ] } capability-advertise conventional缺省情况下， 路由刷新、多协议扩展和 字节 号功能处于使能状态。
BGP 4 AS手工对 会话进行软复位。
(4) BGP退回系统视图。
a.
quit退回用户视图。
b.
quit
c. 手工对 BGP 会话进行软复位。
refresh bgp [ instance instance-name ] { ipv4-address [ mask-length ] | all | external | group group-name | internal } { export | import } ipv4 [ multicast | [ unicast ] [ vpn-instance vpn-instance-name ] ]

##### 1. 功能简介

##### 5.7.7 手工软复位BGP会话（IPv6单播/IPv6组播）

进入系统视图。
(1)
system-view进入 实例视图或 实例视图。
(2) BGP BGP-VPN进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(3) 配置 Route-refresh 功能。请选择其中一项进行配置。
使能本地路由器与 IPv6 BGP 指定对等体/对等体组的 BGP 路由刷新功能。
(cid:123)
peer { group-name | ipv6-address [ prefix-length ] } capability-advertise route-refresh使能本地路由器与指定 IPv6 BGP 对等体/对等体组的 BGP 路由刷新、多协议扩展和 4 字(cid:123)
节 号功能。
AS undo peer { group-name | ipv6-address [ prefix-length ] } capability-advertise conventional缺省情况下，BGP 路由刷新、多协议扩展和 4 字节 AS 号功能处于使能状态。
(4) 退回用户视图。
return手工对 会话进行软复位。
(5) BGP退回系统视图。
a.
quit退回用户视图。
b.
quit
c. 手工对 BGP 会话进行软复位。
refresh bgp [ instance instance-name ] { ipv6-address [ prefix-length ] | all | external | group group-name | internal } { export | import } ipv6 [ multicast | [ unicast ] [ vpn-instance vpn-instance-name ] ]

#### 5.8 配置BGP负载分担

功能简介
1.
通过改变 BGP 选路规则实现负载分担时，设备根据 balance 命令配置的进行 BGP 负载分担的路由条数，选择指定数目的路由进行负载分担，以提高链路利用率。

##### 2. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view

(2) 进入 BGP IPv4 单播地址族视图、BGP-VPN IPv4 单播地址族视图或 BGP IPv4 组播地址族视
图。
请依次执行以下命令进入 单播地址族视图。
BGP IPv4
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 [ unicast ]
请依次执行以下命令进入 单播地址族视图。
BGP-VPN IPv4
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv4 [ unicast ]
请依次执行以下命令进入 BGP IPv4 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 multicast
(3) 配置进行 BGP 负载分担的路由条数。
balance [ ebgp | eibgp | ibgp ] number
缺省情况下，不会进行 BGP 负载分担。
(4) （可选）配置不同 AS_PATH 属性的路由能够形成 BGP 负载分担。
balance as-path-neglect
缺省情况下，不同 AS_PATH 属性的路由之间不能形成 BGP 负载分担。
(5) （可选）配置内容不同但长度相同的 AS_PATH 属性的路由能够形成 BGP 负载分担。
balance as-path-relax
缺省情况下，内容不同但长度相同的 AS_PATH 属性的路由不能形成 BGP 负载分担。

##### 3. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv6 单播地址族视图、BGP-VPN IPv6 单播地址族视图或 BGP IPv6 组播地址族视
图。
请依次执行以下命令进入 BGP IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv6 [ unicast ]
请依次执行以下命令进入 BGP IPv6 组播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 multicast
配置进行 负载分担的路由条数。
(3) BGP
balance [ ebgp | eibgp | ibgp ] number

缺省情况下，不会进行 BGP 负载分担。
(4) （可选）配置不同 AS_PATH 属性的路由能够形成 BGP 负载分担。
balance as-path-neglect缺省情况下，不同 AS_PATH 属性的路由之间不能形成 BGP 负载分担。
(5) （可选）配置内容不同但长度相同的 AS_PATH 属性的路由能够形成 BGP 负载分担。
balance as-path-relax缺省情况下，内容不同但长度相同的 AS_PATH 属性的路由不能形成 BGP 负载分担。

#### 5.9 配置BGP Add-Path

##### 1. 功能简介

缺省情况下，BGP 只发布一条最优路由。如果最优路由所在路径出现网络故障，数据流量将会被中断，直到 BGP 根据新的网络拓扑路由收敛后，被中断的流量才能恢复正常的传输。
配置了 Add-Path（Additional Paths）功能后，BGP 可以向邻居发送本地前缀相同下一跳不同的多条路由。网络出现故障后，次优路由可以成为新的最优路由，这样就缩短了流量中断时间。
Add-Path 能力包括接收和发送两种。为了让对等体间的 Add-Path 能力协商成功，必须一端使能接收能力，另一端使能发送能力。

##### 2. 配置步骤（IPv4单播）

进入系统视图。
(1)
system-view
(2) 进入 BGP IPv4 单播地址族视图或 BGP-VPN IPv4 单播地址族视图。
请依次执行以下命令进入 BGP IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv4 [ unicast ]请依次执行以下命令进入 BGP-VPN IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv4 [ unicast ]
(3) 配置 Add-Path 功能。
peer { group-name | ipv4-address [ mask-length ] } additional-paths { receive | send } *缺省情况下，未配置 Add-Path 功能。
(4) 配置向指定对等体/对等体组发送的 Add-Path 优选路由的最大条数。
peer { group-name | ipv4-address [ mask-length ] } advertise additional-paths best number缺省情况下，向指定对等体 / 对等体组发送的 Add-Path 优选路由的最大条数为 1 。
(5) 配置 Add-Path 优选路由的最大条数。
additional-paths select-best best-number缺省情况下，Add-Path 优选路由的最大条数为 1。

##### 3. 配置步骤（IPv6单播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv6 单播地址族视图或 BGP-VPN IPv6 单播地址族视图。
请依次执行以下命令进入 BGP IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv6 [ unicast ]
请依次执行以下命令进入 BGP-VPN IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv6 [ unicast ]
配置 功能。
(3) Add-Path
peer { group-name | ipv6-address [ prefix-length ] } additional-paths
{ receive | send } *
缺省情况下，未配置 Add-Path 功能。
配置向指定对等体/对等体组发送的 优选路由的最大条数。
(4) Add-Path
peer { group-name | ipv6-address [ prefix-length ] } advertise
additional-paths best number
缺省情况下，向指定对等体/对等体组发送的 Add-Path 优选路由的最大条数为 1。
(5) 配置 Add-Path 优选路由的最大条数。
additional-paths select-best best-number
缺省情况下，Add-Path 优选路由的最大条数为 1。

#### 5.10 配置系统进入二级内存门限告警状态后不断开EBGP对等体

##### 1. 功能简介

当系统进入二级内存门限告警状态后，BGP 会周期性地选择一个 EBGP 对等体，断开与该对等体之间的 BGP 会话，直到系统内存恢复为止。用户可以通过本配置来避免在二级内存门限告警状态下，断开与指定 对等体 对等体组之间的 会话，以达到对特定 对等体 对等体组EBGP / BGP EBGP /进行保护的目的。
内存告警门限的详细介绍，请参见“基础配置指导”中的“设备管理”。

##### 2. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]

ip vpn-instance vpn-instance-name
(3) 配置系统进入二级内存门限告警状态后，不断开与指定 EBGP 对等体/对等体组之间的会话。
peer { group-name | ipv4-address [ mask-length ] } low-memory-exempt缺省情况下，系统在二级内存门限告警状态下，会周期性地选择一个 EBGP 对等体，并断开与该对等体之间的 会话。
BGP

##### 3. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
进入 实例视图或 实例视图。
(2) BGP BGP-VPN
进入 实例视图。
BGP
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 实例视图。
BGP-VPN
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
(3) 配置系统进入二级内存门限告警状态后，不断开与指定 EBGP 对等体/对等体组之间的会话。
peer { group-name | ipv6-address [ prefix-length ] } low-memory-exempt
缺省情况下，系统在二级内存门限告警状态下，会周期性地选择一个 EBGP 对等体，并断开
与该对等体之间的 会话。
BGP

#### 5.11 配置BGP发送协议报文的DSCP优先级

##### 1. 功能简介

DSCP（Differentiated Services Code Point，差分服务编码点）携带在 IP 报文中的 ToS 字段，用来体现报文自身的优先等级，决定报文传输的优先程度。通过配置本功能，可以对 BGP 发送协议报文的 优先级进行设置。
DSCP

##### 2. 配置步骤

(1) 进入系统视图。
system-view
进入 实例视图或 实例视图。
(2) BGP BGP-VPN
进入 实例视图。
BGP
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 实例视图。
BGP-VPN
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
(3) 配置 BGP 发送协议报文的 DSCP 优先级。
peer { group-name | ipv4-address [ mask-length ] | ipv6-address
[ prefix-length ] } dscp dscp-value
缺省情况下，BGP 发送协议报文的 优先级为 48。
DSCP

#### 5.12 配置从对等体/对等体组学到的路由不受迭代策略控制

##### 1. 功能简介

通过 protocol nexthop recursive-lookup 命令配置 路由按照路由策略进行迭代下一BGP跳查找后，可以防止路由变化时的流量丢失，从对等体学到的所有路由都会受迭代策略控制。但在某些组网环境中，不希望来自特定对等体的路由受迭代策略控制（比如直连 EBGP）时，可以配置本功能。

##### 2. 配置步骤

进入系统视图。
(1)
system-view进入 实例视图或 实例视图。
(2) BGP BGP-VPN进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(3) 配置从对等体/对等体组学到的路由不受迭代策略控制。
peer { group-name | ip-address [ mask-length ] | ipv6-address [ prefix-length ] } nexthop-recursive-policy disable缺省情况下，从对等体/对等体组学到的路由受迭代策略控制。

#### 5.13 开启BGP次优路由下刷RIB功能

##### 1. 功能简介

开启 BGP 次优路由下刷 RIB 功能后，当 BGP 路由表中最优路由为通过 network 命令生成或import-route 命令引入的路由，次优路由为从 BGP 对等体收到的路由时，次优路由会下刷到RIB 表项中。在某些组网情况下，执行本命令下刷到达同一目的网络次优路由到 RIB 后，当最优路由发生故障时，系统可以快速切换到次优路由。例如，设备有一条到达 网络的静态路由，
1.1.1.0/24其优先级高于 BGP 路由，BGP 本地引入该静态路由同时从对等体收到到达该网段的路由，执行本命令 BGP 将从对等体收到的路由做为次优路由下刷到 RIB，这时如果开启协议间的 FRR 功能，当静态路由发生故障时，本地引入的静态路由不可达，系统可以快速切换到 次优路由，从而大BGP大缩短了流量中断时间。
协议间 功能的详细介绍，请参见“三层技术-IP 路由配置指导”中的“IP 路由基础”。
FRR

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 BGP 视图。
bgp as-number [ instance instance-name ]
(3) 开启 BGP 次优路由下刷 RIB 功能。

flush suboptimal-route缺省情况下，BGP 次优路由下刷 RIB 功能处于关闭状态，即只有 BGP 最优路由可以下刷到RIB。

#### 5.14 调整和优化BGP网络显示和维护

##### 5.14.1 显示BGP

在完成上述配置后，在任意视图下执行 命令可以显示配置后 的运行情况，通过查看display BGP显示信息验证配置的效果。

###### 1. 调整和优化BGP网络配置显示（IPv4单播）

表5-1 调整和优化 BGP 网络配置显示（IPv4 单播）
操作 命令display bgp [ instance instance-name ] peer ipv4显示邻居收到的 ORF 消息中的前缀信息 [ unicast ] [ vpn-instance vpn-instance-name ] ipv4-address received prefix-list

###### 2. 调整和优化BGP网络配置显示（IPv6单播）

表5-2 调整和优化 BGP 网络配置显示（IPv6 单播）
操作 命令display bgp [ instance instance-name ] peer ipv6 [ unicast ] [ vpn-instance vpn-instance-name ] ipv6-address received prefix-list显示邻居收到的ORF消息中的前缀信息display bgp [ instance instance-name ] peer ipv6 unicast ipv4-address received prefix-list [ ]

###### 3. 调整和优化BGP网络配置显示（IPv4组播）

表5-3 调整和优化 BGP 网络配置显示（IPv4 组播）
操作 命令display bgp [ instance instance-name ] peer ipv4显示邻居收到的ORF消息中的前缀信息multicast ipv4-address received prefix-list

###### 4. 调整和优化BGP网络配置显示（IPv6组播）

表5-4 调整和优化 BGP 网络配置显示（IPv6 组播）
操作 命令display bgp instance instance-name peer ipv6 [ ]显示邻居收到的ORF消息中的前缀信息multicast ipv6-address received prefix-list

##### 5.14.2 复位BGP会话

当 路由策略或协议发生变化后，如果需要通过复位 会话使新的配置生效，请在用户视图BGP BGP下进行下列配置。
表5-5 复位 会话BGP操作 命令reset bgp [ instance instance-name ] { as-number | ipv4-address [ mask-length ] | all | external | group复位IPv4单播地址族下的BGP会话group-name | internal } ipv4 [ unicast ] [ vpn-instance vpn-instance-name ] reset bgp [ instance instance-name ] { as-number |复位IPv4组播地址族下的BGP会话 ipv4-address [ mask-length ] | all | external | group group-name | internal } ipv4 multicast reset bgp [ instance instance-name ] { as-number | ipv6-address [ prefix-length ] | all | external | group group-name | internal } ipv6 [ unicast ]复位 IPv6 单播地址族下的 BGP 会话[ vpn-instance vpn-instance-name ] reset bgp ipv4-address [ mask-length ] ipv6 [ unicast ] reset bgp [ instance instance-name ] { as-number |复位IPv6组播地址族下的BGP会话 ipv6-address [ prefix-length ] | all | external | group group-name | internal } ipv6 multicast复位所有BGP会话 reset bgp [ instance instance-name ] all

#### 5.15 调整和优化BGP网络典型配置举例

##### 5.15.1 BGP负载分担配置

###### 1. 组网需求

所有交换机都配置 BGP，Switch A 在 AS 65008 中，Switch B 和 Switch C 在 AS 65009 中。
Switch A 与 Switch B、Switch C 之间运行 EBGP，Switch B 和 Switch C 之间运行 IBGP。
在 Switch A 上配置负载分担的路由条数为 2，以提高链路利用率。

###### 2. 组网图

图5-1 BGP 负载分担配置组网图

###### 3. 配置步骤

(1) 配置各接口的 IP 地址（略）
(2) 配置 BGP 连接
在 Switch A 上与 Switch B、Switch C 分别建立 EBGP 连接，并将 8.1.1.0/24 网段的路由
(cid:123)
通告给 Switch B 和 Switch C，以便 Switch B 和 Switch C 能够访问 Switch A 的内部网络。
在 Switch B 上与 Switch A 建立 EBGP 连接，与 Switch C 建立 IBGP 连接，并将 9.1.1.0/24
(cid:123)
网段的路由通告给 Switch A，以便 Switch A 能够通过 Switch B 访问内部网络。同时，在
上配置一条到 接口的静态路由（也可以用 等协议来
Switch B Switch C Loopback0 OSPF
实现），以便使用 Loopback 接口建立 IBGP 连接。
在 Switch C 上与 Switch A 建立 EBGP 连接，与 Switch B 建立 IBGP 连接，并将 9.1.1.0/24
(cid:123)
网段的路由通告给 Switch A，以便 Switch A 能够通过 Switch C 访问内部网络。同时，在
Switch C 上配置一条到 Switch B Loopback0 接口的静态路由（也可以用 OSPF 等协议来
实现），以便使用 Loopback 接口建立 IBGP 连接。
配置 A。
\# Switch
<SwitchA> system-view
[SwitchA] bgp 65008
[SwitchA-bgp-default] router-id 1.1.1.1
[SwitchA-bgp-default] peer 3.1.1.1 as-number 65009
[SwitchA-bgp-default] peer 3.1.2.1 as-number 65009
[SwitchA-bgp-default] address-family ipv4 unicast
[SwitchA-bgp-default-ipv4] peer 3.1.1.1 enable
[SwitchA-bgp-default-ipv4] peer 3.1.2.1 enable
[SwitchA-bgp-default-ipv4] network 8.1.1.0 24
[SwitchA-bgp-default-ipv4] quit
[SwitchA-bgp-default] quit
\# 配置 Switch B。
<SwitchB> system-view

[SwitchB] bgp 65009 [SwitchB-bgp-default] router-id 2.2.2.2 [SwitchB-bgp-default] peer 3.1.1.2 as-number 65008 [SwitchB-bgp-default] peer 3.3.3.3 as-number 65009 [SwitchB-bgp-default] peer 3.3.3.3 connect-interface loopback 0 [SwitchB-bgp-default] address-family ipv4 unicast [SwitchB-bgp-default-ipv4] peer 3.1.1.2 enable [SwitchB-bgp-default-ipv4] peer 3.3.3.3 enable [SwitchB-bgp-default-ipv4] network 9.1.1.0 24 [SwitchB-bgp-default-ipv4] quit [SwitchB-bgp-default] quit [SwitchB] ip route-static 3.3.3.3 32 9.1.1.2 \# 配置 Switch C。
<SwitchC> system-view [SwitchC] bgp 65009 [SwitchC-bgp-default] router-id 3.3.3.3 [SwitchC-bgp-default] peer 3.1.2.2 as-number 65008 [SwitchC-bgp-default] peer 2.2.2.2 as-number 65009 [SwitchC-bgp-default] peer 2.2.2.2 connect-interface loopback 0 [SwitchC-bgp-default] address-family ipv4 unicast [SwitchC-bgp-default-ipv4] peer 3.1.2.2 enable [SwitchC-bgp-default-ipv4] peer 2.2.2.2 enable [SwitchC-bgp-default-ipv4] network 9.1.1.0 24 [SwitchC-bgp-default-ipv4] quit [SwitchC-bgp-default] quit [SwitchC] ip route-static 2.2.2.2 32 9.1.1.1 \# 查看 Switch A 的路由表。
[SwitchA] display bgp routing-table ipv4 Total number of routes: 3 BGP local router ID is 1.1.1.1 Status codes: * - valid, > - best, d - dampened, h - history, s - suppressed, S - stale, i - internal, e - external a – additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn
* > 8.1.1.0/24 8.1.1.1 0 32768 i
* >e 9.1.1.0/24 3.1.1.1 0 0 65009i
* e 3.1.2.1 0 0 65009i从 BGP 路由表中可以看出，到目的地址 9.1.1.0/24 有两条有效路由，其中下一跳为 3.1.1.1 (cid:123)
的路由前有标志“ > ”，表示它是当前有效的最优路由（因为 Switch B 的路由器 ID 要小一些）；而下一跳为 的路由前有标志“*”，表示它是当前有效的路由，但不是最优的。
3.1.2.1使用 display ip routing-table 命令查看 路由表项，可以看出到达目的地址IP (cid:123)
9.1.1.0/24 的路由只有一条，下一跳地址为 3.1.1.1，出接口为 Vlan200。

###### 4. 验证配置

(3) 配置负载分担
因为 Switch A 有两条路径到达 AS 65009 的内部网络，所以，可以在 Switch A 配置负载分担
的路由条数为 2，以提高链路利用率。
配置 A。
\# Switch
[SwitchA] bgp 65008
[SwitchA-bgp-default] address-family ipv4 unicast
[SwitchA-bgp-default-ipv4] balance 2
[SwitchA-bgp-default-ipv4] quit
[SwitchA-bgp-default] quit
验证配置
4.
\# 查看 Switch A 的 BGP 路由表。
[SwitchA] display bgp routing-table ipv4
Total number of routes: 3
BGP local router ID is 1.1.1.1
Status codes: * - valid, > - best, d - dampened, h - history,
s - suppressed, S - stale, i - internal, e - external
a – additional-path
Origin: i - IGP, e - EGP, ? - incomplete
Network NextHop MED LocPrf PrefVal Path/Ogn
* > 8.1.1.0/24 8.1.1.1 0 32768 i
* >e 9.1.1.0/24 3.1.1.1 0 0 65009i
* >e 3.1.2.1 0 0 65009i
• 从 BGP 路由表中可以看到，BGP 路由 9.1.1.0/24 存在两个下一跳，分别是 3.1.1.1 和 3.1.2.1，
两条路由前都有标志“>”，表明它们都是当前有效的最优路由。
使用 display ip routing-table 命令查看 IP 路由表项，可以看出到达目的地址
•
的路由有两条，其中一条的下一跳地址为 3.1.1.1，出接口为 Vlan200；另一条的
9.1.1.0/24
下一跳地址为 3.1.2.1，出接口为 Vlan300。

##### 5.15.2 BGP Add-Path配置

###### 1. 组网需求

所有路由器运行 BGP 协议，Switch A 与 Switch B 和 Switch C 建立 EBGP 连接，Switch B、Switch C 和 Switch D 之间建立 IBGP 连接，Route D 与 Route E 建立 IBGP 连接。
Switch D 作为路由反射器，Switch E 为 Switch D 的客户机。
配置 Add-Path 功能，使 Switch E 通过 Switch D 学到 Switch B 和 Switch C 转发的前缀相同下一跳不同的路由信息。

###### 2. 组网图

图5-2 BGP Add-Path 配置组网图

| 接口 | IP地址 | 设备 | 接口 |
|---|---|---|---|
| Vlan-int100 | 10.1.1.1/24 | Switch D | Vlan-int300 |
| Vlan-int200 | 20.1.1.1/24 |  | Vlan-int400 |
| Vlan-int100 | 10.1.1.2/24 |  | Vlan-int500 |
| Vlan-int300 | 30.1.1.2/24 | Switch E | Vlan-int500 |
| Vlan-int200 | 20.1.1.2/24 |  |  |
| Vlan-int400 | 40.1.1.2/24 |  |  |

设备 IP地址Switch A 30.1.1.1/24
40.1.1.1/24 Switch B 50.1.1.1/24
50.1.1.2/24 Switch C

###### 3. 配置步骤

(1) 配置各接口的 IP 地址。
配置 连接
(2) BGP
配置 A。
\# Switch
<SwitchA> system-view
[SwitchA] bgp 10
[SwitchA-bgp-default] peer 10.1.1.2 as-number 20
[SwitchA-bgp-default] peer 20.1.1.2 as-number 20
[SwitchA-bgp-default] address-family ipv4 unicast
[SwitchA-bgp-default-ipv4] peer 10.1.1.2 enable
[SwitchA-bgp-default-ipv4] peer 20.1.1.2 enable
\# 配置 Switch B。
<SwitchB> system-view
[SwitchB] bgp 20
[SwitchB-bgp-default] peer 10.1.1.1 as-number 10
[SwitchB-bgp-default] peer 30.1.1.1 as-number 20
[SwitchB-bgp-default] address-family ipv4 unicast
[SwitchB-bgp-default-ipv4] peer 10.1.1.1 enable
[SwitchB-bgp-default-ipv4] peer 30.1.1.1 enable
\# 配置 Switch C 。
<SwitchC> system-view
[SwitchC] bgp 20
[SwitchC-bgp-default] peer 20.1.1.1 as-number 10

[SwitchC-bgp-default] peer 40.1.1.1 as-number 20 [SwitchC-bgp-default] address-family ipv4 unicast [SwitchC-bgp-default-ipv4] peer 10.1.1.1 enable [SwitchC-bgp-default-ipv4] peer 30.1.1.1 enable \# 配置 Switch D。
<SwitchD> system-view [SwitchD] bgp 20 [SwitchD-bgp-default] peer 30.1.1.2 as-number 20 [SwitchD-bgp-default] peer 40.1.1.2 as-number 20 [SwitchD-bgp-default] peer 50.1.1.2 as-number 20 [SwitchD-bgp-default] address-family ipv4 unicast [SwitchD-bgp-default-ipv4] peer 30.1.1.2 enable [SwitchD-bgp-default-ipv4] peer 40.1.1.2 enable [SwitchD-bgp-default-ipv4] peer 50.1.1.2 enable \# 配置 Switch E。
<SwitchE> system-view [SwitchE] bgp 20 [SwitchE-bgp-default] peer 50.1.1.1 as-number 20 [SwitchE-bgp-default] address-family ipv4 unicast [SwitchE-bgp-default-ipv4] peer 50.1.1.1 enable
(3) 配置发布本地路由\# 配置 Switch A 发布本地 10.1.1.0 24 的路由信息[SwitchA-bgp-default-ipv4] network 10.1.1.0 24
(4) 将下一跳的属性修改成自身的地址\# 配置 Switch B。
[SwitchB-bgp-default-ipv4] peer 30.1.1.1 next-hop-local \# 配置 Switch C。
[SwitchC-bgp-default-ipv4] peer 40.1.1.1 next-hop-local
(5) 配置路由反射器\# 配置 Switch D。
[SwitchD-bgp-default-ipv4] peer 50.1.1.2 reflect-client配置
(6) Add-Path配置 使能 发送能力，配置 优选路由的最大条数为 2，配置向\# Switch D Add-Path Add-Path对等体 50.1.1.2 发送 Add-Path 优选路由的最大条数为 2。
[SwitchD-bgp-default-ipv4] peer 50.1.1.2 additional-paths send [SwitchD-bgp-default-ipv4] additional-paths select-best 2 [SwitchD-bgp-default-ipv4] peer 50.1.1.2 advertise additional-paths best 2 \# 配置 Switch E 使能 Add-Path 接收能力。
[SwitchE-bgp-default-ipv4] peer 50.1.1.1 additional-paths receive

###### 4. 验证配置

\# 查看 Switch E 的 BGP 路由信息。
[Switch E] display bgp routing-table ipv4 Total number of routes: 2

BGP local Switch ID is 50.1.1.2 Status codes: * - valid, > - best, d - dampened, h - history s - suppressed, S - stale, i - internal, e - external a - additional-path Origin: i - IGP, e - EGP, ? - incomplete Network NextHop MED LocPrf PrefVal Path/Ogn i 10.1.1.0/24 30.1.1.2 0 100 0 10i i 40.1.1.2 0 100 0 10i可以看到从 Switch D 学到的两条前缀相同下一跳不同的路由信息。

##### 1. 功能简介

### 6 BGP安全功能

#### 6.1 BGP安全功能配置任务简介

BGP 安全功能配置任务如下：
• 配置BGP的MD5 认证
• 配置BGP GTSM功能
• 配置BGP的keychain认证
• 配置通过IPsec保护IPv6 BGP报文
• 配置BGP RPKI

#### 6.2 配置BGP的MD5认证

功能简介
1.
通过为 BGP 对等体配置 BGP 的 MD5 认证，可以在以下两方面提高 BGP 的安全性：
• 为 BGP 建立 TCP 连接时进行 MD5 认证，只有两台路由器配置的密钥相同时，才能建立 TCP连接，从而避免与非法的 BGP 路由器建立 TCP 连接。
传递 BGP 报文时，对封装 BGP 报文的 TCP 报文段进行 MD5 运算，从而保证 BGP 报文不会
•被篡改。

##### 2. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 实例视图。
BGP-VPN
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
配置 的 认证。
(3) BGP MD5
peer { group-name | ipv4-address [ mask-length ] } password { cipher |
simple } password
缺省情况下，不进行 的 认证。
BGP MD5

##### 3. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]

请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(3) 配置 BGP 的 MD5 认证。
peer { group-name | ipv6-address [ prefix-length ] } password { cipher | simple } password缺省情况下，不进行 BGP 的 MD5 认证。

#### 6.3 配置BGP GTSM功能

##### 1. 功能简介

GTSM（Generalized TTL Security Mechanism，通用 TTL 安全保护机制）是一种简单易行的、对基于 IP 协议的上层业务进行保护的安全机制。GTSM 通过检查接收到的 IP 报文头中的 TTL 值是否在一个预先定义好的范围内，来判断 IP 报文是否合法，避免攻击者向网络设备发送大量有效的 IP报文时对网络设备造成的 利用（CPU-utilization）等类型的攻击。
CPU配置 功能时，用户可以指定本地设备到达某个对等体的最大跳数为 hop-count，则从BGP GTSM该对等体接收到的 BGP 报文的合法 TTL 范围为 255-“hop-count”+1 到 255。只有来自该对等体的报文 TTL 值在该合法范围内时，才将报文上送 CPU 处理；否则，直接丢弃报文。另外，配置功能后，设备会将发送报文的初始 设置为 255。
BGP GTSM TTL对于直连 EBGP 对等体，GTSM 可以提供最佳的保护效果；对于非直连 EBGP 或 IBGP 对等体，由于中间设备可能对 TTL 值进行篡改，GTSM 的保护效果受到中间设备安全性的限制。

##### 2. 配置限制和指导

执行本配置后，只要本地设备和指定的对等体通过了 GTSM 检查，就允许在二者之间建立 EBGP会话，不管二者之间的跳数是否超过 peer ebgp-max-hop 命令指定的跳数范围。
使用 BGP GTSM 功能时，要求本设备和对等体设备上同时配置本特性，指定的 hop-count 值可以不同，只要能够满足合法性检查即可。

##### 3. 配置步骤（IPv4单播/IPv4组播）

进入系统视图。
(1)
system-view进入 实例视图或 实例视图。
(2) BGP BGP-VPN进入 实例视图。
BGP (cid:123)
bgp as-number [ instance instance-name ]请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(3) 使能对等体/对等体组的 BGP GTSM 功能。
peer { group-name | ipv4-address [ mask-length ] } ttl-security hops hop-count缺省情况下，BGP 功能处于关闭状态。
GTSM

##### 1. 功能简介

##### 4. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
使能对等体/对等体组的 功能。
(3) BGP GTSM
peer { group-name | ipv6-address [ prefix-length ] } ttl-security hops
hop-count
缺省情况下，BGP GTSM 功能处于关闭状态。

#### 6.4 配置BGP的keychain认证

功能简介
1.
配置 keychain 认证可以提高 TCP 连接的安全性。BGP 对等体两端必须都配置 keychain 认证，且配置的 必须使用相同的认证算法和密码，才能正常建立 连接，交互 消息。
keychain TCP BGP配置 BGP 的 keychain 认证前，必须配置对应的 keychain，否则 TCP 连接不能正常建立。
关于 keychain 的介绍和配置，请参见“安全配置指导”中的“keychain”。

##### 2. 配置步骤（IPv4单播/IPv4组播）

进入系统视图。
(1)
system-view进入 实例视图或 实例视图。
(2) BGP BGP-VPN进入 实例视图。
BGP (cid:123)
bgp as-number [ instance instance-name ]请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(3) 配置 BGP 的 keychain 认证。
peer { group-name | ip-address [ mask-length ] } keychain keychain-name缺省情况下，不进行 BGP 的 keychain 认证。

##### 3. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)

bgp as-number [ instance instance-name ]请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(3) 配置 BGP 的 keychain 认证。
peer { group-name | ipv6-address [ prefix-length ] } keychain keychain-name缺省情况下，不进行 BGP 的 keychain 认证。

#### 6.5 配置通过IPsec保护IPv6 BGP报文

##### 1. 功能简介

为了避免路由信息外泄或者非法者对设备进行恶意攻击，可以利用 IPsec 安全隧道对 IPv6 BGP 报文进行保护。通过 IPsec 提供的数据机密性、完整性、数据源认证等功能，确保 IPv6 BGP 报文不会被侦听或恶意篡改，并避免非法者构造 IPv6 BGP 报文对设备进行攻击。
在互为 IPv6 BGP 邻居的两台设备上都配置通过 IPsec 保护 IPv6 BGP 报文后，一端设备在发送 IPv6报文时通过 对报文进行加封装，另一端设备接收到报文后，通过 对报文进行解封BGP IPsec IPsec装。如果解封装成功，则接收该报文，正常建立 IPv6 BGP 对等体关系或学习 IPv6 BGP 路由；如果设备接收到不受 IPsec 保护的 IPv6 BGP 报文，或 IPv6 BGP 报文解封装失败，则会丢弃该报文。

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置 IPsec 安全提议和手工方式的 IPsec 安全框架。
配置方法请参见“安全配置指导”中的“IPsec”。
(3) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
(4) 为 IPv6 BGP 对等体/对等体组应用 IPsec 安全框架。
peer { group-name | ipv6-address [ prefix-length ] } ipsec-profile
profile-name
缺省情况下，IPv6 BGP 对等体/对等体组没有应用 IPsec 安全框架。
应用的安全框架必须是手工方式的 IPsec 安全框架。

###### 1. 功能简介

#### 6.6 配置BGP RPKI

##### 6.6.1 功能简介

BGP 路由中的 AS_PATH 属性记录了某条路由从本地到某个 IP 地址（网段）所要经过的所有 AS号。其中，该 IP 地址（网段）所处的 AS 称为源 AS。如果源 AS 号错误会导致无法到达指定 IP 地址（网段）甚至网络瘫痪。使用 RPKI（Resource Infrastructure，资源公钥基础设BGP Public Key施）功能，设备在收到 BGP 路由的时候，会验证源 AS 是否合法，并根据验证结果来决定是否使用该 BGP 路由以及是否发布该路由。

##### 6.6.2 配置RPKI连接参数

功能简介
1.
路由器通过 TCP 协议与 RPKI 服务器建立连接。TCP 连接建立后，路由器从 RPKI 服务器获取 ROA信息。
路由器会根据刷新时间间隔检测与 服务器的连接关系，如果在响应时间内没有收到服务器的RPKI回应，路由器与 RPKI 服务器的连接断开。
与 RPKI 服务器的连接断开后（不包括用户执行 shutdown 命令关闭接口引起的连接断开），路由器会尝试与 RPKI 服务器重新建立连接，并将从该服务器获得的 ROA 信息置为老化状态，路由器将执行如下操作：
• 如果老化时间内，路由器重新与 RPKI 服务器建立连接，则解除 ROA 信息的老化状态。
• 如果直到老化时间超时，路由器与 RPKI 服务器仍然无法重新建立连接，则删除该 ROA 信息。

###### 2. 配置限制和指导

信息的老化时间建议大于 服务器的响应等待时间。
ROA BGP RPKI RPKI 连接建立后，会一直处于通信状态，并周期更新 ROA 信息。如果需要暂时断开某个 RPKI 连接，请在 服务器视图下执行 命令。
BGP RPKI undo port执行 命令后，BGP 视图下的所有配置都会被删除。
undo rpki RPKI

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
开启 功能，并进入 视图。
(3) BGP RPKI BGP RPKI
rpki
配置 服务器地址，并进入 服务器视图。
(4) BGP RPKI BGP RPKI
server [ vpn-instance vpn-instance-name ] tcp { ipv4-address |
ipv6-address }
缺省情况下，未配置 BGP RPKI 的服务器地址。
(5) 配置 BGP RPKI 服务端口号。
port port-number

###### 1. 功能简介

缺省情况下，未配置 BGP RPKI 服务端口。
只有配置与 BGP RPKI 服务器连接的 TCP 端口，才能与 RPKI 服务器建立连接，且本地配置的端口号必须与 服务器上使用的端口号保持一致。
BGP RPKI（可选）指定 连接中使用的 认证密码。
(6) RPKI MD5 passwords { cipher | simple } string缺省情况下，BGP 服务器不进行 的认证。
RPKI MD5使用 MD5 认证时，认证密码必须与 RPKI 服务器上的认证密码保持一致。MD5 认证既可以确保路由器与合法的 BGP RPKI 服务器建立连接，也可以确保 BGP RPKI 报文不会被篡改。
（可选）配置 连接的检测周期。
(7) RPKI refresh-time refresh-time缺省情况下，RPKI 连接的检测周期为 秒。
600本功能用于检测路由器与 服务器的连接状态。
RPKI（可选）配置等待 服务器的响应时间。
(8) BGP RPKI response-time response-time缺省情况下，等待 BGP RPKI 服务器响应时间为 30 秒。
(9) （可选）配置 ROA 信息的老化时间。
purge-time purge-time缺省情况下，ROA 信息的老化时间为 60 秒。

##### 6.6.3 开启BGP RPKI验证功能

功能简介
1.
配置本功能后，设备收到 BGP 路由时，会对 IP 地址（网段）和源 AS 号进行 RPKI 验证。验证结果有以下三种：
Not-found：表示 数据库中不存在包含该 地址（网段）的表项。
• ROA IP Valid：表示 数据库中至少存在一条包含该 地址（网段）的表项，且表项中的 号
• ROA IP AS和收到的路由的源 AS 号相同。
• Invalid：表示 ROA 数据库中至少存在一条包含该 IP 地址（网段）的表项，但表项中的 AS 号和收到的路由的源 AS 号均不同。

###### 2. 配置限制和指导

配置本功能后，设备将使用本地验证的结果作为 RPKI 验证结果；未配置本功能时，将使用 BGP路由报文中的 验证结果。
RPKI

###### 3. 配置步骤

(1) 进入系统视图。
system-view
进入 实例视图。
(2) BGP
bgp as-number [ instance instance-name ]
进入 视图。
(3) BGP RPKI
rpki

(4) 开启 BGP RPKI 验证功能。
check-origin-validation
缺省情况下，BGP RPKI 验证功能处于关闭状态。

##### 6.6.4 配置BGP RPKI验证结果参与路由优选

###### 1. 功能简介

RPKI 验证结果的优先级从高到低依次为 Valid、Not found、Invalid。
配置本功能后，RPKI验证结果将参与路由优选。BGP选择路由时首先丢弃下一跳不可达的路由，其次按照RPKI验证结果进行路由优选，即对于去往同一个IP地址（网段）的多条BGP路由，选择RPKI验证结果优先级最高的路由为最优路由。如果RPKI验证结果相同，则根据“1.5 BGP的选路规则”中的规则选择路由。
无 RPKI 验证结果的路由在与有验证结果的路由共同参与路由优选时，按 Not-found 验证结果处理。
用户可以使用路由策略设置 BGP RPKI 验证结果的匹配条件，从而灵活控制路由的发布与接收。关于路由策略的详细介绍，请参见“三层技术 -IP 路由配置指导”中的“路由策略”。

###### 2. 配置步骤（IPv4单播）

进入系统视图。
(1)
system-view进入 单播地址族视图或 单播地址族视图。
(2) BGP IPv4 BGP-VPN IPv4请依次执行以下命令进入 单播地址族视图。
BGP IPv4 (cid:123)
bgp as-number [ instance instance-name ] address-family ipv4 [ unicast ]请依次执行以下命令进入 BGP-VPN IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv4 [ unicast ]
(3) 配置 BGP RPKI 验证结果参与路由优选。
bestroute origin-as-validation [ allow-invalid ]缺省情况下， BGP RPKI 验证结果不参与路由优选。
未配置 allow-invalid 参数时，验证结果为 Invalid 的路由不参与路由优选。如果希望验证结果为 Invalid 的路由参与路由优选，可以配置 allow-invalid 参数。

###### 3. 配置步骤（IPv6单播）

进入系统视图。
(1)
system-view
(2) 进入 BGP IPv6 单播地址族视图或 BGP-VPN IPv6 单播地址族视图。
请依次执行以下命令进入 BGP IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] address-family ipv6 [ unicast ]请依次执行以下命令进入 BGP-VPN IPv6 单播地址族视图。
(cid:123)

bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv6 [ unicast ]
(3) 配置 BGP RPKI 验证结果参与路由优选。
bestroute origin-as-validation [ allow-invalid ]缺省情况下，BGP RPKI 验证结果不参与路由优选。
未配置 allow-invalid 参数时，验证结果为 Invalid 的路由不参与路由优选。如果希望验证结果为 Invalid 的路由参与路由优选，可以配置 allow-invalid 参数。

##### 6.6.5 配置向对等体/对等体组发送BGP RPKI验证结果

###### 1. 配置限制和指导

验证结果以扩展团体属性的方式传递，配置本条命令前必先配置向对等体/对等体组发布BGP RPKI扩展团体属性且 RPKI 正确配置。未配置向对等体/对等体组发布扩展团体属性，此配置不生效。
目前，设备仅支持向 IBGP 对等体/对等体组发送 BGP RPKI 验证结果。

###### 2. 配置步骤（IPv4单播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv4 单播地址族视图或 BGP-VPN IPv4 单播地址族视图。
请依次执行以下命令进入 BGP IPv4 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ]
address-family ipv4 [ unicast ]
请依次执行以下命令进入 单播地址族视图。
BGP-VPN IPv4
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
address-family ipv4 [ unicast ]
(3) 配置向对等体/对等体组发布扩展团体属性。
peer { group-name | ipv4-address [ mask-length ] }
advertise-ext-community
缺省情况下，不向对等体/对等体组发布扩展团体属性。
配置向对等体/对等体组发送 验证结果。
(4) BGP RPKI
peer { group-name | ipv4-address [ mask-length ] } advertise
origin-as-validation
缺省情况下，不会向对等体/对等体组发送 BGP RPKI 验证结果。

###### 3. 配置步骤（IPv6单播）

(1) 进入系统视图。
system-view
(2) 进入 BGP IPv6 单播地址族视图或 BGP-VPN IPv6 单播地址族视图。
请依次执行以下命令进入 BGP IPv6 单播地址族视图。
(cid:123)

bgp as-number [ instance instance-name ] address-family ipv6 [ unicast ]请依次执行以下命令进入 BGP-VPN IPv6 单播地址族视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name address-family ipv6 [ unicast ]
(3) 配置向对等体/对等体组发布扩展团体属性。
peer { group-name | ipv6-address [ prefix-length ] } advertise-ext-community缺省情况下，不向对等体/对等体组发布扩展团体属性。
(4) 配置向对等体/对等体组发送 BGP RPKI 验证结果。
peer { group-name | ipv6-address [ prefix-length ] } advertise origin-as-validation缺省情况下，不会向对等体/对等体组发送 BGP RPKI 验证结果。

##### 6.6.6 复位BGP RPKI会话

在用户视图下执行以下命令复位 BGP RPKI 连接。
reset bgp [ instance instance-name ] rpki server [ vpn-instance vpn-instance-name ] tcp { ipv4 address | ipv6 address }

#### 6.7 BGP安全功能显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 BGP 的运行情况，通过查看显示信息验证配置的效果。

##### 1. BGP安全功能配置显示（IPv4单播）

表6-1 BGP 安全功能配置显示（IPv4 单播）
操作 命令display bgp [ instance instance-name ] rpki server显示与RPKI服务器连接的相关信息[ [ vpn-instance vpn-instance-name ] ipv4-address ] display bgp [ instance instance-name ] rpki table显示从RPKI服务器获得的ROA信息ipv4 [ ipv4-address min min-length max max-length ]

##### 2. BGP安全功能配置显示（IPv6单播）

表6-2 BGP 安全功能配置显示（IPv6 单播）
操作 命令display bgp [ instance instance-name ] rpki server显示与RPKI服务器连接的相关信息[ [ vpn-instance vpn-instance-name ] ipv6-address ] display bgp [ instance instance-name ] rpki table显示从RPKI服务器获得的ROA信息ipv6 [ ipv6-address min min-length max max-length

#### 6.8 IPv4 BGP安全功能典型配置举例

##### 6.8.1 BGP RPKI配置

###### 1. 组网需求

• 所有路由器运行 BGP 协议，Switch A 与 RPKI 服务器建立连接。Switch A 与 Switch B 建立
IBGP 连接。
• Switch A 将 BGP RPKI 验证结果发送给 Switch B。
• 配置路由策略，使得 Switch B 对收到的 BGP RPKI 验证结果设置匹配条件，控制路由的接
收。

###### 2. 组网图

图6-1 配置组网图BGP RPKI

###### 3. 配置步骤

配置各接口的 地址，在 和 上配置 BGP，建立 邻居，配置过程略
(1) IP Switch A Switch B IBGP配置 与 服务器建立连接
(2) Switch A RPKI <SwitchA> system-view [SwitchA] bgp 100 [SwitchA-bgp-default] rpki [SwitchA-bgp-default-rpki] server tcp 1.1.1.2 [SwitchA-bgp-default-rpki-server] port 1234 [SwitchA-bgp-default-rpki-server] quit在 上开启 验证
(3) Switch A BGP RPKI [SwitchA-bgp-default-rpki] check-origin-validation [SwitchA-bgp-default-rpki] quit
(4) 在 Switch A 上配置 BGP RPKI 验证结果参与路由优选[SwitchA-bgp-default] address-family ipv4 [SwitchA-bgp-default-ipv4] bestroute origin-as-validation

(5) 在 Switch A 上配置向对等体 1.2.3.2 发送 BGP RPKI 验证结果
[SwitchA-bgp-default-ipv4] peer 1.2.3.2 advertise-ext-community
[SwitchA-bgp-default-ipv4] peer 1.2.3.2 advertise origin-as-validation
[SwitchA-bgp-default-ipv4] quit
[SwitchA-bgp-default] quit
(6) 在 Switch B 上对收到的 BGP RPKI 验证结果设置匹配条件，仅接收验证结果为 Valid 的路由
\# 配置路由策略。
<SwitchB> system-view
[SwitchB] route-policy rpki_policy permit node 0
[SwitchB-route-policy-rpki_policy-0] if-match rpki valid
[SwitchB-route-policy-rpki_policy-0] quit
应用路由策略。
\#
[SwitchB] bgp 100
[SwitchB-bgp-default] address-family ipv4
[SwitchB-bgp-default-ipv4] peer 1.2.3.1 route-policy rpki_policy import

###### 4. 验证配置

\# 查看 Switch A 与 RPKI 服务器的连接信息，可以看到 Switch A 与 RPKI 服务器已经建立连接。
[SwitchA] display bgp rpki server Server VPN-index Port State Time ROAs(IPv4/IPv6)
1.1.1.2 0 1234 Establish 00:04:43 5/4 \# 查看从 RPKI 服务器获取的 ROA 信息，可以看到可以看到已经获得 ROA 信息。
[SwitchA] display bgp rpki table ipv4 Total number of entries: 5 Status codes: S - stale, U - used Network Mask-range Origin-AS Server Status
1.2.3.4 8-24 100 1.1.1.2 U
2.2.3.6 8-32 100 1.1.1.2 U
2.2.3.6 10-24 4294967295 1.1.1.2 U
2.2.3.9 20-24 4294967295 1.1.1.2 U
3.2.3.5 8-26 200 1.1.1.2 U \# 查看 Switch A 上 BGP RPKI 验证结果。
[SwitchA] display bgp routing-table ipv4 1.2.3.0 BGP local router ID: 2.2.2.2 Local AS number: 100 Paths: 1 available, 1 best BGP routing table information of 1.2.3.0/24:
Imported route.
Original nexthop: 0.0.0.0 OutLabel : NULL

RxPathID : 0x0 TxPathID : 0x0 Org-validation : Valid AS-path : (null)
Origin : incomplete Attribute value : MED 0, pref-val 32768 State : valid, local, best IP precedence : N/A QoS local ID : N/A Traffic index : N/A
1.2.3.0/24 在 ROA 数据库中的 Network 为 1.2.3.4，Mask-range 为 8-24 的地址前缀范围内，且 AS和路由的源 AS 相匹配，因此验证结果为 Valid。
\# 查看 Switch B 上到达目的网络 1.2.3.0 的 BGP IPv4 单播路由的详细信息。
[SwitchB] display bgp routing-table ipv4 1.2.3.0 RR-client route.
From : 1.2.3.1 (192.168.56.22)
Rely nexthop : 1.2.3.1 Original nexthop: 1.2.3.1 OutLabel : NULL Ext-Community : <Origin Valid State: Valid > RxPathID : 0x0 TxPathID : 0x0 Org-validation : Valid AS-path : (null)
Origin : incomplete Attribute value : MED 0, localpref 100, pref-val 0 State : valid, internal, best IP precedence : N/A QoS local ID : N/A Traffic index : N/A由于 仅允许 验证结果为 的路由信息通过，因此可以看到到达目的网络Switch B BGP RPKI Valid
1.2.3.0 的 BGP IPv4 单播路由的信息。该路由信息中的扩展团体属性包含了 BGP RPKI 验证结果。

#### 6.9 IPv6 BGP安全功能典型配置举例

##### 6.9.1 通过IPsec保护IPv6 BGP报文配置

###### 1. 组网需求

Switch A、Switch B 和 Switch C 三台交换机之间运行 IPv6 BGP 交互路由信息。Switch A 和
•Switch B 之间建立 IBGP 连接，Switch B 和 Switch C 之间建立 EBGP 连接。
为了提高安全性，配置通过 对 报文进行保护。
• IPsec IPv6 BGP

###### 2. 组网图

图6-2 通过 IPsec 保护 IPv6 BGP 报文组网图

###### 3. 配置步骤

(1) 配置各接口的 IPv6 地址（略）
(2) 配置 IBGP 连接
\# 配置 Switch A。
<SwitchA> system-view
[SwitchA] bgp 65008
[SwitchA-bgp-default] router-id 1.1.1.1
[SwitchA-bgp-default] group ibgp internal
[SwitchA-bgp-default] peer 1::2 group ibgp
[SwitchA-bgp-default] address-family ipv6 unicast
[SwitchA-bgp-default-ipv6] peer ibgp enable
[SwitchA-bgp-default-ipv6] quit
[SwitchA-bgp-default] quit
\# 配置 Switch B。
<SwitchB> system-view
[SwitchB] bgp 65008
[SwitchB-bgp-default] router-id 2.2.2.2
[SwitchB-bgp-default] group ibgp internal
[SwitchB-bgp-default] peer 1::1 group ibgp
[SwitchB-bgp-default] address-family ipv6 unicast
[SwitchB-bgp-default-ipv6] peer ibgp enable
[SwitchB-bgp-default-ipv6] quit
(3) 配置 EBGP 连接
\# 配置 Switch C。
<SwitchC> system-view
[SwitchC] bgp 65009
[SwitchC-bgp-default] router-id 3.3.3.3
[SwitchC-bgp-default] group ebgp external
[SwitchC-bgp-default] peer 3::1 as-number 65008
[SwitchC-bgp-default] peer 3::1 group ebgp
[SwitchC-bgp-default] address-family ipv6 unicast
[SwitchC-bgp-default-ipv6] peer ebgp enable
[SwitchC-bgp-default-ipv6] quit
[SwitchC-bgp-default] quit
配置 B。
\# Switch
[SwitchB-bgp-default] group ebgp external

[SwitchB-bgp-default] peer 3::2 as-number 65009 [SwitchB-bgp-default] peer 3::2 group ebgp [SwitchB-bgp-default] address-family ipv6 unicast [SwitchB-bgp-default-ipv6] peer ebgp enable [SwitchB-bgp-default-ipv6] quit [SwitchB-bgp-default] quit
(4) 配置 IPsec 安全提议和安全框架\# 配置 Switch A。创建名为 tran1 的安全提议，报文封装形式采用传输模式，安全协议采用协议。创建手工方式的安全框架 policy001，配置 和密钥。
ESP SPI [SwitchA] ipsec transform-set tran1 [SwitchA-ipsec-transform-set-tran1] encapsulation-mode transport [SwitchA-ipsec-transform-set-tran1] esp encryption-algorithm des [SwitchA-ipsec-transform-set-tran1] esp authentication-algorithm sha1 [SwitchA-ipsec-transform-set-tran1] quit [SwitchA] ipsec profile policy001 manual [SwitchA-ipsec-profile-policy001-manual] transform-set tran1 [SwitchA-ipsec-profile-policy001-manual] sa spi outbound esp 12345 [SwitchA-ipsec-profile-policy001-manual] sa spi inbound esp 12345 [SwitchA-ipsec-profile-policy001-manual] sa string-key outbound esp simple abcdefg [SwitchA-ipsec-profile-policy001-manual] sa string-key inbound esp simple abcdefg [SwitchA-ipsec-profile-policy001-manual] quit配置 B。创建名为 的安全提议，报文封装形式采用传输模式，安全协议采用\# Switch tran1 ESP 协议；创建手工方式的安全框架 policy001，配置 SPI 和密钥。创建名为 tran2 的安全提议，报文封装形式采用传输模式，安全协议采用 ESP 协议；创建手工方式的安全框架 policy002，配置 SPI 和密钥。
[SwitchB] ipsec transform-set tran1 [SwitchB-ipsec-transform-set-tran1] encapsulation-mode transport [SwitchB-ipsec-transform-set-tran1] esp encryption-algorithm des [SwitchB-ipsec-transform-set-tran1] esp authentication-algorithm sha1 [SwitchB-ipsec-transform-set-tran1] quit [SwitchB] ipsec profile policy001 manual [SwitchB-ipsec-profile-policy001-manual] transform-set tran1 [SwitchB-ipsec-profile-policy001-manual] sa spi outbound esp 12345 [SwitchB-ipsec-profile-policy001-manual] sa spi inbound esp 12345 [SwitchB-ipsec-profile-policy001-manual] sa string-key outbound esp simple abcdefg [SwitchB-ipsec-profile-policy001-manual] sa string-key inbound esp simple abcdefg [SwitchB-ipsec-profile-policy001-manual] quit [SwitchB] ipsec transform-set tran2 [SwitchB-ipsec-transform-set-tran2] encapsulation-mode transport [SwitchB-ipsec-transform-set-tran2] esp encryption-algorithm des [SwitchB-ipsec-transform-set-tran2] esp authentication-algorithm sha1 [SwitchB-ipsec-transform-set-tran2] quit [SwitchB] ipsec profile policy002 manual [SwitchB-ipsec-profile-policy002-manual] transform-set tran2 [SwitchB-ipsec-profile-policy002-manual] sa spi outbound esp 54321 [SwitchB-ipsec-profile-policy002-manual] sa spi inbound esp 54321 [SwitchB-ipsec-profile-policy002-manual] sa string-key outbound esp simple gfedcba

[SwitchB-ipsec-profile-policy002-manual] sa string-key inbound esp simple gfedcba [SwitchB-ipsec-profile-policy002-manual] quit \# 配置 Switch C。创建名为 tran2 的安全提议，报文封装形式采用传输模式，安全协议采用ESP 协议。创建手工方式的安全框架 policy002，配置 SPI 和密钥。
[SwitchC] ipsec transform-set tran2 [SwitchC-ipsec-transform-set-tran2] encapsulation-mode transport [SwitchC-ipsec-transform-set-tran2] esp encryption-algorithm des [SwitchC-ipsec-transform-set-tran2] esp authentication-algorithm sha1 [SwitchC-ipsec-transform-set-tran2] quit [SwitchC] ipsec profile policy002 manual [SwitchC-ipsec-profile-policy002-manual] transform-set tran2 [SwitchC-ipsec-profile-policy002-manual] sa spi outbound esp 54321 [SwitchC-ipsec-profile-policy002-manual] sa spi inbound esp 54321 [SwitchC-ipsec-profile-policy002-manual] sa string-key outbound esp simple gfedcba [SwitchC-ipsec-profile-policy002-manual] sa string-key inbound esp simple gfedcba [SwitchC-ipsec-profile-policy002-manual] quit
(5) 配置通过 IPsec 保护 Switch A 和 Switch B 之间的 IPv6 BGP 报文\# 配置 Switch A。
[SwitchA] bgp 65008 [SwitchA-bgp-default] peer 1::2 ipsec-profile policy001 [SwitchA-bgp-default] quit \# 配置 Switch B。
[SwitchB] bgp 65008 [SwitchB-bgp-default] peer 1::1 ipsec-profile policy001 [SwitchB-bgp-default] quit
(6) 配置通过 IPsec 保护 Switch B 和 Switch C 之间的 IPv6 BGP 报文\# 配置 Switch C。
[SwitchC] bgp 65009 [SwitchC-bgp-default] peer ebgp ipsec-profile policy002 [SwitchC-bgp-default] quit \# 配置 Switch B。
[SwitchB] bgp 65008 [SwitchB-bgp-default] peer ebgp ipsec-profile policy002 [SwitchB-bgp-default] quit

###### 4. 验证配置

\# 在 Switch B 上显示 IPv6 BGP 对等体的详细信息。可以看出完成上述配置后 IBGP、EBGP 对等体能够正常建立，且发送和接收的 IPv6 BGP 报文都经过加密。
[SwitchB] display bgp peer ipv6 verbose Peer: 1::1 Local: 2.2.2.2 Type: IBGP link BGP version 4, remote router ID 1.1.1.1 BGP current state: Established, Up for 00h05m54s BGP current event: KATimerExpired BGP last state: OpenConfirm

Port: Local - 24896 Remote - 179 Configured: Active Hold Time: 180 sec Keepalive Time: 60 sec Received : Active Hold Time: 180 sec Negotiated: Active Hold Time: 180 sec Keepalive Time: 60 sec Peer optional capabilities:
Peer support BGP multi-protocol extended Peer support BGP route refresh capability Peer support BGP route AS4 capability Address family IPv6 Unicast: advertised and received InQ updates: 0, OutQ updates: 0 NLRI statistics:
Rcvd: UnReach NLRI 0, Reach NLRI 0 Sent: UnReach NLRI 0, Reach NLRI 3 Message statistics:
Msg type Last rcvd time/ Current rcvd count/ History rcvd count/ Last sent time Current sent count History sent count Open 18:59:15-2013.4.24 1 1 18:59:15-2013.4.24 1 2 Update - 0 0 18:59:16-2013.4.24 1 1 Notification - 0 0 18:59:15-2013.4.24 0 1 Keepalive 18:59:15-2013.4.24 1 1 18:59:15-2013.4.24 1 1 RouteRefresh - 0 0
- 0 0 Total - 2 2
- 3 5 Maximum allowed prefix number: 4294967295 Threshold: 75% Minimum time between advertisements is 15 seconds Optional capabilities:
Multi-protocol extended capability has been enabled Route refresh capability has been enabled Peer preferred value: 0 IPsec profile name: policy001 Routing policy configured:
No routing policy is configured Peer: 3::2 Local: 2.2.2.2 Type: EBGP link BGP version 4, remote router ID 3.3.3.3 BGP current state: Established, Up for 00h05m00s BGP current event: KATimerExpired

BGP last state: OpenConfirm Port: Local - 24897 Remote - 179 Configured: Active Hold Time: 180 sec Keepalive Time: 60 sec Received : Active Hold Time: 180 sec Negotiated: Active Hold Time: 180 sec Keepalive Time: 60 sec Peer optional capabilities:
Peer support BGP multi-protocol extended Peer support BGP route refresh capability Peer support BGP route AS4 capability Address family IPv6 Unicast: advertised and received Received: Total 8 messages, Update messages 1 Sent: Total 8 messages, Update messages 1 Maximum allowed prefix number: 4294967295 Threshold: 75% Minimum time between advertisements is 30 seconds Optional capabilities:
Multi-protocol extended capability has been enabled Route refresh capability has been enabled Peer preferred value: 0 IPsec profile name: policy002 Routing policy configured:
No routing policy is configured

##### 6.9.2 BGP RPKI配置

###### 1. 组网需求

所有路由器运行 协议，Switch 与 服务器建立连接。Switch 与 建立
• BGP A RPKI A Switch B IBGP 连接。
• Switch A 将 BGP RPKI 验证结果发送给 Switch B。
• 配置路由策略，使得 Switch B 对收到的 BGP RPKI 验证结果设置匹配条件，控制路由的接收。

###### 2. 组网图

图6-3 BGP RPKI 配置组网图RPKI server 1::2/64 1::1/64 Vlan-int12 Vlan-int12 2001::1/64 2001::2/64 AS 100 Switch A Switch B

###### 3. 配置步骤

(1) 配置各接口的 IP 地址，在 Router A 和 Router B 上配置 BGP，建立 IBGP 邻居，配置过程略
(2) 配置 Router A 与 RPKI 服务器建立连接
<SwitchA> system-view
[SwitchA] bgp 100
[SwitchA-bgp-default] rpki
[SwitchA-bgp-default-rpki] server tcp 1::2
[RouterA-bgp-default-rpki-server] port 1234
[RouterA-bgp-default-rpki-server] quit
(3) 在 Switch A 上开启 BGP RPKI 验证
[SwitchA-bgp-default-rpki] check-origin-validation
[SwitchA-bgp-default-rpki] quit
(4) 在 Switch A 上配置 BGP RPKI 验证结果参与路由优选
[SwitchA-bgp-default] address-family ipv6
[SwitchA-bgp-default-ipv6] bestroute origin-as-validation
(5) 在 Switch A 上配置向对等体 2001::2 发送 BGP RPKI 验证结果
[SwitchA-bgp-default-ipv6] peer 2001::2 advertise-ext-community
[SwitchA-bgp-default-ipv6] peer 2001::2 advertise origin-as-validation
[SwitchA-bgp-default-ipv6] quit
[SwitchA-bgp-default] quit
(6) 在 Switch B 上对收到的 BGP RPKI 验证结果设置匹配条件，仅接收验证结果为 Valid 的路由
\# 配置路由策略。
<SwitchB> system-view
[SwitchB] route-policy rpki_policy permit node 0
[SwitchB-route-policy-rpki_policy-0] if-match rpki valid
\# 应用路由策略。
<SwitchB> system-view
[SwitchB] bgp 100

[SwitchB-bgp-default] address-family ipv6 [SwitchB-bgp-default-ipv6] peer 2001::1 route-policy rpki_policy import

###### 4. 验证配置

\# 查看 Switch A 与 RPKI 服务器的连接信息，可以看到 Switch A 与 RPKI 服务器已经建立连接。
[SwitchA] display bgp rpki server Server VPN-index Port State Time ROAs(IPv4/IPv6)
1::2 0 1234 Establish 00:04:43 5/5查看从 服务器获取的 信息，可以看到已经获得 信息。
\# RPKI ROA ROA [SwitchA] display bgp rpki table ipv6 Total number of entries: 5 Status codes: S - stale, U - used Network Mask-range Origin-AS Server Status 2001:4860:: 32-32 100 1::2 U 2404:6800:: 32-32 100 1::2 U 2607:F8B0:: 28-28 4294967295 1::2 U 2A03:ACE0:: 40-40 4294967295 1::2 U 2001::1 64-64 200 1::2 U查看 上 验证结果。
\# Switch A BGP RPKI [SwitchA] display bgp routing-table ipv6 2001::1 64 BGP local router ID: 2.2.2.2 Local AS number: 100 Paths: 1 available, 1 best BGP routing table information of 2001::1/64:
Imported route.
Original nexthop: 0.0.0.0 OutLabel : NULL RxPathID : 0x0 TxPathID : 0x0 Org-validation : Valid AS-path : (null)
Origin : incomplete Attribute value : MED 0, pref-val 32768 State : valid, local, best IP precedence : N/A QoS local ID : N/A 2001::1/64 在 ROA 数据库中的 Network 为 2001::1 ， Mask-range 为 64-64 的地址前缀范围内，且AS 和路由的源 AS 号相匹配，因此验证结果为 Valid。
\# 查看 Switch B 上到达目的网络 2001::1 的 BGP IPv6 单播路由的详细信息。
[SwitchB] display bgp routing-table ipv6 2001::1 64

RR-client route.
From : 2001::1 64 (192.168.56.22)
Rely nexthop : 2001::1 Original nexthop: 2001::1 OutLabel : NULL Ext-Community : <Origin Valid State: Valid > RxPathID : 0x0 TxPathID : 0x0 Org-validation : Invalid AS-path : (null)
Origin : incomplete Attribute value : MED 0, localpref 100, pref-val 0 State : valid, internal, best IP precedence : N/A QoS local ID : N/A Traffic index : N/A由于 Switch B 仅允许 BGP RPKI 验证结果为 Valid 的路由信息通过，因此可以看到到达目的网络2001::1 的 BGP IPv6 单播路由的信息。该路由信息中的扩展团体属性包含了 BGP RPKI 验证结果。

##### 1. 功能简介

### 7 提高BGP网络的可靠性

#### 7.1 提高BGP网络的可靠性配置任务简介

提高 BGP 网络的可靠性配置任务如下：
• 配置BGP GR
• 配置BGP NSR
• 配置BGP与BFD联动
• 配置BGP快速重路由

#### 7.2 配置BGP GR

功能简介
1.
BGP GR（Graceful Restart，平滑重启）是一种在主备倒换或 BGP 协议重启时保证转发业务不中断的机制。GR 有两个角色：
Restarter：发生主备倒换或协议重启，且具有 能力的设备。
• GR GR GR Helper：和 GR Restarter 具有邻居关系，协助完成 GR 流程的设备。GR Helper 也具有
•GR 能力。
设备既可以作为 Restarter，又可以作为 Helper。设备的角色由该设备在 过程中GR GR BGP GR的作用决定。
BGP GR 的工作过程为：
(1) GR Restarter 和 GR Helper 通过 Open 消息交互 GR 能力。只有双方都具有 GR 能力时，建立起的 BGP 会话才具备 GR 能力。GR Restarter 还会通过 Open 消息，将本端通过graceful-restart timer restart 命令配置的对端等待重建 BGP 会话时间通告给 GR Helper。
建立具备 能力的 会话后，GR 进行主备倒换或 协议重启时，GR
(2) GR BGP Restarter BGP Restarter 不会删除 RIB（Routing Information Base，路由信息库）和 FIB（Forwarding Information Base，转发信息库）表项，仍然按照原有的转发表项转发报文，并启动 RIB 路由老化定时器（定时器的值由 graceful-restart timer purge-time 命令配置）。
GR Helper 发现 GR Restarter 进行主备倒换或 BGP 协议重启后，GR Helper 不会删除从该 GR Restarter 学习到的路由，而是将这些路由标记为失效路由，仍按照这些路由转发报文，从而确保在 GR Restarter 进行主备倒换或 BGP 协议重启的过程中，报文转发不会中断。
(3) GR Restarter 主备倒换或 BGP 协议重启完成后，它会重新与 GR Helper 建立 BGP 会话。如果在 通告的 会话重建时间内没有成功建立 会话，则 会删GR Restarter BGP BGP GR Helper除标记为失效的路由。
(4) 如果在 GR Restarter 通告的 BGP 会话重建时间内成功建立 BGP 会话，则 GR Restarter 和GR Helper 在建立的 BGP 会话上进行路由信息交互，以便 GR Restarter 恢复路由信息、GR Helper 根据学习到的路由删除路由的失效标记。
(5) BGP 会话建立后，在 GR Restarter 和 GR Helper 上都会启动 End-Of-RIB（路由信息库结束）
标记等待定时器（定时器的值通过 命令配置），graceful-restart timer wait-for-rib

##### 1. 功能简介

该定时器用来控制路由信息收敛的速度。如果定时器超时时没有完成路由信息的交互，则不再接收新的路由，根据已经学习到的 路由信息更新 表项，删除老化GR Restarter BGP RIB的 RIB 表项；GR Helper 则删除标记为失效的路由。
• 如果在 RIB 路由老化定时器超时时没有完成路由信息的交互，则 GR Restarter 会强制退出GR 过程，根据已经学习到的 BGP 路由信息更新 RIB 表项，删除老化的 RIB 表项。

##### 2. 配置限制和指导

End-Of-RIB 标记用来标识路由更新发送的结束。
本端配置的等待 End-Of-RIB 标记的时间不会通告给对端，只用来控制本端路由信息交互的时间，即 上配置的时间只用来控制 从 接收路由更新的时间，GR GR Restarter GR Restarter GR Helper Helper 上配置的时间只用来控制 GR Helper 从 GR Restarter 接收路由更新的时间。当路由信息的数量较多时，建议将本端等待 End-Of-RIB 标记的时间调大，以保证完成所有路由信息的交互。
由于设备在 GR 过程中的角色不可预知，建议在作为 GR Restarter 和 GR Helper 的设备上均进行本配置。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
进入 实例视图。
(2) BGP
bgp as-number [ instance instance-name ]
使能 协议的 能力。
(3) BGP GR
graceful-restart
缺省情况下，BGP 协议的 GR 能力处于关闭状态。
(4) 配置对端等待重建 BGP 会话的时间。
graceful-restart timer restart timer
缺省情况下，对端等待重建 BGP 会话的时间为 150 秒。
对端等待重建 BGP 会话的时间应小于 Open 消息中的 Holdtime 时间。
(5) 配置本端等待 End-Of-RIB 标记的时间。
graceful-restart timer wait-for-rib timer
缺省情况下，本端等待 End-Of-RIB 标记的时间为 600 秒。
(6) 配置 BGP GR 过程中等待通知 RIB 老化失效表项的时间。
graceful-restart timer purge-time timer
缺省情况下，BGP GR 过程中等待通知 RIB 老化失效表项的时间为 480 秒。

#### 7.3 配置BGP NSR

功能简介
1.
BGP NSR （ Nonstop Routing ，不间断路由）是一种通过在 BGP 协议主备进程之间备份必要的协议状态和数据（如 邻居信息和路由信息），使得 协议的主进程中断时，备份进程能够无BGP BGP缝地接管主进程的工作，从而确保对等体感知不到 BGP 协议中断，保持 BGP 路由，并保证转发不会中断的技术。

导致 BGP 主进程中断的事件包括以下几种：
BGP 主进程重启
•BGP 主进程所在的主控板发生故障
•
• BGP 主进程所在的主控板进行 ISSU（In-Service Software Upgrade，不中断业务升级）
BGP NSR 与 BGP GR 具有如下区别，请根据实际情况选择合适的方式确保数据转发不中断：
• 对设备要求不同：BGP 协议的主进程和备进程运行在不同的 IRF 成员设备上，因此要运行 BGP NSR 功能或 BGP GR 功能，必须进行 IRF 堆叠且 IRF 必须有两个或两个以上的成员设备。要运行 BGP GR 功能，可以不进行 IRF 堆叠或 IRF 可以只有一个成员设备。
对 对等体的要求不同：使用 功能时，BGP 对等体不会感知本地设备发生了
• BGP BGP NSR BGP 进程的异常重启或主备倒换等故障，不需要 BGP 对等体协助恢复 BGP 路由信息。BGP GR 要求 BGP 对等体具有 GR 能力，并且在 BGP 会话中断恢复时，BGP 对等体能够作为 GR协助本地设备恢复 路由信息。
helper BGP

##### 2. 配置限制和指导

如果在设备上同时配置了 BGP NSR 和 BGP GR 功能，则二者的关系如下：
• BGP NSR 优先级高于 BGP GR，即 BGP 主进程中断时通过 BGP NSR 确保转发不中断，设备不会作为 GR Restarter 启动 GR 过程。
• GR Helper 协助 GR Restarter 恢复重启前状态时，如果 GR Helper 发生了主备进程倒换，则即便 GR Helper 上配置了 BGP NSR，也无法保证 GR 过程成功。

##### 3. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
(3) 使能 BGP NSR 功能。
non-stop-routing缺省情况下，BGP NSR 功能处于关闭状态。

#### 7.4 配置BGP与BFD联动

##### 1. 功能简介

协议通过存活时间（Keepalive）定时器和保持时间（Holdtime）定时器来维护邻居关系。但BGP这些定时器都是秒级的，而且根据协议规定，设置的保持时间应该至少为存活时间间隔的三倍。这样使得 BGP 邻居关系的检测比较慢，对于报文收发速度快的接口会导致大量报文丢失。通过配置BGP 与 BFD 联动，可以使用 BFD 来检测本地路由器和 BGP 对等体之间的链路。当本地路由器和对等体之间的链路出现故障时，BFD 可以快速检测到该故障，从而加快 协议的收敛速度。
BGP BGP有关 BFD 的介绍和详细配置，请参见“可靠性配置指导”中的“BFD”。
配置通过 BFD 检测本地路由器和指定 BGP 对等体/对等体组之间的链路之前，需要先在本地路由器和指定 BGP 对等体/对等体组之间建立 BGP 会话。

##### 2. 配置限制和指导

配置 BGP GR 功能后，请慎用 BGP 与 BFD 联动功能。因为当链路故障时，系统可能还没来得及启用 GR 处理流程，BFD 已经检测到链路故障了，从而导致 GR 失败。如果设备上同时配置了 BGP GR和 BFD，则在 期间请勿去使能 BFD，否则可能导致 失败。
BGP BGP GR BGP GR

##### 3. 配置步骤（IPv4单播/IPv4组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 实例视图。
BGP
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 实例视图。
BGP-VPN
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
(3) 配置通过 BFD 检测本地路由器和指定 BGP 对等体/对等体组之间的链路。
peer { group-name | ipv4-address [ mask-length ] } bfd [ multi-hop |
single-hop ]
缺省情况下，不使用 检测本地路由器和 对等体/对等体组之间的链路。
BFD BGP

##### 4. 配置步骤（IPv6单播/IPv6组播）

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 实例视图。
BGP
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 实例视图。
BGP-VPN
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
(3) 配置通过 BFD 检测本地路由器和指定 IPv6 BGP 对等体/对等体组之间的链路。
peer { group-name | ipv6-address [ prefix-length ] } bfd [ multi-hop |
single-hop ]
缺省情况下，不使用 检测本地路由器和 对等体/对等体组之间的链路。
BFD IPv6 BGP

#### 7.5 配置BGP快速重路由

##### 7.5.1 功能简介

当 网络中的链路或某台路由器发生故障时，需要通过故障链路或故障路由器传输才能到达目BGP的地的报文将会丢失或产生路由环路，数据流量将会被中断。直到 BGP 根据新的网络拓扑路由收敛后，被中断的流量才能恢复正常的传输。
为了尽可能缩短网络故障导致的流量中断时间，网络管理员可以开启 BGP 快速重路由功能。

图7-1 BGP 快速重路由功能示意图Backup nexthop: Router C Router A Router B Nexthop: Router D Router E如 图 所示，在Router B上开启快速重路由功能后，BGP将为主路由生成备份下一跳。IPv4 组7-1网中BGP通过ARP或Echo方式的BFD会话检测主路由的下一跳是否可达，IPv6 组网中BGP通过ND（Neighbor Discovery，邻居发现）协议检测主路由的下一跳是否可达。当Router B检测到主路由的下一跳不可达后，BGP会使用备份下一跳替换失效下一跳，通过备份下一跳来指导报文的转发，从而大大缩短了流量中断时间。在使用备份下一跳指导报文转发的同时，BGP会重新进行路由优选，优选完毕后，使用新的最优路由来指导报文转发。
开启 BGP 快速重路由功能的方法有如下两种：
• 在 BGP 地址族视图下执行 pic 命令开启当前地址族的 BGP 快速重路由功能。采用这种方法时，BGP 会为当前地址族的所有 BGP 路由自动计算备份下一跳，即只要从不同 BGP 对等体学习到了到达同一目的网络的路由，且这些路由不等价，就会生成主备两条路由。
在 BGP 地址族视图下执行 fast-reroute route-policy 命令指定快速重路由引用的路
•由策略，并在引用的路由策略中，通过 apply [ ipv6 ] fast-reroute backup-nexthop 命令指定备份下一跳的地址。采用这种方式时，只有为主路由计算出的备份下一跳地址与指定的地址相同时，才会为其生成备份下一跳；否则，不会为主路由生成备份下一跳。在引用的路由策略中，还可以配置 子句，用来决定哪些路由可以进if-match行快速重路由保护，BGP 只会为通过 if-match 子句过滤的路由生成备份下一跳。
引用路由策略方式的优先级高于通过 pic 命令开启 BGP 快速重路由方式。
IPv4 单播路由和 IPv6 单播路由支持 BGP 快速重路由功能；IPv4 组播路由和 IPv6 组播路由不支持BGP 快速重路由功能。

##### 7.5.2 通过引用路由策略的方式开启BGP快速重路由功能（IPv4单播）

进入系统视图。
(1)
system-view
(2) 配置 echo 报文的源 IP 地址。
bfd echo-source-ip ipv4-address缺省情况下，未配置 echo 报文的源 IP 地址。
通过 Echo 方式的 BFD 会话检测主路由的下一跳是否可达时，必须执行本配置。
echo 报文的源 IP 地址用户可以任意指定。建议配置 echo 报文的源 IP 地址不属于该设备任何一个接口所在网段。
本命令的详细介绍，请参见“可靠性命令参考”中的“BFD”。
(3) 创建路由策略，并进入路由策略视图。

route-policy route-policy-name permit node node-number本命令的详细介绍，请参见“三层技术-IP 路由命令参考”中的“路由策略”。
(4) 配置快速重路由的备份下一跳地址。
apply fast-reroute backup-nexthop ipv4-address缺省情况下，未指定快速重路由的备份下一跳地址。
本命令的详细介绍，请参见“三层技术-IP 路由命令参考”中的“路由策略”。
(5) 退回系统视图。
quit
(6) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
(7) （可选）配置通过 Echo 方式的 BFD 会话检测主路由的下一跳是否可达。
primary-path-detect bfd echo缺省情况下，通过 ARP 检测主路由的下一跳是否可达。
(8) 进入 BGP IPv4 单播地址族视图或 BGP-VPN IPv4 单播地址族视图。
进入 BGP IPv4 单播地址族视图(cid:123)
address-family ipv4 [ unicast ]进入 单播地址族视图BGP-VPN IPv4 (cid:123)
ip vpn-instance vpn-instance-name address-family ipv4 [ unicast ]在当前地址族视图下指定 快速重路由引用的路由策略。
(9) BGP fast-reroute route-policy route-policy-name缺省情况下，BGP 快速重路由未引用任何路由策略。
引用的路由策略中，只有 apply fast-reroute backup-nexthop 和 apply ipv6命令生效，其他 子句不会生效。
fast-reroute backup-nexthop apply

##### 7.5.3 通过引用路由策略的方式开启BGP快速重路由功能（IPv6单播）

(1) 进入系统视图。
system-view
(2) 创建路由策略，并进入路由策略视图。
route-policy route-policy-name permit node node-number
本命令的详细介绍，请参见“三层技术-IP 路由命令参考”中的“路由策略”。
(3) 配置快速重路由的备份下一跳地址。
apply ipv6 fast-reroute backup-nexthop ipv6-address
缺省情况下，未指定快速重路由的备份下一跳地址。
本命令的详细介绍，请参见“三层技术 路由命令参考”中的“路由策略”。
-IP
退回系统视图。
(4)
quit
进入 实例视图或 实例视图。
(5) BGP BGP-VPN

进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(6) 进入 BGP IPv6 单播地址族视图或 BGP-VPN IPv6 单播地址族视图。
address-family ipv6 [ unicast ]
(7) 在当前地址族视图下指定 BGP 快速重路由引用的路由策略。
fast-reroute route-policy route-policy-name缺省情况下，BGP 快速重路由未引用任何路由策略。
引用的路由策略中，只有 apply fast-reroute backup-nexthop 和 apply ipv6 fast-reroute backup-nexthop 命令生效，其他 apply 子句不会生效。

##### 7.5.4 通过pic命令开启BGP快速重路由（IPv4单播）

###### 1. 配置限制和指导

在某些组网情况下，执行 pic 命令为所有 BGP 路由生成备份下一跳后，可能会导致路由环路，请谨慎使用本功能。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 实例视图。
BGP
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 实例视图。
BGP-VPN
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
(3) 进入 BGP IPv4 单播地址族视图或 BGP-VPN IPv4 单播地址族视图。
address-family ipv4 [ unicast ]
(4) 开启 BGP 快速重路由功能。
pic
缺省情况下，BGP 快速重路由功能处于关闭状态。

##### 7.5.5 通过pic命令开启BGP快速重路由（IPv6单播）

###### 1. 配置限制和指导

在某些组网情况下，执行 pic 命令为所有 BGP 路由生成备份下一跳后，可能会导致路由环路，请谨慎使用本功能。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]
ip vpn-instance vpn-instance-name
进入 单播地址族视图或 单播地址族视图。
(3) BGP IPv6 BGP-VPN IPv6
address-family ipv6 [ unicast ]
开启 快速重路由功能。
(4) BGP
pic
缺省情况下，BGP 快速重路由功能处于关闭状态.
在某些组网情况下，执行 pic 命令为所有 BGP路由生成备份下一跳后，可能会导致路由环路，
请谨慎使用本命令。

#### 7.6 提高BGP网络的可靠性显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 BGP 的运行情况，通过查看显示信息验证配置的效果。

##### 1. 提高BGP网络的可靠性配置显示（IPv4单播）

表7-1 提高 BGP 网络的可靠性配置显示（IPv4 单播）
操作 命令display bgp [ instance instance-name ]显示BGP NSR的运行状态non-stop-routing status

##### 2. 提高BGP网络的可靠性配置显示（IPv6单播）

表7-2 提高 BGP 网络的可靠性配置显示（IPv6 单播）
操作 命令display bgp [ instance instance-name ]显示BGP NSR的运行状态non-stop-routing status

##### 3. 提高BGP网络的可靠性配置显示（IPv4组播）

表 7-3 提高 BGP 网络的可靠性配置显示（ IPv4 组播）
操作 命令display bgp [ instance instance-name ]显示BGP NSR的运行状态non-stop-routing status

##### 4. 提高BGP网络的可靠性配置显示（IPv6组播）

表7-4 提高 网络的可靠性配置显示（IPv6 组播）
BGP操作 命令display bgp instance [ instance-name ]显示BGP NSR的运行状态non-stop-routing status

#### 7.7 提高IPv4 BGP网络的可靠性典型配置举例

##### 7.7.1 BGP GR配置

###### 1. 组网需求

如 图 7-2 所示，所有交换机均运行BGP协议，Switch A和Switch B之间建立EBGP连接，Switch B和Switch C之间建立IBGP连接。现要求实现即便Switch B发生主备倒换，也不会影响Switch A和C之间正在进行的数据传输。
Switch

###### 2. 组网图

图7-2 BGP GR 配置组网图

###### 3. 配置步骤

(1) Switch A 的配置
\# 配置各接口的 IP 地址（略）。
\# 配置 Switch A 与 Switch B 的 EBGP 连接。
<SwitchA> system-view
[SwitchA] bgp 65008
[SwitchA-bgp-default] router-id 1.1.1.1
[SwitchA-bgp-default] peer 200.1.1.1 as-number 65009
使能 功能。
\# BGP GR
[SwitchA-bgp-default] graceful-restart
\# 将 8.0.0.0/8 网段路由通告到 BGP 路由表中。
[SwitchA-bgp-default] address-family ipv4
[SwitchA-bgp-default-ipv4] network 8.0.0.0
\# 使能与 Switch B 交换 BGP IPv4 单播路由的能力。
[SwitchA-bgp-default-ipv4] peer 200.1.1.1 enable
(2) Switch B 的配置

\# 配置各接口的 IP 地址（略）。
\# 配置 Switch B 与 Switch A 的 EBGP 连接。
<SwitchB> system-view [SwitchB] bgp 65009 [SwitchB-bgp-default] router-id 2.2.2.2 [SwitchB-bgp-default] peer 200.1.1.2 as-number 65008 \# 配置 Switch B 与 Switch C 的 IBGP 连接。
[SwitchB-bgp-default] peer 9.1.1.2 as-number 65009使能 功能。
\# BGP GR [SwitchB-bgp-default] graceful-restart \# 将 200.1.1.0/24 和 9.1.1.0/24 网段路由通告到 BGP 路由表中。
[SwitchB-bgp-default] address-family ipv4 [SwitchB-bgp-default-ipv4] network 200.1.1.0 24 [SwitchB-bgp-default-ipv4] network 9.1.1.0 24 \# 使能与 Switch A、Switch C 交换 BGP IPv4 单播路由的能力。
[SwitchB-bgp-default-ipv4] peer 200.1.1.2 enable [SwitchB-bgp-default-ipv4] peer 9.1.1.2 enable
(3) Switch C 的配置\# 配置各接口的 IP 地址（略）。
\# 配置 Switch C 与 Switch B 的 IBGP 连接。
<SwitchC> system-view [SwitchC] bgp 65009 [SwitchC-bgp-default] router-id 3.3.3.3 [SwitchC-bgp-default] peer 9.1.1.1 as-number 65009 \# 使能 BGP GR 功能。
[SwitchC-bgp-default] graceful-restart使能与 交换 单播路由的能力。
\# Switch B BGP IPv4 [SwitchC-bgp-default-ipv4] peer 9.1.1.1 enable

###### 4. 验证配置

在 上 C，同时在 上触发主备倒换，可以发现在整个倒换过程中Switch A ping Switch Switch B Switch A 都可以 ping 通 Switch C。

##### 7.7.2 BGP与BFD联动配置

###### 1. 组网需求

• 在 AS 200 内使用 OSPF 作为 IGP 协议，实现 AS 内的互通。
• Switch A 与 Switch C 之间建立两条 IBGP 连接。当 Switch A 与 Switch C 之间的两条路径均
连通时，Switch C 与 1.1.1.0/24 之间的报文使用 Switch A<－>Switch B<－>Switch C 这条路
径转发；当 Switch A<－>Switch B<－>Switch C 这条路径发生故障时，BFD 能够快速检测并
通告 协议，使得 － － 这条路径能够迅速生效。
BGP Switch A< >Switch D< >Switch C

###### 2. 组网图

图7-3 配置 BGP 与 BFD 联动组网图

| 接口 | IP地址 | 设备 | 接口 |
|---|---|---|---|
| Vlan-int100 | 3.0.1.1/24 | Switch C | Vlan-int101 |
| Vlan-int200 | 2.0.1.1/24 |  | Vlan-int201 |
| Vlan-int100 | 3.0.1.2/24 | Switch D | Vlan-int200 |
| Vlan-int101 | 3.0.2.1/24 |  | Vlan-int201 |

设备 IP地址Switch A 3.0.2.2/24
2.0.2.2/24 Switch B 2.0.1.2/24
2.0.2.1/24

###### 3. 配置步骤

配置各接口的 地址（略）
(1) IP
(2) 配置 OSPF，保证 Switch A 和 Switch C 之间路由可达（略）
(3) Switch A 上的 BGP 配置\# 配置 Switch A 和 Switch C 建立两条 IBGP 连接。
<SwitchA> system-view [SwitchA] bgp 200 [SwitchA-bgp-default] peer 3.0.2.2 as-number 200 [SwitchA-bgp-default] peer 2.0.2.2 as-number 200 [SwitchA-bgp-default] address-family ipv4 unicast [SwitchA-bgp-default-ipv4] peer 3.0.2.2 enable [SwitchA-bgp-default-ipv4] peer 2.0.2.2 enable [SwitchA-bgp-default-ipv4] quit [SwitchA-bgp-default] quit \# 配置当 Switch A 与 Switch C 之间的两条路径均连通时，Switch C 与 1.1.1.0/24 之间的报文使用 － － 这条路径转发。（在 上对发布给对等体Switch A< >Switch B< >Switch C Switch A
2.0.2.2 的 1.1.1.0/24 路由配置较高的 MED 属性值）
定义编号为 2000 的 IPv4 基本 ACL，允许路由 1.1.1.0/24 通过。
(cid:123)
[SwitchA] acl basic 2000

###### 4. 验证配置

[SwitchA-acl-ipv4-basic-2000] rule permit source 1.1.1.0 0.0.0.255 [SwitchA-acl-ipv4-basic-2000] quit定义两个 Route-policy，一个名为 apply_med_50，为路由 1.1.1.0/24 设置 MED 属性值为(cid:123)
50；另一个名为 apply_med_100，为路由 1.1.1.0/24 设置 MED 属性值为 100。
[SwitchA] route-policy apply_med_50 permit node 10 [SwitchA-route-policy-apply_med_50-10] if-match ip address acl 2000 [SwitchA-route-policy-apply_med_50-10] apply cost 50 [SwitchA-route-policy-apply_med_50-10] quit [SwitchA] route-policy apply_med_100 permit node 10 [SwitchA-route-policy-apply_med_100-10] if-match ip address acl 2000 [SwitchA-route-policy-apply_med_100-10] apply cost 100 [SwitchA-route-policy-apply_med_100-10] quit对发布给对等体 3.0.2.2 的路由应用名为 apply_med_50 的 Route-policy，对发布给对等体(cid:123)
的路由应用名为 的 Route-policy。
2.0.2.2 apply_med_100 [SwitchA] bgp 200 [SwitchA-bgp-default] address-family ipv4 unicast [SwitchA-bgp-default-ipv4] peer 3.0.2.2 route-policy apply_med_50 export [SwitchA-bgp-default-ipv4] peer 2.0.2.2 route-policy apply_med_100 export [SwitchA-bgp-default-ipv4] quit \# 配置当 Switch A<－>Switch B<－>Switch C 这条路径发生故障时，BFD 能够快速检测并通告 BGP 协议，使得 Switch A<－>Switch D<－>Switch C 这条路径能够迅速生效。
[SwitchA-bgp-default] peer 3.0.2.2 bfd [SwitchA-bgp-default] quit
(4) Switch C 上的 BGP 配置。
\# 配置 Switch A 和 Switch C 建立两条 IBGP 连接。
<SwitchC> system-view [SwitchC] bgp 200 [SwitchC-bgp-default] peer 3.0.1.1 as-number 200 [SwitchC-bgp-default] peer 2.0.1.1 as-number 200 [SwitchC-bgp-default] address-family ipv4 unicast [SwitchC-bgp-default-ipv4] peer 3.0.1.1 enable [SwitchC-bgp-default-ipv4] peer 2.0.1.1 enable [SwitchC-bgp-default-ipv4] quit配置当 A<－>Switch B<－>Switch 这条路径发生故障时，BFD 能够快速检测并通\# Switch C告 BGP 协议，使得 Switch A<－>Switch D<－>Switch C 这条路径能够迅速生效。
[SwitchC-bgp-default] peer 3.0.1.1 bfd [SwitchC-bgp-default] quit [SwitchC] quit验证配置
4.
下面以 Switch C 为例，Switch A 和 Switch C 类似，不再赘述。
\# 显示 Switch C 的 BFD 信息。
<SwitchC> display bfd session verbose Total Session Num: 1 Up Session Num: 1 Init Mode: Active IPv4 Session Working Under Ctrl Mode:

Local Discr: 513 Remote Discr: 513 Source IP: 3.0.2.2 Destination IP: 3.0.1.1 Session State: Up Interface: N/A Min Tx Inter: 500ms Act Tx Inter: 500ms Min Rx Inter: 500ms Detect Inter: 2500ms Rx Count: 135 Tx Count: 135 Connect Type: Indirect Running Up for: 00:00:58 Hold Time: 2457ms Auth mode: None Detect Mode: Async Slot: 0 Protocol: BGP Version:1 Diag Info: No Diagnostic以上显示信息表明：Switch A 和 Switch C 之间已经建立了 BFD 连接，而且 BFD 协议运行正常。
\# 在 Switch C 上查看 BGP 邻居信息，可以看出 Switch A 和 Switch C 之间建立两条 BGP 连接，且均处于 状态。
Established <SwitchC> display bgp peer ipv4 BGP local router ID: 3.3.3.3 Local AS number: 200 Total number of peers: 2 Peers in established state: 2
* - Dynamically created peer Peer AS MsgRcvd MsgSent OutQ PrefRcv Up/Down State
2.0.1.1 200 4 5 0 0 00:01:55 Established
3.0.1.1 200 4 5 0 0 00:01:52 Established \# 在 Switch C 上查看 1.1.1.0/24 的路由信息，可以看出 Switch C 通过 Switch A<－>Switch B<－>Switch C 这条路径与 1.1.1.0/24 网段通信。
<SwitchC> display ip routing-table 1.1.1.0 24 verbose Summary count : 1 Destination: 1.1.1.0/24 Protocol: BGP Process ID: 0 SubProtID: 0x1 Age: 00h00m09s Cost: 50 Preference: 255 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x1 OrigVrf: default-vrf TableID: 0x2 OrigAs: 0 NibID: 0x15000001 LastAs: 0 AttrID: 0x1 Neighbor: 3.0.1.1 Flags: 0x10060 OrigNextHop: 3.0.1.1 Label: NULL RealNextHop: 3.0.2.1 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: Vlan-interface101 BkTunnel ID: Invalid BkInterface: N/A

###### 1. 组网需求

FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0 \# Switch A 和 Switch B 之间的链路发生故障后，在 Switch C 上查看 1.1.1.0/24 的路由信息，可以看出 Switch C 通过 Switch A<－>Switch D<－>Switch C 这条路径与 1.1.1.0/24 网段通信。
<SwitchC> display ip routing-table 1.1.1.0 24 verbose Summary count : 1 Destination: 1.1.1.0/24 Protocol: BGP Process ID: 0 SubProtID: 0x1 Age: 00h03m08s Cost: 100 Preference: 255 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x1 OrigVrf: default-vrf TableID: 0x2 OrigAs: 0 NibID: 0x15000000 LastAs: 0 AttrID: 0x0 Neighbor: 2.0.1.1 Flags: 0x10060 OrigNextHop: 2.0.1.1 Label: NULL RealNextHop: 2.0.2.1 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: Vlan-interface201 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0

##### 7.7.3 BGP快速重路由配置

组网需求
1.
如 图 7-4 所示，Switch A、Switch B、Switch C和Switch D通过BGP协议实现网络互连。要求链路B正常时，Switch A和Switch D之间的流量通过链路B转发；链路B出现故障时，流量可以快速切换到链路A上。

###### 3. 配置步骤

###### 2. 组网图

图7-4 配置 BGP 快速重路由组网图Loop0
2.2.2.2/32 Vlan-int 100 Vlan-int 101 AS 200
10.1.1.2/24 20.1.1.2/24 Switch B Vlan-int 100 Vlan-int 101
10.1.1.1/24 20.1.1.4/24 Switch A Link B Switch D 23 4 0pooL . 4 Loop0 /
1 . 4 .
1 . 4 .
1 / 32 .
AS 100 Vlan-int 200 Link A Vlan-int 201
30.1.1.1/24
40.1.1.4/24 Switch C Vlan-int 200 Vlan-int 201
30.1.1.3/24 40.1.1.3/24 Loop0
3.3.3.3/32配置步骤
3.
(1) 配置各接口的 IP 地址（略）
(2) 在 AS 200 内配置 OSPF，发布接口地址所在网段的路由（包括 Loopback 接口），确保 Switch
B、Switch 和 之间路由可达（略）
C Switch D
(3) 配置 BGP 连接\# 配置 Switch A 分别与 Switch B 和 Switch C 建立 EBGP 会话，并配置通过 BGP 发布路由
1.1.1.1/32。
<SwitchA> system-view [SwitchA] bgp 100 [SwitchA-bgp-default] router-id 1.1.1.1 [SwitchA-bgp-default] peer 10.1.1.2 as-number 200 [SwitchA-bgp-default] peer 30.1.1.3 as-number 200 [SwitchA-bgp-default] address-family ipv4 unicast [SwitchA-bgp-default-ipv4] peer 10.1.1.2 enable [SwitchA-bgp-default-ipv4] peer 30.1.1.3 enable [SwitchA-bgp-default-ipv4] network 1.1.1.1 32配置 与 建立 会话，与 建立 会话。
\# Switch B Switch A EBGP Switch D IBGP <SwitchB> system-view [SwitchB] bgp 200 [SwitchB-bgp-default] router-id 2.2.2.2 [SwitchB-bgp-default] peer 10.1.1.1 as-number 100 [SwitchB-bgp-default] peer 4.4.4.4 as-number 200 [SwitchB-bgp-default] peer 4.4.4.4 connect-interface loopback 0 [SwitchB-bgp-default] address-family ipv4 unicast [SwitchB-bgp-default-ipv4] peer 10.1.1.1 enable [SwitchB-bgp-default-ipv4] peer 4.4.4.4 enable [SwitchB-bgp-default-ipv4] peer 4.4.4.4 next-hop-local

[SwitchB-bgp-default-ipv4] quit [SwitchB-bgp-default] quit \# 配置 Switch C 与 Switch A 建立 EBGP 会话，与 Switch D 建立 IBGP 会话。
<SwitchC> system-view [SwitchC] bgp 200 [SwitchC-bgp-default] router-id 3.3.3.3 [SwitchC-bgp-default] peer 30.1.1.1 as-number 100 [SwitchC-bgp-default] peer 4.4.4.4 as-number 200 [SwitchC-bgp-default] peer 4.4.4.4 connect-interface loopback 0 [SwitchC-bgp-default] address-family ipv4 unicast [SwitchC-bgp-default-ipv4] peer 30.1.1.1 enable [SwitchC-bgp-default-ipv4] peer 4.4.4.4 enable [SwitchC-bgp-default-ipv4] peer 4.4.4.4 next-hop-local [SwitchC-bgp-default-ipv4] quit [SwitchC-bgp-default] quit配置 分别与 和 建立 会话，并配置 发布路由\# Switch D Switch B Switch C IBGP BGP
4.4.4.4/32 。
<SwitchD> system-view [SwitchD] bgp 200 [SwitchD-bgp-default] router-id 4.4.4.4 [SwitchD-bgp-default] peer 2.2.2.2 as-number 200 [SwitchD-bgp-default] peer 2.2.2.2 connect-interface loopback 0 [SwitchD-bgp-default] peer 3.3.3.3 as-number 200 [SwitchD-bgp-default] peer 3.3.3.3 connect-interface loopback 0 [SwitchD-bgp-default] address-family ipv4 unicast [SwitchD-bgp-default-ipv4] peer 2.2.2.2 enable [SwitchD-bgp-default-ipv4] peer 3.3.3.3 enable [SwitchD-bgp-default-ipv4] network 4.4.4.4 32
(4) 修改路由的首选值，使得 Switch A 和 Switch D 之间的流量优先通过链路 B 转发\# 在 Switch A 上配置从 Switch B 接收到的路由的首选值为 100。
[SwitchA-bgp-default-ipv4] peer 10.1.1.2 preferred-value 100 [SwitchA-bgp-default-ipv4] quit [SwitchA-bgp-default] quit \# 在 Switch D 上配置从 Switch B 接收到的路由的首选值为 100 。
[SwitchD-bgp-default-ipv4] peer 2.2.2.2 preferred-value 100 [SwitchD-bgp-default-ipv4] quit [SwitchD-bgp-default] quit
(5) 配置 BGP 快速重路由\# 配置 Switch A：配置通过 Echo 方式的 BFD 会话检测主路由的下一跳是否可达，并配置 BFD echo 报文的源 IP 地址为 11.1.1.1；创建路由策略 frr，为路由 4.4.4.4/32 指定备份下一跳的地址为 30.1.1.3（对等体 的地址）；在 单播地址族下应用该路由策略。
Switch C BGP IPv4 [SwitchA] bfd echo-source-ip 11.1.1.1 [SwitchA] ip prefix-list abc index 10 permit 4.4.4.4 32 [SwitchA] route-policy frr permit node 10 [SwitchA-route-policy] if-match ip address prefix-list abc [SwitchA-route-policy] apply fast-reroute backup-nexthop 30.1.1.3

[SwitchA-route-policy] quit [SwitchA] bgp 100 [SwitchA-bgp-default] primary-path-detect bfd echo [SwitchA-bgp-default] address-family ipv4 unicast [SwitchA-bgp-default-ipv4] fast-reroute route-policy frr [SwitchA-bgp-default-ipv4] quit [SwitchA-bgp-default] quit \# 配置 Switch D：配置通过 Echo 方式的 BFD 会话检测主路由的下一跳是否可达，并配置 BFD echo 报文的源 IP 地址为 44.1.1.1；创建路由策略 frr，为路由 1.1.1.1/32 指定备份下一跳的地址为 3.3.3.3（对等体 的地址）；在 单播地址族下应用该路由策略。
Switch C BGP IPv4 [SwitchD] bfd echo-source-ip 44.1.1.1 [SwitchD] ip prefix-list abc index 10 permit 1.1.1.1 32 [SwitchD] route-policy frr permit node 10 [SwitchD-route-policy] if-match ip address prefix-list abc [SwitchD-route-policy] apply fast-reroute backup-nexthop 3.3.3.3 [SwitchD-route-policy] quit [SwitchD] bgp 200 [SwitchD-bgp-default] primary-path-detect bfd echo [SwitchD-bgp-default] address-family ipv4 unicast [SwitchD-bgp-default-ipv4] fast-reroute route-policy frr [SwitchD-bgp-default-ipv4] quit [SwitchD-bgp-default] quit

###### 4. 验证配置

\# 在 Switch A 上查看 4.4.4.4/32 路由，可以看到备份下一跳信息。
[SwitchA] display ip routing-table 4.4.4.4 32 verbose Summary count : 1 Destination: 4.4.4.4/32 Protocol: BGP Process ID: 0 SubProtID: 0x2 Age: 00h01m52s Cost: 0 Preference: 255 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0x2 OrigAs: 200 NibID: 0x15000003 LastAs: 200 AttrID: 0x5 Neighbor: 10.1.1.2 Flags: 0x10060 OrigNextHop: 10.1.1.2 Label: NULL RealNextHop: 10.1.1.2 BkLabel: NULL BkNextHop: 30.1.1.3 Tunnel ID: Invalid Interface: Vlan-interface 100 BkTunnel ID: Invalid BkInterface: Vlan-interface 200 FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0 \# 在 Switch D 上查看 1.1.1.1/32 路由，可以看到备份下一跳信息。
[SwitchD] display ip routing-table 1.1.1.1 32 verbose

Summary count : 1 Destination: 1.1.1.1/32 Protocol: BGP Process ID: 0 SubProtID: 0x1 Age: 00h00m36s Cost: 0 Preference: 255 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0x2 OrigAs: 100 NibID: 0x15000003 LastAs: 100 AttrID: 0x1 Neighbor: 2.2.2.2 Flags: 0x10060 OrigNextHop: 2.2.2.2 Label: NULL RealNextHop: 20.1.1.2 BkLabel: NULL BkNextHop: 40.1.1.3 Tunnel ID: Invalid Interface: Vlan-interface 101 BkTunnel ID: Invalid BkInterface: Vlan-interface 201 FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0

#### 7.8 提高IPv6 BGP网络的可靠性典型配置举例

##### 7.8.1 IPv6 BGP与BFD联动配置

###### 1. 组网需求

在 AS 200 内使用 OSPFv3 作为 IGP 协议，实现 AS 内的互通。
•Switch A 与 Switch C 之间建立两条 IBGP 连接。当 Switch A 与 Switch C 之间的两条路径均
•连通时，Switch 与 之间的报文使用 A<－>Switch B<－>Switch 这条路C 1200::0/64 Switch C径转发；当 Switch A<－>Switch B<－>Switch C 这条路径发生故障时，BFD 能够快速检测并通告 IPv6 BGP 协议，使得 Switch A<－>Switch D<－>Switch C 这条路径能够迅速生效。

###### 2. 组网图

图7-5 IPv6 BGP 与 BFD 联动配置组网图Switch B Vlan-int100 Vlan-int101 Vlan-int100 Vlan-int101 AS 100 1200::0/64 AS 200 AS 300 Vlan-int200 Vlan-int201 Switch A Switch C Vlan-int200 Vlan-int201 Switch D

| 接口 | IP地址 | 设备 | 接口 |
|---|---|---|---|
| Vlan-int100 | 3000::1/64 | Switch C | Vlan-int101 |
| Vlan-int200 | 2000::1/64 |  | Vlan-int201 |
| Vlan-int100 | 3000::2/64 | Switch D | Vlan-int200 |
| Vlan-int101 | 3001::2/64 |  | Vlan-int201 |

设备 IP地址Switch A 3001::3/64 2001::3/64 Switch B 2000::2/64 2001::2/64

###### 3. 配置步骤

配置各接口的 地址（略）
(1) IPv6
(2) 配置 OSPFv3，保证 Switch A 和 Switch C 之间路由可达（略）
(3) Switch A 上的 IPv6 BGP 配置\# 配置 Switch A 和 Switch C 建立两条 IBGP 连接。
<SwitchA> system-view [SwitchA] bgp 200 [SwitchA-bgp-default] router-id 1.1.1.1 [SwitchA-bgp-default] peer 3001::3 as-number 200 [SwitchA-bgp-default] peer 2001::3 as-number 200 [SwitchA-bgp-default] address-family ipv6 [SwitchA-bgp-default-ipv6] peer 3001::3 enable [SwitchA-bgp-default-ipv6] peer 2001::3 enable [SwitchA-bgp-default-ipv6] quit \# 配置当 Switch A 与 Switch C 之间的两条路径均连通时，Switch C 与 1200::0/64 之间的报文使用 － － 这条路径转发。（在 上对发布给对等体Switch A< >Switch B< >Switch C Switch A 2001::3 的 1200::0/64 路由配置较高的 MED 属性值）
定义编号为 2000 的 IPv6 基本 ACL，允许路由 1200::0/64 通过。
(cid:123)
[SwitchA] acl ipv6 basic 2000

[SwitchA-acl-ipv6-basic-2000] rule permit source 1200:: 64 [SwitchA-acl-ipv6-basic-2000] quit定义两个 Route-policy，一个名为 apply_med_50，为路由 1200::0/64 设置 MED 属性值为(cid:123)
50；另一个名为 apply_med_100，为路由 1200::0/64 设置 MED 属性值为 100。
[SwitchA] route-policy apply_med_50 permit node 10 [SwitchA-route-policy-apply_med_50-10] if-match ipv6 address acl 2000 [SwitchA-route-policy-apply_med_50-10] apply cost 50 [SwitchA-route-policy-apply_med_50-10] quit [SwitchA] route-policy apply_med_100 permit node 10 [SwitchA-route-policy-apply_med_100-10] if-match ipv6 address acl 2000 [SwitchA-route-policy-apply_med_100-10] apply cost 100 [SwitchA-route-policy-apply_med_100-10] quit对发布给对等体 3001::3 的路由应用名为 apply_med_50 的 Route-policy，对发布给对等(cid:123)
体 的路由应用名为 的 Route-policy。
2001::3 apply_med_100 [SwitchA] bgp 200 [SwitchA-bgp-default] address-family ipv6 unicast [SwitchA-bgp-default-ipv6] peer 3001::3 route-policy apply_med_50 export [SwitchA-bgp-default-ipv6] peer 2001::3 route-policy apply_med_100 export [SwitchA-bgp-default-ipv6] quit \# 配置通过 BFD 检测 Switch A<－>Switch B<－>Switch C 这条路径，当该路径出现故障时，BFD 能够快速检测到并通告 IPv6 BGP 协议，使得 Switch A<－>Switch D<－>Switch C 这条路径能够迅速生效。
[SwitchA-bgp-default] peer 3001::3 bfd [SwitchA-bgp-default] quit
(4) Switch C 上的 IPv6 BGP 配置。
配置 和 建立两条 连接。
\# Switch A Switch C IBGP <SwitchC> system-view [SwitchC] bgp 200 [SwitchC-bgp-default] router-id 3.3.3.3 [SwitchC-bgp-default] peer 3000::1 as-number 200 [SwitchC-bgp-default] peer 2000::1 as-number 200 [SwitchC-bgp-default] address-family ipv6 [SwitchC-bgp-default-ipv6] peer 3000::1 enable [SwitchC-bgp-default-ipv6] peer 2000::1 enable [SwitchC-bgp-default-ipv6] quit配置通过 检测 A<－>Switch B<－>Switch 这条路径，当该路径出现故障时，\# BFD Switch C BFD 能够快速检测到并通告 IPv6 BGP 协议，使得 Switch A<－>Switch D<－>Switch C 这条路径能够迅速生效。
[SwitchC-bgp-default] peer 3000::1 bfd [SwitchC-bgp-default] quit [SwitchC] quit

###### 4. 验证配置

下面以 Switch C 为例，Switch A 与此类似，不再赘述。
\# 显示 Switch C 的 BFD 信息。可以看出，Switch A 和 Switch C 之间已经建立了 BFD 会话，而且协议运行正常。
BFD

<SwitchC> display bfd session verbose Total Session Num: 1 Up Session Num: 1 Init Mode: Active IPv6 Session Working Under Ctrl Mode:
Local Discr: 513 Remote Discr: 513 Source IP: 3001::3 Destination IP: 3000::1 Session State: Up Interface: N/A Min Tx Inter: 500ms Act Tx Inter: 500ms Min Rx Inter: 500ms Detect Inter: 2500ms Rx Count: 13 Tx Count: 14 Connect Type: Indirect Running Up for: 00:00:05 Hold Time: 2243ms Auth mode: None Detect Mode: Async Slot: 0 Protocol: BGP4+ Version:1 Diag Info: No Diagnostic \# 在 Switch C 上查看 BGP 邻居信息。可以看出，Switch A 和 Switch C 之间建立两条 BGP 连接，且均处于 Established 状态。
<SwitchC> display bgp peer ipv6 BGP local router ID: 3.3.3.3 Local AS number: 200 Total number of peers: 2 Peers in established state: 2
* - Dynamically created peer Peer AS MsgRcvd MsgSent OutQ PrefRcv Up/Down State 2000::1 200 8 8 0 0 00:04:45 Established 3000::1 200 5 4 0 0 00:01:53 Established \# 在 Switch C 上查看 1200::0/64 的路由信息，可以看出 Switch C 通过 Switch A<－>Switch B<－>Switch 这条路径与 网段通信。
C 1200::0/64 <SwitchC> display ipv6 routing-table 1200::0 64 verbose Summary count : 1 Destination: 1200::/64 Protocol: BGP4+ Process ID: 0 SubProtID: 0x1 Age: 00h01m07s Cost: 50 Preference: 255 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x1 OrigVrf: default-vrf TableID: 0xa OrigAs: 0 NibID: 0x25000001 LastAs: 0 AttrID: 0x1 Neighbor: 3000::1 Flags: 0x10060 OrigNextHop: 3000::1 Label: NULL RealNextHop: FE80::20C:29FF:FE4A:3873

###### 1. 组网需求

BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: Vlan-interface101 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0 \# Switch A<－>Switch B<－>Switch C 这条路径出现故障后，在 Switch C 上查看 1200::0/64 的路由信息，可以看出 Switch C 通过 Switch A<－>Switch D<－>Switch C 这条路径转发报文。
<SwitchC> display ipv6 routing-table 1200::0 64 verbose Summary count : 1 Destination: 1200::/64 Protocol: BGP4+ Process ID: 0 SubProtID: 0x1 Age: 00h00m57s Cost: 100 Preference: 255 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x1 OrigVrf: default-vrf TableID: 0xa OrigAs: 0 NibID: 0x25000000 LastAs: 0 AttrID: 0x0 Neighbor: 2000::1 Flags: 0x10060 OrigNextHop: 2000::1 Label: NULL RealNextHop: FE80::20C:29FF:FE40:715 BkLabel: NULL BkNextHop: N/A Tunnel ID: Invalid Interface: Vlan-interface201 BkTunnel ID: Invalid BkInterface: N/A FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0

##### 7.8.2 配置BGP快速重路由

组网需求
1.
如 图 7-6 所示，Switch A、Switch B、Switch C和Switch D通过BGP协议实现网络互连。要求链路B正常时，Switch A和Switch D之间的流量通过链路B转发；链路B出现故障时，流量可以快速切换到链路A上。

###### 3. 配置步骤

###### 2. 组网图

图7-6 配置 BGP 快速重路由配置步骤
3.
(1) 配置各接口的 IP 地址（略）
(2) 在 AS 200 内配置 OSPFv3，发布接口地址所在网段的路由，确保 Switch B、Switch C 和之间 路由可达（略）
Switch D IPv6
(3) 配置 BGP 连接\# 配置 Switch A 分别与 Switch B 和 Switch C 建立 EBGP 会话，并配置通过 BGP 发布路由::/64。
<SwitchA> system-view [SwitchA] bgp 100 [SwitchA] router-id 1.1.1.1 [SwitchA-bgp-default] peer 3001::2 as-number 200 [SwitchA-bgp-default] peer 2001::2 as-number 200 [SwitchA-bgp-default] address-family ipv6 unicast [SwitchA-bgp-default-ipv6] peer 3001::2 enable [SwitchA-bgp-default-ipv6] peer 2001::2 enable [SwitchA-bgp-default-ipv6] network 1:: 64 [SwitchA-bgp-default-ipv6] quit [SwitchA-bgp-default] quit \# 配置 Switch B 与 Switch A 建立 EBGP 会话，与 Switch D 建立 IBGP 会话。
<SwitchB> system-view [SwitchB] bgp 200 [SwitchB] router-id 2.2.2.2 [SwitchB-bgp-default] peer 3001::1 as-number 100 [SwitchB-bgp-default] peer 3002::2 as-number 200 [SwitchB-bgp-default] address-family ipv6 unicast [SwitchB-bgp-default-ipv6] peer 3001::1 enable [SwitchB-bgp-default-ipv6] peer 3002::2 enable

[SwitchB-bgp-default-ipv6] peer 3002::2 next-hop-local [SwitchB-bgp-default-ipv6] quit [SwitchB-bgp-default] quit \# 配置 Switch C 与 Switch A 建立 EBGP 会话，与 Switch D 建立 IBGP 会话。
<SwitchC> system-view [SwitchC] bgp 200 [SwitchC] router-id 3.3.3.3 [SwitchC-bgp-default] peer 2001::1 as-number 100 [SwitchC-bgp-default] peer 2002::2 as-number 200 [SwitchC-bgp-default] address-family ipv6 unicast [SwitchC-bgp-default-ipv6] peer 2001::1 enable [SwitchC-bgp-default-ipv6] peer 2002::2 enable [SwitchC-bgp-default-ipv6] peer 2002::2 next-hop-local [SwitchC-bgp-default-ipv6] quit [SwitchC-bgp-default] quit配置 分别与 和 建立 会话，并配置 发布路由 4::/64。
\# Switch D Switch B Switch C IBGP BGP <SwitchD> system-view [SwitchD] bgp 200 [SwitchD-bgp-default] peer 3002::1 as-number 200 [SwitchD-bgp-default] peer 2002::1 as-number 200 [SwitchD-bgp-default] address-family ipv6 unicast [SwitchD-bgp-default-ipv6] peer 3002::1 enable [SwitchD-bgp-default-ipv6] peer 2002::1 enable [SwitchD-bgp-default-ipv6] network 4:: 64 [SwitchD-bgp-default-ipv6] quit [SwitchD-bgp-default] quit
(4) 修改路由的首选值，使得 Switch A 和 Switch D 之间的流量优先通过链路 B 转发\# 在 Switch A 上配置从 Switch B 接收到的路由的首选值为 100。
[SwitchA-bgp-default-ipv6] peer 3001::2 preferred-value 100 [SwitchA-bgp-default-ipv6] quit [SwitchA-bgp-default] quit \# 在 Switch D 上配置从 Switch B 接收到的路由的首选值为 100。
[SwitchD-bgp-default-ipv6] peer 3002::1 preferred-value 100 [SwitchD-bgp-default-ipv6] quit [SwitchD-bgp-default] quit
(5) 配置 BGP 快速重路由\# 配置 Switch A：创建路由策略 frr，为路由 4::/64 指定备份下一跳的地址为 2001::2（邻居Switch C 的地址）；在 BGP IPv6 单播地址族下应用该路由策略。
<SwitchA> system-view [SwitchA] ipv6 prefix-list abc index 10 permit 4:: 64 [SwitchA] route-policy frr permit node 10 [SwitchA-route-policy] if-match ipv6 address prefix-list abc [SwitchA-route-policy] apply ipv6 fast-reroute backup-nexthop 2001::2 [SwitchA-route-policy] quit [SwitchA] bgp 100 [SwitchA-bgp-default] address-family ipv6 unicast

###### 4. 验证配置

[SwitchA-bgp-default-ipv6] fast-reroute route-policy frr [SwitchA-bgp-default-ipv6] quit [SwitchA-bgp-default] quit \# 配置 Switch D：创建路由策略 frr，为路由 1::/64 指定备份下一跳的地址为 2002::1（邻居的地址）；在 单播地址族下应用该路由策略。
Switch C BGP IPv6 <SwitchD> system-view [SwitchD] ipv6 prefix-list abc index 10 permit 1:: 64 [SwitchD] route-policy frr permit node 10 [SwitchD-route-policy] if-match ipv6 address prefix-list abc [SwitchD-route-policy] apply ipv6 fast-reroute backup-nexthop 2002::1 [SwitchD-route-policy] quit [SwitchD] bgp 200 [SwitchD-bgp-default] address-family ipv6 unicast [SwitchD-bgp-default-ipv6] fast-reroute route-policy frr [SwitchD-bgp-default-ipv6] quit [SwitchD-bgp-default] quit验证配置
4.
\# 在 Switch A 上查看 4::/64 路由，可以看到备份下一跳信息。
[SwitchA] display ipv6 routing-table 4:: 64 verbose Summary count : 1 Destination: 4::/64 Protocol: BGP4+ Process ID: 0 SubProtID: 0x2 Age: 00h00m58s Cost: 0 Preference: 255 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0xa OrigAs: 200 NibID: 0x25000003 LastAs: 200 AttrID: 0x3 Neighbor: 3001::2 Flags: 0x10060 OrigNextHop: 3001::2 Label: NULL RealNextHop: 3001::2 BkLabel: NULL BkNextHop: 2001::2 Tunnel ID: Invalid Interface: Vlan-interface 100 BkTunnel ID: Invalid BkInterface: Vlan-interface 200 FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0 \# 在 Switch D 上查看 1::/64 路由，可以看到备份下一跳信息。
[SwitchD] display ipv6 routing-table 1:: 64 verbose Summary count : 1 Destination: 1::/64 Protocol: BGP4+ Process ID: 0 SubProtID: 0x1 Age: 00h03m24s

Cost: 0 Preference: 255 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0xa OrigAs: 100 NibID: 0x25000003 LastAs: 100 AttrID: 0x4 Neighbor: 3002::1 Flags: 0x10060 OrigNextHop: 3002::1 Label: NULL RealNextHop: 3002::1 BkLabel: NULL BkNextHop: 2002::1 Tunnel ID: Invalid Interface: Vlan-interface 101 BkTunnel ID: Invalid BkInterface: Vlan-interface 201 FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0

##### 1. 功能简介

### 8 BGP扩展功能

#### 8.1 BGP扩展功能配置任务简介

BGP 扩展功能配置任务如下：
• 配置BGP BMP
• 配置BGP LS配置BGP LS基本功能(cid:123)
（可选）配置BGP LS路由反射功能(cid:123)
（可选）配置BGP LS信息的AS号和Router ID (cid:123)
（可选）手工软复位LS地址族下的BGP会话(cid:123)

#### 8.2 配置BGP BMP

功能简介
1.
通过配置 BMP（BGP Monitoring Protocol，BGP 监控协议）特性，监控服务器可以对网络中设备上 BGP 会话的运行状态进行实时监控，包括对等体关系的建立与解除、路由信息等。
配置 BMP 的设备称为客户端，监控服务器称为监控端，一个客户端可以连接多个监控服务器，通过配置监控服务器的地址和监听端口号来建立与监控服务器的 连接。
TCP

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 创建 BGP 监控服务器，并进入 BMP Server 视图。
bmp server server-number
(3) 配置监控服务器的 IP 地址和端口号。
server address ipv4-address port port-number
缺省情况下，未配置监控服务器的连接地址和端口号。
配置发送统计信息的周期。
(4)
statistics-interval value
缺省情况下，不向监控服务器发送统计信息。
(5) （可选）配置本地设备与监控服务器之间 TCP 连接的源接口。
server connect-interface interface-type interface-number
缺省情况下，BGP 使用到达监控服务器的最佳路由出接口的主 IPv4 地址建立 TCP 连接。
(6) （可选）配置将本地设备发送给监控对等体/对等体组的路由信息发送给监控服务器。
route-mode adj-rib-out
缺省情况下，不会将本地设备发送给监控对等体/对等体组的路由信息发送给监控服务器。
(7) （可选）配置向监控服务器发送 BGP 优选后的路由信息。
route-mode loc-rib

缺省情况下，不向监控服务器发送 BGP 优选后的最优路由信息。
(8) 退回系统视图。
quit
(9) 进入 BGP 实例视图或 BGP-VPN 实例视图。
进入 BGP 实例视图。
(cid:123)
bgp as-number [ instance instance-name ]请依次执行以下命令进入 BGP-VPN 实例视图。
(cid:123)
bgp as-number [ instance instance-name ] ip vpn-instance vpn-instance-name
(10) 配置 BMP Server 监控对等体/对等体组。
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } bmp server server-number-list缺省情况下，未配置 BMP Server 监控对等体/对等体组。
对于同一个对等体/对等体组，如果执行多次命令，最后一次配置生效。

#### 8.3 配置BGP LS

##### 8.3.1 功能简介

BGP LS（Link State，链路状态）功能可以进行跨域和跨 AS 的 LSDB（Link State DataBase，链路状态数据库）、TEDB（TE DataBase，流量工程数据库）信息发布。设备把收集到的链路状态信息发送给控制器，实现了业务与流量的端到端管理和调度，还可以满足需要链路状态信息的各种应用需求。

##### 8.3.2 配置BGP LS基本功能

(1) 进入系统视图。
system-view
(2) 进入 BGP 实例视图。
bgp as-number [ instance instance-name ]
(3) 指定 LS 对等体/对等体组的 AS 号。
peer { ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] }
as-number as-number
缺省情况下，未指定 LS 对等体/对等体组的 AS 号。
(4) 创建 BGP LS 地址族，并进入 LS 地址族视图。
address-family link-state
(5) 使能本地路由器与对等体/对等体组交换 LS 信息的能力。
peer { group-name | ipv4-address [ mask-length ] | ipv6-address
[ prefix-length ] } enable
缺省情况下，本地路由器不能与对等体/对等体组交换 LS 信息。

###### 1. 功能简介

##### 8.3.3 配置BGP LS路由反射功能

功能简介
1.
通常在同一个 AS 内，为了减少 IBGP 连接数，可以把几个 BGP 路由器划分为一个集群，将其中的一台路由器配置为路由反射器，其它路由器作为客户机，通过路由反射器在客户机之间反射路由。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
进入 实例视图。
(2) BGP
bgp as-number [ instance instance-name ]
进入 地址族视图。
(3) BGP LS
address-family link-state
(4) 配置 BGP LS 路由反射功能。
配置本机作为路由反射器，对等体/对等体组作为路由反射器的客户机。
(cid:123)
peer { group-name | ipv4-address [ mask-length ] | ipv6-address
[ prefix-length ] } reflect-client
缺省情况下，未配置路由反射器及其客户机。
（可选）允许路由反射器在客户机之间反射路由。
(cid:123)
reflect between-clients
缺省情况下，允许路由反射器在客户机之间反射路由。
配置本命令后，可减少同一 AS 内 IBGP 的连接数。
（可选）配置路由反射器的集群 ID。
(cid:123)
reflector cluster-id { cluster-id | ipv4-address }
缺省情况下，每个路由反射器都使用自己的 Router ID 作为集群 ID。

##### 8.3.4 配置BGP LS信息的AS号和Router ID

进入系统视图。
(1)
system-view进入 实例视图。
(2) BGP bgp as-number [ instance instance-name ]进入 地址族视图。
(3) BGP LS address-family link-state
(4) 配置 BGP LS 信息的 AS 号和 Router ID。
domain-distinguisher as-number:router-id缺省情况下，使用本 BGP 进程的 AS 号和 Router ID。
在一个 AS 内，当两台设备把相同的 LS 信息发送到同一个 EBGP 邻居时，由于 Router ID 标识的不同，会被认为是不同的 信息。通过配置本功能，可以解决这个问题。
LS

##### 8.3.5 手工软复位LS地址族下的BGP会话

进入系统视图。
(1)
system-view进入 实例视图
(2) BGP bgp as-number [ instance instance-name ]
(3) 配置 Route-refresh 功能。请选择其中一项进行配置。
使能本地路由器与指定对等体/对等体组的 BGP 路由刷新功能。
(cid:123)
peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } capability-advertise route-refresh使能本地路由器与指定 对等体/对等体组的 路由刷新、多协议扩展和 字节BGP BGP 4 AS (cid:123)
号功能。
undo peer { group-name | ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] } capability-advertise conventional缺省情况下，BGP 路由刷新、多协议扩展和 4 字节 AS 号功能处于使能状态。
(4) 手工对 LS 地址族下的 BGP 会话进行软复位。
a. 退回系统视图。
quit
b. 退回用户视图。
quit手工对 地址族下的 会话进行软复位。
c. LS BGP refresh bgp [ instance instance-name ] { ipv4-address [ mask-length ] | ipv6-address [ prefix-length ] | all | external | group group-name | internal } { export | import } link-state

#### 8.4 BGP扩展功能显示和维护

##### 8.4.1 显示BGP

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 BGP 的运行情况，通过查看显示信息验证配置的效果。

###### 1. BGP扩展功能配置显示（IPv4单播）

表8-1 扩展功能配置显示（IPv4 单播）
BGP操作 命令display bgp [ instance instance-name ] bmp server显示BGP监控服务器的信息server-number

###### 2. GP扩展功能配置显示（IPv4组播）

表8-2 BGP 扩展功能配置显示（IPv4 组播）
操作 命令display bgp [ instance instance-name ] bmp server显示BGP监控服务器的信息server-number

###### 3. BGP扩展功能配置显示（LS地址族）

表8-3 BGP 扩展功能配置显示（LS 地址族）
操作 命令display bgp [ instance instance-name ] group显示BGP LS对等体组的信息link-state [ group-name group-name ] display bgp [ instance instance-name ] link-state [ ls-prefix | peer { ipv4-address | ipv6-address }显示BGP LS地址族信息{ advertised | received } [ statistics ] | statistics ] display bgp [ instance instance-name ] peer link-state [ ipv4-address mask-length |显示BGP LS对等体或对等体组的信息 ipv6-address prefix-length | { ipv4-address | ipv6-address | group-name group-name } log-info | [ ipv4-address | ipv6-address ] verbose ] display bgp [ instance instance-name ] update-group显示BGP LS地址族的打包组信息link-state [ ipv4-address | ipv6-address ]

##### 8.4.2 复位BGP会话

当 BGP 路由策略或协议发生变化后，如果需要通过复位 BGP 会话使新的配置生效，请在用户视图下进行下列配置。
表8-4 复位 BGP 会话操作 命令reset bgp [ instance instance-name ] { as-number | ipv4-address [ mask-length ] | ipv6-address复位LS地址族下的BGP会话[ prefix-length ] | all | external | group group-name | internal } link-state

##### 8.4.3 清除BGP信息

在用户视图下，执行 reset 命令可以清除 BGP 相关统计信息。
表8-5 清除 BGP 信息操作 命令reset bgp [ instance instance-name ] bmp server清除BMP监控服务器记录的报文统计信息server-number statistics

###### 3. 配置步骤

#### 8.5 IPv4 BGP扩展功能典型配置举例

##### 8.5.1 BGP LS配置举例

###### 1. 组网需求

• 所有路由器运行 BGP 协议，Switch A 与 Switch B 建立 IBGP 连接，Switch B 分别与 Switch C
和 Switch D 建立 IBGP 连接。
• Switch B 作为路由反射器，Switch A 为 Switch B 的客户机。
• Switch A 能够通过 Switch B 学到 Switch C 和 Switch D 发布的 LS 信息。

###### 2. 组网图

图8-1 BGP LS 配置组网图Switch C t 12 an - i n V l 24 1 /
1 . 1 .
193 .
Switch A Switch B Vlan-int11
- i n t
192.1.1.1/24 V l an 24
1 . 2 /
193 . 1 .
Vlan-int11 V l an V l an - i n t
192.1.1.2/24 - i n 194 13 t 13 . 1 . 1
194 . 1 / 24 . 1 . 1 . 2 / 24 Switch D配置步骤
3.
(1) 配置各接口的 IP 地址，在 Switch C 和 Switch D 上配置 OSPF
(2) 配置 BGP 连接\# 配置 Switch A。
<SwitchA> system-view [SwitchA] bgp 100 [SwitchA-bgp-default] peer 192.1.1.2 as-number 100 [SwitchA-bgp-default] address-family link-state [SwitchA-bgp-default-ls] peer 192.1.1.2 enable [SwitchA-bgp-default-ls] quit [SwitchA-bgp-default] quit \# 配置 Switch B。
<SwitchB> system-view [SwitchB] bgp 100 [SwitchB-bgp-default] peer 192.1.1.1 as-number 100 [SwitchB-bgp-default] peer 193.1.1.1 as-number 100 [SwitchB-bgp-default] peer 194.1.1.1 as-number 100 [SwitchB-bgp-default] address-family link-state [SwitchB-bgp-default-ls] peer 192.1.1.1 enable [SwitchB-bgp-default-ls] peer 193.1.1.1 enable [SwitchB-bgp-default-ls] peer 194.1.1.1 enable

[SwitchB-bgp-default-ls] quit [SwitchB-bgp-default] quit \# 配置 Switch C。
<SwitchC> system-view [SwitchC] bgp 100 [SwitchC-bgp-default] peer 193.1.1.2 as-number 100 [SwitchC-bgp-default] address-family link-state [SwitchC-bgp-default-ls] peer 193.1.1.2 enable [SwitchC-bgp-default-ls] quit [SwitchC-bgp-default] quit [SwitchC] ospf [SwitchC-ospf-1] distribute bgp-ls [SwitchC-ospf-1] area 0 [SwitchC-ospf-1-area-0.0.0.0] network 0.0.0.0 0.0.0.0 [SwitchC-ospf-1-area-0.0.0.0] quit [SwitchC-ospf-1] quit \# 配置 Switch D 。
<SwitchD> system-view [SwitchD] bgp 100 [SwitchD-bgp-default] peer 194.1.1.2 as-number 100 [SwitchD-bgp-default] address-family link-state [SwitchD-bgp-default-ls] peer 194.1.1.2 enable [SwitchD-bgp-default-ls] quit [SwitchD-bgp-default] quit [SwitchD] ospf [SwitchD-ospf-1] distribute bgp-ls [SwitchD-ospf-1] area 0 [SwitchD-ospf-1-area-0.0.0.0] network 0.0.0.0 0.0.0.0 [SwitchD-ospf-1-area-0.0.0.0] quit [SwitchD-ospf-1] quit
(3) 配置路由反射器\# 配置 Switch B。
[SwitchB] bgp 100 [SwitchB-bgp-default] address-family link-state [SwitchB-bgp-default-ls] peer 192.1.1.1 reflect-client [SwitchB-bgp-default-ls] quit [SwitchB-bgp-default] quit

###### 4. 验证配置

查看 的 信息。
\# Switch A LS [SwitchA] display bgp link-state Total number of routes: 4 BGP local Switch ID is 192.1.1.1 Status codes: * - valid, > - best, d - dampened, h - history, s - suppressed, S - stale, i - internal, e - external a – additional-path

Origin: i - IGP, e - EGP, ? - incomplete Prefix codes: E link, V node, T IP reachable route, u/U unknown, I Identifier, N local node, R remote node, L link, P prefix, L1/L2 ISIS level-1/level-2, O OSPF, D direct, S static, a area-ID, , l link-ID, t topology-ID, s ISO-ID, c confed-ID/ASN, b bgp-identifier, r Switch-ID, i if-address, n peer-address, o OSPF Route-type, p IP-prefix d designated Switch address i Network : [V][O][I0x0][N[c100][b193.1.1.1][a0.0.0.0][r193.1.1.1]]/376 NextHop : 193.1.1.1 LocPrf : 100 PrefVal : 0 OutLabel : NULL MED :
Path/Ogn: i i Network : [V][O][I0x0][N[c100][b194.1.1.1][a0.0.0.0][r194.1.1.1]]/376 NextHop : 194.1.1.1 LocPrf : 100 PrefVal : 0 OutLabel : NULL MED :
Path/Ogn: i i Network :
[T][O][I0x0][N[c100][b193.1.1.1][a0.0.0.0][r193.1.1.1]][P[o0x1][p193.1.1.0/24]]/480 NextHop : 193.1.1.1 LocPrf : 100 PrefVal : 0 OutLabel : NULL MED :
Path/Ogn: i i Network :
[T][O][I0x0][N[c100][b194.1.1.1][a0.0.0.0][r194.1.1.1]][P[o0x1][p194.1.1.0/24]]/480 NextHop : 194.1.1.1 LocPrf : 100 PrefVal : 0 OutLabel : NULL MED :
Path/Ogn: i可以看出，Switch A 从 Switch C 和 Switch D 学到了 LS 信息。

## 07-策略路由配置

目 录策略路由简介创建策略节点对本地报文应用策略策略路由典型配置举例

### 1 策略路由

1策略路由

#### 1.1 策略路由简介

与单纯依照 IP 报文的目的地址查找路由表进行转发不同，策略路由是一种依据用户制定的策略进行路由转发的机制。策略路由可以对于满足一定条件（ACL 规则）的报文，执行指定的操作（设置报文的下一跳）。

##### 1.1.1 报文的转发流程

报文到达后，其后续的转发流程如下：
• 首先根据配置的策略路由转发。
• 若找不到匹配的节点，或虽然找到了匹配的节点但指导报文转发失败时，根据路由表中除缺省路由之外的路由来转发报文。
• 若转发失败，则再根据缺省路由来转发报文。

##### 1.1.2 策略路由类型

根据作用对象的不同，策略路由可分为以下两种类型：
本地策略路由：对设备本身产生的报文（比如本地发出的 报文）起作用，指导其发送。
• ping转发策略路由：对接口接收的报文起作用，指导其转发。
•

##### 1.1.3 策略简介

策略用来定义报文的匹配规则，以及对报文执行的操作。策略由节点组成。
一个策略可以包含一个或者多个节点。节点的构成如下：
• 每个节点由节点编号来标识。节点编号越小节点的优先级越高，优先级高的节点优先被执行。
• 每个节点的具体内容由 if-match 子句和 apply 子句来指定。if-match 子句定义该节点的匹配规则，apply 子句定义该节点的动作。
• 每个节点对报文的处理方式由匹配模式决定。匹配模式分为 permit （允许）和 deny （拒绝）
两种。
应用策略后，系统将根据策略中定义的匹配规则和操作，对报文进行处理：系统按照优先级从高到低的顺序依次匹配各节点，如果报文满足这个节点的匹配规则，就执行该节点的动作；如果报文不满足这个节点的匹配规则，就继续匹配下一个节点；如果报文不能满足策略中任何一个节点的匹配规则，则根据路由表来转发报文。

###### 1. if-match子句关系

在一个节点中可以配置多条 if-match 子句，if-match acl 子句只能配置一条，if-match service-chain 子句支持配置多条。
同一个节点中的不同类型 if-match 子句之间是“与”的关系，即报文必须满足该节点的所有if-match 子句才算满足这个节点的匹配规则。同一类型的 if-match 子句之间是“或”的关系，即报文只需满足一条该类型的 if-match 子句就算满足此类型 if-match 子句的匹配规则。

###### 2. apply子句关系

同一个节点中可以配置多条apply子句，但配置的多条apply子句不一定都会执行。多条apply子句之间的关系请参见“1.3.3 配置策略节点的动作”。

###### 3. 节点的匹配模式与节点的if-match子句、apply子句的关系

一个节点的匹配模式与这个节点的if-match子句、apply子句的关系如 表 所示。
1-1表1-1 节点的匹配模式、if-match 子句、apply 子句三者之间的关系

| 是否满足所有 if-match 子句 |  | 节点匹配模式 |  |  |  |  |
|---|---|---|---|---|---|---|
|  |  | permit（允许模式） |  |  | deny（拒绝模式） |  |
|  | • 如果节点配置了 apply 子句，则执行此节点 apply 子句，如果节点指导报文转发成功，则不再匹配下一节点 • 如果节点未配置 apply 子句，则不会执行任何动作，且不再匹配下一节点，报文将根据路由表来进行转发 |  |  |  |  |  |
|  | 不执行此节点apply子句，继续匹配下一节点 |  |  |  |  |  |

如果一个节点中未配置任何 if-match 子句，则认为所有报文都满足该节点的匹配规则，按照“报文满足所有 if-match 子句”的情况进行后续处理。

##### 1.1.4 策略路由与Track联动

策略路由通过与 Track 联动，增强了应用的灵活性和对网络环境变化的动态感知能力。
策略路由可以在配置报文的下一跳时与 项关联，根据 项的状态来动态地决定策略的可Track Track用性。策略路由配置仅在关联的 Track项状态为 Positive 或 NotReady时生效。关于策略路由与 Track联动的详细介绍和相关配置，请参见“可靠性配置指导”中的“Track”。

#### 1.2 策略路由配置任务简介

策略路由配置任务如下：
(1) 配置策略
a. 创建策略节点
b. 配置策略节点的匹配规则
c. 配置策略节点的动作
(2) 应用策略请选择以下至少一项任务进行配置：
对本地报文应用策略(cid:123)
对接口转发的报文应用策略

#### 1.3 配置策略

##### 1.3.1 创建策略节点

(1) 进入系统视图。
system-view
(2) 创建策略节点，并进入策略节点视图。
policy-based-route policy-name [ deny | permit ] node node-number
(3) （可选）设置当前策略节点的描述信息。
description text
缺省情况下，未设置当前策略节点的描述信息。

##### 1.3.2 配置策略节点的匹配规则

###### 1. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入策略节点视图。
policy-based-route policy-name [ deny | permit ] node node-number
设置匹配规则。
(3)
设置 匹配规则。
ACL
(cid:123)
if-match acl { acl-number | name acl-name }
缺省情况下，未设置 匹配规则。
ACL
策略路由不支持匹配二层信息的 匹配规则。
ACL
设置 ACL 匹配规则时，对于 ACL 规则的 permit/deny 动作以及 time-range 指定的规则生
效时间段等的处理机制不再生效。
设置服务链匹配规则。
(cid:123)
if-match service-chain { path-id service-path-id [ path-index
service-patch-index ] }
缺省情况下，未设置服务链匹配规则。

##### 1.3.3 配置策略节点的动作

###### 1. 功能简介

用户通过配置 apply 子句指导策略节点的动作。目前，策略路由仅提供了一种 apply 子句，即apply next-hop，用来设置报文转发的下一跳。
apply子句的含义、执行优先情况和详细说明如 表 1-2 所示。
表1-2 apply 子句的含义以及执行优先情况等说明

|  | 子句 |  |  | 含义 |  |  | 执行优先情况/详细说明 |  |
|---|---|---|---|---|---|---|---|---|
|  |  |  | 设置报文的下一跳 |  |  |  |  |  |

|  | 子句 |  |  | 含义 |  |  | 执行优先情况/详细说明 |  |
|---|---|---|---|---|---|---|---|---|
|  |  |  | 设置报文的服务链规则 |  |  |  |  |  |

###### 2. 配置限制和指导

策略路由通过查询 FIB 表中是否存在下一跳地址对应的条目，判断设置的报文转发下一跳地址是否可用。策略路由周期性检查 FIB 表，设备到下一跳的路径发生变化时，策略路由无法及时感知，可能会导致通信发生短暂中断。

###### 3. 配置指导报文转发类动作

进入系统视图。
(1)
system-view进入策略节点视图。
(2)
policy-based-route policy-name [ deny | permit ] node node-number
(3) 配置动作。
设置报文转发的下一跳。
(cid:123)
apply next-hop [ vpn-instance vpn-instance-name ] { ip-address [ direct ] [ track track-entry-number ] }&<1-2>缺省情况下，未设置报文转发的下一跳。
用户通过一次或多次配置本命令可以同时配置多个下一跳，每个节点最多可以配置 个下2一跳，这些下一跳起到主备的作用。
设置报文的服务链规则。
(cid:123)
apply service-chain path-id service-path-id [ path-index service-patch-index ]缺省情况下，未设置报文的服务链规则。
本配置对软件转发的报文不生效。

#### 1.4 应用策略

##### 1.4.1 对本地报文应用策略

###### 1. 功能简介

通过本配置，可以将已经配置的策略应用到本地，指导设备本身产生报文的发送。应用策略时，该策略必须已经存在，否则配置将失败。

###### 2. 配置限制和指导

• 对本地报文只能应用一个策略。应用新的策略前必须删除本地原来已经应用的策略。
• 若无特殊需求，建议用户不要对本地报文应用策略。否则，有可能会对本地报文的发送造成
不必要的影响（如 ping、telnet 服务的失效）。

###### 3. 配置步骤

(1) 进入系统视图。

system-view
(2) 对本地报文应用策略。
ip local policy-based-route policy-name缺省情况下，未对本地报文应用策略。

##### 1.4.2 对接口转发的报文应用策略

###### 1. 功能简介

通过本配置，可以将已经配置的策略应用到接口，指导接口接收的所有报文的转发。应用策略时，该策略必须已经存在，否则配置将失败。

###### 2. 配置限制和指导

• 对接口转发的报文应用策略时，一个接口只能应用一个策略。应用新的策略前必须删除接口
上原来已经应用的策略。
• 一个策略可以同时被多个接口应用。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 对接口转发的报文应用策略。
ip policy-based-route policy-name
缺省情况下，未对接口转发的报文应用策略。

#### 1.5 策略路由显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置策略路由后的运行情况，通过查看显示信息验证配置的效果。
在用户视图下执行 reset 命令可以清除策略路由的统计信息。
表 策略路由显示和维护1-3操作 命令display ip policy-based-route policy [显示已经配置的策略policy-name ] display ip policy-based-route interface显示接口下转发策略路由的配置信息和统计信息 interface-type interface-number [ slot slot-number ] display ip policy-based-route local [ slot显示本地策略路由的配置信息和统计信息slot-number ]显示已经应用的策略路由信息 display ip policy-based-route setup reset ip policy-based-route statistics清除策略路由的统计信息[ policy policy-name ]

###### 2. 组网图

#### 1.6 策略路由典型配置举例

##### 1.6.1 基于报文协议类型的本地策略路由配置举例

###### 1. 组网需求

Switch A 分别与 Switch B 和 Switch C 直连（保证 Switch B 和 Switch C 之间路由完全不可达）。通过策略路由控制 Switch A 产生的报文：
• 指定所有 TCP 报文的下一跳为 1.1.2.2；
• 其它报文仍然按照查找路由表的方式进行转发。
组网图
2.
图1-1 基于报文协议类型的本地策略路由的配置举例组网图Switch B Vlan-int10 Vlan-int10 Switch A
1.1.2.1/24 1.1.2.2/24 Vlan-int20 Vlan-int20
1.1.3.1/24 1.1.3.2/24 Switch C

###### 3. 配置步骤

(1) 配置 Switch A
\# 创建 VLAN 10 和 VLAN 20。
<SwitchA> system-view
[SwitchA] vlan 10
[SwitchA-vlan10] quit
[SwitchA] vlan 20
[SwitchA-vlan20] quit
\# 配置接口 Vlan-interface10 和 Vlan-interface20 的 IP 地址。
[SwitchA] interface vlan-interface 10
[SwitchA-Vlan-interface10] ip address 1.1.2.1 24
[SwitchA-Vlan-interface10] quit
[SwitchA] interface vlan-interface 20
[SwitchA-Vlan-interface20] ip address 1.1.3.1 24
[SwitchA-Vlan-interface20] quit
\# 定义访问控制列表 ACL 3101，用来匹配 TCP 报文。
[SwitchA] acl advanced 3101
[SwitchA-acl-ipv4-adv-3101] rule permit tcp
[SwitchA-acl-ipv4-adv-3101] quit
\# 定义 5 号节点，指定所有 TCP 报文的下一跳为 1.1.2.2。
[SwitchA] policy-based-route aaa permit node 5
[SwitchA-pbr-aaa-5] if-match acl 3101
[SwitchA-pbr-aaa-5] apply next-hop 1.1.2.2
[SwitchA-pbr-aaa-5] quit
\# 在 Switch A 上应用本地策略路由。
[SwitchA] ip local policy-based-route aaa

(2) 配置 Switch B
\# 创建 VLAN 10
<SwitchB> system-view
[SwitchB] vlan 10
[SwitchB-vlan10] quit
\# 配置接口 Vlan-interface10 的 IP 地址。
[SwitchB] interface vlan-interface 10
[SwitchB-Vlan-interface10] ip address 1.1.2.2 24
配置
(3) Switch C
\#创建
VLAN 20
<SwitchC> system-view
[SwitchC] vlan 20
[SwitchC-vlan20] quit
配置接口 的 地址。
\# Vlan-interface20 IP
[SwitchC] interface vlan-interface 20
[SwitchC-Vlan-interface20] ip address 1.1.3.2 24

###### 4. 验证配置

从 Switch A 上通过 Telnet 方式登录 Switch B（1.1.2.2/24），结果成功。
从 Switch A 上通过 Telnet 方式登录 Switch C（1.1.3.2/24），结果失败。
从 Switch A 上 ping Switch C（1.1.3.2/24），结果成功。
由于 Telnet 使用的是 TCP 协议，ping 使用的是 ICMP 协议，所以由以上结果可证明：Switch A 发出的 TCP 报文的下一跳为 1.1.2.2，接口 Vlan-interface20 不发送 TCP 报文，但可以发送非 TCP报文，策略路由设置成功。

##### 1.6.2 基于报文协议类型的转发策略路由配置举例

###### 1. 组网需求

分别与 和 直连（保证 和 之间路由完全不可达）。
Switch A Switch B Switch C Switch B Switch C通过策略路由控制从 的接口 接收的报文：
Switch A Vlan-interface11指定所有 报文的下一跳为 1.1.2.2；
• TCP其它报文仍然按照查找路由表的方式进行转发。
•

###### 2. 组网图

图1-2 基于报文协议类型的转发策略路由的配置举例组网图

###### 3. 配置步骤

配置前请确保 Switch B 和 Host A，Switch C 和 Host A 之间路由可达。
(1) 配置 Switch A \# 创建 VLAN 10 和 VLAN 20。
<SwitchA> system-view [SwitchA] vlan 10 [SwitchA-vlan10] quit [SwitchA] vlan 20 [SwitchA-vlan20] quit配置接口 和 的 地址。
\# Vlan-interface10 Vlan-interface20 IP [SwitchA] interface vlan-interface 10 [SwitchA-Vlan-interface10] ip address 1.1.2.1 24 [SwitchA-Vlan-interface10] quit [SwitchA] interface vlan-interface 20 [SwitchA-Vlan-interface20] ip address 1.1.3.1 24 [SwitchA-Vlan-interface20] quit定义访问控制列表 3101，用来匹配 报文。
\# ACL TCP [SwitchA] acl advanced 3101 [SwitchA-acl-ipv4-adv-3101] rule permit tcp [SwitchA-acl-ipv4-adv-3101] quit \# 定义 5 号节点，指定所有 TCP 报文的下一跳为 1.1.2.2。
[SwitchA] policy-based-route aaa permit node 5 [SwitchA-pbr-aaa-5] if-match acl 3101

###### 1. 组网需求

[SwitchA-pbr-aaa-5] apply next-hop 1.1.2.2 [SwitchA-pbr-aaa-5] quit \# 在接口 Vlan-interface11 上应用转发策略路由，处理此接口接收的报文。
[SwitchA] interface vlan-interface 11 [SwitchA-Vlan-interface11] ip address 10.110.0.10 24 [SwitchA-Vlan-interface11] ip policy-based-route aaa [SwitchA-Vlan-interface11] quit

###### 4. 验证配置

从 上通过 方式登录 B，结果成功。
Host A Telnet Switch从 上通过 方式登录 C，结果失败。
Host A Telnet Switch从 上 C，结果成功。
Host A ping Switch由于 使用的是 协议，ping 使用的是 协议，所以由以上结果可证明：从Telnet TCP ICMP Switch A的接口 Vlan-interface11 接收的 TCP 报文的下一跳为 1.1.2.2，接口 Vlan-interface20 不转发 TCP报文，但可以转发非 TCP 报文，策略路由设置成功。

##### 1.6.3 基于EVPN的服务链策略路由配置举例

组网需求
1.
Switch A、Switch B、Switch C 为分布式 EVPN 网关设备，Switch D 为 RR，负责在交换机之间反射 BGP 路由。通过匹配以太网服务实例的策略路由，使 Server 1 发出报文先经过以太网服务实例1 中的服务器处理，再发送到 Server2。

###### 2. 组网图

图1-3 基于 EVPN 的服务链策略路由配置组网图

###### 3. 配置步骤

(1) 配置 IP 地址和单播路由协议。
请按照 图 1-3 配置各接口的IP地址和子网掩码，具体配置过程略。
(2) 配置 Switch A
\# 开启 L2VPN 能力。
<SwitchA> system-view
[SwitchA] l2vpn enable
\# 关闭远端 MAC 地址和远端 ARP 自动学习功能。
[SwitchA] vxlan tunnel mac-learning disable
[SwitchA] vxlan tunnel arp-learning disable
\# 在 VSI 实例 vpna 下创建 EVPN 实例，并配置自动生成 EVPN 实例的 RD 和 RT。
[SwitchA] vsi vpna
[SwitchA-vsi-vpna] evpn encapsulation vxlan
[SwitchA-vsi-vpna-evpn-vxlan] route-distinguisher auto
[SwitchA-vsi-vpna-evpn-vxlan] vpn-target auto
[SwitchA-vsi-vpna-evpn-vxlan] quit
\# 创建 VXLAN 10。
[SwitchA-vsi-vpna] vxlan 10
[SwitchA-vsi-vpna-vxlan-10] quit
[SwitchA-vsi-vpna] quit
配置 发布 路由。
\# BGP EVPN
[SwitchA] bgp 200
[SwitchA-bgp-default] peer 4.4.4.4 as-number 200
[SwitchA-bgp-default] peer 4.4.4.4 connect-interface loopback 0
[SwitchA-bgp-default] address-family l2vpn evpn
[SwitchA-bgp-default-evpn] peer 4.4.4.4 enable
[SwitchA-bgp-default-evpn] quit
[SwitchA-bgp-default] quit
\# 创建 VPN 实例 vpna。
[SwitchA] ip vpn-instance vpna
[SwitchA-vpn-instance-vpna] route-distinguisher 1:1
[SwitchA-vpn-instance-vpna] address-family ipv4
[SwitchA-vpn-ipv4-vpna] vpn-target 2:2
[SwitchA-vpn-ipv4-vpna] quit
[SwitchA-vpn-instance-vpna] address-family evpn
[SwitchA-vpn-evpn-vpna] vpn-target 1:1
[SwitchA-vpn-evpn-vpna] quit
[SwitchA-vpn-instance-vpna] quit
\# 配置 VSI 虚接口 VSI-interface1。
[SwitchA] interface vsi-interface 1
[SwitchA-Vsi-interface1] ip binding vpn-instance vpna
[SwitchA-Vsi-interface1] ip address 10.1.1.1 255.255.255.0
[SwitchA-Vsi-interface1] mac-address 0001-0001-0001
[SwitchA-Vsi-interface1] local-proxy-arp enable
[SwitchA-Vsi-interface1] distributed-gateway local

[SwitchA-Vsi-interface1] quit \# 创建 VSI 虚接口 VSI-interface3，在该接口上配置 VPN 实例 vpna 对应的 L3VNI 为 1000。
[SwitchA] interface vsi-interface 3 [SwitchA-Vsi-interface3] ip binding vpn-instance vpna [SwitchA-Vsi-interface3] l3-vni 1000 [SwitchA-Vsi-interface3] quit配置 所在的 实例和接口 关联。
\# VXLAN 10 VSI VSI-interface1 [SwitchA] vsi vpna [SwitchA-vsi-vpna] gateway vsi-interface 1 [SwitchA-vsi-vpna] quit配置 接口 11。
\# VLAN [SwitchA] interface vlan-interface 11 [SwitchA-Vlan-interface11] ip address 11.1.1.1 255.255.255.0 [SwitchA-Vlan-interface11] ospf 1 area 0.0.0.0 [SwitchA-Vlan-interface11] quit \# 配置以太网服务实例 1000 与 VSI 实例 vpna 关联。
[SwitchA] interface gigabitethernet 1/0/1 [SwitchA-GigabitEthernet1/0/1] port link-mode bridge [SwitchA-GigabitEthernet1/0/1] service-instance 1000 [SwitchA-GigabitEthernet1/0/1-srv1000] encapsulation s-vid 2 [SwitchA-GigabitEthernet1/0/1-srv1000] xconnect vsi vpna定义访问控制列表 3000，用来匹配源地址为 10.1.1.10，目的地址为 的报\# ACL 10.1.1.20文。
<SwitchA> system-view [SwitchA] acl advanced 3000 [SwitchA-acl-ipv4-adv-3000] rule 0 permit ip source 10.1.1.10 0 destination 10.1.1.20 \# 定义 0 号节点，指定所有源地址为 10.1.1.1，目的地址为 10.1.1.20 的报文的下一跳为
10.1.1.11。
[SwitchA] policy-based-route aa permit node 0 [SwitchA-pbr-aa-0] if-match acl 3000 [SwitchA-pbr-aa-0] apply service-chain path-id 1 [SwitchA-pbr-aa-0] apply next-hop vpn-instance vpna 10.1.1.11在 虚接口 上应用转发策略路由，处理此接口接收的报文。
\# VSI 3 [SwitchA] interface vsi-interface 3 [SwitchA-Vsi-interface3] ip policy-based-route aa [SwitchA-Vsi-interface3] quit配置
(3) Switch B开启 能力。
\# L2VPN <SwitchB> system-view [SwitchB] l2vpn enable \# 关闭远端 MAC 地址和远端 ARP 自动学习功能。
[SwitchB] vxlan tunnel mac-learning disable [SwitchB] vxlan tunnel arp-learning disable \# 在 VSI 实例 vpna 下创建 EVPN 实例，并配置自动生成 EVPN 实例的 RD 和 RT。
[SwitchB] vsi vpna

[SwitchB-vsi-vpna] evpn encapsulation vxlan [SwitchB-vsi-vpna-evpn-vxlan] route-distinguisher auto [SwitchB-vsi-vpna-evpn-vxlan] vpn-target auto [SwitchB-vsi-vpna-evpn-vxlan] quit \# 创建 VXLAN 10。
[SwitchB-vsi-vpna] vxlan 10 [SwitchB-vsi-vpna-vxlan-10] quit [SwitchB-vsi-vpna] quit \# 配置 BGP 发布 EVPN 路由。
[SwitchB] bgp 200 [SwitchB-bgp-default] peer 4.4.4.4 as-number 200 [SwitchB-bgp-default] peer 4.4.4.4 connect-interface loopback0 [SwitchB-bgp-default] address-family l2vpn evpn [SwitchB-bgp-default-evpn] peer 4.4.4.4 enable \# 创建 VPN 实例 vpna。
[SwitchB] ip vpn-instance vpna [SwitchB-vpn-instance-vpna] route-distinguisher 1:1 [SwitchB-vpn-instance-vpna] address-family ipv4 [SwitchB-vpn-ipv4-vpna] vpn-target 2:2 [SwitchB-vpn-ipv4-vpna] quit [SwitchB-vpn-instance-vpna] address-family evpn [SwitchB-vpn-evpn-vpna] vpn-target 1:1 [SwitchB-vpn-evpn-vpna] quit [SwitchB-vpn-instance-vpna] quit \# 配置 VSI 虚接口 VSI-interface1。
[SwitchB] interface vsi-interface 1 [SwitchB-Vsi-interface1] ip binding vpn-instance vpna [SwitchB-Vsi-interface1] ip address 10.1.1.1 255.255.255.0 [SwitchB-Vsi-interface1] mac-address 0001-0001-0001 [SwitchB-Vsi-interface1] local-proxy-arp enable [SwitchB-Vsi-interface1] distributed-gateway local [SwitchB-Vsi-interface1] quit \# 配置 VXLAN 10 所在的 VSI 实例和接口 VSI-interface1 关联。
[SwitchB] vsi vpna [SwitchB-vsi-vpna] gateway vsi-interface 1 [SwitchB-vsi-vpna] quit \# 配置 VSI 虚接口 VSI-interface3。
[SwitchB] interface vsi-interface 3 [SwitchB-Vsi-interface3] ip binding vpn-instance vpna [SwitchB-Vsi-interface3] l3-vni 1000 [SwitchB-Vsi-interface3] quit \# 配置接口 GigabitEthernet1/0/1 作为 AC 接口。
[SwitchB] interface gigabitethernet 1/0/1 [SwitchB-GigabitEthernet1/0/1] port link-mode bridge [SwitchB-GigabitEthernet1/0/1] service-instance 1000 [SwitchB-GigabitEthernet1/0/1-srv1000] encapsulation s-vid 2 [SwitchB-GigabitEthernet1/0/1-srv1000] xconnect vsi vpna

[SwitchB-GigabitEthernet1/0/1-srv1000] quit [SwitchB-GigabitEthernet1/0/1] quit \# 定义 0 号节点，指定所有源地址为 10.1.1.1 的报文的下一跳为 10.1.1.11。
[SwitchB] policy-based-route aa permit node 0 [SwitchB-pbr-aa-0] if-match service-chain path-id 1 [SwitchB-pbr-aa-0] apply next-hop vpn-instance vpna 10.1.1.11 [SwitchB-pbr-aa-0] quit \# 在 VSI 虚接口 3 上应用转发策略路由，处理此接口接收的报文。
[SwitchB] interface vsi-interface 3 [SwitchB-Vsi-interface3] ip policy-based-route aa [SwitchB-Vsi-interface3] quit
(4) 配置 Switch C \# 开启 L2VPN 能力。
<SwitchC> system-view [SwitchC] l2vpn enable关闭远端 地址和远端 自动学习功能。
\# MAC ARP [SwitchC] vxlan tunnel mac-learning disable [SwitchC] vxlan tunnel arp-learning disable \# 在 VSI 实例 vpna 下创建 EVPN 实例，并配置自动生成 EVPN 实例的 RD 和 RT。
[SwitchC] vsi vpna [SwitchC-vsi-vpna] evpn encapsulation vxlan [SwitchC-vsi-vpna-evpn-vxlan] route-distinguisher auto [SwitchC-vsi-vpna-evpn-vxlan] vpn-target auto [SwitchC-vsi-vpna-evpn-vxlan] quit \# 创建 VXLAN 10。
[SwitchC-vsi-vpna] vxlan 10 [SwitchC-vsi-vpna-vxlan-10] quit [SwitchC-vsi-vpna] quit \# 配置 BGP 发布 EVPN 路由。
[SwitchC] bgp 200 [SwitchC-bgp-default] peer 4.4.4.4 as-number 200 [SwitchC-bgp-default] peer 4.4.4.4 connect-interface loopback 0 [SwitchC-bgp-default] address-family l2vpn evpn [SwitchC-bgp-default-evpn] peer 4.4.4.4 enable [SwitchC-bgp-default-evpn] quit [SwitchC-bgp-default] quit创建 实例 vpna。
\# VPN [SwitchC] ip vpn-instance vpna [SwitchC-vpn-instance-vpna] route-distinguisher 1:1 [SwitchC-vpn-instance-vpna] address-family ipv4 [SwitchC-vpn-ipv4-vpna] vpn-target 2:2 [SwitchC-vpn-ipv4-vpna] quit [SwitchC-vpn-instance-vpna] address-family evpn [SwitchC-vpn-evpn-vpna] vpn-target 1:1 [SwitchC-vpn-evpn-vpna] quit [SwitchC-vpn-instance-vpna] quit

\# 创建 VSI 虚接口 VSI-interface1，并为其配置 IP 地址，该 IP 地址作为 VXLAN 10 内虚拟机的网关地址。
[SwitchC] interface vsi-interface 1 [SwitchC-Vsi-interface1] ip binding vpn-instance vpna [SwitchC-Vsi-interface1] ip address 10.1.1.1 255.255.255.0 [SwitchC-Vsi-interface1] mac-address 0001-0001-0001 [SwitchC-Vsi-interface1] local-proxy-arp enable [SwitchC-Vsi-interface1] distributed-gateway local [SwitchC-Vsi-interface1] quit \# 创建 VSI 虚接口 VSI-interface3，在该接口上配置 VPN 实例 vpna 对应的 L3VNI 为 1000。
[SwitchC] interface vsi-interface 3 [SwitchC-Vsi-interface3] ip binding vpn-instance vpna [SwitchC-Vsi-interface3] l3-vni 1000 [SwitchC-Vsi-interface3] quit \# 配置 VXLAN 10 所在的 VSI 实例和接口 VSI-interface1 关联。
[SwitchC] vsi vpna [SwitchC-vsi-vpna] gateway vsi-interface 1 [SwitchC-vsi-vpna] quit \# 在接入服务器的接口 GigabitEthernet1/0/1 上绑定 VSI。
[SwitchC] interface gigabitethernet 1/0/1 [SwitchC-GigabitEthernet1/0/1] port link-mode bridge [SwitchC-GigabitEthernet1/0/1] service-instance 2000 [SwitchC-GigabitEthernet1/0/1-srv2000] encapsulation s-vid 2 [SwitchC-GigabitEthernet1/0/1] xconnect vsi vpna [SwitchC-GigabitEthernet1/0/1] quit
(5) 配置 Switch D \# 配置 Switch D 与其他交换机建立 BGP 连接。
<SwitchD> system-view [SwitchD] bgp 200 [SwitchD-bgp-default] group evpn [SwitchD-bgp-default] peer 1.1.1.1 group evpn [SwitchD-bgp-default] peer 2.2.2.2 group evpn [SwitchD-bgp-default] peer 3.3.3.3 group evpn [SwitchD-bgp-default] peer evpn as-number 200 [SwitchD-bgp-default] peer evpn connect-interface loopback 0 \# 配置 BGP 发布 EVPN 路由，并关闭 BGP EVPN 路由的 VPN-Target 过滤功能。
[SwitchD-bgp-default] address-family l2vpn evpn [SwitchD-bgp-default-evpn] peer evpn enable [SwitchD-bgp-default-evpn] undo policy vpn-target \# 配置 Switch D 为路由反射器。
[SwitchD-bgp-default-evpn] peer evpn reflect-client [SwitchD-bgp-default-evpn] quit [SwitchD-bgp-default] quit \# 配置 VLAN 接口 11 接口数据。
[SwitchD] interface vlan-interface 11 [SwitchD-Vlan-interface11] ip address 11.1.1.4 255.255.255.0

###### 4. 验证配置

[SwitchD-Vlan-interface11] ospf 1 area 0.0.0.0 [SwitchD-Vlan-interface11] quit \# 配置 VLAN 接口 12 接口数据。
[SwitchD] interface vlan-interface 12 [SwitchD-Vlan-interface12] ip address 12.1.1.4 255.255.255.0 [SwitchD-Vlan-interface12] ospf 1 area 0.0.0.0 [SwitchD-Vlan-interface12] quit \# 配置 VLAN 接口 13 接口数据。
[SwitchD] interface Vlan-interface 13 [SwitchD-Vlan-interface13] ip address 13.1.1.4 255.255.255.0 [SwitchD-Vlan-interface13] ospf 1 area 0.0.0.0 [SwitchD-Vlan-interface13] quit验证配置
4.
这时通过抓包可以看到 Server 1 发出报文先经过以太网服务实例 1 中的服务器处理，再发送到Server2。

## 08-IPv6静态路由配置

目 录静态路由简介配置单跳检测静态路由与 联动（直连）配置举例

##### 1. 功能简介

### 1 IPv6静态路由

#### 1.1 IPv6静态路由简介

静态路由是一种特殊的路由，由管理员手工配置。当网络结构比较简单时，只需配置静态路由就可以使网络正常工作。
静态路由不能自动适应网络拓扑结构的变化。当网络发生故障或者拓扑发生变化后，必须由网络管理员手工修改配置。
静态路由与 静态路由类似，适合于一些结构比较简单的 网络。
IPv6 IPv4 IPv6

#### 1.2 配置IPv6静态路由

(1) 进入系统视图。
system-view
(2) 配置 IPv6 静态路由。
（公网）
ipv6 route-static ipv6-address prefix-length { interface-type
interface-number [ next-hop-address ] | next-hop-address | vpn-instance
d-vpn-instance-name nexthop-address } [ permanent ] [ preference
preference ] [ tag tag-value ] [ description text ]
缺省情况下，未配置 IPv6 静态路由。
（VPN 网络）
ipv6 route-static vpn-instance s-vpn-instance-name ipv6-address
prefix-length { interface-type interface-number [ next-hop-address ] |
nexthop-address [ public ] | vpn-instance d-vpn-instance-name
nexthop-address } [ permanent ] [ preference preference ] [ tag tag-value ]
[ description text ]
缺省情况下，未配置 IPv6 静态路由。
(3) （可选）配置 IPv6 静态路由的缺省优先级。
ipv6 route-static default-preference default-preference
缺省情况下，IPv6 静态路由的缺省优先级为 60。

#### 1.3 配置IPv6静态路由删除

功能简介
1.
使用 undo ipv6 route-static 命令可以删除一条 IPv6 静态路由，而使用 delete ipv6 static-routes all 命令可以删除包括缺省路由在内的所有 IPv6 静态路由。

##### 2. 配置步骤

进入系统视图。
(1)

system-view
(2) 删除所有 IPv6 静态路由。
delete ipv6 [ vpn-instance vpn-instance-name ] static-routes all

#### 1.4 配置IPv6静态路由与BFD联动

##### 1.4.1 功能简介

BFD（Bidirectional Forwarding Detection，双向转发检测）提供了一个通用的、标准化的、介质无关、协议无关的快速故障检测机制，可以为上层协议（如路由协议等）统一地快速检测两台路由器间双向转发路径的故障。使能 IPv6 与 BFD 联动功能后，BFD 将对 IPv6 静态路由的下一跳可达性进行快速检测。当检测到下一跳不可达时，相应的 IPv6 静态路由将会被删除。
关于 BFD 的详细介绍，请参见“可靠性配置指导”中的“BFD”。

##### 1.4.2 配置限制和指导

路由振荡时，使能 功能可能会加剧振荡，请谨慎使用。
BFD

##### 1.4.3 配置双向检测

###### 1. 功能简介

双向检测，即本端和对端需要同时进行配置，通过控制报文检测两个方向上的链路状态，实现毫秒级别的链路故障检测。
双向检测支持直连下一跳和非直连下一跳：
• 直连下一跳是指下一跳和本端是直连的，配置时必须指定出接口和下一跳。
• 非直连下一跳是指下一跳和本端不是直连的，中间还有其它设备。配置时必须指定下一跳和BFD 源 IPv6 地址。

###### 2. 配置直连下一跳双向检测

(1) 进入系统视图。
system-view
(2) 配置静态路由与 BFD 联动。
ipv6 route-static [ vpn-instance s-vpn-instance-name ] ipv6-address
prefix-length interface-type interface-number next-hop-address bfd
control-packet [ bfd-source ipv6-address ] [ preference preference ]
[ tag tag-value ] [ description text ]
缺省情况下，未配置 IPv6 静态路由与 BFD 联动。

###### 3. 配置非直连下一跳双向检测

(1) 进入系统视图。
system-view
(2) 配置静态路由与 BFD 联动。

###### 1. 功能简介

ipv6 route-static [ vpn-instance s-vpn-instance-name ] ipv6-address prefix-length [ vpn-instance d-vpn-instance-name ] { next-hop-address bfd control-packet bfd-source ipv6-address } [ preference preference ] [ tag tag-value ] [ description text ]缺省情况下，未配置 IPv6 静态路由与 BFD 联动。

##### 1.4.4 配置单跳检测

功能简介
1.
单跳检测，即只需要本端进行配置，通过 echo 报文检测链路的状态。echo 报文的目的地址为本端接口地址，发送给下一跳设备后会直接转发回本端。这里所说的“单跳”是 的一跳。
IPv6

###### 2. 配置限制和指导

IPv6 静态路由的出接口为处于 SPOOFING 状态时，不能使用 BFD 进行检测。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置 echo 报文的源 IPv6 地址。
bfd echo-source-ipv6 ipv6-address
缺省情况下，未配置 echo 报文的源 IPv6 地址。
echo 报文源 IPv6 地址仅支持全球单播地址。
本命令的详细情况请参见“可靠性命令参考”中的“BFD”。
配置静态路由与 联动。
(3) BFD
ipv6 route-static [ vpn-instance s-vpn-instance-name ] ipv6-address
prefix-length interface-type interface-number next-hop-address bfd
echo-packet [ bfd-source ipv6-address ] [ preference preference ] [ tag
tag-value ] [ description text ]
缺省情况下，未配置 IPv6 静态路由与 BFD 联动。
下一跳 IPv6 地址必须为全球单播地址。

#### 1.5 IPv6静态路由显示和维护

在完成上述配置后，在任意视图下执行 display 命令查看 IPv6 静态路由配置的运行情况并检验配置结果。
表1-1 IPv6 静态路由显示和维护操作 命令显示IPv6静态路由下一跳信息 display ipv6 route-static nib [ nib-id ] [ verbose ] display ipv6 route-static routing-table [ vpn-instance显示IPv6静态路由表信息vpn-instance-name ] [ ipv6-address prefix-length ]

###### 2. 组网图

操作 命令查看IPv6静态路由表信息（本命令的详细情况请参见“三层技术 display ipv6 routing-table protocol static [ inactive | verbose ]
-IP路由命令参考”中的“IP路由基础”）

#### 1.6 IPv6静态路由典型配置举例

##### 1.6.1 IPv6静态路由基本功能配置举例

###### 1. 组网要求

要求各交换机之间配置 IPv6 静态路由后，可以使所有主机和交换机之间互通。
组网图
2.
图1-1 IPv6 静态路由基本功能配置组网图

###### 3. 配置步骤

(1) 配置各 VLAN 虚接口的 IPv6 地址（略）
(2) 配置 IPv6 静态路由
\# 在 Switch A 上配置 IPv6 缺省路由。
<SwitchA> system-view
[SwitchA] ipv6 route-static :: 0 4::2
\# 在 Switch B 上配置两条 IPv6 静态路由。
<SwitchB> system-view
[SwitchB] ipv6 route-static 1:: 64 4::1
[SwitchB] ipv6 route-static 3:: 64 5::1
\# 在 Switch C 上配置 IPv6 缺省路由。
<SwitchC> system-view
[SwitchC] ipv6 route-static :: 0 5::2
(3) 配置主机地址和网关

根据组网图配置好各主机的 IPv6 地址，并将 Host A 的缺省网关配置为 1::1，Host B 的缺省网关配置为 2::1，Host 的缺省网关配置为 3::1。
C

###### 4. 验证配置

\# 查看 Switch A 的 IPv6 静态路由信息。
[SwitchA] display ipv6 routing-table protocol static Summary Count : 1 Static Routing table Status : <Active> Summary Count : 1 Destination: :: Protocol : Static NextHop : 4::2 Preference: 60 Interface : Vlan-interface200 Cost : 0 Static Routing table Status : <Inactive> Summary Count : 0查看 的 静态路由信息。
\# Switch B IPv6 [SwitchB] display ipv6 routing-table protocol static Summary Count : 2 Static Routing table Status : <Active> Summary Count : 2 Destination: 1::/64 Protocol : Static NextHop : 4::1 Preference: 60 Interface : Vlan-interface200 Cost : 0 Destination: 3::/64 Protocol : Static NextHop : 5::1 Preference: 60 Interface : Vlan-interface300 Cost : 0 Static Routing table Status : <Inactive> Summary Count : 0 \# 使用 Ping 进行验证。
[SwitchA] ping ipv6 3::1 Ping6(56 data bytes) 4::1 --> 3::1, press CTRL_C to break 56 bytes from 3::1, icmp_seq=0 hlim=62 time=0.700 ms 56 bytes from 3::1, icmp_seq=1 hlim=62 time=0.351 ms 56 bytes from 3::1, icmp_seq=2 hlim=62 time=0.338 ms 56 bytes from 3::1, icmp_seq=3 hlim=62 time=0.373 ms 56 bytes from 3::1, icmp_seq=4 hlim=62 time=0.316 ms
--- Ping6 statistics for 3::1 --- 5 packet(s) transmitted, 5 packet(s) received, 0.0% packet loss round-trip min/avg/max/std-dev = 0.316/0.416/0.700/0.143 ms

###### 1. 组网需求

##### 1.6.2 IPv6静态路由与BFD联动（直连）配置举例

组网需求
1.
• 在 Switch A 上配置 IPv6 静态路由可以到达 120::/64 网段，在 Switch B 上配置 IPv6 静态路由可以到达 网段，并都使能 检测功能。
121::/64 BFD在 Switch C 上配置 IPv6 静态路由可以到达 120::/64 网段和 121::/64 网段。
•当 Switch A 和 Switch B 通过 L2 Switch 通信的链路出现故障时，BFD 能够快速感知，并且切
•换到 进行通信。
Switch C

###### 2. 组网图

图1-2 IPv6 静态路由与 BFD 联动（直连）配置组网图

| 接口 | IPv6地址 | 设备 | 接口 |
|---|---|---|---|
| Vlan-int10 | 12::1/64 | Switch B | Vlan-int10 |
| Vlan-int11 | 10::102/64 |  | Vlan-int13 |
| Vlan-int11 | 10:: 100/64 |  |  |
| Vlan-int13 | 13::2/64 |  |  |

设备 IPv6地址Switch A 12::2/64 13::1/64 Switch C

###### 3. 配置步骤

配置各接口的 地址（略）
(1) IPv6配置 静态路由和
(2) IPv6 BFD在 上配置静态路由，并使能 检测功能，使用双向检测方式。
\# Switch A BFD <SwitchA> system-view [SwitchA] interface vlan-interface 10 [SwitchA-vlan-interface10] bfd min-transmit-interval 500 [SwitchA-vlan-interface10] bfd min-receive-interval 500 [SwitchA-vlan-interface10] bfd detect-multiplier 9 [SwitchA-vlan-interface10] quit [SwitchA] ipv6 route-static 120:: 64 vlan-interface 10 12::2 bfd control-packet [SwitchA] ipv6 route-static 120:: 64 10::100 preference 65 [SwitchA] quit在 上配置 静态路由，并使能 检测功能，使用双向检测方式。
\# Switch B IPv6 BFD <SwitchB> system-view [SwitchB] interface vlan-interface 10 [SwitchB-vlan-interface10] bfd min-transmit-interval 500 [SwitchB-vlan-interface10] bfd min-receive-interval 500

[SwitchB-vlan-interface10] bfd detect-multiplier 9 [SwitchB-vlan-interface10] quit [SwitchB] ipv6 route-static 121:: 64 vlan-interface 10 12::1 bfd control-packet [SwitchB] ipv6 route-static 121:: 64 13::2 preference 65 [SwitchB] quit \# 在 Switch C 上配置静态路由。
<SwitchC> system-view [SwitchC] ipv6 route-static 120:: 64 13::1 [SwitchC] ipv6 route-static 121:: 64 10::102

###### 4. 验证配置

下面以 Switch A 为例，Switch B 和 Switch A 类似，不再赘述。
\# 查看 BFD 会话，可以看到 BFD 会话已经创建。
<SwitchA> display bfd session Total Session Num: 1 Up Session Num: 1 Init Mode: Active IPv6 Session Working Under Ctrl Mode:
Local Discr: 513 Remote Discr: 33 Source IP: 12::1 Destination IP: 12::2 Session State: Up Interface: Vlan10 Hold Time: 2012ms \# 查看静态路由，可以看到 Switch A 经过 L2 Switch 到达 Switch B。
<SwitchA> display ipv6 routing-table protocol static Summary Count : 1 Static Routing table Status : <Active> Summary Count : 1 Destination: 120::/64 Protocol : Static NextHop : 12::2 Preference: 60 Interface : Vlan10 Cost : 0 Direct Routing table Status : <Inactive> Summary Count : 0当 Switch A 和 Switch B 通过 L2 Switch 通信的链路出现故障时：
\# 查看 IPv6 静态路由，可以看到 Switch A 经过 Switch C 到达 Switch B。
<SwitchA> display ipv6 routing-table protocol static Summary Count : 1 Static Routing table Status : <Active> Summary Count : 1

Destination: 120::/64 Protocol : Static NextHop : 10::100 Preference: 65 Interface : Vlan11 Cost : 0 Static Routing table Status : < Inactive> Summary Count : 0

##### 1.6.3 IPv6静态路由与BFD联动（非直连）配置举例

###### 1. 组网需求

在 上配置 静态路由可以到达 网段，在 上配置 静态路由
• Switch A IPv6 120::/64 Switch B IPv6可以到达 121::/64 网段，并都使能 BFD 检测功能。
• 在 Switch C 和 Switch D 上配置 IPv6 静态路由可以到达 120::/64 网段和 121::/64 网段。
• Switch A 存在到 Switch B 的接口 Loopback1（2::9/128）的路由，出接口为 Vlan-interface10；
Switch B 存在到 Switch A 的接口 Loopback1（1::9/128）的路由，出接口为 Vlan-interface12；
Switch D 存在到 1::9/128 的路由，出接口为 Vlan-interface10 ，存在到 2::9/128 的路由，出接口为 Vlan-interface12。
当 和 通过 通信的链路出现故障时，BFD 能够快速感知，并且切
• Switch A Switch B Switch D换到 Switch C 进行通信。

###### 2. 组网图

图1-3 IPv6 静态路由与 BFD 联动（非直连）配置组网图Loop1 Loop1 121::/64 120::/64 1::9/128 2::9/128 Switch D Vlan-int10 Vlan-int12 Vlan-int10 Vlan-int12 Switch A V 13 Switch B l an n t
- i BFD - i n an t 11 V l Vlan-int11 Vlan-int13 Switch C

| 接口 | IPv6地址 | 设备 | 接口 |
|---|---|---|---|
| Vlan-int10 | 12::1/64 | Switch B | Vlan-int12 |
| Vlan-int11 | 10::102/64 |  | Vlan-int13 |
| Loop1 | 1::9/128 |  | Loop1 |
| Vlan-int11 | 10::100/64 | Switch D | Vlan-int10 |
| Vlan-int13 | 13::2/64 |  | Vlan-int12 |

设备 IPv6地址Switch A 11::2/64 13::1/64 2::9/128 Switch C 12::2/64 11::1/64

###### 3. 配置步骤

(1) 配置各接口的 IPv6 地址（略）
(2) 配置 IPv6 静态路由和 BFD
\# 在 Switch A 上配置 IPv6 静态路由，并使能 BFD 检测功能，使用双向检测方式。
<SwitchA> system-view

[SwitchA] bfd multi-hop min-transmit-interval 500 [SwitchA] bfd multi-hop min-receive-interval 500 [SwitchA] bfd multi-hop detect-multiplier 9 [SwitchA] ipv6 route-static 120:: 64 2::9 bfd control-packet bfd-source 1::9 [SwitchA] ipv6 route-static 120:: 64 10::100 preference 65 [SwitchA] ipv6 route-static 2::9 128 12::2 [SwitchA] quit \# 在 Switch B 上配置 IPv6 静态路由，并使能 BFD 检测功能，使用双向检测方式。
<SwitchB> system-view [SwitchB] bfd multi-hop min-transmit-interval 500 [SwitchB] bfd multi-hop min-receive-interval 500 [SwitchB] bfd multi-hop detect-multiplier 9 [SwitchB] ipv6 route-static 121:: 64 1::9 bfd control-packet bfd-source 2::9 [SwitchB] ipv6 route-static 121:: 64 13::2 preference 65 [SwitchB] ipv6 route-static 1::9 128 11::1 [SwitchB] quit \# 在 Switch C 上配置静态路由。
<SwitchC> system-view [SwitchC] ipv6 route-static 120:: 64 13::1 [SwitchC] ipv6 route-static 121:: 64 10::102 \# 在 Switch D 上配置静态路由。
<SwitchD> system-view [SwitchD] ipv6 route-static 120:: 64 11::2 [SwitchD] ipv6 route-static 121:: 64 12::1 [SwitchD] ipv6 route-static 2::9 128 11::2 [SwitchD] ipv6 route-static 1::9 128 12::1

###### 4. 验证配置

下面以 Switch A 为例，Switch B 和 Switch A 类似，不再赘述。
\# 查看 BFD 会话，可以看到 BFD 会话已经创建。
<SwitchA> display bfd session Total Session Num: 1 Up Session Num: 1 Init Mode: Active IPv6 Session Working Under Ctrl Mode:
Local Discr: 513 Remote Discr: 33 Source IP: 1::9 Destination IP: 2::9 Session State: Up Interface: N/A Hold Time: 2012ms \# 查看 IPv6 静态路由，可以看到 Switch A 经过 Switch D 到达 Switch B。
<SwitchA> display ipv6 routing-table protocol static Summary Count : 1 Static Routing table Status : <Active>

Summary Count : 1 Destination: 120::/64 Protocol : Static NextHop : 2::9 Preference: 60 Interface : Vlan10 Cost : 0 Static Routing table Status : <Inactive> Summary Count : 0当 Switch A 和 Switch B 通过 Switch D 通信的链路出现故障时：
查看 静态路由，可以看到 经过 到达 B。
\# IPv6 Switch A Switch C Switch <SwitchA> display ipv6 routing-table protocol static Summary Count : 1 Static Routing table Status : <Active> Summary Count : 1 Destination: 120::/64 Protocol : Static NextHop : 10::100 Preference: 65 Interface : Vlan11 Cost : 0 Static Routing table Status : <Inactive> Summary Count : 0

### 2 IPv6缺省路由

缺省路由是在路由器没有找到匹配的 路由表项时使用的路由。
IPv6 IPv6缺省路由有两种生成方式：
IPv6第一种是网络管理员手工配置。配置请参见“1.2 配置IPv6 静态路由”，指定的目的地址为::/0
•（前缀长度为 0）。
• 第二种是动态路由协议生成（如 OSPFv3、IPv6 IS-IS 和 RIPng），由路由能力比较强的路由器将 IPv6 缺省路由发布给其它路由器，其它路由器在自己的路由表里生成指向那台路由器的缺省路由。配置请参见各个路由协议手册。

## 09-RIPng配置

目 录简介配置 的路由信息控制配置 对接收 发布的路由进行过滤调整和优化 网络配置 报文的发送速率配置配置RIPng快速重路由功能配置 报文的零域检查

RIPng基本功能配置举例快速重路由配置举例

### 1 RIPng

1 RIPng

#### 1.1 RIPng简介

RIPng（RIP generation，下一代 协议）是基于距离矢量（Distance-Vector）算法的协议。
next RIP它通过 UDP 报文交换路由信息，使用的端口号为 521。RIPng 是对原来的 IPv4 网络中 RIP-2 协议的扩展，大多数 RIP 的概念都可以用于 RIPng。

##### 1.1.1 RIPng的路由度量值

使用跳数来衡量到达目的地址的距离（也称为度量值或开销）。在 中，从一个路由器RIPng RIPng到其直连网络的跳数为 0，通过与其相连的路由器到达另一个网络的跳数为 1，其余以此类推。当跳数大于或等于 16 时，目的网络或主机就被定义为不可达。

##### 1.1.2 RIPng的路由数据库

每个运行 的路由器都管理一个路由数据库，该路由数据库包含了到所有可达目的地的路由项，RIPng这些路由项包含下列信息：
• 目的地址：主机或网络的 IPv6 地址。
• 下一跳地址：为到达目的地，需要经过的相邻路由器的接口 IPv6 地址。
• 出接口：转发 IPv6 报文通过的出接口。
• 度量值：本路由器到达目的地的开销。
• 路由时间：从路由项最后一次被更新到现在所经过的时间，路由项每次被更新时，路由时间重置为 0。
• 路由标记（Route Tag）：用于标识外部路由，以便在路由策略中根据 Tag 对路由进行灵活的控制。关于路由策略的详细信息，请参见“三层技术-IP 路由配置指导”中的“路由策略”。

##### 1.1.3 RIPng报文及路由发布过程

RIPng 有两种报文：Request 报文和 Response 报文，并采用组播方式发送报文，使用链路本地地址 FF02::9 作为 RIPng 路由更新的目的地址；使用链路本地地址 FE80::/10 作为 RIPng 路由更新的源地址。
当 RIPng 路由器启动后或者需要更新部分路由表项时，便会发出 Request 报文，向邻居请求需要的路由信息。
报文包含本地路由表的信息，一般在下列情况下产生：
Response对某个 Request 报文进行响应
•作为更新报文周期性地发出
•在路由发生变化时触发更新
•收到 Request 报文的 RIPng 路由器会以 Response 报文形式发回给请求路由器。

收到 Response 报文的路由器会更新自己的 RIPng 路由表。为了保证路由的准确性，RIPng 路由器会对收到的 报文进行有效性检查，比如源 地址是否是链路本地地址，端口号是否Response IPv6正确等，没有通过检查的报文会被忽略。

##### 1.1.4 协议规范

与 RIPng 相关的规范有：
RFC 2080：RIPng for IPv6
•RFC 2081：RIPng Protocol Applicability Statement
•

#### 1.2 RIPng配置任务简介

RIPng 配置任务如下：
(1) 配置RIPng的基本功能
(2) （可选）配置RIPng的路由信息控制配置接口附加度量值(cid:123)
配置RIPng路由聚合(cid:123)
配置RIPng发布缺省路由(cid:123)
配置RIPng对接收/发布的路由进行过滤(cid:123)
配置RIPng协议优先级(cid:123)
配置RIPng引入外部路由(cid:123)
（可选）调整和优化RIPng网络
(3)
配置RIPng定时器(cid:123)
配置水平分割和毒性逆转(cid:123)
配置最大等价路由条数(cid:123)
配置RIPng报文的发送速率(cid:123)
配置RIPng触发更新的时间间隔(cid:123)
(4) （可选）提高 RIPng 的可靠性配置RIPng GR (cid:123)
配置 RIPng NSR (cid:123)
配置RIPng快速重路由(cid:123)
(5) （可选）提高RIPng的安全性配置RIPng报文的零域检查(cid:123)
配置IPsec (cid:123)

#### 1.3 配置RIPng的基本功能

(1) 进入系统视图。
system-view
(2) 进入 RIPng 视图。

###### 1. 功能简介

ripng [ process-id ] [ vpn-instance vpn-instance-name ]缺省情况下，系统没有运行 RIPng。
(3) 退回系统视图。
quit
(4) 进入接口视图。
interface interface-type interface-number
(5) 在接口上使能 RIPng 路由协议。
ripng process-id enable缺省情况下，接口上的 RIPng 功能处于关闭状态。
如果接口没有使能 RIPng，那么 RIPng 进程在该接口上既不发送也不接收 RIPng 路由。

#### 1.4 配置RIPng的路由信息控制

##### 1.4.1 配置接口附加度量值

###### 1. 功能简介

附加度量值是在 路由原来度量值的基础上所增加的度量值（跳数），包括发送附加度量值和RIPng接收附加度量值。
• 发送附加度量值：不会改变路由表中的路由度量值，仅当接口发送 RIPng 路由信息时才会添加到发送路由上。
• 接收附加度量值：会影响接收到的路由度量值，接口接收到一条合法的 RIPng 路由时，在将其加入路由表前会把附加度量值加到该路由上。

###### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 设置接口接收 RIPng 路由时的附加度量值。
ripng metricin value缺省情况下，接口接收 RIPng 路由时的附加度量值为 0。
(4) 设置接口发送 RIPng 路由时的附加度量值。
ripng metricout value缺省情况下，接口发送 RIPng 路由时的附加度量值为 1。

##### 1.4.2 配置RIPng路由聚合

功能简介
1.
RIPng 的路由聚合是在接口上实现的，在接口上配置路由聚合，此时可以将 RIPng 要在这个接口上发布出去的路由按最长匹配原则聚合后发布出去。
RIPng 路由聚合可提高网络的可扩展性和效率，缩减路由表。

###### 1. 功能简介

RIPng 将多条路由聚合成一条路由时，聚合路由的 Metric 值将取所有路由 Metric 的最小值。
例如，RIPng 从接口发布出去的路由有两条：11:11:11::24 Metric=2 和 11:11:12::34 Metric=3，在此接口上配置的聚合路由为 11::0/16，则最终发布出去的路由为 Metric=2。
11::0/16

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
配置 在接口发布聚合的 地址，并指定被聚合的路由的 前缀。
(3) RIPng IPv6 IPv6
ripng summary-address ipv6-address prefix-length
缺省情况下，未配置 在接口发布聚合的 地址。
RIPng IPv6

##### 1.4.3 配置RIPng发布缺省路由

###### 1. 功能简介

用户可以配置 以指定度量值向邻居发布一条缺省路由。
RIP

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
配置 发布缺省路由。
(3) RIPng
ripng default-route { only | originate } [ cost cost-value | route-policy
route-policy-name ] *
缺省情况下，RIPng 进程不发布缺省路由。
缺省路由将被强制通过指定接口的路由更新报文发布出去，该路由的发布不考虑其是否已经
存在于本设备的 IPv6 路由表中。

##### 1.4.4 配置RIPng对接收/发布的路由进行过滤

功能简介
1.
用户可通过使用 IPv6 ACL 和 IPv6 前缀列表对接收到的路由信息进行过滤，只有通过过滤的路由才能被加入到 路由表；此外，还可对本机所有要发布的路由进行过滤，包括从其它路由协议引RIPng入的路由和从邻居学到的 RIPng 路由，只有通过过滤的路由才能被发布给 RIPng 邻居。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 RIPng 视图。
ripng [ process-id ] [ vpn-instance vpn-instance-name ]

(3) 对接收的路由信息进行过滤。
filter-policy { ipv6-acl-number | prefix-list prefix-list-name } import
缺省情况下，RIPng 不对接收的路由信息进行过滤。
(4) 对发布的路由信息进行过滤。
filter-policy { ipv6-acl-number | prefix-list prefix-list-name } export
[ protocol [ process-id ] ]
缺省情况下，RIPng 不对发布的路由信息进行过滤。

##### 1.4.5 配置RIPng协议优先级

###### 1. 功能简介

任何路由协议都具备特有的协议优先级，在设备进行路由选择时能够在不同的协议中选择最佳路由。
可以手工设置 RIPng 协议的优先级，设置的值越小，其优先级越高。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 RIPng 视图。
ripng [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 配置 RIPng 路由的优先级。
preference { preference | route-policy route-policy-name } *
缺省情况下，RIPng 路由的优先级为 100。

##### 1.4.6 配置RIPng引入外部路由

(1) 进入系统视图。
system-view
(2) 进入 RIPng 视图。
ripng [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 引入外部路由。
配置 RIPng 引入 BGP4+协议的路由。
(cid:123)
import-route bgp4+ [ as-number ] [ allow-ibgp ] [ cost cost-value |
route-policy route-policy-name ] *
配置 RIPng 引入直连或静态路由。
(cid:123)
import-route { direct | static } [ cost cost-value | route-policy
route-policy-name ] *
配置 RIPng 引入 isisv6、ospfv3 协议或其他 ripng 进程的路由。
(cid:123)
import-route { isisv6 | ospfv3 | ripng } [ process-id ] [ allow-direct |
cost cost-value | route-policy route-policy-name ] *
缺省情况下，RIPng 不引入其它路由。
（可选）配置引入路由的缺省度量值。
(4)

default cost cost-value缺省情况下，引入路由的缺省度量值为 0。

#### 1.5 调整和优化RIPng网络

##### 1.5.1 配置RIPng定时器

###### 1. 功能简介

用户可通过调节 RIPng 定时器来调整 RIPng 路由协议的性能，以满足网络需要。

###### 2. 配置限制和指导

在配置 RIPng 定时器时需要注意，定时器值的调整应考虑网络的性能，并在所有运行 RIPng 的路由器上进行统一配置，避免增加不必要的网络流量。

###### 3. 配置步骤

进入系统视图。
(1)
system-view进入 视图。
(2) RIPng ripng [ process-id ] [ vpn-instance vpn-instance-name ]配置 定时器的值。
(3) RIPng timers { garbage-collect garbage-collect-value | suppress suppress-value | timeout timeout-value | update update-value } *缺省情况下，Update 定时器的值为 秒，Timeout 定时器的值为 秒，Suppress 定时器30 180的值为 120 秒，Garbage-collect 定时器的值为 120 秒。

##### 1.5.2 配置水平分割和毒性逆转

###### 1. 配置限制和指导

• 如果同时配置了水平分割和毒性逆转，则只有毒性逆转功能生效。
• 配置水平分割可以使得从一个接口学到的路由不能通过此接口向外发布，用于避免相邻路由
器间的路由环路。因此，建议不要关闭水平分割。
• 配置毒性逆转可以使得从一个接口学到的路由还可以从这个接口向外发布，但此时这些路由
的度量值已设置为 16，即不可达。

###### 2. 配置水平分割

(1) 进入系统视图。
system-view
进入接口视图。
(2)
interface interface-type interface-number
使能水平分割功能。
(3)
ripng split-horizon
缺省情况下，水平分割功能处于使能状态。

###### 3. 配置毒性逆转

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 使能毒性逆转功能。
ripng poison-reverse
缺省情况下，毒性逆转功能处于关闭状态。

##### 1.5.3 配置最大等价路由条数

(1) 进入系统视图。
system-view
(2) 进入 RIPng 视图。
ripng [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 配置 RIPng 最大等价路由条数。
maximum load-balancing number
缺省情况下，RIPng 支持的等价路由的最大条数与系统支持最大等价路由的条数相同。

##### 1.5.4 配置RIPng报文的发送速率

###### 1. 功能简介

RIPng 周期性地将路由信息放在 RIPng 报文中向邻居发送。
如果路由表里的路由条目数量很多，同时发送大量 RIPng 协议报文有可能会对当前设备和网络带宽带来冲击；因此，路由器将 RIPng 协议报文分为多个批次进行发送，并且对 RIPng 接口每次允许发送的 协议报文最大个数做出限制。
RIPng用户可根据需要配置接口发送 RIPng 报文的时间间隔以及接口一次发送 RIPng 报文的最大个数。

###### 2. 配置步骤

进入系统视图。
(1)
system-view配置 报文的发送速率。
(2) RIPng请依次执行以下命令在 视图下配置 报文发送速率。
RIP RIPng (cid:123)
ripng [ process-id ] [ vpn-instance vpn-instance-name ] output-delay time count count缺省情况下，接口发送 RIPng 报文的时间间隔为 20 毫秒，一次最多发送 3 个 RIPng 报文。
请依次执行以下命令在接口视图下配置 报文发送速率。
RIPng (cid:123)
interface interface-type interface-number ripng output-delay time count count缺省情况下，接口发送 报文的速率以 进程配置的为准。
RIPng RIPng

##### 1. 功能简介

##### 1.5.5 配置RIPng触发更新的时间间隔

功能简介
1.
RIPng 路由信息变化后将以触发更新的方式通知邻居设备，加速邻居设备的路由收敛。如果路由信息频繁变化，且每次变化都立即发送触发更新，将会占用大量系统资源，并影响路由器的效率。通过调节触发更新的时间间隔，可以抑制由于路由信息频繁变化带来的影响。本命令在路由信息变化不频繁的情况下将连续触发更新的时间间隔缩小到 minimum-interval，而在路由信息变化频繁的情况下可以进行相应惩罚，增加 incremental-interval×2 n-2 （n 为连续触发更新的次数），将等待时间按照配置的惩罚增量延长，最大不超过 maximum-interval。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 RIPng 视图。
ripng [ process-id ] [ vpn-instance vpn-instance-name ]
配置 触发更新的时间间隔。
(3) RIPng
timer triggered maximum-interval [ minimum-interval
[ incremental-interval ] ]
缺省情况下，发送触发更新的最大时间间隔为 5 秒，最小间隔为 50 毫秒，增量惩罚间隔为 200
毫秒。

#### 1.6 配置RIPng GR

###### 1. 功能简介

GR（Graceful Restart，平滑重启）是一种在协议重启或主备倒换时 进行平滑重启，保证转RIPng发业务不中断的机制。
GR 有两个角色：
• GR Restarter：发生协议重启或主备倒换事件且具有 GR 能力的设备。
Helper：和 具有邻居关系，协助完成 流程的设备。
• GR GR Restarter GR在普通的路由协议重启的情况下，路由器需要重新学习 路由，并更新 表，此时会引起网RIPng FIB络暂时的中断，基于 RIPng 的 GR 可以解决这个问题。
应用了 GR 特性的设备向外发送 RIPng 全部路由表请求报文，重新从邻居处学习 RIPng 路由，在此期间 FIB 表不变化。在路由协议重启完毕后，设备将重新学到的 RIPng 路由下刷给 FIB 表，使该设备的路由信息恢复到重启前的状态。
本配置在 GR Restarter 上进行。启动了 RIPng 的设备缺省就是 GR Helper。

##### 2. 配置限制和指导

设备充当 后不能再配置 功能。
GR Restarter RIPng NSR

##### 3. 配置步骤

(1) 进入系统视图。
system-view

(2) 进入 RIPng 视图。
ripng [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 使能 RIPng 协议的 GR 能力。
graceful-restart
缺省情况下，RIPng 协议的 GR 能力处于关闭状态。
(4) （可选）配置 RIPng 协议的 GR 重启间隔时间。
graceful-restart interval interval
缺省情况下，RIPng 协议的 GR 重启间隔时间为 60 秒。

#### 1.7 配置RIPng NSR

##### 1. 功能简介

NSR（Nonstop Routing，不间断路由）通过将 RIPng 路由信息从主进程备份到备进程，使设备在发生主备倒换时新主进程可以无缝完成路由的重新生成、下刷，邻接关系不会发生中断，从而避免了主备倒换对转发业务的影响。
GR 特性需要周边设备配合才能完成路由信息的恢复，在网络应用中有一定的限制。NSR 特性不需要周边设备的配合，网络应用更加广泛。

##### 2. 配置限制和指导

各个进程的 功能是相互独立的，只对本进程生效。如果存在多个 进程，建议在各个进NSR RIPng程下使能 RIPng NSR 功能。
设备配置了 RIPng NSR 功能后不能在充当 GR Restarter。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 RIPng 视图。
ripng [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 使能 RIPng NSR 功能。
non-stop-routing
缺省情况下，RIPng 功能处于关闭状态。
NSR

#### 1.8 配置RIPng快速重路由

##### 1.8.1 功能简介

在部署了备份链路的 网络中，当主用链路发生故障时，RIPng 会对路由进行重新计算，在路RIPng由收敛完成后，流量可以通过备份链路进行传输。在路由收敛期间，数据流量将会被中断。
为了尽可能缩短网络故障导致的流量中断时间，网络管理员可以根据需要配置 RIPng 快速重路由功能。

图1-1 RIPng 快速重路由功能示意图如 图 所示，通过在Router B上配置快速重路由功能，RIPng可以为路由指定备份下一跳，当1-1 Router B检测到主用下一跳地址无法到达时，会直接使用备份下一跳地址来指导报文的转发，从而大大缩短了流量路径切换的时间。在快速切换流量传输路径的同时，RIPng会根据变化后的网络拓扑重新计算路由，在路由收敛完毕后，使用新计算出来的最优路由来指导报文转发。

##### 1.8.2 配置限制和指导

• 本功能只适合在主链路三层接口 up，主链路由双通变为单通或者不通的情况下使用。在主链
路三层接口 down 的情况下，本功能不可用。单通现象，即一条链路上的两端，有且只有一端
可以收到另一端发来的报文，此链路称为单向链路。
RIPng 快速重路由功能仅对非迭代 RIPng 路由（即从直连邻居学到 RIPng 路由）有效。
•
等价路由不支持快速重路由功能。
•

##### 1.8.3 配置RIPng快速重路由功能

(1) 进入系统视图。
system-view
(2) 配置路由策略。
在路由策略中通过 命令在路由策略中
apply ipv6 fast-reroute backup-interface
指定备份下一跳。详细配置请参见“三层技术-IP 路由配置指导”中的“路由策略”。
(3) 进入 RIPng 视图。
ripng [ process-id ] [ vpn-instance vpn-instance-name ]
(4) 开启 RIPng 快速重路由功能。
fast-reroute route-policy route-policy-name
缺省情况下，RIPng 快速重路由功能处于关闭状态。

##### 1.8.4 配置RIPng快速重路由支持BFD检测功能

###### 1. 功能简介

RIPng 协议的快速重路由特性中，主用链路缺省不使用 BFD 进行链路故障检测。配置本功能后，将使用 BFD（Echo 方式）进行检测，可以加快 RIPng 协议的收敛速度。

###### 2. 配置步骤

###### 1. 功能简介

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置 BFD Echo 报文源地址。
bfd echo-source-ipv6 ipv6-address
缺省情况下，未配置 BFD Echo 报文源地址。
echo 报文的源 IPv6 地址用户可以任意指定。建议配置 echo 报文的源 IPv6 地址不属于该设备
任何一个接口所在网段。
本命令的详细介绍请参见“可靠性命令参考”中的“BFD”。
(3) 进入接口视图。
interface interface-type interface-number
(4) 使能 RIPng 协议中主用链路的 BFD（Echo 方式）检测功能。
ripng primary-path-detect bfd echo
缺省情况下，RIPng 协议中主用链路的 BFD（Echo 方式）检测功能处于关闭状态。

#### 1.9 提高RIPng的安全性

##### 1.9.1 配置RIPng报文的零域检查

功能简介
1.
RIPng 报文头部中的一些字段必须配置为 0，也称为零域。使能 RIPng 报文的零域检查功能后，如果报文头部零域中的值不为零，这些报文将被丢弃，不做处理。如果能确保所有报文都是可信任的，则不需要进行该项检查，以节省 CPU 处理时间。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 RIPng 视图。
ripng [ process-id ] [ vpn-instance vpn-instance-name ]
(3) 使能对 RIPng 报文头部的零域检查功能。
checkzero缺省情况下，RIPng 报文的零域检查功能处于使能状态。

##### 1.9.2 配置IPsec保护RIPng报文

###### 1. 功能简介

在安全性要求较高的网络环境中，可以通过配置基于 IPsec 安全框架的认证方式来对 RIPng 报文进行有效性检查和验证。 IPsec 安全框架的具体情况请参见“安全配置指导”中的“ IPsec ”。
设备在发送的报文中会携带配置好的 IPsec 安全框架的 SPI（Security Parameter Index，安全参数索引）值，接收报文时通过 SPI 值进行 IPsec 安全框架匹配：只有安全框架匹配的报文才能接收；
否则将不会接收报文，从而不能正常建立邻居和学习路由。

###### 2. 配置限制和指导

RIPng 支持在进程和接口下配置 IPsec 安全框架。进程下配置的 IPsec 安全框架对该进程下的所有报文有效，接口下的 IPsec 安全框架只对接口下的报文有效。当接口和接口所在进程均配置了 IPsec安全框架时，接口下的配置生效。

###### 3. RIPng进程上应用IPsec安全框架

(1) 进入系统视图。
system-view
(2) 进入 RIPng 视图。
ripng [ process-id ] [ vpn-instance vpn-instance-name ]
配置 进程应用 安全框架。
(3) RIPng IPsec
enable ipsec-profile profile-name
缺省情况下，RIPng 进程没有应用 安全框架。
IPsec

###### 4. 接口上应用IPsec安全框架

(1) 进入系统视图。
system-view
进入接口视图。
(2)
interface interface-type interface-number
配置使能了 的接口上应用 安全框架。
(3) RIPng IPsec
ripng ipsec-profile profile-name
缺省情况下，RIPng 接口没有应用 安全框架。
IPsec

#### 1.10 RIPng显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 RIPng 的运行情况，通过查看显示信息验证配置的效果。
在用户视图下执行 reset 命令可以重启 RIPng 进程或清除指定 RIPng 进程的统计信息。
表1-1 RIPng 显示和维护操作 命令显示RIPng进程的GR状态信息 display ripng [ process-id ] graceful-restart显示RIPng进程的NSR状态信息 display ripng [ process-id ] non-stop-routing显示RIPng进程的配置信息 display ripng [ process-id] display ripng process-id database [ ipv6-address显示RIPng发布数据库中的路由prefix-length ] display ripng process-id interface [ interface-type显示指定RIPng进程的接口信息interface-number ] display ripng process-id neighbor [ interface-type显示RIPng进程的邻居信息interface-number ]

操作 命令display ripng process-id route [ ipv6-address显示指定RIPng进程的路由信息 prefix-length [ verbose ] | peer ipv6-address | statistics ]重启指定RIPng进程 reset ripng process-id process清除RIPng进程的统计信息 reset ripng process-id statistics

#### 1.11 RIPng典型配置举例

##### 1.11.1 RIPng基本功能配置举例

###### 1. 组网需求

• Switch A、Switch B 和 Switch C 相连并通过 RIPng 来学习网络中的 IPv6 路由信息。
• 在 Switch B 上对接收的 Switch A 的路由（2::/64）进行过滤，使其不加入到 Switch B 的 RIPng
进程的路由表中，发布给 Switch A 的路由只有（4::/64）。

###### 2. 组网图

图1-2 基本功能配置组网图RIPng

###### 3. 配置步骤

(1) 配置各接口的 IPv6 地址（略）
(2) 配置 RIPng 的基本功能
\# 配置 Switch A。
<SwitchA> system-view
[SwitchA] ripng 1
[SwitchA-ripng-1] quit
[SwitchA] interface vlan-interface 100
[SwitchA-Vlan-interface100] ripng 1 enable
[SwitchA-Vlan-interface100] quit
[SwitchA] interface vlan-interface 400
[SwitchA-Vlan-interface400] ripng 1 enable
[SwitchA-Vlan-interface400] quit
\# 配置 Switch B。
<SwitchB> system-view
[SwitchB] ripng 1
[SwitchB-ripng-1] quit
[SwitchB] interface vlan-interface 200

[SwitchB-Vlan-interface200] ripng 1 enable [SwitchB-Vlan-interface200] quit [SwitchB] interface vlan-interface 100 [SwitchB-Vlan-interface100] ripng 1 enable [SwitchB-Vlan-interface100] quit \# 配置 Switch C。
<SwitchC> system-view [SwitchC] ripng 1 [SwitchC-ripng-1] quit [SwitchC] interface vlan-interface 200 [SwitchC-Vlan-interface200] ripng 1 enable [SwitchC-Vlan-interface200] quit [SwitchC] interface vlan-interface 500 [SwitchC-Vlan-interface500] ripng 1 enable [SwitchC-Vlan-interface500] quit [SwitchC] interface vlan-interface 600 [SwitchC-Vlan-interface600] ripng 1 enable [SwitchC-Vlan-interface600] quit查看 的 路由表。
\# Switch B RIPng [SwitchB] display ripng 1 route Route Flags: A - Aging, S - Suppressed, G - Garbage-collect, D – Direct O - Optimal, F - Flush to RIB
---------------------------------------------------------------- Peer FE80::20F:E2FF:FE23:82F5 on Vlan-interface100 Destination 2::/64, via FE80::20F:E2FF:FE23:82F5, cost 1, tag 0, AOF, 6 secs Peer FE80::20F:E2FF:FE00:100 on Vlan-interface200 Destination 4::/64, via FE80::20F:E2FF:FE00:100, cost 1, tag 0, AOF, 11 secs Destination 5::/64, via FE80::20F:E2FF:FE00:100, cost 1, tag 0, AOF, 11 Local route Destination 1::/64, via ::, cost 0, tag 0, DOF Destination 3::/64, via ::, cost 0, tag 0, DOF查看 的 路由表。
\# Switch A RIPng [SwitchA] display ripng 1 route Route Flags: A - Aging, S - Suppressed, G - Garbage-collect, D – Direct O - Optimal, F - Flush to RIB
---------------------------------------------------------------- Peer FE80::200:2FF:FE64:8904 on Vlan-interface100 Destination 3::/64, via FE80::200:2FF:FE64:8904, cost 1, tag 0, AOF, 31 secs Destination 4::/64, via FE80::200:2FF:FE64:8904, cost 2, tag 0, AOF, 31 secs

Destination 5::/64, via FE80::200:2FF:FE64:8904, cost 2, tag 0, AOF, 31 secs Local route Destination 2::/64, via ::, cost 0, tag 0, DOF Destination 1::/64, via ::, cost 0, tag 0, DOF
(3) 配置 Switch B 对接收和发布的路由进行过滤[SwitchB] ipv6 prefix-list aaa permit 4:: 64 [SwitchB] ipv6 prefix-list bbb deny 2:: 64 [SwitchB] ipv6 prefix-list bbb permit :: 0 less-equal 128 [SwitchB] ripng 1 [SwitchB-ripng-1] filter-policy prefix-list aaa export [SwitchB-ripng-1] filter-policy prefix-list bbb import [SwitchB-ripng-1] quit查看 和 的 路由表。
\# Switch B Switch A RIPng [SwitchB] display ripng 1 route Route Flags: A - Aging, S - Suppressed, G - Garbage-collect, D – Direct O - Optimal, F - Flush to RIB
---------------------------------------------------------------- Peer FE80::1:100 on Vlan-interface100 Peer FE80::3:200 on Vlan-interface200 Destination 4::/64, via FE80::2:200, cost 1, tag 0, AOF, 11 secs Destination 5::/64, via FE80::2:200, cost 1, tag 0, AOF, 11 secs Local route Destination 1::/64, via ::, cost 0, tag 0, DOF Destination 3::/64, via ::, cost 0, tag 0, DOF [SwitchA] display ripng 1 route Route Flags: A - Aging, S - Suppressed, G - Garbage-collect, D – Direct O - Optimal, F - Flush to RIB
---------------------------------------------------------------- Peer FE80::2:100 on Vlan-interface100 Destination 4::/64, via FE80::1:100, cost 2, tag 0, AOF, 2 secs

##### 1.11.2 RIPng引入外部路由配置举例

###### 1. 组网需求

Switch B 上运行两个 RIPng 进程：RIPng100 和 RIPng200。Switch B 通过 RIPng100 和
•Switch A 交换路由信息，通过 RIPng200 和 Switch C 交换路由信息。

###### 3. 配置步骤

要求在 Switch B 上配置路由引入，将两个不同进程的 RIPng 路由相互引入到对方的 RIPng 进
•程中。

###### 2. 组网图

图1-3 RIPng 引入外部路由配置组网图配置步骤
3.
(1) 配置各接口的 IPv6 地址（略）
(2) 配置 RIPng \# 在 Switch A 上启动 RIPng 进程 100。
<SwitchA> system-view [SwitchA] ripng 100 [SwitchA-ripng-100] quit [SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] ripng 100 enable [SwitchA-Vlan-interface100] quit [SwitchA] interface vlan-interface 200 [SwitchA-Vlan-interface200] ripng 100 enable [SwitchA-Vlan-interface200] quit \# 在 Switch B 上启动两个 RIPng 进程，进程号分别为 100 和 200。
<SwitchB> system-view [SwitchB] ripng 100 [SwitchB-ripng-100] quit [SwitchB] interface vlan-interface 100 [SwitchB-Vlan-interface100] ripng 100 enable [SwitchB-Vlan-interface100] quit [SwitchB] ripng 200 [SwitchB-ripng-200] quit [SwitchB] interface vlan-interface 300 [SwitchB-Vlan-interface300] ripng 200 enable [SwitchB-Vlan-interface300] quit \# 在 Switch C 上启动 RIPng 进程 200。
<SwitchC> system-view [SwitchC] ripng 200 [SwitchC] interface vlan-interface 300 [SwitchC-Vlan-interface300] ripng 200 enable [SwitchC-Vlan-interface300] quit [SwitchC] interface vlan-interface 400 [SwitchC-Vlan-interface400] ripng 200 enable

[SwitchC-Vlan-interface400] quit \# 查看 Switch A 的路由表信息。
[SwitchA] display ipv6 routing-table Destinations : 7 Routes : 7 Destination: ::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: 1::/64 Protocol : Direct NextHop : :: Preference: 0 Interface : Vlan100 Cost : 0 Destination: 1::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: 2::/64 Protocol : Direct NextHop : :: Preference: 0 Interface : Vlan200 Cost : 0 Destination: 2::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: FE80::/10 Protocol : Direct NextHop : :: Preference: 0 Interface : NULL0 Cost : 0 Destination: FF00::/8 Protocol : Direct NextHop : :: Preference: 0 Interface : NULL0 Cost : 0配置 引入外部路由
(3) RIPng在 上将两个不同 进程的路由相互引入到对方的路由表中。
\# Switch B RIPng [SwitchB] ripng 100 [SwitchB-ripng-100] import-route ripng 200 [SwitchB-ripng-100] quit [SwitchB] ripng 200 [SwitchB-ripng-200] import-route ripng 100 [SwitchB-ripng-200] quit查看路由引入后 的路由表信息。
\# Switch A [SwitchA] display ipv6 routing-table Destinations : 8 Routes : 8 Destination: ::1/128 Protocol : Direct

NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: 1::/64 Protocol : Direct NextHop : :: Preference: 0 Interface : Vlan100 Cost : 0 Destination: 1::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: 2::/64 Protocol : Direct NextHop : :: Preference: 0 Interface : Vlan200 Cost : 0 Destination: 2::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: 4::/64 Protocol : RIPng NextHop : FE80::200:BFF:FE01:1C02 Preference: 100 Interface : Vlan100 Cost : 1 Destination: FE80::/10 Protocol : Direct NextHop : :: Preference: 0 Interface : NULL0 Cost : 0 Destination: FF00::/8 Protocol : Direct NextHop : :: Preference: 0 Interface : NULL0 Cost : 0

##### 1.11.3 RIPng GR配置举例

###### 1. 组网需求

、 和 通过 协议实现网络互连。
• Switch A Switch B Switch C RIPng作为 Restarter，Switch 和 作为 并且通过 机制与
• Switch A GR B Switch C GR Helper GR Switch A 保持同步。

###### 3. 配置步骤

###### 2. 组网图

图1-4 RIPng GR 配置组网图配置步骤
3.
(1) 配置各路由器接口的 IPv6 地址和 RIPng 协议请按照上面组网图配置各接口的 IPv6 地址，具体配置过程略。
配置各路由器之间采用 RIPng 协议进行互连，确保 Router A、Router B 和 Router C 之间能够在网络层互通，并且各路由器之间能够借助 RIPng 协议实现动态路由更新。
(2) 配置 RIPng GR \# 使能 Switch A 的 RIPng GR 功能。
<SwitchA> system-view [SwitchA] ripng 1 [SwitchA-ripng-1] graceful-restart

###### 4. 验证配置

\# 在 Switch A 上触发协议重启或主备倒换后，查看 RIPng 的 GR 状态。
<SwitchA> display ripng 1 graceful-restart RIPng process: 1 Graceful Restart capability : Enabled Current GR state : Normal Graceful Restart period : 60 seconds Graceful Restart remaining time: 0 seconds

##### 1.11.4 RIPng NSR配置举例

###### 1. 组网需求

S、Switch A、Switch 通过 协议实现网络互连。要求对 进行主备倒换时，
Switch B RIPng Switch S
Switch A 和 Switch B 到 Switch S 的邻居没有中断，Switch A 到 Switch B 的流量没有中断。

###### 2. 组网图

图1-5 RIPng NSR 配置组网图

###### 3. 配置步骤

配置各接口的 地址和 协议
(1) IPv6 RIPng请按照上面组网图配置各接口的 地址，具体配置过程略。
IPv6配置各交换机之间采用 协议进行互连，确保 S、Switch 和 之间能够RIPng Switch A Switch D在网络层互通，并且各路由器之间能够借助 RIPng 协议实现动态路由更新。
(2) 配置 RIPng NSR \# 使能 Switch S 的 RIPng NSR 功能。
<SwitchS> system-view [SwitchS] ripng 1 [SwitchS-ripng-1] non-stop-routing [SwitchS-ripng-1] quit

###### 4. 验证配置

进行主备倒换。
\# Switch S [SwitchS] placement reoptimize Predicted changes to the placement Program Current location New location
--------------------------------------------------------------------- lb 0/0 0/0 lsm 0/0 0/0 slsp 0/0 0/0 rib6 0/0 0/0 routepolicy 0/0 0/0 rib 0/0 0/0 staticroute6 0/0 0/0 staticroute 0/0 0/0 eviisis 0/0 0/0 ospf 0/0 1/0 Continue? [y/n]:y Re-optimization of the placement start. You will be notified on completion Re-optimization of the placement complete. Use 'display placement' to view the new placement \# 查看 Switch A 上 RIPng 协议的邻居和路由。
[SwitchA] display ripng 1 neighbor Neighbor Address: FE80::AE45:5CE7:422E:2867 Interface : Vlan-interface100 Version : RIPng version 1 Last update: 00h00m23s Bad packets: 0 Bad routes : 0

[SwitchA] display ripng 1 route Route Flags: A - Aging, S - Suppressed, G - Garbage-collect, D - Direct O - Optimal, F - Flush to RIB
---------------------------------------------------------------- Peer FE80::AE45:5CE7:422E:2867 on Vlan-interface100 Destination 1400:1::/64, via FE80::AE45:5CE7:422E:2867, cost 1, tag 0, AOF, 1 secs Destination 4004::4/128, via FE80::AE45:5CE7:422E:2867, cost 2, tag 0, AOF, 1 secs Local route Destination 2002::2/128, via ::, cost 0, tag 0, DOF Destination 1200:1::/64, via ::, cost 0, tag 0, DOF \# 查看 Switch B 上 RIPng 协议的邻居和路由。
[SwitchB] display ripng 1 neighbor Neighbor Address: FE80::20C:29FF:FECE:6277 Interface : Vlan-interface200 Version : RIPng version 1 Last update: 00h00m18s Bad packets: 0 Bad routes : 0 [SwitchB] display ripng 1 route Route Flags: A - Aging, S - Suppressed, G - Garbage-collect, D - Direct O - Optimal, F - Flush to RIB
---------------------------------------------------------------- Peer FE80::20C:29FF:FECE:6277 on Vlan-interface200 Destination 2002::2/128, via FE80::20C:29FF:FECE:6277, cost 2, tag 0, AOF, 24 secs Destination 1200:1::/64, via FE80::20C:29FF:FECE:6277, cost 1, tag 0, AOF, 24 secs Local route Destination 4004::4/128, via ::, cost 0, tag 0, DOF Destination 1400:1::/64, via ::, cost 0, tag 0, DOF通过上面信息可以看出在 Switch S 发生主备倒换的时候， Switch A 和 Switch B 的邻居和路由信息保持不变，从 到 的流量转发没有受到主备倒换的影响。
Switch A Switch B

##### 1.11.5 RIPng快速重路由配置举例

###### 1. 组网需求

Switch A、Switch B 和 Switch C 通过 RIPng 协议实现网络互连。要求当 Switch A 和 Switch B 之间的链路出现单通故障时，业务可以快速切换到链路 B 上。

###### 3. 配置步骤

###### 2. 组网图

图1-6 RIPng 快速重路由配置组网图

| 接口 | IP地址 | 设备 | 接口 |
|---|---|---|---|
| Vlan-int100 | 1::1/64 | Switch B | Vlan-int101 |
| Vlan-int200 | 2::1/64 |  | Vlan-int200 |
| Loop0 | 10::1/128 |  | Loop0 |
| Vlan-int100 | 1::2/64 |  |  |
| Vlan-int101 | 3::2/64 |  |  |

设备 IP地址Switch A 3::1/64 2::2/64 20::1/128 Switch C配置步骤
3.
(1) 配置各路由器接口的 IPv6 地址和 RIPng 协议请按照上面组网图配置各接口的 IP 地址和子网掩码，具体配置过程略。
配置各交换机之间采用 RIPng 协议进行互连，确保 Switch A、Switch B 和 Switch C 之间能够在网络层互通，并且各交换机之间能够借助 协议实现动态路由更新。
RIPng具体配置过程略。
(2) 配置 RIPng 快速重路由\# 配置 Switch A。
<SwitchA> system-view [SwitchA] ipv6 prefix-list abc index 10 permit 20::1 128 [SwitchA] route-policy frr permit node 10 [SwitchA-route-policy-frr-10] if-match ipv6 address prefix-list abc [SwitchA-route-policy-frr-10] apply ipv6 fast-reroute backup-interface vlan-interface 100 backup-nexthop 1::2 [SwitchA-route-policy-frr-10] quit [SwitchA] ripng 1 [SwitchA-ripng-1] fast-reroute route-policy frr [SwitchA-ripng-1] quit \# 配置 Switch B。
<SwitchB> system-view [SwitchB] ipv6 prefix-list abc index 10 permit 10::1 128 [SwitchB] route-policy frr permit node 10 [SwitchB-route-policy-frr-10] if-match ipv6 address prefix-list abc [SwitchB-route-policy-frr-10] apply ipv6 fast-reroute backup-interface vlan-interface 101 backup-nexthop 3::2 [SwitchB-route-policy-frr-10] quit

[SwitchB] ripng 1 [SwitchB-ripng-1] fast-reroute route-policy frr [SwitchB-ripng-1] quit

###### 4. 验证配置

在 上查看 的路由信息，可以看到备份下一跳信息。
\# Switch A 20::1/128 [SwitchA] display ipv6 routing-table 20::1 128 verbose Summary count : 1 Destination: 20::1/128 Protocol: RIPng Process ID: 1 SubProtID: 0x0 Age: 00h17m42s Cost: 1 Preference: 100 IpPre: N/A QosLocalID: N/A Tag: 0 State: Inactive Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0xa OrigAs: 0 NibID: 0x22000003 LastAs: 0 AttrID: 0xffffffff Neighbor: FE80::34CD:9FF:FE2F:D02 Flags: 0x41 OrigNextHop: FE80::34CD:9FF:FE2F:D02 Label: NULL RealNextHop: FE80::34CD:9FF:FE2F:D02 BkLabel: NULL BkNextHop: FE80::7685:45FF:FEAD:102 Tunnel ID: Invalid Interface: Vlan-interface200 BkTunnel ID: Invalid BkInterface: Vlan-interface100 FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0 \# 在 Switch B 上查看 10::1/128 的路由信息，可以看到备份下一跳信息。
[SwitchB] display ipv6 routing-table 10::1 128 verbose Summary count : 1 Destination: 10::1/128 Protocol: RIPng Process ID: 1 SubProtID: 0x0 Age: 00h22m34s Cost: 1 Preference: 100 IpPre: N/A QosLocalID: N/A Tag: 0 State: Inactive Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0xa OrigAs: 0 NibID: 0x22000001 LastAs: 0 AttrID: 0xffffffff Neighbor: FE80::34CC:E8FF:FE5B:C02 Flags: 0x41 OrigNextHop: FE80::34CC:E8FF:FE5B:C02 Label: NULL RealNextHop: FE80::34CC:E8FF:FE5B:C02 BkLabel: NULL BkNextHop: FE80::7685:45FF:FEAD:102 Tunnel ID: Invalid Interface: Vlan-interface200

BkTunnel ID: Invalid BkInterface: Vlan-interface101 FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0

##### 1.11.6 RIPng IPsec安全框架配置举例

###### 1. 组网需求

A、Switch 和 相连并通过 来学习网络中的 路由信息。
• Switch B Switch C RIPng IPv6
要求配置 安全框架对 A、Switch 和 之间的 报文进行有效性检
• IPsec Switch B Switch C RIPng
查和验证。

###### 2. 组网图

图1-7 RIPng IPsec 安全框架配置组网图

###### 3. 配置步骤

(1) 配置各接口的 IPv6 地址（略）
(2) 配置 RIPng 基本功能
\# 配置 Switch A。
<SwitchA> system-view
[SwitchA] ripng 1
[SwitchA-ripng-1] quit
[SwitchA] interface vlan-interface 100
[SwitchA-Vlan-interface100] ripng 1 enable
[SwitchA-Vlan-interface100] quit
\# 配置 Switch B。
<SwitchB> system-view
[SwitchB] ripng 1
[SwitchB-ripng-1] quit
[SwitchB] interface vlan-interface 200
[SwitchB-Vlan-interface200] ripng 1 enable
[SwitchB-Vlan-interface200] quit
[SwitchB] interface vlan-interface 100
[SwitchB-Vlan-interface100] ripng 1 enable
[SwitchB-Vlan-interface100] quit
\# 配置 Switch C。
<SwitchC> system-view
[SwitchC] ripng 1
[SwitchC-ripng-1] quit
[SwitchC] interface vlan-interface 200
[SwitchC-Vlan-interface200] ripng 1 enable
[SwitchC-Vlan-interface200] quit
(3) 配置 RIPng IPsec 安全框架

\# 配置 Switch A。创建名为 protrf1 的安全提议，报文封装形式采用传输模式，安全协议采用协议。创建一条安全框架 profile001，协商方式为 manual，配置 和密钥。
ESP SPI [SwitchA] ipsec transform-set protrf1 [SwitchA-ipsec-transform-set-protrf1] esp encryption-algorithm 3des-cbc [SwitchA-ipsec-transform-set-protrf1] esp authentication-algorithm md5 [SwitchA-ipsec-transform-set-protrf1] encapsulation-mode transport [SwitchA-ipsec-transform-set-protrf1] quit [SwitchA] ipsec profile profile001 manual [SwitchA-ipsec-profile-profile001-manual] transform-set protrf1 [SwitchA-ipsec-profile-profile001-manual] sa spi inbound esp 256 [SwitchA-ipsec-profile-profile001-manual] sa spi outbound esp 256 [SwitchA-ipsec-profile-profile001-manual] sa string-key inbound esp simple abc [SwitchA-ipsec-profile-profile001-manual] sa string-key outbound esp simple abc [SwitchA-ipsec-profile-profile001-manual] quit配置 B。创建名为 的安全提议，报文封装形式采用传输模式，安全协议采用\# Switch protrf1 ESP 协议。创建一条安全框架 profile001，协商方式为 manual，配置 SPI 和密钥。
[SwitchB] ipsec transform-set protrf1 [SwitchB-ipsec-transform-set-protrf1] esp encryption-algorithm 3des-cbc [SwitchB-ipsec-transform-set-protrf1] esp authentication-algorithm md5 [SwitchB-ipsec-transform-set-protrf1] encapsulation-mode transport [SwitchB-ipsec-transform-set-protrf1] quit [SwitchB] ipsec profile profile001 manual [SwitchB-ipsec-profile-profile001-manual] transform-set protrf1 [SwitchB-ipsec-profile-profile001-manual] sa spi inbound esp 256 [SwitchB-ipsec-profile-profile001-manual] sa spi outbound esp 256 [SwitchB-ipsec-profile-profile001-manual] sa string-key inbound esp simple abc [SwitchB-ipsec-profile-profile001-manual] sa string-key outbound esp simple abc [SwitchB-ipsec-profile-profile001-manual] quit \# 配置 Switch C。创建名为 protrf1 的安全提议，报文封装形式采用传输模式，安全协议采用ESP 协议。创建一条安全框架 profile001，协商方式为 manual，配置 SPI 和密钥。
[SwitchC] ipsec transform-set protrf1 [SwitchC-ipsec-transform-set-protrf1] esp encryption-algorithm 3des-cbc [SwitchC-ipsec-transform-set-protrf1] esp authentication-algorithm md5 [SwitchC-ipsec-transform-set-protrf1] encapsulation-mode transport [SwitchC-ipsec-transform-set-protrf1] quit [SwitchC] ipsec profile profile001 manual [SwitchC-ipsec-profile-profile001-manual] transform-set protrf1 [SwitchC-ipsec-profile-profile001-manual] sa spi inbound esp 256 [SwitchC-ipsec-profile-profile001-manual] sa spi outbound esp 256 [SwitchC-ipsec-profile-profile001-manual] sa string-key inbound esp simple abc [SwitchC-ipsec-profile-profile001-manual] sa string-key outbound esp simple abc [SwitchC-ipsec-profile-profile001-manual] quit
(4) RIPng 进程上应用 IPsec 安全框架\# 配置 Switch A。
[SwitchA] ripng 1 [SwitchA-ripng-1] enable ipsec-profile profile001 [SwitchA-ripng-1] quit

\# 配置 Switch B。
[SwitchB] ripng 1 [SwitchB-ripng-1] enable ipsec-profile profile001 [SwitchB-ripng-1] quit \# 配置 Switch C。
[SwitchC] ripng 1 [SwitchC-ripng-1] enable ipsec-profile profile001 [SwitchC-ripng-1] quit

###### 4. 验证配置

以上配置完成后，Switch A、Switch 和 之间的 报文将被加密传输。
B Switch C RIPng

## 10-OSPFv3配置

目 录简介配置 的区域属性配置 的虚连接配置 接口的网络类型为广播配置 的路由信息控制过滤通过接收到的 计算出来的路由信息配置OSPFv3 协议的优先级配置 定时器

配置LSA重新生成的时间间隔忽略 报文中的 检查功能简介配置Stub路由器配置配置 快速重路由支持 检测功能（ 方式）
配置OSPFv3 网管功能

NSSA区域配置举例配置举例快速重路由配置举例

### 1 OSPFv3

1 OSPFv3

#### 1.1 OSPFv3简介

是 OSPF（Open First，开放最短路径优先）版本 的简称，主要提供对OSPFv3 Shortest Path 3 IPv6的支持。

##### 1.1.1 OSPFv3和OSPFv2的异同点

OSPFv3 和 OSPFv2 在很多方面是相同的：
Router ID，Area ID 仍然是 32 位的。
•
• 相同类型的报文：Hello 报文，DD（Database Description，数据库描述）报文，LSR（Link Request，链路状态请求）报文，LSU（Link Update，链路状态更新）报文和State State LSAck （ Link State Acknowledgment ，链路状态确认）报文。
• 相同的邻居发现机制和邻接形成机制。
• 相同的 LSA 扩散机制和老化机制。
和 的不同主要有：
OSPFv3 OSPFv2是基于链路运行；OSPFv2 是基于网段运行。在配置 时，不需要考虑是否
• OSPFv3 OSPFv3配置在同一网段，只要在同一链路，就可以直接建立联系。
• OSPFv3 在同一条链路上可以运行多个实例，即一个接口可以使能多个 OSPFv3 进程（使用不同的实例）。
• OSPFv3 是通过 Router ID 来标识邻居；OSPFv2 则是通过 IPv4 地址来标识邻居。
关于 OSPF 版本 2 的介绍，请参见“三层技术-IP 路由”中的“OSPF”。

##### 1.1.2 OSPFv3的协议报文

和 一样，OSPFv3 也有五种报文类型，如下：
OSPFv2报文：周期性发送，用来发现和维持 邻居关系，以及进行 DR（Designated
• Hello OSPFv3 Router，指定路由器）/BDR（Backup Designated Router，备份指定路由器）的选举。
• DD（Database Description，数据库描述）报文：描述了本地 LSDB（Link State DataBase，链路状态数据库）中每一条 LSA（Link State Advertisement，链路状态通告）的摘要信息，用于两台路由器进行数据库同步。
• LSR（Link State Request，链路状态请求）报文：向对方请求所需的 LSA。两台路由器互相交换 报文之后，得知对端的路由器有哪些 是本地的 所缺少的，这时需要发送DD LSA LSDB LSR 报文向对方请求所需的 LSA。
• LSU（Link State Update，链路状态更新）报文：向对方发送其所需要的 LSA。
（ ，链路状态确认）报文：用来对收到的 进行确认。
• LSAck Link State Acknowledgment LSA

##### 1.1.3 OSPFv3的LSA类型

LSA（Link Advertisement，链路状态通告）是 协议计算和维护路由信息的主要来源，State OSPFv3常用的 LSA 有以下几种类型：
• Router LSA（Type-1）：由每个路由器生成，描述本路由器的链路状态和开销，只在路由器所处区域内传播。
• Network LSA（Type-2）：由广播网络和 NBMA（Non-Broadcast Multi-Access，非广播多路访问）网络的 DR（Designated Router，指定路由器）生成，描述本网段接口的链路状态，只在 所处区域内传播。
DR LSA（Type-3）：由 ABR（Area Router，区域边界路由器）生成，
• Inter-Area-Prefix Border在与该 LSA 相关的区域内传播，描述一条到达本自治系统内其他区域的 IPv6 地址前缀的路由。
• Inter-Area-Router LSA（Type-4）：由 ABR 生成，在与该 LSA 相关的区域内传播，描述一条到达本自治系统内的 ASBR（Autonomous System Boundary Router，自治系统边界路由器）
的路由。
LSA（Type-5）：由 生成，描述到达其它 AS（Autonomous System，自
• AS External ASBR治系统）的路由，传播到整个 AS（Stub 区域和 NSSA 区域除外）。缺省路由也可以用 AS External LSA 来描述。
• NSSA LSA（Type-7）：由 NSSA（Not-So-Stubby Area）区域内的 ASBR 生成，描述到 AS外部的路由，仅在 NSSA 区域内传播。
Link LSA（Type-8）：路由器为每一条链路生成一个 Link LSA，在本地链路范围内传播，描
•述该链路上所连接的 地址前缀及路由器的 地址。
IPv6 Link-local LSA（Type-9）：包含路由器上的 前缀信息，Stub 区域信息或穿越区
• Intra-Area-Prefix IPv6域（Transit Area）的网段信息，该 LSA 在区域内传播。由于 Router LSA 和 Network LSA 不再包含地址信息，导致了 Intra-Area-Prefix LSA 的引入。
• Grace LSA（Type-11）：由 Restarter 在重启的时候生成，在本地链路范围内传播。这个 LSA描述了重启设备的重启原因和重启时间间隔，目的是通知邻居本设备将进入 GR（Graceful Restart，平滑重启）。

##### 1.1.4 协议规范

与 OSPFv3 相关的协议规范有：
• RFC 2328：OSPF Version 2
• RFC 3101：OSPF Not-So-Stubby Area (NSSA) Option
• RFC 4552：Authentication/Confidentiality for OSPFv3
• RFC 5187：OSPFv3 Graceful Restart
• RFC 5286：Basic Specification for IP Fast Reroute: Loop-Free Alternates
• RFC 5329 ： Traffic Engineering Extensions to OSPF Version 3
• RFC 5340：OSPF for IPv6
• RFC 5523：OSPFv3-Based Layer 1 VPN Auto-Discovery
• RFC 5643：Management Information Base for OSPFv3

RFC 6506：Supporting Authentication Trailer for OSPFv3
•RFC 6565：OSPFv3 as a Provider Edge to Customer Edge (PE-CE) Routing Protocol
•RFC 6969：OSPFv3 Instance ID Registry Update
•
• RFC 7166：Supporting Authentication Trailer for OSPFv3

#### 1.2 OSPFv3配置任务简介

OSPFv3 配置任务如下：
(1) 使能OSPFv3 功能
(2) （可选）配置OSPFv3 的区域属性配置OSPFv3 的Stub区域(cid:123)
配置OSPFv3 的NSSA区域(cid:123)
配置OSPFv3 的虚连接(cid:123)
所有非骨干区域必须与骨干区域保持连通，并且骨干区域自身也要保持连通。无法满足这个要求时，可以通过在 ABR 上配置 OSPFv3 虚连接予以解决。
(3) （可选）配置OSPFv3 的网络类型配置OSPFv3 接口的网络类型为广播(cid:123)
配置OSPFv3 接口的网络类型为NBMA (cid:123)
配置OSPFv3 接口的网络类型为P2MP (cid:123)
配置OSPFv3 接口的网络类型为P2P (cid:123)
(4) （可选）配置OSPFv3 的路由信息控制配置OSPFv3 区域间路由聚合(cid:123)
配置对引入的外部路由信息进行路由聚合(cid:123)
过滤通过接收到的LSA计算出来的路由信息(cid:123)
配置过滤Inter-Area-Prefix-LSA (cid:123)
配置OSPFv3 接口的开销值(cid:123)
配置OSPFv3 最大等价路由条数(cid:123)
配置OSPFv3 协议的优先级(cid:123)
配置 OSPFv3 引入外部路由(cid:123)
配置OSPFv3 引入缺省路由(cid:123)
(5) （可选）配置OSPFv3 定时器配置OSPFv3 报文定时器(cid:123)
配置接口的LSA传输延迟时间(cid:123)
配置SPF计算时间间隔(cid:123)
配置LSA重新生成的时间间隔(cid:123)
配置接口发送 LSU 报文的时间间隔和一次发送 LSU 报文的最大个数(cid:123)
(6) （可选）配置接口的DR优先级
(7) （可选）配置OSPFv3 报文相关功能忽略DD报文中的MTU检查(cid:123)

##### 1. 功能简介

禁止接口收发OSPFv3 报文(cid:123)
(8) （可选）配置前缀抑制
(9) （可选）配置Stub路由器
(10) （可选）提高 OSPF 网络的可靠性配置OSPFv3 GR (cid:123)
配置OSPFv3 NSR (cid:123)
配置OSPFv3 与BFD联动(cid:123)
配置OSPFv3 快速重路由(cid:123)
(11) （可选）配置OSPFv3 安全功能配置OSPFv3 验证(cid:123)
应用IPsec安全框架保护OSPFv3 报文(cid:123)
(12) （可选）配置OSPFv3 日志和告警功能配置邻居状态变化的输出开关(cid:123)
配置OSPFv3 的日志信息个数(cid:123)
配置OSPFv3 网管功能(cid:123)

#### 1.3 使能OSPFv3功能

功能简介
1.
要在路由器上使能 OSPFv3 功能，必须先创建 OSPFv3 进程、指定该进程的 Router ID 并在接口上使能 OSPFv3 功能。
在一台路由器上可以创建多个 OSPFv3 进程，OSPFv3 进程是本地概念。不同的路由器之间，即使进程不同也可以进行报文交换。
用来在一个自治系统中唯一的标识一台路由器。在 中，用户必须手工配置一个Router ID OSPFv3 Router ID，而且必须保证自治系统中任意两台路由器的 Router ID 都不相同。因此，为了保证OSPFv3 运行的稳定性，在进行网络规划时，应确定路由器 ID 的划分并手工配置。

##### 2. 配置限制和指导

如果在同一台路由器上运行了多个 OSPFv3 进程，必须为不同的进程指定不同的 Router ID。

##### 3. 配置步骤

进入系统视图。
(1)
system-view启动 OSPFv3，并进入 视图。
(2) OSPFv3 ospfv3 [ process-id | vpn-instance vpn-instance-name ] *缺省情况下，系统没有运行 OSPFv3。
(3) 配置路由器的 Router ID。
router-id router-id缺省情况下，运行 OSPFv3 协议的路由器没有 Router ID。
(4) 进入接口视图。
interface interface-type interface-number

(5) 在接口上使能 OSPFv3 功能。
ospfv3 process-id area area-id [ instance instance-id ]
缺省情况下，接口上的 OSPFv3 功能处于关闭状态。

#### 1.4 配置OSPFv3的区域属性

##### 1.4.1 功能简介

OSPFv3 支持 Stub 区域、NSSA 区域和虚连接的配置，其原理及应用环境与 OSPFv2 相同。
OSPFv3 划分区域后，可以减少网络中 LSA 的数量，OSPFv3 的扩展性也得以增强。对于位于 AS边缘的一些非骨干区域，为了更多的缩减其路由表规模和降低 的数量，可以将它们配置为LSA Stub区域。
Stub 区域不能引入外部路由，为了在允许将自治系统外部路由通告到 OSPFv3 路由域内部的同时，保持其余部分的 Stub 区域的特征，网络管理员可以将区域配置为 NSSA 区域。NSSA 区域也是位于 AS 边缘的非骨干区域。
在划分区域之后，非骨干区域之间的 OSPFv3 路由更新是通过骨干区域来交换完成的。对此，要求所有非骨干区域必须与骨干区域保持连通，并且骨干区域自身也要保持连通。但在实OSPFv3际应用中，可能会因为各方面条件的限制，无法满足这个要求。这时可以通过配置 OSPFv3 虚连接予以解决。

##### 1.4.2 配置OSPFv3的Stub区域

###### 1. 配置限制和指导

对于位于 Stub 区域中的所有路由器都必须执行本配置。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 进入 OSPFv3 区域视图。
area area-id
(4) 配置一个区域为 Stub 区域。
stub [ default-route-advertise-always | no-summary ] *
缺省情况下，没有区域被配置为 Stub 区域。
参数 no-summary 只能在 ABR 上配置。指定 no-summary 参数后，ABR 只向区域内发布一
条描述缺省路由的 Inter-Area-Prefix-LSA。
(5) （可选）配置发送到 Stub 区域的缺省路由的开销值。
default-cost cost - value
缺省情况下，发送到 Stub 区域的缺省路由的开销值为 1。

##### 1.4.3 配置OSPFv3的NSSA区域

###### 1. 配置限制和指导

对于位于 NSSA 区域中的所有路由器都必须执行本配置。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 进入 OSPFv3 区域视图。
area area-id
(4) 配置一个区域为 NSSA 区域。
nssa [ default-route-advertise [ cost cost-value | nssa-only |
route-policy route-policy-name | tag tag | type type ] * |
no-import-route | no-summary | [ translate-always | translate-never ] |
suppress-fa | translator-stability-interval value ] *
缺省情况下，没有区域被配置为 NSSA 区域。
指定 no-summary 参数可以将该区域配置为 Totally NSSA 区域，该区域的 ABR 不会将区域
间的路由信息传递到本区域。
(5) （可选）配置发送到 NSSA 区域的缺省路由的开销值。
default-cost cost-value
缺省情况下，发送到 NSSA 区域的缺省路由的开销值为 1。
本命令只有在 NSSA 区域和 Totally NSSA 区域的 ABR/ASBR 上配置才能生效。

##### 1.4.4 配置OSPFv3的虚连接

###### 1. 功能简介

对于没有和骨干区域直接相连的非骨干区域，或者不连续的骨干区域，可以使用该配置建立逻辑上的连通性。

###### 2. 配置限制和指导

虚连接的两端必须是 ABR，而且必须在两端同时配置才可生效。
虚连接不能在使能了 能力的进程下的区域进行配置。
GR

###### 3. 配置步骤

(1) 进入系统视图。
system-view
进入 视图。
(2) OSPFv3
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
进入 区域视图。
(3) OSPFv3
area area-id

###### 2. 配置步骤

(4) 创建并配置虚连接。
vlink-peer router-id [ dead seconds | hello seconds | instance
instance-id | ipsec-profile profile-name | keychain keychain-name |
retransmit seconds | trans-delay seconds ] *

#### 1.5 配置OSPFv3的网络类型

##### 1.5.1 配置限制和指导

OSPFv3 根据链路层协议类型将网络分为四种不同的类型：广播、NBMA、P2MP 和 P2P。接口的网络类型根据物理接口而定，用户可以根据需要配置 OSPFv3 接口的网络类型：
• 如果在广播网络上有不支持组播地址的路由器，可以将接口的网络类型改为 NBMA。
• 如果一网段内只有两台路由器运行 OSPFv3 协议，也可将接口类型配置为 P2P，节省网络开销。

##### 1.5.2 配置OSPFv3接口的网络类型为广播

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
配置 接口的网络类型。
(3) OSPFv3
ospfv3 network-type broadcast [ instance instance-id ]
缺省情况下，接口的网络类型为广播类型。

##### 1.5.3 配置OSPFv3接口的网络类型为NBMA

###### 1. 配置限制和指导

当路由器的接口类型为 时，由于无法通过广播 报文的形式发现相邻路由器，必须手工NBMA Hello指定相邻路由器的本地链路地址、该相邻路由器是否有 DR 选举权等。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置 OSPFv3 接口的网络类型为 NBMA。
ospfv3 network-type nbma [ instance instance-id ]缺省情况下，接口的网络类型为广播类型。
(4) （可选）配置 OSPFv3 接口的路由优先级。
ospfv3 dr-priority priority缺省情况下，接口的路由优先级为 1。

###### 2. 配置步骤

本命令设置的优先级用于实际的 DR 选举。
(5) 配置 NBMA 网络的邻居。
ospfv3 peer ipv6-address [ cost cost-value | dr-priority priority ] [ instance instance-id ]缺省情况下，未指定邻居接口的链路本地地址。

##### 1.5.4 配置OSPFv3接口的网络类型为P2MP

###### 1. 配置限制和指导

当路由器的接口的网络类型为 P2MP，且在 网络中接口选择单播形式发送报文时，由于无法P2MP通过广播 Hello 报文的形式发现相邻路由器，必须手工指定相邻路由器的本地链路地址。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置 OSPFv3 接口的网络类型为 P2MP。
ospfv3 network-type p2mp [ unicast ] [ instance instance-id ]缺省情况下，接口的网络类型为广播类型。
(4) 配置 P2MP（单播）网络的邻居。
ospfv3 peer ipv6-address [ cost cost-value | dr-priority priority ] [ instance instance-id ]缺省情况下，未指定邻居接口的链路本地地址。

##### 1.5.5 配置OSPFv3接口的网络类型为P2P

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置 OSPFv3 接口的网络类型为 P2P。
ospfv3 network-type p2p [ instance instance-id ]
缺省情况下，接口的网络类型为广播类型。

#### 1.6 配置OSPFv3的路由信息控制

##### 1.6.1 配置OSPFv3区域间路由聚合

###### 1. 功能简介

如果一个区域中存在多个连续的网段，则可以在 ABR 上配置路由聚合将它们聚合成一个网段，ABR只发送一条聚合后的 LSA，所有落入本命令指定的聚合网段范围的 LSA 将不再会被单独发送出去，这样可减小其它区域中 LSDB 的规模。

###### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 进入 OSPFv3 区域视图。
area area-id
(4) 配置 ABR 路由聚合。
abr-summary ipv6-address prefix-length [ not-advertise ] [ cost cost-value ]缺省情况下，ABR 不对路由进行聚合。

##### 1.6.2 配置对引入的外部路由信息进行路由聚合

###### 1. 功能简介

如果引入的路由中存在多个连续的网段，则可以在 上配置路由聚合将它们聚合成一个网段。
ASBR如果本地路由器是 ASBR，配置 ASBR 路由聚合可对引入的聚合地址范围内的 Type-5 LSA 描述的路由进行聚合；当配置了 NSSA 区域时，对引入的聚合地址范围内的 Type-7 LSA 描述的路由进行聚合。
如果本地路由器同时是 ASBR 和 ABR，并且是 NSSA 区域的转换路由器，则对由 Type-7 LSA 转化成的 Type-5 LSA 描述的路由进行聚合处理；如果不是 NSSA 区域的转换路由器，则不进行聚合处理。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
进入 视图。
(2) OSPFv3
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
配置 路由聚合。
(3) ASBR
asbr-summary ipv6-address prefix-length [ cost cost-value |
not-advertise | nssa-only | tag tag ] *
缺省情况下，ASBR 不对引入的路由进行聚合。

###### 1. 功能简介

##### 1.6.3 过滤通过接收到的LSA计算出来的路由信息

功能简介
1.
OSPFv3 接收到 LSA 后，可以根据一定的过滤条件来决定是否将计算后得到的路由信息加入到本地路由表中。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
进入 视图。
(2) OSPFv3
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
过滤通过接收到的 计算出来的路由信息。
(3) LSA
filter-policy { ipv6-acl-number [ gateway prefix-list-name ] |
prefix-list prefix-list-name [ gateway prefix-list-name ] | gateway
prefix-list-name | route-policy route-policy-name } import
缺省情况下，不对通过接收到的 LSA 计算出来的路由信息进行过滤。
本命令只对 OSPFv3 计算出来的路由进行过滤，没有通过过滤的路由将不被加入到本地路由
表中，从而不能用于转发报文。

##### 1.6.4 配置过滤Inter-Area-Prefix-LSA

###### 1. 配置限制和指导

此命令只在 ABR 路由器上有效，对区域内部路由器无效。

###### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 进入 OSPFv3 区域视图。
area area-id
(4) 配置对 Inter-Area-Prefix-LSA 进行过滤。
filter { ipv6-acl-number | prefix-list prefix-list-name | route-policy route-policy-name } { export | import }缺省情况下，不对 Inter-Area-Prefix-LSA 进行过滤。

##### 1.6.5 配置OSPFv3接口的开销值

###### 1. 功能简介

有两种方式来配置接口的开销值：
OSPFv3第一种方法是在接口视图下直接配置开销值；
•

###### 1. 功能简介

第二种方法是配置接口的带宽参考值，OSPFv3 根据带宽参考值自动计算接口的开销值，计
•算公式为：接口开销＝带宽参考值（100Mbps）÷接口带宽（Mbps），当计算出来的开销值大于 65535，开销取最大值 65535；当计算出来的开销值小于 1 时，开销取最小值 1。

###### 2. 配置接口的开销值

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置 OSPFv3 接口的开销值。
ospfv3 cost cost-value [ instance instance-id ]
缺省情况下，OSPFv3根据接口的带宽自动计算链路开销，对于 VLAN接口，缺省值为 1；对
于 Loopback 接口，缺省取值为 0。

###### 3. 配置带宽参考值

(1) 进入系统视图。
system-view
(2) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 配置带宽参考值。
bandwidth-reference value
缺省情况下，带宽参考值为 100Mbps。

##### 1.6.6 配置OSPFv3最大等价路由条数

功能简介
1.
如果到一个目的地有几条开销相同的路径，可以通过等价路由负载分担来提高链路利用率。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 配置 OSPFv3 最大等价路由条数。
maximum load-balancing number
缺省情况下，OSPFv3 支持的等价路由的最大条数与系统支持最大等价路由的条数相同。

###### 1. 功能简介

##### 1.6.7 配置OSPFv3协议的优先级

功能简介
1.
由于路由器上可能同时运行多个动态路由协议，就存在各个路由协议之间路由信息共享和选择的问题。系统为每一种路由协议设置一个优先级，在不同协议发现同一条路由时，优先级高的路由将被优选。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 配置 OSPFv3 协议的路由优先级。
preference [ ase ] { preference | route-policy route-policy-name } *
缺省情况下，对于自治系统内部路由，OSPFv3 协议的路由优先级为 10；对于自治系统外部
路由，OSPFv3 协议的路由优先级为 150。

##### 1.6.8 配置OSPFv3引入外部路由

###### 1. 配置限制和指导

由于 OSPFv3 是基于链路状态的路由协议，不能直接对发布的 LSA 进行过滤，所以只能在 OSPFv3引入路由时进行过滤，只有符合条件的路由才能转换成 LSA 发布出去。

###### 2. 配置步骤

进入系统视图。
(1)
system-view进入 视图。
(2) OSPFv3 ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 引入外部路由信息。
import-route bgp4+ [ as-number ] [ allow-ibgp ] [ [ cost cost-value | inherit-cost ] | nssa-only | route-policy route-policy-name | tag tag | type type ] * import-route { direct | static } [ [ cost cost-value | inherit-cost ] | nssa-only | route-policy route-policy-name | tag tag | type type ] * import-route { isisv6 | ospfv3 | ripng } [ process-id | all-processes ] [ allow-direct | [ cost cost-value | inherit-cost ] | nssa-only | route-policy route-policy-name | tag tag | type type ] *缺省情况下，不引入外部路由信息。
执行 命令引入 路由时，未指定 参数表示只引入import-route IPv6 BGP allow-ibgp EBGP 路由；指定 allow-ibgp 参数表示将 IBGP 路由也引入，容易引起路由环路，请慎用。
(4) （可选）对引入的外部路由信息进行过滤。

filter-policy { ipv6-acl-number | prefix-list prefix-list-name } export [ bgp4+ | direct | { isisv6 | ospfv3 | ripng } [ process-id ] | static ]缺省情况下，不对引入的路由信息进行过滤。
本命令只对本设备使用 引入的路由起作用。如果没有配置import-route import-route命令来引入其它外部路由（包括不同进程的 OSPFv3 路由），则本命令失效。
(5) 配置路由引入的全局标记。
default tag tag缺省情况下，路由引入的全局标记为 1。

##### 1.6.9 配置OSPFv3引入缺省路由

###### 1. 功能简介

OSPFv3 不能通过 import-route 命令从其它协议引入缺省路由，如果想把缺省路由引入到OSPFv3 路由区域，必须要使用下面命令配置 OSPFv3 引入缺省路由。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 配置 OSPFv3 引入缺省路由。
default-route-advertise [ [ always | permit-calculate-other ] | cost
cost-value | route-policy route-policy-name | tag tag | type type ] *
缺省情况下，未引入缺省路由。
(4) 配置路由引入的全局标记。
default tag tag
缺省情况下，路由引入的全局标记为 1。

#### 1.7 配置OSPFv3定时器

##### 1.7.1 配置OSPFv3报文定时器

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置接口发送 hello 报文的时间间隔。
ospfv3 timer hello seconds [ instance instance-id ]
缺省情况下，P2P、Broadcast 网络类型接口发送 Hello 报文的时间间隔的值为 10 秒；P2MP、
NBMA 类型接口发送 Hello 报文的时间间隔为 30 秒。
(4) 配置相邻路由器间失效时间。

###### 2. 配置步骤

###### 1. 功能简介

###### 2. 配置步骤

ospfv3 timer dead seconds [ instance instance-id ]缺省情况下，P2P、Broadcast 网络类型接口的 OSPFv3 邻居失效时间为 40 秒；P2MP、类型接口的 邻居失效的时间为 秒。
NBMA OSPFv3 120相邻路由器间失效时间的值不要设置得太小，否则邻居很容易失效。
配置轮询定时器。
(5)
ospfv3 timer poll seconds [ instance instance-id ]缺省情况下，发送轮询 Hello 报文的时间间隔为 120 秒。
(6) 配置相邻路由器重传 LSA 的时间间隔。
ospfv3 timer retransmit interval [ instance instance-id ]缺省情况下，LSA 的重传时间间隔为 5 秒。
相邻路由器重传 LSA 时间间隔的值不要设置得太小，否则将会引起不必要的重传。

##### 1.7.2 配置接口的LSA传输延迟时间

功能简介
1.
LSA 在本路由器的链路状态数据库（LSDB）中会随时间老化（每秒钟加 1），但在网络的传输过程中却不会，所以有必要在发送之前将 的老化时间增加一定的延迟时间。此配置对低速率的网络LSA尤其重要。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置接口的 LSA 传输延迟时间。
ospfv3 trans-delay seconds [ instance instance-id ]缺省情况下，接口的 LSA 传输延迟时间为 1 秒。

##### 1.7.3 配置SPF计算时间间隔

###### 1. 功能简介

当 OSPFv3 的 LSDB 发生改变时，需要重新计算最短路径。如果网络频繁变化，且每次变化都立即计算最短路径，将会占用大量系统资源，并影响路由器的效率。通过调节 SPF 计算时间间隔，可以抑制由于网络频繁变化带来的影响。
本命令在网络变化不频繁的情况下将连续路由计算的时间间隔缩小到 minimum-interval，而在n-2网络变化频繁的情况下可以进行相应惩罚，增加 incremental-interval×2 （n 为连续触发路由计算的次数），将等待时间按照配置的惩罚增量延长，最大不超过 maximum-interval。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 OSPFv3 视图。

###### 1. 功能简介

###### 2. 配置步骤

ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 配置 SPF 计算时间间隔。
spf-schedule-interval maximum-interval [ minimum-interval [ incremental-interval ] ]缺省情况下，SPF 计算的最大时间间隔为 秒，最小时间间隔为 毫秒，时间间隔惩罚增量5 50为 200 毫秒。

##### 1.7.4 配置LSA重新生成的时间间隔

###### 1. 功能简介

通过调节 LSA 重新生成的时间间隔，可以抑制网络频繁变化可能导致的带宽资源和路由器资源被过多占用的问题。
本命令在网络变化不频繁的情况下将 LSA 重新生成时间间隔缩小到 minimum-interval，而在网络 变 化 频 繁 的 情 况 下 可 以 进 行 相 应 惩 罚 ， 将 等 待 时 间 按 照 配 置 的 惩 罚 增 量 延 长 ， 增 加n-2 incremental-interval × 2 （ n 为 连 续 触 发 路 由 计 算 的 次 数 ）， 最 大 不 超 过maximum-interval。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 配置 LSA 重新生成的时间间隔。
lsa-generation-interval maximum-interval [ minimum-interval [ incremental-interval ] ]缺省情况下，最大时间间隔为 5 秒，最小时间间隔为 0 毫秒，惩罚增量为 0 毫秒。

##### 1.7.5 配置接口发送LSU报文的时间间隔和一次发送LSU报文的最大个数

功能简介
1.
如果路由器路由表里的路由条目很多，在与邻居进行 LSDB 同步时，可能需要发送大量 LSU ，有可能会对当前设备和网络带宽带来影响；因此，路由器将 报文分为多个批次进行发送，并且对LSU OSPFv3 接口每次允许发送的 LSU 报文的最大个数做出限制。
用户可根据需要配置 OSPFv3 接口发送 LSU 报文的时间间隔以及接口一次发送 LSU 报文的最大个数。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 配置接口发送 LSU 报文的时间间隔和一次发送 LSU 报文的最大个数。

transmit-pacing interval interval count count缺省情况下，OSPFv3 接口发送 LSU 报文的时间间隔为 20 毫秒，一次最多发送 3 个 LSU 报文。

#### 1.8 配置接口的DR优先级

##### 1. 功能简介

路由器接口的 DR 优先级将影响接口在选举 DR 时所具有的资格，优先级为 0 的路由器不会被选举为 DR 或 BDR。

##### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置接口的 DR 优先级。
ospfv3 dr-priority priority [ instance instance-id ]缺省情况下，接口的 DR 优先级为 1。

#### 1.9 配置OSPFv3报文相关功能

##### 1.9.1 忽略DD报文中的MTU检查

###### 1. 功能简介

在 LSA 数量不多的情况下，没有必要去检查 MTU 大小，可以设置忽略 DD 报文中的 MTU 检查，从而提高性能。

###### 2. 配置限制和指导

双方的接口 MTU 必须相同才能建立邻居关系。

###### 3. 配置步骤

进入系统视图。
(1)
system-view进入接口视图。
(2)
interface interface-type interface-number
(3) 忽略 DD 报文中的 MTU 检查。
ospfv3 mtu-ignore [ instance instance-id ]缺省情况下，接口在进行 DD 报文交换时执行 MTU 检查。

###### 1. 功能简介

##### 1.9.2 禁止接口收发OSPFv3报文

功能简介
1.
当运行 OSPFv3 协议的接口被配置为 Silent 状态后，该接口的直连路由仍可以由同一路由器的其他接口通过 发布，但 报文将被阻塞，接口上不会建立 邻居Intra-Area-Prefix-LSA OSPFv3 OSPFv3关系。这一特性可以增强 OSPFv3 的组网适应能力。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 禁止接口收发 OSPFv3 报文。
silent-interface { interface-type interface-number | all }
缺省情况下，允许接口收发 OSPFv3 报文。
不同的进程可以对同一接口禁止收发 报文，但本命令只对本进程已经使能的
OSPFv3
OSPFv3 接口起作用，不对其它进程的接口起作用。

#### 1.10 配置前缀抑制

##### 1.10.1 功能简介

接口使能 OSPFv3 后，会将接口下的所有网段路由都通过 LSA 发布，但有时候网段路由是不希望被发布的。通过前缀抑制配置，可以减少 LSA 中携带不需要的前缀，即不发布某些网段路由，从而提高网络安全性，加快路由收敛。
当使能前缀抑制时，Type-8 LSA 中不发布处于抑制的接口前缀信息；对于广播网或者 NBMA 网络，DR 在生成引用 Type-2 LSA 的 Type-9 LSA 时，不发布处于抑制的接口前缀信息；对于 P2P 或 P2MP网络，生成引用 Type-1 LSA 的 Type-9 LSA 时，不发布处于抑制的接口前缀信息。

##### 1.10.2 配置限制和指导

如果需要抑制前缀发布，建议整个 OSPFv3 网络都配置本命令，否则会有互通问题。

##### 1.10.3 配置全局前缀抑制

(1) 进入系统视图。
system-view
(2) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 配置前缀抑制功能。
prefix-suppression
缺省情况下，不抑制 进程进行前缀发布。
OSPFv3
不能抑制 接口和处于 状态接口对应的前缀。
LoopBack silent-interface

##### 1.10.4 配置接口前缀抑制

进入系统视图。
(1)
system-view进入接口视图。
(2)
interface interface-type interface-number
(3) 配置接口的前缀抑制功能。
ospfv3 prefix-suppression [ disable ] [ instance instance-id ]缺省情况下，不抑制接口进行前缀发布。

#### 1.11 配置Stub路由器

##### 1. 功能简介

路由器用来控制流量，它告知其他 路由器不要使用这个 路由器来转发数据，但Stub OSPFv3 Stub可以拥有一个到 Stub 路由器的路由。
将当前路由器配置为 Stub 路由器的功能，可通过 R-bit 和 max-metric 两种模式来实现：
• R-bit 模式：通过清除该路由器发布 Type-1 LSA 中 options 域的 R-bit，使其他路由器不通过该路由器来转发数据。
• max-metric 模式：该路由器发布的 Type-1 LSA 的链路度量值将设为最大值 65535，这样其邻居计算出这条路由的开销就会很大，如果邻居上有到这个目的地址开销更小的路由，则数据不会通过这个 路由器转发。
Stub

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 配置当前路由器为 Stub 路由器。请选择其中一项进行配置。
配置当前路由器为 路由器，且发布的 中的 域的 将被清除。
Stub Type-1 LSA options R-bit
(cid:123)
stub-router r-bit [ include-stub | on-startup { seconds | wait-for-bgp
[ seconds ] } ] *
配置当前路由器为 Stub 路由器，且发布的 Type-1 LSA 的链路度量值将设置为最大值
(cid:123)
65535。
stub-router max-metric [ external-lsa [ max-metric-value ] |
summary-lsa [ max-metric-value ] | include-stub | on-startup { seconds
| wait-for-bgp [ seconds ] } ] *
缺省情况下，当前路由器没有被配置为 路由器。
Stub
路由器与 区域无关。
Stub Stub

##### 1.12.3 配置GR Restarter

##### 1.12.4 配置GR Helper

#### 1.12 配置OSPFv3 GR

##### 1.12.1 功能简介

GR（Graceful Restart，平滑重启）是一种在协议重启或主备倒换时保证转发业务不中断的机制。
GR 有两个角色：
GR Restarter：发生协议重启或主备倒换事件且具有 GR 能力的设备。
•
• GR Helper：和 GR Restarter 具有邻居关系，协助完成 GR 流程的设备。
支持 OSPFv3 的 GR Restarter 能力的设备主备倒换后，为了实现设备转发业务的不中断，它必须完成下列两项任务：
重启过程 GR Restarter 转发表项保持稳定；
•重启流程结束后重建所有邻居关系，重新获取完整的网络拓扑信息。
•设备（GR Restarter）主备倒换后，首先向邻居发送 Grace LSA 通告邻居本设备进入 GR；邻居收到 后，如果支持 能力则进入 模式（此时该邻居称为 Helper）。
Grace-LSA GR Helper Helper GR GR Restarter 重新建立邻居， GR Helper 帮助 GR Restarter 进行 LSDB 的同步。同步完成之后，GR 流程结束，进入正常的 OSPFv3 流程。这样就能实现设备在主备倒换时转发业务正常进行。

##### 1.12.2 配置限制和指导

设备充当 后不能再配置 功能。
GR Restarter OSPFv3 NSR配置GR
1.12.3 Restarter
(1) 进入系统视图。
system-view
(2) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 使能 GR 能力。
graceful-restart enable [ global | planned-only ] *缺省情况下，OSPFv3 协议的 GR Restarter 能力处于关闭状态。
(4) （可选）配置 GR 重启时间间隔。
graceful-restart interval interval缺省情况下，OSPFv3 协议的 重启间隔时间为 秒。
GR 120配置GR
1.12.4 Helper
(1) 进入系统视图。
system-view
(2) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 使能 GR Helper 能力。
graceful-restart helper enable [ planned-only ]

#### 1.13 配置OSPFv3 NSR

##### 3. 配置步骤

缺省情况下，OSPFv3 的 GR Helper 能力处于开启状态。
(4) 使能 LSA 严格检查能力。
graceful-restart helper strict-lsa-checking缺省情况下，OSPFv3 协议的 GR Helper 严格 LSA 检查能力处于关闭状态。

##### 1.12.5 以GR方式重启OSPFv3进程

###### 1. 功能简介

设备进行主备倒换或者进行如下操作均可以以 GR 方式重启 OSPFv3 进程。

###### 2. 配置步骤

请在用户视图下执行本命令，以 方式重启 进程。
GR OSPFv3 reset ospfv3 [ process-id ] process graceful-restart配置OSPFv3
1.13 NSR

##### 1. 功能简介

NSR（Nonstop Routing，不间断路由）通过将 OSPFv3 链路状态信息从主进程备份到备进程，使设备在发生主备倒换时可以自行完成链路状态的恢复和路由的重新生成，邻接关系不会发生中断，从而避免了主备倒换对转发业务的影响。
GR 特性需要周边设备配合才能完成路由信息的恢复，在网络应用中有一定的限制。NSR 特性不需要周边设备的配合，网络应用更加广泛。

##### 2. 配置限制和指导

设备配置了 OSPFv3 NSR 功能后不能再充当 GR Restarter。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 使能 OSPFv3 NSR 功能。
non-stop-routing缺省情况下，OSPFv3 NSR 功能处于关闭状态。
各个进程的 NSR功能是相互独立的，只对本进程生效。如果存在多个 OSPFv3 进程，建议在各个进程下使能 OSPFv3 NSR 功能。

#### 1.14 配置OSPFv3与BFD联动

##### 1. 功能简介

BFD（Bidirectional Detection，双向转发检测）能够为 邻居之间的链路提供Forwarding OSPFv3快速检测功能。当邻居之间的链路出现故障时，加快 OSPFv3 协议的收敛速度。关于 BFD 的介绍和基本功能配置，请参见“可靠性配置指导”中的“BFD”。

##### 2. 配置步骤

OSPFv3 使用 BFD 来进行快速故障检测时，可以通过 Hello 报文动态发现邻居，将邻居地址通知就开始建立会话。BFD 会话建立前处于 状态，此时 控制报文以不小于 秒的时间BFD down BFD 1间隔周期发送以减少控制报文流量，直到会话建立以后才会以协商的时间间隔发送以实现快速检测。
进行配置 BFD 之前，需要配置 OSPFv3 功能。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 配置路由器的 ID。
router-id router-id
(4) 退出 OSPFv3 视图。
quit
(5) 进入接口视图。
interface interface-type interface-number在接口上使能 OSPFv3。
(6)
ospfv3 process-id area area-id [ instance instance-id ]在指定接口上使能 BFD。
(7) OSPFv3 ospfv3 bfd enable [ instance instance-id ]缺省情况下，运行 的接口的 功能处于关闭状态。
OSPFv3 BFD

#### 1.15 配置OSPFv3快速重路由

##### 1.15.1 功能简介

在部署了备份链路的 OSPFv3 网络中，当主用链路发生故障时，OSPFv3 会对路由进行重新计算，在路由收敛完成后，流量可以通过备份链路进行传输。在路由收敛期间，数据流量将会被中断。
为了尽可能缩短网络故障导致的流量中断时间，网络管理员可以根据需要配置 快速重路由OSPFv3功能。
图1-1 快速重路由功能示意图OSPFv3如 图 1-1 所示，通过在Router B上使能快速重路由功能，OSPFv3 将为路由计算或指定备份下一跳，当Router B检测到主用下一跳地址无法到达时，会直接使用备份下一跳地址来指导报文的转发，从

###### 2. 配置步骤

而大大缩短了流量路径切换的时间。在快速切换流量传输路径的同时，OSPFv3 会根据变化后的网络拓扑重新计算路由，在路由收敛完毕后，使用新计算出来的最优路由来指导报文转发。
在为快速重路由功能指定备份下一跳地址时，可以采用以下两种方式：
通过 LFA（Loop Alternate）算法选取备份下一跳地址。
• Free在路由策略中指定备份下一跳，为符合过滤条件的路由指定备份下一跳地址。
•

##### 1.15.2 配置通过LFA算法选取备份下一跳

###### 1. 配置限制和指导

快速重路由功能（通过 算法选取备份下一跳信息）使能后，不能配置OSPFv3 LFA vlink-peer命令。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) （可选）禁止接口参与 LFA 计算。
ospfv3 fast-reroute lfa-backup exclude缺省情况下，接口参与 LFA 计算，有资格被选为备份接口。
(4) 退回系统视图。
quit进入 视图。
(5) OSPFv3 ospfv3 [ process-id | vpn-instance vpn-instance-name ] *配置 快速重路由功能（通过 算法选取备份下一跳信息）。
(6) OSPFv3 LFA fast-reroute lfa [ abr-only ]缺省情况下，OSPFv3 快速重路由功能处于关闭状态。
abr-only 表示只有到 ABR 设备的路由才能作为备份下一跳。

##### 1.15.3 配置通过路由策略指定备份下一跳

###### 1. 功能简介

网络管理员可以通过 命令在路由策略中指apply ipv6 fast-reroute backup-interface定备份下一跳，为符合过滤条件的路由指定备份下一跳，关于 apply ipv6 fast-reroute backup-interface 命令以及路由策略的相关配置，请参见“三层技术-IP 路由配置指导”中的“路由策略”。

###### 2. 配置步骤

进入系统视图。
(1)
system-view进入接口视图。
(2)
interface interface-type interface-number

###### 1. 功能简介

###### 2. 配置步骤

(3) （可选）禁止接口参与 LFA 计算。
ospfv3 fast-reroute lfa-backup exclude
缺省情况下，接口参与 LFA 计算，有资格被选为备份接口。
(4) 退回系统视图。
quit
(5) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(6) 配置 OSPFv3 快速重路由功能（通过路由策略指定备份下一跳）。
fast-reroute route-policy route-policy-name
缺省情况下，OSPFv3 快速重路由功能处于关闭状态。

##### 1.15.4 配置OSPFv3快速重路由支持BFD检测功能（Ctrl方式）

###### 1. 功能简介

OSPFv3 协议的快速重路由特性中，主用链路缺省不使用 BFD 进行链路故障检测。配置本功能后，将使用 BFD 进行检测，可以更快速的发现主用链路的故障，从而加快 OSPFv3 协议的收敛速度。
使用 control 报文双向检测方式时，需要建立 OSPF 邻居的两端设备均支持 BFD 配置。

###### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 使能 OSPFv3 协议中主用链路的 BFD 检测功能。
ospfv3 primary-path-detect bfd ctrl [ instance instance-id ]缺省情况下，OSPFv3 协议中主用链路的 BFD 检测功能（Ctrl 方式）处于关闭状态。

##### 1.15.5 配置OSPFv3快速重路由支持BFD检测功能（Echo方式）

功能简介
1.
OSPFv3 协议的快速重路由特性中，主用链路缺省不使用 BFD 进行链路故障检测。配置本功能后，将使用 进行检测，可以更快速的发现主用链路的故障，从而加快 协议的收敛速度。
BFD OSPFv3使用 echo 报文单跳检测方式时，仅需要一端设备支持 BFD 配置。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 配置 BFD Echo 报文源地址。
bfd echo-source-ipv6 ipv6-address缺省情况下，未配置 BFD Echo 报文源地址。
echo 报文的源 IPv6 地址用户可以任意指定。建议配置 echo 报文的源 IPv6 地址不属于该设备任何一个接口所在网段。

本命令的详细情况请参见“可靠性命令参考”中的“BFD”。
(3) 进入接口视图。
interface interface-type interface-number
(4) 使能 OSPFv3 协议中主用链路的 BFD 检测功能。
ospfv3 primary-path-detect bfd echo [ instance instance-id ]缺省情况下，OSPFv3 协议中主用链路的 BFD 检测功能（Echo 方式）处于关闭状态。

#### 1.16 配置OSPFv3安全功能

##### 1.16.1 配置OSPFv3验证

###### 1. 功能简介

从安全性角度来考虑，为了避免路由信息外泄或者 OSPFv3 路由器受到恶意攻击，OSPFv3 提供基于 keychain 的报文验证功能。
配置 OSPFv3 验证后， OSPFv3 路由器建立邻居关系时，在发送的报文中会携带验证字段，在接收报文时会进行验证，只有通过验证的报文才能接收，否则将不会接收报文，不能正常建立邻居。

###### 2. 配置限制和指导

接口视图下配置的验证模式，其优先级高于 区域视图下配置的验证模式。
OSPFv3

###### 3. 配置区域验证

(1) 进入系统视图。
system-view
进入 视图。
(2) OSPFv3
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
进入 区域视图。
(3) OSPFv3
area area-id
(4) 配置 OSPFv3 区域的验证模式。
authentication-mode keychain keychain-name
缺省情况下，未配置区域验证模式。
关于 keychain 功能的介绍，请参见“安全配置指导”中的“ keychain ”。

###### 4. 配置接口验证

进入系统视图。
(1)
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置 OSPFv3 接口的验证模式。
ospfv3 authentication-mode keychain keychain-name [ instance instance-id ]缺省情况下，接口不对 报文进行验证。
OSPFv3关于 keychain 功能的介绍，请参见“安全配置指导”中的“keychain”。

###### 1. 功能简介

##### 1.16.2 应用IPsec安全框架保护OSPFv3报文

功能简介
1.
从安全性角度来考虑，为了避免路由信息外泄或者对设备进行恶意攻击，OSPFv3 提供基于 IPsec的报文验证功能。IPsec 安全框架的具体情况请参见“安全配置指导”中的“IPsec”。
设备在发送的报文中会携带配置好的 IPsec 安全框架的 SPI（Security Parameter Index，安全参数索引）值，接收报文时通过 SPI 值进行 IPsec 安全框架匹配：只有能够匹配的报文才能接收；否则将不会接收报文，从而不能正常建立邻居和学习路由。

###### 2. 配置限制和指导

OSPFv3 支持在区域、接口、虚连接和伪连接下配置 IPsec 安全框架。
• 当需要保护区域内的所有报文时，可以在区域下配置 IPsec 安全框架，此时区域内所有路由器都需要配置相同的 安全框架。
IPsec当需要保护区域下某些接口的报文时，可以在接口下配置 IPsec 安全框架，此时直连邻居接
•口需要配置相同的 IPsec 安全框架。
当需要保护虚连接的报文时，可以配置虚连接应用 安全框架，此时虚连接上的两个邻
• IPsec居需要配置相同的 IPsec 安全框架。
当接口和接口所在区域均配置了 IPsec 安全框架时，接口下的生效；当虚连接和区域 0 均配置了IPsec 安全框架时，虚连接的生效。

###### 3. 在OSPFv3区域上应用IPsec安全框架

(1) 进入系统视图。
system-view
(2) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 进入 OSPFv3 区域视图。
area area-id
(4) 配置 OSPFv3 区域应用 IPsec 安全框架。
enable ipsec-profile profile-name
缺省情况下，OSPFv3 区域没有应用 IPsec 安全框架。

###### 4. 在OSPFv3接口上应用IPsec安全框架

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置使能了 OSPFv3 的接口上应用 IPsec 安全框架。
ospfv3 ipsec-profile profile-name [ instance instance-id ]
缺省情况下，OSPFv3 接口没有应用 IPsec 安全框架。

###### 5. 在OSPFv3虚连接上应用IPsec安全框架

(1) 进入系统视图。

###### 1. 功能简介

system-view
(2) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 进入 OSPFv3 区域视图。
area area-id
(4) 配置 OSPFv3 虚连接应用 IPsec 安全框架。
vlink-peer router-id [ dead seconds | hello seconds | instance instance-id | ipsec-profile profile-name | keychain keychain-name | retransmit seconds | trans-delay seconds ] *缺省情况下，OSPFv3 虚连接没有应用 安全框架。
IPsec

#### 1.17 配置OSPFv3日志和告警功能

##### 1.17.1 配置邻居状态变化的输出开关

功能简介
1.
打开邻居状态变化的输出开关后，OSPFv3 邻居状态变化时会生成日志信息发送到设备的信息中心，通过设置信息中心的参数，最终决定日志信息的输出规则（即是否允许输出以及输出方向）。（有关信息中心参数的配置请参见“网络管理和监控配置指导”中的“信息中心”。）

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 配置邻居状态变化的输出开关。
log-peer-change
缺省情况下，邻居状态变化的输出开关处于打开状态。

##### 1.17.2 配置OSPFv3的日志信息个数

###### 1. 功能简介

OSPFv3 的日志信息包括路由计算、邻居和 LSA 老化的日志信息。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(3) 配置保存 OSPFv3 的日志信息的最大个数。
event-log { lsa-flush | peer | spf } size count
缺省情况下，路由计算、邻居和 LSA 老化的日志信息个数均为 10 个。

###### 1. 功能简介

##### 1.17.3 配置OSPFv3网管功能

功能简介
1.
配置 OSPFv3 进程绑定 MIB 功能后，可以通过网管软件对指定的 OSPFv3 进程进行管理。
开启 OSPFv3 模块的告警功能后，该模块会生成告警信息，用于报告该模块的重要事件。生成的告警信息将发送到设备的 SNMP 模块，通过设置 SNMP 中告警信息的发送参数，来决定告警信息输出的相关属性。（有关告警信息的详细介绍，请参见“网络管理和监控配置指导”中的“SNMP”。）
通过调整 在指定时间间隔内允许输出的告警信息条数，可以避免网络出现大量告警信息时OSPFv3对资源的消耗。
OSPFv3 使用 MIB（Management Information Base，管理信息库）为 NMS（Network Management System，网络管理系统）提供对 OSPFv3 实例的管理，但标准 OSPFv3 MIB 中定义的 MIB 为单实例管理对象，无法对多个 实例进行管理。因此，参考 中对 多实例的管OSPFv3 RFC 4750 OSPF理方法，为管理 OSPFv3 的 SNMP 实体定义一个上下文名称，以此来区分不同的 OSPFv3 实例，实现对多个 OSPFv3 实例进行管理。由于上下文名称只是 SNMPv3 独有的概念，对于 SNMPv1/v2c，会将团体名映射为上下文名称以对不同协议进行区分。

###### 2. 配置步骤

进入系统视图。
(1)
system-view配置 进程绑定 MIB。
(2) OSPFv3 ospfv3 mib-binding process-id缺省情况下，MIB 绑定在进程号最小的 OSPFv3 进程上。
(3) 开启 OSPFv3 的告警功能。
snmp-agent trap enable ospfv3 [ grrestarter-status-change | grhelper-status-change | if-state-change | if-cfg-error | if-bad-pkt | neighbor-state-change | nssatranslator-status-change | virtif-bad-pkt | virtif-cfg-error |virtif-state-change | virtgrhelper-status-change | virtneighbor-state-chang ] *缺省情况下，OSPFv3 的告警功能处于开启状态。
(4) 进入 OSPFv3 视图。
ospfv3 [ process-id | vpn-instance vpn-instance-name ] *
(5) 配置管理 OSPFv3 的 SNMP 实体所使用的上下文名称。
snmp context-name context-name缺省情况下，未配置管理 OSPFv3 的 SNMP 实体所使用的上下文名称。
(6) （可选）配置 OSPFv3 在指定时间间隔内允许输出的告警信息条数。
snmp trap rate-limit interval trap-interval count trap-number缺省情况下，OSPFv3 模块在 10 秒内允许输出 7 条告警信息。

#### 1.18 OSPFv3显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 OSPFv3 的运行情况，通过查看显示信息验证配置的效果。
在用户视图下执行 reset 命令可以清除 OSPFv3 的统计信息、重启 OSPFv3 进程或者重新向OSPFv3 引入外部路由。
表1-1 OSPFv3 显示和维护操作 命令display ospfv3 [ process-id ] [ area area-id ]显示OSPFv3的ABR聚合信息abr-summary [ ipv6-address prefix-length ] [ verbose ] display ospfv3 area peer [ process-id ] [ area-id ]显示OSPFv3邻居信息 [ [ interface-type interface-number ] [ verbose ] | peer-router-id | statistics ] display ospfv3 [ process-id ] [ area area-id ]显示 OSPFv3 请求列表的信息 request-queue [ interface-type interface-number ] [ neighbor-id ] display ospfv3 [ process-id ] [ area area-id ]显示OSPFv3重传列表的信息 retrans-queue [ interface-type interface-number ] [ neighbor-id ] display ospfv3 [ process-id ] [ area area-id ] spf-tree显示OSPFv3区域的拓扑信息[ verbose ] display ospfv3 [ process-id ] [ verbose ]显示OSPFv3的进程信息显示到OSPFv3的区域边界路由器和自display ospfv3 [ process-id ] abr-asbr治系统边界路由器的路由信息display ospfv3 [ process-id ] asbr-summary显示OSPFv3的ASBR聚合信息[ ipv6-address prefix-length ] [ verbose ] display ospfv3 [ process-id ] event-log { lsa-flush |显示OSPFv3路由计算的日志信息peer | spf } display ospfv3 [ process-id ] graceful-restart显示OSPFv3进程的GR状态信息[ verbose ] display ospfv3 [ process-id ] interface显示OSPFv3的接口信息[ interface-type interface-number | verbose ] display ospfv3 [ process-id ] lsdb [ { external | grace | inter-prefix | inter-router | intra-prefix | link |显示OSPFv3的链路状态数据库信息 network | nssa | router | unknown [ type ] } [ link-state-id ] [ originate-router router-id | self-originate ] | statistics | total | verbose ]显示OSPFv3的路由下一跳信息 display ospfv3 [ process-id ] nexthop显示OSPFv3进程的NSR状态信息 display ospfv3 [ process-id ] non-stop-routing display ospfv3 [ process-id ] routing [ ipv6-address显示OSPFv3路由表信息prefix-length ]显示OSPFv3的报文统计信息 display ospfv3 [ process-id ] statistics [ error ]显示OSPFv3的虚连接信息 display ospfv3 [ process-id ] vlink reset ospfv3 [ process-id ] event-log [ lsa-flush |清除OSPFv3的日志信息peer | spf ]

操作 命令reset ospfv3 [ process-id ] process重启OSPFv3进程[ graceful-restart ]重新向OSPFv3引入外部路由 reset ospfv3 [ process-id ] redistribution清除OSPFv3的统计信息 reset ospfv3 [ process-id ] statistics

#### 1.19 OSPFv3配置举例

##### 1.19.1 OSPFv3 Stub区域配置举例

###### 1. 组网需求

所有的交换机都运行 OSPFv3，整个自治系统划分为 个区域。其中 和 作
• 3 Switch B Switch C为 ABR 来转发区域之间的路由。
• 要求将 Area 2 配置为 Stub 区域，减少通告到此区域内的 LSA 数量，但不影响路由的可达性。

###### 2. 组网图

图1-2 OSPFv3 Stub 区域配置组网图

###### 3. 配置步骤

(1) 配置各接口的 IPv6 地址（略）
配置 基本功能
(2) OSPFv3
配置 A，启动 OSPFv3，并配置其 为 1.1.1.1。
\# Switch Router ID
<SwitchA> system-view
[SwitchA] ospfv3
[SwitchA-ospfv3-1] router-id 1.1.1.1
[SwitchA-ospfv3-1] quit
[SwitchA] interface vlan-interface 300
[SwitchA-Vlan-interface300] ospfv3 1 area 1
[SwitchA-Vlan-interface300] quit
[SwitchA] interface vlan-interface 200

[SwitchA-Vlan-interface200] ospfv3 1 area 1 [SwitchA-Vlan-interface200] quit \# 配置 Switch B，启动 OSPFv3，并配置其 Router ID 为 2.2.2.2。
<SwitchB> system-view [SwitchB] ospfv3 [SwitchB-ospfv3-1] router-id 2.2.2.2 [SwitchB-ospfv3-1] quit [SwitchB] interface vlan-interface 100 [SwitchB-Vlan-interface100] ospfv3 1 area 0 [SwitchB-Vlan-interface100] quit [SwitchB] interface vlan-interface 200 [SwitchB-Vlan-interface200] ospfv3 1 area 1 [SwitchB-Vlan-interface200] quit \# 配置 Switch C，启动 OSPFv3，并配置其 Router ID 为 3.3.3.3。
<SwitchC> system-view [SwitchC] ospfv3 [SwitchC-ospfv3-1] router-id 3.3.3.3 [SwitchC-ospfv3-1] quit [SwitchC] interface vlan-interface 100 [SwitchC-Vlan-interface100] ospfv3 1 area 0 [SwitchC-Vlan-interface100] quit [SwitchC] interface vlan-interface 400 [SwitchC-Vlan-interface400] ospfv3 1 area 2 [SwitchC-Vlan-interface400] quit \# 配置 Switch D，启动 OSPFv3，并配置其 Router ID 为 4.4.4.4。
<SwitchD> system-view [SwitchD] ospfv3 [SwitchD-ospfv3-1] router-id 4.4.4.4 [SwitchD-ospfv3-1] quit [SwitchD] interface vlan-interface 400 [SwitchD-Vlan-interface400] ospfv3 1 area 2 [SwitchD-Vlan-interface400] quit查看 的 邻居状态。
\# Switch B OSPFv3 [SwitchB] display ospfv3 peer OSPFv3 Process 1 with Router ID 2.2.2.2 Area: 0.0.0.0
------------------------------------------------------------------------- Router ID Pri State Dead-Time InstID Interface
3.3.3.3 1 Full/BDR 00:00:40 0 Vlan100 Area: 0.0.0.1
------------------------------------------------------------------------- Router ID Pri State Dead-Time InstID Interface
1.1.1.1 1 Full/DR 00:00:40 0 Vlan200 \# 查看 Switch C 的 OSPFv3 邻居状态。

[SwitchC] display ospfv3 peer OSPFv3 Process 1 with Router ID 3.3.3.3 Area: 0.0.0.0
------------------------------------------------------------------------- Router ID Pri State Dead-Time InstID Interface
2.2.2.2 1 Full/DR 00:00:40 0 Vlan100 Area: 0.0.0.2
------------------------------------------------------------------------- Router ID Pri State Dead-Time InstID Interface
4.4.4.4 1 Full/BDR 00:00:40 0 Vlan400 \# 查看 Switch D 的 OSPFv3 路由表信息。
[SwitchD] display ospfv3 routing OSPFv3 Process 1 with Router ID 4.4.4.4
------------------------------------------------------------------------- I - Intra area route, E1 - Type 1 external route, N1 - Type 1 NSSA route IA - Inter area route, E2 - Type 2 external route, N2 - Type 2 NSSA route
* - Selected route
*Destination: 2001::/64 Type : IA Area : 0.0.0.2 AdvRouter : 3.3.3.3 Preference : 10 NibID : 0x23000004 Cost : 2 Interface : Vlan400 BkInterface: N/A Nexthop : FE80::48C0:26FF:FEDA:305 BkNexthop : N/A Status : Rely
*Destination: 2001:1::/64 Type : IA Area : 0.0.0.2 AdvRouter : 3.3.3.3 Preference : 10 NibID : 0x23000004 Cost : 3 Interface : Vlan400 BkInterface: N/A Nexthop : FE80::48C0:26FF:FEDA:305 BkNexthop : N/A Status : Rely
*Destination: 2001:2::/64 Type : I Area : 0.0.0.2 AdvRouter : 4.4.4.4 Preference : 10 NibID : 0x23000002 Cost : 1 Interface : Vlan400 BkInterface: N/A Nexthop : ::
BkNexthop : N/A Status : Direct

*Destination: 2001:3::1/128
Type : IA Area : 0.0.0.2
AdvRouter : 3.3.3.3 Preference : 10
NibID : 0x23000004 Cost : 3
Interface : Vlan400 BkInterface: N/A
Nexthop : FE80::48C0:26FF:FEDA:305
BkNexthop : N/A
Status : Rely
Total: 4
Intra area: 1 Inter area: 3 ASE: 0 NSSA: 0
(3) 配置 Stub 区域
\# 配置 Switch D 的 Stub 区域。
[SwitchD] ospfv3
[SwitchD-ospfv3-1] area 2
[SwitchD-ospfv3-1-area-0.0.0.2] stub
\# 配置 Switch C 的 Stub 区域，设置发送到 Stub 区域的缺省路由的开销为 10。
[SwitchC] ospfv3
[SwitchC-ospfv3-1] area 2
[SwitchC-ospfv3-1-area-0.0.0.2] stub
[SwitchC-ospfv3-1-area-0.0.0.2] default-cost 10
\# 查看 Switch D 的 OSPFv3 路由表信息，可以看到路由表中多了一条缺省路由，它的开销值
为直连路由的开销和所配置的开销值之和。
[SwitchD] display ospfv3 routing
OSPFv3 Process 1 with Router ID 4.4.4.4
-------------------------------------------------------------------------
I - Intra area route, E1 - Type 1 external route, N1 - Type 1 NSSA route
IA - Inter area route, E2 - Type 2 external route, N2 - Type 2 NSSA route
* - Selected route
*Destination: ::/0
Type : IA Area : 0.0.0.2
AdvRouter : 3.3.3.3 Preference : 10
NibID : 0x23000003 Cost : 11
Interface : Vlan400 BkInterface: N/A
Nexthop : FE80::48C0:26FF:FEDA:305
BkNexthop : N/A
Status : Rely
*Destination: 2001::/64
Type : IA Area : 0.0.0.2
AdvRouter : 3.3.3.3 Preference : 10
NibID : 0x23000003 Cost : 2
Interface : Vlan400 BkInterface: N/A
Nexthop : FE80::48C0:26FF:FEDA:305

BkNexthop : N/A Status : Rely
*Destination: 2001:1::/64 Type : IA Area : 0.0.0.2 AdvRouter : 3.3.3.3 Preference : 10 NibID : 0x23000003 Cost : 3 Interface : Vlan400 BkInterface: N/A Nexthop : FE80::48C0:26FF:FEDA:305 BkNexthop : N/A Status : Rely
*Destination: 2001:2::/64 Type : I Area : 0.0.0.2 AdvRouter : 4.4.4.4 Preference : 10 NibID : 0x23000001 Cost : 1 Interface : Vlan400 BkInterface: N/A Nexthop : ::
BkNexthop : N/A Status : Direct
*Destination: 2001:3::1/128 Type : IA Area : 0.0.0.2 AdvRouter : 3.3.3.3 Preference : 10 NibID : 0x23000003 Cost : 3 Interface : Vlan400 BkInterface: N/A Nexthop : FE80::48C0:26FF:FEDA:305 BkNexthop : N/A Status : Rely Total: 5 Intra area: 1 Inter area: 4 ASE: 0 NSSA: 0
(4) 配置 Totally Stub 区域配置 C，设置 为 区域。
\# Switch Area 2 Totally Stub [SwitchC-ospfv3-1-area-0.0.0.2] stub no-summary \# 查看 Switch D 的 OSPFv3 路由表，可以发现路由表项数目减少了，其他非直连路由都被抑制，只有缺省路由被保留。
[SwitchD] display ospfv3 routing OSPFv3 Process 1 with Router ID 4.4.4.4
------------------------------------------------------------------------- I - Intra area route, E1 - Type 1 external route, N1 - Type 1 NSSA route IA - Inter area route, E2 - Type 2 external route, N2 - Type 2 NSSA route
* - Selected route
*Destination: ::/0 Type : IA Area : 0.0.0.2

###### 2. 组网图

AdvRouter : 3.3.3.3 Preference : 10 NibID : 0x23000003 Cost : 11 Interface : Vlan400 BkInterface: N/A Nexthop : FE80::48C0:26FF:FEDA:305 BkNexthop : N/A Status : Rely
*Destination: 2001:2::/64 Type : I Area : 0.0.0.2 AdvRouter : 4.4.4.4 Preference : 10 NibID : 0x23000001 Cost : 1 Interface : Vlan400 BkInterface: N/A Nexthop : ::
BkNexthop : N/A Status : Direct Total: 2 Intra area: 1 Inter area: 1 ASE: 0 NSSA: 0

##### 1.19.2 OSPFv3 NSSA区域配置举例

###### 1. 组网需求

所有的交换机都运行 OSPFv3，整个自治系统划分为 个区域。其中 和 作
• 3 Switch B Switch C为 ABR 来转发区域之间的路由。
• 要求将 Area 1 配置为 NSSA 区域，同时将 Switch A 配置为 ASBR 引入外部路由（静态路由），且路由信息可正确的在 AS 内传播。
组网图
2.
图1-3 OSPFv3 NSSA 区域配置组网图

###### 3. 配置步骤

配置各接口的 地址（略）
(1) IPv6配置OSPFv3 基本功能（同前例 Stub区域配置举例）
(2) 1.19.1 OSPFv3配置 为 区域
(3) Area 1 NSSA

\# 配置 Switch A 的 NSSA 区域。
[SwitchA] ospfv3 [SwitchA-ospfv3-1] area 1 [SwitchA-ospfv3-1-area-0.0.0.1] nssa [SwitchA-ospfv3-1-area-0.0.0.1] quit [SwitchA-ospfv3-1] quit配置 的 区域。
\# Switch B NSSA [SwitchB] ospfv3 [SwitchB-ospfv3-1] area 1 [SwitchB-ospfv3-1-area-0.0.0.1] nssa [SwitchB-ospfv3-1-area-0.0.0.1] quit [SwitchB-ospfv3-1] quit \# 查看 Switch D 的 OSPFv3 路由表信息。
[SwitchD] display ospfv3 1 routing OSPFv3 Process 1 with Router ID 4.4.4.4
------------------------------------------------------------------------- I - Intra area route, E1 - Type 1 external route, N1 - Type 1 NSSA route IA - Inter area route, E2 - Type 2 external route, N2 - Type 2 NSSA route
* - Selected route
*Destination: 2001::/64 Type : IA Area : 0.0.0.2 AdvRouter : 3.3.3.3 Preference : 10 NibID : 0x23000003 Cost : 2 Interface : Vlan200 BkInterface: N/A Nexthop : FE80::48C0:26FF:FEDA:305 BkNexthop : N/A Status : Rely
*Destination: 2001:1::/64 Type : IA Area : 0.0.0.2 AdvRouter : 3.3.3.3 Preference : 10 NibID : 0x23000003 Cost : 3 Interface : Vlan200 BkInterface: N/A Nexthop : FE80::48C0:26FF:FEDA:305 BkNexthop : N/A Status : Rely
*Destination: 2001:2::/64 Type : I Area : 0.0.0.2 AdvRouter : 4.4.4.4 Preference : 10 NibID : 0x23000001 Cost : 1 Interface : Vlan200 BkInterface: N/A Nexthop : ::
BkNexthop : N/A Status : Direct

*Destination: 2001:3::/64
Type : IA Area : 0.0.0.2
AdvRouter : 3.3.3.3 Preference : 10
NibID : 0x23000003 Cost : 4
Interface : Vlan200 BkInterface: N/A
Nexthop : FE80::48C0:26FF:FEDA:305
BkNexthop : N/A
Status : Rely
Total: 4
Intra area: 1 Inter area: 3 ASE: 0 NSSA: 0
(4) 配置 Switch A 引入静态路由
配置 上的静态路由，并配置 引入静态路由。
\# Switch A OSPFv3
[SwitchA] ipv6 route-static 1234:: 64 null 0
[SwitchA] ospfv3 1
[SwitchA-ospfv3-1] import-route static
[SwitchA-ospfv3-1] quit
\# 查看 Switch D 的 OSPFv3 路由表，可以看到 NSSA 区域引入的一条 AS 外部的路由。
[SwitchD] display ospfv3 1 routing
OSPFv3 Process 1 with Router ID 4.4.4.4
-------------------------------------------------------------------------
I - Intra area route, E1 - Type 1 external route, N1 - Type 1 NSSA route
IA - Inter area route, E2 - Type 2 external route, N2 - Type 2 NSSA route
* - Selected route
*Destination: 2001::/64
Type : IA Area : 0.0.0.2
AdvRouter : 3.3.3.3 Preference : 10
NibID : 0x23000002 Cost : 2
Interface : Vlan400 BkInterface: N/A
Nexthop : FE80::48C0:26FF:FEDA:305
BkNexthop : N/A
Status : Rely
*Destination: 2001:1::/64
Type : IA Area : 0.0.0.2
AdvRouter : 3.3.3.3 Preference : 10
NibID : 0x23000002 Cost : 3
Interface : Vlan400 BkInterface: N/A
Nexthop : FE80::48C0:26FF:FEDA:305
BkNexthop : N/A
Status : Rely
*Destination: 2001:2::/64
Type : I Area : 0.0.0.2
AdvRouter : 4.4.4.4 Preference : 10
NibID : 0x23000004 Cost : 1

###### 1. 组网需求

Interface : Vlan400 BkInterface: N/A Nexthop : ::
BkNexthop : N/A Status : Direct
*Destination: 2001:3::/64 Type : IA Area : 0.0.0.2 AdvRouter : 3.3.3.3 Preference : 10 NibID : 0x23000002 Cost : 4 Interface : Vlan400 BkInterface: N/A Nexthop : FE80::48C0:26FF:FEDA:305 BkNexthop : N/A Status : Rely
*Destination: 1234::/64 Type : E2 Tag : 1 AdvRouter : 2.2.2.2 Preference : 150 NibID : 0x23000001 Cost : 1 Interface : Vlan400 BkInterface: N/A Nexthop : FE80::48C0:26FF:FEDA:305 BkNexthop : N/A Status : Normal Total: 5 Intra area: 1 Inter area: 3 ASE: 1 NSSA: 0

##### 1.19.3 OSPFv3的DR选择配置举例

组网需求
1.
• Switch A 的优先级配置为 100，它是网络上的最高优先级，所以 Switch A 被选为 DR；
• Switch C 的优先级配置为 2，它是优先级次高的，被选为 BDR；
• Switch B 的优先级配置为 0，这意味着它将无法成为 DR；
• Switch D 没有配置优先级，取缺省值 1。

###### 2. 组网图

图1-4 OSPFv3 的 DR 选择配置组网图

###### 3. 配置步骤

(1) 配置各接口的 IPv6 地址（略）
(2) 配置 OSPFv3 基本功能
\# 配置 Switch A，启动 OSPFv3，并配置其 Router ID 为 1.1.1.1。
<SwitchA> system-view
[SwitchA] ospfv3
[SwitchA-ospfv3-1] router-id 1.1.1.1
[SwitchA-ospfv3-1] quit
[SwitchA] interface vlan-interface 100
[SwitchA-Vlan-interface100] ospfv3 1 area 0
[SwitchA-Vlan-interface100] quit
\# 配置 Switch B，启动 OSPFv3，并配置其 Router ID 为 2.2.2.2。
<SwitchB> system-view
[SwitchB] ospfv3
[SwitchB-ospfv3-1] router-id 2.2.2.2
[SwitchB-ospfv3-1] quit
[SwitchB] interface vlan-interface 200
[SwitchB-Vlan-interface200] ospfv3 1 area 0
[SwitchB-Vlan-interface200] quit
配置 C，启动 OSPFv3，并配置其 为 3.3.3.3。
\# Switch Router ID
<SwitchC> system-view
[SwitchC] ospfv3
[SwitchC-ospfv3-1] router-id 3.3.3.3
[SwitchC-ospfv3-1] quit
[SwitchC] interface vlan-interface 100
[SwitchC-Vlan-interface100] ospfv3 1 area 0
[SwitchC-Vlan-interface100] quit
\# 配置 Switch D，启动 OSPFv3，并配置其 Router ID 为 4.4.4.4。
<SwitchD> system-view
[SwitchD] ospfv3
[SwitchD-ospfv3-1] router-id 4.4.4.4

[SwitchD-ospfv3-1] quit [SwitchD] interface vlan-interface 200 [SwitchD-Vlan-interface200] ospfv3 1 area 0 [SwitchD-Vlan-interface200] quit \# 查看 Switch A 的邻居信息，可以看到 DR 优先级（缺省为 1）以及邻居状态，此时优先级相等，Router ID 大者被选为 DR，可以看到 Switch D 为 DR，Switch C 为 BDR。
[SwitchA] display ospfv3 peer OSPFv3 Process 1 with Router ID 1.1.1.1 Area: 0.0.0.0
------------------------------------------------------------------------- Router ID Pri State Dead-Time InstID Interface
2.2.2.2 1 2-Way/DROther 00:00:36 0 Vlan200
3.3.3.3 1 Full/BDR 00:00:35 0 Vlan100
4.4.4.4 1 Full/DR 00:00:33 0 Vlan200 \# 查看 Switch D 的邻居信息，可以看到 Switch D 和其他邻居之间的邻居状态都为 Full。
[SwitchD] display ospfv3 peer OSPFv3 Process 1 with Router ID 4.4.4.4 Area: 0.0.0.0
------------------------------------------------------------------------- Router ID Pri State Dead-Time InstID Interface
1.1.1.1 1 Full/DROther 00:00:30 0 Vlan100
2.2.2.2 1 Full/DROther 00:00:37 0 Vlan200
3.3.3.3 1 Full/BDR 00:00:31 0 Vlan100配置接口的 优先级
(3) DR配置 的接口 的 优先级为 100。
\# Switch A Vlan-interface100 DR [SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] ospfv3 dr-priority 100 [SwitchA-Vlan-interface100] quit配置 的接口 的 优先级为 0。
\# Switch B Vlan-interface200 DR [SwitchB] interface vlan-interface 200 [SwitchB-Vlan-interface200] ospfv3 dr-priority 0 [SwitchB-Vlan-interface200] quit \# 配置 Switch C 的接口 Vlan-interface100 的 DR 优先级为 2。
[SwitchC] interface vlan-interface 100 [SwitchC-Vlan-interface100] ospfv3 dr-priority 2 [SwitchC-Vlan-interface100] quit \# 显示 Switch A 的邻居信息，可以看到 DR 优先级已经更新，但 DR/BDR 并未改变。
[SwitchA] display ospfv3 peer OSPFv3 Process 1 with Router ID 1.1.1.1 Area: 0.0.0.0

-------------------------------------------------------------------------
Router ID Pri State Dead-Time InstID Interface
2.2.2.2 0 2-Way/DROther 00:00:36 0 Vlan200
3.3.3.3 2 Full/BDR 00:00:35 0 Vlan200
4.4.4.4 1 Full/DR 00:00:33 0 Vlan200
\# 显示 Switch D 的邻居信息，可以看到 Switch D 仍然为 DR。
[SwitchD] display ospfv3 peer
OSPFv3 Process 1 with Router ID 4.4.4.4
Area: 0.0.0.0
-------------------------------------------------------------------------
Router ID Pri State Dead-Time InstID Interface
1.1.1.1 100 Full/DROther 00:00:30 0 Vlan100
2.2.2.2 0 Full/DROther 00:00:37 0 Vlan200
3.3.3.3 2 Full/BDR 00:00:31 0 Vlan100
(4) 重新进行 DR/BDR 选择
\# 将所有接口进行一次 shutdown 和 undo shutdown，使 OSPFv3 进行 DR/BDR 的重新选
举。
查看 的邻居信息，可以看到 为 BDR。
\# Switch A Switch C
[SwitchA] display ospfv3 peer
OSPFv3 Process 1 with Router ID 1.1.1.1
Area: 0.0.0.0
-------------------------------------------------------------------------
Router ID Pri State Dead-Time InstID Interface
2.2.2.2 0 Full/DROther 00:00:36 0 Vlan200
3.3.3.3 2 Full/BDR 00:00:35 0 Vlan100
4.4.4.4 1 Full/DROther 00:00:33 0 Vlan200
\# 查看 Switch D 的邻居信息，可以看到 Switch A 为 DR。
[SwitchD] display ospfv3 peer
OSPFv3 Process 1 with Router ID 4.4.4.4
Area: 0.0.0.0
-------------------------------------------------------------------------
Router ID Pri State Dead-Time InstID Interface
1.1.1.1 100 Full/DR 00:00:30 0 Vlan100
2.2.2.2 0 2-Way/DROther 00:00:37 0 Vlan200
3.3.3.3 2 Full/BDR 00:00:31 0 Vlan100

##### 1.19.4 OSPFv3引入外部路由配置举例

###### 1. 组网需求

• Switch A、Switch B 和 Switch C 位于 Area 2 内；

###### 3. 配置步骤

Switch B 上运行两个 OSPFv3 进程：OSPFv3 1 和 OSPFv3 2。Switch B 通过 OSPFv3 1 和
•交换路由信息，通过 和 交换路由信息；
Switch A OSPFv3 2 Switch C在 上配置 进程 引入外部路由，引入直连路由和 进程 的路由，
• Switch B OSPFv3 2 OSPFv3 1并将引入的外部路由的开销值设置为 3，使得 Switch C 能够学习到达 1::0/64 和 2::0/64 的路由，但 Switch A 不能学习到达 3::0/64 和 4::0/64 的路由。

###### 2. 组网图

图1-5 OSPFv3 引入外部路由配置组网图配置步骤
3.
(1) 配置各接口的 IPv6 地址（略）
(2) 配置 OSPFv3 \# 在 Switch A 上启动 OSPFv3 进程 1。
<SwitchA> system-view [SwitchA] ospfv3 1 [SwitchA-ospfv3-1] router-id 1.1.1.1 [SwitchA-ospfv3-1] quit [SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] ospfv3 1 area 2 [SwitchA-Vlan-interface100] quit [SwitchA] interface vlan-interface 200 [SwitchA-Vlan-interface200] ospfv3 1 area 2 [SwitchA-Vlan-interface200] quit \# 在 Switch B 上启动两个 OSPFv3 进程，进程号分别为 1 和 2。
<SwitchB> system-view [SwitchB] ospfv3 1 [SwitchB-ospfv3-1] router-id 2.2.2.2 [SwitchB-ospfv3-1] quit [SwitchB] interface vlan-interface 100 [SwitchB-Vlan-interface100] ospfv3 1 area 2 [SwitchB-Vlan-interface100] quit [SwitchB] ospfv3 2 [SwitchB-ospfv3-2] router-id 3.3.3.3 [SwitchB-ospfv3-2] quit [SwitchB] interface vlan-interface 300 [SwitchB-Vlan-interface300] ospfv3 2 area 2

[SwitchB-Vlan-interface300] quit \# 在 Switch C 上启动 OSPFv3 进程 2。
<SwitchC> system-view [SwitchC] ospfv3 2 [SwitchC-ospfv3-2] router-id 4.4.4.4 [SwitchC-ospfv3-2] quit [SwitchC] interface vlan-interface 300 [SwitchC-Vlan-interface300] ospfv3 2 area 2 [SwitchC-Vlan-interface300] quit [SwitchC] interface vlan-interface 400 [SwitchC-Vlan-interface400] ospfv3 2 area 2 [SwitchC-Vlan-interface400] quit查看 的路由表信息。
\# Switch C [SwitchC] display ipv6 routing-table Destinations : 7 Routes : 7 Destination: ::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: 3::/64 Protocol : Direct NextHop : :: Preference: 0 Interface : Vlan300 Cost : 0 Destination: 3::2/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: 4::/64 Protocol : Direct NextHop : :: Preference: 0 Interface : Vlan400 Cost : 0 Destination: 4::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: FE80::/10 Protocol : Direct NextHop : :: Preference: 0 Interface : NULL0 Cost : 0 Destination: FF00::/8 Protocol : Direct NextHop : :: Preference: 0 Interface : NULL0 Cost : 0
(3) 配置 OSPFv3 引入外部路由\# 在 Switch B 上配置 OSPFv3 引入外部路由，引入直连路由和 OSPFv3 进程 1 的路由，并将引入的外部路由的开销值设备为 3。

[SwitchB] ospfv3 2 [SwitchB-ospfv3-2] import-route ospfv3 1 cost 3 [SwitchB-ospfv3-2] import-route direct cost 3 [SwitchB-ospfv3-2] quit \# 查看路由引入后 Switch C 的路由表信息。
[SwitchC] display ipv6 routing-table Destinations : 9 Routes : 9 Destination: ::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: 1::/64 Protocol : O_ASE2 NextHop : FE80::200:CFF:FE01:1C03 Preference: 150 Interface : Vlan300 Cost : 3 Destination: 2::/64 Protocol : O_ASE2 NextHop : FE80::200:CFF:FE01:1C03 Preference: 150 Interface : Vlan300 Cost : 3 Destination: 3::/64 Protocol : Direct NextHop : :: Preference: 0 Interface : Vlan300 Cost : 0 Destination: 3::2/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: 4::/64 Protocol : Direct NextHop : :: Preference: 0 Interface : Vlan400 Cost : 0 Destination: 4::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: FE80::/10 Protocol : Direct NextHop : :: Preference: 0 Interface : NULL0 Cost : 0 Destination: FF00::/8 Protocol : Direct NextHop : :: Preference: 0 Interface : NULL0 Cost : 0

###### 1. 组网需求

###### 3. 配置步骤

##### 1.19.5 OSPFv3发布ASBR聚合路由配置举例

组网需求
1.
• Switch A、Switch B 和 Switch C 位于 Area 2 内；
• Switch B 上运行两个 OSPFv3 进程：1 和 2。Switch B 通过进程 1 和 Switch A 交换路由信息，通过进程 2 和 Switch C 交换路由信息；
在 Switch A 的接口 Vlan-interface200 上配置地址 2:1:1::1/64、2:1:2::1/64、2:1:3::1/64，并
•在 上配置 进程 引入直连路由和 进程 的路由，使得Switch B OSPFv3 2 OSPFv3 1 Switch C能够学习到达 2::/64、2:1:1::/64、2:1:2::/64、2:1:3::/64 的路由；
• 为了减小 Switch C 的路由表规模，在 Switch B 上配置 ASBR 聚合路由，只发布聚合后的路由2::/16。

###### 2. 组网图

图1-6 OSPFv3 发布 ASBR 聚合路由配置组网图配置步骤
3.
(1) 配置各接口的 IPv6 地址（略）
(2) 配置 OSPFv3 \# 在 Switch A 上启动 OSPFv3 进程 1。
<SwitchA> system-view [SwitchA] ospfv3 1 [SwitchA-ospfv3-1] router-id 1.1.1.1 [SwitchA-ospfv3-1] quit [SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] ospfv3 1 area 2 [SwitchA-Vlan-interface100] quit [SwitchA] interface vlan-interface 200 [SwitchA-Vlan-interface200] ipv6 address 2:1:1::1 64 [SwitchA-Vlan-interface200] ipv6 address 2:1:2::1 64 [SwitchA-Vlan-interface200] ipv6 address 2:1:3::1 64 [SwitchA-Vlan-interface200] ospfv3 1 area 2 [SwitchA-Vlan-interface200] quit \# 在 Switch B 上启动两个 OSPFv3 进程，进程号分别为 1 和 2。
<SwitchB> system-view [SwitchB] ospfv3 1

[SwitchB-ospfv3-1] router-id 2.2.2.2 [SwitchB-ospfv3-1] quit [SwitchB] interface vlan-interface 100 [SwitchB-Vlan-interface100] ospfv3 1 area 2 [SwitchB-Vlan-interface100] quit [SwitchB] ospfv3 2 [SwitchB-ospfv3-2] router-id 3.3.3.3 [SwitchB-ospfv3-2] quit [SwitchB] interface vlan-interface 300 [SwitchB-Vlan-interface300] ospfv3 2 area 2 [SwitchB-Vlan-interface300] quit \# 在 Switch C 上启动 OSPFv3 进程 2。
<SwitchC> system-view [SwitchC] ospfv3 2 [SwitchC-ospfv3-2] router-id 4.4.4.4 [SwitchC-ospfv3-2] quit [SwitchC] interface vlan-interface 300 [SwitchC-Vlan-interface300] ospfv3 2 area 2 [SwitchC-Vlan-interface300] quit [SwitchC] interface vlan-interface 400 [SwitchC-Vlan-interface400] ospfv3 2 area 2 [SwitchC-Vlan-interface400] quit
(3) 配置 OSPFv3 引入外部路由\# 在 Switch B 上配置 OSPFv3 进程 2 引入直连路由和 OSPFv3 进程 1 的路由。
[SwitchB] ospfv3 2 [SwitchB-ospfv3-2] import-route ospfv3 1 [SwitchB-ospfv3-2] import-route direct [SwitchB-ospfv3-2] quit \# 查看路由引入后 Switch C 的路由表信息。
[SwitchC] display ipv6 routing-table Destinations : 12 Routes : 12 Destination: ::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: 1::/64 Protocol : O_ASE2 NextHop : FE80::200:CFF:FE01:1C03 Preference: 150 Interface : Vlan300 Cost : 1 Destination: 2::/64 Protocol : O_ASE2 NextHop : FE80::200:CFF:FE01:1C03 Preference: 150 Interface : Vlan300 Cost : 1 Destination: 2:1:1::/64 Protocol : O_ASE2 NextHop : FE80::200:CFF:FE01:1C03 Preference: 150

Interface : Vlan300 Cost : 1 Destination: 2:1:2::/64 Protocol : O_ASE2 NextHop : FE80::200:CFF:FE01:1C03 Preference: 150 Interface : Vlan300 Cost : 1 Destination: 2:1:3::/64 Protocol : O_ASE2 NextHop : FE80::200:CFF:FE01:1C03 Preference: 150 Interface : Vlan300 Cost : 1 Destination: 3::/64 Protocol : Direct NextHop : 3::2 Preference: 0 Interface : Vlan300 Cost : 0 Destination: 3::2/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: 4::/64 Protocol : Direct NextHop : 4::1 Preference: 0 Interface : Vlan400 Cost : 0 Destination: 4::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: FE80::/10 Protocol : Direct NextHop : :: Preference: 0 Interface : NULL0 Cost : 0 Destination: FF00::/8 Protocol : Direct NextHop : :: Preference: 0 Interface : NULL0 Cost : 0
(4) 配置 OSPFv3 发布 ASBR 聚合路由\# 在 Switch B 上配置 OSPFv3 进程 2 发布 ASBR 聚合路由 2::/16 。
[SwitchB] ospfv3 2 [SwitchB-ospfv3-2] asbr-summary 2:: 16 [SwitchB-ospfv3-2] quit \# 查看路由聚合后 Switch C 的路由表信息。
[SwitchC] display ipv6 routing-table Destinations : 9 Routes : 9 Destination: ::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: 1::/64 Protocol : O_ASE2

NextHop : FE80::200:CFF:FE01:1C03 Preference: 150 Interface : Vlan300 Cost : 1 Destination: 2::/16 Protocol : O_ASE2 NextHop : FE80::200:CFF:FE01:1C03 Preference: 150 Interface : Vlan300 Cost : 1 Destination: 3::/64 Protocol : Direct NextHop : 3::2 Preference: 0 Interface : Vlan300 Cost : 0 Destination: 3::2/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: 4::/64 Protocol : Direct NextHop : 4::1 Preference: 0 Interface : Vlan400 Cost : 0 Destination: 4::1/128 Protocol : Direct NextHop : ::1 Preference: 0 Interface : InLoop0 Cost : 0 Destination: FE80::/10 Protocol : Direct NextHop : :: Preference: 0 Interface : NULL0 Cost : 0 Destination: FF00::/8 Protocol : Direct NextHop : :: Preference: 0 Interface : NULL0 Cost : 0

##### 1.19.6 OSPFv3 GR配置举例

###### 1. 组网需求

、 和 既属于同一自治系统，也属于同一 区域，通过
• Switch A Switch B Switch C OSPFv3 OSPFv3 协议实现网络互连，并提供 GR 机制。
• Switch A 作为 GR Restarter，Switch B 和 Switch C 作为 GR Helper 并且通过 GR 机制与Switch A 保持同步。

###### 3. 配置步骤

###### 2. 组网图

图1-7 OSPFv3 GR 配置组网图配置步骤
3.
(1) 配置各接口的 IPv6 地址（略）
(2) 配置 OSPFv3 基本功能\# 配置 Switch A，启动 OSPFv3，并设置其 Router ID 为 1.1.1.1。
<SwitchA> system-view [SwitchA] ospfv3 1 [SwitchA-ospfv3-1] router-id 1.1.1.1 [SwitchA-ospfv3-1] graceful-restart enable [SwitchA-ospfv3-1] quit [SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] ospfv3 1 area 1 [SwitchA-Vlan-interface100] quit \# 配置 Switch B，启动 OSPFv3，并设置其 Router ID 为 2.2.2.2。缺省情况下，Switch B 的能力处于开启状态。
GR helper <SwitchB> system-view [SwitchB] ospfv3 1 [SwitchB-ospfv3-1] router-id 2.2.2.2 [SwitchB-ospfv3-1] quit [SwitchB] interface vlan-interface 100 [SwitchB-Vlan-interface100] ospfv3 1 area 1 [SwitchB-Vlan-interface100] quit \# 配置 Switch C，启动 OSPFv3，并设置其 Router ID 为 3.3.3.3。缺省情况下，Switch C 的能力处于开启状态。
GR helper <SwitchC> system-view [SwitchC] ospfv3 1 [SwitchC-ospfv3-1] router-id 3.3.3.3 [SwitchC-ospfv3-1] quit [SwitchC] interface vlan-interface 100 [SwitchC-Vlan-interface100] ospfv3 1 area 1 [SwitchC-Vlan-interface100] quit

###### 1. 组网需求

###### 4. 验证配置

运行稳定后，在 Switch A 上主备倒换进入 OSPFv3 协议的 GR 进程。

##### 1.19.7 OSPFv3 NSR配置举例

组网需求
1.
• Switch A、Switch B 和 Switch S 既属于同一自治系统，也属于同一 OSPFv3 区域，通过OSPFv3 协议实现网络互连。Switch S 为分布式设备，提供 NSR 机制；
当 Switch S 进行主备倒换时，Switch A 和 Switch B 与 Switch S 的邻居没有中断，Switch A
•到 的流量没有中断。
Switch B

###### 2. 组网图

图1-8 OSPFv3 NSR 配置组网图

###### 3. 配置步骤

配置各接口的 地址（略）
(1) IPv6配置 基本功能
(2) OSPFv3 \# 配置 Switch A，启动 OSPFv3，并设置其 Router ID 为 1.1.1.1。
<SwitchA> system-view [SwitchA] ospfv3 1 [SwitchA-ospfv3-1] router-id 1.1.1.1 [SwitchA-ospfv3-1] quit [SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] ospfv3 1 area 1 [SwitchA-Vlan-interface100] quit \# 配置 Switch B，启动 OSPFv3，并设置其 Router ID 为 2.2.2.2。
<SwitchB> system-view [SwitchB] ospfv3 1 [SwitchB-ospfv3-1] router-id 2.2.2.2 [SwitchB-ospfv3-1] quit [SwitchB] interface vlan-interface 200 [SwitchB-Vlan-interface200] ospfv3 1 area 1 [SwitchB-Vlan-interface200] quit配置 S，启动 OSPFv3，并设置其 为 3.3.3.3。使能 能力。
\# Switch Router ID NSR <SwitchS> system-view [SwitchS] ospfv3 1 [SwitchS-ospfv3-1] router-id 3.3.3.3 [SwitchS-ospfv3-1] non-stop-routing [SwitchS-ospfv3-1] quit [SwitchS] interface vlan-interface 100

###### 3. 配置步骤

[SwitchS-Vlan-interface100] ospfv3 1 area 1 [SwitchS-Vlan-interface100] quit [SwitchS] interface vlan-interface 200 [SwitchS-Vlan-interface200] ospfv3 1 area 1 [SwitchS-Vlan-interface200] quit

###### 4. 验证配置

运行稳定后，在 Switch S 上主备倒换进入 OSPFv3 协议的 NSR 阶段，保证倒换期间流量正常转发，倒换后平滑升级。

##### 1.19.8 OSPFv3与BFD联动配置举例

###### 1. 组网需求

Switch A、Switch B 和 Switch C 上运行 OSPFv3，网络层相互可达。
•当 Switch A 和 Switch B 通过 L2 Switch 通信的链路出现故障时 BFD 能够快速感知通告
•协议，并且切换到 进行通信。
OSPFv3 Switch C

###### 2. 组网图

图1-9 OSPFv3 与 BFD 联动配置组网图

| 接口 | IPv6地址 | 设备 | 接口 |
|---|---|---|---|
| Vlan-int10 | 2001::1/64 | Switch B | Vlan-int10 |
| Vlan-int11 | 2001:2::1/64 |  | Vlan-int13 |
| Vlan-int11 | 2001:2::2/64 |  |  |
| Vlan-int13 | 2001:3::1/64 |  |  |

设备 IPv6地址Switch A 2001::2/64 2001:3::2/64 Switch C配置步骤
3.
(1) 配置各接口的 IPv6 地址（略）
(2) 配置 OSPFv3 基本功能\# 配置 Switch A ，启动 OSPFv3 ，并设置其 Router ID 为 1.1.1.1 。
<SwitchA> system-view [SwitchA] ospfv3 [SwitchA-ospfv3-1] router-id 1.1.1.1 [SwitchA-ospfv3-1] quit

[SwitchA] interface vlan-interface 10 [SwitchA-Vlan-interface10] ospfv3 1 area 0 [SwitchA-Vlan-interface10] quit [SwitchA] interface vlan-interface 11 [SwitchA-Vlan-interface11] ospfv3 1 area 0 [SwitchA-Vlan-interface11] quit \# 配置 Switch B，启动 OSPFv3，并设置其 Router ID 为 2.2.2.2。
<SwitchB> system-view [SwitchB] ospfv3 [SwitchB-ospfv3-1] router-id 2.2.2.2 [SwitchB-ospfv3-1] quit [SwitchB] interface vlan-interface 10 [SwitchB-Vlan-interface10] ospfv3 1 area 0 [SwitchB-Vlan-interface10] quit [SwitchB] interface vlan-interface 13 [SwitchB-Vlan-interface13] ospfv3 1 area 0 [SwitchB-Vlan-interface13] quit \# 配置 Switch C，启动 OSPFv3，并设置其 Router ID 为 3.3.3.3。
<SwitchC> system-view [SwitchC] ospfv3 [SwitchC-ospfv3-1] router-id 3.3.3.3 [SwitchC-ospfv3-1] quit [SwitchC] interface vlan-interface 11 [SwitchC-Vlan-interface11] ospfv3 1 area 0 [SwitchC-Vlan-interface11] quit [SwitchC] interface vlan-interface 13 [SwitchC-Vlan-interface13] ospfv3 1 area 0 [SwitchC-Vlan-interface13] quit配置 功能
(3) BFD在 上使能 检测功能，并配置 参数。
\# Switch A BFD BFD [SwitchA] bfd session init-mode active [SwitchA] interface vlan-interface 10 [SwitchA-Vlan-interface10] ospfv3 bfd enable [SwitchA-Vlan-interface10] bfd min-transmit-interval 500 [SwitchA-Vlan-interface10] bfd min-receive-interval 500 [SwitchA-Vlan-interface10] bfd detect-multiplier 7 [SwitchA-Vlan-interface10] return \# 在 Switch B 上使能 BFD 检测功能，并配置 BFD 参数。
[SwitchB] bfd session init-mode active [SwitchB] interface vlan-interface 10 [SwitchB-Vlan-interface10] ospfv3 bfd enable [SwitchB-Vlan-interface10] bfd min-transmit-interval 500 [SwitchB-Vlan-interface10] bfd min-receive-interval 500 [SwitchB-Vlan-interface10] bfd detect-multiplier 6

###### 4. 验证配置

下面以 Switch A 为例，Switch B 和 Switch A 类似，不再赘述。

\# 显示 Switch A 的 BFD 信息。
<SwitchA> display bfd session Total Session Num: 1 Init Mode: Active IPv6 session working in control packet mode:
Local Discr: 1441 Remote Discr: 1450 Source IP: FE80::20F:FF:FE00:1202（Switch A 接口 Vlan-interface10 的链路本地地址）
FE80::20F:FF:FE00:1200（Switch 接口 的链路本地地址）
Destination IP: B Vlan-interface10 Session State: Up Interface: Vlan10 Hold Time: 2319ms在 上查看 的路由信息，可以看出 和 是通过\# Switch A 2001:4::0/64 Switch A Switch B L2 Switch进行通信的。
<SwitchA> display ipv6 routing-table 2001:4::0 64 Summary Count : 1 Destination: 2001:4::/64 Protocol : O_INTRA NextHop : FE80::20F:FF:FE00:1200 Preference: 10 Interface : Vlan10 Cost : 1当 和 通过 通信的链路出现故障时：
Switch A Switch B L2 Switch在 上查看 的路由信息，可以看出 和 已经切换到\# Switch A 2001:4::0/64 Switch A Switch B Switch C 进行通信。
<SwitchA> display ipv6 routing-table 2001:4::0 64 Summary Count : 1 Destination: 2001:4::/64 Protocol : O_INTRA NextHop : FE80::BAAF:67FF:FE27:DCD0 Preference: 10 Interface : Vlan11 Cost : 2

##### 1.19.9 OSPFv3快速重路由配置举例

###### 1. 组网需求

如 图 所示，Switch A、Switch B和Switch C属于同一OSPF区域，通过OSPFv3 协议实现网络1-10互连。要求当Switch A和Switch B之间的链路出现故障时，业务可以快速切换到链路B上。

###### 3. 配置步骤

###### 2. 组网图

图1-10 OSPFv3 快速重路由配置组网图

| 接口 | IP地址 | 设备 | 接口 |
|---|---|---|---|
| Vlan-int100 | 1::1/64 | Switch B | Vlan-int101 |
| Vlan-int200 | 2::1/64 |  | Vlan-int200 |
| Loop0 | 10::1/128 |  | Loop0 |
| Vlan-int100 | 1::2/64 |  |  |
| Vlan-int101 | 3::2/64 |  |  |

设备 IP地址Switch A 3::1/64 2::2/64 20::1/128 Switch C配置步骤
3.
(1) 配置各交换机接口的 IP 地址和 OSPFv3 协议请按照上面组网图配置各接口的 IP 地址和子网掩码，具体配置过程略。
配置各交换机之间采用 OSPFv3 协议进行互连，确保 Switch A、Switch B 和 Switch C 之间能够在网络层互通，并且各交换机之间能够借助 协议实现动态路由更新。
OSPFv3具体配置过程略。
(2) 配置 OSPFv3 快速重路由OSPFv3 支持快速重路由的配置方法有两种，一种是通过 LFA 算法选取备份下一跳，另一种是在路由策略中指定备份下一跳，两种方法任选一种。
方法一：使能 和 的 快速重路由功能（通过 算法选取备份下Switch A Switch B OSPFv3 LFA一跳信息）
\# 配置 Switch A。
<SwitchA> system-view [SwitchA] ospfv3 1 [SwitchA-ospfv3-1] fast-reroute lfa [SwitchA-ospfv3-1] quit \# 配置 Switch B。
<SwitchB> system-view [SwitchB] ospfv3 1 [SwitchB-ospfv3-1] fast-reroute lfa [SwitchB-ospfv3-1] quit方法二：使能 Switch A 和 Switch B 的 OSPFv3 快速重路由功能（通过路由策略指定备份下一跳）
\# 配置 Switch A。

<SwitchA> system-view [SwitchA] ipv6 prefix-list abc index 10 permit 20::1 128 [SwitchA] route-policy frr permit node 10 [SwitchA-route-policy-frr-10] if-match ipv6 address prefix-list abc [SwitchA-route-policy-frr-10] apply ipv6 fast-reroute backup-interface vlan-interface 100 backup-nexthop 1::2/64 [SwitchA-route-policy-frr-10] quit [SwitchA] ospfv3 1 [SwitchA-ospfv3-1] fast-reroute route-policy frr [SwitchA-ospfv3-1] quit \# 配置 Switch B。
<SwitchB> system-view [SwitchB] ipv6 prefix-list abc index 10 permit 10::1 128 [SwitchB] route-policy frr permit node 10 [SwitchB-route-policy-frr-10] if-match ipv6 address prefix-list abc [SwitchB-route-policy-frr-10] apply ipv6 fast-reroute backup-interface vlan-interface 101 backup-nexthop 3::2/64 [SwitchB-route-policy-frr-10] quit [SwitchB] ospfv3 1 [SwitchB-ospfv3-1] fast-reroute route-policy frr [SwitchB-ospfv3-1] quit

###### 4. 验证配置

在 上查看 的路由信息，可以看到备份下一跳信息。
\# Switch A 20::1/128 [SwitchA] display ipv6 routing-table 20::1 128 verbose Summary count : 1 Destination: 20::1/128 Protocol: O_INTRA Process ID: 1 SubProtID: 0x1 Age: 00h03m45s Cost: 6 Preference: 10 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0xa OrigAs: 0 NibID: 0x23000005 LastAs: 0 AttrID: 0xffffffff Neighbor: ::
Flags: 0x10041 OrigNextHop: FE80::7685:45FF:FEAD:102 Label: NULL RealNextHop: FE80::7685:45FF:FEAD:102 BkLabel: NULL BkNextHop: FE80::34CD:9FF:FE2F:D02 Tunnel ID: Invalid Interface: Vlan-interface200 BkTunnel ID: Invalid BkInterface: Vlan-interface100 FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0 \# 在 Switch B 上查看 10::1/128 的路由信息，可以看到备份下一跳信息。
[SwitchB] display ipv6 routing-table 10::1 128 verbose

Summary count : 1 Destination: 10::1/128 Protocol: O_INTRA Process ID: 1 SubProtID: 0x1 Age: 00h03m10s Cost: 1 Preference: 10 IpPre: N/A QosLocalID: N/A Tag: 0 State: Active Adv OrigTblID: 0x0 OrigVrf: default-vrf TableID: 0xa OrigAs: 0 NibID: 0x23000006 LastAs: 0 AttrID: 0xffffffff Neighbor: ::
Flags: 0x10041 OrigNextHop: FE80::34CC:E8FF:FE5B:C02 Label: NULL RealNextHop: FE80::34CC:E8FF:FE5B:C02 BkLabel: NULL BkNextHop: FE80::7685:45FF:FEAD:102 Tunnel ID: Invalid Interface: Vlan-interface200 BkTunnel ID: Invalid BkInterface: Vlan-interface101 FtnIndex: 0x0 TrafficIndex: N/A Connector: N/A PathID: 0x0

##### 1.19.10 OSPFv3 IPsec安全框架配置举例

###### 1. 组网需求

所有的交换机都运行 OSPFv3，整个自治系统划分为 个区域。
• 2要求配置 安全框架对 A、Switch 和 之间的 报文进行有效性
• IPsec Switch B Switch C OSPFv3检查和验证。

###### 2. 组网图

图1-11 OSPFv3 IPsec 安全框架配置组网图OSPFv3 Switch B Area 0 Switch C Vlan-int100 2001::1/64 Vlan-int100 2001::2/64 Vlan-int200 2001:1::1/64 OSPFv3 Vlan-int200 Area 1 2001:1::2/64 Switch A

###### 3. 配置步骤

(1) 配置各接口的 IPv6 地址（略）
(2) 配置 OSPFv3 基本功能

\# 配置 Switch A，启动 OSPFv3，并设置其 Router ID 为 1.1.1.1。
<SwitchA> system-view [SwitchA] ospfv3 1 [SwitchA-ospfv3-1] router-id 1.1.1.1 [SwitchA-ospfv3-1] quit [SwitchA] interface vlan-interface 200 [SwitchA-Vlan-interface200] ospfv3 1 area 1 [SwitchA-Vlan-interface200] quit \# 配置 Switch B，启动 OSPFv3，并设置其 Router ID 为 2.2.2.2。
<SwitchB> system-view [SwitchB] ospfv3 1 [SwitchB-ospfv3-1] router-id 2.2.2.2 [SwitchB-ospfv3-1] quit [SwitchB] interface vlan-interface 100 [SwitchB-Vlan-interface100] ospfv3 1 area 0 [SwitchB-Vlan-interface100] quit [SwitchB] interface vlan-interface 200 [SwitchB-Vlan-interface200] ospfv3 1 area 1 [SwitchB-Vlan-interface200] quit配置 C，启动 OSPFv3，并设置其 为 3.3.3.3。
\# Switch Router ID <SwitchC> system-view [SwitchC] ospfv3 1 [SwitchC-ospfv3-1] router-id 3.3.3.3 [SwitchC-ospfv3-1] quit [SwitchC] interface vlan-interface 100 [SwitchC-Vlan-interface100] ospfv3 1 area 0 [SwitchC-Vlan-interface100] quit
(3) 配置 OSPFv3 IPsec 安全框架\# 配置 Switch A。创建名为 trans 的安全提议，报文封装形式采用传输模式，安全协议采用协议。创建一条安全框架 profile001，协商方式为 manual，配置 和密钥。
ESP SPI [SwitchA] ipsec transform-set trans [SwitchA-ipsec-transform-set-trans] encapsulation-mode transport [SwitchA-ipsec-transform-set-trans] protocol esp [SwitchA-ipsec-transform-set-trans] esp encryption-algorithm aes-cbc-128 [SwitchA-ipsec-transform-set-trans] esp authentication-algorithm sha1 [SwitchA-ipsec-transform-set-trans] quit [SwitchA] ipsec profile profile001 manual [SwitchA-ipsec-profile-manual-profile001] transform-set trans [SwitchA-ipsec-profile-manual-profile001] sa spi outbound esp 123456 [SwitchA-ipsec-profile-manual-profile001] sa spi inbound esp 123456 [SwitchA-ipsec-profile-manual-profile001] sa string-key outbound esp simple abcdefg [SwitchA-ipsec-profile-manual-profile001] sa string-key inbound esp simple abcdefg [SwitchA-ipsec-profile-manual-profile001] quit \# 配置 Switch B。创建名为 trans 的安全提议，报文封装形式采用传输模式，安全协议采用ESP 协议。创建一条安全框架 profile001，协商方式为 manual，配置 SPI 和密钥。创建一条安全框架 profile002，协商方式为 manual，配置 和密钥。
SPI

[SwitchB] ipsec transform-set trans [SwitchB-ipsec-transform-set-trans] encapsulation-mode transport [SwitchB-ipsec-transform-set-trans] protocol esp [SwitchB-ipsec-transform-set-trans] esp encryption-algorithm aes-cbc-128 [SwitchB-ipsec-transform-set-trans] esp authentication-algorithm sha1 [SwitchB-ipsec-transform-set-trans] quit [SwitchB] ipsec profile profile001 manual [SwitchB-ipsec-profile-manual-profile001] transform-set trans [SwitchB-ipsec-profile-manual-profile001] sa spi outbound esp 123456 [SwitchB-ipsec-profile-manual-profile001] sa spi inbound esp 123456 [SwitchB-ipsec-profile-manual-profile001] sa string-key outbound esp simple abcdefg [SwitchB-ipsec-profile-manual-profile001] sa string-key inbound esp simple abcdefg [SwitchB-ipsec-profile-manual-profile001] quit [SwitchB] ipsec profile profile002 manual [SwitchB-ipsec-profile-manual-profile002] transform-set trans [SwitchB-ipsec-profile-manual-profile002] sa spi outbound esp 256 [SwitchB-ipsec-profile-manual-profile002] sa spi inbound esp 256 [SwitchB-ipsec-profile-manual-profile002] sa string-key outbound esp simple byebye [SwitchB-ipsec-profile-manual-profile001] sa string-key inbound esp simple byebye [SwitchB-ipsec-profile-manual-profile001] quit \# 配置 Switch C。创建名为 trans 的安全提议，报文封装形式采用传输模式，安全协议采用ESP 协议。创建一条安全框架 profile002，协商方式为 manual，配置 SPI 和密钥。
[SwitchC] ipsec transform-set trans [SwitchC-ipsec-transform-set-trans] encapsulation-mode transport [SwitchC-ipsec-transform-set-trans] protocol esp [SwitchC-ipsec-transform-set-trans] esp encryption-algorithm aes-cbc-128 [SwitchC-ipsec-transform-set-trans] esp authentication-algorithm sha1 [SwitchC-ipsec-transform-set-trans] quit [SwitchC] ipsec profile profile002 manual [SwitchC-ipsec-profile-manual-profile002] transform-set trans [SwitchC-ipsec-profile-manual-profile002] sa spi outbound esp 256 [SwitchC-ipsec-profile-manual-profile002] sa spi inbound esp 256 [SwitchC-ipsec-profile-manual-profile002] sa string-key outbound esp simple byebye [SwitchC-ipsec-profile-manual-profile001] sa string-key inbound esp simple byebye [SwitchC-ipsec-profile-manual-profile001] quit配置 区域上应用 安全框架
(4) OSPFv3 IPsec配置 A。
\# Switch [SwitchA] ospfv3 1 [SwitchA-ospfv3-1] area 1 [SwitchA-ospfv3-1-area-0.0.0.1] enable ipsec-profile profile001 [SwitchA-ospfv3-1-area-0.0.0.1] quit [SwitchA-ospfv3-1] quit \# 配置 Switch B。
[SwitchB] ospfv3 1 [SwitchB-ospfv3-1] area 0 [SwitchB-ospfv3-1-area-0.0.0.0] enable ipsec-profile profile002 [SwitchB-ospfv3-1-area-0.0.0.0] quit

[SwitchB-ospfv3-1] area 1 [SwitchB-ospfv3-1-area-0.0.0.1] enable ipsec-profile profile001 [SwitchB-ospfv3-1-area-0.0.0.1] quit [SwitchB-ospfv3-1] quit \# 配置 Switch C。
[SwitchC] ospfv3 1 [SwitchC-ospfv3-1] area 0 [SwitchC-ospfv3-1-area-0.0.0.0] enable ipsec-profile profile002 [SwitchC-ospfv3-1-area-0.0.0.0] quit [SwitchC-ospfv3-1] quit

###### 4. 验证配置

以上配置完成后，Switch A、Switch 和 之间的 报文将被加密传输。
B Switch C OSPFv3

## 11-IPv6策略路由配置

目 录策略路由简介创建 策略节点对本地报文应用 策略策略路由典型配置举例

### 1 IPv6策略路由

#### 1.1 IPv6策略路由简介

与单纯依照 IPv6 报文的目的地址查找路由表进行转发不同，策略路由是一种依据用户制定的策略进行路由转发的机制。策略路由可以对于满足一定条件（ACL 规则）的报文，执行指定的操作（设置报文的下一跳）。

##### 1.1.1 IPv6报文的转发流程

报文到达后，其后续的转发流程如下：
• 首先根据配置的策略路由转发。
• 若找不到匹配的节点，或虽然找到了匹配的节点但指导 IPv6 报文转发失败时，根据路由表中除缺省路由之外的路由来转发报文。
• 若转发失败，则根据缺省路由来转发报文。

##### 1.1.2 IPv6策略路由类型

根据作用对象的不同，策略路由可分为本地策略路由和转发策略路由：
本地策略路由：对设备本身产生的报文（比如本地发出的 报文）起作用，指导其发送。
• ping转发策略路由：对接口接收的报文起作用，指导其转发。
•

##### 1.1.3 IPv6策略简介

IPv6 策略用来定义报文的匹配规则，以及对报文执行的操作。IPv6 策略由节点组成。
一个 IPv6 策略可以包含一个或者多个节点。节点的构成如下：
• 每个节点由节点编号来标识。节点编号越小节点的优先级越高，优先级高的节点优先被执行。
• 每个节点的具体内容由 if-match 子句和 apply 子句来指定。if-match 子句定义该节点的匹配规则，apply 子句定义该节点的动作。
• 每个节点对报文的处理方式由匹配模式决定。匹配模式分为 permit （允许）和 deny （拒绝）
两种。
应用 IPv6 策略后，系统将根据 IPv6 策略中定义的匹配规则和操作，对报文进行处理：系统按照优先级从高到低的顺序依次匹配各节点，如果报文满足这个节点的匹配规则，就执行该节点的动作；
如果报文不满足这个节点的匹配规则，就继续匹配下一个节点；如果报文不能满足 IPv6 策略中任何一个节点的匹配规则，则根据路由表来转发报文。

###### 1. if-match子句关系

目前，IPv6 策略路由支持通过 if-match acl 子句设置 匹配规则，在一个节点中只能配置一ACL条 if-match acl 子句。

###### 2. apply子句关系

目前，IPv6 策略路由仅提供了一种 apply 子句，即 apply next-hop，用来设置报文转发的下一跳。

###### 3. 节点的匹配模式与节点的if-match子句、apply子句的关系

一个节点的匹配模式与这个节点的if-match子句、apply子句的关系如 表 所示。
1-1表1-1 节点的匹配模式、if-match 子句、apply 子句三者之间的关系

| 是否满足所有 if-match 子句 |  | 节点匹配模式 |  |  |  |  |
|---|---|---|---|---|---|---|
|  |  | permit（允许模式） |  |  | deny（拒绝模式） |  |
|  | • 如果节点配置了apply 子句，则执行此节点apply 子句，不再匹配下一节点，如果节点指导报文转发成功，则不再匹配下一节点 • 如果节点未配置 apply 子句，则不会执行任何动作，且不再匹配下一节点，报文将根据路由表来进行转发 |  |  |  |  |  |
|  | 不执行此节点apply子句，继续匹配下一节点 |  |  |  |  |  |

如果一个节点中未配置任何 if-match 子句，则认为所有报文都满足该节点的匹配规则，按照“报文满足所有 if-match 子句”的情况进行后续处理。

##### 1.1.4 策略路由与Track联动

策略路由通过与 Track 联动，增强了应用的灵活性和对网络环境变化的动态感知能力。
策略路由可以在配置报文的下一跳时与 Track 项关联，根据 Track 项的状态来动态地决定策略的可用性。策略路由配置仅在关联的 Track项状态为 或 NotReady时生效。关于策略路由与Positive Track联动的详细介绍和相关配置，请参见“可靠性配置指导”中的“Track”。

#### 1.2 IPv6策略路由配置任务简介

策略路由配置任务如下：
IPv6配置IPv6 策略
(1)
a. 创建IPv6 策略节点
b. 配置IPv6 策略节点的匹配规则
c. 配置IPv6 策略节点的动作
(2) 应用 IPv6 策略请选择以下至少一项任务进行配置：
对本地报文应用IPv6 策略(cid:123)
对接口转发的报文应用IPv6 策略(cid:123)

###### 1. 功能简介

#### 1.3 配置IPv6策略

##### 1.3.1 创建IPv6策略节点

(1) 进入系统视图。
system-view
(2) 创建 IPv6 策略节点，并进入 IPv6 策略节点视图。
ipv6 policy-based-route policy-name [ deny | permit ] node node-number
(3) （可选）设置当前 IPv6 策略节点的描述信息。
description text
缺省情况下，未设置当前 IPv6 策略节点的描述信息。

##### 1.3.2 配置IPv6策略节点的匹配规则

(1) 进入系统视图。
system-view
(2) 进入 IPv6 策略节点视图。
ipv6 policy-based-route policy-name [ deny | permit ] node node-number
(3) 设置匹配规则。
设置 ACL 匹配规则。
(cid:123)
if-match acl { ipv6-acl-number | name ipv6-acl-name }
缺省情况下，未设置 ACL 匹配规则。
IPv6 策略路由不支持匹配二层信息的 ACL 匹配规则。
设置 ACL 匹配规则时，对于 ACL 规则的 permit/deny 动作以及 time-range 指定的规则生
效时间段等的处理机制不再生效。

##### 1.3.3 配置IPv6策略节点的动作

功能简介
1.
用户通过配置 apply 子句指导 IPv6 策略节点的动作。目前，IPv6 策略路由仅提供了一种 apply子句，即 apply next-hop，用来设置报文转发的下一跳。

###### 2. 配置限制和指导

策略路由通过查询 表中是否存在下一跳地址对应的条目，判断设置的报文转发下一跳地址IPv6 FIB是否可用。IPv6 策略路由周期性检查 FIB 表，设备到下一跳的路径发生变化时，IPv6 策略路由无法及时感知，可能会导致通信发生短暂中断。

###### 3. 配置指导报文转发类动作

进入系统视图。
(1)
system-view
(2) 进入 IPv6 策略节点视图。
ipv6 policy-based-route policy-name [ deny | permit ] node node-number

###### 1. 功能简介

###### 3. 配置步骤

###### 1. 功能简介

###### 3. 配置步骤

(3) 配置动作。
设置报文转发的下一跳。
(cid:123)
apply next-hop [ vpn-instance vpn-instance-name ] { ipv6-address
[ direct ] [ track track-entry-number ] } &<1-2>
缺省情况下，未设置报文转发的下一跳。
用户通过一次或多次配置本命令可以同时配置多个下一跳，每个节点最多可以配置 个下
2
一跳，这些下一跳起到主备的作用。

#### 1.4 应用IPv6策略

##### 1.4.1 对本地报文应用IPv6策略

功能简介
1.
通过本配置，可以将已经配置的 IPv6 策略应用到本地，指导设备本身产生 IPv6 报文的发送。应用策略时，该 策略必须已经存在，否则配置将失败。
IPv6 IPv6

###### 2. 配置限制和指导

对本地报文只能应用一个 IPv6 策略。应用新的 IPv6 策略前必须删除本地原来已经应用的 IPv6 策略。
若无特殊需求，建议用户不要对本地报文应用 IPv6 策略。否则，有可能会对本地报文的发送造成不必要的影响（如 ping、telnet 服务的失效）。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 对本地报文应用 IPv6 策略。
ipv6 local policy-based-route policy-name缺省情况下，未对本地报文应用 IPv6 策略。

##### 1.4.2 对接口转发的报文应用IPv6策略

功能简介
1.
通过本配置，可以将已经配置的 IPv6 策略应用到接口，指导接口接收的所有 IPv6 报文的转发。应用 IPv6 策略时，该 IPv6 策略必须已经存在，否则配置将失败。

###### 2. 配置限制和指导

对接口转发的报文应用 策略时，一个接口只能应用一个 策略。应用新的 策略前必须IPv6 IPv6 IPv6删除接口上原来已经应用的 IPv6 策略。
一个 IPv6 策略可以同时被多个接口应用。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 进入接口视图。

###### 1. 组网需求

interface interface-type interface-number
(3) 对接口转发的报文应用 IPv6 策略。
ipv6 policy-based-route policy-name缺省情况下，未对接口转发的报文应用 IPv6 策略。

#### 1.5 IPv6策略路由显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示 IPv6 策略路由配置后的运行情况，通过查看显示信息验证配置的效果。
在用户视图下，用户可以执行 reset 命令可以清除 IPv6 策略路由的统计信息。
表1-2 IPv6 策略路由显示和维护操作 命令display ipv6 policy-based-route [ policy显示已经配置的IPv6策略policy-name ] display ipv6 policy-based-route interface显示接口下IPv6转发策略路由的配置信息和统interface-type interface-number [ slot计信息slot-number ] display ipv6 policy-based-route local [ slot显示IPv6本地策略路由的配置信息和统计信息slot-number ]显示已经应用的IPv6策略路由信息 display ipv6 policy-based-route setup reset ipv6 policy-based-route statistics清除IPv6策略路由的统计信息[ policy policy-name ]

#### 1.6 IPv6策略路由典型配置举例

##### 1.6.1 基于报文协议类型的IPv6本地策略路由配置举例

组网需求
1.
Switch A 分别与 Switch B 和 Switch C 直连（保证 Switch B 和 Switch C 之间路由完全不可达）。通过策略路由控制 产生的报文：
Switch A指定所有 报文的下一跳为 1::2；
• TCP其它 IPv6 报文仍然按照查找路由表的方式进行转发。
•

###### 2. 组网图

图1-1 基于报文协议类型的本地策略路由的配置举例组网图

###### 3. 配置步骤

(1) 配置 Switch A
\# 创建 VLAN 10 和 VLAN 20。
<SwitchA> system-view
[SwitchA] vlan 10
[SwitchA-vlan10] quit
[SwitchA] vlan 20
[SwitchA-vlan20] quit
\# 配置接口 Vlan-interface10 和 Vlan-interface20 的 IPv6 地址。
[SwitchA] interface vlan-interface 10
[SwitchA-Vlan-interface10] ipv6 address 1::1 64
[SwitchA-Vlan-interface10] quit
[SwitchA] interface vlan-interface 20
[SwitchA-Vlan-interface20] ipv6 address 2::1 64
[SwitchA-Vlan-interface20] quit
\# 定义访问控制列表 ACL 3001 ，用来匹配 TCP 报文。
[SwitchA] acl ipv6 advanced 3001
[SwitchA-acl-ipv6-adv-3001] rule permit tcp
[SwitchA-acl-ipv6-adv-3001] quit
\# 定义 5 号节点，指定所有 TCP 报文的下一跳为 1::2。
[SwitchA] ipv6 policy-based-route aaa permit node 5
[SwitchA-pbr6-aaa-5] if-match acl 3001
[SwitchA-pbr6-aaa-5] apply next-hop 1::2
[SwitchA-pbr6-aaa-5] quit
\# 在 Switch A 上应用本地策略路由。
[SwitchA] ipv6 local policy-based-route aaa
(2) 配置 Switch B
\# 创建 VLAN 10
<SwitchB> system-view
[SwitchB] vlan 10
[SwitchB-vlan10] quit
\# 配置接口 Vlan-interface10 的 IP 地址。
[SwitchB] interface vlan-interface 10
[SwitchB-Vlan-interface10] ipv6 address 1::2 64
配置
(3) Switch C
\#创建
VLAN 20
<SwitchC> system-view
[SwitchC] vlan 20
[SwitchC-vlan20] quit
配置接口 的 地址。
\# Vlan-interface20 IP
[SwitchC] interface vlan-interface 20
[SwitchC-Vlan-interface20] ipv6 address 2::2 64

###### 4. 验证配置

从 Switch A 上通过 Telnet 方式登录 Switch B（1::2/64），结果成功。

从 Switch A 上通过 Telnet 方式登录 Switch C（2::2/64），结果失败。
从 Switch A 上 ping Switch C（2::2/64），结果成功。
由于 Telnet 使用的是 TCP 协议，ping 使用的是 ICMP6 协议，所以由以上结果可证明：Switch A 发出的 报文的下一跳为 1::2，接口 不发送 报文，但可以发送非 报文，TCP Vlan-interface20 TCP TCP策略路由设置成功。

##### 1.6.2 基于报文协议类型的IPv6转发策略路由配置举例

###### 1. 组网需求

Switch A 分别与 Switch B 和 Switch C 直连（保证 Switch B 和 Switch C 之间路由完全不可达）。通过策略路由控制从 Switch A 的接口 Vlan-interface11 接收的报文：
• 指定所有 TCP 报文的下一跳为 1::2；
• 其它 IPv6 报文仍然按照查找路由表的方式进行转发。

###### 2. 组网图

图1-2 基于报文协议类型的 IPv6 转发策略路由配置举例组网图

###### 3. 配置步骤

(1) 配置 Switch A
创建 和 20。
\# VLAN 10 VLAN
<SwitchA> system-view
[SwitchA] vlan 10
[SwitchA-vlan10] quit
[SwitchA] vlan 20
[SwitchA-vlan20] quit

\# 配置动态路由协议 RIPng。
[SwitchA] ripng 1 [SwitchA-ripng-1] quit [SwitchA] interface vlan-interface 10 [SwitchA-Vlan-interface10] ipv6 address 1::1 64 [SwitchA-Vlan-interface10] ripng 1 enable [SwitchA-Vlan-interface10] quit [SwitchA] interface vlan-interface 20 [SwitchA-Vlan-interface20] ipv6 address 2::1 64 [SwitchA-Vlan-interface20] ripng 1 enable [SwitchA-Vlan-interface20] quit \# 定义访问控制列表 ACL 3001，用来匹配 TCP 报文。
[SwitchA] acl ipv6 advanced 3001 [SwitchA-acl-ipv6-adv-3001] rule permit tcp [SwitchA-acl-ipv6-adv-3001] quit \# 定义 5 号节点，指定所有 TCP 报文的下一跳为 1::2。
[SwitchA] ipv6 policy-based-route aaa permit node 5 [SwitchA-pbr6-aaa-5] if-match acl 3001 [SwitchA-pbr6-aaa-5] apply next-hop 1::2 [SwitchA-pbr6-aaa-5] quit在接口 上应用转发策略路由，处理此接口接收的报文。
\# Vlan-interface11 [SwitchA] interface vlan-interface 11 [SwitchA-Vlan-interface11] ipv6 address 10::2 64 [SwitchA-Vlan-interface11] undo ipv6 nd ra halt [SwitchA-Vlan-interface11] ripng 1 enable [SwitchA-Vlan-interface11] ipv6 policy-based-route aaa
(2) 配置 Switch B \# 创建 VLAN 10 <SwitchB> system-view [SwitchB] vlan 10 [SwitchB-vlan10] quit \# 配置动态路由协议 RIPng。
[SwitchB] ripng 1 [SwitchB-ripng-1] quit [SwitchB] interface vlan-interface 10 [SwitchB-Vlan-interface10] ipv6 address 1::2 64 [SwitchB-Vlan-interface10] ripng 1 enable [SwitchB-Vlan-interface10] quit
(3) 配置 Switch C \#创建VLAN 20 <SwitchC> system-view [SwitchC] vlan 20 [SwitchC-vlan20] quit配置动态路由协议 RIPng。
\# [SwitchC] ripng 1 [SwitchC-ripng-1] quit

[SwitchC] interface vlan-interface 20 [SwitchC-Vlan-interface20] ipv6 address 2::2 64 [SwitchC-Vlan-interface20] ripng 1 enable [SwitchC-Vlan-interface20] quit

###### 4. 验证配置

在 Host A 上安装 IPv6 协议栈，并将 IPv6 地址配置为 10::3。
C:\>ipv6 install Installing...
Succeeded.
C:\>ipv6 adu 4/10::3从 Host A 上通过 Telnet 方式登录 Router B，结果成功。
从 Host A 上通过 Telnet 方式登录 Router C，结果失败。
从 Host A 上 ping Router C，结果成功。
由于 Telnet 使用的是 TCP 协议，ping 使用的是 ICMP 协议，所以由以上结果可证明：从 Switch A的接口 Vlan-interface11接收的 TCP报文的下一跳为 1::2，接口 Vlan-interface20不转发 TCP报文，但可以转发非 TCP 报文，策略路由设置成功。

## 12-路由策略配置

目 录路由策略简介配置团体属性列表配置 子句路由策略显示和维护在 路由引入中应用路由策略配置举例

### 1 路由策略

1路由策略

#### 1.1 路由策略简介

路由策略是为了改变网络流量所经过的途径而修改路由信息的技术，主要通过改变路由属性（包括可达性）来实现。路由策略可以用来控制路由的发布、控制路由的接收、管理引入的路由和设置路由的属性。

##### 1.1.1 路由策略的实现

路由策略的实现步骤如下：
(1) 首先要定义将要实施路由策略的路由信息的特征，即定义一组匹配规则。可以灵活使用过滤器来定义各种匹配规则。
(2) 然后再将匹配规则应用于路由的发布、接收和引入等过程的路由策略中。

##### 1.1.2 过滤器

过滤器可以看作是路由策略过滤路由的工具，单独配置的过滤器没有任何过滤效果，只有在路由协议的相关命令中应用这些过滤器，才能够达到预期的过滤效果。

###### 1. 访问控制列表

访问控制列表可以指定 IP 地址和子网范围，用于匹配路由信息的目的网段地址或下一跳地址。
ACL 的相关内容请参见“ACL 和 QoS 配置指导”中的“ACL”。

###### 2. 地址前缀列表

地址前缀列表的作用类似于 ACL，但比它更为灵活，且更易于用户理解。使用地址前缀列表过滤路由信息时，其匹配对象为路由信息的目的地址。
一个地址前缀列表由前缀列表名标识。每个前缀列表可以包含多个表项，每个表项可以独立指定一个网络前缀形式的匹配范围，并用一个索引号来标识，索引号指明了在地址前缀列表中进行匹配检查的顺序。
每个表项之间是“或”的关系，在匹配的过程中，路由器按升序依次检查由索引号标识的各个表项，只要有某一表项满足条件，就意味着通过该地址前缀列表的过滤（不再对下一个表项进行匹配）。

###### 3. AS路径访问列表（as-path）

as-path 仅用于 BGP 路由的过滤。BGP 路由的 AS_PATH 属性记录了从本地到目的地址所要经过的所有 AS 号。as-path 就是针对 AS_PATH 属性指定匹配条件。
as-path 的相关内容请参见“三层技术-IP 路由配置指导”中的“BGP”。

###### 4. 团体属性列表（community-list）

community-list 仅用于 BGP 路由的过滤。 BGP 路由中包含团体（ COMMUNITY ）属性，该属性用来标识路由所属的组。community-list 就是针对团体属性指定匹配条件。
团体属性列表的相关内容请参见“三层技术-IP 路由配置指导”中的“BGP”。

###### 5. 扩展团体属性列表（extcommunity-list）

extcommunity-list 仅用于 BGP 路由的过滤。BGP 扩展团体属性有两种，一种是用于 VPN 的 RT（Route Target，路由目标）扩展团体，另一种则是 SoO（Site of Origin，源站点）扩展团体。扩展团体属性列表就是针对这两种属性指定匹配条件。

###### 6. 路由策略

路由策略是一种比较复杂的过滤器，它不仅可以匹配路由信息的某些属性，还可以在条件满足时改变路由信息的属性。路由策略可以使用前面几种过滤器定义自己的匹配规则。
一个路由策略可以由多个节点构成，每个节点是匹配检查的一个单元。在匹配过程中，系统按节点序号升序依次检查各个节点。不同节点间是“或”的关系，如果通过了其中一个节点，就意味着通过该路由策略，不再对其他节点进行匹配（配置了 子句的情况除外）。
continue每个节点对路由信息的处理方式由匹配模式决定。匹配模式分为 和 两种。
permit deny permit：指定节点的匹配模式为允许模式。当路由信息通过该节点的过滤后，将执行该节点
•的 apply 子句，不进入下一个节点的匹配（配置了 continue 子句的情况除外）；如果路由信息没有通过该节点过滤，将进入下一个节点继续匹配。
• deny：指定节点的匹配模式为拒绝模式（此模式下 apply 子句和 continue 子句不会被执行）。当路由信息通过该节点的过滤后，将被拒绝通过该节点，不进入下一个节点的匹配；如果路由信息没有通过该节点的过滤，将进入下一个节点继续匹配。
每个节点可以由一组 if-match、apply 和 子句组成。
continue if-match 子句：定义匹配规则，匹配对象是路由信息的一些属性。同一节点中的不同
•if-match 子句是“与”的关系，只有满足节点内所有 if-match 子句指定的匹配条件，才能通过该节点的匹配。
• apply 子句：指定动作，也就是在通过节点的匹配后，对路由信息的一些属性进行设置。
• continue 子句：用来配置下一个执行节点。当路由成功匹配当前路由策略节点（必须是permit 节点）时，可以指定路由继续匹配同一路由策略内的下一个节点，这样可以组合路由策略各个节点的 子句和 子句，增强路由策略的灵活性。
if-match apply if-match、apply 和 continue 子句可以根据应用进行设置，都是可选的。
如果只过滤路由，不设置路由的属性，则不需要使用 apply 子句。
•如果某个 permit 节点未配置任何 if-match 子句，则该节点匹配所有的路由。
•通常在多个 deny 节点后设置一个不含 if-match 子句和 apply 子句的 permit 节点，用
•于允许其它的路由通过。

#### 1.2 路由策略配置任务简介

路由策略配置任务如下：
(1) （可选）配置过滤器配置IPv4 地址前缀列表(cid:123)
配置 IPv6 地址前缀列表(cid:123)
配置AS路径过滤列表(cid:123)
配置团体属性列表(cid:123)
配置扩展团体属性列表(cid:123)

##### 1. 功能简介

##### 2. 配置步骤

(2) 配置路由策略
a. 创建路由策略
b. 配置if-match子句
c. 配置apply子句
d. 配置continue子句

#### 1.3 配置IPv4地址前缀列表

##### 1. 配置限制和指导

如果所有表项都是deny 模式，则任何路由都不能通过该过滤列表。要允许其它所有IPv4路由通过，需要在多条 deny 模式的表项后定义一条 permit 0.0.0.0 0 less-equal 32 表项。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 配置 IPv4 地址前缀列表。
ip prefix-list prefix-list-name [ index index-number ] { deny | permit } ip-address mask-length [ greater-equal min-mask-length ] [ less-equal max-mask-length ]

#### 1.4 配置IPv6地址前缀列表

##### 1. 配置限制和指导

如果所有表项都是deny 模式，则任何路由都不能通过该过滤列表。要允许其它所有IPv6路由通过，需要在多条 deny 模式的表项后定义一条 permit :: 0 less-equal 128 表项。

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置 IPv6 地址前缀列表。
ipv6 prefix-list prefix-list-name [ index index-number ] { deny | permit }
ipv6-address { inverse inverse-prefix-length | prefix-length
[ greater-equal min-prefix-length ] [ less-equal max-prefix-length ] }

#### 1.5 配置AS路径过滤列表

功能简介
1.
一个 AS 路径过滤列表可以包含多个表项。在匹配过程中，各表项之间是“或”的关系，即只要路由信息通过该列表中的一条表项，就认为通过该 路径过 滤列表。
AS

##### 2. 配置步骤

(1) 进入系统视图。
system-view

##### 2. 配置步骤

###### 1. 功能简介

(2) 配置 AS 路径过滤列表。
ip as-path as-path-number { deny | permit } regular-expression

#### 1.6 配置团体属性列表

##### 1. 功能简介

一个团体属性列表可以定义多个表项。在匹配过程中，各表项之间是“或”的关系，即只要路由信息通过该列表中的一条表项，就认为通过该团体属性列表。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 配置团体属性列表。
配置基本团体属性列表。
(cid:123)
ip community-list { basic-comm-list-num | basic basic-comm-list-name } { deny | permit } [ community-number&<1-32> | aa:nn&<1-32> ] [ internet | no-advertise | no-export | no-export-subconfed ] *配置高级团体属性列表。
(cid:123)
ip community-list { adv-comm-list-num | advanced adv-comm-list-name } { deny | permit } regular-expression

#### 1.7 配置扩展团体属性列表

功能简介
1.
一个扩展团体属性列表可以定义多个表项。在匹配过程中，各表项之间是“或”的关系，即只要路由信息通过该列表中的一条表项，就认为通过该扩展团体属性列表。

##### 2. 配置步骤

(1) 进入系统视图。
system-view
配置扩展团体属性列表。
(2)
ip extcommunity-list ext-comm-list-number { deny | permit } { rt
route-target | soo site-of-origin }&<1-32>

#### 1.8 配置路由策略

##### 1.8.1 创建路由策略

##### 1. 功能简介

路由策略中至少应该有一个节点的匹配模式是permit。如果路由策略的所有节点都是deny 模式，则没有路由信息能通过该路由策略。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 创建路由策略，并进入该路由策略视图。
route-policy route-policy-name { deny | permit } node node-number

##### 1.8.2 配置if-match子句

###### 1. 功能简介

在一个节点中，可以没有 if-match 子句，也可以有多个 if-match 子句。当不指定 if-match子句时，如果该节点的匹配模式为允许模式，则所有路由信息都会通过该节点的过滤；如果该节点的匹配模式为拒绝模式，则所有路由信息都会被拒绝。

###### 2. 配置限制和指导

如果配置了多条相同类型的 if-match 子句，设备在显示路由策略时，会将这些 if-match 子句合并为一条 if-match 子句。如果合并后的 if-match 子句超过命令行最大长度，则这些相同类型的 if-match 子句会分成多条显示，这些子句之间是“或”的关系，即满足一个匹配条件，就认为匹配该 语句，例如出现多条 子句时，各个子句的团体属性if-match if-match community之间是“或”的关系，即满足其中一个团体属性，就认为匹配 if-match community 子句。
如果一个节点中 if-match 子句只指定了 IPv6 ACL，没有指定 IPv4 ACL，所有的 IPv4 路由信息都会匹配这个节点。如果一个节点中 if-match 子句只指定 IPv4 ACL，没有指定 IPv6 ACL，所有的 IPv6 路由信息都会匹配这个节点。
如果 if-match 子句对应的 ACL 不存在，则默认满足该匹配条件。如果 if-match 子句对应的中没有匹配的 规则或者 规则处于非激活状态，则默认不满足该匹配条件。
ACL ACL ACL如果 子句对应的前缀列表、团体属性列表或扩展团体属性列表不存在，则默认满足该匹if-match配条件。如果 if-match 子句对应的前缀列表、团体属性列表或扩展团体属性列表中没有匹配的规则，则默认不满足该匹配条件。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入路由策略视图。
route-policy route-policy-name { deny | permit } node node-number
(3) 配置通过 ACL 或 IP 地址前缀列表匹配路由。
（IPv4 网络）
if-match ip { address | next-hop | route-source } { acl ipv4-acl-number |
prefix-list prefix-list-name }
（IPv6 网络）
if-match ipv6 { address | next-hop | route-source } { acl ipv6-acl-number
| prefix-list prefix-list-name }
缺省情况下，未配置通过 或 地址前缀列表匹配路由。
ACL IP
路由策略使用非 的 进行路由过滤。
VPN ACL

(4) 配置 BGP 路由信息的匹配条件。
配置 BGP 路由信息的 AS 路径匹配条件。
(cid:123)
if-match as-path as-path-number&<1-32>
配置匹配 BGP 路由信息的团体属性匹配条件。
(cid:123)
if-match community { { basic-community-list-number | name
comm-list-name } [ whole-match ] | adv-community-list-number }&<1-32>
配置 BGP 路由的扩展团体属性匹配条件。
(cid:123)
if-match extcommunity ext-comm-list-number&<1-32>
配置 BGP 路由信息的本地优先级匹配条件。
(cid:123)
if-match local-preference preference
配置 BGP RPKI 验证结果的匹配条件。
(cid:123)
if-match rpki { invalid | not-found | valid }
缺省情况下，未配置 BGP 路由信息匹配条件。
(5) 配置基于路由信息的匹配条件。
配置路由信息的路由开销匹配条件。
(cid:123)
if-match cost cost-value
配置路由信息的出接口匹配条件。
(cid:123)
if-match interface { interface-type interface-number }&<1-16>
将路由策略应用到 BGP 时，BGP 协议不支持配置路由信息的出接口匹配条件。
配置路由信息类型匹配条件。
(cid:123)
if-match route-type { bgp-evpn-imet | bgp-evpn-ip-prefix |
bgp-evpn-mac-ip | external-type1 | external-type1or2 | external-type2
| internal | is-is-level-1 | is-is-level-2 | nssa-external-type1 |
nssa-external-type1or2 | nssa-external-type2 } *
配置 路由信息标记的匹配条件。
IGP
(cid:123)
if-match tag tag-value
缺省情况下，未配置基于路由信息的匹配条件。
(6) 配置 L3VNI 的匹配条件。
if-match l3-vni vxlan-id
缺省情况下，未配置 L3VNI 的匹配条件。

##### 1.8.3 配置apply子句

(1) 进入系统视图。
system-view
进入路由策略视图。
(2)
route-policy route-policy-name { deny | permit } node node-number
配置 路由属性。
(3) BGP
配置 路由的 属性。
BGP AS_PATH
(cid:123)

apply as-path as-number&<1-32> [ replace ]删除 BGP 路由的团体属性。
(cid:123)
apply comm-list { comm-list-number | comm-list-name } delete缺省情况下，没有删除 BGP 路由的团体属性。
配置 BGP 路由的团体属性。
(cid:123)
apply community { none | additive | { community-number&<1-32> | aa:nn&<1-32> | internet | no-advertise | no-export | no-export-subconfed } * [ additive ] }配置 路由的 扩展团体属性。
BGP RT (cid:123)
apply extcommunity { rt route-target }&<1-32> [ additive ]配置 路由的 扩展团体属性。
BGP SoO (cid:123)
apply extcommunity soo site-of-origin&<1-32> [ additive ]配置 路由的本地优先级。
BGP (cid:123)
apply local-preference preference配置 BGP 路由的 ORIGIN 属性。
(cid:123)
apply origin { egp as-number | igp | incomplete }配置 BGP 路由的首选值。
(cid:123)
apply preferred-value preferred-value配置 BGP 路由的流量索引。
(cid:123)
apply traffic-index { value | clear }缺省情况下，未配置 BGP 路由属性。
(4) 配置路由开销。
配置路由信息的路由开销。
(cid:123)
apply cost [ + | - ] cost-value缺省情况下，未配置路由信息的路由开销。
配置路由信息的开销类型。
(cid:123)
apply cost-type { external | internal | type-1 | type-2 }缺省情况下，未配置路由信息的开销类型。
配置路由信息的下一跳地址。
(5)
（IPv4 网络）
apply ip-address next-hop ip-address [ public | vpn-instance vpn-instance-name ]（IPv6 网络）
apply ipv6 next-hop ipv6-address缺省情况下，未配置路由信息的下一跳地址。
对于引入的路由，使用本命令设置下一跳地址无效。
配置路由优先级。
(6)
配置路由的 优先级。
IP (cid:123)

apply ip-precedence { value | clear }缺省情况下，未配置路由的 IP 优先级。
配置路由协议的优先级。
(cid:123)
apply preference preference缺省情况下，未配置路由协议的优先级。
配置路由收敛优先级。
(cid:123)
apply prefix-priority { critical | high | medium }缺省情况下，路由收敛优先级为低（Low）。
(7) 配置引入路由到 IS-IS 某个级别的区域。
apply isis { level-1 | level-1-2 | level-2 }缺省情况下，未配置引入路由到 IS-IS 某个级别的区域。
(8) 配置 IGP 路由信息的标记。
apply tag tag-value缺省情况下，未配置 IGP 路由信息的标记。
(9) 配置快速重路由备份。
（IPv4 网络）
apply fast-reroute { backup-interface interface-type interface-number [ backup-nexthop ip-address ] | backup-nexthop ip-address }（IPv6 网络）
apply ipv6 fast-reroute { backup-interface interface-type interface-number [ backup-nexthop ipv6-address ] | backup-nexthop ipv6-address }缺省情况下，未配置快速重路由备份。
(10) 配置 L3VNI。
apply l3-vni vxlan-id缺省情况下，未配置 L3VNI。

##### 1.8.4 配置continue子句

###### 1. 配置限制和指导

当配置 continue 子句的多个节点配置相同的 apply 子句（没有叠加属性）只是子句的值不相同时，以最后一个节点的 子句为准；如果配置的是有叠加属性的 子句（命令apply apply apply as-path 不指定参数 replace/命令 apply cost 指定参数+或-/命令 apply community 指定参数 additive/命令 apply extcommunity 指定参数 additive），属性会全部叠加到路由上。
当配置 continue 子句的多个节点配置 apply community 子句时，使用命令行 apply comm-list delete 不能删除前面节点中配置的团体属性。

###### 2. 配置步骤

进入系统视图。
(1)
system-view

##### 1.10.1 在RIP中引入静态路由时应用路由策略配置举例

(2) 进入路由策略视图。
route-policy route-policy-name { deny | permit } node node-number
(3) 配置下一个执行节点。
continue [ node-number ]
缺省情况下，未配置下一个执行节点。
下一个执行节点序列号必须大于当前节点序列号。

#### 1.9 路由策略显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后路由策略的运行情况，通过查看显示信息验证配置的效果。
在用户视图下执行 reset 命令可以清除路由策略的统计信息。
表1-1 路由策略显示和维护操作 命令显示BGP AS路径过滤列表信息 display ip as-path [ as-path-number ] display ip community-list显示BGP团体属性列表信息 [ basic-community-list-number | adv-community-list-number | name comm-list-name ]显示BGP扩展团体属性列表信息 display ip extcommunity-list [ ext-comm-list-number ]显示IPv4地址前缀列表的统计信息 display ip prefix-list [ name prefix-list-name ]显示IPv6地址前缀列表的统计信息 display ipv6 prefix-list [ name prefix-list-name ]显示路由策略信息 display route-policy [ name route-policy-name ]清除IPv4地址前缀列表的统计信息 reset ip prefix-list [ prefix-list-name ]清除IPv6地址前缀列表的统计信息 reset ipv6 prefix-list [ prefix-list-name ]

#### 1.10 路由策略典型配置举例

在 中引入静态路由时应用路由策略配置举例
1.10.1 RIP

###### 1. 组网需求

与 通信，都运行 协议。
• Switch A Switch B RIP使能 上的 协议，配置三条静态路由。
• Switch A RIP设置在引入静态路由时应用路由策略，使三条静态路由部分引入、部分被屏蔽掉
•
——20.1.1.1/32 和 40.1.1.1/32 网段的路由是可见的，30.1.1.1/32 网段的路由则被屏蔽。
• 通过在 Switch B 上查看 RIP 路由表，验证路由策略是否生效。

###### 3. 配置步骤

###### 2. 组网图

图1-1 在 RIP 中引入静态路由时应用路由策略配置举例
20.1.1.1/32
30.1.1.1/32
40.1.1.1/32 Vlan-int200 Vlan-int100 Vlan-int100
11.1.1.1/30
10.1.1.1/30 10.1.1.2/30 Switch A Switch B配置步骤
3.
(1) 配置 Switch A \# 配置接口 vlan-interface 100 和 vlan-interface 200 的 IP 地址。
<SwitchA> system-view [SwitchA] interface vlan-interface 100 [SwitchA-vlan-interface100] ip address 10.1.1.1 30 [SwitchA-vlan-interface100] quit [SwitchA] interface vlan-interface 200 [SwitchA-vlan-interface200] ip address 11.1.1.1 30 [SwitchA-vlan-interface200] quit \# 在接口 vlan-interface 100 下使能 RIP。
[SwitchA] interface vlan-interface 100 [SwitchA-vlan-interface100] rip 1 enable [SwitchA-vlan-interface100] quit \# 配置三条静态路由，其下一跳为 11.1.1.2，保证静态路由为 active 状态。
[SwitchA] ip route-static 20.1.1.1 32 11.1.1.2 [SwitchA] ip route-static 30.1.1.1 32 11.1.1.2 [SwitchA] ip route-static 40.1.1.1 32 11.1.1.2 \# 配置路由策略。
[SwitchA] ip prefix-list a index 10 permit 30.1.1.1 32 [SwitchA] route-policy static2rip deny node 0 [SwitchA-route-policy-static2rip-0] if-match ip address prefix-list a [SwitchA-route-policy-static2rip-0] quit [SwitchA] route-policy static2rip permit node 10 [SwitchA-route-policy-static2rip-10] quit启动 协议，同时应用路由策略 对引入的静态路由进行过滤。
\# RIP static2rip [SwitchA] rip [SwitchA-rip-1] import-route static route-policy static2rip
(2) 配置 Switch B \# 配置接口 vlan-interface 100 的 IP 地址。
<SwitchB> system-view [SwitchB] interface vlan-interface 100 [SwitchB-vlan-interface100] ip address 10.1.1.2 30 \# 启动 RIP 协议。

[SwitchB] rip [SwitchB-rip-1] quit \# 在接口下使能 RIP。
[SwitchB] interface vlan-interface 100 [SwitchB-vlan-interface100] rip 1 enable [SwitchB-vlan-interface100] quit

###### 4. 验证配置

\# 查看 Switch B 的 RIP 路由表。
[SwitchB] display ip routing-table Destinations : 14 Routes : 14 Destination/Mask Proto Pre Cost NextHop Interface
0.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
10.1.1.0/30 Direct 0 0 10.1.1.2 Vlan100
10.1.1.0/32 Direct 0 0 10.1.1.2 Vlan100
10.1.1.2/32 Direct 0 0 127.0.0.1 InLoop0
10.1.1.3/32 Direct 0 0 10.1.1.2 Vlan100
20.0.0.0/8 RIP 100 1 10.1.1.1 Vlan100
40.0.0.0/8 RIP 100 1 10.1.1.1 Vlan100
127.0.0.0/8 Direct 0 0 127.0.0.1 InLoop0
127.0.0.0/32 Direct 0 0 127.0.0.1 InLoop0
127.0.0.1/32 Direct 0 0 127.0.0.1 InLoop0
127.255.255.255/32 Direct 0 0 127.0.0.1 InLoop0
224.0.0.0/4 Direct 0 0 0.0.0.0 NULL0
224.0.0.0/24 Direct 0 0 0.0.0.0 NULL0
255.255.255.255/32 Direct 0 0 127.0.0.1 InLoop0

##### 1.10.2 在OSPF中引入IS-IS路由时应用路由策略配置举例

###### 1. 组网需求

• Switch B 与 Switch A 之间通过 OSPF 协议交换路由信息，与 Switch C 之间通过 IS-IS 协议交
换路由信息。
• 要求在 Switch B 上配置路由引入，将 IS-IS 路由引入到 OSPF 中去，并同时使用路由策略设
置路由的属性。其中，设置 172.17.1.0/24 的路由的开销为 100，设置 172.17.2.0/24 的路由
的 属性为 20。
Tag

###### 2. 组网图

图1-2 在 OSPF 中引入 IS-IS 路由时应用路由策略配置组网图IS-IS OSPF Vlan-int100 Vlan-int200
192.168.1.2/24 192.168.2.2/24 Switch B Vlan-int201
172.17.1.1/24 Vlan-int100 Vlan-int200
192.168.1.1/24 Vlan-int202
192.168.2.1/24
172.17.2.1/24 Switch A Switch C Vlan-int203
172.17.3.1/24

###### 3. 配置步骤

配置各接口的 地址（略）
(1) IP配置 路由协议
(2) IS-IS配置 C。
\# Switch <SwitchC> system-view [SwitchC] isis [SwitchC-isis-1] is-level level-2 [SwitchC-isis-1] network-entity 10.0000.0000.0001.00 [SwitchC-isis-1] quit [SwitchC] interface vlan-interface 200 [SwitchC-Vlan-interface200] isis enable [SwitchC-Vlan-interface200] quit [SwitchC] interface vlan-interface 201 [SwitchC-Vlan-interface201] isis enable [SwitchC-Vlan-interface201] quit [SwitchC] interface vlan-interface 202 [SwitchC-Vlan-interface202] isis enable [SwitchC-Vlan-interface202] quit [SwitchC] interface vlan-interface 203 [SwitchC-Vlan-interface203] isis enable [SwitchC-Vlan-interface203] quit \# 配置 Switch B。
<SwitchB> system-view [SwitchB] isis [SwitchB-isis-1] is-level level-2 [SwitchB-isis-1] network-entity 10.0000.0000.0002.00 [SwitchB-isis-1] quit [SwitchB] interface vlan-interface 200 [SwitchB-Vlan-interface200] isis enable [SwitchB-Vlan-interface200] quit

(3) 配置 OSPF 路由协议及路由引入
\# 配置 Switch A，启动 OSPF。
<SwitchA> system-view
[SwitchA] ospf
[SwitchA-ospf-1] area 0
[SwitchA-ospf-1-area-0.0.0.0] network 192.168.1.0 0.0.0.255
[SwitchA-ospf-1-area-0.0.0.0] quit
[SwitchA-ospf-1] quit
\# 配置 Switch B，启动 OSPF，并引入 IS-IS 路由。
[SwitchB] ospf
[SwitchB-ospf-1] area 0
[SwitchB-ospf-1-area-0.0.0.0] network 192.168.1.0 0.0.0.255
[SwitchB-ospf-1-area-0.0.0.0] quit
[SwitchB-ospf-1] import-route isis 1
[SwitchB-ospf-1] quit
\# 查看 SwitchA 的 OSPF 路由表，可以看到引入的路由。
[SwitchA] display ospf routing
OSPF Process 1 with Router ID 192.168.1.1
Routing Tables
Routing for Network
Destination Cost Type NextHop AdvRouter Area
192.168.1.0/24 1 Stub 192.168.1.1 192.168.1.1 0.0.0.0
Routing for ASEs
Destination Cost Type Tag NextHop AdvRouter
172.17.1.0/24 1 Type2 1 192.168.1.2 192.168.2.2
172.17.2.0/24 1 Type2 1 192.168.1.2 192.168.2.2
172.17.3.0/24 1 Type2 1 192.168.1.2 192.168.2.2
Total Nets: 4
Intra Area: 1 Inter Area: 0 ASE: 3 NSSA: 0
配置过滤列表
(4)
配置编号为 的基本 ACL，允许 的路由通过。
\# 2002 172.17.2.0/24
[SwitchB] acl basic 2002
[SwitchB-acl-ipv4-basic-2002] rule permit source 172.17.2.0 0.0.0.255
[SwitchB-acl-ipv4-basic-2002] quit
\# 配置名为 prefix-a 的地址前缀列表，允许 172.17.1.0/24 的路由通过。
[SwitchB] ip prefix-list prefix-a index 10 permit 172.17.1.0 24
(5) 配置路由策略
[SwitchB] route-policy isis2ospf permit node 10
[SwitchB-route-policy-isis2ospf-10] if-match ip address prefix-list prefix-a
[SwitchB-route-policy-isis2ospf-10] apply cost 100
[SwitchB-route-policy-isis2ospf-10] quit
[SwitchB] route-policy isis2ospf permit node 20

[SwitchB-route-policy-isis2ospf-20] if-match ip address acl 2002 [SwitchB-route-policy-isis2ospf-20] apply tag 20 [SwitchB-route-policy-isis2ospf-20] quit [SwitchB] route-policy isis2ospf permit node 30 [SwitchB-route-policy-isis2ospf-30] quit
(6) 在路由引入时应用路由策略配置 B，设置在路由引入时应用路由策略。
\# Switch [SwitchB] ospf [SwitchB-ospf-1] import-route isis 1 route-policy isis2ospf [SwitchB-ospf-1] quit查看 的 路由表，可以看到目的地址为 的路由的开销为 100，\# Switch A OSPF 172.17.1.0/24目的地址为 172.17.2.0/24 的路由的标记域（Tag）为 20，而其他外部路由没有变化。
[SwitchA] display ospf routing OSPF Process 1 with Router ID 192.168.1.1 Routing Tables Routing for Network Destination Cost Type NextHop AdvRouter Area
192.168.1.0/24 1 Transit 192.168.1.1 192.168.1.1 0.0.0.0 Routing for ASEs Destination Cost Type Tag NextHop AdvRouter
172.17.1.0/24 100 Type2 1 192.168.1.2 192.168.2.2
172.17.2.0/24 1 Type2 20 192.168.1.2 192.168.2.2
172.17.3.0/24 1 Type2 1 192.168.1.2 192.168.2.2 Total Nets: 4 Intra Area: 1 Inter Area: 0 ASE: 3 NSSA: 0

##### 1.10.3 在IPv6路由引入中应用路由策略配置举例

###### 1. 组网需求

在 Switch A 和 Switch B 上使能 RIPng 。
•在 Switch A 上配置三条静态路由，并设置在引入静态路由时应用路由策略，使三条静态路由
•部分引入、部分被屏蔽掉——20::/32 和 网段的路由是可见的，30::/32 网段的路由则40::/32被屏蔽。
• 通过在 Switch B 上查看 RIPng 路由表，验证路由策略是否生效。

###### 3. 配置步骤

###### 2. 组网图

图1-3 在 IPv6 路由引入中应用路由策略配置组网图配置步骤
3.
(1) 配置 Switch A \# 配置接口 Vlan-interface100 和 Vlan-interface200 的 IPv6 地址。
<SwitchA> system-view [SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] ipv6 address 10::1 32 [SwitchA-Vlan-interface100] quit [SwitchA] interface vlan-interface 200 [SwitchA-Vlan-interface200] ipv6 address 11::1 32 [SwitchA-Vlan-interface200] quit \# 在接口下使能 RIPng。
[SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] ripng 1 enable [SwitchA-Vlan-interface100] quit \# 配置三条静态路由，其下一跳为 11::2，保证静态路由为 active 状态。
[SwitchA] ipv6 route-static 20:: 32 11::2 [SwitchA] ipv6 route-static 30:: 32 11::2 [SwitchA] ipv6 route-static 40:: 32 11::2 \# 配置路由策略。
[SwitchA] ipv6 prefix-list a index 10 permit 30:: 32 [SwitchA] route-policy static2ripng deny node 0 [SwitchA-route-policy-static2ripng-0] if-match ipv6 address prefix-list a [SwitchA-route-policy-static2ripng-0] quit [SwitchA] route-policy static2ripng permit node 10 [SwitchA-route-policy-static2ripng-10] quit启动 协议并引入静态路由。
\# RIPng [SwitchA] ripng [SwitchA-ripng-1] import-route static route-policy static2ripng
(2) 配置 Switch B \# 配置接口 Vlan-interface100 的 IPv6 地址。
<SwitchB> system-view [SwitchB] interface vlan-interface 100 [SwitchB-Vlan-interface100] ipv6 address 10::2 32 \# 启动 RIPng 协议。

[SwitchB] ripng [SwitchB-ripng-1] quit \# 在接口下使能 RIPng。
[SwitchB] interface vlan-interface 100 [SwitchB-Vlan-interface100] ripng 1 enable [SwitchB-Vlan-interface100] quit

###### 4. 验证配置

\# 查看 Switch B 的 RIPng 路由表。
[SwitchB] display ripng 1 route Route Flags: A - Aging, S - Suppressed, G - Garbage-collect
---------------------------------------------------------------- Peer FE80::7D58:0:CA03:1 on Vlan-interface 100 Destination 20::/32, via FE80::7D58:0:CA03:1, cost 1, tag 0, A, 8 secs Destination 40::/32, via FE80::7D58:0:CA03:1, cost 1, tag 0, A, 3 secs Local route Destination 10::/32, via ::, cost 0, tag 0, DOF
