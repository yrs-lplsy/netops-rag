# S1700, S5700, S6700 V600R025C00 配置指南-安全 01-07 URPF配置

## 7 URPF配置

7 URPF 配置

### 7.1 URPF简介

7.2 URPF配置注意事项
7.3 URPF原理描述
7.4 URPF缺省配置
7.5 配置URPF
7.1 URPF 简介
定义
URPF（Unicast Reverse Path Forwarding）是单播逆向路径转发的简称，其主要功能
是防止基于源IP地址欺骗的网络攻击行为。
URPF根据报文的源IP地址查找FIB（Forwarding Information Base）表中是否存在去
往该地址的路由，并判断报文入接口与路由出接口是否一致。如果FIB表不存在去往该
源IP地址的路由或报文入接口与路由出接口不一致，则丢弃该报文，从而有效防范网
络中通过修改报文源IP地址而进行恶意攻击行为的发生。
目的
拒绝服务DoS（Denial of Service）攻击是一种阻止连接服务的网络攻击，它的攻击方
式有很多种，最基本的DoS攻击就是利用大量合法或伪造的请求占用过多的服务资
源，从而使合法用户无法得到正常服务，URPF技术针对伪造源IP地址的DoS攻击非常
有效。
如图7-1所示，PC_A伪造源地址为10.2.2.2的报文，向Server发起请求，若DeviceA上
没有开启URPF功能，Server在收到请求报文后会向PC_B（10.2.2.2）发送回应报文，
PC_A发起的这种伪造报文对Server和PC_B都造成攻击。若在DeviceA上开启了URPF功
能，DeviceA在接收到这个报文后，检查其入接口是否匹配，发现源地址为10.2.2.2的
报文应该从interface2进入，则DeviceA认为该报文源地址是伪造的，直接丢弃该报
文。而从 PC_B 发向 Server 的正常报文，检查通过后，被正常转发。

图 7-1 URPF 防止基于源地址欺骗示意图

### 7.2 URPF配置注意事项

License 依赖URPF无需License许可即可使用。
硬件依赖表 7-1 支持本特性的硬件

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
特性限制表 7-2 本特性的使用限制

| 特性 | 特性限制 |
|---|---|
| IPv6 URPF | ECMP路由只进行松散URPF检查。 |
| IPv6 URPF | 报文的源IP是主机接口IPv6地址或者源IP对应路由表项的出接口是隧道接口的时候，接口上URPF严格模式失效，降为松散模式。 |
| IPv6 URPF | 对于S6750-H系列，S6730E-H-V2系列，S5735-S-V2系列，S5735E-S- V2系列，S5755-H系列，S5735R-S-V2系列，S6780-H系列，S5735S- S3系列，S5755-S系列，S6750E-S系列，S6730-S-V2系列，S5735I-S- V2系列，S5732-H-V2系列，S6730-H-V2系列，S5735I-H-V2系列， S6750-S系列： SuperVlan接入场景下，绑定SubVlan的接口下配置严格URPF检查时在没有学习或配置源IP的ARP情况下，流量转发不通。 |
| IPV4 URPF | 对于S6750E-S系列，S5735R-S-V2系列，S6780-H系列，S5755-S系列，S6750-S系列： BOOTP/DHCP报文（报文源IP为0.0.0.0且目的IP为255.255.255.255）上送CPU进行处理，URPF功能失效。 |

| 特性 | 特性限制 |
|---|---|
| IPV4 URPF | 对于S6750-H系列，S6730E-H-V2系列，S5735-S-V2系列，S5735E-S- V2系列，S5755-H系列，S5735R-S-V2系列，S6780-H系列，S5735S- S3系列，S5755-S系列，S6750E-S系列，S6730-S-V2系列，S5735I-S- V2系列，S5732-H-V2系列，S6730-H-V2系列，S5735I-H-V2系列， S6750-S系列： SuperVlan接入场景，绑定SubVlan的接口下配置严格URPF检查时，在没有学习或配置源IP的ARP的情况下，流量转发不通。 |
| IPV4 URPF | 源IP命中的FIB表项下一跳为多路径（包括ECMP和FRR）的情况下， URPF严格模式对外呈现为松散检查。 |
| IPV4 URPF | 三层转发报文的源IP对应路由表的出接口是隧道接口（包括TE）时，若配置为严格模式，则自动降级为松散模式；隧道报文解封装后内层IP转发时，不对隧道内层IP做URPF检查。 |
| IPV4 URPF | 有些报文的源IP对应的网段路由的下一跳出接口是本机上送CPU或黑洞丢弃，当设备收到这种报文时，URPF不对报文进行报文合法性校验，且严格模式失效，降为松散模式。可以针对流量的源IP配置ACL丢弃策略，禁止流量继续转发。 |
| IPV4 URPF | 对于产品S6730E-H-V2系列，S6750E-S系列，S6780-H系列，S5755-S 系列，S6750-S系列，S6750-H48X8C，S6750-H48Y8C，S6730- H6FX4Y2CZ-V2： URPF的严格模式与flow-matrix规则同时配置，如果flow-matrix规则命中，不做URPF严格检查，URPF降为松散模式。 |

### 7.3 URPF原理描述

工作模式在复杂的网络环境中，会遇到对端设备记录的路由路径与本端不一致的情况，此时使能URPF的设备可能会丢弃从合法路径接收的报文，为了解决该问题，设备实现了两种URPF模式：
● 严格模式严格模式下，设备不仅要求 FIB 表中存在去往报文源 IP 地址的路由，还要求报文入接口与路由出接口一致。
建议在对端与本端记录的路由路径一致的环境下使用严格模式。例如两台网络边界设备之间只有一条路径，此时使用严格模式能够保证网络的安全性。
● 松散模式松散模式下，设备仅要求FIB表中存在去往报文源IP地址的路由，不要求报文入接口与路由出接口一致。
建议在不能保证对端与本端记录的路由路径一致的环境下使用松散模式。例如两个网络边界设备之间有多条路径，此时松散模式既可以有效地阻止网络攻击，又可以避免合法报文被错误丢弃。

工作机制URPF的工作机制如图7-2所示。
图 7-2 URPF 工作机制

### 7.4 URPF缺省配置

URPF 的缺省配置如表 7-3 所示。
表 7-3 URPF 缺省配置

| 参数 | 缺省值 |
|---|---|
| URPF检查功能 | 未使能 |
| URPF检查模式 | 松散检查 |

### 7.5 配置URPF

#### 7.5.1 使能接口的URPF功能

前提条件在配置URPF之前，需完成以下任务：
配置接口的链路层协议参数，使接口的链路协议状态为Up。
背景信息配置URPF时，需要在接口下使能URPF功能。
操作步骤步骤1 进入系统视图。
system-view步骤 2 进入接口视图。
interface interface-type interface-number步骤3 配置接口从二层模式切换到三层模式。
undo portswitch仅S6780-H系列、S6750-H系列、S6730-H-V2系列、S6730E-H-V2系列、S6750-S系列、S6730-S-V2系列、S6750E-S系列、S5732-H-V2系列、S5755-H系列、S5755-S系列支持该步骤。请用户根据实际接口类型自行选择是否要执行此步骤。
步骤4 使能接口下的URPF功能。
ip urpf enable缺省情况下，接口下未使能URPF功能。
----结束

#### 7.5.2 配置URPF检查模式

背景信息URPF 检查分为严格模式和松散模式，并通过配置参数 allow default-route 允许报文匹配的路由为缺省路由。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置URPF检查模式。
1. 进入接口视图。
interface interface-type interface-number
2. 配置接口从二层模式切换到三层模式。
undo portswitch

仅S6780-H系列、S6750-H系列、S6730-H-V2系列、S6730E-H-V2系列、S6750- S系列、S6730-S-V2系列、S6750E-S系列、S5732-H-V2系列、S5755-H系列、S5755-S系列支持该步骤。请用户根据实际接口类型自行选择是否要执行此步骤。
3. 配置接口的URPF检查模式。
ip urpf { loose | strict }缺省情况下，接口下未开启URPF功能。如果接口下开启URPF功能，则缺省检查模式为松散检查。
4. 配置缺省路由参与URPF检查。
ip urpf allow default-route缺省情况下，未配置缺省路由参与URPF检查。
----结束

#### 7.5.3 （可选）配置对指定流去使能URPF功能

背景信息配置接口的URPF功能后，设备对进入接口的所有报文都进行URPF检查。此时如果要保证某些特定的报文不被丢弃，比如设备信任从某个服务器过来的所有报文，不对其进行URPF检查，可以配置对指定流去使能URPF功能。配置流程如下：
1. 配置流分类：定义一组流量匹配规则，对于不进行URPF检查的特定报文进行分类。请参见《配置指南-QoS配置》中“MQC配置”的“配置流分类”。
2. 配置流行为：在流行为中去使能URPF功能。请参见本节“操作步骤”。
3. 配置流策略：将指定的流分类和流行为绑定，对分类后的特定报文去使能URPF功能。请参见《配置指南-QoS配置》中“MQC配置”的“配置流策略”。
4. 应用流策略：按照需要在相应的视图下应用流策略。请参见《配置指南-QoS配置》中“MQC配置”的“应用流策略”。
说明仅S6780-H、S6750-S、S6730-H-V2、S6750-H、S5732-H-V2、S6750E-S、S6730E-H-V2、S6730-S-V2、S5755-S和S5755-H系列支持配置对指定流去使能URPF功能。
操作步骤步骤1 进入系统视图。
system-view步骤2 创建一个流行为并进入流行为视图，或进入已存在的流行为视图。
traffic behavior behavior-name步骤3 去使能对指定流进行URPF检查功能。
ip urpf disable
----结束检查配置结果执行命令display traffic behavior [ behavior-name ]，查看已配置的流行为信息。
