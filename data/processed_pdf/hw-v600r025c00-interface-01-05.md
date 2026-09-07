# S1700, S5700, S6700 V600R025C00 配置指南-接口管理 01-05 端口隔离配置

## 5 端口隔离配置

5端口隔离配置

### 5.1 端口隔离简介

### 5.2 端口隔离配置注意事项

5.3 配置端口隔离组
5.4 配置端口单向隔离
5.5 配置三层端口隔离
5.6 举例：配置二层端口隔离
5.1 端口隔离简介
定义
端口隔离可实现同一VLAN内端口之间的隔离。用户只需要将端口加入到隔离组中，就
可以实现隔离组内端口之间的二层、三层数据的隔离。同时，为了实现不同端口隔离
组的接口之间的隔离，可以通过配置接口之间的单向隔离功能来实现。
目的
采用端口隔离功能，可以实现同一VLAN内端口之间的隔离。隔离功能为用户提供了更
安全、更灵活的组网方案。
5.2 端口隔离配置注意事项
License 依赖
端口隔离无需License许可即可使用。

硬件依赖表 5-1 支持本特性的硬件

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
| S6750-S | S6750-S16X10Y2CZ，S6750-S16X8YZ，S6750- S24T16X8Y2CZ |

| 系列 | 支持产品 |
|---|---|
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
特性限制无

### 5.3 配置端口隔离组

背景信息如果用户希望隔离同一VLAN内的广播报文，但是不同端口下的用户还可以进行三层通信，则可以将隔离模式设置为二层隔离三层互通；如果用户希望同一VLAN不同端口下用户彻底无法通信，则可以将隔离模式配置为二层三层均隔离。端口隔离的方法和应用场景如图1 端口隔离示例组网图所示。PC1、PC2和PC3同属于VLAN10，将PC1与PC2对应的端口1和端口2加入端口隔离组后，PC1与PC2在VLAN10内不能互相访问，但是PC3与PC1之间可以互相访问，PC3与PC2之间也可以互相访问。
图 5-1 端口隔离示例组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。
操作步骤
1. 进入系统视图。
system-view
2. （可选）配置端口隔离模式。
port-isolate mode { l2 | all }缺省情况下，端口隔离模式为二层隔离三层互通。
说明该配置仅S6780-H、S6750-H、S6730-S-V2、S6750-S、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S5732-H-V2系列支持。
3. 进入以太网接口视图。
interface interface-type interface-number
4. 将接口从三层模式切换到二层模式。
portswitch根据实际接口类型自行选择是否需要执行此步骤。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。

5. 开启端口隔离组功能。
port-isolate enable group group-id
缺省情况下，未开启端口隔离组功能。端口隔离组只是针对同一设备上的端口隔
离组成员，对于不同设备上的接口而言，无法实现该功能。
检查配置结果
执行命令display port-isolate group { group-id | all }，查看接口隔离组的配置。
后续处理
完成配置端口隔离功能后，后续可以按需执行下列任务：
● 当希望一键式清除设备上所有的端口隔离配置时，可以在系统视图下执行clear
configuration port-isolate命令。
● 当希望某个VLAN的端口隔离不生效，VLAN内的用户依旧可以互相访问，可以在
系统视图下执行port-isolate exclude vlan { beginVlanId [ to endVlanId ] }
&<1-10>命令配置端口隔离功能生效时排除VLAN。

### 5.4 配置端口单向隔离

背景信息接入同一个设备不同接口的多台主机，若某台主机存在安全隐患，可能会向其他主机发送大量的广播报文。用户可以通过配置端口单向隔离来实现其他主机对该主机报文的隔离。同一端口隔离组的接口之间互相隔离，不同端口隔离组的接口之间不隔离。
如图1 端口单向隔离示例组网图所示，假设PC4存在安全隐患，会向其他主机发送大量广播报文，可以仅在PC4对应设备接口4上配置与接口5、接口6进行单向隔离，这样PC4发送的广播报文不能到达PC5、PC6，但从PC5、PC6发送的广播报文可以到达PC4。
图 5-2 端口单向隔离示例组网图

操作步骤步骤1 进入系统视图。
system-view步骤2 （可选）配置端口隔离模式。
port-isolate mode { l2 | all }缺省情况下，端口隔离模式为二层隔离三层互通。
说明该配置仅S6780-H、S6750-H、S6730-S-V2、S6750-S、S6750E-S、S6730-H-V2、S6730E-H- V2、S5755-H、S5755-S、S5732-H-V2系列支持。
步骤3 进入以太网接口视图。
interface interface-type interface-number步骤4 将接口从三层模式切换到二层模式。
portswitch根据实际接口类型自行选择是否需要执行此步骤。
仅S6780-H、S6750-H、S6730-S-V2、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤5 配置端口单向隔离功能。
am isolate { { interface-type interface-number1 | interface-name } &<1-8> | { interface-type interface- number1 to interface-number2 } }缺省情况下，未配置端口单向隔离功能。
----结束后续处理完成配置端口单向隔离功能后，后续可以按需执行下列任务：
● 当希望一键式清除设备上所有的端口隔离配置时，可以在系统视图下执行clear configuration port-isolate命令。
● 当希望某个VLAN的端口隔离不生效，VLAN内的用户依旧可以互相访问，可以在系统视图下执行port-isolate exclude vlan { beginVlanId [ to endVlanId ] } &<1-10> 命令配置端口隔离功能生效时排除 VLAN 。

### 5.5 配置三层端口隔离

背景信息配置端口三层隔离功能后，出接口和入接口相同的三层转发流量会在出接口被丢弃，从而避免产生环路。使能端口三层隔离功能后仅隔离三层流量。
说明该配置仅S6780-H、S6750-H、S6730-S-V2、S6750-S、S6750E-S、S6730-H-V2、S6730E-H- V2、S5755-H、S5755-S、S5732-H-V2系列支持。

操作步骤步骤1 进入系统视图。
system-view步骤2 进入以太网接口视图。
interface interface-type interface-number步骤3 将接口从二层模式切换到三层模式。
undo portswitch根据实际接口类型自行选择是否需要执行此步骤。
仅S6780-H系列、S6750-H、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755-S、S5755E-H、S5755-H、S6750-S系列、S5732-H-V2系列支持通过undo portswitch命令将接口从二层模式切换到三层模式。
步骤4 开启端口三层隔离功能。
port-isolate l3 enable缺省情况下，未开启三层端口隔离功能。
----结束

### 5.6 举例：配置二层端口隔离

组网需求如图5-3所示，PC1、PC2和PC3同属于VLAN10，用户希望PC1与PC2之间在VLAN10内不能互相访问，PC1与PC3之间可以互相访问，PC2与PC3之间可以互相访问。
图 5-3 配置二层端口隔离示例组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。
配置思路采用如下的思路配置二层端口隔离：

1. 配置接口加入VLAN。
2. 使能端口隔离功能。
配置注意事项
根据实际接口类型自行选择是否需要执行接口切换到二层模式的步骤。
操作步骤
步骤1 创建VLAN10，并将接口加入VLAN10。
<HUAWEI> system-view
[HUAWEI] sysname DeviceA
[DeviceA] vlan 10
[DeviceA-vlan10] quit
[DeviceA] interface 10ge 1/0/1
[DeviceA-10GE1/0/1] portswitch
[DeviceA-10GE1/0/1] port link-type access
[DeviceA-10GE1/0/1] port default vlan 10
[DeviceA-10GE1/0/1] quit
[DeviceA] interface 10ge 1/0/2
[DeviceA-10GE1/0/2] portswitch
[DeviceA-10GE1/0/2] port link-type access
[DeviceA-10GE1/0/2] port default vlan 10
[DeviceA-10GE1/0/2] quit
[DeviceA] interface 10ge 1/0/3
[DeviceA-10GE1/0/3] portswitch
[DeviceA-10GE1/0/3] port link-type access
[DeviceA-10GE1/0/3] port default vlan 10
[DeviceA-10GE1/0/3] quit
步骤2 配置二层端口隔离功能。
\# 配置10GE1/0/1的二层端口隔离功能。
[DeviceA] interface 10ge 1/0/1
[DeviceA-10GE1/0/1] port-isolate enable group 1
[DeviceA-10GE1/0/1] quit
\# 配置10GE1/0/2的二层端口隔离功能。
[DeviceA] interface 10ge 1/0/2
[DeviceA-10GE1/0/2] port-isolate enable group 1
[DeviceA-10GE1/0/2] quit
----结束
检查配置结果
● PC1和PC2不能互通。
● PC1和PC3可以互通。
● PC2和PC3可以互通。
配置脚本
DeviceA的配置文件
\#
sysname DeviceA
\#
vlan batch 10
\#
interface 10GE1/0/1

port link-type access port default vlan 10 port-isolate enable group 1 \# interface 10GE1/0/2 port link-type access port default vlan 10 port-isolate enable group 1 \# interface 10GE1/0/3 port link-type access port default vlan 10 \# return
