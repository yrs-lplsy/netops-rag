# S1700, S5700, S6700 V600R025C00 配置指南-以太网交换 01-08 VBST配置

## 8 VBST配置

8 VBST 配置

### 8.1 VBST简介

8.2 VBST原理描述
8.3 VBST 配置注意事项
8.4 VBST缺省配置
8.5 配置VBST基本功能
8.6 启用边缘端口和配置BPDU报文过滤功能
8.7 配置影响VBST拓扑收敛的参数
8.8 配置VBST保护功能
8.9 配置设备支持和其他厂商设备互通的参数
8.10 维护VBST
8.11 VBST配置举例
8.1 VBST 简介
定义
VBST（VLAN-Based Spanning Tree）是华为提出的一种生成树协议，通过它可在每个
VLAN内构建一棵生成树，使不同VLAN内的流量通过不同的生成树转发。VBST可以简
单理解为在每个VLAN上运行一个STP或RSTP协议，不同VLAN之间的生成树完全独
立。
目的
以太网中为了进行链路备份，提高网络可靠性，通常会使用冗余链路，但是这也带来
了网络环路的问题。网络环路会引发广播风暴和MAC地址表振荡等问题，导致用户通
信质量差，甚至通信中断。为了解决环路问题，IEEE先后提出了生成树协议STP
（Spanning Tree Protocol）、快速生成树协议RSTP（Rapid Spanning Tree
Protocol ）、多生成树协议 MSTP （ Multiple Spanning Tree Protocol ）。
STP和RSTP不能按VLAN阻塞冗余链路，局域网内所有的VLAN共享一棵生成树，所有
VLAN的报文都沿着一棵生成树进行转发，因此无法在VLAN间实现流量的负载分担；

同时，链路被阻塞后将不承载任何流量，造成带宽浪费，还有可能造成部分VLAN的报文无法转发。
MSTP弥补了STP和RSTP的缺陷，兼容STP和RSTP，既可以快速收敛，又提供了数据转发的多个路径，在数据转发过程中实现VLAN数据的负载均衡。但MSTP中多实例和多进程的概念比较抽象，且配置较为复杂。
为了解决上述问题，华为公司提出了VBST。VBST中生成树的形成是基于VLAN的，不同VLAN间可形成相互独立的生成树，不同VLAN内的流量沿着各自的生成树转发，进而可实现流量的负载分担。同时，对用户来说，VBST没有多实例、多进程的概念，更容易理解，配置维护也简单。
STP、RSTP、MSTP和VBST均可以实现破除环路和链路备份，这几种生成树协议的详细对比请参见表8-1。
表 8-1 生成树协议的比较

| 生成树协议 | 收敛速度 | 流量转发 | 配置复杂度 |
|---|---|---|---|
| STP（基于 IEEE 802.1d 标准） | 最慢 | 所有VLAN共享一棵生成树，所有VLAN 的流量按照同样的路径转发。 | 低 |
| RSTP（基于 IEEE 802.1w 标准） | RSTP、MSTP、 VBST比STP收敛速度快，但 RSTP、MSTP、 VBST之间没有快慢之分。 | 所有VLAN共享一棵生成树，所有VLAN 的流量按照同样的路径转发。 | 低 |
| MSTP（基于 IEEE 802.1s 标准） |  | 通过实例与VLAN的映射，可以实现多棵生成树在VLAN间负载分担，不同VLAN 的流量按照不同的路径转发。每棵生成树之间相互独立。 | 高 |
| VBST |  | 一个VLAN对应一棵生成树，不同VLAN 的流量按照不同的路径转发。每棵生成树之间相互独立。 VBST支持与PVST、PVST+、Rapid PVST +协议互通。 | 中 |

### 8.2 VBST原理描述

VBST 基本原理VBST可以简单理解为在每个VLAN上运行一个STP或RSTP，不同VLAN之间的生成树计算完全独立，可以实现对不同VLAN的流量进行负载分担。网络中每台设备的角色、设备上每个端口的角色以及端口状态确定后，生成树计算收敛完成，网络达到一个稳定状态。
设备角色：
VBST 基于每个 VLAN 计算出一棵生成树：每个生成树包含一个根桥 RB （ Root Bridge）；除根桥外，网络中其他设备均为非根桥设备。
端口角色：

VBST支持根端口、指定端口、Alternate端口、Backup端口和边缘端口，与RSTP类似，详细介绍请参见STP/RSTP/MSTP配置中的“设备角色、端口角色和端口状态”。
端口状态：
VBST支持的端口状态有Forwarding、Learning、Discarding，与STP/RSTP/MSTP类似，详细介绍请参见STP/RSTP/MSTP配置中的“设备角色、端口角色和端口状态”。
定时器：
VBST支持的定时器包括Hello Time、Forward Delay、Max Age，与STP/RSTP/MSTP类似，详细介绍请参见STP/RSTP/MSTP配置中的“生成树协议定时器”。
VBST报文：
VBST网络中，设备之间通过交互VBST报文来进行生成树拓扑计算。与STP/RSTP报文相比，VBST报文有以下几点不同：
● 如图8-1所示，VBST报文中的DMAC填充0100-0CCC-CCCD，而STP/RSTP报文中DMAC填充0180-C200-0000。
● 如图8-1所示，VBST报文在源MAC地址字段和协议长度字段之间加入了四字节的
802.1q Tag 。
● 如图8-1所示，VBST报文中的Data字段依据对接设备填充STP/RSTP报文，默认填充RSTP报文。但在STP/RSTP报文末尾会增加一个6字节的Originating VLAN字段，具体包括Type、Length和VLAN ID。
– Type：长度2字节，取值固定为0x0000。
– Length：长度2字节，取值固定为2。
– VLAN ID：长度2字节，取值为发送该报文的原始VLAN ID。
● VBST报文中桥ID的构成与STP/RSTP/MSTP略有不同，桥优先级占据高4位，VLAN ID占据随后的12位，其余的低48位是MAC地址。

图 8-1 STP/RSTP 报文与 VBST 报文的封装格式对比图VBST 拓扑计算VBST支持基于VLAN的拓扑计算，每个VLAN都会发送带有VLAN Tag报文的VBST报文，拓扑计算独立进行，拓扑计算方法跟STP/RSTP相同（详细介绍请参见STP/RSTP/ MSTP配置中的"STP/RSTP拓扑计算方法"）。如图8-2所示：
● STP/RSTP协议通过拓扑计算，在网络中生成一棵根桥为DeviceD的生成树，DeviceA 和 DeviceF 之间、 DeviceB 和 DeviceE 之间的链路被阻塞。这样， HostB 和HostD同属于VLAN2，由于DeviceB和DeviceE之间的链路被阻塞，DeviceC和DeviceD之间的链路又不允许VLAN2的报文通过，因此HostB和HostD之间无法互相通讯。

● VBST协议通过拓扑计算，在网络中分别生成根桥为DeviceF的VLAN2生成树和根
桥为DeviceD的VLAN3生成树，VLAN2、VLAN3的流量分别沿着各自的生成树转
发，流量就分担在DeviceB-DeviceE、DeviceC-DeviceD两条路径上，实现了不同
VLAN内流量的负载分担。
图 8-2 STP/RSTP 与 VBST 的拓扑计算结果对比图
VBST 快速收敛机制
VBST支持普通P/A机制和增强P/A机制，详细介绍请参见STP/RSTP/MSTP配置中的
"RSTP/MSTP快速收敛机制"。

VBST 保护功能VBST支持BPDU保护、TC保护、根保护和环路保护，详细介绍请参见STP/RSTP/MSTP配置中的"了解RSTP/MSTP保护功能"。
VBST 与 STP/RSTP 互通现网中存在VBST设备与STP/RSTP设备混合组网的场景。由于VBST报文与STP/RSTP报文的格式不同，所以存在如何互通的问题。为了实现与STP/RSTP互通：
● 对于Access端口，VBST设备将只根据此端口所在的VLAN使用STP报文（对接STP设备）或RSTP报文（对接RSTP设备）与对端交互。这样，拓扑计算将按照STP/ RSTP协议进行，STP/RSTP协议不区分VLAN，所以最终形成一棵各VLAN共享的生成树。
● 对于Trunk端口
– VBST设备和RSTP设备对接时，在VLAN 1内，VBST设备使用RSTP报文与对端交互，其他VLAN内使用填充RSTP Data的VBST报文与对端交互。
– VBST设备和STP设备对接时，在VLAN 1内，VBST设备使用STP报文与对端交互，其他 VLAN 内使用填充 STP Data 的 VBST 报文与对端交互。
下面结合图8-3介绍生成树形成原理。DeviceA和DeviceB部署STP/RSTP，DeviceC和DeviceD部署VBST，假设各设备间均采用Trunk端口连接，DeviceA、DeviceB、DeviceC和DeviceD的各接口上均允许VLAN 1和VLAN 10通过。
由于STP/RSTP设备只能收发STP/RSTP报文，对于VBST报文只能透传。因此，在VLAN 1内，系统将按STP/RSTP协议形成一棵生成树。
说明当STP/RSTP设备为园区交换机时，不支持透传VBST报文。

图 8-3 VBST 通过 Trunk 端口和 STP/RSTP 协议互通示意图假设VLAN 1的生成树的阻塞点在DeviceD上。DeviceD运行VBST协议，阻塞只针对VLAN 1，DeviceD仍然可以接收并转发VLAN 10的VBST报文，VLAN 10内也存在环路，系统触发VLAN 10的生成树计算。由于DeviceA、DeviceB直接透传VLAN 10的VBST报文，所以只有DeviceC和DeviceD上的四个端口参与VLAN 10的生成树计算。最终可形成如图8-3所示的VLAN 1和VLAN 10生成树。
假设VLAN 1的生成树的阻塞点在DeviceB上。DeviceB运行STP/RSTP协议，阻塞针对端口，DeviceB无法转发VLAN 10的VBST报文，VLAN 10内不存在环路，系统不会触发VLAN 10的生成树计算。但VLAN 10的VBST报文可沿VLAN 1的生成树转发，可认为VLAN 10 与 VLAN 1 共享生成树，如图 8-3 所示。
可见，在与STP/RSTP对接时，只有使用Trunk端口对接且阻塞点设置在VBST设备的方案才能实现负载分担，所以推荐使用此对接互通方案。
VBST 与 PVST/PVST+/Rapid PVST+协议互通现网中也存在VBST设备与PVST/PVST+/Rapid PVST+设备混合组网的场景。
● 对于Access端口VBST 设备将只根据此端口所在 VLAN 使用 STP （对接 PVST/PVST+ 设备）或 RSTP（对接Rapid PVST+设备）报文与对端交互。这样，拓扑计算将按照STP/RSTP协议进行，由于STP/RSTP协议不区分VLAN，所以最终形成一棵各VLAN共享的生成树。

● 对于Trunk端口
– VBST设备和Rapid PVST+设备对接时，在VLAN 1中，VBST设备使用RSTP报
文与对端交互（也会同时发填充RSTP Data的VBST报文），其他VLAN内使用
RSTP Data填充的VBST报文与对端交互。
– VBST设备和PVST+设备对接时，在VLAN 1中，VBST设备使用STP报文与对端
交互（也会同时发填充STP Data的VBST报文），其他VLAN内使用STP Data
填充的VBST报文与对端交互。
– VBST设备和PVST设备对接时，报文交互跟VBST与PVST+对接类似。区别在
于，在VLAN 1中，VBST设备和PVST设备之间只发送填充STP Data的VBST报
文交互。
两端报文可互相识别且均携带VLAN信息，因此可基于VLAN生成生成树。因此，
VBST设备与PVST/PVST+/Rapid PVST+设备使用Trunk端口对接时，就如同VBST
设备跟VBST设备对接一样。

### 8.3 VBST配置注意事项

License 依赖VBST无需License许可即可使用。
硬件依赖表 8-2 支持本特性的硬件

| 系列 | 支持产品 |
|---|---|
| S6750-H | S6750-H36C，S6750-H48X8C，S6750-H48Y8C |
| S1730S-S3 | S1730S-S24P4S-A3，S1730S-S24P4X-A3， S1730S-S24T4S-QA3，S1730S-S24T4X-QA3， S1730S-S48P4S-A3，S1730S-S48T4S-A3， S1730S-S48T4X-A3，S1730S-S8P4X-QA3， S1730S-S8T4X-QA3 |
| S6730E-H-V2 | S6730E-H6FX4Y2CZ-V2 |
| S5735E-S-V2 | S5735E-S24HJ4XE-V2，S5735E-S24HS4XE-V2， S5735E-S24J4XE-V2，S5735E-S48HJ4XE-V2， S5735E-S48HS4XE-V2，S5735E-S48J4XE-V2 |

| 系列 | 支持产品 |
|---|---|
| S5735-S-V2 | S5735-S24HJ4XE-V2，S5735-S24HS4XE-V2， S5735-S24J4XE-V2，S5735-S24P4XE-V2，S5735- S24P4XEZ-V2，S5735-S24P8J4XEZ-V2，S5735- S24PN4XE-V2，S5735-S24ST4XE-V2，S5735- S24T4XE-C-V2，S5735-S24T4XE-V2，S5735- S24T4XEZ-V2，S5735-S24T8J4XE-XA-V2，S5735- S24T8J4XEZ-V2，S5735-S24U4XE-V2，S5735- S48HJ4XE-V2，S5735-S48HS4XE-V2，S5735- S48J4XE-V2，S5735-S48P4XE-V2，S5735- S48P4XEZ-V2，S5735-S48PN4XE-V2，S5735- S48S4XE-V2，S5735-S48T4XE-C-V2，S5735- S48T4XE-V2，S5735-S48T4XE-XA-V2，S5735- S48T4XEZ-V2，S5735-S48U4XE-V2 |
| S5735S-S3 | S5735S-S24P4X-A3，S5735S-S48P4X-A3 |
| S6750E-S | S6750E-S16X10Y2CZ，S6750E-S24T16X8Y2CZ |
| S5735I-L-V2 | S5735I-L10T4X-A-V2，S5735I-L8P4X-A-V2 |
| S6730-H-V2 | S6730-H24X6C-V2，S6730-H28X6CZ-V2，S6730- H48X6C-TV2，S6730-H48X6C-V2，S6730- H48X6CZ-V2，S6730-H48Y6C-TV2，S6730- H48Y6C-V2，S6730-H6FX4Y2CZ-V2 |
| S5735I-H-V2 | S5735I-H24U8S4XE-QA-V2，S5735I-H8T2XN- V2，S5735I-H8T4S2XN-V2，S5735I-H8U2XN-V2 |
| S6750-S | S6750-S16X10Y2CZ，S6750-S16X8YZ，S6750- S24T16X8Y2CZ |
| S5735S-L3 | S5735S-L24P4S-A3，S5735S-L24P4XE-A3， S5735S-L24PN4XE-A3，S5735S-L24ST4X-A3， S5735S-L24T4S-QA3，S5735S-L24T4X-QA3， S5735S-L24T8J4XE-A3，S5735S-L48P4S-A3， S5735S-L48P4XE-A3，S5735S-L48PN4XE-A3， S5735S-L48S4X-A3，S5735S-L48T4S-A3，S5735S- L48T4XE-A3，S5735S-L8P4X-QA3，S5735S- L8T4X-QA3 |
| S5755-H | S5755-H24HB2Y2CZ，S5755-H24N4Y-A，S5755- H24P4Y2CZ，S5755-H24T4Y2CZ，S5755- H24U4Y2CZ，S5755-H24UM4Y2CZ，S5755- H24UN4Y2CZ，S5755-H24UTM4X4Y2C，S5755- H48N4Y-A，S5755-H48P4Y2CZ，S5755- H48T4Y2CZ，S5755-H48T4Y2CZ-B，S5755- H48U4Y2CZ，S5755-H48UM4Y2CZ，S5755- H48UN4Y2CZ，S5755-H48UTM4X4Y2C |
| S5735R-S-V2 | S5735R-S24P4X-V2，S5735R-S24T8J4X-XA-V2， S5735R-S48P4X-V2，S5735R-S48T4X-XA-V2 |
| S6780-H | S6780-H4Z |

| 系列 | 支持产品 |
|---|---|
| S5735E-L-V2 | S5735E-L16LP2UM2X-QA-V2，S5735E-L16LP2X- QA-V2，S5735E-L24HJ4XE-A-V2，S5735E- L24P4S-A-V2，S5735E-L24P4XE-A-V2，S5735E- L24ST4XE-A-V2，S5735E-L24T4XE-A-V2， S5735E-L48LP4S-A-V2，S5735E-L48LP4XE-A-V2， S5735E-L48S4XE-A-V2，S5735E-L48T4XE-A-V2， S5735E-L8P4X-QA-V2，S5735E-L8T4X-QA-V2 |
| S5755-S | S5755-S24N8YZ，S5755-S24P8J8YZ，S5755- S24P8Y，S5755-S24T8J8YZ，S5755-S24T8Y， S5755-S24U8J8YZ，S5755-S24U8Y，S5755- S24UN8YZ，S5755-S48N8YZ，S5755-S48P8Y， S5755-S48P8YZ，S5755-S48T8Y，S5755- S48T8YZ，S5755-S48T8YZ-B，S5755-S48U8Y， S5755-S48U8YZ，S5755-S48UN8YZ |
| S5735R-L-V2 | S5735R-L16LP2S-QA-V2，S5735R-L16LP2UM2X- QA-V2，S5735R-L16LP2X-QA-V2，S5735R- L16T4S-A-V2，S5735R-L16T4X-QA-V2，S5735R- L24P4S-A-V2，S5735R-L24P4X-A-V2，S5735R- L24T4S-A-V2，S5735R-L24T4X-QA-V2，S5735R- L48LP4S-A-V2，S5735R-L48LP4X-A-V2，S5735R- L48P4X-A-V2，S5735R-L48T4S-A-V2，S5735R- L48T4X-A-V2，S5735R-L8P4S-A-V2，S5735R- L8P4X-QA-V2，S5735R-L8T4S-A-V2，S5735R- L8T4X-QA-V2 |
| S5735-L-V2 | S5735-L10T4X-A-V2，S5735-L14P2S-QA-V2， S5735-L16LP2UM2X-QA-V2，S5735-L16LP2X-QA- V2，S5735-L16P2UM2X-QA-V2，S5735-L16T4S- A-V2，S5735-L16T4X-QA-V2，S5735-L24HJ4XE- A-V2，S5735-L24J4X-A-V2，S5735-L24J4X-D- V2，S5735-L24LU8S4XE-QA-V2，S5735-L24P4S- A-V2，S5735-L24P4XE-A-V2，S5735-L24PN4XE- A-V2，S5735-L24ST4XE-A-V2，S5735-L24T4S-A- V2，S5735-L24T4X-QA-V2，S5735-L24T4XE-A- V2，S5735-L24T4XE-D-V2，S5735-L24T8J4XE-A- V2，S5735-L48J4X-A-V2，S5735-L48J4X-D-V2， S5735-L48LP4S-A-V2，S5735-L48LP4XE-A-V2， S5735-L48LPN4XE-A-V2，S5735-L48P4XE-A-V2， S5735-L48PN4XE-A-V2，S5735-L48S4X-A-V2， S5735-L48S4XE-A-V2，S5735-L48T4S-A-V2， S5735-L48T4XE-A-V2，S5735-L48T4XE-D-V2， S5735-L8P2T4X-A-V2，S5735-L8P4S-A-V2， S5735-L8P4X-QA-V2，S5735-L8T4S-A-V2， S5735-L8T4X-QA-V2 |
| S6730-S-V2 | S6730-S24X6Q-V2，S6730-S48X6Q-V2 |

| 系列 | 支持产品 |
|---|---|
| S5735I-S-V2 | S5735I-S16T2S4XN-V2，S5735I-S16T8S4XE-QD- V2，S5735I-S24T4XE-V2，S5735I-S24T8S4XE-QA- V2，S5735I-S24U4XE-V2，S5735I-S48T4XE-V2， S5735I-S8T4SN-V2，S5735I-S8T4XN-V2，S5735I- S8T8P2S4XN-V2，S5735I-S8U2XN-V2，S5735I- S8U4XN-V2 |
| S5732-H-V2 | S5732-H24S4X6QZ-TV2，S5732-H24S4X6QZ- V2，S5732-H24UM4Y2CZ-KV2，S5732- H24UM4Y2CZ-V2，S5732-H44S4X6QZ-V2， S5732-H48UM4Y2CZ-KV2，S5732-H48UM4Y2CZ- TV2，S5732-H48UM4Y2CZ-V2 |

查询工具如需了解硬件规格、产品部件的配套关系，请点击硬件中心进行查询；如需了解关键规格、全量软件规格，请点击规格查询进行查询。
注意事项VBST的规格如表8-3所示。
表 8-3 VBST 的规格

| 项目 | 规格 |
|---|---|
| 保护VLAN数 | 对于S5735-L-V2、S5735-S-V2、 S5735R-S-V2、S5735E-L-V2、S5735E- S-V2、S5735I-L-V2、S5735I-S-V2、 S5755-S、S5735I-H-V2、S5735R-L- V2、S5735S-S3、S5735S-L3、S1730S- S3：240 对于S6780-H、S6750-S、S6730-H- V2、S6750-H、S5732-H-V2、S6750E- S、S6730E-H-V2、S6730-S-V2、和 S5755-H系列：1000 |
| PV数（PV数指所有使能VBST的接口加入的VLAN数的总和，其中VLAN已创建并且也已使能VLAN的VBST功能。） | 对于S5735-L-V2、S5735-S-V2、 S5735R-S-V2、S5735E-L-V2、S5735E- S-V2、S5735I-L-V2、S5735I-S-V2、 S5735I-H-V2、S5735R-L-V2、S5735S- S3、S5735S-L3、S1730S-S3：600 对于S6780-H、S6750-S、S6730-H- V2、S6750-H、S5732-H-V2、S6750E- S、S6730E-H-V2、S6730-S-V2、和 S5755-H系列：24000 对于S5755-S：1200 |

特性限制表 8-4 本特性的使用限制

| 特性 | 特性限制 |
|---|---|
| VBST功能 | 对于S6750-H系列，S6730E-H-V2系列，S6750E-S系列，S6730-S-V2 系列，S5755-H系列，S6780-H系列，S5732-H-V2系列，S6730-H-V2 系列，S5755-S系列，S6750-S系列： VXLAN隧道的用户侧不支持与VBST网络一起共同组网。 |
| VBST功能 | 如果VLAN所在端口配置了VLAN Mapping、VLAN Stacking，此VLAN 的VBST不能正常协商。 |
| VBST功能 | 环路保护功能和根保护功能不能同时配置在同一端口。 |
| VBST功能 | Root保护是指定端口上的特性。当端口的角色是指定端口时，配置的 Root保护功能才生效。若在其他类型的端口上配置Root保护功能， Root保护功能不会生效。 |
| VBST功能 | 由于Alternate端口是根端口的备份端口，如果设备上有Alternate端口，需要在根端口和Alternate端口上同时配置环路保护。 |
| VBST功能 | VBST只支持进程0，如果设备上存在其他进程，模式无法切换到VBST。如果设备上已配置1:N（N>1）的实例和VLAN的映射关系，必须先删除该映射关系后才能修改STP工作模式为VBST模式。 |
| VBST功能 | 为防止临时环路，在VBST模式下实例4094被保留使用，不能使用 instance instance-id vlan vlan-id静态配置实例4094和VLAN的映射关系。切换VBST模式前需要将实例4094的配置清除或者使用其他可用实例替代实例4094。 |

| 特性 | 特性限制 |
|---|---|
| VBST功能 | 1、在VBST组网中，如果本端设备接口的链路类型配置为Access/ QinQ，则对端设备接口的链路类型也需要配置为Access/QinQ。 2、如两端设备接口的链路类型都不是Access/QinQ，则要求两端接口的 PVID配置一致。否则双方设备将无法成功协商VBST协议状态，无法起到破环效果。 3、由于Hybrid接口可以untagged方式放通多个VLAN，且存在与PVID 不一致的情况，可能导致无法成功协商VBST，因此不建议VBST使用 Hybrid接口。 4、现网中存在VBST设备与STP/RSTP设备混合组网的场景。由于VBST 报文与STP/RSTP报文的格式不同，所以存在如何互通的问题。为了实现与STP/RSTP互通： •对于Access端口，VBST设备将只根据此端口所在的VLAN使用STP报文（对接STP设备）或RSTP报文（对接RSTP设备）与对端交互。这样，拓扑计算将按照STP/RSTP协议进行，STP/RSTP协议不区分VLAN，所以最终形成一棵各VLAN共享的生成树。 •对于Trunk/Hybrid端口 1）VBST设备和RSTP设备对接时，在VLAN 1内，VBST设备使用RSTP报文与对端交互，其他VLAN内使用填充RSTP Data的VBST报文与对端交互。 2）VBST设备和STP设备对接时，在VLAN 1内，VBST设备使用STP报文与对端交互，其他VLAN内使用填充STP Data的VBST报文与对端交互。 |
| VBST功能 | VBST与GVRP互斥 |

### 8.4 VBST缺省配置

VBST的主要缺省配置如表8-5所示。
表 8-5 VBST 缺省配置

| 参数 | 缺省值 |
|---|---|
| 生成树协议工作模式 | MSTP模式 |
| STP功能 | 全局使能、各VLAN使能 |
| 设备优先级 | 32768 |
| 端口优先级 | 128 |
| 路径开销计算方法 | Dot1t，即IEEE 802.1t标准 |
| Forward Delay Time | 1500厘秒（15秒） |
| Hello Time | 200厘秒（2秒） |
| Max Age Time | 2000厘秒（20秒） |

### 8.5 配置VBST基本功能

#### 8.5.1 （可选）调整影响设备角色、端口角色和端口状态的参数

背景信息设备优先级、端口优先级、端口路径开销与BPDU报文中的消息优先级向量密切相关，通过调整这几个参数可以影响生成树计算结果，即可以影响生成树中设备的角色、端口的角色和端口状态。
根桥是生成树的逻辑中心。生成树协议可以通过计算来自动确定根桥，用户也可以手动指定根桥或备份根桥，或者通过配置设备优先级来影响根桥的选举结果。建议手动配置根桥和备份根桥。
● 在运行生成树协议的网络中，请将性能高、网络层次高的设备配置为根桥，以保证二层网络的稳定性，否则新接入设备可能会触发根桥切换，从而导致业务短暂中断。
● 在一棵生成树中，生效的根桥只有一个；当两台或两台以上的设备被指定为同一棵生成树的根桥时，系统将选择MAC地址最小的设备作为根桥。
● 可以在每棵生成树中指定多个备份根桥。当根桥出现故障或被关机时，备份根桥可以取代根桥成为指定生成树的根桥；但此时若配置了新的根桥，则备份根桥将不会成为根桥。如果配置了多个备份根桥，则MAC地址最小的备份根桥将成为指定生成树的根桥。
● 设备在各生成树中的角色互相独立。MSTP网络中设备在作为一棵生成树的根桥或备份根桥的同时，也可以作为其他生成树的根桥或备份根桥；但在同一棵生成树中，一台设备不能既作为根桥，又作为备份根桥。
端口路径开销是生成树计算的重要依据，会影响根端口的选择。非根桥设备上所有端口中到达根桥路径开销最小的端口就是根端口。VBST网络中在不同VLAN中为同一端口配置不同的路径开销值，可以使不同VLAN的流量沿不同的物理链路转发，实现VLAN的负载分担功能。
端口路径开销值取值范围由路径开销计算方法决定。如果链路的速率值越大，则建议将该端口的路径开销值在指定范围内设置越小；如果链路的速率值越小，则建议将该端口的路径开销值配置相对较大，以使其在生成树算法中被选举成为阻塞端口，阻塞其所在链路。
端口优先级会影响端口是否被选举为指定端口。如果希望将某端口阻塞从而破除环路，则可将其端口优先级设置比缺省值大，使其在选举过程中成为被阻塞的端口。
除了设备优先级、端口优先级、端口路径开销这几个参数，其他的一些参数也会影响生成树协议的拓扑收敛，如需调整可以参见8.7 配置影响VBST拓扑收敛的参数。

说明如果已经执行命令配置设备在指定VLAN内为根桥设备或备份根桥设备，若需要改变VLAN内
●设备的优先级，则需要先执行命令undo stp vlan root去使能根桥设备或者备份根桥设备功能，然后再执行命令stp vlan priority配置新的优先级数值。
● 根设备的Hello Time、Forward Delay以及Max Age三个时间参数取值之间应该满足如下公式，否则网络会频繁振荡。
● 2 × (Forward Delay －1.0 second) >= Max Age
● Max Age >= 2 × (Hello Time + 1.0 second)
操作步骤步骤1 进入系统视图。
system-view步骤2 配置设备在指定VLAN内的优先级，从而调整设备在生成树协议中的角色。根据需要选择如下任一配置。
● 配置设备在指定VLAN内为根桥。
stp vlan vlan-id1 [ to vlan-id2 ] [ vlan-id3 [ to vlan-id4 ] ] &<1-9> root primary缺省情况下，设备不作为任何生成树的根桥。配置后指定VLAN内设备优先级数值自动为0，并且不能更改设备优先级。
● 配置设备在指定VLAN内为备份根桥。
stp vlan vlan-id1 [ to vlan-id2 ] [ vlan-id3 [ to vlan-id4 ] ] &<1-9> root secondary缺省情况下，设备不作为任何生成树的备份根桥。配置后指定VLAN内设备优先级数值为4096，并且不能更改设备优先级。
配置设备在指定VLAN内的优先级。数值越小，设备的优先级越高，成为根桥的可
●能性越大；数值越大，设备的优先级越低，成为根桥的可能性越小。
stp vlan vlan-id1 [ to vlan-id2 ] [ vlan-id3 [ to vlan-id4 ] ] &<1-9> priority priority-value缺省情况下，设备在生成树中的优先级取值是32768。
如果已经执行命令配置设备在指定VLAN内为根桥设备或备份根桥设备，若需要改变VLAN内设备的优先级，则需要先执行命令undo stp vlan root去使能根桥设备或者备份根桥设备功能，然后再执行命令stp vlan priority配置新的优先级数值。
步骤3 （可选）配置接口路径开销计算方法。
stp pathcost-standard { dot1d-1998 | dot1t | legacy }缺省情况下，路径开销值的计算方法为IEEE 802.1t（dot1t）标准方法。
同一网络内所有设备的接口路径开销应使用相同的计算方法。
步骤4 进入接口视图。
interface interface-type interface-number步骤5 配置接口从三层模式切换到二层模式。
portswitch仅S6780-H系列、S6750-H系列、S6730-H-V2系列、S6730E-H-V2系列、S6750-S系列、S6730-S-V2系列、S6750E-S系列、S5732-H-V2系列、S5755-H系列、S5755-S系列支持该步骤。请用户根据实际接口类型自行选择是否要执行此步骤。
步骤6 配置指定VLAN内当前接口的路径开销值。
stp vlan vlan-id1 [ to vlan-id2 ] [ vlan-id3 [ to vlan-id4 ] ] &<1-9> cost cost
● 配置接口路径开销计算方法为legacy时，参数cost取值范围是1～200000。

● 配置接口路径开销计算方法为dot1d-1998时，参数cost取值范围是1～65535。
● 配置接口路径开销计算方法为dot1t时，参数cost取值范围是1～200000000。
步骤7 配置指定VLAN内接口优先级。
stp vlan vlan-id1 [ to vlan-id2 ] [ vlan-id3 [ to vlan-id4 ] ] &<1-9> port priority priority-value
缺省情况下，设备上接口的优先级取值是128。
----结束

#### 8.5.2 （可选）手工配置实例和VLAN的映射关系

背景信息VBST借助MSTP现有的实例和VLAN映射关系模型，在实例和VLAN间建立1:1映射关系。这种实例和VLAN的1:1映射关系只用于设备基于实例决定转发状态。
VBST中实例和VLAN间的映射关系，可以手工配置，也可由系统动态指定。如果为VLAN手工配置了映射关系，则以手工配置的为准。
● 手工配置是指在设备上手工指定实例和VLAN间的映射关系。手工配置后，VLAN删除或全局VBST去使能，映射关系不会自动取消。
● 动态指定是指VBST启用后，系统按照递增序为设备上已存在或新创建的VLAN自动分配动态实例ID。动态指定的VLAN和实例的映射关系，无法手工改变，只有在VLAN删除或全局VBST去使能后，映射关系才会自动取消。当动态指定的实例数超过保护VLAN数以后，再新建VLAN，系统会在配置文件中显示该VLAN去使能STP。
手工配置实例和VLAN的映射关系时，需要注意：
● 为防止临时环路，在VBST模式下实例4094被保留使用，不能手工配置实例4094和VLAN的映射关系。切换VBST模式前需要将实例4094的配置清除或者使用其他可用实例替代实例4094。
● VBST中实例和VLAN是1:1映射关系。建议先执行命令display stp vlan instance查看VLAN与生成树实例的映射关系，再进行配置，避免多个VLAN映射一个实例的现象。
● 当指定的VBST实例超过设备支持的VBST实例个数（设备支持的VBST实例个数=手工配置实例个数+动态指定实例个数）时，再新建的VLAN默认VBST功能未生效，并且会产生告警。如需启用该VLAN的VBST功能，可以执行undo vlan把其他VLAN 的资源释放。当支持 VBST 的 VLAN 个数低于上限值的 95% ，告警恢复并且系统会自动重新分配资源。
如下配置属于手工配置实例和VLAN的映射关系。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入MST域视图。
stp region-configuration步骤3 配置实例和VLAN的1:1映射关系。
instance instance-id vlan vlan-id

#### 8.5.3 启用VBST

缺省情况下，所有VLAN均映射到CIST，即实例0。
----结束启用
8.5.3 VBST背景信息在环形网络中一旦启用VBST，设备便立即开始进行生成树计算。设备的优先级、端口优先级等参数会影响到生成树的计算，在计算过程中这些参数的变动可能会导致网络振荡。为了保证生成树计算过程快速而且稳定，必须在配置好设备的优先级、端口优先级等参数后再启用VBST。
PV数指所有使能VBST的接口加入的VLAN数的总和，其中VLAN已创建并且也已使能VLAN的VBST功能。例如设备上有10个接口使能了VBST功能，每个接口都加入了100个VLAN（所有VLAN已创建，并且已使能VLAN的VBST功能），则设备上所有接口占用的PV数就为1000。占用的PV数超过规格可能引起CPU占用率高，从而导致设备处理各项任务不及时，进而影响协议计算，甚至引起设备脱管等。
● VBST 特性的 CPU 占用率与占用的 PV 数成正比。大规格 PV 场景，如果不调整参数，会引起CPU占用率过高。
● 可以在任意视图下执行命令display vbst port-vlan statistics，查看VBST的PV数规格。
说明
● 在运行生成树协议的网络中，请将最核心的设备配置为根桥，以保证二层网络的稳定性，否则新接入的设备可能会触发生成树协议根切换，从而导致业务短暂中断。
● 在环形网络中一旦启用生成树协议，生成树协议便立即开始进行生成树计算，设备的优先级、端口优先级等参数都会影响到生成树的计算，在计算过程中这些参数的变动可能会导致网络振荡。为了保证生成树计算过程快速而且稳定，必须在交换设备及其端口进行必要的基本配置以后才能启用生成树协议。
● VBST生成树协议是在每个VLAN内构建一棵生成树，使不同VLAN内的流量可通过不同的生成树转发，不能解决由于网络规模增大带来的性能降低问题。
● 当VBST网络中PV数满规格时（通过display vbst port-vlan statistics命令可以查看设备支持的PV数规格以及设备已使用的PV数）：
● 请优先调整配置，降低设备使用的PV数。例如查看参与VBST计算的接口加入的VLAN是否冗余，将接口退出冗余VLAN；在不需要参与VBST计算的接口下执行命令stp disable；对于不需要参与VBST计算的VLAN，在系统视图下执行命令stp vlan disable，去使能VLAN的VBST功能。
● 当设备使用的PV数无法调整时，执行命令stp vlan timer hello，调整Hello Time大于或等于4秒，并同步调整Forward Delay和Max Age。
● 如果需要使用到较大的PV数，建议将Hello time时间调长，并同步调整Forward delay和Max-age时间。PV数为8000时，Hello time建议调整为4秒；PV数为16000时，Hello time建议调整为8秒；PV数为24000时，Hello time建议调整为10秒。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置生成树协议工作模式为VBST模式。
stp mode vbst

说明VBST模式与STP、RSTP、MSTP模式互斥。
如果设备上已配置1:N（N>1）的实例和VLAN的映射关系，必须先删除该映射关系后才能修改生成树协议工作模式为VBST模式。
如果设备上已经通过命令protected-instance(sep-segment view)配置了SEP段的保护实例或通过命令protected-instance（ERPS环视图）配置了ERPS环的保护实例，则必须8.5.2 （可选）手工配置实例和VLAN的映射关系，否则不能修改STP工作模式为VBST模式。
如果设备上已配置stp vpls-subinterface enable，必须先在相应接口上执行命令undo stp vpls-subinterface enable后才能修改STP工作模式为VBST模式。
步骤3 使能VBST功能。
stp enable步骤4 使能VLAN的VBST功能。
undo stp vlan vlan-id1 [ to vlan-id2 ] [ vlan-id3 [ to vlan-id4 ] ] &<1-9> disable缺省情况下，设备所有VLAN上生成树协议处于使能状态。
步骤5 进入接口视图。
interface interface-type interface-number步骤6 配置接口从三层模式切换到二层模式。
portswitch仅S6780-H系列、S6750-H系列、S6730-H-V2系列、S6730E-H-V2系列、S6750-S系列、S6730-S-V2系列、S6750E-S系列、S5732-H-V2系列、S5755-H系列、S5755-S系列支持该步骤。请用户根据实际接口类型自行选择是否要执行此步骤。
步骤7 使能VBST功能。
stp enable缺省情况下，设备接口上的生成树协议功能处于使能状态。
步骤8 返回系统视图。
quit步骤9 （可选）配置VBST检测设备间直连接口PVID不一致时的保护模式。
stp pvid-consistency protection mode block缺省情况下，未配置VBST检测设备间直连接口PVID不一致时的保护模式，如果设备间直连接口的PVID不一致，VBST协议不会在PVID内将该接口阻塞。配置直连接口PVID不一致时的保护模式为block后，如果设备间直连接口的PVID不一致，VBST协议会在PVID 内将该接口阻塞。
如果链路两端的接口为Trunk类型且有修改PVID，建议在链路两端配置PVID不一致时的保护模式。避免配置不合理导致流量转发异常。
----结束

#### 8.5.4 检查配置结果

操作步骤
● 执行命令display stp vlan instance，查看VLAN与生成树实例的映射关系。
● 执行命令display stp vlan [ vlan-id ] information [ brief | global ]，查看生成树的状态信息、统计信息以及全局概要信息。

● 执行命令display stp vlan [ vlan-id ] bridge { local | root }，查看本桥或根桥的
生成树状态详细信息。
● 执行命令display stp vlan [ vlan-id ] abnormal-interface，查看运行生成树协
议的异常端口信息。
● 执行命令display stp vlan [ vlan-id ] history，查看端口历史角色变化信息和触
发端口角色变化的优先级信息。
● 执行命令display stp brief，查看生成树的简要信息。
● 执行命令display stp vlan vlan-id v-vbst，查看指定VLAN生成树的虚拟VBST计
算结果。
仅S6780-H，S6730E-H-V2，S6730-S-V2，S6730-H-V2，S5755-H，S5732-H-
V2，S6750E-S，S6750-S，S6750-H，S5755-S支持该命令。
● 执行命令display vbst local v-vbst phy-state m-lag mlag-id，查询对端M-LAG
成员口的接口的UP/DOWN状态。
仅S6780-H，S6730E-H-V2，S6730-S-V2，S6730-H-V2，S5755-H，S5732-H-
V2，S6750E-S，S6750-S，S6750-H，S5755-S支持该命令。
● 执行命令 display vbst local v-vbst port-state vlan vlan-id m-lag mlag-id ，查
询对端M-LAG成员口的转发状态。
仅S6780-H，S6730E-H-V2，S6730-S-V2，S6730-H-V2，S5755-H，S5732-H-
V2，S6750E-S，S6750-S，S6750-H，S5755-S支持该命令。
----结束

### 8.6 启用边缘端口和配置BPDU报文过滤功能

背景信息在VBST里面，如果某一个指定端口位于整个网络的边缘，即不再与其他设备连接，而是直接与终端设备直连，这种端口叫做边缘端口。
边缘端口不接收处理配置BPDU报文，不参与VBST运算，可以由Disable直接转到Forwarding状态，且不经历时延，就像在端口上将VBST禁用。
配置为边缘端口后，端口仍然会发送BPDU报文，这可能导致BPDU报文发送到其他网络，引起其他网络产生振荡。因此可以配置边缘端口的BPDU报文过滤功能，使边缘端口不处理、不发送BPDU报文。

说明在全局下配置边缘端口和BPDU报文过滤功能后，设备上所有的端口不会主动发送BPDU报文，且均不会主动与对端设备直连端口协商，所有端口均处于转发状态。这将可能导致网络成环，引起广播风暴，请用户慎用。
在接口下配置边缘端口和BPDU报文过滤功能后，接口将不处理、不发送BPDU报文。该接口将无法成功与对端设备直连端口协商生成树协议状态，请慎用。
接口使能生成树协议后，会默认启用边缘端口自动探测功能，当端口在（2 × Hello Timer + 1）
秒的时间内收不到BPDU报文，自动将端口设置为边缘端口，否则设置为非边缘端口。VBST时每个VLAN都有一个Hello Timer的值，当同一个端口加入多个VLAN时，则端口在（2 x min { Hello Timer } + 1）时间内收不到BPDU报文，自动将端口设置成边缘端口。例如端口同时加入VLAN 2（Hello Timer=2秒）、VLAN 3（Hello Timer=3秒）、VLAN 4（Hello Timer=4秒），则该端口如果在（2 x 2 + 1）=5秒内收不到BPDU报文，自动将端口设置成边缘端口。如果在接口视图下配置了stp edged-port enable或stp edged-port disable或者在系统视图下配置了stp edged-port default，边缘端口自动探测功能就不生效了。
配置边缘端口需要注意：
● 全局配置边缘端口和BPDU报文过滤功能后，设备上所有的端口不会主动发送BPDU报文，且均不会主动与对端设备直连端口协商，所有端口均处于转发状态。这将可能导致网络成环，引起广播风暴，请用户慎用。
● 在接口上配置边缘端口和BPDU报文过滤功能后，端口将不处理、不发送BPDU报文。该端口将无法成功与对端设备直连端口协商 VBST 协议状态，请用户手动在与终端设备直连的接口上配置边缘和BPDU报文过滤功能。
由于终端设备无法参与生成树协议计算，无法回应BPDU报文，因此设备上与终端相连的接口有如下两种处理方式：
● 配置端口为边缘端口，并配置BPDU报文过滤功能。
● 接口下去使能生成树协议，使端口一直保持在转发状态。
从可用性和安全性考虑，建议把端口指定为边缘端口。当连接的终端设备出现环路时，边缘端口可以自动切换为非边缘端口，自动启动该接口生成树协议破环功能。为了防止攻击者通过终端设备伪造BPDU报文恶意攻击设备，还可以配置BPDU保护功能。
操作步骤
● 在全局下配置：
a. 进入系统视图。
system-view
b. 配置设备上所有端口为边缘端口。
stp edged-port default缺省情况下，设备的所有端口为非边缘端口。
c. 配置设备上所有端口为BPDU filter端口。
stp bpdu-filter default缺省情况下，设备的所有端口为非BPDU filter端口。
● 在接口下配置：
a. 进入系统视图。
system-view
b. 进入接口视图。
interface interface-type interface-number
c. 配置接口从三层模式切换到二层模式。
portswitch

仅S6780-H系列、S6750-H系列、S6730-H-V2系列、S6730E-H-V2系列、S6750-S系列、S6730-S-V2系列、S6750E-S系列、S5732-H-V2系列、S5755-H系列、S5755-S系列支持该步骤。请用户根据实际接口类型自行选择是否要执行此步骤。
d. 配置端口为边缘端口。
stp edged-port enable缺省情况下，设备的所有端口为非边缘端口。
e. 配置端口为BPDU filter端口。
stp bpdu-filter enable缺省情况下，设备的所有端口为非BPDU filter端口。
----结束检查配置结果
● 执行命令display stp vlan [ vlan-id ] information，根据Edged Port Default查看全局边缘端口的配置情况、根据Bpdu-filter Default查看全局BPDU filter端口的配置情况、根据Port Edged字段查看接口下边缘端口的配置情况。
● 在接口视图下执行命令display this，查看接口下BPDU filter端口的配置情况。

### 8.7 配置影响VBST拓扑收敛的参数

#### 8.7.1 配置VBST网络直径

背景信息网络中任意两台终端设备都通过特定路径彼此相连，这些路径由一系列的设备构成。
网络直径就是指网络中任意两台终端设备间的最大设备数。网络直径越大，说明网络的规模越大。例如图8-4所示网络的网络直径为5。
● DeviceC-DeviceA-DeviceD-DeviceB-DeviceE
● DeviceD-DeviceA-DeviceC-DeviceB-DeviceE图 8-4 生成树协议网络直径若网络直径设置不合理，可能会引起网络收敛速度慢，影响用户的正常通信。根据当前的网络规模设置合适的网络直径，可以帮助加快网络收敛速度。
建议同一环网中的所有设备配置相同的网络直径。

操作步骤步骤1 进入系统视图。
system-view步骤2 配置网络直径。
stp vlan vlan-id1 [ to vlan-id2 ] [ vlan-id3 [ to vlan-id4 ] ] &<1-9> bridge-diameter dbridge-diameter缺省情况下，生成树的网络直径是7。
说明配置网络直径后，设备会根据网络直径计算出Forward Delay、Hello Time以及Max Age定时器的最优值。建议通过配置网络直径的方式去调整Forward Delay、Hello Time以及Max Age定时器的值。
----结束

#### 8.7.2 配置VBST定时器

背景信息在生成树的计算过程中，用到了以下三个时间参数：
● Forward Delay：用于确定状态迁移的延迟时间。在运行生成树算法的网络中，当网络拓扑结构发生变化时，因为新的BPDU配置消息需要经过一定的时间才能传遍整个网络，所以本应被阻塞的端口可能还来不及被阻塞而之前被阻塞的端口已经不再阻塞，这样就有可能会形成临时的环路。为了避免这种情况引起的临时环路，可以通过Forward Delay定时器设置延时时间，即在这个延时时间内所有端口会临时被阻塞。
● Hello Time：用于检测链路是否存在故障。生成树协议每隔Hello Time时间会发送配置BPDU报文，以确认链路是否存在故障。如果设备根端口在超时时间（超时时间＝Hello Time × 3 × Timer Factor）内没有收到BPDU，则会由于消息超时而重新计算生成树。
Age：用于确定配置BPDU报文是否超时。设备根据Max Age时间来确定端口
● Max收到的配置BPDU报文是否超时。如果端口收到的配置BPDU报文超时，则需要重新计算。
在配置上述三个时间参数时，同一环网中的设备配置时间建议保持一致。
通常情况下，不建议通过本配置直接调整上述三个时间参数。由于这三个时间参数的取值与网络规模有关，因此建议通过调整网络直径，使生成树协议自动调整这三个时间参数的值。当网络直径取缺省值时，这三个时间参数也分别取其各自的缺省值。
须知根设备的Hello Time、Forward Delay以及Max Age三个时间参数取值之间应该满足如下公式，否则网络会频繁振荡。
● 2 × (Forward Delay －1.0 second) >= Max Age
● Max Age >= 2 × (Hello Time + 1.0 second)

操作步骤步骤1 进入系统视图。
system-view步骤2 配置Forward Delay时间。
stp vlan vlan-id1 [ to vlan-id2 ] [ vlan-id3 [ to vlan-id4 ] ] &<1-9> timer forward-delay time-value缺省情况下，设备的Forward Delay时间是1500厘秒（15秒）。
步骤3 配置Hello Time时间。
stp vlan vlan-id1 [ to vlan-id2 ] [ vlan-id3 [ to vlan-id4 ] ] &<1-9> timer hello time-value缺省情况下，设备的Hello Time时间是200厘秒（2秒）。
步骤4 配置Max Age时间。
stp vlan vlan-id1 [ to vlan-id2 ] [ vlan-id3 [ to vlan-id4 ] ] &<1-9> timer max-age time-value缺省情况下，设备的Max Age时间是2000厘秒（20秒）。
----结束检查配置结果执行命令display stp vlan [ vlan-id ] information [ global ]，根据Config Times字段查看各定时器的配置情况。

#### 8.7.3 配置VBST超时时间

背景信息在运行生成树算法的网络中，如果设备在配置的超时时间（超时时间＝Hello Time × 3× Timer Factor）内没有收到上游设备发送的BPDU，就认为上游设备已经出现故障，本设备会重新进行生成树计算。
由于上游设备繁忙，有时设备在较长的时间内收不到上游设备发送的BPDU。在这种情况下一般不应该重新进行生成树计算，因此，在稳定的网络中，可以配置超时时间，以减少网络资源的浪费。
操作步骤步骤 1 进入系统视图。
system-view步骤2 配置未收到上游的BPDU重新开始生成树计算的超时时间。
stp timer-factor factor缺省情况下，设备未收到上游的BPDU就重新开始生成树计算的超时时间是Hello Timer的9倍。
----结束检查配置结果执行命令display stp vlan [ vlan-id ] information [ global ]，根据Timer-factor字段查看超时时间的配置情况。

#### 8.7.4 配置TC报文刷新MAC表功能

背景信息部署生成树协议后，任何对拓扑有影响的变化，例如本设备的端口由Down变为Up状态，生成树协议都会发送TC类型BPDU报文通知刷新MAC表项。而有时这种变化导致大量的刷新可能会引入未知的单播或广播问题。为解决此问题，可去使能设备收到TC类型BPDU报文后刷新MAC表功能。
当去使能设备收到TC类型BPDU报文后刷新MAC表功能时，如果MAC表项错误就会造成长时间断流，所以该功能的影响很大，请谨慎部署该命令。
操作步骤步骤1 进入系统视图。
system-view步骤2 去使能TC类型BPDU报文刷新MAC表功能。
stp flush disable缺省情况下，设备收到TC类型BPDU报文后会刷新MAC表。
----结束检查配置结果在系统视图下执行命令display this，查看TC类型BPDU报文刷新MAC表功能的配置情况。

#### 8.7.5 配置端口的链路类型

背景信息点对点链路可帮助实现快速收敛。与点对点链路相连的两个端口如果为根端口或者指定端口，则端口可以通过传送同步报文（Proposal报文和Agreement报文）快速迁移到转发状态，减少了不必要的转发延迟时间。
操作步骤步骤 1 进入系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤3 配置接口从三层模式切换到二层模式。
portswitch仅S6780-H系列、S6750-H系列、S6730-H-V2系列、S6730E-H-V2系列、S6750-S系列、S6730-S-V2系列、S6750E-S系列、S5732-H-V2系列、S5755-H系列、S5755-S系列支持该步骤。请用户根据实际接口类型自行选择是否要执行此步骤。
步骤4 配置接口的链路类型。
stp point-to-point { auto | force-false | force-true }

缺省情况下，端口的链路类型为auto，即由生成树协议自动检测与端口相连的链路是否是点到点链路。
● 如果当前以太网接口工作在全双工模式，则当前接口相连的链路是点到点链路，执行命令stp point-to-point force-true实现快速收敛。
● 如果当前以太网接口工作在半双工模式，可通过执行命令stp point-to-point force-true，强制链路类型为点对点链路，实现快速收敛。
----结束检查配置结果执行命令display stp vlan [ vlan-id ] information，根据Point-to-point字段查看接口链路类型的配置情况。

#### 8.7.6 配置BPDU报文最大发送速率

背景信息端口在每个 Hello Time 时间内 BPDU 的最大发送数目值越大，表示单位时间内发送的BPDU越多，则占用的系统资源也越多。适当的配置该值可以限制端口发送BPDU的速度，防止在网络拓扑动荡时，生成树协议占用过多的带宽资源。
如果设备的所有端口都需要配置每秒发送BPDU的最大数目且取值相同，则可以直接在系统视图下执行命令stp transmit-limit进行配置。
接口视图下配置的优先级高于系统视图下配置的优先级，即如果设备上在系统视图和接口视图同时配置了stp transmit-limit，则对于相应的接口，接口视图下配置的stp transmit-limit取值生效。
操作步骤
● 在系统视图下配置每个接口每秒发送BPDU的最大数目。
a. 进入系统视图。
system-view
b. 配置每个接口每秒发送BPDU的最大数目。
stp transmit-limit packet-number缺省情况下，接口每秒发送BPDU的最大数目是6。
● 在接口视图下配置接口每秒发送BPDU的最大数目。
a. 进入系统视图。
system-view
b. 进入接口视图。
interface interface-type interface-number
c. 配置接口从三层模式切换到二层模式。
portswitch仅S6780-H系列、S6750-H系列、S6730-H-V2系列、S6730E-H-V2系列、S6750-S系列、S6730-S-V2系列、S6750E-S系列、S5732-H-V2系列、S5755-H 系列、 S5755-S 系列支持该步骤。请用户根据实际接口类型自行选择是否要执行此步骤。
d. 配置接口每秒发送BPDU的最大数目。
stp transmit-limit packet-number

缺省情况下，接口每秒发送BPDU的最大数目由stp transmit-limit (system view)配置的值决定，但若不配置stp transmit-limit (system view)，则接口每秒发送BPDU的最大数目是6。
----结束检查配置结果执行命令display stp vlan [ vlan-id ] information [ global ]，根据Transit Limit字段查看接口下BPDU报文最大发送速率的配置情况。

### 8.8 配置VBST保护功能

#### 8.8.1 了解VBST保护功能

BPDU 保护如图 8-5 所示， DeviceC 上将与 PC 相连的端口设置为边缘端口。当边缘端口接收到BPDU报文时，DeviceC会自动将边缘端口设置为非边缘端口，并重新进行生成树计算。当攻击者发送的BPDU报文中的桥优先级高于现有网络中根桥优先级时会改变当前网络拓扑，可能会导致业务流量中断。这是网络中一种简单的拒绝服务DoS（Denial of Service）攻击方式。
DeviceC上启动了BPDU保护功能后，如果边缘端口收到BPDU报文，边缘端口将被error-down，但保持边缘端口属性不变。
图 8-5 BPDU 保护TC 保护设备在接收到 TC （ Topology Change ）类型 BPDU 报文后，会执行 MAC 地址表项和 ARP表项的删除操作。如果有人伪造TC类型BPDU报文恶意攻击设备，设备短时间内会收到很多TC类型BPDU报文，频繁的删除操作会给设备造成很大的负担，给网络的稳定带来隐患。

启用TC保护功能后，在单位时间内，设备处理TC类型BPDU报文的次数可配置。如果在单位时间内，设备收到TC类型BPDU报文数量大于配置的阈值，那么设备只会处理阈值指定的次数。对于其他超出阈值的TC类型BPDU报文，定时器到期后设备只对其统一处理一次。这样可以避免频繁的删除MAC地址表项和ARP表项，从而达到保护设备的目的。
根保护由于维护人员的错误配置或网络中的恶意攻击，网络中合法根桥有可能会收到优先级更高的BPDU，使得合法根桥失去根地位，从而引起网络拓扑结构的错误变动。这种拓扑变化可能会导致原来应该通过高速链路的流量被牵引到低速链路上，造成网络拥塞。
如图8-6所示，DeviceA和DeviceB处于网络核心层，两者间链路带宽为100GB/s，DeviceA为网络中的根桥。DeviceC和DeviceA、DeviceC和DeviceB之间的链路带宽为10GB/s。正常情况下，DeviceB和DeviceC之间的链路被阻塞。当DeviceD新接入DeviceC时，假设DeviceD的桥优先级高于DeviceA，此时DeviceD会被选举为新的根桥，如果DeviceA和DeviceB之间的100GB/s链路被阻塞，会导致VLAN中的流量都通过两条10GB/s链路传输，可能会引起网络拥塞及流量丢失。
图 8-6 根保护此时可以在DeviceC连接DeviceD的端口上，配置根保护。对于启用根保护功能的指定端口，其端口角色只能保持为指定端口。一旦启用根保护功能的指定端口收到优先级更高的BPDU时，端口状态将进入Discarding状态，不再转发报文。经过一段时间（通常为两倍的Forward Delay），如果端口一直没有再收到优先级较高的BPDU，端口会自动恢复到正常的Forwarding状态。
当端口的角色是指定端口时，配置的根保护功能才生效。
环路保护在运行生成树协议的网络中，根端口和其他阻塞端口状态是依靠不断接收来自上游设备的BPDU维持。当由于链路拥塞或者单向链路故障导致这些端口收不到来自上游交换

设备的BPDU时，设备会重新选择根端口。原先的根端口会转变为指定端口，而原先的阻塞端口会迁移到转发状态，从而造成网络中产生环路。如图8-7所示，当BP2-CP1之间的链路发生拥塞时，DeviceC由于根端口CP1在超时时间内收不到来自上游设备的BPDU报文，Alternate端口CP2放开转变成了根端口，根端口CP1转变成指定端口，从而形成了环路。
图 8-7 链路发生拥塞情况拓扑的变化启动了环路保护功能后，如果根端口或Alternate端口长时间收不到来自上游设备的BPDU报文时，则向网管发出通知信息（此时根端口会进入Discarding状态，角色切换为指定端口），而Alternate端口则会一直保持在阻塞状态（角色也会切换为指定端口），不转发报文，从而不会在网络中形成环路。直到链路不再拥塞或单向链路故障恢复，端口重新收到BPDU报文进行协商，并恢复到链路拥塞或者单向链路故障前的角色和状态。
环路保护功能只能在根端口或Alternate端口上配置生效。

#### 8.8.2 配置BPDU保护功能

背景信息边缘端口直接和用户终端相连，正常情况下，边缘端口不会收到BPDU报文。如果攻击者伪造BPDU恶意攻击设备，当边缘端口接收到BPDU报文时，设备会自动将边缘端口设置为非边缘端口，并重新进行生成树计算，从而引起网络振荡。通过使能BPDU保护可以防止伪造BPDU恶意攻击。边缘端口的配置请参见8.6 启用边缘端口和配置BPDU报文过滤功能。
说明使能设备的BPDU保护功能只对通过stp edged-port或stp edged-port default手工配置的边缘端口生效，对通过系统的边缘端口自动探测功能设置成的边缘端口不生效。
请在有边缘端口的设备上进行以下配置。

操作步骤步骤1 进入系统视图。
system-view步骤2 配置BPDU保护功能。
stp bpdu-protection缺省情况下，BPDU保护功能处于去使能状态。
说明配置BPDU保护功能后，如果边缘端口收到BPDU报文，边缘端口将会被error-down，边缘端口属性不变。如果希望被error-down的边缘端口恢复Up，可通过如下方式实现：
● 在接口视图下执行命令restart。
● 在接口视图下先执行命令shutdown，再执行命令undo shutdown。
● 在系统视图下执行命令error-down auto-recovery cause bpdu-protection interval interval-value，使能端口自动恢复为Up的功能，并设置端口自动恢复为Up的延时时间。使被关闭的端口经过延时时间interval-value后能够自动恢复。
---- 结束检查配置结果执行命令display stp vlan [ vlan-id ] information [ global ]，根据BPDU- Protection字段查看BPDU保护功能的配置情况。

#### 8.8.3 配置TC保护功能

背景信息如果攻击者伪造拓扑变化BPDU报文恶意攻击设备，设备短时间内会收到很多拓扑变化BPDU报文，频繁的删除MAC或者ARP表项操作会给设备造成很大的负担，也给网络的稳定带来很大隐患。
启用TC保护功能后，在指定时间内，设备处理拓扑变化报文的次数可配置。如果在指定时间内，设备收到拓扑变化报文的数量大于配置的最大数量，那么设备只会处理指定的报文个数。对于其他超出最大数量的拓扑变化报文，指定时间超时后设备只对其统一处理一次。这样可以避免频繁的删除MAC地址表项和ARP表项，从而达到保护设备的目的。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置对TC类型BPDU报文的保护功能。
stp tc-protection缺省情况下，设备对TC类型BPDU报文的保护功能处于关闭状态。
步骤3 配置TC保护功能的参数，请选择执行其中一个或两个：
● 配置设备处理最大数量的拓扑变化报文所需的时间。
stp tc-protection interval interval-value缺省情况下，设备处理最大数量的拓扑变化报文所需的时间是Hello Time。

● 配置设备在设定时间内处理拓扑变化报文的最大数量。
stp tc-protection threshold threshold
缺省情况下，设备在指定时间内处理拓扑变化报文的最大数量是1。
说明
● TC保护功能的参数有两个：处理拓扑变化报文的时间和最大数量，即在设定的某段时间内能
处理的最大数量的BPDU报文，例如，时间设定为10秒，最大数量设定为5，则设备收到拓扑
变化报文后，在10秒内只会处理最开始收到的5个拓扑变化报文，对于后面收到的报文则会
等10秒超时后再统一处理。
● 在stp tc-protection interval指定的时间内，设备只会处理stp tc-protection threshold指
定的数量拓扑变化报文，对于其他的报文会延迟处理，所以可能会影响生成树的收敛速度。
----结束
检查配置结果
执行命令display stp vlan [ vlan-id ] information [ global ]，根据字段Tc-
protection、Tc-protection threshold、Tc-protection interval查看TC保护功能的配置
情况。

#### 8.8.4 配置根保护功能

背景信息由于维护人员的错误配置或网络中的恶意攻击，网络中的合法根桥设备有可能会收到优先级更高的BPDU报文，使得合法根桥设备失去根桥的地位，引起网络拓扑结构的错误变动。这种拓扑变化可能会导致原来应该通过高速链路的流量被牵引到低速链路上，造成网络拥塞。为了防止这种情况发生，可在设备上部署根保护功能，通过维持指定端口的角色来保护根桥设备的地位。
一般在根桥的端口上配置根保护功能。当端口的角色是指定端口时，配置的根保护功能才生效。
根保护功能和环路保护功能互斥，配置了根保护功能的端口不能再配置环路保护。
操作步骤步骤1 进入系统视图。
system-view步骤 2 进入接口视图。
interface interface-type interface-number步骤3 配置接口从三层模式切换到二层模式。
portswitch仅S6780-H系列、S6750-H系列、S6730-H-V2系列、S6730E-H-V2系列、S6750-S系列、S6730-S-V2系列、S6750E-S系列、S5732-H-V2系列、S5755-H系列、S5755-S系列支持该步骤。请用户根据实际接口类型自行选择是否要执行此步骤。
步骤4 配置根保护功能。
stp root-protection缺省情况下，端口的根保护功能处于关闭状态。
----结束

检查配置结果执行命令display stp vlan [ vlan-id ] information [ brief ]，根据Protection Type字段查看接口下根保护功能的配置情况。

#### 8.8.5 配置环路保护功能

背景信息在运行生成树协议的网络中，根端口和其他阻塞端口状态是依靠不断接收来自上游设备的BPDU维持。当由于链路拥塞或者单向链路故障导致这些端口收不到来自上游设备的BPDU时，设备会重新选择根端口。原先的根端口会转变为指定端口，而原先的阻塞端口会迁移到转发状态，从而造成网络中产生环路。为了防止以上情况发生，可部署环路保护功能。
启动了环路保护功能后，如果根端口或Alternate端口长时间收不到来自上游的BPDU报文时，则向网管发出通知信息（如果是根端口则进入Discarding状态）。而阻塞端口则会一直保持在阻塞状态，不转发报文，从而不会在网络中形成环路。直到根端口或Alternate 端口收到 BPDU 报文，端口状态才恢复正常为 Forwarding 状态。
由于Alternate端口是根端口的备份端口，如果设备上有Alternate端口，需要在根端口和Alternate端口上同时配置环路保护。
根保护功能和环路保护功能互斥，配置了环路保护功能的端口不能再配置根保护。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入根端口或Alternate端口的接口视图。
interface interface-type interface-number步骤3 配置接口从三层模式切换到二层模式。
portswitch仅S6780-H系列、S6750-H系列、S6730-H-V2系列、S6730E-H-V2系列、S6750-S系列、S6730-S-V2系列、S6750E-S系列、S5732-H-V2系列、S5755-H系列、S5755-S系列支持该步骤。请用户根据实际接口类型自行选择是否要执行此步骤。
步骤4 配置环路保护功能。
stp loop-protection缺省情况下，环路保护功能处于关闭状态。
----结束检查配置结果执行命令 display stp vlan [ vlan-id ] information [ brief ] ，根据 Protection Type 字段查看接口下环路保护功能的配置情况。

### 8.9 配置设备支持和其他厂商设备互通的参数

背景信息设备部署VBST，与其他厂商设备互通时，支持调整如下参数：
● P/A（Proposal/Agreement）机制设备快速迁移P/A（Proposal/Agreement）机制支持普通方式和增强方式两种。
华为设备与其他厂商设备的P/A机制不同会导致互通失败。可以根据其他厂商设备的P/A机制，选择华为设备端口使用增强的快速迁移机制还是普通的快速迁移机制。
● 丢弃Handreamnet交换机发送的非标准STP/RSTP协议报文如果华为设备与Handreamnet交换机混合组网，Handreamnet交换机发送的非标准STP/RSTP协议报文可能会造成临时环路，因此需要配置接口丢弃Handreamnet交换机发送的非标准STP/RSTP协议报文，以避免临时环路的发生。
● 回切延迟设备使能VBST功能同其他厂商设备PVST协议对接时，对端不支持P/A协商机制，协商不同步，导致网络收敛时间增长。若对端为根桥设备，且除对接端口外设备还有相应的Alternate端口，则可在对接的端口上使能回切延迟功能，延迟时间为2 * Forward Delay + 8s，保证端口状态发生变化时对端端口先完成生成树计算，本端端口再进行生成树状态的切换，使得状态切换过程中业务不中断。端口使能回切延迟功能后，作用于端口加入的所有VLAN，若某个VLAN在设备上对应对接的端口没有相应的Alternate端口，链路故障恢复时，该对接的端口状态恢复也要等待2 * Forward Delay + 8s，请慎用。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤3 配置接口从三层模式切换到二层模式。
portswitch仅 S6780-H 系列、 S6750-H 系列、 S6730-H-V2 系列、 S6730E-H-V2 系列、 S6750-S 系列、S6730-S-V2系列、S6750E-S系列、S5732-H-V2系列、S5755-H系列、S5755-S系列支持该步骤。请用户根据实际接口类型自行选择是否要执行此步骤。
步骤4 配置设备支持和其他厂商设备互通的参数，根据需要选择配置。
● 配置端口使用普通的快速迁移方式。
stp no-agreement-check缺省情况下，端口使用增强的快速迁移机制。
● 配置接口丢弃Handreamnet交换机发送的非标准STP/RSTP协议报文。
stp agreement-legacy缺省情况下，接口不丢弃Handreamnet交换机发送的非标准STP/RSTP协议报文。
● 配置接口的回切延迟功能。
stp revertive slow

缺省情况下，接口的回切延迟功能处于未使能状态。
----结束检查配置结果在接口视图下执行命令display this，查看接口下和其他厂商设备互通的参数。

### 8.10 维护VBST

#### 8.10.1 查看VBST统计信息

背景信息通过查看VBST协议运行信息和VBST报文的统计信息，如果设备拓扑变化的次数递增，则可以确定网络存在振荡。
操作步骤
● 执行命令display stp vlan [ vlan-id ] information [ brief | global ]，查看生成树的状态信息、统计信息以及全局概要信息。
● 执行命令display stp vlan [ vlan-id ] bridge { root | local }，查看本桥和根桥的生成树状态信息。
● 执行命令display stp vlan instance，查看实例与VLAN的映射关系。
● 执行命令display stp vlan [ vlan-id ] bpdu statistics，查看BPDU报文收发计数。
● 执行命令display stp vlan [ vlan-id ] tc-bpdu statistics，查看端口TC/TCN报文收发计数。
● 执行命令display stp vlan [ vlan-id ] topology-change，查看拓扑变化相关的统计信息。
● 执行命令display vbst local { instance [ vlan vlan-id ] | port port-id port-id | port-instance port-id port-id | portlist }，查看VBST内部数据区中的信息。
● 执行命令display stp brief，查看生成树的简要信息。
● 执行命令display vbst port-vlan statistics，查看VBST的PV数统计信息。
● 执行命令 display stp vlan vlan-id v-vbst ，查看指定 VLAN 生成树的虚拟 VBST 计算结果。
仅S6780-H，S6730E-H-V2，S6730-S-V2，S6730-H-V2，S5755-H，S5732-H- V2，S6750E-S，S6750-S，S6750-H，S5755-S支持该命令。
----结束

#### 8.10.2 清除VBST统计信息

背景信息当需要统计一定时间内VBST报文的流量时，需要在统计开始前清除VBST报文的统计信息，使VBST报文重新统计，保证统计信息的正确性。

须知清除VBST的BPDU统计信息后，以前的信息将无法恢复，务必仔细确认。
操作步骤
● 在用户视图下执行命令reset stp vlan { vlan-id | all } tc-bpdu statistics，清除TC/TCN BPDU报文的统计信息。
● 在用户视图下执行命令reset stp vlan { vlan-id | all } bpdu statistics，清除BPDU报文的统计信息。
----结束

#### 8.10.3 配置MCheck恢复接口工作模式

背景信息运行 VBST 的设备，如果某个端口与运行 STP 的设备直连，则该端口会自动将其工作模式迁移到STP模式，然后向外发送配置BPDU报文从而保证设备之间的互通。但是，如果运行STP的设备关机或被移走，该端口无法自动迁移回原来的VBST模式，这样会导致与其他运行VBST的设备无法互通。此时可以通过执行MCheck操作，将端口从STP模式手动迁移回原来的VBST模式。
操作步骤
● 在接口视图下执行MCheck操作，使接口从STP模式迁移回VBST模式。
system-view interface interface-type interface-number portswitch stp vlan vlan-id mcheck仅S6780-H系列、S6750-H系列、S6730-H-V2系列、S6750-S系列、S5732-H-V2系列、S6750E-S、S6730E-H-V2、S5755-H系列、S5755-S系列支持命令portswitch。
● 在系统视图下执行MCheck操作，使设备上接口从STP模式迁移回VBST模式。
system-view stp vlan vlan-id mcheck
----结束

### 8.11 VBST配置举例

#### 8.11.1 举例：配置VBST基本功能

组网需求如图 8-8 所示，设备 DeviceC 和 DeviceD 分别双归接入到 DeviceA 和 DeviceB 。 DeviceC 接入VLAN 10、20的业务流量，DeviceD接入VLAN 20、30的业务流量。由于双归接入，设备间存在环形网络。用户希望部署VBST，使各VLAN内的业务流量正常转发，同时希望不同VLAN内的业务流量能够在链路上负载分担，以提高链路利用率。

图 8-8 配置 VBST 功能组网图说明本例中interface1、interface2、interface3、interface4、interface5分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3、10GE1/0/4、10GE1/0/5。
操作步骤步骤1 在设备DeviceA、DeviceB、DeviceC和DeviceD上创建VLAN10、VLAN20和VLAN30。
\# 在DeviceA上创建VLAN10、VLAN20和VLAN30。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 10 20 30 \# 在DeviceB上创建VLAN10、VLAN20和VLAN30。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan batch 10 20 30 \# 在 DeviceC 上创建 VLAN10 和 VLAN20 。
<HUAWEI> system-view [HUAWEI] sysname DeviceC [DeviceC] vlan batch 10 20

\# 在DeviceD上创建VLAN20和VLAN30。
<HUAWEI> system-view [HUAWEI] sysname DeviceD [DeviceD] vlan batch 20 30步骤2 配置接口加入VLAN。
\# 将DeviceA接口10GE1/0/1加入VLAN10、VLAN20和VLAN30，10GE1/0/2加入VLAN20和VLAN30，10GE1/0/3加入VLAN10和VLAN20。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type trunk [DeviceA-10GE1/0/1] port trunk allow-pass vlan 10 20 30 [DeviceA-10GE1/0/1] undo port trunk allow-pass vlan 1 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type trunk [DeviceA-10GE1/0/2] port trunk allow-pass vlan 20 30 [DeviceA-10GE1/0/2] undo port trunk allow-pass vlan 1 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] portswitch [DeviceA-10GE1/0/3] port link-type trunk [DeviceA-10GE1/0/3] port trunk allow-pass vlan 10 20 [DeviceA-10GE1/0/3] undo port trunk allow-pass vlan 1 [DeviceA-10GE1/0/3] quit \# 将DeviceB接口10GE1/0/1加入VLAN10、VLAN20和VLAN30，10GE1/0/2加入VLAN10和VLAN20，10GE1/0/3加入VLAN20和VLAN30。
[DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] portswitch [DeviceB-10GE1/0/1] port link-type trunk [DeviceB-10GE1/0/1] port trunk allow-pass vlan 10 20 30 [DeviceB-10GE1/0/1] undo port trunk allow-pass vlan 1 [DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] portswitch [DeviceB-10GE1/0/2] port link-type trunk [DeviceB-10GE1/0/2] port trunk allow-pass vlan 10 20 [DeviceB-10GE1/0/2] undo port trunk allow-pass vlan 1 [DeviceB-10GE1/0/2] quit [DeviceB] interface 10ge 1/0/3 [DeviceB-10GE1/0/3] portswitch [DeviceB-10GE1/0/3] port link-type trunk [DeviceB-10GE1/0/3] port trunk allow-pass vlan 20 30 [DeviceB-10GE1/0/3] undo port trunk allow-pass vlan 1 [DeviceB-10GE1/0/3] quit \# 将DeviceC接口10GE1/0/2加入VLAN10和VLAN20，10GE1/0/3加入VLAN10和VLAN20，10GE1/0/4加入VLAN10，10GE1/0/5加入VLAN20。
[DeviceC] interface 10ge 1/0/2 [DeviceC-10GE1/0/2] portswitch [DeviceC-10GE1/0/2] port link-type trunk [DeviceC-10GE1/0/2] port trunk allow-pass vlan 10 20 [DeviceC-10GE1/0/2] undo port trunk allow-pass vlan 1 [DeviceC-10GE1/0/2] quit [DeviceC] interface 10ge 1/0/3 [DeviceC-10GE1/0/3] portswitch [DeviceC-10GE1/0/3] port link-type trunk [DeviceC-10GE1/0/3] port trunk allow-pass vlan 10 20 [DeviceC-10GE1/0/3] undo port trunk allow-pass vlan 1 [DeviceC-10GE1/0/3] quit [DeviceC] interface 10ge 1/0/4 [DeviceC-10GE1/0/4] portswitch

[DeviceC-10GE1/0/4] port link-type access [DeviceC-10GE1/0/4] port default vlan 10 [DeviceC-10GE1/0/4] quit [DeviceC] interface 10ge 1/0/5 [DeviceC-10GE1/0/5] portswitch [DeviceC-10GE1/0/5] port link-type access [DeviceC-10GE1/0/5] port default vlan 20 [DeviceC-10GE1/0/5] quit \# 将DeviceD接口10GE1/0/2加入VLAN20和VLAN30，10GE1/0/3加入VLAN20和VLAN30，10GE1/0/4加入VLAN20，10GE1/0/5加入VLAN30。
[DeviceD] interface 10ge 1/0/2 [DeviceD-10GE1/0/2] portswitch [DeviceD-10GE1/0/2] port link-type trunk [DeviceD-10GE1/0/2] port trunk allow-pass vlan 20 30 [DeviceD-10GE1/0/2] undo port trunk allow-pass vlan 1 [DeviceD-10GE1/0/2] quit [DeviceD] interface 10ge 1/0/3 [DeviceD-10GE1/0/3] portswitch [DeviceD-10GE1/0/3] port link-type trunk [DeviceD-10GE1/0/3] port trunk allow-pass vlan 20 30 [DeviceD-10GE1/0/3] undo port trunk allow-pass vlan 1 [DeviceD-10GE1/0/3] quit [DeviceD] interface 10ge 1/0/4 [DeviceD-10GE1/0/4] portswitch [DeviceD-10GE1/0/4] port link-type access [DeviceD-10GE1/0/4] port default vlan 20 [DeviceD-10GE1/0/4] quit [DeviceD] interface 10ge 1/0/5 [DeviceD-10GE1/0/5] portswitch [DeviceD-10GE1/0/5] port link-type access [DeviceD-10GE1/0/5] port default vlan 30 [DeviceD-10GE1/0/5] quit步骤3 配置设备的生成树协议工作在VBST模式。
\# 配置DeviceA的工作模式为VBST。
[DeviceA] stp mode vbst \# 配置DeviceB的工作模式为VBST。
[DeviceB] stp mode vbst \# 配置DeviceC的工作模式为VBST。
[DeviceC] stp mode vbst \# 配置DeviceD的工作模式为VBST。
[DeviceD] stp mode vbst步骤4 分别配置VLAN10、VLAN20、VLAN30的根桥和备份根桥。
\# 配置DeviceA为VLAN10的根桥。
[DeviceA] stp vlan 10 root primary \# 配置DeviceB为VLAN10的备份根桥。
[DeviceB] stp vlan 10 root secondary \# 配置DeviceA为VLAN20的根桥。
[DeviceA] stp vlan 20 root primary \# 配置DeviceB为VLAN20的备份根桥。
[DeviceB] stp vlan 20 root secondary

\# 配置DeviceB为VLAN30的根桥。
[DeviceB] stp vlan 30 root primary \# 配置DeviceA为VLAN30的备份根桥。
[DeviceA] stp vlan 30 root secondary步骤5 配置各VLAN中端口的路径开销值，实现将该端口阻塞。
说明
● 端口路径开销值取值范围由路径开销计算方法决定，本例选择使用缺省的IEEE 802.1t计算方法，配置将被阻塞端口的路径开销值为2000000。
● 同一网络内所有设备的端口路径开销应使用相同的计算方法。
\# 将DeviceC上的端口10GE1/0/2在VLAN10中的路径开销值配置为2000000，在VLAN20中的路径开销值配置为2000000。
[DeviceC] interface 10ge 1/0/2 [DeviceC-10GE1/0/2] stp vlan 10 cost 2000000 [DeviceC-10GE1/0/2] stp vlan 20 cost 2000000 [DeviceC-10GE1/0/2] quit \# 将DeviceD上的端口10GE1/0/2在VLAN20中的路径开销值配置为2000000，在VLAN30中的路径开销值配置为2000000。
[DeviceD] interface 10ge 1/0/2 [DeviceD-10GE1/0/2] stp vlan 20 cost 2000000 [DeviceD-10GE1/0/2] stp vlan 30 cost 2000000 [DeviceD-10GE1/0/2] quit步骤6 使能VBST，实现破除环路。
全局使能VBST功能。
缺省情况下，全局VBST功能已使能。为确保全局VBST使能，可执行命令display stp vlan information查看VBST的使能状态。如果未使能，请在系统视图执行命令undo stp vlan disable全局使能VBST功能。
VLAN使能VBST功能。
缺省情况下，VLAN上的VBST功能处于使能状态。为确保VLAN的VBST功能使能，可执行命令display stp vlan vlan-id information查看VLAN上的VBST状态。如果提示该VLAN上VBST功能未使能，请在系统视图执行命令undo stp vlan vlan-id disable使能该VLAN的VBST功能。
---- 结束检查配置结果一段时间生成树协议计算稳定后，执行以下操作，验证配置结果。
\# 在DeviceA上执行display stp vlan bridge local命令，查看STP工作模式。根据Protocol字段可以看出，STP工作在VBST模式。
[DeviceA] display stp vlan bridge local
------------------------------------------------------------------ VLANID BridgeID HelloTime MaxAge ForwardDelay Protocol
------------------------------------------------------------------ 10 10.00e0-fc00-df01 2 20 15 VBST 20 20.00e0-fc00-df01 2 20 15 VBST 30 4126.00e0-fc00-df01 2 20 15 VBST
------------------------------------------------------------------

\# 在DeviceA、DeviceB、DeviceC和DeviceD上分别执行display stp vlan information brief命令，查看端口状态。以DeviceA回显为例，DeviceA分别参加VLAN10、VLAN20和VLAN30的生成树计算。DeviceA在VLAN10和VLAN20中都是根桥，所以在VLAN10中10GE1/0/1和10GE1/0/3都被选举为指定端口；在VLAN20中10GE1/0/1、10GE1/0/2和10GE1/0/3都被选举为指定端口。DeviceA在VLAN30中是备份根桥，所以VLAN30中10GE1/0/1被选举为根端口，10GE1/0/2被选举为指定端口。
[DeviceA] display stp vlan information brief
-------------------------------------------------------------------------------- VLANID Interface Role STPState Protection Cost Edged
-------------------------------------------------------------------------------- 10 10GE1/0/1 DESI forwarding none 200 disable 10 10GE1/0/3 DESI forwarding none 200 disable 20 10GE1/0/1 DESI forwarding none 200 disable 20 10GE1/0/2 DESI forwarding none 200 disable 20 10GE1/0/3 DESI forwarding none 200 disable 30 10GE1/0/1 ROOT forwarding none 200 disable 30 10GE1/0/2 DESI forwarding none 200 disable
--------------------------------------------------------------------------------配置脚本
● DeviceA \# sysname DeviceA \# stp vlan 10 20 root primary stp vlan 30 root secondary \# vlan batch 10 20 30 \# stp mode vbst \# interface 10GE1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 20 30 \# interface 10GE1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 20 30 \# interface 10GE1/0/3 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 20 \# return
● DeviceB \# sysname DeviceB \# stp vlan 10 20 root secondary stp vlan 30 root primary \# vlan batch 10 20 30 \# stp mode vbst \# interface 10GE1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 20 30 \# interface 10GE1/0/2 port link-type trunk

undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 20 \# interface 10GE1/0/3 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 20 30 \# return
● DeviceC \# sysname DeviceC \# vlan batch 10 20 \# stp mode vbst \# interface 10GE1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 20 stp vlan 10 20 cost 2000000 \# interface 10GE1/0/3 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 20 \# interface 10GE1/0/4 port link-type access port default vlan 10 \# interface 10GE1/0/5 port link-type access port default vlan 20 \# return
● DeviceD \# sysname DeviceD \# vlan batch 20 30 \# stp mode vbst \# interface 10GE1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 20 30 stp vlan 20 30 cost 2000000 \# interface 10GE1/0/3 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 20 30 \# interface 10GE1/0/4 port link-type access port default vlan 20 \# interface 10GE1/0/5 port link-type access port default vlan 30 \# return
