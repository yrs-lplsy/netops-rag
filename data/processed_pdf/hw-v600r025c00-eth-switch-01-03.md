# S1700, S5700, S6700 V600R025C00 配置指南-以太网交换 01-03 Eth-Trunk配置

## 3 Eth-Trunk配置

### 3.1 Eth-Trunk简介

3.2 Eth-Trunk原理描述
3.3 Eth-Trunk配置注意事项
3.4 Eth-Trunk缺省配置
3.5 创建及配置Eth-Trunk接口
3.6 配置Eth-Trunk接口负载分担方式
3.7 配置Eth-Trunk接口手工1:1主备模式
3.8 配置Eth-Trunk的流量转发行为
3.9 配置Eth-Trunk二层子接口绑定BD
3.10 配置Eth-Trunk三层子接口
3.11 删除Eth-Trunk配置
3.12 维护Eth-Trunk
3.13 Eth-Trunk配置举例
3.14 Eth-Trunk常见配置错误
3.1 Eth-Trunk 简介
定义
Eth-Trunk又叫以太网链路聚合，它通过将多条以太网物理链路捆绑在一起成为一条逻
辑链路，从而实现增加链路带宽的目的。同时，这些捆绑在一起的链路通过相互间的
动态备份，可以有效地提高链路的可靠性。
目的
随着网络规模不断扩大，用户对骨干链路的带宽和可靠性提出越来越高的要求。在传
统技术中，常用更换高速率的单板或更换支持高速率单板的设备的方式来增加带宽，
但这种方案需要付出高额的费用，而且不够灵活。

Eth-Trunk采用链路聚合技术，可以在不进行硬件升级的条件下，通过将多个物理接口捆绑为一个逻辑接口，达到增加链路带宽的目的。在实现增大带宽目的的同时，Eth- Trunk采用备份链路的机制，可以有效的提高设备之间链路的可靠性。
Eth-Trunk主要有以下三个优势：
● 增加带宽链路聚合接口的最大带宽可以达到各成员接口带宽之和。
● 提高可靠性当某条活动链路出现故障时，流量可以切换到其他可用的成员链路上，从而提高链路聚合接口的可靠性。
● 负载分担在一个链路聚合组内，可以实现在各成员活动链路上的负载分担。

### 3.2 Eth-Trunk原理描述

#### 3.2.1 基本概念

如图3-1所示，DeviceA与DeviceB之间通过三条以太网物理链路相连，将这三条链路捆绑在一起，就成为了一条逻辑链路，这条逻辑链路的最大带宽等于原先三条以太网物理链路的带宽总和，从而达到了增加链路带宽的目的；同时，这三条以太网物理链路相互备份，当某条活动链路出现故障时，流量可以切换到其他可用的成员链路上，有效地提高了链路的可靠性。
图 3-1 Eth-Trunk 示意图下面介绍Eth-Trunk的一些基本概念。
链路聚合组和链路聚合接口如图3-2所示，链路聚合组LAG（Link Aggregation Group）是指将若干条以太链路捆绑在一起所形成的逻辑链路，也称为Eth-Trunk链路。
每个聚合组唯一对应着一个逻辑接口，这个逻辑接口称之为链路聚合接口或Eth-Trunk接口。Eth-Trunk接口可以作为普通的以太网接口来使用，实现各种路由协议以及其他业务。与普通以太网接口的差别在于：转发的时候链路聚合组需要从成员接口中选择一个或多个接口来进行数据转发。
成员接口和成员链路如图3-2所示，组成Eth-Trunk接口的各个物理接口称为成员接口。成员接口对应的链路称为成员链路。

图 3-2 链路聚合组与链路聚合接口、成员接口和成员链路的关系示意图活动接口和非活动接口、活动链路和非活动链路Eth-Trunk接口的成员接口存在活动接口和非活动接口两种。转发数据的接口称为活动接口，不转发数据的接口称为非活动接口。
活动接口对应的链路称为活动链路，非活动接口对应的链路称为非活动链路。
活动接口数上限阈值设置活动接口数上限阈值的目的是在保证带宽的情况下提高网络的可靠性。当活动接口数目达到上限阈值时，再向Eth-Trunk接口中添加成员接口，不会增加Eth-Trunk活动接口的数目，超过上限阈值的链路状态将被置为Down，作为备份链路。
例如，有8条无故障链路在一个Eth-Trunk接口内，每条链路都能提供1G的带宽，现在最多需要5G的带宽，那么上限阈值就可以设为5或者更大的值。其他的链路就自动进入备份状态以提高网络的可靠性。
手工模式链路聚合不支持活动接口数上限阈值的配置。
活动接口下限阈值设置活动接口数下限阈值是为了保证最小带宽，当活动链路数目小于下限阈值时，Eth-Trunk接口的状态转为Down。在多链路冗余场景下，可以通过设置活动接口数下限阈值，保证主链路带宽不够的情况下切换至备用链路。
链路聚合模式根据是否启用链路聚合控制协议LACP（Link Aggregation Control Protocol），链路聚合的模式分为手工模式和LACP模式，具体请参见3.2.3 手工模式Eth-Trunk和3.2.2 LACP 模式 Eth-Trunk 。

#### 3.2.2 LACP模式Eth-Trunk

LACP模式Eth-Trunk，Eth-Trunk的建立、成员接口的加入也需要手工配置，最大的区别就是链路聚合控制协议LACP的参与。
作为链路聚合技术，手工模式Eth-Trunk可以实现多个物理接口聚合成一个Eth-Trunk接口来提高带宽，同时能够检测到同一聚合组内的成员链路有断路等有限故障，但是无法检测到链路层故障、链路错连等故障。为了提高Eth-Trunk的容错性，同时能提供备份功能，保证成员链路的高可靠性，出现了链路聚合控制协议LACP（Link Aggregation Control Protocol ）。
LACP是基于IEEE 802.1AX标准的一种实现链路动态聚合与解聚合的协议，以供设备根据自身配置自动形成聚合链路并启动聚合链路收发数据，LACP模式就是采用LACP的一

种链路聚合模式。聚合链路形成以后，LACP负责维护链路状态，在聚合条件发生变化时，自动调整链路聚合。
如图3-3所示，DeviceA与DeviceB之间创建Eth-Trunk，需要将DeviceA上的四个接口与DeviceB捆绑成一个Eth-Trunk。由于错将DeviceA上的一个接口与DeviceC相连，这将会导致DeviceA向DeviceB传输数据时可能会将本应该发到DeviceB的数据发送到DeviceC上。而手工模式的Eth-Trunk不能及时检测到此故障。
如果在DeviceA和DeviceB上都启用LACP协议，经过协商后，Eth-Trunk就会选择正确连接的链路作为活动链路来转发数据，从而DeviceA发送的数据能够正确到达DeviceB。
图 3-3 Eth-Trunk 错连示意图LACP 模式下 Eth-Trunk 建立过程LACP通过链路聚合控制协议数据单元LACPDU（Link Aggregation Control Protocol Data Unit）与对端交互信息。在LACP模式的Eth-Trunk中加入成员接口后，这些接口将通过发送LACPDU向对端通告自己的系统优先级、MAC地址、接口优先级、接口号和操作Key（用来判断各接口相连对端是否在同一聚合组以及各接口带宽是否一致等）
等信息。对端接收到这些信息后，将这些信息与自身接口所保存的信息比较，用以选择能够聚合的接口，双方对哪些接口能够成为活动接口达成一致，确定活动链路。
LACP模式中，系统LACP优先级和接口LACP优先级是两个重要的参数，直接影响链路聚合主动端和活动接口的选择。
● 系统LACP优先级系统LACP优先级是为了区分两端设备优先级的高低而配置的参数。LACP模式下，两端设备所选择的活动接口必须保持一致，否则链路聚合组就无法建立。此时可以使其中一端具有更高的优先级，另一端根据高优先级的一端来选择活动接口即可。系统LACP优先级值越小优先级越高。
● 接口LACP优先级接口LACP优先级是为了区别同一个Eth-Trunk接口中的不同成员接口被选为活动接口的优先程度，优先级高的接口将优先被选为活动接口。接口LACP优先级值越小，优先级越高。
说明如果您想了解LACPDU报文的详细结构，可以使用报文格式查询工具。
LACP模式Eth-Trunk建立的过程如下：
1. 在LACP模式的Eth-Trunk中加入成员接口后，两端互相发送LACPDU报文。

如图3-4所示，在DeviceA和DeviceB上创建Eth-Trunk并配置为LACP模式，然后向Eth-Trunk中手工加入成员接口。此时成员接口上便启用了LACP协议，两端互发LACPDU报文。
图 3-4 LACP 模式 Eth-Trunk 互发 LACPDU
2. 确定主动端和活动链路。
如图3-5所示，两端设备均会收到对端发来的LACPDU报文。以DeviceB为例，当DeviceB收到DeviceA发送的报文时，DeviceB会查看并记录对端信息，然后比较系统优先级字段，如果DeviceA的系统优先级高于本端的系统优先级，则确定DeviceA为LACP主动端。如果DeviceA和DeviceB的系统优先级相同，比较两端设备的MAC地址，MAC地址小的一端为LACP主动端。
选出主动端后，两端都会以主动端的接口优先级来选择活动接口，如果主动端的接口优先级都相同则选择接口编号比较小的为活动接口。两端设备选择了一致的活动接口后，活动链路组便可以建立起来，这些活动链路以负载分担的方式转发数据。
图 3-5 LACP 模式确定主动端和活动链路的过程LACP 抢占如图 3-6 所示，接口 Port1 、 Port2 和 Port3 为 Eth-Trunk 的成员接口， DeviceA 为主动端，活动接口数上限阈值为2，三个接口的LACP优先级分别为10、20、30。当通过LACP协议协商完毕后，接口Port1和Port2因为优先级较高被选作活动接口，Port3成为备份接口。

图 3-6 LACP 抢占场景使能LACP抢占功能后，聚合组会始终保持高优先级的接口作为活动接口的状态。以下两种情况需要使能LACP抢占功能：
● Port1接口出现故障而后又恢复了正常。当接口Port1出现故障时被Port3所取代，如果Eth-Trunk接口未使能LACP抢占功能，则故障恢复时Port1将处于备份状态；
如果使能了LACP抢占功能，当Port1故障恢复时，由于接口优先级比Port3高，将重新成为活动接口，Port3再次成为备份接口。
如果希望Port3接口替换Port1、Port2中的一个接口成为活动接口，可以使能LACP
●抢占功能，并配置Port3的接口LACP优先级较高。如果没有使能LACP抢占功能，即使将备份接口的优先级调整为高于当前活动接口的优先级，系统也不会重新选择活动接口。
LACP 抢占延时抢占延时是LACP抢占发生时，处于备用状态的链路将会等待一段时间后再切换到转发状态。配置抢占延时是为了避免由于某些链路状态频繁变化而导致Eth-Trunk数据传输不稳定的情况。
如图3-6所示，Port1由于链路故障切换为非活动接口，此后该链路又恢复了正常。若系统使能了LACP抢占功能并配置了抢占延时，Port1重新切换回活动状态就需要经过抢占延时的时间。
活动链路与非活动链路切换LACP模式Eth-Trunk两端设备中任何一端检测到以下事件，都会触发聚合组的链路切换：
● 链路Down事件。
● LACP协议发现链路故障。
● 接口不可用。
● 在使能了LACP抢占功能的前提下，更改备份接口的优先级高于当前活动接口的优先级。
在以上故障场景中，可以按照如下步骤进行切换：
关闭故障链路。
1.
2. 从备份链路中选择优先级最高的链路接替活动链路中的故障链路。
3. 优先级最高的备份链路转为活动状态并转发数据，完成切换。

LACP 模式实现方式链路聚合协议LACP分为静态LACP模式和动态LACP模式，其特点如下。
静态LACP模式如图3-7所示，两台直接相连的设备都支持LACP协议，在两台设备上配置静态LACP模式Eth-Trunk接口，实现流量的负载分担与链路的冗余备份。静态LACP模式应用场景比较广泛，在向用户提供备份链路的同时，又提供一定的故障保护能力。当有一条链路出现故障时，系统能够自动选择一条优先级最高的可用备份链路变为活动链路。
图 静态 模式 接口示意图3-7 LACP Eth-Trunk动态LACP模式静态LACP模式和动态LACP模式在LACP协议交互方面没有区别，区别在于两种模式在LACP协商失败后的处理不一致：
● 静态LACP模式下，LACP协商失败后Eth-Trunk变为Down，不能转发数据。
● 动态LACP模式下，LACP协商失败后Eth-Trunk变为Down，但其成员接口继承Eth- Trunk的VLAN属性状态变为Indep，可独立进行二层数据转发。
当部署动态LACP模式Eth-Trunk接口的设备能够收到对端的LACP协议报文时，两端设备将通过LACP协议报文进行聚合参数协商。协商成功后的聚合链路功能与两端都配置为静态LACP模式Eth-Trunk接口的链路一样。
动态LACP模式下的Eth-Trunk通常应用于设备和服务器直连的场景，如图3-8所示，服务器A需要通过DeviceA从文件服务器B获取配置文件。
● 当服务器A重启后为空配置时，LACP协商失败，此时动态LACP协议可保证服务器A通过Eth-Trunk成员接口从文件服务器B获取到配置文件。
● 当DeviceA收到服务器A的LACP协议报文时，服务器A和DeviceA将通过LACP协议报文进行聚合参数协商。
图 3-8 动态 LACP 模式 Eth-Trunk 接口示意图说明动态LACP模式Eth-Trunk仅用于华为公司设备与服务器互连的场景。其他场景下，建议部署静态LACP模式Eth-Trunk，如果部署动态LACP，则网络会有成环风险。

#### 3.2.3 手工模式Eth-Trunk

手工模式Eth-Trunk，Eth-Trunk的建立、成员接口的加入由手工配置，没有链路聚合控制协议LACP的参与。如果某条活动链路故障，链路聚合组自动在剩余的活动链路中平均分担流量。当需要在两个直连设备之间提供一个较大的链路带宽，而其中一端或两端设备都不支持LACP协议时，可以配置手工模式Eth-Trunk。
如图3-9所示，DeviceA与DeviceB之间创建Eth-Trunk，手工模式下三条活动链路都参与数据转发并分担流量。当一条链路故障时，故障链路无法转发数据，链路聚合组自动在剩余的两条活动链路中分担流量。
图 3-9 手工模式 Eth-Trunk

#### 3.2.4 手工1:1主备模式Eth-Trunk

说明该配置仅S6730-H-V2、S6730E-H-V2、S6730-S-V2系列支持。
随着网络中部署业务的日渐增多，对于业务的可靠性要求也越来越高。可以在两端设备上创建手工1:1主备模式Eth-Trunk接口，加入两个成员接口并指定主接口，为数据传输提供1:1链路备份。手工1:1主备模式通常应用在两端或其中一端设备不支持LACP协议的情况下。
手工1:1主备模式下，Eth-Trunk接口的创建、成员接口的加入都需要手工配置完成，并且成员接口是否处于活动状态也完全由手工配置决定。
如图3-10所示，在DeviceA、DeviceB上配置手工1:1主备模式Eth-Trunk接口，为数据传输提供1:1链路备份。
图 3-10 手工 1:1 主备模式组网图缺省情况下，先加入1:1主备模式Eth-Trunk接口的成员口将成为主接口，主接口处于活动状态，可以转发数据，而备份接口处于非活动状态，不能转发数据。当主接口故障时，备份接口切换为活动状态，转发数据。

#### 3.2.5 链路聚合模式对比

手工模式Eth-Trunk、手工1:1主备模式Eth-Trunk和LACP模式Eth-Trunk的区别如表3-1所示。
表 3-1 链路聚合模式比较

| 维度 | 手工模式 | LACP模式 | 手工1:1主备模式 |
|---|---|---|---|
| Eth-Trunk 的建立方式 | Eth-Trunk接口的创建、成员接口的加入由手工配置，没有链路聚合控制协议的参与。 | Eth-Trunk接口的创建、成员接口的加入由手工配置，LACP协议参与链路动态调整，负责链路状态维护。在聚合条件发生变化时，自动调整或解散链路聚合。 | Eth-Trunk接口的创建、成员接口的加入都需要手工配置完成，并且成员接口是否处于活动状态也完全由手工配置决定。 |
| 设备是否需要支持 LACP协议 | 不需要 | 需要 | 不需要 |
| 数据转发 | 正常情况下，所有链路都是活动链路。所有活动链路均参与数据转发。如果某条活动链路故障，链路聚合组自动在剩余的活动链路中分担流量。 | 正常情况下，部分链路是活动链路。所有活动链路均参与数据转发。如果某条活动链路故障，链路聚合组自动在非活动链路中选择一条链路作为活动链路，参与数据转发的链路数目不变。 | 正常情况下，Eth- Trunk接口中的主接口处理活动状态，可以转发数据，而备份接口处于非活动状态，不能转发数据。当主接口故障时，备份接口处于活动状态，转发数据。 |
| 检测故障 | 只能检测到同一聚合组内的成员链路有断路等故障，无法检测到链路断连、错连等故障。 | 不仅能够检测到同一聚合组内的成员链路有断路等故障，还可以检测到链路故障、链路错连等故障。 | 只能检测到同一聚合组内的成员链路有断路等故障，无法检测到链路断连、错连等故障。 |

### 3.3 Eth-Trunk配置注意事项

License 依赖Eth-Trunk无需License许可即可使用。
硬件依赖表 3-2 支持本特性的硬件

| 系列 | 支持产品 |
|---|---|
| S6750-H | S6750-H36C，S6750-H48X8C，S6750-H48Y8C |

| 系列 | 支持产品 |
|---|---|
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
| S5735S-L3 | S5735S-L24P4S-A3，S5735S-L24P4XE-A3， S5735S-L24PN4XE-A3，S5735S-L24ST4X-A3， S5735S-L24T4S-QA3，S5735S-L24T4X-QA3， S5735S-L24T8J4XE-A3，S5735S-L48P4S-A3， S5735S-L48P4XE-A3，S5735S-L48PN4XE-A3， S5735S-L48S4X-A3，S5735S-L48T4S-A3，S5735S- L48T4XE-A3，S5735S-L8P4X-QA3，S5735S- L8T4X-QA3 |

| 系列 | 支持产品 |
|---|---|
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

特性限制表 3-3 本特性的使用限制

| 特性 | 特性限制 |
|---|---|
| Eth- Trunk基础功能 | 对于S6750-H系列，S6730E-H-V2系列，S6750E-S系列，S6730-S-V2 系列，S5755-H系列，S6780-H系列，S5732-H-V2系列，S6730-H-V2 系列，S5755-S系列，S6750-S系列：如果本端为堆叠设备，且对端配置超时模式为fast，本端发生主备倒换时，对端LACP可能会超时震荡。建议此场景下两端配置超时模式为slow。 |
| Eth- Trunk基础功能 | Eth-Trunk接口的各成员口默认权重为1，可以对权重进行配置调节，此调节会引起Trunk口转发行为的改变，权重越大的成员口被哈希的机会也越大，成员口的权重之和不能大于Trunk支持的最大成员口数目。 |
| Eth- Trunk基础功能 | 静态LACP模式的Eth-Trunk在1：N场景下，状态为Up的Eth-Trunk接口成员链路数的上限阈值设置为1。在主用链路状态变为Down，备用链路切换为主用链路之前，原主用链路状态Down先不上报给Eth-Trunk，满足如下任一条件，原主用链路状态Down才会上报给Eth-Trunk，避免因 Eth-Trunk接口变为Down引起整网路由重新计算。 1、延时报Down定时器60秒超时。 2、备用链路故障状态无法变为Up。 |
| Eth- Trunk基础功能 | 对于Eth-trunk的成员端口故障恢复后打印告警的功能： 1、只有成员口故障恢复（Down到Up）后满足Trunk内所有成员口状态都Up才发送Trap。 2、Trap发送支持三秒抑制。 |
| Eth- Trunk基础功能 | 修改物理接口加入Eth-Trunk时，可能发生广播流量多包或丢包问题。 |
| Eth- Trunk基础功能 | 内层报文为VXLAN报文时，只对基于IP报文的负载分担生效，对于非IP 报文（比如MAC-IN-MAC类型的报文），hash模板中的IP相关字段填0 进行hash。对于内层报文的Tag超过2层的报文，芯片无法解析，也无法hash。非2的整次幂成员个数，选路天然不均，成员端口数量越多问题越明显。 |
| Eth- Trunk基础功能 | 对于产品S6780-H系列，S6750-H48X8C，S6750-H48Y8C：未知单播和广播流量在eth-trunk hash-mode为1/2/4/5/6算法时，小范围变化的情况下，无法负载分担。 |
| Eth- Trunk基础功能 | Shutdown Eth-Trunk的成员链路时广播流量可能少量多包或丢包。 |

| 特性 | 特性限制 |
|---|---|
| Eth- Trunk基础功能 | BUM流会先复制到所有Eth-Trunk成员口，然后再对不需要发送流量的成员口进行剪枝，这会占用实际成员口的转发带宽，导致实际的转发能力小于预期，此时设备内部会对此剪枝进行带宽补偿，但补偿能力有限（不同的字节补偿能力不同）。举例说明，比如4个GE入口（100% BUM流量），出口为一个Eth-Trunk口（其有两个成员口），预期出口带宽可达到90%以上，实际带宽在65%左右（256字节，如果没有补偿，则出口带宽只有50%，在该示例情况下，额外补偿了15%的带宽）。不同的字节下出口带宽如下： 128字节：70% 148字节：69% 256字节：65% 512字节：62% 1024字节：61% |
| Eth- Trunk基础功能 | 修改Eth-Trunk成员口为独立物理接口时，可能发生广播流量多包或丢包问题。 |
| Eth- Trunk基础功能 | Eth-Trunk的成员链路故障恢复时流量回切可能少量多包或丢包。 |
| Eth- Trunk基础功能 | 对于S6750-H系列，S6730E-H-V2系列，S6750E-S系列，S6730-S-V2 系列，S6780-H系列，S5732-H-V2系列，S6730-H-V2系列，S6750-S 系列：配置tunnel inner-header/tunnel inner-header outer-header时，L2TP 报文源目的端口号不参与hash，tunnel-id和session-id参与hash。 |
| Eth- Trunk基础功能 | 对于S6750-H系列，S6780-H系列，S5755-S系列：配置弹性负载分担，eth-trunk hash-mode id配置为10、11、12算法时，可能无法负载分担。建议参考产品手册中命令行eth-trunk hash- mode的建议算法配置。 |
| Eth- Trunk基础功能 | Eth-Trunk扩容时，由于两端设备处理成员口加入操作存在时间差，成员口直接加入可能存在丢包。 |

### 3.4 Eth-Trunk缺省配置

表 3-4 Eth-Trunk 参数缺省值

| 参数 | 缺省值 |
|---|---|
| 链路聚合模式 | 手工模式 |
| 系统LACP优先级 | 32768 |

| 参数 | 缺省值 |
|---|---|
| 接口LACP优先级 | 32768 |
| LACP抢占 | 去使能 |

### 3.5 创建及配置Eth-Trunk接口

#### 3.5.1 创建Eth-Trunk接口并配置链路聚合模式

前提条件在配置Eth-Trunk之前，需完成以下任务：
连接接口，使接口的物理层状态为Up。
背景信息手工模式Eth-Trunk适用于对端设备不支持LACP协议的场景；动态LACP模式Eth-Trunk仅用于华为公司设备与服务器互连的场景；其他场景下，建议部署静态LACP模式Eth- Trunk，如果部署动态LACP，则网络会有成环风险。
如果用户希望利用单一设备集中管理和维护整个网络设备的Eth-Trunk配置，可以配置Eth-Trunk自协商功能，具体操作请参见：网络助手配置（WebMaster方案）-> 配置网络助手 ->（可选）配置Eth-Trunk自协商。该功能仅支持静态LACP模式Eth-Trunk。
操作步骤步骤1 进入系统视图。
system-view步骤2 创建Eth-Trunk接口并进入Eth-Trunk接口视图。
interface eth-trunk trunk-id步骤 3 （可选） 将 Eth-Trunk 接口切换为二层模式或三层模式，请根据当前接口模式自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-S-V2、S6750-S、S6750E-S、S6730-H-V2、S6730E- H-V2、S5755-H、S5755-S、S5732-H-V2系列支持该步骤。
切换为二层模式：
portswitch切换成三层模式：
undo portswitch

#### 3.5.2 向Eth-Trunk接口中加入成员接口

说明
● Eth-Trunk接口支持二层Eth-Trunk接口和三层Eth-Trunk接口：当需要将Eth-Trunk接口加入VLAN或进行二层转发时，需要配置二层Eth-Trunk接口，此时Eth-Trunk接口的三层功能和标识被禁止，并将采用系统MAC地址；当需要通过Eth-Trunk接口承载三层数据报文时，需要配置三层Eth-Trunk接口，此时可以在Eth-Trunk接口上配置IP地址，MAC地址及MTU值等。
● Eth-Trunk接口的二三层模式不影响成员接口的加入，成员接口既可以加入二层Eth-Trunk，也可以加入三层Eth-Trunk。
步骤4 配置链路聚合模式。
mode { manual load-balance | lacp-static | lacp-dynamic }缺省情况下，链路聚合模式为manual load-balance。
manual load-balance表示手工模式Eth-Trunk，该模式下所有链路都参与负载分担；
lacp-static表示静态LACP模式Eth-Trunk，lacp-dynamic表示动态LACP模式Eth- Trunk。
步骤5 （可选）去使能Eth-Trunk的静态LACP稳定优选功能。
lacp stable-preferred disable缺省情况下，使能Eth-Trunk的静态LACP稳定优选功能。
说明该功能仅在配置为静态LACP模式的Eth-Trunk生效。
----结束向 接口中加入成员接口
3.5.2 Eth-Trunk背景信息向Eth-Trunk接口中加入成员接口有两种方式：
● 在Eth-Trunk接口视图下添加具体的成员接口，分为批量添加和单个添加两种方式。
● 在需要加入Eth-Trunk的接口视图下将该接口加入相应的Eth-Trunk接口。
链路聚合前需要了解的注意事项
● 成员接口加入 Eth-Trunk 时，必须为缺省的接口类型，成员接口不能配置某些业务（如静态MAC地址，由于各接口支持的业务范围不一致，故无法列举全部不能配置的业务类型，具体参见设备报错提示），如果配置设备会报错。
● Eth-Trunk链路两端相连的物理接口的数量、速率、双工方式、流控配置必须一致。
● Eth-Trunk链路两端相连的物理接口的jumbo（超大帧长度）建议配置为一致。
● 如果本端设备接口加入了Eth-Trunk，与该接口直连的对端接口也必须加入Eth- Trunk，两端才能正常通信。
● 两台设备对接时需要保证两端设备上链路聚合的模式一致。
● 链路聚合可以聚合不同速率、不同双工模式的成员接口；且成员接口可以同时包含光口和电口。
● Eth-Trunk接口不能嵌套，即成员接口不能是Eth-Trunk接口。

● LACP模式Eth-Trunk可以聚合不同单板、不同速率及不同双工模式的成员接口。
但是不同速率的成员接口不能同时处于转发状态，半双工模式的成员接口无法转
发。请在配置前检查成员接口所在单板、接口速率以及双工模式。
说明
在添加成员接口后，如果对Eth-Trunk接口执行命令shutdown，Eth-Trunk接口的物理状态为
Administratively DOWN，则成员接口的配置文件会自动显示shutdown，且物理状态也变为
Administratively DOWN。
操作步骤
● 在Eth-Trunk接口视图下向Eth-Trunk中添加成员接口
a. 进入系统视图。
system-view
b. 进入Eth-Trunk接口视图。
interface eth-trunk trunk-id
c. 执行以下两种方法之一进行成员接口的添加：
▪
批量添加成员接口。
trunkport interface-type { interface-number1 [ to interface-number2 ] } &<1-16>
▪
添加单个成员接口。
trunkport interface-type interface-number
● 在成员接口视图下向Eth-Trunk中添加成员接口
a. 进入系统视图。
system-view
b. 进入要捆绑到此Eth-Trunk接口的成员接口的接口视图。
interface interface-type interface-number
c. 将当前接口加入Eth-Trunk接口。
eth-trunk trunk-id
----结束
后续处理
当在设备本端和对端配置完3.5.1 创建Eth-Trunk接口并配置链路聚合模式和3.5.2 向
Eth-Trunk 接口中加入成员接口， Eth-Trunk 功能即可正常使用，可以继续在 Eth-Trunk
接口上配置相关业务。如果需要调整Eth-Trunk的状态参数，可以参考3.5.4 （可选）
配置手工模式Eth-Trunk参数或3.5.5 （可选）配置LACP模式Eth-Trunk参数。
链路聚合后需要了解的注意事项
● 一个以太网接口只能加入到一个Eth-Trunk接口，如果需要加入其他Eth-Trunk接
口，必须先退出原来的Eth-Trunk接口。
● 当成员接口加入Eth-Trunk后，学习MAC地址或ARP地址时是按照Eth-Trunk来学
习的，而不是按照成员接口来学习。
● Eth-Trunk成员接口退出Eth-Trunk接口或者物理接口加入Eth-Trunk接口时，建议
先把成员接口/物理接口shutdown，退出/加入Eth-Trunk后再undo shutdown。
● 删除Eth-Trunk接口时需要先删除Eth-Trunk接口中的所有成员接口。

#### 3.5.3 （可选）配置Eth-Trunk成员接口权重值

背景信息在一个Eth-Trunk接口中，通过对各成员链路配置不同的权重值，可以实现流量负载分担。某成员接口的权重值占所有成员接口权重之和的比例越大，该成员链路承担的负载就越大。因此，如果需要提高某个成员接口承担的负载能力，可以通过配置该功能来提高此成员接口的权重。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入Eth-Trunk成员接口视图。
interface interface-type interface-number步骤3 配置成员接口的权重值。
distribute-weight weight-value缺省情况下，成员接口的权重为1。
对于一个Eth-Trunk接口，其所有成员接口权重之和不能大于支持的最大成员接口数。
----结束

#### 3.5.4 （可选）配置手工模式Eth-Trunk参数

##### 3.5.4.1 配置Eth-Trunk接口活动接口数的下限阈值

背景信息设置活动接口数下限阈值是为了保证最小带宽，当活动链路数目小于下限阈值时，Eth-Trunk接口的状态转为Down。请根据实际网络规划来确定是否配置该值，非多链路冗余组网场景，建议使用缺省值。缺省情况下，活动接口数下限阈值为1。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入Eth-Trunk接口视图。
interface eth-trunk trunk-id步骤3 配置Eth-Trunk接口中活动接口数下限阈值。
least active-linknumber link-number本端和对端设备的活动接口数下限阈值可以不同。如果下限阈值不同，以下限阈值数值较大的一端为准。
---- 结束

#### 3.5.5 （可选）配置LACP模式Eth-Trunk参数

##### 3.5.5.1 配置影响LACP主动端选择的参数

背景信息对于LACP模式的Eth-Trunk接口，通过LACP系统优先级区分Eth-Trunk两端设备的优先级高低，优先级高的设备将作为LACP主动端。当Eth-Trunk接口两端的LACP系统优先级相同时，可以配置LACP系统ID，通过LACP系统ID决策两端设备优先级的高低，从而确定LACP主动端。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置当前设备的LACP系统优先级。
lacp priority priority设备的系统LACP优先级值越小优先级越高。
步骤 3 进入 Eth-Trunk 接口视图。
interface eth-trunk trunk-id步骤4 配置Eth-Trunk接口的LACP系统ID。
lacp system-id mac-address缺省情况下，Eth-Trunk接口的LACP系统ID为系统桥MAC。系统桥MAC可以通过display bridge mac-address命令查看。
LACP系统ID值越小的优先级越高。
----结束

##### 3.5.5.2 配置影响活动链路选择的参数

背景信息缺省情况下，LACP主动端确定后，另一端将按照LACP主动端的接口优先级及接口编号选择活动接口，从而实现两端设备活动接口的选择达成一致。在实际使用中，用户可以根据需求调整影响活动链路选择的参数。
● Eth-Trunk 接口选择活动接口的方式：如果 Eth-Trunk 接口中成员接口拥有不同的速率，若依据接口优先级来选择活动接口，可能会选中速率低的成员接口。如果用户希望选中接口速率高的成员接口，可以依据接口速率选择活动接口。
● 不同速率的接口可转发数据报文：在LACP模式下，不同速率的以太网接口可以加入同一个Eth-Trunk接口。当不同速率的接口加入同一个LACP模式Eth-Trunk后，为了使加入的成员接口都能被选中转发流量，可以开启不同速率的接口均可转发数据报文的功能。
● Eth-Trunk接口中活动接口数的上限和下限阈值：为保证Eth-Trunk接口的状态和带宽，可以设置活动接口数的阈值，以减小成员链路的状态变化带来的影响。
– 设置活动接口数下限阈值是为了保证最小带宽，当活动链路数目小于下限阈值时，Eth-Trunk接口的状态转为Down。请根据实际网络规划来确定是否配置该值，非多链路冗余组网场景，建议使用缺省值。缺省情况下，活动接口数下限阈值为1。

– 设置活动接口数上限阈值是在保证带宽的情况下提高网络的可靠性，当活动
链路数达到上限阈值时，再向Eth-Trunk中添加成员接口，不会增加Eth-
Trunk活动接口的数目，超过上限阈值的链路状态将被置为Down，作为备份
链路。
● Eth-Trunk接口接收LACP协议报文的超时时间：如果对端Eth-Trunk某个成员接口
发生自环或其他故障，而本端Eth-Trunk不能及时感知对端成员接口状态的变化
（缺省情况下，本端接收LACP协议报文的超时时间是90秒），此时必然造成数据
流量丢失。为了保证数据流量可靠的传输到对端，可以修改Eth-Trunk接口接收
LACP协议报文的超时时间。如果本端成员接口在设置的超时时间内未收到对端发
送的LACP协议报文，本端成员接口状态立即变为Down，不再转发数据。
● Eth-Trunk接口LACP抢占功能：当活动链路中出现故障链路时，系统会从备用链
路中选择优先级最高的链路替代故障链路；如果被替代的故障链路恢复了正常，
同时该链路的优先级又高于替代自己的链路，在缺省关闭抢占功能的情况下，系
统不会重新选择活动接口，故障恢复后的链路将作为备用链接。如果开启了LACP
抢占功能，高优先级链路会抢占低优先级链路，回切到活动状态。
● 成员接口LACP优先级：缺省情况下，主动端的接口LACP优先级是相同的，此时
会按照接口编号来确定活动接口，接口编号小的会被选择为活动接口。如果用户
希望指定活动接口，可以修改接口LACP优先级。
操作步骤
步骤1 进入系统视图。
system-view
步骤2 进入Eth-Trunk接口视图。
interface eth-trunk trunk-id
步骤3 在Eth-Trunk接口视图下，根据实际需要选择配置影响活动链路的参数。
表 3-5 Eth-Trunk 接口视图下，配置影响活动链路的参数

| 操作 | 命令 | 说明 |
|---|---|---|
| 配置Eth-Trunk接口选择活动接口的方式 | lacp select { priority | speed } | priority表示依据接口优先级选择活动接口。接口优先级配置请参见配置成员接口的LACP优先级。 speed表示依据接口速率选择活动接口。为保证Eth-Trunk正常工作，建议Eth-Trunk接口两端配置相同的活动接口选择方式。 |

| 操作 | 命令 | 说明 |
|---|---|---|
| 开启不同速率的接口可转发数据报文功能 | lacp mixed-rate link enable | 当Eth-Trunk接口中存在不同速率的成员接口时，活动接口的选择仍是按照主动端设备的接口优先级、端口ID，选择活动接口。如果希望指定端口成为活动端口，可以配置成员接口的LACP优先级提高接口优先级。 |
| 配置Eth-Trunk接口中活动接口数上限阈值 | lacp max active- linknumber link-number | 为保证Eth-Trunk链路状态不震荡，建议在同一条 Eth-Trunk链路两端的Eth- Trunk接口上配置相同的上限阈值。否则在原来选中的链路全部切换时，可能导致未配置的一端Eth- Trunk链路状态震荡。 |
| 配置Eth-Trunk接口中活动接口数下限阈值 | least active-linknumber link-number | 本端和对端设备的活动接口数下限阈值可以不同。如果下限阈值不同，以下限阈值数值较大的一端为准。 |
| 配置Eth-Trunk接口接收 LACP协议报文的超时时间 | lacp timeout fast [ user-defined user- defined ] | 缺省情况下，本地接收报文的超时时间是90秒（slow），对端发送LACP 报文的周期是30秒。如果配置为fast，本地接收报文的超时时间是3秒，对端发送LACP报文的周期是1秒；如果配置为fast user-defined user- defined，可以自定义本地接收报文的超时时间。两端配置的超时时间可以不一致。但为了便于维护，建议用户配置一致的 LACP协议报文超时时间。 |

| 操作 | 命令 | 说明 |
|---|---|---|
| 配置Eth-Trunk接口的 LACP抢占功能 | lacp preempt enable | 开启Eth-Trunk接口的 LACP抢占功能。开启该功能后，缺省抢占等待时间是30秒。在进行LACP抢占时，系统将根据主动端接口的优先级进行抢占。为保证Eth-Trunk正常工作，要求Eth-Trunk接口两端统一配置LACP抢占开启或关闭。 |
|  | lacp preempt delay delay-time | 配置LACP抢占等待时间。如果未配置该命令，系统会按照缺省抢占等待时间 30秒来执行抢占操作。当链路两端设备配置的抢占等待时间不一致时，以等待时间最长的作为实际抢占等待时间。 |

步骤4 返回系统视图，进入Eth-Trunk成员接口视图。
quit interface interface-type interface-number步骤5 配置成员接口的LACP优先级。根据实际需要进行配置。
lacp priority priority接口LACP优先级反映了接口成为活动接口的优先程度，接口LACP优先级的值越小优先级越高。如果接口优先级相同，则选择接口编号比较小的成为活动接口。
----结束

##### 3.5.5.3 配置Eth-Trunk接口震荡抑制功能

背景信息Eth-Trunk接口震荡抑制功能主要包括接口状态震荡抑制功能和非法MAC报文抑制功能。
● 在Eth-Trunk接口的状态频繁震荡、接收报文频繁变化等震荡场景下，会导致LACP协议的协商状态跟着频繁震荡，从而影响Eth-Trunk接口的正常使用，此时可以使能LACP模式下的Eth-Trunk接口状态震荡抑制功能。
● 当LACP模式的Eth-Trunk接口协商成功时，端口会保存最近收到的报文的源MAC地址，并启动MAC地址检查，当收到的报文携带的MAC地址与保存的MAC地址不一致时，可能会因为重新协商导致 Eth-Trunk 接口状态振荡，为避免该情况，设备默认使能非法MAC报文抑制功能，当接口收到和有效源MAC不一致的报文时，会将错误报文直接丢弃，并记录错误报文。如果不需要对报文中的源MAC地址进行检查时，可以去使能该功能。

操作步骤步骤1 进入系统视图。
system-view步骤2 进入Eth-Trunk接口视图。
interface eth-trunk trunk-id步骤3 根据实际需求选择如下配置。
● 配置Eth-Trunk接口状态震荡抑制功能。
lacp dampening state-flapping缺省情况下，Eth-Trunk接口状态震荡抑制功能未使能。
● 配置Eth-Trunk接口接收非法MAC报文抑制功能。
undo lacp dampening unexpected-mac disable缺省情况下，Eth-Trunk接口接收非法MAC报文抑制功能已使能。
----结束

##### 3.5.5.4 配置与服务器对接场景下Eth-Trunk成员接口强制Up功能

背景信息服务器与设备对接时，如果设备与服务器直连的接口加入静态LACP模式的Eth-Trunk，当服务器重启或刚上线时，Eth-Trunk接口接收LACP协议报文超时后，Eth-Trunk成员接口的状态会变为Down。这时可以通过配置Eth-Trunk成员接口强制Up，使该接口继续转发业务流量。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入Eth-Trunk成员接口视图。
interface interface-type interface-number步骤3 配置Eth-Trunk成员接口强制UP功能。
lacp force-up [ extension ]缺省情况下，成员接口未配置强制UP。
如果指定extension参数，则强制UP功能在配置后只生效一次，以防止在服务器端口错连或者误退出场景下，造成流量丢失。如果后续接口状态出现从DOWN到UP的变化，强制UP功能会再次生效。
配置该功能后，只有当Eth-Trunk接口为静态LACP模式，且所有的成员接口接收LACP协议报文超时的场景下，接口配置的force-up状态才会生效。
Eth-Trunk所有成员接口的force-up状态生效时，通过least active-linknumber link- number 命令配置的 Eth-Trunk 接口中活动接口数下限阈值会生效，但是通过 lacp max active-linknumber link-number命令配置的上限阈值将不再生效。
----结束

##### 3.5.5.5 配置与其他厂商设备对接的参数

背景信息设备与其他厂商设备对接的可配置参数包括如下几个方面，请根据实际场景需要进行选择配置。
● 忽略接收到的LACP协议报文中的Reserved字段的取值：华为设备之间的对接，如果两端设备配置的抢占等待时间不一致，两端设备会通过LACP协议报文中Reserved字段进行协商，系统会选择抢占等待时间较长的时间为等待时间。华为设备和其他厂商设备对接时，如果其他厂商对LACP协议报文中Reserved字段定义和华为不一致，则会导致LACP协议震荡，造成业务中断。这种场景下，可以使能设备忽略LACP协议报文中的Reserved字段的取值。
● 配置LACP协议报文中的CollectorMaxDelay字段取值：其他厂商设备通过静态LACP模式的Eth-Trunk双归接入两台华为设备，如果这两台华为设备的系统软件不一致，可能会出现发送的LACP协议报文中CollectorMaxDelay字段缺省值不同的情况，这将导致其他厂商设备同一个Eth-Trunk接口内成员接口收到携带CollectorMaxDelay值不同的LACP协议报文。而对于有些厂商在这种情况下会出现CPU占用率升高，影响设备性能。为了解决这一问题，可在其中一台华为设备上修改 CollectorMaxDelay 字段取值，保证两台华为设备发送的 LACP 协议报文中CollectorMaxDelay字段值一致。
● 配置Eth-Trunk接口的成员接口在LACP中的Key值：设备作为PE双归与其他厂家设备对接时，当其他厂家设备不支持E-Trunk对接，需要手工配置两台PE具有相同的系统ID、系统优先级和Portkey，以保证两侧PE链路均能选中。
操作步骤
● 配置与其他厂商设备对接时，忽略接收到的LACP协议报文中的Reserved字段的取值。
a. 进入系统视图。
system-view
b. 开启设备忽略接收到的LACP协议报文中的Reserved字段的取值的功能。
lacp ignore aggregation delay缺省情况下，设备识别接收到的LACP协议报文中的Reserved字段取值。
● 配置与其他厂商设备对接时，LACP协议报文中的CollectorMaxDelay字段取值。
a. 进入系统视图。
system-view
b. 进入 Eth-Trunk 接口视图。
interface eth-trunk trunk-id
c. 配置LACP协议报文中的CollectorMaxDelay字段取值。
lacp collector delay delay-time
● 配置与其他厂商设备对接时，Eth-Trunk接口的成员接口在LACP中的Key值。
a. 进入系统视图。
system-view
b. 进入Eth-Trunk接口视图。
interface eth-trunk trunk-id
c. 配置 Eth-Trunk 接口的成员接口在 LACP 中的 Key 值。
lacp portkey portkey
----结束

##### 3.5.5.6 配置跨设备Eth-Trunk场景下成员接口编号增加32768

背景信息如图3-11所示，DeviceB和DeviceC上创建相同的Eth-Trunk ID、LACP系统ID、系统LACP优先级，以及不同的Eth-Trunk成员接口编号，就可以使跨设备的Eth-Trunk接口协商成功。两台设备不分主备，都参与数据的转发，平均分担流量，并且当一台设备故障时，流量可以通过另外一台设备转发，从而实现设备级保护。
在该组网中，DeviceB和DeviceC需要是L3网关角色，不能是二层透传设备。因为如果网关部署在更上一级的设备，则网关设备上学习到的下游设备的ARP/ND表项就会产生两个出口，出现MAC漂移现象，所以下游设备以跨设备Eth-Trunk方式接入的设备必须是组网部署中的L3网关角色。
图 3-11 LACP 模式跨设备 Eth-Trunk 组网图DeviceA跨设备接入DeviceB和DeviceC时，为了保证LACP可以协商成功，DeviceB和DeviceC上Eth-Trunk接口的以下参数需要保证一致：
● 执行命令lacp priority priority，配置相同的系统LACP优先级。
● 执行命令lacp system-id mac-address，配置相同的LACP系统ID。
● 执行命令 interface eth-trunk trunk-id ，配置相同的 Eth-Trunk ID 。
● 配置相同的端口速率。如果成员接口的速率不同，执行命令lacp mixed-rate link enable，开启不同速率的接口加入Eth-Trunk接口后可转发数据报文的功能。
除此之外，还需要保证DeviceB和DeviceC上Eth-Trunk成员接口的编号不同，通过配置成员接口编号扩展功能，使其中一台设备的Eth-Trunk成员接口编号增加32768。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入Eth-Trunk接口视图。
interface eth-trunk trunk-id

步骤3 配置其中一台设备的Eth-Trunk成员接口编号增加32768。
lacp port-id-extension enable
----结束

#### 3.5.6 检查配置结果

操作步骤
● 执行命令display eth-trunk [ trunk-id [ interface interface-type interface- number | verbose ] | brief ]，查看Eth-Trunk的配置信息。
● 执行命令display eth-trunk membership trunk-id，查看Eth-Trunk的成员接口信息。
----结束

### 3.6 配置Eth-Trunk接口负载分担方式

#### 3.6.1 了解Eth-Trunk接口负载分担

Eth-Trunk接口支持静态负载分担方式。
静态负载分担方式在使用Eth-Trunk转发数据时，由于Eth-Trunk接口两端设备之间有多条物理链路，可能会产生同一数据流的第一个数据帧在一条物理链路上传输，而第二个数据帧在另外一条物理链路上传输的情况。这样一来同一数据流的第二个数据帧就有可能比第一个数据帧先到达对端设备，从而产生接收数据包乱序的情况。
为了避免这种情况的发生，Eth-Trunk采用逐流负载分担的机制，这种机制把数据帧中的地址通过HASH算法生成HASH-KEY值，然后根据这个数值在Eth-Trunk转发表中寻找对应的出接口，不同的MAC或IP地址HASH得出的HASH-KEY值不同，从而出接口也就不同，这样既保证了同一数据流的帧在同一条物理链路转发，又实现了流量在聚合组内各物理链路上的负载分担，即逐流的负载分担。
逐流负载分担下的数据流转发机制如图3-12所示，Eth-Trunk位于MAC与LLC子层之间，属于数据链路层。
图 3-12 Eth-Trunk 接口在以太网协议栈的位置Eth-Trunk 模块内部维护一张转发表，这张表由以下两项组成。
● HASH-KEY值HASH-KEY值是根据数据帧的MAC地址或IP地址等，经HASH算法计算得出。

● 接口号
Eth-Trunk转发表表项分布和设备每个Eth-Trunk支持加入的成员接口数量相关，
不同的HASH-KEY值对应不同的出接口。
例如，某设备每Eth-Trunk支持最大加入接口数为8个，将接口1、2、3、4捆绑为
一个Eth-Trunk接口，此时生成的转发表如图3-13所示。其中HASH-KEY值为0、
1、2、3、4、5、6、7，对应的出接口号分别为1、2、3、4、1、2、3、4。
图 3-13 Eth-Trunk 转发表示例
Eth-Trunk模块根据转发表转发数据帧的过程如下：
Eth-Trunk模块从MAC子层接收到一个数据帧后，根据负载分担方式提取数据帧的
1.
源MAC地址/IP地址或目的MAC地址/IP地址。
2. 根据HASH算法进行计算，得到HASH-KEY值。
3. Eth-Trunk 模块根据 HASH-KEY 值在转发表中查找对应的接口，把数据帧从该接口
发送出去。
负载分担方式的选择
逐流负载分担基于数据流的属性，如源MAC地址、目的MAC地址、源IP地址、目的IP
地址、TCP/UDP的源端口号或TCP/UDP的目的端口号来分担负载。用户可以根据流量
模型设置基于不同属性的负载分担方式，流量中某个参数变化越频繁，选择对应负载
分担方式的流量就越均衡。例如，在网络中，如果报文的IP地址变化较频繁，那么选
择基于目的IP地址、源IP地址或源IP和目的IP地址的负载分担模式更有利于流量在各物
理链路间合理的负载分担；如果报文的MAC地址变化较频繁，IP地址比较固定，那么
选择基于目的MAC地址、源MAC地址或源MAC和目的MAC地址的负载分担模式更有利
于流量在各物理链路间合理的负载分担。
例如，DeviceA的一条TCP报文流的源IP地址为192.168.1.1（MAC地址：a-a-a，源端
口号：50），目的IP地址为172.16.1.1（MAC地址：b-b-b，目的端口号：2000），另
一条TCP报文流的源IP地址为192.168.1.1（MAC地址：a-a-a，源端口号：60），目的
IP地址为10.1.1.1（MAC地址：c-c-c，目的端口号：2000）。如果在DeviceA上配置基
于报文的源MAC地址进行负载分担，则报文出接口仅有1个；如果在DeviceA上配置基
于报文的目的IP地址进行负载分担，则报文出接口有两个，去往不同目的IP的报文会从
不同的出接口转发。
配置负载分担方式时，请注意：
● 负载分担方式只在流量的出接口上生效，如果发现各入接口的流量不均衡，请修
改上行出接口的负载分担方式。
● 尽量将数据流通过负载分担在所有活动链路上传输，避免数据流仅在一条链路上
传输，造成流量拥堵，影响业务正常运行。
例如，数据报文的目的MAC和IP地址只有一个，则应选择根据报文的源MAC和IP
地址进行负载分担，如果选择根据报文的目的MAC和IP地址进行负载分担则会造
成流量只在一条链路上传输，造成流量拥堵。

#### 3.6.2 配置静态负载分担方式

背景信息设备已为各类型报文指定了缺省的静态负载分担方式，如果网络中流量负载分担均衡，则无需调整负载分担方式。如果流量负载分担失衡，则可以根据流量模型设置基于不同属性的负载分担方式。配置静态负载分担方式有两种方法：
● 配置全局增强负载分担模板，在模板中指定各类型报文的负载分担方式，对全局生效。
● 直接在Eth-Trunk接口下指定各类型报文的负载分担方式，仅对当前Eth-Trunk接口生效。
已知单播和未知单播的负载分担方式的生效机制是不同的：
● 对于已知单播，两种方式下均可配置报文的负载分担方式和HASH算法，具体生效规则如下：
– 报文的负载分担方式：当Eth-Trunk接口下各报文的负载分担方式均为缺省配置时，以全局增强负载分担模板中的配置生效；当Eth-Trunk接口下报文的负载分担方式存在非缺省配置时（例如只修改了二层报文的负载分担方式），则所有类型的报文的负载分担方式均以Eth-Trunk接口下的配置生效。
– HASH算法：当Eth-Trunk接口下为缺省配置时，以全局增强负载分担模板中的配置生效；当Eth-Trunk接口下修改了缺省配置，则以Eth-Trunk接口下的配置生效。
● 对于未知单播，仅全局增强负载分担模板下的配置生效。
由于负载分担只对出方向的流量有效，因此链路两端接口的负载分担模式可以不一致，两端互不影响。负载分担方式的配置，与报文类别有关，与报文的转发流程无关。系统会识别以太帧携带的三层报文类别，比如报文被识别为IP报文，此时即使只做L2转发，依然会选择IP报文对应的负载分担方式进行负载分担。当报文无法识别为IP报文或MPLS报文时，系统才基于L2报文的负载分担方式进行负载分担。
操作步骤
● 配置基于全局增强负载分担模板的负载分担方式
a. 进入系统视图。
system-view
b. 创建静态负载分担模板并进入静态负载分担模板视图，或进入已存在的静态负载分担模板视图。
load-balance profile profile-name设备支持一个负载分担模板，默认的负载分担模板是default。当新创建负载分担模板时，会覆盖原有的负载分担模板。
c. 对于不同类型的报文分别配置负载分担方式，以下步骤可不选、选择其一或多选，请根据网络转发报文的实际情况选择。
▪配置指定负载分担模板中IP报文负载分担方式。
对于S5735-S-V2，S5735-L-V2，S5735I-S-V2，S5735E-S-V2，S5735E- L-V2，S5735I-L-V2，S5735I-H-V2，S1730S-S3，S5735S-L3，S5735S- S3，S5735R-L-V2，S5735R-S-V2，配置IPv4和IPv6报文负载分担方式：
ip [ src-ip | dst-ip | protocol | l4-src-port | l4-dst-port | src-mac | dst-mac | flowlabel |
* src-interface | eth-type | innervlan | outervlan ]缺省情况下，IP报文负载分担方式为src-ip、dst-ip、l4-src-port、l4-dst- port。 flowlabel仅对IPv6报文生效。

对于S5755-S，配置IPv4和IPv6报文负载分担方式：
ip [ src-ip | dst-ip | protocol | l4-src-port | l4-dst-port | src-mac | dst-mac | flowlabel | src-interface | session-id ] *缺省情况下，IP报文负载分担方式为session-id、src-ip、dst-ip、l4-src- port、l4-dst-port。 flowlabel仅对IPv6报文生效。
对于S6780-H、S6750-H，配置IPv4和IPv6报文负载分担方式：
ip [ src-ip | dst-ip | protocol | l4-src-port | l4-dst-port | src-mac | dst-mac | flowlabel | src-interface | dest-qp | session-id ] *缺省情况下，IP报文负载分担方式为session-id、dest-qp、src-ip、dst- ip、l4-src-port、l4-dst-port。 flowlabel仅对IPv6报文生效。
对于S5732-H-V2、S6730E-H-V2、S6730-S-V2、S6730-H-V2、S5755-
H、S6750E-S、S6750-S系列：
○ 配置IPv4报文负载分担方式：
ip [ src-ip | dst-ip | protocol | l4-src-port | l4-dst-port ] *缺省情况下，IPv4报文负载分担方式为src-ip、dst-ip、l4-src-port、l4-dst-port。
○ 配置IPv6报文负载分担方式：
ipv6 [ protocol | src-ip | dst-ip | l4-src-port | l4-dst-port | flowlabel ] *缺省情况下， IPv6 报文的负载分担方式为 src-ip 、 dst-ip 、 l4-src- port、l4-dst-port。
▪配置指定负载分担模板中MPLS报文负载分担方式。
mpls [ src-ip | dst-ip | top-label | 2nd-label | 3rd-label | src-interface | l4-src-port | l4- dst-port | protocol | vlan | src-mac | dst-mac | fourth-label | fifth-label ] *缺省情况下，MPLS报文负载分担方式为top-label、2nd-label。
该配置仅S6780-H、S6750-H、S6730-S-V2、S6750-S、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S5732-H-V2系列支持。
src-mac、dst-mac、fourth-label、fifth-label参数仅S6750-H、S6780-H、S5755-S上支持。
vlan参数在S6780-H、S6750-H、S5755-S上不支持。
▪配置指定负载分担模板中二层报文的负载分担方式。
l2 [ src-mac | dst-mac | src-interface | eth-type | vlan | innervlan | outervlan ] *缺省情况下，二层报文的负载分担方式为src-mac、dst-mac。
缺省情况下，对于S6750-H、S6780-H、S5755-S、S5735R-S-V2，二层报文的负载分担方式为src-mac、dst-mac、vlan。
innervlan、outervlan参数仅S5735E-L-V2、S5735-L-V2、S5735E-S- V2、S5735-S-V2、S5735I-S-V2、S5735I-L-V2、S5735I-H-V2、S5735S-L3、S1730S-S3，S5735S-S3、S5735R-L-V2、S5735R-S-V2产品支持。
vlan参数仅S6780-H、S6750-H、S6730-S-V2、S6750-S、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S5732-H-V2系列支持。
d. 配置负载分担模板中隧道类（比如GRE、VXLAN）报文匹配外层或内层字段参与 HASH 计算。
对于S5755-S：
tunnel { inner-header | outer-header }

对于S6780-H、S6750-H、S6750E-S、S6750-S、S6730E-H-V2、S6730-S- V2、S6730-H-V2、S5755-H、S5732-H-V2系列：
tunnel { inner-header | outer-header } *缺省情况下，隧道类报文采用outer-header，即匹配外层字段参与HASH计算。
该配置仅S6780-H、S6750-H、S6730-S-V2、S6750-S、S6750E-S、S6730- H-V2、S6730E-H-V2、S5755-H、S5755-S、S5732-H-V2系列支持。
e. 配置负载分担模板中MAC-in-MAC报文匹配外层报文头或内层报文头参与HASH计算。
mac-in-mac { outer-header | inner-header }缺省情况下，MAC-in-MAC报文匹配外层报文头参与HASH计算。
该配置仅S6750-H、S6780-H支持。
f. 配置指定负载分担模板中负载分担HASH算法计算结果的偏移量。
eth-trunk universal-id universal-id hash-mode hash-mode-id缺省情况下，负载分担 HASH 算法计算结果的偏移量为 1 。
universal-id参数仅S5732-H-V2、S6730-H-V2、S5755-H、S6750-S、S6750E-S、S6730E-H-V2、S6730-S-V2系列支持。
hash-mode参数仅S5735E-L-V2，S5735-L-V2，S5735E-S-V2，S5735-S- V2，S5735I-S-V2，S5735I-L-V2，S5735I-H-V2，S6750-H，S5735S-L3，S1730S-S3，S5735S-S3，S5735R-L-V2，S6780-H，S5735R-S-V2，S5755- S产品支持。
配置基于Eth-Trunk接口的负载分担方式
●该配置仅S6750E-S、S6750-S、S6730E-H-V2、S6730-S-V2、S6730-H-V2、S5755-H、S5732-H-V2系列支持。
a. 进入系统视图。
system-view
b. 进入Eth-Trunk接口视图。
interface eth-trunk trunk-id
c. 配置IP报文的负载分担方式。
load-balance { dst-ip | src-ip | src-dst-ip | dst-mac | src-mac | src-dst-mac | round-robin | enhanced profile profile-name }缺省情况下，Eth-Trunk接口的负载分担模式为src-dst-ip配置enhanced profile参数时，该表示该Eth-Trunk接口将使用load- balance profile命令所设置全局负载分担模板中的配置。
d. 配置Eth-Trunk接口弹性HASH功能。
load-balance enhanced resilient缺省情况下，弹性HASH功能未配置。
弹性HASH是指在链路增加或减少时，尽量少的切换链路上的流量，只有部分流量进行链路切换。例如，一个 Eth-Trunk 接口中包含 3 条成员链路，当一条链路故障无法转发数据时，未配置弹性HASH的情况下另外两条链路会重新分配流量。如果配置了弹性HASH，另外两条链路上之前分配的流量不会发生变化，只是将故障链路上的流量大致均匀地分配到这两条链路上，这样对业务

造成的影响较小。当故障链路恢复后，会从这两条链路卸载一部分流量到故障恢复的链路上，但各链路的流量分配和故障前流量分配不会完全一致。
----结束检查配置结果
● 执行命令display eth-trunk [ trunk-id [ verbose ] ]，通过Hash Arithmetic字段查看Eth-Trunk接口的负载分担方式。
● 执行命令display load-balance profile [ profile-name ]，查看指定负载分担模板的详细信息。
后续处理
● 输入包含指定五元组信息以及源MAC地址、目的MAC地址的报文后，模拟计算报文的出接口。
display load-balance forwarding-path unicast interface eth-trunk trunk-id src-interface interface-type interface-number { ethtype ethtype-number | vlan vlan-id | [ [ src-ip src-ip-data | dst-ip dst-ip-data ] * | [ src-ipv6 src-ipv6-
* data | dst-ipv6 dst-ipv6-data ] ] | src-mac src-mac-data | dst-mac dst-mac- data | protocol { protocol-number | icmp | igmp | ip | ospf | tcp [ l4-src-port
* src-port-data | l4-dst-port dst-port-data ] | udp [ l4-src-port src-port-data | l4-dst-port dst-port-data ] * } } * slot slot-id
● 查看包含指定五元组信息以及源MAC地址、目的MAC地址的报文的出接口（查询报文的出接口需要有流量经过时才会有查询结果）。
display port forwarding-path { src-ip src-ip-data [ ip-mask-len | source-ip- mask ] | dst-ip dst-ip-data [ ip-mask-len | dst-ip-mask ] | src-mac src-mac- data | dst-mac dst-mac-data | protocol { protocol-number | gre | icmp | igmp | ip | ipinip | ospf | tcp [ l4-src-port src-port-data | l4-dst-port dst-port-data ]
* | udp [ l4-src-port src-port-data | l4-dst-port dst-port-data ] * } } *该命令仅S6780-H、S6750-H、S6730-S-V2、S6750-S、S6750E-S、S6730-H- V2、S6730E-H-V2、S5755-H、S5755-S、S5732-H-V2系列支持。

### 3.7 配置Eth-Trunk接口手工1:1主备模式

说明该配置仅S6730-H-V2、S6730E-H-V2、S6730-S-V2系列支持。

#### 3.7.1 创建手工1:1主备模式Eth-Trunk

前提条件在配置手工1:1主备模式Eth-Trunk接口之前，需要完成以下任务：
连接接口并配置接口的物理参数，使接口的物理层状态为Up。

背景信息随着网络中部署业务的日渐增多，对于业务的可靠性要求也越来越高。可以在组成Eth-Trunk链路的两端设备上创建1:1主备模式Eth-Trunk接口，为数据传输提供1:1链路备份。
如图3-14所示，在两台直接相连的设备上配置1:1主备模式Eth-Trunk接口，为数据传输提供1:1链路备份。
图 3-14 手工 1:1 主备模式 Eth-Trunk 接口示意图操作步骤步骤 1 进入系统视图。
system-view步骤2 创建Eth-Trunk接口并进入Eth-Trunk接口视图。
interface eth-trunk trunk-id步骤3 配置当前Eth-Trunk工作模式为手工1:1主备模式。
mode manual backup缺省情况下，Eth-Trunk的工作模式为手工负载分担模式。
----结束

#### 3.7.2 向Eth-Trunk接口中加入成员接口

背景信息向Eth-Trunk接口中添加成员接口分为两种方式：
● 在Eth-Trunk接口视图下添加具体的成员接口，分为批量添加和单个添加两种方式。
● 在成员接口视图下，将该接口加入相应的Eth-Trunk接口。将成员接口加入Eth- Trunk接口时，需要注意以下问题：
– Eth-Trunk接口不能嵌套，即成员接口不能是Eth-Trunk接口。
– 不同的以太网接口可以加入同一个Eth-Trunk接口。
说明物理接口加入Eth-Trunk接口后会受到如下影响：
● 在添加成员接口后，如果对Eth-Trunk接口执行命令shutdown，Eth-Trunk接口的物理状态为 Administratively DOWN ，则成员接口的配置文件会自动显示 shutdown ，且物理状态也变为Administratively DOWN。
● 在添加成员接口后，如果对Eth-Trunk接口执行命令undo shutdown，则成员接口的配置文件会自动显示undo shutdown。

操作步骤
● 在Eth-Trunk接口视图下
a. 进入系统视图。
system-view
b. 进入Eth-Trunk接口视图。
interface eth-trunk trunk-id
c. 执行以下两种方法之一进行成员接口的添加：
▪批量添加成员接口。
trunkport interface-type { interface-number1 [ to interface-number2 ] } & <1-16>手工1:1主备模式Eth-Trunk接口一次批量操作最多只能添加或删除两个成员接口。
▪添加单个成员接口。
trunkport interface-type interface-number
● 在成员接口视图下
a. 进入系统视图。
system-view
b. 进入要捆绑到此Eth-Trunk的成员接口的接口视图。
interface interface-type interface-number
c. 将当前接口加入Eth-Trunk。
eth-trunk trunk-id说明
● 成员接口不能有IP地址等三层配置项，也不可以配置任何业务。
● 成员接口不能配置静态MAC地址。
● 一个以太网接口只能加入到一个Eth-Trunk接口，如果需要加入其他Eth-Trunk接口，必须先退出原来的Eth-Trunk接口。
● 如果成员口的PST（Port State Table）状态为Down，该成员口不会作为Eth- trunk的出接口转发报文。
----结束后续处理当 Eth-Trunk 成员口的状态由 Up 变为 Down 或由 Down 变为 Up 时，需要将成员口的状态变化信息通过Trap告知用户，以便用户确认是否是设备的故障导致。

#### 3.7.3 （可选）指定Eth-Trunk成员接口中的主接口

背景信息正常情况下，1:1主备模式Eth-Trunk接口中的主接口处于活动状态，可以转发数据。
而备份接口处于非活动状态，不能转发数据。如果需要更改当前的备份接口为主接口可通过如下方法实现：
● 在原主接口对应的接口视图下执行命令undo port-master取消主接口配置，再在原备份接口对应的接口视图下执行命令port-master重新指定主接口。重新指定主接口时会产生短暂的数据中断。

操作步骤步骤1 进入系统视图。
system-view步骤2 进入成员接口。
interface interface-type interface-number步骤3 指定该成员接口为主接口。
port-master缺省情况下，先加入1:1主备模式Eth-Trunk接口的成员口将成为主接口。
在两个成员接口中，只可以配置一个主接口。
----结束

#### 3.7.4 检查配置结果

操作步骤
● 执行命令display eth-trunk [ trunk-id [ interface interface-type interface- number ] ]，查看手工1∶1主备模式Eth-Trunk接口配置信息、活动接口信息。
● 执行命令display eth-trunk membershiptrunk-id，查看Eth-Trunk的成员接口。
----结束

### 3.8 配置Eth-Trunk的流量转发行为

#### 3.8.1 配置Eth-Trunk接口流量本地优先转发

背景信息在设备集群/堆叠场景中，为了保证流量的可靠传输，流量的出接口设置为Eth-Trunk接口，那么Eth-Trunk接口中必定存在跨框成员口。当集群/堆叠设备转发流量时，Eth- Trunk接口通过HASH算法可能会选择跨框的成员口。由于集群/堆叠设备间线缆带宽有限，跨框转发流量增加了集群/堆叠设备之间的带宽承载压力，同时也降低了流量转发效率。为了解决这个问题，可以使能 Eth-Trunk 接口流量本地优先转发功能。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入Eth-Trunk接口视图。
interface eth-trunk trunk-id步骤 3 配置 Eth-Trunk 接口流量本地优先转发功能。
undo local-preference disable缺省情况下，已开启Eth-Trunk接口流量本地优先转发功能。

说明
● 开启Eth-Trunk接口流量本地优先转发功能，必须确保本设备Eth-Trunk接口出接口的带宽足以承载本设备转发的流量，防止发生丢包。
● 流量本地优先转发功能只对已知单播有效，对广播、组播和未知单播均不生效。
----结束

#### 3.8.2 配置LACP未选中成员口入方向的报文丢弃

背景信息如图3-15所示，DeviceA配置Eth-Trunk LACP模式，DeviceB的一个接口配置为Eth- Trunk LACP模式，另一个接口是普通物理口，这几个接口在同一个广播域中。由于该场景中LACP未选中接口属性继承Eth-Trunk接口，而报文上送后STP不会阻塞Eth- Trunk成员口，因此流量会继续转发，可能存在成环的风险。
图 3-15 LACP 模式 Eth-Trunk 示意图操作步骤步骤1 进入系统视图。
system-view步骤2 开启未选中成员口入方向的报文丢弃功能。
undo lacp unselected-member discard input-packet disable缺省情况下，已开启未选中成员口入方向的报文丢弃功能。
----结束

### 3.9 配置Eth-Trunk二层子接口绑定BD

前提条件在创建Eth-Trunk的二层子接口前，已创建对应的Eth-Trunk接口。该Eth-Trunk接口下成员接口的加入没有配置顺序要求，可以在二层子接口创建之后再进行。
背景信息当设备通过二层Eth-Trunk接口接入二层网络，可以为不同的Eth-Trunk二层子接口配置相同的BD，以实现在不同的Eth-Trunk二层子接口之间来往报文的二层转发。
说明该配置仅S6780-H、S6750-H、S6730-S-V2、S6750-S、S6750E-S、S6730-H-V2、S6730E-H- V2、S5755-H、S5755-S、S5732-H-V2系列支持。

操作步骤步骤1 进入系统视图。
system-view步骤2 进入Eth-Trunk接口视图。
interface eth-trunk trunk-id步骤3 配置Eth-Trunk接口为二层模式，并返回至系统视图。
portswitch quit步骤4 创建Bridge-domain。
bridge-domain bd-id步骤5 进入需要创建二层子接口的主接口视图。
interface interface-type interface-number步骤6 配置接口的链路类型为trunk，hybrid或access。
port link-type { trunk | hybrid | access }步骤 7 创建 Eth-Trunk 接口的二层子接口，并进入 Eth-Trunk 二层子接口视图。
interface eth-trunk trunk-id.subnumber mode l2 subnumber是Eth-Trunk二层子接口的编号。
步骤8 配置Eth-Trunk二层子接口绑定BD。
bridge-domain bd-id
----结束后续处理Eth-Trunk二层子接口创建完成后，可以在该子接口下配置流封装、流动作等相关业务，同时可以通过display trunk-id.subnumber命令查看Eth- interface eth-trunk Trunk子接口的状态信息。

### 3.10 配置Eth-Trunk三层子接口

前提条件在创建 Eth-Trunk 三层子接口前，已创建对应的 Eth-Trunk 接口。该 Eth-Trunk 接口下成员接口的加入没有配置顺序要求，可以在三层子接口创建之后再进行。
背景信息设备支持在三层Eth-Trunk接口上配置三层子接口。当三层设备通过三层Eth-Trunk接口接入二层网络设备且二层网络设备的端口划分到不同的VLAN中时，为了实现三层Eth-Trunk接口可以正确识别不同的VLAN报文，从而保证不同VLAN间的用户可以正常通信，需要在三层设备与二层设备相连的Eth-Trunk接口上创建三层子接口与下游用户的VLAN分别对应。
说明该配置仅S6780-H、S6750-H、S6730-S-V2、S6750-S、S6750E-S、S6730-H-V2、S6730E-H- V2、S5755-H、S5755-S、S5732-H-V2系列支持。

操作步骤步骤1 进入系统视图。
system-view步骤2 进入Eth-Trunk接口视图。
interface eth-trunk trunk-id步骤3 配置Eth-Trunk接口为三层模式，并返回至系统视图。
undo portswitch quit步骤4 创建Eth-Trunk接口的三层子接口，并进入Eth-Trunk三层子接口视图。
interface eth-trunk trunk-id.subnumber subnumber是Eth-Trunk三层子接口的编号。
说明缺省情况下，三层子接口状态发生改变会产生linkdown告警（Trap OID：1.3.6.1.6.1.1.5.3）。
如果设备上三层子接口数量较多，接口产生的linkdown告警每隔几分钟会上报一次，此时网管设备需要处理大量的接口状态告警信息，增加了网管设备的负担。为解决上述问题，在确认不需要关注linkdown告警的情况下可以在系统视图下执行subinterface trap updown disable命令关闭三层子接口产生linkdown告警功能。执行此命令后设备上所有子接口状态发生变化均不会产生linkdown告警，请谨慎操作。
步骤5 配置Eth-Trunk三层子接口对单层Tag报文的终结功能。
dot1q termination vid low-pe-vid
----结束后续处理Eth-Trunk三层子接口创建完成后，可以在该子接口下配置IP地址、MTU值及相关业务，同时可以通过display interface eth-trunk trunk-id.subnumber命令查看Eth- Trunk子接口的状态信息。

### 3.11 删除Eth-Trunk配置

前提条件已在设备上配置了Eth-Trunk接口及成员接口。
操作步骤将指定成员接口从Eth-Trunk接口中删除成员接口从Eth-Trunk接口中删除前，建议先将成员接口shutdown，删除后再undo shutdown。
删除成员接口有如下两种方式，请根据需要选择其一即可。
● 在Eth-Trunk接口视图下删除成员接口
a. 进入系统视图。
system-view

### 3.12 维护Eth-Trunk

b. 进入Eth-Trunk接口视图。
interface eth-trunk trunk-id
c. 删除指定成员接口。
undo trunkport interface-type { interface-number1 [ to interface-number2 ] } &<1-16>
● 在成员接口视图下删除对应Eth-Trunk接口
a. 进入系统视图。
system-view
b. 进入Eth-Trunk成员接口视图。
interface interface-type interface-number
c. 删除Eth-Trunk接口。
undo eth-trunk
删除Eth-Trunk接口
将所有的成员接口从Eth-Trunk接口中删除。
1. 进入系统视图。
system-view
2. 将所有的成员接口从 Eth-Trunk 接口中删除，参考将指定成员接口从 Eth-Trunk 接
口中删除。
3. 删除Eth-Trunk接口。
undo interface eth-trunk trunk-id
说明
如果Eth-Trunk接口下创建了三层子接口，需要先在系统视图下执行undo interface eth-trunk
trunk-id.subnumber删除三层子接口，再删除Eth-Trunk接口。
三层子接口仅S6780-H、S6750-H、S6730-S-V2、S6750-S、S6750E-S、S6730-H-V2、
S6730E-H-V2、S5755-H、S5755-S、S5732-H-V2系列支持。
任务示例
从Eth-Trunk 1中删除成员接口10GE1/0/1。
方法一：
<HUAWEI> system-view
[HUAWEI] interface eth-trunk 1
[HUAWEI-Eth-Trunk1] undo trunkport 10ge 1/0/1
方法二：
<HUAWEI> system-view
[HUAWEI] interface 10ge 1/0/1
[HUAWEI-10GE1/0/1] undo eth-trunk
所有成员接口均从Eth-Trunk 1接口中删除后，可以删除Eth-Trunk 1接口。
<HUAWEI> system-view
[HUAWEI] undo interface eth-trunk 1
维护
3.12 Eth-Trunk

#### 3.12.1 监控Eth-Trunk运行状况

背景信息在日常维护工作中，可以在任意视图下选择执行以下命令，了解Eth-Trunk的运行状况。
操作步骤监控Eth-Trunk运行状况的相关操作如表3-6所示。
表 3-6 监控 Eth-Trunk 运行状况

| 操作 | 命令 |
|---|---|
| 未配置静态LACP模式Eth-Trunk时，查看 LACP的系统优先级和系统ID。 | display lacp brief |
| 配置静态LACP模式Eth-Trunk后，查看 Eth-Trunk接口的配置信息。 | display eth-trunk [ trunk-id [ interface interface-type interface- number | verbose ] | brief ] |
| 查看Eth-Trunk接口的状态信息。 | display interface eth-trunk [ trunk-id [ .subnumber ] | main ] |
| 查看Eth-Trunk接口的转发表。 | display interface eth-trunk trunk-id forwarding-table |
| 查看Eth-Trunk以及Eth-Trunk成员接口信息。 | display eth-trunk membership trunk- id |
| 查看LACP模式下的LACP报文收发统计信息。 | display lacp statistics eth-trunk [ trunk-id [ interface interface-type interface-number ] ] |
| 查看Eth-Trunk接口管理状态数据表。 | display fwm trunk ifmstate interface interface-type interface-number |
| 查看转发面和控制面的Eth-Trunk ID信息。 | display fwm eth-trunk trunk-id local- id [ slot slot-id ] |
| 查看LACP使能数据表。 | display fwm eth-trunk lacpenable trunk-id |
| 查看Eth-Trunk中的成员接口信息。 | display fwm eth-trunk member trunk-id |
| 查看Eth-Trunk状态信息。 | display fwm eth-trunk status trunk- id |
| 查看Eth-Trunk负载分担模板数据表。 | display fwm eth-trunk profile trunk- id |

#### 3.12.2 查询Eth-Trunk故障信息

背景信息当Eth-Trunk接口发生故障（例如协商失败、接口状态震荡等）或LACP协议产生断连故障时，可以在任意视图下执行以下命令查看故障原因，通过获取的信息方便进行故障定位。
操作步骤查询Eth-Trunk故障信息的相关操作如3.12.2 查询Eth-Trunk故障信息所示。
表 3-7 查询 Eth-Trunk 故障信息

| 操作 | 命令 |
|---|---|
| 查看Eth-Trunk接口故障原因 | display eth-trunk troubleshooting |
| 查看LACP模式下LACP发生断连的原因 | display lacp troubleshooting |

#### 3.12.3 清除统计信息

背景信息当您需要统计一定时间内某接口的流量信息，这时必须在统计开始前清除该接口原有的统计信息，使接口重新进行统计。
须知清除计数器信息后，以前的信息将无法恢复，务必仔细确认。
操作步骤清除Eth-Trunk接口相关的统计信息如表3-8所示，请在用户视图下执行以下命令。
表 3-8 清除统计信息

| 操作 | 命令 |
|---|---|
| 清除Eth-Trunk接口的报文统计信息 | reset interface counters eth-trunk trunk-id |
| 清除LACP模式Eth-Trunk接口的LACP报文统计信息 | reset lacp statistics eth-trunk [ trunk-id [ interface interface-type interface-number ] ] |

#### 3.12.4 配置LACP告警控制功能

背景信息当LACP模式Eth-Trunk的业务出现故障时，设备会上报LACP告警。为了避免告警频繁上报，可以配置LACP告警控制功能。配置该功能后，LACP只在如下场景上报hwLacpNegotiateFailed、hwLacpPartialLinkLoss、hwLacpTotalLinkLoss和Eth- Trunk的linkdown告警：
● 物理链路Down导致LACP协商Down。
● LACP超时导致LACP协商Down。
● LACP判断报文环回导致LACP协商Down。
● LACP判断当前端口对端的协商报文中的系统ID、端口Key和参考端口对端的系统ID、端口Key不一致导致的LACP协商Down。
操作步骤步骤 进入系统视图。
1 system-view步骤2 开启LACP告警控制功能。
lacp alarm-control link-failure当设备已经上报hwLacpNegotiateFailed、hwLacpPartialLinkLoss、hwLacpTotalLinkLoss或Eth-Trunk的linkdown告警时，执行lacp alarm-control link- failure命令后，如果已上报的告警触发条件不在该命令指定的4种场景内，设备会上报恢复告警，但是实际上产生该告警的问题依然存在，并未解决。
说明执行lacp alarm-control link-failure命令后，除了该命令指定的4种场景，其他情况均不会上报hwLacpNegotiateFailed、hwLacpPartialLinkLoss、hwLacpTotalLinkLoss和Eth-Trunk的linkdown告警，因此请谨慎操作。
----结束

#### 3.12.5 配置Eth-Trunk成员接口通过私有MIB发送Trap

背景信息当Eth-Trunk成员接口的状态发生变化时，系统会将成员接口的状态变化信息通过Trap告知用户，以便用户确认是否是设备的故障导致。如果用户需要精确到指定ID的Eth- Trunk接口，可以使能Eth-Trunk成员接口通过私有MIB发送Trap信息，使该Trap信息中携带指定ID的Eth-Trunk接口信息。
配置该功能后，只会发送私有MIB的Trap，不会发送公有MIB的Trap。需要用华为公司的私有MIB查看发送的Trap告警。
操作步骤步骤1 进入系统视图。
system-view

步骤2 配置Eth-Trunk成员接口通过私有MIB发送Trap信息。
trunk-member trap in private-mib enable
----结束

#### 3.12.6 使用Ping检测三层Eth-Trunk成员接口连通性

前提条件在使用Ping检测三层Eth-Trunk成员接口连通性前，必须确保已在三层Eth-Trunk接口下配置了IP地址。
背景信息Eth-Trunk是由多个物理接口捆绑的一个逻辑接口，每一个成员接口的传输路径都不一样，其承载业务的相应时延、抖动和丢包率等也不尽相同。因此，当一个Eth-Trunk承载的业务质量大幅下降的时候，无法准确判断是Eth-Trunk中的哪一个成员接口出了问题。通过Ping检测Eth-Trunk成员接口，实现对某一实际物理链路的检测，方便用户精确定位出现故障的链路。
说明适用于直连的Eth-Trunk接口的检测场景。
操作步骤步骤1 进入系统视图。
system-view步骤2 在接收端开启三层Eth-Trunk成员接口检测功能。
trunk member-port-inspect缺省情况下，设备未使能Eth-Trunk成员接口检测功能。
说明配置该命令后，会对设备上所有三层Eth-Trunk接口生效，如果后续仅需要对Eth-Trunk链路的连通性进行检测，在执行完Eth-Trunk接口的成员接口检测后，请关闭该功能。否则，仍然对Eth- Trunk成员接口进行检测，造成系统资源的浪费。
步骤 3 在发送端发起对三层 Eth-Trunk 成员接口的检测。
ping [ ip ] -a source-ip-address -i interface-type interface-number [ -8021p 8021p-value | -c count | | { -f | ignore-mtu } | -h ttl-value | -m time | -p pattern | -q | -r | -ri | -s packetsize | -system-time | -t timeout | { - tos tos-value | -dscp dscp-value } | -v | -vpn-instance vpn-instance-name ] * host [ ip-forwarding ]说明在进行三层Eth-Trunk成员接口检测时，必须指定-a和-i参数，分别用于指定发送ICMP ECHO- REQUEST报文的源IP地址和接口。
命令执行结果输出包括：
● 对每一个 ping 报文的响应情况，如果发送端超时后仍没有收到响应报文，则输出“Request time out”，表示Eth-Trunk某一个成员接口出现故障，否则显示响应报文中数据字节数、报文序号、响应时间等，表示Eth-Trunk成员接口未出现故障。

#### 3.13.1 举例：配置手工模式Eth-Trunk

● 最后的统计信息，包括发送报文数、接收报文数、未响应报文百分比和响应时间
的最小、最大和平均值。
<HUAWEI> ping -a 192.168.1.1 -i 10ge 1/0/1 10.1.1.2
PING 10.1.1.2: 56 data bytes, press CTRL_C to break
Reply from 10.1.1.2: bytes=56 Sequence=1 ttl=254 time=2
ms
Reply from 10.1.1.2: bytes=56 Sequence=2 ttl=254 time=1
ms
Reply from 10.1.1.2: bytes=56 Sequence=3 ttl=254 time=2
ms
Reply from 10.1.1.2: bytes=56 Sequence=4 ttl=254 time=1
ms
Reply from 10.1.1.2: bytes=56 Sequence=5 ttl=254 time=2
ms
--- 10.1.1.2 ping statistics ---
5 packet(s) transmitted
5 packet(s) received
0.00% packet loss
round-trip min/avg/max = 1/1/2 ms
----结束

### 3.13 Eth-Trunk配置举例

举例：配置手工模式
3.13.1 Eth-Trunk组网需求如图3-16所示，DeviceA和DeviceB之间存在多条链路，需要提供较大的带宽来实现流量负载分担，同时也希望能够提供一定的冗余度，保证数据传输和链路的可靠性。
图 3-16 配置手工模式 Eth-Trunk 组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。
操作步骤步骤1 在DeviceA和DeviceB上分别创建Eth-Trunk1并配置为手工模式。
\# 配置DeviceA。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] interface eth-trunk 1 [DeviceA-Eth-Trunk1] portswitch [DeviceA-Eth-Trunk1] mode manual load-balance \# 配置DeviceB。
<HUAWEI> system-view [HUAWEI] sysname DeviceB

[DeviceB] interface eth-trunk 1 [DeviceB-Eth-Trunk1] portswitch [DeviceB-Eth-Trunk1] mode manual load-balance步骤2 向DeviceA和DeviceB的Eth-Trunk接口中加入成员接口。
\# 配置DeviceA。
[DeviceA-Eth-Trunk1] trunkport 10ge 1/0/1 to 1/0/3 [DeviceA-Eth-Trunk1] quit \# 配置DeviceB。
[DeviceB-Eth-Trunk1] trunkport 10ge 1/0/1 to 1/0/3 [DeviceB-Eth-Trunk1] quit
----结束检查配置结果在任意视图下执行display eth-trunk 1命令，检查Eth-Trunk是否创建成功，及成员接口是否正确加入。
[DeviceA] display eth-trunk 1 Eth-Trunk1's state information is:
Working Mode: Normal Hash Arithmetic: profile default Least Active-linknumber: 1 Max Bandwidth-affected-linknumber: 128 Operating Status: up Number of Up Ports in Trunk: 3
-------------------------------------------------------------------------------- PortName Status Weight 10GE1/0/1 Up 1 10GE1/0/2 Up 1 10GE1/0/3 Up 1从以上信息看出Eth-Trunk 1中包含3个成员接口10GE1/0/1、10GE1/0/2、10GE1/0/3，成员接口的状态都为Up。Eth-Trunk 1的“Operating Status”为Up。
配置脚本
● DeviceA \# sysname DeviceA \# interface Eth-Trunk1 \# interface 10GE1/0/1 eth-trunk 1 \# interface 10GE1/0/2 eth-trunk 1 \# interface 10GE1/0/3 eth-trunk 1 \# return
● DeviceB \# sysname DeviceB \# interface Eth-Trunk1 \# interface 10GE1/0/1 eth-trunk 1 \# interface 10GE1/0/2

eth-trunk 1 \# interface 10GE1/0/3 eth-trunk 1 \# return

#### 3.13.2 举例：配置静态LACP模式Eth-Trunk

组网需求如图3-17所示，DeviceA和DeviceB之间存在多条链路，在两台设备上配置静态LACP模式链路聚合组，提高两设备之间的带宽与可靠性，具体要求如下：
● 两条活动链路具有负载分担的能力。
● 两设备间的链路具有1条冗余备份链路，当活动链路出现故障链路时，备份链路替代故障链路，保持数据传输的可靠性。
图 3-17 配置静态 LACP 模式 Eth-Trunk 组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。
操作步骤步骤1 在DeviceA和DeviceB上分别创建Eth-Trunk1并配置为静态LACP模式。
\# 配置DeviceA。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] interface eth-trunk 1 [DeviceA-Eth-Trunk1] mode lacp-static [DeviceA-Eth-Trunk1] quit \# 配置DeviceB。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] interface eth-trunk 1 [DeviceB-Eth-Trunk1] mode lacp-static [DeviceB-Eth-Trunk1] quit步骤2 向DeviceA和DeviceB的Eth-Trunk接口中加入成员接口。
\# 配置DeviceA。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] eth-trunk 1 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2

[DeviceA-10GE1/0/2] eth-trunk 1 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] eth-trunk 1 [DeviceA-10GE1/0/3] quit \# 配置DeviceB。
[DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] eth-trunk 1 [DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] eth-trunk 1 [DeviceB-10GE1/0/2] quit [DeviceB] interface 10ge 1/0/3 [DeviceB-10GE1/0/3] eth-trunk 1 [DeviceB-10GE1/0/3] quit步骤3 在DeviceA上配置系统优先级为100，DeviceB上保持缺省值，使DeviceA成为LACP主动端。
[DeviceA] lacp priority 100步骤4 在DeviceA上配置活动接口上限阈值为2，剩余一条作为冗余备份链路。
[DeviceA] interface eth-trunk 1 [DeviceA-Eth-Trunk1] lacp max active-linknumber 2 [DeviceA-Eth-Trunk1] quit步骤5 在DeviceA上配置接口优先级确定活动链路。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] lacp priority 100 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] lacp priority 100 [DeviceA-10GE1/0/2] quit
----结束检查配置结果\# 查看各Device设备的Eth-Trunk信息，查看链路是否协商成功。
[DeviceA] display eth-trunk 1 Eth-Trunk1's state information is:
Local:
LAG ID: 1 Working Mode: Static Preempt Delay: Disabled Hash Arithmetic: profile default System Priority: 100 System ID: xxxx-xxxx-xxxx Least Active-linknumber: 1 Max Active-linknumber: 2 Operating Status: up Number Of Up Ports In Trunk: 2 Timeout Period: Slow
-------------------------------------------------------------------------------- ActorPortName Status PortType PortPri PortNo PortKey PortState Weight 10GE1/0/1 Selected 10GE 100 1 20289 10111100 1 10GE1/0/2 Selected 10GE 100 2 20289 10111100 1 10GE1/0/3 Unselect 10GE 32768 3 20289 10100000 1 Partner:
-------------------------------------------------------------------------------- ActorPortName SysPri SystemID PortPri PortNo PortKey PortState 10GE1/0/1 32768 xxxx-xxxx-xxxx 32768 4 20289 10111100 10GE1/0/2 32768 xxxx-xxxx-xxxx 32768 5 20289 10111100 10GE1/0/3 32768 xxxx-xxxx-xxxx 32768 6 20289 10100000 [DeviceB] display eth-trunk 1 Eth-Trunk1's state information is:
Local:
LAG ID: 1 Working Mode: Static Preempt Delay: Disabled Hash Arithmetic: profile default

System Priority: 32768 System ID: xxxx-xxxx-xxxx Least Active-linknumber: 1 Max Active-linknumber: 128 Operating Status: up Number Of Up Ports In Trunk: 2 Timeout Period: Slow
-------------------------------------------------------------------------------- ActorPortName Status PortType PortPri PortNo PortKey PortState Weight 10GE1/0/1 Selected 10GE 32768 4 20289 10111100 1 10GE1/0/2 Selected 10GE 32768 5 20289 10111100 1 10GE1/0/3 Unselect 10GE 32768 6 20289 10100000 1 Partner:
-------------------------------------------------------------------------------- ActorPortName SysPri SystemID PortPri PortNo PortKey PortState 10GE1/0/1 100 xxxx-xxxx-xxxx 100 1 20289 10111100 10GE1/0/2 100 xxxx-xxxx-xxxx 100 2 20289 10111100 10GE1/0/3 100 xxxx-xxxx-xxxx 32768 3 20289 10100000通过以上显示信息可以看到，DeviceA的系统优先级为100，高于DeviceB的系统优先级。Eth-Trunk的成员接口中10GE1/0/1、10GE1/0/2成为活动接口，处于“Selected”状态，接口10GE1/0/3处于“Unselect”状态，同时实现冗余备份功能。
配置脚本
● DeviceA \# sysname DeviceA \# lacp priority 100 \# interface Eth-Trunk1 mode lacp-static lacp max active-linknumber 2 \# interface 10GE1/0/1 eth-trunk 1 lacp priority 100 \# interface 10GE1/0/2 eth-trunk 1 lacp priority 100 \# interface 10GE1/0/3 eth-trunk 1 \# return
● DeviceB \# sysname DeviceB \# interface Eth-Trunk1 mode lacp-static \# interface 10GE1/0/1 eth-trunk 1 \# interface 10GE1/0/2 eth-trunk 1 \# interface 10GE1/0/3 eth-trunk 1 \# return

#### 3.13.3 举例：配置动态LACP模式Eth-Trunk

组网需求如图3-18所示，服务器A与DeviceA建立动态LACP模式链路聚合，两端设备将通过动态LACP协议报文进行链路聚合协商。
图 3-18 动态 LACP 模式 Eth-Trunk 组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。
操作步骤步骤1 在DeviceA上创建动态LACP模式Eth-Trunk接口，并将以太网物理接口加入Eth-Trunk接口。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] interface eth-trunk 1 [DeviceA-Eth-Trunk1] mode lacp-dynamic [DeviceA-Eth-Trunk1] quit [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] eth-trunk 1 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] eth-trunk 1 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] eth-trunk 1 [DeviceA-10GE1/0/3] quit步骤2 在DeviceA上配置活动接口上限阈值为2。
[DeviceA] interface eth-trunk 1 [DeviceA-Eth-Trunk1] lacp max active-linknumber 2 [DeviceA-Eth-Trunk1] quit步骤 3 在 DeviceA 上配置接口优先级确定活动链路。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] lacp priority 100 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] lacp priority 100 [DeviceA-10GE1/0/2] quit
----结束检查配置结果\# 在 DeviceA 上执行 display eth-trunk 命令查看 Eth-Trunk 信息。
[DeviceA] display eth-trunk 1 Eth-Trunk1's state information is:
Local:

LAG ID: 1 Working Mode: Dynamic Preempt Delay: Disabled Hash Arithmetic: profile default System Priority: 32768 System ID: xxxx-xxxx-xxxx Least Active-linknumber: 1 Max Active-linknumber: 2 Operating Status: up Number Of Up Ports In Trunk: 0 Timeout Period: Slow
-------------------------------------------------------------------------------- ActorPortName Status PortType PortPri PortNo PortKey PortState Weight 10GE1/0/1 Indep 10GE 100 0 321 10100010 1 10GE1/0/2 Indep 10GE 100 1 321 10100010 1 10GE1/0/3 Indep 10GE 32768 2 321 10100010 1 Partner:
-------------------------------------------------------------------------------- ActorPortName SysPri SystemID PortPri PortNo PortKey PortState 10GE1/0/1 0 xxxx-xxxx-xxxx 0 0 0 10100011 10GE1/0/2 0 xxxx-xxxx-xxxx 0 0 0 10100011 10GE1/0/3 0 xxxx-xxxx-xxxx 0 0 0 10100011通过以上显示信息可以看到，Eth-Trunk的ID是1，Eth-Trunk的模式是动态LACP模式，Eth-Trunk的成员接口10GE1/0/1、10GE1/0/2、10GE1/0/3的状态都为Indep。
\# 当 DeviceA 能够收到服务器 A 的 LACP 协议报文，且两端通过 LACP 协议报文链路聚合协商成功，在DeviceA上执行display eth-trunk命令查看Eth-Trunk信息。
[DeviceA] display eth-trunk 1 Eth-Trunk1's state information is:
Local:
LAG ID: 1 Working Mode: Dynamic Preempt Delay: Disabled: Hash Arithmetic: profile default System Priority: 32768 System ID: xxxx-xxxx-xxxx Least Active-linknumber: 1 Max Active-linknumber: 2 Operating Status: up Number Of Up Ports In Trunk: 2 Timeout Period: Slow
-------------------------------------------------------------------------------- ActorPortName Status PortType PortPri PortNo PortKey PortState Weight 10GE1/0/1 Selected 10GE 100 0 321 10111100 1 10GE1/0/2 Selected 10GE 100 1 321 10111100 1 10GE1/0/3 Unselect 10GE 32768 2 321 10100000 Partner:
-------------------------------------------------------------------------------- ActorPortName SysPri SystemID PortPri PortNo PortKey PortState 10GE1/0/1 32768 xxxx-xxxx-xxxx 32768 0 321 10111100 10GE1/0/2 32768 xxxx-xxxx-xxxx 32768 1 321 10111100 10GE1/0/3 32768 xxxx-xxxx-xxxx 32768 2 321 10100000通过以上显示信息可以看到，Eth-Trunk的ID是1、Eth-Trunk的模式是动态LACP模式，Eth-Trunk的成员接口中10GE1/0/1、10GE1/0/2成为活动接口，处于Selected状态，接口10GE1/0/3处于Unselect状态。
配置脚本DeviceA \# sysname DeviceA \# interface Eth-Trunk1 mode lacp-dynamic

lacp max active-linknumber 2 \# interface 10GE1/0/1 eth-trunk 1 lacp priority 100 \# interface 10GE1/0/2 eth-trunk 1 lacp priority 100 \# interface 10GE1/0/3 eth-trunk 1 \# return

#### 3.13.4 举例：配置LACP模式的跨设备Eth-Trunk

组网需求如图3-19所示，DeviceA跨设备接入DeviceB和DeviceC，在DeviceA上部署LACP模式的Eth-Trunk接口，成员接口分别与DeviceB和DeviceC的10GE1/0/1～10GE1/0/2连接，10GE1/0/1～10GE1/0/2的接口速率和双工模式相同，现在需要使流量可以在两台设备上负载分担。
图 3-19 跨设备 Eth-Trunk 组网图说明本例中interface1、interface2、interface3、interface4分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3、10GE1/0/4。
配置思路采用如下的思路配置跨设备LACP模式链路聚合：
1. 分别在DeviceA、DeviceB、DeviceC上创建Eth-Trunk1，并配置为静态LACP模式，将成员接口加入Eth-Trunk1。
2. 在DeviceB和DeviceC上配置相同的LACP系统ID。
3. 在DeviceB和DeviceC上配置相同的系统LACP优先级。
4. 在DeviceC上配置Eth-Trunk成员接口在LACP协议中的编号扩展，使成员接口编号均增加32768，避免和设备DeviceB上的成员接口在LACP协议中的编号相同。

操作步骤步骤1 分别在DeviceA、DeviceB和DeviceC上创建Eth-Trunk1并配置为LACP模式，并将成员接口加入Eth-Trunk1。
\# 配置DeviceA。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] interface eth-trunk 1 [DeviceA-Eth-Trunk1] mode lacp-static [DeviceA-Eth-Trunk1] trunkport 10ge 1/0/1 to 1/0/4 [DeviceA-Eth-Trunk1] quit \# 配置DeviceB。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] interface eth-trunk 1 [DeviceB-Eth-Trunk1] mode lacp-static [DeviceB-Eth-Trunk1] trunkport 10ge 1/0/1 to 1/0/2 \# 配置DeviceC。
<HUAWEI> system-view [HUAWEI] sysname DeviceC [DeviceC] interface eth-trunk 1 [DeviceC-Eth-Trunk1] mode lacp-static [DeviceC-Eth-Trunk1] trunkport 10ge 1/0/1 to 1/0/2步骤2 配置DeviceB和DeviceC的系统ID为00e0-fc00-0000。
\# 配置DeviceB。
[DeviceB-Eth-Trunk1] lacp system-id 00e0-fc00-0000 [DeviceB-Eth-Trunk1] quit \# 配置DeviceC。
[DeviceC-Eth-Trunk1] lacp system-id 00e0-fc00-0000 [DeviceC-Eth-Trunk1] quit步骤3 在DeviceB和DeviceC上配置系统LACP优先级为100。
\# 配置DeviceB。
[DeviceB] lacp priority 100 \# 配置DeviceC。
[DeviceC] lacp priority 100步骤4 在DeviceC上配置Eth-Trunk成员接口编号扩展，使成员接口编号均增加32768。
[DeviceC] interface eth-trunk 1 [DeviceC-Eth-Trunk1] lacp port-id-extension enable [DeviceC-Eth-Trunk1] quit
----结束检查配置结果\# 查看各Device设备的Eth-Trunk信息，查看链路是否协商成功。
[DeviceA] display eth-trunk 1 Eth-Trunk1's state information is:
Local:
LAG ID: 1 Working Mode: Static

Preempt Delay: Disabled Hash Arithmetic: profile default System Priority: 100 System ID: 00e0-fc12-1111 Least Active-linknumber: 1 Max Active-linknumber: 128 Operating Status: up Number Of Up Ports In Trunk: 4 Timeout Period: Slow
-------------------------------------------------------------------------------- ActorPortName Status PortType PortPri PortNo PortKey PortState Weight 10GE1/0/1 Selected 10GE 32768 3 321 10111100 1 10GE1/0/2 Selected 10GE 32768 1 321 10100010 1 10GE1/0/3 Selected 10GE 32768 4 321 10111100 1 10GE1/0/4 Selected 10GE 32768 2 321 10100010 1 Partner:
-------------------------------------------------------------------------------- ActorPortName SysPri SystemID PortPri PortNo PortKey PortState 10GE1/0/1 100 00e0-fc00-0000 32768 32769 321 10111100 10GE1/0/2 100 00e0-fc00-0000 32768 32770 321 10111100 10GE1/0/1 100 00e0-fc00-0000 32768 4 321 10111100 10GE1/0/2 100 00e0-fc00-0000 32768 5 321 10111100 [DeviceB] display eth-trunk 1 Eth-Trunk1's state information is:
Local:
LAG ID: 1 Working Mode: Static Preempt Delay: Disabled Hash Arithmetic: profile default System Priority: 100 System ID: 00e0-fc00-0000 Least Active-linknumber: 1 Max Active-linknumber: 128 Operating Status: up Number Of Up Ports In Trunk: 2 Timeout Period: Slow
-------------------------------------------------------------------------------- ActorPortName Status PortType PortPri PortNo PortKey PortState Weight 10GE1/0/1 Selected 10GE 32768 4 321 10111100 1 10GE1/0/2 Selected 10GE 32768 5 321 10111100 1 Partner:
-------------------------------------------------------------------------------- ActorPortName SysPri SystemID PortPri PortNo PortKey PortState 10GE1/0/3 100 00e0-fc12-1111 32768 4 321 10111100 10GE1/0/4 100 00e0-fc12-1111 32768 2 321 10100010 [DeviceC] display eth-trunk 1 Eth-Trunk1's state information is:
Local:
LAG ID: 1 Working Mode: Static Preempt Delay: Disabled Hash Arithmetic: profile default System Priority: 100 System ID: 00e0-fc00-0000 Least Active-linknumber: 1 Max Active-linknumber: 128 Operating Status: up Number Of Up Ports In Trunk: 2 Timeout Period: Slow
-------------------------------------------------------------------------------- ActorPortName Status PortType PortPri PortNo PortKey PortState Weight 10GE1/0/1 Selected 10GE 32768 32769 321 10111100 1 10GE1/0/2 Selected 10GE 32768 32770 321 10111100 1 Partner:
-------------------------------------------------------------------------------- ActorPortName SysPri SystemID PortPri PortNo PortKey PortState 10GE1/0/1 100 00e0-fc12-1111 32768 3 321 10111100 10GE1/0/2 100 00e0-fc12-1111 32768 1 321 10100010通过以上显示信息可以看到，各Device的Operating Status均为Up，表明Eth-Trunk1已经协商成功。DeviceB和DeviceC上的成员接口成为活动接口，处于“Selected”状态，表示DeviceB和DeviceC上的成员接口均可以负载分担。DeviceC的PortNo显示成员接口的LACP编号已经增加32768。
配置脚本
● DeviceA \# sysname DeviceA

\# interface Eth-Trunk1 mode lacp-static \# interface 10GE1/0/1 eth-trunk 1 \# interface 10GE1/0/2 eth-trunk 1 \# interface 10GE1/0/3 eth-trunk 1 \# interface 10GE1/0/4 eth-trunk 1 \# return
● DeviceB \# sysname DeviceB \# lacp priority 100 \# interface Eth-Trunk1 mode lacp-static lacp system-id 00e0-fc00-0000 \# interface 10GE1/0/1 eth-trunk 1 \# interface 10GE1/0/2 eth-trunk 1 \# return
● DeviceC \# sysname DeviceC \# lacp priority 100 \# interface Eth-Trunk1 mode lacp-static lacp system-id 00e0-fc00-0000 lacp port-id-extension enable \# interface 10GE1/0/1 eth-trunk 1 \# interface 10GE1/0/2 eth-trunk 1 \# return

#### 3.13.5 举例：配置Eth-Trunk接口手工1∶1主备模式

组网需求对于全双工点对点链路，随着承载的业务量越来越多，单条物理链路已不能满足正常的业务可靠性需求。为了在不增加硬件资源的情况下提升链路可靠性，可以采用链路聚合技术部署 Eth-Trunk 接口实现。
如图3-20所示，为了提高DeviceA和DeviceB之间的链路可靠性，可在DeviceA、DeviceB上部署手工1:1主备模式Eth-Trunk接口。

图 3-20 配置手工 1∶1 主备模式 Eth-Trunk 接口组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
注意事项为了保证手工1:1主备模式Eth-Trunk接口正常转发数据，需要注意：
必须为Eth-Trunk接口指定主接口，数据通过主接口转发。缺省情况下，先加入1:1主备模式Eth-Trunk接口的成员口将成为主接口。
配置思路采用如下的思路配置手工1∶1主备模式Eth-Trunk：
分别在DeviceA、DeviceB设备上创建手工1∶1主备模式Eth-Trunk接口，将以太网物理接口加入Eth-Trunk接口，实现链路聚合。
1. 分别在DeviceA、DeviceB设备上指定Eth-Trunk接口的主接口，实现冗余备份，提高链路可靠性。
数据准备为完成此配置例，需准备如下的数据：
● Eth-Trunk接口ID。
● Eth-Trunk的成员接口类型和编号。
操作步骤步骤1 分别在DeviceA、DeviceB设备上创建手工1∶1主备模式Eth-Trunk接口，将以太网物理接口加入Eth-Trunk接口。
\# 配置 DeviceA 。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] interface eth-trunk 1 [DeviceA-Eth-Trunk1] mode manual backup [DeviceA-Eth-Trunk1] trunkport 10ge 1/0/1 [DeviceA-Eth-Trunk1] trunkport 10ge 1/0/2 [DeviceA-Eth-Trunk1] quit \#配置DeviceB。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] interface eth-trunk 1 [DeviceB-Eth-Trunk1] mode manual backup [DeviceB-Eth-Trunk1] trunkport 10ge 1/0/1 [DeviceB-Eth-Trunk1] trunkport 10ge 1/0/2 [DeviceB-Eth-Trunk1] quit

步骤2 分别在DeviceA、DeviceB设备上指定Eth-Trunk接口的主接口。
\#配置DeviceA。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] undo shutdown [DeviceA-10GE1/0/1] port-master [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] undo shutdown [DeviceA-10GE1/0/2] quit \#配置DeviceB。
[DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] undo shutdown [DeviceB-10GE1/0/1] port-master [DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] undo shutdown [DeviceB-10GE1/0/2] quit
----结束操作结果\# 上述配置完成后，查看配置了手工1∶1主备模式Eth-Trunk接口信息，可以看到Eth- Trunk的ID、Eth-Trunk的模式是手工1:1主备模式等信息。以DeviceA的显示信息为例。
[DeviceA] display eth-trunk 1 Eth-Trunk1's state information is:
WorkingMode: BACKUP WorkingState: Master
-------------------------------------------------------------------------------- PortName Slave/Master Status 10GE1/0/1 M Up 10GE1/0/2 S Up配置脚本
● DeviceA的配置文件sysname DeviceA \# interface Eth-Trunk1 mode manual backup \# interface 10GE1/0/1 eth-trunk 1 port-master \# interface 10GE1/0/2 eth-trunk 1 \# return
● DeviceB的配置文件\# sysname DeviceB \# interface Eth-Trunk1 mode manual backup \# interface 10GE1/0/1 eth-trunk 1 port-master

\# interface 10GE1/0/2 eth-trunk 1 \# return

#### 3.13.6 举例：配置Eth-Trunk接口流量本地优先转发示例（集群/堆叠）

组网需求如图3-21所示，为了增加设备的容量采用设备集群技术，将DeviceA和DeviceB通过专用的集群电缆链接起来，对外呈现为一台逻辑交换机。为了实现设备间的备份、提高可靠性，采用跨集群设备Eth-Trunk接口技术，将不同设备上的物理接口加入同一个Eth-Trunk接口。在网络无任何故障情况下，在PE设备上查看成员口信息时，发现VLAN2的数据流量会通过成员口10GE1/0/1和10GE1/0/2转发，VLAN3的数据流量通过成员口10GE1/0/1和10GE1/0/2转发。增加了集群设备之间的带宽承载能力，也降低了流量转发效率。
为了有效保证VLAN2的数据流量通过成员口10GE1/0/1转发，VLAN3的数据流量通过成员口10GE1/0/2转发，可在集群/堆叠设备上使能Eth-Trunk接口流量本地优先转发功能。
说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。

图 3-21 接口流量本地优先转发组网图操作步骤步骤1 创建Eth-Trunk接口，并配置允许通过的VLAN。
\# 配置集群/堆叠设备。
<HUAWEI> system-view [HUAWEI] sysname CSS [CSS] interface eth-trunk 10 [CSS-Eth-Trunk10] portswitch [CSS-Eth-Trunk10] port link-type trunk [CSS-Eth-Trunk10] port trunk allow-pass vlan all [CSS-Eth-Trunk10] quit \# 配置汇聚设备PE。
<HUAWEI> system-view [HUAWEI] sysname PE [PE] interface eth-trunk 10 [PE-Eth-Trunk10] portswitch [PE-Eth-Trunk10] port link-type trunk

[PE-Eth-Trunk10] port trunk allow-pass vlan all [PE-Eth-Trunk10] quit步骤2 加入Eth-Trunk的成员接口。
\# 配置集群/堆叠设备。
[CSS] interface 10ge 1/1/0/1 [CSS-10GE1/1/0/1] portswitch [CSS-10GE1/1/0/1] eth-trunk 10 [CSS-10GE1/1/0/1] quit [CSS] interface 10ge 2/1/0/1 [CSS-10GE2/1/0/1] eth-trunk 10 [CSS-10GE2/1/0/1] quit \# 配置汇聚设备PE。
[PE] interface eth-trunk 10 [PE-Eth-Trunk10] trunkport 10ge 1/0/1 to 1/0/2 [PE-Eth-Trunk10] quit步骤3 在集群/堆叠交换机CSS上使能Eth-Trunk接口流量本地优先转发功能。
[CSS] interface eth-trunk 10 [CSS-Eth-Trunk10] undo local-preference disable [CSS-Eth-Trunk10] quit默认情况下，设备已使能Eth-Trunk接口流量本地优先转发功能。
步骤4 配置二层转发功能。
\# 配置集群/堆叠设备。
[CSS] vlan batch 2 3 [CSS] interface 10ge 1/1/0/2 [CSS-10GE1/1/0/2] port link-type trunk [CSS-10GE1/1/0/2] port trunk allow pass vlan 2 [CSS-10GE1/1/0/2] quit [CSS] interface 10ge 2/1/0/2 [CSS-10GE2/1/0/2] port link-type trunk [CSS-10GE2/1/0/2] port trunk allow pass vlan 3 [CSS-10GE2/1/0/2] quit \# 配置接入设备DeviceC，配置DeviceD方法类似，不做赘述。
<HUAWEI> system-view [HUAWEI] sysname DeviceC [DeviceC] vlan 2 [DeviceC-vlan2] quit [DeviceC] interface 10ge 1/0/1 [DeviceC-10GE1/0/1] portswitch [DeviceC-10GE1/0/1] port link-type trunk [DeviceC-10GE1/0/1] port trunk allow pass vlan 2 [DeviceC-10GE1/0/1] quit [DeviceC] interface 10ge 1/0/2 [DeviceC-10GE1/0/2] portswitch [DeviceC-10GE1/0/2] port link-type trunk [DeviceC-10GE1/0/2] port trunk allow pass vlan 2 [DeviceC-10GE1/0/2] quit
----结束检查配置结果\# 上述配置成功后，在任意视图下执行 display eth-trunk membership 命令，可以看到Eth-Trunk接口的成员口信息。例如：
以集群/堆叠交换机CSS的显示为例。

<CSS> display eth-trunk membership 10 Trunk ID: 10 Used status: Valid TYPE: Ethernet Working Mode : Normal Number Of Ports in Trunk = 2 Number Of Up Ports in Trunk = 2 Operate status: up Interface 10GE1/1/0/1, valid, operate up, weight=1 Interface 10GE2/1/0/1, valid, operate up, weight=1配置脚本
● CSS sysname CSS \# vlan batch 2 3 \# interface Eth-Trunk10 port link-type trunk port trunk allow-pass vlan 2 to 4094 \# interface 10GE1/1/0/2 port link-type trunk port trunk allow-pass vlan 2 \# interface 10GE2/1/0/2 port link-type trunk port trunk allow-pass vlan 3 \# interface 10GE1/1/0/1 eth-trunk 10 \# interface 10GE2/1/0/1 eth-trunk 10 \# return
● PE \# sysname PE \# interface Eth-Trunk10 port link-type trunk port trunk allow-pass vlan 2 to 4094 \# interface 10GE1/0/1 eth-trunk 10 \# interface 10GE1/0/2 eth-trunk 10 \# return
● DeviceC \# sysname DeviceC \# vlan batch 2 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 2 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2

\# return
● DeviceD \# sysname DeviceD \# vlan batch 3 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 3 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 3 \# return

### 3.14 Eth-Trunk常见配置错误

#### 3.14.1 负载分担方式配置错误导致Eth-Trunk出接口流量不均衡

说明仅S6730-H-V2，S6730-S-V2，S6730E-H-V2，S5755-H，S5732-H-V2，S6750E-S，S6750- S，S5755-S产品支持该配置。
故障现象Eth-Trunk的负载分担模式配置不合理，导致数据流量在Eth-Trunk各活动链路的负载分担不均衡。
处理步骤
1. 执行display eth-trunk命令，检查Eth-Trunk接口的负载分担模式和实际组网环境的匹配情况，比如二层组网的场景下不适合使用基于源IP地址与目的IP地址进行负载分担。
2. 在Eth-Trunk视图下执行load-balance命令，配置与实际流量相符的负载分担模式。

#### 3.14.2 配置活动接口下限阈值错误导致Eth-Trunk接口两端不能Up

故障现象配置活动接口下限阈值错误，导致Eth-Trunk接口的状态为Down。
处理步骤
1. 执行display eth-trunk trunk-id命令，查看Eth-Trunk接口下是否配置了活动接口数目的下限阈值。
如果 Eth-Trunk 接口下 Up 状态的成员接口数目少于配置的活动接口数目的下限阈值时，Eth-Trunk状态会变为Down。
2. 在Eth-Trunk视图下执行least active-linknumber link-number命令，配置链路聚合活动接口数下限阈值小于Eth-Trunk接口下Up状态的成员接口数目。

本端和对端设备的活动接口数下限阈值可以不同。如果下限阈值不同，以下限阈值数值较大的一端为准。

#### 3.14.3 对端未配置Eth-Trunk导致接口物理UP而链路协议DOWN

故障现象如下图所示，DeviceA上配置Eth-Trunk而DeviceB上未配置Eth-Trunk，会导致DeviceA的物理成员接口是UP状态，链路聚合协议是DOWN状态。
说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。
处理步骤
1. 在DeviceB上分别在10GE1/0/1、10GE1/0/2、10GE1/0/3接口视图下执行命令display this，查看到这三个接口均未加入Eth-Trunk。如果接口加入Eth-Trunk，可以在回显信息看到类似如下配置项，否则接口未加入任何Eth-Trunk。
\# interface 10GE1/0/1 eth-trunk 1 \#
2. 在DeviceB上配置和DeviceA相同模式的Eth-Trunk，具体请参见3.5.1 创建Eth- Trunk接口并配置链路聚合模式。
