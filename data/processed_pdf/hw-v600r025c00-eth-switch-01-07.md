# S1700, S5700, S6700 V600R025C00 配置指南-以太网交换 01-07 STP RSTP MSTP配置

## 7 STP/RSTP/MSTP配置

### 7.1 STP/RSTP/MSTP简介

7.2 STP/RSTP/MSTP原理描述
7.3 STP/RSTP/MSTP配置注意事项
7.4 STP/RSTP/MSTP缺省配置
7.5 配置STP/RSTP/MSTP
7.6 配置MSTP多进程
7.7 启用边缘端口和配置BPDU报文过滤功能（RSTP/MSTP）
7.8 配置影响STP/RSTP/MSTP拓扑收敛的参数
7.9 配置RSTP/MSTP保护功能
7.10 配置设备与其他厂商设备互通的参数
7.11 维护STP/RSTP/MSTP
7.12 STP/RSTP/MSTP配置举例
7.1 STP/RSTP/MSTP 简介
定义
生成树协议是以太网中的破环协议，运行该协议的设备通过彼此交互信息来发现网络
中的环路，并有选择地对某些端口进行阻塞，最终将环形网络修剪成无环路的树形网
络，达到破除环路的目的。另外，如果当前活动的链路发生故障，生成树协议还可以
激活冗余备份链路，恢复网络连通性。
目的
以太网中为了进行链路备份，提高网络可靠性，通常会使用冗余链路，但是这也带来
了网络环路的问题。网络环路会引发广播风暴和 MAC 地址表振荡等问题，导致用户通
信质量差，甚至通信中断。为了解决环路问题，IEEE先后提出了生成树协议STP
（Spanning Tree Protocol）、快速生成树协议RSTP（Rapid Spanning Tree
Protocol）、多生成树协议MSTP（Multiple Spanning Tree Protocol）。

RSTP在STP基础上进行了改进，可实现网络拓扑的快速收敛。
STP和RSTP不能按VLAN阻塞冗余链路，局域网内所有的VLAN共享一棵生成树，所有VLAN的报文都沿着一棵生成树进行转发，因此无法在VLAN间实现流量的负载分担；
同时，链路被阻塞后将不承载任何流量，造成带宽浪费，还有可能造成部分VLAN的报文无法转发。MSTP弥补了STP和RSTP的缺陷，兼容STP和RSTP，既可以快速收敛，又提供了数据转发的多个路径，在数据转发过程中实现VLAN数据的负载均衡。
STP、RSTP和MSTP均可以实现破除环路和链路备份，这几种生成树协议的详细对比请参见表7-1。
表 7-1 生成树协议的比较

| 生成树协议 | 收敛速度 | 流量转发 | 配置复杂度 |
|---|---|---|---|
| STP（基于 IEEE 802.1d 标准） | 最慢 | 所有VLAN共享一棵生成树，所有VLAN 的流量按照同样的路径转发。 | 低 |
| RSTP（基于 IEEE 802.1w 标准） | RSTP和MSTP比 STP收敛速度快，但RSTP和 MSTP之间没有快慢之分。 | 所有VLAN共享一棵生成树，所有VLAN 的流量按照同样的路径转发。 | 低 |
| MSTP（基于 IEEE 802.1s 标准） |  | 通过实例与VLAN的映射，可以实现多棵生成树在VLAN间负载分担，不同VLAN 的流量按照不同的路径转发。每棵生成树之间相互独立。 | 高 |

### 7.2 STP/RSTP/MSTP原理描述

#### 7.2.1 设备角色、端口角色和端口状态

网络中部署并使能生成树协议后，设备间通过交互BPDU（Bridge Protocol Data Unit）报文进行生成树计算。当网络中每台设备的角色、设备上每个端口的角色以及端口状态确定后，生成树协议计算收敛完成，网络达到一个稳定状态。
设备角色生成树协议破环的关键在于生成一个树形的网络结构，而树形的网络结构必须有树根，即根桥RB（Root Bridge）。根桥是整个网络的逻辑中心，但不一定是物理中心。
除根桥外，网络中其他设备均为非根桥设备。根桥会根据网络拓扑的变化而动态变化。
STP/RSTP网络中有且仅有一个根桥；MSTP网络中可以生成多个生成树，即可以有多个根桥。
端口角色各生成树协议支持的端口角色如表7-2所示。

表 7-2 生成树协议支持的端口角色

| 生成树协议 | 根端口 | 指定端口 | Alterna te端口 | Backup 端口 | 边缘端口 | Master 端口 | 域边缘端口 |
|---|---|---|---|---|---|---|---|
| STP | √ | √ | √ | x | x | x | x |
| RSTP | √ | √ | √ | √ | √ | x | x |
| MSTP | √ | √ | √ | √ | √ | √ | √ |

根端口根端口就是去往根桥路径开销最小的端口，根端口负责向根桥方向转发数据。在一个运行STP/RSTP协议的设备上根端口有且只有一个，根桥上没有根端口。
指定端口指定端口和指定桥相关，具体含义如表7-3所示。
表 7-3 指定桥与指定端口的含义

| 分类 | 指定桥 | 指定端口 |
|---|---|---|
| 对于一台设备而言 | 与本机直接相连并且负责向本机转发配置消息的设备 | 指定桥向本机转发配置消息的端口 |
| 对于一个局域网而言 | 负责向本网段转发配置消息的设备 | 指定桥向本网段转发配置消息的端口 |

如图7-1所示，AP1、AP2、BP1、BP2、CP1、CP2分别表示设备DeviceA、DeviceB、DeviceC的端口。
● DeviceA通过端口AP1向DeviceB转发配置BPDU报文，则DeviceB的指定桥就是DeviceA，指定端口就是DeviceA的端口AP1。
● 与局域网LAN相连的有两台设备：DeviceB和DeviceC，假设DeviceB负责向LAN转发配置BPDU报文，则LAN的指定桥就是DeviceB，指定端口就是DeviceB的BP2。
图 7-1 指定桥与指定端口示意图

Alternate端口Alternate端口是根端口的备份端口，提供了从指定桥到根桥的另一条可切换路径。
Alternate端口是由于学习到其他网桥发送的配置BPDU报文而阻塞的端口。
Backup端口Backup端口作为指定端口的备份，提供了另一条从根桥到相应网段的备份通路。
Backup端口是由于学习到自己发送的配置BPDU报文而阻塞的端口。
如图7-2所示：DeviceC上CP2为根端口，CP1为Alternate端口，CP2故障时CP1可以切换为根端口；DeviceB上BP1为指定端口，BP2为Backup端口，BP1故障时BP2可以切换为指定端口。
图 7-2 Alternate 端口和 Backup 端口示意图边缘端口设备上与终端设备直连的端口为边缘端口。边缘端口位于网络的边缘，不参与生成树计算，可以直接进入转发状态。
端口使能生成树协议后，会默认启用边缘端口自动探测功能，当端口在（2 × Hello Time + 1）秒的时间内收不到BPDU报文，自动将端口设置为边缘端口，否则设置为非边缘端口。如果手动配置设备上端口为边缘端口，边缘端口自动探测功能就不生效了。
Master端口介绍Master端口和域边缘端口之前先了解几个MSTP的基本概念。MSTP网络中一般有多个MST（Multiple Spanning Tree）域，每个MST域内会计算出一棵生成树，即内部生成树 IST （ Internal Spanning Tree ）。将每个 MST 域看作一个节点，所有的 MST 域之间会计算出一棵生成树，即公共生成树CST（Common Spanning Tree）。所有的IST和CST构成一棵完整的生成树，即公共和内部生成树CIST（Common and Internal Spanning Tree）。总根即CIST中的根桥。

Master端口是MST域中和总根相连的路径最短的端口，是MST域中的报文去往总根的必经之路。
域边缘端口域边缘端口是指位于MST域的边缘并连接其他MST域或者单生成树的端口。
Master端口是特殊的域边缘端口，Master端口在CIST上的角色是根端口，在其他各实例上的角色都是Master端口。
如图7-3所示，设备DeviceA、DeviceB、DeviceC、DeviceD和它们之间的链路构成一个MST域。MST域内的端口AP1、DP1和DP2都和其他域直接相连，它们都是本MST域的域边缘端口。DeviceA的端口AP1在域内的所有端口中到总根的路径开销最小，所以AP1为Master端口。
图 7-3 Master 端口和域边缘端口示意图端口状态STP 端口状态运行STP协议的设备的端口存在5种端口状态，如表7-4所示。STP端口状态的迁移机制如图7-4所示。
表 7-4 STP 端口状态

| 端口状态 | 说明 |
|---|---|
| Disabled | 端口状态为Down，不处理BPDU报文，也不转发用户流量。 |
| Blocking | 端口仅接收并处理BPDU报文，不转发用户流量。 |
| Listening | 过渡状态，开始生成树计算，端口可以接收和发送BPDU报文，但不转发用户流量。 |

| 端口状态 | 说明 |
|---|---|
| Learning | 过渡状态，设备根据收到的用户流量构建MAC地址表。端口可以接收和发送BPDU报文，但不转发用户流量。 |
| Forwardi ng | 端口可以接收和发送BPDU报文，也转发用户流量。只有根端口或指定端口才能进入Forwarding状态。 |

图 7-4 STP 端口状态迁移图
1. 端口Up或使能了STP，会从Disabled状态进入到Blocking状态。
2. 端口被选举为根端口或指定端口，会进入Listening状态。
3. 端口的Forward Delay定时器超时，会进入Learning/Forwarding状态。
端口不再是根端口或指定端口时，会进入Blocking状态。
4.
5. 端口Down或者去使能STP时，就进入Disabled状态。
说明缺省情况下华为设备处于MSTP模式，当从MSTP模式切换到STP模式，运行STP协议的设备上端口支持的端口状态仍然保持和MSTP支持的端口状态一样，支持的状态仅包括Forwarding、Learning和Discarding。具体请参见下面RSTP/MSTP端口状态介绍。
RSTP/MSTP端口状态RSTP和MSTP支持的端口状态相同，相比于STP，RSTP/MSTP将端口状态缩减为3种，具体如表7-5所示。

表 7-5 RSTP/MSTP 端口状态

| 端口状态 | 说明 |
|---|---|
| Forwardi ng | 端口转发用户流量，也学习MAC地址，且接收和发送BPDU报文。 |
| Learning | 过渡状态，设备根据收到的用户流量构建MAC地址表。端口可以接收和发送BPDU报文，但不转发用户流量。 |
| Discardi ng | 端口只接收BPDU报文，不转发用户流量，也不学习MAC地址。 |

端口状态和端口角色是没有必然联系的，表7-6显示了各种端口角色能够具有的端口状态。Yes：表示端口支持的状态。No：表示端口不支持的状态。
表 7-6 端口状态和端口角色对应表

| 端口状态 | 根端口/ Master端口 | 指定端口 | 边缘端口/域边缘端口 | Alternate 端口 | Backup端口 |
|---|---|---|---|---|---|
| Forwar ding | Yes | Yes | Yes | No | No |
| Learnin g | Yes | Yes | Yes | No | No |
| Discardi ng | Yes | Yes | Yes | Yes | Yes |

#### 7.2.2 BPDU报文

生成树拓扑计算是基于设备之间交互BPDU报文实现的，BPDU报文中携带了生成树拓扑计算需要的信息。BPDU报文被封装在以太网数据帧中，目的MAC：01-80- C2-00-00-00。
BPDU 报文分类BPDU报文可以分为以下几类。
● 配置BPDU（Configuration BPDU）：STP用来进行生成树计算和维护生成树拓扑的报文。
● RST BPDU：RSTP用来进行生成树计算和维护生成树拓扑的报文。
● MST BPDU：MSTP用来进行生成树计算和维护生成树拓扑的报文。
● TCN BPDU（Topology Change Notification BPDU）：网络拓扑发生变化时用来通知相关设备的报文。

BPDU 报文格式BPDU报文中根据Protocol Version Identifier和BPDU Type字段取值判断BPDU报文类型，具体如表7-7所示。
表 7-7 BPDU 报文类型

| Protocol Version Identifier | BPDU Type | BPDU报文类型 |
|---|---|---|
| 0 | 0x00 | 配置BPDU |
| 2 | 0x02 | RST BPDU |
| 3 | 0x02 | MST BPDU |
| 0 | 0x80 | TCN BPDU |

● 配置BPDU使用图7-5中的前35个字节。其中Root Identifier、Root Path Cost、
Bridge Identifier、Port Identifier字段是配置BPDU报文的核心内容，这4个字段
构成了消息优先级向量{ 根桥ID，根路径开销，发送设备BID，发送端口PID }。
– Root Identifier：当前根桥的BID（Bridge ID）。BID是由桥优先级（Bridge
Priority）与桥MAC地址构成。BID桥优先级占据高16位，其余的低48位是
MAC地址。BID最小的设备会被选举为根桥。
– Root Path Cost：根路径开销，简称RPC。路径开销（Path Cost）是一个端
口变量，是生成树协议用于选择链路的参考值。生成树协议通过计算路径开
销，选择较为“强壮”的链路，阻塞多余的链路，将网络修剪成无环路的树
形网络结构。根路径开销就是某端口到根桥所经过的各个桥上的各端口路径
开销的累加值。
– Bridge Identifier：发送设备的BID。
– Port Identifier：发送端口的PID（Port ID）。PID由两部分构成的，高4位是
端口优先级，低12位是端口号。
● RST BPDU和配置BPDU基本一致，RST BPDU作了一些小变化。增加了Version 1
Length字段，并且Flags字段使用了中间的六位。Flags字段STP仅使用了最低位和
最高位，中间六位保留。而RSTP使用了中间六位，如图7-6所示。
● MST BPDU 前 36 个字节和 RST BPDU 相同，从第 37 个字节开始是 MSTP 专有字段。
最后的MSTI配置信息字段由若干MSTI配置信息组连缀而成。
● TCN BPDU长度为4个字节，只使用了图7-5中的前3个字段，即只有Protocol
Identifier（协议号）、Protocol Version Identifier（协议版本）和BPDU Type
（BPDU类型）。
BPDU报文各字段含义详见表7-8。

表 7-8 BPDU 报文各字段含义

| 域 | 字节 | 说明 |
|---|---|---|
| Protocol Identifier | 2 | 协议标识符。 ● 高4 bytes：表示协议ID。 ● 低12 bytes：表示进程ID。 |
| Protocol Version Identifier | 1 | 协议版本标识符，STP为0，RSTP为2，MSTP为3。 |
| BPDU Type | 1 | 当前BPDU类型： ● 0x00：配置BPDU。 ● 0x80：TCN BPDU。 ● 0x02：Protocol Version Identifier为2时代表RST BPDU，Protocol Version Identifier为3时代表MST BPDU。 |
| Flags | 1 | 网络拓扑变化标志。对于MSTP，是指CIST标志字段。 ● 最低位=TC（Topology Change，拓扑变化）标志。 ● 最高位=TCA（Topology Change Acknowledgment，拓扑变化确认）标志。 |
| Root Identifier | 8 | 当前根桥的BID。对于MSTP，代表CIST的总根BID。 |
| Root Path Cost | 4 | 根路径开销，本端口累计到根桥的开销。对于MSTP，是指CIST外部路径开销，从本设备所属的MST域到CIST 根桥所属MST域的累计路径开销。CIST外部路径开销根据链路带宽计算。 |
| Bridge Identifier | 8 | 本设备的BID。对于MSTP，是指CIST的域根设备ID，即 IST Master的ID。如果总根在这个域内，那么域根设备 ID就是总根设备ID。 |
| Port Identifier | 2 | 发送该BPDU的端口ID。对于MSTP，是指本端口在IST 中的指定端口ID。 |
| Message Age | 2 | BPDU报文的生存期。如果配置BPDU是根桥发出的，则Message Age为0。否则，Message Age是从根桥发送到当前桥接收到BPDU 的总时间，包括传输延时等。实际实现中，配置BPDU 报文经过一个桥，Message Age增加一个固定值（当 Max Age < 24时，固定值为1；当 24 ≤ Max Age < 40 时，固定值为2；当Max Age = 40时，固定值为3）。 |
| Max Age | 2 | BPDU报文的最大生存期，超时则认为到根设备的链路故障。 |
| Hello Time | 2 | Hello Time定时器，缺省为2秒，即发送两个相邻BPDU 的时间间隔。 |
| Forward Delay | 2 | Forward Delay定时器，缺省为15秒。控制Listening和 Learning状态的持续时间。 |

| 域 | 字节 | 说明 |
|---|---|---|
| Version 1 Length | 1 | Version1 BPDU的长度，值固定为0。 |
| Version 3 Length | 2 | Version3 BPDU的长度。 IEEE 802.1s模式：该字段位于37-38字节。 Legacy模式：该字段位于38-39字节。 |
| MST Configuration Identifier | 51 | MST配置标识，表示MST域的标签信息，包含4个字段。 |
| CIST Internal Root Path Cost | 4 | CIST内部路径开销指从本端口到IST Master设备的累计路径开销。CIST内部路径开销根据链路带宽计算。 IEEE 802.1s模式：该字段位于90-93字节 Legacy模式：该字段位于98-101字节。 |
| CIST Bridge Identifier | 8 | CIST的指定设备ID。 IEEE 802.1s模式：该字段位于94-101字节。 Legacy模式：该字段位于90-97字节。 |
| CIST Remaining Hops | 1 | BPDU报文在CIST中的剩余跳数。 |
| MSTI Configuration Messages(may be absent) | 16 | MSTI配置信息。每个MSTI的配置信息占16 bytes，如果有n个MSTI就占用n×16bytes。实例ID包含在每个MSTI的配置信息中。 |

说明：IEEE 802.1s和Legacy报文格式整体是一致的，区别仅为表2 BPDU报文各字段含义中部分字段位置差异。

#### 7.2.3 生成树协议定时器

BPDU报文中携带的与时间相关的字段包括Hello Time、Forward Delay、Max Age和Message Age。其中Hello Time、Forward Delay和Max Age为三个定时器的值，缺省值分别为2秒、15秒、20秒，设备也支持手工配置。
Hello Time 定时器和超时时间设备每隔Hello Time时间会向周围设备发送BPDU报文，以确认链路是否存在故障。如果设备在超时时间内没有收到上游设备发送的BPDU，则生成树会重新进行计算。超时时间的计算公式如下，其中Timer Factor缺省值为3，设备支持手工配置Timer Factor来调整超时时间。
超时时间＝Hello Time × 3 × Timer Factor当网络拓扑稳定之后，Hello Time定时器的值只有在根桥修改后才有效。新的根桥会在发出的BPDU报文中填充相应的字段以向非根桥传递该定时器修改的信息。但当拓扑变化之后，TCN BPDU的发送不受这个定时器的管理。

Forward Delay 定时器设备状态迁移的延迟时间。链路故障会引发网络重新进行生成树的计算，生成树的结构将发生相应的变化。不过重新计算得到的新配置消息无法立刻传遍整个网络，如果新选出的根端口和指定端口立刻就开始数据转发的话，可能会造成临时环路。为此，STP采用了一种状态迁移机制，新选出的根端口和指定端口要经过2倍的Forward Delay延时后才能进入转发状态，这个延时保证了新的配置消息传遍整个网络，从而防止了临时环路的产生。
Forward Delay定时器指一个端口处于Listening和Learning状态的各自持续时间，默认是15秒。即Listening状态持续15秒，随后Learning状态再持续15秒。这两个状态下的端口均不转发用户流量，这正是STP用于避免临时环路的关键。
Max Age 定时器和 Message Age Max Age定时器的值即BPDU报文老化时间，可在根桥上通过命令人为改动老化时间。
Max Age通过BPDU报文的传输，可保证Max Age在整网中一致。运行生成树协议的网络中非根桥设备收到BPDU报文后，报文中的Message Age和Max Age会进行比较：
● 如果 Message Age 小于等于 Max Age ，则该非根桥设备继续转发 BPDU 报文。
● 如果Message Age大于Max Age，则该BPDU报文将被老化。该非根桥设备直接丢弃该BPDU，可认为网络直径过大，导致根桥连接失败。
如果配置BPDU（这里以配置BPDU举例，RST BPDU/MST BPDU的情况类似）是根桥发出的，则Message Age为0。否则，Message Age是从根桥发送到当前桥接收到BPDU的总时间，包括传输延时等。实际实现中，配置BPDU报文每经过一个桥，Message Age增加一个固定值（当Max Age < 24时，固定值为1；当 24 ≤ Max Age < 40时，固定值为2；当Max Age = 40时，固定值为3）。
如图7-7所示：
DeviceB和DeviceC从DeviceA收到配置BPDU，Message Age为0，所以在DeviceB
●和DeviceC去往DeviceA的端口上，配置BPDU报文的老化时间为（Max Age－
0）。
● DeviceD和DeviceE从DeviceB收到配置BPDU，Message Age为1，所以在DeviceD和DeviceE去往DeviceA的端口上，配置BPDU报文的老化时间为（Max Age－
1）。
● DeviceF从DeviceE收到配置BPDU，Message Age为2，所以在DeviceF去往DeviceA的端口上，配置BPDU报文的老化时间为（Max Age－2）。

图 7-7 Message Age 示意图

#### 7.2.4 根桥、根端口和指定端口的选举原则

BPDU报文中携带的Root Identifier、Root Path Cost、Bridge Identifier、Port Identifier字段构成了消息优先级向量{ 根桥ID，根路径开销，发送设备BID，发送端口}。设备通过交互并比较消息优先级向量中各字段的值确定根桥、根端口、指定端PID口。
● BID由桥优先级（Bridge Priority）与桥MAC地址构成，高16位是桥优先级，其余的低48位是MAC地址。
● 根路径开销RPC（Root Path Cost）就是某端口到根桥所经过的各个桥上的各端口路径开销的累加值。路径开销（Path Cost）是一个端口变量，是生成树协议用于选择链路的参考值。生成树协议通过计算路径开销，选择较为“强壮”的链路，阻塞多余的链路，将网络修剪成无环路的树形网络结构。
● PID由两部分构成的，高4位是端口优先级，低12位是端口号。
根桥选举最小BID原则：BID最小的设备被选举为根桥。
根端口选举
1. 最小RPC原则：非根桥设备上，根路径开销RPC最小的端口被选举为根端口。
2. 最小发送设备BID原则：非根桥设备上如果有两个及以上端口的根路径开销相同，则收到BPDU报文中“发送设备BID”最小的端口被选举为根端口。
根桥上每个端口到根桥的根路径开销都是0，根桥上没有根端口。
指定端口选举最小PID原则：根路径开销相同的情况下，阻塞PID值较大的端口，PID小的端口被选举为指定端口。

如图7-8所示的情况下PID才起作用，DeviceA上端口PA1的PID小于端口PA2的PID，由于两个端口上收到的BPDU中，根路径开销、发送设备BID都相同，所以消除环路的依据就只有PID。
图 7-8 应用 PID 进行比较的拓扑

#### 7.2.5 STP/RSTP拓扑计算方法

网络中所有的设备使能生成树协议后，每一台设备都认为自己是根桥。此时，每台设备不转发用户流量，仅收发配置BPDU/RST BPDU。所有设备通过交互配置BPDU/RST BPDU进行选举工作，选出根桥、根端口和指定端口。
STP/RSTP 算法实现的基本过程
1. 初始状态由于每个桥都认为自己是根桥，所以在每个端口所发出的BPDU中，根桥字段都是用各自的BID，RPC字段是累计的到根桥的开销（初始状态由于每个桥都认为自己是根桥，因此RPC为0），发送者BID是自己的BID，端口PID是发送该BPDU端口的端口ID。
2. 选择根桥网络初始化时，网络中所有的STP设备都认为自己是“根桥”，根桥ID为自身的设备ID。通过交换配置消息，设备之间比较根桥ID，网络中BID最小的设备被选为根桥。
3. 选择根端口和指定端口，选择过程如表7-9所示表 7-9 根端口和指定端口的选择过程

| 步骤 | 过程 |
|---|---|
| 1 | 非根桥设备将接收最优配置消息（最优配置消息的选择过程如表7-10所示）的那个端口定为根端口。 |

| 步骤 | 过程 |
|---|---|
| 2 | 设备根据根端口的配置消息和根端口的路径开销，为每个端口计算一个指定端口配置消息： ● 根桥ID替换为根端口的配置消息的根桥ID； ● 根路径开销替换为根端口配置消息的根路径开销加上根端口对应的路径开销； ● 发送者BID替换为自身设备的ID； ● 发送端口PID替换为自身端口ID。 |
| 3 | 设备将计算出的配置消息与角色待定端口自己的配置消息进行比较： ● 如果计算出的配置消息更优，则该端口被确定为指定端口，其配置消息也被计算出的配置消息替换，并周期性地向外发送； ● 如果该端口自己的配置消息更优，则不更新该端口的配置消息并将该端口阻塞。该端口将不再转发数据，且只接收不发送配置消息。 |

表 7-10 最优配置消息的选择过程

| 步骤 | 过程 |
|---|---|
| 1 | 每个端口将收到的配置消息与自己的配置消息进行比较： ● 如果收到的配置消息优先级较低，则将其直接丢弃，对自己的配置消息不进行任何处理； ● 如果收到的配置消息优先级较高，则用该配置消息的内容将自己配置消息的内容替换掉； ● 如果收到的配置消息和自己的一样，则将其直接丢弃。 |
| 2 | 设备将所有端口的配置消息进行比较，选出最优的配置消息。 |

STP 算法实现举例一旦根桥、根端口和指定端口选举成功，整个树形拓扑就建立完毕了。下面结合例子说明STP算法实现的具体过程。

图 7-9 组网图及 STP 计算后的拓扑如图7-9所示，DeviceA、DeviceB和DeviceC的优先级分别为0、1和2，DeviceA与DeviceB之间、DeviceA与DeviceC之间以及DeviceB与DeviceC之间链路的路径开销分别为5、10和4。
1. 各设备的初始状态如表7-11所示。
表 7-11 各设备的初始状态

| 设备 | 端口名称 | 端口的配置消息 {根桥ID，根路径开销，发送设备BID，发送端口PID} |
|---|---|---|
| DeviceA | Port A1 | {0，0，0，Port A1} |
|  | Port A2 | {0，0，0，Port A2} |
| DeviceB | Port B1 | {1，0，1，Port B1} |
|  | Port B2 | {1，0，1，Port B2} |
| DeviceC | Port C1 | {2，0，2，Port C1} |
|  | Port C2 | {2，0，2，Port C2} |

各设备的比较过程及结果如表7-12所示。
2.

表 7-12 STP 拓扑计算过程及结果

| 设备 | 比较过程 | 比较后端口的配置消息 |
|---|---|---|
| Dev iceA | ● Port A1收到Port B1的配置消息{1，0， 1，Port B1}，发现自己的配置消息{0， 0，0，Port A1}更优，于是将其丢弃。 ● Port A2收到Port C1的配置消息{2，0， 2，Port C1}，发现自己的配置消息{0， 0，0，Port A2}更优，于是将其丢弃。 ● DeviceA发现自己各端口的配置消息中的根桥和指定桥都是自己，于是认为自己就是根桥，各端口的配置消息都不作任何修改，此后便周期性地向外发送配置消息。 | ● Port A1：{0，0，0， Port A1} ● Port A2：{0，0，0， Port A2} |
| Dev iceB | ● Port B1收到Port A1的配置消息{0，0， 0，Port A1}，发现其比自己的配置消息 {1，0，1，Port B1}更优，于是更新自己的配置消息。 ● Port B2收到Port C2的配置消息{2，0， 2，Port C2}，发现自己的配置消息{1， 0，1，Port B2}更优，于是将其丢弃。 | ● Port B1：{0，0，0， Port A1} ● Port B2：{1，0，1， Port B2} |
|  | ● DeviceB比较自己各端口的配置消息，发现Port B1的配置消息最优，于是该端口被确定为根端口，其配置消息不变。 ● DeviceB根据根端口的配置消息和路径开销，为Port B2计算出指定端口的配置消息 {0，5，1，Port B2}，然后与Port B2本身的配置消息{1，0，1，Port B2}进行比较，发现计算出的配置消息更优，于是 Port B2被确定为指定端口，其配置消息也被替换为计算出的配置消息，并周期性地向外发送。 | ● 根端口Port B1：{0， 0，0，Port A1} ● 指定端口Port B2： {0，5，1，Port B2} |
| Dev iceC | ● Port C1收到Port A2的配置消息{0，0， 0，Port A2}，发现其比自己的配置消息 {2，0，2，Port C1}更优，于是更新自己的配置消息。 ● Port C2收到Port B2更新前的配置消息 {1，0，1，Port B2}，发现其比自己的配置消息{2，0，2，Port C2}更优，于是更新自己的配置消息。 | ● Port C1：{0，0，0， Port A2} ● Port C2：{1，0，1， Port B2} |

| 设备 | 比较过程 | 比较后端口的配置消息 |
|---|---|---|
|  | ● DeviceC比较自己各端口的配置消息，发现Port C1的配置消息最优，于是该端口被确定为根端口，其配置消息不变。 ● DeviceC根据根端口的配置消息和路径开销，为Port C2计算出指定端口的配置消息 {0，10，2，Port C2}，然后与Port C2本身的配置消息{1，0，1，Port B2}进行比较，发现计算出的配置消息更优，于是 Port C2被确定为指定端口，其配置消息也被替换为计算出的配置消息。 | ● 根端口Port C1：{0， 0，0，Port A2} ● 指定端口Port C2： {0，10，2，Port C2} |
|  | ● Port C2收到Port B2更新后的配置消息 {0，5，1，Port B2}，发现其比自己的配置消息{0，10，2，Port C2}更优，于是更新自己的配置消息。 ● Port C1收到Port A2周期性发来的配置消息{0，0，0，Port A2}，发现其与自己的配置消息一样，于是将其丢弃。 | ● Port C1：{0，0，0， Port A2} ● Port C2：{0，5，1， Port B2} |
|  | ● DeviceC比较Port C1的根路径开销10（收到的配置消息中的根路径开销0＋本端口所在链路的路径开销10）与Port C2的根路径开销9（收到的配置消息中的根路径开销5＋本端口所在链路的路径开销4），发现后者更小，因此Port C2的配置消息更优，于是Port C2被确定为根端口，其配置消息不变。 ● DeviceC根据根端口的配置消息和路径开销，为Port C1计算出指定端口的配置消息 {0，9，2，Port C1}，然后与Port C1本身的配置消息{0，0，0，Port A2}进行比较，发现本身的配置消息更优，于是Port C1被阻塞，其配置消息不变。从此，Port C1不再转发数据，直至有触发生成树计算的新情况出现，譬如DeviceB与DeviceC之间的链路down掉。 | ● 阻塞端口Port C1： {0，0，0，Port A2} ● 根端口Port C2：{0， 5，1，Port B2} |

网络收敛后，根桥会按照一定的时间间隔产生并向外发送配置BPDU，其他设备收到该配置BPDU后，如果优先级比自己的配置BPDU高，则非根桥设备会根据收到的配置BPDU中携带的信息更新自己相应的端口存储的配置BPDU信息，否则会丢弃该配置BPDU。

#### 7.2.6 MSTP拓扑计算方法

MSTP 基本概念MSTP网络中包含1个或多个MST域（Multiple Spanning Tree Region），每个MST Region中包含一个或多个MSTI。MSTI是所有运行STP/RSTP/MSTP的设备经MSTP协议计算后形成的树状网络。
图 7-10 MSTP 网络层次示意图MST域（MST Region）
MST域是多生成树域，由网络中的多台设备以及它们之间的网段所构成。同一个MST域的设备具有下列特点：
● 都启动了MSTP。

● 具有相同的域名。
● 具有相同的VLAN到生成树实例映射配置。
● 具有相同的MSTP修订级别配置。
一个局域网可以存在多个MST域，各MST域之间在物理上直接或间接相连。用户可以
通过MSTP配置命令把多台设备划分在同一个MST域内。
如图7-11所示，MST Region 4中由设备B、C、D和E构成，域中有3个MSTI。
图 7-11 MST Region 示意图
VLAN映射表
VLAN映射表描述了VLAN和MSTI之间的映射关系。
如图7-11所示，MST Region 4的VLAN映射表是：
● VLAN1映射到MSTI1
● VLAN2映射到MSTI2
● 其余VLAN映射到MSTI3
CST、IST、CIST、SST
● 公共生成树 CST （ Common Spanning Tree ）是连接网络内所有 MST 域的一棵生成
树。
如果把每个MST域看作是一个节点，CST就是这些节点通过STP或RSTP协议计算生
成的一棵生成树。如图7-10所示，黑色线条连接各个域构成CST。
● 内部生成树IST（Internal Spanning Tree）是各MST域内的一棵生成树。
IST是一个特殊的MSTI，MSTI的ID为0，通常称为MSTI0。
IST是CIST在MST域中的一个片段。如图7-10所示，深蓝色线条在域中连接该域的
所有交换设备构成IST。
● 公共和内部生成树CIST（Common and Internal Spanning Tree）是通过STP或
RSTP协议计算生成的，连接一个网络内所有设备的单生成树。如图7-10所示，所
有MST域的IST加上CST就构成一棵完整的生成树，即CIST。
● 单生成树SST（Single Spanning Tree）有两种情况：

– 运行STP或RSTP的设备只能属于一个生成树。
– MST域中只有一个设备，这个设备构成单生成树。
域根、总根、主桥
● 域根（Regional Root）分为IST域根和MSTI域根。
IST域根如图7-10所示，在MST域中IST生成树中距离总根（CIST Root）最近的设
备是IST域根。
一个MST域内可以生成多棵生成树，每棵生成树都称为一个MSTI。MSTI域根是每
个多生成树实例的树根。如图7-10所示，域中不同的MSTI有各自的域根。
● 总根是CIST（Common and Internal Spanning Tree）的根桥。如图7-10中的
DeviceA。
● 主桥（Master Bridge）也就是IST Master，它是域内距离总根最近的交换设备。
如图7-10中的黄色标识的设备。
如果总根在MST域中，则总根为该域的主桥。
MSTP 拓扑计算
MSTP可以将整个二层网络划分为多个MST域，各个域之间通过计算生成CST。域内则
通过计算生成多棵生成树，每棵生成树都被称为是一个多生成树实例。其中实例0被称
为IST，其他的多生成树实例为MSTI。MSTP同STP一样，使用配置消息进行生成树的
计算，只是配置消息中携带的是设备上MSTP的配置信息。
优先级向量
MSTI和CIST都是根据优先级向量来计算的，这些优先级向量信息都包含在MST BPDU
中。各设备互相交换MST BPDU来生成MSTI和CIST。
● 参与CIST计算的优先级向量为：
{ 根交换设备ID，外部路径开销，域根ID，内部路径开销，指定交换设备ID，指定
端口ID，接收端口ID }
● 参与MSTI计算的优先级向量为：
{ 域根ID，内部路径开销，指定交换设备ID，指定端口ID，接收端口ID }
括号中的向量的优先级从左到右依次递减。各字段详见表7-13。
表 7-13 向量说明

| 向量名 | 说明 |
|---|---|
| 根交换设备ID | 根交换设备ID用于选择CIST中的根交换设备。根交换设备ID = Priority(16bits) + MAC(48bits)。其中Priority为MSTI0的优先级。 |
| 外部路径开销（ERPC） | 从CIST的域根到达总根的路径开销。MST域内所有交换设备上保存的外部路径开销相同。若CIST根交换设备在域中，则域内所有交换设备上保存的外部路径开销为0。 |
| 域根ID | 域根ID用于选择MSTI中的域根。域根ID = Priority(16bits) + MAC(48bits)。其中Priority为MSTI0的优先级。 |

| 向量名 | 说明 |
|---|---|
| 内部路径开销（IRPC） | 本桥到达域根的路径开销。域边缘端口保存的内部路径开销大于非域边缘端口保存的内部路径开销。 |
| 指定交换设备ID | CIST或MSTI实例的指定交换设备是本桥通往域根的最邻近的上游桥。如果本桥就是总根或域根，则指定交换设备为自己。 |
| 指定端口ID | 指定交换设备上同本设备上根端口相连的端口。Port ID = Priority(4位) + 端口号（12位）。端口优先级必须是16的整数倍。 |
| 接收端口ID | 接收到BPDU报文的端口。Port ID = Priority(4位) + 端口号（12位）。端口优先级必须是16的整数倍。 |

比较原则同一向量比较，值最小的向量具有最高优先级。
优先级向量比较原则如下。
1. 首先，比较根交换设备ID。
2. 如果根交换设备ID相同，再比较外部路径开销。
3. 如果外部路径开销相同，再比较域根ID。
4. 如果域根ID仍然相同，再比较内部路径开销。
5. 如果内部路径仍然相同，再比较指定交换设备ID。
6. 如果指定交换设备ID仍然相同，再比较指定端口ID。
7. 如果指定端口ID还相同，再比较接收端口ID。
如果端口接收到的BPDU内包含的配置消息优于端口上保存的配置消息，则端口上原来保存的配置消息被新收到的配置消息替代。端口同时更新交换设备保存的全局配置消息。反之，新收到的BPDU被丢弃。
CIST的计算经过比较配置消息后，在整个网络中选择一个优先级最高的设备作为CIST的树根。在每个MST域内MSTP通过计算生成IST；同时MSTP将每个MST域作为单台设备对待，通过计算在MST域间生成CST。CST和IST构成了整个网络的CIST。
MSTI的计算在MST域内，MSTP根据VLAN和生成树实例的映射关系，针对不同的VLAN生成不同的生成树实例。每棵生成树独立进行计算，计算过程与STP计算生成树的过程类似。
MSTI的特点：
● 每个MSTI独立计算自己的生成树，互不干扰。
● 每个MSTI的生成树计算方法与STP基本相同。
● 每个MSTI的生成树可以有不同的根，不同的拓扑。
● 每个 MSTI 在自己的生成树内发送 BPDU 。
● 每个MSTI的拓扑通过命令配置决定。
● 每个端口在不同MSTI上的生成树参数可以不同。

● 每个端口在不同MSTI上的角色、状态可以不同。
在运行MSTP协议的网络中，一个VLAN报文将沿着如下路径进行转发：
● 在MST域内，沿着其对应的MSTI转发。
在MST域间，沿着CST转发。
●

#### 7.2.7 拓扑变化机制

网络中发生拓扑变化时，例如链路中断或接口异常Down等情况，由于MAC地址的老化时间的存在（缺省为5分钟），如果不及时通知上游设备，会导致上游设备的报文在这段时间内一直向一个不可达的链路发送。如图7-12所示，正常情况下，DeviceA和DeviceB之间的链路被阻塞，由A到B的流量依次流经DeviceA、DeviceC、DeviceD和DeviceB。如果DeviceC和DeviceD之间的链路发生故障，流量需要由DeviceA直接转发到DeviceB，但是在DeviceA上，仍然存在指向DeviceC的MAC地址表项，因此在此MAC地址表项老化前，流量还会转发给DeviceC，这样就导致流量的丢失。此时就需要拓扑变化机制来将拓扑的变更及时通知到整个网络。
图 7-12 MAC 地址未老化导致流量丢失生成树协议拓扑变化处理过程如图7-13所示。
图 7-13 TCN 的发送和 TC 的泛洪

1. T点接口发生变更后，下游设备会不间断地向上游设备发送TCN BPDU报文。
2. 上游设备收到下游设备发来的TCN BPDU报文后，只有指定端口处理TCN BPDU报
文。其他端口也有可能收到TCN BPDU报文，但不会处理。
3. 上游设备会把BPDU报文中的Flags的TCA位置1，然后发送给下游设备，告知下游
设备停止发送TCN BPDU报文。
4. 上游设备复制一份TCN BPDU报文，向根桥方向发送。
5. 重复步骤1、2、3、4，直到根桥收到TCN BPDU报文。
6. 根桥把BPDU报文中Flags的TC位和TCA位同时置1后发送，TC位置1是为了通知下
游设备直接删除桥MAC地址表项，TCA位置1是为了通知下游设备停止发送TCN
BPDU报文。
说明
● TCN BPDU报文主要用来向上游设备乃至根桥通知拓扑变化。
● TCA标记置位的配置BPDU报文主要是上游设备用来告知下游设备已经知道拓扑变化，通知下
游设备停止发送TCN BPDU报文。
● TC标记置位的配置BPDU报文主要是上游设备用来告知下游设备拓扑发生变化，请下游设备
直接删除桥 MAC 地址表项，从而达到快速收敛的目的。
在一个运行RSTP的网络中，检测拓扑是否发生变化只有一个标准：一个非边缘端口迁
移到Forwarding状态。
一旦检测到拓扑发生变化，设备将进行如下处理：
● 为本交换设备的所有非边缘指定端口和根端口启动一个TC While Timer，该计时
器值是Hello Time的两倍。
在这个时间内，清空所有端口上学习到的MAC地址。同时，由非边缘指定端口和
根端口向外发送RST BPDU，其中TC置位。一旦TC While Timer超时，则停止发
送RST BPDU。
● 其他交换设备接收到RST BPDU后，清空所有端口学习到MAC地址，除了收到RST
BPDU的端口。然后也为自己所有的非边缘指定端口和根端口启动TC While
Timer，重复上述过程。
这样就实现了RST BPDU在网络中的泛洪。

#### 7.2.8 RSTP/MSTP快速收敛机制

RSTP/MSTP 快速收敛的关键在于引入了 Proposal/Agreement 机制、根端口快速切换机制、边缘端口。
Proposal/Agreement 机制Proposal/Agreement机制简称P/A机制，其目的是使一个指定端口尽快进入Forwarding状态。P/A机制分为普通P/A机制和增强P/A机制两种。
普通P/A机制如图 7-14 所示，根桥 DeviceA 和 DeviceB 之间新添加了一条链路。在当前状态下，DeviceB的另外几个端口p2是Alternate端口，p3是指定端口且处于Forwarding状态，p4是边缘端口。

图 7-14 普通 P/A 机制示意图新链路连接成功后，P/A机制协商过程如下：
1. p0和p1两个端口马上都先成为指定端口，发送RST BPDU。
2. DeviceB的p1口收到更优的RST BPDU，马上意识到自己将成为根端口，而不是指定端口，停止发送RST BPDU。
3. DeviceA的p0进入Discarding状态，于是发送的RST BPDU中把Proposal和Agreement置1。
4. DeviceB收到根桥发送来的携带Proposal的RST BPDU，开始将自己的所有端口进入sync变量置位。
5. p2已经阻塞，状态不变；p4是边缘端口，不参与运算；所以只需要阻塞非边缘指定端口p3。
6. 各端口的synced变量置位后，p2、p3进入Discarding状态，p1进入Forwarding状态并向DeviceA返回Agreement位置位的回应RST BPDU。
7. 当DeviceA判断出这是对刚刚发出的Proposal的回应，于是端口p0马上进入Forwarding状态。
下游设备继续执行P/A协商过程。
事实上对于STP，指定端口的选择可以很快完成，主要的速度瓶颈在于：为了避免环路，必须等待足够长的时间，使全网的端口状态全部确定，也就是说必须要等待至少一个Forward Delay所有端口才能进行转发。而RSTP的主要目的就是消除这个瓶颈，通过阻塞自己的非根端口来保证不会出现环路。而使用P/A机制加快了上游端口转到Forwarding状态的速度。
说明P/A机制要求两台交换设备之间链路必须是点对点的全双工模式。一旦P/A协商不成功，指定端口的选择就需要等待两个Forward Delay，协商过程与STP一样。

增强P/A机制如图7-15所示，增强P/A机制工作过程如下：
1. 协商开始时，每一台设备都认为自己是根桥，根桥上的端口是指定端口，端口状态为Discarding，端口的synced变量置位，触发Proposal和Agreement同时置位。
上游设备发送Proposal报文，请求进行快速迁移。下游设备接收到后，把与上游设备相连的端口设置为根端口，并阻塞所有非边缘端口。
2. 上游设备继续发送Agreement报文。下游设备接收到后，根端口转为Forwarding状态。
3. 下游设备回应Agreement报文。上游设备接收到后，把与下游设备相连的端口设置为指定端口，指定端口进入Forwarding状态。
缺省情况下，设备使用增强的快速迁移机制。如果设备和其他厂商的设备进行互通，而其他厂商设备使用普通的P/A机制，此时，可在华为设备上通过设置P/A机制为普通的快速迁移机制，从而实现华为设备和其他厂商设备进行互通。
图 7-15 增强 P/A 机制示意图根端口快速切换机制如果RSTP/MSTP网络中一个根端口失效，那么网络中最优的Alternate端口将成为根端口并直接进入Forwarding状态。因为通过这个Alternate端口连接的网段上必然有个指定端口可以通往根桥。
如图7-16所示，DeviceA为根桥，DeviceB为备份根桥，DeviceC的interface2为Alternate端口。DeviceC的根端口interface1接口故障：STP模式时，DeviceC的interface2会先切换成根端口并进入Discarding状态，等待一个Forward Delay时间（缺省值为15秒）后进入Learning状态，继续等待一个Forward Delay时间（缺省值为15秒）后才进入Forwarding状态。RSTP/MSTP模式时，DeviceC的interface2会切换成根端口，并直接进入Forwarding状态。
相比较STP模式时接口需要等待2*Forward Delay时间才能进入Forwarding状态，RSTP/MSTP模式时的根端口快速切换机制使接口直接切换成Forwarding状态，减少业务流量丢包。

图 7-16 根端口快速切换机制边缘端口在RSTP/MSTP里面，如果某一个指定端口位于整个网络的边缘，即不再与其他交换设备连接，而是直接与终端设备直连，这种端口叫做边缘端口。
边缘端口不参与生成树运算，可以由Disable直接转到Forwarding状态，且不经历时延，就像在端口上将生成树协议禁用。但是一旦边缘端口收到BPDU，就丧失了边缘端口属性，成为普通端口，并重新进行生成树计算，从而引起网络振荡，BPDU保护可以解决此问题。

#### 7.2.9 STP/RSTP/MSTP兼容性

RSTP 兼容 STP RSTP可以和STP互相兼容，但是此时会失去RSTP的快速收敛等优势。
运行RSTP的设备与运行STP的设备相连时：运行STP的设备会忽略RSTP BPDU；运行RSTP的设备在某端口上接收到运行STP的设备发出的配置BPDU，在两个Hello Time时间之后，便把自己的端口转换到 STP 模式，发送配置 BPDU ，从而实现了互相兼容。
运行STP的设备被撤离网络后，运行RSTP的设备上可以手动执行MCheck操作，使与之相连的端口迁移回原来的RSTP模式。
MSTP 兼容 STP/RSTP运行MSTP的设备与运行STP的设备相连时，运行MSTP的设备会将与STP设备相连的接口切换到STP模式，实现互相兼容。
运行 STP 的设备被撤离网络后，运行 MSTP 的设备上可以手动执行 MCheck 操作，使与之相连的端口迁移回原来的MSTP模式。
运行MSTP的设备与运行RSTP的设备之间可以互相识别报文。

### 7.3 STP/RSTP/MSTP配置注意事项

License 依赖STP/RSTP/MSTP特性无需License许可即可使用。
硬件依赖表 7-14 支持本特性的硬件

| 系列 | 支持产品 |
|---|---|
| S6750-H | S6750-H36C，S6750-H48X8C，S6750-H48Y8C |
| S1730S-S3 | S1730S-S24P4S-A3，S1730S-S24P4X-A3， S1730S-S24T4S-QA3，S1730S-S24T4X-QA3， S1730S-S48P4S-A3，S1730S-S48T4S-A3， S1730S-S48T4X-A3，S1730S-S8P4X-QA3， S1730S-S8T4X-QA3 |
| S6730E-H-V2 | S6730E-H6FX4Y2CZ-V2 |
| S5735E-S-V2 | S5735E-S24HJ4XE-V2，S5735E-S24HS4XE-V2， S5735E-S24J4XE-V2，S5735E-S48HJ4XE-V2， S5735E-S48HS4XE-V2，S5735E-S48J4XE-V2 |
| S5735-S-V2 | S5735-S24HJ4XE-V2，S5735-S24HS4XE-V2， S5735-S24J4XE-V2，S5735-S24P4XE-V2，S5735- S24P4XEZ-V2，S5735-S24P8J4XEZ-V2，S5735- S24PN4XE-V2，S5735-S24ST4XE-V2，S5735- S24T4XE-C-V2，S5735-S24T4XE-V2，S5735- S24T4XEZ-V2，S5735-S24T8J4XE-XA-V2，S5735- S24T8J4XEZ-V2，S5735-S24U4XE-V2，S5735- S48HJ4XE-V2，S5735-S48HS4XE-V2，S5735- S48J4XE-V2，S5735-S48P4XE-V2，S5735- S48P4XEZ-V2，S5735-S48PN4XE-V2，S5735- S48S4XE-V2，S5735-S48T4XE-C-V2，S5735- S48T4XE-V2，S5735-S48T4XE-XA-V2，S5735- S48T4XEZ-V2，S5735-S48U4XE-V2 |
| S5735S-S3 | S5735S-S24P4X-A3，S5735S-S48P4X-A3 |
| S6750E-S | S6750E-S16X10Y2CZ，S6750E-S24T16X8Y2CZ |
| S5735I-L-V2 | S5735I-L10T4X-A-V2，S5735I-L8P4X-A-V2 |
| S6730-H-V2 | S6730-H24X6C-V2，S6730-H28X6CZ-V2，S6730- H48X6C-TV2，S6730-H48X6C-V2，S6730- H48X6CZ-V2，S6730-H48Y6C-TV2，S6730- H48Y6C-V2，S6730-H6FX4Y2CZ-V2 |
| S5735I-H-V2 | S5735I-H24U8S4XE-QA-V2，S5735I-H8T2XN- V2，S5735I-H8T4S2XN-V2，S5735I-H8U2XN-V2 |

| 系列 | 支持产品 |
|---|---|
| S6750-S | S6750-S16X10Y2CZ，S6750-S16X8YZ，S6750- S24T16X8Y2CZ |
| S5735S-L3 | S5735S-L24P4S-A3，S5735S-L24P4XE-A3， S5735S-L24PN4XE-A3，S5735S-L24ST4X-A3， S5735S-L24T4S-QA3，S5735S-L24T4X-QA3， S5735S-L24T8J4XE-A3，S5735S-L48P4S-A3， S5735S-L48P4XE-A3，S5735S-L48PN4XE-A3， S5735S-L48S4X-A3，S5735S-L48T4S-A3，S5735S- L48T4XE-A3，S5735S-L8P4X-QA3，S5735S- L8T4X-QA3 |
| S5755-H | S5755-H24HB2Y2CZ，S5755-H24N4Y-A，S5755- H24P4Y2CZ，S5755-H24T4Y2CZ，S5755- H24U4Y2CZ，S5755-H24UM4Y2CZ，S5755- H24UN4Y2CZ，S5755-H24UTM4X4Y2C，S5755- H48N4Y-A，S5755-H48P4Y2CZ，S5755- H48T4Y2CZ，S5755-H48T4Y2CZ-B，S5755- H48U4Y2CZ，S5755-H48UM4Y2CZ，S5755- H48UN4Y2CZ，S5755-H48UTM4X4Y2C |
| S5735R-S-V2 | S5735R-S24P4X-V2，S5735R-S24T8J4X-XA-V2， S5735R-S48P4X-V2，S5735R-S48T4X-XA-V2 |
| S6780-H | S6780-H4Z |
| S5735E-L-V2 | S5735E-L16LP2UM2X-QA-V2，S5735E-L16LP2X- QA-V2，S5735E-L24HJ4XE-A-V2，S5735E- L24P4S-A-V2，S5735E-L24P4XE-A-V2，S5735E- L24ST4XE-A-V2，S5735E-L24T4XE-A-V2， S5735E-L48LP4S-A-V2，S5735E-L48LP4XE-A-V2， S5735E-L48S4XE-A-V2，S5735E-L48T4XE-A-V2， S5735E-L8P4X-QA-V2，S5735E-L8T4X-QA-V2 |
| S5755-S | S5755-S24N8YZ，S5755-S24P8J8YZ，S5755- S24P8Y，S5755-S24T8J8YZ，S5755-S24T8Y， S5755-S24U8J8YZ，S5755-S24U8Y，S5755- S24UN8YZ，S5755-S48N8YZ，S5755-S48P8Y， S5755-S48P8YZ，S5755-S48T8Y，S5755- S48T8YZ，S5755-S48T8YZ-B，S5755-S48U8Y， S5755-S48U8YZ，S5755-S48UN8YZ |
| S5735R-L-V2 | S5735R-L16LP2S-QA-V2，S5735R-L16LP2UM2X- QA-V2，S5735R-L16LP2X-QA-V2，S5735R- L16T4S-A-V2，S5735R-L16T4X-QA-V2，S5735R- L24P4S-A-V2，S5735R-L24P4X-A-V2，S5735R- L24T4S-A-V2，S5735R-L24T4X-QA-V2，S5735R- L48LP4S-A-V2，S5735R-L48LP4X-A-V2，S5735R- L48P4X-A-V2，S5735R-L48T4S-A-V2，S5735R- L48T4X-A-V2，S5735R-L8P4S-A-V2，S5735R- L8P4X-QA-V2，S5735R-L8T4S-A-V2，S5735R- L8T4X-QA-V2 |

| 系列 | 支持产品 |
|---|---|
| S5735-L-V2 | S5735-L10T4X-A-V2，S5735-L14P2S-QA-V2， S5735-L16LP2UM2X-QA-V2，S5735-L16LP2X-QA- V2，S5735-L16P2UM2X-QA-V2，S5735-L16T4S- A-V2，S5735-L16T4X-QA-V2，S5735-L24HJ4XE- A-V2，S5735-L24J4X-A-V2，S5735-L24J4X-D- V2，S5735-L24LU8S4XE-QA-V2，S5735-L24P4S- A-V2，S5735-L24P4XE-A-V2，S5735-L24PN4XE- A-V2，S5735-L24ST4XE-A-V2，S5735-L24T4S-A- V2，S5735-L24T4X-QA-V2，S5735-L24T4XE-A- V2，S5735-L24T4XE-D-V2，S5735-L24T8J4XE-A- V2，S5735-L48J4X-A-V2，S5735-L48J4X-D-V2， S5735-L48LP4S-A-V2，S5735-L48LP4XE-A-V2， S5735-L48LPN4XE-A-V2，S5735-L48P4XE-A-V2， S5735-L48PN4XE-A-V2，S5735-L48S4X-A-V2， S5735-L48S4XE-A-V2，S5735-L48T4S-A-V2， S5735-L48T4XE-A-V2，S5735-L48T4XE-D-V2， S5735-L8P2T4X-A-V2，S5735-L8P4S-A-V2， S5735-L8P4X-QA-V2，S5735-L8T4S-A-V2， S5735-L8T4X-QA-V2 |
| S6730-S-V2 | S6730-S24X6Q-V2，S6730-S48X6Q-V2 |
| S5735I-S-V2 | S5735I-S16T2S4XN-V2，S5735I-S16T8S4XE-QD- V2，S5735I-S24T4XE-V2，S5735I-S24T8S4XE-QA- V2，S5735I-S24U4XE-V2，S5735I-S48T4XE-V2， S5735I-S8T4SN-V2，S5735I-S8T4XN-V2，S5735I- S8T8P2S4XN-V2，S5735I-S8U2XN-V2，S5735I- S8U4XN-V2 |
| S5732-H-V2 | S5732-H24S4X6QZ-TV2，S5732-H24S4X6QZ- V2，S5732-H24UM4Y2CZ-KV2，S5732- H24UM4Y2CZ-V2，S5732-H44S4X6QZ-V2， S5732-H48UM4Y2CZ-KV2，S5732-H48UM4Y2CZ- TV2，S5732-H48UM4Y2CZ-V2 |

查询工具如需了解硬件规格、产品部件的配套关系，请点击硬件中心进行查询；如需了解关键规格、全量软件规格，请点击规格查询进行查询。
特性限制表 7-15 本特性的使用限制特性限制快速生成树是在整个交换网络应用单生成树实例，不能解决由于网络规模增大带来的性能降低问题，网络直径不要超过7。

#### 7.5.1 了解STP/RSTP/MSTP

| 特性限制 |
|---|
| 环路保护功能和根保护功能不能同时配置在同一端口。 |
| 在配置MSTP多实例的时候，随着实例个数的增加，协议报文的长度会变长；MSTP 在每个进程中独立发送MSTP报文，配置MSTP多进程的时候，发送的协议报文会增多。在多进程、多实例的情况下，STP默认CPCAR值不能满足协议需要，用户要手动放大STP的CPCAR值。否则，协议报文可能会被CAR掉。 |
| 使能设备的BPDU保护功能只对手工配置的边缘端口生效。 |
| V8：port id分配在资源侧写入DB，若DB重启，可保证重启前后接口与port id的映射关系不变。 Yunshan Lite：port id分配在组件侧，重启后接口与port id的映射关系会丢失，只能重新分配，无法保证重启前后映射关系不变。 |

### 7.4 STP/RSTP/MSTP缺省配置

生成树协议的主要缺省配置如表7-16所示。
表 7-16 生成树协议缺省配置

| 参数 | 缺省配置 |
|---|---|
| 生成树协议工作模式 | MSTP模式 |
| 生成树协议功能 | 使能 |
| 设备的优先级 | 32768 |
| 端口的优先级 | 128 |
| 路径开销的计算方法 | Dot1t，即IEEE 802.1t标准 |
| Forward Delay Time | 1500厘秒（15秒） |
| Hello Time | 200厘秒（2秒） |
| Max Age Time | 2000厘秒（20秒） |

### 7.5 配置STP/RSTP/MSTP

了解
7.5.1 STP/RSTP/MSTP STP/RSTP/MSTP是IEEE先后提出的三种局域网破环协议，主要用于破除网络环路，也可以实现冗余链路备份。运行STP/RSTP/MSTP的设备之间通过交互BPDU报文实现生成树拓扑计算。这三种破环协议的对比如表 7-17 所示： STP 和 RSTP 是单生成树协议，而MSTP是多生成树协议；在收敛速度方面STP收敛速度最慢。

表 7-17 生成树协议的比较

| 生成树协议 | 收敛速度 | 流量转发 | 配置复杂度 |
|---|---|---|---|
| STP（基于 IEEE 802.1d 标准） | 最慢 | 所有VLAN共享一棵生成树，所有VLAN 的流量按照同样的路径转发。 | 低 |
| RSTP（基于 IEEE 802.1w 标准） | RSTP和MSTP比 STP收敛速度快，但RSTP和 MSTP之间没有快慢之分。 | 所有VLAN共享一棵生成树，所有VLAN 的流量按照同样的路径转发。 | 低 |
| MSTP（基于 IEEE 802.1s 标准） |  | 通过实例与VLAN的映射，可以实现多棵生成树在VLAN间负载分担，不同VLAN 的流量按照不同的路径转发。每棵生成树之间相互独立。 | 高 |

RSTP 出现背景随着局域网规模的不断增长，STP拓扑收敛速度慢的问题逐渐凸显。STP协议的收敛速度慢主要体现在：
● STP算法是被动的算法，依赖定时器等待的方式判断拓扑变化。
● STP算法要求在稳定的拓扑中，由根桥主动发出配置BPDU报文，非根桥设备只能被动中继配置BPDU报文将其并传遍整个STP网络。
此外，STP协议也没有细致区分端口状态和端口角色。例如，从用户的角度来说，Listening、Learning和Blocking状态都不转发用户流量，三种状态没有区别；从使用和配置的角度来说，端口之间最本质的区别在于端口角色，而不在于端口状态。而网络协议的优劣往往取决于协议是否对各种情况加以细致区分。
因此，针对STP的以上不足，RSTP所做的改进有：
● 新增了Alternate端口、Backup端口、边缘端口这几种端口角色，并精简了端口状态，详细介绍请参见7.2.1 设备角色、端口角色和端口状态。而且在配置BPDU的格式中，充分利用Flag字段，明确了端口角色。
● 配置BPDU的处理方式发生了变化。
– 拓扑稳定后，对于非根桥设备，无论是否收到根桥传来的配置 BPDU 报文，都会自主地按照Hello Timer规定的时间间隔发送配置BPDU。
– 如果一个端口在超时时间（超时时间＝Hello Time × 3 × Timer Factor）内没有收到上游设备发送过来的配置BPDU，那么该设备认为与此邻居之间的协商失败。而不像STP那样需要先等待一个Max Age。
– 当一个端口收到上游的指定桥发来的RST BPDU报文时，该端口会将其与自身存储的RST BPDU进行比较。如果该端口存储的RST BPDU的优先级较高，则直接丢弃收到的RST BPDU，并立即向上游设备回应自身存储的RST BPDU。
当上游设备收到回应的RST BPDU后，会根据其中相应的字段立即更新自己存储的RST BPDU。由此，RSTP处理次等BPDU报文不再依赖于任何定时器通过超时解决拓扑收敛，从而加快了拓扑收敛。
● 引入快速收敛机制，包括Proposal/Agreement机制、根端口快速切换机制、新增边缘端口。

● 引入多种保护功能，包括BPDU保护、根保护、环路保护、TC保护。
MSTP 出现背景
对于STP/RSTP，局域网内所有的VLAN共享一棵生成树，因此无法在VLAN间实现数据
流量的负载均衡，链路被阻塞后将不承载任何流量，造成带宽浪费，还有可能造成部
分VLAN的报文无法转发。
如图7-17所示网络中，在局域网内应用STP或RSTP，DeviceD为根交换设备，生成树结
构在图中用虚线表示，DeviceA和DeviceF之间、DeviceB和DeviceE之间的链路被阻
塞。
HostB和HostD同属于VLAN2，由于DeviceB和DeviceE之间的链路被阻塞，DeviceC和
DeviceD之间的链路又不允许VLAN2的报文通过，因此HostB和HostD之间无法互通。
图 7-17 STP/RSTP 的示意图
为了解决上述问题，MSTP把一个交换网络划分成多个域，每个域内形成多棵生成树，
生成树之间彼此独立。每棵生成树叫做一个多生成树实例 MSTI （ Multiple Spanning
Tree Instance），每个域叫做一个MST域（MST Region：Multiple Spanning Tree
Region）。
所谓实例就是多个VLAN的一个集合。通过将多个VLAN捆绑到一个实例，可以节省通
信开销和资源占用率。MSTP各个实例拓扑的计算相互独立，在这些实例上可以实现负
载均衡。可以把多个相同拓扑结构的VLAN映射到一个实例里，这些VLAN在端口上的
转发状态取决于端口在对应MSTP实例的状态。
如图7-18所示，MSTP通过设置VLAN映射表（即VLAN和MSTI的对应关系表），把
VLAN和MSTI联系起来。每个VLAN只能对应一个MSTI，即同一VLAN的数据只能在一
个 MSTI 中传输，而一个 MSTI 可能对应多个 VLAN 。经计算，最终生成两棵生成树：
● MSTI1以DeviceF为根交换设备，转发VLAN2的报文。
● MSTI2以DeviceD为根交换设备，转发VLAN3的报文。

这样属于同一VLAN的主机可以互通，同时不同VLAN的报文沿不同的路径转发，实现了负载分担。
图 7-18 MST 域内的多棵生成树示意图

#### 7.5.2 配置生成树协议工作模式

背景信息设备支持STP、RSTP和MSTP三种生成树协议工作模式。在只运行STP的环形网络中，设备可选择STP模式；在只运行RSTP的环形网络中，设备可选择RSTP模式。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置设备的生成树协议工作模式。
stp mode { stp | rstp | mstp }缺省情况下，设备的生成树协议工作模式为MSTP模式。
MSTP模式兼容STP和RSTP模式。
----结束

#### 7.5.3 配置MST域（MSTP）

背景信息生成树协议工作模式配置为MSTP时，需要在设备上配置MST域。

MST域即多生成树域，是由网络中的多台设备以及它们之间的网段所构成。这些设备启动MSTP后，具有相同域名、相同VLAN到生成树映射配置和相同MSTP修订级别配置，并且物理上直接相连。一个网络中可以存在多个MST域。
当两台设备的以下配置相同时，这两台设备就属于同一个MST域。
● MST域的域名。
● VLAN映射表：多生成树实例和VLAN的映射关系。
● MST域的修订级别。
在MST BPDU中，包含一个记录该BPDU剩余生存跳数的字段。
● 根桥发送的BPDU的剩余生存跳数为MST域的最大跳数。
非根桥发送的BPDU的剩余生存跳数为MST域的最大跳数减去本设备距根桥的跳
●数。
如果设备收到的BPDU中携带的剩余生存跳数为0，则设备将该BPDU丢弃。因此，MST域内生成树的最大跳数会决定生成树的网络规模大小。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入MST域视图。
stp region-configuration步骤3 配置MST域的域名。
region-name name步骤4 （可选）配置MST域的修订级别。
revision-level level缺省情况下，MST域的MSTP修订级别为0。
当设备所在域的MSTP修订级别不为0，则需要执行本操作。
步骤5 配置VLAN映射表。根据需要选择执行如下一种方法。
方法一和方法二是在MST域视图下配置，方法三是在VLAN-Instance视图下配置。
VLAN-Instance视图下配置和MST域视图下配置是互斥的，如果已在MST域视图下配置了VLAN映射表，则需要先删除才能在VLAN-Instance视图下配置VLAN映射表。
方法一：在 MST 域视图下手动配置多生成树实例和 VLAN 的映射关系。
instance instance-id vlan { vlan-id1 [ to vlan-id2 ] }&<1-10>方法二：在MST域视图下配置多生成树实例和VLAN按照缺省算法自动分配映射关系。
vlan-mapping modulo modulo方法三：在VLAN-Instance视图下配置VLAN映射表。提交配置前可以在VLAN- Instance视图下执行命令check mapping查看当前配置的实例和VLAN vlan instance的映射关系是否正确。
quit vlan instance instance instance-id vlan { vlan-id [ to vlan-id ] }&<1-10>缺省情况下，所有 VLAN 均映射到生成树实例 0 。
不能将同一个VLAN映射到多个不同的实例上。如果将一个已经和实例建立映射关系的VLAN又映射到另一个实例上，原来的映射关系将被取消。

上述步骤配置完成后，为了保证设备的MST域配置完全正确，建议在MST域视图下使用命令check region-configuration进行校验。
步骤6 返回系统视图。
quit步骤7 （可选）进入MSTP进程视图。
stp process process-id本步骤仅需要在ID非0的MSTP进程中配置系统参数时执行。
步骤8 配置MST域的最大跳数。
stp max-hops hop缺省情况下，MST域的最大跳数为20。
----结束检查配置结果
● 执行命令display stp region-configuration [ digest ]，查看MST域配置信息。
● 执行命令display vlan instance mapping，查看实例和VLAN的映射关系。

#### 7.5.4 （可选）调整影响设备角色、端口角色和端口状态的参数

背景信息设备优先级、端口优先级、端口路径开销与BPDU报文中的消息优先级向量密切相关，通过调整这几个参数可以影响生成树计算结果，即可以影响生成树中设备的角色、端口的角色和端口状态。
根桥是生成树的逻辑中心。生成树协议可以通过计算来自动确定根桥，用户也可以手动指定根桥或备份根桥，或者通过配置设备优先级来影响根桥的选举结果。建议手动配置根桥和备份根桥。
● 在运行生成树协议的网络中，请将性能高、网络层次高的设备配置为根桥，以保证二层网络的稳定性，否则新接入设备可能会触发根桥切换，从而导致业务短暂中断。
● 在一棵生成树中，生效的根桥只有一个；当两台或两台以上的设备被指定为同一棵生成树的根桥时，系统将选择MAC地址最小的设备作为根桥。
● 可以在每棵生成树中指定多个备份根桥。当根桥出现故障或被关机时，备份根桥可以取代根桥成为指定生成树的根桥；但此时若配置了新的根桥，则备份根桥将不会成为根桥。如果配置了多个备份根桥，则MAC地址最小的备份根桥将成为指定生成树的根桥。
● 设备在各生成树中的角色互相独立。MSTP网络中设备在作为一棵生成树的根桥或备份根桥的同时，也可以作为其他生成树的根桥或备份根桥；但在同一棵生成树中，一台设备不能既作为根桥，又作为备份根桥。
端口路径开销是生成树计算的重要依据，会影响根端口的选择。非根桥设备上所有端口中到达根桥路径开销最小的端口就是根端口。MSTP网络中在不同生成树实例中为同一端口配置不同的路径开销值，可以使不同VLAN的流量沿不同的物理链路转发，实现VLAN 的负载分担功能。
端口路径开销值取值范围由路径开销计算方法决定。如果链路的速率值越大，则建议将该端口的路径开销值在指定范围内设置越小；如果链路的速率值越小，则建议将该

端口的路径开销值配置相对较大，以使其在生成树算法中被选举成为阻塞端口，阻塞其所在链路。
IEEE 802.1d-1998标准方法、IEEE 802.1t标准方法和华为计算方法中规定的路径开销如表7-18所示，而各设备制造商采用的路径开销标准各不相同。
表 7-18 路径开销列表

| 端口速率 | 端口模式 | STP路径开销（推荐值） |  |  |
|---|---|---|---|---|
|  |  | IEEE 802.1d-1998 标准方法 | IEEE 802.1t标准方法 | 华为计算方法 |
| 0 | - | 65535 | 200,000,000 | 200,000 |
| 10Mbps | Half-Duplex | 100 | 2,000,000 | 2000 |
|  | Full-Duplex | 99 | 1,999,999 | 1999 |
|  | Aggregated Link 2 Ports | 95 | 1,000,000 | 1800 |
|  | Aggregated Link 3 Ports | 95 | 666,666 | 1600 |
|  | Aggregated Link 4 Ports | 95 | 500,000 | 1400 |
| 100Mbps | Half-Duplex | 19 | 200,000 | 200 |
|  | Full-Duplex | 18 | 199,999 | 199 |
|  | Aggregated Link 2 Ports | 15 | 100,000 | 180 |
|  | Aggregated Link 3 Ports | 15 | 66,666 | 160 |
|  | Aggregated Link 4 Ports | 15 | 50,000 | 140 |
| 1000Mbps | Full-Duplex | 4 | 20,000 | 20 |
|  | Aggregated Link 2 Ports | 3 | 10,000 | 18 |
|  | Aggregated Link 3 Ports | 3 | 6666 | 16 |
|  | Aggregated Link 4 Ports | 3 | 5000 | 14 |
| 2500Mbps | Full-Duplex | 3 | 8000 | 17 |
|  | Aggregated Link 2 Ports | 3 | 4000 | 12 |

| 端口速率 | 端口模式 | STP路径开销（推荐值） |  |  |
|---|---|---|---|---|
|  |  | IEEE 802.1d-1998 标准方法 | IEEE 802.1t标准方法 | 华为计算方法 |
|  | Aggregated Link 3 Ports | 3 | 2666 | 7 |
|  | Aggregated Link 4 Ports | 2 | 2000 | 2 |
| 10Gbps | Full-Duplex | 2 | 2000 | 2 |
|  | Aggregated Link 2 Ports | 1 | 1000 | 1 |
|  | Aggregated Link 3 Ports | 1 | 666 | 1 |
|  | Aggregated Link 4 Ports | 1 | 500 | 1 |
| 40Gbps | Full-Duplex | 1 | 500 | 1 |
|  | Aggregated Link 2 Ports | 1 | 250 | 1 |
|  | Aggregated Link 3 Ports | 1 | 166 | 1 |
|  | Aggregated Link 4 Ports | 1 | 125 | 1 |

端口优先级会影响端口是否被选举为指定端口。如果希望将某端口阻塞从而破除环路，则可将其端口优先级设置比缺省值大，使其在选举过程中成为被阻塞的端口。
除了设备优先级、端口优先级、端口路径开销这几个参数，其他的一些参数也会影响生成树协议的拓扑收敛，如需调整可以参见7.8 配置影响STP/RSTP/MSTP拓扑收敛的参数。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置设备优先级，从而调整设备在生成树协议中的角色。根据需要选择如下任一配置。
生成树协议工作模式为STP或RSTP时，无需指定instance；生成树协议工作模式为MSTP时，如果不指定instance，则配置设备在实例0上为根桥设备、备份根桥设备或配置设备在实例0上的优先级。
● 配置设备为根桥。
stp [ instance instance-id ] root primary

缺省情况下，设备不作为任何生成树的根桥。配置后该设备优先级数值自动为0，并且不能更改设备优先级。
配置设备为备份根桥。
●stp [ instance instance-id ] root secondary缺省情况下，设备不作为任何生成树的备份根桥。配置后该设备优先级数值为4096，并且不能更改设备优先级。
● 配置设备优先级。数值越小，设备的优先级越高，成为根桥的可能性越大；数值越大，设备的优先级越低，成为根桥的可能性越小。
stp [ instance instance-id ] priority priority缺省情况下，设备在生成树中的优先级取值是32768。
如果已经执行命令指定当前设备为根桥设备或备份根桥设备，若需要改变当前设备的优先级，则需要先执行命令undo stp [ instance instance-id ] root去使能根桥设备或者备份根桥设备功能，然后再执行命令stp [ instance instance-id ] priority priority配置新的优先级数值。
步骤3 （可选）配置接口路径开销计算方法。
stp pathcost-standard { dot1d-1998 | dot1t | legacy }缺省情况下，路径开销值的计算方法为 IEEE 802.1t （ dot1t ）标准方法。
同一网络内所有设备的接口路径开销应使用相同的计算方法。
步骤4 配置二层接口的路径开销值。
1. 进入接口视图。
interface interface-type interface-number
2. 配置接口从三层模式切换到二层模式。
portswitch仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。请根据当前接口模式自行选择是否要执行此步骤。
3. 配置当前二层接口的路径开销值。
stp [ instance instance-id ] cost cost
– 配置接口路径开销计算方法为legacy时，参数cost取值范围是1～200000。
– 配置接口路径开销计算方法为dot1d-1998时，参数cost取值范围是1～65535。
– 配置接口路径开销计算方法为dot1t时，参数cost取值范围是1～200000000。
4. 退出接口视图，返回到系统视图。
quit步骤5 配置当前进程下所有Eth-Trunk接口的路径开销值。
stp eth-trunk cost cost
● 配置接口路径开销计算方法为legacy时，参数cost取值范围是1～200000。
● 配置接口路径开销计算方法为dot1d-1998时，参数cost取值范围是1～65535。
● 配置接口路径开销计算方法为dot1t时，参数cost取值范围是1～200000000。
说明如果端口下配置了stp cost命令，则以端口下配置的cost生效。
步骤6 配置接口优先级。

stp [ instance instance-id ] port priority priority缺省情况下，设备上接口的优先级取值是128。
步骤7 （可选）配置BRIDGE-MIB中dot1dStpRootPort和dot1dStpPort节点查询结果为物理端口的端口号，从而在网管上更方便识别物理接口。
stp bridge-mib port use-port-number缺省情况下，BRIDGE-MIB中dot1dStpRootPort和dot1dStpPort节点查询结果为STP接口ID。
----结束

#### 7.5.5 启用STP/RSTP/MSTP

背景信息在环形网络中一旦启用STP/RSTP/MSTP，设备便立即开始进行生成树计算。设备的优先级、端口优先级等参数会影响到生成树的计算，在计算过程中这些参数的变动可能会导致网络振荡。为了保证生成树计算过程快速而且稳定，必须在配置好设备的优先级、端口优先级等参数后再启用 STP/RSTP/MSTP 。
说明
● 在运行生成树协议的网络中，请将最核心的设备配置为根桥，以保证二层网络的稳定性，否则新接入设备可能会触发生成树协议根切换，从而导致业务短暂中断。
● 对于开启了生成树协议的设备，每当有终端设备接入时会导致生成树重新计算收敛，这会导致终端设备获取IP地址的时间比较长。可以将设备上连接终端的端口配置成边缘端口或在该端口下去使能生成树协议。
操作步骤步骤1 进入系统视图。
system-view步骤2 使能STP/RSTP/MSTP功能。
stp enable缺省情况下，设备上的STP/RSTP/MSTP功能处于开启状态。
----结束

#### 7.5.6 检查配置结果

操作步骤
● 执行命令display stp [ instance instance-id ] [ interface interface-type interface-number | slot slot-id ] [ brief ]，查看生成树的状态信息与统计信息。
● 执行命令display stp [ instance instance-id ] abnormal-interface，查看运行生成树协议的异常端口信息。
● 执行命令 display stp active ，查看状态为 Up 的所有接口的生成树状态详细信息和统计信息。
● 执行命令display stp bridge { local | root }，查看本桥或根桥的生成树状态详细信息。

● 执行命令display stp global，查看生成树协议的全局概要信息。
● 执行命令display stp vlan vlan-id [ blocked-interface ]，查看加入指定VLAN的
端口的生成树状态。
----结束

### 7.6 配置MSTP多进程

#### 7.6.1 了解MSTP多进程

MSTP多进程是基于MSTP协议的增强性技术。此技术可将设备上的端口绑定到不同的进程中，并以进程为单位进行MSTP协议计算，不在同一个进程内的端口不参与此进程中的MSTP协议计算，从而实现各个进程内的生成树计算相互独立，互不影响。
产生背景如图7-19所示：
● UPE为汇聚层设备，运行MSTP。
● UPE1和UPE2之间为二层链路。
● UPE1和UPE2下接有多个环，不同环通过不同端口接入。
● 环上的设备为接入层设备，只运行STP/RSTP，同时UPE1和UPE2属于不同的运营商，不希望计算在一个生成树中，拓扑变化不能影响对方。
UPE1和UPE2同时连接多个接入环，各个环之间互相独立，不需要互通，这样在启动生成树协议时就不能将所有设备构成的环路计算成一个大生成树，这就需要在各个设备构成的环上启用独立的生成树协议进行计算，且互不影响。
MSTP支持生成树多实例，但是MSTP支持的多实例必须存在同一个域中，且同一个域中所有设备配置也必须一致。如果不同的设备属于不同的域，那么MSTP在进行生成树计算时，只按一个实例进行计算。所以，当网络内的设备属于不同域时，整个网络只能在一个实例中进行生成树计算，网络内任何一台设备状态发生变化，都将影响整个网络。图7-19所示组网中与UPE相连的接入层设备只支持STP/RSTP协议，不支持MSTP协议。根据MSTP协议标准，UPE收到来自接入层设备的STP/RSTP报文后，则认为彼此不属于同一个域。那么UPE和接入层设备构成的环只会计算出一个生成树，不能实现各个接入环的相互独立。
为了解决上述问题，引入了MSTP多进程。此技术可将设备上的端口绑定到不同的进程中，并以进程为单位进行MSTP计算，不在同一个进程内的端口不参与此进程中的MSTP计算，从而实现各个进程内的生成树计算相互独立，互不影响。可将图7-19所示组网划分为多个MSTP进程，每个进程对应一个设备构成的环，每个MSTP进程功能相同，支持生成树多实例，各进程进行MSTP计算时相互独立，不会影响到其他进程中的MSTP计算。
说明MSTP多进程机制并不只限于MSTP协议，RSTP和STP协议同样适用。

图 7-19 MSTP 和 STP/RSTP 混合应用场景图目的通过部署MSTP多进程可以实现：
● 极大地提升了在不同组网条件下生成树协议的可部署性。
为了保证运行不同类型生成树协议的网络可靠运行，可将不同类型的生成树协议划分到不同的进程中，不同进程对应的网络进行独立的生成树协议计算。
● 增强了组网的可靠性，对于大量的二层接入设备，可减少单台设备故障对整个网络的冲击。
通过进程隔离不同的拓扑计算，即某台设备故障只影响其所在的进程对应的拓扑，不会影响其他进程拓扑计算。
● 网络扩容时，可减少网络管理者维护量，从而提升了用户运维管理的方便性。
当网络扩容时，只需要划分新的进程与原有网络对接，不需要调整原有网络的MSTP进程配置。如果是某个进程中进行了设备扩容，此时也只需要针对扩容的进程进行修改，而不需要调整其他进程中的配置。
● 实现二层端口分割管理每个MSTP进程可以管理设备上的部分端口，即设备的二层端口资源被多个MSTP进程分割管理，每个MSTP进程上均可运行标准的MSTP。
MSTP 多进程原理共享链路的状态如图7-19所示，UPE1和UPE2之间的链路是共享链路：共享链路上的端口需要参与多个接入环/多个MSTP进程的计算，UPE1和UPE2之间的MSTP报文需要能区分是来自哪个进程的MSTP报文。
此外，共享链路上的同一个端口同时参与多个MSTP进程的计算，多个MSTP进程中都会计算出端口状态，这样端口就可能同时存在多个状态，从而无法决定采用哪个生成树的状态。

对于上述情况，共享链路上的端口虽然参与多个MSTP进程的状态计算，但是只具有MSTP进程0的状态，从而不会影响其他MSTP进程。
说明设备启动后，设备默认存在ID为0的MSTP进程，系统视图和接口视图中的MSTP相关配置都属于此进程。
可靠性如图7-20所示，当接入层设备产生拓扑变化后，通过MSTP多进程的特性，UPE可以把TC报文洪泛到环上所有设备，同时可以保证一个接入环的拓扑变化消息不会洪泛到其他接入环上，UPE1和UPE2及时刷新和本生成树相关端口的MAC和ARP表项，并且不影响其他的设备。
图 7-20 MSTP 多进程拓扑变化示意图共享链路故障问题及解决方法如图7-21所示，如果UPE1和UPE2之间的共享链路故障，可能导致多个交换设备接入环路都会打开阻塞端口。假设UPE1配置为最高优先级，UPE2配置为次高优先级，接入层设备采用默认优先级或配置为更低优先级。当UPE1和UPE2之间的共享链路发生故障后，接入层设备上的（根端口替换端口）阻塞端口因不再收到高优先级BPDU报文而重新进行生成树计算，新计算的结果是成为指定端口，此时就会产生永久环路。

图 7-21 接入环路之间形成环路示意图为了解决共享链路故障时多个接入环之间形成环路的问题，可以通过如下两种方式解决：
● UPE1和UPE2之间的共享链路使用Eth-Trunk，提高链路可靠性，如图7-22所示。
图 7-22 共享链路使用 Eth-Trunk 示意图

● UPE1和UPE2之间部署根保护。
如图7-23所示，假设UPE1配置为最高优先级，UPE2配置为次高优先级，接入环
上的设备采用默认优先级或配置为更低的优先级，并在UPE1和UPE2上配置根保
护。
以UPE1、DeviceA、DeviceB和UPE2组成的接入环为例，假设阻塞端口为DeviceB
的BP1，当UPE1和UPE2之间的共享链路发生故障后，BP1端口因不再收到高优先
级BPDU报文而重新进行生成树计算，新计算的结果是该端口成为指定端口，同时
和下游设备进行P/A协商。
当与UPE2直连的DeviceB发送的更高优先级的BPDU报文到达UPE2的启动了根保
护的端口后，该端口将被阻塞，因为后续会持续收到报文，所以该端口将一直处
于阻塞状态。从而保证不会出现环路。
图 7-23 MSTP 多进程部署跟保护示意图

#### 7.6.2 创建MSTP进程

背景信息进程的ID是识别MSTP多进程的唯一标识。MSTP设备将端口绑定在进程中，设备将以进程为单位进行MSTP协议计算，不在此进程内的端口将不参与此进程的协议计算。
请在与接入环相连接的设备上进行以下配置。
说明正常启动后，设备默认存在ID为0的MSTP进程，系统视图和接口视图中的MSTP相关配置都属于此进程，此进程的默认工作模式为MSTP。
操作步骤步骤1 进入系统视图。
system-view

步骤2 创建并进入指定ID的MSTP进程视图。
stp process process-id步骤3 配置设备的生成树协议工作模式为MSTP。
stp mode mstp步骤4 配置MSTP进程的TC通告功能。MSTP进程在收到TC报文后，能够及时通告给MSTP进程0中的实例，使其及时刷新MAC表项和ARP表项，从而保证用户业务不中断。
stp tc-notify process 0
----结束

#### 7.6.3 配置接口加入MSTP进程

背景信息通过将接口加入MSTP进程中，使接口参与MSTP进程计算：
● 使能MSTP功能的设备与接入环相连的链路叫做接入链路。
● 多个接入环共用的链路叫做共享链路。共享链路上的接口需要参与多个接入环和多个 MSTP 进程的计算。
操作步骤
● 配置接口加入MSTP进程－接入链路：
a. 进入系统视图。
system-view
b. 进入接口视图。此命令中指定的接口必须是设备与接入环相连接的二层接口。
interface interface-type interface-number
c. 配置接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
d. 配置接口加入指定ID的MSTP进程中。
stp binding process process-id说明
● 如果加入MSTP进程的接口上存在子接口，并且子接口上配置了其他业务，例如VPLS业务，此时可以在主接口上使用命令stp vpls-subinterface enable，当主接口在收到TC报文后，能够通告其子接口及时刷新MAC表项和ARP表项，从而保证用户业务不中断。
● 一个接入链路所在接口只能加入一个MSTP进程，若多次执行本命令配置当前端口加入不同ID的MSTP进程，以最后一次配置为准。
● 配置接口加入MSTP进程－共享链路：
a. 进入系统视图。
system-view
b. 进入接口视图。此命令中指定的接口不是设备与接入环相连接的接口，而是配置了MSTP多进程的设备之间的共享链路上的接口。

interface interface-type interface-number
c. 配置接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
d. 配置共享链路上的接口参与多个MSTP进程的计算。
stp binding process process-id1 [ to process-id2 ] link-share说明对于存在共享链路的进程，必须在进程视图下使能stp enable。对于共享链路上的接口，接口下必须使能stp enable。
----结束

#### 7.6.4 （可选）调整影响设备角色、端口角色和端口状态的参数

背景信息设备优先级、端口优先级、端口路径开销与BPDU报文中的消息优先级向量密切相关，通过调整这几个参数可以影响生成树计算结果，即可以影响生成树中设备的角色、端口的角色和端口状态。
根桥是生成树的逻辑中心。生成树协议可以通过计算来自动确定根桥，用户也可以手动指定根桥或备份根桥，或者通过配置设备优先级来影响根桥的选举结果。建议手动配置根桥和备份根桥。
● 在运行生成树协议的网络中，请将性能高、网络层次高的设备配置为根桥，以保证二层网络的稳定性，否则新接入设备可能会触发根桥切换，从而导致业务短暂中断。
● 在一棵生成树中，生效的根桥只有一个；当两台或两台以上的设备被指定为同一棵生成树的根桥时，系统将选择MAC地址最小的设备作为根桥。
● 可以在每棵生成树中指定多个备份根桥。当根桥出现故障或被关机时，备份根桥可以取代根桥成为指定生成树的根桥；但此时若配置了新的根桥，则备份根桥将不会成为根桥。如果配置了多个备份根桥，则MAC地址最小的备份根桥将成为指定生成树的根桥。
● 设备在各生成树中的角色互相独立。MSTP网络中设备在作为一棵生成树的根桥或备份根桥的同时，也可以作为其他生成树的根桥或备份根桥；但在同一棵生成树中，一台设备不能既作为根桥，又作为备份根桥。
端口路径开销是生成树计算的重要依据，会影响根端口的选择。非根桥设备上所有端口中到达根桥路径开销最小的端口就是根端口。MSTP网络中在不同生成树实例中为同一端口配置不同的路径开销值，可以使不同VLAN的流量沿不同的物理链路转发，实现VLAN的负载分担功能。
端口路径开销值取值范围由路径开销计算方法决定。如果链路的速率值越大，则建议将该端口的路径开销值在指定范围内设置越小；如果链路的速率值越小，则建议将该端口的路径开销值配置相对较大，以使其在生成树算法中被选举成为阻塞端口，阻塞其所在链路。
IEEE 802.1d-1998标准方法、IEEE 802.1t标准方法和华为计算方法中规定的路径开销如表7-19所示，而各设备制造商采用的路径开销标准各不相同。

表 7-19 路径开销列表

| 端口速率 | 端口模式 | STP路径开销（推荐值） |  |  |
|---|---|---|---|---|
|  |  | IEEE 802.1d-1998 标准方法 | IEEE 802.1t标准方法 | 华为计算方法 |
| 0 | - | 65535 | 200,000,000 | 200,000 |
| 10Mbps | Half-Duplex | 100 | 2,000,000 | 2000 |
|  | Full-Duplex | 99 | 1,999,999 | 1999 |
|  | Aggregated Link 2 Ports | 95 | 1,000,000 | 1800 |
|  | Aggregated Link 3 Ports | 95 | 666,666 | 1600 |
|  | Aggregated Link 4 Ports | 95 | 500,000 | 1400 |
| 100Mbps | Half-Duplex | 19 | 200,000 | 200 |
|  | Full-Duplex | 18 | 199,999 | 199 |
|  | Aggregated Link 2 Ports | 15 | 100,000 | 180 |
|  | Aggregated Link 3 Ports | 15 | 66,666 | 160 |
|  | Aggregated Link 4 Ports | 15 | 50,000 | 140 |
| 1000Mbps | Full-Duplex | 4 | 20,000 | 20 |
|  | Aggregated Link 2 Ports | 3 | 10,000 | 18 |
|  | Aggregated Link 3 Ports | 3 | 6666 | 16 |
|  | Aggregated Link 4 Ports | 3 | 5000 | 14 |
| 2500Mbps | Full-Duplex | 3 | 8000 | 17 |
|  | Aggregated Link 2 Ports | 3 | 4000 | 12 |
|  | Aggregated Link 3 Ports | 3 | 2666 | 7 |
|  | Aggregated Link 4 Ports | 2 | 2000 | 2 |
| 10Gbps | Full-Duplex | 2 | 2000 | 2 |

| 端口速率 | 端口模式 | STP路径开销（推荐值） |  |  |
|---|---|---|---|---|
|  |  | IEEE 802.1d-1998 标准方法 | IEEE 802.1t标准方法 | 华为计算方法 |
|  | Aggregated Link 2 Ports | 1 | 1000 | 1 |
|  | Aggregated Link 3 Ports | 1 | 666 | 1 |
|  | Aggregated Link 4 Ports | 1 | 500 | 1 |
| 40Gbps | Full-Duplex | 1 | 500 | 1 |
|  | Aggregated Link 2 Ports | 1 | 250 | 1 |
|  | Aggregated Link 3 Ports | 1 | 166 | 1 |
|  | Aggregated Link 4 Ports | 1 | 125 | 1 |

端口优先级会影响端口是否被选举为指定端口。如果希望将某端口阻塞从而破除环路，则可将其端口优先级设置比缺省值大，使其在选举过程中成为被阻塞的端口。
除了设备优先级、端口优先级、端口路径开销这几个参数，其他的一些参数也会影响生成树协议的拓扑收敛，如需调整可以参见7.8 配置影响STP/RSTP/MSTP拓扑收敛的参数。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入MSTP进程视图。
stp process process-id步骤 3 配置设备优先级，从而调整设备在生成树协议中的角色。根据需要选择如下任一配置。
生成树协议工作模式为MSTP时，如果不指定instance，则配置设备在实例0上为根桥设备、备份根桥设备或配置设备在实例0上的优先级。
● 配置设备为根桥。
stp [ instance instance-id ] root primary缺省情况下，设备不作为任何生成树的根桥。配置后该设备优先级数值自动为0，并且不能更改设备优先级。
● 配置设备为备份根桥。
stp [ instance instance-id ] root secondary缺省情况下，设备不作为任何生成树的备份根桥。配置后该设备优先级数值为4096，并且不能更改设备优先级。

● 配置设备优先级。数值越小，设备的优先级越高，成为根桥的可能性越大；数值
越大，设备的优先级越低，成为根桥的可能性越小。
stp [ instance instance-id ] priority priority
缺省情况下，设备在生成树中的优先级取值是32768。
如果已经执行命令指定当前设备为根桥设备或备份根桥设备，若需要改变当前设
备的优先级，则需要先执行命令undo stp [ instance instance-id ] root去使能根
桥设备或者备份根桥设备功能，然后再执行命令stp
[ instance instance-id ]
priority priority配置新的优先级数值。
步骤4 返回系统视图。
quit
步骤5 （可选）配置接口路径开销计算方法。
stp pathcost-standard { dot1d-1998 | dot1t | legacy }
缺省情况下，路径开销值的计算方法为IEEE 802.1t（dot1t）标准方法。
同一网络内所有设备的接口路径开销应使用相同的计算方法。
步骤6 进入接口视图。
interface interface-type interface-number
步骤7 配置接口从三层模式切换到二层模式。
portswitch
请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、
S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从
三层模式切换到二层模式。
步骤8 将端口绑定到进程。
stp binding process process-id
步骤9 配置当前二层端口的路径开销值。
stp [ process process-id ] [ instance instance-id ] cost cost
● 配置端口路径开销计算方法为legacy时，参数cost取值范围是1～200000。
● 配置端口路径开销计算方法为dot1d-1998时，参数cost取值范围是1～65535。
● 配置端口路径开销计算方法为dot1t时，参数cost取值范围是1～200000000。
步骤10 配置当前进程下所有Eth-Trunk接口的路径开销值。
stp eth-trunk cost cost
● 配置接口路径开销计算方法为 legacy 时，参数 cost 取值范围是 1 ～ 200000 。
● 配置接口路径开销计算方法为dot1d-1998时，参数cost取值范围是1～65535。
● 配置接口路径开销计算方法为dot1t时，参数cost取值范围是1～200000000。
说明
如果端口下配置了stp cost命令，则以端口下配置的cost生效。
步骤11 配置端口优先级。
stp [ process process-id ] [ instance instance-id ] port priority priority
缺省情况下，设备上端口的优先级取值是 128 。
步骤12 （可选）配置BRIDGE-MIB中dot1dStpRootPort和dot1dStpPort节点查询结果为物理
端口的端口号，从而在网管上更方便识别物理接口。

stp bridge-mib port use-port-number缺省情况下，BRIDGE-MIB中dot1dStpRootPort和dot1dStpPort节点查询结果为STP接口ID。
----结束

#### 7.6.5 启用MSTP

背景信息当设备配置MSTP多进程基本功能后，必须在指定进程视图下使能设备MSTP功能，该进程的MSTP相关配置才能生效。
在环形网络中一旦启用MSTP，MSTP便立即开始进行生成树计算。而且，诸如设备的优先级、端口优先级等参数都会影响到生成树的计算，在计算过程中这些参数的变动可能会导致网络振荡。为了保证生成树计算过程快速而且稳定，必须在对设备及其接口进行必要的基本配置以后才能启用MSTP。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入指定ID的MSTP进程视图。
stp process process-id步骤3 使能STP/RSTP/MSTP功能。
stp enable缺省情况下，设备上的STP/RSTP/MSTP功能处于开启状态。
----结束

#### 7.6.6 检查配置结果

操作步骤
● 执行命令display stp [ process process-id ] [ instance instance-id ] [ interface interface-type interface-number | slot slot-id ] [ brief ]，查看生成树的状态信息与统计信息。
● 执行命令display stp [ process process-id ] [ instance instance-id ] abnormal- interface，查看运行生成树协议的异常端口信息。
执行命令display ，查看状态为Up的所有接口的生成树状态详细信息
● stp active和统计信息。
● 执行命令display stp bridge { local | root }，查看本桥或根桥的生成树状态详细信息。
● 执行命令display stp global ，查看生成树协议的全局概要信息。
● 执行命令 display stp vlan vlan-id [ blocked-interface ] ，查看加入指定 VLAN 的端口的生成树状态。
----结束

### 7.7 启用边缘端口和配置BPDU报文过滤功能（RSTP/MSTP）

背景信息在RSTP/MSTP里面，如果某一个指定端口位于整个网络的边缘，即不再与其他设备连接，而是直接与终端设备直连，这种端口叫做边缘端口。
边缘端口不接收处理配置BPDU报文，不参与RSTP/MSTP运算，可以由Disable直接转到Forwarding状态，且不经历时延，就像在端口上将RSTP/MSTP禁用。
配置为边缘端口后，端口仍然会发送BPDU报文，这可能导致BPDU报文发送到其他网络，引起其他网络产生振荡。因此可以配置边缘端口的BPDU报文过滤功能，使边缘端口不处理、不发送BPDU报文。
说明在全局下配置边缘端口和 BPDU 报文过滤功能后，设备上所有的端口不会主动发送 BPDU 报文，且均不会主动与对端设备直连端口协商，所有端口均处于转发状态。这将可能导致网络成环，引起广播风暴，请用户慎用。
在接口下配置边缘端口和BPDU报文过滤功能后，接口将不处理、不发送BPDU报文。该接口将无法成功与对端设备直连端口协商生成树协议状态，请慎用。
接口使能生成树协议后，会默认启用边缘端口自动探测功能，当端口在（2 × Hello Timer + 1）
秒的时间内收不到BPDU报文，自动将端口设置为边缘端口，否则设置为非边缘端口。如果在接口视图下配置了stp edged-port enable或stp edged-port disable或者在系统视图下配置了stp edged-port default，边缘端口自动探测功能就不生效了。
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
c. 将接口从三层模式切换到二层模式。
portswitch
请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、
S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过
portswitch命令将接口从三层模式切换到二层模式。
d. 配置端口为边缘端口。
stp edged-port enable
缺省情况下，设备的所有端口为非边缘端口。
e. 配置端口为BPDU filter端口。
stp bpdu-filter enable
缺省情况下，设备的所有端口为非BPDU filter端口。
----结束
检查配置结果
执行命令display stp [ process process-id ] [ instance instance-id ] [ interface
interface-type interface-number | slot slot-id ]，根据Port Edged字段查看边缘端口
的配置情况。

### 7.8 配置影响STP/RSTP/MSTP拓扑收敛的参数

#### 7.8.1 配置STP/RSTP/MSTP网络直径

背景信息网络中任意两台终端设备都通过特定路径彼此相连，这些路径由一系列的设备构成。
网络直径就是指网络中任意两台终端设备间的最大设备数。网络直径越大，说明网络的规模越大。例如图7-24所示网络的网络直径为5。
● DeviceC-DeviceA-DeviceD-DeviceB-DeviceE
● DeviceD-DeviceA-DeviceC-DeviceB-DeviceE图 7-24 生成树协议网络直径

若网络直径设置不合理，可能会引起网络收敛速度慢，影响用户的正常通信。根据当前的网络规模设置合适的网络直径，可以帮助加快网络收敛速度。
建议同一环网中的所有设备配置相同的网络直径。
操作步骤步骤1 进入系统视图。
system-view步骤2 （可选）进入MSTP进程视图。
本步骤仅需要在ID非0的MSTP进程中配置系统参数时执行。当在ID为0的进程中配置时，可跳过本步，直接进入下一步。
stp process process-id步骤3 配置网络直径。
stp bridge-diameter diameter缺省情况下，网络直径为7。
说明配置网络直径后，设备会根据网络直径计算出Forward Delay、Hello Time以及Max Age定时器的最优值。建议通过配置网络直径的方式去调整Forward Delay、Hello Time以及Max Age定时器的值。
----结束检查配置结果执行命令display global，根据Bridge-diameter字段查看网络直径的配置情况。
stp

#### 7.8.2 配置STP/RSTP/MSTP定时器

背景信息在生成树的计算过程中，用到了以下三个时间参数：
● Forward Delay：用于确定状态迁移的延迟时间。在运行生成树算法的网络中，当网络拓扑结构发生变化时，因为新的 BPDU 配置消息需要经过一定的时间才能传遍整个网络，所以本应被阻塞的端口可能还来不及被阻塞而之前被阻塞的端口已经不再阻塞，这样就有可能会形成临时的环路。为了避免这种情况引起的临时环路，可以通过Forward Delay定时器设置延时时间，即在这个延时时间内所有端口会临时被阻塞。
● Hello Time：用于检测链路是否存在故障。生成树协议每隔Hello Time时间会发送配置BPDU报文，以确认链路是否存在故障。如果设备根端口在超时时间（超时时间＝Hello Time × 3 × Timer Factor）内没有收到BPDU，则会由于消息超时而重新计算生成树。
● Max Age：用于确定配置BPDU报文是否超时。设备根据Max Age时间来确定端口收到的配置 BPDU 报文是否超时。如果端口收到的配置 BPDU 报文超时，则需要重新计算。
在配置上述三个时间参数时，同一环网中的设备配置时间建议保持一致。

#### 7.8.3 配置STP/RSTP/MSTP超时时间

通常情况下，不建议通过本配置直接调整上述三个时间参数。由于这三个时间参数的取值与网络规模有关，因此建议通过调整网络直径，使生成树协议自动调整这三个时间参数的值。当网络直径取缺省值时，这三个时间参数也分别取其各自的缺省值。
须知根设备的Hello Time、Forward Delay以及Max Age三个时间参数取值之间应该满足如下公式，否则网络会频繁振荡。
● 2 × (Forward Delay －1.0 second) >= Max Age
● Max Age >= 2 × (Hello Time + 1.0 second)
操作步骤步骤1 进入系统视图。
system-view步骤 2 （可选）进入 MSTP 进程视图。
本步骤仅需要在ID非0的MSTP进程中配置系统参数时执行。当在ID为0的进程中配置时，可跳过本步，直接进入下一步。
stp process process-id步骤3 配置Forward Delay时间。
stp timer forward-delay forward-delay缺省情况下，设备的Forward Delay时间是1500厘秒（15秒）。
步骤4 配置Hello Time时间。
stp timer hello hello-time缺省情况下，设备的Hello Time时间是200厘秒（2秒）。
步骤5 配置Max Age时间。
stp timer max-age max-age缺省情况下，设备的Max Age时间是2000厘秒（20秒）。
----结束检查配置结果执行命令display stp [ process process-id ] [ instance instance-id ] [ interface interface-type interface-number | slot slot-id ]，根据Config Times字段查看各定时器的配置情况。
配置 超时时间
7.8.3 STP/RSTP/MSTP背景信息在运行生成树算法的网络中，如果设备在配置的超时时间（超时时间＝Hello Time × 3× Timer Factor）内没有收到上游设备发送的BPDU，就认为上游设备已经出现故障，本设备会重新进行生成树计算。

由于上游设备繁忙，有时设备在较长的时间内收不到上游设备发送的BPDU。在这种情况下一般不应该重新进行生成树计算，因此，在稳定的网络中，可以配置超时时间，以减少网络资源的浪费。
操作步骤步骤1 进入系统视图。
system-view步骤2 （可选）进入MSTP进程视图。
本步骤仅需要在ID非0的MSTP进程中配置系统参数时执行。当在ID为0的进程中配置时，可跳过本步，直接进入下一步。
stp process process-id步骤3 配置未收到上游的BPDU重新开始生成树计算的超时时间。
stp timer-factor factor缺省情况下，设备未收到上游的BPDU就重新开始生成树计算的超时时间是Hello Timer 的 9 倍。
----结束检查配置结果执行命令display stp global，根据Timer-factor字段查看超时时间的配置情况。

#### 7.8.4 配置STP/RSTP/MSTP的收敛方式

背景信息当生成树的拓扑结构发生改变时，和它建立映射关系的VLAN的转发路径也将发生变化。此时，设备的ARP表中与这些VLAN相关的表项也需要更新。根据对ARP表项的处理方式不同，生成树协议的收敛方式分为fast和normal两种：
● fast：ARP表将需要更新的表项直接删除。
● normal：ARP表将需要更新的表项快速老化。设备将ARP表中这些表项的剩余存活时间置为0，对这些表项进行老化处理。如果配置的ARP老化探测次数大于零，则ARP对这些表项进行老化探测。
建议使用缺省的生成树协议收敛方式，即normal收敛方式。若选择fast方式，频繁的ARP表项删除可能会导致设备CPU占用率高达100%，报文处理超时导致网络振荡。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置生成树协议的收敛方式。
stp converge { fast | normal }缺省情况下，生成树协议的收敛方式是normal。
----结束

检查配置结果执行命令display stp [ process process-id ] [ instance instance-id ] [ interface interface-type interface-number | slot slot-id ]，根据STP Converge Mode字段查看生成树协议的收敛方式。

#### 7.8.5 配置TC报文刷新MAC表功能

背景信息部署生成树协议后，任何对拓扑有影响的变化，例如本设备的端口由Down变为Up状态，生成树协议都会发送TC类型BPDU报文通知刷新MAC表项。而有时这种变化导致大量的刷新可能会引入未知的单播或广播问题。为解决此问题，可去使能设备收到TC类型BPDU报文后刷新MAC表功能。
当去使能设备收到TC类型BPDU报文后刷新MAC表功能时，如果MAC表项错误就会造成长时间断流，所以该功能的影响很大，请谨慎部署该命令。
操作步骤步骤1 进入系统视图。
system-view步骤2 （可选）进入MSTP进程视图。
本步骤仅需要在ID非0的MSTP进程中配置系统参数时执行。当在ID为0的进程中配置时，可跳过本步，直接进入下一步。
stp process process-id步骤3 去使能TC类型BPDU报文刷新MAC表功能。
stp flush disable缺省情况下，设备收到TC类型BPDU报文后会刷新MAC表。
----结束检查配置结果在系统视图或 MSTP 进程视图下执行命令 display this ，查看 TC 类型 BPDU 报文刷新MAC表功能的配置情况。

#### 7.8.6 配置TC/TCN报文抑制功能

背景信息某些特殊场景下，当接口收到TC或者TCN报文的时候不希望刷新ARP和MAC表项，可以在接口下配置TC/TCN报文抑制功能。配置TC/TCN报文抑制功能后，接口收到TC或者TCN报文后不会刷新ARP和MAC表项，也不会将TC或者TCN报文扩散到本设备其他端口。
配置TC/TCN报文抑制功能后可能会导致设备不能正确刷新ARP和MAC表项，进而导致拓扑变化之后丢包时间过长，请谨慎部署该功能。

操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤3 配置接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 配置TC/TCN报文抑制功能。
stp tc-restriction enable缺省情况下，TC/TCN报文抑制功能处于去使能状态。
----结束检查配置结果执行命令display stp interface interface-type interface-number，根据TC Restriction字段查看接口下TC/TCN报文抑制功能的使能状态。

#### 7.8.7 配置参与生成树计算的桥MAC

背景信息某些场景下要求两台设备模拟同一个根桥，即要求两台设备发出的BPDU报文中的桥ID是一致的。但是一般情况下，由于每台设备的桥MAC不一样，所以桥ID不一致，此时可以配置两台设备参与生成树协议计算的桥MAC相同。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置设备参与生成树协议计算的桥MAC。
stp bridge-address mac-address缺省情况下，设备参与生成树计算的桥MAC是设备的MAC地址。
----结束检查配置结果执行如下命令，根据CIST Bridge字段查看生成树协议桥MAC地址。
● display stp [ process process-id ] [ instance instance-id ] [ interface interface-type interface-number | slot slot-id ]
● display stp global

#### 7.8.8 配置端口的链路类型（RSTP/MSTP）

背景信息点对点链路可帮助实现快速收敛。与点对点链路相连的两个端口如果为根端口或者指定端口，则端口可以通过传送同步报文（Proposal报文和Agreement报文）快速迁移到转发状态，减少了不必要的转发延迟时间。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤3 配置接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 配置接口的链路类型。
stp point-to-point { auto | force-false | force-true }缺省情况下，端口的链路类型为auto，即由生成树协议自动检测与端口相连的链路是否是点到点链路。
● 如果当前以太网接口工作在全双工模式，则当前接口相连的链路是点到点链路，执行命令stp point-to-point force-true实现快速收敛。
● 如果当前以太网接口工作在半双工模式，可通过执行命令stp point-to-point force-true，强制链路类型为点对点链路，实现快速收敛。
----结束检查配置结果执行命令 display stp [ process process-id ] [ instance instance-id ] [ interface interface-type interface-number | slot slot-id ]，根据Point-to-point字段查看接口链路类型的配置情况。

#### 7.8.9 配置BPDU报文最大发送速率（RSTP/MSTP）

背景信息端口在每个Hello Time时间内BPDU的最大发送数目值越大，表示单位时间内发送的BPDU越多，则占用的系统资源也越多。适当的配置该值可以限制端口发送BPDU的速度，防止在网络拓扑动荡时，生成树协议占用过多的带宽资源。
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
c. 将接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
d. 配置接口每秒发送BPDU的最大数目。
stp transmit-limit packet-number缺省情况下，接口每秒发送BPDU的最大数目由stp transmit-limit (system view)配置的值决定，但若不配置stp transmit-limit (system view)，则接口每秒发送BPDU的最大数目是6。
----结束检查配置结果执行命令display stp [ process process-id ] [ instance instance-id ] [ interface interface-type interface-number | slot slot-id ] ，根据 Transit Limit 字段查看接口下BPDU报文最大发送速率的配置情况。

#### 7.8.10 配置子接口继承主接口的环路状态（STP/RSTP）

前提条件已配置生成树协议工作模式为STP或RSTP。
背景信息当二层子接口所在的网络中出现环路时，可以配置二层子接口继承主接口的环路状态，从而破除二层子接口所在网络的环路。

说明该配置仅S6780-H、S6750-H、S6730-S-V2、S6750-S、S6750E-S、S6730-H-V2、S6730E-H- V2、S5755-H、S5755-S、S5732-H-V2系列支持。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤3 配置接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 配置二层子接口继承主接口的环路状态。
loop-protect l2-subinterface enable
----结束检查配置结果在接口视图下执行命令display this，查看接口下二层子接口继承主接口的环路状态的配置情况。

### 7.9 配置RSTP/MSTP保护功能

#### 7.9.1 了解RSTP/MSTP保护功能

BPDU 保护如图7-25所示，DeviceC上将与PC相连的端口设置为边缘端口。当边缘端口接收到BPDU 报文时， DeviceC 会自动将边缘端口设置为非边缘端口，并重新进行生成树计算。当攻击者发送的BPDU报文中的桥优先级高于现有网络中根桥优先级时会改变当前网络拓扑，可能会导致业务流量中断。这是网络中一种简单的拒绝服务DoS（Denial of Service）攻击方式。
DeviceC上启动了BPDU保护功能后，如果边缘端口收到BPDU报文，边缘端口将被error-down，但保持边缘端口属性不变。

图 7-25 BPDU 保护TC 保护设备在接收到TC（Topology Change）类型BPDU报文后，会执行MAC地址表项和ARP表项的删除操作。如果有人伪造TC类型BPDU报文恶意攻击设备，设备短时间内会收到很多TC类型BPDU报文，频繁的删除操作会给设备造成很大的负担，给网络的稳定带来隐患。
启用TC保护功能后，在单位时间内，设备处理TC类型BPDU报文的次数可配置。如果在单位时间内，设备收到TC类型BPDU报文数量大于配置的阈值，那么设备只会处理阈值指定的次数。对于其他超出阈值的TC类型BPDU报文，定时器到期后设备只对其统一处理一次。这样可以避免频繁的删除MAC地址表项和ARP表项，从而达到保护设备的目的。
根保护由于维护人员的错误配置或网络中的恶意攻击，网络中合法根桥有可能会收到优先级更高的BPDU，使得合法根桥失去根地位，从而引起网络拓扑结构的错误变动。这种拓扑变化可能会导致原来应该通过高速链路的流量被牵引到低速链路上，造成网络拥塞。
如图7-26所示，DeviceA和DeviceB处于网络核心层，两者间链路带宽为100GB/s，DeviceA 为网络中的根桥。 DeviceC 处于接入层， DeviceC 和 DeviceA 、 DeviceC 和DeviceB之间的链路带宽为10GB/s。正常情况下，DeviceB和DeviceC之间的链路被阻塞。当DeviceD新接入DeviceC时，假设DeviceD的桥优先级高于DeviceA，此时DeviceD会被选举为新的根桥，如果DeviceA和DeviceB之间的100GB/s链路被阻塞，会导致VLAN中的流量都通过两条10GB/s链路传输，可能会引起网络拥塞及流量丢失。

图 7-26 根保护此时可以在DeviceC连接DeviceD的端口上，配置根保护。对于启用根保护功能的指定端口，其端口角色只能保持为指定端口。一旦启用根保护功能的指定端口收到优先级更高的BPDU时，端口状态将进入Discarding状态，不再转发报文。经过一段时间（通常为两倍的Forward Delay），如果端口一直没有再收到优先级较高的BPDU，端口会自动恢复到正常的Forwarding状态。
当端口的角色是指定端口时，配置的根保护功能才生效。
环路保护在运行生成树协议的网络中，根端口和其他阻塞端口状态是依靠不断接收来自上游设备的BPDU维持。当由于链路拥塞或者单向链路故障导致这些端口收不到来自上游交换设备的BPDU时，设备会重新选择根端口。原先的根端口会转变为指定端口，而原先的阻塞端口会迁移到转发状态，从而造成网络中产生环路。如图7-27所示，当BP2-CP1之间的链路发生拥塞时，DeviceC由于根端口CP1在超时时间内收不到来自上游设备的BPDU报文，Alternate端口CP2放开转变成了根端口，根端口CP1转变成指定端口，从而形成了环路。

图 7-27 链路发生拥塞情况拓扑的变化启动了环路保护功能后，如果根端口或Alternate端口长时间收不到来自上游设备的BPDU报文时，则向网管发出通知信息（此时根端口会进入Discarding状态，角色切换为指定端口），而Alternate端口则会一直保持在阻塞状态（角色也会切换为指定端口），不转发报文，从而不会在网络中形成环路。直到链路不再拥塞或单向链路故障恢复，端口重新收到BPDU报文进行协商，并恢复到链路拥塞或者单向链路故障前的角色和状态。
环路保护功能只能在根端口或Alternate端口上配置生效。
共享链路保护功能共享链路保护功能用在设备双归属接入网络的场景中。
MSTP网络中，当共享链路故障时，通过共享链路保护功能，使本设备的工作模式强制转换为RSTP模式，配合使用根保护功能，可以避免网络环路。

#### 7.9.2 配置BPDU保护功能

背景信息边缘端口直接和用户终端相连，正常情况下，边缘端口不会收到BPDU报文。如果攻击者伪造BPDU恶意攻击设备，当边缘端口接收到BPDU报文时，设备会自动将边缘端口设置为非边缘端口，并重新进行生成树计算，从而引起网络振荡。通过使能BPDU保护可以防止伪造BPDU恶意攻击。边缘端口的配置请参见7.7 启用边缘端口和配置BPDU报文过滤功能（RSTP/MSTP）。
说明使能设备的BPDU保护功能只对通过stp edged-port或stp edged-port default手工配置的边缘端口生效，对通过系统的边缘端口自动探测功能设置成的边缘端口不生效。

请在有边缘端口的设备上进行以下配置。
操作步骤步骤1 进入系统视图。
system-view步骤2 （可选）进入MSTP进程视图。
本步骤仅需要在ID非0的MSTP进程中配置系统参数时执行。当在ID为0的进程中配置时，可跳过本步，直接进入下一步。
stp process process-id步骤3 配置BPDU保护功能。
stp bpdu-protection缺省情况下，BPDU保护功能处于去使能状态。
说明配置 BPDU 保护功能后，如果边缘端口收到 BPDU 报文，边缘端口将会被 error-down ，边缘端口属性不变。如果希望被error-down的边缘端口恢复Up，可通过如下方式实现：
在接口视图下执行命令restart。
●
● 在接口视图下先执行命令shutdown，再执行命令undo shutdown。
● 在系统视图下执行命令error-down auto-recovery cause bpdu-protection interval interval-value，使能端口自动恢复为Up的功能，并设置端口自动恢复为Up的延时时间。使被关闭的端口经过延时时间interval-value后能够自动恢复。配置时需要注意：
– 缺省情况下，未使能处于error-down状态的端口状态自动恢复为Up的功能，所以没有缺省延迟时间值。当用户配置该命令时，必须指定恢复延迟时间。
– 取值越小表示端口的管理状态自动恢复为Up的延迟时间越短，端口Up/Down状态震荡频率越高。
– 取值越大表示端口的管理状态自动恢复为Up的延迟时间越长，端口流量中断时间越长。
– 自动恢复仅对配置error-down auto-recovery命令之后发生error-down的端口有效，对配置此命令之前已经error-down的端口不生效。
----结束检查配置结果执行如下命令，根据BPDU-Protection字段查看BPDU保护功能的配置情况。
● display stp [ process process-id ] [ instance instance-id ] [ interface interface-type interface-number | slot slot-id ]
● display stp active
● display stp global

#### 7.9.3 配置TC保护功能

背景信息如果攻击者伪造拓扑变化BPDU报文恶意攻击设备，设备短时间内会收到很多拓扑变化BPDU报文，频繁的删除MAC或者ARP表项操作会给设备造成很大的负担，也给网络的稳定带来很大隐患。

启用TC保护功能后，在指定时间内，设备处理拓扑变化报文的次数可配置。如果在指定时间内，设备收到拓扑变化报文的数量大于配置的最大数量，那么设备只会处理指定的报文个数。对于其他超出最大数量的拓扑变化报文，指定时间超时后设备只对其统一处理一次。这样可以避免频繁的删除MAC地址表项和ARP表项，从而达到保护设备的目的。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置对TC类型BPDU报文的保护功能。
stp tc-protection缺省情况下，设备对TC类型BPDU报文的保护功能处于关闭状态。
步骤3 配置TC保护功能的参数，请选择执行其中一个或两个：
● 配置设备处理最大数量的拓扑变化报文所需的时间。
stp tc-protection interval interval-value缺省情况下，设备处理最大数量的拓扑变化报文所需的时间是 Hello Time 。
● 配置设备在设定时间内处理拓扑变化报文的最大数量。
stp tc-protection threshold threshold缺省情况下，设备在指定时间内处理拓扑变化报文的最大数量是1。
说明
● TC保护功能的参数有两个：处理拓扑变化报文的时间和最大数量，即在设定的某段时间内能处理的最大数量的BPDU报文，例如，时间设定为10秒，最大数量设定为5，则设备收到拓扑变化报文后，在10秒内只会处理最开始收到的5个拓扑变化报文，对于后面收到的报文则会等10秒超时后再统一处理。处理拓扑变化报文的时间推荐配置为一个STP实例下的端口数目除以10，在指定时间内配置的最大报文数量推荐配置为1，即假设一个STP实例下的端口个数为100，推荐配置设备每10秒处理1个拓扑变化报文。
● 在stp tc-protection interval指定的时间内，设备只会处理stp tc-protection threshold指定的数量拓扑变化报文，对于其他的报文会延迟处理，所以可能会影响生成树的收敛速度。
----结束检查配置结果执行命令display stp global，根据字段Tc-protection、Tc-protection threshold、Tc- protection interval 查看 TC 保护功能的配置情况。

#### 7.9.4 配置根保护功能

背景信息由于维护人员的错误配置或网络中的恶意攻击，网络中的合法根桥设备有可能会收到优先级更高的BPDU报文，使得合法根桥设备失去根桥的地位，引起网络拓扑结构的错误变动。这种拓扑变化可能会导致原来应该通过高速链路的流量被牵引到低速链路上，造成网络拥塞。为了防止这种情况发生，可在设备上部署根保护功能，通过维持指定端口的角色来保护根桥设备的地位。
一般在根桥的端口上配置根保护功能。当端口的角色是指定端口时，配置的根保护功能才生效。

根保护功能和环路保护功能互斥，配置了根保护功能的端口不能再配置环路保护。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤3 配置接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 （可选）将端口绑定到进程。
本步骤仅在需要把端口绑定到ID非0进程时配置。当端口属于ID为0的进程，可跳过本步，直接进入下一步。
stp binding process process-id步骤5 配置根保护功能。
stp root-protection缺省情况下，端口的根保护功能处于关闭状态。
----结束检查配置结果执行如下命令，根据Protection Type字段查看接口下根保护功能的配置情况。
● display stp [ process process-id ] [ instance instance-id ] [ interface interface-type interface-number | slot slot-id ]
● display stp active

#### 7.9.5 配置环路保护功能

背景信息在运行生成树协议的网络中，根端口和其他阻塞端口状态是依靠不断接收来自上游设备的BPDU维持。当由于链路拥塞或者单向链路故障导致这些端口收不到来自上游设备的BPDU时，设备会重新选择根端口。原先的根端口会转变为指定端口，而原先的阻塞端口会迁移到转发状态，从而造成网络中产生环路。为了防止以上情况发生，可部署环路保护功能。
启动了环路保护功能后，如果根端口或Alternate端口长时间收不到来自上游的BPDU时，端口角色变为指定端口，端口状态变为 Discarding 状态，同时向网管发出通知信息，而阻塞端口则会一直保持在阻塞状态，不转发报文，从而不会在网络中形成环路。直到根端口或Alternate端口收到BPDU报文，端口状态才恢复正常为Forwarding状态。

由于Alternate端口是根端口的备份端口，如果设备上有Alternate端口，需要在根端口和Alternate端口上同时配置环路保护。
根保护功能和环路保护功能互斥，配置了环路保护功能的端口不能再配置根保护。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入根端口或Alternate端口的接口视图。
interface interface-type interface-number步骤3 配置接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 （可选）将端口绑定到进程。
本步骤仅在需要把端口绑定到ID非0进程时配置。当端口属于ID为0的进程，可跳过本步，直接进入下一步。
stp binding process process-id步骤5 配置环路保护功能。
stp loop-protection缺省情况下，环路保护功能处于关闭状态。
----结束检查配置结果执行如下命令，根据Protection Type字段查看接口下环路保护功能的配置情况。
● display stp [ process process-id ] [ instance instance-id ] [ interface interface-type interface-number | slot slot-id ]
● display stp active

#### 7.9.6 配置共享链路保护功能（MSTP）

背景信息共享链路保护功能用在设备双归属接入网络的场景中。
当共享链路故障时，通过共享链路保护功能，使本设备的工作模式强制转换为RSTP模式，配合使用根保护功能，可以避免网络环路。
操作步骤步骤1 进入系统视图。
system-view

步骤2 进入MSTP进程视图。
stp process process-id步骤3 配置共享链路保护功能。
stp link-share-protection
----结束检查配置结果在MSTP进程视图下执行命令display this，查看共享链路保护功能配置情况。

### 7.10 配置设备与其他厂商设备互通的参数

#### 7.10.1 了解设备与其他厂商互通参数

P/A 机制设备快速迁移P/A（Proposal/Agreement）机制支持普通方式和增强方式两种，详细的介绍请参见Proposal/Agreement机制。在运行生成树协议的网络中，如果华为设备与其他厂商设备混合组网，华为设备与其他厂商设备的P/A机制不同可能导致互通失败。可以根据其他厂商设备的P/A机制，选择华为设备端口使用增强的快速迁移机制还是普通的快速迁移机制。
● 增强方式：当前端口在计算同步标志位时计算根端口。
a. 上游设备发送Proposal报文，请求进行快速迁移，下游设备接收到后，把与上游设备相连的端口设置为根端口，并阻塞所有非边缘端口。
b. 上游设备继续发送Agreement报文，下游设备接收到后，根端口转为Forwarding状态。
c. 下游设备回应Agreement报文，上游设备接收到后，把与下游设备相连的端口设置为指定端口，指定端口进入Forwarding状态。
● 普通方式：当前端口在计算同步标志位时忽略根端口。
a. 上游设备发送Proposal报文，请求进行快速迁移，下游设备接收到后，把与上游设备相连的端口设置为根端口，并阻塞所有非边缘端口，根端口转为Forwarding状态。
b. 下游设备回应Agreement报文，上游设备接收到后，把与下游设备相连的端口设置为指定端口，指定端口进入Forwarding状态。
接口收发 MSTP 协议的报文格式（MSTP）
MSTP报文存在两种格式：一种为dot1s，即IEEE 802.1s规定的报文格式；另一种为legacy，是一种私有报文格式。
MSTP 网络中，如果华为设备与其他厂商设备混合组网，可以指定报文的格式，也可以配置MSTP报文格式自适应功能，即根据收到的MSTP报文格式自动切换端口支持的MSTP协议报文格式，使报文格式与对端匹配。

摘要侦听功能（MSTP）
MSTP网络中，华为设备与其他厂商设备混合组网时，在域名、修订级别、VLAN实例映射表全都一致的情况下，由于双方BPDU报文密钥不一致，会导致两台设备不能正常互通。在这种情况下，需要在华为设备上使能摘要侦听功能。
使能摘要侦听功能后，华为设备的BPDU报文密钥与其他厂商设备的BPDU报文密钥一致。

#### 7.10.2 配置接口Proposal/Agreement机制

背景信息设备快速迁移P/A（Proposal/Agreement）机制支持普通方式和增强方式两种。
在运行生成树协议的网络中，如果华为设备与其他厂商设备混合组网，华为设备与其他厂商设备的P/A机制不同可能导致互通失败。可以根据其他厂商设备的P/A机制，选择华为设备端口使用增强的快速迁移机制还是普通的快速迁移机制。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤3 配置接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 配置端口使用普通的快速迁移方式。
stp no-agreement-check缺省情况下，端口使用增强的快速迁移机制。
----结束检查配置结果在接口视图下执行命令display this，查看接口下P/A机制的方式。

#### 7.10.3 配置接口收发MSTP报文的格式（MSTP）

背景信息MSTP报文存在两种格式：一种为dot1s，即IEEE 802.1s规定的报文格式；另一种为legacy，是一种私有报文格式。
MSTP网络中，如果华为设备与其他厂商设备混合组网，可以指定报文的格式，也可以配置MSTP报文格式自适应功能，即根据收到的MSTP报文格式自动切换端口支持的MSTP协议报文格式，使报文格式与对端匹配。

操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤3 配置接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 配置接口收发MSTP报文的格式。
stp compliance { auto | dot1s | legacy }说明如果直连的端口上一端配置dot1s，而另一端配置legacy，是不能协商成功的。
缺省情况下，MSTP报文收发格式为auto模式。
----结束检查配置结果执行命令display stp [ process process-id ] [ instance instance-id ] interface interface-type interface-number，根据Port Protocol Type字段查看接口收发MSTP报文的格式。

#### 7.10.4 使能摘要侦听功能（MSTP）

背景信息MSTP网络中，华为设备与其他厂商设备混合组网时，在域名、修订级别、VLAN实例映射表全都一致的情况下，由于双方BPDU报文密钥不一致，会导致两台设备不能正常互通。在这种情况下，需要在华为设备上使能摘要侦听功能。
使能摘要侦听功能后，华为设备的 BPDU 报文密钥与其他厂商设备的 BPDU 报文密钥一致。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤 3 配置接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。

仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 使能摘要侦听功能。
stp config-digest-snoop缺省情况下，摘要侦听功能处于未使能状态。
----结束检查配置结果执行命令display stp [ process process-id ] [ instance instance-id ] interface interface-type interface-number，根据Config-digest-snoop字段查看摘要侦听功能的配置情况。

### 7.11 维护STP/RSTP/MSTP

#### 7.11.1 查看拓扑变化统计信息

背景信息通过查看拓扑变化相关的统计信息，如果设备拓扑变化次数递增，则可以确定网络存在振荡。
操作步骤
● 执行命令display stp [ process process-id ] [ instance instance-id ] topology- change，查看生成树协议拓扑变化相关的统计信息。
● 执行命令display stp [ process process-id ] [ instance instance-id ] [ interface interface-type interface-number | slot slot-id ] tc-bpdu statistics，查看端口TC/TCN BPDU报文收发计数。
----结束

#### 7.11.2 清除STP/RSTP/MSTP统计信息

背景信息须知清除生成树协议的统计信息后，以前的信息将无法恢复，务必仔细确认。
操作步骤
● 执行命令 reset stp [ interface interface-type interface-number ] statistics ，清除生成树的统计信息。
----结束

#### 7.11.3 配置MCheck恢复接口工作模式（RSTP/MSTP）

背景信息在运行RSTP/MSTP的设备上，如果某个端口和另一台运行STP的设备连接，则该端口会自动迁移到STP工作模式。
如果运行STP的设备被关机或移走，该端口无法自动迁移回RSTP/MSTP模式，此时需要在设备上执行MCheck操作，将端口手动迁移回RSTP/MSTP模式。
以下情况需要执行MCheck操作，将端口手动迁移回RSTP/MSTP模式：
● 运行STP的设备被关机或移走。
● 运行STP的设备切换为RSTP模式。
● 运行STP的设备切换为MSTP模式。
操作步骤
● 在接口视图下执行MCheck操作，使接口从STP模式迁移回RSTP/MSTP模式。
system-view interface interface-type interface-number stp mcheck
● 在系统视图下执行MCheck操作，使设备上接口从STP模式迁移回RSTP/MSTP模式。
system-view stp mcheck
● 在MSTP进程视图下执行MCheck操作，使MSTP进程下接口从STP模式迁移回MSTP模式。
system-view stp process process-id stp mcheck
----结束

### 7.12 STP/RSTP/MSTP配置举例

#### 7.12.1 举例：配置STP功能

组网需求如图7-28所示，网络中DeviceA、DeviceB、DeviceC和DeviceD之间存在环路。用户希望在网络中部署STP，破除网络环路，从而避免广播风暴和MAC表振荡。
图 7-28 配置 STP 功能组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。

操作步骤步骤1 配置生成树协议工作在STP模式。

| <HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] stp mode stp |
|---|
| <HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] stp mode stp |
| <HUAWEI> system-view [HUAWEI] sysname DeviceC [DeviceC] stp mode stp |
| <HUAWEI> system-view [HUAWEI] sysname DeviceD [DeviceD] stp mode stp |

步骤2 配置根桥和备份根桥。一般将网络中性能高、网络层次高的设备指定为根桥和备份根桥。
\# 配置DeviceA为根桥。
[DeviceA] stp root primary \# 配置DeviceB为备份根桥。
[DeviceB] stp root secondary步骤3 配置网络中所有设备使用相同的端口路径开销计算方法；并配置DeviceC上10GE1/0/1的端口路径开销值，实现将该端口阻塞。
\# 配置DeviceA的端口路径开销的计算方法为华为私有计算方法。
[DeviceA] stp pathcost-standard legacy \# 配置DeviceB的端口路径开销的计算方法为华为私有计算方法。
[DeviceB] stp pathcost-standard legacy \# 配置DeviceC的端口路径开销的计算方法为华为私有计算方法；并配置DeviceC上10GE1/0/1的端口路径开销值为20000，使该端口的路径开销大于其他接口，从而实现将该端口阻塞。

[DeviceC] stp pathcost-standard legacy [DeviceC] interface 10ge 1/0/1 [DeviceC-10GE1/0/1] portswitch [DeviceC-10GE1/0/1] stp cost 20000 [DeviceC-10GE1/0/1] undo shutdown [DeviceC-10GE1/0/1] quit \# 配置DeviceD的端口路径开销的计算方法为华为私有计算方法。
[DeviceD] stp pathcost-standard legacy步骤4 设备DeviceB和DeviceC与PC相连的端口上去使能STP功能。
\# DeviceB的端口10GE1/0/2上去使能STP功能。
[DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] portswitch [DeviceB-10GE1/0/2] stp disable [DeviceB-10GE1/0/2] quit \# DeviceC的端口10GE1/0/2上去使能STP功能。
[DeviceC] interface 10ge 1/0/2 [DeviceC-10GE1/0/2] portswitch [DeviceC-10GE1/0/2] stp disable [DeviceC-10GE1/0/2] quit步骤5 启用STP。
缺省情况下，设备上生成树协议处于使能状态，无需操作。在系统视图下执行命令stp enable可以启用STP/RSTP/MSTP功能。
----结束检查配置结果一段时间生成树协议计算稳定后，执行以下操作，验证配置结果。
\# 在DeviceA上执行命令display stp brief，查看端口角色和端口状态。根桥DeviceA上10GE1/0/1和10GE1/0/2为指定端口，处于forwarding状态。
[DeviceA] display stp brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 DESI forwarding none 2 disable 0 10GE1/0/2 DESI forwarding none 2 disable \# 在DeviceB上执行命令display stp interface brief，查看10GE1/0/1的端口角色和端口状态。DeviceB上10GE1/0/1为指定端口，处于forwarding状态。
[DeviceB] display stp interface 10ge 1/0/1 brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 DESI forwarding none 2 disable \# 在DeviceC上执行命令display stp brief，查看端口角色和端口状态。DeviceC上10GE1/0/1为Alternate端口，处于discarding状态；10GE1/0/3为根端口，处于forwarding状态。
[DeviceC] display stp brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 ALTE discarding none 20000 disable 0 10GE1/0/3 ROOT forwarding none 2 disable

配置脚本
● DeviceA \# sysname DeviceA \# stp mode stp stp instance 0 root primary stp pathcost-standard legacy \# return
● DeviceB \# sysname DeviceB \# stp mode stp stp instance 0 root secondary stp pathcost-standard legacy \# interface 10GE1/0/2 stp disable \# return
● DeviceC \# sysname DeviceC \# stp mode stp stp pathcost-standard legacy \# interface 10GE1/0/1 stp instance 0 cost 20000 \# interface 10GE1/0/2 stp disable \# return
● DeviceD \# sysname DeviceD \# stp mode stp stp pathcost-standard legacy \# return

#### 7.12.2 举例：配置RSTP功能

组网需求如图7-29所示，网络中DeviceA、DeviceB、DeviceC和DeviceD之间存在环路。用户希望在网络中部署RSTP，破除网络环路，从而避免广播风暴和MAC表振荡。
图 7-29 配置 RSTP 功能组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。

操作步骤步骤1 配置生成树协议工作在RSTP模式。

| <HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] stp mode rstp |
|---|
| <HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] stp mode rstp |
| <HUAWEI> system-view [HUAWEI] sysname DeviceC [DeviceC] stp mode rstp |
| <HUAWEI> system-view [HUAWEI] sysname DeviceD [DeviceD] stp mode rstp |

步骤2 配置根桥和备份根桥。一般将网络中性能高、网络层次高的设备指定为根桥和备份根桥。
\# 配置DeviceA为根桥。
[DeviceA] stp root primary \# 配置DeviceB为备份根桥。
[DeviceB] stp root secondary步骤3 配置网络中所有设备使用相同的端口路径开销计算方法；并配置DeviceC上10GE1/0/1的端口路径开销值，实现将该端口阻塞。
\# 配置DeviceA的端口路径开销计算方法为华为私有计算方法。
[DeviceA] stp pathcost-standard legacy \# 配置DeviceB的端口路径开销计算方法为华为私有计算方法。
[DeviceB] stp pathcost-standard legacy \# 配置DeviceC的端口路径开销计算方法为华为私有计算方法；配置DeviceC端口10GE1/0/1端口路径开销值为20000，使该端口的路径开销大于其他接口，从而实现将该端口阻塞。

[DeviceC] stp pathcost-standard legacy [DeviceC] interface 10ge 1/0/1 [DeviceC-10GE1/0/1] portswitch [DeviceC-10GE1/0/1] stp cost 20000 [DeviceC-10GE1/0/1] quit \# 配置DeviceD的端口路径开销计算方法为华为私有计算方法。
[DeviceD] stp pathcost-standard legacy步骤4 配置设备DeviceB和DeviceC与PC相连的端口为边缘端口。
\# DeviceB端口10GE1/0/2配置为边缘端口，并配置BPDU保护功能。
[DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] portswitch [DeviceB-10GE1/0/2] stp edged-port enable [DeviceB-10GE1/0/2] quit [DeviceB] stp bpdu-protection \# DeviceC端口10GE1/0/2配置为边缘端口，并配置BPDU保护功能。
[DeviceC] interface 10ge 1/0/2 [DeviceC-10GE1/0/2] portswitch [DeviceC-10GE1/0/2] stp edged-port enable [DeviceC-10GE1/0/2] quit [DeviceC] stp bpdu-protection步骤5 启用RSTP。
缺省情况下，设备上生成树协议处于使能状态，无需操作。在系统视图下执行命令stp enable可以启用STP/RSTP/MSTP功能。
步骤6 在根桥DeviceA的指定端口10GE1/0/1和10GE1/0/2上配置根保护功能。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] stp root-protection [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] stp root-protection [DeviceA-10GE1/0/2] quit
----结束检查配置结果一段时间生成树协议计算稳定后，执行以下操作，验证配置结果。
\# 在DeviceA上执行命令display stp brief，查看端口状态和端口的保护类型。根桥DeviceA的10GE1/0/1和10GE1/0/2为指定端口，并配置了根保护功能。
[DeviceA] display stp brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 DESI forwarding root 2 disable 0 10GE1/0/2 DESI forwarding root 2 disable \# 在DeviceB上执行命令display stp interface brief，查看10GE1/0/1的端口角色和端口状态。DeviceB上10GE1/0/1为指定端口，处于forwarding状态。
[DeviceB] display stp interface 10ge 1/0/1 brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 DESI forwarding none 2 disable \# 在DeviceC上执行命令display stp brief，查看端口角色和端口状态。DeviceC上10GE1/0/1为Alternate端口，处于discarding状态；10GE1/0/3为根端口，处于forwarding状态。

[DeviceC] display stp brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 ALTE discarding none 20000 disable 0 10GE1/0/3 ROOT forwarding none 2 disable配置脚本
● DeviceA \# sysname DeviceA \# stp mode rstp stp instance 0 root primary stp pathcost-standard legacy \# interface 10GE1/0/1 stp root-protection \# interface 10GE1/0/2 stp root-protection \# return
● DeviceB \# sysname DeviceB \# stp mode rstp stp bpdu-protection stp instance 0 root secondary stp pathcost-standard legacy \# interface 10GE1/0/2 stp edged-port enable \# return
● DeviceC \# sysname DeviceC \# stp mode rstp stp bpdu-protection stp pathcost-standard legacy \# interface 10GE1/0/1 stp instance 0 cost 20000 \# interface 10GE1/0/2 stp edged-port enable \# return
● DeviceD \# sysname DeviceD \# stp mode rstp stp pathcost-standard legacy \# return

#### 7.12.3 举例：配置MSTP功能

组网需求如图7-30所示，网络中DeviceA、DeviceB、DeviceC和DeviceD之间存在环路。用户希望在网络中部署MSTP，破除网络环路，从而避免广播风暴和MAC表振荡；并且实现VLAN2～VLAN10和VLAN11～VLAN20的流量负载分担。
图 配置 功能组网图7-30 MSTP说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。
操作步骤步骤1 配置DeviceA、DeviceB、DeviceC和DeviceD到域名为RG1的域内，创建实例MSTI1和实例MSTI2。

说明当两台设备的MST域的域名、实例和VLAN的映射关系、MST域的修订级别都相同时，这两台设备属于同一个MST域。
不能将同一个VLAN映射到多个不同的实例上。如果将一个已经和实例建立映射关系的VLAN又映射到另一个实例上，原来的映射关系将被取消。
\# 在DeviceA上配置MST域。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] stp region-configuration [DeviceA-mst-region] region-name RG1 [DeviceA-mst-region] instance 1 vlan 2 to 10 [DeviceA-mst-region] instance 2 vlan 11 to 20 [DeviceA-mst-region] quit \# 在DeviceB上配置MST域。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] stp region-configuration [DeviceB-mst-region] region-name RG1 [DeviceB-mst-region] instance 1 vlan 2 to 10 [DeviceB-mst-region] instance 2 vlan 11 to 20 [DeviceB-mst-region] quit \# 在DeviceC上配置MST域。
<HUAWEI> system-view [HUAWEI] sysname DeviceC [DeviceC] stp region-configuration [DeviceC-mst-region] region-name RG1 [DeviceC-mst-region] instance 1 vlan 2 to 10 [DeviceC-mst-region] instance 2 vlan 11 to 20 [DeviceC-mst-region] quit \# 在DeviceD上配置MST域。
<HUAWEI> system-view [HUAWEI] sysname DeviceD [DeviceD] stp region-configuration [DeviceD-mst-region] region-name RG1 [DeviceD-mst-region] instance 1 vlan 2 to 10 [DeviceD-mst-region] instance 2 vlan 11 to 20 [DeviceD-mst-region] quit步骤2 在MST域RG1内，分别配置MSTI1、MSTI2的根桥和备份根桥。
\# 配置 DeviceA 为 MSTI1 的根桥。
[DeviceA] stp instance 1 root primary \# 配置DeviceB为MSTI1的备份根桥。
[DeviceB] stp instance 1 root secondary \# 配置DeviceB为MSTI2的根桥。
[DeviceB] stp instance 2 root primary \# 配置DeviceA为MSTI2的备份根桥。
[DeviceA] stp instance 2 root secondary步骤3 配置同一网络内所有设备的端口路径开销应使用相同的计算方法；配置实例MSTI1和MSTI2中将要被阻塞端口的路径开销值大于缺省值。

\# 配置DeviceA的端口路径开销计算方法为华为计算方法。
[DeviceA] stp pathcost-standard legacy \# 配置DeviceB的端口路径开销计算方法为华为计算方法。
[DeviceB] stp pathcost-standard legacy \# 配置DeviceC的端口路径开销计算方法为华为计算方法，将端口10GE1/0/2在实例MSTI2中的路径开销值配置为20000。
[DeviceC] stp pathcost-standard legacy [DeviceC] interface 10ge 1/0/2 [DeviceC-10GE1/0/2] portswitch [DeviceC-10GE1/0/2] stp instance 2 cost 20000 [DeviceC-10GE1/0/2] quit \# 配置DeviceD的端口路径开销计算方法为华为计算方法，将端口10GE1/0/2在实例MSTI1中的路径开销值配置为20000。
[DeviceD] stp pathcost-standard legacy [DeviceD] interface 10ge 1/0/2 [DeviceD-10GE1/0/2] portswitch [DeviceD-10GE1/0/2] stp instance 1 cost 20000 [DeviceD-10GE1/0/2] quit步骤4 设备全局启用MSTP。
缺省情况下，设备上生成树协议处于使能状态，无需操作。在系统视图下执行命令stp enable可以启用STP/RSTP/MSTP功能。
步骤5 在设备与终端相连的端口上去使能MSTP。
\# 在DeviceC端口10GE1/0/1上去使能MSTP功能。
[DeviceC] interface 10ge 1/0/1 [DeviceC-10GE1/0/1] portswitch [DeviceC-10GE1/0/1] stp disable [DeviceC-10GE1/0/1] quit \# 在DeviceD端口10GE1/0/1上去使能MSTP功能。
[DeviceD] interface 10ge 1/0/1 [DeviceD-10GE1/0/1] portswitch [DeviceD-10GE1/0/1] stp disable [DeviceD-10GE1/0/1] quit步骤6 配置保护功能，如在各实例的根桥设备的指定端口配置根保护功能。
\# 在 DeviceA 端口 10GE1/0/1 上启动根保护。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] stp root-protection [DeviceA-10GE1/0/1] quit \# 在DeviceB端口10GE1/0/1上启动根保护。
[DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] portswitch [DeviceB-10GE1/0/1] stp root-protection [DeviceB-10GE1/0/1] quit步骤 7 创建 VLAN 并将接口加入 VLAN 。
\# 在DeviceA上创建VLAN2～20，并将DeviceA的端口10GE1/0/1和10GE1/0/2分别加入VLAN。

[DeviceA] vlan batch 2 to 20 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type trunk [DeviceA-10GE1/0/1] port trunk allow-pass vlan 2 to 20 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type trunk [DeviceA-10GE1/0/2] port trunk allow-pass vlan 2 to 20 [DeviceA-10GE1/0/2] quit \# 在DeviceB上创建VLAN2～20，并将DeviceB的端口10GE1/0/1和10GE1/0/2分别加入VLAN。
[DeviceB] vlan batch 2 to 20 [DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] portswitch [DeviceB-10GE1/0/1] port link-type trunk [DeviceB-10GE1/0/1] port trunk allow-pass vlan 2 to 20 [DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] portswitch [DeviceB-10GE1/0/2] port link-type trunk [DeviceB-10GE1/0/2] port trunk allow-pass vlan 2 to 20 [DeviceB-10GE1/0/2] quit \# 在DeviceC上创建VLAN2～20，并将DeviceC的端口10GE1/0/1、10GE1/0/2和10GE1/0/3分别加入VLAN。
[DeviceC] vlan batch 2 to 20 [DeviceC] interface 10ge 1/0/1 [DeviceC-10GE1/0/1] portswitch [DeviceC-10GE1/0/1] port link-type access [DeviceC-10GE1/0/1] port default vlan 2 [DeviceC-10GE1/0/1] quit [DeviceC] interface 10ge 1/0/2 [DeviceC-10GE1/0/2] portswitch [DeviceC-10GE1/0/2] port link-type trunk [DeviceC-10GE1/0/2] port trunk allow-pass vlan 2 to 20 [DeviceC-10GE1/0/2] quit [DeviceC] interface 10ge 1/0/3 [DeviceC-10GE1/0/3] portswitch [DeviceC-10GE1/0/3] port link-type trunk [DeviceC-10GE1/0/3] port trunk allow-pass vlan 2 to 20 [DeviceC-10GE1/0/3] quit \# 在DeviceD上创建VLAN2～20，并将DeviceD的端口10GE1/0/1、10GE1/0/2和10GE1/0/3分别加入VLAN。
[DeviceD] vlan batch 2 to 20 [DeviceD] interface 10ge 1/0/1 [DeviceD-10GE1/0/1] portswitch [DeviceD-10GE1/0/1] port link-type access [DeviceD-10GE1/0/1] port default vlan 11 [DeviceD-10GE1/0/1] quit [DeviceD] interface 10ge 1/0/2 [DeviceD-10GE1/0/2] portswitch [DeviceD-10GE1/0/2] port link-type trunk [DeviceD-10GE1/0/2] port trunk allow-pass vlan 2 to 20 [DeviceD-10GE1/0/2] quit [DeviceD] interface 10ge 1/0/3 [DeviceD-10GE1/0/3] portswitch [DeviceD-10GE1/0/3] port link-type trunk [DeviceD-10GE1/0/3] port trunk allow-pass vlan 2 to 20 [DeviceD-10GE1/0/3] quit
----结束

检查配置结果在网络计算稳定后，执行以下操作，验证配置结果。本配置举例以实例1和实例2为例，因此不用关注实例0中端口的状态。
\# 在DeviceA上执行命令display stp brief，查看端口角色和端口状态。在MSTI1中，由于DeviceA是根桥，DeviceA的端口10GE1/0/2和10GE1/0/1成为指定端口。在MSTI2中，DeviceA的端口10GE1/0/1成为指定端口，端口10GE1/0/2成为根端口。
[DeviceA] display stp brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 DESI forwarding root 2 disable 0 10GE1/0/2 DESI forwarding none 2 disable 1 10GE1/0/1 DESI forwarding root 2 disable 1 10GE1/0/2 DESI forwarding none 2 disable 2 10GE1/0/1 DESI forwarding root 2 disable 2 10GE1/0/2 ROOT forwarding none 2 disable \# 在DeviceB上执行命令display stp brief，查看端口角色和端口状态。在MSTI2中，由于DeviceB是根桥，端口10GE1/0/1和10GE1/0/2在MSTI2中成为指定端口。在MSTI1中，DeviceB的端口10GE1/0/1成为指定端口，端口10GE1/0/2成为根端口。
[DeviceB] display stp brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 DESI forwarding root 2 disable 0 10GE1/0/2 ROOT forwarding none 2 disable 1 10GE1/0/1 DESI forwarding root 2 disable 1 10GE1/0/2 ROOT forwarding none 2 disable 2 10GE1/0/1 DESI forwarding root 2 disable 2 10GE1/0/2 DESI forwarding none 2 disable \# 在DeviceC上执行命令display stp interface brief，查看端口角色和端口状态。
DeviceC的端口10GE1/0/3在MSTI1和MSTI2中为根端口。DeviceC的另一个端口10GE1/0/2，在MSTI2中被阻塞，在MSTI1中被计算为指定端口。
[DeviceC] display stp interface 10ge 1/0/3 brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/3 ROOT forwarding none 2 disable 1 10GE1/0/3 ROOT forwarding none 2 disable 2 10GE1/0/3 ROOT forwarding none 2 disable [DeviceC] display stp interface 10ge 1/0/2 brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/2 DESI forwarding none 2 disable 1 10GE1/0/2 DESI forwarding none 2 disable 2 10GE1/0/2 ALTE discarding none 20000 disable \# 在DeviceD上执行命令display stp interface brief，查看端口角色和端口状态。
DeviceD的端口10GE1/0/3在MSTI1和MSTI2中为根端口。DeviceD的另一个端口10GE1/0/2 ，在 MSTI1 中被阻塞，在 MSTI2 中被计算为指定端口。
[DeviceD] display stp interface 10ge 1/0/3 brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/3 ALTE discarding none 2 disable 1 10GE1/0/3 ROOT forwarding none 2 disable 2 10GE1/0/3 ROOT forwarding none 2 disable [DeviceD] display stp interface 10ge 1/0/2 brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/2 ROOT forwarding none 2 disable 1 10GE1/0/2 ALTE discarding none 20000 disable 2 10GE1/0/2 DESI forwarding none 2 disable配置脚本
● DeviceA

\# sysname DeviceA \# vlan batch 2 to 20 \# stp instance 1 root primary stp instance 2 root secondary stp pathcost-standard legacy \# stp region-configuration region-name RG1 instance 1 vlan 2 to 10 instance 2 vlan 11 to 20 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 2 to 20 stp root-protection \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2 to 20 \# return
● DeviceB \# sysname DeviceB \# vlan batch 2 to 20 \# stp instance 1 root secondary stp instance 2 root primary stp pathcost-standard legacy \# stp region-configuration region-name RG1 instance 1 vlan 2 to 10 instance 2 vlan 11 to 20 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 2 to 20 stp root-protection \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2 to 20 \# return
● DeviceC \# sysname DeviceC \# vlan batch 2 to 20 \# stp pathcost-standard legacy \# stp region-configuration region-name RG1 instance 1 vlan 2 to 10 instance 2 vlan 11 to 20 \# interface 10GE1/0/1 port link-type access port default vlan 2 stp disable \# interface 10GE1/0/2

port link-type trunk port trunk allow-pass vlan 2 to 20 stp instance 2 cost 20000 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 2 to 20 \# return
● DeviceD \# sysname DeviceD \# vlan batch 2 to 20 \# stp pathcost-standard legacy \# stp region-configuration region-name RG1 instance 1 vlan 2 to 10 instance 2 vlan 11 to 20 \# interface 10GE1/0/1 port link-type access port default vlan 11 stp disable \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2 to 20 stp instance 1 cost 20000 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 2 to 20 \# return

#### 7.12.4 举例：配置MSTP多进程功能

组网需求如图7-31所示，DeviceA和DeviceB作为PE设备，下接DeviceC~DeviceH作为CE侧设备构成多个接入环。DeviceA与DeviceC、DeviceD构成一个环路；DeviceB与DeviceG、DeviceH构成一个环路；DeviceA、DeviceB与DeviceE、DeviceF构成一个环路。
通过部署MSTP多进程，实现不同环上的生成树协议进行独立计算，互不影响。
图 7-31 MSTP 多进程组网图说明本例中interface1、interface2、interface3、interface4、interface5分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3、10GE1/0/4、10GE1/0/5。

操作步骤步骤1 配置MSTP基本功能，将设备加入到域，并创建实例。
\# 在DeviceA上配置域和实例。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] stp region-configuration [DeviceA-mst-region] region-name RG1 [DeviceA-mst-region] instance 1 vlan 2 to 100 [DeviceA-mst-region] instance 2 vlan 101 to 200 [DeviceA-mst-region] instance 3 vlan 201 to 300 [DeviceA-mst-region] quit \# 在DeviceB上配置域和实例。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] stp region-configuration [DeviceB-mst-region] region-name RG1 [DeviceB-mst-region] instance 1 vlan 2 to 100 [DeviceB-mst-region] instance 2 vlan 101 to 200 [DeviceB-mst-region] instance 3 vlan 201 to 300 [DeviceB-mst-region] quit \# 在DeviceC~DeviceH上配置域和实例。以DeviceC为例，DeviceD~DeviceH配置类似。
<HUAWEI> system-view [HUAWEI] sysname DeviceC [DeviceC] stp region-configuration [DeviceC-mst-region] region-name RG1 [DeviceC-mst-region] instance 1 vlan 2 to 100 [DeviceC-mst-region] quit步骤 2 在 DeviceA 和 DeviceB 上启用 MSTP 。
缺省情况下，设备上生成树协议处于使能状态，无需操作。在系统视图下执行命令stp enable可以启用STP/RSTP/MSTP功能。

\# 在DeviceA上启用MSTP。
[DeviceA] stp enable \# 在DeviceB上启用MSTP。
[DeviceB] stp enable \# 在DeviceC上启用MSTP。以DeviceC为例，DeviceD~DeviceH配置类似。
[DeviceC] stp enable步骤3 在设备上创建MSTP多进程并将端口加入到相应的进程。
\# 在DeviceA上创建进程1和进程2；将DeviceA的端口10GE1/0/3和10GE1/0/4加入到进程1，端口10GE1/0/2加入到进程2。
[DeviceA] stp process 1 [DeviceA-mst-process-1] quit [DeviceA] stp process 2 [DeviceA-mst-process-2] quit [DeviceA] interface 10ge 1/0/4 [DeviceA-10GE1/0/4] portswitch [DeviceA-10GE1/0/4] stp binding process 1 [DeviceA-10GE1/0/4] quit [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] stp binding process 1 [DeviceA-10GE1/0/3] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] stp binding process 2 [DeviceA-10GE1/0/2] quit \# 在DeviceB上创建进程2和进程3；将DeviceB的端口10GE1/0/3和10GE1/0/4加入到进程3，端口10GE1/0/2加入到进程2。
[DeviceB] stp process 2 [DeviceB-mst-process-2] quit [DeviceB] stp process 3 [DeviceB-mst-process-3] quit [DeviceB] interface 10ge 1/0/4 [DeviceB-10GE1/0/4] portswitch [DeviceB-10GE1/0/4] stp binding process 3 [DeviceB-10GE1/0/4] quit [DeviceB] interface 10ge 1/0/3 [DeviceB-10GE1/0/3] portswitch [DeviceB-10GE1/0/3] stp binding process 3 [DeviceB-10GE1/0/3] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] portswitch [DeviceB-10GE1/0/2] stp binding process 2 [DeviceB-10GE1/0/2] quit \# 在DeviceC~DeviceH上创建进程。以DeviceC为例，创建进程1，将端口10GE1/0/1和10GE1/0/2加入到进程1，DeviceD~DeviceH配置类似。
[DeviceC] stp process 1 [DeviceC-mst-process-1] quit [DeviceC] interface 10ge 1/0/1 [DeviceC-10GE1/0/3] stp binding process 1 [DeviceC-10GE1/0/3] quit [DeviceC] interface 10ge 1/0/2 [DeviceC-10GE1/0/2] portswitch [DeviceC-10GE1/0/2] stp binding process 1 [DeviceC-10GE1/0/2] quit步骤4 配置共享链路。
\# 配置DeviceA。

[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] stp binding process 2 link-share [DeviceA-10GE1/0/1] quit \# 配置DeviceB。
[DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] portswitch [DeviceB-10GE1/0/1] stp binding process 2 link-share [DeviceB-10GE1/0/1] quit步骤5 启动进程的MSTP功能。
\# 配置DeviceA。
[DeviceA] stp process 1 [DeviceA-mst-process-1] stp enable [DeviceA-mst-process-1] quit [DeviceA] stp process 2 [DeviceA-mst-process-2] stp enable [DeviceA-mst-process-2] quit \# 配置DeviceB。
[DeviceB] stp process 3 [DeviceB-mst-process-3] stp enable [DeviceB-mst-process-3] quit [DeviceB] stp process 2 [DeviceB-mst-process-2] stp enable [DeviceB-mst-process-2] quit \# 配置DeviceC。DeviceD~DeviceH配置类似。
[DeviceC] stp process 1 [DeviceC-mst-process-1] stp enable [DeviceC-mst-process-1] quit步骤6 配置其他功能。
\# 在DeviceA上配置优先级和根保护。
[DeviceA] stp process 1 [DeviceA-mst-process-1] stp instance 0 root primary [DeviceA-mst-process-1] stp instance 1 root primary [DeviceA-mst-process-1] quit [DeviceA] stp process 2 [DeviceA-mst-process-2] stp instance 0 root primary [DeviceA-mst-process-2] stp instance 2 root primary [DeviceA-mst-process-2] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] stp root-protection [DeviceA-10GE1/0/2] quit \# 在DeviceB上配置优先级和根保护。
[DeviceB] stp process 3 [DeviceB-mst-process-3] stp instance 0 root primary [DeviceB-mst-process-3] stp instance 3 root primary [DeviceB-mst-process-3] quit [DeviceB] stp process 2 [DeviceB-mst-process-2] stp instance 0 root secondary [DeviceB-mst-process-2] stp instance 2 root secondary [DeviceB-mst-process-2] quit [DeviceB] interface 10ge 1/0/2 [DeviceB] portswitch [DeviceB-10GE1/0/2] stp root-protection [DeviceB-10GE1/0/2] quit

说明
● 每个环中都要确保下游CE设备的MSTP优先级低于PE设备。缺省情况下，设备在指定生成树中的优先级是32768，CE设备无需配置。
● 在双接环接入时，建议DeviceA和DeviceB分别作为不同实例的主备根。
\# 在DeviceA上配置MSTP多进程的共享链路保护功能。
[DeviceA] stp process 2 [DeviceA-mst-process-2] stp link-share-protection [DeviceA-mst-process-2] quit \# 在DeviceB上配置MSTP多进程的共享链路保护功能。
[DeviceB] stp process 2 [DeviceB-mst-process-2] stp link-share-protection [DeviceB-mst-process-2] quit步骤7 创建VLAN，并将端口加入到VLAN中。
\# 在DeviceA上创建VLAN2～VLAN200，并将端口10GE1/0/3和端口10GE1/0/4加入到VLAN2～VLAN100中，将端口10GE1/0/1和端口10GE1/0/2加入到VLAN101～VLAN200 中。
[DeviceA] vlan batch 2 to 200 [DeviceA] interface 10ge 1/0/3 [DeviceB-10GE1/0/3] portswitch [DeviceA-10GE1/0/3] port link-type trunk [DeviceA-10GE1/0/3] port trunk allow-pass vlan 2 to 100 [DeviceA-10GE1/0/3] quit [DeviceA] interface 10ge 1/0/4 [DeviceA-10GE1/0/4] portswitch [DeviceA-10GE1/0/4] port link-type trunk [DeviceA-10GE1/0/4] port trunk allow-pass vlan 2 to 100 [DeviceA-10GE1/0/4] quit [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type trunk [DeviceA-10GE1/0/1] port trunk allow-pass vlan 101 to 200 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type trunk [DeviceA-10GE1/0/2] port trunk allow-pass vlan 101 to 200 [DeviceA-10GE1/0/2] quit \# 在DeviceB上创建VLAN101～VLAN300，并将端口10GE1/0/3和端口10GE1/0/4加入到VLAN201～VLAN300中，将端口10GE1/0/1和端口10GE1/0/2加入到VLAN101～VLAN200中。
[DeviceB] vlan batch 101 to 300 [DeviceB] interface 10ge 1/0/3 [DeviceB-10GE1/0/3] portswitch [DeviceB-10GE1/0/3] port link-type trunk [DeviceB-10GE1/0/3] port trunk allow-pass vlan 201 to 300 [DeviceB-10GE1/0/3] quit [DeviceB] interface 10ge 1/0/4 [DeviceB-10GE1/0/4] portswitch [DeviceB-10GE1/0/4] port link-type trunk [DeviceB-10GE1/0/4] port trunk allow-pass vlan 201 to 300 [DeviceB-10GE1/0/4] quit [DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] portswitch [DeviceB-10GE1/0/1] port link-type trunk [DeviceB-10GE1/0/1] port trunk allow-pass vlan 101 to 200 [DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2

[DeviceB-10GE1/0/2] portswitch [DeviceB-10GE1/0/2] port link-type trunk [DeviceB-10GE1/0/2] port trunk allow-pass vlan 101 to 200 [DeviceB-10GE1/0/2] quit \# 配置DeviceC，在DeviceC上创建VLAN2～VLAN100，并将端口10GE1/0/1和端口10GE1/0/2加入到VLAN2～VLAN100中，DeviceD~DeviceH配置类似。
[DeviceC] vlan batch 2 to 100 [DeviceC] interface 10ge 1/0/1 [DeviceC-10GE1/0/3] portswitch [DeviceC-10GE1/0/3] port link-type trunk [DeviceC-10GE1/0/3] port trunk allow-pass vlan 2 to 100 [DeviceC-10GE1/0/3] quit [DeviceC] interface 10ge 1/0/2 [DeviceC-10GE1/0/2] portswitch [DeviceC-10GE1/0/3] port link-type trunk [DeviceC-10GE1/0/3] port trunk allow-pass vlan 2 to 100 [DeviceC-10GE1/0/2] quit
----结束检查配置结果
● 在DeviceA上执行display stp interface brief命令，可以看到：
\# 端口10GE1/0/4在MSTP进程1的CIST和实例1中为指定端口。
[DeviceA] display stp process 1 interface 10ge 1/0/4 brief MSTID Port Role STP State Protection 0 10GE1/0/4 DESI FORWARDING NONE 1 10GE1/0/4 DESI FORWARDING NONE \# 端口10GE1/0/2在MSTP进程2的CIST和实例2中为指定端口。
[DeviceA] display stp process 2 interface 10ge 1/0/2 brief MSTID Port Role STP State Protection 0 10GE1/0/2 DESI FORWARDING ROOT 2 10GE1/0/2 DESI FORWARDING ROOT
● 在DeviceB上执行display stp interface brief命令，可以看到：
\# 端口10GE1/0/4在MSTP进程3的CIST和实例3中为指定端口。
[DeviceB] display stp process 3 interface 10ge 1/0/4 brief MSTID Port Role STP State Protection 0 10GE1/0/4 DESI FORWARDING NONE 3 10GE1/0/4 DESI FORWARDING NONE \# 端口10GE1/0/2在MSTP进程2的CIST和实例2中为指定端口。
[DeviceB] display stp process 2 interface 10ge 1/0/2 brief MSTID Port Role STP State Protection 0 10GE1/0/2 DESI FORWARDING ROOT 2 10GE1/0/2 DESI FORWARDING ROOT配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 2 to 200 \# stp enable \# stp region-configuration region-name RG1 instance 1 vlan 2 to 100 instance 2 vlan 101 to 200 instance 3 vlan 201 to 300 \#

stp process 1 stp instance 0 root primary stp instance 1 root primary stp enable stp process 2 stp instance 0 root primary stp instance 2 root primary stp link-share-protection stp enable \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 101 to 200 stp binding process 2 link-share \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 101 to 200 stp binding process 2 stp root-protection \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 2 to 100 stp binding process 1 \# interface 10GE1/0/4 port link-type trunk port trunk allow-pass vlan 2 to 100 stp binding process 1 \# return
● DeviceB \# sysname DeviceB \# vlan batch 101 to 300 \# stp enable \# stp region-configuration region-name RG1 instance 1 vlan 2 to 100 instance 2 vlan 101 to 200 instance 3 vlan 201 to 300 \# stp process 2 stp instance 0 root secondary stp instance 2 root secondary stp link-share-protection stp enable stp process 3 stp instance 0 root primary stp instance 3 root primary stp enable \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 101 to 200 stp binding process 2 link-share \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 101 to 200 stp binding process 2 stp root-protection \# interface 10GE1/0/3 port link-type trunk

port trunk allow-pass vlan 201 to 300 stp binding process 3 \# interface 10GE1/0/4 port link-type trunk port trunk allow-pass vlan 201 to 300 stp binding process 3 \# return
● DeviceC（DeviceD~DeviceH配置类似）
\# sysname DeviceC \# vlan batch 2 to 100 \# stp enable \# stp region-configuration region-name RG1 instance 1 vlan 2 to 100 \# stp process 1 stp enable \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 2 to 100 stp binding process 1 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2 to 100 stp binding process 1 \# return

#### 7.12.5 举例：配置MSTP+VRRP组合组网

组网需求如图7-32所示，主机通过DeviceC接入网络，DeviceC通过双上行连接DeviceA和DeviceB来接入Internet。由于接入备份的需要，用户部署了冗余链路。冗余备份链路的存在导致出现环网，可能会引起广播风暴和MAC地址表项被破坏。用户希望在存在冗余备份链路的同时消除网络中的环路，在一条上行链路断开的时候，流量能切换到另外一条上行链路转发，还能合理利用网络带宽。
此时可以在网络中部署MSTP解决环路问题。MSTP可阻塞二层网络中的冗余链路，将网络修剪成树状，达到消除环路的目的。同时在 DeviceA 和 DeviceB 上配置 VRRP ，HostA以DeviceA为默认网关接入Internet，DeviceB作为备份网关；HostB以DeviceB为默认网关接入Internet，DeviceA作为备份网关，以实现可靠性及流量的负载分担。
图 7-32 配置 MSTP+VRRP 组合组网图说明本例中interface1、interface2、interface3和interface4分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3和10GE1/0/4。

| 设备 | 接口 | 对应的VLANIF | IP地址 |
|---|---|---|---|
| DeviceA | interface1和 interface2 | VLANIF2 | 10.1.2.102/24 |
|  | interface1和 interface2 | VLANIF3 | 10.1.3.102/24 |
|  | interface3 | VLANIF4 | 10.1.4.102/24 |
| DeviceB | interface1和 interface2 | VLANIF2 | 10.1.2.103/24 |
|  | interface1和 interface2 | VLANIF3 | 10.1.3.103/24 |
|  | interface3 | VLANIF5 | 10.1.5.103/24 |

配置思路采用以下思路配置：

1. 配置设备的二层转发功能。
2. 在处于环形网络中的设备上配置MSTP基本功能，包括：
a. 配置MST域并创建多实例，配置VLAN2映射到MSTI1，VLAN3映射到
MSTI2，实现流量的负载分担。
b. 在MST域内，配置各实例的根桥与备份根桥。
c. 配置各实例中某端口的路径开销值，实现将该端口阻塞。
d. 使能MSTP，实现破除环路，包括：
▪
设备全局使能MSTP。
▪
除与终端设备相连的端口外，其他端口使能MSTP。
说明
与终端相连的端口不用参与MSTP计算，建议将其设置为边缘端口。
3. 配置保护功能，实现对设备或链路的保护。例如：在各实例的根桥设备指定端口
配置根保护功能。
4. 配置各设备端口IP地址及路由协议，使各设备间网络层连通。
5. 在DeviceA和DeviceB上创建VRRP备份组1和VRRP备份组2，在备份组1中，配置
DeviceA为Master设备，DeviceB为Backup设备；在备份组2中，配置DeviceB为
Master设备，DeviceA为Backup设备，实现流量的负载均衡。
操作步骤
步骤1 配置处于环网中的设备的二层转发功能
● 在设备DeviceA、DeviceB、DeviceC上创建VLAN2～3
\# 在DeviceA上创建VLAN2～3。
<HUAWEI> system-view
[HUAWEI] sysname DeviceA
[DeviceA] vlan batch 2 to 3
\# 在DeviceB上创建VLAN2～3。
<HUAWEI> system-view
[HUAWEI] sysname DeviceB
[DeviceB] vlan batch 2 to 3
\# 在DeviceC上创建VLAN2～3。
<HUAWEI> system-view
[HUAWEI] sysname DeviceC
[DeviceC] vlan batch 2 to 3
● 将设备上相应的端口加入VLAN
\# 将DeviceA端口10GE1/0/1加入VLAN。
[DeviceA] interface 10ge1/0/1
[DeviceA-10GE1/0/1] portswitch
[DeviceA-10GE1/0/1] port link-type trunk
[DeviceA-10GE1/0/1] port trunk allow-pass vlan 2 to 3
[DeviceA-10GE1/0/1] quit
\# 将DeviceA端口10GE1/0/2加入VLAN。
[DeviceA] interface 10ge1/0/2
[DeviceA-10GE1/0/2] portswitch
[DeviceA-10GE1/0/2] port link-type trunk
[DeviceA-10GE1/0/2] port trunk allow-pass vlan 2 to 3
[DeviceA-10GE1/0/2] quit
\# 将DeviceB端口10GE1/0/1加入VLAN。

[DeviceB] interface 10ge1/0/1 [DeviceB-10GE1/0/1] portswitch [DeviceB-10GE1/0/1] port link-type trunk [DeviceB-10GE1/0/1] port trunk allow-pass vlan 2 to 3 [DeviceB-10GE1/0/1] quit \# 将DeviceB端口10GE1/0/2加入VLAN。
[DeviceB] interface 10ge1/0/2 [DeviceB-10GE1/0/2] portswitch [DeviceB-10GE1/0/2] port link-type trunk [DeviceB-10GE1/0/2] port trunk allow-pass vlan 2 to 3 [DeviceB-10GE1/0/2] quit \# 将DeviceC端口10GE1/0/1加入VLAN。
[DeviceC] interface 10ge1/0/1 [DeviceC-10GE1/0/1] portswitch [DeviceC-10GE1/0/1] port link-type trunk [DeviceC-10GE1/0/1] port trunk allow-pass vlan 2 to 3 [DeviceC-10GE1/0/1] quit \# 将DeviceC端口10GE1/0/2加入VLAN。
[DeviceC] interface 10ge1/0/2 [DeviceC-10GE1/0/2] portswitch [DeviceC-10GE1/0/2] port link-type access [DeviceC-10GE1/0/2] port default vlan 2 [DeviceC-10GE1/0/2] quit \# 将DeviceC端口10GE1/0/3加入VLAN。
[DeviceC] interface 10ge1/0/3 [DeviceC-10GE1/0/3] portswitch [DeviceC-10GE1/0/3] port link-type access [DeviceC-10GE1/0/3] port default vlan 3 [DeviceC-10GE1/0/3] quit \# 将DeviceC端口10GE1/0/4加入VLAN。
[DeviceC] interface 10ge1/0/4 [DeviceC-10GE1/0/4] portswitch [DeviceC-10GE1/0/4] port link-type trunk [DeviceC-10GE1/0/4] port trunk allow-pass vlan 2 to 3 [DeviceC-10GE1/0/4] quit步骤2 配置MSTP基本功能
1. 配置DeviceA、DeviceB、DeviceC到域名为RG1的域内，创建实例MSTI1和实例MSTI2 \# 配置DeviceA的MST域。
[DeviceA] stp region-configuration [DeviceA-mst-region] region-name RG1 [DeviceA-mst-region] instance 1 vlan 2 [DeviceA-mst-region] instance 2 vlan 3 [DeviceA-mst-region] quit \# 配置DeviceB的MST域。
[DeviceB] stp region-configuration [DeviceB-mst-region] region-name RG1 [DeviceB-mst-region] instance 1 vlan 2 [DeviceB-mst-region] instance 2 vlan 3 [DeviceB-mst-region] quit \# 配置DeviceC的MST域。
[DeviceC] stp region-configuration [DeviceC-mst-region] region-name RG1 [DeviceC-mst-region] instance 1 vlan 2 [DeviceC-mst-region] instance 2 vlan 3 [DeviceC-mst-region] quit
2. 在域RG1内，配置MSTI1与MSTI2的根桥与备份根桥

– 配置MSTI1的根桥与备份根桥
\# 配置DeviceA为MSTI1的根桥。
[DeviceA] stp instance 1 root primary
\# 配置DeviceB为MSTI1的备份根桥。
[DeviceB] stp instance 1 root secondary
– 配置MSTI2的根桥与备份根桥
\# 配置DeviceB为MSTI2的根桥。
[DeviceB] stp instance 2 root primary
\# 配置DeviceA为MSTI2的备份根桥。
[DeviceA] stp instance 2 root secondary
配置实例MSTI1和MSTI2中将要被阻塞端口的路径开销值大于缺省值
3.
说明
– 端口路径开销值取值范围由路径开销计算方法决定，这里选择使用华为计算方法为例，
配置实例MSTI1和MSTI2中将被阻塞端口的路径开销值为20000。
– 同一网络内所有设备的端口路径开销应使用相同的计算方法。
\# 配置DeviceA的端口路径开销计算方法为华为计算方法。
[DeviceA] stp pathcost-standard legacy
\# 配置DeviceB的端口路径开销计算方法为华为计算方法。
[DeviceB] stp pathcost-standard legacy
\# 配置DeviceC的端口路径开销计算方法为华为计算方法，将端口10GE1/0/1在实
例MSTI2中的路径开销值配置为20000，将端口10GE1/0/4在实例MSTI1中的路径
开销值配置为20000。
[DeviceC] stp pathcost-standard legacy
[DeviceC] interface 10ge1/0/1
[DeviceC-10GE1/0/1] stp instance 2 cost 20000
[DeviceC-10GE1/0/1] quit
[DeviceC] interface 10ge1/0/4
[DeviceC-10GE1/0/4] stp instance 1 cost 20000
[DeviceC-10GE1/0/4] quit
4. 使能MSTP，实现破除环路
设备全局使能MSTP
–
\# 在DeviceA上启动MSTP。
[DeviceA] stp enable
\# 在DeviceB上启动MSTP。
[DeviceB] stp enable
\# 在DeviceC上启动MSTP。
[DeviceC] stp enable
– 将与Host相连的端口设置为边缘端口
\# 配置DeviceC端口的10GE1/0/2和10GE1/0/3为边缘端口。
[DeviceC] interface 10ge1/0/2
[DeviceC-10GE1/0/2] stp edged-port enable
[DeviceC-10GE1/0/2] quit
[DeviceC] interface 10ge1/0/3
[DeviceC-10GE1/0/3] stp edged-port enable
[DeviceC-10GE1/0/3] quit
（可选）配置DeviceC的BPDU保护功能。
[DeviceC] stp bpdu-protection

– 将与Network相连的端口设置为边缘端口
\# 配置DeviceA端口10GE1/0/3为边缘端口。
[DeviceA] interface 10ge1/0/3
[DeviceA-10GE1/0/3] stp edged-port enable
[DeviceA-10GE1/0/3] quit
（可选）配置DeviceA的BPDU保护功能。
[DeviceA] stp bpdu-protection
\# 配置DeviceB端口10GE1/0/3为边缘端口。
[DeviceB] interface 10ge1/0/3
[DeviceB-10GE1/0/3] stp edged-port enable
[DeviceB-10GE1/0/3] quit
（可选）配置DeviceB的BPDU保护功能。
[DeviceB] stp bpdu-protection
说明
如果与边缘端口相连的是使能了STP功能的网络设备，配置BPDU保护功能后，如果边
缘端口收到BPDU报文，边缘端口将会被shutdown，边缘端口属性不变。
步骤3 配置保护功能，如在各实例的根桥设备的指定端口配置根保护功能
\# 在DeviceA端口10GE1/0/1上启动根保护。
[DeviceA] interface 10ge1/0/1
[DeviceA-10GE1/0/1] stp root-protection
[DeviceA-10GE1/0/1] quit
\# 在DeviceB端口10GE1/0/1上启动根保护。
[DeviceB] interface 10ge1/0/1
[DeviceB-10GE1/0/1] stp root-protection
[DeviceB-10GE1/0/1] quit
步骤4 验证配置结果
经过以上配置，在网络计算稳定后，执行以下操作，验证配置结果。
说明
本配置举例以实例1和实例2为例，因此不用关注实例0中端口的状态。
在DeviceA上执行display brief命令，查看端口状态和端口的保护类型，结果如
\# stp
下：
[DeviceA] display stp brief
MSTID Port Role STP State Protection
0 10GE1/0/1 DESI FORWARDING ROOT
0 10GE1/0/2 DESI FORWARDING NONE
1 10GE1/0/1 DESI FORWARDING ROOT
1 10GE1/0/2 DESI FORWARDING NONE
2 10GE1/0/1 DESI FORWARDING ROOT
2 10GE1/0/2 ROOT FORWARDING NONE
在MSTI1中，由于DeviceA是根桥，DeviceA的端口10GE1/0/1和10GE1/0/2成为指定端
口。在MSTI2中，DeviceA的端口10GE1/0/1成为指定端口，端口10GE1/0/2成为根端
口。
\# 在DeviceB上执行display stp brief命令，结果如下：
[DeviceB] display stp brief
MSTID Port Role STP State Protection
0 10GE1/0/1 DESI FORWARDING ROOT
0 10GE1/0/2 ROOT FORWARDING NONE

1 10GE1/0/1 DESI FORWARDING ROOT 1 10GE1/0/2 ROOT FORWARDING NONE 2 10GE1/0/1 DESI FORWARDING ROOT 2 10GE1/0/2 DESI FORWARDING NONE在MSTI2中，由于DeviceB是根桥，端口10GE1/0/1和10GE1/0/2在MSTI2中成为指定端口。在MSTI1中，DeviceB的端口10GE1/0/1成为指定端口，端口10GE1/0/2成为根端口。
\# 在DeviceC上执行display stp interface brief命令，结果如下：
[DeviceC] display stp interface 10ge1/0/1 brief MSTID Port Role STP State Protection 0 10GE1/0/1 ROOT FORWARDING NONE 1 10GE1/0/1 ROOT FORWARDING NONE 2 10GE1/0/1 ALTE DISCARDING NONE [DeviceC] display stp interface 10ge1/0/4 brief MSTID Port Role STP State Protection 0 10GE1/0/4 ALTE DISCARDING NONE 1 10GE1/0/4 ALTE DISCARDING NONE 2 10GE1/0/4 ROOT FORWARDING NONE DeviceC的端口10GE1/0/1在MSTI1中为根端口，在MSTI2中被阻塞。DeviceC的另一个端口10GE1/0/4，在MSTI1中被阻塞，在MSTI2中为根端口。
步骤5 配置设备间的网络互连\# 配置设备各端口的IP地址，以DeviceA为例。DeviceB的配置与DeviceA类似，详见配置文件。
[DeviceA] vlan batch 4 [DeviceA] interface 10ge1/0/3 [DeviceA-10GE1/0/3] port link-type trunk [DeviceA-10GE1/0/3] port trunk allow-pass vlan 4 [DeviceA-10GE1/0/3] quit [DeviceA] interface vlanif 2 [DeviceA-Vlanif2] ip address 10.1.2.102 24 [DeviceA-Vlanif2] quit [DeviceA] interface vlanif 3 [DeviceA-Vlanif3] ip address 10.1.3.102 24 [DeviceA-Vlanif3] quit [DeviceA] interface vlanif 4 [DeviceA-Vlanif4] ip address 10.1.4.102 24 [DeviceA-Vlanif4] quit \# 配置DeviceA、DeviceB和Network间采用OSPF协议进行互连。以DeviceA为例，DeviceB的配置与DeviceA类似，详见配置文件。
[DeviceA] ospf 1 [DeviceA-ospf-1] area 0 [DeviceA-ospf-1-area-0.0.0.0] network 10.1.2.0 0.0.0.255 [DeviceA-ospf-1-area-0.0.0.0] network 10.1.3.0 0.0.0.255 [DeviceA-ospf-1-area-0.0.0.0] network 10.1.4.0 0.0.0.255 [DeviceA-ospf-1-area-0.0.0.0] quit [DeviceA-ospf-1] quit步骤6 配置VRRP备份组\# 在DeviceA和DeviceB上创建VRRP备份组1，配置DeviceA的优先级为120，抢占延时为20秒，作为Master设备。
[DeviceA] interface vlanif 2 [DeviceA-Vlanif2] vrrp vrid 1 virtual-ip 10.1.2.100 [DeviceA-Vlanif2] vrrp vrid 1 priority 120 [DeviceA-Vlanif2] vrrp vrid 1 preempt timer delay 20 [DeviceA-Vlanif2] quit \# DeviceB的优先级为缺省值，作为Backup设备。

[DeviceB] interface vlanif 2 [DeviceB-Vlanif2] vrrp vrid 1 virtual-ip 10.1.2.100 [DeviceB-Vlanif2] quit \# 在DeviceA和DeviceB上创建VRRP备份组2，配置DeviceB的优先级为120，抢占延时为20秒，作为Master设备。
[DeviceB] interface vlanif 3 [DeviceB-Vlanif3] vrrp vrid 2 virtual-ip 10.1.3.100 [DeviceB-Vlanif3] vrrp vrid 2 priority 120 [DeviceB-Vlanif3] vrrp vrid 2 preempt timer delay 20 [DeviceB-Vlanif3] quit \# DeviceA的优先级为缺省值，作为Backup设备。
[DeviceA] interface vlanif 3 [DeviceA-Vlanif3] vrrp vrid 2 virtual-ip 10.1.3.100 [DeviceA-Vlanif3] quit \# 配置主机HostA的缺省网关为备份组1的虚拟IP地址10.1.2.100，配置主机HostB的缺省网关为备份组2的虚拟IP地址10.1.3.100。
步骤7 验证配置结果\# 完成上述配置后，在 DeviceA 上执行 display vrrp 命令，可以看到 DeviceA 在备份组 1中作为Master设备，在备份组2中作为Backup设备。
[DeviceA] display vrrp Vlanif2 | Virtual Router 1 State : Master Virtual IP : 10.1.2.100 Master IP : 10.1.2.102 PriorityRun : 120 PriorityConfig : 120 MasterPriority : 120 Preempt : YES Delay Time : 20 s TimerRun : 1 s TimerConfig : 1 s Auth type : NONE Virtual MAC : 00e0-fc12-3456 Check TTL : YES Config type : normal-vrrp Backup-forward : disabled Create time : 2021-05-11 11:39:18 Last change time : 2021-05-26 11:38:58 Vlanif3 | Virtual Router 2 State : Backup Virtual IP : 10.1.3.100 Master IP : 10.1.3.103 PriorityRun : 100 PriorityConfig : 100 MasterPriority : 120 Preempt : YES Delay Time : 0 s TimerRun : 1 s TimerConfig : 1 s Auth type : NONE Virtual MAC : 00e0-fc12-3457 Check TTL : YES Config type : normal-vrrp Backup-forward : disabled Create time : 2021-05-11 11:40:18 Last change time : 2021-05-26 11:48:58 \# 在 DeviceB 上执行 display vrrp 命令，可以看到 DeviceB 在备份组 1 中作为 Backup 设备，在备份组2中作为Master设备。
[DeviceB] display vrrp Vlanif2 | Virtual Router 1

State : Backup Virtual IP : 10.1.2.100 Master IP : 10.1.2.102 PriorityRun : 100 PriorityConfig : 100 MasterPriority : 120 Preempt : YES Delay Time : 0 s TimerRun : 1 s TimerConfig : 1 s Auth type : NONE Virtual MAC : 00e0-fc12-3456 Check TTL : YES Config type : normal-vrrp Backup-forward : disabled Create time : 2021-05-11 11:39:18 Last change time : 2021-05-26 11:38:58 Vlanif3 | Virtual Router 2 State : Master Virtual IP : 10.1.3.100 Master IP : 10.1.3.103 PriorityRun : 120 PriorityConfig : 120 MasterPriority : 120 Preempt : YES Delay Time : 20 s TimerRun : 1 s TimerConfig : 1 s Auth type : NONE Virtual MAC : 00e0-fc12-3457 Check TTL : YES Config type : normal-vrrp Backup-forward : disabled Create time : 2021-05-11 11:40:18 Last change time : 2021-05-26 11:48:58
----结束配置脚本
● DeviceA的配置文件\# sysname DeviceA \# vlan batch 2 to 4 \# stp instance 1 root primary stp instance 2 root secondary stp bpdu-protection stp pathcost-standard legacy \# stp region-configuration region-name RG1 instance 1 vlan 2 instance 2 vlan 3 \# interface Vlanif2 ip address 10.1.2.102 255.255.255.0 vrrp vrid 1 virtual-ip 10.1.2.100 vrrp vrid 1 priority 120 vrrp vrid 1 preempt timer delay 20 \# interface Vlanif3 ip address 10.1.3.102 255.255.255.0 vrrp vrid 2 virtual-ip 10.1.3.100 \# interface Vlanif4 ip address 10.1.4.102 255.255.255.0 \#

interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 2 to 3 stp root-protection \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2 to 3 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 4 stp edged-port enable \# ospf 1 area 0.0.0.0 network 10.1.2.0 0.0.0.255 network 10.1.3.0 0.0.0.255 network 10.1.4.0 0.0.0.255 \# return
● DeviceB的配置文件\# sysname DeviceB \# vlan batch 2 to 3 5 \# stp instance 1 root secondary stp instance 2 root primary stp bpdu-protection stp pathcost-standard legacy \# stp region-configuration region-name RG1 instance 1 vlan 2 instance 2 vlan 3 \# interface Vlanif2 ip address 10.1.2.103 255.255.255.0 vrrp vrid 1 virtual-ip 10.1.2.100 \# interface Vlanif3 ip address 10.1.3.103 255.255.255.0 vrrp vrid 2 virtual-ip 10.1.3.100 vrrp vrid 2 priority 120 vrrp vrid 2 preempt timer delay 20 \# interface Vlanif5 ip address 10.1.5.103 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 2 to 3 stp root-protection \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2 to 3 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 5 stp edged-port enable \# ospf 1 area 0.0.0.0 network 10.1.2.0 0.0.0.255 network 10.1.3.0 0.0.0.255 network 10.1.5.0 0.0.0.255

\# return
● DeviceC的配置文件\# sysname DeviceC \# vlan batch 2 to 3 \# stp bpdu-protection stp pathcost-standard legacy \# stp region-configuration region-name RG1 instance 1 vlan 2 instance 2 vlan 3 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 2 to 3 stp instance 2 cost 20000 \# interface 10GE1/0/2 port link-type access port default vlan 2 stp edged-port enable \# interface 10GE1/0/3 port link-type access port default vlan 3 stp edged-port enable \# interface 10GE1/0/4 port link-type trunk port trunk allow-pass vlan 2 to 3 stp instance 1 cost 20000 \# return

#### 7.12.6 举例：配置CE通过MSTP双归接入VPLS

组网需求说明该配置仅S6780-H、S6750-H、S6750E-S、S6750-S、S6730E-H-V2、S6730-S-V2、S6730-H- V2、S5755-H、S5732-H-V2系列支持。
如图7-33所示，CE双归接入PE设备，PE之间建立VPLS全连接。CE与PE之间运行MSTP协议。正常情况下流量沿主用链路转发，当主用链路发生故障时流量切换到备用链路上。
图 7-33 配置 CE 通过 MSTP 双归接入 VPLS 组网图说明本例中interface1、interface2、interface3、interface4分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3、10GE1/0/4。

表 7-20 数据规划

| 设备 | 接口 | 对应的三层接口 | IP地址 |
|---|---|---|---|
| PE1 | 10GE1/0/1 | 10GE1/0/1.1 | - |
|  | 10GE1/0/2 | VLANIF 10 | 172.16.1.1/24 |
|  | 10GE1/0/3 | VLANIF 40 | 172.19.1.2/24 |
|  | Loopback1 | - | 1.1.1.1/32 |
| PE2 | 10GE1/0/1 | 10GE1/0/1.1 | - |
|  | 10GE1/0/2 | VLANIF 10 | 172.16.1.2/24 |
|  | 10GE1/0/3 | VLANIF 20 | 172.17.1.1/24 |
|  | Loopback1 | - | 2.2.2.2/32 |
| PE3 | 10GE1/0/1 | 10GE1/0/1.1 | - |
|  | 10GE1/0/2 | VLANIF 20 | 172.17.1.2/24 |
|  | 10GE1/0/3 | VLANIF 30 | 172.18.1.1/24 |
|  | Loopback1 | - | 3.3.3.3/32 |
| PE4 | 10GE1/0/1 | 10GE1/0/1.1 | - |
|  | 10GE1/0/2 | VLANIF 30 | 172.18.1.2/24 |
|  | 10GE1/0/3 | VLANIF 40 | 172.19.1.1/24 |
|  | Loopback1 | - | 4.4.4.4/32 |
| CE1 | 10GE1/0/1 | - | - |
|  | 10GE1/0/4 | - | - |
|  | 10GE1/0/2 | - | - |

| 设备 | 接口 | 对应的三层接口 | IP地址 |
|---|---|---|---|
| CE2 | 10GE1/0/1 | - | - |
|  | 10GE1/0/4 | - | - |
|  | 10GE1/0/2 | - | - |

配置思路采用如下思路配置CE通过MSTP双归接入VPLS：
1. 在骨干网上配置路由协议实现互通。
2. 在PE之间建立远端LDP会话。
3. PE间建立VPLS全连接。
4. 配置MSTP，PE1和PE2为主根，PE3和PE4为备份根。
操作步骤步骤1 按表7-20配置各端口所属的VLAN和VLANIF接口的IP地址。
说明避免将PE上AC侧和PW侧的物理端口加入相同的VLAN中，否则可能引起环路。
\# 配置CE1，要求CE1发送给PE1的报文带有一层VLAN Tag。
<HUAWEI> system-view [HUAWEI] sysname CE1 [CE1] vlan batch 100 [CE1] interface 10ge 1/0/1 [CE1-10GE1/0/1] port link-type trunk [CE1-10GE1/0/1] port trunk allow-pass vlan 100 [CE1-10GE1/0/1] quit [CE1] interface 10ge 1/0/4 [CE1-10GE1/0/4] port link-type trunk [CE1-10GE1/0/4] port trunk allow-pass vlan 100 [CE1-10GE1/0/4] quit [CE1] interface 10ge 1/0/2 [CE1-10GE1/0/2] port link-type access [CE1-10GE1/0/2] port default vlan 100 [CE1-10GE1/0/2] quit \# 配置 CE2 ，要求 CE2 发送给 PE2 的报文带有一层 VLAN Tag 。
<HUAWEI> system-view [HUAWEI] sysname CE2 [CE2] vlan batch 100 [CE2] interface 10ge 1/0/1 [CE2-10GE1/0/1] port link-type trunk [CE2-10GE1/0/1] port trunk allow-pass vlan 100 [CE2-10GE1/0/1] quit [CE2] interface 10ge 1/0/4 [CE2-10GE1/0/4] port link-type trunk [CE2-10GE1/0/4] port trunk allow-pass vlan 100 [CE2-10GE1/0/4] quit [CE2] interface 10ge 1/0/2 [CE2-10GE1/0/2] port link-type access [CE2-10GE1/0/2] port default vlan 100 [CE2-10GE1/0/2] quit \# 配置PE1。

<HUAWEI> system-view [HUAWEI] sysname PE1 [PE1] vlan batch 10 40 [PE1] interface 10ge 1/0/2 [PE1-10GE1/0/2] port link-type trunk [PE1-10GE1/0/2] port trunk allow-pass vlan 10 [PE1-10GE1/0/2] quit [PE1] interface 10ge 1/0/3 [PE1-10GE1/0/3] port link-type trunk [PE1-10GE1/0/3] port trunk allow-pass vlan 40 [PE1-10GE1/0/3] quit [PE1] interface vlanif 10 [PE1-Vlanif10] ip address 172.16.1.1 24 [PE1-Vlanif10] quit [PE1] interface vlanif 40 [PE1-Vlanif40] ip address 172.19.1.2 24 [PE1-Vlanif40] quit \# 配置PE2。
<HUAWEI> system-view [HUAWEI] sysname PE2 [PE2] vlan batch 10 20 [PE2] interface 10ge 1/0/2 [PE2-10GE1/0/2] port link-type trunk [PE2-10GE1/0/2] port trunk allow-pass vlan 10 [PE2-10GE1/0/2] quit [PE2] interface 10ge 1/0/3 [PE2-10GE1/0/3] port link-type trunk [PE2-10GE1/0/3] port trunk allow-pass vlan 20 [PE2-10GE1/0/3] quit [PE2] interface vlanif 10 [PE2-Vlanif10] ip address 172.16.1.2 24 [PE2-Vlanif10] quit [PE2] interface vlanif 20 [PE2-Vlanif20] ip address 172.17.1.1 24 [PE2-Vlanif20] quit \# 配置PE3。
<HUAWEI> system-view [HUAWEI] sysname PE3 [PE3] vlan batch 20 30 [PE3] interface 10ge 1/0/2 [PE3-10GE1/0/2] port link-type trunk [PE3-10GE1/0/2] port trunk allow-pass vlan 20 [PE3-10GE1/0/2] quit [PE3] interface 10ge 1/0/3 [PE3-10GE1/0/3] port link-type trunk [PE3-10GE1/0/3] port trunk allow-pass vlan 30 [PE3-10GE1/0/3] quit [PE3] interface vlanif 20 [PE3-Vlanif20] ip address 172.17.1.2 24 [PE3-Vlanif20] quit [PE3] interface vlanif 30 [PE3-Vlanif30] ip address 172.18.1.1 24 [PE3-Vlanif30] quit \# 配置PE4。
<HUAWEI> system-view [HUAWEI] sysname PE4 [PE4] vlan batch 30 40 [PE4] interface 10ge 1/0/2 [PE4-10GE1/0/2] port link-type trunk [PE4-10GE1/0/2] port trunk allow-pass vlan 30 [PE4-10GE1/0/2] quit [PE4] interface 10ge 1/0/3 [PE4-10GE1/0/3] port link-type trunk [PE4-10GE1/0/3] port trunk allow-pass vlan 40 [PE4-10GE1/0/3] quit

[PE4] interface vlanif 30 [PE4-Vlanif30] ip address 172.18.1.2 24 [PE4-Vlanif30] quit [PE4] interface vlanif 40 [PE4-Vlanif40] ip address 172.19.1.1 24 [PE4-Vlanif40] quit步骤2 配置IGP，本例中使用OSPF。配置OSPF时，注意需要发布PE1、PE2、PE3和PE4的32位Loopback端口地址（LSR-ID）。
\# 配置PE1。
[PE1] router id 1.1.1.1 [PE1] interface loopback 1 [PE1-LoopBack1] ip address 1.1.1.1 32 [PE1-LoopBack1] quit [PE1] ospf 1 [PE1-ospf-1] area 0 [PE1-ospf-1-area-0.0.0.0] network 1.1.1.1 0.0.0.0 [PE1-ospf-1-area-0.0.0.0] network 172.16.1.0 0.0.0.255 [PE1-ospf-1-area-0.0.0.0] network 172.19.1.0 0.0.0.255 [PE1-ospf-1-area-0.0.0.0] quit [PE1-ospf-1] quit \# 配置 PE2 。
[PE2] router id 2.2.2.2 [PE2] interface loopback 1 [PE2-LoopBack1] ip address 2.2.2.2 32 [PE2-LoopBack1] quit [PE2] ospf 1 [PE2-ospf-1] area 0 [PE2-ospf-1-area-0.0.0.0] network 2.2.2.2 0.0.0.0 [PE2-ospf-1-area-0.0.0.0] network 172.16.1.0 0.0.0.255 [PE2-ospf-1-area-0.0.0.0] network 172.17.1.0 0.0.0.255 [PE2-ospf-1-area-0.0.0.0] quit [PE2-ospf-1] quit \# 配置PE3。
[PE3] router id 3.3.3.3 [PE3] interface loopback 1 [PE3-LoopBack1] ip address 3.3.3.3 32 [PE3-LoopBack1] quit [PE3] ospf 1 [PE3-ospf-1] area 0 [PE3-ospf-1-area-0.0.0.0] network 3.3.3.3 0.0.0.0 [PE3-ospf-1-area-0.0.0.0] network 172.17.1.0 0.0.0.255 [PE3-ospf-1-area-0.0.0.0] network 172.18.1.0 0.0.0.255 [PE3-ospf-1-area-0.0.0.0] quit [PE3-ospf-1] quit \# 配置PE4。
[PE4] router id 4.4.4.4 [PE4] interface loopback 1 [PE4-LoopBack1] ip address 4.4.4.4 32 [PE4-LoopBack1] quit [PE4] ospf 1 [PE4-ospf-1] area 0 [PE4-ospf-1-area-0.0.0.0] network 4.4.4.4 0.0.0.0 [PE4-ospf-1-area-0.0.0.0] network 172.18.1.0 0.0.0.255 [PE4-ospf-1-area-0.0.0.0] network 172.19.1.0 0.0.0.255 [PE4-ospf-1-area-0.0.0.0] quit [PE4-ospf-1] quit \# 等待40秒后，在PE1、PE2、PE3和PE4上执行display ip routing-table命令可以看到已学到彼此的路由。以PE1的显示为例：

[PE1] display ip routing-table Route Flags: R - relay, D - download to fib, T - to vpn-instance
------------------------------------------------------------------------------ Routing Tables: Public Destinations : 12 Routes : 13 Destination/Mask Proto Pre Cost Flags NextHop Interface
1.1.1.1/32 Direct 0 0 D 127.0.0.1 LoopBack1
2.2.2.2/32 OSPF 10 1 D 172.16.1.2 Vlanif10
3.3.3.3/32 OSPF 10 2 D 172.19.1.1 Vlanif40 OSPF 10 2 D 172.16.1.2 Vlanif10
4.4.4.4/32 OSPF 10 1 D 172.19.1.1 Vlanif40
127.0.0.0/8 Direct 0 0 D 127.0.0.1 InLoopBack0
127.0.0.1/32 Direct 0 0 D 127.0.0.1 InLoopBack0
172.16.1.0/24 Direct 0 0 D 172.16.1.1 Vlanif10
172.16.1.1/32 Direct 0 0 D 127.0.0.1 Vlanif10
172.17.1.0/24 OSPF 10 2 D 172.16.1.2 Vlanif10
172.18.1.0/24 OSPF 10 2 D 172.19.1.1 Vlanif40
172.19.1.0/24 Direct 0 0 D 172.19.1.2 Vlanif40
172.19.1.2/32 Direct 0 0 D 127.0.0.1 Vlanif40步骤3 配置MPLS基本能力和LDP。
\# 配置 PE1 。
[PE1] mpls lsr-id 1.1.1.1 [PE1] mpls [PE1-mpls] quit [PE1] mpls ldp [PE1-mpls-ldp] quit [PE1] interface vlanif 10 [PE1-Vlanif10] mpls [PE1-Vlanif10] mpls ldp [PE1-Vlanif10] quit [PE1] interface vlanif 40 [PE1-Vlanif40] mpls [PE1-Vlanif40] mpls ldp [PE1-Vlanif40] quit \# 配置PE2。
[PE2] mpls lsr-id 2.2.2.2 [PE2] mpls [PE2-mpls] quit [PE2] mpls ldp [PE2-mpls-ldp] quit [PE2] interface vlanif 10 [PE2-Vlanif10] mpls [PE2-Vlanif10] mpls ldp [PE2-Vlanif10] quit [PE2] interface vlanif 20 [PE2-Vlanif20] mpls [PE2-Vlanif20] mpls ldp [PE2-Vlanif20] quit \# 配置PE3。
[PE3] mpls lsr-id 3.3.3.3 [PE3] mpls [PE3-mpls] quit [PE3] mpls ldp [PE3-mpls-ldp] quit [PE3] interface vlanif 20 [PE3-Vlanif20] mpls [PE3-Vlanif20] mpls ldp [PE3-Vlanif20] quit [PE3] interface vlanif 30 [PE3-Vlanif30] mpls

[PE3-Vlanif30] mpls ldp [PE3-Vlanif30] quit \# 配置PE4。
[PE4] mpls lsr-id 4.4.4.4 [PE4] mpls [PE4-mpls] quit [PE4] mpls ldp [PE4-mpls-ldp] quit [PE4] interface vlanif 30 [PE4-Vlanif30] mpls [PE4-Vlanif30] mpls ldp [PE4-Vlanif30] quit [PE4] interface vlanif 40 [PE4-Vlanif40] mpls [PE4-Vlanif40] mpls ldp [PE4-Vlanif40] quit步骤4 在PE之间建立远端LDP会话。
\# 配置PE1。
[PE1] mpls ldp remote-peer 3.3.3.3 [PE1-mpls-ldp-remote-3.3.3.3] remote-ip 3.3.3.3 [PE1-mpls-ldp-remote-3.3.3.3] quit \# 配置PE2。
[PE2] mpls ldp remote-peer 4.4.4.4 [PE2-mpls-ldp-remote-4.4.4.4] remote-ip 4.4.4.4 [PE2-mpls-ldp-remote-4.4.4.4] quit \# 配置PE3。
[PE3] mpls ldp remote-peer 1.1.1.1 [PE3-mpls-ldp-remote-1.1.1.1] remote-ip 1.1.1.1 [PE3-mpls-ldp-remote-1.1.1.1] quit \# 配置PE4。
[PE4] mpls ldp remote-peer 2.2.2.2 [PE4-mpls-ldp-remote-2.2.2.2] remote-ip 2.2.2.2 [PE4-mpls-ldp-remote-2.2.2.2] quit配置完成后，在PE上执行display mpls ldp session命令可以看到对等体的Status项为“Operational”，即远端对等体关系已建立。以PE1的显示为例：
[PE1] display mpls ldp session LDP Session(s) in Public Network Codes: LAM(Label Advertisement Mode), SsnAge Unit(DDDD:HH:MM)
A '*' before a session means the session is being deleted.
------------------------------------------------------------------------------ PeerID Status LAM SsnRole SsnAge KASent/Rcv
------------------------------------------------------------------------------
2.2.2.2:0 Operational DU Passive 0000:00:00 4/4
3.3.3.3:0 Operational DU Passive 0000:00:00 4/4
4.4.4.4:0 Operational DU Passive 0000:00:00 4/4
------------------------------------------------------------------------------ TOTAL: 3 session(s) Found.
步骤5 在PE上使能MPLS L2VPN。
\# 配置PE1。
[PE1] mpls l2vpn [PE1-l2vpn] quit \# 配置PE2。

[PE2] mpls l2vpn [PE2-l2vpn] quit \# 配置PE3。
[PE3] mpls l2vpn [PE3-l2vpn] quit \# 配置PE4。
[PE4] mpls l2vpn [PE4-l2vpn] quit步骤6 在PE上配置VSI。
\# 配置PE1。
[PE1] vsi a2 static [PE1-vsi-a2] pwsignal ldp [PE1-vsi-a2-ldp] vsi-id 2 [PE1-vsi-a2-ldp] peer 2.2.2.2 [PE1-vsi-a2-ldp] peer 3.3.3.3 [PE1-vsi-a2-ldp] peer 4.4.4.4 [PE1-vsi-a2-ldp] quit [PE1-vsi-a2] quit \# 配置PE2。
[PE2] vsi a2 static [PE2-vsi-a2] pwsignal ldp [PE2-vsi-a2-ldp] vsi-id 2 [PE2-vsi-a2-ldp] peer 1.1.1.1 [PE2-vsi-a2-ldp] peer 3.3.3.3 [PE2-vsi-a2-ldp] peer 4.4.4.4 [PE2-vsi-a2-ldp] quit [PE2-vsi-a2] quit \# 配置PE3。
[PE3] vsi a2 static [PE3-vsi-a2] pwsignal ldp [PE3-vsi-a2-ldp] vsi-id 2 [PE3-vsi-a2-ldp] peer 1.1.1.1 [PE3-vsi-a2-ldp] peer 2.2.2.2 [PE3-vsi-a2-ldp] peer 4.4.4.4 [PE3-vsi-a2-ldp] quit [PE3-vsi-a2] quit \# 配置PE4。
[PE4] vsi a2 static [PE4-vsi-a2] pwsignal ldp [PE4-vsi-a2-ldp] vsi-id 2 [PE4-vsi-a2-ldp] peer 1.1.1.1 [PE4-vsi-a2-ldp] peer 2.2.2.2 [PE4-vsi-a2-ldp] peer 3.3.3.3 [PE4-vsi-a2-ldp] quit [PE4-vsi-a2] quit步骤7 在PE上配置VSI与端口的绑定。
\# 配置PE1。
[PE1] interface 10ge 1/0/1 [PE1-10GE1/0/1] port link-type hybrid [PE1-10GE1/0/1] quit [PE1] interface 10ge 1/0/1.1 [PE1-10GE1/0/1.1] dot1q termination vid 100 [PE1-10GE1/0/1.1] l2 binding vsi a2 [PE1-10GE1/0/1.1] quit

\# 配置PE2。
[PE2] interface 10ge 1/0/1 [PE2-10GE1/0/1] port link-type hybrid [PE2-10GE1/0/1] quit [PE2] interface 10ge 1/0/1.1 [PE2-10GE1/0/1.1] dot1q termination vid 100 [PE2-10GE1/0/1.1] l2 binding vsi a2 [PE2-10GE1/0/1.1] quit \# 配置PE3。
[PE3] interface 10ge 1/0/1 [PE3-10GE1/0/1] port link-type hybrid [PE3-10GE1/0/1] quit [PE3] interface 10ge 1/0/1.1 [PE3-10GE1/0/1.1] dot1q termination vid 100 [PE3-10GE1/0/1.1] l2 binding vsi a2 [PE3-10GE1/0/1.1] quit \# 配置PE4。
[PE4] interface 10ge 1/0/1 [PE4-10GE1/0/1] port link-type hybrid [PE4-10GE1/0/1] quit [PE4] interface 10ge 1/0/1.1 [PE4-10GE1/0/1.1] dot1q termination vid 100 [PE4-10GE1/0/1.1] l2 binding vsi a2 [PE4-10GE1/0/1.1] quit步骤8 配置STP。
1. 配置域。
\# 配置PE1。
[PE1] stp region-configuration [PE1-mst-region] region-name RG1 [PE1-mst-region] quit \# 配置PE2。
[PE2] stp region-configuration [PE2-mst-region] region-name RG1 [PE2-mst-region] quit \# 配置PE3。
[PE3] stp region-configuration [PE3-mst-region] region-name RG1 [PE3-mst-region] quit \# 配置PE4。
[PE4] stp region-configuration [PE4-mst-region] region-name RG1 [PE4-mst-region] quit \# 配置CE1。
[CE1] stp region-configuration [CE1-mst-region] region-name RG1 [CE1-mst-region] quit \# 配置CE2。
[CE2] stp region-configuration [CE2-mst-region] region-name RG1 [CE2-mst-region] quit
2. 配置设备优先级，使得PE1、PE2为根桥，PE3、PE4为备根。
\# 配置PE1。
[PE1] stp instance 0 priority 0 \# 配置PE2。

[PE2] stp instance 0 priority 0 \# 配置PE3。
[PE3] stp instance 0 priority 4096 \# 配置PE4。
[PE4] stp instance 0 priority 4096
3. 配置CE与PE间使能MSTP与VPLS联动，并在备根上配置根保护。
\# 配置CE1。
[CE1] stp enable [CE1] interface 10ge 1/0/4 [CE1-10GE1/0/4] stp enable [CE1-10GE1/0/4] quit [CE1] interface 10ge 1/0/1 [CE1-10GE1/0/1] stp enable [CE1-10GE1/0/1] quit [CE1] interface 10ge 1/0/2 [CE1-10GE1/0/2] stp edged-port enable [CE1-10GE1/0/2] quit（可选）配置CE1的BPDU保护功能。
[CE1] stp bpdu-protection \# 配置 CE2 。
[CE2] stp enable [CE2] interface 10ge 1/0/4 [CE2-10GE1/0/4] stp enable [CE2-10GE1/0/4] quit [CE2] interface 10ge 1/0/1 [CE2-10GE1/0/1] stp enable [CE2-10GE1/0/1] quit [CE2] interface 10ge 1/0/2 [CE2-10GE1/0/2] stp edged-port enable [CE2-10GE1/0/2] quit（可选）配置CE2的BPDU保护功能。
[CE2] stp bpdu-protection说明如果与边缘端口相连的是使能了STP功能的网络设备，配置BPDU保护功能后，如果边缘端口收到BPDU报文，边缘端口将会被shutdown，边缘端口属性不变。
\# 配置PE1。
[PE1] stp enable [PE1] interface 10ge 1/0/1 [PE1-10GE1/0/1] stp vpls-subinterface enable [PE1-10GE1/0/1] stp enable [PE1-10GE1/0/1] quit [PE1] interface 10ge 1/0/2 [PE1-10GE1/0/2] stp disable [PE1-10GE1/0/2] quit [PE1] interface 10ge 1/0/3 [PE1-10GE1/0/3] stp disable [PE1-10GE1/0/3] quit \# 配置PE2。
[PE2] stp enable [PE2] interface 10ge 1/0/1 [PE2-10GE1/0/1] stp vpls-subinterface enable [PE2-10GE1/0/1] stp enable [PE2-10GE1/0/1] quit [PE2] interface 10ge 1/0/2 [PE2-10GE1/0/2] stp disable [PE2-10GE1/0/2] quit [PE2] interface 10ge 1/0/3

[PE2-10GE1/0/3] stp disable [PE2-10GE1/0/3] quit \# 配置PE3。
[PE3] stp enable [PE3] interface 10ge 1/0/1 [PE3-10GE1/0/1] stp vpls-subinterface enable [PE3-10GE1/0/1] stp root-protection [PE3-10GE1/0/1] stp enable [PE3-10GE1/0/1] quit [PE3] interface 10ge 1/0/2 [PE3-10GE1/0/2] stp disable [PE3-10GE1/0/2] quit [PE3] interface 10ge 1/0/3 [PE3-10GE1/0/3] stp disable [PE3-10GE1/0/3] quit \# 配置PE4。
[PE4] stp enable [PE4] interface 10ge 1/0/1 [PE4-10GE1/0/1] stp vpls-subinterface enable [PE4-10GE1/0/1] stp root-protection [PE4-10GE1/0/1] stp enable [PE4-10GE1/0/1] quit [PE4] interface 10ge 1/0/2 [PE4-10GE1/0/2] stp disable [PE4-10GE1/0/2] quit [PE4] interface 10ge 1/0/3 [PE4-10GE1/0/3] stp disable [PE4-10GE1/0/3] quit
----结束检查配置结果在PE上执行display vsi name a2 verbose命令，VSI状态为UP。
以PE1的显示为例：
[PE1] display vsi name a2 verbose
***VSI Name : a2 Administrator VSI : no Isolate Spoken : disable VSI Index : 0 PW Signaling : ldp Member Discovery Style : static PW MAC Learn Style : unqualify Encapsulation Type : vlan MTU : 1500 Diffserv Mode : uniform Mpls Exp : -- DomainId : 255 Domain Name :
Ignore AcState : disable P2P VSI : disable Create Time : 0 days, 20 hours, 29 minutes, 54 seconds VSI State : up VSI ID : 2
*Peer Router ID : 2.2.2.2 Negotiation-vc-id : 2 primary or secondary : primary ignore-standby-state : no VC Label : 4099 Peer Type : dynamic Session : up Tunnel ID : 0xd Broadcast Tunnel ID : 0xd

Broad BackupTunnel ID : 0x0 CKey : 2 NKey : 1 Stp Enable : 0 PwIndex : 0 Control Word : disable
*Peer Router ID : 3.3.3.3 Negotiation-vc-id : 2 primary or secondary : primary ignore-standby-state : no VC Label : 4100 Peer Type : dynamic Session : up Tunnel ID : 0xf Broadcast Tunnel ID : 0xf Broad BackupTunnel ID : 0x0 CKey : 4 NKey : 3 Stp Enable : 0 PwIndex : 0 Control Word : disable
*Peer Router ID : 4.4.4.4 Negotiation-vc-id : 2 primary or secondary : primary ignore-standby-state : no VC Label : 4101 Peer Type : dynamic Session : up Tunnel ID : 0xb Broadcast Tunnel ID : 0xb Broad BackupTunnel ID : 0x0 CKey : 6 NKey : 5 Stp Enable : 0 PwIndex : 0 Control Word : disable Interface Name : 10GE1/0/1.1 State : up Access Port : false Last Up Time : 2015/03/16 15:56:44 Total Up Time : 0 days, 0 hours, 1 minutes, 24 seconds
**PW Information:
*Peer Ip Address : 3.3.3.3 PW State : up Local VC Label : 4100 Remote VC Label : 4099 Remote Control Word : disable PW Type : label Local VCCV : alert lsp-ping bfd Remote VCCV : alert lsp-ping bfd Tunnel ID : 0xf Broadcast Tunnel ID : 0xf Broad BackupTunnel ID : 0x0 Ckey : 0x4 Nkey : 0x3 Main PW Token : 0xf Slave PW Token : 0x0 Tnl Type : LSP OutInterface : Vlanif10 Backup OutInterface :
Stp Enable : 0 PW Last Up Time : 2015/03/16 15:56:48 PW Total Up Time : 0 days, 0 hours, 1 minutes, 24 seconds
*Peer Ip Address : 4.4.4.4 PW State : up Local VC Label : 4101

Remote VC Label : 4099 Remote Control Word : disable PW Type : label Local VCCV : alert lsp-ping bfd Remote VCCV : alert lsp-ping bfd Tunnel ID : 0xb Broadcast Tunnel ID : 0xb Broad BackupTunnel ID : 0x0 Ckey : 0x6 Nkey : 0x5 Main PW Token : 0xb Slave PW Token : 0x0 Tnl Type : LSP OutInterface : Vlanif40 Backup OutInterface :
Stp Enable : 0 PW Last Up Time : 2015/03/16 15:56:49 PW Total Up Time : 0 days, 0 hours, 1 minutes, 24 seconds
*Peer Ip Address : 2.2.2.2 PW State : up Local VC Label : 4099 Remote VC Label : 4099 Remote Control Word : disable PW Type : label Local VCCV : alert lsp-ping bfd Remote VCCV : alert lsp-ping bfd Tunnel ID : 0xd Broadcast Tunnel ID : 0xd Broad BackupTunnel ID : 0x0 Ckey : 0x2 Nkey : 0x1 Main PW Token : 0xd Slave PW Token : 0x0 Tnl Type : LSP OutInterface : Vlanif10 Backup OutInterface :
Stp Enable : 0 PW Last Up Time : 2015/03/16 15:57:06 PW Total Up Time : 0 days, 0 hours, 1 minutes, 24 seconds在PC1（10.1.1.1）上能够ping通PC2（10.1.1.2）。
当CE1和PE1之间的链路或者PE1设备出现故障时，PE4由备根切换为主根。PC1和PC2仍然可以相互Ping通，流量经PE4转发。
配置脚本
● CE1的配置文件\# sysname CE1 \# vlan batch 100 \# stp bpdu-protection \# stp enable \# stp region-configuration region-name RG1 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 100 \# interface 10GE1/0/2 port link-type access port default vlan 100 stp edged-port enable

\# interface 10GE1/0/4 port link-type trunk port trunk allow-pass vlan 100 \# return
● CE2的配置文件\# sysname CE2 \# vlan batch 100 \# stp bpdu-protection \# stp enable \# stp region-configuration region-name RG1 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 100 \# interface 10GE1/0/2 port link-type access port default vlan 100 stp edged-port enable \# interface 10GE1/0/4 port link-type trunk port trunk allow-pass vlan 100 \# return
● PE1的配置文件\# sysname PE1 \# router id 1.1.1.1 \# vlan batch 10 40 \# stp instance 0 priority 0 stp enable \# stp region-configuration region-name RG1 \# mpls lsr-id 1.1.1.1 mpls \# mpls l2vpn \# vsi a2 static pwsignal ldp vsi-id 2 peer 2.2.2.2 peer 3.3.3.3 peer 4.4.4.4 \# mpls ldp \# mpls ldp remote-peer 3.3.3.3 remote-ip 3.3.3.3 \# interface Vlanif10 ip address 172.16.1.1 255.255.255.0 mpls mpls ldp

\# interface Vlanif40 ip address 172.19.1.2 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid stp vpls-subinterface enable \# interface 10GE1/0/1.1 dot1q termination vid 100 l2 binding vsi a2 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 10 stp disable \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 40 stp disable \# interface LoopBack1 ip address 1.1.1.1 255.255.255.255 \# ospf 1 area 0.0.0.0 network 1.1.1.1 0.0.0.0 network 172.16.1.0 0.0.0.255 network 172.19.1.0 0.0.0.255 \# return
● PE2的配置文件\# sysname PE2 \# router id 2.2.2.2 \# vlan batch 10 20 \# stp instance 0 priority 0 stp enable \# stp region-configuration region-name RG1 \# mpls lsr-id 2.2.2.2 mpls \# mpls l2vpn \# vsi a2 static pwsignal ldp vsi-id 2 peer 1.1.1.1 peer 3.3.3.3 peer 4.4.4.4 \# mpls ldp \# mpls ldp remote-peer 4.4.4.4 remote-ip 4.4.4.4 \# interface Vlanif10 ip address 172.16.1.2 255.255.255.0 mpls mpls ldp

\# interface Vlanif20 ip address 172.17.1.1 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid stp vpls-subinterface enable \# interface 10GE1/0/1.1 dot1q termination vid 100 l2 binding vsi a2 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 10 stp disable \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 20 stp disable \# interface LoopBack1 ip address 2.2.2.2 255.255.255.255 \# ospf 1 area 0.0.0.0 network 2.2.2.2 0.0.0.0 network 172.16.1.0 0.0.0.255 network 172.17.1.0 0.0.0.255 \# return
● PE3的配置文件\# sysname PE3 \# router id 3.3.3.3 \# vlan batch 20 30 \# stp instance 0 priority 4096 stp enable \# stp region-configuration region-name RG1 \# mpls lsr-id 3.3.3.3 mpls \# mpls l2vpn \# vsi a2 static pwsignal ldp vsi-id 2 peer 1.1.1.1 peer 2.2.2.2 peer 4.4.4.4 \# mpls ldp \# mpls ldp remote-peer 1.1.1.1 remote-ip 1.1.1.1 \# interface Vlanif20 ip address 172.17.1.2 255.255.255.0 mpls mpls ldp

\# interface Vlanif30 ip address 172.18.1.1 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid stp root-protection stp vpls-subinterface enable \# interface 10GE1/0/1.1 dot1q termination vid 100 l2 binding vsi a2 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 20 stp disable \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 30 stp disable \# interface LoopBack1 ip address 3.3.3.3 255.255.255.255 \# ospf 1 area 0.0.0.0 network 3.3.3.3 0.0.0.0 network 172.17.1.0 0.0.0.255 network 172.18.1.0 0.0.0.255 \# return
● PE4的配置文件\# sysname PE4 \# router id 4.4.4.4 \# vlan batch 30 40 \# stp instance 0 priority 4096 stp enable \# stp region-configuration region-name RG1 \# mpls lsr-id 4.4.4.4 mpls \# mpls l2vpn \# vsi a2 static pwsignal ldp vsi-id 2 peer 1.1.1.1 peer 2.2.2.2 peer 3.3.3.3 \# mpls ldp \# mpls ldp remote-peer 2.2.2.2 remote-ip 2.2.2.2 \# interface Vlanif30 ip address 172.18.1.2 255.255.255.0 mpls

mpls ldp \# interface Vlanif40 ip address 172.19.1.1 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid stp root-protection stp vpls-subinterface enable \# interface 10GE1/0/1.1 dot1q termination vid 100 l2 binding vsi a2 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 30 stp disable \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 40 stp disable \# interface LoopBack1 ip address 4.4.4.4 255.255.255.255 \# ospf 1 area 0.0.0.0 network 4.4.4.4 0.0.0.0 network 172.18.1.0 0.0.0.255 network 172.19.1.0 0.0.0.255 \# return
