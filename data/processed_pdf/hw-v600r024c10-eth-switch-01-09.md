# S1700, S5700, S6700 V600R024C10 配置指南-以太网交换 01-09 SEP配置

## 9 SEP配置

9 SEP 配置

### 9.1 SEP简介

9.2 SEP原理描述
9.3 SEP组网方式
9.4 SEP配置注意事项
9.5 SEP缺省配置
9.6 配置SEP基本功能
9.7 配置SEP多实例
在SEP段中，如果不指定阻塞端口，SEP段中的每个端口均有可能成为阻塞端口。通过
灵活指定阻塞端口，可以使阻塞端口指定到预期位置，提升网络转发性能且更好支持
SEP多实例场景下的流量负载分担。
9.8 配置网络拓扑变化通告
网络拓扑变化通告部署在连接上、下级网络的设备上，用于上、下级网络拓扑变化时
发送拓扑变化通告通知对方网络，以便对方网络中的所有设备及时清除MAC地址表项
和ARP表项，重新学习对方网络拓扑变化后的MAC地址，从而保证用户流量不中断。
9.9 维护SEP
9.10 SEP配置举例
9.1 SEP 简介
定义
智能以太保护SEP（Smart Ethernet Protection）是一种专用于以太网链路层的环网协
议。SEP是一种以太环路保护机制，通过有选择性地阻塞网络环路中的冗余链路，达到
消除网络二层环路的目的，避免报文在环路网络中增生和无限循环，有效防止形成网
络风暴。
SEP 环网协议以 SEP 段为基本单位。 SEP 段是由一组配置了相同的段 ID 、控制 VLAN 且互
连的二层交换设备群体构成。一个SEP段在无故障产生时，存在一个自动协商或手工灵
活指定的阻塞端口。SEP协议通过SEP段中的阻塞端口破除环路。

目的以太网交换网络中为了进行链路备份，提高网络可靠性，通常会使用冗余链路。但是使用冗余链路会在交换网络上产生环路，引起广播风暴以及MAC地址表不稳定等故障现象，从而导致用户通信质量较差，甚至通信中断。
为了解决环路问题，数据通信设备一般支持STP/RSTP/MSTP系列生成树协议。STP/ RSTP/MSTP是以太网络二层破环技术的标准协议，应用成熟、场景广泛，且支持与其他制造商设备互通。但是运行生成树协议的网络拓扑收敛速度慢，收敛时间在秒级，不能满足一些实时业务的要求，且收敛时间受网络拓扑影响。
为此，华为公司推出了SEP协议。相比STP/RSTP/MSTP系列生成树协议，SEP具有以下优势：
● 支持最快小于50毫秒的环网故障倒换性能，从而提供链路故障时的快速收敛能力，实现链路的快速切换。
● 支持灵活选择阻塞端口，更好地支持流量负载分担。
● 支持链路恢复后回切方式灵活配置。
● 支持拓扑查看，显示SEP网络拓扑结构。
● 简化配置，更好支持多环组网。

### 9.2 SEP原理描述

#### 9.2.1 SEP基本原理

SEP是一种专用于以太网链路层的环网协议，以SEP段为基本单位。每台交换设备上只能有两个端口加入同一SEP段。
在SEP段中，为了防止出现环路，可以启动环路保护机制，选择性地阻塞端口，消除以太网冗余链路。当环网发生链路故障时，运行SEP协议的设备可以迅速地放开阻塞端口，进行链路倒换，恢复环网上各节点间链路通信。
如图9-1所示是一个典型的SEP应用组网。CE1通过两条链路接入NPE（Network Provider Edge）。在NPE1、NPE2上部署了VRRP备份组。最初，NPE1是主用状态，NPE2是备用状态。
图 9-1 SEP 典型组网当NPE1与Device5之间的链路或节点发生故障时：

1. 以Device1与Device5之间的链路发生故障为例。通过VRRP功能，NPE1的状态将
由主变为备，NPE2的状态将由备变为主。
2. 根据是否部署SEP，流量转发过程区分如下：
– 当未部署SEP时：CE1上送的流量仍然按原路径转发。由于状态已经变为备的
NPE1已经不再转发流量，导致流量中断。
– 当已部署SEP时：如图9-2所示，通过SEP协议环路保护机制，Device5上的阻
塞端口被放开并进入转发状态，同时Device5发送LSA（Link Status
Advertisement）报文通知SEP段上的其他节点刷新各自的LSA数据库。CE1上
送的流量切换到备用链路Device5>Device2>Device4>NPE2，从而保证了流
量正常传输。其中关于端口角色的详细介绍，请参见9.2.2 SEP基本概念。
图 9-2 SEP 典型组网故障前后示意
在普通SEP组网中，一个物理环上只能配置一个SEP段，也只能指定一个阻塞点。当
SEP段处于完整状态时，阻塞端口会阻止所有的业务数据通过。这样，所有业务数据在
SEP段上只能通过一条路径传输。副边缘端口侧的链路空闲，造成带宽浪费。
为了解决带宽浪费问题，实现负载分担，可部署 SEP 多实例功能。 SEP 多实例允许在一
个物理环路配置两个逻辑环路，即两个SEP段。每一个SEP段独立检测物理环路的完整
性，并相应的阻塞或放开端口，彼此互不影响。要了解关于SEP多实例的详细信息，请
参见9.7.1 了解多实例。

#### 9.2.2 SEP基本概念

SEP 网络结构和基本概念如图9-3所示，Device1～Device5组成了双归链路接入上级二层网络组网。位于上级二层网络的两台边缘设备Device1和Device5之间采用非直连方式，这种组网方式称为开放环接入。该接入方式在整个网络中引入了新的环路。为了消除网络中冗余环路，有效地保证链路连通性，需要启动环路保护机制。
图 9-3 SEP 开放环组网图9-3所示是一个典型的启动SEP协议的开放环组网图，下面结合该图介绍SEP的几个基本概念，如表 9-1 所示。
表 9-1 SEP 基本概念

| 概念 | 描述 |
|---|---|
| SEP段（Segment） | SEP以SEP段为基本单位。SEP段是由一组配置了相同的段 ID、控制VLAN且互连的二层交换设备群体构成。一个SEP段物理上对应一个环形或者线性连接的以太网拓扑。每个SEP段具有控制VLAN、边缘端口和普通端口等要素。 |

| 概念 | 描述 |
|---|---|
| 控制VLAN（Control VLAN） | 在SEP段中，控制VLAN只用来传递SEP协议报文。每个SEP段必须配置控制VLAN。当接口加入已经配置控制 VLAN的SEP段后，接口将自动加入控制VLAN。不同SEP段可以使用相同ID的控制VLAN。与控制VLAN相对，数据VLAN用来传递数据报文。 |
| 节点（Node） | 加入SEP段的二层交换设备称之为节点。每个节点不能有多于两个端口加入同一个SEP段。 |
| 端口角色 | SEP协议中规定，端口的角色主要有普通端口、边缘端口两大类。详细介绍如表9-2所示。 |
| 阻塞端口 | 在SEP段中，为了防止形成环路而被阻塞的端口称为阻塞端口。在SEP段中，如果不指定阻塞端口，SEP段中的每个端口均有可能成为阻塞端口。在无故障产生时，一个SEP段中只有一个阻塞端口。 |
| 端口状态 | 在SEP段中，启动SEP协议的端口状态分为两种，如表9-3所示。 |

表 9-2 SEP 端口角色

| 端口角色 | 子端口角色 | 描述 |
|---|---|---|
| 边缘端口（Edge Port） | 主边缘端口（Primary Edge Port） | 主边缘端口的职责是发起阻塞端口抢占、终结报文以及向其他网络发送拓扑变化消息。一个SEP段中只有一个主边缘端口，由用户配置并选举决定。 |
|  | 副边缘端口（Secondary Edge Port） | 副边缘端口的职责是终结报文以及向其他网络发送拓扑变化消息。一个SEP段中只有一个副边缘端口，由用户配置并选举决定。 |
|  | 无邻居主边缘端口（No-Neighbor Primary Edge Port） | 处于SEP段最边缘的端口是无邻居边缘端口，由用户配置并选举决定。从两个无邻居边缘端口中选举出一个无邻居主边缘端口。无邻居主边缘端口的职责是发起阻塞端口抢占、终结报文以及向其他网络发送拓扑变化消息。无邻居主边缘端口一般用于与其他设备制造商设备互通或与不支持SEP协议的设备互通。 |

| 端口角色 | 子端口角色 | 描述 |
|---|---|---|
|  | 无邻居副边缘端口（No-Neighbor Secondary Edge Port） | 处于SEP段最边缘的端口是无邻居边缘端口，由用户配置并选举决定。从两个无邻居边缘端口中选举出一个无邻居副边缘端口。无邻居副边缘端口的职责是终结报文以及向其他网络发送拓扑变化消息。无邻居副边缘端口一般用于与其他设备制造商设备互通或与不支持SEP协议的设备互通。 |
| 普通端口（Common Port） | - | 在SEP段中，除边缘端口以外所有的端口都是普通端口。普通端口负责监测自己直连的启动SEP协议的链路状态，并把链路状态的变化消息及时通知邻居端口。邻居端口不断向SEP段中其他端口扩散消息，最后到达主边缘端口。然后由主边缘端口决策如何处理上报的链路状态变化消息。 |
| 注：主边缘端口和无邻居边缘端口建议不要配置在同一个SEP段中；副边缘端口和无邻居边缘端口建议不要配置在同一个SEP段中。 |  |  |

表 9-3 SEP 端口状态表

| 端口状态 | 描述 |
|---|---|
| Forwarding | 在Forwarding状态下，端口既转发用户流量，又接收/发送 SEP协议报文。 |
| Discarding | 在Discarding状态下，端口接收/发送SEP协议报文。 |
| 注：端口状态和端口角色没有必然的联系。不同角色的端口均支持Forwarding和 Discarding两种状态。 |  |

SEP 协议报文SEP协议报文类型如表9-4所示。
表 9-4 SEP 协议报文类型

| 报文类型 | 报文的子类型 | 描述 |
|---|---|---|
| Hello | - | 端口加入SEP段后，开始启动邻居协商机制。端口之间通过收发邻居协议报文（Hello报文），与相邻端口协商建立邻居关系。邻居协商成功后，端口之间继续发送和接收邻居协议报文，用于检测邻居状态的变化。 |

| 报文类型 | 报文的子类型 | 描述 |
|---|---|---|
| LSA | LSA请求报文 | 链路状态通告报文（Link Status Advertisement），当端口启用SEP协议后开始周期发送LSA报文给邻居端口，在端口邻居状态机状态进入Up后，开始更新各自的LSA数据库。更新的内容是本端口所保存的所有链路拓扑信息。 |
|  | LSA应答报文 |  |
| TC | - | 拓扑变化报文（Topology Change），当本地SEP 段中的拓扑发生变化，需要发送TC报文，通知上级网络下级网络的拓扑发生变化，上级网络中的节点需要更新MAC地址转发表和ARP表。 TC报文由本地SEP段和上级网络相交的设备发起。 |
| 主边缘端口选举报文 | - | 端口启动SEP协议后，如果符合参与主边缘端口选举要求，则主动将自己的端口角色设置为主边缘端口，并开始周期发送主边缘选举报文，不需要等待邻居协商成功。主边缘选举报文中携带端口角色（主边缘端口、副边缘端口、普通端口）、端口的桥MAC地址、端口ID、拓扑数据库状态是否完整。 |
| 抢占报文 | 抢占请求报文 | 抢占报文用于阻塞指定端口。抢占报文由选举出的主边缘端口或无邻居主边缘端口的兄弟端口发起。 |
|  | 抢占应答报文 |  |

#### 9.2.3 SEP实现机制

邻居协商机制端口加入SEP段后，开始启动邻居协商机制。端口之间通过收发邻居协议报文（Hello报文），与相邻端口协商建立邻居关系。邻居协商成功后，端口之间继续发送和接收邻居协议报文，用于检测邻居状态的变化。
邻居协商机制可以防止链路单通。邻居协商机制是双向的，链路两端的端口均要向对端发送邻居协议报文。若有一端端口在超时时间内没有收到对端发送的邻居协议报文，则会将端口的邻居状态置为 Down 。
邻居协商机制为显示SEP段拓扑提供了必要的信息。利用邻居协商机制建立起各端口的邻居关系，各条链路便可以串联成一个完整的SEP段，从而有助于显示完整的SEP段拓扑信息。
链路状态同步SEP段中链路完成邻居协商后进入链路状态同步阶段，SEP段上的节点周期性发送链路状态通告报文LSA。所有节点收到其他节点发送的LSA报文后，更新本地的邻居状态数据库，保证 SEP 段上所有节点链路数据库一致。
如果在3倍的LSA报文发送周期内本节点仍然未收到对端设备或SEP段中其他设备的LSA报文，本设备保存环路上其他设备LSA节点信息的数据库将老化。

当SEP段中有故障节点恢复时，该节点需要及时获取SEP段上所有节点的拓扑信息。该节点会主动发送LSA请求报文，邻居端口收到LSA请求报文后发送LSA ACK应答报文，将本节点最新的链路状态信息通知给故障恢复的节点。
拓扑显示拓扑显示功能用于每台设备上都能够查看到当前网络连通性最大的拓扑。链路状态的同步，保证了每台设备上拓扑显示内容的一致性。
SEP段拓扑类型如表9-5所示。
表 9-5 SEP 段拓扑类型表

| 拓扑类型 | 说明 |
|---|---|
| 环形拓扑 | SEP段上每一个端口的邻居状态均为Up，且每一个端口都有邻居端口和兄弟端口。即SEP段上每个节点均有两个端口加入SEP段。 |
| 线性拓扑 | 除环形拓扑之外的所有拓扑均是线性拓扑。 |

主边缘端口选举只有将端口角色配置为主边缘端口、副边缘端口或无邻居边缘端口，才有参与主边缘端口选举的权利。
说明如果节点上只有一个端口启动了SEP协议，必须通过命令配置端口角色为edge，才认为此端口是边缘端口。
如图9-4所示，网络中链路无故障的情况下，端口启动SEP协议后：
● 端口角色为普通端口的端口不参与主边缘端口选举。即，只有Device1和Device5上的P1端口参与主边缘端口选举。
● 如果Device1和Device5上的P1端口角色相同，则MAC地址大的端口将被选举为主边缘端口。
主边缘端口选出后，即开始周期发送主边缘端口选举报文，不需要等待邻居协商成功。主边缘端口选举报文中携带端口角色（主边缘端口、副边缘端口、普通端口）、端口的桥MAC地址、端口ID、拓扑数据库状态是否完整。

图 9-4 主边缘端口选举示意如图9-4所示，当SEP段中出现链路故障，Device1、Device5上的P1端口收到故障通告报文或Device5上的P1端口超时后没有收到主边缘端口选举报文，此时Device1上的P1端口角色将变为副边缘端口，SEP段中存在两个副边缘端口。
两个副边缘端口都在周期性地发送主边缘端口选举报文。当SEP段中最后一处链路故障恢复后，两个副边缘端口都可以收到对端发送的主边缘端口选举报文。在1个周期内（缺省情况下周期为1秒）内完成新的主边缘端口选举。
灵活指定阻塞端口正常情况下，阻塞端口是最后完成邻居协商的链路两端的其中一个端口，通过协商选出的阻塞端口有时并不是用户所需要的阻塞点。为了满足用户的需求，可灵活指定阻塞端口。指定阻塞端口后并不立即生效，只有抢占机制生效后，阻塞端口才会从当前的阻塞点抢占到指定的阻塞点。
设备支持的阻塞端口指定方式如表9-6所示。
表 灵活指定阻塞端口方式表9-6

| 阻塞端口方式 | 说明 |
|---|---|
| 指定优先级最高的端口为阻塞端口 | 端口优先级比较原则如下： 1. 比较端口优先级（端口优先级可配置，数值取值越大，优先级越高）。 2. 端口优先级相同，比较端口的桥MAC地址。桥 MAC地址越小，优先级越高。 3. 桥MAC地址相同，比较端口编号。端口编号越小，优先级越高。 |

| 阻塞端口方式 | 说明 |
|---|---|
| 指定SEP段中间的端口为阻塞端口 | - |
| 根据用户配置的跳数指定阻塞端口 | 主边缘端口的跳数为1，主边缘端口的邻居端口的跳数为2。跳数是沿着主边缘端口的下游邻居方向依次增加。 |
| 根据设备名+端口名指定阻塞端口 | 当SEP协议启动后，设备名＋端口名确定了用户需要阻塞的端口。用户在配置前可通过显示命令查看当前环的详细拓扑信息，获取到拓扑中所有端口信息，然后指定设备名和端口名。如果环路中存在多台设备的设备名称、端口名称相同，则阻塞端口位于从主边缘端口开始查找，阻塞设备名称、端口名称第一次出现的位置。根据设备名+端口名指定阻塞端口时，如果用户在后续的操作中修改了对应的设备名或端口名，那么将导致抢占无法生效。 |

链路故障恢复后，正常情况下，在最后恢复的链路中选择一个阻塞端口。阻塞端口是否迁移，由是否抢占模式决定。详细说明如表9-7所示。
表 9-7 是否抢占模式说明

| 模式 | 说明 |
|---|---|
| 不抢占模式 | 当最后一处故障恢复或最后启动SEP协议的链路的两端端口在邻居协商完成后，通过互相发送端口阻塞状态报文选择最优端口阻塞，其他端口进入转发状态。 |

| 模式 | 说明 |
|---|---|
| 抢占模式 | 抢占只能在位于主边缘端口的设备或者是无邻居边缘主端口的设备上进行。抢占模式又分为延时抢占和手工抢占两种模式： ● 延时抢占当最后一个端口故障恢复后，边缘端口将不再收到故障通告报文。主边缘端口在3秒内没有收到故障通告报文，立即启动延时定时器。延时定时器超时后，SEP段中的节点执行阻塞端口抢占。 ● 手工抢占当用户通过命令配置手工抢占模式，在确定主边缘端口和副边缘端口的链路状态数据都完整的情况下，选举出的主边缘端口或无邻居主边缘端口的兄弟端口发送抢占报文阻塞指定的端口。端口阻塞后立即发送端口阻塞状态报文，原阻塞端口放开进入转发状态，手工抢占完成。说明同一台设备只允许两个端口加入同一个SEP段。如果其中一个端口是无邻居主边缘端口，那么另外一个接口为无邻居主边缘端口的兄弟端口。阻塞端口抢占报文的发起由无邻居主边缘端口的兄弟端口是否是阻塞端口决定。如果阻塞端口是无邻居主边缘端口的兄弟端口，那么无需发送阻塞端口抢占报文；如果阻塞端口不是无邻居主边缘端口的兄弟端口，那么由无邻居主边缘端口的兄弟端口发送阻塞抢占报文。 |

拓扑变化通告拓扑变化通告部署在连接上、下级网络的设备上，用于上、下级网络拓扑变化时发送拓扑变化报文通知对方网络。在启用SEP协议的拓扑中，存在如表9-8所示的两种拓扑变化通告。
表 9-8 SEP 拓扑变化通告

| 拓扑变化通告 | 说明 |
|---|---|
| 端口故障 | 在SEP段完整的情况下，有端口故障产生，如图9-5 所示。端口故障包括链路故障和端口邻居状态故障。当SEP段中的其他端口收到故障通告报文后，如果该端口所在设备存在处于转发状态的端口，则该端口需要发出Flush-FDB（Forwarding Database）报文通知SEP段中其他节点拓扑发生变化。 |

| 拓扑变化通告 | 说明 |
|---|---|
| 故障恢复且抢占生效 | SEP段中存在故障。当最后一处端口故障恢复，同时进行了阻塞端口抢占。抢占由主边缘端口或无邻居主边缘端口触发。当SEP 段中的其他端口收到主边缘端口或无邻居主边缘端口的抢占报文后，需要发出Flush-FDB报文通知SEP 段中其他节点拓扑发生变化。 |

图 9-5 SEP 拓扑变化通告示意拓扑变化抑制在SEP段拓扑变化时会发生拓扑变化通告报文，以通知其他SEP段或上级网络。但是，如下情况会导致SEP段产生大量的拓扑变化通告报文：

● 链路闪断
● SEP段受到恶意拓扑变化攻击
● 多级SEP组网
如图9-6所示，SEP段组网为3级。当ID为3的SEP段发生拓扑变化时，SEP拓扑变化
通告报文经过Device4和Device6、报文数量以乘以2的速度加扩散到ID为2的SEP
段。以此类推，SEP拓扑变化通告报文每经过一个SEP段，SEP拓扑变化通告报文
的数量都将乘以2。
图 9-6 多级 SEP 组网
频繁的拓扑变化通告将导致网络设备CPU处理能力下降，且同时导致SEP段中的设备频
繁刷新Flush-FDB报文，占用带宽。为避免此类情况产生，需要对拓扑变化通告报文进
行抑制，抑制的措施有：
● 基于拓扑变化进行源抑制，同一个源端口触发的拓扑变化通告报文不会被重复处
理。
● 指定的时间（该时间可配置）内只处理特定数量的拓扑变化通告报文。缺省情况
下，2秒钟内处理3个不同源的拓扑变化通告报文。
● 网络规划时尽量避免多级别（多于3级）的SEP组网。

### 9.3 SEP组网方式

#### 9.3.1 开放环组网

如图9-7，Device1～Device5组成半环网络接入上级二层网络，位于上级二层网络的两台边缘设备Device1和Device5之间不是直连的方式，这种组网方式称之为开放环接入。此组网位于接入层，完成单播业务及组播业务的二层透传功能。通过在接入层运行SEP协议，实现接入环的冗余保护倒换、拓扑查看。
开放环组网的特点是环上的两个边缘端口部署在两个边缘设备上。
图 9-7 SEP 开放环组网

#### 9.3.2 封闭环组网

如图9-8，Device1～Device5组成了双归链路接入上级二层网络组网，位于上级二层网络的两台边缘设备Device1和Device5之间是直连的方式，这种组网方式称之为封闭环接入。此组网位于汇聚层，完成单播及组播业务的汇聚。通过在汇聚层运行SEP协议，实现汇聚层的冗余保护倒换、拓扑查看。
封闭环组网的特点是环上的两个边缘端口部署在同一个边缘设备上。

图 9-8 SEP 封闭环组网

#### 9.3.3 多环组网

如图9-9，Device1～Device14的组网方式称为多环接入，Device1～Device5位于汇聚层，Device6～Device14位于接入层。网络中接入层与汇聚层均透传二层业务。通过在接入层与汇聚层运行SEP协议，实现接入层与汇聚层的冗余保护倒换、拓扑查看。
如果接入层拓扑发生变化，SEP段内会发送Flush-FDB报文通知本SEP段内其他节点进行MAC转发表和ARP表刷新。SEP段上的边缘设备会发送TC报文，通知上级网络，本SEP段的拓扑发生变化。
多环组网在配置上和单环的差别在于需要配置环间的拓扑变化通告。

图 9-9 SEP 多环组网

#### 9.3.4 SEP多实例组网

如图9-10所示，SEP多实例允许在一个物理环路配置两个逻辑环路，即两个SEP段。每一个SEP段上所有设备、端口角色、控制VLAN等都必须遵循基本的SEP原则。相应的，一个物理环路上有两个阻塞端口，各个阻塞端口分别检测物理环路的完整性，并相应的阻塞或放开，彼此互不影响。
一个物理环路上可以包含一个或两个SEP段，每个SEP段上均需要配置一个保护实例，每个保护实例代表一个VLAN范围。不同的SEP段计算出的拓扑仅对该SEP段有效，不影响其他SEP段。
通过给每个SEP段配置不同的保护实例，各阻塞端口只对本SEP段所保护的VLAN有效。属于不同VLAN的数据流量就可以通过不同的路径传输，从而实现业务流量的负载分担和链路备份。

图 9-10 SEP 多实例组网

### 9.4 SEP配置注意事项

License 依赖SEP无需License许可即可使用。
硬件依赖表 9-9 支持本特性的硬件

| 系列 | 支持产品 |
|---|---|
| S6750-H | S6750-H36C，S6750-H48Y8C |
| S1730S-S3 | S1730S-S24P4S-A3，S1730S-S24P4X-A3， S1730S-S24T4S-QA3，S1730S-S24T4X-QA3， S1730S-S48P4S-A3，S1730S-S48T4S-A3， S1730S-S48T4X-A3，S1730S-S8P4X-QA3， S1730S-S8T4X-QA3 |
| S6730E-H-V2 | S6730E-H6FX4Y2CZ-V2 |

| 系列 | 支持产品 |
|---|---|
| S5735-S-V2 | S5735-S24HS4XE-V2，S5735-S24P4XE-V2， S5735-S24P4XEZ-V2，S5735-S24P8J4XEZ-V2， S5735-S24PN4XE-V2，S5735-S24ST4XE-V2， S5735-S24T4XE-C-V2，S5735-S24T4XE-V2， S5735-S24T4XEZ-V2，S5735-S24T8J4XE-XA-V2， S5735-S24T8J4XEZ-V2，S5735-S24U4XE-V2， S5735-S48HS4XE-V2，S5735-S48P4XE-V2， S5735-S48P4XEZ-V2，S5735-S48PN4XE-V2， S5735-S48S4XE-V2，S5735-S48T4XE-C-V2， S5735-S48T4XE-V2，S5735-S48T4XE-XA-V2， S5735-S48T4XEZ-V2，S5735-S48U4XE-V2 |
| S5735E-S-V2 | S5735E-S24HS4XE-V2，S5735E-S48HS4XE-V2 |
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
| S5735E-L-V2 | S5735E-L16LP2UM2X-QA-V2，S5735E-L16LP2X- QA-V2，S5735E-L24P4S-A-V2，S5735E-L24P4XE- A-V2，S5735E-L24ST4XE-A-V2，S5735E- L24T4XE-A-V2，S5735E-L48LP4S-A-V2，S5735E- L48LP4XE-A-V2，S5735E-L48S4XE-A-V2， S5735E-L48T4XE-A-V2，S5735E-L8P4X-QA-V2， S5735E-L8T4X-QA-V2 |
| S5755-S | S5755-S24P8J8YZ，S5755-S24P8Y，S5755- S24T8J8YZ，S5755-S24T8Y，S5755-S24U8J8YZ， S5755-S24U8Y，S5755-S48P8Y，S5755- S48P8YZ，S5755-S48T8Y，S5755-S48T8YZ， S5755-S48U8Y，S5755-S48U8YZ |
| S5735R-L-V2 | S5735R-L16LP2S-QA-V2，S5735R-L16LP2UM2X- QA-V2，S5735R-L16LP2X-QA-V2，S5735R- L16T4S-A-V2，S5735R-L16T4X-QA-V2，S5735R- L24P4S-A-V2，S5735R-L24P4X-A-V2，S5735R- L24T4S-A-V2，S5735R-L24T4X-QA-V2，S5735R- L48LP4S-A-V2，S5735R-L48LP4X-A-V2，S5735R- L48P4X-A-V2，S5735R-L48T4S-A-V2，S5735R- L48T4X-A-V2，S5735R-L8P4S-A-V2，S5735R- L8P4X-QA-V2，S5735R-L8T4S-A-V2，S5735R- L8T4X-QA-V2 |
| S5735-L-V2 | S5735-L10T4X-A-V2，S5735-L14P2S-QA-V2， S5735-L16LP2UM2X-QA-V2，S5735-L16LP2X-QA- V2，S5735-L16P2UM2X-QA-V2，S5735-L16T4S- A-V2，S5735-L16T4X-QA-V2，S5735- L24LU8S4XE-QA-V2，S5735-L24P4S-A-V2， S5735-L24P4XE-A-V2，S5735-L24PN4XE-A-V2， S5735-L24ST4XE-A-V2，S5735-L24T4S-A-V2， S5735-L24T4X-QA-V2，S5735-L24T4XE-A-V2， S5735-L24T4XE-D-V2，S5735-L24T8J4XE-A-V2， S5735-L48LP4S-A-V2，S5735-L48LP4XE-A-V2， S5735-L48LPN4XE-A-V2，S5735-L48P4XE-A-V2， S5735-L48PN4XE-A-V2，S5735-L48S4X-A-V2， S5735-L48S4XE-A-V2，S5735-L48T4S-A-V2， S5735-L48T4XE-A-V2，S5735-L48T4XE-D-V2， S5735-L8P2T4X-A-V2，S5735-L8P4S-A-V2， S5735-L8P4X-QA-V2，S5735-L8T4S-A-V2， S5735-L8T4X-QA-V2 |
| S5735I-S-V2 | S5735I-S16T2S4XN-V2，S5735I-S16T8S4XE-QD- V2，S5735I-S24T4XE-V2，S5735I-S24T8S4XE-QA- V2，S5735I-S24U4XE-V2，S5735I-S48T4XE-V2， S5735I-S8T4SN-V2，S5735I-S8T4XN-V2，S5735I- S8T8P2S4XN-V2，S5735I-S8U2XN-V2，S5735I- S8U4XN-V2 |

| 系列 | 支持产品 |
|---|---|
| S5732-H-V2 | S5732-H24S4X6QZ-TV2，S5732-H24S4X6QZ- V2，S5732-H24UM4Y2CZ-KV2，S5732- H24UM4Y2CZ-V2，S5732-H44S4X6QZ-V2， S5732-H48UM4Y2CZ-KV2，S5732-H48UM4Y2CZ- TV2，S5732-H48UM4Y2CZ-V2 |

查询工具如需了解硬件规格、产品部件的配套关系，请点击硬件中心进行查询；如需了解关键规格、全量软件规格，请点击规格查询进行查询。
特性限制表 9-10 本特性的使用限制特性限制根据设备名+端口名指定或抢占阻塞端口时，如果环路中存在多台设备的设备名称、端口名称相同，则阻塞端口位于从主边缘端口开始查找，阻塞设备名称、端口名称第一次出现的位置。
SEP和VBST同时使能时，由于VBST动态分配实例VLAN映射关系，会导致SEP功能不符合预期结果。

### 9.5 SEP缺省配置

SEP缺省配置如表9-11所示。
表 9-11 SEP 缺省配置

| 参数 | 缺省值 |
|---|---|
| 阻塞端口位置 | 缺省情况下，系统自动协商出一个阻塞端口。协商的原则是从最后建立起来或故障恢复的那条链路的两个端口中协商出一个阻塞端口。 |
| 加入SEP段中的端口优先级 | 64（端口优先级的取值范围是1～128，取值越大，优先级越高） |
| 主边缘端口的抢占模式 | 不抢占 |
| 网络拓扑变化通知消息发送范围 | 不发送 |
| SEP拓扑变化保护时间间隔 | 2秒 |

#### 9.6.2 配置控制VLAN

### 9.6 配置SEP基本功能

#### 9.6.1 创建SEP段

前提条件在创建SEP段之前，需完成以下任务：
在物理上搭建环形拓扑的组网环境。
●
● 设备正确上电，且工作正常。
背景信息SEP协议以SEP段为基本单位。所谓SEP段，就是由一组配置了相同的SEP段ID和控制VLAN且互连的二层交换设备群体构成。
对于已经配置 SEP 的设备，可以通过命令 description 配置该 SEP 段相关的描述信息，信息中可以包含SEP段的ID等，便于维护。
操作步骤步骤1 进入系统视图。
system-view步骤2 创建SEP段并进入SEP-Segment视图。
sep segment segment-id设备整机最大支持配置256个SEP Segment，每个单板上最大支持配置48个。
步骤3 （可选）执行命令，配置SEP段的描述信息。
description text缺省情况下，SEP段没有描述信息。
----结束配置控制
9.6.2 VLAN背景信息在SEP段中，控制VLAN只用来转发SEP协议报文，不用来转发用户业务报文，从而提高了SEP协议的安全性。每个SEP段必须配置控制VLAN，当接口加入已经配置控制VLAN的SEP段后，接口将自动加入控制VLAN。
说明在无邻居场景下，不在SEP段中的设备不能加入SEP段的控制VLAN，否则会导致网络成环。
操作步骤步骤1 进入系统视图。
system-view

步骤2 进入已经成功创建的SEP-Segment视图。
sep segment segment-id步骤3 配置SEP段的控制VLAN，用于转发SEP协议报文。
control-vlan vlan-id注意事项如下：
● 由参数vlan-id指定的控制VLAN必须是未被创建的，未被VBST（VLAN-Based Spanning Tree）的动态实例使用且未通过trunk、hybrid、access、qinq、mapping、stacking等方式使用的VLAN。
● 不同SEP段可以使用相同ID的控制VLAN。
● 如果SEP段中已经加入接口，那么将不能直接删除控制VLAN。如果需要删除已配置的控制VLAN，必须在接口视图下执行命令undo sep segment segment-id将接口退出SEP段，然后在SEP-segment视图下执行命令undo control-vlan删除控制VLAN。
● 如果SEP段中没有接口加入，可以多次配置控制VLAN，以最后一次配置为准。
● 控制VLAN成功创建后，配置文件会自动显示创建普通VLAN的命令。
● 每个 SEP 段必须配置控制 VLAN ，当接口加入已经配置控制 VLAN 的 SEP 段后，接口将自动加入控制VLAN。
– 如果接口类型是Trunk类型，则配置文件中，加入SEP段的接口下会自动显示命令port trunk allow-pass vlan。
– 如果接口类型是Hybrid类型，则配置文件中，加入SEP段的接口下会自动显示命令port hybrid tagged vlan。
----结束

#### 9.6.3 配置保护实例

背景信息SEP段的保护实例用于确定该SEP段所保护的VLAN范围。一个SEP段内可以创建一个或多个保护实例。在非SEP多实例场景下，可以让一个SEP段保护所有VLAN或指定范围的VLAN；在SEP多实例场景下，给两个SEP段配置不同的保护实例，让每个保护实例保护不同范围的VLAN，从而让不同VLAN的数据流量通过不同的路径传输，实现业务流量的负载分担和链路备份。
只有先配置SEP段的保护实例，才能成功将端口加入SEP段。
操作步骤步骤1 进入系统视图。
system-view步骤2 （可选）创建并配置生成树实例与VLAN间的映射关系。
说明如果已经使用命令stp mode vbst设置STP工作模式为VBST，则必须执行此步骤静态配置生成树实例与VLAN的映射关系，否则配置SEP段的保护实例不能成功。
1. 进入MST域视图。
stp region-configuration

2. 创建生成树实例并配置该实例与VLAN间的映射关系。
instance instance-id vlan { vlan-id1 [ to vlan-id2 ] }&<1-10>
缺省情况下，所有VLAN均映射到实例0上。
3. 退出MST域视图。
quit
步骤3 进入已经成功创建的SEP-Segment视图。
sep segment segment-id
步骤4 配置SEP段的保护实例。
protected-instance { all | { instance-id1 [ to instance-id2 ] } &<1-10> }
如果配置了保护实例与VLAN间的映射关系，则此步骤中的参数instance-id，必须与上
面操作中命令instance instance-id vlan vlan-id设置的instance-id一致。
缺省情况下，SEP段上没有配置保护实例。
说明
如果选择参数all，则SEP保护实例针对所有VLAN有效；如果需要创建多个保护实例，请在同一
SEP 段内多次执行上面命令即可。
----结束

#### 9.6.4 将二层端口加入SEP段并配置端口角色

背景信息为了保证SEP协议报文的正常转发，必须将二层端口加入SEP段并为加入SEP段的端口设置不同的端口角色。
端口加入SEP段后，如果符合参与主边缘端口选举要求，则主动将自己的端口角色设置为主边缘端口，并开始周期发送主边缘选举报文，不需要等待邻居协商成功。
主边缘选举报文中携带端口角色（主边缘端口、副边缘端口、普通端口）、端口的桥MAC地址、端口ID、拓扑数据库状态是否完整等信息。
端口角色的设置如表9-12所示。

表 9-12 端口角色

| 端口角色 | 子端口角色 | 说明 | 场景 |
|---|---|---|---|
| 普通端口（Comm on Port） | - | 在SEP段中，除边缘端口以外所有的端口都是普通端口。普通端口负责监测自己直连的启动SEP 协议的链路状态，并把链路状态的变化消息及时通知邻居端口。邻居端口不断向SEP段中其他端口扩散消息，最后到达主边缘端口。然后由主边缘端口决策如何处理上报的链路状态变化消息。 | - |
| 边缘端口（Edge Port） | 主边缘端口（Primary Edge Port） | 一个SEP段中只有一个主边缘端口，由用户配置并选举决定。主边缘端口的职责是发起阻塞端口抢占、终结报文以及向其他网络发送拓扑变化消息。 | 开放环组网封闭环组网多环组网 |
|  | 副边缘端口（Secondary Edge Port） | 一个SEP段中只有一个副边缘端口，由用户配置并选举决定。副边缘端口的职责是终结报文以及向其他网络发送拓扑变化消息。 |  |

| 端口角色 | 子端口角色 | 说明 | 场景 |
|---|---|---|---|
|  | 无邻居主边缘端口（No-Neighbor Primary Edge Port） | 处于SEP段最边缘的端口是无邻居边缘端口，由用户配置并选举决定。从两个无邻居边缘端口中选举出一个无邻居主边缘端口。无邻居主边缘端口的职责是发起阻塞端口抢占、终结报文以及向其他网络发送拓扑变化消息。无邻居主边缘端口一般用于与其他设备制造商设备互通或与不支持SEP协议的设备互通。 | 混合组网，当前版本暂不支持 |
|  | 无邻居副边缘端口（No-Neighbor Secondary Edge Port） | 处于SEP段最边缘的端口是无邻居边缘端口，由用户配置并选举决定。从两个无邻居边缘端口中选举出一个无邻居副边缘端口。无邻居副边缘端口的职责是终结报文以及向其他网络发送拓扑变化消息。无邻居副边缘端口一般用于与其他设备制造商设备互通或与不支持SEP协议的设备互通。 |  |
| 注1：主边缘端口和无邻居边缘端口建议不要配置在同一个SEP段中，副边缘端口和无邻居边缘端口建议不要配置在同一个SEP段中。注2：除了无邻居边缘端口以外，所有端口在加入SEP段之前，必须已经去使能 STP。注3：所有端口在加入SEP段之前，必须已经去使能Smart Link。注4：所有端口在加入SEP段之前，必须已经去使能端口安全，否则会导致无法破环。 |  |  |  |

操作步骤步骤1 进入系统视图。
system-view

步骤2 进入需要加入SEP段的以太网接口视图。
interface interface-type interface-number步骤3 配置接口的链路类型为Trunk或Hybrid类型。
port link-type { trunk | hybrid }步骤4 去使能二层端口的STP功能。
stp disable步骤5 将二层端口加入指定SEP段，并为加入SEP段的二层端口设置不同的端口角色。
sep segment segment-id [ edge [ no-neighbor ] { primary | secondary } ]说明同一接口只允许加入两个SEP段。
----结束

#### 9.6.5 配置端口的阻塞方式

背景信息在SEP段中，为了防止形成环路而被阻塞的端口称为阻塞端口。
用户可通过配置端口阻塞方式来指定阻塞端口在网络中的位置。SEP支持阻塞端口方式如表9-13所示。
表 9-13 端口阻塞方式表

| 端口阻塞方式 | 说明 |
|---|---|
| 指定优先级最高的端口为阻塞端口 | 适用于网络规模较大的网络中。故障恢复后，SEP段上优先级最高的端口将成为阻塞端口。但是需要人为预先设置SEP段上的端口优先级。 |
| 指定SEP段中间位置的端口为阻塞端口 | 适用于网络中流量需要对称分布的场景中。故障恢复后，位于SEP段上中间位置的端口将成为阻塞端口。 |
| 根据用户配置的跳数指定阻塞端口 | 适用于网络规模较小的网络中。故障恢复后，根据用户配置的跳数阻塞指定端口。但是网络规划者需要熟悉整个SEP段的拓扑，并了解阻塞端口距离主边缘端口的跳数。 |
| 根据设备名+端口名指定阻塞端口 | 适用于网络规模较小的网络中。故障恢复后，根据设备名+端口名阻塞指定端口。但是网络规划者需要熟悉整个SEP上的设备名称和接口名称，并保证设备名称是唯一的。 |

请在主边缘端口或无邻居主边缘端口位于的设备上执行如下配置。

操作步骤步骤1 进入系统视图。
system-view步骤2 进入已经成功创建的SEP-Segment视图。
sep segment segment-id步骤3 配置端口的阻塞方式。
block port { sysname sysname interface { { xgigabitethernet | multige | gigabitethernet | eth-trunk | ethernet | 100ge | 40ge | 25ge | 10ge | 50ge | 200ge | 400ge | ge } interface-number | ifname } | hop hop- id | optimal | middle }缺省情况下，系统会自动协商出一个阻塞端口。协商的原则是从最后建立起来或故障恢复的那条链路的两个端口中协商出一个阻塞端口。
----结束后续处理如果端口阻塞方式选择指定优先级高的端口是阻塞端口，请在需要阻塞的接口视图下执行命令sep segment segment-id priority priority，将需要阻塞的端口优先级调高，保证故障恢复时，阻塞端口成功迁移到用户指定的端口。
缺省情况下，加入SEP段中的端口优先级是64。端口优先级的取值范围是1～128，取值越大，优先级越高。

#### 9.6.6 配置抢占模式

背景信息用户指定端口的阻塞方式后，阻塞端口是否从当前阻塞点迁移到用户指定的阻塞点，可以通过抢占和不抢占两种模式决定。如表9-14所示。
表 9-14 抢占功能模式

| 抢占功能模式 |  | 优点 | 缺点 |
|---|---|---|---|
| 不抢占模式 |  | 缺省情况下，SEP处于不抢占模式。不抢占模式下阻塞端口不会造成SEP段上的链路短暂中断。 | 阻塞端口是最后完成邻居协商的链路两端的其中一个端口。 |
| 抢占模式 | 延时抢占 | 无需人为干涉，每一次故障恢复，系统都能够自动完成每一次抢占，并保证当前阻塞点迁移到用户指定的阻塞点。 | 需要人为预先通过命令指定延时抢占，且抢占延时时间没有缺省值，用户必须通过命令配置抢占延时时间。延时抢占配置成功后，需要人为预先模拟一次故障，才能保证阻塞端口是用户指定的端口。 |

| 抢占功能模式 |  | 优点 | 缺点 |
|---|---|---|---|
|  | 手工抢占 | 可以人为控制当前阻塞点是否迁移到用户指定的阻塞点。 | 需要人为预先通过命令指定手工抢占。故障恢复后，当抢占动作完成，手工抢占不再起作用。为了保证下一次故障恢复后，当前阻塞点能够迁移到用户指定的阻塞点，需要再进行一次手工抢占配置。这增加了用户的维护量。 |

触发抢占必须同时满足以下条件：
● SEP段拓扑必须是完整。
● SEP段中已经成功选举出主边缘端口或无邻居主边缘端口。
● 主边缘端口或无邻居主边缘端口位于的设备上，已经灵活指定阻塞端口。
请在主边缘端口或无邻居主边缘端口位于的二层交换设备上执行如下配置。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入已经成功创建的SEP-Segment视图。
sep segment segment-id步骤3 在主边缘端口所在设备上配置SEP的抢占模式。
preempt { manual | delay seconds }缺省情况下，设备上没有配置抢占模式，即为不抢占模式。
----结束

#### 9.6.7 检查配置结果

操作步骤
● 执行命令display sep segment { segment-id | all }，查看SEP段的配置信息。
● 执行命令display sep interface [ { ifName | ifType ifNum } | segment segment-id ] [ verbose ]，查看本设备上加入SEP的端口信息。
● 执行命令display sep topology [ segment segment-id ] [ verbose ]，查看SEP段的拓扑状态信息。
----结束

### 9.7 配置SEP多实例

在 SEP 段中，如果不指定阻塞端口， SEP 段中的每个端口均有可能成为阻塞端口。通过灵活指定阻塞端口，可以使阻塞端口指定到预期位置，提升网络转发性能且更好支持SEP多实例场景下的流量负载分担。

#### 9.7.1 了解多实例

SEP多实例允许在一个物理环路配置两个SEP段。通过给每个SEP段配置不同的保护实例，实现业务流量的负载分担和链路备份。
如图9-11所示，在普通的SEP组网图中，一个物理环上只能配置一个SEP段，也只能指定一个阻塞点。当SEP段处于完整状态时，阻塞端口会阻止所有的业务数据通过。这样，所有业务数据在SEP段上只能通过主边缘端口侧的链路传输，副边缘端口侧的链路空闲，造成带宽浪费。
图 9-11 SEP 组网SEP多实例允许在一个物理环路配置两个逻辑环路，即两个SEP段。每一个SEP段上所有设备、端口角色、控制VLAN等都必须遵循基本的SEP原则。相应的，一个物理环路上有两个阻塞端口，各个阻塞端口分别检测物理环路的完整性，并相应的阻塞或放开，彼此互不影响。
一个物理环路上可以包含一个或两个SEP段，每个SEP段上均需要配置一个保护实例，每个保护实例代表一个VLAN范围。不同的SEP段计算出的拓扑仅对该SEP段有效，不影响其他SEP段。
通过给每个SEP段配置不同的保护实例，各阻塞端口只对本SEP段所保护的VLAN有效。属于不同VLAN的数据流量就可以通过不同的路径传输，从而实现业务流量的负载分担和链路备份。

图 9-12 SEP 多实例组网如图9-12所示，Device1～Device4组成的SEP多实例环上有两个SEP段。P1是ID为1的SEP段的阻塞端口，P2是ID为2的SEP段的阻塞端口。
● SEP段1上配置保护实例1，保护对应的VLAN100～VLAN200数据，其传输路径是Device1->Device2。P2作为SEP段2的阻塞端口，阻塞仅对VLAN201～VLAN400数据有效，不会影响VLAN100～VLAN200数据通过。
● SEP段2上配置保护实例2，保护对应的VLAN201～VLAN400数据，其传输路径是Device3->Device4。P1作为SEP段1的阻塞端口，阻塞仅对VLAN100～VLAN200数据有效，不会影响VLAN201～VLAN400数据通过。
当节点或链路故障时，各SEP段独立计算拓扑变化，更新各自节点上的LSA数据库。
如图9-13所示，Device3和Device4之间发生链路故障。此故障对SEP段1中，VLAN100～VLAN200数据传输路径无影响，但是阻断了SEP段中VLAN201～VLAN400数据的传输路径。

图 9-13 SEP 多实例链路故障示意Device3和Device4之间发生链路故障后，SEP段2中的设备Device3开始发送LSA报文通知SEP段2上的其他节点刷新各自的LSA数据库，阻塞端口放开并进入转发状态。SEP段2中的拓扑重新收敛后，VLAN201～VLAN400数据传输路径是Device3->Device1- >Device2。
当Device3和Device4之间链路故障恢复，SEP段2上的设备重新执行延时抢占，抢占延时时间超时后，P1点再次成为阻塞端口，并发送LSA报文通知SEP段2中各节点刷新各自的LSA数据库。SEP段2中的拓扑重新收敛后，VLAN201～VLAN400数据传输路径切回原来的路径Device3->Device4。

#### 9.7.2 配置多实例

SEP多实例允许在一个物理环路配置两个SEP段。通过给每个SEP段配置不同的保护实例，实现业务流量的负载分担和链路备份。
前提条件参照9.6 配置SEP基本功能，完成两个SEP段的相关配置。
背景信息典型组网如图9-14所示，在SEP段上部署多实例，不同的实例与不同的VLAN映射。这样属于不同VLAN的数据流量就可以通过不同的路径传输，从而实现流量的负载分担和链路备份，也解决了带宽浪费问题。

图 9-14 SEP 多实例典型组网说明SEP多实例只允许在一个物理环路上配置两个逻辑环路，即两个SEP段。两个SEP段需配置不同的阻塞端口和优先级。
在执行9.6.3 配置保护实例时，如果已按SEP多实例的要求完成多个保护实例的配置，请略过下面步骤。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入MST域视图。
stp region-configuration步骤3 配置保护实例与VLAN的映射关系。
instance instance-id vlan { vlan-id1 [ to vlan-id2 ] }&<1-10>参数instance-id必须与命令protected-instance { all | { instance-id1 [ to instance- id2 ] } &<1-10> }中指定的instance-id一致。
当需要将某个VLAN从一个Segment切换到另一个Segment时，建议先将阻塞端口关闭，否则可能会出现环路。当需要配置保护实例与MUX VLAN间的映射关系时，建议

同一个MUX VLAN下的主VLAN、互通型和隔离型从VLAN配置在同一个保护实例下，否则可能导致部分环路。
保护实例与VLAN的映射关系生效后，SEP段上端口的转发状态变化或拓扑变化只影响对应的VLAN，而不影响其他VLAN，从而保证业务数据可靠传输。
----结束

#### 9.7.3 检查配置结果

操作步骤
● 执行命令display stp region-configuration，查看当前生效的MST域配置信息。
----结束

### 9.8 配置网络拓扑变化通告

网络拓扑变化通告部署在连接上、下级网络的设备上，用于上、下级网络拓扑变化时发送拓扑变化通告通知对方网络，以便对方网络中的所有设备及时清除MAC地址表项和ARP表项，重新学习对方网络拓扑变化后的MAC地址，从而保证用户流量不中断。

#### 9.8.1 配置下级网络拓扑变化通告：SEP拓扑变化通告

背景信息SEP协议运行在接入层，为了便于上级网络及时感知接入层网络拓扑是否发生变化，需要在连接上、下层网络的设备上部署SEP拓扑变化通告。
当指定SEP段的拓扑发生变化，而没有及时通知到上级网络，那么上级网络的MAC地址表中仍然保留下游网络拓扑变化前的MAC地址表项，这样就会导致用户流量中断。
为了保证用户流量正常通信，需要部署下级网络向上级网络发送拓扑变化通告，用户可根据实际网络选择本SEP段的拓扑变化通知的指定对象。
当上级网络收到下游网络拓扑变化的消息后，会在本网络内发送TC报文，通知本网络内的所有设备清除MAC地址，重新学习下游网络拓扑变化后的MAC地址，从而保证用户流量不中断。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入已经成功创建的SEP-Segment视图。
sep segment segment-id步骤3 配置SEP拓扑变化通告。
tc-notify segment { segmentIdBgn [ to segmentIdEnd ] } &<1-10>缺省情况下，本SEP段不发送网络拓扑变化通告。
----结束

### 9.9 维护SEP

后续处理如果SEP段上存在多级环（3级或3级以上），当多条链路发送拓扑变化通告，将导致上级网络接收到多个相同的拓扑变化通告，使得上级网络处理有效报文的效率降低，此时需要抑制拓扑变化通告。抑制拓扑变化通告可避免上级网络同时处理多条相同的拓扑变化通告报文，使得上级网络在保护时间内仅处理3条不同源的拓扑变化通告报文，同时还可以避免SEP段上的设备受到TC（Topology Change）攻击。
在Sep-segment视图下，执行命令tc-protection interval interval-value，配置SEP拓扑变化保护时间间隔，抑制拓扑变化通告。
缺省情况下，SEP拓扑变化保护时间间隔是2秒，且2秒钟内只处理3个不同源的拓扑变化通告报文。
说明
● 当存在多级环（3级或3级以上）时必须配置此命令，否则采用缺省值。
● 配置较长的时间间隔，可以使SEP协议运行更稳定，但是会导致环路收敛性能降低。

#### 9.8.2 检查配置结果

操作步骤
● 执行命令display sep interface verbose，查看本设备加入SEP的端口信息。
● 在系统视图下执行命令oam-mgr进入AM管理视图，然后执行命令display this，查看上级网络拓扑变化通告的配置信息。
----结束维护
9.9 SEP查看错误信息日常维护中，可以查看是否存在SEP错误信息，如表9-15所示。
表 9-15 查看错误信息

| 操作 | 命令 |
|---|---|
| 显示SEP收到的错误报文计数以及最近收到的错误报文内容。 | display sep error packet |

清除统计信息日常维护中，还可以清除SEP统计信息，包括清除SEP段上指定接口的SEP协议报文统计信息、错误报文计数，如表9-16所示。
须知清除SEP的统计信息后，以前的信息将无法恢复，请务必仔细确认。

表 9-16 清除统计信息

| 操作 | 命令 |
|---|---|
| 清除SEP段上指定接口的SEP协议报文统计信息。 | reset sep interface { ifName | { ifType ifNum } } statistics |
| 清除SEP协议的错误报文计数。 | reset sep error packet statistics |

### 9.10 SEP配置举例

#### 9.10.1 举例：配置SEP封闭环

组网需求为了进行链路备份，提高网络可靠性，用户通常会使用冗余链路接入上层网络，但是使用冗余链路会在网络中产生环路。环路会造成报文在环路内不断的循环转发，最终导致广播风暴以及MAC地址表不稳定等故障现象，从而导致用户通信质量较差，甚至通信中断。为了阻塞冗余环路，并实现当环网上发生链路故障时，阻塞的冗余链路能够迅速恢复通信，可在环网上部署SEP协议。
该组网的特点是多台二层交换设备组成双归链路接入上级网络，位于上级网络的两台边缘设备之间是直连的方式。此组网位于汇聚层，完成单播业务及组播业务的二层透传功能。通过在汇聚层运行SEP协议，实现冗余保护倒换。
如图9-15所示，多台二层交换设备Device1～Device5形成环形网络。此种情况下在汇聚层运行SEP协议。
● 当环网上没有故障链路时，SEP能够消除以太网冗余环路。
● 当环网上发生链路故障时，SEP能够迅速恢复环网上各节点间通信通路。
图 9-15 SEP 封闭环组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。

配置思路采用如下的思路配置SEP封闭环：
1. 配置SEP基本功能：
a. 在Device1～Device5上配置Segment ID为1的SEP段和VLAN ID为10的控制VLAN。
b. 将环网上所有设备加入SEP段并配置Device1上接口10GE1/0/1和10GE1/0/3加入SEP段的端口角色。
c. 在端口角色为主边缘端口的设备上配置灵活指定阻塞端口的方式是依据端口优先级，优先阻塞优先级高的端口。
d. 配置加入SEP段的端口优先级。
配置Device3上的端口10GE1/0/2优先级最高，SEP段上其他的端口均采用缺省优先级，确保阻塞优先级最高的端口。
e. 在端口角色为主边缘端口的设备上配置SEP抢占模式是延时抢占。
2. 配置CE1、Device1～Device5二层转发功能。

操作步骤步骤1 配置SEP基本功能。
1. 配置Segment ID为1的SEP段和VLAN ID为10控制VLAN。
\# 配置Device1。
<HUAWEI> system-view [HUAWEI] sysname Device1 [Device1] sep segment 1 [Device1-sep-segment1] control-vlan 10 [Device1-sep-segment1] protected-instance all [Device1-sep-segment1] quit \# 配置Device2。
<HUAWEI> system-view [HUAWEI] sysname Device2 [Device2] sep segment 1 [Device2-sep-segment1] control-vlan 10 [Device2-sep-segment1] protected-instance all [Device2-sep-segment1] quit \# 配置Device3。
<HUAWEI> system-view [HUAWEI] sysname Device3 [Device3] sep segment 1 [Device3-sep-segment1] control-vlan 10 [Device3-sep-segment1] protected-instance all [Device3-sep-segment1] quit \# 配置Device4。
<HUAWEI> system-view [HUAWEI] sysname Device4 [Device4] sep segment 1 [Device4-sep-segment1] control-vlan 10 [Device4-sep-segment1] protected-instance all [Device4-sep-segment1] quit \# 配置Device5。
<HUAWEI> system-view [HUAWEI] sysname Device5 [Device5] sep segment 1 [Device5-sep-segment1] control-vlan 10 [Device5-sep-segment1] protected-instance all [Device5-sep-segment1] quit说明
– 控制VLAN的ID必须是没有被创建或使用的，但是控制VLAN创建后，在配置文件会自动显示创建普通VLAN的命令。
– 每个SEP段必须配置控制VLAN，当接口加入已经配置控制VLAN的SEP段后，接口将自动加入控制VLAN。
2. 将环网上的设备加入Segment1，并配置端口角色。
说明缺省情况下，二层端口上STP处于使能状态。在将端口加入SEP段之前，请先去使能STP。
\# 配置Device1的接口10GE1/0/1端口角色为主边缘端口、接口10GE1/0/3端口角色为副边缘端口。
[Device1] interface 10ge 1/0/1 [Device1-10GE1/0/1] port link-type hybrid [Device1-10GE1/0/1] stp disable [Device1-10GE1/0/1] sep segment 1 edge primary [Device1-10GE1/0/1] quit [Device1] interface 10ge 1/0/3 [Device1-10GE1/0/3] port link-type hybrid [Device1-10GE1/0/3] stp disable

[Device1-10GE1/0/3] sep segment 1 edge secondary [Device1-10GE1/0/3] quit \# 配置Device2。
[Device2] interface 10ge 1/0/1 [Device2-10GE1/0/1] port link-type hybrid [Device2-10GE1/0/1] stp disable [Device2-10GE1/0/1] sep segment 1 [Device2-10GE1/0/1] quit [Device2] interface 10ge 1/0/2 [Device2-10GE1/0/2] port link-type hybrid [Device2-10GE1/0/2] stp disable [Device2-10GE1/0/2] sep segment 1 [Device2-10GE1/0/2] quit \# 配置Device3。
[Device3] interface 10ge 1/0/1 [Device3-10GE1/0/1] port link-type hybrid [Device3-10GE1/0/1] stp disable [Device3-10GE1/0/1] sep segment 1 [Device3-10GE1/0/1] quit [Device3] interface 10ge 1/0/2 [Device3-10GE1/0/2] port link-type hybrid [Device3-10GE1/0/2] stp disable [Device3-10GE1/0/2] sep segment 1 [Device3-10GE1/0/2] quit \# 配置Device4。
[Device4] interface 10ge 1/0/1 [Device4-10GE1/0/1] port link-type hybrid [Device4-10GE1/0/1] stp disable [Device4-10GE1/0/1] sep segment 1 [Device4-10GE1/0/1] quit [Device4] interface 10ge 1/0/2 [Device4-10GE1/0/2] port link-type hybrid [Device4-10GE1/0/2] stp disable [Device4-10GE1/0/2] sep segment 1 [Device4-10GE1/0/2] quit \# 配置Device5。
[Device5] interface 10ge 1/0/1 [Device5-10GE1/0/1] port link-type hybrid [Device5-10GE1/0/1] stp disable [Device5-10GE1/0/1] sep segment 1 [Device5-10GE1/0/1] quit [Device5] interface 10ge 1/0/3 [Device5-10GE1/0/3] port link-type hybrid [Device5-10GE1/0/3] stp disable [Device5-10GE1/0/3] sep segment 1 [Device5-10GE1/0/3] quit
3. 配置灵活指定阻塞端口。
\# 在主边缘端口位于的设备 Device1 上配置阻塞端口的方式为依据端口优先级，优先阻塞优先级高的端口。
[Device1] sep segment 1 [Device1-sep-segment1] block port optimal [Device1-sep-segment1] quit
4. 配置Device3上的端口10GE1/0/2优先级。
[Device3] interface 10ge 1/0/2 [Device3-10GE1/0/2] sep segment 1 priority 128 [Device3-10GE1/0/2] quit
5. 配置抢占模式。
\# 在主边缘端口位于的设备 Device1 上配置抢占模式为延时抢占。
[Device1] sep segment 1 [Device1-sep-segment1] preempt delay 30 [Device1-sep-segment1] quit

说明
– 延时抢占时间没有缺省值，用户必须通过本命令配置延时抢占时间。
– 当最后一个端口故障恢复后，边缘端口将不再收到故障通告报文。主边缘端口在3秒内没有收到故障通告报文，立即启动延时定时器。延时定时器超时后，SEP段中的节点执行阻塞端口抢占。
所以，在此配置示例中，需要先人为制造端口故障，再恢复端口故障，延时抢占才能成功执行。例如：
在Device2设备上对接口10GE1/0/2执行shutdown命令，模拟端口故障。然后再在端口10GE1/0/2执行undo shutdown命令，端口故障恢复。
步骤2 配置CE和Device1～Device5的二层转发功能。
具体配置过程略。请参考本配置举例中的配置文件。
步骤3 验证配置结果。
● 对Device3上的接口10GE1/0/1执行命令shutdown模拟端口故障，在Device3上执行命令display sep interface查看接口10GE1/0/2能否从阻塞状态放开进入转发状态。
<Device3> display sep interface 10ge 1/0/2 SEP segment 1
---------------------------------------------------------------- Interface Port Role Neighbor Status Port Status
---------------------------------------------------------------- 10GE1/0/2 common up forwarding
----结束配置脚本Device1 \# sysname Device1 \# vlan batch 10 100 200 \# sep segment 1 control-vlan 10 block port optimal preempt delay 30 protected-instance 0 to 48 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 10 100 stp disable sep segment 1 edge primary \# interface 10GE1/0/2 port link-type hybrid port hybrid pvid vlan 200 port hybrid tagged vlan 100 port hybrid untagged vlan 200 \# interface 10GE1/0/3 port link-type hybrid port hybrid tagged vlan 10 100 200 stp disable sep segment 1 edge secondary \# return Device2

\# sysname Device2 \# vlan batch 10 100 \# sep segment 1 control-vlan 10 protected-instance 0 to 48 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 10 100 stp disable sep segment 1 \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 10 100 stp disable sep segment 1 \# return Device3 \# sysname Device3 \# vlan batch 10 100 \# sep segment 1 control-vlan 10 protected-instance 0 to 48 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 10 100 stp disable sep segment 1 \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 10 100 stp disable sep segment 1 sep segment 1 priority 128 \# interface 10GE1/0/3 port link-type hybrid port hybrid tagged vlan 100 \# return Device4 \# sysname Device4 \# vlan batch 10 100 \# sep segment 1 control-vlan 10 protected-instance 0 to 48 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 10 100 stp disable sep segment 1 \# interface 10GE1/0/2 port link-type hybrid

#### 9.10.2 举例：配置SEP多实例

port hybrid tagged vlan 10 100 stp disable sep segment 1 \# return Device5 \# sysname Device5 \# vlan batch 10 100 200 \# sep segment 1 control-vlan 10 protected-instance 0 to 48 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 10 100 stp disable sep segment 1 \# interface 10GE1/0/2 port link-type hybrid port hybrid pvid vlan 200 port hybrid tagged vlan 100 port hybrid untagged vlan 200 \# interface 10GE1/0/3 port link-type hybrid port hybrid tagged vlan 10 100 200 stp disable sep segment 1 \# return CE1 \# sysname CE1 \# vlan batch 100 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 100 \# return举例：配置 多实例
9.10.2 SEP组网需求在普通的SEP组网图中，一个物理环上只能配置一个SEP段，也只能指定一个阻塞点。
当SEP段处于完整状态时，阻塞端口会阻止所有的业务数据通过。这样，所有业务数据在SEP段上只能通过一条路径传输，阻塞端口侧的链路空闲，造成带宽浪费。
SEP多实例可解决带宽浪费问题，并实现负载分担。
图 9-16 SEP 多实例封闭环组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。

如图9-16所示，多台二层交换设备Device1～Device4形成环形网络接入上层网络。在汇聚层上运行SEP协议。在Device1～Device4上配置SEP多实例，通过两个SEP段解决带宽浪费问题，实现负载分担并提供链路备份。
配置思路采用如下的思路配置SEP多实例封闭环：
1. 配置SEP基本功能：
a. 在Device1～Device4上创建两个SEP段和一个控制VLAN。
不同SEP段可以使用相同ID的控制VLAN。

b. 配置SEP保护实例，并将实例与用户VLAN映射，确保端口的转发状态变化或
拓扑变化只影响对应的VLAN，而不影响其他VLAN，保证业务数据可靠传
输。
c. 将环网上所有设备加入SEP段，并配置Device1上接口10GE1/0/1是主边缘端
口、10GE1/0/3是副边缘端口。
d. 在端口角色为主边缘端口的设备上配置端口阻塞方式，灵活指定阻塞端口。
e. 配置SEP抢占模式，确保故障恢复时用户指定的阻塞端口生效。
2. 配置CE1、CE2、Device1～Device4二层转发功能。
操作步骤
步骤1 创建SEP段和控制VLAN。
● 配置Segment ID为1的SEP段和VLAN ID为10的控制VLAN。
\# 配置Device1。
<HUAWEI> system-view
[HUAWEI] sysname Device1
[Device1] sep segment 1
[Device1-sep-segment1] control-vlan 10
[Device1-sep-segment1] quit
\# 配置Device2。
<HUAWEI> system-view
[HUAWEI] sysname Device2
[Device2] sep segment 1
[Device2-sep-segment1] control-vlan 10
[Device2-sep-segment1] quit
\# 配置Device3。
<HUAWEI> system-view
[HUAWEI] sysname Device3
[Device3] sep segment 1
[Device3-sep-segment1] control-vlan 10
[Device3-sep-segment1] quit
\# 配置Device4。
<HUAWEI> system-view
[HUAWEI] sysname Device4
[Device4] sep segment 1
[Device4-sep-segment1] control-vlan 10
[Device4-sep-segment1] quit
● 配置Segment ID为2的SEP段和VLAN ID为10的控制VLAN。
\# 配置Device1。
[Device1] sep segment 2
[Device1-sep-segment2] control-vlan 10
[Device1-sep-segment2] quit
\# 配置Device2。
[Device2] sep segment 2
[Device2-sep-segment2] control-vlan 10
[Device2-sep-segment2] quit
\# 配置Device3。
[Device3] sep segment 2
[Device3-sep-segment2] control-vlan 10
[Device3-sep-segment2] quit
\# 配置 Device4 。
[Device4] sep segment 2
[Device4-sep-segment2] control-vlan 10
[Device4-sep-segment2] quit

说明
● 控制VLAN的ID必须是没有被创建或使用的。
● 控制VLAN成功创建后，配置文件会自动显示创建普通VLAN的命令。
● 每个SEP段必须配置控制VLAN，当接口加入已经配置控制VLAN的SEP段后，接口将自动加入控制VLAN。不需使用命令port trunk allow-pass vlan配置，该命令会自动显示在加入SEP段的接口配置文件中。
步骤2 配置SEP段保护实例，并将实例与用户VLAN映射。
\# 配置Device1。
[Device1] vlan batch 100 to 500 [Device1] sep segment 1 [Device1-sep-segment1] protected-instance 1 [Device1-sep-segment1] quit [Device1] sep segment 2 [Device1-sep-segment2] protected-instance 2 [Device1-sep-segment2] quit [Device1] stp region-configuration [Device1-mst-region] instance 1 vlan 100 to 300 [Device1-mst-region] instance 2 vlan 301 to 500 [Device1-mst-region] quit Device2～Device4配置略。Device2～Device4配置与Device1配置类似，具体配置请参见本示例配置文件。
步骤3 将环网上的设备加入SEP段，并配置端口角色。
说明缺省情况下，二层端口上STP处于使能状态。在将端口加入SEP段之前，请先去使能STP。
\# 配置Device1的端口10GE1/0/1端口角色为主边缘端口，10GE1/0/3端口角色为副边缘端口。
[Device1] interface 10ge 1/0/1 [Device1-10GE1/0/1] port link-type hybrid [Device1-10GE1/0/1] stp disable [Device1-10GE1/0/1] sep segment 1 edge primary [Device1-10GE1/0/1] sep segment 2 edge primary [Device1-10GE1/0/1] quit [Device1] interface 10ge 1/0/3 [Device1-10GE1/0/3] port link-type hybrid [Device1-10GE1/0/3] stp disable [Device1-10GE1/0/3] sep segment 1 edge secondary [Device1-10GE1/0/3] sep segment 2 edge secondary [Device1-10GE1/0/3] quit \# 配置Device2。
[Device2] interface 10ge 1/0/1 [Device2-10GE1/0/1] port link-type hybrid [Device2-10GE1/0/1] stp disable [Device2-10GE1/0/1] sep segment 1 [Device2-10GE1/0/1] sep segment 2 [Device2-10GE1/0/1] quit [Device2] interface 10ge 1/0/2 [Device2-10GE1/0/2] port link-type hybrid [Device2-10GE1/0/2] stp disable [Device2-10GE1/0/2] sep segment 1 [Device2-10GE1/0/2] sep segment 2 [Device2-10GE1/0/2] quit \# 配置Device3。

[Device3] interface 10ge 1/0/1 [Device3-10GE1/0/1] port link-type hybrid [Device3-10GE1/0/1] stp disable [Device3-10GE1/0/1] sep segment 1 [Device3-10GE1/0/1] sep segment 2 [Device3-10GE1/0/1] quit [Device3] interface 10ge 1/0/2 [Device3-10GE1/0/2] port link-type hybrid [Device3-10GE1/0/2] stp disable [Device3-10GE1/0/2] sep segment 1 [Device3-10GE1/0/2] sep segment 2 [Device3-10GE1/0/2] quit配置Device4。
\# [Device4] interface 10ge 1/0/1 [Device4-10GE1/0/1] port link-type hybrid [Device4-10GE1/0/1] stp disable [Device4-10GE1/0/1] sep segment 1 [Device4-10GE1/0/1] sep segment 2 [Device4-10GE1/0/1] quit [Device4] interface 10ge 1/0/3 [Device4-10GE1/0/3] port link-type hybrid [Device4-10GE1/0/3] stp disable [Device4-10GE1/0/3] sep segment 1 [Device4-10GE1/0/3] sep segment 2 [Device4-10GE1/0/3] quit步骤4 灵活指定阻塞端口。
\# 在主边缘端口所在的设备Device1上配置阻塞端口的方式是设备名+端口名，抢占模式是延时抢占。
说明
● 在本配置举例中，需要模拟端口故障然后恢复来完成延时抢占，为保证延时抢占功能在两个SEP段上都生效，需模拟位于两个SEP段上的端口故障。比如：
– 在SEP segment 1上，在Device2的10GE1/0/1接口视图下执行命令shutdown来模拟端口故障，然后执行命令undo shutdown来模拟端口故障恢复。
– 在SEP segment 2上，在Device3的10GE1/0/1接口视图下执行命令shutdown来模拟端口故障，然后执行命令undo shutdown来模拟端口故障恢复。
[Device1] sep segment 1 [Device1-sep-segment1] block port sysname Device3 interface 10ge 1/0/1 [Device1-sep-segment1] preempt delay 15 [Device1-sep-segment1] quit [Device1] sep segment 2 [Device1-sep-segment2] block port sysname Device2 interface 10ge 1/0/1 [Device1-sep-segment2] preempt delay 15 [Device1-sep-segment2] quit步骤5 配置CE1、CE2、Device1～Device4的二层转发功能。
具体配置过程略。请参考本配置举例中的配置文件。
步骤6 验证配置结果。
模拟故障产生情况下，查看阻塞端口是否能够从阻塞状态放开进入转发状态。
将Device2上的端口10GE1/0/1shutdown模拟端口故障。
在Device3上执行命令display sep interface，查看在Segment 1中端口10GE1/0/1能否从阻塞状态放开进入转发状态。
<Device3> display sep interface 10ge 1/0/1 SEP segment 1
----------------------------------------------------------------

Interface Port Role Neighbor Status Port Status
---------------------------------------------------------------- 10GE1/0/1 common up forwarding SEP segment 2
---------------------------------------------------------------- Interface Port Role Neighbor Status Port Status
---------------------------------------------------------------- 10GE1/0/1 common up forwarding从上述表项可以发现10GE1/0/1的状态可以成功从阻塞状态进入转发状态，Segment 1中转发路径变化并没有影响Segment 2的转发路径。
----结束配置脚本Device1 \# sysname Device1 \# vlan batch 10 100 to 500 \# stp region-configuration instance 1 vlan 100 to 300 instance 2 vlan 301 to 500 \# sep segment 1 control-vlan 10 block port sysname Device3 interface 10GE1/0/1 preempt delay 15 protected-instance 1 sep segment 2 control-vlan 10 block port sysname Device2 interface 10GE1/0/1 preempt delay 15 protected-instance 2 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 10 100 to 500 stp disable sep segment 1 edge primary sep segment 2 edge primary \# interface 10GE1/0/3 port link-type hybrid port hybrid tagged vlan 10 100 to 500 stp disable sep segment 1 edge secondary sep segment 2 edge secondary \# return Device2 \# sysname Device2 \# vlan batch 10 100 to 500 \# stp region-configuration instance 1 vlan 100 to 300 instance 2 vlan 301 to 500 \# sep segment 1 control-vlan 10 protected-instance 1 sep segment 2 control-vlan 10

protected-instance 2 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 10 100 to 500 stp disable sep segment 1 sep segment 2 \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 10 100 to 500 stp disable sep segment 1 sep segment 2 \# interface 10GE1/0/3 port link-type hybrid port hybrid tagged vlan 100 to 300 \# return Device3 \# sysname Device3 \# vlan batch 10 100 to 500 \# stp region-configuration instance 1 vlan 100 to 300 instance 2 vlan 301 to 500 \# sep segment 1 control-vlan 10 protected-instance 1 sep segment 2 control-vlan 10 protected-instance 2 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 10 100 to 500 stp disable sep segment 1 sep segment 2 \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 10 100 to 500 stp disable sep segment 1 sep segment 2 \# interface 10GE1/0/3 port link-type hybrid port hybrid tagged vlan 301 to 500 \# return Device4 \# sysname Device4 \# vlan batch 10 60 100 to 500 \# stp region-configuration instance 1 vlan 100 to 300 instance 2 vlan 301 to 500 \# sep segment 1

control-vlan 10 protected-instance 1 sep segment 2 control-vlan 10 protected-instance 2 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 10 100 to 500 stp disable sep segment 1 sep segment 2 \# interface 10GE1/0/3 port link-type hybrid port hybrid tagged vlan 10 100 to 500 stp disable sep segment 1 sep segment 2 \# return CE1 \# sysname CE1 \# vlan batch 100 to 300 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 100 to 300 \# return CE2 \# sysname CE2 \# vlan batch 301 to 500 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 301 to 500 \# return

#### 9.10.3 举例：配置SEP多环

组网需求为了进行链路备份，提高网络可靠性，用户通常会使用冗余链路接入上层网络，但是使用冗余链路会在网络中产生环路。环路会造成报文在环路内不断的循环转发，最终导致广播风暴以及MAC地址表不稳定等故障现象，从而导致用户通信质量较差，甚至通信中断。为了阻塞冗余环路，并实现当环网上发生链路故障时，阻塞的冗余链路能够迅速恢复通信，可在环网上部署SEP协议。
该组网的特点是接入层和汇聚层均由多台二层交换设备构成环形网络，通过在接入层和汇聚层运行SEP协议，实现接入层和汇聚层冗余保护倒换。
如图 9-17 所示，接入层和汇聚层由多台二层交换设备构成环形网络。在接入层、汇聚层运行SEP协议。当环网上没有故障链路时，SEP能够消除以太网冗余环路。当环网上发生链路故障时，SEP能够迅速恢复环网上各节点间通信通路。

图 9-17 SEP 多环组网图说明本例中interface1、interface2、interface3、interface4分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3、10GE1/0/4。

配置思路采用如下的思路配置SEP多环：
1. 配置SEP基本功能：
a. 配置Segment ID分别为1、2、3的SEP段，VLAN ID分别为10、20和30的控制VLAN。
▪在Device1～Device5上配置Segment ID为1的SEP段和VLAN ID为10的控制VLAN。
▪在Device2、Device6～Device8和Device3上配置Segment ID为2的SEP段和VLAN ID为20的控制VLAN。
▪在Device3、Device9～Device11和Device4上配置Segment ID为3的SEP段和VLAN ID为30的控制VLAN。
b. 将环网上的设备加入SEP段，并配置SEP段边缘设备上接口加入SEP段中的端口角色。
▪将 Device1 ～ Device5 构成环网的接口加入 Segment ID 为 1 的 SEP 段，并配置Device1上接口10GE1/0/1和10GE1/0/3加入SEP段的端口角色。
▪将Device2上接口10GE1/0/2，Device6～Device8上两个接口及Device3上的接口10GE1/0/2加入Segment ID为2的SEP段，并分别配置Device2和Device3上接口10GE1/0/2加入SEP段的端口角色。
▪将Device3上接口10GE1/0/1，Device9～Device11上两个接口及Device4上的接口10GE1/0/1加入Segment ID为3的SEP段，并分别配置Device3和Device4上接口10GE1/0/1加入SEP段的端口角色。
c. 在端口角色为主边缘端口的设备上配置灵活指定阻塞端口。
▪Segment1采用的阻塞端口方式是依据端口优先级，优先阻塞优先级高的端口。
▪Segment2采用的阻塞端口方式是依据设备名+接口名。
▪Segment3采用的阻塞端口方式是依据用户配置的跳数指定阻塞端口。
在端口角色为主边缘端口的设备上配置SEP抢占模式。
d.
Segment1采用的抢占模式是延时抢占；Segment2和Segment3采用的抢占模式是手工抢占。
e. 在SEP段之间相交的设备Device2、Device3和Device4上配置SEP拓扑变化通告。
2. 配置CE1、CE2、Device1～Device11二层转发功能。
操作步骤步骤1 配置SEP基本功能。
1. 配置Segment ID分别为1、2、3的SEP段，并按图9-17所示，配置VLAN ID为
10、20、30的控制VLAN。
\# 配置Device1。
<HUAWEI> system-view [HUAWEI] sysname Device1 [Device1] sep segment 1

[Device1-sep-segment1] control-vlan 10 [Device1-sep-segment1] protected-instance all [Device1-sep-segment1] quit \# 配置Device2。
<HUAWEI> system-view [HUAWEI] sysname Device2 [Device2] sep segment 1 [Device2-sep-segment1] control-vlan 10 [Device2-sep-segment1] protected-instance all [Device2-sep-segment1] quit [Device2] sep segment 2 [Device2-sep-segment2] control-vlan 20 [Device2-sep-segment2] protected-instance all [Device2-sep-segment2] quit \# 配置Device3。
<HUAWEI> system-view [HUAWEI] sysname Device3 [Device3] sep segment 1 [Device3-sep-segment1] control-vlan 10 [Device3-sep-segment1] protected-instance all [Device3-sep-segment1] quit [Device3] sep segment 2 [Device3-sep-segment2] control-vlan 20 [Device3-sep-segment2] protected-instance all [Device3-sep-segment2] quit [Device3] sep segment 3 [Device3-sep-segment3] control-vlan 30 [Device3-sep-segment3] protected-instance all [Device3-sep-segment3] quit \# 配置Device4。
<HUAWEI> system-view [HUAWEI] sysname Device4 [Device4] sep segment 1 [Device4-sep-segment1] control-vlan 10 [Device4-sep-segment1] protected-instance all [Device4-sep-segment1] quit [Device4] sep segment 3 [Device4-sep-segment3] control-vlan 30 [Device4-sep-segment3] protected-instance all [Device4-sep-segment3] quit \# 配置Device5。
<HUAWEI> system-view [HUAWEI] sysname Device5 [Device5] sep segment 1 [Device5-sep-segment1] control-vlan 10 [Device5-sep-segment1] protected-instance all [Device5-sep-segment1] quit \# 配置Device6～Device11。
Device6～Device11的配置与Device1～Device5的配置类似，主要区别在于不同SEP段配置的控制VLAN不同。
具体配置过程略。请参见本示例的配置文件。
说明
– 控制VLAN的ID必须是没有被创建或使用的，但是控制VLAN创建后，在配置文件会自动显示创建普通VLAN的命令。
– 每个 SEP 段必须配置控制 VLAN ，当接口加入已经配置控制 VLAN 的 SEP 段后，接口将自动加入控制VLAN。
2. 按图9-17所示，将环网上的设备加入指定SEP段，并设置端口角色。

说明缺省情况下，二层端口上STP处于使能状态。在将端口加入SEP段之前，请先去使能STP。
\# 配置Device1的接口10GE1/0/1端口角色为主边缘端口、接口10GE1/0/3端口角色为副边缘端口。
[Device1] interface 10ge 1/0/1 [Device1-10GE1/0/1] port link-type hybrid [Device1-10GE1/0/1] stp disable [Device1-10GE1/0/1] sep segment 1 edge primary [Device1-10GE1/0/1] quit [Device1] interface 10ge 1/0/3 [Device1-10GE1/0/3] port link-type hybrid [Device1-10GE1/0/3] stp disable [Device1-10GE1/0/3] sep segment 1 edge secondary [Device1-10GE1/0/3] quit \# 配置Device2。
[Device2] interface 10ge 1/0/1 [Device2-10GE1/0/1] port link-type hybrid [Device2-10GE1/0/1] stp disable [Device2-10GE1/0/1] sep segment 1 [Device2-10GE1/0/1] quit [Device2] interface 10ge 1/0/3 [Device2-10GE1/0/3] port link-type hybrid [Device2-10GE1/0/3] stp disable [Device2-10GE1/0/3] sep segment 1 [Device2-10GE1/0/3] quit [Device2] interface 10ge 1/0/2 [Device2-10GE1/0/2] port link-type hybrid [Device2-10GE1/0/2] stp disable [Device2-10GE1/0/2] sep segment 2 edge primary [Device2-10GE1/0/2] quit \# 配置Device3。
[Device3] interface 10ge 1/0/3 [Device3-10GE1/0/3] port link-type hybrid [Device3-10GE1/0/3] stp disable [Device3-10GE1/0/3] sep segment 1 [Device3-10GE1/0/3] quit [Device3] interface 10ge 1/0/4 [Device3-10GE1/0/4] port link-type hybrid [Device3-10GE1/0/4] stp disable [Device3-10GE1/0/4] sep segment 1 [Device3-10GE1/0/4] quit [Device3] interface 10ge 1/0/2 [Device3-10GE1/0/2] port link-type hybrid [Device3-10GE1/0/2] stp disable [Device3-10GE1/0/2] sep segment 2 edge secondary [Device3-10GE1/0/2] quit [Device3] interface 10ge 1/0/1 [Device3-10GE1/0/1] port link-type hybrid [Device3-10GE1/0/1] stp disable [Device3-10GE1/0/1] sep segment 3 edge secondary [Device3-10GE1/0/1] quit \# 配置Device4。
[Device4] interface 10ge 1/0/2 [Device4-10GE1/0/2] port link-type hybrid [Device4-10GE1/0/2] stp disable [Device4-10GE1/0/2] sep segment 1 [Device4-10GE1/0/2] quit [Device4] interface 10ge 1/0/3 [Device4-10GE1/0/3] port link-type hybrid [Device4-10GE1/0/3] stp disable [Device4-10GE1/0/3] sep segment 1 [Device4-10GE1/0/3] quit [Device4] interface 10ge 1/0/1

[Device4-10GE1/0/1] port link-type hybrid [Device4-10GE1/0/1] stp disable [Device4-10GE1/0/1] sep segment 3 edge primary [Device4-10GE1/0/1] quit \# 配置Device5。
[Device5] interface 10ge 1/0/1 [Device5-10GE1/0/1] port link-type hybrid [Device5-10GE1/0/1] stp disable [Device5-10GE1/0/1] sep segment 1 [Device5-10GE1/0/1] quit [Device5] interface 10ge 1/0/3 [Device5-10GE1/0/3] port link-type hybrid [Device5-10GE1/0/3] stp disable [Device5-10GE1/0/3] sep segment 1 [Device5-10GE1/0/3] quit \# 配置Device6～Device11。
Device6～Device11的配置与Device1～Device5的配置类似，主要区别在于Device6～Device11上加入SEP段的端口不需要指定端口角色。
具体配置过程略。请参见本示例的配置文件。
3. 配置灵活指定阻塞端口。
\# 在Segment1中主边缘端口位于的设备Device1上配置阻塞端口的方式为依据端口优先级，优先阻塞优先级高的端口。
[Device1] sep segment 1 [Device1-sep-segment1] block port optimal [Device1-sep-segment1] quit \# 配置Device3上的端口10GE1/0/4优先级为128，优先阻塞优先级高的端口。
[Device3] interface 10ge 1/0/4 [Device3-10GE1/0/4] sep segment 1 priority 128 [Device3-10GE1/0/4] quit Segment1中的其他端口均采用默认优先级。
\# 在Segment2中主边缘端口位于的设备Device2上配置阻塞端口的方式为依据设备名+接口名。
用户在配置前，可通过命令display sep topology查看当前环的拓扑信息，获取到拓扑中所有端口信息，然后指定设备名和端口名。
[Device2] sep segment 2 [Device2-sep-segment2] block port sysname Device7 interface 10GE1/0/1 [Device2-sep-segment2] quit \# 在Segment3中主边缘端口位于的设备Device4上配置阻塞端口的方式为依据用户配置的跳数指定阻塞端口。
[Device4] sep segment 3 [Device4-sep-segment3] block port hop 5 [Device4-sep-segment3] quit说明SEP约定，主边缘端口的跳数为1，主边缘端口的邻居端口的跳数为2。跳数是沿着主边缘端口的下游邻居方向依次增加。
4. 配置抢占模式。
\# 在Segment1中主边缘端口位于的设备Device1上配置抢占模式为延时抢占。
[Device1] sep segment 1 [Device1-sep-segment1] preempt delay 30 [Device1-sep-segment1] quit

说明
– 延时抢占时间没有缺省值，用户必须通过本命令配置延时抢占时间。
– 当最后一个端口故障恢复后，边缘端口将不再收到故障通告报文。主边缘端口在3秒内没有收到故障通告报文，立即启动延时定时器。延时定时器超时后，SEP段中的节点执行阻塞端口抢占。
所以，在此配置示例中，需要先人为制造端口故障，再恢复端口故障，延时抢占才能成功执行。例如：
在Device2设备上对接口10GE1/0/2执行shutdown命令，模拟端口故障。然后再在端口10GE1/0/2执行undo shutdown命令，端口故障恢复。
\# 在Segment2中主边缘端口位于的设备Device2上配置抢占模式为手工抢占。
[Device2] sep segment 2 [Device2-sep-segment2] preempt manual [Device2-sep-segment2] quit \# 在Segment3中主边缘端口位于的设备Device4上配置抢占模式为手工抢占。
[Device4] sep segment 3 [Device4-sep-segment3] preempt manual [Device4-sep-segment3] quit
5. 配置SEP拓扑变化通告。
在Segment2中配置Segment2的拓扑变化通告给Segment1。
\# \# 配置Device2。
[Device2] sep segment 2 [Device2-sep-segment2] tc-notify segment 1 [Device2-sep-segment2] quit \# 配置Device3。
[Device3] sep segment 2 [Device3-sep-segment2] tc-notify segment 1 [Device3-sep-segment2] quit \# 在Segment3中配置Segment3的拓扑变化通告给Segment1。
\# 配置Device3。
[Device3] sep segment 3 [Device3-sep-segment3] tc-notify segment 1 [Device3-sep-segment3] quit \# 配置Device4。
[Device4] sep segment 3 [Device4-sep-segment3] tc-notify segment 1 [Device4-sep-segment3] quit说明SEP拓扑通告用于下级网络向上级网络通告，部署于SEP段之间相交的设备上。
步骤2 配置CE和Device1～Device11的二层转发功能。
具体配置过程略。请参考本配置举例中的配置文件。
步骤3 验证配置结果。
上述配置成功后，执行以下操作，验证配置结果。
对Device2上的接口10GE1/0/1执行命令shutdown模拟端口故障，在Device3上执行命令 display sep interface 查看接口 10GE1/0/4 能否从阻塞状态放开进入转发状态。
<Device3> display sep interface 10ge 1/0/4 SEP segment 1
---------------------------------------------------------------- Interface Port Role Neighbor Status Port Status

----------------------------------------------------------------
10GE1/0/4 common up forwarding
----结束
配置脚本
Device1
\#
sysname Device1
\#
vlan batch 10 100 200 300
\#
sep segment 1
control-vlan 10
block port optimal
preempt delay 30
protected-instance 0 to 48
\#
interface 10GE1/0/1
port link-type hybrid
port hybrid tagged vlan 10 100 200
stp disable
sep segment 1 edge primary
\#
interface 10GE1/0/2
port link-type hybrid
port hybrid pvid vlan 300
port hybrid tagged vlan 100 200
port hybrid untagged vlan 300
\#
interface 10GE1/0/3
port link-type hybrid
port hybrid tagged vlan 10 100 200 300
stp disable
sep segment 1 edge secondary
\#
return
Device2
\#
sysname Device2
\#
vlan batch 10 20 100 200
\#
sep segment 1
control-vlan 10
protected-instance 0 to 48
sep segment 2
control-vlan 20
block port sysname Device7 interface 10GE1/0/1
tc-notify segment 1
protected-instance 0 to 48
\#
interface 10GE1/0/1
port link-type hybrid
port hybrid tagged vlan 10 100 200
stp disable
sep segment 1
\#
interface 10GE1/0/2
port link-type hybrid
port hybrid tagged vlan 20 200
stp disable
sep segment 2 edge primary
\#
interface 10GE1/0/3
port link-type hybrid

port hybrid tagged vlan 10 100 200 stp disable sep segment 1 \# return Device3 \# sysname Device3 \# vlan batch 10 20 30 100 200 \# sep segment 1 control-vlan 10 protected-instance 0 to 48 sep segment 2 control-vlan 20 tc-notify segment 1 protected-instance 0 to 48 sep segment 3 control-vlan 30 tc-notify segment 1 protected-instance 0 to 48 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 30 100 stp disable sep segment 3 edge secondary \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 20 200 stp disable sep segment 2 edge secondary \# interface 10GE1/0/3 port link-type hybrid port hybrid tagged vlan 10 100 200 stp disable sep segment 1 \# interface 10GE1/0/4 port link-type hybrid port hybrid tagged vlan 10 100 200 stp disable sep segment 1 sep segment 1 priority 128 \# return Device4 \# sysname Device4 \# vlan batch 10 30 100 200 \# sep segment 1 control-vlan 10 protected-instance 0 to 48 sep segment 3 control-vlan 30 block port hop 5 tc-notify segment 1 protected-instance 0 to 48 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 30 100 stp disable

sep segment 3 edge primary \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 10 100 200 stp disable sep segment 1 \# interface 10GE1/0/3 port link-type hybrid port hybrid tagged vlan 10 100 200 stp disable sep segment 1 \# return Device5 \# sysname Device5 \# vlan batch 10 100 200 300 \# sep segment 1 control-vlan 10 protected-instance 0 to 48 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 10 100 200 stp disable sep segment 1 \# interface 10GE1/0/2 port link-type hybrid port hybrid pvid vlan 300 port hybrid tagged vlan 100 200 port hybrid untagged vlan 300 \# interface 10GE1/0/3 port link-type hybrid port hybrid tagged vlan 10 100 200 300 stp disable sep segment 1 \# return Device6 \# sysname Device6 \# vlan batch 20 200 \# sep segment 2 control-vlan 20 protected-instance 0 to 48 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 20 200 stp disable sep segment 2 \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 20 200 stp disable sep segment 2 \# return

Device7 \# sysname Device7 \# vlan batch 20 200 \# sep segment 2 control-vlan 20 protected-instance 0 to 48 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 20 200 stp disable sep segment 2 \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 20 200 stp disable sep segment 2 \# interface 10GE1/0/3 port link-type hybrid port hybrid tagged vlan 200 \# return Device8 \# sysname Device8 \# vlan batch 20 200 \# sep segment 2 control-vlan 20 protected-instance 0 to 48 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 20 200 stp disable sep segment 2 \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 20 200 stp disable sep segment 2 \# return Device9 \# sysname Device9 \# vlan batch 30 100 \# sep segment 3 control-vlan 30 protected-instance 0 to 48 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 30 100 stp disable sep segment 3 \# interface 10GE1/0/2

port link-type hybrid port hybrid tagged vlan 30 100 stp disable sep segment 3 \# return Device10 \# sysname Device10 \# vlan batch 30 100 \# sep segment 3 control-vlan 30 protected-instance 0 to 48 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 30 100 stp disable sep segment 3 \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 30 100 stp disable sep segment 3 \# interface 10GE1/0/3 port link-type hybrid port hybrid tagged vlan 100 \# return Device11 \# sysname Device11 \# vlan batch 30 100 \# sep segment 3 control-vlan 30 protected-instance 0 to 48 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 30 100 stp disable sep segment 3 \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 30 100 stp disable sep segment 3 \# return CE1 \# sysname CE1 \# vlan batch 100 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 100 \# return

CE2 \# sysname CE2 \# vlan batch 200 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 200 \# return
