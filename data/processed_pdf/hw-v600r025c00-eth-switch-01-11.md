# S1700, S5700, S6700 V600R025C00 配置指南-以太网交换 01-11 二层协议透明传输配置

## 11 二层协议透明传输配置

### 11.1 二层协议透明传输简介

11.2 二层协议透明传输原理描述
11.3 二层协议透明传输配置注意事项
11.4 二层协议透明传输缺省配置
11.5 配置基于接口的二层协议透明传输
11.6 配置基于VLAN的二层协议透明传输
11.7 配置基于QinQ的二层协议透明传输
11.8 配置基于VPLS的二层协议透明传输
11.9 配置BPDU协议报文透明传输
11.10 维护二层协议透明传输
11.11 二层协议透明传输配置举例
11.1 二层协议透明传输简介
定义
二层协议报文透明传输（ Layer 2 Protocol Tunneling ）是利用二层隧道技术使不同地
域私网用户的二层协议报文，通过运营商网络内的指定通道进行透明传输。
目的
在实际组网中，用户经常利用运营商提供的专线来构建自己的二层网络，这使同一用
户私网的不同分支可能分布在运营商公网的两侧。如图11-1所示，用户A的网络分为网
络1和网络2，二者通过运营商网络相连接。当网络1和网络2中共同运行某种二层协议
（如MSTP协议）时，要求网络1和网络2中的二层协议报文能够穿越运营商网络，以完
成二层协议的计算（如生成树的计算）。通常二层协议报文的目的MAC都是一样的，
例如 MSTP 协议，其协议报文是 BPDU 报文，目的 MAC 均是 0180-C200-0000 。因此，
当用户网络的二层协议报文到达运营商网络的PE设备时，PE不能识别该二层协议报文
是来自用户网络还是来运营商网络，都会把收到的二层协议报文发送给CPU进行处
理，完成生成树计算。

这样用户网络1的设备就和PE1完成了生成树计算功能，而不是和用户网络2的设备完成生成树计算。用户网络1的二层协议报文无法穿越运营商网络到达用户网络2中。
图 11-1 二层协议在 ISP 网络透明传输为了解决上述问题，就要求在运营商网络中能够透传用户网络的二层协议报文。利用二层协议透传功能，即可实现上述要求，过程如下：
1. PE1 收到 CE1 发来的二层协议报文后，将二层协议报文的目的 MAC 地址替换成一个特定的组播MAC地址，然后在运营商网络中进行转发。
2. 替换成特定的组播MAC地址的二层协议报文被转发至运营商网络另一端的PE2，被还原为原始的目的MAC地址，并发送给CE2。

### 11.2 二层协议透明传输原理描述

二层协议透明传输的基本原理是：
● 在骨干网的用户接入侧替换原始二层协议报文的组播目的MAC地址为特定的组播MAC地址。
● 修改MAC地址后的报文在骨干网中根据配置的透明传输方式决定是否对报文进行处理。
● 当该二层协议报文到达出节点时，通过匹配设备上配置的特殊组播目的MAC和二层协议的映射关系，将报文的组播目的MAC还原成该二层协议标准的组播目的MAC地址，并根据配置的透明传输方式决定是否处理该报文。
二层协议报文需要在骨干网络中透明传输，其传输过程中必须达到以下要求：
● 同一个用户网络的所有分支都能收到其他分支的二层协议报文。
● 用户网络的二层协议报文不能被骨干网设备的CPU处理。
● 不同客户网络中的二层协议报文必须隔离，不能互相影响。
按照应用场景的不同，设备支持如表11-1所示的二层协议透明传输。

表 11-1 二层协议透明传输不同应用场景概览

| 场景 | 描述 | 对应任务 |
|---|---|---|
| 配置基于接口的二层协议透明传输 | 当骨干网设备上每个接口只有一个用户网络接入，且用户网络发送的二层协议报文不需要携带VLAN Tag时，为了实现该二层协议报文在骨干网络中的透明传输，可以配置基于接口的二层协议透明传输功能。 | 11.5 配置基于接口的二层协议透明传输 |
| 配置基于VLAN的二层协议透明传输 | 当骨干网设备上每个接口有多个用户网络接入，且用户网络发送的二层协议报文需要携带VLAN Tag 时，为了实现该二层协议报文在骨干网络中的透明传输，可以配置基于VLAN 的二层协议透明传输功能。 | 11.6 配置基于VLAN的二层协议透明传输 |
| 配置基于QinQ的二层协议透明传输 | 当骨干网设备上每个接口有多个用户网络接入，且用户网络发送的报文需要携带VLAN Tag时，为了实现不同用户网络的协议报文在骨干网络中的透明传输，同时为了节省运营商的VLAN ID，可以配置基于QinQ的二层协议透明传输功能。 | 11.7 配置基于QinQ的二层协议透明传输 |

### 11.3 二层协议透明传输配置注意事项

License 依赖二层协议透明传输无需License许可即可使用。
硬件依赖表 11-2 支持本特性的硬件

| 系列 | 支持产品 |
|---|---|
| S6750-H | S6750-H36C，S6750-H48X8C，S6750-H48Y8C |

| 系列 | 支持产品 |
|---|---|
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
| S5735S-L3 | S5735S-L24P4S-A3，S5735S-L24P4XE-A3， S5735S-L24PN4XE-A3，S5735S-L24ST4X-A3， S5735S-L24T4S-QA3，S5735S-L24T4X-QA3， S5735S-L24T8J4XE-A3，S5735S-L48P4S-A3， S5735S-L48P4XE-A3，S5735S-L48PN4XE-A3， S5735S-L48S4X-A3，S5735S-L48T4S-A3，S5735S- L48T4XE-A3，S5735S-L8P4X-QA3，S5735S- L8T4X-QA3 |

| 系列 | 支持产品 |
|---|---|
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

特性限制表 11-3 本特性的使用限制

| 特性 | 特性限制 |
|---|---|
| L2PT基础功能 | 1.不能将STP、GVRP和GMRP这几种协议报文的目的MAC地址替换成相同的组播MAC地址 2.不能将EFM(802.3ah)、LACP和DLDP这几种协议报文的目的MAC地址替换成相同的组播MAC地址 3.配置二层协议透明传输功能时，下面的组播MAC地址不能作为二层协议报文被替换后的组播MAC地址： BPDU报文的目的MAC地址：0180-C200-0000～0180-C200-002F。 Smart Link协议报文：010F-E200-0004。特殊的组播MAC地址：0100-0CCC-CCCC和0100-0CCC-CCCD。本设备上已经使用过的普通组播MAC地址。 |
| L2PT基础功能 | 透传基于物理口生效的BPDU协议报文时L2PT隧道出口不能为trunk。 |
| L2PT基础功能 | L2PT下发ACL规则基于mac+协议号方式，LACP和3AH的协议mac和协议号都一样(只是子协议号不同)，使能LACP时，打3AH协议报文会误上送；同理，使能3AH时，打LACP协议报文也会误上送； |
| L2PT基础功能 | L2PT支持叠加的场景 L2PT仅支持default vlan、trunk allow-pass vlan、hybrid vlan、vlan stacking且端口下无其他叠加业务的场景。 |
| L2PT基础功能 | 端口对BPDU报文动作为丢弃时不支持流策略重定向此类报文。 |
| L2PT基础功能 | 端口隔离叠加L2PT，端口隔离不生效。 |

### 11.4 二层协议透明传输缺省配置

表 11-4 二层协议透明传输参数缺省值

| 参数 | 缺省值 |
|---|---|
| 设备通过硬件转发BPDU协议报文时是否允许二层接口转发BPDU协议报文 | 不允许 |
| 带TAG的BPDU报文透传功能 | 不使能 |
| 设备上是否存在用户自定义的二层透明传输协议的特征信息 | 不存在 |
| 接口发出的BPDU（Bridge Protocol Data Unit）报文携带指定的VLAN ID值 | 不携带VLAN ID值 |

### 11.5 配置基于接口的二层协议透明传输

#### 11.5.1 了解基于接口的二层协议透明传输

如图11-2所示，PE设备的每个接口只连接了一个用户网络，且所有的用户网络不属于同一个LAN。若此时用户网络发送到PE的二层协议报文（BPDU）不带VLAN标签，PE设备需要区分该二层协议报文来自哪一个用户LAN。LAN-A的二层协议报文必须被转发到其他LAN-A的用户网络中，而不能被转发到其他的用户网络中，并且还要避免该二层协议报文被运营商网络设备处理。
图 11-2 基于接口的二层协议透明传输针对这种场景，处理方式是替换来自用户网络的原始二层协议报文的组播MAC地址为指定组播MAC地址。
1. 在骨干网设备上，连接相同的用户网络的接口加入到同一个VLAN中。骨干网设备收到用户网络的二层协议报文，因为不同的协议报文有不同的目的MAC地址，因此设备可识别出该报文属于哪种二层协议的报文（如STP协议的BPDU报文），根据接口的缺省VLAN，给该报文打上对应的VLAN ID。
2. 骨干网设备根据配置的特殊组播目的MAC和二层协议的映射关系，将该二层协议报文的标准组播目的MAC地址修改为指定的组播目的MAC地址。
3. 修改MAC后的二层报文在骨干网内部的节点上按照普通的二层报文转发，用户网络的二层协议报文正常地穿越骨干网络。
4. 用户网络的二层协议报文到达骨干网设备的出节点设备时，再次根据设备上配置的特殊组播目的 MAC 和二层协议的映射关系，将该报文的组播目的 MAC 地址还原成二层协议的标准组播MAC地址，然后再转发到用户侧。

#### 11.5.2 （可选）自定义二层透明传输协议的特征信息

背景信息当用户网络中特定组播目的MAC地址的协议报文（非标准二层协议报文）需要在骨干网络中进行透明传输时，可以在PE上定义二层透明传输协议的特征信息。这些特征信息包括协议的名称、以太封装类型、报文的目的MAC地址、报文被替换后的组播MAC地址等。
配置用户自定义的二层透明传输协议的特征信息时，下面的组播MAC地址不能作为二层协议报文被替换后的组播MAC地址：

● BPDU报文的目的MAC地址：0180-C200-0000～0180-C200-002F。
● Smart Link协议报文：010F-E200-0004。
● 特殊的组播MAC地址：0100-0CCC-CCCC和0100-0CCC-CCCD。
● 本设备上已经使用过的普通组播MAC地址。
操作步骤
步骤1 进入系统视图。
system-view
步骤2 自定义二层透明传输协议的特征信息。
l2protocol-tunnel user-defined-protocol protocol-name protocol-mac protocol-mac [ encap-type
{ { ethernetii protocol-type protocol-type } | { llc dsap dsap-value ssap ssap-value } | { snap protocol-
type protocol-type } } ] group-mac { group-mac | default-group-mac }
----结束

#### 11.5.3 配置二层协议透明传输的方式

背景信息配置二层透明传输包括两种方式：
● 修改骨干网设备可以识别的缺省二层协议组播MAC地址为其他的组播MAC地址，这种方式只适用于STP/RSTP/MSTP协议。
● 替换来自用户网络的原始二层协议报文的组播MAC地址为指定组播MAC地址，适用于所有类型的二层协议透明传输。
在设备上根据二层协议的类型和需要透明传输的方式，选择如下配置步骤之一。
操作步骤
● 修改骨干网设备可以识别的缺省二层协议组播MAC地址为其他的组播MAC地址进入系统视图。
a.
system-view
b. 配置PE设备的角色为provider。
bpdu-tunnel stp bridge role provider
● 替换来自用户网络的原始二层协议报文的组播MAC地址为指定组播MAC地址
a. 进入系统视图。
system-view将二层协议报文的组播目的MAC地址替换成为一个指定的组播MAC地址。
b.
l2protocol-tunnel protocol group-mac { group-mac | default-group-mac }

说明不能将SSTP、STP和GMRP协议报文的目的MAC地址替换成相同的组播MAC地址。
配置二层协议透明传输功能时，下面的组播MAC地址不能作为二层协议报文被替换后的组播MAC地址：
● BPDU报文的目的MAC地址：0180-C200-0000～0180-C200-002F。
● Smart Link协议报文：010F-E200-0004。
● 特殊的组播MAC地址：0100-0CCC-CCCC和0100-0CCC-CCCD。
● 本设备上已经使用过的普通组播MAC地址。
----结束

#### 11.5.4 使能接口的二层协议透明传输功能

背景信息请在PE设备上根据需要透明传输的协议类型，进行以下配置。
说明不能把l2protocol-tunnel enable命令和l2protocol-tunnel vlan命令在同一个接口下配置相同协议类型，否则会提示配置冲突。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入PE的用户侧接口视图。
interface interface-type interface-number步骤3 将接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 配置接口的链路类型为Hybrid。
port link-type hybrid步骤5 配置接口的缺省VLAN。
port hybrid pvid vlan vlan-id步骤6 配置接口以untagged方式允许缺省VLAN通过。
port hybrid untagged vlan vlan-id说明步骤 6 指定的 VLAN 和步骤 5 配置的 VLAN 需相同。
步骤7 使能接口的二层协议透明传输功能。
l2protocol-tunnel { all | user-defined-protocol protocol-name | { protocol } &<1-16> } enable

步骤8 （可选）使能二层协议透明传输功能的接口丢弃协议报文的阈值。
l2protocol-tunnel drop-threshold rate [ user-defined-protocol protocol-name | { protocol } &<1-16> ]缺省情况下，使能二层协议透明传输功能的接口丢弃协议报文的阈值是0，表示使能二层协议透明传输功能的接口不限制入接口的二层协议报文流量。
当使能二层协议透明传输功能的接口收到大量的协议报文时，为防止恶意攻击，可在接口下配置协议报文丢弃阈值。在单位(1秒)时间内，当二层协议报文入接口（使能二层协议透明传输功能的接口）方向通过的二层协议报文超过配置的阈值时，将丢弃协议报文。
----结束

#### 11.5.5 检查二层协议透明传输配置结果

操作步骤
● 执行命令display l2protocol-tunnel group-mac { all | protocol | user- defined-protocol protocol-name }，查看所有的二层协议或者指定的二层协议的透明传输信息。
----结束

### 11.6 配置基于VLAN的二层协议透明传输

#### 11.6.1 了解基于VLAN的二层协议透明传输

在多数情况下，PE都是作为汇聚设备存在，如图11-3所示，PE1的汇聚接口上同时收到来自LAN-A、LAN-B的报文。为了区分这两个不同的用户网络，CE发送到PE的二层协议报文就必须携带VLAN ID，其中，LAN-A的VLAN ID为200，LAN-B的VLAN ID为100。为保证LAN-A的二层协议报文被转发到其他LAN-A的用户网络中，而不被转发到LAN-B的用户网络中，并且还要避免该二层协议报文被运营商网络设备处理。可在PE设备上配置基于VLAN的二层协议透明传输，二层协议报文会通过二层隧道，穿越骨干网络。

图 11-3 基于 VLAN 的二层协议透明传输与基于接口的二层协议透明传输类似，针对这种场景，处理方式是替换来自用户网络的原始二层协议报文的组播MAC地址为指定组播MAC地址。
1. 配置用户网络设备发送到骨干网的二层协议报文带有指定的VLAN ID。
说明当用户网络发送到骨干网的二层协议报文为STP协议报文时，在设备上执行命令stp bpdu vlan使能接口发出的STP协议报文携带指定的VLAN ID值。
2. 配置骨干网设备能够识别带有VLAN ID的二层协议报文，并允许这些VLAN ID通过。
3. 骨干网设备根据配置的特殊组播目的MAC和二层协议的映射关系，将该二层协议报文的标准组播目的MAC地址修改为指定的组播目的MAC地址。
4. 修改MAC后的二层报文在骨干网内部的节点上按照普通的二层报文转发，用户网络的二层协议报文正常地穿越骨干网络。
5. 用户网络的二层协议报文到达骨干网设备的出节点设备时，再次根据设备上配置的特殊组播目的 MAC 和二层协议的映射关系，将该报文的组播目的 MAC 地址还原成二层协议的标准组播MAC地址，然后再转发到用户侧。

#### 11.6.2 （可选）自定义二层透明传输协议的特征信息

背景信息当用户网络中特定组播目的MAC地址的协议报文（非标准二层协议报文）需要在骨干网络中进行透明传输时，可以在PE上定义二层透明传输协议的特征信息。这些特征信息包括协议的名称、以太封装类型、报文的目的MAC地址、报文被替换后的组播MAC地址等。
配置用户自定义的二层透明传输协议的特征信息时，下面的组播MAC地址不能作为二层协议报文被替换后的组播MAC地址：

● BPDU报文的目的MAC地址：0180-C200-0000～0180-C200-002F。
● Smart Link协议报文：010F-E200-0004。
● 特殊的组播MAC地址：0100-0CCC-CCCC和0100-0CCC-CCCD。
● 本设备上已经使用过的普通组播MAC地址。
操作步骤
步骤1 进入系统视图。
system-view
步骤2 自定义二层透明传输协议的特征信息。
l2protocol-tunnel user-defined-protocol protocol-name protocol-mac protocol-mac [ encap-type
{ { ethernetii protocol-type protocol-type } | { llc dsap dsap-value ssap ssap-value } | { snap protocol-
type protocol-type } } ] group-mac { group-mac | default-group-mac }
----结束

#### 11.6.3 配置二层协议透明传输的方式

背景信息配置二层透明传输包括两种方式：
● 修改骨干网设备可以识别的缺省二层协议组播MAC地址为其他的组播MAC地址，这种方式只适用于STP/RSTP/MSTP协议。
● 替换来自用户网络的原始二层协议报文的组播MAC地址为指定组播MAC地址，适用于所有类型的二层协议透明传输。
在设备上根据二层协议的类型和需要透明传输的方式，选择如下配置步骤之一。
操作步骤
● 修改骨干网设备可以识别的缺省二层协议组播MAC地址为其他的组播MAC地址进入系统视图。
a.
system-view
b. 配置PE设备的角色为provider。
bpdu-tunnel stp bridge role provider
● 替换来自用户网络的原始二层协议报文的组播MAC地址为指定组播MAC地址
a. 进入系统视图。
system-view将二层协议报文的组播目的MAC地址替换成为一个指定的组播MAC地址。
b.
l2protocol-tunnel protocol group-mac { group-mac | default-group-mac }

说明不能将SSTP、STP和GMRP协议报文的目的MAC地址替换成相同的组播MAC地址。
配置二层协议透明传输功能时，下面的组播MAC地址不能作为二层协议报文被替换后的组播MAC地址：
● BPDU报文的目的MAC地址：0180-C200-0000～0180-C200-002F。
● Smart Link协议报文：010F-E200-0004。
● 特殊的组播MAC地址：0100-0CCC-CCCC和0100-0CCC-CCCD。
● 本设备上已经使用过的普通组播MAC地址。
----结束

#### 11.6.4 使能接口基于VLAN的二层协议透明传输功能

背景信息请在PE设备上根据需要透明传输的协议类型，进行以下配置。
说明不能把l2protocol-tunnel vlan命令和l2protocol-tunnel enable命令在同一个接口下配置相同协议类型，否则会提示配置冲突。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入PE的用户侧接口视图。
interface interface-type interface-number步骤3 将接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 配置接口的链路类型以下步骤，请根据需要任选一种。
● 配置接口的链路类型为Trunk
a. 配置接口的链路类型为Trunk。
port link-type trunk
b. 将接口加入到指定的VLAN中。
port trunk allow-pass vlan { { vlan-id1 [ to vlan-id2 ] } &<1-40> | all }
● 配置接口的链路类型为Hybrid
a. 配置接口的链路类型为Hybrid。
port link-type hybrid
b. 配置接口以tagged方式允许VLAN通过。
port hybrid tagged vlan { { vlan-id1 [ to vlan-id2 ] } &<1-10> | all }

说明接口允许通过VLAN的范围必须包含用户二层协议报文中的VLAN ID。
步骤5 使能接口基于VLAN的二层协议透明传输功能。
l2protocol-tunnel { all | user-defined-protocol protocol-name | protocol } vlan { low-vid [ to high-vid ] } &<1-10>步骤6 （可选）使能二层协议透明传输功能的接口丢弃协议报文的阈值。
l2protocol-tunnel drop-threshold rate [ user-defined-protocol protocol-name | { protocol } &<1-16> ]缺省情况下，使能二层协议透明传输功能的接口丢弃协议报文的阈值是0，表示使能二层协议透明传输功能的接口不限制入接口的二层协议报文流量。
当使能二层协议透明传输功能的接口收到大量的协议报文时，为防止是恶意攻击，可在接口下配置协议报文丢弃阈值。在单位(1秒)时间内，当二层协议报文入接口（使能二层协议透明传输功能的接口）方向通过的二层协议报文超过配置的阈值时，将丢弃协议报文。
----结束

#### 11.6.5 检查二层协议透明传输配置结果

操作步骤执行命令display
● l2protocol-tunnel group-mac { all | protocol | user- defined-protocol protocol-name }，查看所有的二层协议或者指定的二层协议的透明传输信息。
----结束

### 11.7 配置基于QinQ的二层协议透明传输

#### 11.7.1 了解基于QinQ的二层协议透明传输

当接入大量用户网络时，如果仍采用上述的基于VLAN的方式透明传输二层协议报文，那么就需要使用大量的运营商VLAN ID，造成VLAN ID资源的紧张。此时，可以在骨干网络内部使用QinQ方式来转发用户的二层协议报文。
QinQ协议是基于IEEE 802.1Q技术的一种二层隧道协议。通过在802.1Q标签报文的基础上再增加一层 802.1Q 的标签头来达到扩展 VLAN 空间的功能，从而实现私网 VLAN 在公网透明传输。

图 11-4 基于 QinQ 的二层协议透明传输如图11-4所示，PE收到VLAN为100～199的二层协议报文，为该报文打上外层VLAN20，然后在骨干网络中传输；PE收到VLAN为200～299的二层协议报文，为该报文打上外层VLAN30，然后在骨干网络中传输。同时，在PE的汇聚接口上配置基于QinQ的二层协议透明传输功能，这样既能实现不同用户网络的二层协议报文在骨干网络中的透明传输，又可以节约运营商的VLAN。
1. 骨干网设备根据用户VLAN ID，为二层协议报文分配不同的外层Tag，即公网中的VLAN ID。
2. 骨干网设备根据配置的特定的组播目的MAC地址和二层协议的目的MAC地址映射关系，将该二层协议报文的目的组播MAC地址修改为指定的组播目的MAC地址。
3. 骨干网设备根据修改MAC地址后的二层协议报文的不同外层Tag，选择不同的二层隧道，在骨干网内部的节点上按照普通的二层报文转发。
4. 用户网络的二层协议报文到达骨干网设备的出节点设备时，再次根据设备上配置的特定目的组播MAC地址和二层协议目的组播MAC地址的映射关系，将该报文的目的组播 MAC 地址还原成二层协议的原始组播 MAC 地址。去掉外层 Tag ，并根据内层用户VLAN ID，将二层协议报文转发到相应的用户网络中。

#### 11.7.2 （可选）自定义二层透明传输协议的特征信息

背景信息当用户网络中特定组播目的MAC地址的协议报文（非标准二层协议报文）需要在骨干网络中进行透明传输时，可以在PE上定义二层透明传输协议的特征信息。这些特征信息包括协议的名称、以太封装类型、报文的目的MAC地址、报文被替换后的组播MAC地址等。
配置用户自定义的二层透明传输协议的特征信息时，下面的组播MAC地址不能作为二层协议报文被替换后的组播MAC地址：

● BPDU报文的目的MAC地址：0180-C200-0000～0180-C200-002F。
● Smart Link协议报文：010F-E200-0004。
● 特殊的组播MAC地址：0100-0CCC-CCCC和0100-0CCC-CCCD。
● 本设备上已经使用过的普通组播MAC地址。
操作步骤
步骤1 进入系统视图。
system-view
步骤2 自定义二层透明传输协议的特征信息。
l2protocol-tunnel user-defined-protocol protocol-name protocol-mac protocol-mac [ encap-type
{ { ethernetii protocol-type protocol-type } | { llc dsap dsap-value ssap ssap-value } | { snap protocol-
type protocol-type } } ] group-mac { group-mac | default-group-mac }
----结束

#### 11.7.3 配置二层协议透明传输的方式

背景信息配置二层透明传输包括两种方式：
● 修改骨干网设备可以识别的缺省二层协议组播MAC地址为其他的组播MAC地址，这种方式只适用于STP/RSTP/MSTP协议。
● 替换来自用户网络的原始二层协议报文的组播MAC地址为指定组播MAC地址，适用于所有类型的二层协议透明传输。
在设备上根据二层协议的类型和需要透明传输的方式，选择如下配置步骤之一。
操作步骤
● 修改骨干网设备可以识别的缺省二层协议组播MAC地址为其他的组播MAC地址进入系统视图。
a.
system-view
b. 配置PE设备的角色为provider。
bpdu-tunnel stp bridge role provider
● 替换来自用户网络的原始二层协议报文的组播MAC地址为指定组播MAC地址
a. 进入系统视图。
system-view将二层协议报文的组播目的MAC地址替换成为一个指定的组播MAC地址。
b.
l2protocol-tunnel protocol group-mac { group-mac | default-group-mac }

说明不能将SSTP、STP和GMRP协议报文的目的MAC地址替换成相同的组播MAC地址。
配置二层协议透明传输功能时，下面的组播MAC地址不能作为二层协议报文被替换后的组播MAC地址：
● BPDU报文的目的MAC地址：0180-C200-0000～0180-C200-002F。
● Smart Link协议报文：010F-E200-0004。
特殊的组播MAC地址：0100-0CCC-CCCC和0100-0CCC-CCCD。
●
● 本设备上已经使用过的普通组播MAC地址。
----结束

#### 11.7.4 使能接口基于QinQ的二层协议透明传输功能

背景信息请在PE设备上根据需要透明传输的协议类型，进行以下配置。
说明不能把l2protocol-tunnel vlan命令和l2protocol-tunnel enable命令在同一个接口下配置相同协议类型，否则会提示配置冲突。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入PE的用户侧接口视图。
interface interface-type interface-number步骤3 将接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤 4 配置接口的链路类型为 dot1q-tunnel 。
port link-type dot1q-tunnel步骤5 为用户的二层协议报文打上外层VLAN Tag。
port default vlan vlan-id步骤6 使能接口基于QinQ的二层协议透明传输功能。
l2protocol-tunnel { all | user-defined-protocol protocol-name | protocol } vlan { low-vid [ to high-vid ] } &<1-10>说明步骤5指定的外层VLAN需要包含在步骤6配置的VLAN中。
步骤7 （可选）使能二层协议透明传输功能的接口丢弃协议报文的阈值。
l2protocol-tunnel drop-threshold rate [ user-defined-protocol protocol-name | { protocol } &<1-16> ]

缺省情况下，使能二层协议透明传输功能的接口丢弃协议报文的阈值是0，表示使能二层协议透明传输功能的接口不限制入接口的二层协议报文流量。
当使能二层协议透明传输功能的接口收到大量的协议报文时，为防止是恶意攻击，可在接口下配置协议报文丢弃阈值。在单位(1秒)时间内，当二层协议报文入接口（使能二层协议透明传输功能的接口）方向通过的二层协议报文超过配置的阈值时，将丢弃协议报文。
----结束

#### 11.7.5 检查二层协议透明传输配置结果

操作步骤
● 执行命令display l2protocol-tunnel group-mac { all | protocol | user- defined-protocol protocol-name }，查看所有的二层协议或者指定的二层协议的透明传输信息。
----结束

### 11.8 配置基于VPLS的二层协议透明传输

说明该配置仅S6780-H、S6750-H、S6750E-S、S6750-S、S6730E-H-V2、S6730-S-V2、S6730-H- V2、S5755-H、S5732-H-V2系列支持。

#### 11.8.1 了解基于VPLS的二层协议透明传输

当接入用户在运营商网络通过利用VPLS构建的L2VPN网络进行互通时，配置基于VPLS的二层协议透明传输就可以实现二层协议报文通过L2VPN隧道进行透明传输。
图 11-5 基于 VPLS 的二层协议透明传输如图11-5所示，Device的汇聚接口上配置基于VPLS的二层协议透明传输功能，根据用户接入Device设备的接口来绑定不同的VSI。
1. 配置用户网络设备接入 PE 设备的接口的二层协议透明传输功能，替换来自用户网络的原始二层协议报文的组播MAC地址为指定组播MAC地址。
2. 将用户侧接入接口绑定到同一L2VPN中，这样二层协议报文可以通过L2VPN隧道在骨干网进行二层协议透明传输。

#### 11.8.2 （可选）自定义二层透明传输协议的特征信息

背景信息当用户网络中特定组播目的MAC地址的协议报文（非标准二层协议报文）需要在骨干网络中进行透明传输时，可以在PE上定义二层透明传输协议的特征信息。这些特征信息包括协议的名称、以太封装类型、报文的目的MAC地址、报文被替换后的组播MAC地址等。
配置用户自定义的二层透明传输协议的特征信息时，下面的组播MAC地址不能作为二层协议报文被替换后的组播MAC地址：
● BPDU报文的目的MAC地址：0180-C200-0000～0180-C200-002F。
● Smart Link协议报文：010F-E200-0004。
● 特殊的组播MAC地址：0100-0CCC-CCCC和0100-0CCC-CCCD。
● 本设备上已经使用过的普通组播MAC地址。
操作步骤步骤1 进入系统视图。
system-view步骤2 自定义二层透明传输协议的特征信息。
l2protocol-tunnel user-defined-protocol protocol-name protocol-mac protocol-mac [ encap-type { { ethernetii protocol-type protocol-type } | { llc dsap dsap-value ssap ssap-value } | { snap protocol- type protocol-type } } ] group-mac { group-mac | default-group-mac }
----结束

#### 11.8.3 配置二层协议透明传输的方式

背景信息配置二层透明传输包括两种方式：
● 修改骨干网设备可以识别的缺省二层协议组播MAC地址为其他的组播MAC地址，这种方式只适用于STP/RSTP/MSTP协议。
● 替换来自用户网络的原始二层协议报文的组播MAC地址为指定组播MAC地址，适用于所有类型的二层协议透明传输。
在设备上根据二层协议的类型和需要透明传输的方式，选择如下配置步骤之一。
操作步骤
● 修改骨干网设备可以识别的缺省二层协议组播MAC地址为其他的组播MAC地址
a. 进入系统视图。
system-view
b. 配置PE设备的角色为provider。
bpdu-tunnel stp bridge role provider
● 替换来自用户网络的原始二层协议报文的组播MAC地址为指定组播MAC地址
a. 进入系统视图。
system-view

b. 将二层协议报文的组播目的MAC地址替换成为一个指定的组播MAC地址。
l2protocol-tunnel protocol group-mac { group-mac | default-group-mac }
说明
不能将SSTP、STP和GMRP协议报文的目的MAC地址替换成相同的组播MAC地址。
配置二层协议透明传输功能时，下面的组播MAC地址不能作为二层协议报文被替换后
的组播MAC地址：
● BPDU报文的目的MAC地址：0180-C200-0000～0180-C200-002F。
● Smart Link协议报文：010F-E200-0004。
● 特殊的组播MAC地址：0100-0CCC-CCCC和0100-0CCC-CCCD。
● 本设备上已经使用过的普通组播MAC地址。
----结束

#### 11.8.4 使能接口基于VPLS的二层协议透明传输功能

背景信息路由主接口和子接口接入方式的 场景，请在 上根据需要透明传输的协议类型，VPLS PE进行以下配置。
操作步骤
● 配置以太网接口接入VPLS场景的二层协议透明传输。
a. 进入系统视图。
system-view
b. 进入以太网接口视图。
interface interface-type interface-number
c. 将接口从二层模式切换到三层模式。
undo portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过undo portswitch命令将接口从二层模式切换到三层模式。
d. 将以太网接口与VSI绑定。
l2 binding vsi vsi-name
e. 使能接口基于 VPLS 的二层协议透明传输功能。
l2protocol-tunnel { all | protocol-type | user-defined-protocol protocol-name } enable说明protocol-type为lldp时，由于LLDP默认是开启状态，在执行该步骤前需要在接口视图下执行undo lldp enable命令关闭LLDP功能。
f. （可选）使能二层协议透明传输功能的接口丢弃协议报文的阈值。
l2protocol-tunnel drop-threshold rate [ user-defined-protocol protocol-name | { protocol } &<1-16> ]缺省情况下，使能二层协议透明传输功能的接口丢弃协议报文的阈值是0，表示使能二层协议透明传输功能的接口不限制入接口的二层协议报文流量。
当使能二层协议透明传输功能的接口收到大量的协议报文时，为防止恶意攻击，可在接口下配置协议报文丢弃阈值。在单位(1秒)时间内，当二层协议报

文入接口（使能二层协议透明传输功能的接口）方向通过的二层协议报文超过配置的阈值时，将丢弃协议报文。
● 配置以太网子接口接入VPLS场景的二层协议透明传输。
a. 进入系统视图。
system-view
b. 进入以太网接口视图。
interface interface-type interface-number
c. 将接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
d. 配置端口类型。
port link-type { hybrid | trunk }
e. 退出接口视图。
quit
f. 进入以太网子接口视图。
interface interface-type interface-number.subinterface-number
g. 请根据实际情况选择一种进行配置：
▪配置子接口dot1q封装的单层VLAN ID。
dot1q termination vid low-pe-vid▪配置子接口QinQ封装的双层VLAN ID。
qinq termination pe-vid pe-vid ce-vid ce-vid [ to high-ce-vid ]将以太网子接口与VSI绑定。
h.
l2 binding vsi vsi-name
i. 使能子接口基于VPLS的二层协议透明传输功能。
l2protocol-tunnel { all | protocol-type | user-defined-protocol protocol-name } enable说明protocol-type为lldp时，由于LLDP默认是开启状态，在执行该步骤前需要在子接口对应的主接口下执行undo lldp enable命令关闭LLDP功能。
protocol-type为stp时，由于STP默认是开启状态，在执行该步骤前需要在子接口对应的主接口下执行stp disable命令关闭STP功能。
j. （可选）使能二层协议透明传输功能的接口丢弃协议报文的阈值。
l2protocol-tunnel drop-threshold rate [ user-defined-protocol protocol-name | { protocol } &<1-16> ]缺省情况下，使能二层协议透明传输功能的接口丢弃协议报文的阈值是0，表示使能二层协议透明传输功能的接口不限制入接口的二层协议报文流量。
当使能二层协议透明传输功能的接口收到大量的协议报文时，为防止恶意攻击，可在接口下配置协议报文丢弃阈值。在单位(1秒)时间内，当二层协议报文入接口（使能二层协议透明传输功能的接口）方向通过的二层协议报文超过配置的阈值时，将丢弃协议报文。
----结束

#### 11.8.5 检查二层协议透明传输配置结果

操作步骤
● 执行命令display l2protocol-tunnel group-mac { all | protocol | user- defined-protocol protocol-name }，查看所有的二层协议或者指定的二层协议的透明传输信息。
----结束

### 11.9 配置BPDU协议报文透明传输

背景信息当骨干网边缘设备接入多个用户边缘设备，为了提高转发BPDU协议报文效率，骨干网设备通过硬件转发BPDU协议报文。缺省情况下，设备通过硬件转发BPDU协议报文时不允许二层接口转发BPDU协议报文。那么，骨干网边缘设备接入的多个用户边缘设备就无法实现正常互通。此时，可以配置在设备通过硬件转发 BPDU 协议报文时允许二层接口转发BPDU协议报文。
如果希望二层接口仅转发带VLAN Tag的BPDU报文，而Untag的BPDU报文正常上送CPU处理，可以在系统视图下配置二层接口支持硬件转发带VLAN Tag的BPDU协议报文功能。
操作步骤
● 配置透传所有BPDU协议报文
a. 进入系统视图。
system-view
b. 进入接口视图。
interface interface-type interface-number
c. 将接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch 命令将接口从三层模式切换到二层模式。
d. 配置设备通过二层接口进行硬件转发BPDU协议报文。
bpdu bridge enable缺省情况下，设备通过硬件转发BPDU协议报文时不允许二层接口转发BPDU协议报文。
说明在执行bpdu bridge enable命令之前，如果希望通过硬件转发某种协议（例如STP等）的BPDU报文，请首先在全局去使能该协议。
● 配置透传带VLAN Tag的BPDU协议报文
a. 进入系统视图。
system-view

b. 配置设备通过二层接口进行硬件转发带VLAN Tag的BPDU协议报文。
bpdu bridge tagged-packet enable
缺省情况下，设备通过硬件转发BPDU协议报文时不允许二层接口转发带
VLAN Tag的BPDU协议报文。
----结束

### 11.10 维护二层协议透明传输

背景信息维护二层协议透明传输，包括以下部分：
● 查看指定接口透明传输的二层协议统计信息。
display l2protocol-tunnel statistics
● 清除指定接口透明传输的二层协议统计信息。
reset l2protocol-tunnel statistics
● 查看设备的全局 BPDU 信息。
display bpdu-tunnel global config

### 11.11 二层协议透明传输配置举例

#### 11.11.1 举例：配置基于接口的二层协议透明传输

组网需求如图11-6所示，CE设备为企业处于不同地域网络的边缘设备，PE1和PE2为运营商网络的边缘设备。企业的两个网络是二层网络，并且通过运营商网络实现互联。为了防止二层网络形成环路，网络中运行STP协议，并且企业用户希望STP只在用户自有网络中运行以生成正确的生成树。
说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。
图 11-6 配置基于接口的二层协议透明传输组网图

配置思路采用如下思路配置基于接口的二层协议透明传输的基本功能：
1. 配置CE的STP功能，破除二层网络中的环路。
2. 把PE的CE侧接口加入到指定的VLAN中，实现PE设备对指定用户VLAN报文的转发。
3. 配置PE基于接口的二层协议透明传输功能，实现STP协议报文不上送PE设备的CPU进行处理。
操作步骤步骤1 使能CE设备的生成树计算功能\# 配置CE1。
<HUAWEI> system-view [HUAWEI] sysname CE1 [CE1] vlan 100 [CE1-vlan100] quit [CE1] stp enable [CE1] interface 10ge 1/0/1 [CE1-10GE1/0/1] portswitch [CE1-10GE1/0/1] port link-type access [CE1-10GE1/0/1] port default vlan 100 [CE1-10GE1/0/1] quit \# 配置CE2。
<HUAWEI> system-view [HUAWEI] sysname CE2 [CE2] vlan 100 [CE2-vlan100] quit [CE2] stp enable [CE2] interface 10ge 1/0/1 [CE2-10GE1/0/1] portswitch [CE2-10GE1/0/1] port link-type access [CE2-10GE1/0/1] port default vlan 100 [CE2-10GE1/0/1] quit步骤2 将PE1和PE2的接口10GE1/0/1加入到VLAN100中，PE设备使能二层协议透明传输功能\# 配置PE1。
<HUAWEI> system-view [HUAWEI] sysname PE1 [PE1] stp enable [PE1] vlan 100 [PE1-vlan100] quit [PE1] interface 10ge 1/0/1 [PE1-10GE1/0/1] portswitch [PE1-10GE1/0/1] port link-type access [PE1-10GE1/0/1] port default vlan 100 [PE1-10GE1/0/1] stp disable [PE1-10GE1/0/1] l2protocol-tunnel stp enable [PE1-10GE1/0/1] quit \# 配置PE2。
<HUAWEI> system-view [HUAWEI] sysname PE2 [PE2] stp enable [PE2] vlan 100 [PE2-vlan100] quit [PE2] interface 10ge 1/0/1

[PE2-10GE1/0/1] portswitch [PE2-10GE1/0/1] port link-type access [PE2-10GE1/0/1] port default vlan 100 [PE2-10GE1/0/1] stp disable [PE2-10GE1/0/1] l2protocol-tunnel stp enable [PE2-10GE1/0/1] quit说明如果对端设备发送的为非标准协议报文，用户可以先执行命令l2protocol-tunnel user- defined-protocol protocol-name protocol-mac protocol-mac [ encap-type { { ethernetii | snap } protocol-type protocol-type-value | llc dsap dsap-value ssap ssap-value } ] group- mac { group-mac | default-group-mac }，自定义二层透明传输协议的特征信息，然后执行命令l2protocol-tunnel user-defined-protocol protocol-name enable，使能接口的二层协议透明传输功能。
步骤3 配置PE替换接收到CE的STP协议报文的目的MAC地址\# 配置PE1 [PE1] l2protocol-tunnel stp group-mac 0100-5e00-0011 \# 配置PE2 [PE2] l2protocol-tunnel stp group-mac 0100-5e00-0011步骤4 配置CE2设备的优先级为4096 [CE2] stp priority 4096步骤5 检查配置结果\# 配置完成后，在PE上使用display l2protocol-tunnel group-mac命令可以查看透明传输的二层协议名称、协议类型、协议报文的组播目的MAC地址、Group MAC地址以及报文的优先级。
以PE1的显示为例。
[PE1] display l2protocol-tunnel group-mac stp Protocol EncapeType ProtocolType Protocol-MAC Group-MAC Pri
----------------------------------------------------------------------------- stp llc dsap 0x42 0180-c200-0000 0100-5e00-0011 0 ssap 0x42 \# 等待30秒，在CE1和CE2设备上执行display stp brief命令可以检查MSTP的根。CE1和CE2之间完成了生成树计算功能。CE1上的10GE1/0/1为根（Root）端口，CE2上的10GE1/0/1为指定（Designated）端口。
[CE1] display stp brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 ROOT forwarding none 2000 disable [CE2] display stp brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 DESI forwarding none 2000 disable
----结束配置文件
● CE1的配置文件\# sysname CE1 \# vlan batch 100 \# interface 10GE1/0/1

port link-type access port default vlan 100 \# return
● CE2的配置文件\# sysname CE2 \# vlan batch 100 \# stp instance 0 priority 4096 \# interface 10GE1/0/1 port link-type access port default vlan 100 \# return
● PE1的配置文件\# sysname PE1 \# vlan batch 100 \# l2protocol-tunnel stp group-mac 0100-5e00-0011 \# interface 10GE1/0/1 port link-type access port default vlan 100 stp disable l2protocol-tunnel stp enable \# return
● PE2的配置文件\# sysname PE2 \# vlan batch 100 \# l2protocol-tunnel stp group-mac 0100-5e00-0011 \# interface 10GE1/0/1 port link-type access port default vlan 100 stp disable l2protocol-tunnel stp enable \# return

#### 11.11.2 举例：配置基于VLAN的二层协议透明传输

组网需求如图11-7所示，CE设备为企业处于不同地域网络的边缘设备，PE1和PE2为运营商的边缘设备。VLAN100和VLAN200所属二层网络为不同用户，并且通过运营商网络实现互联。为了防止二层网络形成环路，网络中运行STP协议，并且企业用户希望STP只在各自自有网络中运行以生成正确的生成树，即：
● VLAN100中的设备可以共同完成生成树计算。
● VLAN200中的设备可以共同完成生成树计算。

说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。
图 配置基于 的二层协议透明传输组网图11-7 VLAN配置思路采用如下的思路配置基于VLAN的二层协议透明传输的基本功能：
1. 配置CE设备的STP功能，破除二层网络中的环路。
2. 配置CE发送到PE的STP协议报文带有指定的Tag值，实现VLAN100和VLAN200中STP独立计算。
3. 配置PE基于VLAN的二层协议透明传输功能，实现STP协议报文不上送PE设备的CPU进行处理。
操作步骤步骤1 使能CE的生成树计算功能\# 配置CE1。
<HUAWEI> system-view [HUAWEI] sysname CE1 [CE1] stp enable \# 配置CE2。
<HUAWEI> system-view [HUAWEI] sysname CE2 [CE2] stp enable \# 配置CE3。
<HUAWEI> system-view [HUAWEI] sysname CE3 [CE3] stp enable \# 配置CE4。
<HUAWEI> system-view [HUAWEI] sysname CE4 [CE4] stp enable步骤2 配置CE1与CE2发送到PE的STP协议报文带Tag100。配置CE3与CE4发送到PE的STP协议报文带Tag200

\# 配置CE1。
[CE1] vlan 100 [CE1-vlan100] quit [CE1] interface 10ge 1/0/1 [CE1-10GE1/0/1] portswitch [CE1-10GE1/0/1] port link-type trunk [CE1-10GE1/0/1] port trunk allow-pass vlan 100 [CE1-10GE1/0/1] stp bpdu vlan 100 [CE1-10GE1/0/1] quit \# 配置CE2。
[CE2] vlan 100 [CE2-vlan100] quit [CE2] interface 10ge 1/0/1 [CE2-10GE1/0/1] portswitch [CE2-10GE1/0/1] port link-type trunk [CE2-10GE1/0/1] port trunk allow-pass vlan 100 [CE2-10GE1/0/1] stp bpdu vlan 100 [CE2-10GE1/0/1] quit \# 配置CE3。
[CE3] vlan 200 [CE3-vlan200] quit [CE3] interface 10ge 1/0/1 [CE3-10GE1/0/1] portswitch [CE3-10GE1/0/1] port link-type trunk [CE3-10GE1/0/1] port trunk allow-pass vlan 200 [CE3-10GE1/0/1] stp bpdu vlan 200 [CE3-10GE1/0/1] quit \# 配置CE4。
[CE4] vlan 200 [CE4-vlan200] quit [CE4] interface 10ge 1/0/1 [CE4-10GE1/0/1] portswitch [CE4-10GE1/0/1] port link-type trunk [CE4-10GE1/0/1] port trunk allow-pass vlan 200 [CE4-10GE1/0/1] stp bpdu vlan 200 [CE4-10GE1/0/1] quit步骤3 配置PE的接口，使得CE的STP协议报文可以透明传输到对端\# 配置PE1。
<HUAWEI> system-view [HUAWEI] sysname PE1 [PE1] vlan 100 [PE1-vlan100] quit [PE1] vlan 200 [PE1-vlan200] quit [PE1] interface 10ge 1/0/2 [PE1-10GE1/0/2] portswitch [PE1-10GE1/0/2] port link-type trunk [PE1-10GE1/0/2] port trunk allow-pass vlan 100 [PE1-10GE1/0/2] l2protocol-tunnel stp vlan 100 [PE1-10GE1/0/2] quit [PE1] interface 10ge 1/0/3 [PE1-10GE1/0/3] portswitch [PE1-10GE1/0/3] port link-type trunk [PE1-10GE1/0/3] port trunk allow-pass vlan 200 [PE1-10GE1/0/3] l2protocol-tunnel stp vlan 200 [PE1-10GE1/0/3] quit \# 配置PE2。
<HUAWEI> system-view [HUAWEI] sysname PE2

[PE2] vlan 100 [PE2-vlan100] quit [PE2] vlan 200 [PE2-vlan200] quit [PE2] interface 10ge 1/0/2 [PE2-10GE1/0/2] portswitch [PE2-10GE1/0/2] port link-type trunk [PE2-10GE1/0/2] port trunk allow-pass vlan 100 [PE2-10GE1/0/2] l2protocol-tunnel stp vlan 100 [PE2-10GE1/0/2] quit [PE2] interface 10ge 1/0/3 [PE2-10GE1/0/3] portswitch [PE2-10GE1/0/3] port link-type trunk [PE2-10GE1/0/3] port trunk allow-pass vlan 200 [PE2-10GE1/0/3] l2protocol-tunnel stp vlan 200 [PE2-10GE1/0/3] quit说明如果对端设备发送的为非标准协议报文，用户可以先执行命令l2protocol-tunnel user- defined-protocol protocol-name protocol-mac protocol-mac [ encap-type { { ethernetii | snap } protocol-type protocol-type-value | llc dsap dsap-value ssap ssap-value } ] group- mac { group-mac | default-group-mac }，自定义二层透明传输协议的特征信息，然后执行命令l2protocol-tunnel user-defined-protocol protocol-name vlan { low-id [ to high-id ] } &<1-10> ，使能接口基于 VLAN 的二层协议透明传输功能。
步骤4 配置PE替换接收到CE的STP协议报文的MAC地址\# 配置PE1。
[PE1] l2protocol-tunnel stp group-mac 0100-5e00-0011 \# 配置PE2。
[PE2] l2protocol-tunnel stp group-mac 0100-5e00-0011步骤5 配置CE2和CE4设备的优先级为4096 \# 配置CE2。
[CE2] stp priority 4096 \# 配置CE4。
[CE4] stp priority 4096步骤6 检查配置结果配置完成后，在PE上使用display group-mac命令可以查看透明\# l2protocol-tunnel传输的二层协议名称、协议类型、协议报文的组播目的MAC地址、Group MAC地址以及报文的优先级。
以PE1的显示为例。
[PE1] display l2protocol-tunnel group-mac stp Protocol EncapeType ProtocolType Protocol-MAC Group-MAC Pri
----------------------------------------------------------------------------- stp llc dsap 0x42 0180-c200-0000 0100-5e00-0011 0 ssap 0x42等待30秒后，在CE1和CE2设备上执行display brief命令可以检查MSTP的根。
\# stp CE1和CE2之间完成了生成树计算功能。CE1上的10GE1/0/1为根（Root）端口，CE2上的 10GE1/0/1 为指定（ Designated ）端口。
[CE1] display stp brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 ROOT forwarding none 2000 disable

[CE2] display stp brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 DESI forwarding none 2000 disable \# 等待30秒后，在CE3和CE4设备上执行display stp brief命令可以检查MSTP的根。
CE3和CE4之间完成了生成树计算功能。CE3上的10GE1/0/1为根（Root）端口，CE4上的10GE1/0/1为指定（Designated）端口。
[CE3] display stp brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 ROOT forwarding none 2000 disable [CE4] display stp brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 DESI forwarding none 2000 disable
----结束配置文件
● CE1的配置文件\# sysname CE1 \# vlan batch 100 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 100 stp bpdu vlan 100 \# return
● CE2的配置文件\# sysname CE2 \# vlan batch 100 \# stp instance 0 priority 4096 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 100 stp bpdu vlan 100 \# return
● CE3的配置文件\# sysname CE3 \# vlan batch 200 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 200 stp bpdu vlan 200 \# return
● CE4的配置文件\# sysname CE4 \# vlan batch 200 \# stp instance 0 priority 4096

\# \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 200 stp bpdu vlan 200 \# return
● PE1的配置文件\# sysname PE1 \# vlan batch 100 200 \# l2protocol-tunnel stp group-mac 0100-5e00-0011 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 100 l2protocol-tunnel stp vlan 100 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 200 l2protocol-tunnel stp vlan 200 \# return
● PE2的配置文件\# sysname PE2 \# vlan batch 100 200 \# l2protocol-tunnel stp group-mac 0100-5e00-0011 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 100 l2protocol-tunnel stp vlan 100 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 200 l2protocol-tunnel stp vlan 200 \# return

#### 11.11.3 举例：配置基于QinQ（Dot1q-tunnel）的二层协议透明传输

组网需求如图11-8所示，CE设备为企业处于不同地域网络的边缘设备，PE1和PE2为运营商的边缘设备。VLAN100和VLAN200所属二层网络为不同用户，并且通过运营商网络实现互联。为了防止二层网络形成环路，网络中运行STP协议，并且企业用户希望STP只在各自自有网络中运行以生成正确的生成树。即：
● VLAN100 中的设备可以共同完成生成树计算。
● VLAN200中的设备可以共同完成生成树计算。
同时，由于公网VLAN资源紧张，需要尽量减少使用运营商网络VLAN ID数量。

说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。
图 11-8 基于 QinQ 的二层协议透明传输组网图配置思路采用如下的思路配置基于QinQ（Dot1q-tunnel）的二层协议透明传输的基本功能：
1. 配置CE设备的STP功能，破除二层网络中的环路。
2. 配置CE发送到PE的STP协议报文带有指定的Tag值，实现VLAN100和VLAN200中STP独立计算。
3. 配置PE基于QinQ的二层协议透明传输功能，实现STP协议报文不上送PE设备的CPU进行处理。
4. 配置PE的QinQ（Dot1q-tunnel）功能。使得CE发出的带有不同Tag值的STP协议报文都被打上外层Tag10在骨干网络中传输，实现节约公网VLAN资源。
操作步骤步骤1 使能CE设备的生成树计算功能\# 配置CE1。
<HUAWEI> system-view [HUAWEI] sysname CE1 [CE1] stp enable \# 配置CE2。
<HUAWEI> system-view [HUAWEI] sysname CE2 [CE2] stp enable \# 配置CE3。
<HUAWEI> system-view [HUAWEI] sysname CE3 [CE3] stp enable \# 配置 CE4 。
<HUAWEI> system-view [HUAWEI] sysname CE4 [CE4] stp enable

步骤2 配置CE1与CE2发送到PE的STP协议报文带Tag100。配置CE3与CE4发送到PE的STP协议报文带Tag200 \# 配置CE1。
[CE1] vlan 100 [CE1-vlan100] quit [CE1] interface 10ge 1/0/1 [CE1-10GE1/0/1] portswitch [CE1-10GE1/0/1] port link-type trunk [CE1-10GE1/0/1] port trunk allow-pass vlan 100 [CE1-10GE1/0/1] stp bpdu vlan 100 [CE1-10GE1/0/1] quit \# 配置CE2。
[CE2] vlan 100 [CE2-vlan100] quit [CE2] interface 10ge 1/0/1 [CE2-10GE1/0/1] portswitch [CE2-10GE1/0/1] port link-type trunk [CE2-10GE1/0/1] port trunk allow-pass vlan 100 [CE2-10GE1/0/1] stp bpdu vlan 100 [CE2-10GE1/0/1] quit \# 配置CE3。
[CE3] vlan 200 [CE3-vlan200] quit [CE3] interface 10ge 1/0/1 [CE3-10GE1/0/1] portswitch [CE3-10GE1/0/1] port link-type trunk [CE3-10GE1/0/1] port trunk allow-pass vlan 200 [CE3-10GE1/0/1] stp bpdu vlan 200 [CE3-10GE1/0/1] quit \# 配置CE4。
[CE4] vlan 200 [CE4-vlan200] quit [CE4] interface 10ge 1/0/1 [CE4-10GE1/0/1] portswitch [CE4-10GE1/0/1] port link-type trunk [CE4-10GE1/0/1] port trunk allow-pass vlan 200 [CE4-10GE1/0/1] stp bpdu vlan 200 [CE4-10GE1/0/1] quit步骤3 配置PE的QinQ二层协议透明传输功能。使来自CE的VLAN100和VLAN200的报文被打上外层Tag10在运营商网络中传输\# 配置 PE1 。
[PE1] vlan 10 [PE1-vlan10] quit [PE1] interface 10ge 1/0/2 [PE1-10GE1/0/2] portswitch [PE1-10GE1/0/2] port link-type dot1q-tunnel [PE1-10GE1/0/2] port default vlan 10 [PE1-10GE1/0/2] l2protocol-tunnel stp vlan 10 [PE1-10GE1/0/2] quit [PE1] interface 10ge 1/0/3 [PE1-10GE1/0/3] portswitch [PE1-10GE1/0/3] port link-type dot1q-tunnel [PE1-10GE1/0/3] port default vlan 10 [PE1-10GE1/0/3] l2protocol-tunnel stp vlan 10 [PE1-10GE1/0/3] quit \# 配置PE2。

[PE2] vlan 10 [PE2-vlan10] quit [PE2] interface 10ge 1/0/2 [PE2-10GE1/0/2] portswitch [PE2-10GE1/0/2] port link-type dot1q-tunnel [PE2-10GE1/0/2] port default vlan 10 [PE2-10GE1/0/2] l2protocol-tunnel stp vlan 10 [PE2-10GE1/0/2] quit [PE2] interface 10ge 1/0/3 [PE2-10GE1/0/3] portswitch [PE2-10GE1/0/3] port link-type dot1q-tunnel [PE2-10GE1/0/3] port default vlan 10 [PE2-10GE1/0/3] l2protocol-tunnel stp vlan 10 [PE2-10GE1/0/3] quit说明如果对端设备发送的为非标准协议报文，用户可以先执行命令l2protocol-tunnel user- defined-protocol protocol-name protocol-mac protocol-mac [ encap-type { { ethernetii | snap } protocol-type protocol-type-value | llc dsap dsap-value ssap ssap-value } ] group- mac { group-mac | default-group-mac }，自定义二层透明传输协议的特征信息，然后执行命令l2protocol-tunnel user-defined-protocol protocol-name vlan { low-id [ to high-id ] } &<1-10>，使能接口基于QinQ的二层协议透明传输功能。
步骤 4 配置 PE 替换接收到 CE 的 STP 协议报文的 MAC 地址\# 配置PE1 [PE1] l2protocol-tunnel stp group-mac 0100-5e00-0011 \# 配置PE2 [PE2] l2protocol-tunnel stp group-mac 0100-5e00-0011步骤5 检查配置结果配置完成后，在PE上使用display l2protocol-tunnel group-mac命令可以查看透明传输的二层协议名称、协议类型、协议报文的组播目的MAC地址、Group MAC地址以及报文的优先级。
以PE1的显示为例。
[PE1] display l2protocol-tunnel group-mac stp Protocol EncapeType ProtocolType Protocol-MAC Group-MAC Pri
----------------------------------------------------------------------------- stp llc dsap 0x42 0180-c200-0000 0100-5e00-0011 0 ssap 0x42配置完成后，在CE1和CE2设备上执行display stp brief命令可以检查MSTP的根。CE1和 CE2 之间完成了生成树计算功能。 CE1 上的 10GE1/0/1 为根（ Root ）端口， CE2 上的10GE1/0/1为指定（Designated）端口。
[CE1] display stp brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 ROOT forwarding none 2000 disable [CE2] display stp brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 DESI forwarding none 2000 disable在CE3和CE4设备上执行display stp brief命令可以检查MSTP的根。CE3和CE4之间完成了生成树计算功能。CE3上的10GE1/0/1为根（Root）端口，CE4上的10GE1/0/1为指定（ Designated ）端口。
[CE3] display stp brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 ROOT forwarding none 2000 disable

[CE4] display stp brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 DESI forwarding none 2000 disable在PE设备上执行display vlan命令可以查看QinQ的信息。
以PE1的显示为例。
[PE1] display vlan 10 verbose
* : Management-VLAN
--------------------- VLAN ID : 10 VLAN Name :
VLAN Type : Common Description : VLAN 0010 Status : Enable Broadcast : Enable MAC Learning : Enable Smart MAC Learning : Disable Current MAC Learning Result : Enable Statistics : Disable Property : Default VLAN State : Up
---------------- Untagged Port: 10GE1/0/1 10GE1/0/2
---------------- Active Untag Port: 10GE1/0/1 10GE1/0/2
------------------- Interface Physical 10GE1/0/1 Up 10GE1/0/2 Up
----结束配置文件CE1的配置文件
●\# sysname CE1 \# vlan batch 100 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 100 stp bpdu vlan 100 \# return
● CE2的配置文件\# sysname CE2 \# vlan batch 100 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 100 stp bpdu vlan 100 \# return
● CE3的配置文件\# sysname CE3 \# vlan batch 200 \#

interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 200 stp bpdu vlan 200 \# return
● CE4的配置文件\# sysname CE4 \# vlan batch 200 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 200 stp bpdu vlan 200 \# return
● PE1的配置文件\# sysname PE1 \# vlan batch 10 \# l2protocol-tunnel stp group-mac 0100-5e00-0011 \# interface 10GE1/0/2 port link-type dot1q-tunnel port default vlan 10 l2protocol-tunnel stp vlan 10 \# interface 10GE1/0/3 port link-type dot1q-tunnel port default vlan 10 l2protocol-tunnel stp vlan 10 \# return
● PE2的配置文件\# sysname PE2 \# vlan batch 10 \# l2protocol-tunnel stp group-mac 0100-5e00-0011 \# interface 10GE1/0/2 port link-type dot1q-tunnel port default vlan 10 l2protocol-tunnel stp vlan 10 \# interface 10GE1/0/3 port link-type dot1q-tunnel port default vlan 10 l2protocol-tunnel stp vlan 10 \# return

#### 11.11.4 举例：配置基于QinQ（VLAN Stacking）的二层协议透明传输

组网需求如图11-9所示，CE设备为企业处于不同地域网络的边缘设备，PE1和PE2为运营商的边缘设备。VLAN100和VLAN200所属二层网络为不同用户，并且通过运营商网络实现互联。为了防止二层网络形成环路，网络中运行STP协议，并且企业用户希望STP只在各自自有网络中运行以生成正确的生成树。即：
● VLAN100中的设备可以共同完成生成树计算。
● VLAN200中的设备可以共同完成生成树计算。
同时，由于公网VLAN资源紧张，需要尽量减少使用运营商网络VLAN ID数量。
说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。
图 11-9 基于 QinQ 的二层协议透明传输组网图配置思路采用如下的思路配置基于QinQ（VLAN Stacking）的二层协议透明传输的基本功能：
1. 配置CE设备的STP功能，破除二层网络中的环路。
2. 配置CE发送到PE的STP协议报文带有指定的Tag值，实现VLAN100和VLAN200中STP 独立计算。
3. 配置PE基于VLAN的二层协议透明传输功能，实现STP协议报文不上送PE设备的CPU进行处理。
4. 配置PE的QinQ（VLAN Stacking）功能。使得CE发出的带有不同Tag值的STP协议报文都被打上外层Tag10在骨干网络中传输，实现节约公网VLAN资源。
操作步骤步骤1 使能CE设备的生成树计算功能\# 配置 CE1 。
<HUAWEI> system-view [HUAWEI] sysname CE1 [CE1] stp enable

\# 配置CE2。
<HUAWEI> system-view [HUAWEI] sysname CE2 [CE2] stp enable \# 配置CE3。
<HUAWEI> system-view [HUAWEI] sysname CE3 [CE3] stp enable \# 配置CE4。
<HUAWEI> system-view [HUAWEI] sysname CE4 [CE4] stp enable步骤2 配置CE1与CE2发送到PE的STP协议报文带Tag100。配置CE3与CE4发送到PE的STP协议报文带Tag200 \# 配置CE1。
[CE1] vlan 100 [CE1-vlan100] quit [CE1] interface 10ge 1/0/1 [CE1-10GE1/0/1] portswitch [CE1-10GE1/0/1] port link-type hybrid [CE1-10GE1/0/1] port hybrid tagged vlan 100 [CE1-10GE1/0/1] stp bpdu vlan 100 [CE1-10GE1/0/1] quit \# 配置CE2。
[CE2] vlan 100 [CE2-vlan100] quit [CE2] interface 10ge 1/0/1 [CE2-10GE1/0/1] portswitch [CE2-10GE1/0/1] port link-type hybrid [CE2-10GE1/0/1] port hybrid tagged vlan 100 [CE2-10GE1/0/1] stp bpdu vlan 100 [CE2-10GE1/0/1] quit \# 配置CE3。
[CE3] vlan 200 [CE3-vlan200] quit [CE3] interface 10ge 1/0/1 [CE3-10GE1/0/1] portswitch [CE3-10GE1/0/1] port link-type hybrid [CE3-10GE1/0/1] port hybrid tagged vlan 200 [CE3-10GE1/0/1] stp bpdu vlan 200 [CE3-10GE1/0/1] quit \# 配置CE4。
[CE4] vlan 200 [CE4-vlan200] quit [CE4] interface 10ge 1/0/1 [CE4-10GE1/0/1] portswitch [CE4-10GE1/0/1] port link-type hybrid [CE4-10GE1/0/1] port hybrid tagged vlan 200 [CE4-10GE1/0/1] stp bpdu vlan 200 [CE4-10GE1/0/1] quit步骤 3 配置 PE 的 QinQ 二层协议透明传输功能。使来自 CE 的 VLAN100 和 VLAN200 的报文被打上外层Tag10在运营商网络中传输\# 配置PE1。

<HUAWEI> system-view [HUAWEI] sysname PE1 [PE1] vlan 10 [PE1-vlan10] quit [PE1] interface 10ge 1/0/2 [PE1-10GE1/0/2] portswitch [PE1-10GE1/0/2] port link-type hybrid [PE1-10GE1/0/2] port hybrid untagged vlan 10 [PE1-10GE1/0/2] port vlan-stacking vlan 100 stack-vlan 10 [PE1-10GE1/0/2] l2protocol-tunnel stp vlan 10 [PE1-10GE1/0/2] quit [PE1] interface 10ge 1/0/3 [PE1-10GE1/0/3] portswitch [PE1-10GE1/0/3] port link-type hybrid [PE1-10GE1/0/3] port hybrid untagged vlan 10 [PE1-10GE1/0/3] port vlan-stacking vlan 200 stack-vlan 10 [PE1-10GE1/0/3] l2protocol-tunnel stp vlan 10 [PE1-10GE1/0/3] quit [PE1] interface 10ge 1/0/1 [PE1-10GE1/0/1] portswitch [PE1-10GE1/0/1] port link-type trunk [PE1-10GE1/0/1] port trunk allow-pass vlan 10 [PE1-10GE1/0/1] quit \# 配置PE2。
<HUAWEI> system-view [HUAWEI] sysname PE2 [PE2] vlan 10 [PE2-vlan10] quit [PE2] interface 10ge 1/0/2 [PE2-10GE1/0/2] portswitch [PE2-10GE1/0/2] port link-type hybrid [PE2-10GE1/0/2] port hybrid untagged vlan 10 [PE2-10GE1/0/2] port vlan-stacking vlan 100 stack-vlan 10 [PE2-10GE1/0/2] l2protocol-tunnel stp vlan 10 [PE2-10GE1/0/2] quit [PE2] interface 10ge 1/0/3 [PE2-10GE1/0/3] portswitch [PE2-10GE1/0/3] port link-type hybrid [PE2-10GE1/0/3] port hybrid untagged vlan 10 [PE2-10GE1/0/3] port vlan-stacking vlan 200 stack-vlan 10 [PE2-10GE1/0/3] l2protocol-tunnel stp vlan 10 [PE2-10GE1/0/3] quit [PE2] interface 10ge 1/0/1 [PE2-10GE1/0/1] portswitch [PE2-10GE1/0/1] port link-type trunk [PE2-10GE1/0/1] port trunk allow-pass vlan 10 [PE2-10GE1/0/1] quit说明如果对端设备发送的为非标准协议报文，用户可以先执行命令l2protocol-tunnel user- defined-protocol protocol-name protocol-mac protocol-mac [ encap-type { { ethernetii | snap } protocol-type protocol-type-value | llc dsap dsap-value ssap ssap-value } ] group- mac { group-mac | default-group-mac }，自定义二层透明传输协议的特征信息，然后执行命令l2protocol-tunnel user-defined-protocol protocol-name vlan { low-id [ to high-id ] } &<1-10>，使能接口基于QinQ的二层协议透明传输功能。
步骤4 配置PE替换接收到CE的STP协议报文的MAC地址\# 配置PE1 [PE1] l2protocol-tunnel stp group-mac 0100-0100-0100 \# 配置PE2 [PE2] l2protocol-tunnel stp group-mac 0100-0100-0100

步骤5 配置CE2和CE4设备的优先级为4096 \# 配置CE2。
[CE2] stp priority 4096配置CE4。
\# [CE4] stp priority 4096步骤6 检查配置结果配置完成后，在PE上使用display group-mac命令可以查看透明传l2protocol-tunnel输的二层协议名称、协议类型、协议报文的组播目的MAC地址、Group MAC地址以及报文的优先级。
以PE1的显示为例。
[PE1] display l2protocol-tunnel group-mac stp Protocol EncapeType ProtocolType Protocol-MAC Group-MAC Pri
----------------------------------------------------------------------------- stp llc dsap 0x42 0180-c200-0000 0100-0100-0100 0 ssap 0x42配置完成后，在CE1和CE2设备上执行display stp brief命令可以检查MSTP的根。CE1和 CE2 之间完成了生成树计算功能。 CE1 上的 10GE1/0/1 为根（ Root ）端口， CE2 上的10GE1/0/1为指定（Designated）端口。
[CE1] display stp brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 ROOT forwarding none 2000 disable [CE2] display stp brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 DESI forwarding none 2000 disable在CE3和CE4设备上执行display stp brief命令可以检查MSTP的根。CE3和CE4之间完成了生成树计算功能。CE3上的10GE1/0/1为根（Root）端口，CE4上的10GE1/0/1为指定（Designated）端口。
[CE3] display stp brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 ROOT forwarding none 2000 disable [CE4] display stp brief MSTID Port Role STP State Protection Cost Edged 0 10GE1/0/1 DESI forwarding none 2000 disable在PE设备上执行display vlan命令可以查看QinQ的信息。
以PE1的显示为例。
[PE1] display vlan 10 verbose
* : Management-VLAN
--------------------- VLAN ID : 10 VLAN Name :
VLAN Type : Common Description : VLAN 0010 Status : Enable Broadcast : Enable MAC Learning : Enable Smart MAC Learning : Disable Current MAC Learning Result : Enable Statistics : Disable Property : Default VLAN State : Up
---------------- Untagged Port: 10GE1/0/2 10GE1/0/3
---------------- Active Untag Port: 10GE1/0/2 10GE1/0/3

----------------
Tagged Port: 10GE1/0/1
----------------
Active Tag Port: 10GE1/0/1
----------------
QinQ-stack Port: 10GE1/0/2 10GE1/0/3
---------------------
Interface Physical
10GE1/0/1 Up
10GE1/0/2 Up
10GE1/0/3 Up
----结束
配置文件
● CE1的配置文件
\#
sysname CE1
\#
vlan batch 100
\#
interface 10GE1/0/1
port link-type hybrid
port hybrid tagged vlan 100
stp bpdu vlan 100
\#
return
● CE2的配置文件
\#
sysname CE2
\#
vlan batch 100
\#
stp instance 0 priority 4096
\#
interface 10GE1/0/1
port link-type hybrid
port hybrid tagged vlan 100
stp bpdu vlan 100
\#
return
● CE3的配置文件
\#
sysname CE3
\#
vlan batch 200
\#
interface 10GE1/0/1
port link-type hybrid
port hybrid tagged vlan 200
stp bpdu vlan 200
\#
return
● CE4的配置文件
\#
sysname CE4
\#
vlan batch 200
\#
stp instance 0 priority 4096
\#
interface 10GE1/0/1
port link-type hybrid
port hybrid tagged vlan 200

stp bpdu vlan 200 \# return
● PE1的配置文件\# sysname PE1 \# vlan batch 10 \# l2protocol-tunnel stp group-mac 0100-0100-0100 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# interface 10GE1/0/2 port link-type hybrid port hybrid untagged vlan 10 port vlan-stacking vlan 100 stack-vlan 10 l2protocol-tunnel stp vlan 10 \# interface 10GE1/0/3 port link-type hybrid port hybrid untagged vlan 10 port vlan-stacking vlan 200 stack-vlan 10 l2protocol-tunnel stp vlan 10 \# return
● PE2的配置文件\# sysname PE2 \# vlan batch 10 \# l2protocol-tunnel stp group-mac 0100-0100-0100 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# interface 10GE1/0/2 port link-type hybrid port hybrid untagged vlan 10 port vlan-stacking vlan 100 stack-vlan 10 l2protocol-tunnel stp vlan 10 \# interface 10GE1/0/3 port link-type hybrid port hybrid untagged vlan 10 port vlan-stacking vlan 200 stack-vlan 10 l2protocol-tunnel stp vlan 10 \# return

#### 11.11.5 举例：配置基于VPLS的二层协议透明传输

组网需求如图11-10所示，CE设备为企业处于不同地域网络的边缘设备，PE1和PE2为运营商网络的边缘设备。企业的两个网络是二层网络，在运营商网络利用 VPLS 构建的 L2VPN 实现二层互联。为了防止二层网络形成环路，网络中运行STP协议，并且企业用户希望STP只在用户自有网络中运行以生成正确的生成树。

说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
图 11-10 配置基于 VPLS 的二层协议透明传输组网图表 11-5 数据规划

| 设备 | 接口 | 对应的三层接口 | IP地址 |
|---|---|---|---|
| PE1 | 10GE1/0/1 | 10GE1/0/1.1 | - |
|  | 10GE1/0/2 | VLANIF20 | 4.4.4.4/24 |
|  | Loopback1 | - | 1.1.1.1/32 |
| PE2 | 10GE1/0/1 | VLANIF30 | 5.5.5.5/24 |
|  | 10GE1/0/2 | 10GE1/0/2.1 | - |
|  | Loopback1 | - | 3.3.3.3/32 |
| PE3 | 10GE1/0/1 | VLANIF20 | 4.4.4.5/24 |
|  | 10GE1/0/2 | VLANIF30 | 5.5.5.4/24 |
|  | Loopback1 | - | 2.2.2.2/32 |
| CE1 | 10GE1/0/1 | VLANIF10 | 10.1.1.1/24 |
| CE2 | 10GE1/0/1 | VLANIF10 | 10.1.1.2/24 |

配置思路采用如下思路配置基于 VPLS 的二层协议透明传输的基本功能：
1. 在PE1和PE2之间利用VPLS构建L2VPN网络。
2. 配置CE的STP功能，破除二层网络中的环路。

3. 在PE的CE侧接口创建终结子接口，并将子接口绑定VSI实例，实现CE侧设备接入
L2VPN网络。
4. 配置PE基于VPLS的二层协议透明传输功能，实现STP协议报文不上送PE设备的
CPU进行处理。
操作步骤
步骤1 配置PE设备之间基于VPLS的L2VPN网络。
1. 按表11-5配置各接口所属的VLAN和VLANIF接口的IP地址。
\# 配置CE1。
<HUAWEI> system-view
[HUAWEI] sysname CE1
[CE1] vlan batch 10
[CE1] interface 10ge 1/0/1
[CE1-10GE1/0/1] port link-type trunk
[CE1-10GE1/0/1] port trunk allow-pass vlan 10
[CE1-10GE1/0/1] quit
[CE1] interface vlanif 10
[CE1-Vlanif10] ip address 10.1.1.1 24
[CE1-Vlanif10] quit
\# 配置CE2。
<HUAWEI> system-view
[HUAWEI] sysname CE2
[CE2] vlan batch 10
[CE2] interface 10ge 1/0/1
[CE2-10GE1/0/1] port link-type trunk
[CE2-10GE1/0/1] port trunk allow-pass vlan 10
[CE2-10GE1/0/1] quit
[CE2] interface vlanif 10
[CE2-Vlanif10] ip address 10.1.1.2 24
[CE2-Vlanif10] quit
\# 配置PE1。PE2和P的配置同PE1。
<HUAWEI> system-view
[HUAWEI] sysname PE1
[PE1] vlan batch 20
[PE1] interface 10ge 1/0/2
[PE1-10GE1/0/2] port link-type hybrid
[PE1-10GE1/0/2] port hybrid pvid vlan 20
[PE1-10GE1/0/2] port hybrid tagged vlan 20
[PE1-10GE1/0/2] quit
[PE1] interface vlanif 20
[PE1-Vlanif20] ip address 4.4.4.4 24
[PE1-Vlanif20] quit
2. 配置路由协议。
配置OSPF时，注意需要发布PE1、P和PE2的32位Loopback接口地址（LSR-
ID）。
\# 配置PE1。
[PE1] router id 1.1.1.1
[PE1] interface loopback 1
[PE1-LoopBack1] ip address 1.1.1.1 32
[PE1-LoopBack1] quit
[PE1] ospf 1
[PE1-ospf-1] area 0
[PE1-ospf-1-area-0.0.0.0] network 1.1.1.1 0.0.0.0
[PE1-ospf-1-area-0.0.0.0] network 4.4.4.4 0.0.0.255
[PE1-ospf-1-area-0.0.0.0] quit
[PE1-ospf-1] quit

\# 配置P。
[P] router id 2.2.2.2 [P] interface loopback 1 [P-LoopBack1] ip address 2.2.2.2 32 [P-LoopBack1] quit [P] ospf 1 [P-ospf-1] area 0 [P-ospf-1-area-0.0.0.0] network 2.2.2.2 0.0.0.0 [P-ospf-1-area-0.0.0.0] network 4.4.4.5 0.0.0.255 [P-ospf-1-area-0.0.0.0] network 5.5.5.4 0.0.0.255 [P-ospf-1-area-0.0.0.0] quit [P-ospf-1] quit \# 配置PE2。
[PE2] router id 3.3.3.3 [PE2] interface loopback 1 [PE2-LoopBack1] ip address 3.3.3.3 32 [PE2-LoopBack1] quit [PE2] ospf 1 [PE2-ospf-1] area 0 [PE2-ospf-1-area-0.0.0.0] network 3.3.3.3 0.0.0.0 [PE2-ospf-1-area-0.0.0.0] network 5.5.5.5 0.0.0.255 [PE2-ospf-1-area-0.0.0.0] quit [PE2-ospf-1] quit
3. 配置MPLS基本能力和LDP \# 配置PE1。
[PE1] mpls lsr-id 1.1.1.1 [PE1] mpls [PE1-mpls] quit [PE1] mpls ldp [PE1-mpls-ldp] quit [PE1] interface vlanif 20 [PE1-Vlanif20] mpls [PE1-Vlanif20] mpls ldp [PE1-Vlanif20] quit \# 配置P。
[P] mpls lsr-id 2.2.2.2 [P] mpls [P-mpls] quit [P] mpls ldp [P-mpls-ldp] quit [P] interface vlanif 20 [P-Vlanif20] mpls [P-Vlanif20] mpls ldp [P-Vlanif20] quit [P] interface vlanif 30 [P-Vlanif30] mpls [P-Vlanif30] mpls ldp [P-Vlanif30] quit \# 配置PE2。
[PE2] mpls lsr-id 3.3.3.3 [PE2] mpls [PE2-mpls] quit [PE2] mpls ldp [PE2-mpls-ldp] quit [PE2] interface vlanif 30 [PE2-Vlanif30] mpls [PE2-Vlanif30] mpls ldp [PE2-Vlanif30] quit

配置完成后，在PE1、P和PE2上执行display mpls ldp session命令可以看到PE1和P之间或PE2和P之间的对等体的Status项为“Operational”，即对等体关系已建立。执行display mpls lsp命令可以看到LSP的建立情况。以PE1的显示为例：
[PE1] display mpls ldp session LDP Session(s) in Public Network Codes: LAM(Label Advertisement Mode), SsnAge Unit(DDDD:HH:MM)
A '*' before a session means the session is being deleted.
------------------------------------------------------------------------------ PeerID Status LAM SsnRole SsnAge KASent/Rcv
------------------------------------------------------------------------------
2.2.2.2:0 Operational DU Passive 0000:15:29 3717/3717
------------------------------------------------------------------------------ TOTAL: 1 session(s) Found.
4. 在PE之间建立远端LDP会话。
\# 配置PE1。
[PE1] mpls ldp remote-peer 3.3.3.3 [PE1-mpls-ldp-remote-3.3.3.3] remote-ip 3.3.3.3 [PE1-mpls-ldp-remote-3.3.3.3] quit \# 配置PE2。
[PE2] mpls ldp remote-peer 1.1.1.1 [PE2-mpls-ldp-remote-1.1.1.1] remote-ip 1.1.1.1 [PE2-mpls-ldp-remote-1.1.1.1] quit配置完成后，在PE1或PE2上执行display mpls ldp session命令可以看到PE1和PE2之间的对等体的Status项为“Operational”，即远端对等体关系已建立。以PE1的显示为例：
[PE1] display mpls ldp session LDP Session(s) in Public Network Codes: LAM(Label Advertisement Mode), SsnAge Unit(DDDD:HH:MM)
A '*' before a session means the session is being deleted.
------------------------------------------------------------------------------ PeerID Status LAM SsnRole SsnAge KASent/Rcv
------------------------------------------------------------------------------
2.2.2.2:0 Operational DU Passive 0000:15:29 3717/3717
3.3.3.3:0 Operational DU Passive 0000:00:00 2/2
------------------------------------------------------------------------------ TOTAL: 2 session(s) Found.
5. 在PE上使能MPLS L2VPN。
\# 配置PE1。
[PE1] mpls l2vpn [PE1-l2vpn] quit \# 配置PE2。
[PE2] mpls l2vpn [PE2-l2vpn] quit
6. 在PE上配置VSI。
\# 配置PE1。
[PE1] vsi a2 static [PE1-vsi-a2] pwsignal ldp [PE1-vsi-a2-ldp] vsi-id 2 [PE1-vsi-a2-ldp] peer 3.3.3.3 [PE1-vsi-a2-ldp] quit [PE1-vsi-a2] quit \# 配置PE2。

[PE2] vsi a2 static [PE2-vsi-a2] pwsignal ldp [PE2-vsi-a2-ldp] vsi-id 2 [PE2-vsi-a2-ldp] peer 1.1.1.1 [PE2-vsi-a2-ldp] quit [PE2-vsi-a2] quit步骤2 使能CE设备的生成树计算功能。
\# 配置CE1。
[CE1] stp enable \# 配置CE2。
[CE2] stp enable步骤3 将PE1和PE2的接入侧的子接口绑定VSI并使能二层协议透明传输功能。
\# 配置PE1。
[PE1] vcmp role silent [PE1] interface 10ge 1/0/1 [PE1-10GE1/0/1] port link-type hybrid [PE1-10GE1/0/1] quit [PE1] interface 10ge 1/0/1.1 [PE1-10GE1/0/1.1] dot1q termination vid 10 [PE1-10GE1/0/1.1] l2 binding vsi a2 [PE1-10GE1/0/1.1] l2protocol-tunnel stp enable [PE1-10GE1/0/1.1] quit \# 配置PE2。
[PE2] vcmp role silent [PE2] interface 10ge 1/0/2 [PE2-10GE1/0/2] port link-type hybrid [PE2-10GE1/0/2] quit [PE2] interface 10ge 1/0/2.1 [PE2-10GE1/0/2.1] dot1q termination vid 10 [PE2-10GE1/0/2.1] l2 binding vsi a2 [PE2-10GE1/0/2.1] l2protocol-tunnel stp enable [PE2-10GE1/0/2.1] quit步骤4 配置PE替换接收到CE的STP协议报文的目的MAC地址。
\# 配置PE1 [PE1] l2protocol-tunnel stp group-mac 0100-0100-0100 \# 配置PE2 [PE2] l2protocol-tunnel stp group-mac 0100-0100-0100步骤5 配置CE2设备的优先级为4096。
[CE2] stp priority 4096步骤6 检查配置结果。
配置完成后，在PE上使用display group-mac命令可以查看透明\# l2protocol-tunnel传输的二层协议名称、协议类型、协议报文的组播目的MAC地址、Group MAC地址以及报文的优先级。
以PE1的显示为例。
[PE1] display l2protocol-tunnel group-mac stp Protocol EncapeType ProtocolType Protocol-MAC Group-MAC Pri
----------------------------------------------------------------------------- stp llc dsap 0x42 0180-c200-0000 0100-0100-0100 0 ssap 0x42

\# 等待30秒，在CE1和CE2设备上执行display stp命令可以检查MSTP的根。CE1和CE2之间完成了生成树计算功能。CE1上的10GE1/0/1为根（Root）端口，CE2上的10GE1/0/1为指定（Designated）端口。
[CE1] display stp brief MSTID Port Role STP State Protection 0 10GE1/0/1 ROOT FORWARDING NONE [CE2] display stp brief MSTID Port Role STP State Protection 0 10GE1/0/1 DESI FORWARDING NONE
----结束配置文件
● CE1的配置文件\# sysname CE1 \# vlan batch 10 \# stp enable \# interface Vlanif10 ip address 10.1.1.1 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# return
● CE2的配置文件\# sysname CE2 \# vlan batch 10 \# stp instance 0 priority 4096 stp enable \# interface Vlanif10 ip address 10.1.1.2 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# return
● PE1的配置文件\# sysname PE1 \# router id 1.1.1.1 \# vcmp role silent \# vlan batch 20 \# l2protocol-tunnel stp group-mac 0100-0100-0100 \# mpls lsr-id 1.1.1.1 mpls \# mpls l2vpn \#

vsi a2 static pwsignal ldp vsi-id 2 peer 3.3.3.3 \# mpls ldp \# mpls ldp remote-peer 3.3.3.3 remote-ip 3.3.3.3 \# interface Vlanif20 ip address 4.4.4.4 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid \# interface 10GE1/0/1.1 dot1q termination vid 10 l2 binding vsi a2 l2protocol-tunnel stp enable \# interface 10GE1/0/2 port link-type hybrid port hybrid pvid vlan 20 port hybrid tagged vlan 20 \# interface LoopBack1 ip address 1.1.1.1 255.255.255.255 \# ospf 1 area 0.0.0.0 network 1.1.1.1 0.0.0.0 network 4.4.4.0 0.0.0.255 \# return
● P的配置文件\# sysname P \# router id 2.2.2.2 \# vlan batch 20 30 \# mpls lsr-id 2.2.2.2 mpls \# mpls ldp \# interface Vlanif20 ip address 4.4.4.5 255.255.255.0 mpls mpls ldp \# interface Vlanif30 ip address 5.5.5.4 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 20 port hybrid tagged vlan 20 \# interface 10GE1/0/2 port link-type hybrid port hybrid pvid vlan 30 port hybrid tagged vlan 30

\# interface LoopBack1 ip address 2.2.2.2 255.255.255.255 \# ospf 1 area 0.0.0.0 network 2.2.2.2 0.0.0.0 network 4.4.4.0 0.0.0.255 network 5.5.5.0 0.0.0.255 \# return
● PE2的配置文件\# sysname PE2 \# router id 3.3.3.3 \# vcmp role silent \# vlan batch 30 \# l2protocol-tunnel stp group-mac 0100-0100-0100 \# mpls lsr-id 3.3.3.3 mpls \# mpls l2vpn \# vsi a2 static pwsignal ldp vsi-id 2 peer 1.1.1.1 \# mpls ldp \# mpls ldp remote-peer 1.1.1.1 remote-ip 1.1.1.1 \# interface Vlanif30 ip address 5.5.5.5 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 30 port hybrid tagged vlan 30 \# interface 10GE1/0/2 port link-type hybrid \# interface 10GE1/0/2.1 dot1q termination vid 10 l2 binding vsi a2 l2protocol-tunnel stp enable \# interface LoopBack1 ip address 3.3.3.3 255.255.255.255 \# ospf 1 area 0.0.0.0 network 3.3.3.3 0.0.0.0 network 5.5.5.0 0.0.0.255 \# return
