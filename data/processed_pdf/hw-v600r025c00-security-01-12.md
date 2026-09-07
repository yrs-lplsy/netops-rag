# S1700, S5700, S6700 V600R025C00 配置指南-安全 01-12 SSL配置

## 12 SSL配置

12 SSL 配置

### 12.1 SSL简介

### 12.2 SSL配置注意事项

12.3 SSL 原理描述
12.4 SSL缺省配置
12.5 配置SSL
12.1 SSL 简介
定义
安全套接层SSL（Secure Sockets Layer）协议是在Internet基础上提供的一种保证私密
性的安全协议。SSL能使客户端与服务器之间的通信不被窃听，还能验证通信双方身
份，保证网络上数据传输的安全性。
目的
基于万维网的电子商务和网上银行等新兴应用极大地方便了人们的日常生活，受到人
们的青睐。由于这些应用都需要在网络上进行在线交易，它们对网络通信的安全性提
出了更高的要求。传统的万维网协议HTTP（Hypertext Transfer Protocol ）不具备安
全机制——采用明文的形式传输数据、不能验证通信双方的身份、无法防止传输的数
据被篡改等，导致 HTTP 无法满足电子商务和网上银行等应用的安全性要求。 Netscape
公司提出的安全协议SSL，利用数据加密、身份验证和消息完整性验证机制，为网络上
数据的传输提供安全性保证。SSL可以为HTTP提供安全连接，从而很大程度上改善了
万维网的安全性问题。
虽然SSL设计的初衷是为了解决万维网的安全性问题，但是由于SSL位于应用层和传输
层之间，它可以为任何基于TCP等可靠连接的应用层协议提供安全性保证。
12.2 SSL 配置注意事项
License 依赖
SSL无需License许可即可使用。

硬件依赖表 12-1 支持本特性的硬件

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
| S6730-H-V2 | S6730-H24X6C-V2，S6730-H28X6CZ-V2，S6730- H48X6C-TV2，S6730-H48X6C-V2，S6730- H48X6CZ-V2，S6730-H48Y6C-TV2，S6730- H48Y6C-V2，S6730-H6FX4Y2CZ-V2 |
| S5735I-H-V2 | S5735I-H24U8S4XE-QA-V2，S5735I-H8T2XN- V2，S5735I-H8T4S2XN-V2，S5735I-H8U2XN-V2 |
| S6750-S | S6750-S16X10Y2CZ，S6750-S16X8YZ，S6750- S24T16X8Y2CZ |

| 系列 | 支持产品 |
|---|---|
| S5735S-L3 | S5735S-L24P4S-A3，S5735S-L24P4XE-A3， S5735S-L24PN4XE-A3，S5735S-L24ST4X-A3， S5735S-L24T4S-QA3，S5735S-L24T4X-QA3， S5735S-L24T8J4XE-A3，S5735S-L48P4S-A3， S5735S-L48P4XE-A3，S5735S-L48PN4XE-A3， S5735S-L48S4X-A3，S5735S-L48T4S-A3，S5735S- L48T4XE-A3，S5735S-L8P4X-QA3，S5735S- L8T4X-QA3 |
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
特性限制表 12-2 本特性的使用限制

| 特性 | 特性限制 |
|---|---|
| SSL业务 | SSL加载证书文件（身份证书、CA、吊销列表）存在文件大小限制，文件大小不能超过（包含）50kB。 |

| 特性 | 特性限制 |
|---|---|
| SSL业务 | 配置使用SSL证书时，单个SSL策略最多加载1本证书、4本信任证书、2 个证书吊销列表；配置使用PKI域下证书时，单个SSL策略最多使用1本证书、64本信任证书、64个证书吊销列表。 |
| SSL安全 | 出于安全性考虑，不建议使用该特性提供的弱安全算法或弱安全协议。设备默认自带弱安全算法/协议特性包WEAKEA，如果确实需要使用，请执行命令install feature-software WEAKEA安装弱安全算法/协议特性包WEAKEA。 |
| SSL基础 | 创建SSL策略，DH模数默认值为3072，可配置2048、3072、4096；签名算法默认开启ecdsa-secp256r1-sha256，ecdsa-secp384r1-sha384， ecdsa-secp521r1-sha512，ed25519，ed448，rsa-pss-pss-sha256， rsa-pss-pss-sha384，rsa-pss-pss-sha512，rsa-pss-rsae-sha256，rsa- pss-rsae-sha384，rsa-pss-rsae-sha512，可单独配置，增加安全性。创建SSL策略后，如果是签名算法不匹配或者DH模数长度过长导致的 SSL握手失败，可以通过diffie-hellman modulus命令调整DH模数长度；通过signature algorithm-list命令调整签名算法。 |

### 12.3 SSL原理描述

#### 12.3.1 协议分类

设备支持的SSL协议主要包含两类：TLS和DTLS。
● TLS (Transport Layer Security)：传输层安全协议，是一种安全协议。用于在互联网通信中为TCP连接提供数据加密、身份认证和完整性保护。
● DTLS（Datagram Transport Layer Security）：数据报传输层安全协议， 是TLS协议的UDP适配版本。它为基于UDP的不可靠传输提供类似TLS的安全功能。在保留TLS的核心加密和认证功能的同时，DTLS通过添加显式序列号、Epoch字段和分片控制机制，有效解决了UDP传输中的丢包、乱序及数据报大小限制问题。
TLS和DTLS安全协议的比较如表12-3所示。
表 12-3 TLS 和 DTLS 安全协议的比较

| 差异项 | TLS | DTLS |
|---|---|---|
| 设计目标 | 确保数据在传输过程中的安全性，保障数据的机密性、完整性和身份验证。 | 专为适应UDP的无连接和不可靠特性而设计。 |
| 应用场景 | 适用于需要可靠数据传输的场景，例如网页浏览和电子邮件等。 | 适用于需要低延迟和实时性优先的应用场景，如视频通话、在线游戏等。 |
| 传输层协议 | 基于TCP（可靠传输）。 | 基于UDP（不可靠传输）。 |

| 差异项 | TLS | DTLS |
|---|---|---|
| 记录层头部 | ● Content Type：标识上层协议类型。 ● Version：协议版本。 ● Length：加密后数据的长度（不包括头部）。 | ● Content Type：标识上层协议类型。 ● Version：协议版本。 ● Epoch：密钥阶段标识。 ● Sequence Number：数据包序列号，每个Epoch内独立递增，用于防止重放攻击。重放攻击是一种网络安全攻击方式，攻击者通过截获并重复发送合法的数据包（如身份认证信息、交易请求等），欺骗系统误认为这是新的有效请求，从而绕过验证机制。 ● Length：加密后数据的长度（不包括头部）。 |
| 握手协议层头部 | ● MsgType：握手消息类型。 ● Length：完整握手消息的总长度。 | ● MsgType：握手消息类型。 ● Length：完整握手消息的总长度。 ● Message Sequence：消息序列号，用于确保分片按顺序重组。 ● Fragment Offset：分片偏移量，用于确定分片在原消息中的位置。 ● Fragment Length：当前分片的实际数据长度。 |
| 分片传输 | 依赖TCP传输层处理数据分片。 | 支持分片传输。实现方式如下： ● 发送：大消息（如握手协议）会被拆分为多个分片，每个分片独立加密传输。 ● 接收：通过Epoch + Sequence Number重组分片，并按 Fragment Offset重组排序。 |
| 防重放攻击 | 依赖TCP序列号。 | 支持防重放攻击。通过记录层头部的序列号和Epoch字段，确保每个请求或数据包的唯一性，并保证其时效性，从而有效防止重放攻击。 |
| 消息丢失处理 | 依赖TCP重传机制。 | 支持消息重传。 |
| Cookie机制 | 无 | 握手过程的ClientHello和 ServerHello之间引入了Cookie机制。 |

#### 12.3.2 协议安全机制

SSL协议实现的安全机制包括：
● 身份验证机制：基于证书利用数字签名方法对服务器和客户端进行身份验证，其中客户端的身份验证是可选的。
● 数据传输的机密性：利用对称密钥算法对传输的数据进行加密。
● 消息完整性验证：消息传输过程中使用消息验证码MAC（Message Code）算法来检验消息的完整性。
Authentication身份验证机制客户端必须保证SSL服务器是真实的，以免重要信息被非法窃取。SSL利用数字签名来验证通信双方的身份。
数字签名可以通过非对称密钥算法实现。由于通过私钥加密后的数据只能利用对应的公钥进行解密，因此根据解密是否成功，就可以判断发送者的身份，如同发送者对数据进行了“签名”。例如，Alice使用自己的私钥对一段固定的信息加密后发给Bob，Bob利用Alice的公钥解密，如果解密结果与固定信息相同，那么就能够确认信息的发送者为Alice，这个过程就称为数字签名。
使用数字签名验证身份时，需要确保被验证者的公钥是真实的，否则，非法用户可能会冒充被验证者与验证者通信。通过数字证书来发布用户的公钥，可以保证公钥的真实性。
数字证书（简称证书）是一个包含用户的公钥及其身份信息的文件，证明了用户与公钥的关联。数字证书由CA（Certificate Authority）证书机构签发，CA签发证书的同时会提供证书机构文件，证明CA的身份也保证所颁发证书的真实性。
验证SSL服务器/SSL客户端的身份时，SSL服务器/SSL客户端需要将从CA获取的证书发送给对端，对端利用证书机构文件判断该证书的真实性。如果该证书确实属于SSL服务器/SSL客户端，则对端利用该证书中的公钥验证SSL服务器/SSL客户端的身份。
数据传输的机密性网络上传输的数据很容易被非法用户窃取， SSL 采用在通信双方之间建立加密通道的方法保证数据传输的机密性。
所谓加密通道，是指发送方在发送数据前，使用加密算法和加密密钥对数据进行加密，然后将数据发送给对方；接收方接收到数据后，利用解密算法和解密密钥从密文中获取明文。没有解密密钥的第三方，无法将密文恢复为明文，从而保证数据传输的机密性。
加解密算法分为两类：
● 非对称密钥算法：数据加密和解密时使用不同的密钥，一个是公开的公钥，一个是由用户秘密保存的私钥。利用公钥（或私钥）加密的数据只能用相应的私钥（或公钥）才能解密。非对称密钥算法一般用于对较少的信息进行加密。
● 对称密钥算法：数据加密和解密时使用相同的密钥。对称密钥算法具有计算速度快的优点，通常用于对大量信息进行加密（如对所有报文加密）。

SSL利用非对称密钥算法RSA、Diffie-Hellman和ECDHE加密客户端随机生成的密钥premaster secret，两端根据premaster secret生成对称密钥算法使用的密钥，然后利用对称密钥算法对传输数据进行加密。
消息完整性验证为了避免网络中传输的数据被非法篡改，SSL利用基于密钥的MAC算法来保证消息的完整性。
MAC算法是将密钥和任意长度的数据转换为固定长度数据的一种算法。
● 发送端在密钥参与下，利用MAC算法计算出消息的MAC值，并将其加在消息之后发送给接收端。
● 接收端利用同样的密钥和MAC算法计算出消息的MAC值，并与接收到的MAC值比较。
如果二者相同，则报文没有改变。否则，报文在传输过程中被修改，接收端将丢弃该报文。

#### 12.3.3 协议结构

如图12-1所示，SSL位于应用层和传输层之间。SSL协议分为两层：底层是SSL记录协议（SSL record protocol）；上层是SSL握手协议（SSL handshake protocol）、SSL密码变化协议（SSL change cipher spec protocol）和SSL警告协议（SSL alert protocol）。
图 12-1 SSL 协议栈
● SSL记录协议：主要负责对上层的数据进行分块、计算并添加MAC、加密后形成记录块，最后把记录块传输给对方。实际的数据传输是使用SSL记录协议来实现的。
● SSL握手协议：握手协议是在应用程序的数据传输之前使用的。用来协商通信过程中使用的加密套件（数据加密算法、密钥交换算法和MAC算法等），实现服务器和客户端的身份验证，并在服务器和客户端之间安全地交换密钥。
● SSL密码变化协议：客户端和服务器端通过密码变化协议通知对端，随后的报文都将使用新协商的加密套件和密钥进行保护和传输。
● SSL警告协议：用来向对端报告握手过程或应用数据传输过程中发生的告警信息，以便对端进行相应的处理。告警消息中包含告警的严重级别和描述。

#### 12.3.4 协议工作过程

握手过程SSL通过握手在客户端和服务器之间建立会话，完成双方身份的验证、密钥和加密套件的协商。 握手过程如图12-2所示。除Change Cipher Spec消息属于SSL密码变化协议外，其他握手过程交互的消息均属于SSL握手协议，统称为SSL握手消息。

其中，服务器对SSL客户端的身份验证是可选的，即图12-2中蓝色部分标识的内容（步骤4、6和8）为可选。
图 12-2 握手过程示意图
1. SSL客户端发送消息给SSL服务器启动握手，携带它支持的SSL版本和加密套件等信息。
在DTLS协议中，为了增强安全性，在握手过程的ClientHello和ServerHello之间引入了Cookie机制。具体来说，Cookie是一种在首次握手时由服务器生成并发送给客户端的临时验证令牌。该机制通过以下流程实现安全防护：
a. SSL 服务器接收到 ClientHello 后，不立即分配会话资源，而是生成一个加密的Cookie，并通过HelloVerifyRequest消息发送给客户端。该Cookie通常基于客户端IP地址、ClientHello中的部分字段以及服务器密钥通过HMAC算法生成，确保无法伪造。
b. SSL客户端收到HelloVerifyRequest后，将其中的Cookie提取出来，并将其填入新的ClientHello消息的“Cookie”扩展字段中，然后重新发送该ClientHello。
SSL服务器收到带Cookie的ClientHello后，重新验证该Cookie是否合法。若验证通过，则继续握手流程；否则，服务器再次返回HelloVerifyRequest。
服务器响应 客户端，携带选定的版本、加密套件。如果 服务器允许
2. SSL SSL SSL SSL客户端在以后的通信中重用本次会话，SSL服务器还会为本次会话分配会话ID。
3. SSL服务器将携带自己公钥信息的数字证书发送给SSL客户端，以便客户端对服务器进行身份认证。

4. （可选）SSL服务器要求SSL客户端提供证书，以便服务器对客户端进行身份认
证。
5. SSL服务器通知SSL客户端版本和加密套件协商结束，开始进行密钥交换。
6. （可选）SSL客户端发送自己的证书给SSL服务器。
7. SSL客户端验证SSL服务器的证书合法后，利用证书中的公钥加密SSL客户端随机生
成的密钥发给SSL服务器。
实际上，这个随机生成的密钥不能直接用来加密数据或计算MAC值，该密钥是用
来计算对称密钥和MAC密钥的信息，称为premaster secret。SSL客户端和SSL服
务器利用premaster secret计算出相同的主密钥（master secret），再利用
master secret生成用于对称密钥算法、MAC算法的密钥。premaster secret是计
算对称密钥、MAC算法密钥的关键。
8. （可选）SSL客户端发送验证消息给服务器，以便服务器对客户端进行身份认证。
客户端通过计算已交互的握手消息、主密钥的Hash值，利用自己的私钥对其进行
加密，通过Certificate Verify消息发给服务器。服务器同样计算已交互的握手消
息、主密钥的Hash值，利用客户端证书中的公钥解密Certificate Verify消息，并
将解密结果与计算出的Hash值比较。如果二者相同，则客户端身份验证成功。
9. SSL客户端通知SSL服务器后续报文将采用协商好的密钥（利用master secret生成
的密钥）和加密套件进行加密和 MAC 计算。
10. SSL客户端通知SSL服务器，让服务器验证握手过程的安全。
SSL客户端计算已交互的握手消息的Hash值，利用协商好的密钥和加密套件处理
Hash值（计算并添加MAC值、加密等），并通过Finished消息发送给SSL服务
器。SSL服务器利用同样的方法计算已交互的握手消息的Hash值，并与Finished消
息的解密结果比较，如果二者相同，且MAC值验证成功，则证明密钥和加密套件
协商成功。
说明
Hash值指的是利用Hash算法（MD5或SHA）将任意长度的数据转换为固定长度的数据。
11. SSL服务器通知SSL客户端后续报文将采用协商好的密钥（利用master secret生成
的密钥）和加密套件进行加密和MAC计算。
12. SSL服务器通知SSL客户端，让客户端验证握手过程的安全。
SSL服务器计算已交互的握手消息的Hash值，利用协商好的密钥和加密套件处理
Hash值（计算并添加MAC值、加密等），并通过Finished消息发送给SSL客户
端。SSL客户端利用同样的方法计算已交互的握手消息的Hash值，并与Finished消
息的解密结果比较，如果二者相同，且MAC值验证成功，则证明密钥和加密套件
协商成功。
握手成功后，SSL客户端也就完成了对SSL服务器的身份验证。因为只有拥有私钥的SSL
服务器才能从Client Exchange消息中解密得到premaster secret，才有后续握手的
Key
成功。
客户端和服务器握手过程中，需要使用非对称密钥算法来加密密钥、验证通信对端的
身份，计算量较大，占用了大量的系统资源。为了简化SSL握手过程，SSL允许重用已
经协商过的会话，如图12-3所示，具体过程如下：

图 12-3 恢复原有会话的 SSL 握手过程示意图
1. SSL客户端发送Client Hello消息，消息中的会话ID设置为计划重用的会话的ID。
2. SSL服务器如果允许重用该会话，则通过在Server Hello消息中设置相同的会话ID来应答。这样，SSL客户端和SSL服务器就可以利用原有会话的密钥和加密套件，不必重新协商。
3. SSL客户端发送Change Cipher Spec消息，通知SSL服务器后续报文将采用原有会话的密钥和加密套件进行加密和MAC计算。
4. SSL客户端计算已交互的握手消息的Hash值，利用原有会话的密钥和加密套件处理Hash值，并通过Finished消息发送给SSL服务器，以便SSL服务器判断密钥和加密套件是否正确。
5. 同样地，SSL服务器发送Change Cipher Spec消息，通知SSL客户端后续报文将采用原有会话的密钥和加密套件进行加密和MAC计算。
6. SSL服务器计算已交互的握手消息的Hash值，利用原有会话的密钥和加密套件处理Hash值，并通过Finished消息发送给SSL客户端，以便SSL客户端判断密钥和加密套件是否正确。
数据传输过程握手完成后，客户端和服务器即可以交换应用层数据。在SSL中，实际的数据传输是使用SSL记录协议来实现的。
图12-4描述了数据传输过程。记录协议接收传输的应用数据，将数据分片成可管理的块，进行数据压缩（可选），添加MAC，接着利用加密算法进行数据加密，最后增加SSL 记录报头。被接收的数据刚好与接收数据的工作过程相反，依次被解密、验证、解压缩和重新装配。

图 12-4 数据传输过程示意图

### 12.4 SSL缺省配置

SSL的主要缺省配置如表12-4所示。
表 12-4 SSL 缺省配置

| 参数 | 缺省配置 |
|---|---|
| SSL策略加密套件 | 未配置 |
| SSL策略加密套件中支持的加密算法 | 未配置 |
| SSL策略 | 未配置 |
| 当前SSL策略所采用的最低版本 | TLS1.2 |
| SSL策略加载证书 | SSL策略未加载数字证书 |
| SSL策略加载数字证书撤销列表CRL | SSL策略未加载CRL |
| SSL策略加载信任证书机构文件 | SSL策略未加载信任证书机构文件 |
| SSL策略绑定加密套件 | SSL策略未绑定加密套件 |

### 12.5 配置SSL

#### 12.5.1 （可选）配置SSL策略加密套件

背景信息加密套件是指在SSL通信中，服务器和客户端所使用的加密算法的组合。在SSL握手初期，客户端将自身支持的加密套件列表发送给服务器；在握手阶段，服务器根据自己的配置从中尽可能的选出一个套件，作为之后所要使用的加密方式。
每种加密套件中支持的加密算法大多包含了如下信息：
● 密钥交换算法：用于决定客户端与服务器之间在握手的过程中如何认证。使用非对称加密算法来生成会话密钥，因为非对称算法不会将重要数据在通信中传输。
用到的算法包括RSA、Diffie-Hellman和ECDHE。
● 签名算法：用于CA证书签名。用到的算法包括RSA和DSS。
● 加密算法：用于对数据进行加密传输。一般有对称加和非对称加密，但是非对称加密算法太耗性能，再者有些非对称加密算法有内容长度的限制，所以真正要传输的数据会使用对称加密来进行加密。算法名称后通常带密钥的长度和加密模式（GCM和CBC）。用到的算法包括：AES_128、AES_256、AES_128_CBC、AES_256_CBC 、 AES_128_GCM 、 AES_256_GCM 和 ChaCha20-Poly1305 。
● 完整性校验算法：用于校验消息的完整性。用到的算法包括SHA、SHA256和SHA384。
例如加密套件中支持的加密算法tls12_ck_rsa_aes_128_cbc_sha，此算法是基于TLS协议，使用的密钥交换算法为RSA，加密算法为AES_128_CBC（密钥长度为128，加密模式为CBC），完整性校验算法为SHA。
表 12-5 加密套件中支持的加密算法

| TLS版本 | 加密套件中支持的加密算法 | 描述 |
|---|---|---|
| TLS1.1、 TLS1.2和 TLS1.3 | tls1_ck_rsa_with_aes_256 _sha | 此算法中的密钥交换算法为RSA，签名算法为RSA，加密算法为AES_256，完整性校验算法为SHA。 |
|  | tls1_ck_rsa_with_aes_128 _sha | 此算法中的密钥交换算法为RSA，签名算法为RSA，加密算法为AES_128，完整性校验算法为SHA。 |
|  | tls1_ck_dhe_rsa_with_aes _256_sha | 此算法中的密钥交换算法为Diffie- Hellman和RSA，签名算法为RSA，加密算法为AES_256，完整性校验算法为 SHA。 |
|  | tls1_ck_dhe_dss_with_aes _256_sha | 此算法中的密钥交换算法为Diffie- Hellman，签名算法为DSS，加密算法为AES_256，完整性校验算法为SHA。 |
|  | tls1_ck_dhe_rsa_with_aes _128_sha | 此算法中的密钥交换算法为Diffie- Hellman，签名算法为RSA，加密算法为AES_128，完整性校验算法为SHA。 |

| TLS版本 | 加密套件中支持的加密算法 | 描述 |
|---|---|---|
|  | tls1_ck_dhe_dss_with_aes _128_sha | 此算法中的密钥交换算法为Diffie- Hellman，签名算法为DSS，加密算法为AES_128，完整性校验算法为SHA。 |
| TLS1.2和 TLS1.3 | tls12_ck_rsa_aes_128_cbc _sha | 此算法中的密钥交换算法为RSA，签名算法为RSA，加密算法为AES_128_CBC （密钥长度为128，加密模式为 CBC），完整性校验算法为SHA。 |
|  | tls12_ck_rsa_aes_256_cbc _sha | 此算法中的密钥交换算法为Diffie- Hellman，签名算法为DSS，加密算法为AES_256_CBC（密钥长度为256，加密模式为CBC），完整性校验算法为 SHA。 |
|  | tls12_ck_rsa_aes_128_cbc _sha256 | 此算法中的密钥交换算法为Diffie- Hellman，签名算法为RSA，加密算法为AES_128_CBC（密钥长度为256，加密模式为CBC），完整性校验算法为 SHA256。 |
|  | tls12_ck_dhe_rsa_aes_128 _cbc_sha | 此算法中的密钥交换算法为Diffie- Hellman，签名算法为RSA，加密算法为AES_128_CBC（密钥长度为128，加密模式为CBC），完整性校验算法为 SHA。 |
|  | tls12_ck_dhe_dss_aes_128 _cbc_sha | 此算法中的密钥交换算法为Diffie- Hellman，签名算法为DSS，加密算法为AES_128_CBC（密钥长度为128，加密模式为CBC），完整性校验算法为 SHA。 |
|  | tls12_ck_dhe_dss_aes_256 _cbc_sha | 此算法中的密钥交换算法为Diffie- Hellman，签名算法为DSS，加密算法为AES_256_CBC（密钥长度为256，加密模式为CBC），完整性校验算法为 SHA。 |
|  | tls12_ck_dhe_rsa_aes_256 _cbc_sha | 此算法中的密钥交换算法为Diffie- Hellman，签名算法为RSA，加密算法为AES_256_CBC（密钥长度为256，加密模式为CBC），完整性校验算法为 SHA。 |
|  | tls12_ck_dhe_dss_aes_128 _cbc_sha256 | 此算法中的密钥交换算法为Diffie- Hellman，签名算法为DSS，加密算法为AES_128_CBC（密钥长度为128，加密模式为CBC），完整性校验算法为 SHA256。 |

| TLS版本 | 加密套件中支持的加密算法 | 描述 |
|---|---|---|
|  | tls12_ck_dhe_rsa_aes_128 _cbc_sha256 | 此算法中的密钥交换算法为Diffie- Hellman，签名算法为RSA，加密算法为AES_128_CBC（密钥长度为128，加密模式为CBC），完整性校验算法为 SHA256。 |
|  | tls12_ck_dhe_dss_aes_256 _cbc_sha256 | 此算法中的密钥交换算法为Diffie- Hellman，签名算法为DSS，加密算法为AES_256_CBC（密钥长度为256，加密模式为CBC），完整性校验算法为 SHA256。 |
|  | tls12_ck_dhe_rsa_aes_256 _cbc_sha256 | 此算法中的密钥交换算法为Diffie- Hellman，签名算法为RSA，加密算法为AES_256_CBC（密钥长度为256，加密模式为CBC），完整性校验算法为 SHA256。 |
|  | tls12_ck_rsa_with_aes_12 8_gcm_sha256 | 此算法中的密钥交换算法为RSA，签名算法为RSA，加密算法为AES_128_gcm （密钥长度为128，加密模式为 GCM），完整性校验算法为SHA256。 |
|  | tls12_ck_rsa_with_aes_25 6_gcm_sha384 | 此算法中的密钥交换算法为RSA，签名算法为RSA，加密算法为AES_256_gcm （密钥长度为256，加密模式为 GCM），完整性校验算法为SHA384。 |
|  | tls12_ck_dhe_rsa_with_ae s_128_gcm_sha256 | 此算法中的密钥交换算法为Diffie- Hellman，签名算法为RSA，加密算法为AES_128_gcm（密钥长度为128，加密模式为GCM），完整性校验算法为 SHA256。 |
|  | tls12_ck_dhe_rsa_with_ae s_256_gcm_sha384 | 此算法中的密钥交换算法为Diffie- Hellman，签名算法为RSA，加密算法为AES_256_gcm（密钥长度为256，加密模式为GCM），完整性校验算法为 SHA384。 |
|  | tls12_ck_dhe_dss_with_ae s_128_gcm_sha256 | 此算法中的密钥交换算法为Diffie- Hellman，签名算法为DSS，加密算法为AES_128_gcm（密钥长度为128，加密模式为GCM），完整性校验算法为 SHA256。 |
|  | tls12_ck_dhe_dss_with_ae s_256_gcm_sha384 | 此算法中的密钥交换算法为Diffie- Hellman，签名算法为DSS，加密算法为AES_256_gcm（密钥长度为256，加密模式为GCM），完整性校验算法为 SHA384。 |

| TLS版本 | 加密套件中支持的加密算法 | 描述 |
|---|---|---|
|  | tls12_ck_rsa_aes_256_cbc _sha256 | 此算法中的密钥交换算法为RSA，签名算法为RSA，加密算法为AES_256_cbc （密钥长度为256，加密模式为 CBC），完整性校验算法为SHA256。 |
|  | tls12_ck_ecdhe_rsa_with_ aes_128_gcm_sha256 | 此算法中的密钥交换算法为ECDHE，签名算法为RSA，加密算法为 AES_128_gcm（密钥长度为128，加密模式为GCM），完整性校验算法为 SHA256。 |
|  | tls12_ck_ecdhe_rsa_with_ aes_256_gcm_sha384 | 此算法中的密钥交换算法为ECDHE，签名算法为RSA，加密算法为 AES_256_gcm（密钥长度为256，加密模式为GCM），完整性校验算法为 SHA384。 |
|  | tls12_ck_ecdhe_ecdsa_wit h_aes_128_gcm_sha256 | 此算法中的密钥交换算法为ECDHE，签名算法为ECDSA，加密算法为 AES_128_gcm（密钥长度为128，加密模式为GCM），完整性校验算法为 SHA256。 |
|  | tls12_ck_ecdhe_ecdsa_wit h_aes_256_gcm_sha384 | 此算法中的密钥交换算法为ECDHE，签名算法为ECDSA，加密算法为 AES_256_gcm（密钥长度为256，加密模式为GCM），完整性校验算法为 SHA384。 |
| TLS1.3 | tls13_aes_128_gcm_sha25 6 | 此算法中的加密算法为AES_128_gcm （密钥长度为128，加密模式为 GCM），完整性校验算法为SHA256。 |
|  | tls13_aes_256_gcm_sha38 4 | 此算法中的加密算法为AES_256_gcm （密钥长度为256，加密模式为 GCM），完整性校验算法为SHA256。 |
|  | tls13_chacha20_poly1305 _sha256 | 此算法中的加密算法为ChaCha20- Poly1305，完整性校验算法为 SHA256。 |
|  | tls13_aes_128_ccm_sha25 6 | 此算法中的加密算法为AES_128_ccm （密钥长度为128，加密模式为 CCM），完整性校验算法为SHA256。 |

操作步骤步骤1 进入系统视图。
system-view

步骤2 创建SSL策略加密套件并进入SSL策略加密套件定制视图。
ssl cipher-suite-list customization-policy-name缺省情况下，没有创建SSL策略加密套件。
步骤3 配置SSL策略加密算法套中支持的加密算法。
set cipher-suite { tls1_ck_rsa_with_aes_256_sha | tls1_ck_rsa_with_aes_128_sha | tls1_ck_dhe_rsa_with_aes_256_sha | tls1_ck_dhe_dss_with_aes_256_sha | tls1_ck_dhe_rsa_with_aes_128_sha | tls1_ck_dhe_dss_with_aes_128_sha | tls12_ck_rsa_aes_128_cbc_sha | tls12_ck_rsa_aes_256_cbc_sha | tls12_ck_rsa_aes_128_cbc_sha256 | tls12_ck_rsa_aes_256_cbc_sha256 | tls12_ck_dhe_dss_aes_128_cbc_sha | tls12_ck_dhe_rsa_aes_128_cbc_sha | tls12_ck_dhe_dss_aes_256_cbc_sha | tls12_ck_dhe_rsa_aes_256_cbc_sha | tls12_ck_dhe_dss_aes_128_cbc_sha256 | tls12_ck_dhe_rsa_aes_128_cbc_sha256 | tls12_ck_dhe_dss_aes_256_cbc_sha256 | tls12_ck_dhe_rsa_aes_256_cbc_sha256 | tls12_ck_rsa_with_aes_128_gcm_sha256 | tls12_ck_rsa_with_aes_256_gcm_sha384 | tls12_ck_dhe_rsa_with_aes_128_gcm_sha256 | tls12_ck_dhe_rsa_with_aes_256_gcm_sha384 | tls12_ck_dhe_dss_with_aes_128_gcm_sha256 | tls12_ck_dhe_dss_with_aes_256_gcm_sha384 | tls12_ck_ecdhe_rsa_with_aes_128_gcm_sha256 | tls12_ck_ecdhe_rsa_with_aes_256_gcm_sha384| tls13_aes_128_gcm_sha256 | tls13_aes_256_gcm_sha384 | tls13_chacha20_poly1305_sha256 | tls13_aes_128_ccm_sha256 | tls12_ck_ecdhe_ecdsa_with_aes_128_gcm_sha256 | tls12_ck_ecdhe_ecdsa_with_aes_256_gcm_sha384 }缺省情况下，SSL策略加密套件中没有配置任何加密算法。
说明出于安全性考虑，不建议使用该特性提供的弱安全算法或弱安全协议。如果确实需要使用，请执行命令install feature-software WEAKEA安装弱安全算法/协议特性包WEAKEA。设备默认自带弱安全算法/协议特性包WEAKEA，特性包安装或卸载的详细步骤请参见《CLI配置指南-系统管理配置》中的“升级维护配置”。
该特性中需要安装弱安全算法/协议特性包后才能使用命令如下所示：

| 命令 | 安装特性包后才能使用的参数 |
|---|---|
| set cipher-suite | tls12_ck_dhe_dss_aes_128_cbc_sha、 tls12_ck_dhe_dss_aes_128_cbc_sha256、 tls12_ck_dhe_dss_aes_256_cbc_sha、 tls12_ck_dhe_dss_aes_256_cbc_sha256、 tls12_ck_dhe_rsa_aes_128_cbc_sha、 tls12_ck_dhe_rsa_aes_128_cbc_sha256、 tls12_ck_dhe_rsa_aes_256_cbc_sha、 tls12_ck_dhe_rsa_aes_256_cbc_sha256、 tls12_ck_rsa_aes_128_cbc_sha、 tls12_ck_rsa_aes_128_cbc_sha256、 tls12_ck_rsa_aes_256_cbc_sha、 tls12_ck_rsa_aes_256_cbc_sha256、 tls12_ck_rsa_with_aes_128_gcm_sha256、 tls12_ck_rsa_with_aes_256_gcm_sha384、 tls1_ck_dhe_dss_with_aes_128_sha、 tls1_ck_dhe_dss_with_aes_256_sha、 tls1_ck_dhe_rsa_with_aes_128_sha、 tls1_ck_dhe_rsa_with_aes_256_sha、 tls1_ck_rsa_with_aes_128_sha、 tls1_ck_rsa_with_aes_256_sha |
| ssl minimum version | tls1.1 |

SSL通过握手在客户端和服务器之间建立会话，完成双方身份的验证、密钥和加密套件的协商，在通信过程中建议使用TLS1.2及以上版本的安全套件。TLS版本中，使用CBC模式的对称加密算法可能存在数据受到明文恢复攻击而泄露加密传输的内容，因此，在TLS版本中不建议使用CBC模式对数据加密。
同等安全条件下，相对于ECDHE类型的密钥交换算法，DHE类型的密钥交换算法在协商使用时CPU占用较高。建议优先使用ECDHE类型的密钥交换算法，对应算法套为tls12_ck_ecdhe_rsa_with_aes_128_gcm_sha256，tls12_ck_ecdhe_rsa_with_aes_256_gcm_sha384；同时在使用该算法套列表的SSL策略下，选择配置brainpool和curve的椭圆曲线配置参数。
----结束

#### 12.5.2 配置SSL策略（手工加载证书）

前提条件在为SSL策略加载信任证书机构文件之前，需完成以下任务：
客户端或服务器已从 CA （ Certificate Authority ，证书机构）申请了证书文件，并将证书上传到系统根目录下名为security的子目录下。
背景信息SSL利用数据加密、身份验证和消息完整性验证机制，为基于TCP可靠连接的应用层协议提供安全性保证。应用层协议可以关联SSL策略，使应用层协议与SSL结合，从而为应用层协议提供安全连接。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置SSL策略并进入SSL策略视图。
ssl policy policy-name缺省情况下，没有配置SSL策略。
步骤3 （可选）配置ECDHE算法的椭圆曲线参数。
ecdh group { nist | curve | brainpool | ffdhe } *缺省情况下，ECDHE算法椭圆曲线参数为Curve、Nist和Brainpool。
步骤4 （可选）配置禁止TLS1.3使用brainpoolr1曲线。
ssl forbidden tls13-use-brainpoolr1缺省情况下，TLS1.3允许使用brainpoolr1曲线。
步骤5 （可选）配置数字证书链的最小路径长度。
ssl verify certificate-chain minimum-path-length path-length缺省情况下，数字证书链最小路径长度是1。
步骤6 （可选）配置数字证书校验功能。
● 配置校验对端数字证书的增强型密钥用法字段。
ssl verify key-usage enable

● 配置校验对端证书的哈希算法和签名算法。
ssl verify certificate-signature-algorithm enable
● 配置校验对端发送的CA证书的基本约束字段。
ssl verify basic-constrain enable
● 校验本地加载的数字证书是否为X.509v3版本。
ssl verify version cert-version3 enable
● 校验本地加载的CRL是否为X.509v2版本。
ssl verify version crl-version2 enable
缺省情况下，数字证书校验功能去使能。
步骤7 （可选）设置Diffie-Hellman密钥交换算法的模数。
diffie-hellman modulus modulus-val
缺省情况下，Diffie-Hellman密钥交换算法的模数为3072。
步骤8 （可选）设置SSL握手过程支持的签名算法。
signature algorithm-list { ecdsa-secp256r1-sha256 | ecdsa-secp384r1-sha384 | ecdsa-secp521r1-sha512
| ed25519 | ed448 | rsa-pss-pss-sha256 | rsa-pss-pss-sha384 | rsa-pss-pss-sha512 | rsa-pss-rsae-sha256 |
rsa-pss-rsae-sha384 | rsa-pss-rsae-sha512 | rsa-pkcs1-sha256 | rsa-pkcs1-sha384 | rsa-pkcs1-sha512 |
ecdsa-sha1 | ecdsa-sha224 | rsa-sha1 | rsa-sha224 | dsa-sha1 | dsa-sha224 | dsa-sha256 | dsa-sha384 |
*
dsa-sha512 | sm2-sm3 }
缺省情况下，配置的签名算法为ed25519，ed448，ecdsa-secp256r1-sha256，ecdsa-
secp384r1-sha384，ecdsa-secp521r1-sha512，rsa-pss-pss-sha256，rsa-pss-pss-
sha384，rsa-pss-pss-sha512，rsa-pss-rsae-sha256，rsa-pss-rsae-sha384，rsa-pss-
rsae-sha512。
步骤9 （可选）配置当前SSL策略所采用的最低版本。
ssl minimum version { tls1.1 | tls1.2 | tls1.3 }
缺省情况下，SSL策略所采用的最低版本为TLS1.2。
说明
● SSL策略所支持的SSL版本包括TLS1.1、TLS1.2和TLS1.3，其安全性依次升高，建议用户使用
TLS1.2或者TLS1.3。
● 该命令中的参数tls1.1需要执行命令install feature-software WEAKEA安装弱安全算法/协
议特性包（WEAKEA）后才能使用。
步骤10 为SSL策略加载证书。
缺省情况下，SSL策略未加载证书。
说明
● 为保证更好的安全性，建议使用安全性更高的证书：RSA/DSA证书的签名算法长度大于等于
3072，ECC证书的签名算法长度大于等于256，并且证书的哈希算法为SHA-256或更高版
本。
● RSA/DSA证书的签名算法长度小于等于2048，ECC证书的签名算法长度小于256，或证书的
哈希算法为SHA1、SHA224、MD4、MD5，需要执行命令install feature-software
WEAKEA后才能使用。
● 为SSL策略加载PEM格式的证书
certificate load pem-cert certFile key-pair keyType key-file keyFile auth-code [ cipher authCode ]
● 为SSL策略加载PEM格式的证书链
certificate load pem-chain certFile key-pair keyType key-file keyFile auth-code [ cipher authCode ]
● 为SSL策略加载PFX格式的证书
形式一：

certificate load pfx-cert certFile key-pair keyType key-file keyFile auth-code [ cipher authCode ]形式二：
certificate load pfx-cert certFile key-pair keyType mac [ cipher macCode auth-code cipher authCode ]步骤11 （可选）为SSL策略加载数字证书撤销列表CRL（Certificate Revocation List）。
crl load crlType crlFile缺省情况下，SSL策略未加载CRL。
步骤12 （可选）为SSL策略加载信任证书机构文件。
缺省情况下，SSL策略未加载信任证书机构文件。
信任证书机构文件用于验证服务器发送的数字证书的真实性。一个SSL策略最多可以同时加载4个信任证书机构文件。
说明
● 如果需要对对端进行身份认证需要配置此步骤。
● 为保证更好的安全性，建议使用安全性更高的证书：RSA/DSA证书的签名算法长度大于等于3072 ， ECC 证书的签名算法长度大于等于 256 ，并且证书的哈希算法为 SHA-256 或更高版本。
● RSA/DSA证书的签名算法长度小于等于2048，ECC证书的签名算法长度小于256，或证书的哈希算法为SHA1、SHA224、MD4、MD5，需要执行命令install feature-software WEAKEA后才能使用。
● 为SSL策略加载ASN1格式信任证书机构文件trusted-ca load asn1-ca caFile
● 为SSL策略加载PEM格式信任证书机构文件trusted-ca load pem-ca caFile
● 为SSL策略加载PFX格式信任证书机构文件trusted-ca load pfx-ca caFile auth-code [ cipher authCode ]步骤13 （可选）排除算法套列表中密钥交换算法。
* cipher-suite exclude key-exchange { rsa | dhe } cipher-suite exclude cipher mode cbc cipher-suite exclude hmac sha1缺省情况下，SSL策略不支持RSA密钥交换算法、CBC加密模式算法及SHA1摘要算法。
步骤14 （可选）为SSL策略绑定加密套件。
binding cipher-suite-customization customization-name缺省情况下，SSL策略没有绑定加密套件。
绑定加密套件中的加密算法之前需已完成SSL策略加密套件的配置，配置过程请参见
12.5.1 （可选）配置SSL策略加密套件。
步骤15 （可选）设置证书过期的告警阈值和检查间隔。
quit ssl certificate alarm-threshold early-alarm time check-interval check-period缺省情况下，证书过期提前告警阈值为90天，证书过期告警检查周期为24小时。
步骤 16 （可选）开启 SSL 重协商功能。
ssl renegotiation enable缺省情况下，SSL重协商功能关闭。

当应用SSL进行数据传输时，可以使能SSL重协商功能，在不中断连接的情况下定期更新密钥和算法，以提高通信的安全性。
----结束

#### 12.5.3 配置SSL策略（PKI加载证书）

前提条件要绑定的PKI域名已加载了证书，加载的证书可以是设备初始证书或者用户申请的数字证书。如何使用PKI方式加载证书，请参见《CLI配置指南-安全-PKI配置》。
背景信息SSL利用数据加密、身份验证和消息完整性验证机制，为基于TCP可靠连接的应用层协议提供安全性保证。应用层协议可以关联SSL策略，使应用层协议与SSL结合，从而为应用层协议提供安全连接。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置SSL策略并进入SSL策略视图。
ssl policy policy-name缺省情况下，没有配置SSL策略。
步骤3 （可选）配置ECDHE算法的椭圆曲线参数。
* ecdh group { nist | curve | brainpool | ffdhe }缺省情况下，ECDHE算法椭圆曲线参数为Curve、Nist和Brainpool。
步骤4 （可选）配置禁止TLS1.3使用brainpoolr1曲线。
ssl forbidden tls13-use-brainpoolr1缺省情况下，TLS1.3允许使用brainpoolr1曲线。
步骤5 （可选）配置数字证书链的最小路径长度。
ssl verify certificate-chain minimum-path-length path-length缺省情况下，数字证书链最小路径长度是1。
步骤6 （可选）配置数字证书校验功能。
● 配置校验对端数字证书的增强型密钥用法字段。
ssl verify key-usage enable
● 配置校验对端证书的哈希算法和签名算法。
ssl verify certificate-signature-algorithm enable
● 配置校验对端发送的CA证书的基本约束字段。
ssl verify basic-constrain enable
● 校验本地加载的数字证书是否为X.509v3版本。
ssl verify version cert-version3 enable
● 校验本地加载的CRL是否为X.509v2版本。
ssl verify version crl-version2 enable缺省情况下，数字证书校验功能去使能。

步骤7 （可选）设置Diffie-Hellman密钥交换算法的模数。
diffie-hellman modulus modulus-val缺省情况下，Diffie-Hellman密钥交换算法的模数为3072。
步骤8 （可选）设置SSL握手过程支持的签名算法。
signature algorithm-list { ecdsa-secp256r1-sha256 | ecdsa-secp384r1-sha384 | ecdsa-secp521r1-sha512 | ed25519 | ed448 | rsa-pss-pss-sha256 | rsa-pss-pss-sha384 | rsa-pss-pss-sha512 | rsa-pss-rsae-sha256 | rsa-pss-rsae-sha384 | rsa-pss-rsae-sha512 | rsa-pkcs1-sha256 | rsa-pkcs1-sha384 | rsa-pkcs1-sha512 | ecdsa-sha1 | ecdsa-sha224 | rsa-sha1 | rsa-sha224 | dsa-sha1 | dsa-sha224 | dsa-sha256 | dsa-sha384 |
* dsa-sha512 | sm2-sm3 }缺省情况下，配置的签名算法为ed25519，ed448，ecdsa-secp256r1-sha256，ecdsa- secp384r1-sha384，ecdsa-secp521r1-sha512，rsa-pss-pss-sha256，rsa-pss-pss- sha384，rsa-pss-pss-sha512，rsa-pss-rsae-sha256，rsa-pss-rsae-sha384，rsa-pss- rsae-sha512。
步骤9 （可选）配置当前SSL策略所采用的最低版本。
ssl minimum version { tls1.1 | tls1.2 | tls1.3 }缺省情况下，SSL策略所采用的最低版本为TLS1.2。
说明
● SSL策略所支持的SSL版本包括TLS1.1、TLS1.2和TLS1.3，其安全性依次升高，建议用户使用TLS1.2或者TLS1.3。
● 该命令中的参数tls1.1需要执行命令install feature-software WEAKEA安装弱安全算法/协议特性包（WEAKEA）后才能使用。
步骤10 为SSL策略绑定PKI域。绑定PKI域后，SSL策略使用PKI域下的本地证书、CA证书、证书撤销列表。
pki-domain pki-domain步骤11 （可选）排除算法套列表中密钥交换算法。
cipher-suite exclude key-exchange { rsa | dhe } * cipher-suite exclude cipher mode cbc cipher-suite exclude hmac sha1缺省情况下，SSL策略不支持RSA密钥交换算法、CBC加密模式算法及SHA1摘要算法。
步骤12 （可选）为SSL策略绑定加密套件。
binding cipher-suite-customization customization-name缺省情况下，SSL策略没有绑定加密套件。
绑定加密套件中的加密算法之前需已完成SSL策略加密套件的配置，配置过程请参见
12.5.1 （可选）配置SSL策略加密套件。
步骤13 （可选）开启SSL重协商功能。
ssl renegotiation enable缺省情况下，SSL重协商功能关闭。
当应用 SSL 进行数据传输时，可以使能 SSL 重协商功能，在不中断连接的情况下定期更新密钥和算法，以提高通信的安全性。
----结束

#### 12.5.4 配置DTLS策略

前提条件要绑定的PKI域名已加载了证书，加载的证书可以是设备初始证书或者用户申请的数字证书。如何使用PKI方式加载证书，请参见《CLI配置指南-安全-PKI配置》。
背景信息DTLS利用数据加密、身份验证和消息完整性验证机制，为基于UDP的应用层协议提供安全性保证。应用层协议可以关联DTLS策略，使应用层协议与DTLS结合，从而为应用层协议提供安全连接。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置DTLS策略并进入DTLS策略视图。
dtls policy policyName缺省情况下，没有配置DTLS策略。
步骤3 （可选）配置数字证书链的最小路径长度。
ssl verify certificate-chain minimum-path-length path-length缺省情况下，数字证书链最小路径长度是1。
步骤4 （可选）配置数字证书校验功能。
配置校验对端数字证书的增强型密钥用法字段。
●ssl verify key-usage enable配置校验对端证书的哈希算法和签名算法。
●ssl verify certificate-signature-algorithm enable配置校验对端发送的CA证书的基本约束字段。
●ssl verify basic-constrain enable缺省情况下，数字证书校验功能关闭。
步骤5 （可选）配置Diffie-Hellman密钥交换算法的模数。
diffie-hellman modulus modulus-val缺省情况下， Diffie-Hellman 密钥交换算法的模数为 3072 。
步骤6 （可选）配置签名算法。
signature algorithm-list { ecdsa-secp256r1-sha256 | ecdsa-secp384r1-sha384 | ecdsa-secp521r1-sha512 | ed25519 | ed448 | rsa-pss-pss-sha256 | rsa-pss-pss-sha384 | rsa-pss-pss-sha512 | rsa-pss-rsae-sha256 | rsa-pss-rsae-sha384 | rsa-pss-rsae-sha512 | rsa-pkcs1-sha256 | rsa-pkcs1-sha384 | rsa-pkcs1-sha512 | ecdsa-sha1 | ecdsa-sha224 | rsa-sha1 | rsa-sha224 | dsa-sha1 | dsa-sha224 | dsa-sha256 | dsa-sha384 |
* dsa-sha512 }缺省情况下，配置的签名算法为ed25519，ed448，ecdsa-secp256r1-sha256，ecdsa- secp384r1-sha384，ecdsa-secp521r1-sha512，rsa-pss-pss-sha256，rsa-pss-pss- sha384，rsa-pss-pss-sha512，rsa-pss-rsae-sha256，rsa-pss-rsae-sha384，rsa-pss- rsae-sha512 。
步骤7 为DTLS策略绑定PKI域。绑定PKI域后，DTLS策略使用PKI域下的本地证书、CA证书、证书撤销列表。

pki-domain pki-domain缺省情况下，不绑定PKI域名。
步骤8 （可选）为DTLS策略绑定加密套件。
binding cipher-suite-customization customization-name缺省情况下，DTLS策略没有绑定加密套件。默认所有的加密算法都可以使用。
绑定加密套件中的加密算法之前需已完成DTLS策略加密套件的配置，配置过程请参见
12.5.1 （可选）配置SSL策略加密套件。
----结束

#### 12.5.5 配置使用商密算法套的SSL策略

前提条件要绑定的PKI域名已加载了SM2-SM3证书，加载的证书可以是设备初始证书或者用户申请的数字证书。如何使用PKI方式加载证书，请参见《CLI配置指南-安全-PKI配置》。
背景信息如果应用需要使用商密算法套TLS_SM4_CCM_SM3和TLS_SM4_GCM_SM3，必须要使用配套的ecdh group算法和签名算法。商密算法套TLS_SM4_CCM_SM3和TLS_SM4_GCM_SM3不能与其他算法套一同配置使用。
操作步骤步骤1 进入系统视图。
system-view步骤2 创建SSL策略加密套件并进入SSL策略加密套件定制视图。
ssl cipher-suite-list customization-policy-name缺省情况下，没有创建SSL策略加密算法套件。
步骤3 配置SSL策略加密算法套中支持的加密算法。
set cipher-suite { tls13_sm4_ccm_sm3 | tls13_sm4_gcm_sm3 }缺省情况下，SSL策略加密套件中没有配置任何加密算法。
步骤 4 配置 SSL 策略并进入 SSL 策略视图。
ssl policy policy-name缺省情况下，没有配置SSL策略。
步骤5 绑定已创建的商密加密算法套件。
binding cipher-suite-customization cipher-suite-name缺省情况下，没有配置SSL加密算法套件。
步骤6 配置ECDHE算法的椭圆曲线参数。
ecdh group curve-sm2缺省情况下，ECDHE算法椭圆曲线参数值为Curve、Nist和Brainpool。
商密算法套件不能使用默认的ECDHE椭圆曲线算法。

步骤7 配置签名算法。
signature algorithm-list sm2-sm3缺省情况下，配置的签名算法为ed25519，ed448，ecdsa-secp256r1-sha256，ecdsa- secp384r1-sha384，ecdsa-secp521r1-sha512，rsa-pss-pss-sha256，rsa-pss-pss- sha384，rsa-pss-pss-sha512，rsa-pss-rsae-sha256，rsa-pss-rsae-sha384，rsa-pss- rsae-sha512。
商密算法套件不能使用默认的签名算法。
步骤8 为SSL策略绑定PKI域。绑定PKI域后，SSL策略使用PKI域下的本地证书、CA证书、证书撤销列表。
pki-domain pki-domain缺省情况下，不绑定PKI域名。
PKI域下的证书，证书撤销列表都必须是SM2-SM3证书。
----结束

#### 12.5.6 应用SSL策略

背景信息SSL本身只是一种安全协议，SSL策略只有与各种应用关联后才能生效。
操作步骤步骤1 应用SSL策略。SSL策略的具体应用请参见表12-6。
表 12-6 SSL 策略的主要应用

| SSL策略的主要应用 | 具体应用示例 |
|---|---|
| 在BGP中应用SSL | 《CLI配置指南-IP路由配置》中的“配置BGP的SSL/TLS 认证” |
| 在HTTPS中应用SSL | 《CLI配置指南-系统管理》中的“举例：通过使用 RESTCONF管理设备” |

----结束
