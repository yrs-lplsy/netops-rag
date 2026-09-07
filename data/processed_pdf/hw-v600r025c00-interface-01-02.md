# S1700, S5700, S6700 V600R025C00 配置指南-接口管理 01-02 接口基础配置

## 2 接口基础配置

2接口基础配置

### 2.1 接口简介

2.2 接口基础配置注意事项
2.3 配置接口的描述信息
2.4 配置接口的MTU值
2.5 配置流量统计时间间隔
2.6 配置开启或关闭接口
2.7 维护接口
2.1 接口简介

#### 2.1.1 接口分类

接口是设备与网络中的其他设备交换数据并相互作用的部件，分为物理接口和逻辑接口两类。
物理接口物理接口是真实存在的、有器件支持的接口。物理接口分为管理接口和业务接口。不同硬件设备支持的物理接口不同，具体请参见《了解产品-硬件描述》中机箱的“接口”信息。例如如何确认设备是否支持MEth接口，如果“接口”信息中有ETH类型接口，则说明该设备支持MEth接口，如果“接口”信息中没有ETH类型接口，则说明该设备不支持MEth接口。
管理接口管理接口不承担业务传输，主要为用户提供配置管理支持，也就是用户通过此类接口可以登录到设备，并进行配置和管理操作。关于管理接口的详细配置，请参见《CLI配置指南 - 基础配置》中的“首次登录设备”。
设备支持的管理接口如表2-1所示：

表 2-1 管理接口

| 接口名称 | 接口描述 | 接口用途 |
|---|---|---|
| Console 接口 | 遵循EIA/TIA-232标准，接口类型是DCE。 | 该接口和配置终端的COM串口连接，用于搭建现场配置环境。 |
| MEth接口 | 遵循10/100/1000BASE-TX标准。 | 该接口和配置终端或网管站的网口连接，用于搭建现场或远程配置环境。 |

说明设备是否支持MEth接口，请参见《了解产品-硬件描述》中机箱的“接口”信息，如果“接口”信息中有ETH类型接口，则说明该设备支持MEth接口，如果“接口”信息中没有ETH类型接口，则说明该设备不支持MEth接口。
业务接口业务接口需要承担业务传输。业务接口有时也被称为端口，为便于描述，在本手册中，统一描述为接口。
设备支持的业务接口如表2-2所示。
表 2-2 业务接口

| 接口类型 | 描述 |
|---|---|
| 三层以太网接口 | 接口工作在网络层，可以配置IPv4/IPv6地址，处理三层协议，提供路由功能。 |
| 二层以太网接口 | 接口工作在数据链路层，处理二层协议，实现二层快速转发。 |
| MultiGE接口 | 接口工作在数据链路层或网络层： ● 工作在数据链路层：处理二层协议，实现二层快速转发。 ● 工作在网络层：处理三层协议，提供路由功能。 MultiGE接口支持的最大速率为10000Mbit/s。 |

逻辑接口逻辑接口是指能够实现数据交换功能但物理上不存在、需要通过配置建立的接口。逻辑接口需要承担业务传输。
设备支持的逻辑接口如表2-3所示。

表 2-3 逻辑接口分类

| 接口类型 | 接口描述 | 应用场景 |
|---|---|---|
| VLANIF 接口 | VLANIF接口是基于VLAN的具有三层特性的逻辑接口，每个VLAN 对应一个VLANIF接口。 | VLANIF接口用于实现不同VLAN间且不同网段的用户进行三层互通。由于配置较为简单，是实现VLAN间互通最常用的一种技术。在为 VLANIF接口配置IP地址后，该接口即可作为本VLAN内用户的网关，对需要跨网段的报文进行基于IP地址的三层转发。如果存在多个不同网段的情况，而这些网段的用户都需要实现互通，则需要在VLANIF接口上配置一个主IP地址和多个从IP地址。 |
| Eth- Trunk接口 | Eth-Trunk接口是将多个以太网接口捆绑成的一个具有二层特性或三层特性的逻辑接口。捆绑在一起的每个以太网接口称为成员接口。 | Eth-Trunk接口比以太网接口具有更大的带宽和更高的可靠性，用于链路聚合场景。 |
| 以太网二层子接口 | 以太网二层子接口是在物理接口上配置出来的具有二层特性的逻辑接口，可以在一个物理接口上配置多个子接口。仅S6780-H、 S6750-H、S6730-S-V2、S6750- S、S6750E-S、S6730-H-V2、 S6730E-H-V2、S5755-H、 S5755-S、S5732-H-V2系列支持。 | 在VXLAN网络中，业务接入点统一表现为二层子接口，通过在二层子接口上配置流封装实现不同的接口接入不同的数据报文。 |
| 以太网三层子接口 | 以太网三层子接口是在物理接口上配置出来的具有三层特性的逻辑接口，可以在一个物理接口上配置多个子接口。仅S6780-H、 S6750-H、S6730-S-V2、S6750- S、S6750E-S、S6730-H-V2、 S6730E-H-V2、S5755-H、 S5755-S、S5732-H-V2系列支持。 | 以太网三层子接口能实现不同VLAN 间且不同网段的用户的三层互通。 VLANIF接口可以实现不同VLAN间的互通，但是会对应一个或多个物理接口。在一个物理接口上配置多个子接口，这些子接口分别对应不同VLAN，这样只需连接一个物理接口就可实现不同VLAN之间的互通。 |
| Eth- Trunk二层子接口 | Eth-Trunk二层子接口是在Eth- Trunk接口上配置出来的具有二层特性的逻辑接口，可以在一个 Eth-Trunk接口上配置多个Eth- Trunk子接口。仅S6780-H、 S6750-H、S6730-S-V2、S6750- S、S6750E-S、S6730-H-V2、 S6730E-H-V2、S5755-H、 S5755-S、S5732-H-V2系列支持。 | 在VXLAN网络中，业务接入点统一表现为二层子接口，通过在二层子接口上配置流封装实现不同的接口接入不同的数据报文。 |

| 接口类型 | 接口描述 | 应用场景 |
|---|---|---|
| Eth- Trunk三层子接口 | Eth-Trunk三层子接口是在Eth- Trunk接口上配置出来的具有三层特性的逻辑接口，可以在一个 Eth-Trunk接口上配置多个Eth- Trunk子接口。仅S6780-H、 S6750-H、S6730-S-V2、S6750- S、S6750E-S、S6730-H-V2、 S6730E-H-V2、S5755-H、 S5755-S、S5732-H-V2系列支持。 | Eth-Trunk三层子接口能实现不同 VLAN间且不同网段的用户的三层互通。当三层设备通过三层Eth-Trunk 接口接入二层网络设备且二层网络设备的端口划分到不同的VLAN中时，为了实现三层Eth-Trunk接口可以正确识别不同的VLAN报文，从而保证不同VLAN间的用户可以正常通信，需要在三层设备与二层设备相连的Eth-Trunk接口上创建Eth- Trunk三层子接口与下游用户的 VLAN分别对应。 |
| NVE接口 | NVE接口是实现网络虚拟化功能的逻辑接口。仅S6780-H、 S6750-H、S6730-S-V2、S6750- S、S6750E-S、S6730-H-V2、 S6730E-H-V2、S5755-H、 S5755-S、S5732-H-V2系列支持。 | 在VXLAN网络中，NVE接口用于在 NVE之间建立VXLAN隧道，对 VXLAN报文进行封装和解封装，能实现VXLAN的二层互通。 |
| VBDIF接口 | VBDIF接口是基于BD创建的三层逻辑接口。仅S6780-H、S6750- H、S6730-S-V2、S6750-S、 S6750E-S、S6730-H-V2、 S6730E-H-V2、S5755-H、 S5755-S、S5732-H-V2系列支持。 | BD是VXLAN网络中转发数据报文的二层广播域。VBDIF接口能实现不同网段的VXLAN间，及VXLAN和非 VXLAN的通信，也可实现二层网络接入三层网络。 |

| 接口类型 | 接口描述 | 应用场景 |
|---|---|---|
| Loopbac k接口 | Loopback接口是一种逻辑接口，任何送到该接口的数据报文都会被认为是送往设备自身的。 Loopback接口具有如下特点： ● Loopback接口一旦被创建，其物理状态和链路协议状态永远是Up，直到被删除。即使该接口上没有配置IP地址。当用户需要一个接口状态通常是Up的接口的IP地址时，可以选择 Loopback接口的IP地址。 ● Loopback接口配置IP地址后，就可以对外发布。Loopback接口上可以配置32位掩码的IP地址，以达到节省地址空间的目的。 ● 对于目的地址不是本地IP地址，出接口是本地Loopback接口的报文，设备会将其直接丢弃。 ● Loopback接口上不能配置封装任何链路层协议。数据链路层也就不存在协商问题，其协议状态通常情况下都是Up。系统在启动时，会自动创建一个 InLoopback0接口，它是一个特殊而固定的Loopback接口。 InLoopback0接口使用环回地址 127.0.0.1/8接收所有发送给本机的数据包，该接口上的IP地址是不可以改变的，也不通过路由协议对外发布。 | Loopback接口可以应用在如下场景： ● 将Loopback接口的IP地址指定为报文的源地址，可以提高网络可靠性。 ● 根据Loopback接口的IP地址控制访问接口和过滤日志等信息，使信息变得简单。 |
| NULL0接口 | NULL0接口是系统自动创建的一个接口。NULL0接口一直处于UP 状态，但是不能转发数据报文，任何发送到该接口的网络数据报文都会被丢弃。不能在NULL0接口上配置IP地址，也不能在 NULL0接口上封装任何链路层协议。 | NULL0接口可以应用在如下场景： ● 防止路由环路：NULL0接口最典型的使用是用来防止路由环路。例如，在聚合一组路由时，总是创建一条到NULL0接口的路由。 ● 过滤流量：NULL0接口提供了过滤流量的一个可选的方法。可以通过将不想要的报文发送到 NULL0接口，避免使用访问控制列表。例如，在静态路由中指定到达某一网段的下一跳为NULL0 接口，则任何发送到该网段的数据报文都会被丢弃。 |

| 接口类型 | 接口描述 | 应用场景 |
|---|---|---|
| Tunnel接口 | Tunnel接口是具有三层特性的逻辑接口，隧道两端的设备利用 Tunnel接口发送报文、识别并处理来自隧道的报文。仅S6780- H、S6750-H、S6730-S-V2、 S6750-S、S6750E-S、S6730-H- V2、S6730E-H-V2、S5755-H、 S5755-S、S5732-H-V2系列支持。 | Tunnel接口下配置具体隧道模式后可以应用于对应模式的场景。 |
| Virtual- MEth接口 | Virtual-MEth接口是为虚IP登录设置的逻辑接口。 | 虚IP登录场景下，设备选主成功会自动创建Virtual-MEth接口，并设置虚IP地址实现通过虚IP登录进行管理。 |

#### 2.1.2 接口编号规则

管理接口编号规则管理接口的编号规则如下：
表 2-4 各管理接口编号

| 接口名称 | 管理接口编号 |
|---|---|
| Console接口 | console 0 |
| MEth接口 | MEth 0/0/0 |

业务接口编号规则业务接口的编号规则如下：
设备采用“槽位号/子卡号/接口序号”的编号规则来定义业务接口。
● 槽位号：表示设备所在的槽位号。
● 子卡号：表示设备支持的子卡号。无子卡款型默认取值为0。
● 接口序号：表示设备上各接口的编排顺序号。

### 2.2 接口基础配置注意事项

License 依赖接口基础无需License许可即可使用。

硬件依赖表 2-5 支持本特性的硬件

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
| S6750-S | S6750-S16X10Y2CZ，S6750-S16X8YZ，S6750- S24T16X8Y2CZ |

| 系列 | 支持产品 |
|---|---|
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
特性限制表 2-6 本特性的使用限制

| 特性 | 特性限制 |
|---|---|
| 接口基础功能 | 三层接口上收到的报文DMAC等于设备系统MAC，会进行三层转发； |

| 特性 | 特性限制 |
|---|---|
| 接口基础功能 | 对于S6750-H系列，S6730E-H-V2系列，S6750E-S系列，S6730-S-V2 系列，S5755-H系列，S6780-H系列，S5732-H-V2系列，S6730-H-V2 系列，S5755-S系列，S6750-S系列：二层主接口的三层子接口无法配置IP地址。 |
| 接口基础功能 | VLANIF接口数量对于产品S1730S-S3系列，S5735-L-V2系列，S5735-S-V2系列， S5735E-L-V2系列，S5735E-S-V2系列，S5735I-H-V2系列，S5735I-L- V2系列，S5735I-S-V2系列，S5735S-L3系列，S5735S-S3系列， S5755-S系列，S6730-S-V2系列： 1024个对于产品S5732-H-V2系列，S5755-H系列，S6730-H-V2系列， S6730E-H-V2系列，S6750-H系列，S6750-S系列，S6750E-S系列， S6780-H系列： 4094个对于产品S5735R-L-V2系列： 256个对于产品S5735R-S-V2系列： 512个 |
| 接口基础功能 | 对于S5735R-L-V2系列，S1730S-S3系列，S5735-L-V2系列，S5735S- L3系列，S5735-S-V2系列，S5735E-S-V2系列，S5735I-S-V2系列， S5735R-S-V2系列，S5735I-L-V2系列，S5735E-L-V2系列，S5735S-S3 系列，S5735I-H-V2系列：对于IP地址冲突检测去使能和冲突抢占功能： 1、配置非抢占模式，对于同一IP地址，设备重启后不保证和重启前选择的接口一致。 2、VRRP虚地址不支持配置冲突抢占功能。 3、当业务指定的源接口IP地址被抢占时，接口协议状态为DOWN，会导致业务中断。 4、IP地址抢占生效后，由于接口切换会导致流量短暂中断。 |
| 接口基础功能 | 接口固定索引的功能依赖device.sys文件，当device.sys文件中的数据被删除时，无法保证设备重启后接口的索引不变。 |
| 接口基础功能 | 对于S6750-H系列，S6730E-H-V2系列，S6750E-S系列，S6730-S-V2 系列，S5755-H系列，S6780-H系列，S5732-H-V2系列，S6730-H-V2 系列，S5755-S系列，S6750-S系列：对于三层子接口、VLANIF接口、Tunnel接口的统计信息，通过MIB和命令行的统计结果未做隔离，因此通过reset interface counters和reset interface counters if-mib命令清除统计会导致命令行和MIB的统计全清零。 |
| 接口基础功能 | display interface相关查询接口信息的命令不显示离线的接口。 |

| 特性 | 特性限制 |
|---|---|
| 接口基础功能 | 对于S6750-H系列，S6730E-H-V2系列，S6750E-S系列，S6730-S-V2 系列，S5755-H系列，S6780-H系列，S5732-H-V2系列，S6730-H-V2 系列，S5755-S系列，S6750-S系列： openconfig-vlan.yang存在when条件约束：when "current()/oc- if:config/oc-if:type = 'ianaift:l3ipvlan'"，此YANG支持的VLANIF和 VBDIF接口，VLANIF接口的接口类型为ianaift:propVirtual，VBDIF的接口类型为ianaift:other，可以通过openconfig-vlan.yang查询出来，不满足when条件约束。 |
| 流量统计 | 主备倒换期间查询接口流量和速率会出现突变。 MPU主备倒换流量变小，速率变大。 |
| IP地址借用 | 对于三层接口借用Loopback接口的IPv4地址功能： 1、只支持借用后的IGP协议和IGP协议基础上的BGP协议，用于远端的路由学习。 2、不支持三层接口借用Loopback口IPv4地址之后的ARP学习、直连路由、直连路由基础上的BGP协议，以及底层流量转发。因为此时同一IP 地址对应多个出接口，下一跳出口不确定 |

### 2.3 配置接口的描述信息

背景信息为了方便管理和维护设备，可以配置接口的描述信息，描述接口所属的设备、接口类型和对端网元设备等信息。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface { interface-name | interface-type interface-number }步骤3 配置接口的描述信息。
description description描述信息把输入的第一个非空格字符作为第一个字符开始显示。
----结束检查配置结果执行命令 display interface description [ interface-name | interface-type [ interface-number ] ]，查看接口的描述信息。

### 2.4 配置接口的MTU值

背景信息网络层一般要限制每次发送数据包的最大长度。任何时候网络层接收到一份要发送的IP数据包时，它要判断向本地哪个接口发送数据，并查询该接口获得其最大传输单元MTU（Maximum Transmission Unit）。网络层把MTU值与要发送的IP数据包长度进行比较，如果IP数据包的长度比MTU值大，那么IP数据包就需要进行分片，分片后的数据包长度小于等于MTU。
MTU的大小决定了发送端一次能够发送报文的最大字节数。正确配置MTU值，是保证设备之间正常、高效通信的前提。
● 如果MTU配置过小而报文尺寸较大，可能会造成报文分片过多，报文可能被QoS队列丢弃，影响数据正常传输。
● 如果MTU配置过大，则可能会超过了接收端所能够承受的最大值，或者是超过了发送路径上途经的某台设备所能够承受的最大值，也会造成报文分片甚至丢弃，加重网络传输的负担，影响数据正常传输。
在链路层，MTU用于限制帧的长度。实际上，不同的供应商，甚至同一供应商的不同产品型号对MTU的定义也不尽相同。
以以太网为例，图1是一个完整的以太帧：
图 2-1 一个完整的以太帧（单位为字节）
在一些设备上：
● 在以太网接口配置MTU用以指示以太帧IP报文的最大长度，MTU是一个三层的定义，即IP MTU。
● MTU的值等于数据载荷与目的MAC地址、源MAC地址与报文长度的总和，即MTU = IP MTU + 14Bytes。
● MTU 的值等于数据载荷与目的 MAC 地址、源 MAC 地址、 CRC 与报文长度的总和，即MTU = IP MTU + 18Bytes。
在本设备上，MTU是三层的定义。如图2-2所示，MTU表示IP报文头与IP载荷的最大长度。如果一个以太接口的MTU设置为1500Bytes，那么IP报文头与IP载荷小于1500Bytes的报文将不会被分片发出。
图 2-2 设备 MTU 定义

操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface { interface-name | interface-type interface-number }步骤3 配置接口从二层模式切换到三层模式。
undo portswitch仅S6780-H系列、S6750-H、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755-S、S5755E-H、S5755-H、S6750-S系列、S5732-H-V2系列支持通过undo portswitch命令将接口从二层模式切换到三层模式。请根据当前接口模式自行选择是否要执行此步骤。
步骤4 配置接口的MTU值。
mtu mtu缺省情况下， MTU 是 1500 字节。不同硬件不同接口的缺省值可能有所不同，可通过display default-parameter interface命令查看。当需要保证网络中的大报文不丢失时，需要配置该步骤来设置报文分片的大小，对大报文进行强制分片。
说明如果接口下配置了IS-IS业务，IS-IS邻居建立成功后，如果修改MTU值，可能会导致IS-IS业务中断，请谨慎操作。
----结束检查配置结果执行命令display interface { interface-name | interface-type interface-number }，查看接口当前运行状态信息及MTU值。

### 2.5 配置流量统计时间间隔

背景信息通过配置接口的流量统计时间间隔功能，用户可以对感兴趣的报文进行统计与分析。
同时，通过预先查看接口的流量统计，及时采取流量控制的措施，可以避免网络拥塞和业务中断。
● 当用户发现网络有拥塞的情况时，可以将接口的流量统计时间间隔设置为小于300秒（拥塞加剧时，设置为30秒），观察接口在短时间内的流量分布情况。对于导致拥塞的数据报文，采取流量控制措施。
● 当网络带宽充裕，业务运行正常时，可以将接口的流量统计时间间隔设置为大于300 秒。一旦发现有流量参数异常的情况，及时修改流量统计时间间隔，便于更实时的观察该流量参数的趋势。

说明
● 在系统视图下配置的流量统计时间间隔对接口下的时间间隔为缺省值的所有接口都生效。
● 在接口视图下配置的流量统计时间间隔只对本接口生效，不影响其他接口。
● 在接口视图下配置的时间间隔的优先级高于在系统视图下配置的时间间隔。
操作步骤
● 配置全局流量统计时间间隔
a. 进入系统视图。
system-view
b. 配置全局流量统计时间间隔。
set flow-stat interval interval缺省情况下，全局流量统计时间间隔为300秒。
● 配置接口流量统计时间间隔
a. 进入系统视图。
system-view
b. 进入接口视图。
interface { interface-name | interface-type interface-number }
c. 配置接口流量统计时间间隔。
set flow-stat interval interval缺省情况下，接口流量统计时间间隔为300秒。
----结束

### 2.6 配置开启或关闭接口

背景信息当修改了接口的工作参数配置，且新的配置未能立即生效时，可以依次执行shutdown和undo shutdown命令或restart命令关闭和重启接口，使新的配置生效。
建议当接口闲置（即没有连接电缆或光纤）时，请使用shutdown命令关闭该接口，以防止由于干扰导致接口异常。
说明
● 依次执行shutdown和undo shutdown相当于执行restart命令，不会修改或删除接口的配置信息。
● NULL接口一直处于Up状态，不能使用命令关闭或启动NULL接口。
● Loopback接口一旦被创建，将一直保持Up状态，不能使用命令关闭或启动Loopback接口。
操作步骤
● 关闭接口
a. 进入系统视图。
system-view
b. 进入指定的接口视图。
interface { interface-name | interface-type interface-number }

c. 关闭接口。
shutdown
缺省情况下，接口处于打开状态。
说明
如果当需要关闭某个主接口下的大量子接口时，可以在子接口视图下使用shutdown
命令逐一关闭每个子接口，但是工作量会非常大，此时可以在系统视图下使用
shutdown interface命令对子接口进行批量关闭。
● 启动接口
a. 进入系统视图。
system-view
b. 进入指定的接口视图。
interface { interface-name | interface-type interface-number }
c. 启动接口。
undo shutdown
缺省情况下，接口处于打开状态。
d. （可选）配置接口切换到三层模式。
undo portswitch
仅S6780-H系列、S6750-H、S6750E-S、S6730-H-V2、S6730E-H-V2、
S5755-S、S5755E-H、S5755-H、S6750-S系列、S5732-H-V2系列支持通过
undo portswitch命令将接口从二层模式切换到三层模式。请根据当前接口
模式自行选择是否要执行此步骤。
e. （可选）关闭接口的协议状态。
shutdown network-layer
在排除光模块或者光纤故障的场景中，用户仅希望接口的协议状态Down，物
理层和链路层状态不发生变更，可以执行shutdown network-layer命令关
闭接口的协议状态，待物理层和链路层故障彻底修复后，再执行undo
shutdown network-layer命令恢复接口的协议状态。
说明
shutdown network-layer和protocol up-delay-time命令不可同时配置。
----结束

### 2.7 维护接口

背景信息须知清除接口的统计信息后，所有的统计数据都不能被恢复，请务必仔细确认。
操作步骤维护接口的相关操作，可执行如表2-7所示命令。

表 2-7 维护接口的相关操作

| 操作 | 视图 | 命令 | 说明 |
|---|---|---|---|
| 查看接口的诊断信息 | 用户视图 | display interface troubleshooting [ interface-name | interface-type interface-number ] | 接口故障时，用户可以一键式查看所有故障接口或者指定接口的诊断信息，包括接口 Down、闪断、错包的原因及告警等信息，从而快速定位故障原因。 |
| 查看所有业务接口的错误报文统计信息 | 所有视图 | display interface counters errors [ slot slotid ] | 无 |
| 查看接口默认配置 | 所有视图 | display default- parameter interface [ interface-name | interface-type interface-number ] | 当接口已经存在，或更改了接口的默认配置后，用户可以查看接口的默认配置信息，包括接口状态、MTU值、向对端发送请求报文的时间间隔、流量统计时间间隔、告警阈值、接口描述信息，以及接口状态变化是否向网管端发告警的功能。 |
| 查看设备上指定类型接口的简要信息 | 所有视图 | display interface interface-type brief main non-unicast | 在监控接口的状态或检查接口的故障原因时，用户可查看当前指定类型所有接口的简要信息，包括接口的物理状态、协议状态、接收方向最近一段时间的带宽利用率、发送方向最近一段时间的带宽利用率、接收的错误报文数和发送的错误报文数。 |
| 按照面板顺序查看当前所有接口的简要信息 | 所有视图 | display interface brief panel-order | 当用户想进行接口的故障诊断或流量统计时，可以根据自己的需要按照面板顺序查看当前所有接口的简要信息，包括接口的物理状态、协议状态、接收方向最近一段时间的带宽利用率、发送方向最近一段时间的带宽利用率、接收的错误报文数和发送的错误报文数。 |

| 操作 | 视图 | 命令 | 说明 |
|---|---|---|---|
| 查看与IP相关的接口的简要信息和描述信息 | 所有视图 | display ip interface description | 无 |
| 查看接口的IPv6信息 | 所有视图 | display ipv6 interface brief | 无 |
| 查看接口在管理信息库 MIB（Management Information Base）中的索引值 | 所有视图 | display mib-index interface [ interface- type [ interface- number ] | interface- name ] | 为了方便网管查看接口名字所对应的接口索引，用户可以执行本命令查看接口索引的具体数值。 |
| 监控指定接口的详细信息，包括运行状态和统计信息 | 所有视图 | monitor interface counters [ rate ] { interface-name | interface-type interface-number } | 监控接口统计信息，方便用户通过流量和速率分析网络状况。 |
| 监控接口当前的流量统计信息 | 所有视图 | monitor interface- statistics interface { interface-name | interface-type interface-number } &<1-5> |  |
| 批量监控接口当前的流量统计信息 | 所有视图 | monitor interface- statistics batch [ interface interface- type [ interface- number-begin [ to interface-number- end ] ] ] |  |
| 监控接口的报文个数或报文速率 | 所有视图 | monitor interface- information interface { interface-name | interface-type interface-number } |  |
| 清除接口的统计信息 | 所有视图 | reset interface counters [ interface- name | interface-type [ interface-number ] ] | 接口统计信息有助于分析接口的故障原因和接口的工作状态。当您需要统计一定时间内接口的流量信息时，需要在统计开始前清除该接口下原有的统计信息。 |

| 操作 | 视图 | 命令 | 说明 |
|---|---|---|---|
| 清除接口的峰值速率和峰值速率时间的显示值 | 系统视图 | reset counters peak- rate interface { all | interface-name | interface-type [ interface-number ] } | 设备会保存接口的历史速率峰值，如果后续时间的峰值速率都小于已经保存的峰值速率，则保存的峰值速率值将不会再更新，如果需要获取后续时间内的峰值速率，则需要清除之前已经保存的峰值速率。 |
