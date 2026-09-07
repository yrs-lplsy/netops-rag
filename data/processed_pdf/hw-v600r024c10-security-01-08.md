# S1700, S5700, S6700 V600R024C10 配置指南-安全 01-08 MACsec配置

## 8 MACsec配置

### 8.1 MACsec简介

8.2 MACsec原理描述
8.3 MACsec应用场景
8.4 MACsec配置注意事项
8.5 MACsec缺省配置
8.6 启用MACsec功能
8.7 调整MACsec参数
8.8 检查配置结果
8.9 维护MACsec
8.10 MACsec配置举例
8.1 MACsec 简介
定义
MACsec （ Media Access Control Security ）是基于 802.1AE 和 802.1X 协议的安全通信
方法，可为以太网链路提供设备到设备的安全保护。它通过数据加密、完整性校验、
重播保护等功能为用户提供安全的MAC层数据发送和接收服务，保证以太网数据帧的
安全性。
目的
数据以明文形式传输存在许多安全隐患，比如：银行账户信息被窃取和篡改，遭受恶
意网络攻击等。MACsec采用二层加密技术，提供逐跳设备的数据安全传输，通过保护
传输的以太网数据帧，降低信息泄露和遭受恶意网络攻击的风险，适用于对数据机密
性要求较高的场合。

### 8.2 MACsec原理描述

MACsec应用在点对点组网的环境中，即从一台设备的接口到另一台设备的接口的组网。本端和对端之间使用安全密钥对数据报文进行加密和解密，密钥的协商以及安全通道的建立和管理由MKA（MACsec Key Agreement）协议负责。MKA协议定义了复杂的密钥生成体系，确保MACsec数据传输的安全性。其中，CAK（secure Connectivity Association Key）是用户在设备上配置的密钥，不直接用于数据报文的加密，而是由它和其他参数派生出用于数据加密的SAK（Secure Association Key）。
MACsec密钥派生关系可参考MACsec密钥体系。
MACsec 运行机制设备到设备的MACsec交互过程主要分为三个阶段：会话协商、安全通信和会话保活。
图 8-1 MACsec 的交互过程
1. 会话协商在两端设备的接口上开启MACsec功能，并配置相同的CAK后，两端设备会通过MKA 协议选举出密钥服务器（ Key Server ），密钥服务器根据 CAK 生成用于加密数据报文的SAK，分发给对端设备。
安全通信
2.
发送方使用SAK加密数据报文，接收方使用SAK解密数据报文。两端设备既可以作为发送方，也可以作为接收方，通信过程都受到MACsec保护。
3. 会话保活MKA协议定义了一个MKA会话保活定时器，用于规定MKA会话的超时时间。
MKA会话协商成功后，两端设备会通过交互MKA协议报文确认连接的存在。设备收到对端的MKA协议报文后，启动定时器。
– 如果在该超时时间内收到对端的MKA协议报文，则重启定时器。
– 如果在该超时时间内未收到对端的MKA协议报文，则认为该连接已不安全，删除建立的会话，重新进行MKA协商。

MACsec 密钥体系在两端设备配置相同的CAK，由密钥服务器生成SAK分发给对端设备的过程如图8-2所示，其中涉及的概念如下：
● CAK（secure Connectivity Association Key，安全连接关联密钥）：必须在两端设备的接口上配置相同的CAK，它不直接用于数据报文的加密，而是由它和CKN派生出用于数据加密的SAK。
● CKN（secure Connectivity Association Key Name，安全连接关联密钥名称）：
CAK的名称，必须在两端设备的接口上配置相同的CKN。
● SAK（Secure Association Key，安全关联密钥）：由密钥服务器根据CAK和CKN生成，用于数据报文的加密和解密。
● KEK（Key Encrypting Key，密钥加密密钥）：两端设备根据相同的CAK和CKN生成相同的KEK，用于SAK的加解密，防止在发布SAK的传输过程中泄密。
ICV（Integrity Value，完整性校验值）：发送端根据报文计算生成ICV放
● Check在报文尾部，报文接收端使用相同的算法计算得到ICV与报文携带的ICV进行比对。如果这两个ICV相同，说明报文没有被修改，校验通过；否则认为报文被修改，丢弃该报文。
● ICK （ ICV Key ，完整性校验密钥）：两端设备根据相同的 CAK 和 CKN 生成相同的ICK，用于计算MKA协议报文的ICV。仅MKA协议报文的ICV计算需要使用ICK，数据报文的ICV计算不需要使用ICK。
图 8-2 MACsec 密钥派生关系图设备生成和安装SAK的密钥流程如下：
1. 两端设备上配置相同的CAK和CKN，生成其他密钥。
– 密钥服务器：根据CAK和CKN生成SAK、KEK、ICK，并在本地安装SAK，用于数据报文的加解密。
– 对端设备：根据CAK和CKN生成KEK、ICK，由于对端设备的CAK和CKN与密钥服务器相同，所以对端设备生成的KEK和ICK也与密钥服务器相同。
2. 密钥服务器通过MKA协议报文将SAK发送给对端设备。
– 密钥服务器使用KEK加密SAK。
– 密钥服务器同时根据ICK生成ICV放在MKA协议报文尾部用于校验报文的完整性。

– 密钥服务器将加密后的SAK通过MKA协议报文发送给对端设备。
3. 对端设备接收MKA协议报文，并安装SAK。
– 对端设备接收MKA协议报文，根据报文中的CKN在本端查找匹配的CAK和
ICK。如果匹配成功，则继续进行下一步操作。
– 对端设备根据ICK计算得到ICV，如果与报文中携带的ICV不相同，则认为报文
被修改；如果相同，则认为报文完整，继续进行下一步操作。
– 对端设备使用KEK解密出SAK，并在本地安装SAK用于数据报文的加解密。

### 8.3 MACsec应用场景

园区内设备跨楼栋互联，链路暴露在公共区域，多园区设备跨区域互联，基于运营商网络通信传输，数据可能经过多个节点，裸露在外的网络设备互联线容易被嫁接中间非法设备，用于镜像监听，窃取数据。MACsec 提供了基于物理层的链路加密，保证数据在网络设备间传输的安全性。
如图8-3所示，支持网络设备（交换机、AR）之间的MACsec加密；并且，当存在中间设备时，中间设备配置二层协议透明传输 MKA 报文后， MACsec 支持跨设备对接。
图 8-3 MACsec 应用场景

### 8.4 MACsec配置注意事项

License 依赖MACsec无需License许可即可使用。
硬件依赖表 8-1 支持本特性的硬件

| 系列 | 支持产品 |
|---|---|
| S6750-H | S6750-H36C，S6750-H48Y8C |

| 系列 | 支持产品 |
|---|---|
| S5755-H | S5755-H24HB2Y2CZ，S5755-H24N4Y-A，S5755- H24P4Y2CZ，S5755-H24T4Y2CZ，S5755- H24U4Y2CZ，S5755-H24UM4Y2CZ，S5755- H24UN4Y2CZ，S5755-H24UTM4X4Y2C，S5755- H48N4Y-A，S5755-H48P4Y2CZ，S5755- H48T4Y2CZ，S5755-H48T4Y2CZ-B，S5755- H48U4Y2CZ，S5755-H48UM4Y2CZ，S5755- H48UN4Y2CZ，S5755-H48UTM4X4Y2C |
| S6780-H | S6780-H4Z |
| S5735E-L-V2 | S5735E-L16LP2UM2X-QA-V2，S5735E-L16LP2X- QA-V2 |
| S5755-S | S5755-S24P8J8YZ，S5755-S24P8Y，S5755- S24T8J8YZ，S5755-S24T8Y，S5755-S24U8J8YZ， S5755-S24U8Y，S5755-S48P8Y，S5755- S48P8YZ，S5755-S48T8Y，S5755-S48T8YZ， S5755-S48U8Y，S5755-S48U8YZ |
| S5735R-L-V2 | S5735R-L16LP2S-QA-V2，S5735R-L16LP2UM2X- QA-V2，S5735R-L16LP2X-QA-V2 |
| S6750E-S | S6750E-S16X10Y2CZ，S6750E-S24T16X8Y2CZ |
| S5735-L-V2 | S5735-L14P2S-QA-V2，S5735-L16LP2UM2X-QA- V2，S5735-L16LP2X-QA-V2，S5735-L16P2UM2X- QA-V2 |
| S5735I-S-V2 | S5735I-S16T2S4XN-V2，S5735I-S8T8P2S4XN-V2 |
| S5732-H-V2 | S5732-H24S4X6QZ-TV2，S5732-H24S4X6QZ- V2，S5732-H24UM4Y2CZ-KV2，S5732- H24UM4Y2CZ-V2，S5732-H44S4X6QZ-V2， S5732-H48UM4Y2CZ-KV2，S5732-H48UM4Y2CZ- TV2，S5732-H48UM4Y2CZ-V2 |
| S6730-H-V2 | S6730-H28X6CZ-V2，S6730-H48X6CZ-V2 |
| S6750-S | S6750-S16X10Y2CZ，S6750-S16X8YZ，S6750- S24T16X8Y2CZ |

查询工具如需了解硬件规格、产品部件的配套关系，请点击硬件中心进行查询；如需了解关键规格、全量软件规格，请点击规格查询进行查询。
MACsec 注意事项
● 需要对端设备也支持 MACsec 功能。
● V600R024C00及之前版本基础软件包中默认不支持该特性，如需使用，请登录华为技术支持网站，在软件下载专区中搜索对应产品和版本，下载MACsec特性包和对应的使用手册。

● 对于V600R024C10之前的版本，如果已安装独MACsec独立特性包，升级到
V600R024C10及之后的版本前，需要先执行reset feature-software next-
startup product_version_MACSEC.ccx命令清除下次启动特性包（可以使用
display startup feature-software命令查询正在使用的特性包），再执行
startup system-software XX_VxxRxxCxxSPCxx.cc命令配置设备下次启动时使用
的系统软件包。
● V600R024C10及以后版本基础软件包中默认支持该特性。当基础软件包需要降级
到V600R024C00及之前版本时，若设备已配置MACsec功能，需要使用命令
startup system-software product_version.cc feature-software
product_version_MACSEC.ccx同时配置设备下次启动时使用的系统软件包和
MACsec特性包。
● 组建堆叠时，若要使用MACsec功能，V600R024C00及之前版本的所有堆叠成员
设备均需安装MACsec特性包。堆叠后，原来不支持MACsec的端口仍不支持
MACsec，原来支持MACsec的端口仍支持MACsec。
● MACec支持能力取决于接口，与所插入的光模块型号无关。具体的接口支持范
围，详见“特性限制”表“MACsec的端口范围”。
表 8-2 MACSec 接口支持情况

| 产品 | 支持MACsec功能的接口 |
|---|---|
| S5751-L、S5731I-L系列远端模块 | 所有接口，每台远端模块最大同时支持 16个端口。配置步骤请参考《智能极简园区网络配置（小行星方案）》-《配置远端模块 MACsec功能》。 |
| S5751R-L | 所有接口，最大同时支持16个端口。 S5751R-L系列交换机仅支持通过Web网管进行配置，相关操作请参见《CloudEngine S5751R V600R024C10 产品文档》。 |
| S5732-H24S4X6QZ-V2/S5732- H24S4X6QZ-TV2 | ● HSIC-X08S000插卡上的接口。 ● HSIC-Y08S000插卡上的接口。 ● 面板上的GE接口1~24，40GE接口 5~6，10GE接口1~4。 |
| S5732-H24UM4Y2CZ-KV2/S5732- H24UM4Y2CZ-V2/S5732- H48UM4Y2CZ-KV2/S5732- H48UM4Y2CZ-V2/S5732- H48UM4Y2CZ-TV2 | ● S7X08000插卡上的接口。 ● S7C02000插卡上的接口。 ● 面板上的所有MultiGE接口。 |
| S5732-H44S4X6QZ-V2 | ● HSIC-X08S000插卡上的接口。 ● HSIC-Y08S000插卡上的接口。 ● 面板上的GE接口1~44，40GE接口 5~6，10GE接口1~4。 |

| 产品 | 支持MACsec功能的接口 |
|---|---|
| S6750-H36C | 面板上的100G端口1~16，25~36。存在互斥关系：100GE端口1~4与35~36 互斥，100GE端口5~8与33~34互斥， 100GE端口9~12与29~32互斥，100GE 端口13~16与25~28互斥。默认100G端口1~16支持。 |
| S6750-H48Y8C | 面板上的25GE端口1~32，100GE端口 1~8。存在互斥关系：25GE端口1~8与100GE 端口7~8互斥，25GE端口9~16与100GE 端口5~6互斥，25GE端口17~24与100GE 端口3~4互斥，25GE端口25~32与100GE 端口1~2互斥。默认25GE端口1~24，100GE端口1~2支持。 |
| S5755-H24HB2Y2CZ/S5755- H24P4Y2CZ/S5755-H24T4Y2CZ/S5755- H24U4Y2CZ/S5755-H24UM4Y2CZ/ S5755-H24UN4Y2CZ/S5755- H48P4Y2CZ/S5755-H48T4Y2CZ/S5755- H48T4Y2CZ-B/S5755-H48U4Y2CZ/ S5755-H48UN4Y2CZ/S5755- H48UM4Y2CZ | ● HSIC-X08S000插卡上的接口。 ● HSIC-Y08S000插卡上的接口。 ● 面板上的所有接口。 |
| S5755-H24N4Y-A/S5755- H24UTM4X4Y2C/S5755-H48N4Y-A/ S5755-H48UTM4X4Y2C | 面板上的所有接口。 |

| 产品 | 支持MACsec功能的接口 |
|---|---|
| S6780-H | ● XSIC-C10H000插卡上的接口：A模式下：所有槽位的40GE/100GE接口 1~2，9~10支持。B模式下：槽位1的 40GE/100GE接口1~2，9~10支持，槽位3的全端口支持。 ● XSIC-C16H000插卡上的接口：A模式下：所有槽位的40GE/100GE接口1~6 支持。B模式下：槽位1的40GE/ 100GE接口1~6支持，槽位3的全端口支持。 ● XSIC-D12B000插卡上的接口：A模式下：所有槽位的400GE接口1~2支持。 B模式下：槽位1的400GE接口 1~2支持，槽位3的全端口支持。 ● XSIC-L16Q000插卡上的接口：A模式下：所有槽位的40GE接口1~6支持。 B模式下：槽位1的40GE接口1~6支持，槽位3的全端口支持。 ● XSIC-Y26B000、XSIC-X26B000、 XSIC-M26B000插卡上的接口：A模式下：所有槽位的40GE/100GE接口1~2 支持。 B模式下：槽位1的40GE/ 100GE接口1~2支持，槽位3的全端口支持。 |
| S5735-L16LP2UM2X-QA-V2/S5735- L16P2UM2X-QA-V2/S5735R- L16LP2UM2X-QA-V2/S5735E- L16LP2UM2X-QA-V2 | 面板上的16*GE电口+ 2*MultiGE口。 |
| S5735-L14P2S-QA-V2 | 面板上的14*GE电口，2*GE光口 |
| S5735-L16LP2X-QA-V2/S5735R- L16LP2S-QA-V2/S5735R-L16LP2X-QA- V2/S5735E-L16LP2X-QA-V2 | 面板上的16*GE电口。 |
| S5735I-S16T2S4XN-V2/S5735I- S8T8P2S4XN-V2 | 面板上的接口： M0模式：GE电接口9~16，GE光接口 17~18 M1模式：GE电接口9~12，10GE光接口 5~6 |
| S6730-H28X6CZ-V2 | ● 面板上的10GE接口1~28，40GE/ 100GE接口5~6及其拆分接口。 ● HSIC-X08S000插卡上的接口。 ● HSIC-Y08S000插卡上的接口。 |

| 产品 | 支持MACsec功能的接口 |
|---|---|
| S6730-H48X6CZ-V2 | ● 面板上的10GE接口1~48，40GE/ 100GE接口5~6及其拆分接口。 ● HSIC-X08S000插卡上的接口。 ● HSIC-Y08S000插卡上的接口。 |
| S6730-H6FX4Y2CZ-V2/S6730E-H-V2 | ● HSIC-X08S000插卡上的接口。 ● HSIC-Y08S000插卡上的接口。 |
| S6750-S | ● HSIC-X08S000插卡上的接口。 ● HSIC-Y08S000插卡上的接口。 ● 面板上的所有接口。 |
| S6750E-S | ● HSIC-X08S000插卡上的接口。 ● HSIC-Y08S000插卡上的接口。 ● 面板上的所有接口。 |
| S5755-S24P8J8YZ/S5755-S24T8J8YZ/ S5755-S24U8J8YZ | ● HSIC-X08S000插卡上的接口。 ● 面板上的所有接口。 |
| S5755-S24P8Y/S5755-S24T8Y/S5755- S24U8Y | 面板上的GE接口1~24支持MACsec，剩余带宽8*25G口抢占，最多可支持6个 25G口。 |
| S5755-S48P8YZ/S5755-S48T8YZ/ S5755-S48U8YZ | ● HSIC-X08S000插卡上的接口。 ● 面板上的所有接口。 |
| S5755-S48P8Y/S5755-S48T8Y/S5755- S48U8Y | 面板上的GE接口1~48，剩余带宽8*25G 口抢占，最多可支持6个25G口。 |

特性限制表 8-3 本特性的使用限制

| 特性限制 |
|---|
| 特殊报文不加密。涉及LLDP，MKA，1588，Pause，XLDP |
| 端口与协议对端均配置MACsec功能，且能接收到通过观察口传输过来的镜像报文，如果镜像报文中有MKA协议报文时，端口除了会接收到协议对端的MKA协议报文，还会收到镜像的MKA报文，这样会导致端口识别到两个peer（MI不一样）；由于设备不支持多点连接，协议无法正常建立，观察口数据流量无法传输。 |
| MACsec数据面加密算法切换时存在丢包可能。 |
| 端口工作在半双工时，配置MACsec，可能会由于冲突导致MACsec协议断链。建议不要在半双工时使用MACsec |

特性限制MACSec的端口范围对于产品S6750-H36C：
100G端口1-16，25-36支持，存在互斥关系；
100GE端口1-4与35-36互斥，100GE端口5-8与33-34互斥，100GE端口9-12与29-32互斥，100GE端口13-16与25-28互斥，默认100G端口1-16支持。
对于产品S5732-H44S4X6QZ-V2：
GE接口1~44，40GE接口5~6，10GE接口1~4。
对于产品S6730-H28X6CZ-V2：
10GE接口1~28，40GE/100GE接口5~6。
对于产品S6750-H48Y8C：
25GE端口1-32，100GE端口1-8支持，存在互斥关系；
25GE端口1-8与100GE端口7-8互斥，25GE端口9-16与100GE端口5-6互斥，25GE端口 17-24 与 100GE 端口 3-4 互斥， 25GE 端口 25-32 与 100GE 端口 1-2 互斥；
默认25GE端口1-24，100GE端口1-2支持。
对于产品S5755-S48T8Y，S5755-S48T8YZ，S5755-S48U8Y，S5755-S48U8YZ，S5755-S48P8Y，S5755-S48P8YZ：
GE接口：1-48支持MACSEC，剩余带宽8*25G口抢占，最多可支持6个25G口MACSEC。
对于产品S5732-H48UM4Y2CZ-KV2，S5732-H48UM4Y2CZ-V2，S5732- H48UM4Y2CZ-TV2：
MultiGE接口1~48。
对于产品S5735R-L16LP2UM2X-QA-V2，S5735E-L16LP2UM2X-QA-V2，S5735- L16LP2UM2X-QA-V2，S5735-L16P2UM2X-QA-V2：
16*GE电+ 2*MultiGE支持对于产品S6730-H48X6CZ-V2：
10GE接口1~48，40GE/100GE接口5~6。
对于产品S5732-H24UM4Y2CZ-KV2，S5732-H24UM4Y2CZ-V2：
MultiGE接口1~24。
对于产品S5735R-L16LP2X-QA-V2，S5735R-L16LP2S-QA-V2，S5735E-L16LP2X- QA-V2 ， S5735-L16LP2X-QA-V2 ：
16*GE电支持MACSEC对于产品S5735I-S-V2系列：
M0模式：GE电接口9-16，GE光接口17~18 M1模式：GE电接口9~12，10GE光接口5~6对于产品S5735-L14P2S-QA-V2：
14*GE电+2*GE光支持对于产品S5732-H24S4X6QZ-V2，S5732-H24S4X6QZ-TV2：
GE接口1~24，40GE接口5~6，10GE接口1~4。

特性限制对于产品S5755-H系列，S6750-S系列，S6750E-S系列，S5755-S24P8J8YZ，S5755-S24P8Y，S5755-S24T8J8YZ，S5755-S24T8Y，S5755-S24U8J8YZ，S5755- S24U8Y：
所有接口

### 8.5 MACsec缺省配置

表 8-4 MACsec 缺省配置

| 参数 | 缺省配置 |
|---|---|
| 接口的MACsec功能 | 未开启 |
| 密钥服务器优先级 | 16 |
| CAK | 未配置 |
| 加密模式 | normal |
| 加密偏移量 | 0 |
| MACsec帧头是否包含SCI | 包含 |
| SAK超时时间 | 3600秒 |
| 重播保护窗口大小 | 0 |
| MKA会话超时时间 | 6秒 |
| MACsec能力值 | 3 |

### 8.6 启用MACsec功能

背景信息启用MACsec功能首先需要创建并配置MACsec模板，然后在接口上应用模板并配置CAK。
为保证设备间的MKA会话可以正常建立，必须保证两端设备的接口上配置相同的CKN和CAK。两端设备的接口启用MACsec功能后，会根据优先级选出密钥服务器，用户可以在模板中配置MKA密钥服务器优先级数值，数值越小优先级越高，优先级高的设备将被选举为密钥服务器。当双方优先级相同时，则比较接口的SCI（Secure Channel Identifier）值。SCI由接口MAC地址和接口索引（Interface Index）的最后两个字节组成，SCI值较小的设备将被选举为密钥服务器。
为保障用户业务数据在网络中的安全传输，MACsec提供了数据加密和完整性校验的功能，可以通过配置加密模式选择性开启数据加密和完整性校验的功能。加密模式有以下三种：

● none：既不进行数据加密也不进行完整性校验。
● normal：既进行数据加密又进行完整性校验。
● integrity-only：只进行完整性校验不进行数据加密。
说明
在已经建立MACsec连接的情况下，Server端可以切换加密算法，Client端响应Server端进行算法
切换。但是当华为设备作为Server，而不支持加密算法切换的其他厂商设备做Client时，会导致
MACsec协商中断。
操作步骤
步骤1 进入系统视图。
system-view
步骤2 （可选）配置下次启动生效的MACsec工作模式。
macsec next-work-mode { a-mode | b-mode } slot slot-id
缺省情况下，MACsec工作模式为a-mode。即所有插卡槽位均支持MACsec功能，但所
有插卡槽位上的插卡不支持满接口MACsec功能。
说明
仅S6780-H支持该配置。
步骤3 创建并配置MACsec模板。
1. 创建一个MACsec模板，并且进入MACsec模板视图。
mac-security-profile name profile-name
2. （可选）配置MKA密钥服务器优先级。
mka keyserver priority priority
缺省情况下，MKA密钥服务器的优先级为16。
3. （可选）配置MACsec加密模式。
macsec mode { none | normal | integrity-only }
缺省情况下，MACsec加密模式为normal。
说明
当在网络中有数据流量的情况下部署MACsec时，为减少流量中断时间，可先配置两端加密
模式为none，待两端设备MKA会话协商成功后再将加密模式修改为normal。
步骤4 返回系统视图。
quit
步骤5 进入需要应用MACsec模板的接口。
interface interface-type interface-number
步骤6 配置CKN和CAK。
mka cak-mode static ckn string-name cak string-key
缺省情况下，未配置CKN和CAK。
CKN 为 CAK 的名称。为保证设备间的 MKA 会话可以正常建立，必须保证两端设备的接
口上配置相同的CKN和CAK。
步骤7 在接口上应用MACsec模板。

### 8.7 调整MACsec参数

mac-security-profile profile-name说明只有在接口上应用MACsec模板，MACsec功能才能生效。支持MACsec功能的接口请参考《MACSec配置注意事项》。
步骤8 （可选）开启设备的MACSec模块xpn模式下盐值字节序转换功能。
macsec xpn-salt reverse其他品牌的网络设备在实现MACSec功能时，xpn模式下发的盐值采用网络序或者主机序。通过配置该命令行可以兼容不同的实现方式。
----结束调整 参数
8.7 MACsec背景信息用户可以创建并配置一个新的MACsec模板，也可以进入已创建的MACsec模板修改参数。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入MACsec模板视图。
mac-security-profile name profile-name步骤3 配置MACsec参数。
表 8-5 配置 MACsec 参数

| 操作 | 命令 | 说明 |
|---|---|---|
| 配置MKA密钥生成算法 | mka cryptographic- algorithm { aes- cmac-128 | aes- cmac-256 | sm4- cmac-128 } | 设备使用MKA密钥生成算法根据CAK和 CKN生成KEK、ICK和SAK。缺省情况下，MKA密钥生成算法为AES- CMAC-128。密钥服务器生成SAK后，要通过MKA报文将加密后的SAK发送给对端设备，对端设备收到MKA报文后，对其进行完整性校验，如果校验不通过，则丢弃报文，如果校验通过，则解密报文得到 SAK。而且需要保证两端配置的密钥生成算法一致，否则可能协商不成功。仅S6750-H、S6780-H、S5755-S支持 sm4-cmac-128算法。 |

| 操作 | 命令 | 说明 |
|---|---|---|
| 配置MACsec数据报文加密算法 | macsec cipher-suite { gcm-aes-128 | gcm- aes-256 | gcm-aes- xpn-128 | gcm-aes- xpn-256 | gcm- sm4-128 | gcm-sm4- xpn-128 } * | 会话协商完成后，两端设备通过使用 SAK加解密数据报文进行加密通信。缺省情况下，设备支持的加密算法因设备而异，实际使用的算法由两端设备按加密强度由高到低自动协商确定。仅S6750-H、S6780-H、S5755-S支持 gcm-sm4-128、gcm-sm4-xpn-128算法。 |
| 配置MACsec加密偏移量 | macsec confidentiality-offset offset-value | MACsec加密偏移量表示从数据帧的 MACsec TAG字段后偏移多少字节再开始加密，协议提供0、30、50字节三个加密偏移量选择。某些需要识别IPv4/ IPv6报文头部的应用（比如负载均衡）要求报文头部不能被加密，因此需要配置加密偏移量。缺省情况下，MACsec加密偏移量为0字节。如果本端不是密钥服务器，则应用密钥服务器发布的加密偏移量；如果本端是密钥服务器，则应用本端配置的加密偏移量，并将该值发布给对端。 |
| 配置MACsec重播保护窗口 | macsec replay- window window-size | 为防止恶意用户通过重复发送捕获到的数据报文进行网络攻击，缺省情况下，接收方会丢弃重复或乱序的数据报文。但在某些情况下，数据报文因为发送优先级的不同，在转发过程中会被重新排序，最终到达接收端时变为乱序。为保证能够正常接收这些乱序的数据报文，需要配置重播保护窗口。假设设备配置的重播保护窗口大小为 a，如果接收到了一个报文序号为x的报文，则下一个允许被接收的报文的序号必须大于或等于x+1-a。请结合数据报文在传输网络中的转发途径，选择适当的重播保护窗口大小。若数据报文有可能被多次转发，那么乱序的可能性和乱序的范围会比较大，则建议适当调大重播保护窗口大小，反之调小。缺省情况下，MACsec重播保护窗口大小为0。 |

| 操作 | 命令 | 说明 |
|---|---|---|
| 配置MACsec帧头包含SCI | macsec include-sci | SCI（Secure Channel Identifier）用来标识报文的来源，由接口MAC地址和接口索引（Interface Index）的最后两个字节组成。当设备与其他厂商的设备对接配置MACsec功能时，由于实现原理的差异，可能需要在MACsec帧头中包含SCI，用以识别报文来源。由于当前设备仅支持设备到设备的MACsec，两端设备接口一一对应，此时MACsec帧头中可不必包含SCI。缺省情况下，MACsec帧头包含SCI。两端设备MACsec帧头是否包含SCI需要保持一致：两端都配置MACsec帧头包含SCI，或者两端都配置MACsec帧头不包含SCI。 |
| 配置MKA会话超时时间 | mka timer mka-life life-time | 会话协商完成，建立安全通道后，两端设备会通过交互MKA协议报文确认连接的存在。MKA协议定义了一个MKA会话保活定时器，用来规定MKA会话的超时时间。设备收到对端MKA协议报文后，启动定时器。 ● 如果在该超时时间内收到对端的 MKA协议报文，则重启定时器。 ● 如果在该超时时间内未收到对端的 MKA协议报文，则认为该连接已不安全，删除建立的会话，重新进行 MKA会话协商。缺省情况下，MKA会话超时时间为6 秒。 |
| 配置SAK超时时间 | mka timer sak-life life-time | 使用MACsec进行安全通信时，SAK被用于对数据报文进行加密和解密，为提高数据报文的安全性，当同一个SAK加密的数据报文达到一定数量或使用同一个 SAK超过一定时间时，需要更换SAK，由密钥服务器重新生成和分发新的 SAK，可根据实际情况调整SAK超时时间。缺省情况下，SAK超时时间为3600秒。如果本端不是密钥服务器，则应用密钥服务器发布的SAK超时时间；如果本端是密钥服务器，则应用本端配置的SAK 超时时间，并将该值发布给对端。 |

| 操作 | 命令 | 说明 |
|---|---|---|
| 配置MACsec能力值 | macsec capability capability-value | 能力值含义： ● 2：支持校验完整性和机密性，只能从报文头开始加密。 ● 3：支持校验完整性和机密性，允许从报文头、偏移30字节、偏移50字节开始加密。缺省情况下，MACsec能力值为3。当对接其他类型设备，如果对端设备只支持MACsec能力2，因此需要配置设备 MACsec能力和对端一致。如果MACsec能力配置为2，通过命令 macsec confidentiality-offset配置 MACsec加密偏移量为30或50将不生效，此时MACsec加密偏移量始终为0。 |
| 配置MACsec的安全策略 | macsec policy { must- secure | should- secure } | 安全策略含义： ● must-secure：MKA会话启动协商后明文报文全部丢弃，协商成功后报文正常加密和解密。 ● should-secure：MKA会话未协商成功前明文报文放通，MKA会话协商成功后丢弃明文报文，报文加、解密功能正常。缺省情况下，MACsec的安全策略为 must-secure。 |

----结束

### 8.8 检查配置结果

操作步骤步骤1 执行命令display macsec port ability [ slot slot-id ]，查看对应单板上端口的MACsec支持情况。
该命令行仅S6750-H系列支持。
步骤2 执行命令display mac-security-profile configuration [ name profile-name ]，查看MACsec模板的配置信息。
步骤3 执行命令display mka interface { interface-name | interface-type interface- number } [ verbose ]，查看指定接口的MACsec配置结果和MKA会话信息。
步骤 4 执行命令 display macsec statistics interface { interface-name | interface-type interface-number }，查看指定接口经过MACsec保护的数据报文的统计信息。
----结束

### 8.9 维护MACsec

操作步骤步骤1 在用户视图下执行命令reset mka statistics interface { interface-name | interface- type interface-number }，清除指定接口的MKA协议报文的统计信息。
步骤2 在用户视图下执行命令reset macsec statistics interface { interface-name | interface-type interface-number }，清除指定接口经过MACsec保护的数据报文的统计信息。
----结束

### 8.10 MACsec配置举例

#### 8.10.1 举例：配置MACsec

组网需求如图1所示，DeviceA和DeviceB相连，两台设备之间传输重要信息，要求对两台设备之间的数据通信进行安全保护。
图 8-4 配置设备到设备的 MACsec 功能组网图说明本例中interface1代表10GE1/0/1。
配置思路在两端设备上配置MACsec功能的配置思路如下：
1. 配置密钥服务器优先级，此处设置DeviceA作为密钥服务器。
2. 配置加密模式为normal，实现数据加密和完整性校验功能。
3. 配置MKA会话协商使用的CKN为f1c3b2a4d6d9a7c5b4e1ab56dc21ed79ac97be533671dcab2678ac55cf71aced，CAK为ab2145369adcadef69512347adceb210。

说明如下图所示，DeviceA和DeviceB设备之间存在中间设备（属于存在透传设备的级联场景）
DeviceC、DeviceD和DeviceE。
● 为了保证两端设备能够进行MACsec会话协商，需要中间设备支持二层协议透明传输功能。
这是由于，DeviceA和DeviceB之间建立MACsec会话协商时，除LLDP、MKA、1588、Pause外，其他类型的报文将会被加密，导致在DeviceC、DeviceD、DeviceE上面无法识别。比如STP报文，在DeviceA上面加密后，在DeviceC上面将会无法识别。
配置步骤如下，具体配置过程请参见《CLI配置指南-以太网交换配置》中的“二层协议透明传输配置”。
1. 在中间设备DeviceC和DeviceE的系统视图下执行命令l2protocol-tunnel user- defined-protocol protocol-name protocol-mac 0180-c200-0003 group-mac group-mac ，自定义二层透明传输 EAP 报文。
2. 在中间设备DeviceC与DeviceA相连的接口和DeviceE与DeviceB相连的接口执行命令l2protocol-tunnel user-defined-protocol protocol-name enable，使能接口的二层协议透明传输功能。
● 为了保证报文不会在中间设备上丢弃，如果中间设备与DeviceA或DeviceB相连的接口链路类型或中间设备之间相连的接口链路类型为trunk/hybrid，需要接口放通pvid（缺省VLAN）对应的VLAN。
这是由于，DeviceA和DeviceB发送的MACSec的协议报文和加密后的数据报文不携带VLAN，中间设备上的接口链路类型为trunk/hybrid时，报文被打上了带pvid的VLAN Tag。以中间设备DeviceC与DeviceA相连的接口为例，不同链路类型下常见配置如下：
● 示例1：接口链路类型为trunk，缺省VLAN为VLAN1，默认放通VLAN1。接口链路类型为hybrid时配置要求一致。
interface XXX port link-type trunk l2protocol-tunnel user-defined-protocol mka enable
● 示例2：接口链路类型为trunk，不放通VLAN1的情况下，需要指定接口的缺省VLAN并放通该VLAN。接口链路类型为hybrid时配置要求一致。
interface XXX port link-type trunk undo trunk port allow-pass vlan 1 //不放通VLAN1 port trunk pvid vlan 400 //指定接口的缺省VLAN为VLAN400 port trunk allow-pass vlan 400 //放通VLAN400 l2protocol-tunnel user-defined-protocol mka enable
● 示例3：接口链路类型为access，发送报文不带Tag。
interface XXX port link-type access l2protocol-tunnel user-defined-protocol mka enable操作步骤步骤1 配置DeviceA。
\# 创建MACsec模板。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] mac-security-profile name test1 \# 配置DeviceA的密钥服务器优先级为1，加密模式为normal。

[DeviceA-macsec-profile-test1] mka keyserver priority 1 [DeviceA-macsec-profile-test1] macsec mode normal [DeviceA-macsec-profile-test1] quit \# 配置CKN为f1c3b2a4d6d9a7c5b4e1ab56dc21ed79ac97be533671dcab2678ac55cf71aced，CAK为ab2145369adcadef69512347adceb210，应用MACsec模板。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] mka cak-mode static ckn f1c3b2a4d6d9a7c5b4e1ab56dc21ed79ac97be533671dcab2678ac55cf71aced cak ab2145369adcadef69512347adceb210 [DeviceA-10GE1/0/1] mac-security-profile test1 [DeviceA-10GE1/0/1] quit步骤2 配置DeviceB \# 创建MACsec模板。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] mac-security-profile name test2 \# 配置DeviceB的密钥服务器优先级为2，加密模式为normal。
[DeviceB-macsec-profile-test2] mka keyserver priority 2 [DeviceB-macsec-profile-test2] macsec mode normal [DeviceB-macsec-profile-test2] quit \# 配置CKN为f1c3b2a4d6d9a7c5b4e1ab56dc21ed79ac97be533671dcab2678ac55cf71aced，CAK为ab2145369adcadef69512347adceb210，应用MACsec模板，。
[DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] mka cak-mode static ckn f1c3b2a4d6d9a7c5b4e1ab56dc21ed79ac97be533671dcab2678ac55cf71aced cak ab2145369adcadef69512347adceb210 [DeviceB-10GE1/0/1] mac-security-profile test2 [DeviceB-10GE1/0/1] quit
----结束检查配置结果\# 在DeviceA上检查配置结果。
[DeviceA] display mka interface 10ge 1/0/1 Interface 10GE1/0/1:
CKN: F1C3B2A4D6D9A7C5B4E1AB56DC21ED79AC97BE533671DCAB2678AC55CF71ACED MKA status : SUCCEEDED MI : 5B8D4074D0E0639D8AE1AF1E MN : 52 MACsec mode : normal Key server : YES Live peers : 1 Potential peers : 0 Live peers list :
MI MN Priority Capability Rx-SCI 67C7271E983BA02C04A88ACD 53 2 3 000B09BACF0A0024 Potential peers list:
MI MN Priority Capability Rx-SCI
-- -- -- -- -- \# 在DeviceB上检查配置结果。
[DeviceB] display mka interface 10ge 1/0/1 Interface 10GE1/0/1:

CKN: F1C3B2A4D6D9A7C5B4E1AB56DC21ED79AC97BE533671DCAB2678AC55CF71ACED MKA status : SUCCEEDED MI : 67C7271E983BA02C04A88ACD MN : 56 MACsec mode : normal Key server : NO Live peers : 1 Potential peers : 0 Live peers list :
MI MN Priority Capability Rx-SCI 5B8D4074D0E0639D8AE1AF1E 55 1 3 000B09C312CE0031 Potential peers list:
MI MN Priority Capability Rx-SCI
-- -- -- -- --通过显示信息可以看出，MKA status为SUCCEEDED，表示MKA会话协商成功；
MACsec mode为normal，表示MACsec加密模式为normal。
配置脚本DeviceA \# sysname DeviceA \# mac-security-profile name test1 mka keyserver priority 1 \# interface 10GE1/0/1 mka cak-mode static ckn f1c3b2a4d6d9a7c5b4e1ab56dc21ed79ac97be533671dcab2678ac55cf71aced cak %^%#&gqJ1f*uV0vqB$ZT5hr#qwL/;Cd/`OmO<m2+hh1A1&w{)jh1"'poiXB\UAn9%^%# mac-security-profile test1 \# return DeviceB \# sysname DeviceB \# mac-security-profile name test2 mka keyserver priority 2 \# interface 10GE1/0/1 mka cak-mode static ckn f1c3b2a4d6d9a7c5b4e1ab56dc21ed79ac97be533671dcab2678ac55cf71aced cak %^%#W5_!' 9]i>47d&X^Vro#S!z<4s+/N5\Ek*#27i_Wz-U3/"3tJM1.6++,nP+Z%^%# ~ mac-security-profile test2 \# return
