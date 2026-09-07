# S1700, S5700, S6700 V600R025C00 配置指南-安全 01-04 风暴抑制配置

## 4 风暴抑制配置

4风暴抑制配置

### 4.1 风暴抑制简介

4.2 风暴抑制配置注意事项
4.3 风暴抑制缺省配置
4.4 配置流量抑制
4.5 配置风暴控制
4.6 风暴抑制配置举例
4.7 风暴抑制常见配置错误
4.1 风暴抑制简介
定义
风暴抑制是用于控制广播、未知组播以及未知单播报文，防止这类报文引起广播风暴
的安全技术。
风暴抑制包括流量抑制和风暴控制两个子功能：
● 流量抑制通过配置阈值来限制广播、未知组播未知单播报文的速率。当流量超过
阈值时，系统将丢弃多余的流量，阈值范围内的报文可以正常通过，从而将流量
限制在合理的范围内。此外，流量抑制还支持对接口出方向的流量进行阻塞。
● 风暴控制通过阻塞报文或关闭接口来阻断广播、未知组播或未知单播报文的流
量。此外，风暴控制还支持通过抑制报文来控制报文的平均速率。当流量超过指
定的阈值时，系统会执行对应的风暴控制动作。
流量抑制和风暴控制功能均用于控制广播风暴，二者之间的对比如表4-1所述。

表 4-1 流量抑制和风暴控制对比

| 对比项 | 流量抑制 | 风暴控制 |
|---|---|---|
| 流量控制机制 | ● 如果配置接口出方向的流量抑制功能，系统将直接阻塞对应报文类型的流量。 ● 其他情况下，系统将丢弃超过阈值的流量，阈值范围内的报文可以正常通过。 | ● 如果风暴控制的动作是抑制报文，当接口上接收的报文平均速率超过配置的高阈值时，系统将丢弃超额的流量，直至报文平均速率不超过该阈值。 ● 其他情况下，当流量超过指定的阈值时，系统会阻塞该接口收到的流量或者直接将该接口关闭。 |
| 流量检测机制 | ● 基于芯片进行检测。 ● 流量超过阈值，流量抑制功能立即生效。 | ● 基于软件进行检测。 ● 在检测时间间隔内，报文平均速率超过阈值，风暴控制功能生效。 |

目的当设备某个二层以太网接口收到广播、未知组播或未知单播报文时，如果根据报文的目的MAC地址设备不能明确报文的出接口，设备会向同一VLAN内的其他二层以太接口转发这些报文，这样可能导致广播风暴，降低设备转发性能。此外，VXLAN网络也会出现同样的问题。
风暴抑制特性中的流量抑制和风暴控制功能，可以有效地控制这几类报文流量。

### 4.2 风暴抑制配置注意事项

License 依赖风暴抑制无需License许可即可使用。
硬件依赖表 4-2 支持本特性的硬件

| 系列 | 支持产品 |
|---|---|
| S6750-H | S6750-H36C，S6750-H48X8C，S6750-H48Y8C |
| S1730S-S3 | S1730S-S24P4S-A3，S1730S-S24P4X-A3， S1730S-S24T4S-QA3，S1730S-S24T4X-QA3， S1730S-S48P4S-A3，S1730S-S48T4S-A3， S1730S-S48T4X-A3，S1730S-S8P4X-QA3， S1730S-S8T4X-QA3 |
| S6730E-H-V2 | S6730E-H6FX4Y2CZ-V2 |

| 系列 | 支持产品 |
|---|---|
| S5735E-S-V2 | S5735E-S24HJ4XE-V2，S5735E-S24HS4XE-V2， S5735E-S24J4XE-V2，S5735E-S48HJ4XE-V2， S5735E-S48HS4XE-V2，S5735E-S48J4XE-V2 |
| S5735-S-V2 | S5735-S24HJ4XE-V2，S5735-S24HS4XE-V2， S5735-S24J4XE-V2，S5735-S24P4XE-V2，S5735- S24P4XEZ-V2，S5735-S24P8J4XEZ-V2，S5735- S24PN4XE-V2，S5735-S24ST4XE-V2，S5735- S24T4XE-C-V2，S5735-S24T4XE-V2，S5735- S24T4XEZ-V2，S5735-S24T8J4XE-XA-V2，S5735- S24T8J4XEZ-V2，S5735-S24U4XE-V2，S5735- S48HJ4XE-V2，S5735-S48HS4XE-V2，S5735- S48J4XE-V2，S5735-S48P4XE-V2，S5735- S48P4XEZ-V2，S5735-S48PN4XE-V2，S5735- S48S4XE-V2，S5735-S48T4XE-C-V2，S5735- S48T4XE-V2，S5735-S48T4XE-XA-V2，S5735- S48T4XEZ-V2，S5735-S48U4XE-V2 |
| S5735S-S3 | S5735S-S24P4X-A3，S5735S-S48P4X-A3 |
| S6750E-S | S6750E-S16X10Y2CZ，S6750E-S24T16X8Y2CZ |
| S5735I-L-V2 | S5735I-L10T4X-A-V2，S5735I-L8P4X-A-V2 |
| S6730-H-V2 | S6730-H24X6C-V2，S6730-H28X6CZ-V2，S6730- H48X6C-TV2，S6730-H48X6C-V2，S6730- H48X6CZ-V2，S6730-H48Y6C-TV2，S6730- H48Y6C-V2，S6730-H6FX4Y2CZ-V2 |
| S5735I-H-V2 | S5735I-H24U8S4XE-QA-V2，S5735I-H8T2XN- V2，S5735I-H8T4S2XN-V2，S5735I-H8U2XN-V2 |
| S6750-S | S6750-S16X10Y2CZ，S6750-S16X8YZ，S6750- S24T16X8Y2CZ |
| S5735S-L3 | S5735S-L24P4S-A3，S5735S-L24P4XE-A3， S5735S-L24PN4XE-A3，S5735S-L24ST4X-A3， S5735S-L24T4S-QA3，S5735S-L24T4X-QA3， S5735S-L24T8J4XE-A3，S5735S-L48P4S-A3， S5735S-L48P4XE-A3，S5735S-L48PN4XE-A3， S5735S-L48S4X-A3，S5735S-L48T4S-A3，S5735S- L48T4XE-A3，S5735S-L8P4X-QA3，S5735S- L8T4X-QA3 |
| S5755-H | S5755-H24HB2Y2CZ，S5755-H24N4Y-A，S5755- H24P4Y2CZ，S5755-H24T4Y2CZ，S5755- H24U4Y2CZ，S5755-H24UM4Y2CZ，S5755- H24UN4Y2CZ，S5755-H24UTM4X4Y2C，S5755- H48N4Y-A，S5755-H48P4Y2CZ，S5755- H48T4Y2CZ，S5755-H48T4Y2CZ-B，S5755- H48U4Y2CZ，S5755-H48UM4Y2CZ，S5755- H48UN4Y2CZ，S5755-H48UTM4X4Y2C |

| 系列 | 支持产品 |
|---|---|
| S5735R-S-V2 | S5735R-S24P4X-V2，S5735R-S24T8J4X-XA-V2， S5735R-S48P4X-V2，S5735R-S48T4X-XA-V2 |
| S6780-H | S6780-H4Z |
| S5735E-L-V2 | S5735E-L16LP2UM2X-QA-V2，S5735E-L16LP2X- QA-V2，S5735E-L24HJ4XE-A-V2，S5735E- L24P4S-A-V2，S5735E-L24P4XE-A-V2，S5735E- L24ST4XE-A-V2，S5735E-L24T4XE-A-V2， S5735E-L48LP4S-A-V2，S5735E-L48LP4XE-A-V2， S5735E-L48S4XE-A-V2，S5735E-L48T4XE-A-V2， S5735E-L8P4X-QA-V2，S5735E-L8T4X-QA-V2 |
| S5755-S | S5755-S24N8YZ，S5755-S24P8J8YZ，S5755- S24P8Y，S5755-S24T8J8YZ，S5755-S24T8Y， S5755-S24U8J8YZ，S5755-S24U8Y，S5755- S24UN8YZ，S5755-S48N8YZ，S5755-S48P8Y， S5755-S48P8YZ，S5755-S48T8Y，S5755- S48T8YZ，S5755-S48T8YZ-B，S5755-S48U8Y， S5755-S48U8YZ，S5755-S48UN8YZ |
| S5735R-L-V2 | S5735R-L16LP2S-QA-V2，S5735R-L16LP2UM2X- QA-V2，S5735R-L16LP2X-QA-V2，S5735R- L16T4S-A-V2，S5735R-L16T4X-QA-V2，S5735R- L24P4S-A-V2，S5735R-L24P4X-A-V2，S5735R- L24T4S-A-V2，S5735R-L24T4X-QA-V2，S5735R- L48LP4S-A-V2，S5735R-L48LP4X-A-V2，S5735R- L48P4X-A-V2，S5735R-L48T4S-A-V2，S5735R- L48T4X-A-V2，S5735R-L8P4S-A-V2，S5735R- L8P4X-QA-V2，S5735R-L8T4S-A-V2，S5735R- L8T4X-QA-V2 |
| S5735-L-V2 | S5735-L10T4X-A-V2，S5735-L14P2S-QA-V2， S5735-L16LP2UM2X-QA-V2，S5735-L16LP2X-QA- V2，S5735-L16P2UM2X-QA-V2，S5735-L16T4S- A-V2，S5735-L16T4X-QA-V2，S5735-L24HJ4XE- A-V2，S5735-L24J4X-A-V2，S5735-L24J4X-D- V2，S5735-L24LU8S4XE-QA-V2，S5735-L24P4S- A-V2，S5735-L24P4XE-A-V2，S5735-L24PN4XE- A-V2，S5735-L24ST4XE-A-V2，S5735-L24T4S-A- V2，S5735-L24T4X-QA-V2，S5735-L24T4XE-A- V2，S5735-L24T4XE-D-V2，S5735-L24T8J4XE-A- V2，S5735-L48J4X-A-V2，S5735-L48J4X-D-V2， S5735-L48LP4S-A-V2，S5735-L48LP4XE-A-V2， S5735-L48LPN4XE-A-V2，S5735-L48P4XE-A-V2， S5735-L48PN4XE-A-V2，S5735-L48S4X-A-V2， S5735-L48S4XE-A-V2，S5735-L48T4S-A-V2， S5735-L48T4XE-A-V2，S5735-L48T4XE-D-V2， S5735-L8P2T4X-A-V2，S5735-L8P4S-A-V2， S5735-L8P4X-QA-V2，S5735-L8T4S-A-V2， S5735-L8T4X-QA-V2 |

| 系列 | 支持产品 |
|---|---|
| S6730-S-V2 | S6730-S24X6Q-V2，S6730-S48X6Q-V2 |
| S5735I-S-V2 | S5735I-S16T2S4XN-V2，S5735I-S16T8S4XE-QD- V2，S5735I-S24T4XE-V2，S5735I-S24T8S4XE-QA- V2，S5735I-S24U4XE-V2，S5735I-S48T4XE-V2， S5735I-S8T4SN-V2，S5735I-S8T4XN-V2，S5735I- S8T8P2S4XN-V2，S5735I-S8U2XN-V2，S5735I- S8U4XN-V2 |
| S5732-H-V2 | S5732-H24S4X6QZ-TV2，S5732-H24S4X6QZ- V2，S5732-H24UM4Y2CZ-KV2，S5732- H24UM4Y2CZ-V2，S5732-H44S4X6QZ-V2， S5732-H48UM4Y2CZ-KV2，S5732-H48UM4Y2CZ- TV2，S5732-H48UM4Y2CZ-V2 |

查询工具如需了解硬件规格、产品部件的配套关系，请点击硬件中心进行查询；如需了解关键规格、全量软件规格，请点击规格查询进行查询。
特性限制表 4-3 本特性的使用限制

| 特性 | 特性限制 |
|---|---|
| 风暴控制 | 风暴控制只对二层流量生效。 |
| 风暴控制 | * 从22.0版本开始，三层主接口视图下不支持配置风暴控制命令(storm control enable/storm control action)。 * 22.0之前的版本，三层主接口视图下配置风暴控制命令后功能无法生效。 |
| 流量抑制 | 对于一个接口下同种报文的入方向流量，设备仅允许同时配置流量抑制或风暴控制两种功能中的一种。 |
| 流量抑制 | 流量抑制只对二层流量生效。 |

### 4.3 风暴抑制缺省配置

风暴抑制的缺省配置如表4-4所示。
表 4-4 风暴抑制缺省配置

| 参数 | 缺省配置 |
|---|---|
| 接口入方向的流量抑制功能 | 已启用 |

| 参数 | 缺省配置 |
|---|---|
| 接口入方向的流量抑制方式 | 百分比方式 |
| 百分比抑制比例值 | ● 广播报文的流量抑制：10% ● 未知组播报文、未知单播报文的流量抑制：100% ● MAC漂移联动未知单播流量抑制： 50% |
| 接口出方向的流量抑制功能 | 未启用 |
| VLAN/BD的流量抑制功能 | 未启用 |
| MAC漂移联动流量抑制功能 | 已启用 |
| MAC漂移联动流量抑制的方式 | 百分比方式 |
| 风暴控制功能 | 未启用 |
| 风暴控制时记录日志或者上报告警功能 | 未启用 |
| 风暴控制的检测时间间隔 | 5秒 |

### 4.4 配置流量抑制

#### 4.4.1 了解流量抑制

流量抑制按以下三种形式来限制广播、未知组播或未知单播报文：
● 在接口视图下，入方向上，设备支持对广播、未知组播及未知单播报文按百分比或报文速率进行流量抑制。
设备监控接口下的各类报文速率，当入口流量超过配置的阈值时，设备会丢弃超额的流量。
● 在接口视图下，出方向上，设备支持对广播、未知组播和未知单播报文的阻塞。
● 在VLAN或BD视图下，设备支持对广播、未知组播和未知单播报文按比特速率进行流量抑制。
设备监控同一VLAN或BD内各类报文的速率，当VLAN或BD内流量超过配置的阈值时，设备会丢弃超额的流量。
此外，设备支持以下流量抑制相关功能：
● ICMP报文流量抑制。通过指定限速阈值对ICMP报文进行限速，防止大量ICMP报文上送CPU处理，导致其他业务功能异常。
● MAC漂移联动流量抑制。在设备开启MAC漂移检测功能后，若检测到MAC地址发生漂移，将触发对漂移端口的流量抑制功能。

#### 4.4.2 配置接口入方向的流量抑制

背景信息为了防止广播风暴，可以配置接口入方向的流量抑制。设备支持对广播、未知组播或未知单播报文按百分比或报文速率进行流量抑制。当广播、未知组播或未知单播流量超过配置的阈值时，系统将丢弃超额的流量，使流量降低到合理的范围内。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤3 配置接口从三层模式切换到二层模式。
portswitch仅 S6780-H 系列、 S6750-H 系列、 S6730-H-V2 系列、 S6730E-H-V2 系列、 S6750-S 系列、S6730-S-V2系列、S6750E-S系列、S5732-H-V2系列、S5755-H系列、S5755-S系列支持该步骤。请用户根据实际接口类型自行选择是否要执行此步骤。
步骤4 配置接口入方向的流量抑制。
storm suppression { broadcast | multicast | unknown-unicast } { percent-value | cir cir-value [ gbps | kbps | mbps ] [ cbs cbs-value [ bytes | kbytes | mbytes ] ] | packets packets-per-second }如果对同一类型报文多次配置接口入方向的流量抑制，且分别指定参数percent-value和cir cir-value，那么只有最后配置的命令会生效。
----结束检查配置结果执行命令display storm suppression { broadcast | multicast | unknown-unicast } [ interface { interface-name | interface-type interface-number } ]命令，查看接口入方向的流量抑制配置阈值和实际生效的阈值。
说明流量抑制的限速阈值与实际限速效果之间存在误差，请以报文实际通过的速率为准。

#### 4.4.3 配置接口出方向的流量抑制

背景信息对于某些下接网络不希望接收任何广播、未知组播或未知单播流量的接口（比如此接口下的用户较为固定，且对安全性要求较高），可以配置接口出方向的流量抑制，将该接口的广播、未知组播或未知单播报文完全阻断。
操作步骤步骤1 进入系统视图。
system-view

步骤2 进入接口视图。
interface interface-type interface-number步骤3 配置接口从三层模式切换到二层模式。
portswitch仅S6780-H系列、S6750-H系列、S6730-H-V2系列、S6730E-H-V2系列、S6750-S系列、S6730-S-V2系列、S6750E-S系列、S5732-H-V2系列、S5755-H系列、S5755-S系列支持该步骤。请用户根据实际接口类型自行选择是否要执行此步骤。
步骤4 配置接口出方向的流量抑制。
storm suppression { broadcast | multicast | unknown-unicast } block outbound
----结束

#### 4.4.4 配置VLAN的流量抑制

背景信息为了限制进入VLAN的广播、未知组播或未知单播类型报文的速率，防止广播风暴，可以在该 VLAN 内配置对应报文类型的流量抑制功能，超过限制速率的报文将被丢弃。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入VLAN视图。
vlan vlan-id步骤3 配置VLAN的流量抑制。
对于S6780-H、S6750-H、S6730E-H-V2、S6730-S-V2、S6730-H-V2、S5732-H- V2、S5755-S、S6750E-S、S6750-S和S5755-H系列storm suppression { broadcast | multicast | unknown-unicast } cir cir-value [ gbps | kbps | mbps ] [ cbs cbs-value [ bytes | kbytes | mbytes ] ]对于S5735S-S3、S5735R-S-V2、S5735E-S-V2、S5735-S-V2、S5735S-L3、S1730S- S3、S5735R-L-V2、S5735E-L-V2、S5735-L-V2、S5735I-L-V2、S5735I-H-V2、S5735I-S-V2：
storm suppression broadcast cir cir-value [ gbps | kbps | mbps ] [ cbs cbs-value [ bytes | kbytes | mbytes ] ]
----结束

#### 4.4.5 配置BD的流量抑制

背景信息为了限制进入BD的广播、未知组播或未知单播类型报文的速率，防止广播风暴，可以在该BD内配置对应报文类型的流量抑制功能，超过限制速率的报文将被丢弃。
操作步骤步骤1 进入系统视图。

system-view步骤2 进入BD视图。
bridge-domain bd-id步骤3 配置BD的流量抑制。
storm suppression { broadcast | multicast | unknown-unicast } cir cir-value [ gbps | kbps | mbps ] [ cbs cbs-value [ bytes | kbytes | mbytes ] ]说明该命令仅在S6780-H，S6750-H，S6730E-H-V2，S6730-S-V2，S6730-H-V2，S5732-H-V2，S6750E-S，S6750-S，S5755-S，S5755-H产品上支持。
----结束

#### 4.4.6 配置VSI的流量抑制

背景信息为了限制进入 VSI 域的广播、未知组播或未知单播报文的速率，防止广播风暴，可以在该VSI域内执行本命令，配置对应报文类型的流量抑制功能。配置VSI的流量抑制功能后，设备将对指定VSI域下的广播、未知组播或未知单播报文进行限制，超过限制速率的报文将被丢弃。仅S6780-H、S6750E-S、S6750-S、S6730E-H-V2、S6730-S-V2、S6730-H-V2、S5755-H、S5732-H-V2、S6750-H系列支持。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置MPLS。
mpls quit步骤3 配置MPLS L2VPN。
mpls l2vpn quit步骤4 进入VSI视图。
vsi vsi-id步骤 5 配置 VSI 的流量抑制。
storm suppression { broadcast | multicast | unknown-unicast } cir cir-value [ gbps | kbps | mbps ] [ cbs cbs-value [ bytes | kbytes | mbytes ] ]
----结束

#### 4.4.7 配置MAC漂移联动流量抑制

背景信息在设备开启 MAC 漂移检测功能后，若检测到 MAC 地址发生漂移，将触发对漂移接口的流量抑制功能。通过配置MAC漂移联动流量抑制，可以按照承诺信息速率CIR或百分比指定流量抑制的阈值，并可以使报文强制按照MAC漂移联动流量抑制的阈值进行转发。

操作步骤步骤1 进入系统视图。
system-view步骤2 配置MAC漂移联动流量抑制的阈值。
配置接口下MAC漂移联动流量抑制的阈值。
storm suppression mac-address flapping { percent-value | cir cir-value [ kbps | mbps | gbps ] } [ force ]缺省情况下，MAC漂移联动流量抑制的阈值按照百分比进行配置，比例值为50%。
说明当接口发生MAC地址漂移且配置了相应接口的流量抑制功能时：
● 若已配置该命令且已指定force参数，那么MAC漂移联动流量抑制功能生效。
● 若未配置该命令行或未指定force参数，那么接口的流量抑制功能生效。
对于以下情况，MAC漂移联动流量抑制功能不会生效：
● 若接口同时配置风暴控制功能，则 MAC 漂移联动流量抑制功能不生效。
----结束

### 4.5 配置风暴控制

#### 4.5.1 了解风暴控制

风暴控制可以用来防止广播、未知组播或未知单播报文产生广播风暴。
在一个检测时间间隔内，设备监控接口下接收报文的平均速率并和配置的高阈值和低阈值相比较，当平均速率大于高阈值时，设备会对该接口进行风暴控制，执行配置好的风暴控制动作；当平均速率小于低阈值，设备会将对应类型的报文恢复到正常转发状态。
风暴控制动作包括关闭接口、阻塞报文和抑制报文：
● 如果动作为关闭接口，则需要手动执行命令来开启接口，或者使能接口状态自动恢复为Up功能。
● 如果动作为阻塞报文，当接口上接收的报文平均速率小于指定的最小阈值时，系统会取消在接口上对该报文的阻塞，当接口上接收的报文平均速率超过配置的最大阈值时，系统将丢弃该报文的所有流量。
● 如果动作为抑制报文，当接口上接收的报文平均速率超过配置的最大阈值时，系统将丢弃超额的流量，直至报文平均速率不超过该阈值。

#### 4.5.2 配置风暴控制

背景信息为了限制进入接口的广播、未知组播或未知单播报文的速率，防止广播风暴，可以在该接口上配置对应报文类型的风暴控制功能。

操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤3 配置接口从三层模式切换到二层模式。
portswitch仅S6780-H系列、S6750-H系列、S6730-H-V2系列、S6730E-H-V2系列、S6750-S系列、S6730-S-V2系列、S6750E-S系列、S5732-H-V2系列、S5755-H系列、S5755-S系列支持该步骤。请用户根据实际接口类型自行选择是否要执行此步骤。
步骤4 配置接口上的广播、未知组播或未知单播报文的风暴控制高低阈值。根据高低阈值的不同计量单位，设备支持以下三种配置方式：
● 指定包模式的低阈值min-rate-value和高阈值max-rate-value。阈值的单位为pps（包/秒）。
storm control { broadcast | multicast | unknown-unicast } min-rate min-rate-value max-rate max- rate-value
● 指定字节模式的低阈值min-rate-value-kbps和高阈值max-rate-value-kbps。阈值的单位为kbps（千比特/秒）。
storm control { broadcast | multicast | unknown-unicast } min-rate kbps min-rate-value-kbps max- rate kbps max-rate-value-kbps指定百分比模式的低阈值min-rate-value-percent和高阈值max-rate-value-
●percent。阈值的单位为百分比（报文占用接口带宽的百分比）。
storm control { broadcast | multicast | unknown-unicast } min-rate percent min-rate-value- percent max-rate percent max-rate-value-percent步骤5 配置风暴控制的动作。
1. 配置风暴控制的动作为关闭接口、阻塞报文或抑制报文。
storm control action { error-down | block | suppress }
2. （可选）接口Error-Down发生前，使能接口状态自动恢复为Up的功能。风暴控制的动作为阻塞报文（block）或抑制报文（suppress）时，不需要配置。
如果处于Error-Down状态的接口数量较多，逐一手动恢复接口状态将产生大量重复工作，且可能出现部分接口配置遗漏。为避免这一问题，用户可在系统视图下使能接口状态自动恢复为Up的功能，并设置接口自动恢复为Up的延时时间。
说明此步骤对已经处于Error-Down状态的接口不生效，只对配置此步骤后进入Error-Down状态的接口生效。
可以通过执行命令display error-down recovery查看接口状态自动恢复信息。
error-down auto-recovery cause storm-control interval interval-value步骤6 （可选）配置风暴控制的检测时间间隔。
storm control interval interval-value缺省情况下，风暴控制的检测时间间隔是5秒。
步骤 7 （可选）使能在风暴控制时记录日志或者上报告警的功能。
storm control enable { log | trap }
----结束

检查配置结果执行命令display storm control [ interface interface-type interface-number [ verbose ] ]，查看接口的风暴控制信息。
后续处理配置接口下风暴控制的动作为关闭接口（error-down）后，在风暴控制检测时间间隔内，当接口上接收广播、未知组播或未知单播报文的平均速率大于指定的高阈值时，接口将进行关闭处理。对于处于Error-Down状态的接口，可在该接口的接口视图下依次执行命令shutdown和undo shutdown，或者执行命令restart，重启接口，从而恢复接口状态。

### 4.6 风暴抑制配置举例

#### 4.6.1 举例：配置接口入方向的流量抑制

组网需求如图4-1所示，DeviceA作为二层网络到三层设备的衔接点，需要通过接口入方向的流量抑制功能限制二层网络转发的广播、未知组播和未知单播报文，防止产生广播风暴。
图 4-1 配置接口入方向的流量抑制组网图说明本例中interface1代表10GE1/0/1。
操作步骤步骤 1 进入接口视图。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch步骤2 配置广播流量抑制，按承诺信息速率CIR进行抑制，限制广播报文的最大速率为100kbit/s。
[DeviceA-10GE1/0/1] storm suppression broadcast cir 100步骤3 配置未知组播流量抑制，按百分比（即报文速率和接口速率的比值）抑制，百分比值为80%。
[DeviceA-10GE1/0/1] storm suppression multicast 80步骤4 配置未知单播流量抑制，按承诺信息速率CIR进行抑制，限制未知单播报文的最大速率为100kbit/s。

[DeviceA-10GE1/0/1] storm suppression unknown-unicast cir 100 [DeviceA-10GE1/0/1] quit
----结束检查配置结果\# 查看接口入方向流量抑制的配置信息。
[DeviceA] display storm suppression broadcast interface 10ge 1/0/1
------------------------------------------------------------------------------------------------ Configured Current interface percent(%) cir(kbps) cbs(bytes) pps percent(%) cir(kbps) cbs(bytes) pps
------------------------------------------------------------------------------------------------ 10GE1/0/1 -- 100 18800 -- -- 100 18800 --
------------------------------------------------------------------------------------------------ [DeviceA] display storm suppression multicast interface 10ge 1/0/1
------------------------------------------------------------------------------------------------ Configured Current interface percent(%) cir(kbps) cbs(bytes) pps percent(%) cir(kbps) cbs(bytes) pps
------------------------------------------------------------------------------------------------ 10GE1/0/1 80 -- -- -- 80 -- -- --
------------------------------------------------------------------------------------------------ [DeviceA] display storm suppression unknown-unicast interface 10ge 1/0/1
------------------------------------------------------------------------------------------------ Configured Current interface percent(%) cir(kbps) cbs(bytes) pps percent(%) cir(kbps) cbs(bytes) pps
------------------------------------------------------------------------------------------------ 10GE1/0/1 -- 100 18800 -- -- 100 18800 --
------------------------------------------------------------------------------------------------其中，Configured字段显示已配置的流量抑制百分比值、承诺信息速率和承诺突发尺寸，Current字段显示实际生效的流量抑制百分比值、承诺信息速率和承诺突发尺寸。
可以看出，DeviceA的接口10GE1/0/1在入方向限制广播报文的最大速率为100kbit/s，限制未知组播报文速率和接口速率的比值不超过80%，限制未知单播报文的最大速率为100kbit/s。
配置脚本DeviceA \# sysname DeviceA \# interface 10GE1/0/1 storm suppression broadcast cir 100 kbps storm suppression multicast 80 storm suppression unknown-unicast cir 100 kbps \# return

#### 4.6.2 举例：配置风暴控制

组网需求如图4-2所示，DeviceA作为二层网络到三层设备的衔接点，需要通过风暴控制限制二层网络转发的广播、未知组播和未知单播报文，防止产生广播风暴。
图 4-2 配置风暴控制组网图说明本例中interface1代表10GE1/0/1。

配置思路采用如下思路配置风暴控制：
● 通过在10GE1/0/1接口视图下配置风暴控制功能，限制二层网络转发的广播、未知组播和未知单播报文产生广播风暴。
● 使能在风暴控制时记录日志的功能，以便及时提醒网络管理员采取措施来保护设备。
操作步骤步骤1 进入接口视图。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch步骤2 配置广播、未知组播和未知单播报文的风暴控制高低阈值。在风暴控制检测时间间隔内，当接口接收广播、未知组播或未知单播报文的平均速率大于2000pps时，则对该接口对应类型的报文进行风暴控制；当接口接收广播、未知组播或未知单播报文的平均速率小于1000pps时，则将该接口对应类型的报文恢复到正常转发状态。
[DeviceA-10GE1/0/1] storm control broadcast min-rate 1000 max-rate 2000 [DeviceA-10GE1/0/1] storm control multicast min-rate 1000 max-rate 2000 [DeviceA-10GE1/0/1] storm control unknown-unicast min-rate 1000 max-rate 2000步骤3 配置风暴控制的动作为阻塞报文。
[DeviceA-10GE1/0/1] storm control action block步骤4 配置风暴控制的检测时间间隔为90秒。
[DeviceA-10GE1/0/1] storm control interval 90步骤5 使能在风暴控制时记录日志的功能。
[DeviceA-10GE1/0/1] storm control enable log [DeviceA-10GE1/0/1] quit
----结束检查配置结果查看风暴控制的配置信息。
\# [DeviceA] display storm control interface 10ge 1/0/1
-------------------------------------------------------------------------------- NOTE:
BC = Broadcast; MC = Multicast; UUC = Unknown Unicast Int = Interval value (unit: seconds)
-------------------------------------------------------------------------------- PortName Type MaxRate Mode Action Punish- Trap Log Int Last Status Punish-Time
-------------------------------------------------------------------------------- 10GE1/0/1 BC 2000 Pps Block Normal Off On 90 -- 10GE1/0/1 MC 2000 Pps Block Normal Off On 90 -- 10GE1/0/1 UUC 2000 Pps Block Normal Off On 90 --其中，Punish-Status字段显示当前接口的报文状态，Last Punish-Time字段显示上一次实施风暴控制惩罚的时间。可以看出，DeviceA的接口10GE1/0/1的广播、未知组

播和未知单播报文状态正常，且没有出现实施风暴控制惩罚，说明广播、未知组播和未知单播报文在检测时间间隔内的平均速率没有超过设定值，网络状态良好。
配置脚本DeviceA的配置脚本\# sysname DeviceA \# interface 10GE1/0/1 storm control broadcast min-rate 1000 max-rate 2000 storm control multicast min-rate 1000 max-rate 2000 storm control unknown-unicast min-rate 1000 max-rate 2000 storm control interval 90 storm control action block storm control enable log \# return

### 4.7 风暴抑制常见配置错误

#### 4.7.1 接口入方向的流量抑制无效

故障现象接口配置了广播、未知组播或未知单播报文的流量抑制功能后，仍然出现了对应类型的报文引起的广播风暴，导致正常流量中断。
可能原因
● 接口下没有配置对应类型报文的流量抑制或者配置的流量抑制阈值过大。
● 对应类型的报文在入接口没有被丢弃。
操作步骤步骤1 检查接口入方向的流量抑制配置。
● 任意视图下执行命令display storm suppression { broadcast | multicast | unknown-unicast } [ interface { interface-name | interface-type interface- number } ]查看流量抑制信息，或者在接口视图下使用命令display this查看该接口的流量抑制配置信息。
a. 检查有无配置对应类型报文的流量抑制。
b. 确认流量抑制阈值是否过大：
▪如果流量抑制阈值过大，请在接口视图下执行命令storm suppression { broadcast | multicast | unknown-unicast } { percent-value | cir cir-value [ gbps | kbps | mbps ] [ cbs cbs-value [ bytes | kbytes | mbytes ] ] | packets packets-per-second }修改流量抑制参数。
▪如果流量抑制阈值合适，请继续执行以下检查。
步骤2 检查报文在接口入方向是否被丢弃。有以下两种方法：
● 用户视图下执行命令display interface interface-type interface-number，查看输出信息中输出带宽占用率是否在抑制前后有较大变化。正常情况下，在配置流

量抑制之后，接口丢弃超过阈值限制的报文，接口带宽利用率会降低。如果没有变化或变化很小，请执行后续步骤。
● 准备另外一个接口B，将要检查的接口A（即配置流量抑制的接口）和接口B加入相同VLAN，查看接口B的出方向流量是否为接口A上配置的抑制后的流量。如果不是，说明报文没有在接口A的入方向被丢弃。请执行后续步骤。
步骤3 请收集如下信息，并联系技术支持人员。
● 上述步骤的执行结果。
● 设备的配置文件、日志信息、告警信息。
----结束
