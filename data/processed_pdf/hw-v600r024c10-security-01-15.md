# S1700, S5700, S6700 V600R024C10 配置指南-安全 01-15 Keychain配置

## 15 Keychain配置

Keychain本身只对加密和认证的Key进行管理，只有在被应用程序使用时，Keychain才能发挥作用。

### 15.1 Keychain简介

15.2 Keychain原理描述
Keychain配置注意事项
15.3
15.4 Keychain缺省配置
15.5 配置Keychain
15.6 Keychain配置举例
15.1 Keychain 简介
定义
Keychain即“钥匙串”，形象地说，当应用程序不断地变换自己的加密锁时，就需要
不同的钥匙，才能打开。
Keychain中的Key，不是算法，也不是密钥，而是一套加密和认证的规则。keychain通
过对它拥有的一系列Key进行集中控制和灵活管理，为应用程序提供动态的安全认证服
务。
目的
RIP、IS-IS、OSPF、BGP等应用程序在和对端进行会话之前，需要首先建立传输层的连
接。
为了保证应用程序会话连接和交互数据的安全性，可以对报文进行MD5算法的认证，
但MD5认证存在如下缺点：
● MD5算法相对简单，无法满足安全性要求高的网络。
● 考虑到密钥安全，应定期更换密钥。MD5算法和密钥直接在应用程序中配置，与
应用程序之间是一对一的静态绑定。因此，需要分别在两端设备的多个应用程序
上逐个进行手动更换。
为了替代MD5，Keychain定义了应用程序认证的Key的集合：

● Keychain中的每个Key中可以灵活挑选相对MD5更安全的算法，后续还能扩展选
择更安全的算法。
● Keychain中的每个Key拥有独立的算法、密钥和活跃时间。两端设备的应用程序使
用了Keychain认证，即会匹配多个Key。因此可以根据Key的活跃时间实现在两端
设备的多个应用程序上定期自动更换认证算法和密钥。
● Keychain中的Key在进行动态更换时，不需要断开重连正在使用的传输层连接，可
以始终保持应用程序会话连接的稳定性，不会中断业务。

### 15.2 Keychain原理描述

#### 15.2.1 Keychain的基本概念

Keychain拥有一系列的加密和认证的规则Key，即Key的集合。
Key 的三要素Keychain中的每个Key包含三个要素：
● 认证算法：支持MD5、SHA-1、HMAC-MD5、HMAC-SHA1-12、HMAC- SHA1-20、HMAC-SHA-256、SHA-256、SM3、HMAC-SHA-384、HMAC- SHA-512算法。
说明为了保证更好的安全性，建议不要使用MD5、HMAC-MD5和SHA-1算法。
● 认证密钥：一段用于加密的字符串。同一明文信息使用不同的密钥加密，会得到不同的密文；只有使用同一个密钥加密，才会得到相同的密文。
● Key的活跃时间：代表了这个Key生效的时间段，当一个Key没有处于活跃时间时，会由另一个活跃的Key来替代。
说明使用认证算法和密钥对报文进行加密计算，会得到一串长度固定的信息摘要字符串，即Message Authentication Code（信息认证码，简称MAC）。
Key 的 ID 和分类为了对设备中的Key的集合进行管理，Keychain定义了Key的ID以便进行区分。而设备中的Key分为发送Key和接收Key两类：
● 发送Key：用于设备在发送报文前进行加密。
● 接收Key：用于设备在接收报文后进行解密。
说明
● 本设备的发送Key需要与对端设备的接收Key一致，这样才能在对端设备上使用同种算法和同个密钥来解密收到的加密报文。
● 设备上的发送Key和接收Key可以是同一个，也可以不是。在某一时间段，使用哪个Key进行发送加密只取决于哪个Key当前正处于发送活跃时间，使用哪个Key进行接收解密只取决于哪个Key当前正处于接收活跃时间。

Key 的活跃时间为了对设备中的Key的集合进行控制，即决定哪个Key是当前生效的Key，生效时间段是多久，哪个Key是接下来准备用来替代的Key，Keychain定义了Key的活跃时间。
Key的活跃时间代表了这个Key生效的时间段：
● 某个Key处于发送活跃时间，即为当前生效的发送Key。
● 某个Key处于接收活跃时间，即为当前生效的接收Key。
不论是发送还是接收活跃时间，都可以采用两种时间模式来进行定义：
● 绝对时间模式：表示Keychain中的Key只能在一个指定的时间段内生效，例如2019年12月10日的12:00-18:00。
● 周期时间模式：如表15-1所示，表示Keychain中的Key可以周期性地在一个指定的时间段内生效表 15-1 周期时间模式

| 周期 | 时间段 |
|---|---|
| 每日 | 每日的指定时间，例如12:00-18:00。 |
| 每周 | 每周的指定周几，例如周一、周三、周五、周日。 |
| 每月 | 每月的指定日期，例如3号到8号。 |
| 每年 | 每年的指定月份，例如六月到九月。 |

说明
● 缺省发送Key：如果在某个时间段内没有活跃的发送Key，此时设备发送的报文将无法进行加密，无法为应用程序提供安全认证服务。为避免这种情况，设备支持配置缺省发送Key，在某个时间段内没有其他活跃的发送Key时生效。
● 接收容忍时间：当对端设备的发送Key进行更换时，本端设备的接收Key也必须同步进行对应更换，否则本端设备接收到的报文会因为无法解密而丢包。两端设备在同时更换Key时，由于报文传输的过程存在一个时间差，本端更换新Key后可能才接收到对端使用老Key加密的报文。同时，还考虑到网络中两端设备的时钟可能出现不同步的情况，设备支持配置接收容忍时间，保证在更换Key时有一个平滑的时间过渡。接收容忍时间只对接收Key生效，配置以后，接收Key的真实活跃时间=接收容忍时间+Key原来的活跃时间+接收容忍时间。即，对接收key的启动和结束时间都将会进行相应的延长。
Key 的集合Keychain是Key的集合，相同类型的多个Key可以放到1个集合中，称为1条Keychain。
这里的相同类型，一般指的是Key的活跃时间的模式。例如每年指定月份活跃的Key和每月指定日期活跃的key就不属于相同类型，因为把这2个Key放在1条Keychain中，无法进行时间上的切换。
根据业务需求，设备支持配套多条Keychain，提供给多个应用程序选择使用。
例如表15-2中的6条Key，Key1、Key3属于相同类型，可以放到1个集合KeychainA中；Key2、Key4属于相同类型，可以放到1个集合KeychainB中；Key5只能单独放到1个集合KeychainC中；Key6只能单独放到1个集合KeychainD中。

表 15-2 Key 的集合示例

| Key | 认证算法 | 认证密钥（加密字符串） | 活跃时间 | Key的集合 |
|---|---|---|---|---|
| Key1 | HMAC- SHA1-20 | AbCdEfGh | 2019年12月10 日12:00-15:00 | KeychainA |
| Key2 | HMAC- SHA1-20 | HgFeDcBa | 每周一、周三、周五、周日 | KeychainB |
| Key3 | HMAC- SHA-256 | AcEgHfDb | 2019年12月10 日15:00-18:00 | KeychainA |
| Key4 | HMAC- SHA-256 | HeBgDfCa | 每周二、周四、周六 | KeychainB |
| Key5 | HMAC- SHA-256 | DhAgBfCe | 每月3号到8号 | KeychainC |
| Key6 | HMAC- SHA-256 | EaHgBcFd | 每年六月到九月 | KeychainD |

#### 15.2.2 Keychain的实现原理（非TCP）

Keychain本身只对加密和认证的Key进行管理，只有在被应用程序使用时，Keychain才能发挥作用。
应用程序在使用Keychain认证时，是通过绑定一条Keychain来实现，例如绑定KeychainA，则可以使用这条Keychain中的Key集合来进行加密和解密。

加密过程图 15-1 非 TCP 应用程序使用 Keychain 认证的加密过程说明如果应用程序向Keychain询问未获得活跃的发送Key，应用程序在发送报文时将无法使用Keychain认证，即不做加密正常发送。

解密过程图 15-2 非 TCP 应用程序使用 Keychain 认证的解密过程说明
● 解密过程并非解开密码，而是重新加密后判断新的加密结果与收到的老的解密结果是否一致，一致则表示可以正确解密。
● 特别地，当IS-IS使用Keychain认证时，解密过程中IS-IS不向Keychain提供Key ID，Keychain会查找所有活跃的接收key，找一个算法相同的进行解密。

#### 15.2.3 Keychain的实现原理（TCP）

TCP应用程序使用Keychain认证的原理与非TCP应用程序类似，只是增加了TCP增强认证选项。
TCP 增强认证选项TCP增强认证选项的格式如图15-3所示，TCP报文头中会携带此认证选项，专门用于为TCP连接提供认证保护。
图 15-3 TCP 增强认证选项的格式
● Kind：8个比特，用于标识此选项的类型，由IANA分配。

● Length：8个比特，用于标识此选项的总长度。
● T：1个比特，用于标识此选项是否被包含在TCP增强认证计算的对象中，0表示包
含，默认值是0。
K：1个比特，为以后预留，当前值是0。
●
● Alg-id：6个比特，用于标识TCP增强认证的算法。
● Res：2个比特，为以后预留，当前值是0。
● Key-id：6个比特，用于标识Keychain认证的Key。
● Authentication Data：长度可变，至少包含TCP增强认证计算的结果。
由于IANA没有统一定义Kind和Alg-id字段的取值，各设备商使用不同的取值。为了使
不同厂商的设备能够互通，Keychain支持配置TCP Kind和TCP algorithm-id。
加密过程
图 15-4 TCP 应用程序使用 Keychain 认证的加密过程

解密过程图 15-5 TCP 应用程序使用 Keychain 认证的解密过程

### 15.3 Keychain配置注意事项

License 依赖Keychain无需License许可即可使用。
硬件依赖表 15-3 支持本特性的硬件

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
特性限制无

### 15.4 Keychain缺省配置

Keychain的缺省配置如表15-4所示。
表 15-4 Keychain 缺省配置

| 参数 | 缺省值 |
|---|---|
| 认证算法加密后的摘要长度 | HMAC-SHA-256：32字节 SHA-256：32字节 HMAC-SHA1-20：20字节 |
| 接收容忍时间 | 0：不容忍 |
| TCP增强认证选项中的类型值：TCP Kind | 254 |
| TCP认证的算法ID：TCP algorithm-id | HMAC-SHA1-12：2 MD5：3 SHA-1：4 HMAC-MD5：5 HMAC-SHA1-20：6 HMAC-SHA-256：7 SHA-256：8 SM3：9 HMAC-SHA-384：11 HMAC-SHA-512：12 HMAC-SM3：13 说明为了保证更好的安全性，建议不要使用 MD5、HMAC-MD5和SHA-1算法。 |

### 15.5 配置Keychain

| 参数 | 缺省值 |
|---|---|
| 时间格式 | LMT（当地平均时间，Local Mean Time） |

配置
15.5 Keychain

#### 15.5.1 创建Keychain

前提条件在配置Keychain任务之前，需要提前完成NTP配置，保证发送端和接收端时间一致。
背景信息配置 Keychain 首先需要创建 Keychain ，可以根据需要创建 1 条或多条 Keychain 。
操作步骤步骤1 进入系统视图。
system-view步骤2 创建Keychain，并进入Keychain视图。
keychain keychain-name mode { absolute | periodic { daily | weekly | monthly | yearly } }创建Keychain时，时间模式是必配的。Keychain创建成功后，再进入Keychain视图，时间模式可以不用指定，即可以直接输入keychain Keychain-name去进入已创建的Keychain的视图。
步骤3 （可选）配置Keychain的接收容忍时间。
receive-tolerance { value | infinite | seconds secvalue }建议配置接收容忍时间，避免因时钟抖动造成丢包。
配置容忍时间可以采用两种方式：
● 指定一个具体的时间，单位是分钟或秒，其中分钟的最大值是14400分钟（10天），秒的最大值是864000秒（十天）。缺省情况下，接收容忍时间均是0，即不容忍。所以，建议配置接收容忍时间，避免因时钟抖动造成丢包。
● 配置infinite，容忍时间为无限大，即Key-id的接收永久生效。
步骤4 （可选）配置Keychain的时间格式：LMT（当地平均时间，Local Mean Time）或者UTC（通用协调时间，Universal Time Coordinated）。
time mode { lmt | utc }缺省情况下，Keychain的时间格式是LMT。
步骤5 在TCP的应用程序中使用Keychain，还需要配置TCP增强认证选项中的类型值（TCP Kind）和TCP认证的算法ID（TCP algorithm-id）。在非TCP的应用程序中使用Keychain，则不需要配置此步骤。
tcp-kind kind-value tcp-algorithm-id { md5 | sha-1 | hmac-md5 | hmac-sha1-12 | hmac-sha1-20 | hmac-sha-256 | sha-256 | sm3 | hmac-sha-384 | hmac-sha-512 | hmac-sm3 } algorithm-id

说明为了保证更好的安全性，建议不要使用MD5、HMAC-MD5和SHA-1算法。
步骤6 退出Keychain视图。
quit
----结束

#### 15.5.2 配置Keychain中的Key

背景信息创建Keychain以后，需要创建Keychain中的Key并对其进行配置，可以根据需要在每条Keychain中创建1个或多个Key。
操作步骤步骤 1 进入系统视图。
system-view步骤2 进入已创建的Keychain视图。
keychain keychain-name步骤3 创建Key，并进入Key视图。
key-id key-id步骤4 配置Key的认证算法。
algorithm { md5 | sha-1 | hmac-md5 | hmac-sha1-12 | hmac-sha1-20 | hmac-sha-256 | sha-256 | sm3 | hmac-sha-384 | hmac-sha-512 | hmac-sm3 }说明为了保证更好的安全性，建议不要使用MD5、HMAC-MD5和SHA-1算法。
此命令中的md5、sha-1、hmac-md5、hmac-sha1-12和hmac-sha1-20参数需要安装弱安全算法/协议特性包后才能使用。
出于安全性考虑，不建议使用该特性提供的弱安全算法或弱安全协议。如果确实需要使用，请执行命令install feature-software WEAKEA安装弱安全算法/协议特性包WEAKEA。设备默认自带弱安全算法/协议特性包WEAKEA，特性包安装或卸载的详细步骤请参见《CLI配置指南-系统管理配置》中的“升级维护配置”。
步骤5 配置Key的认证密钥（加密字符串）。
key-string { plain-cipher-text | plain plain-text | cipher plain-cipher-text }说明密码建议符合密码复杂度规则：大写、小写、数字、特殊字符（不包括？和空格）中至少有2种，并且长度不能小于8。
为了保证更好的安全性，建议使用cipher类型，在查看配置文件时，配置的密钥会以密文方式显示。
步骤 6 配置 Key 的发送活跃时间，如表 15-5 所示，需要根据已配置的 Keychain 的时间模式来进行对应的配置。
Key的活跃时间，依赖时钟同步。

表 15-5 配置 Key 的发送活跃时间

| Keychain的时间模式 | Key的发送活跃时间的配置命令 |
|---|---|
| 绝对时间模式：absolute | send-time start-time start-date { duration { duration-value | infinite } | { to end-time end-date } } |
| 周期时间模式（每天）：periodic daily | send-time daily start-time to end- time |
| 周期时间模式（每周）：periodic weekly | send-time day { start-day to end-day | start-day &<1-7> } |
| 周期时间模式（每月）：periodic monthly | send-time date { start-date to end- date | start-date &<1-31> } |
| 周期时间模式（每年）：periodic yearly | send-time month { start-month to end-month | start-month &<1-12> } |

步骤7 配置Key的接收活跃时间，如表15-6所示，需要根据已配置的Keychain的时间模式来进行对应的配置。
Key的活跃时间，依赖时钟同步。
表 15-6 配置 Key 的接收活跃时间

| Keychain的时间模式 | Key的接收活跃时间的配置命令 |
|---|---|
| 绝对时间模式：absolute | receive-time start-time start-date { duration { duration-value | infinite } | { to end-time end-date } } |
| 周期时间模式（每天）：periodic daily | receive-time daily start-time to end- time |
| 周期时间模式（每周）：periodic weekly | receive-time day { start-day to end- day | start-day &<1-7> } |
| 周期时间模式（每月）：periodic monthly | receive-time date { start-date to end- date | start-date &<1-31> } |
| 周期时间模式（每年）：periodic yearly | receive-time month { start-month to end-month | start-month &<1-12> } |

步骤8 （可选）配置该key为缺省发送key。
default send-key-id每条Keychain中只能存在1个缺省的发送key。
步骤9 退出Key视图。
quit步骤10 （可选）配置认证算法加密后的摘要长度。
digest-length { hmac-sha1-20 | hmac-sha-256 | sha-256 } length

缺省情况下，认证算法加密后的摘要长度是：
● HMAC-SHA1-20：20字节
● HMAC-SHA-256：32字节
● SHA-256：32字节步骤11 退出Keychain视图。
quit
----结束

#### 15.5.3 使用Keychain

背景信息Keychain本身只对加密和认证的Key进行管理，只有在被应用程序使用时，Keychain才能发挥作用。如表15-7所示，在这些应用程序中可以使用Keychain。
表 15-7 在应用程序中使用 Keychain

| 应用程序 | 传输层协议 | 视图 | 生效范围 | 配置参考章节 | 支持的加密算法 |
|---|---|---|---|---|---|
| RIP | 非 TCP | 接口视图 | 接口 | IP路由配置>RIP配置>提升RIP网络安全性>配置RIP-2报文的认证方式 | 请参见rip authentication- mode md5命令 |
| IS- IS/IS- ISv6 | 非 TCP | IS-IS视图 | IS-IS 区域 | IP路由配置>IS-IS 配置>配置IS-IS认证 IP路由配置>IS- ISv6配置>配置 IPv6 IS-IS认证 | 请参见area- authentication-mode（IS- IS视图）命令的keychain keychain-name参数说明部分 |
|  |  | IS-IS视图 | IS-IS 路由域 |  | 请参见domain- authentication-mode命令的keychain keychain-name 参数说明部分 |
|  |  | 接口视图 | 接口 |  | 请参见isis authentication- mode（P2P接口）或isis authentication-mode（广播网接口）命令的keychain keychain-name参数说明部分 |

| 应用程序 | 传输层协议 | 视图 | 生效范围 | 配置参考章节 | 支持的加密算法 |
|---|---|---|---|---|---|
| OSPF / OSPF v3 | 非 TCP | OSPF区域视图 | OSPF 区域 | IP路由配置>OSPF 配置>配置OSPF认证 IP路由配置 >OSPFv3配置>配置OSPFv3认证 | 请参见authentication- mode（OSPF区域视图）或 authentication-mode （OSPFv3区域视图）或 authentication-mode （OSPFv3视图）命令的 keychain参数说明部分 |
|  |  | 接口 | 接口 |  | 请参见ospf authentication-mode或 ospf authentication-mode multi-area命令的keychain 参数说明部分 |
|  |  | OSPF区域视图 | 虚连接 |  | 请参见vlink-peer命令的 keychain参数说明部分 |
| MPLS LDP UDP | 非 TCP | MPLS- LDP视图 | 对等体或对等体组 | MPLS配置>MPLS LDP配置>配置 LDP安全特性>配置LDP Keychain 认证 | 不支持弱加密算法，具体情况请参见authentication udp-remote key-chain命令的注意事项部分 |
| MPLS RSVP | 非 TCP | 接口视图 | 接口 | MPLS配置>MPLS TE配置>配置 RSVP-TE认证>配置RSVP-TE认证 | 请参见algorithm命令的算法部分说明为了保证更好的安全性，建议不要使用MD5、HMAC-MD5和 SHA-1算法，推荐使用其他更安全的算法，包括HMAC- SHA-256、SHA-256、HMAC- SHA-384、HMAC-SHA-512、 SM3、HMAC-SM3。 |
|  | 非 TCP | MPLS RSVP- TE邻居视图 | RSVP 邻居 | MPLS配置>MPLS TE配置>配置 RSVP-TE认证>配置RSVP-TE认证 | 请参见algorithm命令的算法部分说明为了保证更好的安全性，建议不要使用MD5、HMAC-MD5和 SHA-1算法，推荐使用其他更安全的算法，包括HMAC- SHA-256、SHA-256、HMAC- SHA-384、HMAC-SHA-512、 SM3、HMAC-SM3。 |
| MPLS LDP | TCP | MPLS- LDP视图 | 对等体或对等体组 | MPLS配置>MPLS LDP配置>配置 LDP安全特性>配置LDP Keychain 认证 | 请参见authentication key- chain （MPLS-LDP视图）命令的注意事项部分 |

| 应用程序 | 传输层协议 | 视图 | 生效范围 | 配置参考章节 | 支持的加密算法 |
|---|---|---|---|---|---|
| BGP/ BGP4 + | TCP | BGP视图及相关视图 | 对等体或对等体组 | IP路由配置>BGP 配置>配置BGP认证>配置Keychain 认证 IP路由配置 >BGP4+配置>配置BGP4+认证 | 请参见BGP特性peer keychain命令的keychain- name参数说明部分 |
| 组播 MSDP | TCP | VPN实例 MSDP 视图 | 对等体 | MSDP配置>配置 MSDP对等体> （可选）配置 MSDP认证 | 请参见algorithm命令的算法部分 |
|  | TCP | 公网实例 MSDP 视图 | 对等体 | MSDP配置>配置 MSDP对等体> （可选）配置 MSDP认证 | 请参见algorithm命令的算法部分 |

下面以RIP为例，介绍使用Keychain的配置。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入接口视图。
interface interface-type interface-number步骤3 将接口从二层模式切换到三层模式。
undo portswitch仅 S6780-H 、 S6750-H 、 S6730-H-V2 、 S6730E-H-V2 、 S5755-H 、 S5755-S 、 S6750-
S、S6750E-S、S5732-H-V2系列支持通过undo portswitch命令将接口从二层模式切换到三层模式。
请用户根据实际接口类型自行选择是否要执行此步骤。
步骤4 配置RIP使用Keychain认证。
rip authentication-mode md5 nonstandard keychain keychain-name步骤5 退出接口视图。
quit
----结束

#### 15.5.4 检查Keychain配置结果

操作步骤执行命令display keychain-name，查看Keychain的配置信息。
● keychain
● 执行命令display keychain keychain-name key-id key-id，查看Keychain中key的配置信息。
----结束

### 15.6 Keychain配置举例

#### 15.6.1 举例：配置IS-IS使用Keychain认证

组网需求如图 15-6 所示，网络中 DeviceA 、 DeviceB 和 DeviceC 通过 IS-IS 实现互通。
为了确保IS-IS连接的稳定和安全，配置Keychain为IS-IS提供动态的安全认证服务。
图 15-6 Keychain 组网图说明本例中interface1，interface2分别代表Vlanif10，Vlanif20。
配置本例，需要准备以下数据：
● IS-IS进程号
● IS-IS进程的NET（网络实体名称，Network Entity Title）
● Keychain名称
● Keychain的接收容忍时间
● Keychain 中 Key 的 ID
● Key的认证算法和认证密钥（加密字符串）
● Key的活跃发送时间和活跃接收时间配置注意事项
● 配置本例前，需要提前完成NTP配置。
● 使用Keychain认证的两端之间的配置需要对应，以DeviceA和DeviceB为例：
– DeviceA和DeviceB配置的Keychain名称需要相同。
– DeviceA和DeviceB配置的Keychain的时间模式需要相同。
– DeviceA和DeviceB配置的Keychain的Key的ID需要相同。配置多个Key时，两端都需要配置相同ID的多个Key。

– 对于同一个Key，DeviceA和DeviceB配置的认证算法和认证密钥（加密字符
串）需要相同。
– 对于同一个Key，DeviceA和DeviceB配置的活跃发送时间和接收活跃时间需
要对应。例如，DeviceB的活跃接收时间至少需要包含DeviceA的活跃发送时
间，以避免丢包。反之亦然。
● 如果Keychain中配置多个Key时，其中只能有1个Key配置为缺省发送key。
配置思路
1. 配置IS-IS。
2. 创建Keychain。
3. 配置Keychain中的Key，以及Key-id的认证算法为hmac-sha-256。
4. 配置IS-IS使用Keychain认证。
操作步骤
步骤1 配置IS-IS。
\# 配置DeviceA。
<HUAWEI> system-view
[HUAWEI] sysname DeviceA
[DeviceA] isis 1
[DeviceA-isis-1] is-level level-1
[DeviceA-isis-1] network-entity 10.0000.0000.0001.00
[DeviceA-isis-1] quit
[DeviceA] interface 10ge 1/0/1
[DeviceA-10ge1/0/1] port link-type trunk
[DeviceA-10ge1/0/1] port trunk allow-pass vlan 10
[DeviceA-10ge1/0/1] quit
[DeviceA] vlan batch 10
[DeviceA] interface vlanif 10
[DeviceA-10GE1/0/1Vlanif10] ip address 192.168.1.1 24
[DeviceA-10GE1/0/1Vlanif10] isis enable 1
[DeviceA-10GE1/0/1Vlanif10] quit
\# 配置DeviceB。
<HUAWEI> system-view
[HUAWEI] sysname DeviceB
[DeviceB] isis 1
[DeviceB-isis-1] is-level level-1
[DeviceB-isis-1] network-entity 10.0000.0000.0002.00
[DeviceB-isis-1] quit
[DeviceB] interface 10ge 1/0/1
[DeviceB-10ge1/0/1] port link-type trunk
[DeviceB-10ge1/0/1] port trunk allow-pass vlan 10
[DeviceB-10ge1/0/1] quit
[DeviceB] vlan batch 10 20
[DeviceB] interface vlanif 10
[DeviceB-10GE1/0/1Vlanif10] ip address 192.168.1.2 24
[DeviceB-10GE1/0/1Vlanif10] isis enable 1
[DeviceB-10GE1/0/1Vlanif10] quit
[DeviceB] interface 10ge 1/0/2
[DeviceB-10ge1/0/2] port link-type trunk
[DeviceB-10ge1/0/2] port trunk allow-pass vlan 20
[DeviceB-10ge1/0/2] quit
[DeviceB] interface vlanif 20
[DeviceB-10GE1/0/2Vlanif20] ip address 192.168.2.2 24
[DeviceB-10GE1/0/2Vlanif20] isis enable 1
[DeviceB-10GE1/0/2Vlanif20] quit
\# 配置DeviceC。

<HUAWEI> system-view [HUAWEI] sysname DeviceC [DeviceC] isis 1 [DeviceC-isis-1] is-level level-1 [DeviceC-isis-1] network-entity 10.0000.0000.0003.00 [DeviceC-isis-1] quit [DeviceC] interface 10ge 1/0/2 [DeviceC-10ge1/0/2] port link-type trunk [DeviceC-10ge1/0/2] port trunk allow-pass vlan 20 [DeviceC-10ge1/0/2] quit [DeviceA] vlan batch 20 [DeviceC] interface vlanif 20 [DeviceC-10GE1/0/2Vlanif20] ip address 192.168.2.1 24 [DeviceC-10GE1/0/2Vlanif20] isis enable 1 [DeviceC-10GE1/0/2Vlanif20] quit步骤2 创建Keychain。
\# 配置DeviceA。
[DeviceA] keychain huawei mode absolute [DeviceA-keychain-huawei] receive-tolerance 10 [DeviceA-keychain-huawei] quit \# 配置DeviceB。
[DeviceB] keychain huawei mode absolute [DeviceB-keychain-huawei] receive-tolerance 10 [DeviceB-keychain-huawei] quit \# 配置DeviceC。
[DeviceC] keychain huawei mode absolute [DeviceC-keychain-huawei] receive-tolerance 10 [DeviceC-keychain-huawei] quit步骤3 配置Keychain中的Key。
\# 配置DeviceA。
[DeviceA] keychain huawei [DeviceA-keychain-huawei] key-id 1 [DeviceA-keychain-huawei-keyid-1] algorithm hmac-sha-256 [DeviceA-keychain-huawei-keyid-1] key-string cipher YsHsjx_202206 [DeviceA-keychain-huawei-keyid-1] send-time 12:00 2019-12-10 to 18:00 2019-12-10 [DeviceA-keychain-huawei-keyid-1] receive-time 12:00 2019-12-10 to 18:00 2019-12-10 [DeviceA-keychain-huawei-keyid-1] default send-key-id [DeviceA-keychain-huawei-keyid-1] quit [DeviceA-keychain-huawei] quit \# 配置DeviceB。
[DeviceB] keychain huawei [DeviceB-keychain-huawei] key-id 1 [DeviceB-keychain-huawei-keyid-1] algorithm hmac-sha-256 [DeviceB-keychain-huawei-keyid-1] key-string cipher YsHsjx_202206 [DeviceB-keychain-huawei-keyid-1] send-time 12:00 2019-12-10 to 18:00 2019-12-10 [DeviceB-keychain-huawei-keyid-1] receive-time 12:00 2019-12-10 to 18:00 2019-12-10 [DeviceB-keychain-huawei-keyid-1] default send-key-id [DeviceB-keychain-huawei-keyid-1] quit [DeviceB-keychain-huawei] quit \# 配置DeviceC。
[DeviceC] keychain huawei [DeviceC-keychain-huawei] key-id 1 [DeviceC-keychain-huawei-keyid-1] algorithm hmac-sha-256 [DeviceC-keychain-huawei-keyid-1] key-string cipher YsHsjx_202206 [DeviceC-keychain-huawei-keyid-1] send-time 12:00 2019-12-10 to 18:00 2019-12-10 [DeviceC-keychain-huawei-keyid-1] receive-time 12:00 2019-12-10 to 18:00 2019-12-10

[DeviceC-keychain-huawei-keyid-1] default send-key-id [DeviceC-keychain-huawei-keyid-1] quit [DeviceC-keychain-huawei] quit步骤4 配置IS-IS使用Keychain认证。
\# 配置DeviceA。
[DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] isis authentication-mode keychain huawei [DeviceA-10GE1/0/1] quit [DeviceA] quit \# 配置DeviceB。
[DeviceB] interface 10ge 1/0/1 [DeviceB-10GE1/0/1] isis authentication-mode keychain huawei [DeviceB-10GE1/0/1] quit [DeviceB] interface 10ge 1/0/2 [DeviceB-10GE1/0/2] isis authentication-mode keychain huawei [DeviceB-10GE1/0/2] quit [DeviceB] quit \# 配置DeviceC。
[DeviceC] interface 10ge 1/0/2 [DeviceC-10GE1/0/2] isis authentication-mode keychain huawei [DeviceC-10GE1/0/2] quit [DeviceC] quit
----结束检查配置结果以DeviceA为例查看IS-IS使用Keychain认证是否配置成功。
● 执行display keychain keychain-name，查看当前处于Active状态的Key-id。
<DeviceA> display keychain huawei Keychain Information:
---------------------- Keychain Name : huawei Timer Mode : Absolute Receive Tolerance(min) : 10 Digest Length : 32 Time Zone : LMT TCP Kind : 254 TCP Algorithm IDs :
HMAC-MD5 : 5 HMAC-SHA1-12 : 2 HMAC-SHA1-20 : 6 MD5 : 3 SHA1 : 4 HMAC-SHA-256 : 7 SHA-256 : 8 SM3 : 9 HMAC-SHA-384 : 11 HMAC-SHA-512 : 12 Number of Key ID : 1 Active Send Key ID : 1 Active Receive Key ID : 01 Default send Key ID : 1 Key ID Information:
SHA1 : 4 HMAC-SHA-256 : 7 SHA-256 : 8 SM3 : 9 Number of Key ID : 1 Active Send Key ID : 1 Active Receive Key ID : 01

Default send Key ID : 1 Key ID Information:
---------------------- Key ID : 1 Key string : ****** Algorithm : HMAC-SHA-256 SEND TIMER :
Start time : 2019-12-10 12:00 End time : 2019-12-10 18:00 Status : Active RECEIVE TIMER :
Start time : 2019-12-10 12:00 End time : 2019-12-10 18:00 Status : Active
● 执行display isis lsdb verbose查看IS-IS的链路状态数据库的详细信息。
<DeviceA> display isis lsdb verbose Database information for ISIS(1)
----------------------------------- Level-1 Link State Database LSPID Seq Num Checksum HoldTime Length ATT/P/OL
----------------------------------------------------------------------------- 0000.0000.0001.00-00* 0x0000020a 0x94e6 409 68 0/0/0 SOURCE 0000.0000.0001.00 NLPID IPV4 AREA ADDR 10 INTF ADDR 192.168.1.1 NBR ID 0000.0000.0002.01 COST: 10 IP-Internal 192.168.1.0 255.255.255.0 COST: 10 0000.0000.0002.00-00 0x00000219 0xfa60 431 95 0/0/0 SOURCE 0000.0000.0002.00 NLPID IPV4 AREA ADDR 10 INTF ADDR 192.168.1.2 INTF ADDR 192.168.2.2 NBR ID 0000.0000.0002.01 COST: 10 NBR ID 0000.0000.0003.01 COST: 10 IP-Internal 192.168.1.0 255.255.255.0 COST: 10 IP-Internal 192.168.2.0 255.255.255.0 COST: 10 0000.0000.0002.01-00 0x0000007e 0xa767 305 55 0/0/0 SOURCE 0000.0000.0002.01 NLPID IPV4 NBR ID 0000.0000.0002.00 COST: 0 NBR ID 0000.0000.0001.00 COST: 0 0000.0000.0003.00-00 0x0000020c 0xd59e 322 68 0/0/0 SOURCE 0000.0000.0003.00 NLPID IPV4 AREA ADDR 10 INTF ADDR 192.168.2.1 NBR ID 0000.0000.0003.01 COST: 10 IP-Internal 192.168.2.0 255.255.255.0 COST: 10 0000.0000.0003.01-00 0x0000007e 0xcc3f 322 55 0/0/0 SOURCE 0000.0000.0003.01 NLPID IPV4 NBR ID 0000.0000.0003.00 COST: 0 SOURCE 0000.0000.0002.01 NLPID IPV4 NBR ID 0000.0000.0002.00 COST: 0 NBR ID 0000.0000.0001.00 COST: 0 0000.0000.0003.00-00 0x0000020c 0xd59e 322 68 0/0/0 SOURCE 0000.0000.0003.00

NLPID IPV4 AREA ADDR 10 INTF ADDR 192.168.2.1 NBR ID 0000.0000.0003.01 COST: 10 IP-Internal 192.168.2.0 255.255.255.0 COST: 10 0000.0000.0003.01-00 0x0000007e 0xcc3f 322 55 0/0/0 SOURCE 0000.0000.0003.01 NLPID IPV4 NBR ID 0000.0000.0003.00 COST: 0 NBR ID 0000.0000.0002.00 COST: 0 Total LSP(s): 5
*(In TLV)-Leaking Route, *(By LSPID)-Self LSP, +-Self LSP(Extended), ATT-Attached, P-Partition, OL-Overload配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 10 \# keychain huawei mode absolute receive-tolerance 10 \# key-id 1 algorithm hmac-sha-256 key-string cipher %+%#)teP2/_7j#@>|r-p:jgDgyKC%=80dRNA,;Cjwwv ~ %+%# send-time 12:00 2019-12-10 to 18:00 2019-12-10 receive-time 12:00 2019-12-10 to 18:00 2019-12-10 default send-key-id \# isis 1 is-level level-1 network-entity 10.0000.0000.0001.00 \# interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# interface vlanif 10 ip address 192.168.1.1 255.255.255.0 isis enable 1 isis authentication-mode keychain huawei \# return
● DeviceB \# sysname DeviceB \# vlan batch 10 20 \# keychain huawei mode absolute receive-tolerance 10 \# key-id 1 algorithm hmac-sha-256 key-string cipher %+%#$V_<R'XnL6F&H`P2DLn#IE7-+' ks9 \acM<OSf)%+%# ~ ~ send-time 12:00 2019-12-10 to 18:00 2019-12-10 receive-time 12:00 2019-12-10 to 18:00 2019-12-10 default send-key-id \# isis 1 is-level level-1 network-entity 10.0000.0000.0002.00 \#

interface 10GE1/0/1 port link-type trunk port trunk allow-pass vlan 10 \# interface vlanif 10 ip address 192.168.1.2 255.255.255.0 isis enable 1 isis authentication-mode keychain huawei \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 20 \# interface vlanif 20 ip address 192.168.2.2 255.255.255.0 isis enable 1 isis authentication-mode keychain huawei \# return
● DeviceC \# sysname DeviceC \# vlan batch 20 \# keychain huawei mode absolute receive-tolerance 10 \# key-id 1 algorithm hmac-sha-256 key-string cipher %+%#v@>@B\eP.Ruug(%b,;fS!5}]GV:rLU3(]U'zd9|>%+%# send-time 12:00 2019-12-10 to 18:00 2019-12-10 receive-time 12:00 2019-12-10 to 18:00 2019-12-10 default send-key-id \# isis 1 is-level level-1 network-entity 10.0000.0000.0003.00 \# interface 10GE1/0/2 port link-type trunk port trunk allow-pass vlan 20 \# interface vlanif 20 ip address 192.168.2.1 255.255.255.0 isis enable 1 isis authentication-mode keychain huawei \# return

#### 15.6.2 举例：配置BGP使用Keychain认证

组网需求如图15-7所示，网络中DeviceA和DeviceB通过BGP实现互通。
为了确保BGP连接的稳定和安全，配置Keychain为BGP提供动态的安全认证服务。
图 15-7 Keychain 组网图说明本例中interface1代表Vlanif1。

配置本例，需要准备以下数据：
● Keychain名称
● Keychain的接收容忍时间
● TCP增强认证选项中的类型值（TCP Kind）和TCP认证的算法ID（TCP algorithm- id）
● Keychain中Key的ID
● Key的认证算法和认证密钥（加密字符串）
● Key的活跃发送时间和活跃接收时间配置注意事项
● 配置本例前，需要提前完成 NTP 和 BGP 配置。
● DeviceA和DeviceB配置的Keychain名称需要相同。
● DeviceA和DeviceB配置的Keychain的时间模式需要相同。
● DeviceA和DeviceB配置的Keychain的Key的ID需要相同。配置多个Key时，两端都需要配置相同ID的多个Key。
● 对于同一个Key，DeviceA和DeviceB配置的认证算法和认证密钥（加密字符串）
需要相同。
● 对于同一个Key，DeviceA和DeviceB配置的活跃发送时间和接收活跃时间需要对应。例如，DeviceB的活跃接收时间至少需要包含DeviceA的活跃发送时间，以避免丢包。反之亦然。
● 如果Keychain中配置多个Key时，其中只能有1个Key配置为缺省发送key。
配置思路
1. 创建Keychain。
2. 配置Keychain中的Key，以及Key-id的认证算法为hmac-sha-256。
3. 配置BGP使用Keychain认证。
操作步骤步骤1 创建Keychain。
\# 配置DeviceA。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] keychain huawei mode absolute [DeviceA-keychain-huawei] receive-tolerance 10 [DeviceA-keychain-huawei] tcp-kind 182 [DeviceA-keychain-huawei] tcp-algorithm-id hmac-sha-256 17 [DeviceA-keychain-huawei] quit \# 配置DeviceB。
<HUAWEI> system-view [HUAWEI] sysname DeviceB

[DeviceB] keychain huawei mode absolute [DeviceB-keychain-huawei] receive-tolerance 10 [DeviceB-keychain-huawei] tcp-kind 182 [DeviceB-keychain-huawei] tcp-algorithm-id hmac-sha-256 17 [DeviceB-keychain-huawei] quit步骤2 配置Keychain中的Key。
配置DeviceA。
\# [DeviceA] keychain huawei [DeviceA-keychain-huawei] key-id 1 [DeviceA-keychain-huawei-keyid-1] algorithm hmac-sha-256 [DeviceA-keychain-huawei-keyid-1] key-string cipher YsHsjx_202207 [DeviceA-keychain-huawei-keyid-1] send-time 12:00 2019-12-10 to 15:00 2019-12-10 [DeviceA-keychain-huawei-keyid-1] receive-time 12:00 2019-12-10 to 15:00 2019-12-10 [DeviceA-keychain-huawei-keyid-1] default send-key-id [DeviceA-keychain-huawei-keyid-1] quit [DeviceA-keychain-huawei] key-id 2 [DeviceA-keychain-huawei-keyid-2] algorithm hmac-sha-256 [DeviceA-keychain-huawei-keyid-2] key-string cipher YsHsjx_202206 [DeviceA-keychain-huawei-keyid-2] send-time 15:05 2019-12-10 to 18:00 2019-12-10 [DeviceA-keychain-huawei-keyid-2] receive-time 15:05 2019-12-10 to 18:00 2019-12-10 [DeviceA-keychain-huawei-keyid-2] quit [DeviceA-keychain-huawei] quit \# 配置DeviceB。
[DeviceB] keychain huawei [DeviceB-keychain-huawei] key-id 1 [DeviceB-keychain-huawei-keyid-1] algorithm hmac-sha-256 [DeviceB-keychain-huawei-keyid-1] key-string cipher YsHsjx_202207 [DeviceB-keychain-huawei-keyid-1] send-time 12:00 2019-12-10 to 15:00 2019-12-10 [DeviceB-keychain-huawei-keyid-1] receive-time 12:00 2019-12-10 to 15:00 2019-12-10 [DeviceB-keychain-huawei-keyid-1] default send-key-id [DeviceB-keychain-huawei-keyid-1] quit [DeviceB-keychain-huawei] key-id 2 [DeviceB-keychain-huawei-keyid-2] algorithm hmac-sha-256 [DeviceB-keychain-huawei-keyid-2] key-string cipher YsHsjx_202206 [DeviceB-keychain-huawei-keyid-2] send-time 15:05 2019-12-10 to 18:00 2019-12-10 [DeviceB-keychain-huawei-keyid-2] receive-time 15:05 2019-12-10 to 18:00 2019-12-10 [DeviceB-keychain-huawei-keyid-2] quit [DeviceB-keychain-huawei] quit步骤3 配置BGP使用Keychain认证。
\# 配置DeviceA。
[DeviceA] vlan batch 1 [DeviceA] interface vlanif 1 [DeviceA-Vlanif1] ip address 192.168.1.1 24 [DeviceA-Vlanif1] quit [DeviceA] bgp 1 [DeviceA-bgp] router-id 1.1.1.1 [DeviceA-bgp] peer 192.168.1.2 as-number 1 [DeviceA-bgp] peer 192.168.1.2 keychain huawei [DeviceA-bgp] quit [DeviceA] quit \# 配置DeviceB。
[DeviceA] vlan batch 2 [DeviceB] interface vlanif 2 [DeviceB-Vlanif2] ip address 192.168.1.2 24 [DeviceB-Vlanif2] quit [DeviceB] bgp 1 [DeviceB-bgp] router-id 2.2.2.2 [DeviceB-bgp] peer 192.168.1.1 as-number 1 [DeviceB-bgp] peer 192.168.1.1 keychain huawei

[DeviceB-bgp] quit [DeviceB] quit
----结束检查配置结果以DeviceA为例查看BGP使用Keychain认证是否配置成功。
● 执行display keychain keychain-name，查看当前处于Active状态的Key-id。
<DeviceA> display keychain huawei Keychain Information:
---------------------- Keychain Name : huawei Timer Mode : Absolute Receive Tolerance(min) : 10 Digest Length : 32 Time Zone : LMT TCP Kind : 182 TCP Algorithm IDs :
HMAC-MD5 : 5 HMAC-SHA1-12 : 2 HMAC-SHA1-20 : 6 MD5 : 3 SHA1 : 4 HMAC-SHA-256 : 17 SHA-256 : 8 SM3 : 9 HMAC-SHA-384 : 11 HMAC-SHA-512 : 12 Number of Key ID : 2 Active Send Key ID : 1 Active Receive Key ID : 01 Default send Key ID : 1 Key ID Information:
---------------------- Key ID : 1 Key string : ****** Algorithm : HMAC-SHA-256 SEND TIMER :
Start time : 2019-12-10 12:00 End time : 2019-12-10 15:00 Status : Active RECEIVE TIMER :
Start time : 2019-12-10 12:00 End time : 2019-12-10 15:00 Status : Active Key ID : 2 Key string : ****** Algorithm : HMAC-SHA-256 SEND TIMER :
Start time : 2019-12-10 15:05 End time : 2019-12-10 18:00 Status : Inactive RECEIVE TIMER :
Start time : 2019-12-10 15:05 End time : 2019-12-10 18:00 Status : Inactive
● 执行display bgp peer ipv4-address verbose查看BGP对等体已配置的认证类型是Keychain(huawei)。
<DeviceA> display bgp peer 192.168.1.2 verbose BGP Peer is 192.168.1.2, remote AS 1 Type: IBGP link BGP version 4, Remote router ID 2.2.2.2 Update-group ID: 3

BGP current state: Established, Up for 00h27m26s BGP current event: RecvKeepalive BGP last state: OpenConfirm BGP Peer Up count: 2 Received total routes: 0 Received active routes total: 0 Advertised total routes: 0 Port: Local - 58168 Remote - 179 Configured: Connect-retry Time: 32 sec Configured: Min Hold Time: 0 sec Configured: Active Hold Time: 180 sec Keepalive Time:60 sec Received : Active Hold Time: 180 sec Negotiated: Active Hold Time: 180 sec Keepalive Time:60 sec Peer optional capabilities:
Peer supports bgp multi-protocol extension Peer supports bgp route refresh capability Peer supports bgp 4-byte-as capability Address family IPv4 Unicast: advertised and received Received: Total 34 messages Update messages 1 Open messages 1 KeepAlive messages 32 Notification messages 0 Refresh messages 0 Sent: Total 33 messages Update messages 1 Open messages 1 KeepAlive messages 31 Notification messages 0 Refresh messages 0 Authentication type configured: Keychain(huawei)
Last keepalive received: 2019-12-10 10:12:29+00:00 Last keepalive sent : 2019-12-10 10:12:04+00:00 Last update received: 2019-12-10 09:45:14+00:00 Last update sent : 2019-12-10 09:45:14+00:00 No refresh received since peer has been configured No refresh sent since peer has been configured Minimum route advertisement interval is 15 seconds Optional capabilities:
Route refresh capability has been enabled 4-byte-as capability has been enabled Peer Preferred Value: 0 Routing policy configured:
No routing policy is configured配置脚本
● DeviceA \# sysname DeviceA \# vlan batch 1 \# keychain huawei mode absolute receive-tolerance 10 tcp-kind 182 tcp-algorithm-id hmac-sha-256 17 \# key-id 1 algorithm hmac-sha-256 key-string cipher %+%#1h29-c>>[H,XTu>Q}##;"}JOQOK#c>TD6> d-BaJ%+%# ~ send-time 12:00 2019-12-10 to 15:00 2019-12-10 receive-time 12:00 2019-12-10 to 15:00 2019-12-10 default send-key-id \# key-id 2 algorithm hmac-sha-256 key-string cipher %+%#^<Sn.IK2iK'N%[VnMhv-I)|C4d<K$F$a.6%jEN@K%+%# send-time 15:05 2019-12-10 to 18:00 2019-12-10

receive-time 15:05 2019-12-10 to 18:00 2019-12-10 \# interface vlanif 1 ip address 192.168.1.1 255.255.255.0 \# bgp 1 router-id 1.1.1.1 peer 192.168.1.2 as-number 1 peer 192.168.1.2 keychain huawei \# ipv4-family unicast peer 192.168.1.2 enable \# return
● DeviceB \# sysname DeviceB \# vlan batch 2 \# keychain huawei mode absolute receive-tolerance 10 tcp-kind 182 tcp-algorithm-id hmac-sha-256 17 \# key-id 1 algorithm hmac-sha-256 key-string cipher %+%#p8cb/;OMFES0Wx@PY^"Ka{6q2MB;oG|[ZO-_]u}&%+%# send-time 12:00 2019-12-10 to 15:00 2019-12-10 receive-time 12:00 2019-12-10 to 15:00 2019-12-10 default send-key-id \# key-id 2 algorithm hmac-sha-256 key-string cipher %+%#&Yq4=s*P:L<"8iG-|o1ZB*Qi0qCn%N{Y3a&Z-zuD%+%# send-time 15:05 2019-12-10 to 18:00 2019-12-10 receive-time 15:05 2019-12-10 to 18:00 2019-12-10 \# interface vlanif 2 ip address 192.168.1.2 255.255.255.0 \# bgp 1 router-id 2.2.2.2 peer 192.168.1.1 as-number 1 peer 192.168.1.1 keychain huawei \# ipv4-family unicast peer 192.168.1.1 enable \# return
