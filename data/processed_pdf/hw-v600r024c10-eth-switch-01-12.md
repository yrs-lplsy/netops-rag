# S1700, S5700, S6700 V600R024C10 配置指南-以太网交换 01-12 Loopback Detection配置

## 12 Loopback Detection配置

### 12.1 Loopback Detection简介

12.2 Loopback Detection原理描述
12.3 Loopback Detection配置注意事项
12.4 Loopback Detection缺省配置
12.5 配置自动模式的Loopback Detection
12.6 配置手工模式的Loopback Detection
12.7 维护Loopback Detection
12.8 Loopback Detection配置举例
简介
12.1 Loopback Detection
定义
Loopback Detection（LBDT），即环路检测，是一种通过周期性发送环路检测报文来
检测设备下挂网络是否存在环路的检测技术。
目的
网络中的环路会导致设备对广播、组播以及未知单播等报文进行重复发送，造成网络
资源浪费甚至网络瘫痪。为了能够及时发现二层网络中的环路，避免对整个网络造成
严重影响，需要提供一种检测功能，使网络中出现环路时能及时通知用户检查网络连
接和配置情况，并能够使出问题的接口受控。
受益
Loopback Detection可以检测设备的接口是否发生环路。

### 12.2 Loopback Detection原理描述

环路检测技术Loopback Detection是通过从接口周期性发送一种特殊的检测报文，然后检测该报文是否返回本设备（不要求收、发接口为同一接口），进而判断该接口、设备下挂网络或设备双接口间是否存在环路：
● 如果发现检测报文从发出去的接口接收到，则认为该接口发生自环或该接口下挂的网络或设备中存在环路。
● 如果发现检测报文被本设备上的其他接口接收到，则认为该接口所在的网络发生环路或设备发生自环。
发现环路后，设备会向网管发送告警并记录日志，同时根据用户事先的配置对问题接口采取一定的处理动作（即环路处理动作），从而使该接口处于受控状态，减小环路对本设备乃至网络的影响。
接口受控后仍继续发送检测报文，当设备在一定时间内没有收到受控接口发出的检测报文，则认为环路已经消除，该受控接口将自动恢复为正常状态。这个过程称为受控接口自动恢复。
检测报文Loopback Detection通过周期性发送检测报文，并检测其是否返回本设备，以判断是否存在环路，这就要求：
● 当接口或网络中存在环路时，从该接口发送出去的检测报文必须能够送回到本设备。
● 根据检测报文，系统能识别出是否本设备发送出去的检测报文，以及是本设备的哪个接口发送出去的检测报文。
为此，Loopback Detection发送的检测报文需要携带发送设备的MAC地址、发送报文的接口号，以便设备判断报文是否本设备发出以及从哪个接口发出。同时，还需要携带广播或组播类型的目的MAC地址，以保证接口或网络出现环路时，检测报文能够回送到本设备。如图12-1所示为Loopback Detection的检测报文格式。
图 12-1 Loopback Detection 检测报文格式各字段含义如表12-1所述。
表 各字段的含义12-1

| 字段 | 含义 |
|---|---|
| DMAC | 目的MAC地址，如果是Tagged报文，取值为全F；如果是Untagged 报文，取值为BPDU MAC（0180-C200-000A），也可配置为广播或组播MAC。 DMAC为广播（全F）、组播或BPDU MAC，可以保证接口或网络出现环路时，检测报文能够回送到本设备。 |

| 字段 | 含义 |
|---|---|
| SMAC | 源MAC地址，填写本设备的系统MAC地址，以唯一性标识本设备发出的报文。 |
| 802.1Q Tag | 其中包含TPID（Tag Protocol Identifier），TPID取值为0x8100，表示802.1Q Tag帧。 |
| Protocol- Type | 检测报文的类型，包括协议号和子协议号两部分。其中，协议号取值为0x9998，子协议号取值为0x0001，表示是 Loopback Detection检测报文。 |
| PortInfo | 发送检测报文的接口信息，以便设备进行接口比较，判断是否为本设备的接口发出。 |
| Flag | Untagged/tagged检测报文标志： ● 0x0003：表示是Untagged报文。 ● 0x0004：表示是Tagged报文。 |

Loopback Detection同时发送Untagged和Tagged两种检测报文。这就使得Loopback Detection可以基于VLAN进行检测，也可以基于接口进行检测。
检测报文发送条件以下情况均会发出探测报文：
1. 接口从Down变为Up时，发出环路检测探测报文。
2. 定时发送，默认每隔5秒发出环路检测探测报文。
环路处理动作当系统检测到环路时，可以根据用户事先配置的处理动作对接口进行处理，使其处于某种受控状态。具体处理动作如表12-2所示。
表 12-2 环路处理动作

| 处理动作 | 描述 | 适用场景 | 是否抑制网络风暴 |
|---|---|---|---|
| Alarm | 当检测到环路时，只向网管发送告警和记录日志。 | 当用户仅需要告警环路，而不希望影响本接口流量的正常转发时，可以选择此模式。 | 否 |
| Block | 当检测到环路时，向网管发送告警，同时阻塞接口，只允许 BPDU报文通过。 | 当用户需要接口在检测到环路之后不允许数据报文通过，但又要保证某些 BPDU协议报文（如LLDP等）的正常转发，可以选择此动作。 | 是 |
| Error- down | 当检测到环路时，向网管发送告警，同时关闭接口。 | 当用户需要接口在检测到环路之后彻底不参加任何计算或转发，以防止网络风暴，可以选择此动作。 | 是 |

无论用户选用何种处理动作，只要接口或网络中出现环路，对正常业务都会有影响，而Loopback Detection仅为单节点环路检测技术，不具备网络级的破除环路功能。因此，建议用户在发现环路时及时进行破环处理。
受控接口自动恢复受控接口，即配置了环路处理动作的接口。为及时在环路消失后将受控接口恢复到正常状态，Loopback Detection支持环路状态自动恢复功能。系统在经过设置的恢复时间后会尝试在下一个恢复时间内恢复接口，若该恢复时间内没有收到受控接口发出的检测报文，则认为受控接口下的环路已经消除，将恢复该接口为正常状态。
需要注意的是，更改受控接口的Loopback Detection处理动作，该接口将自动恢复为正常状态，并根据更改后的配置重新进行环路检测及相应的处理。
说明被Loopback Detection关闭的接口，即接口状态error-down，不能经过恢复时间自动恢复。此时若要使受控端口恢复为正常状态，需要依次执行命令shutdown和undo shutdown手动恢复，或者执行命令restart重启接口。如果用户希望被关闭的接口可以自动恢复，则必须在接口error-down前，在系统视图下执行命令error-down auto-recovery cause loopback-detect interval interval-value ，使能接口状态自动恢复为 Up 的功能，并设置接口自动恢复为 Up 的延时时间，才可使被关闭的接口经过延时时间后能够自动恢复。
自动检测接口 PVID 的环路PVID（接口缺省VLAN标识，Port Default VLAN ID），即接口的缺省VLAN-ID。缺省情况下，所有接口的PVID均为VLAN1。
● 对于Access接口，可以通过port default vlan vlan-id命令，修改接口缺省的VLAN-ID（对应PVID）。
● 对于Hybrid/Trunk接口，可以通过port hybrid pvid vlan vlan-id和port trunk pvid vlan vlan-id，分别修改接口的PVID。
自动模式的Loopback Detection功能，可以检测组网中PVID对应的VLAN是否存在环路。当检测到环路时接口采取的动作为仅上报告警。
自动检测环路功能默认是开启的，通过命令loopback-detect auto disable关闭。

### 12.3 Loopback Detection配置注意事项

License 依赖Loopback Detection无需License许可即可使用。
硬件依赖表 12-3 支持本特性的硬件

| 系列 | 支持产品 |
|---|---|
| S6750-H | S6750-H36C，S6750-H48Y8C |
| S6730E-H-V2 | S6730E-H6FX4Y2CZ-V2 |

| 系列 | 支持产品 |
|---|---|
| S1730S-S3 | S1730S-S24P4S-A3，S1730S-S24P4X-A3， S1730S-S24T4S-QA3，S1730S-S24T4X-QA3， S1730S-S48P4S-A3，S1730S-S48T4S-A3， S1730S-S48T4X-A3，S1730S-S8P4X-QA3， S1730S-S8T4X-QA3 |
| S5735-S-V2 | S5735-S24HS4XE-V2，S5735-S24P4XE-V2， S5735-S24P4XEZ-V2，S5735-S24P8J4XEZ-V2， S5735-S24PN4XE-V2，S5735-S24ST4XE-V2， S5735-S24T4XE-C-V2，S5735-S24T4XE-V2， S5735-S24T4XEZ-V2，S5735-S24T8J4XE-XA-V2， S5735-S24T8J4XEZ-V2，S5735-S24U4XE-V2， S5735-S48HS4XE-V2，S5735-S48P4XE-V2， S5735-S48P4XEZ-V2，S5735-S48PN4XE-V2， S5735-S48S4XE-V2，S5735-S48T4XE-C-V2， S5735-S48T4XE-V2，S5735-S48T4XE-XA-V2， S5735-S48T4XEZ-V2，S5735-S48U4XE-V2 |
| S5735E-S-V2 | S5735E-S24HS4XE-V2，S5735E-S48HS4XE-V2 |
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
| S5735E-L-V2 | S5735E-L16LP2UM2X-QA-V2，S5735E-L16LP2X- QA-V2，S5735E-L24P4S-A-V2，S5735E-L24P4XE- A-V2，S5735E-L24ST4XE-A-V2，S5735E- L24T4XE-A-V2，S5735E-L48LP4S-A-V2，S5735E- L48LP4XE-A-V2，S5735E-L48S4XE-A-V2， S5735E-L48T4XE-A-V2，S5735E-L8P4X-QA-V2， S5735E-L8T4X-QA-V2 |
| S5755-S | S5755-S24P8J8YZ，S5755-S24P8Y，S5755- S24T8J8YZ，S5755-S24T8Y，S5755-S24U8J8YZ， S5755-S24U8Y，S5755-S48P8Y，S5755- S48P8YZ，S5755-S48T8Y，S5755-S48T8YZ， S5755-S48U8Y，S5755-S48U8YZ |
| S5735R-L-V2 | S5735R-L16LP2S-QA-V2，S5735R-L16LP2UM2X- QA-V2，S5735R-L16LP2X-QA-V2，S5735R- L16T4S-A-V2，S5735R-L16T4X-QA-V2，S5735R- L24P4S-A-V2，S5735R-L24P4X-A-V2，S5735R- L24T4S-A-V2，S5735R-L24T4X-QA-V2，S5735R- L48LP4S-A-V2，S5735R-L48LP4X-A-V2，S5735R- L48P4X-A-V2，S5735R-L48T4S-A-V2，S5735R- L48T4X-A-V2，S5735R-L8P4S-A-V2，S5735R- L8P4X-QA-V2，S5735R-L8T4S-A-V2，S5735R- L8T4X-QA-V2 |

| 系列 | 支持产品 |
|---|---|
| S5735-L-V2 | S5735-L10T4X-A-V2，S5735-L14P2S-QA-V2， S5735-L16LP2UM2X-QA-V2，S5735-L16LP2X-QA- V2，S5735-L16P2UM2X-QA-V2，S5735-L16T4S- A-V2，S5735-L16T4X-QA-V2，S5735- L24LU8S4XE-QA-V2，S5735-L24P4S-A-V2， S5735-L24P4XE-A-V2，S5735-L24PN4XE-A-V2， S5735-L24ST4XE-A-V2，S5735-L24T4S-A-V2， S5735-L24T4X-QA-V2，S5735-L24T4XE-A-V2， S5735-L24T4XE-D-V2，S5735-L24T8J4XE-A-V2， S5735-L48LP4S-A-V2，S5735-L48LP4XE-A-V2， S5735-L48LPN4XE-A-V2，S5735-L48P4XE-A-V2， S5735-L48PN4XE-A-V2，S5735-L48S4X-A-V2， S5735-L48S4XE-A-V2，S5735-L48T4S-A-V2， S5735-L48T4XE-A-V2，S5735-L48T4XE-D-V2， S5735-L8P2T4X-A-V2，S5735-L8P4S-A-V2， S5735-L8P4X-QA-V2，S5735-L8T4S-A-V2， S5735-L8T4X-QA-V2 |
| S5735I-S-V2 | S5735I-S16T2S4XN-V2，S5735I-S16T8S4XE-QD- V2，S5735I-S24T4XE-V2，S5735I-S24T8S4XE-QA- V2，S5735I-S24U4XE-V2，S5735I-S48T4XE-V2， S5735I-S8T4SN-V2，S5735I-S8T4XN-V2，S5735I- S8T8P2S4XN-V2，S5735I-S8U2XN-V2，S5735I- S8U4XN-V2 |
| S5732-H-V2 | S5732-H24S4X6QZ-TV2，S5732-H24S4X6QZ- V2，S5732-H24UM4Y2CZ-KV2，S5732- H24UM4Y2CZ-V2，S5732-H44S4X6QZ-V2， S5732-H48UM4Y2CZ-KV2，S5732-H48UM4Y2CZ- TV2，S5732-H48UM4Y2CZ-V2 |

查询工具如需了解硬件规格、产品部件的配套关系，请点击硬件中心进行查询；如需了解关键规格、全量软件规格，请点击规格查询进行查询。
特性限制表 12-4 本特性的使用限制特性限制LBDT与ERPS、Smart Link、STP/RSTP/MSTP/VBST等环网协议冲突，使能了LBDT功能的接口建议不要再配置这些环网功能，反之亦然。
检测到环路后触发接口error-down，当环路解除后，只能通过shutdown/undo shutdown 方式手工消除接口 Error-down ，或配置 Error-down 自动恢复。

| 特性限制 |
|---|
| 当有2个或2个以上接口加入同一VLAN，且这些接口使能了Loopback Detection功能时，在产生环路后可能会出现hwLdtPortLoop告警震荡，可能只有部分接口产生该告警，且这些接口之间可能存在MAC漂移。此时，请用户配置接口Error-Down，或者在产生告警后手动排查网络，消除环路。 |
| 当环路中存在接口的PVID是检测的VLAN或者接口以Untagged方式加入检测的 VLAN时，检测报文的VLAN Tag会被剥离，导致报文优先级发生变化，系统可能会无法检测到环路。 |
| 配置接口的LoopbackDetection处理动作为Error-Down时，环回告警只有在端口UP 并重新检测没有环路后才会解除。 |
| LBDT仅为单节点环路检测技术，不具备网络级的破除环路功能。 |
| LBDT untag报文不支持双端口环路检测。 |
| 对于产品S1730S-S3系列，S5735S-L3系列，S5735S-S3系列，S5735I-H8T4S2XN- V2： LBDT自动检测在eth-trunk口部署HSR时，检测不出环路。 |

### 12.4 Loopback Detection缺省配置

表 12-5 Loopback Detection 缺省配置

| 参数 | 缺省值 |
|---|---|
| 自动模式Loopback Detection使能状态 | Enable |
| 手工模式Loopback Detection使能状态 | Disable |
| 检测到环路后的处理动作 | Alarm（自动模式） Error-down（手动模式） |
| 检测报文的发送周期 | 5秒 |
| 受控接口的恢复时间 | 3倍检测报文发送周期 |

说明
● Loopback Detection自动检测模式下：检测报文为Tagged类型报文，目的MAC为全F，无法修改。
● Loopback Detection手工检测模式下：
● 检测报文默认为Untagged类型报文，目的MAC为0180-C200-000A，可通过loopback- detect untagged mac-address命令来修改Loopback Detection untagged检测报文的目的 MAC 。
● 若通过loopback-detect vlan命令行指定检测了VLAN，则检测报文为Tagged类型报文，目的MAC为全F，无法修改。

### 12.5 配置自动模式的Loopback Detection

#### 12.5.1 使能自动模式的Loopback Detection功能

背景信息PVID（接口缺省VLAN标识，Port Default VLAN ID），即接口的缺省VLAN-ID。缺省情况下，所有接口的PVID均为VLAN1。
● 对于Access接口，可以通过port default vlan vlan-id命令，修改接口缺省的VLAN-ID（对应PVID）。
● 对于Hybrid/Trunk接口，可以通过port hybrid pvid vlan vlan-id和port trunk pvid vlan vlan-id，分别修改接口的PVID。
自动模式的Loopback Detection功能，可以检测组网中PVID对应的VLAN是否存在环路。当检测到环路时接口采取的动作为仅上报告警。
操作步骤步骤1 进入系统视图。
system-view步骤2 使能所有接口的自动模式的Loopback Detection功能。
undo loopback-detect auto disable缺省情况下，设备上已经使能自动模式的Loopback Detection功能，当检测到PVID存在环路时设备将上报告警。
说明
● Loopback Detection功能需要发送大量检测报文来进行环路检测，这将会耗费一定的系统资源，开启前请确保设备预留足够的系统资源。
● 如果需要关闭自动模式的Loopback Detection功能，请执行命令loopback-detect auto disable。
当通过loopback-detect enable配置设备的手工模式Loopback Detection功能时，设备自动
●模式的Loopback Detection功能将失效。
● 当通过loopback-detect enable配置接口的手工模式Loopback Detection功能时，设备相应接口自动模式的Loopback Detection功能将失效。
----结束

#### 12.5.2 （可选）配置检测报文的发送周期

背景信息使能Loopback Detection功能后，接口便按一定的时间间隔发送环路检测报文，此时间间隔称为 Loopback Detection 检测报文的发送周期。周期越小，单位时间内发送的环路检测报文越多，环路检测结果越准确，但也会消耗更多的系统资源来发送报文，影响系统性能。用户可根据现网情况调整Loopback Detection环路检测报文的发送周期，以在系统性能和环路检测的准确度之间进行平衡。

操作步骤步骤1 进入系统视图。
system-view步骤2 配置Loopback Detection报文的发送周期。
loopback-detect transmit interval packet-interval-time缺省情况下，Loopback Detection报文的发送周期为5秒。
----结束

#### 12.5.3 （可选）配置受控接口的恢复时间

背景信息使能Loopback Detection后，接口会周期性地发送环路检测报文，检测到环路后就会出现告警，使接口处于受控状态，并开始计时。经过设置的恢复时间后，设备会尝试在下一个恢复时间内恢复接口，若该恢复时间内没有收到受控接口发出的检测报文，则认为受控接口下的环路已经消除，将恢复该接口为正常状态。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入需要配置受控接口的恢复时间的接口视图。
interface interface-type interface-number步骤3 配置环路消失后接口的告警恢复时间。
loopback-detect recovery-time recovery-time-value缺省情况下，环路消失后接口将在3个报文发送周期内自动恢复告警。
说明建议恢复时间至少是检测报文发送周期的3倍；如果发送周期配置的非常小，恢复时间建议至少比发送周期大10秒。
步骤4 返回系统视图。
quit
----结束

#### 12.5.4 检查配置结果

操作步骤步骤1 执行命令display loopback-detect，查看环路检测的配置信息和接口状态。
步骤 2 执行命令 display loopback-detect interface { interface-value | ifTypeifNum } ， 查看具体接口环路检测的配置信息和接口状态信息。
----结束

### 12.6 配置手工模式的Loopback Detection

#### 12.6.1 使能手工模式的Loopback Detection功能

前提条件Loopback Detection功能需要发送大量检测报文来进行环路检测，这将会耗费一定的系统资源，开启前请确保设备预留足够的系统资源。
背景信息设备上使能Loopback Detection功能后，便会周期性发送目的MAC为BPDU MAC的Untagged环路检测报文来进行环路检测。由于设备通常不允许BPDU报文通过，因此，此时Untagged环路检测报文只能检测接口自环，而无法检测设备下挂环路以及检测设备双接口环路。
如果需要Loopback Detection检测设备下挂环路，需要配置基于Tagged检测报文的Loopback Detection功能。或者，当设备之间相连的接口均为Access类型接口或同一设备的出接口、入接口的PVID相同时，可以配置loopback-detect untagged mac- address实现基于Untagged检测报文的环路检测。
如果需要Loopback Detection检测设备双接口环路，则必须配置对指定的VLAN进行环路检测。
操作步骤步骤1 进入系统视图。
system-view步骤2 （可选）使能所有接口的手工模式的Loopback Detection功能。
loopback-detect enable缺省情况下，设备上没有使能手工模式的Loopback Detection功能。
步骤3 进入需要配置Loopback Detection的接口视图。
interface interface-type interface-number步骤 使能接口的 功能。
4 Loopback Detection loopback-detect enable缺省情况下，接口上没有使能手工模式的Loopback Detection功能。
说明如果系统视图下和接口视图下同时使能或者去使能Loopback Detection功能，以接口视图下的配置为准。
步骤5 （可选）配置基于VLAN Tag标识的检测报文的Loopback Detection功能：
1. 根据需要，选择一种接口加入 VLAN 的配置：
– Access类型接口，并将接口加入需要使能Loopback Detection功能的VLAN。
port link-type access port default vlan vlan-id

– Hybrid类型接口，并将接口以Tagged方式加入需要使能Loopback Detection
功能的VLAN。
port link-type hybrid
port hybrid tagged vlan { { vlan-id1 [ to vlan-id2 ] }&<1-10> | all }
– Trunk类型接口，并将接口加入需要使能Loopback Detection功能的VLAN。
port link-type trunk
port trunk allow-pass vlan { { vlan-id1 [ to vlan-id2 ] }&<1-10> | all }
2. 配置对指定的VLAN进行环路检测。
loopback-detect vlan { vlan-id1 [ to vlan-id2 ] }
缺省情况下，设备上没有配置对指定VLAN进行环路检测。
说明
– 配置该功能之前，指定的VLAN必须先创建。
– 只有当指定的VLAN创建后，接口才会发送带指定VLAN Tag的检测报文。
– 当环路中存在接口的PVID是检测的VLAN或者接口以Untagged方式加入检测的VLAN
时，检测报文的VLAN Tag会被剥离，导致报文优先级发生变化，系统可能会无法检测
到环路。
– 对于Loopback Detection基于VLAN检测的受控接口：
▪
若将接口取消检测此VLAN，则接口将自动恢复为正常状态。
▪
若接口未使能GVRP，当接口手动退出此VLAN时，接口自动恢复为正常状态。
▪
若接口同时使能GVRP，当接口手动或通过GVRP动态退出此VLAN时，如果受控接
口被执行的是除Error-down之外的动作，则可以自动恢复为正常状态。
步骤6 返回系统视图。
quit
----结束

#### 12.6.2 （可选）配置检测报文的发送周期

背景信息使能Loopback Detection功能后，接口便按一定的时间间隔发送环路检测报文，此时间间隔称为Loopback Detection检测报文的发送周期。周期越小，单位时间内发送的环路检测报文越多，环路检测结果越准确，但也会消耗更多的系统资源来发送报文，影响系统性能。用户可根据现网情况调整 Loopback Detection 环路检测报文的发送周期，以在系统性能和环路检测的准确度之间进行平衡。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置Loopback Detection报文的发送周期。
loopback-detect transmit interval packet-interval-time缺省情况下，Loopback Detection报文的发送周期为5秒。
----结束

#### 12.6.3 （可选）配置Loopback Detection处理动作

背景信息未使能Loopback Detection环路检测功能的设备所在的网络出现环路后，设备不对接口做任何处理。此时，需要用户手工关闭接口，才会避免环路对本设备和网络的影响。
用户可以事先配置Loopback Detection检测到环路时的处理动作，这样，检测到环路后，设备会自动根据配置设置接口为受控状态，以便及时减少环路对本设备和整个网络的影响。
Loopback Detection检测到环路时的处理动作有如下几种：
● Alarm：上报告警。当检测到环路时，设备向网管上报告警，但对接口不做任何处理。
说明若要使设备上报告警生效，必须先在系统视图下配置 snmp-agent trap enable 或 snmp- agent trap enable feature-name lbdt，打开Loopback Detection的告警开关。
● Block：阻塞接口。当检测到环路时，设备将该接口与其他接口隔离，不能转发除BPDU报文外的报文。
● Error-down：关闭接口。当检测到环路时，设备关闭该接口。
有关处理动作的详细描述，请参见环路处理动作，用户可以根据实际需要任选一种进行配置。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置Loopback Detection检测到环路后对所有接口的处理动作。
loopback-detect action { alarm | block | error-down }缺省情况下，接口的Loopback Detection功能为Error-down状态。
步骤3 进入需要配置Loopback Detection处理动作的接口视图。
interface interface-type interface-number步骤4 配置Loopback Detection检测到环路后对接口的处理动作。
loopback-detect action { alarm | block | error-down }缺省情况下，接口的Loopback Detection功能与系统视图下的配置保持一致。
说明如果系统视图下和接口视图下同时配置了处理动作，接口视图下的配置优先生效。
步骤 5 返回系统视图。
quit
----结束

#### 12.6.4 （可选）配置受控接口的恢复时间

背景信息使能Loopback Detection后，接口会周期性地发送环路检测报文，检测到环路后就对接口采取由loopback-detect action配置的处理动作，使接口处于受控状态，并开始计时。经过设置的恢复时间后，设备会尝试在下一个恢复时间内恢复接口，若该恢复时间内没有收到受控接口发出的检测报文，则认为受控接口下的环路已经消除，将恢复该接口为正常状态。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入需要配置受控接口的恢复时间的接口视图。
interface interface-type interface-number步骤 3 配置环路消失后接口的告警恢复时间。
loopback-detect recovery-time recovery-time-value缺省情况下，环路消失后接口将在3个报文发送周期内自动恢复告警。
说明建议恢复时间至少是检测报文发送周期的3倍；如果发送周期配置的非常小，恢复时间建议至少比发送周期大10秒。
步骤4 配置接口由环路引起的Error-down后状态自动恢复为Up功能，并指定其延迟时间。
error-down auto-recovery cause loopback-detect interval interval-value缺省情况下，处于Error-down状态的接口状态自动恢复功能未使能。
说明此方式对已经处于Error-down状态的接口不生效，只对配置该命令后进入Error-down状态的接口生效。
步骤5 返回系统视图。
quit
----结束

#### 12.6.5 检查配置结果

操作步骤步骤1 执行命令display loopback-detect，查看环路检测的配置信息和接口状态。
步骤 2 执行命令 display loopback-detect interface { interface-value | ifTypeifNum } ， 查看具体接口环路检测的配置信息和接口状态信息。
----结束

### 12.7 维护Loopback Detection

背景信息日常维护中，需要了解Loopback-Detection配置信息时，可以在任意视图中执行以下命令。
操作步骤维护Loopback Detection运行状况的相关操作如表12-6所示。
表 12-6 维护 Loopback-Detection 配置的命令

| 操作 | 命令 |
|---|---|
| 查看环路检测的配置信息和接口状态信息。 | display loopback-detect |
| 查看具体接口环路检测的配置信息和接口状态信息。 | display loopback-detect interface { interface-value | ifType ifNum } |
| 查看环路检测报文收发统计信息。 | display loopback-detect statistics interface { interface-value | ifType ifNum } |
| 清除环路检测报文收发统计信息。 | reset loopback-detect statistics interface |

### 12.8 Loopback Detection配置举例

#### 12.8.1 举例：配置自动模式的Loopback Detection检测设备下挂网络环路

组网需求如图12-2所示，某新建网络以下挂方式接入到DeviceA，该网络连接的接口的默认PVID为1。新建网络可能因连接或配置错误而产生环路，进而影响到DeviceA及其上行网络的通信。
用户希望能在DeviceA上检测到新建网络中的环路，防止环路影响DeviceA及其所连网络的正常通信。
说明本例中interface1分别代表10GE1/0/1。

图 12-2 配置自动模式的 Loopback Detection 检测设备下挂网络环路示例组网图配置思路由于接口PVID为1，因此可以在DeviceA上配置自动模式的Loopback Detection功能，检测该网络是否存在环路。可采用如下思路配置：
1. 在DeviceA上全局使能自动模式的Loopback Detection功能，实现对下行网络PVID环路的检测。
2. 配置Loopback Detection功能的相关参数，实现DeviceA在检测到环路后能及时告警，防止环路影响DeviceA及其所连网络的正常通信。
说明新建网络中的交换设备上需要配置接口的链路类型为Trunk或Hybrid，并允许相应的VLAN通过，以保证新建网络内以及新建网络与DeviceA间的二层互通。
操作步骤步骤1 在DeviceA上配置自动模式的Loopback Detection功能。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] undo loopback-detect auto disable步骤 2 配置接口对指定 VLAN 进行环路检测。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] port link-type access [DeviceA-10GE1/0/1] port default vlan 1 [DeviceA-10GE1/0/1] quit步骤3 配置Loopback Detection检测报文的发送周期。
[DeviceA] loopback-detect transmit interval 5
----结束检查配置结果
1. 在系统视图下执行命令display loopback-detect检查配置是否成功。
[DeviceA] display loopback-detect
--------------------------------------------------------------------------------

Loopback-detect transmit interval: 5s
-------------------------------------------------------------------------------- (A): Auto Loopback-detect
-------------------------------------------------------------------------------- Interface RecoveryTime Action Status
-------------------------------------------------------------------------------- 10GE1/0/1 15 Error-down Normal
2. 下挂网络中出现环路，然后执行命令display loopback-detect检查10GE1/0/1接口是否关闭。
[DeviceA] display loopback-detect
-------------------------------------------------------------------------------- Loopback-detect transmit interval: 10s
-------------------------------------------------------------------------------- (A): Auto Loopback-detect
-------------------------------------------------------------------------------- Interface RecoveryTime Action Status
-------------------------------------------------------------------------------- 10GE1/0/1 15 Alarm(A) Alarm(A)
配置脚本\# sysname DeviceA \# loopback-detect transmit interval 5 undo loopback-detect auto disable \# interface 10GE1/0/1 port link-type access port default vlan 1 \# return

#### 12.8.2 举例：配置手工模式的Loopback Detection检测接口自环

组网需求如图12-3所示，某企业网络中的设备DeviceA的interface1上安装了光模块，为避免因光纤插错、接口被高压击坏等情况导致接口interface1发生Tx-Rx自环而影响现有网络，用户希望能在DeviceA上及时检测出接口interface1上存在的Tx-Rx自环，并希望环路存在时阻塞接口以减小环路对现有网络的冲击。
说明本例中interface1分别代表10GE1/0/1。

图 12-3 配置手工模式的 Loopback Detection 检测接口自环示例组网图配置思路为检测DeviceA上的下行接口interface1是否存在TX-RX自环，可以在DeviceA上的该接口上配置Loopback Detection功能。配置思路如下：
1. 在DeviceA的接口interface1上使能Loopback Detection功能，实现对该接口的TX- RX自环检测。
2. 配置Loopback Detection处理动作和接口自动恢复时间，实现发现环路后，DeviceA自动阻塞接口以减少环路对现有网络的冲击，以及环路消失后接口自动恢复。
操作步骤步骤1 在DeviceA上使能接口的Loopback Detection功能。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] loopback-detect enable [DeviceA-10GE1/0/1] quit步骤2 配置Loopback Detection处理动作。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] loopback-detect action error-down [DeviceA-10GE1/0/1] quit
----结束检查配置结果在系统视图下执行命令display loopback-detect检查配置是否成功。
[DeviceA] display loopback-detect
-------------------------------------------------------------------------------- Loopback-detect transmit interval: 5s
--------------------------------------------------------------------------------
-------------------------------------------------------------------------------- Interface RecoveryTime Action Status
-------------------------------------------------------------------------------- 10GE1/0/1 15 Error-down Normal

配置脚本\# sysname DeviceA \# interface 10GE1/0/1 loopback-detect enable loopback-detect action error-down \# return

#### 12.8.3 举例：配置手工模式的Loopback Detection检测设备下挂网络环路

组网需求如图12-4所示，某新建网络以下挂方式接入到DeviceA，该网络所属VLAN为100。新建网络可能因连接或配置错误而产生环路，进而影响到DeviceA及其上行网络的通信。
用户希望能在DeviceA上检测到新建网络中的环路，防止环路影响DeviceA及其所连网络的正常通信。
说明本例中interface1分别代表10GE1/0/1。
图 12-4 配置手工模式的 Loopback Detection 检测设备下挂网络环路示例组网图配置思路由于新建网络仅有VLAN 100，因此可以在DeviceA上配置Loopback Detection功能，检测该网络是否存在环路。可采用如下思路配置Loopback Detection功能：
1. 在 DeviceA 的接口 interface1 上使能 Loopback Detection 功能，并配置对指定VLAN进行环路检测，实现对下行网络环路的检测。
2. 配置Loopback Detection功能的相关参数，实现DeviceA在检测到环路后能及时关闭接口interface1，防止环路影响DeviceA及其所连网络的正常通信。

说明新建网络中的交换设备上需要配置接口的链路类型为Trunk或Hybrid，并允许相应的VLAN通过，以保证新建网络内以及新建网络与DeviceA间的二层互通。
操作步骤步骤1 在DeviceA上使能接口的Loopback Detection功能。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] loopback-detect enable [DeviceA-10GE1/0/1] quit步骤2 配置接口对指定VLAN进行环路检测。
[DeviceA] vlan batch 100 [DeviceA-vlan100] quit [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] port link-type hybrid [DeviceA-10GE1/0/1] port hybrid tagged vlan 100 [DeviceA-10GE1/0/1] loopback-detect vlan 100 [DeviceA-10GE1/0/1] quit步骤3 配置Loopback Detection检测报文的发送周期和处理动作。
[DeviceA] loopback-detect transmit interval 10 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] loopback-detect action error-down [DeviceA-10GE1/0/1] quit
----结束检查配置结果
1. 在系统视图下执行命令display loopback-detect检查配置是否成功。
[DeviceA] display loopback-detect
-------------------------------------------------------------------------------- Loopback-detect transmit interval: 10s
--------------------------------------------------------------------------------
-------------------------------------------------------------------------------- Interface RecoveryTime Action Status
-------------------------------------------------------------------------------- 10GE1/0/1 30 Error-down Normal
2. 在下挂网络中构造环路，然后执行命令display loopback-detect检查10GE1/0/1接口是否关闭。
[DeviceA] display loopback-detect
-------------------------------------------------------------------------------- Loopback-detect transmit interval: 10s
--------------------------------------------------------------------------------
-------------------------------------------------------------------------------- Interface RecoveryTime Action Status
-------------------------------------------------------------------------------- 10GE1/0/1 30 Error-down Errordown配置脚本\# sysname DeviceA \# vlan batch 100 \# loopback-detect transmit interval 10 \# interface 10GE1/0/1

port link-type hybrid port hybrid tagged vlan 100 loopback-detect enable loopback-detect action error-down loopback-detect vlan 100 \# return

#### 12.8.4 举例：配置手工模式的Loopback Detection检测设备所在网络环路

组网需求如图12-5所示，某二层网络中，所属VLAN为100。网络拓扑变动频繁时，往往会因连接错误或配置错误而产生环路，进而导致广播风暴，影响DeviceA以及整个网络的通信。
用户希望能在DeviceA上检测到网络中的环路，并希望环路存在时阻塞接口以减小环路对DeviceA及其所在网络的冲击，环路消失时阻塞接口能自动恢复到正常状态。
说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
图 12-5 配置手工模式的 Loopback Detection 检测设备所在网络环路示例组网图配置思路为检测 DeviceA 所在网络是否存在环路，可以在 DeviceA 上的 interface1 和 interface2 上分别配置Loopback Detection功能；同时本例中，DeviceA发出的Untagged检测报文会被网络中的其他设备丢弃，导致检测报文无法送回DeviceA，进而无法实现环路检测，所以本例必须配置对指定VLAN进行环路检测。配置思路如下：
1. 使能接口的Loopback Detection功能，并配置对VLAN 100进行环路检测，实现对DeviceA所在网络的环路检测。
2. 配置Loopback Detection处理动作和接口自动恢复时间，实现发现环路后，DeviceA自动阻塞接口以减少环路对其及其所在网络的冲击，环路消失后接口自动恢复。
说明网络中的其他设备上需要配置接口的链路类型为Trunk或Hybrid，并允许相应的VLAN通过，以保证网络内的二层互通。

操作步骤步骤1 在DeviceA上使能接口的Loopback Detection功能。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] loopback-detect enable [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] loopback-detect enable [DeviceA-10GE] quit步骤2 配置接口对指定VLAN进行环路检测。
[DeviceA] vlan batch 100 [DeviceA-vlan100] quit [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] port link-type hybrid [DeviceA-10GE1/0/1] port hybrid tagged vlan 100 [DeviceA-10GE1/0/1] loopback-detect vlan 100 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] port link-type hybrid [DeviceA-10GE1/0/2] port hybrid tagged vlan 100 [DeviceA-10GE1/0/2] loopback-detect vlan 100 [DeviceA-10GE1/0/2] quit步骤3 配置Loopback Detection检测报文的发送周期和处理动作。
[DeviceA] loopback-detect transmit interval 10 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] loopback-detect action block [DeviceA-10GE1/0/1] loopback-detect recovery-time 30 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] loopback-detect action block [DeviceA-10GE1/0/2] loopback-detect recovery-time 30 [DeviceA-10GE1/0/2] quit
----结束检查配置结果
1. 在系统视图下执行命令display loopback-detect检查配置是否成功。
[DeviceA] display loopback-detect
-------------------------------------------------------------------------------- Loopback-detect transmit interval: 10s
--------------------------------------------------------------------------------
-------------------------------------------------------------------------------- Interface RecoveryTime Action Status
-------------------------------------------------------------------------------- 10GE1/0/1 30 Block Normal 10GE1/0/2 30 Block Normal
2. 配置成功后，等待一段时间（约10秒），执行命令display loopback-detect检查接口10GE1/0/1或10GE1/0/2 是否有一个被阻塞。
[DeviceA] display loopback-detect
-------------------------------------------------------------------------------- Loopback-detect transmit interval: 10s
--------------------------------------------------------------------------------
-------------------------------------------------------------------------------- Interface RecoveryTime Action Status
-------------------------------------------------------------------------------- 10GE1/0/1 30 Block Normal 10GE1/0/2 30 Block Block上述显示信息表明，接口10GE1/0/2被阻塞了。
3. 关闭接口10GE1/0/1，30秒后，执行命令display loopback-detect检查接口10GE1/0/2 是否恢复为正常状态。

[DeviceA] display loopback-detect
-------------------------------------------------------------------------------- Loopback-detect transmit interval: 10s
--------------------------------------------------------------------------------
-------------------------------------------------------------------------------- Interface RecoveryTime Action Status
-------------------------------------------------------------------------------- 10GE1/0/1 30 Block Normal 10GE1/0/2 30 Block Normal上述显示信息表明，接口10GE1/0/2恢复为正常状态。
配置脚本\# sysname DeviceA \# vlan batch 100 \# loopback-detect transmit interval 10 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 100 loopback-detect enable loopback-detect action block loopback-detect recovery-time 30 loopback-detect vlan 100 \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 100 loopback-detect enable loopback-detect action block loopback-detect recovery-time 30 loopback-detect vlan 100 \# return
