# S1700, S5700, S6700 V600R025C00 配置指南-以太网交换 01-10 ERPS配置

## 10 ERPS配置

### 10.1 ERPS简介

10.2 ERPS原理描述
10.3 ERPS配置注意事项
10.4 ERPS缺省配置
10.5 配置ERPSv1
10.6 配置ERPSv2
10.7 配置ERPS环定时器
10.8 配置ERPS环MEL值
10.9 配置ERPS多实例
10.10 配置ERPS over VPLS
10.11 配置ERPS接口与CFM联动
10.12 维护ERPS
10.13 ERPS配置举例
10.14 ERPS常见配置错误
10.1 ERPS 简介
定义
以太网环保护ERPS（Ethernet Ring Protection Switching），是ITU-T定义的一种二层
破环协议标准，标准号为ITU-T G.8032/Y1344，因此又称为G.8032。它定义了环自动
保护RAPS（Ring Auto Protection Switching）协议报文和保护倒换机制。
目的
以太网交换网络中为了进行链路备份，提高网络可靠性，通常会使用冗余链路（如环
形网络）。但是使用冗余链路会在网络中产生环路，可能会引起广播风暴以及MAC地

址表不稳定等现象，从而影响用户通信质量，甚至导致通信中断。为了解决环路问题，目前设备支持如表 设备支持的环网协议所示的环网协议：
表 10-1 设备支持的环网协议

| 环网协议 | 优点 | 局限性 |
|---|---|---|
| STP/RSTP/MSTP | ● 生成树协议适用于任何形式的二层网络。 ● 生成树协议是IEEE标准协议，可以实现与其他制造商设备的互通。 | 生成树协议收敛速度慢，且收敛速度受网络大小影响，无法满足收敛速度达到电信级可靠性要求。 |
| ERPS | ● 收敛速度快，满足电信级可靠性。 ● ERPS协议是ITU-T标准协议，可以实现与其他制造商设备的互通。 ● v2版本不仅支持单环组网，还支持相交环等多环组网方式。 | 需要预先规划好网络拓扑，配置相对复杂。 |

ERPS作为ITU-T发布的破环标准协议，解决了STP/RSTP/MSTP协议的缺陷，不仅具有收敛速度快，满足电信级可靠性和支持多种组网方式的优点，还具备良好的兼容性，可以实现与其他制造商设备的互通，因此ERPS协议被广泛的应用在二层环路组网中。

### 10.2 ERPS原理描述

#### 10.2.1 ERPS基本概念

ERPS是一个用于破除以太网链路层环路的协议。它以ERPS环为基本单位，通过阻塞环保护链路RPL（Ring Link） Owner端口，并控制其他普通端口，使得端口Protection的状态在Forwarding（转发）和Discarding（丢弃）之间切换，达到消除环路的目的。ERPS目前有ERPSv1和ERPSv2两个版本，ERPSv2完全兼容ERPSv1，并在ERPSv1的基础上进行了功能扩展，更好地发挥了ERPS的优势。
如图10-1所示，为了提高链路可靠性，DeviceA～DeviceD组成双归链路，接入上级网络，这样的接入方式将在整个网络中引入新的环路。为了消除网络中的冗余环路，有效地保证链路连通性，需要启动破除环路机制。

图 10-1 ERPS 单环示意图我们可以在如图10-1所示的网络中部署ERPS协议，下面结合该图介绍ERPS协议的基本概念：
ERPS 环ERPS环由一组配置了相同的控制VLAN且互连的二层交换设备（节点）构成，是ERPS协议的基本单位。ERPS环分为主环和子环。缺省情况下，ERPS环都是主环。主环是封闭的环，子环是非封闭的环，需要通过命令进行配置。如图10-2所示，DeviceA～DeviceD组成的ERPS环是主环，DeviceC～DeviceF组成的环是子环。子环的配置只有ERPSv2版本支持，ERPSv1版本不支持。
图 10-2 ERPS 主环和子环示意图

ERPS 端口ERPS协议中规定的端口主要有RPL owner端口、RPL neighbour端口和普通端口三种类型。其中RPL neighbour端口类型只有ERPSv2版本支持，ERPSv1版本不支持。
● RPL owner端口一个ERPS环只有一个RPL owner端口，由用户配置决定，通过阻塞RPL owner端口转发用户流量来防止ERPS环中产生环路。当RPL owner端口所在设备收到故障报文得知ERPS环上其他节点或链路故障时，会自动放开RPL owner端口，此端口恢复流量的接收和发送，保证流量不会中断。RPL owner端口所在的链路即为环保护链路RPL。
neighbour端口
● RPL RPL neighbour端口指的是与RPL owner端口直连的端口。引入RPL neighbour端口角色可以减少RPL neighbour端口所在设备刷新FDB表项的次数。正常情况下，RPL owner端口和RPL neighbour端口都会被阻塞，以防止环路产生，当ERPS环出现故障时，RPL owner端口和RPL neighbour端口都会被放开。
● 普通端口在ERPS环中，除RPL owner端口和RPL neighbour端口以外的端口都是普通端口，普通端口负责监测自己直连的 ERPS 协议的链路状态，并把链路状态的变化消息及时通知给其他端口。
ERPS协议的端口状态分为两种：
● Forwarding：在Forwarding状态下，端口既转发用户流量又接收/发送ERPS协议报文。
● Discarding：在Discarding状态下，端口不转发用户流量，但可以发送和接收ERPS协议报文。
VLAN ERPS中有两种类型的VLAN，数据VLAN和控制VLAN。数据VLAN用来传递数据报文；
控制VLAN用来传递ERPS协议报文，每个ERPS环必须配置控制VLAN。当端口加入已经配置控制VLAN的ERPS环后，端口将自动加入控制VLAN。不同ERPS环不能使用相同ID的控制VLAN。
保护实例对于运行ERPS协议的二层设备，传递ERPS协议报文和数据报文的VLAN必须映射到保护实例中，这样ERPS协议才会按照其阻塞原则对这些报文进行转发或阻塞，否则，VLAN 报文可能会在成环的网络中产生广播风暴导致网络不可用。
定时器ERPS协议中使用的定时器主要有Guard Timer定时器、WTR（Wait to Restore）
Timer定时器、Holdoff Timer定时器和WTB（Wait to Block）Timer定时器。其中WTB Timer定时器只有ERPSv2版本支持，ERPSv1版本不支持。
● Guard Timer链路故障或节点故障所涉及到的设备在故障恢复或执行清除操作后，向其他设备发送 NR （ No Request ） RAPS 报文，并同时启动 Guard Timer 定时器，在该定时器超时前不处理NR RAPS报文，目的是防止收到过期的NR RAPS报文。如果定时器超时后还能收到其他端口发送的NR RAPS报文，则本端口的转发状态变为Forwarding状态。

● WTR Timer
当设备或链路发生故障时，RPL owner端口会被放开，当故障恢复时，原故障端
口可能还未由Down状态变为Up状态。为了防止系统立即阻塞RPL owner端口而
引起网络震荡，当RPL owner端口收到某端口的NR RAPS报文后，系统会启动
WTR Timer定时器。如果在定时器超时前收到其他端口的SF（Signal Failed）
RAPS报文，则关闭WTR Timer定时器，不阻塞RPL owner端口。如果在WTR
Timer定时器超时前始终没有收到其他端口的SF RAPS报文，则当WTR Timer定时
器超时后，阻塞RPL owner端口，发送NRRB（No Request RPL Blocked） RAPS
报文。其他端口在收到该报文后，再将自己端口的转发状态设置为Forwarding状
态。
● Holdoff Timer
对于运行ERPS的二层网络，保护倒换的顺序可能会有不同的要求，例如，多层业
务的应用中，服务器出现故障后，用户可能会希望能有一段时间恢复服务器的故
障，而客户端感知不到，即不会立即进行保护倒换。这种情况下，可设置合适的
Holdoff Timer定时器，当发生故障时，故障并不会立即上报ERPS，而只有当
Holdoff Timer定时器超时后，如果故障仍未能恢复才会上报。
● WTB Timer
当清除端口的切换状态（强制切换或手工切换）时，启用 WTB Timer 定时器，因
为ERPS环内可能存在多个手工切换阻塞节点，只有当定时器超时后，清除操作才
起作用，这样可以防止立即阻塞RPL owner端口而引起阻塞点震荡。
WTB Timer定时器不支持配置，该定时器的值为Guard Timer定时器的值加5s，
缺省值为7s。
回切 / 非回切模式
当ERPS链路恢复正常后，可以通过设置ERPS的回切/非回切模式来决定是否重新阻塞
RPL owner端口。
● 在回切模式下，如果故障链路恢复，等待WTR时间后，会重新阻塞RPL owner端
口。阻塞链路会重新切回到RPL上。
● 在非回切模式下，如果故障链路恢复，不启动WTR Timer定时器，而且阻塞链路
还保持在原来的故障链路上，不会重新切回到RPL上。
缺省情况下，ERPS环处于回切模式。
ERPSv1版本只支持回切模式，ERPSv2版本两种模式都支持。
阻塞点切换方式
由于RPL owner端口所在链路可能拥有更高的带宽，此时可以考虑将带宽低的链路进
行阻塞，让用户流量回到RPL上进行传输。ERPS支持通过人为的配置来干预端口的阻
塞，包括强制切换FS（Forced Switch）和手工切换MS（Manual Switch）两种倒换方
式。
● 强制切换：配置了强制切换的端口会马上被阻塞，不管环上其他链路是否存在故
障等情况。
● 手工切换：对ERPS环上端口执行手工切换阻塞操作的流程和强制切换类似，区别
在于如果环的状态不是 Idle 或者 Pending 时，手工切换操作将不发挥作用。
除了强制切换和手工切换，ERPS还支持清除操作，该功能主要用于如下三种情况：
● 清除本地配置的手工切换和强制切换功能。

● 当ERPS环处于回切模式时，在WTB Timer定时器或WTR Timer定时器超时之前，
手工触发回切动作。
● 当ERPS环处于非回切模式时，手工触发回切动作。
阻塞点手工切换仅在ERPSv2版本上支持，ERPSv1版本不支持。
子环 RAPS 报文传输方式
ERPSv2版本除了支持单环组网，还支持相交环等多环组网方式。在相交环组网中，子
环RAPS报文传输方式分为虚通道VC（Virtual Channel）和非虚通道NVC（Non
Virtual Channel）两种方式。
虚通道方式：子环的RAPS协议报文会通过相交节点在主环内运行。即相交节点不
●
终结子环的协议报文。子环的阻塞端口会同时阻塞子环的RAPS协议报文和数据流
量。
● 非虚通道方式：子环的RAPS协议报文会在相交节点上终结，子环的阻塞端口仅阻
塞数据流量，不阻塞子环的RAPS协议报文。
如图 10-3 所示，一个主环分别和两个子环相交，其中左边子环的 RAPS 报文传输方式为
虚通道方式，右边子环的RAPS报文传输方式为非虚通道方式。
图 虚通道和非虚通道相交环示意图
10-3
缺省情况下，子环RAPS报文传输方式为非虚通道方式，除了如图10-4所示的特殊组网
场景（子环的链路是不连续的多个部分）下必须使用虚通道方式外，其他组网建议采
用缺省的非虚通道方式。如图 10-4 所示，链路 b 和链路 d 分别属于主环 1 和主环 2 ，只有
链路a和链路c属于子环，链路a和链路c是独立的两条链路，无法感知到对方的链路变
化，所以此时需要采用虚通道来传输RAPS报文。

图 10-4 虚通道特殊应用组网图虚通道和非虚通道两种子环RAPS报文传输方式的优缺点比较如表10-2所示。
表 10-2 虚通道和非虚通道方式优缺点比较

| 子环 RAPS报文传输方式 | 优点 | 缺点 |
|---|---|---|
| 虚通道 | 可应用于如图10-4所示的特殊组网中。 | 子网的RAPS通道受相连的网络拓扑影响，需要在RAPS通道所在网络为虚通道预留资源、分配控制VLAN ID等。 |
| 非虚通道 | 不需要相邻网络预留资源、分配控制VLAN ID等。 | 不能应用于如图10-4所示的特殊组网中。 |

ERPSv1 与 ERPSv2 ERPS目前有ERPSv1和ERPSv2两个版本，ERPSv1是ITU-T在2008年6月发布的版本，ERPSv2是ITU-T在2010年8月发布的版本。ERPSv2完全兼容ERPSv1，并在ERPSv1的基础上进行了功能扩展。ERPSv1和ERPSv2的区别如表10-3所示。

表 10-3 ERPSv1 和 ERPSv2 比较

| 功能 | ERPSv1 | ERPSv2 |
|---|---|---|
| 创建环 | 只支持创建单环，不支持配置子环。 | 支持创建多环，可以配置主环和子环。 |
| 配置端口角色 | 支持配置RPL owner和普通端口。 | 在支持配置RPL owner和普通端口基础上，还支持配置RPL neighbour端口。 |
| 配置网络拓扑变化通告 | 不支持该功能。 | 支持该功能。 |
| 子环传输R-APS报文采用虚通道或非虚通道 | 不支持该功能。 | 支持该功能。 |
| 回切\非回切模式 | 默认为回切模式，不支持配置，不支持非回切模式。 | 支持配置为回切模式或非回切模式。 |
| 手工切换阻塞点 | 不支持该功能。 | 支持该功能，且支持强制切换和手工切换。 |

说明由于ERPSv2完全兼容ERPSv1，所以如果当前ERPS环内所有设备同时支持ERPSv1和ERPSv2，建议配置ERPSv2。

#### 10.2.2 ERPS协议报文

ERPS协议的报文只有一种，即RAPS PDU报文。RAPS PDU报文包含ERPS环信息，在ERPS环上传递以实现各设备端口信息的互通。RAPS PDU报文基本格式如图10-5所示：
图 10-5 RAPS PDU 报文基本格式各字段含义如表10-4所示：

表 10-4 RAPS PDU 报文字段含义

| 字段名称 | 长度 | 说明 |
|---|---|---|
| MEL | 3位 | 标识维护实例等级。 |
| Version | 5位 | ● 0x00：v1版本。 ● 0x01：v2版本。 |
| OpCode | 8位 | 固定值0x28，标识该PDU是RAPS PDU。 |
| Flags | 8位 | 固定值0x00，该字段在接收的过程中会被忽略。 |
| TLV（type- length-value） Offset | 8位 | 固定值0x20，表示报文中的TLV从该字段之后偏移32个字节后开始。 |
| R-APS Specific Information | 32x8 位 | 该字段携带RAPS环信息，是RAPS PDU的核心字段。对于该字段，ERPSv1版本和ERPSv2版本在某些子字段上存在一定的差异。图10-6描述ERPSv1版本该字段具体包含的各子字段，图10-7描述ERPSv2版本该字段具体包含的各子字段。 |
| TLV | 无限制 | 描述报文中需要加载的信息，其中End TLV是固定值 0x00。 |

图 10-6 ERPSv1 版本 RAPS Specific Information 格式图 10-7 ERPSv2 版本 RAPS Specific Information 格式

RAPS Specific Information各子字段含义如表 RAPS Specific Information各子字段含义所示：
表 10-5 RAPS Specific Information 各子字段含义

| 字段名称 | 长度 | 说明 |
|---|---|---|
| Request/ State | 4位 | 标识该信息是请求信息或当前状态信息： ● 1101：FS（Forced Switch）RAPS ● 1110：Event报文 ● 1011：SF（Signal Failed）RAPS ● 0111：MS（Manual Switch）RAPS ● 0000：NR（No Request）RAPS ● 其他：保留字段 |
| Reserved 1 | 4位 | 对于ERPSv1，该字段是“Reserved 1”，表示保留字段，留作以后报文应答或是保护类型标识。对于ERPSv2，该字段是“Sub-code”： ● 当“Request/State”字段的取值为1110时，该字段为 0000表示FDB表项刷新请求。 ● 当“Request/State”字段取其他值时，该字段的取值为全0，为保留字段，且在接收过程中会被忽略。 |
| Sub-code |  |  |
| Status | 8位 | 标识状态信息： ● RB（RPL Blocked，1位）：RB=1标识RPL链路被阻塞；RB=0标识RPL链路解除阻塞。非RPL Owner设备在发送RPL PDU时将该字段置为0。 ● DNF（Do Not Flush，1位）：DNF=1标识收到当前信息不刷新FDB缓冲区；DNF=0标识收到当前信息可刷新FDB缓冲区。 ● BPR（Blocked Port Reference，1位）：阻塞端口标志位，该字段为0表示阻塞第一个端口，该字段为1表示阻塞第二个端口。只有ERPSv2版本支持该字段。 ● Status Reserved：保留字段。在发送过程中，此字段全置为0，且在接收的过程中会被忽略。该字段在 ERPSv1版本有6位，在ERPSv2版本有5位。 |
| Node ID | 6x8位 | 标识RAPS环节点设备的MAC地址，该字段属于提示信息，不影响RAPS环的保护切换操作。 |
| Reserved 2 | 24x8位 | 保留字段，在发送过程中，此字段全置为0，且在接收的过程中会被忽略。 |

#### 10.2.3 ERPS单环

ERPS是一种专用于以太网链路层的标准环网协议，以ERPS环为基本单位。在ERPS环中，为了防止出现环路，可以启动破除环路机制，阻塞RPL owner端口，消除环路。
当环网发生链路故障时，运行ERPS协议的设备可以迅速地放开阻塞端口，进行链路保护倒换，恢复环网上各节点间链路通信。ERPS单环是指在ERPS组网中只配置一个ERPS环。ERPSv1和ERPSv2均支持配置ERPS单环。
本节主要以示例的形式按照链路正常->链路故障->链路恢复的过程（包括保护倒换操作），介绍基本的单环组网下ERPS的实现原理。
链路正常如图 ERPS的单环组网图（链路正常）所示，由DeviceA～DeviceE组成的环路上各设备通信正常。
1. 为防止环路产生，ERPS首先会阻塞RPL owner端口，如果配置了RPL neighbour端口，该端口同样会被阻塞，其他端口可以正常转发业务流量。
2. ERPS环上的RPL owner端口以5s的时间间隔为周期向环中其他节点发送NRRB RAPS 报文，表示 ERPS 环当前链路一切正常。
图 的单环组网图（链路正常）
10-8 ERPS链路故障如图 ERPS的单环组网图（链路故障）所示，当DeviceD和DeviceE之间的链路发生故障时，ERPS协议启动保护倒换机制，将故障链路的两端端口阻塞，然后放开RPL

owner端口和RPL neighbour端口，这两个端口重新恢复用户流量的接收和发送，从而保证了流量不中断。具体处理过程如下：
1. DeviceD和DeviceE检测到链路故障，将故障链路上的端口阻塞，并刷新本设备的FDB表项。
2. DeviceD和DeviceE向外发送携带本地端口链路故障消息的SF RAPS报文，即一旦感知到链路故障，DeviceD和DeviceE会连续发送3个相同的SF RAPS报文，然后以5s的时间间隔持续稳定发送。
3. 其他设备收到DeviceD和DeviceE发送的SF RAPS报文后，会刷新本设备的FDB表项。当收到该RAPS报文后，DeviceC设备（RPL owner端口所在设备）会放开RPL owner端口，并刷新自己的FDB表项。同样，当DeviceB设备（RPL neighbour端口所在设备）收到RAPS报文后，会放开RPL neighbour端口，并刷新自己的FDB表项。
图 10-9 ERPS 的单环组网图（链路故障）
链路恢复链路恢复正常后，如果ERPS环配置的是回切模式，RPL owner端口所在设备会重新阻塞RPL链路上的流量，故障链路重新被用来完成用户流量的传送。如果ERPS环配置的是非回切模式，阻塞链路还保持在原来的故障链路上，不会重新切回到RPL上。以回切模式为例，具体恢复过程如下：
1. 当DeviceD和DeviceE之间的链路恢复后，DeviceD和DeviceE为了防止收到过期的NR RAPS协议报文，分别启动Guard Timer定时器，在该定时器超时前不接收其他NR RAPS协议报文。同时DeviceD和DeviceE会向外发送NR RAPS报文。

2. 当DeviceC（RPL owner端口所在设备）收到NR RAPS报文后，设备启动WTR
Timer定时器。当该定时器超时后，RPL owner端口被阻塞，同时向外发送NRRB
RAPS报文。
3. 当收到DeviceC发送的NRRB RAPS协议报文后，DeviceD和DeviceE将自己设备上
原来阻塞的端口放开，停止发送NR RAPS协议报文并且完成FDB表项的刷新。其
他设备收到DeviceC发送的NRRB RAPS协议报文后，也完成FDB表项的刷新。

#### 10.2.4 ERPS多环

ERPS多环是指在ERPS组网中配置多个ERPS环。ERPSv1只支持单环组网，ERPSv2不仅支持基本的单环组网，还支持多环组网方式。在ERPS多环组网中，既有主环也有子环。子环RAPS报文传输方式根据报文是否会进入主环分为虚通道传输和非虚通道传输。
本节主要以相交环组网，子环RAPS报文传输方式为非虚通道方式为例，按照链路正常- >链路故障->链路恢复的过程，介绍多环组网下ERPS的实现原理。
链路正常如图 ERPS 的多环组网图（链路正常）所示，由 DeviceA ～ DeviceE 组成的 ERPS 环为主环，DeviceB、DeviceC和DeviceF组成的ERPS环为子环1，DeviceC、DeviceD和DeviceG组成的ERPS环为子环2，各个环路都通信正常。
1. 为防止环路产生，ERPS的三个环分别阻塞自己的RPL owner端口。
2. 主环的RPL owner端口以5s的时间间隔为周期向主环其他节点发送NRRB RAPS报文。同样，子环1和子环2的RPL owner端口也以5s的时间间隔为周期向自己环中其他节点发送NRRB RAPS报文。主环的协议报文只在主环上传输，两个子环的报文会在相交节点终结，也不会进入主环。
PC1和上层网络之间的流量走向为PC1<->DeviceF<->DeviceB<->DeviceA<- >Router1，PC2和上层网络之间的流量走向为PC2<->DeviceG<->DeviceD<- >DeviceE<->Router2。

图 10-10 ERPS 的多环组网图（链路正常）
链路故障如图 ERPS的多环组网图（链路故障）所示，当DeviceD和DeviceG之间的链路发生故障时，ERPS协议启动保护倒换机制，将故障链路的两端端口阻塞，子环2会将RPL owner端口放开，重新恢复用户流量的接收和发送，PC1的用户流量不受影响，为了保证PC2的下行流量不中断，需要在相交节点DeviceC和DeviceD将子环2的拓扑变化信息通告到主环。最终 PC2 和上层网络之间的流量走向为 PC2<->DeviceG<->DeviceC<- >DeviceB<->DeviceA<->DeviceE<->Router2。具体处理过程如下：
1. DeviceD和DeviceG检测到链路故障，将故障链路上的端口阻塞，并刷新本设备的FDB表项。
2. DeviceG在子环2内部发送携带本地端口链路故障消息的SF RAPS报文，即一旦感知到链路故障，DeviceG连续发送3个相同的SF RAPS报文，然后以5s的时间间隔持续稳定发送SF RAPS报文。
3. DeviceG设备（RPL owner端口所在设备）放开RPL owner端口，并刷新自己的FDB表项。
4. 主环的相交节点DeviceC收到该SF RAPS报文后，刷新自己的FDB表项。而DeviceC和DeviceD在感知到这个网络拓扑变化后，在主环内发送Event报文，通告子环2的网络拓扑发生变化。

5. 其他主环节点收到Event报文后，会刷新自己的FDB表项。
图 10-11 ERPS 的多环组网图（链路故障）
链路恢复
链路恢复后，如果各个ERPS环配置的是回切模式，RPL owner端口所在设备会重新阻
塞RPL链路上的流量，故障链路重新被用来完成报文的传送。如果ERPS环配置的是非
回切模式，阻塞链路还保持在原来的故障链路上，不会重新切回到 RPL 上。以回切模式
为例，具体恢复过程如下：
1. 当DeviceD和DeviceG之间的链路恢复后，DeviceD和DeviceG为了防止收到过期
的RAPS协议报文，分别启动Guard Timer，在该定时器超时前不接收其他RAPS协
议报文。同时DeviceD和DeviceG会在子环2内部发送NR RAPS报文。
2. DeviceG（RPL owner端口所在设备）启动WTR Timer。当WTR Timer超时后，
DeviceG阻塞RPL owner端口，放开故障恢复链路的端口，同时向外发送NRRB
RAPS报文。
3. 当DeviceD收到DeviceG发送的NRRB RAPS报文后，将自己设备上原来阻塞的端口
放开，停止发送 NR RAPS 报文并且完成 FDB 表项的刷新。 DeviceC 收到 DeviceG 发
送的NRRB RAPS报文后，也完成FDB表项的刷新。
4. 相交节点DeviceC和DeviceD完成自身的FDB表项刷新以后，会在主环内发送Event
报文，通告子环2的拓扑变化情况。

5. 其他主环节点收到Event报文后，会刷新自己的FDB表项。
最终PC2的用户流量又会切换到如图10-10所示的走向。

#### 10.2.5 ERPS快速检测

ERPS快速检测是指在ERPS组网中配置快速检测模式以进行高性能保护倒换。ERPSv1不支持此模式，ERPSv2支持基本的单环组网和子环非虚通道场景部署此模式。
在ERPS快速检测模式下，单环场景RPL owner端口所在设备通过持续向组网发送双向检测报文以实现毫秒级的故障检测；多环场景则通过边缘节点设备向子环上设备发送检测报文。一旦设备链路发生故障，预期接收检测报文的端口收到硬件上报的中断以感知设备发生故障，进而快速实现保护倒换。
本节按照链路正常->链路故障->链路恢复的过程，介绍ERPS快速检测模式下实现快速检测的原理。
单环场景
● 链路正常如图 10-12 所示， DeviceA ~ DeviceD 四台设备组成 ERPS 环网，各设备均处于 IDLE状态。其中DeviceA（RPL owner端口所在设备）通过环上的两个ERPS成员口分别从两个方向（Direction_W、Direction_E）向外周期性发送检测报文，环上其他设备的两个ERPS成员口均能收到此报文并将此报文从相邻接口转发出去回到DeviceA。
图 10-12 ERPS 的单环组网图
● 链路故障当DeviceB上与DeviceC相连的端口发生故障时，在Direction_E方向上的DeviceA、DeviceB，在Direction_W方向上的DeviceC、DeviceD、DeviceA会分别收到超时事件，以快速使设备感知故障，此时DeviceA的RPL owner端口将被放开，并刷新MAC地址，恢复流量的接收和发送，保证流量不会中断。
● 链路恢复当DeviceB上与DeviceC相连的端口故障恢复时，所有设备上的检测报文正常接收，经过WTR Timer计时结束之后，配置RPL owner端口的DeviceA通过检测报文

触发回切事件，以快速使设备感知故障恢复，此时DeviceA的RPL owner的端口将被阻塞。
ERPS快速检测仅对设备的保护倒换性能有增益，不会对设备及端口本身的ERPS状态造成影响。
多环场景
● 链路正常如图10-13所示，DeviceA ~ DeviceD四台设备组成ERPS环网主环，DeviceC~DeviceF四台设备组成ERPS环网子环。
主、子环各设备均处于IDLE状态。其中DeviceC和DeviceD通过指定的ERPS子环边缘端口，分别从两个方向（Direction_W、Direction_E）向外周期性发送检测报文，环上其他设备的两个ERPS成员口均能收到此报文并将此报文从相邻接口转发出去，最终，Direction_E方向的报文由DeviceD的子环边缘端口接收并终结，Direction_W方向的报文由DeviceC的子环边缘端口接收并终结。
图 10-13 ERPS 的多环组网图
● 链路故障当DeviceD上与DeviceE相连的端口发生故障时，在Direction_E方向上的DeviceD，在Direction_W方向上的DeviceE、DeviceF、DeviceC会分别收到超时事件，以快速使设备感知故障，此时DeviceE的RPL owner端口和DeviceF的RPL Neighbour端口将被放开，并刷新MAC地址，恢复流量的接收和发送，保证流量不会中断。
● 链路恢复当DeviceD上与DeviceE相连的端口故障恢复时，所有设备上的检测报文正常接收，经过WTR Timer计时结束之后，配置RPL owner端口的DeviceE通过检测报文触发回切事件，以快速使设备感知故障恢复，此时 DeviceA 的 RPL owner 的端口将被阻塞。
ERPS快速检测仅对设备的保护倒换性能有增益，不会对设备及端口本身的ERPS状态造成影响。

### 10.3 ERPS配置注意事项

License 依赖ERPS无需License许可即可使用。
硬件依赖表 10-6 支持本特性的硬件

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
特性限制表 10-7 本特性的使用限制

| 特性 | 特性限制 |
|---|---|
| ERPS基础功能 | ERPS特性仅允许联动Outward型MEP场景，其他场景暂不支持，联动不生效。建议配置时保证联动的MEP是outward型。 |

| 特性 | 特性限制 |
|---|---|
| ERPS基础功能 | ERPS和VBST同时使能时，由于VBST动态分配实例VLAN映射关系，会导致ERPS功能不符合预期结果。 |
| ERPS基础功能 | 在集群/堆叠设备上配置ERPS，集群/堆叠拆分后，使用display erps verbose查询命令行回显的阻塞设备MAC有可能不正确。建议设备拆分后ERPS端口退出后再加入。 |
| ERPS基础功能 | ERPS环内设备间接入其他设备透传的场景下，如果设备和透传设备间的链路断开，透传设备的另一端无法感知到链路断开，导致设备不能正确发送报文，查询出来的阻塞设备MAC与实际不符合。 |
| ERPS公共配置与查询 | 控制VLAN的VLAN ID不能和BPDU Tunnel的VLAN ID相同。 |

### 10.4 ERPS缺省配置

表 10-8 ERPS 缺省值

| 参数 | 缺省值 |
|---|---|
| ERPS环 | 未创建 |
| Guard Timer定时器 | 200毫秒 |
| WTR Timer定时器 | 5分钟 |
| Holdoff Timer | 0百毫秒 |
| ERPS协议版本号 | ERPSv1 |

### 10.5 配置ERPSv1

#### 10.5.1 创建ERPS环

背景信息ERPS环是ERPS协议的基本单位，由一组配置了相同控制VLAN、数据VLAN且互连的二层交换设备构成。在配置逻辑上，需要先创建ERPS环，才能配置其他相关功能。
操作步骤步骤1 进入系统视图。
system-view步骤2 创建ERPS环并进入ERPS环视图。
erps ring ring-id

步骤3 （可选）开启ERPS协议报文的目的MAC封装环网ID功能。
encapsulate-ring-id enable缺省情况下，没有开启ERPS协议报文的目的MAC封装环网ID功能。
步骤4 （可选）配置描述信息。
description description缺省情况下，ERPS环的描述信息为ERPS环名称，例如Ring 1。
----结束

#### 10.5.2 配置控制VLAN

背景信息控制VLAN与数据VLAN相对。在ERPS环中，控制VLAN只用来传递ERPS协议报文，不用来转发用户业务报文，从而提高了ERPS协议的安全性。同一ERPS环中的所有设备必须配置相同的控制VLAN，不同ERPS环不能使用相同ID的控制VLAN。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入已经成功创建的ERPS环视图。
erps ring ring-id步骤3 配置ERPS环的控制VLAN。
control-vlan vlan-id说明
● 命令control-vlan可多次执行，以最后一次配置为准。
● 由参数vlan-id指定的控制VLAN必须是未被创建或使用过的VLAN。
● 如果ERPS环中已经有接口加入，那么将不能修改控制VLAN。若需要删除已配置的控制VLAN，必须在接口视图下执行命令undo erps ring或在ERPS环视图下执行命令undo port将接口退出ERPS环，然后再执行命令undo control-vlan删除控制VLAN。
● 控制VLAN成功创建后，配置文件会自动显示命令vlan batch vlan-id1 [ to vlan-id2 ] &<1-10>。
● 当接口加入已经配置控制VLAN的ERPS环后，接口将自动加入控制VLAN，而且如果接口类型是Trunk类型，则配置文件中，加入ERPS环的接口下会自动显示命令port trunk allow-pass vlan-id，如果接口类型是Hybrid类型，则配置文件中，加入ERPS环的接口下会自动显vlan示命令port hybrid tagged vlan vlan-id。
----结束

#### 10.5.3 配置保护实例并激活与VLAN的映射关系

背景信息对于运行ERPS协议的二层设备，传递ERPS协议报文和数据报文的VLAN必须映射到保护实例中，这样ERPS协议才会按照其阻塞原则对这些报文进行转发或阻塞。否则，VLAN报文可能会在成环的网络中产生广播风暴导致网络不可用。

操作步骤步骤1 进入系统视图。
system-view步骤2 进入ERPS环视图。
erps ring ring-id步骤3 创建ERPS环的保护实例protected-instance { all | { instance-id1 [ to instance-id2 ] } &<1-10> }缺省情况下，ERPS环上没有配置保护实例。
说明
● 如果已经在系统视图下使用stp mode命令设置STP工作模式为VBST，则protected- instance命令配置的保护实例必须为已创建的静态实例。
● 在同一ERPS环下多次执行protected-instance命令配置ERPS环的保护实例，结果按多次执行命令的累加生效。
● 如果已经有接口加入ERPS环，那么将不能修改保护实例。若需要删除已配置的保护实例，必须在接口视图下执行命令 undo erps ring 或在 ERPS 环视图下执行命令 undo port 将接口退出ERPS环，然后再执行命令undo protected-instance删除保护实例。
步骤4 退出ERPS环视图，进入系统视图。
quit步骤5 配置实例与VLAN的映射关系。
1. 进入MST域视图。
stp region-configuration
2. 配置保护实例与VLAN的映射关系。
instance instance-id vlan { vlan-id1 [ to vlan-id2 ] } &<1-10>缺省情况下，MST域内所有的VLAN都映射到实例0。
参数instance-id必须与protected-instance中指定的instance-id一致。
说明
– 不能将同一个VLAN映射到多个不同的实例上。如果将一个已经和实例建立映射关系的VLAN又映射到另一个实例上，原来的映射关系将被取消。
– 通过执行命令vlan-mapping modulo modulo可以配置多生成树实例和VLAN按照缺省算法自动分配映射关系，但是自动分配机制很难刚好满足实际的多生成树实例与VLAN的映射关系，因此不建议通过本命令进行配置。
– 当需要配置保护实例与MUX VLAN间的映射关系时，建议同一个MUX VLAN下的主VLAN、互通型和隔离型从VLAN配置在同一个保护实例下，否则可能导致环路。
----结束

#### 10.5.4 将二层端口加入ERPS环并配置端口角色

前提条件在配置将二层端口加入ERPS环并配置端口角色之前，需要完成以下任务：
● 如果是三层口的话，需要使用命令portswitch将三层口转换成二层口。

仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
● 加入ERPS环的二层接口去使能STP和Smart Link：
– 若接口已经使能STP功能，请在接口视图下执行命令stp disable，禁用STP功能。
– 若接口下已经使能Smart Link功能，请在Smart Link组视图下执行命令undo port，禁用Smart Link功能。
● 将端口加入ERPS环之前，需要分别执行命令control-vlan和protected-instance配置控制VLAN和保护实例。
背景信息ERPS创建后，将二层端口加入到ERPS环并配置一定的端口角色，ERPS才能正常工作。
将二层端口加入ERPS环并配置端口角色有两种方式：
● 在ERPS环视图下指定具体的端口和端口角色。
● 在具体的接口视图下将当前端口加入到相应的ERPS环并配置端口角色。
说明
● 由于ERPS端口既要允许控制VLAN中的报文通过，又要允许数据VLAN中的报文通过，所以应为Trunk类型或Hybrid类型。
● 当前不支持单独发送刷新MAC的报文，建议不要将RPL配置在两个上行节点之间的直连链路上。
● 修改端口角色前，需要先执行shutdown命令将端口关闭，完成端口角色修改后再执行undo shutdown命令将端口打开，否则会导致流量不通。
● 所有端口在加入ERPS段之前，必须已经去使能端口安全，否则会导致无法破环。
操作步骤步骤1 进入系统视图。
system-view步骤2 将二层端口加入ERPS环。
● 在ERPS环视图下指定端口和端口角色。
interface interface-type interface-number portswitch stp disable port link-type trunk port trunk allow-pass vlan { { vlan-id1 [ to vlan-id2 ] }&<1-10> | all } quit erps ring ring-id port interface-type interface-number [ rpl owner ]
● 在接口视图下将当前接口加入ERPS环并配置端口角色。
interface interface-type interface-number portswitch stp disable port link-type trunk port trunk allow-pass vlan { { vlan-id1 [ to vlan-id2 ] }&<1-10> | all } erps ring ring-id [ rpl owner ]
----结束

#### 10.5.5 （可选）配置ERPS环的自愈功能

背景信息ERPS环稳定时，如果非owner设备在没有故障时向外误发送ERPS的R-APS PDU报文中包含信号失效的SF字段，可能会导致环上的owner节点放开阻塞，形成环路。使能自愈功能后，设备会通过检测状态消除由于误发送造成的环路。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入已经成功创建的ERPS环视图。
erps ring ring-id步骤3 关闭ERPS环的自愈功能。
erps self-heal disable缺省情况下，该功能默认使能。
----结束

#### 10.5.6 检查ERPSv1的配置结果

操作步骤步骤1 执行命令display erps [ ring ring-id ] [ verbose ]，查看当前设备加入ERPS环的端口和环的信息。
步骤2 执行命令display erps interface interface-type interface-number [ ring ring-id ]，查看加入ERPS环的端口物理状态信息。
----结束

### 10.6 配置ERPSv2

#### 10.6.1 创建ERPS环

背景信息ERPS环是ERPS协议的基本单位，ERPS环由一组配置了相同控制VLAN、数据VLAN且互连的二层交换设备构成。在配置逻辑上，需要先创建ERPS环，才能配置其他相关功能。
如果用户希望利用单一设备集中管理和维护整个网络设备的环网配置，可以配置环网自部署功能，具体操作请参见：网络助手配置（WebMaster方案）-> 配置网络助手 ->（可选）配置环网自部署。仅ERPSv2支持该功能。
操作步骤步骤1 进入系统视图。

system-view步骤2 创建ERPS环并进入ERPS环视图。
erps ring ring-id缺省情况下，通过命令erps ring ring-id创建的ERPS环为主环。
步骤3 配置设备运行ERPS协议的版本号为v2。
version v2缺省情况下，设备运行的ERPS协议版本号为v1。
当需要将ERPS版本由v2变为v1时，需要清除ERPSv2版本支持但是ERPSv1版本不支持的相关配置。
步骤4 （可选）将ERPS环配置为子环。
sub-ring ERPS环创建后默认为主环。主环和子环的区别在于，主环是一个封闭的环，而子环不是。若当前ERPS环需要配置为主环，则不用执行此步骤。
必须保证没有接口加入需要配置为子环的ERPS环。如果有，必须先在接口视图下执行命令 undo erps ring 或在 ERPS 环视图下执行命令 undo port 将接口退出 ERPS 环。
步骤5 （可选）配置子环节点上RAPS报文的传输方式。
virtual-channel { enable | disable }缺省情况下，子环节点上RAPS报文的传输方式为非虚通道方式，建议使用缺省的传输方式即可。当子环的链路是不连续的多个部分时，需要采用虚通道传输方式。若当前ERPS环为主环，则不用执行此步骤。
说明如果需要使用虚通道，则需要在子环所有节点、子环跟主环相交节点上都配置虚通道传输方式。
步骤6 （可选）开启ERPS协议报文的目的MAC封装环网ID功能。
encapsulate-ring-id enable缺省情况下，没有开启ERPS协议报文的目的MAC封装环网ID功能。
步骤7 （可选）配置描述信息。
description description缺省情况下，ERPS环的描述信息为ERPS环名称，例如Ring 1。
---- 结束

#### 10.6.2 配置控制VLAN

背景信息控制VLAN与数据VLAN相对。在ERPS环中，控制VLAN只用来传递ERPS协议报文，不用来转发用户业务报文，从而提高了ERPS协议的安全性。同一ERPS环中的所有设备必须配置相同的控制VLAN，不同ERPS环不能使用相同ID的控制VLAN。
操作步骤步骤1 进入系统视图。
system-view

步骤2 进入已经成功创建的ERPS环视图。
erps ring ring-id步骤3 配置ERPS环的控制VLAN。
control-vlan vlan-id说明
● 命令control-vlan可多次执行，以最后一次配置为准。
● 由参数vlan-id指定的控制VLAN必须是未被创建或使用过的VLAN。
● 如果ERPS环中已经有接口加入，那么将不能修改控制VLAN。若需要删除已配置的控制VLAN，必须在接口视图下执行命令undo erps ring或在ERPS环视图下执行命令undo port将接口退出ERPS环，然后再执行命令undo control-vlan删除控制VLAN。
● 控制VLAN成功创建后，配置文件会自动显示命令vlan batch vlan-id1 [ to vlan-id2 ] &<1-10>。
● 当接口加入已经配置控制VLAN的ERPS环后，接口将自动加入控制VLAN，而且如果接口类型是Trunk类型，则配置文件中，加入ERPS环的接口下会自动显示命令port trunk allow-pass vlan vlan-id，如果接口类型是Hybrid类型，则配置文件中，加入ERPS环的接口下会自动显示命令port hybrid tagged vlan vlan-id。
---- 结束

#### 10.6.3 配置保护实例并激活与VLAN的映射关系

背景信息对于运行ERPS协议的二层设备，传递ERPS协议报文和数据报文的VLAN必须映射到保护实例中，这样ERPS协议才会按照其阻塞原则对这些报文进行转发或阻塞。否则，VLAN报文可能会在成环的网络中产生广播风暴导致网络不可用。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入ERPS环视图。
erps ring ring-id步骤3 创建ERPS环的保护实例protected-instance { all | { instance-id1 [ to instance-id2 ] } &<1-10> }缺省情况下，ERPS环上没有配置保护实例。
说明
● 如果已经在系统视图下使用stp mode命令设置STP工作模式为VBST，则protected- instance命令配置的保护实例必须为已创建的静态实例。
● 在同一ERPS环下多次执行protected-instance命令配置ERPS环的保护实例，结果按多次执行命令的累加生效。
● 如果已经有接口加入ERPS环，那么将不能修改保护实例。若需要删除已配置的保护实例，必须在接口视图下执行命令undo erps ring或在ERPS环视图下执行命令undo port将接口退出ERPS 环，然后再执行命令 undo protected-instance 删除保护实例。
步骤4 退出ERPS环视图，进入系统视图。
quit

步骤5 配置实例与VLAN的映射关系。
1. 进入MST域视图。
stp region-configuration
2. 配置保护实例与VLAN的映射关系。
instance instance-id vlan { vlan-id1 [ to vlan-id2 ] } &<1-10>缺省情况下，MST域内所有的VLAN都映射到实例0。
参数instance-id必须与protected-instance中指定的instance-id一致。
说明
– 不能将同一个VLAN映射到多个不同的实例上。如果将一个已经和实例建立映射关系的VLAN又映射到另一个实例上，原来的映射关系将被取消。
– 通过执行命令vlan-mapping modulo modulo可以配置多生成树实例和VLAN按照缺省算法自动分配映射关系，但是自动分配机制很难刚好满足实际的多生成树实例与VLAN的映射关系，因此不建议通过本命令进行配置。
– 当需要配置保护实例与MUX VLAN间的映射关系时，建议同一个MUX VLAN下的主VLAN、互通型和隔离型从VLAN配置在同一个保护实例下，否则可能导致环路。
---- 结束

#### 10.6.4 将二层端口加入ERPS环并配置端口角色

前提条件
● 如果是三层口的话，需要使用命令portswitch将三层口转换成二层口。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
● 加入ERPS环的二层接口下去使能STP和Smart Link：
– 若接口已经使能STP功能，请在接口视图下执行命令stp disable，去使能STP功能。
– 若接口下已经使能Smart Link功能，请在Smart Link组视图下执行命令undo port ，禁用Smart Link功能。
● 将端口加入ERPS环之前，需要分别使用命令control-vlan和protected-instance配置控制VLAN和保护实例。
背景信息ERPS创建后，将二层端口加入到ERPS环并配置一定的端口角色，ERPS才能正常工作。
将二层端口加入ERPS环有两种添加方式：
● 在ERPS环视图下指定具体的端口和端口角色。
● 在具体的接口视图下将当前端口加入到相应的ERPS环并配置端口角色。

说明
● 由于ERPS端口既要允许控制VLAN中的报文通过，又要允许数据VLAN中的报文通过，所以应为Trunk类型或Hybrid类型。
● 由于当前不支持单独发送刷新MAC的报文，建议不要将RPL配置在两个上行节点之间的直连链路上。
● 当需要修改端口角色时，需要先执行shutdown命令将端口关闭，完成端口角色修改后再执行undo shutdown命令将端口打开，否则会导致流量不通。
● 所有端口在加入ERPS段之前，必须已经去使能端口安全，否则会导致无法破环。
操作步骤步骤1 进入系统视图。
system-view步骤2 将二层端口加入ERPS环。
● 在ERPS环视图下指定端口和端口角色。
interface interface-type interface-number portswitch stp disable port link-type trunk port trunk allow-pass vlan { { vlan-id1 [ to vlan-id2 ] }&<1-10> | all } quit erps ring ring-id port interface-type interface-number [ rpl { owner | neighbour } ]
● 在接口视图下将当前接口加入ERPS环并配置端口角色。
interface interface-type interface-number portswitch stp disable port link-type trunk port trunk allow-pass vlan { { vlan-id1 [ to vlan-id2 ] }&<1-10> | all } erps ring ring-id [ rpl { owner | neighbour } ]
----结束

#### 10.6.5 配置网络拓扑变化通告

背景信息当本ERPS环的拓扑发生变化时，如没有及时通知上级二层网络，那么上级二层网络的MAC地址表就不会刷新，这样就会导致用户流量中断。为了保证用户流量正常通信，此时本 ERPS 环需要根据用户实际网络的拓扑变化情况，通知指定对象。
频繁的拓扑变化通告将导致CPU处理能力下降，且同时导致ERPS环上被频繁刷新Flush-FDB报文，占用带宽。为避免此类情况产生，需要对拓扑变化通告报文进行抑制。通过配置ERPS拓扑变化保护时间间隔可以实现抑制拓扑变化通告，还可以通过配置交换设备在拓扑变化保护时间间隔内处理拓扑变化报文的最大阈值，来避免频繁的删除MAC地址表项和ARP表项，从而达到保护设备的目的。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入已经成功创建的ERPS环视图。
erps ring ring-id

步骤3 配置本ERPS环向其他ERPS环通告网络拓扑变化。
tc-notify erps ring { ring-id1 [ to ring-id2 ] } &<1-10> ring-id1 [ to ring-id2 ]参数标识本ERPS环的网络拓扑变化需要通知的ERPS环的起始环ID和结束环ID，必须保证ring-id1和ring-id2指定的环存在，否则配置不生效。
当其他ERPS网络收到本ERPS环的拓扑变化消息后，会在本网络内发送Flush-FDB报文，通知本网络内的所有设备清除MAC地址，重新学习下游网络拓扑变化后的MAC地址，从而保证用户流量不中断。
步骤4 （可选）配置本ERPS环拓扑变化的保护时间间隔，抑制拓扑变化通告。
tc-protection interval interval-value步骤5 （可选）配置本ERPS环在拓扑变化保护时间间隔内处理拓扑变化报文的最大数量。
tc-protection threshold threshold-value这里的拓扑变化保护时间指的是通过命令tc-protection interval配置的拓扑变化保护时间间隔。
----结束

#### 10.6.6 （可选）配置ERPS环的保护倒换功能

背景信息ERPS环中节点设备或链路故障发生或恢复后，为了整个ERPS环的正常运行，需要配置回切机制、设置定时器或者切换阻塞点。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入已经成功创建的ERPS环视图。
erps ring ring-id步骤3 配置ERPS环的回切/非回切模式。
revertive { enable | disable }缺省情况下，ERPS环处于回切模式。
步骤4 退出ERPS环视图，进入系统视图。
quit步骤5 进入需要阻塞点人工切换的接口视图。
interface interface-type interface-number步骤6 配置本端口作为阻塞点的人工切换方式。
erps ring ring-id protect-switch { force | manual }通过ring ring-id参数指定的ERPS环ID必须是本端口加入的ERPS环。
如果需要取消阻塞点人工切换的配置，可以在ERPS环视图下执行clear命令将人工保护倒换的配置清除。
步骤 7 退出 ERPS 环视图，进入系统视图。
quit
----结束

#### 10.6.8 （可选）配置ERPS环的快速检测模式

#### 10.6.7 （可选）配置ERPS环的自愈功能

背景信息ERPS环稳定时，如果非owner设备在没有故障时向外误发送ERPS的R-APS PDU报文中包含信号失效的SF字段，可能会导致环上的owner节点放开阻塞，形成环路。使能自愈功能后，设备会通过检测状态消除由于误发送造成的环路。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入已经成功创建的ERPS环视图。
erps ring ring-id步骤3 关闭ERPS环的自愈功能。
erps self-heal disable缺省情况下，该功能默认使能。
----结束（可选）配置 环的快速检测模式
10.6.8 ERPS前提条件
● 加入ERPS环的二层端口下未开启生成树协议，若端口下已经开启生成树协议，请关闭生成树协议。
● 已经配置控制VLAN，具体操作见10.6.2 配置控制VLAN。
● 已经配置保护实例，具体操作见10.6.3 配置保护实例并激活与VLAN的映射关系。
● 配置revertive enable命令，将ERPS环设置为回切模式，缺省情况下，ERPS环已处于回切模式。
背景信息ERPS环创建后，可配置ERPS环为快速检测模式。配置快速检测模式后：
● 对于单环组网方式，ERPS RPL owner端口所在的设备节点将会发送链路探测报文，以快速检测链路的连通性。
● 对于多环场景组网方式，当在ERPS子环各节点配置快速检测模式后，需要指定快速检测模式ERPS子环的两个边缘端口，快速检测模式ERPS环的子环边缘端口将会发送链路探测报文，快速检测链路连通性。
配置了快速检测模式ERPS环的端口如果在一段时间内未接收到探测报文，将认为ERPS环路上发生了链路故障，会自动放开 RPL owner 端口、刷新 MAC 地址，恢复流量的接收和发送，保证流量不会中断。

说明
● 仅S5735I-S8T4SN-V2、S5735I-S8T4XN-V2、S5735I-S8U4XN-V2、S5735I-H8T4S2XN- V2、S5735I-H24U8S4XE-QA-V2、S5735I-S24T8S4XE-QA-V2、S5735I-S16T8S4XE-QD- V2、S5735I-S16T2S4XN-V2, S5735I-S8T8P2S4XN-V2、S5735I-H8T2XN-V2、S5735I- H8U2XN-V2、S5735I-S8U2XN-V2款型支持该配置。
● 只有在ERPS环的所有设备上都配置快速检测模式后，快速检测模式功能才会生效。
● 开启ERPS快速检测模式后，ERPS快速检测模式的发包设备将会持续发送探测报文，即使没有业务流量，也会占用ERPS端口一定的带宽。
● 单台设备最多配置一个ERPS环为快速检测模式。
● 快速检测模式不支持与第三方设备或老版本设备对接。
● 快速检测模式ERPS环上的所有端口必须为物理口。
● 快速检测模式不能与虚通道模式同时配置。
● 如果需要取消当前端口在指定ERPS环的边缘端口配置，需要先shutdown端口，否则可能会导致链路切换异常。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入已经成功创建的ERPS环视图。
erps ring ring-id步骤3 配置设备运行ERPS协议的版本号为v2。
version v2缺省情况下，设备运行的ERPS协议版本号为v1。
步骤4 开启ERPS快速检测模式。
fast-detection enable缺省情况下，ERPS环未开启快速检测模式。
步骤5 指定ERPS环为子环，单环场景则跳过此步。
sub-ring步骤6 退出ERPS环视图。
quit步骤 7 进入接口视图。
interface interface-type interface-number步骤8 将端口加入ERPS环。
erps ring ring-id步骤9 在主子环相交设备的子环端口上，指定端口为边缘端口，单环场景则跳过此步。
erps ring ringid edge-port缺省情况下，加入ERPS环的端口，未设置为边缘端口。
步骤 10 退出接口视图。
quit
----结束

#### 10.6.9 检查ERPSv2的配置结果

操作步骤步骤1 执行命令display erps [ ring ring-id ] [ verbose ]，查看当前设备加入ERPS环的端口和环的信息。
步骤2 执行命令display erps interface interface-type interface-number [ ring ring-id ]，查看加入ERPS环的端口物理状态信息。
----结束

### 10.7 配置ERPS环定时器

背景信息ERPS 环中节点设备或链路故障恢复后，为了防止出现网络震荡，会启用 ERPS 环定时器，帮助减少业务流量的中断时间。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入已经成功创建的ERPS环视图。
erps ring ring-id步骤3 配置ERPS环的WTR Timer定时器、Guard Timer定时器和Holdoff Timer定时器，根据网络实际情况和需要配置其中一种或多种。
表 10-9 配置 ERPS 环定时器

| 操作 | 命令 | 说明 |
|---|---|---|
| 配置ERPS环的WTR Timer 定时器 | wtr-timer time-value | 缺省情况下，ERPS环的 WTR Timer定时器为5分钟。 |
| 配置ERPS环的Guard Timer定时器 | guard-timer time-value | 缺省情况下，ERPS环的 Guard Timer定时器为200 厘秒。 |
| 配置ERPS环的Holdoff Timer定时器 | holdoff-timer time- value | 缺省情况下，ERPS环上的 Holdoff Timer定时器为0 百毫秒。 |

不同定时器的差异请参见定时器。
----结束

### 10.8 配置ERPS环MEL值

背景信息在运行ERPS协议的二层网络中，如果同时还配置了其他故障检测协议（比如CFM），ERPS环协议报文中的MEL字段可用于检测当前报文是否能通过。如果ERPS环中配置的MEL值比故障检测协议报文中的MEL值小，则该报文无法通过；反之，报文则能通过。MEL值除了用于检测当前报文是否能通过，还能用于与其他制造商设备互通，相同的MEL值更便于设备之间的通信顺畅。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入已经成功创建的ERPS环视图。
erps ring ring-id步骤3 配置ERPS环的MEL值。
raps-mel level-id缺省情况下，ERPS协议报文中MEL字段值为7。
----结束

### 10.9 配置ERPS多实例

#### 10.9.1 了解ERPS多实例

ERPS多实例是指在一个物理环路上配置多个逻辑的ERPS环路。在普通的ERPS组网中，一个物理环上只能配置一个ERPS环，也只能指定一个阻塞点。当ERPS环处于完整状态时，阻塞端口会阻止所有的用户报文通过，这导致所有用户报文在ERPS环上只能通过一条路径传输，阻塞端口另一侧的链路空闲，造成了带宽浪费。在配置ERPS多实例后，每个ERPS环上可以配置一个或多个保护实例，每个保护实例代表一个VLAN范围，各阻塞端口只对本ERPS环所保护的VLAN有效，不同VLAN的数据流量就可以通过不同的路径传输，从而实现流量的负载分担和链路备份，避免了带宽的浪费，提高了带宽的利用率。
如图 ERPS多实例组网图所示，可以在DeviceA、DeviceB、DeviceC、DeviceD和DeviceE组成的物理环路上配置ERPS Ring1和ERPS Ring2。ERPS Ring1的阻塞端口为Interface1，其保护实例对应的VLAN范围是VLAN100～VLAN200。ERPS Ring2的阻塞端口为Interface2，其保护实例对应的VLAN范围是VLAN300～VLAN400。完成相关配置后，数据VLAN100～VLAN200会按照数据流1所示的路线进行转发，数据VLAN300～VLAN400会按照数据流2所示的路线进行转发，从而实现了负载分担，提高了链路的利用率。

图 10-14 ERPS 多实例组网图

#### 10.9.2 创建ERPS环

背景信息ERPS环是ERPS协议的基本单位，由一组配置了相同控制VLAN、数据VLAN且互连的二层交换设备构成。在配置逻辑上，需要先创建ERPS环，才能配置其他相关功能。
操作步骤步骤1 进入系统视图。
system-view步骤2 创建ERPS环并进入ERPS环视图。
erps ring ring-id步骤3 （可选）开启ERPS协议报文的目的MAC封装环网ID功能。
encapsulate-ring-id enable缺省情况下，没有开启 协议报文的目的 封装环网 功能。
ERPS MAC ID步骤4 （可选）配置描述信息。
description description

#### 10.9.4 配置保护实例并激活与VLAN的映射关系

缺省情况下，ERPS环的描述信息为ERPS环名称，例如Ring 1。
----结束

#### 10.9.3 配置控制VLAN

背景信息控制VLAN与数据VLAN相对。在ERPS环中，控制VLAN只用来传递ERPS协议报文，不用来转发用户业务报文，从而提高了ERPS协议的安全性。同一ERPS环中的所有设备必须配置相同的控制VLAN，不同ERPS环不能使用相同ID的控制VLAN。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入已经成功创建的ERPS环视图。
erps ring ring-id步骤3 配置ERPS环的控制VLAN。
control-vlan vlan-id说明
● 命令control-vlan可多次执行，以最后一次配置为准。
由参数vlan-id指定的控制VLAN必须是未被创建或使用过的VLAN。
●
● 如果ERPS环中已经有接口加入，那么将不能修改控制VLAN。若需要删除已配置的控制VLAN，必须在接口视图下执行命令undo erps ring或在ERPS环视图下执行命令undo port将接口退出ERPS环，然后再执行命令undo control-vlan删除控制VLAN。
● 控制VLAN成功创建后，配置文件会自动显示命令vlan batch vlan-id1 [ to vlan-id2 ] &<1-10>。
● 当接口加入已经配置控制VLAN的ERPS环后，接口将自动加入控制VLAN，而且如果接口类型是Trunk类型，则配置文件中，加入ERPS环的接口下会自动显示命令port trunk allow-pass vlan vlan-id，如果接口类型是Hybrid类型，则配置文件中，加入ERPS环的接口下会自动显示命令port hybrid tagged vlan vlan-id。
----结束配置保护实例并激活与 的映射关系
10.9.4 VLAN背景信息对于运行ERPS协议的二层设备，传递ERPS协议报文和数据报文的VLAN必须映射到保护实例中，这样ERPS协议才会按照其阻塞原则对这些报文进行转发或阻塞。否则，VLAN报文可能会在成环的网络中产生广播风暴导致网络不可用。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入ERPS环视图。
erps ring ring-id

步骤3 创建ERPS环的保护实例protected-instance { all | { instance-id1 [ to instance-id2 ] } &<1-10> }缺省情况下，ERPS环上没有配置保护实例。
说明
● 如果已经在系统视图下使用stp mode命令设置STP工作模式为VBST，则protected- instance命令配置的保护实例必须为已创建的静态实例。
● 在同一ERPS环下多次执行protected-instance命令配置ERPS环的保护实例，结果按多次执行命令的累加生效。
● 如果已经有接口加入ERPS环，那么将不能修改保护实例。若需要删除已配置的保护实例，必须在接口视图下执行命令undo erps ring或在ERPS环视图下执行命令undo port将接口退出ERPS环，然后再执行命令undo protected-instance删除保护实例。
步骤4 退出ERPS环视图，进入系统视图。
quit步骤5 配置实例与VLAN的映射关系。
1. 进入MST域视图。
stp region-configuration
2. 配置保护实例与VLAN的映射关系。
instance instance-id vlan { vlan-id1 [ to vlan-id2 ] } &<1-10>缺省情况下，MST域内所有的VLAN都映射到实例0。
参数instance-id必须与protected-instance中指定的instance-id一致。
说明
– 不能将同一个VLAN映射到多个不同的实例上。如果将一个已经和实例建立映射关系的VLAN又映射到另一个实例上，原来的映射关系将被取消。
– 通过执行命令vlan-mapping modulo modulo可以配置多生成树实例和VLAN按照缺省算法自动分配映射关系，但是自动分配机制很难刚好满足实际的多生成树实例与VLAN的映射关系，因此不建议通过本命令进行配置。
– 当需要配置保护实例与MUX VLAN间的映射关系时，建议同一个MUX VLAN下的主VLAN、互通型和隔离型从VLAN配置在同一个保护实例下，否则可能导致环路。
----结束

#### 10.9.5 将二层端口加入ERPS环并配置端口角色

前提条件在配置将二层端口加入ERPS环并配置端口角色之前，需要完成以下任务：
● 如果是三层口的话，需要使用命令portswitch将三层口转换成二层口。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
● 加入ERPS环的二层接口去使能STP和Smart Link：
– 若接口已经使能 STP 功能，请在接口视图下执行命令 stp disable ，禁用 STP 功能。
– 若接口下已经使能Smart Link功能，请在Smart Link组视图下执行命令undo port，禁用Smart Link功能。

● 将端口加入ERPS环之前，需要分别执行命令control-vlan和protected-instance
配置控制VLAN和保护实例。
背景信息
ERPS创建后，将二层端口加入到ERPS环并配置一定的端口角色，ERPS才能正常工作。
将二层端口加入ERPS环并配置端口角色有两种方式：
● 在ERPS环视图下指定具体的端口和端口角色。
● 在具体的接口视图下将当前端口加入到相应的ERPS环并配置端口角色。
说明
● 由于ERPS端口既要允许控制VLAN中的报文通过，又要允许数据VLAN中的报文通过，所以应
为Trunk类型或Hybrid类型。
● 当前不支持单独发送刷新MAC的报文，建议不要将RPL配置在两个上行节点之间的直连链路
上。
修改端口角色前，需要先执行shutdown命令将端口关闭，完成端口角色修改后再执行undo
●
shutdown命令将端口打开，否则会导致流量不通。
● 所有端口在加入 ERPS 段之前，必须已经去使能端口安全，否则会导致无法破环。
操作步骤
步骤1 进入系统视图。
system-view
步骤2 将二层端口加入ERPS环。
● 在ERPS环视图下指定端口和端口角色。
interface interface-type interface-number
portswitch
stp disable
port link-type trunk
port trunk allow-pass vlan { { vlan-id1 [ to vlan-id2 ] }&<1-10> | all }
quit
erps ring ring-id
port interface-type interface-number [ rpl owner ]
● 在接口视图下将当前接口加入ERPS环并配置端口角色。
interface interface-type interface-number
portswitch
stp disable
port link-type trunk
port trunk allow-pass vlan { { vlan-id1 [ to vlan-id2 ] }&<1-10> | all }
erps ring ring-id [ rpl owner ]
----结束

#### 10.9.6 检查ERPS多实例的配置结果

操作步骤步骤1 执行命令display erps [ ring ring-id ] [ verbose ]，查看当前设备加入ERPS环的端口和环的信息。
步骤 2 执行命令 display erps interface interface-type interface-number [ ring ring-id ] ，查看加入ERPS环的端口物理状态信息。
----结束

#### 10.10.2 配置ERPS over VPLS

### 10.10 配置ERPS over VPLS

说明该配置仅S6780-H、S6750-H、S6750E-S、S6750-S、S6730E-H-V2、S6730-S-V2、S6730-H- V2、S5755-H、S5732-H-V2系列支持。

#### 10.10.1 了解ERPS over VPLS

当使能ERPS协议的接口存在子接口或设备上存在VLANIF接口，且该子接口或VLANIF接口绑定了VSI实例时，通常子接口或VLANIF接口并不能及时感知到主接口的拓扑变化，所以设备不能及时通告VPLS网络刷新MAC表项。为解决此问题，可在主接口上配置拓扑变化通告功能。
图10-15是CE接入PE的VPLS组网。组网中存在环路，且PE3会收到双份对端CE发送的流量。为解决此问题，可以在PE1-CE1-CE2-PE2之间的物理链路上使能ERPS，通过配置ERPS的RPL owner端口，使得CE2的interface2被阻断，这样CE1的流量便不会经过CE2 ，而会直接通过 PE1 传输给 PE3 ，从而不会出现双份流量或环路。
图10-15中ERPS环通过以太子接口或VLANIF接口接入VPLS网络，为了保证VPLS网络可以及时感知ERPS环的拓扑变化，需要在PE1和PE2接入ERPS环的主接口上使能拓扑变化通告功能。
图 10-15 配置 CE 接入的 ERPS over VPLS 示例组网图配置
10.10.2 ERPS over VPLS前提条件
● 在 PE 设备上运行路由协议，使 VPLS 骨干网络内的各设备能互通。
● 在VPLS骨干网络上配置MPLS基本能力，建立LDP LSP隧道。
● PE之间建立VPLS连接，并将VSI与相应的以太子接口或VLANIF接口绑定。

● CE和PE设备的接口已经加入ERPS环。
操作步骤
步骤1 进入系统视图。
system-view
步骤2 进入接口视图。
interface interface-type interface-number
步骤3 使能主接口的拓扑变化通告功能。
erps vpls-subinterface enable
缺省情况下，主接口在收到拓扑变化报文后不会通告其绑定了VSI的子接口及时刷新
MAC表项。
使能主接口的拓扑变化通告功能后，当主接口的转发状态是Discarding状态时，绑定了
VSI的子接口会变为Discarding状态，从而防止CE接入PE时，VPLS网络形成环路。
----结束

#### 10.10.3 检查配置结果

操作步骤
● 在接口视图下执行命令display this，查看是否使能主接口的拓扑变化通告功能。
----结束

### 10.11 配置ERPS接口与CFM联动

#### 10.11.1 了解ERPS与CFM联动

如果两个ERPS节点中间部署了传输设备，当传输设备故障时，ERPS节点无法快速感知甚至无法感知。因此在ERPS透传传输网络的情况下，无法实现快速收敛，甚至会造成用户流量中断。为了解决这一问题，可以在连接传输设备的ERPS节点上部署CFM检测功能，当发生设备或链路故障时，ERPS会及时通告网络中的其他设备，进行流量的快速切换。
说明该配置仅S6780-H、S6750-H、S6730-S-V2、S6750-S、S6750E-S、S6730-H-V2、S6730E-H- V2、S5755-H、S5755-S、S5732-H-V2系列支持。
说明当前ERPS特性仅支持联动Outward型MEP场景，其他场景暂不支持。
如图10-16所示，DeviceA、DeviceB和DeviceC组成了一个ERPS环，DeviceA和DeviceC通过三台中继传输设备相连。在DeviceA和DeviceC节点配置CFM功能，并在DeviceA的Interface1配置与Relay1的Interface1端口状态联动，在DeviceC的Interface1 配置与 Relay3 的 Interface1 端口状态联动。
正常情况下，ERPS环的RPL owner端口以5s的时间间隔为周期向外发送NR RAPS报文，表示当前ERPS环链路一切正常。

图 10-16 ERPS 透传传输网络链路正常组网图如图10-17所示，当中继传输设备Relay2存在故障时，DeviceA和DeviceC通过联动功能都会检测到CFM协议状态变为Down，联动接口Interface1通告ERPS，ERPS分别阻塞DeviceA和DeviceC的端口Interface1，然后DeviceA和DeviceC从与DeviceB相连的端口发送SF RAPS报文，并刷新本设备的FDB表项。DeviceB收到SF RAPS报文后，会放开RPL owner端口，并刷新自己的FDB表项。当Relay2设备恢复正常后，在回切模式下，会重新阻塞RPL owner端口，同时向外发送NRRB RAPS报文。DeviceA和DeviceC收到NRRB报文后，放开阻塞的端口Interface1，并刷新FDB表项，完成流量的回切。

图 10-17 ERPS 透传传输网络链路故障组网图

#### 10.11.2 配置ERPS接口与CFM联动

背景信息在加入ERPS环的接口上配置以太网CFM联动功能后，可以加速故障检测，实现拓扑的快速收敛和减少流量的中断时间。
说明该配置仅S6780-H、S6750-H、S6730-S-V2、S6750-S、S6750E-S、S6730-H-V2、S6730E-H- V2、S5755-H、S5755-S、S5732-H-V2系列支持。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入需要配置与CFM联动的接口视图。
interface interface-type interface-number步骤3 配置ERPS接口联动CFM功能。
erps ring ring-id track cfm md md-name ma ma-name mep mep-id remote-mep rmep-id只有当配置ERPS联动CFM功能的接口与mep mep-id命令配置的接口型MEP所在的接口是同一个接口时， ERPS 联动 CFM 功能才能生效。
步骤4 （可选）配置ERPS环的MEL值。
raps-mel level-id

缺省情况下，ERPS协议报文中MEL字段值为7。
----结束

#### 10.11.3 检查ERPS接口与CFM联动的配置结果

前提条件说明该配置仅S6780-H、S6750-H、S6730-S-V2、S6750-S、S6750E-S、S6730-H-V2、S6730E-H- V2、S5755-H、S5755-S、S5732-H-V2系列支持。
操作步骤步骤1 执行命令display erps interface interface-type interface-number [ ring ring-id ]，查看加入ERPS环的端口物理状态信息。
----结束

### 10.12 维护ERPS

背景信息通过reset命令可以将ERPS统计计数置0，便于重新统计。
须知清除ERPS的统计信息后，以前的信息将无法恢复，执行此操作前请务必仔细确认。
操作步骤步骤1 在用户视图下清除当前设备ERPS环的报文统计计数。
reset erps [ ring ring-id ] statistics
----结束

### 10.13 ERPS配置举例

#### 10.13.1 举例：配置ERPSv1功能

组网需求以太网交换网络中为了进行链路备份，提高网络可靠性，通常会使用冗余链路。但是使用冗余链路会在交换网络上产生环路，导致广播风暴以及 MAC 地址表不稳定等故障现象，从而导致用户通信质量较差，甚至通信中断。为了解决使用冗余链路引起的环路问题，可以在组成环网的设备上部署ERPS协议，ERPS协议是ITU-T定义的一种二层破环协议标准，且收敛速度快，可以满足收敛速度达到电信级可靠性要求。

如图 ERPS单环组网图所示，以部署ERPS的单环为例，DeviceA、DeviceB、DeviceC和DeviceD组成了一个ERPS单环。
图 10-18 ERPS 单环组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
配置思路采用如下的思路配置ERPS环：
1. 配置加入ERPS环的所有端口类型为Trunk型。
2. 创建ERPS环，并配置控制VLAN和保护实例。
3. 将二层端口加入 ERPS 环并配置端口角色。
4. 配置ERPS环的Guard Timer和WTR Timer定时器。
5. 配置DeviceA～DeviceD二层转发功能。
操作步骤步骤1 配置加入ERPS环的所有端口类型为Trunk型。
\# 配置DeviceA。DeviceB、DeviceC、DeviceD的配置与DeviceA类似，详见配置脚本。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch

[DeviceA-10GE1/0/1] port link-type trunk [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type trunk [DeviceA-10GE1/0/2] quit步骤2 创建ERPS环，并配置保护实例，配置ERPS环的控制VLAN ID为10，ERPS环1传递VLAN100～200的数据报文。
\# 配置DeviceA。DeviceB、DeviceC、DeviceD的配置与DeviceA类似，详见配置脚本。
[DeviceA] stp region-configuration [DeviceA-mst-region] instance 1 vlan 10 100 to 200 [DeviceA-mst-region] quit [DeviceA] erps ring 1 [DeviceA-erps-ring1] control-vlan 10 [DeviceA-erps-ring1] protected-instance 1 [DeviceA-erps-ring1] quit步骤3 将二层端口加入ERPS环并配置端口角色，将DeviceB的端口10GE1/0/1配置为RPL owner端口。
\# 配置 DeviceA 。 DeviceC 、 DeviceD 的配置与 DeviceA 类似，详见配置脚本。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] stp disable [DeviceA-10GE1/0/1] erps ring 1 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] stp disable [DeviceA-10GE1/0/2] erps ring 1 [DeviceA-10GE1/0/2] quit \# 配置DeviceB。
[DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] stp disable [DeviceB-10GE1/0/1] erps ring 1 rpl owner [DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] stp disable [DeviceB-10GE1/0/2] erps ring 1 [DeviceB-10GE1/0/2] quit步骤4 配置ERPS环的Guard Timer和WTR Timer定时器。
\# 配置DeviceA。DeviceB、DeviceC、DeviceD的配置与DeviceA类似，详见配置脚本。
[DeviceA] erps ring 1 [DeviceA-erps-ring1] wtr-timer 6 [DeviceA-erps-ring1] guard-timer 100 [DeviceA-erps-ring1] quit步骤5 配置DeviceA～DeviceD二层转发功能。
\# 配置DeviceA。DeviceB、DeviceC、DeviceD的配置与DeviceA相同，详见配置脚本。
[DeviceA] vlan batch 100 to 200 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] undo port trunk allow-pass vlan 1 [DeviceA-10GE1/0/1] port trunk allow-pass vlan 100 to 200 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] undo port trunk allow-pass vlan 1

[DeviceA-10GE1/0/2] port trunk allow-pass vlan 100 to 200 [DeviceA-10GE1/0/2] quit步骤6 验证配置结果\# 在网络稳定后，在设备上执行display erps，查看设备加入的ERPS环的端口和环的概要信息。以DeviceB为例。
[DeviceB] display erps D : Discarding F : Forwarding R : RPL Owner N : RPL Neighbour FS : Forced MS : Manual Switch Total number of rings configured = 1 Ring Control WTR Timer Guard Timer Port 1 Port 2 ID VLAN (min) (csec)
-------------------------------------------------------------------------------- 1 10 6 100 (D,R)10GE1/0/1 (F)10GE1/0/2
-------------------------------------------------------------------------------- \# 在设备上执行display erps verbose，查看设备加入的ERPS环的端口和环的详细信息。以DeviceB为例。
[DeviceB] display erps verbose Ring ID : 1 Description : Ring 1 Control Vlan : 10 Protected Instance : 1 Service Vlan : 100 to 200 WTR Timer Setting (min) : 6 Running (s) : 0 Guard Timer Setting (csec) : 100 Running (csec) : 0 Holdoff Timer Setting (deciseconds) : 0 Running (deciseconds) : 0 WTB Timer Running (csec) : 0 Ring State : Idle RAPS_MEL : 7 Revertive Mode : Revertive R-APS Channel Mode : - Version : 1 Sub-ring : No Forced Switch Port : - Manual Switch Port : - TC-Notify : - Time since last topology change : 0 days 4h:12m:20s Blocked device MAC address : 00e0-fcb5-ee02
-------------------------------------------------------------------------------- Port Port Role Port Status Signal Status
-------------------------------------------------------------------------------- 10GE1/0/1 RPL Owner Discarding Non-failed 10GE1/0/2 Common Forwarding Non-failed
----结束配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 10 100 to 200 //控制VLAN成功创建后，配置文件会自动显示vlan batch vlan-id \# stp region-configuration instance 1 vlan 10 100 to 200 \# erps ring 1 control-vlan 10 protected-instance 1

wtr-timer 6 guard-timer 100 \# interface 10ge 1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 \# interface 10ge 1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 \# return
● DeviceB \# sysname DeviceB \# vlan batch 10 100 to 200 \# stp region-configuration instance 1 vlan 10 100 to 200 \# erps ring 1 control-vlan 10 protected-instance 1 wtr-timer 6 guard-timer 100 \# interface 10ge 1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 rpl owner \# interface 10ge 1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 \# return
● DeviceC \# sysname DeviceC \# vlan batch 10 100 to 200 \# stp region-configuration instance 1 vlan 10 100 to 200 \# erps ring 1 control-vlan 10 protected-instance 1 wtr-timer 6 guard-timer 100 \# interface 10ge 1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable

erps ring 1 \# interface 10ge 1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 \# return
● DeviceD \# sysname DeviceD \# vlan batch 10 100 to 200 \# stp region-configuration instance 1 vlan 10 100 to 200 \# erps ring 1 control-vlan 10 protected-instance 1 wtr-timer 6 guard-timer 100 \# interface 10ge 1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 \# interface 10ge 1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 \# return

#### 10.13.2 举例：配置ERPSv2功能

组网需求以太网交换网络中为了进行链路备份，提高网络可靠性，通常会使用冗余链路。但是使用冗余链路会在交换网络上产生环路，导致广播风暴以及MAC地址表不稳定等故障现象，从而导致用户通信质量较差，甚至通信中断。为了解决使用冗余链路引起的环路问题，可以在组成环网的设备上部署ERPS协议，ERPS协议是ITU-T定义的一种二层破环协议标准，且收敛速度快，可以满足收敛速度达到电信级可靠性要求。ERPSv2功能不仅能解决环路问题，还支持多环组网、配置回切模式等功能，在能够提高网络可靠性的同时，还能适应更多组网场景。
如图 ERPS相交环组网图所示，以部署ERPS的相交环为例，DeviceA、DeviceB、DeviceC和 DeviceD组成的环为主环，DeviceA、LSW1、LSW2、LSW3和DeviceD组成的环为子环。
图 10-19 ERPS 相交环组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。

配置思路采用如下的思路配置ERPS环：
1. 配置加入ERPS环的所有端口类型为Trunk型。
2. 创建ERPS环，并配置控制VLAN和保护实例。
3. 配置ERPS协议版本，配置子环。
4. 将二层端口加入ERPS环并配置端口角色。
5. 配置网络拓扑变化通告和拓扑变化保护功能。
6. 配置ERPS环的Guard Timer和WTR Timer定时器。
7. 配置DeviceA～DeviceD、LSW1～LSW3二层转发功能。
操作步骤步骤1 配置加入ERPS环的所有端口类型为Trunk型。
\# 配置DeviceA。DeviceB、DeviceC、DeviceD、LSW1、LSW2和LSW3的配置与DeviceA 类似，详见配置脚本。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] interface 10ge 1/0/1

[DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type trunk [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type trunk [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] portswitch [DeviceA-10GE1/0/3] port link-type trunk [DeviceA-10GE1/0/3] quit步骤2 创建ERPS环1、ERPS环2并配置两个ERPS环的保护实例，配置ERPS环1的控制VLAN ID为10，ERPS环2的控制VLAN ID为20，ERPS环1、ERPS环2传递VLAN100～200的数据报文。
\# 配置DeviceA。DeviceB、DeviceC、DeviceD、LSW1、LSW2、LSW3的配置与DeviceA类似，详见配置脚本。
[DeviceA] stp region-configuration [DeviceA-mst-region] instance 1 vlan 10 20 100 to 200 [DeviceA-mst-region] quit [DeviceA] erps ring 1 [DeviceA-erps-ring1] control-vlan 10 [DeviceA-erps-ring1] protected-instance 1 [DeviceA-erps-ring1] quit [DeviceA] erps ring 2 [DeviceA-erps-ring2] control-vlan 20 [DeviceA-erps-ring2] protected-instance 1 [DeviceA-erps-ring2] quit步骤3 配置ERPS协议版本为v2，将ERPS环2配置为子环。
\# 配置DeviceA。DeviceB、DeviceC、DeviceD、LSW1、LSW2、LSW3的配置与DeviceA类似，详见配置脚本。
[DeviceA] erps ring 1 [DeviceA-erps-ring1] version v2 [DeviceA-erps-ring1] quit [DeviceA] erps ring 2 [DeviceA-erps-ring2] version v2 [DeviceA-erps-ring2] sub-ring [DeviceA-erps-ring2] quit步骤4 将二层端口加入ERPS环并配置端口角色，分别将DeviceB的端口10GE1/0/1和LSW3的端口10GE1/0/2配置为RPL owner端口。
\# 配置DeviceA。DeviceC、DeviceD、LSW1和LSW2的配置与DeviceA类似，详见配置脚本。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] stp disable [DeviceA-10GE1/0/1] erps ring 2 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] stp disable [DeviceA-10GE1/0/2] erps ring 1 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] stp disable [DeviceA-10GE1/0/3] erps ring 1 [DeviceA-10GE1/0/3] quit \# 配置 DeviceB 。 LSW3 的配置与 DeviceB 类似，详见配置脚本。
[DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] stp disable [DeviceB-10GE1/0/1] erps ring 1 rpl owner

[DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] stp disable [DeviceB-10GE1/0/2] erps ring 1 [DeviceB-10GE1/0/2] quit步骤5 在相交节点DeviceA和DeviceD配置网络拓扑变化通告，并配置拓扑变化保护。
\# 配置DeviceA。DeviceD的配置与DeviceA类似，详见配置脚本。
[DeviceA] erps ring 1 [DeviceA-erps-ring1] tc-protection interval 200 [DeviceA-erps-ring1] tc-protection threshold 60 [DeviceA-erps-ring1] quit [DeviceA] erps ring 2 [DeviceA-erps-ring2] tc-notify erps ring 1 [DeviceA-erps-ring2] quit步骤6 配置ERPS环的Guard Timer和WTR Timer定时器。
\# 配置DeviceA。DeviceB、DeviceC、DeviceD、LSW1、LSW2和LSW3的配置与DeviceA类似，详见配置脚本。
[DeviceA] erps ring 1 [DeviceA-erps-ring1] wtr-timer 6 [DeviceA-erps-ring1] guard-timer 100 [DeviceA-erps-ring1] quit [DeviceA] erps ring 2 [DeviceA-erps-ring2] wtr-timer 6 [DeviceA-erps-ring2] guard-timer 100 [DeviceA-erps-ring2] quit步骤7 配置DeviceA～DeviceD、LSW1～LSW3二层转发功能\# 配置DeviceA。DeviceB、DeviceC、DeviceD、LSW1、LSW2和LSW3的配置与DeviceA相同，详见配置脚本。
[DeviceA] vlan batch 100 to 200 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] undo port trunk allow-pass vlan 1 [DeviceA-10GE1/0/1] port trunk allow-pass vlan 100 to 200 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] undo port trunk allow-pass vlan 1 [DeviceA-10GE1/0/2] port trunk allow-pass vlan 100 to 200 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] undo port trunk allow-pass vlan 1 [DeviceA-10GE1/0/3] port trunk allow-pass vlan 100 to 200 [DeviceA-10GE1/0/3] quit步骤 8 验证配置结果\# 在网络稳定后，在设备上执行display erps，查看设备加入的ERPS环的端口和环的概要信息。以DeviceB为例。
[DeviceB] display erps D : Discarding F : Forwarding R : RPL Owner N : RPL Neighbour FS : Forced Device MS : Manual Device Total number of rings configured = 1 Ring Control WTR Timer Guard Timer Port 1 Port 2 ID VLAN (min) (csec)
-------------------------------------------------------------------------------- 1 10 6 100 (D,R)10GE1/0/1 (F)10GE1/0/2
--------------------------------------------------------------------------------

\# 在设备上执行display erps verbose，查看设备加入的ERPS环的端口和环的详细信息。
[DeviceB] display erps verbose Ring ID : 1 Description : Ring 1 Control Vlan : 10 Protected Instance : 1 Service Vlan : 100 to 200 WTR Timer Setting (min) : 6 Running (s) : 0 Guard Timer Setting (csec) : 100 Running (csec) : 0 Holdoff Timer Setting (deciseconds) : 0 Running (deciseconds) : 0 WTB Timer Running (csec) : 0 Ring State : Idle RAPS_MEL : 7 Revertive Mode : Revertive R-APS Channel Mode : - Version : 2 Sub-ring : No Forced Device Port : - Manual Device Port : - TC-Notify : - Time since last topology change : 0 days 4h:12m:20s Blocked device MAC address : 00e0-fcb5-ee02
-------------------------------------------------------------------------------- Port Port Role Port Status Signal Status
-------------------------------------------------------------------------------- 10GE1/0/1 RPL Owner Discarding Non-failed 10GE1/0/2 Common Forwarding Non-failed
----结束配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 10 20 100 to 200 //控制VLAN成功创建后，配置文件会自动显示vlan batch vlan-id \# stp region-configuration instance 1 vlan 10 20 100 to 200 \# erps ring 1 control-vlan 10 protected-instance 1 wtr-timer 6 guard-timer 100 version v2 tc-protection interval 200 tc-protection threshold 60 erps ring 2 control-vlan 20 protected-instance 1 wtr-timer 6 guard-timer 100 version v2 sub-ring tc-notify erps ring 1 \# interface 10ge 1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 20 100 to 200 stp disable erps ring 2 \# interface 10ge 1/0/2

port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 \# interface 10ge 1/0/3 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 \# return
● DeviceB \# sysname DeviceB \# vlan batch 10 100 to 200 \# stp region-configuration instance 1 vlan 10 100 to 200 \# erps ring 1 control-vlan 10 protected-instance 1 wtr-timer 6 guard-timer 100 version v2 \# interface 10ge 1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 rpl owner \# interface 10ge 1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 \# return
● DeviceC \# sysname DeviceC \# vlan batch 10 100 to 200 \# stp region-configuration instance 1 vlan 10 100 to 200 \# erps ring 1 control-vlan 10 protected-instance 1 wtr-timer 6 guard-timer 100 version v2 \# interface 10ge 1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 \#

interface 10ge 1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 \# return
● DeviceD \# sysname DeviceD \# vlan batch 10 20 100 to 200 \# stp region-configuration instance 1 vlan 10 20 100 to 200 \# erps ring 1 control-vlan 10 protected-instance 1 wtr-timer 6 guard-timer 100 version v2 tc-protection interval 200 tc-protection threshold 60 erps ring 2 control-vlan 20 protected-instance 1 wtr-timer 6 guard-timer 100 version v2 sub-ring tc-notify erps ring 1 \# interface 10ge 1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 20 100 to 200 stp disable erps ring 2 \# interface 10ge 1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 \# interface 10ge 1/0/3 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 \# return
● LSW1 \# sysname LSW1 \# vlan batch 20 100 to 200 \# stp region-configuration instance 1 vlan 20 100 to 200 \# erps ring 2 control-vlan 20 protected-instance 1

wtr-timer 6 guard-timer 100 version v2 sub-ring \# interface 10ge 1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 20 100 to 200 stp disable erps ring 2 \# interface 10ge 1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 20 100 to 200 stp disable erps ring 2 \# return
● LSW2 \# sysname LSW2 \# vlan batch 20 100 to 200 \# stp region-configuration instance 1 vlan 20 100 to 200 \# erps ring 2 control-vlan 20 protected-instance 1 wtr-timer 6 guard-timer 100 version v2 sub-ring \# interface 10ge 1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 20 100 to 200 stp disable erps ring 2 \# interface 10ge 1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 20 100 to 200 stp disable erps ring 2 \# return
● LSW3 \# sysname LSW3 \# vlan batch 20 100 to 200 \# stp region-configuration instance 1 vlan 20 100 to 200 \# erps ring 2 control-vlan 20 protected-instance 1 wtr-timer 6 guard-timer 100 version v2 sub-ring

\# interface 10ge 1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 20 100 to 200 stp disable erps ring 2 \# interface 10ge 1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 20 100 to 200 stp disable erps ring 2 rpl owner \# return

#### 10.13.3 举例：配置ERPSv2快速检测模式

组网需求以太网交换网络中为了进行链路备份，提高网络可靠性，通常会使用冗余链路。但是使用冗余链路会在交换网络上产生环路，导致广播风暴以及 MAC 地址表不稳定等故障现象，从而导致用户通信质量较差，甚至通信中断。为了解决使用冗余链路引起的环路问题，可以在组成环网的设备上部署ERPS协议，ERPS协议是ITU-T定义的一种二层破环协议标准，且收敛速度快，可以满足收敛速度达到电信级可靠性要求。
如图10-20所示，以部署ERPS的单环为例，DeviceA、DeviceB、DeviceC和DeviceD组成了一个ERPS单环。
说明仅S5735I-S8T4SN-V2、S5735I-S8T4XN-V2、S5735I-S8U4XN-V2、S5735I-H8T4S2XN-V2、S5735I-H24U8S4XE-QA-V2、S5735I-S24T8S4XE-QA-V2、S5735I-S16T8S4XE-QD-V2、S5735I-S16T2S4XN-V2, S5735I-S8T8P2S4XN-V2、S5735I-H8T2XN-V2、S5735I-H8U2XN- V2、S5735I-S8U2XN-V2款型支持该配置举例。
图 10-20 ERPS 单环组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。

配置思路采用如下的思路配置ERPS环：
1. 配置加入ERPS环的所有端口类型为Trunk型。
2. 配置DeviceA～DeviceD二层转发功能。
3. 创建ERPS环，使能ERPS快速检测模式，并配置控制VLAN和保护实例。
4. 将二层端口加入ERPS环并配置端口角色。
5. 配置ERPS环的Guard Timer和WTR Timer定时器。
操作步骤步骤1 配置加入ERPS环的所有端口类型为Trunk型。
\# 配置DeviceA。DeviceB、DeviceC、DeviceD的配置与DeviceA类似，详见配置脚本。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] port link-type trunk [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] port link-type trunk [DeviceA-10GE1/0/2] quit步骤 2 配置 DeviceA ～ DeviceD 二层转发功能。
\# 配置DeviceA。DeviceB、DeviceC、DeviceD的配置与DeviceA相同，详见配置脚本。

[DeviceA] vlan batch 100 to 200 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] undo port trunk allow-pass vlan 1 [DeviceA-10GE1/0/1] port trunk allow-pass vlan 100 to 200 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] undo port trunk allow-pass vlan 1 [DeviceA-10GE1/0/2] port trunk allow-pass vlan 100 to 200 [DeviceA-10GE1/0/2] quit步骤3 创建ERPS环，使能ERPS快速检测模式，并配置控制VLAN和保护实例。配置ERPS环的控制VLAN ID为10，ERPS环1传递VLAN100～200的数据报文。
\# 配置DeviceA。DeviceB、DeviceC、DeviceD的配置与DeviceA类似，详见配置脚本。
[DeviceA] erps ring 1 [DeviceA-erps-ring1] version v2 [DeviceA-erps-ring1] fast-detection enable [DeviceA-erps-ring1] control-vlan 10 [DeviceA-erps-ring1] protected-instance 1 [DeviceA-erps-ring1] quit [DeviceA] stp region-configuration [DeviceA-mst-region] instance 1 vlan 10 100 to 200 [DeviceA-mst-region] quit步骤4 将二层端口加入ERPS环并配置端口角色，将DeviceB的端口10GE1/0/1配置为RPL owner端口。
\# 配置DeviceA。DeviceC、DeviceD配置与DeviceA类似，详见配置脚本。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] stp disable [DeviceA-10GE1/0/1] erps ring 1 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] stp disable [DeviceA-10GE1/0/2] erps ring 1 [DeviceA-10GE1/0/2] quit \# 配置DeviceB。
[DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] stp disable [DeviceB-10GE1/0/1] erps ring 1 rpl owner [DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] stp disable [DeviceB-10GE1/0/2] erps ring 1 [DeviceB-10GE1/0/2] quit步骤5 配置ERPS环的Guard Timer和WTR Timer定时器。
\# 配置DeviceA。DeviceB、DeviceC、DeviceD配置与DeviceA类似，详见配置脚本。
[DeviceA] erps ring 1 [DeviceA-erps-ring1] wtr-timer 6 [DeviceA-erps-ring1] guard-timer 100 [DeviceA-erps-ring1] quit步骤6 验证配置结果\# 在网络稳定后，在设备上执行display erps，查看设备加入的ERPS环的端口和环的概要信息。以 DeviceA 为例。
[DeviceA] display erps D : Discarding F : Forwarding

R : RPL Owner N : RPL Neighbour FS : Forced Device MS : Manual Device Total number of rings configured = 1 Ring Control WTR Timer Guard Timer Port 1 Port 2 ID VLAN (min) (csec)
-------------------------------------------------------------------------------- 1 10 6 100 (D,R)10GE1/0/1 (F)10GE1/0/2
-------------------------------------------------------------------------------- \# 在设备上执行display erps verbose，查看设备加入的ERPS环的端口和环的详细信息。以DeviceB为例。
[DeviceB] display erps verbose Ring ID : 1 Description : Ring 1 Control Vlan : 10 Protected Instance : 1 Service Vlan : 100 to 200 WTR Timer Setting (min) : 6 Running (s) : 0 Guard Timer Setting (csec) : 100 Running (csec) : 0 Holdoff Timer Setting (deciseconds) : 0 Running (deciseconds) : 0 WTB Timer Running (csec) : 0 Ring State : Protection RAPS_MEL : 7 Revertive Mode : Revertive R-APS Channel Mode : - Version : 2 Sub-ring : No Fast-Detection : Yes Forced Device Port : - Manual Device Port : - TC-Notify : - Time since last topology change : 0 days 4h:12m:20s Blocked device MAC address : 00e0-fcb5-ee02
-------------------------------------------------------------------------------- Port Port Role Port Status Signal Status
-------------------------------------------------------------------------------- 10GE1/0/1 RPL Owner Discarding Non-failed 10GE1/0/2 Common Forwarding Non-failed
----结束配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 10 100 to 200 //控制VLAN成功创建后，配置文件会自动显示vlan batch vlan-id \# stp region-configuration instance 1 vlan 10 100 to 200 \# erps ring 1 control-vlan 10 protected-instance 1 version v2 fast-detection enable wtr-timer 6 guard-timer 100 \# interface 10ge 1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable

erps ring 1 \# interface 10ge 1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 \# return
● DeviceB \# sysname DeviceB \# vlan batch 10 100 to 200 \# stp region-configuration instance 1 vlan 10 100 to 200 \# erps ring 1 control-vlan 10 protected-instance 1 version v2 fast-detection enable wtr-timer 6 guard-timer 100 \# interface 10ge 1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 rpl owner \# interface 10ge 1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 \# return
● DeviceC \# sysname DeviceC \# vlan batch 10 100 to 200 \# stp region-configuration instance 1 vlan 10 100 to 200 \# erps ring 1 control-vlan 10 protected-instance 1 version v2 fast-detection enable wtr-timer 6 guard-timer 100 \# interface 10ge 1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 \# interface 10ge 1/0/2 port link-type trunk

undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 \# return
● DeviceD \# sysname DeviceD \# vlan batch 10 100 to 200 \# stp region-configuration instance 1 vlan 10 100 to 200 \# erps ring 1 control-vlan 10 protected-instance 1 version v2 fast-detection enable wtr-timer 6 guard-timer 100 \# interface 10ge 1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 \# interface 10ge 1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 to 200 stp disable erps ring 1 \# return

#### 10.13.4 举例：配置ERPS多实例

组网需求在ERPS组网中，一个物理环上只能配置一个ERPS环，也只能指定一个阻塞点。当ERPS环处于完整状态时，阻塞端口会阻止所有的用户报文通过，这导致所有用户报文在ERPS环上只能通过一条路径传输，阻塞端口另一侧的链路空闲，造成了带宽浪费。
如图 ERPS 单环多实例组网图所示，在 DeviceA ～ DeviceD 上配置两个 ERPS 实例， ERPS环1和ERPS环2，ERPS环1阻塞DeviceB的P1端口，ERPS环2阻塞DeviceA的P2端口，实现负载分担并提供链路备份。
图 10-21 ERPS 单环多实例组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。

配置思路采用如下的思路配置ERPS单环多实例：
1. 配置加入ERPS环的所有端口类型为Trunk型。
2. 创建ERPS环，并配置控制VLAN和保护实例。
3. 将二层端口加入ERPS环并配置端口角色。
4. 配置ERPS环的Guard Timer和WTR Timer定时器。
5. 配置DeviceA～DeviceD二层转发功能。
操作步骤步骤1 配置加入ERPS环的所有端口类型为Trunk型。

\# 配置DeviceA。DeviceB、DeviceC、DeviceD的配置与DeviceA类似，详见配置脚本。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type trunk [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type trunk [DeviceA-10GE1/0/2] quit步骤2 创建ERPS环1、ERPS环2并配置两个ERPS环的保护实例，配置ERPS环1的控制VLAN ID为10，ERPS环2的控制VLAN ID为20，ERPS环1传递VLAN100～VLAN200的数据报文，ERPS环2传递VLAN300～VLAN400的数据报文。
\# 配置DeviceA。DeviceB、DeviceC、DeviceD的配置与DeviceA类似，详见配置脚本。
[DeviceA] erps ring 1 [DeviceA-erps-ring1] control-vlan 10 [DeviceA-erps-ring1] protected-instance 1 [DeviceA-erps-ring1] quit [DeviceA] stp region-configuration [DeviceA-mst-region] instance 1 vlan 10 100 to 200 [DeviceA-mst-region] quit [DeviceA] erps ring 2 [DeviceA-erps-ring2] control-vlan 20 [DeviceA-erps-ring2] protected-instance 2 [DeviceA-erps-ring2] quit [DeviceA] stp region-configuration [DeviceA-mst-region] instance 2 vlan 20 300 to 400 [DeviceA-mst-region] quit步骤3 将二层端口加入ERPS环并配置端口角色，分别将DeviceA的端口10GE1/0/1和DeviceB的端口10GE1/0/2配置为RPL owner。
\# 配置DeviceA。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] stp disable [DeviceA-10GE1/0/1] erps ring 1 [DeviceA-10GE1/0/1] erps ring 2 rpl owner [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] stp disable [DeviceA-10GE1/0/2] erps ring 1 [DeviceA-10GE1/0/2] erps ring 2 [DeviceA-10GE1/0/2] quit \# 配置DeviceB。
[DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] stp disable [DeviceB-10GE1/0/1] erps ring 1 [DeviceB-10GE1/0/1] erps ring 2 [DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] stp disable [DeviceB-10GE1/0/2] erps ring 1 rpl owner [DeviceB-10GE1/0/2] erps ring 2 [DeviceB-10GE1/0/2] quit \# 配置DeviceC。DeviceD的配置与DeviceC类似，详见配置脚本。
[DeviceC] interface 10ge 1/0/1 [DeviceC-10GE1/0/1] stp disable

[DeviceC-10GE1/0/1] erps ring 1 [DeviceC-10GE1/0/1] erps ring 2 [DeviceC-10GE1/0/1] quit [DeviceC] interface 10ge 1/0/2 [DeviceC-10GE1/0/2] stp disable [DeviceC-10GE1/0/2] erps ring 1 [DeviceC-10GE1/0/2] erps ring 2 [DeviceC-10GE1/0/2] quit步骤4 配置ERPS环的Guard Timer和WTR Timer定时器。
\# 配置DeviceA。DeviceB、DeviceC、DeviceD的配置与DeviceA类似，详见配置脚本。
[DeviceA] erps ring 1 [DeviceA-erps-ring1] wtr-timer 6 [DeviceA-erps-ring1] guard-timer 100 [DeviceA-erps-ring1] quit [DeviceA] erps ring 2 [DeviceA-erps-ring2] wtr-timer 6 [DeviceA-erps-ring2] guard-timer 100 [DeviceA-erps-ring2] quit步骤5 配置DeviceA～DeviceD二层转发功能。
\# 配置DeviceA。DeviceB、DeviceC、DeviceD的配置与DeviceA类似，详见配置脚本。
[DeviceA] vlan batch 100 to 200 300 to 400 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] undo port trunk allow-pass vlan 1 [DeviceA-10GE1/0/1] port trunk allow-pass vlan 100 to 200 300 to 400 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] undo port trunk allow-pass vlan 1 [DeviceA-10GE1/0/2] port trunk allow-pass vlan 100 to 200 300 to 400 [DeviceA-10GE1/0/2] quit步骤6 验证配置结果\# 在网络稳定后，在设备上执行display erps，查看设备加入的ERPS环的端口和环的概要信息。以DeviceB为例。
[DeviceB] display erps D : Discarding F : Forwarding R : RPL Owner N : RPL Neighbour FS : Forced Device MS : Manual Device Total number of rings configured = 2 Ring Control WTR Timer Guard Timer Port 1 Port 2 ID VLAN (min) (csec)
-------------------------------------------------------------------------------- 1 10 6 100 (F)10GE1/0/1 (D,R)10GE1/0/2 2 20 6 100 (F)10GE1/0/1 (F)10GE1/0/2
-------------------------------------------------------------------------------- \# 在设备上执行display erps verbose，查看设备加入的ERPS环的端口和环的详细信息。以DeviceB为例。
[DeviceB] display erps verbose Ring ID : 1 Description : Ring 1 Control Vlan : 10 Protected Instance : 1 Service Vlan : 100 to 200 WTR Timer Setting (min) : 6 Running (s) : 0

Guard Timer Setting (csec) : 100 Running (csec) : 0 Holdoff Timer Setting (deciseconds) : 0 Running (deciseconds) : 0 WTB Timer Running (csec) : 0 Ring State : Idle RAPS_MEL : 7 Revertive Mode : Revertive R-APS Channel Mode : - Version : 1 Sub-ring : No Forced Device Port : - Manual Device Port : - TC-Notify : - Time since last topology change : 0 days 0h:35m:5s Blocked device MAC address : 00e0-fcb5-ee02
-------------------------------------------------------------------------------- Port Port Role Port Status Signal Status
-------------------------------------------------------------------------------- 10GE1/0/1 Common Forwarding Non-failed 10GE1/0/2 RPL Owner Discarding Non-failed Ring ID : 2 Description : Ring 2 Control Vlan : 20 Protected Instance : 2 Service Vlan : 300 to 400 WTR Timer Setting (min) : 6 Running (s) : 0 Guard Timer Setting (csec) : 100 Running (csec) : 0 Holdoff Timer Setting (deciseconds) : 0 Running (deciseconds) : 0 WTB Timer Running (csec) : 0 Ring State : Idle RAPS_MEL : 7 Revertive Mode : Revertive R-APS Channel Mode : - Version : 1 Sub-ring : No Forced Device Port : - Manual Device Port : - TC-Notify : - Time since last topology change : 0 days 0h:35m:30s Blocked device MAC address : 00e0-fcb5-ee01
-------------------------------------------------------------------------------- Port Port Role Port Status Signal Status
-------------------------------------------------------------------------------- 10GE1/0/1 Common Forwarding Non-failed 10GE1/0/2 Common Forwarding Non-failed
----结束配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 10 20 100 to 200 300 to 400 //控制VLAN成功创建后，配置文件会自动显示vlan batch vlan- \# stp region-configuration instance 1 vlan 10 100 to 200 instance 2 vlan 20 300 to 400 \# erps ring 1 control-vlan 10 protected-instance 1 wtr-timer 6 guard-timer 100 erps ring 2 control-vlan 20

protected-instance 2 wtr-timer 6 guard-timer 100 \# interface 10ge 1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 20 100 to 200 300 to 400 stp disable erps ring 1 erps ring 2 rpl owner \# interface 10ge 1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 20 100 to 200 300 to 400 stp disable erps ring 1 erps ring 2 \# return
● DeviceB \# sysname DeviceB \# vlan batch 10 20 100 to 200 300 to 400 \# stp region-configuration instance 1 vlan 10 100 to 200 instance 2 vlan 20 300 to 400 \# erps ring 1 control-vlan 10 protected-instance 1 wtr-timer 6 guard-timer 100 erps ring 2 control-vlan 20 protected-instance 2 wtr-timer 6 guard-timer 100 \# interface 10ge 1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 20 100 to 200 300 to 400 stp disable erps ring 1 erps ring 2 \# interface 10ge 1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 20 100 to 200 300 to 400 stp disable erps ring 1 rpl owner erps ring 2 \# return
● DeviceC \# sysname DeviceC \# vlan batch 10 20 100 to 200 300 to 400 \# stp region-configuration instance 1 vlan 10 100 to 200 instance 2 vlan 20 300 to 400

\# erps ring 1 control-vlan 10 protected-instance 1 wtr-timer 6 guard-timer 100 erps ring 2 control-vlan 20 protected-instance 2 wtr-timer 6 guard-timer 100 \# interface 10ge 1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 20 100 to 200 300 to 400 stp disable erps ring 1 erps ring 2 \# interface 10ge 1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 20 100 to 200 300 to 400 stp disable erps ring 1 erps ring 2 \# return
● DeviceD \# sysname DeviceD \# vlan batch 10 20 100 to 200 300 to 400 \# stp region-configuration instance 1 vlan 10 100 to 200 instance 2 vlan 20 300 to 400 \# erps ring 1 control-vlan 10 protected-instance 1 wtr-timer 6 guard-timer 100 erps ring 2 control-vlan 20 protected-instance 2 wtr-timer 6 guard-timer 100 \# interface 10ge 1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 20 100 to 200 300 to 400 stp disable erps ring 1 erps ring 2 \# interface 10ge 1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 20 100 to 200 300 to 400 stp disable erps ring 1 erps ring 2 \# return

#### 10.13.5 举例：配置CE接入的ERPS over VPLS（采用以太网子接口接入）

组网需求图10-22是CE接入PE的VPLS组网。但是该组网却存在一个问题，就是PE3会收到双份对端CE发送的流量。为解决此问题，可以在PE1-CE1-CE2-PE2之间的物理链路上使能ERPS，通过配置ERPS的RPL owner端口，使得CE2的interface2被阻断。这样，CE1的流量便不会经过CE2，而是直接通过PE1传输给PE3，从而避免双份流量或环路。
图 10-22 配置 CE 接入的 ERPS over VPLS（采用以太网子接口接入）示例组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。
PE1、PE2、PE3上各接口的IP地址如表1所示。
表 10-10 数据规划

| 设备 | 接口 | IP地址 |
|---|---|---|
| PE1 | 10GE1/0/1.1 | - |
|  | 10GE1/0/2 | 10.1.1.1/24 |
|  | Loopback1 | 1.1.1.1/32 |
| PE2 | 10GE1/0/1.1 | - |
|  | 10GE1/0/2 | 10.2.1.1/24 |
|  | Loopback1 | 2.2.2.2/32 |
| PE3 | 10GE1/0/1 | 10.1.1.2/24 |
|  | 10GE1/0/2 | 10.2.1.2/24 |

| 设备 | 接口 | IP地址 |
|---|---|---|
|  | 10GE1/0/3.1 | - |
|  | Loopback1 | 3.3.3.3/32 |

配置思路采用如下的思路配置CE接入的ERPS over VPLS示例（采用以太子接口接入）：
1. 在PE设备上运行IGP协议，使VPLS骨干网络内的各设备能互通。
2. 在VPLS骨干网络上配置MPLS基本能力，建立LDP LSP隧道。
3. PE之间建立VPLS连接，并将VSI与相应的以太子接口绑定。
4. 配置ERPS，包括：
– 在PE1-CE1-CE2-PE2之间的物理链路上，启用ERPS。
– 配置CE2的10GE1/0/2为RPL owner端口。
数据准备为完成此配置例，需准备如下的数据：
● 配置OSPF协议所需数据：各接口IP地址、OSPF进程号、OSPF区域标识。
● MPLS LSR-ID（作为MPLS对等体地址）。
● VSI名称和VSI ID。
● 绑定VSI的以太子接口。
● ERPS环ID、控制VLAN ID、RPL owner端口。
操作步骤步骤1 配置VPLS骨干网接口IP地址和IGP协议，使PE互通，本例IGP使用OSPF协议。配置OSPF时，注意需要发布PE1、PE2和PE3的32位Loopback接口地址（LSR-ID）。
具体配置步骤请参见配置脚本。
步骤2 在MPLS骨干网上配置MPLS基本能力，PE之间建立动态LDP LSP。
\# 配置 PE1 。
[PE1] mpls lsr-id 1.1.1.1 [PE1] mpls [PE1-mpls] quit [PE1] mpls ldp [PE1-mpls-ldp] quit [PE1] interface 10ge 1/0/2 [PE1-10GE1/0/2] mpls [PE1-10GE1/0/2] mpls ldp [PE1-10GE1/0/2] quit \# 配置PE2。
[PE2] mpls lsr-id 2.2.2.2 [PE2] mpls [PE2-mpls] quit [PE2] mpls ldp

[PE2-mpls-ldp] quit [PE2] interface 10ge 1/0/2 [PE2-10GE1/0/2] mpls [PE2-10GE1/0/2] mpls ldp [PE2-10GE1/0/2] quit \# 配置PE3。
[PE3] mpls lsr-id 3.3.3.3 [PE3] mpls [PE3-mpls] quit [PE3] mpls ldp [PE3-mpls-ldp] quit [PE3] interface 10ge 1/0/1 [PE3-10GE1/0/1] mpls [PE3-10GE1/0/1] mpls ldp [PE3-10GE1/0/1] quit [PE3] interface 10ge 1/0/2 [PE3-10GE1/0/2] mpls [PE3-10GE1/0/2] mpls ldp [PE3-10GE1/0/2] quit步骤3 在PE上使能MPLS L2VPN。
\# 配置PE1。
[PE1] mpls l2vpn [PE1-l2vpn] quit \# 配置PE2。
[PE2] mpls l2vpn [PE2-l2vpn] quit \# 配置PE3。
[PE3] mpls l2vpn [PE3-l2vpn] quit步骤4 配置VPLS。
\# 配置PE1。
[PE1] vsi s1 static [PE1-vsi-s1] pwsignal ldp [PE1-vsi-s1-ldp] vsi-id 10 [PE1-vsi-s1-ldp] peer 3.3.3.3 [PE1-vsi-s1-ldp] quit [PE1-vsi-s1] quit [PE1] interface 10ge 1/0/1 [PE1-10GE1/0/1] portswitch [PE1-10GE1/0/1] port link-type trunk [PE1-10GE1/0/1] quit [PE1] interface 10ge 1/0/1.1 [PE1-10GE1/0/1.1] shutdown [PE1-10GE1/0/1.1] dot1q termination vid 10 [PE1-10GE1/0/1.1] l2 binding vsi s1 [PE1-10GE1/0/1.1] undo shutdown [PE1-10GE1/0/1.1] quit \# 配置PE2。
[PE2] vsi s1 static [PE2-vsi-s1] pwsignal ldp [PE2-vsi-s1-ldp] vsi-id 10 [PE2-vsi-s1-ldp] peer 3.3.3.3 [PE2-vsi-s1-ldp] quit [PE2-vsi-s1] quit [PE2] interface 10ge 1/0/1 [PE2-10GE1/0/1] portswitch

[PE2-10GE1/0/1] port link-type trunk [PE2-10GE1/0/1] quit [PE2] interface 10ge 1/0/1.1 [PE2-10GE1/0/1.1] shutdown [PE2-10GE1/0/1.1] dot1q termination vid 10 [PE2-10GE1/0/1.1] l2 binding vsi s1 [PE2-10GE1/0/1.1] undo shutdown [PE2-10GE1/0/1.1] quit \# 配置PE3。
[PE3] vsi s1 static [PE3-vsi-s1] pwsignal ldp [PE3-vsi-s1-ldp] vsi-id 10 [PE3-vsi-s1-ldp] peer 1.1.1.1 [PE3-vsi-s1-ldp] peer 2.2.2.2 [PE3-vsi-s1-ldp] quit [PE3-vsi-s1] quit [PE3] interface 10ge 1/0/1 [PE3-10GE1/0/1] portswitch [PE3-10GE1/0/1] port link-type trunk [PE3-10GE1/0/1] quit [PE3] interface 10ge 1/0/1.1 [PE3-10GE1/0/1.1] shutdown [PE3-10GE1/0/1.1] dot1q termination vid 10 [PE3-10GE1/0/1.1] l2 binding vsi s1 [PE3-10GE1/0/1.1] undo shutdown [PE3-10GE1/0/1.1] quit步骤5 在PE1、PE2、CE1和CE2上配置ERPS。
\# 配置PE1。
[PE1] erps ring 1 [PE1-erps-ring1] control-vlan 100 [PE1-erps-ring1] protected-instance 1 [PE1-erps-ring1] version v2 [PE1-erps-ring1] sub-ring [PE1-erps-ring1] quit [PE1] stp region-configuration [PE1-mst-region] instance 1 vlan 10 100 [PE1-mst-region] quit [PE1] interface 10ge 1/0/1 [PE1-10GE1/0/1] portswitch [PE1-10GE1/0/1] port link-type trunk [PE1-10GE1/0/1] undo port trunk allow-pass vlan 1 [PE1-10GE1/0/1] stp disable [PE1-10GE1/0/1] erps ring 1 [PE1-10GE1/0/1] erps vpls-subinterface enable [PE1-10GE1/0/1] quit \# 配置 PE2 。
[PE2] erps ring 1 [PE2-erps-ring1] control-vlan 100 [PE2-erps-ring1] protected-instance 1 [PE2-erps-ring1] version v2 [PE2-erps-ring1] sub-ring [PE2-erps-ring1] quit [PE2] stp region-configuration [PE2-mst-region] instance 1 vlan 10 100 [PE2-mst-region] quit [PE2] interface 10ge 1/0/1 [PE2-10GE1/0/1] portswitch [PE2-10GE1/0/1] port link-type trunk [PE2-10GE1/0/1] undo port trunk allow-pass vlan 1 [PE2-10GE1/0/1] stp disable [PE2-10GE1/0/1] erps ring 1 [PE2-10GE1/0/1] erps vpls-subinterface enable [PE2-10GE1/0/1] quit

\# 配置CE1。
<Device> system-view [Device] sysname CE1 [CE1] erps ring 1 [CE1-erps-ring1] control-vlan 100 [CE1-erps-ring1] protected-instance 1 [CE1-erps-ring1] version v2 [CE1-erps-ring1] sub-ring [CE1-erps-ring1] quit [CE1] stp region-configuration [CE1-mst-region] instance 1 vlan 10 100 [CE1-mst-region] quit [CE1] interface 10ge 1/0/1 [CE1-10GE1/0/1] portswitch [CE1-10GE1/0/1] port link-type trunk [CE1-10GE1/0/1] undo port trunk allow-pass vlan 1 [CE1-10GE1/0/1] port trunk allow-pass vlan 10 [CE1-10GE1/0/1] stp disable [CE1-10GE1/0/1] erps ring 1 [CE1-10GE1/0/1] quit [CE1] interface 10ge 1/0/2 [CE1-10GE1/0/2] portswitch [CE1-10GE1/0/2] port link-type trunk [CE1-10GE1/0/2] undo port trunk allow-pass vlan 1 [CE1-10GE1/0/2] port trunk allow-pass vlan 10 [CE1-10GE1/0/2] stp disable [CE1-10GE1/0/2] erps ring 1 [CE1-10GE1/0/2] quit \# 配置CE2。
<Device> system-view [Device] sysname CE2 [CE2] erps ring 1 [CE2-erps-ring1] control-vlan 100 [CE2-erps-ring1] protected-instance 1 [CE2-erps-ring1] version v2 [CE2-erps-ring1] sub-ring [CE2-erps-ring1] quit [CE2] stp region-configuration [CE2-mst-region] instance 1 vlan 10 100 [CE2-mst-region] quit [CE2] interface 10ge 1/0/1 [CE2-10GE1/0/1] portswitch [CE2-10GE1/0/1] port link-type trunk [CE2-10GE1/0/1] undo port trunk allow-pass vlan 1 [CE2-10GE1/0/1] port trunk allow-pass vlan 10 [CE2-10GE1/0/1] stp disable [CE2-10GE1/0/1] erps ring 1 [CE2-10GE1/0/1] quit [CE2] interface 10ge 1/0/2 [CE2-10GE1/0/2] portswitch [CE2-10GE1/0/2] port link-type trunk [CE2-10GE1/0/2] undo port trunk allow-pass vlan 1 [CE2-10GE1/0/2] port trunk allow-pass vlan 10 [CE2-10GE1/0/2] stp disable [CE2-10GE1/0/2] erps ring 1 rpl owner [CE2-10GE1/0/2] quit步骤6 验证配置结果完成上述配置后，在PE3上执行display vsi name s1 verbose命令，可以看到，PE3与PE1（1.1.1.1）和PE2（2.2.2.2）分别建立了PW。
[PE3] display vsi name s1 verbose
***VSI Name : s1 Administrator VSI : no Isolate Spoken : disable

VSI Index : 2 PW Signaling : ldp Member Discovery Style : static PW MAC Learn Style : unqualify Encapsulation Type : vlan MTU : 1500 Diffserv Mode : uniform Mpls Exp : -- DomainId : 255 Domain Name :
Ignore AcState : disable P2P VSI : disable Create Time : 0 days, 1 hours, 19 minutes, 38 seconds VSI State : up VSI ID : 10
*Peer Router ID : 1.1.1.1 Negotiation-vc-id : 10 primary or secondary : primary ignore-standby-state : no VC Label : 32891 Peer Type : dynamic Session : up Tunnel ID : 0x0000000001004c4b41 Broadcast Tunnel ID : -- Broad BackupTunnel ID : -- CKey : 2 NKey : 1862271177 Stp Enable : 0 PwIndex : 1 Control Word : disable BFD for PW : unavailable
*Peer Router ID : 2.2.2.2 Negotiation-vc-id : 10 primary or secondary : primary ignore-standby-state : no VC Label : 32892 Peer Type : dynamic Session : up Tunnel ID : 0x0000000001004c4b42 Broadcast Tunnel ID : -- Broad BackupTunnel ID : -- CKey : 2 NKey : 1862271178 Stp Enable : 0 PwIndex : 2 Control Word : disable BFD for PW : unavailable
**PW Information:
*Peer Ip Address : 1.1.1.1 PW State : up Local VC Label : 32891 Remote VC Label : 32890 Remote Control Word : disable PW Type : label Local VCCV : alert lsp-ping bfd Remote VCCV : alert lsp-ping bfd Tunnel ID : 0x0000000001004c4b41 Broadcast Tunnel ID : -- Broad BackupTunnel ID : -- Ckey : 2 Nkey : 1862271177 Main PW Token : 0x0 Slave PW Token : 0x0 Tnl Type : ldp OutInterface : LDP LSP Backup OutInterface : --

Stp Enable : 0 PW Last Up Time : 2016/06/14 17:35:12 PW Total Up Time : 0 days, 1 hours, 19 minutes, 38 seconds
*Peer Ip Address : 2.2.2.2 PW State : up Local VC Label : 32892 Remote VC Label : 32893 Remote Control Word : disable PW Type : label Local VCCV : alert lsp-ping bfd Remote VCCV : alert lsp-ping bfd Tunnel ID : 0x0000000001004c4b42 Broadcast Tunnel ID : -- Broad BackupTunnel ID : -- Ckey : 2 Nkey : 1862271178 Main PW Token : 0x0 Slave PW Token : 0x0 Tnl Type : ldp OutInterface : LDP LSP Backup OutInterface : -- Stp Enable : 0 PW Last Up Time : 2016/06/14 10:35:45 PW Total Up Time : 0 days, 1 hours, 19 minutes, 45 seconds而且可以看到，在 CE2 上，与 CE1 相连的链路被阻断。
[CE2] display erps D : Discarding F : Forwarding R : RPL Owner N : RPL Neighbour FS : Forced Device MS : Manual Device Total number of rings configured = 1 Ring Control WTR Timer Guard Timer Port 1 Port 2 ID VLAN (min) (csec)
-------------------------------------------------------------------------------- 1 100 5 200 (F)10GE1/0/1 (D,R)10GE1/0/2
--------------------------------------------------------------------------------
----结束配置脚本
● PE1 \# sysname PE1 \# vlan batch 100 \# stp region-configuration instance 1 vlan 10 100 \# erps ring 1 control-vlan 100 protected-instance 1 version v2 sub-ring \# mpls lsr-id 1.1.1.1 \# mpls \# mpls l2vpn \# vsi s1 static pwsignal ldp

vsi-id 10 peer 3.3.3.3 \# mpls ldp \# interface 10GE1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 100 stp disable erps ring 1 erps vpls-subinterface enable \# interface 10GE1/0/1.1 dot1q termination vid 10 l2 binding vsi s1 \# interface 10GE1/0/2 undo portswitch ip address 10.1.1.1 255.255.255.0 mpls mpls ldp \# interface LoopBack1 ip address 1.1.1.1 255.255.255.255 \# ospf 1 area 0.0.0.0 network 1.1.1.1 0.0.0.0 network 10.1.1.0 0.0.0.255 \# return
● PE2 \# sysname PE2 \# vlan batch 100 \# stp region-configuration instance 1 vlan 10 100 \# erps ring 1 control-vlan 100 protected-instance 1 version v2 sub-ring \# mpls lsr-id 2.2.2.2 \# mpls \# mpls l2vpn \# vsi s1 static pwsignal ldp vsi-id 10 peer 3.3.3.3 \# mpls ldp \# interface 10GE1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 100 stp disable erps ring 1 erps vpls-subinterface enable \# interface 10GE1/0/1.1

dot1q termination vid 10 l2 binding vsi s1 \# interface 10GE1/0/2 undo portswitch ip address 10.2.1.1 255.255.255.0 mpls mpls ldp \# interface LoopBack1 ip address 2.2.2.2 255.255.255.255 \# ospf 1 area 0.0.0.0 network 2.2.2.2 0.0.0.0 network 10.2.1.0 0.0.0.255 \# return
● PE3 \# sysname PE3 \# mpls lsr-id 3.3.3.3 \# mpls \# mpls l2vpn \# vsi s1 static pwsignal ldp vsi-id 10 peer 1.1.1.1 peer 2.2.2.2 \# mpls ldp \# interface 10GE1/0/1 undo portswitch ip address 10.1.1.2 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/2 undo portswitch ip address 10.2.1.2 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/3 port link-type trunk \# interface 10GE1/0/3.1 dot1q termination vid 10 l2 binding vsi s1 \# interface LoopBack1 ip address 3.3.3.3 255.255.255.255 \# ospf 1 area 0.0.0.0 network 3.3.3.3 0.0.0.0 network 10.1.1.0 0.0.0.255 network 10.2.1.0 0.0.0.255 \# return
● CE1 \# sysname CE1

\# vlan batch 10 100 \# stp region-configuration instance 1 vlan 10 100 \# erps ring 1 control-vlan 100 protected-instance 1 version v2 sub-ring \# interface 10GE1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 stp disable erps ring 1 \# interface 10GE1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 stp disable erps ring 1 \# return
● CE2 \# sysname CE1 \# vlan batch 10 100 \# stp region-configuration instance 1 vlan 10 100 \# erps ring 1 control-vlan 100 protected-instance 1 version v2 sub-ring \# interface 10GE1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 stp disable erps ring 1 \# interface 10GE1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 stp disable erps ring 1 rpl owner \# return

#### 10.13.6 举例：配置CE接入的ERPS over VPLS（采用VLANIF接口接入）

组网需求图10-23是CE接入PE的VPLS组网。但是该组网却存在一个问题，就是PE3会收到双份对端CE发送的流量。为解决此问题，可以在PE1-CE1-CE2-PE2之间的物理链路上使能

ERPS，通过配置ERPS的RPL owner端口，使得CE2的interface2被阻断。这样，CE1的流量便不会经过CE2，而是直接通过PE1传输给PE3，从而避免双份流量或环路。
图 10-23 配置 CE 接入的 ERPS over VPLS（采用 VLANIF 接口接入）示例组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
PE1、PE2、PE3上各接口的IP地址如表1所示。
表 10-11 数据规划

| 设备 | 接口 | IP地址 |
|---|---|---|
| PE1 | 10GE1/0/1 | - |
|  | 10GE1/0/2 | 10.1.1.1/24 |
|  | Loopback1 | 1.1.1.1/32 |
| PE2 | 10GE1/0/1 | - |
|  | 10GE1/0/2 | 10.2.1.1/24 |
|  | Loopback1 | 2.2.2.2/32 |
| PE3 | 10GE1/0/1 | 10.1.1.2/24 |
|  | 10GE1/0/2 | 10.2.1.2/24 |
|  | 10GE1/0/3 | - |
|  | Loopback1 | 3.3.3.3/32 |

配置思路采用如下的思路配置CE接入的ERPS over VPLS示例（采用VLANIF接口接入）：

1. 在PE设备上运行IGP协议，使VPLS骨干网络内的各设备能互通。
2. 在VPLS骨干网络上配置MPLS基本能力，建立LDP LSP隧道。
3. PE之间建立VPLS连接，并将VSI与相应的VLANIF接口绑定。
4. 配置ERPS，包括：
– 在PE1-CE1-CE2-PE2之间的物理链路上，启用ERPS。
– 配置CE2的10GE1/0/2为RPL owner端口。
数据准备
为完成此配置例，需准备如下的数据：
● 配置OSPF协议所需数据：各接口IP地址、OSPF进程号、OSPF区域标识。
● MPLS LSR-ID（作为MPLS对等体地址）。
● VSI名称和VSI ID。
● 绑定VSI的VLANIF接口。
● ERPS环ID、控制VLAN ID、RPL owner端口。
操作步骤
步骤1 配置VPLS骨干网接口IP地址和IGP协议，使PE互通，本例IGP使用OSPF协议。配置
OSPF时，注意需要发布PE1、PE2和PE3的32位Loopback接口地址（LSR-ID）。
具体配置步骤参考配置脚本。
步骤2 在MPLS骨干网上配置MPLS基本能力，PE之间建立动态LDP LSP。
\# 配置PE1。
[PE1] mpls lsr-id 1.1.1.1
[PE1] mpls
[PE1-mpls] quit
[PE1] mpls ldp
[PE1-mpls-ldp] quit
[PE1] interface 10ge 1/0/2
[PE1-10GE1/0/2] mpls
[PE1-10GE1/0/2] mpls ldp
[PE1-10GE1/0/2] quit
\# 配置PE2。
[PE2] mpls lsr-id 2.2.2.2
[PE2] mpls
[PE2-mpls] quit
[PE2] mpls ldp
[PE2-mpls-ldp] quit
[PE2] interface 10ge 1/0/2
[PE2-10GE1/0/2] mpls
[PE2-10GE1/0/2] mpls ldp
[PE2-10GE1/0/2] quit
\# 配置PE3。
[PE3] mpls lsr-id 3.3.3.3
[PE3] mpls
[PE3-mpls] quit
[PE3] mpls ldp
[PE3-mpls-ldp] quit
[PE3] interface 10ge 1/0/1
[PE3-10GE1/0/1] mpls

[PE3-10GE1/0/1] mpls ldp [PE3-10GE1/0/1] quit [PE3] interface 10ge 1/0/2 [PE3-10GE1/0/2] mpls [PE3-10GE1/0/2] mpls ldp [PE3-10GE1/0/2] quit步骤3 在PE上使能MPLS L2VPN。
\# 配置PE1。
[PE1] mpls l2vpn [PE1-l2vpn] quit \# 配置PE2。
[PE2] mpls l2vpn [PE2-l2vpn] quit \# 配置PE3。
[PE3] mpls l2vpn [PE3-l2vpn] quit步骤 配置 。
4 VPLS \# 配置PE1。
[PE1] vsi s1 static [PE1-vsi-s1] pwsignal ldp [PE1-vsi-s1-ldp] vsi-id 10 [PE1-vsi-s1-ldp] peer 3.3.3.3 [PE1-vsi-s1-ldp] quit [PE1-vsi-s1] quit [PE1] vlan 10 [PE1-vlan10] quit [PE1] interface vlanif10 [PE1-Vlanif10] l2 binding vsi s1 [PE1-Vlanif10] quit \# 配置PE2。
[PE2] vsi s1 static [PE2-vsi-s1] pwsignal ldp [PE2-vsi-s1-ldp] vsi-id 10 [PE2-vsi-s1-ldp] peer 3.3.3.3 [PE2-vsi-s1-ldp] quit [PE2-vsi-s1] quit [PE2] interface vlanif10 [PE2-Vlanif10] l2 binding vsi s1 [PE2-Vlanif10] quit \# 配置PE3。
[PE3] vsi s1 static [PE3-vsi-s1] pwsignal ldp [PE3-vsi-s1-ldp] vsi-id 10 [PE3-vsi-s1-ldp] peer 1.1.1.1 [PE3-vsi-s1-ldp] peer 2.2.2.2 [PE3-vsi-s1-ldp] quit [PE3-vsi-s1] quit [PE3] vlan 10 [PE3-vlan10] quit [PE3] interface 10ge 1/0/3 [PE3-10GE1/0/3] portswitch [PE3-10GE1/0/3] port link-type trunk [PE3-10GE1/0/3] port trunk allow-pass vlan 10 [PE3-10GE1/0/3] quit [PE3] interface vlanif10

[PE3-Vlanif10] l2 binding vsi s1 [PE3-Vlanif10] quit步骤5 在PE1、PE2、CE1和CE2上配置ERPS。
\# 配置PE1。
[PE1] erps ring 1 [PE1-erps-ring1] control-vlan 100 [PE1-erps-ring1] protected-instance 1 [PE1-erps-ring1] version v2 [PE1-erps-ring1] sub-ring [PE1-erps-ring1] quit [PE1] stp region-configuration [PE1-mst-region] instance 1 vlan 10 100 [PE1-mst-region] quit [PE1] interface 10ge 1/0/1 [PE1-10GE1/0/1] portswitch [PE1-10GE1/0/1] port link-type trunk [PE1-10GE1/0/1] undo port trunk allow-pass vlan 1 [PE1-10GE1/0/1] port trunk allow-pass vlan 10 [PE1-10GE1/0/1] stp disable [PE1-10GE1/0/1] erps ring 1 [PE1-10GE1/0/1] quit \# 配置 PE2 。
[PE2] erps ring 1 [PE2-erps-ring1] control-vlan 100 [PE2-erps-ring1] protected-instance 1 [PE2-erps-ring1] version v2 [PE2-erps-ring1] sub-ring [PE2-erps-ring1] quit [PE2] stp region-configuration [PE2-mst-region] instance 1 vlan 10 100 [PE2-mst-region] quit [PE2] interface 10ge 1/0/1 [PE2-10GE1/0/1] portswitch [PE2-10GE1/0/1] port link-type trunk [PE2-10GE1/0/1] undo port trunk allow-pass vlan 1 [PE2-10GE1/0/1] port trunk allow-pass vlan 10 [PE2-10GE1/0/1] stp disable [PE2-10GE1/0/1] erps ring 1 [PE2-10GE1/0/1] quit \# 配置CE1。
<Device> system-view [Device] sysname CE1 [CE1] erps ring 1 [CE1-erps-ring1] control-vlan 100 [CE1-erps-ring1] protected-instance 1 [CE1-erps-ring1] version v2 [CE1-erps-ring1] sub-ring [CE1-erps-ring1] quit [CE1] stp region-configuration [CE1-mst-region] instance 1 vlan 10 100 [CE1-mst-region] quit [CE1] interface 10ge 1/0/1 [CE1-10GE1/0/1] portswitch [CE1-10GE1/0/1] port link-type trunk [CE1-10GE1/0/1] undo port trunk allow-pass vlan 1 [CE1-10GE1/0/1] port trunk allow-pass vlan 10 [CE1-10GE1/0/1] stp disable [CE1-10GE1/0/1] erps ring 1 [CE1-10GE1/0/1] quit [CE1] interface 10ge 1/0/2 [CE1-10GE1/0/2] portswitch [CE1-10GE1/0/2] port link-type trunk [CE1-10GE1/0/2] undo port trunk allow-pass vlan 1 [CE1-10GE1/0/2] port trunk allow-pass vlan 10

[CE1-10GE1/0/2] stp disable [CE1-10GE1/0/2] erps ring 1 [CE1-10GE1/0/2] quit \# 配置CE2。
<Device> system-view [Device] sysname CE2 [CE2] erps ring 1 [CE2-erps-ring1] control-vlan 100 [CE2-erps-ring1] protected-instance 1 [CE2-erps-ring1] version v2 [CE2-erps-ring1] sub-ring [CE2-erps-ring1] quit [CE2] stp region-configuration [CE2-mst-region] instance 1 vlan 10 100 [CE2-mst-region] quit [CE2] interface 10ge 1/0/1 [CE2-10GE1/0/1] portswitch [CE2-10GE1/0/1] port link-type trunk [CE2-10GE1/0/1] undo port trunk allow-pass vlan 1 [CE2-10GE1/0/1] port trunk allow-pass vlan 10 [CE2-10GE1/0/1] stp disable [CE2-10GE1/0/1] erps ring 1 [CE2-10GE1/0/1] quit [CE2] interface 10ge 1/0/2 [CE2-10GE1/0/2] portswitch [CE2-10GE1/0/2] port link-type trunk [CE2-10GE1/0/2] undo port trunk allow-pass vlan 1 [CE2-10GE1/0/2] port trunk allow-pass vlan 10 [CE2-10GE1/0/2] stp disable [CE2-10GE1/0/2] erps ring 1 rpl owner [CE2-10GE1/0/2] quit步骤6 验证配置结果完成上述配置后，在PE3上执行display vsi name s1 verbose命令，可以看到，PE3与PE1（1.1.1.1）和PE2（2.2.2.2）分别建立了PW。
[PE3] display vsi name s1 verbose
***VSI Name : s1 Administrator VSI : no Isolate Spoken : disable VSI Index : 2 PW Signaling : ldp Member Discovery Style : static PW MAC Learn Style : unqualify Encapsulation Type : vlan MTU : 1500 Diffserv Mode : uniform Mpls Exp : -- DomainId : 255 Domain Name :
Ignore AcState : disable P2P VSI : disable Create Time : 0 days, 1 hours, 19 minutes, 38 seconds VSI State : up VSI ID : 10
*Peer Router ID : 1.1.1.1 Negotiation-vc-id : 10 primary or secondary : primary ignore-standby-state : no VC Label : 32891 Peer Type : dynamic Session : up Tunnel ID : 0x0000000001004c4b41 Broadcast Tunnel ID : -- Broad BackupTunnel ID : -- CKey : 2

NKey : 1862271177 Stp Enable : 0 PwIndex : 1 Control Word : disable BFD for PW : unavailable
*Peer Router ID : 2.2.2.2 Negotiation-vc-id : 10 primary or secondary : primary ignore-standby-state : no VC Label : 32892 Peer Type : dynamic Session : up Tunnel ID : 0x0000000001004c4b42 Broadcast Tunnel ID : -- Broad BackupTunnel ID : -- CKey : 2 NKey : 1862271178 Stp Enable : 0 PwIndex : 2 Control Word : disable BFD for PW : unavailable
**PW Information:
*Peer Ip Address : 1.1.1.1 PW State : up Local VC Label : 32891 Remote VC Label : 32890 Remote Control Word : disable PW Type : label Local VCCV : alert lsp-ping bfd Remote VCCV : alert lsp-ping bfd Tunnel ID : 0x0000000001004c4b41 Broadcast Tunnel ID : -- Broad BackupTunnel ID : -- Ckey : 2 Nkey : 1862271177 Main PW Token : 0x0 Slave PW Token : 0x0 Tnl Type : ldp OutInterface : LDP LSP Backup OutInterface : -- Stp Enable : 0 PW Last Up Time : 2016/06/14 17:35:12 PW Total Up Time : 0 days, 1 hours, 19 minutes, 38 seconds
*Peer Ip Address : 2.2.2.2 PW State : up Local VC Label : 32892 Remote VC Label : 32893 Remote Control Word : disable PW Type : label Local VCCV : alert lsp-ping bfd Remote VCCV : alert lsp-ping bfd Tunnel ID : 0x0000000001004c4b42 Broadcast Tunnel ID : -- Broad BackupTunnel ID : -- Ckey : 2 Nkey : 1862271178 Main PW Token : 0x0 Slave PW Token : 0x0 Tnl Type : ldp OutInterface : LDP LSP Backup OutInterface : -- Stp Enable : 0 PW Last Up Time : 2016/06/14 10:35:45 PW Total Up Time : 0 days, 1 hours, 19 minutes, 45 seconds而且可以看到，在CE2上，与CE1相连的链路被阻断。

[CE2] display erps D : Discarding F : Forwarding R : RPL Owner N : RPL Neighbour FS : Forced Device MS : Manual Device Total number of rings configured = 1 Ring Control WTR Timer Guard Timer Port 1 Port 2 ID VLAN (min) (csec)
-------------------------------------------------------------------------------- 1 100 5 200 (F)10GE1/0/1 (D,R)10GE1/0/2
--------------------------------------------------------------------------------
----结束配置脚本
● PE1 \# sysname PE1 \# vlan batch 10 100 \# stp region-configuration instance 1 vlan 10 100 \# erps ring 1 control-vlan 100 protected-instance 1 version v2 sub-ring \# mpls lsr-id 1.1.1.1 \# mpls \# mpls l2vpn \# vsi s1 static pwsignal ldp vsi-id 10 peer 3.3.3.3 \# mpls ldp \# interface Vlanif10 l2 binding vsi s1 \# interface 10GE1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 stp disable erps ring 1 \# interface 10GE1/0/2 undo portswitch ip address 10.1.1.1 255.255.255.0 mpls mpls ldp \# interface LoopBack1 ip address 1.1.1.1 255.255.255.255 \# ospf 1 area 0.0.0.0 network 1.1.1.1 0.0.0.0

network 10.1.1.0 0.0.0.255 \# return
● PE2 \# sysname PE2 \# vlan batch 10 100 \# stp region-configuration instance 1 vlan 10 100 \# erps ring 1 control-vlan 100 protected-instance 1 version v2 sub-ring \# mpls lsr-id 2.2.2.2 \# mpls \# mpls l2vpn \# vsi s1 static pwsignal ldp vsi-id 10 peer 3.3.3.3 \# mpls ldp \# interface Vlanif10 l2 binding vsi s1 \# interface 10GE1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 stp disable erps ring 1 \# interface 10GE1/0/2 undo portswitch ip address 10.2.1.1 255.255.255.0 mpls mpls ldp \# interface LoopBack1 ip address 2.2.2.2 255.255.255.255 \# ospf 1 area 0.0.0.0 network 2.2.2.2 0.0.0.0 network 10.2.1.0 0.0.0.255 \# return
● PE3 \# sysname PE3 \# vlan batch 10 \# mpls lsr-id 3.3.3.3 \# mpls \# mpls l2vpn \#

vsi s1 static pwsignal ldp vsi-id 10 peer 1.1.1.1 peer 2.2.2.2 \# mpls ldp \# interface Vlanif10 l2 binding vsi s1 \# interface 10GE1/0/1 undo portswitch ip address 10.1.1.2 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/2 undo portswitch ip address 10.2.1.2 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 10 \# interface LoopBack1 ip address 3.3.3.3 255.255.255.255 \# ospf 1 area 0.0.0.0 network 3.3.3.3 0.0.0.0 network 10.1.1.0 0.0.0.255 network 10.2.1.0 0.0.0.255 \# return
● CE1 \# sysname CE1 \# vlan batch 10 100 \# stp region-configuration instance 1 vlan 10 100 \# erps ring 1 control-vlan 100 protected-instance 1 version v2 sub-ring \# interface 10GE1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 stp disable erps ring 1 \# interface 10GE1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 stp disable erps ring 1 \# return
● CE2

\# sysname CE1 \# vlan batch 10 100 \# stp region-configuration instance 1 vlan 10 100 \# erps ring 1 control-vlan 100 protected-instance 1 version v2 sub-ring \# interface 10GE1/0/1 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 stp disable erps ring 1 \# interface 10GE1/0/2 port link-type trunk undo port trunk allow-pass vlan 1 port trunk allow-pass vlan 10 100 stp disable erps ring 1 rpl owner \# return

### 10.14 ERPS常见配置错误

#### 10.14.1 ERPS链路流量不能正常转发

故障现象配置完ERPS功能后，由于环状态异常，导致业务数据流量不能正常进行转发。
操作步骤步骤1 在任意视图下查看ERPS环在本设备上的信息display erps [ ring ring-id ] verbose正常情况下，在显示信息中， ERPS 环上的端口角色只有一个 RPL Owner ，其他端口角色是普通端口或RPL Neighbour端口，环内的每个节点的环状态 “Ring State”为Idle。
如果ERPS环不完整或状态不正常：
1. 请检查ERPS环上各设备是否均加入了ERPS环。
2. 请检查ERPS环上各设备ERPS环的配置是否一致，包括ERPS协议版本号、主环和/或子环配置。
3. 请检查 ERPS 环上各设备是否正确配置了端口角色、控制 VLAN 和保护实例。
4. 请检查相关端口是否已经配置允许指定数据VLAN通过。
----结束
