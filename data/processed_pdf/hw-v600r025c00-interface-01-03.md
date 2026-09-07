# S1700, S5700, S6700 V600R025C00 配置指南-接口管理 01-03 逻辑接口配置

## 3 逻辑接口配置

3逻辑接口配置

### 3.1 逻辑接口简介

3.2 逻辑接口配置注意事项
3.3 逻辑接口缺省配置
3.4 配置VLANIF接口
3.5 配置Eth-Trunk接口
3.6 配置子接口
3.7 配置NVE接口
3.8 配置VBDIF接口
3.9 配置Loopback接口
3.10 配置Tunnel接口
3.11 维护逻辑接口
3.1 逻辑接口简介
逻辑接口是指能够实现数据交换功能但物理上不存在、需要通过配置建立的虚拟接
口。本节主要介绍设备支持的几种类型的逻辑接口，详细情况见表3-1。

表 3-1 逻辑接口分类

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

### 3.2 逻辑接口配置注意事项

License 依赖逻辑接口无需License许可即可使用。
硬件依赖表 3-2 支持本特性的硬件

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
特性限制无

### 3.3 逻辑接口缺省配置

逻辑接口的缺省配置如表3-3所示。
表 3-3 逻辑接口缺省配置

| 接口类型 | 缺省配置 |
|---|---|
| VLANIF接口 | 系统缺省没有此接口。 |
| Eth-Trunk接口 | 系统缺省没有此接口。 |
| 以太网二层子接口 | 系统缺省没有此接口。仅S6780-H、S6750-H、S6730-S-V2、 S6750-S、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755- H、S5755-S、S5732-H-V2系列支持。 |
| 以太网三层子接口 | 系统缺省没有此接口。仅S6780-H、S6750-H、S6730-S-V2、 S6750-S、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755- H、S5755-S、S5732-H-V2系列支持。 |
| Eth-Trunk二层子接口 | 系统缺省没有此接口。仅S6780-H、S6750-H、S6730-S-V2、 S6750-S、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755- H、S5755-S、S5732-H-V2系列支持。 |
| Eth-Trunk三层子接口 | 系统缺省没有此接口。仅S6780-H、S6750-H、S6730-S-V2、 S6750-S、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755- H、S5755-S、S5732-H-V2系列支持。 |

### 3.5 配置Eth-Trunk接口

| 接口类型 | 缺省配置 |
|---|---|
| NVE接口 | 系统缺省没有此接口。仅S6780-H、S6750-H、S6730-S-V2、 S6750-S、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755- H、S5755-S、S5732-H-V2系列支持。 |
| VBDIF接口 | 系统缺省没有此接口。仅S6780-H、S6750-H、S6730-S-V2、 S6750-S、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755- H、S5755-S、S5732-H-V2系列支持。 |
| Loopback接口 | 系统在启动时会自动创建一个InLoopback0接口。 |
| NULL0接口 | 系统在启动时会自动创建一个NULL0接口。 |
| Tunnel接口 | 系统缺省没有此接口。仅S6780-H、S6750-H、S6730-S-V2、 S6750-S、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755- H、S5755-S、S5732-H-V2系列支持。 |

### 3.4 配置VLANIF接口

背景信息VLANIF接口的配置请参见VLAN配置。
配置 接口
3.5 Eth-Trunk操作步骤步骤1 进入系统视图。
system-view步骤2 创建Eth-Trunk接口并进入Eth-Trunk接口视图。
interface eth-trunk trunk-id
----结束

### 3.6 配置子接口

背景信息说明该配置仅S6780-H、S6750-H、S6730-S-V2、S6750-S、S6750E-S、S6730-H-V2、S6730E-H- V2、S5755-H、S5755-S、S5732-H-V2系列支持。

#### 3.6.1 配置以太网二层子接口

背景信息当设备接入二层网络时，可以配置以太网二层子接口。

操作步骤步骤1 进入系统视图。
system-view步骤2 进入需要创建二层子接口的主接口视图。
interface interface-type interface-number步骤3 配置接口的链路类型为trunk，hybrid或access。
port link-type { trunk | hybrid | access }步骤4 退回系统视图。
quit步骤5 创建并进入以太网二层子接口视图。
interface interface-type interface-number.subnumber mode l2
----结束

#### 3.6.2 配置以太网三层子接口

背景信息当设备接入三层网络时，可以配置以太网三层子接口，可实现不同VLAN间且不同网段的用户的三层互通。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入主接口，切换以太网接口到三层模式。
interface interface-type interface-number undo portswitch步骤3 创建并进入以太网三层子接口视图。
interface interface-type interface-number.subnumber
----结束

#### 3.6.3 配置Eth-Trunk二层子接口

背景信息当设备通过二层Eth-Trunk接口接入二层网络，可以配置Eth-Trunk二层子接口，以实现在Eth-Trunk二层子接口之间来往报文的二层转发。
说明该配置仅S6780-H、S6750-H、S6730-S-V2、S6750-S、S6750E-S、S6730-H-V2、S6730E-H- V2、S5755-H、S5755-S、S5732-H-V2系列支持。
操作步骤步骤1 进入系统视图。
system-view

#### 3.6.4 配置Eth-Trunk三层子接口

步骤2 进入Eth-Trunk接口视图。
interface eth-trunk trunk-id步骤3 配置Eth-Trunk接口为二层模式，并返回至系统视图。
portswitch quit步骤4 进入需要创建二层子接口的主接口视图。
interface interface-type interface-number步骤5 配置接口的链路类型为trunk，hybrid或access。
port link-type { trunk | hybrid | access }步骤6 退回系统视图。
quit步骤7 创建Eth-Trunk接口的二层子接口，并进入Eth-Trunk二层子接口视图。
interface eth-trunk trunk-id.subnumber mode l2 subnumber是Eth-Trunk二层子接口的编号。
----结束配置 三层子接口
3.6.4 Eth-Trunk背景信息Eth-Trunk三层子接口的配置请参见Eth-Trunk配置。

### 3.7 配置NVE接口

背景信息在VXLAN网络中，NVE接口用于在NVE之间建立VXLAN隧道，对VXLAN报文进行封装和解封装，能实现VXLAN的二层互通。
说明该配置仅S6780-H、S6750-H、S6730-S-V2、S6750-S、S6750E-S、S6730-H-V2、S6730E-H- V2、S5755-H、S5755-S、S5732-H-V2系列支持。
操作步骤步骤1 进入系统视图。
system-view步骤2 创建并进入NVE接口。
interface nve interface-number
----结束

### 3.8 配置VBDIF接口

背景信息BD是VXLAN网络中转发数据报文的二层广播域。VBDIF接口能实现不同网段的VXLAN间，及VXLAN和非VXLAN的通信，也可实现二层网络接入三层网络。
说明该配置仅S6780-H、S6750-H、S6730-S-V2、S6750-S、S6750E-S、S6730-H-V2、S6730E-H- V2、S5755-H、S5755-S、S5732-H-V2系列支持。
操作步骤步骤1 进入系统视图。
system-view步骤 2 创建并进入 VBDIF 接口。
interface vbdif bd-id
----结束

### 3.9 配置Loopback接口

操作步骤步骤1 进入系统视图。
system-view步骤2 创建并进入Loopback接口。
interface loopback loopback-number
----结束检查配置结果执行命令display interface loopback [ loopback-number ]，查看Loopback接口的状态信息。

### 3.10 配置Tunnel接口

背景信息说明该配置仅S6780-H、S6750-H、S6730-S-V2、S6750-S、S6750E-S、S6730-H-V2、S6730E-H- V2、S5755-H、S5755-S、S5732-H-V2系列支持。
Tunnel接口可以应用在VPN类业务中。以GRE为例，Tunnel接口叠加业务的配置请参见GRE配置。

操作步骤步骤1 进入系统视图。
system-view步骤2 创建并进入Tunnel口。
interface tunnel interface-number
----结束

### 3.11 维护逻辑接口

背景信息可以配置接口的告警、统计等功能，用于维护逻辑接口。
说明该配置仅 S6780-H 、 S6750-H 、 S6730-S-V2 、 S6750-S 、 S6750E-S 、 S6730-H-V2 、 S6730E-H- V2、S5755-H、S5755-S、S5732-H-V2系列支持。
关闭子接口产生 linkdown 告警在系统视图下执行subinterface disable命令可以关闭子接口产生trap updown linkdown告警的功能。
说明执行此命令后设备上所有子接口状态发生变化均不会产生linkdown告警，请谨慎操作。
配置三层子接口流量统计功能当需要检查网络状况或处理网络故障时，可以打开三层子接口的流量统计功能，统计通过三层子接口的流量信息。
说明缺省情况下，三层子接口的流量统计功能处于关闭状态。
流量统计功能开启后，任意视图下执行命令display interface [ interface-type [ interface- number ] ]，或接口视图下执行命令display this interface，查看接口流量统计信息。
1. 进入系统视图。
system-view
2. 进入指定的三层子接口视图。
interface interface-type interface-number.subinterface-number
3. （可选）使能子接口的IPv6功能。
ipv6 enable说明需要使能三层子接口IPv6报文统计时必须先使能子接口的IPv6功能。
4. 使能三层子接口的流量统计功能。
statistics { ipv4 | ipv6 } enable [ inbound | outbound ]

配置二层子接口流量统计功能当需要检查网络状况或处理网络故障时，可以打开二层子接口的流量统计功能，统计通过二层子接口的流量信息。
说明缺省情况下，二层子接口的流量统计功能处于关闭状态。
流量统计功能开启后，任意视图下执行命令display interface [ interface-type [ interface- number ] ]，或接口视图下执行命令display this interface，查看接口流量统计信息。
1. 进入系统视图。
system-view
2. 进入指定的二层主接口视图。
interface interface-type interface-number
3. 配置接口的链路类型为trunk，hybrid或access。
port link-type { trunk | hybrid | access }
4. 退出主接口视图。
quit
5. 进入指定的二层子接口视图。
interface interface-type interface-number.subinterface-number mode l2
6. 使能二层子接口的流量统计功能。
statistics enable
