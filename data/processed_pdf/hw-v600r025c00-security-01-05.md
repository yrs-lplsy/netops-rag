# S1700, S5700, S6700 V600R025C00 配置指南-安全 01-05 IPSG配置

## 5 IPSG配置

5 IPSG 配置

### 5.1 IPSG简介

5.2 IPSG原理描述
5.3 IPSG配置注意事项
5.4 IPSG缺省配置
5.5 配置基于静态绑定表的IPSG
5.6 配置基于动态绑定表的IPSG
5.7 （可选）配置IP报文检查告警功能
5.8 （可选）配置丢弃源IP地址与目的IP地址相同的IP报文
5.9 维护IPSG
5.10 IPSG配置举例
5.11 IPSG常见配置错误
简介
5.1 IPSG
定义
IP源防攻击IPSG（IP Source Guard）是一种基于二层接口的源IP地址过滤技术，它能
够防止恶意主机伪造合法主机的IP地址来仿冒合法主机，还能确保非授权主机不能通
过自己指定IP地址的方式来访问网络或攻击网络。
目的
随着网络规模越来越大，通过伪造源IP地址实施的网络攻击（简称IP地址欺骗攻击）也
逐渐增多。一些攻击者通过伪造合法用户的IP地址获取网络访问权限，非法访问网
络，甚至造成合法用户无法访问网络，或者信息泄露。IPSG针对IP地址欺骗攻击提供
了一种防御机制，可以有效阻止此类网络攻击行为。
一个典型的利用IPSG防攻击的示例如图1所示，非法主机伪造合法主机的IP地址获取上
网权限。此时，通过在Device的用户侧的接口或VLAN上部署IPSG功能，Device可以对
进入接口的IP报文进行检查，丢弃非法主机的报文，从而阻止此类攻击。

图 5-1 IPSG 典型防攻击受益
● 可以有效降低为保证网络正常运行和网络信息安全而产生的维护成本。
● 可以提供安全的网络环境以及更稳定的网络服务。

### 5.2 IPSG原理描述

IPSG 的基本原理IPSG利用绑定表（源IP地址、源MAC地址、所属VLAN、入接口、掩码的绑定关系）去匹配检查二层接口上收到的IP报文，只有匹配绑定表的报文才允许通过，其他报文将被丢弃。
绑定表如表1所示，包括静态和动态两种。
说明仅IPv6静态绑定表中存在掩码。
表 5-1 绑定表

| 绑定表类型 | 生成过程 | 适用场景 |
|---|---|---|
| 静态绑定表 | 使用user-bind static命令手工配置。 | 针对IPv4、IPv6主机，适用于主机数较少且主机使用静态IP地址的场景。 |
| DHCP Snooping动态绑定表 | 配置DHCP Snooping功能后，DHCP主机动态获取IP 地址时，设备根据DHCP 服务器发送的DHCP回复报文动态生成。 | 针对IPv4、IPv6主机，适用于主机数较多且主机从 DHCP服务器获取IP地址的场景。 |

绑定表生成后，IPSG基于绑定表向指定的接口或者指定的VLAN下发ACL，由该ACL来匹配检查所有IP报文。主机发送的报文，只有匹配绑定表才会允许通过，不匹配绑定表的报文都将被丢弃。当绑定表信息变化时，设备会重新下发ACL。缺省情况下，如果在没有绑定表的情况下使能了IPSG，设备会允许除IGMP协议报文和MLD协议报文外的IP协议报文通过，尝试通过该设备进行转发的IP数据报文将被丢弃。
说明IPSG只匹配检查主机发送的IP报文，对于ARP等非IP报文，IPSG不做匹配检查。
IPSG原理图如图1所示，非法主机仿冒合法主机的IP地址发送报文到达Device后，因报文和绑定表不匹配被Device丢弃。
图 5-2 IPSG 实现原理图IPSG一般应用在用户侧的接入设备上，可以基于接口或者基于VLAN应用。
● 在用户侧的接口上应用IPSG，该接口接收的所有IP报文均进行IPSG检查。
● 在用户侧的VLAN上应用IPSG，属于该VLAN的所有接口接收到IP报文均进行IPSG检查。
● 如果用户侧的接入设备不支持IPSG功能，也可以在上层设备的接口或者VLAN上应用IPSG。
IPSG 中的接口角色IPSG仅支持在二层物理接口或者VLAN上应用，且只对使能了IPSG功能的非信任接口进行检查。对于IPSG来说，缺省所有的接口均为非信任接口，信任接口由用户指定。
IPSG的信任接口/非信任接口也就是DHCP Snooping中的信任接口/非信任接口，信任接口/非信任接口同样适用于基于静态绑定表方式的IPSG。
IPSG 中各接口角色如图 2 所示。其中：
● Interface1和Interface2接口为非信任接口且使能IPSG功能，从Interface1和Interface2接口收到的报文会执行IPSG检查。

● Interface3接口为非信任接口但未使能IPSG功能，从Interface3接口收到的报文不
会执行IPSG检查，可能存在攻击。
● Interface4接口为用户指定的信任接口，从Interface4接口收到的报文也不会执行
IPSG检查，但此接口一般不存在攻击。在DHCP Snooping的场景下，通常把与合
法DHCP服务器直接或间接连接的接口设置为信任接口。
图 5-3 IPSG 中的接口角色
IPSG 的过滤方式
绑定表项包含：MAC地址、IP地址、VLAN ID、入接口、掩码。静态绑定表项中指定
的信息均用于IPSG过滤接口收到的报文。而对于动态绑定表，IPSG依据该表项中的哪
些信息过滤接口收到的报文，由用户设置的检查项决定，缺省是四项都进行匹配检
查。常见的几种检查项如表2所示，其他组合类似，不一一列举。
说明
仅IPv6静态绑定表中存在掩码。
表 5-2 IPSG 的过滤方式

| 设置的检查项 | 含义 |
|---|---|
| 基于源IP地址过滤 | 根据源IP地址对报文进行过滤，只有源IP地址和绑定表匹配，才允许报文通过。 |
| 基于源MAC地址过滤 | 根据源MAC地址对报文进行过滤，只有源MAC地址和绑定表匹配，才允许报文通过。 |
| 基于源IP地址+源 MAC地址过滤 | 根据源IP和源MAC地址对报文进行过滤，只有源IP和源MAC 地址都和绑定表匹配，才允许报文通过。 |
| 基于源IP地址+源 MAC地址+接口过滤 | 根据源IP地址、源MAC地址和接口对报文进行过滤，只有源 IP、源MAC地址和接口都和绑定表匹配，才允许报文通过。 |

| 设置的检查项 | 含义 |
|---|---|
| 基于源IP地址+源 MAC地址+接口 +VLAN过滤 | 根据源IP地址、源MAC地址、接口和VLAN对报文进行过滤，只有源IP地址、源MAC地址、接口和VLAN都和绑定表匹配，才允许报文通过。 |

### 5.3 IPSG配置注意事项

License 依赖IPSG无需License许可即可使用。
硬件依赖表 5-3 支持本特性的硬件

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

| 系列 | 支持产品 |
|---|---|
| S6730-H-V2 | S6730-H24X6C-V2，S6730-H28X6CZ-V2，S6730- H48X6C-TV2，S6730-H48X6C-V2，S6730- H48X6CZ-V2，S6730-H48Y6C-TV2，S6730- H48Y6C-V2，S6730-H6FX4Y2CZ-V2 |
| S5735I-H-V2 | S5735I-H24U8S4XE-QA-V2，S5735I-H8T2XN- V2，S5735I-H8T4S2XN-V2，S5735I-H8U2XN-V2 |
| S6750-S | S6750-S16X10Y2CZ，S6750-S16X8YZ，S6750- S24T16X8Y2CZ |
| S5735S-L3 | S5735S-L24P4S-A3，S5735S-L24P4XE-A3， S5735S-L24PN4XE-A3，S5735S-L24ST4X-A3， S5735S-L24T4S-QA3，S5735S-L24T4X-QA3， S5735S-L24T8J4XE-A3，S5735S-L48P4S-A3， S5735S-L48P4XE-A3，S5735S-L48PN4XE-A3， S5735S-L48S4X-A3，S5735S-L48T4S-A3，S5735S- L48T4XE-A3，S5735S-L8P4X-QA3，S5735S- L8T4X-QA3 |
| S5755-H | S5755-H24HB2Y2CZ，S5755-H24N4Y-A，S5755- H24P4Y2CZ，S5755-H24T4Y2CZ，S5755- H24U4Y2CZ，S5755-H24UM4Y2CZ，S5755- H24UN4Y2CZ，S5755-H24UTM4X4Y2C，S5755- H48N4Y-A，S5755-H48P4Y2CZ，S5755- H48T4Y2CZ，S5755-H48T4Y2CZ-B，S5755- H48U4Y2CZ，S5755-H48UM4Y2CZ，S5755- H48UN4Y2CZ，S5755-H48UTM4X4Y2C |
| S5735R-S-V2 | S5735R-S24P4X-V2，S5735R-S24T8J4X-XA-V2， S5735R-S48P4X-V2，S5735R-S48T4X-XA-V2 |
| S6780-H | S6780-H4Z |
| S5735E-L-V2 | S5735E-L16LP2UM2X-QA-V2，S5735E-L16LP2X- QA-V2，S5735E-L24HJ4XE-A-V2，S5735E- L24P4S-A-V2，S5735E-L24P4XE-A-V2，S5735E- L24ST4XE-A-V2，S5735E-L24T4XE-A-V2， S5735E-L48LP4S-A-V2，S5735E-L48LP4XE-A-V2， S5735E-L48S4XE-A-V2，S5735E-L48T4XE-A-V2， S5735E-L8P4X-QA-V2，S5735E-L8T4X-QA-V2 |
| S5755-S | S5755-S24N8YZ，S5755-S24P8J8YZ，S5755- S24P8Y，S5755-S24T8J8YZ，S5755-S24T8Y， S5755-S24U8J8YZ，S5755-S24U8Y，S5755- S24UN8YZ，S5755-S48N8YZ，S5755-S48P8Y， S5755-S48P8YZ，S5755-S48T8Y，S5755- S48T8YZ，S5755-S48T8YZ-B，S5755-S48U8Y， S5755-S48U8YZ，S5755-S48UN8YZ |

| 系列 | 支持产品 |
|---|---|
| S5735R-L-V2 | S5735R-L16LP2S-QA-V2，S5735R-L16LP2UM2X- QA-V2，S5735R-L16LP2X-QA-V2，S5735R- L16T4S-A-V2，S5735R-L16T4X-QA-V2，S5735R- L24P4S-A-V2，S5735R-L24P4X-A-V2，S5735R- L24T4S-A-V2，S5735R-L24T4X-QA-V2，S5735R- L48LP4S-A-V2，S5735R-L48LP4X-A-V2，S5735R- L48P4X-A-V2，S5735R-L48T4S-A-V2，S5735R- L48T4X-A-V2，S5735R-L8P4S-A-V2，S5735R- L8P4X-QA-V2，S5735R-L8T4S-A-V2，S5735R- L8T4X-QA-V2 |
| S5735-L-V2 | S5735-L10T4X-A-V2，S5735-L14P2S-QA-V2， S5735-L16LP2UM2X-QA-V2，S5735-L16LP2X-QA- V2，S5735-L16P2UM2X-QA-V2，S5735-L16T4S- A-V2，S5735-L16T4X-QA-V2，S5735-L24HJ4XE- A-V2，S5735-L24J4X-A-V2，S5735-L24J4X-D- V2，S5735-L24LU8S4XE-QA-V2，S5735-L24P4S- A-V2，S5735-L24P4XE-A-V2，S5735-L24PN4XE- A-V2，S5735-L24ST4XE-A-V2，S5735-L24T4S-A- V2，S5735-L24T4X-QA-V2，S5735-L24T4XE-A- V2，S5735-L24T4XE-D-V2，S5735-L24T8J4XE-A- V2，S5735-L48J4X-A-V2，S5735-L48J4X-D-V2， S5735-L48LP4S-A-V2，S5735-L48LP4XE-A-V2， S5735-L48LPN4XE-A-V2，S5735-L48P4XE-A-V2， S5735-L48PN4XE-A-V2，S5735-L48S4X-A-V2， S5735-L48S4XE-A-V2，S5735-L48T4S-A-V2， S5735-L48T4XE-A-V2，S5735-L48T4XE-D-V2， S5735-L8P2T4X-A-V2，S5735-L8P4S-A-V2， S5735-L8P4X-QA-V2，S5735-L8T4S-A-V2， S5735-L8T4X-QA-V2 |
| S6730-S-V2 | S6730-S24X6Q-V2，S6730-S48X6Q-V2 |
| S5735I-S-V2 | S5735I-S16T2S4XN-V2，S5735I-S16T8S4XE-QD- V2，S5735I-S24T4XE-V2，S5735I-S24T8S4XE-QA- V2，S5735I-S24U4XE-V2，S5735I-S48T4XE-V2， S5735I-S8T4SN-V2，S5735I-S8T4XN-V2，S5735I- S8T8P2S4XN-V2，S5735I-S8U2XN-V2，S5735I- S8U4XN-V2 |
| S5732-H-V2 | S5732-H24S4X6QZ-TV2，S5732-H24S4X6QZ- V2，S5732-H24UM4Y2CZ-KV2，S5732- H24UM4Y2CZ-V2，S5732-H44S4X6QZ-V2， S5732-H48UM4Y2CZ-KV2，S5732-H48UM4Y2CZ- TV2，S5732-H48UM4Y2CZ-V2 |

查询工具如需了解硬件规格、产品部件的配套关系，请点击硬件中心进行查询；如需了解关键规格、全量软件规格，请点击规格查询进行查询。

特性限制表 5-4 本特性的使用限制

| 特性限制 |
|---|
| 绑定表是否生效依赖硬件资源，实际生效情况可以通过命令display ip source check user-bind status查看。 |
| 对于S6750-H系列，S6730E-H-V2系列，S6750E-S系列，S6730-S-V2系列，S5755- H系列，S6780-H系列，S5732-H-V2系列，S6730-H-V2系列，S5755-S系列， S6750-S系列： IPSG与M-LAG互斥。 |
| 对于S5735R-L-V2系列，S1730S-S3系列，S5735-L-V2系列，S5735S-L3系列， S5735-S-V2系列，S5735E-S-V2系列，S5735I-S-V2系列，S5735R-S-V2系列， S5735I-L-V2系列，S5735E-L-V2系列，S5735S-S3系列，S5735I-H-V2系列：丢弃源IP地址与目的IP地址相同的IP报文功能对于二层报文不生效 |
| 对于S6750-H系列，S1730S-S3系列，S5735S-L3系列，S5735-S-V2系列，S5735E- S-V2系列，S5735R-S-V2系列，S6780-H系列，S5735E-L-V2系列，S5735S-S3系列，S5755-S系列，S5735R-L-V2系列，S5735-L-V2系列，S5735I-S-V2系列， S5735I-L-V2系列，S5735I-H-V2系列：设备可以学习到被IPSG丢弃的报文的MAC地址，可能造成占用MAC规格、触发MAC 漂移、改变流量转发路径等影响。 |

### 5.4 IPSG缺省配置

IPSG的主要缺省配置如表1所示。
表 5-5 IPSG 缺省配置

| 参数 | 缺省值 |
|---|---|
| IP报文检查功能 | 未使能 |
| IP报文检查选项 | ● 基于静态绑定表：根据配置的绑定表项进行完全匹配，即绑定表项有几项，就检查几项。 ● 基于动态绑定表：源IP地址、源MAC 地址、接口和VLAN。 |
| IP报文检查告警功能 | 未使能 |
| IP报文检查告警阈值 | 100 |
| 丢弃源IP地址与目的IP地址相同的IP报文功能 | 未使能 |

### 5.5 配置基于静态绑定表的IPSG

#### 5.5.1 开启基于静态绑定表的IPSG功能

背景信息该方式适用于局域网络中主机数较少且主机被分配固定IP地址的情况。静态绑定表创建后，IPSG并未生效，只有在指定接口或在指定VLAN上使能IPSG后才生效。
● 基于接口使能IPSG：该接口接收的所有的报文均进行IPSG检查。如果用户只希望在某些不信任的接口上进行IPSG检查，而信任其他接口，可以选择此方式。并且，当接口属于多个VLAN时，基于接口使能IPSG更方便，无需在每个VLAN上使能。
● 基于VLAN使能IPSG：属于该VLAN的所有接口接收的报文均进行IPSG检查。如果用户只希望在某些不信任的VLAN上进行IPSG检查，而信任其他VLAN，可以选择此方式。并且，当多个接口属于同一VLAN时，基于VLAN使能IPSG更方便，无需在每个接口上使能。
说明
● 如果在VLAN和接口下都配置了IPSG功能，则先配置的生效，后配置的不生效。
● 设备ACL资源不足时可能会导致绑定表下发失败，但是设备可以查看到IPSG相关配置，此时需要通过执行命令行display ip source check user-bind status static [ [ { interface { interface-name | interface-type interface-number } | ip-address ip-address | ipv6- address ipv6-address [ ipv6-prefix ipv6-prefix ]| mac-address mac-address | vlan vlan- id } * ] [ valid | invalid ] | summary ] [ slot slot-id ]，查看回显中的Status字段确认IPSG功能是否生效。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置静态绑定表项。静态绑定表项包括IPv4和IPv6两种绑定表项，请根据网络环境选择配置。
配置IPv4静态绑定表项。
●user-bind static { ip-address { start-ip [ to end-ip ] } &<1-10> | mac-address mac-address } * [ interface { interface-type interface-number | interface-name } ] [ vlan vlan-id [ ce-vlan ce-vlan-id ] ]
● 配置IPv6静态绑定表项。
user-bind static { { ipv6-address { start-ipv6 [ to end-ipv6 ] } &<1-10> | ipv6-prefix prefix/prefix-length } | mac-address mac-address } * [ interface { interface-type interface-number | interface-name } ] [ vlan vlan- id [ ce-vlan ce-vlan-id ] ]缺省情况下，不存在静态绑定表。

说明IPSG按照静态绑定表项进行完全匹配，即静态绑定表项包含几项就检查几项。请确保所创建的绑定表是正确且完整的，主机发送的报文只有匹配绑定表才会允许通过，不匹配绑定表的报文都将被丢弃。
设备支持将多个IP地址（段）做批量绑定，例如多个IP批量绑定到同一个接口或同一个MAC。
● 如果这些IP地址不是连续的，可以重复输入1～10个start-ip地址。例如执行命令user-bind static ip-address 10.0.0.1 10.0.0.3 10.0.0.5 interface 10GE 1/0/1，将多个IP地址绑定到同一个接口。
● 如果这些IP地址是连续的，可以重复输入1～10个start-ip to end-ip的地址段。需要注意的是，采用关键字to输入的区间不能有交叉。例如执行命令user-bind static ip-address
10.0.0.1 to 10.0.0.4 mac-address 00e0-fc12-3456，将多个IP地址绑定到同一个MAC地址。
步骤3 （可选）配置信任接口。
说明主机是静态地址分配的环境，一般不需要配置信任接口。但当上行接口同时在使能IPSG功能的VLAN内，则需要将上行口配置成信任接口，否则回程报文会因匹配不到绑定表而被丢弃，具体情况请参考IPSG中未配置上行信任接口导致IP报文被丢弃。配置为信任接口后，从信任接口收到的报文不做匹配检查直接允许通过，可以避免上述问题的发生。
1. 全局使能DHCP功能。
dhcp enable缺省情况下，全局未使能DHCP功能。
2. 全局使能DHCP Snooping功能。
dhcp snooping enable缺省情况下，全局未使能DHCP Snooping功能。
3. 配置信任接口。
– 在接口视图下配置信任接口。
interface interface-type interface-number dhcp snooping trusted quit
– 在VLAN视图下配置信任接口。
vlan vlan-id dhcp snooping trusted interface interface-type interface-number quit缺省情况下，接口为未信任状态。
步骤4 开启IPSG功能。
● 在接口视图下开启IPSG功能。以下方式，请根据网络环境任选一种。
interface interface-type interface-number ipv4 source check user-bind enable quit interface interface-type interface-number ipv6 source check user-bind enable quit
● 在VLAN视图下开启IPSG功能。以下方式，请根据网络环境任选一种。
vlan vlan-id ipv4 source check user-bind enable quit vlan vlan-id ipv6 source check user-bind enable quit缺省情况下，未开启IPSG功能。
----结束

检查配置结果
● 执行命令display ip source check user-bind statistics [ interface { interface- name | interface-type interface-number } ]，查看IPSG的丢弃报文统计信息。
● 执行命令display ip source check user-bind status [ [ static [ { interface { interface-name | interface-type interface-number } | ip-address ip-address| ipv6-address ipv6-address [ ipv6-prefix ipv6-prefix ] | mac-address mac- address | vlan vlan-id } * ] [ valid | invalid ] ] | summary ] [ slot slot-id ]，查看IPSG静态绑定表项信息以及状态。

### 5.6 配置基于动态绑定表的IPSG

#### 5.6.1 开启基于动态绑定表的IPSG功能

背景信息该方式适用于局域网络中主机较多，或者主机使用 DHCP 动态获取 IP 地址的情况。主机能通过合法的DHCP服务器获取IP地址，对于与其直接或间接相连的设备接口设置为信任接口，其他接口设置为非信任接口，IPSG对于从信任接口收到的报文不做匹配检查，直接允许通过。从而保证合法主机只能从合法的DHCP服务器获取IP地址，私自架设的DHCP Server仿冒者无法为合法主机分配IP地址。在连接用户的接口或VLAN下使能DHCP Snooping功能之后，需将连接DHCP服务器的接口配置为“信任”模式，两者同时生效设备即能够生成DHCP Snooping动态绑定表。
动态绑定表创建后，IPSG并未生效，只有在指定接口或在指定VLAN上使能IPSG后才生效。
● 基于接口使能IPSG：该接口接收的所有的报文均进行IPSG检查。如果用户只希望在某些不信任的接口上进行IPSG检查，而信任其他接口，可以选择此方式。并且，当接口属于多个VLAN时，基于接口使能IPSG更方便，无需在每个VLAN上使能。
● 基于VLAN使能IPSG：属于该VLAN的所有接口接收的报文均进行IPSG检查。如果用户只希望在某些不信任VLAN上进行IPSG检查，而信任其他VLAN，可以选择此方式。并且，当多个接口属于相同的VLAN时，基于VLAN使能IPSG更方便，无需在每个接口上使能。
说明
● 如果在VLAN和接口下都使能IPSG功能，则先配置的生效，后配置的不生效。
● 设备ACL资源不足时可能会导致绑定表下发失败，但是设备可以查看到IPSG相关配置，此时需要通过执行命令行display ip source check user-bind status dynamic [ { interface { interface-name | interface-typeinterface-number } | ip-address ip-address | ipv6- address ipv6-address [ ipv6-prefix ipv6-prefix ] | mac-address mac-address | vlan vlan- id } * ] [ valid | invalid ] [ slot slot-id ]，查看回显中的Status字段确认IPSG功能是否生效。
操作步骤步骤 1 进入系统视图。
system-view步骤2 配置DHCP Snooping功能，生成动态绑定表。

1. 全局使能DHCP功能。
dhcp enable
缺省情况下，全局未使能DHCP功能。
2. 全局使能DHCP Snooping功能。
dhcp snooping enable
缺省情况下，全局未使能DHCP Snooping功能。
3. 配置信任接口。
– 在接口视图下配置信任接口。
interface interface-type interface-number
dhcp snooping enable
dhcp snooping trusted
quit
– 在VLAN视图下配置信任接口。
vlan vlan-id
dhcp snooping enable
dhcp snooping trusted interface interface-type interface-number
quit
步骤3 开启IPSG功能。
● 在接口视图下开启 IPSG 功能。以下方式，请根据网络环境任选一种。
interface interface-type interface-number
ipv4 source check user-bind enable
quit
interface interface-type interface-number
ipv6 source check user-bind enable
quit
● 在VLAN视图下开启IPSG功能。以下方式，请根据网络环境任选一种。
vlan vlan-id
ipv4 source check user-bind enable
quit
vlan vlan-id
ipv6 source check user-bind enable
quit
缺省情况下，未开启IPSG功能。
步骤4 （可选）配置IP报文检查项。
使能IPSG功能后，在设备接收到IP报文时，按照设置的检查项对其进行匹配检查，只
有通过检查的报文才能被转发，否则被丢弃。IP报文的接口信息为必查项，IP报文的可
选的检查项包括：源IP地址、源MAC地址、VLAN。
● 接口视图下配置 IP 报文检查项。
interface interface-type interface-number
ip source check user-bind check-item { ip-address | mac-address | vlan } *
quit
● VLAN视图下配置IP报文检查项。
vlan vlan-id
ip source check user-bind check-item { ip-address | mac-address | interface } *
quit
缺省情况下，IP报文检查项包括IP地址、MAC地址、VLAN和接口。如果用户信任某些
检查项，或者某些项目不固定（例如客户端的流量可能从不同的接口进入设备），可
以选择配置此步骤。一般采用缺省值。
----结束

检查配置结果
● 执行命令display ip source check user-bind configuration [ vlan vlan-id | interface { interface-name | interface-type interface-number } ]，查看接口、VLAN下IPSG的配置信息。
● 执行命令display ip source check user-bind statistics [ interface { interface- name | interface-type interface-number } ]，查看IPSG的丢弃报文统计信息。
● 执行命令display ip source check user-bind status [ [ dynamic [ { interface { interface-name | interface-type interface-number } | ip-address ip-address | ipv6-address ipv6-address [ ipv6-prefix ipv6-prefix ] | mac-address mac- address | vlan vlan-id } * ] [ valid | invalid ] ] | summary ] [ slot slot-id ]，查看IPSG动态绑定表项信息以及状态。

### 5.7 （可选）配置IP报文检查告警功能

背景信息配置 IP 报文告警后，在设备丢弃 IP 报文时会记录日志，如果被丢弃的报文数量超过告警阈值，设备还会向网管发送告警信息。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置IP报文检查告警功能。
● 在接口视图下开启IP报文检查告警功能。
interface interface-type interface-number ip source check user-bind alarm enable quit
● 在VLAN视图下开启IP报文检查告警功能。
vlan vlan-id ip source check user-bind alarm enable quit缺省情况下，未开启IP报文检查告警功能。
步骤3 配置IP报文检查告警阈值。
● 在接口视图下配置IP报文检查告警阈值。
interface interface-type interface-number ip source check user-bind alarm threshold threshold quit在VLAN视图下配置IP报文检查告警阈值。
●vlan vlan-id ip source check user-bind alarm threshold threshold quit缺省情况下，IP报文检查告警阈值为100。
----结束

### 5.8 （可选）配置丢弃源IP地址与目的IP地址相同的IP报文

背景信息源IP地址与目的IP地址相同的IP报文出现的场景比较特殊，比如管理员做一些内部测试时，可能会构造这种报文。缺省情况下，这类报文可以被正常转发。当管理员通过某些软件检测到此类报文流量过大，怀疑为LAND攻击时，可以配置丢弃这类报文。
说明对于S5735R-L-V2、S1730S-S3、S5735-L-V2、S5735S-L3、S5735-S-V2、S5735E-S-V2、S5735I-S-V2、S5735R-S-V2、S5735I-L-V2、S5735E-L-V2、S5735S-S3、S5735I-H-V2，丢弃源IP地址与目的IP地址相同的IP报文功能对于二层报文不生效。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置丢弃源IP地址与目的IP地址相同的IP报文。
ip anti-attack source-ip equals destination-ip drop { all | slot slot-id }
----结束

### 5.9 维护IPSG

日常维护中，还可以清除IPSG的丢弃报文统计信息。如有需要，可在用户视图下执行以下命令。
须知清除IPSG的丢弃报文统计信息后，以前的信息将无法恢复，务必仔细确认。
表 5-6 清除 IPSG 相关的统计信息

| 操作 | 命令 |
|---|---|
| 清除IPSG的丢弃报文统计信息。 | reset ip source check user-bind statistics [ vlan vlan-id | interface [ interface-name | interface-type interface-number ] ] |

### 5.10 IPSG配置举例

#### 5.10.1 举例：基于接口配置静态绑定表的IPSG

组网需求如图 基于接口配置静态绑定表的IPSG组网图所示，PC1和PC2通过DeviceA接入网络，PC1和PC2均使用静态配置的IP地址。管理员希望用户使用固定IP地址上网，不允许私自更改IP地址非法获取网络访问权限。
图 5-4 基于接口配置静态绑定表的 IPSG 组网图说明本例中interface1和interface2分别代表10GE1/0/1和10GE1/0/2。
操作步骤步骤1 在DeviceA上创建静态绑定表项。
\# 在DeviceA上创建静态绑定表项。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] user-bind static ip-address 10.0.0.1 mac-address 00e0-fc12-3456 [DeviceA] user-bind static ip-address 10.0.0.11 mac-address 00e0-fc12-3478步骤2 开启IPSG功能。
\# 在DeviceA的10GE1/0/1、10GE1/0/2接口使能IPSG。
[DeviceA] interface 10GE 1/0/1 [DeviceA-10GE1/0/1] ipv4 source check user-bind enable [DeviceA-10GE1/0/1] quit [DeviceA] interface 10GE 1/0/2 [DeviceA-10GE1/0/2] ipv4 source check user-bind enable [DeviceA-10GE1/0/2] quit
----结束检查配置结果\# 查看静态绑定表信息。
[DeviceA] display ip source check user-bind status User-bind table on slot 1:

#### 5.10.2 举例：基于VLAN配置静态绑定表的IPSG

----------------------------------------------------------------------------------------------------------
IP Address Prefix Vlan(O/I) Interface Binding
MAC Address Type Status
-----------------------------------------------------------------------------------------------------------
10.0.0.1 - - /- - DHCP
00e0-fc12-3456 Static IPv4/-
10.0.0.11 - - /- - DHCP
00e0-fc12-3478 Static IPv4/-
-----------------------------------------------------------------------------------------------------------
Total count: 2
配置文件
DeviceA
\#
sysname DeviceA
\#
user-bind static ip-address 10.0.0.1 mac-address 00e0-fc12-3456
user-bind static ip-address 10.0.0.11 mac-address 00e0-fc12-3478
\#
interface 10GE1/0/1
ipv4 source check user-bind enable
\#
interface 10GE1/0/2
ipv4 source check user-bind enable
\#
return
举例：基于 配置静态绑定表的
5.10.2 VLAN IPSG
组网需求
如图 基于VLAN配置静态绑定表的IPSG组网图所示，PC1和PC2通过DeviceA接入网
络，Gateway为企业出口网关，PC1和PC2均使用静态配置的IP地址。管理员在
DeviceA上做了接口限制，希望PC使用管理员分配的固定IP地址、从固定的接口上线。
同时为了安全考虑，不允许外来人员的电脑随意接入内网。
图 5-5 基于 VLAN 配置静态绑定表的 IPSG 组网图
说明
本例中interface1、interface2、interface3和interface4分别代表10GE1/0/1、10GE1/0/2、
10GE1/0/3和10GE1/0/4。

操作步骤步骤1 配置各接口所属VLAN。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 10 [DeviceA] interface 10GE 1/0/1 [DeviceA-10GE1/0/1] port link-type access [DeviceA-10GE1/0/1] port default vlan 10 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10GE 1/0/2 [DeviceA-10GE1/0/2] port link-type access [DeviceA-10GE1/0/2] port default vlan 10 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10GE 1/0/3 [DeviceA-10GE1/0/3] port link-type access [DeviceA-10GE1/0/3] port default vlan 10 [DeviceA-10GE1/0/3] quit [DeviceA] interface 10GE 1/0/4 [DeviceA-10GE1/0/4] port link-type trunk [DeviceA-10GE1/0/4] port trunk allow-pass vlan 10 [DeviceA-10GE1/0/4] quit步骤2 在DeviceA的10GE1/0/1和10GE1/0/2接口上创建静态绑定表项。
[DeviceA] user-bind static ip-address 10.0.0.1 mac-address 00e0-fc12-3456 interface 10GE 1/0/1 [DeviceA] user-bind static ip-address 10.0.0.2 mac-address 00e0-fc12-3478 interface 10GE 1/0/2步骤3 配置上行口10GE1/0/4为信任接口。
[DeviceA] dhcp enable [DeviceA] dhcp snooping enable [DeviceA] interface 10GE 1/0/4 [DeviceA-10GE1/0/4] dhcp snooping trusted [DeviceA-10GE1/0/4] quit步骤4 在连接PC的VLAN10上使能IPSG功能。

[DeviceA] vlan 10 [DeviceA-vlan10] ipv4 source check user-bind enable [DeviceA-vlan10] quit
----结束检查配置结果\# 查看静态绑定表信息。
[DeviceA] display ip source check user-bind status User-bind table on slot 1:
-------------------------------------------------------------------------------- IP Address Prefix Vlan(O/I) Interface Binding MAC Address Type Status
--------------------------------------------------------------------------------
10.0.0.1 - - /- 10GE1/0/1 DHCP 00e0-fc12-3456 Static IPv4/-
10.0.0.2 - - /- 10GE1/0/2 DHCP 00e0-fc12-3478 Static IPv4/-
-------------------------------------------------------------------------------- Total count: 2配置脚本DeviceA \# sysname DeviceA \# dhcp enable \# dhcp snooping enable user-bind static ip-address 10.0.0.1 mac-address 00e0-fc12-3456 interface 10GE1/0/1 user-bind static ip-address 10.0.0.2 mac-address 00e0-fc12-3478 interface 10GE1/0/2 \# vlan batch 10 \# vlan 10 ipv4 source check user-bind enable \# interface 10GE1/0/1 port link-type access port default vlan 10 \# interface 10GE1/0/2 port link-type access port default vlan 10 \# interface 10GE1/0/3 port link-type access port default vlan 10 \# interface 10GE1/0/4 port link-type trunk port trunk allow-pass vlan 10 dhcp snooping trusted \# return

#### 5.10.3 举例：基于VLAN配置动态绑定表的IPSG

组网需求如图 基于VLAN配置动态绑定表的IPSG组网图所示，PC1和PC2通过DeviceA接入网络。管理员希望PC使用动态分配的地址，不允许私自配置静态IP地址，如果私自指定IP地址将无法访问网络。
图 5-6 基于 VLAN 配置动态绑定表的 IPSG 组网图说明本例中interface1、interface2和interface3分别代表10GE1/0/1、10GE1/0/2和10GE1/0/3。
操作步骤步骤1 配置各接口所属VLAN。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 10 [DeviceA] interface 10GE 1/0/1 [DeviceA-10GE1/0/1] port link-type access [DeviceA-10GE1/0/1] port default vlan 10 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10GE 1/0/2 [DeviceA-10GE1/0/2] port link-type access [DeviceA-10GE1/0/2] port default vlan 10 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10GE 1/0/3 [DeviceA-10GE1/0/3] port link-type trunk [DeviceA-10GE1/0/3] port trunk allow-pass vlan 10 [DeviceA-10GE1/0/3] quit步骤2 使能DHCP Snooping功能，并将连接DHCP Server的10GE1/0/3接口配置为信任接口。
[DeviceA] dhcp enable [DeviceA] dhcp snooping enable [DeviceA] vlan 10 [DeviceA-vlan10] dhcp snooping enable [DeviceA-vlan10] dhcp snooping trusted interface 10GE 1/0/3

步骤3 在DeviceA的VLAN10上使能IPSG功能。
[DeviceA-vlan10] ipv4 source check user-bind enable [DeviceA-vlan10] quit
----结束检查配置结果\# 查看动态绑定表信息。
[DeviceA] display ip source check user-bind status User-bind table on slot 1:
-------------------------------------------------------------------------------- IP Address Prefix Vlan(O/I) Interface Binding MAC Address Type Status
--------------------------------------------------------------------------------
10.1.1.254 - 10 /- 10GE1/0/1 DHCP 00e0-fc12-3456 Dynamic IPv4/-
10.1.1.253 - 10 /- 10GE1/0/2 DHCP 00e0-fc12-3478 Dynamic IPv4/-
-------------------------------------------------------------------------------- Total count: 2配置脚本DeviceA \# sysname DeviceA \# vlan batch 10 \# dhcp enable \# dhcp snooping enable \# vlan 10 dhcp snooping enable dhcp snooping trusted interface 10GE1/0/3 ipv4 source check user-bind enable \# interface 10GE1/0/1 port link-type access port default vlan 10 \# interface 10GE1/0/2 port link-type access port default vlan 10 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 10 \# return

#### 5.10.4 举例：配置IPSG防止DHCP动态主机私自更改IP地址

组网需求如图5-7所示，PC1、PC2和PC3通过DeviceA接入网络，DeviceB作为DHCP Server为PC1和PC2动态分配IP地址，PC3使用静态IP地址，Gateway为企业出口网关。管理员希望PC1和PC2不能私自配置静态IP地址，私自配置IP地址后将无法访问网络。

说明本例中interface1、interface2、interface3和interface4分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3和10GE1/0/4。
图 5-7 配置 IPSG 防止 DHCP 动态主机私自更改 IP 地址组网图操作步骤步骤1 在DeviceB上配置DHCP Server功能。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan batch 10 [DeviceB] interface 10GE 1/0/1 [DeviceB-10GE1/0/1] port link-type trunk [DeviceB-10GE1/0/1] port trunk allow-pass vlan 10 [DeviceB-10GE1/0/1] quit [DeviceB] dhcp enable [DeviceB] ip pool 10 [DeviceB-ip-pool-10] network 10.1.1.0 mask 24 [DeviceB-ip-pool-10] gateway-list 10.1.1.1 [DeviceB-ip-pool-10] quit [DeviceB] interface vlanif 10 [DeviceB-Vlanif10] dhcp enable [DeviceB] interface vlanif 10 [DeviceB-Vlanif10] ip address 10.1.1.1 255.255.255.0 [DeviceB-Vlanif10] dhcp select global [DeviceB-Vlanif10] quit步骤2 在DeviceA上配置DHCP Snooping功能。

\# 配置各接口所属VLAN。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 10 [DeviceA] interface 10GE 1/0/1 [DeviceA-10GE1/0/1] port link-type access [DeviceA-10GE1/0/1] port default vlan 10 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10GE 1/0/2 [DeviceA-10GE1/0/2] port link-type access [DeviceA-10GE1/0/2] port default vlan 10 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10GE 1/0/3 [DeviceA-10GE1/0/3] port link-type access [DeviceA-10GE1/0/3] port default vlan 10 [DeviceA-10GE1/0/3] quit [DeviceA] interface 10GE 1/0/4 [DeviceA-10GE1/0/4] port link-type trunk [DeviceA-10GE1/0/4] port trunk allow-pass vlan 10 [DeviceA-10GE1/0/4] quit \# 使能DHCP Snooping功能，并将连接DHCP Server的10GE1/0/4接口配置为信任接口。
[DeviceA] dhcp enable [DeviceA] dhcp snooping enable [DeviceA] vlan 10 [DeviceA-vlan10] dhcp snooping enable [DeviceA-vlan10] dhcp snooping trusted interface 10GE 1/0/4步骤3 创建PC3的静态绑定表项。
[DeviceA] user-bind static ip-address 10.0.0.3 mac-address 00e0-fc12-3489 interface 10GE 1/0/3 vlan 10步骤4 在连接PC的VLAN10上使能IPSG功能。
[DeviceA] vlan 10 [DeviceA-vlan10] ipv4 source check user-bind enable [DeviceA-vlan10] quit
----结束检查配置结果\# 查看PC1和PC2的动态绑定表信息。
[DeviceA] display dhcp snooping user-bind all DHCP Dynamic Bind-table:
Flags:O - outer vlan ,I - inner vlan ,P - Vlan-mapping IP Address MAC Address VSI/VLAN(O/I/P) Interface Lease
--------------------------------------------------------------------------------
10.1.1.254 00e0-fc12-3456 10 /-- /-- GE10GE1/0/1 2014.08.17-07:31
10.1.1.253 00e0-fc12-3478 10 /-- /-- GE10GE1/0/2 2014.08.17-07:34
-------------------------------------------------------------------------------- Print count: 2 Total count: 2 \# 查看PC3的静态绑定表信息。
[ ~ DeviceA] display user-bind static all DHCP static Bind-table:
Flags:O - outer vlan ,I - inner vlan IP Address MAC Address VLAN(O/I) Interface
--------------------------------------------------------------------------------
10.0.0.3 00e0-fc12-3489 10/-- 10GE1/0/3
-------------------------------------------------------------------------------- Print count: 1 Total count: 1

配置脚本DeviceA \# sysname DeviceA \# vlan batch 10 \# dhcp enable \# dhcp snooping enable user-bind static ip-address 10.0.0.3 mac-address 00e0-fc12-3489 interface 10GE 1/0/3 vlan 10 \# vlan 10 dhcp snooping enable dhcp snooping trusted interface 10GE 1/0/4 ipv4 source check user-bind enable \# interface 10GE 1/0/1 port link-type access port default vlan 10 \# interface 10GE 1/0/2 port link-type access port default vlan 10 \# interface 10GE 1/0/3 port link-type access port default vlan 10 \# interface 10GE 1/0/4 port link-type trunk port trunk allow-pass vlan 10 \# return DeviceB \# sysname DeviceB \# vlan batch 10 \# dhcp enable \# ip pool 10 gateway-list 10.1.1.1 network 10.1.1.0 mask 255.255.255.0 \# interface Vlanif10 ip address 10.1.1.1 255.255.255.0 dhcp select global \# interface 10GE 1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# return

### 5.11 IPSG常见配置错误

#### 5.11.1 接口或VLAN上未使能导致IPSG功能不生效

故障现象已创建并生成了绑定表，但IPSG功能未能生效。
可能原因IPSG没有在指定接口或者指定VLAN上使能。
操作步骤步骤1 查看用户侧接口上是否使能了IPSG。
display ip source check user-bind status static [ { interface interface-type interface-number | ip-address ip-address | ipv6-address ipv6-address [ ipv6-prefix ipv6-prefix ]| mac-address mac-address | vlan vlan- id } * ] [ valid | invalid ] [ slot slot-id ]步骤2 如果接口未使能IPSG，在VLAN视图下查看用户侧的VLAN上是否使能了IPSG。
display this步骤3 如果接口和VLAN上均未使能IPSG功能（显示信息中无“ipv4 source check user- bind enable或ipv6 source check user-bind enable”），请在接口视图或者VLAN视图下使能IPSG功能。
● 使能IPv4报文检查功能ipv4 source check user-bind enable
● 使能IPv6报文检查功能ipv6 source check user-bind enable说明接口或VLAN方式只选择其一即可，两者的区别在于：
● 基于接口使能IPSG：该接口接收的所有的报文均进行IPSG检查。如果用户只希望在某些不信任的接口上进行IPSG检查，而信任其他接口，可以选择此方式。并且，当接口属于多个VLAN时，基于接口使能IPSG更方便，无需在每个VLAN上使能。
● 基于VLAN使能IPSG：属于该VLAN的所有接口接收的报文均进行IPSG检查。如果用户只希望在某些不信任VLAN上进行IPSG检查，而信任其他VLAN，可以选择此方式。并且，当多个接口属于相同的VLAN时，基于VLAN使能IPSG更方便，无需在每个接口上使能。
另外，需要注意的是，IPSG仅在使能的接口或使能的VLAN上生效，未使能的接口和VLAN上不会执行IPSG检查。所以如果是部分的接口或VLAN上IPSG不生效，很可能是这部分接口或VLAN上未使能IPSG导致的。
----结束

#### 5.11.2 静态绑定表项错误导致合法主机IP报文被丢弃

故障现象已创建静态绑定表且使能了IPSG功能，但合法主机IP报文被丢弃。
可能原因合法主机绑定表信息不正确。

操作步骤步骤1 查看静态绑定表信息是否正确。
display ip source check user-bind status static [ { interface interface-type interface-number | ip-address ip-address | ipv6-address ipv6-address [ ipv6-prefix ipv6-prefix ]| mac-address mac-address | vlan vlan- id } * ] [ valid | invalid ] [ slot slot-id ]步骤2 如果合法主机信息不在绑定表中，请添加该主机的绑定表项。只有绑定表中存在该主机的表项，设备才允许主机的报文通过。
user-bind static { ip-address { start-ip [ to end-ip ] } &<1-10> | ipv6-address { start-ipv6-address [ to end- ipv6-address ] } &<1-10> | ipv6-prefix prefix | mac-address mac-address } * [ interface { interface-type interface-number | interface-name }] [ vlan vlan-id [ ce-vlan ce-vlan-id ] ]步骤3 如果合法主机信息在绑定表中，请查看该条表项的MAC地址是否正确，是否因主机更换了网卡未及时刷新绑定表导致。如果是，请删除该条绑定表项并重新添加。
undo user-bind static [ ip-address { start-ip [ to end-ip ] } &<1-10> | ipv6-address { start-ipv6-address [ to end-ipv6-address ] } &<1-10> | ipv6-prefix prefix | mac-address mac-address | interface { interface- type interface-number | interface-name } | vlan vlan-id [ ce-vlan ce-vlan-id ] ] *步骤4 如果合法主机信息在绑定表中，请查看该条表项是否包含VLAN信息。如果包含VLAN信息，查看主机接入的接口是否加入该VLAN中。只有该接口加入了这个VLAN，设备才允许主机的报文通过。
display vlan
----结束

#### 5.11.3 IPSG中未配置上行信任接口导致IP报文被丢弃

故障现象VLAN内使能IPSG后所有主机访问不了外网，合法主机IP报文被丢弃。
如图1所示，PC1和PC2同属于VLAN10，Interface1允许VLAN10报文通过。在DeviceA上创建了PC1和PC2的静态绑定表项，并且基于VLAN10使能了IPSG功能。PC无法访问Internet（PC之间可以通信）。以PC1为例说明。
● PC1发往Internet的报文：当报文到达DeviceA的Interface1接口时，DeviceA检查报文和绑定表匹配，允许报文通过。
● 从Internet发往PC1的回程报文：当报文到达DeviceA的Interface3接口时，因为Interface3接口在VLAN10内，DeviceA会检查报文是否和绑定表匹配，因匹配失败（绑定表中无对应的绑定表项）而丢弃报文。

#### 5.11.4 上行接口使能IPSG导致IP报文被丢弃

图 5-8 IPSG 中未配置上行信任接口导致 IP 报文被丢弃可能原因在使能IPSG功能的VLAN内，未将上行口配置成信任接口。
操作步骤步骤1 检查上行口是否在使能IPSG功能的VLAN内。
display ip source check user-bind status static [ { interface interface-type interface-number | ip-address ip-address | ipv6-address ipv6-address [ ipv6-prefix ipv6-prefix ]| mac-address mac-address | vlan vlan- id } * ] [ valid | invalid ] [ slot slot-id ]步骤2 如果上行接口同时在使能IPSG功能的VLAN内，则需要将上行口配置成信任接口，否则回程报文会因匹配不到绑定表而被丢弃。
1. 进入系统视图。
system-view
2. 全局使能DHCP功能。
dhcp enable
3. 全局使能DHCP Snooping功能。
dhcp snooping enable
4. Interface3接口视图下配置信任接口。
dhcp snooping trusted
----结束上行接口使能 导致 报文被丢弃
5.11.4 IPSG IP故障现象接口上使能IPSG后所有主机访问不了外网，合法主机IP报文被丢弃。
如图1所示，在DeviceA上创建了PC1和PC2的静态绑定表项，Interface1、Interface2和Interface3上同时使能了IPSG功能后，PC无法访问Internet（PC之间可以互通）。以PC1为例说明。

● PC1发往Internet的报文：当报文到达DeviceA的Interface1接口时，DeviceA检查
报文和绑定表匹配，允许报文通过。
● 从Internet发往PC1的回程报文：当报文到达DeviceA的Interface3接口时，因
Interface3使能了IPSG功能，DeviceA检查报文是否和绑定表匹配，因匹配失败
（绑定表中无对应的绑定表项）而丢弃报文。
图 5-9 上行接口使能 IPSG 导致 IP 报文被丢弃
可能原因
上行接口使能IPSG功能，但是未将上行口配置成信任接口。
操作步骤
步骤1 查看上行接口Interface3是否使能了IPSG功能。
display ip source check user-bind status static [ { interface interface-type interface-number | ip-address
ip-address | ipv6-address ipv6-address [ ipv6-prefix ipv6-prefix ]| mac-address mac-address | vlan vlan-
id } * ] [ valid | invalid ] [ slot slot-id ]
步骤2 如果接口上使能了IPSG功能（显示信息中含有“ipv4 source check user-bind
enable或ipv6 source check user-bind enable”），请在接口视图下去使能IPSG功
能。
● 去使能IPv4报文检查功能
undo ipv4 source check user-bind enable
● 去使能IPv6报文检查功能
undo ipv6 source check user-bind enable
----结束

#### 5.11.5 动态环境下未配置DHCP Snooping导致IPSG功能不生效

故障现象主机通过DHCP服务器可以动态获取到IP地址，使能IPSG后功能不生效。

可能原因配置了DHCP功能，但是未配置DHCP Snooping功能。
操作步骤步骤1 检查DHCP Snooping动态绑定表是否存在。在主机通过DHCP方式获取IP地址的环境下，IPSG借助DHCP Snooping动态绑定表，对接口上接收的报文进行匹配检查。只有配置了DHCP Snooping功能，设备才会在主机上线时自动生成的DHCP Snooping动态绑定表。
display ip source check user-bind status dynamic [ { interface interface-type interface-number | ip- address ip-address | ipv6-address ipv6-address [ ipv6-prefix ipv6-prefix ]| mac-address mac-address | vlan vlan-id } * ] [ valid | invalid ] [ slot slot-id ]步骤2 如果没有动态绑定表项，请参见配置动态绑定表中的步骤，完成DHCP Snooping动态绑定表的配置。
说明DHCP Snooping配置完成后，主机重新上线后，设备会生成DHCP Snooping绑定表，IPSG才能生效。并且，如果设备在没有生成DHCP Snooping动态绑定表的情况下使能了IPSG，设备会拒绝所有除DHCP请求报文外的其他IP报文，DHCP主机的通信都会受到影响。所以，使能IPSG功能之前请先配置DHCP Snooping生成动态绑定表。
----结束
