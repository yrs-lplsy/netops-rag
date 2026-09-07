# S1700, S5700, S6700 V600R025C00 配置指南-安全 01-03 本机防攻击配置

## 3 本机防攻击配置

### 3.1 本机防攻击简介

3.2 本机防攻击配置注意事项
3.3 本机防攻击缺省配置
3.4 配置CPU防攻击
3.5 配置端口防攻击
3.6 配置用户级限速
3.7 配置攻击溯源
3.8 配置畸形报文攻击防范
3.9 配置分片报文攻击防范
3.10 配置TCP SYN泛洪攻击防范
3.11 配置UDP泛洪攻击防范
3.12 配置ICMP泛洪攻击防范
3.13 维护本机防攻击
3.14 本机防攻击配置举例
3.15 常见配置错误
3.1 本机防攻击简介
定义
本机防攻击是为了保证CPU对正常业务的处理而设计的一种CPU保护机制。网络中存
在着大量需要正常上送CPU的报文和针对CPU（Central Processing Unit）的恶意攻击
报文。
● 如果正常上送CPU的报文如果数量巨大，会导致CPU占用率过高，设备性能下
降，从而影响业务正常运行。

● 如果CPU长时间繁忙的处理恶意攻击报文，会导致其他业务中断甚至系统中断。
基于上面两种情况考虑，设备提供了本机防攻击功能。当CPU接收的正常业务报文或
恶意攻击报文数量较多时，确保CPU能够正常运行，从而保证业务的正常运行。
功能简介
本机防攻击的基本功能包括CPU防攻击、端口防攻击、用户级限速、攻击溯源和攻击
防范等。如图3-1所示，本机防攻击通过多级安全机制，实现对设备的分级保护。
图 3-1 本机防攻击的防护分级
第一级：通过过滤器、攻击溯源惩罚丢弃功能等直接丢弃上送CPU的恶意报文。
第二级：基于协议报文CPCAR（Control Plane Committed Access Rate）的限速。对
上送CPU的报文按照协议类型进行速率限制，保证每种协议上送CPU的报文不会过
多。
控制CPCAR是CPU防攻击的核心部分。CPCAR是基于设备对协议报文进行限速，用户
级限速是基于发起攻击的用户MAC地址对协议报文进行限速。
第三级：基于队列的调度和限速。协议报文CPCAR限速之后，设备可对一类协议再分
配一个队列，各个队列之间按照权重或优先级方式调度，在有冲突的情况下高优先级
的队列优先处理。同时，可以针对每个队列进行限速，限制各个队列向CPU上送报文
的最大速率。对于超过队列最大速率的协议报文，设备会直接丢弃。
其中，端口防攻击的限速处理方式就是将协议报文移入低优先级队列处理。
第四级：所有报文统一限速。该功能是为了限制CPU处理的报文总数，保证CPU在其
正常处理能力范围内尽可能多的处理报文。
在进行所有报文统一限速之前，设备支持通过分析上送CPU处理的报文的内容和行
为，判断报文是否具有攻击特性，并对具有攻击特性的报文执行丢弃或限速等攻击防
范措施。攻击防范主要包含畸形报文攻击防范、分片报文攻击防范、TCP SYN泛洪攻
击防范、UDP泛洪攻击防范和ICMP泛洪攻击防范。

### 3.2 本机防攻击配置注意事项

License 依赖本机防攻击无需License许可即可使用。
硬件依赖表 3-1 支持本特性的硬件

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

特性限制表 3-2 本特性的使用限制

| 特性 | 特性限制 |
|---|---|
| CPCAR | 对于S6730E-H-V2系列，S6750E-S系列，S6730-S-V2系列，S5755-H 系列，S5732-H-V2系列，S6730-H-V2系列，S6750-S系列：从V600R022C10版本开始，said-ping协议报文上送CPU可配置限速最大值从10000修改为5000。如果在V600R022C10版本之前配置了超过 5000的car值，会导致该配置恢复失败。 |
| CPCAR | 对于S6750-H系列，S6730E-H-V2系列，S6750E-S系列，S6730-S-V2 系列，S5755-H系列，S6780-H系列，S5732-H-V2系列，S6730-H-V2 系列，S6750-S系列： CPCAR支持的协议中，部分协议不支持丢包监控。具体支持丢包监控的协议可通过display cpu-defend drop-packet record命令的packet-type 参数查询。 |
| 攻击溯源 | 端口防攻击对单播类协议报文不生效 |
| 攻击溯源 | 1. 当攻击协议类型较多时，如果同时攻击的协议在同一组队列，由于队列限速或CPU端口限速的影响，协议上送CPU的报文速率低于端口防攻击惩罚门限，无法进行防攻击惩罚。 2. 当单个协议的端口防攻击阈值超过队列限速或CPU端口限速时，协议上送CPU的报文速率低于端口防攻击惩罚门限，无法进行防攻击惩罚。 |
| 攻击溯源 | 端口安全丢弃的报文无法触发端口防攻击 |
| ARPSec | 对于S6750-H系列，S6730E-H-V2系列，S6750E-S系列，S6730-S-V2 系列，S5755-H系列，S6780-H系列，S5732-H-V2系列，S6730-H-V2 系列，S5755-S系列，S6750-S系列：不支持同时开启动态ARP检测和M-LAG功能。 |
| ARPSec | DAI约束对于产品S1730S-S3系列，S5735S-L3系列，S5735S-S3系列： DAI对流策略修改vlan后的ARP报文不生效对于产品S5732-H-V2系列，S5735-L-V2系列，S5735-S-V2系列， S5735E-L-V2系列，S5735E-S-V2系列，S5735I-H-V2系列，S5735I-L- V2系列，S5735I-S-V2系列，S5735R-L-V2系列，S5735R-S-V2系列， S5755-H系列，S5755-S系列，S6730-H-V2系列，S6730-S-V2系列， S6730E-H-V2系列，S6750-H系列，S6750-S系列，S6750E-S系列， S6780-H系列： 1、DAI对流策略修改vlan后的ARP报文不生效； 2、VXLAN场景中：DAI对于vxlan隧道场景的ARP报文不生效； 3、VXLAN场景中：如果在绑定了BD的VLAN视图下使能DAI，则此 VLAN维度的DAI功能不生效。可以通过在BD下使能DAI功能替代。 |
| ARPSec | 1、EAI叠加VLANIF，EAI功能不生效。 2、在Super-VLAN下使能出口ARP检测功能，出口ARP检测功能无效（Super-VLAN场景会创建VLANIF接口）。 |

| 特性 | 特性限制 |
|---|---|
| ARPSec | 对于S6750-H系列，S1730S-S3系列，S6730E-H-V2系列，S6750E-S系列，S6730-S-V2系列，S5735S-L3系列，S5755-H系列，S6780-H系列，S5732-H-V2系列，S6730-H-V2系列，S5755-S系列，S6750-S系列：同一个VLAN下，不允许同时配置EAI以及ARP二层代答。 |

### 3.3 本机防攻击缺省配置

本机防攻击的主要缺省配置如下表所示。
表 3-3 CPU 防攻击缺省配置

| 参数 | 缺省配置 |
|---|---|
| 防攻击策略 | 设备自带的一个名称为default的防攻击策略，并且该策略已被应用。 |
| 协议报文的CPCAR值 | 设备对上送CPU的报文按照default策略缺省的限速值进行限速，可通过命令 display cpu-defend configuration查看。 |
| 上送到CPU的所有报文的CPCAR值 | 上送设备CPU的报文CAR缺省速率可以通过命令display cpu-defend configuration查看。 |
| 协议联动功能 | 具体可通过命令application-apperceive enable查看支持的报文类型。 |
| 动态自适应调整协议报文的默认CPCAR 值 | 具体可通过命令cpu-defend dynamic- adjust enable查看支持的报文类型。 |
| 过滤器功能 | 未配置过滤器。 |
| 主机防攻击功能 | 未开启主机防攻击功能。 |

表 3-4 端口防攻击缺省配置

| 参数 | 缺省配置 |
|---|---|
| 端口防攻击支持防范的报文类型 | 具体可通过命令auto-port-defend protocol disable查看支持的报文类型。 |
| 端口防攻击功能的状态 | 已开启。 |

| 参数 | 缺省配置 |
|---|---|
| 端口防攻击的检查阈值 | 端口防攻击的检查阈值，缺省情况下， XLDP为默认CAR10%，其他协议为默认 CAR80%。缺省情况下，一般的款型IP分片报文端口防攻击的检查阈值为1228pps。缺省情况下，S5735I-L-V2、S5735I-S- V2、S5735I-H-V2、S5735S-L3、 S1730S-S3、S5735R-L-V2、S5735E-L- V2、S5735-L-V2、S5735S-S3、 S5735R-S-V2、S5735E-S-V2、S5735-S- V2款型IP分片报文的检测阈值为 320pps。缺省情况下，S5755-S款型IP分片报文的检测阈值为614pps。 |
| 端口防攻击的采样比 | 采样比为8，即每8个报文采样1个报文。 |
| 端口防攻击的老化探测周期 | 300秒。 |

表 3-5 用户级限速缺省配置

| 参数 | 缺省配置 |
|---|---|
| 用户级限速支持限制的报文类型 | 具体可通过命令cpu-defend host-car查看支持的报文类型。 |
| 用户级限速功能的状态 | 全局和接口下的用户级限速功能均已开启。 |
| 用户级限速的限速值 | 20pps。 |

表 3-6 攻击溯源缺省配置

| 参数 | 缺省配置 |
|---|---|
| 攻击溯源防范的报文类型 | 具体可通过命令auto-defend protocol 查看支持的报文类型。 |
| 攻击溯源功能的状态 | 已开启。 |

| 参数 | 缺省配置 |
|---|---|
| 攻击溯源的检查阈值 | 对于S6780-H、S6750-H、S6730E-H- V2、S6730-H-V2、S6730-S-V2、 S5732-H-V2、S6750E-S、S6750-S、 S5755-S，S5755-H，缺省情况下，攻击溯源事件上报阈值为128pps。对于S5735I-L-V2、S5735I-S-V2、 S5735I-H-V2、S5735S-L3、S1730S- S3、S5735R-L-V2、S5735E-L-V2、 S5735-L-V2、S5735S-S3，S5735R-S- V2，S5735E-S-V2，S5735-S-V2，缺省情况下，攻击溯源事件上报阈值为 60pps。 |
| 攻击溯源的采样比 | 采样比为8，即每8个报文采样1个报文。 |
| 攻击溯源的溯源模式 | 基于源IP地址和基于源MAC地址溯源。 |
| 攻击溯源的惩罚措施 | 未开启。 |

表 3-7 畸形报文攻击防范、分片报文攻击防范、TCP SYN 泛洪攻击防范、UDP 泛洪攻击防范和 ICMP 泛洪攻击防范的缺省配置

| 参数 | 缺省配置 |
|---|---|
| 畸形报文攻击防范功能 | 已开启 |
| 分片报文攻击防范功能 | 已开启 |
| 分片报文限制速率 | 155000000bit/s |
| TCP Syn攻击防范功能 | 已开启 |
| TCP Syn泛洪报文限制速率 | 155000000bit/s |
| UDP泛洪攻击防范功能 | 已开启 |
| ICMP泛洪攻击防范功能 | 已开启 |
| ICMP泛洪报文限制速率 | 155000000bit/s |

### 3.4 配置CPU防攻击

#### 3.4.1 了解CPU防攻击

CPU 防攻击的核心是 CPCAR 。设备支持通过命令行修改 CPCAR ，包括协议报文的CPCAR、上送到CPU的所有报文的CPCAR以及协议联动后的CPCAR。并且，在默认CPCAR不能满足业务需求时，支持动态自适应调整协议报文的默认CPCAR。此外，CPU防攻击还提供了过滤器功能，根据定义的ACL来处理符合特征的报文。

协议联动功能协议联动是指设备对基于会话连接的应用层数据的保护功能。当协议会话连接建立后，基于协议的默认CPCAR就不再起作用，设备以协议联动设定的CPCAR对建立会话连接的报文进行限速。通常，协议联动设定的CPCAR要比默认CPCAR大很多，以此来保证业务运行的可靠性和稳定性。
例如，FTP协议，当协议启动但没有文件传输的情况下，设备通过默认CPCAR对FTP报文进行限速；当设备进行文件传输时，设备检测到协议会话连接建立，对建立会话连接的FTP报文通过协议联动设定的CPCAR进行限速，以避免文件传输时出现报文流量瞬间激增超过默认CPCAR，导致传输失败的情况出现。
动态自适应调整协议报文的默认CPCAR值动态自适应调整协议报文的默认CPCAR值应用在用户接入相关的协议报文上，主要解决协议报文默认CPCAR值无法满足上送速率的场景。开启该功能后，设备会根据协议报文的丢包情况和CPU占用率调整默认CPCAR值。
例如，用户通过ARP请求报文触发认证上线，当大规模用户认证的情况下，设备收到的ARP请求报文速率超过默认CPCAR值导致丢包，此时设备会根据丢包率和CPU占用率调整协议报文的CPCAR值。
过滤器功能过滤器功能是指通过定义ACL来设置过滤器，设备通过ACL把符合特征的用户纳入到过滤器中，被纳入过滤器的用户所发的报文到达设备后均根据ACL规则进行处理。如果ACL规则中的动作为deny，设备会直接丢弃该报文；如果ACL规则中的动作为permit，设备会提高报文优先级。

#### 3.4.2 配置CPCAR值

背景信息为了减少上送CPU的报文数量，降低不同类型报文的相互影响以达到保护CPU的目的，设备支持对上送CPU的报文进行分类限速，主要分为协议报文CPCAR限速、上送CPU的所有协议报文限速和协议联动限速。
● 协议联动限速的优先级最高，如果还配置了协议报文CPCAR限速和上送CPU的所有协议报文限速，则设备以协议联动限速值为准。
● 如果没有配置协议联动限速，但同时配置了协议报文CPCAR限速和上送CPU的所有协议报文限速，则设备以二者中的最小限速值为准。
操作步骤步骤1 进入系统视图。
system-view步骤2 创建防攻击策略并进入防攻击策略视图。
cpu-defend policy policy-name步骤3 配置上送CPU报文的限速方式。
● 配置协议报文 CPCAR 限速。
car packet-type packet-type pps pps-value
● 配置上送到CPU的所有报文的CPCAR。
car all-packets pps pps-value

缺省情况下，上送设备CPU的报文CAR速率可以通过命令display cpu-defend configuration查看。
● 配置协议联动限速。
a. 开启协议联动功能。
application-apperceive packet-type enable
b. 配置协议连接建立时协议报文的CPCAR值。
linkup-car packet-type packet-type pps pps-value
c. 配置协议联动触发惩罚的比例阈值。
linkup session anti-attack ratio-threshold rate-value-percent缺省情况下，触发惩罚的比例阈值为50%。
步骤4 （可选）配置丢弃上送CPU的报文。
deny packet-type packet-type缺省情况下，设备不会丢弃上送CPU的报文。
步骤5 （可选）配置防攻击策略的描述信息。
description description缺省情况下，防攻击策略没有配置描述信息。
步骤6 返回系统视图。
quit步骤7 应用防攻击策略。
● 批量配置防攻击策略。
cpu-defend-policy policy-name batch slot { start-slot [ to end-slot ] } &<1-12>
● 单独配置防攻击策略。
cpu-defend-policy policy-name [ slot slot-id | mcu ]创建防攻击策略之后，必须将策略在系统视图下应用，否则防攻击策略不会生效。
----结束

#### 3.4.3 （可选）配置动态自适应调整协议报文的默认CPCAR值

背景信息协议报文默认CPCAR值无法满足报文上送速率时，可以配置动态自适应调整协议报文的默认 CPCAR 值功能。 CPCAR 值的动态自适应调整记录可通过 display cpu-defend dynamic-adjust history-record命令进行查看。
设备支持的CPCAR值动态自适应调整功能的协议报文类型及其调整后的最大CPCAR值如下表所示：

| 协议报文类型 | 协议报文说明 | 调整后的最大CPCAR值 |
|---|---|---|
| arp-reply | ARP响应报文 | 2倍默认值 |
| arp-request | ARP请求报文 | 2倍默认值 |
| arp-request-uc | 单播ARP请求报文 | 2倍默认值 |
| dhcp-reply | DHCP应答报文 | 1.5倍默认值 |

| 协议报文类型 | 协议报文说明 | 调整后的最大CPCAR值 |
|---|---|---|
| dhcp-request | DHCP请求报文 | 1.5倍默认值 |
| dhcp-discovery 说明 S6780-H、S6750-H、 S5755-S不支持该参数。 | DHCP发现报文 | 1.5倍默认值 |
| nd | IPv6邻居发现协议报文 | 2倍默认值 |
| pim | PIM单播报文 | 2倍默认值 |
| pim-mc | PIM组播报文 | 2倍默认值 |
| igmp | IGMP报文 | 2倍默认值 |

说明仅S6780-H、S6750-H、S6730E-H-V2、S6730-S-V2、S6730-H-V2、S5732-H-V2、S5755-S、S6750E-S、S6750-S和S5755-H系列支持配置动态自适应调整协议报文的默认CPCAR值。
操作步骤步骤1 进入系统视图。
system-view步骤2 开启动态自适应调整协议报文的默认CPCAR值。
cpu-defend dynamic-adjust [ packet-type packet-type ] enable如果不指定packet-type参数，则所有支持该功能的协议报文类型均开启该功能。
----结束

#### 3.4.4 （可选）配置协议报文限速的丢包监控

背景信息协议报文的速率超过其对应的CPCAR值后，设备会丢弃超过限速值的报文。如果希望查看哪些报文被丢弃，可以使能协议报文限速丢包监控功能。
说明仅S6750-H、S6730E-H-V2、S6730-S-V2、S6730-H-V2、S6780-H、S6750E-S、S6750-S、S5732-H-V2和S5755-H系列支持该配置。配置协议报文限速的丢包监控。
操作步骤步骤1 进入系统视图。
system-view步骤 2 使能协议报文限速丢包监控功能。
undo cpu-defend drop-packet monitor disable缺省情况下，协议报文限速丢包监控功能处于使能状态。

步骤3 配置由于超过协议报文限速而被丢弃的报文上送CPU的限速值。
cpu-defend drop-packet pps pps-value缺省情况下，由于超过协议报文限速而被丢弃的报文上送CPU的限速值为64 pps。
----结束

#### 3.4.5 （可选）配置过滤器

背景信息设备支持通过ACL灵活设置过滤器。过滤器应用的ACL需要注意以下几点：
● 过滤器应用的ACL，按照其rule配置的实际动作执行。
● 过滤器应用的ACL不支持以下参数，若ACL配置了以下任一参数，则过滤器无效：
– 基本ACL：vpn-instance
– 高级 ACL ： vpn-instance 、 icmp-type 、 igmp-type 、 source-pool 、source-port-pool、destination-pool、destination-port-pool
– 二层ACL：802.3
– 基本ACL6：vpn-instance
– 高级ACL6：destination、vpn-instance、icmpv6-type操作步骤步骤1 进入系统视图。
system-view步骤2 创建防攻击策略并进入防攻击策略视图。
cpu-defend policy policy-name步骤3 配置过滤器。
filter filter-id acl { acl-number | ipv6 ipv6-acl-number } [ interface { interface-type interface-number1 [ to interface-type interface-number2 ] } &<1-8> ] [ vlan { vlan-id1 [ to vlan-id2 ] } &<1-8> ]步骤4 返回系统视图。
quit步骤5 应用防攻击策略。
● 批量配置防攻击策略。
cpu-defend-policy policy-name batch slot { start-slot [ to end-slot ] } &<1-12>
● 单独配置防攻击策略。
cpu-defend-policy policy-name [ slot slot-id | mcu ]创建防攻击策略之后，必须将策略在系统视图下应用，否则防攻击策略不会生效。
----结束

#### 3.4.6 （可选）配置主机防攻击

背景信息配置了ssh server acl、telnet server acl命令后，SSH、Telnet报文会上送CPU。配置了主机防攻击功能后，这些报文会匹配硬件ACL，当报文匹配了硬件ACL中的deny规则时，会被直接丢弃、不会再上送CPU，因此可以避免影响其他正常报文的上送。
操作步骤步骤1 进入系统视图。
system-view步骤2 开启主机防攻击功能。
cpu-defend local-host anti-attack enable
----结束

#### 3.4.7 检查配置结果

操作步骤
● 执行命令display cpu-defend policy [ policy-name ]，查看防攻击策略的配置信息。
● 执行命令display cpu-defend configuration [ packet-type packet-type ] { all | slot slot-id | mcu }，查看上送CPU的协议报文的速率配置信息。
● 执行命令display cpu-defend dynamic-adjust history-record [ packet-type packet-type ] { all | slot slot-id | mcu }，查看有线方式下，协议报文CPCAR值的动态自适应调整的历史记录。
● 执行命令display cpu-defend drop-packet record [ packet-type packet-type ] [ slot slot-id ]，查看由协议报文限速而产生的丢包记录。
仅S6780-H、S6750-H、S6730E-H-V2、S6730-H-V2、S6730-S-V2、S5732-H- V2、S6750E-S、S6750-S和S5755-H系列支持display cpu-defend drop-packet record命令。
● 执行命令display cpu-defend linkup statistics [ packet-type packet-type ] { all | slot slot-id }，查看协议联动功能的统计信息。
● 执行命令display cpu-defend linkup configuration [ packet-type packet- type ] { all | slot slot-id } ，查看协议联动功能的配置信息。
● 执行命令display cpu-defend local-host anti-attack [ slot slot-id ]，查看配置了主机防攻击功能后，报文匹配硬件ACL的统计信息及对应协议绑定ACL的编号和状态。
● 执行命令display cpu-defend rate [ packet-type packet-type ] { all | slot slot- id | mcu }，查看协议报文的CPCAR。
● 执行命令display cpu-defend statistics [ packet-type packet-type ] { all | slot slot-id | mcu }，查看上送CPU的报文统计信息。
ICMP快回功能开启的情况下，不区分统计ICMPv4和ICMPv6报文，ICMPv4和ICMPv6报文的总统计计数记录在回显字段icmp中。
● 执行命令display cpu-defend filter statistics [ slot slot-id ]，查看基于过滤器丢弃的报文统计信息。

对于环回报文，只统计丢包数，不统计丢弃字节数。
----结束

### 3.5 配置端口防攻击

#### 3.5.1 了解端口防攻击

端口防攻击是针对DoS攻击的一种防御方式。它基于端口维度进行防御，可以避免攻击端口的协议报文挤占带宽，其他端口的协议报文无法正常上送CPU处理而造成的业务中断。
端口防攻击的处理流程如下：
1. 基于端口维度进行报文解析，并统计收到的端口防攻击所防范的协议报文的数量。
2. 当单位时间上送CPU的报文数量超过了端口防攻击检查阈值时，就认为该端口存在攻击。
3. 检测到攻击后，设备会发送日志。并将产生攻击的端口上收到的未超出协议限速值（该值等同于防攻击策略里协议报文的CPCAR值）的报文移入低优先级队列后再上送CPU处理；超出限速值的报文直接丢弃。
端口防攻击的限速处理方式，相比较攻击溯源的惩罚措施，对设备正常业务造成的影响更小。
此外，端口防攻击还提供了白名单功能、老化探测功能和端口防攻击事件上报功能。
白名单功能：将合法用户加入到白名单中，设备不对白名单内的用户报文进行端口防攻击处理，从而保证合法用户的报文能够正常上送CPU处理。白名单可以通过ACL或端口灵活设置。
老化探测功能：设备一旦检测到存在攻击的端口，就会在老化探测周期内（假设为T秒）对该端口的攻击报文持续进行移入低优先级队列的处理。达到T秒之后，设备会再次计算该端口收到协议报文的速率，如果该值超过了检查阈值（即存在攻击），则继续对其进行移入低优先级队列的处理；反之，则正常上送。
请根据设备CPU使用率和业务运行情况，配置合理的端口防攻击老化探测周期。老化探测周期过短，设备频繁启动端口报文速率的检测，消耗 CPU 资源；老化探测周期过长，设备长时间进行端口防攻击限速，可能会导致过多的协议报文未被CPU及时处理而影响该协议对应的正常业务。
端口防攻击事件上报功能：当端口存在攻击时，设备以事件（event）上报的方式提醒管理员，以便管理员采取一定的措施来保护设备。

#### 3.5.2 配置端口防攻击

背景信息通过部署基于端口的防攻击功能，可以有效控制从端口上送到CPU处理的报文数量。

操作步骤步骤1 进入系统视图。
system-view步骤2 创建防攻击策略并进入防攻击策略视图。
cpu-defend policy policy-name步骤3 开启端口防攻击功能。
auto-port-defend enable步骤4 （可选）关闭指定协议的端口防攻击功能。
auto-port-defend protocol packet-type disable对于如果管理员发现设备检测出的多种攻击报文类型中，仅有少部分才是真正的攻击报文，则可以删除不必要的报文类型，避免设备因对过多的协议报文进行限速而影响正常业务。
步骤5 （可选）配置基于端口防攻击的协议报文检查阈值。
auto-port-defend protocol packet-type threshold threshold-value步骤 6 （可选）配置基于端口防攻击的协议报文采样比。
auto-port-defend sample sample-value步骤7 （可选）配置端口防攻击的老化探测周期。
auto-port-defend aging-time aging-time步骤8 （可选）配置端口防攻击的白名单。
auto-port-defend whitelist whitelist-id { acl acl-number | acl ipv6 ipv6-acl-number | interface interface- type interface-number }缺省情况下，没有配置端口防攻击的白名单。
说明通过ACL设置端口防攻击白名单时需要注意以下几点：
● 使用ACL设置白名单时，需要配置ACL和对应的rule。
● ACL可以是基本ACL、高级ACL、二层ACL、基本ACL6和高级ACL6。
ACL中配置的rule，其动作无论配置为permit还是deny，命中该ACL的报文均会被当作合法
●报文，不对其进行端口防攻击处理。
● 如果ACL中配置rule为空，即没有配置rule的动作，则白名单功能不生效。
● 如果ACL的rule通过某协议定义，则需要保证端口防攻击功能支持该协议。
● 设备ACL资源不足，可能会导致白名单功能失效。
步骤9 （可选）开启端口防攻击事件上报功能。
undo auto-port-defend alarm disable缺省情况下，端口防攻击事件上报功能处于开启状态。
步骤10 返回系统视图。
quit步骤11 应用防攻击策略。
● 批量配置防攻击策略。
cpu-defend-policy policy-name batch slot { start-slot [ to end-slot ] } &<1-12>
● 单独配置防攻击策略。
cpu-defend-policy policy-name [ slot slot-id | mcu ]

创建防攻击策略之后，必须将策略在系统视图下应用，否则防攻击策略不会生效。
----结束任务示例在名称为test的防攻击策略中，开启端口防攻击功能，其中端口防攻击功能的协议报文检查阈值采用默认值、采样比是7、老化探测周期是200秒，并且接口10GE1/0/1收到的所有协议报文均合法，配置端口防攻击白名单，不对该接口应用端口防攻击功能。
<HUAWEI> system-view [HUAWEI] cpu-defend policy test [HUAWEI-cpu-defend-policy-test] auto-port-defend enable [HUAWEI-cpu-defend-policy-test] auto-port-defend sample 7 [HUAWEI-cpu-defend-policy-test] auto-port-defend aging-time 200 [HUAWEI-cpu-defend-policy-test] auto-port-defend whitelist 1 interface 10ge 1/0/1 [HUAWEI-cpu-defend-policy-test] quit [HUAWEI] cpu-defend-policy test

#### 3.5.3 检查配置结果

操作步骤
● 执行命令display cpu-defend policy [ policy-name ]，查看防攻击策略的配置信息。
● 执行命令display cpu-defend auto-port-defend configuration [ slot slot- id ]，查看端口防攻击的配置信息。
● 执行命令display cpu-defend auto-port-defend attack-source [ slot slot- id ]，查看端口防攻击的溯源信息。
● 执行命令display cpu-defend auto-port-defend whitelist slot slot-id，查看端口防攻击的白名单信息。
● 执行命令display cpu-defend auto-port-defend statistics [ slot slot-id ]，查看端口防攻击的报文统计信息。
----结束

### 3.6 配置用户级限速

说明仅S6780-H、S6750E-S、S6750-S、S6730E-H-V2、S6730-S-V2、S6730-H-V2、S6750-H、S5732-H-V2和S5755-H系列支持配置用户级限速。

#### 3.6.1 了解用户级限速

用户侧主机容易遭受病毒攻击，借此向网络中发送大量的协议报文，导致设备的CPU占用率过高，性能下降，从而影响正常的业务，此时，管理员可以配置用户级限速功能。用户级限速功能是指基于用户MAC地址识别用户，对用户的特定报文进行限速，使得单个用户发起攻击时只对该用户进行限速，从而不影响其他用户。与CPCAR基于设备，端口防攻击基于端口相比，基于用户 MAC 地址进行限速能够精确到每个用户，对正常用户的影响更小。
用户级限速的处理流程如下：

1. 设备对收到的用户协议报文的源MAC地址进行哈希计算，将收到的不同源MAC地
址的报文放到不同的限速桶中。
2. 当单位时间限速桶内的报文超过了限速值时，该限速桶会丢弃收到的报文，并且
每隔10分钟对限速桶内的丢包数目进行统计。如果10分钟内限速桶丢弃的报文数
目超过2000个，设备会发送该限速桶的丢包日志。如果同时存在多个限速桶丢包
数目超过2000个，设备只发送丢包数目最多的10个限速桶的丢包日志。

#### 3.6.2 配置用户级限速

背景信息配置用户级限速功能，基于用户MAC地址进行精确限速，减少对正常用户的影响。
操作步骤步骤1 进入系统视图。
system-view步骤2 全局开启用户级限速功能。
cpu-defend host-car enable步骤3 配置用户级限速的限速值。
cpu-defend host-car [ mac-address mac-address | car-id car-id ] pps pps-value步骤4 配置用户级限速可以限制的报文类型。
cpu-defend host-car { { 8021x | arp | dhcp-request | dhcpv6-request | nd | mac-miss } * | all }步骤5 进入指定的接口视图。
interface interface-type interface-number步骤6 开启接口下的用户级限速功能。
undo host-car disable缺省情况下，接口下的用户级限速功能开启。
当全局开启用户级限速功能时，接口下的用户级限速功能一同被开启，此时可以在接口视图下配置host-car disable，按需关闭接口下的用户及限速功能。网络侧的接口建议关闭接口下的用户级限速功能，避免DHCP、ARP等协议报文被丢弃。
---- 结束任务示例开启用户级限速功能，并配置用户级限速的限速值为15pps、仅限制ARP报文的速率。
<HUAWEI> system-view [HUAWEI] cpu-defend host-car enable [HUAWEI] cpu-defend host-car pps 15 [HUAWEI] cpu-defend host-car arp

#### 3.6.3 （可选）配置用户级限速的丢包监控

背景信息

使能用户级限速功能后，如果单位时间内设备接收的来自同一源MAC地址的报文数量超过限速值，设备会丢弃超过限速值的报文。通过配置用户级限速的丢包监控功能，可以方便用户查看哪些报文被丢弃。
说明仅S6750-H、S6730E-H-V2、S6730-S-V2、S6730-H-V2、S6780-H、S6750E-S、S6750-S、S5732-H-V2和S5755-H系列支持配置协议报文限速的丢包监控。
操作步骤步骤1 进入系统视图。
system-view步骤2 使能用户级限速的丢包监控功能。
undo cpu-defend host-car drop-packet monitor disable缺省情况下，用户级限速的丢包监控功能处于使能状态。
步骤3 配置由于用户级限速而被丢弃的报文上送CPU的限速值。
cpu-defend host-car drop-packet pps pps-value缺省情况下，用户级限速的丢包监控的限速值为64 pps。
----结束

#### 3.6.4 检查配置结果

操作步骤
● 执行命令display cpu-defend host-car [ mac-address mac-address ] statistics [ slot slot-id ]，查看用户级限速丢弃的报文数。
执行命令display
● cpu-defend host-car drop-packet record [ car-id car-id ] [ slot slot-id ]，查看由于用户级限速而产生的丢包记录。
----结束

### 3.7 配置攻击溯源

#### 3.7.1 了解攻击溯源

攻击溯源能够防御DoS攻击。如图3-2所示，攻击溯源包括报文解析、流量分析、攻击源识别和发送日志告警通知管理员以及实施惩罚四个过程。
1. 从IP地址、MAC地址以及端口三个维度对上送CPU的报文进行报文解析，其中端口通过“物理端口+VLAN”标识。
2. 根据IP地址、MAC地址或者端口信息统计接收到的协议报文数量。
3. 当单位时间上送CPU的报文数量超过了阈值时，则认为是攻击。
4. 当检测到攻击后，会发送日志、告警通知管理员或者直接实施惩罚，如丢弃攻击报文。

图 3-2 攻击溯源原理此外，攻击溯源还提供了白名单功能。将合法用户加入到通过白名单中，设备不对白名单内的用户报文进行溯源和攻击惩罚处理，从而保证合法用户的报文能够正常上送CPU处理。白名单可以通过ACL或端口灵活设置。

#### 3.7.2 配置攻击溯源

背景信息配置攻击溯源功能后，设备能够通过分析上送CPU的报文是否会对CPU造成攻击，追溯攻击源并以日志或告警的方式通知管理员，以便管理员采取措施对攻击源进行防御部署。
操作步骤步骤1 进入系统视图。
system-view步骤2 创建防攻击策略并进入防攻击策略视图。
cpu-defend policy policy-name步骤 3 开启攻击溯源功能。
auto-defend enable步骤4 配置攻击溯源检查阈值。
auto-defend threshold threshold-value步骤5 配置攻击溯源的采样比。
auto-defend attack-packet sample sample-value步骤6 配置攻击溯源防范的报文类型。
auto-defend protocol { { arp | icmp | dhcp | ttl-expired | tcp | udp | udpv6 | 8021x | telnet | dhcpv6 | dns | nd | icmpv6 | tcpv6 | igmp | mld } * | all }步骤7 配置攻击溯源的溯源模式。
auto-defend trace-type { source-mac | source-ip | source-portvlan } *

溯源模式的优先级由高到低为：基于MAC地址>基于IP地址>基于接口和VLAN信息，配置多种溯源模式时，按照上述优先级生效。
步骤8 （可选）配置攻击溯源的白名单。
auto-defend whitelist whitelist-id { acl acl-number | acl ipv6 ipv6-acl-number | interface interface-type interface-number }缺省情况下，没有攻击溯源的白名单。
说明通过ACL设置攻击溯源白名单时需要注意以下几点：
● 使用ACL设置白名单时，需要配置ACL和对应的rule，如果ACL中配置rule为空，即没有配置rule的动作，则白名单功能不生效。
● ACL可以是基本ACL、高级ACL、二层ACL、基本ACL6和高级ACL6。
● ACL中配置的rule，其动作无论配置为permit还是deny，命中该ACL的报文均会被当作合法报文，不对其进行溯源和攻击惩罚处理。
● 如果ACL的rule通过某协议定义，则需要保证攻击溯源功能支持该协议。
● 设备ACL资源不足，可能会导致白名单功能失效。
步骤9 （可选）配置攻击溯源事件上报功能。
1. 开启攻击溯源事件上报功能。
auto-defend alarm enable缺省情况下，攻击溯源事件上报功能处于关闭状态。
2. 配置攻击溯源事件上报阈值。
auto-defend alarm threshold alarm-threshold对于S6780-H、S6750-H、S6730E-H-V2、S6730-S-V2、S6730-H-V2、S5732- H-V2、S6750E-S、S6750-S、S5755-S、S5755-H，缺省情况下，攻击溯源事件上报阈值为128pps。
对于S5735I-L-V2、S5735I-S-V2、S5735I-H-V2、S5735S-L3、S1730S-S3、S5735R-L-V2、S5735E-L-V2、S5735-L-V2、S5735S-S3，S5735R-S-V2，S5735E-S-V2，S5735-S-V2，缺省情况下，攻击溯源事件上报阈值为60pps。
步骤10 配置攻击溯源惩罚措施。
auto-defend action { deny [ timeout timeout-num ] | error-down }说明
● error-down是指设备检测到故障后将接口状态设置为ERROR DOWN状态，此时接口不能收发报文，接口指示灯为常灭。
如果配置攻击溯源的惩罚措施是将攻击报文进入的接口ERROR DOWN，则会造成设备业务的中断，接口下合法的用户会受牵连，请谨慎使用。
● 设备不对攻击溯源的白名单用户进行攻击溯源的惩罚。
步骤11 返回系统视图。
quit步骤12 应用防攻击策略。
● 批量配置防攻击策略。
cpu-defend-policy policy-name batch slot { start-slot [ to end-slot ] } &<1-12>
● 单独配置防攻击策略。
cpu-defend-policy policy-name [ slot slot-id | mcu ]

创建防攻击策略之后，必须将策略在系统视图下应用，否则防攻击策略不会生效。
----结束任务示例在名称为test的防攻击策略下，开启攻击溯源功能，并配置攻击溯源的检查阈值为200pps、采样比是7、溯源模式是基于源IP地址溯源，并且配置攻击溯源的惩罚措施为丢弃攻击报文。
<HUAWEI> system-view [HUAWEI] cpu-defend policy test [HUAWEI-cpu-defend-policy-test] auto-defend enable [HUAWEI-cpu-defend-policy-test] auto-defend threshold 200 [HUAWEI-cpu-defend-policy-test] auto-defend attack-packet sample 7 [HUAWEI-cpu-defend-policy-test] auto-defend trace-type source-ip [HUAWEI-cpu-defend-policy-test] auto-defend action deny [HUAWEI-cpu-defend-policy-test] quit [HUAWEI] cpu-defend-policy test后续处理配置攻击溯源的惩罚措施为 ERROR DOWN 时，设备在识别出攻击源后，会将攻击报文进入的接口状态置为Down。接口状态被置为Down后，建议先排除攻击，再将接口状态恢复Up。
表 3-8 将接口状态恢复 Up 的方法

| 方法 | 适用场景 | 处理步骤 |
|---|---|---|
| 手动恢复 | ● 预期Down状态的接口数量较少。 ● 接口已经被置为Down状态。 | 对应接口视图下依次执行命令 shutdown和undo shutdown，或者执行命令restart，重启接口。 |
| 自动恢复 | ● 预期Down状态的接口数量较多，逐一手动恢复接口状态工作量大，且可能遗漏部分接口。 ● 接口还未被置为Down状态。该方式对已经是Down状态的接口不生效。 | 在系统视图下执行命令error-down auto-recovery cause auto-defend interval开启接口状态自动恢复为Up 的功能，并设置接口自动恢复为Up的延时时间。可以通过命令display error-down recovery，查看接口状态自动恢复信息。 |

#### 3.7.3 检查配置结果

操作步骤
● 执行命令display cpu-defend policy [ policy-name ]，查看防攻击策略的配置信息。
● 执行命令display auto-defend attack-source [ slot slot-id | history [ slot slot- id ] | trace-type { source-mac | source-ip | source-portvlan } [ slot slot- id ] ]，查看攻击源信息。
● 执行命令display auto-defend configuration [ cpu-defend policy policy- name | slot slot-id ]，查看防攻击策略的攻击溯源配置信息。

● 执行命令display auto-defend whitelist slot slot-id，查看攻击溯源的白名单信
息。
----结束

### 3.8 配置畸形报文攻击防范

#### 3.8.1 了解畸形报文攻击防范

畸形报文攻击是通过向目标设备发送有缺陷的IP报文，使得目标设备在处理这样的IP报文时出错和崩溃，影响目标设备承载的业务正常运行。畸形报文攻击防范是指设备实时检测出畸形报文并予以丢弃，实现对设备的保护。
畸形报文攻击主要分为以下几类：
没有 IP 载荷的泛洪如果IP报文只有20字节的IP报文头，没有数据部分，就认为是没有IP载荷的报文。攻击者经常构造只有IP头部，没有携带任何高层数据的IP报文，目标设备在处理这些没有IP载荷的报文时会出错和崩溃，影响目标设备承载的业务正常运行。
启用畸形报文攻击防范后，设备检测接收到的IP报文是否有载荷，如果没有载荷，则直接将其丢弃。
IGMP 空报文正常的IGMP报文由20字节的IP报文头加上8字节的数据部分组成，总长28个字节。总长度小于28字节的IGMP报文称为IGMP空报文。设备在处理IGMP空报文时会出错和崩溃，影响目标设备承载的业务正常运行。
启用畸形报文攻击防范后，设备检测接收到的IGMP报文是否为空报文，如果是空报文，则直接将其丢弃。
LAND 攻击LAND攻击是攻击者利用TCP连接三次握手机制中的缺陷，向目标主机发送一个源地址和目的地址均为目标主机、源端口和目的端口相同的SYN报文，目标主机接收到该报文后，将创建一个源地址和目的地址均为自己的 TCP 空连接，直至连接超时。在这种攻击方式下，目标主机将会创建大量无用的TCP空连接，耗费大量资源，直至设备瘫痪。
启用畸形报文攻击防范后，设备采用检测TCP SYN报文的源地址和目的地址是否一致或源端口和目的端口是否一致的方法来避免LAND攻击。如果TCP SYN报文中的源地址和目的地址一致，或者源端口和目的端口一致，则认为是畸形报文攻击，丢弃该报文。
Smurf 攻击Smurf 攻击是指攻击者向目标网络发送源地址为目标主机地址、目的地址为目标网络广播地址的ICMP请求报文，目标网络中的所有主机接收到该报文后，都会向目标主机发送ICMP响应报文，导致目标主机收到过多报文而消耗大量资源，甚至导致设备瘫痪或网络阻塞。

启用畸形报文攻击防范后，设备通过检测ICMP请求报文的目标地址是否是广播地址或子网广播地址来判断是否是Smurf攻击。如果检测到此类报文，直接将其丢弃。
TCP 标志位非法攻击TCP报文包含6个标志位：URG、ACK、PSH、RST、SYN、FIN，不同的系统对这些标志位组合的应答是不同的：
● 6个标志位全部为1，就是圣诞树攻击。设备在受到圣诞树攻击时，会造成系统崩溃。
● SYN和FIN同时为1，如果端口是关闭的，会使接收方应答一个RST | ACK消息；如果端口是打开的，会使接收方应答一个SYN | ACK消息，这可用于主机探测(主机在线或者下线)和端口探测（端口打开或者关闭）。
● 6个标志位全部为0，如果端口是关闭的，会使接收方应答一个RST | ACK消息，这可以用于探测主机；如果端口是开放的，Linux和UNIX系统不会应答，而Windows系统将回答RST | ACK消息，这可以探测操作系统类型（Windows系统，Linux和UNIX系统等）。
启用畸形报文攻击防范后，设备会检查 TCP 报文的各个标志位避免 TCP 标志位非法攻击。如果符合下面条件之一，则将该TCP报文丢弃：
● 6个标志位全部为1；
● SYN和FIN位同时为1；
● 6个标志位全部为0。

#### 3.8.2 配置畸形报文攻击防范

背景信息配置畸形报文攻击防范功能后，设备将对收到的上送CPU的报文进行分析处理，判断其是否是几种畸形报文攻击报文类型之一，若是，则直接丢弃畸形报文。
操作步骤步骤1 进入系统视图。
system-view步骤2 开启畸形报文攻击防范功能。
anti-attack abnormal enable说明在系统视图下，执行命令anti-attack enable可以开启所有的攻击防范功能（包括畸形报文攻击防范功能）。
----结束检查配置结果执行命令display anti-attack statistics abnormal，查看设备上畸形报文攻击防范的统计数据。

### 3.9 配置分片报文攻击防范

#### 3.9.1 了解分片报文攻击防范

分片报文攻击是通过向目标设备发送分片出错的报文，使得目标设备在处理分片错误的报文时崩溃、重启或消耗大量的CPU资源，影响目标设备承载的业务正常运行。分片报文攻击防范是指设备实时检测出分片报文并予以丢弃或者限速处理，实现对本设备的保护。
分片报文攻击主要分为以下几类：
分片数量巨大攻击IP报文中的偏移量是以8字节为单位的。正常情况下，IP报文的头部有20个字节，IP报文的最大载荷为65515。对这些数据进行分片，分片个数最大可以达到8189片，对于超过8189的分片报文，设备在重组这些分片报文时会消耗大量的CPU资源。
针对分片数量巨大攻击，如果同一报文的分片数目超过8189个，则设备认为是恶意报文，丢弃该报文的所有分片。
巨大 Offset 攻击攻击者向目标设备发送一个Offset值超大的分片报文，导致目标设备需要分配巨大的内存空间来存放所有分片报文，消耗大量资源。
Offset字段占13个bit，单位为8字节，所以Offset的最大取值为8191。但是在正常情况下，Offset值不会超过8190。这是因为IP报文的最大载荷为65515个字节，如果Offset=8190，8190*8=65520，就超过了65515。所以，正常Offset的最大值是8189，8189*8=65512，最后一片报文最多只有3个字节IP载荷。
设备在收到分片报文时判断Offset是否大于8189，如果大于就当作恶意分片报文直接丢弃。
重复分片攻击重复分片攻击就是把同样的分片报文多次向目标主机发送，存在两种情况：
● 多次发送的分片完全相同，这样会造成目标主机的 CPU 和内存使用不正常；
● 多次发送的分片报文不相同，但Offset相同，目标主机就会处于无法处理的状态：哪一个分片应该保留，哪一个分片应该丢弃，还是都丢弃。这样就会造成目标主机的CPU和内存使用不正常。
启用分片报文攻击防范后，对于重复分片类报文的攻击，设备实现对分片报文进行CAR（Committed Access Rate）限速，保留首片，丢弃其余所有相同的重复分片，保证不对CPU造成攻击。
Syndrop 攻击Syndrop攻击的原理是IP分片错误，第二片包含在第一片之中。即数据包中第二片IP包的偏移量小于第一片结束的位移，而且算上第二片IP包的Data，也未超过第一片的尾部。Syndrop攻击使用了TCP协议，Flag为SYN，而且带有载荷。

如图3-3所示：
● 第一片IP载荷为28字节，IP头部20字节；
● 第二片IP载荷为4字节，IP头部20字节，Offset=24（错误，正确应该是28）。
图 3-3 Syndrop 攻击分片示意图Syndrop攻击会导致系统崩溃或重启。启用分片报文攻击防范后，对于Syndrop攻击，设备会直接丢弃所有分片报文。
NewTear 攻击NewTear攻击是分片错误的攻击。如图3-4所示，protocol使用UDP。
● 第一片IP载荷28字节（包含UDP头部，UDP检验和为0）；
● 第二片IP载荷4字节，offset=24（错误，正确应该是28）。
图 3-4 NewTear 攻击分片示意图NewTear攻击会导致系统崩溃或重启。启用分片报文攻击防范后，对于NewTear攻击，设备会直接丢弃所有分片报文。

Bonk 攻击Bonk攻击是分片错误的攻击。如图3-5所示，protocol使用UDP。
● 第一片IP载荷为36字节（包含UDP头部，UDP检验和为0）；
● 第二片IP载荷为4字节，offset=32（错误，正确应该是36）。
图 3-5 Bonk 攻击分片示意图Bonk攻击会导致系统崩溃或重启。启用分片报文攻击防范后，对于Bonk攻击，设备会直接丢弃所有分片报文。
Nesta 攻击Nesta攻击是分片错误的攻击。如图3-6所示：
● 第一片IP载荷为18，protocol为UDP，检验和为0；
● 第二片offset为48，IP载荷为116字节；
● 第三片offset为0，more frag为1，也就是还有分片，40字节的IP option，都是EOL，IP载荷为224字节。
图 3-6 Nesta 攻击分片示意图Nesta攻击会导致系统崩溃或重启。启用分片报文攻击防范后，对于Nesta攻击，设备会直接丢弃所有分片报文。

#### 3.9.2 配置分片报文攻击防范

背景信息配置分片报文攻击防范功能后，设备将对收到的分片报文进行限速处理。对于超出限速值的分片报文，设备直接丢弃。
操作步骤步骤1 进入系统视图。
system-view步骤2 开启分片报文攻击防范功能。
anti-attack fragment enable说明在系统视图下，执行命令anti-attack enable可以开启所有的攻击防范功能（包括分片报文攻击防范功能）。
步骤 3 配置分片报文的限制速率。
anti-attack fragment car cir cir-num
----结束检查配置结果执行命令display anti-attack statistics fragment，查看设备上分片报文攻击防范的统计数据。

### 3.10 配置TCP SYN泛洪攻击防范

#### 3.10.1 了解TCP SYN泛洪攻击防范

TCP SYN攻击利用了TCP三次握手的漏洞。如图3-7所示，在TCP的3次握手期间，当接收端（目标设备）收到来自发送端（攻击者）的初始SYN报文时，向发送端返回一个SYN+ACK报文。接收端在等待发送端的最终ACK报文时，该连接一直处于半连接状态。如果接收端最终没有收到ACK报文包，则重新发送一个SYN+ACK到发送端。如果经过多次重试，发送端始终没有返回 ACK 报文，则接收端关闭会话并从内存中刷新会话，从传输第一个SYN+ACK到会话关闭大约需要30秒。
在这段时间内，攻击者可能发送大量SYN报文到开放的端口，并且不回应接收端的SYN +ACK报文。接收端内存很快就会超过负荷，且无法再接收任何新的连接，并将现有的连接断开。

图 3-7 TCP SYN 泛洪攻击设备对 TCP SYN 攻击的处理方式如图 3-8 所示。开启 TCP SYN 泛洪攻击防范后，设备对SYN报文进行速率限制，保证设备受到攻击时资源不被耗尽。
TCP图 3-8 TCP SYN 泛洪攻击防范

#### 3.10.2 配置TCP SYN泛洪攻击防范

背景信息配置TCP SYN泛洪攻击防范功能后，设备将对收到的TCP SYN报文进行限速处理。对于超出限速值的TCP SYN报文，设备直接丢弃。

操作步骤步骤1 进入系统视图。
system-view步骤2 开启TCP SYN泛洪攻击防范功能。
anti-attack tcp-syn enable说明在系统视图下，执行命令anti-attack enable可以开启所有的攻击防范功能（包括TCP SYN泛洪攻击防范功能）。
步骤3 配置TCP SYN报文的限制速率。
anti-attack tcp-syn car cir cir-num
----结束检查配置结果执行命令display anti-attack statistics tcp-syn，查看TCP SYN泛洪攻击防范的统计数据。

### 3.11 配置UDP泛洪攻击防范

#### 3.11.1 了解UDP泛洪攻击防范

UDP泛洪攻击是指攻击者在短时间内向目标设备发送大量的UDP报文，导致目标设备负担过重而不能处理正常的业务。UDP泛洪攻击分为以下两类：
● Fraggle攻击Fraggle攻击的原理如图3-9所示。攻击者发送源地址为目标设备IP地址，目的地址为广播地址，目的端口号为7的UDP报文。如果该广播网络中有很多主机都启用了UDP响应请求服务，目标设备将会收到很多主机发送的UDP回应报文，设备处理这些报文会消耗CPU资源，造成系统繁忙，从而达到攻击效果。
开启泛洪攻击防范功能后，设备默认UDP端口号为7的报文是攻击报文，直接将其丢弃。

图 3-9 Fraggle 攻击
● UDP诊断端口攻击攻击者向目标设备的 UDP 诊断端口（ 7-echo ， 13-daytime ， 19-Chargen 等 UDP 端口）发送大量UDP请求报文，形成泛洪，消耗网络带宽资源，并且目标设备为这些请求提供服务回应UDP报文时会消耗CPU资源，造成负担过重而不能处理正常的业务。
开启泛洪攻击防范功能后，设备将UDP端口为7、13和19的报文认为是攻击报文，直接丢弃。

#### 3.11.2 配置UDP泛洪攻击防范

背景信息配置UDP泛洪攻击防范功能后，对于收到的端口号为7、13和19的报文，设备直接丢弃。
操作步骤步骤1 进入系统视图。
system-view步骤2 开启UDP泛洪攻击防范功能。
anti-attack udp-flood enable说明在系统视图下，执行命令anti-attack enable可以开启所有的攻击防范功能（包括UDP泛洪攻击防范功能）。
----结束检查配置结果执行命令display anti-attack statistics udp-flood，查看UDP泛洪攻击防范的统计数据。

### 3.12 配置ICMP泛洪攻击防范

#### 3.12.1 了解ICMP泛洪攻击防范

通常情况下，网络管理员会用Ping程序对网络进行监控和故障排除，大概过程如下：
1. 源设备向接收设备发出ICMP请求报文；
2. 接收设备接收到ICMP请求报文后，会向源设备回应一个ICMP响应报文。
如图3-10所示，如果攻击者向目标设备发送大量的ICMP请求报文，则目标设备会忙于处理这些请求，而无法继续处理其他的数据报文，造成对正常业务的冲击。
图 3-10 ICMP 泛洪攻击设备对ICMP泛洪攻击的处理方式如图3-11所示。开启ICMP泛洪攻击防范后，设备针对ICMP报文进行速率限制，保证设备受到攻击时资源不被耗尽。

图 3-11 ICMP 泛洪攻击防范

#### 3.12.2 配置ICMP泛洪攻击防范

背景信息配置ICMP泛洪攻击防范功能后，设备将对收到的ICMP报文进行限速处理。对于超出限速值的ICMP报文，设备直接丢弃。
操作步骤步骤1 进入系统视图。
system-view步骤2 开启ICMP泛洪攻击防范功能。
anti-attack icmp-flood enable说明在系统视图下，执行命令anti-attack enable可以开启所有的攻击防范功能（包括ICMP泛洪攻击防范功能）。
步骤3 配置ICMP泛洪攻击报文的限制速率。
anti-attack icmp-flood car cir cir-num
----结束检查配置结果执行命令display anti-attack statistics icmp-flood，查看ICMP泛洪攻击防范的统计数据。

### 3.13 维护本机防攻击

日常维护中，还可以清除本机防攻击的相关统计信息。如有需要，可在用户视图下执行以下命令。
须知清除本机防攻击相关的统计信息后，以前的信息将无法恢复，务必仔细确认。
表 3-9 清除本机防攻击相关的统计信息

| 操作 | 命令 |
|---|---|
| 清除上送CPU的报文统计信息 | reset cpu-defend statistics [ packet- type packet-type ] { all | slot slot-id | mcu } |
| 清除协议联动的统计信息 | reset cpu-defend linkup statistics [ packet-type packet-type ] { slot slot- id | all } |
| 清除由于协议报文限速而产生的丢包记录 | reset cpu-defend drop-packet record [ packet-type packet-type ] [ slot slot- id ] 仅S6750-H、S6730E-H-V2、S6730-S- V2、S6730-H-V2、S6780-H、S6750E- S、S6750-S、S5732-H-V2和S5755-H系列支持该命令。 |
| 清除基于过滤器上送CPU的报文统计信息 | reset cpu-defend filter statistics [ slot slot-id ] |
| 清除端口防攻击的报文统计信息 | reset cpu-defend auto-port-defend statistics [ slot slot-id ] |
| 清除端口防攻击溯源信息 | reset cpu-defend auto-port-defend attack-source [ slot slot-id ] |
| 清除用户级限速的报文统计信息 | reset cpu-defend host-car [ mac- address mac-address ] statistics [ slot slot-id ] 仅S6750-H、S6730E-H-V2、S6730-S- V2、S6730-H-V2、S6780-H、S6750E- S、S6750-S、S5732-H-V2和S5755-H系列支持该命令。 |

| 操作 | 命令 |
|---|---|
| 清除由于用户级限速而产生的丢包记录 | reset cpu-defend host-car drop-packet record [ car-id car-id ] [ slot slot-id ] 仅S6750-H、S6730E-H-V2、S6730-S- V2、S6730-H-V2、S6780-H、S6750E- S、S6750-S、S5732-H-V2和S5755-H系列支持该命令。 |
| 清除攻击溯源统计信息 | reset auto-defend attack-source [ slot slot-id ] |
| 清除攻击溯源历史统计信息 | reset auto-defend attack-source history [ slot slot-id ] |
| 基于溯源模式清除攻击溯源统计信息 | reset auto-defend attack-source trace- type { source-mac [ mac-address ] | source-ip [ ip-address | ipv6-address ] | source-portvlan [ interface interface- type interface-number vlan vlan-id [ inner-vlan inner-vlan-id ] ] } [ slot slot-id ] |
| 清除攻击防范的报文统计信息 | reset anti-attack statistics [ abnormal | fragment | tcp-syn | udp-flood | icmp- flood ] |

### 3.14 本机防攻击配置举例

#### 3.14.1 举例：配置CPU防攻击

组网需求如图3-12所示，大量用户通过DeviceA访问Internet，管理员发现攻击者发送大量的ARP Request报文，影响CPU的正常工作，希望能够减小ARP报文对CPU处理正常业务的影响。
图 3-12 配置本机防攻击示例组网图说明本例中interface1，interface2，interface3和interface4分别代表10GE1/0/1，10GE1/0/2，10GE1/0/3，10GE1/0/4。

操作步骤步骤1 配置防攻击策略。
\# 创建防攻击策略。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] cpu-defend policy test1 \# 配置ARP Request报文上送CPU的速率限制。
[DeviceA-cpu-defend-policy-test1] car packet-type arp-request pps 128 [DeviceA-cpu-defend-policy-test1] quit步骤2 全局应用防攻击策略。
[DeviceA] cpu-defend-policy test1
----结束检查配置结果\# 查看配置的防攻击策略的信息。
[DeviceA] display cpu-defend policy test1 ============================================== Policy name: test1 Policy applies on slot: <1> Car packet-type arp-request(pps) : 128 ============================================== \# 查看配置的CAR的信息。
[DeviceA] display cpu-defend configuration all Car configurations on mcu :
---------------------------------------------------------------------- PacketType Status Current(pps) Default(pps) Queue
---------------------------------------------------------------------- arp-miss Enabled 1536 1536 13 arp-reply Enabled 2048 2048 23 arp-request Enabled 128 2048 23 arp-request-uc Enabled 2048 2048 23……配置文件DeviceA的配置文件\# sysname DeviceA \# cpu-defend policy test1

car packet-type arp-request pps 128 \# cpu-defend-policy test1 \# return

#### 3.14.2 举例：配置攻击溯源

组网需求如图3-13所示，位于不同网段的用户通过DeviceA访问Internet。由于接入的用户数量多，DeviceA经常因为处理大量的ARP报文导致CPU使用率高，影响正确业务。
管理员希望设备能够对上送CPU的ARP报文进行分析，将超过阈值的报文判定为攻击报文，并找出攻击源用户或者源接口，通过日志、告警的方式通知管理员，以便管理员采取一定的安全措施来保护CPU。此外，Net2网段的用户为固定合法用户，需要确保该网段用户的ARP报文能够正常上送CPU。
图 3-13 配置攻击溯源示例组网图说明本例中interface1，interface2，interface3和interface4分别代表10GE1/0/1，10GE1/0/2，10GE1/0/3，10GE1/0/4。
操作步骤步骤1 配置防攻击策略。
\# 创建防攻击策略。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] cpu-defend policy test1 \# 开启攻击溯源功能。
[DeviceA-cpu-defend-policy-test1] auto-defend enable \# 配置攻击溯源检查阈值为100pps。
[DeviceA-cpu-defend-policy-test1] auto-defend threshold 100 \# 配置攻击溯源的采样比为 7 ，即每 7 个报文采样 1 个报文。
[DeviceA-cpu-defend-policy-test1] auto-defend attack-packet sample 7 \# 配置攻击溯源防范的报文类型为ARP报文。

[DeviceA-cpu-defend-policy-test1] auto-defend protocol arp \# 配置攻击溯源的溯源模式为基于源MAC地址和源IP地址。
[DeviceA-cpu-defend-policy-test1] auto-defend trace-type source-mac source-ip \# 开启攻击溯源事件上报功能。
[DeviceA-cpu-defend-policy-test1] auto-defend alarm enable \# 配置攻击溯源惩罚措施，设备受到攻击时丢弃报文，持续时长为360s。在配置攻击溯源惩罚措施之前，请确保设备受到了非法攻击，避免因误丢弃大量正常协议报文而影响正常业务。
[DeviceA-cpu-defend-policy-test1] auto-defend action deny timeout 360 [DeviceA-cpu-defend-policy-test1] quit \# 配置攻击溯源白名单。
[DeviceA] acl number 2001 [DeviceA-acl-basic-2001] rule permit source 10.2.2.0 0.0.0.255 [DeviceA-acl-basic-2001] quit [DeviceA] cpu-defend policy test1 [DeviceA-cpu-defend-policy-test1] auto-defend whitelist 1 acl 2001 [DeviceA-cpu-defend-policy-test1] quit步骤2 应用防攻击策略。
[DeviceA] cpu-defend-policy test1
----结束检查配置结果\# 查看攻击溯源的配置信息。
[DeviceA] display auto-defend configuration cpu-defend policy test1
----------------------------------------------------------------------- Name : test1 Related slot : *** auto-defend : enable auto-defend threshold : 100 (pps)
auto-defend attack-packet sample : 7 (pps)
auto-defend alarm : enable auto-defend alarm threshold : 128 (pps)
auto-defend action : deny timer: 360 (second)
auto-defend trace-type : source-mac source-ip auto-defend protocol : arp auto-defend whitelist 1 : acl number 2001
-----------------------------------------------------------------------配置文件DeviceA的配置文件\# sysname DeviceA \# cpu-defend policy test1 auto-defend enable auto-defend threshold 100 auto-defend attack-packet sample 7 auto-defend protocol arp auto-defend trace-type source-mac source-ip auto-defend alarm enable auto-defend action deny timeout 360 auto-defend whitelist 1 acl 2001

\# cpu-defend-policy test1 \# acl number 2001 rule 5 permit source 10.2.2.0 0.0.0.255 \# return

#### 3.14.3 举例：配置攻击防范

组网需求如图1所示，如果DeviceA受到来自Internet网络不同类型的网络攻击，如畸形报文攻击、分片报文攻击和泛洪攻击，将会造成DeviceA瘫痪。为了预防这种情况，管理员希望通过在DeviceA上部署各种攻击防范措施来为用户提供安全的网络环境，保障正常的网络服务。
图 3-14 配置畸形报文攻击、分片报文攻击与泛洪攻击防范组网图操作步骤步骤1 配置畸形报文攻击防范。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] anti-attack abnormal enable步骤2 配置分片报文攻击防范，分片报文的限制速率为15000bit/s。
[DeviceA] anti-attack fragment enable [DeviceA] anti-attack fragment car cir 15000步骤3 配置泛洪攻击防范。
\# 配置TCP SYN泛洪攻击防范，TCP SYN报文的限制速率为15000bit/s。
[DeviceA] anti-attack tcp-syn enable [DeviceA] anti-attack tcp-syn car cir 15000 \# 配置UDP泛洪攻击防范，对特定端口发送的UDP报文直接丢弃。
[DeviceA] anti-attack udp-flood enable \# 配置ICMP泛洪攻击防范，ICMP泛洪报文的限制速率为15000bit/s。
[DeviceA] anti-attack icmp-flood enable [DeviceA] anti-attack icmp-flood car cir 15000
----结束检查配置结果\# 配置完成后，可以通过执行命令display anti-attack statistics查看报文攻击防范的统计数据。

<DeviceA> display anti-attack statistics Packets Statistic Information:
------------------------------------------------------------------------------- AntiAtkType TotalPacketNum DropPacketNum PassPacketNum (H) (L) (H) (L) (H) (L)
------------------------------------------------------------------------------- Abnormal 0 0 0 0 0 0 Fragment 0 0 0 0 0 0 Icmp-flood 0 0 0 0 0 0 Tcp-syn 0 58 0 0 0 58 Udp-flood 0 0 0 0 0 0
-------------------------------------------------------------------------------配置文件DeviceA的配置文件\# sysname DeviceA \# anti-attack abnormal enable anti-attack fragment enable anti-attack fragment car cir 15000 anti-attack tcp-syn enable anti-attack tcp-syn car cir 15000 anti-attack udp-flood enable anti-attack icmp-flood enable anti-attack icmp-flood car cir 15000 \# return

### 3.15 常见配置错误

#### 3.15.1 攻击溯源功能不生效

故障现象配置了攻击溯源功能后，攻击溯源功能不生效。
可能原因本类故障的常见原因主要包括：
配置攻击溯源的防攻击策略没有被应用。
●
● 攻击溯源的检测阈值过大造成设备不认为该报文为攻击报文。
操作步骤
1. 执行命令display current-configuration，确定防攻击策略是否被应用。
– 如果显示信息中包含配置cpu-defend-policy，则表示已应用了防攻击策略。
此时，执行步骤2。
– 如果显示信息中没有配置 cpu-defend-policy ，则表示防攻击策略没有被应用。此时，需要在系统视图下执行命令cpu-defend-policy，应用防攻击策略。
2. 检查攻击溯源检测阈值是否过大。

执行命令display auto-defend configuration查看“auto-defend threshold”字段取值。如果攻击溯源的检查阈值较大，则在防攻击策略视图下执行命令auto- defend threshold命令减小攻击溯源的检查阈值。

#### 3.15.2 协议报文没有上送CPU

故障现象配置了CPU防攻击功能后，协议报文没有上送CPU。
可能原因本类故障的常见原因主要包括：
● 配置了匹配协议报文且动作为丢弃的规则（如针对该类协议报文的上送规则为deny）。
● 非法报文攻击CPU，导致协议报文无法上送。
操作步骤
1. 检查设备上是否配置了匹配协议报文且动作为丢弃的规则。
a. 在系统视图下，执行命令display current-configuration，查看配置的防攻击策略。
b. 然后执行命令display cpu-defend policy [ policy-name ]，检查防攻击策略下是否配置了针对此协议报文的上送CPU规则是否为deny。
如果针对此协议报文的上送CPU规则为deny，请在防攻击策略视图下执行命令car，将上送规则修改为CAR。
如果针对此协议报文的上送CPU规则不是deny，请继续执行以下检查。
2. 检查上送CPU的统计信息。
执行命令display cpu-defend statistics，检查上送CPU的统计信息。如果有大量协议报文被丢弃，则该协议报文可能为非法攻击报文，请分析报文是否为非法攻击报文（如通过攻击溯源功能），如果确定是非法攻击报文，请使用过滤器或者流策略阻止此协议报文上送CPU。

#### 3.15.3 如何防止DHCPv6类型报文对CPU的冲击

执行命令display cpu-defend statistics检查CPCAR报文统计信息，如果存在大量DHCPv6类型的丢包现象，请确认此网络是否需要IPv6，如果不需要，建议配置cpu- defend policy策略将DHCPv6类型报文直接丢弃。

#### 3.15.4 过多ARP Reply报文上送CPU时如何处理

ARP Reply报文上送过多会造成CPU负载过大，查看ARP Reply报文上送过多的命令是display cpu-defend configuration packet-type arp-reply all或display cpu- defend statistics packet-type arp-reply all 。
通过display cpu-defend statistics packet-type arp-reply all命令查看到的Drop(Bytes)数较多，则说明ARP Reply报文上送过多。

这种情况下，可以适当调整ARP Reply报文的CPCAR值。如果是受到攻击的情况，则需要确认攻击源。可以通过获取报文头或打开调试开关的方式查看攻击源，然后配置过滤器将攻击源屏蔽。
说明调整CPCAR不当将会影响网络业务，如果需要调整CPCAR，建议联系技术支持人员处理。

#### 3.15.5 如何定位常见的攻击，解决办法包括哪些

常见的攻击，可以通过以下步骤进行定位：
1. 执行命令reset cpu-defend statistics，清除上送CPU的报文统计计数。
2. 等待1分钟后，执行命令display cpu-defend statistics，查看这段时间内上送CPU和丢弃的协议报文数量，如ICMP、TTL Expired、SSH、FTP等。如果上送或丢弃的报文数量较大，则可认为是攻击，如ICMP攻击、TTL Expired攻击、SSH流量攻击、FTP攻击等。
3. 通过攻击溯源来确认攻击源。
对于这些攻击，可以在确认攻击源之后，通过在 cpu-defend policy 中配置过滤器或者攻击溯源惩罚功能来丢弃攻击报文。
另外，对于ICMP攻击，还可以针对该攻击源设备的ICMP报文速率进行抑制；对于SSH、FTP攻击，还可以通过配置流策略以丢弃攻击报文。
