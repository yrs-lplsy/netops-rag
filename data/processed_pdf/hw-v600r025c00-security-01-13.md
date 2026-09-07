# S1700, S5700, S6700 V600R025C00 配置指南-安全 01-13 SSH配置

## 13 SSH配置

13 SSH 配置背景信息说明SSH2.0版本中，使用CBC（Cipher Block Chaining）模式的对称加密算法可能受到明文恢复攻击而泄露加密传输的内容，因此，在SSH2.0中不建议使用CBC模式对数据加密。

### 13.1 SSH简介

13.2 SSH配置注意事项
13.3 SSH工作过程
13.4 SSH缺省配置
13.5 配置SSH服务器
13.6 配置SSH客户端
13.7 SSH的常见配置错误
13.1 SSH 简介
定义
SSH是Secure Shell（安全外壳）的简称，是一种在不安全的网络环境中，通过加密机
制和认证机制，实现安全的访问以及文件传输等业务的网络安全协议。
SSH协议有SSH1.X（SSH2.0之前的版本）和SSH2.0版本。SSH2.0协议相比SSH1.X协议
来说，在结构上做了扩展，可以支持更多的认证方法和密钥交换方法，同时提高了服
务能力（如SFTP）。
目的
Telnet 缺少安全的认证方式，而且传输过程采用 TCP 进行明文传输，存在很大的安全隐
患。单纯提供Telnet服务容易招致DoS（Denial of Service）、主机IP地址欺骗、路由
欺骗等恶意攻击。随着人们对网络安全的重视，传统的Telnet通过明文传送密码和数据
的方式，已经慢慢不被人接受。SSH是一个网络安全协议，通过对网络数据的加密，

解决了这个问题。它在一个不安全的网络环境中，提供了安全的登录和其他安全网络服务。
SSH通过TCP进行数据交互，它在TCP之上构建了一个安全的通道。另外SSH服务除了支持标准端口22外，还支持其他服务端口，以防止受到非法攻击。

### 13.2 SSH配置注意事项

License 依赖SSH无需License许可即可使用。
硬件依赖表 13-1 支持本特性的硬件

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

特性限制表 13-2 本特性的使用限制

| 特性 | 特性限制 |
|---|---|
| SSH业务 | 当设备作为Stelnet服务端时，在登录过程中强制修改密码时，退格键无法用于删除旧密码、新密码以及确认密码字段的输入内容。 |
| SSH业务 | 设备作为SFTP服务器时，上传或下载操作的文件名不支持中文字符。 |
| SSH安全 | 出于安全性考虑，不建议使用该特性提供的弱安全算法或者弱安全协议。设备默认自带弱安全算法/协议特性包WEAKEA，如果确实需要使用，请执行命令install feature-software WEAKEA安装弱安全算法/协议特性包WEAKEA。 |

### 13.3 SSH工作过程

本小节以SSH2.0为例介绍SSH工作的过程，具体分为所述的几个阶段。
表 13-3 工作过程

| 阶段 | 说明 |
|---|---|
| 连接建立 | SSH服务器在22号端口侦听客户端的连接请求，在客户端向服务器端发起连接请求后，双方建立一个TCP连接。 |
| 版本协商 | 双方通过版本协商确定最终使用的SSH版本号。 |
| 算法协商 | SSH支持多种算法，双方根据本端和对端支持的算法，协商出最终用于产生会话密钥的密钥交换算法、用于数据信息加密的加密算法、用于进行数字签名和认证的公钥算法，以及用于数据完整性保护的HMAC算法。 |
| 密钥交换 | 双方通过DH（Diffie-Hellman Exchange）交换，动态地生成用于保护数据传输的会话密钥和用来标识该SSH连接的会话ID，并完成客户端对服务器端的身份认证。 |
| 用户认证 | SSH客户端向服务器端发起认证请求，服务器端对客户端进行认证。 |
| 会话请求 | 认证通过后，SSH客户端向服务器端发送会话请求，请求服务器提供某种类型的服务（Stelnet、SFTP或SCP），即请求与服务器建立相应的会话。 |
| 会话交互 | 会话建立后，SSH服务器端和客户端在该会话上进行数据信息的交互。 |

### 13.4 SSH缺省配置

SSH的主要缺省配置如13.4 SSH缺省配置所示。
表 13-4 SSH 缺省配置

| 参数 | 缺省配置 |
|---|---|
| STelnet服务器功能 | 关闭 |
| SSH服务器端口号 | 22 |
| SSH服务器密钥对的更新周期 | 0小时，表示永不更新 |
| SSH连接认证超时时间 | 60秒 |
| SSH连接的认证重试次数 | 3 |
| VTY用户界面的认证方式 | 没有配置认证方式 |
| VTY用户界面所支持的协议 | 支持所有协议类型 |
| SSH用户的认证方式 | 认证方式是空，即不支持任何认证方式 |
| SSH用户的服务方式 | 服务方式是空，即不支持任何服务方式 |
| SSH服务器为用户分配公钥 | 没有为用户分配公钥 |
| 用户级别 | VTY用户界面对应的默认命令访问级别是 0 |
| SSH客户端首次登录 | 关闭 |
| SSH客户端给SSH服务器分配RSA、DSA 或ECC公钥 | 没有为SSH服务器分配RSA、DSA或ECC 公钥 |

### 13.5 配置SSH服务器

#### 13.5.1 配置SSH服务器功能及参数

背景信息配置SSH服务器功能及参数包括配置服务器本地密钥对生成、SSH服务器功能的开启以及服务器参数的配置：端口号、密钥对更新时间、SSH认证超时时间或SSH认证重试次数等。

说明为了保证更好的安全性，建议定期修改密钥。
●
● 为了保证SSH算法协商成功，SSH服务器配置的密钥交换算法、加密算法、公钥算法和HMAC算法，SSH客户端也必须要支持，否则会导致协商失败。
● SSH服务器不支持兼容SSH1.X版本。
● 为了保证更好的安全性，建议不要使用小于3072位的RSA算法作为SSH用户的认证方式，建议您使用更安全的ECC认证算法。
操作步骤步骤1 进入系统视图。
system-view步骤2 生成本地密钥对。
方式一：生成本地RSA、DSA或ECC密钥对。
● 生成本地RSA密钥对。
rsa local-key-pair create
● 生成DSA密钥对。
dsa local-key-pair create
● 生成ECC密钥对。
ecc local-key-pair create密钥对生成后，可以执行display public、display rsa local-key-pair dsa local-key- pair public或display ecc local-key-pair public命令查看本地密钥对中RSA、DSA或ECC的公钥信息。
如果用户确认无需继续使用本地的RSA、DSA或者ECC密钥对，可以通过命令rsa local-key-pair destroy、dsa local-key-pair destroy或ecc local-key-pair destroy销毁本地所有的RSA、DSA或者ECC密钥。执行该命令后，设备上用于存放对应密钥的文件将被清空，请用户谨慎使用。
方式二：生成带标签的SM2、RSA、DSA或ECC密钥对。
说明方式二可以最多生成20对密钥对，用户可以在不同时期使用不同的密钥对，更好地确保了通信的安全性。设备最多可生成RSA、DSA或ECC的密钥对数，可以通过rsa key-pair maximum、dsa key- pair maximum和ecc key-pair maximum命令配置。
1. 生成带标签的RSA、DSA、SM2或ECC密钥对。
– 生成带标签的RSA密钥对。
rsa key-pair label label-name [ modulus modulus-bits ]
– 生成带标签的DSA密钥对。
dsa key-pair label label-name [ modulus modulus-bits ]
– 生成带标签的ECC密钥对。
ecc key-pair label label-name [ modulus modulus-bits ]
– 生成带标签的SM2密钥对。
sm2 key-pair label label-name
2. 为 SSH 服务器分配主机密钥或者 PKI 证书。
ssh server assign { rsa-host-key key-name | dsa-host-key key-name | ecc-host-key key-name | sm2- host-key key-name | pki key-name }缺省情况下，没有为SSH服务器分配密钥或者PKI证书。

密钥对生成后，可以执行display rsa key-pair [ brief | label label-name ]、display dsa key-pair [ brief | label label-name ]、display ecc key-pair [ brief | label label-name ]、display sm2 key-pair [ brief | label label-name ]命令查看带标签的RSA、DSA、SM2或ECC密钥对信息。
步骤3 使能SSH服务器公钥算法。
ssh server publickey { dsa | ecc | rsa | x509v3-ssh-rsa | rsa_sha2_256 | rsa_sha2_512 | sm2 | x509v3-
* rsa2048-sha256 | x509v3-ecdsa-sha2 | sm2-sm3 }缺省情况下，ECC，RSA_SHA2_256、RSA_SHA2_512公钥算法是开启的。
设备以出厂配置启动时，RSA_SHA2_256、RSA_SHA2_512公钥算法是开启的。
说明命令中的参数dsa、rsa和x509v3-ssh-rsa需要执行命令install feature-software WEAKEA安装弱安全算法/协议特性包后才能使用。
当使用公钥认证登录设备时，SSH服务器支持的公钥算法需要与命令ssh user authentication- type配置SSH用户的认证方式相同，否则用户无法登录设备。
步骤4 使能SSH服务器功能。
● 设备作为STelnet服务器。
stelnet [ ipv4 | ipv6 ] server enable缺省情况下，STelnet服务为关闭状态。
● 设备作为SFTP服务器。
sftp [ ipv4 | ipv6 ] server enable缺省情况下，SFTP服务为关闭状态。
● 设备作为SCP服务器。
scp [ ipv4 | ipv6 ] server enable缺省情况下，SCP服务为关闭状态。
步骤5 配置SSH服务器端口号。
ssh [ ipv4 | ipv6 ] server port port-number缺省情况下，SSH服务器端的端口号是22。
如果配置了新的端口号，SSH服务器端先断开当前已经建立的所有SSH连接，然后使用新的端口号开始尝试连接。这样可以有效防止攻击者对SSH服务标准端口的访问，确保安全性。
步骤6 使能SSH服务器上的keepalive特性。
undo ssh server keepalive disable缺省情况下，SSH服务器上的keepalive特性处于使能状态。
SSH服务器在使能keepalive特性之后，若收到SSH客户端的keepalive报文之后，会进行响应。这样防止在SSH客户端收不到keepalive响应报文时断开与SSH服务器的连接，避免造成客户端重新连接服务器浪费服务器资源。
步骤7 （可选）配置SSH服务器的扩展属性。
配置SSH服务器端的密钥交换算法列表。
1.
ssh server key-exchange { dh_group_exchange_sha256 | dh_group_exchange_sha1 | dh_group1_sha1 | ecdh_sha2_nistp256 | ecdh_sha2_nistp384 | ecdh_sha2_nistp521 | sm2_kep | dh_group14_sha1 | dh_group16_sha512 | curve25519_sha256 | sm2_sm3 } *缺省情况下，SSH服务器使用dh_group_exchange_sha256、dh_group16_sha512、curve25519_sha256密钥交换算法。

在客户端与服务器协商的过程中，二者对报文传输的密钥交换算法进行协商，服务器端根据客户端发来的密钥交换算法列表与自身的密钥交换算法列表进行对比，选择客户端与自己相匹配的第一个密钥交换算法作为报文传输的密钥交换算法，如果客户端的密钥交换算法列表与服务器端的密钥交换算法列表没有相匹配的算法，则协商失败。
说明
– 为保证更好的安全性，建议使用安全性更高的curve25519_sha256、ecdh_sha2_nistp521、ecdh_sha2_nistp384和ecdh_sha2_nistp256密钥交换算法。
– 命令中的参数dh_group_exchange_sha1、dh_group1_sha1、sm2_kep和dh_group14_sha1，需要执行命令install feature-software WEAKEA安装弱安全算法/协议特性包后才能使用。
2. 配置SSH会话密钥重协商条件。
* ssh server rekey { data-limit data-limit | max-packet max-packet | time minutes }缺省情况下，满足以下三个条件中的至少一个时，SSH服务器即触发密钥重协商：
– 使用当前密钥传输报文总数据量达到1000兆字节。
– 发送和接收的报文总个数达到 2147483648 个。
– SSH连接时长达到60分钟。
为了提高传输安全性，SSH服务器可以启动密钥重协商，如果重协商失败，就会断开SSH连接。
3. 配置与SSH客户端进行Diffie-hellman-group-exchange密钥交换时支持的最小密钥长度。
ssh server dh-exchange min-len min-len缺省情况下，SSH服务器与客户端进行Diffie-hellman-group-exchange密钥交换时，支持的最小密钥长度为3072比特。
说明Diffie-hellman-group-exchange密钥交换算法的最小长度小于等于2048比特时，存在安全风险，需要执行命令install feature-software WEAKEA安装弱安全算法/协议特性包（WEAKEA）后才能使用。建议将最小长度设置为3072bits。此命令对IPv4和IPv6均生效。
4. 配置SSH服务器端的加密算法。
ssh server cipher { des_cbc | 3des_cbc | aes128_cbc | aes256_cbc | aes128_ctr | aes256_ctr | arcfour128 | arcfour256 | aes192_cbc | aes192_ctr | aes128_gcm | aes256_gcm | blowfish_cbc |
* sm4_cbc | sm4_gcm | sm4_ctr }缺省情况下， SSH 服务器使用的加密算法为 AES256_GCM 、 AES128_GCM 、AES256_CTR、AES192_CTR、AES128_CTR加密算法。
说明
– 为保证更好的安全性，建议使用以下安全性更高的加密算法：AES256_GCM、AES128_GCM、AES256_CTR、AES192_CTR、AES128_CTR。
– 命令中的参数blowfish_cbc、des_cbc、3des_cbc、aes128_cbc、aes256_cbc、arcfour128、arcfour256、aes192_cbc和sm4_cbc，需要执行命令install feature- software WEAKEA安装弱安全算法/协议特性包后才能使用。
5. 配置SSH服务器上的校验算法。
ssh server hmac { md5 | md5_96 | sha1 | sha1_96 | sha2_256 | sha2_256_96 | sha2_512 | sm3 | sha2_256_etm | sha2_512_etm } *缺省情况下，SSH服务器使用的HMAC认证算法为SHA2_512_ETM、SHA2_256_ETM、SHA2_512和SHA2_256。

设备以出厂配置启动时，SSH服务器使用的HMAC认证算法为SHA2_512、SHA2_256。
说明
– 为保证更好的安全性，建议使用以下安全性更高的HMAC算法：SHA2_512_ETM、SHA2_256_ETM、SHA2_512、SHA2_256。
– 命令中的参数md5、md5_96、sha1、sha1_96和sha2_256_96，需要执行命令install feature-software WEAKEA安装弱安全算法/协议特性包后才能使用。
6. 关闭SSH服务端使用不安全算法时的风险提示功能。
ssh server security-banner disable缺省情况下，SSH服务端使用不安全算法时的风险提示功能处于使能状态。
7. 配置SSH认证超时时间。
ssh server timeout seconds缺省情况下，SSH连接认证超时时间是60秒。
当设置的SSH认证超时时间到达后，如果用户还未登录成功，则终止当前连接，确保了安全性。
8. 配置SSH认证重试次数。
ssh server authentication-retries times缺省情况下，SSH连接的认证重试次数是3。
配置SSH认证重试次数用来设置SSH用户请求连接的认证重试次数，防止非法用户登录。
9. 配置访问控制列表。
ssh [ ipv6 ] server acl { acl-number | acl-name }缺省情况下，没有配置访问控制列表。
配置了访问控制列表，可控制哪些客户端能以SSH方式访问本设备。
10. 配置SSH服务器认证时允许使用的RSA最小公钥长度。
ssh server rsa-key min-length min-length-val缺省情况下，SSH服务器允许使用的RSA公钥最小长度是512比特。
步骤8 配置SSH服务器的源接口或源地址。
缺省情况下，未指定SSH服务器端的源接口和IPv4/IPv6源地址。
● 配置SSH服务器的源接口为指定接口。
ssh server-source -i interface-type interface-number缺省情况下，未指定 SSH 服务端的源接口。
● 配置SSH服务器源接口为设备上所有有效接口。
ssh server-source all-interface
● 配置SSH服务端的IPv4源地址。
ssh server-source -a ip-address [ -vpn-instance vpnName ]
● 配置SSH服务器的IPv6源地址。
ssh ipv6 server-source -a ipv6-address [ -vpn-instance vpn-instance-name ]缺省情况下，未指定SSH服务端的源接口和IPv6源地址。
● 配置 SSH 服务器的 IPv6 源接口为所有有效接口。
ssh ipv6 server-source all-interface

说明配置ssh server-source all-interface或ssh ipv6 server-source all-interface命令后，将不会指定SSH服务器的源接口，用户可从所有有效接口登录，增加系统安全风险，建议用户谨慎使用。
步骤9 配置单个IP地址连接SSH服务器的最大连接数。
ssh server ip-limit-session limit-session-num缺省情况下，单个IP地址连接SSH服务器的最大连接数是256。
步骤10 开启SSH服务器的键盘交互认证方式。
ssh server authentication-type keyboard-interactive enable缺省情况下，SSH服务器的键盘交互认证方式已开启。
使用口令卡认证方式的SSH用户登录，必须开启键盘交互认证方式。
步骤11 （可选）使能SSH服务器上的客户端IP地址锁定功能。
undo ssh server ip-block disable缺省情况下， SSH 服务器上的客户端 IP 地址锁定功能处于使能状态。
● 如果SSH服务器上的客户端IP地址锁定功能处于使能状态，则被锁定的客户端IP地址不能被认证通过，同时会在display ssh server ip-block list命令回显中显示被锁定的客户端IP地址。
● 如果SSH服务器上的客户端IP地址锁定功能处于去使能状态，则display ssh server ip-block list命令回显中会把先前锁定的客户端IP地址记录删除，新的认证失败的客户端IP地址也不会被记录显示。
说明在SSH连接中，如果用户在5分钟内连续6次认证失败，则IP地址将会被锁定5分钟，可以通过执行命令activate ssh server ip-block ip-address ip-address [ vpn-instance vpn-name ]提前对被锁定的IP地址进行解锁。
步骤12 （可选）配置在一定时间内通过SSH登录服务器失败次数的告警上报门限和告警恢复门限。
ssh server login-failed threshold-alarm upper-limit report-times lower-limit resume-times period period- time缺省情况下，在5分钟内发生30次或30次以上次数登录失败，产生告警；在5分钟内登录失败次数小于20，取消告警。
步骤 13 （可选）配置 SSH 协议报文的 DSCP 优先级。
ssh server dscp value缺省情况下，SSH协议报文的DSCP优先级值为48。
步骤14 （可选）使能SSH服务器的本地端口转发服务。
ssh server tcp forwarding enable缺省情况下，SSH服务器的本地端口转发服务没有使能。
----结束查询配置结果
● 执行display dsa peer-public-key命令，查看DSA公共密钥的详细信息。

● 执行display ecc peer-public-key命令，查看ECC公共密钥的详细信息。
执行display peer-public-key命令，查看RSA公共密钥的详细信息。
● rsa
● 执行display sm2 peer-public-key命令，查看SM2公共密钥的详细信息。
● 执行display sftp client命令，查看SFTP客户端的各项配置信息。

#### 13.5.2 配置VTY用户界面支持SSH协议

背景信息在通过SSH方式登录设备前，需要配置登录时采用的VTY用户界面，使其支持SSH协议。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入VTY用户界面视图。
user-interface vty first-ui-number [ last-ui-number ]缺省情况下，没有进入任何用户界面视图。
步骤3 配置VTY用户界面的认证方式为AAA。
authentication-mode aaa缺省情况下，VTY用户界面没有验证方式。
如果配置用户界面支持的协议是SSH，必须设置VTY用户界面认证方式为AAA认证，否则protocol inbound ssh将不能配置成功。
步骤4 配置VTY用户界面支持SSH协议。
protocol inbound { all | ssh }缺省情况下，用户界面支持所有协议类型，包括SSH。
----结束

#### 13.5.3 配置SSH用户

背景信息配置SSH用户包括创建SSH用户和配置SSH用户的认证方式，设备支持的认证方式包括RSA、password、password-rsa、DSA、password-dsa、ECC、password-ecc、password-x509v3-rsa、x509v3-rsa、sm2、password-sm2、password-x509v3- ecdsa-sha2、password-sm2-sm3和all。其中：
● password-rsa认证需要同时满足password认证和RSA认证。
● password-dsa认证需要同时满足password认证和DSA认证。
● password-ecc认证需要同时满足password认证和ECC认证。
password-x509v3-rsa认证需要同时满足password认证和X509V3-SSH-RSA认证。
●
● password-sm2需要同时满足password认证和SM2认证。
● password-x509v3-ecdsa-sha2指定SSH用户认证方式为password和X509V3- ECDSA-SHA2两种认证。

● password-sm2-sm3指定需要经过password和SM2-SM3两种认证。
● all认证是指所有认证方式满足其中一种即可。
说明
为了保证更好的安全性，建议不要使用小于3072位的RSA算法作为SSH用户的认证方式，建议您
使用更安全的ECC认证算法。
操作步骤
步骤1 进入系统视图。
system-view
步骤2 创建SSH用户。
ssh user user-name
缺省情况下，没有创建SSH用户。
步骤3 配置SSH用户的认证方式。
ssh user user-name authentication-type { password | rsa | password-rsa | all | dsa | password-dsa | ecc |
password-ecc | sm2 | password-sm2 | password-x509v3-rsa | x509v3-rsa | password-x509v3-ecdsa-sha2
| x509v3-ecdsa-sha2 | sm2-sm3 | password-sm2-sm3 }
缺省情况下，SSH用户的认证方式是空，即不支持任何认证方式。
如果没有使用ssh user user-name命令配置相应的SSH用户，则可以直接执行ssh
authentication-type default password命令为用户配置SSH认证缺省采用密码认
证，此时只需再配置AAA用户即可，在用户数量比较多时，对用户使用缺省的密码认
证方式可以简化配置。
● password认证依靠AAA实现，当用户使用password、password-rsa、password-
x509v3-rsa、password-dsa或password-ecc、password-sm2、password-
x509v3-ecdsa-sha2、password-sm2-sm3认证方式登录设备时，需要在AAA视图
下创建同名的本地用户。
● 如果SSH用户使用RSA、DSA、SM2或ECC认证，需要在服务器端和客户端都需要
生成本地RSA、DSA、SM2或ECC密钥对（请参见13.5.1 配置SSH服务器功能及参
数），并且服务器端和客户端都需要将对方的公钥配置到本地。
根据上面配置的认证方式，进行选择配置，具体操作见表13-5。
表 13-5 不同认证方式的配置

| 认证方式 | 配置说明 |
|---|---|
| password认证 | 创建AAA同名用户，请根据表13-6进行配置。 |
| RSA、DSA、ECC、SM2或SM2-SM3认证 | 生成本地RSA、DSA、SM2、ECC密钥对，请根据表13-7进行配置。使用SM2-SM3认证方式时，配套使用的密钥对也为SM2类型，需要执行sm2 key-pair label label-name命令生成本地密钥对。 |

| 认证方式 | 配置说明 |
|---|---|
| password-rsa、password-dsa、 password-sm2、password-ecc、 password-sm2-sm3认证 | 创建AAA同名用户并生成本地RSA、 DSA、SM2或ECC密钥对，请根据表13-6 和表13-7进行配置。 |
| x509v3-rsa、x509v3-ecdsa-sha2 | 对SSH用户绑定PKI域，请根据表13-8进行配置。 |
| password-x509v3-rsa、password- x509v3-ecdsa-sha2 | 创建AAA同名用户并绑定PKI域，请根据表13-6和表13-8进行配置。 |

表 13-6 在 AAA 视图下创建同名的本地用户

| 操作步骤 | 命令 | 说明 |
|---|---|---|
|  | system-view |  |
|  | aaa |  |
|  | local-user user-name password irreversible- cipher password |  |
|  | local-user user-name service-type ssh |  |
|  | local-user user-name privilege level level |  |
|  | quit |  |

表 13-7 配置 SSH 用户的本地 RSA、DSA、SM2 或 ECC 密钥

| 操作步骤 | 命令 | 说明 |
|---|---|---|
|  | system-view |  |

| 操作步骤 | 命令 | 说明 |
|---|---|---|
|  | ssh authorization-type default { aaa | root } |  |
|  | rsa peer-public-key key- name [ encoding-type enc-type ] 或 dsa peer-public-key key-name encoding- type enc-type 或 ecc peer-public-key key- name [ encoding-type enc-type ] 或 sm2 peer-public-key key-name [ encoding- type enc-type ] |  |
|  | public-key-code begin |  |
|  | hex-data |  |

| 操作步骤 | 命令 | 说明 |
|---|---|---|
|  | public-key-code end |  |
|  | peer-public-key end |  |
|  | ssh user user-name assign { rsa-key | dsa- key | ecc-key | sm2-key} key-name |  |

表 13-8 配置对 SSH 用户绑定 PKI 域

| 操作步骤 | 命令 | 说明 |
|---|---|---|
|  | system-view |  |
|  | ssh user user-name assign pki pki-name |  |

步骤4 配置SSH用户的服务方式。
ssh user user-name service-type { all | { sftp | stelnet | snetconf } * }缺省情况下，SSH用户的服务方式是空，即不支持任何服务方式。
步骤 5 （可选）配置 SSH 用户的 SAN/CN 校验。
ssh user user-name cert-verify-san enable缺省情况下，不校验证书中CN（common name）或者SAN（Subject Alternative Name）中是否包含该认证用户的域名。
当配置SSH用户绑定PKI域后，可校验PKI证书中SAN（Subject Alternative Name）或者CN（common name）中是否包含该认证用户的域名，增强安全性。
步骤6 （可选）配置允许SSH用户建立连接的源接口。
ssh user user-name source -i { interface-type interface-num | interface-name }缺省情况下，没有指定允许SSH用户建立连接的源接口。
----结束

#### 13.5.4 应用SSH

背景信息SSH本身只是一种安全协议，SSH策略只有与各种应用关联后才能生效。
操作步骤步骤1 应用SSH策略。设备作为SSH服务器对应的具体应用请参见表13-9。
表 13-9 设备作为 SSH 服务器的主要应用

| SSH策略的主要应用 | 具体应用示例 |
|---|---|
| SSH在Stelnet登录中的应用 | 举例：配置IPv4用户通过STelnet登录设备（RSA认证） |
| SSH在SFTP中的应用 | 举例：配置设备作为SFTP服务器（通过 IPv4） |
| SSH在SCP中的应用 | 配置设备作为SCP服务器 |
| SSH在Netconf中的应用 | 举例：通过使用NETCONF与ncclient通信 |

----结束

### 13.6 配置SSH客户端

#### 13.6.1 配置设备首次连接SSH服务器的方式

背景信息作为客户端的设备首次连接SSH服务器时，因为客户端还没有保存过SSH服务器的公钥或没有绑定相关的 PKI 证书，无法对 SSH 服务器有效性进行检查，这样会导致连接不成功。
用户可以根据需求选择以下一种方式来解决：
● 使能SSH客户端首次登录功能方式：不对SSH服务器进行有效性检查，确保首次连接成功。成功连接后，系统将自动分配并保存公钥，为下次连接时认证使用。
● SSH客户端绑定指定SSH服务器公钥方式：将服务器端产生的公钥直接保存至客户端，保证在首次连接时SSH服务器有效性检查能够通过。
● SSH客户端分配PKI证书方式：将用于与服务器端进行认证的PKI域绑定在客户端上，保证在首次连接时SSH服务器的证书验证合法。
第一种方式配置比较简单，后两种方式配置比较复杂，但是安全性更高。

说明
● 为了保证更好的安全性，建议定期修改密钥。
● 为了保证更好的安全性，建议不要使用小于3072位的RSA算法作为SSH用户的认证方式，建议您使用更安全的ECC认证算法。
操作步骤步骤1 进入系统视图。
system-view步骤2 （可选）生成本地密钥对。
此步骤仅在设备以RSA、DSA或ECC方式登录SSH服务器的时候执行，设备以password方式登录SSH服务器，则无需执行。
● 生成本地RSA密钥对。
rsa local-key-pair create
● 生成DSA密钥对。
dsa local-key-pair create
● 生成ECC密钥对。
ecc local-key-pair create密钥对生成后，可以执行display rsa local-key-pair public、display dsa local-key- pair public或display ecc local-key-pair public命令查看本地密钥对中RSA、DSA或ECC的公钥信息。
如果用户确认无需继续使用本地的DSA或者ECC密钥对，可以通过命令dsa local-key- pair destroy或ecc local-key-pair destroy销毁本地所有的DSA或者ECC密钥。执行该命令后，设备上用于存放对应密钥的文件将被清空，请用户谨慎使用。
步骤3 配置设备首次连接SSH服务器的方式。
● 使能SSH客户端首次登录功能方式ssh client first-time enable缺省情况下，SSH客户端首次登录功能是关闭的。
● SSH客户端绑定指定SSH服务器公钥方式
a. 进入RSA、DSA、ECC、SM2公共密钥视图。
▪进入RSA公共密钥视图。
rsa peer-public-key key-name [ encoding-type enc-type ]▪进入DSA公共密钥视图。
dsa peer-public-key key-name encoding-type enc-type▪进入ECC公共密钥视图。
ecc peer-public-key key-name [ encoding-type enc-type ]▪进入SM2公共密钥视图。
sm2 peer-public-key key-name [ encoding-type enc-type ]
b. 进入公共密钥编辑视图。
public-key-code begin缺省情况下，系统中没有密钥对。
c. 编辑公共密钥。
hex-data

▪键入的公共密钥必须是按公钥格式编码的十六进制字符串，由SSH服务器随机生成。
▪进入公共密钥编辑视图后，即可将服务器上产生的RSA、DSA或ECC公钥输入到客户端。
d. 退出公共密钥编辑视图。
public-key-code end▪如果输入的密钥编码hex-data不合法，执行本步骤后，将无法生成密钥。
▪如果指定的密钥key-name已经被删除，再执行本步骤时，系统会提示：
密钥已经不存在，此时直接退到系统视图。
e. 退出公共密钥视图，回到系统视图。
peer-public-key end为SSH客户端绑定RSA、DSA、ECC或SM2公钥。
f.
ssh client peer server-name assign { rsa-key | dsa-key | ecc-key | sm2-key } key-name缺省情况下，没有为SSH客户端分配公钥。
如果 SSH 客户端保存的 SSH 服务器公钥失效，执行命令 undo ssh client peer server-name assign { rsa-key | dsa-key | ecc-key | sm2-key }，取消SSH客户端与RSA、DSA、ECC或SM2公钥的绑定关系，再执行本命令，为SSH客户端重新分配RSA、DSA或ECC公钥。
● SSH客户端绑定用于与SSH服务器进行认证的PKI域或者主机密钥。
ssh client assign { sm2-host-key key-name | pki pki-domain }缺省情况下，没有为SSH客户端绑定PKI域名。
缺省情况下，没有为SSH客户端分配SM2主机密钥。
步骤4 使能SSH客户端公钥算法。
ssh client publickey { dsa | ecc | rsa | sm2 | rsa_sha2_256 | rsa_sha2_512 | x509v3-ssh-rsa | x509v3-
* rsa2048-sha256 | x509v3-ecdsa-sha2 | sm2-sm3 }缺省情况下，ECC、RSA_SHA2_256、RSA_SHA2_512公钥算法是开启的。
以出厂配置启动时，RSA_SHA2_256、RSA_SHA2_512公钥算法是开启的。
执行此命令可以配置使用更安全的公钥算法登录设备，同时拒绝使用其他公钥算法，从而提升设备安全性。推荐使用RSA_SHA2_256或RSA_SHA2_512公钥算法。
● 如果 ssh client first-time enable 命令功能使能，客户端登录服务器时会提示保存服务器公钥，执行保存操作时，SSH客户端会自动根据ssh client publickey命令配置的公钥算法，选择能够与SSH客户端协商成功的公钥算法分配给SSH服务器。
● 如果ssh client first-time enable命令功能关闭，则必须执行ssh client peer assign命令为SSH服务器分配公钥，且分配的公钥算法必须能和ssh client publickey命令配置的公钥算法协商成功。这样SSH客户端对SSH服务器的公钥验证才会通过。
说明命令中的参数dsa、ecc和rsa，需要执行命令install feature-software WEAKEA安装弱安全算法/协议特性包后才能使用。
----结束

查询配置结果
● 执行display dsa peer-public-key命令，查看DSA公共密钥的详细信息。
● 执行display ecc peer-public-key命令，查看ECC公共密钥的详细信息。
● 执行display rsa peer-public-key命令，查看RSA公共密钥的详细信息。
● 执行display sm2 peer-public-key命令，查看SM2公共密钥的详细信息。
● 执行display sftp client命令，查看SFTP客户端的各项配置信息。

#### 13.6.2 配置SSH客户端参数

背景信息配置SSH客户端参数包括配置SSH客户端发送keepalive报文的时间间隔和SSH客户端发送的keepalive报文的最大数目等。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置SSH客户端发送keepalive报文的时间间隔。
ssh client keepalive-interval seconds缺省情况下，SSH客户端发送keepalive报文的时间间隔为0秒，即不发送keepalive报文。
如果设置发送报文的时间间隔是0秒，那么配置的最大keepalive报文数量将无效。
如果SSH客户端在周期内没有收到来自服务器的任何数据，客户端则在周期之后发送keepalive报文给服务器，直到达到配置的最大数目。如果客户端收不到服务器的keepalive的响应报文，它就会断开与服务器的连接。
步骤3 配置SSH客户端发送的keepalive报文的最大数目。
ssh client keepalive-maxcount count缺省情况下，SSH客户端发送的keepalive报文的最大数目为3。
如果SSH客户端在周期内没有收到来自服务器的任何数据，客户端则在周期之后发送keepalive报文给服务器，直到达到配置的最大数目。如果客户端收不到服务器的keepalive的响应报文，它就会断开与服务器的连接。
步骤4 （可选）配置SSH客户端上的密钥交换算法列表。
ssh client key-exchange { dh_group_exchange_sha256 | dh_group_exchange_sha1 | dh_group1_sha1 | ecdh_sha2_nistp256 | ecdh_sha2_nistp384 | ecdh_sha2_nistp521 | sm2_kep | dh_group14_sha1 |
* dh_group16_sha512 | curve25519_sha256 | sm2_sm3 }缺省情况下，当设备加载配置文件启动时，且配置文件中不存在ssh client key-exchange的配置时，SSH客户端默认使用dh_group_exchange_sha256，dh_group16_sha512，curve25519_sha256 密钥交换算法。
设备以出厂配置启动时，SSH服务器默认使用dh_group_exchange_sha256，dh_group16_sha512，curve25519_sha256密钥交换算法。

说明
● 为保证更好的安全性，建议使用安全性更高的curve25519_sha256、ecdh_sha2_nistp521、ecdh_sha2_nistp384和ecdh_sha2_nistp256密钥交换算法。
● 命令中的参数dh_group_exchange_sha1、dh_group1_sha1、sm2_kep和dh_group14_sha1，需要执行命令install feature-software WEAKEA安装弱安全算法/协议特性包后才能使用。
步骤5 （可选）配置SSH会话密钥重协商条件。
ssh client rekey { data-limit data-limit | max-packet max-packet | time minutes } *为了提高传输安全性，SSH客户端可以启动密钥重协商，如果重协商失败，就会断开SSH连接。缺省情况下，满足以下三个条件中的至少一个时，SSH客户端即触发密钥重协商：
● 使用当前密钥传输报文总数据量达到1000兆字节。
● 发送和接收的报文总个数达到2147483648个。
● SSH连接时长达到60分钟。
步骤6 （可选）配置SSH客户端的加密算法列表。
ssh client cipher { des_cbc | 3des_cbc | aes128_cbc | aes256_cbc | aes128_ctr | aes256_ctr | arcfour128 |
* arcfour256 | aes192_cbc | aes192_ctr | aes128_gcm | aes256_gcm | sm4_cbc | sm4_gcm | sm4_ctr }缺省情况下，
● 设备以空配置启动时，SSH客户端使用的加密算法为：AES256_GCM、AES128_GCM、AES256_CTR、AES192_CTR、AES128_CTR加密算法。
● 当设备加载配置文件启动时，且配置文件中不存在ssh client cipher的配置时，SSH客户端使用的加密算法为：AES128_CTR、AES256_CTR、AES192_CTR、AES128_GCM、AES256_GCM加密算法。
说明
● 为保证更好的安全性，建议使用以下安全性更高的加密算法：AES256_GCM、AES128_GCM、AES256_CTR、AES192_CTR、AES128_CTR。
● 命令中的参数des_cbc、3des_cbc、aes128_cbc、aes256_cbc、arcfour128、arcfour256、aes192_cbc和sm4_cbc，需要执行命令install feature-software WEAKEA安装弱安全算法/协议特性包后才能使用。
步骤7 （可选）配置SSH客户端上的校验算法列表。
ssh client hmac { md5 | md5_96 | sha1 | sha1_96 | sha2_256 | sha2_256_96 | sha2_512 | sm3 | sha2_256_etm | sha2_512_etm } *缺省情况下，
● 设备以出厂配置启动时，SSH客户端支持的HMAC认证算法为SHA2_512和SHA2_256。
● 当设备加载配置文件启动时，且配置文件中不存在ssh client hmac的配置时，SSH客户端支持的HMAC认证算法为SHA2_512、SHA2_256、SHA2_256_ETM和SHA2_512_ETM。
说明
● 为保证更好的安全性，建议使用以下安全性更高的 HMAC 算法： SHA2_512_ETM 、SHA2_256_ETM、SHA2_256、SHA2_512。
● 命令中的参数md5、md5_96、sha1、sha1_96和sha2_256_96，需要执行命令install feature-software WEAKEA安装弱安全算法/协议特性包后才能使用。

步骤8 （可选）配置SSH协议报文的DSCP优先级。
ssh client dscp value缺省情况下，SSH协议报文的DSCP优先级值为48。
----结束

#### 13.6.3 应用SSH

背景信息SSH本身只是一种安全协议，SSH策略只有与各种应用关联后才能生效。
操作步骤步骤1 应用SSH策略。设备作为SSH客户端对应的具体应用请参见表13-10。
表 13-10 设备作为 SSH 客户端的主要应用

| SSH策略的主要应用 | 具体应用示例 |
|---|---|
| SSH在Stelnet登录中的应用 | 举例：配置设备作为STelnet客户端登录其他设备（AAA本地认证和RSA认证） |
| SSH在SFTP中的应用 | 举例：配置设备作为SFTP客户端（password认证和RSA认证方式） |
| SSH在SCP中的应用 | 举例：配置设备作为SCP客户端 |

----结束

### 13.7 SSH的常见配置错误

#### 13.7.1 SSH密钥交换失败

故障现象当设备作为SSH服务器时，第三方客户端软件在连接过程中密钥交换失败，导致SSH连接失败。
可能原因密钥交换成功的前提是协商出客户端和服务器端使用的密钥交换算法、加密算法、公钥算法和HMAC算法，当其中出现一个算法协商失败就会导致密钥交换失败。算法协商失败的原因一般是SSH服务器上没有配置客户端支持的算法。
操作步骤步骤1 通过其他方式登录SSH服务器，具体操作请参见《CLI配置指南-基础配置》中的“登录设备命令行界面配置”。

步骤2 打开SSH服务器的调试信息开关。
system-view info-center enable quit terminal monitor terminal debugging debugging ssh server all步骤3 通过第三方客户端软件连接SSH服务器。
步骤4 在SSH服务器用户终端显示的调试信息中查看客户端支持的算法列表。
将调试信息拷贝到TXT文本中，使用以下正则表达式搜索，获取第三方客户端软件支持的算法列表，具体见表13-11。
表 13-11 查找客户端支持的算法列表

| 算法 | 正则表达式 |
|---|---|
| 密钥交换算法 | SSH protocol packet received.*key_ex |
| 加密算法 | SSH protocol packet received.*ciph_ctos |
| 公钥算法 | SSH protocol packet received.*ser_host_key |
| HMAC校验算法 | SSH protocol packet received.*hmac_ctos |

步骤5 选取客户端和服务器同时支持的密钥交换算法，加密算法，公钥算法和HMAC校验算法，并在SSH服务器上配置。设备作为SSH服务器支持的算法和具体配置方式请参见
13.5.1 配置SSH服务器功能及参数。
----结束
