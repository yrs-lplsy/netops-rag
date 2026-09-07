# S1700, S5700, S6700 V600R024C10 配置指南-以太网交换 01-04 VLAN配置

## 4 VLAN配置

4 VLAN 配置
4.1 VLAN简介
4.2 VLAN原理描述
4.3 VLAN配置注意事项
4.4 VLAN缺省配置
4.5 创建和删除VLAN
4.6 修改和恢复缺省VLAN
4.7 配置VLANIF接口
4.8 配置同一VLAN内的互通
4.9 配置不同VLAN间的互通
4.10 配置管理VLAN
4.11 配置VLAN pool
4.12 配置VLAN聚合
4.13 配置MUX VLAN
4.14 配置VLAN Mapping
4.15 配置 VLAN 终结
4.16 配置QinQ
4.17 配置QinQ Mapping
4.18 配置QinQ Stacking
4.19 配置Voice VLAN
4.20 配置VLAN内未知报文隔离
4.21 配置 VLAN 透传
4.22 配置丢弃入方向的Tagged报文，防止接口被私自接入其他设备
4.23 维护VLAN

4.24 VLAN配置举例
4.25 VLAN常见配置错误

### 4.1 VLAN简介

定义VLAN（Virtual Local Area Network）即虚拟局域网，是将一个物理的LAN在逻辑上划分成多个广播域的通信技术。
目的早期的以太网是为简单、小型网络而设计的局域网技术，是基于CSMA/CD（Carrier Sense Multiple Access/Collision Detection），并采用共享介质的总线技术。随着时间的推移，局域网承载的数据类型越来越多，包括图形、语音和视频，面临的问题也更加突出。
● 产生冲突：网络中多台主机同时发送数据，造成冲突。主机越多，冲突越严重。
● 产生广播：网络中任意一台主机发送的数据都会被发送到其他所有主机，造成广播。主机越多，广播越泛滥。
● 加剧数据安全的隐患：网络中所有主机共享一台传输通道，无法有效控制数据安全。数据越复杂，数据安全的隐患越大。
虽然采用二层设备的组网架构，通过快速二层交换将数据控制在局域网范围内传输，能有效解决冲突的问题，但是广播和安全的问题依然存在。
为了减少广播，可以通过设置不同网段来实现主机之间的隔离，但是成本较高。在这种情况下，出现了VLAN（Virtual Local Area Network）技术。
VLAN技术可以把一个物理局域网划分成多个逻辑局域网，即多个VLAN。每个VLAN是一个广播域，使得VLAN内的主机可以互通，而VLAN间不能直接互通。这样，广播报文被限制在一个VLAN内，同时提高了网络安全性。
受益使用VLAN能给用户带来以下受益。
● 限制广播域：广播域被限制在一个VLAN内，既节省带宽，又提高网络处理能力。
● 增强局域网的安全性：不同VLAN内的报文在传输时是相互隔离的，即一个VLAN内的用户不能和其他VLAN内的用户直接通信。
● 提高局域网的健壮性：局域网内的故障是隔离的，被限制在一个VLAN内，本VLAN内的故障不会影响其他VLAN内用户的正常工作。
● 灵活构建虚拟工作组：VLAN可以划分不同的用户到不同的工作组，同一工作组的用户也不必局限于某一固定的物理位置，网络构建和维护更方便灵活。

### 4.2 VLAN原理描述

#### 4.2.1 VLAN标签

定义当一个局域网被划分为多个VLAN时，每个VLAN都用一个唯一的VLAN标签来标识。
VLAN标签也称为VLAN Tag或802.1Q Tag。
格式IEEE 802.1Q标准对传统Ethernet帧格式进行了修改，在源MAC地址字段和协议类型字段之间加入4字节的802.1Q Tag，形成了VLAN的帧格式。具体如图4-1所示。
图 4-1 基于 802.1Q 的 VLAN 帧格式
802.1Q Tag包含4个字段，其含义如下：
● TPID：Tag Protocol Identifier，用来判断本VLAN帧是否带有802.1Q Tag，长度为16比特，缺省取值为0x8100。取值为0x8100时表示802.1Q Tag帧。如果不支持802.1Q协议的设备收到这样的帧，会将其丢弃。
各设备厂商可以自定义该字段的值。当邻居设备将TPID值配置为非0x8100时， 本设备为了能够识别这样的帧，实现与各厂家互通，必须在本设备上修改TPID值，确保和邻居设备的TPID值相同。
● PRI：Priority，表示帧的优先级，长度为3比特，取值范围为0～7，值越大优先级越高。用于当设备阻塞时，优先发送优先级高的数据帧。
● CFI：Canonical Format Indicator，表示MAC地址是否是标准格式，长度为1比特，取值范围为0或1，缺省取值为0。取值为0表示MAC地址以标准格式封装，取值为1表示MAC地址以非标准格式封装。
● VID：VLAN ID，表示该帧所属的VLAN，长度为12比特，取值范围为0～4095。
由于0和4095为协议保留取值，所以VLAN ID的有效取值范围为1～4094。
分类每台支持802.1Q协议的设备利用VLAN ID来识别报文所属的VLAN，并根据报文是否携带 VLAN Tag 以及携带的 VLAN Tag 值，来对报文进行处理。因此，数据帧根据是否携带VLAN Tag，分为以下两种形式：
● 有标记帧（Tagged帧），加入了4字节802.1Q Tag的帧。

● 无标记帧（Untagged帧），原始的、未加入4字节802.1Q Tag的帧。
各类设备对Tagged帧、Untagged帧的支持情况不尽相同，通常来说：
● 用户主机、服务器、Hub、无管理交换机只能收发Untagged帧。
● 交换机、路由器、防火墙和WLAN AC既能收发Tagged帧，也能收发Untagged
帧。
● 语音终端可以收发一个VLAN的Tagged帧或Untagged帧。

#### 4.2.2 链路类型和接口类型

链接类型如图4-2所示，VLAN组网中的链路包括：
● 接入链路（Access Link），连接不能或不需要识别VLAN Tag的终端设备。图中，用户主机和设备之间的链路都是接入链路，接入链路上通过的帧为Untagged帧。
● 干道链路（Trunk Link），连接设备和设备的链路。干道链路上通过的帧为Tagged帧，所有数据帧必须都打上VLAN Tag。
图 链路类型示意图4-2接口类型在802.1Q协议中定义VLAN帧后，设备的有些接口可以识别VLAN帧，有些接口则不能识别VLAN帧。根据对VLAN帧的识别情况，将接口分以下几类：
● Access 接口：是设备上用来连接终端设备的接口，这些终端设备不能或不需要识别VLAN Tag。该接口只能连接接入链路，有如下特点：
– 由于设备内部只处理Tagged帧，如果该接口收到Untagged帧，设备将强制加上该接口的PVID（缺省VLAN）。

– 如果该接口收到Tagged帧，只允许VLAN ID与接口的PVID（缺省VLAN）相
同的VLAN通过该接口。
– Access接口发送的数据帧永远是Untagged帧。
● Trunk接口：是设备上用来和其他设备连接的接口，这些设备能识别VLAN Tag。
该接口只能连接干道链路，有如下特点：
– 允许多个VLAN的帧（Tagged帧）通过。
– 该接口发送的帧，接口缺省VLAN内的帧是Untagged帧（VLAN ID=PVID），
其他VLAN内的帧都必须是Tagged帧。
● Hybrid接口：既可以连接Access接口能连接的设备，也可以连接Trunk接口能连接
的设备。该接口既可以连接接入链路又可以连接干道链路，有如下特点：
– 不确定是否能识别VLAN Tag的情况下，建议使用该接口。
– 允许多个VLAN的帧（Tagged帧）通过，并且在出接口方向可根据需要设置
某些VLAN内的帧带Tag，某些VLAN内的帧不带Tag。
● QinQ接口：是指使用QinQ协议的接口。QinQ接口可以给数据帧加上双重VLAN
Tag，即在原来VLAN Tag的基础上，给数据帧加上一个新的VLAN Tag，从而满足
网络对VLAN数量的需求。因此，也称为802.1Q-in-802.1Q接口。

#### 4.2.3 缺省VLAN

缺省VLAN又称为PVID（Port ID），每个接口都有缺省VLAN。
Default VLAN
● Access接口只属于1个VLAN，它的缺省VLAN就是它所在的VLAN。
● Hybrid接口和Trunk接口属于多个VLAN，但是缺省VLAN只有1个，所以需要设置缺省VLAN。
如果设置了接口的缺省VLAN，其处理数据帧的方式请参见“4.2.4 VLAN标签的添加和剥离”。

#### 4.2.4 VLAN标签的添加和剥离

在配置了接口类型和缺省VLAN后，接口对数据帧的处理方式有几种不同情况，如表4-1所示。
说明为了提高设备对数据帧的处理效率，设备内部的数据帧一律都带有VLAN Tag，以便设备对这些数据帧以统一的方式处理。
表 4-1 不同类型接口对数据帧的处理方式

| 接口类型 | 接收帧处理过程 | 发送帧处理过程 |
|---|---|---|
| Access 接口 | 判断数据帧的VLAN Tag： ● 无Tag，则添加本接口PVID Tag。 ● 有Tag，若Tag与PVID Tag相同，则允许该VLAN帧进入，否则丢弃。 | 先剥离帧的PVID Tag，然后再发送。 |

| 接口类型 | 接收帧处理过程 | 发送帧处理过程 |
|---|---|---|
| Trunk接口 | 判断数据帧VLAN Tag： ● 无Tag，则添加本接口PVID Tag。当PVID 在允许通过的VLAN ID列表里时，则允许该VLAN帧进入，否则丢弃。 ● 有Tag，当该数据帧的VLAN ID在允许通过的VLAN ID列表里时，则允许该VLAN 帧进入，否则丢弃。 | 判断VLAN在本接口的属性： ● 如果是接口的PVID Tag，且是该接口允许通过的VLAN ID时，先剥离帧的PVID Tag，然后再发送。 ● 如果不是接口的PVID Tag，且是该接口允许通过的VLAN ID时，则直接发送。否则丢弃。 |
| Hybrid 接口 | 判断数据帧VLAN Tag： ● 无Tag，则添加本接口PVID Tag。当PVID 在允许通过的VLAN ID列表里时，则允许该VLAN帧进入，否则丢弃。 ● 有Tag，当该数据帧的VLAN ID在允许通过的VLAN ID列表里时，则允许该VLAN 帧进入，否则丢弃。说明 Trunk接口和Hybrid接口对接收到的数据帧的处理规则是一样的。 | 判断接口是否允许该数据帧通过： ● 如果允许，则发送该数据帧。发送时，可以通过命令设置发送时是否携带VLAN Tag。 ● 如果不允许，直接丢弃。 |

#### 4.2.5 LNP基本原理

定义链路类型协商协议LNP（Link-type Negotiation Protocol）用来动态协商以太网接口的链路类型为Access或者Trunk。
● 以太网接口的链路类型协商为Access，缺省情况下加入VLAN1。
● 以太网接口的链路类型协商为Trunk，缺省情况下加入VLAN1～4094。
产生背景当前，设备支持的以太网接口的链路类型有：Access、Hybrid、Trunk和QinQ。这四种接口的链路类型分别用于不同的网络位置，均由手工配置指定。如果网络拓扑变更，以太网接口的链路类型也需要重新配置，配置较为繁琐。为了简化用户配置，可通过LNP配置以太网接口的链路类型自协商功能，自动协商出接口的链路类型为Access或者Trunk，并加入相应VLAN。
实现过程当图4-3网络中二层设备连接成功后，设备接口物理状态为Up。经过LNP协商后，DeviceD、DeviceE、DeviceF、DeviceG上连接终端的接口以Access类型加入缺省VLAN1，Device之间互连的接口以Trunk类型允许所有VLAN通过。

图 4-3 LNP 典型应用组网图
● LNP的协商条件LNP在原有的接口链路类型Access、Hybrid、Trunk和QinQ基础上，新增了以下两种：
– Negotiation-desirable：主动发送LNP报文。
– Negotiation-auto：不会主动发送LNP报文。
当LNP功能使能时，触发LNP协商需要满足如下条件之一：
– 收到对端发送的LNP报文。
– 本端的接口状态或接口类型等配置发生变化。
说明
● 由于协商为Trunk类型的接口缺省会加入所有VLAN，建议配置环网协议来破除环路。
● 如果二层网络中部署了环网协议STP/RSTP/MSTP/VBST等，无论接口是否阻塞，LNP均可协商成功。
● LNP协商原则二层以太网接口的链路类型决定了协商的结果。在二层接口物理状态为Up条件下，LNP协商原则如表4-2所示。

表 4-2 LNP 协商原则

| 本端接口的链路类型 | 对端接口的链路类型（协商状态） | 本端协商结果 | 对端最终状态 |
|---|---|---|---|
| Negotiation- desirable/ Negotiation-auto | Access(使能LNP 协商) | Access | Access |
|  | Hybrid(使能LNP 协商) | Trunk | Hybrid |
|  | QinQ(使能LNP协商) | Access | QinQ |
|  | Trunk(使能LNP协商) | Trunk | Trunk |
|  | 不支持LNP协商或者去使能LNP协商 | Access | 接口的链路类型不确定 |
| Negotiation- desirable | Negotiation- desirable | Trunk | Trunk |
|  | Negotiation-auto | Trunk | Trunk |
| Negotiation-auto | Negotiation-auto | Access | Access |

LNP协议协商依赖本端和对端的正常通信。当设备出现通信延迟等问题，可能导致接口的链路类型协商错误。LNP协商经过三次正常通信后，接口的链路类型才会进入协商的稳态，否则处于协商态继续保持协商。在接口的链路类型进入稳态前，接口处于阻塞状态不参与报文转发，因此避免了报文转发的震荡或错误。
VCMP（VLAN Central Management Protocol，VLAN集中管理协议）域名会影响LNP协商，只有链路两端域名一致（都非空，且相同）或至少一端域名为空时能成功协商为Trunk，否则协商为Access。
说明
● Eth-Trunk接口的成员口配置不对称（例如成员端口数不一致）时，无法保证LNP可以协商成功。
● 如果二层接口已经通过配置设置了接口链路类型Access、Hybrid、Trunk或QinQ，即使已开启LNP功能，该二层接口的接口链路类型也不受LNP协商结果影响，保持设置的类型不变。
● 协商失败时，接口的链路类型为Access。

#### 4.2.6 同一VLAN内的互通原理

同设备 VLAN 内互通如图4-4所示，用户主机Host1和Host2连接在同台设备上，属于同一VLAN2，且位于相同网段，连接接口均设置为 Access 接口。

图 4-4 同设备 VLAN 内互通当用户主机 Host1 发送报文给用户主机 Host2 时，报文的发送过程如下（假设 DeviceA还未建立任何转发表项）。
1. Host1判断目的IP地址跟自己的IP地址在同一网段，于是发送ARP广播请求报文获取目的主机Host2的MAC地址，报文目的MAC地址填写全F，目的IP地址为Host2的IP地址10.1.1.3。
2. 报文到达DeviceA的接口interface1，发现是Untagged帧，给报文添加VID=2的Tag（Tag的VID=接口的PVID），然后将报文的“源MAC地址+VID”与接口的对应关系（00e0-fc00-1111, 2, interface1）添加进MAC表。
3. 在所有允许VLAN2通过的接口（本例中接口为interface2）广播该报文。
DeviceA的接口interface2在发出ARP请求报文前，根据接口配置，剥离VID=2的
4.
Tag。
5. Host2收到该ARP请求报文，将Host1的MAC地址和IP地址对应关系记录ARP表。
然后比较目的IP与自己的IP，发现跟自己的相同，就发送ARP响应报文，报文中封装自己的MAC地址00e0-fc00-2222，目的IP为Host1的IP地址10.1.1.2。
6. DeviceA的接口interface2收到ARP响应报文后，同样给报文添加VID=2的Tag。
7. DeviceA将报文的“源MAC地址+VID”与接口的对应关系（00e0-fc00-2222, 2, interface2）添加进MAC表，然后根据报文的“目的MAC地址+VID”（00e0- fc00-1111, 2）查找MAC地址表，由于前面已记录，查找成功，向出接口interface1 转发该 ARP 响应报文。
8. DeviceA向出接口interface1转发前，同样根据接口配置剥离VID=2的Tag。
9. Host1收到Host2的ARP响应报文，将Host2的MAC地址和IP地址对应关系记录ARP表。
跨设备 VLAN 内互通如图4-5所示，用户主机Host1和Host2连接在不同的设备上，属于同一个VLAN2，且位于相同网段。为了识别和发送跨越设备的数据帧，设备与设备间通过干道链路连接，且允许携带VLAN2的报文通过。
当同一VLAN的用户处于不同网段时，无法通过DeviceA与DeviceB直接进行二层互通。
可借助VLANIF技术实现三层互通，其互通原理与“跨设备VLAN间互通（VLANIF接口）”原理类似，不再赘述。

图 4-5 跨设备 VLAN 内互通当用户主机Host1发送报文给用户主机Host2时，报文的发送过程如下（假设DeviceA和 DeviceB 上还未建立任何转发表项）。
Host1判断目的IP地址跟自己的IP地址在同一网段，于是发送ARP广播请求报文获
1.
取目的主机Host2的MAC地址，报文目的MAC地址填写全F，目的IP地址为Host2的IP地址10.1.1.3。
2. 报文到达设备的接口interface1，发现是Untagged帧，给报文添加VID=2的Tag（Tag的VID=接口的PVID），然后将报文的“源MAC地址+VID”与接口的对应关系（00e0-fc00-1111, 2, interface1）添加进MAC表。
3. 根据报文“目的MAC地址+VID”查找DeviceA的MAC表，没有找到，于是报文被广播到DeviceA的interface2接口。
4. DeviceA的interface2接口在发出ARP请求报文前，因为接口的PVID=1，与报文的VID不相同，且该报文的VID在该端口是放通的，所以直接透传该报文到DeviceB的interface2接口，不剥离报文的Tag，只有接口的PVID和报文的VID相同，发送时才会把报文的VID剥掉。
5. DeviceB的interface2接口收到该报文后，判断报文的Tag中的VID=2是接口允许通过的VLAN，接收该报文。
6. 根据报文“目的MAC地址+VID”查找DeviceB的MAC表，没有找到，于是报文被广播到DeviceB的interface1接口。
7. DeviceB的接口interface1在发出ARP请求报文前，根据接口配置，剥离VID=2的Tag。
8. Host2收到该ARP请求报文，将Host1的MAC地址和IP地址对应关系记录ARP表。
然后比较目的IP与自己的IP，发现跟自己的相同，就发送ARP响应报文，报文中封装自己的MAC地址00e0-fc00-2222，目的IP为Host1的IP地址10.1.1.2。
9. DeviceB的接口interface1收到ARP响应报文后，同样给报文添加VID=2的Tag。
10. DeviceB向自己的出接口interface2转发Host2的ARP响应报文前，因为接口interface2为Trunk接口且PVID=1，与报文的VID不相同，所以直接透传报文到DeviceA的interface2接口，不剥离报文的Tag。
11. DeviceA 的 interface2 接口收到 Host2 的 ARP 响应报文后，判断报文的 Tag 中的VID=2是接口允许通过的VLAN，接收该报文。
12. DeviceA将报文的“源MAC地址+VID”与接口的对应关系（00e0-fc00-2222, 2, interface2）添加进MAC表，然后根据报文的“目的MAC地址+VID”（00e0-

fc00-1111, 2）查找MAC地址表，由于前面已记录，查找成功，向出接口interface1转发该ARP响应报文。
13. DeviceA向出接口interface1转发前，同样根据接口配置，剥离VID=2的Tag。
14. Host1收到Host2的ARP响应报文，将Host2的MAC地址和IP地址对应关系记录ARP表。
由此可见，干道链路除了支持传输多个VLAN的数据帧外，还起到透传VLAN的作用，即干道链路上，数据帧只会转发，不会发生Tag的添加或剥离。

#### 4.2.7 不同VLAN间的互通原理

同设备 VLAN 间互通（VLANIF 接口）
如图4-6所示，用户主机Host1和Host2连接在同台设备上，分别属于VLAN2和VLAN3，并位于不同的网段。在DeviceA上分别创建VLANIF2和VLANIF3并配置其IP地址，然后将用户主机的缺省网关设置为所属VLAN对应VLANIF接口的IP地址。
图 4-6 通过 VLANIF 实现同设备 VLAN 间互访当用户主机Host1发送报文给用户主机Host2时，报文的发送过程如下（假设DeviceA上还未建立任何转发表项）。
Host1判断目的IP地址跟自己的IP地址不在同一网段，因此，它发出请求网关MAC
1.
地址的ARP请求报文，目的IP为网关IP地址10.1.1.1，目的MAC为全F。
2. 报文到达DeviceA的接口interface1，DeviceA给报文添加VID=2的Tag（Tag的VID= 接口的 PVID ），然后将报文的“源 MAC 地址 +VID+ 接口”的对应关系（00e0-fc00-1111， 2，interface1）添加进MAC表。
3. DeviceA检查报文是ARP请求报文，且目的IP是自己VLANIF2接口的IP地址，给Host1应答，并将VLANIF2接口的MAC地址00e0-fc00-3333封装在应答报文中，应答报文从interface1发出。同时，DeviceA会将Host1的IP地址与MAC地址的对应关系记录到ARP表。
4. Host1收到DeviceA的应答报文，将DeviceA的VLANIF2接口的IP地址与MAC地址对应关系记录到自己的ARP表中，并向DeviceA发送目的MAC为00e0- fc00-3333、目的IP为Host2的IP地址 10.2.2.2的报文。
5. 报文到达 DeviceA 的接口 interface1 ，同样给报文添加 VID=2 的 Tag 。
6. DeviceA根据报文的“源MAC地址+VID+接口”的对应关系更新MAC表，并比较报文的目的MAC地址与VLANIF2的MAC地址，发现两者相等，进行三层转发，根据目的IP查找三层转发表，没有找到匹配项，上送CPU查找路由表。

7. CPU根据报文的目的IP去找路由表，发现匹配了一个直连网段（VLANIF3对应的网
段），于是继续查找ARP表，没有找到，DeviceA会在目的网段对应的VLAN3的所
有接口发送ARP请求报文，目的IP是10.2.2.2，从接口interface2发出。
Host2收到ARP请求报文，发现请求IP是自己的IP地址，就发送ARP应答报文，将
8.
自己的MAC地址包含在其中。同时，将VLANIF3的MAC地址与IP地址的对应关系
记录到自己的ARP表中。
DeviceA的接口interface2收到Host2的ARP应答报文后，给报文添加VID=3的
9.
Tag，并将Host2的MAC和IP的对应关系记录到自己的ARP表中。然后，将Host1
的报文转发给Host2，发送前，同样剥离报文中的Tag。同时，将Host2的IP地
址、MAC地址、VID及出接口的对应关系记录到三层转发表中。
至此，Host1完成对Host2的单向访问。Host2访问Host1的过程与此类似。
跨设备 VLAN 间互通（VLANIF 接口）
由于VLANIF接口的IP地址只能在设备上生成直连路由，当不同VLAN的用户跨多台设备
互访时，除配置VLANIF接口的IP地址外，还需要配置静态路由或运行动态路由协议。
如图4-7所示，用户主机Host1和Host2连接在不同的设备上，分别属于VLAN2和
VLAN3 ，并位于不同的网段。主机与设备之间使用 Access 接口，设备之间使用 Trunk 接
口。在DeviceA上分别创建VLANIF2和VLANIF4，配置其IP地址为10.1.1.1和10.1.4.1；
在DeviceB上分别创建VLANIF3和VLANIF4，配置其IP地址为10.1.2.1和10.1.4.2，并在
DeviceA和DeviceB上分别配置静态路由。DeviceA上静态路由的目的网段是
10.1.2.0/24，下一跳是10.1.4.2；DeviceB上静态路由的目的网段是10.1.1.0/24，下一
跳是10.1.4.1。
图 4-7 通过 VLANIF 实现跨设备 VLAN 间互访
当用户主机Host1发送报文给用户主机Host2时，报文的发送过程如下（假设DeviceA
和DeviceB上还未建立任何转发表项）。
1. 与同设备VLAN间互通（VLANIF接口）的步骤1～6一样，经过“Host1比较目的
IP地址—>Host1查ARP表—>Host1获取网关MAC地址—>Host1将发给Host2的报
文送到DeviceA—>DeviceA查MAC表—>DeviceA查三层转发表”的过程，
DeviceA 上送 CPU 查找路由表。
2. DeviceA的CPU根据报文的目的IP 10.1.2.2去找路由表，发现匹配了一条静态路
由，目的网段是10.1.2.0/24的下一跳IP地址为10.1.4.2，于是继续查找ARP表，没
有找到，DeviceA会在下一跳IP地址对应的VLAN4的所有接口广播ARP请求报文，

目的IP是10.1.4.2。报文从DeviceA的接口interface2发出前，根据接口配置，发送该ARP请求报文到DeviceB的interface2接口，不会剥除报文的Tag。
3. ARP请求报文到达DeviceB后，发现目的IP为VLANIF4接口的IP地址，给DeviceA回应，填写VLANIF4接口的MAC地址。
4. DeviceB的ARP响应报文从其interface2直接发送到DeviceA，DeviceA接收后，记录VLANIF4的MAC地址与IP地址的对应关系到ARP表项。
5. DeviceA将Host1的报文转发给DeviceB，报文的目的MAC修改为DeviceB的VLANIF4接口的MAC地址，源MAC地址修改自己的VLANIF4接口的MAC地址，并将刚用到的转发信息记录在三层转发表中（10.1.2.0/24， 下一跳IP的MAC地址，出口VLAN， 出接口）。同样，报文是直接转发到DeviceB的interface2接口。
6. DeviceB收到DeviceA转发的Host1的报文后，与同设备VLAN间互通（VLANIF接口）的步骤6～9一样，经过“查MAC表—>查三层转发表—>送CPU—>匹配直连路由—>查ARP表并获取Host2的MAC地址—>将Host1的报文转发给Host2”的过程，同时将Host2的IP地址、MAC地址、出口VLAN、出接口记录到三层转发表项。
至此，Host1完成对Host2的单向访问。Host2访问Host1的过程与此类似。
同设备 VLAN 间互通（三层子接口）
说明该特性仅S6780-H、S6750-H、S6750-S、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755-
H、S5755-S、S5732-H-V2系列支持。
如图4-8所示，用户主机属于不同的VLAN，并位于不同的网段。其中，Host1和Host2属于VLAN2，Host3和Host4属于VLAN3，DeviceA通过以太网接口interface1与DeviceB相连。在DeviceA的interface1上创建2个子接口interface1.1和interface1.2，并配置802.1Q封装与VLAN2和VLAN3分别对应。配置子接口的IP地址，保证两个子接口对应的IP地址路由可达，并将用户设备的缺省网关设置为所属VLAN对应子接口的IP地址。
图 4-8 通过子接口实现 VLAN 间的通信

当用户主机Host1发送报文给用户主机Host3时，报文的发送过程如下。（假设DeviceA上还未建立任何转发表项）。
1. Host1判断Host3的IP地址跟自己的IP地址不在同一网段，因此，它发出请求网关MAC地址的ARP请求报文，目的IP为网关IP地址10.1.1.1，目的MAC为全F。
2. 报文到达DeviceA的接口interface1，DeviceA将“源MAC地址+VID+接口”的对应关系（00e0-fc00-1111，2，interface1）添加进MAC表。
3. DeviceA检查报文是ARP请求报文，且目的IP是自己interface1.1接口的IP地址，给Host1应答，并将VLAN2对应的子接口interface1.1的MAC地址00e0-fc00-3333封装在应答报文中。同时，DeviceA会将Host1的IP地址与MAC地址的对应关系记录到ARP表。
4. Host1收到DeviceA的应答报文，将DeviceA的子接口interface1.1的IP地址与MAC地址对应关系记录到自己的ARP表中，并向DeviceA发送目的MAC为00e0- fc00-3333、目的IP为Host3的IP地址10.2.2.2的报文。
5. 报文到达DeviceA的接口interface1，DeviceA根据报文的“源MAC地址+VID+接口”的对应关系更新MAC表，并比较报文的目的MAC地址与子接口interface1.1的MAC地址，发现两者相等，进行三层转发。由于Host3的IP地址为直连路由，报文将通过VLAN3关联的子接口interface1.2进行转发。
6. DeviceA作为VLAN3内主机的网关，会在目的网段对应的VLAN3的所有接口发送ARP请求报文，目的IP地址是10.2.2.2。
Host3收到ARP请求报文，发现请求IP地址是自己的IP地址，就发送ARP应答报
7.
文，将自己的MAC地址包含在其中。同时，将VLAN3对应的子接口interface1.2的MAC地址与IP地址的对应关系记录到自己的ARP表中。
8. DeviceA收到Host3的ARP应答报文后，并将Host3的MAC和IP的对应关系记录到自己的ARP表中。然后，将Host1的报文转发给Host3。同时，将Host3的IP地址、MAC地址、VID及出接口的对应关系记录到三层转发表中。
至此，Host1完成对Host3的单向访问。Host3访问Host1的过程与此类似。

### 4.3 VLAN配置注意事项

License 依赖VLAN无需License许可即可使用。
硬件依赖表 4-3 支持本特性的硬件

| 系列 | 支持产品 |
|---|---|
| S6750-H | S6750-H36C，S6750-H48Y8C |
| S6730E-H-V2 | S6730E-H6FX4Y2CZ-V2 |
| S1730S-S3 | S1730S-S24P4S-A3，S1730S-S24P4X-A3， S1730S-S24T4S-QA3，S1730S-S24T4X-QA3， S1730S-S48P4S-A3，S1730S-S48T4S-A3， S1730S-S48T4X-A3，S1730S-S8P4X-QA3， S1730S-S8T4X-QA3 |

| 系列 | 支持产品 |
|---|---|
| S5735-S-V2 | S5735-S24HS4XE-V2，S5735-S24P4XE-V2， S5735-S24P4XEZ-V2，S5735-S24P8J4XEZ-V2， S5735-S24PN4XE-V2，S5735-S24ST4XE-V2， S5735-S24T4XE-C-V2，S5735-S24T4XE-V2， S5735-S24T4XEZ-V2，S5735-S24T8J4XE-XA-V2， S5735-S24T8J4XEZ-V2，S5735-S24U4XE-V2， S5735-S48HS4XE-V2，S5735-S48P4XE-V2， S5735-S48P4XEZ-V2，S5735-S48PN4XE-V2， S5735-S48S4XE-V2，S5735-S48T4XE-C-V2， S5735-S48T4XE-V2，S5735-S48T4XE-XA-V2， S5735-S48T4XEZ-V2，S5735-S48U4XE-V2 |
| S5735E-S-V2 | S5735E-S24HS4XE-V2，S5735E-S48HS4XE-V2 |
| S5735S-S3 | S5735S-S24P4X-A3，S5735S-S48P4X-A3 |
| S6750E-S | S6750E-S16X10Y2CZ，S6750E-S24T16X8Y2CZ |
| S5735I-L-V2 | S5735I-L10T4X-A-V2，S5735I-L8P4X-A-V2 |
| S6730-H-V2 | S6730-H24X6C-V2，S6730-H28X6CZ-V2，S6730- H48X6C-TV2，S6730-H48X6C-V2，S6730- H48X6CZ-V2，S6730-H48Y6C-TV2，S6730- H48Y6C-V2，S6730-H6FX4Y2CZ-V2 |
| S5735I-H-V2 | S5735I-H24U8S4XE-QA-V2，S5735I-H8T2XN- V2，S5735I-H8T4S2XN-V2，S5735I-H8U2XN-V2 |
| S6750-S | S6750-S16X10Y2CZ，S6750-S16X8YZ，S6750- S24T16X8Y2CZ |
| S5735S-L3 | S5735S-L24P4S-A3，S5735S-L24P4XE-A3， S5735S-L24PN4XE-A3，S5735S-L24ST4X-A3， S5735S-L24T4S-QA3，S5735S-L24T4X-QA3， S5735S-L24T8J4XE-A3，S5735S-L48P4S-A3， S5735S-L48P4XE-A3，S5735S-L48PN4XE-A3， S5735S-L48S4X-A3，S5735S-L48T4S-A3，S5735S- L48T4XE-A3，S5735S-L8P4X-QA3，S5735S- L8T4X-QA3 |
| S5755-H | S5755-H24HB2Y2CZ，S5755-H24N4Y-A，S5755- H24P4Y2CZ，S5755-H24T4Y2CZ，S5755- H24U4Y2CZ，S5755-H24UM4Y2CZ，S5755- H24UN4Y2CZ，S5755-H24UTM4X4Y2C，S5755- H48N4Y-A，S5755-H48P4Y2CZ，S5755- H48T4Y2CZ，S5755-H48T4Y2CZ-B，S5755- H48U4Y2CZ，S5755-H48UM4Y2CZ，S5755- H48UN4Y2CZ，S5755-H48UTM4X4Y2C |
| S5735R-S-V2 | S5735R-S24P4X-V2，S5735R-S24T8J4X-XA-V2， S5735R-S48P4X-V2，S5735R-S48T4X-XA-V2 |
| S6780-H | S6780-H4Z |

| 系列 | 支持产品 |
|---|---|
| S5735E-L-V2 | S5735E-L16LP2UM2X-QA-V2，S5735E-L16LP2X- QA-V2，S5735E-L24P4S-A-V2，S5735E-L24P4XE- A-V2，S5735E-L24ST4XE-A-V2，S5735E- L24T4XE-A-V2，S5735E-L48LP4S-A-V2，S5735E- L48LP4XE-A-V2，S5735E-L48S4XE-A-V2， S5735E-L48T4XE-A-V2，S5735E-L8P4X-QA-V2， S5735E-L8T4X-QA-V2 |
| S5755-S | S5755-S24P8J8YZ，S5755-S24P8Y，S5755- S24T8J8YZ，S5755-S24T8Y，S5755-S24U8J8YZ， S5755-S24U8Y，S5755-S48P8Y，S5755- S48P8YZ，S5755-S48T8Y，S5755-S48T8YZ， S5755-S48U8Y，S5755-S48U8YZ |
| S5735R-L-V2 | S5735R-L16LP2S-QA-V2，S5735R-L16LP2UM2X- QA-V2，S5735R-L16LP2X-QA-V2，S5735R- L16T4S-A-V2，S5735R-L16T4X-QA-V2，S5735R- L24P4S-A-V2，S5735R-L24P4X-A-V2，S5735R- L24T4S-A-V2，S5735R-L24T4X-QA-V2，S5735R- L48LP4S-A-V2，S5735R-L48LP4X-A-V2，S5735R- L48P4X-A-V2，S5735R-L48T4S-A-V2，S5735R- L48T4X-A-V2，S5735R-L8P4S-A-V2，S5735R- L8P4X-QA-V2，S5735R-L8T4S-A-V2，S5735R- L8T4X-QA-V2 |
| S5735-L-V2 | S5735-L10T4X-A-V2，S5735-L14P2S-QA-V2， S5735-L16LP2UM2X-QA-V2，S5735-L16LP2X-QA- V2，S5735-L16P2UM2X-QA-V2，S5735-L16T4S- A-V2，S5735-L16T4X-QA-V2，S5735- L24LU8S4XE-QA-V2，S5735-L24P4S-A-V2， S5735-L24P4XE-A-V2，S5735-L24PN4XE-A-V2， S5735-L24ST4XE-A-V2，S5735-L24T4S-A-V2， S5735-L24T4X-QA-V2，S5735-L24T4XE-A-V2， S5735-L24T4XE-D-V2，S5735-L24T8J4XE-A-V2， S5735-L48LP4S-A-V2，S5735-L48LP4XE-A-V2， S5735-L48LPN4XE-A-V2，S5735-L48P4XE-A-V2， S5735-L48PN4XE-A-V2，S5735-L48S4X-A-V2， S5735-L48S4XE-A-V2，S5735-L48T4S-A-V2， S5735-L48T4XE-A-V2，S5735-L48T4XE-D-V2， S5735-L8P2T4X-A-V2，S5735-L8P4S-A-V2， S5735-L8P4X-QA-V2，S5735-L8T4S-A-V2， S5735-L8T4X-QA-V2 |
| S5735I-S-V2 | S5735I-S16T2S4XN-V2，S5735I-S16T8S4XE-QD- V2，S5735I-S24T4XE-V2，S5735I-S24T8S4XE-QA- V2，S5735I-S24U4XE-V2，S5735I-S48T4XE-V2， S5735I-S8T4SN-V2，S5735I-S8T4XN-V2，S5735I- S8T8P2S4XN-V2，S5735I-S8U2XN-V2，S5735I- S8U4XN-V2 |

| 系列 | 支持产品 |
|---|---|
| S5732-H-V2 | S5732-H24S4X6QZ-TV2，S5732-H24S4X6QZ- V2，S5732-H24UM4Y2CZ-KV2，S5732- H24UM4Y2CZ-V2，S5732-H44S4X6QZ-V2， S5732-H48UM4Y2CZ-KV2，S5732-H48UM4Y2CZ- TV2，S5732-H48UM4Y2CZ-V2 |

查询工具如需了解硬件规格、产品部件的配套关系，请点击硬件中心进行查询；如需了解关键规格、全量软件规格，请点击规格查询进行查询。
特性限制表 4-4 本特性的使用限制

| 特性 | 特性限制 |
|---|---|
| VLAN基础 | 不允许在VLAN Stacking的外层VLAN的VLANIF接口上配置IP地址来接入IP业务。不支持在vlan stacking的外层vlan的vlanif接口上配置IP地址来接入IP业务 |
| VLAN基础 | 使用VLAN1时要注意如下事项： - 建议不要使用VLAN1作为管理VLAN或者业务VLAN。 - 对于不需要加入VLAN1的接口要及时退出VLAN1，以避免环路。但 Trunk接口上一般要保持允许VLAN1通过，否则，一些通过VLAN1传输的协议报文会被Trunk接口错误丢弃而引起故障。这种情况下，需要采取措施规避允许VLAN1通过所带来的潜在安全风险。 - 在Eth-Trunk、环形组网环境下建议接口退出VLAN1。 - 在与接入设备对接时，接入设备的上行接口建议不要透传VLAN1，防止在VLAN1中产生广播风暴。 - 接口绑定VLANIF接口进行三层转发时，建议接口从VLAN1中退出，避免形成VLAN1内的二层环路。 |
| VLAN基础 | 请用户独立规划业务VLAN和管理VLAN，以便业务VLAN上发生的任何广播风暴不会影响到设备的管理。 |
| VLAN基础 | 对于产品S1730S-S3系列，S5735S-L3系列，S5735S-S3系列，S5735I- H-V2系列，S5735I-S16T8S4XE-QD-V2，S5735I-S8U2XN-V2， S5735I-S24T8S4XE-QA-V2，S5735I-S48T4XE-V2： VLAN内流量在出端口VLAN成员检查时被丢弃时会占用出端口带宽。 VLAN内BUM流量在出端口源剪枝时被丢弃时会占用出端口带宽。 |
| VLAN基础 | 基于子网划分的VLAN做三层转发时，需要配置接口的PVID与关联子网的VLAN ID相同。 |

| 特性 | 特性限制 |
|---|---|
| VLAN基础 | 1、MuxVLAN不支持叠加VLAN切片，一个端口上同时有MuxVLAN和 VLAN切片配置时，VLAN切片的功能不生效。 2、VLAN划分不支持叠加VLAN切片，同一个端口叠加VLAN划分业务后，VLAN切片功能不生效。 3、Voice-vlan不支持叠加VLAN切片，同一个端口叠加Voice-vlan业务后，切片功能不生效。 |
| VLAN基础 | 对于S6750-H系列，S6730E-H-V2系列，S6750E-S系列，S5755-H系列，S6780-H系列，S5732-H-V2系列，S6730-H-V2系列，S5755-S系列，S6750-S系列：由于芯片资源限制，VLAN流量统计和二层子接口流量统计互斥。 |
| VLAN基础 | 对于S1730S-S3系列，S5735S-L3系列，S5735-S-V2系列，S5735E-S- V2系列，S5755-H系列，S5735R-S-V2系列，S5735E-L-V2系列， S5735S-S3系列，S5755-S系列，S5735R-L-V2系列，S5735-L-V2系列，S5735I-S-V2系列，S5735I-L-V2系列，S5735I-H-V2系列：先判断是否为隧道报文（iptnl或srv6的隧道报文），如是要先做异常检查，如检查version版本号不对，就报错误丢弃。 1、SRV6隧道： nexthead 默认值为 59\143\41\4 （支持可配） 2、IP Tunl 隧道： protocol值为 29（不支持可配） |
| VLAN基础 | 对于S5735R-L-V2系列，S1730S-S3系列，S5735-L-V2系列，S5735S- L3系列，S5735-S-V2系列，S5735E-S-V2系列，S5735I-S-V2系列， S5735R-S-V2系列，S5735I-L-V2系列，S5735E-L-V2系列，S5735S-S3 系列，S5735I-H-V2系列：设备不支持外层VLAN为Tag 0的两层VLAN报文，收到此类报文后会丢弃。 |
| VLAN基础 | 对于S5755-S系列： port discard tagged-packet命令会丢弃外层VLAN为Tag 0的两层VLAN 报文。 |
| VLAN基础 | 实际运用中，Trunk接口需要透传哪些VLAN就透传哪些VLAN，请不要用port trunk allow-pass vlan all。 |
| MUX VLAN | MUX VLAN复制的MAC表项被命中之后，原始的MAC表项因没有流量触发而老化，老化时同步会删除复制的MAC，已知单播变成广播。对于产品S5732-H-V2系列，S5755-S系列，S6730E-H-V2系列， S6750-H系列，S6750-S系列，S6750E-S系列，S6780-H系列，S5755- H24N4Y-A，S5755-H24P4Y2CZ，S5755-H24T4Y2CZ，S5755- H24U4Y2CZ，S5755-H24UN4Y2CZ，S5755-H24UTM4X4Y2C， S5755-H48N4Y-A，S5755-H48P4Y2CZ，S5755-H48T4Y2CZ，S5755- H48U4Y2CZ，S5755-H48UN4Y2CZ，S5755-H48UTM4X4Y2C， S6730-H24X6C-V2，S6730-H28X6CZ-V2，S6730-H48X6C-TV2， S6730-H48X6C-V2，S6730-H48X6CZ-V2，S6730-H48Y6C-TV2， S6730-H48Y6C-V2： M-LAG叠加MUX VLAN，单归变双归时反向同步时存在暂态的MUX MAC删除行为。 |

| 特性 | 特性限制 |
|---|---|
| MUX VLAN | 不能在同一接口上配置MUX VLAN和基于VLAN ID的灵活QinQ功能。 |
| MUX VLAN | 针对MUX VLAN的流量统计功能限制： 1、流量从principal vlan走向group/seperate vlan时，流量在principal vlan中统计，group/seperate vlan上统计不到。 2、流量在group/seperate vlan中统计，principal vlan上统计不到。 |
| MUX VLAN | 如果指定VLAN已经用于Group VLAN或Separate VLAN，那么该VLAN 不能再用于创建VLANIF接口，或者在VLAN Mapping、VLAN Stacking、Super-VLAN、Sub-VLAN的配置中使用。可以为Principal VLAN创建VLANIF接口。 |
| MUX VLAN | 每组MUX VLAN所有成员VLAN必须在同一个STP实例中否则会导致流量不通或者成环。对于vlan mapping/stacking同样有此约束。 |
| MUX VLAN | 端口加入主VLAN、隔离型从VLAN、互通型从VLAN而不使能MUX VLAN是用于设备之间级联，需要对该接连接口上流量学习MAC，否则会导致流量广播。 |
| MUX VLAN | MUX VLAN功能与下面这些功能不支持叠加组合：对于产品S5735I-H-V2系列，S5735I-S16T2S4XN-V2，S5735I- S16T8S4XE-QD-V2，S5735I-S24T8S4XE-QA-V2，S5735I-S48T4XE- V2，S5735I-S8T8P2S4XN-V2，S5735I-S8U2XN-V2： 1、端口安全功能、基于端口的MAC-Limit、基于VLAN的MAC-Limit。 2、Separate VLAN（隔离型从VLAN）不支持叠加NAC功能；Principal VLAN（主VLAN）和Group VLAN（互通型从VLAN）支持叠加NAC功能。对于产品S1730S-S3系列，S5732-H-V2系列，S5735-L-V2系列， S5735-S-V2系列，S5735E-L-V2系列，S5735E-S-V2系列，S5735I-L-V2 系列，S5735R-L-V2系列，S5735R-S-V2系列，S5735S-L3系列， S5735S-S3系列，S5755-H系列，S5755-S系列，S6730-H-V2系列， S6730E-H-V2系列，S6750-H系列，S6750-S系列，S6750E-S系列， S6780-H系列，S5735I-S24T4XE-V2，S5735I-S24U4XE-V2，S5735I- S8T4SN-V2，S5735I-S8T4XN-V2，S5735I-S8U4XN-V2： 1、端口安全功能、基于端口的MAC-Limit、基于VLAN的MAC-Limit。 2、VBST功能。 3、NAC功能。 |
| MUX VLAN | 对于S5755-S系列：三层环网倒换时，MuxVlan的VLAN隔离功能会短时间不生效。 |
| VLAN Mapping | 不支持在Vlan Mapping对应的Vlanif接口上配置IP地址来接入IP业务 |
| VLAN Mapping | <1>N:1场景命令行拆分会造成流量短时断流； <2>基于vlan范围段配置 N:1场景，当CIB资源已超限时，取消其中一个vlan的映射关系，拆分后的命令行可能功能不生效; |

| 特性 | 特性限制 |
|---|---|
| VLAN Mapping | VLAN Mapping不支持三层及以上VLAN tag的变换。 |
| VLAN Mapping | 对于S6750-H系列，S6730E-H-V2系列，S6750E-S系列，S5755-H系列，S6780-H系列，S5732-H-V2系列，S6730-H-V2系列，S5755-S系列，S6750-S系列：同时配置VLAN-Mapping业务和EVC-BD业务，EVC-BD业务部分可能功能受损。对于产品S6750-H系列，S6780-H系列：相同芯片下同时配置VLAN-Mapping业务和EVC-BD业务，且配置的 VLAN段个数总数大于芯片VLAN-Range规格（一个芯片VLAN-Range规格为128）（VLAN-Mapping业务配置的VLAN段的VLAN个数>=4） （EVC-BD业务配置的VLAN段个数>64），带配置升级到新版本后， EVC-BD业务部分可能功能受损。对于产品S5732-H-V2系列，S5755-H系列，S5755-S系列，S6730-H- V2系列，S6730E-H-V2系列，S6750-S系列，S6750E-S系列：相同主接口下同时配置VLAN-Mapping业务和EVC-BD业务，且配置的 VLAN段个数总数大于主接口VLAN-Range规格（一个主接口VLAN- Range规格为8）（VLAN-Mapping业务配置的VLAN段的VLAN个数 >=4），带配置升级到新版本后,EVC-BD业务部分可能功能受损。 |
| VLAN Mapping | 同一个端口不支持对同一个VLAN配置VLAN Mapping和Voice VLAN。 |
| VLAN Mapping | 对于S6750-H系列，S6730E-H-V2系列，S6750E-S系列，S5755-H系列，S6780-H系列，S5732-H-V2系列，S6730-H-V2系列，S5755-S系列，S6750-S系列： VLAN Mapping N:1场景不支持三层VLANIF口。 |
| VLAN Mapping | VLAN变换的资源是多个业务共享，共享业务包括VLAN Stacking、BD 子接口、MUX VLAN。 |
| VLAN Mapping | VLAN Mapping N:1不支持Eth-Trunk端口。 |
| VLAN Mapping | 正向流不学习MAC的情况下，反向流均无法正常还原 <1>N:1反向流量不支持广播、未知单播、保留组播，仅实现了二层单播互通； <2>端口安全、MAC limit、BPDU、NAC等 |
| VLAN Mapping | 配置VLAN Mapping N:1的端口下，接收VLAN不同、MAC相同的报文后，反向流量只会将报文映射为MAC学习时报文所带的VLAN。 |
| VLAN Mapping | 如果有多个VLAN映射到同一个vlan，即使有多个vlan的流变换后生成同一个MAC，BE表只保存第一个学到的MAC的原始外层vlan。 |
| VLAN Mapping | 1. 当配置N:1 VLAN Mapping时，出接口需要以Tagged的方式加入 map-vlan，VLAN Mapping才会生效。 2. VLAN Mapping支持Mapping前按照VLAN匹配，不支持8021p的方式匹配。 |

| 特性 | 特性限制 |
|---|---|
| Super VLAN | ND snooping与supper VLAN互斥 |
| QinQ | 1、端口配置vlan stacking后，对于该端口未配置stacking的原始 VLAN，默认会stacking端口的PVID。 2、端口上vlan stacking和qinq子接口配置的外层VLAN段不能重叠。 3、vlan stacking不支持和L2PT叠加，软转发只替换gmac，不支持叠加 vlan stacking。 4、协议报文中携带的vlan和stacking前的vlan一样，也不会再叠加 stacking vlan，软转发只替换gmac。 5、配置灵活QinQ功能的当前接口类型必须为Hybrid或Trunk，且只在入方向生效。 6、叠加后的外层VLAN必须存在，且当前接口必须以Untagged方式加入叠加后的stack-vlan中。 7、port vlan-stacking指定的叠加前的VLAN和QINQ二层子接口配置的外层VLAN不能重叠。 8、如果设备内部转发资源超规格，仍然可配置VLAN Stacking功能，但设备重启后，可能会发生原来不生效的VLAN Stacking配置变为生效、原来生效的VLAN Stacking配置反而不生效的情况。即在业务规格超限/ 资源超限情况下，配置恢复前后业务生效结果不保证一致。 9、端口下同时配置voice vlan和VLAN Stacking，可能会互相影响，配置时提示warning信息（对齐园区V5）。 |
| QinQ | 不支持在VLAN-Stacking对应的Vlanif接口上配置IP地址来接入IP业务 |
| QinQ | 对于S6750-H系列，S6730E-H-V2系列，S6750E-S系列，S5735S-L3系列，S5755-H系列，S6780-H系列，S5732-H-V2系列，S6730-H-V2系列，S5755-S系列，S6750-S系列：相同芯片下同时配置VLAN-Stacking业务和EVC-BD业务，且配置的 VLAN段个数总数大于芯片VLAN-Range规格，带配置升级到新版本后， EVC-BD业务部分可能功能受损。对于产品S6750-H系列，S6780-H系列：相同芯片下同时配置VLAN-Stacking业务和EVC-BD业务，且配置的 VLAN段个数总数大于芯片VLAN-Range规格（一个芯片VLAN-Range规格为128）（VLAN-Stacking业务配置的VLAN段的VLAN个数>=4） （EVC-BD业务配置的VLAN段个数>64），带配置升级到新版本后， EVC-BD业务部分可能功能受损。对于产品S5732-H-V2系列，S5735S-L3系列，S5755-H系列，S5755-S 系列，S6730-H-V2系列，S6730E-H-V2系列，S6750-S系列，S6750E- S系列：相同主接口下同时配置VLAN-Stacking业务和EVC-BD业务，且配置的 VLAN段个数总数大于主接口VLAN-Range规格（一个主接口VLAN- Range规格为8）（VLAN-Stacking业务配置的VLAN段的VLAN个数 >=4），带配置升级到新版本后,EVC-BD业务部分可能功能受损。 |

| 特性 | 特性限制 |
|---|---|
| QinQ | 接口同时配置VLAN Stacking和VLAN Mapping时，不支持VLAN Stacking后的外层VLAN连续匹配VLAN Mapping规则进行变换。例如，入方向报文为VLAN ID为3，接口下配置port vlan-stacking vlan 3 stack-vlan 4后，再配置port vlan-mapping vlan 4 map-vlan 5不生效，即配置VLAN Stacking后的外层VLAN 4不支持连续进行VLAN Mapping变换。 |
| QinQ | 对于S5755-S系列：同一个主接口下，带优先级的VLAN-stacking配置和以下配置同时存在时，带优先级的VLAN-stacking配置不生效。 1、带两层tag的VLAN-mapping； 2、qinq二层子接口； 3、qinq三层子接口。 |

### 4.4 VLAN缺省配置

VLAN参数默认缺省值如表4-5所示。
表 4-5 VLAN 参数默认缺省值

| 参数 | 缺省值 |
|---|---|
| 缺省VLAN | VLAN 1 |
| 接口链路类型 | 对于S5732-H-V2，S6780-H，S6750-H ，S6750E-S， S6750-S，S6730E-H-V2，S6730-H-V2，S5755-S， S5755-H：negotiation-desirable 对于S5735I-L-V2，S5735I-S-V2，S5735I-H-V2， S5735R-L-V2，S5735E-L-V2、S5735-L-V2，S5735R-S- V2，S5735E-S-V2，S5735-S-V2，S5735S-L3， S5735S-S3，S1730S-S3：negotiation-auto |
| VLAN Damping功能 | 未使能状态，且延迟时间为0秒 |
| VLAN的流量统计功能 | 关闭 |
| VLANIF接口的流量统计功能 | 关闭 |
| VLANIF接口变为Down的延迟时间 | 0秒 |
| VLANIF接口的MTU | 1500字节 |

### 4.5 创建和删除VLAN

背景信息VLAN 1是系统自带的VLAN，既不需要创建，也不可以删除。
操作步骤
● 创建VLAN。
a. 进入系统视图。
system-view
b. 创建VLAN并进入VLAN视图。如果VLAN已经创建，则直接进入VLAN视图。
设备的VLAN范围是1～4094（0和4095保留）。
vlan vlan-id
c. （可选）配置VLAN的描述信息。
description description缺省情况下，VLAN的描述信息中体现了VLAN的编号，例如VLAN2的描述信息是VLAN 0002。
d. （可选）配置VLAN的名称。
name vlan-name缺省情况下，VLAN没有名称。
VLAN名称配置成功后，用户可在系统视图下执行命令vlan vlan-name vlan- name，可以直接进入对应的VLAN视图。
● 批量创建VLAN。
a. 进入系统视图。
system-view
b. 批量创建VLAN。
vlan batch { vlan-id1 [ to vlan-id2 ] } &<1-10>说明如果需要在多个VLAN中配置相同的业务，可以通过临时VLAN组的方式进行批量配置。首先在系统视图下执行命令vlan range { vlan-id1 [ to vlan-id2 ] } &<1-10>，创建临时VLAN组并进入VLAN-Range视图。然后在VLAN-Range视图下配置相关业务并提交后，VLAN组中所有成员VLAN会生成对应的配置文件。
● 删除VLAN。
a. 进入系统视图。
system-view
b. 删除单个VLAN。
undo vlan vlan-id
● 批量删除VLAN。
a. 进入系统视图。
system-view
b. 批量删除 VLAN 。
undo vlan batch { vlan-id1 [ to vlan-id2 ] } &<1-10>
----结束

检查配置结果
● 执行命令display vlan [ summary ]，查看所有VLAN的信息。
● 执行命令display default-parameter vlan vlan-id，查看VLAN的缺省配置信息。

### 4.6 修改和恢复缺省VLAN

前提条件如果接口处于三层模式，则需要执行命令portswitch将接口从三层模式切换到二层模式。
仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
操作步骤
● 修改Access接口的缺省VLAN。
system-view interface interface-type interface-number port link-type access port default vlan vlan-id
● 修改Trunk接口的缺省VLAN。
system-view interface interface-type interface-number port link-type trunk port trunk pvid vlan vlan-id
● 修改Hybrid接口的缺省VLAN。
system-view interface interface-type interface-number port link-type hybrid port hybrid pvid vlan vlan-id
● 恢复Access接口的缺省VLAN。
system-view interface interface-type interface-number port link-type access undo port default vlan [ vlan-id ]
● 恢复Trunk接口的缺省VLAN。
system-view interface interface-type interface-number port link-type trunk undo port trunk pvid vlan [ vlan-id ]
● 恢复Hybrid接口的缺省VLAN。
system-view interface interface-type interface-number port link-type hybrid undo port hybrid pvid vlan [ vlan-id ]
----结束检查配置结果执行命令display port vlan [ interface-type interface-number ] [ active ]，查看接口所属的缺省VLAN（PVID）。

### 4.7 配置VLANIF接口

前提条件在配置VLANIF接口之前，需完成以下任务：
● VLANIF接口对应的VLAN，已经创建。
● 接口已经加入VLANIF对应的VLAN，详见“4.8.2 配置基于接口划分VLAN（静态配置接口类型）”、“4.8.4 配置基于MAC地址划分VLAN”、“4.8.5 配置基于子网划分VLAN”、“4.8.6 配置基于协议划分VLAN”。
背景信息VLANIF接口的基本介绍和应用，详见“4.9.2 配置VLANIF接口实现不同VLAN间的互通”。
延迟VLANIF接口状态变为Down的时间可避免由于VLANIF接口状态变化而引起的网络振荡，此功能也可称为 VLAN Damping 功能。
当VLAN中接口状态变为Down而引起VLAN状态变为Down时，VLAN会向VLANIF接口上报Down事件，从而引起VLANIF接口状态变化。为避免由于VLANIF接口状态变化引起的网络振荡，可以在VLANIF接口上启动VLAN Damping功能。当VLAN中最后一个处于Up状态的成员端口变为Down后，启动VLAN Damping功能的设备会抑制设定的时间后再上报给VLANIF接口。如果在抑制的时间内VLAN中有成员口状态变为Up，则VLANIF接口状态保持Up不变。
操作步骤步骤1 进入系统视图。
system-view步骤2 创建VLANIF接口，并进入VLANIF接口视图（不同设备支持的VLANIF接口数量不同，详见：接口基础配置注意事项）。
interface vlanif vlan-id步骤3 配置VLANIF接口的IP地址。
ip address ip-address { mask | mask-length } [ sub ]步骤4 （可选）配置延迟VLANIF接口状态变为Down的时间。
damping time delay-time步骤5 （可选）配置VLANIF接口的MTU。
mtu mtu步骤6 （可选）配置网管获取的VLANIF接口带宽，此命令配置的带宽值为接口的期望带宽值，不直接影响设备的流量转发行为。
bandwidth bandwidth
----结束检查配置结果执行命令display interface vlanif [ interface-number | main]，查看VLANIF接口的物理状态、接口IP地址等配置信息。

### 4.8 配置同一VLAN内的互通

#### 4.8.1 了解同一VLAN内的互通

同一VLAN内的互通原理在前文已有介绍，接下来主要介绍VLAN的划分方式。
如表4-6所示，设备支持基于多种划分VLAN的方式。缺省情况下，划分VLAN的方式优先级高低顺序从左至右依次为：基于MAC地址划分VLAN或基于子网划分VLAN > 基于协议划分VLAN > 基于接口划分VLAN。
● 如果报文同时匹配了基于MAC地址划分VLAN和基于子网划分VLAN，缺省情况下，优先基于MAC地址划分VLAN。但是可以通过命令改变基于MAC地址划分VLAN和基于子网划分VLAN的优先级，从而决定优先划分VLAN的方式。
● 基于接口划分VLAN的优先级最低，但却是最常用的VLAN划分方式。
表 4-6 VLAN 划分方式差异表

| VLAN划分方式 | 原理 | 优点 | 缺点 |
|---|---|---|---|
| 基于接口划分VLAN | 根据设备的接口编号来划分 VLAN。网络管理员给设备的每个接口配置不同的PVID，即一个接口缺省属于的VLAN。 ● 当一个数据帧进入设备接口时，如果没有带VLAN标签，且该接口上配置了 PVID，那么，该数据帧就会被打上接口的PVID。 ● 如果进入的帧已经带有 VLAN标签，那么设备不会再增加VLAN标签，即使接口已经配置了PVID。对VLAN帧的处理由接口类型决定。 | 定义成员简单。 | 成员移动需重新配置 VLAN。 |
| 基于MAC地址划分VLAN | 根据计算机网卡的MAC地址来划分VLAN。网络管理员成功配置MAC地址和VLAN ID映射关系表，如果设备收到的是untagged （不带VLAN标签）帧，则依据该表为帧添加Tag。 | 当终端用户的物理位置发生改变，不需要重新配置 VLAN。提高了终端用户的安全性和接入的灵活性。 | ● 只适用于网卡不经常更换、网络环境较简单的场景中。 ● 需要预先定义网络中所有成员。 |

| VLAN划分方式 | 原理 | 优点 | 缺点 |
|---|---|---|---|
| 基于子网划分VLAN | 如果设备收到的是untagged （不带VLAN标签）帧，设备根据报文中的源IP地址信息，确定添加的VLAN ID。 | 将指定网段或IP地址发出的报文在指定的VLAN中传输，有利于管理。 | 网络中的用户分布需要有规律，且多个用户在同一个网段。 |
| 基于协议划分 | 根据数据帧所属的协议（族）类型及封装格式来划分 VLAN。网络管理员预先配置以太网帧中的协议域和VLAN ID的映射关系表，如果收到的是 untagged帧，就依据该表给数据帧添加指定VLAN的 Tag。然后数据帧将在指定 VLAN中传输。 | 将网络中提供的服务类型与VLAN相绑定，方便管理和维护。 | ● 需要对网络中所有的协议类型和 VLAN ID 的映射关系表进行初始配置。 ● 需要分析各种协议的格式并进行相应的转换，消耗设备较多的资源，速度上稍具劣势。 |

基于子网划分VLAN和基于协议划分VLAN统称为基于网络层划分VLAN。

#### 4.8.2 配置基于接口划分VLAN（静态配置接口类型）

前提条件在配置基于接口划分 VLAN 之前，需完成以下任务：
● VLAN已经创建，详见4.5 创建和删除VLAN。
背景信息基于接口划分VLAN是最简单、最有效的VLAN划分方式。它按照设备的接口来定义VLAN成员，将指定接口加入到指定VLAN中之后，接口就可以转发该VLAN的报文，从而实现VLAN内的主机可以直接互通（即二层互通），而VLAN间的主机不能直接互通，将广播报文限制在一个VLAN内。在操作前，需预先了解接口类型、缺省VLAN、接口处理Tagged或Untagged报文的方式，详见“4.2 VLAN原理描述”。

操作步骤步骤1 进入系统视图。
system-view步骤2 进入需要加入VLAN的以太网接口视图。
interface interface-type interface-number步骤3 将接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 配置二层以太网接口属性。
port link-type { access | hybrid | trunk }步骤5 关联接口和VLAN。
● Access 类型接口，以下步骤请根据情况任选一种。
配置接口的缺省VLAN，并将接口加入到指定的VLAN中。
port default vlan vlan-id如果需要配置接口的缺省VLAN，并批量将接口加入VLAN，则在VLAN视图下执行以下命令。
port interface-type { interface-number1 [ to interface-number2 ] } &<1-10>
● Trunk类型接口，将接口以Tagged方式加入到指定的VLAN中。
port trunk allow-pass vlan { { vlan-id1 [ to vlan-id2 ] } &<1-40> | all }如果需要修改Trunk接口的缺省VLAN，可以在接口视图下执行命令port trunk pvid vlan vlan-id。
● Hybrid类型接口，以下步骤请根据情况任选一种。
将Hybrid接口以Untagged方式加入VLAN。
port hybrid untagged vlan { { vlan-id1 [ to vlan-id2 ] } &<1-10> | all }将Hybrid接口以Tagged方式加入VLAN。
port hybrid tagged vlan { { vlan-id1 [ to vlan-id2 ] } &<1-10> | all }如果需要修改Hybrid接口的缺省VLAN，可以在接口视图下执行命令port hybrid pvid vlan vlan-id。
----结束检查配置结果
● 执行命令display vlan vlan-id1 [ verbose | to vlan-id2 ]，查看指定VLAN的信息。
● 执行命令display vlan [ summary ]，查看所有VLAN的信息。
● 执行命令display vlan vlan-name vlan-name，查看指定VLAN的信息。

#### 4.8.3 配置基于接口划分VLAN（LNP动态协商链路类型）

前提条件在配置基于接口划分VLAN之前，需完成以下任务：

● 设备连接成功后，设备接口物理状态为Up。
● 对端设备需要使能链路类型自协商功能。
背景信息
当前，设备支持的以太网接口的链路类型有：Access、Hybrid、Trunk和QinQ。这四
种接口的链路类型分别用于不同的网络位置，均由手工配置指定。如果网络拓扑变
更，以太网接口的链路类型也需要重新配置，配置较为繁琐。为了简化用户配置，可
通过LNP配置以太网接口的链路类型自协商功能，自动协商出接口的链路类型为Access
或者Trunk，并加入相应VLAN。
部署LNP时，一般需要同时部署VLAN集中管理协议VCMP（VLAN Central
Management Protocol），以集中创建、删除VLAN，最大程度简化用户配置。有关
VCMP的配置请参见6 VCMP配置。
操作步骤
步骤1 进入系统视图。
system-view
步骤2 全局使能链路类型自协商功能。
undo lnp disable
缺省情况下，全局LNP处于使能状态，此时所有接口的链路类型自协商功能处于使能
状态。
步骤3 进入需要使能链路类型自协商功能的以太网接口视图。
interface interface-type interface-number
步骤4 将接口从三层模式切换到二层模式。
portswitch
仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二
层模式。
步骤5 配置基于二层以太网接口使能链路类型自协商功能。
undo port negotiation disable
缺省情况下，设备上所有接口的链路类型自协商功能处于使能状态。
说明
● 当支持链路类型自协商功能的设备和不支持链路类型自协商功能的设备互通时，支持链路类
型自协商功能的设备会不断发送自协商报文，导致带宽浪费。此时，可通过在对应的二层以
太网接口视图下执行命令port negotiation disable去使能链路类型自协商功能。
● 为了保证链路类型自协商功能生效，必须保证全局下和接口视图下的链路类型自协商功能都
处于使能状态。
步骤6 设置二层以太网接口的链路类型的自协商方式。
port link-type { negotiation-desirable | negotiation-auto }
缺省情况下，二层以太网接口的链路类型的自协商方式是negotiation-desirable。

说明配置为negotiation-desirable或negotiation-auto的接口有以下约束：
● 不支持创建子接口；
● 不支持使能MUX VLAN；
● 不支持配置自动模式Voice VLAN。
步骤7 查看运行LNP协议的二层接口自协商的状态信息。
display lnp { interface interface-type interface-number | summary }步骤8 配置接口允许通过的VLAN。
● 当LNP协商结果为Trunk类型时
a. 配置协商为Trunk类型的接口只允许通过的VLAN。
port trunk allow-pass only-vlan { { vlan-id1 [ to vlan-id2 ] } & <1-10> | none }缺省情况下，协商为Trunk类型的接口允许所有VLAN通过。
（可选）配置接口的缺省VLAN。
b.
port trunk pvid vlan vlan-id当接口（比如连接AP、语音设备的接口）上收到Untagged、Tagged两种报文时，此时需要在接口上配置缺省VLAN，给Untagged报文加上VLAN Tag。
缺省情况下，协商为Trunk类型的接口的缺省VLAN为VLAN1。
● 当LNP协商结果为Access类型时配置协商为Access类型的接口的缺省VLAN。
port default vlan vlan-id缺省情况下，协商为Access类型的接口的缺省VLAN以及加入的VLAN均为VLAN1。
----结束检查配置结果在任意视图下执行命令display lnp { interface interface-type interface-number | summary }，查看运行LNP协议的二层接口自协商的状态信息。
后续处理当需要统计一定时间内LNP报文的统计信息，必须在统计开始前清除原有的统计信息，使系统重新进行统计。可在用户视图下执行reset lnp statistics [ interface interface-type interface-number ] 命令，再执行 display lnp { interface interface- type interface-number | summary }，查看运行LNP协议的二层接口自协商的状态信息。
说明清除LNP报文统计信息后，以前的信息将无法恢复，务必仔细确认。

#### 4.8.4 配置基于MAC地址划分VLAN

前提条件在配置基于MAC地址划分VLAN之前，需完成以下任务：
● VLAN已经创建，详见4.5 创建和删除VLAN。

背景信息基于MAC地址划分VLAN不需要关注终端用户的物理位置，提高了终端用户的安全性和接入的灵活性。
基于MAC地址划分VLAN只处理Untagged报文，对于Tagged报文则使用基于接口划分VLAN的方式转发。
当接口收到的报文为Untagged报文时，接口会根据报文的源MAC地址去匹配MAC- VLAN表项：
● 如果匹配成功，则按照匹配到的VLAN ID进行转发。
● 如果匹配失败，则按其他匹配原则进行匹配，具体请参见4.8.1 了解同一VLAN内的互通。
说明采用基于MAC地址方式划分的VLAN不支持处理上送CPU的协议报文，建议在二层透传场景下使用该方式。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入VLAN视图。
vlan vlan-id步骤3 关联MAC地址和VLAN。
mac-vlan mac-address mac-address [ priority priority ] MAC地址不可设置为全F、全0或组播地址。
步骤4 返回系统视图。
quit步骤5 进入需要加入VLAN的以太网接口视图。
interface interface-type interface-number步骤6 将接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤7 配置二层以太网接口属性。
port link-type hybrid步骤8 配置基于MAC地址划分的VLAN通过当前Hybrid接口。
port hybrid untagged vlan { { vlan-id1 [ to vlan-id2 ] } &<1-10> | all }步骤9 开启基于MAC地址划分VLAN的功能。
mac-vlan enable步骤10 （可选）接口下同时配置基于MAC地址划分VLAN和基于子网划分VLAN时，选择其中一种的使其优先级更高。

vlan precedence { ip-subnet-vlan | mac-vlan }缺省情况下，基于MAC地址划分VLAN优先级高于基于子网划分VLAN优先级。
----结束检查配置结果执行命令display mac-vlan { vlan vlan-id | mac-address { mac-address | all } }，查看基于MAC地址划分VLAN的相关信息。

#### 4.8.5 配置基于子网划分VLAN

前提条件在配置基于子网划分VLAN之前，需完成以下任务：
● VLAN已经创建，详见4.5 创建和删除VLAN。
背景信息基于子网划分VLAN可以保证用户自由地移动、增加和减少，适用于对安全需求不高，对移动性和简易管理需求较高的场景。
基于子网划分的VLAN只处理Untagged报文，对于Tagged报文则使用基于接口划分VLAN的方式转发。
当设备接口接收到Untagged报文时，设备根据报文的源IP地址和指定网段来匹配报文所属的VLAN：
● 如果匹配成功，则按照匹配到的VLAN ID进行转发。
● 如果匹配失败，则按其他匹配原则进行匹配，具体请参见4.8.1 了解同一VLAN内的互通。
说明采用基于子网方式划分的VLAN不支持处理上送CPU的协议报文，建议在二层透传场景下使用该方式。
操作步骤步骤 1 进入系统视图。
system-view步骤2 进入VLAN视图。
vlan vlan-id步骤3 关联IP子网和VLAN。
ip-subnet-vlan [ ip-subnet-index ] ip ip-address { mask | mask-length } [ priority priority ] IP网段或IP地址不能配置为组播网段或组播地址。
步骤4 返回系统视图。
quit步骤5 进入需要加入VLAN的以太网接口视图。
interface interface-type interface-number

步骤6 将接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤7 配置二层以太网接口属性。
port link-type hybrid步骤8 配置基于子网划分的VLAN通过当前Hybrid接口。
port hybrid untagged vlan { { vlan-id1 [ to vlan-id2 ] } &<1-10> | all }步骤9 开启基于子网划分VLAN的功能。
ip-subnet-vlan enable步骤10 （可选）接口下同时配置基于MAC地址划分VLAN和基于子网划分VLAN时，配置接口优先基于MAC地址划分VLAN还是基于子网划分VLAN。
vlan precedence { ip-subnet-vlan | mac-vlan }缺省情况下，基于MAC地址划分VLAN优先级高于基于子网划分VLAN优先级。
----结束检查配置结果执行命令display ip-subnet-vlan vlan { vlan-id1 [ to vlan-id2 ] | all }，查看基于子网划分VLAN的相关信息。

#### 4.8.6 配置基于协议划分VLAN

前提条件在配置基于协议划分VLAN之前，需完成以下任务：
VLAN已经创建，详见4.5 创建和删除VLAN。
●背景信息基于协议划分VLAN可减少手工配置VLAN的工作量，也可保证用户自由地增加、移动和修改。
基于协议划分VLAN只处理untagged报文，对于Tagged报文则使用基于接口划分VLAN的方式转发。
当设备接口接收到untagged帧时，设备先识别帧的协议模板，然后确定报文所属的VLAN。
● 如果接口配置了属于某些协议VLAN，且报文的协议模板匹配其中某个协议VLAN，则给报文打上该协议VLAN的Tag。
● 如果接口配置了属于某些协议VLAN，但报文的协议模板和所有协议VLAN不匹配，则给报文打接口PVID的Tag。

说明基于协议方式划分的VLAN不支持处理上送CPU的协议报文，建议在二层透传场景下使用该方式。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入VLAN视图。
vlan vlan-id步骤3 关联协议和VLAN，并指定协议模板。
protocol-vlan [ protocol-index1 ] { at | ipv4 | ipv6 | ipx { ethernetii | llc | raw | snap } | mode { ethernetii- etype etype-id1 | llc { dsap dsapValue ssap ssapValue } | snap-etype etype-id1 } }
● 可选参数protocol-index1是协议模板索引值。
协议模板由协议类型+封装格式确定，一个协议VLAN可由一个协议模板定义。
● 配置源和目的服务接入点时，需要注意以下几点：
– dsapValue 和 ssapValue 不能同时设置成 0xaa 。
– dsapValue和ssapValue不能同时设置成0xe0，0xe0对应的是IPX报文的llc封装格式。
– dsapValue和ssapValue也不能同时设成0xff，0xff对应的是IPX报文的raw封装格式。
步骤4 返回系统视图。
quit步骤5 进入需要加入VLAN的以太网接口视图。
interface interface-type interface-number步骤6 将接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤7 配置二层以太网接口属性。
port link-type hybrid步骤8 配置基于协议划分的VLAN通过当前Hybrid接口。
port hybrid untagged vlan { { vlan-id1 [ to vlan-id2 ] } &<1-10> | all }步骤9 配置接口关联协议VLAN。
protocol-vlan vlan vlan-id { all | protocol-index1 [ to protocol-index2 ] } [ priority priority ]参数vlan-id必须是基于协议划分的VLAN ID。
----结束检查配置结果
● 执行命令display protocol-vlan interface { interface-type interface-number | all }，查看接口关联基于协议划分VLAN的配置信息。

● 执行命令display protocol-vlan vlan { vlan-id1 [ to vlan-id2 ] | all }，查看
VLAN上所配置的协议及协议模板的索引。

### 4.9 配置不同VLAN间的互通

#### 4.9.1 了解不同VLAN间的互通

不同VLAN间的用户要实现互通，如果是不同网段用户，常用的技术为：
● 通过VLANIF接口：VLANIF接口是一种三层的逻辑接口，能实现不同VLAN间，不同网段的用户进行三层互通。由于配置较为简单，是实现VLAN间互通最常用的一种技术。
每个VLAN对应一个VLANIF接口，在为VLANIF接口配置IP地址后，该接口即可作为本VLAN内用户的缺省网关，对需要跨网段的报文进行基于IP地址的三层转发。
如果存在多个不同网段的情况，而这些网段的用户都需要实现互通，则需要在VLANIF接口上配置一个主IP地址和多个从IP地址。
● 通过三层子接口：三层子接口是一种三层的逻辑接口，能实现不同 VLAN 间，不同网段的用户进行三层互通。虽然VLANIF接口可以实现不同VLAN间的互通，但是会占用多个物理接口，为解决这个问题，可以使用三层子接口。
说明仅S6780-H、S6750-H、S6750-S、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S5732-H-V2系列支持三层子接口。
详细的原理介绍请参见“4.2.7 不同VLAN间的互通原理”。

#### 4.9.2 配置VLANIF接口实现不同VLAN间的互通

前提条件在配置VLANIF接口实现不同VLAN间的互通之前，需完成以下任务：
● VLAN已经创建，详见“4.5 创建和删除VLAN”。
背景信息VLANIF 接口是一种三层的逻辑接口，能实现不同 VLAN 间，不同网段的用户进行三层互通。由于配置较为简单，是实现VLAN间互通最常用的一种技术。
每个VLAN对应一个VLANIF接口，在为VLANIF接口配置IP地址后，该接口即可作为本VLAN内用户的缺省网关，对需要跨网段的报文进行基于IP地址的三层转发。
通过VLANIF接口实现VLAN间互通只适用于各个VLAN内主机处于不同网段的场景。详细的实现机制，请参见“同设备VLAN间互通（VLANIF接口）、跨设备VLAN间互通（VLANIF接口）”。
操作步骤步骤1 进入系统视图。
system-view

#### 4.9.3 配置三层子接口实现不同VLAN间的互通

步骤2 创建VLANIF接口，并进入VLANIF接口视图。
interface vlanif vlan-id步骤3 配置VLANIF接口的IP地址。
ip address ip-address { mask | mask-length } [ sub ]如果存在多个不同网段的情况，而这些网段的用户都需要实现互通，则需要在VLANIF接口上配置一个主IP地址和多个从IP地址。另外，不同的VLANIF接口所配置的IP地址是在不同的网段中。
----结束检查配置结果执行命令display interface vlanif，可以查看VLANIF接口信息。
后续处理若需要VLAN内的所有用户都不能通过VLANIF接口与其他VLAN内用户通信，但是VLAN内用户还可以互相通信，可以在VLANIF接口视图下执行命令shutdown。
VLANIF接口上的流量包括二层流量和三层流量，如果在VLANIF接口视图下执行shutdown命令，则只能禁止三层流量，不能禁止二层流量。此时，执行display interface vlanif命令可以看到VLANIF接口下的流量计数仍在增加。
配置三层子接口实现不同 间的互通
4.9.3 VLAN前提条件说明该配置仅S6780-H、S6750-H、S6750-S、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755-
H、S5755-S、S5732-H-V2系列支持。
在配置三层子接口实现不同VLAN间的互通之前，需完成以下任务：
● VLAN已经创建，详见“4.5 创建和删除VLAN”。
● 执行命令undo portswitch，将接口从二层模式切换到三层模式。
说明请用户根据实际接口类型自行选择是否要执行接口切换到三层模式的步骤。
背景信息不同VLAN间要进行通信，最直接的办法是将不同的VLAN连接到三层设备的不同接口，通过路由实现不同VLAN间的数据通信。但这样会浪费设备上有限的物理接口。为解决这个问题，可以使用三层子接口。
三层子接口是一种三层的逻辑接口，在一个物理接口上配置多个子接口，这些子接口分别对应不同VLAN，这样只需连接一个物理接口就可实现不同VLAN之间的互通。通过三层子接口实现VLAN间互通只适用于各个VLAN内主机处于不同网段的场景。详细的实现机制，请参见“同设备VLAN间互通（三层子接口）”。

操作步骤步骤1 进入系统视图。
system-view步骤2 创建子接口并进入子接口视图。
interface interface-type interface-number.subinterface-number说明缺省情况下，三层子接口状态发生改变会产生linkdown告警（Trap OID：1.3.6.1.6.1.1.5.3）。
如果设备上三层子接口数量较多，接口产生的linkdown告警每隔几分钟会上报一次，此时网管设备需要处理大量的接口状态告警信息，增加了网管设备的负担。为解决上述问题，在确认不需要关注linkdown告警的情况下可以在系统视图下执行subinterface trap updown disable命令关闭三层子接口产生linkdown告警。执行此命令后，设备上所有子接口状态发生变化均不会产生linkdown告警，请谨慎操作。
步骤3 配置子接口的封装类型及关联的VLAN ID。
dot1q termination vid low-pe-vid步骤4 配置子接口的IP地址。
ip address ip-address { mask | mask-length } [ sub ]子接口的IP地址和主接口的IP地址可以在同一主网段上，但其子网掩码不能相同。
----结束检查配置结果执行命令display vlan vlan-id verbose，可以查看VLAN与子接口关联的信息。

### 4.10 配置管理VLAN

#### 4.10.1 配置管理VLAN实现对设备的集中管理

前提条件在配置管理VLAN实现对设备的集中管理之前，需完成以下任务：
● VLAN已经创建，详见“4.5 创建和删除VLAN”。
● VLAN 已经划分，详见“ 4.8.2 配置基于接口划分 VLAN （静态配置接口类型）”、“4.8.4 配置基于MAC地址划分VLAN”、“4.8.5 配置基于子网划分VLAN”、“4.8.6 配置基于协议划分VLAN”。
背景信息配置管理VLAN功能后，用户可以通过管理VLAN对应的VLANIF接口实现网管集中管理设备。通过管理网口只能登录本地设备，通过管理VLAN的VLANIF接口既可以登录本地设备，也可以登录远程设备。
操作步骤步骤1 进入系统视图。
system-view

步骤2 进入VLAN视图。
vlan vlan-id步骤3 创建管理VLAN。
management-vlan创建管理VLAN后，加入该VLAN的接口类型必须是Trunk或Hybrid。
步骤4 返回系统视图。
quit步骤5 创建VLANIF接口，并进入VLANIF接口视图。
interface vlanif vlan-id vlan-id必须是配置为管理VLAN的ID。
步骤6 配置VLANIF接口的IP地址。
ip address ip-address { mask | mask-length } [ sub ]一般情况下，一个管理VLANIF接口只需配置一个管理IP地址，但在有些特殊情况下，比如同一管理VLAN的用户分别属于多个不同网段，则需要在该接口上配置一个主管理IP 地址和多个从管理 IP 地址。
----结束检查配置结果执行命令display vlan，查看管理VLAN的配置信息，带有*的VLAN为管理VLAN。
后续处理管理VLAN配置成功后，需要登录到设备上才能实现通过网管集中管理设备。可根据需要选择一种登录方式：
● 如果管理本地设备，则需要通过Telnet、STelnet方式登录到本地设备。具体配置请参见CLI配置指南中的“登录设备命令行界面”。
● 如果管理远程设备，则需要先通过Telnet、STelnet方式登录到本地设备，然后再从本地设备通过Telnet、STelnet登录到远端设备。具体配置请参见《CLI配置指南-基础配置》中的“登录设备命令行界面”。

### 4.11 配置VLAN pool

背景信息VLAN pool是多个VLAN的合集，其目的是简化网络部署。用户接入认证成功后，认证服务器为用户授权VLAN pool。设备根据一定的算法从VLAN pool中选择一个VLAN分配给新接入的用户。
操作步骤步骤1 进入系统视图。
system-view步骤2 批量创建VLAN。
vlan batch { vlan-id1 [ to vlan-id2 ] } &<1-10>

步骤3 创建VLAN pool，并进入VLAN pool视图。
vlan pool pool-name步骤4 将指定VLAN添加到VLAN pool中。
vlan { start-vlan-id [ to end-vlan-id ] } &<1-10>步骤5 （可选）配置VLAN pool中的VLAN分配算法。
assignment { even | hash }缺省情况下，VLAN pool中的VLAN分配算法为hash。
----结束检查配置结果在任意视图下执行命令display vlan pool，查看VLAN pool的配置信息。
后续处理在RADIUS服务器上配置为通过认证的用户授权标准RADIUS属性Tunnel-Private- Group-ID ，让用户加入指定的 VLAN pool 。

### 4.12 配置VLAN聚合

#### 4.12.1 了解VLAN聚合

说明仅S5735-S-V2、S5732-H-V2、S5735E-S-V2、S5735I-H-V2、S5735I-S-V2、S6730E-H-V2、S6730-H-V2、S5755-H、S6750-H、S6750E-S、S6750-S、S6780-H、S5735S-S3、S5735R-S- V2、S5755-S系列支持VLAN聚合功能。
产生背景交换网络中，VLAN技术以其对广播域的灵活控制和部署方便而得到了广泛的应用。但是在一般的三层设备中，通常是采用一个VLAN对应一个三层逻辑接口的方式实现广播域之间的互通，这样导致了IP地址的浪费。例如，设备内VLAN划分如图4-9所示。

图 4-9 普通 VLAN 网络示意图表 4-7 普通 VLAN 主机地址划分示例

| VLAN | 子网 | 网关地址 | 可用地址数 | 可用主机数 | 实际需求 |
|---|---|---|---|---|---|
| 2 | 1.1.1.0/28 | 1.1.1.1 | 14 | 13 | 10 |
| 3 | 1.1.1.16/29 | 1.1.1.17 | 6 | 5 | 5 |
| 4 | 1.1.1.24/30 | 1.1.1.25 | 2 | 1 | 1 |

如表4-7所示，VLAN2预计未来有10个主机地址的需求，给其分配一个掩码长度是28的子网1.1.1.0/28，其中1.1.1.0为子网号，1.1.1.15为子网定向广播地址，这两个地址都不能用作主机地址，此外1.1.1.1作为子网缺省网关地址也不可作为主机地址，剩下范围在1.1.1.2～1.1.1.14的地址可以被主机使用，共13个。这样，尽管VLAN2只需要10个地址，但是按照子网划分却要分给它13个地址。
同理，VLAN3预计未来有5个主机地址的需求，至少需要分配一个掩码长度是29的子网1.1.1.16/29。VLAN4预计未来只有1个主机，则分配一个掩码长度是30的子网
1.1.1.24/30。
上述VLAN一共需要10＋5＋1＝16个地址，但是按照普通VLAN的编址方式，即使最优化的方案也需要占用16＋8＋4＝28个地址，浪费了将近一半的地址。而且，如果VLAN2后来并没有10台主机，而实际只接入了3台主机，那么多出来的地址也会因不能再被其他VLAN使用而被浪费掉。
同时，这种划分也给后续的网络升级和扩展带来了很大不便。
综上所述，很多IP地址被子网号、子网定向广播地址、子网缺省网关地址消耗掉，而不能用于VLAN内的主机地址。同时，这种地址分配的约束也降低了编址的灵活性，使许多闲置地址也被浪费掉。为了解决这一问题VLAN Aggregation就应运而生。

实现原理VLAN Aggregation技术（也称为Super VLAN，即VLAN聚合）就是在一个物理网络内，用多个VLAN隔离广播域，使不同的VLAN属于同一个子网。它引入了Super-VLAN和Sub-VLAN的概念。
● Super-VLAN：和通常意义上的VLAN不同，它只建立三层接口，与该子网对应，而且不包含物理端口。可以把它看作一个逻辑的三层概念—若干Sub-VLAN的集合。
● Sub-VLAN：只包含物理端口，用于隔离广播域的VLAN，不能建立三层VLANIF接口。它与外部的三层交换是靠Super-VLAN的三层接口来实现的。
一个Super-VLAN可以包含一个或多个保持着不同广播域的Sub-VLAN。Sub-VLAN不再占用一个独立的子网网段。在同一个Super-VLAN中，无论主机属于哪一个Sub- VLAN，它的IP地址都在Super-VLAN对应的子网网段内。
这样，Sub-VLAN间共用同一个三层接口，既减少了一部分子网号、子网缺省网关地址和子网定向广播地址的消耗，又实现了不同广播域使用同一子网网段地址的目的，消除了子网差异，增加了编址的灵活性，减少了闲置地址浪费。
仍以表4-7所示例子进行说明。用户需求不变，仍旧是VLAN2预计未来有10个主机地址的需求，VLAN3预计未来有5个主机地址的需求，VLAN4预计未来有1个主机地址的需求。
按照VLAN Aggregation的实现方式，新建VLAN10并配置为Super-VLAN，给其分配一个掩码长度是24的子网1.1.1.0/24，其中1.1.1.0为子网号，1.1.1.1为子网网关地址如图4-10所示。Sub-VLAN（VLAN2、VLAN3、VLAN4）的地址划分如表4-8所示。
图 4-10 VLAN Aggregation 网络示意图

表 4-8 VLAN Aggregation 主机地址划分示例

| VLAN | 子网 | 网关地址 | 可用地址数 | 可用IP地址 | 实际需求 |
|---|---|---|---|---|---|
| 2 | 1.1.1.0/24 | 1.1.1.1 | 10 | 1.1.1.2～1.1.1.11 | 10 |
| 3 |  |  | 5 | 1.1.1.12～1.1.1.16 | 5 |
| 4 |  |  | 1 | 1.1.1.17 | 1 |

VLAN Aggregation的实现中，各Sub-VLAN间的界线也不再是从前的子网界线了，它们可以根据其各自主机的需求数目在Super-VLAN对应子网内灵活的划分地址范围。
从表4-8中可以看到，VLAN2、VLAN3和VLAN4共用同一个子网（1.1.1.0/24）、子网缺省网关地址（1.1.1.1）和子网定向广播地址（1.1.1.255）。这样，普通VLAN实现方式中用到的其他子网号（1.1.1.16、1.1.1.24）和子网缺省网关（1.1.1.17、
1.1.1.25），以及子网定向广播地址（1.1.1.15、1.1.1.23、1.1.1.27）就都可以用来作为主机 IP 地址使用。
这样，3个VLAN一共需要10＋5＋1＝16个地址，实际上在这个子网里就刚好分配了16个地址（1.1.1.2～1.1.1.17）给3个VLAN。这16个主机地址加上子网号（1.1.1.0）、子网缺省网关（1.1.1.1）和子网定向广播地址（1.1.1.255），一共用去了19个IP地址，网段内仍剩余255－19＝236的地址可以被任意Sub-VLAN内的主机使用。
VLAN 间通信
● 概述VLAN Aggregation在实现不同VLAN间共用同一子网网段地址的同时也带来了Sub-VLAN间的三层转发问题。
普通VLAN实现方式中，VLAN间的主机可以通过各自不同的网关进行三层转发来达到互通的目的。但是VLAN Aggregation方式下，同一个Super-VLAN内的主机使用的是同一个网段的地址和共用同一个网关地址。即使是属于不同的Sub-VLAN的主机，由于它们同属一个子网，彼此通信时只会做二层转发，而不会通过网关进行三层转发。而实际上不同的Sub-VLAN的主机在二层是相互隔离的，这就造成了Sub-VLAN间无法通信的问题。
解决这一问题的方法就是使用ARP代理。
● 不同Sub-VLAN间的三层互通例如，Super-VLAN（VLAN10）包含Sub-VLAN（VLAN2和VLAN3），具体组网如图4-11所示。

图 4-11 ARP 代理实现不同 Sub-VLAN 间的三层互通组网图VLAN2内的PC1与VLAN3内的PC2的通信过程如下：（假设PC1的ARP表中无PC2的对应表项并且网关上使能了Sub-VLAN间的ARP Proxy）。
a. PC1将PC2的IP地址（1.1.1.3）和自己所在网段1.1.1.0/24进行比较，发现PC2和自己在同一个子网，但是PC1的ARP表中无PC2的对应表项。
b. PC1发送ARP广播，请求PC2的MAC地址。
c. PC2并不在VLAN2的广播域内，无法接收到PC1的这个ARP请求。
d. 由于网关上使能Sub-VLAN间的ARP代理，当网关收到PC1的ARP请求后，开始在路由表中查找，发现ARP请求中的PC2的IP地址（1.1.1.3）为直连接口路由，则网关向所有其他Sub-VLAN发送一个ARP广播，请求PC2的MAC地址。
e. PC2收到网关发送的ARP广播后，对此请求进行ARP应答。
f. 网关收到PC2的应答后，就把自己的MAC地址当作PC2的MAC地址回应给PC1。
g. 网关和PC1的ARP表中都存在PC2的对应表项。
h. PC1之后要发给PC2的报文都先发送给网关，由网关做三层转发。
PC2发送报文给PC1的过程和上述的PC1到PC2的报文流程类似，不再赘述。
● Sub-VLAN 与外部网络的二层通信在基于端口的VLAN二层通信中，无论是数据帧进入接口还是从接口发出都不会有针对Super-VLAN的报文。如图4-12所示。

图 4-12 Sub-VLAN 与外部网络的二层通信组网图从PC1侧Port1进入设备DeviceA的帧会被打上VLAN2的Tag，在设备DeviceA中这个Tag不会因为VLAN2是VLAN10的Sub-VLAN而变为VLAN10的Tag。该数据帧从Trunk类型的接口Port3出去时，依然是携带VLAN2的Tag。
也就是说，设备DeviceA本身不会发出VLAN10的报文。就算其他设备有VLAN10的报文发送到该设备上，这些报文也会因为设备DeviceA上没有VLAN10对应物理端口而被丢弃。
Super-VLAN中是不存在物理端口的，这种限制是强制的，表现在：
– 如果先配置了Super-VLAN，再配置Trunk接口时，Trunk的VLAN allowed表项里就自动滤除了Super VLAN。
如图4-12所示，虽然DeviceA的Port3允许所有的VLAN通过，但是也不会有作为Super-VLAN的VLAN10的报文从该接口进出。
– 如果先配置了Trunk端口，并允许所有VLAN通过，则在此设备上将无法配置Super VLAN。本质原因是有物理端口的VLAN都不能被配置为Super VLAN。
对于设备DeviceA而言，有效的VLAN只有VLAN2和VLAN3，所有的数据帧都在这两个VLAN中转发。
● Sub-VLAN与外部网络的三层通信

图 4-13 Sub-VLAN 与外部网络的三层通信组网图如图4-13所示，DeviceA上配置了Super-VLAN 4，Sub-VLAN 2和Sub-VLAN 3，并配置一个普通的VLAN10；DeviceB上配置两个普通的VLAN，VLAN 10和VLAN 20。假设Super-VLAN 4中的Sub-VLAN 2下的PC1想访问与DeviceB相连的主机PC3，通信过程如下：（假设DeviceA上已经配置了去往1.1.3.0/24网段的路由，DeviceB上已配置了去往1.1.1.0/24网段的路由）
a. PC1将PC3的IP地址（1.1.3.2）和自己所在网段1.1.1.0/24进行比较，发现PC3和自己不在同一个子网。
b. PC1发送ARP请求给自己的网关，请求网关的MAC地址。
c. DeviceA收到该ARP请求后，查找Sub-VLAN和Super-VLAN的对应关系，从Sub-VLAN 2发送ARP应答给PC1。ARP应答报文中的源MAC地址为Super- VLAN 4对应的VLANIF4的MAC地址。
d. PC1学习到网关的MAC地址。
e. PC1向网关发送目的MAC为Super-VLAN 4对应的VLANIF4的MAC、目的IP为
1.1.3.2的报文。
f. DeviceA收到该报文后进行三层转发，下一跳地址为1.1.2.2，出接口为VLANIF10，把报文发送给DeviceB。
g. DeviceB收到该报文后进行三层转发，通过直连出接口VLANIF20，把报文发送给PC3。
h. PC3的回应报文，在DeviceB上进行三层转发到达DeviceA。
i. DeviceA收到该报文后，三层转发报文的目的IP地址为1.1.1.2，当DeviceA三层流量通过 VLANIF 10 转二层流量时，指定的下一跳 IP 地址通过 super VLAN 4映射到sub VLAN 2，报文通过VLAN 2发送给PC1。

#### 4.12.2 创建Sub-VLAN

操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤3 将接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否需要执行此步骤。
仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 配置二层接口属性为Access。
port link-type access对于S5735I-L-V2，S5735I-S-V2，S5735I-H-V2，S5735-L-V2，S5735E-L-V2，S5735R-L-V2，S5735-S-V2，S5735E-S-V2，S5735R-S-V2，S5735S-L3，S5735S- S3，S1730S-S3系列，缺省情况下，接口的链路类型为negotiation-auto类型。
对于S5732-H-V2，S6780-H，S6750-H，S6750-S，S6750E-S，S6730-H-V2，S6730E-H-V2，S5755-H，S5755-S系列，缺省情况下，接口的链路类型为negotiation-desirable类型。
步骤5 退出接口视图，返回到系统视图。
quit步骤6 创建Sub-VLAN，并进入Sub-VLAN视图。
vlan vlan-id如果设备上创建了多个VLAN，为了便于管理和维护，建议为VLAN创建名称，即在VLAN视图下执行命令name vlan-name，创建VLAN名称。VLAN名称配置成功后，用户可在系统视图下执行命令vlan vlan-name vlan-name直接进入对应的VLAN视图。
步骤7 将端口加入VLAN。
port interface-type { interface-number1 [ to interface-number2 ] } &<1-10>
----结束

#### 4.12.3 创建Super-VLAN

前提条件在配置Super-VLAN之前必须已完成配置Sub-VLAN。
操作步骤步骤1 进入系统视图。
system-view

步骤2 创建VLAN，并进入VLAN视图。
vlan vlan-id本配置步骤中的vlan-id与Sub-VLAN中的vlan-id不能相同。
步骤3 创建Super-VLAN。
aggregate-vlan在VLAN视图下执行命令undo aggregate-vlan，可以将一个Super-VLAN改变为Sub- VLAN。
步骤4 将Sub-VLAN加入Super-VLAN。
access-vlan { vlan-id1 [ to vlan-id2 ] } &<1-10>只有Sub-VLAN才能成功加入Super-VLAN。如果要将多个Sub-VLAN批量加入到Super- VLAN中，必须保证这些Sub-VLAN没有创建对应的VLANIF接口。
----结束

#### 4.12.4 配置Super-VLAN对应的VLANIF接口的IP地址

背景信息Super-VLAN对应的VLANIF接口的IP地址应包含各Sub-VLAN用户所在的子网段，所有Sub-VLAN共用Super-VLAN的VLANIF接口IP地址，从而解决IP地址资源问题。
操作步骤步骤1 进入系统视图。
system-view步骤2 创建Super-VLAN对应的VLANIF接口，并进入VLANIF接口视图。
interface vlanif vlan-id步骤3 配置VLANIF接口的IP地址。
ip address ip-address { mask | mask-length } [ sub ]
----结束

#### 4.12.5 （可选）使能Super-VLAN对应的VLANIF接口的ARP Proxy

前提条件在使能该功能之前，需配置Super-VLAN对应的VLANIF接口的IP地址。
背景信息VLAN聚合在实现不同Sub-VLAN间共用一个子网网段地址的同时也带来了Sub-VLAN间的三层转发问题。普通VLAN实现方式中，VLAN间的主机可以通过各自不同的网关进行三层转发达到互通的目的。但是VLAN聚合方式下，同一个Super-VLAN内的主机使用的是同一个网段的地址和共用同一个网关地址。即使是属于不同的 Sub-VLAN 的主机，由于它们同属一个子网，彼此通信时只会做二层转发，而不会通过网关进行三层转发。而实际上不同的Sub-VLAN的主机在二层是相互隔离的，这就造成了Sub-VLAN间无法通信。

为了实现Sub-VLAN间相互通信及Sub-VLAN与其他网络的互通，需要利用ARP Proxy功能。在创建好Super-VLAN和对应的VLANIF接口后，用户需要开启设备的ARP Proxy功能，Super-VLAN利用ARP Proxy功能可以进行ARP请求和响应报文的转发与处理，从而实现Sub-VLAN之间的三层互通。当以太网存在大量VLAN时，不同的VLAN间需要通信，VLAN聚合还可以简化配置。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入Super-VLAN对应的VLANIF接口视图。
interface vlanif vlan-id步骤3 使能Sub-VLAN间的ARP Proxy功能。
arp proxy inter-vlan enable
----结束

#### 4.12.6 检查配置结果

操作步骤
● 执行display vlan vlan-id [ verbose | to vlan-id2 ]命令，查看VLAN信息。
● 执行display interface vlanif [ vlan-id ]命令，查看VLANIF接口信息
----结束任务示例执行display vlan vlan-id verbose命令可以看到VLAN类型。例如：
<HUAWEI> display vlan 40 verbose VLAN ID : 20 VLAN Type : Super Description : VLAN 0020 Status : Enable Broadcast : Enable MAC Learning : Enable Statistics : Disable
---------------- sub-VLAN List: 10执行 display interface vlanif 命令，可以看到 VLANIF 接口物理状态、链路协议状态、IP地址和掩码等信息。例如：
<HUAWEI> display interface vlanif 2 Vlanif2 current state : UP (ifindex: 22)
Line protocol current state : UP Last line protocol up time : 2013-08-07 07:28:59 Description:
Route Port,The Maximum Transmit Unit is 1500 Internet Address is 10.1.1.2/24 IP Sending Frames' Format is PKTFMT_ETHNT_2, Hardware address is 00e0-fc12-3456 Physical is VLANIF Current system time: 2013-08-08 07:30:27 Last 300 seconds input rate 941 bits/sec, 2 packets/sec Last 300 seconds output rate 968 bits/sec, 3 packets/sec Input: 827 packets,0 bytes 410 unicast,417 broadcast,0 multicast 0 errors,0 drops

Output:819 packets,0 bytes 402 unicast,417 broadcast,0 multicast 0 errors,0 drops Last 300 seconds input utility rate: -- Last 300 seconds output utility rate: --

### 4.13 配置MUX VLAN

#### 4.13.1 了解MUX VLAN

产生背景MUX VLAN（Multiplex VLAN）提供了一种通过VLAN进行网络资源控制的机制。
例如在企业网络中，网络管理员希望员工和客户均可以访问企业的服务器，员工之间可以互相交流，而客户之间互相隔离不能互访。为了实现所有用户都可访问企业服务器，可通过配置VLAN间通信实现。如果企业规模很大，拥有大量的用户，那么就要为不能互相访问的客户都分配VLAN，这不但需要消耗大量的VLAN ID，还增加了网络维护的复杂度。
通过MUX VLAN提供的二层流量隔离的机制可以实现员工之间互相交流，而客户之间互相隔离。
基本概念如表4-9所示，MUX VLAN分为Principal VLAN和Subordinate VLAN，Subordinate VLAN又分为Separate VLAN和Group VLAN。
表 4-9 MUX VLAN 划分表

| MUX VLAN | VLAN类型 | 所属接口 | 通信权限 |
|---|---|---|---|
| Principal VLAN（主 VLAN） | - | Principal port | Principal port可以和MUX VLAN 内的所有接口进行通信。 |
| Subordinate VLAN（从 VLAN） | Separate VLAN（隔离型从VLAN） | Separate port | Separate port只能和Principal port进行通信，和其他类型的接口实现完全隔离。每个Separate VLAN必须绑定一个Principal VLAN。 |
|  | Group VLAN （互通型从 VLAN） | Group port | Group port可以和Principal port 进行通信，在同一组内的接口也可互相通信，但不能和其他组接口或Separate port通信。每个Group VLAN必须绑定一个 Principal VLAN。 |

### 4.14 配置VLAN Mapping

#### 4.13.2 配置MUX VLAN

前提条件在配置MUX VLAN之前，需完成以下任务：
1. 创建VLAN。
2. 配置接口以Access、Hybrid或Trunk类型加入VLAN。
背景信息MUX VLAN分为主VLAN、互通型从VLAN、隔离型从VLAN，具体特点如下：
● 主VLAN中的接口可以与MUX VLAN内的所有接口进行通信。
● 同一互通型从VLAN中的接口之间可以互相通信，也可以和主VLAN中的接口进行通信，但不能和其他互通型从VLAN中的接口或隔离型从VLAN中的接口通信。
隔离型从VLAN中的接口只能和主VLAN中的接口进行通信。
●操作步骤步骤1 进入系统视图。
system-view步骤2 创建VLAN并进入VLAN视图。
vlan vlan-id步骤3 配置该VLAN为主VLAN。
mux-vlan步骤4 配置互通型从VLAN。
subordinate group { vlan-id1 [ to vlan-id2 ] } &<1-10>步骤5 配置隔离型从VLAN。
subordinate separate vlan-id步骤6 返回系统视图。
quit步骤 7 开启接口的 MUX VLAN 功能。有多个接口时请重复执行如下步骤。
interface interface-type interface-number port mux-vlan enable vlan { vlan-id1 [ to vlan-id2 ] } &<1-10> quit
----结束检查配置结果执行命令display mux-vlan，查看所有MUX VLAN相关配置信息。
配置
4.14 VLAN Mapping

#### 4.14.1 了解VLAN Mapping

定义及应用VLAN Mapping通过修改报文携带的VLAN Tag来实现不同VLAN的相互映射。
VLAN Mapping主要用在如下两种场景：
● 两个VLAN相同的二层用户网络通过骨干网络互联，为了实现用户之间的二层互通，以及二层协议的统一部署，需要实现两个用户网络的无缝连接，此时就需要骨干网可以传输来自用户网络的带有VLAN Tag的二层报文。而在通常情况下，骨干网的VLAN规划和用户网络的VLAN规划是不一致的，所以在骨干网中无法直接传输用户网络的带有VLAN Tag的二层报文。
通过VLAN Mapping技术，一侧用户网络的带有VLAN Tag的二层报文进入骨干网后，骨干网边缘设备将用户网络的VLAN（C-VLAN）修改为骨干网中可以识别和承载的VLAN（S-VLAN），传输到另一侧之后，边缘设备再将S-VLAN修改为C- VLAN。这样就可以很好的实现两个用户网络二层无缝连接。
● 如果由于规划的差异，导致两个直接相连的二层网络中部署的VLAN ID不一致。
但是用户又希望可以把两个网络作为单个二层网络进行统一管理，例如用户二层互通和二层协议的统一部署。此时也可以在连接两个网络的设备上部署VLAN Mapping功能，实现两个网络之间不同VLAN ID的映射，达到二层互通和统一管理的目的。
分类VLAN Mapping分为基于VLAN的VLAN Mapping和基于MQC的VLAN Mapping两类，其中基于VLAN的VLAN Mapping包括以下三种映射方式：
● 1 to 1的映射方式当部署VLAN Mapping功能设备上的接口收到带有单层VLAN Tag的报文时，将单层报文所携带的VLAN Tag替换为新的VLAN Tag。
● 2 to 1的映射方式当部署VLAN Mapping功能设备上的接口收到带有两层VLAN Tag的报文时，将两层报文携带的内、外层VLAN Tag映射为一层VLAN Tag。
● 2 to 2的映射方式
– 当部署VLAN Mapping功能设备上的接口收到带有两层VLAN Tag的报文时，将两层报文所携带的内、外层VLAN Tag都替换为新的VLAN Tag。
– 当部署 VLAN Mapping 功能设备上的接口收到带有两层 VLAN Tag 的报文时，将两层报文携带的外层Tag替换为新的VLAN Tag，内层Tag作为数据透传。
基于MQC的VLAN Mapping指的是通过MQC可以对分类后的报文实现VLAN Mapping。用户可以根据多种匹配规则对报文进行流分类，然后将流分类与VLAN Mapping的动作相关联，对匹配规则的报文重标记报文的VLAN ID值。基于MQC的VLAN Mapping能够针对业务类型提供差别服务。
基本原理设备收到带 Tag 的数据报文后，根据配置的 VLAN Mapping 方式，决定替换单层、双层或双层中的外层Tag，然后进入MAC地址学习阶段，根据源MAC地址+映射后的VLAN ID刷新MAC地址表项，根据目的MAC+映射后VLAN ID查找MAC地址表项。如果没有找到，则在VLAN ID对应的VLAN内广播，否则从表项对应的接口转发。

如图4-14所示，当DeviceA在接口interface1上配置了VLAN 2和VLAN 3映射后，接口在向外发送VLAN 2的帧时，将帧中的VLAN 2替换成VLAN 3；在接收VLAN 3的帧时，将帧中的VLAN 3替换成VLAN 2，然后按照二层转发流程进行数据转发，这样VLAN 2和VLAN 3就能实现互相通信。
说明如果需要通过VLAN Mapping实现两个VLAN内设备互相通信，这两个VLAN内设备的IP地址还必须处于同一网段。如果两个VLAN内设备的IP地址不在同一网段，那么设备间的互通需要依赖三层路由实现，这样就失去了VLAN Mapping的意义。
图 4-14 VLAN Mapping 功能示意图

#### 4.14.2 配置基于VLAN的VLAN Mapping

背景信息配置基于VLAN的VLAN Mapping功能可实现接口在接收到带单层、双层Tag时，根据配置的VLAN Mapping映射方式替换单层、双层或双层中的外层Tag为公网的VLAN Tag。
配置基于 VLAN 的 VLAN Mapping 功能可实现接口在接收到带单层 Tag 时，根据配置的VLAN Mapping映射方式替换单层Tag为公网的VLAN Tag。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入以太网接口视图。
interface interface-type interface-number步骤 3 将接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。

仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 配置接口的链路类型及接口允许通过的VLAN。根据需要选择如下一种方式进行配置。
说明
● 配置VLAN Mapping功能的接口类型必须为Trunk或Hybrid。接口必须以Tagged的方式加入映射后的VLAN。
● 若配置的映射方式是2 to 1或2 to 2时，VLAN Mapping接口上允许通过的VLAN必须是外层VLAN ID。
● 配置接口的链路类型为Trunk；并配置VLAN Mapping接口允许通过的VLAN，该VLAN为映射后的VLAN。
port link-type trunk port trunk allow-pass vlan { vlan-id1 [ to vlan-id2 ] } &<1-40>
● 配置接口的链路类型为Hybrid；并配置VLAN Mapping接口允许通过的VLAN，该VLAN为映射后的VLAN。
port link-type hybrid port hybrid tagged vlan { vlan-id1 [ to vlan-id2 ] } &<1-10>步骤5 配置VLAN Mapping功能。根据需要选择如下一种方式进行配置。
● 1 to 1的VLAN Mapping，将报文中携带的单层Tag映射为指定的Tag。
port vlan-mapping vlan vlan-id1 [ to vlan-id2 ] map-vlan vlan-id3 [ remark-8021p 8021p-value ]
● 2 to 1的VLAN Mapping，将报文中携带的两层Tag映射为指定的一层Tag。
port vlan-mapping vlan vlan-id1 inner-vlan vlan-id5 map-single-vlan vlan-id3
● 2 to 2的VLAN Mapping，将报文中携带的两层Tag中的外层Tag映射为指定的Tag，内层作为数据透传。
port vlan-mapping vlan vlan-id1 inner-vlan vlan-id5 to vlan-id6 map-vlan vlan-id3 [ remark-8021p 8021p-value ]
● 2 to 2的VLAN Mapping，将报文中携带的两层Tag映射为指定的两层Tag。
port vlan-mapping vlan vlan-id1 inner-vlan vlan-id5 map-vlan vlan-id3 map-inner-vlan vlan-id4 [ remark-8021p 8021p-value ]
----结束检查配置结果在接口视图下执行命令display this，查看接口的VLAN Mapping的配置。

#### 4.14.3 配置基于MQC的VLAN Mapping

背景信息通过MQC可以对分类后的报文实现VLAN Mapping。用户可以根据多种匹配规则对报文进行流分类，然后将流分类与VLAN Mapping的动作相关联，对匹配规则的报文重标记报文的VLAN ID值。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置流分类，详细配置请参见《配置指南-QoS配置》 MQC配置 中的“配置流分类”。

步骤3 配置流行为。
1. 创建一个流行为并进入流行为视图，或进入已存在的流行为视图。
traffic behavior behavior-name
2. 替换报文的外层VLAN Tag值。
vlan-mapping vlan vlan-id
3. （可选）替换报文的内层VLAN Tag值。
vlan-mapping inner-vlan inner-vlan-id
4. 退出流行为视图。
quit步骤4 配置流策略，详细配置请参见《配置指南-QoS配置》 MQC配置 中的“配置流策略”。
步骤5 应用流策略，详细配置请参见《配置指南-QoS配置》 MQC配置 中的“应用流策略”。
----结束检查配置结果
● 执行命令display traffic classifier [ classifier-name ]，查看流分类的配置信息。
● 执行命令display traffic behavior [ behavior-name ]，查看流行为的配置信息。
● 执行命令display traffic policy [ policy-name [ classifier classifier-name ] ]，查看流策略的配置信息。
● 执行命令display traffic-policy applied-record，查看流策略的应用记录信息。

### 4.15 配置VLAN终结

#### 4.15.1 了解VLAN终结

定义VLAN终结是指设备对接收到的报文中的VLAN标签进行识别，根据后续的转发行为对报文中的单层或双层VLAN标签进行剥除，然后进行三层转发或其他处理。也就是这些VLAN标签只在终结之前生效，之后的三层转发或其他处理不再依据报文中的这些标签。
VLAN终结的实质包含两个方面：
● 对接口接收的报文，剥除VLAN标签后进行三层转发或其他处理。
● 对接口发出的报文，将相应的VLAN标签添加到报文中后再发送。
分类根据对所终结的VLAN报文处理方式的不同，VLAN终结分为以下两种：
● Dot1q 终结：对接收到的带有一层或两层 VLAN Tag 的报文，剥除报文的最外一层VLAN Tag；对从接口发出的报文，添加一层VLAN Tag。
● QinQ终结：对接收到的带有两层VLAN Tag的报文，剥除报文的两层VLAN Tag；
对从接口发出的报文，添加两层VLAN Tag。

VLAN终结一般在子接口上进行，如果子接口是对报文中的单层VLAN标签终结，该子接口就称为Dot1q终结子接口；如果子接口是对报文中的双层VLAN标签终结，该子接口就称为QinQ终结子接口。
说明Dot1q终结子接口和QinQ终结子接口不支持透传不带VLAN Tag的报文，收到不带VLAN Tag的报文会直接丢弃。
目的划分VLAN后，VLAN内的主机可以二层互通，而VLAN间的主机不能二层互通，可以在设备上通过VLANIF来实现VLAN间的三层互通，也可以通过终结子接口实现VLAN间的三层互通。如图4-15所示，当DeviceA的三层以太网接口有限，只使用一个接口接入用户或网络时，可将一个三层以太网接口虚拟成多个逻辑子接口（相对子接口而言，这个三层以太网接口称为主接口）。
图 4-15 通过子接口互联组网图由于三层以太网子接口不支持VLAN报文，当它收到VLAN报文时，会将VLAN报文当成是非法报文而丢弃，因此，需要在子接口上将 VLAN Tag 剥掉，也就是需要 VLAN 终结。

#### 4.15.2 配置Dot1q终结子接口实现VLAN间的通信

背景信息当设备通过一个三层以太网接口接入属于不同VLAN且位于不同网段的用户时，可通过在子接口上配置Dot1q终结、配置IP地址实现三层互通。
说明为了成功实现VLAN间互通，VLAN内主机的缺省网关必须是对应子接口的IP地址。

操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤3 将接口切换到三层模式。
undo portswitch仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过undo portswitch命令将接口从二层模式切换到三层模式。
步骤4 退出接口视图。
quit步骤5 进入子接口视图。
interface interface-type interface-number.subinterface-number步骤6 配置子接口的IP地址。
ip address ip-address { mask | mask-length } [ sub ]步骤7 配置子接口终结的VLAN。
dot1q termination vid low-pe-vid说明本命令执行成功后，终结子接口对报文的处理如下：
● 接收报文时，剥掉报文中携带的Tag后进行三层转发。转发出去的报文是否带Tag由出接口决定。
● 发送报文时，将所接收的对端报文中的VLAN信息添加到报文中再发送。
子接口下配置dot1q termination vid命令后，该子接口下会自动生成encapsulation dot1q- termination的配置，即该子接口的终结封装方式为Dot1q；反之在子接口下配置undo dot1q termination vid命令后，该子接口下的encapsulation dot1q-termination配置也会同步删除。
----结束

#### 4.15.3 配置Dot1q终结子接口接入L2VPN

前提条件说明该配置仅S6780-H、S6750-H、S6750E-S、S6750-S、S6730E-H-V2、S6730-H-V2、S5755-
H、S5732-H-V2系列支持。
在配置Dot1q终结子接口接入L2VPN之前，需完成以下任务：
● 设备之间正确连接。
● 配置CE所在的VLAN和基本的二层转发功能，使PE收到的CE报文带有一层VLAN Tag。
● VCMP的角色不能是Client。

背景信息如图4-16所示，当用户跨L2VPN网络互通时，CE发往PE的业务数据报文中带有一层Tag时，可通过配置Dot1q终结子接口接入L2VPN功能实现用户间的互通。
VLAN VPN用户网络通过子接口接入运营商网络时，子接口上需要终结VLAN Tag。当CE发往PE的业务数据报文中带有一层VLAN Tag时，子接口是对报文的单层Tag终结，那么该子接口称为Dot1q终结子接口。
图 4-16 配置 Dot1q 终结子接口接入 L2VPN操作步骤步骤1 进入PE设备的系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤3 配置端口类型。
port link-type { hybrid | trunk }步骤4 退出接口视图。
quit步骤5 进入PE的CE侧子接口视图。
interface interface-type interface-number.subinterface-number步骤6 配置子接口终结的VLAN。
dot1q termination vid low-pe-vid创建某VLAN对应的VLANIF接口后，该VLAN不能再用作Dot1q终结子接口配置的VLAN、QinQ终结子接口配置的外层VLAN。
说明本命令执行成功后，终结子接口对报文的处理如下：
● 接收报文时，剥掉报文中携带的Tag后进行三层转发。转发出去的报文是否带Tag由出接口决定。
● 发送报文时，将所接收的对端报文中的VLAN信息添加到报文中再发送。
子接口下配置dot1q termination vid命令后，该子接口下会自动生成encapsulation dot1q- termination的配置，即该子接口的终结封装方式为Dot1q；反之在子接口下配置undo dot1q termination vid命令后，该子接口下的encapsulation dot1q-termination配置也会同步删除。

步骤7 配置L2VPN。
Dot1q终结子接口配置成功后，需要部署VPN业务，这样才能实现L2VPN网络两端的用户互通。L2VPN的配置步骤，请参见VPLS配置和VPWS配置。
说明Dot1q终结子接口可以支持以下方式的VPWS同种介质连接：
● BGP方式本地连接。
● BGP方式远程连接。
● LDP方式本地连接。
● LDP方式远程连接。
Dot1q终结子接口可以支持以下方式的VPLS连接：
● LDP方式的VPLS。
● BGP方式的VPLS。
----结束检查配置结果
● 执行命令display dot1q information termination [ interface { interface- name | interface-type interface-number } ]，查看封装方式为dot1q的子接口信息。
● 执行命令display vsi [ name vsi-name ] [ verbose ]，查看VPLS的VSI实例信息。
● 执行命令display vll ccc [ ccc-name | type { local | remote } ]，查看CCC连接信息。
● 执行命令display mpls static-l2vc，查看SVC方式L2VPN连接信息。
● 执行命令display mpls l2vc，在PE上查看本端LDP方式VPWS连接信息。
● 执行命令display mpls l2vc remote-info，在PE上查看远端LDP方式VPWS连接信息。

#### 4.15.4 配置QinQ终结子接口接入L2VPN

前提条件说明该配置仅S6780-H、S6750-H、S6750E-S、S6750-S、S6730E-H-V2、S6730-H-V2、S5755-
H、S5732-H-V2系列支持。
在配置QinQ终结子接口接入L2VPN之前，需完成以下任务：
● 设备之间正确连接。
配置CE所在的VLAN和基本的二层转发功能，使PE收到的CE报文带有两层VLAN
●Tag。
● VCMP的角色不能是Client。
背景信息如图4-17所示，当用户跨L2VPN网络互通，CE发往PE的业务数据报文中带有两层VLAN Tag时，可通过配置QinQ终结子接口接入L2VPN功能实现用户间的互通。

VPN用户网络通过子接口接入运营商网络时，子接口上需要终结VLAN Tag。当CE发往PE的业务数据报文中带有两层VLAN Tag时，子接口是对报文的双层Tag终结，那么该子接口称为QinQ终结子接口。
图 4-17 配置 QinQ 终结子接口接入 L2VPN操作步骤步骤1 进入PE设备的系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤3 配置端口类型。
port link-type { hybrid | trunk }步骤4 退出接口视图。
quit步骤5 进入PE的CE侧子接口视图。
interface interface-type interface-number.subinterface-number步骤6 （可选）配置QinQ终结子接口的属性。
qinq termination l2 { symmetry | asymmetry }缺省情况下，未配置QinQ终结子接口的属性。
QinQ终结子接口接入L2VPN时，PE根据子接口QinQ终结的配置、QinQ终结子接口接入VPWS/VPLS时接口的属性配置以及封装类型的配置对报文进行不同的处理，具体请参见以下表格。
说明关于封装方式，请参见命令encapsulation(子接口视图)或者mpls l2vc。

表 4-10 接入 VPLS 场景报文入接口处理

| 入接口类型 | 以太封装方式 | VLAN封装方式 |
|---|---|---|
| 对称方式 | 剥掉外层Tag。 | 不处理，两层Tag都保留。 |
| 非对称方式 | 两层Tag都剥掉。 | 剥掉外层Tag。 |
| 缺省情况 | 两层Tag都剥掉。 | 不处理，两层Tag都保留。 |

表 4-11 接入 VPLS 场景报文出接口处理

| 入接口类型 | 以太封装方式 | VLAN封装方式 |
|---|---|---|
| 对称方式 | 剥掉MPLS标签，根据子接口上QinQ终结配置的pe- vid为报文添加外层tag。 | 剥掉MPLS标签，内层报文有tag，替换报文外层tag 为子接口上配置QinQ终结的pe-vid；内层报文无 tag，根据子接口上QinQ 终结配置的pe-vid为报文添加外层tag。 |
| 非对称 | 剥掉MPLS标签，根据子接口上QinQ终结配置的ce- vid和pe-vid为报文添加两层tag。 | 剥掉MPLS标签，内层报文无tag则根据子接口上 QinQ终结配置的ce-vid和 pe-vid为报文添加两层 tag；内层报文有tag则先剥掉外层tag再根据子接口上QinQ终结配置的ce-vid 和pe-vid为报文添加两层 tag。 |
| 缺省情况 | 剥掉MPLS标签，根据子接口上QinQ终结配置的ce- vid和pe-vid为报文添加两层tag。 | 剥掉MPLS标签，内层报文透传。 |

表 4-12 接入 VPWS 场景报文入接口处理

| 入接口类型 | Raw封装方式 | Tagged封装方式 |
|---|---|---|
| 对称方式 | 剥掉外层Tag。 | 不处理，两层Tag都保留。 |
| 非对称 | 两层Tag都剥掉。 | 剥掉外层Tag。 |
| 缺省情况 | 剥掉外层Tag。 | 不处理，两层Tag都保留。 |

表 4-13 接入 VPWS 场景报文出接口处理

| 入接口类型 | Raw封装方式 | Tagged封装方式 |
|---|---|---|
| 对称方式 | 剥掉MPLS标签，根据子接口上QinQ终结配置的pe- vid为报文添加外层tag。 | 剥掉MPLS标签，内层报文有tag，替换报文外层tag 为子接口上配置QinQ终结的pe-vid；内层报文无 tag，添加子接口上配置 QinQ终结的pe-vid为报文的外层tag。 |
| 非对称 | 剥掉MPLS标签，根据子接口上QinQ终结配置的ce- vid和pe-vid为报文添加两层tag。 | 剥掉MPLS标签，内层报文无tag则根据子接口上 QinQ终结配置的ce-vid和 pe-vid为报文添加两层 tag；内层报文有tag则先剥掉外层tag再根据子接口上QinQ终结配置的ce-vid 和pe-vid为报文添加两层 tag。 |
| 缺省情况 | 剥掉MPLS标签，根据子接口上QinQ终结配置的pe- vid为报文添加外层tag。 | 剥掉MPLS标签，内层报文有tag，替换报文外层tag 为子接口上配置QinQ终结的pe-vid；内层报文无 tag，根据子接口上QinQ 终结配置的pe-vid为报文添加外层tag。 |

步骤7 配置子接口终结的内外层VLAN。
qinq termination pe-vid pe-vid ce-vid ce-vid [ to high-ce-vid ]创建某VLAN对应的VLANIF接口后，该VLAN不能再用作子接口配置的外层VLAN。
步骤8 配置L2VPN。
L2VPN的配置步骤，请参见VPLS配置和VPWS配置。
说明QinQ终结子接口可以支持以下方式的VPWS同种介质连接：
● CCC方式本地连接
● CCC方式远程连接
● SVC方式远程连接
● BGP方式本地连接
● BGP方式远程连接
● LDP方式远程连接QinQ终结子接口可以支持以下方式的VPLS连接：
● LDP 方式的 VPLS BGP方式的VPLS
●
----结束

检查配置结果
● 执行命令display qinq information termination [ interface { interface- typeinterface-number | interface-name } ]，查看封装方式QinQ的子接口信息。
● 执行命令display vsi [ name vsi-name ] [ verbose ]，查看VPLS的VSI实例信息。
● 执行命令display vll ccc [ ccc-name | type { local | remote } ]，查看CCC连接信息。
● 执行命令display mpls static-l2vc，查看SVC方式L2VPN连接信息。
● 执行命令display mpls l2vc，在PE上查看本端LDP方式VPWS连接信息。
● 执行命令display mpls l2vc remote-info，在PE上查看远端LDP方式VPWS连接信息。

### 4.16 配置QinQ

#### 4.16.1 了解QinQ

基本概念QinQ（802.1Q-in-802.1Q）技术是一项扩展VLAN空间的技术，也叫做VLAN Stacking或Double VLAN，通过在802.1Q标签报文的基础上再增加一层802.1Q Tag来达到扩展VLAN空间的功能。由于报文有两层802.1Q Tag（一层公网Tag，一层私网Tag），即802.1Q-in-802.1Q，所以称之为QinQ协议。
QinQ在公网的传输过程中，设备只根据外层VLAN Tag转发报文，而用户的私网VLAN Tag将被当作报文的数据部分进行传输。因此QinQ也是一种简单实用的VPN技术。如图4-18所示，用户网络A的私网VLAN为VLAN 1~10，用户网络B的私网VLAN为VLAN 1~20。中间公网为用户网络A和用户网络B分配的公网VLAN分别为VLAN 3和VLAN 4。当用户网络A和B中带VLAN Tag的报文进入中间公网时，报文外面就会被分别封装上VLAN 3和VLAN 4的VLAN Tag。这样，来自不同用户网络的报文在公网中传输时被完全分开，即使这些用户网络各自的VLAN范围存在重叠，在公网中传输时也不会产生冲突。当报文穿过公网到达另一侧PE设备后，报文会被剥离外层的公网VLAN Tag，然后再传送给用户网络的CE设备。

图 4-18 QinQ 典型应用组网图受益使用QinQ能给用户带来以下受益。
● 扩展VLAN空间。
IEEE 802.1Q中定义的802.1Q Tag中只有12比特用于标识VID，仅能表示4096个VLAN（即0~4095）。QinQ通过在原有的802.1Q Tag基础上再增加一层802.1Q Tag，使VLAN空间扩展到4094×4094（0和4095为协议保留取值）。
● QinQ内外层标签可以代表不同的信息，更利于业务的部署。
例如业务部署时，可以用内层标签代表用户，外层标签代表业务。
QinQ 报文封装格式如图4-19所示，QinQ报文在802.1Q Tag外层再增加一层802.1Q Tag。
QinQ报文比802.1Q报文多四个字节，因此建议用户在组网时适当增加网络中各接口的最大帧长（至少为1504字节）。当前设备缺省支持的最大帧长超过1504字节，不需要手动配置。接口允许通过的超大帧长度的相关配置请参见《CLI配置指南-接口管理》“以太网接口配置”中的“配置以太网接口通用属性”。

图 4-19 QinQ 报文封装格式QinQ 分类及实现原理QinQ分为基本QinQ和灵活QinQ。
基本QinQ基本QinQ又称为QinQ二层隧道，是基于接口方式实现的。当在接口下配置基本QinQ功能后，设备会对从该接口进来的报文加上一层本接口缺省VLAN的Tag：
● 如果接收到的是已经带有VLAN Tag的报文，该报文就成为带有双层VLAN Tag的报文。
● 如果接收到的是不带VLAN Tag的报文，该报文就成为带有接口缺省VLAN Tag的报文。
基本QinQ对进入一个接口的所有以太网帧全部封装一个相同的外层VLAN Tag，封装方式不够灵活。
灵活QinQ灵活QinQ是基于接口与VLAN相结合的方式实现的。接口对收到的报文，可以通过单层VLAN Tag转发，也可以通过双层VLAN Tag转发；并且对于从同一个接口收到的报文，还可以根据VLAN的不同进行不同的操作。例如为具有不同内层VLAN ID的报文添加不同的外层VLAN Tag，或者根据不同报文的802.1P优先级而添加不同的外层VLAN Tag。
当前设备支持多种功能的灵活QinQ。
● 基于MQC的灵活QinQ通过使用流分类中丰富的匹配规则，可以实现对特定业务流的筛选，然后对符合流分类的报文添加外层VLAN Tag。基于MQC的灵活QinQ实际上是在全局、VLAN或者端口上应用了包含VLAN Stacking流行为的流策略。
● 基于VLAN ID的灵活QinQ，可以实现对携带不同VLAN Tag的报文添加不同的外层VLAN。
● 基于802.1P优先级的灵活QinQ，可以实现对携带不同802.1P优先级的报文添加不同的外层VLAN。
● 当入方向的报文不携带任何VLAN Tag时，也可以通过配置对Untagged报文添加双层VLAN Tag的方式，实现VLAN Stacking。

#### 4.16.2 配置基本QinQ

背景信息当在接口下配置基本QinQ功能后，设备会对从该接口进来的报文加上一层VLAN Tag：
● 如果接收到的是已经带有VLAN Tag的报文，该报文就成为带有双层VLAN Tag的报文。
● 如果接收到的是不带VLAN Tag的报文，该报文就成为带有接口缺省VLAN Tag的报文。
例如为了使私网与公网有效分离，可以在设备上配置基本QinQ，内层VLAN Tag（私网VLAN Tag）用于内部网络，外层VLAN Tag（公网VLAN Tag）用于外部网络，从而满足不同私网用户之间相同VLAN的透明传输。
操作步骤步骤 1 进入系统视图。
system-view步骤2 创建VLAN。
vlan vlan-id步骤3 返回系统视图。
quit步骤4 进入以太网接口视图。
interface interface-type interface-number步骤5 将接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤 6 配置接口类型为 dot1q-tunnel 。
port link-type dot1q-tunnel步骤7 配置接口的缺省VLAN。
port default vlan vlan-id
----结束检查配置结果执行命令 display current-configuration interface interface-type interface- number，查看接口的QinQ配置。

#### 4.16.3 配置基于MQC的灵活QinQ

背景信息基于MQC的灵活QinQ通过使用流分类中丰富的匹配规则，可以实现对特定业务流的筛选，然后对符合流分类的报文添加外层VLAN Tag。基于MQC的灵活QinQ实际上是在全局、VLAN或者端口上应用了包含VLAN Stacking流行为的流策略。
说明
● 接口学习MAC地址时，学习的是QinQ报文外层VLAN的MAC地址。
● 对于需要单层透传的VLAN，请不要指定为灵活QinQ的内层VLAN。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置流分类，详细配置请参见《配置指南-QoS配置》 MQC配置 中的“配置流分类”。
步骤3 配置流行为。
1. 创建一个流行为并进入流行为视图，或进入已存在的流行为视图。
traffic behavior behavior-name
2. 配置添加外层VLAN Tag。
vlan-stacking vlan vlan-id
3. 退出流行为视图，返回到系统视图。
quit步骤4 配置流策略，详细配置请参见《配置指南-QoS配置》 MQC配置 中的“配置流策略”。
步骤5 应用流策略，详细配置请参见《配置指南-QoS配置》 MQC配置 中的“应用流策略”。
流策略可以在全局、VLAN和接口上应用。包含vlan stacking的流策略只能应用在入方向。
----结束检查配置结果
● 执行命令display traffic classifier [ classifier-name ]，查看流分类的配置信息。
● 执行命令display traffic behavior [ behavior-name ]，查看流行为的配置信息。
● 执行命令display traffic policy [ policy-name [ classifier classifier-name ] ]，查看流策略的配置信息。
● 执行命令 display traffic-policy applied-record ，查看流策略的应用记录信息。

#### 4.16.4 配置基于VLAN ID和802.1P的灵活QinQ

背景信息配置基于VLAN ID和802.1P优先级的灵活QinQ功能，可以根据进入接口的报文的VLAN ID和802.1P优先级灵活地添加外层VLAN Tag，优先保证重要用户的正常通信。
说明
● 接口类型建议为Hybrid，仅Hybrid接口区分Tagged和Untagged方式。
● 如果配置为Trunk接口，可以配置port trunk pvid vlan命令实现对携带缺省VLAN报文的VLAN Tag剥除操作。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number该接口可以是物理接口，也可以是Eth-Trunk接口。
不能在同一接口上配置MUX VLAN和灵活QinQ功能。
步骤3 将接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 配置二层接口属性为Hybrid或Trunk。
port link-type { hybrid | trunk }对于S5735I-L-V2，S5735I-S-V2，S5735I-H-V2，S5735-L-V2，S5735E-L-V2，S5735R-L-V2，S5735-S-V2，S5735E-S-V2，S5735R-S-V2，S5735S-L3，S5735S- S3，S1730S-S3系列，缺省情况下，接口的链路类型为negotiation-auto类型。
对于S5732-H-V2，S6780-H，S6750-H，S6750-S，S6750E-S，S6730-H-V2，S6730E-H-V2，S5755-H，S5755-S系列，缺省情况下，接口的链路类型为negotiation-desirable类型。
步骤5 配置接口加入VLAN。
● Hybrid接口下，配置Untagged的方式发送帧，以Untagged形式将Hybrid类型接口加入VLAN。
port hybrid untagged vlan { { vlan-id1 [ to vlan-id2 ] } &<1-10> | all }
● Hybrid接口下，配置Tagged的方式发送帧，以Tagged的形式将Hybrid类型接口加入VLAN。
port hybrid tagged vlan { { vlan-id1 [ to vlan-id2 ] } &<1-40> | all }
● Trunk 接口下，配置将 Trunk 类型接口加入 VLAN 。
port trunk allow-pass vlan { { vlan-id1 [ to vlan-id2 ] } &<1-40> | all }一个内层VLAN在一个接口上只能叠加一个外层VLAN，且叠加后的外层VLAN必须是设备上已经存在的VLAN，叠加前的VLAN可以不创建。

步骤6 根据需要，选择配置入接口的灵活QinQ功能。
● 基于VLAN ID的灵活QinQ功能。
port vlan-stacking vlan vlan-id1 [ to vlan-id2 ] stack-vlan vlan-id3 [ remark-8021p 8021p-value3 ]
● 基于802.1P优先级的灵活QinQ功能。
port vlan-stacking 8021p low-8021p stack-vlan vlan-id3 [ remark-8021p 8021p-value3 ]
● 基于VLAN ID和802.1P优先级的灵活QinQ功能。
port vlan-stacking vlan vlan-id1 [ to vlan-id2 ] 8021p low8021p [ to high8021p ] stack-vlan vlan- id3 [ remark-8021p 8021p-value3 ]缺省情况下，外层VLAN优先级与内层VLAN优先级保持一致。
当接口的PVID不是缺省值VLAN1时，需要恢复接口的PVID为缺省值后才可以配置port vlan-stacking命令。
基于VLAN ID和802.1P优先级的灵活QinQ功能仅对入方向的报文生效。
步骤7 退出接口视图，返回到系统视图。
quit步骤8 进入接口视图。
interface interface-type interface-number该接口与步骤2中的接口不同，该接口是QinQ报文需要转发出去的接口。
步骤9 配置接口属性。
port link-type trunk步骤10 配置接口加入需要通过的外层VLAN。
port trunk allow-pass vlan { { vlan-id1 [ to vlan-id2 ] } &<1-40> | all }
----结束检查配置结果执行命令display current-configuration interface interface-type interface- number，查看接口的灵活QinQ配置信息。

#### 4.16.5 配置对Untagged报文添加双层VLAN Tag

背景信息通常，若要给报文打上双层Tag，需要通过两台设备完成。配置该功能后：
● 可实现通过一台设备给报文打上两层Tag，方便了用户配置。
● 也可实现当二层接口收到Untagged报文后根据实际业务或用户添加双层Tag，达到区分业务或用户的目的。
说明
● 接口类型建议为Hybrid，仅Hybrid接口区分Tagged和Untagged方式。
● 如果配置为Trunk接口，可以配置port trunk pvid vlan命令实现对携带缺省VLAN报文的VLAN Tag剥除操作。
操作步骤步骤1 进入系统视图。

system-view步骤2 创建添加的外层VLAN。
vlan vlan-id步骤3 返回系统视图。
quit步骤4 进入接口视图。
interface interface-type interface-number该接口可以是物理接口，也可以是Eth-Trunk接口。
步骤5 将接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤 6 配置二层接口属性为 Hybrid 或 Trunk 。
port link-type { hybrid | trunk }对于S5735I-L-V2，S5735I-S-V2，S5735I-H-V2，S5735-L-V2，S5735E-L-V2，S5735R-L-V2，S5735-S-V2，S5735E-S-V2，S5735R-S-V2，S5735S-L3，S5735S- S3，S1730S-S3系列，缺省情况下，接口的链路类型为negotiation-auto类型。
对于S5732-H-V2，S6780-H，S6750-H，S6750-S，S6750E-S，S6730-H-V2，S6730E-H-V2，S5755-H，S5755-S系列，缺省情况下，接口的链路类型为negotiation-desirable类型。
步骤7 配置接口加入VLAN。
● Hybrid接口下，配置Untagged的方式发送帧，以Untagged形式将Hybrid类型接口加入VLAN。
port hybrid untagged vlan { { vlan-id1 [ to vlan-id2 ] } &<1-10> | all }
● Trunk接口下，配置将Trunk类型接口加入VLAN。
port trunk allow-pass vlan { { vlan-id1 [ to vlan-id2 ] } &<1-40> | all }步骤8 配置对Untagged报文添加双层VLAN Tag。
port vlan-stacking untagged stack-vlan vlan-id3 stack-inner-vlan stackInnerVid当接口的PVID不是缺省值VLAN1时，需要恢复接口的PVID为缺省值后才可以配置port vlan-stacking命令。
步骤9 退出接口视图，返回到系统视图。
quit步骤10 进入接口视图。
interface interface-type interface-number该接口与步骤2中的接口不同，该接口是QinQ报文需要转发出去的接口。
步骤11 配置接口属性。
port link-type trunk步骤 12 配置接口加入需要通过的外层 VLAN 。
port trunk allow-pass vlan { { vlan-id1 [ to vlan-id2 ] } &<1-40> | all }
----结束

检查配置结果
● 在入接口的接口视图下执行命令display this，查看入接口的VLAN Stacking的配置信息。
在出接口的接口视图下执行命令display this，查看出接口的VLAN Stacking的配
●置信息。

#### 4.16.6 配置外层VLAN Tag的TPID值

背景信息VLAN Tag中的TPID（Tag Protocol Identifier）字段代表VLAN Tag的协议类型，IEEE
802.1Q协议规定该字段的取值为0x8100。在不同的网络规划或不同厂商设备的QinQ报文中，外层VLAN Tag的TPID值可能不同。此时用户可以配置设备外层VLAN Tag的TPID值，从而实现与现有网络规划或其他厂商设备兼容。
● 为了实现与不同厂商的设备互通，配置外层VLAN Tag的TPID值需要和该接口相连的设备能够识别的TPID值相同。
● 配置设备外层 VLAN Tag 的 TPID 值后，在入方向是对报文起到识别的作用，在出方向是对报文的TPID进行修改或添加。
● 设备不能在dot1q-tunnel类型接口下配置外层VLAN Tag的TPID值。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入以太网接口视图。
interface interface-type interface-number步骤3 将接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤 4 配置外层 VLAN Tag 的 TPID 值。
qinq protocol ethertype-value设备支持配置的TPID值包括0x8100、0x9100、0x88a8。缺省情况下，外层VLAN Tag的TPID值为0x8100。
----结束

### 4.17 配置QinQ Mapping

说明该配置仅S6780-H、S6750-H、S6750E-S、S6750-S、S6730E-H-V2、S6730-H-V2、S5755-
H、S5732-H-V2系列支持。

#### 4.17.1 了解QinQ Mapping

QinQ Mapping 的基本原理QinQ Mapping发生在报文从入接口接收进来之后，从出接口转发出去之前。
● 子接口在向外发送本地VLAN帧时，将帧中的VLAN Tag替换成外部VLAN的VLAN Tag。
● 在接收外部VLAN的帧时，将帧中的VLAN Tag替换成本地VLAN的VLAN Tag。
在实际组网中，QinQ Mapping功能可以将用户的VLAN Tag映射为运营商的VLAN Tag，从而起到屏蔽不同用户VLAN Tag的作用。
QinQ Mapping功能一般部署在ME边缘设备上，对用户侧上送的报文进行映射操作。
将用户报文携带的Tag映射用户指定的Tag后再接入公网。QinQ Mapping功能常应用于但不局限于以下场景：
● 新局点和老局点部署的VLAN ID冲突，但是新局点需要与老局点互通。
● 接入公网的各个局点规划不一致，导致VLAN ID冲突，但是各个局点之间不需要互通。
公网两端的VLAN ID规划不对称。
●目前，设备支持以下几种映射方式：
● 1 to 1的映射方式当部署QinQ Mapping功能设备上的子接口收到带有一层Tag的报文时，将报文中携带的一层Tag映射为用户指定的一层Tag。
● 2 to 1的映射方式当部署QinQ Mapping功能的子接口收到带有两层Tag的报文后，将报文中携带的外层Tag映射为用户指定的一层Tag，内层VLAN不变。
图 4-20 QinQ Mapping 功能示意图说明图中interface1、interface2分别代表10GE1/0/1.1、10GE1/0/2。

如图4-20所示，当在DeviceB和DeviceC的子接口10GE1/0/1.1上配置了1 to 1的映射后，以PC1向PC2发送帧为例：
1. PC1发送Untagged帧到DeviceA，封装一层VLAN Tag 20。
2. DeviceA发送带VLAN Tag 20的帧到DeviceB，在10GE1/0/1.1接口把帧的VLAN Tag 20替换为VLAN Tag 50。
3. DeviceB上的接口10GE1/0/2向外发送的帧中携带的Tag是运营商的VLAN Tag 50。
4. ISP网络透传DeviceB发送的帧。
5. DeviceC上的接口10GE1/0/1.1收到DeviceB发送过来的数据帧后，将帧中的VLAN替换为VLAN 40。
Tag 50 Tag PC2向PC1发送帧的流程同理。
由此通过QinQ Mapping的1 to 1 映射方式，实现了PC1和PC2的互通。
QinQ Mapping 与 VLAN Mapping QinQ Mapping与VLAN Mapping的比较表4-14如所示。
表 4-14 QinQ Mapping 与 VLAN Mapping 差异表

| Mapping 类型 | 相同点 | 不同点 |
|---|---|---|
| 1 to 1 | 接口收到Tagged帧后，将帧中的一层Tag映射为用户指定的一层Tag。 | ● QinQ Mapping的映射动作发生在子接口上，并且主要用于接入VPLS网络。 ● VLAN Mapping的映射动作发生在主接口上，并且主要用于通过VLAN转发的二层网络。 |
| 2 to 1 | 入接口收到的帧带有两层Tag。将帧中的外层 Tag映射为用户指定的一层Tag，内层Tag作为业务数据透传。 | ● QinQ Mapping的映射动作发生在子接口上，并且主要用于接入VPLS网络。 ● VLAN Mapping的映射动作发生在主接口上，并且主要用于通过VLAN转发的二层网络。 |

#### 4.17.2 配置1 to 1的QinQ Mapping功能

背景信息在子接口上部署1 to 1的QinQ Mapping功能，当子接口收到带有一层Tag的报文后，将报文中携带的一层Tag映射为用户指定的一层Tag。
操作步骤步骤 1 进入系统视图。
system-view步骤2 进入接口视图。

interface interface-type interface-number步骤3 配置端口类型。
port link-type { hybrid | trunk }步骤4 退出接口视图。
quit步骤5 进入PE的CE侧以太网子接口或Eth-Trunk子接口视图。
interface interface-type interface-number.subinterface-number步骤6 将报文中携带的一层Tag映射为指定的Tag。
qinq mapping vid vid [ to vlanId2 ] map-vlan vid map-vid对于带有一层Tag的报文，将携带的一层Tag映射为另一层Tag，映射前的Tag和其他子接口下的外层Tag互斥，两者取值不能相同。
说明如果已经在子接口上配置QinQ Mapping功能，那么不能再配置Stacking、QinQ终结、Dot1q终结相关命令。
---- 结束

#### 4.17.3 配置2 to 1的QinQ Mapping功能

背景信息在子接口上部署2 to 1的QinQ Mapping功能，当子接口收到带有两层Tag的报文后，将报文中携带的外层Tag映射为用户指定的一层Tag，内层VLAN不变。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤3 配置端口类型。
port link-type { hybrid | trunk }步骤4 退出接口视图。
quit步骤5 进入PE的CE侧以太网子接口或Eth-Trunk子接口视图。
interface interface-type interface-number.subinterface-number步骤6 将携带两层Tag的报文中的外层Tag映射为用户指定的Tag。
qinq mapping pe-vid peVid ce-vid ceVid [ to ceVid2 ] map-vlan vid map-vid映射前的外层Tag和其他子接口下的外层Tag互斥，两者取值不能相同。
说明如果已经在子接口上配置QinQ Mapping功能，那么不能再配置Stacking、QinQ终结、Dot1q终结相关命令。
----结束

### 4.18 配置QinQ Stacking

说明该配置仅S6780-H、S6750-H、S6750E-S、S6750-S、S6730E-H-V2、S6730-H-V2、S5755-
H、S5732-H-V2系列支持。

#### 4.18.1 了解QinQ Stacking

定义及应用早期QinQ技术主要应用于二层网络中，部署在CE设备（二层设备）上，通过VLAN Stacking技术进行VLAN叠加，通过外层VLAN进行二层转发。而QinQ Stacking子接口一般部署在PE设备上，QinQ Stacking子接口能够识别用户的VLAN后对用户的二层数据帧进行VLAN叠加操作。
当用户报文接入L2VPN网络时，如果通过主接口接入L2VPN，这样就无法满足在同一个物理接口接入多个用户需求，缺少灵活性。此时可部署 QinQ Stacking 子接口绑定VSI或L2VC接入L2VPN网络，解决同一个物理接口接入多个用户的需求。
说明
● QinQ Stacking子接口必须和L2VPN结合起来部署才有意义，QinQ Stacking子接口不支持三层转发功能。L2VPN的具体介绍，请参见VPLS配置和VPWS配置。
● 通过QinQ Stacking或QinQ Mapping子接口接入VPLS网络，二层组播流量从网络侧到QinQ Stacking或QinQ Mapping子接口时，接口先剥掉外层Tag，再封装学习到的两层Tag后向下游设备转发。

#### 4.18.2 配置QinQ Stacking子接口接入L2VPN

背景信息在以太网子接口上部署QinQ Stacking功能：
● QinQ Stacking子接口接收报文时，先检查报文中的是否携带VLAN Tag，如果报文中没有携带VLAN Tag，直接丢弃该报文。如果携带VLAN Tag，接口按照下方式处理报文：
– 如果报文中携带一层 VLAN Tag ，且 VLAN Tag 和 vid low-ce-vid [ to high-ce- vid ]中指定的VLAN Tag一致，则在设定范围内的用户报文上再打上一层外层Tag。否则丢弃该报文。
VLAN
– 如果报文中携带两层VLAN Tag，且外层VLAN Tag和vid low-ce-vid [ to high-ce-vid ]中的指定的VLAN Tag一致，则在设定范围内的用户报文上再打上一层外层VLAN Tag，内层VLAN Tag作为数据透传。否则丢弃该报文。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入PE的用户侧以太网子接口视图。
interface interface-type interface-number.subinterface-number

步骤3 配置QinQ Stacking子接口。
qinq stacking vid low-ce-vid [ to high-ce-vid ] pe-vid pevid说明主接口和该主接口的子接口不能对同一VLAN进行VLAN Mapping或VLAN Stacking配置。
如果子接口下需要配置多个QinQ Stacking，建议使用qinq stacking vid low-ce-vid to high- ce-vid pe-vid pevid命令合并配置。
步骤4 配置L2VPN。
L2VPN的配置步骤，请参见VPLS配置和VPWS配置，在需要配置L2VPN的设备上进行如下配置。
1. 进入系统视图。
system-view
2. 进入已经成功配置QinQ Stacking子接口视图。
interface interface-type interface-number.subinterface-number
3. 根据部署的业务，配置QinQ Stacking子接口接入L2VPN如表4-15所示。
表 4-15 QinQ Stacking 子接口接入 L2VPN

| 业务类型 | QinQ Stacking子接口配置 |
|---|---|
| VPWS | 执行命令mpls l2vc { ip-address | pw-template pw- template-name } *vc-id [ [ control-word | no-control- word ] | [ raw | tagged ] | tunnel-policy policy-name | [ secondary | bypass ] | ignore-standby-state ] *，创建 VPWS连接。 |
| VPLS | 执行命令l2 binding vsi vsi-name，将终结子接口和VSI实例绑定。 |

说明QinQ Stacking子接口接入VPWS时，要求两端用户VLAN必须对称。
----结束检查配置结果
● 执行 display qinq information stacking [ interface { interface-type interface- number | interface-name } ]命令，查看QinQ Stacking子接口配置信息。
● 查看CCC方式连接的L2VPN配置信息：
– 执行命令display vll ccc [ ccc-name | type { local | remote } ]，查看CCC连接信息。
– 执行命令display l2vpn ccc-interface vc-type ccc [ up | down ]，查看CCC连接的接口信息。
● 查看LDP方式连接的L2VPN配置信息：
– 执行命令 display mpls l2vc [ vc-id | interface interface-type interface- number ]，在PE上查看本端LDP方式VPWS连接信息。
– 执行命令display mpls l2vc remote-info [ vc-id | unmatch | verbose ]，在PE上查看远端LDP方式VPWS连接信息。

● 查看BGP方式连接的L2VPN配置信息：
– 执行命令display mpls l2vpn [ l2vpn-name [ local-ce | remote-ce ] ]，查
看BGP方式VPWS信息。
– 执行命令display mpls l2vpn connection l2vpn-name [ remote-ce
remote-ce-id | down | up | verbose ]，查看BGP方式VPWS连接信息。
● 查看SVC方式连接的L2VPN配置信息：
– 执行命令display mpls static-l2vc [ vc-id | interface interface-type
interface-number | state { down | up } | brief ]，查看在PW两端的设备上
查看静态PW信息。

### 4.19 配置Voice VLAN

#### 4.19.1 了解Voice VLAN

Voice VLAN 定义及分类Voice VLAN是为用户的语音流专门划分的VLAN。
网络中经常有数据、语音、视频等多种流量同时传输。因为丢包和时延对通话质量的影响很大，用户对语音的质量比数据或者视频的质量更为敏感，因此在带宽有限的情况下就需要优先保证通话质量。通过配置Voice VLAN，设备可识别语音流，将语音流加入到Voice VLAN中传输，并对其进行有针对性的QoS保障，当网络发生拥塞时可以优先保证语音流的传输。
Voice VLAN可以通过以下两种方式来实现对语音数据流的识别：
● 通过收到报文的源MAC地址，即基于MAC地址的方式设备可以根据进入接口的数据报文中的源MAC地址字段来判断该数据流是否为语音数据流。源MAC地址匹配系统设置的语音设备的组织唯一标识符OUI（Organizationally Unique Identifier）的报文被认为是语音数据流。用户需要预先设置OUI，适用于IP电话上送untagged语音报文的场景。
● 通过报文携带的VLAN Tag，即基于VLAN的方式若有大量IP电话接入设备，配置IP电话的OUI会非常繁琐。可在设备上配置基于VLAN来提升语音报文的优先级，此时设备会根据进入接口的报文的VLAN ID来判断该数据报文是否为语音报文。当VLAN ID匹配系统配置的Voice VLAN后，则认为是语音数据流。这种方式实现的前提是IP电话支持获取设备上配置的Voice VLAN 信息，在大量 IP 电话接入的情况下，可以简化配置。
以上方案是从方便配置的角度给出的。实际上，不管IP电话上送的语音报文是否带VLAN Tag，基于MAC地址和基于VLAN的Voice VLAN都可以实现。主要区别在于：当IP电话上送的是untagged语音报文时，必须配置OUI，才能把语音报文和数据报文区分开来；如果IP电话上送的是带Tag语音报文，则可配置基于VLAN的Voice VLAN，这样在大量IP电话接入的情况下，就不用配置繁琐的OUI，简化配置。
基于 MAC 地址的 Voice VLAN
● OUI OUI指的是MAC地址的前24位（二进制），可以用来表示一个MAC地址段，是IEEE为不同设备供应商分配的一个全球唯一的标识符，各设备厂商再从这个地址段中分配24位，从而形成48位的MAC地址。所以根据OUI识别IP电话机的原理就

是根据IP电话厂商申请的MAC地址段来识别哪些报文是话机发送的，以此来判断哪些报文属于语音报文。
Voice VLAN中的OUI有别于上述的通常意义的OUI，这个OUI是由用户来配置的，而且可以使用掩码，即不需要一定是24位掩码的，掩码长度用户可以自己指定。
OUI的值为voice-vlan mac-address命令中的mac-address和oui-mask参数相与的结果。
● 实现原理如图4-21所示，设备接收到PC和IP Phone发出的untagged报文后会做如下处理：
如果源MAC匹配设备上配置的OUI（源MAC地址与配置的OUI掩码进行与运算后等于OUI视为匹配），则为该报文加上Voice VLAN的Tag，并提升报文优先级；如果不匹配，就会为其加上PVID的VLAN Tag，从而保证语音报文的优先发送。
图 4-21 基于 MAC 地址的 Voice VLAN 示意图基于 VLAN 的 Voice VLAN基于VLAN的Voice VLAN实现原理如下：
设备收到PC和IP Phone发来的报文后会判断报文的VLAN ID与接口上配置的Voice VLAN ID是否相同，如果相同则认为此数据流为语音数据流并提升优先级。PC发出的untagged报文则会被加上PVID的VLAN Tag。因此基于VLAN的Voice VLAN需要IP Phone可以获取设备上配置的Voice VLAN信息。
IP Phone获取设备上Voice VLAN信息的方法有很多种，以下以IP Phone通过LLDP协议获取设备Voice VLAN信息为例介绍一下实现过程。
图 4-22 基于 VLAN 的 Voice VLAN 示意图
1. 如图4-22所示，IP电话上线会主动发送LLDP报文，以获取设备上配置的Voice VLAN信息；

2. 设备收到IP电话发送的LLDP报文，会在相关字段填充Voice VLAN信息发给IP电
话；
3. IP电话收到携带Voice VLAN信息的LLDP报文后，再次发送语音报文时就会带Tag
发送；
4. 设备收到带Tag的语音报文，如果Tag和设备上配置的Voice VLAN匹配，则为其提
升优先级后转发。
设备收到untagged报文，仍然会加入到PVID所在的VLAN中。这样，当发生网络拥塞
的时候设备就能保证语音报文的优先发送。
Voice VLAN 的安全模式和普通模式
根据使能了Voice VLAN功能的接口对接收到的数据包的过滤机制可以将Voice VLAN的
工作模式分为安全模式和普通模式。
不同的Voice VLAN模式介绍如表4-16所示。
表 4-16 Voice VLAN 的安全模式和普通模式

| Voic e VLA N模式 | 场景 | 处理报文的方式 | 注意事项 |
|---|---|---|---|
| 安全模式 | 使能了Voice VLAN功能的入接口只允许收到的源地址与OUI匹配的语音报文通过，该Voice VLAN内的非语音报文将被直接丢弃，其他 VLAN内的报文正常转发。 | 判断该报文源MAC地址和OUI不匹配：不修改优先级并禁止数据在 Voice VLAN内转发。判断该报文源MAC地址和OUI匹配：修改优先级并允许在Voice VLAN 内转发。 | 只有指定语音报文基于 MAC地址提升优先级时，安全模式才会生效。 |
| 普通模式 | 使能了Voice VLAN功能的入接口允许同时传输语音报文和非语音报文，容易受到恶意数据流量的攻击。 | 判断该报文源MAC地址和OUI不匹配：不修改优先级并允许数据在 Voice VLAN内转发。判断该报文源MAC地址和OUI匹配：修改优先级并允许在Voice VLAN 内转发。 | 不建议将语音和数据业务规划在同一个VLAN 里面。如确有此需要，请确认Voice VLAN工作在普通模式。 |

#### 4.19.2 配置Voice VLAN（基于MAC地址识别语音报文）

背景信息基于MAC地址方式下，设备可以根据进入接口的数据报文中的源MAC地址字段来判断该数据流是否为语音数据流。源MAC地址匹配设备配置的语音设备OUI的报文被认为是语音数据流并提升优先级。

操作步骤步骤1 进入系统视图。
system-view步骤2 配置Voice VLAN的OUI。
voice-vlan mac-address mac-address mask oui-mask [ description text ]缺省情况下，未配置Voice VLAN的OUI。
步骤3 进入接口视图。
interface interface-type interface-number步骤4 将接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤 5 指定 VLAN 是 Voice VLAN ，同时使能接口的 Voice VLAN 功能。
voice-vlan vlan-id enable [ include-untagged ]缺省情况下，接口未使能Voice VLAN功能。
步骤6 配置语音报文按照MAC地址提升优先级。
voice-vlan remark-mode mac-address缺省情况下，语音报文按照VLAN提升报文优先级。
步骤7 配置接口加入VLAN。详细配置请参见4.8.2 配置基于接口划分VLAN（静态配置接口类型）。
步骤8 （可选）配置Voice VLAN的工作模式为安全模式。
voice-vlan security enable缺省情况下，Voice VLAN的工作模式是普通模式。
----结束

#### 4.19.3 配置Voice VLAN（基于VLAN识别语音报文）

背景信息在基于VLAN的Voice VLAN模式下，当设备接口上收到的报文携带VLAN ID与系统配置的Voice VLAN ID相同时，该报文就被认为是语音报文并提升优先级。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤3 将接口从三层模式切换到二层模式。
portswitch

请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口从三层模式切换到二层模式。
步骤4 指定VLAN是Voice VLAN，同时使能接口的Voice VLAN功能。
voice-vlan vlan-id enable [ include-untagged ]步骤5 配置语音报文按照VLAN提升优先级。
voice-vlan remark-mode vlan步骤6 配置接口加入VLAN。详细配置请参见4.8.2 配置基于接口划分VLAN（静态配置接口类型）。
步骤7 使用LLDP协议，将Voice VLAN信息通告给IP Phone。
quit lldp enable interface interface-type interface-number undo lldp disable缺省情况下，全局LLDP功能处于开启状态。全局LLDP功能开启后，缺省情况下接口LLDP功能处于开启状态。
----结束

#### 4.19.4 （可选）调整Voice VLAN的802.1p和DSCP优先级

背景信息相对于数据业务，语音业务对网络实时性要求更高。通过调整Voice VLAN的802.1p优先级、DSCP优先级，可以使Voice VLAN内的语音报文以更高的优先级进行传输，从而保证语音业务的传输质量。
如需了解802.1p优先级和DSCP优先级，可以参见《CLI配置指南-QoS配置》中的“报文重标记原理”。
操作步骤步骤1 进入系统视图。
system-view步骤 2 配置 Voice VLAN 的 802.1p 和 DSCP 优先级。
voice-vlan remark { 8021p 8021p-value | dscp dscp-value } *缺省情况下，Voice VLAN的802.1p优先级是5，DSCP优先级是46。
----结束

#### 4.19.5 检查Voice VLAN的配置结果

操作步骤
● 执行命令 display voice-vlan oui ，查看 Voice VLAN 的 OUI 及其相关属性。
● 执行命令display voice-vlan [ vlan-id ] status，查看Voice VLAN的相关信息。
----结束

### 4.20 配置VLAN内未知报文隔离

背景信息如果用户希望隔离VLAN内的未知报文，包括广播报文、未知单播报文、未知组播报文、同时不影响报文上送CPU，则可以配置VLAN内未知报文隔离功能。适用于大中型园区，汇聚交换机，接入交换机通过配置DHCP Option 148自动化开局上线场景。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入VLAN视图。
vlan vlan-id步骤3 隔离VLAN内未知报文。
unknown-flow drop
----结束

### 4.21 配置VLAN透传

#### 4.21.1 配置VLAN透传，提高设备转发效率

前提条件在配置VLAN透传，提高设备转发效率之前，需完成以下任务：
● VLAN已经创建，详见“4.5 创建和删除VLAN”。
● VLAN已经划分，详见“4.8.2 配置基于接口划分VLAN（静态配置接口类型）”、“4.8.4 配置基于MAC地址划分VLAN”、“4.8.5 配置基于子网划分VLAN”、“4.8.6 配置基于协议划分VLAN”。
背景信息VLAN透传功能是指设备直接透明传输指定VLAN内的报文，不会上送CPU处理，从而提高设备的转发效率。经过CPU处理的转发机制称为软转发，软转发增加了报文的处理环节，会对报文的转发速度和效率造成较大影响。
说明仅S6780-H、S6750-H、S6750-S、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S5732-H-V2系列支持配置VLAN透传功能。
操作步骤步骤1 进入系统视图。
system-view

步骤2 进入VLAN视图。
vlan vlan-id步骤3 配置VLAN透传功能。
protocol-transparent缺省情况下，未启用VLAN透传功能。
----结束检查配置结果在VLAN视图下执行命令display this，可以查看VLAN透传功能是否已经成功配置。

### 4.22 配置丢弃入方向的Tagged报文，防止接口被私自接入其他设备

背景信息网络中主机用户发送的都为Untagged报文。当设备某接口规划用作接入主机用户时，接口只需要处理Untagged报文。为了防止主机用户私自更改接口用途，接入其他设备，可以配置接口丢弃入方向的Tagged报文。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入以太网接口视图。
interface interface-type interface-number步骤3 将接口从三层模式切换到二层模式。
portswitch请用户根据实际接口类型自行选择是否要执行此步骤。
仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S6750-
S 、 S6750E-S 、 S5732-H-V2 系列支持通过 portswitch 命令将接口从三层模式切换到二层模式。
步骤4 配置接口丢弃入方向的Tagged报文。
port discard tagged-packet缺省情况下，接口不丢弃入方向的Tagged报文。
----结束检查配置结果在接口视图下执行命令display this，可以查看接口丢弃入方向Tagged报文的配置信息。

### 4.23 维护VLAN

维护 VLAN 报文的流量信息在VLAN视图下执行命令statistics enable，启用VLAN报文的流量统计功能。
system-view vlan vlan-id statistics enable须知清除的操作务必仔细确认，一旦执行成功后，以前的信息将无法恢复。
维护VLAN流量的相关操作，如表4-17所示。
表 4-17 维护 VLAN 的流量信息

| 操作 | 命令 |
|---|---|
| 查看VLAN报文的流量信息 | display vlan vlan-id statistics [ slot slot-id ] |
| 清除VLAN报文的统计信息 | reset vlan vlan-id statistics [ slot slot- id ] |

维护 VLANIF 接口的流量信息在VLANIF接口视图下执行命令statistics { ipv4 | ipv6 } enable [ inbound | outbound ]，启用VLANIF接口的流量统计功能。
VLANIF接口统计的是该VLAN下所有的三层转发流量，即通过该VLANIF接口的流量信息都会被统计到。
须知清除的操作务必仔细确认，一旦执行成功后，以前的信息将无法恢复。
维护VLANIF接口流量的相关操作，如表4-18所示。
表 4-18 维护 VLANIF 接口的流量信息

| 操作 | 命令 |
|---|---|
| 查看VLANIF接口的流量信息 | display interface vlanif [ interface- number ] |

| 操作 | 命令 |
|---|---|
| 清除VLANIF接口的统计信息 | reset interface counters vlanif [ interface-number ] |

查看 VLAN 相关资源统计信息执行命令display fwm vlan statistics [ slot slot-id | ipc | resource-apply ]，查看VLAN相关资源的统计信息。

### 4.24 VLAN配置举例

#### 4.24.1 举例：配置基于接口划分VLAN（静态配置接口类型），实现同一VLAN内的互通（同设备）

组网需求如图4-23所示，把连接Host1和Host2的接口划分到VLAN2，把连接Host3和Host4的接口划分到VLAN3，实现同一VLAN内的主机可以通信，不同VLAN内的主机不能直接二层通信。
● Host1和Host2可以互相通信，Host3和Host4可以互相通信。
● Host1和VLAN3内的Host3、Host4不能互相通信，Host2和VLAN3内的Host3、Host4不能互相通信。
图 4-23 基于接口划分 VLAN 组网图（同设备）
说明本例中interface1、interface2、interface3、interface4分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3、10GE1/0/4。

操作步骤步骤1 创建VLAN，并配置设备与主机相连的接口为Access类型接口。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 2 3 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type access [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type access [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] portswitch [DeviceA-10GE1/0/3] port link-type access [DeviceA-10GE1/0/3] quit [DeviceA] interface 10ge 1/0/4 [DeviceA-10GE1/0/4] portswitch [DeviceA-10GE1/0/4] port link-type access [DeviceA-10GE1/0/4] quit步骤2 配置接口加入VLAN。
\# 将10GE1/0/1和10GE1/0/2接口加入VLAN2。
[DeviceA] vlan 2 [DeviceA-vlan2] port 10ge 1/0/1 to 1/0/2 [DeviceA-vlan2] quit \# 将10GE1/0/3和10GE1/0/4接口加入VLAN3。
[DeviceA] vlan 3 [DeviceA-vlan3] port 10ge 1/0/3 to 1/0/4 [DeviceA-vlan3] quit
----结束检查配置结果\# 执行display vlan命令可以查看VLAN状态。
[DeviceA] display vlan The total number of vlans is : 2
-------------------------------------------------------------------------------- U: Up; D: Down; TG: Tagged; UT: Untagged; MP: Vlan-mapping; ST: Vlan-stacking; \#: ProtocolTransparent-vlan; *: Management-vlan; MAC-LRN: MAC-address learning; STAT: Statistic; BC: Broadcast; MC: Multicast; UC: Unknown-unicast; FWD: Forward; DSD: Discard;
-------------------------------------------------------------------------------- VID Ports
-------------------------------------------------------------------------------- 2 UT:10GE1/0/1(U) 10GE1/0/2(U)
3 UT:10GE1/0/3(U) 10GE1/0/4(U)
VID Type Status Property MAC-LRN STAT BC MC UC Description
-------------------------------------------------------------------------------- 2 common enable default enable disable FWD FWD FWD VLAN 0002 3 common enable default enable disable FWD FWD FWD VLAN 0003 \# VLAN2的主机无法Ping通VLAN3内的主机，但是同一VLAN内的主机可以互相Ping通。

配置脚本\# sysname DeviceA \# vlan batch 2 to 3 \# interface 10GE1/0/1 port link-type access port default vlan 2 \# interface 10GE1/0/2 port link-type access port default vlan 2 \# interface 10GE1/0/3 port link-type access port default vlan 3 \# interface 10GE1/0/4 port link-type access port default vlan 3 \# return

#### 4.24.2 举例：配置基于接口划分VLAN（静态配置接口类型），实现同一VLAN内的互通（跨设备）

组网需求如图4-24所示，把Host1、Host2、Host5、Host6划分到VLAN2，把Host3、Host4、Host7、Host8划分到VLAN3。DeviceA与DeviceC、DeviceC与DeviceB之间相连的链路允许VLAN2和VLAN3的报文通过。希望实现DeviceA和DeviceB下属于同一VLAN内的主机可以直接通信，属于不同VLAN间的主机不能直接进行二层通信。
图 4-24 基于接口划分 VLAN 组网图（跨设备）
说明本例中interface1、interface2、interface3、interface4、interface5分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3、10GE1/0/4、10GE1/0/5。
操作步骤步骤 1 配置 DeviceA 、 DeviceB 与主机相连的接口为 Access 类型的接口，并将 Host1 、 Host2 、Host5、Host6划分到VLAN2，将Host3、Host4、Host7、Host8划分到VLAN3。
\# 配置DeviceA。

<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 2 3 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type access [DeviceA-10GE1/0/1] port default vlan 2 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type access [DeviceA-10GE1/0/2] port default vlan 2 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] portswitch [DeviceA-10GE1/0/3] port link-type access [DeviceA-10GE1/0/3] port default vlan 3 [DeviceA-10GE1/0/3] quit [DeviceA] interface 10ge 1/0/4 [DeviceA-10GE1/0/4] portswitch [DeviceA-10GE1/0/4] port link-type access [DeviceA-10GE1/0/4] port default vlan 3 [DeviceA-10GE1/0/4] quit \# 配置DeviceB。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan batch 2 3 [DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] portswitch [DeviceB-10GE1/0/1] port link-type access [DeviceB-10GE1/0/1] port default vlan 2 [DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] portswitch [DeviceB-10GE1/0/2] port link-type access [DeviceB-10GE1/0/2] port default vlan 2 [DeviceB-10GE1/0/2] quit [DeviceB] interface 10ge 1/0/3 [DeviceB-10GE1/0/3] portswitch [DeviceB-10GE1/0/3] port link-type access [DeviceB-10GE1/0/3] port default vlan 3 [DeviceB-10GE1/0/3] quit [DeviceB] interface 10ge 1/0/4 [DeviceB-10GE1/0/4] portswitch [DeviceB-10GE1/0/4] port link-type access [DeviceB-10GE1/0/4] port default vlan 3 [DeviceB-10GE1/0/4] quit步骤2 配置DeviceA与DeviceC、DeviceB与DeviceC之间的链路为干道链路\# 配置DeviceA。
[DeviceA] interface 10ge 1/0/5 [DeviceA-10GE1/0/5] portswitch [DeviceA-10GE1/0/5] port link-type trunk [DeviceA-10GE1/0/5] port trunk allow-pass vlan 2 3 [DeviceA-10GE1/0/5] quit \# 配置DeviceB。
[DeviceB] interface 10ge 1/0/5 [DeviceB-10GE1/0/5] portswitch [DeviceB-10GE1/0/5] port link-type trunk [DeviceB-10GE1/0/5] port trunk allow-pass vlan 2 3 [DeviceB-10GE1/0/5] quit \# 配置DeviceC。

<HUAWEI> system-view [HUAWEI] sysname DeviceC [DeviceC] vlan batch 2 3 [DeviceC] interface 10ge 1/0/1 [DeviceC-10GE1/0/1] portswitch [DeviceC-10GE1/0/1] port link-type trunk [DeviceC-10GE1/0/1] port trunk allow-pass vlan 2 3 [DeviceC-10GE1/0/1] quit [DeviceC] interface 10ge 1/0/2 [DeviceC-10GE1/0/2] portswitch [DeviceC-10GE1/0/2] port link-type trunk [DeviceC-10GE1/0/2] port trunk allow-pass vlan 2 3 [DeviceC-10GE1/0/2] quit
----结束检查配置结果\# 执行命令display vlan可以查看VLAN状态，以DeviceA为例：
[DeviceA] display vlan 2
-------------------------------------------------------------------------------- U: Up; D: Down; TG: Tagged; UT: Untagged; MP: Vlan-mapping; ST: Vlan-stacking; \#: ProtocolTransparent-vlan; *: Management-vlan; MAC-LRN: MAC-address learning; STAT: Statistic; BC: Broadcast; MC: Multicast; UC: Unknown-unicast; FWD: Forward; DSD: Discard;
-------------------------------------------------------------------------------- VID Ports
-------------------------------------------------------------------------------- 2 UT:10GE1/0/1(U) 10GE1/0/2(U)
TG:10GE1/0/5(U)
VID Type Status Property MAC-LRN STAT BC MC UC Description
-------------------------------------------------------------------------------- 2 common enable default enable disable FWD FWD FWD VLAN 0002 \# 执行命令display port vlan，查看10GE1/0/5接口上可以通过的VLAN信息，以DeviceA为例：
[DeviceA] display port vlan 10ge 1/0/5 Port Link Type PVID Trunk VLAN List Port Description
--------------------------------------------------------------------------------------------------------------- 10GE1/0/5 trunk 1 1-3 \# 在DeviceA和DeviceB下，属于相同VLAN2或相同VLAN3内的主机之间能够互相Ping通，并且VLAN2的主机无法Ping通VLAN3内的主机。
配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 2 to 3 \# interface 10GE1/0/1 port link-type access port default vlan 2 \# interface 10GE1/0/2 port link-type access port default vlan 2 \#

interface 10GE1/0/3 port link-type access port default vlan 3 \# interface 10GE1/0/4 port link-type access port default vlan 3 \# interface 10GE1/0/5 port link-type trunk port trunk allow-pass vlan 2 to 3 \# return
● DeviceB \# sysname DeviceB \# vlan batch 2 to 3 \# interface 10GE1/0/1 port link-type access port default vlan 2 \# interface 10GE1/0/2 port link-type access port default vlan 2 \# interface 10GE1/0/3 port link-type access port default vlan 3 \# interface 10GE1/0/4 port link-type access port default vlan 3 \# interface 10GE1/0/5 port link-type trunk port trunk allow-pass vlan 2 to 3 \# return
● DeviceC \# sysname DeviceC \# vlan batch 2 to 3 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 2 to 3 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2 to 3 \# return

#### 4.24.3 举例：配置基于接口划分VLAN（LNP动态协商链路类型），实现同一VLAN的互通（跨设备）

组网需求如图4-25所示，不必手工设置链路类型，设备之间通过Trunk链路类型连接，Device和用户终端之间通过Access链路类型连接，并加入对应VLAN。缺省情况下，全局LNP处于使能状态，所有接口的链路类型自协商功能处于使能状态。希望实现DeviceA和

DeviceB下属于同一VLAN内的主机可以直接通信，属于不同VLAN间的主机不能直接进行二层通信。
图 4-25 配置 LNP 实现以太网接口链路类型自协商组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。
操作步骤步骤1 使能全局链路类型自协商功能。
\#配置DeviceA。DeviceB的配置与DeviceA类似，不再赘述。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 10 20 [DeviceA] undo lnp disable步骤2 配置DeviceA、DeviceB与主机相连的接口为negotiation-desirable类型的接口。
\# 配置 DeviceA 。 DeviceB 的配置与 DeviceA 类似，不再赘述。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type negotiation-desirable [DeviceA-10GE1/0/1] port default vlan 10 [DeviceA-10GE1/0/1] undo port negotiation disable [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] portswitch [DeviceA-10GE1/0/3] port link-type negotiation-desirable [DeviceA-10GE1/0/3] port default vlan 20 [DeviceA-10GE1/0/3] undo port negotiation disable [DeviceA-10GE1/0/3] quit步骤3 配置DeviceA与DeviceC、DeviceB与DeviceC之间的链路为干道链路。
\# 配置DeviceA。DeviceB的配置与DeviceA类似，不再赘述。

[DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type negotiation-desirable [DeviceA-10GE1/0/2] port trunk allow-pass only-vlan 10 20 [DeviceA-10GE1/0/2] undo port negotiation disable [DeviceA-10GE1/0/2] quit \# 配置DeviceC。
<HUAWEI> system-view [HUAWEI] sysname DeviceC [DeviceC] vlan batch 10 20 [DeviceC] undo lnp disable [DeviceC] interface 10ge 1/0/1 [DeviceC-10GE1/0/1] portswitch [DeviceC-10GE1/0/1] port link-type negotiation-desirable [DeviceC-10GE1/0/1] port trunk allow-pass only-vlan 10 20 [DeviceC-10GE1/0/1] undo port negotiation disable [DeviceC-10GE1/0/1] quit [DeviceC] interface 10ge 1/0/2 [DeviceC-10GE1/0/2] portswitch [DeviceC-10GE1/0/2] port link-type negotiation-desirable [DeviceC-10GE1/0/2] port trunk allow-pass only-vlan 10 20 [DeviceC-10GE1/0/2] undo port negotiation disable [DeviceC-10GE1/0/2] quit
----结束检查配置结果\# 在任意视图下执行命令display lnp summary，查看运行LNP协议的二层接口自协商的状态信息。以DeviceC为例：
<DeviceC> display lnp summary Global LNP : Negotiation enable
------------------------------------------------------------------------------------------------------------------- C: Configured; N: Negotiated; *: Negotiation disable; Port link-type(C) link-type(N) InDropped OutDropped FSM
------------------------------------------------------------------------------------------------------------------- 10GE1/0/1 desirable trunk 0 0 trunk 10GE1/0/2 desirable trunk 0 0 trunk \# 在任意视图下执行命令display lnp interface { interface-name | interface-type interface-number }，查看10GE1/0/1接口运行链路类型自协商的状态信息。以DeviceC为例：
<DeviceC> display lnp interface 10ge 1/0/1 LNP information for 10GE1/0/1:
Port link type: trunk Negotiation mode: desirable Hello timer expiration(s): 22 Negotiation timer expiration(s): 0 Trunk timer expiration(s): 292 FSM state: trunk Packets statistics 554 packets received 0 packets dropped bad version: 0, bad TLV(s): 0, bad port link type: 0, bad negotiation state: 0, other: 0 555 packets output 0 packets dropped other: 0 \# 在DeviceA和DeviceB下，属于相同VLAN10或相同VLAN20内的主机之间能够互相Ping通，并且VLAN10的主机无法Ping通VLAN20内的主机。

配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 10 20 \# undo lnp disable \# interface 10GE1/0/1 port link-type negotiation-desirable port default vlan 10 undo port negotiation disable \# interface 10GE1/0/2 port link-type negotiation-desirable port trunk allow-pass only-vlan 10 20 undo port negotiation disable \# interface 10GE1/0/3 port link-type negotiation-desirable port default vlan 20 undo port negotiation disable \# return
● DeviceB \# sysname DeviceB \# vlan batch 10 20 \# undo lnp disable \# interface 10GE1/0/1 port link-type negotiation-desirable port default vlan 10 undo port negotiation disable \# interface 10GE1/0/2 port link-type negotiation-desirable port trunk allow-pass only-vlan 10 20 undo port negotiation disable \# interface 10GE1/0/3 port link-type negotiation-desirable port default vlan 20 undo port negotiation disable \# return
● DeviceC \# sysname DeviceC \# vlan batch 10 20 \# undo lnp disable \# interface 10GE1/0/1 port link-type negotiation-desirable port trunk allow-pass only-vlan 10 20 undo port negotiation disable \# interface 10GE1/0/2 port link-type negotiation-desirable port trunk allow-pass only-vlan 10 20 undo port negotiation disable

#### 4.24.4 举例：配置基于接口划分VLAN，并利用VLANIF接口实现不同网段的互通（跨设备）

\# return举例：配置基于接口划分 VLAN，并利用 接口实现
4.24.4 VLANIF不同网段的互通（跨设备）
组网需求如图4-26所示，DeviceA下的Host1、Host2划分到VLAN2，DeviceB下的Host3、Host4也划分到相同的VLAN2中。DeviceA下的主机与DeviceB下的主机属于不同的网段，且DeviceA与DeviceB之间通过三层网络通信。希望实现DeviceA下的Host1、Host2和DeviceB下的Host3、Host4能够互相通信。
图 4-26 基于接口划分 VLAN 组网图（VLANIF 接口，跨设备）
说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。
操作步骤步骤1 分别在DeviceA、DeviceB上创建VLAN。
\# 配置DeviceA。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 2 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type access [DeviceA-10GE1/0/1] port default vlan 2 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type access [DeviceA-10GE1/0/2] port default vlan 2 [DeviceA-10GE1/0/2] quit \# 配置DeviceB。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan batch 2 [DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] portswitch [DeviceB-10GE1/0/1] port link-type access [DeviceB-10GE1/0/1] port default vlan 2

[DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] portswitch [DeviceB-10GE1/0/2] port link-type access [DeviceB-10GE1/0/2] port default vlan 2 [DeviceB-10GE1/0/2] quit步骤2 配置DeviceA与DeviceB之间的链路为干道链路。
\# 配置DeviceA。
[DeviceA] vlan batch 4 [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] portswitch [DeviceA-10GE1/0/3] port link-type trunk [DeviceA-10GE1/0/3] port trunk allow-pass vlan 4 [DeviceA-10GE1/0/3] quit \# 配置DeviceB。
[DeviceB] vlan batch 4 [DeviceB] interface 10ge 1/0/3 [DeviceB-10GE1/0/3] portswitch [DeviceB-10GE1/0/3] port link-type trunk [DeviceB-10GE1/0/3] port trunk allow-pass vlan 4 [DeviceB-10GE1/0/3] quit步骤3 创建VLANIF接口并配置IP地址。
\# 配置DeviceA。
[DeviceA] interface vlanif 2 [DeviceA-Vlanif2] ip address 10.10.10.1 24 [DeviceA-Vlanif2] quit [DeviceA] interface vlanif 4 [DeviceA-Vlanif4] ip address 10.10.30.1 24 [DeviceA-Vlanif4] quit \# 配置DeviceB。
[DeviceB] interface vlanif 2 [DeviceB-Vlanif2] ip address 10.10.20.1 24 [DeviceB-Vlanif2] quit [DeviceB] interface vlanif 4 [DeviceB-Vlanif4] ip address 10.10.30.2 24 [DeviceB-Vlanif4] quit步骤4 配置OSPF基本功能，保证DeviceA与DeviceB之间跨网络的情况下能够路由可达。
配置DeviceA。
\# [DeviceA] router id 1.1.1.1 [DeviceA] ospf 1 [DeviceA-ospf-1] area 0 [DeviceA-ospf-1-area-0.0.0.0] network 10.10.10.0 0.0.0.255 [DeviceA-ospf-1-area-0.0.0.0] network 10.10.30.0 0.0.0.255 [DeviceA-ospf-1-area-0.0.0.0] quit [DeviceA-ospf-1] quit \# 配置DeviceB。
[DeviceB] router id 2.2.2.2 [DeviceB] ospf 1 [DeviceB-ospf-1] area 0 [DeviceB-ospf-1-area-0.0.0.0] network 10.10.20.0 0.0.0.255 [DeviceB-ospf-1-area-0.0.0.0] network 10.10.30.0 0.0.0.255 [DeviceB-ospf-1-area-0.0.0.0] quit [DeviceB-ospf-1] quit
----结束

检查配置结果在DeviceA的主机上配置缺省网关为VLANIF2接口的IP地址10.10.10.1/24，在DeviceB的主机上配置缺省网关为VLANIF2接口的IP地址10.10.20.1/24。配置完成后，Host1、Host2、Host3、Host4能够相互Ping通。
配置脚本
● DeviceA \# sysname DeviceA \# router id 1.1.1.1 \# vlan batch 2 4 \# interface Vlanif2 ip address 10.10.10.1 255.255.255.0 \# interface Vlanif4 ip address 10.10.30.1 255.255.255.0 \# interface 10GE1/0/1 port link-type access port default vlan 2 \# interface 10GE1/0/2 port link-type access port default vlan 2 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 4 \# ospf 1 area 0.0.0.0 network 10.10.10.0 0.0.0.255 network 10.10.30.0 0.0.0.255 \# return
● DeviceB \# sysname DeviceB \# router id 2.2.2.2 \# vlan batch 2 4 \# interface Vlanif2 ip address 10.10.20.1 255.255.255.0 \# interface Vlanif4 ip address 10.10.30.2 255.255.255.0 \# interface 10GE1/0/1 port link-type access port default vlan 2 \# interface 10GE1/0/2 port link-type access port default vlan 2 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 4 \#

ospf 1 area 0.0.0.0 network 10.10.20.0 0.0.0.255 network 10.10.30.0 0.0.0.255 \# return

#### 4.24.5 举例：配置基于MAC地址划分VLAN

组网需求如图4-27所示，根据主机MAC地址将网络内主机Host1、Host2、Host3划分到VLAN10。主机之间可以互相访问且能访问Internet。如果私自更换其他主机接入网络，则无法访问Internet，且和其他合法主机间也无法互访。
图 4-27 基于 MAC 地址划分 VLAN 组网图说明本例中interface1、interface2、interface3、interface4分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3、10GE1/0/4。
操作步骤步骤1 创建VLAN10，并将用户主机的MAC地址与VLAN进行关联。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan 10 [DeviceA-vlan10] mac-vlan mac-address 00e0-fc00-1111 [DeviceA-vlan10] mac-vlan mac-address 00e0-fc00-2222 [DeviceA-vlan10] mac-vlan mac-address 00e0-fc00-3333 [DeviceA-vlan10] quit步骤2 配置接口加入VLAN10，并在接口10GE1/0/2~10GE1/0/4上使能基于MAC地址划分VLAN。

[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type hybrid [DeviceA-10GE1/0/1] port hybrid tagged vlan 10 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type hybrid [DeviceA-10GE1/0/2] port hybrid untagged vlan 10 [DeviceA-10GE1/0/2] mac-vlan enable [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] portswitch [DeviceA-10GE1/0/3] port link-type hybrid [DeviceA-10GE1/0/3] port hybrid untagged vlan 10 [DeviceA-10GE1/0/3] mac-vlan enable [DeviceA-10GE1/0/3] quit [DeviceA] interface 10ge 1/0/4 [DeviceA-10GE1/0/4] portswitch [DeviceA-10GE1/0/4] port link-type hybrid [DeviceA-10GE1/0/4] port hybrid untagged vlan 10 [DeviceA-10GE1/0/4] mac-vlan enable [DeviceA-10GE1/0/4] quit
----结束检查配置结果\# 执行命令display mac-vlan vlan 10，查看基于MAC地址划分VLAN的信息。
[DeviceA] display mac-vlan vlan 10 Total MAC VLAN address count: 3
--------------------------------------------------- MAC Address Mask VLAN Priority
--------------------------------------------------- 00e0-fc00-1111 ffff-ffff-ffff 10 0 00e0-fc00-2222 ffff-ffff-ffff 10 0 00e0-fc00-3333 ffff-ffff-ffff 10 0 \# 网络内合法主机Host1、Host2、Host3可以互访且均能访问Internet，如果更换成其他主机不能访问。
配置脚本DeviceA \# sysname DeviceA \# vlan batch 10 \# vlan 10 mac-vlan mac-address 00e0-fc00-1111 mac-vlan mac-address 00e0-fc00-2222 mac-vlan mac-address 00e0-fc00-3333 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 10 \# interface 10GE1/0/2 port link-type hybrid port hybrid untagged vlan 10 mac-vlan enable \# interface 10GE1/0/3 port link-type hybrid

port hybrid untagged vlan 10 mac-vlan enable \# interface 10GE1/0/4 port link-type hybrid port hybrid untagged vlan 10 mac-vlan enable \# return

#### 4.24.6 举例：配置基于子网划分VLAN

组网需求如图4-28所示，PC1、PC2、PC3的IP地址网段不相同。希望将不同IP地址网段的PC划分到不同的VLAN，即PC1、PC2、PC3分别划分到VLAN100、VLAN200、VLAN300中。
图 4-28 基于子网划分 VLAN 组网图说明本例中interface1代表10GE1/0/1。
操作步骤步骤1 创建VLAN，并关联IP子网和VLAN。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 100 200 300 [DeviceA] vlan 100 [DeviceA-vlan100] ip-subnet-vlan 1 ip 192.168.1.2 24 priority 2 [DeviceA-vlan100] quit [DeviceA] vlan 200 [DeviceA-vlan200] ip-subnet-vlan 1 ip 192.168.2.2 24 priority 3 [DeviceA-vlan200] quit [DeviceA] vlan 300 [DeviceA-vlan300] ip-subnet-vlan 1 ip 192.168.3.2 24 priority 4 [DeviceA-vlan300] quit

步骤2 配置接口10GE1/0/1为Hybrid类型，接口允许VLAN100、VLAN200、VLAN300通过，并使能基于子网划分VLAN功能。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type hybrid [DeviceA-10GE1/0/1] port hybrid untagged vlan 100 [DeviceA-10GE1/0/1] port hybrid untagged vlan 200 [DeviceA-10GE1/0/1] port hybrid untagged vlan 300 [DeviceA-10GE1/0/1] ip-subnet-vlan enable [DeviceA-10GE1/0/1] quit
----结束检查配置结果\# 在DeviceA上执行命令display ip-subnet-vlan vlan all，查看设备上基于子网划分VLAN的信息。
[DeviceA] display ip-subnet-vlan vlan all IP-subnet-VLAN count: 3 total count: 3
---------------------------------------------------------------- VLAN Index IpAddress SubnetMask Priority
---------------------------------------------------------------- 100 1 192.168.1.2 255.255.255.0 2 200 1 192.168.2.2 255.255.255.0 3 300 1 192.168.3.2 255.255.255.0 4
----------------------------------------------------------------配置脚本DeviceA \# sysname DeviceA \# vlan batch 100 200 300 \# vlan 100 ip-subnet-vlan 1 ip 192.168.1.2 255.255.255.0 priority 2 \# vlan 200 ip-subnet-vlan 1 ip 192.168.2.2 255.255.255.0 priority 3 \# vlan 300 ip-subnet-vlan 1 ip 192.168.3.2 255.255.255.0 priority 4 \# interface 10GE1/0/1 port link-type hybrid port hybrid untagged vlan 100 port hybrid untagged vlan 200 port hybrid untagged vlan 300 ip-subnet-vlan enable \# return

#### 4.24.7 举例：配置基于协议划分VLAN

组网需求如图4-29所示，网络中PC1使用IPv4协议，PC2使用IPv6协议。希望将使用不同协议的PC划分到不同的VLAN，PC1划分到VLAN10，PC2划分到VLAN20。

图 4-29 基于协议划分 VLAN 组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。
操作步骤步骤1 创建VLAN，并将IPv4协议和VLAN10关联，IPv6协议和VLAN20关联。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 10 20 [DeviceA] vlan 10 [DeviceA-vlan10] protocol-vlan ipv4 [DeviceA-vlan10] quit [DeviceA] vlan 20 [DeviceA-vlan20] protocol-vlan ipv6 [DeviceA-vlan20] quit步骤2 配置接口10GE1/0/2关联协议VLAN10，接口10GE1/0/3关联协议VLAN20。
[DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] protocol-vlan vlan 10 all priority 5 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type hybrid [DeviceA-10GE1/0/2] port hybrid untagged vlan 10 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] protocol-vlan vlan 20 all priority 6 [DeviceA-10GE1/0/3] portswitch [DeviceA-10GE1/0/3] port link-type hybrid [DeviceA-10GE1/0/3] port hybrid untagged vlan 20 [DeviceA-10GE1/0/3] quit [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type trunk [DeviceA-10GE1/0/1] port trunk allow-pass vlan 10 20 [DeviceA-10GE1/0/1] quit
----结束

检查配置结果\# 执行命令display protocol-vlan vlan all，查看VLAN上所配置的协议及协议索引。
[DeviceA] display protocol-vlan vlan all
---------------------------------------------------------------- VLAN Protocol Index Protocol Type
---------------------------------------------------------------- 10 0 ipv4 20 0 ipv6 \# 执行命令display protocol-vlan interface all，查看接口关联基于协议划分VLAN的配置信息。
[DeviceA] display protocol-vlan interface all
------------------------------------------------------------------------------- Interface VLAN Index Protocol Type Priority
------------------------------------------------------------------------------- 10GE1/0/2 10 0 ipv4 5 10GE1/0/3 20 0 ipv6 6配置脚本DeviceA \# sysname DeviceA \# vlan batch 10 20 \# vlan 10 protocol-vlan 0 ipv4 \# vlan 20 protocol-vlan 0 ipv6 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 20 \# interface 10GE1/0/2 port link-type hybrid port hybrid untagged vlan 10 protocol-vlan vlan 10 0 priority 5 \# interface 10GE1/0/3 port link-type hybrid port hybrid untagged vlan 20 protocol-vlan vlan 20 0 priority 6 \# return

#### 4.24.8 举例：配置VLANIF接口实现不同VLAN间的互通（同设备）

组网需求如图4-30所示，DeviceA下的主机被划分到不同的VLAN中，分别是VLAN2和VLAN3，且位于不同的网段。希望实现VLAN2和VLAN3之间相互通信。

图 4-30 配置 VLANIF 接口实现不同 VLAN 间的互通组网图（同设备）
说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
操作步骤步骤1 创建VLAN，并配置接口加入VLAN。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 2 3 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type access [DeviceA-10GE1/0/1] port default vlan 2 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type access [DeviceA-10GE1/0/2] port default vlan 3 [DeviceA-10GE1/0/2] quit步骤2 配置VLANIF接口的IP地址。
[DeviceA] interface vlanif 2 [DeviceA-Vlanif2] ip address 10.10.10.2 24 [DeviceA-Vlanif2] quit [DeviceA] interface vlanif 3 [DeviceA-Vlanif3] ip address 10.10.20.2 24 [DeviceA-Vlanif3] quit
---- 结束检查配置结果在VLAN2中的主机上配置IP地址为10.10.10.1/24，缺省网关为接口VLANIF2的IP地址
10.10.10.2/24，在VLAN3中的主机上配置IP地址为10.10.20.1/24，缺省网关为接口VLANIF3的IP地址10.10.20.2/24。配置完成后，VLAN2中的主机与VLAN3中的主机能够相互Ping通。
配置脚本\# sysname DeviceA \# vlan batch 2 to 3

\# interface Vlanif2 ip address 10.10.10.2 255.255.255.0 \# interface Vlanif3 ip address 10.10.20.2 255.255.255.0 \# interface 10GE1/0/1 port link-type access port default vlan 2 \# interface 10GE1/0/2 port link-type access port default vlan 3 \# return

#### 4.24.9 举例：配置VLANIF接口实现不同VLAN间的互通（跨设备）

组网需求如图 4-31 所示， DeviceA 下的 Host1 、 Host2 划分到 VLAN2 ， DeviceB 下的 Host3 、Host4划分到VLAN3中。DeviceA下的主机与DeviceB下的主机属于不同的网段，且DeviceA与DeviceB之间通过三层网络通信。希望实现DeviceA下的Host1、Host2和DeviceB下的Host3、Host4能够互相通信。
图 4-31 配置 VLANIF 接口实现不同 VLAN 间的互通组网图（跨设备）
说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。
操作步骤步骤1 分别在DeviceA、DeviceB上创建VLAN。
\# 配置DeviceA。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 2 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type access [DeviceA-10GE1/0/1] port default vlan 2 [DeviceA-10GE1/0/1] quit

[DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type access [DeviceA-10GE1/0/2] port default vlan 2 [DeviceA-10GE1/0/2] quit \# 配置DeviceB。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan batch 3 [DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] portswitch [DeviceB-10GE1/0/1] port link-type access [DeviceB-10GE1/0/1] port default vlan 3 [DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] portswitch [DeviceB-10GE1/0/2] port link-type access [DeviceB-10GE1/0/2] port default vlan 3 [DeviceB-10GE1/0/2] quit步骤2 配置DeviceA与DeviceB之间的链路为干道链路。
\# 配置DeviceA。
[DeviceA] vlan batch 4 [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] portswitch [DeviceA-10GE1/0/3] port link-type trunk [DeviceA-10GE1/0/3] port trunk allow-pass vlan 4 [DeviceA-10GE1/0/3] quit \# 配置DeviceB。
[DeviceB] vlan batch 4 [DeviceB] interface 10ge 1/0/3 [DeviceB-10GE1/0/3] portswitch [DeviceB-10GE1/0/3] port link-type trunk [DeviceB-10GE1/0/3] port trunk allow-pass vlan 4 [DeviceB-10GE1/0/3] quit步骤3 创建VLANIF接口并配置IP地址。
\# 配置DeviceA。
[DeviceA] interface vlanif 2 [DeviceA-Vlanif2] ip address 10.10.10.1 24 [DeviceA-Vlanif2] quit [DeviceA] interface vlanif 4 [DeviceA-Vlanif4] ip address 10.10.30.1 24 [DeviceA-Vlanif4] quit \# 配置DeviceB。
[DeviceB] interface vlanif 3 [DeviceB-Vlanif2] ip address 10.10.20.1 24 [DeviceB-Vlanif2] quit [DeviceB] interface vlanif 4 [DeviceB-Vlanif4] ip address 10.10.30.2 24 [DeviceB-Vlanif4] quit步骤4 配置OSPF基本功能，保证DeviceA与DeviceB之间跨网络的情况下能够路由可达。
\# 配置DeviceA。
[DeviceA] router id 1.1.1.1 [DeviceA] ospf 1 [DeviceA-ospf-1] area 0 [DeviceA-ospf-1-area-0.0.0.0] network 10.10.10.0 0.0.0.255

[DeviceA-ospf-1-area-0.0.0.0] network 10.10.30.0 0.0.0.255 [DeviceA-ospf-1-area-0.0.0.0] quit [DeviceA-ospf-1] quit \# 配置DeviceB。
[DeviceB] router id 2.2.2.2 [DeviceB] ospf 1 [DeviceB-ospf-1] area 0 [DeviceB-ospf-1-area-0.0.0.0] network 10.10.20.0 0.0.0.255 [DeviceB-ospf-1-area-0.0.0.0] network 10.10.30.0 0.0.0.255 [DeviceB-ospf-1-area-0.0.0.0] quit [DeviceB-ospf-1] quit
----结束检查配置结果在DeviceA的主机上配置缺省网关为VLANIF2接口的IP地址10.10.10.1/24，在DeviceB的主机上配置缺省网关为VLANIF3接口的IP地址10.10.20.1/24。配置完成后，Host1、Host2、Host3、Host4能够相互Ping通。
配置脚本
● DeviceA \# sysname DeviceA \# router id 1.1.1.1 \# vlan batch 2 4 \# interface Vlanif2 ip address 10.10.10.1 255.255.255.0 \# interface Vlanif4 ip address 10.10.30.1 255.255.255.0 \# interface 10GE1/0/1 port link-type access port default vlan 2 \# interface 10GE1/0/2 port link-type access port default vlan 2 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 4 \# ospf 1 area 0.0.0.0 network 10.10.10.0 0.0.0.255 network 10.10.30.0 0.0.0.255 \# return
● DeviceB \# sysname DeviceB \# router id 2.2.2.2 \# vlan batch 3 to 4 \# interface Vlanif3 ip address 10.10.20.1 255.255.255.0

\# interface Vlanif4 ip address 10.10.30.2 255.255.255.0 \# interface 10GE1/0/1 port link-type access port default vlan 3 \# interface 10GE1/0/2 port link-type access port default vlan 3 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 4 \# ospf 1 area 0.0.0.0 network 10.10.20.0 0.0.0.255 network 10.10.30.0 0.0.0.255 \# return

#### 4.24.10 举例：配置三层子接口实现不同VLAN间的互通

组网需求如图4-32所示，VLAN2内的主机和VLAN3内的主机位于不同的网段。希望在DeviceA上配置三层子接口，实现VLAN2与VLAN3之间的主机互通。
说明该配置仅S6780-H、S6750-H、S6750-S、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755-
H、S5755-S、S5732-H-V2系列支持。
图 4-32 通过三层子接口实现不同 VLAN 间的互通组网图说明本例中interface1、interface2、interface3、interface4分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3、10GE1/0/4。

操作步骤步骤1 在DeviceB上创建VLAN。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan batch 2 3 [DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] portswitch [DeviceB-10GE1/0/1] port link-type access [DeviceB-10GE1/0/1] port default vlan 2 [DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] portswitch [DeviceB-10GE1/0/2] port link-type access [DeviceB-10GE1/0/2] port default vlan 3 [DeviceB-10GE1/0/2] quit步骤2 在DeviceB的接口10GE1/0/3上配置允许用户所属的VLAN通过。
[DeviceB] interface 10ge 1/0/3 [DeviceB-10GE1/0/3] portswitch [DeviceB-10GE1/0/3] port link-type trunk [DeviceB-10GE1/0/3] port trunk allow-pass vlan 2 3 [DeviceB-10GE1/0/3] quit步骤3 在DeviceA上创建子接口并关联VLAN。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] interface 10ge 1/0/4 [DeviceA-10GE1/0/4] undo portswitch [DeviceA-10GE1/0/4] quit [DeviceA] interface 10ge 1/0/4.1 [DeviceA-10GE1/0/4.1] dot1q termination vid 2 [DeviceA-10GE1/0/4.1] quit [DeviceA] interface 10ge 1/0/4.2 [DeviceA-10GE1/0/4.2] dot1q termination vid 3 [DeviceA-10GE1/0/4.2] quit步骤4 在DeviceA上配置IP地址。
[DeviceA] interface 10ge 1/0/4.1 [DeviceA-10GE1/0/4.1] ip address 10.10.10.2 24 [DeviceA-10GE1/0/4.1] quit [DeviceA] interface 10ge 1/0/4.2 [DeviceA-10GE1/0/4.2] ip address 10.10.20.2 24 [DeviceA-10GE1/0/4.2] quit
----结束检查配置结果在VLAN2的主机上配置缺省网关为接口10GE1/0/4.1的IP地址10.10.10.2/24，在VLAN3的主机上配置缺省网关为接口10GE1/0/4.2的IP地址10.10.20.2/24。配置完成后，VLAN2和VLAN3之间的主机能够相互Ping通。
配置脚本
● DeviceA \# sysname DeviceA \# interface 10GE1/0/4 undo portswitch \# interface 10GE1/0/4.1 ip address 10.10.10.2 255.255.255.0

encapsulation dot1q-termination dot1q termination vid 2 \# interface 10GE1/0/4.2 ip address 10.10.20.2 255.255.255.0 encapsulation dot1q-termination dot1q termination vid 3 \# return
● DeviceB \# sysname DeviceB \# vlan batch 2 to 3 \# interface 10GE1/0/1 port link-type access port default vlan 2 \# interface 10GE1/0/2 port link-type access port default vlan 3 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 2 to 3 \# return

#### 4.24.11 举例：配置通过流策略实现VLAN间三层隔离

组网需求如图4-33所示，为了通信的安全性，某公司将访客、员工、服务器分别划分到VLAN10、VLAN20、VLAN30中。公司希望：
● 员工、服务器主机、访客均能访问Internet。
● 访客只能访问Internet，不能访问服务器，也不能与其他任何VLAN的用户通信。
● 员工A可以访问服务器区的所有资源，但员工B只能访问服务器A的21端口（FTP服务）。
图 4-33 配置通过流策略实现 VLAN 间三层隔离组网图说明本例中interface1、interface2、interface3、interface4分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3、10GE1/0/4。

配置思路可采用如下思路配置通过流策略实现VLAN间互访控制，如组网中二层隔离三层互通已实现，请重点从第4步开始关注：
1. 配置VLAN并将各接口加入VLAN，使员工、服务器、访客间二层隔离。
2. 配置VLANIF接口及其IP地址，使员工、服务器、访客间可三层互通。
3. 配置上行路由，使员工、服务器、访客均可通过DeviceD访问Internet。
4. 配置高级ACL和基于ACL的流分类：
– 访客只能访问Internet，与企业员工及服务器不能互访。
– 员工A可以访问服务器区的所有资源和Internet。
– 员工B只能访问服务器A的21端口（FTP服务）和Internet。
5. 配置流行为。
6. 配置并应用流策略，使ACL和流行为生效。
操作步骤步骤1 配置VLAN并将各接口加入VLAN，使员工、服务器、访客间二层隔离。
\# 在DeviceA上创建VLAN10，并将接口10GE1/0/1以Untagged方式加入VLAN10，接口10GE1/0/2以Tagged方式加入VLAN10。DeviceB和DeviceC的配置与DeviceA类似，不再赘述。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 10 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type access [DeviceA-10GE1/0/1] port default vlan 10 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch

[DeviceA-10GE1/0/2] port link-type trunk [DeviceA-10GE1/0/2] port trunk allow-pass vlan 10 [DeviceA-10GE1/0/2] quit \# DeviceD上创建VLAN10、VLAN20、VLAN30、VLAN100，并配置接口10GE1/0/1~10GE1/0/4分别以Tagged方式加入VLAN10、VLAN20、VLAN30、VLAN100。
<HUAWEI> system-view [HUAWEI] sysname DeviceD [DeviceD] vlan batch 10 20 30 100 [DeviceD] interface 10ge 1/0/1 [DeviceD-10GE1/0/1] portswitch [DeviceD-10GE1/0/1] port link-type trunk [DeviceD-10GE1/0/1] port trunk allow-pass vlan 10 [DeviceD-10GE1/0/1] quit [DeviceD] interface 10ge 1/0/2 [DeviceD-10GE1/0/2] portswitch [DeviceD-10GE1/0/2] port link-type trunk [DeviceD-10GE1/0/2] port trunk allow-pass vlan 20 [DeviceD-10GE1/0/2] quit [DeviceD] interface 10ge 1/0/3 [DeviceD-10GE1/0/3] portswitch [DeviceD-10GE1/0/3] port link-type trunk [DeviceD-10GE1/0/3] port trunk allow-pass vlan 30 [DeviceD-10GE1/0/3] quit [DeviceD] interface 10ge 1/0/4 [DeviceD-10GE1/0/4] portswitch [DeviceD-10GE1/0/4] port link-type trunk [DeviceD-10GE1/0/4] port trunk allow-pass vlan 100 [DeviceD-10GE1/0/4] quit步骤2 配置VLANIF接口及其IP地址，使员工、服务器、访客间可以三层互通。
\# 在DeviceD上创建VLANIF10、VLANIF20、VLANIF30、VLANIF100，并分别配置其IP地址为10.1.1.1/24、10.1.2.1/24、10.1.3.1/24、10.1.100.1/24。
[DeviceD] interface vlanif 10 [DeviceD-Vlanif10] ip address 10.1.1.1 24 [DeviceD-Vlanif10] quit [DeviceD] interface vlanif 20 [DeviceD-Vlanif20] ip address 10.1.2.1 24 [DeviceD-Vlanif20] quit [DeviceD] interface vlanif 30 [DeviceD-Vlanif30] ip address 10.1.3.1 24 [DeviceD-Vlanif30] quit [DeviceD] interface vlanif 100 [DeviceD-Vlanif100] ip address 10.1.100.1 24 [DeviceD-Vlanif100] quit步骤3 配置上行路由，使员工、服务器、访客均可通过DeviceD访问Internet。
\# 在DeviceD上配置OSPF基本功能，发布用户网段以及DeviceD与Router之间的互联网段。
[DeviceD] ospf [DeviceD-ospf-1] area 0 [DeviceD-ospf-1-area-0.0.0.0] network 10.1.1.0 0.0.0.255 [DeviceD-ospf-1-area-0.0.0.0] network 10.1.2.0 0.0.0.255 [DeviceD-ospf-1-area-0.0.0.0] network 10.1.3.0 0.0.0.255 [DeviceD-ospf-1-area-0.0.0.0] network 10.1.100.0 0.0.0.255 [DeviceD-ospf-1-area-0.0.0.0] quit [DeviceD-ospf-1] quit

说明Router上需要进行如下配置：
● 将连接DeviceD的接口以Tagged方式加入VLAN100，并指定VLANIF100的IP地址与
10.1.100.1在同一网段。
● 配置OSPF基本功能，并发布DeviceD与Router之间的互联网段。
具体配置请参见使用设备的产品文档，本文不再赘述。
步骤4 配置并应用流策略，控制员工、访客、服务器之间的访问。
1. 配置ACL规则。
\# 在DeviceD上配置ACL 3000，禁止访客访问员工区和服务器区。
[DeviceD] acl 3000 [DeviceD-acl4-advance-3000] rule deny ip destination 10.1.2.0 0.0.0.255 [DeviceD-acl4-advance-3000] rule deny ip destination 10.1.3.0 0.0.0.255 [DeviceD-acl4-advance-3000] quit \# 在DeviceD上配置ACL 3001，使员工A可以访问服务器区的所有资源，员工B只能访问服务器A的21端口（FTP服务）。
[DeviceD] acl 3001 [DeviceD-acl4-advance-3001] rule permit ip source 10.1.2.2 0 destination 10.1.3.0 0.0.0.255 [DeviceD-acl4-advance-3001] rule permit tcp destination 10.1.3.2 0 destination-port eq 21 [DeviceD-acl4-advance-3001] rule deny ip destination 10.1.3.0 0.0.0.255 [DeviceD-acl4-advance-3001] quit
2. 配置流分类。
\# 在DeviceD上创建流分类c_custom、c_staff，并分别配置匹配规则3000、3001。
[DeviceD] traffic classifier c_custom [DeviceD-classifier-c_custom] if-match acl 3000 [DeviceD-classifier-c_custom] quit [DeviceD] traffic classifier c_staff [DeviceD-classifier-c_staff] if-match acl 3001 [DeviceD-classifier-c_staff] quit
3. 配置流行为。
\# 在DeviceD上创建流行为b1，并配置允许动作。
[DeviceD] traffic behavior b1 [DeviceD-behavior-b1] permit [DeviceD-behavior-b1] quit
4. 配置流策略，关联流分类和流行为。
\# 在 DeviceD 上创建流策略 p_custom 、 p_staff ，并分别将流分类 c_custom 、c_staff与流行为b1关联。
[DeviceD] traffic policy p_custom [DeviceD-classifier-p_custom] classifier c_custom behavior b1 [DeviceD-classifier-p_custom] quit [DeviceD] traffic policy p_staff [DeviceD-classifier-p_staff] classifier c_staff behavior b1 [DeviceD-classifier-p_staff] quit
5. 应用流策略，实现员工、访客、服务器之间的访问控制。
\# 在DeviceD上，分别在VLAN10、VLAN20的入方向应用流策略p_custom、p_staff 。
[DeviceD] vlan 10 [DeviceD-vlan10] traffic-policy p_custom inbound [DeviceD-vlan10] quit

[DeviceD] vlan 20 [DeviceD-vlan20] traffic-policy p_staff inbound [DeviceD-vlan20] quit
----结束检查配置结果配置访客A的IP地址为10.1.1.2/24，缺省网关为VLANIF10接口的IP地址10.1.1.1；配置员工A的IP地址为10.1.2.2/24，缺省网关为VLANIF20接口的IP地址10.1.2.1；配置员工B的IP地址为10.1.2.3/24，缺省网关为VLANIF20接口的IP地址10.1.2.1；配置服务器A的IP地址为10.1.3.2/24，缺省网关为VLANIF30接口的IP地址10.1.3.1。
配置完成后：
● 访客A不能Ping通员工A、服务器A；员工A和服务器A不能Ping通访客A。
● 员工A可以Ping通服务器A，即可以使用服务器A的FTP服务，也可以使用服务器A的其它服务。
● 员工B Ping不通服务器A，只能使用服务器A的FTP服务。
● 访客、员工A、员工B、服务器A均可以Ping通Router连接DeviceD的接口的IP地址
10.1.100.2/24 ，也就都可以访问 Internet 。
配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 10 \# interface 10GE1/0/1 port link-type access port default vlan 10 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 10 \# return
● DeviceB \# sysname DeviceB \# vlan batch 20 \# interface 10GE1/0/1 port link-type access port default vlan 20 \# interface 10GE1/0/2 port link-type access port default vlan 20 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 20 \# return
● DeviceC \# sysname DeviceC \#

vlan batch 30 \# interface 10GE1/0/1 port link-type access port default vlan 30 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 30 \# return
● DeviceD \# sysname DeviceD \# vlan batch 10 20 30 100 \# acl number 3000 rule 5 deny ip destination 10.1.2.0 0.0.0.255 rule 10 deny ip destination 10.1.3.0 0.0.0.255 acl number 3001 rule 10 permit ip source 10.1.2.2 0 destination 10.1.3.0 0.0.0.255 rule 5 permit tcp destination 10.1.3.2 0 destination-port eq ftp rule 15 deny ip destination 10.1.3.0 0.0.0.255 \# traffic classifier c_custom if-match acl 3000 traffic classifier c_staff if-match acl 3001 \# traffic behavior b1 permit \# traffic policy p_custom classifier c_custom behavior b1 traffic policy p_staff classifier c_staff behavior b1 \# vlan 10 traffic-policy p_custom inbound vlan 20 traffic-policy p_staff inbound \# interface Vlanif10 ip address 10.1.1.1 255.255.255.0 \# interface Vlanif20 ip address 10.1.2.1 255.255.255.0 \# interface Vlanif30 ip address 10.1.3.1 255.255.255.0 \# interface Vlanif100 ip address 10.1.100.1 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 20 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 30 \# interface 10GE1/0/4 port link-type trunk

port trunk allow-pass vlan 100 \# ospf 1 area 0.0.0.0 network 10.1.1.0 0.0.0.255 network 10.1.2.0 0.0.0.255 network 10.1.3.0 0.0.0.255 network 10.1.100.0 0.0.0.255 \# return

#### 4.24.12 举例：配置基于接口划分VLAN，实现不同VLAN内的互通（接入层设备作为网关）

组网需求如图4-34所示，PC1和PC2分别属于VLAN 2和VLAN 3，通过接入层设备DeviceB接入汇聚层设备DeviceA。PC3属于VLAN 4，通过接入层设备DeviceC接入汇聚层设备DeviceA。接入层设备DeviceB作为PC1和PC2的网关，DeviceC作为PC3的网关，通过在设备上配置静态路由，实现用户PC间的互访以及和上层设备的互连。
图 4-34 配置接入层设备作为网关组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。
操作步骤步骤1 配置接入层设备DeviceB。
\# 创建VLAN。

<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan batch 2 3 \# 将接口加入相应VLAN。
[DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] portswitch [DeviceB-10GE1/0/2] port link-type access [DeviceB-10GE1/0/2] port default vlan 2 [DeviceB-10GE1/0/2] quit [DeviceB] interface 10ge 1/0/3 [DeviceB-10GE1/0/3] portswitch [DeviceB-10GE1/0/3] port link-type access [DeviceB-10GE1/0/3] port default vlan 3 [DeviceB-10GE1/0/3] quit \# 配置VLANIF接口，作为用户PC的网关。
[DeviceB] interface vlanif 2 [DeviceB-Vlanif2] ip address 192.168.2.1 24 [DeviceB-Vlanif2] quit [DeviceB] interface vlanif 3 [DeviceB-Vlanif3] ip address 192.168.3.1 24 [DeviceB-Vlanif3] quit \# 配置DeviceB和DeviceA互连。
[DeviceB] vlan batch 5 [DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] portswitch [DeviceB-10GE1/0/1] port link-type access [DeviceB-10GE1/0/1] port default vlan 5 [DeviceB-10GE1/0/1] quit [DeviceB] interface Vlanif 5 [DeviceB-Vlanif5] ip address 192.168.5.2 24 [DeviceB-Vlanif5] quit [DeviceB] ip route-static 0.0.0.0 0.0.0.0 192.168.5.1步骤2 配置接入层设备DeviceC。
\# 创建VLAN。
<HUAWEI> system-view [HUAWEI] sysname DeviceC [DeviceC] vlan batch 4将接口加入相应VLAN。
\# [DeviceC] interface 10ge 1/0/2 [DeviceC-10GE1/0/2] portswitch [DeviceC-10GE1/0/2] port link-type access [DeviceC-10GE1/0/2] port default vlan 4 [DeviceC-10GE1/0/2] quit \# 配置VLANIF接口，作为用户PC的网关。
[DeviceC] interface vlanif 4 [DeviceC-Vlanif4] ip address 192.168.4.1 24 [DeviceC-Vlanif4] quit \# 配置DeviceC和DeviceA互连。
[DeviceC] vlan batch 5 [DeviceC] interface 10ge 1/0/1 [DeviceC-10GE1/0/1] portswitch [DeviceC-10GE1/0/1] port link-type access [DeviceC-10GE1/0/1] port default vlan 5 [DeviceC-10GE1/0/1] quit [DeviceC] interface Vlanif 5

[DeviceC-Vlanif5] ip address 192.168.5.3 24 [DeviceC-Vlanif5] quit [DeviceC] ip route-static 0.0.0.0 0.0.0.0 192.168.5.1步骤3 配置汇聚层设备DeviceA。
\# 创建VLAN。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 5 \# 将接口加入相应VLAN。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type access [DeviceA-10GE1/0/1] port default vlan 5 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type access [DeviceA-10GE1/0/2] port default vlan 5 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] portswitch [DeviceA-10GE1/0/3] port link-type access [DeviceA-10GE1/0/3] port default vlan 5 [DeviceA-10GE1/0/3] quit \# 配置VLANIF接口，实现和上层设备的互连。
[DeviceA] interface vlanif 5 [DeviceA-Vlanif5] ip address 192.168.5.1 24 [DeviceA-Vlanif5] quit \# 配置回程明细路由，实现内网网段之间互访。
[DeviceA] ip route-static 192.168.2.0 255.255.255.0 192.168.5.2 [DeviceA] ip route-static 192.168.3.0 255.255.255.0 192.168.5.2 [DeviceA] ip route-static 192.168.4.0 255.255.255.0 192.168.5.3 \# 配置缺省路由，实现内网网段到上层设备的访问。
[DeviceA] ip route-static 0.0.0.0 0.0.0.0 192.168.5.4
----结束检查配置结果\# 执行命令 display vlan 可以查看 VLAN 状态，以 DeviceB 为例：
[DeviceB] display vlan 2
-------------------------------------------------------------------------------- U: Up; D: Down; TG: Tagged; UT: Untagged; MP: Vlan-mapping; ST: Vlan-stacking; \#: ProtocolTransparent-vlan; *: Management-vlan; MAC-LRN: MAC-address learning; STAT: Statistic; BC: Broadcast; MC: Multicast; UC: Unknown-unicast; FWD: Forward; DSD: Discard;
-------------------------------------------------------------------------------- VID Ports
-------------------------------------------------------------------------------- 2 UT:10GE1/0/2(U)
TG:10GE1/0/1(U)
VID Type Status Property MAC-LRN STAT BC MC UC Description

--------------------------------------------------------------------------------
2 common enable default enable disable FWD FWD FWD VLAN 0002
\# 执行命令display port vlan，查看接口上可以通过的VLAN信息，以DeviceB的接口
10GE1/0/1为例：
[DeviceB] display port vlan 10ge 1/0/1
Port Link Type PVID Trunk VLAN List Port Description
---------------------------------------------------------------------------------------------------------------
10GE1/0/1 access 5 --
配置脚本
● DeviceA
\#
sysname DeviceA
\#
vlan batch 5
\#
interface Vlanif5
ip address 192.168.5.1 255.255.255.0
\#
interface 10GE1/0/1
port link-type access
port default vlan 5
\#
interface 10GE1/0/2
port link-type access
port default vlan 5
\#
interface 10GE1/0/3
port link-type access
port default vlan 5
\#
ip route-static 0.0.0.0 0.0.0.0 192.168.5.4
ip route-static 192.168.2.0 255.255.255.0 192.168.5.2
ip route-static 192.168.3.0 255.255.255.0 192.168.5.2
ip route-static 192.168.4.0 255.255.255.0 192.168.5.3
\#
return
● DeviceB
\#
sysname DeviceB
\#
vlan batch 2 to 3 5
\#
interface Vlanif2
ip address 192.168.2.1 255.255.255.0
\#
interface Vlanif3
ip address 192.168.3.1 255.255.255.0
\#
interface Vlanif5
ip address 192.168.5.2 255.255.255.0
\#
interface 10GE1/0/1
port link-type access
port default vlan 5
\#
interface 10GE1/0/2
port link-type access
port default vlan 2
\#
interface 10GE1/0/3
port link-type access
port default vlan 3
\#

ip route-static 0.0.0.0 0.0.0.0 192.168.5.1 \# return
● DeviceC \# sysname DeviceC \# vlan batch 4 to 5 \# \# interface Vlanif4 ip address 192.168.4.1 255.255.255.0 \# interface Vlanif5 ip address 192.168.5.3 255.255.255.0 \# interface 10GE1/0/1 port link-type access port default vlan 5 \# interface 10GE1/0/2 port link-type access port default vlan 4 \# ip route-static 0.0.0.0 0.0.0.0 192.168.5.1 \# return

#### 4.24.13 举例：配置基于接口划分VLAN，实现不同VLAN内的互通（汇聚层设备作为网关）

组网需求如图4-35所示，PC1和PC2分别属于VLAN 2和VLAN 3，通过接入层设备DeviceB接入汇聚层设备DeviceA。PC3属于VLAN 4，通过接入层设备DeviceC接入汇聚层设备DeviceA。DeviceC不做任何配置，当做HUB即插即用。汇聚层设备DeviceA作为PC1、PC2和PC3的网关，实现用户PC间的互访以及和上层设备的互连。
图 4-35 配置汇聚层设备作为网关组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。

操作步骤步骤1 配置接入层设备DeviceB。
\# 创建VLAN。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan batch 2 3 \# 将接口加入相应VLAN。
[DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] portswitch [DeviceB-10GE1/0/2] port link-type access [DeviceB-10GE1/0/2] port default vlan 2 [DeviceB-10GE1/0/2] quit [DeviceB] interface 10ge 1/0/3 [DeviceB-10GE1/0/3] portswitch [DeviceB-10GE1/0/3] port link-type access [DeviceB-10GE1/0/3] port default vlan 3 [DeviceB-10GE1/0/3] quit [DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] portswitch [DeviceB-10GE1/0/1] port link-type trunk [DeviceB-10GE1/0/1] port trunk allow-pass vlan 2 3 [DeviceB-10GE1/0/1] quit步骤2 配置汇聚层设备DeviceA。
\# 创建VLAN。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 2 to 5 \# 将连接DeviceB、DeviceC的接口加入相应VLAN。
[DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch

[DeviceA-10GE1/0/2] port link-type trunk [DeviceA-10GE1/0/2] port trunk allow-pass vlan 2 3 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] portswitch [DeviceA-10GE1/0/3] port link-type access [DeviceA-10GE1/0/3] port default vlan 4 [DeviceA-10GE1/0/3] quit \# 配置VLANIF接口，作为用户PC的网关。
[DeviceA] interface vlanif 2 [DeviceA-Vlanif2] ip address 192.168.2.1 24 [DeviceA-Vlanif2] quit [DeviceA] interface vlanif 3 [DeviceA-Vlanif3] ip address 192.168.3.1 24 [DeviceA-Vlanif3] quit [DeviceA] interface vlanif 4 [DeviceA-Vlanif4] ip address 192.168.4.1 24 [DeviceA-Vlanif4] quit \# 将连接上层设备的接口加入相应VLAN。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type access [DeviceA-10GE1/0/1] port default vlan 5 [DeviceA-10GE1/0/1] quit \# 配置VLANIF接口，实现内网网段到上层设备的访问。
[DeviceA] interface vlanif 5 [DeviceA-Vlanif5] ip address 192.168.5.1 24 [DeviceA-Vlanif5] quit
----结束检查配置结果\# 执行命令display vlan可以查看VLAN状态，以DeviceB为例：
[DeviceB] display vlan 2
-------------------------------------------------------------------------------- U: Up; D: Down; TG: Tagged; UT: Untagged; MP: Vlan-mapping; ST: Vlan-stacking; \#: ProtocolTransparent-vlan; *: Management-vlan; MAC-LRN: MAC-address learning; STAT: Statistic; BC: Broadcast; MC: Multicast; UC: Unknown-unicast; FWD: Forward; DSD: Discard;
-------------------------------------------------------------------------------- VID Ports
-------------------------------------------------------------------------------- 2 UT:10GE1/0/2(U)
TG:10GE1/0/1(U)
VID Type Status Property MAC-LRN STAT BC MC UC Description
-------------------------------------------------------------------------------- 2 common enable default enable disable FWD FWD FWD VLAN 0002 \# 执行命令display port vlan，查看接口上可以通过的VLAN信息，以DeviceB的接口10GE1/0/1为例：
[DeviceB] display port vlan 10ge 1/0/1 Port Link Type PVID Trunk VLAN List Port Description
--------------------------------------------------------------------------------------------------------------- 10GE1/0/1 trunk 1 2-3

配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 2 to 5 \# interface Vlanif2 ip address 192.168.2.1 255.255.255.0 \# interface Vlanif3 ip address 192.168.3.1 255.255.255.0 \# interface Vlanif4 ip address 192.168.4.1 255.255.255.0 \# interface Vlanif5 ip address 192.168.5.1 255.255.255.0 \# interface 10GE1/0/1 port link-type access port default vlan 5 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2 to 3 \# interface 10GE1/0/3 port link-type access port default vlan 4 \# return
● DeviceB \# sysname DeviceB \# vlan batch 2 to 3 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 2 to 3 \# interface 10GE1/0/2 port link-type access port default vlan 2 \# interface 10GE1/0/3 port link-type access port default vlan 3 \# return

#### 4.24.14 举例：配置管理VLAN实现对本地设备的集中管理

组网需求如图4-36所示，PC与DeviceA在同一个网段，希望通过管理VLAN实现以STelnet方式登录到DeviceA。
图 4-36 配置管理 VLAN 实现对本地设备的集中管理组网图说明本例中interface1代表10GE1/0/1。

操作步骤步骤1 创建管理VLAN。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan 2 [DeviceA-vlan2] management-vlan [DeviceA-vlan2] quit步骤2 配置接口加入到管理VLAN中。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type trunk [DeviceA-10GE1/0/1] port trunk allow-pass vlan 2 [DeviceA-10GE1/0/1] quit步骤3 创建VLANIF接口，并配置VLANIF接口的IP地址。
[DeviceA] interface vlanif 2 [DeviceA-Vlanif2] ip address 10.10.10.2 24 [DeviceA-Vlanif2] quit步骤4 在DeviceA上生成本地密钥对。
[DeviceA] rsa local-key-pair create The key name will be:Host The range of public key size is (2048, 3072).
NOTE: Key pair generation will take a short while.
Please input the modulus [default = 3072]:
步骤5 在DeviceA上配置VTY用户界面。
[DeviceA] user-interface vty 0 4 [DeviceA-ui-vty0-4] authentication-mode aaa [DeviceA-ui-vty0-4] protocol inbound ssh [DeviceA-ui-vty0-4] quit步骤6 创建SSH用户。
[DeviceA] aaa [DeviceA-aaa] local-user client001 password irreversible-cipher Huawei@123 [DeviceA-aaa] local-user client001 privilege level 3 [DeviceA-aaa] local-user client001 service-type ssh [DeviceA-aaa] quit [DeviceA] ssh user client001 [DeviceA] ssh user client001 authentication-type password步骤7 启用STelnet服务功能。
[DeviceA] stelnet server enable [DeviceA] ssh user client001 service-type stelnet说明PC和DeviceA之间通过其他设备相连，中间设备上需要透传管理VLAN2。
----结束

检查配置结果配置完成后，用户PC即可采用password认证方式登录DeviceA。建议采用OpenSSH作为SSH的登录软件，用户PC登录到DeviceA，可以对DeviceA进行集中管理。
配置脚本\# sysname DeviceA \# vlan batch 2 \# vlan 2 management-vlan \# aaa local-user client001 password irreversible-cipher $1b$g/#_YP]w_)$IWm]C@&R&C9bFS<b>6P6'wB $R:#)y6*Hz:Z4(+S=$ local-user client001 privilege level 3 local-user client001 service-type ssh \# interface Vlanif2 ip address 10.10.10.2 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 2 \# stelnet server enable ssh user client001 ssh user client001 authentication-type password ssh user client001 service-type stelnet \# user-interface vty 0 4 authentication-mode aaa protocol inbound ssh \# return

#### 4.24.15 举例：配置VLAN聚合

组网需求如图4-37所示，VLAN2和VLAN3是两个Sub-VLAN，二者接入到VLAN4这个Super- VLAN中，VLAN2和VLAN3的PC需要进行互通。

图 4-37 VLAN 间通过 VLAN 聚合通信组网图配置思路采用如下思路配置VLAN间通过VLAN聚合通信：
1. 在DeviceA和DeviceB上创建VLAN，确定用户所属的VLAN。
在Device上配置VLAN聚合。
2.
a. 配置二层转发功能。
b. 创建Super-VLAN，并把Sub-VLAN加入Super-VLAN。
c. 创建Super-VLAN对应的VLANIF接口，并配置IP地址，作为网关地址。
数据准备为完成此配置例，需准备如下的数据：
● 用户所属的VLAN ID。
● 用户的IP地址。
● DeviceA，DeviceB连接用户的接口编号。
● Sub-VLAN ID、Super-VLAN ID。
● Super-VLAN对应的VLANIF接口编号及IP地址。
操作步骤步骤1 在DeviceA，DeviceB上创建VLAN，并将二层端口加入VLAN。
\# 配置DeviceA。

<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 2 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type access [DeviceA-10GE1/0/1] port default vlan 2 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type access [DeviceA-10GE1/0/2] port default vlan 2 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] portswitch [DeviceA-10GE1/0/3] port link-type trunk [DeviceA-10GE1/0/3] port trunk allow-pass vlan 2 [DeviceA-10GE1/0/3] quit \# 配置DeviceB。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan batch 3 [DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] portswitch [DeviceB-10GE1/0/1] port link-type access [DeviceB-10GE1/0/1] port default vlan 3 [DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] portswitch [DeviceB-10GE1/0/2] port link-type access [DeviceB-10GE1/0/2] port default vlan 3 [DeviceB-10GE1/0/2] quit [DeviceB] interface 10ge 1/0/3 [DeviceB-10GE1/0/3] portswitch [DeviceB-10GE1/0/3] port link-type trunk [DeviceB-10GE1/0/3] port trunk allow-pass vlan 3 [DeviceB-10GE1/0/3] quit步骤2 在Device上配置VLAN聚合。
\# 配置二层转发功能。
<HUAWEI> system-view [HUAWEI] sysname Device [Device] vlan batch 2 to 4 [Device] interface 10ge 1/0/1 [Device-10GE1/0/1] portswitch [Device-10GE1/0/1] port link-type trunk [Device-10GE1/0/1] port trunk allow-pass vlan 2 [Device-10GE1/0/1] quit [Device] interface 10ge 1/0/2 [Device-10GE1/0/2] portswitch [Device-10GE1/0/2] port link-type trunk [Device-10GE1/0/2] port trunk allow-pass vlan 3 [Device-10GE1/0/2] quit \# 创建Super-VLAN，并将Sub-VLAN加入Super-VLAN。
[Device] vlan 4 [Device-vlan4] aggregate-vlan [Device-vlan4] access-vlan 2 to 3 [Device-vlan4] quit \# 创建Super-VLAN对应的VLANIF接口，并配置IP地址。
[Device] interface vlanif 4 [Device-Vlanif4] ip address 10.1.1.12 24

上述配置完成后，为各PC配置IP地址，PC的IP地址和VLANIF接口的IP地址应处于同一网段。配置成功后，各VLAN中的员工与设备之间可以互通，但VLAN2和VLAN3中的PC不能互通。
步骤3 使能VLAN间ARP代理功能。
[Device-vlanif4] arp proxy inter-vlan enable [Device-vlanif4] quit步骤4 检查配置结果。
上述配置完成后，VLAN2中的PC与VLAN3中的PC可以互通。
----结束配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 2 \# interface 10GE1/0/1 port link-type access port default vlan 2 \# interface 10GE1/0/2 port link-type access port default vlan 2 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 2 \# return
● DeviceB \# sysname DeviceB \# vlan batch 3 \# interface 10GE1/0/1 port link-type access port default vlan 3 \# interface 10GE1/0/2 port link-type access port default vlan 3 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 3 \# return
● Device \# sysname Device \# vlan batch 2 to 4 \# vlan 4 aggregate-vlan access-vlan 2 to 3 \# interface Vlanif4 ip address 10.1.1.12 255.255.255.0

arp proxy inter-vlan enable \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 2 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 3 \# return

#### 4.24.16 举例：配置MUX VLAN（同设备）

组网需求如图4-38所示，网络内主机通过DeviceA与Server互访。网络内主机与Server在同一网段。用户希望VLAN3内的主机可以互相访问，VLAN4内的主机不能互访。
图 4-38 配置 MUX VLAN 组网图说明本例中interface1、interface2、interface3、interface4、interface5分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3、10GE1/0/4、10GE1/0/5。
操作步骤步骤1 创建VLAN。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 2 3 4步骤2 配置MUX VLAN，将VLAN2配置成主VLAN，VLAN3配置成互通型从VLAN，VLAN4配置成隔离型从VLAN。
[DeviceA] vlan 2 [DeviceA-vlan2] mux-vlan [DeviceA-vlan2] subordinate group 3 [DeviceA-vlan2] subordinate separate 4 [DeviceA-vlan2] quit步骤3 配置接口加入VLAN，并在接口下使能MUX VLAN功能。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch

[DeviceA-10GE1/0/1] port link-type access [DeviceA-10GE1/0/1] port default vlan 2 [DeviceA-10GE1/0/1] port mux-vlan enable vlan 2 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type access [DeviceA-10GE1/0/2] port default vlan 3 [DeviceA-10GE1/0/2] port mux-vlan enable vlan 3 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] portswitch [DeviceA-10GE1/0/3] port link-type access [DeviceA-10GE1/0/3] port default vlan 3 [DeviceA-10GE1/0/3] port mux-vlan enable vlan 3 [DeviceA-10GE1/0/3] quit [DeviceA] interface 10ge 1/0/4 [DeviceA-10GE1/0/4] portswitch [DeviceA-10GE1/0/4] port link-type access [DeviceA-10GE1/0/4] port default vlan 4 [DeviceA-10GE1/0/4] port mux-vlan enable vlan 4 [DeviceA-10GE1/0/4] quit [DeviceA] interface 10ge 1/0/5 [DeviceA-10GE1/0/5] portswitch [DeviceA-10GE1/0/5] port link-type access [DeviceA-10GE1/0/5] port default vlan 4 [DeviceA-10GE1/0/5] port mux-vlan enable vlan 4 [DeviceA-10GE1/0/5] quit
----结束检查配置结果
● Host1、Host2、Host3、Host4可以和Server互通。
● Host1和Host2可以互相ping通。
● Host3和Host4互相ping不通。
● VLAN3内主机（Host1、Host2）和VLAN4内主机（Host3、Host4）互相ping不通。
配置脚本DeviceA \# sysname DeviceA \# vlan batch 2 to 4 \# vlan 2 mux-vlan subordinate separate 4 subordinate group 3 \# interface 10GE1/0/1 port link-type access port default vlan 2 port mux-vlan enable vlan 2 \# interface 10GE1/0/2 port link-type access port default vlan 3 port mux-vlan enable vlan 3 \# interface 10GE1/0/3 port link-type access

port default vlan 3 port mux-vlan enable vlan 3 \# interface 10GE1/0/4 port link-type access port default vlan 4 port mux-vlan enable vlan 4 \# interface 10GE1/0/5 port link-type access port default vlan 4 port mux-vlan enable vlan 4 \# return

#### 4.24.17 举例：配置MUX VLAN（级联设备）

组网需求如图4-39所示，用户希望网络内主机均可以访问Internet，并且VLAN3内的主机可以互相访问，VLAN4内的主机不能互访。
图 4-39 配置 MUX VLAN 组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。
操作步骤步骤 1 配置 MUX VLAN 。
\# 在DeviceB上创建VLAN 2~VLAN 4，配置VLAN 2为主VLAN，VLAN 3为互通型从VLAN，VLAN4为隔离型从VLAN。

<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan batch 2 3 4 [DeviceB] vlan 2 [DeviceB-vlan2] mux-vlan [DeviceB-vlan2] subordinate group 3 [DeviceB-vlan2] subordinate separate 4 [DeviceB-vlan2] quit \# 在DeviceC上创建VLAN 2~VLAN 4，配置VLAN 2为主VLAN，VLAN 3为互通型从VLAN，VLAN 4为隔离型从VLAN。
<HUAWEI> system-view [HUAWEI] sysname DeviceC [DeviceC] vlan batch 2 3 4 [DeviceC] vlan 2 [DeviceC-vlan2] mux-vlan [DeviceC-vlan2] subordinate group 3 [DeviceC-vlan2] subordinate separate 4 [DeviceC-vlan2] quit \# 在DeviceD上创建VLAN 2~VLAN 4，配置VLAN 2为主VLAN，VLAN 3为互通型从VLAN，VLAN 4为隔离型从VLAN。
<HUAWEI> system-view [HUAWEI] sysname DeviceD [DeviceD] vlan batch 2 3 4 [DeviceD] vlan 2 [DeviceD-vlan2] mux-vlan [DeviceD-vlan2] subordinate group 3 [DeviceD-vlan2] subordinate separate 4 [DeviceD-vlan2] quit \# 配置DeviceB的上行口interface1加入VLAN 2，并使能MUX VLAN功能，配置下行口interface2允许VLAN3通过，并使能MUX VLAN功能，interface3允许VLAN 2～VLAN 4通过。
[DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] portswitch [DeviceB-10GE1/0/1] port link-type trunk [DeviceB-10GE1/0/1] port trunk allow-pass vlan 2 [DeviceB-10GE1/0/1] port mux-vlan enable vlan 2 [DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] portswitch [DeviceB-10GE1/0/2] port link-type trunk [DeviceB-10GE1/0/2] port trunk allow-pass vlan 3 [DeviceB-10GE1/0/2] port mux-vlan enable vlan 3 [DeviceB-10GE1/0/2] quit [DeviceB] interface 10ge 1/0/3 [DeviceB-10GE1/0/3] portswitch [DeviceB-10GE1/0/3] port link-type trunk [DeviceB-10GE1/0/3] port trunk allow-pass vlan 2 to 4 [DeviceB-10GE1/0/3] quit步骤2 配置接入设备。
\# 配置DeviceC的上行口interface1允许VLAN 2~VLAN 4通过，配置下行口interface2和interface3加入VLAN 3并在接口下使能MUX VLAN功能。
[DeviceC] interface 10ge 1/0/1 [DeviceC-10GE1/0/1] portswitch [DeviceC-10GE1/0/1] port link-type trunk [DeviceC-10GE1/0/1] port trunk allow-pass vlan 2 to 4 [DeviceC-10GE1/0/1] quit [DeviceC] interface 10ge 1/0/2 [DeviceC-10GE1/0/2] portswitch [DeviceC-10GE1/0/2] port link-type access [DeviceC-10GE1/0/2] port default vlan 3 [DeviceC-10GE1/0/2] port mux-vlan enable vlan 3

[DeviceC-10GE1/0/2] quit [DeviceC] interface 10ge 1/0/3 [DeviceC-10GE1/0/3] portswitch [DeviceC-10GE1/0/3] port link-type access [DeviceC-10GE1/0/3] port default vlan 3 [DeviceC-10GE1/0/3] port mux-vlan enable vlan 3 [DeviceC-10GE1/0/3] quit \# 配置DeviceD的上行口interface1允许VLAN 2通过并使能MUX VLAN功能，配置下行口interface2和interface3加入VLAN 4并在接口下使能MUX VLAN功能。
[DeviceD] interface 10ge 1/0/1 [DeviceD-10GE1/0/1] portswitch [DeviceD-10GE1/0/1] port link-type trunk [DeviceD-10GE1/0/1] port trunk allow-pass vlan 2 [DeviceD-10GE1/0/1] port mux-vlan enable vlan 2 [DeviceD-10GE1/0/1] quit [DeviceD] interface 10ge 1/0/2 [DeviceD-10GE1/0/2] portswitch [DeviceD-10GE1/0/2] port link-type access [DeviceD-10GE1/0/2] port default vlan 4 [DeviceD-10GE1/0/2] port mux-vlan enable vlan 4 [DeviceD-10GE1/0/2] quit [DeviceD] interface 10ge 1/0/3 [DeviceD-10GE1/0/3] portswitch [DeviceD-10GE1/0/3] port link-type access [DeviceD-10GE1/0/3] port default vlan 4 [DeviceD-10GE1/0/3] port mux-vlan enable vlan 4 [DeviceD-10GE1/0/3] quit步骤3 在DeviceA上创建VLANIF 2，配置IP地址为10.1.1.1 24，并配置接口interface1加入VLAN 2。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 2 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type trunk [DeviceA-10GE1/0/1] port trunk allow-pass vlan 2 [DeviceA-10GE1/0/1] quit [DeviceA] interface vlanif 2 [DeviceA-Vlanif2] ip address 10.1.1.1 24 [DeviceA-Vlanif2] quit说明如果MUX VLAN中有多个Group VLAN，并且Group VLAN之间需要互通，则需要在DeviceA的VLANIF接口下执行arp proxy intra-vlan enable命令配置VLAN内ARP Proxy功能，但该操作也会导致Separate VLAN内设备互通。
步骤4 配置网络内主机的IP地址，使其和DeviceA上VLANIF 2接口的IP地址同网段。
----结束检查配置结果
● Host1、Host2、Host3、Host4可以访问Internet。
● Host1和Host2可以互相ping通。
● Host3和Host4互相ping不通。
● VLAN3内主机（Host1、Host2）ping不通VLAN4内主机（Host3、Host4），VLAN4 内主机（ Host3 、 Host4 ）可以 ping 通 VLAN3 内主机（ Host1 、 Host2 ）。

配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 2 \# interface Vlanif2 ip address 10.10.10.1 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 2 \# return
● DeviceB \# sysname DeviceB \# vlan batch 2 to 4 \# vlan 2 mux-vlan subordinate separate 4 subordinate group 3 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 2 port mux-vlan enable vlan 2 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 3 port mux-vlan enable vlan 3 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 2 to 4 \# return
● DeviceC \# sysname DeviceC \# vlan batch 2 to 4 \# vlan 2 mux-vlan subordinate separate 4 subordinate group 3 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 2 to 4 \# interface 10GE1/0/2 port link-type access port default vlan 3 port mux-vlan enable vlan 3 \# interface 10GE1/0/3 port link-type access port default vlan 3 port mux-vlan enable vlan 3 \# return

● DeviceD
\#
sysname DeviceD
\#
vlan batch 2 to 4
\#
vlan 2
mux-vlan
subordinate separate 4
subordinate group 3
\#
interface 10GE1/0/1
port link-type trunk
port trunk allow-pass vlan 2
port mux-vlan enable vlan 2
\#
interface 10GE1/0/2
port link-type access
port default vlan 4
port mux-vlan enable vlan 4
\#
interface 10GE1/0/3
port link-type access
port default vlan 4
port mux-vlan enable vlan 4
\#
return

#### 4.24.18 举例：配置基于VLAN的VLAN Mapping（1 to 1）

组网需求如图4-40所示，DeviceA下的PC1和PC2划分在VLAN 5，DeviceC下的PC3和PC4划分在VLAN 6。PC1、PC2、PC3、PC4均属于同一网段，希望在DeviceB上通过1 to 1 VLAN Mapping实现不同VLAN间PC的互通。
图 4-40 配置基于 VLAN 的 VLAN Mapping 示例（1 to 1）组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。

操作步骤步骤1 配置DeviceA的接口10GE1/0/1和10GE1/0/2划分到VLAN 5，接口10GE1/0/3允许VLAN 5通过。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 5 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type access [DeviceA-10GE1/0/1] port default vlan 5 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type access [DeviceA-10GE1/0/2] port default vlan 5 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] portswitch [DeviceA-10GE1/0/3] port link-type trunk [DeviceA-10GE1/0/3] port trunk allow-pass vlan 5 [DeviceA-10GE1/0/3] quit步骤2 配置DeviceC的接口10GE1/0/1和10GE1/0/2划分到VLAN 6，接口10GE1/0/3允许VLAN 6通过。
<HUAWEI> system-view [HUAWEI] sysname DeviceC [DeviceC] vlan batch 6 [DeviceC] interface 10ge 1/0/1 [DeviceC-10GE1/0/1] portswitch [DeviceC-10GE1/0/1] port link-type access [DeviceC-10GE1/0/1] port default vlan 6 [DeviceC-10GE1/0/1] quit [DeviceC] interface 10ge 1/0/2 [DeviceC-10GE1/0/2] portswitch [DeviceC-10GE1/0/2] port link-type access [DeviceC-10GE1/0/2] port default vlan 6 [DeviceC-10GE1/0/2] quit [DeviceC] interface 10ge 1/0/3 [DeviceC-10GE1/0/3] portswitch [DeviceC-10GE1/0/3] port link-type trunk [DeviceC-10GE1/0/3] port trunk allow-pass vlan 6 [DeviceC-10GE1/0/3] quit步骤3 在DeviceB的接口10GE1/0/1上配置VLAN Mapping，并配置接口10GE1/0/1和10GE1/0/2允许VLAN 6通过。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan batch 6 [DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] portswitch [DeviceB-10GE1/0/1] port link-type trunk [DeviceB-10GE1/0/1] port trunk allow-pass vlan 6 [DeviceB-10GE1/0/1] port vlan-mapping vlan 5 map-vlan 6 [DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] portswitch [DeviceB-10GE1/0/2] port link-type trunk [DeviceB-10GE1/0/2] port trunk allow-pass vlan 6 [DeviceB-10GE1/0/2] quit
----结束检查配置结果VLAN 5中的PC1或PC2能够与VLAN 6中的PC3或PC4互相ping通。

配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 5 \# interface 10GE1/0/1 port link-type access port default vlan 5 \# interface 10GE1/0/2 port link-type access port default vlan 5 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 5 \# return
● DeviceB \# sysname DeviceB \# vlan batch 6 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 6 port vlan-mapping vlan 5 map-vlan 6 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 6 \# return
● DeviceC \# sysname DeviceC \# vlan batch 6 \# interface 10GE1/0/1 port link-type access port default vlan 6 \# interface 10GE1/0/2 port link-type access port default vlan 6 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 6 \# return

#### 4.24.19 举例：配置基于VLAN的VLAN Mapping（N : 1）

组网需求说明此举例是1 to 1中的N:1 VLAN Mapping。
DeviceA上行接口出去的报文携带VLAN 100~109，上行接口的链路类型可以配置Trunk类型或者Hybrid类型。
如图4-41所示，为了区分不同的家庭用户，需要在DeviceB~DeviceE用不同的VLAN来承载不同用户的相同业务，这样需要用到多个VLAN。因此需要在Device上完成VLAN的汇聚功能（N:1），将由多个VLAN发送的不同用户的相同业务采用同一个VLAN进行发送，节约VLAN资源。
图 4-41 配置 VLAN Mapping 示例（N:1）组网图说明本例中 interface1 代表 10GE1/0/1 。
操作步骤步骤1 配置Device。
\# 创建VLAN。
<HUAWEI> system-view [HUAWEI] sysname Device [Device] vlan batch 10 100 to 109 \# 配置接口加入VLAN。

[Device] interface 10ge 1/0/1 [Device-10GE1/0/1] port link-type hybrid [Device-10GE1/0/1] port hybrid tagged vlan 10 100 to 109步骤2 配置VLAN Mapping功能。
[Device-10GE1/0/1] port vlan-mapping vlan 100 to 109 map-vlan 10
----结束检查配置结果VLAN100～109的用户可以通过Device正常访问网络。
配置脚本Device的配置文件\# sysname Device \# vlan batch 10 100 to 109 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 10 100 to 109 port vlan-mapping vlan 100 to 109 map-vlan 10 \# return

#### 4.24.20 举例：配置基于VLAN的VLAN Mapping（2 to 1）

组网需求如图4-42所示，DeviceA下的PC1属于VLAN 2，PC3属于VLAN 3；DeviceB下的PC2属于VLAN 2，PC4属于VLAN 3。DeviceC和DeviceD上部署了QinQ功能。希望在DeviceE上部署VLAN Mapping，实现不同分支间属于同一VLAN的PC能够互访。
图 4-42 配置基于 VLAN 的 VLAN Mapping 示例（2 to 1）组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。

操作步骤步骤1 在DeviceA上创建VLAN 2和VLAN 3，并配置接口加入VLAN。DeviceB的配置与DeviceA类似，不再赘述。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 2 3 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type access [DeviceA-10GE1/0/1] port default vlan 2 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type access [DeviceA-10GE1/0/2] port default vlan 3 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] portswitch [DeviceA-10GE1/0/3] port link-type trunk [DeviceA-10GE1/0/3] port trunk allow-pass vlan 2 3 [DeviceA-10GE1/0/3] quit步骤 2 在 DeviceC 上配置接口 10GE1/0/1 的类型为 QinQ ， 10GE1/0/1 的外层 Tag 为 VLAN 201。DeviceD的配置与DeviceC类似，不再赘述。
<HUAWEI> system-view [HUAWEI] sysname DeviceC

[DeviceC] vlan batch 201 [DeviceC] interface 10ge 1/0/1 [DeviceC-10GE1/0/1] portswitch [DeviceC-10GE1/0/1] port link-type dot1q-tunnel [DeviceC-10GE1/0/1] port default vlan 201 [DeviceC-10GE1/0/1] quit [DeviceC] interface 10ge 1/0/2 [DeviceC-10GE1/0/2] portswitch [DeviceC-10GE1/0/2] port link-type trunk [DeviceC-10GE1/0/2] port trunk allow-pass vlan 201 [DeviceC-10GE1/0/2] quit步骤3 在DeviceE上配置VLAN Mapping功能：报文带两层VLAN，外层是VLAN 201，内层是VLAN 2时，则将两层VLAN替换成VLAN 501；报文带两层VLAN，外层是VLAN 201，内层是VLAN 3时，则将两层VLAN替换成VLAN 502。
<HUAWEI> system-view [HUAWEI] sysname DeviceE [DeviceE] vlan batch 501 502 [DeviceE] interface 10ge 1/0/1 [DeviceE-10GE1/0/1] portswitch [DeviceE-10GE1/0/1] port link-type trunk [DeviceE-10GE1/0/1] port trunk allow-pass vlan 501 502 [DeviceE-10GE1/0/1] port vlan-mapping vlan 201 inner-vlan 2 map-single-vlan 501 [DeviceE-10GE1/0/1] port vlan-mapping vlan 201 inner-vlan 3 map-single-vlan 502 [DeviceE-10GE1/0/1] quit [DeviceE] interface 10ge 1/0/2 [DeviceE-10GE1/0/2] portswitch [DeviceE-10GE1/0/2] port link-type trunk [DeviceE-10GE1/0/2] port trunk allow-pass vlan 501 502 [DeviceE-10GE1/0/2] port vlan-mapping vlan 201 inner-vlan 2 map-single-vlan 501 [DeviceE-10GE1/0/2] port vlan-mapping vlan 201 inner-vlan 3 map-single-vlan 502 [DeviceE-10GE1/0/2] quit [DeviceE] interface 10ge 1/0/3 [DeviceE-10GE1/0/3] portswitch [DeviceE-10GE1/0/3] port link-type trunk [DeviceE-10GE1/0/3] port trunk allow-pass vlan 501 502 [DeviceE-10GE1/0/3] quit
----结束检查配置结果属于同一VLAN的PC1和PC2之间可以互访，PC3和PC4之间可以互访。属于不同VLAN的PC间无法互访。
配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 2 to 3 \# interface 10GE1/0/1 port link-type access port default vlan 2 \# interface 10GE1/0/2 port link-type access port default vlan 3 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 2 to 3 \# return

● DeviceB
\#
sysname DeviceB
\#
vlan batch 2 to 3
\#
interface 10GE1/0/1
port link-type access
port default vlan 2
\#
interface 10GE1/0/2
port link-type access
port default vlan 3
\#
interface 10GE1/0/3
port link-type trunk
port trunk allow-pass vlan 2 to 3
\#
return
● DeviceC
\#
sysname DeviceC
\#
vlan batch 201
\#
interface 10GE1/0/1
port link-type dot1q-tunnel
port default vlan 201
\#
interface 10GE1/0/2
port link-type trunk
port trunk allow-pass vlan 201
\#
return
● DeviceD
\#
sysname DeviceD
\#
vlan batch 201
\#
interface 10GE1/0/1
port link-type dot1q-tunnel
port default vlan 201
\#
interface 10GE1/0/2
port link-type trunk
port trunk allow-pass vlan 201
\#
return
● DeviceE
\#
sysname DeviceE
\#
vlan batch 501 to 502
\#
interface 10GE1/0/1
port link-type trunk
port trunk allow-pass vlan 501 to 502
port vlan-mapping vlan 201 inner-vlan 2 map-single-vlan 501
port vlan-mapping vlan 201 inner-vlan 3 map-single-vlan 502
\#
interface 10GE1/0/2
port link-type trunk
port trunk allow-pass vlan 501 to 502
port vlan-mapping vlan 201 inner-vlan 2 map-single-vlan 501
port vlan-mapping vlan 201 inner-vlan 3 map-single-vlan 502
\#

interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 501 to 502 \# return

#### 4.24.21 举例：配置基于VLAN的VLAN Mapping（2 to 2）

组网需求如图4-43所示，DeviceA下连接PC1属于VLAN 10，DeviceF下连接PC2属于VLAN 30。
DeviceB和DeviceE上部署了QinQ，DeviceC和DeviceD之间规划的VLAN ID与下层网络不同。希望在DeviceC和DeviceD上部署VLAN Mapping，实现不同分支间属于不同VLAN的PC能够互访。
图 4-43 配置基于 VLAN 的 VLAN Mapping 示例（2 to 2）组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
操作步骤步骤1 在DeviceA和DeviceF上创建VLAN，并配置接口加入VLAN。
\# 配置DeviceA。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 10 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type access [DeviceA-10GE1/0/1] port default vlan 10

[DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type trunk [DeviceA-10GE1/0/2] port trunk allow-pass vlan 10 [DeviceA-10GE1/0/2] quit \# 配置DeviceF。
<HUAWEI> system-view [HUAWEI] sysname DeviceF [DeviceF] vlan batch 30 [DeviceF] interface 10ge 1/0/1 [DeviceF-10GE1/0/1] portswitch [DeviceF-10GE1/0/1] port link-type access [DeviceF-10GE1/0/1] port default vlan 30 [DeviceF-10GE1/0/1] quit [DeviceF] interface 10ge 1/0/2 [DeviceF-10GE1/0/2] portswitch [DeviceF-10GE1/0/2] port link-type trunk [DeviceF-10GE1/0/2] port trunk allow-pass vlan 30 [DeviceF-10GE1/0/2] quit步骤2 在DeviceB和DeviceE上配置QinQ。
\# 在 DeviceB 上配置接口 10GE1/0/1 的类型为 QinQ ， 10GE1/0/1 的外层 Tag 为VLAN20。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan batch 20 [DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] portswitch [DeviceB-10GE1/0/1] port link-type dot1q-tunnel [DeviceB-10GE1/0/1] port default vlan 20 [DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] portswitch [DeviceB-10GE1/0/2] port link-type trunk [DeviceB-10GE1/0/2] port trunk allow-pass vlan 20 [DeviceB-10GE1/0/2] quit \# 在DeviceE上配置接口10GE1/0/1的类型为QinQ，10GE1/0/1的外层Tag为VLAN40。
<HUAWEI> system-view [HUAWEI] sysname DeviceE [DeviceE] vlan batch 40 [DeviceE] interface 10ge 1/0/1 [DeviceE-10GE1/0/1] portswitch [DeviceE-10GE1/0/1] port link-type dot1q-tunnel [DeviceE-10GE1/0/1] port default vlan 40 [DeviceE-10GE1/0/1] quit [DeviceE] interface 10ge 1/0/2 [DeviceE-10GE1/0/2] portswitch [DeviceE-10GE1/0/2] port link-type trunk [DeviceE-10GE1/0/2] port trunk allow-pass vlan 40 [DeviceE-10GE1/0/2] quit步骤3 在DeviceC和DeviceD上配置VLAN Mapping。
在DeviceC上的接口10GE1/0/1上配置VLAN Mapping，报文带两层VLAN，外层是\# VLAN 20，内层是VLAN 10时，则将外层VLAN替换成VLAN 50，内层VLAN替换成VLAN 60。
<HUAWEI> system-view [HUAWEI] sysname DeviceC [DeviceC] vlan batch 50 [DeviceC] interface 10ge 1/0/1

[DeviceC-10GE1/0/1] portswitch [DeviceC-10GE1/0/1] port link-type trunk [DeviceC-10GE1/0/1] port trunk allow-pass vlan 50 [DeviceC-10GE1/0/1] port vlan-mapping vlan 20 inner-vlan 10 map-vlan 50 map-inner-vlan 60 [DeviceC-10GE1/0/1] quit [DeviceC] interface 10ge 1/0/2 [DeviceC-10GE1/0/2] portswitch [DeviceC-10GE1/0/2] port link-type trunk [DeviceC-10GE1/0/2] port trunk allow-pass vlan 50 [DeviceC-10GE1/0/2] quit \# 在DeviceD上的接口10GE1/0/1上配置VLAN Mapping，报文带两层VLAN，外层是VLAN 40，内层是VLAN 30时，则将外层VLAN替换成VLAN 50，内层VLAN替换成VLAN 60。
<HUAWEI> system-view [HUAWEI] sysname DeviceD [DeviceD] vlan batch 50 [DeviceD] interface 10ge 1/0/1 [DeviceD-10GE1/0/1] portswitch [DeviceD-10GE1/0/1] port link-type trunk [DeviceD-10GE1/0/1] port trunk allow-pass vlan 50 [DeviceD-10GE1/0/1] port vlan-mapping vlan 40 inner-vlan 30 map-vlan 50 map-inner-vlan 60 [DeviceD-10GE1/0/1] quit [DeviceD] interface 10ge 1/0/2 [DeviceD-10GE1/0/2] portswitch [DeviceD-10GE1/0/2] port link-type trunk [DeviceD-10GE1/0/2] port trunk allow-pass vlan 50 [DeviceD-10GE1/0/2] quit
----结束检查配置结果配置PC1和PC2的IP地址属于同一网段，PC1和PC2能互相ping通。
配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 10 \# interface 10GE1/0/1 port link-type access port default vlan 10 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 10 \# return
● DeviceB \# sysname DeviceB \# vlan batch 20 \# interface 10GE1/0/1 port link-type dot1q-tunnel port default vlan 20 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 20

\# return
● DeviceC \# sysname DeviceC \# vlan batch 50 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 50 port vlan-mapping vlan 20 inner-vlan 10 map-vlan 50 map-inner-vlan 60 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 50 \# return
● DeviceD \# sysname DeviceD \# vlan batch 50 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 50 port vlan-mapping vlan 40 inner-vlan 30 map-vlan 50 map-inner-vlan 60 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 50 \# return
● DeviceE \# sysname DeviceE \# vlan batch 40 \# interface 10GE1/0/1 port link-type dot1q-tunnel port default vlan 40 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 40 \# return
● DeviceF \# sysname DeviceF \# vlan batch 30 \# interface 10GE1/0/1 port link-type access port default vlan 30 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 30 \# return

#### 4.24.22 举例：配置基于MQC的VLAN Mapping

组网需求如图4-44所示，DeviceA下连接的PC1属于VLAN200，PC2属于VLAN300；DeviceD下连接的PC3属于VLAN200，PC4属于VLAN300。DeviceB与DeviceC之间的网络规划VLAN2给PC1和PC3用，规划VLAN3给PC2和PC4用。希望在DeviceB和DeviceC上配置基于MQC的VLAN Mapping功能，实现PC1能够单向访问PC3，PC2能够单向访问PC4。
图 配置基于 的 组网图4-44 MQC VLAN Mapping说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。
操作步骤步骤1 创建VLAN并将接口加入VLAN。
\# 在DeviceA上创建VLAN200、VLAN300，并将接口10GE1/0/2加入VLAN200，10GE1/0/3 加入 VLAN300 ， 10GE1/0/1 允许 VLAN200 和 VLAN300 的报文通过。
DeviceD的配置与DeviceA相同，不再赘述。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 200 300 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type trunk [DeviceA-10GE1/0/1] port trunk allow-pass vlan 200 300 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type access [DeviceA-10GE1/0/2] port default vlan 200 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] portswitch

[DeviceA-10GE1/0/3] port link-type access [DeviceA-10GE1/0/3] port default vlan 300 [DeviceA-10GE1/0/3] quit \# 在DeviceB上创建VLAN2、VLAN3，即替换后的外层VLAN；并配置接口10GE1/0/1和10GE1/0/2允许VLAN2和VLAN3报文通过。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan batch 2 3 [DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] portswitch [DeviceB-10GE1/0/1] port link-type trunk [DeviceB-10GE1/0/1] port trunk allow-pass vlan 2 3 [DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] portswitch [DeviceB-10GE1/0/2] port link-type trunk [DeviceB-10GE1/0/2] port trunk allow-pass vlan 2 3 [DeviceB-10GE1/0/2] quit \# 在DeviceC上创建VLAN200、VLAN300，即替换后的外层VLAN；并配置接口10GE1/0/1和10GE1/0/2允许VLAN200和VLAN300报文通过。
<HUAWEI> system-view [HUAWEI] sysname DeviceC [DeviceC] vlan batch 200 300 [DeviceC] interface 10ge 1/0/1 [DeviceC-10GE1/0/1] portswitch [DeviceC-10GE1/0/1] port link-type trunk [DeviceC-10GE1/0/1] port trunk allow-pass vlan 200 300 [DeviceC-10GE1/0/1] quit [DeviceC] interface 10ge 1/0/2 [DeviceC-10GE1/0/2] portswitch [DeviceC-10GE1/0/2] port link-type trunk [DeviceC-10GE1/0/2] port trunk allow-pass vlan 200 300 [DeviceC-10GE1/0/2] quit步骤2 配置流分类、流行为、流策略。
\# 在DeviceB上配置流分类、流行为、流策略，将VLAN200映射到VLAN2，VLAN300映射到VLAN3。
[DeviceB] traffic classifier name1 [DeviceB-classifier-name1] if-match vlan 200 [DeviceB-classifier-name1] quit [DeviceB] traffic behavior name1 [DeviceB-behavior-name1] vlan-mapping vlan 2 [DeviceB-behavior-name1] quit [DeviceB] traffic classifier name2 [DeviceB-classifier-name2] if-match vlan 300 [DeviceB-classifier-name2] quit [DeviceB] traffic behavior name2 [DeviceB-behavior-name2] vlan-mapping vlan 3 [DeviceB-behavior-name2] quit [DeviceB] traffic policy name1 [DeviceB-trafficpolicy-name1] classifier name1 behavior name1 [DeviceB-trafficpolicy-name1] classifier name2 behavior name2 [DeviceB-trafficpolicy-name1] quit \# 在DeviceC上配置流分类、流行为、流策略，将VLAN2映射到VLAN200，VLAN3映射到VLAN300。
[DeviceC] traffic classifier name1 [DeviceC-classifier-name1] if-match vlan 2 [DeviceC-classifier-name1] quit [DeviceC] traffic behavior name1 [DeviceC-behavior-name1] vlan-mapping vlan 200 [DeviceC-behavior-name1] quit

[DeviceC] traffic classifier name2 [DeviceC-classifier-name2] if-match vlan 3 [DeviceC-classifier-name2] quit [DeviceC] traffic behavior name2 [DeviceC-behavior-name2] vlan-mapping vlan 300 [DeviceC-behavior-name2] quit [DeviceC] traffic policy name1 [DeviceC-trafficpolicy-name1] classifier name1 behavior name1 [DeviceC-trafficpolicy-name1] classifier name2 behavior name2 [DeviceC-trafficpolicy-name1] quit步骤3 在接口上应用流策略实现VLAN Mapping功能。
\# 在DeviceB的接口10GE1/0/1上应用流策略实现VLAN Mapping功能。
[DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] traffic-policy name1 inbound [DeviceB-10GE1/0/1] quit \# 在DeviceC的接口10GE1/0/2上应用流策略实现VLAN Mapping功能。
[DeviceC] interface 10ge 1/0/2 [DeviceC-10GE1/0/2] traffic-policy name1 inbound [DeviceC-10GE1/0/2] quit
---- 结束检查配置结果配置完成后PC1能够访问PC3；PC2能够访问PC4。
配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 200 300 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 200 300 \# interface 10GE1/0/2 port link-type access port default vlan 200 \# interface 10GE1/0/3 port link-type access port default vlan 300 \# return
● DeviceB \# sysname DeviceB \# vlan batch 2 to 3 \# traffic classifier name1 type or if-match vlan 200 \# traffic classifier name2 type or if-match vlan 300 \# traffic behavior name1 vlan-mapping vlan 2 \#

traffic behavior name2 vlan-mapping vlan 3 \# traffic policy name1 classifier name1 behavior name1 precedence 5 classifier name2 behavior name2 precedence 10 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 2 to 3 traffic-policy name1 inbound \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2 to 3 \# return
● DeviceC \# sysname DeviceC \# vlan batch 200 300 \# traffic classifier name1 type or if-match vlan 2 \# traffic classifier name2 type or if-match vlan 3 \# traffic behavior name1 vlan-mapping vlan 200 \# traffic behavior name2 vlan-mapping vlan 300 \# traffic policy name1 classifier name1 behavior name1 precedence 5 classifier name2 behavior name2 precedence 10 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 200 300 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 200 300 traffic-policy name1 inbound \# return
● DeviceD \# sysname DeviceD \# vlan batch 200 300 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 200 300 \# interface 10GE1/0/2 port link-type access port default vlan 200 \# interface 10GE1/0/3 port link-type access port default vlan 300 \# return

#### 4.24.23 举例：配置Dot1q终结子接口接入VPWS

组网需求如图4-45所示，CE1、CE2分别通过VLAN方式接入PE1和PE2。CE1和CE2之间建立LDP方式的VPWS，使CE1和CE2的用户网络可以互通。
图 4-45 配置 Dot1q 终结子接口接入 VPWS 组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
配置思路采用如下的思路配置：
1. 在骨干网相关设备（PE、P）上配置路由协议实现互通，并使能MPLS。
2. 本例使用缺省隧道策略，建立LSP作为传输业务数据的隧道。
3. PE上使能MPLS L2VPN，并创建VC连接。
4. 在PE连接CE的接口上配置Dot1q子接口接入VPWS。
说明VCMP的角色是Client时，不能配置VLAN终结子接口。
操作步骤步骤1 按图4-45配置CE、PE和P的各接口所属VLAN和VLANIF接口的IP地址。
\# 配置CE1，要求CE1发送给PE1的报文带有一层VLAN Tag。
<HUAWEI> system-view [HUAWEI] sysname CE1 [CE1] vlan batch 10 [CE1] interface 10ge 1/0/1 [CE1-10GE1/0/1] port link-type trunk [CE1-10GE1/0/1] port trunk allow-pass vlan 10 [CE1-10GE1/0/1] quit [CE1] interface vlanif 10 [CE1-Vlanif10] ip address 10.10.10.1 24 [CE1-Vlanif10] quit \# 配置CE2，要求CE2发送给PE2的报文带有一层VLAN Tag。

<HUAWEI> system-view [HUAWEI] sysname CE2 [CE2] vlan batch 10 [CE2] interface 10ge 1/0/1 [CE2-10GE1/0/1] port link-type trunk [CE2-10GE1/0/1] port trunk allow-pass vlan 10 [CE2-10GE1/0/1] quit [CE2] interface vlanif 10 [CE2-Vlanif10] ip address 10.10.10.2 24 [CE2-Vlanif10] quit \# 配置PE1。
<HUAWEI> system-view [HUAWEI] sysname PE1 [PE1] vlan batch 20 [PE1] interface 10ge 1/0/2 [PE1-10GE1/0/2] port link-type hybrid [PE1-10GE1/0/2] port hybrid pvid vlan 20 [PE1-10GE1/0/2] port hybrid tagged vlan 20 [PE1-10GE1/0/2] quit [PE1] interface vlanif 20 [PE1-Vlanif20] ip address 10.1.1.1 24 [PE1-Vlanif20] quit \# 配置P。
<HUAWEI> system-view [HUAWEI] sysname P [P] vlan batch 20 30 [P] interface 10ge 1/0/1 [P-10GE1/0/1] port link-type hybrid [P-10GE1/0/1] port hybrid pvid vlan 30 [P-10GE1/0/1] port hybrid tagged vlan 30 [P-10GE1/0/1] quit [P] interface 10ge 1/0/2 [P-10GE1/0/2] port link-type hybrid [P-10GE1/0/2] port hybrid pvid vlan 20 [P-10GE1/0/2] port hybrid tagged vlan 20 [P-10GE1/0/2] quit [P] interface vlanif 20 [P-Vlanif20] ip address 10.1.1.2 24 [P-Vlanif20] quit [P] interface vlanif 30 [P-Vlanif30] ip address 10.2.2.2 24 [P-Vlanif30] quit \# 配置PE2。
<HUAWEI> system-view [HUAWEI] sysname PE2 [PE2] vlan batch 30 [PE2] interface 10ge 1/0/1 [PE2-10GE1/0/1] port link-type hybrid [PE2-10GE1/0/1] port hybrid pvid vlan 30 [PE2-10GE1/0/1] port hybrid tagged vlan 30 [PE2-10GE1/0/1] quit [PE2] interface vlanif 30 [PE2-Vlanif30] ip address 10.2.2.1 24 [PE2-Vlanif30] quit步骤2 在MPLS骨干网上配置IGP，本示例中使用OSPF。
配置OSPF时，注意需要发布PE1、P和PE2作为LSR ID的32位Loopback接口地址。
\# 配置PE1。
[PE1] router id 1.1.1.1 [PE1] interface loopback 1 [PE1-LoopBack1] ip address 1.1.1.1 32 [PE1-LoopBack1] quit [PE1] ospf 1

[PE1-ospf-1] area 0 [PE1-ospf-1-area-0.0.0.0] network 1.1.1.1 0.0.0.0 [PE1-ospf-1-area-0.0.0.0] network 10.1.1.1 0.0.0.255 [PE1-ospf-1-area-0.0.0.0] quit [PE1-ospf-1] quit \# 配置P。
[P] router id 2.2.2.2 [P] interface loopback 1 [P-LoopBack1] ip address 2.2.2.2 32 [P-LoopBack1] quit [P] ospf 1 [P-ospf-1] area 0 [P-ospf-1-area-0.0.0.0] network 2.2.2.2 0.0.0.0 [P-ospf-1-area-0.0.0.0] network 10.1.1.2 0.0.0.255 [P-ospf-1-area-0.0.0.0] network 10.2.2.2 0.0.0.255 [P-ospf-1-area-0.0.0.0] quit [P-ospf-1] quit \# 配置PE2。
[PE2] router id 3.3.3.3 [PE2] interface loopback 1 [PE2-LoopBack1] ip address 3.3.3.3 32 [PE2-LoopBack1] quit [PE2] ospf 1 [PE2-ospf-1] area 0 [PE2-ospf-1-area-0.0.0.0] network 3.3.3.3 0.0.0.0 [PE2-ospf-1-area-0.0.0.0] network 10.2.2.1 0.0.0.255 [PE2-ospf-1-area-0.0.0.0] quit [PE2-ospf-1] quit \# 配置完成后，PE1、P、PE2之间应能建立OSPF邻居关系，执行display ospf peer命令可以看到邻居状态为Full。执行display ip routing-table命令可以看到PE之间学习到对方的Loopback1接口路由。以PE1的显示为例：
[PE1] display ospf peer (M) Indicates MADJ neighbor OSPF Process 1 with Router ID 1.1.1.1 Area 0.0.0.0 interface 10.1.1.1(Vlanif20)'s neighbors Router ID : 2.2.2.2 Address: 10.1.1.2 State : Full Mode:Nbr is Master Priority: 1 DR : 10.1.1.2 BDR: 10.1.1.1 MTU: 0 Dead timer due (in seconds) : 30 Retrans timer interval : 5 Neighbor up time : 00h06m22s Neighbor up time stamp : 2024-08-03 10:32:05 Authentication Sequence : 0 [PE1] display ip routing-table Route Flags: R - relay, D - download to fib, T - to vpn-instance
------------------------------------------------------------------------------ Routing Tables: Public Destinations : 8 Routes : 8 Destination/Mask Proto Pre Cost Flags NextHop Interface
1.1.1.1/32 Direct 0 0 D 127.0.0.1 LoopBack1
2.2.2.2/32 OSPF 10 1 D 10.1.1.2 Vlanif20
3.3.3.3/32 OSPF 10 2 D 10.1.1.2 Vlanif20
10.1.1.0/24 Direct 0 0 D 10.1.1.1 Vlanif20
10.1.1.1/32 Direct 0 0 D 127.0.0.1 Vlanif20
10.2.2.0/24 OSPF 10 2 D 10.1.1.2 Vlanif20
127.0.0.0/8 Direct 0 0 D 127.0.0.1 InLoopBack0
127.0.0.1/32 Direct 0 0 D 127.0.0.1 InLoopBack0步骤3 在MPLS骨干网上配置MPLS基本能力和LDP

\# 配置PE1。
[PE1] mpls lsr-id 1.1.1.1 [PE1] mpls [PE1-mpls] quit [PE1] mpls ldp [PE1-mpls-ldp] quit [PE1] interface vlanif 20 [PE1-Vlanif20] mpls [PE1-Vlanif20] mpls ldp [PE1-Vlanif20] quit配置P。
\# [P] mpls lsr-id 2.2.2.2 [P] mpls [P-mpls] quit [P] mpls ldp [P-mpls-ldp] quit [P] interface vlanif 20 [P-Vlanif20] mpls [P-Vlanif20] mpls ldp [P-Vlanif20] quit [P] interface vlanif 30 [P-Vlanif30] mpls [P-Vlanif30] mpls ldp [P-Vlanif30] quit \# 配置PE2。
[PE2] mpls lsr-id 3.3.3.3 [PE2] mpls [PE2-mpls] quit [PE2] mpls ldp [PE2-mpls-ldp] quit [PE2] interface vlanif 30 [PE2-Vlanif30] mpls [PE2-Vlanif30] mpls ldp [PE2-Vlanif30] quit步骤4 在PE之间建立远端LDP会话。
\# 配置PE1。
[PE1] mpls ldp remote-peer 3.3.3.3 [PE1-mpls-ldp-remote-3.3.3.3] remote-ip 3.3.3.3 [PE1-mpls-ldp-remote-3.3.3.3] quit \# 配置PE2。
[PE2] mpls ldp remote-peer 1.1.1.1 [PE2-mpls-ldp-remote-1.1.1.1] remote-ip 1.1.1.1 [PE2-mpls-ldp-remote-1.1.1.1] quit上述配置完成后，在PE1或PE2上执行display mpls ldp session命令可以看到PE1和PE2之间的对等体的Status项为“Operational”，即远端对等体关系已建立。
以PE1的显示为例：
[PE1] display mpls ldp session LDP Session(s) in Public Network Codes: LAM(Label Advertisement Mode), SsnAge Unit(DDDD:HH:MM)
A '*' before a session means the session is being deleted.
------------------------------------------------------------------------------ PeerID Status LAM SsnRole SsnAge KASent/Rcv
------------------------------------------------------------------------------
2.2.2.2:0 Operational DU Passive 0000:15:29 3717/3717
3.3.3.3:0 Operational DU Passive 0000:00:00 2/2
------------------------------------------------------------------------------ TOTAL: 2 session(s) Found.

步骤5 在PE上使能MPLS L2VPN，并创建VC连接\# 配置PE1：在接入CE1的接口10GE1/0/1.1上创建VC。
[PE1] mpls l2vpn [PE1-l2vpn] quit [PE1] vcmp role silent [PE1] interface 10ge 1/0/1 [PE1-10GE1/0/1] port link-type hybrid [PE1-10GE1/0/1] quit [PE1] interface 10ge 1/0/1.1 [PE1-10GE1/0/1.1] dot1q termination vid 10 [PE1-10GE1/0/1.1] mpls l2vc 3.3.3.3 101 [PE1-10GE1/0/1.1] quit \# 配置PE2：在接入CE2的接口10GE1/0/2.1上创建VC。
[PE2] mpls l2vpn [PE2-l2vpn] quit [PE2] vcmp role silent [PE2] interface 10ge 1/0/2 [PE2-10GE1/0/2] port link-type hybrid [PE2-10GE1/0/2] quit [PE2] interface 10ge 1/0/2.1 [PE2-10GE1/0/2.1] dot1q termination vid 10 [PE2-10GE1/0/2.1] mpls l2vc 1.1.1.1 101 [PE2-10GE1/0/2.1] quit
----结束检查配置结果在PE上查看L2VPN连接信息，可以看到建立了一条L2 VC，状态为UP。
以PE1的显示为例：
[PE1] display mpls l2vc interface 10ge 1/0/1.1
*client interface : 10GE1/0/1.1 is up Administrator PW : no session state : up AC status : up VC state : up Label state : 0 Token state : 0 VC ID : 101 VC type : VLAN destination : 3.3.3.3 local group ID : 0 remote group ID : 0 local VC label : 1038 remote VC label : 1038 local AC OAM State : up local PSN OAM State : up local forwarding state : forwarding local status code : 0x0 (forwarding)
remote AC OAM state : up remote PSN OAM state : up remote forwarding state: forwarding remote status code : 0x0 (forwarding)
remote interface : 10GE1/0/2.1 ignore standby state : no BFD for PW : unavailable VCCV State : up manual fault : not set active state : active forwarding entry : exist TTL Value : 1 link state : up local VC MTU : 1500 remote VC MTU : 1500 local VCCV : alert ttl lsp-ping bfd remote VCCV : alert ttl lsp-ping bfd

local control word : disable remote control word : disable tunnel policy name : -- PW template name : -- primary or secondary : primary load balance type : flow Access-port : false Switchover Flag : false VC tunnel info : 1 tunnels NO.0 TNL type : ldp , TNL ID : 0x0000000001004ccb43 create time : 0 days, 0 hours, 4 minutes, 42 seconds up time : 0 days, 0 hours, 3 minutes, 6 seconds last change time : 0 days, 0 hours, 3 minutes, 6 seconds VC last up time : 2024/08/03 14:33:29 VC total up time : 0 days, 0 hours, 3 minutes, 6 seconds CKey : 385 NKey : 16777471 PW redundancy mode : frr AdminPw interface : -- AdminPw link state : -- Forward state : send active, receive active Diffserv Mode : uniform Service Class : cs- Color : -- DomainId : - Domain Name : - CE1和CE2能够相互Ping通。
以CE1的显示为例：
[CE1] ping 10.10.10.2 PING 10.10.10.2: 56 data bytes, press CTRL_C to break Reply from 10.10.10.2: bytes=56 Sequence=1 ttl=255 time=31 ms Reply from 10.10.10.2: bytes=56 Sequence=2 ttl=255 time=10 ms Reply from 10.10.10.2: bytes=56 Sequence=3 ttl=255 time=5 ms Reply from 10.10.10.2: bytes=56 Sequence=4 ttl=255 time=2 ms Reply from 10.10.10.2: bytes=56 Sequence=5 ttl=255 time=28 ms
--- 10.10.10.2 ping statistics --- 5 packet(s) transmitted 5 packet(s) received
0.00% packet loss round-trip min/avg/max = 2/15/31 ms配置脚本
● CE1 \# sysname CE1 \# vlan batch 10 \# interface Vlanif10 ip address 10.10.10.1 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# return
● CE2 \# sysname CE2 \# vlan batch 10 \# interface Vlanif10 ip address 10.10.10.2 255.255.255.0 \#

interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# return
● PE1 \# sysname PE1 \# router id 1.1.1.1 \# vcmp role silent \# vlan batch 20 \# mpls lsr-id 1.1.1.1 mpls \# mpls l2vpn \# mpls ldp \# mpls ldp remote-peer 3.3.3.3 remote-ip 3.3.3.3 \# interface Vlanif20 ip address 10.1.1.1 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid \# interface 10GE1/0/1.1 encapsulation dot1q-termination dot1q termination vid 10 mpls l2vc 3.3.3.3 101 \# interface 10GE1/0/2 port link-type hybrid port hybrid pvid vlan 20 port hybrid tagged vlan 20 \# interface LoopBack1 ip address 1.1.1.1 255.255.255.255 \# ospf 1 area 0.0.0.0 network 1.1.1.1 0.0.0.0 network 10.1.1.0 0.0.0.255 \# return
● P \# sysname P \# router id 2.2.2.2 \# vlan batch 20 30 \# mpls lsr-id 2.2.2.2 mpls \# mpls ldp \# interface Vlanif20 ip address 10.1.1.2 255.255.255.0 mpls

mpls ldp \# interface Vlanif30 ip address 10.2.2.2 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 30 port hybrid tagged vlan 30 \# interface 10GE1/0/2 port link-type hybrid port hybrid pvid vlan 20 port hybrid tagged vlan 20 \# interface LoopBack1 ip address 2.2.2.2 255.255.255.255 \# ospf 1 area 0.0.0.0 network 2.2.2.2 0.0.0.0 network 10.1.1.0 0.0.0.255 network 10.2.2.0 0.0.0.255 \# return
● PE2 \# sysname PE2 \# router id 3.3.3.3 \# vcmp role silent \# vlan batch 30 \# mpls lsr-id 3.3.3.3 mpls \# mpls l2vpn \# mpls ldp \# mpls ldp remote-peer 1.1.1.1 remote-ip 1.1.1.1 \# interface Vlanif30 ip address 10.2.2.1 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 30 port hybrid tagged vlan 30 \# interface 10GE1/0/2 port link-type hybrid \# interface 10GE1/0/2.1 encapsulation dot1q-termination dot1q termination vid 10 mpls l2vc 1.1.1.1 101 \# interface LoopBack1 ip address 3.3.3.3 255.255.255.255 \# ospf 1

area 0.0.0.0 network 3.3.3.3 0.0.0.0 network 10.2.2.0 0.0.0.255 \# return

#### 4.24.24 举例：配置QinQ终结子接口接入VPWS

组网需求如图4-46所示，CE1、CE2分别通过VLAN方式接入PE1和PE2。CE1和CE2之间建立LDP方式的VPWS。DeviceA分别与CE1、PE1相连。DeviceB分别与CE2、PE2相连。Device的CE侧接口配置灵活QinQ，对CE发送过来的报文打上允许通过的外层VLAN Tag。
当Device连接多个CE时，对不同CE发送过来的不同的VLAN Tag报文打上相同的外层VLAN Tag，还可以达到节省公网VLAN数量的目的。
图 4-46 配置 QinQ 终结子接口接入 VPWS 组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
配置思路采用如下的思路配置：
1. 在骨干网相关设备（PE、P）上配置路由协议实现互通，并使能MPLS。
2. 本例使用缺省隧道策略，建立LSP作为传输业务数据的隧道。
3. PE上使能MPLS L2VPN，并创建VC连接。
4. 在PE连接Device的接口上配置QinQ子接口接入VPWS。
5. 在Device连接CE的接口上配置灵活QinQ。
说明VCMP的角色是Client时，不能配置VLAN终结子接口。

操作步骤步骤1 按图4-46配置CE、PE和P的各接口所属VLAN和VLANIF接口的IP地址\# 配置CE1，要求CE1发送给PE1的报文带有一层VLAN Tag。
<HUAWEI> system-view [HUAWEI] sysname CE1 [CE1] vlan batch 10 [CE1] interface 10ge 1/0/1 [CE1-10GE1/0/1] port link-type trunk [CE1-10GE1/0/1] port trunk allow-pass vlan 10 [CE1-10GE1/0/1] quit [CE1] interface vlanif 10 [CE1-Vlanif10] ip address 10.10.10.1 24 [CE1-Vlanif10] quit \# 配置CE2，要求CE2发送给PE2的报文带有一层VLAN Tag。
<HUAWEI> system-view [HUAWEI] sysname CE2 [CE2] vlan batch 10 [CE2] interface 10ge 1/0/1 [CE2-10GE1/0/1] port link-type trunk [CE2-10GE1/0/1] port trunk allow-pass vlan 10 [CE2-10GE1/0/1] quit [CE2] interface vlanif 10 [CE2-Vlanif10] ip address 10.10.10.2 24 [CE2-Vlanif10] quit \# 配置PE1。
<HUAWEI> system-view [HUAWEI] sysname PE1 [PE1] vlan batch 20 [PE1] interface 10ge 1/0/2 [PE1-10GE1/0/2] port link-type hybrid [PE1-10GE1/0/2] port hybrid pvid vlan 20 [PE1-10GE1/0/2] port hybrid tagged vlan 20 [PE1-10GE1/0/2] quit [PE1] interface vlanif 20 [PE1-Vlanif20] ip address 10.1.1.1 24 [PE1-Vlanif20] quit \# 配置P。
<HUAWEI> system-view [HUAWEI] sysname P [P] vlan batch 20 30 [P] interface 10ge 1/0/1 [P-10GE1/0/1] port link-type hybrid [P-10GE1/0/1] port hybrid pvid vlan 30 [P-10GE1/0/1] port hybrid tagged vlan 30 [P-10GE1/0/1] quit [P] interface 10ge 1/0/2 [P-10GE1/0/2] port link-type hybrid [P-10GE1/0/2] port hybrid pvid vlan 20 [P-10GE1/0/2] port hybrid tagged vlan 20 [P-10GE1/0/2] quit [P] interface vlanif 20 [P-Vlanif20] ip address 10.1.1.2 24 [P-Vlanif20] quit [P] interface vlanif 30 [P-Vlanif30] ip address 10.2.2.2 24 [P-Vlanif30] quit \# 配置PE2。
<HUAWEI> system-view [HUAWEI] sysname PE2 [PE2] vlan batch 30 [PE2] interface 10ge 1/0/1 [PE2-10GE1/0/1] port link-type hybrid

[PE2-10GE1/0/1] port hybrid pvid vlan 30 [PE2-10GE1/0/1] port hybrid tagged vlan 30 [PE2-10GE1/0/1] quit [PE2] interface vlanif 30 [PE2-Vlanif30] ip address 10.2.2.1 24 [PE2-Vlanif30] quit步骤2 在Device的接口上配置灵活QinQ和允许通过的VLAN。
\# 配置DeviceA。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan 100 [DeviceA-vlan100] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] port link-type hybrid [DeviceA-10GE1/0/2] port hybrid tagged vlan 100 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] port link-type hybrid [DeviceA-10GE1/0/1] port hybrid untagged vlan 100 [DeviceA-10GE1/0/1] port vlan-stacking vlan 10 stack-vlan 100 [DeviceA-10GE1/0/1] quit \# 配置 DeviceB 。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan 100 [DeviceB-vlan100] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] port link-type hybrid [DeviceB-10GE1/0/2] port hybrid tagged vlan 100 [DeviceB-10GE1/0/2] quit [DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] port link-type hybrid [DeviceB-10GE1/0/1] port hybrid untagged vlan 100 [DeviceB-10GE1/0/1] port vlan-stacking vlan 10 stack-vlan 100 [DeviceB-10GE1/0/1] quit步骤3 在MPLS骨干网上配置IGP，本示例中使用OSPF。
配置OSPF时，注意需要发布PE1、P和PE2作为LSR ID的32位Loopback接口地址。
配置PE1。
\# [PE1] router id 1.1.1.1 [PE1] interface loopback 1 [PE1-LoopBack1] ip address 1.1.1.1 32 [PE1-LoopBack1] quit [PE1] ospf 1 [PE1-ospf-1] area 0 [PE1-ospf-1-area-0.0.0.0] network 1.1.1.1 0.0.0.0 [PE1-ospf-1-area-0.0.0.0] network 10.1.1.1 0.0.0.255 [PE1-ospf-1-area-0.0.0.0] quit [PE1-ospf-1] quit \# 配置P。
[P] router id 2.2.2.2 [P] interface loopback 1 [P-LoopBack1] ip address 2.2.2.2 32 [P-LoopBack1] quit [P] ospf 1 [P-ospf-1] area 0 [P-ospf-1-area-0.0.0.0] network 2.2.2.2 0.0.0.0 [P-ospf-1-area-0.0.0.0] network 10.1.1.2 0.0.0.255 [P-ospf-1-area-0.0.0.0] network 10.2.2.2 0.0.0.255 [P-ospf-1-area-0.0.0.0] quit [P-ospf-1] quit

\# 配置PE2。
[PE2] router id 3.3.3.3 [PE2] interface loopback 1 [PE2-LoopBack1] ip address 3.3.3.3 32 [PE2-LoopBack1] quit [PE2] ospf 1 [PE2-ospf-1] area 0 [PE2-ospf-1-area-0.0.0.0] network 3.3.3.3 0.0.0.0 [PE2-ospf-1-area-0.0.0.0] network 10.2.2.1 0.0.0.255 [PE2-ospf-1-area-0.0.0.0] quit [PE2-ospf-1] quit \# 配置完成后，PE1、P、PE2之间应能建立OSPF邻居关系，执行display ospf peer命令可以看到邻居状态为Full。执行display ip routing-table命令可以看到PE之间学习到对方的Loopback1接口路由。以PE1的显示为例：
[PE1] display ospf peer (M) Indicates MADJ neighbor OSPF Process 1 with Router ID 1.1.1.1 Area 0.0.0.0 interface 10.1.1.1(Vlanif20)'s neighbors Router ID : 2.2.2.2 Address: 10.1.1.2 State : Full Mode:Nbr is Master Priority: 1 DR : 10.1.1.2 BDR: 10.1.1.1 MTU: 0 Dead timer due (in seconds) : 30 Retrans timer interval : 5 Neighbor up time : 00h06m22s Neighbor up time stamp : 2024-08-03 10:32:05 Authentication Sequence : 0 [PE1] display ip routing-table Route Flags: R - relay, D - download to fib, T - to vpn-instance
------------------------------------------------------------------------------ Routing Tables: Public Destinations : 8 Routes : 8 Destination/Mask Proto Pre Cost Flags NextHop Interface
1.1.1.1/32 Direct 0 0 D 127.0.0.1 LoopBack1
2.2.2.2/32 OSPF 10 1 D 10.1.1.2 Vlanif20
3.3.3.3/32 OSPF 10 2 D 10.1.1.2 Vlanif20
10.1.1.0/24 Direct 0 0 D 10.1.1.1 Vlanif20
10.1.1.1/32 Direct 0 0 D 127.0.0.1 Vlanif20
10.2.2.0/24 OSPF 10 2 D 10.1.1.2 Vlanif20
127.0.0.0/8 Direct 0 0 D 127.0.0.1 InLoopBack0
127.0.0.1/32 Direct 0 0 D 127.0.0.1 InLoopBack0步骤4 在MPLS骨干网上配置MPLS基本能力和LDP。
\# 配置PE1。
[PE1] mpls lsr-id 1.1.1.1 [PE1] mpls [PE1-mpls] quit [PE1] mpls ldp [PE1-mpls-ldp] quit [PE1] interface vlanif 20 [PE1-Vlanif20] mpls [PE1-Vlanif20] mpls ldp [PE1-Vlanif20] quit配置P。
\# [P] mpls lsr-id 2.2.2.2 [P] mpls [P-mpls] quit [P] mpls ldp [P-mpls-ldp] quit

[P] interface vlanif 20 [P-Vlanif20] mpls [P-Vlanif20] mpls ldp [P-Vlanif20] quit [P] interface vlanif 30 [P-Vlanif30] mpls [P-Vlanif30] mpls ldp [P-Vlanif30] quit \# 配置PE2。
[PE2] mpls lsr-id 3.3.3.3 [PE2] mpls [PE2-mpls] quit [PE2] mpls ldp [PE2-mpls-ldp] quit [PE2] interface vlanif 30 [PE2-Vlanif30] mpls [PE2-Vlanif30] mpls ldp [PE2-Vlanif30] quit步骤5 在PE之间建立远端LDP会话。
\# 配置PE1。
[PE1] mpls ldp remote-peer 3.3.3.3 [PE1-mpls-ldp-remote-3.3.3.3] remote-ip 3.3.3.3 [PE1-mpls-ldp-remote-3.3.3.3] quit \# 配置PE2。
[PE2] mpls ldp remote-peer 1.1.1.1 [PE2-mpls-ldp-remote-1.1.1.1] remote-ip 1.1.1.1 [PE2-mpls-ldp-remote-1.1.1.1] quit上述配置完成后，在PE1或PE2上执行display mpls ldp session命令可以看到PE1和PE2之间的对等体的Status项为“Operational”，即远端对等体关系已建立。
以PE1的显示为例：
[PE1] display mpls ldp session LDP Session(s) in Public Network Codes: LAM(Label Advertisement Mode), SsnAge Unit(DDDD:HH:MM)
A '*' before a session means the session is being deleted.
------------------------------------------------------------------------------ PeerID Status LAM SsnRole SsnAge KASent/Rcv
------------------------------------------------------------------------------
2.2.2.2:0 Operational DU Passive 0000:15:29 3717/3717
3.3.3.3:0 Operational DU Passive 0000:00:00 2/2
------------------------------------------------------------------------------ TOTAL: 2 session(s) Found.
步骤6 在PE上使能MPLS L2VPN，并创建VC连接。
\# 配置PE1：在接入CE1的接口10GE1/0/1.1上创建VC。
[PE1] mpls l2vpn [PE1-l2vpn] quit [PE1] vcmp role silent [PE1] interface 10ge 1/0/1 [PE1-10GE1/0/1] port link-type hybrid [PE1-10GE1/0/1] quit [PE1] interface 10ge 1/0/1.1 [PE1-10GE1/0/1.1] qinq termination pe-vid 100 ce-vid 10 [PE1-10GE1/0/1.1] mpls l2vc 3.3.3.3 101 [PE1-10GE1/0/1.1] quit \# 配置PE2：在接入CE2的接口10GE1/0/2.1上创建VC。

[PE2] mpls l2vpn [PE2-l2vpn] quit [PE2] vcmp role silent [PE2] interface 10ge 1/0/2 [PE2-10GE1/0/2] port link-type hybrid [PE2-10GE1/0/2] quit [PE2] interface 10ge 1/0/2.1 [PE2-10GE1/0/2.1] qinq termination pe-vid 100 ce-vid 10 [PE2-10GE1/0/2.1] mpls l2vc 1.1.1.1 101 [PE2-10GE1/0/2.1] quit
----结束检查配置结果在PE上查看L2VPN连接信息，可以看到建立了一条L2 VC，状态为UP。
以PE1的显示为例：
[PE1] display mpls l2vc interface 10ge 1/0/1.1
*client interface : 10GE1/0/1.1 is up Administrator PW : no session state : up AC status : up VC state : up Label state : 0 Token state : 0 VC ID : 101 VC type : VLAN destination : 3.3.3.3 local group ID : 0 remote group ID : 0 local VC label : 1038 remote VC label : 1038 local AC OAM State : up local PSN OAM State : up local forwarding state : forwarding local status code : 0x0 (forwarding)
remote AC OAM state : up remote PSN OAM state : up remote forwarding state: forwarding remote status code : 0x0 (forwarding)
remote interface : 10GE1/0/2.1 ignore standby state : no BFD for PW : unavailable VCCV State : up manual fault : not set active state : active forwarding entry : exist TTL Value : 1 link state : up local VC MTU : 1500 remote VC MTU : 1500 local VCCV : alert ttl lsp-ping bfd remote VCCV : alert ttl lsp-ping bfd local control word : disable remote control word : disable tunnel policy name : -- PW template name : -- primary or secondary : primary load balance type : flow Access-port : false Switchover Flag : false VC tunnel info : 1 tunnels NO.0 TNL type : ldp , TNL ID : 0x0000000001004ccb43 create time : 0 days, 0 hours, 4 minutes, 42 seconds up time : 0 days, 0 hours, 3 minutes, 6 seconds last change time : 0 days, 0 hours, 3 minutes, 6 seconds VC last up time : 2024/08/03 14:33:29 VC total up time : 0 days, 0 hours, 3 minutes, 6 seconds CKey : 385 NKey : 16777471 PW redundancy mode : frr

AdminPw interface : -- AdminPw link state : -- Forward state : send active, receive active Diffserv Mode : uniform Service Class : cs- Color : -- DomainId : - Domain Name : - CE1和CE2能够相互Ping通。
以CE1的显示为例：
[CE1] ping 10.10.10.2 PING 10.10.10.2: 56 data bytes, press CTRL_C to break Reply from 10.10.10.2: bytes=56 Sequence=1 ttl=255 time=31 ms Reply from 10.10.10.2: bytes=56 Sequence=2 ttl=255 time=10 ms Reply from 10.10.10.2: bytes=56 Sequence=3 ttl=255 time=5 ms Reply from 10.10.10.2: bytes=56 Sequence=4 ttl=255 time=2 ms Reply from 10.10.10.2: bytes=56 Sequence=5 ttl=255 time=28 ms
--- 10.10.10.2 ping statistics --- 5 packet(s) transmitted 5 packet(s) received
0.00% packet loss round-trip min/avg/max = 2/15/31 ms配置脚本
● CE1 \# sysname CE1 \# vlan batch 10 \# interface Vlanif10 ip address 10.10.10.1 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# return
● CE2 \# sysname CE2 \# vlan batch 10 \# interface Vlanif10 ip address 10.10.10.2 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# return
● DeviceA \# sysname DeviceA \# vlan batch 100 \# interface 10GE1/0/1 port link-type hybrid port hybrid untagged vlan 100 port vlan-stacking vlan 10 stack-vlan 100 \#

interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 100 \# return
● DeviceB \# sysname DeviceB \# vlan batch 100 \# interface 10GE1/0/1 port link-type hybrid port hybrid untagged vlan 100 port vlan-stacking vlan 10 stack-vlan 100 \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 100 \# return
● PE1 \# sysname PE1 \# router id 1.1.1.1 \# vcmp role silent \# vlan batch 20 \# mpls lsr-id 1.1.1.1 mpls \# mpls l2vpn \# mpls ldp \# mpls ldp remote-peer 3.3.3.3 remote-ip 3.3.3.3 \# interface Vlanif20 ip address 10.1.1.1 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid \# interface 10GE1/0/1.1 encapsulation qinq-termination qinq termination pe-vid 100 ce-vid 10 mpls l2vc 3.3.3.3 101 \# interface 10GE1/0/2 port link-type hybrid port hybrid pvid vlan 20 port hybrid tagged vlan 20 \# interface LoopBack1 ip address 1.1.1.1 255.255.255.255 \# ospf 1 area 0.0.0.0 network 1.1.1.1 0.0.0.0 network 10.1.1.0 0.0.0.255 \# return

● P
\#
sysname P
\#
router id 2.2.2.2
\#
vlan batch 20 30
\#
mpls lsr-id 2.2.2.2
mpls
\#
mpls ldp
\#
interface Vlanif20
ip address 10.1.1.2 255.255.255.0
mpls
mpls ldp
\#
interface Vlanif30
ip address 10.2.2.2 255.255.255.0
mpls
mpls ldp
\#
interface 10GE1/0/1
port link-type hybrid
port hybrid pvid vlan 30
port hybrid tagged vlan 30
\#
interface 10GE1/0/2
port link-type hybrid
port hybrid pvid vlan 20
port hybrid tagged vlan 20
\#
interface LoopBack1
ip address 2.2.2.2 255.255.255.255
\#
ospf 1
area 0.0.0.0
network 2.2.2.2 0.0.0.0
network 10.1.1.0 0.0.0.255
network 10.2.2.0 0.0.0.255
\#
return
● PE2
\#
sysname PE2
\#
router id 3.3.3.3
\#
vcmp role silent
\#
vlan batch 30
\#
mpls lsr-id 3.3.3.3
mpls
\#
mpls l2vpn
\#
mpls ldp
\#
mpls ldp remote-peer 1.1.1.1
remote-ip 1.1.1.1
\#
interface Vlanif30
ip address 10.2.2.1 255.255.255.0
mpls
mpls ldp
\#

interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 30 port hybrid tagged vlan 30 \# interface 10GE1/0/2 port link-type hybrid \# interface 10GE1/0/2.1 encapsulation qinq-termination qinq termination pe-vid 100 ce-vid 10 mpls l2vc 1.1.1.1 101 \# interface LoopBack1 ip address 3.3.3.3 255.255.255.255 \# ospf 1 area 0.0.0.0 network 3.3.3.3 0.0.0.0 network 10.2.2.0 0.0.0.255 \# return

#### 4.24.25 举例：配置Dot1q终结子接口接入VPLS

组网需求如图4-47所示，PE1和PE2启动VPLS功能。CE1连接PE1设备，CE2连接PE2。CE1和CE2属于一个VPLS。采用LDP作为VPLS信令建立PW，配置VPLS，实现CE1与CE2的互通。
图 4-47 配置 Dot1q 终结子接口接入 VPLS 组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
配置思路采用如下的思路配置：
1. 在骨干网上配置路由协议实现互通。
2. 在PE连接CE的接口上配置Dot1q子接口接入VPLS。
3. 在PE之间建立远端LDP会话。

4. PE间建立传输业务数据所使用的隧道。
5. PE上使能MPLS L2VPN。
6. 在PE上创建VSI，指定信令为LDP。
说明
VCMP的角色是Client时，不能配置VLAN终结子接口。
操作步骤
步骤1 按图4-47配置各接口所属的VLAN
说明
避免将PE上AC侧和PW侧的物理接口加入相同的VLAN中，否则可能引起环路。
\# 配置CE1，要求CE1发送给PE1的报文带有一层VLAN Tag。
<HUAWEI> system-view
[HUAWEI] sysname CE1
[CE1] vlan batch 10
[CE1] interface 10ge 1/0/1
[CE1-10GE1/0/1] port link-type trunk
[CE1-10GE1/0/1] port trunk allow-pass vlan 10
[CE1-10GE1/0/1] quit
[CE1] interface vlanif 10
[CE1-Vlanif10] ip address 10.1.1.1 24
[CE1-Vlanif10] quit
\# 配置CE2，要求CE2发送给PE2的报文带有一层VLAN Tag。
<HUAWEI> system-view
[HUAWEI] sysname CE2
[CE2] vlan batch 10
[CE2] interface 10ge 1/0/1
[CE2-10GE1/0/1] port link-type trunk
[CE2-10GE1/0/1] port trunk allow-pass vlan 10
[CE2-10GE1/0/1] quit
[CE2] interface vlanif 10
[CE2-Vlanif10] ip address 10.1.1.2 24
[CE2-Vlanif10] quit
\# 配置PE1。
<HUAWEI> system-view
[HUAWEI] sysname PE1
[PE1] vlan batch 20
[PE1] interface 10ge 1/0/2
[PE1-10GE1/0/2] port link-type hybrid
[PE1-10GE1/0/2] port hybrid pvid vlan 20
[PE1-10GE1/0/2] port hybrid tagged vlan 20
[PE1-10GE1/0/2] quit
[PE1] interface vlanif 20
[PE1-Vlanif20] ip address 4.4.4.4 24
[PE1-Vlanif20] quit
\# 配置P。
<HUAWEI> system-view
[HUAWEI] sysname P
[P] vlan batch 20 30
[P] interface 10ge 1/0/1
[P-10GE1/0/1] port link-type hybrid
[P-10GE1/0/1] port hybrid pvid vlan 20
[P-10GE1/0/1] port hybrid tagged vlan 20
[P-10GE1/0/1] quit
[P] interface 10ge 1/0/2
[P-10GE1/0/2] port link-type hybrid
[P-10GE1/0/2] port hybrid pvid vlan 30

[P-10GE1/0/2] port hybrid tagged vlan 30 [P-10GE1/0/2] quit [P] interface vlanif 20 [P-Vlanif20] ip address 4.4.4.5 24 [P-Vlanif20] quit [P] interface vlanif 30 [P-Vlanif30] ip address 5.5.5.4 24 [P-Vlanif30] quit \# 配置PE2。
<HUAWEI> system-view [HUAWEI] sysname PE2 [PE2] vlan batch 30 [PE2] interface 10ge 1/0/1 [PE2-10GE1/0/1] port link-type hybrid [PE2-10GE1/0/1] port hybrid pvid vlan 30 [PE2-10GE1/0/1] port hybrid tagged vlan 30 [PE2-10GE1/0/1] quit [PE2] interface vlanif 30 [PE2-Vlanif30] ip address 5.5.5.5 24 [PE2-Vlanif30] quit步骤2 在MPLS骨干网上配置IGP，本示例中使用OSPF。
配置 OSPF 时，注意需要发布 PE1 、 P 和 PE2 作为 LSR ID 的 32 位 Loopback 接口地址。
\# 配置PE1。
[PE1] router id 1.1.1.1 [PE1] interface loopback 1 [PE1-LoopBack1] ip address 1.1.1.1 32 [PE1-LoopBack1] quit [PE1] ospf 1 [PE1-ospf-1] area 0 [PE1-ospf-1-area-0.0.0.0] network 1.1.1.1 0.0.0.0 [PE1-ospf-1-area-0.0.0.0] network 4.4.4.4 0.0.0.255 [PE1-ospf-1-area-0.0.0.0] quit [PE1-ospf-1] quit \# 配置P。
[P] router id 2.2.2.2 [P] interface loopback 1 [P-LoopBack1] ip address 2.2.2.2 32 [P-LoopBack1] quit [P] ospf 1 [P-ospf-1] area 0 [P-ospf-1-area-0.0.0.0] network 2.2.2.2 0.0.0.0 [P-ospf-1-area-0.0.0.0] network 4.4.4.5 0.0.0.255 [P-ospf-1-area-0.0.0.0] network 5.5.5.4 0.0.0.255 [P-ospf-1-area-0.0.0.0] quit [P-ospf-1] quit \# 配置PE2。
[PE2] router id 3.3.3.3 [PE2] interface loopback 1 [PE2-LoopBack1] ip address 3.3.3.3 32 [PE2-LoopBack1] quit [PE2] ospf 1 [PE2-ospf-1] area 0 [PE2-ospf-1-area-0.0.0.0] network 3.3.3.3 0.0.0.0 [PE2-ospf-1-area-0.0.0.0] network 5.5.5.5 0.0.0.255 [PE2-ospf-1-area-0.0.0.0] quit [PE2-ospf-1] quit \# 配置完成后，PE1、P、PE2之间应能建立OSPF邻居关系，执行display ip routing- table命令可以看到PE之间学习到对方的Loopback1接口路由。以PE1的显示为例：

[PE1] display ip routing-table Route Flags: R - relay, D - download to fib, T - to vpn-instance
------------------------------------------------------------------------------ Routing Tables: Public Destinations : 8 Routes : 8 Destination/Mask Proto Pre Cost Flags NextHop Interface
1.1.1.1/32 Direct 0 0 D 127.0.0.1 LoopBack1
2.2.2.2/32 OSPF 10 1 D 4.4.4.5 Vlanif20
3.3.3.3/32 OSPF 10 2 D 4.4.4.5 Vlanif20
4.4.4.0/24 Direct 0 0 D 4.4.4.4 Vlanif20
4.4.4.4/32 Direct 0 0 D 127.0.0.1 Vlanif20
5.5.5.0/24 OSPF 10 2 D 4.4.4.5 Vlanif20
127.0.0.0/8 Direct 0 0 D 127.0.0.1 InLoopBack0
127.0.0.1/32 Direct 0 0 D 127.0.0.1 InLoopBack0步骤3 在MPLS骨干网上配置MPLS基本能力和LDP。
\# 配置PE1。
[PE1] mpls lsr-id 1.1.1.1 [PE1] mpls [PE1-mpls] quit [PE1] mpls ldp [PE1-mpls-ldp] quit [PE1] interface vlanif 20 [PE1-Vlanif20] mpls [PE1-Vlanif20] mpls ldp [PE1-Vlanif20] quit \# 配置P。
[P] mpls lsr-id 2.2.2.2 [P] mpls [P-mpls] quit [P] mpls ldp [P-mpls-ldp] quit [P] interface vlanif 20 [P-Vlanif20] mpls [P-Vlanif20] mpls ldp [P-Vlanif20] quit [P] interface vlanif 30 [P-Vlanif30] mpls [P-Vlanif30] mpls ldp [P-Vlanif30] quit \# 配置PE2。
[PE2] mpls lsr-id 3.3.3.3 [PE2] mpls [PE2-mpls] quit [PE2] mpls ldp [PE2-mpls-ldp] quit [PE2] interface vlanif 30 [PE2-Vlanif30] mpls [PE2-Vlanif30] mpls ldp [PE2-Vlanif30] quit配置完成后在PE1、P和PE2上执行display mpls ldp session命令可以看到PE1和P之间或PE2和P之间的对等体的Status项为“Operational”，即对等体关系已建立。执行display mpls lsp命令可以看到LSP的建立情况。以PE1的显示为例：
[PE1] display mpls ldp session LDP Session(s) in Public Network Codes: LAM(Label Advertisement Mode), SsnAge Unit(DDDD:HH:MM)
A '*' before a session means the session is being deleted.
------------------------------------------------------------------------------ PeerID Status LAM SsnRole SsnAge KASent/Rcv
------------------------------------------------------------------------------

2.2.2.2:0 Operational DU Passive 0000:15:29 3717/3717
------------------------------------------------------------------------------
TOTAL: 1 session(s) Found.
步骤4 在PE之间建立远端LDP会话。
\# 配置PE1。
[PE1] mpls ldp remote-peer 3.3.3.3
[PE1-mpls-ldp-remote-3.3.3.3] remote-ip 3.3.3.3
[PE1-mpls-ldp-remote-3.3.3.3] quit
\# 配置PE2。
[PE2] mpls ldp remote-peer 1.1.1.1
[PE2-mpls-ldp-remote-1.1.1.1] remote-ip 1.1.1.1
[PE2-mpls-ldp-remote-1.1.1.1] quit
上述配置完成后，在PE1或PE2上执行display mpls ldp session命令可以看到PE1和
PE2之间的对等体的Status项为“Operational”，即远端对等体关系已建立。
以PE1的显示为例：
[PE1] display mpls ldp session
LDP Session(s) in Public Network
Codes: LAM(Label Advertisement Mode), SsnAge Unit(DDDD:HH:MM)
A '*' before a session means the session is being deleted.
------------------------------------------------------------------------------
PeerID Status LAM SsnRole SsnAge KASent/Rcv
------------------------------------------------------------------------------
2.2.2.2:0 Operational DU Passive 0000:15:29 3717/3717
3.3.3.3:0 Operational DU Passive 0000:00:00 2/2
------------------------------------------------------------------------------
TOTAL: 2 session(s) Found.
步骤5 在PE上使能MPLS L2VPN。
\# 配置PE1
[PE1] mpls l2vpn
[PE1-l2vpn] quit
\# 配置PE2
[PE2] mpls l2vpn
[PE2-l2vpn] quit
步骤6 在PE上配置VSI。
\# 配置PE1。
[PE1] vsi a2 static
[PE1-vsi-a2] pwsignal ldp
[PE1-vsi-a2-ldp] vsi-id 2
[PE1-vsi-a2-ldp] peer 3.3.3.3
[PE1-vsi-a2-ldp] quit
[PE1-vsi-a2] quit
\# 配置PE2。
[PE2] vsi a2 static
[PE2-vsi-a2] pwsignal ldp
[PE2-vsi-a2-ldp] vsi-id 2
[PE2-vsi-a2-ldp] peer 1.1.1.1
[PE2-vsi-a2-ldp] quit
[PE2-vsi-a2] quit
步骤7 在PE上配置VSI与接口的绑定。
\# 配置PE1。

[PE1] vcmp role silent [PE1] interface 10ge 1/0/1 [PE1-10GE1/0/1] port link-type hybrid [PE1-10GE1/0/1] quit [PE1] interface 10ge 1/0/1.1 [PE1-10GE1/0/1.1] dot1q termination vid 10 [PE1-10GE1/0/1.1] l2 binding vsi a2 [PE1-10GE1/0/1.1] quit \# 配置PE2。
[PE2] vcmp role silent [PE2] interface 10ge 1/0/2 [PE2-10GE1/0/2] port link-type hybrid [PE2-10GE1/0/2] quit [PE2] interface 10ge 1/0/2.1 [PE2-10GE1/0/2.1] dot1q termination vid 10 [PE2-10GE1/0/2.1] l2 binding vsi a2 [PE2-10GE1/0/2.1] quit
----结束检查配置结果完成上述配置后，在PE1上执行display vsi name a2 verbose命令，可以看到名字为a2的VSI建立了一条PW到PE2，VSI状态为UP。
[PE1] display vsi name a2 verbose
***VSI Name : a2 Work Mode : normal Administrator VSI : no Isolate Spoken : disable VSI Index : 4 PW Signaling : ldp Member Discovery Style : static PW MAC Learn Style : unqualify Encapsulation Type : vlan MTU : 1500 Diffserv Mode : uniform Service Class : cs- Color : -- DomainId : - Domain Name : - Ignore AcState : disable P2P VSI : disable Multicast Fast Switch : disable Create Time : 0 days, 0 hours, 3 minutes, 50 seconds VSI State : up Resource Status : -- VSI ID : 2
*Peer Router ID : 3.3.3.3 Negotiation-vc-id : 2 Encapsulation Type : vlan primary or secondary : primary ignore-standby-state : no VC Label : 1031 Peer Type : dynamic Session : up Tunnel ID : 0x0000000001004cab43 Broadcast Tunnel ID : -- Broad BackupTunnel ID : -- CKey : 193 NKey : 16777441 Stp Enable : 0 PwIndex : 193 Control Word : disable

BFD for PW : unavailable Interface Name : 10GE1/0/1.1 State : up Ac Block State : unblocked Access Port : false Last Up Time : 2024/08/03 11:35:21 Total Up Time : 0 days, 0 hours, 3 minutes, 42 seconds
**PW Information:
*Peer Ip Address : 3.3.3.3 PW State : up Local VC Label : 1031 Remote VC Label : 1031 Remote Control Word : disable PW Type : label Local VCCV : alert lsp-ping bfd Remote VCCV : alert lsp-ping bfd Tunnel ID : 0x0000000001004cab43 Broadcast Tunnel ID : -- Broad BackupTunnel ID : -- Ckey : 193 Nkey : 16777441 Main PW Token : 0x0 Slave PW Token : 0x0 Tnl Type : ldp OutInterface : -- Backup OutInterface : -- Stp Enable : 0 Mac Flapping : 0 PW Last Up Time : 2024/08/03 11:36:54 PW Total Up Time : 0 days, 0 hours, 2 minutes, 9 seconds在CE1（10.1.1.1）上能够ping通CE2（10.1.1.2）。
[CE1] ping 10.1.1.2 PING 10.1.1.2: 56 data bytes, press CTRL_C to break Reply from 10.1.1.2: bytes=56 Sequence=1 ttl=255 time=90 ms Reply from 10.1.1.2: bytes=56 Sequence=2 ttl=255 time=77 ms Reply from 10.1.1.2: bytes=56 Sequence=3 ttl=255 time=34 ms Reply from 10.1.1.2: bytes=56 Sequence=4 ttl=255 time=46 ms Reply from 10.1.1.2: bytes=56 Sequence=5 ttl=255 time=94 ms
--- 10.1.1.2 ping statistics --- 5 packet(s) transmitted 5 packet(s) received
0.00% packet loss round-trip min/avg/max = 34/68/94 ms配置脚本
● CE1 \# sysname CE1 \# vlan batch 10 \# interface Vlanif10 ip address 10.1.1.1 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# return
● CE2 \# sysname CE2

\# vlan batch 10 \# interface Vlanif10 ip address 10.1.1.2 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# return
● PE1 \# sysname PE1 \# router id 1.1.1.1 \# vcmp role silent \# vlan batch 20 \# mpls lsr-id 1.1.1.1 mpls \# mpls l2vpn \# vsi a2 static pwsignal ldp vsi-id 2 peer 3.3.3.3 \# mpls ldp \# mpls ldp remote-peer 3.3.3.3 remote-ip 3.3.3.3 \# interface Vlanif20 ip address 4.4.4.4 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid \# interface 10GE1/0/1.1 encapsulation dot1q-termination dot1q termination vid 10 l2 binding vsi a2 \# interface 10GE1/0/2 port link-type hybrid port hybrid pvid vlan 20 port hybrid tagged vlan 20 \# interface LoopBack1 ip address 1.1.1.1 255.255.255.255 \# ospf 1 area 0.0.0.0 network 1.1.1.1 0.0.0.0 network 4.4.4.0 0.0.0.255 \# return
● P \# sysname P \# router id 2.2.2.2

\# vlan batch 20 30 \# mpls lsr-id 2.2.2.2 mpls \# mpls ldp \# interface Vlanif20 ip address 4.4.4.5 255.255.255.0 mpls mpls ldp \# interface Vlanif30 ip address 5.5.5.4 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 20 port hybrid tagged vlan 20 \# interface 10GE1/0/2 port link-type hybrid port hybrid pvid vlan 30 port hybrid tagged vlan 30 \# interface LoopBack1 ip address 2.2.2.2 255.255.255.255 \# ospf 1 area 0.0.0.0 network 2.2.2.2 0.0.0.0 network 4.4.4.0 0.0.0.255 network 5.5.5.0 0.0.0.255 \# return
● PE2 \# sysname PE2 \# router id 3.3.3.3 \# vcmp role silent \# vlan batch 30 \# mpls lsr-id 3.3.3.3 mpls \# mpls l2vpn \# vsi a2 static pwsignal ldp vsi-id 2 peer 1.1.1.1 \# mpls ldp \# mpls ldp remote-peer 1.1.1.1 remote-ip 1.1.1.1 \# interface Vlanif30 ip address 5.5.5.5 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1

port link-type hybrid port hybrid pvid vlan 30 port hybrid tagged vlan 30 \# interface 10GE1/0/2 port link-type hybrid \# interface 10GE1/0/2.1 encapsulation dot1q-termination dot1q termination vid 10 l2 binding vsi a2 \# interface LoopBack1 ip address 3.3.3.3 255.255.255.255 \# ospf 1 area 0.0.0.0 network 3.3.3.3 0.0.0.0 network 5.5.5.0 0.0.0.255 \# return

#### 4.24.26 举例：配置QinQ终结子接口接入VPLS

组网需求如图4-48所示，PE1和PE2启动VPLS功能。CE1通过DeviceA连接PE1，CE2通过DeviceB连接PE2。CE1和CE2属于一个VPLS。采用LDP作为VPLS信令建立PW，配置VPLS，实现CE1与CE2的互通。Device的CE侧接口配置灵活QinQ，对CE发送过来的报文打上允许通过的外层VLAN Tag。
当Device连接多个CE时，对不同CE发送过来的不同的VLAN Tag报文打上相同的外层VLAN Tag，还可以达到节省公网VLAN数量的目的。
图 4-48 配置 QinQ 终结子接口接入 VPLS 组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。

配置思路采用如下的思路配置：
1. 在骨干网上配置路由协议实现互通。
2. 在Device连接CE的接口上配置灵活QinQ。
3. 在PE之间建立远端LDP会话。
4. PE间建立传输业务数据所使用的隧道。
5. PE上使能MPLS L2VPN。
6. 在PE上创建VSI，指定信令为LDP。
7. 在PE连接Device的接口上配置QinQ子接口接入VPLS。
说明VCMP的角色是Client时，不能配置VLAN终结子接口。
操作步骤步骤 1 按图 4-48 配置各接口所属的 VLAN说明避免将PE上AC侧和PW侧的物理接口加入相同的VLAN中，否则可能引起环路。
\# 配置CE1，要求CE1发送给PE1的报文带有一层VLAN Tag。
<HUAWEI> system-view [HUAWEI] sysname CE1 [CE1] vlan batch 10 [CE1] interface 10ge 1/0/1 [CE1-10GE1/0/1] port link-type trunk [CE1-10GE1/0/1] port trunk allow-pass vlan 10 [CE1-10GE1/0/1] quit [CE1] interface vlanif 10 [CE1-Vlanif10] ip address 10.1.1.1 24 [CE1-Vlanif10] quit \# 配置CE2，要求CE2发送给PE2的报文带有一层VLAN Tag。
<HUAWEI> system-view [HUAWEI] sysname CE2 [CE2] vlan batch 10 [CE2] interface 10ge 1/0/1 [CE2-10GE1/0/1] port link-type trunk [CE2-10GE1/0/1] port trunk allow-pass vlan 10 [CE2-10GE1/0/1] quit [CE2] interface vlanif 10 [CE2-Vlanif10] ip address 10.1.1.2 24 [CE2-Vlanif10] quit \# 配置PE1。
<HUAWEI> system-view [HUAWEI] sysname PE1 [PE1] vlan batch 20 [PE1] interface 10ge 1/0/2 [PE1-10GE1/0/2] port link-type hybrid [PE1-10GE1/0/2] port hybrid pvid vlan 20 [PE1-10GE1/0/2] port hybrid tagged vlan 20 [PE1-10GE1/0/2] quit [PE1] interface vlanif 20 [PE1-Vlanif20] ip address 4.4.4.4 24 [PE1-Vlanif20] quit \# 配置P。

<HUAWEI> system-view [HUAWEI] sysname P [P] vlan batch 20 30 [P] interface 10ge 1/0/1 [P-10GE1/0/1] port link-type hybrid [P-10GE1/0/1] port hybrid pvid vlan 20 [P-10GE1/0/1] port hybrid tagged vlan 20 [P-10GE1/0/1] quit [P] interface 10ge 1/0/2 [P-10GE1/0/2] port link-type hybrid [P-10GE1/0/2] port hybrid pvid vlan 30 [P-10GE1/0/2] port hybrid tagged vlan 30 [P-10GE1/0/2] quit [P] interface vlanif 20 [P-Vlanif20] ip address 4.4.4.5 24 [P-Vlanif20] quit [P] interface vlanif 30 [P-Vlanif30] ip address 5.5.5.4 24 [P-Vlanif30] quit \# 配置PE2。
<HUAWEI> system-view [HUAWEI] sysname PE2 [PE2] vlan batch 30 [PE2] interface 10ge 1/0/1 [PE2-10GE1/0/1] port link-type hybrid [PE2-10GE1/0/1] port hybrid pvid vlan 30 [PE2-10GE1/0/1] port hybrid tagged vlan 30 [PE2-10GE1/0/1] quit [PE2] interface vlanif 30 [PE2-Vlanif30] ip address 5.5.5.5 24 [PE2-Vlanif30] quit步骤2 在Device的接口上配置灵活QinQ和允许通过的VLAN \# 配置DeviceA。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan 100 [DeviceA-vlan100] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] port link-type hybrid [DeviceA-10GE1/0/2] port hybrid tagged vlan 100 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] port link-type hybrid [DeviceA-10GE1/0/1] port hybrid untagged vlan 100 [DeviceA-10GE1/0/1] port vlan-stacking vlan 10 stack-vlan 100 [DeviceA-10GE1/0/1] quit \# 配置DeviceB。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan 100 [DeviceB-vlan100] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] port link-type hybrid [DeviceB-10GE1/0/2] port hybrid tagged vlan 100 [DeviceB-10GE1/0/2] quit [DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] port link-type hybrid [DeviceB-10GE1/0/1] port hybrid untagged vlan 100 [DeviceB-10GE1/0/1] port vlan-stacking vlan 10 stack-vlan 100 [DeviceB-10GE1/0/1] quit步骤 3 在 MPLS 骨干网上配置 IGP ，本示例中使用 OSPF 。
配置OSPF时，注意需要发布PE1、P和PE2作为LSR ID的32位Loopback接口地址。
\# 配置PE1。

[PE1] router id 1.1.1.1 [PE1] interface loopback 1 [PE1-LoopBack1] ip address 1.1.1.1 32 [PE1-LoopBack1] quit [PE1] ospf 1 [PE1-ospf-1] area 0 [PE1-ospf-1-area-0.0.0.0] network 1.1.1.1 0.0.0.0 [PE1-ospf-1-area-0.0.0.0] network 4.4.4.4 0.0.0.255 [PE1-ospf-1-area-0.0.0.0] quit [PE1-ospf-1] quit \# 配置P。
[P] router id 2.2.2.2 [P] interface loopback 1 [P-LoopBack1] ip address 2.2.2.2 32 [P-LoopBack1] quit [P] ospf 1 [P-ospf-1] area 0 [P-ospf-1-area-0.0.0.0] network 2.2.2.2 0.0.0.0 [P-ospf-1-area-0.0.0.0] network 4.4.4.5 0.0.0.255 [P-ospf-1-area-0.0.0.0] network 5.5.5.4 0.0.0.255 [P-ospf-1-area-0.0.0.0] quit [P-ospf-1] quit \# 配置 PE2 。
[PE2] router id 3.3.3.3 [PE2] interface loopback 1 [PE2-LoopBack1] ip address 3.3.3.3 32 [PE2-LoopBack1] quit [PE2] ospf 1 [PE2-ospf-1] area 0 [PE2-ospf-1-area-0.0.0.0] network 3.3.3.3 0.0.0.0 [PE2-ospf-1-area-0.0.0.0] network 5.5.5.5 0.0.0.255 [PE2-ospf-1-area-0.0.0.0] quit [PE2-ospf-1] quit配置完成后，PE1、P、PE2之间应能建立OSPF邻居关系，执行display \# ip routing- table命令可以看到PE之间学习到对方的Loopback1接口路由。以PE1的显示为例：
[PE1] display ip routing-table Route Flags: R - relay, D - download to fib, T - to vpn-instance
------------------------------------------------------------------------------ Routing Tables: Public Destinations : 8 Routes : 8 Destination/Mask Proto Pre Cost Flags NextHop Interface
1.1.1.1/32 Direct 0 0 D 127.0.0.1 LoopBack1
2.2.2.2/32 OSPF 10 1 D 4.4.4.5 Vlanif20
3.3.3.3/32 OSPF 10 2 D 4.4.4.5 Vlanif20
4.4.4.0/24 Direct 0 0 D 4.4.4.4 Vlanif20
4.4.4.4/32 Direct 0 0 D 127.0.0.1 Vlanif20
5.5.5.0/24 OSPF 10 2 D 4.4.4.5 Vlanif20
127.0.0.0/8 Direct 0 0 D 127.0.0.1 InLoopBack0
127.0.0.1/32 Direct 0 0 D 127.0.0.1 InLoopBack0步骤4 在MPLS骨干网上配置MPLS基本能力和LDP。
\# 配置PE1。
[PE1] mpls lsr-id 1.1.1.1 [PE1] mpls [PE1-mpls] quit [PE1] mpls ldp [PE1-mpls-ldp] quit [PE1] interface vlanif 20 [PE1-Vlanif20] mpls

[PE1-Vlanif20] mpls ldp [PE1-Vlanif20] quit \# 配置P。
[P] mpls lsr-id 2.2.2.2 [P] mpls [P-mpls] quit [P] mpls ldp [P-mpls-ldp] quit [P] interface vlanif 20 [P-Vlanif20] mpls [P-Vlanif20] mpls ldp [P-Vlanif20] quit [P] interface vlanif 30 [P-Vlanif30] mpls [P-Vlanif30] mpls ldp [P-Vlanif30] quit \# 配置PE2。
[PE2] mpls lsr-id 3.3.3.3 [PE2] mpls [PE2-mpls] quit [PE2] mpls ldp [PE2-mpls-ldp] quit [PE2] interface vlanif 30 [PE2-Vlanif30] mpls [PE2-Vlanif30] mpls ldp [PE2-Vlanif30] quit配置完成后在PE1、P和PE2上执行display mpls ldp session命令可以看到PE1和P之间或PE2和P之间的对等体的Status项为“Operational”，即对等体关系已建立。执行display mpls lsp命令可以看到LSP的建立情况。以PE1的显示为例：
[PE1] display mpls ldp session LDP Session(s) in Public Network Codes: LAM(Label Advertisement Mode), SsnAge Unit(DDDD:HH:MM)
A '*' before a session means the session is being deleted.
------------------------------------------------------------------------------ PeerID Status LAM SsnRole SsnAge KASent/Rcv
------------------------------------------------------------------------------
2.2.2.2:0 Operational DU Passive 0000:15:29 3717/3717
------------------------------------------------------------------------------ TOTAL: 1 session(s) Found.
步骤5 在PE之间建立远端LDP会话。
\# 配置PE1。
[PE1] mpls ldp remote-peer 3.3.3.3 [PE1-mpls-ldp-remote-3.3.3.3] remote-ip 3.3.3.3 [PE1-mpls-ldp-remote-3.3.3.3] quit \# 配置PE2。
[PE2] mpls ldp remote-peer 1.1.1.1 [PE2-mpls-ldp-remote-1.1.1.1] remote-ip 1.1.1.1 [PE2-mpls-ldp-remote-1.1.1.1] quit上述配置完成后，在PE1或PE2上执行display mpls ldp session命令可以看到PE1和PE2之间的对等体的Status项为“Operational”，即远端对等体关系已建立。
以PE1的显示为例：
[PE1] display mpls ldp session LDP Session(s) in Public Network Codes: LAM(Label Advertisement Mode), SsnAge Unit(DDDD:HH:MM)
A '*' before a session means the session is being deleted.
------------------------------------------------------------------------------

PeerID Status LAM SsnRole SsnAge KASent/Rcv
------------------------------------------------------------------------------
2.2.2.2:0 Operational DU Passive 0000:15:29 3717/3717
3.3.3.3:0 Operational DU Passive 0000:00:00 2/2
------------------------------------------------------------------------------ TOTAL: 2 session(s) Found.
步骤6 在PE上使能MPLS L2VPN。
\# 配置PE1。
[PE1] mpls l2vpn [PE1-l2vpn] quit \# 配置PE2。
[PE2] mpls l2vpn [PE2-l2vpn] quit步骤7 在PE上配置VSI。
\# 配置PE1。
[PE1] vsi a2 static [PE1-vsi-a2] pwsignal ldp [PE1-vsi-a2-ldp] vsi-id 2 [PE1-vsi-a2-ldp] peer 3.3.3.3 [PE1-vsi-a2-ldp] quit [PE1-vsi-a2] quit \# 配置PE2。
[PE2] vsi a2 static [PE2-vsi-a2] pwsignal ldp [PE2-vsi-a2-ldp] vsi-id 2 [PE2-vsi-a2-ldp] peer 1.1.1.1 [PE2-vsi-a2-ldp] quit [PE2-vsi-a2] quit步骤8 在PE上配置VSI与接口的绑定。
\# 配置PE1。
[PE1] vcmp role silent [PE1] interface 10ge 1/0/1 [PE1-10GE1/0/1] port link-type hybrid [PE1-10GE1/0/1] quit [PE1] interface 10ge 1/0/1.1 [PE1-10GE1/0/1.1] qinq termination pe-vid 100 ce-vid 10 [PE1-10GE1/0/1.1] l2 binding vsi a2 [PE1-10GE1/0/1.1] quit \# 配置 PE2 。
[PE2] vcmp role silent [PE2] interface 10ge 1/0/2 [PE2-10GE1/0/2] port link-type hybrid [PE2-10GE1/0/2] quit [PE2] interface 10ge 1/0/2.1 [PE2-10GE1/0/2.1] qinq termination pe-vid 100 ce-vid 10 [PE2-10GE1/0/2.1] l2 binding vsi a2 [PE2-10GE1/0/2.1] quit
----结束检查配置结果完成上述配置后，在PE1上执行display vsi name a2 verbose命令，可以看到名字为a2的VSI建立了一条PW到PE2，VSI状态为UP。

[PE1] display vsi name a2 verbose
***VSI Name : a2 Work Mode : normal Administrator VSI : no Isolate Spoken : disable VSI Index : 4 PW Signaling : ldp Member Discovery Style : static PW MAC Learn Style : unqualify Encapsulation Type : vlan MTU : 1500 Diffserv Mode : uniform Service Class : cs- Color : -- DomainId : - Domain Name : - Ignore AcState : disable P2P VSI : disable Multicast Fast Switch : disable Create Time : 0 days, 0 hours, 3 minutes, 50 seconds VSI State : up Resource Status : -- VSI ID : 2
*Peer Router ID : 3.3.3.3 Negotiation-vc-id : 2 Encapsulation Type : vlan primary or secondary : primary ignore-standby-state : no VC Label : 1031 Peer Type : dynamic Session : up Tunnel ID : 0x0000000001004cab43 Broadcast Tunnel ID : -- Broad BackupTunnel ID : -- CKey : 193 NKey : 16777441 Stp Enable : 0 PwIndex : 193 Control Word : disable BFD for PW : unavailable Interface Name : 10GE1/0/1.1 State : up Ac Block State : unblocked Access Port : false Last Up Time : 2024/08/03 11:35:21 Total Up Time : 0 days, 0 hours, 3 minutes, 42 seconds
**PW Information:
*Peer Ip Address : 3.3.3.3 PW State : up Local VC Label : 1031 Remote VC Label : 1031 Remote Control Word : disable PW Type : label Local VCCV : alert lsp-ping bfd Remote VCCV : alert lsp-ping bfd Tunnel ID : 0x0000000001004cab43 Broadcast Tunnel ID : -- Broad BackupTunnel ID : -- Ckey : 193 Nkey : 16777441 Main PW Token : 0x0 Slave PW Token : 0x0 Tnl Type : ldp OutInterface : --

Backup OutInterface : -- Stp Enable : 0 Mac Flapping : 0 PW Last Up Time : 2024/08/03 11:36:54 PW Total Up Time : 0 days, 0 hours, 2 minutes, 9 seconds在CE1（10.1.1.1）上能够ping通CE2（10.1.1.2）。
[CE1] ping 10.1.1.2 PING 10.1.1.2: 56 data bytes, press CTRL_C to break Reply from 10.1.1.2: bytes=56 Sequence=1 ttl=255 time=90 ms Reply from 10.1.1.2: bytes=56 Sequence=2 ttl=255 time=77 ms Reply from 10.1.1.2: bytes=56 Sequence=3 ttl=255 time=34 ms Reply from 10.1.1.2: bytes=56 Sequence=4 ttl=255 time=46 ms Reply from 10.1.1.2: bytes=56 Sequence=5 ttl=255 time=94 ms
--- 10.1.1.2 ping statistics --- 5 packet(s) transmitted 5 packet(s) received
0.00% packet loss round-trip min/avg/max = 34/68/94 ms配置脚本
● CE1 \# sysname CE1 \# vlan batch 10 \# interface Vlanif10 ip address 10.1.1.1 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# return
● CE2 \# sysname CE2 \# vlan batch 10 \# interface Vlanif10 ip address 10.1.1.2 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# return
● DeviceA \# sysname DeviceA \# vlan batch 100 \# interface 10GE1/0/1 port link-type hybrid port hybrid untagged vlan 100 port vlan-stacking vlan 10 stack-vlan 100 \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 100 \# return

● DeviceB
\#
sysname DeviceB
\#
vlan batch 100
\#
interface 10GE1/0/1
port link-type hybrid
port hybrid untagged vlan 100
port vlan-stacking vlan 10 stack-vlan 100
\#
interface 10GE1/0/2
port link-type hybrid
port hybrid tagged vlan 100
\#
return
● PE1
\#
sysname PE1
\#
router id 1.1.1.1
\#
vcmp role silent
\#
vlan batch 20
\#
mpls lsr-id 1.1.1.1
mpls
\#
mpls l2vpn
\#
vsi a2 static
pwsignal ldp
vsi-id 2
peer 3.3.3.3
\#
mpls ldp
\#
mpls ldp remote-peer 3.3.3.3
remote-ip 3.3.3.3
\#
interface Vlanif20
ip address 4.4.4.4 255.255.255.0
mpls
mpls ldp
\#
interface 10GE1/0/1
port link-type hybrid
\#
interface 10GE1/0/1.1
encapsulation qinq-termination
qinq termination pe-vid 100 ce-vid 10
l2 binding vsi a2
\#
interface 10GE1/0/2
port link-type hybrid
port hybrid pvid vlan 20
port hybrid tagged vlan 20
\#
interface LoopBack1
ip address 1.1.1.1 255.255.255.255
\#
ospf 1
area 0.0.0.0
network 1.1.1.1 0.0.0.0
network 4.4.4.0 0.0.0.255
\#
return

● P
\#
sysname P
\#
router id 2.2.2.2
\#
vlan batch 20 30
\#
mpls lsr-id 2.2.2.2
mpls
\#
mpls ldp
\#
interface Vlanif20
ip address 4.4.4.5 255.255.255.0
mpls
mpls ldp
\#
interface Vlanif30
ip address 5.5.5.4 255.255.255.0
mpls
mpls ldp
\#
interface 10GE1/0/1
port link-type hybrid
port hybrid pvid vlan 20
port hybrid tagged vlan 20
\#
interface 10GE1/0/2
port link-type hybrid
port hybrid pvid vlan 30
port hybrid tagged vlan 30
\#
interface LoopBack1
ip address 2.2.2.2 255.255.255.255
\#
ospf 1
area 0.0.0.0
network 2.2.2.2 0.0.0.0
network 4.4.4.0 0.0.0.255
network 5.5.5.0 0.0.0.255
\#
return
● PE2
\#
sysname PE2
\#
router id 3.3.3.3
\#
vcmp role silent
\#
vlan batch 30
\#
mpls lsr-id 3.3.3.3
mpls
\#
mpls l2vpn
\#
vsi a2 static
pwsignal ldp
vsi-id 2
peer 1.1.1.1
\#
mpls ldp
\#
mpls ldp remote-peer 1.1.1.1
remote-ip 1.1.1.1
\#

interface Vlanif30 ip address 5.5.5.5 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 30 port hybrid tagged vlan 30 \# interface 10GE1/0/2 port link-type hybrid \# interface 10GE1/0/2.1 encapsulation qinq-termination qinq termination pe-vid 100 ce-vid 10 l2 binding vsi a2 \# interface LoopBack1 ip address 3.3.3.3 255.255.255.255 \# ospf 1 area 0.0.0.0 network 3.3.3.3 0.0.0.0 network 5.5.5.0 0.0.0.255 \# return

#### 4.24.27 举例：配置基本QinQ

组网需求如图4-49所示，DeviceA和DeviceB下连接用户网络A和用户网络B，且DeviceA和DeviceB分布在不同的地域。DeviceA和DeviceB之间通过公网相连。公网划分给用户网络A的VLAN为100，划分给用户网络B的VLAN为200。用户希望在DeviceA和DeviceB上部署基本QinQ功能，实现用户网络A和用户网络B独立划分VLAN，互不影响；不同地域间用户网络A内的用户能够互通，不同地域间用户网络B内的用户能够互通，不同地域间用户网络A和用户网络B内的用户相互隔离。
图 4-49 配置基本 QinQ 组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。

操作步骤步骤1 创建VLAN。
\# 在DeviceA上创建VLAN100和VLAN200 <HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 100 200 \# 在DeviceB上创建VLAN100和VLAN200 <HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan batch 100 200步骤2 在DeviceA上配置接口10GE1/0/1、10GE1/0/2的类型为QinQ，10GE1/0/1的外层tag为VLAN100，10GE1/0/2的外层tag为VLAN200。DeviceB的配置与DeviceA类似，不再赘述。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type dot1q-tunnel [DeviceA-10GE1/0/1] port default vlan 100 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type dot1q-tunnel [DeviceA-10GE1/0/2] port default vlan 200 [DeviceA-10GE1/0/2] quit步骤3 在DeviceA上配置接口10GE1/0/3加入VLAN100和VLAN200。DeviceB的配置与DeviceA类似，不再赘述。
[DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] portswitch [DeviceA-10GE1/0/3] port link-type trunk [DeviceA-10GE1/0/3] port trunk allow-pass vlan 100 200 [DeviceA-10GE1/0/3] quit
----结束检查配置结果
● DeviceA下用户网络A内的任一台主机ping同一VLAN内DeviceB下用户网络A内的主机，可以ping通。
● DeviceA下用户网络B内的任一台主机ping同一VLAN内DeviceB下用户网络B内的主机，可以ping通。
● DeviceA 下用户网络 A 内的任一台主机 ping 同一 VLAN 内 DeviceB 下用户网络 B 内的主机，不能ping通。
配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 100 200 \# interface 10GE1/0/1 port link-type dot1q-tunnel port default vlan 100 \# interface 10GE1/0/2

port link-type dot1q-tunnel port default vlan 200 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 100 200 \# return
● DeviceB \# sysname DeviceB \# vlan batch 100 200 \# interface 10GE1/0/1 port link-type dot1q-tunnel port default vlan 100 \# interface 10GE1/0/2 port link-type dot1q-tunnel port default vlan 200 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 100 200 \# return

#### 4.24.28 举例：配置基于MQC的灵活QinQ

组网需求如图4-50所示，DeviceA下连接的PC1属于VLAN200，PC2属于VLAN300；DeviceD下连接的PC3属于VLAN200，PC4属于VLAN300。PC1与PC3属于同一网段，PC2与PC4属于同一网段。DeviceB与DeviceC之间的网络规划VLAN2给PC1和PC3用，规划VLAN3给PC2和PC4用。希望在DeviceB上配置基于MQC的灵活QinQ功能，实现PC1能够单向访问PC3，PC2能够单向访问PC4。
图 4-50 配置基于 MQC 的灵活 QinQ 组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。

操作步骤步骤1 创建VLAN并将接口加入VLAN。
\# 在DeviceA上创建VLAN200、VLAN300，并将接口10GE1/0/2加入VLAN200，10GE1/0/3加入VLAN300，10GE1/0/1允许VLAN200和VLAN300的报文通过。
DeviceD的配置与DeviceA相同，不再赘述。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 200 300 [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type trunk [DeviceA-10GE1/0/1] port trunk allow-pass vlan 200 300 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type access [DeviceA-10GE1/0/2] port default vlan 200 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/3 [DeviceA-10GE1/0/3] portswitch [DeviceA-10GE1/0/3] port link-type access [DeviceA-10GE1/0/3] port default vlan 300 [DeviceA-10GE1/0/3] quit \# 在DeviceB上创建VLAN2、VLAN3，即需要添加的外层VLAN；并配置接口10GE1/0/1和10GE1/0/2允许VLAN2和VLAN3报文通过。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan batch 2 3 [DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] portswitch [DeviceB-10GE1/0/1] port link-type trunk [DeviceB-10GE1/0/1] port trunk allow-pass vlan 2 3 [DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] portswitch [DeviceB-10GE1/0/2] port link-type trunk [DeviceB-10GE1/0/2] port trunk allow-pass vlan 2 3 [DeviceB-10GE1/0/2] quit

\# 在DeviceC上创建VLAN2、VLAN3，并配置接口10GE1/0/1和10GE1/0/2允许VLAN2和VLAN3报文通过。
<HUAWEI> system-view [HUAWEI] sysname DeviceC [DeviceC] vlan batch 2 3 [DeviceC] interface 10ge 1/0/1 [DeviceC-10GE1/0/1] portswitch [DeviceC-10GE1/0/1] port link-type hybrid [DeviceC-10GE1/0/1] port hybrid untagged vlan 2 3 [DeviceC-10GE1/0/1] quit [DeviceC] interface 10ge 1/0/2 [DeviceC-10GE1/0/2] portswitch [DeviceC-10GE1/0/2] port link-type hybrid [DeviceC-10GE1/0/2] port hybrid untagged vlan 2 3 [DeviceC-10GE1/0/2] quit步骤2 配置流分类、流行为、流策略。
\# 在DeviceB上配置流分类、流行为、流策略，在VLAN200报文的外层添加VLAN2，在VLAN300报文的外层添加VLAN3。
[DeviceB] traffic classifier name1 [DeviceB-classifier-name1] if-match vlan 200 [DeviceB-classifier-name1] quit [DeviceB] traffic behavior name1 [DeviceB-behavior-name1] vlan-stacking vlan 2 [DeviceB-behavior-name1] quit [DeviceB] traffic classifier name2 [DeviceB-classifier-name2] if-match vlan 300 [DeviceB-classifier-name2] quit [DeviceB] traffic behavior name2 [DeviceB-behavior-name2] vlan-stacking vlan 3 [DeviceB-behavior-name2] quit [DeviceB] traffic policy name1 [DeviceB-trafficpolicy-name1] classifier name1 behavior name1 [DeviceB-trafficpolicy-name1] classifier name2 behavior name2 [DeviceB-trafficpolicy-name1] quit步骤3 在接口上应用流策略。
\# 在DeviceB的接口10GE1/0/1上应用流策略。
[DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] traffic-policy name1 inbound [DeviceB-10GE1/0/1] quit
----结束检查配置结果配置完成后PC1能够访问PC3；PC2能够访问PC4。
配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 200 300 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 200 300 \# interface 10GE1/0/2

port link-type access port default vlan 200 \# interface 10GE1/0/3 port link-type access port default vlan 300 \# return
● DeviceB \# sysname DeviceB \# vlan batch 2 to 3 \# traffic classifier name1 type or if-match vlan 200 \# traffic classifier name2 type or if-match vlan 300 \# traffic behavior name1 vlan-stacking vlan 2 \# traffic behavior name2 vlan-stacking vlan 3 \# traffic policy name1 classifier name1 behavior name1 precedence 5 classifier name2 behavior name2 precedence 10 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 2 to 3 traffic-policy name1 inbound \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2 to 3 \# return
● DeviceC \# sysname DeviceC \# vlan batch 2 to 3 \# interface 10GE1/0/1 port link-type hybrid port hybrid untagged vlan 2 to 3 \# interface 10GE1/0/2 port link-type hybrid port hybrid untagged vlan 2 to 3 \# return
● DeviceD \# sysname DeviceD \# vlan batch 200 300 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 200 300 \# interface 10GE1/0/2 port link-type access

port default vlan 200 \# interface 10GE1/0/3 port link-type access port default vlan 300 \# return

#### 4.24.29 举例：配置基于VLAN ID的灵活QinQ

组网需求如图1 配置基于VLAN ID的灵活QinQ组网图所示，X地中的用户业务中包括业务A和业务B，Y地类似。其中，两地的业务A属于同一VLAN范围，业务B属于同一VLAN范围。
为了保证各业务之间的安全性和节省核心/骨干网VLAN ID，要求两地的流量通过核心/骨干网透明传输，相同业务之间可以互通，不同业务之间相互隔离。
图 4-51 配置基于 VLAN ID 的灵活 QinQ 组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
操作步骤步骤1 创建VLAN \# 在DeviceA的接口10GE1/0/1上创建VLAN2、VLAN3，即需要添加的外层VLAN。
DeviceB的配置与DeviceA类似，不再赘述。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 2 3步骤2 配置入接口加入VLAN。
\# 在 DeviceA 的接口 10GE1/0/1 上配置灵活 QinQ 功能。 DeviceB 的配置与 DeviceA 类似，不再赘述。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch

[DeviceA-10GE1/0/1] port link-type hybrid [DeviceA-10GE1/0/1] port hybrid untagged vlan 2 3 [DeviceA-10GE1/0/1] port vlan-stacking vlan 200 to 299 stack-vlan 2 [DeviceA-10GE1/0/1] port vlan-stacking vlan 300 to 399 stack-vlan 3 [DeviceA-10GE1/0/1] quit步骤3 配置出接口加入外层VLAN。
\# 在DeviceA上配置10GE1/0/2允许VLAN2和VLAN3报文通过。DeviceB的配置与DeviceA类似，不再赘述。
[DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type trunk [DeviceA-10GE1/0/2] port trunk allow-pass vlan 2 3 [DeviceA-10GE1/0/2] quit
----结束检查配置结果
● 从X地用户VLAN200～VLAN299的一台A业务服务器ping Y地用户同一VLAN内的A业务服务器，可以ping通则表示租户内部A业务服务器可以互相通信。
● 从X地用户VLAN300～VLAN399的一台B业务服务器ping Y地用户同一VLAN内的B业务服务器，可以ping通则表示租户内部B业务服务器可以互相通信。
● 从X地用户VLAN200～VLAN299的一台A业务服务器ping Y地用户内VLAN300～VLAN399的B业务服务器，不能ping通，则表示不同业务之间是互相隔离的。
配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 2 3 \# interface 10GE1/0/1 port link-type hybrid port hybrid untagged vlan 2 3 port vlan-stacking vlan 200 to 299 stack-vlan 2 port vlan-stacking vlan 300 to 399 stack-vlan 3 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2 3 \# return
● DeviceB \# sysname DeviceB \# vlan batch 2 3 \# interface 10GE1/0/1 port link-type hybrid port hybrid untagged vlan 2 3 port vlan-stacking vlan 200 to 299 stack-vlan 2 port vlan-stacking vlan 300 to 399 stack-vlan 3 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2 3 \# return

#### 4.24.30 举例：配置基于VLAN ID和802.1P的灵活QinQ

组网需求如图4-52所示，X地中的用户业务中包括业务A和业务B。其中，业务A和B各自属于不同VLAN。业务A和B都包含优先级不同的子业务c与d，子业务c要送至Y地，子业务d要送至Z地。为了保证不同优先级业务的安全性和节省核心/骨干网VLAN ID，要求两地的流量通过核心/骨干网透明传输，优先保证重要业务的正常通信。
为实现以上需求，可以在分别在X、Y、Z地配置相应的灵活QinQ功能，使不同优先级的业务能相互隔离，实现差异化的业务保障。
图 4-52 配置基于 VLAN ID 和 802.1P 的灵活 QinQ 组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。
操作步骤步骤1 创建VLAN \# 在DeviceA上创建VLAN2、VLAN3，即需要添加的外层VLAN。DeviceB的配置与DeviceA 类似，不再赘述。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 2 3步骤2 创建VLAN并将入接口加入VLAN。
\# 在DeviceA的接口10GE1/0/1上配置灵活QinQ功能。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] port link-type hybrid [DeviceA-10GE1/0/1] port hybrid untagged vlan 2 3 [DeviceA-10GE1/0/1] port vlan-stacking vlan 200 8021p 0 stack-vlan 2 [DeviceA-10GE1/0/1] port vlan-stacking vlan 200 8021p 1 stack-vlan 3 [DeviceA-10GE1/0/1] port vlan-stacking vlan 300 8021p 0 stack-vlan 2 [DeviceA-10GE1/0/1] port vlan-stacking vlan 300 8021p 1 stack-vlan 3 [DeviceA-10GE1/0/1] quit

\# 在DeviceB的接口10GE1/0/1上配置灵活QinQ功能。
[DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] port link-type hybrid [DeviceB-10GE1/0/1] port hybrid untagged vlan 2 [DeviceB-10GE1/0/1] port vlan-stacking vlan 200 8021p 0 stack-vlan 2 [DeviceB-10GE1/0/1] port vlan-stacking vlan 300 8021p 0 stack-vlan 2 [DeviceB-10GE1/0/1] quit \# 在DeviceB的接口10GE1/0/3上配置灵活QinQ功能。
[DeviceB] interface 10ge 1/0/3 [DeviceB-10GE1/0/3] port link-type hybrid [DeviceB-10GE1/0/3] port hybrid untagged vlan 3 [DeviceB-10GE1/0/3] port vlan-stacking vlan 200 8021p 1 stack-vlan 3 [DeviceB-10GE1/0/3] port vlan-stacking vlan 300 8021p 1 stack-vlan 3 [DeviceB-10GE1/0/3] quit步骤3 配置出接口加入外层VLAN。
\# 在DeviceA上配置10GE1/0/2允许VLAN2和VLAN3报文通过。DeviceB的配置与DeviceA类似，不再赘述。
[DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] port link-type trunk [DeviceA-10GE1/0/2] port trunk allow-pass vlan 2 3 [DeviceA-10GE1/0/2] quit
----结束检查配置结果
● 从X地用户的业务A或B的子业务c服务器，可以ping通Y地的子业务c服务器，则表示用户同一业务服务器可以互相通信。
● 从X地用户的业务A或B的子业务d服务器，可以ping通Z地的子业务d服务器，则表示用户同一业务服务器可以互相通信。
● 从X地用户的业务A或B的子业务c服务器，不能ping通Z地用户的子业务d服务器，则表示不同业务之间是互相隔离的。
配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 2 3 \# interface 10GE1/0/1 port link-type hybrid port hybrid untagged vlan 2 3 port vlan-stacking vlan 200 8021p 0 stack-vlan 2 port vlan-stacking vlan 200 8021p 1 stack-vlan 3 port vlan-stacking vlan 300 8021p 0 stack-vlan 2 port vlan-stacking vlan 300 8021p 1 stack-vlan 3 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2 3 \# return
● DeviceB \# sysname DeviceB \#

vlan batch 2 3 \# interface 10GE1/0/1 port link-type hybrid port hybrid untagged vlan 2 port vlan-stacking vlan 200 8021p 0 stack-vlan 2 port vlan-stacking vlan 300 8021p 0 stack-vlan 2 \# interface 10GE1/0/3 port link-type hybrid port hybrid untagged vlan 3 port vlan-stacking vlan 200 8021p 1 stack-vlan 3 port vlan-stacking vlan 300 8021p 1 stack-vlan 3 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2 3 \# return

#### 4.24.31 举例：配置基于VLAN Mapping的灵活QinQ

组网需求如图4-53所示，家庭网关连接的用户业务有PC上网业务、IPTV业务、VoIP业务。
楼道设备分配各种业务的VLAN为：
● PC上网业务独立的VLAN：VLAN1000～VLAN1100 IPTV业务共享的VLAN：VLAN1101
●
● VoIP业务共享的VLAN：VLAN1102
● 家庭网关共享的VLAN：VLAN1103每个小区设备下行与50个楼道设备相连，对楼道设备上送的PC上网业务VLAN分别映射为VLAN101、VLAN102、VLAN103、……VLAN150。
运营商的汇聚设备下行与50个小区设备相连，对小区设备上送的报文添加外层VLAN，分别为：VLAN21、VLAN22、VLAN23、……VLAN70。
图 4-53 配置基于 VLAN Mapping 的灵活 QinQ 组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。

配置思路采用如下的思路配置灵活QinQ以及VLAN Mapping：
1. 在DeviceA和DeviceB上创建相关VLAN。
2. 在DeviceB上配置VLAN Mapping功能，并将接口加入VLAN。
3. 在DeviceA上配置灵活QinQ功能，并将接口加入VLAN。
4. DeviceA和DeviceB的其他下行接口配置与10GE1/0/1类似，此处不再赘述。
5. DeviceA的其他下行小区交换机配置与DeviceB类似，此处不再赘述。
操作步骤步骤1 创建VLAN。
\# 配置DeviceA。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 21 to 70 1101 to 1103配置DeviceB。
\# <HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan batch 101 to 150 1000 to 1103步骤2 在DeviceB上配置VLAN Mapping功能，并将接口加入VLAN。
\# 配置接口加入VLAN。
[DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] portswitch [DeviceB-10GE1/0/1] port link-type hybrid [DeviceB-10GE1/0/1] port hybrid tagged vlan 101 1000 to 1103 [DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] portswitch [DeviceB-10GE1/0/2] port link-type hybrid [DeviceB-10GE1/0/2] port hybrid tagged vlan 101 to 150 1101 to 1103 [DeviceB-10GE1/0/2] quit \# 配置接口VLAN Mapping功能。
[DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] port vlan-mapping vlan 1000 to 1100 map-vlan 101 [DeviceB-10GE1/0/1] quit步骤3 在DeviceA上配置灵活QinQ功能，并将接口加入VLAN。
\# 配置接口加入VLAN。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type hybrid [DeviceA-10GE1/0/1] port hybrid untagged vlan 21 [DeviceA-10GE1/0/1] port hybrid tagged vlan 1101 to 1103 [DeviceA-10GE1/0/1] quit \# 配置接口灵活QinQ功能。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] port vlan-stacking vlan 101 to 150 stack-vlan 21 [DeviceA-10GE1/0/1] quit
----结束检查配置结果PC上网业务、IPTV业务、VoIP业务都可以正常使用。

配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 21 to 70 1101 to 1103 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 1101 to 1103 port hybrid untagged vlan 21 port vlan-stacking vlan 101 to 150 stack-vlan 21 \# return
● DeviceB \# sysname DeviceB \# vlan batch 101 to 150 1000 to 1103 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 101 1000 to 1103 port vlan-mapping vlan 1000 to 1100 map-vlan 101 \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 101 to 150 1101 to 1103 \# return

#### 4.24.32 举例：配置对Untagged报文添加双层VLAN Tag

组网需求如图4-54所示，PC1的用户需要向PC2的用户发送Untagged报文，同时，也仅接收Untagged的报文。PC2的用户业务需要完成同样的功能。在骨干网传输的过程中，需要为Untagged的报文添加双层VLAN Tag，节省公网VLAN的同时，保证不同用户业务之间的隔离。
图 4-54 配置对 Untagged 报文添加双层 VLAN Tag 场景的组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。

操作步骤步骤1 创建VLAN \# 在DeviceA的接口10GE1/0/1上创建VLAN2，即需要添加的外层VLAN。DeviceB的配置与DeviceA类似，不再赘述。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 2步骤2 创建VLAN并将入接口加入VLAN。
\# 在DeviceA的接口10GE1/0/1上配置为Untagged报文添加双层Tag功能。DeviceB的配置与DeviceA类似，不再赘述。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type hybrid [DeviceA-10GE1/0/1] port hybrid untagged vlan 2 [DeviceA-10GE1/0/1] port vlan-stacking untagged stack-vlan 2 stack-inner-vlan 200 [DeviceA-10GE1/0/1] quit步骤 3 配置出接口加入外层 VLAN 。
\# 在DeviceA上配置10GE1/0/2允许VLAN2报文通过。DeviceB的配置与DeviceA类似，不再赘述。
[DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type trunk [DeviceA-10GE1/0/2] port trunk allow-pass vlan 2 [DeviceA-10GE1/0/2] quit
----结束检查配置结果配置完成后，DeviceA能为PC1上送的报文添加双层VLAN Tag，并且在PC2上接收到不带VLAN Tag的报文。
配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 2 \# interface 10GE1/0/1 port link-type hybrid port hybrid untagged vlan 2 port vlan-stacking untagged stack-vlan 2 stack-inner-vlan 200 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2 \# return
● DeviceB \# sysname DeviceB \# vlan 2

\# interface 10GE1/0/1 port link-type hybrid port hybrid untagged vlan 2 port vlan-stacking untagged stack-vlan 2 stack-inner-vlan 200 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 2 \# return

#### 4.24.33 举例：配置单层QinQ Mapping子接口接入VPWS

组网需求如图4-55所示，CE1、CE2分别通过VLAN方式接入PE1和PE2。CE1和CE2之间建立LDP方式的VPWS。
图 4-55 配置单层 QinQ Mapping 子接口接入 VPWS 组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
配置思路采用如下思路配置：
1. 在骨干网相关设备（PE、P）上配置路由协议实现互通，并使能MPLS。
2. 本例使用缺省隧道策略，建立 LSP 作为传输业务数据的隧道。
3. PE上使能MPLS L2VPN，并创建VC连接。
4. 在PE1连接CE1的接口上配置单层QinQ Mapping子接口接入VPWS。
5. 在PE2连接CE2的接口上配置Dot1q子接口接入VPWS。
说明VCMP的角色是Client时，不能配置VLAN终结子接口。
操作步骤步骤1 按图4-55配置CE、PE和P的各接口所属VLAN和VLANIF接口的IP地址\# 配置CE1，要求CE1发送给PE1的报文带有一层VLAN Tag。

<HUAWEI> system-view [HUAWEI] sysname CE1 [CE1] vlan batch 10 [CE1] interface 10ge 1/0/1 [CE1-10GE1/0/1] port link-type trunk [CE1-10GE1/0/1] port trunk allow-pass vlan 10 [CE1-10GE1/0/1] quit [CE1] interface vlanif 10 [CE1-Vlanif10] ip address 10.10.10.1 24 [CE1-Vlanif10] quit \# 配置CE2，要求CE2发送给PE2的报文带有一层VLAN Tag。
<HUAWEI> system-view [HUAWEI] sysname CE2 [CE2] vlan batch 20 [CE2] interface 10ge 1/0/1 [CE2-10GE1/0/1] port link-type trunk [CE2-10GE1/0/1] port trunk allow-pass vlan 20 [CE2-10GE1/0/1] quit [CE2] interface vlanif 20 [CE2-Vlanif20] ip address 10.10.10.2 24 [CE2-Vlanif20] quit \# 配置PE1。
<HUAWEI> system-view [HUAWEI] sysname PE1 [PE1] vlan batch 20 [PE1] interface 10ge 1/0/2 [PE1-10GE1/0/2] port link-type hybrid [PE1-10GE1/0/2] port hybrid pvid vlan 20 [PE1-10GE1/0/2] port hybrid tagged vlan 20 [PE1-10GE1/0/2] quit [PE1] interface vlanif 20 [PE1-Vlanif20] ip address 10.1.1.1 24 [PE1-Vlanif20] quit \# 配置P。
<HUAWEI> system-view [HUAWEI] sysname P [P] vlan batch 20 30 [P] interface 10ge 1/0/1 [P-10GE1/0/1] port link-type hybrid [P-10GE1/0/1] port hybrid pvid vlan 30 [P-10GE1/0/1] port hybrid tagged vlan 30 [P-10GE1/0/1] quit [P] interface 10ge 1/0/2 [P-10GE1/0/2] port link-type hybrid [P-10GE1/0/2] port hybrid pvid vlan 20 [P-10GE1/0/2] port hybrid tagged vlan 20 [P-10GE1/0/2] quit [P] interface vlanif 20 [P-Vlanif20] ip address 10.1.1.2 24 [P-Vlanif20] quit [P] interface vlanif 30 [P-Vlanif30] ip address 10.2.2.2 24 [P-Vlanif30] quit \# 配置PE2。
<HUAWEI> system-view [HUAWEI] sysname PE2 [PE2] vlan batch 30 [PE2] interface 10ge 1/0/1 [PE2-10GE1/0/1] port link-type hybrid [PE2-10GE1/0/1] port hybrid pvid vlan 30 [PE2-10GE1/0/1] port hybrid tagged vlan 30 [PE2-10GE1/0/1] quit [PE2] interface vlanif 30 [PE2-Vlanif30] ip address 10.2.2.1 24 [PE2-Vlanif30] quit

步骤2 在MPLS骨干网上配置IGP，本示例中使用OSPF配置OSPF时，注意需要发布PE1、P和PE2作为LSR ID的32位Loopback接口地址。
\# 配置PE1。
[PE1] router id 1.1.1.1 [PE1] interface loopback 1 [PE1-LoopBack1] ip address 1.1.1.1 32 [PE1-LoopBack1] quit [PE1] ospf 1 [PE1-ospf-1] area 0 [PE1-ospf-1-area-0.0.0.0] network 1.1.1.1 0.0.0.0 [PE1-ospf-1-area-0.0.0.0] network 10.1.1.1 0.0.0.255 [PE1-ospf-1-area-0.0.0.0] quit [PE1-ospf-1] quit \# 配置P。
[P] router id 2.2.2.2 [P] interface loopback 1 [P-LoopBack1] ip address 2.2.2.2 32 [P-LoopBack1] quit [P] ospf 1 [P-ospf-1] area 0 [P-ospf-1-area-0.0.0.0] network 2.2.2.2 0.0.0.0 [P-ospf-1-area-0.0.0.0] network 10.1.1.2 0.0.0.255 [P-ospf-1-area-0.0.0.0] network 10.2.2.2 0.0.0.255 [P-ospf-1-area-0.0.0.0] quit [P-ospf-1] quit \# 配置PE2。
[PE2] router id 3.3.3.3 [PE2] interface loopback 1 [PE2-LoopBack1] ip address 3.3.3.3 32 [PE2-LoopBack1] quit [PE2] ospf 1 [PE2-ospf-1] area 0 [PE2-ospf-1-area-0.0.0.0] network 3.3.3.3 0.0.0.0 [PE2-ospf-1-area-0.0.0.0] network 10.2.2.1 0.0.0.255 [PE2-ospf-1-area-0.0.0.0] quit [PE2-ospf-1] quit \# 配置完成后，PE1、P、PE2之间应能建立OSPF邻居关系，执行display ospf peer命令可以看到邻居状态为Full。执行display ip routing-table命令可以看到PE之间学习到对方的Loopback1接口路由。以PE1的显示为例：
[PE1] display ospf peer (M) Indicates MADJ neighbor OSPF Process 1 with Router ID 1.1.1.1 Area 0.0.0.0 interface 10.1.1.1(Vlanif20)'s neighbors Router ID : 2.2.2.2 Address: 10.1.1.2 State : Full Mode:Nbr is Master Priority: 1 DR : 10.1.1.2 BDR: 10.1.1.1 MTU: 0 Dead timer due (in seconds) : 30 Retrans timer interval : 5 Neighbor up time : 00h06m22s Neighbor up time stamp : 2024-08-03 10:32:05 Authentication Sequence : 0 [PE1] display ip routing-table Route Flags: R - relay, D - download to fib, T - to vpn-instance
------------------------------------------------------------------------------ Routing Tables: Public Destinations : 8 Routes : 8 Destination/Mask Proto Pre Cost Flags NextHop Interface

1.1.1.1/32 Direct 0 0 D 127.0.0.1 LoopBack1
2.2.2.2/32 OSPF 10 1 D 10.1.1.2 Vlanif20
3.3.3.3/32 OSPF 10 2 D 10.1.1.2 Vlanif20
10.1.1.0/24 Direct 0 0 D 10.1.1.1 Vlanif20
10.1.1.1/32 Direct 0 0 D 127.0.0.1 Vlanif20
10.2.2.0/24 OSPF 10 2 D 10.1.1.2 Vlanif20
127.0.0.0/8 Direct 0 0 D 127.0.0.1 InLoopBack0
127.0.0.1/32 Direct 0 0 D 127.0.0.1 InLoopBack0
步骤3 在MPLS骨干网上配置MPLS基本能力和LDP。
\# 配置PE1。
[PE1] mpls lsr-id 1.1.1.1
[PE1] mpls
[PE1-mpls] quit
[PE1] mpls ldp
[PE1-mpls-ldp] quit
[PE1] interface vlanif 20
[PE1-Vlanif20] mpls
[PE1-Vlanif20] mpls ldp
[PE1-Vlanif20] quit
\# 配置P。
[P] mpls lsr-id 2.2.2.2
[P] mpls
[P-mpls] quit
[P] mpls ldp
[P-mpls-ldp] quit
[P] interface vlanif 20
[P-Vlanif20] mpls
[P-Vlanif20] mpls ldp
[P-Vlanif20] quit
[P] interface vlanif 30
[P-Vlanif30] mpls
[P-Vlanif30] mpls ldp
[P-Vlanif30] quit
\# 配置PE2。
[PE2] mpls lsr-id 3.3.3.3
[PE2] mpls
[PE2-mpls] quit
[PE2] mpls ldp
[PE2-mpls-ldp] quit
[PE2] interface vlanif 30
[PE2-Vlanif30] mpls
[PE2-Vlanif30] mpls ldp
[PE2-Vlanif30] quit
步骤 4 在 PE 之间建立远端 LDP 会话。
\# 配置PE1。
[PE1] mpls ldp remote-peer 3.3.3.3
[PE1-mpls-ldp-remote-3.3.3.3] remote-ip 3.3.3.3
[PE1-mpls-ldp-remote-3.3.3.3] quit
\# 配置PE2。
[PE2] mpls ldp remote-peer 1.1.1.1
[PE2-mpls-ldp-remote-1.1.1.1] remote-ip 1.1.1.1
[PE2-mpls-ldp-remote-1.1.1.1] quit
上述配置完成后，在 PE1 或 PE2 上执行 display mpls ldp session 命令可以看到 PE1 和
PE2之间的对等体的Status项为“Operational”，即远端对等体关系已建立。
以PE1的显示为例：

[PE1] display mpls ldp session LDP Session(s) in Public Network Codes: LAM(Label Advertisement Mode), SsnAge Unit(DDDD:HH:MM)
A '*' before a session means the session is being deleted.
------------------------------------------------------------------------------ PeerID Status LAM SsnRole SsnAge KASent/Rcv
------------------------------------------------------------------------------
2.2.2.2:0 Operational DU Passive 0000:15:29 3717/3717
3.3.3.3:0 Operational DU Passive 0000:00:00 2/2
------------------------------------------------------------------------------ TOTAL: 2 session(s) Found.
步骤5 在PE上使能MPLS L2VPN，并创建VC连接。
\# 配置PE1：在接入CE1的接口10GE1/0/1.1上创建VC。
[PE1] mpls l2vpn [PE1-l2vpn] quit [PE1] vcmp role silent [PE1] interface 10ge 1/0/1 [PE1-10GE1/0/1] port link-type hybrid [PE1-10GE1/0/1] quit [PE1] interface 10ge 1/0/1.1 [PE1-10GE1/0/1.1] qinq mapping vid 10 map-vlan vid 20 [PE1-10GE1/0/1.1] mpls l2vc 3.3.3.3 101 [PE1-10GE1/0/1.1] quit \# 配置PE2：在接入CE2的接口10GE1/0/2.1上创建VC。
[PE2] mpls l2vpn [PE2-l2vpn] quit [PE2] vcmp role silent [PE2] interface 10ge 1/0/2 [PE2-10GE1/0/2] port link-type hybrid [PE2-10GE1/0/2] quit [PE2] interface 10ge 1/0/2.1 [PE2-10GE1/0/2.1] dot1q termination vid 20 [PE2-10GE1/0/2.1] mpls l2vc 1.1.1.1 101 [PE2-10GE1/0/2.1] quit
----结束检查配置结果在PE上查看L2VPN连接信息，可以看到建立了一条L2 VC，状态为UP。
以PE1的显示为例：
[PE1] display mpls l2vc interface 10ge 1/0/1.1
*client interface : 10GE1/0/1.1 is up Administrator PW : no session state : up AC status : up VC state : up Label state : 0 Token state : 0 VC ID : 101 VC type : VLAN destination : 3.3.3.3 local group ID : 0 remote group ID : 0 local VC label : 1038 remote VC label : 1038 local AC OAM State : up local PSN OAM State : up local forwarding state : forwarding local status code : 0x0 (forwarding)
remote AC OAM state : up remote PSN OAM state : up remote forwarding state: forwarding remote status code : 0x0 (forwarding)

remote interface : 10GE1/0/2.1 ignore standby state : no BFD for PW : unavailable VCCV State : up manual fault : not set active state : active forwarding entry : exist TTL Value : 1 link state : up local VC MTU : 1500 remote VC MTU : 1500 local VCCV : alert ttl lsp-ping bfd remote VCCV : alert ttl lsp-ping bfd local control word : disable remote control word : disable tunnel policy name : -- PW template name : -- primary or secondary : primary load balance type : flow Access-port : false Switchover Flag : false VC tunnel info : 1 tunnels NO.0 TNL type : ldp , TNL ID : 0x0000000001004ccb43 create time : 0 days, 0 hours, 4 minutes, 42 seconds up time : 0 days, 0 hours, 3 minutes, 6 seconds last change time : 0 days, 0 hours, 3 minutes, 6 seconds VC last up time : 2024/08/03 14:33:29 VC total up time : 0 days, 0 hours, 3 minutes, 6 seconds CKey : 385 NKey : 16777471 PW redundancy mode : frr AdminPw interface : -- AdminPw link state : -- Forward state : send active, receive active Diffserv Mode : uniform Service Class : cs- Color : -- DomainId : - Domain Name : - CE1和CE2能够相互Ping通。
以CE1的显示为例：
[CE1] ping 10.10.10.2 PING 10.10.10.2: 56 data bytes, press CTRL_C to break Reply from 10.10.10.2: bytes=56 Sequence=1 ttl=255 time=31 ms Reply from 10.10.10.2: bytes=56 Sequence=2 ttl=255 time=10 ms Reply from 10.10.10.2: bytes=56 Sequence=3 ttl=255 time=5 ms Reply from 10.10.10.2: bytes=56 Sequence=4 ttl=255 time=2 ms Reply from 10.10.10.2: bytes=56 Sequence=5 ttl=255 time=28 ms
--- 10.10.10.2 ping statistics --- 5 packet(s) transmitted 5 packet(s) received
0.00% packet loss round-trip min/avg/max = 2/15/31 ms配置脚本
● CE1 \# sysname CE1 \# vlan batch 10 \# interface Vlanif10 ip address 10.10.10.1 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10

\# return
● CE2 \# sysname CE2 \# vlan batch 20 \# interface Vlanif20 ip address 10.10.10.2 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 20 \# return
● PE1 \# sysname PE1 \# router id 1.1.1.1 \# vcmp role silent \# vlan batch 20 \# mpls lsr-id 1.1.1.1 mpls \# mpls l2vpn \# mpls ldp \# mpls ldp remote-peer 3.3.3.3 remote-ip 3.3.3.3 \# interface Vlanif20 ip address 10.1.1.1 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid \# interface 10GE1/0/1.1 qinq mapping vid 10 map-vlan vid 20 mpls l2vc 3.3.3.3 101 \# interface 10GE1/0/2 port link-type hybrid port hybrid pvid vlan 20 port hybrid tagged vlan 20 \# interface LoopBack1 ip address 1.1.1.1 255.255.255.255 \# ospf 1 area 0.0.0.0 network 1.1.1.1 0.0.0.0 network 10.1.1.0 0.0.0.255 \# return
● P \# sysname P \# router id 2.2.2.2

\# vlan batch 20 30 \# mpls lsr-id 2.2.2.2 mpls \# mpls ldp \# interface Vlanif20 ip address 10.1.1.2 255.255.255.0 mpls mpls ldp \# interface Vlanif30 ip address 10.2.2.2 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 30 port hybrid tagged vlan 30 \# interface 10GE1/0/2 port link-type hybrid port hybrid pvid vlan 20 port hybrid tagged vlan 20 \# interface LoopBack1 ip address 2.2.2.2 255.255.255.255 \# ospf 1 area 0.0.0.0 network 2.2.2.2 0.0.0.0 network 10.1.1.0 0.0.0.255 network 10.2.2.0 0.0.0.255 \# return
● PE2 \# sysname PE2 \# router id 3.3.3.3 \# vcmp role silent \# vlan batch 30 \# mpls lsr-id 3.3.3.3 mpls \# mpls l2vpn \# mpls ldp \# mpls ldp remote-peer 1.1.1.1 remote-ip 1.1.1.1 \# interface Vlanif30 ip address 10.2.2.1 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 30 port hybrid tagged vlan 30 \# interface 10GE1/0/2

port link-type hybrid \# interface 10GE1/0/2.1 encapsulation dot1q-termination dot1q termination vid 20 mpls l2vc 1.1.1.1 101 \# interface LoopBack1 ip address 3.3.3.3 255.255.255.255 \# ospf 1 area 0.0.0.0 network 3.3.3.3 0.0.0.0 network 10.2.2.0 0.0.0.255 \# return

#### 4.24.34 举例：配置双层QinQ Mapping子接口接入VPWS

组网需求如图4-56所示，CE1、CE2分别通过VLAN方式接入PE1和PE2。CE1和CE2之间建立LDP方式的 VPWS 。 DeviceA 分别与 CE1 、 PE1 相连。 DeviceB 分别与 CE2 、 PE2 相连。 Device的CE侧接口配置灵活QinQ，对CE发送过来的报文打上允许通过的外层VLAN Tag。当DeviceA与DeviceB允许通过的VLAN不同时，需要使用双层QinQ Mapping子接口接入VPWS方式使CE1与CE2互通。
当Device连接多个CE时，对不同CE发送过来的不同的VLAN Tag报文打上相同的外层VLAN Tag，还可以达到节省公网VLAN数量的目的。
图 4-56 配置双层 QinQ Mapping 子接口接入 VPWS 组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
配置思路采用如下思路配置：

1. 在骨干网相关设备（PE、P）上配置路由协议实现互通，并使能MPLS。
2. 本例使用缺省隧道策略，建立LSP作为传输业务数据的隧道。
3. PE上使能MPLS L2VPN，并创建VC连接。
4. 在PE1连接DeviceA的接口上配置双层QinQ Mapping子接口接入VPWS。
5. 在PE2连接DeviceB的接口上配置QinQ子接口接入VPWS。
6. 在Device连接CE的接口上配置灵活QinQ。
说明
VCMP的角色是Client时，不能配置VLAN终结子接口。
操作步骤
步骤1 按图4-56配置CE、PE和P的各接口所属VLAN和VLANIF接口的IP地址
\# 配置CE1，要求CE1发送给PE1的报文带有一层VLAN Tag。
<HUAWEI> system-view
[HUAWEI] sysname CE1
[CE1] vlan batch 10
[CE1] interface 10ge 1/0/1
[CE1-10GE1/0/1] port link-type trunk
[CE1-10GE1/0/1] port trunk allow-pass vlan 10
[CE1-10GE1/0/1] quit
[CE1] interface vlanif 10
[CE1-Vlanif10] ip address 10.10.10.1 24
[CE1-Vlanif10] quit
\# 配置CE2，要求CE2发送给PE2的报文带有一层VLAN Tag。
<HUAWEI> system-view
[HUAWEI] sysname CE2
[CE2] vlan batch 10
[CE2] interface 10ge 1/0/1
[CE2-10GE1/0/1] port link-type trunk
[CE2-10GE1/0/1] port trunk allow-pass vlan 10
[CE2-10GE1/0/1] quit
[CE2] interface vlanif 10
[CE2-Vlanif10] ip address 10.10.10.2 24
[CE2-Vlanif10] quit
\# 配置PE1。
<HUAWEI> system-view
[HUAWEI] sysname PE1
[PE1] vlan batch 20
[PE1] interface 10ge 1/0/2
[PE1-10GE1/0/2] port link-type hybrid
[PE1-10GE1/0/2] port hybrid pvid vlan 20
[PE1-10GE1/0/2] port hybrid tagged vlan 20
[PE1-10GE1/0/2] quit
[PE1] interface vlanif 20
[PE1-Vlanif20] ip address 10.1.1.1 24
[PE1-Vlanif20] quit
\# 配置P。
<HUAWEI> system-view
[HUAWEI] sysname P
[P] vlan batch 20 30
[P] interface 10ge 1/0/1
[P-10GE1/0/1] port link-type hybrid
[P-10GE1/0/1] port hybrid pvid vlan 30
[P-10GE1/0/1] port hybrid tagged vlan 30
[P-10GE1/0/1] quit
[P] interface 10ge 1/0/2
[P-10GE1/0/2] port link-type hybrid

[P-10GE1/0/2] port hybrid pvid vlan 20 [P-10GE1/0/2] port hybrid tagged vlan 20 [P-10GE1/0/2] quit [P] interface vlanif 20 [P-Vlanif20] ip address 10.1.1.2 24 [P-Vlanif20] quit [P] interface vlanif 30 [P-Vlanif30] ip address 10.2.2.2 24 [P-Vlanif30] quit \# 配置PE2。
<HUAWEI> system-view [HUAWEI] sysname PE2 [PE2] vlan batch 30 [PE2] interface 10ge 1/0/1 [PE2-10GE1/0/1] port link-type hybrid [PE2-10GE1/0/1] port hybrid pvid vlan 30 [PE2-10GE1/0/1] port hybrid tagged vlan 30 [PE2-10GE1/0/1] quit [PE2] interface vlanif 30 [PE2-Vlanif30] ip address 10.2.2.1 24 [PE2-Vlanif30] quit步骤2 在Device的接口上配置灵活QinQ和允许通过的VLAN。
\# 配置 DeviceA 。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan 100 [DeviceA-vlan100] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] port link-type hybrid [DeviceA-10GE1/0/2] port hybrid tagged vlan 100 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] port link-type hybrid [DeviceA-10GE1/0/1] port hybrid untagged vlan 100 [DeviceA-10GE1/0/1] port vlan-stacking vlan 10 stack-vlan 100 [DeviceA-10GE1/0/1] quit \# 配置DeviceB。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan 200 [DeviceB-vlan200] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] port link-type hybrid [DeviceB-10GE1/0/2] port hybrid tagged vlan 200 [DeviceB-10GE1/0/2] quit [DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] port link-type hybrid [DeviceB-10GE1/0/1] port hybrid untagged vlan 200 [DeviceB-10GE1/0/1] port vlan-stacking vlan 10 stack-vlan 200 [DeviceB-10GE1/0/1] quit步骤3 在MPLS骨干网上配置IGP，本示例中使用OSPF。
配置OSPF时，注意需要发布PE1、P和PE2作为LSR ID的32位Loopback接口地址。
\# 配置PE1。
[PE1] router id 1.1.1.1 [PE1] interface loopback 1 [PE1-LoopBack1] ip address 1.1.1.1 32 [PE1-LoopBack1] quit [PE1] ospf 1 [PE1-ospf-1] area 0 [PE1-ospf-1-area-0.0.0.0] network 1.1.1.1 0.0.0.0 [PE1-ospf-1-area-0.0.0.0] network 10.1.1.1 0.0.0.255

[PE1-ospf-1-area-0.0.0.0] quit [PE1-ospf-1] quit \# 配置P。
[P] router id 2.2.2.2 [P] interface loopback 1 [P-LoopBack1] ip address 2.2.2.2 32 [P-LoopBack1] quit [P] ospf 1 [P-ospf-1] area 0 [P-ospf-1-area-0.0.0.0] network 2.2.2.2 0.0.0.0 [P-ospf-1-area-0.0.0.0] network 10.1.1.2 0.0.0.255 [P-ospf-1-area-0.0.0.0] network 10.2.2.2 0.0.0.255 [P-ospf-1-area-0.0.0.0] quit [P-ospf-1] quit \# 配置PE2。
[PE2] router id 3.3.3.3 [PE2] interface loopback 1 [PE2-LoopBack1] ip address 3.3.3.3 32 [PE2-LoopBack1] quit [PE2] ospf 1 [PE2-ospf-1] area 0 [PE2-ospf-1-area-0.0.0.0] network 3.3.3.3 0.0.0.0 [PE2-ospf-1-area-0.0.0.0] network 10.2.2.1 0.0.0.255 [PE2-ospf-1-area-0.0.0.0] quit [PE2-ospf-1] quit \# 配置完成后，PE1、P、PE2之间应能建立OSPF邻居关系，执行display ospf peer命令可以看到邻居状态为Full。执行display ip routing-table命令可以看到PE之间学习到对方的Loopback1接口路由。以PE1的显示为例：
[PE1] display ospf peer (M) Indicates MADJ neighbor OSPF Process 1 with Router ID 1.1.1.1 Area 0.0.0.0 interface 10.1.1.1(Vlanif20)'s neighbors Router ID : 2.2.2.2 Address: 10.1.1.2 State : Full Mode:Nbr is Master Priority: 1 DR : 10.1.1.2 BDR: 10.1.1.1 MTU: 0 Dead timer due (in seconds) : 30 Retrans timer interval : 5 Neighbor up time : 00h06m22s Neighbor up time stamp : 2024-08-03 10:32:05 Authentication Sequence : 0 [PE1] display ip routing-table Route Flags: R - relay, D - download to fib, T - to vpn-instance
------------------------------------------------------------------------------ Routing Tables: Public Destinations : 8 Routes : 8 Destination/Mask Proto Pre Cost Flags NextHop Interface
1.1.1.1/32 Direct 0 0 D 127.0.0.1 LoopBack1
2.2.2.2/32 OSPF 10 1 D 10.1.1.2 Vlanif20
3.3.3.3/32 OSPF 10 2 D 10.1.1.2 Vlanif20
10.1.1.0/24 Direct 0 0 D 10.1.1.1 Vlanif20
10.1.1.1/32 Direct 0 0 D 127.0.0.1 Vlanif20
10.2.2.0/24 OSPF 10 2 D 10.1.1.2 Vlanif20
127.0.0.0/8 Direct 0 0 D 127.0.0.1 InLoopBack0
127.0.0.1/32 Direct 0 0 D 127.0.0.1 InLoopBack0步骤4 在MPLS骨干网上配置MPLS基本能力和LDP。
\# 配置PE1。

[PE1] mpls lsr-id 1.1.1.1 [PE1] mpls [PE1-mpls] quit [PE1] mpls ldp [PE1-mpls-ldp] quit [PE1] interface vlanif 20 [PE1-Vlanif20] mpls [PE1-Vlanif20] mpls ldp [PE1-Vlanif20] quit \# 配置P。
[P] mpls lsr-id 2.2.2.2 [P] mpls [P-mpls] quit [P] mpls ldp [P-mpls-ldp] quit [P] interface vlanif 20 [P-Vlanif20] mpls [P-Vlanif20] mpls ldp [P-Vlanif20] quit [P] interface vlanif 30 [P-Vlanif30] mpls [P-Vlanif30] mpls ldp [P-Vlanif30] quit \# 配置PE2。
[PE2] mpls lsr-id 3.3.3.3 [PE2] mpls [PE2-mpls] quit [PE2] mpls ldp [PE2-mpls-ldp] quit [PE2] interface vlanif 30 [PE2-Vlanif30] mpls [PE2-Vlanif30] mpls ldp [PE2-Vlanif30] quit步骤5 在PE之间建立远端LDP会话。
\# 配置PE1。
[PE1] mpls ldp remote-peer 3.3.3.3 [PE1-mpls-ldp-remote-3.3.3.3] remote-ip 3.3.3.3 [PE1-mpls-ldp-remote-3.3.3.3] quit \# 配置PE2。
[PE2] mpls ldp remote-peer 1.1.1.1 [PE2-mpls-ldp-remote-1.1.1.1] remote-ip 1.1.1.1 [PE2-mpls-ldp-remote-1.1.1.1] quit上述配置完成后，在PE1或PE2上执行display session命令可以看到PE1和mpls ldp PE2之间的对等体的Status项为“Operational”，即远端对等体关系已建立。
以PE1的显示为例：
[PE1] display mpls ldp session LDP Session(s) in Public Network Codes: LAM(Label Advertisement Mode), SsnAge Unit(DDDD:HH:MM)
A '*' before a session means the session is being deleted.
------------------------------------------------------------------------------ PeerID Status LAM SsnRole SsnAge KASent/Rcv
------------------------------------------------------------------------------
2.2.2.2:0 Operational DU Passive 0000:15:29 3717/3717
3.3.3.3:0 Operational DU Passive 0000:00:00 2/2
------------------------------------------------------------------------------ TOTAL: 2 session(s) Found.

步骤6 在PE上使能MPLS L2VPN，并创建VC连接。
\# 配置PE1：在接入CE1的接口10GE1/0/1.1上创建VC。
[PE1] mpls l2vpn [PE1-l2vpn] quit [PE1] vcmp role silent [PE1] interface 10ge 1/0/1 [PE1-10GE1/0/1] port link-type hybrid [PE1-10GE1/0/1] quit [PE1] interface 10ge 1/0/1.1 [PE1-10GE1/0/1.1] qinq mapping pe-vid 100 ce-vid 10 map-vlan vid 200 [PE1-10GE1/0/1.1] mpls l2vc 3.3.3.3 101 [PE1-10GE1/0/1.1] quit \# 配置PE2：在接入CE2的接口10GE1/0/2.1上创建VC。
[PE2] mpls l2vpn [PE2-l2vpn] quit [PE2] vcmp role silent [PE2] interface 10ge 1/0/2 [PE2-10GE1/0/2] port link-type hybrid [PE2-10GE1/0/2] quit [PE2] interface 10ge 1/0/2.1 [PE2-10GE1/0/2.1] qinq termination pe-vid 200 ce-vid 10 [PE2-10GE1/0/2.1] mpls l2vc 1.1.1.1 101 [PE2-10GE1/0/2.1] quit
----结束检查配置结果在PE上查看L2VPN连接信息，可以看到建立了一条L2 VC，状态为UP。
以PE1的显示为例：
[PE1] display mpls l2vc interface 10ge 1/0/1.1
*client interface : 10GE1/0/1.1 is up Administrator PW : no session state : up AC status : up VC state : up Label state : 0 Token state : 0 VC ID : 101 VC type : VLAN destination : 3.3.3.3 local group ID : 0 remote group ID : 0 local VC label : 1038 remote VC label : 1038 local AC OAM State : up local PSN OAM State : up local forwarding state : forwarding local status code : 0x0 (forwarding)
remote AC OAM state : up remote PSN OAM state : up remote forwarding state: forwarding remote status code : 0x0 (forwarding)
remote interface : 10GE1/0/2.1 ignore standby state : no BFD for PW : unavailable VCCV State : up manual fault : not set active state : active forwarding entry : exist TTL Value : 1 link state : up local VC MTU : 1500 remote VC MTU : 1500 local VCCV : alert ttl lsp-ping bfd remote VCCV : alert ttl lsp-ping bfd

local control word : disable remote control word : disable tunnel policy name : -- PW template name : -- primary or secondary : primary load balance type : flow Access-port : false Switchover Flag : false VC tunnel info : 1 tunnels NO.0 TNL type : ldp , TNL ID : 0x0000000001004ccb43 create time : 0 days, 0 hours, 4 minutes, 42 seconds up time : 0 days, 0 hours, 3 minutes, 6 seconds last change time : 0 days, 0 hours, 3 minutes, 6 seconds VC last up time : 2024/08/03 14:33:29 VC total up time : 0 days, 0 hours, 3 minutes, 6 seconds CKey : 385 NKey : 16777471 PW redundancy mode : frr AdminPw interface : -- AdminPw link state : -- Forward state : send active, receive active Diffserv Mode : uniform Service Class : cs- Color : -- DomainId : - Domain Name : - CE1和CE2能够相互Ping通。
以CE1的显示为例：
[CE1] ping 10.10.10.2 PING 10.10.10.2: 56 data bytes, press CTRL_C to break Reply from 10.10.10.2: bytes=56 Sequence=1 ttl=255 time=6 ms Reply from 10.10.10.2: bytes=56 Sequence=2 ttl=255 time=5 ms Reply from 10.10.10.2: bytes=56 Sequence=3 ttl=255 time=5 ms Reply from 10.10.10.2: bytes=56 Sequence=4 ttl=255 time=13 ms Reply from 10.10.10.2: bytes=56 Sequence=5 ttl=255 time=5 ms
--- 10.10.10.2 ping statistics --- 5 packet(s) transmitted 5 packet(s) received
0.00% packet loss round-trip min/avg/max = 5/6/13 ms配置脚本
● CE1 \# sysname CE1 \# vlan batch 10 \# interface Vlanif10 ip address 10.10.10.1 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# return
● CE2 \# sysname CE2 \# vlan batch 10 \# interface Vlanif10 ip address 10.10.10.2 255.255.255.0 \#

interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# return
● DeviceA \# sysname DeviceA \# vlan batch 100 \# interface 10GE1/0/1 port link-type hybrid port hybrid untagged vlan 100 port vlan-stacking vlan 10 stack-vlan 100 \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 100 \# return
● DeviceB \# sysname DeviceB \# vlan batch 200 \# interface 10GE1/0/1 port link-type hybrid port hybrid untagged vlan 200 port vlan-stacking vlan 10 stack-vlan 200 \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 200 \# return
● PE1 \# sysname PE1 \# router id 1.1.1.1 \# vcmp role silent \# vlan batch 20 \# mpls lsr-id 1.1.1.1 mpls \# mpls l2vpn \# mpls ldp \# mpls ldp remote-peer 3.3.3.3 remote-ip 3.3.3.3 \# interface Vlanif20 ip address 10.1.1.1 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid \# interface 10GE1/0/1.1 qinq mapping pe-vid 100 ce-vid 10 map-vlan vid 200

mpls l2vc 3.3.3.3 101 \# interface 10GE1/0/2 port link-type hybrid port hybrid pvid vlan 20 port hybrid tagged vlan 20 \# interface LoopBack1 ip address 1.1.1.1 255.255.255.255 \# ospf 1 area 0.0.0.0 network 1.1.1.1 0.0.0.0 network 10.1.1.0 0.0.0.255 \# return
● P \# sysname P \# router id 2.2.2.2 \# vlan batch 20 30 \# mpls lsr-id 2.2.2.2 mpls \# mpls ldp \# interface Vlanif20 ip address 10.1.1.2 255.255.255.0 mpls mpls ldp \# interface Vlanif30 ip address 10.2.2.2 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 30 port hybrid tagged vlan 30 \# interface 10GE1/0/2 port link-type hybrid port hybrid pvid vlan 20 port hybrid tagged vlan 20 \# interface LoopBack1 ip address 2.2.2.2 255.255.255.255 \# ospf 1 area 0.0.0.0 network 2.2.2.2 0.0.0.0 network 10.1.1.0 0.0.0.255 network 10.2.2.0 0.0.0.255 \# return
● PE2 \# sysname PE2 \# router id 3.3.3.3 \# vcmp role silent \# vlan batch 30

\# mpls lsr-id 3.3.3.3 mpls \# mpls l2vpn \# mpls ldp \# mpls ldp remote-peer 1.1.1.1 remote-ip 1.1.1.1 \# interface Vlanif30 ip address 10.2.2.1 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 30 port hybrid tagged vlan 30 \# interface 10GE1/0/2 port link-type hybrid \# interface 10GE1/0/2.1 encapsulation qinq-termination qinq termination pe-vid 200 ce-vid 10 mpls l2vc 1.1.1.1 101 \# interface LoopBack1 ip address 3.3.3.3 255.255.255.255 \# ospf 1 area 0.0.0.0 network 3.3.3.3 0.0.0.0 network 10.2.2.0 0.0.0.255 \# return

#### 4.24.35 举例：配置单层QinQ Mapping子接口接入VPLS

组网需求如图4-57所示，PE1和PE2启动VPLS功能。CE1连接PE1设备，CE2连接PE2。CE1和CE2属于一个VPLS。采用LDP作为VPLS信令建立PW，配置VPLS，实现CE1与CE2的互通。
图 4-57 配置单层 QinQ Mapping 子接口接入 VPLS 组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。

配置思路采用如下思路配置：
1. 在骨干网相关设备上配置路由协议实现互通。
2. 在 PE 之间建立远端 LDP 会话。
3. PE间建立传输业务数据所使用的隧道。
4. PE上使能MPLS L2VPN。
5. 在PE上创建VSI，指定信令为LDP。
6. 在PE1连接CE1的接口上配置单层QinQ Mapping子接口接入VPLS。
7. 在PE2连接CE2的接口上配置Dot1q子接口接入VPLS。
说明VCMP的角色是Client时，不能配置VLAN终结子接口。
操作步骤步骤1 按图4-57配置各接口所属的VLAN说明避免将PE上AC侧和PW侧的物理接口加入相同的VLAN中，否则可能引起环路。
\# 配置CE1，要求CE1发送给PE1的报文带有一层VLAN Tag。
<HUAWEI> system-view [HUAWEI] sysname CE1 [CE1] vlan batch 10 [CE1] interface 10ge 1/0/1 [CE1-10GE1/0/1] port link-type trunk [CE1-10GE1/0/1] port trunk allow-pass vlan 10 [CE1-10GE1/0/1] quit [CE1] interface vlanif 10 [CE1-Vlanif10] ip address 10.1.1.1 24 [CE1-Vlanif10] quit \# 配置CE2，要求CE2发送给PE2的报文带有一层VLAN Tag。
<HUAWEI> system-view [HUAWEI] sysname CE2 [CE2] vlan batch 20 [CE2] interface 10ge 1/0/1 [CE2-10GE1/0/2] port link-type trunk [CE2-10GE1/0/2] port trunk allow-pass vlan 20

[CE2-10GE1/0/2] quit [CE2] interface vlanif 20 [CE2-Vlanif20] ip address 10.1.1.2 24 [CE2-Vlanif20] quit \# 配置PE1。
<HUAWEI> system-view [HUAWEI] sysname PE1 [PE1] vlan batch 20 [PE1] interface 10ge 1/0/2 [PE1-10GE1/0/2] port link-type hybrid [PE1-10GE1/0/2] port hybrid pvid vlan 20 [PE1-10GE1/0/2] port hybrid tagged vlan 20 [PE1-10GE1/0/2] quit [PE1] interface vlanif 20 [PE1-Vlanif20] ip address 4.4.4.4 24 [PE1-Vlanif20] quit \# 配置P。
<HUAWEI> system-view [HUAWEI] sysname P [P] vlan batch 20 30 [P] interface 10ge 1/0/1 [P-10GE1/0/1] port link-type hybrid [P-10GE1/0/1] port hybrid pvid vlan 20 [P-10GE1/0/1] port hybrid tagged vlan 20 [P-10GE1/0/1] quit [P] interface 10ge 1/0/2 [P-10GE1/0/2] port link-type hybrid [P-10GE1/0/2] port hybrid pvid vlan 30 [P-10GE1/0/2] port hybrid tagged vlan 30 [P-10GE1/0/2] quit [P] interface vlanif 20 [P-Vlanif20] ip address 4.4.4.5 24 [P-Vlanif20] quit [P] interface vlanif 30 [P-Vlanif30] ip address 5.5.5.4 24 [P-Vlanif30] quit \# 配置PE2。
<HUAWEI> system-view [HUAWEI] sysname PE2 [PE2] vlan batch 30 [PE2] interface 10ge 1/0/1 [PE2-10GE1/0/1] port link-type hybrid [PE2-10GE1/0/1] port hybrid pvid vlan 30 [PE2-10GE1/0/1] port hybrid tagged vlan 30 [PE2-10GE1/0/1] quit [PE2] interface vlanif 30 [PE2-Vlanif30] ip address 5.5.5.5 24 [PE2-Vlanif30] quit步骤 2 在 MPLS 骨干网上配置 IGP ，本示例中使用 OSPF 。
配置OSPF时，注意需要发布PE1、P和PE2作为LSR ID的32位Loopback接口地址。
\# 配置PE1。
[PE1] router id 1.1.1.1 [PE1] interface loopback 1 [PE1-LoopBack1] ip address 1.1.1.1 32 [PE1-LoopBack1] quit [PE1] ospf 1 [PE1-ospf-1] area 0 [PE1-ospf-1-area-0.0.0.0] network 1.1.1.1 0.0.0.0 [PE1-ospf-1-area-0.0.0.0] network 4.4.4.4 0.0.0.255 [PE1-ospf-1-area-0.0.0.0] quit [PE1-ospf-1] quit \# 配置P。

[P] router id 2.2.2.2 [P] interface loopback 1 [P-LoopBack1] ip address 2.2.2.2 32 [P-LoopBack1] quit [P] ospf 1 [P-ospf-1] area 0 [P-ospf-1-area-0.0.0.0] network 2.2.2.2 0.0.0.0 [P-ospf-1-area-0.0.0.0] network 4.4.4.5 0.0.0.255 [P-ospf-1-area-0.0.0.0] network 5.5.5.4 0.0.0.255 [P-ospf-1-area-0.0.0.0] quit [P-ospf-1] quit \# 配置PE2。
[PE2] router id 3.3.3.3 [PE2] interface loopback 1 [PE2-LoopBack1] ip address 3.3.3.3 32 [PE2-LoopBack1] quit [PE2] ospf 1 [PE2-ospf-1] area 0 [PE2-ospf-1-area-0.0.0.0] network 3.3.3.3 0.0.0.0 [PE2-ospf-1-area-0.0.0.0] network 5.5.5.5 0.0.0.255 [PE2-ospf-1-area-0.0.0.0] quit [PE2-ospf-1] quit \# 配置完成后， PE1 、 P 、 PE2 之间应能建立 OSPF 邻居关系，执行 display ip routing- table命令可以看到PE之间学习到对方的Loopback1接口路由。以PE1的显示为例：
[PE1] display ip routing-table Route Flags: R - relay, D - download to fib, T - to vpn-instance
------------------------------------------------------------------------------ Routing Tables: Public Destinations : 8 Routes : 8 Destination/Mask Proto Pre Cost Flags NextHop Interface
1.1.1.1/32 Direct 0 0 D 127.0.0.1 LoopBack1
2.2.2.2/32 OSPF 10 1 D 4.4.4.5 Vlanif20
3.3.3.3/32 OSPF 10 2 D 4.4.4.5 Vlanif20
4.4.4.0/24 Direct 0 0 D 4.4.4.4 Vlanif20
4.4.4.4/32 Direct 0 0 D 127.0.0.1 Vlanif20
5.5.5.0/24 OSPF 10 2 D 4.4.4.5 Vlanif20
127.0.0.0/8 Direct 0 0 D 127.0.0.1 InLoopBack0
127.0.0.1/32 Direct 0 0 D 127.0.0.1 InLoopBack0步骤3 在MPLS骨干网上配置MPLS基本能力和LDP。
\# 配置PE1。
[PE1] mpls lsr-id 1.1.1.1 [PE1] mpls [PE1-mpls] quit [PE1] mpls ldp [PE1-mpls-ldp] quit [PE1] interface vlanif 20 [PE1-Vlanif20] mpls [PE1-Vlanif20] mpls ldp [PE1-Vlanif20] quit \# 配置P。
[P] mpls lsr-id 2.2.2.2 [P] mpls [P-mpls] quit [P] mpls ldp [P-mpls-ldp] quit [P] interface vlanif 20 [P-Vlanif20] mpls [P-Vlanif20] mpls ldp [P-Vlanif20] quit

[P] interface vlanif 30 [P-Vlanif30] mpls [P-Vlanif30] mpls ldp [P-Vlanif30] quit \# 配置PE2。
[PE2] mpls lsr-id 3.3.3.3 [PE2] mpls [PE2-mpls] quit [PE2] mpls ldp [PE2-mpls-ldp] quit [PE2] interface vlanif 30 [PE2-Vlanif30] mpls [PE2-Vlanif30] mpls ldp [PE2-Vlanif30] quit配置完成后在PE1、P和PE2上执行display mpls ldp session命令可以看到PE1和P之间或PE2和P之间的对等体的Status项为“Operational”，即对等体关系已建立。执行display mpls lsp命令可以看到LSP的建立情况。以PE1的显示为例：
[PE1] display mpls ldp session LDP Session(s) in Public Network Codes: LAM(Label Advertisement Mode), SsnAge Unit(DDDD:HH:MM)
A '*' before a session means the session is being deleted.
------------------------------------------------------------------------------ PeerID Status LAM SsnRole SsnAge KASent/Rcv
------------------------------------------------------------------------------
2.2.2.2:0 Operational DU Passive 0000:15:29 3717/3717
------------------------------------------------------------------------------ TOTAL: 1 session(s) Found.
步骤4 在PE之间建立远端LDP会话。
\# 配置PE1。
[PE1] mpls ldp remote-peer 3.3.3.3 [PE1-mpls-ldp-remote-3.3.3.3] remote-ip 3.3.3.3 [PE1-mpls-ldp-remote-3.3.3.3] quit \# 配置PE2。
[PE2] mpls ldp remote-peer 1.1.1.1 [PE2-mpls-ldp-remote-1.1.1.1] remote-ip 1.1.1.1 [PE2-mpls-ldp-remote-1.1.1.1] quit上述配置完成后，在PE1或PE2上执行display mpls ldp session命令可以看到PE1和PE2之间的对等体的Status项为“Operational”，即远端对等体关系已建立。
以PE1的显示为例：
[PE1] display mpls ldp session LDP Session(s) in Public Network Codes: LAM(Label Advertisement Mode), SsnAge Unit(DDDD:HH:MM)
A '*' before a session means the session is being deleted.
------------------------------------------------------------------------------ PeerID Status LAM SsnRole SsnAge KASent/Rcv
------------------------------------------------------------------------------
2.2.2.2:0 Operational DU Passive 0000:15:29 3717/3717
3.3.3.3:0 Operational DU Passive 0000:00:00 2/2
------------------------------------------------------------------------------ TOTAL: 2 session(s) Found.
步骤5 在PE上使能MPLS L2VPN。
\# 配置PE1。
[PE1] mpls l2vpn [PE1-l2vpn] quit

\# 配置PE2。
[PE2] mpls l2vpn [PE2-l2vpn] quit步骤6 在PE上配置VSI。
\# 配置PE1。
[PE1] vsi a2 static [PE1-vsi-a2] pwsignal ldp [PE1-vsi-a2-ldp] vsi-id 2 [PE1-vsi-a2-ldp] peer 3.3.3.3 [PE1-vsi-a2-ldp] quit [PE1-vsi-a2] quit \# 配置PE2。
[PE2] vsi a2 static [PE2-vsi-a2] pwsignal ldp [PE2-vsi-a2-ldp] vsi-id 2 [PE2-vsi-a2-ldp] peer 1.1.1.1 [PE2-vsi-a2-ldp] quit [PE2-vsi-a2] quit步骤 7 在 PE 上配置 VSI 与接口的绑定。
\# 配置PE1。
[PE1] vcmp role silent [PE1] interface 10ge 1/0/1 [PE1-10GE1/0/1] port link-type hybrid [PE1-10GE1/0/1] quit [PE1] interface 10ge 1/0/1.1 [PE1-10GE1/0/1.1] qinq mapping vid 10 map-vlan vid 20 [PE1-10GE1/0/1.1] l2 binding vsi a2 [PE1-10GE1/0/1.1] quit \# 配置PE2。
[PE2] vcmp role silent [PE2] interface 10ge 1/0/2 [PE2-10GE1/0/2] port link-type hybrid [PE2-10GE1/0/2] quit [PE2] interface 10ge 1/0/2.1 [PE2-10GE1/0/2.1] dot1q termination vid 20 [PE2-10GE1/0/2.1] l2 binding vsi a2 [PE2-10GE1/0/2.1] quit
----结束检查配置结果完成上述配置后，在PE1上执行display vsi name a2 verbose命令，可以看到名字为a2的VSI建立了一条PW到PE2，VSI状态为UP。
[PE1] display vsi name a2 verbose
***VSI Name : a2 Work Mode : normal Administrator VSI : no Isolate Spoken : disable VSI Index : 4 PW Signaling : ldp Member Discovery Style : static PW MAC Learn Style : unqualify Encapsulation Type : vlan MTU : 1500

Diffserv Mode : uniform Service Class : cs- Color : -- DomainId : - Domain Name : - Ignore AcState : disable P2P VSI : disable Multicast Fast Switch : disable Create Time : 0 days, 0 hours, 3 minutes, 50 seconds VSI State : up Resource Status : -- VSI ID : 2
*Peer Router ID : 3.3.3.3 Negotiation-vc-id : 2 Encapsulation Type : vlan primary or secondary : primary ignore-standby-state : no VC Label : 1031 Peer Type : dynamic Session : up Tunnel ID : 0x0000000001004cab43 Broadcast Tunnel ID : -- Broad BackupTunnel ID : -- CKey : 193 NKey : 16777441 Stp Enable : 0 PwIndex : 193 Control Word : disable BFD for PW : unavailable Interface Name : 10GE1/0/1.1 State : up Ac Block State : unblocked Access Port : false Last Up Time : 2024/08/03 11:35:21 Total Up Time : 0 days, 0 hours, 3 minutes, 42 seconds
**PW Information:
*Peer Ip Address : 3.3.3.3 PW State : up Local VC Label : 1031 Remote VC Label : 1031 Remote Control Word : disable PW Type : label Local VCCV : alert lsp-ping bfd Remote VCCV : alert lsp-ping bfd Tunnel ID : 0x0000000001004cab43 Broadcast Tunnel ID : -- Broad BackupTunnel ID : -- Ckey : 193 Nkey : 16777441 Main PW Token : 0x0 Slave PW Token : 0x0 Tnl Type : ldp OutInterface : -- Backup OutInterface : -- Stp Enable : 0 Mac Flapping : 0 PW Last Up Time : 2024/08/03 11:36:54 PW Total Up Time : 0 days, 0 hours, 2 minutes, 9 seconds在CE1（10.1.1.1）上能够ping通CE2（10.1.1.2）。
[CE1] ping 10.1.1.2 PING 10.1.1.2: 56 data bytes, press CTRL_C to break Reply from 10.1.1.2: bytes=56 Sequence=1 ttl=255 time=90 ms Reply from 10.1.1.2: bytes=56 Sequence=2 ttl=255 time=77 ms Reply from 10.1.1.2: bytes=56 Sequence=3 ttl=255 time=34 ms

Reply from 10.1.1.2: bytes=56 Sequence=4 ttl=255 time=46 ms Reply from 10.1.1.2: bytes=56 Sequence=5 ttl=255 time=94 ms
--- 10.1.1.2 ping statistics --- 5 packet(s) transmitted 5 packet(s) received
0.00% packet loss round-trip min/avg/max = 34/68/94 ms配置脚本
● CE1 \# sysname CE1 \# vlan batch 10 \# interface Vlanif10 ip address 10.1.1.1 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# return
● CE2 \# sysname CE2 \# vlan batch 20 \# interface Vlanif20 ip address 10.1.1.2 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 20 \# return
● PE1 \# sysname PE1 \# router id 1.1.1.1 \# vcmp role silent \# vlan batch 20 \# mpls lsr-id 1.1.1.1 mpls \# mpls l2vpn \# vsi a2 static pwsignal ldp vsi-id 2 peer 3.3.3.3 \# mpls ldp \# mpls ldp remote-peer 3.3.3.3 remote-ip 3.3.3.3 \# interface Vlanif20 ip address 4.4.4.4 255.255.255.0 mpls

mpls ldp \# interface 10GE1/0/1 port link-type hybrid \# interface 10GE1/0/1.1 qinq mapping vid 10 map-vlan vid 20 l2 binding vsi a2 \# interface 10GE1/0/2 port link-type hybrid port hybrid pvid vlan 20 port hybrid tagged vlan 20 \# interface LoopBack1 ip address 1.1.1.1 255.255.255.255 \# ospf 1 area 0.0.0.0 network 1.1.1.1 0.0.0.0 network 4.4.4.0 0.0.0.255 \# return
● P \# sysname P \# router id 2.2.2.2 \# vlan batch 20 30 \# mpls lsr-id 2.2.2.2 mpls \# mpls ldp \# interface Vlanif20 ip address 4.4.4.5 255.255.255.0 mpls mpls ldp \# interface Vlanif30 ip address 5.5.5.4 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 20 port hybrid tagged vlan 20 \# interface 10GE1/0/2 port link-type hybrid port hybrid pvid vlan 30 port hybrid tagged vlan 30 \# interface LoopBack1 ip address 2.2.2.2 255.255.255.255 \# ospf 1 area 0.0.0.0 network 2.2.2.2 0.0.0.0 network 4.4.4.0 0.0.0.255 network 5.5.5.0 0.0.0.255 \# return
● PE2

\# sysname PE2 \# router id 3.3.3.3 \# vcmp role silent \# vlan batch 30 \# mpls lsr-id 3.3.3.3 mpls \# mpls l2vpn \# vsi a2 static pwsignal ldp vsi-id 2 peer 1.1.1.1 \# mpls ldp \# mpls ldp remote-peer 1.1.1.1 remote-ip 1.1.1.1 \# interface Vlanif30 ip address 5.5.5.5 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 30 port hybrid tagged vlan 30 \# interface 10GE1/0/2 port link-type hybrid \# interface 10GE1/0/2.1 encapsulation dot1q-termination dot1q termination vid 20 l2 binding vsi a2 \# interface LoopBack1 ip address 3.3.3.3 255.255.255.255 \# ospf 1 area 0.0.0.0 network 3.3.3.3 0.0.0.0 network 5.5.5.0 0.0.0.255 \# return

#### 4.24.36 举例：配置双层QinQ Mapping子接口接入VPLS

组网需求如图4-58所示，PE1和PE2启动VPLS功能。CE1通过DeviceA连接PE1，CE2通过DeviceB连接PE2。CE1和CE2属于一个VPLS。采用LDP作为VPLS信令建立PW，配置VPLS，实现CE1与CE2的互通。Device的CE侧接口配置灵活QinQ，对CE发送过来的报文打上允许通过的外层VLAN Tag。当DeviceA与DeviceB允许通过的VLAN不同时，需要使用双层QinQ Mapping子接口接入VPLS方式使CE1与CE2互通。
当Device连接多个CE时，对不同CE发送过来的不同的VLAN Tag报文打上相同的外层VLAN Tag，还可以达到节省公网VLAN数量的目的。

图 4-58 配置双层 QinQ Mapping 子接口接入 VPLS 组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
配置思路采用如下思路配置：
1. 在骨干网上配置路由协议实现互通。
2. 在Device连接CE的接口上配置灵活QinQ。
3. 在PE之间建立远端LDP会话。
4. PE间建立传输业务数据所使用的隧道。
5. PE上使能MPLS L2VPN。
6. 在PE上创建VSI，指定信令为LDP。
在PE1连接DeviceA的接口上配置双层QinQ Mapping子接口接入VPLS。
7.
8. 在PE2连接DeviceB的接口上配置QinQ子接口接入VPLS。
说明VCMP的角色是Client时，不能配置VLAN终结子接口。
操作步骤步骤1 按图4-58配置各接口所属的VLAN说明避免将PE上AC侧和PW侧的物理接口加入相同的VLAN中，否则可能引起环路。
\# 配置CE1，要求CE1发送给PE1的报文带有一层VLAN Tag。
<HUAWEI> system-view [HUAWEI] sysname CE1 [CE1] vlan batch 10 [CE1] interface 10ge 1/0/1

[CE1-10GE1/0/1] port link-type trunk [CE1-10GE1/0/1] port trunk allow-pass vlan 10 [CE1-10GE1/0/1] quit [CE1] interface vlanif 10 [CE1-Vlanif10] ip address 10.1.1.1 24 [CE1-Vlanif10] quit \# 配置CE2，要求CE2发送给PE2的报文带有一层VLAN Tag。
<HUAWEI> system-view [HUAWEI] sysname CE2 [CE2] vlan batch 10 [CE2] interface 10ge 1/0/1 [CE2-10GE1/0/1] port link-type trunk [CE2-10GE1/0/1] port trunk allow-pass vlan 10 [CE2-10GE1/0/1] quit [CE2] interface vlanif 10 [CE2-Vlanif10] ip address 10.1.1.2 24 [CE2-Vlanif10] quit \# 配置PE1。
<HUAWEI> system-view [HUAWEI] sysname PE1 [PE1] vlan batch 20 [PE1] interface 10ge 1/0/2 [PE1-10GE1/0/2] port link-type hybrid [PE1-10GE1/0/2] port hybrid pvid vlan 20 [PE1-10GE1/0/2] port hybrid tagged vlan 20 [PE1-10GE1/0/2] quit [PE1] interface vlanif 20 [PE1-Vlanif20] ip address 4.4.4.4 24 [PE1-Vlanif20] quit \# 配置P。
<HUAWEI> system-view [HUAWEI] sysname P [P] vlan batch 20 30 [P] interface 10ge 1/0/1 [P-10GE1/0/1] port link-type hybrid [P-10GE1/0/1] port hybrid pvid vlan 20 [P-10GE1/0/1] port hybrid tagged vlan 20 [P-10GE1/0/1] quit [P] interface 10ge 1/0/2 [P-10GE1/0/2] port link-type hybrid [P-10GE1/0/2] port hybrid pvid vlan 30 [P-10GE1/0/2] port hybrid tagged vlan 30 [P-10GE1/0/2] quit [P] interface vlanif 20 [P-Vlanif20] ip address 4.4.4.5 24 [P-Vlanif20] quit [P] interface vlanif 30 [P-Vlanif30] ip address 5.5.5.4 24 [P-Vlanif30] quit \# 配置PE2。
<HUAWEI> system-view [HUAWEI] sysname PE2 [PE2] vlan batch 30 [PE2] interface 10ge 1/0/1 [PE2-10GE1/0/1] port link-type hybrid [PE2-10GE1/0/1] port hybrid pvid vlan 30 [PE2-10GE1/0/1] port hybrid tagged vlan 30 [PE2-10GE1/0/1] quit [PE2] interface vlanif 30 [PE2-Vlanif30] ip address 5.5.5.5 24 [PE2-Vlanif30] quit步骤2 在Device的接口上配置灵活QinQ和允许通过的VLAN。
\# 配置DeviceA。

<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan 100 [DeviceA-vlan100] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] port link-type hybrid [DeviceA-10GE1/0/2] port hybrid tagged vlan 100 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] port link-type hybrid [DeviceA-10GE1/0/1] port hybrid untagged vlan 100 [DeviceA-10GE1/0/1] port vlan-stacking vlan 10 stack-vlan 100 [DeviceA-10GE1/0/1] quit \# 配置DeviceB。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan 200 [DeviceB-vlan200] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] port link-type hybrid [DeviceB-10GE1/0/2] port hybrid tagged vlan 100 [DeviceB-10GE1/0/2] quit [DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] port link-type hybrid [DeviceB-10GE1/0/1] port hybrid untagged vlan 200 [DeviceB-10GE1/0/1] port vlan-stacking vlan 10 stack-vlan 200 [DeviceB-10GE1/0/1] quit步骤3 在MPLS骨干网上配置IGP，本示例中使用OSPF。
配置OSPF时，注意需要发布PE1、P和PE2作为LSR ID的32位Loopback接口地址。
\# 配置PE1。
[PE1] router id 1.1.1.1 [PE1] interface loopback 1 [PE1-LoopBack1] ip address 1.1.1.1 32 [PE1-LoopBack1] quit [PE1] ospf 1 [PE1-ospf-1] area 0 [PE1-ospf-1-area-0.0.0.0] network 1.1.1.1 0.0.0.0 [PE1-ospf-1-area-0.0.0.0] network 4.4.4.4 0.0.0.255 [PE1-ospf-1-area-0.0.0.0] quit [PE1-ospf-1] quit \# 配置P。
[P] router id 2.2.2.2 [P] interface loopback 1 [P-LoopBack1] ip address 2.2.2.2 32 [P-LoopBack1] quit [P] ospf 1 [P-ospf-1] area 0 [P-ospf-1-area-0.0.0.0] network 2.2.2.2 0.0.0.0 [P-ospf-1-area-0.0.0.0] network 4.4.4.5 0.0.0.255 [P-ospf-1-area-0.0.0.0] network 5.5.5.4 0.0.0.255 [P-ospf-1-area-0.0.0.0] quit [P-ospf-1] quit \# 配置PE2。
[PE2] router id 3.3.3.3 [PE2] interface loopback 1 [PE2-LoopBack1] ip address 3.3.3.3 32 [PE2-LoopBack1] quit [PE2] ospf 1 [PE2-ospf-1] area 0 [PE2-ospf-1-area-0.0.0.0] network 3.3.3.3 0.0.0.0 [PE2-ospf-1-area-0.0.0.0] network 5.5.5.5 0.0.0.255

[PE2-ospf-1-area-0.0.0.0] quit [PE2-ospf-1] quit \# 配置完成后，PE1、P、PE2之间应能建立OSPF邻居关系，执行display ip routing- table命令可以看到PE之间学习到对方的Loopback1接口路由。以PE1的显示为例：
[PE1] display ip routing-table Route Flags: R - relay, D - download to fib, T - to vpn-instance
------------------------------------------------------------------------------ Routing Tables: Public Destinations : 8 Routes : 8 Destination/Mask Proto Pre Cost Flags NextHop Interface
1.1.1.1/32 Direct 0 0 D 127.0.0.1 LoopBack1
2.2.2.2/32 OSPF 10 1 D 4.4.4.5 Vlanif20
3.3.3.3/32 OSPF 10 2 D 4.4.4.5 Vlanif20
4.4.4.0/24 Direct 0 0 D 4.4.4.4 Vlanif20
4.4.4.4/32 Direct 0 0 D 127.0.0.1 Vlanif20
5.5.5.0/24 OSPF 10 2 D 4.4.4.5 Vlanif20
127.0.0.0/8 Direct 0 0 D 127.0.0.1 InLoopBack0
127.0.0.1/32 Direct 0 0 D 127.0.0.1 InLoopBack0步骤4 在MPLS骨干网上配置MPLS基本能力和LDP。
\# 配置PE1。
[PE1] mpls lsr-id 1.1.1.1 [PE1] mpls [PE1-mpls] quit [PE1] mpls ldp [PE1-mpls-ldp] quit [PE1] interface vlanif 20 [PE1-Vlanif20] mpls [PE1-Vlanif20] mpls ldp [PE1-Vlanif20] quit \# 配置P。
[P] mpls lsr-id 2.2.2.2 [P] mpls [P-mpls] quit [P] mpls ldp [P-mpls-ldp] quit [P] interface vlanif 20 [P-Vlanif20] mpls [P-Vlanif20] mpls ldp [P-Vlanif20] quit [P] interface vlanif 30 [P-Vlanif30] mpls [P-Vlanif30] mpls ldp [P-Vlanif30] quit \# 配置PE2。
[PE2] mpls lsr-id 3.3.3.3 [PE2] mpls [PE2-mpls] quit [PE2] mpls ldp [PE2-mpls-ldp] quit [PE2] interface vlanif 30 [PE2-Vlanif30] mpls [PE2-Vlanif30] mpls ldp [PE2-Vlanif30] quit配置完成后在PE1、P和PE2上执行display mpls ldp session命令可以看到PE1和P之间或PE2和P之间的对等体的Status项为“Operational”，即对等体关系已建立。执行display mpls lsp命令可以看到LSP的建立情况。以PE1的显示为例：

[PE1] display mpls ldp session LDP Session(s) in Public Network Codes: LAM(Label Advertisement Mode), SsnAge Unit(DDDD:HH:MM)
A '*' before a session means the session is being deleted.
------------------------------------------------------------------------------ PeerID Status LAM SsnRole SsnAge KASent/Rcv
------------------------------------------------------------------------------
2.2.2.2:0 Operational DU Passive 0000:15:29 3717/3717
------------------------------------------------------------------------------ TOTAL: 1 session(s) Found.
步骤5 在PE之间建立远端LDP会话。
\# 配置PE1。
[PE1] mpls ldp remote-peer 3.3.3.3 [PE1-mpls-ldp-remote-3.3.3.3] remote-ip 3.3.3.3 [PE1-mpls-ldp-remote-3.3.3.3] quit \# 配置PE2。
[PE2] mpls ldp remote-peer 1.1.1.1 [PE2-mpls-ldp-remote-1.1.1.1] remote-ip 1.1.1.1 [PE2-mpls-ldp-remote-1.1.1.1] quit上述配置完成后，在 PE1 或 PE2 上执行 display mpls ldp session 命令可以看到 PE1 和PE2之间的对等体的Status项为“Operational”，即远端对等体关系已建立。
以PE1的显示为例：
[PE1] display mpls ldp session LDP Session(s) in Public Network Codes: LAM(Label Advertisement Mode), SsnAge Unit(DDDD:HH:MM)
A '*' before a session means the session is being deleted.
------------------------------------------------------------------------------ PeerID Status LAM SsnRole SsnAge KASent/Rcv
------------------------------------------------------------------------------
2.2.2.2:0 Operational DU Passive 0000:15:29 3717/3717
3.3.3.3:0 Operational DU Passive 0000:00:00 2/2
------------------------------------------------------------------------------ TOTAL: 2 session(s) Found.
步骤6 在PE上使能MPLS L2VPN。
\# 配置PE1。
[PE1] mpls l2vpn [PE1-l2vpn] quit \# 配置PE2。
[PE2] mpls l2vpn [PE2-l2vpn] quit步骤7 在PE上配置VSI。
\# 配置PE1。
[PE1] vsi a2 static [PE1-vsi-a2] pwsignal ldp [PE1-vsi-a2-ldp] vsi-id 2 [PE1-vsi-a2-ldp] peer 3.3.3.3 [PE1-vsi-a2-ldp] quit [PE1-vsi-a2] quit \# 配置PE2。
[PE2] vsi a2 static [PE2-vsi-a2] pwsignal ldp

[PE2-vsi-a2-ldp] vsi-id 2 [PE2-vsi-a2-ldp] peer 1.1.1.1 [PE2-vsi-a2-ldp] quit [PE2-vsi-a2] quit步骤8 在PE上配置VSI与接口的绑定。
\# 配置PE1。
[PE1] vcmp role silent [PE1] interface 10ge 1/0/1 [PE1-10GE1/0/1] port link-type hybrid [PE1-10GE1/0/1] quit [PE1] interface 10ge 1/0/1.1 [PE1-10GE1/0/1.1] qinq mapping pe-vid 100 ce-vid 10 map-vlan vid 200 [PE1-10GE1/0/1.1] l2 binding vsi a2 [PE1-10GE1/0/1.1] quit \# 配置PE2。
[PE2] vcmp role silent [PE2] interface 10ge 1/0/2 [PE2-10GE1/0/2] port link-type hybrid [PE2-10GE1/0/2] quit [PE2] interface 10ge 1/0/2.1 [PE2-10GE1/0/2.1] qinq termination pe-vid 200 ce-vid 10 [PE2-10GE1/0/2.1] l2 binding vsi a2 [PE2-10GE1/0/2.1] quit
----结束检查配置结果完成上述配置后，在PE1上执行display vsi name a2 verbose命令，可以看到名字为a2的VSI建立了一条PW到PE2，VSI状态为UP。
[PE1] display vsi name a2 verbose
***VSI Name : a2 Work Mode : normal Administrator VSI : no Isolate Spoken : disable VSI Index : 4 PW Signaling : ldp Member Discovery Style : static PW MAC Learn Style : unqualify Encapsulation Type : vlan MTU : 1500 Diffserv Mode : uniform Service Class : cs- Color : -- DomainId : - Domain Name : - Ignore AcState : disable P2P VSI : disable Multicast Fast Switch : disable Create Time : 0 days, 0 hours, 3 minutes, 50 seconds VSI State : up Resource Status : -- VSI ID : 2
*Peer Router ID : 3.3.3.3 Negotiation-vc-id : 2 Encapsulation Type : vlan primary or secondary : primary ignore-standby-state : no VC Label : 1031 Peer Type : dynamic

Session : up Tunnel ID : 0x0000000001004cab43 Broadcast Tunnel ID : -- Broad BackupTunnel ID : -- CKey : 193 NKey : 16777441 Stp Enable : 0 PwIndex : 193 Control Word : disable BFD for PW : unavailable Interface Name : 10GE1/0/1.1 State : up Ac Block State : unblocked Access Port : false Last Up Time : 2024/08/03 11:35:21 Total Up Time : 0 days, 0 hours, 3 minutes, 42 seconds
**PW Information:
*Peer Ip Address : 3.3.3.3 PW State : up Local VC Label : 1031 Remote VC Label : 1031 Remote Control Word : disable PW Type : label Local VCCV : alert lsp-ping bfd Remote VCCV : alert lsp-ping bfd Tunnel ID : 0x0000000001004cab43 Broadcast Tunnel ID : -- Broad BackupTunnel ID : -- Ckey : 193 Nkey : 16777441 Main PW Token : 0x0 Slave PW Token : 0x0 Tnl Type : ldp OutInterface : -- Backup OutInterface : -- Stp Enable : 0 Mac Flapping : 0 PW Last Up Time : 2024/08/03 11:36:54 PW Total Up Time : 0 days, 0 hours, 2 minutes, 9 seconds在CE1（10.1.1.1）上能够ping通CE2（10.1.1.2）。
[CE1] ping 10.1.1.2 PING 10.1.1.2: 56 data bytes, press CTRL_C to break Reply from 10.1.1.2: bytes=56 Sequence=1 ttl=255 time=90 ms Reply from 10.1.1.2: bytes=56 Sequence=2 ttl=255 time=77 ms Reply from 10.1.1.2: bytes=56 Sequence=3 ttl=255 time=34 ms Reply from 10.1.1.2: bytes=56 Sequence=4 ttl=255 time=46 ms Reply from 10.1.1.2: bytes=56 Sequence=5 ttl=255 time=94 ms
--- 10.1.1.2 ping statistics --- 5 packet(s) transmitted 5 packet(s) received
0.00% packet loss round-trip min/avg/max = 34/68/94 ms配置脚本
● CE1 \# sysname CE1 \# vlan batch 10 \# interface Vlanif10 ip address 10.1.1.1 255.255.255.0

\# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# return
● CE2 \# sysname CE2 \# vlan batch 10 \# interface Vlanif10 ip address 10.1.1.2 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# return
● DeviceA \# sysname DeviceA \# vlan batch 100 \# interface 10GE1/0/1 port link-type hybrid port hybrid untagged vlan 100 port vlan-stacking vlan 10 stack-vlan 100 \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 100 \# return
● DeviceB \# sysname DeviceB \# vlan batch 200 \# interface 10GE1/0/1 port link-type hybrid port hybrid untagged vlan 200 port vlan-stacking vlan 10 stack-vlan 200 \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 200 \# return
● PE1 \# sysname PE1 \# router id 1.1.1.1 \# vcmp role silent \# vlan batch 20 \# mpls lsr-id 1.1.1.1 mpls \# mpls l2vpn \#

vsi a2 static pwsignal ldp vsi-id 2 peer 3.3.3.3 \# mpls ldp \# mpls ldp remote-peer 3.3.3.3 remote-ip 3.3.3.3 \# interface Vlanif20 ip address 4.4.4.4 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid \# interface 10GE1/0/1.1 qinq mapping pe-vid 100 ce-vid 10 map-vlan vid 200 l2 binding vsi a2 \# interface 10GE1/0/2 port link-type hybrid port hybrid pvid vlan 20 port hybrid tagged vlan 20 \# interface LoopBack1 ip address 1.1.1.1 255.255.255.255 \# ospf 1 area 0.0.0.0 network 1.1.1.1 0.0.0.0 network 4.4.4.0 0.0.0.255 \# return
● P \# sysname P \# router id 2.2.2.2 \# vlan batch 20 30 \# mpls lsr-id 2.2.2.2 mpls \# mpls ldp \# interface Vlanif20 ip address 4.4.4.5 255.255.255.0 mpls mpls ldp \# interface Vlanif30 ip address 5.5.5.4 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 20 port hybrid tagged vlan 20 \# interface 10GE1/0/2 port link-type hybrid port hybrid pvid vlan 30 port hybrid tagged vlan 30 \#

interface LoopBack1 ip address 2.2.2.2 255.255.255.255 \# ospf 1 area 0.0.0.0 network 2.2.2.2 0.0.0.0 network 4.4.4.0 0.0.0.255 network 5.5.5.0 0.0.0.255 \# return
● PE2 \# sysname PE2 \# router id 3.3.3.3 \# vcmp role silent \# vlan batch 30 \# mpls lsr-id 3.3.3.3 mpls \# mpls l2vpn \# vsi a2 static pwsignal ldp vsi-id 2 peer 1.1.1.1 \# mpls ldp \# mpls ldp remote-peer 1.1.1.1 remote-ip 1.1.1.1 \# interface Vlanif30 ip address 5.5.5.5 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 30 port hybrid tagged vlan 30 \# interface 10GE1/0/2 port link-type hybrid \# interface 10GE1/0/2.1 encapsulation qinq-termination qinq termination pe-vid 200 ce-vid 10 l2 binding vsi a2 \# interface LoopBack1 ip address 3.3.3.3 255.255.255.255 \# ospf 1 area 0.0.0.0 network 3.3.3.3 0.0.0.0 network 5.5.5.0 0.0.0.255 \# return

#### 4.24.37 举例：配置QinQ Stacking子接口接入VPWS

组网需求如图4-59所示，CE1、CE2分别通过VLAN方式接入PE1和PE2。CE1和CE2之间建立LDP方式的VPWS。DeviceA分别与CE1、PE1相连。DeviceB分别与CE2、PE2相连。
DeviceA对CE1上送报文的VLAN Tag不进行改变，转发到PE1。DeviceB的CE2侧接口配置灵活QinQ，对CE发送过来的报文打上允许通过的外层VLAN Tag。DeviceB上送到PE2的报文带有双层VLAN Tag，所以需要在PE1上配置QinQ Stacking子接口接入VPWS方式使CE1与CE2互通。
当Device连接多个CE时，对不同CE发送过来的不同的VLAN Tag报文打上相同的外层VLAN Tag，还可以达到节省公网VLAN数量的目的。
图 4-59 配置 QinQ Stacking 子接口接入 VPWS 组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
配置思路采用如下的思路配置：
1. 在骨干网相关设备（PE、P）上配置路由协议实现互通，并使能MPLS。
2. 本例使用缺省隧道策略，建立LSP作为传输业务数据的隧道。
3. PE上使能MPLS L2VPN，并创建VC连接。
4. 在PE1连接DeviceA的接口上配置QinQ Stacking子接口接入VPWS。
5. 在PE2连接DeviceB的接口上配置QinQ子接口接入VPWS。
6. 在DeviceA连接CE1的接口上配置允许VLAN通过。
7. 在DeviceB连接CE2的接口上配置灵活QinQ。
说明VCMP的角色是Client时，不能配置VLAN终结子接口。

操作步骤步骤1 按图4-59配置CE、PE和P的各接口所属VLAN和VLANIF接口的IP地址\# 配置CE1，要求CE1发送给PE1的报文带有一层VLAN Tag。
<HUAWEI> system-view [HUAWEI] sysname CE1 [CE1] vlan batch 10 [CE1] interface 10ge 1/0/1 [CE1-10GE1/0/1] port link-type trunk [CE1-10GE1/0/1] port trunk allow-pass vlan 10 [CE1-10GE1/0/1] quit [CE1] interface vlanif 10 [CE1-Vlanif10] ip address 10.10.10.1 24 [CE1-Vlanif10] quit \# 配置CE2，要求CE2发送给PE2的报文带有一层VLAN Tag。
<HUAWEI> system-view [HUAWEI] sysname CE2 [CE2] vlan batch 10 [CE2] interface 10ge 1/0/1 [CE2-10GE1/0/1] port link-type trunk [CE2-10GE1/0/1] port trunk allow-pass vlan 10 [CE2-10GE1/0/1] quit [CE2] interface vlanif 10 [CE2-Vlanif10] ip address 10.10.10.2 24 [CE2-Vlanif10] quit \# 配置PE1。
<HUAWEI> system-view [HUAWEI] sysname PE1 [PE1] vlan batch 20 [PE1] interface 10ge 1/0/2 [PE1-10GE1/0/2] port link-type hybrid [PE1-10GE1/0/2] port hybrid pvid vlan 20 [PE1-10GE1/0/2] port hybrid tagged vlan 20 [PE1-10GE1/0/2] quit [PE1] interface vlanif 20 [PE1-Vlanif20] ip address 10.1.1.1 24 [PE1-Vlanif20] quit \# 配置P。
<HUAWEI> system-view [HUAWEI] sysname P [P] vlan batch 20 30 [P] interface 10ge 1/0/1 [P-10GE1/0/1] port link-type hybrid [P-10GE1/0/1] port hybrid pvid vlan 30 [P-10GE1/0/1] port hybrid tagged vlan 30 [P-10GE1/0/1] quit [P] interface 10ge 1/0/2 [P-10GE1/0/2] port link-type hybrid [P-10GE1/0/2] port hybrid pvid vlan 20 [P-10GE1/0/2] port hybrid tagged vlan 20 [P-10GE1/0/2] quit [P] interface vlanif 20 [P-Vlanif20] ip address 10.1.1.2 24 [P-Vlanif20] quit [P] interface vlanif 30 [P-Vlanif30] ip address 10.2.2.2 24 [P-Vlanif30] quit \# 配置PE2。
<HUAWEI> system-view [HUAWEI] sysname PE2 [PE2] vlan batch 30 [PE2] interface 10ge 1/0/1 [PE2-10GE1/0/1] port link-type hybrid

[PE2-10GE1/0/1] port hybrid pvid vlan 30 [PE2-10GE1/0/1] port hybrid tagged vlan 30 [PE2-10GE1/0/1] quit [PE2] interface vlanif 30 [PE2-Vlanif30] ip address 10.2.2.1 24 [PE2-Vlanif30] quit步骤2 在Device的接口上配置灵活QinQ和允许通过的VLAN。
\# 配置DeviceA。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan 10 [DeviceA-vlan10] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] port link-type hybrid [DeviceA-10GE1/0/2] port hybrid tagged vlan 10 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] port link-type hybrid [DeviceA-10GE1/0/1] port hybrid tagged vlan 10 [DeviceA-10GE1/0/1] quit \# 配置DeviceB。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan 100 [DeviceB-vlan100] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] port link-type hybrid [DeviceB-10GE1/0/2] port hybrid tagged vlan 100 [DeviceB-10GE1/0/2] quit [DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] port link-type hybrid [DeviceB-10GE1/0/1] port hybrid untagged vlan 100 [DeviceB-10GE1/0/1] port vlan-stacking vlan 10 stack-vlan 100 [DeviceB-10GE1/0/1] quit步骤3 在MPLS骨干网上配置IGP，本示例中使用OSPF。
配置OSPF时，注意需要发布PE1、P和PE2作为LSR ID的32位Loopback接口地址。
\# 配置PE1。
[PE1] router id 1.1.1.1 [PE1] interface loopback 1 [PE1-LoopBack1] ip address 1.1.1.1 32 [PE1-LoopBack1] quit [PE1] ospf 1 [PE1-ospf-1] area 0 [PE1-ospf-1-area-0.0.0.0] network 1.1.1.1 0.0.0.0 [PE1-ospf-1-area-0.0.0.0] network 10.1.1.1 0.0.0.255 [PE1-ospf-1-area-0.0.0.0] quit [PE1-ospf-1] quit \# 配置P。
[P] router id 2.2.2.2 [P] interface loopback 1 [P-LoopBack1] ip address 2.2.2.2 32 [P-LoopBack1] quit [P] ospf 1 [P-ospf-1] area 0 [P-ospf-1-area-0.0.0.0] network 2.2.2.2 0.0.0.0 [P-ospf-1-area-0.0.0.0] network 10.1.1.2 0.0.0.255 [P-ospf-1-area-0.0.0.0] network 10.2.2.2 0.0.0.255 [P-ospf-1-area-0.0.0.0] quit [P-ospf-1] quit \# 配置PE2。

[PE2] router id 3.3.3.3 [PE2] interface loopback 1 [PE2-LoopBack1] ip address 3.3.3.3 32 [PE2-LoopBack1] quit [PE2] ospf 1 [PE2-ospf-1] area 0 [PE2-ospf-1-area-0.0.0.0] network 3.3.3.3 0.0.0.0 [PE2-ospf-1-area-0.0.0.0] network 10.2.2.1 0.0.0.255 [PE2-ospf-1-area-0.0.0.0] quit [PE2-ospf-1] quit \# 配置完成后，PE1、P、PE2之间应能建立OSPF邻居关系，执行display ospf peer命令可以看到邻居状态为Full。执行display ip routing-table命令可以看到PE之间学习到对方的Loopback1接口路由。以PE1的显示为例：
[PE1] display ospf peer (M) Indicates MADJ neighbor OSPF Process 1 with Router ID 1.1.1.1 Area 0.0.0.0 interface 10.1.1.1(Vlanif20)'s neighbors Router ID : 2.2.2.2 Address: 10.1.1.2 State : Full Mode:Nbr is Master Priority: 1 DR : 10.1.1.2 BDR: 10.1.1.1 MTU: 0 Dead timer due (in seconds) : 30 Retrans timer interval : 5 Neighbor up time : 00h06m22s Neighbor up time stamp : 2024-08-03 10:32:05 Authentication Sequence : 0 [PE1] display ip routing-table Route Flags: R - relay, D - download to fib, T - to vpn-instance
------------------------------------------------------------------------------ Routing Tables: Public Destinations : 8 Routes : 8 Destination/Mask Proto Pre Cost Flags NextHop Interface
1.1.1.1/32 Direct 0 0 D 127.0.0.1 LoopBack1
2.2.2.2/32 OSPF 10 1 D 10.1.1.2 Vlanif20
3.3.3.3/32 OSPF 10 2 D 10.1.1.2 Vlanif20
10.1.1.0/24 Direct 0 0 D 10.1.1.1 Vlanif20
10.1.1.1/32 Direct 0 0 D 127.0.0.1 Vlanif20
10.2.2.0/24 OSPF 10 2 D 10.1.1.2 Vlanif20
127.0.0.0/8 Direct 0 0 D 127.0.0.1 InLoopBack0
127.0.0.1/32 Direct 0 0 D 127.0.0.1 InLoopBack0步骤4 在MPLS骨干网上配置MPLS基本能力和LDP。
\# 配置PE1。
[PE1] mpls lsr-id 1.1.1.1 [PE1] mpls [PE1-mpls] quit [PE1] mpls ldp [PE1-mpls-ldp] quit [PE1] interface vlanif 20 [PE1-Vlanif20] mpls [PE1-Vlanif20] mpls ldp [PE1-Vlanif20] quit \# 配置P。
[P] mpls lsr-id 2.2.2.2 [P] mpls [P-mpls] quit [P] mpls ldp [P-mpls-ldp] quit [P] interface vlanif 20 [P-Vlanif20] mpls

[P-Vlanif20] mpls ldp [P-Vlanif20] quit [P] interface vlanif 30 [P-Vlanif30] mpls [P-Vlanif30] mpls ldp [P-Vlanif30] quit \# 配置PE2。
[PE2] mpls lsr-id 3.3.3.3 [PE2] mpls [PE2-mpls] quit [PE2] mpls ldp [PE2-mpls-ldp] quit [PE2] interface vlanif 30 [PE2-Vlanif30] mpls [PE2-Vlanif30] mpls ldp [PE2-Vlanif30] quit步骤5 在PE之间建立远端LDP会话。
\# 配置PE1。
[PE1] mpls ldp remote-peer 3.3.3.3 [PE1-mpls-ldp-remote-3.3.3.3] remote-ip 3.3.3.3 [PE1-mpls-ldp-remote-3.3.3.3] quit \# 配置PE2。
[PE2] mpls ldp remote-peer 1.1.1.1 [PE2-mpls-ldp-remote-1.1.1.1] remote-ip 1.1.1.1 [PE2-mpls-ldp-remote-1.1.1.1] quit上述配置完成后，在PE1上执行display mpls ldp session命令查看LDP会话的建立情况，可以看到增加了与PE2的远端LDP会话。
以PE1的显示为例：
[PE1] display mpls ldp session LDP Session(s) in Public Network Codes: LAM(Label Advertisement Mode), SsnAge Unit(DDDD:HH:MM)
A '*' before a session means the session is being deleted.
------------------------------------------------------------------------------ PeerID Status LAM SsnRole SsnAge KASent/Rcv
------------------------------------------------------------------------------
2.2.2.2:0 Operational DU Passive 0000:15:29 3717/3717
3.3.3.3:0 Operational DU Passive 0000:00:00 2/2
------------------------------------------------------------------------------ TOTAL: 2 session(s) Found.
步骤6 在PE上使能MPLS L2VPN，并创建VC连接。
\# 配置 PE1 ：在接入 CE1 的接口 10GE1/0/1.1 上创建 VC 。
[PE1] mpls l2vpn [PE1-l2vpn] quit [PE1] vcmp role silent [PE1] interface 10ge 1/0/1 [PE1-10GE1/0/1] port link-type hybrid [PE1-10GE1/0/1] quit [PE1] interface 10ge 1/0/1.1 [PE1-10GE1/0/1.1] qinq stacking vid 10 pe-vid 100 [PE1-10GE1/0/1.1] mpls l2vc 3.3.3.3 101 [PE1-10GE1/0/1.1] quit \# 配置 PE2 ：在接入 CE2 的接口 10GE1/0/2.1 上创建 VC 。
[PE2] mpls l2vpn [PE2-l2vpn] quit [PE2] vcmp role silent

[PE2] interface 10ge 1/0/2 [PE2-10GE1/0/2] port link-type hybrid [PE2-10GE1/0/2] quit [PE2] interface 10ge 1/0/2.1 [PE2-10GE1/0/2.1] qinq termination pe-vid 100 ce-vid 10 [PE2-10GE1/0/2.1] mpls l2vc 1.1.1.1 101 [PE2-10GE1/0/2.1] quit
----结束检查配置结果在PE上查看L2VPN连接信息，可以看到建立了一条L2 VC，状态为UP。
以PE1的显示为例：
[PE1] display mpls l2vc interface 10ge 1/0/1.1
*client interface : 10GE1/0/1.1 is up Administrator PW : no session state : up AC status : up VC state : up Label state : 0 Token state : 0 VC ID : 101 VC type : VLAN destination : 3.3.3.3 local group ID : 0 remote group ID : 0 local VC label : 1038 remote VC label : 1038 local AC OAM State : up local PSN OAM State : up local forwarding state : forwarding local status code : 0x0 (forwarding)
remote AC OAM state : up remote PSN OAM state : up remote forwarding state: forwarding remote status code : 0x0 (forwarding)
remote interface : 10GE1/0/2.1 ignore standby state : no BFD for PW : unavailable VCCV State : up manual fault : not set active state : active forwarding entry : exist TTL Value : 1 link state : up local VC MTU : 1500 remote VC MTU : 1500 local VCCV : alert ttl lsp-ping bfd remote VCCV : alert ttl lsp-ping bfd local control word : disable remote control word : disable tunnel policy name : -- PW template name : -- primary or secondary : primary load balance type : flow Access-port : false Switchover Flag : false VC tunnel info : 1 tunnels NO.0 TNL type : ldp , TNL ID : 0x0000000001004ccb43 create time : 0 days, 0 hours, 4 minutes, 42 seconds up time : 0 days, 0 hours, 3 minutes, 6 seconds last change time : 0 days, 0 hours, 3 minutes, 6 seconds VC last up time : 2024/08/03 14:33:29 VC total up time : 0 days, 0 hours, 3 minutes, 6 seconds CKey : 385 NKey : 16777471 PW redundancy mode : frr AdminPw interface : -- AdminPw link state : -- Forward state : send active, receive active

Diffserv Mode : uniform Service Class : cs- Color : -- DomainId : - Domain Name : - CE1和CE2能够相互Ping通。
以CE1的显示为例：
[CE1] ping 10.10.10.2 PING 10.10.10.2: 56 data bytes, press CTRL_C to break Reply from 10.10.10.2: bytes=56 Sequence=1 ttl=255 time=31 ms Reply from 10.10.10.2: bytes=56 Sequence=2 ttl=255 time=10 ms Reply from 10.10.10.2: bytes=56 Sequence=3 ttl=255 time=5 ms Reply from 10.10.10.2: bytes=56 Sequence=4 ttl=255 time=2 ms Reply from 10.10.10.2: bytes=56 Sequence=5 ttl=255 time=28 ms
--- 10.10.10.2 ping statistics --- 5 packet(s) transmitted 5 packet(s) received
0.00% packet loss round-trip min/avg/max = 2/15/31 ms配置脚本
● CE1 \# sysname CE1 \# vlan batch 10 \# interface Vlanif10 ip address 10.10.10.1 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# return
● CE2 \# sysname CE2 \# vlan batch 10 \# interface Vlanif10 ip address 10.10.10.2 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# return
● DeviceA \# sysname DeviceA \# vlan batch 10 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 10 \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 10 \# return

● DeviceB
\#
sysname DeviceB
\#
vlan batch 100
\#
interface 10GE1/0/1
port link-type hybrid
port hybrid untagged vlan 100
port vlan-stacking vlan 10 stack-vlan 100
\#
interface 10GE1/0/2
port link-type hybrid
port hybrid tagged vlan 100
\#
return
● PE1
\#
sysname PE1
\#
router id 1.1.1.1
\#
vcmp role silent
\#
vlan batch 20
\#
mpls lsr-id 1.1.1.1
mpls
\#
mpls l2vpn
\#
mpls ldp
\#
mpls ldp remote-peer 3.3.3.3
remote-ip 3.3.3.3
\#
interface Vlanif20
ip address 10.1.1.1 255.255.255.0
mpls
mpls ldp
\#
interface 10GE1/0/1
port link-type hybrid
\#
interface 10GE1/0/1.1
qinq stacking vid 10 pe-vid 100
mpls l2vc 3.3.3.3 101
\#
interface 10GE1/0/2
port link-type hybrid
port hybrid pvid vlan 20
port hybrid tagged vlan 20
\#
interface LoopBack1
ip address 1.1.1.1 255.255.255.255
\#
ospf 1
area 0.0.0.0
network 1.1.1.1 0.0.0.0
network 10.1.1.0 0.0.0.255
\#
return
● P
\#
sysname P
\#
router id 2.2.2.2
\#

vlan batch 20 30 \# mpls lsr-id 2.2.2.2 mpls \# mpls ldp \# interface Vlanif20 ip address 10.1.1.2 255.255.255.0 mpls mpls ldp \# interface Vlanif30 ip address 10.2.2.2 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 30 port hybrid tagged vlan 30 \# interface 10GE1/0/2 port link-type hybrid port hybrid pvid vlan 20 port hybrid tagged vlan 20 \# interface LoopBack1 ip address 2.2.2.2 255.255.255.255 \# ospf 1 area 0.0.0.0 network 2.2.2.2 0.0.0.0 network 10.1.1.0 0.0.0.255 network 10.2.2.0 0.0.0.255 \# return
● PE2 \# sysname PE2 \# router id 3.3.3.3 \# vcmp role silent \# vlan batch 30 \# mpls lsr-id 3.3.3.3 mpls \# mpls l2vpn \# mpls ldp \# mpls ldp remote-peer 1.1.1.1 remote-ip 1.1.1.1 \# interface Vlanif30 ip address 10.2.2.1 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 30 port hybrid tagged vlan 30 \# interface 10GE1/0/2 port link-type hybrid

\# interface 10GE1/0/2.1 encapsulation qinq-termination qinq termination pe-vid 100 ce-vid 10 mpls l2vc 1.1.1.1 101 \# interface LoopBack1 ip address 3.3.3.3 255.255.255.255 \# ospf 1 area 0.0.0.0 network 3.3.3.3 0.0.0.0 network 10.2.2.0 0.0.0.255 \# return

#### 4.24.38 举例：配置QinQ Stacking子接口接入VPLS

组网需求如图4-60所示，PE1和PE2启动VPLS功能。CE1通过DeviceA连接PE1设备，CE2通过DeviceB连接PE2。CE1和CE2属于一个VPLS。采用LDP作为VPLS信令建立PW，配置VPLS ，实现 CE1 与 CE2 的互通。 DeviceA 对 CE1 上送报文的 VLAN Tag 不进行改变，转发到PE1。DeviceB的CE2侧接口配置灵活QinQ，对CE发送过来的报文打上运营商指定允许通过的外层VLAN Tag。DeviceA上送到PE1的报文带有单层VLAN Tag，而DeviceB上送到PE2的报文带有双层VLAN Tag，所以需要在PE1上配置QinQ Stacking子接口接入VPLS方式使CE1与CE2互通。
当Device连接多个CE时，对不同CE发送过来的不同的VLAN Tag报文打上相同的外层VLAN Tag，还可以达到节省公网VLAN数量的目的。
图 4-60 配置 QinQ Stacking 子接口接入 VPLS 组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。

配置思路采用如下的思路配置：
1. 在骨干网上配置路由协议实现互通。
2. 在DeviceA连接CE1的接口上配置允许VLAN通过。
3. 在DeviceB连接CE2的接口上配置灵活QinQ。
4. 在PE之间建立远端LDP会话。
5. PE间建立传输业务数据所使用的隧道。
6. PE上使能MPLS L2VPN。
7. 在PE上创建VSI，指定信令为LDP。
8. 在PE1连接DeviceA的接口上配置QinQ Stacking子接口接入VPLS。
9. 在PE2连接DeviceB的接口上配置QinQ子接口接入VPLS。
说明VCMP的角色是Client时，不能配置VLAN终结子接口。
操作步骤步骤1 按图4-60配置各接口所属的VLAN说明避免将PE上AC侧和PW侧的物理接口加入相同的VLAN中，否则可能引起环路。
\# 配置CE1，要求CE1发送给PE1的报文带有一层VLAN Tag。
<HUAWEI> system-view [HUAWEI] sysname CE1 [CE1] vlan batch 10 [CE1] interface 10ge 1/0/1 [CE1-10GE1/0/1] port link-type trunk [CE1-10GE1/0/1] port trunk allow-pass vlan 10 [CE1-10GE1/0/1] quit [CE1] interface vlanif 10 [CE1-Vlanif10] ip address 10.1.1.1 24 [CE1-Vlanif10] quit \# 配置CE2，要求CE2发送给PE2的报文带有一层VLAN Tag。
<HUAWEI> system-view [HUAWEI] sysname CE2 [CE2] vlan batch 10 [CE2] interface 10ge 1/0/1 [CE2-10GE1/0/1] port link-type trunk [CE2-10GE1/0/1] port trunk allow-pass vlan 10 [CE2-10GE1/0/1] quit [CE2] interface vlanif 10 [CE2-Vlanif10] ip address 10.1.1.2 24 [CE2-Vlanif10] quit \# 配置PE1。
<HUAWEI> system-view [HUAWEI] sysname PE1 [PE1] vlan batch 20 [PE1] interface 10ge 1/0/2 [PE1-10GE1/0/2] port link-type hybrid [PE1-10GE1/0/2] port hybrid pvid vlan 20 [PE1-10GE1/0/2] port hybrid tagged vlan 20 [PE1-10GE1/0/2] quit [PE1] interface vlanif 20

[PE1-Vlanif20] ip address 4.4.4.4 24 [PE1-Vlanif20] quit \# 配置P。
<HUAWEI> system-view [HUAWEI] sysname P [P] vlan batch 20 30 [P] interface 10ge 1/0/1 [P-10GE1/0/1] port link-type hybrid [P-10GE1/0/1] port hybrid pvid vlan 20 [P-10GE1/0/1] port hybrid tagged vlan 20 [P-10GE1/0/1] quit [P] interface 10ge 1/0/2 [P-10GE1/0/2] port link-type hybrid [P-10GE1/0/2] port hybrid pvid vlan 30 [P-10GE1/0/2] port hybrid tagged vlan 30 [P-10GE1/0/2] quit [P] interface vlanif 20 [P-Vlanif20] ip address 4.4.4.5 24 [P-Vlanif20] quit [P] interface vlanif 30 [P-Vlanif30] ip address 5.5.5.4 24 [P-Vlanif30] quit \# 配置PE2。
<HUAWEI> system-view [HUAWEI] sysname PE2 [PE2] vlan batch 30 [PE2] interface 10ge 1/0/1 [PE2-10GE1/0/1] port link-type hybrid [PE2-10GE1/0/1] port hybrid pvid vlan 30 [PE2-10GE1/0/1] port hybrid tagged vlan 30 [PE2-10GE1/0/1] quit [PE2] interface vlanif 30 [PE2-Vlanif30] ip address 5.5.5.5 24 [PE2-Vlanif30] quit步骤2 在Device的接口上配置灵活QinQ和允许通过的VLAN。
\# 配置DeviceA。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan 10 [DeviceA-vlan10] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] port link-type hybrid [DeviceA-10GE1/0/2] port hybrid tagged vlan 10 [DeviceA-10GE1/0/2] quit [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] port link-type hybrid [DeviceA-10GE1/0/1] port hybrid tagged vlan 10 [DeviceA-10GE1/0/1] quit \# 配置DeviceB。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan 100 [DeviceB-vlan100] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] port link-type hybrid [DeviceB-10GE1/0/2] port hybrid tagged vlan 100 [DeviceB-10GE1/0/2] quit [DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] port link-type hybrid [DeviceB-10GE1/0/1] port hybrid untagged vlan 100 [DeviceB-10GE1/0/1] port vlan-stacking vlan 10 stack-vlan 100 [DeviceB-10GE1/0/1] quit步骤3 在MPLS骨干网上配置IGP，本示例中使用OSPF。

配置OSPF时，注意需要发布PE1、P和PE2作为LSR ID的32位Loopback接口地址。
\# 配置PE1。
[PE1] router id 1.1.1.1 [PE1] interface loopback 1 [PE1-LoopBack1] ip address 1.1.1.1 32 [PE1-LoopBack1] quit [PE1] ospf 1 [PE1-ospf-1] area 0 [PE1-ospf-1-area-0.0.0.0] network 1.1.1.1 0.0.0.0 [PE1-ospf-1-area-0.0.0.0] network 4.4.4.4 0.0.0.255 [PE1-ospf-1-area-0.0.0.0] quit [PE1-ospf-1] quit \# 配置P。
[P] router id 2.2.2.2 [P] interface loopback 1 [P-LoopBack1] ip address 2.2.2.2 32 [P-LoopBack1] quit [P] ospf 1 [P-ospf-1] area 0 [P-ospf-1-area-0.0.0.0] network 2.2.2.2 0.0.0.0 [P-ospf-1-area-0.0.0.0] network 4.4.4.5 0.0.0.255 [P-ospf-1-area-0.0.0.0] network 5.5.5.4 0.0.0.255 [P-ospf-1-area-0.0.0.0] quit [P-ospf-1] quit \# 配置PE2。
[PE2] router id 3.3.3.3 [PE2] interface loopback 1 [PE2-LoopBack1] ip address 3.3.3.3 32 [PE2-LoopBack1] quit [PE2] ospf 1 [PE2-ospf-1] area 0 [PE2-ospf-1-area-0.0.0.0] network 3.3.3.3 0.0.0.0 [PE2-ospf-1-area-0.0.0.0] network 5.5.5.5 0.0.0.255 [PE2-ospf-1-area-0.0.0.0] quit [PE2-ospf-1] quit \# 配置完成后，PE1、P、PE2之间应能建立OSPF邻居关系，执行display ip routing- table命令可以看到PE之间学习到对方的Loopback1接口路由。以PE1的显示为例：
[PE1] display ip routing-table Route Flags: R - relay, D - download to fib, T - to vpn-instance
------------------------------------------------------------------------------ Routing Tables: Public Destinations : 8 Routes : 8 Destination/Mask Proto Pre Cost Flags NextHop Interface
1.1.1.1/32 Direct 0 0 D 127.0.0.1 LoopBack1
2.2.2.2/32 OSPF 10 1 D 4.4.4.5 Vlanif20
3.3.3.3/32 OSPF 10 2 D 4.4.4.5 Vlanif20
4.4.4.0/24 Direct 0 0 D 4.4.4.4 Vlanif20
4.4.4.4/32 Direct 0 0 D 127.0.0.1 Vlanif20
5.5.5.0/24 OSPF 10 2 D 4.4.4.5 Vlanif20
127.0.0.0/8 Direct 0 0 D 127.0.0.1 InLoopBack0
127.0.0.1/32 Direct 0 0 D 127.0.0.1 InLoopBack0步骤4 在MPLS骨干网上配置MPLS基本能力和LDP。
\# 配置 PE1 。
[PE1] mpls lsr-id 1.1.1.1 [PE1] mpls [PE1-mpls] quit

[PE1] mpls ldp [PE1-mpls-ldp] quit [PE1] interface vlanif 20 [PE1-Vlanif20] mpls [PE1-Vlanif20] mpls ldp [PE1-Vlanif20] quit \# 配置P。
[P] mpls lsr-id 2.2.2.2 [P] mpls [P-mpls] quit [P] mpls ldp [P-mpls-ldp] quit [P] interface vlanif 20 [P-Vlanif20] mpls [P-Vlanif20] mpls ldp [P-Vlanif20] quit [P] interface vlanif 30 [P-Vlanif30] mpls [P-Vlanif30] mpls ldp [P-Vlanif30] quit \# 配置PE2。
[PE2] mpls lsr-id 3.3.3.3 [PE2] mpls [PE2-mpls] quit [PE2] mpls ldp [PE2-mpls-ldp] quit [PE2] interface vlanif 30 [PE2-Vlanif30] mpls [PE2-Vlanif30] mpls ldp [PE2-Vlanif30] quit配置完成后在PE1、P和PE2上执行display mpls ldp session命令可以看到PE1和P之间或PE2和P之间的对等体的Status项为“Operational”，即对等体关系已建立。执行display mpls lsp命令可以看到LSP的建立情况。以PE1的显示为例：
[PE1] display mpls ldp session LDP Session(s) in Public Network Codes: LAM(Label Advertisement Mode), SsnAge Unit(DDDD:HH:MM)
A '*' before a session means the session is being deleted.
------------------------------------------------------------------------------ PeerID Status LAM SsnRole SsnAge KASent/Rcv
------------------------------------------------------------------------------
2.2.2.2:0 Operational DU Passive 0000:15:29 3717/3717
------------------------------------------------------------------------------ TOTAL: 1 session(s) Found.
步骤5 在PE之间建立远端LDP会话。
\# 配置 PE1 。
[PE1] mpls ldp remote-peer 3.3.3.3 [PE1-mpls-ldp-remote-3.3.3.3] remote-ip 3.3.3.3 [PE1-mpls-ldp-remote-3.3.3.3] quit \# 配置PE2。
[PE2] mpls ldp remote-peer 1.1.1.1 [PE2-mpls-ldp-remote-1.1.1.1] remote-ip 1.1.1.1 [PE2-mpls-ldp-remote-1.1.1.1] quit上述配置完成后，在PE1或PE2上执行display mpls ldp session命令可以看到PE1和PE2之间的对等体的Status项为“Operational”，即远端对等体关系已建立。
以PE1的显示为例：
[PE1] display mpls ldp session LDP Session(s) in Public Network

Codes: LAM(Label Advertisement Mode), SsnAge Unit(DDDD:HH:MM)
A '*' before a session means the session is being deleted.
------------------------------------------------------------------------------ PeerID Status LAM SsnRole SsnAge KASent/Rcv
------------------------------------------------------------------------------
2.2.2.2:0 Operational DU Passive 0000:15:29 3717/3717
3.3.3.3:0 Operational DU Passive 0000:00:00 2/2
------------------------------------------------------------------------------ TOTAL: 2 session(s) Found.
步骤6 在PE上使能MPLS L2VPN。
\# 配置PE1。
[PE1] mpls l2vpn [PE1-l2vpn] quit \# 配置PE2。
[PE2] mpls l2vpn [PE2-l2vpn] quit步骤7 在PE上配置VSI。
\# 配置 PE1 。
[PE1] vsi a2 static [PE1-vsi-a2] pwsignal ldp [PE1-vsi-a2-ldp] vsi-id 2 [PE1-vsi-a2-ldp] peer 3.3.3.3 [PE1-vsi-a2-ldp] quit [PE1-vsi-a2] quit \# 配置PE2。
[PE2] vsi a2 static [PE2-vsi-a2] pwsignal ldp [PE2-vsi-a2-ldp] vsi-id 2 [PE2-vsi-a2-ldp] peer 1.1.1.1 [PE2-vsi-a2-ldp] quit [PE2-vsi-a2] quit步骤8 在PE上配置VSI与接口的绑定。
\# 配置PE1。
[PE1] vcmp role silent [PE1] interface 10ge 1/0/1 [PE1-10GE1/0/1] port link-type hybrid [PE1-10GE1/0/1] quit [PE1] interface 10ge 1/0/1.1 [PE1-10GE1/0/1.1] qinq stacking vid 10 pe-vid 100 [PE1-10GE1/0/1.1] l2 binding vsi a2 [PE1-10GE1/0/1.1] quit \# 配置PE2。
[PE2] vcmp role silent [PE2] interface 10ge 1/0/2 [PE2-10GE1/0/2] port link-type hybrid [PE2-10GE1/0/2] quit [PE2] interface 10ge 1/0/2.1 [PE2-10GE1/0/2.1] qinq termination pe-vid 100 ce-vid 10 [PE2-10GE1/0/2.1] l2 binding vsi a2 [PE2-10GE1/0/2.1] quit
----结束

检查配置结果在PE上查看L2VPN连接信息，可以看到建立了一条L2 VC，状态为UP。
以PE1的显示为例：
[PE1] display vsi name a2 verbose
***VSI Name : a2 Work Mode : normal Administrator VSI : no Isolate Spoken : disable VSI Index : 4 PW Signaling : ldp Member Discovery Style : static PW MAC Learn Style : unqualify Encapsulation Type : vlan MTU : 1500 Diffserv Mode : uniform Service Class : cs- Color : -- DomainId : - Domain Name : - Ignore AcState : disable P2P VSI : disable Multicast Fast Switch : disable Create Time : 0 days, 0 hours, 3 minutes, 50 seconds VSI State : up Resource Status : -- VSI ID : 2
*Peer Router ID : 3.3.3.3 Negotiation-vc-id : 2 Encapsulation Type : vlan primary or secondary : primary ignore-standby-state : no VC Label : 1031 Peer Type : dynamic Session : up Tunnel ID : 0x0000000001004cab43 Broadcast Tunnel ID : -- Broad BackupTunnel ID : -- CKey : 193 NKey : 16777441 Stp Enable : 0 PwIndex : 193 Control Word : disable BFD for PW : unavailable Interface Name : 10GE1/0/1.1 State : up Ac Block State : unblocked Access Port : false Last Up Time : 2024/08/03 11:35:21 Total Up Time : 0 days, 0 hours, 3 minutes, 42 seconds
**PW Information:
*Peer Ip Address : 3.3.3.3 PW State : up Local VC Label : 1031 Remote VC Label : 1031 Remote Control Word : disable PW Type : label Local VCCV : alert lsp-ping bfd Remote VCCV : alert lsp-ping bfd Tunnel ID : 0x0000000001004cab43 Broadcast Tunnel ID : -- Broad BackupTunnel ID : -- Ckey : 193

Nkey : 16777441 Main PW Token : 0x0 Slave PW Token : 0x0 Tnl Type : ldp OutInterface : -- Backup OutInterface : -- Stp Enable : 0 Mac Flapping : 0 PW Last Up Time : 2024/08/03 11:36:54 PW Total Up Time : 0 days, 0 hours, 2 minutes, 9 seconds CE1和CE2能够相互Ping通。
以CE1的显示为例：
[CE1] ping 10.1.1.2 PING 10.1.1.2: 56 data bytes, press CTRL_C to break Reply from 10.1.1.2: bytes=56 Sequence=1 ttl=255 time=90 ms Reply from 10.1.1.2: bytes=56 Sequence=2 ttl=255 time=77 ms Reply from 10.1.1.2: bytes=56 Sequence=3 ttl=255 time=34 ms Reply from 10.1.1.2: bytes=56 Sequence=4 ttl=255 time=46 ms Reply from 10.1.1.2: bytes=56 Sequence=5 ttl=255 time=94 ms
--- 10.1.1.2 ping statistics --- 5 packet(s) transmitted 5 packet(s) received
0.00% packet loss round-trip min/avg/max = 34/68/94 ms配置脚本
● CE1 \# sysname CE1 \# vlan batch 10 \# interface Vlanif10 ip address 10.1.1.1 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# return
● CE2 \# sysname CE2 \# vlan batch 10 \# interface Vlanif10 ip address 10.1.1.2 255.255.255.0 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# return
● DeviceA \# sysname DeviceA \# vlan batch 10 \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 10

\# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 10 \# return
● DeviceB \# sysname DeviceB \# vlan batch 100 \# interface 10GE1/0/1 port link-type hybrid port hybrid untagged vlan 100 port vlan-stacking vlan 10 stack-vlan 100 \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 100 \# return
● PE1 \# sysname PE1 \# router id 1.1.1.1 \# vcmp role silent \# vlan batch 20 \# mpls lsr-id 1.1.1.1 mpls \# mpls l2vpn \# vsi a2 static pwsignal ldp vsi-id 2 peer 3.3.3.3 \# mpls ldp \# mpls ldp remote-peer 3.3.3.3 remote-ip 3.3.3.3 \# interface Vlanif20 ip address 4.4.4.4 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid \# interface 10GE1/0/1.1 qinq stacking vid 10 pe-vid 100 l2 binding vsi a2 \# interface 10GE1/0/2 port link-type hybrid port hybrid pvid vlan 20 port hybrid tagged vlan 20 \# interface LoopBack1 ip address 1.1.1.1 255.255.255.255 \# ospf 1

area 0.0.0.0 network 1.1.1.1 0.0.0.0 network 4.4.4.0 0.0.0.255 \# return
● P \# sysname P \# router id 2.2.2.2 \# vlan batch 20 30 \# mpls lsr-id 2.2.2.2 mpls \# mpls ldp \# interface Vlanif20 ip address 4.4.4.5 255.255.255.0 mpls mpls ldp \# interface Vlanif30 ip address 5.5.5.4 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 20 port hybrid tagged vlan 20 \# interface 10GE1/0/2 port link-type hybrid port hybrid pvid vlan 30 port hybrid tagged vlan 30 \# interface LoopBack1 ip address 2.2.2.2 255.255.255.255 \# ospf 1 area 0.0.0.0 network 2.2.2.2 0.0.0.0 network 4.4.4.0 0.0.0.255 network 5.5.5.0 0.0.0.255 \# return
● PE2 \# sysname PE2 \# router id 3.3.3.3 \# vcmp role silent \# vlan batch 30 \# mpls lsr-id 3.3.3.3 mpls \# mpls l2vpn \# vsi a2 static pwsignal ldp vsi-id 2 peer 1.1.1.1 \#

mpls ldp \# mpls ldp remote-peer 1.1.1.1 remote-ip 1.1.1.1 \# interface Vlanif30 ip address 5.5.5.5 255.255.255.0 mpls mpls ldp \# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 30 port hybrid tagged vlan 30 \# interface 10GE1/0/2 port link-type hybrid \# interface 10GE1/0/2.1 encapsulation qinq-termination qinq termination pe-vid 100 ce-vid 10 l2 binding vsi a2 \# interface LoopBack1 ip address 3.3.3.3 255.255.255.255 \# ospf 1 area 0.0.0.0 network 3.3.3.3 0.0.0.0 network 5.5.5.0 0.0.0.255 \# return

#### 4.24.39 举例：配置Voice VLAN（基于MAC地址识别语音报文，IP Phone上送Untagged语音报文）

组网需求如图4-61所示，DeviceA下行连接数据业务和语音业务，DeviceA使用VLAN2传输语音报文，使用VLAN3传输数据报文。IP Phone A和Host1串行接入DeviceA，IP Phone B单独接入DeviceA，IP Phone发送的都是untagged语音报文。用户希望提高语音报文的传输优先级以保证用户的通话质量。
图 4-61 配置基于 MAC 地址识别语音报文的 Voice VLAN 组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。

操作步骤步骤1 在DeviceA上创建VLAN并配置接口加入VLAN。
\# 创建VLAN。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 2 3 \# 配置接口加入VLAN。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type hybrid [DeviceA-10GE1/0/1] port hybrid pvid vlan 3 [DeviceA-10GE1/0/1] port hybrid untagged vlan 2 to 3 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type hybrid [DeviceA-10GE1/0/2] port hybrid untagged vlan 2 to 3 [DeviceA-10GE1/0/2] quit步骤 2 配置 Voice VLAN 的 OUI 。
[DeviceA] voice-vlan mac-address 00e0-fc12-3456 mask ffff-ff00-0000步骤3 在接口下使能Voice VLAN并配置基于MAC地址提升语音报文优先级。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] voice-vlan 2 enable include-untagged [DeviceA-10GE1/0/1] voice-vlan remark-mode mac-address [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] voice-vlan 2 enable include-untagged [DeviceA-10GE1/0/2] voice-vlan remark-mode mac-address [DeviceA-10GE1/0/2] quit
----结束检查配置结果执行命令display voice-vlan 2 status，查看Voice VLAN的配置是否正确。
[DeviceA] display voice-vlan 2 status Voice VLAN Configuration:
-------------------------------------------------------------------------- Voice VLAN ID : 2 Voice VLAN status : Enable Voice VLAN 8021p remark : 5 Voice VLAN dscp remark : 46
-------------------------------------------------------------------------- Port Information:
------------------------------------------------------------------------------ Port Add-Mode Security-Mode PribyVLAN Untag
------------------------------------------------------------------------------ 10GE1/0/1 Manual Normal Disable Enable 10GE1/0/2 Manual Normal Disable Enable配置脚本\# sysname DeviceA \# voice-vlan mac-address 00e0-fc12-3456 mask ffff-ff00-0000 \# vlan batch 2 to 3

\# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 3 port hybrid untagged vlan 2 to 3 voice-vlan 2 enable include-untagged voice-vlan remark-mode mac-address \# interface 10GE1/0/2 port link-type hybrid port hybrid untagged vlan 2 to 3 voice-vlan 2 enable include-untagged voice-vlan remark-mode mac-address \# return

#### 4.24.40 举例：配置Voice VLAN（基于VLAN识别语音报文，IP Phone上送Tagged语音报文）

组网需求如图4-62所示，DeviceA下行连接数据业务和语音业务，DeviceA使用VLAN2传输语音报文，使用 VLAN3 传输数据报文。 IP Phone A 和 Host1 串行接入 DeviceA ， IP Phone B单独接入DeviceA，IP Phone支持通过LLDP协议获取Voice VLAN信息，发送的是Tagged语音报文。用户希望提高语音报文的传输优先级以保证用户的通话质量。
图 4-62 配置基于 VLAN 识别语音报文的 Voice VLAN 组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
操作步骤步骤1 在DeviceA上创建VLAN并配置接口加入VLAN。
\# 创建VLAN。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan batch 2 3 \# 配置接口加入 VLAN 。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type hybrid

[DeviceA-10GE1/0/1] port hybrid pvid vlan 3 [DeviceA-10GE1/0/1] port hybrid untagged vlan 3 [DeviceA-10GE1/0/1] port hybrid tagged vlan 2 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type hybrid [DeviceA-10GE1/0/2] port hybrid tagged vlan 2 [DeviceA-10GE1/0/2] quit步骤2 使能LLDP。
[DeviceA] lldp enable步骤3 在接口下使能Voice VLAN并配置基于VLAN提升语音报文优先级。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] voice-vlan 2 enable [DeviceA-10GE1/0/1] voice-vlan remark-mode vlan [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] voice-vlan 2 enable [DeviceA-10GE1/0/2] voice-vlan remark-mode vlan [DeviceA-10GE1/0/2] quit
---- 结束检查配置结果执行命令display voice-vlan 2 status，查看Voice VLAN的配置是否正确。
[DeviceA] display voice-vlan 2 status Voice VLAN Configuration:
-------------------------------------------------------------------------- Voice VLAN ID : 2 Voice VLAN status : Enable Voice VLAN 8021p remark : 5 Voice VLAN dscp remark : 46
-------------------------------------------------------------------------- Port Information:
------------------------------------------------------------------------------ Port Add-Mode Security-Mode PribyVLAN Untag
------------------------------------------------------------------------------ 10GE1/0/1 Manual Normal Enable Disable 10GE1/0/2 Manual Normal Enable Disable配置脚本\# sysname DeviceA \# vlan batch 2 to 3 \# lldp enable \# interface 10GE1/0/1 port link-type hybrid port hybrid pvid vlan 3 port hybrid tagged vlan 2 port hybrid untagged vlan 3 voice-vlan 2 enable \# interface 10GE1/0/2 port link-type hybrid port hybrid tagged vlan 2 voice-vlan 2 enable \# return

#### 4.24.41 举例：配置VLAN内协议报文透传

组网需求如图4-63所示，同一VLAN内的多台设备与网络中的同一台服务器之间通过DeviceA同时通信时，DeviceA需要先对数据进行处理，将导致核心交换机处理能力下降，从而影响通信效果，也增加了通信成本。为了解决此问题，在DeviceA上使能VLAN协议报文透传功能后，指定VLAN内的数据到达DeviceA后直接被转发出去，而不上送CPU处理，从而提高了设备的运行性能、降低了通信成本、也减少了设备受到恶意数据攻击。
说明仅S6780-H、S6750-H、S6750-S、S6750E-S、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-S、S5732-H-V2系列支持该举例。
图 4-63 配置 VLAN 内协议报文透传组网图说明本例中interface1、interface2、interface3分别代表10GE1/0/1、10GE1/0/2、10GE1/0/3。
操作步骤步骤1 配置DeviceA。
\# 创建VLAN并使能VLAN协议透传功能。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] vlan 10 [DeviceA-vlan10] protocol-transparent [DeviceA-vlan10] quit

\# 配置接口加入VLAN。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] portswitch [DeviceA-10GE1/0/1] port link-type hybrid [DeviceA-10GE1/0/1] port hybrid tagged vlan 10 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] portswitch [DeviceA-10GE1/0/2] port link-type hybrid [DeviceA-10GE1/0/2] port hybrid tagged vlan 10 [DeviceA-10GE1/0/2] quit步骤2 配置DeviceB。
\# 配置下行口加入到VLAN10，上行口允许VLAN10通过<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] vlan 10 [DeviceB-vlan10] quit [DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] portswitch [DeviceB-10GE1/0/1] port link-type access [DeviceB-10GE1/0/1] port default vlan 10 [DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] portswitch [DeviceB-10GE1/0/2] port link-type access [DeviceB-10GE1/0/2] port default vlan 10 [DeviceB-10GE1/0/2] quit [DeviceB] interface 10ge 1/0/3 [DeviceB-10GE1/0/3] portswitch [DeviceB-10GE1/0/3] port link-type trunk [DeviceB-10GE1/0/3] port trunk allow-pass vlan 10 [DeviceB-10GE1/0/3] quit
----结束检查配置结果\# 配置完成后，进入DeviceA的VLAN10视图，执行命令display this，查看该VLAN已经使能了VLAN内协议报文透传功能。
[DeviceA] vlan 10 [DeviceA-vlan10] display this \# vlan 10 protocol-transparent \# return配置脚本\# DeviceA \# sysname DeviceA \# vlan 10 protocol-transparent \# interface 10GE1/0/1 port link-type hybrid port hybrid tagged vlan 10 \# interface 10GE1/0/2 port link-type hybrid

port hybrid tagged vlan 10 \# return \# DeviceB \# sysname DeviceB \# vlan batch 10 \# interface 10GE1/0/1 port link-type access port default vlan 10 \# interface 10GE1/0/2 port link-type access port default vlan 10 \# interface 10GE1/0/3 port link-type trunk port trunk allow-pass vlan 10 \# return

### 4.25 VLAN常见配置错误

#### 4.25.1 创建VLANIF接口失败

故障现象设备上出现错误提示信息，显示创建VLANIF接口失败。
可能的原因
● 创建的VLANIF接口数量已达到规格限制。
● 对应的VLAN不能用来创建VLANIF接口。
操作步骤
● 创建的VLANIF接口数量已达到规格限制。
a. 查看VLANIF接口的配置信息。
display interface brief通过回显信息中的“Interface”字段，查看VLANIF接口数量。
b. 统计VLANIF接口数量，判断是否已达到设备支持的VLANIF接口数量，不同设备支持的VLANIF接口数量不同，详见：接口基础配置注意事项。
c. 删除不再需要的VLANIF接口。
undo interface vlanif interface-number
● 对应的VLAN不能用来创建为VLANIF接口。
a. 查看VLAN类型。
display vlan summary
b. 指定其他 VLAN 作为 VLANIF 接口。
interface vlanif interface-number
----结束

#### 4.25.2 VLANIF接口的状态为Down

故障现象执行命令display interface vlanif [ interface-number ]，发现VLANIF接口的状态为Down。
可能的原因
● 接口与VLAN没有关联，即没有接口加入VLAN。
● 加入VLAN的各接口的物理状态全是Down。
● VLANIF接口下没有配置IP地址。
● VLANIF接口被Shutdown。
操作步骤
● 没有接口加入VLAN。
a. 查看 VLAN 的接口信息。
display vlan vlan-id [ verbose | to vlan-id2 ] port trunk pvid vlan vlan-id仅表示在Trunk接口上配置PVID，并没有将接口加入VLAN。port hybrid pvid vlan vlan-id仅表示在Hybrid接口上配置PVID，并没有将接口加入VLAN。
b. 将接口加入VLAN，具体操作参见“关联接口和VLAN”。
● 加入VLAN的各接口的物理状态全是Down。
排查加入VLAN的各接口Down的故障。只要有一个接口物理状态是Up，VLANIF接口状态就是Up。
● VLANIF接口下没有配置IP地址。
a. 查看VLANIF接口的IP地址信息。
display interface vlanif [ interface-number ]
b. 配置VLANIF接口的IP地址。
system-view interface vlanif vlan-id ip address ip-address { mask | mask-length } [ sub ]
● VLANIF接口被Shutdown。
查看 接口的状态。
a. VLANIF display interface vlanif [ interface-number ]
b. 开启VLANIF接口。
system-view interface vlanif interface-number undo shutdown
----结束

#### 4.25.3 同一VLAN内无法互通（同设备）

故障现象同设备下，同一VLAN内的用户无法互通。

可能的原因
● VLAN内需要互通的接口Down。
● VLAN内的用户不在同一网段。
● MAC地址表项不正确。
● VLAN相关配置不正确。
● 设备配置了端口隔离功能。
● 终端设备上配置了错误的静态ARP表项。
操作步骤
● VLAN内需要互通的接口是否Up。
a. 查看需要互通的接口的运行状态。
display interface interface-type interface-number
b. 如果接口的状态为Down，排查接口Down的故障。
● VLAN内的用户是否在同一网段。
检查同一 VLAN 内的用户，其 IP 地址是否在同一网段。如果不是在同一网段，需要重新进行配置。
● MAC地址表项是否正确。
a. 查看设备学习到MAC地址、MAC地址对应接口、所属VLAN是否正确。
display mac-address
b. 删除MAC地址表项，并使设备重新学习指定的MAC地址。
system-view undo mac-address all如果只有动态MAC地址不正确，则在用户视图下执行命令reset mac- address，清除动态MAC地址表项。
● VLAN相关配置是否正确。
请执行如下操作查看VLAN相关配置是否正确。

| 检查项 | 检查方法及处理建议 |
|---|---|
| 需要互通的接口所在的VLAN是否已经创建 | 在任意视图下执行命令display vlan vlan-id查看需要互通的接口所在的VLAN是否已经创建，如果未创建请在系统视图下执行命令vlan命令创建VLAN。 |
| 检查需要互通的接口是否加入 VLAN | 在任意视图下执行display vlan vlan-id查看需要互通的接口是否已经加入指定VLAN，如果未加入请将接口加入指定 VLAN，具体操作参见“关联接口和VLAN”。 |
| 接口和终端是否按照规划的对应关系进行连接 | 按照正确的对应关系将终端与设备接口进行连接。 |

● 设备是否配置了端口隔离。
a. 查看接口是否配置了端口隔离功能。
system-view
interface interface-type interface-number
display this

b. 关闭接口的端口隔离功能。
system-view
interface interface-type interface-number
portswitch
undo port-isolate enable [ group group-id ]
仅S6780-H、S6750-H、S6730-H-V2、S6730E-H-V2、S5755-H、S5755-
S、S6750-S、S6750E-S、S5732-H-V2系列支持通过portswitch命令将接口
从三层模式切换到二层模式。
● 查看终端设备上是否配置了错误的静态ARP表项，如果终端设备上配置了错误的
静态ARP表项，则用户自行修改。
----结束

#### 4.25.4 使用VLANIF接口的2台设备无法实现互通

故障现象如图4-64所示，在DeviceA的VLANIF2接口上配置IP地址，在DeviceB的VLANIF2接口上也配置相应的 IP 地址， 2 个 IP 地址属于同一网段，但是 DeviceA 和 DeviceB 无法 Ping通。
图 4-64 使用 VLANIF 接口的 2 台设备无法实现互通示意图可能的原因
● VLANIF接口处于Down状态。
● 设备互连的接口未加入VLAN。
● 设备互连的接口上配置PVID不一致。
操作步骤
● VLANIF接口是否Up。
a. 分别在DeviceA、DeviceB上查看VLANIF接口是否Up。
display interface vlanif [ vlan-id ]显示信息中的“current state”和“Line protocol current state”字段，只要其中一个字段为“DOWN”，则表示该VLANIF接口为Down。
b. 参考“4.25.2 VLANIF接口的状态为Down”，排查VLANIF接口状态为Down的故障。
● 设备互连的接口是否加入VLAN。
分别在DeviceA、DeviceB上查看是否有与对端互连的接口。
a.
display vlan vlan-id [ verbose | to vlan-id2 ]
b. 根据显示信息，进行相应的操作。
▪如果没有“Ports”字段，则将接口加入到VLAN，具体操作参见“关联接口和VLAN”。

▪如果有“Ports”字段，但两端接口加入VLAN方式不一致，即一端接口是Untagged方式加入VLAN（接口前显示“UT”），另一端是Tagged方式加入VLAN（接口前显示“TG”），则将接口加入VLAN的方式均修改为Tagged方式，具体操作参见“关联接口和VLAN”。
▪如果有“Ports”字段，但接口状态为Down（接口后显示“D”），则排查物理接口Down的故障。
● 设备互连的接口上配置PVID是否一致。
a. 分别在DeviceA、DeviceB上查看PVID信息。
display port vlan [ interface-type interface-number ] [ active ]
b. 修改PVID，保证interface1、interface2的PVID一致，具体操作参见“4.6 修改和恢复缺省VLAN”。
----结束
