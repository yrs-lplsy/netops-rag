# S1700, S5700, S6700 V600R024C10 配置指南-以太网交换 01-02 MAC配置

## 2 MAC配置

2 MAC 配置

### 2.1 MAC简介

2.2 MAC原理描述
2.3 MAC配置注意事项
2.4 MAC缺省配置
2.5 配置MAC表项
2.6 配置动态MAC表项的老化时间
2.7 关闭MAC地址学习功能
2.8 配置MAC地址限制
2.9 配置MAC地址防漂移和漂移检测
2.10 配置三层逻辑接口的MAC地址
配置MAC刷新ARP功能
2.11
2.12 配置端口桥功能
2.13 配置丢弃全零MAC地址报文
2.14 配置丢弃匹配不到MAC地址的报文
2.15 配置MAC地址变化定时上报告警功能
2.16 配置 BPDU MAC
2.17 维护MAC表
2.18 MAC配置举例
2.19 MAC常见配置错误
2.1 MAC 简介
定义
MAC（Media Access Control）地址，也称为物理地址、硬件地址或链路地址，由网
络设备制造商生产时写在网卡内部，用来定义网络设备的位置。MAC地址由48比特

长、12位的16进制数字组成，其中从左到右开始，0到23bit是厂商向IETF等机构申请用来标识厂商的代码，24到47bit由厂商自行分派，是各个厂商制造的所有网卡的一个唯一编号。
目的在互联网中，IP地址无法具体标识一个用户，因为IP地址只是逻辑上的标识，任何人都能随意修改。为了解决上述问题，提出了MAC地址，用来唯一标识一个用户。
MAC地址可以分为3种类型：
● 物理MAC地址：这种类型的MAC地址唯一的标识了以太网上的一个终端，该地址为全球唯一的硬件地址。
● 广播MAC地址：全1的MAC地址为广播地址（FF-FF-FF-FF-FF-FF），用来表示LAN上的所有终端设备。
● 组播MAC地址：除广播地址外，第8bit为1的MAC地址为组播MAC地址（例如01-00-00-00-00-00），用来代表LAN上的一组终端。其中以01-80-c2开头的组播MAC地址叫BPDU MAC，一般作为协议报文的目的MAC地址标示某种协议报文。

### 2.2 MAC原理描述

#### 2.2.1 MAC地址表的定义和分类

MAC 地址表的定义MAC地址表记录了设备学习到的其他设备的MAC地址与接口的对应关系，以及接口所属VLAN等信息。设备在转发报文时，根据报文的目的MAC地址查询MAC地址表，如果MAC地址表中包含与报文目的MAC地址对应的表项，则直接通过该表项中的出接口转发该报文；如果MAC地址表中没有包含报文目的MAC地址对应的表项时，设备将采取广播方式在所属VLAN内除接收接口外的所有接口转发该报文。
MAC 地址表的分类MAC地址表中的表项分为：动态MAC表项、静态MAC表项和黑洞MAC表项。
表 2-1 不同 MAC 地址表的特点和作用

| MAC地址表类型 | 特点 | 作用 |
|---|---|---|
| 动态MAC表项 | 由接口通过报文中的源 MAC地址学习获得，表项可老化。在系统复位、单板热插拔或单板复位后，动态表项会丢失。 | 通过查看动态MAC地址表项，可以判断两台相连设备之间是否有数据转发。通过查看指定动态MAC地址表项的个数，可以获取接口下通信的用户数。 |

| MAC地址表类型 | 特点 | 作用 |
|---|---|---|
| 静态MAC表项 | 由用户手工配置，并下发到各单板，表项不可老化。在系统复位、单板热插拔或单板复位后，保存的表项不会丢失。一条静态MAC地址表项，只能绑定一个出接口。接口和MAC地址静态绑定后，其他接口收到源MAC 是该MAC地址的报文将会被丢弃。接口和MAC地址静态绑定后，不会影响该接口动态 MAC地址表项的学习。 | 通过绑定静态MAC地址表项，可以保证合法用户的使用，防止其他用户使用该MAC进行攻击。 |
| 黑洞MAC表项 | 由用户手工配置，并下发到各单板，表项不可老化。在系统复位、单板热插拔或单板复位后，保存的表项不会丢失。配置黑洞MAC地址后，源 MAC地址或目的MAC地址是该MAC的报文将会被丢弃。 | 通过配置黑洞MAC地址表项，可以过滤掉非法用户。 |

#### 2.2.2 MAC地址表的组成和作用

MAC 地址表的组成MAC地址表是以MAC地址和VLAN ID为索引来唯一标识。当一台目的主机属于多个VLAN时，在MAC地址表中就会存在相同MAC地址拥有多个不同VLAN ID的情况。表2-2 中是不同的 MAC 地址表项。如第一条 MAC 地址表项的作用是：从设备任意接口进入的目的MAC为00e0-fc12-1234，VLAN ID为10的报文，都会从interface1接口转发出去。
表 2-2 MAC 地址表项

| MAC地址 | VLAN ID | 出接口 |
|---|---|---|
| 00e0-fc12-1234 | 10 | interface1 |
| 00e0-fc12-5678 | 20 | interface2 |

MAC 地址表的作用MAC地址表用于指导报文进行单播转发。如图2-1中，PC1发往PC3的报文，在到达DeviceA时，根据报文中的目的MAC地址MAC3和VLAN10查询DeviceA的MAC地址表，获取出接口interface3，然后报文直接从接口interface3转发到PC3，完成数据的转发。
图 2-1 基于 MAC 地址表的转发流程图

#### 2.2.3 MAC地址学习和老化

MAC 地址学习过程一般情况下，MAC地址表是设备根据收到的数据帧里的源MAC地址自动学习而建立的。
图 2-2 MAC 地址学习示意图如图2-2，Host1向DeviceA发送数据时，DeviceA从数据帧中解析出源MAC地址（即Host1的MAC地址）和VLAN ID。
● 如果MAC地址表中不存在该MAC地址表项，设备则将这个新MAC地址以及该MAC地址对应的interface1和VLAN ID作为一个新的表项加入到MAC地址表中。
● 如果MAC地址表中已经存在该MAC地址表项，设备将通过重置该表项的老化时间，对该表项进行更新。

说明
● 如果interface1加入了Eth-TrunkA，则MAC地址表项的出接口就是Eth-TrunkA。
● 设备所有接口默认加入VLAN 1，如果不做修改所有MAC地址表项的VLAN ID都是VLAN 1。
● 设备对于BPDU MAC（形如：0180-c200-xxxx）不会进行MAC地址学习。
所以设备在收到数据帧时，才会触发MAC地址的学习和刷新。
MAC 地址老化过程为适应网络的变化，MAC表需要不断更新。MAC表中自动生成的表项（即动态MAC表项）并非永远有效，每一条表项都有一个生存周期，到达生存周期仍得不到更新的表项将被删除，这个生存周期被称作老化时间。如果在到达生存周期前记录被更新，则该表项的老化时间重新计算。
图 2-3 MAC 地址老化过程示意图如图2-3所示，设备MAC地址老化时间设置为T。在t 时刻有源MAC地址为00e0- fc00-0001、VLAN为1的报文从某接口进入。假定该接口已加入VLAN 1。如果之前MAC地址表不存在关于(MAC：00e0-fc00-0001，VLAN：1)的任何种类表项，那么这个地址就会作为动态MAC地址表项学习到地址表里，同时该表项的命中标志位被置1。
设备周期性 ( 每经过 T 时间 ) 地对所有学习到的动态 MAC 地址表项进行检查。
1. 在t 时刻，检查到动态表项(MAC：00e0-fc00-0001，VLAN：1)的命中标志位为1，则将该表项的命中标志位置为0，但不删除这条表项。
2. 在t 时刻和t 时刻之间没有这种报文进入设备，那么该表项的命中标志位会一直保2 3持为0。
3. 在t 时刻，设备检查到该表项的命中标志位为0，认为该表项的老化时间到达，将删除此条表项。
如上所述，通过自动老化，一条动态表项在MAC地址表存在的最短时间是设备所配置的老化时间 T 到 2T 之间。
设备MAC地址老化时间可手动设置。通过设置此时间，可以灵活控制动态学习到的MAC表项在MAC地址表存在的时间。

### 2.3 MAC配置注意事项

依赖License MAC特性无需License许可即可使用。
硬件依赖表 2-3 支持本特性的硬件

| 系列 | 支持产品 |
|---|---|
| S6750-H | S6750-H36C，S6750-H48Y8C |
| S6730E-H-V2 | S6730E-H6FX4Y2CZ-V2 |
| S1730S-S3 | S1730S-S24P4S-A3，S1730S-S24P4X-A3， S1730S-S24T4S-QA3，S1730S-S24T4X-QA3， S1730S-S48P4S-A3，S1730S-S48T4S-A3， S1730S-S48T4X-A3，S1730S-S8P4X-QA3， S1730S-S8T4X-QA3 |
| S5735-S-V2 | S5735-S24HS4XE-V2，S5735-S24P4XE-V2， S5735-S24P4XEZ-V2，S5735-S24P8J4XEZ-V2， S5735-S24PN4XE-V2，S5735-S24ST4XE-V2， S5735-S24T4XE-C-V2，S5735-S24T4XE-V2， S5735-S24T4XEZ-V2，S5735-S24T8J4XE-XA-V2， S5735-S24T8J4XEZ-V2，S5735-S24U4XE-V2， S5735-S48HS4XE-V2，S5735-S48P4XE-V2， S5735-S48P4XEZ-V2，S5735-S48PN4XE-V2， S5735-S48S4XE-V2，S5735-S48T4XE-C-V2， S5735-S48T4XE-V2，S5735-S48T4XE-XA-V2， S5735-S48T4XEZ-V2，S5735-S48U4XE-V2 |
| S5735E-S-V2 | S5735E-S24HS4XE-V2，S5735E-S48HS4XE-V2 |
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
| S5735E-L-V2 | S5735E-L16LP2UM2X-QA-V2，S5735E-L16LP2X- QA-V2，S5735E-L24P4S-A-V2，S5735E-L24P4XE- A-V2，S5735E-L24ST4XE-A-V2，S5735E- L24T4XE-A-V2，S5735E-L48LP4S-A-V2，S5735E- L48LP4XE-A-V2，S5735E-L48S4XE-A-V2， S5735E-L48T4XE-A-V2，S5735E-L8P4X-QA-V2， S5735E-L8T4X-QA-V2 |
| S5755-S | S5755-S24P8J8YZ，S5755-S24P8Y，S5755- S24T8J8YZ，S5755-S24T8Y，S5755-S24U8J8YZ， S5755-S24U8Y，S5755-S48P8Y，S5755- S48P8YZ，S5755-S48T8Y，S5755-S48T8YZ， S5755-S48U8Y，S5755-S48U8YZ |
| S5735R-L-V2 | S5735R-L16LP2S-QA-V2，S5735R-L16LP2UM2X- QA-V2，S5735R-L16LP2X-QA-V2，S5735R- L16T4S-A-V2，S5735R-L16T4X-QA-V2，S5735R- L24P4S-A-V2，S5735R-L24P4X-A-V2，S5735R- L24T4S-A-V2，S5735R-L24T4X-QA-V2，S5735R- L48LP4S-A-V2，S5735R-L48LP4X-A-V2，S5735R- L48P4X-A-V2，S5735R-L48T4S-A-V2，S5735R- L48T4X-A-V2，S5735R-L8P4S-A-V2，S5735R- L8P4X-QA-V2，S5735R-L8T4S-A-V2，S5735R- L8T4X-QA-V2 |

| 系列 | 支持产品 |
|---|---|
| S5735-L-V2 | S5735-L10T4X-A-V2，S5735-L14P2S-QA-V2， S5735-L16LP2UM2X-QA-V2，S5735-L16LP2X-QA- V2，S5735-L16P2UM2X-QA-V2，S5735-L16T4S- A-V2，S5735-L16T4X-QA-V2，S5735- L24LU8S4XE-QA-V2，S5735-L24P4S-A-V2， S5735-L24P4XE-A-V2，S5735-L24PN4XE-A-V2， S5735-L24ST4XE-A-V2，S5735-L24T4S-A-V2， S5735-L24T4X-QA-V2，S5735-L24T4XE-A-V2， S5735-L24T4XE-D-V2，S5735-L24T8J4XE-A-V2， S5735-L48LP4S-A-V2，S5735-L48LP4XE-A-V2， S5735-L48LPN4XE-A-V2，S5735-L48P4XE-A-V2， S5735-L48PN4XE-A-V2，S5735-L48S4X-A-V2， S5735-L48S4XE-A-V2，S5735-L48T4S-A-V2， S5735-L48T4XE-A-V2，S5735-L48T4XE-D-V2， S5735-L8P2T4X-A-V2，S5735-L8P4S-A-V2， S5735-L8P4X-QA-V2，S5735-L8T4S-A-V2， S5735-L8T4X-QA-V2 |
| S5735I-S-V2 | S5735I-S16T2S4XN-V2，S5735I-S16T8S4XE-QD- V2，S5735I-S24T4XE-V2，S5735I-S24T8S4XE-QA- V2，S5735I-S24U4XE-V2，S5735I-S48T4XE-V2， S5735I-S8T4SN-V2，S5735I-S8T4XN-V2，S5735I- S8T8P2S4XN-V2，S5735I-S8U2XN-V2，S5735I- S8U4XN-V2 |
| S5732-H-V2 | S5732-H24S4X6QZ-TV2，S5732-H24S4X6QZ- V2，S5732-H24UM4Y2CZ-KV2，S5732- H24UM4Y2CZ-V2，S5732-H44S4X6QZ-V2， S5732-H48UM4Y2CZ-KV2，S5732-H48UM4Y2CZ- TV2，S5732-H48UM4Y2CZ-V2 |

查询工具如需了解硬件规格、产品部件的配套关系，请点击硬件中心进行查询；如需了解关键规格、全量软件规格，请点击规格查询进行查询。
特性限制表 2-4 本特性的使用限制

| 特性 | 特性限制 |
|---|---|
| MAC约束 | 一条静态MAC地址表项，只能绑定一个出接口。 |
| MAC约束 | 配置MAC-Limit时，超出规格的情况下，命令行等配置可以正常下发，但实际以单板规格限制值生效。 |
| MAC约束 | 一条静态MAC地址表项，只能绑定一个出接口。 |

| 特性 | 特性限制 |
|---|---|
| MAC地址防漂移和漂移 | 在1个广播域（如VLAN或BD）存在1个MAC在多个端口漂移时，记录的 MAC老化后查询漂移记录仍然显示为旧记录在1个广播域（如VLAN或BD）存在多个MAC在不同端口漂移时，如果记录的MAC老化后查询漂移记录仍然显示为旧记录 |
| MAC地址防漂移和漂移 | MAC迁移时可能只有1块单板产生MAC漂移记录。 |
| MAC地址防漂移和漂移 | 1、MAC地址漂移检测功能只能检测单环场景，而对于多环场景，只能检测第一个环。即若一个VLAN内存在两个或多个环，漂移告警中只能上报第一个环的端口信息，不管第一个环上的端口状态是up还是 down。 2、MAC地址漂移检测功能一个老化周期内（默认是5分钟，可以配置）只能检测一个VLAN内的第一个环。例如：一个VLAN内PortA和PortB发生了MAC地址漂移，把其中一个端口down掉后，同一个老化周期内， PortC和PortD又发生MAC地址漂移，则漂移告警中的漂移端口仍然显示 PortA和PortB。 3、当发生MAC地址漂移，并且环路未解除时，如果端口加入Eth-Trunk 接口或者退出Eth-Trunk接口，MAC地址漂移记录中Original-Port和 Move-Ports信息不变。请在环路解除后再清除MAC漂移表项进行重新检测，从而避免重新检测的源端口和漂移端口不准确，误导环路的定位，并且导致惩罚动作（接口Error-Down、接口风暴抑制等）下发到不准确的漂移端口上。 4、环网频繁切换时也可能导致在指定时间内mac move超过指定次数从而触发“mac-address flapping detection”告警，这时建议降低 flapping检测安全等级，或延长环网回切倒换时间。对于产品S5755-S系列，S6750-H系列，S6750-S系列，S6750E-S系列，S6780-H系列，S5755-H24HB2Y2CZ，S5755-H24N4Y-A，S5755- H24P4Y2CZ，S5755-H24T4Y2CZ，S5755-H24U4Y2CZ，S5755- H24UN4Y2CZ，S5755-H24UTM4X4Y2C，S5755-H48N4Y-A，S5755- H48P4Y2CZ，S5755-H48T4Y2CZ，S5755-H48T4Y2CZ-B，S5755- H48U4Y2CZ，S5755-H48UN4Y2CZ，S5755-H48UTM4X4Y2C： 5、L2VPN共享VP方式的子接口（子接口与主接口共享VP），无法漂移。 |
| MAC地址防漂移和漂移 | 1、MAC漂移联动风暴抑制，抑制行为基于物理口生效。物理口上配置的子接口流量也受到抑制。 2、MAC漂移联动风暴抑制不能基于子接口粒度生效。 3、MAC漂移的original端口为可信任端口，风暴抑制和沙箱只针对本板 move端口生效。 4、MAC漂移联动风暴抑制动作区分报文类型处理：未知单播、组播、广播，比如：默认抑制行为为1%的端口速率。具体效果为未知单播、组播、广播三种类型各为1%端口速率。 |
| MAC地址防漂移和漂移 | 设备跨板、跨芯片接口配置mac学习优先级，MAC防漂移功能不生效。 |

| 特性 | 特性限制 |
|---|---|
| MAC管理 | 对于S6750-H系列，S6730E-H-V2系列，S6750E-S系列，S5755-H系列，S6780-H系列，S5732-H-V2系列，S6730-H-V2系列，S5755-S系列，S6750-S系列： 1、本地M-LAG成员端口down时，查询MAC的出接口显示在peerlink或 virtual peerlink接口。 2、从对端设备的孤立端口（未配对的M-LAG成员口）同步过来的MAC 地址显示在peerlink或virtual peerlink接口。 3、通过display mac-address total-number interface查询virtual peerlink接口的MAC统计时不统计M-LAG成员设备同步过来的MAC地址。 4、通过display mac-address total-number interface查询peerlink接口的MAC统计时可以统计M-LAG成员设备同步过来的MAC地址。 |
| MAC管理 | 通过display mac-address total-number查询各单板local MAC数目之和，在单板local MAC同步完成前可能存在MAC重复计数出现显示值与实际值不一致（如跨板Eth-trunk多成员同时收到相同MAC+VLAN流量），只影响计数显示，对流量转发并无影响。 |
| MAC管理 | 1、端口退出VLAN时会基于端口+VLAN批量删除MAC，当VLAN大于10 个，删除类型变更为基于端口批量删除，该端口上其他VLAN的MAC地址也会被删除掉，导致未知单播泛洪。 2、破环协议需要基于端口+VLAN批量删除MAC的场景删除类型变更为基于端口批量删除，该端口上其他VLAN的MAC地址也会被删除掉，导致未知单播泛洪。 |
| MAC管理 | 跨板LAG上使能MAClimit（包括VLAN/BD/子接口/隧道），只限制本板，达到MAClimit限制并告警后当其中某块单板单板上local的MAC低于MAClimit限制值时告警会被撤销，如果还有其他单板的MAC数量达到limit限制则依赖20分钟定时器进行再次告警。举例：跨板LAG使能 BD的MAClimit达到limit限制告警后，如果不同单板上学习的MAC出端口为不同的二层子接口，基于二层子接口删除MAC时会导致告警撤销。 20分钟之后依然处于达到limit的单板会再次上报告警。 |
| MAC管理 | 跨板Eth-Trunk上使能MAClimit只限制本板，达到MAClimit限制并告警后当其中某块单板单板上local的MAC低于MAClimit限制值时告警会被撤销，如果还有其他单板的MAC数量达到limit限制则依赖20分钟定时器进行再次告警。举例：跨板LAG使能VLAN的MAClimit达到limit限制告警后，如果不同单板上学习的MAC出端口为物理接口，基于物理口删除 MAC时会导致告警撤销。20分钟之后依然处于达到limit的单板会再次上报告警。 |
| MAC管理 | 1、通过display mac-address命令查询MAC表时age时间来源于为MAC 软表中记录的时间 2、由于板间同步、软硬表同步导致不同单板上学习到MAC软表时间可能不一致 3、建议基于slot查询MAC表 |
| MAC管理 | 设备收到源MAC是本机系统MAC的流量，无VLANIF三层口的情况下会学习到本机系统MAC。 |

| 特性 | 特性限制 |
|---|---|
| MAC管理 | 1、如果MAC漂移超过10次时，设备会关闭MAC刷新ARP功能。 2、MAC漂移消除后，设备通过1秒定时器检测存在新的MAC漂移表项，则开启MAC刷新ARP功能。 |
| MAC管理 | 对于S6750-H系列，S6730E-H-V2系列，S6750E-S系列，S5755-H系列，S6780-H系列，S5732-H-V2系列，S6730-H-V2系列，S5755-S系列，S6750-S系列： CPU持续冲高或ETH_Q_MACDWN队列持续高水位时，EVPN MAC无法立即删除，需要等待ETH_Q_MACDWN队列降低到一定可用空间进行发起EVPN MAC对账进行恢复。加上硬表MAC删除时间，对账恢复时间约 7min。 |
| MAC管理 | 对于S5735R-L-V2系列，S1730S-S3系列，S5735-L-V2系列，S5735S- L3系列，S5735-S-V2系列，S5735E-S-V2系列，S5735I-S-V2系列， S5735R-S-V2系列，S5735I-L-V2系列，S5735E-L-V2系列，S5735S-S3 系列，S5735I-H-V2系列：基于接口配置的MAC Limit不支持超限告警上报。 |
| MAC管理 | 如果设备上已经存在DHCP Snooping绑定表生成的静态MAC表项类型的表项，那么此MAC表项不能再配置成静态MAC。 |

### 2.4 MAC缺省配置

MAC缺省配置如表2-5所示。
表 2-5 MAC 缺省配置

| 参数 | 缺省值 |
|---|---|
| 动态MAC表项的老化时间 | 300秒 |
| 基于接口、VLAN或流行为的MAC地址学习功能 | 开启 |
| 基于接口或VLAN限制的 MAC地址学习数量 | 不限制 |
| 接口学习MAC地址的优先级 | 0 |
| 相同优先级的接口发生 MAC地址漂移 | 允许 |
| MAC漂移检测功能 | 开启 |
| MAC刷新ARP功能 | 未开启 |
| MAC刷新ND功能 | 开启，不可关闭 |

### 2.5 配置MAC表项

#### 2.5.1 配置静态MAC表项

背景信息设备通过源MAC地址学习自动建立MAC地址表时，无法区分合法用户和非法用户的报文，带来了安全隐患。如果非法用户将攻击报文的源MAC地址伪装成合法用户的MAC地址，并从设备的其他接口进入，设备就会学习到错误的MAC地址表项，于是将本应转发给合法用户的报文转发给非法用户。为了提高安全性，网络管理员可手工在MAC地址表中加入特定MAC地址表项，将用户设备与接口绑定，从而防止非法用户骗取数据。
静态MAC地址表项有如下特性：
● 静态MAC地址表项不会老化，保存后设备重启不会消失，只能手动删除。
● 静态MAC地址表项中指定的VLAN必须已经创建并且已经加入绑定的端口。
● 静态MAC地址表项中指定的MAC地址，必须是单播MAC地址，不能是组播和广播MAC地址。
● 静态MAC地址表项的优先级高于动态MAC地址表项，对静态MAC地址进行漂移的报文会被丢弃。
操作步骤步骤1 进入系统视图。
system-view步骤2 添加静态MAC表项。
● 指定VLAN配置静态MAC表项。
mac-address static mac-address interface-type interface-number vlan vlan-id
● 指定BD配置静态MAC表项。
mac-address static mac-address interface-type interface-number bridge-domain bd-id [ vid pe-vid ]仅S6780-H、S6750-H、S6750-S、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S5732-H-V2系列支持该命令。
● 配置基于 VSI 静态 MAC 地址。
mac-address static mac-address { interface-type interface-number | interface-name } { { vsi vsi-name [ pe-vid pe-vid [ ce-vid ce-vid ] ] } | { vlanif-type vlanif-number | vlanif-name } vsi vsi-name }仅S6730E-H-V2、S6730-H-V2、S5732-H-V2、S5755-H、S6750-H、S6780-
H、S6750E-S、S6750-S系列支持该命令。
----结束检查配置结果
● 执行命令display mac-address static vlan vlan-id [ verbose ]，查看基于VLAN配置的静态MAC表项。
● 执行命令display mac-address static bridge-domain bd-id [ verbose ]，查看基于BD配置的静态MAC表项。

仅S6780-H、S6750-H、S6750-S、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S5732-H-V2系列支持该命令。
● 执行命令display mac-address static { { [ vlan vlan-Id ] | [ interface { porttype portname } ] } * | [ vsi vsiname ] } [ verbose ]，查看基于VSI配置的静态MAC表项。
仅S6730E-H-V2、S6730-H-V2、S5732-H-V2、S5755-H、S6750-H、S6780-
H、S6750E-S、S6750-S系列支持该命令。

#### 2.5.2 配置黑洞MAC表项

背景信息为了防止黑客通过MAC地址攻击用户设备或网络，可将非信任用户的MAC地址配置为黑洞MAC地址，过滤掉非法MAC地址。当设备收到目的MAC或源MAC地址为黑洞MAC地址的报文，且报文携带的VLAN为黑洞MAC对应的VLAN时，直接丢弃。
操作步骤步骤1 进入系统视图。
system-view步骤2 添加黑洞MAC表项。
● 指定VLAN配置黑洞MAC表项。
mac-address blackhole mac-address vlan vlan-id
● 配置全局黑洞MAC表项。
mac-address blackhole mac-address
● 配置基于VSI黑洞MAC表项。
mac-address blackhole mac-address vsi vsi-name仅S6730E-H-V2、S6730-H-V2、S5732-H-V2、S5755-H、S6750-H、S6780-
H、S6750E-S、S6750-S系列支持该命令。
----结束检查配置结果执行命令display mac-address blackhole [ vlan vlan-id ] [ verbose ]，查看指定VLAN的黑洞MAC表项。
执行命令display mac-address blackhole [ vsi vsi-name ] [ verbose ]，查看VSI的黑洞MAC表项。

### 2.6 配置动态MAC表项的老化时间

背景信息动态MAC表项不需要手工创建，表项可老化。用户可以配置动态MAC表项的老化时间。
● 如果用户配置的老化时间过长，设备会保存许多过时的MAC地址，从而耗尽MAC地址表资源，导致设备无法学习新的MAC地址。

● 如果用户配置的老化时间太短，设备过早地删除MAC地址，导致设备广播大量的
数据报文，增加网络的负担。
请用户需要根据实际情况，配置合适的老化时间。例如网络比较稳定，可以将老化时
间配置得长一些，防止设备突然广播大量的数据报文，造成安全隐患。
操作步骤
步骤1 进入系统视图。
system-view
步骤2 配置动态MAC表项的老化时间。
mac-address aging-time timeValue
缺省情况下，动态MAC地址表项的老化时间是300秒。0表示动态MAC地址表项不被老
化。
----结束
检查配置结果
执行命令display mac-address aging-time，查看动态MAC表项的老化时间。

### 2.7 关闭MAC地址学习功能

#### 2.7.1 了解关闭MAC地址学习

开启MAC地址学习功能时，收到来自周边设备的以太网帧，解析出源MAC地址，结合接收该以太网帧的接口，在MAC地址表项中添加新表项。以后设备接收到去往该目的MAC地址的以太网帧时，则直接查询MAC地址表项就可以得到正确的发送接口，可以避免广播。
由于MAC地址表的容量是有限的，当黑客伪造大量源MAC地址不同的报文发送到设备后，设备上的MAC地址表项资源可能会被耗尽。当MAC表被填满后，即使它再收到正常的报文，也无法学习到报文中的源MAC地址，导致报文广播转发，浪费带宽资源。
关闭MAC地址学习功能可以有效防止这种攻击。
说明MAC地址学习限制规则对已经上线的用户不生效，对新上线的用户生效。
如表2-6所示，可以采用如下方式关闭MAC地址学习。
表 2-6 关闭 MAC 地址学习方式说明

| 关闭MAC地址学习方式 | 描述 |
|---|---|
| 基于接口关闭MAC地址学习 | 某个接口关闭MAC地址学习后，将不再自动学习到新的动态MAC地址表项。之前学习到的动态表项在老化时间到达后自动删除。 |

| 关闭MAC地址学习方式 | 描述 |
|---|---|
| 基于VLAN关闭MAC地址学习 | 某个VLAN关闭MAC地址学习后，该 VLAN下的接口将不再自动学习到新的动态MAC地址表项。之前学习到的动态表项在老化时间到达后自动删除。 |
| 基于BD关闭MAC地址学习 | 某个BD关闭MAC地址学习后，该BD下的接口将不再自动学习到新的动态MAC地址表项。之前学习到的动态表项在老化时间到达后自动删除。 |
| 基于流行为关闭MAC地址学习 | 基于流行为关闭MAC地址学习后，匹配到流策略时，接口下不学习到新的动态 MAC地址表项。之前学习到的动态表项在老化时间到达后自动删除。 |

#### 2.7.2 配置基于接口关闭MAC地址学习

背景信息为提高设备的安全性，可以基于接口关闭MAC地址学习。例如某接口固定与某台服务器相连，可以在该接口上配置该服务器的静态MAC地址，且关闭该接口的MAC地址学习功能，指定动作为丢弃。这样其他服务器或终端将无法通过该接口通信，增强了网络的稳定性和安全性。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入以太接口视图。
interface interface-type interface-number步骤3 将接口从三层模式切换到二层模式。请根据当前接口模式自行选择是否要执行此步骤。
portswitch仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 关闭MAC地址学习功能。
mac-address learning disable [ action { discard | forward } ]关闭MAC地址学习功能的缺省动作为forward，即对报文按照MAC地址表项进行转发，如果没有对应的MAC地址表项，则广播该报文。当配置动作为discard时，会对报文的源 MAC 地址进行匹配，当接口和 MAC 地址与 MAC 地址表项匹配时，对该报文进行转发；当接口和MAC地址与MAC地址表项不匹配时，丢弃该报文。
----结束

检查配置结果执行命令display current-configuration interface interface-type interface- number，查看基于接口关闭MAC地址学习的功能是否配置成功。

#### 2.7.3 配置基于VLAN关闭MAC地址学习

背景信息网络环境固定的情况下，为提高设备的安全性，可以基于VLAN关闭MAC地址学习。关闭后，设备将不会再从该VLAN学习新的MAC地址，这样将无法通过该VLAN通信，增强了网络的稳定性和安全性。
操作步骤步骤1 进入系统视图。
system-view步骤 2 进入 VLAN 视图。
vlan vlan-id步骤3 关闭MAC地址学习功能。
mac-address learning disable缺省情况下，MAC地址学习功能处于打开状态。
----结束检查配置结果执行命令display vlan [ vlan-id [ verbose ] ]，查看基于VLAN关闭MAC地址学习的功能是否配置成功。

#### 2.7.4 配置基于BD关闭MAC地址学习

背景信息网络环境固定的情况下，为提高设备的安全性，可以基于BD关闭MAC地址学习。关闭后，设备将不会再从该BD学习新的MAC地址，这样将无法通过该BD通信，增强了网络的稳定性和安全性。
说明该配置仅S6780-H、S6750-H、S6750-S、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755-
H、S5755-S、S5732-H-V2系列支持。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入BD视图。
bridge-domain bd-id

步骤3 关闭MAC地址学习功能。
mac-address learning disable缺省情况下，MAC地址学习功能处于打开状态。
----结束检查配置结果执行命令display bridge-domain [ binding-info | bd-id [ verbose | brief | binding- info ] ]，查看基于BD关闭MAC地址学习的功能是否配置成功。

#### 2.7.5 配置基于VSI关闭MAC地址学习

背景信息去使能基于VSI的MAC地址学习能力，可以将VPLS模拟成VPWS。例如，当只有两台PE，PE下只有一台CE时，可以去使能PE的MAC地址学习能力，减轻PE学习MAC地址的压力。
说明该配置仅S6780-H、S6750-H、S6750E-S、S6750-S、S6730E-H-V2、S6730-H-V2、S5755-
H、S5732-H-V2系列支持。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入VSI视图。
vsi vsi-name [ static | auto ]同一设备上不同VSI实例的名称不能相同。
步骤3 关闭MAC地址学习功能。
mac-learning disable缺省情况下，设备使能 MAC 地址学习能力。
说明执行mac-learning disable命令后，将不能自动学习MAC地址，报文将在网络内广播，请慎重使用。
----结束检查配置结果执行命令display mac-address [ mac-address ] [ vlan vlan-id | vsi vsi-name ] [ verbose ]，查看MAC地址表项信息。

#### 2.7.6 配置基于流行为关闭MAC地址学习

背景信息基于流行为禁止MAC地址学习功能，主要应用在以下场景：
● 在网络比较稳定、报文的MAC地址相对固定的情况下，设备没有必要继续学习其他所有报文的MAC地址。此时通过应用流策略，对策略下所有流分类禁止MAC地址学习功能，既可以节省MAC地址表项开支，也可以提高设备的运行效率。
● 某些非法用户有时会采用频繁变换MAC地址的方式对网络进行攻击，此时通过应用流策略，对策略下所有流分类禁止MAC地址学习功能，可以避免此类攻击所造成的设备MAC地址表项溢出的问题，保护设备性能不受影响。
操作步骤步骤1 配置流分类。

| 步骤 | 命令 |
|---|---|
| 进入系统视图 | system-view |
| 创建一个流分类并进入流分类视图，或进入已存在的流分类视图 | traffic classifier classifier-name [ type { and | or } ] |
| 定义流分类中的匹配规则流分类中可定义的规则有很多种，详细内容可参见《CLI配置指南-QoS配置- MQC配置》 | if-match |
| 退出流分类视图 | quit |

步骤2 配置流行为。

| 步骤 | 命令 |
|---|---|
| 创建一个流行为，进入流行为视图 | traffic behavior behavior-name |
| 在流行为视图下配置禁止MAC地址学习功能 | mac-address learning disable |
| 退出流行为视图 | quit |

步骤3 配置流策略。

| 步骤 | 命令 |
|---|---|
| 创建一个流策略并进入流策略视图，或进入已存在的流策略视图 | traffic policy policy-name |
| 在流策略中为指定的流分类配置所需流行为，即绑定流分类和流行为 | classifier classifier-name behavior behavior-name [ precedence precedence-value ] |

| 步骤 | 命令 |
|---|---|
| 退出流策略视图 | quit |

步骤4 应用流策略。请根据实际情况选择应用流策略方式。

| 步骤 |  | 命令 |
|---|---|---|
| 在接口上应用流策略 | 进入二层接口视图 | interface interface-type interface- number |
|  | 在接口上应用流策略 | traffic-policy policy-name inbound |
| 在 VLA N上应用流策略 | 进入VLAN视图 | vlan vlan-id |
|  | 在VLAN上应用流策略 | traffic-policy policy-name inbound |
| 在全局应用流策略 |  | traffic-policy policy-name global [ slot slot-id ] inbound |

----结束
检查配置结果
执行命令display traffic behavior [ behavior-name ]，查看基于流行为禁止MAC地
址学习的功能是否配置成功。

### 2.8 配置MAC地址限制

#### 2.8.1 了解MAC地址限制

一些安全性较差的网络容易受到黑客的MAC地址攻击，由于MAC地址表的容量是有限的，当黑客伪造大量源MAC地址不同的报文并发送给设备后，设备的MAC表项资源就可能被耗尽。当MAC表被填满后，即使它再收到正常的报文，也无法学习到报文中的源MAC地址。
MAC地址限制功能可以限制MAC地址学习数量，当超过限制数时不再学习MAC地址，同时可以配置当 MAC 地址数达到限制后对报文采取的动作，从而防止 MAC 地址表资源耗尽，提高网络安全性。
用户可以根据实际情况选择配置：

● 基于接口的MAC地址限制：针对单个接口进行MAC地址限制。
● 基于VLAN的MAC地址限制：针对VLAN下的多个接口进行MAC地址限制。
● 基于BD的MAC地址限制：针对BD下的多个接口进行MAC限制。
● 基于VSI的MAC地址限制：针对VSI下的多个接口进行MAC限制。

#### 2.8.2 配置基于接口的MAC地址限制

背景信息配置基于接口的MAC地址限制，当MAC地址表项达到限制数时，该接口将不能再学习新的MAC地址表项，同时可以配置当MAC地址数达到限制后对报文采取的动作，确定是否丢弃源MAC地址不包含在MAC地址表中的报文。
说明为保证配置的MAC地址学习限制规则的数量限制准确，请在配置此功能前先使用reset mac- address命令清除已经学习到的MAC地址。
第一次执行mac-address limit命令时，必须先配置mac-address limit maximum后，才能配置action和alarm参数，之后执行mac-address limit命令，将无配置次序要求。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤3 将接口从三层模式切换到二层模式。请用户根据实际接口类型自行选择是否要执行此步骤。
portswitch仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 限制MAC地址学习数量。
mac-address limit maximum max缺省情况下，没有配置MAC地址学习数量。
步骤5 当MAC地址数达到限制后，对报文应采取的动作。
mac-address limit action { discard | forward } MAC地址数达到限制后，对报文应采取的缺省动作为discard，即报文被丢弃。当配置动作为forward时，源MAC为新MAC地址的报文继续被转发，但是MAC地址表项不记录。
步骤6 配置当MAC地址数达到限制后是否进行告警。
mac-address limit alarm { disable | enable } MAC地址数达到限制后，系统默认发送告警。
----结束

检查配置结果执行命令display mac-address limit [ interface-type interface-number ]，查看MAC地址学习限制规则。

#### 2.8.3 配置基于VLAN的MAC地址限制

背景信息配置基于VLAN的MAC地址限制，当MAC地址表项达到限制数时，该VLAN下的接口将不能再学习新的MAC地址表项，同时可以配置当MAC地址数达到限制后对报文采取的动作，确定是否丢弃源MAC地址不包含在MAC地址表中的报文。
说明为保证配置的MAC地址学习限制规则的数量限制准确，请在配置此功能前先使用reset mac- address命令清除已经学习到的MAC地址。
第一次执行mac-address limit命令时，必须先配置mac-address limit maximum后，才能配置action和alarm参数，之后执行mac-address limit命令，将无配置次序要求。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入VLAN视图。
vlan vlan-id步骤3 限制MAC地址学习数量。
mac-address limit maximum max缺省情况下，没有配置MAC地址学习数量。
步骤4 当MAC地址数达到限制后，对报文应采取的动作。
mac-address limit action { discard | forward } MAC地址数达到限制后，对报文应采取的缺省动作为forward，源MAC为新MAC地址的报文继续被转发，但是MAC地址表项不记录。
步骤5 配置当MAC地址数达到限制后是否进行告警。
mac-address limit alarm { disable | enable } MAC 地址数达到限制后，系统默认发送告警。
----结束检查配置结果执行命令display mac-address limit [ vlan vlan-id ]，查看MAC地址学习限制规则。

#### 2.8.4 配置基于BD的MAC地址限制

背景信息配置基于BD的MAC地址限制，当MAC地址表项达到限制数时，该BD下的接口将不能再学习新的MAC地址表项，同时可以配置当MAC地址数达到限制后对报文采取的动作，确定是否丢弃源MAC地址不包含在MAC地址表中的报文。
说明该配置仅S6780-H、S6750-H、S6750-S、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755-
H、S5755-S、S5732-H-V2系列支持。
说明为保证配置的MAC地址学习限制规则的数量限制准确，请在配置此功能前先使用reset mac- address命令清除已经学习到的MAC地址。
第一次执行mac-address limit命令时，必须先配置mac-address limit maximum后，才能配置action和alarm参数，之后执行mac-address limit命令，将无配置次序要求。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入BD视图。
bridge-domain bd-id步骤3 限制MAC地址学习数量。
mac-address limit maximum max缺省情况下，没有配置MAC地址学习数量。
步骤4 当MAC地址数达到限制后，对报文应采取的动作。
mac-address limit action { discard | forward } MAC地址数达到限制后，对报文应采取的缺省动作为forward，源MAC为新MAC地址的报文继续被转发，但是MAC地址表项不记录。
步骤5 配置当MAC地址数达到限制后是否进行告警。
mac-address limit alarm { disable | enable } MAC地址数达到限制后，系统默认发送告警。
----结束检查配置结果执行命令display mac-address limit [ bridge-domain bd-id ]，查看MAC地址学习限制规则。

#### 2.8.5 配置基于VSI的MAC地址限制

背景信息在网络中MAC地址表的容量有限，当黑客伪造大量源MAC地址不同的报文发送攻击时，设备的动态MAC地址表就可能被填满。当动态MAC地址表被填满后，即使设备再

收到合法报文，也无法学习到报文中的源MAC地址。配置基于VSI的MAC地址限制可以控制接入用户数量，当超过限制数量时不再学习MAC地址，同时可以配置丢弃报文动作，防止MAC地址攻击，提高网络安全性。
说明该配置仅S6780-H、S6750-H、S6750E-S、S6750-S、S6730E-H-V2、S6730-H-V2、S5755-
H、S5732-H-V2系列支持。
说明为保证配置的MAC地址学习限制规则的数量限制准确，请在配置此功能前先使用reset mac- address命令清除已经学习到的MAC地址。
第一次执行mac-address limit命令时，必须先配置mac-address limit maximum后，才能配置action和alarm参数，之后执行mac-address limit命令，将无配置次序要求。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入VSI视图。
vsi vsiname步骤3 限制MAC地址学习数量。
mac-address limit maximum maxValue缺省情况下，没有配置MAC地址学习数量。
步骤4 当MAC地址数达到限制后，对报文应采取的动作。
mac-address limit action { discard | forward } MAC地址数达到限制后，对报文应采取的缺省动作为discard，源MAC为新MAC地址的报文将被丢弃。
步骤5 配置当MAC地址数达到限制后是否进行告警。
mac-address limit alarm { disable | enable } MAC地址数达到限制后，系统默认发送告警。
----结束检查配置结果执行命令display mac-address limit vsi vsiname，查看VSI的MAC地址学习限制规则。

### 2.9 配置MAC地址防漂移和漂移检测

#### 2.9.1 了解MAC地址漂移

什么是 MAC 地址漂移MAC地址漂移是指设备上一个VLAN内有两个或者三个端口学习到同一个MAC地址，后学习到的MAC地址表项覆盖原MAC地址表项的现象。通常认为第一个学习到MAC地

址的接口是正确的出接口，称为源端口（Original Port），后学习的端口是漂移端口（Move Port），漂移端口通常是在环路上或者下挂网络中有环路的端口。图2-4所示，MAC地址为00e0-fc12-3456，VLAN ID为2的表项，出接口由interface1刷新为interface2，这就是MAC地址漂移。设备出现MAC地址漂移时，设备CPU占用率会有不同程度的升高。
正常情况下，网络中不会在短时间内出现大量MAC地址漂移的情况。出现这种现象一般都意味着网络中存在环路或非法用户进行网络攻击，可以通过查看告警信息和漂移记录，快速定位和排除环路。
图 2-4 MAC 地址漂移示意图如何防止 MAC 地址漂移在规划网络时，可以通过下面两种方式来避免MAC地址漂移：
● 提高接口MAC地址学习优先级。当不同接口学到相同的MAC地址表项时，高优先级接口学到的MAC地址表项可以覆盖低优先级接口学到的MAC地址表项，防止MAC地址在接口间发生漂移。
● 不允许相同优先级的接口发生MAC地址表项覆盖。当伪造网络设备所连接口的优先级与安全的网络设备相同时，后学习到的伪造网络设备的MAC地址表项不会覆盖之前正确的表项。但如果网络设备下电，仍会学习到伪造网络设备的MAC地址，当网络设备再次上电时将无法学习到正确的MAC地址。
如图2-5所示，为防止非法用户伪造服务器MAC地址入侵DeviceA，可以提高服务器侧接口Port1的MAC地址学习优先级。
图 2-5 MAC 防漂移应用组网图

如何进行 MAC 地址漂移检测MAC地址漂移检测是利用MAC地址出接口跳变的现象，检测MAC地址是否发生漂移的功能。
配置MAC地址漂移检测功能后，在发生MAC地址漂移时，可以上报包括MAC地址、VLAN，以及跳变的接口等信息的告警。其中跳变的接口即为可能出现环路的接口。网络管理员可以根据告警信息，手工排查网络中环路的源头，也可以使用MAC漂移检测提供的后续动作，使跳变的端口down或者VLAN从端口中退出，实现自动破环。
图 2-6 MAC 地址漂移检测组网图如图2-6网络中，若DeviceC和DeviceD之间误接网线，则DeviceB、DeviceC、DeviceD之间形成环路。当DeviceA上interface1接口从网络中收到一个广播报文后转发给DeviceB，该报文经过环路，会被DeviceA上interface2接口收到。配置MAC地址漂移检测功能，DeviceA就会感知到MAC地址出接口跳变的现象。若连续出现此现象，DeviceA就会上报MAC漂移告警，提醒用户进行维护。
MAC 地址漂移后的处理机制接口发生MAC地址漂移后，设备会自动触发广播和未知单播的流量抑制，使得发生漂移的出接口转发速率为入接口带宽的1%，用户可以执行storm suppression mac- address flapping命令使接口下MAC漂移联动流量抑制的阈值按照cir进行灵活的配置，并可以使报文强制按照MAC漂移联动流量抑制的阈值进行转发。
用户还可以配置发生漂移后接口Error-Down功能。当检测到发生MAC地址漂移，接口将会被Error-Down并上报告警。

#### 2.9.2 配置MAC地址防漂移

背景信息可以通过两种方式来配置MAC地址防漂移：
● 提高接口MAC地址学习优先级
● 不允许相同优先级的接口发生MAC地址漂移操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤 3 将接口从三层模式切换到二层模式。请根据当前接口模式自行选择是否要执行此步骤。
portswitch仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 配置接口学习MAC地址的优先级。
mac-address learning priority priority-id缺省情况下，接口学习MAC地址的优先级为0。取值范围是0～3，数值越大优先级越高。
步骤5 返回系统视图。
quit步骤6 配置不允许相同优先级的接口发生MAC地址漂移。
undo mac-address learning priority priority-id allow-flapping缺省情况下，允许相同优先级的接口发生MAC地址漂移。
---- 结束

#### 2.9.3 配置MAC地址漂移检测

背景信息配置MAC地址漂移检测功能可以检测到设备上所有的MAC地址是否发生了漂移。若发生漂移，设备会上报告警到网管系统。同时可以在设备上执行命令display mac- address flapping active-table查看MAC漂移的活动记录以及执行display mac- address flapping aged-table 命令查看 MAC 漂移老化记录。

说明
● 当端口发生MAC地址漂移后，系统会触发广播、组播和未知单播的流量抑制，使得发生漂移的出接口转发速率为入接口带宽的1%（用户可以执行storm suppression mac-address flapping命令使接口下MAC漂移联动流量抑制的阈值按照cir进行灵活的配置，并可以使报文强制按照MAC漂移联动流量抑制的阈值进行转发）。此时用户需要排查网络中是否存在环路。以下情况不会因为MAC漂移触发流量抑制：
● 当接口配置了相应报文类型的风暴控制或者流量抑制功能。例如执行命令storm suppression broadcast配置接口下允许通过的最大广播报文的流量，那么当发生MAC地址漂移后，系统不会自动触发广播流量抑制。
● 如果MAC地址漂移到peer-link接口上，则MAC漂移联动流量抑制功能在peer-link接口上不会生效。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置全局MAC地址漂移检测功能。
mac-address flapping detection [ security-level { low | middle | high }]缺省情况下，已经配置了全局MAC地址漂移检测功能，检测安全级别为中级别，即MAC地址发生10次迁移后系统认为发生了MAC地址漂移。
步骤3 （可选）配置MAC地址漂移检测的VLAN白名单，即指定不检测的VLAN。
mac-address flapping detection exclude vlan { vlan-id1 [ to vlan-id2 ] } &<1-10>缺省情况下，未配置MAC地址漂移检测的VLAN白名单。
步骤4 （可选）将指定MAC加入MAC漂移检测白名单，即不检测该MAC。
mac-address flapping detection exclude mac-address mac-address-mask缺省情况下，没有指定MAC加入MAC漂移检测白名单。
步骤5 （可选）配置MAC地址漂移表项的老化时间。
mac-address flapping aging-time aging-time缺省情况下，MAC地址漂移表项的老化时间为300秒。
步骤6 （可选）配置MAC地址漂移定时上报Trap的时间间隔。
1. 使能MAC漂移定时上报Trap功能。
mac-address flapping periodical trap enable缺省情况下，MAC地址漂移定时上报Trap功能处于未开启。
2. 配置MAC地址漂移定时上报Trap的时间间隔。
mac-address flapping periodical trap interval interval缺省情况下，MAC地址漂移定时上报Trap的时间间隔是2分钟。
步骤7 （可选）配置发生漂移后接口的处理动作。
1. 进入接口视图。
interface interface-type interface-number
2. 将接口从三层模式切换到二层模式。请根据当前接口模式自行选择是否要执行此步骤。
portswitch

仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
3. 配置发生MAC地址漂移后触发接口Error-Down。
mac-address flapping trigger error-down缺省情况下，没有配置发生MAC地址漂移后触发接口Error-Down。
----结束检查配置结果执行命令display mac-address flapping [ slot slot-id ] [ begin datetime hourtime ]，查看MAC地址漂移的配置信息。
后续处理配置发生MAC地址漂移后触发接口Error-Down后，如果检测到发生MAC地址漂移，接口将会被 Error-Down 并上报告警。 Error-Down 是指设备检测到故障后将接口状态设置为ERROR DOWN状态，此时接口不能收发报文，接口指示灯为常灭。可以通过display error-down recovery命令可以查看设备上所有被Error-Down的接口信息。
接口被Error-Down时，建议先排除引起接口Error-Down的原因。有以下两种方式可以恢复接口状态：
● 手动恢复（Error-Down发生后）
当处于Error-Down状态的接口数量较少时，可在该接口视图下依次执行命令shutdown和undo shutdown，或者执行命令restart，重启接口。
● 自动恢复（Error-Down发生前）
如果处于Error-Down状态的接口数量较多，逐一手动恢复接口状态将产生大量重复工作，且可能出现部分接口配置遗漏。为避免这一问题，用户可在系统视图下执行命令error-down auto-recovery cause mac-address-flapping interval interval-value使能接口状态自动恢复为Up的功能，并设置接口自动恢复为Up的延时时间。可以通过display error-down recovery查看接口状态自动恢复信息。
说明此方式对已经处于Error-Down状态的接口不生效，只对配置该命令后进入Error-Down状态的接口生效。

### 2.10 配置三层逻辑接口的MAC地址

背景信息缺省情况下，三层接口的接口MAC是从系统MAC范围段中动态分配的。对于三层物理接口，接口MAC不可以重新指定；但对于三层逻辑接口，支持重新配置接口MAC。
说明该配置仅S6780-H、S6750-H、S6750-S、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755-
H、S5755-S、S5732-H-V2系列支持。

操作步骤步骤1 进入系统视图。
system-view步骤2 进入相应的三层逻辑接口视图。
interface interface-type interface-number如果Eth-Trunk接口是二层口，需要执行undo portswitch命令设置成三层口。
步骤3 配置接口MAC。
mac-address mac-address
----结束

### 2.11 配置MAC刷新ARP功能

背景信息在以太网中，主机设备是根据 MAC 地址来发送、接收以太网数据帧。 ARP 用于提供 IP地址到MAC地址的映射。当不同网段间通信时，需要使用ARP表项来将IP地址映射到正确的MAC地址及相应的出接口上。
一般来说设备上的MAC表项和ARP表项的出接口是一致的。如图2-7所示，在T1时间点，MAC地址表项和ARP表项的出接口是一致的，都是interface1。当端口切换后，在T2时间点，MAC地址表项的出接口在收到报文时立即刷新为interface2，但是ARP表项的出接口还是interface1，需要等待T3时间点即ARP表项的老化时间到达后，通过ARP老化探测，才会刷新为interface2。这样就在T2时间点和T3时间点之间，ARP表项的出接口是不可用的，会导致不同网段间设备的通信中断。
图 2-7 配置 MAC 刷新 ARP 功能之前MAC刷新ARP可以实现在MAC出接口更新时，直接刷新ARP表项的出接口的功能。如图2-8所示，在配置MAC刷新ARP功能后，在T2时间点，MAC地址表项出接口刷新为interface2后，直接把ARP表项的出接口刷新为interface2。解决了T2时间点和T3时间点之间，ARP表项出接口不可用的问题，避免了业务通信的中断。

图 2-8 配置 MAC 刷新 ARP 功能之后操作步骤步骤1 进入系统视图。
system-view步骤2 配置MAC刷新ARP功能。
mac-address update arp enable缺省情况下，设备未开启MAC刷新ARP功能。
说明该命令只对动态ARP表项生效，不会更新静态ARP表项。
使用arp anti-attack entry-check { fixed-mac | fixed-all | send-ack } enable命令配置ARP表项固化功能后，MAC刷新ARP功能不生效。
开启了MAC刷新ARP功能后，只有MAC表项的出接口发生变化，才会更新对应的ARP表项。
----结束检查配置结果执行命令display current-configuration，查看MAC刷新ARP功能是否配置成功。若存在undo mac-address update arp enable配置，说明设备没有配置MAC刷新ARP功能，若不存在undo mac-address update arp enable配置，说明设备成功配置了MAC刷新ARP功能。

### 2.12 配置端口桥功能

背景信息配置端口桥功能的目的是实现对同源同宿报文的转发。同源同宿报文即源MAC地址和目的MAC地址均在设备的同一接口上学习到的报文。缺省情况下，设备不转发同源同宿报文，当接口收到这种报文时，设备判断为非法报文并直接丢弃该报文。配置端口桥功能后，当接口收到同源同宿报文时，若设备上的MAC地址表中存在与该报文的目的MAC地址对应的表项，则将报文从本接口转发出去。
操作步骤步骤1 进入系统视图。
system-view

步骤2 进入接口视图。
interface interface-type interface-number步骤3 将接口从三层模式切换到二层模式。请用户根据实际接口类型自行选择是否要执行此步骤。
portswitch仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 配置端口桥功能。
port bridge enable缺省情况下，没有配置端口桥功能。
----结束

### 2.13 配置丢弃全零MAC地址报文

背景信息网络中存在一些老的主机或设备，当这些主机或设备的网卡发生故障时可能会向网络中发送源MAC地址或目的MAC地址是全0非法MAC的报文。为避免当前设备收到这些报文，可以为其配置丢弃全0MAC地址报文的功能。配置该功能后，当设备收到源MAC或目的MAC地址为全0非法MAC地址的报文时，会丢弃该报文。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置设备丢弃全0非法MAC地址报文。
drop illegal-mac enable缺省情况下，设备不丢弃全0非法MAC地址报文。
----结束

### 2.14 配置丢弃匹配不到MAC地址的报文

背景信息当DHCP用户下线后，用户的MAC地址表项会老化。如果有转发到此用户的流量，在设备上找不到目的MAC地址表项，会将报文广播到此VLAN下所有接口，其他的用户都能接收到该流量，对安全造成影响。配置丢弃匹配不到MAC地址的报文功能后，不仅可以降低设备的负荷，同时安全也得到了保证。
操作步骤步骤1 进入系统视图。
system-view

步骤2 进入VLAN视图。
vlan vlan-id步骤3 配置设备丢弃匹配不到MAC地址的报文。
mac-address miss action discard缺省情况下，设备会在VLAN内广播匹配不到MAC地址的报文。
----结束

### 2.15 配置MAC地址变化定时上报告警功能

背景信息当用户需要了解MAC地址的变化情况时，可配置设备学习到MAC地址或MAC地址发生老化时发送告警的功能。
操作步骤步骤1 进入系统视图。
system-view步骤2 （可选）配置设备对MAC地址发生学习或老化的检查周期。
mac-address notification interval interval-time缺省情况下，设备对MAC地址发生学习或老化的检查周期为10秒。
步骤3 （可选）配置设备对动态MAC定时上报周期。
mac-address notification full-report interval interval-time缺省情况下，设备对动态MAC定时上报的周期为1440分钟。
该步骤仅在S5735E-S-V2，S5735-S-V2，S5735I-L-V2，S5735I-S-V2，S5735I-H- V2，S5735R-L-V2，S5735R-S-V2，S5735E-L-V2，S5735-L-V2，S5735S-L3，S5735S-S3，S1730S-S3产品上支持。
步骤4 进入接口视图。
interface interface-type interface-number步骤5 将接口从三层模式切换到二层模式。请根据当前接口模式自行选择是否要执行此步骤。
portswitch仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤6 配置MAC地址学习或老化的告警功能。
mac-address notification { aging | learning | all }缺省情况下，未配置MAC地址学习或老化的告警功能。
----结束

### 2.16 配置BPDU MAC

背景信息缺省情况下设备对于BPDU帧不做二层转发，当需要对其他厂商私有协议报文按BPDU帧处理时，把这些报文的MAC配置成BPDU MAC，这样设备就会丢弃这些使用BPDU MAC的报文。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置BPDU MAC。
mac-address bpdu mac-address [ mac-address-mask ]缺省情况下，设备默认存在以下BPDU MAC：
● 0180-c200-008a ffff-ffff-ffff
● 0180-c200-8585 ffff-ffff-ffff
● 010f-e200-0001 ffff-ffff-ffff
● 0100-0ccc-cccc ffff-ffff-ffff
● 0180-c200-0000 ffff-ffff-ffff
● 0180-c200-0001 ffff-ffff-ffff
● 0180-c200-0002 ffff-ffff-ffff
● 0180-c200-0003 ffff-ffff-ffff
● 0180-c200-0004 ffff-ffff-ffff
● 0180-c200-0005 ffff-ffff-ffff
● 0180-c200-0006 ffff-ffff-ffff
● 0180-c200-0007 ffff-ffff-ffff
● 0180-c200-0008 ffff-ffff-ffff
● 0180-c200-0009 ffff-ffff-ffff
● 0180-c200-000a ffff-ffff-ffff
● 0180-c200-000b ffff-ffff-ffff
● 0180-c200-000c ffff-ffff-ffff
● 0180-c200-000d ffff-ffff-ffff
● 0180-c200-000e ffff-ffff-ffff
● 0180-c200-000f ffff-ffff-ffff
● 0180-c200-0010 ffff-ffff-ffff
● 0180-c200-0011 ffff-ffff-ffff
● 0180-c200-0012 ffff-ffff-ffff
● 0180-c200-0013 ffff-ffff-ffff
● 0180-c200-0016 ffff-ffff-ffff

● 0180-c200-0017 ffff-ffff-ffff
● 0180-c200-0018 ffff-ffff-ffff
● 0180-c200-0019 ffff-ffff-ffff
● 0180-c200-001a ffff-ffff-ffff
● 0180-c200-001b ffff-ffff-ffff
● 0180-c200-001c ffff-ffff-ffff
● 0180-c200-001d ffff-ffff-ffff
● 0180-c200-001e ffff-ffff-ffff
● 0180-c200-001f ffff-ffff-ffff
● 0180-c200-0020 ffff-ffff-ffe0
----结束

### 2.17 维护MAC表

#### 2.17.1 查看MAC地址

日常维护中，需要了解MAC地址信息时，可以在任意视图中执行以下命令。
表 2-7 查看 MAC 地址的命令

| 操作 | 命令 |
|---|---|
| 查看所有MAC地址表项 | display mac-address |
| 查看静态MAC地址表项 | display mac-address static |
| 查看指定VLAN下静态MAC地址表项 | display mac-address static vlan vlan-id |
| 查看指定VLAN下学习到的MAC地址表项 | display mac-address dynamic vlan vlan-id |
| 查看指定BD下静态MAC地址表项仅S6780-H、S6750-H、S6750-S、 S6750E-S、S6730-H-V2、S6730E-H- V2、S5755-H、S5755-S、S5732-H- V2系列支持。 | display mac-address static bridge- domain bd-id |
| 查看指定VSI下MAC地址表项仅S6780-H、S6750-H、S6750E-S、 S6750-S、S6730E-H-V2、S6730-H- V2、S5755-H、S5732-H-V2系列支持。 | display mac-address mac-address [ vsi vsiName ] [ verbose ] |
| 查看指定接口下学习到的MAC地址表项 | display mac-address dynamic interface interface-type interface-number |

| 操作 | 命令 |
|---|---|
| 查看通过二层隧道学习到的MAC地址表项仅S6780-H、S6750-H、S6750-S、 S6750E-S、S6730-H-V2、S6730E-H- V2、S5755-H、S5755-S、S5732-H- V2系列支持。 | display mac-address tunnel [ verbose ] |
| 查看指定MAC地址在芯片中的MAC地址表项信息 | display mac-address mac-address vlan vlan-id slot slot-id forward-engine |
| 查看指定MAC地址是否存在 | display mac-address mac-address |
| 查看系统MAC地址 | display system mac-address |
| 查看桥MAC地址 | display bridge mac-address |
| 查看接口的MAC地址 | display interface interface-type interface-number 显示信息中的Hardware address即为该接口的MAC地址 |
| 查看VLANIF的MAC地址 | display interface vlanif vlan-id 显示信息中的Hardware address即为该 VLANIF的MAC地址 |
| 查看MAC地址表项的统计计数 | ● 查看总的统计计数: display mac- address total-number ● 查看各种类型MAC地址表项的统计计数: display mac-address summary |
| 查看MAC地址的返回码的类型和数量 | display mac-address statistics { insert | remove } slot <slot-id> |
| 查看BPDU MAC | display mac-address bpdu |
| 查看设备学到MAC地址的DB表、软表以及硬表的信息 | display fwm mac diag |

#### 2.17.2 清除MAC地址

日常维护中，可以清除MAC地址，包括静态MAC地址、动态MAC地址等。
须知清除的操作务必仔细确认，一旦执行成功后，以前的信息将无法恢复。

表 2-8 清除 MAC 地址的命令

| 操作 | 视图 | 命令 |
|---|---|---|
| 清除所有静态和黑洞MAC地址表项 | 系统视图 | undo mac-address all |
| 按照VLAN清除MAC地址表项 |  | undo mac-address vlan vlan-id |
| 按照端口清除MAC地址表项 |  | undo mac-address interface-type interface-number |
| 清除所有静态MAC地址表项 |  | undo mac-address static |
| 清除所有黑洞MAC地址表项 |  | undo mac-address blackhole |
| 删除所有MAC地址学习限制规则 |  | undo mac-address limit all |
| 基于VSI清除MAC地址表项仅S6780-H、S6750-H、 S6750E-S、S6750-S、S6730E- H-V2、S6730-H-V2、S5755- H、S5732-H-V2系列支持。 | 用户视图 | reset mac-address vsi vsi-name |
| 清除动态MAC地址表项 | 用户视图 | reset mac-address |

#### 2.17.3 查看和清除MAC漂移信息

须知清除的操作务必仔细确认，一旦执行成功后，以前的信息将无法恢复。
表 2-9 查看和清除 MAC 漂移信息

| 操作 | 视图 | 命令 |
|---|---|---|
| 查看MAC地址漂移的历史记录 | 所有视图 | display mac-address flapping [ slot slot-id ] [ begin datetime hourtime ] |
| 查看MAC漂移的活动记录 |  | display mac-address flapping active-table [ slot slot-id ] |
| 查看MAC漂移老化记录 |  | display mac-address flapping aged- table [ slot slot-id ] |
| 清除MAC地址漂移历史记录 | 用户视图 | reset mac-address flapping record [ all ] |

### 2.18 MAC配置举例

#### 2.18.1 举例：配置静态MAC表项

组网需求如图2-9所示，服务器通过10GE1/0/2接口连接设备。为避免设备在转发目的地址为服务器地址的报文时进行广播，要求在设备上设置服务器的静态MAC地址表项，使设备始终通过10GE1/0/2接口单播发送去往服务器的报文。为了保证PC用户和服务器的安全通信，同时把PC用户的MAC地址和接口10GE1/0/1静态绑定。
说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
图 2-9 配置静态 MAC 地址组网图配置思路采用如下思路配置静态MAC：
1. 创建VLAN，并将接口加入VLAN，实现二层转发功能。
2. 在接口上配置服务器的静态MAC地址表项。
操作步骤步骤1 创建VLAN2，并将10GE1/0/1、10GE1/0/2加入VLAN 2。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 2 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type access

[DeviceA-10GE1/0/1] port default vlan 2 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type access [DeviceA-10GE1/0/2] port default vlan 2 [DeviceA-10GE1/0/2] quit步骤2 在接口10GE1/0/1上配置PC对应的静态MAC地址表项。
[DeviceA] mac-address static 00e0-fc12-3456 10ge 1/0/1 vlan 2步骤3 在接口10GE1/0/2上配置Server对应的静态MAC地址表项。
[DeviceA] mac-address static 00e0-fc12-3457 10ge 1/0/2 vlan 2
----结束检查配置结果\# 在任意视图下执行命令display mac-address static vlan vlan-id [ verbose ]，查看基于VLAN配置的静态MAC地址表项。
[DeviceA] display mac-address static vlan 2
------------------------------------------------------------------------------- MAC Address VLAN/VSI/BD Learned-From Type Age
------------------------------------------------------------------------------- 00e0-fc12-3456 2/-/- 10GE1/0/1 static - 00e0-fc12-3457 2/-/- 10GE1/0/2 static -
------------------------------------------------------------------------------- Total items: 2配置脚本\# sysname DeviceA \# vlan batch 2 \# interface 10GE1/0/1 port link-type access port default vlan 2 \# interface 10GE1/0/2 port link-type access port default vlan 2 \# mac-address static 00e0-fc12-3456 10GE1/0/1 vlan 2 mac-address static 00e0-fc12-3457 10GE1/0/2 vlan 2 \# return

#### 2.18.2 举例：配置黑洞MAC表项

组网需求如图2-10所示，设备收到一个非法用户的访问，非法用户的MAC地址为00e0- fc12-3456，所属VLAN为VLAN 3。通过指定该MAC地址为黑洞MAC，实现非法用户的过滤。

图 2-10 配置黑洞 MAC 地址组网图配置思路采用如下的思路配置黑洞MAC：
1. 创建VLAN，实现二层转发功能。
2. 添加黑洞MAC表，防止非法MAC地址攻击。
操作步骤步骤1 添加黑洞MAC地址表项。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan 3 [DeviceA-vlan3] quit [DeviceA] mac-address blackhole 00e0-fc12-3456 vlan 3
----结束检查配置结果\# 在任意视图下执行命令display mac-address blackhole，查看黑洞MAC地址表项。
[DeviceA] display mac-address blackhole vlan 3
------------------------------------------------------------------------------- MAC Address VLAN/VSI/BD Learned-From Type Age
------------------------------------------------------------------------------- 00e0-fc12-3456 3/-/- - blackhole -
------------------------------------------------------------------------------- Total items: 1配置脚本\# sysname DeviceA \# vlan batch 3 \# mac-address blackhole 00e0-fc12-3456 vlan 3 \# return

#### 2.18.3 举例：配置基于接口关闭MAC地址学习

组网需求如图2-11所示，用户网络1和用户网络2通过DeviceB与DeviceA相连，DeviceA连接DeviceB的接口为10GE1/0/1。用户网络1和用户网络2分别属于VLAN 10和VLAN 20。
在DeviceA上，为了防止黑客伪造大量源MAC地址进行攻击，可以基于接口10GE1/0/1关闭MAC地址学习。
图 2-11 配置基于接口关闭 MAC 地址学习组网图说明本例中interface1代表10GE1/0/1。
配置思路采用如下的思路配置基于接口关闭MAC地址学习：
1. 创建VLAN，并将接口加入到VLAN中，实现二层转发功能。
2. 配置基于接口关闭MAC地址学习，实现防止MAC地址攻击。
操作步骤步骤1 创建VLAN，并将接口加入到VLAN中。
\# 将10GE1/0/1加入VLAN 10和VLAN 20。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 10 20 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type trunk [DeviceA-10GE1/0/1] port trunk allow-pass vlan 10 20 [DeviceA-10GE1/0/1] quit步骤 2 配置基于接口关闭 MAC 地址学习。
\# 在接口10GE1/0/1上关闭MAC地址学习，端口学习到新的MAC地址的报文直接丢弃。

[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] mac-address learning disable action discard [DeviceA-10GE1/0/1] quit
----结束检查配置结果\# 在任意视图下执行命令display current-configuration interface，查看关闭MAC地址学习是否配置成功。
[DeviceA] display current-configuration interface 10ge 1/0/1 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 20 mac-address learning disable action discard \# return配置脚本\# sysname DeviceA \# vlan batch 10 20 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 20 mac-address learning disable action discard \# return

#### 2.18.4 举例：配置基于VLAN关闭MAC地址学习

组网需求如图2-12所示，用户网络1通过DeviceB与DeviceA相连，DeviceA的接口为10GE1/0/1。用户网络2通过DeviceC与DeviceA相连，DeviceA的接口为10GE1/0/2。
10GE1/0/1、10GE1/0/2同属于VLAN 2。为了防止黑客伪造大量源MAC地址进行攻击，可对VLAN 2关闭MAC地址学习。
图 2-12 配置基于 VLAN 关闭 MAC 地址学习组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。

配置思路采用如下的思路配置基于VLAN关闭MAC地址学习：
1. 创建VLAN，并将接口加入到VLAN中，实现二层转发功能。
2. 配置基于VLAN关闭MAC地址学习，实现防止MAC地址攻击。
操作步骤步骤1 创建VLAN，并将接口加入到VLAN中。
\# 将10GE1/0/1、10GE1/0/2加入VLAN 2。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan 2 [DeviceA-vlan2] quit [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type trunk [DeviceA-10GE1/0/1] port trunk allow-pass vlan 2 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type trunk [DeviceA-10GE1/0/2] port trunk allow-pass vlan 2 [DeviceA-10GE1/0/2] quit步骤2 配置基于VLAN关闭MAC地址学习。
\# 在VLAN 2上关闭MAC地址学习。
[DeviceA] vlan 2 [DeviceA-vlan2] mac-address learning disable [DeviceA-vlan2] quit
----结束检查配置结果\# 在任意视图下执行命令display vlan 2 verbose，查看关闭MAC地址学习是否配置成功。
[DeviceA] display vlan 2 verbose
* : Management-VLAN
--------------------- VLAN ID : 2 VLAN Name :
VLAN Type : Common Description : VLAN 0002 Status : Enable Broadcast : Enable MAC Learning : Disable Smart MAC Learning : Disable Current MAC Learning Result : Enable Statistics : Disable Property : Default VLAN State : Up
---------------- Tagged Port: 10GE1/0/1 10GE1/0/2
---------------- Active Tag Port: 10GE1/0/1 10GE1/0/2
--------------------- Interface Physical 10GE1/0/1 UP 10GE1/0/2 UP

配置脚本\# sysname DeviceA \# vlan batch 2 \# vlan 2 mac-address learning disable \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 2 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2 \# return

#### 2.18.5 举例：配置基于流行为关闭MAC地址学习

组网需求如图2-13所示，用户网络1和用户网络2通过DeviceB与DeviceA相连，DeviceA连接DeviceB的接口为10GE1/0/1。用户网络1和用户网络2分别属于VLAN 10和VLAN 20。
在DeviceA上，为了防止黑客伪造大量源MAC地址进行攻击，可以基于流行为关闭MAC地址学习。
图 2-13 配置基于流行为关闭 MAC 地址学习组网图说明本例中interface1代表10GE1/0/1。
配置思路采用如下的思路配置基于流行为关闭 MAC 地址学习：
1. 创建VLAN，并将接口加入到VLAN中，实现二层转发功能。
2. 配置基于流行为关闭MAC地址学习，实现防止MAC地址攻击。

操作步骤步骤1 创建VLAN，并将接口加入到VLAN中。
\# 将10GE1/0/1加入VLAN 10和VLAN 20。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 10 20 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type trunk [DeviceA-10GE1/0/1] port trunk allow-pass vlan 10 20 [DeviceA-10GE1/0/1] quit步骤2 配置基于流行为关闭MAC地址学习。
\# 配置流策略，并在流行为视图下关闭MAC地址学习。
[DeviceA] traffic classifier class1 [DeviceA-classifier-class1] if-match destination-mac 00e0-fc12-3456 [DeviceA-classifier-class1] quit [DeviceA] traffic behavior b1 [DeviceA-behavior-b1] mac-address learning disable [DeviceA-behavior-b1] quit [DeviceA] traffic policy poly1 [DeviceA-trafficpolicy-poly1] classifier class1 behavior b1 [DeviceA-trafficpolicy-poly1] quit \# 在接口10GE1/0/1上应用流策略。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] traffic-policy poly1 inbound [DeviceA-10GE1/0/1] quit
----结束检查配置结果\# 在任意视图下执行命令display traffic policy，查看禁止MAC地址学习是否配置成功。
[DeviceA] display traffic policy Traffic Policy Information:
Policy: poly1 Classifier: class1 Type: OR Behavior: b1 Mac-address learning:
Mac-address learning disable Total policy number is 1 \# 在任意视图下执行命令display traffic-policy applied-record，查看流策略的应用记录。
[DeviceA] display traffic-policy applied-record Total records : 1
-------------------------------------------------------------------------------- Policy Type/Name Apply Parameter Slot State
-------------------------------------------------------------------------------- poly1 10GE1/0/1(IN) 1 success
--------------------------------------------------------------------------------配置脚本\# sysname DeviceA

\# vlan batch 10 20 \# traffic classifier class1 type or if-match destination-mac 00e0-fc12-3456 ffff-ffff-ffff \# traffic behavior b1 mac-address learning disable \# traffic policy poly1 classifier class1 behavior b1 precedence 5 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 20 traffic-policy poly1 inbound \# return

#### 2.18.6 举例：配置基于接口的MAC地址限制

组网需求如图2-14所示，用户网络1和用户网络2通过DeviceB与DeviceA相连，DeviceA连接DeviceB的接口为10GE1/0/1。用户网络1和用户网络2分别属于VLAN 10和VLAN 20。
在DeviceA上，为了控制接入用户数量，可以基于接口10GE1/0/1配置MAC地址限制。
图 2-14 配置基于接口的 MAC 地址限制组网图说明本例中interface1代表10GE1/0/1。
配置思路采用如下的思路配置基于接口的MAC地址限制：
1. 创建VLAN，并将接口加入到VLAN中，实现二层转发功能。
2. 配置基于接口的MAC地址限制，控制接入用户数量。

操作步骤步骤1 创建VLAN，并将接口加入到VLAN中。
\# 将10GE1/0/1加入VLAN 10和VLAN 20。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 10 20 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type trunk [DeviceA-10GE1/0/1] port trunk allow-pass vlan 10 20 [DeviceA-10GE1/0/1] quit步骤2 配置基于接口的MAC地址限制。
\# 在接口10GE1/0/1上配置动态学习MAC地址的数量和动作：最多可以学习100个MAC地址，超过最大MAC地址学习数量的报文进行告警提示。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] mac-address limit maximum 100 alarm enable [DeviceA-10GE1/0/1] quit
----结束检查配置结果\# 在任意视图下执行命令display mac-address limit，查看动态学习MAC地址的数量和动作是否配置成功。
[DeviceA] display mac-address limit MAC Address Limit is enabled Total MAC Address limit rule count : 1 Port VLAN/VSI/SI/BD Slot Maximum Action Alarm
---------------------------------------------------------------------------- 10GE1/0/1 -- -- 100 discard enable配置脚本\# sysname DeviceA \# vlan batch 10 20 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 20 mac-address limit maximum 100 alarm enable \# return

#### 2.18.7 举例：配置基于VLAN的MAC地址限制

组网需求如图 2-15 所示，用户网络 1 通过 DeviceB 与 DeviceA 相连， DeviceA 的接口为10GE1/0/1。用户网络2通过DeviceC与DeviceA相连，DeviceA的接口为10GE1/0/2。
10GE1/0/1、10GE1/0/2同属于VLAN 2。为控制接入用户数，对VLAN 2进行配置MAC地址限制。

图 2-15 配置基于 VLAN 的 MAC 地址限制组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
配置思路采用如下的思路配置基于 VLAN 的 MAC 地址限制：
1. 创建VLAN，并将接口加入到VLAN中，实现二层转发功能。
2. 配置基于VLAN的MAC地址限制，控制接入用户数量。
操作步骤步骤1 创建VLAN，并将接口加入到VLAN中。
\# 将10GE1/0/1、10GE1/0/2加入VLAN 2。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan 2 [DeviceA-vlan2] quit [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type trunk [DeviceA-10GE1/0/1] port trunk allow-pass vlan 2 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type trunk [DeviceA-10GE1/0/2] port trunk allow-pass vlan 2 [DeviceA-10GE1/0/2] quit步骤2 配置基于VLAN的MAC地址限制。
\# 在VLAN 2上配置动态学习MAC地址的数量和动作：最多可以学习100个MAC地址，超过最大MAC地址学习数量的报文继续转发但不加入MAC地址表。
[DeviceA] vlan 2 [DeviceA-vlan2] mac-address limit maximum 100 action forward [DeviceA-vlan2] quit
----结束检查配置结果\# 在任意视图下执行命令display mac-address limit，查看动态学习MAC地址的数量和动作是否配置成功。

[DeviceA] display mac-address limit MAC Address Limit is enabled Total MAC Address limit rule count : 1 Port VLAN/VSI/SI/BD Slot Maximum Action Alarm
-------------------------------------------------------------------
-- 2 -- 100 forward enable配置脚本\# sysname DeviceA \# vlan batch 2 \# vlan 2 mac-address limit maximum 100 action forward \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 2 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2 \# return

#### 2.18.8 举例：配置基于VSI的MAC地址限制

组网需求如图2-16所示骨干网。为了保证骨干网的安全，在PE设备上通过配置基于VSI的MAC地址学习限制功能，实现对CE的接入控制。
图 配置基于 的 地址限制组网图2-16 VSI MAC说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
配置思路采用如下的思路配置基于VSI的MAC地址限制：

1. 在骨干网上配置路由协议实现互通。
2. 在PE之间建立远端LDP会话。
3. 在PE间建立传输业务数据所使用的隧道。
4. 在PE上使能MPLS L2VPN。
5. 在PE上创建VSI，指定信令为LDP。
6. 在PE设备基于VSI配置MAC地址学习限制，完成对CE的接入控制。
操作步骤
步骤1 配置各接口所属的VLAN以及相关接口IP地址
\# 配置CE1。
<HUAWEI> system-view
[HUAWEI] sysname CE1
[CE1] vlan 10
[CE1-vlan10] quit
[CE1] interface vlanif 10
[CE1-Vlanif10] ip address 10.1.1.1 255.255.255.0
[CE1-Vlanif10] quit
[CE1] interface 10ge 1/0/1
[CE1-10GE1/0/1] port link-type trunk
[CE1-10GE1/0/1] port trunk allow-pass vlan 10
[CE1-10GE1/0/1] quit
配置CE2。
\#
<HUAWEI> system-view
[HUAWEI] sysname CE2
[CE2] vlan 40
[CE2-vlan40] quit
[CE2] interface vlanif 40
[CE2-Vlanif40] ip address 10.1.1.2 255.255.255.0
[CE2-Vlanif40] quit
[CE2] interface 10ge 1/0/1
[CE2-10GE1/0/1] port link-type trunk
[CE2-10GE1/0/1] port trunk allow-pass vlan 40
[CE2-10GE1/0/1] quit
\# 配置PE1。
<HUAWEI> system-view
[HUAWEI] sysname PE1
[PE1] vlan batch 10 20
[PE1] interface vlanif 20
[PE1-Vlanif20] ip address 4.4.4.4 255.255.255.0
[PE1-Vlanif20] quit
[PE1] interface 10ge 1/0/1
[PE1-10GE1/0/1] port link-type trunk
[PE1-10GE1/0/1] port trunk allow-pass vlan 10
[PE1-10GE1/0/1] quit
[PE1] interface 10ge 1/0/2
[PE1-10GE1/0/2] port link-type trunk
[PE1-10GE1/0/2] port trunk allow-pass vlan 20
[PE1-10GE1/0/2] quit
\# 配置P。
<HUAWEI> system-view
[HUAWEI] sysname P
[P] vlan batch 20 30
[P] interface vlanif 20
[P-Vlanif20] ip address 4.4.4.2 255.255.255.0
[P-Vlanif20] quit
[P] interface vlanif 30

[P-Vlanif30] ip address 5.5.5.5 255.255.255.0 [P-Vlanif30] quit [P] interface 10ge 1/0/1 [P-10GE1/0/1] port link-type trunk [P-10GE1/0/1] port trunk allow-pass vlan 20 [P-10GE1/0/1] quit [P] interface 10ge 1/0/2 [P-10GE1/0/2] port link-type trunk [P-10GE1/0/2] port trunk allow-pass vlan 30 [P-10GE1/0/2] quit \# 配置PE2。
<HUAWEI> system-view [HUAWEI] sysname PE2 [PE2] vlan batch 30 40 [PE2] interface vlanif 30 [PE2-Vlanif30] ip address 5.5.5.2 255.255.255.0 [PE2-Vlanif30] quit [PE2] interface 10ge 1/0/1 [PE2-10GE1/0/1] port link-type trunk [PE2-10GE1/0/1] port trunk allow-pass vlan 30 [PE2-10GE1/0/1] quit [PE2] interface 10ge 1/0/2 [PE2-10GE1/0/2] port link-type trunk [PE2-10GE1/0/2] port trunk allow-pass vlan 40 [PE2-10GE1/0/2] quit步骤2 配置IGP，本例中使用OSPF。
配置OSPF时，注意需要发布PE1、P和PE2的32位Loopback接口地址（LSR-ID）。
\# 配置PE1。
[PE1] router id 1.1.1.1 [PE1] interface loopback 1 [PE1-LoopBack1] ip address 1.1.1.1 32 [PE1-LoopBack1] quit [PE1] ospf 1 [PE1-ospf-1] area 0 [PE1-ospf-1-area-0.0.0.0] network 1.1.1.1 0.0.0.0 [PE1-ospf-1-area-0.0.0.0] network 4.4.4.4 0.0.0.255 [PE1-ospf-1-area-0.0.0.0] quit [PE1-ospf-1] quit \# 配置P。
[P] router id 2.2.2.2 [P] interface loopback 1 [P-LoopBack1] ip address 2.2.2.2 32 [P-LoopBack1] quit [P] ospf 1 [P-ospf-1] area 0 [P-ospf-1-area-0.0.0.0] network 2.2.2.2 0.0.0.0 [P-ospf-1-area-0.0.0.0] network 4.4.4.2 0.0.0.255 [P-ospf-1-area-0.0.0.0] network 5.5.5.5 0.0.0.255 [P-ospf-1-area-0.0.0.0] quit [P-ospf-1] quit \# 配置PE2。
[PE2] router id 3.3.3.3 [PE2] interface loopback 1 [PE2-LoopBack1] ip address 3.3.3.3 32 [PE2-LoopBack1] quit [PE2] ospf 1 [PE2-ospf-1] area 0 [PE2-ospf-1-area-0.0.0.0] network 3.3.3.3 0.0.0.0 [PE2-ospf-1-area-0.0.0.0] network 5.5.5.2 0.0.0.255 [PE2-ospf-1-area-0.0.0.0] quit [PE2-ospf-1] quit

配置完成后，在PE1、P和PE2上执行display ip routing-table命令可以看到已学到彼此的路由。以PE1的显示为例：
[PE1] display ip routing-table Route Flags: R - relay, D - download to fib, T - to vpn-instance
------------------------------------------------------------------------------ Routing Tables: Public Destinations : 8 Routes : 8 Destination/Mask Proto Pre Cost Flags NextHop Interface
1.1.1.1/32 Direct 0 0 D 127.0.0.1 LoopBack1
2.2.2.2/32 OSPF 10 1 D 4.4.4.2 Vlanif20
3.3.3.3/32 OSPF 10 2 D 4.4.4.2 Vlanif20
4.4.4.0/24 Direct 0 0 D 4.4.4.4 Vlanif20
4.4.4.4/32 Direct 0 0 D 127.0.0.1 Vlanif20
5.5.5.0/24 OSPF 10 2 D 4.4.4.2 Vlanif20
127.0.0.0/8 Direct 0 0 D 127.0.0.1 InLoopBack0
127.0.0.1/32 Direct 0 0 D 127.0.0.1 InLoopBack0步骤3 配置MPLS基本能力和LDP。
\# 配置PE1。
[PE1] mpls lsr-id 1.1.1.1 [PE1] mpls [PE1-mpls] quit [PE1] mpls ldp [PE1-mpls-ldp] quit [PE1] interface vlanif 20 [PE1-Vlanif20] mpls [PE1-Vlanif20] mpls ldp [PE1-Vlanif20] quit \# 配置P。
[P] mpls lsr-id 2.2.2.2 [P] mpls [P-mpls] quit [P] mpls ldp [P-mpls-ldp] quit [P] interface vlanif 20 [P-Vlanif20] mpls [P-Vlanif20] mpls ldp [P-Vlanif20] quit [P] interface vlanif 30 [P-Vlanif30] mpls [P-Vlanif30] mpls ldp [P-Vlanif30] quit \# 配置PE2。
[PE2] mpls lsr-id 3.3.3.3 [PE2] mpls [PE2-mpls] quit [PE2] mpls ldp [PE2-mpls-ldp] quit [PE2] interface vlanif 30 [PE2-Vlanif30] mpls [PE2-Vlanif30] mpls ldp [PE2-Vlanif30] quit配置完成后，在PE1、P和PE2上执行display mpls ldp session命令可以看到PE1和P之间或PE2和P之间的对等体的Status项为“Operational”，即对等体关系已建立。执行display mpls lsp命令可以看到LSP的建立情况。以PE1的显示为例：
[PE1] display mpls ldp session LDP Session(s) in Public Network Codes: LAM(Label Advertisement Mode), SsnAge Unit(DDDD:HH:MM)
A '*' before a session means the session is being deleted.
------------------------------------------------------------------------------ PeerID Status LAM SsnRole SsnAge KASent/Rcv

------------------------------------------------------------------------------
2.2.2.2:0 Operational DU Passive 000:15:29 3717/3717
------------------------------------------------------------------------------
TOTAL: 1 session(s) Found.
步骤4 在PE之间建立远端LDP会话。
\# 配置PE1。
[PE1] mpls ldp remote-peer 3.3.3.3
[PE1-mpls-ldp-remote-3.3.3.3] remote-ip 3.3.3.3
[PE1-mpls-ldp-remote-3.3.3.3] quit
\# 配置PE2。
[PE2] mpls ldp remote-peer 1.1.1.1
[PE2-mpls-ldp-remote-1.1.1.1] remote-ip 1.1.1.1
[PE2-mpls-ldp-remote-1.1.1.1] quit
配置完成后，在PE1或PE2上执行display mpls ldp session命令可以看到PE1和PE2之
间的对等体的Status项为“Operational”，即远端对等体关系已建立。
步骤5 在PE上使能MPLS L2VPN。
\# 配置PE1。
[PE1] mpls l2vpn
[PE1-l2vpn] quit
\# 配置PE2。
[PE2] mpls l2vpn
[PE2-l2vpn] quit
步骤6 在PE上配置VSI。
\# 配置PE1。
[PE1] vsi a2 static
[PE1-vsi-a2] pwsignal ldp
[PE1-vsi-a2-ldp] vsi-id 2
[PE1-vsi-a2-ldp] peer 3.3.3.3
[PE1-vsi-a2-ldp] quit
[PE1-vsi-a2] quit
\# 配置PE2。
[PE2] vsi a2 static
[PE2-vsi-a2] pwsignal ldp
[PE2-vsi-a2-ldp] vsi-id 2
[PE2-vsi-a2-ldp] peer 1.1.1.1
[PE2-vsi-a2-ldp] quit
[PE2-vsi-a2] quit
步骤7 在PE上配置VSI与接口的绑定。
\# 配置PE1。
[PE1] interface vlanif 10
[PE1-Vlanif10] l2 binding vsi a2
[PE1-Vlanif10] quit
\# 配置PE2。
[PE2] interface vlanif 40
[PE2-Vlanif40] l2 binding vsi a2
[PE2-Vlanif40] quit
步骤8 验证配置结果。
完成上述配置后，在PE1上执行display vsi name a2 verbose命令，可以看到名字为
a2的VSI建立了一条PW到PE2，VSI状态为UP。
[PE1] display vsi name a2 verbose

***VSI Name : a2
Administrator VSI : no
Isolate Spoken : disable
VSI Index : 0
PW Signaling : ldp
Member Discovery Style : static
PW MAC Learn Style : unqualify
Encapsulation Type : vlan
MTU : 1500
Diffserv Mode : uniform
Mpls Exp : --
DomainId : 255
Domain Name :
Ignore AcState : disable
P2P VSI : disable
Create Time : 0 days, 0 hours, 5 minutes, 1 seconds
VSI State : up
VSI ID : 2
*Peer Router ID : 3.3.3.3
Negotiation-vc-id : 2
primary or secondary : primary
ignore-standby-state : no
VC Label : 4098
Peer Type : dynamic
Session : up
Tunnel ID : 0x1
Broadcast Tunnel ID : 0x1
Broad BackupTunnel ID : 0x0
CKey : 2
NKey : 1
Stp Enable : 0
PwIndex : 0
Control Word : disable
Interface Name : Vlanif10
State : up
Access Port : false
Last Up Time : 2010/12/30 11:31:18
Total Up Time : 0 days, 0 hours, 1 minutes, 35 seconds
**PW Information:
*Peer Ip Address : 3.3.3.3
PW State : up
Local VC Label : 4098
Remote VC Label : 4098
Remote Control Word : disable
PW Type : label
Local VCCV : alert lsp-ping bfd
Remote VCCV : alert lsp-ping bfd
Tunnel ID : 0x1
Broadcast Tunnel ID : 0x1
Broad BackupTunnel ID : 0x0
Ckey : 0x2
Nkey : 0x1
Main PW Token : 0x1
Slave PW Token : 0x0
Tnl Type : LSP
OutInterface : Vlanif20
Backup OutInterface :
Stp Enable : 0
PW Last Up Time : 2010/12/30 11:32:03
PW Total Up Time : 0 days, 0 hours, 1 minutes, 35 seconds
在 CE1 （ 10.1.1.1 ）上能够 ping 通 CE2 （ 10.1.1.2 ）。
[CE1] ping 10.1.1.2
PING 10.1.1.2: 56 data bytes, press CTRL_C to break
Reply from 10.1.1.2: bytes=56 Sequence=1 ttl=255 time=90 ms
Reply from 10.1.1.2: bytes=56 Sequence=2 ttl=255 time=77 ms

Reply from 10.1.1.2: bytes=56 Sequence=3 ttl=255 time=34 ms Reply from 10.1.1.2: bytes=56 Sequence=4 ttl=255 time=46 ms Reply from 10.1.1.2: bytes=56 Sequence=5 ttl=255 time=94 ms
--- 10.1.1.2 ping statistics --- 5 packet(s) transmitted 5 packet(s) received
0.00% packet loss round-trip min/avg/max = 34/68/94 ms步骤9 在PE1的VSI上配置MAC地址学习限制。
\# 在VSI上配置MAC地址学习限制规则：最多可以学习300个MAC地址，超过最大MAC地址学习数量的报文直接丢弃并进行告警提示。
[PE1] vsi a2 static [PE1-vsi-a2] mac-address limit maximum 300 action discard alarm enable [PE1-vsi-a2] quit
----结束检查配置结果\# 在任意视图下执行 display mac-address limit 命令，查看 MAC 地址学习限制规则是否配置成功。
<PE1> display mac-address limit MAC limit is enabled Total MAC limit rule count : 1 PORT VLAN/VSI SLOT Maximum Rate(ms) Action Alarm
----------------------------------------------------------------------------
- a2 - 300 - discard enable配置脚本
● CE1的配置文件\# sysname CE1 \# vlan batch 10 \# interface Vlanif10 ip address 10.1.1.1 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# return
● CE2的配置文件\# sysname CE2 \# vlan batch 40 \# interface Vlanif40 ip address 10.1.1.2 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 40 \# return
● PE1的配置文件

\# sysname PE1 \# router id 1.1.1.1 \# vlan batch 10 20 \# mpls lsr-id 1.1.1.1 mpls \# mpls l2vpn \# vsi a2 static mac-address limit maximum 300 action discard alarm enable pwsignal ldp vsi-id 2 peer 3.3.3.3 \# mpls ldp \# mpls ldp remote-peer 3.3.3.3 remote-ip 3.3.3.3 \# interface Vlanif10 l2 binding vsi a2 \# interface Vlanif20 ip address 4.4.4.4 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 20 \# interface LoopBack1 ip address 1.1.1.1 255.255.255.255 \# ospf 1 area 0.0.0.0 network 1.1.1.1 0.0.0.0 network 4.4.4.0 0.0.0.255 \# return
● P的配置文件\# sysname P \# router id 2.2.2.2 \# vlan batch 20 30 \# mpls lsr-id 2.2.2.2 mpls \# mpls ldp \# interface Vlanif20 ip address 4.4.4.2 255.255.255.0 mpls mpls ldp \# interface Vlanif30 ip address 5.5.5.5 255.255.255.0 mpls

mpls ldp \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 20 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 30 \# interface LoopBack1 ip address 2.2.2.2 255.255.255.255 \# ospf 1 area 0.0.0.0 network 2.2.2.2 0.0.0.0 network 4.4.4.0 0.0.0.255 network 5.5.5.0 0.0.0.255 \# return
● PE2的配置文件\# sysname PE2 \# router id 3.3.3.3 \# vlan batch 30 40 \# mpls lsr-id 3.3.3.3 mpls \# mpls l2vpn \# vsi a2 static pwsignal ldp vsi-id 2 peer 1.1.1.1 \# mpls ldp \# mpls ldp remote-peer 1.1.1.1 remote-ip 1.1.1.1 \# interface Vlanif30 ip address 5.5.5.2 255.255.255.0 mpls mpls ldp \# interface Vlanif40 l2 binding vsi a2 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 30 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 40 \# interface LoopBack1 ip address 3.3.3.3 255.255.255.255 \# ospf 1 area 0.0.0.0 network 3.3.3.3 0.0.0.0 network 5.5.5.0 0.0.0.255 \# return

#### 2.18.9 举例：配置MAC地址防漂移

组网需求如图2-17所示，用户需要访问企业的服务器。如果某些非法用户从其他接口假冒服务器的MAC地址发送报文，则服务器的MAC地址将在其他接口学习到。这样用户发往服务器的报文就会发往非法用户，不仅会导致用户与服务器不能正常通信，还会导致一些重要用户信息被窃取。为了提高服务器安全性，防止被非法用户攻击，可配置MAC防漂移功能。
图 2-17 配置 MAC 地址防漂移组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
配置思路采用如下的思路配置 MAC 防漂移：
1. 创建VLAN，并将接口加入到VLAN中，实现二层转发功能。
2. 在服务器连接的接口上配置MAC防漂移功能，实现MAC地址防漂移。

操作步骤步骤1 在DeviceA上创建VLAN，并将接口加入到VLAN中。
\# 将10GE1/0/1、10GE1/0/2加入VLAN10。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 10 [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type trunk [DeviceA-10GE1/0/2] port trunk allow-pass vlan 10 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10geint 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type hybrid [DeviceA-10GE1/0/1] port hybrid pvid vlan 10 [DeviceA-10GE1/0/1] port hybrid untagged vlan 10 [DeviceA-10GE1/0/1] quit步骤2 # 在10GE1/0/1上配置MAC防漂移功能。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] mac-address learning priority 2 [DeviceA-10GE1/0/1] quit [DeviceA] undo mac-address learning priority 2 allow-flapping
----结束检查配置结果\# 在任意视图下执行display current-configuration命令，查看接口MAC地址学习的优先级配置是否正确。
[DeviceA] display current-configuration interface 10ge 1/0/1 \# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 10 port hybrid untagged vlan 10 mac-address learning priority 2 \# return配置脚本\# sysname DeviceA \# vlan batch 10 undo mac-address learning priority 2 allow-flapping \# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 10 port hybrid untagged vlan 10 mac-address learning priority 2 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 10 \# return

#### 2.18.10 举例：配置MAC地址漂移检测

组网需求如图2-18所示，网络中两台设备间网线误接形成了网络环路，引起MAC地址发生漂移、MAC地址表震荡。
为了能够及时检测网络中出现的环路，可以在DeviceA上配置MAC地址漂移检测功能，通过检测是否发生MAC地址漂移来判断网络中存在的环路，从而排除故障。
图 2-18 配置 MAC 地址漂移检测组网图说明MAC地址漂移检测功能只能检测单环场景，对于多环场景的限制说明，请查看“MAC配置注意事项”。
说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
配置思路采用如下思路配置MAC地址漂移检测：
1. 开启MAC地址漂移检测功能，实现检测网络中是否存在MAC地址漂移。
2. 配置MAC地址漂移表项的老化时间。
3. 配置接口MAC地址漂移后的处理动作，实现破除环路。
操作步骤步骤1 开启MAC地址漂移检测功能。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] mac-address flapping detection步骤2 配置MAC地址漂移表项的老化时间。
[DeviceA] mac-address flapping aging-time 500步骤3 配置10GE1/0/1、10GE1/0/2接口MAC地址漂移后关闭。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] mac-address flapping trigger error-down [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch

[DeviceA-10GE1/0/2] mac-address flapping trigger error-down [DeviceA-10GE1/0/2] quit步骤4 配置被Shutdown接口的自动恢复功能、自动恢复时间。
[DeviceA] error-down auto-recovery cause mac-address-flapping interval 500
----结束检查配置结果执行命令display mac-address flapping，查看MAC漂移相关的配置。
[DeviceA] display mac-address flapping MAC Address Flapping Configurations :
------------------------------------------------------------------------- Flapping detection : Enable Aging time(s) : 500 Quit-VLAN Recover time(m) : -- Exclude VLAN-list : -- Security level : Middle Exclude BD-list : --
-------------------------------------------------------------------------执行命令 display mac-address flapping active-table ，查看 MAC 漂移的活动记录。
第一个学习到MAC地址的接口是正确的出接口，称为源端口（Original Port），后学习的端口是漂移端口（Move Port），配置该功能后将关闭漂移端口。
[DeviceA] display mac-address flapping active-table S: start time E: end time (D): error down
------------------------------------------------------------------------------- Time : S:2019-10-26 10:39:27 E:2019-10-26 10:50:09 VLAN/BD/VSI : 2000/-/- MAC Address : 00e0-fc12-3456 Original-Port: 10GE1/0/1 Move-Ports : 10GE1/0/2 MoveNum : 65535
------------------------------------------------------------------------------- Total items on slot 1: 1配置脚本\# sysname DeviceA \# mac-address flapping aging-time 500 \# error-down auto-recovery cause mac-address-flapping interval 500 \# interface 10GE1/0/1 mac-address flapping trigger error-down \# interface 10GE1/0/2 mac-address flapping trigger error-down \# return

### 2.19 MAC常见配置错误

#### 2.19.1 设备上无法学习正确的MAC表项

故障现象二层数据转发失败，设备上无法学习正确的MAC转发表项。
操作步骤步骤1 查看是否配置错误导致MAC地址无法正确学习。

| 检查项 | 检查方法 | 后续操作 |
|---|---|---|
| 接口所属的 VLAN是否创建 | 在任意视图下，执行命令 display vlan vlan-id，如果提示“Error: The VLAN does not exist.”，则表示该VLAN没有创建。 | 请在系统视图下，执行命令vlan vlan-id创建VLAN。 |
| 接口是否透传对应VLAN | 在任意视图下，执行命令 display vlan vlan-id，查看显示信息中是否存在该接口名。如果没有该接口名，则表示该接口没有透传对应VLAN。 | 对于Trunk接口，执行命令port trunk allow-pass vlan，将接口加入VLAN。对于Hybrid接口，执行命令port hybrid tagged vlan 或者port hybrid untagged vlan，将接口加入VLAN。对于Access接口，执行命令port default vlan，将接口加入VLAN。 |
| 设备是否配置了黑洞MAC | 在任意视图下，执行 display mac-address blackhole命令，查看是否配置了黑洞MAC。 | 如果有黑洞MAC相关配置，请在系统视图下，执行命令undo mac- address blackhole删除黑洞MAC 地址。 |
| 接口和VLAN是否关闭了MAC地址学习功能 | 在接口视图和VLAN视图下，分别执行命令display this | include learning 查看是否存在mac- address learning disable的配置。如果存在，则说明接口或VLAN 关闭了MAC地址学习功能。 | 请在接口视图或VLAN视图下，执行命令undo mac-address learning disable打开MAC地址学习功能。 |
| BD是否关闭了 MAC地址学习功能 | 在BD视图下，执行命令 display this | include learning查看是否存在 mac-address learning disable的配置。如果存在，则说明BD关闭了 MAC地址学习功能。 | 请在BD视图下，执行命令undo mac-address learning disable打开MAC地址学习功能。 |

| 检查项 | 检查方法 | 后续操作 |
|---|---|---|
| 接口和VLAN是否配置了MAC地址学习限制数量 | 在接口视图和VLAN视图下，执行display this | include mac-address limit查看是否存在MAC地址学习限制数量的配置。如果存在，则说明配置了 MAC地址学习限制数。 | ● 请在接口视图或VLAN视图下，执行命令mac-address limit增加MAC地址学习数量。 ● 请在接口视图或VLAN视图下，执行命令undo mac-address limit取消MAC地址限制。 |
| BD是否配置了 MAC地址学习限制数量 | 在BD视图下，执行 display this | include mac-address limit查看是否存在MAC地址学习限制数量的配置。如果存在，则说明配置了MAC地址学习限制数。 | ● 请在BD视图下，执行命令mac- address limit增加MAC地址学习数量。 ● 请在BD视图下，执行命令undo mac-address limit取消MAC地址限制。 |

执行完上述操作后，故障仍然存在，请执行步骤2。
步骤2 检查网络中是否存在环路导致MAC地址表项振荡。
一般情况下MAC地址漂移是由环路导致的，在系统视图下执行命令mac-address
1.
flapping detection，配置MAC地址漂移检测功能。
2. 配置MAC地址漂移检测功能后，系统将检测VLAN内所有MAC地址是否发生漂移。
如果系统中不存在环路，请执行步骤3。
步骤3 检查MAC地址数是否已达设备支持的最大规格。设备学习到的MAC地址数达到产品支持的规格，将无法继续学习新的MAC地址表项。
● 如果该接口学习到的MAC地址数小于等于该接口连接的实际运行的主机数，说明设备接入的主机已经超过了设备支持的规格，请调整网络部署。
● 如果该接口学习到的MAC地址数远大于该接口所连接网络实际运行的主机数，说明该接口所连接的网络可能存在恶意刷新MAC地址表项的攻击，请根据下列方法处理。

| 场景分类 | 解决方法 |
|---|---|
| 接口与其他设备相连 | 在该接口连接的设备上执行命令 display mac-address查看MAC地址表项，根据MAC地址学习接口找到可能存在攻击的主机所在的接口。如果查找到的接口还下连其他设备，请重复上述操作直至查找到恶意攻击的主机。 |

| 场景分类 | 解决方法 |
|---|---|
| 接口与主机相连 | – 和管理员确认后先断开该主机，等该主机恶意攻击排除后再接入网络。 – 和管理员确认后在该接口上执行 mac-address limit命令配置接口 MAC地址学习数量为1。 |

----结束
