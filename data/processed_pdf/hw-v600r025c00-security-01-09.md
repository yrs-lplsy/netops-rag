# S1700, S5700, S6700 V600R025C00 配置指南-安全 01-09 业务和管理隔离配置

## 9 业务和管理隔离配置

背景信息为了保证设备的网络安全性，本着最小化攻击面的原则，设备遵循X.805的三层三面安全隔离机制：
● 管理平面：承载设备的操作维护数据流，也称为O&M平面。
● 控制平面：承载设备协议交互的数据流，也称为信令平面。
● 业务平面：承载设备信息转发的数据流，也称为转发平面或用户平面。
三面隔离后，任何一个平面在遭受攻击时，不会影响其他平面的正常运行和安全。例如，业务平面受到DoS攻击，不会影响管理平面，此时管理员可以通过管理平面登录来解决问题；如果不隔离，业务平面的处理任务会进一步占用CPU、内存等资源直至耗尽，导致管理员无法对设备进行管理。
业务平面与管理平面的隔离，即是业务接口流量与管理接口流量的隔离，其实现原理是：
● 禁止从业务接口上送管理数据，业务网络的用户无法通过业务接口访问设备管理接口连接的管理网络，实现业务接口与管理接口的物理隔离。
业务接口和管理接口分别绑定不同的VPN，数据不能互访，实现业务接口与管理
●接口的逻辑隔离。
说明仅S6780-H，S6750-S，S6750-H，S6730-S-V2，S6730-H-V2，S5732-H-V2，S5755-H，S6750E-S，S6730E-H-V2，S5755-S支持该功能。
License 依赖业务和管理隔离无需License许可即可使用。

硬件依赖表 9-1 支持本特性的硬件

| 系列 | 支持产品 |
|---|---|
| S6780-H | S6780-H4Z |
| S6750-H | S6750-H36C/S6750-H48Y8C/S6750-H48X8C |
| S6750-S | S6750-S16X8YZ/S6750-S16X10Y2CZ/S6750- S24T16X8Y2CZ |
| S6750E-S | S6750E-S16X10Y2CZ/S6750E-S24T16X8Y2CZ |
| S6730-S-V2 | S6730-S24X6Q-V2/S6730-S48X6Q-V2 |
| S6730-H-V2 | S6730-H48X6CZ-V2/S6730-H28X6CZ-V2/S6730- H48Y6C-V2/S6730-H48Y6C-TV2/S6730- H6FX4Y2CZ-V2/S6730-H24X6C-V2/S6730- H48X6C-V2/S6730-H48X6C-TV2 |
| S6730E-H-V2 | S6730E-H6FX4Y2CZ-V2 |
| S5732-H-V2 | S5732-H48UM4Y2CZ-V2/S5732-H48UM4Y2CZ- KV2/S5732-H48UM4Y2CZ-TV2/S5732- H24UM4Y2CZ-V2/S5732-H24UM4Y2CZ-KV2/ S5732-H44S4X6QZ-V2/S5732-H24S4X6QZ-V2/ S5732-H24S4X6QZ-TV2 |
| S5755-H | S5755-H24N4Y-A/S5755-H24P4Y2CZ/S5755- H24T4Y2CZ/S5755-H24U4Y2CZ/S5755- H24UN4Y2CZ/S5755-H24UTM4X4Y2C/S5755- H48N4Y-A/S5755-H48P4Y2CZ/S5755-H48T4Y2CZ/ S5755-H48U4Y2CZ/S5755-H48UN4Y2CZ/S5755- H48UTM4X4Y2C/S5755-H48T4Y2CZ-B/S5755- H24HB2Y2CZ/S5755-H24UM4Y2CZ/S5755- H48UM4Y2CZ |
| S5755-S | S5755-S24N8YZ/S5755-S24UN8YZ/S5755- S48N8YZ/S5755-S48UN8YZ/S5755-S24P8J8YZ/ S5755-S24P8Y/S5755-S24T8J8YZ/S5755-S24T8Y/ S5755-S24U8J8YZ/S5755-S24U8Y/S5755-S48P8Y/ S5755-S48P8YZ/S5755-S48T8Y/S5755-S48T8YZ/ S5755-S48U8Y/S5755-S48U8YZ/S5755-S48T8YZ-B |

特性限制无操作步骤
● 使能业务平面与管理平面的隔离功能，禁止从业务平面上送管理数据。

system-view undo management-plane isolate disable缺省情况下，设备的隔离功能默认使能。
配置业务接口和管理接口分别绑定不同的VPN，确保数据不能互访。
●
a. 创建并配置VPN实例management。
system-view ip vpn-instance management ipv4-family quit此处实例名称以management为例代表管理平面的VPN，实际配置时可以自己定义。
b. 创建并配置VPN实例service。
ip vpn-instance service ipv4-family quit此处实例名称以service为例代表业务平面的VPN，实际配置时可以自己定义。
c. 将管理接口绑定到 management ；将业务接口绑定到 service 。
interface meth 0/0/0 ip binding vpn-instance management quit interface interface-type interface-number ip binding vpn-instance service quit说明
● 建议根据业务实际需求，将业务接口绑定不同的VPN实例，即具体的业务只被绑定到必须的业务接口，实现更细粒度的业务隔离。
● 管理设备使用的LoopBack逻辑接口，也可以绑定到management。
● 若需隔离IPv6网络，需要在VPN实例视图下执行ipv6-family [ unicast ]命令使能VPN实例的IPv6地址族。
----结束任务示例如图9-1所示，192.168.20.0/24网段的业务网络和设备的业务接口interface1相连；
192.168.10.0/24网段的管理网络和设备的管理接口interface2相连。在设备上采用VPN逻辑隔离的配置方式来实现业务平面与管理平面的隔离，防止出现 192.168.20.0/24 可以Ping通192.168.10.0/24的现象，避免设备因管理接口地址泄露而遭受攻击。
图 9-1 业务与管理隔离示例组网图说明本例中interface1、interface2分别代表10GE1/0/1、MEth0/0/0。

本例中设备的配置脚本：
\# ip vpn-instance management ipv4-family \# ip vpn-instance service ipv4-family \# interface MEth0/0/0 ip binding vpn-instance management ip address 192.168.10.1 255.255.255.0 \# interface 10GE1/0/1 ip binding vpn-instance service ip address 192.168.20.1 255.255.255.0 \# return
