# S1700, S5700, S6700 V600R025C00 配置指南-安全 01-14 HTTPS配置

## 14 HTTPS配置

### 14.1 HTTPS简介

14.2 HTTPS配置注意事项
14.3 HTTPS原理描述
14.4 HTTPS缺省配置
14.5 配置HTTPS客户端
14.6 举例：配置设备作为HTTPS客户端
14.1 HTTPS 简介
定义
HTTP（Hypertext Transfer Protocol）即超文本传输协议，是用于从WWW服务器传
输超文本到本地浏览器的传输协议。HTTP位于应用层，基于TCP/IP协议来传输各种数
据，例如Web页面，HTTP由请求和响应构成，是一个标准的客户端/服务器模型。
HTTPS（Secure HTTP）是支持安全套接层SSL（Secure Sockets Layer）协议的HTTP
协议。
目的
HTTP功能为用户和使用HTTP协议传输数据的特性提供了统一的接口。但是HTTP协议
不具备安全机制，采用明文形式传输数据，不能验证通信双方的身份，无法防止传输
的数据被篡改，安全性很低。HTTPS是在HTTP上建立SSL加密层，并对传输数据进行
加密，是HTTP协议的安全版。HTTPS从以下几方面提高了设备的安全性：
● 客户端与服务器之间交互的数据需要经过加密，保证了数据传输的安全性和完整
性，从而实现了对设备的安全管理。
● 对服务器和客户端进行基于证书的身份认证。
● 消息传输过程中使用消息验证码 MAC （ Message Authentication Code ）算法来
检验消息的完整性。
当前需要开启HTTPS服务器功能的特性有：

NETCONF场景下，通过HTTPS协议从HTTPS服务器加载指定YANG文件的配置数据到配置数据库。

### 14.2 HTTPS配置注意事项

硬件依赖表 14-1 支持本特性的硬件

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

| 系列 | 支持产品 |
|---|---|
| S6750-S | S6750-S16X10Y2CZ，S6750-S16X8YZ，S6750- S24T16X8Y2CZ |
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
特性限制无

### 14.3 HTTPS原理描述

HTTP 报文格式HTTP是一种请求/响应协议，HTTP报文包括请求报文和响应报文。

请求报文HTTP客户端向服务器端发送一个请求，请求报文中包含三部分：请求行、请求头部和请求数据，如图14-1所示。
图 14-1 请求报文格式表 14-2 请求报文各字段解释

| 字段名 | 含义 |
|---|---|
| Method | HTTP操作方法，作用于URI中指定的目标资源。包括GET、HEAD、PUT、 POST、TRACE、OPTIONS、DELETE以及扩展方法。 |
| URI | URL地址。 |
| HTTP/Version-number | HTTP协议版本。 |
| Header-Name-n:value | 头部字段名：值。 |
| Optional request body | （可选）请求消息体。 |

响应报文HTTP服务器收到客户端发送的请求后，会返回响应报文给客户端。响应报文也包含三部分：响应行、响应头部和响应数据，如图14-2所示。
图 14-2 响应报文格式

表 14-3 响应报文各字段解释

| 字段名 | 含义 |
|---|---|
| HTTP/Version-number | HTTP协议版本。 |
| Status code | HTTP状态码。状态代码为3位数字，200~299的状态码表示成功，300~399的状态码指资源重定向，400~499的状态码指客户端请求出错，500~599的状态码指服务端出错。 |
| Message | HTTP状态消息。 |
| Header-Name-n:value | 头部字段名：值。 |
| Optional response body | （可选）响应消息体。 |

HTTP 协议通信过程基于HTTP协议的客户/服务器模式的信息交换过程如图14-3所示，它分四个过程：建立连接、发送请求、发送响应、关闭连接。
图 14-3 HTTP 协议通信过程
1. HTTP客户端向HTTP服务器发起连接请求。
2. 建立连接后，HTTP客户端发送一个请求报文给HTTP服务器。
3. HTTP服务器接到请求报文后，发送响应报文给HTTP客户端。
4. HTTP 客户端接收服务器返回的信息后，一般由 HTTP 客户端请求关闭连接。

HTTP 应用 SSL HTTP协议不具备安全机制，采用明文形式传输数据，不能验证通信双方的身份，无法防止传输的数据被篡改，安全性很低。安全协议SSL利用数据加密、身份验证和消息完整性验证机制，为基于TCP可靠连接的应用层协议提供了安全性保证。HTTPS是在HTTP上应用SSL来保障HTTP的安全性，对HTTPS可以简单理解为HTTPS＝HTTP +SSL。安全连接的URL将以https://而不是以http://开头。
HTTP应用SSL进行数据传输时，HTTP客户端首先向HTTP服务器的适当端口发起一个连接，然后发送ClientHello来开始SSL握手。当SSL握手完成，客户端就初始化第一个HTTP请求。所有的HTTP数据必须作为SSL的“应用数据”发送。
HTTPS连接时需要进行证书申请，申请证书前需要了解以下相关概念：
数字证书数字证书是由CA签发的一个声明，证明证书主体（证书申请者拥有了证书后即成为证书主体）与证书中所包含的公钥的唯一对应关系。数字证书中包括证书申请者的名称及相关信息、申请者的公钥、签发数字证书的CA的数字签名及数字证书的有效期等内容。数字证书使网上通信双方的身份得到了互相验证，提高了通信的可靠性。
设备可以加载PEM、ASN1和PFX三种格式的数字证书文件。不同格式的数字证书文件的内容是一样的。
● PEM是最常用的一种数字证书格式，文件的扩展名是.pem，适用于系统之间的文本模式传输。
● ASN1是通用的数字证书格式之一，文件的扩展名是.der，是大多数浏览器的默认格式。
● PFX是通用的数字证书格式之一，文件的扩展名是.pfx，是可移植的二进制格式，可以转换为PEM或ASN1格式。
CA CA是发放、管理、废除数字证书的机构。CA的作用是检查数字证书持有者身份的合法性，并签发数字证书（在证书上签字），以防证书被伪造或篡改，以及对证书和密钥进行管理。国际上被广泛信任的CA，被称之为根CA。根CA可授权其他CA为其下级CA。CA的身份也需要证明，而证明信息在信任证书机构文件中描述。
例如：CA1作为最上级CA也叫根证书，签发下一级CA2证书，CA2又可以给它的下一级CA3签发证书，以此下去，最终由CAn签发服务器的证书。
如果服务器端的证书由CA3签发，则在客户端验证证书的过程从服务器端的证书有效性验证开始。先由CA3证书验证服务器端证书的有效性，如果通过则再由CA2证书验证CA3证书的有效性，最后由最上级CA1证书验证CA2证书的有效性。只有通过最上级CA证书即根证书的验证，服务器证书才会验证成功。
证书撤销列表CRL（Certificate Revocation List）
CRL由CA发布，它指定了一套证书发布者认为无效的证书。
数字证书的寿命是有限的，但CA可通过证书撤销过程缩短证书的寿命。CRL指定的寿命通常比数字证书指定的寿命要短。由 CA 撤销数字证书，意味着 CA 在数字证书正常到期之前撤销允许使用密钥对的有关声明。在撤销证书到期后，CRL中的有关数据被删除，以缩短CRL列表的大小。

### 14.4 HTTPS缺省配置

HTTPS的主要缺省配置如表14-4所示。
表 14-4 HTTPS 缺省配置

| 参数 | 缺省配置 |
|---|---|
| HTTP | 关闭 |

### 14.5 配置HTTPS客户端

#### 14.5.1 配置SSL策略

背景信息在配置HTTPS前，需要在设备上部署SSL策略，并加载相应的数字证书。SSL策略是指设备启动时使用的SSL参数。只有与应用层协议（如HTTP协议）关联后，SSL策略才能生效。
说明
● 为保证更好的安全性，建议使用安全性更高的证书：RSA/DSA证书的签名算法长度大于等于3072，ECC证书的签名算法长度大于等于256，并且证书的哈希算法为SHA-256或更高版本。
● RSA/DSA证书的签名算法长度小于等于2048，ECC证书的签名算法长度小于256，或证书的哈希算法为SHA1、SHA224、MD4、MD5，需要执行命令install feature-software WEAKEA后才能使用。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置SSL策略并进入SSL策略视图。
ssl policy policy-name步骤3 HTTPS客户端需要根据HTTPS服务器加载的证书格式为SSL策略加载证书。
● 为SSL策略加载PEM格式的证书。
certificate load pem-cert certFile key-pair keyType key-file keyFile auth-code [ cipher authCode ]
● 为SSL策略加载PFX格式的证书。
形式一：
certificate load pfx-cert certFile key-pair keyType mac [ cipher macCode auth-code cipher authCode ]形式二：
certificate load pfx-cert certFile key-pair keyType key-file keyFile auth-code [ cipher authCode ]
● 为SSL策略加载PEM格式的证书链。
certificate load pem-chain certFile key-pair keyType key-file keyFile auth-code [ cipher authCode ]

步骤4 HTTPS客户端需要根据HTTPS服务器加载的信任证书机构文件为SSL策略加载信任证书机构文件。
● 为SSL策略加载PEM格式信任证书机构文件。
trusted-ca load pem-ca caFile
● 为SSL策略加载PFX格式信任证书机构文件。
trusted-ca load pfx-ca caFile auth-code [ cipher authCode ]
● 为SSL策略加载ASN1格式信任证书机构文件。
trusted-ca load asn1-ca caFile
----结束

#### 14.5.2 配置HTTPS客户端

前提条件在配置HTTPS客户端之前，需确保设备与HTTPS客户端之间的路由可达。
操作步骤步骤1 进入系统视图。
system-view步骤2 使能HTTP功能，并进入HTTP视图。
http步骤3 为HTTPS客户端配置SSL策略。
client ssl-policy policy-name步骤4 配置HTTPS客户端对服务器端进行合法性校验。
client ssl-verify peer步骤5 （可选）配置HTTPS客户端绑定的源接口。
client source-interface { interface-name | interface-type interface-number }缺省情况下，未绑定客户端源接口。
步骤6 （可选）配置HTTPS客户端的源IPv6地址和VPN。
client ipv6 source-address ipv6-address [ vpn-instance ipv6-vpn-instance-name ]
----结束

#### 14.5.3 配置HTTPS下载系统软件

前提条件在配置HTTPS下载系统软件之前，需要完成以下任务：配置SSL策略。
背景信息设备可通过HTTPS方式下载系统软件。如果在下载文件时未指定SSL策略，则将使用HTTPS客户端配置的SSL策略。

操作步骤步骤1 下载文件。
download file-url [ save-as file-path | [ ssl-policy policy-name [ ssl-verify peer [ verify-dns ] ] | verify- dns ] | vpn-instance vpn-name | source-ip ip-address ] *
----结束

#### 14.5.4 配置HTTPS上传本地文件

前提条件在配置HTTPS上传本地文件之前，需要完成以下任务：配置SSL策略。
背景信息设备可通过HTTPS方式上传本地文件到服务器，如果不指定SSL策略，则使用HTTPS客户端配置的SSL策略。在服务器端可根据本地文件分析设备运行状态。
操作步骤步骤1 上传文件。
upload file-url local-file file-path [ [ ssl-policy policy-name [ ssl-verify peer [ verify-dns ] ] | verify-dns ] | user-name name-value password password-value | vpn-instance vpn-name | source-ip ip-address ] *
----结束

### 14.6 举例：配置设备作为HTTPS客户端

组网需求如图14-4所示，在配置HTTPS客户端之前，需要在设备上部署SSL策略，并加载相应的数字证书，与应用层协议HTTP协议关联后，用户才可以通过HTTPS客户端登录HTTPS服务器。
图 14-4 配置通过 HTTPS 访问其他设备文件组网图配置思路采用如下的思路配置通过HTTPS访问其他设备文件：
1. 配置HTTPS客户端的SSL策略。
2. 配置HTTPS客户端。

操作步骤步骤1 配置HTTPS客户端的SSL策略。
\# 通过SFTP方式将已申请好的数字证书上传到设备的/pki/public目录下。如果使用PKI方式申请数字证书，请参见《配置指南-PKI配置》。
\# 配置PKI域。并导入本地证书和私钥文件。
<HUAWEI> system-view [HUAWEI] pki realm domain1 [HUAWEI-pki-realm-domain1] quit [HUAWEI] pki import-certificate local realm domain1 pem filename https_local.pem [HUAWEI] pki import rsa-key-pair http-key pem restconf.pem //如果是在本设备上生成的私钥文件，不再需要此步骤。
\# 导入对端的CA证书，用于验证对端的本地证书合法性。
[HUAWEI] pki import-certificate ca realm domain1 pem filename https_ca.pem说明这里以CA证书为例，用户在实际配置过程中需要将ca和test.crt替换为设备上已有的证书类型和名称。用户可以自行将证书上传至设备中进行安装，也可以通过申请和下载后进行安装，详细过程请参考《PKI配置》中的“获取证书”章节。
\# 配置SSL绑定PKI域。
[HUAWEI] ssl policy policy1 [HUAWEI-ssl-policy-policy1] pki-domain domain1 [HUAWEI-ssl-policy-policy1] quit步骤2 配置HTTPS客户端。
[HUAWEI] http [HUAWEI-http] client ssl-policy policy1 [HUAWEI-http] client ssl-verify peer [HUAWEI-http] quit
----结束检查配置结果执行命令display ssl policy查看HTTPS客户端是否配置成功。
[HUAWEI] display ssl policy SSL Policy Name: policy1 PKI domain: domain_name Policy Applicants: HTTP-CLIENT Key-pair Type:
Certificate File Type:
Certificate Type:
Certificate Filename:
Key-file Filename:
CRL File:
Trusted-CA File:
配置脚本\# ssl policy policy1 pki-domain domain1 \# http client ssl-policy policy1 client ssl-verify peer \#

pki realm domain1 \# return
