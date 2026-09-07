# S1700, S5700, S6700 V600R024C10 配置指南-安全 01-06 端口安全配置

## 6 端口安全配置

6端口安全配置

### 6.1 端口安全简介

6.2 端口安全原理描述
6.3 端口安全配置注意事项
6.4 端口安全缺省配置
6.5 配置端口安全
6.6 端口安全配置举例
6.1 端口安全简介
定义
端口安全（Port Security）指的是一种将接口学习到的动态MAC地址转换为安全MAC
地址的安全功能。
目的
非法用户获取到设备某接口的MAC地址以后，企图以该接口的MAC地址为目的MAC地
址与设备通信，从而发起攻击。
为避免这种攻击，设备可以使能端口安全功能，将接口学习到的动态 MAC 地址转换为
安全MAC地址。此时，接口上之前学习到的动态MAC地址表项将被删除，接口重新学
习的MAC数量达到上限后不再学习新的MAC地址。对于接口收到的报文，如果其中的
源MAC地址在MAC地址表项中不存在，均视为非法用户攻击，并实施丢弃报文、告警
上报、或者关闭接口的保护动作。

### 6.2 端口安全原理描述

安全 MAC 的分类表 6-1 安全 MAC 地址的说明

| 类型 | 含义 | 特点 | 场景 |
|---|---|---|---|
| 安全动态MAC 地址 | 接口使能端口安全功能后，接口上之前学习到的动态MAC地址表项将被删除，接口重新学习到的动态 MAC地址即转换为安全动态MAC地址。 | 设备重启或接口down 之后表项会丢失，需要重新学习。只有在设置老化时间后才会被老化，缺省情况下不会被老化。可以限制地址的数量。可以设置接口的保护动作：丢弃报文、告警上报、或者关闭接口。 | 设备接入的用户变动比较频繁，可以在设备的用户侧接口配置安全动态MAC地址功能。这样，保证安全的同时，也可以通过老化及时清除绑定的MAC地址表项。 |
| Sticky MAC地址 | 接口使能端口安全功能，再使能Sticky MAC功能后，接口当前的安全动态MAC地址、之后学习到的动态MAC地址转换为 Sticky MAC地址。 | 重启设备或接口down 之后表项不会丢失。不会被老化。可以限制地址的数量。可以设置接口的保护动作：丢弃报文、告警上报、或者关闭接口。 | 设备接入的用户变动较少，可以在设备的用户侧接口配置Sticky MAC 地址功能。这样，保证安全的同时，绑定的 MAC地址表项不会丢失。 |
| 安全静态MAC 地址 | 接口使能端口安全功能后，再手工配置的静态MAC地址。 | 重启设备或接口down 之后表项不会丢失。不会被老化。 | 设备接入的用户变动较少，且数量较少，可以在设备的用户侧接口配置安全静态MAC地址功能，手工实现MAC地址表项的绑定。 |

说明接口的Sticky MAC功能去使能以后，接口Sticky MAC地址会转换后安全动态MAC地址。接口的端口安全功能再去使能后，接口的安全动态MAC地址将被删除，重新学习动态MAC地址。
安全 MAC 地址的老化只有安全动态MAC地址，在设置老化时间后才会被老化。
说明当设备同时启用全局MAC地址老化和安全动态MAC地址老化功能时，全局MAC地址老化机制可能会对安全动态MAC地址的流量匹配造成影响，在极端情况下可能导致安全动态MAC地址被异常老化并重新学习。

● 绝对时间老化：如绝对老化时间为5分钟，系统每隔5分钟检测一次是否存在这个
MAC的流量。若没有流量，则立即将这个安全动态MAC地址老化。
● 相对时间老化：如相对老化时间为5分钟，系统每隔1分钟检测一次是否存在这个
MAC的流量。若没有流量，则经过5分钟后将这个安全动态MAC地址老化。
● 强制时间老化：如强制老化时间为5分钟，系统每隔1分钟计算一次每个MAC的存
在时间。若大于等于5分钟，则立即将这个安全动态MAC地址老化。
端口安全的保护动作
接口使能端口安全功能后，如果收到报文的源MAC地址在MAC地址表项中不存在，无
论报文的目的MAC地址是否存在，均视为非法用户攻击，并实施对应安全动作。
说明
如果设备使能了静态MAC地址漂移的检测功能，也可以对于这个功能检测到的非法报文（收到
源MAC地址在其他接口的静态MAC地址表项中）实施对应安全动作。
接口使能端口安全功能后，用户通过ARP报文接入网络。由于ARP报文具有较高的业务优先级，
当设备端口接收到源MAC地址不在本端口静态MAC表中的超限报文时，无法触发error-down接
口状态切换及安全告警上报的预期保护动作。这种情况不仅限于ARP报文，其他类似业务场景
中，只要对应业务报文的优先级高于超限报文，系统也只会触发非法报文丢弃动作，而抑制
error-down状态切换及告警上报等低优先级保护动作。
表 6-2 端口安全的保护动作

| 动作 | 说明 |
|---|---|
| restrict | 丢弃非法报文；并上报告警。推荐使用restrict动作。 |
| protect | 只丢弃非法报文；不上报告警。 |
| error-down | 丢弃非法报文；并关闭接口，即接口状态被置为error-down；并上报告警。默认情况下，接口关闭后不会自动恢复，只能由网络管理人员在接口视图下使用restart命令重启接口进行恢复。如果用户希望被关闭的接口可以自动恢复，则可在接口error-down 前通过在系统视图下执行error-down auto-recovery cause portsec-reachedlimit interval interval-value命令使能接口状态自动恢复为Up的功能，并设置接口自动恢复为Up的延时时间，使被关闭的接口经过延时时间后能够自动恢复。 |

### 6.3 端口安全配置注意事项

License 依赖端口安全无需License许可即可使用。

硬件依赖表 6-3 支持本特性的硬件

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
特性限制表 6-4 本特性的使用限制特性限制主接口（含物理口和LAG）使能端口安全达到预期MAC数量后的动作对附属子接口也生效主接口（含物理口和LAG）使能MAC-Limit达到预期MAC数量后的动作对附属子接口也生效

| 特性限制 |
|---|
| 对于S6750-H系列，S6730E-H-V2系列，S6750E-S系列，S5755-H系列，S6780-H 系列，S5732-H-V2系列，S6730-H-V2系列，S5755-S系列，S6750-S系列：端口安全功能在接入VXLAN网络的接口上不生效 |
| 端口安全MAC迁移场景，端口A学到了动态安全MAC，源MAC为此MAC的流量从端口B接入，会触发该MAC的流量持续命中，从而导致端口A上学习到的动态安全MAC 无法老化。 |
| 对于S6750-H系列，S6730E-H-V2系列，S6750E-S系列，S5755-H系列，S6780-H 系列，S5732-H-V2系列，S6730-H-V2系列，S5755-S系列，S6750-S系列：端口安全叠加MLAG超限场景，超限报文无法触发MLAG选主。 |

### 6.4 端口安全缺省配置

端口安全的缺省配置如表 6-5 所示。
表 6-5 端口安全缺省配置

| 参数 | 缺省值 |
|---|---|
| 端口安全功能 | 未使能 |
| 安全MAC地址数量 | 1个 |
| 端口安全的保护动作 | restrict |
| 安全动态MAC地址老化时间 | 未使能 |

### 6.5 配置端口安全

前提条件关闭接口的Smart Link、SEP、ERPS功能，否则会导致这些功能无法破环。
关闭接口的MAC地址学习限制功能，避免功能冲突。

#### 6.5.1 配置安全动态MAC地址功能

操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface { interface-name | interface-type interface-number }步骤3 将接口从三层模式切换到二层模式。
portswitch

仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 使能端口安全功能，并配置MAC学习的数量限制。
port-security enable [ maximum max-number ]说明接口开启端口安全功能后，即表示安全动态MAC地址功能生效。
步骤5 （可选）配置端口安全的保护动作。
port-security protect-action { protect | restrict | error-down }步骤6 （可选）配置安全动态MAC地址的老化时间。
port-security aging-time time [ type { absolute | inactivity | force } ]请合理配置MAC表项老化时间，设置时间过短（比如1分钟）会导致MAC表项老化过快，流量转发失败。
步骤7 退出接口视图。
quit步骤8 （可选）删除安全动态MAC地址表项。
undo mac-address security { [ interface-type interface-number | interface-name ] | [ vlan vlanId ] } *
----结束检查配置结果
● 执行display port-security [ interface { interface-typeinterface-number | interface-name } ]命令，查看端口安全信息。
● 执行display trapbuffer命令或者通过网管，查看端口安全相关告警。

#### 6.5.2 配置Sticky MAC地址功能

操作步骤步骤1 进入系统视图。
system-view步骤 2 进入接口视图。
interface { interface-name | interface-type interface-number }步骤3 将接口从三层模式切换到二层模式。
portswitch仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 开启端口安全功能，并配置MAC学习的数量限制。
port-security enable [ maximum max-number ]步骤5 开启Sticky MAC地址功能。
port-security mac-address sticky

说明接口开启Sticky MAC地址功能，安全动态MAC地址将转换为Sticky MAC地址，之后学习到的MAC地址也成为Sticky MAC地址。
接口开启Sticky MAC地址功能，即使配置了port-security aging-time命令，Sticky MAC地址也不会被老化。
Sticky MAC表项配置或发生变更时需要通过命令save才能保证整机重启后按照新配置或变更的MAC表项生效。
Sticky MAC表项通过命令save保存在后缀是dtbl、ztbl或者ctbl的文件中，文件在设备重启时不丢弃。这个文件的文件名称必须与系统配置文件的名称保持一致，比如系统配置文件是test.cfg，则Sticky MAC表项文件必须是test.ctbl，否则会导致设备重启后Sticky MAC地址表项恢复失败。
步骤6 （可选）配置端口安全的保护动作。
port-security protect-action { protect | restrict | error-down }步骤7 （可选）手工增加一条Sticky MAC地址表项。
port-security mac-address sticky mac-address vlan vlan-id步骤8 退出接口视图。
quit步骤9 （可选）删除Sticky MAC地址表项。
undo mac-address sticky { [ portType portNum | portName ] | [ vlan vlanId ] } *
----结束检查配置结果执行display
● port-security [ interface { interface-type interface-number | interface-name } ]命令，查看端口安全信息。
● 执行display trapbuffer命令或者通过网管，查看端口安全相关告警。

#### 6.5.3 配置安全静态MAC地址功能

操作步骤步骤1 进入系统视图。
system-view步骤 2 进入接口视图。
interface { interface-name | interface-type interface-number }步骤3 将接口从三层模式切换到二层模式。
portswitch仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 开启端口安全功能，并配置MAC学习的数量限制。
port-security enable [ maximum max-number ]步骤5 手工配置一条安全静态MAC地址表项。
port-security mac-address mac-address vlan vlan-id

说明即使配置了port-security aging-time命令，安全静态MAC地址表项也不会被老化。
步骤6 退出接口视图。
quit步骤7 （可选）删除安全静态MAC地址表项。
undo mac-address sec-config { [ portType portNum | portName ] | [ vlan vlanId ] } *
----结束检查配置结果
● 执行display port-security [ interface { interface-typeinterface-number | interface-name } ]命令，查看端口安全信息。
● 执行display trapbuffer命令或者通过网管，查看端口安全相关告警。

#### 6.5.4 配置静态MAC地址漂移检测功能

背景信息为了能够使得设备在检测到静态MAC地址漂移时，上报告警提示网络管理人员去识别并修复接入问题，可以在设备上使能静态MAC地址漂移检测功能，并且在接口使能端口安全功能。这样，接口收到静态MAC地址发生漂移的报文时，将实施端口安全的保护动作，例如上报告警。
操作步骤步骤1 进入系统视图。
system-view步骤2 使能静态MAC地址漂移检测功能。
port-security static-flapping protect步骤3 进入接口视图。
interface { interface-name | interface-type interface-number }步骤4 将接口从三层模式切换到二层模式。
portswitch仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤5 使能端口安全功能，并配置MAC学习的数量限制。
port-security enable [ maximum max-number ]步骤6 （可选）配置端口安全的保护动作。
port-security protect-action { protect | restrict | error-down }步骤 7 退出接口视图。
quit
----结束

检查配置结果执行display trapbuffer命令或者通过网管，查看端口安全相关告警。

#### 6.5.5 配置端口安全和认证模式下不同广播域用户上线功能

前提条件用户使能了端口安全和端口认证功能。
背景信息在用户授权变更的场景中，当用户从VLAN 10下线时，未及时删除对应的Sticky MAC条目。如果该用户的MAC地址随后在VLAN 20中试图上线，设备将验证此MAC地址的合法性。因该MAC地址在VLAN 10已被记录，导致验证失败，从而触发告警等端口保护动作。为了避免这一问题，可以开启端口安全与认证模式下的"不同广播域用户上线"功能。这确保了即使在多个广播域中，每个MAC地址在设备中只保留一个记录。当用户从一个广播域迁移到另一个时，如从VLAN 10转移到VLAN 20，系统会自动清除原广播域中的旧MAC条目。启用此功能后，用户在广播域变更后的重新上线过程不影响端口安全表项，不会触发告警等端口保护动作。
操作步骤步骤1 进入系统视图。
system-view步骤2 开启端口安全和认证模式下不同广播域用户上线功能，即基于MAC为Key模式匹配同一端口下的用户。
port-security mac-address convert-from-dynamic multi-authen enhance enable说明该功能开启后对于认证配置的Muti-Share模式不生效。
除了Sticky类型的MAC表项，该功能开启后对于命令行配置的有配置文件的静态类型MAC表项该功能不生效。
开启该功能后会触发全局删除Security和Sticky类型的MAC表项并触发用户重新上线。
----结束

### 6.6 端口安全配置举例

#### 6.6.1 举例：配置端口安全

组网需求如图 6-1 所示，本公司员工的 PC1 、 PC2 、 PC3 ，在同一个 VLAN10 中可以互通，并且通过接入设备DeviceA连接到公司网络。为了保证公司网络的安全性，希望仅允许本公司员工的PC1、PC2、PC3可以访问公司网络，其他外来人员使用自己携带的PC禁止访问公司网络。

图 6-1 端口安全组网图说明本例中interface1，interface2，interface3分别代表10GE1/0/1，10GE1/0/2，10GE1/0/3。
配置思路
1. 配置VLAN，实现本公司员工PC间互通。
2. 配置端口安全功能，限制接口MAC学习数量，阻止外来人员PC访问公司网络。
操作步骤步骤1 配置VLAN。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 10 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type access [DeviceA-10GE1/0/1] port default vlan 10 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type access [DeviceA-10GE1/0/2] port default vlan 10 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] portswitch [DeviceA-10GE1/0/3] port link-type access [DeviceA-10GE1/0/3] port default vlan 10 [DeviceA-10GE1/0/3] quit步骤2 配置端口安全功能。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] port-security enable maximum 1 [DeviceA-10GE1/0/1] port-security mac-address sticky [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] port-security enable maximum 1 [DeviceA-10GE1/0/2] port-security mac-address sticky [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/3

[DeviceA-10GE1/0/3] port-security enable maximum 1 [DeviceA-10GE1/0/3] port-security mac-address sticky [DeviceA-10GE1/0/3] quit
----结束检查配置结果DeviceA的这3个接口，插入PC1、PC2、PC3以外的其他PC，无法访问公司网络。
配置脚本\# sysname DeviceA \# vlan batch 10 \# interface 10GE1/0/1 port link-type access port default vlan 10 port-security enable maximum 1 port-security mac-address sticky \# interface 10GE1/0/2 port link-type access port default vlan 10 port-security enable maximum 1 port-security mac-address sticky \# interface 10GE1/0/3 port link-type access port default vlan 10 port-security enable maximum 1 port-security mac-address sticky \# return
