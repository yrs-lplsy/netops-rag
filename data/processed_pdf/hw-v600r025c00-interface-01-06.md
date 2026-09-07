# S1700, S5700, S6700 V600R025C00 配置指南-接口管理 01-06 串口透传配置

## 6 串口透传配置

6串口透传配置

### 6.1 串口透传简介

### 6.2 串口透传原理描述

串口透传配置注意事项
6.3
6.4 串口透传缺省配置
6.5 配置串口透传
6.6 维护串口透传
6.7 举例：配置串口透传
6.1 串口透传简介定义串口透传是指在数据传输过程中，通过设备将远程终端单元RTU（Remote Terminal Unit）发送的串行数据与IP网络中服务器发送的IP报文相互转换，实现对现场状况的监控。
目的为了对现场状况进行监控，服务器需要与RTU进行通信。但是RTU只能通过串口通信，而服务器又需要IP网络来通信，那么如何使两者建立连接成为一个问题。通过配置串口透传技术可以解决这个问题。设备一端通过串口与RTU相连，另一端利用IP网络与服务器相连，在配置串口透传功能后，将RTU传送的串行数据封装成IP报文，再通过IP网络将封装后的IP报文传送到服务器，并还能够将服务器发送的IP报文解封装为串行数据，然后通过串口传递给RTU，实现服务器对现场状况的监控。
6.2 串口透传原理描述串口透传基本架构串口透传基本架构如图1所示。

图 6-1 串口透传基本架构示意图说明设备仅支持RS485串口与RTU相连。
串口透传基本架构中，主要包括以下三种角色：
● RTU RTU 是安装在远程现场的电子设备，负责对现场信号、工业设备的监测和控制。
RTU将测得的状态或信号转换成可在通信媒体上发送的数据格式；它还将从服务器发送来的数据转换成命令，实现对现场工业设备的功能控制。
● Device Device一端通过串口与RTU建立连接，另一端通过IP网络与服务器建立连接。将接收到的串口数据转发给服务器；并将服务器发送过来的IP报文解封装为串行数据通过串口传送给RTU。
● 服务器通过接收现场RTU设备的数据，对现场的运行设备进行监视和控制，以实现数据采集、设备控制、测量、参数调节以及各类信号报警等各项功能。
串口透传工作过程在串口透传功能中，设备可以作为TCP Server、TCP Client或UDP Client与服务器建立IP连接。
● 设备作为TCP Server时，串口透传报文转发流程如图2所示。
图 6-2 设备作为 TCP Server 时串口透传报文转发示意图

设备作为TCP Server，串口透传报文转发流程主要分为如下六个步骤：
a. 服务器向Device发送TCP连接请求。
b. Device接收服务器发起的TCP连接请求，通过TCP三次握手后，建立TCP连接。
c. 服务器将TCP报文发送给Device。
d. Device将服务器发送的TCP报文转换成串行数据后，通过串口发送到RTU。
e. RTU发送串行数据给Device。
f. Device将RTU发送的串行数据封装成TCP报文后，通过IP网络发送到服务器。
说明在通过步骤1和2建立TCP连接后，RTU、Device或服务器都可以首先发送报文给对端，上述流程是以服务器首先发送TCP报文（步骤3）为例说明。
● 设备作为TCP Client时，串口透传报文转发流程如图3所示。
图 6-3 设备作为 TCP Client 时串口透传报文转发示意图设备作为TCP Client，串口透传报文转发流程主要分为如下六个步骤：
a. Device向服务器发送TCP连接请求。
b. 服务器接收 Device 发起的 TCP 连接请求，通过 TCP 三次握手后，建立 TCP 连接。
c. RTU发送串行数据给Device。
d. Device将RTU发送的串行数据封装成TCP报文后，通过IP网络发送到服务器。
e. 服务器将TCP报文发送给Device。
Device将服务器发送的TCP报文转换成串行数据后，通过串口发送到RTU。
f.
说明在通过步骤 1 和 2 建立 TCP 连接后， RTU 、 Device 或服务器都可以首先发送报文给对端，上述流程是以RTU首先发送串行数据（步骤3）为例说明。
● 设备作为UDP Client时，串口透传报文转发流程如图4所示。

图 6-4 设备作为 UDP Client 时串口透传报文转发示意图设备作为UDP Client，串口透传报文转发流程主要分为如下两个步骤：
a. RTU发送串行数据给Device。
b. Device将RTU发送的串行数据封装成UDP报文后，通过IP网络发送到服务器。

### 6.3 串口透传配置注意事项

License 依赖串口透传无需License许可即可使用。
硬件依赖表 6-1 支持本特性的硬件

| 系列 | 支持产品 |
|---|---|
| S5735I-S-V2 | S5735I-S16T2S4XN-V2，S5735I-S8T4SN-V2， S5735I-S8T4XN-V2，S5735I-S8T8P2S4XN-V2， S5735I-S8U4XN-V2 |
| S5735I-H-V2 | S5735I-H8T4S2XN-V2 |

查询工具如需了解硬件规格、产品部件的配套关系，请点击硬件中心进行查询；如需了解关键规格、全量软件规格，请点击规格查询进行查询。
特性限制表 6-2 本特性的使用限制

| 特性 | 特性限制 |
|---|---|
| 串口透传业务 | 串口透传特性与堆叠特性互斥 |

| 特性 | 特性限制 |
|---|---|
| 串口透传业务 | 串口使能串口透传之后，串口不可以分配给容器。串口分配给容器之后，不可以使能串口透传特性。 |

### 6.4 串口透传缺省配置

表 6-3 串口透传参数缺省值

| 参数 | 缺省配置 |
|---|---|
| 串口透传功能 | 未使能 |
| RS485串口 | 业务口 |
| 串口业务模式 | NONE模式 |
| RAW业务功能 | 未使能 |
| 设备串口透传业务模式 | 未配置 |

### 6.5 配置串口透传

#### 6.5.1 配置TTY用户界面的属性

背景信息每个用户界面有对应的用户界面视图（User-interface view），在用户界面视图下网络管理员可以配置一系列参数，比如传输速率等，设备要保持这些参数与RTU的相关参数一致。当用户使用该用户界面登录的时候，将受到这些参数的约束，从而达到统一管理各种用户会话连接的目的。
实体类型终端TTY（True Type Terminal）用户界面是用来管理和监控通过TTY方式登录的用户。TTY方式是指异步串口的登录方式，包括重定向登录方式和反向Telnet登录方式。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入TTY用户界面视图。
user-interface tty first-ui-number步骤3 配置与数据传输相关的属性。
● 配置TTY用户界面的传输速率。
speed speed-value

缺省情况下，传输速率为9600bit/s。
● 配置TTY用户界面的数据位。
databits bitsvalue缺省情况下，用户界面的数据位是8位。
● 配置TTY用户界面的校验位。
parity { even [ non-strip ] | none | odd [ non-strip ] }缺省情况下，校验位为none，即不进行校验。
● 配置TTY用户界面的停止位。
stopbits stopbits缺省情况下，停止位为1位。
----结束

#### 6.5.2 配置串口透传

前提条件在配置串口透传之前，需完成以下任务：
● 设备与RTU通过串口连接。
● 设备与服务器路由可达。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入TTY用户界面视图。
user-interface tty first-ui-number说明设备配置的与数据传输相关的属性与RTU保持一致。
步骤3 配置串口业务模式为RAW模式并进入RAW业务视图。
mode { none | raw }缺省情况下，串口业务模式为NONE。其中RAW模式表示透传模式，NONE模式表示无业务模式。
步骤4 关闭RAW业务功能。
undo raw-transport enable缺省情况下，RAW业务功能处于未使能状态。
说明在配置串口透传业务中设备的工作模式与串口透传业务的基本属性之前必须关闭RAW业务功能，否则配置不生效。
步骤 5 根据业务需求配置串口透传业务中设备的工作模式。
● 配置设备作为TCP服务器。
raw-transport tcp server server-port server-port server-ip server-ip [ client-ip client-ip ] [ vpn- instance vpn-instance-name ]

● 配置设备作为TCP客户端。
raw-transport tcp client server-port server-port server-ip server-ip [ vpn-instance vpn-instance-
name ]
● 配置设备作为UDP客户端。
raw-transport udp client server-port server-port server-ip server-ip
步骤6 （可选）配置串口透传业务的基本属性。
● 配置报文封装大小。
raw-transport packet-size size
缺省情况下，未配置报文封装大小，即设备对接收的报文不进行封装，按照报文
实际大小（不超过2000byte）发送出去。
● 配置报文封装定时器。
raw-transport packet-timer time
缺省情况下，报文封装定时时间为100毫秒。
● 开启特定字符筛选功能。
raw-transport special-char char-value
缺省情况下，特定字符筛选功能处于关闭状态。
● 开启Best effort模式，使缓存中的数据从旧的数据开始丢弃，先收到的数据先封
装。
raw-transport best-effort
缺省情况下，Best effort模式处于关闭状态，缓存中的数据从新的数据开始丢弃。
● 配置TCP连接的超时时间。
raw-transport tcp idle-timeout time
缺省情况下，TCP连接的超时时间为0分钟，表示不自动断开连接。
步骤7 （可选）配置UDP侦听源端口。用户想要实现该功能，需要配置设备作为UDP客户
端，此时才会使用指定端口进行UDP连接。
raw-transport udp client client-port port
缺省情况下，未配置UDP侦听源端口，即设备将使用随机端口进行UDP连接。
步骤8 开启RAW业务功能。
raw-transport enable
缺省情况下，RAW业务功能处于未使能状态。
开启RAW业务功能后，在RAW业务视图下配置的设备的工作模式及串口透传业务的基
本属性才会生效。
说明
● 执行本命令之后，会存在一定的安全风险，可能会导致设备接收/发送的报文在网络传输中被
攻击篡改，设备连接的客户端/服务端被仿冒等。
● 若串口透传报文在公网中传输且涉及敏感信息（口令、密钥、个人信息等），在管理控制
RTU设备时，建议在网络出口增加防火墙设备与远端服务器或与客户端建立加密通道来避免
报文篡改与仿冒攻击。
----结束
检查配置结果
● 执行命令display transport info，查看当前串口业务配置。
● 执行命令display transport mode，查看当前串口业务模式。

● 执行命令display transport session，查看当前串口会话信息。
● 执行命令display transport stat，查看当前串口状态信息。

### 6.6 维护串口透传

删除串口透传的配置信息表 6-4 删除串口透传的配置信息

| 操作 | 命令 |
|---|---|
| 在TTY用户界面视图下删除指定会话连接。 | kick-out session session-id |

### 6.7 举例：配置串口透传

组网需求如图1所示，电表作为RTU通过RS485串口连接至DeviceA，DeviceA与服务器路由可达。
RTU负责采集现场电力的实时数据，服务器需要对RTU的采集的数据进行监控与统一管理，以便及时掌握现场电力情况，可以通过配置RS485串口透传实现此目的。在此业务中，DeviceA作为TCP Server，接收服务器的连接请求，实现服务器与RTU的通信。
图 6-5 配置 DeviceA 作为 TCP Server 实现 RS485 串口透传组网图说明本例中interface1代表10GE1/0/1。
配置思路采用以下思路配置设备：
1. 通过Telnet等远程登录方式登录DeviceA。
2. 配置 DeviceA 接口 10GE1/0/1 的 IP 地址。
3. 配置静态路由，使DeviceA与服务器路由可达。
4. 开启DeviceA的RS485串口透传功能并配置DeviceA作为TCP Server。

操作步骤步骤1 配置DeviceA接口10GE1/0/1的IP地址。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 10 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] port link-type trunk [DeviceA-10GE1/0/1] port trunk allow-pass vlan 10 [DeviceA-10GE1/0/1] quit [DeviceA] interface vlanif 10 [DeviceA-vlanif10] ip address 10.1.1.1 255.255.255.0 [DeviceA-vlanif10] quit步骤2 配置静态路由，使DeviceA与服务器路由可达。
[DeviceA] ip route-static 10.2.1.1 255.255.255.0 vlanif 10步骤3 开启DeviceA的RS485串口透传功能并配置DeviceA作为TCP Server。
[DeviceA] user-interface tty 1 [DeviceA-ui-tty1] mode raw [DeviceA-ui-tty1-raw] undo raw-transport enable [DeviceA-ui-tty1-raw] raw-transport tcp server server-port 5000 server-ip 10.1.1.1 [DeviceA-ui-tty1-raw] raw-transport packet-size 255 [DeviceA-ui-tty1-raw] raw-transport packet-timer 60 [DeviceA-ui-tty1-raw] raw-transport enable [DeviceA-ui-tty1-raw] quit [DeviceA-ui-tty1] quit [DeviceA] quit <DeviceA> save步骤4 验证配置结果。
服务器能接收RTU采集的数据。
----结束配置脚本\# sysname DeviceA \# vlan batch 10 \# interface Vlanif10 ip address 10.1.1.1 255.255.255.0 \# interface 10ge 1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# ip route-static 10.2.1.1 255.255.255.0 Vlanif10 \# user-interface tty 1 mode raw raw-transport packet-size 255 raw-transport packet-timer 60 raw-transport tcp server server-port 5000 server-ip 10.1.1.1 raw-transport enable \# return
