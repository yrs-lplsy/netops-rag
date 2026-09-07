# S1700, S5700, S6700 V600R024C10 配置指南-以太网交换 01-06 VCMP配置

## 6 VCMP配置

6 VCMP 配置

### 6.1 VCMP简介

6.2 VCMP原理描述
6.3 VCMP配置注意事项
6.4 VCMP缺省配置
6.5 配置VCMP
6.6 维护VCMP
6.7 VCMP配置举例
6.1 VCMP 简介
定义
VCMP（VLAN Central Management Protocol，VLAN集中管理协议）是一个位于OSI
参考模型第二层的通信协议，它提供了一种在二层网络中传播VLAN配置信息，并自动
地在整个二层网络中保证VLAN配置信息一致的功能。
目的
通常情况下，设备上需要保持 VLAN 信息的同步，以保证所有设备都能进行正确的数据
转发。小型网络中，网络管理员可登录到每台设备上进行VLAN的配置和维护。但大型
网络中，设备很多，会有大量的VLAN信息需要配置和维护。如果仅靠网络管理员手工
操作，工作量很大，也不能保证配置的一致性。
为了解决上述问题，可通过VCMP实现VLAN的集中管理。这样，只需在一台设备上进
行创建、删除VLAN等操作，这些变更会自动通知到指定范围内的所有设备，从而使这
些设备无需手工操作即可实现VLAN的创建、删除等动作的同步，即减少了在多台设备
上修改同一个数据的工作量，也保证了修改的一致性。

说明
● VCMP只能帮助网络管理员同步VLAN配置，但不能帮助其动态地划分端口到VLAN。因此，VCMP一般需要与LNP结合使用，以最大程度简化用户配置。有关LNP的详细描述，请参见LNP基本原理。
● GVRP也可减少VLAN配置，且可将端口动态地划分到VLAN，但GVRP创建的VLAN是动态VLAN，而VCMP创建的VLAN是静态VLAN。
受益在二层网络中的设备上部署VCMP后：
● 可实现VLAN的集中管理和维护，减少网络维护成本。
● 可实现接入设备的即插即用。

### 6.2 VCMP原理描述

#### 6.2.1 基本概念

VCMP使用域来管理设备，这个域就称为VCMP管理域；并通过角色定义来确定设备的属性，称为VCMP的角色，VCMP共定义了Server、Client、Transparent和Silent四种角色。VCMP管理域及角色如图6-1所示。
图 6-1 VCMP 管理域及角色示意图VCMP 管理域如图6-1所示，VCMP管理域由一组域名相同的设备通过Trunk或Hybrid链路类型的接口互连构成。同一域内的每台设备都必须使用相同的域名，且一台设备只能加入一个VCMP管理域，不同域的设备间不能同步VLAN信息。

VCMP管理域确定了VCMP管理设备的范围，凡是加入域的角色为Client的设备，均会受到域内角色为Server的设备管理。在Server上创建、删除VLAN或修改VLAN名称、描述时，Client会自动同步修改，使其保存的VLAN信息与Server上的一致，从而减少在多台设备上重复修改同一个VLAN信息的工作量，也保证了修改的一致性。
域中只能有一台管理设备，但可以有多台被管理设备。
VCMP 的角色VCMP通过角色定义确定设备的属性，VCMP角色定义如表6-1所示。
表 6-1 VCMP 的角色

| VCMP的角色 | 定义及作用 | 说明 |
|---|---|---|
| Server | 作为VCMP管理域的管理角色，负责将VLAN信息通过 VCMP报文同步给同域的其它设备。 | Server上创建、删除VLAN和修改 VLAN名称、描述的信息会在全域内传播。 |
| Client | 作为VCMP管理域的被管理角色，属于某特定VCMP管理域，根据Server发过来的VCMP 报文将VLAN信息同步到本地。 | Client上创建、删除VLAN和修改 VLAN名称、描述的信息不会在域内传播，但会被Server发送的 VLAN信息覆盖。 |
| Transparent | 作为透传角色，不受VCMP的管理行为影响，也不影响 VCMP管理域中的其他设备。 | Transparent直接转发VCMP报文（仅向Trunk或Hybrid类型链路转发）。 Transparent上创建、删除VLAN和修改VLAN名称、描述的信息不受 Server影响，也不会在域内传播。这样可满足某些设备不希望受 VCMP管理，但需要转发VCMP报文的需求。 |
| Silent | 部署在VCMP管理域的边缘，不受VCMP的管理行为影响，也不影响VCMP管理域中的其他设备，可用来隔离VCMP管理域。 | Silent收到VCMP报文后直接丢弃，而不转发该报文。 Silent上创建、删除VLAN和修改 VLAN名称、描述的信息不受 Server影响，也不会在域内传播。 |

说明
● Transparent和Silent不属于任何VCMP管理域。
● VCMP管理域的边缘设备如果希望受VCMP的管理，也可设置为Client角色，但为防止本域的VCMP报文传输到其他域中，需要将连接其他域的接口去使能VCMP功能。

#### 6.2.2 实现机制

VCMP通过在各角色设备间交互VCMP报文实现VLAN的集中管理，VCMP报文只能在Trunk或Hybrid类型接口的VLAN 1上传输。Client通过设备ID识别Server，它从收到的第一个VCMP报文中获取并记录Server的设备ID，后续只同步该设备ID的Server的

VLAN信息。Client学习到Server的设备ID后，不再改变（除非其角色发生改变），而Server必须配置设备ID后，才可正常收发VCMP报文、行使VLAN集中管理职能。
VCMP为确保在各种场景下Server与Client的VLAN信息保持一致，定义了Summary- Advert、Subset-Advert和Advert-Request三种组播方式的报文。三种报文的作用及触发场景如表6-2所示。
表 6-2 VCMP 协议报文

| 报文类型 | 作用 | 触发场景 | 触发报文的角色 |
|---|---|---|---|
| Summary-Advert | Server通过该报文向VCMP管理域内的其他设备通告域名、设备ID、配置修订号以及VLAN 信息。 | ● Server每5分钟发一次 Summary- Advert报文，以确保Server与 Client上的 VLAN信息的实时同步，防止因传输丢包等原因导致的同步遗漏。 ● Server上的配置变更（包括创建/删除VLAN、 VCMP管理域名修改、设备ID修改、认证密码修改、Server设备重启等情况）。 ● 收到同域的 Client的Advert- Request报文。 | Server |

| 报文类型 | 作用 | 触发场景 | 触发报文的角色 |
|---|---|---|---|
| Subset-Advert | Server通过该报文向VCMP管理域内的其他设备通告非默认配置的VLAN 名称或VLAN描述。 | Server上存在非默认配置的VLAN名称或VLAN描述，且满足以下任一条件： ● Server上的配置变更（包括创建/删除VLAN、 VLAN名称/ VLAN描述修改、VCMP管理域名修改、设备 ID修改、认证密码修改等情况）。 ● 收到同域的 Client的Advert- Request报文。 Server发送Subset- Advert报文，以确保Server与Client 上的VLAN信息实时同步，防止因传输丢包等原因导致的同步遗漏。 | Server |
| Advert-Request | Client通过该报文主动请求同步 VLAN信息，以便及时同步，避免不必要的等待。 | ● 新插入一台 Client设备。 ● Client设备发生重启或接口 Up。 | Client |

其中，由Server发送的Summary-Advert和Subset-Advert报文会携带配置修订号。配置修订号用来确定Server发送的VLAN信息是否比当前的更新，Client使用它来判断是否需要同步 Server 的 VLAN 信息。它以 8 位十六进制数体现，高四位用来标识 VCMP 管理域或设备ID的变更，低四位用来标识VLAN的变更。只要Server有VLAN变更，配置修订号就会自动递增。而当VCMP管理域名或设备ID变更时，配置修订号的高四位会重新计算，低四位会清零。
Server 上配置变更的 VLAN 同步机制当Server上的配置变更（包括创建、删除VLAN、修改VLAN的名称、描述，VCMP管理域名、设备ID修改，以及Server重启等情况）时，Server会发送携带变更信息的Summary-Advert 和 Subset-Advert 报文，以通告 VCMP 管理域内的 Client 进行同步。
下面以在Server上创建VLAN 100为例，介绍Server上配置变更的同步原理。假设Server上的VLAN的名称、描述均为缺省情况，即无需发送Subset-Advert报文。

如图6-2所示，DeviceA设置为Server，DeviceB设置为Transparent，DeviceC、DeviceD和DeviceE设置为Client，DeviceF设置为Silent。
图 6-2 Server 上配置变更的同步原理图网络管理员在Server上创建VLAN 100后：
1. Server发送携带变更VLAN的Summary-Advert报文，以向邻居通告这个配置变更。
2. Transparent收到Summary-Advert报文后，直接转发这个VCMP报文。
3. Client收到Summary-Advert报文后：
– 如果Client上第一次收到该报文，则学习报文中携带的设备ID、配置修订号、VLAN信息。若本地Client的VCMP管理域名为空，则也会学习报文中携带的VCMP管理域名。
– 如果Client上不是第一次收到该报文，则进行如下处理：
i. 根据Client上配置的认证密码以及报文携带的VCMP管理域名、设备ID、配置修订号等字段对报文进行VCMP认证。认证通过才会进行下一步。
如果认证失败，则直接丢弃该报文。
ii. 将本地保存的VCMP管理域名、设备ID，分别与报文携带的进行比较。
两者均相同才会进入下一步。
iii. 比较本地配置修订号与报文携带的配置修订号：
○ 如果高四位不等，则Client根据Summary-Advert报文同步Server上的VLAN信息，并学习VCMP管理域名和设备ID。

○ 如果高四位相等但本地配置修订号的低4位小于等于Summary- Advert报文中的配置修订号的低4位，则Client仅同步Server上的VLAN信息。
iv. 将Summary-Advert报文转发给VCMP管理域的其他设备。
本例中，Client不是第一次收到Summary-Advert报文，并且Client发现本地与Summary-Advert报文中的配置修订号的高4位相等，但本地配置修订号的低4位小于等于Summary-Advert报文中的配置修订号的低4位，于是根据Summary- Advert报文同步Server上的VLAN信息，在本地创建VLAN 100。
Silent收到Summary-Advert报文，则直接丢弃该报文。
4.
说明
● 其他触发Summary-Advert报文的场景中，VLAN同步过程与此相同。
● 如果Server上存在非缺省配置的VLAN名称、描述，Server还会发送Subset-Advert报文。
● Client从Server同步VLAN信息后30分钟内，会自动生成一个名为vlan.dat的文件用于存储当前的VLAN信息，设备重启时会读取该文件获取重启前VLAN的信息。该文件不可以做修改、删除、覆盖等任何处理。只有在下面几种情况下，才会自动删除该文件：
● 通过命令 reset vcmp 清除 VCMP 的管理域信息。
● 通过命令vcmp role { server | silent | transparent } 修改设备的VCMP角色为非Client。
● 通过命令startup saved-configuration configuration-file配置新的配置文件，并且新配置文件的名称和当前配置文件的名称不一样。
● 执行reset saved-configuration命令，清除已经保存的配置文件。注意该操作会清除所有的配置信息。
新增或重启 Client 配置的 VLAN 同步机制为确保Server与Client上的VLAN信息的同步，Server每5分钟发送一次Summary- Advert报文，向全域通告VCMP管理域名、设备ID和配置修订号，Server还会发送Subset-Advert报文来通告发生变更的VLAN名称和VLAN描述。当新插入一台Client或Client重启时，为了及时获取Server上的VLAN配置信息，新Client和重启的Client会发送Advert-Request组播报文，请求Server的VLAN配置信息。下面介绍这种场景下的VLAN同步原理。假设Server上的VLAN的名称、描述均为缺省情况，即无需发送Subset-Advert报文。
如图6-3所示，DeviceA设置为Server，DeviceB设置为Transparent，DeviceC和DeviceE设置为Silent，DeviceD设置为Client，DeviceF为新插入的一台设备，作为Client。

图 6-3 新增 Client 的 VLAN 同步原理图在DeviceF上配置VCMP功能并指定角色为Client后，DeviceF即为一台新的Client：
1. 新Client向邻居发送Advert-Request报文，请求Server的VLAN配置。
2. Client收到新Client的Advert-Request报文后，向邻居转发该报文。
3. Transparent收到Advert-Request报文，继续向邻居转发该报文。
4. 如果：
– Server 收到 Advert-Request 报文 :
▪根据Server上配置的认证密码以及报文携带的VCMP管理域名、设备ID、配置修订号等字段对报文进行VCMP认证。认证通过才会进行下一步。
▪如果该Advert-Request报文中的管理域名或设备ID非空，但与Server上配置的管理域名或设备ID不相等，则丢弃该Advert-Request报文；否则，回复携带Server上VLAN信息的Summary-Advert报文。
– Silent收到Advert-Request报文，则直接丢弃该报文。
5. Client、Transparent、Silent、新Client收到Server回复的Summary-Advert报文后，如 Server 上配置变更的 VLAN 同步机制所述处理该报文。只不过本场景中，Client发现VCMP管理域名、设备ID和配置修订号跟Summary-Advert报文携带的相等，直接转发该报文；而新Client则会同步Server的VLAN信息，如果新Client没有配置VCMP管理域，还会学习Server的VCMP管理域名和设备ID。

说明Client重启或接口Up，也会触发Advert-Request报文，其VLAN同步过程与此类似。
如果Server上存在非缺省配置的VLAN名称、描述，Server还会发送Subset-Advert报文。
多 Server 告警机制VCMP管理域内只能有一台Server。为防止用户假冒Server攻击网络，Server在收到Summary-Advert报文后，会将报文中的VCMP管理域名、设备ID、源MAC地址与本地的进行匹配。如果VCMP管理域名和设备ID匹配，但报文中的源MAC地址与本地的系统MAC地址不同，则会向网管发送“多Server”事件告警。为了防止告警太多影响Server性能，VCMP抑制告警的发送次数，仅每30分钟向网管发送一次告警。
VCMP 认证机制未知设备加入VCMP管理域，可能会将其设备上的VLAN信息同步到域内，进而影响域内网络的稳定。为防止未知设备加入，使VCMP管理域更安全，可以为域中的Server和Client配置域认证密码。
如果 Server 或 Client 配置了域认证密码，则用该密码字符串（默认使用空字符串）作为Key值，对报文中的VCMP管理域名、设备ID等字段进行SHA-256摘要计算，并把得到的摘要信息随Summary-Advert报文、Subset-Advert报文或Advert-Request报文发送。域内每台Client在收到的Server的Summary-Advert或Subset-Advert报文时，则用本地配置的认证密码对报文中的VCMP管理域名、设备ID和配置修订号等字段进行SHA-256摘要计算，并把得到的摘要信息与报文中携带的摘要信息进行比较。如果匹配，则认证通过，进行后续VCMP处理；否则，丢弃该Summary-Advert或Subset- Advert报文。Server收到Client的Advert-Request报文时进行同样的认证处理。
如果未配置域密码，则直接认证通过。
说明
● 同一VCMP管理域中的Server和每台Client上配置的域密码必须相同。
● 为充分保证设备安全，请用户定期修改密码。

#### 6.2.3 应用场景

随着网络规模的不断扩大，网络内设备的数量越来越多，而这些设备的VLAN配置需要同步，以保证正确的数据转发。在这些设备上进行重复创建、删除VLAN等操作，既浪费时间，也容易出错。
为此，可以在网络中部署VCMP，并根据要管理的范围确定VCMP管理域，然后选择汇聚设备或核心设备作为VCMP的Server。这样，只需在汇聚或核心设备上创建、删除VLAN或修改VLAN的名称、描述，同域内的接入设备会同步修改，进而实现VLAN的集中管理，降低配置和维护的工作量。同时，如果VCMP管理域没有设置认证密码，插入一台空配置的设备时，Server会通知其同步VLAN配置，实现即插即用。
在网络中部署VCMP时，建议：
● 将网络中的汇聚设备或核心设备设置为Server。一个VCMP管理域只能有一个Server。
● 将网络中的接入设备设置为Client。
● 如果网络中某些设备不希望被Server管理，且在网络中的位置处于Server、Client之间，则可以将其设置为Transparent。

● 将网络中与其他网络互联的边界设备设置为Silent，以免影响互联的网络。
图 6-4 VCMP 应用场景组网图
如图6-4所示，某企业有部门A和部门B两个部门，分别属于不同二层网络，各部门规
模较大，需要配置和维护的VLAN信息很多。为了方便VLAN的配置和维护，可在部门A
和部门B内分别部署VCMP，管理域分别为VCMP1和VCMP2，并选择汇聚设备AGG1作
为VCMP1的Server，接入设备ACC1～ACC2作为VCMP1的Client，汇聚设备AGG2作为
VCMP2的Server，接入设备ACC3～ACC4作为VCMP2的Client。这样，网络管理员只
需分别在AGG1和AGG2上创建、删除VLAN或修改VLAN的名称、描述，ACC1～ACC2
和ACC3～ACC4会分别同步AGG1和AGG2上的VLAN信息，实现了VLAN的统一配置和
管理。
说明
由于VCMP报文只能在Trunk和Hybrid类型接口上传送，为免去手工设置链路类型的麻烦，部署
VCMP时，一般需要同时部署LNP动态协商链路类型，以自动协商出链路类型，最大程度简化用
户配置。有关LNP的详细描述请参见LNP基本原理。

### 6.3 VCMP配置注意事项

License 依赖VCMP无需License许可即可使用。

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
特性限制表 6-4 本特性的使用限制特性限制VCMP只能帮助网络管理员同步VLAN配置，但不能帮助其动态地划分端口到VLAN。在支持LNP的形态上可以与LNP结合使用，以最大程度简化用户配置。
VCMP报文只能在VLAN 1中传输，缺省情况下，所有接口均加入VLAN 1，为避免环路，部署 VCMP 的网络需要同时部署破环协议，比如 STP 等。部署 STP 后，被阻塞的端口无法接收和发送VCMP报文。

| 特性限制 |
|---|
| 一台交换机只能加入一个VCMP管理域。一个VCMP管理域只能有一个Server。 |
| 如果设置了认证密码，则Server与所有Client上的密码必须保持一致。 |
| 如果GVRP已使能，则VCMP的角色只能是Transparent或Silent，不允许切换到Client 或者Server；反之，当VCMP处于Client或者Server角色时，不允许使能GVRP功能。 |
| 角色为Client的设备不允许配置终结子接口。有关终结子接口的配置，请参见相应版本“逻辑接口配置”的“配置子接口”章节。 |
| 在Server上删除VLAN后，Client会通过VCMP协议同步删除VLAN，但VLAN下的配置不会同步删除。此时，配置文件中会产生vlan vlan-id configuration命令，其中 vlan-id为删除的VLAN的VLAN ID，VLAN下的配置也都移入该VLAN配置视图下。 |
| 使能NETCONF并配置callhome和endpoint后，不能再配置VCMP和LNP功能；配置 VCMP或LNP功能后，使能NETCONF并依次配置callhome和endpoint后，会联动删除VCMP和LNP功能。 |
| 如果Server上创建、删除的VLAN，在Client上为ERPS、SEP的控制VLAN，或者堆叠的保留VLAN，则Client不会创建和删除这些VLAN。 |

### 6.4 VCMP缺省配置

VCMP的缺省配置如表1所示。
表 6-5 VCMP 缺省配置

| 参数 | 缺省值 |
|---|---|
| VCMP管理域 | 未配置 |
| VCMP管理域的角色 | Silent |
| 设备ID | 未配置 |
| VCMP管理域的认证密码 | 未配置 |
| 接口的VCMP功能 | 使能 |

### 6.5 配置VCMP

#### 6.5.1 配置VCMP Server

前提条件在配置VCMP之前，需完成以下任务：
● 连接接口并配置接口的物理参数，使接口的物理层状态为Up。

#### 6.5.2 配置VCMP Client

● 配置接口的链路类型为Trunk或Hybrid，使接口能转发VCMP报文。
说明
● VCMP一般需要跟LNP功能结合使用，以自动协商出链路类型，简化用户配置。LNP具体配置
请参见基于接口划分VLAN（LNP动态协商链路类型）。
● 可以使用命令display lnp summary查看设备上是否配置LNP以及接口的链路类型。如果设
备上没有配置LNP，或者接口的链路类型不是Trunk或Hybrid类型，则可执行命令port link-
type { hybrid | trunk }手工配置接口的链路类型。
操作步骤
步骤1 进入系统视图。
system-view
步骤2 配置VCMP管理域中设备的角色为Server。
vcmp role server
缺省情况下，VCMP管理域中设备的角色是Silent。
步骤3 配置VCMP管理域。
vcmp domain domain-name
缺省情况下，设备上未创建VCMP管理域。
同一VCMP管理域内的每台设备都必须使用相同的域名。一台设备只能加入一个VCMP
管理域。
步骤4 为角色是Server的设备配置设备ID。
vcmp device-id device-name
缺省情况下，没有配置设备ID。
步骤5 （可选）配置VCMP管理域的认证密码。
vcmp authentication sha2-256 password password
缺省情况下，未配置VCMP管理域的认证密码，VCMP报文直接认证通过。
如果设置认证密码，则同一VCMP管理域内的Server及每台Client上必须设置一致的认
证密码。为充分保证设备安全，请用户定期修改密码。
说明
密码建议符合密码复杂度规则：大写、小写、数字、特殊字符中至少有2种，并且长度不能小于
8。
步骤6 （可选）打开VCMP告警开关。
snmp-agent trap enable feature-name vcmp
为防止用户仿冒Server攻击网络，可打开VCMP告警开关。这样，当收到仿冒Server的
VCMP报文后，会向网管发送“多Server”事件告警。
----结束
配置
6.5.2 VCMP Client
前提条件
在配置VCMP之前，需完成以下任务：

● 连接接口并配置接口的物理参数，使接口的物理层状态为Up。
● 配置接口的链路类型为Trunk或Hybrid，使接口能转发VCMP报文。
说明
● VCMP一般需要跟LNP功能结合使用，以自动协商出链路类型，简化用户配置。LNP具体配置
请参见基于接口划分VLAN（LNP动态协商链路类型）。
● 可以使用命令display lnp summary查看设备上是否配置LNP以及接口的链路类型。如果设
备上没有配置LNP，或者接口的链路类型不是Trunk或Hybrid类型，则可执行命令port link-
type { hybrid | trunk }手工配置接口的链路类型。
操作步骤
步骤1 进入系统视图。
system-view
步骤2 配置VCMP管理域中设备的角色为Client。
vcmp role client
缺省情况下，VCMP管理域中设备的角色是Silent。
步骤3 配置VCMP管理域。
vcmp domain domain-name
缺省情况下，设备上未创建VCMP管理域。
同一VCMP管理域内的每台设备都必须使用相同的域名。角色为Client的设备上如果没
有配置VCMP管理域，域名由学习到的第一个VCMP报文决定。
一台设备只能加入一个VCMP管理域。
步骤4 （可选）配置VCMP管理域的认证密码。
vcmp authentication sha2-256 password password
缺省情况下，未配置VCMP管理域的认证密码，VCMP报文直接认证通过。
如果设置认证密码，则同一VCMP管理域内的Server及每台Client上必须设置一致的认
证密码。为充分保证设备安全，请用户定期修改密码。
说明
密码建议符合密码复杂度规则：大写、小写、数字、特殊字符中至少有2种，并且长度不能小于
8。
----结束

#### 6.5.3 （可选）配置VCMP Transparent

前提条件在配置 VCMP 之前，需完成以下任务：
● 连接接口并配置接口的物理参数，使接口的物理层状态为Up。
● 配置接口的链路类型为Trunk或Hybrid，使接口能转发VCMP报文。

说明VCMP一般需要跟LNP功能结合使用，以自动协商出链路类型，简化用户配置。LNP具体配置
●请参见基于接口划分VLAN（LNP动态协商链路类型）。
● 可以使用命令display lnp summary查看设备上是否配置LNP以及接口的链路类型。如果设备上没有配置LNP，或者接口的链路类型不是Trunk或Hybrid类型，则可执行命令port link- type { hybrid | trunk }手工配置接口的链路类型。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置VCMP管理域中设备的角色为Transparent。
vcmp role transparent缺省情况下，VCMP管理域中设备的角色是Silent。
步骤3 进入需要使能VCMP功能的以太网接口视图。
interface interface-type interface-number VCMP只能在二层以太网接口上使能。
步骤4 （可选）基于接口使能VCMP功能。
undo vcmp disable缺省情况下，设备上所有接口的VCMP功能处于使能状态。
----结束

#### 6.5.4 （可选）配置VCMP Silent

前提条件在配置VCMP之前，需完成以下任务：
● 连接接口并配置接口的物理参数，使接口的物理层状态为Up。
● 配置接口的链路类型为Trunk或Hybrid，使接口能转发VCMP报文。
说明
● VCMP一般需要跟LNP功能结合使用，以自动协商出链路类型，简化用户配置。LNP具体配置请参见基于接口划分VLAN（LNP动态协商链路类型）。
● 可以使用命令display lnp summary查看设备上是否配置LNP以及接口的链路类型。如果设备上没有配置LNP，或者接口的链路类型不是Trunk或Hybrid类型，则可执行命令port link- type { hybrid | trunk }手工配置接口的链路类型。
操作步骤步骤1 进入系统视图。
system-view步骤 2 配置 VCMP 管理域中设备的角色为 Silent 。
vcmp role silent缺省情况下，VCMP管理域中设备的角色是Silent。

步骤3 进入需要使能VCMP功能的以太网接口视图。
interface interface-type interface-number VCMP只能在二层以太网接口上使能。
步骤4 （可选）基于接口使能VCMP功能。
undo vcmp disable缺省情况下，设备上所有接口的VCMP功能处于使能状态。
说明VCMP管理域的边缘设备如果希望受VCMP的管理，也可设置为Client角色，但为防止本域的VCMP报文传输到其他域中，需要在连接其他域的接口上执行命令vcmp disable去使能VCMP功能。
----结束

#### 6.5.5 检查配置结果

操作步骤
● 使用命令display vcmp { status | counters | track }，查看VCMP配置信息。
● 使用命令display vcmp interface brief，查看二层以太网接口的VCMP使能的状态。
----结束

### 6.6 维护VCMP

背景信息Client学习到VCMP管理域ID、设备ID后，不会再变更。而当VCMP管理域内更换Server时，Client需要重新学习这些VCMP信息，因此，必须在学习开始前清除Client上原有学习到的VCMP信息。
如果需要查看最近一段时间内角色为Client的设备上VLAN变化轨迹，需要先清除原有的VLAN变化轨迹。
须知清除VCMP运行信息后，以前的信息将无法恢复，请务必仔细确认。
操作步骤步骤1 在确认需要清除学习到的VCMP信息后，请在用户视图下执行命令reset vcmp counters，清除学习到的VCMP信息。
步骤 2 在确认需要清除原有的 VLAN 变化轨迹后，请在用户视图下执行命令 reset vcmp track，清除原有的VLAN变化轨迹。
----结束

### 6.7 VCMP配置举例

#### 6.7.1 举例：配置VCMP实现对二层网络中VLAN配置的集中管理

组网需求如图6-5所示，某企业分支网络为二层网络，AGG为其汇聚设备，ACC1～ACC3为接入设备，其中ACC1用来接入外来访客。企业分支规模越来越大，网络管理员需要在各设备上配置和维护大量的VLAN信息，工作量大而且容易出错。因此，管理员希望减少VLAN配置和维护的工作量，但外来访客接入分支网络的权限需要限制，管理员希望ACC1上的VLAN能独立配置和维护。
图 6-5 配置 VCMP 实现对二层网络中 VLAN 配置的集中管理组网图说明本例中 interface1 ， interface2 ， interface3 分别代表 10GE1/0/1 ， 10GE1/0/2 ， 10GE1/0/3 。
配置思路可在此网络中部署VCMP，将汇聚设备AGG设置为Server，接入设备ACC2～ACC3设置为Client，为使ACC1不受VCMP管理，将其设置为Silent。这样，只需在AGG上修改VLAN信息，该信息将自动发送到网络中的ACC1～ACC3上。ACC2～ACC3会自动同步AGG上的VLAN信息，而ACC1不受VCMP的影响，从而既减少了在多台设备上修改同一个 VLAN 信息的工作量，也保证了 ACC1 的 VLAN 独立性。
同时，为免去手工设置链路类型的麻烦，配置通过LNP自动协商链路类型。
采用如下的思路配置VCMP：

1. 配置LNP，实现链路类型自动协商，简化用户配置。
2. 指定各设备的角色，以确定VCMP管理范围、管理与被管理对象。
3. 在角色为Server和Client的设备上分别配置VCMP相关参数，包括认证密码、设备
ID等，以保证Server和Client间能安全通信和身份识别。
4. 使能VCMP，使VCMP功能生效。
操作步骤
步骤1 配置通过LNP自动协商链路类型。
缺省情况下，全局和接口上的LNP处于使能状态，此时所有接口通过LNP自协商链路类
型。
可以使用命令display lnp summary查看设备全局和接口上是否使能链路类型自协商
功能（分别关注显示信息的“Global LNP”和“link-type(C)”字段），并检查接口的
链路类型（关注显示信息的“link-type(N)”字段）：
● 如果全局或接口上没有使能链路类型自协商功能，可执行如下步骤进行配置：
\# 全局使能链路类型自协商功能。ACC1、ACC2和ACC3的配置与AGG类似，不再
赘述。
<HUAWEI> system-view
[HUAWEI] sysname AGG
[AGG] undo lnp disable
\# 接口下使能链路类型自协商功能。ACC1、ACC2和ACC3的配置与AGG类似，不
再赘述。
[AGG] interface 10GE 1/0/1
[AGG-10GE1/0/1] undo port negotiation disable
[AGG-10GE1/0/1] port link-type negotiation-desirable
[AGG-10GE1/0/1] quit
[AGG] interface 10GE 1/0/2
[AGG-10GE1/0/2] undo port negotiation disable
[AGG-10GE1/0/2] port link-type negotiation-desirable
[AGG-10GE1/0/2] quit
[AGG] interface 10GE 1/0/3
[AGG-10GE1/0/3] undo port negotiation disable
[AGG-10GE1/0/3] port link-type negotiation-desirable
[AGG-10GE1/0/3] quit
● 如果全局和接口上已使能链路类型自协商功能，但设备间连接接口的链路类型为
Access，为保证VCMP正常运行，可以执行命令port link-type { trunk | hybrid }
手工指定接口的链路类型。
步骤2 指定各设备的角色。
\# 配置AGG的角色为Server。
[AGG] vcmp role server
\# 配置ACC1的角色为Silent。
[ACC1] vcmp role silent
\# 配置ACC2的角色为Client。
[ACC2] vcmp role client
\# 配置 ACC3 的角色为 Client 。
[ACC3] vcmp role client
步骤3 在Server和Client上配置VCMP相关参数。

\# 在AGG上配置VCMP管理域、设备ID和认证密码。
[AGG] vcmp domain vd1 [AGG] vcmp device-id server [AGG] vcmp authentication sha2-256 password YsHs_02 \# 在ACC2上配置VCMP管理域和认证密码。
[ACC2] vcmp domain vd1 [ACC2] vcmp authentication sha2-256 password YsHs_02 \# 在ACC3上配置VCMP管理域和认证密码。
[ACC3] vcmp domain vd1 [ACC3] vcmp authentication sha2-256 password YsHs_02步骤4 使能VCMP功能。
缺省情况下，接口上的VCMP功能已使能，无需再使能。但为避免VCMP报文影响PC终端，可在Client连接PC终端的接口上去使能VCMP功能。
\# 配置ACC2。
[ACC2] interface 10GE 1/0/2 [ACC2-10GE1/0/2] vcmp disable [ACC2-10GE1/0/2] quit \# 配置ACC3。
[ACC3] interface 10GE 1/0/2 [ACC3-10GE1/0/2] vcmp disable [ACC3-10GE1/0/2] quit
----结束检查配置结果配置完成后，执行display vcmp status命令可以查看VCMP配置信息，包括VCMP管理域域名、设备角色、设备ID、配置修订号和域密码。
以AGG显示为例：
[AGG] display vcmp status VCMP information:
Domain : vd1 Role : Server Server ID : server Configuration Revision : 0x239c0000 Password : ******在AGG上通过命令vlan vlan-id创建VLAN10，分别在ACC1～ACC3上执行命令display vlan summary 可以看到 ACC2 和 ACC3 同步了 AGG 上 VLAN 信息，而 ACC1 上没有同步AGG上的VLAN信息：
[AGG] vlan 10 [AGG-vlan10] quit [AGG] display vlan summary Static VLAN:
Total 2 static VLAN.
1 10 Dynamic VLAN:
Total 0 dynamic VLAN.
Reserved VLAN:
Total 0 reserved VLAN.
[ACC1] display vlan summary Static VLAN:
Total 1 static VLAN.

Dynamic VLAN:
Total 0 dynamic VLAN.
Reserved VLAN:
Total 0 reserved VLAN.
[ACC2] display vlan summary Static VLAN:
Total 2 static VLAN.
1 10 Dynamic VLAN:
Total 0 dynamic VLAN.
Reserved VLAN:
Total 0 reserved VLAN.
[ACC3] display vlan summary Static VLAN:
Total 2 static VLAN.
1 10 Dynamic VLAN:
Total 0 dynamic VLAN.
Reserved VLAN:
Total 0 reserved VLAN.
配置脚本
● AGG的配置文件\# sysname AGG \# vcmp role server vcmp domain vd1 vcmp device-id server vcmp authentication sha2-256 password %^%#6dD+>}ffA7[j2#]0%%GfN#;I}#.lQ2Yfb2b1y"0%^%# \# return
● ACC1的配置文件\# sysname ACC1 \# vcmp role silent \# return
● ACC2的配置文件\# sysname ACC2 \# vcmp role client vcmp domain vd1 vcmp authentication sha2-256 password %^%#6dD+>}ffA7[j2#]0%%GfN#;I}#.lQ2Yfb2b1y"0%^%# \# interface 10GE1/0/2 vcmp disable \# return
● ACC3的配置文件\# sysname ACC3 \# vcmp role client vcmp domain vd1

vcmp authentication sha2-256 password %^%#6dD+>}ffA7*[j2#]0%%GfN#;I}#.lQ2Yfb2b1y"0%^%# \# interface 10GE1/0/2 vcmp disable \# return
