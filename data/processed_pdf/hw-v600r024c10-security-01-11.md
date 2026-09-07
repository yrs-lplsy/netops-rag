# S1700, S5700, S6700 V600R024C10 配置指南-安全 01-11 PPPoE+配置

## 11 PPPoE+配置

### 11.1 PPPoE+简介

11.2 PPPoE+原理
11.3 PPPoE+配置注意事项
11.4 PPPoE+缺省配置
11.5 配置PPPoE+
11.6 PPPoE+配置举例
11.1 PPPoE+简介
定义
PPPoE+（Point-to-Point Protocol over Ethernet plus），又称PPPoE Intermediate
Agent，它部署在终端用户主机和宽带远程接入服务器BRAS（Broadband Remote
Access Server）之间的接入设备Device上，如下图所示。通过将终端用户主机接入的
端口信息（如槽位号/子卡号/接口号、VLAN、MAC地址等）通过PAD（PPPoE Active
Discovery ）报文上送给PPPoE Server，由PPPoE Server根据报文信息实现终端用户的
用户账号与接入端口的绑定认证，避免用户账号被盗用。
图 11-1 PPPoE+ 组网示意图

目的PPPoE是一种通过一个远端接入设备为以太网上的主机提供接入服务，并可以对接入的每个主机实现控制和计费的技术。PPPoE使用Client/Server模型，PPPoE Client向PPPoE Server发起连接请求，在两者会话协商过程中，PPPoE Server向PPPoE Client提供接入控制、认证等功能。
目前所使用的PPPoE具有较好的认证和安全机制，但仍然存在一些缺陷。比如PPPoE Server仅通过用户名和密码对接入用户进行认证，如果账号被盗，盗用者可以很容易的在其他地方通过该账号接入网络并通过PPPoE认证，进而实现盗用RADIUS服务。为了解决上述问题，引入了PPPoE+特性。

### 11.2 PPPoE+原理

PPPoE可分为三个阶段，即Discovery阶段、Session阶段和Terminate阶段。PPPoE+主要作用于Discovery阶段和Session阶段。PPPoE+的具体流程如图所示：
图 11-2 PPPoE+工作流程示意图
1. 终端用户主机（PPPoE Client）发起PPPoE请求，发送PADI（PPPoE Active Discovery Initial）报文。
2. Device截获PADI报文后把终端用户主机接入的端口信息（如槽位号/子卡号/接口号、VLAN、MAC地址等）以PPPoE+ Tag形式插入PADI报文里，再转发给BRAS（PPPoE Server）。
3. BRAS收到PADI+Tag以后，向终端用户主机回应PADO（PPPoE Active Discovery Offer）报文。
4. 终端用户主机收到PADO报文后，发送PADR（PPPoE Active Discovery Request）
报文。
5. Device截获PADR报文后把PPPoE+ Tag插入到PADR报文里，再转发给BRAS。

6. BRAS收到PADR+Tag以后，将产生一个唯一的会话ID（PPP Session ID），标识
和终端用户主机的这个会话，并向终端用户主机回应PADS（PPPoE Active
Discovery Session-confirmation）报文。如果没有发生错误，双方进入Session阶
段。
7. Session阶段内，终端用户主机和BRAS之间进行PPP协商和PPP报文传输。PPP协
商完成后，BRAS将PPPoE+ Tag封装在RADIUS报文的Radius NAS-Port-ID属性里
发送给RADIUS Server，RADIUS Server将根据该属性值对终端用户主机进行用户
账号与接入端口的绑定认证。
8. PPPoE会话建立后，PPPoE Client和PPPoE Server随时可以通过发送PADT
（PPPoE Active Discovery Terminate）报文的方式来结束PPPoE会话。

### 11.3 PPPoE+配置注意事项

License 依赖PPPoE+无需License许可即可使用。
硬件依赖表 11-1 支持本特性的硬件

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

| 系列 | 支持产品 |
|---|---|
| S6730-H-V2 | S6730-H24X6C-V2，S6730-H28X6CZ-V2，S6730- H48X6C-TV2，S6730-H48X6C-V2，S6730- H48X6CZ-V2，S6730-H48Y6C-TV2，S6730- H48Y6C-V2，S6730-H6FX4Y2CZ-V2 |
| S6750-S | S6750-S16X10Y2CZ，S6750-S16X8YZ，S6750- S24T16X8Y2CZ |
| S5735S-L3 | S5735S-L24P4S-A3，S5735S-L24P4XE-A3， S5735S-L24PN4XE-A3，S5735S-L24ST4X-A3， S5735S-L24T4S-QA3，S5735S-L24T4X-QA3， S5735S-L24T8J4XE-A3，S5735S-L48P4S-A3， S5735S-L48P4XE-A3，S5735S-L48PN4XE-A3， S5735S-L48S4X-A3，S5735S-L48T4S-A3，S5735S- L48T4XE-A3，S5735S-L8P4X-QA3，S5735S- L8T4X-QA3 |
| S5755-H | S5755-H24HB2Y2CZ，S5755-H24N4Y-A，S5755- H24P4Y2CZ，S5755-H24T4Y2CZ，S5755- H24U4Y2CZ，S5755-H24UM4Y2CZ，S5755- H24UN4Y2CZ，S5755-H24UTM4X4Y2C，S5755- H48N4Y-A，S5755-H48P4Y2CZ，S5755- H48T4Y2CZ，S5755-H48T4Y2CZ-B，S5755- H48U4Y2CZ，S5755-H48UM4Y2CZ，S5755- H48UN4Y2CZ，S5755-H48UTM4X4Y2C |
| S5735R-S-V2 | S5735R-S24P4X-V2，S5735R-S24T8J4X-XA-V2， S5735R-S48P4X-V2，S5735R-S48T4X-XA-V2 |
| S6780-H | S6780-H4Z |
| S5735E-L-V2 | S5735E-L16LP2UM2X-QA-V2，S5735E-L16LP2X- QA-V2，S5735E-L24P4S-A-V2，S5735E-L24P4XE- A-V2，S5735E-L24ST4XE-A-V2，S5735E- L24T4XE-A-V2，S5735E-L48LP4S-A-V2，S5735E- L48LP4XE-A-V2，S5735E-L48S4XE-A-V2， S5735E-L48T4XE-A-V2，S5735E-L8P4X-QA-V2， S5735E-L8T4X-QA-V2 |
| S5755-S | S5755-S24P8J8YZ，S5755-S24P8Y，S5755- S24T8J8YZ，S5755-S24T8Y，S5755-S24U8J8YZ， S5755-S24U8Y，S5755-S48P8Y，S5755- S48P8YZ，S5755-S48T8Y，S5755-S48T8YZ， S5755-S48U8Y，S5755-S48U8YZ |

| 系列 | 支持产品 |
|---|---|
| S5735R-L-V2 | S5735R-L16LP2S-QA-V2，S5735R-L16LP2UM2X- QA-V2，S5735R-L16LP2X-QA-V2，S5735R- L16T4S-A-V2，S5735R-L16T4X-QA-V2，S5735R- L24P4S-A-V2，S5735R-L24P4X-A-V2，S5735R- L24T4S-A-V2，S5735R-L24T4X-QA-V2，S5735R- L48LP4S-A-V2，S5735R-L48LP4X-A-V2，S5735R- L48P4X-A-V2，S5735R-L48T4S-A-V2，S5735R- L48T4X-A-V2，S5735R-L8P4S-A-V2，S5735R- L8P4X-QA-V2，S5735R-L8T4S-A-V2，S5735R- L8T4X-QA-V2 |
| S5735-L-V2 | S5735-L10T4X-A-V2，S5735-L14P2S-QA-V2， S5735-L16LP2UM2X-QA-V2，S5735-L16LP2X-QA- V2，S5735-L16P2UM2X-QA-V2，S5735-L16T4S- A-V2，S5735-L16T4X-QA-V2，S5735- L24LU8S4XE-QA-V2，S5735-L24P4S-A-V2， S5735-L24P4XE-A-V2，S5735-L24PN4XE-A-V2， S5735-L24ST4XE-A-V2，S5735-L24T4S-A-V2， S5735-L24T4X-QA-V2，S5735-L24T4XE-A-V2， S5735-L24T4XE-D-V2，S5735-L24T8J4XE-A-V2， S5735-L48LP4S-A-V2，S5735-L48LP4XE-A-V2， S5735-L48LPN4XE-A-V2，S5735-L48P4XE-A-V2， S5735-L48PN4XE-A-V2，S5735-L48S4X-A-V2， S5735-L48S4XE-A-V2，S5735-L48T4S-A-V2， S5735-L48T4XE-A-V2，S5735-L48T4XE-D-V2， S5735-L8P2T4X-A-V2，S5735-L8P4S-A-V2， S5735-L8P4X-QA-V2，S5735-L8T4S-A-V2， S5735-L8T4X-QA-V2 |
| S5735I-S-V2 | S5735I-S24T4XE-V2，S5735I-S24U4XE-V2， S5735I-S8T4SN-V2，S5735I-S8T4XN-V2，S5735I- S8U4XN-V2 |
| S5732-H-V2 | S5732-H24S4X6QZ-TV2，S5732-H24S4X6QZ- V2，S5732-H24UM4Y2CZ-KV2，S5732- H24UM4Y2CZ-V2，S5732-H44S4X6QZ-V2， S5732-H48UM4Y2CZ-KV2，S5732-H48UM4Y2CZ- TV2，S5732-H48UM4Y2CZ-V2 |

查询工具如需了解硬件规格、产品部件的配套关系，请点击硬件中心进行查询；如需了解关键规格、全量软件规格，请点击规格查询进行查询。
特性限制无

### 11.4 PPPoE+缺省配置

PPPoE+的缺省配置如表1示。
表 11-2 PPPoE+缺省配置

| 参数 | 缺省配置 |
|---|---|
| 全局PPPoE+功能 | 关闭 |
| 信任接口 | 所有接口为非信任接口 |
| 对用户侧PPPoE报文原有信息字段的处理方式 | replace |
| 在PPPoE报文中添加的信息字段格式和内容 | common格式的circuit-id和remote-id |
| 在PPPoE报文中添加的VENDOR ID值 | 2011 |
| 对服务器侧PPPoE回应报文原有信息字段的处理方式 | 不处理 |

### 11.5 配置PPPoE+

前提条件在配置PPPoE+之前，需要保证下行的Host和上行的PPPoE Server已完成PPPoE配置，可以成功进行PPPoE认证。
说明在PPPoE+配置完成后，设备会将用户侧的网络信息封装进用户侧上送的PPPoE报文，并用于PPPoE认证和RADIUS认证。当用户侧的网络配置发生变更时，如果未及时更新设备上的PPPoE +配置，有可能会导致PPPoE用户无法上线。

#### 11.5.1 开启PPPoE+功能

背景信息为了防止用户账号盗用现象，可以配置PPPoE+功能。开启全局PPPoE+功能是配置PPPoE+具体功能的前提条件。
操作步骤步骤1 进入系统视图。
system-view步骤2 开启全局PPPoE+功能。
pppoe intermediate-agent information enable

在系统视图下执行该命令后，所有接口都将开启PPPoE+功能。
缺省情况下，全局未开启PPPoE+功能。
----结束

#### 11.5.2 配置PPPoE+信任接口

背景信息设备与PPPoE Server相连的接口必须是信任接口，才可以防止PPPoE Server欺骗，并且防止PPPoE报文被转发至非PPPoE业务端口而遭到非法用户的获取。配置信任接口后，从PPPoE Client到PPPoE Server方向的PPPoE报文将只会由信任接口进行转发，同时也只有从信任接口收到的PPPoE报文才会被转发至PPPoE Client。
说明信任接口只对PPPoE Discovery阶段的协议报文进行控制，对于PPPoE Session阶段的业务报文不进行控制。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤3 配置接口为信任接口。
pppoe uplink-port trusted
----结束

#### 11.5.3 配置对用户侧PPPoE报文的处理方式

背景信息通过配置对用户侧PPPoE报文的处理方式，设备可以将终端用户主机接入的端口信息加入PPPoE报文中，实现终端用户的用户账号与接入端口的绑定认证，避免用户账号被盗用。
可在系统视图或接口视图下配置对用户侧 PPPoE 报文原有信息字段的处理方式，系统视图下的配置对所有接口都生效。如果希望在某个接口上采用其他处理方式，则可以在指定接口下进行配置，此时该接口对PPPoE报文的处理方式将以在该接口上所做的配置为准。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置对用户侧PPPoE报文原有信息字段的处理方式。
● 系统视图下配置全局对用户侧PPPoE报文原有信息字段的处理方式。
配置所有接口对PPPoE报文中原有信息字段的处理方式。
pppoe intermediate-agent information policy { drop | keep | replace }

缺省情况下，设备接口对收到的用户侧PPPoE报文中的信息字段采取replace方式。
说明
– drop：如果设备收到的报文包含Tags信息，剥掉PPPoE报文中原有的信息字段；如果设备收到的报文不包含Tags信息，不对PPPoE报文做处理。
– replace：如果设备收到的报文包含Tags信息，按照设定的字段格式对PPPoE报文中原有的信息字段进行替换；如果设备收到的报文不包含Tags信息，按照设定的字段格式在PPPoE报文中增加Tags信息。
– keep：如果设备收到的报文包含Tags信息，不对PPPoE报文做处理；如果设备收到的报文不包含Tags信息，按照设定的字段格式在PPPoE报文中增加Tags信息。
接口视图下配置对用户侧PPPoE报文原有信息字段的处理方式。
●
a. 进入接口视图。
interface interface-type interface-number
b. 配置指定接口对PPPoE报文中原有信息字段的处理方式。
pppoe intermediate-agent information policy { drop | keep | replace }
c. （可选）配置在PPPoE报文中添加的信息字段格式。
pppoe intermediate-agent information [ vlan vlan-id ] [ ce-vlan cevlan-id ] format { circuit- id | remote-id } { common | extend | user-defined text }缺省情况下，设备在PPPoE报文中添加的信息字段是格式为common的circuit-id和remote-id。
接口视图和系统视图下同时配置该命令时，接口视图下的配置优先生效。
d. 返回系统视图。
quit步骤3 （可选）当设备对用户侧PPPoE报文原有信息字段的处理方式为replace时，可配置用于替换原有PPPoE报文信息字段的字段格式和内容。
1. 配置在PPPoE报文中添加的信息字段内容。
pppoe intermediate-agent information encapsulation { circuit-id | remote-id } *
2. 配置在PPPoE报文中添加的信息字段格式。
pppoe intermediate-agent information format { circuit-id | remote-id } { common | extend | user- defined text }缺省情况下，设备在PPPoE报文中添加的信息字段是格式为common的circuit-id和remote-id。
步骤4 （可选）配置设备在PPPoE报文中添加的VENDOR ID值。
pppoe intermediate-agent information vendor-id vendor-id缺省情况下，设备在PPPoE报文中添加的VENDOR ID值为2011。
说明VENDOR ID用于标识厂商，使能PPPoE+功能后，设备必须通过含有VENDOR ID的PPPoE报文才能与PPPoE Server进行PPP协商。设备默认在PPPoE报文中添加值为2011的VENDOR ID。如果设备对接其他厂商的PPPoE Server，要求的VENDOR ID值是其他值时（例如3561），则可以通过命令pppoe intermediate-agent information vendor-id vendor-id进行修改。
----结束

#### 11.5.4 （可选）配置对服务器侧PPPoE报文的处理方式

背景信息通常情况下，设备不需要对服务器侧回应的PPPoE报文进行处理，直接透传报文给PPPoE Client即可。只有在PPPoE Client无法识别设备直接透传的PPPoE报文时，为了

保证PPPoE Client和PPPoE Server之间PPPoE会话的正常建立，设备才需要对服务器侧回应的PPPoE报文进行处理。具体处理方式如下：
● 当设备上配置的对PPPoE报文原有信息字段的处理方式为replace或keep时，
– 如果服务器侧回应的PPPoE报文不含信息字段，则设备直接透传PPPoE报文；
– 如果服务器侧回应的PPPoE报文中含有信息字段，且格式和内容与设备在用户侧PPPoE报文中添加的信息字段格式和内容一致，设备会将该PPPoE报文中的信息字段剥掉再进行转发，如果不一致，则设备直接透传PPPoE报文。
● 当设备上配置的对PPPoE报文原有信息字段的处理方式为drop时，设备直接透传PPPoE报文。
说明如果配置设备需要处理服务器侧的PPPoE回应报文，会使大量PPPoE用户并发上线的速度受到影响。
只有在全局使能了PPPoE+功能之后，对服务器侧PPPoE报文的处理方式配置才生效，而且如需修改此配置，必须先去使能PPPoE+功能才可以进行配置更改。
操作步骤步骤 1 进入系统视图。
system-view步骤2 配置设备处理服务器侧发送的PPPoE回应报文，直接对其进行透传。
pppoe intermediate-agent information ignore-reply disable缺省情况下，设备不处理服务器侧发送的PPPoE回应报文。
----结束

#### 11.5.5 检查配置结果

操作步骤步骤1 查看全局配置的circuit-id和remote-id格式信息。
display pppoe intermediate-agent information format步骤2 查看在PPPoE报文中添加的信息字段内容以及VENDOR ID值。
display pppoe intermediate-agent information encapsulation步骤3 查看全局配置的对用户侧和服务器侧PPPoE报文中原有信息字段的处理方式。
display pppoe intermediate-agent information policy步骤4 查看PPPoE+的配置信息。
display pppoe intermediate-agent information configuration
----结束

#### 11.5.6 常见配置错误

##### 11.5.6.1 配置PPPoE+后，PPPoE用户无法上线

故障现象配置了PPPoE+功能后，PPPoE用户无法上线。

常见原因本类故障的常见原因主要包括：
● 配置网络侧接口为非信任接口
● 配置对用户侧PPPoE报文原有信息字段的处理方式与业务需求不相符
● 配置在PPPoE报文中添加的信息字段格式与PPPoE服务器要求的格式不一致操作步骤步骤1 检查与PPPoE服务器连接的网络侧接口是否为信任接口。
如果网络侧接口不是信任接口，设备将会丢弃PPPoE报文，从而使合法PPPoE用户无法上线。
进入网络侧接口视图，执行命令display this，检查接口上是否配置了pppoe uplink- port trusted命令：
● 如果没有配置，则网络侧接口是非信任接口，请执行命令pppoe uplink-port trusted 配置。
● 如果已经配置，则网络侧接口是信任接口，请继续执行以下检查。
步骤2 检查针对用户侧PPPoE报文原有信息字段的处理方式是否与业务需求相符。
在系统视图以及PPPoE用户侧接口视图下分别执行命令display this，查看全局和接口上是否配置了pppoe intermediate-agent information policy命令。
● 如果接口和全局均配置了针对用户侧PPPoE报文原有信息字段的处理方式，则以接口下配置为准。
● 如果均没有配置，则设备缺省采用replace方式。
检查处理方式是否与业务需求相符：
● 如果不相符，请执行命令pppoe intermediate-agent information policy { drop | keep | replace }配置合适的处理方式。
● 如果相符，请继续执行以下检查。
步骤3 检查在PPPoE报文中添加的信息字段格式与PPPoE服务器要求的格式是否一致。
执行命令 display pppoe intermediate-agent information format 查看在 PPPoE 报文中添加的信息字段格式是否与PPPoE服务器要求的格式一致：
如果不一致，请执行命令pppoe intermediate-agent information [ vlan vlan-id ] [ ce-vlan cevlan-id ] format { circuit-id | remote-id } { common | extend | user- defined text }配置合适的信息字段格式。
----结束

### 11.6 PPPoE+配置举例

#### 11.6.1 举例：配置PPPoE+

组网需求如图11-3所示，Device上行连接BRAS设备，下行连接终端用户主机，BRAS内置PPPoE Server功能。网络中存在非法用户获取合法用户的PPPoE报文、盗用合法用户账号的现象，管理员希望能够为合法用户提供账号安全保障，避免用户账号被盗用。
图 11-3 配置 PPPoE+功能示例组网图配置思路采用如下思路在Device上配置PPPoE+功能：
1. 全局使能PPPoE+功能，实现终端用户的用户账号与接入端口的绑定认证，防止用户账号被盗用。
2. 配置Device与PPPoE Server连接的接口为信任接口，防止PPPoE报文被转发至非PPPoE业务端口而遭到非法用户的获取。
根据PPPoE Server对PPPoE报文信息字段格式的要求，配置Device对用户侧PPPoE
3.
报文中原有信息字段的处理方式，使Device能够与PPPoE Server正常通信。
操作步骤步骤1 使能PPPoE+功能。

<HUAWEI> system-view [HUAWEI] pppoe intermediate-agent information enable说明全局使能后，所有接口都将使能PPPoE+功能。
步骤2 配置接口为信任接口。
<HUAWEI> interface 10GE1/0/1 [HUAWEI-10GE1/0/1] pppoe uplink-port trusted [HUAWEI-10GE1/0/1] quit步骤3 配置所有接口对用户侧PPPoE报文中原有信息字段的处理方式为replace，使用Device的circuit-id和remote-id替换原有PPPoE报文中的信息字段。
[HUAWEI] pppoe intermediate-agent information policy replace步骤4 配置用于替换原有PPPoE报文信息字段的circuit-id的格式为extend。
[HUAWEI] pppoe intermediate-agent information format circuit-id extend步骤5 验证配置结果。
\# 执行命令display pppoe intermediate-agent information policy，查看对用户侧PPPoE 报文中原有信息字段的处理方式是否配置正确。
[HUAWEI] display pppoe intermediate-agent information policy The current information Policy :REPLACE The current ignore-reply Policy:ENABLE \# 执行命令display pppoe intermediate-agent information format，查看circuit- id格式信息是否配置正确。
[HUAWEI] display pppoe intermediate-agent information format The current information format :
Circuit ID : EXTEND Remote ID : COMMON For example:
interface 10GE1/0/1 SVLAN:200 CVLAN:100 The PPPOE Intermediate Agent information follow:
Circuit ID:00 04 00 c8 00 00 Remote ID:0025-9efb-494a
----结束配置文件Device的配置文件\# pppoe intermediate-agent information enable pppoe intermediate-agent information format circuit-id extend \# interface 10GE1/0/1 pppoe uplink-port trusted \# return
