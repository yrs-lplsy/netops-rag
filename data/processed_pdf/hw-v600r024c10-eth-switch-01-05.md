# S1700, S5700, S6700 V600R024C10 配置指南-以太网交换 01-05 GVRP配置

## 5 GVRP配置

5 GVRP 配置

### 5.1 GVRP简介

5.2 GVRP配置注意事项
5.3 GVRP原理描述
5.4 GVRP缺省配置
5.5 配置GVRP功能
5.6 维护GVRP
5.7 GVRP配置举例
5.1 GVRP 简介
定义
GARP VLAN注册协议GVRP（GARP VLAN Registration Protocol），用于注册和注销
VLAN属性。GVRP使得设备之间能够互相交换VLAN配置信息，从而实现VLAN的动态
创建与管理。
GVRP是GARP的一种具体应用。通用属性注册协议GARP（Generic Attribute
Registration Protocol）建立了一种属性传递扩散的通用机制，以保证协议实体能够注
册和注销该属性。 GARP 作为一个属性注册协议的载体，可以用来传播属性。将 GARP
协议报文的内容映射成不同的属性即可支持不同上层协议应用。
GARP通过目的MAC地址区分不同的应用。在IEEE Std 802.1Q中将01-80-C2-00-00-21
分配给VLAN应用，即GVRP。
目的
如果要为网络中的所有设备都配置VLAN，需要网络管理员在每台设备上分别进行手工
添加。如图5-1所示，DeviceA上有VLAN2，DeviceB和DeviceC上只有VLAN1，三台设
备通过Trunk链路连接在一起。为了使DeviceA上VLAN2的报文可以传到DeviceC，网
络管理员必须在DeviceB和DeviceC上分别手工添加VLAN2。

图 5-1 GVRP 适用组网图对于上面的组网情况，手工添加VLAN很简单，但是当实际组网复杂到网络管理员无法短时间内了解网络的拓扑结构，或者是整个网络的VLAN太多时，工作量会非常大，而且非常容易配置错误。
在这种情况下，用户可以通过GVRP的VLAN自动注册功能完成VLAN的配置，即在一台设备上配置 VLAN 后，通过 GVRP 协议将配置的 VLAN 信息快速传播至整个网络。
受益GVRP主要用于维护设备动态VLAN属性。通过GVRP，一台设备上的VLAN信息会迅速传播到整个交换网。GVRP实现动态分发、注册和传播VLAN属性，从而达到减少网络管理员的手工配置量及保证VLAN配置正确的目的。

### 5.2 GVRP配置注意事项

License 依赖GVRP无需License许可即可使用。
硬件依赖表 5-1 支持本特性的硬件

| 系列 | 支持产品 |
|---|---|
| S6750-H | S6750-H36C，S6750-H48Y8C |
| S6730E-H-V2 | S6730E-H6FX4Y2CZ-V2 |
| S1730S-S3 | S1730S-S24P4S-A3，S1730S-S24P4X-A3， S1730S-S24T4S-QA3，S1730S-S24T4X-QA3， S1730S-S48P4S-A3，S1730S-S48T4S-A3， S1730S-S48T4X-A3，S1730S-S8P4X-QA3， S1730S-S8T4X-QA3 |

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
特性限制无

### 5.3 GVRP原理描述

#### 5.3.1 GVRP基本概念

应用实体在设备上，每一个参与协议的端口可以视为一个应用实体。当GARP应用在端口上启动后，该端口即为一个GARP应用实体。对于GVRP而言，GVRP在设备上启动后，每个启动GVRP的端口对应一个GVRP应用实体，如图 GVRP应用实体示意图所示。
图 5-2 GVRP 应用实体示意图VLAN 的注册和注销GVRP可以实现VLAN属性的自动注册和注销：
● VLAN的注册：指的是将端口加入VLAN。

● VLAN的注销：指的是将端口退出VLAN。
GVRP通过声明和回收声明的方式来实现VLAN属性的注册和注销，如图 VLAN的注册
与注销所示。
图 5-3 VLAN 的注册与注销
● 当端口接收到一个VLAN属性声明时，该端口将注册该声明中包含的VLAN信息，
使得端口加入VLAN。
● 当端口接收到一个VLAN属性的回收声明时，该端口将注销该声明中包含的VLAN
信息，使得端口退出 VLAN 。
GVRP的属性注册和注销仅仅是对于接收到GVRP协议报文的端口而言的。
消息类型
GARP应用实体之间的信息交换借助于消息的传递来完成，主要有三类消息起作用，分
别为Join消息、Leave消息和LeaveAll消息。同样，GVRP应用实体也主要通过这三类消
息进行信息交互。
● Join消息
当一个应用实体希望其它设备注册自己的属性信息时，它将对外发送Join消息；当
收到其它实体的Join消息或本设备静态配置了某些属性，需要其它GVRP应用实体
进行注册时，它也会向外发送Join消息。
Join消息分为JoinEmpty和JoinIn两种，区别如下：
– JoinEmpty：声明一个本身没有注册的属性。
– JoinIn：声明一个本身已经注册的属性。
● Leave消息
当一个应用实体希望其它设备注销自己的属性信息时，它将对外发送 Leave 消息；
当收到其它实体的Leave消息注销某些属性或静态注销了某些属性后，它也会向外
发送Leave消息。
Leave消息分为LeaveEmpty和LeaveIn两种，区别如下：
LeaveEmpty：注销一个本身没有注册的属性。
–
– LeaveIn：注销一个本身已经注册的属性。
● LeaveAll消息
每个应用实体启动后，将同时启动LeaveAll定时器，当该定时器超时后应用实体
将对外发送 LeaveAll 消息。
LeaveAll消息用来注销所有的属性，以使其它应用实体重新注册其实体上所有的
属性信息，以此来周期性地清除网络中的垃圾属性（例如某个属性已经被删除，
但由于设备突然断电，并没有发送Leave消息来通知其他实体注销此属性）。

定时器GARP协议定义了四类定时器，用于控制各类GARP消息的发送，GVRP作为GARP的一种应用，同样使用这四类定时器。下面分别介绍一下它们的作用。
● Join定时器Join定时器用来控制Join消息（包括JoinIn和JoinEmpty）的发送。
为了保证Join消息能够可靠地传输到其它应用实体，发送第一个Join消息后将等待一个Join定时器的时间间隔，如果在一个Join定时器时间内收到JoinIn消息，则不发送第二个Join消息；如果没收到，则再发送一个Join消息。每个端口维护独立的Join定时器。
● Hold定时器Hold定时器用来控制Join消息（包括JoinIn和JoinEmpty）和Leave消息（包括LeaveIn和LeaveEmpty）的发送。
当在应用实体上配置属性或应用实体接收到消息时不会立刻将该消息传播到其它设备，而是在等待一个Hold定时器后再发送消息，设备将此Hold定时器时间段内接收到的消息尽可能封装成最少数量的报文，这样可以减少报文的发送量。如果没有Hold定时器的话，每来一个消息就发送一个，造成网络上报文量太大，既不利于网络的稳定，也不利于充分利用每个报文的数据容量。
每个端口维护独立的Hold定时器。Hold定时器的值要小于等于Join定时器值的一半。
● Leave定时器Leave定时器是用来控制属性注销的。
每个应用实体接收到Leave或LeaveAll消息后会启动Leave定时器，如果在Leave定时器超时之前没有接收到该属性的Join消息，属性才会被注销。
这是因为网络中如果有一个实体因为不存在某个属性而发送了Leave消息，并不代表所有的实体都不存在该属性了，因此不能立刻注销属性，而是要等待其他实体的消息。
例如，某个属性在网络中有两个源，分别在应用实体A和B上，其他应用实体通过GVRP协议注册了该属性。当把此属性从应用实体A上删除的时候，实体A发送Leave消息，由于实体B上还存在该属性源，在接收到Leave消息之后，会发送Join消息，以表示它还有该属性。其他应用实体如果收到了应用实体B发送的Join消息，则该属性仍然被保留，不会被注销。只有当其它应用实体等待两个Join定时器以上仍没有收到该属性的Join消息时，才能认为网络中确实没有该属性了，所以这就要求Leave定时器的值大于2倍Join定时器的值。
每个端口维护独立的Leave定时器。
● LeaveAll定时器每个应用实体启动后，将同时启动LeaveAll定时器，当该定时器超时后GARP应用实体将对外发送LeaveAll消息，随后再启动LeaveAll定时器，开始新的一轮循环。
接收到LeaveAll消息的实体将重新启动所有的定时器，包括LeaveAll定时器。在自己的LeaveAll定时器重新超时之后才会再次发送LeaveAll消息，这样就避免了短时间内发送多个LeaveAll消息。
如果不同设备的LeaveAll定时器同时超时，就会同时发送多个LeaveAll消息，增加不必要的报文数量，为了避免不同设备同时发生LeaveAll定时器超时，实际定时器运行的值是大于 LeaveAll 定时器的值，小于 1.5 倍 LeaveAll 定时器值的一个随机值。一次LeaveAll事件相当于全网所有属性的一次Leave。由于LeaveAll影响范围很广，所以建议LeaveAll定时器的值不能太小，至少应该大于Leave定时器的值。
每个设备只在全局维护一个LeaveAll定时器。

注册模式手工配置的VLAN称为静态VLAN，通过GVRP协议创建的VLAN称为动态VLAN。GVRP有三种注册模式，不同的模式对静态VLAN和动态VLAN的处理方式也不同。GVRP的三种注册模式分别定义如下：
● Normal模式：允许动态VLAN在端口上进行注册，同时会发送静态VLAN和动态VLAN的声明消息。
● Fixed模式：不允许动态VLAN在端口上注册，只发送静态VLAN的声明消息。
● Forbidden模式：禁止该接口动态注册、注销VLAN，同时删除端口上所有VLAN，不发送VLAN的声明消息。

#### 5.3.2 GVRP报文结构

GARP协议报文采用IEEE 802.3 Ethernet封装形式，报文结构如图5-4所示。
图 5-4 GARP 协议报文各个字段的说明如表 GARP协议报文字段含义所示。
表 5-2 GARP 协议报文字段含义

| 字段 | 含义 |
|---|---|
| PDU | 封装在GARP协议报文中的GARP PDU（Protocol Data Unit，协议数据单元）。 |
| Protocol ID | 协议ID，取值为1。 |
| Message | 消息，每个Message由Attribute Type、Attribute List构成。 |
| Attribute Type | 属性类型，由具体的GARP应用定义。取值为0x01时表示VLAN ID，代表GVRP。 |
| Attribute List | 属性列表，由多个属性构成。 |
| Attribute | 属性，每个属性由Attribute Length、Attribute Event、 Attribute Value构成。 |
| Attribute Length | 属性长度，取值为2～255，单位为字节。 |

| 字段 | 含义 |
|---|---|
| Attribute Event | 属性描述的事件，取值及含义为： ● 0：LeaveAll Event ● 1：JoinEmpty Event ● 2：JoinIn Event ● 3：LeaveEmpty Event ● 4：LeaveIn Event ● 5：Empty Event |
| Attribute Value | 属性取值。GVRP的属性取值为VLAN ID，但LeaveAll属性的Attribute Value值无效。 |
| End Mark | 结束标志，取值为0x00。 |

#### 5.3.3 GVRP实现机制

VLAN 属性的单向注册在DeviceA上创建静态VLAN2，通过VLAN属性的单向注册，将DeviceB和DeviceC的相应端口自动加入VLAN2，如图 VLAN属性的单向注册所示。
图 5-5 VLAN 属性的单向注册
1. 在DeviceA上创建静态VLAN2后，Port1启动Join定时器和Hold定时器，等待Hold定时器超时后，DeviceA向DeviceB发送第一个JoinEmpty消息，Join定时器超时后再次启动Hold定时器，再等待Hold定时器超时后，发送第二个JoinEmpty消息。
2. DeviceB上接收到第一个JoinEmpty后创建动态VLAN2，并把接收到JoinEmpty消息的Port2加入到动态VLAN2中，同时告知Port3启动Join定时器和Hold定时器，等待 Hold 定时器超时后向 DeviceC 发送第一个 JoinEmpty 消息， Join 定时器超时后再次启动Hold定时器，Hold定时器超时之后，发送第二个JoinEmpty消息。
DeviceB上收到第二个JoinEmpty后，因为Port2已经加入动态VLAN2，所以不作处理。

3. DeviceC上接收到第一个JoinEmpty后创建动态VLAN2，并把接收到JoinEmpty消
息的Port4加入到动态VLAN2中。DeviceC上收到第二个JoinEmpty后，因为Port4
已经加入动态VLAN2，所以不作处理。
4. 此后，每当LeaveAll定时器超时或收到LeaveAll消息，设备会重新启动LeaveAll定
时器、Join定时器、Hold定时器和Leave定时器。DeviceA的Port1在Hold定时器
超时之后发送第一个JoinEmpty消息，Join定时器超时后再次启动Hold定时器，再
等待Hold定时器超时后，发送第二个JoinEmpty消息，DeviceB向DeviceC发送
JoinEmpty消息的过程也是如此。
VLAN 属性的双向注册
通过上述VLAN属性的单向注册过程，端口Port1、Port2、Port4已经加入VLAN2，但
是Port3还没有加入VLAN2（只有收到JoinEmpty消息或JoinIn消息的端口才能加入动
态VLAN）。为使VLAN2流量可以双向互通，需要进行DeviceC到DeviceA方向的VLAN
属性的注册过程，如图 VLAN属性的双向注册所示。
图 5-6 VLAN 属性的双向注册
1. VLAN属性的单向注册完成后，在DeviceC上创建静态VLAN2（将动态VLAN转换
成静态VLAN），Port4启动Join定时器和Hold定时器，等待Hold定时器超时后，
DeviceC向DeviceB发送第一个JoinIn消息（因为Port4已经注册了VLAN2，所以发
送JoinIn消息），Join定时器超时后再次启动Hold定时器，Hold定时器超时之后，
发送第二个JoinIn消息。
2. DeviceB上接收到第一个JoinIn后，把接收到JoinIn消息的Port3加入到动态VLAN2
中，同时告知 Port2 启动 Join 定时器和 Hold 定时器，等待 Hold 定时器超时后，向
DeviceA发送第一个JoinIn消息，Join定时器超时后再次启动Hold定时器，Hold定
时器超时之后，发送第二个JoinIn消息；DeviceB上收到第二个JoinIn后，因为
Port3已经加入动态VLAN2，所以不作处理。DeviceA上接收到JoinIn之后，停止
向DeviceB发送JoinEmpty消息。此后，当LeaveAll定时器超时或收到LeaveAll消
息，所有设备重新启动LeaveAll定时器、Join定时器、Hold定时器和Leave定时
器。DeviceA的Port1在Hold定时器超时之后就开始发送JoinIn消息。
3. DeviceB向DeviceC发送JoinIn消息。
4. DeviceC收到JoinIn消息后，由于本身已经创建了静态VLAN2，所以不会再创建动
态 VLAN2 。

VLAN 属性的单向注销当设备上不再需要VLAN2时，可以通过VLAN属性的注销过程将VLAN2从设备上删除，如图 VLAN属性的单向注销所示。
图 5-7 VLAN 属性的单向注销
1. 在DeviceA上删除静态VLAN2，Port1启动Hold定时器，等待Hold定时器超时后，DeviceA向DeviceB发送LeaveEmpty消息。LeaveEmpty消息只需发送一次。
2. DeviceB上接收到LeaveEmpty，Port2启动Leave定时器，等待Leave定时器超时之后Port2注销VLAN2，将Port2从动态VLAN2中删除（由于此时VLAN2中还存在端口Port3，所以不会删除VLAN2），同时告知Port3 启动Hold定时器和Leave定时器，等待Hold定时器超时后，向DeviceC发送LeaveIn消息。由于DeviceC的静态VLAN2还没有删除，Port3在Leave定时器超时之前仍然能够收到Port4发送的JoinIn消息，所以DeviceA和DeviceB上仍然能够学习到动态的VLAN2。
3. DeviceC上接收到LeaveIn后，由于DeviceC上存在静态VLAN2，所以Port4不会从VLAN2中删除。
VLAN 属性的双向注销为了彻底删除所有设备上的VLAN2，需要进行VLAN属性的双向注销，如图 VLAN属性的双向注销所示。
图 5-8 VLAN 属性的双向注销

1. 在DeviceC上删除静态VLAN2，Port4启动Hold定时器，等待Hold定时器超时后，
DeviceC向DeviceB发送LeaveEmpty消息。
2. DeviceB接收到LeaveEmpty消息后，Port3启动Leave定时器，等待Leave定时器超
时之后Port3注销VLAN2，将Port3从动态VLAN2中删除并删除动态VLAN2，同时
告知Port2启动Hold定时器，等待Hold定时器超时后，向DeviceA发送
LeaveEmpty消息。
3. DeviceA接收到LeaveEmpty消息后，Port1启动Leave定时器，等待Leave定时器
超时之后Port1注销VLAN2，将Port1从动态VLAN2中删除并删除动态VLAN2。

#### 5.3.4 GVRP组网方式

GVRP特性使得不同设备上的VLAN信息可以由协议动态维护和更新，用户只需要对少数设备进行VLAN配置即可应用到整个交换网络，无需耗费大量时间进行拓扑分析和配置管理。如图5-9所示，所有设备都使能GVRP功能，设备之间相连的端口均为Trunk端口，并允许所有VLAN通过。只需在DeviceA和DeviceC上分别手工配置静态VLAN100～1000，设备DeviceB就可以通过GVRP协议学习到这些VLAN，最后各设备上都存在VLAN100～1000。
图 5-9 典型组网应用

### 5.4 GVRP缺省配置

GVRP的缺省配置如表1所示。
表 5-3 GVRP 缺省配置

| 参数 | 缺省值 |
|---|---|
| GVRP功能 | 全局和接口GVRP功能都处于关闭状态 |
| GVRP接口注册模式 | Normal |
| LeaveAll定时器 | 1000厘秒 |
| Hold定时器 | 10厘秒 |
| Join定时器 | 20厘秒 |
| Leave定时器 | 60厘秒 |

### 5.5 配置GVRP功能

#### 5.5.1 启用GVRP功能

背景信息在启用接口的GVRP功能之前，必须先全局启用GVRP功能。此外，GVRP功能只能配置在Trunk类型的接口上，并且需要通过配置来保证所有动态注册的VLAN都能够从该接口通过。
操作步骤步骤1 进入系统视图。
system-view步骤2 使能全局GVRP功能。
gvrp缺省情况下，未使能全局GVRP功能。
步骤3 进入接口视图。
interface interface-type interface-number步骤4 配置接口为Trunk类型。
port link-type trunk对于S5735I-L-V2，S5735I-S-V2，S5735I-H-V2，S5735-L-V2，S5735E-L-V2，S5735R-L-V2，S5735-S-V2，S5735E-S-V2，S5735R-S-V2，S5735S-L3，S5735S- S3，S1730S-S3系列，缺省情况下，接口的链路类型为negotiation-auto类型。
对于S5732-H-V2，S6780-H，S6750-H，S6750-S，S6750E-S，S6730-H-V2，S6730E-H-V2，S5755-H，S5755-S系列，缺省情况下，接口的链路类型为negotiation-desirable类型。
步骤5 配置将Trunk类型接口加入到指定的VLAN中。
port trunk allow-pass vlan { { { vlan-id1 [ to vlan-id2 ] } &<1-10> } | all }步骤6 使能接口GVRP功能。
gvrp缺省情况下，未使能接口GVRP功能。

说明
● 由于配置VLAN时会触发GVRP消息，如果需要配置的VLAN数量较多，建议逐个设备批量配置同时增加定时器时间，否则有可能造成动态VLAN震荡。
● 如果接口切换到其他链路类型（如Access、Hybrid、dot1q-tunnel等），则用户需要先去使能接口下的GVRP功能。
● STP/RSTP/MSTP/SEP协议的实例0的阻塞接口能阻塞GVRP协议报文，ERPS/Smart Link协议的阻塞接口会阻塞GVRP协议报文。为确保GVRP正常运行并防止GVRP协议成环，建议不要在环网协议的阻塞接口上使能GVRP功能。
● GVRP功能只能运行在MSTP的CIST实例上，并且CIST实例上被MSTP阻塞的端口不能收发GVRP报文。
● 全局GVRP功能与VBST功能互斥。
● 接口GVRP功能与M-LAG互斥。
----结束

#### 5.5.2 （可选）配置GVRP接口注册模式

背景信息GVRP的接口注册模式有三种：
● Normal模式：允许该接口动态注册、注销VLAN，传播动态VLAN以及静态VLAN信息。
● Fixed模式：禁止该接口动态注册、注销VLAN，只传播静态VLAN信息，不传播动态VLAN信息。也就是说被设置为Fixed模式的Trunk接口，即使允许所有VLAN通过，实际通过的VLAN也只能是手动创建的那部分。
● Forbidden模式：禁止该接口动态注册、注销VLAN。也就是说被配置为Forbidden模式的Trunk接口，不允许所有VLAN通过。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤3 配置GVRP接口注册模式。
gvrp registration { fixed | forbidden | normal }缺省情况下，GVRP接口注册模式为Normal模式。
说明配置GVRP接口注册模式之前，需要先使能接口的GVRP功能。
----结束

#### 5.5.3 （可选）配置GARP定时器功能

背景信息GVRP使用GARP协议的标准定时器作为自己的定时器。每个GVRP应用实体启动后，将同时启动LeaveAll定时器，当该定时器超时后，应用实体将对外发送LeaveAll消息，以

使其他应用实体重新注册其实体上所有的属性信息。随后所有设备重新启动LeaveAll定时器，开始新的一轮计时。
在全网有多台设备的情况下，各个设备的LeaveAll定时器的取值可能不相同，但每台设备都将以全网最小的LeaveAll定时器为准发送LeaveAll消息。因为每次LeaveAll定时器超时后发送LeaveAll消息，其它的设备接收到之后都会清零LeaveAll定时器，因此即使全网存在很多不同的LeaveAll定时器，也只有最小的那个LeaveAll定时器起作用。
使用命令garp timer设置接口的GARP定时器时，需要注意以下几点：
● undo garp timer命令用来恢复接口的GARP定时器的值为缺省值。如果缺省值不满足取值范围的要求，则undo garp timer命令无效。
● 各个定时器的取值范围会由于其他定时器取值的改变而改变。如果用户想要设置的定时器的值不在当前可以设置的取值范围内，可以通过改变相关定时器的取值实现。
● 如果用户想恢复各定时器的值为缺省值，可以先恢复Hold定时器的值为缺省值，然后再依次恢复Join、Leave、LeaveAll定时器的值为缺省值。
当需要GVRP动态注册的VLAN数量较多或网络半径较大时，使用缺省定时器值可能会导致VLAN震荡、设备CPU占用率偏高，这时需要相应增大定时器值。对于不同VLAN数目，定时器推荐取值如表 GARP定时器取值与动态注册VLAN数目的对应关系所示。
表 5-4 GARP 定时器取值与动态注册 VLAN 数目的对应关系

|  | 需要动态注册的VLAN数量（N） |  |  |  |
|---|---|---|---|---|
| 定时器类型 | N<=500 | 500<N<=100 0 | 1000<N<=15 00 | N>1500 |
| GARP Hold定时器 | 100厘秒（1秒钟） | 200厘秒（2秒钟） | 800厘秒（8秒钟） | 1000厘秒（10 秒钟） |
| GARP Join定时器 | 600厘秒（6秒钟） | 1200厘秒（12 秒钟） | 4000厘秒（40 秒钟） | 6000厘秒（1 分钟） |
| GARP Leave定时器 | 3000厘秒（30 秒钟） | 6000厘秒（1 分钟） | 20000厘秒（3 分钟20秒） | 30000厘秒（5 分钟） |
| GARP LeaveAll定时器 | 12000厘秒（2 分钟） | 24000厘秒（4 分钟） | 30000厘秒（5 分钟） | 32765厘秒（5 分钟27.65秒） |

操作步骤步骤1 进入系统视图。
system-view步骤2 配置GARP的LeaveAll定时器的值。
garp timer leaveall timer-value缺省情况下， LeaveAll 定时器的值为 1000 厘秒，即 10 秒。
由于接口Leave定时器的值受全局LeaveAll定时器的值限制，所以在配置LeaveAll定时器的值时，需要保证设备上所有配置GARP定时器的接口都是处于正常工作状态。

步骤3 进入接口视图。
interface interface-type interface-number步骤4 配置接口Hold定时器、Join定时器、Leave定时器的值。
garp timer { hold | join | leave } timer-value缺省情况下，Hold定时器的值为10厘秒，Join定时器的值为20厘秒，Leave定时器的值为60厘秒。
----结束

#### 5.5.4 检查配置结果

操作步骤
● 使用命令display gvrp status查看全局GVRP的开启或关闭状态信息。
● 使用命令display gvrp statistics [ interface interface-type interface-number ]查看接口的GVRP统计信息。
● 使用命令 display garp timer [ interface interface-type interface-number ] 查看GARP定时器的值。
----结束

### 5.6 维护GVRP

清除统计信息清除接口的GARP统计信息，包括接口接收、发送和丢弃GVRP数据包的统计信息，如表 清除接口的GARP统计信息所示。
须知清除GARP的统计信息后，以前的信息将无法恢复，务必仔细确认。
表 5-5 清除接口的 GARP 统计信息

| 操作 | 命令 |
|---|---|
| 清除接口的GARP统计信息 | reset garp statistics [ interface interface-type interface-number ] |

### 5.7 GVRP配置举例

#### 5.7.1 举例：配置GVRP功能

组网需求如图5-10所示，公司A总部、公司A的分公司以及公司B之间通过交换设备相连，需要通过GVRP功能，实现VLAN的动态注册。公司A的分公司与总部通过DeviceA和DeviceB互通；公司B通过DeviceB和DeviceC与公司A互通，但只允许公司B配置的VLAN通过。
图 5-10 配置 GVRP 的组网图说明本例中interface1，interface2，分别代表10GE1/0/1，10GE1/0/2。
配置思路采用如下的思路配置GVRP：
1. 使能GVRP功能，实现VLAN的动态注册。
2. 公司A的所有设备配置GVRP功能并配置接口注册模式为Normal，以简化配置。
3. 公司B的所有设备配置GVRP功能并将与公司A相连的接口的注册模式配置为Fixed，以控制只允许公司B配置的VLAN通过。
操作步骤步骤1 全局使能GVRP功能。
\# 配置DeviceA。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] gvrp \# 配置DeviceB。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] gvrp \# 配置DeviceC。

<HUAWEI> system-view [HUAWEI] sysname DeviceC [DeviceC] gvrp步骤2 配置接口为Trunk类型，并允许所有VLAN通过。
\# 配置DeviceA。
[DeviceA] interface 10GE 1/0/1 [DeviceA-10GE1/0/1] port link-type trunk [DeviceA-10GE1/0/1] port trunk allow-pass vlan all [DeviceA-10GE1/0/1] quit [DeviceA] interface 10GE 1/0/2 [DeviceA-10GE1/0/2] port link-type trunk [DeviceA-10GE1/0/2] port trunk allow-pass vlan all [DeviceA-10GE1/0/2] quit DeviceB和DeviceC的配置过程和DeviceA类似，在此不再赘述，具体请参考配置脚本。
步骤3 使能接口的GVRP功能，并配置接口注册模式。
\# 配置DeviceA。
[DeviceA] interface 10GE 1/0/1 [DeviceA-10GE1/0/1] gvrp [DeviceA-10GE1/0/1] gvrp registration normal [DeviceA-10GE1/0/1] quit [DeviceA] interface 10GE 1/0/2 [DeviceA-10GE1/0/2] gvrp [DeviceA-10GE1/0/2] gvrp registration normal [DeviceA-10GE1/0/2] quit DeviceB的配置过程和DeviceA类似，在此不再赘述，具体请参考配置脚本。
\# 配置DeviceC。
[DeviceC] interface 10GE 1/0/1 [DeviceC-10GE1/0/1] gvrp [DeviceC-10GE1/0/1] gvrp registration fixed [DeviceC-10GE1/0/1] quit [DeviceC] interface 10GE 1/0/2 [DeviceC-10GE1/0/2] gvrp [DeviceC-10GE1/0/2] gvrp registration normal [DeviceC-10GE1/0/2] quit步骤4 在Device上创建VLAN101～VLAN200。
\# 配置DeviceA。
[DeviceA] vlan batch 101 to 200 \# 配置DeviceC。
[DeviceC] vlan batch 101 to 200
----结束检查配置结果配置完成后，公司A的分公司用户可以与总部互通，公司A属于VLAN101～VLAN200的用户可以与公司B用户互通。
在DeviceA上使用命令display gvrp status，查看全局GVRP的使能情况，结果如下：
[DeviceA] display gvrp status GVRP status: enabled.

在DeviceA上使用命令display gvrp statistics，查看接口的GVRP统计信息，其中包括：GVRP状态、GVRP注册失败次数、上一个GVRP数据单元源MAC地址和接口GVRP注册类型，结果如下：
[DeviceA] display gvrp statistics GVRP statistics on port 10GE1/0/1 GVRP status : Enabled GVRP registrations failed : 0 GVRP last PDU origin : 0000-0000-0000 GVRP registration type : Normal GVRP statistics on port 10GE1/0/2 GVRP status : Enabled GVRP registrations failed : 0 GVRP last PDU origin : 0000-0000-0000 GVRP registration type : Normal DeviceB和DeviceC的查看方法与DeviceA类似，在此不再赘述。
配置脚本
● DeviceA的配置文件\# sysname DeviceA \# vlan batch 101 to 200 \# gvrp \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 2 to 4094 gvrp \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2 to 4094 gvrp \# return
● DeviceB的配置文件\# sysname DeviceB \# gvrp \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 2 to 4094 gvrp \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2 to 4094 gvrp \# return
● DeviceC的配置文件\# sysname DeviceC \# vlan batch 101 to 200 \# gvrp

\# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 2 to 4094 gvrp gvrp registration fixed \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2 to 4094 gvrp gvrp registration normal \# return
