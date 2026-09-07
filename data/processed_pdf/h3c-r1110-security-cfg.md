# H3C R1110 安全配置指导

H3C S6520X-EI & S6520X-HI系列以太网交换机安全配置指导新华三技术有限公司http://www.h3c.com资料版本：6W100-20180821产品版本：Release 1110

未经本公司书面许可，任何单位和个人不得擅自摘抄、复制本书内容的部分或全部，并不得以任何形式传播。
H3C、 、H3CS、H3CIE、H3CNE、Aolynk、 、H Care、 、IRF、NetPilot、Netflow、SecEngine、SecPath、SecCenter、SecBlade、Comware、ITCMM、HUASAN、华三均为新华三技术有限公司的商标。对于本手册中出现的其它公司的商标、产品标识及商品名称，由各自权利人拥有。
由于产品版本升级或其他原因，本手册内容有可能变更。H3C 保留在没有任何通知或者提示的情况下对本手册的内容进行修改的权利。本手册仅作为使用指导，H3C 尽全力在本手册中提供准确的信息，但是 H3C 并不确保手册内容完全没有错误，本手册中的所有陈述、信息和建议也不构成任何明示或暗示的担保。

## 00-前言

前 言本配置指导主要介绍各种安全业务特性的原理及配置方法，包括 AAA、PKI 等身份认证特性，公钥管理、SSH、IPsec 等数据安全特性，以及 IP Source Guard、ARP 攻击防御等安全防御特性。
前言部分包含如下内容：
• 读者对象
• 本书约定
• 资料意见反馈

### 读者对象

本手册主要适用于如下工程师：
网络规划人员
•
• 现场技术支持与维护人员
• 负责网络配置和维护的网络管理员

### 本书约定

#### 1. 命令行格式约定

格 式 意 义粗体 命令行关键字（命令中保持不变、必须照输的部分）采用加粗字体表示。
斜体 命令行参数（命令中必须由实际值进行替代的部分）采用斜体表示。
表示用“[ ]”括起来的部分在命令配置时是可选的。
[ ] { x | y | ... } 表示从多个选项中仅选取一个。
[ x | y | ... ] 表示从多个选项中选取一个或者不选。
{ x | y | ... } * 表示从多个选项中至少选取一个。
[ x | y | ... ] * 表示从多个选项中选取一个、多个或者不选。
&<1-n> 表示符号&前面的参数可以重复输入1～n次。
\# 由“#”号开始的行表示为注释行。

#### 2. 图形界面格式约定

格 式 意 义< > 带尖括号“ < > ”表示按钮名，如“单击 < 确定 > 按钮”。
[ ] 带方括号“[ ]”表示窗口名、菜单名和数据表，如“弹出[新建用户]窗口”。
多级菜单用“/”隔开。如[文件/新建/文件夹]多级菜单表示[文件]菜单下的[新建]子菜单下/的[文件夹]菜单项。

#### 3. 各类标志

本书还采用各种醒目标志来表示在操作过程中应该特别注意的地方，这些标志的意义如下：
该标志后的注释需给予格外关注，不当的操作可能会对人身造成伤害。
提醒操作中应注意的事项，不当的操作可能会导致数据丢失或者设备损坏。
为确保设备配置成功或者正常工作而需要特别关注的操作或信息。
对操作内容的描述进行必要的补充和说明。
配置、操作、或使用设备的技巧、小窍门。

#### 4. 图标约定

本书使用的图标及其含义如下：
该图标及其相关描述文字代表一般网络设备，如路由器、交换机、防火墙等。
该图标及其相关描述文字代表一般意义下的路由器，以及其他运行了路由协议的设备。
该图标及其相关描述文字代表二、三层以太网交换机，以及运行了二层协议的设备。
该图标及其相关描述文字代表无线控制器、无线控制器业务板和有线无线一体化交换机的无线控制引擎设备。
该图标及其相关描述文字代表无线接入点设备。
TT该图标及其相关描述文字代表无线终结单元。
TT该图标及其相关描述文字代表无线终结者。
该图标及其相关描述文字代表无线Mesh设备。
该图标代表发散的无线射频信号。
该图标代表点到点的无线射频信号。
该图标及其相关描述文字代表防火墙、UTM、多业务安全网关、负载均衡等安全设备。
该图标及其相关描述文字代表防火墙插卡、负载均衡插卡、NetStream插卡、SSL VPN插卡、IPS插卡、ACG插卡等安全插卡。

#### 5. 示例约定

由于设备型号不同、配置不同、版本升级等原因，可能造成本手册中的内容与用户使用的设备显示信息不一致。实际使用中请以设备显示的内容为准。
本手册中出现的端口编号仅作示例，并不代表设备上实际具有此编号的端口，实际使用中请以设备上存在的端口编号为准。

### 资料意见反馈

如果您在使用过程中发现产品资料的任何问题，可以通过以下方式反馈：
E-mail：info@h3c.com感谢您的反馈，让我们做得更好！

## 01-AAA配置

目 录简介认证、授权、计费方法协议规范配置本地用户配置网络接入类本地用户属性本地用户及本地用户组显示和维护配置EAP认证方案配置 认证服务器

配置RADIUS服务器的状态配置发送 报文的最大尝试次数配置 的检查方式配置RADIUS属性解释功能配置 告警功能配置 计费服务器HWTACACS显示和维护

配置LDAP服务器IP地址配置 用户属性参数指定 认证服务器创建ISP域配置 域的状态域显示和维护配置RADIUS用户

配置连接记录策略连接记录策略显示和维护用户的 认证、 授权、 计费配置设备作为RADIUS服务器对 802.1X用户进行认证和授权配置附录

### 1 AAA

1 AAA

#### 1.1 AAA简介

##### 1.1.1 AAA实现的功能

AAA（Authentication、Authorization、Accounting，认证、授权、计费）是网络安全的一种管理机制，提供了认证、授权、计费三种安全功能。
• 认证：确认访问网络的远程用户的身份，判断访问者是否为合法的网络用户。
• 授权：对不同用户赋予不同的权限，限制用户可以使用的服务。例如，管理员授权办公用户才能对服务器中的文件进行访问和打印操作，而其它临时访客不具备此权限。
• 计费：记录用户使用网络服务过程中的所有操作，包括使用的服务类型、起始时间、数据流量等，用于收集和记录用户对网络资源的使用情况，并可以实现针对时间、流量的计费需求，也对网络起到监视作用。

##### 1.1.2 AAA基本组网结构

AAA采用客户端/服务器结构，客户端运行于NAS（Network Access Server，网络接入服务器）上，负责验证用户身份与管理用户接入，服务器上则集中管理用户信息。AAA的基本组网结构如 图 1-1。
图1-1 AAA 基本组网结构示意图当用户想要通过 获得访问其它网络的权利或取得某些网络资源的权利时，首先需要通过NAS AAA认证，而 NAS 就起到了验证用户的作用。NAS 负责把用户的认证、授权、计费信息透传给服务器。
服务器根据自身的配置对用户的身份进行判断并返回相应的认证、授权、计费结果。NAS 根据服务器返回的结果，决定是否允许用户访问外部网络、获取网络资源。
AAA 可以通过多种协议来实现，这些协议规定了 NAS 与服务器之间如何传递用户信息。目前设备支持 RADIUS（Remote Service，远程认证拨号用户服务）协议、Authentication Dial-In User HWTACACS（HW Terminal Access Controller Access Control System，HW 终端访问控制器控制系统协议）协议和 LDAP（Lightweight Directory Access Protocol，轻量级目录访问协议）协议，在实际应用中，最常使用 RADIUS 协议。

用户可以根据实际组网需求来决定认证、授权、计费功能分别由使用哪种协议类型的服务器来承担。
例如，可以选择 服务器实现认证和授权，RADIUS 服务器实现计费。
HWTACACS当然，用户也可以只使用 提供的一种或两种安全服务。例如，公司仅仅想让员工在访问某些AAA特定资源时进行身份认证，则网络管理员只需要配置认证服务器。但是若希望对员工使用网络的情况进行记录，那么还需要配置计费服务器。
目前，设备支持动态口令认证机制。

##### 1.1.3 RADIUS协议简介

RADIUS（Remote Service，远程认证拨号用户服务）是一种分布式的、Authentication Dial-In User客户端/服务器结构的信息交互协议，能保护网络不受未授权访问的干扰，常应用在既要求较高安全性、又允许远程用户访问的各种网络环境中。RADIUS 协议合并了认证和授权的过程，它定义了的报文格式及其消息传输机制，并规定使用 作为封装 报文的传输层协议，RADIUS UDP RADIUS UDP 端口 1812、1813 分别作为认证/授权、计费端口。
RADIUS 最初仅是针对拨号用户的 AAA 协议，后来随着用户接入方式的多样化发展，RADIUS 也适应多种用户接入方式，如以太网接入、ADSL 接入。它通过认证授权来提供接入服务，通过计费来收集、记录用户对网络资源的使用。

###### 1. 客户端/服务器模式

客户端：RADIUS 客户端一般位于 上，可以遍布整个网络，负责将用户信息传输到指定
• NAS的 RADIUS 服务器，然后根据服务器返回的信息进行相应处理（如接受/拒绝用户接入）。
• 服务器：RADIUS 服务器一般运行在中心计算机或工作站上，维护用户的身份信息和与其相关的网络服务信息，负责接收 NAS 发送的认证、授权、计费请求并进行相应的处理，然后给NAS 返回处理结果（如接受/拒绝认证请求）。另外，RADIUS 服务器还可以作为一个代理，以 客户端的身份与其它的 认证服务器进行通信，负责转发 认证和RADIUS RADIUS RADIUS计费报文。
RADIUS服务器通常要维护三个数据库，如 图 1-2 所示：
图1-2 RADIUS 服务器的组成“Users”：用于存储用户信息（如用户名、口令以及使用的协议、IP 地址等配置信息）。
•“Clients”：用于存储 RADIUS 客户端的信息（如 NAS 的共享密钥、IP 地址等）。
•
• “Dictionary”：用于存储 RADIUS 协议中的属性和属性值含义的信息。

###### 2. 安全的消息交互机制

客户端和 服务器之间认证消息的交互是通过共享密钥的参与来完成的。共享密钥RADIUS RADIUS是一个带外传输的客户端和服务器都知道的字符串，不需要单独进行网络传输。RADIUS 报文中有一个 16 字节的验证字字段，它包含了对整个报文的数字签名数据，该签名数据是在共享密钥的参

与下利用 MD5 算法计算出的。收到 RADIUS 报文的一方要验证该签名的正确性，如果报文的签名不正确，则丢弃它。通过这种机制，保证了 客户端和 服务器之间信息交互的安RADIUS RADIUS全性。另外，为防止用户密码在不安全的网络上传递时被窃取，在 RADIUS 报文传输过程中还利用共享密钥对用户密码进行了加密。

###### 3. 用户认证机制

服务器支持多种方法来认证用户，例如 PAP（Password Protocol，密码认RADIUS Authentication证协议）、CHAP（Challenge Handshake Authentication Protocol，质询握手认证协议）以及 EAP（Extensible Authentication Protocol，可扩展认证协议）。

###### 4. RADIUS的基本消息交互流程

用户、RADIUS客户端和RADIUS服务器之间的交互流程如 图 1-3 所示。
图1-3 RADIUS 的基本消息交互流程消息交互流程如下：
(1) 用户发起连接请求，向 RADIUS 客户端发送用户名和密码。
(2) RADIUS 客户端根据获取的用户名和密码，向 RADIUS 服务器发送认证请求包（Access-Request），其中的密码在共享密钥的参与下利用 MD5 算法进行加密处理。
(3) RADIUS 服务器对用户名和密码进行认证。如果认证成功，RADIUS 服务器向 RADIUS 客户端发送认证接受包（Access-Accept）；如果认证失败，则返回认证拒绝包（Access-Reject）。
由于 协议合并了认证和授权的过程，因此认证接受包中也包含了用户的授权信息。
RADIUS客户端根据接收到的认证结果接入 拒绝用户。如果允许用户接入，则 客户
(4) RADIUS / RADIUS端向 RADIUS 服务器发送计费开始请求包（Accounting-Request）。
(5) RADIUS 服务器返回计费开始响应包（Accounting-Response），并开始计费。
(6) 用户开始访问网络资源。

(7) 用户请求断开连接。
(8) RADIUS 客户端向 RADIUS 服务器发送计费停止请求包（Accounting-Request）。
(9) RADIUS 服务器返回计费结束响应包（Accounting-Response），并停止计费。
(10) 通知用户结束访问网络资源。

###### 5. RADIUS报文结构

RADIUS采用UDP报文来传输消息，通过定时器机制、重传机制、备用服务器机制，确保RADIUS服务器和客户端之间交互消息的正确收发。RADIUS报文结构如 图 1-4 所示。
图1-4 RADIUS 报文结构各字段的解释如下：
(1) Code 域长度为 1 个字节，用于说明RADIUS报文的类型，如 表 1-1 所示。
表1-1 域的主要取值说明Code

|  | Code |  |  | 报文类型 |  |  | 报文说明 |  |
|---|---|---|---|---|---|---|---|---|
|  |  |  | Access-Request认证请求包 |  |  |  |  |  |
|  |  |  | Access-Accept认证接受包 |  |  |  |  |  |
|  |  |  | Access-Reject认证拒绝包 |  |  |  |  |  |
|  |  |  | Accounting-Request 计费请求包 |  |  |  |  |  |
|  |  |  | Accounting-Respons e计费响应包 |  |  |  |  |  |

域
(2) Identifier长度为 个字节，用于匹配请求包和响应包，以及检测在一段时间内重发的请求包。对于类1型一致且属于同一个交互过程的请求包和响应包，该 Identifier 值相同。
(3) Length 域

长度为 2 个字节，表示 RADIUS 数据包（包括 Code、Identifier、Length、Authenticator 和Attribute）的长度，单位为字节。超过 域的字节将作为填充字符被忽略。如果接收到Length的包的实际长度小于 Length 域的值时，则包会被丢弃。
(4) Authenticator 域长度为 16 个字节，用于验证 RADIUS 服务器的应答报文，另外还用于用户密码的加密。
Authenticator 包括两种类型：Request Authenticator 和 Response Authenticator。
(5) Attribute 域不定长度，用于携带专门的认证、授权和计费信息。Attribute 域可包括多个属性，每一个属性都采用（Type、Length、Value）三元组的结构来表示。
类型（Type）：表示属性的类型。
(cid:123)
长度（Length）：表示该属性（包括类型、长度和属性值）的长度，单位为字节。
(cid:123)
属性值（Value）：表示该属性的信息，其格式和内容由类型决定。
(cid:123)

###### 6. RADIUS扩展属性

RADIUS 协议具有良好的可扩展性，RFC 2865 中定义的 26 号属性（Vendor-Specific）用于设备厂商对 RADIUS 进行扩展，以实现标准 RADIUS 没有定义的功能。
设备厂商可以在 号属性中封装多个自定义的（Type、Length、Value）子属性，以提供更多的扩26展功能。26 号属性的格式如 图 1-5 所示：
• Vendor-ID，表示厂商代号，最高字节为 0，其余 3 字节的编码见 RFC 1700。
• Vendor-Type，表示子属性类型。
• Vendor-Length，表示子属性长度。
• Vendor-Data，表示子属性的内容。
设备支持的RADIUS扩展属性的Vendor-ID为 25506，属性的具体介绍请参见“1.18.3 附录C RADIUS扩展属性（Vendor-ID=25506）”。
图1-5 号属性的格式26

##### 1.1.4 HWTACACS协议简介

HWTACACS（HW Terminal Access Controller Access Control System，HW 终端访问控制器控制系统协议）是在 （ ）基础上进行了功能增强的安全协议。该协议与 协TACACS RFC 1492 RADIUS议类似，采用客户端/服务器模式实现 NAS 与 HWTACACS 服务器之间的通信。
HWTACACS 协议主要用于 PPP（Point-to-Point Protocol，点对点协议）和 VPDN（Virtual Private Dial-up Network，虚拟专用拨号网络）接入用户及终端用户的认证、授权和计费。其典型应用是对

需要登录到 NAS 设备上进行操作的终端用户进行认证、授权以及对终端用户执行的操作进行记录。
设备作为 的客户端，将用户名和密码发给 服务器进行验证，用户验证通HWTACACS HWTACACS过并得到授权之后可以登录到设备上进行操作，HWTACACS 服务器上会记录用户对设备执行过的命令。

###### 1. HWTACACS协议与RADIUS协议的区别

HWTACACS协议与RADIUS协议都实现了认证、授权和计费功能，它们有很多相似点：结构上都采用客户端/服务器模式；都使用共享密钥对传输的用户信息进行加密；都有较好的灵活性和可扩展性。两者之间存在的主要区别如 表 1-2 所示。
表1-2 协议和 协议区别HWTACACS RADIUS HWTACACS 协议 RADIUS 协议使用TCP，网络传输更可靠 使用UDP，网络传输效率更高除了HWTACACS报文头，对报文主体全部进行加密 只对认证报文中的密码字段进行加密协议报文较为复杂，认证和授权分离，使得认证、授权服务可以分离在不同的服务器上实现。例如，可以用一协议报文比较简单，认证和授权结合，难以分离个HWTACACS服务器进行认证，另外一个HWTACACS服务器进行授权支持对设备的配置命令进行授权使用。用户可使用的命 不支持对设备的配置命令进行授权使用令行受到用户角色和AAA授权的双重限制，某角色的用用户登录设备后可以使用的命令行由用户所具有的角户输入的每一条命令都需要通过HWTACACS服务器授色决定，关于用户角色的相关介绍请参见“基础配置指权，如果授权通过，命令就可以被执行导”中的“RBAC”

###### 2. HWTACACS的基本消息交互流程

下面以Telnet用户为例，说明使用HWTACACS对用户进行认证、授权和计费的过程。基本消息交互流程图如 图 1-6 所示。

图1-6 Telnet 用户认证、授权和计费流程图基本消息交互流程如下：
(1) Telnet 用户请求登录设备。
(2) HWTACACS 客户端收到请求之后，向 HWTACACS 服务器发送认证开始报文。
(3) HWTACACS 服务器发送认证回应报文，请求用户名。
(4) HWTACACS 客户端收到回应报文后，向用户询问用户名。
(5) 用户输入用户名。
(6) HWTACACS 客户端收到用户名后，向 HWTACACS 服务器发送认证持续报文，其中包括了用户名。
(7) HWTACACS 服务器发送认证回应报文，请求登录密码。

(8) HWTACACS 客户端收到回应报文，向用户询问登录密码。
(9) 用户输入密码。
(10) HWTACACS 客户端收到登录密码后，向 HWTACACS 服务器发送认证持续报文，其中包括
了登录密码。
如果认证成功，HWTACACS 服务器发送认证回应报文，指示用户通过认证。
(11)
客户端向 服务器发送授权请求报文。
(12) HWTACACS HWTACACS
(13) 如果授权成功，HWTACACS 服务器发送授权回应报文，指示用户通过授权。
(14) HWTACACS 客户端收到授权成功报文，向用户输出设备的配置界面，允许用户登录。
(15) HWTACACS 客户端向 HWTACACS 服务器发送计费开始报文。
(16) HWTACACS 服务器发送计费回应报文，指示计费开始报文已经收到。
(17) 用户请求断开连接。
(18) HWTACACS 客户端向 HWTACACS 服务器发送计费结束报文。
(19) HWTACACS 服务器发送计费结束报文，指示计费结束报文已经收到。

##### 1.1.5 LDAP协议简介

LDAP（Lightweight Protocol，轻量级目录访问协议）是一种目录访问协议，用于Directory Access提供跨平台的、基于标准的目录服务。它是在 X.500 协议的基础上发展起来的，继承了 X.500 的优点，并对 X.500 在读取、浏览和查询操作方面进行了改进，适合于存储那些不经常改变的数据。
LDAP 协议的典型应用是用来保存系统中的用户信息，如 Microsoft 的 Windows 操作系统就使用了Active Directory Server（一种 LDAP 服务器软件）来保存操作系统的用户、用户组等信息，用于用户登录 时的认证和授权。
Windows

###### 1. LDAP目录服务

LDAP 中使用目录记录并管理系统中的组织信息、人员信息以及资源信息。目录按照树型结构组织，由多个条目（Entry）组成的。条目是具有 DN（Distinguished Name，识别名）的属性（Attribute）
集合。属性用来承载各种类型的数据信息，例如用户名、密码、邮件、计算机名、联系电话等。
LDAP 协议基于 Client/Server 结构提供目录服务功能，所有的目录信息数据存储在 LDAP 服务器上。
目前，Microsoft 的 Active Directory Server、IBM 的 Tivoli Directory Server 和 Sun 的 Sun ONE Directory Server 都是常用的 LDAP 服务器软件。

###### 2. 使用LDAP协议进行认证和授权

AAA 可以使用 LDAP 协议对用户提供认证和授权服务。LDAP 协议中定义了多种操作来实现 LDAP的各种功能，用于认证和授权的操作主要为绑定和查询。
绑定操作的作用有两个：一是与 服务器建立连接并获取 服务器的访问权限。二
• LDAP LDAP是用于检查用户信息的合法性。
• 查询操作就是构造查询条件，并获取 LDAP 服务器的目录资源信息的过程。
使用 协议进行认证时，其基本的工作流程如下：
LDAP客户端使用 服务器管理员 与 服务器进行绑定，与 服务器建立
(1) LDAP LDAP DN LDAP LDAP连接并获得查询权限。
(2) LDAP 客户端使用认证信息中的用户名构造查询条件，在 LDAP 服务器指定根目录下查询此用户，得到用户的 DN。

(3) LDAP 客户端使用用户 DN 和用户密码与 LDAP 服务器进行绑定，检查用户密码是否正确。
使用 LDAP 协议进行授权的过程与认证过程相似，首先必须通过与 LDAP 服务器进行绑定，建立与
服务器的连接，然后在此连接的基础上通过查询操作得到用户的授权信息。与认证过程稍有不同的
是，授权过程不仅仅会查询用户 DN，还会同时查询相应的 LDAP 授权信息。

###### 3. LDAP认证的基本消息交互流程

下面以Telnet用户登录设备为例，说明如何使用LDAP认证服务器来对用户进行认证。用户的LDAP认证基本消息交互流程如 图 1-7 所示。
图1-7 LDAP 认证的基本消息交互流程基本消息交互流程如下：
(1) 用户发起连接请求，向 LDAP 客户端发送用户名和密码。
(2) LDAP 客户端收到请求之后，与 LDAP 服务器建立 TCP 连接。
(3) LDAP 客户端以管理员 DN 和管理员 DN 密码为参数向 LDAP 服务器发送管理员绑定请求报文（Administrator Bind Request）获得查询权限。
(4) LDAP 服务器进行绑定请求报文的处理。如果绑定成功，则向 LDAP 客户端发送绑定成功的回应报文。
(5) LDAP 客户端以输入的用户名为参数，向 LDAP 服务器发送用户 DN 查询请求报文（User DN Search Request）。
服务器收到查询请求报文后，根据报文中的查询起始地址、查询范围、以及过滤条件，
(6) LDAP对用户 DN 进行查找。如果查询成功，则向 LDAP 客户端发送查询成功的回应报文。查询得到的用户 DN 可以是一或多个。
(7) LDAP 客户端以查询得到的用户 DN 和用户输入的密码为参数，向 LDAP 服务器发送用户 DN绑定请求报文（User Request），检查用户密码是否正确。
DN Bind

(8) LDAP 服务器进行绑定请求报文的处理。
如果绑定成功，则向 LDAP 客户端发送绑定成功的回应报文。
•
如果绑定失败，则向 LDAP 客户端发送绑定失败的回应报文。LDAP 客户端以下一个查询到的
•
用户 DN（如果存在的话）为参数，继续向服务器发送绑定请求，直至有一个 绑定成功，
DN
或者所有 DN 均绑定失败。如果所有用户 DN 都绑定失败，则 LDAP 客户端通知用户登录失败
并拒绝用户接入。
(9) LDAP客户端保存绑定成功的用户DN，并进行授权处理。如果设备采用LDAP授权方案，则进
行 图 1-8 所示的用户授权交互流程；如果设备采用非LDAP的授权方案，则执行其它协议的授
权处理流程，此处略。
授权成功之后，LDAP 客户端通知用户登录成功。
(10)

###### 4. LDAP授权的基本消息交互流程

下面以Telnet用户登录设备为例，说明如何使用LDAP服务器来对用户进行授权。用户的LDAP授权基本消息交互流程如 图 1-8 所示。
图1-8 LDAP 授权的基本消息交互流程
(1) 用户发起连接请求，向 LDAP 客户端发送用户名和密码。
(2) LDAP客户端收到请求之后，进行认证处理。如果设备采用LDAP认证方案，则按照 图 1-7 所示进行LDAP认证。LDAP认证流程完成之后，如果已经和该LDAP授权服务器建立了绑定关系，则直接转到步骤（6），否则转到步骤（4）；如果设备采用非LDAP认证方案，则执行其它协议的认证处理流程，之后转到步骤（3）。
(3) LDAP 客户端与 LDAP 服务器建立 TCP 连接。
客户端以管理员 和管理员 密码为参数向 服务器发送管理员绑定请求报文
(4) LDAP DN DN LDAP（ Administrator Bind Request ）获得查询权限。
(5) LDAP 服务器进行绑定请求报文的处理。如果绑定成功，则向 LDAP 客户端发送绑定成功的回应报文。

###### 1. 认证方法

(6) LDAP 客户端以输入的用户名为参数（如果用户认证使用的是相同 LDAP 服务器，则以保存的
绑定成功的用户 为参数），向 服务器发送授权查询请求报文。
DN LDAP
服务器收到查询请求报文后，根据报文中的查询起始地址、查询范围、过滤条件以及
(7) LDAP
LDAP 客户端关心的 LDAP 属性，对用户信息进行查找。如果查询成功，则向 LDAP 客户端
发送查询成功的回应报文。
(8) 授权成功后，LDAP 客户端通知用户登录成功。

##### 1.1.6 基于域的用户管理

NAS对用户的管理是基于ISP（Internet Provider，互联网服务提供商）域的，每个用户都Service属于一个ISP域。一般情况下，用户所属的ISP域是由用户登录时提供的用户名决定的，如 图 1-9所示。
图1-9 用户名决定域名为便于对不同接入方式的用户进行区分管理，提供更为精细且有差异化的认证、授权、计费服务，AAA 将用户划分为以下几个类型：
• lan-access 用户：LAN 接入用户，如 802.1X 认证、MAC 地址认证用户。
• login 用户：登录设备用户，如 SSH、Telnet、FTP、终端接入用户（即从 Console 口登录的用户）。
• Portal 接入用户。
• HTTP/HTTPS 用户：使用 HTTP 或 HTTPS 服务登录设备的用户。
对于某些接入方式，用户最终所属的 ISP 域可由相应的认证模块（例如 802.1X）提供命令行来指定，用于满足一定的用户认证管理策略。

##### 1.1.7 认证、授权、计费方法

在具体实现中，一个 域对应着设备上一套实现 的配置策略，它们是管理员针对该域用户ISP AAA制定的一套认证、授权、计费方法，可根据用户的接入特征以及不同的安全需求组合使用。
认证方法
1.
AAA 支持以下认证方法：
• 不认证：对用户非常信任，不对其进行合法性检查，一般情况下不采用这种方法。

本地认证：认证过程在接入设备上完成，用户信息（包括用户名、密码和各种属性）配置在
•接入设备上。优点是速度快，可以降低运营成本；缺点是存储信息量受设备硬件条件限制。
远端认证：认证过程在接入设备和远端的服务器之间完成，接入设备和远端服务器之间通过
•RADIUS、HWTACACS 或 LDAP 协议通信。优点是用户信息集中在服务器上统一管理，可实现大容量、高可靠性、支持多设备的集中式统一认证。当远端服务器无效时，可配置备选认证方式完成认证。

###### 2. 授权方法

AAA 支持以下授权方法：
不授权：接入设备不请求授权信息，不对用户可以使用的操作以及用户允许使用的网络服务
•进行授权。此时，认证通过的 login 用户只有系统给予的缺省用户角色 level-0，其中FTP/SFTP/SCP 用户的工作目录是设备的根目录，但并无访问权限；认证通过的非 login 用户，可直接访问网络。关于用户角色 的详细介绍请参见“基础配置指导”中的“RBAC”。
level-0本地授权：授权过程在接入设备上进行，根据接入设备上为本地用户配置的相关属性进行授
•权。
• 远端授权：授权过程在接入设备和远端服务器之间完成。RADIUS 协议的认证和授权是绑定在一起的，不能单独使用 RADIUS 进行授权。RADIUS 认证成功后，才能进行授权，RADIUS授权信息携带在认证回应报文中下发给用户。HWTACACS/LDAP 协议的授权与认证相分离，在认证成功后，授权信息通过授权报文进行交互。当远端服务器无效时，可配置备选授权方式完成授权。

###### 3. 计费方法

AAA 支持以下计费方法：
• 不计费：不对用户计费。
• 本地计费：计费过程在接入设备上完成，实现了本地用户连接数的统计和限制，并没有实际的费用统计功能。
• 远端计费：计费过程在接入设备和远端的服务器之间完成。当远端服务器无效时，可配置备选计费方式完成计费。

##### 1.1.8 AAA的扩展应用

对于 login 用户， AAA 还可以对其提供以下服务，用于提高对设备操作的安全性：
• 命令行授权：用户执行的每一条命令都需要接受授权服务器的检查，只有授权成功的命令才被允许执行。关于命令行授权的详细介绍请参考“基础配置指导”中的“配置用户通过 CLI登录设备”。
命令行计费：若未开启命令行授权功能，则计费服务器对用户执行过的所有有效命令进行记
•录；若开启了命令行授权功能，则计费服务器仅对授权通过的命令进行记录。关于命令行计费的详细介绍请参考“基础配置指导”中的“配置用户通过 CLI 登录设备”。
• 用户角色切换认证：在不退出当前登录、不断开当前连接的前提下，用户将当前的用户角色切换为其它用户角色时，只有通过服务器的认证，该切换操作才被允许。关于用户角色切换的详细介绍请参考“基础配置指导”中的“RBAC”。

##### 1.1.9 AAA支持VPN多实例

通过AAA支持VPN多实例，可实现认证/授权/计费报文在VPN之间的交互。如 图 所示，各私网1-10客户端之间业务隔离，连接客户端的MCE设备作为NAS，通过VPN网络把私网客户端的认证/授权/计费信息透传给网络另一端的私网服务器，实现了对私网客户端的集中认证，且各私网的认证报文互不影响。
图1-10 AAA 支持 VPN 多实例典型组网图在 MCE 设备上进行的 Portal 接入认证在本特性的配合下，也可支持多实例功能。关于 MCE 的相关介绍请见参见“MCE 配置指导”中的“MCE”。关于 的相关介绍请参见“安全配置指导”Portal中的“Portal”。

##### 1.1.10 设备的RADIUS服务器功能

设备的 RADIUS 服务器功能是指，设备作为 RADIUS 服务器端与 RADIUS 的客户端配合完成用户的认证和授权等功能。作为 RADIUS 服务器的设备，既可以独立于 RADIUS 客户端，也可以与客户端位于同一台设备上。
RADIUS设备支持RADIUS服务器功能给RADIUS的应用提供了更多便利，一方面，使得用户组网方式更加灵活，另一方面，可减少用户专门部署RADIUS服务器的组网成本。该功能的典型组网如 图 1-11所示。通过在汇聚层设备上配置RADIUS服务器功能，并在接入层设备上部署相应的认证方案，实现对用户的认证和授权。

图1-11 RADIUS 服务器功能典型组网设备作为 RADIUS 服务器可以实现如下功能：
• RADIUS 用户信息管理：通过本地用户配置实现，可管理的用户信息包括用户名、密码、授权 ACL、授权 VLAN、过期截止时间以及描述信息。
• RADIUS 客户端信息管理：支持创建、删除及修改 RADIUS 客户端。RADIUS 客户端以 IP 地址为标识，并具有共享密钥等属性。RADIUS 服务器通过配置指定被管理的 RADIUS 客户端，并只处理来自其管理范围内的客户端的 报文，对其它报文直接作丢弃处理。
RADIUS对网络接入类用户的 认证和授权功能。暂不支持 计费功能。
• RADIUS RADIUS作为 RADIUS 服务器的设备接收到 RADIUS 报文后，首先检查 RADIUS 客户端是否在可管理的范围内，并使用共享密钥检验报文的合法性，然后依次检查用户帐号是否存在、用户口令是否正确，以及用户的其它属性是否满足要求，例如帐号是否在有效期内，最后决定是否允许用户通过认证，并对认证通过的用户授予对应的权限。
• 设备作为 RADIUS 服务器时，认证端口为 UDP 端口 1812，不可修改。
• 设备的 RADIUS 服务器功能只支持 IPv4 组网，不支持 IPv6 组网。
• 设备的 RADIUS 服务器功能只支持 PAP 和 CHAP 认证机制。
• 设备的 RADIUS 服务器功能不支持用户名中携带域名。

##### 1.1.11 协议规范

与 AAA、RADIUS、HWTACACS、LDAP 相关的协议规范有：
• RFC 2865：Remote Authentication Dial In User Service (RADIUS)
• RFC 2866：RADIUS Accounting
• RFC 2867：RADIUS Accounting Modifications for Tunnel Protocol Support
• RFC 2868：RADIUS Attributes for Tunnel Protocol Support
• RFC 2869：RADIUS Extensions

RFC 3576：Dynamic Authorization Extensions to Remote Authentication Dial In User
•Service (RADIUS)
4818：RADIUS
• RFC Delegated-IPv6-Prefix Attribute 5176：Dynamic
• RFC Authorization Extensions to Remote Authentication Dial In User Service (RADIUS)
• RFC 1492：An Access Control Protocol, Sometimes Called TACACS
• RFC 1777：Lightweight Directory Access Protocol
• RFC 2251：Lightweight Directory Access Protocol (v3)

#### 1.2 FIPS相关说明

设备运行于 模式时，本特性部分配置相对于非 模式有所变化，具体差异请见本文相关描FIPS FIPS述。有关 FIPS 模式的详细介绍请参见“安全配置指导”中的“FIPS”。

#### 1.3 AAA配置任务简介

配置任务如下：
AAA配置 方案
(1) AAA若选择使用本地 AAA 方案，则需要配置本地用户；若选择使用远程 AAA 方案，则需要配置RADIUS、HWTACACS 或 LDAP。
配置本地用户(cid:123)
配置RADIUS (cid:123)
配置HWTACACS (cid:123)
配置LDAP (cid:123)
创建 域并配置相关属性
(2) ISP
a. 创建ISP域
b. 配置ISP域的属性
(3) 在ISP域中配置实现AAA的方法请根据实际需求为用户所在的 ISP 域配置实现认证、授权、计费的方法，这些方法中将会引用已经配置的 方案。
AAA配置ISP域的AAA认证方法(cid:123)
配置ISP域的AAA授权方法(cid:123)
配置ISP域的AAA计费方法(cid:123)
(4) （可选）配置 AAA 高级功能限制同时在线的最大用户连接数(cid:123)
配置NAS-ID (cid:123)
配置设备 ID (cid:123)
配置设备作为RADIUS服务器(cid:123)
配置连接记录策略(cid:123)

#### 1.4 配置本地用户

##### 1.4.1 本地用户简介

当选择使用本地认证、本地授权、本地计费方法对用户进行认证、授权或计费时，应在设备上创建本地用户并配置相关属性。
所谓本地用户，是指在本地设备上设置的一组用户属性的集合。该集合以用户名和用户类别为用户的唯一标识。本地用户分为两类，一类是设备管理用户；另一类是网络接入用户。设备管理用户供设备管理员登录设备使用，网络接入用户供通过设备访问网络服务的用户使用。
为使某个请求网络服务的用户可以通过本地认证，需要在设备上的本地用户数据库中添加相应的表项。具体步骤是，创建一个本地用户并进入本地用户视图，然后在本地用户视图下配置相应的用户属性，可配置的用户属性包括：
描述信息
•服务类型
•用户可使用的网络服务类型。该属性是本地认证的检测项，如果没有用户可以使用的服务类型，则该用户无法通过认证。
用户状态
•用于指示是否允许该用户请求网络服务器，包括 active 和 block 两种状态。active 表示允许该用户请求网络服务，block 表示禁止该用户请求网络服务。
最大用户数
•使用当前用户名接入设备的最大用户数目。若当前该用户名的接入用户数已达最大值，则使用该用户名的新用户将被禁止接入。
• 所属的用户组每一个本地用户都属于一个本地用户组，并继承组中的所有属性（密码管理属性和用户授权属性）。关于本地用户组的介绍和配置请参见“1.4.5 配置用户组属性”。
• 绑定属性用户认证时需要检测的属性，用于限制接入用户的范围。若用户的实际属性与设置的绑定属性不匹配，则不能通过认证，因此在配置绑定属性时要考虑该用户是否需要绑定某些属性。
• 用户授权属性用户认证通过后，接入设备给用户下发授权属性。由于可配置的授权属性都有其明确的使用环境和用途，因此配置授权属性时要考虑该用户是否需要某些属性。
本地用户的授权属性在用户组和本地用户视图下都可以配置，且本地用户视图下的配置优先级高于用户组视图下的配置。用户组的配置对组内所有本地用户生效。
密码管理属性
•用户密码的安全属性，可用于对本地用户的认证密码进行管理和控制。可设置的策略包括：
密码老化时间、密码最小长度、密码组合策略、密码复杂度检查策略和用户登录尝试次数限制策略。
本地用户的密码管理属性在系统视图（具有全局性）、用户组视图和本地用户视图下都可以配置，其生效的优先级顺序由高到底依次为本地用户、用户组、全局。全局配置对所有本地用户生效，用户组的配置对组内所有本地用户生效。有关密码管理以及全局密码配置的详细介绍请参见“安全配置指导”中的“Password Control”。

有效期
•网络接入类本地用户在有效期内才能认证成功。

##### 1.4.2 本地用户配置任务简介

本地用户配置任务如下：
(1) 配置本地用户属性配置设备管理类本地用户属性(cid:123)
配置网络接入类本地用户属性(cid:123)
（可选）配置用户组属性
(2)
（可选）配置本地用户过期自动删除功能
(3)

##### 1.4.3 配置设备管理类本地用户属性

###### 1. 配置限制和指导

开启设备管理类全局密码管理功能（通过命令 enable）后，设备上将不显password-control示配置的本地用户密码，也不会将该密码保存在当前配置中。如果关闭了设备管理类全局密码管理功能，已配置的密码将恢复在当前配置中。当前配置可通过 display current-configuration命令查看。
授权属性和密码控制属性均可以在本地用户视图和用户组视图下配置，各视图下的配置优先级顺序从高到底依次为：本地用户视图-->用户组视图。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 添加设备管理类本地用户，并进入设备管理类本地用户视图。
local-user user-name class manage
(3) 设置本地用户的密码。
（非 FIPS 模式）
password [ { hash | simple } string ]
可以不为本地用户设置密码。为提高用户帐户的安全性，建议设置本地用户密码。
（FIPS 模式）
password
必须且只能通过交互式方式设置明文密码，否则用户的本地认证不能成功。
(4) 设置本地用户可以使用的服务类型。
（非 FIPS 模式）
service-type { ftp | { http | https | ssh | telnet | terminal } * }
（ FIPS 模式）
service-type { https | ssh | terminal } *
缺省情况下，本地用户不能使用任何服务类型。
(5) （可选）设置本地用户的状态。

state { active | block }缺省情况下，本地用户处于活动状态，即允许该用户请求网络服务。
(6) （可选）设置使用当前本地用户名接入设备的最大用户数。
access-limit max-user-number缺省情况下，不限制使用当前本地用户名接入的用户数。
由于 FTP/SFTP/SCP 用户不支持计费，因此 FTP/SFTP/SCP 用户不受此属性限制。
(7) （可选）设置本地用户的授权属性。
authorization-attribute { idle-cut minutes | user-role role-name | work-directory directory-name } *缺省情况下：
授权 FTP/SFTP/SCP 用户可以访问的目录为设备的根目录，但无访问权限。
(cid:123)
由用户角色为 network-admin 或者 level-15 的用户创建的本地用户被授权用户角色(cid:123)
network-operator。
(8) （可选）设置设备管理类本地用户的密码管理属性。请至少选择其中一项进行配置。
设置密码老化时间。
(cid:123)
password-control aging aging-time设置密码最小长度。
(cid:123)
password-control length length设置密码组合策略。
(cid:123)
password-control composition type-number type-number [ type-length type-length ]设置密码的复杂度检查策略。
(cid:123)
password-control complexity { same-character | user-name } check设置用户登录尝试次数以及登录尝试失败后的行为。
(cid:123)
password-control login-attempt login-times [ exceed { lock | lock-time time | unlock } ]缺省情况下，采用本地用户所属用户组的密码管理策略。
(9) （可选）设置本地用户所属的用户组。
group group-name缺省情况下，本地用户属于用户组 system。

##### 1.4.4 配置网络接入类本地用户属性

###### 1. 配置限制和指导

开启网络接入类全局密码管理功能（通过命令 password-control enable network-class）
后，设备上将不显示配置的本地用户密码，也不会将该密码保存在当前配置中。如果关闭了网络接入类全局密码管理功能，已配置的密码将恢复在当前配置中。当前配置可通过 display current-configuration 命令查看。
授权属性和密码控制属性均可以在本地用户视图和用户组视图下配置，各视图下的配置优先级顺序从高到底依次为：本地用户视图-->用户组视图。

###### 2. 配置步骤

在绑定接口属性时要考虑绑定接口类型是否合理。对于不同接入类型的用户，请按照如下方式进行绑定接口属性的配置：
用户：配置绑定的接口为开启 的二层以太网接口。
• 802.1X 802.1X地址认证用户：配置绑定的接口为开启 地址认证的二层以太网接口。
• MAC MAC认证用户：配置绑定的接口为开启 认证的二层以太网接口。
• Web Web用户：若使能 的接口为 接口，且没有通过 portal roaming enable
• Portal Portal VLAN命令配置 Portal 用户漫游功能，则配置绑定的接口为用户实际接入的二层以太网接口；其它情况下，配置绑定的接口均为使能 Portal 的接口。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 添加网络接入类本地用户，并进入网络接入类本地用户视图。
local-user user-name class network
(3) （可选）设置本地用户的密码。
password { cipher | simple } string
(4) （可选）设置本地用户的描述信息。
description text缺省情况下，未配置本地用户的描述信息。
(5) 设置本地用户可以使用的服务类型。
service-type { lan-access | portal }缺省情况下，本地用户不能使用任何服务类型。
（可选）设置本地用户的状态。
(6)
state { active | block }缺省情况下，本地用户处于活动状态，即允许该用户请求网络服务。
（可选）设置使用当前本地用户名接入设备的最大用户数。
(7)
access-limit max-user-number缺省情况下，不限制使用当前本地用户名接入的用户数。
(8) （可选）设置本地用户的绑定属性。
bind-attribute { ip ip-address | location interface interface-type interface-number | mac mac-address | vlan vlan-id } *缺省情况下，未设置本地用户的任何绑定属性。
（可选）设置本地用户的授权属性。
(9)
authorization-attribute { acl acl-number | idle-cut minutes | ip-pool ipv4-pool-name | ipv6-pool ipv6-pool-name | session-timeout minutes | user-profile profile-name | vlan vlan-id } *缺省情况下，本地用户无授权属性。
(10) （可选）设置网络接入类本地用户的密码管理属性。请至少选择其中一项进行配置。
设置密码最小长度。
(cid:123)

password-control length length设置密码组合策略。
(cid:123)
password-control composition type-number type-number [ type-length type-length ]设置密码的复杂度检查策略。
(cid:123)
password-control complexity { same-character | user-name } check缺省情况下，采用本地用户所属用户组的密码管理策略。
(11) （可选）设置本地用户所属的用户组。
group group-name缺省情况下，本地用户属于用户组 system。
(12) （可选）设置本地用户的有效期。
validity-datetime { from start-date start-time to expiration-date expiration-time | from start-date start-time | to expiration-date expiration-time }缺省情况下，未限制本地用户的有效期，该用户始终有效。

##### 1.4.5 配置用户组属性

###### 1. 功能简介

为了简化本地用户的配置，增强本地用户的可管理性，引入了用户组的概念。用户组是一个本地用户属性的集合，某些需要集中管理的属性可在用户组中统一配置和管理，用户组内的所有本地用户都可以继承这些属性。

###### 2. 配置步骤

进入系统视图。
(1)
system-view创建用户组，并进入用户组视图。
(2)
user-group group-name缺省情况下，存在一个用户组，名称为 system。
(3) 设置用户组的授权属性。
authorization-attribute { acl acl-number | idle-cut minutes | ip-pool ipv4-pool-name | ipv6-pool ipv6-pool-name | session-timeout minutes | user-profile profile-name | vlan vlan-id | work-directory directory-name } *缺省情况下，未设置用户组的授权属性。
(4) （可选）设置用户组的密码管理属性。请至少选择其中一项进行配置。
设置密码老化时间。
(cid:123)
password-control aging aging-time设置密码最小长度。
(cid:123)
password-control length length

设置密码组合策略。
(cid:123)
password-control composition type-number type-number [ type-length type-length ]设置密码的复杂度检查策略。
(cid:123)
password-control complexity { same-character | user-name } check设置用户登录尝试次数以及登录尝试失败后的行为。
(cid:123)
password-control login-attempt login-times [ exceed { lock | lock-time time | unlock } ]缺省情况下，采用全局密码管理策略。全局密码管理策略的相关配置请参见“安全配置指导”中的“Password Control”。
1.4.6 配置本地用户过期自动删除功能

###### 1. 功能简介

开启本地用户过期自动删除功能之后，设备将定时（10 分钟，不可配）检查网络接入类本地用户是否过期并自动删除过期的本地用户。

###### 2. 配置步骤

进入系统视图。
(1)
system-view开启本地用户过期自动删除功能。
(2)
local-user auto-delete enable缺省情况下，本地用户过期自动删除功能处于关闭状态。

##### 1.4.7 本地用户及本地用户组显示和维护

完成上述配置后，在任意视图下执行 display 命令可以显示配置后本地用户及本地用户组的运行情况，通过查看显示信息验证配置的效果。
表1-3 本地用户及本地用户组显示和维护操作 命令display local-user [ class { manage | network } | idle-cut { disable | enable } | service-type { ftp | http | https |显示本地用户的配置信息和在线lan-access | portal | ssh | telnet | terminal } | state用户数的统计信息{ active | block } | user-name user-name class { manage | network } | vlan vlan-id ]显示本地用户组的相关配置 display user-group { all | name group-name }

#### 1.5 配置RADIUS

##### 1.5.1 RADIUS配置任务简介

RADIUS 配置任务如下：

(1) 配置EAP认证方案
若要对 RADIUS 认证服务器使用 EAP 认证方法进行可达性探测，则需要配置 EAP 认证方案，
并在 服务器探测模板中引用该方案。
RADIUS
配置RADIUS服务器探测模板
(2)
若要对 认证服务器进行可达性探测，则需要配置 服务器探测模板，并在
RADIUS RADIUS
RADIUS 认证服务器配置中引用该模板。
(3) 创建RADIUS方案
(4) 配置RADIUS认证服务器
配置RADIUS计费服务器
(5)
配置RADIUS报文的共享密钥
(6)
若配置 认证/计费服务器时未指定共享密钥，则可以通过本任务统一指定对所有认证
RADIUS
/计费 RADIUS 服务器生效的共享密钥。
(7) 配置RADIUS方案所属的VPN
若配置 RADIUS 认证 / 计费服务器时未指定所属的 VPN ，则可以通过本任务统一指定所有认证
/计费 RADIUS 服务器所属的 VPN。
(8) （可选）配置RADIUS服务器的状态
(9) （可选）配置RADIUS服务器的定时器
(10) （可选）配置 RADIUS 报文交互参数
配置发送RADIUS报文使用的源IP地址
(cid:123)
配置发送给RADIUS服务器的用户名格式和数据统计单位
(cid:123)
配置发送RADIUS报文的最大尝试次数
(cid:123)
配置允许发起实时计费请求的最大尝试次数
(cid:123)
配置RADIUS报文的DSCP优先级
(cid:123)
（可选）配置 属性参数
(11) RADIUS
配置RADIUS 的检查方式
Attribute 15
(cid:123)
配置RADIUS 的CAR参数解析功能
Attribute 25
(cid:123)
配置RADIUS Attribute 31 中的MAC地址格式
(cid:123)
配置RADIUS Remanent_Volume属性的流量单位
(cid:123)
配置RADIUS属性解释功能
(cid:123)
(12) （可选）配置 RADIUS 扩展功能
配置RADIUS计费报文缓存功能
(cid:123)
配置用户下线时设备强制发送RADIUS计费停止报文
(cid:123)
配置RADIUS服务器负载分担功能
(cid:123)
配置RADIUS的accounting-on功能
(cid:123)
配置RADIUS的session control功能
(cid:123)
配置RADIUS DAE服务器功能
(cid:123)
配置RADIUS告警功能
(cid:123)

###### 4. 配置步骤

##### 1.5.2 RADIUS配置限制和指导

采用设备作为 服务器时，创建的 方案中，仅 认证服务器、RADIUS 报RADIUS RADIUS RADIUS文的共享密钥和发送给 RADIUS 服务器的用户名格式需要配置，其它配置无需关注。

##### 1.5.3 配置EAP认证方案

###### 1. 功能简介

EAP 认证方案是一个 EAP 认证选项的配置集合，用于指定设备采用的 EAP 认证方法以及某些 EAP认证方法需要引用的 CA 证书。

###### 2. 配置限制和指导

一个 认证方案可以同时被多个探测模版引用。
EAP系统最多支持配置 16 个 EAP 认证方案。

###### 3. 配置准备

配置 证书之前，需要通过 或 的方式将证书文件导入设备的存储介质的根目录下。在CA FTP TFTP IRF 组网环境中，需要保证主设备的存储介质的根目录下已经保存了 CA 证书文件。
配置步骤
4.
(1) 进入系统视图。
system-view
(2) 创建 EAP 认证方案，并进入 EAP 认证方案视图。
eap-profile eap-profile-name
(3) 配置 EAP 认证方法。
method { md5 | peap-gtc | peap-mschapv2 | ttls-gtc | ttls-mschapv2 }缺省情况下，采用的 EAP 认证方法为 MD5-Challenge。
(4) 配置当前认证方案要使用的 CA 证书。
ca-file file-name缺省情况下，未配置 CA 证书。
当使用 认证方法为 PEAP-GTC、PEAP-MSCHAPv2、TTLS-GTC、TTLS-MSCHAPv2 EAP时，则需要通过本命令配置使用的 CA 证书，用于校验服务器证书。

##### 1.5.4 配置RADIUS服务器探测模板

###### 1. 功能简介

RADIUS 服务器探测功能是指，设备周期性发送探测报文探测 RADIUS 服务器是否可达或可用：如果服务器不可达，则置服务器状态为 block，如果服务器可达，则置服务器状态为 active。该探测功能不依赖于实际用户的认证过程，无论是否有用户向 服务器发起认证，无论是否有用RADIUS户在线，设备都会自动对指定的 RADIUS 服务器进行探测，便于及时获得该服务器的可达状态。
RADIUS 服务器探测模板用于配置探测参数，并且可以被 RADIUS 方案视图下的 RADIUS 服务器配置引用。
目前，设备支持两种探测方式：

简单探测方式：设备采用探测模板中配置的探测用户名、密码构造一个认证请求报文，并在
•探测周期内选择随机时间点向引用了探测模板的 服务器发送该报文。如果在本次探RADIUS测周期内收到服务器的认证响应报文，则认为当前探测周期内该服务器可达。
• EAP 探测方式：设备采用指定的 EAP 认证方案中配置的 EAP 认证方法启动服务器探测。在探测过程中，设备会在配置的探测周期超时后使用探测模板中配置的探测用户名和密码，模拟一个合法 认证用户向引用了该探测模板的 服务器发起一次 认证，如果EAP RADIUS EAP在探测超时时间内（不可配）成功完成该次认证，则认为当前探测周期内该服务器可用。
EAP 探测方式相较于简单探测方式，由于探测过程还原了完整的认证过程，更能保证 RADIUS 服务器探测结果的可靠性。建议在接入用户使用 EAP 认证方法的组网环境中，使用该方式的服务器探测功能。

###### 2. 配置限制和指导

系统支持同时存在多个 服务器探测模板。
RADIUS只有一个 服务器配置中成功引用了一个已经存在的服务器探测模板，设备才会启动对该RADIUS RADIUS 服务器的探测功能。
若探测模板中引用的 EAP 认证方案不存在，则设备会暂时采用简单探测方式发起探测。当引用的EAP 认证方案配置成功后，下一个探测周期将使用 EAP 方式发起探测。
服务器探测功能启动后，以下情况发生将会导致探测过程中止：
• 删除该 RADIUS 服务器配置；
• 取消对服务器探测模板的引用；
• 删除对应的服务器探测模板；
• 将该 RADIUS 服务器的状态手工置为 block；
删除当前 方案。
• RADIUS

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置 RADIUS 服务器探测模板。
radius-server test-profile profile-name username name [ password
{ cipher | simple } string ] [ interval interval ] [ eap-profile
eap-profile-name ]

##### 1.5.5 创建RADIUS方案

###### 1. 配置限制和指导

系统最多支持配置 16 个 RADIUS 方案。一个 RADIUS 方案可以同时被多个 ISP 域引用。

###### 2. 配置步骤

进入系统视图。
(1)
system-view创建 方案，并进入 方案视图。
(2) RADIUS RADIUS radius scheme radius-scheme-name

###### 1. 功能简介

###### 1. 功能简介

##### 1.5.6 配置RADIUS认证服务器

功能简介
1.
由于 RADIUS 服务器的授权信息是随认证应答报文发送给 RADIUS 客户端的，RADIUS 的认证和授权功能由同一台服务器实现，因此 认证服务器相当于 认证/授权服务器。通过RADIUS RADIUS在 RADIUS 方案中配置 RADIUS 认证服务器，指定设备对用户进行 RADIUS 认证时与哪些服务器进行通信。
一个 RADIUS 方案中最多允许配置一个主认证服务器和 16 个从认证服务器。缺省情况下，当主服务器不可达时，设备根据从服务器的配置顺序由先到后查找状态为 active 的从服务器并与之交互。
开启服务器负载分担功能后，设备会根据各服务器的权重以及服务器承载的用户负荷，按比例进行用户负荷分配并选择要交互的服务器。

###### 2. 配置限制和指导

建议在不需要备份的情况下，只配置主 RADIUS 认证服务器即可。
在实际组网环境中，可以指定一台服务器既作为某个 RADIUS 方案的主认证服务器，又作为另一个RADIUS 方案的从认证服务器。
在同一个方案中指定的主认证服务器和从认证服务器的 VPN、主机名、IP 地址、端口号不能完全相同，并且各从认证服务器的 VPN、主机名、IP 地址、端口号也不能完全相同。

###### 3. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入 RADIUS 方案视图。
radius scheme radius-scheme-name
(3) 配置主 RADIUS 认证服务器。
primary authentication { host-name | ipv4-address | ipv6 ipv6-address } [ port-number | key { cipher | simple } string | test-profile profile-name | vpn-instance vpn-instance-name | weight weight-value ] *缺省情况下，未配置主 RADIUS 认证服务器。
仅在 服务器负载分担功能处于开启状态下，参数 才能生效。
RADIUS weight（可选）配置从 认证服务器。
(4) RADIUS secondary authentication { host-name | ipv4-address | ipv6 ipv6-address } [ port-number | key { cipher | simple } string | test-profile profile-name | vpn-instance vpn-instance-name | weight weight-value ] *缺省情况下，未配置从 RADIUS 认证服务器。
仅在 RADIUS 服务器负载分担功能处于开启状态下，参数 weight 才能生效。

##### 1.5.7 配置RADIUS计费服务器

功能简介
1.
通过在 RADIUS 方案中配置 RADIUS 计费服务器，指定设备对用户进行 RADIUS 计费时与哪些服务器进行通信。

###### 3. 配置步骤

一个 RADIUS 方案中最多允许配置一个主计费服务器和 16 个从计费服务器。缺省情况下，当主服务器不可达时，设备根据从服务器的配置顺序由先到后查找状态为 的从服务器并与之交互。
active开启服务器负载分担功能后，设备会根据各服务器的权重以及服务器承载的用户负荷，按比例进行用户负荷分配并选择要交互的服务器。

###### 2. 配置限制和指导

建议在不需要备份的情况下，只配置主 计费服务器即可。
RADIUS在实际组网环境中，可以指定一台服务器既作为某个 RADIUS 方案的主计费服务器，又作为另一个RADIUS 方案的从计费服务器。
在同一个方案中指定的主计费服务器和从计费服务器的 VPN、主机名、IP 地址、端口号不能完全相同，并且各从计费服务器的 VPN、主机名、IP 地址、端口号也不能完全相同。
目前 RADIUS 不支持对 FTP/SFTP/SCP 用户进行计费。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 进入 RADIUS 方案视图。
radius scheme radius-scheme-name
(3) 配置主 RADIUS 计费服务器。
primary accounting { host-name | ipv4-address | ipv6 ipv6-address } [ port-number | key { cipher | simple } string | vpn-instance vpn-instance-name | weight weight-value ] *缺省情况下，未配置主 RADIUS 计费服务器。
仅在 RADIUS 服务器负载分担功能处于开启状态下，参数 weight 才能生效。
(4) （可选）配置从 RADIUS 计费服务器。
secondary accounting { host-name | ipv4-address | ipv6 ipv6-address } [ port-number | key { cipher | simple } string | vpn-instance vpn-instance-name | weight weight-value ] *缺省情况下，未配置从 RADIUS 计费服务器。
仅在 RADIUS 服务器负载分担功能处于开启状态下，参数 weight 才能生效。

##### 1.5.8 配置RADIUS报文的共享密钥

###### 1. 功能简介

RADIUS 客户端与 RADIUS 服务器使用 MD5 算法并在共享密钥的参与下生成验证字，接受方根据收到报文中的验证字来判断对方报文的合法性。只有在共享密钥一致的情况下，彼此才能接收对方发来的报文并作出响应。
由于设备优先采用配置 RADIUS 认证/计费服务器时指定的报文共享密钥，因此，本配置中指定的报文共享密钥仅在配置 认证 计费服务器时未指定相应密钥的情况下使用。
RADIUS RADIUS /

###### 2. 配置限制和指导

必须保证设备上设置的共享密钥与 RADIUS 服务器上的完全一致。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 RADIUS 方案视图。
radius scheme radius-scheme-name
(3) 配置 RADIUS 报文的共享密钥。
key { accounting | authentication } { cipher | simple } string
缺省情况下，未配置 RADIUS 报文的共享密钥。

##### 1.5.9 配置RADIUS方案所属的VPN

###### 1. 功能简介

该配置用于为 RADIUS 方案下的所有 RADIUS 服务器统一指定所属的 VPN。RADIUS 服务器所属的 VPN 也可以在配置 RADIUS 服务器的时候单独指定，且被优先使用。未单独指定所属 VPN 的服务器，则属于所在 RADIUS 方案所属的 VPN。

###### 2. 配置步骤

进入系统视图。
(1)
system-view进入 方案视图。
(2) RADIUS radius scheme radius-scheme-name
(3) 配置 RADIUS 方案所属的 VPN。
vpn-instance vpn-instance-name缺省情况下，RADIUS 方案属于公网。

##### 1.5.10 配置RADIUS服务器的状态

###### 1. RADIUS服务器状态切换简介

RADIUS 方案中各服务器的状态（active、block）决定了设备向哪个服务器发送请求报文，以及设备在与当前服务器通信中断的情况下，如何转而与另外一个服务器进行交互。在实际组网环境中，可指定一个主 RADIUS 服务器和多个从 RADIUS 服务器，由从服务器作为主服务器的备份。
当 RADIUS 服务器负载分担功能处于开启状态时，设备仅根据当前各服务器承载的用户负荷调度状态为 的服务器发送认证或计费请求。当 服务器负载分担功能处于关闭状态时，设active RADIUS备上主从服务器的切换遵从以下原则：
• 当主服务器状态为 active 时，设备首先尝试与主服务器通信，若主服务器不可达，则按照从服务器的配置先后顺序依次查找状态为 active 的从服务器。
• 只要存在状态为 active 的服务器，设备就仅与状态为 active 的服务器通信，即使该服务器不可达，设备也不会尝试与状态为 block 的服务器通信。
• 当主/从服务器的状态均为 block 时，设备才会尝试与主服务器进行通信，若未配置主服务器，则设备尝试与首个配置的从服务器通信。

如果服务器不可达，则设备将该服务器的状态置为 block，并启动该服务器的 quiet 定时器。
•当服务器的 定时器超时，或者手动将服务器状态置为 时，该服务器将恢复为quiet active active 状态。
• 在一次认证或计费过程中，如果设备在尝试与从服务器通信时，之前已经查找过的服务器状态由 block 恢复为 active，则设备并不会立即恢复与该服务器的通信，而是继续查找从服务器。如果所有已配置的服务器都不可达，则认为本次认证或计费失败。
如果在认证或计费过程中删除了当前正在使用的服务器，则设备在与该服务器通信超时后，
•将会立即从主服务器开始依次查找状态为 active 的服务器并与之进行通信。
一旦服务器状态满足自动切换的条件，则所有 方案视图下该服务器的状态都会相应
• RADIUS地变化。
• 将认证服务器的状态由 active 修改为 block 时，若该服务器引用了 RADIUS 服务器探测模板，则关闭对该服务器的探测功能；反之，将认证服务器的状态由 block 更改为 active 时，若该服务器引用了一个已存在的 服务器探测模板，则开启对该服务器的探测功能。
RADIUS缺省情况下，设备将配置了 IP 地址的各 RADIUS 服务器的状态均置为 active，认为所有的
•服务器均处于正常工作状态，但有些情况下用户可能需要通过以下配置手工改变 RADIUS 服务器的当前状态。例如，已知某服务器故障，为避免设备认为其 active 而进行无意义的尝试，可暂时将该服务器状态手工置为 block。

###### 2. 配置限制和指导

设置的服务器状态不能被保存在配置文件中，可通过 display radius scheme 命令查看。
设备重启后，各服务器状态将恢复为缺省状态 active。

###### 3. 配置步骤

进入系统视图。
(1)
system-view进入 方案视图。
(2) RADIUS radius scheme radius-scheme-name设置 认证服务器的状态。请至少选择其中一项进行配置。
(3) RADIUS设置主 RADIUS 认证服务器的状态。
(cid:123)
state primary authentication { active | block }设置主 RADIUS 计费服务器的状态。
(cid:123)
state primary accounting { active | block }设置从 RADIUS 认证服务器的状态。
(cid:123)
state secondary authentication [ { host-name | ipv4-address | ipv6 ipv6-address } [ port-number | vpn-instance vpn-instance-name ] * ] { active | block }设置从 RADIUS 计费服务器的状态。
(cid:123)
state secondary accounting [ { host-name | ipv4-address | ipv6 ipv6-address } [ port-number | vpn-instance vpn-instance-name ] * ] { active | block }缺省情况下，RADIUS 服务器的状态为 active。

###### 1. 定时器简介

##### 1.5.11 配置RADIUS服务器的定时器

定时器简介
1.
在与 RADIUS 服务器交互的过程中，设备上可启动的定时器包括以下几种：
• 服务器响应超时定时器（response-timeout）：如果在 RADIUS 请求报文发送出去一段时间后，设备还没有得到 RADIUS 服务器的响应，则有必要重传 RADIUS 请求报文，以保证用户尽可能地获得 RADIUS 服务，这段时间被称为 RADIUS 服务器响应超时时间。
服务器恢复激活状态定时器（quiet）：当服务器不可达时，设备将该服务器的状态置为 block，
•并开启超时定时器，在设定的一定时间间隔之后，再将该服务器的状态恢复为 active。这段时间被称为 RADIUS 服务器恢复激活状态时长。
• 实时计费间隔定时器（realtime-accounting）：为了对用户实施实时计费，有必要定期向服务器发送实时计费更新报文，通过设置实时计费的时间间隔，设备会每隔设定的时间向RADIUS 服务器发送一次在线用户的计费信息。

###### 2. 配置限制和指导

设置 RADIUS 服务器的定时器时，请遵循以下配置原则：
• 要根据配置的从服务器数量合理设置发送 RADIUS 报文的最大尝试次数和 RADIUS 服务器响应超时时间，避免因为超时重传时间过长，在主服务器不可达时，出现设备在尝试与从服务器通信的过程中接入模块（例如 模块）的客户端连接已超时的现象。但是，有些接入Telnet模块的客户端的连接超时时间较短，在配置的从服务器较多的情况下，即使将报文重传次数和 RADIUS 服务器响应超时时间设置的很小，也可能会出现上述客户端超时的现象，并导致初次认证或计费失败。这种情况下，由于设备会将不可达服务器的状态设置为 block，在下次认证或计费时设备就不会尝试与这些状态为 的服务器通信，一定程度上缩短了查找block可达服务器的时间，因此用户再次尝试认证或计费就可以成功。
• 要根据配置的从服务器数量合理设置服务器恢复激活状态的时间。如果服务器恢复激活状态时间设置得过短，就会出现设备反复尝试与状态 active 但实际不可达的服务器通信而导致的认证或计费频繁失败的问题；如果服务器恢复激活状态设置的过长，则会导致已经恢复激活状态的服务器暂时不能为用户提供认证或计费服务。
实时计费间隔的取值对设备和 服务器的性能有一定的相关性要求，取值小，会增加
• RADIUS网络中的数据流量，对设备和 RADIUS 服务器的性能要求就高；取值大，会影响计费的准确性。因此要结合网络的实际情况合理设置计费间隔的大小，一般情况下，建议当用户量比较大（大于等于 1000）时，尽量把该间隔的值设置得大一些（大于 分钟）。
15

###### 3. 配置步骤

(1) 进入系统视图。
system-view
进入 方案视图。
(2) RADIUS
radius scheme radius-scheme-name
设置 定时器参数。请至少选择其中一项进行配置。
(3) RADIUS
设置服务器响应超时时间。
(cid:123)
timer response-timeout seconds
缺省情况下，服务器响应超时定时器为 3 秒。

###### 1. 功能简介

设置服务器恢复激活状态的时间。
(cid:123)
timer quiet minutes缺省情况下，服务器恢复激活状态前需要等待 5 分钟。
设置实时计费间隔。
(cid:123)
timer realtime-accounting interval [ second ]缺省情况下，实时计费间隔为 12 分钟。

##### 1.5.12 配置发送RADIUS报文使用的源IP地址

功能简介
1.
RADIUS 服务器上通过 IP 地址来标识接入设备，并根据收到的 RADIUS 报文的源 IP 地址是否与服务器所管理的接入设备的 地址匹配，来决定是否处理来自该接入设备的认证或计费请求。若IP RADIUS 服务器收到的 RADIUS 认证或计费报文的源地址在所管理的接入设备 IP 地址范围内，则会进行后续的认证或计费处理，否则直接丢弃该报文。
设备发送 RADIUS 报文时，根据以下顺序查找使用的源 IP 地址：
(1) 当前所使用的 RADIUS 方案中配置的发送 RADIUS 报文使用的源 IP 地址。
(2) 根据当前使用的服务器所属的 VPN 查找系统视图下通过 radius nas-ip 命令配置的私网源地址，对于公网服务器则直接查找该命令配置的公网源地址。
(3) 通过路由查找到的发送 RADIUS 报文的出接口地址。

###### 2. 配置限制和指导

发送 RADIUS 报文使用的源 IP 地址在系统视图和 RADIUS 方案视图下均可配置，系统视图下的配置将对所有 方案生效，RADIUS 方案视图下的配置仅对本方案有效，并且具有高于前者的RADIUS优先级。
为保证认证和计费报文可被服务器正常接收并处理，接入设备上发送 RADIUS 报文使用的源 IP 地址必须与 RADIUS 服务器上指定的接入设备的 IP 地址保持一致。
通常，该地址为接入设备上与 RADIUS 服务器路由可达的接口 IP 地址，为避免物理接口故障时从服务器返回的报文不可达，推荐使用 Loopback 接口地址为发送 RADIUS 报文使用的源 IP 地址。
但在一些特殊的组网环境中，例如在接入设备使用 VRRP（Virtual Router Redundancy Protocol，虚拟路由器冗余协议）进行双机热备应用时，可以将该地址指定为 VRRP 上行链路所在备份组的虚拟 IP 地址。
源接口配置和源 IP 地址配置不能同时存在，后配置的生效。

###### 3. 为所有RADIUS方案配置发送RADIUS报文使用的源IP地址

进入系统视图。
(1)
system-view
(2) 设置设备发送 RADIUS 报文使用的源 IP 地址。
radius nas-ip { interface interface-type interface-number | { ipv4-address | ipv6 ipv6-address } [ vpn-instance vpn-instance-name ] }缺省情况下，未指定发送 报文使用的源 地址，设备将使用到达 服务器的RADIUS IP RADIUS路由出接口的主 IPv4 地址或 IPv6 地址作为发送 RADIUS 报文的源 IP 地址。

###### 4. 为指定RADIUS方案配置发送RADIUS报文使用的源IP地址

(1) 进入系统视图。
system-view
(2) 进入 RADIUS 方案视图。
radius scheme radius-scheme-name
(3) 设置设备发送 RADIUS 报文使用的源 IP 地址。
nas-ip { ipv4-address | interface interface-type interface-number | ipv6
ipv6-address }
缺省情况下，未指定设备发送 RADIUS 报文使用的源 IP 地址，使用系统视图下由命令 radius
nas-ip 指定的源 IP 地址。

##### 1.5.13 配置发送给RADIUS服务器的用户名格式和数据统计单位

###### 1. 功能简介

接入用户通常以“userid@isp-name”的格式命名，“@”后面的部分为 ISP 域名，设备通过该域名决定将用户归于哪个 域。由于有些较早期的 服务器不能接受携带有 域名的用户ISP RADIUS ISP名，因此就需要设备首先将用户名中携带的 ISP 域名去除后再传送给该类 RADIUS 服务器。通过设置发送给 RADIUS 服务器的用户名格式，就可以选择发送 RADIUS 服务器的用户名中是否要携带域名，以及是否保持用户输入的原始用户名格式。
ISP设备通过发送计费报文，向 服务器报告在线用户的数据流量统计值，该值的单位可配。
RADIUS

###### 2. 配置限制和指导

如果要在两个乃至两个以上的 域中引用相同的 方案，建议设置该 方案允许ISP RADIUS RADIUS用户名中携带 ISP 域名，使得 RADIUS 服务器端可以根据 ISP 域名来区分不同的用户。
为保证 RADIUS 服务器计费的准确性，设备上设置的发送给 RADIUS 服务器的数据流或者数据包的单位应与 RADUIS 服务器上的流量统计单位保持一致。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 RADIUS 方案视图。
radius scheme radius-scheme-name
(3) 设置发送给 RADIUS 服务器的用户名格式。
user-name-format { keep-original | with-domain | without-domain }
缺省情况下，发送给 RADIUS 服务器的用户名携带 ISP 域名。
如果采用设备作为 RADIUS 服务器，则发送给 RADIUS 服务器的用户名格式必须设置为
without-domain。
(4) 设置发送给 RADIUS 服务器的数据流或者数据包的单位。
data-flow-format { data { byte | giga-byte | kilo-byte | mega-byte } |
packet { giga-packet | kilo-packet | mega-packet | one-packet } } *
缺省情况下，数据流的单位为字节，数据包的单位为包。

###### 1. 功能简介

###### 2. 配置步骤

##### 1.5.14 配置发送RADIUS报文的最大尝试次数

功能简介
1.
由于RADIUS协议采用UDP报文来承载数据，因此其通信过程是不可靠的。如果设备在应答超时定时器规定的时长内（由timer response-timeout命令配置）没有收到RADIUS服务器的响应，则设备有必要向RADIUS服务器重传RADIUS请求报文。如果发送RADIUS请求报文的累计次数已达到指定的最大尝试次数而RADIUS服务器仍旧没有响应，则设备将尝试与其它服务器通信，如果不存在状态为active的服务器，则认为本次认证或计费失败。关于RADIUS服务器状态的相关内容，请参见“1.5.10 配置RADIUS服务器的状态”。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 RADIUS 方案视图。
radius scheme radius-scheme-name
设置发送 报文的最大尝试次数。
(3) RADIUS
retry retries
缺省情况下，发送 报文的最大尝试次数为 次。
RADIUS 3

##### 1.5.15 配置允许发起实时计费请求的最大尝试次数

###### 1. 功能简介

通过在设备上配置发起实时计费请求的最大尝试次数，允许设备向 服务器发出的实时计费RADIUS请求没有得到响应的次数超过指定的最大值时切断用户连接。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 RADIUS 方案视图。
radius scheme radius-scheme-name
(3) 设置允许发起实时计费请求的最大尝试次数。
retry realtime-accounting retries缺省情况下，允许发起实时计费请求的最大尝试次数为 5。

##### 1.5.16 配置RADIUS报文的DSCP优先级

###### 1. 功能简介

DSCP 携带在 IP 报文中的 ToS 字段，用来体现报文自身的优先等级，决定报文传输的优先程度。
通过本命令可以指定设备发送的 RADIUS 报文携带的 DSCP 优先级的取值。配置 DSCP 优先级的取值越大，RADIUS 报文的优先级越高。

###### 2. 配置步骤

(1) 进入系统视图。

system-view
(2) 配置 RADIUS 报文的 DSCP 优先级。
radius [ ipv6 ] dscp dscp-value缺省情况下，RADIUS 报文的 DSCP 优先级为 0。

##### 1.5.17 配置RADIUS Attribute 15的检查方式

###### 1. 功能简介

RADIUS 15 号属性为Login-Service属性，该属性携带在Access-Accept报文中，由RADIUS服务器下发给设备，表示认证用户的业务类型，例如属性值 表示Telnet业务。设备检查用户登录时采用0的业务类型与服务器下发的Login-Service属性所指定的业务类型是否一致，如果不一致则用户认证失败 。由于RFC中并未定义SSH、FTP和Terminal这三种业务的Login-Service属性值，因此设备无法针对SSH、FTP、Terminal用户进行业务类型一致性检查，为了支持对这三种业务类型的检查，H3C为Login-Service属性定义了 表 1-4 所示的扩展取值。
表1-4 扩展的 Login-Service 属性值属性值 描述50 用户的业务类型为SSH 51 用户的业务类型为FTP 52 用户的业务类型为Terminal可以通过配置设备对 号属性的检查方式，控制设备是否使用扩展的 属性RADIUS 15 Login-Service值对用户进行业务类型一致性检查。
• 严格检查方式：设备使用标准属性值和扩展属性值对用户业务类型进行检查，对于 SSH、FTP、Terminal 用户，当 RADIUS 服务器下发的 Login-Service 属性值为对应的扩展取值时才能够通过认证。
松散检查方式：设备使用标准属性值对用户业务类型进行检查，对于 SSH、FTP、Terminal
•用户，在 RADIUS 服务器下发的 Login-Service 属性值为 0（表示用户业务类型为 Telnet）时才能够通过认证。

###### 2. 配置限制和指导

由于某些 RADIUS 服务器不支持自定义的属性，无法下发扩展的 Login-Service 属性，若要使用这类 服务器对 SSH、FTP、Terminal 用户进行认证，建议设备上对 号属性值采RADIUS RADIUS 15用松散检查方式。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 RADIUS 方案视图。
radius scheme radius-scheme-name
(3) 配置对 RADIUS Attribute 15 的检查方式。
attribute 15 check-mode { loose | strict }

##### 1.5.19 配置RADIUS Attribute 31中的MAC地址格式

缺省情况下，对 RADIUS Attribute 15 的检查方式为 strict 方式。

##### 1.5.18 配置RADIUS Attribute 25的CAR参数解析功能

###### 1. 功能简介

的 号属性为 属性，该属性由 服务器下发给设备，但 中并未定义具RADIUS 25 class RADIUS RFC体的用途，仅规定了设备需要将服务器下发的 class 属性再原封不动地携带在计费请求报文中发送给服务器即可，同时 RFC 并未要求设备必须对该属性进行解析。目前，某些 RADIUS 服务器利用class 属性来对用户下发 CAR 参数，为了支持这种应用，可以通过本特性来控制设备是否将 RADIUS号属性解析为 参数，解析出的 参数可被用来进行基于用户的流量监管控制。
25 CAR CAR

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 RADIUS 方案视图。
radius scheme radius-scheme-name
开启 的 参数解析功能。
(3) RADIUS Attribute 25 CAR
attribute 25 car
缺省情况下，RADIUS 的 参数解析功能处于关闭状态。
Attribute 25 CAR
配置RADIUS 中的MAC地址格式
1.5.19 Attribute 31

###### 1. 配置限制和指导

不同的 服务器对填充在 中的 地址有不同的格式要求，为了保RADIUS RADIUS Attribute 31 MAC证 RADIUS 报文的正常交互，设备发送给服务器的 RADIUS Attribute 31 号属性中 MAC 地址的格式必须与服务器的要求保持一致。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 RADIUS 方案视图。
radius scheme radius-scheme-name
(3) 配置 RADIUS Attribute 31 中的 MAC 地址格式。
attribute 31 mac-format section { six | three } separator
separator-character { lowercase | uppercase }
缺省情况下，RADIUS Attribute 31 中的 MAC 地址为大写字母格式，且被分隔符“-”分成 6
段，即为 HH-HH-HH-HH-HH-HH 的格式。

##### 1.5.20 配置RADIUS Remanent_Volume属性的流量单位

###### 1. 功能简介

Remanent_Volume 属性为 H3C 自定义 RADIUS 属性，携带在 RADIUS 服务器发送给接入设备的认证响应或实时计费响应报文中，用于向接入设备通知在线用户的剩余流量值。

##### 1.5.21 配置RADIUS属性解释功能

###### 2. 配置限制和指导

设备管理员设置的 Remanent_Volume 属性流量单位应与 RADIUS 服务器上统计用户流量的单位保持一致，否则设备无法正确使用 Remanent_Volume 属性值对用户进行计费。

###### 3. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入 RADIUS 方案视图。
radius scheme radius-scheme-name
(3) 配置 RADIUS Remanent_Volume 属性的流量单位。
attribute remanent-volume unit { byte | giga-byte | kilo-byte | mega-byte }缺省情况下，Remanent_Volume 属性的流量单位是千字节。
配置 属性解释功能
1.5.21 RADIUS

###### 1. 功能简介

不同厂商的 服务器所支持的 属性集有所不同，而且相同属性的用途也可能不同。
RADIUS RADIUS为了兼容不同厂商的服务器的 RADIUS 属性，需要开启 RADIUS 属性解释功能，并定义相应的RADIUS 属性转换规则和 RADIUS 属性禁用规则。
开启 RADIUS 解释功能后，设备在发送和接收 RADIUS 报文时，可以按照配置的属性转换规则以及属性禁用规则对 RADIUS 报文中的属性进行不同的处理：
设备发送 RADIUS 报文时，将报文中匹配上禁用规则的属性从报文中删除，将匹配上转换规
•则的属性替换为指定的属性；
设备接收 报文时，不处理报文中匹配上禁用规则的属性，将匹配上转换规则的属性
• RADIUS解析为指定的属性。
如果设备需要按照某种既定规则去处理一些无法识别的其他厂商的私有 RADIUS 属性，可以定义RADIUS 扩展属性。通过自定义 RADIUS 扩展属性，并结合 RADIUS 属性转换功能，可以将系统不可识别的属性映射为已知属性来处理。

###### 2. 配置限制和指导

在一个 方案视图下，对于同一个 属性，存在以下配置限制：
RADIUS RADIUS如果已经配置了禁用规则，则不允许再配置转换规则；反之亦然。
•基于方向（received、sent）的规则和基于报文类型（access-accept、
•access-request、accounting）的规则，不能同时配置，只能存在一种。
• 对于基于方向的规则，可以同时存在两条不同方向的规则；对于基于报文类型的规则，可以存在同时存在三条不同类型的规则。

###### 3. 配置RADIUS属性解释功能（基于RADIUS方案）

(1) 进入系统视图。
system-view
(2) （可选）定义 RADIUS 扩展属性。

radius attribute extended attribute-name [ vendor vendor-id ] code attribute-code type { binary | date | integer | interface-id | ip | ipv6 | ipv6-prefix | octets | string }
(3) 进入 RADIUS 方案视图。
radius scheme radius-scheme-name
(4) 开启 RADIUS 属性解释功能。
attribute translate缺省情况下，RADIUS 属性解释功能处于关闭状态。
配置 属性转换/禁用规则。请至少选择其中一项进行配置。
(5) RADIUS配置 属性转换规则。
RADIUS (cid:123)
attribute convert src-attr-name to dest-attr-name { { access-accept | access-request | accounting } * | { received | sent } * }缺省情况下，未配置任何 RADIUS 属性转换规则。
配置 RADIUS 属性禁用规则。
(cid:123)
attribute reject attr-name { { access-accept | access-request | accounting } * | { received | sent } * }缺省情况下，未配置任何 RADIUS 属性禁用规则。

###### 4. 配置RADIUS属性解释功能（基于RADIUS DAE服务器）

(1) 进入系统视图。
system-view
(2) （可选）定义 RADIUS 扩展属性。
radius attribute extended attribute-name [ vendor vendor-id ] code
attribute-code type { binary | date | integer | interface-id | ip | ipv6 |
ipv6-prefix | octets | string }
进入 服务器视图。
(3) RADIUS DAE
radius dynamic-author server
(4) 开启 RADIUS 属性解释功能。
attribute translate
缺省情况下，RADIUS 属性解释功能处于关闭状态。
(5) 配置 RADIUS 属性转换/禁用规则。请至少选择其中一项进行配置。
配置 RADIUS 属性转换。
(cid:123)
attribute convert src-attr-name to dest-attr-name { { coa-ack |
coa-request } * | { received | sent } * }
缺省情况下，未配置任何 RADIUS 属性转换。
配置 RADIUS 属性禁用。
(cid:123)
attribute reject attr-name { { coa-ack | coa-request } * | { received |
sent } * }
缺省情况下，未配置任何 属性禁用。
RADIUS

###### 1. 功能简介

###### 1. 功能简介

###### 2. 配置步骤

##### 1.5.22 配置RADIUS计费报文缓存功能

功能简介
1.
当用户请求断开连接或者设备强行切断用户连接的情况下，设备会向 RADIUS 计费服务器发起停止计费请求。为了使得设备尽量与 服务器同步切断用户连接，可以开启对无响应的RADIUS RADIUS停止计费报文缓存功能，将停止计费报文缓存在本机上，然后多次尝试向服务器发起停止计费请求。
如果在发起停止计费请求的尝试次数达到指定的最大值后设备仍然没有收到响应，则将其从缓存中删除。

###### 2. 配置步骤

进入系统视图。
(1)
system-view进入 方案视图。
(2) RADIUS radius scheme radius-scheme-name
(3) 开启对无响应的 RADIUS 停止计费请求报文的缓存功能。
stop-accounting-buffer enable缺省情况下，设备缓存未得到响应的 RADIUS 停止计费请求报文。
(4) （可选）设置发起 RADIUS 停止计费请求的最大尝试次数。
retry stop-accounting retries缺省情况下，发起 RADIUS 停止计费请求的最大尝试次数为 500。

##### 1.5.23 配置用户下线时设备强制发送RADIUS计费停止报文

功能简介
1.
通常，RADIUS 服务器在收到用户的计费开始报文后才会生成用户表项，但有一些 RADIUS 服务器在用户认证成功后会立即生成用户表项。如果设备使用该类 服务器进行认证/授权/计费，RADIUS则在用户认证后，因为一些原因（比如授权失败）并未发送计费开始报文，则在该用户下线时设备也不会发送 RADIUS 计费停止报文，就会导致 RADIUS 服务器上该用户表项不能被及时释放，形成服务器和设备上用户信息不一致的问题。为了解决这个问题，建议开启本功能。
开启本功能后，只要用户使用 RADIUS 服务器进行计费，且设备未向 RADIUS 服务器发送计费开始报文，则在用户下线时设备会强制发送一个 计费停止报文给服务器，使得服务器收到此RADIUS报文后及时释放用户表项。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 RADIUS 方案视图。
radius scheme radius-scheme-name
(3) 配置用户下线时设备强制发送 RADIUS 计费停止报文。
stop-accounting-packet send-force缺省情况下，用户下线时设备不会强制发送计费停止报文。

###### 2. 配置步骤

###### 1. 功能简介

###### 3. 配置步骤

##### 1.5.24 配置RADIUS服务器负载分担功能

功能简介
1.
缺省情况下，RADIUS 服务器的调度采用主/从模式，即设备优先与主服务器交互，当主服务器不可达时，设备根据从服务器的配置顺序由先到后查找状态为 的从服务器并与之交互。
active RADIUS 方案中开启了服务器负载分担功能后，设备会根据各服务器的权重以及服务器承载的用户负荷，按比例进行用户负荷分配并选择要交互的服务器。
负载分担模式下，某台计费服务器开始对某用户计费后，该用户后续计费请求报文均会发往同一计费服务器。如果该计费服务器不可达，则直接返回计费失败。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 RADIUS 方案视图。
radius scheme radius-scheme-name
(3) 开启 RADIUS 服务器负载分担功能。
server-load-sharing enable缺省情况下，RADIUS 服务器负载分担功能处于关闭状态。

##### 1.5.25 配置RADIUS的accounting-on功能

###### 1. 功能简介

开启 accounting-on 功能后，整个设备会在重启后主动向 RADIUS 服务器发送 accounting-on 报文来告知自己已经重启，并要求 RADIUS 服务器停止计费且强制通过本设备上线的用户下线。该功能可用于解决设备重启后，重启前的原在线用户因被 服务器认为仍然在线而短时间内无法再RADIUS次登录的问题。若设备发送 accounting-on 报文后 RADIUS 服务器无响应，则会在按照一定的时间间隔（interval interval）尝试重发几次（send send-times）。
accounting-on 扩展功能是为了适应分布式架构而对 accounting-on 功能的增强。
accounting-on 扩展功能适用于 lan-access 用户，该类型的用户数据均保存在用户接入的成员设备上。开启 accounting-on 扩展功能后，当有用户发起接入认证的成员设备重启时，设备会向 RADIUS服务器发送携带设成员设备标识的 报文，用于通知 服务器对该成员设备的accounting-on RADIUS用户停止计费且强制用户下线。如果自上一次重启之后，成员设备上没有用户接入认证的记录，则该成员设备再次重启，并不会触发设备向 RADIUS 服务器发送携带成员设备标识的 accounting-on报文。

###### 2. 配置限制和指导

只有在 功能处于开启状态，且和 服务器配合使用的情况下，accounting-on accounting-on H3C iMC扩展功能才能生效。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 进入 RADIUS 方案视图。

###### 1. 功能简介

radius scheme radius-scheme-name
(3) 开启 accounting-on 功能。
accounting-on enable [ interval interval | send send-times ] *缺省情况下，accounting-on 功能处于关闭状态。
(4) （可选）开启 accounting-on 扩展功能。
accounting-on extended缺省情况下，accounting-on 扩展功能处于关闭状态。

##### 1.5.26 配置RADIUS的session control功能

功能简介
1.
H3C 的 iMC RADIUS 服务器使用 session control 报文向设备发送授权信息的动态修改请求以及断开连接请求。开启 功能后，设备会打开知名 端口 来监听并接RADIUS session control UDP 1812收 RADIUS 服务器发送的 session control 报文。
当设备收到 session control 报文时，通过 session control 客户端配置验证 RADIUS session control报文的合法性。

###### 2. 配置限制和指导

需要注意的是，该功能仅能和 H3C 的 iMC RADIUS 服务器配合使用。缺省情况下，为节省系统资源，设备上的 功能处于关闭状态。因此，在使用 服务器且RADIUS session control iMC RADIUS服务器需要对用户授权信息进行动态修改或强制用户下线的情况下，必须开启此功能。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 开启 RADIUS session control 功能。
radius session-control enable
缺省情况下，RADIUS session control 功能处于关闭状态。
(3) 指定 session control 客户端。
radius session-control client { ip ipv4-address | ipv6 ipv6-address }
[ key { cipher | simple } string | vpn-instance vpn-instance-name ] *
缺省情况下，未指定 session control 客户端。

##### 1.5.27 配置RADIUS DAE服务器功能

###### 1. 功能简介

DAE（Dynamic Authorization Extensions，动态授权扩展）协议是 RFC 5176 中定义的 RADIUS协议的一个扩展，它用于强制认证用户下线，或者更改在线用户授权信息。DAE 采用客户端/服务器通信模式，由 客户端和 服务器组成。
DAE DAE客户端：用于发起 请求，通常驻留在一个 服务器上，也可以为一个单独
• DAE DAE RADIUS的实体。

###### 2. 配置步骤

DAE 服务器：用于接收并响应 DAE 客户端的 DAE 请求，通常为一个 NAS（Network Access
•Server，网络接入服务器）设备。
报文包括以下两种类型：
DAE DMs（Disconnect Messages）：用于强制用户下线。DAE 客户端通过向 设备发送
• NAS DM请求报文，请求 NAS 设备按照指定的匹配条件强制用户下线。
• COA（Change of Authorization）Messages：用于更改用户授权信息。DAE 客户端通过向NAS 设备发送 COA 请求报文，请求 NAS 设备按照指定的匹配条件更改用户授权信息。
在设备上开启 RADIUS DAE 服务后，设备将作为 RADIUS DAE 服务器在指定的 UDP 端口监听指定的 RADIUS DAE 客户端发送的 DAE 请求消息，然后根据请求消息进行用户授权信息的修改、断开用户连接、关闭/重启用户接入端口或重认证用户，并向 DAE客户端发送 DAE应答消息。
RADIUS

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 开启 RADIUS DAE 服务，并进入 RADIUS DAE 服务器视图。
radius dynamic-author server
缺省情况下， 服务处于关闭状态。
RADIUS DAE
指定 客户端。
(3) RADIUS DAE
client { ip ipv4-address | ipv6 ipv6-address } [ key { cipher | simple }
string | vpn-instance vpn-instance-name ] *
缺省情况下，未指定 RADIUS DAE 客户端。
(4) （可选）指定 RADIUS DAE 服务端口。
port port-number
缺省情况下，RADIUS 服务端口为 3799。
DAE

##### 1.5.28 配置RADIUS告警功能

###### 1. 功能简介

开启相应的 RADIUS 告警功能后，RADIUS 模块会生成告警信息，用于报告该模块的重要事件：
当 向 服务器发送计费或认证请求没有收到响应时，会重传请求，当重传次数达
• NAS RADIUS到最大传送次数时仍然没有收到响应时，NAS 认为该服务器不可达，并发送表示 RADIUS 服务器不可达的告警信息。
• 当 timer quiet 定时器设定的时间到达后，NAS 将服务器的状态置为激活状态并发送表示服务器可达的告警信息。
RADIUS当 NAS 发现认证失败次数与认证请求总数的百分比超过阈值时，会发送表示认证失败次数超
•过阈值的告警信息。
生成的告警信息将发送到设备的 模块，通过设置 中告警信息的发送参数，来决定告SNMP SNMP警信息输出的相关属性。有关告警信息的详细介绍，请参见“网络管理和监控配置指导”中的“ SNMP ”。
配置步骤
2.
(1) 进入系统视图。
system-view

(2) 开启 RADIUS 告警功能。
snmp-agent trap enable radius [ accounting-server-down |
accounting-server-up | authentication-error-threshold |
authentication-server-down | authentication-server-up ] *
缺省情况下，所有类型的 RADIUS 告警功能均处于关闭状态。

##### 1.5.29 RADIUS显示和维护

完成上述配置后，在任意视图下执行 display 命令可以显示配置后 RADIUS 的运行情况，通过查看显示信息验证配置的效果。
在用户视图下，执行 命令可以清除相关统计信息。
reset表1-5 RADIUS 显示和维护操作 命令显示所有或指定RADIUS方案的配置信息 display radius scheme [ radius-scheme-name ]显示RADIUS服务器的负载统计信息 display radius server-load statistics显示RADIUS报文的统计信息 display radius statistics display stop-accounting-buffer { radius-scheme显示缓存的RADIUS停止计费请求报文的相radius-scheme-name | session-id session-id |关信息 time-range start-time end-time | user-name user-name }清除所有RADIUS服务器的历史负载统计信reset radius server-load statistics息reset radius statistics清除RADIUS协议的统计信息reset stop-accounting-buffer { radius-scheme radius-scheme-name | session-id session-id |清除缓存的RADIUS停止计费请求报文time-range start-time end-time | user-name user-name }

#### 1.6 配置HWTACACS

##### 1.6.1 HWTACACS配置任务简介

配置任务如下：
HWTACACS创建HWTACACS方案
(1)
配置HWTACACS认证服务器
(2)
配置HWTACACS授权服务器
(3)
配置HWTACACS计费服务器
(4)
(5) 配置 HWTAC ACS 报文的共享密钥若配置 HWTACACS 服务器时未指定共享密钥，则可以通过本任务统一指定对所有认证/计费服务器生效的共享密钥。
HWTACACS配置HWTACACS方案所属的VPN
(6)

###### 3. 配置步骤

若配置 HWTACACS 服务器时未指定所属的 VPN，则可以通过本任务统一指定所有服务器所属的 VPN。
HWTACACS（可选）配置HWTACACS服务器的定时器
(7)
（可选）配置 报文交互参数
(8) HWTACACS配置发送HWTACACS报文使用的源IP地址(cid:123)
配置发送给HWTACACS服务器的用户名格式和数据统计单位(cid:123)
(9) （可选）配置HWTACACS计费报文缓存功能

##### 1.6.2 创建HWTACACS方案

###### 1. 配置限制和指导

系统最多支持配置 个 方案。一个 方案可以同时被多个 域引用。
16 HWTACACS HWTACACS ISP

###### 2. 配置步骤

(1) 进入系统视图。
system-view
创建 方案，并进入 方案视图。
(2) HWTACACS HWTACACS
hwtacacs scheme hwtacacs-scheme-name

##### 1.6.3 配置HWTACACS认证服务器

###### 1. 功能简介

通过在 HWTACACS 方案中配置 HWTACACS 认证服务器，指定设备对用户进行 HWTACACS 认证时与哪个服务器进行通信。
一个 HWTACACS 方案中最多允许配置一个主认证服务器和 16 个从认证服务器。当主服务器不可达时，设备根据从服务器的配置顺序由先到后查找状态为 active 的从服务器并与之交互。

###### 2. 配置限制和指导

建议在不需要备份的情况下，只配置主 HWTACACS 认证服务器即可。
在实际组网环境中，可以指定一台服务器既作为某个 HWTACACS 方案的主认证服务器，又作为另一个 方案的从认证服务器。
HWTACACS在同一个方案中指定的主认证服务器和从认证服务器的 VPN、主机名、IP 地址、端口号不能完全相同，并且各从认证服务器的 VPN、主机名、IP 地址、端口号也不能完全相同。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 进入 HWTACACS 方案视图。
hwtacacs scheme hwtacacs-scheme-name
(3) 配置主 HWTACACS 认证服务器。
primary authentication { host-name | ipv4-address | ipv6 ipv6-address } [ port-number | key { cipher | simple } string | single-connection | vpn-instance vpn-instance-name ] *

缺省情况下，未配置主 HWTACACS 认证服务器。
(4) （可选）配置从 HWTACACS 认证服务器。
secondary authentication { host-name | ipv4-address | ipv6 ipv6-address } [ port-number | key { cipher | simple } string | single-connection | vpn-instance vpn-instance-name ] *缺省情况下，未配置从 HWTACACS 认证服务器。

##### 1.6.4 配置HWTACACS授权服务器

###### 1. 功能简介

通过在 HWTACACS 方案中配置 HWTACACS 授权服务器，指定设备对用户进行 HWTACACS 授权时与哪个服务器进行通信。
一个 HWTACACS 方案中最多允许配置一个主授权服务器和 16 个从授权服务器。当主服务器不可达时，设备根据从服务器的配置顺序由先到后查找状态为 active 的从服务器并与之交互。

###### 2. 配置限制和指导

建议在不需要备份的情况下，只配置主 授权服务器即可。
HWTACACS在实际组网环境中，可以指定一台服务器既作为某个 方案的主授权服务器，又作为另HWTACACS一个 HWTACACS 方案的从授权服务器。
在同一个方案中指定的主授权服务器和从授权服务器的 VPN、主机名、IP 地址、端口号不能完全相同，并且各从授权服务器的 VPN、主机名、IP 地址、端口号也不能完全相同。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 HWTACACS 方案视图。
hwtacacs scheme hwtacacs-scheme-name
(3) 配置主 HWTACACS 授权服务器。
primary authorization { host-name | ipv4-address | ipv6 ipv6-address }
[ port-number | key { cipher | simple } string | single-connection |
vpn-instance vpn-instance-name ] *
缺省情况下，未配置主 授权服务器。
HWTACACS
（可选）配置从 授权服务器。
(4) HWTACACS
secondary authorization { host-name | ipv4-address | ipv6 ipv6-address }
[ port-number | key { cipher | simple } string | single-connection |
vpn-instance vpn-instance-name ] *
缺省情况下，未配置从 HWTACACS 授权服务器。

###### 1. 功能简介

##### 1.6.5 配置HWTACACS计费服务器

功能简介
1.
通过在 HWTACACS 方案中配置 HWTACACS 计费服务器，指定设备对用户进行 HWTACACS 计费时与哪个服务器进行通信。
一个 HWTACACS 方案中最多允许配置一个主计费服务器和 16 个从计费服务器。当主服务器不可达时，设备根据从服务器的配置顺序由先到后查找状态为 active 的从服务器并与之交互。

###### 2. 配置限制和指导

建议在不需要备份的情况下，只配置主 HWTACACS 计费服务器即可。
在实际组网环境中，可以指定一台服务器既作为某个 HWTACACS 方案的主计费服务器，又作为另一个 HWTACACS 方案的从计费服务器。
在同一个方案中指定的主计费服务器和从计费服务器的 VPN、主机名、IP 地址、端口号不能完全相同，并且各从计费服务器的 VPN、主机名、IP 地址、端口号也不能完全相同。
目前 HWTACACS 不支持对 FTP/SFTP/SCP 用户进行计费。

###### 3. 配置步骤

进入系统视图。
(1)
system-view进入 方案视图。
(2) HWTACACS hwtacacs scheme hwtacacs-scheme-name
(3) 配置主 HWTACACS 计费服务器。
primary accounting { host-name | ipv4-address | ipv6 ipv6-address } [ port-number | key { cipher | simple } string | single-connection | vpn-instance vpn-instance-name ] *缺省情况下，未配置主 HWTACACS 计费服务器。
(4) （可选）配置从 HWTACACS 计费服务器。
secondary accounting { host-name | ipv4-address | ipv6 ipv6-address } [ port-number | key { cipher | simple } string | single-connection | vpn-instance vpn-instance-name ] *缺省情况下，未配置从 HWTACACS 计费服务器。

##### 1.6.6 配置HWTACACS报文的共享密钥

###### 1. 功能简介

HWTACACS客户端与 HWTACACS服务器使用 MD5算法并在共享密钥的参与下加密 HWTACACS报文。只有在密钥一致的情况下，彼此才能接收对方发来的报文并作出响应。
由于设备优先采用配置 认证/授权/计费服务器时指定的报文共享密钥，因此，本配置HWTACACS中指定的 HWTACACS 报文共享密钥仅在配置 HWTACACS 认证 / 授权 / 计费服务器时未指定相应密钥的情况下使用。

###### 2. 配置限制和指导

必须保证设备上设置的共享密钥与 HWTACACS 服务器上的完全一致。

###### 1. 功能简介

###### 2. 配置步骤

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 HWTACACS 方案视图。
hwtacacs scheme hwtacacs-scheme-name
(3) 配置 HWTACACS 认证、授权、计费报文的共享密钥。
key { accounting | authentication | authorization } { cipher | simple }
string
缺省情况下，未设置 HWTACACS 报文的共享密钥。

##### 1.6.7 配置HWTACACS方案所属的VPN

功能简介
1.
该配置用于指定 HWTACACS 方案所属的 VPN，即为 HWTACACS 方案下的所有 HWTACACS 服务器统一指定所属的 VPN。HWTACACS 服务器所属的 VPN 也可以在配置 HWTACACS 服务器的时候单独指定，且被优先使用。未单独指定所属 的服务器，则属于所在 方案所VPN HWTACACS属的 VPN。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 HWTACACS 方案视图。
hwtacacs scheme hwtacacs-scheme-name
(3) 配置 HWTACACS 方案所属的 VPN。
vpn-instance vpn-instance-name缺省情况下，HWTACACS 方案属于公网。

##### 1.6.8 配置HWTACACS服务器的定时器

###### 1. 定时器及服务器状态切换简介

在与 HWTACACS 服务器交互的过程中，设备上可启动的定时器包括以下几种：
• 服务器响应超时定时器（response-timeout）：如果在 HWTACACS 请求报文传送出去一段时间后，设备还没有得到 HWTACACS 服务器的响应，则会将该服务器的状态置为 block，并向下一个 服务器发起请求，以保证用户尽可能得到 服务，这段HWTACACS HWTACACS时间被称为 HWTACACS 服务器响应超时时长。
• 实时计费间隔定时器（realtime-accounting）：为了对用户实施实时计费，有必要定期向服务器发送用户的实时计费信息，通过设置实时计费的时间间隔，设备会每隔设定的时间向HWTACACS 服务器发送一次在线用户的计费信息。
• 服务器恢复激活状态定时器（quiet）：当服务器不可达时，设备将该服务器的状态置为 block，并开启超时定时器，在设定的一定时间间隔之后，再将该服务器的状态恢复为 active 。这段时间被称为服务器恢复激活状态时长。

###### 3. 配置步骤

HWTACACS 方案中各服务器的状态（active、block）决定了设备向哪个服务器发送请求报文，以及设备在与当前服务器通信中断的情况下，如何转而与另外一个服务器进行交互。在实际组网环境中，可指定一个主 HWTACACS 服务器和多个从 HWTACACS 服务器，由从服务器作为主服务器的备份。通常情况下，设备上主从服务器的切换遵从以下原则：
• 当主服务器状态为 active 时，设备首先尝试与主服务器通信，若主服务器不可达，则按照从服务器的配置先后顺序依次查找状态为 active 的从服务器进行认证或者计费。
只要存在状态为 active 的服务器，设备就仅与状态为 active 的服务器通信，即使该服务
•器不可达，设备也不会尝试与状态为 block 的服务器通信。
当主/从服务器的状态均为 时，设备尝试与主服务器进行通信，若未配置主服务器，则
• block设备尝试与首个配置的从服务器通信。
• 如果服务器不可达，则设备将该服务器的状态置为 block，同时启动该服务器的 quiet 定时器。当服务器的 quiet 定时器超时，该服务器将恢复为 active 状态。
• 在一次认证或计费过程中，如果设备在尝试与从服务器通信时，之前已经查找过的服务器状态由 block 恢复为 active，则设备并不会立即恢复与该服务器的通信，而是继续查找从服务器。如果所有已配置的服务器都不可达，则认为本次认证或计费失败。
如果在认证或计费过程中删除了当前正在使用的服务器，则设备在与该服务器通信超时后，
•将会立即从主服务器开始依次查找状态为 active 的服务器并与之进行通信。
• 一旦服务器状态满足自动切换的条件，则所有 HWTACACS 方案视图下该服务器的状态都会相应地变化。

###### 2. 配置限制和指导

实时计费间隔的取值对设备和 HWTACACS 服务器的性能有一定的相关性要求，取值越小，对设备和 服务器的性能要求越高。建议当用户量比较大（大于等于 1000）时，尽量把该间HWTACACS隔的值设置得大一些（大于 15 分钟）。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 进入 HWTACACS 方案视图。
hwtacacs scheme hwtacacs-scheme-name
(3) 设置 HWTACACS 定时器参数。请至少选择其中一项进行配置。
设置 HWTACACS 服务器响应超时时间。
(cid:123)
timer response-timeout seconds缺省情况下，服务器响应超时时间为 5 秒。
设置实时计费的时间间隔。
(cid:123)
timer realtime-accounting minutes缺省情况下，实时计费间隔为 12 分钟。
设置服务器恢复激活状态的时间。
(cid:123)
timer quiet minutes缺省情况下，服务器恢复激活状态前需要等待 分钟。
5

###### 1. 功能简介

##### 1.6.9 配置发送HWTACACS报文使用的源IP地址

功能简介
1.
HWTACACS 服务器上通过 IP 地址来标识接入设备，并根据收到的 HWTACACS 报文的源 IP 地址是否与服务器所管理的接入设备的 地址匹配，来决定是否处理来自该接入设备的认证、授权或计IP费请求。若 HWTACACS 服务器收到的 HWTACACS 认证或计费报文的源地址在所管理的接入设备IP 地址范围内，则会进行后续的认证或计费处理，否则直接丢弃该报文。
设备发送 HWTACACS 报文时，根据以下顺序查找使用的源 IP 地址：
(1) 当前所使用的 HWTACACS 方案中配置的发送 HWTACACS 报文使用的源 IP 地址。
(2) 根据当前使用的服务器所属的 VPN 查找系统视图下通过 hwtacacs nas-ip 命令配置的私网源地址，对于公网服务器则直接查找该命令配置的公网源地址。
(3) 通过路由查找到的发送 HWTACACS 报文的出接口地址。

###### 2. 配置限制和指导

发送给 HWTACACS 报文使用的源 IP 地址在系统视图和 HWTACACS 方案视图下均可以进行配置，系统视图下的配置将对所有 方案生效，HWTACACS 方案视图下的配置仅对本方案有HWTACACS效，并且具有高于前者的优先级。
为保证认证、授权和计费报文可被服务器正常接收并处理，接入设备上发送 HWTACACS 报文使用的源 IP 地址必须与 HWTACACS 服务器上指定的接入设备的 IP 地址保持一致。
通常，该地址为接入设备上与 HWTACACS 服务器路由可达的接口 IP 地址，为避免物理接口故障时从服务器返回的报文不可达，推荐使用 Loopback 接口地址为发送 HWTACACS 报文使用的源 IP地址。但在一些特殊的组网环境中，例如在接入设备使用 进行双机热备应用时，可以将该地VRRP址指定为 VRRP 上行链路所在备份组的虚拟 IP 地址。
源接口配置和源 IP 地址配置不能同时存在，后配置的生效。

###### 3. 为所有HWTACACS方案配置发送HWTACACS报文使用的源IP地址

(1) 进入系统视图。
system-view
(2) 设置设备发送 HWTACACS 报文使用的源 IP 地址。
hwtacacs nas-ip { interface interface-type interface-number |
{ ipv4-address | ipv6 ipv6-address } [ vpn-instance vpn-instance-name ] }
缺省情况下，未指定发送 HWTACACS 报文使用的源 IP 地址，设备将使用到达 HWTACACS
服务器的路由出接口的主 地址或 地址作为发送 报文的源 地址。
IPv4 IPv6 RADIUS IP

###### 4. 为指定HWTACACS方案配置发送HWTACACS报文使用的源IP地址

(1) 进入系统视图。
system-view
进入 方案视图。
(2) HWTACACS
hwtacacs scheme hwtacacs-scheme-name
设置设备发送 报文使用的源 地址。
(3) HWTACACS IP
nas-ip { ipv4-address | interface interface-type interface-number | ipv6
ipv6-address }

缺省情况下，未指定设备发送 HWTACACS 报文使用的源 IP 地址，使用系统视图下由命令指定的源 地址。
hwtacacs nas-ip IP

##### 1.6.10 配置发送给HWTACACS服务器的用户名格式和数据统计单位

###### 1. 功能简介

接入用户通常以“userid@isp-name”的格式命名，“@”后面的部分为 ISP 域名，设备通过该域名决定将用户归于哪个 ISP 域的。由于有些 HWTACACS 服务器不能接受携带有 ISP 域名的用户名，因此就需要设备首先将用户名中携带的 ISP 域名去除后再传送给该类 HWTACACS 服务器。通过设置发送给 服务器的用户名格式，就可以选择发送 服务器的用户名中是否HWTACACS HWTACACS要携带 ISP 域名。
设备通过发送计费报文，向 HWTACACS服务器报告在线用户的数据流量统计值，该值的单位可配。

###### 2. 配置限制和指导

如果要在两个乃至两个以上的 ISP 域中引用相同的 HWTACACS 方案，建议设置该 HWTACACS 方案允许用户名中携带 ISP 域名，使得 HWTACACS 服务器端可以根据 ISP 域名来区分不同的用户。
为保证 HWTACACS 服务器计费的准确性，设备上设置的发送给 HWTACACS 服务器的数据流或者数据包的单位应与 服务器上的流量统计单位保持一致。
HWTACACS

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 HWTACACS 方案视图。
hwtacacs scheme hwtacacs-scheme-name
设置发送给 服务器的用户名格式。
(3) HWTACACS
user-name-format { keep-original | with-domain | without-domain }
缺省情况下，发送给 服务器的用户名携带 域名。
HWTACACS ISP
设置发送给 服务器的数据流或者数据包的单位。
(4) HWTACACS
data-flow-format { data { byte | giga-byte | kilo-byte | mega-byte } |
packet { giga-packet | kilo-packet | mega-packet | one-packet } } *
缺省情况下，数据流的单位为字节，数据包的单位为包。

##### 1.6.11 配置HWTACACS计费报文缓存功能

###### 1. 功能简介

当用户请求断开连接或者设备强行切断用户连接的情况下，设备会向 HWTACACS 计费服务器发送停止计费请求报文，通过开启对无响应的 HWTACACS 停止计费请求报文的缓存功能，将其缓存在本机上，然后发送直到 HWTACACS 计费服务器产生响应，或者在发起停止计费请求报文的尝试次数达到指定的最大值后将其丢弃。

###### 2. 配置步骤

(1) 进入系统视图。
system-view

(2) 进入 HWTACACS 方案视图。
hwtacacs scheme hwtacacs-scheme-name
(3) 开启对无响应的 HWTACACS 停止计费请求报文的缓存功能。
stop-accounting-buffer enable
缺省情况下，设备缓存未得到响应的 HWTACACS 计费请求报文。
(4) （可选）设置发起 HWTACACS 停止计费请求的最大尝试次数。
retry stop-accounting retries
缺省情况下，发起 HWTACACS 停止计费请求的最大尝试次数为 100。

##### 1.6.12 HWTACACS显示和维护

完成上述配置后，在任意视图下执行 命令可以显示配置后 的运行情况，通display HWTACACS过查看显示信息验证配置的效果。
在用户视图下，执行 reset 命令可以清除相关统计信息。
表1-6 HWTACACS 显示和维护操作 命令查看所有或指定HWTACACS方案的配置信息或 display hwtacacs scheme [ hwtacacs-scheme-name统计信息 [ statistics ] ]显示缓存的HWTACACS停止计费请求报文的相 display stop-accounting-buffer关信息 hwtacacs-scheme hwtacacs-scheme-name reset hwtacacs statistics { accounting | all |清除HWTACACS协议的统计信息authentication | authorization } reset stop-accounting-buffer hwtacacs-scheme清除缓存的HWTACACS停止计费请求报文hwtacacs-scheme-name

#### 1.7 配置LDAP

##### 1.7.1 LDAP配置任务简介

LDAP 配置任务如下：
(1) 配置 LDAP 服务器
a. 创建LDAP服务器
b. 配置LDAP服务器IP地址
c. （可选）配置LDAP版本号
d. （可选）配置LDAP服务器的连接超时时间
e. 配置具有管理员权限的用户属性配置 用户属性参数
f. LDAP（可选）配置LDAP属性映射表
(2)
创建LDAP方案
(3)
指定LDAP认证服务器
(4)

###### 2. 配置步骤

(5) （可选）指定LDAP授权服务器
(6) （可选）引用LDAP属性映射表

##### 1.7.2 创建LDAP服务器

(1) 进入系统视图。
system-view
(2) 创建 LDAP 服务器，并进入 LDAP 服务器视图。
ldap server server-name

##### 1.7.3 配置LDAP服务器IP地址

###### 1. 配置限制和指导

LDAP服务器视图下仅能同时存在一个 IPv4地址类型的 LDAP服务器或一个 IPv6地址类型的 LDAP服务器。多次配置，后配置的生效。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 LDAP 服务器视图。
ldap server server-name
(3) 配置 LDAP 服务器 IP 地址。
{ ip ipv4-address | ipv6 ipv6-address } [ port port-number ] [ vpn-instance vpn-instance-name ]缺省情况下，未配置 LDAP 服务器 IP 地址。

##### 1.7.4 配置LDAP版本号

###### 1. 配置限制和指导

目前设备仅支持 LDAPv2 和 LDAPv3 两个协议版本。
Microsoft 的 LDAP 服务器只支持 LDAPv3 版本。
设备上配置的 LDAP 版本号需要与服务器支持的版本号保持一致。

###### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入 LDAP 服务器视图。
ldap server server-name
(3) 配置 LDAP 版本号。
protocol-version { v2 | v3 }缺省情况下，LDAP 版本号为 LDAPv3。

###### 1. 功能简介

##### 1.7.5 配置LDAP服务器的连接超时时间

功能简介
1.
设备向 LDAP 服务器发送绑定请求、查询请求，如果经过指定的时间后未收到 LDAP 服务器的回应，则认为本次认证、授权请求超时。若使用的 域中配置了备份的认证、授权方案，则设备会继续ISP尝试进行其他方式的认证、授权处理，否则本次认证、授权失败。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 LDAP 服务器视图。
ldap server server-name
(3) 配置 LDAP 服务器的连接超时时间。
server-timeout time-interval
缺省情况下，LDAP 服务器的连接超时时间为 10 秒。

##### 1.7.6 配置具有管理员权限的用户属性

###### 1. 功能简介

配置 LDAP 认证过程中绑定服务器所使用的用户 DN 和用户密码，该用户具有管理员权限。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 LDAP 服务器视图。
ldap server server-name
(3) 配置具有管理员权限的用户 DN。
login-dn dn-string
缺省情况下，未配置具有管理员权限的用户 DN。
配置的管理员权限的用户 必须与 服务器上管理员的 一致。
DN LDAP DN
配置具有管理员权限的用户密码。
(4)
login-password { ciper | simple } string
缺省情况下，未配置具有管理权限的用户密码。

##### 1.7.7 配置LDAP用户属性参数

###### 1. 功能简介

要对用户进行身份认证，就需要以用户 及密码为参数与 服务器进行绑定，因此需要首先DN LDAP从 LDAP 服务器获取用户 DN 。 LDAP 提供了一套 DN 查询机制，在与 LDAP 服务器建立连接的基础上，按照一定的查询策略向服务器发送查询请求。该查询策略由设备上指定的 LDAP 用户属性定义，具体包括以下几项：
用户 DN 查询的起始节点（search-base-dn）
•

用户 DN 查询的范围（search-scope）
•用户名称属性（user-name-attribute）
•用户名称格式（user-name-format）
•
• 用户对象类型（user-object-class）

###### 2. 配置限制和指导

服务器上的目录结构可能具有很深的层次，如果从根目录进行用户 的查找，耗费的时间LDAP DN将会较长，因此必须配置用户查找的起始点 DN，以提高查找效率。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 LDAP 服务器视图。
ldap server server-name
(3) 配置用户查询的起始 DN。
search-base-dn base-dn
缺省情况下，未指定用户查询的起始 DN。
（可选）配置用户查询的范围。
(4)
search-scope { all-level | single-level }
缺省情况下，用户查询的范围为 all-level。
（可选）配置用户查询的用户名属性。
(5)
user-parameters user-name-attribute { name-attribute | cn | uid }
缺省情况下，用户查询的用户名属性为 cn。
(6) （可选）配置用户查询的用户名格式。
user-parameters user-name-format { with-domain | without-domain }
缺省情况下，用户查询的用户名格式为 without-domain。
(7) （可选）配置用户查询的自定义用户对象类型。
user-parameters user-object-class object-class-name
缺省情况下，未指定自定义用户对象类型，根据使用的 LDAP 服务器的类型使用各服务器缺
省的用户对象类型。

##### 1.7.8 配置LDAP属性映射表

###### 1. 功能简介

在用户的 授权过程中，设备会通过查询操作得到用户的授权信息，该授权信息由 服务LDAP LDAP器通过若干 LDAP 属性下发给设备。若设备从 LDAP 服务器查询得到某 LDAP 属性，则该属性只有在被设备的 AAA 模块解析之后才能实际生效。如果某 LDAP 服务器下发给用户的属性不能被 AAA模块解析，则该属性将被忽略。因此，需要通过配置 LDAP 属性映射表来指定要获取哪些 LDAP 属性，以及 服务器下发的这些属性将被 模块解析为什么类型的 属性，具体映射为哪LDAP AAA AAA种类型的 AAA 属性由实际应用需求决定。

###### 2. 配置步骤

每一个 LDAP 属性映射表项定义了一个 LDAP 属性与一个 AAA 属性的对应关系。将一个 LDAP 属性表在指定的 方案视图中引用后，该映射关系将在 授权过程中生效。
LDAP LDAP

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 创建 LDAP 的属性映射表，并进入属性映射表视图。
ldap attribute-map map-name
(3) 配置 LDAP 属性映射表项。
map ldap-attribute ldap-attribute-name [ prefix prefix-value delimiter
delimiter-value ] aaa-attribute { user-group | user-profile }

##### 1.7.9 创建LDAP方案

###### 1. 配置限制和指导

系统最多支持配置 16 个 LDAP 方案。一个 LDAP 方案可以同时被多个 ISP 域引用。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 创建 LDAP 方案，并进入 LDAP 方案视图。
ldap scheme ldap-scheme-name

##### 1.7.10 指定LDAP认证服务器

进入系统视图。
(1)
system-view进入 方案视图。
(2) LDAP ldap scheme ldap-scheme-name
(3) 指定 LDAP 认证服务器。
authentication-server server-name缺省情况下，未指定 LDAP 认证服务器。

##### 1.7.11 指定LDAP授权服务器

(1) 进入系统视图。
system-view
进入 方案视图。
(2) LDAP
ldap scheme ldap-scheme-name
指定 授权服务器。
(3) LDAP
authorization-server server-name
缺省情况下，未指定 授权服务器。
LDAP

###### 1. 功能简介

##### 1.7.12 引用LDAP属性映射表

功能简介
1.
在使用 LDAP 授权方案的情况下，可以通过在 LDAP 方案中引用 LDAP 属性映射表，将 LDAP 授权服务器下发给用户的 属性映射为 模块可以解析的某类属性。
LDAP AAA

###### 2. 配置限制和指导

一个 LDAP 方案视图中只能引用一个 LDAP 属性映射表，后配置的生效。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 LDAP 方案视图。
ldap scheme ldap-scheme-name
(3) 引用 LDAP 属性映射表。
attribute-map map-name
缺省情况下，未引用任何 属性映射表。
LDAP

##### 1.7.13 LDAP显示和维护

完成上述配置后，在任意视图下执行 display 命令可以显示配置后 LDAP 的运行情况，通过查看显示信息验证配置的效果。
表1-7 LDAP 显示和维护操作 命令查看所有或指定LDAP方案的配置信息 display ldap scheme [ ldap-scheme-name ]

#### 1.8 创建ISP域

##### 1.8.1 ISP域简介

在多 ISP 的应用环境中，不同 ISP 域的用户有可能接入同一台设备。而且各 ISP 用户的用户属性（例如用户名及密码构成、服务类型/权限等）有可能不相同，因此有必要通过设置 ISP 域把它们区分开，并为每个 ISP 域单独配置一套认证、授权、计费方法及 ISP 域的相关属性。
对于设备来说，每个接入用户都属于一个 ISP 域。系统中最多可以配置 16 个 ISP 域，包括一个系统缺省存在的名称为 的 域。如果某个用户在登录时没有提供 域名，系统将把它归system ISP ISP于缺省的 ISP 域。系统缺省的 ISP 域可以手工修改为一个指定的 ISP 域；如果用户所属的 ISP 域下未应用任何认证、授权、计费方法，系统将使用缺省的认证、授权、计费方法，分别为本地认证、本地授权和本地计费。
用户认证时，设备将按照如下先后顺序为其选择认证域：接入模块指定的认证域-->用户名中指定的ISP 域-->系统缺省的 ISP 域。其中，接入模块是否支持指定认证域由各接入模块决定。如果根据以

###### 2. 配置步骤

上原则决定的认证域在设备上不存在，但设备上为未知域名的用户指定了 ISP 域，则最终使用该指定的 域认证，否则，用户将无法认证。
ISP

##### 1.8.2 配置限制和指导

一个 ISP 域被配置为缺省的 ISP 域后，将不能够被删除，必须首先使用命令 undo domain default enable 将其修改为非缺省 ISP 域，然后才可以被删除。
系统缺省存在的 system 域只能被修改，不能被删除。
如果一个 ISP 域中使用 RADIUS 方案对用户进行认证、授权或计费，请合理规划域名的长度，并保证设备发送给RADIUS服务器的整体用户名长度不超过253字符，否会导致认证、授权或计费失败。

##### 1.8.3 创建非缺省ISP域

(1) 进入系统视图。
system-view
(2) 创建 ISP 域并进入其视图。
domain isp-name
缺省情况下，存在一个的 ISP 域，名称为 system。

##### 1.8.4 配置缺省ISP域

(1) 进入系统视图。
system-view
(2) 配置缺省的 ISP 域。
domain default enable isp-name
缺省情况下，系统缺省的 ISP 域为 system。

##### 1.8.5 配置未知域名用户的ISP域

进入系统视图。
(1)
system-view配置未知域名的用户的 域。
(2) ISP domain if-unknown isp-name缺省情况下，没有为未知域名的用户指定 ISP 域。

#### 1.9 配置ISP域的属性

##### 1.9.1 配置ISP域的状态

###### 1. 功能简介

通过域的状态（active、block）控制是否允许该域中的用户请求网络服务。
配置步骤
2.
(1) 进入系统视图。

system-view
(2) 进入 ISP 域视图。
domain isp-name
(3) 设置 ISP 域的状态。
state { active | block }缺省情况下，当前 ISP 域处于活动状态，即允许任何属于该域的用户请求网络服务。

##### 1.9.2 配置ISP域的用户授权属性

###### 1. 授权属性介绍

ISP 域下可配置如下授权属性：
• ACL：用户被授权访问匹配指定 ACL 的网络资源。
• CAR：用户流量将受到指定的监管动作控制。
• 可点播的最大节目数：用户可以同时点播的最大节目数。
• IPv4 地址池：用户可以从指定的地址池中分配得到一个 IPv4 地址。
• IPv6 地址池：用户可以从指定的地址池中分配得到一个 IPv6 地址。
• 重定向 URL：用户认证成功后，首次访问网络时将被推送此 URL 提供的 Web 页面。
• 用户组：用户将继承该用户组中的所有属性。
• User Profile：用户访问行为将受到该 User Profile 中预设配置的限制。
用户认证成功之后，优先采用服务器下发的属性值，其次采用 ISP 域下配置的属性值。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 ISP 域视图。
domain isp-name
(3) 设置当前 ISP 域下的用户授权属性。
authorization-attribute { acl acl-number | car inbound cir
committed-information-rate [ pir peak-information-rate ] outbound cir
committed-information-rate [ pir peak-information-rate ] | igmp
max-access-number max-access-number | ip-pool ipv4-pool-name |
ipv6-pool ipv6-pool-name | mld max-access-number max-access-number |
url url-string | user-group user-group-name | user-profile
profile-name }
缺省情况下，IPv4 用户可以同时点播的最大节目数为 4，IPv6 用户可以同时点播的最大节目
数为 4，无其它授权属性。

###### 1. 功能简介

###### 2. 配置步骤

##### 1.9.3 设置设备上传到服务器的用户在线时间中保留闲置切断时间

功能简介
1.
设备上传到服务器的用户在线时间中保留闲置切断时间：当用户异常下线时，上传到服务器上的用户在线时间中包含了一定的闲置切断时间，此时服务器上记录的用户时长将大于用户实际在线时长。
该闲置切断时间在用户认证成功后由 AAA 授权，对于 Portal 认证用户，若接入接口上开启了 Portal用户在线探测功能，则 Portal 在线探测闲置时长为闲置切断时间。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 ISP 域视图。
domain isp-name
(3) 设置设备上传到服务器的用户在线时间中保留闲置切断时间。
session-time include-idle-time缺省情况下，设备上传到服务器的用户在线时间中扣除闲置切断时间。

#### 1.10 在ISP域中配置实现AAA的方法

##### 1.10.1 配置ISP域的AAA认证方法

###### 1. 配置限制和指导

配置 域的 认证方法时，需要注意的是：
ISP AAA当选择了 协议的认证方案以及非 协议的授权方案时，AAA 只接受
• RADIUS RADIUS RADIUS服务器的认证结果，RADIUS 授权的信息虽然在认证成功回应的报文中携带，但在认证回应的处理流程中不会被处理。
• 当使用 HWTACACS 方案进行用户角色切换认证时，系统使用用户输入的用户角色切换用户名进行角色切换认证；当使用 RADIUS 方案进行用户角色切换认证时，系统使用 RADIUS 服务器上配置的“$enabn$”形式的用户名进行用户角色切换认证，其中 为用户希望切换到的n用户角色 level-n 中的 n。
• FIPS 模式下不支持 none 认证方法。

###### 2. 配置准备

配置前的准备工作：
• 确定要配置的接入方式或者服务类型。AAA 可以对不同的接入方式和服务类型配置不同的认证方案。
• 确定是否为所有的接入方式或服务类型配置缺省的认证方法，缺省的认证方法对所有接入用户都起作用，但其优先级低于为具体接入方式或服务类型配置的认证方法。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
进入 域视图。
(2) ISP

domain isp-name
(3) （可选）为当前 ISP 域配置缺省的认证方法。
authentication default { hwtacacs-scheme hwtacacs-scheme-name [ radius-scheme radius-scheme-name ] [ local ] [ none ] | ldap-scheme ldap-scheme-name [ local ] [ none ] | local [ none ] | none | radius-scheme radius-scheme-name [ hwtacacs-scheme hwtacacs-scheme-name ] [ local ] [ none ] }缺省情况下，当前 ISP 域的缺省认证方法为 local。
(4) 为指定类型的用户或服务配置认证方法。
为 lan-access 用户配置认证方法。
(cid:123)
authentication lan-access { ldap-scheme ldap-scheme-name [ local ] [ none ] | local [ none ] | none | radius-scheme radius-scheme-name [ local ] [ none ] }缺省情况下，lan-access 用户采用缺省的认证方法。
为 login 用户配置认证方法。
(cid:123)
authentication login { hwtacacs-scheme hwtacacs-scheme-name [ radius-scheme radius-scheme-name ] [ local ] [ none ] | ldap-scheme ldap-scheme-name [ local ] [ none ] | local [ none ] | none | radius-scheme radius-scheme-name [ hwtacacs-scheme hwtacacs-scheme-name ] [ local ] [ none ] }缺省情况下，login 用户采用缺省的认证方法。
为 用户配置认证方法。
Portal (cid:123)
authentication portal { ldap-scheme ldap-scheme-name [ local ] [ none ] | local [ none ] | none | radius-scheme radius-scheme-name [ local ] [ none ] }缺省情况下，Portal 用户采用缺省的认证方法。
配置用户角色切换认证方法。
(cid:123)
authentication super { hwtacacs-scheme hwtacacs-scheme-name | radius-scheme radius-scheme-name } *缺省情况下，用户角色切换认证采用缺省的认证方法。

##### 1.10.2 配置ISP域的AAA授权方法

###### 1. 配置限制和指导

配置 ISP 域的 AAA 授权方法时，需要注意的是：
目前设备暂不支持使用 LDAP 进行授权。
•
• 在一个 ISP 域中，只有 RADIUS 授权方法和 RADIUS 认证方法引用了相同的 RADIUS 方案，授权才能生效。若 授权未生效或者 授权失败，则用户认证会失败。
RADIUS RADIUS RADIUS模式下不支持 none 授权方法。
• FIPS

###### 2. 配置准备

配置前的准备工作：
• 确定要配置的接入方式或者服务类型，AAA 可以按照不同的接入方式和服务类型进行 AAA 授权的配置。
• 确定是否为所有的接入方式或服务类型配置缺省的授权方法，缺省的授权方法对所有接入用户都起作用，但其优先级低于为具体接入方式或服务类型配置的授权方法。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
进入 域视图。
(2) ISP
domain isp-name
（可选）为当前 域配置缺省的授权方法。
(3) ISP
authorization default { hwtacacs-scheme hwtacacs-scheme-name
[ radius-scheme radius-scheme-name ] [ local ] [ none ] | local [ none ] |
none | radius-scheme radius-scheme-name [ hwtacacs-scheme
hwtacacs-scheme-name ] [ local ] [ none ] }
缺省情况下，当前 ISP 域的缺省授权方法为 local。
(4) 为指定类型的用户或服务配置授权方法。
配置命令行授权方法。
(cid:123)
authorization command { hwtacacs-scheme hwtacacs-scheme-name [ local ]
[ none ] | local [ none ] | none }
缺省情况下，命令行授权采用缺省的授权方法。
为 lan-access 用户配置授权方法。
(cid:123)
authorization lan-access { local [ none ] | none | radius-scheme
radius-scheme-name [ local ] [ none ] }
缺省情况下，lan-access 用户采用缺省的授权方法。
为 login 用户配置授权方法。
(cid:123)
authorization login { hwtacacs-scheme hwtacacs-scheme-name
[ radius-scheme radius-scheme-name ] [ local ] [ none ] | local [ none ]
| none | radius-scheme radius-scheme-name [ hwtacacs-scheme
hwtacacs-scheme-name ] [ local ] [ none ] }
缺省情况下，login 用户采用缺省的授权方法。
为 Portal 用户配置授权方法。
(cid:123)
authorization portal { local [ none ] | none | radius-scheme
radius-scheme-name [ local ] [ none ] }
缺省情况下， Portal 用户采用缺省的授权方法。

###### 3. 配置步骤

##### 1.10.3 配置ISP域的AAA计费方法

###### 1. 配置限制和指导

配置 ISP 域的 AAA 认证方法时，需要注意的是：
• 不支持对 FTP 类型 login 用户进行计费。
• 本地计费仅用于配合本地用户视图下的access-limit 命令来实现对本地用户连接数的限制功能。
FIPS 模式下不支持 none 计费方法。
•

###### 2. 配置准备

配置前的准备工作：
确定要配置的接入方式或者服务类型，AAA 可以按照不同的接入方式和服务类型进行 计
• AAA费的配置。
• 确定是否为所有的接入方式或服务类型配置缺省的计费方法，缺省的计费方法对所有接入用户都起作用，但其优先级低于为具体接入方式或服务类型配置的计费方法。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 进入 ISP 域视图。
domain isp-name
(3) （可选）为当前 ISP 域配置缺省的计费方法。
accounting default { hwtacacs-scheme hwtacacs-scheme-name [ radius-scheme radius-scheme-name ] [ local ] [ none ] | local [ none ] | none | radius-scheme radius-scheme-name [ hwtacacs-scheme hwtacacs-scheme-name ] [ local ] [ none ] }缺省情况下，当前 ISP 域的缺省计费方法为 local。
(4) 为指定类型的用户配置计费方法。
配置命令行计费方法。
(cid:123)
accounting command hwtacacs-scheme hwtacacs-scheme-name缺省情况下，命令行计费采用缺省的计费方法。
为 用户配置计费方法。
lan-access (cid:123)
accounting lan-access { broadcast radius-scheme radius-scheme-name1 radius-scheme radius-scheme-name2 [ local ] [ none ] | local [ none ] | none | radius-scheme radius-scheme-name [ local ] [ none ] }缺省情况下，lan-access 用户采用缺省的计费方法。
为 login 用户配置计费方法。
(cid:123)
accounting login { hwtacacs-scheme hwtacacs-scheme-name [ radius-scheme radius-scheme-name ] [ local ] [ none ] | local [ none ] | none | radius-scheme radius-scheme-name [ hwtacacs-scheme hwtacacs-scheme-name ] [ local ] [ none ] }

缺省情况下，login 用户采用缺省的计费方法。
为 Portal 用户配置授权方法。
(cid:123)
accounting portal { broadcast radius-scheme radius-scheme-name1 radius-scheme radius-scheme-name2 [ local ] [ none ] | local [ none ] | none | radius-scheme radius-scheme-name [ local ] [ none ] }缺省情况下，Portal 用户采用缺省的计费方法。
(5) （可选）配置扩展计费策略。
配置用户计费开始失败策略。
(cid:123)
accounting start-fail { offline | online }缺省情况下，如果用户计费开始失败，则允许用户保持在线状态。
配置用户计费更新失败策略。
(cid:123)
accounting update-fail { [ max-times times ] offline | online }缺省情况下，如果用户计费更新失败，允许用户保持在线状态。
配置用户计费配额（流量或时长）耗尽策略。
(cid:123)
accounting quota-out { offline | online }缺省情况下，用户的计费配额耗尽后将被强制下线。

##### 1.10.4 ISP域显示和维护

完成上述配置后，在任意视图下执行 display 命令可以显示配置后 AAA 的运行情况，通过查看显示信息验证配置的效果。
表1-8 域显示和维护ISP操作 命令显示所有或指定ISP域的配置信息 display domain [ isp-name ]

#### 1.11 限制同时在线的最大用户连接数

##### 1. 功能简介

通过配置同时在线的最大用户连接数，可以限制采用指定登录方式（FTP、SSH、Telnet 等）同时接入设备的在线用户数。
该配置对于通过任何一种认证方式（none、password 或者 scheme）接入设备的用户都生效。

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置同时在线的最大用户连接数。
（非 FIPS 模式）
aaa session-limit { ftp | http | https | ssh | telnet } max-sessions
（FIPS 模式）

#### 1.14 配置设备作为RADIUS服务器

aaa session-limit { https | ssh } max-sessions缺省情况下，最大用户连接数为 32。

#### 1.12 配置NAS-ID

##### 1. NAS-ID的应用

用户进行 RADIUS 认证时，系统会获取设备的 NAS-ID 来设置 RADIUS 报文中的 NAS-Identifier 属性，该属性用于向 RADIUS 服务器标识用户的接入位置。
若在实际网络中，用户的接入 VLAN 可以标识用户的接入位置，则可通过建立用户接入 VLAN 与指定的 NAS-ID 之间的绑定关系来实现接入位置信息的映射。

##### 2. 配置限制和指导

将被 或端口安全相应特性进行引用，具体应用请参见“安全配置指导”中的NAS-ID Profile Portal“Portal”或“端口安全”。
一个 NAS-ID profile 中可以指定多组 NAS-ID 和 VLAN 绑定。
一个 可以与多个 进行绑定，一个 只能绑定一个 NAS-ID。
NAS-ID VLAN VLAN

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 创建 NAS-ID Profile，并进入 NAS-ID-Profile 视图。
aaa nas-id profile profile-name
(3) 设置 NAS-ID 与 VLAN 的绑定关系。
nas-id nas-identifier bind vlan vlan-id

#### 1.13 配置设备ID

##### 1. 功能简介

RADIUS 计费过程使用 Acct-Session-Id 属性作为用户的计费 ID。设备使用系统时间、随机数以及设备 ID 为每个在线用户生成一个唯一的 Acct-Session-Id 值。

##### 2. 配置步骤

进入系统视图。
(1)
system-view配置设备 ID。
(2)
aaa device-id device-id缺省情况下，设备 ID 为 0。
配置设备作为 服务器
1.14 RADIUS

##### 1.14.1 配置任务简介

配置设备作为 RADIUS 服务器任务如下：

(1) 配置RADIUS用户
(2) 指定RADIUS客户端
(3) 激活RADIUS服务器配置

##### 1.14.2 配置限制和指导

为保证 RADIUS 服务器功能可以正常运行，请确保 RADIUS session control 功能处于关闭状态。

##### 1.14.3 配置RADIUS用户

RADIUS用户通过网络接入类本地用户进行配置管理。RADIUS用户支持的用户属性包括用户名、密码、描述信息、授权ACL、授权VLAN以及过期截止时间，具体配置请参见“1.4.4 配置网络接入类本地用户属性”。

##### 1.14.4 指定RADIUS客户端

###### 1. 功能简介

本配置用来指定要管理的 RADIUS 客户端的 IP 地址，以及与 RADIUS 客户端通信的共享密钥。

###### 2. 配置限制和指导

RADIUS 服务器上指定的 RADIUS 客户端 IP 地址必须和 RADIUS 客户端上配置的发送 RADIUS 报文的源 IP 地址保持一致。
RADIUS 服务器上指定的共享密钥必须和 RADIUS 客户端上配置的共享密钥保持一致。

###### 3. 配置步骤

进入系统视图。
(1)
system-view指定 客户端。
(2) RADIUS radius-server client ip ipv4-address key { cipher | simple } string

##### 1.14.5 激活RADIUS服务器配置

###### 1. 功能简介

设备启动后会自动激活已有的 客户端和 用户配置。之后若对 客户端和RADIUS RADIUS RADIUS网络接入类本地用户进行了增加、修改或删除操作，则都需要使用此命令对其进行激活，否则更新后的配置不生效。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 激活 RADIUS 服务器配置。
radius-server activate
执行激活命令会导致 RADIUS 服务器进程重启。RADIUS 服务器进程重启期间，设备无法作
为 RADIUS 服务器为用户提供认证服务。

##### 1.14.6 RADIUS服务器显示和维护

完成上述配置后，在任意视图下执行 命令可以显示处于激活状态的 用户和display RADIUS RADIUS 客户端信息，通过查看显示信息验证配置的效果。
表1-9 服务器显示和维护RADIUS操作 命令显示处于激活状态的RADIUS客户端display radius-server active-client信息显示处于激活状态的RADIUS用户信display radius-server active-user [ user-name ]息

#### 1.15 配置连接记录策略

##### 1.15.1 功能简介

本功能适用于设备作为 Telnet 客户端或者 FTP/SSH/SFTP 客户端与服务器端建立连接的场景。如果设备上配置了连接记录策略，当设备作为客户端与服务器端成功建立连接时，系统会按照策略中指定的计费方案向 AAA 服务器发送计费开始报文，并在设备与服务器端断开连接时发送计费结束报文。通过此功能，AAA 服务器上将会记录设备的连接情况，便于管理员进行查看。

##### 1.15.2 配置限制和指导

连接记录业务处理过程中，系统发送给 AAA 服务器的计费报文中封装的是用户输入的原始用户名，因此计费方案中通过 user-name-format 命令设置的用户名格式并不生效。

##### 1.15.3 配置步骤

(1) 进入系统视图。
system-view
(2) 创建连接计录策略，并进入连接记录策略视图。
aaa connection-recording policy
(3) 指定连接记录策略采用的 HWTACACS 计费方案。
accounting hwtacacs-scheme hwtacacs-scheme-name

##### 1.15.4 连接记录策略显示和维护

完成上述配置后，在任意视图下执行 display 命令可以显示连接记录策略的配置信息。
表1-10 连接记录策略显示和维护操作 命令显示连接记录策略的配置信息 display aaa connection-recording policy

#### 1.16 AAA典型配置举例

##### 1.16.1 SSH用户的HWTACACS认证、授权、计费配置

###### 1. 组网需求

通过配置 Switch 实现使用 HWTACACS 服务器对 SSH 登录 Switch 的用户进行认证、授权、计费。
由一台 服务器担当认证、授权、计费服务器的职责，服务器 地址为 10.1.1.1/24。
• HWTACACS IP与认证、授权、计费 服务器交互报文时的共享密钥均为 expert，向
• Switch HWTACACS HWTACACS 服务器发送的用户名中不带域名。
• SSH 用户登录 Switch 时使用 HWTACACS 服务器上配置的用户名以及密码进行认证，认证通过后具有缺省的用户角色 network-operator。

###### 2. 组网图

图1-12 SSH 用户 HWTACACS 认证、授权和计费配置组网图

###### 3. 配置HWTACACS服务器

在 HWTACACS服务器上设置与 Switch交互报文时的共享密钥为 expert；添加 SSH用户名及密码，具体配置步骤略。

###### 4. 配置Switch

\# 配置各接口的 IP 地址，具体配置步骤略。
\# 创建 HWTACACS 方案 hwtac 。
<Switch> system-view [Switch] hwtacacs scheme hwtac \# 配置主认证服务器的 IP 地址为 10.1.1.1，认证端口号为 49。
[Switch-hwtacacs-hwtac] primary authentication 10.1.1.1 49 \# 配置主授权服务器的 IP 地址为 10.1.1.1，授权端口号为 49。
[Switch-hwtacacs-hwtac] primary authorization 10.1.1.1 49 \# 配置主计费服务器的 IP 地址为 10.1.1.1，计费端口号为 49。
[Switch-hwtacacs-hwtac] primary accounting 10.1.1.1 49 \# 配置与认证、授权、计费服务器交互报文时的共享密钥均为明文 expert。
[Switch-hwtacacs-hwtac] key authentication simple expert [Switch-hwtacacs-hwtac] key authorization simple expert [Switch-hwtacacs-hwtac] key accounting simple expert

###### 1. 组网需求

\# 配置向 HWTACACS 服务器发送的用户名不携带域名。
[Switch-hwtacacs-hwtac] user-name-format without-domain [Switch-hwtacacs-hwtac] quit创建 域 bbb，为 用户配置 认证方法为 认证/授权/计费。
\# ISP login AAA HWTACACS [Switch] domain bbb [Switch-isp-bbb] authentication login hwtacacs-scheme hwtac [Switch-isp-bbb] authorization login hwtacacs-scheme hwtac [Switch-isp-bbb] accounting login hwtacacs-scheme hwtac [Switch-isp-bbb] quit \# 创建本地 RSA 及 DSA 密钥对。
[Switch] public-key local create rsa [Switch] public-key local create dsa \# 使能 SSH 服务器功能。
[Switch] ssh server enable \# 设置 SSH 用户登录用户线的认证方式为 AAA 认证。
[Switch] line vty 0 63 [Switch-line-vty0-63] authentication-mode scheme [Switch-line-vty0-63] quit \# 使能缺省用户角色授权功能，使得认证通过后的 SSH 用户具有缺省的用户角色 network-operator。
[Switch] role default-role enable

###### 5. 验证配置

用户向 Switch 发起 SSH 连接，按照提示输入正确用户名及密码后，可成功登录 Switch，并具有用户角色 network-operator 所拥有的命令行执行权限。

##### 1.16.2 SSH用户的local认证、HWTACACS授权、RADIUS计费配置

组网需求
1.
通过配置 Switch 实现 local 认证，HWTACACS 授权和 RADIUS 计费。SSH 用户的用户名和密码为hello。
一台HWTACACS服务器（担当授权服务器的职责）与Switch相连，服务器IP地址为10.1.1.2。
•与授权 服务器交互报文时的共享密钥均为 expert，发送给Switch HWTACACS HWTACACS服务器的用户名中不带域名。
• 一台 RADIUS 服务器（担当计费服务器的职责）与 Switch 相连，服务器 IP 地址为 10.1.1.1。
Switch 与计费 RADIUS 服务器交互报文时的共享密钥为 expert。
• 认证通过后的 SSH 用户具有缺省的用户角色 network-operator。

###### 2. 组网图

图1-13 SSH 用户 local 认证、HWTACACS 授权和 RADIUS 计费配置组网图

###### 3. 配置HWTACACS服务器

在 HWTACACS服务器上设置与 Switch交互报文时的共享密钥为 expert；添加 SSH用户名及密码，具体配置步骤略。

###### 4. 配置RADIUS服务器

在 服务器上设置与 交互报文时的共享密钥为 expert；添加 用户名及密码，具RADIUS Switch SSH体配置步骤略。

###### 5. 配置Switch

\# 配置各接口的 IP 地址，具体配置步骤略。
\# 创建本地 RSA 及 DSA 密钥对。
<Switch> system-view [Switch] public-key local create rsa [Switch] public-key local create dsa \# 使能 SSH 服务器功能。
[Switch] ssh server enable设置 用户登录用户线的认证方式为 认证。
\# SSH AAA [Switch] line vty 0 63 [Switch-line-vty0-63] authentication-mode scheme [Switch-line-vty0-63] quit配置 方案。
\# HWTACACS [Switch] hwtacacs scheme hwtac [Switch-hwtacacs-hwtac] primary authorization 10.1.1.2 49 [Switch-hwtacacs-hwtac] key authorization simple expert [Switch-hwtacacs-hwtac] user-name-format without-domain [Switch-hwtacacs-hwtac] quit \# 配置 RADIUS 方案。
[Switch] radius scheme rd [Switch-radius-rd] primary accounting 10.1.1.1 1813 [Switch-radius-rd] key accounting simple expert [Switch-radius-rd] user-name-format without-domain [Switch-radius-rd] quit

###### 6. 验证配置

###### 2. 组网图

\# 创建设备管理类本地用户 hello。
[Switch] local-user hello class manage \# 配置该本地用户的服务类型为 SSH。
[Switch-luser-manage-hello] service-type ssh \# 配置该本地用户密码为明文 123456TESTplat&!。（若是 FIPS模式下，只能使用交互式方式设置）。
[Switch-luser-manage-hello] password simple 123456TESTplat&!
[Switch-luser-manage-hello] quit创建 域 bbb，为 用户配置 认证方法为本地认证、HWTACACS 授权、RADIUS 计\# ISP login AAA费。
[Switch] domain bbb [Switch-isp-bbb] authentication login local [Switch-isp-bbb] authorization login hwtacacs-scheme hwtac [Switch-isp-bbb] accounting login radius-scheme rd [Switch-isp-bbb] quit \# 使能缺省用户角色授权功能，使得认证通过后的 SSH 用户具有缺省的用户角色 network-operator。
[Switch] role default-role enable验证配置
6.
用户向 Switch 发起 SSH 连接，按照提示输入用户名 hello@bbb 及正确的密码后，可成功登录 Switch，并具有用户角色 network-operator 拥有的命令行执行权限。

##### 1.16.3 SSH用户的RADIUS认证和授权配置

###### 1. 组网需求

配置 实现使用 服务器对登录 的 用户进行认证和授权。
Switch RADIUS Switch SSH由一台 iMC 服务器担当认证/授权 RADIUS 服务器的职责，服务器 IP 地址为 10.1.1.1/24。
•Switch 与 RADIUS 服务器交互报文时使用的共享密钥为 expert，向 RADIUS 服务器发送的用
•户名带域名。服务器根据用户名携带的域名来区分提供给用户的服务。
用户登录 时使用 服务器上配置的用户名 以及密码进行认证，
• SSH Switch RADIUS hello@bbb认证通过后具有缺省的用户角色 network-operator。
组网图
2.
图 1-14 SSH 用户 RADIUS 认证 / 授权配置组网图

###### 3. 配置RADIUS服务器

下面以 iMC 为例（使用 iMC 版本为：iMC PLAT 5.0(E0101)、iMC UAM 5.0(E0101)），说明RADIUS 服务器的基本配置。
(1) 增加接入设备登录进入 iMC 管理平台，选择“业务”页签，单击导航树中的[接入业务/接入设备管理/接入设备配置]菜单项，进入接入设备配置页面，在该页面中单击“增加”按钮，进入增加接入设备页面。
a. 设置与 Switch 交互报文时使用的认证、计费共享密钥为“expert”；
b. 设置认证及计费的端口号分别为“1812”和“1813”；
c. 选择业务类型为“设备管理业务”；
d. 选择接入设备类型为“H3C”；
e. 选择或手工增加接入设备，添加 IP 地址为 10.1.1.2 的接入设备；
f. 其它参数采用缺省值，并单击<确定>按钮完成操作。
添加的接入设备 IP 地址要与 Switch 发送 RADIUS 报文的源地址保持一致。缺省情况下，设备发送 RADIUS 报文的源地址是发送 RADIUS 报文的接口 IP 地址。
• 若设备上通过命令 nas-ip 或者 radius nas-ip 指定了发送 RADIUS 报文的源地址，则此处的接入设备 IP 地址就需要修改并与指定源地址保持一致。
若设备使用缺省的发送 RADIUS 报文的源地址，例如，本例中为接口 Vlan-interface3 的
•地址 10.1.1.2，则此处接入设备 地址就选择 10.1.1.2。
IP IP

图1-15 增加接入设备增加设备管理用户
(2)
选择“用户”页签，单击导航树中的[接入用户视图/设备管理用户]菜单项，进入设备管理用户列表页面，在该页面中单击<增加>按钮，进入增加设备管理用户页面。
a. 输入用户名“hello@bbb”和密码；
b. 选择服务类型为“SSH”；
添加所管理设备的 地址，IP 地址范围为“10.1.1.0～10.1.1.255”；
c. IP单击<确定>按钮完成操作。
d.
添加的所管理设备的 地址范围要包含添加的接入设备的 地址。
IP IP

图1-16 增加设备管理用户

###### 4. 配置Switch

\# 配置各接口的 IP 地址，具体配置步骤略。
生成 及 密钥对。
\# RSA DSA <Switch> system-view [Switch] public-key local create rsa [Switch] public-key local create dsa使能 服务器功能。
\# SSH [Switch] ssh server enable \# 设置 SSH 用户登录用户线的认证方式为 AAA 认证。
[Switch] line vty 0 63 [Switch-line-vty0-63] authentication-mode scheme [Switch-line-vty0-63] quit \# 使能缺省用户角色授权功能，使得认证通过后的 SSH 用户具有缺省的用户角色 network-operator 。
[Switch] role default-role enable \# 创建 RADIUS 方案 rad。
[Switch] radius scheme rad

\# 配置主认证服务器的 IP 地址为 10.1.1.1，认证端口号为 1812。
[Switch-radius-rad] primary authentication 10.1.1.1 1812 \# 配置与认证服务器交互报文时的共享密钥为明文 expert。
[Switch-radius-rad] key authentication simple expert配置向 服务器发送的用户名要携带域名。
\# RADIUS [Switch-radius-rad] user-name-format with-domain [Switch-radius-rad] quit \# 创建 ISP 域 bbb，为 login 用户配置 AAA 认证方法为 RADIUS 认证/授权、不计费。
[Switch] domain bbb [Switch-isp-bbb] authentication login radius-scheme rad [Switch-isp-bbb] authorization login radius-scheme rad [Switch-isp-bbb] accounting login none [Switch-isp-bbb] quit

###### 5. 验证配置

用户向 发起 连接，按照提示输入用户名 及正确的密码后，可成功登录 Switch，Switch SSH hello@bbb并具有用户角色 network-operator 所拥有的命令行执行权限。

##### 1.16.4 SSH用户的LDAP认证配置

###### 1. 组网需求

配置 Switch 实现使用 LDAP 服务器对登录 Switch 的 SSH 用户进行认证，且认证通过后具有缺省的用户角色 level-0。
• 一台 LDAP 认证服务器与 Switch 相连，服务器 IP 地址为 10.1.1.1。服务器域名为 ldap.com。
• 在 LDAP 服务器上设置管理员 administrator 的密码为 admin!123456；并添加用户名为 aaa的用户，密码为 ldap!123456。

###### 2. 组网图

图1-17 用户 认证配置组网图SSH LDAP

###### 3. 配置LDAP服务器

本文以 Microsoft Windows 2003 Server 的 Active Directory 为例，说明该例中 LDAP 服务器的基本配置。
(1) 添加用户 aaa
a. 在LDAP服务器上，选择[开始/管理工具]中的[Active Directory用户和计算机]，打开Active Directory 用户管理界面；
b. 在 Active Directory 用户管理界面的左侧导航树中，点击 ldap.com 节点下的“Users”按钮；
c. 选择[操作/新建/用户]，打开[新建对象-用户]对话框；
d. 在对话框中输入用户登录名 aaa，并单击<下一步>按钮。
图1-18 新建用户 aaa
e. 在弹出的对话框的“密码”区域框内输入用户密码 ldap!123456，并单击<下一步>按钮。
用户帐户的其它属性（密码的更改方式、密码的生存方式、是否禁用帐户）请根据实际情况选择配置，图中仅为示例。

图1-19 设置用户密码单击<完成>按钮，创建新用户 aaa。
f.
(2) 将用户 aaa 加入 Users 组
a. 在 Active Directory 用户管理界面的左侧导航树中，点击 ldap.com 节点下的“Users”按钮；
在右侧的 信息框中右键单击用户 aaa，选择“属性”项；
b. Users在弹出的[aaa 属性]对话框中选择“隶属于”页签，并单击<添加(D)...>按钮。
c.

图1-20 修改用户属性
d. 在弹出的[选择组]对话框中的可编辑区域框中输入对象名称“Users”，单击<确定>，完成用户 aaa 添加到 Users 组。
图1-21 添加用户 aaa 到用户组 Users
(3) 配置管理员密码

###### 5. 验证配置

a. 在右侧的 Users 信息框中右键单击管理员用户 administrator，选择“设置密码(S)...”项；
b. 在弹出的密码添加对话框中设置管理员密码，详细过程略。

###### 4. 配置Switch

配置各接口的 地址，具体配置步骤略。
\# IP生成本地 及 密钥对。
\# RSA DSA <Switch> system-view [Switch] public-key local create rsa [Switch] public-key local create dsa使能 服务器功能。
\# SSH [Switch] ssh server enable \# 设置 SSH 用户登录用户线的认证方式为 AAA 认证。
[Switch] line vty 0 63 [Switch-line-vty0-63] authentication-mode scheme [Switch-line-vty0-63] quit \# 创建 LDAP 服务器。
[Switch] ldap server ldap1配置 认证服务器的 地址。
\# LDAP IP [Switch-ldap-server-ldap1] ip 10.1.1.1 \# 配置具有管理员权限的用户 DN。
[Switch-ldap-server-ldap1] login-dn cn=administrator,cn=users,dc=ldap,dc=com \# 配置具有管理员权限的用户密码。
[Switch-ldap-server-ldap1] login-password simple admin!123456配置查询用户的起始目录。
\# [Switch-ldap-server-ldap1] search-base-dn dc=ldap,dc=com [Switch-ldap-server-ldap1] quit \# 创建 LDAP 方案。
[Switch] ldap scheme ldap-shm1 \# 配置 LDAP 认证服务器。
[Switch-ldap-ldap-shm1] authentication-server ldap1 [Switch-ldap-ldap-shm1] quit \# 创建 ISP 域 bbb ，为 login 用户配置 AAA 认证方法为 LDAP 认证、不授权、不计费。
[Switch] domain bbb [Switch-isp-bbb] authentication login ldap-scheme ldap-shm1 [Switch-isp-bbb] authorization login none [Switch-isp-bbb] accounting login none [Switch-isp-bbb] quit验证配置
5.
用户向 Switch 发起 SSH 连接，按照提示输入用户名 aaa@bbb 及正确的密码 ldap!123456 后，可成功登录 Switch，并具有用户角色 所拥有的命令行执行权限。
level-0

###### 1. 组网需求

##### 1.16.5 802.1X用户的RADIUS认证、授权和计费配置

组网需求
1.
需要实现使用 RADIUS 服务器对通过 Switch 接入的 802.1X 用户进行认证、授权和计费。
• 在接入端口 Ten-GigabitEthernet1/0/1 上对接入用户进行 802.1X 认证，并采用基于 MAC 地址的接入控制方式，即该端口下的所有用户都需要单独认证；
Switch 与 RADIUS 服务器交互报文时使用的共享密钥为 expert，认证/授权、计费的端口号分
•别为 和 1813，向 服务器发送的用户名携带域名；
1812 RADIUS用户认证时使用的用户名为 dot1x@bbb。
•用户认证成功后，认证服务器授权下发 4，将用户所在端口加入该 VLAN，允许用户访
• VLAN问该 VLAN 中的网络资源。
• 对 802.1X 用户进行包月方式计费，费用为 120 元/月，以月为周期对用户上网服务的使用量按时长进行统计，允许每月最大上网使用量为 120 个小时。

###### 2. 组网图

图1-22 802.1X 用户 RADIUS 认证、授权和计费配置组网图RADIUS server
10.1.1.1/24 Vlan-int3
10.1.1.2/24 Vlan-int2 Vlan-int4 Internet XGE1/0/1 Switch
802.1X user

###### 3. 配置RADIUS服务器

下面以 iMC 为例（使用 iMC 版本为： iMC PLAT 5.0(E0101) 、 iMC UAM 5.0(E0101) 、 iMC CAMS
5.0(E0101)），说明 服务器和 服务器的基本配置。
RADIUS Portal
(1) 增加接入设备登录进入 iMC 管理平台，选择“业务”页签，单击导航树中的[接入业务/接入设备配置]菜单项，进入接入设备配置页面，在该页面中单击“增加”按钮，进入增加接入设备页面。
a. 设置与 Switch 交互报文时的认证、计费共享密钥为“expert”；
b. 设置认证及计费的端口号分别为“1812”和“1813”；
c. 选择业务类型为“LAN 接入业务”；
d. 选择接入设备类型为“H3C”；
e. 选择或手工增加接入设备，添加 IP 地址为 10.1.1.2 的接入设备；

f. 其它参数采用缺省值，并单击<确定>按钮完成操作。
添加的接入设备 IP 地址要与 Switch 发送 RADIUS 报文的源地址保持一致。缺省情况下，设
备发送 报文的源地址是发送 报文的接口 地址。
RADIUS RADIUS IP
若设备使用缺省的发送 报文的源地址，例如，本例中为接口 的
• RADIUS Vlan-interface3
IP 地址 10.1.1.2，则此处接入设备 IP 地址就选择 10.1.1.2。
• 若设备上通过命令 nas-ip 或者 radius nas-ip 指定了发送 RADIUS 报文的源地址，
则此处的接入设备 IP 地址就需要修改并与指定源地址保持一致。
图1-23 增加接入设备
(2) 增加计费策略
选择“业务”页签，单击导航树中的[计费业务/计费策略管理]菜单项，进入计费策略管理页面，
在该页面中单击<增加>按钮，进入计费策略配置页面。
a. 输入计费策略名称“UserAcct”；
b. 选择计费策略模板为“包月类型计费”；
c. 设置包月基本信息：计费方式为“按时长”、计费周期为“月”、周期内固定费用为“120
元”；
d. 设置包月使用量限制：允许每月最大上网使用量为 120 个小时。
e. 其它参数采用缺省值，并单击<确定>按钮完成操作。

图1-24 增加计费策略
(3) 增加服务配置选择“业务”页签，单击导航树中的[接入业务/服务配置管理]菜单项，进入服务器配置管理页面，在该页面中单击<增加>按钮，进入增加服务配置页面。
a. 输入服务名为“Dot1x auth”、服务后缀为“bbb”，此服务后缀为 802.1X 用户使用的认证域。指定服务后缀的情况下，RADIUS 方案中必须指定向服务器发送的用户名中携带域名；
选择计费策略为“UserAcct”；
b.
配置授权下发的 为“4”；
c. VLAN ID本配置页面中还有其它服务配置选项，请根据实际情况选择配置；
d.
e. 单击<确定>按钮完成操作。

图1-25 增加服务配置
(4) 增加接入用户选择“用户”页签，单击导航树中的[接入用户视图/所有接入用户]菜单项，进入接入用户列表页面，在该页面中单击<增加>按钮，进入增加接入用户页面。
选择或者手工增加用户姓名为“test”；
a.
b. 输入帐号名“dot1x”和密码；
c. 选择该用户所关联的接入服务为“Dot1x auth”；
d. 本配置页面中还有其它服务配置选项，请根据实际情况选择配置；
e. 单击 < 确定 > 按钮完成操作。

图1-26 增加接入用户

###### 4. 配置Switch

(1) 配置 RADIUS 方案
\# 创建名称为 rad 的 RADIUS 方案并进入该方案视图。
<Switch> system-view
[Switch] radius scheme rad
\# 配置 RADIUS 方案的主认证和主计费服务器及其通信密钥。
[Switch-radius-rad] primary authentication 10.1.1.1
[Switch-radius-rad] primary accounting 10.1.1.1
[Switch-radius-rad] key authentication simple expert
[Switch-radius-rad] key accounting simple expert
\# 配置发送给 RADIUS 服务器的用户名携带 ISP 域名。
[Switch-radius-rad] user-name-format with-domain
[Switch-radius-rad] quit
(2) 配置 ISP 域
\# 创建并进入名称为 bbb 的 ISP 域。
[Switch] domain bbb
为 用户配置 认证方法为 认证/授权/计费，且均使用 方案
\# lan-access AAA RADIUS RADIUS
rad。
[Switch-isp-bbb] authentication lan-access radius-scheme rad
[Switch-isp-bbb] authorization lan-access radius-scheme rad
[Switch-isp-bbb] accounting lan-access radius-scheme rad
[Switch-isp-bbb] quit
配置 认证
(3) 802.1X
\# 开启全局 802.1X 认证。
[Switch] dot1x
\# 开启端口 Ten-GigabitEthernet1/0/1 的 802.1X 认证。

[Switch] interface ten-gigabitethernet 1/0/1 [Switch-Ten-GigabitEthernet1/0/1] dot1x \# 设置接入控制方式（该命令可以不配置，因为端口的接入控制在缺省情况下就是基于 MAC地址的）。
[Switch-Ten-GigabitEthernet1/0/1] dot1x port-method macbased

###### 5. 验证配置

• 若使用 Windows XP 的 802.1X 客户端，则需要正确设置此连接的网络属性：在网络属性的“验
证”页签中，确保选中“启用此网络的 IEEE 802.1x 验证”，并选择要用于此连接的 EAP 认证
类型为“MD5-质询”。
若使用 iNode 802.1X 客户端，则无需启用任何高级认证选项。
•
保证用户在通过认证后，能够及时更新客户端 IP 地址与授权 VLAN 中的资源互通。
•
对于使用 iNode 802.1X 客户端的用户，在客户端的用户属性中输入正确的用户名“dot1x@bbb”
和密码后，通过主动发起连接可成功通过认证；对于使用 Windows XP 802.1X 客户端的用户，在
系统自动弹出的认证对话框中输入正确的用户名“dot1x@bbb”和密码后，可成功通过认证。认证
通过后，服务器向该用户所在端口授权下发了 4。可使用命令
VLAN display dot1x connetion
查看到上线用户的连接情况。

##### 1.16.6 设备作为RADIUS服务器对802.1X用户进行认证和授权配置

###### 1. 组网需求

Switch B 做为 RADIUS 服务器对通过 Switch A 接入的 802.1X 用户进行认证和授权。
• 在 Switch A 接入端口 Ten-GigabitEthernet1/0/1 上对接入用户进行 802.1X 认证；
• Switch A与RADIUS服务器交互报文时使用的共享密钥为expert，认证/授权的端口号为1812，向 RADIUS 服务器发送的用户名不携带域名；
• 用户认证时使用的用户名为 dot1x。
• 用户认证成功后，认证服务器授权下发 VLAN 4，将用户所在端口加入该 VLAN，允许用户访问该 VLAN 中的网络资源。

###### 3. 配置步骤

###### 2. 组网图

图1-27 设备作为 RADIUS 服务器对 802.1X 用户进行认证和授权配置组网图配置步骤
3.
(1) 配置 NAS
a. 配置 RADIUS 方案\# 创建名称为 rad 的 RADIUS 方案并进入该方案视图。
<SwitchA> system-view [SwitchA] radius scheme rad \# 配置主认证服务器 IP 地址为 10.1.1.1，认证报文的共享密钥为明文 expert。
[SwitchA-radius-rad] primary authentication 10.1.1.1 key simple expert \# 配置发送给 RADIUS 服务器的用户名不携带 ISP 域名。
[SwitchA-radius-rad] user-name-format without-domain [SwitchA-radius-rad] quit
b. 配置 ISP 域\# 创建并进入名称为 bbb 的 ISP 域。
[SwitchA] domain bbb \# 为 lan-access用户配置 AAA认证方法为 RADIUS认证/授权，且均使用 RADIUS方案 rad，并配置不计费。
[SwitchA-isp-bbb] authentication lan-access radius-scheme rad [SwitchA-isp-bbb] authorization lan-access radius-scheme rad [SwitchA-isp-bbb] accounting lan-access none [SwitchA-isp-bbb] quit配置 认证
c. 802.1X开启端口 的 认证。
\# Ten-GigabitEthernet1/0/1 802.1X [SwitchA] interface ten-gigabitethernet 1/0/1 [SwitchA-Ten-GigabitEthernet1/0/1] dot1x \# 指定端口上接入的 802.1X 用户使用认证域 bbb。
[SwitchA-GigabitEthernet1/0/1] dot1x mandatory-domain bbb [SwitchA-Ten-GigabitEthernet1/0/1] quit \# 开启全局 802.1X 认证。
[SwitchA] dot1x
(2) 配置 RADIUS 服务器

###### 4. 验证配置

\# 创建网络接入本地用户 dot1x。
<SwitchB> system-view [SwitchB] local-user dot1x class network配置用户密码为明文 123456。
\# [SwitchB-luser-network-dot1x] password simple 123456 \# 配置授权 VLAN 为 VLAN 4。
[SwitchB-luser-network-dot1x] authorization-attribute vlan 4 [SwitchB-luser-network-dot1x] quit配置 客户端的 地址为 10.1.1.2，共享密钥为明文 expert。
\# RADIUS IP [SwitchB] radius-server client ip 10.1.1.2 key simple expert \# 激活当前配置的 RADIUS 客户端和 RADIUS 用户。
[SwitchB] radius-server activate验证配置
4.
• 若使用 Windows XP 的 802.1X 客户端，则需要正确设置此连接的网络属性：在网络属性的“验证”页签中，确保选中“启用此网络的 IEEE 802.1x 验证”，并选择要用于此连接的 EAP 认证类型为“MD5-质询”。
若使用 客户端，则无需启用任何高级认证选项。
• iNode 802.1X保证用户在通过认证后，能够及时更新客户端 地址与授权 中的资源互通。
• IP VLAN \# 以上配置完成后，可以在 Switch B 上查看到所有处于激活状态的 RADIUS 客户端信息以及RADIUS 用户信息。
[SwitchB] display radius-server active-client Total 1 RADIUS clients.
Client IP: 10.1.1.2 [SwitchB] display radius-server active-user dot1x Total 1 RADIUS users matched.
Username: dot1x Description: Not configured Authorization attributes:
VLAN ID: 4 ACL number: Not configured Validity period:
Expiration time: Not configured
802.1X 用户使用用户名 dot1x 和密码 123456 成功通过认证后，Switch B 将向该用户所在端口授权下发 4。在 上使用命令 可以查看到上线用户的连接情VLAN Switch A display dot1x connection况。

###### 3. 处理过程

###### 1. 故障现象

#### 1.17 AAA常见故障处理

##### 1.17.1 RADIUS认证/授权失败

###### 1. 故障现象

用户认证/授权总是失败。

###### 2. 故障分析

(1) 设备与 RADIUS 服务器之间存在通信故障。
(2) 用户名不是“userid@isp-name”的形式，或设备上没有正确配置用于认证该用户的 ISP
域。
(3) RADIUS 服务器的数据库中没有配置该用户。
(4) 用户侧输入的密码不正确。
(5) RADIUS 服务器和设备的报文共享密钥不同。
处理过程
3.
(1) 使用 ping 命令检查设备与 RADIUS 服务器是否可达。
(2) 使用正确形式的用户名或在设备上确保正确配置了用于该用户认证的 ISP 域。
(3) 检查 RADIUS 服务器的数据库以保证该用户的配置信息确实存在。
(4) 确保接入用户输入正确的密码。
(5) 检查两端的共享密钥，并确保两端一致。

##### 1.17.2 RADIUS报文传送失败

故障现象
1.
RADIUS 报文无法传送到 RADIUS 服务器。

###### 2. 故障分析

(1) 设备与 RADIUS 服务器之间的通信存在故障。
(2) 设备上没有设置相应的 RADIUS 服务器 IP 地址。
(3) 认证/授权和计费服务的 UDP 端口设置不正确。
(4) RADIUS 服务器的认证 / 授权和计费端口被其它应用程序占用。

###### 3. 处理过程

(1) 确保线路通畅。
(2) 确保正确设置 RADIUS 服务器的 IP 地址。
(3) 确保与 RADIUS 服务器提供服务的端口号一致。
(4) 确保 RADIUS 服务器上的认证/授权和计费端口可用。

##### 1.17.3 RADIUS计费功能异常

###### 1. 故障现象

用户认证通过并获得授权，但是计费功能出现异常。

###### 2. 故障分析

###### 2. 故障分析

(1) 计费端口号设置不正确。
(2) 计费服务器和认证服务器不是同一台机器，设备却要求认证和计费功能属于同一个服务器（IP
地址相同）。

###### 3. 处理过程

正确设置 计费端口号。
(1) RADIUS
(2) 确保设备的认证服务器和计费服务器的设置与实际情况相同。

##### 1.17.4 HWTACACS常见配置错误

HWTACACS 的常见配置错误与 RADIUS 基本相似，可以参考以上内容。

##### 1.17.5 LDAP认证失败

###### 1. 故障现象

用户认证失败。
故障分析
2.
(1) 设备与 LDAP 服务器之间存在通信故障。
(2) 配置的认证/授权服务器 IP 地址或端口号不正确。
(3) 用户名不是“userid@isp-name”的形式，或设备上没有正确配置用于认证该用户的 ISP域。
(4) LDAP 服务器目录中没有配置该用户。
(5) 用户输入的密码不正确。
(6) 具有管理员权限的用户 DN 或密码没有配置。
(7) 设备上配置的用户参数（如用户名属性）与服务器上的配置不对应。
(8) 认证操作时，没有配置 LDAP 方案用户查询的起始 DN。

###### 3. 处理过程

(1) 使用 ping 命令检查设备与 LDAP 服务器是否可达。
(2) 确保配置的认证服务器 IP 地址与端口号与 LDAP 服务器实际使用的 IP 地址和端口号相符。
(3) 使用正确形式的用户名或在设备上确保正确配置了用于该用户认证的 ISP 域。
(4) 检查 LDAP 服务器目录以保证该用户的配置信息确实存在。
(5) 确保输入用户密码正确。
(6) 确保配置了正确的管理员用户 DN 和密码。
(7) 确保设备上的用户参数（如用户名属性）配置与 LDAP 服务器上的配置相同。
(8) 认证操作时，确保配置了用户查询的起始 DN。

#### 1.18 附录

##### 1.18.1 附录A 常见RADIUS标准属性列表

标准的RADIUS属性由RFC 2865、RFC 2866、RFC 2867 和RFC 2868 所定义。常见的RADIUS标准属性如 表 1-11 所示。
表1-11 常见 RADIUS 标准属性列表

|  | 属性编号 |  |  | 属性名称 |  |  | 属性编号 |  |  | 属性名称 |  |
|---|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  | User-Name |  |  | 45 |  |  |  |  |  |
|  |  |  | User-Password |  |  | 46 |  |  |  |  |  |
|  |  |  | CHAP-Password |  |  | 47 |  |  |  |  |  |
|  |  |  | NAS-IP-Address |  |  | 48 |  |  |  |  |  |
|  |  |  | NAS-Port |  |  | 49 |  |  |  |  |  |
|  |  |  | Service-Type |  |  | 50 |  |  |  |  |  |
|  |  |  | Framed-Protocol |  |  | 51 |  |  |  |  |  |
|  |  |  | Framed-IP-Address |  |  | 52 |  |  |  |  |  |
|  |  |  | Framed-IP-Netmask |  |  | 53 |  |  |  |  |  |
|  |  |  | Framed-Routing |  |  | 54 |  |  |  |  |  |
|  |  |  | Filter-ID |  |  | 55 |  |  |  |  |  |
|  |  |  | Framed-MTU |  |  | 56-59 |  |  |  |  |  |
|  |  |  | Framed-Compression |  |  | 60 |  |  |  |  |  |
|  |  |  | Login-IP-Host |  |  | 61 |  |  |  |  |  |
|  |  |  | Login-Service |  |  | 62 |  |  |  |  |  |
|  |  |  | Login-TCP-Port |  |  | 63 |  |  |  |  |  |
|  |  |  | (unassigned) |  |  | 64 |  |  |  |  |  |
|  |  |  | Reply-Message |  |  | 65 |  |  |  |  |  |
|  |  |  | Callback-Number |  |  | 66 |  |  |  |  |  |
|  |  |  | Callback-ID |  |  | 67 |  |  |  |  |  |
|  |  |  | (unassigned) |  |  | 68 |  |  |  |  |  |
|  |  |  | Framed-Route |  |  | 69 |  |  |  |  |  |
|  |  |  | Framed-IPX-Network |  |  | 70 |  |  |  |  |  |
|  |  |  | State |  |  | 71 |  |  |  |  |  |
|  |  |  | Class |  |  | 72 |  |  |  |  |  |
|  |  |  | Vendor-Specific |  |  | 73 |  |  |  |  |  |
|  |  |  | Session-Timeout |  |  | 74 |  |  |  |  |  |
|  |  |  | Idle-Timeout |  |  | 75 |  |  |  |  |  |
|  |  |  | Termination-Action |  |  | 76 |  |  |  |  |  |

|  | 属性编号 |  |  | 属性名称 |  |  | 属性编号 |  |  | 属性名称 |  |
|---|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  | Called-Station-Id |  |  | 77 |  |  |  |  |  |
|  |  |  | Calling-Station-Id |  |  | 78 |  |  |  |  |  |
|  |  |  | NAS-Identifier |  |  | 79 |  |  |  |  |  |
|  |  |  | Proxy-State |  |  | 80 |  |  |  |  |  |
|  |  |  | Login-LAT-Service |  |  | 81 |  |  |  |  |  |
|  |  |  | Login-LAT-Node |  |  | 82 |  |  |  |  |  |
|  |  |  | Login-LAT-Group |  |  | 83 |  |  |  |  |  |
|  |  |  | Framed-AppleTalk-Link |  |  | 84 |  |  |  |  |  |
|  |  |  | Framed-AppleTalk-Network |  |  | 85 |  |  |  |  |  |
|  |  |  | Framed-AppleTalk-Zone |  |  | 86 |  |  |  |  |  |
|  |  |  | Acct-Status-Type |  |  | 87 |  |  |  |  |  |
|  |  |  | Acct-Delay-Time |  |  | 88 |  |  |  |  |  |
|  |  |  | Acct-Input-Octets |  |  | 89 |  |  |  |  |  |
|  |  |  | Acct-Output-Octets |  |  | 90 |  |  |  |  |  |
|  |  |  | Acct-Session-Id |  |  | 91 |  |  |  |  |  |

##### 1.18.2 附录B 常见RADIUS标准属性描述

表1-12 常见 标准属性描述RADIUS

|  | 属性 |  | 属性名称 | 描述 |
|---|---|---|---|---|
|  | 编号 |  |  |  |
|  |  |  | User-Name |  |
|  |  |  | User-Password |  |
|  |  |  | CHAP-Password |  |
|  |  |  | NAS-IP-Address |  |
|  |  |  | NAS-Port |  |
|  |  |  | Service-Type |  |
|  |  |  | Framed-Protocol |  |
|  |  |  | Framed-IP-Address |  |
|  |  |  | Filter-ID |  |

|  | 属性 |  | 属性名称 | 描述 |
|---|---|---|---|---|
|  | 编号 |  |  |  |
|  |  |  | Framed-MTU |  |
|  |  |  | Login-IP-Host |  |
|  |  |  | Login-Service |  |
|  |  |  | Reply-Message |  |
|  |  |  | Vendor-Specific |  |
|  |  |  | Session-Timeout |  |
|  |  |  | Idle-Timeout |  |
|  |  |  | Calling-Station-Id |  |
|  |  |  | NAS-Identifier |  |
|  |  |  | Acct-Status-Type |  |
|  |  |  | Acct-Authentic |  |
|  |  |  | CHAP-Challenge |  |
|  |  |  | NAS-Port-Type |  |
|  |  |  | Tunnel-Type |  |
|  |  |  | Tunnel-Medium-Type |  |
|  |  |  | EAP-Message |  |

|  | 属性 |  | 属性名称 | 描述 |
|---|---|---|---|---|
|  | 编号 |  |  |  |
|  |  |  | Message-Authenticator |  |
|  |  |  | Tunnel-Private-Group-I D |  |
|  |  |  | NAS-Port-Id |  |
|  |  |  | Framed-IPv6-Address |  |

##### 1.18.3 附录C RADIUS扩展属性（Vendor-ID=25506）

表 1-13 列出的RADIUS扩展属性为所有产品可支持属性的合集，具体产品支持情况有所不同。
表1-13 RADIUS 扩展属性（Vendor-ID=25506）

|  | 子属性 |  | 子属性名称 | 描述 |
|---|---|---|---|---|
|  | 编号 |  |  |  |
|  |  |  | Input-Peak-Rate |  |
|  |  |  | Input-Average-Rate |  |
|  |  |  | Input-Basic-Rate |  |
|  |  |  | Output-Peak-Rate |  |
|  |  |  | Output-Average-Rate |  |
|  |  |  | Output-Basic-Rate |  |
|  |  |  | Remanent_Volume |  |
|  |  |  | ISP-ID |  |
|  |  |  | Command |  |
|  |  |  | Result_Code |  |
|  |  |  | Connect_ID |  |
|  |  |  | PortalURL |  |
|  |  |  | Ftp_Directory |  |
|  |  |  | Exec_Privilege |  |

|  | 子属性 |  | 子属性名称 | 描述 |
|---|---|---|---|---|
|  | 编号 |  |  |  |
|  |  |  | NAT-IP-Address |  |
|  |  |  | NAT-Start-Port |  |
|  |  |  | NAT-End-Port |  |
|  |  |  | NAS_Startup_Timestam p |  |
|  |  |  | Ip_Host_Addr |  |
|  |  |  | User_Notify |  |
|  |  |  | User_HeartBeat |  |
|  |  |  | Multicast_Receive_Grou p |  |
|  |  |  | IP6_Multicast_Receive_ Group |  |
|  |  |  | MLD-Access-Limit |  |
|  |  |  | local-name |  |
|  |  |  | IGMP-Access-Limit |  |
|  |  |  | VPN-Instance |  |
|  |  |  | ANCP-Profile |  |
|  |  |  | Client-Primary-DNS |  |
|  |  |  | Client-Secondary-DNS |  |
|  |  |  | User_Group |  |
|  |  |  | Acct_IPv6_Input_Octets |  |
|  |  |  | Acct_IPv6_Output_Octet s |  |
|  |  |  | Acct_IPv6_Input_Packet s |  |
|  |  |  | Acct_IPv6_Output_Pack ets |  |
|  |  |  | Acct_IPv6_Input_Gigaw ords |  |
|  |  |  | Acct_IPv6_Output_Giga words |  |
|  |  |  | User-Roles |  |

|  | 子属性 |  | 子属性名称 | 描述 |
|---|---|---|---|---|
|  | 编号 |  |  |  |
|  |  |  | Av-Pair |  |
|  |  |  | Accounting-Level |  |
|  |  |  | Ita-Policy |  |
|  |  |  | NAS-Port-Name |  |
|  |  |  | Auth_Detail_Result |  |
|  |  |  | Input-Committed-Burst-S ize |  |
|  |  |  | Output-Committed-Burst- Size |  |

|  | 子属性 |  | 子属性名称 | 描述 |
|---|---|---|---|---|
|  | 编号 |  |  |  |
|  |  |  | authentication-type |  |
|  |  |  | WEB-URL |  |
|  |  |  | Subscriber-ID |  |
|  |  |  | Subscriber-Profile |  |
|  |  |  | Product_ID |  |

## 02-802.1X配置

目 录协议简介的接入控制方式支持 下发重认证配置端口的授权状态

配置 802.1X静默功能配置配置配置在线用户握手功能配置 接入用户日志信息功能支持 快速部署典型配置举例（ 服务器组网）

### 1 802.1X概述

#### 1.1 802.1X协议简介

802.1X 协议是一种基于端口的网络接入控制协议，即在局域网接入设备的端口上对所接入的用户和
设备进行认证，以便控制用户设备对网络资源的访问。

##### 1.1.1 802.1X的体系结构

802.1X系统中包括三个实体：客户端（Client）、设备端（Device）和认证服务器（Authentication
server），如 图 1-1 所示。
图1-1 802.1X 体系结构图
客户端是请求接入局域网的用户终端，由局域网中的设备端对其进行认证。客户端上必须安装
•
支持 802.1X 认证的客户端软件。
• 设备端是局域网中控制客户端接入的网络设备，位于客户端和认证服务器之间，为客户端提供
接入局域网的端口（物理端口或逻辑端口），并通过与认证服务器的交互来对所连接的客户端
进行认证。
认证服务器用于对客户端进行认证、授权和计费，通常为 RADIUS（Remote Authentication
•
Service，远程认证拨号用户服务）服务器。认证服务器根据设备端发送来的客户
Dial-In User
端认证信息来验证客户端的合法性，并将验证结果通知给设备端，由设备端决定是否允许客户
端接入。在一些规模较小的网络环境中，认证服务器的角色也可以由设备端来代替，即由设备
端对客户端进行本地认证、授权和计费。

##### 1.1.2 802.1X对端口的控制

设备端为客户端提供的接入局域网的端口被划分为两个逻辑端口：受控端口和非受控端口。任何到达该端口的帧，在受控端口与非受控端口上均可见。
• 非受控端口：始终处于双向连通状态，主要用来传递认证报文，保证客户端始终能够发出或接收认证报文。
受控端口：设备端利用认证服务器对需要接入局域网的客户端进行认证，并根据认证结果
•（ Accept 或 Reject ）对受控端口的授权状态进行相应地控制。
客户端认证成功，受控端口处于授权状态。该状态下端口双向连通，用于传递业务报文。
(cid:123)
客户端认证失败，受控端口处于非授权状态。该状态下，又可以分为两种情况：
(cid:123)
双向受控状态：禁止帧的发送和接收；
−

###### 1. EAP中继

###### 2. EAP终结

单向受控状态时：禁止从客户端接收帧，但允许向客户端发送帧。目前，设备上的受控−端口只能处于单向受控状态。
图1-2 受控端口上授权状态的影响

##### 1.1.3 802.1X认证报文的交互机制

802.1X 系统使用 EAP（Extensible Authentication Protocol，可扩展认证协议）来实现客户端、设
备端和认证服务器之间认证信息的交互。EAP 是一种 模式的认证框架，它可以支持多种认证方
C/S
法，例如 MD5-Challenge、EAP-TLS（Extensible Authentication Protocol -Transport Layer Security，
可扩展认证协议-传输层安全）、PEAP（Protected Extensible Authentication Protocol，受保护的扩
展认证协议）等。在客户端与设备端之间，EAP 报文使用 EAPOL（Extensible Authentication Protocol
LAN，局域网上的可扩展认证协议）封装格式承载于数据帧中传递。在设备端与 服务
over RADIUS
器之间，EAP 报文的交互有 EAP 中继和 EAP 终结两种处理机制。
EAP中继
1.
设备端对收到的 EAP 报文进行中继，使用 EAPOR（EAP over RADIUS）封装格式将其承载于
RADIUS 报文中发送给 RADIUS 服务器。
图1-3 EAP 中继原理示意图
该处理机制下，EAP 认证过程在客户端和 服务器之间进行。RADIUS 服务器作为 服
RADIUS EAP
务器来处理客户端的 EAP 认证请求，设备相当于一个中继，仅对 EAP 报文做中转。
终结
2. EAP
设备对 EAP 认证过程进行终结，将收到的 EAP 报文中的客户端认证信息封装在标准的 RADIUS 报
文中，与服务器之间采用 PAP（Password Protocol，密码认证协议）或
Authentication CHAP
（Challenge Handshake Authentication Protocol，质询握手认证协议）方法进行认证。

图1-4 EAP 终结原理示意图

###### 3. EAP中继与EAP终结的对比

表1-1 EAP 中继与 EAP 终结的对比

| 报文交互方式 |  | 优势 |  |  | 局限性 |  |
|---|---|---|---|---|---|---|
|  |  | • 支持多种 EAP 认证方法 • 设备端的配置和处理流程简单 |  |  |  |  |
|  |  | 对RADIUS服务器无特殊要求，支持PAP 认证和CHAP认证即可 |  |  |  |  |

##### 1.1.4 报文格式

###### 1. EAP

EAP报文格式如 图 所示。
1-5图1-5 EAP 报文格式0 7 15

| Code | Identifier |
|---|---|
| Length |  |
| Data |  |

N
• Code：EAP 报文的类型，包括 Request（1）、Response（2）、Success（3）和 Failure
（4）。
• Identifier：用于匹配 Request 消息和 Response 消息的标识符。
• Length：EAP 报文的长度，包含 Code、Identifier、Length 和 Data 域，单位为字节。
• Data：EAP 报文的内容，该字段仅在 EAP 报文的类型为 Request 和 Response 时存在，它由类型域和类型数据两部分组成，例如，类型域为 表示 类型，类型域为 表示1 Identity 4 MD5 challenge 类型。

###### 2. EAPOL

EAPOL是 802.1X协议定义的一种承载EAP报文的封装技术，主要用于在局域网中传送客户端和设备端之间的EAP协议报文。EAPOL数据包的格式如 图 1-6 所示。
图1-6 EAPOL 数据包格式0 7 15

| PAE Ethernet Type |  |
|---|---|
| Protocol Version | Type |
| Length |  |
| Packet Body |  |

N
• PAE Ethernet Type：表示协议类型。EAPOL 的协议类型为 0x888E。
• Protocol Version：表示 EAPOL 数据帧的发送方所支持的 EAPOL 协议版本号。
• Type：表示EAPOL数据帧类型。目前设备上支持的EAPOL数据帧类型见 表 1-2。
表1-2 数据帧类型EAPOL

|  | 类型值 |  |  | 数据帧类型 |  |  | 说明 |  |
|---|---|---|---|---|---|---|---|---|
|  |  |  | EAP-Packet |  |  |  |  |  |
|  |  |  | EAPOL-Start |  |  |  |  |  |
|  |  |  | EAPOL-Logoff |  |  |  |  |  |

• Length：表示数据域的长度，也就是Packet Body字段的长度，单位为字节。当 EAPOL数据
帧的类型为 EAPOL-Start 或 EAPOL-Logoff 时，该字段值为 0，表示后面没有 Packet Body
字段。
Body：数据域的内容。
• Packet

###### 3. EAP报文在RADIUS中的封装

RADIUS 为支持 EAP 认证增加了两个属性：EAP-Message（EAP 消息）和 Message-Authenticator（消息认证码）。在含有 EAP-Message 属性的数据包中，必须同时包含 Message-Authenticator 属性。关于 RADIUS 报文格式的介绍请参见“安全配置指导”中的“AAA”的 RADIUS 协议简介部分。
• EAP-Message如 图 1-7 所示，EAP-Message属性用来封装EAP报文，Value域最长 253 字节，如果EAP报文长度大于 253 字节，可以对其进行分片，依次封装在多个EAP-Message属性中。

图1-7 EAP-Message 属性封装
• Message-Authenticator如图1-8所示，Message-Authenticator属性用于在EAP认证过程中验证携带了EAP-Message属性的RADIUS报文的完整性，避免报文被篡改。如果接收端对接收到的RADIUS报文计算出的完整性校验值与报文中携带的Message-Authenticator属性的Value值不一致，该报文会被认为无效而丢弃。
图1-8 属性封装Message-Authenticator

##### 1.1.5 802.1X的认证过程

设备端支持采用 EAP 中继方式或 EAP 终结方式与远端 RADIUS 服务器交互。以下关于 802.1X 认证过程的描述，都以客户端主动发起认证为例。

###### 1. EAP中继方式

这种方式是 标准规定的，将 承载在其它高层协议中，如 RADIUS，以IEEE 802.1X EAP EAP over便 EAP 报文穿越复杂的网络到达认证服务器。一般来说，需要 RADIUS 服务器支持 EAP 属性：
EAP-Message 和 Message-Authenticator。
如 图 1-9 所示，以MD5-Challenge类型的EAP认证为例，具体认证过程如下。

图1-9 IEEE 802.1X 认证系统的 EAP 中继方式认证流程Client Device Authentication server EAPOL EAPOR
(1) EAPOL-Start
(2) EAP-Request/Identity

| (3) EAP-Response/Identity (6) EAP-Request/MD5 challenge |
|---|
| (7) EAP-Response/MD5 challenge (10) EAP-Success |
| Port au (11) EAP-Request/Identity |
| (12) EAP-Response/Identity ... (13) EAPOL-Logoff Port un (14) EAP-Failure |

(4) RADIUS Access-Request
(EAP-Response/Identity)
(5) RADIUS Access-Challenge
(EAP-Request/MD5 challenge)
(8) RADIUS Access-Request
(EAP-Response/MD5 challenge)
(9) RADIUS Access-Accept
(EAP-Success)
authorized
unauthorized
(1) 当用户需要访问外部网络时打开 802.1X 客户端程序，输入用户名和密码，发起连接请求。此
时，客户端程序将向设备端发出认证请求帧（EAPOL-Start），开始启动一次认证过程。
(2) 设备端收到认证请求帧后，将发出一个 Identity 类型的请求帧（EAP-Request/Identity）要求
用户的客户端程序发送输入的用户名。
客户端程序响应设备端发出的请求，将用户名信息通过 类型的响应帧
(3) Identity
（EAP-Response/Identity）发送给设备端。
(4) 设备端将客户端发送的响应帧中的 EAP 报文封装在 RADIUS 报文（RADIUS Access-Request）
中发送给认证服务器进行处理。
(5) RADIUS 服务器收到设备端转发的用户名信息后，将该信息与数据库中的用户名列表对比，
找到该用户名对应的密码信息，用随机生成的一个 MD5 Challenge 对密码进行加密处理，同
时将此 通过 报文发送给设备端。
MD5 Challenge RADIUS Access-Challenge
设备端将 服务器发送的 转发给客户端。
(6) RADIUS MD5 Challenge
客户端收到由设备端传来的 后，用该 对密码进行加密处理，生成
(7) MD5 Challenge Challenge
EAP-Response/MD5 Challenge 报文，并发送给设备端。
(8) 设备端将此 EAP-Response/MD5 Challenge 报文封装在 RADIUS 报文（RADIUS
Access-Request）中发送给 RADIUS 服务器。

(9) RADIUS 服务器将收到的已加密的密码信息和本地经过加密运算后的密码信息进行对比，如果
相同，则认为该用户为合法用户，并向设备端发送认证通过报文（RADIUS Access-Accept）。
设备收到认证通过报文后向客户端发送认证成功帧（EAP-Success），并将端口改为授权状
(10)
态，允许用户通过端口访问网络。
(11) 用户在线期间，设备端会通过向客户端定期发送握手报文的方法，对用户的在线情况进行监测。
(12) 客户端收到握手报文后，向设备发送应答报文，表示用户仍然在线。缺省情况下，若设备端发
送的两次握手请求报文都未得到客户端应答，设备端就会让用户下线，防止用户因为异常原因
下线而设备无法感知。
(13) 客户端可以发送 EAPOL-Logoff 帧给设备端，主动要求下线。
(14) 设备端把端口状态从授权状态改变成未授权状态，并向客户端发送 EAP-Failure 报文。
EAP 中继方式下，需要保证在客户端和 RADIUS 服务器上选择一致的 EAP 认证方法，而在设备上，
只需要通过 dot1x authentication-method eap 命令启动 EAP 中继方式即可。

###### 2. EAP终结方式

这种方式将EAP报文在设备端终结并映射到RADIUS报文中，利用标准RADIUS协议完成认证、授权和计费。设备端与RADIUS服务器之间可以采用PAP或者CHAP认证方法。如 图 所示，以1-10 CHAP认证为例，具体的认证流程如下。

图1-10 IEEE 802.1X 认证系统的 EAP 终结方式认证流程EAP 终结方式与 EAP 中继方式的认证流程相比，不同之处在于用来对用户密码信息进行加密处理的 MD5 challenge 由设备端生成，之后设备端会把用户名、MD5 challenge 和客户端加密后的密码信息一起发送给 RADIUS 服务器，进行相关的认证处理。

##### 1.1.6 802.1X的认证触发方式

的认证过程可以由客户端主动发起，也可以由设备端发起。
802.1X

###### 1. 客户端主动触发方式

• 组播触发：客户端主动向设备端发送 EAPOL-Start 报文来触发认证，该报文目的地址为组播
MAC 地址 01-80-C2-00-00-03。
• 广播触发：客户端主动向设备端发送 EAPOL-Start 报文来触发认证，该报文的目的地址为广
播 MAC 地址。该方式可解决由于网络中有些设备不支持上述的组播报文，而造成设备端无法
收到客户端认证请求的问题。

目前，iNode 的 802.1X 客户端可支持广播触发方式。
•

###### 2. 设备端主动触发方式

设备端主动触发方式用于支持不能主动发送 EAPOL-Start 报文的客户端，例如 Windows XP 自带的
802.1X 客户端。设备主动触发认证的方式分为以下两种：
组播触发：设备每隔一定时间（缺省为 30 秒）主动向客户端组播发送 Identity 类型的
•帧来触发认证。
EAP-Request单播触发：当设备收到源 地址未知的报文时，主动向该 地址单播发送 类
• MAC MAC Identity型的 EAP-Request 帧来触发认证。若设备端在设置的时长内没有收到客户端的响应，则重发该报文。

#### 1.2 802.1X的接入控制方式

设备不仅支持协议所规定的基于端口的接入控制方式（Port-based），还对其进行了扩展、优化，支持基于 MAC 的接入控制方式（MAC-based）。
• 采用基于端口的接入控制方式时，只要该端口下的第一个用户认证成功后，其它接入用户无须认证就可使用网络资源，但是当第一个用户下线后，其它用户也会被拒绝使用网络。
采用基于 MAC 的接入控制方式时，该端口下的所有接入用户均需要单独认证，当某个用户下
•线后，也只有该用户无法使用网络。

#### 1.3 802.1X支持VLAN下发

##### 1.3.1 授权VLAN

用户在通过远程 AAA/本地 认证时，远程 服务器/接入设备可以下发授权 信
802.1X AAA AAA VLAN息给用户的接入端口，但是仅远程 AAA 服务器支持授权携带 Tag 的 VLAN。

###### 1. 远程AAA授权

该方式下，需要在服务器上指定下发给用户的授权 VLAN 信息，下发的授权 VLAN 信息可以有多种形式，包括数字型 和字符型 VLAN，字符型 又可分为 名称、VLAN 组名、携带VLAN VLAN VLAN后缀的 VLAN ID（后缀用于标识是否携带 Tag）。
设备收到服务器的授权 VLAN 信息后，首先对其进行解析，只要解析成功，即以对应的方法下发授权 VLAN；如果解析不成功，则用户认证失败。
• 若认证服务器下发的授权 VLAN 信息为一个 VLAN ID 或一个 VLAN 名称，则仅当对应的 VLAN不为动态学习到的 VLAN、保留 VLAN、Super VLAN 和 Private VLAN 时，该 VLAN 才是有效的授权 VLAN。当认证服务器下发 名称时，对应的 必须为已存在的 VLAN。
VLAN VLAN若认证服务器下发的授权 VLAN 信息为一个 VLAN 组名，则设备首先会通过组名查找该组内
•配置的 VLAN 列表。若查找到授权 VLAN 列表，则在这一组 VLAN 中，除 Super VLAN、动态 VLAN、Private VLAN 之外的所有 VLAN 都有资格被授权给用户。关于 VLAN 组的相关配置，请参见“二层技术-以太网交换配置指导”中的“VLAN”。

若端口接入控制方式为 MAC-based，当端口链路类型为 Hybrid，且使能了 MAC VLAN 功(cid:123)
能时，若端口上已有其他在线用户，则将选择该组 中在线用户数最少的一个VLAN VLAN作为当前认证用户的授权 VLAN（若在线用户数最小的 VLAN 有多个，则选择 VLAN ID 最小者）；当端口链路类型为 Hybrid 但未使能 MAC VLAN 功能、链路类型为 Access 或 Trunk时，若端口上已有其他在线用户，则查看端口上在线用户的授权 是否存在于该组中，VLAN若存在，则将此 VLAN 授权给当前的认证用户，否则认为当前认证用户授权失败，将被强制下线。若当前用户为端口上第一个在线用户，则直接将该组 VLAN 中 ID 最小的 VLAN授权给当前的认证用户。
若接入控制方式为 Port-based，则将该组 VLAN 中 ID 最小的 VLAN 授权给当前的认证用(cid:123)
户，且后续该端口上的认证用户均被加入该授权 VLAN。
若认证服务器下发的授权 信息为一个包含若干 编号以及若干 名称的字符
• VLAN VLAN VLAN串，则设备首先将其解析为一组 VLAN ID，然后采用与解析一个 VLAN 组名相同的解析逻辑选择一个授权 VLAN。
• 若认证服务器下发的授权 VLAN 信息为一个包含若干个“VLAN ID+后缀”形式的字符串，则只有第一个不携带后缀或者携带 untagged 后缀的 VLAN 将被解析为唯一的 untagged 的授权VLAN，其余 都被解析为 的授权 VLAN。例如服务器下发字符串“1u 3”，其VLAN tagged 2t中的 u和 t 均为后缀，分别表示 untagged 和 tagged。该字符串被解析之后，VLAN 1为 untagged的授权 VLAN，VLAN 2 和 VLAN 3 为 tagged 的授权 VLAN。该方式下发的授权 VLAN 仅对端口链路类型为 或 Trunk，且 接入控制方式为 的端口有效。
Hybrid 802.1X Port-based端口的缺省VLAN将被修改为untagged的授权VLAN。若不存在untagged的授权VLAN，(cid:123)
则不修改端口的缺省 VLAN。
端口将允许所有解析成功的授权 通过。
VLAN (cid:123)

###### 2. 本地AAA授权

该方式下，可以通过配置本地用户的授权属性指定下发给用户的授权 VLAN 信息，且只能指定一个授权 VLAN。设备将此 VLAN 作为该本地用户的授权 VLAN。关于本地用户的相关配置，请参考“安全配置指导”中的“AAA”。

###### 3. 不同类型的端口加入授权VLAN

无论是远程AAA授权，还是本地AAA授权，除了认证服务器下发“VLAN ID+后缀”形式的字符串之外，其它情况下设备均会根据用户认证上线的端口链路类型，按照 表 1-3 将端口加入指定的授权VLAN 中。
表1-3 不同类型的端口加入授权 VLAN

|  | 接入控制方式 |  |  | Access 端口 |  |  | Trunk 端口 |  |  | Hybrid 端口 |  |
|---|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  | • 不支持下发带 Tag 的 VLAN • 加入授权 VLAN • 缺省 VLAN 修改为授权 VLAN |  |  | • 允许授权 VLAN 通过 • 授权 VLAN 未携带 Tag 的情况下，缺省 VLAN 修改为授权 VLAN；授权 VLAN 携带 Tag 的情况下，不会修改该端口的缺省 VLAN |  |  |  |  |  |

|  | 接入控制方式 |  |  | Access 端口 |  |  | Trunk 端口 |  |  | Hybrid 端口 |  |
|---|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  | • 不支持下发带 Tag 的 VLAN • 加入第一个通过认证的用户的授权 VLAN • 缺省 VLAN 修改为第一个通过认证的用户的授权 VLAN |  |  | • 允许授权 VLAN 通过 • 授权 VLAN 未携带 Tag 的情况下，缺省 VLAN 修改为第一个通过认证的用户的授权 VLAN；授权 VLAN 携带 Tag 的情况下，不会修改该端口的缺省 VLAN |  |  |  |  |  |

说明：在授权 VLAN 未携带 Tag 的情况下，只有开启了 MAC VLAN 功能的端口上才允许给不同的用户MAC授权不同的VLAN。如果没有开启MAC VLAN功能，授权给所有用户的VLAN必须相同，否则仅第一个通过认证的用户可以成功上线。
在授权VLAN携带Tag的情况下，无论是否开启了MAC VLAN功能，设备都会给不同的用户授权不同的VLAN，一个VLAN只能授权给一个用户。
授权 VLAN 并不影响端口的配置。但是，授权 VLAN 的优先级高于端口用户配置的 VLAN，即通过认证后起作用的 是授权 VLAN，用户配置的端口配置的 在用户下线后生效。
VLAN VLAN对于 Hybrid 端口，如果认证用户的报文携带 VLAN Tag，则应通过 port hybrid vlan 命令
•配置该端口在转发指定的 VLAN报文时携带 Tag；如果认证用户的报文不携带 Tag，VLAN VLAN则应配置该端口在转发指定的 VLAN 报文时不携带 VLAN Tag。否则，当服务器没有授权下发VLAN 时，用户虽然可以通过认证但不能访问网络。
• 对于 Hybrid 端口，不建议把将要下发或已经下发的授权 VLAN 配置为携带 Tag的方式加入端口。
• 在启动了 802.1X 周期性重认证功能的 Hybrid 端口上，若用户在 MAC VLAN 功能开启之前上线，则 MAC VLAN 功能不能对该用户生效，即系统不会根据服务器下发的 VLAN 生成该用户的 MAC VLAN 表项，只有该在线用户重认证成功且服务器下发的 VLAN 发生变化时，MAC VLAN 功能才会对它生效。MAC VLAN 功能的详细介绍请参见“二层技术-以太网交换配置指导”中的“VLAN”。

##### 1.3.2 802.1X Guest VLAN

802.1X Guest VLAN 功能允许用户在未认证的情况下，访问某一特定 VLAN 中的资源。这个特定的
VLAN 称之为 Guest VLAN，该 VLAN 内通常放置一些用于用户下载客户端软件或其他升级程序的
服务器。
根据端口的接入控制方式不同，Guest VLAN 的生效情况有所不同。

###### 1. Port-based方式

在接入控制方式为Port-based的端口上配置Guest VLAN后，若全局和端口上都使能了 802.1X，端口授权状态为auto，且端口处于激活状态，则该端口就被加入Guest VLAN，所有在该端口接入的用户将被授权访问Guest VLAN里的资源。端口加入Guest VLAN的情况与加入授权VLAN相同，与端口链路类型有关，请参见“1.3.1 授权VLAN”的“表 1-3”。需要注意的是，端口接收的带VLAN Tag的报文，如果该VLAN不是配置的Guest VLAN，则报文仍然可以在该VLAN内转发。
当端口上处于Guest VLAN中的用户发起认证且失败时：如果端口配置了Auth-Fail VLAN，则该端口会被加入Auth-Fail VLAN；如果端口未配置Auth-Fail VLAN，则该端口仍然处于Guest VLAN内。
关于Auth-Fail VLAN的具体介绍请参见“1.3.3 VLAN”。
802.1X Auth-Fail当端口上处于 中的用户发起认证且成功时，端口会离开 VLAN，之后端口加入Guest VLAN Guest VLAN 情况与认证服务器是否下发 VLAN 有关，具体如下：
• 若认证服务器下发 VLAN，则端口加入下发的 VLAN 中。
• 若认证服务器未下发 VLAN，则端口回到初始 VLAN 中。
用户下线后，端口加入 Guest VLAN。

###### 2. MAC-based方式

在接入控制方式为 MAC-based 的端口上配置 Guest VLAN 后，端口上未认证的用户将被授权访问Guest VLAN 里的资源。
当端口上处于 Guest VLAN 中的用户发起认证且失败时，如果端口配置了 Auth-Fail VLAN，则认证失败的用户将被加入 VLAN；如果端口未配置 VLAN，则该用户将离开Auth-Fail Auth-Fail Guest VLAN，回到加入 Guest VLAN 之前端口所在的初始 VLAN。
当端口上处于 Guest VLAN 中的用户发起认证且成功时，设备会根据认证服务器是否下发授权VLAN 决定将该用户加入到下发的授权 VLAN 中，或使其回到加入 Guest VLAN 之前端口所在的初始 VLAN。

##### 1.3.3 802.1X Auth-Fail VLAN

802.1X Auth-Fail VLAN 功能允许用户在认证失败的情况下访问某一特定 VLAN 中的资源，这个
称之为 VLAN。需要注意的是，这里的认证失败是认证服务器因某种原因明确拒绝
VLAN Auth-Fail
用户认证通过，比如用户密码错误，而不是认证超时或网络连接等原因造成的认证失败。
根据端口的接入控制方式不同， Auth-Fail VLAN 的生效情况有所不同。

###### 1. Port-based方式

在接入控制方式为Port-based的端口上配置Auth-Fail VLAN后，若该端口上有用户认证失败，则该端口会离开当前的VLAN 被加入到Auth-Fail VLAN ，所有在该端口接入的用户将被授权访问VLAN里的资源。端口加入Auth-Fail VLAN的情况与加入授权VLAN相同，与端口链路类型Auth-Fail有关，请参见“1.3.1 授权VLAN”的“表 1-3”。
当加入 Auth-Fail VLAN 的端口上有用户发起认证并失败，则该端口将会仍然处于 Auth-Fail VLAN内；如果认证成功，则该端口会离开 Auth-Fail VLAN，之后端口加入 VLAN 情况与认证服务器是否下发授权 VLAN 有关，具体如下：
• 若认证服务器下发了授权 VLAN，则端口加入下发的授权 VLAN 中。
• 若认证服务器未下发授权 VLAN，则端口回到缺省 VLAN 中。
用户下线后，若端口上配置了 Guest VLAN ，则加入 Guest VLAN ，否则加入缺省 VLAN 。

###### 2. MAC-based方式

在接入控制方式为 MAC-based 的端口上配置 Auth-Fail VLAN 后，该端口上认证失败的用户将被授权访问 Auth-Fail VLAN 里的资源。
当 Auth-Fail VLAN 中的用户再次发起认证时，如果认证成功，则设备会根据认证服务器是否下发决定将该用户加入到下发的授权 中，或使其回到端口的缺省 中；如果认证失败，VLAN VLAN VLAN则该用户仍然留在该 Auth-Fail VLAN 中。

##### 1.3.4 802.1X Critical VLAN

802.1X Critical VLAN 功能允许用户在认证时，当所有认证服务器都不可达的情况下访问某一特定
VLAN 中的资源，这个 VLAN 称之为 Critical VLAN。目前，只采用 RADIUS 认证方式的情况下，在
所有 RADIUS 认证服务器都不可达后，端口才会加入 Critical VLAN。若采用了其它认证方式，则
端口不会加入 VLAN。
Critical
根据端口的接入控制方式不同，Critical 的生效情况有所不同。
VLAN

###### 1. Port-based方式

在接入控制方式为Port-based的端口上配置Critical VLAN后，若该端口上有用户认证时，所有认证服务器都不可达，则该端口会被加入到Critical VLAN，之后所有在该端口接入的用户将被授权访问Critical VLAN里的资源。在用户进行重认证时，若所有认证服务器都不可达，且端口指定在此情况下强制用户下线，则该端口也会被加入到Critical VLAN。端口加入Critical VLAN的情况与加入授权VLAN相同，与端口链路类型有关，请参见“1.3.1 授权VLAN”的“表 1-3”。
已经加入 Critical VLAN 的端口上有用户发起认证时，如果所有认证服务器不可达，则端口仍然在Critical VLAN 内；如果服务器可达且认证失败，且端口配置了 Auth-Fail VLAN，则该端口将会加入Auth-Fail VLAN，否则回到端口的缺省 VLAN 中；如果服务器可达且认证成功，则该端口加入 VLAN的情况与认证服务器是否下发 有关，具体如下：
VLAN若认证服务器下发了授权 VLAN，则端口加入下发的授权 中。
• VLAN若认证服务器未下发授权 VLAN，则端口回缺省 中。
• VLAN用户下线后，若端口上配置了 VLAN，则加入 VLAN，否则加入缺省 VLAN。
Guest Guest

###### 2. MAC-based方式

在接入控制方式为 MAC-based 的端口上配置 Critical VLAN 后，若该端口上有用户认证时，所有认证服务器都不可达，则端口将允许 Critical VLAN 通过，用户将被授权访问 Critical VLAN 里的资源。
当 Critical VLAN 中的用户再次发起认证时，如果所有认证服务器不可达，则用户仍然在 Critical VLAN 中；如果服务器可达且认证失败，且端口配置了 Auth-Fail VLAN，则该用户将会加入 Auth-Fail VLAN，否则回到端口的缺省 中；如果服务器可达且认证成功，则设备会根据认证服务器是VLAN否下发授权 VLAN 决定将该用户加入下发的授权 VLAN 中，或使其回到端口的缺省 VLAN 中。

##### 1.3.5 802.1X Critical Voice VLAN

802.1X Critical Voice VLAN 功能允许语音用户在认证时，当其采用的 ISP 域中的所有认证服务器都
不可达的情况下访问语音 VLAN 中的资源。目前，只采用 RADIUS 认证方式的情况下，在所有
RADIUS 认证服务器都不可达后，端口才会加入 Critical Voice VLAN。若采用了其它认证方式，则
端口不会加入 VLAN。
Critical Voice
根据端口的接入控制方式不同，Critical 的生效情况有所不同。
Voice VLAN

###### 1. Port-based方式

在接入控制方式为 Port-based 的端口上配置 Critical Voice VLAN 后，当发现有认证服务器可达后，处于 Critical Voice VLAN 的端口会主动发送组播报文，触发端口上的客户端进行 802.1X 认证。

###### 2. MAC-based方式

在接入控制方式为 MAC-based的端口上配置 VLAN后，当发现有认证服务器可达后，Critical Voice处于 Critical Voice VLAN 的端口会主动向已加入 Critical Voice VLAN 的 MAC 地址发送单播报文触发其进行 802.1X 认证。

#### 1.4 802.1X支持ACL下发

802.1X 支持 ACL（Access Control List，访问控制列表）下发提供了对上线用户访问网络资源的过
滤与控制功能。当用户上线时，如果 RADIUS 服务器上或接入设备的本地用户视图中指定了要下发
给该用户的授权 ACL，则设备会根据下发的授权 ACL 对用户所在端口的数据流进行过滤，与授权
ACL 规则匹配的流量，将按照规则中指定的 permit 或 deny 动作进行处理。由于服务器上或设备本
地用户视图下指定的是授权 ACL 的编号，因此还需要在设备上创建该 ACL 并配置对应的 ACL 规则。
管理员可以通过改变授权的 ACL 编号或设备上对应的 ACL 规则来改变用户的访问权限。
802.1X 认证可成功授权的 ACL 类型为基本 ACL（ACL 编号为 2000～2999）和高级 ACL（ACL 编
号为 3000～3999）。但当下发的 ACL 不存在、未配置 ACL 规则或 ACL 规则配置了 counting、
established、fragment 或 logging 参数时，授权 ACL 不生效。有关 ACL 规则的具体介绍，请参见
“ACL 和 QoS 命令参考”中的“ACL”。

#### 1.5 802.1X支持User Profile下发

802.1X 支持 User Profile 下发提供了对上线用户访问网络资源的过滤与控制功能。当用户上线时，
如果 服务器上或接入设备的本地用户视图中指定了要下发给该用户的授权 Profile，
RADIUS User
则设备会根据服务器下发的授权 User Profile 对用户所在端口的数据流进行过滤，仅允许 User
Profile 策略中允许的数据流通过该端口。由于服务器上指定的是授权 User Profile 名称，因此还需
要在设备上创建该 并配置该对应的 策略。管理员可以通过改变授权的
User Profile User Profile User
Profile 名称或设备上对应的 User Profile 配置来改变用户的访问权限。

#### 1.6 802.1X支持URL重定向功能

用户采用基于 的接入控制方式时，且端口授权状态为 时，支持 扩展属
802.1X MAC auto RADIUS性下发重定向 URL。802.1X 用户认证后，设备会根据 RADIUS 服务器下发的重定向 URL 属性，将用户的 HTTP 或 HTTPS 请求重定向到指定的 Web 认证页面。Web 认证通过后，RADIUS 服务器记录 802.1X 用户的 MAC 地址，并通过 DM 报文强制 Web 用户下线。此后该用户再次发起 802.1X认证，由于 服务器上已记录该用户和其 地址的对应信息，用户可以成功上线。
RADIUS MAC

802.1X 支持 URL 重定向功能和 EAD 快速部署功能互斥。若需要对 802.1X 用户的 HTTPS 请求进
行重定向，需要在设备上配置对 报文进行重定向的内部侦听端口号，具体配置请参见“三
HTTPS
层技术-IP 业务配置指导”中的“HTTP 重定向”。

#### 1.7 802.1X支持CAR属性下发

802.1X 支持 CAR 属性下发后，设备可以对 802.1X 认证上线用户访问网络资源的流量与速率进行
控制。当用户通过 认证后，如果 服务器通过扩展属性字段下发授权 属性给
802.1X RADIUS CAR
该用户，则设备会根据服务器下发的授权 CAR 属性对用户所在端口的数据流进行限速。RADIUS
扩展属性的详细介绍请参见“安全配置指导”中的“AAA”。
CAR 属性具体分为如下几种：
• Input-Peak-Rate：上行峰值速率，单位 bps。用于限制端口上接收报文的峰值速率。
• Input-Average-Rate：上行平均速率，单位 bps。用于限制该端口上接收报文的平均速率。
• Output-Peak-Rate：下行峰值速率，单位 bps。用于限制端口上发送报文的峰值速率。
• Output-Average-Rate：下行平均速率，单位 bps。用于限制该端口上发送报文的平均速率。
如果未授权 Input-Peak-Rate 或 Output-Peak-Rate，则表示对用户报文进行单速率流量监管，否则
进行双速率流量监管。流量监管的详细介绍请参见“ACL 和 QoS 配置指导”中的“QoS”。

#### 1.8 802.1X重认证

802.1X 重认证是指设备周期性对端口上在线的 802.1X 用户发起重认证，以检测用户连接状态的变
化、确保用户的正常在线，并及时更新服务器下发的授权属性（例如 ACL、VLAN 等）。
认证服务器可以通过下发 RADIUS 属性（session-timeout、Termination-action）来指定用户会话超
时时长以及会话中止的动作类型。认证服务器上如何下发以上 RADIUS 属性的具体配置以及是否可
以下发重认证周期的情况与服务器类型有关，请参考具体的认证服务器实现。
设备作为 服务器，认证服务器作为 客户端时，后者可以通过
RADIUS DAE RADIUS DAE COA
（Change of Authorization）Messages 向用户下发重认证属性，这种情况下，无论设备上是否开
启了周期性重认证功能，端口都会立即对该用户发起重认证。关于 RADIUS DAE 服务器的详细内
容，请参见“安全配置指导”中的“AAA”。
802.1X 用户认证通过后，端口对用户的重认证功能具体实现如下：
当认证服务器下发了用户会话超时时长，且指定的会话中止动作为要求用户进行重认证，则无
•
论设备上是否开启周期性重认证功能，端口都会在用户会话超时时长到达后对该用户发起重认
证。
• 当认证服务器下发了用户会话超时时长，且指定的会话中止动作为要求用户下线时：
若设备上开启了周期性重认证功能，且设备上配置的重认证定时器值小于用户会话超时时
(cid:123)
长，则端口会以重认证定时器的值为周期向该端口在线 802.1X 用户发起重认证；若设备上
配置的重认证定时器值大于等于用户会话超时时长，则端口会在用户会话超时时长到达后
强制该用户下线。

若设备上未开启周期性重认证功能，则端口会在用户会话超时时长到达后强制该用户下线。
(cid:123)
当认证服务器未下发用户会话超时时长时，是否对用户进行重认证，由设备上配置的重认证功
•能决定。
对于已在线的 用户，要等当前重认证周期结束并且认证通过后才会按新配置的周期进
• 802.1X行后续的重认证。
• 端口对用户进行重认证过程中，重认证服务器不可达时端口上的 802.1X 用户状态均由端口上的配置决定。
在用户名不改变的情况下，端口允许重认证前后服务器向该用户下发不同的 VLAN。

#### 1.9 802.1X支持EAD快速部署

EAD（Endpoint Admission Defense，端点准入防御）作为一个网络端点接入控制方案，它通过安全客户端、安全策略服务器、接入设备以及第三方服务器的联动，加强了对用户的集中管理，提升了网络的整体防御能力。但是在实际的应用过程中 EAD 客户端的部署工作量很大，例如，需要网络管理员手动为每一个 客户端下载、升级客户端软件，这在 客户端数目较多的情况下给EAD EAD管理员带来了操作上的不便。
802.1X 认证支持的 EAD 快速部署功能就可以解决以上问题，它允许未通过认证的 802.1X 用户访问一个指定的 IP 地址段（称为 Free IP），并可以将用户发起的 HTTP 或 HTTPS 访问请求重定向到该 地址段中的一个指定的 URL（重定向 URL），实现用户自动下载并安装 客户端的目的。
IP EAD Free IP：未通过认证的 802.1X 终端用户可以访问的 IP 地址段，该 IP 地址段中可以配置一个
•或多个特定服务器，用于提供 EAD 客户端的下载升级或者动态地址分配等服务。
重定向 URL：802.1X 终端用户在认证成功之前，如果使用浏览器访问网络，则设备会将用户
•访问的 URL 重定向到已配置的 URL（例如，重定向到 EAD 客户端下载界面），这样只要用户打开浏览器，就必须进入管理员预设的界面。
EAD 快速部署功能通过制订 EAD 规则（通常为 ACL 规则）来给予未通过认证的终端用户受限制的网络访问权限。当大量用户同时认证时，ACL 资源将迅速被占用，如果没有用户认证成功，将出现ACL 资源不足的情况，会导致一部分新接入的用户无法认证。
管理员可以通过配置 规则的老化时间来控制用户对 资源的占用，当用户访问网络时该定EAD ACL时器开始计时，在定时器超时或者用户下载客户端并成功通过认证之后，该用户所占用的 ACL 资源被删除，在老化时间内未进行任何操作的用户所占用的 ACL 资源会及时得到释放。

### 2 配置802.1X

#### 2.1 802.1X配置限制和指导

• 由于通过配置端口安全特性也可以为用户提供 802.1X 认证服务，且还可以提供 802.1X 和
MAC 地址认证的扩展和组合应用，因此在需要灵活使用以上两种认证方式的组网环境下，推
荐使用端口安全特性。无特殊组网要求的情况下，无线环境中通常使用端口安全特性。在仅需
要 802.1X 特性来完成接入控制的组网环境下，推荐单独使用 802.1X 特性。关于端口安全特
性的详细介绍和具体配置请参见“安全配置指导”中的“端口安全”。
• 当端口上配置的 802.1X 认证的 Guest VLAN、Auth-Fail VLAN、Critical VLAN 中存在用户时，
不允许切换该端口的链路类型。
仅支持在二层以太网接口上配置 802.1X 认证功能，且不支持在二层聚合组的成员端口上开启
•
认证功能。
802.1X

#### 2.2 802.1X配置任务简介

802.1X 配置任务如下：
(1) 开启 802.1X
(2) 配置 802.1X 认证的基本功能
配置 802.1X系统的认证方法
(cid:123)
配置端口的授权状态
(cid:123)
配置端口接入控制方式
(cid:123)
（可选）配置端口的强制认证域
(cid:123)
（可选）配置 802.1X认证超时定时器
(cid:123)
（可选）配置 802.1X重认证功能
(cid:123)
（可选）配置 802.1X静默功能
(cid:123)
(3) （可选）配置 802.1X 下发 VLAN 功能
配置 802.1X Guest VLAN
(cid:123)
配置端口延迟加入 802.1X的Guest VLAN
(cid:123)
配置 802.1X Auth-Fail VLAN
(cid:123)
配置 802.1X Critical VLAN
(cid:123)
配置
802.1X Critical Voice VLAN
(cid:123)
（可选）配置 其它功能
(4) 802.1X
配置认证触发功能
(cid:123)
对于不支持主动发送认证触发报文的客户端，可配置认证触发功能，即设备主动向该端口
上的客户端发送认证请求来触发 802.1X 认证。
配置端口同时接入用户数的最大值
(cid:123)
配置设备向接入用户发送认证请求报文的最大次数
(cid:123)
配置在线用户握手功能
(cid:123)

配置 802.1X支持的域名分隔符(cid:123)
配置端口发送 802.1X协议报文不携带VLAN Tag (cid:123)
配置MAC地址认证成功用户进行 802.1X认证的最大尝试次数(cid:123)
配置 802.1X用户IP地址冻结功能(cid:123)
配置 802.1X认证的MAC地址绑定功能(cid:123)
配置 802.1X支持EAD快速部署(cid:123)
配置 802.1X接入用户日志信息功能(cid:123)

#### 2.3 802.1X配置准备

在配置 802.1X 之前，需要完成以下任务：
• 配置 802.1X 用户所属的 ISP 认证域及其使用的 AAA 方案，即本地认证方案或 RADIUS 方案。
• 如果需要通过 RADIUS 服务器进行认证，则应该在 RADIUS 服务器上配置相应的用户名和密码。
• 如果需要本地认证，则应该在设备上手动添加认证的用户名和密码。配置本地认证时，用户使用的服务类型必须设置为 lan-access。

#### 2.4 开启802.1X

##### 1. 配置限制和指导

只有同时开启全局和端口的 后，802.1X 的配置才能在端口上生效。
802.1X在客户端发送不携带 数据流的情况下，若设备的接入端口配置了 功能，则端口的Tag Voice VLAN
802.1X 功能不生效。关于 Voice VLAN 特性请参见“二层技术-以太网交换配置指导”中的“Voice VLAN”。

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 开启全局的 802.1X 功能。
dot1x
缺省情况下，全局的 802.1X 处于关闭状态。
(3) 进入接口视图。
interface interface-type interface-number
(4) 开启端口的 802.1X 功能。
dot1x
缺省情况下，端口的 802.1X 处于关闭状态。

#### 2.5 配置802.1X系统的认证方法

##### 1. 功能简介

设备上的 802.1X 系统采用的认证方法与设备对于 EAP 报文的处理机制有关，具体如下：

##### 1. 功能简介

若指定 authentication-method 为 eap，则表示设备采用 EAP 中继认证方式。该方式下，
•设备端对客户端发送的 报文进行中继处理，并能支持客户端与 服务器之间所有EAP RADIUS类型的 EAP 认证方法。
• 若指定 authentication-method 为 chap 或 pap，则表示设备采用 EAP 终结认证方式，该方式下，设备端对客户端发送的 EAP 报文进行本地终结，并能支持与 RADIUS 服务器之间采用 或 类型的认证方法。
CHAP PAP

##### 2. 配置限制和指导

• 如果客户端采用了 MD5-Challenge 类型的 EAP 认证，则设备端只能采用 CHAP 认证；如果
iNode 802.1X 客户端采用了“用户名+密码”方式的 EAP 认证，设备上可选择使用 PAP 认证
或 CHAP 认证，从安全性上考虑，通常使用 CHAP 认证。
• 如果采用 EAP 中继认证方式，则设备会把客户端输入的内容直接封装后发给服务器，这种情
况下 命令的设置无效，user-name-format 的介绍请参见“安全命
user-name-format
令参考”中的“AAA”。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置 802.1X 系统的认证方法。
dot1x authentication-method { chap | eap | pap }
缺省情况下，设备启用 EAP 终结方式，并采用 CHAP 认证方法。

#### 2.6 配置端口的授权状态

功能简介
1.
通过配置端口的授权状态，可以控制端口上接入的用户是否需要经过认证来访问网络资源。端口支持以下三种授权状态：
强制授权（authorized-force）：表示端口始终处于授权状态，允许用户不经认证即可访
•问网络资源。
强制非授权（unauthorized-force）：表示端口始终处于非授权状态，不允许用户进行认
•证。设备端不为通过该端口接入的客户端提供认证服务。
• 自动识别（auto）：表示端口初始状态为非授权状态，仅允许 EAPOL 报文收发，不允许用户访问网络资源；如果用户通过认证，则端口切换到授权状态，允许用户访问网络资源。这也是最常用的一种状态。

##### 2. 配置步骤

(1) 进入系统视图。
system-view
进入接口视图。
(2)
interface interface-type interface-number
配置端口的授权状态。
(3)
dot1x port-control { authorized-force | auto | unauthorized-force }

##### 1. 功能简介

##### 2. 配置步骤

##### 1. 功能简介

缺省情况下，端口的授权状态为 auto。

#### 2.7 配置端口接入控制方式

##### 1. 功能简介

设备支持两种端口接入控制方式：基于端口控制（portbased）和基于 MAC 控制（macbased）。

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置端口接入控制方式。
dot1x port-method { macbased | portbased }
缺省情况下，端口采用的接入控制方式为 macbased 。

#### 2.8 配置端口的强制认证域

功能简介
1.
在端口上指定强制认证域为 802.1X 接入提供了一种安全控制策略。所有从该端口接入的 802.1X 用户将被强制使用指定的认证域来进行认证、授权和计费，从而防止用户通过恶意假冒其它域账号从本端口接入网络。另外，管理员也可以通过配置强制认证域对不同端口接入的用户指定不同的认证域，从而增加了管理员部署 802.1X 接入策略的灵活性。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 指定端口上 802.1X 用户使用的强制认证域。
dot1x mandatory-domain domain-name缺省情况下，未指定 802.1X 用户使用的强制认证域。

#### 2.9 配置802.1X认证超时定时器

功能简介
1.
802.1X 认证过程中会启动多个定时器以控制客户端、设备以及 RADIUS 服务器之间进行合理、有序的交互。可配置的 认证定时器包括以下两种：
802.1X客户端认证超时定时器：当设备端向客户端发送了 请求报文后，
• EAP-Request/MD5 Challenge设备端启动此定时器，若在该定时器设置的时长内，设备端没有收到客户端的响应，设备端将重发该报文。

认证服务器超时定时器：当设备端向认证服务器发送了 RADIUS Access-Request 请求报文后，
•设备端启动该定时器，若在该定时器设置的时长内，设备端没有收到认证服务器的响应，则
802.1X 认证失败。

##### 2. 配置限制和指导

一般情况下，无需改变认证超时定时器的值，除非在一些特殊或恶劣的网络环境下，才需要通过命令来调节。例如，用户网络状况比较差的情况下，可以适当地将客户端认证超时定时器值调大一些；
还可以通过调节认证服务器超时定时器的值来适应不同认证服务器的性能差异。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置客户端认证超时定时器。
dot1x timer supp-timeout supp-timeout-value
缺省情况下，客户端认证超时定时器的值为 30 秒。
(3) 配置认证服务器超时定时器。
dot1x timer server-timeout server-timeout-value
缺省情况下，认证服务器超时定时器的值为 秒。
100

#### 2.10 配置802.1X重认证功能

##### 1. 配置限制和指导

• 对 802.1X 用户进行周期性重认证时，设备将按照如下由高到低的顺序为其选择重认证时间间
隔：服务器下发的重认证时间间隔、接口视图下配置的周期性重认证定时器的值、系统视图下
配置的周期性重认证定时器的值、设备缺省的周期性重认证定时器的值。
强制端口上所有 在线用户进行重认证后，不论服务器是否下发重认证或端口下是否开
• 802.1X
启了周期性重认证，强制重认证都会正常执行，端口上的所有在线 802.1X 用户会依次进行重
认证操作。
• 修改设备上配置的认证域或 802.1X 系统认证方法都不会影响在线用户的 802.1X 重认证，只
对配置之后新上线的用户生效。

##### 2. 配置步骤

进入系统视图。
(1)
system-view在系统视图或接口视图下配置周期性重认证定时器。
(2)
系统视图下配置周期性重认证定时器。
(cid:123)
dot1x timer reauth-period reauth-period-value缺省情况下，周期性重认证定时器的值为 3600 秒。
依次执行以下命令在接口视图下配置周期性重认证定时器。
(cid:123)
interface interface-type interface-number dot1x timer reauth-period reauth-period-value quit

缺省情况下，端口上未配置 802.1X 周期性重认证定时器，使用系统视图下的周期性重认证定时器的取值。
进入接口视图。
(3)
interface interface-type interface-number开启周期性重认证功能。
(4)
dot1x re-authenticate缺省情况下，周期性重认证功能处于关闭状态。
(5) （可选）强制端口上所有 802.1X 在线用户进行重认证。
dot1x re-authenticate manual开启本功能后，不论服务器是否下发重认证或端口下是否开启了周期性重认证，强制重认证都会正常执行，端口上的所有在线 用户会依次进行重认证操作。
802.1X（可选）配置重认证服务器不可达时端口上的 用户保持在线状态。
(6) 802.1X dot1x re-authenticate server-unreachable keep-online缺省情况下，端口上的 802.1X 在线用户重认证时，若认证服务器不可达，则会被强制下线。
若配置保持用户在线，当服务器在短时间内恢复可达，则可以避免用户频繁上下线；若处于缺省状态，当服务器可达性在短时间内不可恢复，可避免用户在线状态长时间与实际不符。

#### 2.11 配置802.1X静默功能

##### 1. 功能简介

当 802.1X 用户认证失败以后，设备需要静默一段时间（通过命令 dot1x timer quiet-period设置）后再重新发起认证，在静默期间，设备不对 802.1X 认证失败的用户进行 802.1X 认证处理。

##### 2. 配置限制和指导

在网络处在风险位置，容易受攻击的情况下，可以适当地将静默定时器值调大一些，反之，可以将其调小一些来提高对用户认证请求的响应速度。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 开启静默定时器功能。
dot1x quiet-period
缺省情况下，静默定时器功能处于关闭状态。
(3) （可选）配置静默定时器。
dot1x timer quiet-period quiet-period-value
缺省情况下，静默定时器的值为 60 秒。

#### 2.12 配置802.1X Guest VLAN

##### 1. 配置限制和指导

在接入控制方式为 的端口上生成的 表项会覆盖已生成的阻塞
• MAC-based Guest VLAN MAC表项，但如果端口因检测到非法报文而关闭，则 802.1X Guest VLAN 功能无法生效。关于阻塞 MAC 表项和端口的入侵检测功能的具体介绍请参见“安全配置指导”中的“端口安全”。
• 不同的端口可以指定不同的 802.1X Guest VLAN，一个端口最多只能指定一个 802.1X Guest VLAN 。
• 如果用户端设备发出的是携带 Tag 的数据流，且接入端口上使能了 802.1X 认证并配置了VLAN，为保证各种功能的正常使用，请为 VLAN、端口的缺省 和
802.1X Guest Voice VLAN
802.1X 的 Guest VLAN 分配不同的 VLAN ID。
• 如果某个 VLAN 被指定为 Super VLAN，则该 VLAN 不能被指定为某个端口的 802.1X Guest VLAN；同样，如果某个 VLAN 被指定为某个端口的 802.1X Guest VLAN，则该 VLAN 不能被指定为 Super VLAN。关于 Super VLAN 的详细内容请参见“二层技术-以太网交换配置指导”中的“Super VLAN”。

##### 2. 配置准备

配置 802.1X Guest VLAN 之前，需要进行以下配置准备：
• 创建需要配置为 Guest VLAN 的 VLAN。
• 在接入控制方式为 MAC-based 的端口上，保证端口类型为 Hybrid，端口上的 MAC VLAN 功能处于使能状态，且不建议将指定的 Guest VLAN 修改为携带 Tag 的方式。MAC VLAN 功能的具体配置请参见“二层技术-以太网交换配置指导”中的“VLAN”。

##### 3. 配置步骤

进入系统视图。
(1)
system-view进入接口视图。
(2)
interface interface-type interface-number
(3) 配置端口的 802.1X Guest VLAN。
dot1x guest-vlan guest-vlan-id缺省情况下，端口上未配置 802.1X Guest VLAN 。

#### 2.13 配置端口延迟加入802.1X的Guest VLAN

##### 1. 功能简介

开启 认证，且端口的接入控制方式为 方式时，触发 认证后端口会立即
802.1X MAC-based 802.1X被加入到 802.1X Guest VLAN 中。在这种情况下，如果配置了端口延迟加入 802.1X Guest VLAN功能，端口会主动向触发认证的源 MAC 地址单播发送 EAP-Request 报文。若在指定的时间内（通过命令 dot1x timer tx-period 设置）没有收到客户端的响应，则重发该报文，直到重发次数达到命令 dot1x retry 设置的最大次数时，若仍没有收到客户端的响应，才会加入到 802.1X Guest VLAN 中。

##### 2. 配置准备

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置端口延迟加入 802.1X Guest VLAN 的功能。
dot1x guest-vlan-delay { eapol | new-mac }
缺省情况下，端口延迟加入 802.1X Guest VLAN 的功能处于关闭状态。

#### 2.14 配置802.1X Auth-Fail VLAN

##### 1. 配置限制和指导

• 不同的端口可以指定不同的 802.1X Auth-Fail VLAN，一个端口最多只能指定一个 802.1X
Auth-Fail VLAN 。
如果用户端设备发出的是携带 Tag 的数据流，为保证各种功能的正常使用，请为 Voice VLAN、
•
端口的缺省 和 的 分配不同的 ID。
VLAN 802.1X Auth-Fail VLAN VLAN
如果某个 被指定为 VLAN，则该 不能被指定为某个端口的
• VLAN Super VLAN 802.1X
Auth-Fail VLAN；同样，如果某个 VLAN 被指定为某个端口的 802.1X Auth-Fail VLAN，则该
VLAN 不能被指定为 Super VLAN。关于 Super VLAN 的详细内容请参考“二层技术-以太网
交换配置指导”中的“Super VLAN”。
在接入控制方式为 MAC-based 的端口上同时配置了 802.1X Auth-Fail VLAN 与 MAC 地址认
•
证 时，若用户首先进行 地址认证且失败，则加入 地址认证的
Guest VLAN MAC MAC Guest
VLAN 中，之后若该用户再进行 802.1X 认证且失败，则会离开 MAC 地址认证 Guest VLAN
而加入 802.1X Auth-Fail VLAN 中；若用户首先进行 802.1X 认证且失败，之后除非成功通过
地址认证或者 认证，否则会一直位于 中。
MAC 802.1X 802.1X Auth-Fail VLAN
在接入控制方式为 的端口上生成的 表项会覆盖已生成的阻塞
• MAC-based Auth-Fail VLAN
MAC 表项，但如果端口因检测到非法报文而关闭，则 802.1X 的 Auth-Fail VLAN 功能无法生
效。关于端口入侵检测关闭功能的具体介绍请参考“安全配置指导”中的“端口安全”。
配置准备
2.
配置 802.1X Auth-Fail VLAN 之前，需要进行以下配置准备：
• 创建需要配置为 Auth-Fail VLAN 的 VLAN。
• 在接入控制方式为 MAC-based 的端口上，保证端口类型为 Hybrid，端口上的 MAC VLAN 功
能处于使能状态，且不建议将指定的 Auth-Fail VLAN 修改为携带 Tag 的方式。MAC VLAN 功
能的具体配置请参见“二层技术-以太网交换配置指导”中的“VLAN”。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number

#### 2.15 配置802.1X Critical VLAN

(3) 配置端口的 802.1X Auth-Fail VLAN。
dot1x auth-fail vlan authfail-vlan-id
缺省情况下，端口没有配置 802.1X Auth-Fail VLAN。
配置802.1X
2.15 Critical VLAN

##### 2.15.1 配置端口的802.1X Critical VLAN

###### 1. 配置限制和指导

• 不同的端口可以指定不同的 802.1X Critical VLAN，一个端口最多只能指定一个 802.1X
Critical VLAN。
• 如果用户端设备发出的是携带 Tag 的数据流，为保证各种功能的正常使用，请为 Voice VLAN、
端口的缺省 VLAN 和 802.1X 的 Critical VLAN 分配不同的 VLAN ID。
如果某个 VLAN 被指定为 Super VLAN，则该 VLAN 不能被指定为某个端口的 802.1X Critical
•
；同样，如果某个 被指定为某个端口的 ，则该 不能
VLAN VLAN 802.1X Critical VLAN VLAN
被指定为 Super VLAN。关于 Super VLAN 的详细内容请参考“二层技术-以太网交换配置指
导”中的“Super VLAN”。
• 在接入控制方式为Port-based的端口上，若端口已经处于802.1X Auth-Fail VLAN，则当所有
认证服务器都不可达时，端口并不会离开当前的 VLAN 而加入 802.1X Critical VLAN。在接入
控制方式为 MAC-based 的端口上，当处于 Auth-Fail VLAN 的用户再次发起认证时，如果认
证服务器不可达，则该用户仍然留在该 Auth-Fail VLAN 中，不会离开当前的 VLAN 而加入
802.1X Critical VLAN。
• 若端口已经处于 802.1X Guest VLAN，则当所有认证服务器都不可达时，端口会离开当前的
并加入 VLAN。
VLAN 802.1X Critical

###### 2. 配置准备

配置 802.1X Critical VLAN 之前，需要进行以下配置准备：
• 创建需要配置为 Critical VLAN 的 VLAN。
在接入控制方式为 的端口上，保证端口类型为 Hybrid，端口上的 功
• MAC-based MAC VLAN能处于使能状态，且不建议将指定的 Critical VLAN 修改为携带 Tag 的方式。MAC VLAN 功能的具体配置请参见“二层技术 - 以太网交换配置指导”中的“ VLAN ”。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置端口的 802.1X Critical VLAN。
dot1x critical vlan critical-vlan-id
缺省情况下，端口没有配置 802.1X Critical VLAN。

###### 1. 功能简介

##### 2.15.2 配置向802.1X Critical VLAN用户发送认证成功帧

功能简介
1.
802.1X 用户因认证服务器不可达而被加入 Critical VLAN 之后，设备端会向客户端发送 EAP-Failure报文。对于某些 客户端（如 系统的 客户端），在收到 报文后，
802.1X Windows 802.1X EAP-Failure不会再响应设备端后继发送的 EAP-Request/Identity 报文，从而导致该类用户的 802.1X 重认证无法成功。为解决此问题，设备支持通过命令行配置当 802.1X 用户被加入到 Critical VLAN 后，向客户端发送 EAP-Success 报文。客户端收到该报文后认为 802.1X 用户上线成功，此后可以继续响应设备端发送的 报文进行 重认证。
EAP-Request/Identity 802.1X

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
配置当 用户被加入到 后，设备端向客户端发送 报文。
(3) 802.1X Critical VLAN EAP-Success
dot1x critical eapol
缺省情况下，当 用户加入到 后，设备端向客户端发送 报
802.1X Critical VLAN EAP-Failure
文。

#### 2.16 配置802.1X Critical Voice VLAN

##### 1. 配置限制和指导

• 若端口已经处于 802.1X Auth-Fail VLAN，则当所有认证服务器都不可达时，端口并不会离开
当前的 而加入 VLAN。
VLAN 802.1X Critical Voice
若端口已经处于 VLAN，则当所有认证服务器都不可达时，端口会离开当前的
• 802.1X Guest
VLAN 并加入 802.1X Critical Voice VLAN。

##### 2. 配置准备

配置 802.1X Critical Voice VLAN 之前，需要进行以下配置准备：
• 全局和端口的 LLDP（Link Layer Discovery Protocol，链路层发现协议）已经开启，设备通过LLDP 来判断用户是否为语音用户。有关 LLDP 功能的详细介绍请参考“二层技术-以太网交换配置指导”中的“LLDP”。
端口的语音 VLAN 功能已经开启。有关语音 VLAN 的详细介绍请参考“二层技术-以太网交换
•配置指导”中的“VLAN”。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置端口的 802.1X Critical Voice VLAN。

##### 3. 配置步骤

##### 1. 功能简介

dot1x critical-voice-vlan缺省情况下，端口 802.1X Critical Voice VLAN 功能处于关闭状态。

#### 2.17 配置认证触发功能

##### 1. 功能简介

对于不支持主动发送EAPOL-Start报文来发起802.1X认证的客户端，设备支持配置认证触发功能，即设备主动向该端口上的客户端发送认证请求来触发 802.1X 认证。设备提供了以下两种类型的认证触发功能：
• 组播触发功能：启用了该功能的端口会定期（间隔时间通过命令 dot1x timer tx-period设置）向客户端组播发送 报文来检测客户端并触发认证。
EAP-Request/Identity单播触发功能：当启用了该功能的端口收到源 地址未知的报文时，会主动向该 地
• MAC MAC址单播发送 EAP-Request/Identity 报文，若端口在指定的时间内（通过命令 dot1x timer tx-period 设置）没有收到客户端的响应，则重发该报文（重发次数通过命令 dot1x retry设置）。

##### 2. 配置限制和指导

若端口连接的 客户端不能主动发起认证，则需要开启组播触发功能。
• 802.1X若端口连接的 客户端不能主动发起认证，且仅部分 客户端需要进行认证，为
• 802.1X 802.1X避免不希望认证或已认证的 802.1X 客户端收到多余的认证触发报文，则需要开启单播触发功能。
• 建议组播触发功能和单播触发功能不要同时开启，以免认证报文重复发送。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) （可选）配置用户名请求超时定时器。
dot1x timer tx-period tx-period-value缺省情况下，用户名请求超时定时器的值为 30 秒。
(3) 进入接口视图。
interface interface-type interface-number
(4) 开启认证触发功能。
dot1x { multicast-trigger | unicast-trigger }缺省情况下，组播触发功能处于开启状态，单播触发功能处于关闭状态。

#### 2.18 配置端口同时接入用户数的最大值

功能简介
1.
由于系统资源有限，如果当前端口上接入的用户过多，接入用户之间会发生资源的争用。因此限制接入用户数可以使属于当前端口的用户获得可靠的性能保障。

##### 2. 配置步骤

##### 1. 功能简介

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置端口同时接入用户数的最大值。
dot1x max-user max-number
缺省情况下，端口同时接入用户数的最大值为 4294967295。

#### 2.19 配置设备向接入用户发送认证请求报文的最大次数

功能简介
1.
如果设备向用户发送认证请求报文后，在规定的时间里（可通过命令 dot1x timer tx-period或者 dot1x timer supp-timeout 设定）没有收到用户的响应，则设备将向用户重发该认证请求报文，若设备累计发送认证请求报文的次数达到配置的最大值后，仍然没有得到用户响应，则停止发送认证请求。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 配置设备向接入用户发送认证请求报文的最大次数。
dot1x retry retries缺省情况下，设备最多可向接入用户发送 2 次认证请求报文。

#### 2.20 配置在线用户握手功能

##### 1. 功能简介

开 启 设 备 的 在 线 用 户 握 手 功 能 后 ， 设 备 会 定 期 （ 时 间 间 隔 通 过 命 令 dot1x timer设 置 ） 向 通 过 认 证 的 在 线 用 户 发 送 握 手 请 求 报 文handshake-period 802.1X（EAP-Request/Identity），以定期检测用户的在线情况。如果设备连续多次（通过命令 dot1x retry 设置）没有收到客户端的应答报文（EAP-Response/Identity），则会将用户置为下线状态。
有些 802.1X 客户端如果没有收到设备回应的在线握手成功报文（EAP-Success），就会自动下线。
为了避免这种情况发生，需要在端口上开启发送在线握手成功报文功能。
在线用户握手功能处于开启状态的前提下，还可以通过开启在线用户握手安全功能，来防止在线的认证用户使用非法的客户端与设备进行握手报文的交互，而逃过代理检测、双网卡检测等
802.1X iNode 客户端的安全检查功能。开启了在线用户握手安全功能的设备通过检验客户端上传的握手报文中携带的验证信息，来确认用户是否使用 iNode 客户端进行握手报文的交互。如果握手检验不通过，则会将用户置为下线状态。

##### 2. 配置限制和指导

• 部分 802.1X 客户端不支持与设备进行握手报文的交互，因此建议在这种情况下，关闭设备的
在线用户握手功能，避免该类型的在线用户因没有回应握手报文而被强制下线。

在线用户握手功能处于开启状态时，安全握手功能才会生效。
•在线用户握手安全功能仅能在 iNode 客户端和 iMC 服务器配合使用的组网环境中生效。
•只有当 802.1X 客户端需要收到在线握手成功报文时，才需要开启端口发送在线握手成功报文
•功能。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) （可选）配置握手定时器。
dot1x timer handshake-period handshake-period-value
缺省情况下，握手定时器的值为 秒。
15
进入接口视图。
(3)
interface interface-type interface-number
开启在线用户握手功能。
(4)
dot1x handshake
缺省情况下，在线用户握手功能处于开启状态。
(5) （可选）开启在线用户握手安全功能。
dot1x handshake secure
缺省情况下，在线用户握手安全功能处于关闭状态。
(6) （可选）开启端口发送在线握手成功报文功能。
dot1x handshake reply enable
缺省情况下，端口不发送在线握手成功报文。

#### 2.21 配置802.1X支持的域名分隔符

##### 1. 功能简介

每个接入用户都属于一个 域，该域是由用户登录时提供的用户名决定的，若用户名中携带域名，ISP则设备使用该域中的 AAA 配置对用户进行认证、授权和计费，否则使用系统中的缺省域；若设备指定了 802.1X 的强制认证域，则无论用户名中是否携带域名，设备均使用指定的强制认证域。因此，设备能够准确解析用户名中的纯用户名和域名对于为用户提供认证服务非常重要。由于不同的客户端所支持的用户名域名分隔符不同，为了更好地管理和控制不同用户名格式的
802.1X 802.1X用户接入，需要在设备上指定 802.1X 可支持的域名分隔符。
目 前 ，802.1X 支 持 的 域 名 分 隔 符 包 括@ 、 \ 、 . 、 和 / ， 对 应 的 用 户 名 格 式 分 别 为username@domain-name ， domain-name\username ， username.domain-name 和username/domain-name，其中 username 为纯用户名、domain-name 为域名。如果用户名中包含有多个域名分隔符字符，则设备仅将最后一个出现的域名分隔符识别为实际使用的域名分隔符，例如，用户输入的用户名为 123/22\@abc，设备上指定 802.1X 支持的域名分隔符为/、\，则识别出的纯用户名为 @abc ，域名为 123/22 。

##### 3. 配置步骤

##### 1. 功能简介

##### 2. 配置限制和指导

• 如果用户输入的用户名中不包含任何 802.1X 可支持的域名分隔符，则设备会认为该用户名并
未携带域名，则使用系统中的缺省域对该用户进行认证。
• 若设备上指定发送给认证服务器的用户名携带域名（user-name-format with-domain），
则发送给认证服务器的用户名包括三个部分：识别出的纯用户名、域名分隔符@、最终使用
的认证域名。例如，用户输入的用户名为 121.123/22\@abc，指定 802.1X支持的域名分隔符
为/、\、.，最终使用的认证域为 xyz，则发送给认证服务器的用户名为@abc@xyz。
user-name-format 命令的具体介绍请参见“安全命令参考”中的“AAA”。
为保证用户信息可在认证服务器上被准确匹配到，设备上指定的 802.1X 支持的域名分隔符必
•
须与认证服务器支持的域名分隔符保持一致，否则可能会因为服务器匹配用户失败而导致用户
认证失败。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 指定 802.1X 支持的域名分隔符。
dot1x domain-delimiter string
缺省情况下，仅支持域名分隔符@。

#### 2.22 配置端口发送802.1X协议报文不携带VLAN Tag

功能简介
1.
Hybrid 端口开启 802.1X 认证，若该端口上通过 port hyrid vlan 命令配置了转发缺省 VLAN 报文携带 Tag，则端口发送的缺省 内的 协议报文默认携带 Tag。这种情况VLAN VLAN 802.1X VLAN下，当终端发送的是不带 VLAN Tag 的报文进行 802.1X 认证时，由于接收的是带 Tag 的报文，会导致 802.1X 认证失败。为了解决这个问题，设备支持配置端口发送 802.1X 协议报文时不带 VLAN的功能。
Tag

##### 2. 配置准备

配置端口发送 协议报文不携带 之前，需要将开启 认证端口的链路类型配
802.1X VLAN Tag 802.1X置为 Hybrid。具体配置请参见“二层技术-以太网交换配置指导”中的“VLAN”。

##### 3. 配置限制和指导

除非 Hybrid 端口上配置了转发缺省 VLAN 报文携带 VLAN Tag，而终端发送的是不带 VLAN Tag 的报文进行 认证，其它场景请不要开启本功能，否则端口发送的所有 报文都将去除
802.1X 802.1X VLAN Tag，可能导致正常用户无法通过 802.1X 认证。

##### 4. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置端口发送 802.1X 协议报文不携带 VLAN Tag。

##### 1. 功能简介

##### 2. 配置步骤

dot1x eapol untag缺省情况下，端口发送 802.1X 协议报文携带 VLAN Tag。

#### 2.23 配置MAC地址认证成功用户进行802.1X认证的最大尝试次数

##### 1. 功能简介

当端口上开启了 MAC 地址认证和 802.1X 认证的情况下，若已经通过 MAC 地址认证的用户向设备发送了 EAP 报文请求进行 802.1X 认证，缺省情况下，设备允许其进行 802.1X 认证。若该用户通过了 802.1X 认证，设备将强制此 MAC 地址认证用户下线，以 802.1X 用户的身份上线；若该用户未通过 认证，则后续会进行多次 认证尝试。若并不希望此类用户多次进行
802.1X 802.1X 802.1X认证尝试，则可以通过本命令限制 MAC 地址认证成功用户进行 802.1X 认证的最大尝试次数。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置 MAC 地址认证成功用户进行 802.1X 认证的最大次数。
dot1x after-mac-auth max-attempt max-attempts缺省情况下，不限制 MAC 地址认证成功的用户进行 802.1X 认证的最大次数。

#### 2.24 配置802.1X用户IP地址冻结功能

功能简介
1.
基于 802.1X 的 IP Source Guard 功能，需要 802.1X 客户端支持上传 IP 地址，设备会根据 802.1X功能获得的用户 地址和 地址等信息动态生成 绑定表项来过滤端口收到的IP MAC IP Source Guard IPv4 报文。有关 IP Source Guard 的详细介绍，请参考“安全配置指导”中的“IP Source Guard”。
为了防止 802.1X 用户私自修改 IP 地址，设备支持为配置 802.1X 用户 IP 地址冻结功能。开启该功能后，设备首次获取并保存了 802.1X 上线用户的 IP 地址之后，不会随着该用户 IP 地址的变化而更新 IP Source Guard 动态绑定表中用户的 IP 地址。

##### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 开启 802.1X 用户 IP 地址冻结功能。
dot1x user-ip freeze缺省情况下， 802.1X 用户 IP 地址冻结功能处于关闭状态。

##### 3. 配置步骤

#### 2.25 配置802.1X认证的MAC地址绑定功能

##### 1. 功能简介

开启 认证的 地址绑定功能后，设备会将通过 认证上线用户的 地址与用
802.1X MAC 802.1X MAC户接入端口绑定，自动生成 802.1X 认证用户的 MAC 地址与接入端口的绑定表项。同时，设备也支持通过命令行手工配置 802.1X 认证的 MAC 地址绑定表项。这两种方式产生的 802.1X 认证的 MAC地址绑定表项都不会自动老化。因此，当这些 MAC 地址被绑定的用户在其它开启 802.1X 认证的地址绑定功能的端口上进行 认证时，将不能通过认证，实现了 用户通过设备MAC 802.1X 802.1X的指定端口连接网络，不能随意更换接入端口的需求。

##### 2. 配置限制与指导

• 802.1X 认证的 MAC 地址绑定功能仅在接入控制方式为 MAC-based 的端口上生效。
• 802.1X 认证的 MAC 地址绑定表项不会自动老化，即使该用户下线后或设备保存配置重启后
也不会删除此绑定表项。只能通过 undo dot1x mac-binding 命令手工删除表项。用户在
线时，不允许删除此表项。
认证的 地址绑定功能受端口允许同时接入 用户数的最大值（通过
• 802.1X MAC 802.1X dot1x
max-user 命令配置）影响。当绑定表项数等于端口允许同时接入 802.1X 用户最大用户数时，
MAC 地址绑定表项之外的用户均会认证失败。例如，如果开启了 802.1X 认证的 MAC 地址绑
定功能，并且配置了端口允许同时接入 用户数的最大值为 1，此时只能有一个用户通
802.1X
过 802.1X 认证上线，并且此用户下线后其 MAC 地址表项不会老化，这种情况下该端口上其
它用户进行认证会提示认证失败。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 开启 802.1X 认证的 MAC 地址绑定功能。
dot1x mac-binding enable
缺省情况下，802.1X 认证的 MAC 地址绑定功能处于关闭状态。
(4) （可选）手工配置 802.1X 认证 MAC 地址绑定表项。
dot1x mac-binding mac-address
缺省情况下，端口上不存在 802.1X 认证的 MAC 地址绑定表项。

#### 2.26 配置802.1X支持EAD快速部署

##### 1. 配置限制和指导

• MAC 地址认证和端口安全特性不支持 EAD 的快速部署功能，全局使能 MAC 认证或端口安全
功能将会使 快速部署功能失效。
EAD
为使 EAD 快速部署功能生效，必须保证指定端口的授权模式为 auto。
•
MAC 地址认证、端口安全功能均与 Free IP 配置互斥。
•

##### 2. 配置步骤

开启 EAD 快速部署辅助功能与 802.1X Guest VLAN 功能不建议同时配置，否则可能导致
•功能无法正常使用。
802.1X Guest VLAN在同时配置了 与 功能的情况下，请保证 网段为
• Free IP Auth-Fail VLAN Free IP Auth-Fail VLAN 可允许访问的网络资源。这种情况下，用户只能访问 Free IP，不能访问其它资源。
• 重定向 URL 必须处于 Free IP 网段内，否则无法实现重定向。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 开启 EAD 快速部署辅助功能。
dot1x ead-assistant enable缺省情况下，EAD 快速部署辅助功能处于关闭状态。
(3) 配置 Free IP。
dot1x ead-assistant free-ip ip-address { mask-length | mask-address }可通过重复执行此命令来配置多个 Free IP。
(4) （可选）配置用户 HTTP 或 HTTPS 访问的重定向 URL。
dot1x ead-assistant url url-string缺省情况下，未配置 用户 或 访问的重定向 URL。
802.1X HTTP HTTPS若需要对用户的 访问进行重定向，需要在设备上配置对 报文进行重定向的内HTTPS HTTPS部侦听端口号，具体配置请参考“三层技术-IP 业务配置指导”中的“HTTP 重定向”。
(5) （可选）配置 EAD 规则老化时间。
dot1x timer ead-timeout ead-timeout-value缺省情况下，EAD 规则老化时间为 分钟。
30在接入用户数量较多时，可以适当缩短 规则老化时间，以提高 的使用效率。
EAD ACL

#### 2.27 配置802.1X接入用户日志信息功能

##### 1. 功能简介

802.1X 接入用户日志信息是为了满足网络管理员维护的需要，对 802.1X 认证用户的接入信息进行
记录。设备生成的 802.1X 接入用户日志信息会交给信息中心模块处理，信息中心模块的配置将决
定日志信息的发送规则和发送方向。关于信息中心的详细描述请参见“网络管理和监控配置指导”
中的“信息中心”。

##### 2. 配置限制和指导

为了防止设备输出过多的 802.1X 接入用户日志信息，一般情况下建议关闭此功能。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 开启 802.1X 接入用户日志信息功能。
dot1x access-user log enable [ abnormal-logoff | failed-login |
normal-logoff | successful-login ] *

缺省情况下，802.1X 接入用户日志信息功能处于关闭状态。
配置本命令时，如果未指定任何参数，将同时开启所有参数对应的日志功能。

#### 2.28 802.1X显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 802.1X 的运行情况，通过查看显示信息验证配置的效果。
在用户视图下，执行 reset 命令可以清除 802.1X 的统计信息。
表2-1 802.1X 显示和维护操作 命令显示802.1X的会话连接信息、相关统计 display dot1x [ sessions | statistics ] [ interface信息或配置信息 interface-type interface-number ] display dot1x connection [ open ] [ interface显示当前802.1X在线用户的详细信息 interface-type interface-number | slot slot-number | user-mac mac-address | user-name name-string ] display dot1x mac-address { auth-fail-vlan |显示指定类型的VLAN中的802.1X用户critical-vlan | guest-vlan } [ interface的MAC地址信息interface-type interface-number ] reset dot1x guest-vlan interface interface-type清除Guest VLAN内802.1X用户interface-number [ mac-address mac-address ] reset dot1x statistics [ interface interface-type清除802.1X的统计信息interface-number ]

#### 2.29 802.1X典型配置举例

##### 2.29.1 802.1X认证配置举例

###### 1. 组网需求

用户通过 的端口 接入网络，设备对该端口接入的用户进行Device Ten-GigabitEthernet1/0/1 802.1X认证以控制其访问 Internet，具体要求如下：
• 由两台 RADIUS 服务器组成的服务器组与 Device 相连，其 IP 地址分别为 10.1.1.1/24 和
10.1.1.2/24，使用前者作为主认证/计费服务器，使用后者作为备份认证/计费服务器。
• 端口 Ten-GigabitEthernet1/0/1 下的所有接入用户均需要单独认证，当某个用户下线时，也只有该用户无法使用网络。
认证时，首先进行 RADIUS 认证，如果 RADIUS 服务器没有响应则进行本地认证。
•所有接入用户都属于同一个 ISP 域 bbb。
•
• Device 与 RADIUS 认证服务器交互报文时的共享密钥为 name、与 RADIUS 计费服务器交互报文时的共享密钥为 money。

###### 2. 组网图

图2-1 802.1X 认证组网图

###### 3. 配置步骤

下述配置步骤中包含了若干 AAA/RADIUS 协议的配置命令，关于这些命令的详细介绍请参考“安全命令参考”中的“AAA”。
(1) 配置 RADIUS 服务器，添加用户帐户，保证用户的认证/授权/计费功能正常运行（略）
(2) 配置各接口的 IP 地址（略）
(3) 配置本地用户\# 添加网络接入类本地用户，用户名为 localuser，密码为明文输入的 localpass。（此处添加的本地用户的用户名和密码需要与服务器端配置的用户名和密码保持一致，本例中的localuser 仅为示例，请根据实际情况配置）
<Device> system-view [Device] local-user localuser class network [Device-luser-network-localuser] password simple localpass \# 配置本地用户的服务类型为 lan-access 。
[Device-luser-network-localuser] service-type lan-access [Device-luser-network-localuser] quit配置 方案
(4) RADIUS创建 方案 并进入其视图。
\# RADIUS radius1 [Device] radius scheme radius1 \# 配置主认证/计费 RADIUS 服务器的 IP 地址。
[Device-radius-radius1] primary authentication 10.1.1.1 [Device-radius-radius1] primary accounting 10.1.1.1配置备份认证/计费 服务器的 地址。
\# RADIUS IP [Device-radius-radius1] secondary authentication 10.1.1.2 [Device-radius-radius1] secondary accounting 10.1.1.2 \# 配置 Device 与认证/计费 RADIUS 服务器交互报文时的共享密钥。

###### 4. 验证配置

[Device-radius-radius1] key authentication simple name [Device-radius-radius1] key accounting simple money \# 配置发送给 RADIUS 服务器的用户名不携带域名。
[Device-radius-radius1] user-name-format without-domain [Device-radius-radius1] quit发送给服务器的用户名是否携带域名与服务器端是否接受携带域名的用户名以及服务器端的配置有关：
• 若服务器端不接受携带域名的用户名，或者服务器上配置的用户认证所使用的服务不携带域名后缀，则 Device 上指定不携带用户名（without-domain）；
若服务器端可接受携带域名的用户名，且服务器上配置的用户认证所使用的服务携带域名
•后缀，则 上指定携带用户名（with-domain）。
Device
(5) 配置 ISP 域\# 创建域 bbb 并进入其视图。
[Device] domain bbb \# 配置 802.1X 用户使用 RADIUS 方案 radius1 进行认证、授权、计费，并采用 local 作为备选方法。
[Device-isp-bbb] authentication lan-access radius-scheme radius1 local [Device-isp-bbb] authorization lan-access radius-scheme radius1 local [Device-isp-bbb] accounting lan-access radius-scheme radius1 local [Device-isp-bbb] quit
(6) 配置 802.1X开启端口 的 802.1X。
\# Ten-GigabitEthernet1/0/1 [Device] interface ten-gigabitethernet 1/0/1 [Device-Ten-GigabitEthernet1/0/1] dot1x \# 配置端口的 802.1X 接入控制方式为 MAC-based（该配置可选，因为端口的接入控制在缺省情况下就是基于 MAC 地址的）。
[Device-Ten-GigabitEthernet1/0/1] dot1x port-method macbased \# 指定端口上接入的 802.1X 用户使用强制认证域 bbb 。
[Device-Ten-GigabitEthernet1/0/1] dot1x mandatory-domain bbb [Device-Ten-GigabitEthernet1/0/1] quit \# 开启全局 802.1X。
[Device] dot1x
(7) 配置 802.1X 客户端（略）
若使用 客户端，为保证备选的本地认证可成功进行，请确认 连接H3C iNode 802.1X 802.1X属性中的“上传客户端版本号”选项未被选中。
验证配置
4.
使用命令 display dot1x interface 可以查看端口 Ten-GigabitEthernet1/0/1 上的 802.1X 的配置情况。当 用户输入正确的用户名和密码成功上线后，可使用命令 display dot1x
802.1X connection 查看到上线用户的连接情况。

###### 1. 组网需求

##### 2.29.2 802.1X支持Guest VLAN、授权VLAN下发配置举例

组网需求
1.
如 图 2-2 所示，一台主机通过 802.1X认证接入网络，认证服务器为RADIUS服务器。Host接入Device的端口Ten-GigabitEthernet1/0/2 在VLAN 内；认证服务器在VLAN 内；Update Server是用于客1 2户 端 软 件 下 载 和 升 级 的 服 务 器 ， 在VLAN 10 内 ； Device 连 接Internet 网 络 的 端 口Ten-GigabitEthernet1/0/3 在VLAN 5 内。现有如下组网需求：
• 在端口上配置完 Guest VLAN，则立即将该端口 Ten-GigabitEthernet1/0/2 加入 Guest VLAN（VLAN 10）中，此时 Host 和 Update Server 都在 VLAN 10 内，Host 可以访问 Update Server并下载 客户端。
802.1X用户认证成功上线后，认证服务器下发 5，此时 和连接 网络的端口
• VLAN Host Internet Ten-GigabitEthernet1/0/3 都在 VLAN 5 内，Host 可以访问 Internet。

###### 2. 组网图

图2-2 Guest VLAN 及 VLAN 下发组网图

###### 3. 配置步骤

下述配置步骤中包含了若干 AAA/RADIUS 协议的配置命令，关于这些命令的详细介绍请参考“安全命令参考”中的“AAA”。

(1) 配置 RADIUS 服务器，添加用户帐户，指定要授权下发的 VLAN（本例中为 VLAN 5），并保
证用户的认证/授权/计费功能正常运行（略）
创建 并将端口加入对应
(2) VLAN VLAN
<Device> system-view
[Device] vlan 1
[Device-vlan1] port ten-gigabitethernet 1/0/2
[Device-vlan1] quit
[Device] vlan 10
[Device-vlan10] port ten-gigabitethernet 1/0/1
[Device-vlan10] quit
[Device] vlan 2
[Device-vlan2] port ten-gigabitethernet 1/0/4
[Device-vlan2] quit
[Device] vlan 5
[Device-vlan5] port ten-gigabitethernet 1/0/3
[Device-vlan5] quit
(3) 配置 RADIUS 方案
\# 创建 RADIUS 方案 2000 并进入其视图。
[Device] radius scheme 2000
\# 配置主认证/计费 RADIUS 服务器及其共享密钥。
[Device-radius-2000] primary authentication 10.11.1.1 1812
[Device-radius-2000] primary accounting 10.11.1.1 1813
[Device-radius-2000] key authentication simple abc
[Device-radius-2000] key accounting simple abc
\# 配置发送给 RADIUS 服务器的用户名不携带域名。
[Device-radius-2000] user-name-format without-domain
[Device-radius-2000] quit
(4) 配置 ISP 域
创建域 并进入其视图。
\# bbb
[Device] domain bbb
\# 配置 802.1X 用户使用 RADIUS 方案 2000 进行认证、授权、计费。
[Device-isp-bbb] authentication lan-access radius-scheme 2000
[Device-isp-bbb] authorization lan-access radius-scheme 2000
[Device-isp-bbb] accounting lan-access radius-scheme 2000
[Device-isp-bbb] quit
(5) 配置 802.1X
\# 开启端口 Ten-GigabitEthernet1/0/2 的 802.1X。
[Device] interface ten-gigabitethernet 1/0/2
[Device-Ten-GigabitEthernet1/0/2] dot1x
\# 配置端口的 802.1X 接入控制的方式为 Port-based。
[Device-Ten-GigabitEthernet1/0/2] dot1x port-method portbased
\# 配置端口的 802.1X 授权状态为 auto。（此配置可选，端口的授权状态缺省为 auto）
[Device-Ten-GigabitEthernet1/0/2] dot1x port-control auto
\# 配置端口的 802.1X Guest VLAN 为 VLAN10。

[Device-Ten-GigabitEthernet1/0/2] dot1x guest-vlan 10 [Device-Ten-GigabitEthernet1/0/2] quit \# 开启全局 802.1X。
[Device] dot1x
(6) 配置 802.1X 客户端，并保证接入端口加入 Guest VLAN 或授权 VLAN 之后，802.1X 客户端能够及时更新 地址，以实现与相应网络资源的互通（略）
IP

###### 4. 验证配置结果

可以通过命令 display dot1x interface 查看端口 Ten-GigabitEthernet1/0/2 上 Guest VLAN的配置情况。
在端口上配置完 Guest VLAN，则该端口会被立即加入其所属的 Guest VLAN，通过命令 display vlan 10 可以查看到端口 Ten-GigabitEthernet1/0/2 加入了配置的 Guest VLAN（VLAN 10）。
在 用 户 认 证 成 功 之 后 ， 通 过 命 令 display interface 可 以 看 到 用 户 接 入 的 端 口加入了认证服务器下发的 中。
Ten-GigabitEthernet1/0/2 VLAN 5

##### 2.29.3 802.1X支持ACL下发配置举例

###### 1. 组网需求

用户通过 Device 的端口 Ten-GigabitEthernet1/0/1 接入网络，Device 对该端口接入的用户进行
802.1X 认证以控制其访问 Internet，具体要求如下：
• 使用 RADIUS 服务器 10.1.1.1/24 作为认证/授权服务器，RADIUS 服务器 10.1.1.2/24 作为计费服务器；
• 通过认证服务器下发 ACL，禁止上线的 802.1X 用户在工作日的工作时间（8:00～18:00）访问 地址为 的 服务器。
IP 10.0.0.1/24 FTP

###### 2. 组网图

图2-3 支持 下发典型组网图
802.1X ACL RADIUS server cluster Auth: 10.1.1.1 Acct: 10.1.1.2 XGE1/0/2 XGE1/0/3 XGE1/0/1 Internet Vlan-int2
192.168.1.1/24 Host Device FTP server
192.168.1.10/24 10.0.0.1/24

###### 3. 配置步骤

下述配置步骤中包含了若干 AAA/RADIUS 协议的配置命令，关于这些命令的详细介绍请参考“安全命令参考”中的“AAA”。
(1) 配置 RADIUS 服务器，添加用户帐户，指定要授权下发的 ACL（本例中为 ACL 3000），并保证用户的认证/授权/计费功能正常运行（略）
(2) 配置各接口的 IP 地址（略）
(3) 配置 RADIUS 方案<Device> system-view [Device] radius scheme 2000 [Device-radius-2000] primary authentication 10.1.1.1 1812 [Device-radius-2000] primary accounting 10.1.1.2 1813 [Device-radius-2000] key authentication simple abc [Device-radius-2000] key accounting simple abc [Device-radius-2000] user-name-format without-domain [Device-radius-2000] quit
(4) 配置 ISP 域的 AAA 方法[Device] domain bbb [Device-isp-bbb] authentication lan-access radius-scheme 2000 [Device-isp-bbb] authorization lan-access radius-scheme 2000 [Device-isp-bbb] accounting lan-access radius-scheme 2000 [Device-isp-bbb] quit配置名为 的时间段，其时间范围为每周工作日的 点到 点
(5) ftp 8 18 [Device] time-range ftp 8:00 to 18:00 working-day
(6) 配置 ACL 3000，拒绝用户在工作日的工作时间内访问 FTP 服务器 10.0.0.1 的报文通过[Device] acl advanced 3000 [Device-acl-ipv4-adv-3000] rule 0 deny ip destination 10.0.0.1 0 time-range ftp [Device-acl-ipv4-adv-3000] quit
(7) 配置 802.1X \# 开启全局 802.1X。
[Device] dot1x开启端口 的 802.1X。
\# Ten-GigabitEthernet1/0/1 [Device] interface ten-gigabitethernet 1/0/1 [Device-Ten-GigabitEthernet1/0/1] dot1x
(8) 配置 802.1X 客户端，并保证接入端口加入 Guest VLAN 或授权 VLAN 之后客户端能够及时更新 IP 地址，以实现与相应网络资源的互通（略）

###### 4. 验证配置

当用户认证成功上线后，在工作日的工作时间 服务器。
Ping FTP C:\>ping 10.0.0.1 Pinging 10.0.0.1 with 32 bytes of data:

Request timed out.
Request timed out.
Request timed out.
Request timed out.
Ping statistics for 10.0.0.1:
Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),由以上过程可知，用户无法 ping 通 FTP 服务器，说明认证服务器下发的 ACL 已对该用户生效。

##### 2.29.4 802.1X支持EAD快速部署典型配置举例（DHCP中继组网）

###### 1. 组网需求

某公司用户主机通过 Device 接入 Internet，并通过 DHCP 服务器动态获取 IP 地址。目前，公司部署 EAD 解决方案，要求所有用户主机通过 802.1X 认证上网，因此需要所有主机上安装配套的
802.1X 客户端。由于网络中的用户主机数量较大，为减轻网络管理员安装以及升级 802.1X 客户端的工作量，在 网段部署一台 服务器专门提供客户端软件下载。具体要求如下：
192.168.2.0/24 Web未进行 认证或者 认证失败的用户，只能访问 网段，并可通过
• 802.1X 802.1X 192.168.2.0/24该网段内的 DHCP 服务器动态获取 192.168.1.0/24 网段的 IP 地址。
• 未进行 802.1X 认证或者 802.1X 认证失败的用户通过浏览器访问非 192.168.2.0/24 网段的外部网络时，用户访问的页面均会被 Device 重定向至管理员预设的 Web 服务器页面，该 Web服务器页面将提示用户进行 802.1X 客户端的下载。
用户成功通过 802.1X 认证之后，可正常访问网络。
•

###### 2. 组网图

图2-4 支持 快速部署典型配置组网图
802.1X EAD

###### 3. 配置步骤

(1) 完成各服务器的配置
\# 配置 DHCP 服务器，保证用户可成功获取 192.168.1.0/24 网段的 IP 地址（略）。
\# 配置 Web 服务器，保证用户可成功登录预置的 Web 页面进行 802.1X 客户端的下载（略）。
\# 配置认证服务器，保证用户的认证/授权/计费功能正常运行（略）。
(2) 配置各接口的 IP 地址（略）
(3) 配置 DHCP 中继
\# 使能 DHCP 服务。
<Device> system-view
[Device] dhcp enable
\# 配置接口 Vlan-interface2 工作在 DHCP 中继模式。
[Device] interface vlan-interface 2
[Device-Vlan-interface2] dhcp select relay
\# 配置接口 Vlan-interface2 对应 DHCP 服务器组 1。
[Device-Vlan-interface2] dhcp relay server-address 192.168.2.2
[Device-Vlan-interface2] quit
配置 方案和 域
(4) RADIUS ISP
配置 方案。
\# RADIUS
[Device] radius scheme 2000
[Device-radius-2000] primary authentication 10.1.1.1 1812
[Device-radius-2000] primary accounting 10.1.1.2 1813
[Device-radius-2000] key authentication simple abc
[Device-radius-2000] key accounting simple abc
[Device-radius-2000] user-name-format without-domain
[Device-radius-2000] quit
\# 配置 ISP 域的 AAA 方法。
[Device] domain bbb
[Device-isp-bbb] authentication lan-access radius-scheme 2000
[Device-isp-bbb] authorization lan-access radius-scheme 2000
[Device-isp-bbb] accounting lan-access radius-scheme 2000
[Device-isp-bbb] quit
(5) 配置 802.1X
\# 配置 Free IP。
[Device] dot1x ead-assistant free-ip 192.168.2.0 24
\# 配置 IE 访问的重定向 URL。
[Device] dot1x ead-assistant url http://192.168.2.3
全局使能 快速部署功能。
\# EAD
[Device] dot1x ead-assistant enable
\# 开启全局 802.1X。
[Device] dot1x
\# 开启端口 Ten-GigabitEthernet1/0/1 的 802.1X。
[Device] interface ten-gigabitethernet 1/0/1
[Device-Ten-GigabitEthernet1/0/1] dot1x

###### 4. 验证配置结果

以上配置完成之后，执行命令 display dot1x 可以查看 802.1X 的配置情况。用户主机成功获得DHCP 服务器分配的 IP 地址之后，在 Windows XP 操作系统的主机上执行 ping Free IP 中的地址，可验证在 认证成功之前是否可以访问免认证网段 192.168.2.0/24。
802.1X C:\>ping 192.168.2.3 Pinging 192.168.2.3 with 32 bytes of data:
Reply from 192.168.2.3: bytes=32 time<1ms TTL=128 Reply from 192.168.2.3: bytes=32 time<1ms TTL=128 Reply from 192.168.2.3: bytes=32 time<1ms TTL=128 Reply from 192.168.2.3: bytes=32 time<1ms TTL=128 Ping statistics for 192.168.2.3:
Packets: Sent = 4, Received = 4, Lost = 0 (0% loss), Approximate round trip times in milli-seconds:
Minimum = 0ms, Maximum = 0ms, Average = 0ms用户在 802.1X 认证成功之前，通过浏览器访问任何非 Free IP 的外部网站地址时，都会被重定向到页面，此页面提供 客户端的下载服务。需要注意的是，地址栏内输入的地址应Web server 802.1X该为非 Free IP 地址才有效，例如 3.3.3.3 或者 http://3.3.3.3。

##### 2.29.5 802.1X支持EAD快速部署典型配置举例（DHCP服务器组网）

###### 1. 组网需求

某公司用户主机通过 Device 接入 Internet，并通过 DHCP 服务器动态获取 IP 地址。目前，公司部署 EAD 解决方案，要求所有用户主机通过 802.1X 认证上网，因此需要所有主机上安装配套的
802.1X 客户端。由于网络中的用户主机数量较大，为减轻网络管理员安装以及升级 802.1X 客户端的工作量，在 192.168.2.0/24 网段部署一台 Web 服务器专门提供客户端软件下载。具体要求如下：
未进行 认证或者 认证失败的用户，只能访问 网段。
• 802.1X 802.1X 192.168.2.0/24未进行 认证或者 认证失败的用户通过浏览器访问非 网段的外
• 802.1X 802.1X 192.168.2.0/24部网络时，用户访问的页面均会被 Device 重定向至管理员预设的 Web 服务器页面，该 Web服务器页面将提示用户进行 802.1X 客户端的下载。
• 用户成功通过 802.1X 认证之后，可正常访问网络。

###### 2. 组网图

图2-5 802.1X 支持 EAD 快速部署典型配置组网图

###### 3. 配置步骤

(1) 配置 Web 服务器，保证用户可成功登录预置的 Web 页面进行 802.1X 客户端的下载（略）
(2) 配置认证服务器，保证用户的认证/授权/计费功能正常运行（略）
配置各接口的 地址（略）
(3) IP
配置 服务器
(4) DHCP
使能 服务。
\# DHCP
<Device> system-view
[Device] dhcp enable
\# 配置接口 Vlan-interface2 工作在 DHCP 服务器模式。
[Device] interface vlan-interface 2
[Device-Vlan-interface2] dhcp select server
[Device-Vlan-interface2] quit
\# 配置 DHCP 地址池 0 的属性：地址池动态分配的网段为 192.168.1.0/24、网关地址为
192.168.1.1。
[Device] dhcp server ip-pool 0
[Device-dhcp-pool-0] network 192.168.1.0 mask 255.255.255.0
[Device-dhcp-pool-0] gateway-list 192.168.1.1
[Device-dhcp-pool-0] quit
(5) 配置 RADIUS 方案和 ISP 域
配置 方案。
\# RADIUS
[Device] radius scheme 2000
[Device-radius-2000] primary authentication 10.1.1.1 1812
[Device-radius-2000] primary accounting 10.1.1.2 1813
[Device-radius-2000] key authentication simple abc

[Device-radius-2000] key accounting simple abc [Device-radius-2000] user-name-format without-domain [Device-radius-2000] quit \# 配置 ISP 域的 AAA 方法。
[Device] domain bbb [Device-isp-bbb] authentication lan-access radius-scheme 2000 [Device-isp-bbb] authorization lan-access radius-scheme 2000 [Device-isp-bbb] accounting lan-access radius-scheme 2000 [Device-isp-bbb] quit配置
(6) 802.1X配置 IP。
\# Free [Device] dot1x ead-assistant free-ip 192.168.2.0 24 \# 配置 IE 访问的重定向 URL。
[Device] dot1x ead-assistant url http://192.168.2.3 \# 开启 EAD 快速部署辅助功能。
[Device] dot1x ead-assistant enable开启全局 802.1X。
\# [Device] dot1x \# 开启端口 Ten-GigabitEthernet1/0/1 的 802.1X。
[Device] interface ten-gigabitethernet 1/0/1 [Device-Ten-GigabitEthernet1/0/1] dot1x

###### 4. 验证配置

以上配置完成之后，执行命令 可以查看 的配置情况。用户主机成功获得display dot1x 802.1X DHCP 服务器分配的 IP 地址之后，在 Windows XP 操作系统的主机上执行 ping Free IP 中的地址，可验证在 802.1X 认证成功之前是否可以访问免认证网段 192.168.2.0/24。
C:\>ping 192.168.2.3 Pinging 192.168.2.3 with 32 bytes of data:
Reply from 192.168.2.3: bytes=32 time<1ms TTL=128 Reply from 192.168.2.3: bytes=32 time<1ms TTL=128 Reply from 192.168.2.3: bytes=32 time<1ms TTL=128 Reply from 192.168.2.3: bytes=32 time<1ms TTL=128 Ping statistics for 192.168.2.3:
Packets: Sent = 4, Received = 4, Lost = 0 (0% loss), Approximate round trip times in milli-seconds:
Minimum = 0ms, Maximum = 0ms, Average = 0ms用户在 802.1X 认证成功之前，通过浏览器访问任何非 Free IP 的外部网站地址时，都会被重定向到Web server 页面，此页面提供 802.1X 客户端的下载服务。需要注意的是，地址栏内输入的地址应该为非 Free IP 地址才有效，例如 3.3.3.3 或者 http://3.3.3.3 。

###### 3. 处理过程

#### 2.30 802.1X常见故障处理

##### 2.30.1 用户通过浏览器访问外部网络不能正确重定向

###### 1. 故障现象

用户在浏览器中输入地址，但该 HTTP 访问不能被正确重定向到指定的 URL 服务器。

###### 2. 故障分析

• 用户在浏览器地址栏内输入了字符串类型的地址。由于用户主机使用的操作系统首先会将这个
字符串地址作为名字进行网络地址解析，如果解析不成功通常会以非 X.X.X.X 形式的网络地址
发送 请求，这样的请求不能进行重定向；
ARP
用户在 IE 地址栏内输入了 Free IP 内的任意地址。设备会认为用户试图访问 Free IP 内的某台
•
主机，而不对其进行重定向，即使这台主机不存在；
用户在配置和组网时没有将服务器加入 IP，或者配置的 为不存在的地址，或者该
• Free URL
URL 指向的服务器没有提供 Web 服务。
处理过程
3.
• 地址栏内输入的地址应该为 X.X.X.X（点分十进制格式）的非 Free IP 地址才有效。
• 确保设备及服务器上的配置正确且有效。

## 03-MAC地址认证配置

目 录地址认证简介地址认证支持下发 属性地址认证配置任务简介指定 地址认证用户使用的认证域配置 地址认证的配置端口上最多允许同时接入的 地址认证用户数配置MAC地址认证请求中携带用户IP地址地址认证的显示和维护

下发ACL典型配置举例

### 1 MAC地址认证

#### 1.1 MAC地址认证简介

MAC 地址认证是一种基于端口和 MAC 地址对用户的网络访问权限进行控制的认证方法，无需安装客户端软件。设备在启动了 MAC 地址认证的端口上首次检测到用户的 MAC 地址以后，启动对该用户的认证操作。认证过程中，不需要用户手动输入用户名或密码。若该用户认证成功，则允许其通过端口访问网络资源，否则该用户的 MAC 地址就被设置为静默 MAC。在静默时间内，来自此 MAC地址的用户报文到达时，设备直接做丢弃处理，以防止非法 MAC 短时间内的重复认证。

##### 1.1.1 MAC地址认证用户的帐号格式

地址认证用户使用的帐号格式分为两种：
MAC MAC地址帐号：设备使用源MAC地址作为用户认证时的用户名和密码，如 图 所示。
• 1-1固定用户名帐号：所有MAC地址认证用户均使用设备上指定的一个固定用户名和密码替代用
•户的MAC地址作为身份信息进行认证，如 图 1-2 所示。由于同一个端口下可以有多个用户进行认证，因此这种情况下端口上的所有MAC地址认证用户均使用同一个固定用户名进行认证，服务器端仅需要配置一个用户帐户即可满足所有认证用户的认证需求，适用于接入客户端比较可信的网络环境。
图1-1 MAC 地址帐号的 MAC 地址认证示意图

图1-2 固定用户名帐号的 MAC 地址认证示意图Device Local user account abc Host User account MAC: 1-1-1 RADIUS user account Fixed account abc Username/Password Username：abc Password：123 （abc/123）
Host RADIUS server MAC: 2-2-2

##### 1.1.2 MAC地址认证的认证方式

目前设备支持两种方式的 MAC 地址认证，通过 RADIUS（Remote Authentication Dial-In User Service，远程认证拨号用户服务）服务器进行远程认证和在接入设备上进行本地认证。有关远程RADIUS 认证和本地认证的详细介绍请参见“安全配置指导”中的“AAA”。

###### 1. RADIUS服务器认证方式进行MAC地址认证

当选用 服务器认证方式进行 地址认证时，设备作为 客户端，与RADIUS MAC RADIUS RADIUS服务器配合完成 MAC 地址认证操作：
• 若采用 MAC 地址帐号，则设备将检测到的用户 MAC 地址作为用户名和密码发送给 RADIUS服务器进行验证。
• 若采用固定用户名帐号，则设备将一个已经在本地指定的 MAC 地址认证用户使用的固定用户名和对应的密码作为待认证用户的用户名和密码，发送给 RADIUS 服务器进行验证。
RADIUS 服务器完成对该用户的认证后，认证通过的用户可以访问网络。

###### 2. 本地认证方式进行MAC地址认证

当选用本地认证方式进行 MAC 地址认证时，直接在设备上完成对用户的认证。需要在设备上配置本地用户名和密码：
若采用 地址帐号，则设备将检测到的用户 地址作为待认证用户的用户名和密码与
• MAC MAC配置的本地用户名和密码进行匹配。
• 若采用固定用户名帐号，则设备将一个已经在本地指定的 MAC 地址认证用户使用的固定用户名和对应的密码作为待认证用户的用户名和密码与配置的本地用户名和密码进行匹配。
用户名和密码匹配成功后，用户可以访问网络。

##### 1.1.3 MAC地址认证支持VLAN下发

###### 1. 授权VLAN

为了将受限的网络资源与未认证用户隔离，通常将受限的网络资源和未认证的用户划分到不同的VLAN。MAC 地址认证支持远程 服务器/接入设备下发授权 VLAN，即当用户通过 地址认AAA MAC证后，远程 AAA 服务器/接入设备将指定的受限网络资源所在的 VLAN 作为授权 VLAN 下发到用户进行认证的端口。该端口被加入到授权 VLAN 中后，用户便可以访问这些受限的网络资源。

###### 2. 远程AAA授权

该方式下，需要在 AAA 服务器上指定下发给用户的授权 VLAN 信息，下发的授权 VLAN 信息可以有多种形式，包括数字型 VLAN 和字符型 VLAN，字符型 VLAN 又可分为 VLAN 名称、VLAN 组名、携带后缀的 ID（后缀只能为字母 或 t，用于标识是否携带 Tag）。
VLAN u设备收到服务器的授权 信息后，首先对其进行解析，只要解析成功，即以对应的方法下发授VLAN权 VLAN；如果解析不成功，则用户授权失败。
• 若认证服务器下发的授权 VLAN 信息为一个 VLAN ID 或一个 VLAN 名称，则仅当对应的 VLAN不为动态学习到的 VLAN、保留 VLAN、Super VLAN 和 Private VLAN 时，该 VLAN 才是有效的授权 VLAN。当认证服务器下发 VLAN 名称时，对应的 VLAN 必须为已存在的 VLAN。
• 若认证服务器下发的授权 VLAN 信息为一个 VLAN 组名，则设备首先会通过组名查找该组内配置的 列表。若查找到授权 列表，则在这一组 中，除 VLAN、动VLAN VLAN VLAN Super态 VLAN、Private VLAN 之外的所有 VLAN 都有资格被授权给用户。关于 VLAN 组的相关配置，请参见“二层技术-以太网交换配置指导”中的“VLAN”。
当端口链路类型为 Hybrid，且使能了 MAC VLAN 功能时，若端口上已有其他用户，则将(cid:123)
选择该组 VLAN 中在线用户最少的一个 VLAN 作为当前认证用户的授权 VLAN（若在线用户最小的 有多个，则选择 最小者）。
VLAN VLAN ID当端口链路类型为 Hybrid，但未使能 功能或端口链路类型为 或MAC VLAN access trunk (cid:123)
时：
− 若端口上已有其他在线用户，则查看端口上在线用户的授权 VLAN 是否存在于该组中：
存在，则将此 VLAN 授权给当前的认证用户；否则，认为当前认证用户授权失败，将被强制下线。
若当前用户为端口上第一个在线用户，则直接将该组 VLAN 中 ID 最小的 VLAN 授权给−当前的认证用户。
若认证服务器下发的授权 信息为一个包含若干 以及若干 名称的字符串，
• VLAN VLAN ID VLAN则设备首先将其解析为一组 VLAN 列表，然后采用与解析一个 VLAN 组名相同的解析逻辑选择一个授权 VLAN。
• 若认证服务器下发的授权 VLAN 信息为一个包含若干个“VLAN ID+后缀”形式的字符串，则只有第一个不携带后缀或者携带 untagged 后缀的 VLAN 将被解析为唯一的 untagged 的授权VLAN，其余 都被解析为 的授权 VLAN。例如服务器下发字符串“1u 3”，其VLAN tagged 2t中的 u 和 t 均为后缀，分别表示 untagged 和 tagged 。该字符串被解析之后， VLAN 1 为 untagged的授权 VLAN，VLAN 2 和 VLAN 3 为 tagged 的授权 VLAN。该方式下发的授权 VLAN 仅对端口链路类型为 或 的端口有效。
Hybrid Trunk端口的缺省VLAN将被修改为untagged的授权VLAN。若不存在untagged的授权VLAN，(cid:123)
则不修改端口的缺省 VLAN。
端口将允许所有解析成功的授权 VLAN 通过。
(cid:123)

###### 3. 本地AAA授权

该方式下，可以通过配置本地用户的授权属性指定下发给用户的授权 VLAN 信息，且只能指定一个授权 VLAN。设备将此 VLAN 作为该本地用户的授权 VLAN。关于本地用户的相关配置，请参见“安全配置指导”中的“AAA”。

###### 4. 不同类型的端口加入授权VLAN

设备根据用户接入的端口链路类型和授权的 VLAN 是否携带 Tag，按如下情况将端口加入到下发的授权 VLAN 中。需要注意的是，仅远程 AAA 服务器支持授权携带 Tag 的 VLAN。
授权 VLAN 未携带 Tag 的情况下：
• 若用户从 Access 类型的端口接入，则端口离开当前 VLAN 并加入第一个通过认证的用户的授权 中。
VLAN若用户从 Trunk 类型的端口接入，则设备允许下发的授权 VLAN 通过该端口，并且修改该端
•口的缺省 VLAN 为第一个通过认证的用户的授权 VLAN。
若用户从 类型的端口接入，则设备允许授权下发的授权 以不携带 的方式通
• Hybrid VLAN Tag过该端口，并且修改该端口的缺省 VLAN 为第一个通过认证的用户的授权 VLAN。需要注意的是，若该端口上使能了 MAC VLAN 功能，则设备将根据认证服务器/接入设备下发的授权 VLAN动态地创建基于用户 地址的 VLAN，而端口的缺省 并不改变。
MAC VLAN授权 携带 的情况下：
VLAN Tag若用户从 Access 类型的端口接入，则不支持下发带 Tag 的 VLAN。
•若用户从 Trunk 类型的端口接入，则设备允许授权下发的 VLAN 以携带 Tag 的方式通过该端
•口，但是不会修改该端口的缺省 VLAN。
若用户从 类型的端口接入，则设备允许授权下发的 以携带 的方式通过该端
• Hybrid VLAN Tag口，但是不会修改该端口的缺省 VLAN。
授权 VLAN 并不影响端口的配置。但是，授权 VLAN 的优先级高于端口用户配置的 VLAN，即通过认证后起作用的 VLAN 是授权 VLAN，端口用户配置的 VLAN 在用户下线后生效。
• 对于 Hybrid 端口，如果认证用户的报文携带 VLAN Tag，则应通过 port hybrid vlan 命令配置该端口在转发指定的 VLAN报文时携带 VLAN Tag；如果认证用户的报文不携带 VLAN Tag，则应配置该端口在转发指定的 报文时不携带 Tag。否则，当服务器没有授权下发VLAN VLAN VLAN 时，用户虽然可以通过认证但不能访问网络。
• 在授权 VLAN 未携带 Tag 的情况下，只有开启了 MAC VLAN 功能的端口上才允许给不同的用户 MAC 授权不同的 VLAN。如果没有开启 MAC VLAN 功能，授权给所有用户的 VLAN 必须相同，否则仅第一个通过认证的用户可以成功上线。
• 在授权 VLAN 携带 Tag 的情况下，无论是否开启了 MAC VLAN 功能，设备都会给不同的用户授权不同的 VLAN。

###### 5. Guest VLAN

MAC 地址认证的 Guest VLAN 功能允许用户在认证失败的情况下访问某一特定 VLAN 中的资源，比如获取客户端软件，升级客户端或执行其他一些用户升级程序。这个 VLAN 称之为 Guest VLAN。
需要注意的是，这里的认证失败是认证服务器因某种原因明确拒绝用户认证通过，比如用户密码错误，而不是认证超时或网络连接等原因造成的认证失败。
如果接入用户的端口上配置了 Guest VLAN，则该端口上认证失败的用户会被加入 Guest VLAN，且设备允许 Guest VLAN 以不携带 Tag 的方式通过该端口，即该用户被授权访问 Guest VLAN 里的资源。用户被加入 之后，设备将以指定的时间间隔对该用户发起重新认证，若Guest VLAN Guest

VLAN 中的用户再次发起认证未成功，则该用户将仍然处于 Guest VLAN 内；若认证成功，则会根据 服务器/接入设备是否下发授权 决定是否将用户加入到下发的授权 中，在AAA VLAN VLAN AAA服务器/接入设备未下发授权 VLAN 的情况下，用户回到缺省 VLAN 中。若 Guest VLAN 中的用户再次发起认证时，认证服务器不可达，则该用户将仍然处于 Guest VLAN 内，并不会加入到 Critical中。
VLAN

###### 6. Critical VLAN

MAC 地址认证 Critical VLAN 功能允许用户在所有认证服务器都不可达的情况下访问某一特定VLAN 中的资源，这个 VLAN 称之为 Critical VLAN。在端口上配置 Critical VLAN 后，若该端口上有用户认证时，所有认证服务器都不可达，则端口将允许 Critical VLAN 通过，用户将被授权访问里的资源。已经加入 的端口上有用户发起认证时，如果所有认证服务Critical VLAN Critical VLAN器不可达，则端口仍然在 Critical VLAN 内；如果服务器可达且认证失败，且端口配置了 Guest VLAN，则该端口将会加入 Guest VLAN，否则回到缺省 VLAN 中；如果服务器可达且认证成功，则会根据服务器是否下发授权 决定是否将用户加入到下发的授权 中，在 服务器未下AAA VLAN VLAN AAA发授权 VLAN 的情况下，用户回到缺省 VLAN 中。

###### 7. Critical Voice Vlan

MAC 地址认证的 Critical Voice VLAN 功能允许语音用户进行 MAC 地址认证时，若采用的 ISP 域中的所有认证服务器都不可达，则访问端口上已配置的 Voice VLAN 中的资源，这个 VLAN 也被称为地址认证的 VLAN。已经加入 的端口上有用户发起认证时，MAC Critical Voice Critical Voice VLAN如果所有认证服务器不可达，则端口仍然在 Critical Voice VLAN 内；如果服务器可达且认证失败，且端口配置了 Guest VLAN，则该端口将会加入 Guest VLAN，否则回到缺省 VLAN 中；如果服务器可达且认证成功，则会根据 AAA 服务器是否下发授权 VLAN 决定是否将用户加入到下发的授权中，在 服务器未下发授权 的情况下，用户回到缺省 中。
VLAN AAA VLAN VLAN

##### 1.1.4 MAC地址认证支持ACL下发

由远程 AAA 服务器/接入设备下发给用户的 ACL 被称为授权 ACL，它为用户访问网络提供了良好的过滤条件设置功能。当用户通过 MAC 地址认证后，如果远程 AAA 服务器/接入设备上为用户指定了授权 ACL，则设备会根据下发的授权 ACL 对用户所在端口的数据流进行控制，与授权 ACL 规则匹配的流量，将按照规则中指定的 permit 或 deny 动作进行处理。为使下发的授权 ACL 生效，需要提前在设备上配置相应的 ACL 规则。而且在用户访问网络的过程中，可以通过改变远程 AAA 服务器 设备本地的授权 设置来改变用户的访问权限。
/ ACL MAC 地址认证可成功授权的 ACL 类型为基本 ACL（ACL 编号为 2000～2999）和高级 ACL（ACL编号为 3000～3999）。但当下发的 ACL 不存在、未配置 ACL 规则或 ACL 规则配置了 counting、established、fragment 或 logging 参数时，授权 ACL 不生效。有关 ACL 规则的具体介绍，请参见“ACL 和 QoS 命令参考”中的“ACL”。

##### 1.1.5 MAC地址认证支持User Profile下发

从认证服务器（远程或本地）下发的 被称为授权 Profile，它为用户访问网络提供User Profile User了良好的过滤条件设置功能。MAC 地址认证支持认证服务器授权下发 User Profile 功能，即当用户通过 MAC 地址认证后，如果认证服务器上配置了授权 User Profile，则设备会根据服务器下发的授权 User Profile 对用户所在端口的数据流进行控制。为使下发的授权 User Profile 生效，需要提前在设备上配置相应的 User Profile。而且在用户访问网络的过程中，可以通过改变服务器的授权 User Profile 名称或者设备对应的 User Profile 配置来改变用户的访问权限。

##### 1.1.6 MAC地址认证支持URL重定向功能

用户通过 地址认证后，设备会根据 服务器下发的重定向 属性，将用户的MAC RADIUS URL HTTP或 HTTPS 请求重定向到指定的 Web 认证页面。Web 认证通过后，RADIUS 服务器记录用户的 MAC地址信息，并通过 DM 报文强制 Web 用户下线。此后该用户再次进行 MAC 地址认证，由于 RADIUS服务器上已记录该用户和其 MAC 地址的对应信息，用户可以成功上线。
若需要对 MAC 地址认证用户的 HTTPS 请求进行重定向，需要在设备上配置对 HTTPS 报文进行重定向的内部侦听端口号，具体配置请参见“三层技术-IP 业务配置指导”中的“HTTP 重定向”。

##### 1.1.7 MAC地址认证支持下发CAR属性

地址认证支持 属性下发后，设备可以对 地址认证上线用户访问网络资源的流量与MAC CAR MAC速率进行控制。当用户通过 MAC 地址认证后，如果 RADIUS 服务器通过扩展属性字段下发授权 CAR属性给该用户，则设备会根据服务器下发的授权 CAR 属性对用户所在端口的数据流进行限速。
RADIUS 扩展属性的详细介绍请参见“安全配置指导”中的“AAA”。
CAR 属性具体分为如下几种：
Input-Peak-Rate：上行峰值速率，单位 bps。用于限制端口上接收报文的峰值速率。
•
• Input-Average-Rate：上行平均速率，单位 bps。用于限制该端口上接收报文的平均速率。
• Output-Peak-Rate：下行峰值速率，单位 bps。用于限制端口上发送报文的峰值速率。
• Output-Average-Rate：下行平均速率，单位 bps。用于限制该端口上发送报文的平均速率。
如果未授权 Input-Peak-Rate 或 Output-Peak-Rate，则表示对用户报文进行单速率流量监管，否则进行双速率流量监管。流量监管的详细介绍请参见“ACL 和 QoS 配置指导”中的“QoS”。

##### 1.1.8 MAC地址认证支持下发黑洞MAC

用户通过 MAC 地址认证后，如果收到服务器通过 COA 报文授权当前用户 MAC 地址为黑洞 MAC，设 备 将 强 制 该 MAC 地 址 认 证 用 户 下 线 ， 并 添 加 该 用 户 为 静 默 用 户 （ 可 通 过 display mac-authentication 查看），静默时间固定为 10 分钟。在静默时间内，设备不对来自该 MAC地址用户的报文进行认证处理，直接丢弃。静默期后，如果设备再次收到该用户的报文，则可以对其进行认证处理。

##### 1.1.9 MAC地址重认证

地址重认证是指设备周期性对端口上在线的 地址认证用户发起重认证，以检测用户连接MAC MAC状态的变化、确保用户的正常在线，并及时更新服务器下发的授权属性（例如 ACL、VLAN 等）。
认证服务器可以通过下发 RADIUS 属性（session-timeout、Termination-action）来指定用户会话超时时长以及会话中止的动作类型。认证服务器上如何下发以上 RADIUS 属性的具体配置以及是否可以下发重认证周期的情况与服务器类型有关，请参考具体的认证服务器实现。
设备作为 RADIUS DAE 服务器，认证服务器作为 RADIUS DAE 客户端时，后者可以通过 COA（Change Authorization）Messages 向用户下发重认证属性，这种情况下，无论设备上是否开of启了周期性重认证功能，端口都会立即对该用户发起重认证。关于 RADIUS DAE 服务器的详细内容，请参见“安全配置指导”中的“AAA”。
MAC 地址认证用户认证通过后，端口对用户的重认证功能具体实现如下：
• 当认证服务器下发了用户会话超时时长，且指定的会话中止的动作类型为要求用户进行重认证时，则无论设备上是否开启周期性重认证功能，端口均会在用户会话超时时长到达后对该用户进行重认证；
当认证服务器下发了用户会话超时时长，且指定的会话中止的动作类型为要求用户下线时：
•若设备上开启了周期性重认证功能，且设备上配置的重认证定时器值小于用户会话超时时(cid:123)
长，则端口会以重认证定时器的值为周期向该端口在线 MAC 地址认证用户发起重认证；
若设备上配置的重认证定时器值大于等于用户会话超时时长，则端口会在用户会话超时时长到达后强制该用户下线；
若设备上未开启周期性重认证功能，则端口会在用户会话超时时长到达后强制该用户下线。
(cid:123)
当认证服务器未下发用户会话超时时长时，是否对用户进行重认证，由设备上配置的重认证功
•能决定。
对于已在线的 地址认证用户，要等当前重认证周期结束并且认证通过后才会按新配置的
• MAC周期进行后续的重认证。
• MAC 地址重认证过程中，重认证服务器不可达时端口上的 MAC 地址认证用户状态由端口上的配置决定。在网络连通状况短时间内不良的情况下，合法用户是否会因为服务器不可达而被强制下线，需要结合实际的网络状态来调整。若配置为保持用户在线，当服务器在短时间内恢复可达，则可以避免用户频繁上下线；若配置为强制下线，当服务器可达性在短时间内不可恢复，则可避免用户在线状态长时间与实际不符。
• 在用户名不改变的情况下，端口允许重认证前后服务器向该用户下发不同的 VLAN。

#### 1.2 MAC地址认证配置限制和指导

当端口上配置的 地址认证的 VLAN、Critical 中存在用户时，不允许切换该
• MAC Guest VLAN端口的链路类型。
• 仅支持在二层以太网接口上配置 MAC 地址认证功能，且不支持在二层聚合组的成员端口上开启 MAC 地址认证功能。
• 若配置的静态 MAC 或者当前认证通过的 MAC 地址与静默 MAC 相同，则 MAC 地址认证失败后的 MAC 静默功能将会失效。

##### 2. 配置步骤

#### 1.3 MAC地址认证配置任务简介

MAC 地址认证配置任务如下：
(1) 开启MAC地址认证
(2) 配置 MAC 地址认证基本功能指定MAC地址认证用户使用的认证域(cid:123)
配置MAC地址认证用户的帐号格式(cid:123)
（可选）配置MAC地址认证定时器(cid:123)
（可选）配置 地址认证授权 功能
(3) MAC VLAN配置MAC地址认证的Guest VLAN (cid:123)
配置MAC地址认证的Critical VLAN (cid:123)
配置MAC地址认证的Critical Voice VLAN (cid:123)
(4) （可选）配置 MAC 地址认证其它功能开启MAC地址认证下线检测功能(cid:123)
配置端口上最多允许同时接入的MAC地址认证用户数(cid:123)
配置端口工作在MAC地址认证的多VLAN模式(cid:123)
允许用户在相同端口的不同 VLAN 间迁移时无须重认证。
配置MAC地址认证延迟功能(cid:123)
配置MAC地址认证的重认证(cid:123)
配置MAC地址认证请求中携带用户IP地址(cid:123)
配置端口MAC地址认证和 802.1X认证并行处理功能(cid:123)
配置MAC地址认证接入用户日志信息功能(cid:123)

#### 1.4 MAC地址认证配置准备

• 配置 MAC 地址认证之前，请保证端口安全功能关闭，具体配置请参见“安全配置指导”中的
“端口安全”。
• 配置 MAC 地址认证之前，需完成配置 ISP 域和认证方式，具体配置请参见“安全配置指导”
中的“ AAA ”。
若采用本地认证方式，还需创建本地用户并设置其密码，且本地用户的服务类型应设置为
(cid:123)
lan-access。
若采用远程 RADIUS 认证方式，需要确保设备与 RADIUS 服务器之间的路由可达，并添加
(cid:123)
地址认证用户帐号。
MAC

#### 1.5 开启MAC地址认证

##### 1. 配置限制和指导

只有全局和端口的 MAC 地址认证均开启后，MAC 地址认证配置才能在端口上生效。
配置步骤
2.
(1) 进入系统视图。

system-view
(2) 开启全局 MAC 地址认证。
mac-authentication缺省情况下，全局的 MAC 地址认证处于关闭状态。
(3) 进入接口视图。
interface interface-type interface-number
(4) 开启端口 MAC 地址认证。
mac-authentication缺省情况下，端口的 MAC 地址认证处于关闭状态。

#### 1.6 指定MAC地址认证用户使用的认证域

##### 1. 功能简介

为了便于接入设备的管理员更为灵活地部署用户的接入策略，设备支持指定 MAC 地址认证用户使用的认证域，可以通过以下两种配置实现：
在系统视图下指定一个认证域，该认证域对所有开启了 地址认证的端口生效。
• MAC在接口视图下指定该端口的认证域，不同的端口可以指定不同的认证域。
•端口上接入的 地址认证用户将按照如下顺序选择认证域：端口上指定的认证域 系统视图下MAC >指定的认证域 > 系统缺省的认证域。关于认证域的相关介绍请参见“安全配置指导”中的“AAA”。

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 指定 MAC 地址认证用户使用的认证域。
配置全局 MAC 地址认证用户使用的认证域。
(cid:123)
mac-authentication domain domain-name
配置接口上 MAC 地址认证用户使用的认证域。
(cid:123)
interface interface-type interface-number
mac-authentication domain domain-name
缺省情况下，未指定 地址认证用户使用的认证域，使用系统缺省的认证域。
MAC

#### 1.7 配置MAC地址认证用户的帐号格式

(1) 进入系统视图。
system-view
(2) 配置 MAC 地址认证用户的帐号格式。
配置 MAC 地址帐号。
(cid:123)
mac-authentication user-name-format mac-address [ { with-hyphen |
without-hyphen } [ lowercase | uppercase ] ]
配置固定用户名帐号。
(cid:123)

mac-authentication user-name-format fixed [ account name ] [ password { cipher | simple } string ]缺省情况下，使用用户的 地址作为用户名与密码，其中字母为小写，且不带连字符“-”MAC

#### 1.8 配置MAC地址认证定时器

##### 1. 功能简介

可配置的 MAC 地址认证定时器包括以下几种：
• 下线检测定时器（offline-detect）：用来设置用户空闲超时的时间间隔。若设备在一个下线检测定时器间隔之内，没有收到某在线用户的报文，将切断该用户的连接，同时通知 RADIUS服务器停止对其计费。
静默定时器（quiet）：用来设置用户认证失败以后，设备停止对其提供认证服务的时间间隔。
•在静默期间，设备不对来自认证失败用户的报文进行认证处理，直接丢弃。静默期后，如果设备再次收到该用户的报文，则依然可以对其进行认证处理。
• 服务器超时定时器（ server-timeout ）：用来设置设备同 RADIUS 服务器的连接超时时间。
在用户的认证过程中，如果到服务器超时定时器超时时设备一直没有收到 RADIUS 服务器的应答，则 地址认证失败。
MAC

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置 MAC 地址认证定时器。
mac-authentication timer { offline-detect offline-detect-value | quiet
quiet-value | server-timeout server-timeout-value }
缺省情况下，下线检测定时器为 300 秒，静默定时器为 60 秒，服务器超时定时器取值为 100
秒。

#### 1.9 配置MAC地址认证的Guest VLAN

##### 1. 配置限制和指导

端口上生成的 地址认证 表项会覆盖已生成的阻塞 表项。开启了端口
• MAC Guest VLAN MAC安全入侵检测的端口关闭功能时，若端口因检测到非法报文被关闭，则 MAC 地址认证的 Guest VLAN 功能不生效。关于阻塞 MAC 表项和端口的入侵检测功能的具体介绍请参见“安全配置指导”中的“端口安全”。
如果某个 VLAN 被指定为 Super VLAN，则该 VLAN 不能被指定为某个端口的 MAC 地址认证
•的 VLAN；同样，如果某个 被指定为某个端口的 地址认证的 VLAN，Guest VLAN MAC Guest则该 VLAN 不能被指定为 Super VLAN。关于 Super VLAN 的详细内容请参见“二层技术-以太网交换配置指导”中的“Super VLAN”。
• MAC 地址认证 Guest VLAN 功能的优先级高于 MAC 地址认证的静默 MAC 功能，即认证失败的用户可访问指定的 Guest VLAN 中的资源，且该用户的 MAC 地址不会被加入静默 MAC。

##### 2. 配置准备

配置 MAC 地址认证的 Guest VLAN 之前，需要进行以下配置准备，具体配置方法可参见“二层技术-以太网交换”中的“VLAN 配置”：
• 创建需要配置为 Guest VLAN 的 VLAN。
• 配置端口类型为 Hybrid，并建议将指定的 Guest VLAN 修改为不携带 Tag 的方式。
• 通过 mac-vlan enable 命令开启端口上的 MAC VLAN 功能。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置端口的 MAC 地址认证 Guest VLAN。
mac-authentication guest-vlan guest-vlan-id
缺省情况下，未配置 MAC 地址认证的 Guest VLAN。
不同的端口可以指定不同的 MAC 地址认证 Guest VLAN，一个端口最多只能指定一个 MAC
地址认证 Guest VLAN。
(4) 配置设备对 MAC 地址认证 Guest VLAN 中的用户进行重新认证的时间间隔。
mac-authentication guest-vlan auth-period period-value
缺省情况下，设备对 Guest VLAN 中的用户进行重新认证的时间间隔为 30 秒。

#### 1.10 配置MAC地址认证的Critical VLAN

##### 1. 配置限制和指导

端口上生成的 地址认证 表项会覆盖已生成的阻塞 表项。开启了端口
• MAC Critical VLAN MAC安全入侵检测的端口关闭功能时，MAC 地址认证的 Critical VLAN 功能不生效。关于阻塞 MAC表项和端口的入侵检测功能的具体介绍请参见“安全配置指导”中的“端口安全”。
• 如果某个 VLAN 被指定为 Super VLAN，则该 VLAN 不能被指定为某个端口的 MAC 地址认证的 Critical VLAN；同样，如果某个 VLAN被指定为某个端口的 MAC地址认证的 Critical VLAN，则该 不能被指定为 。关于 的详细内容请参见“二层技术 以VLAN Super VLAN Super VLAN -太网交换配置指导”中的“Super VLAN”。
• 当端口上的用户加入指定的 Critical VLAN 后，该用户的 MAC 地址不会被加入静默 MAC。
• 当处于 Guest VLAN 的用户再次发起认证时，如果认证服务器不可达，则该用户仍然留在该Guest VLAN 中，不会离开当前的 VLAN 而加入 Critical VLAN。

##### 2. 配置准备

配置 MAC 地址认证的 Critical VLAN 之前，需要进行以下配置准备：
• 创建需要配置为 Critical VLAN 的 VLAN 。
• 配置端口类型为 Hybrid，且建议将指定的 Critical VLAN 修改为不携带 Tag 的方式。
• 通过 mac-vlan enable 命令开启端口上的 MAC VLAN 功能。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置端口的 Critical VLAN。
mac-authentication critical vlan critical-vlan-id
缺省情况下，未配置 MAC 认证的 Critical VLAN。
不同的端口可以指定不同的 地址认证 VLAN，一个端口最多只能指定一个
MAC Critical MAC
地址认证 Critical VLAN。

#### 1.11 配置MAC地址认证的Critical Voice VLAN

##### 1. 配置准备

配置 MAC 地址认证 Critical Voice VLAN 之前，需要进行以下配置准备：
• 全局和端口的 LLDP（Link Layer Discovery Protocol，链路层发现协议）已经开启，设备通过来判断用户是否为语音用户。有关 功能的详细介绍请参见“二层技术-以太网交LLDP LLDP换配置指导”中的“LLDP”。
• 端口的语音 VLAN 功能已经开启。有关语音 VLAN 的详细介绍请参见“二层技术-以太网交换配置指导”中的“VLAN”。

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置指定端口的 Critical VLAN。
mac-authentication critical-voice-vlan
缺省情况下，端口下 MAC 地址认证的 Critical Voice VLAN 功能处于关闭状态。

#### 1.12 开启MAC地址认证下线检测功能

##### 1. 功能简介

开启端口的 MAC 地址认证下线检测功能后，若设备在一个下线检测定时器间隔之内，未收到此端口下某在线用户的报文，则将切断该用户的连接，同时通知 服务器停止对此用户进行计费。
RADIUS关闭端口的 地址认证下线检测功能后，设备将不会对在线用户的状态进行检测。
MAC

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。

##### 1. 功能简介

##### 2. 配置步骤

interface interface-type interface-number
(3) 开启端口的 MAC 地址认证下线检测功能。
mac-authentication offline-detect enable缺省情况下，端口的 MAC 地址认证下线检测功能处于开启状态。

#### 1.13 配置端口上最多允许同时接入的MAC地址认证用户数

##### 1. 功能简介

由于系统资源有限，如果当前端口下接入的用户过多，接入用户之间会发生资源的争用，因此适当地配置该值可以使端口上已经接入的用户获得可靠的性能保障。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置端口上最多允许同时接入的 MAC 地址认证用户数。
mac-authentication max-user max-number缺省情况下，端口上最多允许同时接入的 MAC 地址认证用户数为 4294967295。

#### 1.14 配置端口工作在MAC地址认证的多VLAN模式

功能简介
1.
MAC 地址认证的端口可以工作在单 VLAN 模式或多 VLAN 模式。端口工作在单 VLAN 模式时，在账号已通过 地址认证，且没有被下发授权 情况下，如果此账号在相同端口上的不同MAC VLAN VLAN 再次接入，则设备将让原账号下线，使得该账号能够在新的 VLAN 内重新开始认证。如果已通过 MAC 地址认证的账号被下发了授权 VLAN，则此账号在属于不同 VLAN 的相同端口再次接入时不会被强制下线。端口工作在多 VLAN 模式时，如果相同 MAC 地址的账号在相同端口上的不同再次接入，设备将能够允许账号的流量在新的 内通过，且允许该用户的报文无需重新VLAN VLAN认证而在多个 VLAN 中转发。
对于接入 IP 电话类用户的端口，指定端口工作在 MAC 地址认证的多 VLAN 模式或为 IP 电话类用户授权 VLAN，可避免 IP 电话终端的报文所携带的 VLAN tag 发生变化后，因用户流量需要重新认证带来语音报文传输质量受干扰的问题。

##### 2. 配置步骤

进入系统视图。
(1)
system-view进入接口视图。
(2)
interface interface-type interface-number配置端口工作在 地址认证的多 模式。
(3) MAC VLAN mac-authentication host-mode multi-vlan缺省情况下，端口工作在 MAC 地址认证的单 VLAN 模式。

#### 1.15 配置MAC地址认证延迟功能

##### 1. 功能简介

端口同时开启了 地址认证和 认证的情况下，某些组网环境中希望设备对用户报文先进MAC 802.1X行 802.1X 认证。例如，有些客户端在发送 802.1X 认证请求报文之前，就已经向设备发送了其它报文，比如 DHCP 报文，因而触发了并不期望的 MAC 地址认证。这种情况下，可以开启端口的 MAC地址认证延时功能。开启该功能后，端口就不会在收到用户报文时立即触发 MAC 地址认证，而是会等待一定的延迟时间，若在此期间该用户一直未进行 认证或未成功通过 认证，则
802.1X 802.1X延迟时间超时后端口会对之前收到的用户报文进行 MAC 地址认证。

##### 2. 配置限制和指导

开 启 了 MAC 地 址 认 证 延 迟 功 能 的 端 口 上 不 建 议 同 时 配 置 端 口 安 全 的 模 式 为mac-else-userlogin-secure 或 mac-else-userlogin-secure-ext，否则 MAC 地址认证延迟功能不生效。端口安全模式的具体配置请参见“安全配置指导”中的“端口安全”。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 开启 MAC 地址认证延迟功能，并指定延迟时间。
mac-authentication timer auth-delay time
缺省情况下，MAC 地址认证延迟功能处于关闭状态。

#### 1.16 配置MAC地址认证的重认证

##### 1. 配置限制和指导

• 对 MAC 地址认证用户进行重认证时，设备将按照如下由高到低的顺序为其选择重认证时间间
隔：服务器下发的重认证时间间隔、接口视图下配置的周期性重认证定时器的值、系统视图下
配置的周期性重认证定时器的值、设备缺省的周期性重认证定时器的值。
修改设备上配置的认证域或 地址认证用户的帐号格式，都不会影响在线用户的重认证，
• MAC
只对配置之后新上线的用户生效。

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 在系统视图或接口视图下配置周期性重认证定时器。
系统视图下配置周期性重认证定时器。
(cid:123)
mac-authentication timer reauth-period reauth-period-value
缺省情况下，周期性重认证定时器的值为 3600 秒。
依次执行以下命令在接口视图下配置周期性重认证定时器。
(cid:123)
interface interface-type interface-number

mac-authentication timer reauth-period reauth-period-value quit缺省情况下，端口上未配置 MAC 地址周期性重认证定时器，端口使用系统视图下的 MAC地址周期性重认证定时器的取值。
进入接口视图。
(3)
interface interface-type interface-number
(4) 开启周期性重认证功能mac-authentication re-authenticate缺省情况下，周期性重认证功能关闭。
(5) （可选）配置重认证服务器不可达时端口上的 MAC 地址认证用户保持在线状态。
mac-authentication re-authenticate server-unreachable keep-online缺省情况下，端口上的 MAC 地址在线用户重认证时，若认证服务器不可达，则用户会被强制下线。

#### 1.17 配置MAC地址认证请求中携带用户IP地址

##### 1. 功能简介

终端用户接入网络时，如果擅自修改自己的 IP 地址，则整个网络环境中可能会出现 IP 地址冲突等问题。
为了解决以上问题，管理员可以在端口上开启 MAC 地址认证请求中携带用户 IP 地址的功能，用户在进行 MAC 地址认证时，设备会把用户的 IP 地址上传到 iMC 服务器。然后 iMC 服务器会把认证用户的 IP地址和MAC地址与服务器上已经存在的 IP与 MAC的绑定表项进行匹配，如果匹配成功，则该用户 MAC 地址认证成功；否则，MAC 地址认证失败。
H3C 的 iMC 服务器上 IP 与 MAC 地址信息绑定表项的生成方式如下：
• 如果在 iMC 服务器上创建用户时手工指定了用户的 IP 地址和 MAC 地址信息，则服务器使用手工指定的 IP 和 MAC 信息生成该用户的 IP 与 MAC 地址的绑定表项。
• 如果在 iMC 服务器上创建用户时未手工指定用户的 IP 地址和 MAC 地址信息，则服务器使用用户初次进行 MAC 地址认证时使用的 IP 地址和 MAC 地址生成该用户的 IP 与 MAC 地址的绑定表项。

##### 2. 配置限制和指导

• 在开启了 MAC 地址认证的端口上，不建议将本命令与 mac-authentication
guest-vlan 命令同时配置；否则，加入 Guest VLAN的用户无法再次发起 MAC地址认证，
用户会一直停留在 Guest VLAN 中。

##### 3. 配置步骤

进入系统视图。
(1)
system-view进入接口视图。
(2)
interface interface-type interface-number配置 地址认证请求中携带用户 地址。
(3) MAC IP

mac-authentication carry user-ip缺省情况下，MAC 地址认证请求中不携带用户 IP 地址。

#### 1.18 配置端口MAC地址认证和802.1X认证并行处理功能

##### 1. 功能简介

端口采用802.1X和MAC地址组合认证，且端口所连接的用户有不能主动发送EAP报文触发802.1X认证的情况下，如果端口配置了 802.1X 单播触发功能，则端口收到源 MAC 地址未知的报文，会先进行 802.1X 认证处理，完成后再进行 MAC 地址认证处理。
配置端口的 MAC 地址认证和 802.1X 认证并行处理功能后，在上述情况下，端口收到源 MAC 地址未知的报文，会向该 地址单播发送 帧来触发 认证，但不等待MAC EAP-Request 802.1X 802.1X认证处理完成，就同时进行 MAC 地址认证的处理。
在某些组网环境下，例如用户不希望端口先被加入 802.1X 的 Guest VLAN 中，接收到源 MAC 地址未知的报文后，先触发 MAC 地址认证，认证成功后端口直接加入 MAC 地址认证的授权 VLAN 中，那么需要配置 MAC 地址认证和 802.1X 认证并行处理功能和端口延迟加入 802.1X Guest VLAN 功能。关于端口延迟加入 功能的详细介绍，请参见“安全配置指导”中的“802.1X”。
802.1X Guest VLAN

##### 2. 配置限制和指导

端口采用 802.1X 和 MAC 地址组合认证功能适用于如下情况：
• 端口上同时开启了 802.1X 和 MAC 地址认证功能，并配置了 802.1X 认证的端口的接入控制方式为 macbased。
• 开启了端口安全功能，并配置了端口安全模式为 userlogin-secure-or-mac 或userlogin-secure-or-mac-ext。端口安全模式的具体配置请参见“安全命令参考”中的“端口安全”。
为保证 地址认证和 认证并行处理功能的正常使用，不建议配置端口的 地址认证MAC 802.1X MAC延迟功能，否则端口触发 802.1X 认证后，仍会等待一定的延迟后再进行 MAC 地址认证。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置端口的 MAC 地址认证和 802.1X 认证并行处理功能。
mac-authentication parallel-with-dot1x
缺省情况下，端口在收到源 MAC 地址未知的报文触发认证时，按照 802.1X 完成后再进行
MAC 地址认证的顺序进行处理。

#### 1.19 配置MAC地址认证接入用户日志信息功能

##### 1. 功能简介

MAC 地址认证接入用户日志信息是为了满足网络管理员维护的需要，对 MAC 地址认证用户的接入信息进行记录。设备生成的 MAC 地址认证接入用户日志信息会交给信息中心模块处理，信息中心

##### 3. 配置步骤

模块的配置将决定日志信息的发送规则和发送方向。关于信息中心的详细描述请参见“网络管理和监控配置指导”中的“信息中心”。

##### 2. 配置限制和指导

为了防止设备输出过多的 MAC 地址认证接入用户日志信息，一般情况下建议关闭此功能。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 开启 MAC 地址认证接入用户日志信息功能。
mac-authentication access-user log enable [ failed-login | logoff | successful-login ] *缺省情况下，MAC 地址认证接入用户日志信息功能处于关闭状态。
配置本命令时，如果未指定任何参数，将同时开启所有参数对应的日志功能。

#### 1.20 MAC地址认证的显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 MAC 地址认证的运行情况，通过查看显示信息验证配置的效果。
在用户视图下，执行 reset 命令可以清除相关统计信息。
表1-1 MAC 地址认证的显示和维护操作 命令display mac-authentication [ interface显示MAC地址认证的相关信息interface-type interface-number ] display mac-authentication connection [ open ] [ interface interface-type interface-number | slot显示MAC地址认证连接信息slot-number | user-mac mac-addr | user-name user-name ] display mac-authentication mac-address显示指定类型的VLAN中的MAC地址认{ critical-vlan | guest-vlan } [ interface证用户的MAC地址信息interface-type interface-number ] reset mac-authentication statistics [ interface清除MAC地址认证的统计信息interface-type interface-number ] reset mac-authentication critical vlan interface清除Critical VLAN内MAC地址认证用户 interface-type interface-number [ mac-address mac-address ] reset mac-authentication critical-voice-vlan清除Critical Voice VLAN内MAC地址认interface interface-type interface-number证用户[ mac-address mac-address ] reset mac-authentication guest-vlan interface清除Guest VLAN内MAC地址认证用户 interface-type interface-number [ mac-address mac-address ]

###### 2. 组网图

#### 1.21 MAC地址认证典型配置举例

##### 1.21.1 本地MAC地址认证配置举例

###### 1. 组网需求

如 图 1-3 所示，某子网的用户主机与设备的端口Ten-GigabitEthernet1/0/1 相连接。
设备的管理者希望在端口 上对用户接入进行 地址认证，以控
• Ten-GigabitEthernet1/0/1 MAC制它们对 Internet 的访问。
• 要求设备每隔 180 秒就对用户是否下线进行检测；并且当用户认证失败时，需等待 180 秒后才能对用户再次发起认证。
• 所有用户都属于 ISP 域 bbb，认证时使用本地认证的方式。
• 使用用户的 MAC 地址作用户名和密码，其中 MAC 地址带连字符、字母小写。
组网图
2.
图1-3 启动 MAC 地址认证对接入用户进行本地认证

###### 3. 配置步骤

添加网络接入类本地接入用户。本例中添加 的本地用户，用户名和密码均为 的\# Host A Host A MAC地址 00-e0-fc-12-34-56，服务类型为 lan-access。
<Device> system-view [Device] local-user 00-e0-fc-12-34-56 class network [Device-luser-network-00-e0-fc-12-34-56] password simple 00-e0-fc-12-34-56 [Device-luser-network-00-e0-fc-12-34-56] service-type lan-access [Device-luser-network-00-e0-fc-12-34-56] quit \# 配置 ISP 域，使用本地认证方法。
[Device] domain bbb [Device-isp-bbb] authentication lan-access local [Device-isp-bbb] quit \# 开启端口 Ten-GigabitEthernet1/0/1 的 MAC 地址认证。
[Device] interface ten-gigabitethernet 1/0/1 [Device-Ten-GigabitEthernet1/0/1] mac-authentication [Device-Ten-GigabitEthernet1/0/1] quit \# 配置 MAC 地址认证用户所使用的 ISP 域。
[Device] mac-authentication domain bbb配置 地址认证的定时器。
\# MAC [Device] mac-authentication timer offline-detect 180 [Device] mac-authentication timer quiet 180

###### 4. 验证配置

\# 配置 MAC 地址认证用户的帐号格式：使用带连字符的 MAC 地址作为用户名与密码，其中字母小写。
[Device] mac-authentication user-name-format mac-address with-hyphen lowercase \# 开启全局 MAC 地址认证。
[Device] mac-authentication验证配置
4.
\# 当用户接入端口 Ten-GigabitEthernet1/0/1 之后，可以通过如下显示信息看到 Host A 成功通过认证，处于上线状态，Host 没有通过认证，它的 地址被加入静默 列表。
B MAC MAC <Device> display mac-authentication Global MAC authentication parameters:
MAC authentication : Enabled User name format : MAC address in lowercase(xx-xx-xx-xx-xx-xx)
Username : mac Password : Not configured Offline detect period : 180 s Quiet period : 180 s Server timeout : 100 s Reauth period : 3600 s Authentication domain : bbb Online MAC-auth users : 1 Silent MAC users:
MAC address VLAN ID From port Port index 00e0-fc11-1111 8 XGE1/0/1 1 Ten-GigabitEthernet1/0/1 is link-up MAC authentication : Enabled Carry User-IP : Disabled Authentication domain : Not configured Auth-delay timer : Disabled Periodic reauth : Disabled Re-auth server-unreachable : Logoff Guest VLAN : Not configured Guest VLAN auth-period : 30 s Critical VLAN : Not configured Critical voice VLAN : Disabled Host mode : Single VLAN Offline detection : Enabled Authentication order : Default Guest VSI : Not configured Guest VSI auth-period : 30 s Critical VSI : Not configured Auto-tag feature : Disabled VLAN tag configuration ignoring : Disabled Max online users : 4294967295 Authentication attempts : successful 1, failed 0

Current online users : 1 MAC address Auth state 00e0-fc12-3456 Authenticated

##### 1.21.2 使用RADIUS服务器进行MAC地址认证配置举例

###### 1. 组网需求

如 图 所示，用户主机Host通过端口Ten-GigabitEthernet1/0/1 连接到设备上，设备通过RADIUS 1-4服务器对用户进行认证、授权和计费。
• 设备的管理者希望在端口 Ten-GigabitEthernet1/0/1 上对用户接入进行 MAC 地址认证，以控制其对 Internet 的访问。
• 要求设备每隔 180 秒就对用户是否下线进行检测；并且当用户认证失败时，需等待 180 秒后才能对用户再次发起认证。
• 所有用户都属于域 2000，认证时采用固定用户名帐号，用户名为 aaa，密码为 123456。

###### 2. 组网图

图1-4 启动 地址认证对接入用户进行 认证MAC RADIUS

###### 3. 配置步骤

配置 服务器，添加接入用户帐户：用户名为 aaa，密码为 123456，并保证用户的认
(1) RADIUS证/授权/计费功能正常运行（略）
(2) 配置使用 RADIUS 服务器进行 MAC 地址认证\# 配置 RADIUS 方案。
<Device> system-view [Device] radius scheme 2000 [Device-radius-2000] primary authentication 10.1.1.1 1812 [Device-radius-2000] primary accounting 10.1.1.2 1813 [Device-radius-2000] key authentication simple abc [Device-radius-2000] key accounting simple abc [Device-radius-2000] user-name-format without-domain [Device-radius-2000] quit \# 配置 ISP 域的 AAA 方法。
[Device] domain bbb [Device-isp-bbb] authentication default radius-scheme 2000

[Device-isp-bbb] authorization default radius-scheme 2000 [Device-isp-bbb] accounting default radius-scheme 2000 [Device-isp-bbb] quit \# 开启端口 Ten-GigabitEthernet1/0/1 的 MAC 地址认证。
[Device] interface ten-gigabitethernet 1/0/1 [Device-Ten-GigabitEthernet1/0/1] mac-authentication [Device-Ten-GigabitEthernet1/0/1] quit \# 配置 MAC 地址认证用户所使用的 ISP 域。
[Device] mac-authentication domain bbb \# 配置 MAC 地址认证的定时器。
[Device] mac-authentication timer offline-detect 180 [Device] mac-authentication timer quiet 180 \# 配置 MAC 地址认证使用固定用户名帐号：用户名为 aaa，密码为明文 123456。
[Device] mac-authentication user-name-format fixed account aaa password simple 123456 \# 开启全局 MAC 地址认证。
[Device] mac-authentication

###### 4. 验证配置

\# 显示 MAC 地址认证配置信息。
<Device> display mac-authentication Global MAC authentication parameters:
MAC authentication : Enabled Username format : Fixed account Username : aaa Password : ****** Offline detect period : 180 s Quiet period : 180 s Server timeout : 100 s Reauth period : 3600 s Authentication domain : bbb Online MAC-auth users : 1 Silent MAC users:
MAC address VLAN ID From port Port index Ten-GigabitEthernet1/0/1 is link-up MAC authentication : Enabled Carry User-IP : Disabled Authentication domain : Not configured Auth-delay timer : Disabled Periodic reauth : Disabled Re-auth server-unreachable : Logoff Guest VLAN : Not configured Guest VLAN auth-period : 30 s Critical VLAN : Not configured Critical voice VLAN : Disabled Host mode : Single VLAN

###### 1. 组网需求

Offline detection : Enabled Authentication order : Default Guest VSI : Not configured Guest VSI auth-period : 30 s Critical VSI : Not configured Auto-tag feature : Disabled VLAN tag configuration ignoring : Disabled Max online users : 4294967295 Authentication attempts : successful 1, failed 0 Current online users : 1 MAC address Auth state 00e0-fc12-3456 Authenticated

##### 1.21.3 下发ACL典型配置举例

组网需求
1.
如 图 1-5 所示，用户主机Host通过端口Ten-GigabitEthernet1/0/1 连接到设备上，设备通过RADIUS服务器对用户进行认证、授权和计费，Internet网络中有一台FTP服务器，IP地址为 10.0.0.1。现有如下组网需求：
• 在端口 Ten-GigabitEthernet1/0/1 上对用户接入进行 MAC 地址认证，以控制其对 Internet 的访问。认证时使用用户的源 MAC 地址做用户名和密码，其中 MAC 地址带连字符、字母小写。
• 当用户认证成功上线后，允许用户访问除 FTP 服务器之外的 Internet 资源。

###### 2. 组网图

图1-5 下发 典型配置组网图ACL

###### 3. 配置步骤

(1) 配置 RADIUS 服务器，保证用户的认证/授权/计费功能正常运行
\# 由于该例中使用了 MAC 地址认证的缺省用户名和密码，即使用用户的源 MAC 地址做用户
名与密码，因此还要保证 RADIUS 服务器上正确添加了接入用户帐户：用户名为
00-e0-fc-12-34-56，密码为 00-e0-fc-12-34-56。
\# 指定 RADIUS 服务器上的授权 ACL 为设备上配置的 ACL 3000。

###### 4. 验证配置

(2) 配置授权 ACL
\# 配置 ACL 3000，拒绝目的 IP 地址为 10.0.0.1 的报文通过。
<Device> system-view
[Device] acl advanced 3000
[Device-acl-ipv4-adv-3000] rule 0 deny ip destination 10.0.0.1 0
[Device-acl-ipv4-adv-3000] quit
(3) 配置使用 RADIUS 服务器进行 MAC 地址认证
\# 配置 RADIUS 方案。
[Device] radius scheme 2000
[Device-radius-2000] primary authentication 10.1.1.1 1812
[Device-radius-2000] primary accounting 10.1.1.2 1813
[Device-radius-2000] key authentication simple abc
[Device-radius-2000] key accounting simple abc
[Device-radius-2000] user-name-format without-domain
[Device-radius-2000] quit
配置 域的 方法。
\# ISP AAA
[Device] domain bbb
[Device-isp-bbb] authentication default radius-scheme 2000
[Device-isp-bbb] authorization default radius-scheme 2000
[Device-isp-bbb] accounting default radius-scheme 2000
[Device-isp-bbb] quit
\# 配置 MAC 地址认证用户所使用的 ISP 域。
[Device] mac-authentication domain bbb
\# 配置 MAC 地址认证用户的帐号格式：使用带连字符的 MAC 地址做用户名与密码，其中字
母小写。
[Device] mac-authentication user-name-format mac-address with-hyphen lowercase
\# 开启端口 Ten-GigabitEthernet1/0/1 上的 MAC 地址认证。
[Device] interface ten-gigabitethernet 1/0/1
[Device-Ten-GigabitEthernet1/0/1] mac-authentication
[Device-Ten-GigabitEthernet1/0/1] quit
\# 开启全局 MAC 地址认证。
[Device] mac-authentication
验证配置
4.
\# 显示 MAC 地址认证配置信息。
<Device> display mac-authentication
Global MAC authentication parameters:
MAC authentication : Enable
Username format : MAC address in lowercase(xx-xx-xx-xx-xx-xx)
Username : mac
Password : Not configured
Offline detect period : 300 s
Quiet period : 60 s
Server timeout : 100 s
Reauth period : 3600 s
Authentication domain : bbb

Online MAC-auth users : 1 Silent MAC users:
MAC address VLAN ID From port Port index Ten-GigabitEthernet1/0/1 is link-up MAC authentication : Enabled Carry User-IP : Disabled Authentication domain : Not configured Auth-delay timer : Disabled Periodic reauth : Disabled Re-auth server-unreachable : Logoff Guest VLAN : Not configured Guest VLAN auth-period : 30 s Critical VLAN : Not configured Critical voice VLAN : Disabled Host mode : Single VLAN Offline detection : Enabled Authentication order : Default Guest VSI : Not configured Guest VSI auth-period : 30 s Critical VSI : Not configured Auto-tag feature : Disabled VLAN tag configuration ignoring : Disabled Max online users : 4294967295 Authentication attempts : successful 1, failed 0 Current online users : 1 MAC address Auth state 00e0-fc12-3456 Authenticated用户认证上线后，Ping FTP 服务器，发现服务器不可达，说明认证服务器下发的 ACL 3000 已生效。
C:\>ping 10.0.0.1 Pinging 10.0.0.1 with 32 bytes of data:
Request timed out.
Request timed out.
Request timed out.
Request timed out.
Ping statistics for 10.0.0.1:
Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),

## 04-Portal配置

目 录简介认证流程配置任务简介配置 服务器配置重定向 的匹配规则配置限制和指导在接口上引用Portal Web服务器功能简介

配置免认证规则配置 最大用户数配置 支持 代理
1.13.1 1-24配置 报文属性配置 重定向功能Portal二次地址分配认证扩展功能配置举例

Portal常见故障处理接入设备强制用户下线后， 认证服务器上还存在该用户

### 1 Portal

1 Portal

#### 1.1 Portal简介

认证通过 页面接受用户输入的用户名和密码，对用户进行身份认证，以达到对用户访问Portal Web进行控制的目的。Portal 认证通常部署在接入层以及需要保护的关键数据入口处实施访问控制。在采用了 Portal 认证的组网环境中，用户可以主动访问已知的 Portal Web 服务器网站进行 Portal 认证，也可以访问任意非 服务器网站时，被强制访问 服务器网站，继而开始Portal Web Portal Web Portal 认证。目前，设备支持的 Portal 版本为 Portal 1.0、Portal 2.0 和 Portal 3.0。

##### 1.1.1 Portal认证的优势

Portal 认证具有如下优势：
• 可以不安装客户端软件，直接使用 Web 页面认证，使用方便。
• 可以为运营商提供方便的管理功能和业务拓展功能，例如运营商可以在认证页面上开展广告、社区服务、信息发布等个性化的业务。
支持多种组网型态，例如二次地址分配认证方式可以实现灵活的地址分配策略且能节省公网
•地址，可跨三层认证方式可以跨网段对用户作认证。
IP

##### 1.1.2 Portal安全扩展功能

Portal 的安全扩展功能是指，在 Portal 身份认证的基础之上，通过强制接入终端实施补丁和防病毒策略，加强网络终端对病毒攻击的主动防御能力。具体的安全扩展功能如下：
安全性检测：在对用户的身份认证的基础上增加了安全认证机制，可以检测接入终端上是否
•安装了防病毒软件、是否更新了病毒库、是否安装了非法软件、是否更新了操作系统补丁等；
访问资源受限：用户通过身份认证后仅仅获得访问指定互联网资源的权限，如病毒服务器、
•操作系统补丁更新服务器等；当用户通过安全认证后便可以访问更多的互联网资源。
安全性检测功能必须与 H3C 的 iMC 安全策略服务器以及 iNode 客户端配合使用。

##### 1.1.3 Portal系统

如 图 1-1 所示，Portal系统通常由如下实体组成：认证客户端、接入设备、Portal认证服务器、Portal Web服务器、AAA服务器和安全策略服务器。

###### 2. 接入设备

##### 1.1.4 使用远程Portal服务器的基本交互过程

图1-1 Portal 系统组成示意图

###### 1. 认证客户端

用户终端的客户端系统，为运行 HTTP/HTTPS 协议的浏览器或运行 Portal 客户端的主机。对用户终端的安全性检测是通过 客户端和安全策略服务器之间的信息交流完成的。目前，Portal 客Portal户端仅支持 H3C iNode 客户端。
接入设备
2.
提供接入服务的设备，主要有三方面的作用：
• 在认证之前，将用户的所有 HTTP/HTTPS 请求都重定向到 Portal Web 服务器。
• 在认证过程中，与 Portal 认证服务器、AAA 服务器交互，完成身份认证/授权/计费的功能。
• 在认证通过后，允许用户访问被授权的互联网资源。

###### 3. Portal服务器

包括 Portal Web服务器和 Portal 认证服务器。Portal Web服务器负责向客户端提供 Web认证页面，并将客户端的认证信息（用户名、密码等）提交给 认证服务器。Portal 认证服务器用于接收Portal Portal 客户端认证请求的服务器端系统，与接入设备交互认证客户端的认证信息。Portal Web 服务器通常与 Portal 认证服务器是一体的，也可以是独立的服务器端系统。

###### 4. AAA服务器

与接入设备进行交互，完成对用户的认证、授权和计费。目前 RADIUS（Remote Authentication Service，远程认证拨号用户服务）服务器可支持对 用户进行认证、授权和计费，Dial-In User Portal以及 LDAP（Lightweight Directory Access Protocol，轻量级目录访问协议）服务器可支持对 Portal用户进行认证。

###### 5. 安全策略服务器

与 Portal 客户端、接入设备进行交互，完成对用户的安全检测，并对用户进行安全授权操作。仅运行 客户端的主机支持与安全策略服务器交互。
Portal使用远程 服务器的基本交互过程
1.1.4 Portal Portal 系统中各基本要素的交互过程如下：

###### 1. 系统组成

(1) 当未认证用户使用浏览器进行 Portal 认证时，可以通过浏览器访问任一互联网地址，接入设
备会将此 或 请求重定向到 服务器的 认证主页上。也可以主动
HTTP HTTPS Portal Web Web
登录 Portal Web 服务器的 Web 认证主页。当未认证用户使用 iNode 客户端进行 Portal 认证
时，可直接打开客户端，输入认证信息。
(2) 用户在认证主页/认证对话框中输入认证信息后提交，Portal Web 服务器会将用户的认证信息
传递给 认证服务器，由 认证服务器处理并转发给接入设备。
Portal Portal
(3) 接入设备与 AAA 服务器交互进行用户的认证、授权和计费。
(4) 认证通过后，如果未对用户采用安全策略，则接入设备会打开用户与互联网的通路，允许用
户访问互联网；如果使用 客户端进行认证，并对用户采用了安全策略，则客户端、接
iNode
入设备与安全策略服务器交互，对用户的安全检测通过之后，安全策略服务器根据用户的安
全性授权用户访问非受限资源。

##### 1.1.5 本地Portal服务

系统组成
1.
接入设备可以同时提供Portal Web服务器和Portal认证服务器功能，对接入的Portal用户进行本地Portal认证，如 图 所示。该组网方式下，Portal系统仅支持通过Web登录、下线的基本认证功1-2能，不支持使用Portal客户端方式的Portal认证，因此不支持Portal扩展功能，无需部署安全策略服务器。
图1-2 使用本地 Portal 服务的 Portal 系统组成示意图内嵌 Portal 服务器认证客户端 认证 / 计费服务器的接入设备

###### 2. 本地Portal Web服务支持用户自定义认证页面

本地 Portal Web 服务支持由用户自定义认证页面的内容，即允许用户编辑一套或多套认证页面的HTML 文件，并将其压缩之后保存至设备的存储介质的根目录中。每套自定义页面文件中包括六个认证页面：登录页面、登录成功页面、在线页面、下线成功页面、登录失败页面和系统忙碌页面。
本地 Portal Web 服务根据不同的认证阶段向客户端推出对应的认证页面。
关于认证页面文件的自定义规范请参见“1.7.3 自定义认证页面文件”。

##### 1.1.6 Portal的认证方式

Portal 支持三种认证方式：直接认证方式、二次地址分配认证方式和可跨三层认证方式。直接认证方式和二次地址分配认证方式下，认证客户端和接入设备之间没有三层转发设备；可跨三层认证方式下，认证客户端和接入设备之间可以（但不必须）跨接三层转发设备。

###### 1. 直接认证方式

用户在认证前通过手工配置或 DHCP 直接获取一个 IP 地址，只能访问 Portal Web 服务器，以及设定的免认证地址；认证通过后即可访问网络资源。认证流程相对简单。

###### 2. 二次地址分配认证方式

用户在认证前通过 获取一个私网 地址，只能访问 服务器，以及设定的免认证DHCP IP Portal Web地址；认证通过后，用户会申请到一个公网 IP 地址，即可访问网络资源。该认证方式解决了 IP 地址规划和分配问题，对未认证通过的用户不分配公网 IP 地址。例如运营商对于小区宽带用户只在访问小区外部资源时才分配公网 IP。目前，仅 H3C iNode 客户端支持该认证方式。需要注意的是，IPv6认证不支持二次地址分配方式。
Portal

###### 3. 可跨三层认证方式

和直接认证方式基本相同，但是这种认证方式允许认证用户和接入设备之间跨越三层转发设备。
对于以上三种认证方式，IP 地址都是用户的唯一标识。接入设备基于用户的 IP 地址下发 ACL 对接口上通过认证的用户报文转发进行控制。由于直接认证和二次地址分配认证下的接入设备与用户之间未跨越三层转发设备，因此接口可以学习到用户的 MAC 地址，接入设备可以利用学习到 MAC 地址增强对用户报文转发的控制力度。

##### 1.1.7 Portal认证流程

直接认证和可跨三层 Portal 认证流程相同。二次地址分配认证流程因为有两次地址分配过程，所以其认证流程和另外两种认证方式有所不同。

###### 1. 直接认证和可跨三层Portal认证的流程（CHAP/PAP认证方式）

图1-3 直接认证/可跨三层 认证流程图Portal直接认证/可跨三层 认证流程：
Portal用户通过 协议访问外部网络。HTTP/HTTPS 报文经过接入设备时，对于
(1) Portal HTTP/HTTPS访问 Portal Web 服务器或设定的免认证地址的 HTTP/HTTPS 报文，接入设备允许其通过；
对于访问其它地址的 HTTP/HTTPS 报文，接入设备将其重定向到 Portal Web 服务器。Portal Web 服务器提供 Web 页面供用户输入用户名和密码。

(2) Portal Web 服务器将用户输入的信息提交给 Portal 认证服务器进行认证。
(3) Portal 认证服务器与接入设备之间进行 CHAP（Challenge Handshake Authentication Protocol，
质询握手认证协议）认证交互。若采用 PAP（Password Protocol，密码认证
Authentication
协议）认证则直接进入下一步骤。采用哪种认证交互方式由 Portal 认证服务器决定。
(4) Portal 认证服务器将用户输入的用户名和密码组装成认证请求报文发往接入设备，同时开启定
时器等待认证应答报文。
(5) 接入设备与 RADIUS 服务器之间进行 RADIUS 协议报文的交互。
(6) 接入设备向 Portal 认证服务器发送认证应答报文，表示认证成功或者认证失败。
(7) Portal 认证服务器向客户端发送认证成功或认证失败报文，通知客户端认证成功（上线）或失
败。
(8) 若认证成功，Portal 认证服务器还会向接入设备发送认证应答确认。若是 iNode 客户端，则还
需要进行以下安全扩展功能的步骤，否则 认证过程结束，用户上线。
Portal
客户端和安全策略服务器之间进行安全信息交互。安全策略服务器检测客户端的安全性是否
(9)
合格，包括是否安装防病毒软件、是否更新病毒库、是否安装了非法软件、是否更新操作系
统补丁等。
(10) 安全策略服务器根据安全检查结果授权用户访问指定的网络资源，授权信息保存到接入设备
中，接入设备将使用该信息控制用户的访问。
步骤(9)、(10)为 Portal 认证安全扩展功能的交互过程。

###### 2. 二次地址分配认证方式的流程（CHAP/PAP认证方式）

图1-4 二次地址分配认证方式流程图二次地址分配认证流程：
(1)～(7)同直接/可跨三层 认证中步骤（1）～（7）。
Portal

(8) 客户端收到认证通过报文后，通过 DHCP 获得新的公网 IP 地址，并通知 Portal 认证服务器用
户已获得新 地址。
IP
认证服务器通知接入设备客户端获得新公网 地址。
(9) Portal IP
接入设备通过 模块得知用户 地址变化后，通告 认证服务器已检测到用户
(10) DHCP IP Portal IP
变化。
(11) 当 Portal 认证服务器接收到客户端以及接入设备发送的关于用户 IP 变化的通告后，通知客户
端上线成功。
(12) Portal 认证服务器向接入设备发送 IP 变化确认报文。
(13) 客户端和安全策略服务器之间进行安全信息交互。安全策略服务器检测客户端的安全性是否
合格，包括是否安装防病毒软件、是否更新病毒库、是否安装了非法软件、是否更新操作系
统补丁等。
安全策略服务器根据用户的安全性授权用户访问指定的网络资源，授权信息保存到接入设备
(14)
中，接入设备将使用该信息控制用户的访问。
步骤(13)、(14)为 Portal 认证扩展功能的交互过程。

##### 1.1.8 Portal支持EAP认证

EAP 认证仅能与 H3C iMC 的 Portal 服务器以及 H3C iNode Portal 客户端配合使用，且仅使用远程服务器的 认证支持该功能。
Portal Portal在对接入用户身份可靠性要求较高的网络应用中，传统的基于用户名和口令的用户身份验证方式存在一定的安全问题，基于数字证书的用户身份验证方式通常被用来建立更为安全和可靠的网络接入认证机制。
EAP（Extensible Authentication Protocol，可扩展认证协议）可支持多种基于数字证书的认证方式（例如 EAP-TLS），它与 Portal 认证相配合，可共同为用户提供基于数字证书的接入认证服务。
图1-5 Portal 支持 EAP 认证协议交互示意图所示，在Portal支持EAP认证的实现中，客户端与Portal服务器之间交互EAP认证报文，如 图 1-5 Portal 服务器与接入设备之间交互携带 EAP-Message 属性的 Portal 协议报文，接入设备与 RADIUS服务器之间交互携带EAP-Message属性的RADIUS协议报文，由具备EAP服务器功能的RADIUS服务器处理EAP-Message属性中封装的EAP报文，并给出EAP认证结果。整个EAP认证过程中，接入设备只是对Portal服务器与RADIUS服务器之间的EAP-Message属性进行透传，并不对其进行任何处理，因此接入设备上无需任何额外配置。

##### 1.1.9 Portal过滤规则

接入设备通过一系列的过滤规则对用户报文进行控制，这些规则也称为 过滤规则。
Portal设备会根据配置以及 用户的认证状态，生成四种不同类型的 过滤规则。设备收到用户Portal Portal报文后，将依次按照如下顺序对报文进行匹配，一旦匹配上某条规则便结束匹配过程：
• 第一类规则：设备允许所有去往 Portal Web 服务器或者符合免认证规则的用户报文通过。

第二类规则：如果 AAA 认证服务器未下发授权 ACL，则设备允许认证成功的 Portal 用户可以
•访问任意的目的网络资源；如果 认证服务器下发了授权 ACL，则设备仅允许认证成功的AAA Portal 用户访问该授权 ACL 允许访问的网络资源。需要注意的是，Portal 认证可成功授权的ACL 类型为基本 ACL（ACL 编号为 2000～2999）和高级 ACL（ACL 编号为 3000～3999）。
当下发的 不存在、未配置 规则或 规则中配置了 counting、established、ACL ACL ACL fragment 或 logging 参数时，授权 ACL 不生效。关于 ACL 规则的详细介绍，请参见“ACL和 QoS 命令参考”中的“ACL”。设备将根据 Portal 用户的在线状态动态添加和删除本规则。
• 第三类规则：设备将所有未认证 Portal 用户的 HTTP/HTTPS 请求报文重定向到 Portal Web服务器。
• 第四类规则：对于直接认证方式和可跨三层认证方式，设备将拒绝所有用户报文通过；对于二次地址分配认证方式，设备将拒绝所有源地址为私网地址的用户报文通过。

#### 1.2 Portal配置限制和指导

仅支持在三层接口上开启 Portal 认证。
通过访问 Web 页面进行的 Portal 认证不能对用户实施安全策略检查，安全检查功能的实现需要与客户端配合。
H3C iNode无论是 客户端还是 客户端发起的 认证，均能支持 认证穿越 NAT，即Web H3C iNode Portal Portal Portal 客户端位于私网、Portal 认证服务器位于公网。

#### 1.3 Portal配置任务简介

配置任务如下：
Portal配置 服务
(1) Portal请根据实际组网环境选择以下一种进行配置。
配置远程 Portal 服务(cid:123)
配置远程Portal认证服务器配置Portal Web服务器配置本地 Portal 服务(cid:123)
配置本地Portal服务配置Portal Web服务器
(2) 开启 Portal 认证并引用 Portal Web 服务器在接口上开启Portal认证(cid:123)
在接口上引用Portal Web服务器(cid:123)
(3) （可选）配置 Portal 认证前用户参数配置Portal认证前用户使用的地址池(cid:123)
(4) （可选）指定Portal用户使用的认证域
(5) （可选）控制Portal用户的接入配置免认证规则(cid:123)
配置源认证网段(cid:123)

配置目的认证网段(cid:123)
配置第二类Portal过滤规则下发的完整性检查功能(cid:123)
配置Portal最大用户数(cid:123)
配置Portal授权信息严格检查模式(cid:123)
配置Portal仅允许DHCP用户上线(cid:123)
配置Portal支持Web代理(cid:123)
配置Portal用户漫游功能(cid:123)
配置Portal用户逃生功能(cid:123)
(6) （可选）配置Portal探测功能配置Portal用户在线探测功能(cid:123)
配置Portal认证服务器的可达性探测功能(cid:123)
配置Portal Web服务器的可达性探测功能(cid:123)
配置Portal用户信息同步功能(cid:123)
(7) （可选）配置 Portal 和 RADIUS 报文属性配置Portal报文属性(cid:123)
可配置 报文的 属性和接入设备的 ID。
Portal BAS-IP/BAS-IPv6配置RADIUS报文属性(cid:123)
可配置 报文的 属性、NAS-Port-Type 属性类型和接口的RADIUS NAS-Port-ID NAS-ID Profile。
(8) （可选）关闭Portal客户端Rule ARP/ND表项生成功能
(9) （可选）配置 Portal 用户上下线功能强制在线Portal用户下线(cid:123)
开启Portal用户上/下线日志功能(cid:123)
（可选）配置Web重定向功能
(10)

#### 1.4 Portal配置准备

Portal 提供了一个用户身份认证和安全认证的实现方案，但是仅仅依靠 Portal 不足以实现该方案。
接入设备的管理者需选择使用 认证方法，以配合 完成用户的身份认证。 认证RADIUS Portal Portal的配置前提：
• Portal 认证服务器、Portal Web 服务器、RADIUS 服务器已安装并配置成功。
• 若采用二次地址分配认证方式，接入设备需启动 DHCP 中继功能，另外需要安装并配置好DHCP 服务器。
• 用户、接入设备和各服务器之间路由可达。
• 如果通过远端 RADIUS 服务器进行认证，则需要在 RADIUS 服务器上配置相应的用户名和密码，然后在接入设备端进行 RADIUS 客户端的相关设置。RADIUS 客户端的具体配置请参见“安全配置指导”中的“AAA”。
如果需要支持 的安全扩展功能，需要安装并配置 安全策略组件。
• Portal CAMS EAD/iMC EAD同时保证在接入设备上的 ACL 配置和安全策略服务器上配置的隔离 ACL 的编号、安全 ACL

##### 3. 配置步骤

的编号对应。安全策略服务器的配置请参考“CAMS EAD 安全策略组件联机帮助”以及“iMC安全策略组件联机帮助”。
EAD

#### 1.5 配置远程Portal认证服务器

##### 1. 功能简介

开启了 Portal 认证功能后，设备收到 Portal 报文时，首先根据报文的源 IP 地址和 VPN 信息查找本地配置的 Portal 认证服务器，若查找到相应的 Portal 认证服务器配置，则认为报文合法，并向该认证服务器回应认证响应报文；否则，认为报文非法，将其丢弃。
Portal

##### 2. 配置限制和指导

不要删除正在被用户使用的 Portal 认证服务器，否则会导致设备上的在线用户无法正常下线。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 创建 Portal 认证服务器，并进入 Portal 认证服务器视图。
portal server server-name设备支持配置多个 Portal 认证服务器。
(3) 指定 Portal 认证服务器的 IP 地址。
（IPv4 网络）
ip ipv4-address [ vpn-instance vpn-instance-name ] [ key { cipher | simple } string ]（IPv6 网络）
ipv6 ipv6-address [ vpn-instance vpn-instance-name ] [ key { cipher | simple } string ]
(4) （可选）配置接入设备主动向 Portal 认证服务器发送 Portal 报文时使用的 UDP 端口号。
port port-number缺省情况下，接入设备主动向 Portal 认证服务器发送 Portal 报文时使用的 UDP 端口号为50100。
接入设备主动向 Portal 认证服务器发送 Portal 报文时使用的 UDP 端口号必须与远程 Portal认证服务器实际使用的监听端口号保持一致。
配置 认证服务器的类型。
(5) Portal server-type { cmcc | imc }缺省情况下，Portal 认证服务器类型为 iMC 服务器。
配置的 Portal 认证服务器类型必须与认证所使用的服务器类型保持一致。
(6) （可选）配置设备定期向 Portal 认证服务器发送注册报文。
server-register [ interval interval-value ]缺省情况下，设备不会向 Portal 认证服务器发送注册报文。

#### 1.6 配置Portal Web服务器

##### 1.6.1 Portal Web服务器配置简介

Portal Web 服务器配置任务如下：
(1) 配置Portal Web服务器基本参数
(2) （可选）开启Portal被动Web认证功能
(3) （可选）配置重定向URL的匹配规则

##### 1.6.2 配置Portal Web服务器基本参数

(1) 进入系统视图。
system-view
(2) 创建 Portal Web 服务器，并进入 Portal Web 服务器视图。
portal web-server server-name
可以配置多个 Portal Web 服务器。
(3) 指定 Portal Web 服务器所属的 VPN。
vpn-instance vpn-instance-name
缺省情况下，Portal Web 服务器位于公网中。
(4) 指定 Portal Web 服务器的 URL。
url url-string
缺省情况下，未指定 Portal Web 服务器的 URL。
对用户的 HTTPS 请求进行重定向时，需要在设备上配置对 HTTPS 报文进行重定向的内部侦
听端口号，具体配置请参见“三层技术-IP 业务配置指导”中的“HTTP 重定向”。
(5) 退回系统视图。
quit
(6) 配置对 HTTPS 报文进行重定向的内部侦听端口号。
http-redirect https-port port-number
缺省情况下，未配置对 HTTPS 报文进行重定向的内部侦听端口号。
本配置仅在需要对用户的 HTTPS 请求进行重定向时配置。
具体命令的介绍请参见“三层技术-IP 业务命令参考”中的“HTTP 重定向”。
(7) 进入 Portal Web 服务器视图。
portal web-server server-name
配置设备重定向给用户的 服务器的 中携带的参数信息。
(8) Portal Web URL
url-parameter param-name { original-url | source-address | source-mac
[ encryption { aes | des } key { cipher | simple } string ] | value
expression }
缺省情况下，未配置设备重定向给用户的 Portal Web 服务器的 URL 中携带的参数信息。
(9) 配置 Portal Web 服务器的类型。
server-type { cmcc | imc }

###### 1. 功能简介

缺省情况下，设备默认支持的 Portal Web 服务器类型为 iMC 服务器。该配置只适用于远程认证。
Portal配置的 服务器类型必须与认证所使用的服务器类型保持一致。
Portal Web

##### 1.6.3 开启Portal被动Web认证功能

###### 1. 功能简介

iOS 系统或者部分 Android 系统的用户接入已开启 Portal 认证的网络后，设备会主动向这类用户终端推送 Portal 认证页面。开启 Portal 被动 Web 认证功能后，仅在这类用户使用浏览器访问 Internet时，设备才会为其推送 Portal 认证页面。

###### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入 Portal Web 服务器视图。
portal web-server server-name
(3) 开启 Portal 被动 Web 认证功能。
captive-bypass enable缺省情况下，Portal 被动 Web 认证功能处于关闭状态。

##### 1.6.4 配置重定向URL的匹配规则

功能简介
1.
重定向 URL 匹配规则用于控制重定向用户的 HTTP 或 HTTPS 请求，该匹配规则可匹配用户的 Web请求地址或者用户的终端信息。与 命令不同的是，重定向匹配规则可以灵活的进行地址的重定url向，而 url 命令一般只用于将用户的 HTTP 或 HTTPS 请求重定向到 Portal Web 服务器进行 Portal认证。

###### 2. 配置限制和指导

为了让用户能够成功访问重定向后的地址，需要通过 portal free-rule 命令配置免认证规则，放行去往该地址的 或 请求报文。
HTTP HTTPS当同时配置了 命令和重定向 的匹配规则时，重定向 匹配规则优先进行地址的重定向。
url URL URL

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 Portal Web 服务器视图。
portal web-server server-name
配置重定向 的匹配规则。
(3) URL
if-match { original-url url-string redirect-url url-string
[ url-param-encryption { aes | des } key { cipher | simple } string ] |
user-agent string redirect-url url-string }

#### 1.7 配置本地Portal服务

##### 1.7.1 功能简介

配置了本地 Portal 服务后，由设备作为 Portal Web 服务器和 Portal 认证服务器，对接入用户进行认证。Portal 认证页面文件存储在设备的根目录下。

##### 1.7.2 配置限制和指导

只有接口上引用的 Portal Web 服务器中的 URL 同时满足以下两个条件时，接口上才会使用本地Portal Web 服务功能。条件如下：
• 该 URL 中的 IP 地址是设备上与客户端路由可达的三层接口 IP 地址（除 127.0.0.1 以外）。
• 该 URL 以/portal/结尾，例如：http://1.1.1.1/portal/。
设备本身自带有缺省页面文件包，用户也可以自定义认证页面的内容和样式。

##### 1.7.3 自定义认证页面文件

###### 1. 功能简介

用户自定义的认证页面为 HTML 文件的形式，压缩后保存在设备的存储介质的根目录中。每套认证页面可包括六个主索引页面（登录页面、登录成功页面、登录失败页面、在线页面、系统忙碌页面、下线成功页面）及其页面元素（认证页面需要应用的各种文件，如 页面中的 back.jpg），Logon.htm每个主索引页面可以引用若干页面元素。
用户在自定义这些页面时需要遵循一定的规范，否则会影响本地 Portal Web 服务功能的正常使用和系统运行的稳定性。

###### 2. 文件名规范

主索引页面文件名不能自定义，必须使用 表 1-1 中所列的固定文件名。
表1-1 主索引页面文件名主索引页面 文件名登录页面 logon.htm登录成功页面 logonSuccess.htm登录失败页面 logonFail.htm在线页面online.htm用于提示用户已经在线系统忙页面busy.htm用于提示系统忙或者该用户正在登录过程中下线成功页面 logoffSuccess.htm

主索引页面文件之外的其他文件名可由用户自定义，但需注意文件名和文件目录名中不能含有中文且字符不区分大小写。

###### 3. 页面请求规范

本地 Portal Web 服务器只能接受 Get 请求和 Post 请求。
Get 请求用于获取认证页面中的静态文件，其内容不能为递归内容。例如，Logon.htm 文件中
•包含了 文件的内容，但 文件中又包含了对 的引用，这种递归Get ca.htm ca.htm Logon.htm引用是不允许的。
• Post 请求用于用户提交用户名和密码以及用户执行登录、下线操作。

###### 4. Post请求中的属性规范

(1) 认证页面中表单（Form）的编辑必须符合以下原则：
认证页面可以含有多个 Form，但是必须有且只有一个 Form 的 action=logon.cgi，否则无
(cid:123)
法将用户信息送到本地 Portal 服务器。
用户名属性固定为”PtUser”，密码属性固定为”PtPwd”。
(cid:123)
需要有用于标记用户登录还是下线的属性”PtButton”，取值为"Logon"表示登录，取值为
(cid:123)
"Logoff"表示下线。
登录 请求必须包含”PtUser”，”PtPwd”和"PtButton"三个属性。
Post
(cid:123)
下线 请求必须包含”PtButton”这个属性。
Post
(cid:123)
(2) 需要包含登录 Post 请求的页面有 logon.htm 和 logonFail.htm。
logon.htm 页面脚本内容的部分示例：
<form action=logon.cgi method = post >
<p>User name:<input type="text" name = "PtUser" style="width:160px;height:22px"
maxlength=64>
<p>Password :<input type="password" name = "PtPwd" style="width:160px;height:22px"
maxlength=32>
<p><input type=SUBMIT value="Logon" name = "PtButton" style="width:60px;"
onclick="form.action=form.action+location.search;>
</form>
需要包含下线 请求的页面有 和 online.htm。
(3) Post logonSuccess.htm
页面脚本内容的部分示例：
online.htm
<form action=logon.cgi method = post >
<p><input type=SUBMIT value="Logoff" name="PtButton" style="width:60px;">
</form>

###### 5. 页面文件压缩及保存规范

• 完成所有认证页面的编辑之后，必须按照标准 Zip 格式将其压缩到一个 Zip 文件中，该 Zip 文
件的文件名只能包含字母、数字和下划线。
• 压缩后的 Zip 文件中必须直接包含认证页面，不允许存在间接目录。
• 压缩生成的 Zip 文件可以通过 FTP 或 TFTP 的二进制方式上传至设备，并保存在设备的根目
录下。

###### 1. 配置准备

###### 2. 配置步骤

Zip 文件保存目录示例：
<Sysname> dir Directory of flash:
1 -rw- 1405 Feb 28 2008 15:53:20 ssid1.zip 0 -rw- 1405 Feb 28 2008 15:53:31 ssid2.zip 2 -rw- 1405 Feb 28 2008 15:53:39 ssid3.zip 3 -rw- 1405 Feb 28 2008 15:53:44 ssid4.zip 2540 KB total (1319 KB free)

###### 6. 认证成功后认证页面自动跳转

若要支持认证成功后认证页面的自动跳转功能，即认证页面会在用户认证成功后自动跳转到指定的网站页面，则需要在认证页面 和 的脚本文件中做如下改动。
logon.htm logonSuccess.htm将 文件中的 的 值设置为“_blank”。
(1) logon.htm Form target修改的脚本内容如下突出显示部分所示：
<form method=post action=logon.cgi target="_blank">
(2) logonSucceess.htm 文件添加页面加载的初始化函数“pt_init()”。
增加的脚本内容如下突出显示部分所示：
<html> <head> <title>LogonSuccessed</title> <script type="text/javascript" language="javascript" src="pt_private.js"></script> </head> <body onload="pt_init();" onbeforeunload="return pt_unload();"> ... ...
</body> </html>

##### 1.7.4 配置本地Portal Web服务参数

配置准备
1.
若指定本地 Portal Web 服务支持的协议类型为 HTTPS，则需要首先完成以下配置：
• 配置 PKI 策略，并成功申请本地证书和 CA 证书，具体配置请参见“安全配置指导”中的“PKI”。
• 配置 SSL 服务器端策略，并指定使用已配置的 PKI 域。为避免在用户浏览器和设备建立 SSL连接过程中用户浏览器出现“使用的证书不安全”的告警，需要通过配置自定义名称为的 服务器端策略，在设备上安装用户浏览器信任的证书。具体配置请参见https_redirect SSL“安全配置指导”中的“SSL”。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 开启本地 Portal 服务，并进入基于 HTTP/HTTPS 协议的本地 Portal Web 服务视图。
portal local-web-server { http | https ssl-server-policy policy-name [ tcp-port port-number ] }
(3) 配置本地 Portal Web 服务提供的缺省认证页面文件。
default-logon-page filename

缺省情况下，本地 Portal Web 服务未提供缺省认证页面文件。
(4) （可选）配置本地 Portal Web 服务的 HTTP/HTTPS 服务侦听的 TCP 端口号。
tcp-port port-number缺省情况下，HTTP 服务侦听的 TCP 端口号为 80，HTTPS 服务侦听的 TCP 端口号为命令指定的 端口号。
portal local-web-server TCP

#### 1.8 在接口上开启Portal认证

##### 1. 配置限制和指导

在接口上开启 Portal 认证时，请遵循以下配置原则：
• 当接入设备和 Portal 用户之间跨越三层设备时，只能配置可跨三层 Portal 认证方式（layer3），但可跨三层 Portal 认证方式不要求接入设备和 Portal 用户之间必需跨越三层设备。
• 允许在接口上同时开启 IPv4 Portal 认证和 IPv6 Portal 认证。
当 Portal 认证方式为二次地址分配方式时，请遵循以下配置限制和指导：
• 在开启二次地址分配方式的 Portal 认证之前，需要保证开启 Portal 的接口已配置或者获取了合法的 IP 地址。
• 在二次地址分配认证方式下，接口上配置的授权 ARP 后，系统会禁止该接口动态学习 ARP表项，只有通过 合法分配到公网 地址的用户的 报文才能够被学习。因此，为DHCP IP ARP保证只有合法用户才能接入网络，建议使用二次地址分配认证方式的 Portal 认证时，接口上同时配置了授权 ARP 功能。
• 为了确保 Portal 用户能在开启二次地址分配认证方式的接口上成功进行 Portal 认证，必须确保 Portal 认证服务器上指定的设备 IP 与设备 BAS-IP 或 BAS-IPv6 属性值保持一致。可以通过 }命令来配置该属性值。
portal { bas-ip | bas-ipv6服务器不支持二次地址分配方式的 认证。
• IPv6 Portal Portal

##### 2. 配置步骤

(1) 进入系统视图。
system-view
进入三层接口视图。
(2)
interface interface-type interface-number
开启 认证，并指定认证方式。
(3) Portal
（IPv4 网络）
portal enable method { direct | layer3 | redhcp }
（IPv6 网络）
portal ipv6 enable method { direct | layer3 }
缺省情况下，接口上的 Portal 认证功能处于关闭状态。

##### 2. 配置步骤

#### 1.9 在接口上引用Portal Web服务器

##### 1. 功能简介

一个接口上可以同时引用一个 服务器和一个 认证服务器。在接口IPv4 Portal Web IPv6 Portal Web上引用指定的 Portal Web 服务器后，设备会将该接口上 Portal 用户的 HTTP 请求报文重定向到该Web 服务器。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入三层接口视图。
interface interface-type interface-number
(3) 引用 Portal Web 服务器。
portal [ ipv6 ] apply web-server server-name [ fail-permit ]缺省情况下，接口上未引用 Portal Web 服务器。

#### 1.10 配置Portal认证前用户使用的地址池

##### 1. 功能简介

在 Portal 用户通过设备的子接口接入网络的组网环境中，当子接口上未配置 IP 地址，且用户需要通过 获取地址时，就必须在用户进行 认证之前为其分配一个 地址使其可以进行DHCP Portal IP Portal 认证。
Portal 用户接入到开启了 Portal 认证的接口上后，该接口就会按照下面的规则为其分配 IP 地址：
• 如果接口上配置了 IP 地址，但没有配置认证前使用的地址池，则用户可以使用客户端上静态配置的 IP 地址或者通过 DHCP 获取分配的 IP 地址。
• 如果接口上配置了 IP 地址，且配置了认证前使用的地址池，当用户通过 DHCP 获取 IP 地址时，接口将从指定的认证前的地址池中为其分配 IP 地址；否则，用户使用客户端上静态配置的 地址。
IP若接口上没有配置 地址，且没有配置认证前使用的地址池，则用户无法进行认证。
• IP用户使用静态配置或动态获取的 地址进行 认证，并通过认证后，认证服务器会为其Portal IP Portal下发授权 IP 地址池，且由 DHCP 重新为其分配 IP 地址。如果认证服务器未下发授权 IP 地址池，则用户继续使用认证之前获得的 IP 地址。

##### 2. 配置限制和指导

仅当接口使用直接认证方式情况下，本配置才能生效。
当使用接口上指定的 IP 地址池为认证前的 Portal 用户分配 IP 地址时，该指定的 IP 地址池必须存在且配置完整，否则无法为 用户分配 地址，并导致用户无法进行 认证。
Portal IP Portal若 用户不进行认证，或认证失败，已分配的地址不会被收回。
Portal

##### 3. 配置步骤

(1) 进入系统视图。
system-view

(2) 进入三层接口视图。
interface interface-type interface-number
(3) 配置 Portal 认证前用户使用的地址池。
portal [ ipv6 ] pre-auth ip-pool pool-name
缺省情况下，接口上未配置 Portal 认证前用户使用的地址池。

#### 1.11 指定Portal用户使用的认证域

##### 1.11.1 功能简介

每个 Portal 用户都属于一个认证域，且在其所属的认证域内进行认证/授权/计费，认证域中定义了一套认证/授权/计费的策略。
通过配置 Portal 用户使用的认证域，使得所有接入的 Portal 用户被强制使用指定的认证域来进行认证、授权和计费。即使 用户输入的用户名中携带的域名相同，接入设备的管理员也可以通过Portal该配置使得不同接口上接入的 Portal 用户使用不同的认证域，从而增加管理员部署 Portal 接入策略的灵活性。

##### 1.11.2 配置限制和指导

Portal 用户将按照如下先后顺序选择认证域：接口上指定的 Portal 用户使用的 ISP 域-->用户名中携带的 ISP 域-->系统缺省的 ISP 域。如果根据以上原则决定的认证域在设备上不存在，但设备上为未知域名的用户指定了 ISP 域，则最终使用该指定的 ISP 域认证。否则，用户将无法认证。关于 ISP域的相关介绍请参见“安全配置指导”中的“AAA”。
对于认证域中指定的授权 ACL，需要注意的是：
如果有流量匹配上该授权 规则，设备将按照规则中指定的 或 动作进行处
• ACL permit deny理。
• 如果没有流量匹配上该授权 ACL 规则，设备将允许所有报文通过，用户可以直接访问网络。
该授权 中不要配置源 地址或源 地址信息，否则，可能会导致引用该
• ACL IPv4/IPv6 MAC ACL的用户不能正常上线。

##### 1.11.3 配置接口上Portal用户使用的认证域

(1) 进入系统视图。
system-view
(2) 进入三层接口视图。
interface interface-type interface-number
(3) 配置接口上 Portal 用户使用的认证域。
portal [ ipv6 ] domain domain-name
缺省情况下，接口上未配置 Portal 用户使用的认证域。
接口上可以同时配置 IPv4 Portal 用户和 IPv6 Portal 用户的认证域。

#### 1.12 控制Portal用户的接入

##### 1.12.1 配置免认证规则

###### 1. 功能简介

免认证规则的匹配项包括主机名、IP 地址、TCP/UDP 端口号、MAC 地址、所连接设备的接口和VLAN，只有符合免认证规则的用户报文才不会触发 Portal 认证，因此这些报文所属的用户不需要通过 Portal 认证即可访问网络资源。

###### 2. 配置限制和指导

如果免认证规则中同时配置了接口和 VLAN，则要求接口属于指定的 VLAN，否则该规则无效。
相同内容的免认证规则不能重复配置，否则提示免认证规则已存在或重复。
无论接口上是否开启 Portal 认证，只能添加或者删除免认证规则，不能修改。

###### 3. 配置基于IP地址的免认证规则

进入系统视图。
(1)
system-view配置基于 地址的 免认证规则。
(2) IP Portal（IPv4 网络）
portal free-rule rule-number { destination ip { ipv4-address { mask-length | mask } | any } [ tcp tcp-port-number | udp udp-port-number ] | source ip { ipv4-address { mask-length | mask } | any } [ tcp tcp-port-number | udp udp-port-number ] } * [ interface interface-type interface-number ]（IPv6 网络）
portal free-rule rule-number { destination ipv6 { ipv6-address prefix-length | any } [ tcp tcp-port-number | udp udp-port-number ] | source ipv6 { ipv6-address prefix-length | any } [ tcp tcp-port-number | udp udp-port-number ] } * [ interface interface-type interface-number ]

###### 4. 配置基于源的免认证规则

进入系统视图。
(1)
system-view
(2) 配置基于源的 Portal 免认证规则。
portal free-rule rule-number source { interface interface-type interface-number | mac mac-address | vlan vlan-id } *关键字仅对通过 接口接入的 用户生效。
vlan VLAN Portal

###### 5. 配置基于目的的免认证规则

(1) 进入系统视图。
system-view
(2) 配置基于目的 Portal 免认证规则。
portal free-rule rule-number destination host-name

###### 3. 配置步骤

缺省情况下，不存在基于目的的 Portal 免认证规则。

##### 1.12.2 配置源认证网段

###### 1. 功能简介

通过配置源认证网段实现只允许在源认证网段范围内的用户 报文才能触发 认HTTP/HTTPS Portal证。如果未认证用户的 HTTP/HTTPS 报文既不满足免认证规则又不在源认证网段内，则将被接入设备丢弃。

###### 2. 配置限制和指导

源认证网段配置仅对可跨三层 Portal 认证有效。
直接认证方式和二次地址分配认证方式下，用户与接入设备上开启 Portal 的接口在同一个网段，因此配置源认证网段没有实际意义。对于直接认证方式，接入设备认为接口上的源认证网段为任意源IP；对于二次地址分配认证方式，接入设备认为接口上的源认证网段为接口私网 IP 决定的私网网段。
如果接口上同时配置了源认证网段和目的认证网段，则源认证网段的配置不会生效。
设备上可以配置多条源认证网段。若配置了网段地址范围有所覆盖或重叠的源认证网段，则仅其中地址范围最大（子网掩码或地址前缀最小）的一条源认证网段配置生效。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 进入三层接口视图。
interface interface-type interface-number
(3) 配置源认证网段。
（IPv4 网络）
portal layer3 source ipv4-network-address { mask-length | mask }（IPv6 网络）
portal ipv6 layer3 source ipv6-network-address prefix-length缺省情况下，对任意用户都进行 Portal 认证。

##### 1.12.3 配置目的认证网段

###### 1. 功能简介

通过配置目的认证网段实现仅对要访问指定目的网段（除免认证规则中指定的目的 IP 地址或网段）
的用户进行 Portal 认证，用户访问非目的认证网段时无需认证，可直接访问。

###### 2. 配置限制和指导

如果接口上同时配置了源认证网段和目的认证网段，则源认证网段的配置无效。
设备上可以配置多条目的认证网段。若配置了网段地址范围有所覆盖或重叠的目的认证网段，则仅其中地址范围最大（子网掩码或地址前缀最小）的一条目的认证网段配置生效。

###### 3. 配置步骤

(1) 进入系统视图。

system-view
(2) 进入三层接口视图。
interface interface-type interface-number
(3) 配置目的认证网段。
（IPv4 网络）
portal free-all except destination ipv4-network-address { mask-length | mask }（IPv6 网络）
portal ipv6 free-all except destination ipv6-network-address prefix-length缺省情况下，对访问任意目的网段的用户都进行 认证。
Portal

##### 1.12.4 配置第二类Portal过滤规则下发的完整性检查功能

###### 1. 功能简介

缺省情况下，用户通过认证后，只要有一块单板成功下发第二类 过滤规则，用户就可以上线，Portal对于通过全局接口接入的用户，上线后可能会无法正常访问网络。开启本功能后，只有设备上所有单板都成功下发第二类 Portal 过滤规则，才会允许用户上线。在全局接口上使能 Portal 认证时，建议配置下发第二类 过滤规则的完整性检查功能，可确保用户上线后可以正常访问网络。
Portal缺省情况下，用户通过认证后，只要有一个成员设备成功下发第二类 过滤规则，用户就可以Portal上线，对于通过全局接口接入的用户，上线后可能会无法正常访问网络。配置本功能后，只有设备上所有成员设备都成功下发第二类 Portal 过滤规则，才会允许用户上线。在全局接口上使能 Portal认证时，建议配置下发第二类 Portal 过滤规则的完整性检查功能，可确保用户上线后可以正常访问网络。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置第二类 Portal 过滤规则下发的完整性检查功能。
portal user-rule assign-check enable
缺省情况下，第二类 过滤规则下发的完整性检查功能处于关闭状态。
Portal

##### 1.12.5 配置Portal最大用户数

###### 1. 功能简介

通过配置可以控制系统中的全局 Portal 接入用户总数和每个接口上的最大 Portal 用户数（包括 IPv4 Portal 用户和 IPv6 Portal 用户）。

###### 2. 配置限制和指导

建议将全局最大Portal用户数配置为所有开启Portal的接口上的最大IPv4 Portal用户数和最大IPv6用户数之和，但不超过整机最大 用户数，否则会有部分 用户因为整机最大用户Portal Portal Portal数已达到而无法上线。

###### 1. 功能简介

###### 3. 配置全局Portal最大用户数

(1) 进入系统视图。
system-view
(2) 配置全局 Portal 最大用户数。
portal max-user max-number
缺省情况下，不限制 Portal 最大用户数。
如果配置的全局 Portal 最大用户数小于当前已经在线的 Portal 用户数，则配置可以执行成功，
且在线 Portal 用户不受影响，但系统将不允许新的 Portal 用户接入。

###### 4. 配置接口上Portal最大用户数

(1) 进入系统视图。
system-view
(2) 进入三层接口视图。
interface interface-type interface-number
(3) 配置 Portal 最大用户数。
portal { ipv4-max-user | ipv6-max-user } max-number
缺省情况下，接口上的 Portal 最大用户数不受限制。
如果接口上配置的 Portal 最大用户数小于当前接口上已经在线的 Portal 用户数，则配置可以
执行成功，且在线 Portal 用户不受影响，但系统将不允许新的 Portal 用户从该接口接入。

##### 1.12.6 配置Portal授权信息严格检查模式

功能简介
1.
严格检查模式用于配合服务器上的用户授权控制策略，允许成功下发了授权信息的用户在线。
开启 Portal 授权信息的严格检查模式后，当认证服务器下发的授权 ACL、User Profile 在设备上不存在或者设备下发 失败时，设备将强制 用户下线。若同时开启了对授权 和User Profile Portal ACL对授权 User Profile 的严格检查模式，则只要其中任意一个授权属性未通过严格授权检查，则用户就会下线。

###### 2. 在接口上配置Portal授权信息严格检查模式

(1) 进入系统视图。
system-view
(2) 进入三层接口视图。
interface interface-type interface-number
(3) 配置 Portal 授权信息的严格检查模式。
portal authorization { acl | user-profile } strict-checking
缺省情况下，Portal 授权信息处于非严格检查模式，即当认证服务器下发的授权 ACL、User
Profile 在设备上不存在或者设备下发 User Profile 失败时，允许 Portal 用户在线。

###### 1. 功能简介

##### 1.12.7 配置Portal仅允许DHCP用户上线

功能简介
1.
为了保证只有合法 IP 地址的用户能够接入，可以配置仅允许 DHCP 用户上线功能，配置此功能后，地址为静态配置的 认证用户将不能上线。
IP Portal

###### 2. 配置限制和指导

本功能仅在采用接入设备作为 DHCP 服务器的组网中生效。
在 网络中，开启本功能后，终端仍会使用临时 地址进行 认证，从而导致认证失败，IPv6 IPv6 Portal所以终端必须关闭临时 IPv6 地址。
此配置不会影响已经在线的用户。

###### 3. 在接口上配置Portal仅允许DHCP用户上线功能

(1) 进入系统视图。
system-view
(2) 进入三层接口视图。
interface interface-type interface-number
(3) 开启 Portal 仅允许 DHCP 用户上线功能。
portal [ ipv6 ] user-dhcp-only
缺省情况下，通过DHCP方式获取IP地址的客户端和配置静态IP地址的客户端都可以上线。

##### 1.12.8 配置Portal支持Web代理

###### 1. 功能简介

设备默认只允许未配置 Web 代理服务器的用户浏览器发起的 HTTP 请求才能触发 Portal 认证。若用户使用配置了 Web 代理服务器的浏览器上网，则用户的这类 HTTP 请求报文将被丢弃，而不能触发 认证。这种情况下，网络管理员可以通过在设备上添加 代理服务器的 端口号，Portal Web TCP来允许使用 Web 代理服务器的用户浏览器发起的 HTTP 请求也可以触发 Portal 认证。

###### 2. 配置限制和指导

如果用户浏览器采用 WPAD（Web Proxy Auto-Discovery，Web 代理服务器自动发现）方式自动配置 Web 代理，需要注意以下几点：
• 需要网络管理员在设备上添加 Web 代理服务器端口，同时配置免认证规则，允许目的 IP 为主机 地址的用户报文免认证。
WPAD IP需要用户在浏览器上将 认证服务器的 地址配置为 代理服务器的例外地址，避
• Portal IP Web免 Portal 用户发送给 Portal 认证服务器的 HTTP 报文被发送到 Web 代理服务器上，从而影响正常的 Portal 认证。
目前，不支持配置 Portal 认证 Web 代理服务器的端口号为 443。
多次配置本命令可以添加多个 Web 代理服务器的 TCP 端口号，其中任意一个端口号发起的 HTTP请求均可触发 Portal 认证。

###### 3. 配置步骤

进入系统视图。
(1)

###### 2. 配置步骤

system-view
(2) 配置允许触发 Portal 认证的 Web 代理服务器端口。
portal web-proxy port port-number

##### 1.12.9 配置Portal用户漫游功能

###### 1. 功能简介

Portal 用户漫游功能允许同属一个 VLAN 的用户在 VLAN 内漫游，即只要 Portal 用户在某 VLAN 接口通过认证，则可以在该 内的任何二层端口上访问网络资源，且移动接入端口时无须重复认VLAN证。若 VLAN 接口上未开启该功能，则在线用户在同一个 VLAN 内其它端口接入时，将无法访问外部网络资源，必须首先在原端口正常下线之后，才能在其它端口重新认证上线。

###### 2. 配置限制和指导

该功能只对通过 接口上线的用户有效，对于通过普通三层接口上线的用户无效。
VLAN设备上有用户在线的情况下，不能配置此功能。
Portal用户漫游功能需要在关闭 Portal客户端 Rule ARP/ND表项生成功能（通过命令 undo portal enable）的情况下才能生效。
refresh { arp | nd }

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 开启 Portal 用户漫游功能。
portal roaming enable
缺省情况下，Portal 用户漫游功能处于关闭状态。

##### 1.12.10 配置Portal用户逃生功能

###### 1. 功能简介

当接入设备探测到 Portal 认证服务器或者 Portal Web 服务器不可达时，可打开接口上的网络限制，允许 Portal 用户不需经过认证即可访问网络资源，也就是通常所说的 Portal 逃生功能。
如果接口同时开启了 Portal 认证服务器不可达时的 Portal 用户逃生功能和 Portal Web 服务器不可达时的 Portal 用户逃生功能，则当任意一个服务器不可达时，即取消接口的 Portal 认证功能，当两个服务器均恢复可达性后，再重新启动 认证功能。重新启动接口的 认证功能之后，未Portal Portal通过认证的用户需要通过认证之后才能访问网络资源，已通过认证的用户可继续访问网络资源。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入三层接口视图。
interface interface-type interface-number
(3) 开启 Portal 认证服务器不可达时的 Portal 用户逃生功能。
portal [ ipv6 ] fail-permit server server-name缺省情况下，设备探测到 Portal 认证服务器不可达时，不允许 Portal 用户逃生。

(4) 开启 Portal Web 服务器不可达时的 Portal 用户逃生功能。
portal [ ipv6 ] apply web-server server-name [ fail-permit ]
缺省情况下，设备探测到 Portal Web 服务器不可达时，不允许 Portal 用户逃生。

#### 1.13 配置Portal探测功能

##### 1.13.1 配置Portal用户在线探测功能

###### 1. 功能简介

IPv4 探测类型为 ARP 或 ICMP，IPv6 探测类型为 ND 或 ICMPv6。
根据探测类型的不同，设备有以下两种探测机制：
• 当探测类型为 ICMP/ICMPv6时，若设备发现一定时间（idle time）内接口上未收到某 Portal用户的报文，则会向该用户定期（interval interval）发送 ICMP/ICMPv6 报文。如果在指定探测次数（retry retries）之内，设备收到了该用户的响应报文，则认为用户在线，且停止发送探测报文，重复这个过程，否则，强制其下线。
当探测类型为 时，若设备发现一定时间（idle time）内接口上未收到某 用
• ARP/ND Portal户的报文，则会向该用户发送 ARP/ND 请求报文。设备定期（interval interval）检测用户 ARP/ND 表项是否被刷新过，如果在指定探测次数（retry retries）内用户 ARP/ND表项被刷新过，则认为用户在线，且停止检测用户 ARP/ND 表项，重复这个过程，否则，强制其下线。

###### 2. 配置限制和指导

ARP 和 ND 方式的探测只适用于直接方式和二次地址分配方式的 Portal 认证。ICMP 方式的探测适用于所有认证方式。

###### 3. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入三层接口视图。
interface interface-type interface-number
(3) 开启 Portal 用户在线探测功能。
（IPv4 网络）
portal user-detect type { arp | icmp } [ retry retries ] [ interval interval ] [ idle time ]（IPv6 网络）
portal ipv6 user-detect type { icmpv6 | nd } [ retry retries ] [ interval interval ] [ idle time ]缺省情况下，接口上的 用户在线探测功能处于关闭状态。
Portal

###### 3. 配置步骤

###### 1. 功能简介

##### 1.13.2 配置Portal认证服务器的可达性探测功能

功能简介
1.
在 Portal 认证的过程中，如果接入设备与 Portal 认证服务器的通信中断，则会导致新用户无法上线，已经在线的 用户无法正常下线的问题。为解决这些问题，需要接入设备能够及时探测到Portal Portal认证服务器可达状态的变化，并能触发执行相应的操作来应对这种变化带来的影响。
开启 Portal 认证服务器的可达性探测功能后，设备会定期检测 Portal 认证服务器发送的报文（例如，用户上线报文、用户下线报文、心跳报文）来判断服务器的可达状态：若设备在指定的探测超时时间（timeout timeout）内收到 Portal 报文，且验证其正确，则认为此次探测成功且服务器可达，否则认为此次探测失败，服务器不可达。
当接入设备检测到 认证服务器可达或不可达状态改变时，可执行以下一种或多种操作：
Portal发送日志：Portal 认证服务器可达或者不可达的状态改变时，发送日志信息。日志信息中记录
•了 Portal 认证服务器名以及该服务器状态改变前后的状态。
• Portal用户逃生：Portal认证服务器不可达时，暂时取消接口上进行的Portal认证，允许该接口接入的所有 Portal 用户访问网络资源。之后，若设备收到 Portal 认证服务器发送的报文，则恢复该端口的Portal认证功能。该功能的详细配置请参见“1.12.10 配置Portal用户逃生功能”。

###### 2. 配置限制和指导

只有当设备上存在开启 认证的接口时，Portal 认证服务器的可达性探测功能才生效。
Portal目前，只有 的 认证服务器支持发送心跳报文，由于心跳报文是周期性发送的，所以iMC Portal iMC的 Portal 认证服务器可以更好得与设备配合，使其能够及时而准确地探测到它的可达性状态。如果要采用心跳报文探测 Portal 服务器的可达性，服务器上必须保证逃生心跳功能处于开启状态。
如果同时指定了多种操作，则 Portal 认证服务器可达状态改变时系统可并发执行多种操作。
设备配置的探测超时时间（timeout timeout）必须大于服务器上配置的逃生心跳间隔时间。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 进入 Portal 认证服务器视图。
portal server server-name
(3) 开启 Portal 认证服务器的可达性探测功能。
server-detect [ timeout timeout ] log缺省情况下，Portal 服务器可达性探测功能处于关闭状态。

##### 1.13.3 配置Portal Web服务器的可达性探测功能

###### 1. 功能简介

在 Portal 认证的过程中，如果接入设备与 Portal Web 服务器的通信中断，将无法完成整个认证过程，因此必须对 Portal Web 服务器的可达性进行探测。
由于 Portal Web 服务器用于对用户提供 Web 服务，不需要和设备交互报文，因此无法通过发送某种协议报文的方式来进行可达性检测。无论是否有接口上开启了 认证，开启了Portal Portal Web服务器的可达性探测功能之后，接入设备采用模拟用户进行 Web 访问的过程来实施探测：接入设

###### 3. 配置步骤

备主动向 Portal Web 服务器发起 TCP 连接，如果连接可以建立，则认为此次探测成功且服务器可达，否则认为此次探测失败。
探测参数
•探测间隔：进行探测尝试的时间间隔。
(cid:123)
失败探测的最大次数：允许连续探测失败的最大次数。若连续探测失败数目达到此值，则(cid:123)
认为服务器不可达。
• 可达状态改变时触发执行的操作（可以选择其中一种或同时使用多种）
发送日志：Portal Web 服务器可达或者不可达的状态改变时，发送日志信息。日志信息中(cid:123)
记录了 Portal Web 服务器名以及该服务器状态改变前后的状态。
Portal用户逃生：Portal Web服务器不可达时，暂时取消端口进行的Portal认证，允许该端(cid:123)
口接入的所有Portal用户访问网络资源。之后，若Portal Web服务器可达，则恢复该端口的Portal认证功能。该功能的详细配置请参见“1.12.10 配置Portal用户逃生功能”。

###### 2. 配置限制和指导

只有当配置了 Portal Web 服务器的 URL 地址，且设备上存在开启 Portal 认证接口时，该 Portal Web服务器的可达性探测功能才生效。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 进入 Portal Web 服务器视图。
portal web-server server-name
(3) 开启 Portal Web 服务器的可达性探测功能。
server-detect [ interval interval ] [ retry retries ] log缺省情况下，Portal Web 认证服务器的可达性探测功能处于关闭状态。

##### 1.13.4 配置Portal用户信息同步功能

###### 1. 功能简介

为了解决接入设备与 Portal 认证服务器通信中断后，两者的 Portal 用户信息不一致问题，设备提供了一种 Portal 用户信息同步功能。该功能利用了 Portal 同步报文的发送及检测机制，具体实现如下：
(1) 由 Portal 认证服务器周期性地（周期为 Portal 认证服务器上指定的用户心跳间隔值）将在线用户信息通过用户同步报文发送给接入设备；
接入设备在用户上线之后，即开启用户同步检测定时器（超时时间为 timeout timeout），
(2)
在收到用户同步报文后，将其中携带的用户列表信息与自己的用户列表信息进行对比，如果发现同步报文中有设备上不存在的用户信息，则将这些自己没有的用户信息反馈给 Portal 认证服务器，Portal 认证服务器将删除这些用户信息；如果发现接入设备上的某用户信息在一个用户同步报文的检测超时时间内，都未在该 认证服务器发送过来的用户同步报文中出Portal现过，则认为 Portal 认证服务器上已不存在该用户，设备将强制该用户下线。

###### 2. 配置限制和指导

只有在支持 Portal 用户心跳功能（目前仅 iMC 的 Portal 认证服务器支持）的 Portal 认证服务器的配合下，本功能才有效。为了实现该功能，还需要在 Portal 认证服务器上选择支持用户心跳功能，且服务器上配置的用户心跳间隔要小于等于设备上配置的检测超时时间。
在设备上删除 认证服务器时将会同时删除该服务器的用户信息同步功能配置。
Portal

###### 3. 配置步骤

(1) 进入系统视图。
system-view
进入 认证服务器视图。
(2) Portal
portal server server-name
开启 用户信息同步功能。
(3) Portal
user-sync timeout timeout
缺省情况下，Portal 用户信息同步功能处于关闭状态。

#### 1.14 配置Portal报文属性

##### 1.14.1 配置BAS-IP/BAS-IPv6属性

###### 1. 功能简介

设备上运行 Portal 2.0 版本时，主动发送给 Portal 认证服务器的报文（例如强制用户下线报文）中必须携带 BAS-IP 属性。设备上运行 Portal 3.0 版本时，主动发送给 Portal 认证服务器的报文必须携带 或者 属性。若配置此功能，设备主动发送的通知类 报文，其源 地BAS-IP BAS-IPv6 Portal IP址为配置的 BAS-IP 或 BAS-IPv6 属性值，否则为 Portal 报文出接口的 IP 地址。

###### 2. 配置限制和指导

设备进行二次地址分配认证和强制 Portal 用户下线过程中，均需要设备主动向 Portal 认证服务器发送相应的通知类 Portal 报文，因此，为了保证二次地址分配认证方式下 Portal 用户可以成功上线，以及设备可以成功通知 Portal 认证服务器用户下线，需要保证 BAS-IP/BAS-IPv6 属性值与 Portal认证服务器上指定的设备 IP 一致。
使用 H3C iMC 的 Portal 认证服务器的情况下，如果 Portal 服务器上指定的设备 IP 不是设备上 Portal报文出接口的 IP 地址，则开启了 Portal 认证的接口上必须配置 BAS-IP 或者 BAS-IPv6 属性与 Portal认证服务器上指定的设备 一致。
IP

###### 3. 在接口上配置BAS-IP/BAS-IPv6属性

(1) 进入系统视图。
system-view
进入三层接口视图。
(2)
interface interface-type interface-number
配置 或 属性。
(3) BAS-IP BAS-IPv6
（IPv4 网络）
portal bas-ip ipv4-address

###### 3. 配置步骤

缺省情况下，发送给 Portal 认证服务器的响应类的 IPv4 Portal 报文中携带的 BAS-IP 属性为报文的源 地址，通知类 报文中携带的 属性为报文出接口的 地IPv4 IPv4 Portal BAS-IP IPv4址。
（IPv6 网络）
portal bas-ipv6 ipv6-address缺省情况下，发送给 Portal 认证服务器的响应类的 IPv6 Portal 报文中携带的 BAS-IPv6 属性为报文的源 IPv6 地址，通知类 IPv6 Portal 报文中携带的 BAS-IPv6 属性为报文出接口的 IPv6地址。

##### 1.14.2 配置接入设备的ID

###### 1. 功能简介

通过配置接入设备的 ID，使得接入设备向 认证服务器发送的协议报文中携带一个属性，此属Portal性用于向 Portal 服务器标识发送协议报文的接入设备。

###### 2. 配置限制和指导

不同设备的设备 ID 不能相同。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 配置接入设备的 ID。
portal device-id device-id缺省情况下，未配置任何设备的 ID。

#### 1.15 配置RADIUS报文属性

##### 1.15.1 配置RADIUS NAS-Port-ID属性格式

###### 1. 功能简介

不同厂商的 服务器对 报文中的 属性格式要求不同，可修改设备发RADIUS RADIUS NAS-Port-ID送的 RADIUS 报文中填充的 NAS-Port-ID 属性的格式。设备支持四种属性格式，分别为 format 1和 format 2、format 3 和 format 4，这四种属性格式具体要求请参见“安全命令参考”中的“Portal”。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置 NAS-Port-ID 属性的格式。
portal nas-port-id format { 1 | 2 | 3 | 4 }
缺省情况下， NAS-Port-ID 属性的格式为 format 2 。

###### 1. 功能简介

##### 1.15.2 配置接入设备发送的RADIUS请求报文的NAS-Port-Type属性类型

功能简介
1.
RADIUS 标准属性 NAS-Port-Type 用于表示用户接入的端口类型。若 Portal 认证接入设备与 Portal客户端之间跨越了多个网络设备，则可能无法正确获取到用户接入的实际端口信息。网络管理员根据用户实际接入环境，通过本配置指定接入设备发送的 RADIUS 请求报文的 NAS-Port-Type 属性类型，可保证接入设备能够向 RADIUS 服务器准确传递用户的接入端口信息。

###### 2. 配置限制和指导

本功能配置后仅对新接入的 Portal 用户生效，对已上线的 Portal 用户不生效。

###### 3. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置接入设备发送的 RADIUS 请求报文的 NAS-Port-Type 属性类型。
portal nas-port-type { 802.11 | adsl-cap | adsl-dmt | async | cable | ethernet | g.3-fax | hdlc | idsl | isdn-async-v110 | isdn-async-v120 | isdn-sync | piafs | sdsl | sync | virtual | wireless-other | x.25 |
x.75 | xdsl }缺省情况下，接入设备发送的 RADIUS 请求报文中的 NAS-Port-Type 属性类型为 Ethernet，属性值为 15。

##### 1.15.3 配置接口的NAS-ID Profile

###### 1. 功能简介

用户的接入 VLAN 可标识用户的接入位置，而在某些应用环境中，网络运营商需要使用接入设备发送给 RADIUS 服务器的 NAS-Identifier 属性值来标识用户的接入位置，因此接入设备上需要建立用户接入 VLAN 与指定的 NAS-ID 之间的绑定关系。当接口上有 Portal 用户上线时，若该接口上指定了 NAS-ID Profile，则接入设备会根据指定的 Profile 名称和用户接入的 VLAN 来获取与此 VLAN 绑定的 ，此 的值将作为向 服务器发送的 请求报文中的NAS-ID NAS-ID RADIUS RADIUS NAS-Identifier 属性值。

###### 2. 配置限制和指导

如果接口上指定了 NAS-ID Profile，则此 Profile 中定义的绑定关系优先使用；如果未指定 NAS-ID Profile 或指定的 Profile 中没有找到匹配的绑定关系，则使用设备名作为 NAS-ID。

###### 3. 配置步骤

进入系统视图。
(1)
system-view创建 Profile，并进入 视图。
(2) NAS-ID NAS-ID-Profile aaa nas-id profile profile-name该命令的具体介绍请参见“安全命令参考”中的“AAA”。

##### 1. 功能简介

##### 3. 配置步骤

(3) 设置 NAS-ID 与 VLAN 的绑定关系。
nas-id nas-identifier bind vlan vlan-id
该命令的具体情况请参见“安全命令参考”中的“AAA”。对于 QinQ 报文，Portal 接入只能
匹配内层VLAN，有关QinQ的详细介绍，请参见“二层技术-以太网交换配置指导”中的“QinQ”。
指定引用的 Profile。
(4) NAS-ID
退回系统视图。
a.
quit
b. 进入三层接口视图。
interface interface-type interface-number
c. 指定引用的 NAS-ID Profile
portal nas-id-profile profile-name

#### 1.16 关闭Portal客户端Rule ARP/ND表项生成功能

##### 1. 功能简介

客户端的 表项生成功能处于开启状态时，Portal 客户端上线后，其Portal Rule ARP/ND ARP/ND表项为 Rule 表项，在 Portal 客户端下线后会被立即删除，导致 Portal 客户端在短时间内再上线时会因 ARP/ND 表项还未学习到而认证失败。此情况下，需要关闭本功能，使得 Portal 客户端上线后其 表项仍为动态表项，在 客户端下线后按老化时间正常老化。
ARP/ND Portal

##### 2. 配置限制和指导

此功能的开启和关闭不影响已经在线的 Portal 客户端的 ARP/ND 表项类型。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 关闭 Portal 客户端 Rule ARP/ND 表项生成功能。
undo portal refresh { arp | nd } enable
缺省情况下，Portal 客户端 Rule ARP/ND 表项生成功能均处于开启状态。

#### 1.17 强制在线Portal用户下线

功能简介
1.
通过配置强制在线用户下线可以终止对用户的 Portal 认证过程，或者将已经通过认证的 Portal 用户删除。

##### 2. 配置限制和指导

当在线用户数目超过 时，执行命令强制在线用户下线需要几分钟的时间，在此期间，请勿进2000行关闭接口上 Portal 功能等操作；否则会导致在线用户删除操作不能正常完成。
配置步骤
3.
(1) 进入系统视图。
system-view

##### 2. 配置步骤

##### 1. 功能简介

(2) 强制指定的在线 Portal 用户或所有在线 Portal 用户下线。
portal delete-user { ipv4-address | all | interface interface-type
interface-number | ipv6 ipv6-address }

#### 1.18 开启Portal用户上/下线日志功能

##### 1. 功能简介

设备开启 Portal 用户上/下线日志功能后，会对用户上线和下线时的信息进行记录，包括用户名、IP地址、接口名称、VLAN、用户 MAC 地址、上线失败原因等。生成的日志信息将被发送到设备的信息中心，通过设置信息中心的参数，决定日志信息的输出规则（即是否允许输出以及输出方向）。
有关信息中心参数的配置请参见“网络管理和监控配置指导”中的“信息中心”。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 开启 Portal 用户上/下线日志功能。
portal log enable缺省情况下，Portal 用户上/下线日志功能处于关闭状态。

#### 1.19 配置Web重定向功能

功能简介
1.
接口上配置了 Web 重定向功能后，当该接口上接入的用户初次通过 Web 页面访问外网时，设备会将用户的初始访问页面重定向到指定的 页面，之后用户才可以正常访问外网。经过一定时长URL（interval）后，设备又可以将用户要访问的网页或者正在访问的网页重定向到指定的 URL 页面。
Web 重定向功能是一种简化的 Portal 功能，它不需要用户通过 Web 访问外部网络之前提供用户名和密码，可通过对用户访问的网页定期重定向的方式为网络服务提供商的业务拓展提供方便，例如可以在重定向的页面上开展广告、信息发布等业务。

##### 2. 配置限制和指导

配置 Web 重定向功能，请遵循以下配置原则：
• Web 重定向功能仅对使用默认端口号 80 的 HTTP 协议报文生效。
• 同时开启 Web 重定向功能和 Portal 功能时，Web 重定向功能失效。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入三层接口视图。
interface interface-type interface-number
(3) 配置 Web 重定向功能。
web-redirect [ ipv6 ] url url-string [ interval interval ]
缺省情况下，Web 重定功能处于关闭状态。

#### 1.20 Portal显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 Portal 的运行情况，通过查看显示信息验证配置的效果。
在用户视图下执行 reset 命令可以清除 Portal 统计信息。
表1-2 Portal 显示和维护操作 命令显示指定接口上的Portal配置信息和Portal运 display portal interface interface-type行状态信息 interface-number display portal packet statistics [ server显示Portal认证服务器的报文统计信息server-name ] display portal rule { all | dynamic | static }显示用于报文匹配的Portal过滤规则信息 interface interface-type interface-number [ slot slot-number ]显示Portal认证服务器信息 display portal server [ server-name ] display portal user { all | interface interface-type interface-number | ip显示Portal用户的信息 ipv4-address | ipv6 ipv6-address | pre-auth [ interface interface-type interface-number | ip ipv4-address | ipv6 ipv6-address ] } [ verbose ]显示Portal Web服务器信息 display portal web-server [ server-name ] display web-redirect rule interface指定接口上的Web重定向过滤规则信息 interface-type interface-number [ slot slot-number ] reset portal packet statistics [ server清除Portal认证服务器的报文统计信息server-name ]

#### 1.21 Portal典型配置举例

##### 1.21.1 Portal直接认证配置举例

###### 1. 组网需求

• 用户主机与接入设备 Switch 直接相连，采用直接方式的 Portal 认证。用户通过手工配置或
DHCP 获取的一个公网 IP 地址进行认证，在通过 Portal 认证前，只能访问 Portal Web 服务器；
在通过 Portal 认证后，可以使用此 IP 地址访问非受限互联网资源。
• 采用一台 Portal 服务器承担 Portal 认证服务器和 Portal Web 服务器的职责。
• 采用 RADIUS 服务器作为认证/计费服务器。

###### 2. 组网图

图1-6 配置 Portal 直接认证组网图

###### 3. 配置步骤

按照组网图配置设备各接口的 IP 地址，保证启动 Portal 之前各主机、服务器和设备之间的路由
•可达。
完成 服务器上的配置，保证用户的认证/计费功能正常运行。
• RADIUS
(1) 配置 Portal server（iMC PLAT 3.20）
下面以 iMC 为例（使用 iMC 版本为：iMC PLAT 3.20-R2602P13、iMC UAM 3.60-E6301），说明 Portal server 的基本配置。
\# 配置 Portal 认证服务器。
登录进入 iMC 管理平台，选择“业务”页签，单击导航树中的[Portal 认证服务器管理/服务器配置]菜单项，进入服务器配置页面。
根据实际组网情况调整以下参数，本例中使用缺省配置。

图1-7 Portal 认证服务器配置页面\# 配置 IP 地址组。
单击导航树中的[Portal 认证服务器管理/IP 地址组配置]菜单项，进入 Portal IP 地址组配置页面，在该页面中单击<增加>按钮，进入增加 IP 地址组配置页面。
填写 IP 地址组名。
(cid:123)
输入起始地址和终止地址。用户主机 IP 地址必须包含在该 IP 地址组范围内。
(cid:123)
选择业务分组，本例中使用缺省的“未分组”。
(cid:123)
选择 IP 地址组的类型为“普通”。
(cid:123)
图1-8 增加 IP 地址组配置页面\# 增加 Portal 设备。
单击导航树中的[Portal 认证服务器管理/设备配置]菜单项，进入 Portal 设备配置页面，在该页面中单击<增加>按钮，进入增加设备信息配置页面。
填写设备名。
(cid:123)
指定 IP 地址为与接入用户相连的设备接口 IP。
(cid:123)
输入密钥，与接入设备 Switch 上的配置保持一致。
(cid:123)
选择是否进行二次地址分配，本例中为直接认证，因此为否。
(cid:123)
选择是否支持逃生心跳功能和用户心跳功能，本例中不支持。
(cid:123)

图1-9 增加设备信息配置页面\# Portal 设备关联 IP 地址组。
在 Portal 设备配置页面中的设备信息列表中，点击 NAS 设备的<端口组信息管理>链接，进入端口组信息配置页面。
图1-10 设备信息列表在端口组信息配置页面中点击<增加>按钮，进入增加端口组信息配置页面。
填写端口组名。
(cid:123)
选择 IP 地址组，用户接入网络时使用的 IP 地址必须属于所选的 IP 地址组。
(cid:123)
其它参数采用缺省值。
(cid:123)

图1-11 增加端口组信息配置页面最后单击导航树中的[业务参数配置/系统配置手工生效]菜单项，使以上 认证服务器配\# Portal置生效。
(2) 配置 Portal server（iMC PLAT 5.0）
下面以 为例（使用 版本为：iMC 5.0(E0101)、iMC 5.0(E0101)），说明iMC iMC PLAT UAM Portal server 的基本配置。
配置 认证服务器。
\# Portal登录进入 管理平台，选择“业务”页签，单击导航树中的[Portal 认证服务器管理/服务器iMC配置]菜单项，进入服务器配置页面。
根据实际组网情况调整以下参数，本例中使用缺省配置。

图1-12 Portal 认证服务器配置页面\# 配置 IP 地址组。
单击导航树中的[Portal 认证服务器管理/IP 地址组配置]菜单项，进入 Portal IP 地址组配置页面，在该页面中单击<增加>按钮，进入增加 IP 地址组配置页面。
填写 IP 地址组名。
(cid:123)
输入起始地址和终止地址。用户主机 IP 地址必须包含在该 IP 地址组范围内。
(cid:123)
选择业务分组，本例中使用缺省的“未分组”。
(cid:123)
选择 IP 地址组的类型为“普通”。
(cid:123)
图1-13 增加 IP 地址组配置页面\# 增加 Portal 设备。
单击导航树中的[Portal 认证服务器管理/设备配置]菜单项，进入 Portal 设备配置页面，在该页面中单击<增加>按钮，进入增加设备信息配置页面。
填写设备名。
(cid:123)

指定 IP 地址为与接入用户相连的设备接口 IP。
(cid:123)
输入密钥，与接入设备 Switch 上的配置保持一致。
(cid:123)
选择是否进行二次地址分配，本例中为直接认证，因此为否。
(cid:123)
选择是否支持逃生心跳功能和用户心跳功能，本例中不支持。
(cid:123)
图1-14 增加设备信息配置页面\# Portal 设备关联 IP 地址组。
在 Portal 设备配置页面中的设备信息列表中，点击 NAS 设备的<端口组信息管理>链接，进入端口组信息配置页面。
图1-15 设备信息列表在端口组信息配置页面中点击<增加>按钮，进入增加端口组信息配置页面。
填写端口组名。
(cid:123)
选择 IP 地址组，用户接入网络时使用的 IP 地址必须属于所选的 IP 地址组。
(cid:123)
其它参数采用缺省值。
(cid:123)

图1-16 增加端口组信息配置页面\# 最后单击导航树中的[业务参数配置/系统配置手工生效]菜单项，使以上 Portal 认证服务器配置生效。
配置
(3) Switch配置 方案RADIUS (cid:123)
创建名称为 的 方案并进入该方案视图。
\# rs1 RADIUS <Switch> system-view [Switch] radius scheme rs1 \# 配置 RADIUS 方案的主认证和主计费服务器及其通信密钥。
[Switch-radius-rs1] primary authentication 192.168.0.112 [Switch-radius-rs1] primary accounting 192.168.0.112 [Switch-radius-rs1] key authentication simple radius [Switch-radius-rs1] key accounting simple radius \# 配置发送给 RADIUS 服务器的用户名不携带 ISP 域名。
[Switch-radius-rs1] user-name-format without-domain [Switch-radius-rs1] quit开启 功能。
\# RADIUS session control [Switch] radius session-control enable配置认证域(cid:123)
\# 创建并进入名称为 dm1 的 ISP 域。
[Switch] domain dm1 \# 配置 ISP 域的 AAA 方法。
[Switch-isp-dm1] authentication portal radius-scheme rs1 [Switch-isp-dm1] authorization portal radius-scheme rs1 [Switch-isp-dm1] accounting portal radius-scheme rs1 [Switch-isp-dm1] quit \# 配置系统缺省的 ISP 域 dm1，所有接入用户共用此缺省域的认证和计费方法。若用户登录时输入的用户名未携带 ISP 域名，则使用缺省域下的认证方法。
[Switch] domain default enable dm1

###### 4. 验证配置

配置 Portal 认证(cid:123)
\# 配置 Portal 认证服务器：名称为 newpt，IP 地址为 192.168.0.111，密钥为明文 portal，监听 报文的端口为 50100。
Portal [Switch] portal server newpt [Switch-portal-server-newpt] ip 192.168.0.111 key simple portal [Switch-portal-server-newpt] port 50100 [Switch-portal-server-newpt] quit \# 配置 Portal Web 服务器的 URL 为 http://192.168.0.111:8080/portal。（Portal Web 服务器的 请与实际环境中的 服务器配置保持一致，此处仅为示例）
URL Portal Web [Switch] portal web-server newpt [Switch-portal-websvr-newpt] url http://192.168.0.111:8080/portal [Switch-portal-websvr-newpt] quit在接口 上开启直接方式的 认证。
\# Vlan-interface100 Portal [Switch] interface vlan-interface 100 [Switch–Vlan-interface100] portal enable method direct \# 在接口 Vlan-interface100 上引用 Portal Web 服务器 newpt。
[Switch–Vlan-interface100] portal apply web-server newpt \# 在接口 Vlan-interface100 上设置发送给 Portal 认证服务器的 Portal 报文中的 BAS-IP 属性值为 2.2.2.1。
[Switch–Vlan-interface100] portal bas-ip 2.2.2.1 [Switch–Vlan-interface100] quit验证配置
4.
\# 以上配置完成后，通过执行以下显示命令可查看 Portal 配置是否生效。
[Switch] display portal interface vlan-interface 100 Portal information of Vlan-interface100 NAS-ID profile: Not configured Authorization : Strict checking ACL : Disabled User profile : Disabled IPv4:
Portal status: Enabled Portal authentication method: Direct Portal web server: newpt Portal mac-trigger-server: Not configured Authentication domain: Not configured Pre-auth domain: Not configured User-dhcp-only: Disabled Pre-auth IP pool: Not configured Max Portal users: Not configured Bas-ip: 2.2.2.1 User detection: Not configured Action for server detection:
Server type Server name Action
-- -- -- Layer3 source network:
IP address Mask

Destination authenticate subnet:
IP address Mask IPv6:
Portal status: Disabled Portal authentication method: Disabled Portal web server: Not configured Portal mac-trigger-server: Not configured Authentication domain: Not configured Pre-auth domain: Not configured User-dhcp-only: Disabled Pre-auth IP pool: Not configured Max Portal users: Not configured Bas-ipv6: Not configured User detection: Not configured Action for server detection:
Server type Server name Action
-- -- -- Layer3 source network:
IP address Prefix length Destination authenticate subnet:
IP address Prefix length用户既可以使用 H3C 的 iNode 客户端，也可以通过网页方式进行 Portal 认证。用户在通过认证前，只能访问认证页面 http://192.168.0.111:8080/portal，且发起的 Web 访问均被重定向到该认证页面，在通过认证后，可访问非受限的互联网资源。
\# Portal 用户认证通过后，可通过执行以下显示命令查看 Switch 上生成的 Portal 在线用户信息。
[Switch] display portal user interface vlan-interface 100 Total portal users: 1 Username: abc Portal server: newpt State: Online VPN instance: N/A MAC IP VLAN Interface 0015-e9a6-7cfe 2.2.2.2 100 Vlan-interface100 Authorization information:
DHCP IP pool: N/A User profile: N/A Session group profile: N/A ACL: N/A Inbound CAR: N/A Outbound CAR: N/A

###### 1. 组网需求

##### 1.21.2 Portal二次地址分配认证配置举例

组网需求
1.
• 用户主机与接入设备 Switch 直接相连，采用二次地址分配方式的 Portal 认证。用户通过 DHCP服务器获取 地址，Portal 认证前使用分配的一个私网地址；通过 认证后，用户申请IP Portal到一个公网地址，才可以访问非受限互联网资源。
• 采用一台 Portal 服务器承担 Portal 认证服务器和 Portal Web 服务器的职责。
采用 服务器作为认证/计费服务器。
• RADIUS

###### 2. 组网图

图1-17 配置 Portal 二次地址分配认证组网图Portal Server
192.168.0.111/24 Vlan-int100
20.20.20.1/24 Vlan-int2
10.0.0.1/24 sub 192.168.0.100/24 Host Switch DHCP server automatically obtains 192.168.0.112/24 an IP address RADIUS server
192.168.0.113/24

###### 3. 配置步骤

Portal 二次地址分配认证方式应用中，DHCP 服务器上需创建公网地址池（20.20.20.0/24）及
•私网地址池（10.0.0.0/24），具体配置略。
二次地址分配认证方式应用中，接入设备需要配置 中继来配合 认证，且启
• Portal DHCP Portal动 Portal 的接口需要配置主 IP 地址（公网 IP）及从 IP 地址（私网 IP）。关于 DHCP 中继的详细配置请参见“三层技术-IP 业务配置指导”中的“DHCP 中继”。
• 请保证在 Portal 认证服务器上添加的 Portal 设备的 IP 地址为与用户相连的接口的公网 IP 地址（20.20.20.1），且与该 设备关联的 地址组中的转换前地址为用户所在的私网网段Portal IP（10.0.0.0/24）、转换后地址为公网网段（20.20.20.0/24）。
• 按照组网图配置设备各接口的 IP 地址，保证启动 Portal 之前各主机、服务器和设备之间的路由可达。
• 完成 RADIUS 服务器上的配置，保证用户的认证/计费功能正常运行。
配置 方案
(1) RADIUS创建名称为 的 方案并进入该方案视图。
\# rs1 RADIUS <Switch> system-view

[Switch] radius scheme rs1 \# 配置 RADIUS 方案的主认证和主计费服务器及其通信密钥。
[Switch-radius-rs1] primary authentication 192.168.0.113 [Switch-radius-rs1] primary accounting 192.168.0.113 [Switch-radius-rs1] key authentication simple radius [Switch-radius-rs1] key accounting simple radius配置发送给 服务器的用户名不携带 域名。
\# RADIUS ISP [Switch-radius-rs1] user-name-format without-domain [Switch-radius-rs1] quit \# 开启 RADIUS session control 功能。
[Switch] radius session-control enable配置认证域
(2)
创建并进入名称为 的 域。
\# dm1 ISP [Switch] domain dm1 \# 配置 ISP 域的 AAA 方法。
[Switch-isp-dm1] authentication portal radius-scheme rs1 [Switch-isp-dm1] authorization portal radius-scheme rs1 [Switch-isp-dm1] accounting portal radius-scheme rs1 [Switch-isp-dm1] quit \# 配置系统缺省的 ISP 域 dm1，所有接入用户共用此缺省域的认证和计费方法。若用户登录时输入的用户名未携带 ISP 域名，则使用缺省域下的认证方法。
[Switch] domain default enable dm1配置 中继和授权
(3) DHCP ARP配置 中继。
\# DHCP [Switch] dhcp enable [Switch] dhcp relay client-information record [Switch] interface vlan-interface 100 [Switch–Vlan-interface100] ip address 20.20.20.1 255.255.255.0 [Switch–Vlan-interface100] ip address 10.0.0.1 255.255.255.0 sub [Switch-Vlan-interface100] dhcp select relay [Switch-Vlan-interface100] dhcp relay server-address 192.168.0.112 \# 开启授权 ARP 功能。
[Switch-Vlan-interface100] arp authorized enable [Switch-Vlan-interface100] quit配置 认证
(4) Portal配置 认证服务器：名称为 newpt，IP 地址为 192.168.0.111，密钥为明文 portal，监\# Portal听 Portal 报文的端口为 50100。
[Switch] portal server newpt [Switch-portal-server-newpt] ip 192.168.0.111 key simple portal [Switch-portal-server-newpt] port 50100 [Switch-portal-server-newpt] quit \# 配置 Portal Web 服务器的 URL 为 http://192.168.0.111:8080/portal。（Portal Web 服务器的 请与实际环境中的 服务器配置保持一致，此处仅为示例）
URL Portal Web [Switch] portal web-server newpt

###### 4. 验证配置

[Switch-portal-websvr-newpt] url http://192.168.0.111:8080/portal [Switch-portal-websvr-newpt] quit \# 在接口 Vlan-interface100 上开启二次地址方式的 Portal 认证。
[Switch] interface vlan-interface 100 [Switch–Vlan-interface100] portal enable method redhcp \# 在接口 Vlan-interface100 上引用 Portal Web 服务器 newpt。
[Switch–Vlan-interface100] portal apply web-server newpt在接口 上设置发送给 报文中的 属性值为 20.20.20.1。
\# Vlan-interface100 Portal BAS-IP [Switch–Vlan-interface100] portal bas-ip 20.20.20.1 [Switch–Vlan-interface100] quit验证配置
4.
\# 以上配置完成后，通过执行以下显示命令可查看 Portal 配置是否生效。
[Switch] display portal interface vlan-interface 100 Portal information of Vlan-interface100 NAS-ID profile: Not configured Authorization : Strict checking ACL : Disabled User profile : Disabled IPv4:
Portal status: Enabled Portal authentication method: Redhcp Portal web server: newpt Portal mac-trigger-server: Not configured Authentication domain: Not configured Pre-auth domain: Not configured User-dhcp-only: Disabled Pre-auth IP pool: Not configured Max Portal users: Not configured Bas-ip: 20.20.20.1 User detection: Not configured Action for server detection:
Server type Server name Action
-- -- -- Layer3 source network:
IP address Mask Destination authenticate subnet:
IP address Mask IPv6:
Portal status: Disabled Portal authentication method: Disabled Portal web server: Not configured Portal mac-trigger-server: Not configured Authentication domain: Not configured Pre-auth domain: Not configured User-dhcp-only: Disabled Pre-auth IP pool: Not configured

Max Portal users: Not configured Bas-ipv6: Not configured User detection: Not configured Action for server detection:
Server type Server name Action
-- -- -- Layer3 source network:
IP address Prefix length Destination authenticate subnet:
IP address Prefix length在采用二次地址分配方式时，请使用 H3C 的 iNode 客户端进行 Portal 认证。通过认证后，可访问非受限的互联网资源。
\# Portal 用户认证通过后，可通过执行以下显示命令查看 Switch 上生成的 Portal 在线用户信息。
[Switch] display portal user interface vlan-interface 100 Total portal users: 1 Username: abc Portal server: newpt State: Online VPN instance: N/A MAC IP VLAN Interface 0015-e9a6-7cfe 20.20.20.2 100 Vlan-interface100 Authorization information:
DHCP IP pool: N/A User profile: N/A Session group profile: N/A ACL: N/A Inbound CAR: N/A Outbound CAR: N/A

##### 1.21.3 可跨三层Portal认证配置举例

###### 1. 组网需求

Switch A 支持 Portal 认证功能。用户 Host 通过 Switch B 接入到 Switch A。
• 配置 Switch A 采用可跨三层 Portal 认证。用户在未通过 Portal 认证前，只能访问 Portal Web服务器；用户通过 Portal 认证后，可以访问非受限互联网资源。
• 采用一台 Portal 服务器承担 Portal 认证服务器和 Portal Web 服务器的职责。
• 采用 RADIUS 服务器作为认证/计费服务器。

###### 2. 组网图

图1-18 配置可跨三层 Portal 认证组网图

###### 3. 配置步骤

• 请保证在 Portal 认证服务器上添加的 Portal 设备的 IP 地址为与用户相连的接口 IP 地址
（20.20.20.1），且与该 设备关联的 地址组为用户所在网段（8.8.8.0/24）。
Portal IP
按照组网图配置设备各接口的 地址，保证启动 之前各主机、服务器和设备之间的路由
• IP Portal
可达。
• 完成 RADIUS 服务器上的配置，保证用户的认证/计费功能正常运行。
(1) 配置 RADIUS 方案
\# 创建名称为 rs1 的 RADIUS 方案并进入该方案视图。
<SwitchA> system-view
[SwitchA] radius scheme rs1
配置 方案的主认证和主计费服务器及其通信密钥。
\# RADIUS
[SwitchA-radius-rs1] primary authentication 192.168.0.112
[SwitchA-radius-rs1] primary accounting 192.168.0.112
[SwitchA-radius-rs1] key authentication simple radius
[SwitchA-radius-rs1] key accounting simple radius
\# 配置发送给 RADIUS 服务器的用户名不携带 ISP 域名。
[SwitchA-radius-rs1] user-name-format without-domain
[SwitchA-radius-rs1] quit
\# 开启 RADIUS session control 功能。
[SwitchA] radius session-control enable
(2) 配置认证域
\# 创建并进入名称为 dm1 的 ISP 域。
[SwitchA] domain dm1
配置 域的 方法。
\# ISP AAA
[SwitchA-isp-dm1] authentication portal radius-scheme rs1

[SwitchA-isp-dm1] authorization portal radius-scheme rs1 [SwitchA-isp-dm1] accounting portal radius-scheme rs1 [SwitchA-isp-dm1] quit \# 配置系统缺省的 ISP 域 dm1，所有接入用户共用此缺省域的认证和计费方法。若用户登录时输入的用户名未携带 域名，则使用缺省域下的认证方法。
ISP [SwitchA] domain default enable dm1
(3) 配置 Portal 认证\# 配置 Portal 认证服务器：名称为 newpt，IP 地址为 192.168.0.111，密钥为明文 portal，监听 报文的端口为 50100。
Portal [SwitchA] portal server newpt [SwitchA-portal-server-newpt] ip 192.168.0.111 key simple portal [SwitchA-portal-server-newpt] port 50100 [SwitchA-portal-server-newpt] quit \# 配置 Portal Web 服务器的 URL 为 http://192.168.0.111:8080/portal。（Portal Web 服务器的 URL 请与实际环境中的 Portal Web 服务器配置保持一致，此处仅为示例）
[SwitchA] portal web-server newpt [SwitchA-portal-websvr-newpt] url http://192.168.0.111:8080/portal [SwitchA-portal-websvr-newpt] quit \# 在接口 Vlan-interface4 上开启可跨三层方式的 Portal 认证。
[SwitchA] interface vlan-interface 4 [SwitchA–Vlan-interface4] portal enable method layer3在接口 上引用 服务器 newpt。
\# Vlan-interface4 Portal Web [SwitchA–Vlan-interface4] portal apply web-server newpt \# 在接口 Vlan-interface4 上设置发送给 Portal 报文中的 BAS-IP 属性值为 20.20.20.1。
[SwitchA–Vlan-interface4] portal bas-ip 20.20.20.1 [SwitchA–Vlan-interface4] quit

###### 4. 验证配置

\# 以上配置完成后，通过执行以下显示命令可查看 Portal 配置是否生效。
[SwitchA] display portal interface vlan-interface 4 Portal information of Vlan-interface4 NAS-ID profile: Not configured Authorization : Strict checking ACL : Disabled User profile : Disabled IPv4:
Portal status: Enabled Portal authentication method: Layer3 Portal web server: newpt Portal mac-trigger-server: Not configured Authentication domain: Not configured Pre-auth domain: Not configured User-dhcp-only: Disabled Pre-auth IP pool: Not configured Max Portal users: Not configured Bas-ip: 20.20.20.1

User detection: Not configured Action for server detection:
Server type Server name Action
-- -- -- Layer3 source network:
IP address Mask Destination authenticate subnet:
IP address Mask IPv6:
Portal status: Disabled Portal authentication method: Disabled Portal web server: Not configured Portal mac-trigger-server: Not configured Authentication domain: Not configured Pre-auth domain: Not configured User-dhcp-only: Disabled Pre-auth IP pool: Not configured Max Portal users: Not configured Bas-ipv6: Not configured User detection: Not configured Action for server detection:
Server type Server name Action
-- -- -- Layer3 source network:
IP address Prefix length Destination authenticate subnet:
IP address Prefix length用户既可以使用 H3C 的 iNode 客户端，也可以通过网页方式进行 Portal 认证。用户在通过认证前，只能访问认证页面 http://192.168.0.111:8080/portal，且发起的 Web 访问均被重定向到该认证页面，在通过认证后，可访问非受限的互联网资源。
\# Portal 用户认证通过后，可通过执行以下显示命令查看 Switch A 上生成的 Portal 在线用户信息。
[SwitchA] display portal user interface vlan-interface 4 Total portal users: 1 Username: abc Portal server: newpt State: Online VPN instance: N/A MAC IP VLAN Interface 0015-e9a6-7cfe 8.8.8.2 4 Vlan-interface4 Authorization information:
DHCP IP pool: N/A User profile: N/A Session group profile: N/A ACL: N/A Inbound CAR: N/A Outbound CAR: N/A

###### 1. 组网需求

##### 1.21.4 Portal直接认证扩展功能配置举例

组网需求
1.
• 用户主机与接入设备 Switch 直接相连，采用直接方式的 Portal 认证。用户通过手工配置或获取的一个公网 地址进行认证，在通过身份认证而没有通过安全认证时可以访问DHCP IP
192.168.0.0/24 网段；在通过安全认证后，可以访问非受限互联网资源。
• 采用一台 Portal 服务器承担 Portal 认证服务器和 Portal Web 服务器的职责。
采用 服务器作为认证/计费服务器。
• RADIUS

###### 2. 组网图

图1-19 配置 Portal 直接认证扩展功能组网图

###### 3. 配置步骤

按照组网图配置设备各接口的 IP 地址，保证启动 Portal 之前各主机、服务器和设备之间的路由
•可达。
• 完成 RADIUS 服务器上的配置，保证用户的认证/计费功能正常运行。
(1) 配置 RADIUS 方案\# 创建名称为 rs1 的 RADIUS 方案并进入该方案视图。
<Switch> system-view [Switch] radius scheme rs1配置 方案的主认证和主计费服务器及其通信密钥。
\# RADIUS [Switch-radius-rs1] primary authentication 192.168.0.112 [Switch-radius-rs1] primary accounting 192.168.0.112 [Switch-radius-rs1] key accounting simple radius [Switch-radius-rs1] key authentication simple radius [Switch-radius-rs1] user-name-format without-domain [Switch-radius-rs1] quit \# 开启 RADIUS session control 功能。

[Switch] radius session-control enable \# 指定一个 session control 客户端 IP 地址为 192.168.0.113，共享密钥为明文 12345。
[Switch] radius session-control client ip 192.168.0.113 key simple 12345配置认证域
(2)
创建并进入名称为 的 域。
\# dm1 ISP [Switch] domain dm1 \# 配置 ISP 域的 AAA 方法。
[Switch-isp-dm1] authentication portal radius-scheme rs1 [Switch-isp-dm1] authorization portal radius-scheme rs1 [Switch-isp-dm1] accounting portal radius-scheme rs1 [Switch-isp-dm1] quit \# 配置系统缺省的 ISP 域 dm1，所有接入用户共用此缺省域的认证和计费方法。若用户登录时输入的用户名未携带 ISP 域名，则使用缺省域下的认证方法。
[Switch] domain default enable dm1
(3) 配置隔离 ACL 为 3000，安全 ACL 为 3001安全策略服务器上需要将 和 分别指定为隔离 和安全 ACL。
ACL 3000 ACL 3001 ACL [Switch] acl advanced 3000 [Switch-acl-ipv4-adv-3000] rule permit ip destination 192.168.0.0 0.0.0.255 [Switch-acl-ipv4-adv-3000] rule deny ip [Switch-acl-ipv4-adv-3000] quit [Switch] acl advanced 3001 [Switch-acl-ipv4-adv-3001] rule permit ip [Switch-acl-ipv4-adv-3001] quit
(4) 配置 Portal 认证\# 配置 Portal 认证服务器：名称为 newpt，IP 地址为 192.168.0.111，密钥为明文 portal，监听 Portal 报文的端口为 50100。
[Switch] portal server newpt [Switch-portal-server-newpt] ip 192.168.0.111 key simple portal [Switch-portal-server-newpt] port 50100 [Switch-portal-server-newpt] quit \# 配置 Portal Web 服务器的 URL 为 http://192.168.0.111:8080/portal。（Portal Web 服务器的 URL 请与实际环境中的 Portal Web 服务器配置保持一致，此处仅为示例）
[Switch] portal web-server newpt [Switch-portal-websvr-newpt] url http://192.168.0.111:8080/portal [Switch-portal-websvr-newpt] quit \# 在接口 Vlan-interface100 上开启直接方式的 Portal 认证。
[Switch] interface vlan-interface 100 [Switch–Vlan-interface100] portal enable method direct \# 在接口 Vlan-interface100 上引用 Portal Web 服务器 newpt。
[Switch–Vlan-interface100] portal apply web-server newpt \# 在接口 Vlan-interface100 上设置发送给 Portal 报文中的 BAS-IP 属性值为 2.2.2.1。

[Switch–Vlan-interface100] portal bas-ip 2.2.2.1 [Switch–Vlan-interface100] quit

###### 4. 验证配置

\# 以上配置完成后，通过执行以下显示命令可查看 Portal 配置是否生效。
[Switch] display portal interface vlan-interface 100 Portal information of Vlan-interface100 NAS-ID profile: Not configured Authorization : Strict checking ACL : Disabled User profile : Disabled IPv4:
Portal status: Enabled Portal authentication method: Direct Portal web server: newpt Portal mac-trigger-server: Not configured Authentication domain: Not configured Pre-auth domain: Not configured User-dhcp-only: Disabled Pre-auth IP pool: Not configured Max Portal users: Not configured Bas-ip: 2.2.2.1 User detection: Not configured Action for server detection:
Server type Server name Action
-- -- -- Layer3 source network:
IP address Mask Destination authenticate subnet:
IP address Mask IPv6:
Portal status: Disabled Portal authentication method: Disabled Portal web server: Not configured Portal mac-trigger-server: Not configured Authentication domain: Not configured Pre-auth domain: Not configured User-dhcp-only: Disabled Pre-auth IP pool: Not configured Max Portal users: Not configured Bas-ipv6: Not configured User detection: Not configured Action for server detection:
Server type Server name Action
-- -- -- Layer3 source network:
IP address Prefix length

Destination authenticate subnet:
IP address Prefix length使用 H3C iNode 客户端的用户在通过认证前，只能访问认证页面 http://192.168.0.111:8080/portal，且发起的 Web 访问均被重定向到该认证页面。通过身份认证但未通过安全认证时，只能访问匹配ACL 3000 的网络资源；通过身份认证以及安全认证后，可以访问匹配 ACL 3001 的互联网资源。
\# Portal 用户认证通过后，可通过执行以下显示命令查看 Switch 上生成的 Portal 在线用户信息。
[Switch] display portal user interface vlan-interface 100 Total portal users: 1 Username: abc Portal server: newpt State: Online VPN instance: N/A MAC IP VLAN Interface 0015-e9a6-7cfe 2.2.2.2 100 Vlan-interface100 Authorization information:
DHCP IP pool: N/A User profile: N/A Session group profile: N/A ACL: 3001 Inbound CAR: N/A Outbound CAR: N/A

##### 1.21.5 Portal二次地址分配认证扩展功能配置举例

###### 1. 组网需求

用户主机与接入设备 Switch 直接相连，采用二次地址分配方式的 Portal 认证。用户通过 DHCP
•服务器获取 地址，Portal 认证前使用分配的一个私网地址；通过 认证后，用户申请IP Portal到一个公网地址。
• 用户在通过身份认证而没有通过安全认证时可以访问 192.168.0.0/24 网段；用户通过安全认证后，可以访问非受限互联网资源。
• 采用一台 Portal 服务器承担 Portal 认证服务器和 Portal Web 服务器的职责。
• 采用 RADIUS 服务器作为认证/计费服务器。

###### 3. 配置步骤

###### 2. 组网图

图1-20 配置 Portal 二次地址分配认证扩展功能组网图配置步骤
3.
• Portal 二次地址分配认证方式应用中，DHCP 服务器上需创建公网地址池（20.20.20.0/24）及私网地址池（10.0.0.0/24），具体配置略。
Portal 二次地址分配认证方式应用中，接入设备需要配置 DHCP 中继来配合 Portal 认证，且启
•动 的接口需要配置主 地址（公网 IP）及从 地址（私网 IP）。关于 中继的详Portal IP IP DHCP细配置请参见“三层技术-IP 业务配置指导”中的“DHCP 中继”。
• 请保证在 Portal 认证服务器上添加的 Portal 设备的 IP 地址为与用户相连的接口的公网 IP 地址（20.20.20.1），且与该 Portal 设备关联的 IP 地址组中的转换前地址为用户所在的私网网段（10.0.0.0/24）、转换后地址为公网网段（20.20.20.0/24）。
按照组网图配置设备各接口的 IP 地址，保证启动 Portal 之前各主机、服务器和设备之间的路由
•可达。
完成 服务器上的配置，保证用户的认证/计费功能正常运行。
• RADIUS
(1) 配置 RADIUS 方案\# 创建名称为 rs1 的 RADIUS 方案并进入该方案视图。
<Switch> system-view [Switch] radius scheme rs1 \# 配置 RADIUS 方案的主认证和主计费服务器及其通信密钥。
[Switch-radius-rs1] primary authentication 192.168.0.113 [Switch-radius-rs1] primary accounting 192.168.0.113 [Switch-radius-rs1] key accounting simple radius [Switch-radius-rs1] key authentication simple radius [Switch-radius-rs1] user-name-format without-domain

[Switch-radius-rs1] quit \# 开启 RADIUS session control 功能。
[Switch] radius session-control enable指定一个 客户端 地址为 192.168.0.113，共享密钥为明文 12345。
\# session control IP [Switch] radius session-control client ip 192.168.0.113 key simple 12345
(2) 配置认证域\# 创建并进入名称为 dm1 的 ISP 域。
[Switch] domain dm1 \# 配置 ISP 域的 AAA 方法。
[Switch-isp-dm1] authentication portal radius-scheme rs1 [Switch-isp-dm1] authorization portal radius-scheme rs1 [Switch-isp-dm1] accounting portal radius-scheme rs1 [Switch-isp-dm1] quit配置系统缺省的 域 dm1，所有接入用户共用此缺省域的认证和计费方法。若用户登录\# ISP时输入的用户名未携带 ISP 域名，则使用缺省域下的认证方法。
[Switch] domain default enable dm1
(3) 配置隔离 ACL 为 3000，安全 ACL 为 3001安全策略服务器上需要将 ACL 3000 和 ACL 3001 分别指定为隔离 ACL 和安全 ACL。
[Switch] acl advanced 3000 [Switch-acl-ipv4-adv-3000] rule permit ip destination 192.168.0.0 0.0.0.255 [Switch-acl-ipv4-adv-3000] rule deny ip [Switch-acl-ipv4-adv-3000] quit [Switch] acl advanced 3001 [Switch-acl-ipv4-adv-3001] rule permit ip [Switch-acl-ipv4-adv-3001] quit配置 中继和授权
(4) DHCP ARP \# 配置 DHCP 中继。
[Switch] dhcp enable [Switch] dhcp relay client-information record [Switch] interface vlan-interface 100 [Switch–Vlan-interface100] ip address 20.20.20.1 255.255.255.0 [Switch–Vlan-interface100] ip address 10.0.0.1 255.255.255.0 sub [Switch-Vlan-interface100] dhcp select relay [Switch-Vlan-interface100] dhcp relay server-address 192.168.0.112 \# 开启授权 ARP 功能。
[Switch-Vlan-interface100] arp authorized enable [Switch-Vlan-interface100] quit
(5) 配置 Portal 认证\# 配置 Portal 认证服务器：名称为 newpt，IP 地址为 192.168.0.111，密钥为明文 portal，监听 报文的端口为 50100。
Portal [Switch] portal server newpt

###### 4. 验证配置

[Switch-portal-server-newpt] ip 192.168.0.111 key simple portal [Switch-portal-server-newpt] port 50100 [Switch-portal-server-newpt] quit \# 配置 Portal Web 服务器的 URL 为 http://192.168.0.111:8080/portal。（Portal Web 服务器的 请与实际环境中的 服务器配置保持一致，此处仅为示例）
URL Portal Web [Switch] portal web-server newpt [Switch-portal-websvr-newpt] url http://192.168.0.111:8080/portal [Switch-portal-websvr-newpt] quit在接口 上开启二次地址方式的 认证。
\# Vlan-interface100 Portal [Switch] interface vlan-interface 100 [Switch–Vlan-interface100] portal enable method redhcp \# 在接口 Vlan-interface100 上引用 Portal Web 服务器 newpt。
[Switch–Vlan-interface100] portal apply web-server newpt在接口 上设置发送给 报文中的 属性值为 20.20.20.1。
\# Vlan-interface100 Portal BAS-IP [Switch–Vlan-interface100] portal bas-ip 20.20.20.1 [Switch–Vlan-interface100] quit验证配置
4.
\# 以上配置完成后，通过执行以下显示命令可查看 Portal 配置是否生效。
[Switch] display portal interface vlan-interface 100 Portal information of Vlan-interface100 NAS-ID profile: Not configured Authorization : Strict checking ACL : Disabled User profile : Disabled IPv4:
Portal status: Enabled Portal authentication method: Redhcp Portal web server: newpt Portal mac-trigger-server: Not configured Authentication domain: Not configured Pre-auth domain: Not configured User-dhcp-only: Disabled Pre-auth IP pool: Not configured Max Portal users: Not configured Bas-ip: 20.20.20.1 User detection: Not configured Action for server detection:
Server type Server name Action
-- -- -- Layer3 source network:
IP address Mask Destination authenticate subnet:
IP address Mask IPv6:
Portal status: Disabled

Portal authentication method: Disabled Portal web server: Not configured Portal mac-trigger-server: Not configured Authentication domain: Not configured Pre-auth domain: Not configured User-dhcp-only: Disabled Pre-auth IP pool: Not configured Max Portal users: Not configured Bas-ipv6: Not configured User detection: Not configured Action for server detection:
Server type Server name Action
-- -- -- Layer3 source network:
IP address Prefix length Destination authenticate subnet:
IP address Prefix length使用 H3C iNode 客户端的用户在通过认证前，只能访问认证页面 http://192.168.0.111:8080/portal，且发起的 访问均被重定向到该认证页面。通过身份认证但未通过安全认证时，只能访问匹配Web ACL 3000 的网络资源；通过身份认证以及安全认证后，可以访问匹配 ACL 3001 的互联网资源。
\# Portal 用户认证通过后，可通过执行以下显示命令查看 Switch 上生成的 Portal 在线用户信息。
[Switch] display portal user interface vlan-interface 100 Total portal users: 1 Username: abc Portal server: newpt State: Online VPN instance: N/A MAC IP VLAN Interface 0015-e9a6-7cfe 20.20.20.2 100 Vlan-interface100 Authorization information:
DHCP IP pool: N/A User profile: N/A Session group profile: N/A ACL: 3001 Inbound CAR: N/A Outbound CAR: N/A

##### 1.21.6 可跨三层Portal认证方式扩展功能配置举例

###### 1. 组网需求

Switch A 支持 Portal 认证功能。用户 Host 通过 Switch B 接入到 Switch A。
• 配置 Switch A 采用可跨三层 Portal 认证。用户在通过身份认证而没有通过安全认证时可以访问 192.168.0.0/24 网段；在通过安全认证后，可以访问非受限互联网资源。
• 采用一台 Portal 服务器承担 Portal 认证服务器和 Portal Web 服务器的职责。
• 采用 RADIUS 服务器作为认证/计费服务器。

###### 2. 组网图

图1-21 配置可跨三层 Portal 认证扩展功能组网图

###### 3. 配置步骤

请保证在 认证服务器上添加的 设备的 地址为与用户相连的接口 地址
• Portal Portal IP IP（20.20.20.1），且与该 Portal 设备关联的 IP 地址组为用户所在网段（8.8.8.0/24）。
• 按照组网图配置设备各接口的 IP 地址，保证启动 Portal 之前各主机、服务器和设备之间的路由可达。
• 完成 RADIUS 服务器上的配置，保证用户的认证/计费功能正常运行。
配置 方案
(1) RADIUS创建名称为 的 方案并进入该方案视图。
\# rs1 RADIUS <SwitchA> system-view [SwitchA] radius scheme rs1 \# 配置 RADIUS 方案的主认证和主计费服务器及其通信密钥。
[SwitchA-radius-rs1] primary authentication 192.168.0.112 [SwitchA-radius-rs1] primary accounting 192.168.0.112 [SwitchA-radius-rs1] key accounting simple radius [SwitchA-radius-rs1] key authentication simple radius [SwitchA-radius-rs1] user-name-format without-domain [SwitchA-radius-rs1] quit \# 开启 RADIUS session control 功能。
[SwitchA] radius session-control enable \# 指定一个 session control 客户端 IP 地址为 192.168.0.113，共享密钥为明文 12345。
[SwitchA] radius session-control client ip 192.168.0.113 key simple 12345
(2) 配置认证域\# 创建并进入名称为 dm1 的 ISP 域。
[SwitchA] domain dm1

\# 配置 ISP 域的 AAA 方法。
[SwitchA-isp-dm1] authentication portal radius-scheme rs1 [SwitchA-isp-dm1] authorization portal radius-scheme rs1 [SwitchA-isp-dm1] accounting portal radius-scheme rs1 [SwitchA-isp-dm1] quit \# 配置系统缺省的 ISP 域 dm1，所有接入用户共用此缺省域的认证和计费方法。若用户登录时输入的用户名未携带 ISP 域名，则使用缺省域下的认证方法。
[SwitchA] domain default enable dm1
(3) 配置隔离 ACL 为 3000，安全 ACL 为 3001安全策略服务器上需要将 ACL 3000 和 ACL 3001 分别指定为隔离 ACL 和安全 ACL。
[SwitchA] acl advanced 3000 [SwitchA-acl-ipv4-adv-3000] rule permit ip destination 192.168.0.0 0.0.0.255 [SwitchA-acl-ipv4-adv-3000] rule deny ip [SwitchA-acl-ipv4-adv-3000] quit [SwitchA] acl advanced 3001 [SwitchA-acl-ipv4-adv-3001] rule permit ip [SwitchA-acl-ipv4-adv-3001] quit
(4) 配置 Portal 认证\# 配置 Portal 认证服务器：名称为 newpt，IP 地址为 192.168.0.111，密钥为明文 portal，监听 Portal 报文的端口为 50100。
[SwitchA] portal server newpt [SwitchA-portal-server-newpt] ip 192.168.0.111 key simple portal [SwitchA-portal-server-newpt] port 50100 [SwitchA-portal-server-newpt] quit \# 配置 Portal Web 服务器的 URL 为 http://192.168.0.111:8080/portal。（Portal Web 服务器的 URL 请与实际环境中的 Portal Web 服务器配置保持一致，此处仅为示例）
[SwitchA] portal web-server newpt [SwitchA-portal-websvr-newpt] url http://192.168.0.111:8080/portal [SwitchA-portal-websvr-newpt] quit \# 在接口 Vlan-interface4 上开启可跨三层方式的 Portal 认证。
[SwitchA] interface vlan-interface 4 [SwitchA–Vlan-interface4] portal enable method layer3 \# 在接口 Vlan-interface4 上引用 Portal Web 服务器 newpt。
[SwitchA–Vlan-interface4] portal apply web-server newpt \# 在接口 Vlan-interface4 上设置发送给 Portal 报文中的 BAS-IP 属性值为 20.20.20.1。
[SwitchA–Vlan-interface4] portal bas-ip 20.20.20.1 [SwitchA–Vlan-interface4] quit

###### 4. 验证配置

以上配置完成后，通过执行以下显示命令可查看 配置是否生效。
\# Portal [SwitchA] display portal interface vlan-interface 4

Portal information of Vlan-interface4 NAS-ID profile: Not configured Authorization : Strict checking ACL : Disabled User profile : Disabled IPv4:
Portal status: Enabled Portal authentication method: Layer3 Portal web server: newpt Portal mac-trigger-server: Not configured Authentication domain: Not configured Pre-auth domain: Not configured User-dhcp-only: Disabled Pre-auth IP pool: Not configured Max Portal users: Not configured Bas-ip: 20.20.20.1 User detection: Not configured Action for server detection:
Server type Server name Action
-- -- -- Layer3 source network:
IP address Mask Destination authenticate subnet:
IP address Mask IPv6:
Portal status: Disabled Portal authentication method: Disabled Portal web server: Not configured Portal mac-trigger-server: Not configured Authentication domain: Not configured Pre-auth domain: Not configured User-dhcp-only: Disabled Pre-auth IP pool: Not configured Max Portal users: Not configured Bas-ipv6: Not configured User detection: Not configured Action for server detection:
Server type Server name Action
-- -- -- Layer3 source network:
IP address Prefix length Destination authenticate subnet:
IP address Prefix length使用 H3C iNode 客户端的用户在通过认证前，只能访问认证页面 http://192.168.0.111:8080/portal，且发起的 访问均被重定向到该认证页面。通过身份认证但未通过安全认证时，只能访问匹配Web ACL 3000 的网络资源；通过身份认证以及安全认证后，可以访问匹配 ACL 3001 的互联网资源。

\# Portal 用户认证通过后，可通过执行以下显示命令查看 Switch A 上生成的 Portal 在线用户信息。
[SwitchA] display portal user interface vlan-interface 4 Total portal users: 1 Username: abc Portal server: newpt State: Online VPN instance: N/A MAC IP VLAN Interface 0015-e9a6-7cfe 8.8.8.2 4 Vlan-interface4 Authorization information:
DHCP IP pool: N/A User profile: N/A Session group profile: N/A ACL: 3001 Inbound CAR: N/A Outbound CAR: N/A

##### 1.21.7 Portal认证服务器探测和用户信息同步功能配置举例

###### 1. 组网需求

用户主机与接入设备 直接相连，通过 认证接入网络，并采用一台 服务器承担Switch Portal Portal Portal 认证服务器和 Portal Web 服务器的职责，采用 RADIUS 服务器作为认证/计费服务器。
具体要求如下：
用户通过手工配置或 获取的一个公网 地址进行认证，在通过 认证前，只能访
• DHCP IP Portal问 Portal 认证服务器；在通过 Portal 认证后，可以使用此 IP 地址访问非受限的互联网资源。
• 接入设备能够探测到 Portal 认证服务器是否可达，并输出可达状态变化的日志信息，在服务器不可达时（例如，网络连接中断、网络设备故障或服务器无法正常提供服务等情况），取消认证，使得用户仍然可以正常访问网络。
Portal接入设备能够与服务器定期进行用户信息的同步。
•

###### 2. 组网图

图1-22 认证服务器探测和用户同步信息功能配置组网图Portal

###### 3. 配置步骤

• 按照组网图配置设备各接口的 IP 地址，保证启动 Portal 之前各主机、服务器和设备之间的路由
可达。
• 完成 RADIUS 服务器上的配置，保证用户的认证/计费功能正常运行。
(1) 配置 Portal 认证服务器（iMC PLAT 3.20）
下面以 为例（使用 版本为：iMC 3.20-R2606P13、iMC 3.60-E6301），
iMC iMC PLAT UAM
说明 Portal server 的相关配置。
\# 配置 Portal 认证服务器。
登录进入 iMC 管理平台，选择“业务”页签，单击导航树中的[Portal 认证服务器管理/服务器
配置]菜单项，进入服务器配置页面。
配置逃生心跳间隔时长及用户心跳间隔时长。
(cid:123)
其它参数使用缺省配置。
(cid:123)
图1-23 Portal 认证服务器配置页面
配置 地址组。
\# IP
单击导航树中的[Portal 认证服务器管理/IP 地址组配置]菜单项，进入 地址组配置页
Portal IP
面，在该页面中单击<增加>按钮，进入增加 IP 地址组配置页面。
填写 IP 地址组名。
(cid:123)
输入起始地址和终止地址。用户主机 地址必须包含在该 地址组范围内。
IP IP
(cid:123)
选择业务分组，本例中使用缺省的“未分组”。
(cid:123)
选择 地址组的类型为“普通”。
IP
(cid:123)

图1-24 增加 IP 地址组配置页面\# 增加 Portal 设备。
单击导航树中的[Portal 认证服务器管理/设备配置]菜单项，进入 Portal 设备配置页面，在该页面中单击<增加>按钮，进入增加设备信息配置页面。
填写设备名。
(cid:123)
指定 IP 地址为与接入用户相连的设备接口 IP。
(cid:123)
输入密钥，与接入设备 Switch 上的配置保持一致。
(cid:123)
选择是否进行二次地址分配，本例中为直接认证，因此为否。
(cid:123)
选择支持逃生心跳功能和用户心跳功能。
(cid:123)
图1-25 增加设备信息配置页面\# Portal 设备关联 IP 地址组。
在 Portal 设备配置页面中的设备信息列表中，点击 NAS 设备的<端口组信息管理>链接，进入端口组信息配置页面。

图1-26 设备信息列表在端口组信息配置页面中点击<增加>按钮，进入增加端口组信息配置页面。
填写端口组名。
(cid:123)
选择 IP 地址组，用户接入网络时使用的 IP 地址必须属于所选的 IP 地址组。
(cid:123)
其它参数采用缺省值。
(cid:123)
图1-27 增加端口组信息配置页面\# 最后单击导航树中的[业务参数配置/系统配置手工生效]菜单项，使以上 Portal 认证服务器配置生效。
配置 认证服务器（iMC 5.0）
(2) Portal PLAT下面以 为例（使用 版本为：iMC 5.0(E0101)、iMC 5.0(E0101)），说明iMC iMC PLAT UAM Portal server 的基本配置。
\# 配置 Portal 认证服务器。
登录进入 iMC 管理平台，选择“业务”页签，单击导航树中的[Portal 认证服务器管理/服务器配置 菜单项，进入服务器配置页面。
]配置逃生心跳间隔时长及用户心跳间隔时长。
(cid:123)
其它参数使用缺省配置。
(cid:123)

图1-28 Portal 认证服务器配置页面\# 配置 IP 地址组。
单击导航树中的[Portal 认证服务器管理/IP 地址组配置]菜单项，进入 Portal IP 地址组配置页面，在该页面中单击<增加>按钮，进入增加 IP 地址组配置页面。
填写 IP 地址组名。
(cid:123)
输入起始地址和终止地址。用户主机 IP 地址必须包含在该 IP 地址组范围内。
(cid:123)
选择业务分组，本例中使用缺省的“未分组”。
(cid:123)
选择 IP 地址组的类型为“普通”。
(cid:123)
图1-29 增加 IP 地址组配置页面\# 增加 Portal 设备。
单击导航树中的[Portal 认证服务器管理/设备配置]菜单项，进入 Portal 设备配置页面，在该页面中单击<增加>按钮，进入增加设备信息配置页面。
填写设备名。
(cid:123)

指定 IP 地址为与接入用户相连的设备接口 IP。
(cid:123)
输入密钥，与接入设备 Switch 上的配置保持一致。
(cid:123)
选择是否进行二次地址分配，本例中为直接认证，因此为否。
(cid:123)
选择支持逃生心跳功能和用户心跳功能。
(cid:123)
图1-30 增加设备信息配置页面\# Portal 设备关联 IP 地址组。
在 Portal 设备配置页面中的设备信息列表中，点击 NAS 设备的<端口组信息管理>链接，进入端口组信息配置页面。
图1-31 设备信息列表在端口组信息配置页面中点击<增加>按钮，进入增加端口组信息配置页面。
填写端口组名。
(cid:123)
选择 地址组，用户接入网络时使用的 地址必须属于所选的 地址组。
IP IP IP (cid:123)
其它参数采用缺省值。
(cid:123)

图1-32 增加端口组信息配置页面\# 最后单击导航树中的[业务参数配置/系统配置手工生效]菜单项，使以上 Portal 认证服务器配置生效。
(3) 配置 Switch配置 RADIUS 方案(cid:123)
\# 创建名称为 rs1 的 RADIUS 方案并进入该方案视图。
<Switch> system-view [Switch] radius scheme rs1 \# 配置 RADIUS 方案的主认证和主计费服务器及其通信密钥。
[Switch-radius-rs1] primary authentication 192.168.0.112 [Switch-radius-rs1] primary accounting 192.168.0.112 [Switch-radius-rs1] key authentication simple radius [Switch-radius-rs1] key accounting simple radius \# 配置发送给 RADIUS 服务器的用户名不携带 ISP 域名。
[Switch-radius-rs1] user-name-format without-domain [Switch-radius-rs1] quit \# 开启 RADIUS session control 功能。
[Switch] radius session-control enable配置认证域(cid:123)
\# 创建并进入名称为 dm1 的 ISP 域。
[Switch] domain dm1 \# 配置 ISP 域的 AAA 方法。
[Switch-isp-dm1] authentication portal radius-scheme rs1 [Switch-isp-dm1] authorization portal radius-scheme rs1 [Switch-isp-dm1] accounting portal radius-scheme rs1 [Switch-isp-dm1] quit

\# 配置系统缺省的 ISP 域 dm1，所有接入用户共用此缺省域的认证和计费方法。若用户登录时输入的用户名未携带 域名，则使用缺省域下的认证方法。
ISP [Switch] domain default enable dm1配置 Portal 认证(cid:123)
\# 配置 Portal 认证服务器：名称为 newpt，IP 地址为 192.168.0.111，密钥为明文 portal，监听 报文的端口为 50100。
Portal [Switch] portal server newpt [Switch-portal-server-newpt] ip 192.168.0.111 key simple portal [Switch-portal-server-newpt] port 50100配置对 认证服务器 的探测功能：每次探测间隔时间为 秒，若服务器可达\# Portal newpt 40状态改变，则发送日志信息。
[Switch-portal-server-newpt] server-detect timeout 40 log此处 timeout 取值应该大于等于 Portal 认证服务器的逃生心跳间隔时长。
\# 配置对 Portal 认证服务器 newpt 的 Portal 用户信息同步功能，检测用户同步报文的时间间隔为 600 秒，如果设备中的某用户信息在 600 秒内未在该 Portal 认证服务器发送的同步报文中出现，设备将强制该用户下线。
[Switch-portal-server-newpt] user-sync timeout 600 [Switch-portal-server-newpt] quit此处 取值应该大于等于 认证服务器上的用户心跳间隔时长。
timeout Portal \# 配置 Portal Web 服务器的 URL 为 http://192.168.0.111:8080/portal。（Portal Web 服务器的 请与实际环境中的 服务器配置保持一致，此处仅为示例）
URL Portal Web [Switch] portal web-server newpt [Switch-portal-websvr-newpt] url http://192.168.0.111:8080/portal [Switch-portal-websvr-newpt] quit \# 在接口 Vlan-interface100 上开启直接方式的 Portal 认证。
[Switch] interface vlan-interface 100 [Switch–Vlan-interface100] portal enable method direct开启 认证服务器 不可达时的 用户逃生功能。
\# Portal newpt Portal [Switch–Vlan-interface100] portal fail-permit server newpt \# 在接口 Vlan-interface100 上引用 Portal Web 服务器 newpt。
[Switch–Vlan-interface100] portal apply web-server newpt \# 在接口 Vlan-interface100 上设置发送给 Portal 报文中的 BAS-IP 属性值为 2.2.2.1。
[Switch–Vlan-interface100] portal bas-ip 2.2.2.1 [Switch–Vlan-interface100] quit

###### 4. 验证配置

\# 以上配置完成后，可以通过执行以下命令查看到 Portal 认证服务器的状态为 Up，说明当前 Portal认证服务器可达。
[Switch] display portal server newpt Portal server: newpt Type : IMC IP : 192.168.0.111 VPN instance : Not configured Port : 50100 Server Detection : Timeout 40s Action: log User synchronization : Timeout 600s Status : Up之后，若接入设备探测到 Portal 认证服务器不可达了，可通过以上显示命令查看到 Portal 认证服务器的状态为 Down，同时，设备会输出表示服务器不可达的日志信息“Portal server newpt turns down from up.”，并取消对该接口接入的用户的 Portal 认证，使得用户可以直接访问外部网络。

##### 1.21.8 使用本地Portal Web服务的直接Portal认证配置举例

###### 1. 组网需求

• 用户主机与接入设备 Switch 直接相连，采用直接方式的 Portal 认证。用户通过手工配置或
DHCP 获取的一个公网 IP 地址进行认证，在通过 Portal 认证前，只能访问 Portal Web 服务器；
在通过 认证后，可以使用此 地址访问非受限互联网资源。
Portal IP
Switch 同时承担 Portal Web 服务器和 Portal 认证服务器的职责。
•
采用 RADIUS 服务器作为认证/计费服务器。
•
配置本地 Portal Web 服务使用 HTTP 协议，且 HTTP 服务侦听的 TCP 端口号为 2331。
•

###### 2. 组网图

图1-33 使用本地 服务的直接 认证组网图Portal Web Portal

###### 3. 配置步骤

按照组网图配置设备各接口的 IP 地址，保证启动 Portal 之前各主机、服务器和设备之间的路由
•可达。
完成 服务器上的配置，保证用户的认证/计费功能正常运行。
• RADIUS按照自定义认证页面文件编辑规范，完成认证页面的编辑。并上传到设备存储介质的根目录下。
•

(1) 配置 RADIUS 方案
\# 创建名称为 rs1 的 RADIUS 方案并进入该方案视图。
<Switch> system-view
[Switch] radius scheme rs1
配置 方案的主认证和主计费服务器及其通信密钥。
\# RADIUS
[Switch-radius-rs1] primary authentication 192.168.0.112
[Switch-radius-rs1] primary accounting 192.168.0.112
[Switch-radius-rs1] key authentication simple radius
[Switch-radius-rs1] key accounting simple radius
\# 配置发送给 RADIUS 服务器的用户名不携带 ISP 域名。
[Switch-radius-rs1] user-name-format without-domain
[Switch-radius-rs1] quit
开启 功能。
\# RADIUS session control
[Switch] radius session-control enable
(2) 配置认证域
\# 创建并进入名称为 dm1 的 ISP 域。
[Switch] domain dm1
\# 配置 ISP 域使用的 RADIUS 方案 rs1。
[Switch-isp-dm1] authentication portal radius-scheme rs1
[Switch-isp-dm1] authorization portal radius-scheme rs1
[Switch-isp-dm1] accounting portal radius-scheme rs1
[Switch-isp-dm1] quit
\# 配置系统缺省的 ISP 域 dm1，所有接入用户共用此缺省域的认证和计费方式。若用户登录
时输入的用户名未携带 域名，则使用缺省域下的认证方案。
ISP
[Switch] domain default enable dm1
(3) 配置 Portal 认证
\# 配置 Portal Web 服务器的 URL 为 http://2.2.2.1:2331/portal（Portal Web 服务器 URL 中的
地址可配置为设备上与客户端路由可达的三层接口 地址或除 以外的
IP IP 127.0.0.1 Loopback
接口的 IP 地址）。
[Switch] portal web-server newpt
[Switch-portal-websvr-newpt] url http://2.2.2.1:2331/portal
[Switch-portal-websvr-newpt] quit
\# 在接口 Vlan-interface100 上开启直接方式的 Portal 认证。
[Switch] interface vlan-interface 100
[Switch–Vlan-interface100] portal enable method direct
\# 在接口 Vlan-interface100 上引用 Portal Web 服务器 newpt。
[Switch–Vlan-interface100] portal apply web-server newpt
[Switch–Vlan-interface100] quit
\# 进入本地 Portal Web 服务视图，并指定使用 HTTP 协议和客户端交互认证信息。
[Switch] portal local-web-server http
\# 配置本地 Portal Web 服务提供的缺省认证页面文件为 abc.zip（设备的存储介质的根目录下
必须已存在该认证页面文件，否则功能不生效）。
[Switch–portal-local-websvr-http] default-logon-page abc.zip
\# 配置本地 Portal Web 服务的 HTTP 服务侦听的 TCP 端口号为 2331。

[Switch–portal-local-webserver-http] tcp-port 2331 [Switch–portal-local-websvr-http] quit

###### 4. 验证配置

\# 以上配置完成后，通过执行以下显示命令可查看 Portal 配置是否生效。
[Switch] display portal interface vlan-interface 100 Portal information of Vlan-interface 100 Authorization Strict checking ACL Disabled User profile Disabled IPv4:
Portal status: Enabled Portal authentication method: Direct Portal web server: newpt Portal mac-trigger-server: Not configured Authentication domain: Not configured Pre-auth domain: Not configured User-dhcp-only: Disabled Pre-auth IP pool: Not configured Max Portal users: Not configured Bas-ip: Not configured User detection: Not configured Action for server detection:
Server type Server name Action
-- -- -- Layer3 source network:
IP address Mask Destination authenticate subnet:
IP address Mask IPv6:
Portal status: Disabled Portal authentication method: Disabled Portal web server: Not configured Portal mac-trigger-server: Not configured Authentication domain: Not configured Pre-auth domain: Not configured User-dhcp-only: Disabled Pre-auth IP pool: Not configured Max Portal users: Not configured Bas-ipv6: Not configured User detection: Not configured Action for server detection:
Server type Server name Action
-- -- -- Layer3 source network:
IP address Prefix length Destination authenticate subnet:

###### 3. 处理过程

###### 1. 故障现象

IP address Prefix length使用本地 Portal Web 服务进行 Portal 认证的组网环境中，只支持通过网页方式进行 Portal 认证。
用户在通过认证前，只能访问认证页面 http://2.2.2.1:2331/portal，且发起的 Web 访问均被重定向到该认证页面，在通过认证后，可访问非受限的互联网资源。
用户认证通过后，可通过执行以下显示命令查看 上生成的 在线用户信息。
\# Portal Switch Portal [Switch] display portal user interface vlan-interface 100 Total portal users： 1 Username: abc Portal server: newpt State: Online VPN instance: -- MAC IP VLAN Interface 0015-e9a6-7cfe 2.2.2.2 100 Vlan-interface100 Authorization information:
IP pool: N/A User profile: N/A Session group profile: N/A ACL: N/A Inbound CAR: N/A Outbound CAR: N/A

#### 1.22 Portal常见故障处理

##### 1.22.1 Portal用户认证时，没有弹出Portal认证页面

故障现象
1.
用户被强制去访问 iMC Portal 认证服务器时没有弹出 Portal 认证页面，也没有错误提示，登录的Portal 认证服务器页面为空白。

###### 2. 故障分析

接入设备上配置的 密钥和 认证服务器上配置的密钥不一致，导致 认证服务器报Portal Portal Portal文验证出错，Portal 认证服务器拒绝弹出认证页面。
处理过程
3.
使用 display portal server 命令查看接入设备上是否配置了 Portal 认证服务器密钥，若没有配置密钥，请补充配置；若配置了密钥，请在 认证服务器视图中使用 ip 或 ipv6 命令修改Portal密钥，或者在 Portal 认证服务器上查看对应接入设备的密钥并修改密钥，直至两者的密钥设置一致。

##### 1.22.2 接入设备上无法强制Portal用户下线

###### 1. 故障现象

用户通过 Portal 认证后，在接入设备上使用 portal delete-user 命令强制用户下线失败，但是使用客户端的“断开”属性可以正常下线。

###### 2. 故障分析

在接入设备上使用 portal delete-user 命令强制用户下线时，由接入设备主动发送下线通知报文到 Portal 认证服务器，Portal 认证服务器会在指定的端口监听该报文（缺省为 50100），但是接入设备发送的下线通知报文的目的端口和 认证服务器真正的监听端口不一致，故 认证Portal Portal服务器无法收到下线通知报文，Portal 认证服务器上的用户无法下线。
当使用客户端的“断开”属性让用户下线时，由 Portal 认证服务器主动向接入设备发送下线请求，其源端口为 50100，接入设备的下线应答报文的目的端口使用请求报文的源端口，避免了其配置上的错误，使得 Portal 认证服务器可以收到下线应答报文，从而 Portal 认证服务器上的用户成功下线。

###### 3. 处理过程

使用 命令查看接入设备对应服务器的端口，并在系统视图中使用display portal server portal server 命令修改服务器的端口，使其和 Portal 认证服务器上的监听端口一致。

##### 1.22.3 RADIUS服务器上无法强制Portal用户下线

###### 1. 故障现象

接入设备使用 H3C 的 iMC 服务器作为 RADIUS 服务器对 Portal 用户进行身份认证，用户通过 Portal认证上线后，管理员无法在 RADIUS 服务器上强制 Portal 用户下线。

###### 2. 故障分析

的 服务器使用 报文向设备发送断开连接请求。接入设备上监听H3C iMC session control session control报文的UDP端口缺省是关闭的，因此无法接收RADIUS服务器发送的Portal用户下线请求。

###### 3. 处理过程

查看接入设备上的 RADIUS session control 功能是否处于开启状态，若未开启，请在系统视图下执行 radius session-control enable 命令开启。

##### 1.22.4 接入设备强制用户下线后，Portal认证服务器上还存在该用户

###### 1. 故障现象

接入设备上通过命令行强制 Portal 用户下线后，Portal 认证服务器上还存在该用户。

###### 2. 故障分析

在接入设备上使用 命令强制用户下线时，由接入设备主动发送下线通知报portal delete-user文到 Portal 认证服务器，若接入设备主动发送的 Portal 报文携带的 BAS-IP/BAS-IPv6 属性值与Portal 认证服务器上指定的设备 IP 地址不一致，Portal 认证服务器会将该下线通知报文丢弃。当接入设备尝试发送该报文超时之后，会将该用户强制下线，但 认证服务器上由于并未成功接收Portal这样的通知报文，认为该用户依然在线。

###### 3. 处理过程

在开启 Portal 认证的接口上配置 BAS-IP/BAS-IPv6 属性值，使其与 Portal 认证服务器上指定的设备 IP 地址保持一致。

###### 1. 故障现象

##### 1.22.5 二次地址分配认证用户无法成功上线

故障现象
1.
设备对用户采用二次地址分配认证方式的 Portal 认证，用户输入正确的用户名和密码，且客户端先后成功获取到了私网 地址和公网的 地址，但认证结果为失败。
IP IP

###### 2. 故障分析

在接入设备对用户进行二次地址分配认证过程中，当接入设备感知到客户端的 IP 地址更新之后，需要主动发送 Portal 通知报文告知 Portal 认证服务器已检测到用户 IP 变化，当 Portal 认证服务器接收到客户端以及接入设备发送的关于用户 IP 变化的通告后，才会通知客户端上线成功。若接入设备主动发送的 报文携带的 属性值与 认证服务器上指定的设备 地址Portal BAS-IP/BAS-IPv6 Portal IP不一致时，Portal 认证服务器会将该 Portal 通知报文丢弃，因此会由于未及时收到用户 IP 变化的通告认为用户认证失败。

###### 3. 处理过程

在开启 Portal 认证的接口上配置 BAS-IP/BAS-IPv6 属性值，使其与 Portal 认证服务器上指定的设备 地址保持一致。
IP

## 05-Web认证配置

目 录认证简介认证配置任务简介配置 认证用户使用的认证域配置 认证最大用户数认证显示和维护使用 服务器远程 认证方式进行 认证配置举例

### 1 Web认证

1 Web认证

#### 1.1 Web认证简介

Web 认证是一种在二层以太网接口上通过网页方式对用户身份合法性进行认证的认证方法。在接入设备的二层以太网接口上开启 Web 认证功能后，未认证用户上网时，接入设备强制用户登录到特定站点，用户可免费访问其中的 资源；当用户需要访问该特定站点之外的 资源时，必须Web Web在接入设备上进行认证，认证通过后可访问特定站点之外的 Web 资源。

##### 1.1.1 Web认证的优势

Web 认证具体有如下优势：
无需安装客户端软件，直接使用 Web 页面认证，使用方便。
•可为运营商提供方便的管理功能和业务拓展功能，例如运营商可以在认证页面上开展商业广
•告、社区服务、信息发布等个性化业务。

##### 1.1.2 Web认证系统

Web认证的典型组网方式如 图 1-1 所示，它由四个基本要素组成：认证客户端、接入设备、本地Portal Web服务器、AAA服务器。
图1-1 Web 认证系统组成示意图

###### 1. 认证客户端

为运行 协议的浏览器，发起 认证。
HTTP Web

###### 2. 接入设备

提供接入服务的设备，主要有三方面的作用：
• 在认证之前，将用户的所有不符合免认证规则的 HTTP 请求都重定向到认证页面。
• 在认证过程中，与 AAA 服务器交互，完成身份认证/授权/计费的功能。有关 AAA 的详细介绍请参见“安全配置指导”中的“AAA”。
• 在认证通过后，允许用户访问被授权的网络资源。

###### 3. 本地Portal Web服务器

本地 Portal Web 服务器集成在接入设备中，负责向认证客户端提供认证页面及其免费 Web 资源，获取认证客户端的用户名、密码等认证信息。

###### 4. AAA服务器

与接入设备进行交互，完成对用户的认证、授权和计费。目前支持的 AAA 服务器包括 RADIUS（Remote Authentication Dial-In User Service，远程认证拨号用户服务）服务器和 LDAP（Lightweight Protocol，轻量级目录访问协议）服务器：
Directory Access可支持对 认证用户进行认证、授权和计费。
• RADIUS Web服务器可支持对 认证用户进行认证。
• LDAP Web

##### 1.1.3 Web认证流程

Web认证的具体认证过程如 图 1-2 所示。
图1-2 认证流程图Web认证用户首次访问 资源的 请求报文经过开启了 认证功能的二层以太网
(1) Web Web HTTP Web接口时，若此 HTTP 报文请求的内容为认证页面或设定的免费访问地址中的 Web 资源，则接入设备允许此 HTTP 报文通过；若请求的内容为其他 Web 资源，则接入设备将此 HTTP 报文重定向到认证页面，用户在认证页面上输入用户名和密码来进行认证。
(2) 接入设备与 AAA 服务器之间进行 RADIUS 协议报文的交互，对用户身份进行验证。
(3) 若 RADIUS 认证成功，则接入设备上向客户端发送登录成功页面，通知客户端认证成功。否则，接入设备上向客户端发送登录失败页面。

##### 1.1.4 Web认证支持VLAN下发

###### 1. 授权VLAN

为了将受限的网络资源与未认证用户隔离，通常将受限的网络资源和未认证的用户划分到不同的VLAN。Web 认证支持远程 AAA 服务器/接入设备下发授权不带 Tag 的 VLAN。当用户通过 Web 认证后，远程 AAA 服务器/接入设备会将授权 VLAN 信息下发给接入设备上用户进行认证的端口，该端口被加入到授权 后，用户便可以访问此 中的网络资源。若该 不存在，则接入VLAN VLAN VLAN设备首先创建 VLAN，而后端口将允许该 VLAN 的用户报文以不携带 tag 的方式通过。
设备根据用户接入的端口链路类型，按如下情况将端口加入到下发的授权 VLAN 中：
若用户从 类型的端口接入，则端口离开当前 并加入第一个通过认证的用户的授
• Access VLAN权 VLAN 中。
• 若用户从 Trunk 类型的端口接入，则设备允许下发的授权 VLAN 通过该端口，并且修改该端口的缺省 VLAN 为第一个通过认证的用户的授权 VLAN。
• 若用户从 Hybrid 类型的端口接入，则设备允许授权下发的授权 VLAN 以不携带 Tag 的方式通过该端口，并且修改该端口的缺省 VLAN 为第一个通过认证的用户的授权 VLAN。需要注意的

是，若该端口上使能了 MAC VLAN 功能，则设备将根据认证服务器/接入设备下发的授权 VLAN动态地创建基于用户 地址的 VLAN，而端口的缺省 并不改变。
MAC VLAN

###### 2. Web认证Auth-Fail VLAN

Web 认证 Auth-Fail VLAN 功能允许用户在认证失败的情况下访问某一特定 VLAN 中的资源，比如病毒补丁服务器，存储客户端软件或杀毒软件的服务器，进行升级客户端或执行其他一些用户升级程序。这个 称为 VLAN。
VLAN Auth-Fail Web 认证支持基于 MAC 地址的 Auth-Fail VLAN，二层以太网接口上配置了 Auth-Fail VLAN 后，此接口将认证失败用户的 MAC 地址与 Auth-Fail VLAN 进行绑定生成相应的 MAC VLAN 表项，认证失败的用户将会被加入 Auth-Fail VLAN 中。加入 Auth-Fail VLAN 中的用户可以访问该 VLAN 中免认证 IP 的资源，但用户的所有访问非免认证 IP 的 HTTP 请求会被重定向到接入设备上的认证页面进行认证，若用户仍然没有通过认证，则将继续处于 内；若认证成功，则该端口Auth-Fail VLAN会离开 Auth-Fail VLAN，之后端口加入 VLAN 情况与认证服务器是否下发授权 VLAN 有关，具体如下：
• 若认证服务器下发了授权 VLAN，则端口加入下发的授权 VLAN 中。
• 若认证服务器未下发授权 VLAN，则端口回到缺省 VLAN 中。

##### 1.1.5 Web认证支持ACL下发

ACL（Access List，访问控制列表）提供了控制用户访问网络资源和限制用户访问权限的Control功能。当用户上线时，如果远程 AAA 服务器上或接入设备的本地用户视图下配置了授权 ACL，则设备会根据远程 AAA 服务器/接入设备下发的授权 ACL 对用户所在端口的数据流进行控制。由于远程 AAA 服务器/接入设备上指定的是授权 ACL 的编号，因此还需要在接入设备上创建该 ACL 并配置对应的 规则。管理员可以通过随时改变远程 服务器/接入设备上授权 的编号或修ACL AAA ACL改接入设备上对应 ACL 的规则来灵活调整认证成功用户的访问权限。
Web 认证可以成功授权的 ACL 类型为基本 ACL（ACL 编号为 2000～2999）和高级 ACL（ACL 编号为 3000～3999）。但当下发的 ACL 不存在、未配置 ACL 规则或 ACL 规则配置了 counting、established、fragment 或 logging 参数时，授权 ACL 不生效。有关 ACL 规则的具体介绍，请参见“ACL 和 QoS 命令参考”中的“ACL”。

#### 1.2 Web认证配置限制和指导

当用户加入授权 或 后，需要自动申请或者手动更新客户端 地址，以保证VLAN Auth-Fail VLAN IP可以与 Auth-Fail VLAN 中的资源互通。
通常情况下，建议用户通过与接入设备直连来进行Web认证。但在某些特殊环境下有如 图 1-3 所示组网，其中Device B作为接入设备，在端口Port B上开启Web认证功能对Host A、Host B、Host C进行Web认证。此时，需要注意如下配置事项：
• 若通过服务器向用户下发授权 VLAN，需保证 Device A 与 Device B 之间的链路类型为 Trunk，且端口 A1、Port 的 与服务器下发的授权 相同。
Port B PVID VLAN ID若不通过服务器向用户下发授权 ，则仅需保证端口 、 的 相同。
• VLAN Port A1 Port B PVID

图1-3 客户端与设备为非直连组网

#### 1.3 Web认证配置任务简介

Web 认证配置任务如下：
(1) 配置Web认证服务器
(2) 配置本地 Portal 服务有关本地 Portal 服务功能的详细配置请参见“安全配置指导”中的“Portal”。
开启Web认证功能
(3)
（可选）配置Web认证用户使用的认证域
(4)
（可选）配置认证成功后页面跳转的时间间隔
(5)
（可选）配置Web认证用户免认证的目的IP地址
(6)
（可选）配置Web认证最大用户数
(7)
(8) （可选）开启Web认证用户在线探测功能
(9) （可选）配置Web认证的Auth-Fail VLAN
(10) （可选）配置Web认证支持Web代理

#### 1.4 Web认证配置准备

设备上的 Web 认证功能支持两种方式的 AAA 认证，在接入设备上进行本地 AAA 认证和通过 AAA服务器进行远程 AAA 认证。
当选用 RADIUS 服务器认证方式进行 Web 认证时，配置 Web 认证之前，需要完成以下任务：
• RADIUS 服务器安装并配置成功，如创建相应的用户名和密码。
• 用户、接入设备和 RADIUS 服务器之间路由可达。
• 在接入设备端进行 RADIUS 客户端的相关设置，保证接入设备和 RADIUS 服务器之间可进行AAA 认证。
当选用本地认证方式进行 Web 认证时，需要先在设备上配置本地用户。
关于 RADIUS 客户端的以及本地用户的具体配置请参见“安全配置指导”中的“AAA”。

##### 2. 配置步骤

#### 1.5 配置Web认证服务器

##### 1. 配置限制和指导

认证使用本地 服务为认证用户提供认证页面，因此需要将接入设备上一个与Web Portal Web Web认证客户端路由可达的三层接口的 IP 地址指定为 Web 认证服务器的 IP 地址。建议使用设备上空闲的 LoopBack 接口的 IP 地址，使用 LoopBack 接口有如下优点：
• 状态稳定，可避免因为接口故障导致用户无法打开认证页面的问题。
• 由于发送到 LoopBack 接口的报文不会被转发到网络中，当请求上线的用户数目较大时，可减轻对系统性能的影响。
配置的 Web 认证服务器的端口号必须与本地 Portal Web 服务中配置的侦听端口号保持一致。

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 创建 Web 认证服务器，并进入 Web 认证服务器视图。
web-auth server server-name
(3) 配置 Web 认证服务器的 IP 地址和端口号。
ip ipv4-address port port-number
(4) 配置 Web 认证服务器的重定向 URL。
url url-string
缺省情况下，Web 认证服务器下不存在重定向 URL。
URL 中的 IP 地址和端口号必须与 Web 认证服务器中的 IP 地址和端口号保持一致。
(5) （可选）配置设备重定向给用户的 URL 中携带的参数信息。
url-parameter parameter-name { original-url | source-address |
source-mac | value expression }
缺省情况下，未配置设备重定向给用户的 URL 中携带的参数信息。

#### 1.6 开启Web认证功能

##### 1. 配置限制和指导

为使 认证功能正常运行，在接入设备的二层以太网接口上开启 认证功能后，请不要再在Web Web此接口上开启端口安全功能和配置端口安全模式。关于端口安全的相关介绍，请参见“安全配置指导”中的“端口安全”。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 开启 Web 认证功能，并指定引用的 Web 认证服务器。
web-auth enable apply server server-name

缺省情况下，Web 认证功能处于关闭状态。

#### 1.7 配置Web认证用户使用的认证域

##### 1. 功能简介

通过在接入设备的二层以太网接口上配置 Web 认证用户使用的认证域，可使得所有从该接口接入的 Web 认证用户都被强制使用指定的认证域来进行认证、授权和计费。管理员可通过该配置对不同接口上的 Web 认证用户使用不同的认证域，从而增加了管理员部署 Web 认证接入策略的灵活性。
从指定二层以太网接口接入的 Web 认证用户将按照如下先后顺序选择认证域：接口上配置的 Web认证用户使用的 域-->用户名中携带的 域-->系统缺省的 域-->设备上为未知域名的用户ISP ISP ISP指定的 ISP 域。如果根据以上原则决定的认证域在设备上不存在，用户将无法认证。关于 ISP 域的相关介绍请参见“安全配置指导”中的“AAA”。

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置 Web 认证用户使用的认证域。
web-auth domain domain-name
缺省情况下，接口上未配置 Web 认证用户使用的认证域。

#### 1.8 配置认证成功后页面跳转的时间间隔

##### 1. 功能简介

在某些应用环境中，例如，Web 认证用户认证成功并加入授权 后，若客户端需要更新 地VLAN IP址，则需要保证认证页面跳转的时间间隔大于用户更新 IP 地址的时间，否则用户会因为 IP 地址还未完成更新而无法打开指定的跳转网站页面。在这种情况下，为了保证 Web 认证功能的正常运行，需要调整认证页面跳转的时间间隔。

##### 2. 配置步骤

进入系统视图。
(1)
system-view创建 认证服务器，并进入 认证服务器视图。
(2) Web Web web-auth server server-name
(3) 配置认证成功后页面跳转的时间间隔。
redirect-wait-time period缺省情况下，Web 认证用户认证成功后认证页面跳转的时间间隔为 5 秒。

##### 3. 配置步骤

#### 1.9 配置Web认证用户免认证的目的IP地址

##### 1. 功能简介

通过配置免认证的目的 地址，可以让用户无需通过 认证即可访问该目的 中的资源。
IP Web IP

##### 2. 配置限制和指导

建议不要将 Web 认证用户免认证目的 IP 和 802.1X 的 Free IP 配置为相同的 IP，否则当取消其中一项配置时，另一项配置也不再生效。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 配置 Web 认证用户免认证的目的 IP 地址。
web-auth free-ip ip-address { mask-length | mask }缺省情况下，不存在 Web 认证用户免认证目的 IP 地址。

#### 1.10 配置Web认证最大用户数

##### 1. 配置限制和指导

若配置的 Web 认证最大用户数小于当前已经在线的 Web 认证用户数，则配置可以执行成功，且在线 Web 认证用户不受影响，但系统不允许新的 Web 认证用户接入。

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置 Web 认证最大用户数。
web-auth max-user max-number
缺省情况下，Web 认证最大用户数为 1024。

#### 1.11 开启Web认证用户在线探测功能

##### 1. 功能简介

开启端口的 Web 认证用户的在线检测功能后，若设备在一个下线检测定时器间隔之内，未收到此端口下某在线用户的报文，则将切断该用户的连接，同时通知 RADIUS 服务器停止对此用户进行计费。

##### 2. 配置限制和指导

配置用户在线检测时间间隔时，需要与 MAC 地址老化时间配成相同时间，否则会导致用户异常下线。

##### 3. 配置步骤

(1) 进入系统视图。

system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 开启 Web 认证用户在线探测功能。
web-auth offline-detect interval interval缺省情况下，Web 认证用户在线探测功能处于关闭状态。

#### 1.12 配置Web认证的Auth-Fail VLAN

##### 1. 配置限制和指导

开启 认证的端口必须配置为 方式，并开启 功能，Auth-Fail 功
• Web Hybrid MAC VLAN VLAN能才生效。
• Auth-Fail VLAN 的网段需设为 Web 认证用户免认证的目的 IP 地址。
• 如果某个 VLAN 被指定为 Super VLAN，则该 VLAN 不能被指定为某个接口的 Auth-Fail VLAN；
同样，如果某个VLAN被指定为某个接口的Auth-Fail VLAN，则该VLAN不能被指定为Super VLAN。
• 禁止删除已被配置为 Web认证 Auth-Fail VLAN的 VLAN。若要删除该 VLAN，需先通过 undo命令取消 认证的 配置。
web-auth auth-fail vlan Web Auth-Fail VLAN

##### 2. 配置步骤

(1) 进入系统视图。
system-view
进入接口视图。
(2)
interface interface-type interface-number
配置 认证的 VLAN。
(3) Web Auth-Fail
web-auth auth-fail vlan authfail-vlan-id
缺省情况下，不存在 认证的 VLAN。
Web Auth-Fail

#### 1.13 配置Web认证支持Web代理

##### 1. 功能简介

设备默认只允许未配置 Web 代理服务器的浏览器发起的 HTTP 请求才能触发 Web 认证。当用户上网使用的浏览器配置了 Web 代理服务器时，用户的 HTTP 请求报文将被丢弃，而不能触发 Web 认证。在这种情况下，网络管理员可以通过在设备上添加 Web 认证代理服务器的 TCP 端口号，来允许配置了 代理服务器的浏览器发起的 请求也可以触发 认证。
Web HTTP Web

##### 2. 配置限制和指导

如果用户浏览器采用 WPAD（Web Proxy Auto-Discovery，Web 代理服务器自动发现）方式自动配置 Web 代理，则需要进行以下操作：
• 由网络管理员在设备上添加 Web 代理服务器端口，并将 WPAD 主机的 IP 地址配置为 Web 认证用户免认证的目的 IP 地址。

##### 3. 配置步骤

由用户在浏览器上将接入设备上 Web 认证服务器的 IP 地址加入到 Web 代理服务器的例外情
•况中，使 认证服务器的 地址不使用 代理服务器，避免 认证用户发送给Web IP Web Web Web认证页面的 HTTP 报文被发送到 Web 代理服务器上，从而影响正常的 Web 认证。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 配置允许触发 Web 认证的 Web 代理服务器端口。
web-auth proxy port port-number多次配置本命令可以添加多个 Web 认证代理服务器的 TCP 端口号，其中任意一个端口号发起的 HTTP 请求均可触发 Web 认证。

#### 1.14 Web认证显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 Web 认证功能的运行情况，通过查看显示信息验证配置的效果。
表1-1 Web 认证显示和维护操作 命令display web-auth [ interface interface-type显示接口上Web认证置信息interface-number ]显示所有Web认证用户免认证的目的IP地display web-auth free-ip址显示所有Web认证服务器信息 display web-auth server [ server-name ] display web-auth user [ interface interface-type显示在线Web认证用户的信息interface-number | slot slot-number ]

#### 1.15 Web认证典型配置举例

##### 1.15.1 使用本地AAA认证方式进行Web认证配置举例

###### 1. 组网需求

用户主机与 Device直接相连，在 Device的接口 Ten-GigabitEthernet1/0/1上对用户进行 Web认证。
具体要求如下：
• 使用本地认证方式进行认证和授权。
• Web 认证服务器的监听 IP 地址为 LoopBack 0 接口 IP 地址，TCP 端口号为 80。设备向 Web认证用户推出自定义的认证页面，并使用 HTTP 协议传输认证数据。

###### 2. 组网图

###### 3. 配置步骤

完成自定义缺省认证页面文件的编辑，将其压缩为名为 的 文件，之后通过 等方
(1) abc Zip FTP式上传到设备（略）。
(2) 配置各接口加入相应 VLAN、对应 VLAN 接口的 IP 地址和接口类型（略）。
(3) 配置本地用户\# 添加网络接入类本地用户，用户名为 localuser ，密码为明文输入的 localpass 。
<Device>system-view [Device] local-user localuser class network [Device-luser-network-localuser] password simple localpass \# 配置本地用户 localuser 的服务类型为 lan-access。
[Device-luser-network-localuser] service-type lan-access [Device-luser-network-localuser] quit
(4) 配置 IPS 域\# 创建一个名称为 local 的 ISP 域，使用本地认证、授权和计费方法。
[Device] domain local [Device-isp-local] authentication lan-access local [Device-isp-local] authorization lan-access local [Device-isp-local] accounting lan-access local [Device-isp-local] quit
(5) 配置本地 Portal Web 服务\# 开启本地 Portal Web 服务，并进入基于 HTTP 协议的本地 Portal Web 服务视图。
[Device] portal local-web-server http \# 配置本地 Portal Web 服务器提供的缺省认证页面文件为 abc.zip。（该自定义认证页面文件需符合编辑规范，并存在于设备存储介质的根目录下）
[Device-portal-local-websvr-http] default-logon-page abc.zip配置本地 服务的 服务侦听的 端口号为 80。
\# Portal Web HTTP TCP [Device–portal-local-websvr-http] tcp-port 80 [Device-portal-local-websvr-http] quit
(6) 配置 Web 认证\# 创建名称为 user 的 Web 认证服务器，并进入其视图。
[Device] web-auth server user配置 认证服务器的重定向 为 http://20.20.0.1:80/portal/。
\# Web URL [Device-web-auth-server-user] url http://20.20.0.1:80/portal/ \# 配置 Web 认证服务器的 IP 地址为 20.20.0.1，端口为 80。

[Device-web-auth-server-user] ip 20.20.0.1 port 80 [Device-web-auth-server-user] quit \# 指定 Web 认证用户使用的认证域为 local。
[Device] interface ten-gigabitethernet 1/0/1 [Device-Ten-GigabitEthernet1/0/1] web-auth domain local \# 开启 Web 认证，并指定引用的 Web 认证服务器为 user。
[Device-Ten-GigabitEthernet1/0/1] web-auth enable apply server user [Device-Ten-GigabitEthernet1/0/1] quit

###### 4. 验证配置举例

以上配置完成且 认证成功后，通过执行以下显示命令可查看在线 认证用户的信息。
Web Web <Device> display web-auth user Total online web-auth users: 1 User Name: localuser MAC address: acf1-df6c-f9ad Access interface: Ten-GigabitEthernet1/0/1 Initial VLAN: 100 Authorization VLAN: N/A Authorization ACL ID: N/A Authorization user profile: N/A

##### 1.15.2 使用RADIUS服务器远程AAA认证方式进行Web认证配置举例

###### 1. 组网需求

用户主机与接入设备 Device 直接相连，接入设备在接口 Ten-GigabitEthernet1/0/1 上对用户进行认证。具体要求如下：
Web使用远程 服务器进行认证、授权和计费。
• RADIUS认证服务器的监听 地址为 接口 地址，TCP 端口号为 80。设备向
• Web IP LoopBack 0 IP Portal用户推出自定义的认证页面，并使用 HTTP 协议传输认证数据。

###### 2. 组网图

RADIUS server
192.168.0.112/24 Vlan-int2
192.168.0.100/24 Vlan-int100
2.2.2.1/24 Internet XGE1/0/1 Device Host
2.2.2.2/24
20.20.0.1/24 Loop0

###### 3. 配置步骤

(1) 配置 RADIUS 服务器，添加用户账户，保证用户的认证/授权/计费功能正常运行（略）。
(2) 完成自定义缺省认证页面文件的编辑，将其压缩为名为 abc 的 Zip 文件，之后通过 FTP 等方
式上传到设备（略）。
(3) 配置各接口加入相应 VLAN、对应 VLAN 接口的 IP 地址和接口类型，保证各主机、服务器和
设备之间路由可达（略）。
(4) 配置 RADIUS 方案
\# 创建名称为 rs1 的 RADIUS 方案并进入该方案视图。
<Device> system-view
[Device] radius scheme rs1
配置 方案的主认证和主计费服务器及其通信密钥。
\# RADIUS
[Device-radius-rs1] primary authentication 192.168.0.112
[Device-radius-rs1] primary accounting 192.168.0.112
[Device-radius-rs1] key authentication simple radius
[Device-radius-rs1] key accounting simple radius
\# 配置发送给 RADIUS 服务器的用户名不携带 ISP 域名。
[Device-radius-rs1] user-name-format without-domain
[Device-radius-rs1] quit
配置认证域
(5)
创建并进入名称为 的 域。
\# dm1 ISP
[Device] domain dm1
\# 配置 ISP 域使用的 RADIUS 方案 rs1。
[Device-isp-dm1] authentication lan-access radius-scheme rs1
[Device-isp-dm1] authorization lan-access radius-scheme rs1
[Device-isp-dm1] accounting lan-access radius-scheme rs1
[Device-isp-dm1] quit
(6) 配置本地 Portal Web 服务
\# 开启本地 Portal Web 服务，并进入基于 HTTP 协议的本地 Portal Web 服务视图。
[Device] portal local-web-server http
\# 配置本地 Portal Web 服务提供的缺省认证页面文件为 abc.zip（设备的存储介质的根目录下
必须已存在该认证页面文件，否则功能不生效）。
[Device-portal-local-websvr-http] default-logon-page abc.zip
\# 配置本地 Portal Web 服务的 HTTP 服务侦听的 TCP 端口号为 80。
[Device–portal-local-websvr-http] tcp-port 80
[Device-portal-local-websvr-http] quit
配置 认证
(7) Web
创建名称为 的 认证服务器，并进入其视图。
\# user Web
[Device] web-auth server user
\# 配置 Web 认证服务器的重定向 URL 为 http://20.20.0.1:80/portal/ 。
[Device-web-auth-server-user] url http://20.20.0.1:80/portal/
配置 认证服务器的 地址为 20.20.0.1，端口号为 80。
\# Web IP
[Device-web-auth-server-user] ip 20.20.0.1 port 80
[Device-web-auth-server-user] quit

\# 指定 Web 认证用户使用的认证域为 dm1。
[Device] interface ten-gigabitethernet 1/0/1 [Device-Ten-GigabitEthernet1/0/1] web-auth domain dm1开启 认证，并指定引用的 认证服务器为 user。
\# Web Web [Device-Ten-GigabitEthernet1/0/1] web-auth enable apply server user [Device-Ten-GigabitEthernet1/0/1] quit

###### 4. 验证配置举例

以上配置完成且 Web 认证成功后，通过执行以下显示命令可查看在线 Web 认证用户的信息。
<Device> display web-auth user Total online web-auth users: 1 User Name: user1 MAC address: acf1-df6c-f9ad Access interface: Ten-GigabitEthernet1/0/1 Initial VLAN: 100 Authorization VLAN: N/A Authorization ACL ID: N/A Authorization user profile: N/A

#### 1.16 常见配置错误举例

##### 1.16.1 本地认证接口配置使用默认domain情况下，用户上线失败

###### 1. 故障现象

在接口下未配置 域且其他配置均正确的情况下，用户通过浏览器上线，上线失败。
ISP

###### 2. 故障分析

缺省情况下，开启 Web 认证的接口上未配置 Web 认证用户使用的认证域时，设备使用系统缺省的system 域，其缺省认证方式是本地（local）。所以本地认证失败原因可能有两个，一个是修改了系统缺省 system 域的认证方案，另一个是更改了系统缺省的 ISP 域。

###### 3. 处理过程

使用 命令查看缺省域下是否配置了正确的本地认证方案。如果不正确，请重新display domain配置。

## 06-Triple认证配置

目 录认证简介配置 认证

### 1 Triple认证

#### 1.1 Triple认证简介

Triple 认证是一种混合认证方案，它允许在接入用户的二层端口上同时开启 Web 认证、MAC 地址认证和 802.1X 认证功能，使得选用其中任意一种方式进行认证的终端均可通过该端口接入网络。
关于 802.1X、MAC 地址认证、Web 认证的详细介绍请分别参见“安全配置指导”中的“802.1X”、“MAC 地址认证”和“Web 认证”。

##### 1.1.1 典型组网

在终端形式多样的网络环境中，不同终端支持的接入认证方式有所不同。如 图 1-1 所示，有的终端只能进行MAC地址认证（比如打印机终端）；有的终端安装了 802.1X客户端软件，可以进行 802.1X认证；有的终端只希望通过 访问进行认证。为了灵活地适应这种网络环境中的多种认证需求，Web需要在接入用户的端口上部署Triple认证，使得用户可以选择任何一种适合的认证机制来进行认证，且只需要成功通过一种方式的认证即可实现接入，无需通过多种认证。
图1-1 Triple 认证典型应用组网图

##### 1.1.2 Triple认证机制

当端口上同时开启了 802.1X 认证、MAC 地址认证和 Web 认证功能后，不同类型的终端报文可触发不同的认证过程：
• 终端网卡接入网络时，如果发送 ARP 报文或者 DHCP 报文（广播报文），则首先触发 MAC地址认证。若 地址认证成功，则不需要再进行其它认证；若 地址认证失败，则允MAC MAC许触发 802.1X 或者 Web 认证。
• 如果终端使用系统自带的 802.1X 客户端或者第三方客户端软件发送 EAP 报文，或者在设备开启单播触发功能的情况下终端发送任意报文，则触发 802.1X 认证。
• 如果终端发送 HTTP 报文，则触发 Web 认证。

端口允许多种认证过程同时进行，且某一种认证失败不会影响同时进行的其它认证过程。一旦终端通过某一种认证，其它认证过程的进行情况有所不同：
如果终端首先通过 地址认证， 认证会立即终止，但 认证仍会继续进行。如
• MAC Web 802.1X果 802.1X 认证成功，则端口上生成的 802.1X 认证用户信息会覆盖已存在的 MAC 地址认证用户信息。否则，用户依然保持 MAC 地址认证在线，且允许再次触发 802.1X 认证，但不能再次触发 认证。
Web如果终端首先通过 802.1X 认证或者 Web 认证，则端口上其他认证会立即终止，且不能被再
•次触发。

##### 1.1.3 Triple认证支持VLAN下发

###### 1. 授权VLAN

服务器向通过认证的用户所在的端口下发授权 VLAN，端口将用户加入对应的授权 VLAN 中。

###### 2. 认证失败的VLAN

用户认证失败后，端口将认证失败的用户加入已配置的认证失败的 VLAN 中：
• 对于 802.1X 认证用户，认证失败的 VLAN 为端口上配置的 802.1X Auth-Fail VLAN。
• 对于 Web 认证用户，认证失败的 VLAN 为端口上配置的 Web Auth-Fail VLAN。
• 对于 MAC 地址认证用户，认证失败的 VLAN 为端口上配置的 Guest VLAN。
端口支持同时配置多种认证失败的 VLAN，用户认证失败后加入各 VLAN 的优先级由高到低分别为：
802.1X 的 Auth-Fail VLAN、MAC 地址认证的 Guest VLAN、Web 认证的 Auth-Fail VLAN。也就是说：
如果 Web 认证失败的用户再进行 MAC 地址认证且认证失败，用户会立刻离开已加入的 Web
•认证的 VLAN，而加入端口上配置的 地址认证的 VLAN。
Auth-Fail MAC Guest如果 认证或 地址认证失败的用户再进行 认证且认证失败，用户会立刻离开
• Web MAC 802.1X已加入的 Web Auth-Fail VLAN 或 MAC 地址认证的 Guest VLAN，而加入端口上配置的
802.1X Auth-Fail VLAN。

###### 3. 服务器不可达VLAN

用户在认证过程中若因服务器不可达导致认证失败，则端口将用户加入已配置的服务器不可达中：
VLAN对于 认证用户，服务器不可达 为端口上配置的 VLAN。
• 802.1X VLAN 802.1X Critical对于 认证用户，服务器不可达 为端口上配置的 VLAN。
• Web VLAN Web Auth-Fail对于 地址认证用户，服务器不可达 为端口上配置的 VLAN。
• MAC VLAN Critical端口支持同时配置多种服务器不可达 VLAN，用户因服务器不可达导致认证失败后加入各 的VLAN情况如下：
• 若用户没有进行 802.1X 认证，则用户加入最后一次认证失败的服务器不可达 VLAN。
如果 认证或 地址认证失败的用户再进行 认证且认证失败，用户会立刻离开
• Web MAC 802.1X已加入的 Web Auth-Fail VLAN 或 MAC 地址认证的 Critical VLAN 而加入端口上配置的 802.1X Critical VLAN。

##### 1.1.4 Triple认证支持ACL下发

设备能够根据服务器下发的授权 对通过认证的用户所在端口的数据流进行控制；在服务器上配ACL置授权 ACL 之前，需要在设备上配置相应的规则。管理员可以通过改变服务器的授权 ACL 设置或设备上对应的 ACL 规则来改变用户的访问权限。

##### 1.1.5 Triple认证支持在线用户探测功能

对于不同的认证用户，其在线探测功能方式不同：
对于 认证用户，通过开启用户在线检测定时器来探测用户是否在线。
• Web对于 认证用户，通过开启端口上的在线用户握手功能或者重认证功能来探测用户是否
• 802.1X在线。
• 对于 MAC 地址认证用户，通过开启下线检测定时器，来探测用户是否在线。
关于各扩展功能的详细介绍请分别参见“安全配置指导”中的“Web 认证”、“802.1X”、“MAC 地址认证”。

#### 1.2 Triple认证配置限制和指导

• 802.1X 认证必须配置为基于 MAC 的接入控制方式（macbased）。
• 如果端口最终加入到 802.1X 或 MAC 地址认证失败的 VLAN 中，且设备上开启了 Web 认证，
则需要将 802.1X 或 MAC 地址认证失败 VLAN 所在的网段设为 Web 认证的免认证 IP。否则，
用户将无法访问认证失败 VLAN 中的资源。
• 如果端口最终加入到 802.1X 或 MAC 地址认证服务器不可达 VLAN 中，且设备上开启了 Web
认证，则需要将 或 地址认证服务器不可达 所在的网段设为 认证的免
802.1X MAC VLAN Web
认证 IP。否则，用户将无法访问服务器不可达 VLAN 中的资源。
• 不要同时配置 Web 认证的免认证 IP 和 802.1X 的 Free IP，否则会使免认证 IP 不可用。

#### 1.3 配置Triple认证

请根据实际组网环境至少选择以下一项进行配置。
配置 认证
• 802.1X具体配置请参见“安全配置指导”的“802.1X”。
配置 MAC 地址认证
•具体配置请参见“安全配置指导”的“MAC 地址认证”。
• 配置 Web 认证具体配置请参见“安全配置指导”的“Web 认证”。

#### 1.4 Triple认证典型配置举例

##### 1.4.1 Triple认证基本功能配置举例

###### 1. 组网需求

如 图 1-2 所示，用户通过接入设备Device接入网络，要求在Device的二层端口上对所有用户进行统一认证，且只要用户通过 802.1X认证、Web认证、MAC地址认证中的任何一种认证，即可接入网络。具体需求如下：
• 终端上静态配置属于 192.168.1.0/24 网段的 IP 地址；
• 使用远程 RADIUS 服务器进行认证、授权和计费，且发送给 RADIUS 服务器的用户名不携带ISP 域名；
本地 Web 认证服务器的监听 IP 地址为 4.4.4.4，设备向 Web 认证用户推出系统默认的认证页
•面，并使用 传输认证数据。
HTTP

###### 2. 组网图

图1-2 Triple 认证基本功能配置组网图

###### 3. 配置步骤

配置各主机、服务器和设备之间路由可达（略）
(1)
配置 服务器
(2) RADIUS保证用户的认证/授权/计费功能正常运行。本例中，RADIUS 服务器上配置一个 802.1X 用户（帐户名为 userdot），一个 Web 认证用户（帐户名为 userpt），以及一个 MAC 地址认证用户（帐户名、密码均为 Printer 的 MAC 地址 f07d6870725f）。
(3) 配置 Web 认证\# 配置端口属于 VLAN 及对应 VLAN 接口的 IP 地址（略）。
\# 完成自定义缺省认证页面文件的编辑，将其压缩为名为 abc 的 Zip 文件，之后通过 FTP 等方式上传到设备（略）。
\# 配置本地 Portal Web 服务使用 HTTP 协议，且使用 Portal Web 服务器提供的缺省认证页面文件 abc.zip。
<Device> system-view

[Device] portal local-web-server http [Device-portal-local-websvr-http] default-logon-page abc.zip [Device-portal-local-websvr-http] quit \# 配置 LoopBack 接口 0 的 IP 地址为 4.4.4.4。
[Device] interface loopback 0 [Device-LoopBack0] ip address 4.4.4.4 32 [Device-LoopBack0] quit \# 创建名称为 webserver 的 Web 认证服务器，并进入其视图。
[Device] web-auth server webserver \# 配置 Web 认证服务器的重定向 URL 为 http://4.4.4.4/portal/。
[Device-web-auth-server-webserver] url http://4.4.4.4/portal/配置 认证服务器的 地址为 4.4.4.4，端口号为 80。
\# Web IP [Device-web-auth-server-webserver] ip 4.4.4.4 port 80 [Device-web-auth-server-webserver] quit \# 开启端口 Ten-GigabitEthernet1/0/1 上的 Web 认证，并指定引用的 Web 认证服务器为webserver 。
[Device] interface ten-gigabitethernet 1/0/1 [Device–Ten-GigabitEthernet1/0/1] web-auth enable apply server webserver [Device–Ten-GigabitEthernet1/0/1] quit
(4) 配置 802.1X 认证\# 开启全局 802.1X 认证。
[Device] dot1x开启端口 上的 认证（必须为基于 的接入控制方式）。
\# Ten-GigabitEthernet1/0/1 802.1X MAC [Device] interface ten-gigabitethernet 1/0/1 [Device–Ten-GigabitEthernet1/0/1] dot1x port-method macbased [Device–Ten-GigabitEthernet1/0/1] dot1x [Device–Ten-GigabitEthernet1/0/1] quit
(5) 配置 MAC 地址认证\# 开启全局 MAC 地址认证。
[Device] mac-authentication \# 开启端口 Ten-GigabitEthernet1/0/1 上的 MAC 地址认证。
[Device] interface ten-gigabitethernet 1/0/1 [Device–Ten-GigabitEthernet1/0/1] mac-authentication [Device–Ten-GigabitEthernet1/0/1] quit
(6) 配置 RADIUS 方案\# 创建并进入名字为 rs1 的 RADIUS 方案视图。
[Device] radius scheme rs1 \# 配置 RADIUS 方案的主认证和主计费服务器及其通信密钥。
[Device-radius-rs1] primary authentication 1.1.1.2 [Device-radius-rs1] primary accounting 1.1.1.2 [Device-radius-rs1] key authentication simple radius [Device-radius-rs1] key accounting simple radius \# 配置发送给 RADIUS 服务器的用户名不携带 ISP 域名。
[Device-radius-rs1] user-name-format without-domain

[Device-radius-rs1] quit
(7) 配置认证域\# 创建并进入名字为 triple 的 ISP 域。
[Device] domain triple配置 用户使用 方案 进行认证、授权、计费。
\# lan-access RADIUS rs1 [Device-isp-triple] authentication lan-access radius-scheme rs1 [Device-isp-triple] authorization lan-access radius-scheme rs1 [Device-isp-triple] accounting lan-access radius-scheme rs1 [Device-isp-triple] quit \# 配置系统缺省的 ISP 域为 triple。若用户登录时输入的用户名未携带 ISP 域名，则使用缺省域下的认证方案。
[Device] domain default enable triple

###### 4. 验证配置

\# Web 用户 userpt 通过 Web 浏览器访问外部网络，其 Web 请求均被重定向到认证页面http://4.4.4.4/portal/logon.html 。用户根据网页提示输入正确的用户名和密码后，能够成功通过 Web认证。通过 display web-auth user 命令查看已在线用户的信息。
[Device] display web-auth user Total online web-auth users: 1 User Name: localuser MAC address: acf1-df6c-f9ad Access interface: Ten-GigabitEthernet1/0/1 Initial VLAN: 8 Authorization VLAN: N/A Authorization ACL ID: N/A Authorization user profile: N/A打印机接入网络后，可成功通过 地址认证。通过\# MAC display mac-authentication connection 命令查看已在线用户的信息。
[Device] display mac-authentication connection Total connections: 1 Slot ID: 1 User MAC address: f07d-6870-725f Access interface: Ten-GigabitEthernet1/0/1 Username: f07d6870725f User access state: Successful Authentication domain: triple Initial VLAN: 8 Authorization untagged VLAN: N/A Authorization tagged VLAN: N/A Authorization VSI: N/A Authorization ACL ID: N/A Authorization user profile: N/A Authorization CAR: N/A Authorization URL: N/A Termination action: Default Session timeout period: N/A

Online from: 2015/01/04 18:01:43 Online duration: 0h 0m 2s \# 用户 userdot 通过 802.1X 客户端发起认证，输入正确的用户名和密码后，可成功通过 802.1X 认证。通过 display dot1x connection 命令查看已在线用户的信息。
[Device] display dot1x connection Total connections: 1 Slot ID: 1 User MAC address: 7446-a091-84fe Access interface: Ten-GigabitEthernet1/0/1 Username: userdot User access state: Successful Authentication domain: triple IPv4 address: 192.168.1.2 Authentication method: CHAP Initial VLAN: 8 Authorization untagged VLAN: N/A Authorization tagged VLAN list: N/A Authorization VSI: N/A Authorization ACL ID: N/A Authorization user profile: N/A Authorization CAR: N/A Authorization URL: N/A Termination action: Default Session timeout period: N/A Online from: 2015/01/04 18:13:01 Online duration: 0h 0m 14s

##### 1.4.2 Triple认证配合VLAN下发及Auth-Fail VLAN功能配置举例

###### 1. 组网需求

如 图 1-3 所示，用户通过接入设备Device接入网络，要求在Device的二层端口上对所有用户进行统一认证，且只要用户通过 802.1X认证、Web认证、MAC地址认证中的任何一种认证，即可接入网络。具体需求如下：
Web 认证用户通过 DHCP 动态获取 IP 地址，认证前使用 192.168.1.0/24 网段的 IP 地址，认
•证成功后使用 网段的 地址，认证失败后使用 网段的 地址。
3.3.3.0/24 IP 2.2.2.0/24 IP DHCP服务器可由接入设备充当也可外置，本例中由接入设备提供 DHCP 服务。
• 802.1X 用户在认证前通过 DHCP 动态获取 192.168.1.0/24 网段的 IP 地址，认证成功后通过DHCP 动态获取 3.3.3.0/24 网段的 IP 地址，认证失败后通过 DHCP 动态获取 2.2.2.0/24 网段的 IP 地址。
打印机成功接入网络后通过 DHCP 获取一个与它的 MAC 地址静态绑定的 IP 地址 3.3.3.111/24。
•
• 使用远程 RADIUS 服务器进行认证、授权和计费，且发送给 RADIUS 服务器的用户名不携带域名。
ISP认证服务器的监听 地址为 4.4.4.4，设备向 认证用户推出自定义的认证页面，并
• Web IP Web使用 HTTP 协议传输认证数据。
• 认证成功的用户可被授权加入 VLAN 3。

###### 3. 配置步骤

认证失败的用户将被加入 VLAN 2，允许访问其中的 Update 服务器资源。
•

###### 2. 组网图

图1-3 认证配合 下发及 功能配置组网图Triple VLAN Auth-Fail VLAN配置步骤
3.
(1) 配置各主机、服务器和设备之间路由可达（略）
(2) 配置 RADIUS 服务器保证用户的认证/授权/计费功能正常运行。本例中，RADIUS 服务器上配置一个 802.1X 用户（帐户名为 userdot），一个 认证用户（帐户名为 userpt），以及一个 地址认证用Web MAC户（帐户名、密码均为 Printer 的 MAC 地址 f07d6870725f），并配置授权 VLAN（VLAN 3）。
设置 服务器所在 地址设为免认证
(3) Update IP IP <Device> system-view [Device] web-auth free-ip 2.2.2.2 24
(4) 上传自定义缺省认证页面完成自定义缺省认证页面文件的编辑，将其压缩为名为 abc 的 Zip 文件，之后通过 FTP 等方式上传到设备。
(5) 配置 DHCP 服务\# 配置端口属于 VLAN 及对应 VLAN 接口的 IP 地址（略）。
\# 开启 DHCP 服务。
[Device] dhcp enable配置 的 地址不参与自动分配。
\# Update server IP [Device] dhcp server forbidden-ip 2.2.2.2 \# 配置 DHCP 地址池 1（动态分配的网段、地址租用期限、网关地址）。建议配置较小的地址租用期限，以缩短终端认证成功或失败后重新获取 地址的时间。
IP [Device] dhcp server ip-pool 1 [Device-dhcp-pool-1] network 192.168.1.0 mask 255.255.255.0 [Device-dhcp-pool-1] expired day 0 hour 0 minute 1 [Device-dhcp-pool-1] gateway-list 192.168.1.1 [Device-dhcp-pool-1] quit

\# 配置 DHCP 地址池 2（动态分配的网段、地址租用期限、网关地址）。建议配置较小的地址租用期限，以缩短终端认证成功后重新获取 地址的时间。
IP [Device] dhcp server ip-pool 2 [Device-dhcp-pool-2] network 2.2.2.0 mask 255.255.255.0 [Device-dhcp-pool-2] expired day 0 hour 0 minute 1 [Device-dhcp-pool-2] gateway-list 2.2.2.1 [Device-dhcp-pool-2] quit \# 配置 DHCP 地址池 3（动态分配的网段、地址租用期限、网关地址）。建议配置较小的地址租用期限，以缩短终端下线后重新获取 IP 地址的时间。
[Device] dhcp server ip-pool 3 [Device-dhcp-pool-3] network 3.3.3.0 mask 255.255.255.0 [Device-dhcp-pool-3] expired day 0 hour 0 minute 1 [Device-dhcp-pool-3] gateway-list 3.3.3.1 [Device-dhcp-pool-3] quit一般情况下，为缩小终端认证状态改变之后更新 IP 地址的时间，建议配置较小的地址租约期限，使得前一个状态的 IP 地址租约尽快过期，以触发新的 IP 地址申请。但是，地址租用期限的配置还要考虑终端的实现，例如 iNode 的 802.1X 客户端就可以选择在断开连接之后自动更新终端 IP 地址，而不必等待租约过期来重获 IP 地址，因此实际应用中需要根据当前组网环境合理调整取值。此处建议取值为 60s。
\# 配置 DHCP 地址池 4，将 MAC 地址为 f07d-6870-725f 的打印机与 IP 地址 3.3.3.111/24 绑定。
[Device] dhcp server ip-pool 4 [Device-dhcp-pool-4] static-bind ip-address 3.3.3.111 mask 255.255.255.0 client-identifier f07d-6870-725f [Device-dhcp-pool-4] quit
(6) 配置 Web 认证\# 配置本地 Portal Web 服务使用 HTTP 协议，且使用 Portal Web 服务器提供的缺省认证页面文件 defaultfile.zip。
[Device] portal local-web-server http [Device-portal-local-websvr-http] default-logon-page defaultfile.zip [Device-portal-local-websvr-http] quit配置 接口 的 地址为 4.4.4.4。
\# LoopBack 0 IP [Device] interface loopback 0 [Device-LoopBack0] ip address 4.4.4.4 32 [Device-LoopBack0] quit创建名称为 的 认证服务器，并进入其视图。
\# webserver Web [Device] web-auth server webserver \# 配置 Web 认证服务器的重定向 URL 为 http://4.4.4.4/portal/。
[Device-web-auth-server-webserver] url http://4.4.4.4/portal/ \# 配置 Web 认证服务器的 IP 地址为 4.4.4.4，端口号为 80。
[Device-web-auth-server-webserver] ip 4.4.4.4 port 80

[Device-web-auth-server-webserver] quit \# 配置 Update 服务器的 IP 地址为免认证 IP。
[Device] web-auth free-ip 2.2.2.2 24在端口 上开启 认证，并配置认证失败的 为 2。
\# Ten-GigabitEthernet1/0/1 Web VLAN VLAN [Device] interface ten-gigabitethernet 1/0/1 [Device–Ten-GigabitEthernet1/0/1] port link-type hybrid [Device–Ten-GigabitEthernet1/0/1] mac-vlan enable [Device–Ten-GigabitEthernet1/0/1] web-auth enable apply server webserver [Device–Ten-GigabitEthernet1/0/1] web-auth auth-fail vlan 2 [Device–Ten-GigabitEthernet1/0/1] quit配置 认证
(7) 802.1X开启全局 认证。
\# 802.1X [Device] dot1x \# 开启端口 Ten-GigabitEthernet1/0/1 上 802.1X 认证（必须为基于 MAC 的接入控制方式），并配置认证失败的 为 2。
VLAN VLAN [Device] interface ten-gigabitethernet 1/0/1 [Device–Ten-GigabitEthernet1/0/1] dot1x port-method macbased [Device–Ten-GigabitEthernet1/0/1] dot1x [Device–Ten-GigabitEthernet1/0/1] dot1x auth-fail vlan 2 [Device–Ten-GigabitEthernet1/0/1] quit
(8) 配置 MAC 地址认证\# 开启全局 MAC 地址认证。
[Device] mac-authentication \# 开启端口 Ten-GigabitEthernet1/0/1 上 MAC 地址认证，并配置认证失败的 VLAN 为 VLAN 2。
[Device] interface ten-gigabitethernet 1/0/1 [Device–Ten-GigabitEthernet1/0/1] mac-authentication [Device–Ten-GigabitEthernet1/0/1] mac-authentication guest-vlan 2 [Device–Ten-GigabitEthernet1/0/1] quit
(9) 配置 RADIUS 方案\# 创建并进入名字为 rs1 的 RADIUS 方案视图。
[Device] radius scheme rs1 \# 配置 RADIUS 方案的主认证和主计费服务器及其通信密钥。
[Device-radius-rs1] primary authentication 1.1.1.2 [Device-radius-rs1] primary accounting 1.1.1.2 [Device-radius-rs1] key authentication simple radius [Device-radius-rs1] key accounting simple radius \# 配置发送给 RADIUS 服务器的用户名不携带 ISP 域名。
[Device-radius-rs1] user-name-format without-domain [Device-radius-rs1] quit
(10) 配置认证域创建并进入名字为 的 域。
\# triple ISP [Device] domain triple \# 配置 lan-access 用户使用 RADIUS 方案 rs1 进行认证、授权、计费。

###### 4. 验证配置

[Device-isp-triple] authentication lan-access radius-scheme rs1 [Device-isp-triple] authorization lan-access radius-scheme rs1 [Device-isp-triple] accounting lan-access radius-scheme rs1 [Device-isp-triple] quit \# 配置系统缺省的 ISP 域为 triple。若用户登录时输入的用户名未携带 ISP 域名，则使用缺省域下的认证方案。
[Device] domain default enable triple验证配置
4.
\# Web 用户 userpt 通过 Web 浏览器访问外部网络，其 Web 请求均被重定向到认证页面http://4.4.4.4/portal/logon.html。用户根据网页提示输入正确的用户名和密码后，能够成功通过Web认证。通过 display web-auth user 命令查看已在线用户的信息。
[Device] display web-auth user Total online web-auth users: 1 User Name: userpt MAC address: 6805-ca17-4a0b Access interface: Ten-GigabitEthernet1/0/1 Initial VLAN: 8 Authorization VLAN: 3 Authorization ACL ID: N/A Authorization user profile: N/A \# 打印机接入网络后，可成功通过 MAC 地址认证。通过 display mac-authentication connection 命令查看已在线用户的信息。
[Device] display mac-authentication connection Total connections: 1 Slot ID: 1 User MAC address: f07d-6870-725f Access interface: Ten-GigabitEthernet1/0/1 Username: f07d6870725f User access state: Successful Authentication domain: triple Initial VLAN: 8 Authorization untagged VLAN: 3 Authorization tagged VLAN: N/A Authorization VSI: N/A Authorization ACL ID: N/A Authorization user profile: N/A Authorization CAR: N/A Authorization URL: N/A Termination action: Default Session timeout period: N/A Online from: 2015/01/04 18:01:43 Online duration: 0h 0m 2s \# 用户 userdot 通过 802.1X 客户端发起认证，输入正确的用户名和密码后，可成功通过 802.1X 认证。通过 display dot1x connection 命令查看已在线用户的信息。
[Device] display dot1x connection

Total connections: 1 Slot ID: 1 User MAC address: 7446-a091-84fe Access interface: Ten-GigabitEthernet1/0/1 Username: userdot User access state: Successful Authentication domain: triple IPv4 address: 3.3.3.3 Authentication method: CHAP Initial VLAN: 8 Authorization untagged VLAN: 3 Authorization tagged VLAN list: N/A Authorization VSI: N/A Authorization ACL ID: N/A Authorization user profile: N/A Authorization CAR: N/A Authorization URL: N/A Termination action: Default Session timeout period: N/A Online from: 2015/01/04 18:13:01 Online duration: 0h 0m 14s \# 通过 display mac-vlan all 命令查看到认证成功用户的 MAC VLAN 表项，该表项中记录了加入授权 的 地址与端口上生成的基于 的 之间的对应关系。
VLAN MAC MAC VLAN [Device] display mac-vlan all The following MAC VLAN addresses exist:
S:Static D:Dynamic MAC ADDR MASK VLAN ID PRIO STATE
-------------------------------------------------------- 6805-ca17-4a0b ffff-ffff-ffff 3 0 D f07d-6870-725f ffff-ffff-ffff 3 0 D 7446-a091-84fe ffff-ffff-ffff 3 0 D Total MAC VLAN address count:3通过 命令查看设备为在线用户分配的 地址信息。
\# display dhcp server ip-in-use IP [Device] display dhcp server ip-in-use IP address Client-identifier/ Lease expiration Type Hardware address
3.3.3.111 01f0-7d68-7072-5f Jan 4 18:14:17 2015 Auto:(C)
3.3.3.2 0168-05ca-174a-0b Jan 4 18:15:01 2015 Auto:(C)
3.3.3.3 0174-46a0-9184-fe Jan 4 18:15:03 2015 Auto:(C)
若用户认证失败，将被加入 VLAN 2 中，端口上生成的 MAC VLAN 表项及 IP 地址分配情况的查看方式同上，此处略。

## 07-端口安全配置

目 录端口安全简介配置端口安全模式配置准备将 地址设置为动态类型的安全 地址配置允许 迁移功能配置开放认证模式配置端口安全接入用户日志信息功能端口安全 模式配置举例

端口安全模式无法设置

### 1 端口安全

1端口安全

#### 1.1 端口安全简介

端口安全通过对已有的 802.1X 认证和 MAC 地址认证进行融合和扩充，在端口上为使用不同认证方式的用户提供基于 MAC 地址的网络接入控制。

##### 1.1.1 端口安全的主要功能

• 通过检测端口收到的数据帧中的源 MAC 地址来控制非授权设备或主机对网络的访问。
• 通过检测从端口发出的数据帧中的目的 MAC 地址来控制对非授权设备的访问。
• 通过定义各种端口安全模式，控制端口上的 MAC 地址学习或定义端口上的组合认证方式，让
设备学习到合法的源 MAC 地址，以达到相应的网络管理效果。

##### 1.1.2 端口安全的特性

###### 1. Need To Know特性（NTK）

Need To Know 特性通过检测从端口发出的数据帧的目的 MAC 地址，保证数据帧只能被发送到已经通过认证或被端口学习到的 MAC 所属的设备或主机上，从而防止非法设备窃听网络数据。

###### 2. 入侵检测（Intrusion Protection）特性

入侵检测特性对端口接收到的数据帧进行检测，源 地址未被端口学习到的报文或未通过认证MAC的报文，被认为是非法报文，如果发现非法报文，则对接收非法报文的端口采取相应的安全策略，包括端口被暂时断开连接、永久断开连接或 MAC 地址被过滤（默认 3 分钟，不可配），以保证端口的安全性。

##### 1.1.3 端口安全模式

端口安全模式分为两大类：控制 MAC 学习类和认证类。
• 控制 MAC 学习类：无需认证，包括端口自动学习 MAC 地址和禁止 MAC 地址学习两种模式。
• 认证类：利用 MAC 地址认证和 802.1X 认证机制来实现，包括单独认证和组合认证等多种模式。
配置了安全模式的端口上收到用户报文后，首先查找MAC地址表，如果该报文的源MAC地址已经存在于MAC地址表中，则端口转发该报文，否则根据端口所采用的安全模式进行MAC地址学习或者触发相应的认证，并在发现非法报文后触发端口执行相应的安全防护措施（Need Know、入To侵检测）或发送Trap告警。缺省情况下，端口出方向的报文转发不受端口安全限制，若触发了端口Need To Know，则才受相应限制。关于各模式的具体工作机制，以及是否触发Need To Know、入侵检测的具体情况请参见 表 1-1。

表1-1 端口安全模式描述表

|  | 端口安全采用方式 |  |  | 安全模式 |  |  |  | 触发的安全防护措施 |  |
|---|---|---|---|---|---|---|---|---|---|
|  |  |  | noRestrictions（缺省情况）表示端口的安全功能关闭，端口处于无限制状态 |  |  |  |  |  |  |
|  |  |  | autoLearn |  |  |  |  |  |  |
|  |  |  | secure |  |  |  |  |  |  |
|  |  |  | userLogin |  |  |  |  |  |  |
|  |  |  | userLoginSecure |  |  |  |  |  |  |
|  |  |  | userLoginSecureExt |  |  |  |  |  |  |
|  |  |  | userLoginWithOUI |  |  |  |  |  |  |
|  |  |  | macAddressWithRadius |  |  |  |  |  |  |
|  |  |  | Or |  | macAddressOrUserLoginSecure |  |  |  |  |
|  |  |  |  |  | macAddressOrUserLoginSecureExt |  |  |  |  |
|  |  |  | Else |  | macAddressElseUserLoginSecure |  |  |  |  |
|  |  |  |  |  | macAddressElseUserLoginSecureExt |  |  |  |  |

由于安全模式种类较多，为便于记忆，部分端口安全模式的名称可按如下规则理解：
• “userLogin”表示基于端口的 802.1X 认证。userLogin 之后，若携带“Secure”，则表示基于 MAC 地址的 802.1X 认证；若携带“Ext”，则表示可允许多个 802.1X 用户认证成功，否则表示仅允许一个 802.1X 用户认证成功。
• “macAddress”表示 MAC 地址认证。
• “Else”之前的认证方式先被采用，失败后根据请求认证的报文协议类型决定是否转为“Else”之后的认证方式。
“Or”之后的认证方式先被采用，失败后转为“Or”之前的认证方式。
•

###### 1. 端口控制MAC地址学习

• autoLearn
该模式下，端口不会将自动学习到的 地址添加为 地址表中的动态 地址，而
MAC MAC MAC
是将这些地址添加到安全 MAC 地址表中，称之为安全 MAC 地址。也可以通过
port-security mac-address security 命令手工配置端口下的安全 MAC 地址。
只有源 MAC 地址为安全 MAC 地址、通过命令 mac-address dynamic 或 mac-address
static 手工配置的 MAC 地址的报文，才能通过该端口。当端口下的安全 MAC 地址数超过
端口安全允许学习的最大安全 MAC 地址数后，端口模式会自动转变为 secure 模式。之后，
该端口停止添加新的安全 MAC。
• secure
该模式下，禁止端口学习 MAC 地址，只有源 MAC 地址为端口上的安全 MAC 地址、通过命
令 mac-address dynamic 或 mac-address static 手工配置的 MAC 地址的报文，才
能通过该端口。有关 地址的详细配置，请参见“二层技术-以太网交换”中的“MAC 地
MAC
址表”。

###### 2. 端口采用802.1X认证

• userLogin
此模式下，端口对接入用户采用基于端口的 802.1X 认证方式。端口下支持接入多个 802.1X
用户，且第一个 802.1X 用户认证成功后，其它用户无须认证就可接入。
• userLoginSecure
此模式下，端口对接入用户采用基于 MAC 地址的 802.1X 认证方式，且最多只允许一个 802.1X
认证用户接入。
userLoginSecureExt
•
该模式与 userLoginSecure 模式类似，但端口支持多个 802.1X 认证用户接入。
userLoginWithOUI
•
该模式与 userLoginSecure 模式类似，但端口上除了允许一个 802.1X 认证用户接入之外，还
额外允许一个特殊用户接入，该用户报文的源 的 与设备上配置的 值相符。
MAC OUI OUI
此模式下，报文首先进行 匹配，OUI 匹配失败的报文再进行 认证，OUI 匹配成功
OUI 802.1X
和 802.1X 认证成功的报文都允许通过端口。
OU（I Identifier，全球统一标识符）是 地址的前 位（二进制），
Organizationally Unique MAC 24
是 IEEE（Institute of Electrical and Electronics Engineers，电气和电子工程师学会）为不同
设备供应商分配的一个全球唯一的标识符。

###### 3. 端口采用MAC地址认证

macAddressWithRadius：端口对对接入用户采用 MAC 地址认证，且允许多个用户接入。

###### 4. 端口采用802.1X和MAC地址认证组合认证

macAddressOrUserLoginSecure
•端口同时处于 userLoginSecure 模式和 macAddressWithRadius 模式，且允许一个 802.1X 认证用户及多个 地址认证用户接入。
MAC此模式下，802.1X 认证优先级大于 MAC 地址认证：报文首先触发 802.1X 认证，默认情况下，如果 802.1X 认证失败再进行 MAC 地址认证；若开启了端口的 MAC 地址认证和 802.1X 认证并行处理功能，则端口配置了 802.1X 单播触发功能的情况下，当端口收到源 MAC 地址未知的报文，会向该 MAC 地址单播发送 EAP-Request 帧来触发 802.1X 认证，但不等待 802.1X认证处理完成，就同时进行 地址认证。
MAC
• macAddressOrUserLoginSecureExt与 类似，但允许端口下有多个 和 地址认证用macAddressOrUserLoginSecure 802.1X MAC户。
• macAddressElseUserLoginSecure端口同时处于 模式和 模式，但 地址认证优先macAddressWithRadius userLoginSecure MAC级大于 802.1X 认证。允许端口下一个 802.1X 认证用户及多个 MAC 地址认证用户接入。
非 802.1X 报文直接进行 MAC 地址认证。802.1X 报文先进行 MAC 地址认证，如果 MAC 地址认证失败再进行 802.1X 认证。

• macAddressElseUserLoginSecureExt
与 macAddressElseUserLoginSecure 类似，但允许端口下有多个 802.1X 和 MAC 地址认证
用户。

#### 1.2 端口安全配置限制和指导

由于端口安全特性通过多种安全模式提供了 802.1X 和 MAC 地址认证的扩展和组合应用，因
•此在需要灵活使用以上两种认证方式的组网环境下，推荐使用端口安全特性。无特殊组网要求的情况下，无线环境中通常使用端口安全特性。而在仅需要 802.1X、MAC 地址认证特性来完成接入控制的组网环境下，推荐单独使用相关特性。关于 802.1X、MAC 地址认证特性的详细介绍和具体配置请参见“安全配置指导”中的“802.1X”、“MAC 地址认证”。
仅支持在二层以太网接口上配置端口安全功能，且不支持在二层聚合组的成员端口上开启端
•口安全功能。

#### 1.3 端口安全配置任务简介

端口安全配置任务如下：
配置端口安全基本功能
(1)
使能端口安全(cid:123)
配置端口安全模式(cid:123)
配置端口安全允许的最大安全MAC地址数(cid:123)
配置安全MAC地址(cid:123)
（可选）配置Need To Know特性(cid:123)
（可选）配置入侵检测特性(cid:123)
(2) （可选）配置端口安全扩展功能配置当前端口不应用下发的授权信息(cid:123)
配置允许MAC迁移功能(cid:123)
配置授权失败用户下线功能(cid:123)
配置指定VLAN内端口安全功能允许同时接入的最大MAC地址数(cid:123)
配置开放认证模式(cid:123)
配置端口安全的Free VLAN功能(cid:123)
配置NAS-ID Profile (cid:123)
以上端口安全扩展功能，在未使能端口安全，但开启 802.1X 或 MAC 地址认证功能的情况下也适用。
(3) （可选）配置端口安全告警功能
(4) （可选）配置端口安全接入用户日志信息功能

#### 1.4 使能端口安全

##### 1. 配置限制和指导

当端口安全处于使能状态时，不能开启端口上的 以及 地址认证，且不能修改
• 802.1X MAC
802.1X 端口接入控制方式和端口授权状态，它们只能随端口安全模式的改变由系统更改。
• 可以通过 undo port-security enable 命令关闭端口安全。但需要注意的是，在端口上有用户在线的情况下，关闭端口会导致在线用户下线。
• 执行使能或关闭端口安全的命令后，端口上的如下配置会被自动恢复为以下缺省情况：
802.1X 端口接入控制方式为 macbased；
(cid:123)
802.1X 端口的授权状态为 auto。
(cid:123)
有关 802.1X 认证配置的详细介绍可参见“安全配置指导”中的“802.1X”。有关 MAC 地址认证配置的详细介绍可参见“安全配置指导”中的“MAC 地址认证”。

##### 2. 配置准备

在使能端口安全之前，需要关闭全局的 802.1X 和 MAC 地址认证。

##### 3. 配置步骤

进入系统视图。
(1)
system-view使能端口安全。
(2)
port-security enable缺省情况下，端口安全功能处于关闭状态。

#### 1.5 配置端口安全模式

##### 1. 配置限制和指导

• 在端口安全未使能的情况下，端口安全模式可以进行配置但不会生效。
• 端口上有用户在线的情况下，改变端口的安全模式会导致在线用户会下线。
如果端口上已经配置了端口安全模式，则不允许开启 认证和 地址认证。
• 802.1X MAC
当端口安全已经使能且当前端口安全模式不是 时，若要改变端口安全模式，
• noRestrictions
必须首先执行 undo port-security port-mode 命令恢复端口安全模式为 noRestrictions
模式。
• 端口安全模式为 macAddressWithRadius、macAddressElseUserLoginSecure、
macAddressElseUserLoginSecureExt、userLoginSecure、userLoginSecureExt、
macAddressOrUserLoginSecure、macAddressOrUserLoginSecureExt 或
userLoginWithOUI 时，设备支持 RADIUS 扩展属性下发重定向 URL。即：用户认证后，设备
会根据 RADIUS 服务器下发的重定向 URL 属性，将用户的 HTTP 或 HTTPS 请求重定向到指
定的 认证页面。Web 认证通过后，RADIUS 服务器记录用户的 地址，并通过
Web MAC DM
报文强制 Web 用户下线。此后该用户再次发起 802.1X 认证或 MAC 地址认证，由于 RADIUS
服务器上已记录该用户和其 MAC 地址的对应信息，用户可以成功上线。
• 若需要对用户的 HTTPS 请求进行重定向，需要在设备上配置对 HTTPS 报文进行重定向的内
部侦听端口号，具体配置请参见“三层技术-IP 业务配置指导”中的“HTTP 重定向”。

##### 2. 配置步骤

##### 2. 配置准备

在配置端口安全模式之前，端口上首先需要满足以下条件：
• 802.1X 认证关闭。
• MAC 地址认证关闭。
• 对于 autoLearn 模式，还需要提前设置端口安全允许的最大安全 MAC 地址数。但是如果端口已经工作在 autoLearn 模式下，则无法更改端口安全允许的最大安全 MAC 地址数。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置允许通过认证的用户 OUI 值。
port-security oui index index-value mac-address oui-value
缺省情况下，不存在允许通过认证的用户 OUI 值。
该命令仅在端口安全模式为 userLoginWithOUI 时必选。在这种情况下，端口除了可以允许一
个 802.1X 的接入用户通过认证之外，仅允许一个与某 OUI 值匹配的用户通过认证。
(3) 进入接口视图。
interface interface-type interface-number
(4) 配置端口的安全模式。
port-security port-mode { autolearn | mac-authentication |
mac-else-userlogin-secure | mac-else-userlogin-secure-ext | secure |
userlogin | userlogin-secure | userlogin-secure-ext |
userlogin-secure-or-mac | userlogin-secure-or-mac-ext |
userlogin-withoui }
缺省情况下，端口处于 noRestrictions 模式。

#### 1.6 配置端口安全允许的最大安全MAC地址数

##### 1. 功能简介

端口安全允许某个端口下有多个用户接入，但是允许的用户数不能超过规定的最大值。
配置端口允许的最大安全 地址 数有两个作用：
MAC控制端口允许接入网络的最大用户数。对于采用 802.1X、MAC 地址认证或者两者组合形式的
•认证类安全模式，端口允许的最大用户数取本命令配置的值与相应模式下允许认证用户数的最小值；
• 控制 autoLearn 模式下端口能够添加的最大安全 MAC 地址数。如果配置了 vlan 关键字，但未指定具体的 vlan-id-list 时，可控制接口允许的每个 VLAN 内的最大安全 MAC 地址数；
否则表示控制指定 内的最大安全 地址数。
vlan-id-list MAC端口安全允许的最大安全 地址数与“二层技术-以太网交换配置指导/MAC 地址表”中配置的MAC端口最多可以学习到的 MAC 地址数无关，且不受其影响。
配置步骤
2.
(1) 进入系统视图。

system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置端口安全允许的最大安全 MAC 地址数。
port-security max-mac-count max-count [ vlan [ vlan-id-list ] ]缺省情况下，端口安全不限制本端口可保存的最大安全 MAC 地址数。

#### 1.7 配置安全MAC地址

##### 1.7.1 功能简介

安全 MAC 地址是一种特殊的 MAC 地址，保存配置后重启设备，不会丢失。在同一个 VLAN 内，一个安全 MAC 地址只能被添加到一个端口上。
安全 MAC 地址可以通过以下两种途径生成：
由 autoLearn 安全模式下的使能端口安全功能的端口自动学习。
•
• 通过命令行手动添加。
缺省情况下，所有的安全 MAC 地址均不老化，除非被管理员通过命令行手工删除，或因为配置的改变（端口的安全模式被改变，或端口安全功能被关闭）而被系统自动删除。但是，安全 地MAC址不老化会带来一些问题：合法用户离开端口后，若有非法用户仿冒合法用户源 MAC 接入，会导致合法用户不能继续接入；虽然该合法用户已离开，但仍然占用端口 MAC 地址资源，而导致其它合法用户不能接入。因此，让某一类安全 MAC 地址能够定期老化，可提高端口接入的安全性和端口资源的利用率。
表1-2 安全 MAC 地址相关属性列表

|  | 类型 |  |  | 生成方式 |  |  | 配置保存机制 |  |  | 老化机制 |  |
|---|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  | 手工添加（未指定sticky 关键字） |  |  | 安全MAC地址在保存配置文件并重启设备后，仍然存在 |  |  |  |  |  |
|  |  |  | 手工添加（指定sticky 关键字），或端口自动学习 |  |  | Sticky MAC地址在保存配置文件并重启设备后，仍然存在，且其老化定时器会重新开始计时 Sticky MAC地址可通过配置转换为动态类型的MAC地址。动态类型的安全MAC地址不能被保存在配置文件中，设备重启后会被丢失 |  |  |  |  |  |

当端口下的安全 MAC 地址数目超过端口允许学习的最大安全 MAC 地址数后，端口安全模式变为secure 模式。该模式下，禁止端口学习 MAC 地址，只有源 MAC 地址为端口上的安全 MAC 地址或通过命令 或 手工配置的 地址的报文，才mac-address dynamic mac-address static MAC能通过该端口。

##### 1.7.2 配置准备

在配置安全 地址之前，需要完成以下配置任务：
MAC设置端口安全允许的最大 地址数。
• MAC配置端口安全模式为 autoLearn。
•当前的接口必须允许指定的 VLAN 通过或已加入该 VLAN，且该 VLAN 已存在。
•

##### 1.7.3 添加安全MAC地址

(1) 进入系统视图。
system-view
(2) 配置安全 MAC 地址的老化时间。
port-security timer autolearn aging [ second ] time-value
缺省情况下，安全 MAC 地址不会老化。
在系统视图或接口视图下配置安全 地址。
(3) MAC
在系统视图下配置安全 地址。
MAC
(cid:123)
port-security mac-address security [ sticky ] mac-address interface
interface-type interface-number vlan vlan-id
依次执行以下命令在接口视图下配置安全 MAC 地址。
(cid:123)
interface interface-type interface-number
port-security mac-address security [ sticky ] mac-address vlan vlan-id
缺省情况下，未配置安全 地址。
MAC
与相同 绑定的同一个 地址不允许同时指定为静态类型的安全 地址和
VLAN MAC MAC Sticky
MAC 地址。

##### 1.7.4 配置安全MAC地址为无流量老化

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置安全地址的老化方式为无流量老化。
port-security mac-address aging-type inactivity
缺省情况下，安全 MAC 地址按照固定时间进行老化，即在配置的安全 MAC 地址的老化时间
到达后立即老化。

##### 1.7.5 将Sticky MAC地址设置为动态类型的安全MAC地址

(1) 进入系统视图。
system-view
(2) 进入接口视图。

##### 1. 功能简介

interface interface-type interface-number
(3) 将 Sticky MAC 地址设置为动态类型的安全 MAC 地址。
port-security mac-address dynamic缺省情况下，Sticky MAC 地址能够被保存在配置文件中，设备重启后也不会丢失。

#### 1.8 配置Need To Know特性

##### 1. 配置步骤

特性用来限制认证端口上出方向的报文转发，可支持以下三种限制方式：
Need To Know ntkonly：仅允许目的 地址为已通过认证的 地址的单播报文通过。
• MAC MAC ntk-withbroadcasts：允许目的 地址为已通过认证的 地址的单播报文或广播
• MAC MAC地址的报文通过。
• ntk-withmulticasts：允许目的 MAC 地址为已通过认证的 MAC 地址的单播报文，广播地址或组播地址的报文通过。

##### 2. 配置限制和指导

配置了 Need To Know 的端口在以上任何一种方式下都不允许目的 MAC 地址未知的单播报文通过。
并非所有的端口安全模式都支持Need To Know特性，配置时需要先了解各模式对此特性的支持情况，具体请参见 表 1-1。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
进入接口视图。
(2)
interface interface-type interface-number
配置端口 特性。
(3) Need To Know
port-security ntk-mode { ntk-withbroadcasts | ntk-withmulticasts |
ntkonly }
缺省情况下，端口没有配置 Need To Know 特性，即所有报文都可成功发送。

#### 1.9 配置入侵检测特性

功能简介
1.
当设备检测到一个非法的用户通过端口试图访问网络时，入侵检测特性用于配置设备可能对其采取的安全措施，包括以下三种方式：
blockmac：表示将非法报文的源 MAC 地址加入阻塞 MAC 地址列表中，源 MAC 地址为阻塞
•地址的报文将被丢弃。此 地址在被阻塞 分钟（系统默认，不可配）后恢复正常。
MAC MAC 3 disableport：表示将收到非法报文的端口永久关闭。
•：表示将收到非法报文的端口暂时关闭一段时间。关闭时长
• disableport-temporarily可通过 port-security timer disableport 命令配置。

##### 2. 配置步骤

##### 1. 功能简介

##### 2. 配置限制和指导

macAddressElseUserLoginSecure 或 macAddressElseUserLoginSecureExt 安全模式下工作的端口，对于同一个报文，只有 MAC 地址认证和 802.1X 认证均失败后，才会触发入侵检测特性。

##### 3. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置入侵检测特性 。
port-security intrusion-mode { blockmac | disableport | disableport-temporarily }缺省情况下，不进行入侵检测处理。
（可选）依次执行以下命令配置系统暂时关闭端口的时间。
(4)
quit port-security timer disableport time-value缺省情况下，系统暂时关闭端口的时间为 20 秒。

#### 1.10 配置当前端口不应用下发的授权信息

##### 1. 功能简介

802.1X 用户或 MAC 地址认证用户通过本地认证或 RADIUS 认证时，本地设备或远程 RADIUS 服
务器会把授权信息下发给用户。通过此配置可实现端口是否忽略这类下发的授权信息。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置当前端口不应用 RADIUS 服务器或设备本地下发的授权信息。
port-security authorization ignore
缺省情况下，端口应用 RADIUS 服务器或设备本地下发的授权信息。

#### 1.11 配置允许MAC迁移功能

功能简介
1.
允许 MAC 迁移功能是指，允许在线的 802.1X 用户或 MAC 地址认证用户移动到设备的其它端口上接入后可以重新认证上线。缺省情况下，如果用户从某一端口上线成功，则该用户在未从当前端口下线的情况下无法在设备的其它端口上（无论该端口是否与当前端口属于同一 VLAN）发起认证，也无法上线。若开启了允许 MAC 地址迁移功能，则允许在线用户离开当前端口在设备的其它端口上（无论该端口是否与当前端口属于同一 VLAN）发起认证。如果该用户在后接入的端口上认证成

##### 3. 配置步骤

功，则当前端口会将该用户立即进行下线处理，保证该用户仅在一个端口上处于上线状态。如果服务器在线用户数已达到上限，将无法进行 地址迁移。
MAC

##### 2. 配置限制和指导

通常，不建议开启该功能，只有在用户漫游迁移需求的情况下建议开启此功能。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 开启允许 MAC 迁移功能。
port-security mac-move permit缺省情况下，允许 MAC 迁移功能处于关闭状态。

#### 1.12 配置授权失败用户下线功能

##### 1. 功能简介

接口上开启授权失败用户下线功能后，当服务器下发的授权信息（目前仅支持 ACL、User Profile）
在设备上不存在或者设备下发授权信息失败时，设备将强制用户下线。该功能用于配合服务器上的用户授权控制策略，它仅允许接口上成功下发了授权信息的用户在线。
对于授权 VLAN 失败的情况，设备会直接让用户直接下线，与此功能无关。
开启本功能时：
• 若不指定任何参数，用户下线之后，设备再次收到该用户的报文就对其进行认证处理。
若指定 参数，则表示开启用户授权失败下线静默功能。用户下线后，设备将
• quiet-period其加入对应认证类型的静默队列，并根据对应认证类型的静默定时器的值来确定用户认证失败以后，设备停止对其提供认证服务的时间间隔。在静默期间，设备不对来自认证失败用户的报文进行认证处理，直接丢弃；静默期后，设备再次收到该用户的报文，则对其进行认证处理。

##### 2. 配置准备

若开启本功能时指定了 quiet-period 参数则需要先完成如下配置：
• 对于 802.1X 用户，通过 dot1x quiet-period 命令开启 802.1X 认证静默定时器功能，并通过 dot1x timer quiet-period 命令设置静默定时器的值。
• 对于 MAC 地址认证用户，通过 mac-authentication timer quiet 命令配置 MAC 地址认证静默定时器的值。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
开启授权失败用户下线功能。
(2)
port-security authorization-fail offline [ quiet-period ]
缺省情况下，授权失败用户下线功能处于关闭状态，即授权失败后用户保持在线。

#### 1.13 配置指定VLAN内端口安全功能允许同时接入的最大MAC地址数

##### 1. 功能简介

通常情况下，端口上端口安全功能允许接入的 地址包括：
MAC端口上 地址认证成功用户的 地址；MAC 地址认证 VLAN、Critical 中
• MAC MAC Guest VLAN用户的 MAC 地址。
认证成功用户的 地址；802.1X 认证 VLAN、Auth-Fail VLAN、Critical
• 802.1X MAC Guest VLAN 中用户的 MAC 地址。
由于系统资源有限，如果当前端口上允许接入的 MAC 地址数过多，接入 MAC 地址之间会发生资源的争用，因此适当地配置端口安全功能允许同时接入的最大 MAC 地址数可以使属于当前端口的用户获得可靠的性能保障。当指定 内，端口允许接入的 地址数超过最大值后，该VLAN MAC VLAN内新接入的 MAC 地址将被拒绝。

##### 2. 配置限制和指导

配置的端口上指定 VLAN 内端口安全功能允许同时接入的最大 MAC 地址数，不能小于当前端口上相应 VLAN 已存在的 MAC 地址数；否则，本次配置不生效。

##### 3. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置指定 VLAN 内端口安全功能允许同时接入的最大 MAC 地址数。
port-security mac-limit max-number per-vlan vlan-id-list缺省情况下，端口上端口安全功能允许同时接入的最大 MAC 地址数为 2147483647。

#### 1.14 配置开放认证模式

##### 1. 功能简介

开启开放认证模式后，端口上的 802.1X、MAC 地址认证用户在接入时即使接入信息不正确（包含不存在的用户名或者错误的密码两种情况）也可以正常接入并访问网络。在这种模式下接入的用户被称为 open 用户，此类用户不支持授权和计费，但可通过 display dot1x connection open、display mac-authentication connection open 命令可以查看用户信息。当开启端口安全的开放认证模式后，不影响接入信息正确的用户正常上线，此类不属于 open 用户。

##### 2. 配置限制和指导

• 开启了全局端口安全的开放认证模式后，开放认证模式在所有端口生效；未开启全局端口安
全开放认证模式时，开放认证模式以端口上配置为准。
• 开放认证模式优先级低于 802.1X 的 Auth-Fail VLAN 和 MAC 地址认证的 Guest VLAN，即如
果端口上配置了 的 或 地址认证的 VLAN，密码错误的接
802.1X Auth-Fail VLAN MAC Guest
入用户会加入认证失败 VLAN，开放认证模式不生效。有关 802.1X、MAC 地址认证的详细介
绍，请参见“安全配置指导”中的“802.1X”和“MAC 地址认证”。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置全局开放认证模式。
port-security authentication open global
缺省情况下，全局端口安全的开放认证模式处于关闭状态。
(3) 进入接口视图。
interface interface-type interface-number
配置端口开放认证模式。
(4)
port-security authentication open
缺省情况下，接口端口安全的开放认证模式处于关闭状态。

#### 1.15 配置端口安全的Free VLAN功能

##### 1. 功能简介

开启 802.1X 认证、MAC 地址认证或端口安全功能并配置了端口安全模式为 userLogin、userLoginSecure 、 userLoginWithOUI 、 userLoginSecureExt 、 macAddressWithRadius 、、 、macAddressOrUserLoginSecure macAddressElseUserLoginSecure macAddressOrUserLoginSecureExt 或 macAddressElseUserLoginSecureExt 时，若配置了端口安全的 Free VLAN 功能，则 Free VLAN 内的流量不需要进行认证，设备直接转发。

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置端口安全的 Free VLAN。
port-security free-vlan vlan-id-list
缺省情况下，未配置端口安全的 Free VLAN。

#### 1.16 配置NAS-ID Profile

##### 1. 功能简介

用户的接入 VLAN 可标识用户的接入位置，而在某些应用环境中，网络运营商需要使用接入设备发送给 服务器的 属性值来标识用户的接入位置，因此接入设备上需要建立用RADIUS NAS-Identifier户接入 VLAN 与指定的 NAS-ID 之间的绑定关系。这样，当用户上线时，设备会将与用户接入 VLAN匹配的 NAS-ID 填充在 RADIUS 请求报文中的 NAS-Identifier 属性中发送给 RADIUS 服务器。

##### 2. 配置限制和指导

可以在系统视图下或者接口视图下进行配置，接口上的配置优先，若接口上没有配NAS-ID Profile置，则使用系统视图下的全局配置。

如果指定了 NAS-ID Profile，则此 Profile 中定义的绑定关系优先使用；如果未指定 NAS-ID Profile或指定的 中没有找到匹配的绑定关系，则使用设备名作为 NAS-ID。
Profile与 的绑定关系的配置请参考“安全配置指导”中的“AAA”。
NAS-ID VLAN

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 在系统视图或接口视图下指定引用的 NAS-ID Profile。
系统视图下指定引用的 NAS-ID Profile。
(cid:123)
port-security nas-id-profile profile-name
依次执行以下命令在接口视图下指定引用的 Profile。
NAS-ID
(cid:123)
interface interface-type interface-number
port-security nas-id-profile profile-name
缺省情况下，未指定引用的 Profile。
NAS-ID

#### 1.17 配置端口安全告警功能

##### 1. 功能简介

开启端口安全告警功能后，该模块会生成告警信息，用于报告该模块的重要事件。生成的告警信息将发送到设备的 SNMP 模块，通过设置 SNMP 中告警信息的发送参数，来决定告警信息输出的相关属性。有关告警信息的详细介绍，请参见“网络管理和监控配置指导”中的“SNMP”。

##### 2. 配置步骤

进入系统视图。
(1)
system-view打开指定告警信息的开关。
(2)
snmp-agent trap enable port-security [ address-learned | dot1x-failure | dot1x-logoff | dot1x-logon | intrusion | mac-auth-failure | mac-auth-logoff | mac-auth-logon ] *缺省情况下，所有告警信息的开关处于关闭状态。

#### 1.18 配置端口安全接入用户日志信息功能

##### 1. 功能简介

端口安全接入用户日志信息是为了满足网络管理员维护的需要，对用户的接入信息进行记录。设备生成的端口安全日志信息会交给信息中心模块处理，信息中心模块的配置将决定日志信息的发送规则和发送方向。关于信息中心的详细描述请参见“网络管理和监控配置指导”中的“信息中心”。

##### 2. 配置限制和指导

为了防止设备输出过多的端口安全接入用户日志信息，一般情况下建议关闭此功能。

##### 3. 配置步骤

(1) 进入系统视图。

###### 2. 组网图

system-view
(2) 开启端口安全接入用户日志信息功能。
port-security access-user log enable [ failed-authorization | mac-learning | violation ] *缺省情况下，端口安全接入用户日志信息功能处于关闭状态。
配置本命令时，如果未指定任何参数，将同时开启所有参数对应的日志功能。

#### 1.19 端口安全显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后端口安全的运行情况，通过查看显示信息验证配置的效果。
表1-3 端口安全显示和维护操作 命令显示端口安全的配置信息、运行情况和统 display port-security interface [ interface-type计信息 interface-number ] display port-security mac-address security显示安全MAC地址信息 [ interface interface-type interface-number ] [ vlan vlan-id ] [ count ] display port-security mac-address block [ interface显示阻塞MAC地址信息 interface-type interface-number ] [ vlan vlan-id ] [ count ]

#### 1.20 端口安全典型配置举例

##### 1.20.1 端口安全autoLearn模式配置举例

###### 1. 组网需求

在 的端口 上对接入用户做如下的限制：
Device Ten-GigabitEthernet1/0/1允许 个用户自由接入，不进行认证，将学习到的用户 地址添加为 地址，
• 64 MAC Sticky MAC老化时间为 30 分钟；
• 当安全 MAC 地址数量达到 64 后，停止学习；当再有新的 MAC 地址接入时，触发入侵检测，并将此端口关闭 30 秒。
组网图
2.
图1-1 端口安全 autoLearn 模式组网图

###### 3. 配置步骤

\# 使能端口安全。
<Device> system-view [Device] port-security enable \# 设置安全 MAC 地址的老化时间为 30 分钟。
[Device] port-security timer autolearn aging 30 \# 设置端口安全允许的最大安全 MAC 地址数为 64。
[Device] interface ten-gigabitethernet 1/0/1 [Device-Ten-GigabitEthernet1/0/1] port-security max-mac-count 64 \# 设置端口安全模式为 autoLearn。
[Device-Ten-GigabitEthernet1/0/1] port-security port-mode autolearn \# 设置触发入侵检测特性后的保护动作为暂时关闭端口，关闭时间为 30 秒。
[Device-Ten-GigabitEthernet1/0/1] port-security intrusion-mode disableport-temporarily [Device-Ten-GigabitEthernet1/0/1] quit [Device] port-security timer disableport 30

###### 4. 验证配置

上述配置完成后，可以使用如下显示命令查看端口安全的配置情况。
[Device] display port-security interface ten-gigabitethernet 1/0/1 Global port security parameters:
Port security : Enabled AutoLearn aging time : 30 min Disableport timeout : 30 s MAC move : Denied Authorization fail : Online NAS-ID profile : Not configured Dot1x-failure trap : Disabled Dot1x-logon trap : Disabled Dot1x-logoff trap : Disabled Intrusion trap : Disabled Address-learned trap : Disabled Mac-auth-failure trap : Disabled Mac-auth-logon trap : Disabled Mac-auth-logoff trap : Disabled Open authentication : Disabled OUI value list :
Index : 1 Value : 123401 Ten-GigabitEthernet1/0/1 is link-up Port mode : autoLearn NeedToKnow mode : Disabled Intrusion protection mode : DisablePortTemporarily Security MAC address attribute Learning mode : Sticky Aging type : Periodical Max secure MAC addresses : 64 Current secure MAC addresses : 0

Authorization : Permitted NAS-ID profile : Not configured Free VLANs : Not configured Open authentication : Disabled MAC-move VLAN check bypass : Disabled可以看到端口安全所允许的最大安全 MAC 地址数为 64，端口模式为 autoLearn，入侵检测保护动作为 DisablePortTemporarily，入侵发生后端口被禁用时间为 30 秒。
配置生效后，端口允许地址学习，学习到的 MAC 地址数可在上述显示信息的“Current number of secure MAC addresses”字段查看到，具体的 MAC 地址信息可以在接口视图下用 display this命令查看。
[Device] interface ten-gigabitethernet 1/0/1 [Device-Ten-GigabitEthernet1/0/1] display this \# interface Ten-GigabitEthernet1/0/1 port-security max-mac-count 64 port-security port-mode autolearn port-security mac-address security sticky 0002-0000-0015 vlan 1 port-security mac-address security sticky 0002-0000-0014 vlan 1 port-security mac-address security sticky 0002-0000-0013 vlan 1 port-security mac-address security sticky 0002-0000-0012 vlan 1 port-security mac-address security sticky 0002-0000-0011 vlan 1 \#当学习到的 地址数达到 后，用命令 display port-security interface 可以看到MAC 64端口模式变为 secure，再有新的 MAC 地址到达将触发入侵保护，可以通过命令 display interface 看到此端口关闭。30 秒后，端口状态恢复。此时，如果手动删除几条安全 MAC 地址后，端口安全的状态重新恢复为 autoLearn，可以继续学习 MAC 地址。

##### 1.20.2 端口安全userLoginWithOUI模式配置举例

###### 1. 组网需求

客户端通过端口 Ten-GigabitEthernet1/0/1 连接到 Device 上，Device 通过 RADIUS 服务器对客户端进行身份认证，如果认证成功，客户端被授权允许访问 Internet 资源。
地址为 的 服务器作为主认证服务器和从计费服务器， 地址为
• IP 192.168.1.2 RADIUS IP
192.168.1.3 的 RADIUS 服务器作为从认证服务器和主计费服务器。认证共享密钥为 name，计费共享密钥为 money。
• 所有接入用户都使用 ISP 域 sun 的认证/授权/计费方法，该域最多可同时接入 30 个用户；
• 系统向 RADIUS 服务器重发报文的时间间隔为 5 秒，重发次数为 5 次，发送实时计费报文的时间间隔为 15 分钟，发送的用户名不带域名。
端口 Ten-GigabitEthernet1/0/1 同时允许一个 802.1X 用户以及一个与指定 OUI 值匹配的设备
•接入。

###### 2. 组网图

图1-2 端口安全 userLoginWithOUI 模式组网图

###### 3. 配置步骤

• 下述配置步骤包含了部分 AAA/RADIUS 协议配置命令，具体介绍请参见“安全配置指导”中的
“AAA”。
• 保证客户端和 RADIUS 服务器之间路由可达。
配置
(1) AAA
配置 方案。
\# RADIUS
<Device> system-view
[Device] radius scheme radsun
[Device-radius-radsun] primary authentication 192.168.1.2
[Device-radius-radsun] primary accounting 192.168.1.3
[Device-radius-radsun] secondary authentication 192.168.1.3
[Device-radius-radsun] secondary accounting 192.168.1.2
[Device-radius-radsun] key authentication simple name
[Device-radius-radsun] key accounting simple money
[Device-radius-radsun] timer response-timeout 5
[Device-radius-radsun] retry 5
[Device-radius-radsun] timer realtime-accounting 15
[Device-radius-radsun] user-name-format without-domain
[Device-radius-radsun] quit
\# 配置 ISP 域。
[Device] domain sun
[Device-isp-sun] authentication lan-access radius-scheme radsun
[Device-isp-sun] authorization lan-access radius-scheme radsun
[Device-isp-sun] accounting lan-access radius-scheme radsun
[Device-isp-sun] quit
(2) 配置 802.1X
\# 配置 802.1X 的认证方式为 CHAP。（该配置可选，缺省情况下 802.1X 的认证方式为 CHAP）
[Device] dot1x authentication-method chap

\# 指定端口上接入的 802.1X 用户使用强制认证域 sun。
[Device] interface ten-gigabitethernet 1/0/1 [Device-Ten-GigabitEthernet1/0/1] dot1x mandatory-domain sun [Device-Ten-GigabitEthernet1/0/1] quit
(3) 配置端口安全\# 使能端口安全。
[Device] port-security enable \# 添加 5 个 OUI 值。（最多可添加 16 个，此处仅为示例。最终，端口仅允许一个与某 OUI值匹配的用户通过认证）
[Device] port-security oui index 1 mac-address 1234-0100-1111 [Device] port-security oui index 2 mac-address 1234-0200-1111 [Device] port-security oui index 3 mac-address 1234-0300-1111 [Device] port-security oui index 4 mac-address 1234-0400-1111 [Device] port-security oui index 5 mac-address 1234-0500-1111设置端口安全模式为 userLoginWithOUI。
\# [Device] interface ten-gigabitethernet 1/0/1 [Device-Ten-GigabitEthernet1/0/1] port-security port-mode userlogin-withoui [Device-Ten-GigabitEthernet1/0/1] quit

###### 4. 验证配置

\# 查看端口安全的配置信息。
[Device] display port-security interface ten-gigabitethernet 1/0/1 Global port security parameters:
Port security : Enabled AutoLearn aging time : 30 min Disableport timeout : 30 s MAC move : Denied Authorization fail : Online NAS-ID profile : Not configured Dot1x-failure trap : Disabled Dot1x-logon trap : Disabled Dot1x-logoff trap : Disabled Intrusion trap : Disabled Address-learned trap : Disabled Mac-auth-failure trap : Disabled Mac-auth-logon trap : Disabled Mac-auth-logoff trap : Disabled Open authentication : Disabled OUI value list :
Index : 1 Value : 123401 Index : 2 Value : 123402 Index : 3 Value : 123403 Index : 4 Value : 123404 Index : 5 Value : 123405 Ten-GigabitEthernet1/0/1 is link-up Port mode : userLoginWithOUI

###### 2. 组网图

NeedToKnow mode : Disabled Intrusion protection mode : NoAction Security MAC address attribute Learning mode : Sticky Aging type : Periodical Max secure MAC addresses : Not configured Current secure MAC addresses : 1 Authorization ：Permitted NAS-ID profile : Not configured Free VLANs : Not configured Open authentication : Disabled MAC-move VLAN check bypass : Disabled配置完成后，如果有 802.1X 用户上线，则可以通过上述显示信息看到当前端口保存的 MAC 地址数为 1。还可以通过 命令查看该 用户的在线情况。
display dot1x 802.1X此外，端口还允许一个 地址与 值匹配的用户通过，可以通过下述命令查看。
MAC OUI [Device] display mac-address interface ten-gigabitethernet 1/0/1 MAC Address VLAN ID State Port/NickName Aging 1234-0300-0011 1 Learned XGE1/0/1 Y

##### 1.20.3 端口安全macAddressElseUserLoginSecure模式配置举例

###### 1. 组网需求

客户端通过端口 Ten-GigabitEthernet1/0/1 连接到 Device 上，Device 通过 RADIUS 服务器对客户端进行身份认证。如果认证成功，客户端被授权允许访问 Internet 资源。
• 可以有多个 MAC 认证用户接入；
• 如果是 802.1X 用户请求认证，先进行 MAC 地址认证，MAC 地址认证失败，再进行 802.1X认证。最多只允许一个 802.1X 用户接入；
• MAC 地址认证设置用户名格式为用户 MAC 地址的形式；
• 上线的 MAC 地址认证用户和 802.1X 认证用户总和不能超过 64 个；
• 为防止报文发往未知目的 MAC 地址，启动 ntkonly 方式的 Need To Know 特性。
组网图
2.
图 1-3 端口安全 macAddressElseUserLoginSecure 模式组网图

###### 3. 配置步骤

• RADIUS认证/计费及ISP域的配置同“1.20.2 端口安全userLoginWithOUI模式配置举例”，
这里不再赘述。
• 保证接入用户和 RADIUS 服务器之间路由可达。
\# 使能端口安全。
<Device> system-view
[Device] port-security enable
\# 配置 MAC 认证的用户名和密码，使用带连字符“-”的 MAC 地址格式，其中字母大写。
[Device] mac-authentication user-name-format mac-address with-hyphen uppercase
配置 地址认证用户所使用的 域。
\# MAC ISP
[Device] mac-authentication domain sun
\# 配置 802.1X 的认证方式为 CHAP。（该配置可选，缺省情况下 802.1X 的认证方式为 CHAP）
[Device] dot1x authentication-method chap
\# 设置端口安全允许的最大 MAC 地址数为 64。
[Device] interface ten-gigabitethernet 1/0/1
[Device-Ten-GigabitEthernet1/0/1] port-security max-mac-count 64
\# 设置端口安全模式为 macAddressElseUserLoginSecure。
[Device-Ten-GigabitEthernet1/0/1] port-security port-mode mac-else-userlogin-secure
\# 指定端口上接入的 802.1X 用户使用强制认证域 sun。
[Device-Ten-GigabitEthernet1/0/1] dot1x mandatory-domain sun
[Device-Ten-GigabitEthernet1/0/1] quit
\# 设置端口 Need To Know 模式为 ntkonly。
[Device-Ten-GigabitEthernet1/0/1] port-security ntk-mode ntkonly
[Device-Ten-GigabitEthernet1/0/1] quit

###### 4. 验证配置

查看端口安全的配置信息。
\# [Device] display port-security interface ten-gigabitethernet 1/0/1 Global port security parameters:
Port security : Enabled AutoLearn aging time : 30 min Disableport timeout : 30 s MAC move : Denied Authorization fail : Online NAS-ID profile : Not configured Dot1x-failure trap : Disabled Dot1x-logon trap : Disabled Dot1x-logoff trap : Disabled Intrusion trap : Disabled Address-learned trap : Disabled Mac-auth-failure trap : Disabled

Mac-auth-logon trap : Disabled Mac-auth-logoff trap : Disabled Open authentication : Disabled OUI value list Ten-GigabitEthernet1/0/1 is link-up Port mode : macAddressElseUserLoginSecure NeedToKnow mode : NeedToKnowOnly Intrusion protection mode : NoAction Security MAC address attribute Learning mode : Sticky Aging type : Periodical Max secure MAC addresses : 64 Current secure MAC addresses : 0 Authorization : Permitted NAS-ID profile : Not configured Free VLANs : Not configured Open authentication : Disabled MAC-move VLAN check bypass : Disabled配置完成后，如果有用户认证上线，则可以通过下述显示信息看到当前端口上的用户认证信息。
\# 查看 MAC 地址认证信息。
[Device] display mac-authentication interface ten-gigabitethernet 1/0/1 Global MAC authentication parameters:
MAC authenticaiton : Enabled User name format : MAC address in uppercase(XX-XX-XX-XX-XX-XX)
Username : mac Password : Not configured Offline detect period : 300 s Quiet period : 180 s Server timeout : 100 s Reauth period : 3600 s Authentication domain : sun Online MAC-auth users : 3 Silent MAC users:
MAC address VLAN ID From port Port index Ten-GigabitEthernet1/0/1 is link-up MAC authentication : Enabled Carry User-IP : Disabled Authentication domain : Not configured Auth-delay timer : Disabled Periodic reauth : Disabled Re-auth server-unreachable : Logoff Guest VLAN : Not configured Guest VLAN auth-period : 30 s Critical VLAN : Not configured Critical voice VLAN : Disabled

Host mode : Single VLAN Offline detection : Enabled Authentication order : Default Guest VSI : Not configured Guest VSI auth-period : 30 s Critical VSI : Not configured Auto-tag feature : Disabled VLAN tag configuration ignoring : Disabled Max online users : 4294967295 Authentication attempts : successful 3, failed 7 Current online users : 0 MAC address Auth state 1234-0300-0011 Authenticated 1234-0300-0012 Authenticated 1234-0300-0013 Authenticated \# 查看 802.1X 认证信息。
[Device] display dot1x interface ten-gigabitethernet 1/0/1 Global 802.1X parameters:
802.1X authentication : Enabled CHAP authentication : Enabled Max-tx period : 30 s Handshake period : 15 s Quiet timer : Disabled Quiet period : 60 s Supp timeout : 30 s Server timeout : 100 s Reauth period : 3600 s Max auth requests : 2 EAD assistant function : Disabled EAD timeout : 30 min Domain delimiter : @ Online 802.1X users : 1 Ten-GigabitEthernet1/0/1 is link-up
802.1X authenticaiton : Enabled Handshake : Enabled Handshake reply : Disabled Handshake security : Disabled Unicast trigger : Disabled Periodic reauth : Disabled Port role : Authenticator Authorization mode : Auto Port access control : MAC-based Multicast trigger : Enabled Mandatory auth domain : sun Guest VLAN : Not configured Auth-Fail VLAN : Not configured Critical VLAN : Not configured

###### 3. 处理过程

Critical voice VLAN : Disabled Add Guest VLAN delay : Disabled Re-auth server-unreachable : Logoff Max online users : 4294967295 User IP freezing : Disabled Reauth period : 60 s Send Packets Without Tag : Disabled Max Attempts Fail Number : 0 Auth-Fail VSI : Not configured Critical VSI : Not configured Add Guest VSI delay : Disabled EAPOL packets: Tx 16331, Rx 102 Sent EAP Request/Identity packets : 16316 EAP Request/Challenge packets: 6 EAP Success packets: 4 EAP Failure packets: 5 Received EAPOL Start packets : 6 EAPOL LogOff packets: 2 EAP Response/Identity packets : 80 EAP Response/Challenge packets: 6 Error packets: 0 Online 802.1X users: 1 MAC address Auth state 0002-0000-0011 Authenticated此外，因为设置了 Need To Know 特性，目的 MAC 地址未知、广播和多播报文都被丢弃。

#### 1.21 端口安全常见故障处理

##### 1.21.1 端口安全模式无法设置

###### 1. 故障现象

无法设置端口的端口安全模式。

###### 2. 故障分析

在当前端口的端口安全模式已配置的情况下，无法直接对端口安全模式进行设置。
处理过程
3.
首先设置端口安全模式为 noRestrictions 状态，再设置新的端口安全模式。
[Device-Ten-GigabitEthernet1/0/1] undo port-security port-mode [Device-Ten-GigabitEthernet1/0/1] port-security port-mode autolearn

##### 1.21.2 无法配置安全MAC地址

###### 1. 故障现象

无法配置安全 地址。
MAC

###### 3. 处理过程

###### 2. 故障分析

端口安全模式为非 autoLearn 时，不能对安全 MAC 地址进行设置。
处理过程
3.
设置端口安全模式为 autoLearn 状态。
[Device-Ten-GigabitEthernet1/0/1] undo port-security port-mode [Device-Ten-GigabitEthernet1/0/1] port-security max-mac-count 64 [Device-Ten-GigabitEthernet1/0/1] port-security port-mode autolearn [Device-Ten-GigabitEthernet1/0/1] port-security mac-address security 1-1-2 vlan 1

## 08-User Profile配置

目 录简介

### 1 User Profile

#### 1.1 User Profile简介

Profile（用户配置文件）提供一个配置模板，用于定义针对一个或一类用户的一系列配置，例User如 QoS（Quality of Service，服务质量）策略。User Profile 可重复使用，并且在用户的接入端口发生变化后，无须重新为用户进行配置，减少了配置工作量。
用户访问设备时，需要先进行上线用户身份认证（例如通过 802.1X 接入认证方式）。用户通过身份认证后，认证服务器会将与用户帐户绑定的 User Profile 名称下发给设备，设备会根据指定 User Profile 里配置的内容对上线用户进行限制。
的典型应用为控制系统为上线用户分配资源。比如基于接口进行流量监管可限制一群User Profile用户（从指定接口接入的所有用户）对带宽资源的使用，而 User Profile 则可对单个用户进行流量监管。

#### 1.2 User Profile配置准备

User Profile 是和接入认证配合使用的，在配置 User Profile 前需要保证已完成相应的接入认证配置。
各接入认证对 User Profile 的支持情况，请参见相关接入认证模块的配置指导。

#### 1.3 配置User Profile

(1) 进入系统视图。
system-view
(2) 创建 User Profile 并进入相应的 User Profile 视图。
user-profile profile-name
(3) 基于 User Profile 应用已创建的 QoS 策略。
qos apply policy policy-name { inbound | outbound }
缺省情况下，未应用 QoS 策略。
关于 策略的具体介绍与配置，请参见“ACL 和 配置指导”中的 配置。
QoS QoS QoS

#### 1.4 User Profile显示和维护

在任意视图下执行 display 命令可以显示 User Profile 的配置信息和在线用户信息，通过查看显示信息验证配置的效果。
表1-1 显示 User Profile操作 命令显示 user profile 的配置信息和在线用 display user-profile [ name profile-name ] [ slot slot-number ]户信息

###### 3. 配置步骤

#### 1.5 User Profile典型配置举例

##### 1.5.1 802.1X本地认证/授权用户应用QoS策略典型配置举例

###### 1. 组网需求

如 图 1-1 所示，接入设备Device上连接了三个 802.1X认证用户，这些用户属于同一个ISP域“user”，为了提高认证/授权的效率，该ISP域内用户采用Device本地认证方法。现要求对三个用户的流量进行如下控制：
• UserA 在每天上午 8:30 至 12:00 间即使通过认证也不能访问网络。
• UserB 在通过认证后的上传速率限制为 2M。
• UserC 在通过认证后的下载速率限制为 4M。

###### 2. 组网需求

图1-1 802.1X 本地认证/授权用户应用 Qos 策略组网示意图XGE1/0/1 Internet Device User A User B Domain: user User C配置步骤
3.
(1) 创建对 UserA 的接入时间进行控制的 QoS 策略\# 创建周期时间段 for_usera，时间范围为每天的 8:30～12:00。
[Device] time-range for_usera 8:30 to 12:00 daily \# 定义基本 IPv4 ACL 2000，匹配 for_usera 内的所有报文。
[Device] acl basic 2000 [Device-acl-basic-2000] rule permit time-range for_usera [Device-acl-basic-2000] quit创建流分类 for_usera，分类规则为匹配 2000。
\# ACL [Device] traffic classifier for_usera [Device-classifier-for_usera] if-match acl 2000 [Device-classifier-for_usera] quit创建流行为 for_usera，动作为拒绝通过。
\# [Device] traffic behavior for_usera [Device-behavior-for_usera] filter deny [Device-behavior-for_usera] quit创建 策略 for_usera，将流分类和流行为进行关联。
\# QoS [Device] qos policy for_usera [Device-qospolicy-for_usera] classifier for_usera behavior for_usera [Device-qospolicy-for_usera] quit

(2) 为 UserA 创建 User Profile，并应用 QoS 策略
\# 创建 User Profile，名称为 usera。
[Device] user-profile usera
\# 由于是对 UserA 发送的报文进行过滤，因此在应用 QoS 策略时应该应用到设备的入方向。
[Device-user-profile-usera] qos apply policy for_usera inbound
[Device-user-profile-usera] quit
(3) 创建对 UserB 的速率进行限制的 QoS 策略
\# 创建流分类 class，匹配所有报文。
[Device] traffic classifier class
[Device-classifier-class] if-match any
[Device-classifier-class] quit
\# 创建流行为 for_userb，动作为流量监管，cir 为 2000kbps。
[Device] traffic behavior for_userb
[Device-behavior-for_userb] car cir 2000
[Device-behavior-for_userb] quit
\# 创建 QoS 策略 for_userb，将流分类和流行为进行关联。
[Device] qos policy for_userb
[Device-qospolicy-for_userb] classifier class behavior for_userb
[Device-qospolicy-for_userb] quit
(4) 为 UserB 创建 User Profile，并应用 QoS 策略
\# 创建 User Profile，名称为 userb。
[Device] user-profile userb
由于是对 发送的报文进行过滤，因此在应用 策略时应该应用到设备的入方向。
\# UserB QoS
[Device-user-profile-userb] qos apply policy for_userb inbound
[Device-user-profile-userb] quit
(5) 创建对 UserC 的速率进行限制的 QoS 策略
\# 创建流行为 for_userc，动作为流量监管，cir 为 4000kbps。
[Device] traffic behavior for_userc
[Device-behavior-for_userc] car cir 4000
[Device-behavior-for_userc] quit
\# 创建 QoS 策略 for_userc，将流分类和流行为进行关联。
[Device] qos policy for_userc
[Device-qospolicy-for_userc] classifier class behavior for_userc
[Device-qospolicy-for_userc] quit
(6) 为 UserC 创建 User Profile，并应用 QoS 策略
\# 创建 User Profile，名称为 userc。
[Device] user-profile userc
\# 由于是对 UserC 接收的报文进行过滤，因此在应用 QoS 策略时应该应用到设备的出方向。
[Device-user-profile-userc] qos apply policy for_userc outbound
[Device-user-profile-userc] quit
创建本地用户
(7)
创建名称为 的本地用户。
\# usera
[Device] local-user usera class network

New local user added.
\# 设置用户密码为“a12345”。
[Device-luser-network-usera] password simple a12345设置用户接入类型为 lan-access。
\# [Device-luser-network-usera] service-type lan-access \# 设置用户的授权 User Profile 为 usera。
[Device-luser-network-usera] authorization-attribute user-profile usera [Device-luser-network-usera] quit创建名称为 的本地用户。
\# userb [Device] local-user userb class network New local user added.
\# 设置用户密码为“b12345”。
[Device-luser-network-userb] password simple b12345设置用户接入类型为 lan-access。
\# [Device-luser-network-userb] service-type lan-access \# 设置用户的授权 User Profile 为 userb。
[Device -luser-network-userb] authorization-attribute user-profile userb [Device -luser-network-userb] quit \# 创建名称为 userc 的本地用户。
[Device] local-user userc class network New local user added.
设置用户密码为“c12345”。
\# [Device-luser-network-userc] password simple c12345 \# 设置用户接入类型为 lan-access。
[Device-luser-network-userc] service-type lan-access \# 设置用户的授权 User Profile 为 userc。
[Device-luser-network-userc] authorization-attribute user-profile userc [Device-luser-network-userc] quit
(8) 配置本地用户的认证/授权/计费方法\# 配置 ISP 域“user”内的 802.1X 用户的 AAA 方案为本地认证/授权，不计费[Device] domain user [Device-isp-user] authentication lan-access local [Device-isp-user] authorization lan-access local [Device-isp-user] accounting login none [Device-isp-user] quit
(9) 配置 802.1X 功能\# 开启指定端口 Ten-GigabitEthernet1/0/1 的 802.1X 特性。
[Device] interface ten-gigabitethernet 1/0/1 [DeviceA-Ten-GigabitEthernet1/0/1] dot1x配置基于 地址的接入控制方式（该配置可选，因为端口的接入控制在缺省情况下就是基于\# MAC MAC 地址的）。
[Device-Ten-GigabitEthernet1/0/1] dot1x port-method macbased [Device-Ten-GigabitEthernet1/0/1] quit \# 开启全局 802.1X 特性。

[Device] dot1x

###### 4. 验证配置

UserA、UserB、UserC 通过 802.1X 客户端连接网络，输入正确的用户名和密码后（注意用户名需要携带域名后缀，例如 应该输入用户名“usera@user”和密码“a12345”），认证成功并受UserA到相应的 Qos 策略的限制。
使用 diplay user-profile 命令在 Device 上可以查看到如下配置信息和在线用户信息。
<Device> display user-profile User-Profile: usera Inbound:
Policy: for_usera slot 1:
User -:
Authentication type: 802.1X Network attributes:
Interface : Ten-GigabitEthernet1/0/1 MAC address : 6805-ca06-557b Service VLAN : 1 User-Profile: userb Inbound:
Policy: for_userb slot 1:
User -:
Authentication type: 802.1X Network attributes:
Interface : Ten-GigabitEthernet1/0/1 MAC address : 80c1-6ee0-2664 Service VLAN : 1 User-Profile: userc Outbound:
Policy: for_userc slot 1:
User -:
Authentication type: 802.1X Network attributes:
Interface : Ten-GigabitEthernet1/0/1 MAC address : 6805-ca05-3efa Service VLAN : 1

## 09-Password Control配置

目 录简介配置限制和指导配置用户组密码管理显示和维护

### 1 Password Control

#### 1.1 Password Control简介

Control（密码管理）是设备提供的密码安全管理功能，它根据管理员定义的安全策略，Password对本地用户登录密码、super 密码的设置、老化、更新等方面进行管理，并对用户的登录状态进行控制。关于本地用户类型的详细介绍，请参见“安全配置指导”中的“AAA”。关于 super 密码的详细介绍，请参见“基础配置指导”中的“RBAC”。

##### 1.1.1 密码设置控制

###### 1. 密码最小长度限制

管理员可以限制用户密码的最小长度。当设置用户密码时，如果输入的密码长度小于设置的最小长度，系统将不允许设置该密码。

###### 2. 密码的组合检测功能

管理员可以设置用户密码的组成元素的组合类型，以及至少要包含每种元素的个数。密码的组成元素包括以下 4 种类型：
[A～Z]
•
• [a～z]
• [0～9]
• 32 个特殊字符（空格~`!@#$%^&*()_+-={}|[]\:”;’<>,./）
密码元素的组合类型有 4 种，具体涵义如下：
• 组合类型为 1 表示密码中至少包含 1 种元素；
• 组合类型为 2 表示密码中至少包含 2 种元素；
• 组合类型为 3 表示密码中至少包含 3 种元素；
• 组合类型为 4 表示密码中包含 4 种元素。
当用户设置密码时，系统会检查设定的密码是否符合配置要求，只有符合要求的密码才能设置成功。

###### 3. 密码的复杂度检测功能

密码的复杂度越低，其被破解的可能性就越大，比如包含用户名、使用重复字符等。出于安全性考虑，管理员可以设置用户密码的复杂度检测功能，确保用户的密码具有较高的复杂度。具体实现是：
配置用户密码时，系统检测输入的密码是否符合一定的复杂度要求，只有符合要求的密码才能设置成功。目前，复杂度检测功能对密码的复杂度要求包括以下两项：
• 密码中不能包含用户名或者字符顺序颠倒的用户名。例如，用户名为“abc”，那么“abc982”或者“2cba”之类的密码就不符合复杂度要求。
• 密码中不能包含连续三个或以上的相同字符。例如，密码“a111”就不符合复杂度要求。

##### 1.1.2 密码更新与老化

###### 1. 密码更新管理

管理员可以设置用户登录设备后修改自身密码的最小间隔时间。当用户登录设备修改自身密码时，如果距离上次修改密码的时间间隔小于配置值，则系统不允许修改密码。例如，管理员配置用户密码更新间隔时间为 48 小时，那么用户在上次修改密码后的 48 小时之内都无法成功进行密码修改操作。
有两种情况下的密码更新并不受该功能的约束：用户首次登录设备时系统要求用户修改密码；密码老化后系统要求用户修改密码。

###### 2. 密码老化管理

密码老化时间用来限制用户密码的使用时间。当密码的使用时间超过老化时间后，需要用户更换密码。
当用户登录时，如果用户输入已经过期的密码，系统将提示该密码已经过期，需要重新设置密码。
如果输入的新密码不符合要求，或连续两次输入的新密码不一致，系统将要求用户重新输入。对于FTP 用户，密码老化后，只能由管理员修改 FTP 用户的密码；对于 Telnet、SSH、Terminal（通过口登录设备）用户可自行修改密码。
Console

###### 3. 密码过期提醒

在用户登录时，系统判断其密码距离过期的时间是否在设置的提醒时间范围内。如果在提醒时间范围内，系统会提示该密码还有多久过期，并询问用户是否修改密码。如果用户选择修改，则记录新的密码及其设定时间。如果用户选择不修改或者修改失败，则在密码未过期的情况下仍可以正常登录。对于 用户，只能由管理员修改 用户的密码；对于 Telnet、SSH、Termina（l 通过FTP FTP Console口登录设备）用户可自行修改密码。

###### 4. 密码老化后允许登录管理

管理员可以设置用户密码过期后在指定的时间内还能登录设备指定的次数。这样，密码老化的用户不需要立即更新密码，依然可以登录设备。例如，管理员设置密码老化后允许用户登录的时间为15天、次数为 3 次，那么用户在密码老化后的 15 天内，还能继续成功登录 3 次。

###### 5. 密码历史记录

系统保存用户密码历史记录。当用户修改密码时，系统会要求用户设置新的密码，如果新设置的密码以前使用过，且在当前用户密码历史记录中，系统将给出错误信息，提示用户密码更改失败。另外，用户更改密码时，系统会将新设置的密码逐一与所有记录的历史密码以及当前密码比较，要求新密码至少要与旧密码有 4 字符不同，且这 4 个字符必须互不相同，否则密码更改失败。
可以配置每个用户密码历史记录的最大条数，当密码历史记录的条数超过配置的最大历史记录条数时，新的密码历史记录将覆盖该用户最老的一条密码历史记录。
由于为设备管理类本地用户配置的密码在哈希运算后以密文的方式保存，配置一旦生效后就无法还原为明文密码，因此，设备管理类本地用户的当前登录密码，不会被记录到该用户的密码历史记录中。

##### 1.1.3 用户登录控制

###### 1. 用户首次登录控制

当全局密码管理功能开启后，用户首次登录设备时，系统会输出相应的提示信息要求用户修改密码，否则不允许登录设备。这种情况下的修改密码不受密码更新时间间隔的限制。

###### 2. 密码尝试次数限制

密码尝试次数限制可以用来防止恶意用户通过不断尝试来破解密码。
每次用户认证失败后，系统会将该用户加入密码管理的黑名单。可加入密码管理功能黑名单的用户包括：FTP 用户和通过 VTY 方式访问设备的用户。不会加入密码管理功能黑名单的用户包括：用户名不存在的用户、通过 Console 口连接到设备的用户。
当用户连续尝试认证的失败累加次数达到设置的尝试次数时，系统对用户的后续登录行为有以下三种处理措施：
永久禁止该用户登录。只有管理员把该用户从密码管理的黑名单中删除后，该用户才能重新
•登录。
不对该用户做禁止，允许其继续登录。在该用户登录成功后，该用户会从密码管理的黑名单
•中删除。
• 禁止该用户一段时间后，再允许其重新登录。当配置的禁止时间超时或者管理员将其从密码管理的黑名单中删除，该用户才可以重新登录。

###### 3. 用户帐号闲置时间管理

管理员可以限制用户帐号的闲置时间，禁止在闲置时间之内始终处于不活动状态的用户登录。若用户自从最后一次成功登录之后，在配置的闲置时间内再未成功登录过，那么该闲置时间到达之后此用户账号立即失效，系统不再允许使用该账号的用户登录。

##### 1.1.4 密码不回显

出于安全考虑，用户输入密码时，系统将不回显用户的密码。

##### 1.1.5 日志功能

当用户成功修改密码或用户登录失败加入密码管理黑名单时，系统将会记录相应的日志。

#### 1.2 FIPS相关说明

设备运行于 模式时，本特性部分配置相对于非 模式有所变化，具体差异请见本文相关描FIPS FIPS述。有关 FIPS 模式的详细介绍请参见“安全配置指导”中的“FIPS”。

#### 1.3 Password Control配置限制和指导

设备存储空间不足会造成以下两个影响：
• 不能开启全局密码管理功能；
• 全局密码管理功能处于开启的状态下，用户登录设备失败。
本特性的各功能可支持在多个视图下配置，各视图可支持的功能不同。而且，相同功能的命令在不同视图下或针对不同密码时有效范围有所不同，具体情况如下：
系统视图下的全局配置对所有本地用户密码都有效；
•用户组视图下的配置只对当前用户组内的所有本地用户密码有效；
•本地用户视图下的配置只对当前的本地用户密码有效；
•为 super 密码的各管理参数所作的配置只对 super 密码有效。
•对于本地用户密码的各管理参数，其生效的优先级顺序由高到低依次为本地用户视图、用户组视图、系统视图。

#### 1.4 Password Control配置任务简介

Password Control 配置任务如下：
(1) 开启密码管理
(2) （可选）配置全局密码管理
(3) （可选）配置用户组密码管理
(4) （可选）配置本地用户密码管理
(5) （可选）配置super密码管理

#### 1.5 开启密码管理

##### 1. 功能简介

开启全局密码管理功能，是密码管理所有配置生效的前提。若要使得具体的密码管理功能（密码老化、密码最小长度、密码历史记录、密码组合检测）生效，还需开启指定的密码管理功能。

##### 2. 配置限制和指导

开启全局密码管理功能，有以下配置限制和指导：
• 开启设备管理类本地用户全局密码管理功能后，设备管理类本地用户密码以及 super 密码的配置将不被显示，即无法通过相应的 display 命令查看到设备管理类本地用户密码以及super 密码的配置。
开启网络接入类本地用户全局密码管理功能后，网络接入类本地用户密码配置将不被显示，
•即无法通过相应的 display 命令查看到网络接入类本地用户密码配置。
首次设置的本地用户密码必须至少由四个不同的字符组成。
•模式下，设备管理类本地用户的全局密码管理功能处开启状态，且不能关闭。
• FIPS

Password Control会记录用户配置密码时的 UTC时间。如果因设备断电重启等原因，UTC时
•间与 记录的 UTC时间不一致，可能导致密码老化管理功能出错。因此，为Password Control保证密码老化管理功能的正常工作，建议设备通过 NTP（Network Time Protocol，网络时间协议）协议获取 UTC 时间。关于 NTP 的详细介绍，请参见“网络管理和监控配置指导”中的“NTP”。
开启全局密码管理功能后，设备自动生成后缀名为“dat”的文件并保存于存储介质中用于记
•录本地用户的认证、登录信息。请不要手工删除或修改该文件。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 开启全局密码管理功能。
（非 FIPS 模式）
password-control enable [ network-class ]
缺省情况下，设备管理类本地用户和网络接入类本地用户全局密码管理功能均处于关闭状态。
（FIPS 模式）
password-control enable [ network-class ]
缺省情况下，设备管理类本地用户全局密码管理功能处于开启状态，且不能关闭；网络接入
类本地用户全局密码管理功能处于关闭状态。
(3) （可选）开启指定的密码管理功能。
password-control { aging | composition | history | length } enable
缺省情况下，各密码管理功能均处于开启状态。

#### 1.6 配置全局密码管理

##### 1. 配置限制和指导

系统视图下的全局密码管理参数对所有设备管理类和网络接入类的本地用户生效。
设备管理类用户支持所有的密码管理功能，其中对密码老化时间、密码最小长度、密码复杂度检查策略、密码组合策略以及用户登录尝试失败后的行为的配置，可分别在系统视图、用户组视图、本地用户视图下配置相关参数，其生效优先级从高到低依次为：本地用户视图 用户组视图 系统视
-> ->图。
网络接入类用户支持的密码管理功能仅包括：配置密码最小长度、配置密码的复杂度检查策略、配置密码的组合策略、配置密码更新的最小时间间隔、配置每个用户密码历史记录的最大条数。其中对密码最小长度、密码复杂度检查策略以及密码组合策略的配置，可分别在系统视图、用户组视图、本地用户视图下配置相关参数，其生效优先级从高到低依次为：本地用户视图->用户组视图->系统视图。
除用户登录尝试失败后的行为配置属于即时生效的配置，会在配置生效后立即影响密码管理黑名单中当前用户的锁定状态以及这些用户后续的登录之外，其它全局密码管理配置生效后仅对后续登录的用户以及后续设置的用户密码有效，不影响当前用户。

##### 2. 配置步骤

(1) 进入系统视图。

system-view
(2) 控制密码设置配置用户密码的最小长度。
(cid:123)
（非 FIPS 模式）
password-control length length缺省情况下，用户密码的最小长度为 10 个字符。
（FIPS 模式）
password-control length length缺省情况下，用户密码的最小长度为 15 个字符。
配置用户密码的组合策略。
(cid:123)
（非 FIPS 模式）
password-control composition type-number type-number [ type-length type-length ]缺省情况下，密码元素的组合类型至少为 1 种，至少要包含每种元素的个数为 1 个。
（FIPS 模式）
password-control composition type-number type-number [ type-length type-length ]缺省情况下，密码元素的组合类型至少为 4 种，至少要包含每种元素的个数为 1 个。
配置用户密码的复杂度检查策略。
(cid:123)
password-control complexity { same-character | user-name } check缺省情况下，不对用户密码进行复杂度检查。
配置每个用户密码历史记录的最大条数。
(cid:123)
password-control history max-record-number缺省情况下，每个用户密码历史记录的最大条数为 4 条。
(3) 管理密码更新与老化配置用户密码更新的最小时间间隔。
(cid:123)
password-control update-interval interval缺省情况下，用户密码更新的最小时间间隔为 24 小时。
配置用户密码的老化时间。
(cid:123)
password-control aging aging-time缺省情况下，用户密码的老化时间为 天。
90配置密码过期前的提醒时间。
(cid:123)
password-control alert-before-expire alert-time缺省情况下，密码过期前的提醒时间为 7 天。
配置密码过期后允许用户登录的时间和次数。
(cid:123)
password-control expired-user-login delay delay times times缺省情况下，密码过期后的 30 天内允许用户登录 3 次。
(4) 控制用户登录

配置用户登录尝试次数以及登录尝试失败后的行为。
(cid:123)
password-control login-attempt login-times [ exceed { lock | lock-time time | unlock } ]缺省情况下，用户登录尝试次数为 次；如果用户登录失败，则 分钟后再允许该用户重3 1新登录。
配置用户帐号的闲置时间。
(cid:123)
password-control login idle-time idle-time缺省情况下，用户帐号的闲置时间为 90 天。
用户账号闲置超时后该账号将会失效，用户无法正常登录设备。若不需要账号闲置时间检查功能，可将 idle-time 配置为 0，表示 Password Control 对用户账号闲置时间无限制。
配置用户认证的超时时间。
(cid:123)
password-control authentication-timeout timeout缺省情况下，用户认证的超时时间为 600 秒。
本功能仅对 telnet 和终端接入类型的登录用户生效，用户认证超时后连接断开。

#### 1.7 配置用户组密码管理

进入系统视图。
(1)
system-view
(2) 创建用户组，并进入用户组视图。
user-group group-name缺省情况下，不存在任何用户组。
用户组的相关配置请参见“安全配置指导”中的“AAA”。
(3) 配置用户组的密码老化时间。
password-control aging aging-time缺省情况下，采用全局密码老化时间。
(4) 配置用户组的密码最小长度。
password-control length length缺省情况下，采用全局密码最小长度。
(5) 配置用户组密码的组合策略。
password-control composition type-number type-number [ type-length type-length ]缺省情况下，采用全局密码组合策略。
(6) 配置用户组密码的复杂度检查策略。
password-control complexity { same-character | user-name } check缺省情况下，采用全局密码复杂度检查策略。
(7) 配置用户组登录尝试次数以及登录尝试失败后的行为。
password-control login-attempt login-times [ exceed { lock | lock-time time | unlock } ]

缺省情况下，采用全局的用户登录尝试限制策略。

#### 1.8 配置本地用户密码管理

(1) 进入系统视图。
system-view
(2) 创建设备管理类或网络接入类本地用户，并进入本地用户视图。
创建设备管理类本地用户，并进入本地用户视图
(cid:123)
local-user user-name class manage
创建网络接入类本地用户，并进入本地用户视图。
(cid:123)
local-user user-name class network
缺省情况下，不存在任何本地用户。
本地用户的相关配置请参见“安全配置指导”中的“AAA”。
(3) 配置本地用户的密码老化时间。
password-control aging aging-time
缺省情况下，采用本地用户所属用户组的密码老化时间。
仅设备管理类本地用户支持此配置。
配置本地用户的密码最小长度。
(4)
password-control length length
缺省情况下，采用本地用户所属用户组的密码最小长度。
(5) 配置本地用户的密码组合策略。
password-control composition type-number type-number [ type-length
type-length ]
缺省情况下，采用本地用户所属用户组的密码组合策略。
配置本地用户密码的复杂度检查策略。
(6)
password-control complexity { same-character | user-name } check
缺省情况下，采用本地用户所属用户组的密码复杂度检查策略。
(7) 配置本地用户登录尝试次数以及登录尝试失败后的行为。
password-control login-attempt login-times [ exceed { lock | lock-time
time | unlock } ]
缺省情况下，采用本地用户所属用户组的用户登录尝试限制策略。
仅设备管理类本地用户支持此配置。

#### 1.9 配置super密码管理

(1) 进入系统视图。
system-view
(2) 配置 super 密码的老化时间。
password-control super aging aging-time
缺省情况下，密码的老化时间为 90 天。

(3) 配置 super 密码的最小长度。
（非 FIPS 模式）
password-control super length length
缺省情况下，密码的最小长度为 10 个字符。
（FIPS 模式）
password-control super length length
缺省情况下，密码的最小长度为 15 个字符。
(4) 配置 super 密码的组合策略。
（非 FIPS 模式）
password-control super composition type-number type-number
[ type-length type-length ]
缺省情况下，密码元素的组合类型至少为 1 种，至少要包含每种元素的个数为 1 个。
（FIPS 模式）
password-control super composition type-number type-number
[ type-length type-length ]
缺省情况下，密码元素的组合类型至少为 4 种，至少要包含每种元素的个数为 1 个。

#### 1.10 Password Control显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 Password Control 的运行情况，通过查看显示信息验证配置的效果。
在用户视图下执行 reset 命令可以清除 Password Control 统计信息。
表1-1 Password Control 显示和维护操作 命令显示密码管理的配置信息 display password-control [ super ]显示用户认证失败后，被加入密码 display password-control blacklist [ user-name user-name | ip ipv4-address | ipv6 ipv6-address ]管理黑名单中的用户信息清除密码管理黑名单中的用户 reset password-control blacklist [ user-name user-name ] reset password-control history-record [ user-name清除用户的密码历史记录 user-name | super [ role role-name ] | network-class [ user-name user-name ] ]当密码历史记录功能未启动时，reset password-control history-record 命令同样可以清除全部或者某个用户的密码历史记录。

#### 1.11 Password Control典型配置举例

##### 1.11.1 Password Control基础配置举例

###### 1. 组网需求

有以下密码管理需求：
全局密码管理策略：用户 次登录失败后就永久禁止登录；最小密码长度为 个字符，密码
• 2 16老化时间为 30 天；允许用户进行密码更新的最小时间间隔为 36 小时；密码过期后 60 天内允许登录 5 次；用户帐号的闲置时间为 30 天；不允许密码中包含用户名或者字符顺序颠倒的用户名；不允许密码中包含连续三个或以上相同字符；密码元素的最少组合类型为 种，至少4要包含每种元素的个数为 4 个。
• 切换到用户角色 network-operator时使用的 super密码管理策略：最小密码长度为 24个字符，密码元素的最少组合类型为 4 种，至少要包含每种元素的个数为 5 个。
• 本地 Telnet 用户 test 的密码管理策略：最小密码长度为 24 个字符，密码元素的最少组合类型为 4 种，至少要包含每种元素的个数为 5 个，密码老化时间为 20 天。

###### 2. 配置步骤

\# 开启全局密码管理功能。
<Sysname> system-view [Sysname] password-control enable配置用户 次登录失败后就永久禁止该用户登录。
\# 2 [Sysname] password-control login-attempt 2 exceed lock \# 配置全局的密码老化时间为 30 天。
[Sysname] password-control aging 30 \# 配置全局的密码的最小长度为 16。
[Sysname] password-control length 16配置密码更新的最小时间间隔为 小时。
\# 36 [Sysname] password-control update-interval 36 \# 配置用户密码过期后的 60 天内允许登录 5 次。
[Sysname] password-control expired-user-login delay 60 times 5 \# 配置用户帐号的闲置时间为 30 天。
[Sysname] password-control login idle-time 30 \# 开启在配置的密码中检查包含用户名或者字符顺序颠倒的用户名的功能。
[Sysname] password-control complexity user-name check \# 开启在配置的密码中检查包含连续三个或以上相同字符的功能。
[Sysname] password-control complexity same-character check \#配置全局的密码元素的最少组合类型为 种，至少要包含每种元素的个数为 个。
4 4 [Sysname] password-control composition type-number 4 type-length 4 \# 配置 super 密码的最小长度为 24。
[Sysname] password-control super length 24 \# 配置 super 密码元素的最少组合类型为 4 种，至少要包含每种元素的个数为 5 个。
[Sysname] password-control super composition type-number 4 type-length 5

\# 配 置 切 换 到 用 户 角 色 network-operator 时 使 用 的 super 密 码 为 明 文123456789ABGFTweuix@#$%!。
[Sysname] super password role network-operator simple 123456789ABGFTweuix@#$%!
\# 添加设备管理类本地用户 test。
[Sysname] local-user test class manage \# 配置本地用户的服务类型为 Telnet。
[Sysname-luser-manage-test] service-type telnet配置本地用户的最小密码长度为 个字符。
\# 24 [Sysname-luser-manage-test] password-control length 24 \# 配置本地用户的密码元素的最少组合类型为 4 种，至少要包含每种元素的个数为 5 个。
[Sysname-luser-manage-test] password-control composition type-number 4 type-length 5 \# 配置本地用户的密码老化时间为 20 天。
[Sysname-luser-manage-test] password-control aging 20 \# 以交互式方式配置本地用户密码。
[Sysname-luser-manage-test] password Password:
Confirm :
Updating user information. Please wait ... ...
[Sysname-luser-manage-test] quit

###### 3. 验证配置

\# 可通过如下命令查看全局密码管理的配置信息。
<Sysname> display password-control Global password control configurations:
Password control: Enabled(device management users)
Disabled (network access users)
Password aging: Enabled (30 days)
Password length: Enabled (16 characters)
Password composition: Enabled (4 types, 4 characters per type)
Password history: Enabled (max history record:4)
Early notice on password expiration: 7 days Maximum login attempts: 2 User authentication timeout: 600 seconds Action for exceeding login attempts: Lock Minimum interval between two updates: 36 hours User account idle time: 30 days Logins with aged password: 5 times in 60 days Password complexity: Enabled (username checking)
Enabled (repeated characters checking)
\# 可通过如下命令查看 super 密码管理的配置信息。
<Sysname> display password-control super Super password control configurations:
Password aging: Enabled (90 days)
Password length: Enabled (24 characters)
Password composition: Enabled (4 types, 5 characters per type)
可通过如下命令查看到本地用户密码管理的配置信息。
\#

<Sysname> display local-user user-name test class manage Total 1 local users matched.
Device management user test:
State: Active Service type: Telnet User group: system Bind attributes:
Authorization attributes:
Work directory: flash:
User role list: network-operator Password control configurations:
Password aging: 20 days Password length: 24 characters Password composition: 4 types, 5 characters per type

## 10-keychain配置

目 录简介

### 1 keychain

#### 1.1 keychain简介

是加密规则（key）的集合，用来为应用程序提供动态认证功能。keychain 在不中断业务keychain的前提下，通过定期更改用于认证的密钥和算法来提升网络数据传输的安全性。
keychain 支持绝对时间模式，该模式的 keychain 中，key 的生命周期是 UTC（Coordinated Universal Time，国际协调时间）绝对时间，不受系统的时区和夏令时的影响。
一个 keychain 中的不同 key 可配置各自的认证密钥、认证算法和生命周期。当系统时间处于 key的生命周期内时，应用程序可以利用它对发送和接收的报文进行校验。当 keychain 内各个 key 的生命周期具有连续性时，随着系统时间的推移，各个 能够依次生效，从而实现动态地更改应用key程序使用的认证算法和认证密钥。

#### 1.2 keychain配置限制和指导

配置 keychain 时需要注意以下几点：
同一个 内的各个 使用 指定的生命周期不可重叠，以确保在同
• keychain key send-lifetime一时刻，应用程序只使用一个 key 对发送的报文进行校验。
• 认证双方在同一时间内所使用的 key 的认证算法和认证密钥必须一致。

#### 1.3 配置keychain

进入系统视图。
(1)
system-view创建 keychain，并进入 视图。
(2) keychain keychain keychain-name mode absolute
(3) （可选）配置 TCP 认证。
配置 TCP 增强认证选项中的类型值。
(cid:123)
tcp-kind kind-value缺省情况下，TCP 增强认证选项中的类型值为 254。
配置 TCP 认证算法对应的算法 ID。
(cid:123)
tcp-algorithm-id { hmac-md5 | md5 } algorithm-id缺省情况下，MD5 认证算法的算法 ID 是 3，HMAC-MD5 认证算法的算法 ID 是 5。
使用 TCP 作为传输层协议的通信双方，类型值及相同的算法 ID 对应的认证算法必须一致。在与友商设备互通时，请检查类型值及算法 ID 的配置，确保两端一致。
(4) （可选）延长 key 在报文接收时的生命周期。
accept-tolerance { value | infinite }缺省情况下，没有为 keychain 中的 key 延长其在报文接收时的生命周期。

用户需要修改认证双方的校验信息时，可能会出现由于校验信息的不匹配导致的业务中断。
为了避免上述情况的发生，可使用该命令为应用协议提供不中断其业务的报文校验服务。
创建一个 key，并进入 视图。
(5) key key key-id配置 key。
(6)
配置 的认证算法。
key (cid:123)
authentication-algorithm { hmac-md5 | hmac-sha-256 | md5 }缺省情况下，未配置 key 的认证算法。
配置 key 的认证密钥。
(cid:123)
key-string { cipher | plain } string缺省情况下，未配置 key 的认证密钥。
配置用来校验发送报文时 key 的 UTC 模式的生命周期。
(cid:123)
send-lifetime utc start-time start-date { duration { duration-value | infinite } | to end-time end-date }缺省情况下，未配置用来校验发送报文时 key 的生命周期。
配置用来校验接收报文时 key 的 UTC 模式的生命周期。
(cid:123)
accept-lifetime utc start-time start-date { duration { duration-value | infinite } | to end-time end-date }缺省情况下，未配置用来校验接收报文时 的生命周期。
key（可选）将当前 指定为 的缺省发送 key。
key keychain (cid:123)
default-send-key同一个 keychain 中，只能将一个 key 指定为缺省的发送 key。

#### 1.4 keychain显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 keychain 的运行情况，通过查看显示信息验证配置的效果。
表1-1 keychain 显示和维护操作 命令显示keychain信息 display keychain [ name keychain-name [ key key-id ] ]

#### 1.5 keychain典型配置举例

##### 1.5.1 keychain基本功能配置举例

###### 1. 组网需求

和 之间建立 邻居，使用 认证方式对发送和接收的报文进行校验。
Switch A Switch B OSPF keychain具体要求为：Switch A 和 Switch B 的 keychain 中创建 key 1 和 key 2，key 1 的生命周期结束后，自动切换成 key 2 来对报文进行校验。

###### 2. 组网图

图1-1 keychain 配置组网图

###### 3. 配置步骤

(1) 配置 Switch A
\# 配置接口的 IP 地址（略）。
\# 配置 OSPF 基本功能。
<SwitchA> system-view
[SwitchA] ospf 1 router-id 1.1.1.1
[SwitchA-ospf-1] area 0
[SwitchA-ospf-1-area-0.0.0.0] network 192.1.1.0 0.0.0.255
[SwitchA-ospf-1-area-0.0.0.0] quit
[SwitchA-ospf-1] quit
\# 配置名称为 abc 的 keychain，并指定其工作于绝对时间模式。
[SwitchA] keychain abc mode absolute
\# 在 keychain abc 中创建 key 1 和 key 2，并配置其认证算法、认证密钥和生命周期。
[SwitchA-keychain-abc] key 1
[SwitchA-keychain-abc-key-1] authentication-algorithm md5
[SwitchA-keychain-abc-key-1] key-string plain 123456
[SwitchA-keychain-abc-key-1] send-lifetime utc 10:00:00 2015/02/06 to 11:00:00
2015/02/06
[SwitchA-keychain-abc-key-1] accept-lifetime utc 10:00:00 2015/02/06 to 11:00:00
2015/02/06
[SwitchA-keychain-abc-key-1] quit
[SwitchA-keychain-abc] key 2
[SwitchA-keychain-abc-key-2] authentication-algorithm hmac-md5
[SwitchA-keychain-abc-key-2] key-string plain pwd123
[SwitchA-keychain-abc-key-2] send-lifetime utc 11:00:00 2015/02/06 to 12:00:00
2015/02/06
[SwitchA-keychain-abc-key-2] accept-lifetime utc 11:00:00 2015/02/06 to 12:00:00
2015/02/06
[SwitchA-keychain-abc-key-2] quit
[SwitchA-keychain-abc] quit
配置接口 使用 验证模式。
\# Vlan-interface 100 keychain
[SwitchA] interface vlan-interface 100
[SwitchA-Vlan-interface100] ospf authentication-mode keychain abc
[SwitchA-Vlan-interface100] quit
(2) 配置 Switch B
\# 配置接口的 IP 地址（略）。
\# 配置 OSPF 基本功能。
[SwitchB] ospf 1 router-id 2.2.2.2

[SwitchB-ospf-1] area 0 [SwitchB-ospf-1-area-0.0.0.0] network 192.1.1.0 0.0.0.255 [SwitchB-ospf-1-area-0.0.0.0] quit [SwitchB-ospf-1] quit \# 配置名称为 abc 的 keychain，并指定其工作于绝对时间模式。
[SwitchB] keychain abc mode absolute在 中创建 和 key2，并配置其认证算法、认证密钥和生命周期。
\# keychain abc key 1 [SwitchB-keychain-abc] key 1 [SwitchB-keychain-abc-key-1] authentication-algorithm md5 [SwitchB-keychain-abc-key-1] key-string plain 123456 [SwitchB-keychain-abc-key-1] send-lifetime utc 10:00:00 2015/02/06 to 11:00:00 2015/02/06 [SwitchB-keychain-abc-key-1] accept-lifetime utc 10:00:00 2015/02/06 to 11:00:00 2015/02/06 [SwitchB-keychain-abc-key-1] quit [SwitchB-keychain-abc] key 2 [SwitchB-keychain-abc-key-2] authentication-algorithm hmac-md5 [SwitchB-keychain-abc-key-2] key-string plain pwd123 [SwitchB-keychain-abc-key-2] send-lifetime utc 11:00:00 2015/02/06 to 12:00:00 2015/02/06 [SwitchB-keychain-abc-key-2] accept-lifetime utc 11:00:00 2015/02/06 to 12:00:00 2015/02/06 [SwitchB-keychain-abc-key-2] quit [SwitchB-keychain-abc] quit \# 配置接口 Vlan-interface 100 使用 keychain 验证模式。
[SwitchB] interface vlan-interface 100 [SwitchB-Vlan-interface100] ospf authentication-mode keychain abc [SwitchB-Vlan-interface100] quit

###### 4. 验证配置

当系统时间处于 的 到 时，通过查看以下信息来确认
(1) 2015/02/06 10:00:00 11:00:00 keychain的运行状态。
\# 查看 Switch A 的 keychain 信息，发现 key 1 为有效 key。
[SwitchA] display keychain Keychain name : abc Mode : absolute Accept tolerance : 0 TCP kind value : 254 TCP algorithm value HMAC-MD5 : 5 MD5 : 3 Default send key ID : None Active send key ID : 1 Active accept key IDs: 1 Key ID : 1 Key string : $c$3$dYTC8QeOKJkwFwP2k/rWL+1p6uMTw3MqNg==

Algorithm : md5 Send lifetime : 10:00:00 2015/02/06 to 11:00:00 2015/02/06 Send status : Active Accept lifetime : 10:00:00 2015/02/06 to 11:00:00 2015/02/06 Accept status : Active Key ID : 2 Key string : $c$3$7TSPbUxoP1ytOqkdcJ3K3x0BnXEWl4mOEw== Algorithm : hmac-md5 Send lifetime : 11:00:00 2015/02/06 to 12:00:00 2015/02/06 Send status : Inactive Accept lifetime : 11:00:00 2015/02/06 to 12:00:00 2015/02/06 Accept status : Inactive \# 查看 Switch B 的 keychain 信息，发现 key 1 为有效 key。
[SwitchB]display keychain Keychain name : abc Mode : absolute Accept tolerance : 0 TCP kind value : 254 TCP algorithm value HMAC-MD5 : 5 MD5 : 3 Default send key ID : None Active send key ID : 1 Active accept key IDs: 1 Key ID : 1 Key string : $c$3$/G/Shnh6heXWprlSQy/XDmftHa2JZJBSgg== Algorithm : md5 Send lifetime : 10:00:00 2015/02/06 to 11:00:00 2015/02/06 Send status : Active Accept lifetime : 10:00:00 2015/02/06 to 11:00:00 2015/02/06 Accept status : Active Key ID : 2 Key string : $c$3$t4qHAw1hpZYN0JKIEpXPcMFMVT81u0hiOw== Algorithm : hmac-md5 Send lifetime : 11:00:00 2015/02/06 to 12:00:00 2015/02/06 Send status : Inactive Accept lifetime : 11:00:00 2015/02/06 to 12:00:00 2015/02/06 Accept status : Inactive当系统时间处于 的 到 时，通过查看以下信息来确认
(2) 2015/02/06 11:00:00 12:00:00 keychain的运行状态。
\# 查看 Switch A 的 keychain 信息，发现 key 2 为有效 key。
[SwitchA]display keychain

Keychain name : abc Mode : absolute Accept tolerance : 0 TCP kind value : 254 TCP algorithm value HMAC-MD5 : 5 MD5 : 3 Default send key ID : None Active send key ID : 2 Active accept key IDs: 2 Key ID : 1 Key string : $c$3$dYTC8QeOKJkwFwP2k/rWL+1p6uMTw3MqNg== Algorithm : md5 Send lifetime : 10:00:00 2015/02/06 to 11:00:00 2015/02/06 Send status : Inactive Accept lifetime : 10:00:00 2015/02/06 to 11:00:00 2015/02/06 Accept status : Inactive Key ID : 2 Key string : $c$3$7TSPbUxoP1ytOqkdcJ3K3x0BnXEWl4mOEw== Algorithm : hmac-md5 Send lifetime : 11:00:00 2015/02/06 to 12:00:00 2015/02/06 Send status : Active Accept lifetime : 11:00:00 2015/02/06 to 12:00:00 2015/02/06 Accept status : Active \# 查看 Switch B 的 keychain 信息，发现 key 2 为有效 key。
[SwitchB]display keychain Keychain name : abc Mode : absolute Accept tolerance : 0 TCP kind value : 254 TCP algorithm value HMAC-MD5 : 5 MD5 : 3 Default send key ID : None Active send key ID : 1 Active accept key IDs: 1 Key ID : 1 Key string : $c$3$/G/Shnh6heXWprlSQy/XDmftHa2JZJBSgg== Algorithm : md5 Send lifetime : 10:00:00 2015/02/06 to 11:00:00 2015/02/06 Send status : Inactive Accept lifetime : 10:00:00 2015/02/06 to 11:00:00 2015/02/06 Accept status : Inactive

Key ID : 2 Key string : $c$3$t4qHAw1hpZYN0JKIEpXPcMFMVT81u0hiOw== Algorithm : hmac-md5 Send lifetime : 11:00:00 2015/02/06 to 12:00:00 2015/02/06 Send status : Active Accept lifetime : 11:00:00 2015/02/06 to 12:00:00 2015/02/06 Accept status : Active

## 11-公钥管理配置

目 录简介功能简介功能简介手工配置远端主机的公钥手工配置远端主机的公钥

### 1 公钥管理

#### 1.1 简介

1公钥管理简介
1.1公钥管理用于非对称密钥算法的密钥管理与发布。

##### 1.1.1 非对称密钥算法原理

非对称密钥算法是数据加解密的一种方法，用来保证数据在网络中安全传输、不被攻击者非法窃听和恶意篡改。如 图 1-1 所示，在非对称密钥算法中，加密和解密使用的密钥一个是对外公开的公钥，一个是由用户秘密保存的私钥，从公钥很难推算出私钥。公钥和私钥一一对应，二者统称为非对称密钥对。通过公钥（或私钥）加密后的数据只能利用对应的私钥（或公钥）进行解密。对称密钥算法中，加密和解密使用相同的密钥。
图1-1 加密和解密转换关系示意图密钥 密钥发送方 接收方明文 密文 明文非对称密钥算法包括 RSA（Rivest Shamir and Adleman）、DSA（Digital Signature Algorithm，数字签名算法）和 ECDSA（Elliptic Curve Digital Signature Algorithm，椭圆曲线数字签名算法）等。

##### 1.1.2 非对称密钥算法作用

非对称密钥算法主要有两个用途：
对发送的数据进行加/解密：发送者利用接收者的公钥对数据进行加密，只有拥有对应私钥的
•接收者才能使用该私钥对数据进行解密，从而可以保证数据的机密性。目前，只有 RSA 算法可以用来对发送的数据进行加/解密。
• 对数据发送者的身份进行认证：非对称密钥算法的这种应用，称为数字签名。发送者利用自己的私钥对数据进行加密，接收者利用发送者的公钥对数据进行解密，从而实现对数据发送者身份的验证。由于只能利用对应的公钥对通过私钥加密后的数据进行解密，因此根据解密是否成功，就可以判断发送者的身份是否合法，如同发送者对数据进行了“签名”。目前，RSA、DSA 和 ECDSA 都可以用于数字签名。
非对称密钥算法应用十分广泛，例如 SSH（Secure Shell，安全外壳）、SSL（Secure Sockets Layer，安全套接字层）、PKI（Public Infrastructure，公钥基础设施）中都利用了非对称密钥算法进行Key数字签名。非对称密钥算法只有与具体的应用（如 SSH、SSL）配合使用，才能实现利用非对称密钥算法进行加 / 解密或数字签名。 SSH 、 SSL 和 PKI 的介绍，请参见“安全配置指导”中的“ SSH ”、“SSL”和“PKI”。

#### 1.2 FIPS相关说明

设备运行于 FIPS 模式时，本特性部分配置相对于非 FIPS 模式有所变化，具体差异请见本文相关描述。有关 FIPS 模式的详细介绍请参见“安全配置指导”中的“FIPS”。

#### 1.3 公钥管理配置任务简介

公钥管理配置任务如下：
(1) 生成本地非对称密钥对
(2) 将本地非对称密钥中的主机公钥分发到远端主机请选择以下一项进行配置：
导出本地非对称密钥对中的主机公钥(cid:123)
显示本地非对称密钥对中的公钥信息(cid:123)
为了实现远端主机对本地设备的身份验证，用户需要将本地的主机公钥保存到远端主机上。
配置远端主机的公钥
(3)
请选择以下一项进行配置：
导入远端主机的公钥(cid:123)
手工配置远端主机的公钥(cid:123)
为了实现本地设备对远端主机的身份验证，用户需要在本地设备上配置远端主机公钥。
(4) （可选）销毁本地非对称密钥对

#### 1.4 生成本地非对称密钥对

##### 1. 配置限制和指导

创建RSA和DSA密钥对时，设备会提示用户输入密钥模数的长度。密钥模数越长，安全性越好，但是生成密钥的时间越长。创建ECDSA密钥对时，可使用不同密钥长度的椭圆曲线，密钥越长，安全性越好，但是生成密钥的时间越长。关于密钥模数长度或密钥长度的配置限制和注意事项请参见表 1-1。
生成密钥对时，如果不指定密钥对名称，系统会以缺省名称命名密钥对，并把该密钥对标记为默认（ default ）。
用户可以使用缺省的密钥对名称创建其他密钥对，但系统不会把该密钥对标记为默认（default）。
非默认名称密钥对的密钥类型和名称不能完全相同，否则需要用户确认是否覆盖原有的密钥对。不同类型的密钥对，名称可以相同。
执行 public-key local create 命令后，生成的密钥对将保存在设备中，设备重启后密钥不会丢失。

表1-1 不同类型密钥对对比

|  | 密钥对类型 |  |  | 生成的密钥对 |  |  | 密钥模数长度/密钥长度 |  |
|---|---|---|---|---|---|---|---|---|
|  |  |  | • 非 FIPS 模式下：不指定密钥对名称时，将同时生 (cid:123) 成两个密钥对服务器密钥对和主机密钥对指定密钥对名称时，只生成一个 (cid:123) 主机密钥对 • FIPS 模式下：只生成一个主机密钥对，包括一个公钥和一个私钥目前，只有 SSH1.5 中应用了 RSA 服务器密钥对 |  |  |  |  |  |
|  |  |  | 只生成一个主机密钥对 |  |  |  |  |  |
|  |  |  | 只生成一个主机密钥对 |  |  |  |  |  |

##### 2. 配置步骤

进入系统视图。
(1)
system-view生成本地非对称密钥对。
(2)
（非 模式）
FIPS public-key local create { dsa | ecdsa [ secp192r1 | secp256r1 | secp384r1 | secp521r1 ] | rsa } [ name key-name ]（FIPS 模式）
public-key local create { dsa | ecdsa [ secp256r1 | secp384r1 | secp521r1 ] | rsa } [ name key-name ]

#### 1.5 将本地非对称密钥中的主机公钥分发到远端主机

##### 1.5.1 功能简介

在某些应用（如 SSH）中，为了实现远端主机采用数字签名方法对本地设备进行身份验证，用户需要将本地的主机公钥保存到远端主机上。
将本地的主机公钥保存到远端主机上，有以下三种方法：

在本地设备上执行 public-key local export 命令按照指定格式将本地主机公钥导出到
•指定文件（执行命令时指定 参数），并将该文件上传到远端主机上。在远端主机上，filename通过从公钥文件中导入的方式将本地的主机公钥保存到远端设备上。
• 在本地设备上执行 public-key local export 命令按照指定格式将本地主机公钥导出到用户界面（执行命令时不指定 filename 参数），通过拷贝粘贴等方式将用户界面上的主机公钥保存到文件中，并将该文件上传到远端主机上。在远端主机上，通过从公钥文件中导入的方式将本地的主机公钥保存到远端设备上。
• 在本地设备上执行 display public-key local public 命令显示非对称密钥对中的公钥信息，并记录主机公钥数据。在远端主机上，通过手工配置的方式将记录的本地主机公钥保存到远端设备上。

##### 1.5.2 导出本地非对称密钥对中的主机公钥

(1) 进入系统视图。
system-view
导出本地非对称密钥对中的主机公钥。
(2)
按照指定格式将本地 主机公钥导出到指定文件或用户界面。
RSA
(cid:123)
（非 模式）
FIPS
public-key local export rsa [ name key-name ] { openssh | ssh1 | ssh2 }
[ filename ]
（FIPS 模式）
public-key local export rsa [ name key-name ] { openssh | ssh2 }
[ filename ]
按照指定格式将本地 ECDSA 主机公钥导出到指定文件或用户界面。
(cid:123)
public-key local export ecdsa [ name key-name ] { openssh | ssh2 }
[ filename ]
按照指定格式将本地 DSA 主机公钥导出到指定文件或用户界面。
(cid:123)
public-key local export dsa [ name key-name ] { openssh | ssh2 }
[ filename ]

##### 1.5.3 显示本地非对称密钥对中的公钥信息

请在任意视图下执行以下命令。
• 显示本地 RSA 密钥对中的公钥信息。
display public-key local rsa public [ name key-name ]若执行本命令时，同时显示了 服务器密钥对和主机密钥对的公钥信息，用户只需记录主RSA机密钥对的公钥信息。
• 显示本地 ECDSA 密钥对中的公钥信息。
display public-key local ecdsa public [ name key-name ]
• 显示本地 DSA 密钥对中的公钥信息。
display public-key local dsa public [ name key-name ]

###### 2. 配置步骤

#### 1.6 配置远端主机的公钥

##### 1.6.1 功能简介

在某些应用（如 SSH）中，为了实现本地设备对远端主机的身份验证，需要在本地设备上配置远端主机的 RSA、ECDSA、DSA 主机公钥。用户可以使用以下方法配置远端主机公钥：
导入远端主机公钥。
•
• 手工配置远端主机公钥。
远端主机公钥信息的获取方法，请参见“1.5 将本地非对称密钥中的主机公钥分发到远端主机”。

##### 1.6.2 配置限制和指导

手工配置远端主机的公钥时，输入的主机公钥必须满足一定的格式要求。通过display public-key local public 命令显示的公钥可以作为输入的公钥内容；通过其他方式（如public-key local export 命令）显示的公钥可能不满足格式要求，导致主机公钥保存失败。
因此，建议选用从公钥文件导入的方式配置远端主机的公钥。

##### 1.6.3 导入远端主机的公钥

###### 1. 功能简介

用户事先将远端主机的公钥文件保存到本地设备（例如，通过 或 TFTP，以二进制方式将远端FTP主机的公钥文件保存到本地设备），本地设备从该公钥文件中导入远端主机的公钥。导入公钥时，系统会自动将远端主机的公钥文件转换为 PKCS（Public Key Cryptography Standards，公共密钥加密标准）编码形式。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
从公钥文件中导入远端主机的公钥。
(2)
public-key peer keyname import sshkey filename

##### 1.6.4 手工配置远端主机的公钥

###### 1. 功能简介

用户事先在远端主机上通过 命令查看其公钥信息，并记display public-key local public录远端主机公钥的内容。在本地设备上采用手工输入的方式将远端主机的公钥配置到本地。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 指定远端主机公钥的名称，并进入公钥视图。
public-key peer keyname
(3) 手工输入远端主机的公钥。
逐个字符输入或拷贝粘贴公钥内容。

###### 1. 组网需求

在输入公钥内容时，字符之间可以有空格，也可以按回车键继续输入数据。保存公钥数据时，将删除空格和回车符。
退出公钥视图时，保存配置的主机公钥。
(4)
peer-public-key end

#### 1.7 销毁本地非对称密钥对

##### 1. 功能简介

在如下几种情况下，建议用户销毁旧的非对称密钥对，并生成新的密钥对：
• 本地设备的私钥泄露。这种情况下，非法用户可能会冒充本地设备访问网络。
• 保存密钥对的存储设备出现故障，导致设备上没有公钥对应的私钥，无法再利用旧的非对称密钥对进行加/解密和数字签名。
• 本地证书到达有效期，需要删除对应的本地密钥对。本地证书的详细介绍，请参见“安全配置指导”中的“PKI”。

##### 2. 配置步骤

进入系统视图。
(1)
system-view销毁本地非对称密钥对。
(2)
public-key local destroy { dsa | ecdsa | rsa } [ name key-name ]

#### 1.8 公钥管理显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后公钥管理的信息，通过查看显示信息验证配置的效果。
表1-2 公钥管理显示和维护操作 命令display public-key local { dsa | ecdsa | rsa } public显示本地非对称密钥对中的公钥信息[ name key-name ] display public-key peer [ brief | name显示保存在本地的远端主机的公钥信息publickey-name ]

#### 1.9 公钥管理典型配置举例

##### 1.9.1 手工配置远端主机的公钥

组网需求
1.
如 图 1-2 所示，为了防止非法用户访问， Device B （本地设备）采用数字签名方法对访问它的 Device A（远端设备）进行身份验证。进行身份验证前，需要在Device B上配置Device A的公钥。
本例中要求：
Device B 采用的非对称密钥算法为 RSA 算法。
•

采用手工配置方式在 Device B 上配置 Device A 的主机公钥。
•

###### 2. 组网图

图1-2 手工配置远端主机的公钥组网图Device A Device B

###### 3. 配置步骤

(1) 配置 Device A
\# 在 Device A 上生成默认名称的本地 RSA 非对称密钥对，密钥模数的长度采用缺省值 1024
比特。
<DeviceA> system-view
[DeviceA] public-key local create rsa
The range of public key modulus is (512 ~ 4096).
If the key modulus is greater than 512, it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
...
Create the key pair successfully.
\# 显示生成的本地 RSA 密钥对的公钥信息。
[DeviceA] display public-key local rsa public
=============================================
Key name: hostkey (default)
Key type: RSA
Time when key pair created: 16:48:31 2011/05/12
Key code:
30819F300D06092A864886F70D010101050003818D0030818902818100DA3B90F59237347B
8D41B58F8143512880139EC9111BFD31EB84B6B7C7A1470027AC8F04A827B30C2CAF79242E
45FDFF51A9C7E917DB818D54CB7AEF538AB261557524A7441D288EC54A5D31EFAE4F681257
6D7796490AF87A8C78F4A7E31F0793D8BA06FB95D54EBB9F94EB1F2D561BF66EA27DFD4788
CB47440AF6BB25ACA50203010001
=============================================
Key name: serverkey (default)
Key type: RSA
Time when key pair created: 16:48:31 2011/05/12
Key code:
307C300D06092A864886F70D0101010500036B003068026100C9451A80F7F0A9BA1A90C7BC
1C02522D194A2B19F19A75D9EF02219068BD7FD90FCC2AF3634EEB9FA060478DD0A1A49ACE
E1362A4371549ECD85BA04DEE4D6BB8BE53B6AED7F1401EE88733CA3C4CED391BAE633028A
AC41C80A15953FB22AA30203010001

(2) 配置 Device B
\# 在 Device B 上配置 Device A 的主机公钥：在公钥视图输入 Device A 的主机公钥，即在
上通过 命令显示的主机公钥
Device A display public-key local rsa public hostkey
内容。
<DeviceB> system-view
[DeviceB] public-key peer devicea
Enter public key view. Return to system view with "peer-public-key end" command.
[DeviceB-pkey-public-key-devicea]30819F300D06092A864886F70D010101050003818D00308189
2818100DA3B90F59237347B
[DeviceB-pkey-public-key-devicea]8D41B58F8143512880139EC9111BFD31EB84B6B7C7A1470027
A
C8F04A827B30C2CAF79242E
[DeviceB-pkey-public-key-devicea]45FDFF51A9C7E917DB818D54CB7AEF538AB261557524A7441D
88EC54A5D31EFAE4F681257
[DeviceB-pkey-public-key-devicea]6D7796490AF87A8C78F4A7E31F0793D8BA06FB95D54EBB9F94
E
B1F2D561BF66EA27DFD4788
[DeviceB-pkey-public-key-devicea]CB47440AF6BB25ACA50203010001
\# 从公钥视图退回到系统视图，并保存用户输入的公钥。
[DeviceB-pkey-public-key-devicea] peer-public-key end

###### 4. 验证配置

\# 显示 Device B 上保存的 Device A 的主机公钥信息。
[DeviceB] display public-key peer name devicea ============================================= Key name: devicea Key type: RSA Key modulus: 1024 Key code:
30819F300D06092A864886F70D010101050003818D0030818902818100DA3B90F59237347B 8D41B58F8143512880139EC9111BFD31EB84B6B7C7A1470027AC8F04A827B30C2CAF79242E 45FDFF51A9C7E917DB818D54CB7AEF538AB261557524A7441D288EC54A5D31EFAE4F681257 6D7796490AF87A8C78F4A7E31F0793D8BA06FB95D54EBB9F94EB1F2D561BF66EA27DFD4788 CB47440AF6BB25ACA50203010001通过对比可以看出，Device B 上保存的 Device A 的主机公钥信息与 Device A 实际的主机公钥信息一致。

##### 1.9.2 从公钥文件中导入远端主机的公钥

###### 1. 组网需求

如 图 1-3 所示，为了防止非法用户访问，Device B（本地设备）采用数字签名方法对访问它的Device A（远端设备）进行身份验证。进行身份验证前，需要在Device B上配置Device A的公钥。
本例中要求：

Device B 采用的非对称密钥算法为 RSA 算法。
•采用从公钥文件中导入的方式在 Device B 上配置 Device A 的主机公钥。
•

###### 2. 组网图

图1-3 从公钥文件中导入远端主机的公钥组网图

###### 3. 配置步骤

(1) 在 Device A 上生成密钥对，并导出公钥
\# 在 Device A 上生成默认名称的本地 RSA 非对称密钥对，密钥模数的长度采用缺省值 1024
比特。
<DeviceA> system-view
[DeviceA] public-key local create rsa
The range of public key modulus is (512 ~ 4096).
If the key modulus is greater than 512, it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
...
Create the key pair successfully.
\# 显示生成的本地 RSA 密钥对的公钥信息。
[DeviceA] display public-key local rsa public
=============================================
Key name: hostkey (default)
Key type: RSA
Time when key pair created: 16:48:31 2011/05/12
Key code:
30819F300D06092A864886F70D010101050003818D0030818902818100DA3B90F59237347B
8D41B58F8143512880139EC9111BFD31EB84B6B7C7A1470027AC8F04A827B30C2CAF79242E
45FDFF51A9C7E917DB818D54CB7AEF538AB261557524A7441D288EC54A5D31EFAE4F681257
6D7796490AF87A8C78F4A7E31F0793D8BA06FB95D54EBB9F94EB1F2D561BF66EA27DFD4788
CB47440AF6BB25ACA50203010001
=============================================
Key name: serverkey (default)
Key type: RSA
Time when key pair created: 16:48:31 2011/05/12
Key code:
307C300D06092A864886F70D0101010500036B003068026100C9451A80F7F0A9BA1A90C7BC
1C02522D194A2B19F19A75D9EF02219068BD7FD90FCC2AF3634EEB9FA060478DD0A1A49ACE
E1362A4371549ECD85BA04DEE4D6BB8BE53B6AED7F1401EE88733CA3C4CED391BAE633028A

AC41C80A15953FB22AA30203010001 \# 将生成的默认名称的 RSA 主机公钥导出到指定文件 devicea.pub 中。
[DeviceA] public-key local export rsa ssh2 devicea.pub在 上启动 服务器功能
(2) Device A FTP启动 服务器功能，创建 用户（用户名为 ftp，密码为 123），并配置 用户的\# FTP FTP FTP用户角色为 network-admin。
[DeviceA] ftp server enable [DeviceA] local-user ftp [DeviceA-luser-manage-ftp] password simple 123 [DeviceA-luser-manage-ftp] service-type ftp [DeviceA-luser-manage-ftp] authorization-attribute user-role network-admin [DeviceA-luser-manage-ftp] quit
(3) Device B 获取 Device A 的公钥文件\# Device B 通过 FTP 以二进制方式从 Device A 获取公钥文件 devicea.pub。
<DeviceB> ftp 10.1.1.1 Connected to 10.1.1.1 (10.1.1.1).
220 FTP service ready.
User (10.1.1.1:(none)): ftp 331 Password required for ftp.
Password:
230 User logged in.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> binary 200 TYPE is now 8-bit binary ftp> get devicea.pub 227 Entering Passive Mode (10,1,1,1,118,252)
150 Accepted data connection 226 File successfully transferred 301 bytes received in 0.003 seconds (98.0 kbyte/s)
ftp> quit 221-Goodbye. You uploaded 0 and downloaded 1 kbytes.
221 Logout.
(4) Device B 从公钥文件中导入公钥\# Device B 从公钥文件中导入 Device A 的主机公钥。
<DeviceB> system-view [DeviceB] public-key peer devicea import sshkey devicea.pub

###### 4. 验证配置

\# 显示 Device B 上保存的 Device A 的主机公钥信息。
[DeviceB] display public-key peer name devicea ============================================= Key name: devicea Key type: RSA Key modulus: 1024 Key code:

30819F300D06092A864886F70D010101050003818D0030818902818100DA3B90F59237347B 8D41B58F8143512880139EC9111BFD31EB84B6B7C7A1470027AC8F04A827B30C2CAF79242E 45FDFF51A9C7E917DB818D54CB7AEF538AB261557524A7441D288EC54A5D31EFAE4F681257 6D7796490AF87A8C78F4A7E31F0793D8BA06FB95D54EBB9F94EB1F2D561BF66EA27DFD4788 CB47440AF6BB25ACA50203010001通过对比可以看出，Device B 上保存的 Device A 的主机公钥信息与 Device A 实际的主机公钥信息一致。

## 12-PKI配置

目 录简介配置 实体创建 域配置证书申请的注册受理机构配置验证 根证书时使用的指纹指定 操作产生的协议报文使用的源 地址配置限制和指导手工在线申请本地证书

配置证书验证关闭 检查的证书验证配置证书访问控制策略PKI典型配置举例常见配置错误举例导出证书失败

### 1 PKI

###### 3. CRL（Certificate Revocation List，证书吊销列表）

1 PKI

#### 1.1 PKI简介

PKI（Public Infrastructure，公钥基础设施）是一个利用公钥理论和技术来实现并提供信息安Key全服务的具有通用性的安全基础设施。
PKI 系统以数字证书的形式分发和使用公钥。数字证书是用户的身份和用户所持有的公钥的结合。
基于数字证书的 PKI 系统，能够为网络通信和网络交易（例如电子政务和电子商务）提供各种安全服务。有关公钥的详细介绍请参见“安全配置指导”中的“公钥管理”。

##### 1.1.1 相关术语

###### 1. 数字证书

数字证书是经 CA（Certificate Authority，证书颁发机构）签名的、包含公钥及相关的用户身份信息的文件，它建立了用户身份信息与用户公钥的关联。CA 对数字证书的签名保证了证书是可信任的。
数字证书的格式遵循 ITU-T X.509 国际标准，目前最常用的为 X.509 V3 标准。数字证书中包含多个字段，包括证书签发者的名称、被签发者的名称（或者称为主题）、公钥信息、CA 对证书的数字签名、证书的有效期等。
本手册中涉及四类证书：CA 证书、RA（Registration Authority，证书注册机构）证书、本地证书和对端证书。
• CA 证书是 CA 持有的证书。若 PKI 系统中存在多个 CA，则会形成一个 CA 层次结构，最上层的 CA 是根 CA，它持有一个自签名的证书（即根 CA 对自己的证书签名），下一级 CA 证书分别由上一级 CA 签发。这样，从根 CA 开始逐级签发的证书就会形成多个可信任的链状结构，每一条路径称为一个证书链。
证书是 持有的证书，由 签发。RA 受 委托，可以为 分担部分管理工作。RA
• RA RA CA CA CA在 PKI 系统中是可选的。
• 本地证书是本设备持有的证书，由 CA 签发。
• 对端证书是其它设备持有的证书，由 CA 签发。

###### 2. CA根证书的指纹

CA 根证书的指纹，即根证书内容的散列值，该值对于每一个证书都是唯一的。
CRL（Certificate List，证书吊销列表）
3. Revocation由于用户名称的改变、私钥泄漏或业务中止等原因，需要存在一种方法将现行的证书吊销，即废除公钥及相关的用户身份信息的绑定关系。在 中，可以通过发布 的方式来公开证书的吊销PKI CRL信息。当一个或若干个证书被吊销以后，CA 签发 CRL 来声明这些证书是无效的，CRL 中会列出所有被吊销的证书的序列号。因此，CRL 提供了一种检验证书有效性的方式。

###### 4. CA策略

CA 策略是指 CA 在受理证书请求、颁发证书、吊销证书和发布 CRL 时所采用的一套标准。通常，以一种叫做 CPS（Certification Statement，证书惯例声明）的文档发布其策略。CA CA Practice

策略可以通过带外（如电话、磁盘、电子邮件等）或其它方式获取。由于不同的 CA 使用不同的策略，所以在选择信任的 进行证书申请之前，必须理解 策略。
CA CA

##### 1.1.2 体系结构

一个PKI体系由终端PKI实体、CA、RA和证书/CRL发布点四类实体共同组成，如下 图 1-1。
图1-1 PKI 体系结构图

###### 2. 终端PKI实体

终端 PKI 实体是 PKI 服务的最终使用者，可以是个人、组织、设备（如路由器、交换机）或计算机中运行的进程，后文简称为 实体。
PKI

###### 3. CA（Certificate Authority，证书颁发机构）

CA 是一个用于签发并管理数字证书的可信 PKI 实体。其作用包括：签发证书、规定证书的有效期和发布 CRL。

###### 4. RA（Registration Authority，证书注册机构）

RA 是一个受 CA 委托来完成 PKI 实体注册的机构，它接收用户的注册申请，审查用户的申请资格，并决定是否同意 CA 给其签发数字证书，用于减轻 CA 的负担。建议在部署 PKI 系统时，RA 与 CA安装在不同的设备上，减少 CA 与外界的直接交互，以保护 CA 的私钥。

###### 5. 证书/CRL发布点

证书/CRL 发布点用于对用户证书和 CRL 进行存储和管理，并提供查询功能。通常，证书/CRL 发布点位于一个目录服务器上，该服务器可以采用 LDAP（Lightweight Protocol，Directory Access轻量级目录访问协议）协议、HTTP 等协议工作。其中，较为常用的是 LDAP 协议，它提供了一种访问发布点的方式。LDAP 服务器负责将 CA/RA 服务器传输过来的数字证书或 CRL 进行存储，并提供目录浏览服务。用户通过访问 LDAP 服务器获取自己和其他用户的数字证书或者 CRL。

##### 1.1.3 数字证书的申请、使用和维护

下面是一个 PKI 实体申请、使用和维护本地证书的典型工作过程，其中由 RA 来完成 PKI 实体的注册：
(1) PKI 实体生成密钥对。

###### 3. Web安全

(2) PKI 实体向 RA 提出证书申请；
(3) RA 审核 PKI 实体身份，将 PKI 实体身份信息和公钥以数字签名的方式发送给 CA；
(4) CA 验证数字签名，同意 PKI 实体的申请，并颁发证书；
(5) RA 接收 CA 返回的证书，将其发布到 LDAP 服务器（或其它形式的发布点）上以提供目录浏
览服务，并通知 实体证书发布成功；
PKI
实体通过 SCEP（Simple Protocol，简单证书注册协议）从 处
(6) PKI Certificate Enrollment RA
获取证书，利用该证书可以与其它 PKI 实体使用加密、数字签名进行安全通信。
(7) 两个 PKI 实体互相发送自己的本地证书给对端以互相验证对端身份的合法性。
若两个 实体均验证对端证书为合法，则两端互相信任，可以建立数据连接；否则，两端
(8) PKI
互不信任，不能建立数据连接。
(9) 当用户的私钥泄漏或证书即将到期时，可删除本地证书再重新申请新的证书。

##### 1.1.4 主要应用

PKI 技术能满足人们对网络交易安全保障的需求。PKI 的应用范围非常广泛，并且在不断发展之中，下面给出几个应用实例。

###### 1. VPN（Virtual Private Network，虚拟专用网络）

VPN 是一种构建在公用通信基础设施上的专用数据通信网络，它可以利用网络层安全协议（如 IPsec）
和建立在 PKI 上的加密与数字签名技术来获得完整性保护。

###### 2. 安全电子邮件

电子邮件的安全也要求机密性、完整性、数据源认证和不可抵赖。目前发展很快的安全电子邮件协议 S/MIME（Secure/Multipurpose Extensions，安全/多用途 邮件扩充协议)，Internet Mail Internet是一个允许发送加密和有签名邮件的协议。该协议的实现需要依赖于 PKI 技术。
Web安全
3.
为了透明地解决 Web 的安全问题，在浏览器和服务器之间进行通信之前，先要建立 SSL 连接。SSL协议允许在浏览器和服务器之间进行加密通信，并且利用 技术对服务器和浏览器端进行身份验PKI证。
目前，H3C 的 PKI 特性可为安全协议 IPsec（IP Security，IP 安全）、SSL（Secure Sockets Layer，安全套接字层）提供证书管理机制。

#### 1.2 FIPS相关说明

设备运行于 FIPS 模式时，本特性部分配置相对于非 FIPS 模式有所变化，具体差异请见本文相关描述。有关 FIPS 模式的详细介绍请参见“安全配置指导”中的“FIPS”。

#### 1.3 PKI配置任务简介

PKI 配置任务如下：
(1) 配置PKI实体
(2) 配置PKI域（可选）配置证书和CRL的存储路径
(3)

(4) 申请本地证书
请至少选择以下一项任务进行配置。
自动在线申请本地证书
(cid:123)
手工在线申请本地证书
(cid:123)
离线申请本地证书
(cid:123)
(5) （可选）停止证书申请过程
(6) （可选）手工获取证书
将 CA 签发的与 PKI 实体所在 PKI 域有关的证书保存到本地，以提高证书的查询效率，减少
向 PKI 证书发布点查询的次数。
(7) （可选）配置证书验证
(8) （可选）导出证书
(9) （可选）删除证书
(10) （可选）配置证书访问控制策略
通过配置证书访问控制策略，对用户访问权限进行控制，保证服务器端的安全性。

#### 1.4 配置PKI实体

##### 1. PKI实体简介

实体的参数是 实体的身份信息，CA 根据 实体提供的身份信息来唯一标识证书申请者。
PKI PKI PKI一个有效的 PKI 实体参数中必须至少包括以下参数之一：
DN（Distinguished Name，识别名），包含以下参数：
•实体通用名。对于 DN 参数，实体的通用名必须配置。
(cid:123)
实体所属国家代码，用标准的两字符代码表示。例如，“CN”是中国的合法国家代码，(cid:123)
“US”是美国的合法国家代码实体所在地理区域名称(cid:123)
实体所属组织名称(cid:123)
实体所属组织部门名称(cid:123)
实体所属州省(cid:123)
FQDN （ Fully Qualified Domain Name ，完全合格域名），是 PKI 实体在网络中的唯一标识
•
• IP 地址

##### 2. 配置限制和指导

实体的配置必须与 证书颁发策略相匹配，因此建议根据 证书颁发策略来配置 实体，PKI CA CA PKI如哪些 PKI 实体参数为必选配置，哪些为可选配置。申请者的身份信息必须符合 CA 证书颁发策略，否则证书申请可能会失败。
Windows 2000 CA 服务器的 SCEP 插件对证书申请的数据长度有一定的限制。PKI 实体配置项超过一定数据长度时， CA 将不会响应 PKI 实体的证书申请。这种情况下如果通过离线方式提交申请，服务器可以完成签发。其它 服务器（例如 服务器和 服务器）
Windows 2000 CA CA RSA OpenCA目前没有这种限制。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 创建一个 PKI 实体，并进入该 PKI 实体视图。
pki entity entity-name
(3) 配置 PKI 实体的通用名。
common-name common-name-sting
缺省情况下，未配置 PKI 实体的通用名。
配置 实体所属国家代码。
(4) PKI
country country-code-string
缺省情况下，未配置 实体所属国家代码。
PKI
配置 实体所在地理区域名称。
(5) PKI
locality locality-name
缺省情况下，未配置 PKI 实体所在地理区域名称。
(6) 配置 PKI 实体所属组织名称。
organization org-name
缺省情况下，未配置 PKI 实体所属组织名称。
(7) 配置 PKI 实体所属组织部门名称。
organization-unit org-unit-name
缺省情况下，未配置 PKI 实体所属组织部门名称。
(8) 配置 PKI 实体所属州或省的名称。
state state-name
缺省情况下，未配置 PKI 实体所属州或省的名称。
(9) 配置 PKI 实体的 FQDN。
fqdn fqdn-name-string
缺省情况下，未配置 PKI 实体的 FQDN。
(10) 配置 PKI 实体的 IP 地址。
ip { ip-address | interface interface-type interface-number }
缺省情况下，未配置 实体的 地址。
PKI IP

#### 1.5 配置PKI域

##### 1.5.1 功能简介

实体在进行 证书申请操作之前需要配置一些注册信息来配合完成申请的过程。这些信息的PKI PKI集合就是一个 PKI 域。
PKI 域是一个本地概念，创建 PKI 域的目的是便于其它应用（比如 IKE、SSL）引用 PKI 的配置。

###### 1. 功能简介

###### 2. 配置步骤

##### 1.5.2 PKI域配置任务简介

域配置任务如下：
PKI创建PKI域
(1)
配置设备信任的CA名称
(2)
(3) 指定用户申请证书的PKI实体名称
(4) 配置证书申请的注册受理机构
(5) 配置注册受理机构服务器的URL
(6) （可选）配置证书申请状态查询的周期和最大次数
(7) 指定LDAP服务器在如下情况下，此配置必选：
需要通过 LDAP 协议获取证书。
(cid:123)
需要通过 LDAP 协议获取 CRL 时，如果 CRL 的 URL 中未包含发布点地址信息。
(cid:123)
(8) 配置验证CA根证书时使用的指纹当证书申请方式为自动方式时，此配置必选。
(cid:123)
当证书申请方式为手工方式时，此配置可选，若不配置，需要用户自行验证根证书指纹。
(cid:123)
(9) 指定证书申请时使用的密钥对
(10) （可选）指定证书的扩展用途
(11) （可选）指定PKI操作产生的协议报文使用的源IP地址

##### 1.5.3 创建PKI域

(1) 进入系统视图。
system-view
(2) 创建一个 PKI 域，并进入 PKI 域视图。
pki domain domain-name

##### 1.5.4 配置设备信任的CA名称

功能简介
1.
获取本地证书之前，若当前的 PKI 域中没有 CA 证书，则需要首先获取 CA 证书。获取 CA 证书之前，必须配置信任的 名称。
CA如果在同一台服务器主机上配置了两个 CA，且它们的 URL 是相同的，则需要在 PKI 域中指定的信任的 CA 名称来区分它们。设备信任的 CA 的名称只是在获取 CA 证书时使用，申请本地证书时不会用到。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 PKI 域视图。
pki domain domain-name

(3) 配置设备信任的 CA 名称。
ca identifier name
缺省情况下，未配置信任的 CA 名称。

##### 1.5.5 指定用户申请证书的PKI实体名称

(1) 进入系统视图。
system-view
进入 域视图。
(2) PKI
pki domain domain-name
指定用于申请证书的 实体名称。
(3) PKI
certificate request entity entity-name
缺省情况下，未指定用于申请证书的 实体名称。
PKI

##### 1.5.6 配置证书申请的注册受理机构

(1) 进入系统视图。
system-view
(2) 进入 PKI 域视图。
pki domain domain-name
(3) 配置证书申请的注册受理机构。
certificate request from { ca | ra }
缺省情况下，未指定证书申请的注册受理机构。

##### 1.5.7 配置注册受理机构服务器的URL

(1) 进入系统视图。
system-view
(2) 进入 PKI 域视图。
pki domain domain-name
(3) 配置注册受理机构服务器的 URL。
certificate request url url-string [ vpn-instance vpn-instance-name ]
缺省情况下，未指定注册受理机构服务器的 URL。

##### 1.5.8 配置证书申请状态查询的周期和最大次数

(1) 进入系统视图。
system-view
(2) 进入 PKI 域视图。
pki domain domain-name
(3) 配置证书申请状态查询的周期和最大次数。
certificate request polling { count count | interval interval }

缺省情况下，证书申请查询间隔为 20 分钟，最多查询 50 次。

##### 1.5.9 指定LDAP服务器

(1) 进入系统视图。
system-view
(2) 进入 PKI 域视图。
pki domain domain-name
指定 服务器。
(3) LDAP
ldap-server host hostname [ port port-number ] [ vpn-instance
vpn-instance-name ]
缺省情况下，未指定 LDAP 服务器。

##### 1.5.10 配置验证CA根证书时使用的指纹

(1) 进入系统视图。
system-view
(2) 进入 PKI 域视图。
pki domain domain-name
(3) 配置验证 CA 根证书时使用的指纹。
（非 FIPS 模式）
root-certificate fingerprint { md5 | sha1 } string
（FIPS 模式）
root-certificate fingerprint sha1 string
缺省情况下，未指定验证根证书时使用的指纹。

##### 1.5.11 指定证书申请时使用的密钥对

###### 1. 配置限制和指导

申请证书前必须指定使用的密钥对，但该密钥对不必已经存在。申请过程中，如果指定的密钥对不存在， PKI 实体可以根据指定的名字、算法和密钥模数长度生成相应的密钥对。

###### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入 PKI 域视图。
pki domain domain-name
(3) 指定证书申请时使用的密钥对。请选择其中一项进行配置。
指定 RSA 密钥对。
(cid:123)
public-key rsa { { encryption name encryption-key-name [ length key-length ] | signature name signature-key-name [ length key-length ] }
* | general name key-name [ length key-length ] }

指定 ECDSA 密钥对。
(cid:123)
（非 FIPS 模式）
public-key ecdsa name key-name [ secp192r1 | secp256r1 | secp384r1 | secp521r1 ]（FIPS 模式）
public-key ecdsa name key-name [ secp256r1 | secp384r1 | secp521r1 ]指定 DSA 密钥对。
(cid:123)
public-key dsa name key-name [ length key-length ]缺省情况下，未指定所使用的密钥对。

##### 1.5.12 指定证书的扩展用途

###### 1. 功能简介

证书申请中会带有指定的证书扩展用途，但最终签发的证书中带有哪些扩展用途，由 CA 自己的策略决定，可能与 PKI 域中指定的配置不完全一致。应用程序（例如 IKE，SSL）认证过程中是否会使用这些用途，由应用程序的策略决定。
目前支持以下证书扩展用途：
• 证书扩展用途为 IKE，即 IKE 对等体使用的证书。
• 证书扩展用途为 SSL 客户端，即 SSL 客户端使用的证书。
• 证书扩展用途为 SSL 服务器端，即 SSL 服务器端使用的证书。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 PKI 域视图。
pki domain domain-name
(3) 指定证书的扩展用途。
usage { ike | ssl-client | ssl-server } *
缺省情况下，证书可用于所有用途。

##### 1.5.13 指定PKI操作产生的协议报文使用的源IP地址

###### 1. 功能简介

如果希望 PKI 实体操作产生的 PKI 协议报文的源 IP 地址是一个特定的地址，例如当 CA 服务器上的策略要求仅接受来自指定地址或网段的证书申请时，则需要通过配置指定该地址。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 PKI 域视图。
pki domain domain-name
(3) 指定 PKI 操作产生的协议报文使用的源 IP 地址。

##### 3. 配置步骤

（IPv4 网络）
source ip { ip-address | interface interface-type interface-number }（IPv6 网络）
source ipv6 { ipv6-address | interface interface-type interface-number }缺省情况下，PKI 操作产生的协议报文的源 地址为系统根据路由查找到的出接口的地址。
IP

#### 1.6 配置证书和CRL的存储路径

##### 1. 功能简介

获取到本地的证书和 CRL有默认存储路径，但同时也允许用户根据自己的需要修改证书文件和 CRL文件的存储路径。证书和 CRL 的存储路径可以指定为不同的路径。
修改了证书或 CRL 的存储目录后，原存储路径下的证书文件（以.cer 和.p12 为后缀的文件）和 CRL文件（以.crl 为后缀的文件）将被移动到新路径下保存。

##### 2. 配置限制和指导

重新配置了证书或 的存储路径后为了防止证书或 文件的丢失，重启或关闭设备前一定要CRL CRL保存配置。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 配置证书和 CRL 的存储路径。
pki storage { certificates | crls } dir-path缺省情况下，证书和 CRL 的存储路径为设备存储介质上的 PKI 目录。

#### 1.7 申请本地证书

##### 1.7.1 功能简介

申请证书的过程就是 PKI 实体向 CA 自我介绍的过程。PKI 实体向 CA 提供身份信息，以及相应的公钥，这些信息将成为颁发给该 PKI 实体证书的主要组成部分。
PKI 实体向 CA 提出证书申请，有离线和在线两种方式。
• 离线申请方式下，CA 允许申请方通过带外方式（如电话、磁盘、电子邮件等）向 CA 提供申请信息。
在线申请方式下，实体通过 SCEP 协议向 CA 提交申请信息。在线申请有自动申请和手工申
•请两种方式。下文将详细介绍这两种方式的具体配置。

##### 1.7.2 配置限制和指导

在线申请本地证书需要遵循以下配置限制和指导：
• 本地证书已存在的情况下，为保证密钥对与现存证书的一致性，不建议执行命令 public-key local create 或 public-key local destroy 创建或删除与现存证书使用的密钥对相

###### 3. 配置步骤

###### 1. 功能简介

同名称的密钥对，否则会导致现存证书不可用。有关公钥相关命令的详细介绍，请参见“安全命令参考”中的“公钥管理”。
若要重新申请本地证书，请先使用 命令删除本地证书，然后再
• pki delete-certificate执行 public-key local create 命令生成新的密钥对。
• 一个 PKI 域中，只能存在 DSA、ECDSA 或 RSA 中一种密钥算法类型的本地证书。采用 DSA和 ECDSA 算法时，一个 PKI 域中最多只能同时申请和存在一个本地证书；采用 RSA 算法时，一个 PKI 域中最多只能同时申请和存在一个用途为签名的 RSA 算法本地证书和一个用途为加密的 RSA 算法本地证书。

##### 1.7.3 配置准备

申请证书之前必须保证设备的系统时钟与 CA 的时钟同步，否则设备可能会错误地认为证书不在有效期内，导致申请证书失败。调整系统时钟的方法请参见“基础配置指导”中的“设备管理”。

##### 1.7.4 自动在线申请本地证书

###### 1. 功能简介

配置证书申请方式为自动方式后，当有应用协议与 联动时，如果应用协议中的 实体无本地PKI PKI证书（例如，IKE 协商采用数字签名方法进行身份认证，但在协商过程中没有发现本地证书），则PKI 实体自动通过 SCEP 协议向 CA 发起证书申请，并在申请成功后将本地证书获取到本地保存。
在证书申请之前，若当前的 PKI 域中没有 CA 证书，也会首先自动获取 CA 证书。

###### 2. 配置限制和指导

对于系统自动申请到的证书，当它们即将过期时或正式过期后，系统不会自动向 发起重新申请。
CA这种情况下，可能会由于证书过期造成应用协议的业务中断。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 进入 PKI 域视图。
pki domain domain-name
(3) 配置证书申请为自动方式。
certificate request mode auto [ password { cipher | simple } string ]缺省情况下，证书申请为手工方式。
证书申请为自动方式时，可以指定吊销证书时使用的密码，是否需要指定密码是由 CA 服务器的策略决定的。

##### 1.7.5 手工在线申请本地证书

功能简介
1.
配置证书申请方式为手工方式后，需要手工执行申请本地证书的操作。手工申请成功后，设备将把申请到的本地证书自动获取到本地保存。

###### 2. 配置步骤

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 PKI 域视图。
pki domain domain-name
(3) 配置证书申请为手工方式。
certificate request mode manual
缺省情况下，证书申请为手工方式。
退回系统视图。
(4)
quit
手工获取 证书。
(5) CA
请参见“1.9 手工获取证书”。
如果 域中不存在 证书，需要手工获取 证书。CA 证书用来验证获取到的本地证书
PKI CA CA
的真实性和合法性。
(6) 手工申请本地证书。
pki request-certificate domain domain-name [ password password ]
此命令不会被保存在配置文件中。
手工申请本地证书时，可以指定吊销证书时使用的密码，是否需要指定密码是由 服务器
CA
的策略决定的。

##### 1.7.6 离线申请本地证书

###### 1. 功能简介

当无法通过 SCEP 协议向 CA 在线申请证书时，可以采用此方式申请本地证书。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 PKI 域视图。
pki domain domain-name
(3) 配置证书申请为手工方式。
certificate request mode manual缺省情况下，证书申请为手工方式。
(4) 退回系统视图。
quit
(5) 手工获取 CA 证书。
请参见“ 手工获取证书”。
1.9如果 域中不存在 证书，需要手工获取 证书。CA 证书用来验证获取到的本地证书PKI CA CA的真实性和合法性。
(6) 手工申请本地证书或生成 PKCS#10 证书申请。

pki request-certificate domain domain-name pkcs10 [ filename filename ]此命令不会被保存在配置文件中。
(7) 通过带外方式将本地证书申请信息发送给 CA。
(8) 通过带外方式将本地证书获取到本地。
(9) 将本地证书导入指定的 PKI 域中。
pki import domain domain-name { der local filename filename | p12 local filename filename | pem local } [ filename filename ] }

#### 1.8 停止证书申请过程

##### 1. 功能简介

用户可以通过此配置停止正在进行中的证书申请过程。用户在证书申请时，可能由于某种原因需要改变证书申请的一些参数，比如通用名、国家代码、FQDN 等，而此时证书申请过程正在进行，为了新的申请不与之前的申请发生冲突，建议先停止之前的申请，再进行新的申请。可以通过 display命令查询正在进行中的证书申请过程。
pki certificate request-status另外，删除 域也可以停止对应的证书申请过程。
PKI

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 停止证书申请过程。
pki abort-certificate-request domain domain-name
此命令不会被保存在配置文件中。

#### 1.9 手工获取证书

##### 1. 功能简介

获取证书的目的是：将 CA 签发的与 PKI 实体所在 PKI 域有关的证书存放到本地，以提高证书的查询效率，减少向 PKI 证书发布点查询的次数。
用户通过此配置可以将已存在的 CA 证书、本地证书或者外部 PKI 实体证书获取至本地保存。获取证书有两种方式：离线导入方式和在线方式。
离线导入方式：通过带外方式（如 FTP、磁盘、电子邮件等）取得证书，然后将其导入至本
•地。如果设备所处的环境中没有证书的发布点、CA服务器不支持通过SCEP协议与设备交互、或者证书对应的密钥对由 CA 服务器生成，则可采用此方式获取证书。
• 在线方式：从证书发布服务器上在线获取证书并下载至本地，包括通过 SCEP 协议获取 CA证书和通过 LDAP 协议获取本地或对端证书。

##### 2. 配置限制和指导

如果本地已有 证书存在，则不允许执行在线方式获取 证书的操作。若想重新获取，请先使CA CA用 pki delete-certificate 命令删除 CA 证书与本地证书后，再执行获取 CA 证书的命令。

如果 PKI 域中已经有本地证书或对端证书，仍然允许执行在线方式获取本地证书或对端证书，获取到的证书直接覆盖已有证书。但对于 算法的证书而言，一个 域中可以存在一个签名用途RSA PKI的证书和一个加密用途的证书，不同用途的证书不会相互覆盖。
如果使能了 CRL 检查，手工获取证书时会触发 CRL 检查，如果 CRL 检查时发现待获取的证书已经吊销，则获取证书失败。
设备根据自身的系统时间来判断当前的证书是否还在其有效期内，设备系统时间不准确可能导致设备对于证书有效期的判断出现误差或错误，例如认为实际还在有效期内证书已过期，因此请确保设备系统时间的准确性。

##### 3. 配置准备

获取本地证书或对端证书之前必须完成以下操作：
• 在线获取本地证书和对端证书是通过 LDAP 协议进行的，因此在线获取本地证书或对端证书之前必须完成 PKI 域中指定 LDAP 服务器的配置。
• 离线导入证书之前，需要通过 FTP、TFTP 等协议将证书文件传送到设备的存储介质中。如果设备所处的环境不允许使用 FTP 、 TFTP 等协议，则可以直接采用在终端上粘贴证书内容的方式导入，但是粘贴的证书必须是 PEM（Privacy Enhanced Mail，增强保密邮件）格式的，因为只有 PEM 格式的证书内容为可打印字符。
• 只有存在签发本地证书的 CA 证书链才能成功导入本地证书，这里的 CA 证书链可以是保存在PKI 域中的，也可以是本地证书中携带的。若设备和本地证书中都没有 CA 证书链，则需要预先获取到 证书链。导入对端证书时，需要满足的条件与导入本地证书相同。
CA离线导入含有被加密的密钥对的本地证书时，需要输入加密口令。请提前联系 服务器管理
• CA员取得该口令。

##### 4. 配置步骤

(1) 进入系统视图。
system-view
(2) 手工获取证书。
离线导入方式
(cid:123)
pki import domain domain-name { der { ca | local | peer } filename
filename | p12 local filename filename | pem { ca | local | peer }
[ filename filename ] }
在线方式
(cid:123)
pki retrieve-certificate domain domain-name { ca | local | peer
entity-name }
pki retrieve-certificate 命令不会被保存在配置文件中。

#### 1.10 配置证书验证

##### 1.10.1 功能简介

在使用每一个证书之前，必须对证书进行验证。证书验证包括检查本地、CA 证书是否由可信的 CA签发，证书是否在有效期内，证书是否未被吊销。申请证书、获取证书以及应用程序使用 PKI 功能

时，都会自动对证书进行验证，因此一般不需要使用命令行手工进行证书验证。如果用户希望在没有任何前述操作的情况下单独执行证书的验证，可以手工执行证书验证。
配置证书验证时可以设置是否必须进行 检查。CRL 检查的目的是查看 实体的证书是否被CRL PKI CA 吊销，若检查结果表明 PKI 实体的证书已经被吊销，那么该证书就不再被其它 PKI 实体信任。
• 如果配置为开启 CRL 检查，则需要首先从 CRL 发布点获取 CRL。PKI 域中未配置 CRL 发布点的 URL 时，从该待验证的证书中获取发布点信息：优先获取待验证的证书中记录的发布点，如果待验证的证书中没有记录发布点，则获取 CA 证书中记录的发布点（若待验证的证书为CA 证书，则获取上一级 CA 证书中记录的发布点）。如果无法通过任何途径得到发布点，则通过 SCEP 协议获取 CRL。由于设备通过 SCEP 获取 CRL 是在获取到 CA 证书和本地证书之后进行，因此该方式下必须保证设备已经获取到 CA 证书和本地证书。开启了 CRL 检查的情况下，如果 域中不存在相应的 CRL、CRL 获取失败、或者 检查时发现待获取的证书PKI CRL已经吊销，则手动申请证书、获取证书的操作将会失败。
• 如果配置为关闭 CRL 检查，则不需要获取 CRL。

##### 1.10.2 配置限制和指导

验证一个 PKI 域中的 CA 证书时，系统会逐级验证本域 CA 证书链上的所有 CA 证书的有效性，因此需要保证设备上存在该 证书链上的所有上级 证书所属的 域。验证某一级 证书时，CA CA PKI CA系统会根据该 CA 证书的签发者名（IssuerName）查找对应的上一级 CA 证书，以及上一级 CA 证书所属的（一个或多个）PKI 域。若查找到了相应的 PKI 域，且该 PKI 域中开启了 CRL 检查，则根据该 PKI 域中的配置对待验证的 CA 证书进行吊销检查，否则不检查待验证的 CA 证书是否被吊销。检查 证书链中的 CA（根 除外）是否被吊销后，从根 逐级验证 证书链的签发关CA CA CA CA系。

##### 1.10.3 开启CRL检查的证书验证

(1) 进入系统视图。
system-view
(2) 进入 PKI 域视图。
pki domain domain-name
(3) （可选）配置 CRL 发布点的 URL。
crl url url-string [ vpn-instance vpn-instance-name ]
缺省情况下，未指定 CRL 发布点的 URL。
(4) 开启 CRL 检查。
crl check enable
缺省情况下，CRL 检查处于开启状态。
(5) 退回系统视图。
quit
(6) 获取 CA 证书。
请参见“1.9 手工获取证书”。
在进行本地证书验证操作之前必须首先获取 CA 证书。

##### 3. 配置步骤

(7) （可选）获取 CRL 并下载至本地。
pki retrieve-crl domain domain-name
验证非根 CA 证书和本地证书时，如果 PKI 域中没有 CRL，系统会自动获取 CRL 再进行验证；
如果 域已经存在 CRL，则可以继续获取 CRL，获取到的新 会覆盖已有 CRL。
PKI CRL
获取到的 不一定是本域 签发的，但肯定是本域 证书链上的一个 证书签发的。
CRL CA CA CA
验证证书的有效性。
(8)
pki validate-certificate domain domain-name { ca | local }

##### 1.10.4 关闭CRL检查的证书验证

(1) 进入系统视图。
system-view
(2) 进入 PKI 域视图。
pki domain domain-name
(3) 关闭 CRL 检查。
undo crl check enable
缺省情况下，CRL 检查处于开启状态。
退回系统视图。
(4)
quit
获取 证书。
(5) CA
请参见“1.9 手工获取证书”。
在进行本地证书验证操作之前必须首先获取 CA 证书。
(6) 验证证书的有效性。
pki validate-certificate domain domain-name { ca | local }
此命令不会被保存在配置文件中。

#### 1.11 导出证书

##### 1. 功能简介

域中已存在的 证书、本地证书可以导出到文件中保存或导出到终端上显示，导出的证书可PKI CA以用于证书备份或供其它设备使用。

##### 2. 配置限制和指导

以 PKCS12 格式导出所有证书时，PKI 域中必须有本地证书，否则会导出失败。
导出证书时若不指定文件名，则表示要将证书导出到终端上显示，这种方式仅 PEM 格式的证书才支持。
导出证书时若指定文件名，则表示证书将导出到指定文件中保存。导出 RSA 算法类型的本地证书时，设备上实际保存证书的证书文件名称并不一定是用户指定的名称，它与本地证书的密钥对用途相关，具体的命名规则请参见 PKI 命令手册。
配置步骤
3.
(1) 进入系统视图。

##### 1. 功能简介

system-view
(2) 导出证书。
导出 DER 格式的证书。
(cid:123)
pki export domain domain-name der { all | ca | local } filename filename导出 PKCS12 格式的证书。
(cid:123)
pki export domain domain-name p12 { all | local } passphrase p12-key filename filename导出 PEM 格式的证书。
(cid:123)
pki export domain domain-name pem { { all | local } [ { 3des-cbc | aes-128-cbc | aes-192-cbc | aes-256-cbc | des-cbc } pem-key ] | ca } [ filename filename ]

#### 1.12 删除证书

功能简介
1.
由 CA 颁发的证书都会设置有效期，证书生命周期的长短由签发证书的 CA 来确定。当用户的私钥被泄漏或证书的有效期快到时，应该重新申请新的证书。以下情况需要删除证书：
证书过期时，可以通过此配置删除已经存在的本地证书、CA 证书或对端证书。
•用户的私钥被泄漏或希望重新申请证书时，可以通过此配置删除已经存在的本地证书。
•

##### 2. 配置限制和指导

删除 CA 证书时将同时删除所在 PKI 域中的本地证书、所有对端证书以及 CRL。
重新申请证书之前，应该先使用命令 删除旧的密钥对，再使用public-key local destroy public-key local create 生成新的密钥对。相关命令的详细介绍可参考“安全命令参考”中的“公钥管理”。

##### 3. 配置步骤

进入系统视图。
(1)
system-view
(2) 删除证书。
pki delete-certificate domain domain - name { ca | local | peer [ serial serial-num ] }如果未指定序列号，则删除所有对端证书。

#### 1.13 配置证书访问控制策略

##### 1.13.1 功能简介

通过配置证书的访问控制策略，可以对安全应用中的用户访问权限进行进一步的控制，保证了与之通信的服务器端的安全性。例如，在 HTTPS（Hypertext Transfer Protocol Secure，超文本传输协议的安全版本）应用中，HTTPS 服务器可以通过引用证书访问控制策略，根据自身的安全需要对客户端的证书合法性进行检测。

###### 1. 证书访问控制规则和属性组

一个证书访问控制策略中可以定义多个证书属性的访问控制规则（通过 rule 命令配置），每一个访问控制规则都与一个证书属性组关联。一个证书属性组是一系列属性规则（通过 attribute 命令配置）的集合，这些属性规则是对证书的颁发者名、主题名以及备用主题名进行过滤的匹配条件。

###### 2. 证书访问控制策略规则的匹配原则

如果一个证书中的相应属性能够满足一条访问控制规则所关联的证书属性组中所有属性规则的要求，则认为该证书和该规则匹配。如果一个证书访问控制策略中有多个规则，则按照规则编号从小到大的顺序遍历所有规则，一旦证书与某一个规则匹配，则立即结束检测，不再继续匹配其它规则。
规则的匹配结果决定了证书的有效性，具体如下：
• 如果证书匹配到的规则中指定了 permit 关键字，则该证书将被认为通过了访问控制策略的检测且有效。
如果证书匹配到的规则中指定了 关键字，则该证书将被认为未通过访问控制策略的检测
• deny且无效。
• 若遍历完所有规则后，证书没有与任何规则匹配，则该证书将因不能通过访问控制策略的检测而被认为无效。
• 若证书访问控制策略下某访问控制规则关联的证书属性组不存在，或者该证书属性组没有配置任何属性，则认为被检测的证书都能够与此规则匹配。
• 若安全应用（如 HTTPS）引用的证书访问控制策略不存在，则认为该应用中被检测的证书有效。

##### 1.13.2 配置步骤

(1) 进入系统视图。
system-view
(2) 创建证书属性组，并进入证书属性组视图。
pki certificate attribute-group group-name
(3) 配置证书颁发者名、证书主题名及备用主题名的属性规则。
attribute id { alt-subject-name { fqdn | ip } | { issuer-name |
subject-name } { dn | fqdn | ip } } { ctn | equ | nctn | nequ} attribute-value
缺省情况下，对证书颁发者名、证书主题名及备用主题名没有限制。
(4) 退回系统视图。
quit
(5) 创建证书访问控制策略，并进入证书访问控制策略视图。
pki certificate access-control-policy policy-name
(6) 配置证书属性的访问控制规则。
rule [ id ] { deny | permit } group-name
缺省情况下，未配置证书属性的访问控制规则，认为所有证书都可以通过该控制策略的过
滤。
一个证书访问控制策略中可配置多个访问控制规则。

#### 1.14 PKI显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 PKI 的运行情况，通过查看显示信息验证配置的效果。
表1-1 PKI 显示和维护操作 命令display pki certificate access-control-policy显示证书访问控制策略的配置信息[ policy-name ] display pki certificate attribute-group显示证书属性组的配置信息[ group-name ] display pki certificate domain domain-name { ca |显示证书内容local | peer [ serial serial-num ] } display pki certificate request-status [ domain显示证书申请状态domain-name ]显示存储在本地的 display pki crl domain domain-name CRL

#### 1.15 PKI典型配置举例

• 当采用 Windows Server 作为 CA 时，需要安装 SCEP 插件。在这种情况下，配置 PKI 域时，
需要使用 certificate request from ra 命令指定 PKI 实体从 RA 注册申请证书。
• 当采用 RSA Keon 软件时，不需要安装 SCEP 插件。在这种情况下，配置 PKI 域时，需要使用
certificate request from ca 命令指定 PKI 实体从 CA 注册申请证书。
当采用 OpenCA 软件时，需要启用 SCEP 功能，在这种情况下，配置 PKI 域时，需要使用
•
命令指定 实体从 注册申请证书。
certificate requeset from ra PKI RA

##### 1.15.1 PKI实体向CA申请证书（采用RSA Keon CA服务器）

###### 1. 组网需求

配置 PKI 实体 Device 向 CA 服务器申请本地证书。

###### 2. 组网图

图1-2 实体向 申请证书组网图PKI CA

###### 3. 配置CA服务器

(1) 创建 CA 服务器 myca
在本例中，CA 服务器上首先需要进行基本属性 Nickname 和 Subject DN 的配置。其它属性
选择默认值。其中，Nickname 为可信任的 CA 名称（本例中为 myca），Subject DN 为 CA
的 属性，包括 CN、OU、O 和 C。
DN
配置扩展属性
(2)
基本属性配置完毕之后，还需要在生成的 CA 服务器管理页面上对“Jurisdiction
Configuration”进行配置，主要内容包括：根据需要选择合适的扩展选项；启动自动颁发证
书功能；添加可以自动颁发证书的地址范围。
以上配置完成之后，还需要保证设备的系统时钟与 CA 的时钟同步才可以正常使用设备来申
请证书和获取 CRL。

###### 4. 配置Device

配置 实体
(1) PKI \# 配置 PKI 实体名称为 aaa ，通用名为 Device 。
<Device> system-view [Device] pki entity aaa [Device-pki-entity-aaa] common-name Device [Device-pki-entity-aaa] quit
(2) 配置 PKI 域\# 创建并进入 PKI 域 torsa。
[Device] pki domain torsa配置设备信任的 的名称为 myca。
\# CA [Device-pki-domain-torsa] ca identifier myca \# 配置注册受理机构服务器的 URL，格式为 http://host:port/Issuing Jurisdiction ID。其中的为 服务器上生成的 进制字符串。
Issuing Jurisdiction ID CA 16 [Device-pki-domain-torsa] certificate request url http://1.1.2.22:446/80f6214aa8865301d07929ae481c7ceed99f95bd \# 配置证书申请的注册受理机构为 CA。
[Device-pki-domain-torsa] certificate request from ca \# 指定 PKI 实体名称为 aaa。
[Device-pki-domain-torsa] certificate request entity aaa \# 配置 CRL 发布点位置。
[Device-pki-domain-torsa] crl url ldap://1.1.2.22:389/CN=myca
(3) # 指定证书申请使用的密钥对，用途为通用，名称为 abc，密钥对长度为 1024 比特。
[Device-pki-domain-torsa] public-key rsa general name abc length 1024 [Device-pki-domain-torsa] quit
(4) 生成 RSA 算法的本地密钥对[Device] public-key local create rsa name abc The range of public key modulus is (512 ~ 4096).
If the key modulus is greater than 512,it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:

Generating Keys...
Create the key pair successfully.
(5) 证书申请\# 获取 CA 证书并下载至本地。
[Device] pki retrieve-certificate domain torsa ca The trusted CA's finger print is:
MD5 fingerprint:EDE9 0394 A273 B61A F1B3 0072 A0B1 F9AB SHA1 fingerprint: 77F9 A077 2FB8 088C 550B A33C 2410 D354 23B2 73A8 Is the finger print correct?(Y/N):y Retrieved the certificates successfully.
\# 手工申请本地证书。（采用 RSA Keon CA 服务器申请证书时，必须指定 password 参数）
[Device] pki request-certificate domain torsa password 1111 Start to request general certificate ...
……Certificate requested successfully.

###### 5. 验证配置

\# 通过以下显示命令可以查看申请到的本地证书信息。
[Device] display pki certificate domain torsa local Certificate:
Data:
Version: 3 (0x2)
Serial Number:
15:79:75:ec:d2:33:af:5e:46:35:83:bc:bd:6e:e3:b8 Signature Algorithm: sha1WithRSAEncryption Issuer: CN=myca Validity Not Before: Jan 6 03:10:58 2013 GMT Not After : Jan 6 03:10:58 2014 GMT Subject: CN=Device Subject Public Key Info:
Public Key Algorithm: rsaEncryption Public-Key: (1024 bit)
Modulus:
00:ab:45:64:a8:6c:10:70:3b:b9:46:34:8d:eb:1a:
a1:b3:64:b2:37:27:37:9d:15:bd:1a:69:1d:22:0f:
3a:5a:64:0c:8f:93:e5:f0:70:67:dc:cd:c1:6f:7a:
0c:b1:57:48:55:81:35:d7:36:d5:3c:37:1f:ce:16:
7e:f8:18:30:f6:6b:00:d6:50:48:23:5c:8c:05:30:
6f:35:04:37:1a:95:56:96:21:95:85:53:6f:f2:5a:
dc:f8:ec:42:4a:6d:5c:c8:43:08:bb:f1:f7:46:d5:
f1:9c:22:be:f3:1b:37:73:44:f5:2d:2c:5e:8f:40:
3e:36:36:0d:c8:33:90:f3:9b Exponent: 65537 (0x10001)
X509v3 extensions:
X509v3 CRL Distribution Points:

Full Name:
DirName: CN = myca Signature Algorithm: sha1WithRSAEncryption b0:9d:d9:ac:a0:9b:83:99:bf:9d:0a:ca:12:99:58:60:d8:aa:
73:54:61:4b:a2:4c:09:bb:9f:f9:70:c7:f8:81:82:f5:6c:af:
25:64:a5:99:d1:f6:ec:4f:22:e8:6a:96:58:6c:c9:47:46:8c:
f1:ba:89:b8:af:fa:63:c6:c9:77:10:45:0d:8f:a6:7f:b9:e8:
25:90:4a:8e:c6:cc:b8:1a:f8:e0:bc:17:e0:6a:11:ae:e7:36:
87:c4:b0:49:83:1c:79:ce:e2:a3:4b:15:40:dd:fe:e0:35:52:
ed:6d:83:31:2c:c2:de:7c:e0:a7:92:61:bc:03:ab:40:bd:69:
1b:f5关于获取到的 CA 证书的详细信息可以通过相应的显示命令来查看，此处略。具体内容请参考命令display pki certificate domain。

##### 1.15.2 PKI实体向CA申请证书（采用Windows 2003 server CA服务器）

###### 1. 组网需求

配置 PKI 实体 Device 向 CA 服务器申请本地证书。

###### 2. 组网图

图1-3 实体向 申请证书组网图PKI CA

###### 3. 配置CA服务器

(1) 安装证书服务器组件
打开[控制面板]/[添加/删除程序]，选择[添加/删除 Windows 组件]中的“证书服务”进行安装。
安装过程中设置 的名称，该名称为信任的 的名称（本例中为 myca）。
CA CA
安装 插件
(2) SCEP
由于 作为 服务器时，缺省情况下不支持 SCEP，所以需要安装
Windows 2003 server CA
SCEP 插件，才能使设备具备证书自动注册、获取等功能。插件安装完毕后，弹出提示框，
提示框中的 URL 地址即为设备上配置的注册服务器地址。
(3) 修改证书服务的属性
完成上述配置后，打开[控制面板/管理工具]中的[证书颁发机构]，如果安装成功，在[颁发的
证书]中将存在两个 CA 颁发给 RA 的证书。选择[CA server 属性]中的“策略模块”的属性为
“如果可以的话，按照证书模板中的设置。否则，将自动颁发证书 。”
(F)
(4) 修改 IIS 服务的属性

打开[控制面板/管理工具]中的[Internet 信息服务(IIS)管理器]，将[默认网站 属性]中“主目录”的本地路径修改为证书服务保存的路径。另外，为了避免与已有的服务冲突，建议修改默认网站的 TCP 端口号为未使用的端口号（本例中为 8080）。
以上配置完成之后，还需要保证设备的系统时钟与 CA 的时钟同步才可以正常使用设备来申请证书。

###### 4. 配置Device

(1) 配置 PKI 实体
\# 配置 PKI 实体名称为 aaa，通用名为 test。
<Device> system-view
[Device] pki entity aaa
[Device-pki-entity-aaa] common-name test
[Device-pki-entity-aaa] quit
(2) 配置 PKI 域
\# 创建并进入 PKI 域 winserver。
[Device] pki domain winserver
配置设备信任的 的名称为 myca。
\# CA
[Device-pki-domain-winserver] ca identifier myca
\# 配置注册受理机构服务器的 URL，格式为 http://host:port/certsrv/mscep/mscep.dll。其中，
为 服务器的主机地址和端口号。
host:port CA
[Device-pki-domain-winserver] certificate request url
http://4.4.4.1:8080/certsrv/mscep/mscep.dll
\# 配置证书申请的注册受理机构为 RA。
[Device-pki-domain-winserver] certificate request from ra
\# 指定 PKI 实体名称为 aaa。
[Device-pki-domain-winserver] certificate request entity aaa
\# 指定证书申请使用的密钥对，用途为通用，名称为 abc，密钥长度为 1024 比特。
[Device-pki-domain-winserver] public-key rsa general name abc length 1024
[Device-pki-domain-winserver] quit
生成 算法的本地密钥对
(3) RSA
[Device] public-key local create rsa name abc
The range of public key modulus is (512 ~ 4096).
If the key modulus is greater than 512,it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
Create the key pair successfully.
证书申请
(4)
获取 证书并下载至本地。
\# CA
[Device] pki retrieve-certificate domain winserver ca
The trusted CA's finger print is:
MD5 fingerprint:766C D2C8 9E46 845B 4DCE 439C 1C1F 83AB
SHA1 fingerprint:97E5 DDED AB39 3141 75FB DB5C E7F8 D7D7 7C9B 97B4

Is the finger print correct?(Y/N):y Retrieved the certificates successfully.
\# 手工申请本地证书。
[Device] pki request-certificate domain winserver Start to request general certificate ...
……Certificate requested successfully.

###### 5. 验证配置

通过以下显示命令可以查看申请到的本地证书信息。
\# [Device] display pki certificate domain winserver local Certificate:
Data:
Version: 3 (0x2)
Serial Number:
(Negative)01:03:99:ff:ff:ff:ff:fd:11 Signature Algorithm: sha1WithRSAEncryption Issuer: CN=sec Validity Not Before: Dec 24 07:09:42 2012 GMT Not After : Dec 24 07:19:42 2013 GMT Subject: CN=test Subject Public Key Info:
Public Key Algorithm: rsaEncryption Public-Key: (2048 bit)
Modulus:
00:c3:b5:23:a0:2d:46:0b:68:2f:71:d2:14:e1:5a:
55:6e:c5:5e:26:86:c1:5a:d6:24:68:02:bf:29:ac:
dc:31:41:3f:5d:5b:36:9e:53:dc:3a:bc:0d:11:fb:
d6:7d:4f:94:3c:c1:90:4a:50:ce:db:54:e0:b3:27:
a9:6a:8e:97:fb:20:c7:44:70:8f:f0:b9:ca:5b:94:
f0:56:a5:2b:87:ac:80:c5:cc:04:07:65:02:39:fc:
db:61:f7:07:c6:65:4c:e4:5c:57:30:35:b4:2e:ed:
9c:ca:0b:c1:5e:8d:2e:91:89:2f:11:e3:1e:12:8a:
f8:dd:f8:a7:2a:94:58:d9:c7:f8:1a:78:bd:f5:42:
51:3b:31:5d:ac:3e:c3:af:fa:33:2c:fc:c2:ed:b9:
ee:60:83:b3:d3:e5:8e:e5:02:cf:b0:c8:f0:3a:a4:
b7:ac:a0:2c:4d:47:5f:39:4b:2c:87:f2:ee:ea:d0:
c3:d0:8e:2c:80:83:6f:39:86:92:98:1f:d2:56:3b:
d7:94:d2:22:f4:df:e3:f8:d1:b8:92:27:9c:50:57:
f3:a1:18:8b:1c:41:ba:db:69:07:52:c1:9a:3d:b1:
2d:78:ab:e3:97:47:e2:70:14:30:88:af:f8:8e:cb:
68:f9:6f:07:6e:34:b6:38:6a:a2:a8:29:47:91:0e:
25:39 Exponent: 65537 (0x10001)
X509v3 extensions:
X509v3 Key Usage:
Digital Signature, Non Repudiation, Key Encipherment, Data Encip

herment X509v3 Subject Key Identifier:
C9:BB:D5:8B:02:1D:20:5B:40:94:15:EC:9C:16:E8:9D:6D:FD:9F:34 X509v3 Authority Key Identifier:
keyid:32:F1:40:BA:9E:F1:09:81:BD:A8:49:66:FF:F8:AB:99:4A:30:21:9 B X509v3 CRL Distribution Points:
Full Name:
URI:file://\\g07904c\CertEnroll\sec.crl Authority Information Access:
CA Issuers - URI:http://gc/CertEnroll/gc_sec.crt CA Issuers - URI:file://\\gc\CertEnroll\gc_sec.crt
1.3.6.1.4.1.311.20.2:
.0.I.P.S.E.C.I.n.t.e.r.m.e.d.i.a.t.e.O.f.f.l.i.n.e Signature Algorithm: sha1WithRSAEncryption 76:f0:6c:2c:4d:bc:22:59:a7:39:88:0b:5c:50:2e:7a:5c:9d:
6c:28:3c:c0:32:07:5a:9c:4c:b6:31:32:62:a9:45:51:d5:f5:
36:8f:47:3d:47:ae:74:6c:54:92:f2:54:9f:1a:80:8a:3f:b2:
14:47:fa:dc:1e:4d:03:d5:d3:f5:9d:ad:9b:8d:03:7f:be:1e:
29:28:87:f7:ad:88:1c:8f:98:41:9a:db:59:ba:0a:eb:33:ec:
cf:aa:9b:fc:0f:69:3a:70:f2:fa:73:ab:c1:3e:4d:12:fb:99:
31:51:ab:c2:84:c0:2f:e5:f6:a7:c3:20:3c:9a:b0:ce:5a:bc:
0f:d9:34:56:bc:1e:6f:ee:11:3f:7c:b2:52:f9:45:77:52:fb:
46:8a:ca:b7:9d:02:0d:4e:c3:19:8f:81:46:4e:03:1f:58:03:
bf:53:c6:c4:85:95:fb:32:70:e6:1b:f3:e4:10:ed:7f:93:27:
90:6b:30:e7:81:36:bb:e2:ec:f2:dd:2b:bb:b9:03:1c:54:0a:
00:3f:14:88:de:b8:92:63:1e:f5:b3:c2:cf:0a:d5:f4:80:47:
6f:fa:7e:2d:e3:a7:38:46:f6:9e:c7:57:9d:7f:82:c7:46:06:
7d:7c:39:c4:94:41:bd:9e:5c:97:86:c8:48:de:35:1e:80:14:
02:09:ad:08关于获取到的 CA 证书的详细信息可以通过相应的显示命令来查看，此处略。具体内容请参考命令display pki certificate domain。

##### 1.15.3 PKI实体向CA申请证书（采用OpenCA服务器）

###### 1. 组网需求

配置 PKI 实体 Device 向 CA 服务器申请本地证书。

###### 2. 组网图

图1-4 PKI 实体向 CA 申请证书组网图

###### 3. 配置CA服务器

配置过程略，具体请参考 服务器的相关手册。
Open CA需要注意的是：
使用 最新版本的 包进行安装，OpenCA 有多个版本，但只有 以后的版本
• OpenCA rpm 0.9.2才支持 SCEP，至少要安装 0.9.2 以后的版本。
• OpenCA 服务器配置完成之后，还需要保证设备的系统时钟与 CA 的时钟同步才可以正常使用设备来申请证书。

###### 4. 配置Device

(1) 配置 PKI 实体
\# 配置 PKI 实体，名称为 aaa、通用名为 rnd、国家码为 CN、组织名为 test、组织部门名为
software。
<Device> system-view
[Device] pki entity aaa
[Device-pki-entity-aaa] common-name rnd
[Device-pki-entity-aaa] country CN
[Device-pki-entity-aaa] organization test
[Device-pki-entity-aaa] organization-unit software
[Device-pki-entity-aaa] quit
(2) 配置 PKI 域
\# 创建并进入 PKI 域 openca。
[Device] pki domain openca
\# 配置设备信任的 CA 的名称为 myca。
[Device-pki-domain-openca] ca identifier myca
\# 配置注册受理机构服务器的 URL。通常，格式为 http://host/cgi-bin/pki/scep。其中，host
为 服务器的主机地址。
OpenCA
[Device-pki-domain-openca] certificate request url
http://192.168.222.218/cgi-bin/pki/scep
\# 配置证书申请的注册受理机构为 RA。
[Device-pki-domain-openca] certificate request from ra
\# 指定 PKI 实体名称为 aaa。
[Device-pki-domain-openca] certificate request entity aaa
指定证书申请使用的 密钥对，用途为通用，名称为 abc，密钥长度为 比特。
\# RSA 1024
[Device-pki-domain-openca] public-key rsa general name abc length 1024
[Device-pki-domain-openca] quit

###### 5. 验证配置

(3) 生成 RSA 算法的本地密钥对
[Device] public-key local create rsa name abc
The range of public key modulus is (512 ~ 4096).
If the key modulus is greater than 512,it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
Create the key pair successfully.
(4) 证书申请
\# 获取 CA 证书并下载至本地。
[Device] pki retrieve-certificate domain openca ca
The trusted CA's finger print is:
MD5 fingerprint:5AA3 DEFD 7B23 2A25 16A3 14F4 C81C C0FA
SHA1 fingerprint:9668 4E63 D742 4B09 90E0 4C78 E213 F15F DC8E 9122
Is the finger print correct?(Y/N):y
Retrieved the certificates successfully.
\# 手工申请本地证书。
[Device] pki request-certificate domain openca
Start to request general certificate ...
……
Certificate requested successfully.
验证配置
5.
\# 通过以下显示命令可以查看申请到的本地证书信息。
[Device] display pki certificate domain openca local
Certificate:
Data:
Version: 3 (0x2)
Serial Number:
21:1d:b8:d2:e4:a9:21:28:e4:de
Signature Algorithm: sha256WithRSAEncryption
Issuer: C=CN, L=shangdi, ST=pukras, O=OpenCA Labs, OU=mysubUnit, CN=sub-ca,
DC=pki-subdomain, DC=mydomain-sub, DC=com
Validity
Not Before: Jun 30 09:09:09 2011 GMT
Not After : May 1 09:09:09 2012 GMT
Subject: CN=rnd, O=test, OU=software, C=CN
Subject Public Key Info:
Public Key Algorithm: rsaEncryption
Public-Key: (1024 bit)
Modulus:
00:b8:7a:9a:b8:59:eb:fc:70:3e:bf:19:54:0c:7e:
c3:90:a5:d3:fd:ee:ff:c6:28:c6:32:fb:04:6e:9c:
d6:5a:4f:aa:bb:50:c4:10:5c:eb:97:1d:a7:9e:7d:
53:d5:31:ff:99:ab:b6:41:f7:6d:71:61:58:97:84:
37:98:c7:7c:79:02:ac:a6:85:f3:21:4d:3c:8e:63:

8d:f8:71:7d:28:a1:15:23:99:ed:f9:a1:c3:be:74:
0d:f7:64:cf:0a:dd:39:49:d7:3f:25:35:18:f4:1c:
59:46:2b:ec:0d:21:1d:00:05:8a:bf:ee:ac:61:03:
6c:1f:35:b5:b4:cd:86:9f:45 Exponent: 65537 (0x10001)
X509v3 extensions:
X509v3 Basic Constraints:
CA:FALSE Netscape Cert Type:
SSL Client, S/MIME X509v3 Key Usage:
Digital Signature, Non Repudiation, Key Encipherment X509v3 Extended Key Usage:
TLS Web Client Authentication, E-mail Protection, Microsoft Smartcardlogin Netscape Comment:
User Certificate of OpenCA Labs X509v3 Subject Key Identifier:
24:71:C9:B8:AD:E1:FE:54:9A:EA:E9:14:1B:CD:D9:45:F4:B2:7A:1B X509v3 Authority Key Identifier:
keyid:85:EB:D5:F7:C9:97:2F:4B:7A:6D:DD:1B:4D:DD:00:EE:53:CF:FD:5B X509v3 Issuer Alternative Name:
DNS:root@docm.com, DNS:, IP Address:192.168.154.145, IP Address:192.168.154.138 Authority Information Access:
CA Issuers - URI:http://192.168.222.218/pki/pub/cacert/cacert.crt OCSP - URI:http://192.168.222.218:2560/
1.3.6.1.5.5.7.48.12 - URI:http://192.168.222.218:830/ X509v3 CRL Distribution Points:
Full Name:
URI:http://192.168.222.218/pki/pub/crl/cacrl.crl Signature Algorithm: sha256WithRSAEncryption 5c:4c:ba:d0:a1:35:79:e6:e5:98:69:91:f6:66:2a:4f:7f:8b:
0e:80:de:79:45:b9:d9:12:5e:13:28:17:36:42:d5:ae:fc:4e:
ba:b9:61:f1:0a:76:42:e7:a6:34:43:3e:2d:02:5e:c7:32:f7:
6b:64:bb:2d:f5:10:6c:68:4d:e7:69:f7:47:25:f5:dc:97:af:
ae:33:40:44:f3:ab:e4:5a:a0:06:8f:af:22:a9:05:74:43:b6:
e4:96:a5:d4:52:32:c2:a8:53:37:58:c7:2f:75:cf:3e:8e:ed:
46:c9:5a:24:b1:f5:51:1d:0f:5a:07:e6:15:7a:02:31:05:8c:
03:72:52:7c:ff:28:37:1e:7e:14:97:80:0b:4e:b9:51:2d:50:
98:f2:e4:5a:60:be:25:06:f6:ea:7c:aa:df:7b:8d:59:79:57:
8f:d4:3e:4f:51:c1:34:e6:c1:1e:71:b5:0d:85:86:a5:ed:63:
1e:08:7f:d2:50:ac:a0:a3:9e:88:48:10:0b:4a:7d:ed:c1:03:
9f:87:97:a3:5e:7d:75:1d:ac:7b:6f:bb:43:4d:12:17:9a:76:
b0:bf:2f:6a:cc:4b:cd:3d:a1:dd:e0:dc:5a:f3:7c:fb:c3:29:
b0:12:49:5c:12:4c:51:6e:62:43:8b:73:b9:26:2a:f9:3d:a4:

###### 2. 组网图

###### 4. 配置Device A

81:99:31:89关于获取到的 CA 证书的详细信息可以通过相应的显示命令来查看，此处略。具体内容请参考命令display pki certificate domain。

##### 1.15.4 使用RSA数字签名方法进行IKE协商认证（采用Windows 2003 server CA服务器）

###### 1. 组网需求

在 Device A 和 Device B 之间建立一个 IPsec 安全隧道对子网 10.1.1.0/24 上的主机 A 与子网
•
11.1.1.0/24 上的主机 B 之间的数据流进行安全保护。
在 和 之间使用 自动协商建立安全通信，IKE 认证策略采用 数字
• Device A Device B IKE RSA签名方法进行身份认证。
• Device A 和 Device B 使用相同的 CA。
组网图
2.
图1-5 使用 RSA 数字签名方法进行 IKE 协商认证组网图

###### 3. 配置CA服务器

本例CA server采用Windows 2003 server CA服务器，CA服务器配置参看“1.15.2 3. 配置CA服务器”。
配置Device
4. A \# 配置 PKI 实体。
<DeviceA> system-view [DeviceA] pki entity en [DeviceA-pki-entity-en] ip 2.2.2.1

[DeviceA-pki-entity-en] common-name devicea [DeviceA-pki-entity-en] quit \# 配置 PKI 域参数。
[DeviceA] pki domain 1 [DeviceA-pki-domain-1] ca identifier CA1 [DeviceA-pki-domain-1] certificate request url http://1.1.1.100/certsrv/mscep/mscep.dll [DeviceA-pki-domain-1] certificate request entity en [DeviceA-pki-domain-1] ldap-server host 1.1.1.102 \# 配置通过 RA 注册申请证书。
[DeviceA-pki-domain-1] certificate request from ra指定证书申请使用的 密钥对，用途为通用，名称为 abc，密钥长度为 比特。
\# RSA 1024 [DeviceA-pki-domain-1] public-key rsa general name abc length 1024 [DeviceA-pki-domain-1] quit \# 生成 RSA 算法的本地密钥对。
[DeviceA] public-key local create rsa name abc The range of public key modulus is (512 ~ 4096).
If the key modulus is greater than 512,it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
Create the key pair successfully.
\# 获取 CA 证书并下载至本地。
[DeviceA] pki retrieve-certificate domain 1 ca手工申请本地证书。
\# [DeviceA] pki request-certificate domain 1 \# 配置 IKE 提议 1，使用数字签名（rsa-signature）方法为身份认证策略。
[DeviceA] ike proposal 1 [DeviceA-ike-proposal-1] authentication-method rsa-signature [DeviceA-ike-proposal-1] quit \# 在 IKE profile 1 中指定 IKE 协商使用的 PKI 域。
[DeviceA] ike profile peer [DeviceA-ike-profile-peer] certificate domain 1

###### 5. 配置Device B

配置 实体。
\# PKI <DeviceB> system-view [DeviceB] pki entity en [DeviceB-pki-entity-en] ip 3.3.3.1 [DeviceB-pki-entity-en] common-name deviceb [DeviceB-pki-entity-en] quit \# 配置 PKI 域参数。（证书申请的注册机构服务器的 URL 根据所使用的 CA 服务器的不同而有所不同，这里的配置只作为示例，请根据具体情况配置。）
[DeviceB] pki domain 1 [DeviceB-pki-domain-1] ca identifier CA1

[DeviceB-pki-domain-1] certificate request url http://1.1.1.100/certsrv/mscep/mscep.dll [DeviceB-pki-domain-1] certificate request entity en [DeviceB-pki-domain-1] ldap-server host 1.1.1.102 \# 配置通过 RA 注册申请证书。
[DeviceB-pki-domain-1] certificate request from ra \# 指定证书申请使用的 RSA 密钥对，用途为通用，名称为 abc，密钥长度为 1024 比特。
[DeviceB-pki-domain-1] public-key rsa general name abc length 1024 [DeviceB-pki-domain-1] quit \# 生成 RSA 算法的本地密钥对。
[DeviceB] public-key local create rsa name abc The range of public key modulus is (512 ~ 4096).
If the key modulus is greater than 512,it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
Create the key pair successfully.
\# 获取 CA 证书并下载至本地。
[DeviceB] pki retrieve-certificate domain 1 ca The trusted CA's finger print is:
MD5 fingerprint:5C41 E657 A0D6 ECB4 6BD6 1823 7473 AABC SHA1 fingerprint:1616 E7A5 D89A 2A99 9419 1C12 D696 8228 87BC C266 Is the finger print correct?(Y/N):y Retrieved the certificates successfully.
\# 手工申请本地证书。
[DeviceB] pki request-certificate domain 1 Start to request general certificate ...
...
Certificate requested successfully.
\# 配置 IKE 提议 1，使用 rsa-signature 方法为身份认证策略。
[DeviceB] ike proposal 1 [DeviceB-ike-proposal-1] authentication-method rsa-signature [DeviceB-ike-proposal-1] quit \# 在 IKE profile 1 中指定 IKE 协商使用的 PKI 域。
[DeviceB] ike profile peer [DeviceB-ike-profile-peer] certificate domain 1以上是对IKE协商采用RSA数字签名认证方法的配置，若希望建立IPsec安全通道进行安全通信，还需要进行 IPsec 的相应配置，具体内容请参见“安全配置指导”中“IPsec”。

###### 1. 组网需求

##### 1.15.5 证书属性的访问控制策略应用举例

组网需求
1.
• 客户端通过 HTTPS 协议远程访问设备（HTTPS 服务器）。
• 通过 SSL 协议保证合法客户端安全登录 HTTPS 服务器。
• HTTPS 服务器要求对客户端进行身份验证，并通过制定证书访问控制策略，对客户端的证书合法性进行检测。

###### 2. 组网图

图1-6 证书属性的访问控制策略应用组网图

###### 3. 配置步骤

SSL 策略所引用的 PKI 域 domain1 必须首先创建。
•
• Device 上也需要申请一个本地证书作为 SSL 服务器端证书。
(1) 配置 HTTPS 服务器\# 配置 HTTPS 服务器使用的 SSL 策略。
<Device> system-view [Device] ssl server-policy abc [Device-ssl-server-policy-abc] pki-domain domain1 [Device-ssl-server-policy-abc] client-verify enable [Device-ssl-server-policy-abc] quit \# 设置 HTTPS 服务使用的 SSL 服务器端策略为 abc [Device] ip https ssl-server-policy abc开启 服务。
\# HTTPS [Device] ip https enable
(2) 配置证书属性组\# 配置证书属性组 mygroup1 ，并创建两个属性规则。规则 1 定义证书主题名的 DN 包含字符串 aabbcc；规则 定义证书颁发者名中的 地址等于 10.0.0.1。
2 IP [Device] pki certificate attribute-group mygroup1 [Device-pki-cert-attribute-group-mygroup1] attribute 1 subject-name dn ctn aabbcc [Device-pki-cert-attribute-group-mygroup1] attribute 2 issuer-name ip equ 10.0.0.1

[Device-pki-cert-attribute-group-mygroup1] quit \# 配置证书属性组 mygroup2，并创建两个属性规则。规则 1 定义证书备用主题名中的 FQDN不包含字符串 apple；规则 2 定义证书颁发者名的 DN 包含字符串 aabbcc。
[Device] pki certificate attribute-group mygroup2 [Device-pki-cert-attribute-group-mygroup2] attribute 1 alt-subject-name fqdn nctn apple [Device-pki-cert-attribute-group-mygroup2] attribute 2 issuer-name dn ctn aabbcc [Device-pki-cert-attribute-group-mygroup2] quit
(3) 配置证书访问控制策略\# 创建访问控制策略 myacp，并定义两个访问控制规则。
[Device] pki certificate access-control-policy myacp规则 定义，当证书的属性与属性组 里定义的属性匹配时，认为该证书无效，不\# 1 mygroup1能通过访问控制策略的检测。
[Device-pki-cert-acp-myacp] rule 1 deny mygroup1 \# 规则 2 定义，当证书的属性与属性组 mygroup2 里定义的属性匹配时，认为该证书有效，可以通过访问控制策略的检测。
[Device-pki-cert-acp-myacp] rule 2 permit mygroup2 [Device-pki-cert-acp-myacp] quit \# 设置 HTTPS 服务使用的证书属性访问控制策略为 myacp。
[Device] ip https certificate access-control-policy myacp

###### 4. 验证配置

当客户端通过浏览器访问 HTTPS 服务器时，服务器端首先根据配置的证书访问控制策略检测客户端证书的有效性。已知该客户端证书的主题名的 DN 为 aabbcc，颁发者名中的 IP 地址为 1.1.1.1，备用主题名中的 名为 banaba，由以上配置可判断匹配结果为：
FQDN本地证书的主题名和属性组 mygroup1 中的属性 1 匹配、颁发者名和属性组 mygroup1 中的属
•性 2 不匹配，因此该证书和证书属性组 mygroup1 不匹配。
本地证书的备用主题名属性和属性组 中的属性 匹配，颁发者名属性和属性组
• mygroup2 1 mygroup2 中的属性 2 匹配，因此该证书和证书属性组 mygroup2 匹配。
该客户端的证书与访问控制策略 myacp 的规则 1 所引用的证书属性组 mygroup1 不匹配，因此规则1 不生效；本地证书与访问控制策略 myacp 的规则 2 所引用的证书属性组 mygroup2 匹配，因此规则 生效，该证书可以通过访问控制策略 的检测。
2 myacp通过以上检测后的合法客户端可以成功访问 HTTPS 服务器提供的网页。

##### 1.15.6 导出、导入证书应用举例

###### 1. 组网需求

某网络中的 将要被 替换，Device 上的 域 中保存了两个携Device A Device B A PKI exportdomain带私钥的本地证书和一个 CA 证书。为保证替换后的证书可用，需要将原来 Device A 上的证书复制到 Device B 上去。具体要求如下：
• 从 Device A 上导出本地证书时，将对应的私钥数据采用 3DES_CBC 算法进行加密，加密口令为 111111。
• 来自 Device A 的证书以 PEM 编码的格式保存于 Device B 上的 PKI 域 importdomain 中。

###### 2. 组网图

图1-7 导出、导入证书应用组网图

###### 3. 配置步骤

(1) 从 Device A 上导出本地证书到指定文件
\# 将 PKI 域中的 CA 证书导出到 PEM 格式的文件中，文件名为 pkicachain.pem 。
<DeviceA> system-view
[DeviceA] pki export domain exportdomain pem ca filename pkicachain.pem
\# 将 PKI 域中的本地证书导出到 PEM 格式的文件中，文件名为 pkilocal.pem。导出时对本地
证书对应的私钥数据采用 3DES_CBC 算法进行加密，加密口令为 111111。
[DeviceA] pki export domain exportdomain pem local 3des-cbc 111111 filename pkilocal.pem
以上过程完成后，系统中将会生成三个 PEM 格式的证书文件，它们分别是：CA 证书文件
pkicachain.pem，带有私钥的本地签名证书文件 pkilocal.pem-signature 和带有私钥的本地加
密证书文件 pkilocal.pem-encryption。
查看 格式的带有私钥的本地签名证书文件 pkilocal.pem-signature。
\# PEM
[DeviceA] quit
<DeviceA> more pkicachain.pem-sign
Bag Attributes
friendlyName:
localKeyID: 90 C6 DC 1D 20 49 4F 24 70 F5 17 17 20 2B 9E AC 20 F3 99 89
subject=/C=CN/O=OpenCA Labs/OU=Users/CN=subsign 11
issuer=/C=CN/L=shangdi/ST=pukras/O=OpenCA Labs/OU=docm/CN=subca1
-----BEGIN CERTIFICATE-----
MIIEgjCCA2qgAwIBAgILAJgsebpejZc5UwAwDQYJKoZIhvcNAQELBQAwZjELMAkG
…… (略)
-----END CERTIFICATE-----
Bag Attributes
friendlyName:
localKeyID: 90 C6 DC 1D 20 49 4F 24 70 F5 17 17 20 2B 9E AC 20 F3 99 89
Key Attributes: <No Attributes>
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIICxjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIZtjSjfslJCoCAggA
略
…… ( )
-----END ENCRYPTED PRIVATE KEY-----
\# 查看 PEM 格式的带有私钥的本地加密证书文件 pkilocal.pem-encryption。
<DeviceA> more pkicachain.pem-encr

Bag Attributes friendlyName:
localKeyID: D5 DF 29 28 C8 B9 D9 49 6C B5 44 4B C2 BC 66 75 FE D6 6C C8 subject=/C=CN/O=OpenCA Labs/OU=Users/CN=subencr 11 issuer=/C=CN/L=shangdi/ST=pukras/O=OpenCA Labs/OU=docm/CN=subca1
-----BEGIN CERTIFICATE----- MIIEUDCCAzigAwIBAgIKCHxnAVyzWhIPLzANBgkqhkiG9w0BAQsFADBmMQswCQYD…… (略)
-----END CERTIFICATE----- Bag Attributes friendlyName:
localKeyID: D5 DF 29 28 C8 B9 D9 49 6C B5 44 4B C2 BC 66 75 FE D6 6C C8 Key Attributes: <No Attributes>
-----BEGIN ENCRYPTED PRIVATE KEY----- MIICxjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQI7H0mb4O7/GACAggA…… (略)
-----END ENCRYPTED PRIVATE KEY-----
(2) 将 Device A 的证书文件下载到 Host通过 将证书文件 pkicachain.pem、pkilocal.pem-sign 和 下载到FTP pkilocal.pem-encr Host上，具体过程略。
(3) 将 Host 上的证书文件上传到 Device B通过 FTP 将证书文件 pkicachain.pem、pkilocal.pem-sign、pkilocal.pem-encr 上传到 Device B 的文件系统中，具体过程略。
(4) 在设备 Device B 上导入证书文件\# 关闭 CRL 检查。（是否进行 CRL 检查，请以实际的使用需求为准，此处仅为示例）
<DeviceB> system-view [DeviceB] pki domain importdomain [DeviceB-pki-domain-importdomain] undo crl check enable \# 指定证书申请使用的签名 RSA 密钥对名称为 sign，加密 RSA 密钥对名称为 encr。
[DeviceB-pki-domain-importdomain] public-key rsa signature name sign encryption name encr [DeviceB-pki-domain-importdomain] quit \# 向 PKI 域中导入 CA 证书，证书文件格式为 PEM 编码，证书文件名称为 pkicachain.pem 。
[DeviceB] pki import domain importdomain pem ca filename pkicachain.pem \# 向 PKI 域中导入本地证书，证书文件格式为 PEM 编码，证书文件名称为pkilocal.pem-signature，证书文件中包含了密钥对。
[DeviceB] pki import domain importdomain pem local filename pkilocal.pem-signature Please input the password:******向 域中导入本地证书，证书文件格式为 编码，证书文件名称为\# PKI PEM pkilocal.pem-encryption，证书文件中包含了密钥对。
[DeviceB] pki import domain importdomain pem local filename pkilocal.pem-encryption Please input the password:****** \# 通过以下显示命令可以查看导入到 Device B 的本地证书信息。
[DeviceB] display pki certificate domain importdomain local Certificate:

Data:
Version: 3 (0x2)
Serial Number:
98:2c:79:ba:5e:8d:97:39:53:00 Signature Algorithm: sha256WithRSAEncryption Issuer: C=CN, L=shangdi, ST=pukras, O=OpenCA Labs, OU=docm, CN=subca1 Validity Not Before: May 26 05:56:49 2011 GMT Not After : Nov 22 05:56:49 2012 GMT Subject: C=CN, O=OpenCA Labs, OU=Users, CN=subsign 11 Subject Public Key Info:
Public Key Algorithm: rsaEncryption Public-Key: (1024 bit)
Modulus:
00:9f:6e:2f:f6:cb:3d:08:19:9a:4a:ac:b4:ac:63:
ce:8d:6a:4c:3a:30:19:3c:14:ff:a9:50:04:f5:00:
ee:a3:aa:03:cb:b3:49:c4:f8:ae:55:ee:43:93:69:
6c:bf:0d:8c:f4:4e:ca:69:e5:3f:37:5c:83:ea:83:
ad:16:b8:99:37:cb:86:10:6b:a0:4d:03:95:06:42:
ef:ef:0d:4e:53:08:0a:c9:29:dd:94:28:02:6e:e2:
9b:87:c1:38:2d:a4:90:a2:13:5f:a4:e3:24:d3:2c:
bf:98:db:a7:c2:36:e2:86:90:55:c7:8c:c5:ea:12:
01:31:69:bf:e3:91:71:ec:21 Exponent: 65537 (0x10001)
X509v3 extensions:
X509v3 Basic Constraints:
CA:FALSE Netscape Cert Type:
SSL Client, S/MIME X509v3 Key Usage:
Digital Signature, Non Repudiation X509v3 Extended Key Usage:
TLS Web Client Authentication, E-mail Protection, Microsoft Smartcardlogin Netscape Comment:
User Certificate of OpenCA Labs X509v3 Subject Key Identifier:
AA:45:54:29:5A:50:2B:89:AB:06:E5:BD:0D:07:8C:D9:79:35:B1:F5 X509v3 Authority Key Identifier:
keyid:70:54:40:61:71:31:02:06:8C:62:11:0A:CC:A5:DB:0E:7E:74:DE:DD X509v3 Subject Alternative Name:
email:subsign@docm.com X509v3 Issuer Alternative Name:
DNS:subca1@docm.com, DNS:, IP Address:1.1.2.2, IP Address:2.2.1.1 Authority Information Access:
CA Issuers - URI:http://titan/pki/pub/cacert/cacert.crt OCSP - URI:http://titan:2560/
1.3.6.1.5.5.7.48.12 - URI:http://titan:830/

X509v3 CRL Distribution Points:
Full Name:
URI:http://192.168.40.130/pki/pub/crl/cacrl.crl Signature Algorithm: sha256WithRSAEncryption 18:e7:39:9a:ad:84:64:7b:a3:85:62:49:e5:c9:12:56:a6:d2:
46:91:53:8e:84:ba:4a:0a:6f:28:b9:43:bc:e7:b0:ca:9e:d4:
1f:d2:6f:48:c4:b9:ba:c5:69:4d:90:f3:15:c4:4e:4b:1e:ef:
2b:1b:2d:cb:47:1e:60:a9:0f:81:dc:f2:65:6b:5f:7a:e2:36:
29:5d:d4:52:32:ef:87:50:7c:9f:30:4a:83:de:98:8b:6a:c9:
3e:9d:54:ee:61:a4:26:f3:9a:40:8f:a6:6b:2b:06:53:df:b6:
5f:67:5e:34:c8:c3:b5:9b:30:ee:01:b5:a9:51:f9:b1:29:37:
02:1a:05:02:e7:cc:1c:fe:73:d3:3e:fa:7e:91:63:da:1d:f1:
db:28:6b:6c:94:84:ad:fc:63:1b:ba:53:af:b3:5d:eb:08:b3:
5b:d7:22:3a:86:c3:97:ef:ac:25:eb:4a:60:f8:2b:a3:3b:da:
5d:6f:a5:cf:cb:5a:0b:c5:2b:45:b7:3e:6e:39:e9:d9:66:6d:
ef:d3:a0:f6:2a:2d:86:a3:01:c4:94:09:c0:99:ce:22:19:84:
2b:f0:db:3e:1e:18:fb:df:56:cb:6f:a2:56:35:0d:39:94:34:
6d:19:1d:46:d7:bf:1a:86:22:78:87:3e:67:fe:4b:ed:37:3d:
d6:0a:1c:0b Certificate:
Data:
Version: 3 (0x2)
Serial Number:
08:7c:67:01:5c:b3:5a:12:0f:2f Signature Algorithm: sha256WithRSAEncryption Issuer: C=CN, L=shangdi, ST=pukras, O=OpenCA Labs, OU=docm, CN=subca1 Validity Not Before: May 26 05:58:26 2011 GMT Not After : Nov 22 05:58:26 2012 GMT Subject: C=CN, O=OpenCA Labs, OU=Users, CN=subencr 11 Subject Public Key Info:
Public Key Algorithm: rsaEncryption Public-Key: (1024 bit)
Modulus:
00:db:26:13:d3:d1:a4:af:11:f3:6d:37:cf:d0:d4:
48:50:4e:0f:7d:54:76:ed:50:28:c6:71:d4:48:ae:
4d:e7:3d:23:78:70:63:18:33:f6:94:98:aa:fa:f6:
62:ed:8a:50:c6:fd:2e:f4:20:0c:14:f7:54:88:36:
2f:e6:e2:88:3f:c2:88:1d:bf:8d:9f:45:6c:5a:f5:
94:71:f3:10:e9:ec:81:00:28:60:a9:02:bb:35:8b:
bf:85:75:6f:24:ab:26:de:47:6c:ba:1d:ee:0d:35:
75:58:10:e5:e8:55:d1:43:ae:85:f8:ff:75:81:03:
8c:2e:00:d1:e9:a4:5b:18:39 Exponent: 65537 (0x10001)

X509v3 extensions:
X509v3 Basic Constraints:
CA:FALSE Netscape Cert Type:
SSL Server X509v3 Key Usage:
Key Encipherment, Data Encipherment Netscape Comment:
VPN Server of OpenCA Labs X509v3 Subject Key Identifier:
CC:96:03:2F:FC:74:74:45:61:38:1F:48:C0:E8:AA:18:24:F0:2B:AB X509v3 Authority Key Identifier:
keyid:70:54:40:61:71:31:02:06:8C:62:11:0A:CC:A5:DB:0E:7E:74:DE:DD X509v3 Subject Alternative Name:
email:subencr@docm.com X509v3 Issuer Alternative Name:
DNS:subca1@docm.com, DNS:, IP Address:1.1.2.2, IP Address:2.2.1.1 Authority Information Access:
CA Issuers - URI:http://titan/pki/pub/cacert/cacert.crt OCSP - URI:http://titan:2560/
1.3.6.1.5.5.7.48.12 - URI:http://titan:830/ X509v3 CRL Distribution Points:
Full Name:
URI:http://192.168.40.130/pki/pub/crl/cacrl.crl Signature Algorithm: sha256WithRSAEncryption 53:69:66:5f:93:f0:2f:8c:54:24:8f:a2:f2:f1:29:fa:15:16:
90:71:e2:98:e3:5c:c6:e3:d4:5f:7a:f6:a9:4f:a2:7f:ca:af:
c4:c8:c7:2c:c0:51:0a:45:d4:56:e2:81:30:41:be:9f:67:a1:
23:a6:09:50:99:a1:40:5f:44:6f:be:ff:00:67:9d:64:98:fb:
72:77:9e:fd:f2:4c:3a:b2:43:d8:50:5c:48:08:e7:77:df:fb:
25:9f:4a:ea:de:37:1e:fb:bc:42:12:0a:98:11:f2:d9:5b:60:
bc:59:72:04:48:59:cc:50:39:a5:40:12:ff:9d:d0:69:3a:5e:
3a:09:5a:79:e0:54:67:a0:32:df:bf:72:a0:74:63:f9:05:6f:
5e:28:d2:e8:65:49:e6:c7:b5:48:7d:95:47:46:c1:61:5a:29:
90:65:45:4a:88:96:e4:88:bd:59:25:44:3f:61:c6:b1:08:5b:
86:d2:4f:61:4c:20:38:1c:f4:a1:0b:ea:65:87:7d:1c:22:be:
b6:17:17:8a:5a:0f:35:4c:b8:b3:73:03:03:63:b1:fc:c4:f5:
e9:6e:7c:11:e8:17:5a:fb:39:e7:33:93:5b:2b:54:72:57:72:
5e:78:d6:97:ef:b8:d8:6d:0c:05:28:ea:81:3a:06:a0:2e:c3:
79:05:cd:c3关于导入的 CA 证书的详细信息可以通过相应的显示命令来查看，此处略。具体内容请参考命令 display pki certificate domain。

#### 1.16 常见配置错误举例

##### 1.16.1 获取CA证书失败

###### 1. 故障现象

获取 CA 证书失败。

###### 2. 故障分析

可能有以下原因：
• 网络连接故障，如网线折断，接口松动；
• 没有设置信任的 CA 名称；
• 证书申请的注册受理机构服务器 URL 位置不正确或未配置；
• 设备的系统时钟与 CA 的时钟不同步；
未指定 服务器可接受的 协议报文的源 地址，或者指定的地址不正确；
• CA PKI IP指纹信息不合法。
•

###### 3. 处理过程

• 排除物理连接故障；
• 查看各必配项是否都正确配置；
• 可通过 ping 命令测试注册服务器是否连接正常；
• 保持系统时钟与 CA 同步；
与 服务器管理员联系，并保证配置正确的源 地址；
• CA IP
在证书服务器上查看指纹信息是否合法。
•

##### 1.16.2 获取本地证书失败

###### 1. 故障现象

获取本地证书失败。

###### 2. 故障分析

可能有以下原因：
• 网络连接故障；
• 执行获取操作之前 PKI 域中没有 CA 证书；
• 没有配置 LDAP 服务器或者配置错误；
• PKI 域没有指定申请使用的密钥对，或者指定的密钥对与待获取的本地证书不匹配；
域中没有引用 实体配置，或 实体配置不正确；
• PKI PKI PKI开启了 检查，但是本地没有 且无法获取到 CRL；
• CRL CRL未指定 服务器可接受的 协议报文的源 地址，或者指定的地址不正确；
• CA PKI IP设备时钟与 服务器的时钟不同步。
• CA

###### 3. 处理过程

• 排除物理连接故障；

###### 1. 故障现象

###### 3. 处理过程

###### 1. 故障现象

获取或者导入 CA 证书；
•配置正确的 LDAP 服务器；
•在 PKI 域中指定申请使用的密钥对，生成指定的密钥对，并使其与待获取的本地证书匹配；
•
• PKI 域中引用正确的 PKI 实体，并正确配置该 PKI 实体；
• 获取 CRL；
• 与 CA 服务器管理员联系，并保证配置正确的源 IP 地址；
• 保持系统时钟与 CA 一致。

##### 1.16.3 本地证书申请失败

故障现象
1.
手工申请证书失败。

###### 2. 故障分析

可能有以下原因：
网络连接故障，如网线折断，接口松动；
•执行申请操作之前 PKI 域中没有 CA 证书；
•
• 证书申请的注册受理机构服务器 URL 位置不正确或未配置；
• 没有配置证书申请注册受理机构或配置不正确；
• 没有配置 PKI 实体 DN 中必配参数或者配置参数不正确；
• PKI 域中没有指定证书申请使用的密钥对，或者 PKI 中指定的密钥对在申请过程中已被修改；
• 当前 PKI 域中有互斥的证书申请程序正在运行；
• 未指定 CA 服务器可接受的 PKI 协议报文的源 IP 地址，或者指定的地址不正确；
• 设备时钟与 CA 服务器的时钟不同步。
处理过程
3.
• 排除物理连接故障；
• 获取或者导入 CA 证书；
• 可通过 ping 命令测试注册服务器是否连接正常；
• 配置正确的证书申请注册受理机构服务器 URL；
• 查看 CA/RA 注册策略，并对相关的 PKI 实体 DN 属性进行正确配置；
• 在 PKI 域中指定证书申请使用的密钥对，或者删除设备上 PKI 域中指定的密钥对并重新申请本地证书；
• 使用 pki abort-certificate- request domain 命令停止正在运行的证书申请程序；
• 与 CA 服务器管理员联系，并保证配置正确的源 IP 地址；
• 保持系统时钟与 CA 一致。

##### 1.16.4 CRL获取失败

故障现象
1.
获取 CRL 失败。

###### 3. 处理过程

###### 1. 故障现象

###### 2. 故障分析

可能有以下原因：
• 网络连接故障，如网线折断，接口松动；
• 获取 CRL 之前未先取得 CA 证书；
• 未设置 CRL 发布点位置，且不能从 PKI 域中 CA 证书或本地证书中获得正确的发布点；
• 设置的 CRL 发布点位置不正确；
• 不能获取 CRL 发布点的情况下，通过 SCEP 协议获取 CRL，但此时 PKI 域中不存在本地证书，或本地证书的密钥对已被修改，或 PKI 域中没有配置正确的证书申请 URL；
• CRL 发布点的 URL 配置中包含不完整的地址（没有主机名或主机地址）且 PKI 域中没有配置LDAP 服务器或者配置不正确；
• CA 没有签发 CRL；
• 未指定 CA 服务器可接受的 PKI 协议报文的源 IP 地址，或者指定的地址不正确。

###### 3. 处理过程

排除物理连接故障；
•获取或导入 CA 证书；
•设置正确 CRL 发布点位置：配置包含完整地址的 CRL 发布点的 URL 或在 PKI 域中配置正确
•的 服务器；
LDAP在无法获取 发布点的情况下，配置正确的证书申请 URL，并保证已经获取了本地证书，
• CRL且本地保存的密钥对的公钥与本地证书的公钥匹配；
• 在 CA 上发布 CRL；
• 与 CA 服务器管理员联系，并保证配置正确的源 IP 地址。

##### 1.16.5 导入CA证书失败

###### 1. 故障现象

导入证书失败。

###### 2. 故障分析

可能有以下原因：
• 开启了 CRL 检查，但是本地没有 CRL 且无法获取到 CRL；
• 指定的导入格式与实际导入的文件格式不一致。
处理过程
3.
• 执行 undo crl check enable 命令，关闭 CRL 检查；
• 请确认导入的文件格式并选择正确的导入格式。

##### 1.16.6 导入本地证书失败

故障现象
1.
导入证书失败。

###### 2. 故障分析

可能有以下原因：
• PKI 域中没有 CA 证书且导入的本地证书中不含 CA 证书链；
• 开启了 CRL 检查，但是本地没有 CRL 且无法获取到 CRL；
• 指定的导入格式与实际导入的文件格式不一致；
• 设备上和证书中都没有该本地证书对应的密钥对；
• 证书已经被吊销；
• 证书不在有效期；
系统时钟设置错误。
•

###### 3. 处理过程

• 获取或者导入 CA 证书；
• 执行 undo crl check enable 命令，关闭 CRL 检查，或者先获取 CRL；
• 请确认导入的文件格式并选择正确的导入格式；
• 请导入包含私钥内容的证书文件；
• 导入未被吊销的证书；
导入还在有效期内的证书；
•
请重新设置正确的系统时钟。
•

##### 1.16.7 导出证书失败

###### 1. 故障现象

导出证书失败。

###### 2. 故障分析

可能有以下原因：
• 以 PKCS#12 格式导出所有证书时 PKI 域中没有本地证书；
• 用户所设置的导出路径不存在；
• 用户所设置的导出路径不合法；
• 要导出的本地证书的公钥和它所属 PKI 域中的密钥对的公钥部分不匹配；
设备磁盘空间已满。
•

###### 3. 处理过程

• 获取或申请本地证书；
• 用 mkdir 命令创建用户所需路径；
• 设置正确的导出路径；
• 在 PKI 域中配置匹配的密钥对；
• 清理设备磁盘空间。

###### 1. 故障现象

##### 1.16.8 设置存储路径失败

故障现象
1.
设置证书或 CRL 存储路径失败。

###### 2. 故障分析

可能有以下原因：
用户所设置的证书或 CRL 存储路径不存在；
•用户所设置的证书或 CRL 存储路径不合法；
•设备磁盘空间已满。
•

###### 3. 处理过程

用 命令创建用户所需路径；
• mkdir设置正确的证书或 存储路径；
• CRL清理设备磁盘空间。
•

## 13-IPsec配置

目 录简介认证与加密安全策略和 安全框架相关说明配置配置 协商方式的 安全策略配置IPsec抗重放窗口和序号的同步功能设置 隧道模式下封装后外层 头的 位

配置手工方式的IPsec安全框架配置本端允许建立 隧道的最大数显示和维护配置IPsec保护RIPng报文协议规范配置配置keychain或者PKI域配置内部MPLS L3VPN实例配置IKE

配置IKE Keepalive功能配置 告警功能主模式及预共享密钥认证配置举例未正确引用IKE提议或IKE keychain导致IKE SA协商失败配置任务简介指定 协商时本端和对端采用的身份认证方式配置匹配对端身份的规则配置IKEv2 安全策略配置IKEv2 全局参数

配置IKEv2 Keepalive功能提议不匹配导致 协商失败

### 1 IPsec

1 IPsec

#### 1.1 IPsec简介

IPsec（IP Security，IP 安全）是 制定的三层隧道加密协议，它为互联网上传输的数据提供了IETF高质量的、基于密码学的安全保证，是一种传统的实现三层 VPN（Virtual Private Network，虚拟专用网络）的安全技术。IPsec 通过在特定通信方之间（例如两个安全网关之间）建立“通道”，来保护通信方之间传输的用户数据，该通道通常称为 隧道。
IPsec

##### 1.1.1 IPsec协议框架

IPsec 协议不是一个单独的协议，它为 IP 层上的网络数据安全提供了一整套安全体系结构，包括安全协议 AH（Authentication Header，认证头）和 ESP（Encapsulating Security Payload，封装安全载荷）、IKE（Internet Exchange，互联网密钥交换）以及用于网络认证及加密的一些算法等。
Key其中，AH 协议和 ESP 协议用于提供安全服务，IKE 协议用于密钥交换。关于 IKE 的详细介绍请参见“安全配置指导”中的“IKE”，本节不做介绍。

##### 1.1.2 IPsec提供的安全服务

提供了两大安全机制：认证和加密。认证机制使 通信的数据接收方能够确认数据发送方的IPsec IP真实身份以及数据在传输过程中是否遭篡改。加密机制通过对数据进行加密运算来保证数据的机密性，以防数据在传输过程中被窃听。
IPsec 为 IP 层的数据报文提供的安全服务具体包括以下几种：
• 数据机密性（Confidentiality）：发送方通过网络传输用户报文前，IPsec 对报文进行加密。
• 数据完整性（Data Integrity）：接收方对发送方发送来的 IPsec 报文进行认证，以确保数据在传输过程中没有被篡改。
• 数据来源认证（Data Origin Authentication）：接收方认证发送 IPsec 报文的发送端是否合法。
• 抗重放（Anti-Replay）：接收方可检测并拒绝接收过时或重复的 IPsec 报文。

##### 1.1.3 IPsec的优点

可为 层上的数据提供安全保护，其优点包括如下几个方面：
IPsec IP支持 IKE（Internet Exchange，互联网密钥交换），可实现密钥的自动协商功能，减少了
• Key密钥协商的开销。可以通过 IKE 建立和维护 SA（Security Association，安全联盟），简化了IPsec 的使用和管理。
• 所有使用 IP 协议进行数据传输的应用系统和服务都可以使用 IPsec，而不必对这些应用系统和服务本身做任何修改。
对数据的加密是以数据包为单位的，而不是以整个数据流为单位，这不仅灵活而且有助于进
•一步提高 数据包的安全性，可以有效防范网络攻击。
IP

##### 1.1.4 安全协议

包括 和 两种安全协议，它们定义了对 报文的封装格式以及可提供的安全服务。
IPsec AH ESP IP AH协议（IP协议号为 51）定义了AH头在IP报文中的封装格式，如 图 所示。AH可提供数
• 1-3据来源认证、数据完整性校验和抗重放功能，它能保护报文免受篡改，但不能防止报文被窃听，适合用于传输非机密数据。AH使用的认证算法有HMAC-MD5 和HMAC-SHA1 等。
• ESP协议（IP协议号为 50）定义了ESP头和ESP尾在IP报文中的封装格式，如 图 1-3 所示。
ESP可提供数据加密、数据来源认证、数据完整性校验和抗重放功能。与AH不同的是，ESP将需要保护的用户数据进行加密后再封装到IP包中，以保证数据的机密性。ESP使用的加密算法有DES、3DES、AES等。同时，作为可选项，ESP还可以提供认证服务，使用的认证算法有HMAC-MD5 和HMAC-SHA1 等。虽然AH和ESP都可以提供认证服务，但是AH提供的认证服务要强于ESP。
在实际使用过程中，可以根据具体的安全需求同时使用这两种协议或仅使用其中的一种。设备支持的 AH 和 ESP 联合使用的方式为：先对报文进行 ESP 封装，再对报文进行 AH 封装。

##### 1.1.5 封装模式

IPsec 支持两种封装模式：传输模式和隧道模式。

###### 1. 传输模式（Transport Mode）

该模式下的安全协议主要用于保护上层协议报文，仅传输层数据被用来计算安全协议头，生成的安全协议头以及加密的用户数据（仅针对ESP封装）被放置在原IP头后面。若要求端到端的安全保障，即数据包进行安全传输的起点和终点为数据包的实际起点和终点时，才能使用传输模式。如 图 1-1所示，通常传输模式用于保护两台主机之间的数据。
图1-1 传输模式下的 IPsec 保护

###### 2. 隧道模式（Tunnel Mode）

该模式下的安全协议用于保护整个IP数据包，用户的整个IP数据包都被用来计算安全协议头，生成的安全协议头以及加密的用户数据（仅针对ESP封装）被封装在一个新的IP数据包中。这种模式下，封装后的IP数据包有内外两个IP头，其中的内部IP头为原有的IP头，外部IP头由提供安全服务的设备添加。在安全保护由设备提供的情况下，数据包进行安全传输的起点或终点不为数据包的实际起点和终点时（例如安全网关后的主机），则必须使用隧道模式。如 图 所示，通常隧道模式用于1-2保护两个安全网关之间的数据。

图1-2 隧道模式下的 IPsec 保护不同的安全协议及组合在隧道和传输模式下的数据封装形式如 图 1-3 所示。
图1-3 安全协议数据封装格式

| Mode Protocol | Transport | Tunnel |
|---|---|---|
| AH | IP AH Data | IP AH IP Data |
| ESP | IP ESP Data ESP-T | IP ESP IP Data ESP-T |
| AH-ESP | IP AH ESP Data ESP-T | IP AH ESP IP Data ESP-T |

##### 1.1.6 安全联盟

IPsec 在两个端点之间提供安全通信，这类端点被称为 IPsec 对等体。SA（Security Association，安全联盟）是 对等体间对某些要素的约定，例如，使用的安全协议（AH、ESP 或两者结合IPsec使用）、协议报文的封装模式（传输模式或隧道模式）、认证算法（HMAC-MD5 或 HMAC-SHA1）、加密算法（DES、3DES 或 AES）、特定流中保护数据的共享密钥以及密钥的生存时间等。
SA 是单向的，在两个对等体之间的双向通信，最少需要两个 SA 来分别对两个方向的数据流进行安全保护。同时，如果两个对等体希望同时使用 和 来进行安全通信，则每个对等体都会针对AH ESP每一种协议来构建一个独立的 SA。
SA 由一个三元组来唯一标识，这个三元组包括 SPI（Security Parameter Index，安全参数索引）、目的 IP 地址和安全协议号。其中，SPI 是用于标识 SA 的一个 32 比特的数值，它在 AH 和 ESP 头中传输。
SA 有手工配置和 IKE 自动协商两种生成方式：
• 手工方式：通过命令行配置 SA 的所有信息。该方式的配置比较复杂，而且不支持一些高级特性（例如定时更新密钥），优点是可以不依赖 而单独实现 功能。该方式主要用于需IKE IPsec要安全通信的对等体数量较少，或小型静态的组网环境中。
• IKE 自动协商方式：对等体之间通过 IKE 协议自动协商生成 SA，并由 IKE 协议维护该 SA。
该方式的配置相对比较简单，扩展能力强。在中、大型的动态网络环境中，推荐使用 IKE 自动协商建立 SA。
手工方式建立的 SA 永不老化。通过 IKE 协商建立的 SA 具有生存时间，该类型的 SA 有两种形式的生存时间：
基于时间的生存时间，定义了一个 从建立到失效的时间；
• SA基于流量的生存时间，定义了一个 SA 允许处理的最大流量。
•

可同时存在基于时间和基于流量两种方式的 SA 生存时间，只要 SA 的生存时间到达指定的时间或流量时，该 就会失效。SA 失效前，IKE 将为 对等体协商建立新的 SA，这样，在旧的SA IPsec SA失效前新的 SA 就已经准备好。在新的 SA 开始协商而没有协商好之前，使用当前旧的 SA 保护通信。
一旦协商出新的 SA，立即采用新的 SA 保护通信。

##### 1.1.7 认证与加密

###### 1. 认证算法

IPsec 使用的认证算法主要是通过杂凑函数实现的。杂凑函数是一种能够接受任意长度的消息输入，并产生固定长度输出的算法，该算法的输出称为消息摘要。IPsec 对等体双方都会计算一个摘要，接收方将发送方的摘要与本地的摘要进行比较，如果二者相同，则表示收到的 IPsec 报文是完整未经篡改的，以及发送方身份合法。目前，IPsec 强制使用基于 HMAC（Hash-based Message Code，基于散列的消息鉴别码）的认证算法，包括 和 HMAC-SHA1。
Authentication HMAC-MD5其中，HMAC-MD5 算法的计算速度快，而 HMAC-SHA1 算法的安全强度高。

###### 2. 加密算法

IPsec 使用的加密算法属于对称密钥系统，这类算法使用相同的密钥对数据进行加密和解密。目前设备的 IPsec 使用三种加密算法：
• DES：使用 56 比特的密钥对一个 64 比特的明文块进行加密。
• 3DES：使用三个 56 比特（共 168 比特）的密钥对明文块进行加密。
• AES：使用 128 比特、192 比特或 256 比特的密钥对明文块进行加密。
这三个加密算法的安全性由高到低依次是：AES、3DES、DES，安全性高的加密算法实现机制复杂，运算速度慢。

##### 1.1.8 IPsec隧道保护的对象

IPsec隧道可以保护匹配ACL（Access Control List，访问控制列表）的报文、隧道接口上的报文和IPv6 路由协议报文。要实现建立IPsec隧道为两个IPsec对等体之间的数据提供安全保护，首先要配置和应用相应的安全策略，这里的安全策略包括IPsec安全策略和IPsec安全框架。有关IPsec安全策略和IPsec安全框架的详细介绍请参见“IPsec安全策略和IPsec安全框架”。
当 对等体根据 安全策略和 安全框架识别出要保护的报文时，就建立一个相应的IPsec IPsec IPsec IPsec 隧道并将其通过该隧道发送给对端。此处的 IPsec 隧道可以是提前手工配置或者由报文触发IKE 协商建立。这些 IPsec 隧道实际上就是两个 IPsec 对等体之间建立的 IPsec SA。由于 IPsec SA是单向的，因此出方向的报文由出方向的 保护，入方向的报文由入方向的 来保护。对端接SA SA收到报文后，首先对报文进行分析、识别，然后根据预先设定的安全策略对报文进行不同的处理（丢弃，解封装，或直接转发）。

##### 1.1.9 IPsec隧道保护匹配ACL的报文

将引用了 的 安全策略应用到接口上后，该接口上匹配 的报文将会受到 保护。
ACL IPsec ACL IPsec这里的接口包括串口、以太网接口等实际物理接口，以及 Tunnel、Virtual Template 等虚接口。
具体的保护机制如下：
只要接口发送的报文与该接口上应用的 安全策略中的 的 规则匹配，就会
• IPsec ACL permit受到出方向 IPsec SA 的保护并进行封装处理。

接口接收到目的地址是本机的 IPsec 报文时，首先根据报文头里携带的 SPI 查找本地的入方
•向 SA，由对应的入方向 进行解封装处理。解封装后的 报文若能与 的IPsec IPsec SA IP ACL permit 规则匹配上则采取后续处理，否则被丢弃。
目前，设备支持的数据流的保护方式包括以下三种：
• 标准方式：一条 IPsec 隧道保护一条数据流。ACL 中的每一个规则对应的数据流分别由一条单独创建的 IPsec 隧道来保护。缺省采用该方式。
• 聚合方式：一条 IPsec 隧道保护 ACL 中定义的所有数据流。ACL 中的所有规则对应的数据流只会由一条创建的 IPsec 隧道来保护。该方式仅用于和老版本的设备互通。
主机方式：一条 IPsec 隧道保护一条主机到主机的数据流。ACL 中的每一个规则对应的不同
•主机之间的数据流分别由一条单独创建的 隧道来保护。这种方式下，受保护的网段之间IPsec存在多条数据流的情况下，将会消耗更多的系统资源。

##### 1.1.10 IPsec隧道保护IPv6路由协议报文

将 IPsec 安全框架应用到某一 IPv6 路由协议（目前支持保护 OSPFv3、IPv6 BGP、RIPng 路由协议）后，设备产生的需要 保护的某一 路由协议的所有报文都要进行封装处理，而设备IPsec IPv6接收到的不受 IPsec 保护的以及解封装失败的业务协议报文都要被丢弃。
由于 IPsec 的密钥交换机制仅适用于两点之间的通信保护，在广播网络一对多的情形下，IPsec 无法实现自动交换密钥，同样，由于广播网络一对多的特性，要求各设备对于接收、发送的报文均使用相同的 参数（相同的 及密钥），因此该方式下必须手工配置用来保护 路由协议报文SA SPI IPv6的 IPsec SA。

##### 1.1.11 IPsec安全策略和IPsec安全框架

IPsec 安全策略和 IPsec 安全框架用于在两个对等体之间建立 IPsec 隧道，保护两个对等体之间需要被安全防护的报文。

###### 1. IPsec安全策略

一个 IPsec 安全策略是若干具有相同名字、不同顺序号的 IPsec 安全策略表项的集合，IPsec 安全策略被应用在接口上，用于控制对等体之间建立 IPsec 隧道，由 ACL 定义要保护的数据范围。IPsec安全策略主要定义了以下内容：
• 要保护的数据流的范围：由 ACL 定义。
• 对数据流实施何种保护：由 IPsec 安全提议定义。
• IPsec SA 的生成方式：手工方式、IKE 协商方式。
• 保护路径的起点或终点：即对等体的 IP 地址。
在同一个 IPsec 安全策略中，顺序号越小的 IPsec 安全策略表项优先级越高。当从一个接口发送数据时，接口将按照顺序号从小到大的顺序逐一匹配引用的 IPsec 安全策略中的每一条安全策略表项。
如果数据匹配上了某一条安全策略表项引用的 ACL，则停止匹配，并对其使用当前这条安全策略表项进行处理，即根据已经建立的 IPsec SA 或者触发 IKE 协商生成的 IPsec SA 对报文进行封装处理；
如果数据与所有安全策略表项引用的 ACL 都不匹配，则直接被正常转发， IPsec 不对数据加以保护。
应用了 IPsec 安全策略的接口收到数据报文时，对于目的地址是本机的 IPsec 报文，根据报文头里携带的 SPI 查找本地的 IPsec SA，并根据匹配的 IPsec SA 对报文进行解封装处理；解封装后的 IP报文若能与 的 规则匹配上则采取后续处理，否则被丢弃。
ACL permit

###### 2. IPsec安全框架

IPsec 安全框架（IPsec Profile）与 IPsec 安全策略类似，但不需要使用 ACL 指定要保护的数据流的范围。一个 IPsec 安全框架由名字唯一确定。IPsec 安全框架包括如下两种：
• 手工方式的 IPsec 安全框架：定义了对数据流进行 IPsec 保护所使用的安全提议，以及 SA 参数，应用于 路由协议中。
IPv6协商方式的 安全框架：定义了对数据流进行 保护所使用的安全提议，IKE
• IKE IPsec IPsec profile 和 SA 参数，应用于隧道接口上。

##### 1.1.12 IPsec反向路由注入功能

RRI（Reverse Route Injection，反向路由注入）功能是一种自动添加到达 IPsec VPN 私网静态路由的机制，可以实现为受 保护的流量自动添加静态路由的功能。在大规模组网中，这种自动IPsec添加静态路由的机制可以简化用户配置，减少在企业总部网关设备上配置静态路由的工作量，并且可以根据 IPsec SA 的创建和删除进行静态路由的动态增加和删除，增强了 IPsec VPN的可扩展性。
如 图 1-4 所示，某企业在企业分支与企业总部之间的所有流量通过IPsec进行保护，企业总部网关上需要配置静态路由，将总部发往分支的数据引到应用IPsec安全策略的接口上来。如果未配置RRI，当企业分支众多或者内部网络规划发生变化时，就需要同时增加或调整总部网关上的静态路由配置，该项工作量大且容易出现配置错误。
企业总部侧网关设备 GW 上配置 RRI 功能后，每一个 IPsec 隧道建立之后，GW 都会自动为其添加一条相应的静态路由。通过 RRI 创建的路由表项可以在路由表中查询到，其目的地址为受保护的对端网络，下一跳地址为 IPsec 隧道的对端地址，它使得发往对端的流量被强制通过 IPsec 保护并转发。
创建的静态路由和手工配置的静态路由一样，可以向内网设备进行广播，允许内网设备选择合RRI适的路由对 IPsec VPN 流量进行转发。也可以为 RRI 创建的静态路由配置优先级，从而更灵活地应用路由管理策略。例如：当设备上还有其他方式配置到达相同目的地的路由时，如果为它们指定相同的优先级，则可实现负载分担，如果指定不同的优先级，则可实现路由备份。同时，还可以通过修改静态路由的 Tag 值，使得设备能够在路由策略中根据 Tag 值对这些 RRI 生成的静态路由进行灵活的控制。

图1-4 IPsec VPN 总部-分支组网图unne l e c t I P s I P s e c t unne

##### 1.1.13 协议规范

与 IPsec 相关的协议规范有：
• RFC 2401：Security Architecture for the Internet Protocol
• RFC 2402：IP Authentication Header 2406：IP
• RFC Encapsulating Security Payload 4552：Authentication/Confidentiality
• RFC for OSPFv3

#### 1.2 FIPS相关说明

设备运行于 FIPS 模式时，本特性部分配置相对于非 FIPS 模式有所变化，具体差异请见本文相关描述。有关 FIPS 模式的详细介绍请参见“安全配置指导”中的“FIPS”。

#### 1.3 IPsec配置限制和指导

通常情况下，由于 协议采用 的 端口进行通信，IPsec 的 和 协议分别使用IKE UDP 500 AH ESP 51或 50 号协议来工作，因此为保障 IKE 和 IPsec 的正常运行，需要确保应用了 IKE 和 IPsec 配置的接口上没有禁止掉属于以上端口和协议的流量。

#### 1.4 配置IPsec隧道保护匹配ACL的报文

设备通过 ACL 来识别由 IPsec 隧道保护的流量时，受保护的流量只能是源地址或目的地址为本机的报文。例如：可配置 IPsec 隧道对设备发送给日志服务器的日志信息进行保护。ACL 中定义的匹配转发流量的规则不生效，IPsec 不会对设备转发的任何数据流和语音流进行保护。

##### 1.4.1 配置IPsec隧道保护匹配ACL的报文的配置任务简介

隧道保护匹配 的报文配置任务如下：
IPsec ACL配置ACL
(1)
配置IPsec安全提议
(2)
(3) 配置 IPsec 安全策略请选择以下一项任务进行配置：
配置手工方式的IPsec安全策略(cid:123)
配置IKE协商方式的IPsec安全策略(cid:123)
(4) 在接口上应用IPsec安全策略
(5) （可选）配置 IPsec 隧道保护匹配 ACL 的报文的辅助功能配置解封装后IPsec报文的ACL检查功能(cid:123)
配置IPsec抗重放功能(cid:123)
配置IPsec抗重放窗口和序号的同步功能(cid:123)
配置共享源接口IPsec安全策略(cid:123)
配置QoS预分类功能(cid:123)
设置IPsec隧道模式下封装后外层IP头的DF位(cid:123)
配置IPsec反向路由注入功能(cid:123)
配置全局IPsec SA生存时间和空闲超时功能(cid:123)
配置IPsec分片功能(cid:123)
配置本端允许建立IPsec隧道的最大数(cid:123)
(可选）配置 日志和告警功能
(6) IPsec配置IPsec报文日志信息记录功能(cid:123)
配置IPsec告警功能(cid:123)

##### 1.4.2 配置ACL

###### 1. ACL规则中关键字的使用

通过配置 来定义需要保护的数据流。在 应用中， 规则中的 关键字IPsec ACL IPsec ACL permit表示与之匹配的流量需要被 IPsec 保护，而 deny 关键字则表示与之匹配的流量不需要保护。一个ACL 中可以配置多条规则，首个与数据流匹配上的规则决定了对该数据流的处理方式。
在IPsec安全策略中定义的ACL既可用于过滤接口入方向数据流，也可用于过滤接口出方向数据流。
• 设备出入方向的数据流都使用 IPsec 安全策略中定义的 ACL 规则来做匹配依据。具体是，出方向的数据流正向匹配ACL规则，入方向的数据流反向匹配ACL规则。例如，对于应用于IPsec安全策略中的某 规则：rule ACL 0 permit ip source 1.1.1.0 0.0.0.255 destination
2.2.2.0 0.0.0.255，设备使用其正向过滤出方向上从 1.1.1.0/24 网段发往 2.2.2.0/24 网段的数据流，反向过滤入方向上从 2.2.2.0/24 网段发往 1.1.1.0/24 网段的数据流。
• 在出方向上，与 ACL的 permit 规则匹配的报文将被 IPsec保护，未匹配上任何规则或与 deny规则匹配上的报文将不被 保护。
IPsec

在入方向上，与 ACL 的 permit 规则匹配上的未被 IPsec 保护的报文将被丢弃；目的地址为
•本机的被 保护的报文将被进行解封装处理。缺省情况下解封装后的 报文若能与IPsec IP ACL的 permit 规则匹配上则采取后续处理，否则被丢弃。若解封装后 IPsec 报文的 ACL 检查功能处于关闭状态，则解封装后的 IP 报文不与 ACL 匹配，直接进行后续处理。
需要注意的是：
• 仅对确实需要 IPsec 保护的数据流配置 permit 规则，避免盲目地使用关键字 any。这是因为，在一个 permit 规则中使用 any 关键字就代表所有指定范围上出方向的流量都需要被IPsec 保护，所有对应入方向上被 IPsec 保护的报文将被接收并处理，入方向上未被 IPsec 保护的报文都将被丢弃。这种情况下，一旦入方向收到的某流量是未被 IPsec 保护的，那么该流量就会被丢弃，这会造成一些本不需要 IPsec 处理的流量丢失，影响正常的业务传输。
• 当一个安全策略下有多条优先级不同的安全策略表项时，合理使用 deny 规则。避免本应该与优先级较低的安全策略表项的 规则匹配而被 保护的出方向报文，因为先ACL permit IPsec与优先级较高的安全策略表项的 ACL deny 规则匹配上，而没有被 IPsec 保护，继而在接收端被丢弃。
下面是一个 deny 规则的错误配置示例。Router A 和 Router B 上分别配置如下所示的 IPsec 安全策略，当 Router A连接的 1.1.2.0/24网段用户访问 Router B连接的 3.3.3.0/24网段时，报文在 Router的应用了 安全策略 的出接口上优先与顺序号为 的安全策略表项匹配，并匹配上了A IPsec testa 1 IPv4 ACL 3000 的 rule 1，因此 Router A 认为它不需要 IPsec 保护，而未进行 IPsec 封装。该报文到达 Router B 后，在应用了 IPsec 安全策略 testb 的入接口上与 IPv4 ACL 3001 的 rule 0 匹配，并被判断为应该受 保护但未被保护的报文而丢弃。
IPsec Router A 上的关键配置如下：
acl advanced 3000 rule 0 permit ip source 1.1.1.0 0.0.0.255 destination 2.2.2.0 0.0.0.255 rule 1 deny ip acl advanced 3001 rule 0 permit ip source 1.1.2.0 0.0.0.255 destination 3.3.3.0 0.0.0.255 rule 1 deny ip \# ipsec policy testa 1 isakmp <---优先级高的安全策略表项security acl 3000 ike-profile aa transform-set 1 \# ipsec policy testa 2 isakmp <---优先级低的安全策略表项security acl 3001 ike-profile bb transform-set 1 Router B 上的关键配置如下：
acl advanced 3001 rule 0 permit ip source 3.3.3.0 0.0.0.255 destination 1.1.2.0 0.0.0.255 rule 1 deny ip \# ipsec policy testb 1 isakmp security acl 3001 ike-profile aa

transform-set 1为保证 Router A 连接的 1.1.2.0/24 网段用户访问 Router B 连接的 3.3.3.0/24 网段的报文可被正确处理，建议将 Router A 上的 IPv4 ACL 3000 中的 deny 规则删除。

###### 2. ACL规则的镜像配置

为保证IPsec对等体上能够成功建立SA，建议两端设备上用于IPsec的ACL配置为镜像对称，即保证两端定义的要保护的数据流范围的源和目的尽量对称。例如，图 1-5 中Router A和Router B上的ACL配置都是完全镜像对称的，因此用于保护主机Host A与主机Host C之间、子网Network 1 与子网Network 2 之间流量的SA均可成功建立。
图1-5 镜像 ACL 配置若IPsec对等体上的ACL配置非镜像，那么只有在一端的ACL规则定义的范围是另外一端的子集时，SA协商可以成功。如 图 1-6 所示，Router A上的ACL规则允许的范围（Host A->Host C）是Router B上ACL规则允许的范围（Network 1）的子集。
2->Network图1-6 非镜像 ACL 配置需要注意的是，在这种 ACL 配置下，并不是任何一端发起的 SA 协商都可以成功，仅当保护范围小（细粒度）的一端向保护范围大（粗粒度）的一端发起的协商才能成功，反之则 协商失败。这SA是因为，协商响应方要求协商发起方发送过来的数据必须在响应方可以接受的范围之内。其结果就是，从细粒度一端向粗粒度一端发送报文时，细粒度侧设备发起的 SA 协商可以成功，例如 Host C；从粗粒度一方向细粒度一方发送报文时，粗粒度侧设备发起的 协商不能成功，例A->Host SA如 Host C->Host A、Host C->Host B、Host D->Host A 等。

###### 1. 功能简介

##### 1.4.3 配置IPsec安全提议

功能简介
1.
IPsec 安全提议是 IPsec 安全策略的一个组成部分，它用于定义 IPsec 需要使用的安全协议、加密/认证算法以及封装模式，为 协商 提供各种安全参数。
IPsec SA

###### 2. 配置限制和指导

• 可对 IPsec 安全提议进行修改，但对已协商成功的 IPsec SA，新修改的安全提议并不起作用，
即仍然使用原来的安全提议，只有新协商的 SA 使用新的安全提议。若要使修改对已协商成功
的 IPsec SA 生效，则需要执行 reset ipsec sa 命令。
• FIPS 模式下，若采用了 ESP 安全协议，则必须同时配置 ESP 加密算法和 ESP 认证算法。
• 传输模式必须应用于数据流的源地址和目的地址与 IPsec 隧道两端地址相同的情况下；若要配
置应用于 路由协议的手工方式的安全框架，则该安全框架引用的安全提议仅支持传输模
IPv6
式的封装模式。
• IKEv1 协商时发起方的 PFS 强度必须大于或等于响应方的 PFS 强度，否则协商会失败。IKEv2
不受该限制。不配置 PFS 特性的一端，按照对端的 PFS 特性要求进行 IKE 协商。
• 可以使用命令为一个安全协议指定多个认证或者加密算法，算法优先级以配置顺序为准。
• 以下这些算法只适用于 IKEv2 协商：
表1-1 协商适用的算法
IKEv2
参数 取值
aes-ctr-128/aes-ctr-192/aes-ctr-256
camellia-cbc-128/camellia-cbc-192/camellia-cbc-2
加密算法
gmac-128/gmac-192/gmac-256/
gcm-128/gcm-192/gcm-256
aes-xcbc-mac
认证算法
PFS（Perfect Secrecy，完 dh-group19
Forward
善的前向安全性）算法
dh-group20

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 创建 IPsec 安全提议，并进入 IPsec 安全提议视图。
ipsec transform-set transform-set-name
(3) 配置 IPsec 安全提议采用的安全协议。
protocol { ah | ah-esp | esp }
缺省情况下，采用 ESP 安全协议。
(4) 配置协议（esp 或 ah-esp）采用的加密算法。
（非 FIPS 模式）

esp encryption-algorithm { 3des-cbc | aes-cbc-128 | aes-cbc-192 | aes-cbc-256 | aes-ctr-128 | aes-ctr-192 | aes-ctr-256 | camellia-cbc-128 | camellia-cbc-192 | camellia-cbc-256 | des-cbc | gmac-128 | gmac-192 | gmac-256 | gcm-128 | gcm-192 | gcm-256 | null } *缺省情况下，ESP 协议没有采用任何加密算法。
非 ESP 协议，请忽略本步骤。
（FIPS 模式）
esp encryption-algorithm { aes-cbc-128 | aes-cbc-192 | aes-cbc-256 | aes-ctr-128 | aes-ctr-192 | aes-ctr-256 | gmac-128 | gmac-192 | gmac-256 | gcm-128 | gcm-192 | gcm-256 } *缺省情况下，ESP 协议没有采用任何加密算法。
非 协议，请忽略本步骤。
ESP
(5) 配置协议（esp 或 ah-esp）采用的认证算法。
（非 FIPS 模式）
esp authentication-algorithm { aes-xcbc-mac | md5 | sha1 | sha256 | sha384 | sha512 } *缺省情况下，ESP 协议没有采用任何认证算法。
非 协议，请忽略本步骤。
ESP认证算法仅适用于 协商。
aes-xcbc-mac IKEv2（FIPS 模式）
esp authentication-algorithm { sha1 | sha256 | sha384 | sha512 } *缺省情况下，ESP 协议没有采用任何认证算法。
非 ESP 协议，请忽略本步骤。
(6) 配置协议（ah 或 ah-esp）采用的认证算法。
（非 FIPS 模式）
ah authentication-algorithm { aes-xcbc-mac | md5 | sha1 | sha256 | sha384 | sha512 } *缺省情况下，AH 协议没有采用任何认证算法。
采用 ESP 协议时，请忽略本步骤。
aes-xcbc-mac 认证算法仅适用于 IKEv2 协商。
（FIPS 模式）
ah authentication-algorithm { sha1 | sha256 | sha384 | sha512 } *缺省情况下，AH 协议没有采用任何认证算法。
采用 ESP 协议时，请忽略本步骤。
(7) 配置安全协议对 IP 报文的封装模式。
encapsulation-mode { transport | tunnel }缺省情况下，安全协议采用隧道模式对 IP 报文进行封装。
(8) （可选）配置使用 IPsec 安全策略发起协商时使用 PFS 特性。
（非 FIPS 模式）

pfs { dh-group1 | dh-group2 | dh-group5 | dh-group14 | dh-group24 | dh-group19 | dh-group20 }（FIPS 模式）
pfs { dh-group14 | dh-group19 | dh-group20 }缺省情况下，使用 安全策略发起协商时不使用 特性。
IPsec PFS有关 PFS（Perfect Secrecy，完善的前向安全性）功能的详细介绍请参见“安全配Forward置指导”中的“IKE”。
(9) （可选）开启 ESN 功能。
esn enable [ both ]缺省情况下，ESN 功能处于关闭状态。

##### 1.4.4 配置手工方式的IPsec安全策略

###### 1. 配置限制和指导

为保证 SA 能够成功生成，IPsec 隧道两端的配置必须符合以下要求：
安全策略引用的 安全提议应采用相同的安全协议、加密/认证算法和报文封装模式。
• IPsec IPsec当前端点的 对端地址应与对端应用 安全策略的接口的主 地址保持一致；当前
• IPv4 IPsec IPv4端点的 IPv6 对端地址应与对端应用 IPsec 安全策略的接口的第一个 IPv6 地址保持一致。
• 应分别设置 inbound 和 outbound 两个方向的 IPsec SA 参数，且保证每一个方向上的 IPsec SA 的唯一性：对于出方向 IPsec SA，必须保证三元组（对端 IP 地址、安全协议、SPI）唯一；
对于入方向 IPsec SA，必须保证 SPI 唯一。
本端和对端 IPsec SA 的 SPI 及密钥必须是完全匹配的。即，本端的入方向 IPsec SA 的 SPI
•及密钥必须和对端的出方向 的 及密钥相同；本端的出方向 的 及IPsec SA SPI IPsec SA SPI密钥必须和对端的入方向 IPsec SA 的 SPI 及密钥相同。
• 两端 IPsec SA 使用的密钥应当以相同的方式输入，即如果一端以字符串方式输入密钥，另一端必须也以字符串方式输入密钥。如果先后以不同的方式输入了密钥，则最后设定的密钥有效。
对于 ESP 协议，以字符串方式输入密钥时，系统会自动地同时生成认证算法的密钥和加密算
•法的密钥。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 创建一条手工方式的 IPsec 安全策略，并进入 IPsec 安全策略视图。
ipsec { ipv6-policy | policy } policy-name seq-number manual
(3) （可选）配置 IPsec 安全策略的描述信息。
description text
缺省情况下，无描述信息。
指定 安全策略引用的 ACL。
(4) IPsec
security acl [ ipv6 ] { acl-number | name acl-name }
缺省情况下，IPsec 安全策略没有引用 ACL。

一条安全策略只能引用一个 ACL。
(5) 指定 IPsec 安全策略所引用的安全提议。
transform-set transform-set-name缺省情况下，IPsec 安全策略没有引用 IPsec 安全提议。
一条手工方式的 IPsec 安全策略只能引用一个安全提议。
(6) 指定 IPsec 隧道的对端 IP 地址。
remote-address { ipv4-address | ipv6 ipv6-address }缺省情况下，未指定 IPsec 隧道的对端地址。
(7) 配置 IPsec SA 的入方向 SPI。
sa spi inbound { ah | esp } spi-number缺省情况下，不存在 IPsec SA 的入方向 SPI。
(8) 配置 IPsec SA 的出方向 SPI。
sa spi outbound { ah | esp } spi-number缺省情况下，不存在 IPsec SA 的出方向 SPI。
(9) 配置 IPsec SA 使用的密钥。
配置 协议的认证密钥（以十六进制方式输入）。
AH (cid:123)
sa hex-key authentication { inbound | outbound } ah { cipher | simple } string配置 AH 协议的认证密钥（以字符串方式输入）。
(cid:123)
sa string-key { inbound | outbound } ah { cipher | simple } string配置 ESP 协议的认证密钥和加密密钥（以字符串方式输入）。
(cid:123)
sa string-key { inbound | outbound } esp { cipher | simple } string配置 协议的认证密钥（以十六进制方式输入）。
ESP (cid:123)
sa hex-key authentication { inbound | outbound } esp { cipher | simple } string配置 ESP 协议的加密密钥（以十六进制方式输入）。
(cid:123)
sa hex-key encryption { inbound | outbound } esp { cipher | simple } string缺省情况下，未配置 IPsec SA 使用的密钥。
根据本安全策略引用的安全提议中指定的安全协议，配置 AH 协议或 ESP 协议的密钥，或者两者都配置。

##### 1.4.5 配置IKE协商方式的IPsec安全策略

###### 1. 配置方式简介

IKE 协商方式的 IPsec 安全策略有以下两种配置方式：
• 直接配置 IPsec 安全策略：在安全策略视图中定义需要协商的各参数；
• 引用 IPsec 安全策略模板配置 IPsec 安全策略：首先在 IPsec 安全策略模板中定义需要协商的各参数，然后通过引用 安全策略模板创建一条 安全策略。应用了该类 安全IPsec IPsec IPsec

策略的接口不能发起协商，仅可以响应远端设备的协商请求。由于 IPsec 安全策略模板中未定义的可选参数由发起方来决定，而响应方会接受发起方的建议，因此这种方式适用于通信对端（例如对端的 IP 地址）未知的情况下，允许这些对端设备向本端设备主动发起协商。
IPsec 安全策略模板与直接配置的 IKE 协商方式的 IPsec 安全策略中可配置的参数类似，但是配置较为简单，除了 IPsec 安全提议和 IKE profile 之外的其它参数均为可选。应用了引用 IPsec 安全策略模板配置的 安全策略的接口不能发起协商，仅可以响应远端设备的协商请求。IPsec 安全IPsec策略模板中未定义的可选参数由发起方来决定，而响应方会接受发起方的建议，例如 IPsec 安全策略模板下的用于定义保护对象范围的 ACL 是可选的，该参数在未配置的情况下，相当于支持最大范围的保护，即完全接受协商发起端的 ACL 设置。

###### 2. 配置限制和指导

隧道两端的配置必须符合以下要求：
IPsec安全策略引用的 安全提议中应包含具有相同的安全协议、认证/加密算法和报文封
• IPsec IPsec装模式的 IPsec 安全提议。
• IPsec 安全策略引用的 IKE profile 参数相匹配。
• 一条 IKE 协商方式的 IPsec 安全策略中最多可以引用六个 IPsec 安全提议。IKE 协商过程中，IKE 将会在隧道两端配置的 IPsec 安全策略中查找能够完全匹配的 IPsec 安全提议。如果 IKE在两端找不到完全匹配的 IPsec 安全提议，则 SA 不能协商成功，需要被保护的报文将被丢弃。
• IKE 协商的发起方必须配置 IPsec 隧道的对端地址，响应方可选配，且当前端点的对端地址与对端的本端地址应保持一致。
对于 协商建立的 SA，遵循以下原则：
IKE IPsec采用隧道两端设置的 IPsec SA 生存时间中较小者。
•可同时存在基于时间和基于流量两种方式的 IPsec SA 生存时间，只要到达指定的时间或指定
•的流量，IPsec 就会老化。
SA一条 安全策略只能引用一个 或者一个 profile。同时引用时
• IPsec IKEv1 profile IKEv2 IKEv2 profile 的优先级高于 IKEv1 profile 的优先级。
IKEv1 profile 的相关配置请参见“安全配置指导”中的“IKE”。
IKEv2 profile 的相关配置请参见“安全配置指导”中的“IKEv2”。

###### 3. 直接配置IKE协商方式的IPsec安全策略

(1) 进入系统视图。
system-view
(2) 创建一条 IKE 协商方式的 IPsec 安全策略，并进入 IPsec 安全策略视图。
ipsec { ipv6-policy | policy } policy-name seq-number isakmp
(3) （可选）配置 IPsec 安全策略的描述信息。
description text
缺省情况下，无描述信息。
指定 安全策略引用的 。
(4) IPsec ACL
security acl [ ipv6 ] { acl-number | name acl-name } [ aggregation |
per-host ]
缺省情况下，IPsec 安全策略没有指定 ACL。

一条 IPsec 安全策略只能引用一个 ACL。
(5) 指定 IPsec 安全策略引用的 IPsec 安全提议。
transform-set transform-set-name&<1-6>缺省情况下，IPsec 安全策略没有引用 IPsec 安全提议。
(6) 指定 IPsec 安全策略引用的 IKE profile 或者 IKEv2 profile。
指定 IPsec 安全策略引用的 IKE profile。
(cid:123)
ike-profile profile-name缺省情况下，IPsec 安全策略没有引用 IKE profile。
指定 IPsec 安全策略引用的 IKEv2 profile。
(cid:123)
ikev2-profile profile-name缺省情况下，IPsec 安全策略没有引用 IKEv2 profile。
(7) 指定 IPsec 隧道的本端 IP 地址。
local-address { ipv4-address | ipv6 ipv6-address }缺省情况下，IPsec 隧道的本端 IPv4 地址为应用 IPsec 安全策略的接口的主 IPv4 地址，本端IPv6 地址为应用 IPsec 安全策略的接口的第一个 IPv6 地址。
此处指定的 IPsec 隧道本端 IP 地址必须与 IKE 使用的标识本端身份的 IP 地址一致。在 VRRP组网环境中，IPsec 隧道本端 IP 地址为应用 IPsec 安全策略接口所在备份组的虚拟 IP 地址。
(8) 指定 IPsec 隧道的对端 IP 地址。
remote-address { [ ipv6 ] host-name | ipv4-address | ipv6 ipv6-address }缺省情况下，未指定 IPsec 隧道的对端 IP 地址。
(9) （可选）配置 IPsec SA 的生存时间或空闲超时时间。
配置 IPsec SA 的生存时间。
(cid:123)
sa duration { time-based seconds | traffic-based kilobytes }缺省情况下，IPsec 安全策略下的 IPsec SA 生存时间为当前全局的 IPsec SA 生存时间。
配置 IPsec SA 的空闲超时时间。
(cid:123)
sa idle-time seconds缺省情况下，IPsec 安全策略下的 IPsec SA 空闲超时时间为当前全局的 IPsec SA 空闲超时时间。
(10) （可选）开启 TFC（Traffic Flow Confidentiality）填充功能。
tfc enable缺省情况下，TFC 填充功能处于关闭状态。

###### 4. 引用IPsec安全策略模板配置IKE协商方式的IPsec安全策略

(1) 进入系统视图。
system-view
(2) 创建一个 IPsec 安全策略模板，并进入 IPsec 安全策略模板视图。
ipsec { ipv6-policy-template | policy-template } template-name
seq-number
(3) （可选）配置 IPsec 安全策略模板的描述信息。

description text缺省情况下，无描述信息。
(4) （可选）指定 IPsec 安全策略模板引用的 ACL。
security acl [ ipv6 ] { acl-number | name acl-name } [ aggregation | per-host ]缺省情况下，IPsec 安全策略模板没有指定 ACL。
一条 IPsec 安全策略模板只能引用一个 ACL。
(5) 指定 IPsec 安全策略模板引用的安全提议。
transform-set transform-set-name&<1-6>缺省情况下 IPsec 安全策略模板没有引用 IPsec 安全提议。
(6) 指定 IPsec 安全策略模板引用的 IKE profile 或者 IKEv2 profile。
指定 IPsec 安全策略模板引用的 IKE profile。
(cid:123)
ike-profile profile-name缺省情况下，IPsec 安全策略模板没有引用 IKE profile。
不能引用已经被其它 IPsec 安全策略或 IPsec 安全策略模板引用的 IKE profile。
指定 IPsec 安全策略模板引用的 IKEv2 profile。
(cid:123)
ikev2-profile profile-name缺省情况下，IPsec 安全策略模板没有引用 IKEv2 profile。
(7) 指定 IPsec 隧道的本端 IP 地址和对端 IP 地址。
指定 IPsec 隧道的本端 IP 地址。
(cid:123)
local-address { ipv4-address | ipv6 ipv6-address }缺省情况下，IPsec 隧道的本端 地址为应用 安全策略的接口的主 地址，本IPv4 IPsec IPv4端 IPv6 地址为应用 IPsec 安全策略的接口的第一个 IPv6 地址。
IPsec 隧道本端 IP 地址必须与 IKE 对等体使用的标识本端身份的 IP 地址一致。VRRP 组网环境中， IPsec 隧道本端 IP 地址为应用 IPsec 安全策略的接口所在备份组的虚拟 IP 地址。
指定 IPsec 隧道的对端 IP 地址。
(cid:123)
remote-address { [ ipv6 ] host-name | ipv4-address | ipv6 ipv6-address }缺省情况下，未指定 IPsec 隧道的对端 IP 地址。
(8) （可选）配置 IPsec SA 的生存时间或者空闲超时时间。
配置 IPsec SA 的生存时间。
(cid:123)
sa duration { time-based seconds | traffic-based kilobytes }缺省情况下，IPsec 安全策略模板下的 IPsec SA 生存时间为当前全局的 IPsec SA 生存时间。
配置 IPsec SA 的空闲超时时间。
(cid:123)
sa idle-time seconds缺省情况下，IPsec 安全策略模板下的 IPsec SA 空闲超时时间为当前全局的 IPsec SA 空闲超时时间。
（可选）开启 TFC（Traffic Confidentiality）填充功能。
(9) Flow

tfc enable缺省情况下，TFC 填充功能处于关闭状态。
(10) 退回系统视图。
quit
(11) 引用安全策略模板创建一条 IKE 协商方式的安全策略。
ipsec { ipv6-policy | policy } policy-name seq-number isakmp template template-name

##### 1.4.6 在接口上应用IPsec安全策略

###### 1. 配置限制与指导

为使定义的 生效，应在每个要加密的数据流和要解密的数据流所在接口上应用一个IPsec SA IPsec安全策略，以对数据进行保护。当取消 IPsec 安全策略在接口上的应用后，此接口便不再具有 IPsec的安全保护功能。
IKE 方式的 IPsec 安全策略可以应用到多个接口上，但建议只应用到一个接口上；手工方式的 IPsec安全策略只能应用到一个接口上。

###### 2. 配置步骤

进入系统视图。
(1)
system-view进入接口视图。
(2)
interface interface-type interface-number
(3) 应用 IPsec 安全策略。
ipsec apply { ipv6-policy | policy } policy-name缺省情况下，接口上没有应用 IPsec 安全策略。
一个接口下最多只能应用一个 IPv4/IPv6 类型的 IPsec 安全策略，但可以同时应用一个 IPv4类型的 安全策略和一个 类型的 安全策略。
IPsec IPv6 IPsec
(4) 配置在指定 slot 上处理当前接口的流量。
service slot slot-number缺省情况下，未指定处理当前接口流量的 slot ，业务处理在接收报文的 slot 上进行。
仅在全局逻辑接口（例如 VLAN 接口）上应用 IKE 协商方式的 IPsec 安全策略，且全局开启了 抗重放检测功能时，必选。
IPsec

##### 1.4.7 配置解封装后IPsec报文的ACL检查功能

###### 1. 功能简介

在隧道模式下，接口入方向上解封装的 报文的内部 头有可能不在当前 安全策略引用IPsec IP IPsec的 ACL 的保护范围内，如网络中一些恶意伪造的攻击报文就可能有此问题，所以设备需要重新检查解封装后的报文的 IP 头是否在 ACL 保护范围内。开启该功能后可以保证 ACL 检查不通过的报文被丢弃，从而提高网络安全性。

###### 3. 配置步骤

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 开启解封装后 IPsec 报文的 ACL 检查功能。
ipsec decrypt-check enable
缺省情况下，解封装后 IPsec 报文的 ACL 检查功能处于开启状态。

##### 1.4.8 配置IPsec抗重放功能

###### 1. 功能简介

重放报文，通常是指设备再次接收到的已经被 IPsec 处理过的报文。IPsec 通过滑动窗口（抗重放窗口）机制检测重放报文。AH 和 ESP 协议报文中带有序列号，如果收到的报文的序列号与已经解封装过的报文序列号相同，或收到的报文的序列号出现得较早，即已经超过了抗重放窗口的范围，则认为该报文为重放报文。
对重放报文的解封装无意义，并且解封装过程涉及密码学运算，会消耗设备大量的资源，导致业务可用性下降，造成了拒绝服务攻击。通过开启 IPsec 抗重放检测功能，将检测到的重放报文在解封装处理之前丢弃，可以降低设备资源的消耗。
在某些特定环境下，业务数据报文的接收顺序可能与正常的顺序差别较大，虽然并非有意的重放攻击，但会被抗重放检测认为是重放报文，导致业务数据报文被丢弃，影响业务的正常运行。因此，这种情况下就可以通过关闭 IPsec 抗重放检测功能来避免业务数据报文的错误丢弃，也可以通过适当地增大抗重放窗口的宽度，来适应业务正常运行的需要。

###### 2. 配置限制和指导

只有 IKE 协商的 IPsec SA 才能够支持抗重放检测，手工方式生成的 IPsec SA 不支持抗重放
•检测。因此该功能开启与否对手工方式生成的 没有影响。
IPsec SA使用较大的抗重放窗口宽度会引起系统开销增大，导致系统性能下降，与抗重放检测用于降
•低系统在接收重放报文时的开销的初衷不符，因此建议在能够满足业务运行需要的情况下，使用较小的抗重放窗口宽度。
• 一般情况下，IRF 系统中设备直接在接收报文的 slot 上进行业务处理。但 IPsec 抗重放检测要求同一个 Vlan 接口发送和接收的流量必须在同一个 slot 上进行处理，此时需要在 Vlan 接口下通过 命令指定转发当前接口流量的 。有关于 命令的详细介绍，请参考“二service slot service层技术-以太网交换命令参考”中的“VLAN”。
• IPsec 抗重放检测功能缺省是开启的，是否关闭该功能请根据实际需求慎重使用。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 开启 IPsec 抗重放检测功能。
ipsec anti-replay check缺省情况下，IPsec 抗重放检测功能处于开启状态。
(3) 配置 IPsec 抗重放窗口宽度。
ipsec anti-replay window width

###### 1. 配置简介

缺省情况下，IPsec 抗重放窗口宽度为 64。

##### 1.4.9 配置IPsec抗重放窗口和序号的同步功能

###### 1. 功能简介

抗重放窗口和序号的同步功能是指，以指定的报文间隔将接口上 入方向抗重放窗口的IPsec IPsec左侧值和出方向 IPsec报文的抗重放序号进行备份。当配置了防重放窗口和序号的同步间隔的 IPsec安全策略被应到接口上时，若 IPsec 冗余备份功能处于开启状态，则可以保证主备切换时 IPsec 流量不间断和抗重放保护不间断。

###### 2. 配置步骤

进入系统视图。
(1)
system-view开启 冗余备份功能。
(2) IPsec ipsec redundancy enable缺省情况下，IPsec 冗余备份功能处于关闭状态。
(3) 进入 IPsec 安全策略视图或者 IPsec 安全策略模板视图。
进入 IPsec 安全策略视图。
(cid:123)
ipsec { ipv6-policy | policy } policy-name seq-number [ isakmp | manual ]进入 安全策略模板视图。
IPsec (cid:123)
ipsec { ipv6-policy-template | policy-template } template-name seq-number配置防重放窗口和序号的同步间隔。
(4)
redundancy replay-interval inbound inbound-interval outbound outbound-interval缺省情况下，同步入方向防重放窗口的报文间隔为 1000 个报文，同步出方向 IPsec SA 防重放序号的报文间隔为 100000 个报文。

##### 1.4.10 配置共享源接口IPsec安全策略

配置简介
1.
为了提高网络的可靠性，通常核心设备到 ISP（Internet Service Provider，互联网服务提供商）都会有两条出口链路，它们互为备份或者为负载分担的关系。由于在不同的接口上应用安全策略时，各个接口将分别协商生成 IPsec SA。因此，则在主备链路切换时，接口状态的变化会触发重新进行IKE 协商，从而导致数据流的暂时中断。这种情况下，两个接口上的 IPsec SA 就需要能够平滑切换。
通过将一个 IPsec 安全策略与一个源接口绑定，使之成为共享源接口 IPsec 安全策略，可以实现主备链路切换时受 IPsec 保护的业务流量不中断。具体机制为：应用相同 IPsec 安全策略的多个物理接口共同使用一个指定的源接口（称为共享源接口）协商 ，当这些物理接口对应的链路切IPsec SA换时，如果该源接口的状态不变化，就不会删除该接口协商出的 IPsec SA，也不需要重新触发 IKE协商，各物理接口继续使用已有的 IPsec SA 保护业务流量。

###### 2. 配置限制和指导

• 只有 IKE 协商方式的 IPsec 安全策略才能配置为 IPsec 共享源接口安全策略。
• 一个 IPsec 安全策略只能与一个源接口绑定。
• 一个源接口可以同时与多个 IPsec 安全策略绑定。
• 删除与共享源接口 IPsec 安全策略绑定的共享源接口时，将使得该共享源接口 IPsec 安全策略
恢复为普通 IPsec 安全策略。
• 若一个 IPsec 安全策略为共享源接口 IPsec 安全策略，但该 IPsec 安全策略中未指定隧道本端
地址，则 IKE 将使用共享源接口地址作为 IPsec 隧道的本端地址进行 IKE 协商；如果共享源
接口 安全策略中指定了隧道本端地址，则将使用指定的隧道本端地址进行 协商。
IPsec IKE

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置 IPsec 安全策略为 IPsec 共享源接口安全策略。
ipsec { ipv6-policy | policy } policy-name local-address interface-type
interface-number
缺省情况下，IPsec 安全策略不是共享源接口 IPsec 安全策略，即未将 IPsec 安全策略与任何
源接口绑定。

##### 1.4.11 配置QoS预分类功能

###### 1. 功能简介

当在接口上同时应用了 IPsec 安全策略与 QoS 策略时，缺省情况下，QoS 使用封装后报文的外层头信息来对报文进行分类。但如果希望 基于被封装报文的原始 头信息对报文进行分类，IP QoS IP则需要配置 QoS 预分类功能来实现。

###### 2. 配置限制和指导

• 若在接口上同时配置 IPsec 和 QoS，同一个 IPsec SA 保护的数据流如果被 QoS 分类进入不
同队列，会导致部分报文发送乱序。由于 IPsec 具有抗重放功能，IPsec 入方向上对于抗重放
窗口之外的报文会进行丢弃，从而导致丢包现象。因此当 IPsec 与 QoS 配合使用时，必须保
证 IPsec 分类与 QoS 分类规则配置保持一致。
• IPsec 的分类规则完全由引用的 ACL 规则确定，QoS 策略及 QoS 分类的相关介绍请参见“ACL
和 QoS 配置指导”中的“QoS 配置方式”。

###### 3. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入 IPsec 安全策略视图或者 IPsec 安全策略模板视图。
进入 IPsec 安全策略视图。
(cid:123)
ipsec { ipv6-policy | policy } policy-name seq-number [ isakmp | manual ]进入 安全策略模板视图。
IPsec (cid:123)

ipsec { ipv6-policy-template | policy-template } template-name seq-number开启 预分类功能。
(3) QoS qos pre-classify缺省情况下，QoS 预分类功能处于关闭状态。

##### 1.4.12 设置IPsec隧道模式下封装后外层IP头的DF位

###### 1. 功能简介

报文头中的 DF（Don’t Fragment，不分片）位用于控制报文是否允许被分片。在隧道模式下，IPsec IP会在原始报文外封装一个新的 IP 头，称为外层 IP 头。IPsec 的 DF 位设置功能允许用户设置 IPsec封装后的报文外层 IP 头的 DF 位，并支持以下三种设置方式：
• clear：表示清除外层 IP 头的 DF 位，IPsec 封装后的报文可被分片。
• set：表示设置外层 IP 头的 DF 位，IPsec 封装后的报文不能被分片。
• copy ：表示外层 IP 头的 DF 位从原始报文 IP 头中拷贝。
封装后外层 IP 头的 DF 位可以在接口视图和系统视图下分别配置，接口视图下的配置优先级高。如果接口下未设置外层 IP 头的 DF 位，则按照系统视图下的全局配置来决定如何设置封装后外层 IP头的 位。
DF

###### 2. 配置限制和指导

• 该功能仅在 IPsec 的封装模式为隧道模式时有效，仅用于设置 IPsec 隧道模式封装后的外层 IP
头的 DF 位，原始报文 IP 头的 DF 位不会被修改。
• 如果有多个接口应用了共享源接口安全策略，则这些接口上必须使用相同的 DF 位设置。
• 转发报文时对报文进行分片、重组，可能会导致报文的转发延时较大。若设置了封装后 IPsec
报文的 DF 位，则不允许对 IPsec 报文进行分片，可以避免引入分片延时。这种情况下，要求
报文转发路径上各个接口的 大于 报文长度，否则，会导致 报文被丢
IPsec MTU IPsec IPsec
弃。如果无法保证转发路径上各个接口的 MTU 大于 IPsec 报文长度，则建议清除 DF 位。

###### 3. 在接口下设置IPsec封装后外层IP头的DF位

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 为当前接口设置 IPsec 封装后外层 IP 头的 DF 位。
ipsec df-bit { clear | copy | set }
缺省情况下，接口下未设置 IPsec 封装后外层 IP 头的 DF 位，采用全局设置的 DF 位。

###### 4. 全局设置IPsec封装后外层IP头的DF位

(1) 进入系统视图。
system-view
(2) 为所有接口设置 IPsec 封装后外层 IP 头的 DF 位。
ipsec global-df-bit { clear | copy | set }

##### 1.5.1 配置IPsec隧道保护IPv6路由协议配置任务简介

缺省情况下，IPsec 封装后外层 IP 头的 DF 位从原始报文 IP 头中拷贝。

##### 1.4.13 配置IPsec反向路由注入功能

###### 1. 配置限制和指导

开启 功能时，会删除相应 安全策略协商出的所有 SA。当有新的流量触发生成RRI IPsec IPsec IPsec SA 时，根据新协商的 IPsec 生成路由信息。
关闭 RRI 功能时，会删除相应 IPsec 安全策略协商出的所有 IPsec SA。
生成的静态路由随 的创建而创建，随 的删除而删除。
RRI IPsec SA IPsec SA功能在隧道模式和传输模式下都支持。
RRI若修改了 生成的静态路由的优先级或 属性，则会删除由相应 安全策略建立的RRI Tag IPsec IPsec SA 和已添加的静态路由，修改后的属性值在下次生成 IPsec SA 且添加静态路由时生效。
在 RRI 功能开启的情况下，对于与未指定目的 IP 地址的 ACL 规则相匹配的报文流触发协商出的IPsec SA，设备并不会为其自动生成一条静态路由。因此，如果 IPsec 安全策略/IPsec 安全策略模板引用了此类型的 ACL 规则，则需要通过手工配置一条到达对端受保护网络的静态路由。

###### 2. 配置步骤

进入系统视图。
(1)
system-view进入 安全策略视图或者 安全策略模板视图。
(2) IPsec IPsec进入 安全策略视图。
IPsec (cid:123)
ipsec { policy | ipv6-policy } policy-name seq-number isakmp进入 IPsec 安全策略模板视图。
(cid:123)
ipsec { ipv6-policy-template | policy-template } template-name seq-number开启 反向路由注入功能。
(3) IPsec reverse-route dynamic缺省情况下，IPsec 反向路由注入功能处于关闭状态。
(4) （可选）配置 IPsec 反向路由功能生成的静态路由的优先级。
reverse-route preference number缺省情况下，IPsec 反向路由注入功能生成的静态路由的优先级为 60。
(5) （可选）配置 IPsec 反向路由功能生成的静态路由的 Tag 值。
reverse-route tag tag-value缺省情况下，IPsec 反向路由注入功能生成的静态路由的 tag 值为 0。

#### 1.5 配置IPsec隧道保护IPv6路由协议

配置 隧道保护 路由协议配置任务简介
1.5.1 IPsec IPv6 IPsec 隧道保护 IPv6 路由协议配置任务如下：
(1) 配置IPsec安全提议

(2) 配置手工方式的IPsec安全框架
(3) 在IPv6 路由协议上应用IPsec安全框架
(4) （可选）配置IPsec分片功能
(5) （可选）配置本端允许建立IPsec隧道的最大数
(6) （可选）配置IPsec报文日志信息记录功能
(7) （可选）配置IPsec告警功能

##### 1.5.2 配置手工方式的IPsec安全框架

手工方式的 安全框架定义了对数据流进行 保护所使用的安全提议，以及 的 SPI、IPsec IPsec SA SA 使用的密钥。

###### 1. 配置限制和指导

IPsec 隧道两端的配置必须符合以下要求：
• IPsec 安全框架引用的 IPsec 安全提议应采用相同的安全协议、加密/认证算法和报文封装模式。
• 本端出方向 IPsec SA 的 SPI 和密钥必须和本端入方向 IPsec SA 的 SPI 和密钥保持一致。
• 同一个范围内的、所有设备上的 IPsec SA 的 SPI 和密钥均要保持一致。该范围与协议相关：
对于 OSPFv3，是 OSPFv3 邻居之间或邻居所在的区域；对于 RIPng，是 RIPng 直连邻居之间或邻居所在的进程；对于 BGP，是 邻居之间或邻居所在的一个组。
BGP两端 使用的密钥应当以相同的方式输入，即如果一端以字符串方式输入密钥，另一
• IPsec SA端必须也以字符串方式输入密钥。如果先后以不同的方式输入了密钥，则最后设定的密钥有效。
• 对于 ESP 协议，以字符串方式输入密钥时，系统会自动地同时生成认证算法的密钥和加密算法的密钥。

###### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 创建一个手工方式的 IPsec 安全框架，并进入 IPsec 安全框架视图。
ipsec profile profile-name manual进入已创建的 IPsec 安全框架时，可以不指定协商方式 manual。
(3) （可选）配置 IPsec 安全框架的描述信息。
description text缺省情况下，无描述信息。
(4) 指定 IPsec 安全框架引用的 IPsec 安全提议。
transform-set transform-set-name缺省情况下，IPsec 安全框架没有引用 IPsec 安全提议。
要引用的 IPsec 安全提议所采用的封装模式必须为传输模式。
(5) 配置 IPsec SA 的 SPI。
sa spi { inbound | outbound } { ah | esp } spi-number缺省情况下，未配置 IPsec SA 的 SPI。

(6) 配置 IPsec SA 使用的密钥。
配置 AH 协议的认证密钥（以十六进制方式输入）。
(cid:123)
sa hex-key authentication { inbound | outbound } ah { cipher | simple }
string
配置 协议的认证密钥（以字符串方式输入）。
AH
(cid:123)
sa string-key { inbound | outbound } ah { cipher | simple } string
配置 ESP 协议的认证密钥和加密密钥（以字符串方式输入）。
(cid:123)
sa string-key { inbound | outbound } esp { cipher | simple } string
配置 ESP 协议的认证密钥（以十六进制方式输入）。
(cid:123)
sa hex-key authentication { inbound | outbound } esp { cipher | simple }
string
配置 协议的加密密钥（以十六进制方式输入）。
ESP
(cid:123)
sa hex-key encryption { inbound | outbound } esp { cipher | simple }
string
缺省情况下，未配置 IPsec SA 使用的密钥。
根据本安全框架引用的安全提议中指定的安全协议，配置 协议或 协议的密钥，或者
AH ESP
两者都配置。

##### 1.5.3 在IPv6路由协议上应用IPsec安全框架

有关在 IPv6 路由协议上应用 IPsec 安全框架的相关配置，请分别参考“三层技术-IP 路由配置指导”中的“IPv6 BGP”、“OSPFv3”和“RIPng”。

#### 1.6 配置全局IPsec SA生存时间和空闲超时功能

##### 1. 功能简介

此功能用来配置 IPsec SA 生存时间和空闲超时功能。对于 IKE 协商建立的 IPsec SA，遵循以下原则：
采用隧道两端设置的 IPsec SA 生存时间中较小者。
•
• 可同时存在基于时间和基于流量两种方式的 IPsec SA 生存时间，只要到达指定的时间或指定的流量，IPsec 就会老化。
SA

##### 2. 配置步骤

(1) 进入系统视图。
system-view
配置 生存时间或者 空闲超时时间。
(2) IPsec SA IPsec SA
配置 生存时间。
IPsec SA
(cid:123)
ipsec sa global-duration { time-based seconds | traffic-based
kilobytes }
缺省情况下，IPsec SA 基于时间的生存时间为 3600 秒，基于流量的生存时间为 1843200
千字节。

开启 IPsec SA 空闲超时功能，并配置 IPsec SA 空闲超时时间。
(cid:123)
ipsec sa idle-time seconds缺省情况下， IPsec SA 空闲超时功能处于关闭状态。

#### 1.7 配置IPsec分片功能

##### 1. 功能简介

通过配置 分片功能，可以选择在报文进行 封装之前是否进行分片：
IPsec IPsec封装前分片功能处于开启状态时，设备会先判断报文在经过 封装之后大小是否会
• IPsec IPsec超过发送接口的 MTU 值，如果封装后的大小超过发送接口的 MTU 值，那么会先对其分片再封装。
• IPsec 封装后分片功能处于开启状态时，无论报文封装后大小是否超过发送接口的 MTU 值，设备会直接对其先进行 IPsec 封装处理，再由后续业务对其进行分片。

##### 2. 配置限制和指导

该功能仅对需要进行 封装的 报文有效。
IPsec IPv4

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置 IPsec 分片功能。
ipsec fragmentation { after-encryption | before-encryption }
缺省情况下，IPsec 封装前分片功能处于开启状态。

#### 1.8 配置本端允许建立IPsec隧道的最大数

##### 1. 配置限制与指导

此功能用来配置对本端 IPsec 隧道数目的限制。本端允许建立 IPsec 隧道的最大数与内存资源有关。
内存充足时可以设置较大的数值，提高 IPsec 的并发性能；内存不足时可以设置较小的数值，降低占用内存的资源。
IPsec

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置本端允许建立 IPsec 隧道的最大数。
ipsec limit max-tunnel tunnel-limit
缺省情况下，不限制本端允许建立 隧道的最大数。
IPsec

##### 2. 配置步骤

#### 1.9 配置IPsec报文日志信息记录功能

##### 1. 功能简介

开启 报文日志记录功能后，设备会在丢弃 报文的情况下，例如入方向找不到对应的IPsec IPsec IPsec SA、AH/ESP 认证失败、ESP 加密失败等时，输出相应的日志信息，该日志信息内容主要包括报文的源和目的 IP 地址、报文的 SPI 值、报文的序列号信息，以及设备丢包的原因。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 开启 IPsec 报文日志记录功能。
ipsec logging packet enable缺省情况下，IPsec 报文日志记录功能处于关闭状态。

#### 1.10 配置IPsec告警功能

##### 1. 功能简介

开启 的 功能后，IPsec 会生成告警信息，用于向网管软件报告该模块的重要事件。生成IPsec Trap的告警信息将被发送到设备的 SNMP 模块，通过设置 SNMP 中告警信息的发送参数，来决定告警信息输出的相关属性。有关告警信息的详细介绍，请参见“网络管理和监控配置指导”中的“SNMP”。
如果希望生成并输出某种类型的 IPsec 告警信息，则需要保证 IPsec 的全局告警功能以及相应类型的告警功能均处于开启状态。

##### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 开启 IPsec 的全局告警功能。
snmp-agent trap enable ipsec global缺省情况下，IPsec 的全局告警功能处于关闭状态。
(3) 开启 IPsec 的指定告警功能。
snmp-agent trap enable ipsec [ auth-failure | decrypt-failure | encrypt-failure | invalid-sa-failure | no-sa-failure | policy-add | policy-attach | policy-delete | policy-detach | tunnel-start | tunnel-stop ] *缺省情况下，IPsec 的所有告警功能均处于关闭状态。

#### 1.11 IPsec显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 IPsec 的运行情况，通过查看显示信息认证配置的效果。
在用户视图下执行 reset 命令可以清除 IPsec 统计信息。

###### 1. 组网需求

表1-2 IPsec 显示和维护操作 命令display ipsec { ipv6-policy | policy } [ policy-name显示IPsec安全策略的信息[ seq-number ] ] display ipsec { ipv6-policy-template |显示IPsec安全策略模板的信息policy-template } [ template-name [ seq-number ] ]显示IPsec安全框架的信息 display ipsec profile [ profile-name ] display ipsec sa [ brief | count | interface interface-type interface-number | { ipv6-policy |显示IPsec SA的相关信息policy } policy-name [ seq-number ] | profile profile-name | remote [ ipv6 ] ip-address ]显示IPsec处理报文的统计信息 display ipsec statistics [ tunnel-id tunnel-id ]显示IPsec安全提议的信息 display ipsec transform-set [ transform-set-name ] display ipsec tunnel { brief | count | tunnel-id显示IPsec隧道的信息tunnel-id } reset ipsec sa [ { ipv6-policy | policy } policy-name [ seq-number ] | profile policy-name | remote清除已经建立的IPsec SA { ipv4-address | ipv6 ipv6-address } | spi { ipv4-address | ipv6 ipv6-address } { ah | esp } spi-num ]清除IPsec的报文统计信息 reset ipsec statistics [ tunnel-id tunnel-id ]

#### 1.12 IPsec典型配置举例

##### 1.12.1 采用手工方式建立保护IPv4报文的IPsec隧道

组网需求
1.
在 Switch A 和 Switch B 之间建立一条 IPsec 隧道，对 Switch A 与 Switch B 之间的数据流进行安全保护。具体要求如下：
封装形式为隧道模式。
•安全协议采用 ESP 协议。
•加密算法采用 AES-CBC-192，认证算法采用 HMAC-SHA1。
•
• 手工方式建立 IPsec SA。

###### 2. 组网图

图1-7 保护 报文的 配置组网图IPv4 IPsec

###### 3. 配置步骤

(1) 配置 Switch A
\# 配置 Vlan-interface1 接口的 IP 地址。
<SwitchA> system-view
[SwitchA] interface vlan-interface 1
[SwitchA-Vlan-interface1] ip address 2.2.2.1 255.255.255.0
[SwitchA-Vlan-interface1] quit
配置一个访问控制列表，定义 和 之间的数据流。
\# Switch A Switch B
[SwitchA] acl advanced 3101
[SwitchA-acl-ipv4-adv-3101] rule 0 permit ip source 2.2.2.1 0 destination 2.2.3.1 0
[SwitchA-acl-ipv4-adv-3101] quit
创建 安全提议 tran1。
\# IPsec
[SwitchA] ipsec transform-set tran1
\# 配置安全协议对 IP 报文的封装形式为隧道模式。
[SwitchA-ipsec-transform-set-tran1] encapsulation-mode tunnel
\# 配置采用的安全协议为 ESP。
[SwitchA-ipsec-transform-set-tran1] protocol esp
\# 配置 ESP 协议采用的加密算法为 AES-CBC-192，认证算法为 HMAC-SHA1。
[SwitchA-ipsec-transform-set-tran1] esp encryption-algorithm aes-cbc-192
[SwitchA-ipsec-transform-set-tran1] esp authentication-algorithm sha1
[SwitchA-ipsec-transform-set-tran1] quit
\# 创建一条手工方式的 IPsec 安全策略，名称为 map1，序列号为 10。
[SwitchA] ipsec policy map1 10 manual
\# 指定引用 ACL 3101。
[SwitchA-ipsec-policy-manual-map1-10] security acl 3101
指定引用的 安全提议为 tran1。
\# IPsec
[SwitchA-ipsec-policy-manual-map1-10] transform-set tran1
\# 指定 IPsec 隧道对端 IP 地址为 2.2.3.1。
[SwitchA-ipsec-policy-manual-map1-10] remote-address 2.2.3.1
\# 配置 ESP 协议的出方向 SPI 为 12345，入方向 SPI 为 54321。
[SwitchA-ipsec-policy-manual-map1-10] sa spi outbound esp 12345
[SwitchA-ipsec-policy-manual-map1-10] sa spi inbound esp 54321
\# 配置 ESP 协议的出方向 SA 的密钥为明文字符串 abcdefg，入方向 SA 的密钥为明文字符串
gfedcba。
[SwitchA-ipsec-policy-manual-map1-10] sa string-key outbound esp simple abcdefg
[SwitchA-ipsec-policy-manual-map1-10] sa string-key inbound esp simple gfedcba
[SwitchA-ipsec-policy-manual-map1-10] quit
\# 在 Vlan-interface1 接口上应用安全策略组。
[SwitchA] interface vlan-interface 1
[SwitchA-Vlan-interface1] ipsec apply policy map1
配置
(2) Switch B
配置 接口的 地址。
\# Vlan-interface1 IP
<SwitchB> system-view

[SwitchB] interface vlan-interface 1 [SwitchB-Vlan-interface1] ip address 2.2.3.1 255.255.255.0 [SwitchB-Vlan-interface1] quit \# 配置一个访问控制列表，定义 Switch B 和 Switch A 之间的数据流。
[SwitchB] acl advanced 3101 [SwitchB-acl-ipv4-adv-3101] rule 0 permit ip source 2.2.3.1 0 destination 2.2.2.1 0 [SwitchB-acl-ipv4-adv-3101] quit \# 创建 IPsec 安全提议 tran1。
[SwitchB] ipsec transform-set tran1 \# 配置安全协议对 IP 报文的封装形式为隧道模式。
[SwitchB-ipsec-transform-set-tran1] encapsulation-mode tunnel配置采用的安全协议为 ESP。
\# [SwitchB-ipsec-transform-set-tran1] protocol esp \# 配置 ESP 协议采用的加密算法为 AES-CBC-192，认证算法为 HMAC-SHA1。
[SwitchB-ipsec-transform-set-tran1] esp encryption-algorithm aes-cbc-192 [SwitchB-ipsec-transform-set-tran1] esp authentication-algorithm sha1 [SwitchB-ipsec-transform-set-tran1] quit \# 创建一条手工方式的 IPsec 安全策略，名称为 use1，序列号为 10。
[SwitchB] ipsec policy use1 10 manual \# 指定引用 ACL 3101。
[SwitchB-ipsec-policy-manual-use1-10] security acl 3101 \# 指定引用的 IPsec 安全提议为 tran1。
[SwitchB-ipsec-policy-manual-use1-10] transform-set tran1 \# 指定 IPsec 隧道对端 IP 地址为 2.2.2.1。
[SwitchB-ipsec-policy-manual-use1-10] remote-address 2.2.2.1配置 协议的出方向 为 54321，入方向 为 12345。
\# ESP SPI SPI [SwitchB-ipsec-policy-manual-use1-10] sa spi outbound esp 54321 [SwitchB-ipsec-policy-manual-use1-10] sa spi inbound esp 12345 \# 配置 ESP 协议的出方向 SA 的密钥为明文字符串 gfedcba，入方向 SA 的密钥为明文字符串abcdefg。
[SwitchB-ipsec-policy-manual-use1-10] sa string-key outbound esp simple gfedcba [SwitchB-ipsec-policy-manual-use1-10] sa string-key inbound esp simple abcdefg [SwitchB-ipsec-policy-manual-use1-10] quit \# 在 Vlan-interface1 接口上应用安全策略组。
[SwitchB] interface vlan-interface 1 [SwitchB-Vlan-interface1] ipsec apply policy use1

###### 4. 验证配置

以上配置完成后，Switch A 和 Switch B 之间的 IPsec 隧道就建立好了，Swtich A 和 Switch B 之间数据流的传输将受到生成的 IPsec SA 的保护。可通过以下显示查看 Switch A 上手工创建的 IPsec SA 。
[SwitchA] display ipsec sa
------------------------------- Interface: Vlan-interface 1
-------------------------------

###### 1. 组网需求

###### 3. 配置步骤

-----------------------------
IPsec policy: map1
Sequence number: 10
Mode: manual
-----------------------------
Tunnel id: 549
Encapsulation mode: tunnel
Path MTU: 1443
Tunnel:
local address: 2.2.2.1
remote address: 2.2.3.1
Flow:
as defined in ACL 3101
[Inbound ESP SA]
SPI: 54321 (0x0000d431)
Transform set: ESP-ENCRYPT-AES-CBC-192 ESP-AUTH-SHA1
No duration limit for this SA
[Outbound ESP SA]
SPI: 12345 (0x00003039)
Transform set: ESP-ENCRYPT-AES-CBC-192 ESP-AUTH-SHA1
No duration limit for this SA
Switch B 上也会产生相应的 IPsec SA 来保护 IPv4 报文，查看方式与 Switch A 同，此处略。

##### 1.12.2 采用IKE方式建立保护IPv4报文的IPsec隧道

组网需求
1.
在 Switch A 和 Switch B 之间建立一条 IPsec 隧道，对 Switch A 与 Switch B 之间的数据流进行安全保护。具体要求如下：
封装形式为隧道模式。
•安全协议采用 ESP 协议。
•加密算法采用 AES-CBC-192，认证算法采用 HMAC-SHA1。
•
• IKE 协商方式建立 IPsec SA。

###### 2. 组网图

图1-8 保护 报文的 配置组网图IPv4 IPsec配置步骤
3.
(1) 配置 Switch A \# 配置 Vlan-interface1 接口的 IP 地址。
<SwitchA> system-view

[SwitchA] interface vlan-interface 1 [SwitchA-Vlan-interface1] ip address 2.2.2.1 255.255.255.0 [SwitchA-Vlan-interface1] quit \# 配置一个访问控制列表，定义由 Switch A 去 Switch B 的数据流。
[SwitchA] acl number 3101 [SwitchA-acl-adv-3101] rule 0 permit ip source 2.2.2.1 0 destination 2.2.3.1 0 [SwitchA-acl-adv-3101] quit \# 创 IPsec 建安全提议 tran1。
[SwitchA] ipsec transform-set tran1 \# 配置安全协议对 IP 报文的封装形式为隧道模式。
[SwitchA-ipsec-transform-set-tran1] encapsulation-mode tunnel配置采用的安全协议为 ESP。
\# [SwitchA-ipsec-transform-set-tran1] protocol esp \# 配置 ESP 协议采用的加密算法为 AES-CBC-192，认证算法为 HMAC-SHA1。
[SwitchA-ipsec-transform-set-tran1] esp encryption-algorithm aes-cbc-192 [SwitchA-ipsec-transform-set-tran1] esp authentication-algorithm sha1 [SwitchA-ipsec-transform-set-tran1] quit \# 创建并配置 IKE keychain，名称为 keychain1。
[SwitchA] ike keychain keychain1 \# 配置与 IP 地址为 2.2.3.1 的对端使用的预共享密钥为明文 12345zxcvb!@#$%ZXCVB。
[SwitchA-ike-keychain-keychain1] pre-shared-key address 2.2.3.1 255.255.255.0 key simple 12345zxcvb!@#$%ZXCVB [SwitchA-ike-keychain-keychain1] quit \# 创建并配置 IKE profile，名称为 profile1。
[SwitchA] ike profile profile1 [SwitchA-ike-profile-profile1] keychain keychain1 [SwitchA-ike-profile-profile1] match remote identity address 2.2.3.1 255.255.255.0 [SwitchA-ike-profile-profile1] quit创建一条 协商方式的 安全策略，名称为 map1，序列号为 10。
\# IKE IPsec [SwitchA] ipsec policy map1 10 isakmp \# 指定引用 ACL 3101。
[SwitchA-ipsec-policy-isakmp-map1-10] security acl 3101 \# 指定引用的安全提议为 tran1 。
[SwitchA-ipsec-policy-isakmp-map1-10] transform-set tran1指定 隧道的本端 地址为 2.2.2.1，对端 地址为 2.2.3.1。
\# IPsec IP IP [SwitchA-ipsec-policy-isakmp-map1-10] local-address 2.2.2.1 [SwitchA-ipsec-policy-isakmp-map1-10] remote-address 2.2.3.1 \# 指定引用的 IKE profile 为 profile1。
[SwitchA-ipsec-policy-isakmp-map1-10] ike-profile profile1 [SwitchA-ipsec-policy-isakmp-map1-10] quit \# 在 Vlan-interface1 接口上应用安全策略组。
[SwitchA] interface vlan-interface 1 [SwitchA-Vlan-interface1] ipsec apply policy map1
(2) 配置 Switch B

\# 配置 Vlan-interface1 接口的 IP 地址。
<SwitchB> system-view [SwitchB] interface vlan-interface 1 [SwitchB-Vlan-interface1] ip address 2.2.3.1 255.255.255.0 [SwitchB-Vlan-interface1] quit \# 配置一个访问控制列表，定义由 Switch B 去 Switch A 的数据流。
[SwitchB] acl number 3101 [SwitchB-acl-adv-3101] rule 0 permit ip source 2.2.3.1 0 destination 2.2.2.1 0 [SwitchB-acl-adv-3101] quit \# 创建 IPsec 安全提议 tran1。
[SwitchB] ipsec transform-set tran1 \# 配置安全协议对 IP 报文的封装形式为隧道模式。
[SwitchB-ipsec-transform-set-tran1] encapsulation-mode tunnel配置采用的安全协议为 ESP。
\# [SwitchB-ipsec-transform-set-tran1] protocol esp \# 配置 ESP 协议采用的加密算法为 AES-CBC-192，认证算法为 HMAC-SHA1。
[SwitchB-ipsec-transform-set-tran1] esp encryption-algorithm aes-cbc-192 [SwitchB-ipsec-transform-set-tran1] esp authentication-algorithm sha1 [SwitchB-ipsec-transform-set-tran1] quit \# 创建并配置 IKE keychain，名称为 keychain1。
[SwitchB] ike keychain keychain1配置与 地址为 的对端使用的预共享密钥为明文 12345zxcvb!@#$%ZXCVB。
\# IP 2.2.2.1 [SwitchB-ike-keychain-keychain1] pre-shared-key address 2.2.2.1 255.255.255.0 key simple 12345zxcvb!@#$%ZXCVB [SwitchB-ike-keychain-keychain1] quit \# 创建并配置 IKE profile，名称为 profile1。
[SwitchB] ike profile profile1 [SwitchB-ike-profile-profile1] keychain keychain1 [SwitchB-ike-profile-profile1] match remote identity address 2.2.2.1 255.255.255.0 [SwitchB-ike-profile-profile1] quit创建一条 协商方式的安全策略，名称为 use1，序列号为 10。
\# IKE [SwitchB] ipsec policy use1 10 isakmp \# 指定引用 ACL 3101。
[SwitchB-ipsec-policy-isakmp-use1-10] security acl 3101 \# 指定引用的 IPsec 安全提议为 tran1。
[SwitchB-ipsec-policy-isakmp-use1-10] transform-set tran1 \# 指定 IPsec 隧道的本端 IP 地址为 2.2.3.1，对端 IP 地址为 2.2.2.1。
[SwitchB-ipsec-policy-isakmp-use1-10] local-address 2.2.3.1 [SwitchB-ipsec-policy-isakmp-use1-10] remote-address 2.2.2.1 \# 指定引用的 IKE 对等体为 profile1。
[SwitchB-ipsec-policy-isakmp-use1-10] ike-profile profile1 [SwitchB-ipsec-policy-isakmp-use1-10] quit \# 在 Vlan-interface1 接口上应用安全策略组。
[SwitchB] interface vlan-interface 1

###### 4. 配置步骤

[SwitchB-Vlan-interface1] ipsec apply policy use1

###### 4. 验证配置

以上配置完成后，Switch A 和 Switch B 之间如果有端到端的报文发送或接收，将触发 IKE 进行 IPsec的协商。IKE 成功协商出 后，Switch 和 之间数据流的传输将受到SA IPsec SA A Switch B IPsec SA的保护。

##### 1.12.3 配置IPsec保护RIPng报文

###### 1. 组网需求

如 图 1-9 所示，Switch A、Switch B和Switch C相连，并通过RIPng来学习网络中的IPv6 路由信息。
在各设备之间建立IPsec隧道，对它们收发的RIPng报文进行安全保护。具体要求如下：
• 安全协议采用 ESP 协议；
• 加密算法采用 128 比特的 AES；
• 认证算法采用 HMAC-SHA1。

###### 2. 组网图

图1-9 配置 IPsec 保护 RIPng 报文组网图

###### 3. 配置思路

(1) 配置 RIPng 的基本功能
RIPng 配置的详细介绍请参考“三层技术-IP 路由配置指导”中的“RIPng”。
(2) 配置 IPsec 安全框架
需要注意的是：
各设备上本端出方向 SA 的 SPI 及密钥必须和本端入方向 SA 的 SPI 及密钥保持一致。
(cid:123)
Switch A、Switch B 和 Switch C 上的安全策略所引用的安全提议采用的安全协议、认证/
(cid:123)
加密算法和报文封装模式要相同，而且所有设备上的 SA 的 SPI 及密钥均要保持一致。
(3) 在 RIPng 进程下或接口上应用 IPsec 安全框架
配置步骤
4.
(1) 配置 Switch A
配置各接口的 IPv6 地址（略）
(cid:123)
配置 RIPng 的基本功能
(cid:123)
<SwitchA> system-view
[SwitchA] ripng 1
[SwitchA-ripng-1] quit
[SwitchA] interface vlan-interface 100
[SwitchA-Vlan-interface100] ripng 1 enable
[SwitchA-Vlan-interface100] quit

配置 IPsec 安全框架(cid:123)
\# 创建并配置名为 tran1 的 IPsec 安全提议（报文封装模式采用传输模式，安全协议采用协议，加密算法采用 比特的 AES，认证算法采用 HMAC-SHA1）。
ESP 128 [SwitchA] ipsec transform-set tran1 [SwitchA-ipsec-transform-set-tran1] encapsulation-mode transport [SwitchA-ipsec-transform-set-tran1] protocol esp [SwitchA-ipsec-transform-set-tran1] esp encryption-algorithm aes-cbc-128 [SwitchA-ipsec-transform-set-tran1] esp authentication-algorithm sha1 [SwitchA-ipsec-transform-set-tran1] quit创建并配置名为 的 安全框架（协商方式为手工方式，出入方向 的\# profile001 IPsec SA SPI 均为 123456，出入方向 SA 的密钥均为明文 abcdefg）。
[SwitchA] ipsec profile profile001 manual [SwitchA-ipsec-profile-manual-profile001] transform-set tran1 [SwitchA-ipsec-profile-manual-profile001] sa spi outbound esp 123456 [SwitchA-ipsec-profile-manual-profile001] sa spi inbound esp 123456 [SwitchA-ipsec-profile-manual-profile001] sa string-key outbound esp simple abcdefg [SwitchA-ipsec-profile-manual-profile001] sa string-key inbound esp simple abcdefg [SwitchA-ipsec-profile-manual-profile001] quit在 进程上应用 安全框架RIPng IPsec (cid:123)
[SwitchA] ripng 1 [SwitchA-ripng-1] enable ipsec-profile profile001 [SwitchA-ripng-1] quit
(2) 配置 Switch B配置各接口的 IPv6 地址（略）
(cid:123)
配置 RIPng 的基本功能(cid:123)
<SwitchB> system-view [SwitchB] ripng 1 [SwitchB-ripng-1] quit [SwitchB] interface vlan-interface 200 [SwitchB-Vlan-interface200] ripng 1 enable [SwitchB-Vlan-interface200] quit [SwitchB] interface vlan-interface 100 [SwitchB-Vlan-interface100] ripng 1 enable [SwitchB-Vlan-interface100] quit配置 IPsec 安全框架(cid:123)
\# 创建并配置名为 tran1 的 IPsec 安全提议（报文封装模式采用传输模式，安全协议采用协议，加密算法采用 比特的 AES，认证算法采用 HMAC-SHA1）。
ESP 128 [SwitchB] ipsec transform-set tran1 [SwitchB-ipsec-transform-set-tran1] encapsulation-mode transport [SwitchB-ipsec-transform-set-tran1] protocol esp [SwitchB-ipsec-transform-set-tran1] esp encryption-algorithm aes-cbc-128 [SwitchB-ipsec-transform-set-tran1] esp authentication-algorithm sha1 [SwitchB-ipsec-transform-set-tran1] quit创建并配置名为 的 安全框架（协商方式为手工方式，出入方向 的\# profile001 IPsec SA SPI 均为 123456，出入方向 SA 的密钥均为明文 abcdefg）。

###### 5. 验证配置

[SwitchB] ipsec profile profile001 manual [SwitchB-ipsec-profile-manual-profile001] transform-set tran1 [SwitchB-ipsec-profile-manual-profile001] sa spi outbound esp 123456 [SwitchB-ipsec-profile-manual-profile001] sa spi inbound esp 123456 [SwitchB-ipsec-profile-manual-profile001] sa string-key outbound esp simple abcdefg [SwitchB-ipsec-profile-manual-profile001] sa string-key inbound esp simple abcdefg [SwitchB-ipsec-profile-manual-profile001] quit在 RIPng 进程上应用 IPsec 安全框架(cid:123)
[SwitchB] ripng 1 [SwitchB-ripng-1] enable ipsec-profile profile001 [SwitchB-ripng-1] quit
(3) 配置 Switch C配置各接口的 IPv6 地址（略）
(cid:123)
配置 RIPng 的基本功能(cid:123)
<SwitchC> system-view [SwitchC] ripng 1 [SwitchC-ripng-1] quit [SwitchC] interface vlan-interface 200 [SwitchC-Vlan-interface200] ripng 1 enable [SwitchC-Vlan-interface200] quit配置 IPsec 安全框架(cid:123)
\# 创建并配置名为 tran1 的 IPsec 安全提议（报文封装模式采用传输模式，安全协议采用ESP 协议，加密算法采用 128 比特的 AES，认证算法采用 HMAC-SHA1）。
[SwitchC] ipsec transform-set tran1 [SwitchC-ipsec-transform-set-tran1] encapsulation-mode transport [SwitchC-ipsec-transform-set-tran1] protocol esp [SwitchC-ipsec-transform-set-tran1] esp encryption-algorithm aes-cbc-128 [SwitchC-ipsec-transform-set-tran1] esp authentication-algorithm sha1 [SwitchC-ipsec-transform-set-tran1] quit \# 创建并配置名为 profile001 的 IPsec 安全框架（协商方式为手工方式，出入方向 SA 的SPI 均为 123456，出入方向 SA 的密钥均为明文 abcdefg）。
[SwitchC] ipsec profile profile001 manual [SwitchC-ipsec-profile-manual-profile001] transform-set tran1 [SwitchC-ipsec-profile-manual-profile001] sa spi outbound esp 123456 [SwitchC-ipsec-profile-manual-profile001] sa spi inbound esp 123456 [SwitchC-ipsec-profile-manual-profile001] sa string-key outbound esp simple abcdefg [SwitchC-ipsec-profile-manual-profile001] sa string-key inbound esp simple abcdefg [SwitchC-ipsec-profile-manual-profile001] quit在 RIPng 进程上应用 IPsec 安全框架(cid:123)
[SwitchC] ripng 1 [SwitchC-ripng-1] enable ipsec-profile profile001 [SwitchC-ripng-1] quit验证配置
5.
以上配置完成后，Switch A、Switch B 和 Switch C 将通过 RIPng 协议学习到网络中的 IPv6 路由信息，且分别产生用于保护 报文的 SA。
RIPng IPsec

###### 1. 组网需求

可以通过如下 display 命令查看 Switch A 上 RIPng 的配置信息。如下显示信息表示 RIPng 进程 1上已成功应用了 安全框架。
IPsec [SwitchA] display ripng 1 RIPng process : 1 Preference : 100 Checkzero : Enabled Default Cost : 0 Maximum number of load balanced routes : 8 Update time : 30 secs Timeout time : 180 secs Suppress time : 120 secs Garbage-Collect time : 120 secs Update output delay: 20(ms) Output count: 3 Graceful-restart interval: 60 secs Triggered Interval : 5 50 200 Number of periodic updates sent : 186 Number of triggered updates sent : 1 IPsec profile name: profile001可以通过如下 命令查看 上生成的 SA。
display Switch A IPsec [SwitchA] display ipsec sa
------------------------------- Global IPsec SA
-------------------------------
----------------------------- IPsec profile: profile001 Mode: Manual
----------------------------- Encapsulation mode: transport [Inbound ESP SA] SPI: 123456 (0x3039)
Connection ID: 90194313219 Transform set: ESP-ENCRYPT-AES-CBC-128 ESP-AUTH-SHA1 No duration limit for this SA [Outbound ESP SA] SPI: 123456 (0x3039)
Connection ID: 64424509441 Transform set: ESP-ENCRYPT-AES-CBC-128ESP-AUTH-SHA1 No duration limit for this SA Switch B 和 Switch C 上也会生成相应的 IPsec SA 来保护 RIPng 报文，查看方式与 Switch A 同，此处略。

##### 1.12.4 配置IPsec反向路由注入

组网需求
1.
企业分支通过 IPsec VPN 接入企业总部，有如下具体需求：
• 总部网关 Switch A 和各分支网关 Switch B、SwitchC、Switch D 之间建立 IPsec 隧道，对总部网络 与分支网络 之间的数据进行安全保护。
4.4.4.0/24 5.5.5.0/24

###### 2. 组网图

使用 IKE 协商方式建立 IPsec SA，采用 ESP 安全协议，DES 加密算法，HMAC-SHA-1-96
•认证算法。
协商采用预共享密钥认证方式、3DES 加密算法、HMAC-SHA1 认证算法。
• IKE在 上开启 反向路由注入功能，实现总部到分支的静态路由随 的建立
• Switch A IPsec IPsec SA而动态生成。
组网图
2.
图1-10 配置 IPsec 反向路由注入功能组网图

###### 3. 配置步骤

(1) 配置 Switch A
配置各接口的 地址（略）
IPv4
(cid:123)
配置 安全提议
IPsec
(cid:123)
创建并配置名为 的安全提议，采用使用 安全协议，DES 加密算法，
\# tran1 ESP
HMAC-SHA-1-96 认证算法。
<SwitchA> system-view
[SwitchA] ipsec transform-set tran1
[SwitchA-ipsec-transform-set-tran1] encapsulation-mode tunnel
[SwitchA-ipsec-transform-set-tran1] protocol esp
[SwitchA-ipsec-transform-set-tran1] esp encryption-algorithm des
[SwitchA-ipsec-transform-set-tran1] esp authentication-algorithm sha1
[SwitchA-ipsec-transform-set-tran1] quit
配置
IKE profile
(cid:123)
\# 创建并配置 IKE profile，名称为 profile1。
[SwitchA] ike profile profile1
[SwitchA-ike-profile-profile1] keychain key1
[SwitchA-ike-profile-profile1] match remote identity address 2.2.2.2 255.255.255.0
[SwitchA-ike-profile-profile1] quit
配置 IPsec 安全策略模板
(cid:123)
\# 创建并配置名为 temp1 的 IPsec 安全策略模板，引用安全提议 tran1
[SwitchA] ipsec policy-template temp1 1
[SwitchA-ipsec-policy-template-temp1-1] transform-set tran1

[SwitchA-ipsec-policy-template-temp1-1] ike-profile profile1配置 RRI 功能(cid:123)
\# 开启 RRI 功能，指定生成的静态路由的优先级为 100、Tag 值为 1000。
[SwitchA-ipsec-policy-template-temp1-1] reverse-route dynamic [SwitchA-ipsec-policy-template-temp1-1] reverse-route preference 100 [SwitchA-ipsec-policy-template-temp1-1] reverse-route tag 1000 [SwitchA-ipsec-policy-template-temp1-1] quit配置 协商方式的 安全策略IKE IPsec (cid:123)
创建并配置名为 的 安全策略，基于安全策略模板 创建\# map1 IPsec temp1 [SwitchA] ipsec policy map1 10 isakmp template temp1配置 IKE 提议(cid:123)
\# 创建并配置 IKE 提议 1，指定使用预共享密钥认证方式、3DES 加密算法、HMAC-SHA1认证算法。
[SwitchA] ike proposal 1 [SwitchA-ike-proposal-1] encryption-algorithm 3des-cbc [SwitchA-ike-proposal-1] authentication-algorithm sha [SwitchA-ike-proposal-1] authentication-method pre-share [SwitchA-ike-proposal-1] quit配置 IKE keychain (cid:123)
创建并配置名为 的 keychain，指定与地址为 的对端使用的预共享密钥\# key1 IKE 2.2.2.2为明文 123。
[SwitchA] ike keychain key1 [SwitchA-ike-keychain-key1] pre-shared-key address 2.2.2.2 key simple 123 [SwitchA-ike-keychain-key1] quit在接口下引用 IPsec 安全策略(cid:123)
\# 在接口 Vlan-interface100 上应用 IPsec 安全策略 map1。
[SwitchA] interface vlan-interface 100 [SwitchA-Vlan-interface100] ipsec apply policy map1 [SwitchA-Vlan-interface100] quit
(2) 配置 Switch B配置各接口的 IPv4 地址（略）
(cid:123)
配置 IPsec 安全提议(cid:123)
创建并配置名为 的安全提议\# tran1 [SwitchB] ipsec transform-set tran1 [SwitchB-ipsec-transform-set-tran1] encapsulation-mode tunnel [SwitchB-ipsec-transform-set-tran1] protocol esp [SwitchB-ipsec-transform-set-tran1] esp encryption-algorithm des [SwitchB-ipsec-transform-set-tran1] esp authentication-algorithm sha1 [SwitchB-ipsec-transform-set-tran1] quit配置ACL (cid:123)
配置 高级 3000，定义要保护由子网 去往子网 的数据流。
\# IPv4 ACL 5.5.5.0/24 4.4.4.0/24 [SwitchB] acl advanced 3000 [SwitchB-acl-ipv4-adv-3000] rule permit ip source 5.5.5.0 0.0.0.255 destination
4.4.4.0 0.0.0.255

[SwitchB-acl-ipv4-adv-3000] quit配置 IKE profile (cid:123)
\# 创建并配置 IKE profile，名称为 profile1。
[SwitchB] ike profile profile1 [SwitchB-ike-profile-profile1] keychain key1 [SwitchB-ike-profile-profile1] match remote identity address 1.1.1.1 255.255.255.0 [SwitchB-ike-profile-profile1] quit配置 方式的安全策略ISAKMP (cid:123)
创建并配置名为 的 安全策略，引用安全提议 tran1，引用 3000，并指\# map1 IPsec ACL定 IPsec 隧道的对端地址为 1.1.1.1。
[SwitchB] ipsec policy map1 10 isakmp [SwitchB-ipsec-policy-isakmp-map1-10] transform-set tran1 [SwitchB-ipsec-policy-isakmp-map1-10] security acl 3000 [SwitchB-ipsec-policy-isakmp-map1-10] remote-address 1.1.1.1 [SwitchB-ipsec-policy-isakmp-map1-10] ike-profile profile1 [SwitchB-ipsec-policy-isakmp-map1-10] quit配置 IKE 提议(cid:123)
\# 创建并配置 IKE 提议 1，指定预共享密钥认证方式、3DES 加密算法、HMAC-SHA1 认证算法。
[SwitchB] ike proposal 1 [SwitchB-ike-proposal-1] encryption-algorithm 3des-cbc [SwitchB-ike-proposal-1] authentication-algorithm sha [SwitchB-ike-proposal-1] authentication-method pre-share [SwitchB-ike-proposal-1] quit配置 IKE keychain (cid:123)
\# 创建并配置名为 key1 的 IKE keychain，指定与地址为 1.1.1.1 的对端使用的预共享密钥为明文 123。
[SwitchB] ike keychain key1 [SwitchB-ike-keychain-key1] pre-shared-key address 1.1.1.1 key simple 123 [SwitchB-ike-keychain-key1] quit在接口上应用 安全策略IPsec (cid:123)
在接口 上应用 安全策略 map1。
\# Vlan-interface100 IPsec [SwitchB] interface vlan-interface 100 [SwitchB-Vlan-interface100] ipsec apply policy map1 [SwitchB-Vlan-interface100] quit保证 SwitchB 上存在到达对端私网网段的路由，出接口为 Vlan-interface100。
(3) 配置 Switch C、Switch D配置步骤与 Switch B 类似，请参考 Switch B 的配置。

###### 4. 验证配置结果

以上配置完成后，当分支子网 向总部网络 发起数据连接时，将触发
5.5.5.0/24 4.4.4.0/24 Rouer B和 Switch A 之间进行 IKE 协商。IKE 成功协商出 IPsec SA 后，企业总部与分支子网之间的数据流传输将受到 IPsec SA 的保护。在 Switch A 上可通过以下显示查看到协商生成的 IPsec SA。
[SwitchA] display ipsec sa

-------------------------------
Interface: Vlan-interface100
-------------------------------
-----------------------------
IPsec policy: map1
Sequence number: 10
Mode: Template
-----------------------------
Tunnel id: 0
Encapsulation mode: tunnel
Perfect Forward Secrecy:
Inside VPN:
Extended Sequence Numbers enable: N
Traffic Flow Confidentiality enable: N
Path MTU: 1463
Tunnel:
local address: 1.1.1.1
remote address: 2.2.2.2
Flow:
sour addr: 4.4.4.0/255.255.255.0 port: 0 protocol: ip
dest addr: 5.5.5.0/255.255.255.0 port: 0 protocol: ip
[Inbound ESP SAs]
SPI: 1014286405 (0x3c74c845)
Connection ID: 90194313219
Transform set: ESP-ENCRYPT-DES-CBC ESP-AUTH-SHA1
SA duration (kilobytes/sec): 1843200/3600
SA remaining duration (kilobytes/sec): 1843199/3590
Max received sequence-number: 4
Anti-replay check enable: Y
Anti-replay window size: 64
UDP encapsulation used for NAT traversal: N
Status: Active
[Outbound ESP SAs]
SPI: 4011716027 (0xef1dedbb)
Connection ID: 64424509441
Transform set: ESP-ENCRYPT-DES-CBC ESP-AUTH-SHA1
SA duration (kilobytes/sec): 1843200/3600
SA remaining duration (kilobytes/sec): 1843199/3590
Max sent sequence-number: 4
UDP encapsulation used for NAT traversal: N
Status: Active
IPsec SA 成功建立后，在 Switch A 上可以通过 display ip routing-table verbose 命令查
看到 反向路由注入生成的静态路由，目的地址为分支子网地址 5.5.5.0/24，下一跳为
IPsec IPsec

隧道对端地址 2.2.2.2，优先级为 100，Tag 值为 1000。Switch A 和 Switch C、Switch D 之间的 IPsec隧道建立成功后，Switch 上也会产生到达各分支子网的相应静态路由，此处显示略。
A

### 2 IKE

2 IKE若无特殊说明，本文中的 IKE 均指第 1 版本的 IKE 协议。

#### 2.1 IKE简介

IKE（Internet Key Exchange，互联网密钥交换）协议利用 ISAKMP（Internet Security Association and Key Management Protocol，互联网安全联盟和密钥管理协议）语言定义密钥交换的过程，是一种对安全服务进行协商的手段。

##### 2.1.1 IKE的优点

用 IPsec 保护一个 IP 数据包之前，必须先建立一个安全联盟（IPsec SA），IPsec SA 可以手工创建或动态建立。IKE 为 IPsec 提供了自动建立 IPsec SA 的服务，具体有以下优点。
首先会在通信双方之间协商建立一个安全通道（IKE SA），并在此安全通道的保护下协商
• IKE建立 IPsec SA，这降低了手工配置的复杂度，简化 IPsec 的配置和维护工作。
• IKE 的精髓在于 DH（Diffie-Hellman）交换技术，它通过一系列的交换，使得通信双方最终计算出共享密钥。在 IKE 的 DH 交换过程中，每次计算和产生的结果都是不相关的。由于每次的建立都运行了 交换过程，因此就保证了每个通过 协商建立的 所IKE SA DH IKE IPsec SA使用的密钥互不相关。
• IPsec 使用 AH 或 ESP 报文头中的顺序号实现防重放。此顺序号是一个 32 比特的值，此数溢出之前，为实现防重放，IPsec SA 需要重新建立，IKE 可以自动重协商 IPsec SA。

##### 2.1.2 IPsec与IKE的关系

如 图 所示，IKE为IPsec协商建立SA，并把建立的参数交给IPsec，IPsec使用IKE建立的SA对IP 2-1报文加密或认证处理。

###### 1. 主模式

图2-1 IPsec 与 IKE 的关系图

##### 2.1.3 IKE的协商过程

使用了两个阶段为 进行密钥协商以及建立 SA：
IKE IPsec第一阶段，通信双方彼此间建立了一个已通过双方身份认证和对通信数据安全保护的通道，
(1)
即建立一个 IKE SA（本文中提到的 IKE SA 都是指第一阶段 SA）。
(2) 第二阶段，用在第一阶段建立的 IKE SA 为 IPsec 协商安全服务，即为 IPsec 协商 IPsec SA，建立用于最终的 IP 数据安全传输的 IPsec SA。
(3) 第一阶段有主模式（Main Mode）和野蛮模式（Aggressive Mode）两种 IKE 协商模式。
主模式
1.
图2-2 主模式协商过程如 图 2-2 所示，第一阶段主模式的IKE协商过程中包含三对消息，具体内容如下：
(1) 第一对消息完成了 SA 交换，它是一个协商确认双方 IKE 安全策略的过程；

###### 2. 野蛮模式

(2) 第二对消息完成了密钥交换，通过交换 Diffie-Hellman 公共值和辅助数据（如：随机数），最
终双方计算生成一系列共享密钥（例如，认证密钥、加密密钥以及用于生成 密钥参数的
IPsec
密钥材料），并使其中的加密密钥和认证密钥对后续的 IKE 消息提供安全保障；
(3) 第三对消息完成了 ID 信息和验证数据的交换，并进行双方身份的认证。
野蛮模式
2.
图2-3 野蛮模式协商过程
如 图 所示，第一阶段野蛮模式的IKE协商过程中包含三条消息，具体内容如下：
2-3
发起方通过第一条消息发送本地 信息，包括建立 所使用的参数、与密钥生成相关
(1) IKE IKE SA
的信息和身份验证信息。
(2) 接收方通过第二条消息对收到的第一个消息进行确认，查找并返回匹配的参数、密钥生成信
息和身份验证信息。
(3) 发起方通过第三条消息回应验证结果，并成功建立 IKE SA。
与主模式相比，野蛮模式的优点是建立 IKE SA 的速度较快。但是由于野蛮模式的密钥交换与身份
认证一起进行，因此无法提供身份保护。在对身份保护要求不高的场合，使用交换报文较少的野蛮
模式可以提高协商的速度；在对身份保护要求较高的场合，则应该使用主模式。

##### 2.1.4 IKE的安全机制

IKE 可以在不安全的网络上安全地认证通信双方的身份、分发密钥以及建立 IPsec SA，具有以下几种安全机制。

###### 1. 身份认证

的身份认证机制用于确认通信双方的身份。设备支持三种认证方法：预共享密钥认证、RSA 数IKE字签名认证和 DSA 数字签名认证。
• 预共享密钥认证：通信双方通过共享的密钥认证对端身份。
• 数字签名认证：通信双方使用由 CA 颁发的数字证书向对端证明自己的身份。

###### 2. DH算法

DH 算法是一种公共密钥算法，它允许通信双方在不传输密钥的情况下通过交换一些数据，计算出共享的密钥。即使第三方（如黑客）截获了双方用于计算密钥的所有交换数据，由于其复杂度很高，也不足以计算出双方的密钥。

###### 3. PFS特性

PFS（Perfect Forward Secrecy，完善的前向安全性）是一种安全特性，它解决了密钥之间相互无关性的需求。由于 IKE 第二阶段协商需要从第一阶段协商出的密钥材料中衍生出用于 IPsec SA 的密钥，若攻击者能够破解 的一个密钥，则会非常容易得掌握其衍生出的任何 的密IKE SA IPsec SA钥。使用 PFS 特性后，IKE 第二阶段协商过程中会增加一次 DH 交换，使得 IKE SA 的密钥和 IPsec SA 的密钥之间没有派生关系，即使 IKE SA 的其中一个密钥被破解，也不会影响它协商出的其它密钥的安全性。

##### 2.1.5 协议规范

与 IKE 相关的协议规范有：
• RFC2408：Internet Security Association and Key Management Protocol (ISAKMP)
• RFC2409：The Internet Key Exchange (IKE)
• RFC2412：The OAKLEY Key Determination Protocol
• Internet-Draft ： draft-ietf-ipsec-isakmp-xauth-06.txt Internet-Draft：draft-dukes-ike-mode-cfg-02.txt
•

#### 2.2 FIPS相关说明

设备运行于 FIPS 模式时，本特性部分配置相对于非 FIPS 模式有所变化，具体差异请见本文相关描述。有关 FIPS 模式的详细介绍请参见“安全配置指导”中的“FIPS”。

#### 2.3 IKE配置任务简介

配置任务如下：
IKE
(1) （可选）配置IKE profile
a. 创建IKE profile
b. 配置匹配对端身份的规则
c. 配置keychain或者PKI域
d. 配置IKE第一阶段的协商模式
e. 配置 IKE profile 引用的 IKE 提议
f. 配置本端身份信息
g. 配置内部MPLS L3VPN实例
h. 配置IKE profile的可选功能
(2) 配置IKE提议
(3) 配置IKE keychain
(4) （可选）配置本端身份信息
(5) （可选）配置 IKE Keepa live 功能
(6) （可选）配置IKE NAT Keepalive功能
(7) （可选）配置全局IKE DPD功能（可选）配置针对无效IPsec SPI的IKE SA恢复功能
(8)

#### 2.5 配置IKE profile

###### 2. 配置步骤

###### 1. 功能简介

(9) （可选）配置对IKE SA数目的限制
(10) （可选）配置IKE告警功能

#### 2.4 IKE配置准备

进行 IKE 配置之前，用户需要确定以下几个因素，以便配置过程的顺利进行。
• 确定 IKE 交换过程中安全保护的强度，包括认证方法、加密算法、认证算法、DH group。
认证方法分为预共享密钥认证和数字签名认证。预共享密钥认证机制简单、不需要证书，(cid:123)
常在小型组网环境中使用；数字签名认证安全性更高，常在“中心—分支”模式的组网环境中使用。例如，在“中心—分支”组网中使用预共享密钥认证进行 协商时，中心侧IKE可能需要为每个分支配置一个预共享密钥，当分支很多时，配置会很复杂，而使用数字签名认证时只需配置一个 PKI 域。
不同认证/加密算法的强度不同，算法强度越高，受保护数据越难被破解，但消耗的计算资(cid:123)
源越多。
DH group 位数越大安全性越高，但是处理速度会相应减慢。应该根据实际组网环境中对安(cid:123)
全性和性能的要求选择合适的 group。
DH确定通信双方预先约定的预共享密钥或所属的 域。关于 的配置，请参见“安全配置
• PKI PKI指导”中的“PKI”。
• 确定通信双方都采用 IKE协商模式的 IPsec安全策略。IPsec安全策略中若不引用 IKE profile，则使用系统视图下配置的 IKE profile 进行协商，若系统视图下没有任何 IKE profile，则使用全局的 IKE 参数进行协商。关于 IPsec 安全策略的配置，请参见“安全配置指导”中的“IPsec”。
配置IKE
2.5 profile

##### 2.5.1 创建IKE profile

###### 1. 功能简介

创建一个 IKE profile，并进入 IKE Profile 视图。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 创建一个 IKE profile，并进入 IKE Profile 视图。
ike profile profile-name

##### 2.5.2 配置匹配对端身份的规则

功能简介
1.
响应方首先需要根据发起方的身份信息查找一个本端的 IKE profile，然后使用此 IKE profile 中的信息验证对端身份，发起方同样需要根据响应方的身份信息查找到一个 IKE profile 用于验证对端身份。
对端身份信息若能满足本地某个 中指定的匹配规则，则该 为查找的结果。
IKE profile IKE profile

###### 2. 配置限制与指导

协商双方都必须配置至少一个 match remote 规则，当对端的身份与 IKE profile 中配置的 match remote 规则匹配时，则使用此 IKE profile 中的信息与对端完成认证。

###### 3. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入 IKE Profile 视图。
ike profile profile-name
(3) 配置匹配对端身份的规则。
match remote { certificate policy-name | identity { address { { ipv4-address [ mask | mask-length ] | range low-ipv4-address high-ipv4-address } | ipv6 { ipv6-address [ prefix-length ] | range low-ipv6-address high-ipv6-address } } [ vpn-instance vpn-instance-name ] | fqdn fqdn-name | user-fqdn user-fqdn-name } }

##### 2.5.3 配置keychain或者PKI域

###### 1. 配置限制与指导

根据 提议中配置的认证方法，配置 或 域。
IKE IKE keychain PKI如果认证方法为数字签名（dsa-signature 或者 rsa-signature），则需要配置 PKI 域。
•如果指定的认证方式为预共享密钥（pre-share），则需要配置 IKE keychain。
•

###### 2. 配置步骤

进入系统视图。
(1)
system-view进入 视图。
(2) IKE Profile ike profile profile-name
(3) 配置 keychain 或者 PKI 域。
配置采用预共享密钥认证时所使用的 keychain。
(cid:123)
keychain keychain-name配置采用数字签名认证时证书所属的 PKI 域。
(cid:123)
certificate domain domain-name缺省情况下，未指定 keychain 和 PKI 域。

##### 2.5.4 配置IKE第一阶段的协商模式

###### 1. 配置限制与指导

配置本端作为发起方时所使用的协商模式（主模式、野蛮模式）。本端作为响应方时，将自动适配发起方的协商模式。

###### 2. 配置步骤

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 IKE Profile 视图。
ike profile profile-name
(3) 配置 IKE 第一阶段的协商模式。
（非 FIPS 模式）
exchange-mode { aggressive | main }
（FIPS 模式）
exchange-mode main
缺省情况下，IKE 第一阶段发起方的协商模式使用主模式。

##### 2.5.5 配置IKE profile引用的IKE提议

###### 1. 配置限制与指导

本端作为发起方时可以使用的 提议（可指定多个），先指定的优先级高。响应方会将发起方的IKE IKE 提议与本端所有的 IKE 提议进行匹配，如果找到匹配项则直接使用，否则继续查找。若未查找到匹配的 IKE 提议，则协商失败。

###### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入 IKE Profile 视图。
ike profile profile-name
(3) 配置 IKE profile 引用的 IKE 提议。
proposal proposal-number&<1-6>缺省情况下，IKE profile 未引用 IKE 提议，使用系统视图下已配置的 IKE 提议进行 IKE 协商。

##### 2.5.6 配置本端身份信息

###### 1. 配置限制与指导

• 如果本端的认证方式为数字签名，则可以配置任何类型的身份信息。若配置的本端身份为 IP
地址，但这个 地址与本地证书中的 地址不同时，设备将使用 FQDN（Fully
IP IP Qualified
Domain Name，完全合格域名）类型的本端身份，该身份的内容为设备的名称（可通过
sysname 命令配置）。
• 如果本端的认证方式为预共享密钥，则只能配置除 DN 之外的其它类型的身份信息。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 IKE Profile 视图。
ike profile profile-name

###### 1. 功能简介

(3) 配置本端身份信息。
local-identity { address { ipv4-address | ipv6 ipv6-address } | dn | fqdn
[ fqdn-name ] | user-fqdn [ user-fqdn-name ] }
缺省情况下，未配置本端身份信息。此时使用系统视图下通过 命令配置的身
ike identity
份信息作为本端身份信息。若两者都没有配置，则使用 IP 地址标识本端的身份，该 IP 地址为
IPsec 安全策略或 IPsec 安全策略模板应用的接口的 IP 地址。

##### 2.5.7 配置内部MPLS L3VPN实例

功能简介
1.
当 IPsec 解封装后得到的报文需要继续转发到不同的 VPN 中去时，设备需要知道在哪个 VPN 实例中查找相应的路由。缺省情况下，设备在与外网相同的 中查找路由，如果不希望在与外网相VPN同的 VPN 中查找路由去转发报文，则可以指定一个内部 VPN 实例，通过查找该内部 VPN 实例中的路由来转发报文。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 IKE Profile 视图。
ike profile profile-name
(3) 配置内部 MPLS L3VPN 实例。
inside-vpn vpn-instance vpn-instance-name
缺省情况下，IKE profile 未指定内部 VPN 实例，设备在收到 IPsec 报文的接口所属的 VPN 中
查找路由。

##### 2.5.8 配置IKE profile的可选功能

(1) 进入系统视图。
system-view
进入 视图。
(2) IKE Profile
ike profile profile-name
配置 的可选功能。
(3) IKE profile
配置 功能。
IKE DPD
(cid:123)
dpd interval interval [ retry seconds ] { on-demand | periodic }
缺省情况下，IKE profile 视图下没有配置 DPD 功能，采用系统视图下的 DPD 配置。若两
者没有配置，则不进行 DPD 探测。
如果 视图下和系统视图下都配置了 功能，则 视图下的 配
IKE profile DPD IKE profile DPD
置生效，如果 IKE profile 视图下没有配置 DPD 功能，则采用系统视图下的 DPD 配置。
配置 IKE profile 的使用范围。
(cid:123)
match local address { interface-type interface-number |
{ ipv4-address | ipv6 ipv6-address } [ vpn-instance
vpn-instance-name ] }

缺省情况下，未限制 IKE profile 的使用范围。
限制 IKE profile 只能在指定的地址或指定接口的地址下使用。配置了 match local的 的优先级高于所有未配置 的 profile。
address IKE profile match local address IKE配置 的优先级。
IKE profile (cid:123)
priority priority缺省情况下，IKE 的优先级为 100。
profile IKE profile 的匹配优先级首先取决于其中是否配置了 match local address，其次决定于配置的优先级值，最后决定于配置 IKE profile 的先后顺序。

#### 2.6 配置IKE提议

##### 1. IKE提议及匹配机制简介

IKE 定义了一套属性数据来描述 IKE 第一阶段使用怎样的参数来与对端进行协商。用户可以创建多条不同优先级的 IKE 提议。协商双方必须至少有一条匹配的 IKE 提议才能协商成功。
在进行 IKE 协商时，协商发起方会将自己的 IKE 提议发送给对端，由对端进行匹配。
• 若发起方使用的 IPsec 安全策略中没有引用 IKE profile，则会将当前系统中所有的 IKE 提议发送给对端，这些 提议的优先级顺序由 提议的序号决定，序号越小优先级越高；
IKE IKE若发起方的 策略中引用了 profile，则会将该 中引用的所有 提议发
• IPsec IKE IKE profile IKE送给对端，这些 IKE 提议的优先级由引用的先后顺序决定，先引用的优先级高。
协商响应方则以对端发送的 IKE 提议优先级从高到低的顺序与本端所有的 IKE 提议进行匹配，直到找到一个匹配的提议来使用。匹配的 IKE 提议将被用来建立 IKE SA。
以上 IKE 提议的匹配原则是：协商双方具有相同的加密算法、认证方法、认证算法和 DH group 标识。匹配的 IKE 提议的 IKE SA 存活时间则取两端的最小值。

##### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 创建 IKE 提议，并进入 IKE 提议视图。
ike proposal proposal-number缺省情况下，存在一个缺省的 IKE 提议。
(3) 配置 IKE 提议的描述信息。
description不存在 IKE 提议的描述信息。
(4) 指定一个供 IKE 提议使用的加密算法。
（非 FIPS 模式）
encryption-algorithm { 3des-cbc | aes-cbc-128 | aes-cbc-192 | aes-cbc-256 | des-cbc }缺省情况下，IKE 提议使用 CBC 模式的 56-bit DES 加密算法。
（FIPS 模式）
encryption-algorithm { aes-cbc-128 | aes-cbc-192 | aes-cbc-256 }

缺省情况下，IKE 提议使用 CBC 模式的 128-bit AES 加密算法。
(5) 指定一个供 IKE 提议使用的认证方法。
authentication-method { dsa-signature | pre-share | rsa-signature }缺省情况下，IKE 提议使用预共享密钥的认证方法。
(6) 指定一个供 IKE 提议使用的认证算法。
（非 FIPS 模式）
authentication-algorithm { md5 | sha | sha256 | sha384 | sha512 }缺省情况下，IKE 提议使用 HMAC-SHA1 认证算法。
（FIPS 模式）
authentication-algorithm { sha | sha256 | sha384 | sha512 }缺省情况下，IKE 提议使用 HMAC-SHA256 认证算法。
(7) 配置 IKE 第一阶段密钥协商时所使用的 DH 密钥交换参数。
（非 FIPS 模式）
dh { group1 | group14 | group2 | group24 | group5 }缺省情况下，IKE 第一阶段密钥协商时所使用的 密钥交换参数为 group1，即 的DH 768-bit Diffie-Hellman group。
（FIPS 模式）
dh group14缺省情况下，IKE 第一阶段密钥协商时所使用的 DH 密钥交换参数为 group14，即 2048-bit的 Diffie-Hellman group。
(8) （可选）指定一个 IKE 提议的 IKE SA 存活时间。
sa duration seconds缺省情况下，IKE 提议的 IKE SA 存活时间为 86400 秒。

#### 2.7 配置IKE keychain

##### 1. IKE keychain及参数简介

在 IKE 需要通过预共享密钥方式进行身份认证时，协商双方需要创建并指定 IKE keychain。IKE用于配置协商双方的密钥信息，具体包括以下内容：
keychain预共享密钥。IKE 协商双方配置的预共享密钥必须相同，否则身份认证会失败。以明文或密文
•方式设置的预共享密钥，均以密文的方式保存在配置文件中。
• IKE keychain 的使用范围。限制 keychain 的使用范围，即 IKE keychain 只能在指定的地址或指定接口对应的地址下使用（这里的地址指的是 IPsec 安全策略/IPsec 安全策略模板下配置的本端地址，若本端地址没有配置，则为引用 IPsec 安全策略的接口的 IP 地址）。
IKE keychain 的优先级。配置了 match local address 的 IKE keychain 的优先级高于所
•有未配置 的 keychain。即 的优先级首先决定于match local address IKE IKE keychain是否配置了 match local address ，其次取决于配置的优先级，最后决定于配置 IKE keychain 的先后顺序。

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 创建 IKE keychain，并进入 IKE keychain 视图。
ike keychain keychain-name [ vpn-instance vpn-instance-name ]
(3) 配置预共享密钥。
（非 FIPS 模式）
pre-shared-key { address { ipv4-address [ mask | mask-length ] | ipv6
ipv6-address [ prefix-length ] } | hostname host-name } key { cipher |
simple } string
（FIPS 模式）
pre-shared-key { address { ipv4-address [ mask | mask-length ] | ipv6
ipv6-address [ prefix-length ] } | hostname host-name } key [ cipher
string ]
缺省情况下，未配置预共享密钥。
（可选）配置 的使用范围。
(4) IKE keychain
match local address { interface-type interface-number | { ipv4-address
| ipv6 ipv6-address } [ vpn-instance vpn-instance-name ] }
缺省情况下，未限制 IKE keychain 的使用范围。
(5) （可选）配置 IKE keychain 的优先级。
priority priority
缺省情况下，IKE 的优先级为 100。
keychain

#### 2.8 配置本端身份信息

##### 1. 配置限制与指导

本端身份信息适用于所有 IKE SA 的协商，而 IKE profile 下的 local-identity 仅适用于本 IKE profile。如果 IKE profile 下没有配置本端身份，则默认使用此处配置的全局本端身份。
如果本端采用的认证方式为数字签名，则本端配置的任何类型的身份信息都有效；
•
• 如果本端采用认证方式为预共享密钥，则本端除 DN 之外的其它类型的身份信息均有效。

##### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 配置本端身份信息。
ike identity { address { ipv4-address | ipv6 ipv6-address }| dn | fqdn [ fqdn-name ] | user-fqdn [ user-fqdn-name ] }缺省情况下，使用 地址标识本端的身份，该 地址为 安全策略或 安全策略模IP IP IPsec IPsec板应用的接口地址。
(3) （可选）配置当使用数字签名认证方式时，本端的身份总从证书的主题字段中获得。

##### 3. 配置步骤

##### 1. 功能简介

ike signature-identity from-certificate缺省情况下，本端身份信息由 local-identity 或 ike identity 命令指定。
在采用 IPsec野蛮协商模式且使用数字签名认证方式的情况下，与仅支持使用 DN类型的身份进行数字签名认证的 设备互通时需要配置本命令。
ComwareV5

#### 2.9 配置IKE Keepalive功能

##### 1. 功能简介

IKE Keepalive 功能用于检测对端是否存活。在对端配置了等待 IKE Keepalive 报文的超时时间后，必须在本端配置发送 IKE Keepalive 报文的时间间隔。当对端 IKE SA 在配置的超时时间内未收到报文时，则删除该 以及由其协商的 SA。
IKE Keepalive IKE SA IPsec

##### 2. 配置限制和指导

• 当有检测对方是否存活的需求时，通常建议配置 IKE DPD，不建议配置 IKE Keepalive。仅当
对方不支持 IKE DPD 功能且支持 IKE Keepalive 功能时，才考虑配置 IKE Keepalive 功能。配
置 IKE Keepalive 功能后，会定时检测对方是否存活，因此会额外消耗网络带宽和计算资源。
• 本端配置的 IKE Keepalive 报文的等待超时时间要大于对端发送的时间间隔。由于网络中一般
不会出现超过连续三次的报文丢失，所以，本端的超时时间可以配置为对端配置的发送
IKE
Keepalive 报文的时间间隔的三倍。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 配置通过 IKE SA 向对端发送 IKE Keepalive 报文的时间间隔。
ike keepalive interval interval
缺省情况下，不向对端发送 IKE Keepalive 报文。
(3) 配置本端等待对端发送 IKE Keepalive 报文的超时时间。
ike keepalive timeout seconds
缺省情况下，永不超时，一直等待对端发送 IKE Keepalive 报文。

#### 2.10 配置IKE NAT Keepalive功能

功能简介
1.
在采用 IKE 协商建立的 IPsec 隧道中，可能存在 NAT 设备，由于在 NAT 设备上的 NAT 会话有一定存活时间，一旦 IPsec 隧道建立后如果长时间没有流量，对应的 NAT 会话表项会被删除，这样将导致 隧道无法继续传输数据。为防止 表项老化，NAT 内侧的 网关设备需要定时向IPsec NAT IKE NAT外侧的 IKE 网关设备发送 NAT Keepalive 报文，以便维持 NAT 设备上对应的 IPsec 流量的会话存活，从而让 NAT 外侧的设备可以访问 NAT 内侧的设备。

##### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 配置向对端发送 NAT Keepalive 报文的时间间隔。

##### 1. 功能简介

ike nat-keepalive seconds缺省情况下，向对端发送 NAT Keepalive 报文的时间间隔为 20 秒。

#### 2.11 配置全局IKE DPD功能

##### 1. 功能简介

DPD（Dead Peer Detection，对等体存活检测）用于检测对端是否存活。本端主动向对端发送 DPD请求报文，对对端是否存活进行检测。如果本端在 DPD 报文的重传时间间隔（retry seconds）
内未收到对端发送的 DPD 回应报文，则重传 DPD 请求报文，若重传两次之后仍然没有收到对端的回应报文，则删除该 和对应的 SA。
DPD IKE SA IPsec

##### 2. 配置限制和指导

• IKE DPD 有两种模式：按需探测模式（on-demand）和定时探测模式（periodic）。一般若
无特别要求，建议使用按需探测模式，在此模式下，仅在本端需要发送报文时，才会触发探
测；如果需要尽快地检测出对端的状态，则可以使用定时探测模式。在定时探测模式下工作，
会消耗更多的带宽和计算资源，因此当设备与大量的 对端通信时，应优先考虑使用按需
IKE
探测模式。
• 如果 IKE profile 视图下和系统视图下都配置了 DPD 探测功能，则 IKE profile 视图下的 DPD
配置生效，如果IKE profile视图下没有配置DPD探测功能，则采用系统视图下的DPD配置。
• 建议配置的触发 IKE DPD 探测的时间间隔大于 DPD 报文的重传时间间隔，使得直到当前 DPD
探测结束才可以触发下一次 DPD 探测，DPD 在重传过程中不触发新的 DPD 探测。
以定时探测模式为例，若本端的 IKE DPD 配置如下：ike dpd interval 10 retry 6
•
则，具体的探测过程为：IKE SA协商成功之后 10秒，本端会发送 DPD探测报文，
periodi
并等待接收 DPD 回应报文。若本端在 6 秒内没有收到 DPD 回应报文，则会第二次发送 DPD
探测报文。在此过程中总共会发送三次 DPD 探测报文，若第三次 DPD 探测报文发出后 6 秒
仍没收到 回应报文，则会删除发送 探测报文的 及其对应的所有 SA。
DPD DPD IKE SA IPsec
若在此过程中收到了 DPD 回应报文，则会等待 10 秒再次发送 DPD 探测报文。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置 IKE DPD 功能。
ike dpd interval interval [ retry seconds ] { on-demand | periodic }
缺省情况下，IKE DPD 功能处于关闭状态。

#### 2.12 配置针对无效IPsec SPI的IKE SA恢复功能

功能简介
1.
当 IPsec 隧道一端的安全网关出现问题（例如安全网关重启）导致其 IPsec SA 丢失时，会造成 IPsec流量黑洞现象：一端（接收端）的 已经丢失，而另一端（发送端）还持有对应的IPsec SA IPsec SA且不断地向对端发送报文，当接收端收到发送端使用此 IPsec SA 封装的 IPsec 报文时，就会因为找不到对应的 SA 而持续丢弃报文，形成流量黑洞。该现象造成 IPsec 通信链路长时间得不到恢复

（只有等到发送端旧的 IPsec SA 生命周期超时，并重建 IPsec SA 后，两端的 IPsec 流量才能得以恢复），因此需要采取有效的 恢复手段来快速恢复中断的 通信链路。
IPsec SA IPsec由 唯一标识，接收方根据 报文中的 在 数据库中查找对应的 SA，IPsec SA SPI IPsec SPI SA IPsec若接收方找不到处理该报文的 IPsec SA，则认为此报文的 SPI 无效。如果接收端当前存在 IKE SA，则会向对端发送删除对应 IPsec SA 的通知消息，发送端 IKE 接收到此通知消息后，就会立即删除此无效 对应的 SA。之后，当发送端需要继续向接收端发送报文时，就会触发两端重建SPI IPsec IPsec SA，使得中断的 IPsec 通信链路得以恢复；如果接收端当前不存在 IKE SA，就不会触发本端向对端发送删除 IPsec SA 的通知消息，接收端将默认丢弃无效 SPI 的 IPsec 报文，使得链路无法恢复。后一种情况下，如果开启了 IPsec 无效 SPI 恢复 IKE SA 功能，就会触发本端与对端协商新的 并发送删除消息给对端，从而使链路恢复正常。
IKE SA

##### 2. 配置限制和指导

由于开启此功能后，若攻击者伪造大量源 IP 地址不同但目的 IP 地址相同的无效 SPI 报文发给设备，会导致设备因忙于与无效对端协商建立 IKE SA 而面临受到 DoS（Denial of Sevice）攻击的风险。
因此，建议通常不要打开 ike invalid-spi-recovery enable 功能。

##### 3. 配置步骤

进入系统视图。
(1)
system-view开启针对无效 的 恢复功能。
(2) IPsec SPI IKE SA ike invalid-spi-recovery enable缺省情况下，针对无效 的 恢复功能处于关闭状态。
IPsec SPI IKE SA

#### 2.13 配置对IKE SA数目的限制

##### 1. 功能简介

由于不同设备的能力不同，为充分利用设备的处理能力，可以配置允许同时处于协商状态的 IKE SA的最大数，也可以配置允许建立的 IKE SA 的最大数。
若设置允许同时协商更多的 IKE SA，则可以充分利用设备处理能力，以便在设备有较强处理能力的情况下得到更高的新建性能；若设置允许同时协商较少的 IKE SA，则可以避免产生大量不能完成协商的 SA，以便在设备处理能力较弱时保证一定的新建性能。
IKE若设置允许建立更多的 SA，则可以使得设备在有充足内存的情况下得到更高的并发性能；若IKE设置允许建立较少的 IKE SA，则可以在设备没有充足内存的情况下，使得 IKE 不过多占用系统内存。

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置对本端 IKE SA 数目的限制。
ike limit { max-negotiating-sa negotiation-limit | max-sa sa-limit }
缺省情况下，不限制允许同时处于协商状态的 IKE SA 数目，也不限制允许建立的 IKE SA 的
最大数目。

#### 2.14 配置IKE告警功能

##### 1. 功能简介

开启 的告警功能后，IKE 会生成告警信息，用于向网管软件报告该模块的重要事件。生成的告IKE警信息将被发送到设备的 SNMP 模块，通过设置 SNMP 中告警信息的发送参数，来决定告警信息输出的相关属性。有关告警信息的详细介绍，请参见“网络管理和监控配置指导”中的“SNMP”。
如果希望生成并输出某种类型的 IKE 告警信息，则需要保证 IKE 的全局告警功能以及相应类型的告警功能均处于开启状态。

##### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 开启 IKE 的全局告警功能。
snmp-agent trap enable ike global缺省情况下，IKE 的告警 Trap 功能处于关闭状态。
(3) 开启 IKE 的指定告警功能。
snmp-agent trap enable ike [ attr-not-support | auth-failure | cert-type-unsupport | cert-unavailable | decrypt-failure | encrypt-failure | invalid-cert-auth | invalid-cookie | invalid-id | invalid-proposal | invalid-protocol | invalid-sign | no-sa-failure | proposal-add | proposal–delete | tunnel-start | tunnel-stop | unsupport-exch-type ] *缺省情况下，IKE 的所有告警功能均处于关闭状态。

#### 2.15 IKE显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 IKE 的运行情况，通过查看显示信息验证配置的效果。
在用户视图下执行 命令可以删除 SA。
reset IKE表2-1 IKE 显示和维护操作 命令显示所有IKE提议的配置信息 display ike proposal display ike sa [ verbose [ connection-id connection-id | remote-address [ ipv6 ]显示当前IKE SA的信息remote-address [ vpn-instance vpn-instance-name ] ] ] display ike statistics显示IKE的统计信息reset ike sa [ connection-id清除 IKE SA connection-id ]清除IKE的MIB统计信息 reset ike statistics

#### 2.16 IKE典型配置举例

##### 2.16.1 IKE主模式及预共享密钥认证配置举例

###### 1. 组网需求

在 Switch A 和 Switch B 之间建立一个 IPsec 隧道，对 Switch A 和 Switch B 之间的数据流进行安全保护。
• Switch A 和 Switch B 之间采用 IKE 协商方式建立 IPsec SA。
• 使用缺省的 IKE 提议。
• 使用缺省的预共享密钥认证方法。

###### 2. 组网图

图2-4 IKE 主模式及预共享密钥认证典型组网图

###### 3. 配置步骤

请保证 与 之间路由可达。
Switch A Switch B
(1) 配置 Switch A \# 配置 Vlan-interface1 的 IP 地址。
<SwitchA> system-view [SwitchA] interface vlan-interface 1 [SwitchA-vlan-interface1] ip address 1.1.1.1 255.255.0.0 [SwitchA-vlan-interface1] quit \# 配置 ACL 3101 ，定义 Switch A 和 Switch B 之间的数据流。
[SwitchA] acl advanced 3101 [SwitchA-acl-ipv4-adv-3101] rule 0 permit ip source 1.1.1.1 0 destination 2.2.2.2 0 [SwitchA-acl-ipv4-adv-3101] quit \# 配置安全提议 tran1。
[SwitchA] ipsec transform-set tran1 \# 配置安全协议对 IP 报文的封装形式为隧道模式。
[SwitchA-ipsec-transform-set-tran1] encapsulation-mode tunnel \# 配置采用的安全协议为 ESP。
[SwitchA-ipsec-transform-set-tran1] protocol esp配置 协议采用的加密算法为 AES-CBC-192，认证算法为 HMAC-SHA1。
\# ESP [SwitchA-ipsec-transform-set-tran1] esp encryption-algorithm aes-cbc-192 [SwitchA-ipsec-transform-set-tran1] esp authentication-algorithm sha1

[SwitchA-ipsec-transform-set-tran1] quit \# 创建 IKE keychain，名称为 keychain1。
[SwitchA] ike keychain keychain1配置与 地址为 的对端使用的预共享密钥为明文 12345zxcvb!@#$%ZXCVB。
\# IP 2.2.2.2 [SwitchA-ike-keychain-keychain1] pre-shared-key address 2.2.2.2 255.255.0.0 key simple 12345zxcvb!@#$%ZXCVB [SwitchA-ike-keychain-keychain1] quit \# 创建 IKE profile，名称为 profile1。
[SwitchA] ike profile profile1指定引用的 为 keychain1。
\# IKE keychain [SwitchA-ike-profile-profile1] keychain keychain1 \# 配置匹配对端身份的规则为 IP 地址 2.2.2.2/16。
[SwitchA-ike-profile-profile1] match remote identity address 2.2.2.2 255.255.0.0 [SwitchA-ike-profile-profile1] quit创建一条 协商方式的 安全策略，名称为 map1，顺序号为 10。
\# IKE IPsec [SwitchA] ipsec policy map1 10 isakmp \# 配置 IPsec 隧道的对端 IP 地址为 2.2.2.2。
[SwitchA-ipsec-policy-isakmp-map1-10] remote-address 2.2.2.2 \# 指定引用 ACL 3101。
[SwitchA-ipsec-policy-isakmp-map1-10] security acl 3101 \# 指定引用的安全提议为 tran1。
[SwitchA-ipsec-policy-isakmp-map1-10] transform-set tran1 \# 指定引用的 IKE profile 为 profile1。
[SwitchA-ipsec-policy-isakmp-map1-10] ike-profile profile1 [SwitchA-ipsec-policy-isakmp-map1-10] quit \# 在 Vlan-interface1 上应用安全策略组。
[SwitchA] interface vlan-interface 1 [SwitchA-Vlan-interface1] ipsec apply policy map1配置
(2) Switch B配置 的 地址。
\# Vlan-interface1 IP <SwitchB> system-view [SwitchB] interface Vlan-interface1 [SwitchB-Vlan-interface1] ip address 2.2.2.2 255.255.0.0 [SwitchB-Vlan-interface1] quit \# 配置 ACL 3101，定义 Switch B 和 Switch A 之间的数据流。
[SwitchB] acl number 3101 [SwitchB-acl-adv-3101] rule 0 permit ip source 2.2.2.2 0 destination 1.1.1.1 0 [SwitchB-acl-adv-3101] quit \# 创建 IPsec 安全提议 tran1。
[SwitchB] ipsec transform-set tran1配置安全协议对 报文的封装形式为隧道模式。
\# IP [SwitchB-ipsec-transform-set-tran1] encapsulation-mode tunnel \# 配置采用的安全协议为 ESP。
[SwitchB-ipsec-transform-set-tran1] protocol esp

###### 1. 组网需求

\# 配置 ESP 协议采用的加密算法为 AES-CBC-192，认证算法为 HMAC-SHA1。
[SwitchB-ipsec-transform-set-tran1] esp encryption-algorithm aes-cbc-192 [SwitchB-ipsec-transform-set-tran1] esp authentication-algorithm sha1 [SwitchB-ipsec-transform-set-tran1] quit \# 创建 IKE keychain，名称为 keychain1。
[SwitchB]ike keychain keychain1 \# 配置与 IP 地址为 1.1.1.1 的对端使用的预共享密钥为明文 12345zxcvb!@#$%ZXCVB。
[SwitchB-ike-keychain-keychain1] pre-shared-key address 1.1.1.1 255.255.0.0 key simple 12345zxcvb!@#$%ZXCVB [SwitchB-ike-keychain-keychain1] quit \# 创建 IKE profile，名称为 profile1。
[SwitchB] ike profile profile1 \# 指定引用的 IKE keychain 为 keychain1。
[SwitchB-ike-profile-profile1] keychain keychain1配置匹配对端身份的规则为 地址 1.1.1.1/16。
\# IP [SwitchB-ike-profile-profile1] match remote identity address 1.1.1.1 255.255.0.0 [SwitchB-ike-profile-profile1] quit \# 创建一条 IKE 协商方式的 IPsec 安全策略，名称为 use1，顺序号为 10。
[SwitchB] ipsec policy use1 10 isakmp \# 配置 IPsec 隧道的对端 IP 地址为 1.1.1.1。
[SwitchB-ipsec-policy-isakmp-use1-10] remote-address 1.1.1.1 \# 指定引用 ACL 3101。
[SwitchB-ipsec-policy-isakmp-use1-10] security acl 3101指定引用的安全提议为 tran1。
\# [SwitchB-ipsec-policy-isakmp-use1-10] transform-set tran1 \# 指定引用的 IKE profile 为 profile1。
[SwitchB-ipsec-policy-isakmp-use1-10] ike-profile profile1 [SwitchB-ipsec-policy-isakmp-use1-10] quit在 上应用安全策略组。
\# Vlan-interface1 [SwitchB] interface vlan-interface 1 [SwitchB-Vlan-interface1] ipsec apply policy use1

###### 4. 验证配置结果

以上配置完成后，Switch A 和 Switch B 之间如果有端到端的报文发送或接收，将触发 IKE 协商。

##### 2.16.2 采用IKE方式建立保护IPv4报文的IPsec隧道

组网需求
1.
在 Switch A 和 Switch B 之间建立一条 IPsec 隧道，对 Switch A 与 Switch B 之间的数据流进行安全保护。具体要求如下：
封装形式为隧道模式。
•安全协议采用 ESP 协议。
•加密算法采用 AES-CBC-192，认证算法采用 HMAC-SHA1。
•
• IKE 协商方式建立 IPsec SA。

###### 2. 组网图

图2-5 保护 IPv4 报文的 IPsec 配置组网图

###### 3. 配置步骤

配置
(1) Switch A配置 接口的 地址。
\# Vlan-interface1 IP <SwitchA> system-view [SwitchA] interface vlan-interface 1 [SwitchA-Vlan-interface1] ip address 2.2.2.1 255.255.255.0 [SwitchA-Vlan-interface1] quit \# 配置一个访问控制列表，定义由 Switch A 去 Switch B 的数据流。
[SwitchA] acl advanced 3101 [SwitchA-acl-ipv4-adv-3101] rule 0 permit ip source 2.2.2.1 0 destination 2.2.3.1 0 [SwitchA-acl-ipv4-adv-3101] quit \# 创建 IPsec 安全提议 tran1。
[SwitchA] ipsec transform-set tran1 \# 配置安全协议对 IP 报文的封装形式为隧道模式。
[SwitchA-ipsec-transform-set-tran1] encapsulation-mode tunnel \# 配置采用的安全协议为 ESP。
[SwitchA-ipsec-transform-set-tran1] protocol esp \# 配置 ESP 协议采用的加密算法为 AES-CBC-192，认证算法为 HMAC-SHA1。
[SwitchA-ipsec-transform-set-tran1] esp encryption-algorithm aes-cbc-192 [SwitchA-ipsec-transform-set-tran1] esp authentication-algorithm sha1 [SwitchA-ipsec-transform-set-tran1] quit \# 创建并配置 IKE keychain，名称为 keychain1。
[SwitchA] ike keychain keychain1配置与 地址为 的对端使用的预共享密钥为明文 。
\# IP 2.2.3.1 12345zxcvb!@#$%ZXCVB [SwitchA-ike-keychain-keychain1] pre-shared-key address 2.2.3.1 255.255.255.0 key simple 12345zxcvb!@#$%ZXCVB [SwitchA-ike-keychain-keychain1] quit \# 创建并配置 IKE profile，名称为 profile1。
[SwitchA] ike profile profile1 [SwitchA-ike-profile-profile1] keychain keychain1 [SwitchA-ike-profile-profile1] match remote identity address 2.2.3.1 255.255.255.0 [SwitchA-ike-profile-profile1] quit创建一条 协商方式的 安全策略，名称为 map1，序列号为 10。
\# IKE IPsec [SwitchA] ipsec policy map1 10 isakmp \# 指定引用 ACL 3101。
[SwitchA-ipsec-policy-isakmp-map1-10] security acl 3101

\# 指定引用的安全提议为 tran1。
[SwitchA-ipsec-policy-isakmp-map1-10] transform-set tran1 \# 指定 IPsec 隧道的本端 IP 地址为 2.2.2.1，对端 IP 地址为 2.2.3.1。
[SwitchA-ipsec-policy-isakmp-map1-10] local-address 2.2.2.1 [SwitchA-ipsec-policy-isakmp-map1-10] remote-address 2.2.3.1 \# 指定引用的 IKE profile 为 profile1。
[SwitchA-ipsec-policy-isakmp-map1-10] ike-profile profile1 [SwitchA-ipsec-policy-isakmp-map1-10] quit在 接口上应用安全策略组。
\# Vlan-interface1 [SwitchA] interface vlan-interface 1 [SwitchA-Vlan-interface1] ipsec apply policy map1
(2) 配置 Switch B \# 配置 Vlan-interface1 接口的 IP 地址。
<SwitchB> system-view [SwitchB] interface vlan-interface 1 [SwitchB-Vlan-interface1] ip address 2.2.3.1 255.255.255.0 [SwitchB-Vlan-interface1] quit \# 配置一个访问控制列表，定义由 Switch B 去 Switch A 的数据流。
[SwitchB] acl advanced 3101 [SwitchB-acl-ipv4-adv-3101] rule 0 permit ip source 2.2.3.1 0 destination 2.2.2.1 0 [SwitchB-acl-ipv4-adv-3101] quit \# 创建 IPsec 安全提议 tran1。
[SwitchB] ipsec transform-set tran1 \# 配置安全协议对 IP 报文的封装形式为隧道模式。
[SwitchB-ipsec-transform-set-tran1] encapsulation-mode tunnel配置采用的安全协议为 ESP。
\# [SwitchB-ipsec-transform-set-tran1] protocol esp \# 配置 ESP 协议采用的加密算法为 AES-CBC-192，认证算法为 HMAC-SHA1。
[SwitchB-ipsec-transform-set-tran1] esp encryption-algorithm aes-cbc-192 [SwitchB-ipsec-transform-set-tran1] esp authentication-algorithm sha1 [SwitchB-ipsec-transform-set-tran1] quit \# 创建并配置 IKE keychain，名称为 keychain1。
[SwitchB] ike keychain keychain1 \# 配置与 IP 地址为 2.2.2.1 的对端使用的预共享密钥为明文 12345zxcvb!@#$%ZXCVB。
[SwitchB-ike-keychain-keychain1] pre-shared-key address 2.2.2.1 255.255.255.0 key simple 12345zxcvb!@#$%ZXCVB [SwitchB-ike-keychain-keychain1] quit \# 创建并配置 IKE profile，名称为 profile1。
[SwitchB] ike profile profile1 [SwitchB-ike-profile-profile1] keychain keychain1 [SwitchB-ike-profile-profile1] match remote identity address 2.2.2.1 255.255.255.0 [SwitchB-ike-profile-profile1] quit \# 创建一条 IKE 协商方式的安全策略，名称为 use1，序列号为 10。
[SwitchB] ipsec policy use1 10 isakmp

\# 指定引用 ACL 3101。
[SwitchB-ipsec-policy-isakmp-use1-10] security acl 3101 \# 指定引用的 IPsec 安全提议为 tran1。
[SwitchB-ipsec-policy-isakmp-use1-10] transform-set tran1指定 隧道的本端 地址为 2.2.3.1，对端 地址为 2.2.2.1。
\# IPsec IP IP [SwitchB-ipsec-policy-isakmp-use1-10] local-address 2.2.3.1 [SwitchB-ipsec-policy-isakmp-use1-10] remote-address 2.2.2.1 \# 指定引用的 IKE 对等体为 profile1。
[SwitchB-ipsec-policy-isakmp-use1-10] ike-profile profile1 [SwitchB-ipsec-policy-isakmp-use1-10] quit \# 在 Vlan-interface1 接口上应用安全策略组。
[SwitchB] interface vlan-interface 1 [SwitchB-Vlan-interface1] ipsec apply policy use1

###### 4. 验证配置

以上配置完成后，Switch A 和 Switch B 之间如果有端到端的报文发送或接收，将触发 IKE 进行 IPsec SA 的协商。IKE 成功协商出 IPsec SA 后，Switch A 和 Switch B 之间数据流的传输将受到 IPsec SA的保护。

#### 2.17 常见错误配置举例

##### 2.17.1 提议不匹配导致IKE SA协商失败

###### 1. 故障现象

(1) 通过如下命令查看当前的 IKE SA 信息，发现 IKE SA 的状态（Flags 字段）为 Unknown。
<Sysname> display ike sa
Connection-ID Remote Flag DOI
------------------------------------------------------------------
1 192.168.222.5 Unknown IPsec
Flags:
RD--READY RL--REPLACED FD-FADING RK-REKEY
(2) 打开 IKE 事件和报文调试信息开关后分别可以看到如下调试信息。
IKE 事件调试信息：
The attributes are unacceptable.
IKE 报文调试信息：
Construct notification packet: NO_PROPOSAL_CHOSEN.

###### 2. 故障分析

IKE 提议配置错误。

###### 3. 处理过程

排查 提议相关配置。具体包括：检查两端的 提议是否匹配，即 提议中的认证方
(1) IKE IKE IKE法、认证算法、加密算法是否匹配。
(2) 修改 IKE 提议的配置，使本端 IKE 提议的配置和对端匹配。

###### 1. 故障现象

##### 2.17.2 未正确引用IKE提议或IKE keychain导致IKE SA协商失败

故障现象
1.
(1) 通过如下命令查看当前的 IKE SA 信息，发现 IKE SA 的状态（Flags 字段）为 Unknown。
<Sysname> display ike sa Connection-ID Remote Flag DOI
------------------------------------------------------------------ 1 192.168.222.5 Unknown IPsec Flags:
RD--READY RL--REPLACED FD-FADING RK-REKEY
(2) 打开 IKE 事件和报文调试信息开关后分别可以看到如下调试信息。
IKE 事件调试信息：
Notification PAYLOAD_MALFORMED is received.
IKE 报文调试信息：
Construct notification packet: PAYLOAD_MALFORMED.

###### 2. 故障分析

故障原因可能为以下两点：
匹配到的 中没有引用协商过程中匹配到的 提议。
(1) IKE profile IKE通过调试信息看到：
Failed to find proposal 1 in profile profile1.
(2) 匹配到的 IKE profile 中没有引用协商过程中匹配到的 IKE keychain。
通过调试信息看到：
Failed to find keychain keychain1 in profile profile1.

###### 3. 处理过程

(1) 检查匹配到的 IKE 提议是否在 IKE profile 下引用。以故障分析中的调试信息为例，IKE profile
profile1 中需要引用 IKE proposal 1。
(2) 检查匹配到的 IKE keychain 是否在 IKE profile 下引用。以故障分析中的调试信息为例，IKE
中需要引用 keychain1。
profile profile1 IKE keychain

##### 2.17.3 提议不匹配导致IPsec SA协商失败

###### 1. 故障现象

通过 命令查看当前的 信息，发现 协商成功，其状态（Flags
(1) display ike sa IKE SA IKE SA字段）为 RD。但通过 display ipsec sa 命令查看当前的 IPsec SA 时，发现没有协商出相应的 IPsec SA。
(2) 打开 IKE 调试信息开关可以看到以下调试信息：
The attributes are unacceptable.
或者：
Construct notification packet: NO_PROPOSAL_CHOSEN.

###### 2. 故障分析

安全策略参数配置错误。
IPsec

###### 3. 处理过程

(1) 排查 IPsec 相关配置。具体包括：检查双方接口上应用的 IPsec 安全策略的参数是否匹配，即
引用的 IPsec 安全提议的协议、加密算法和认证算法是否匹配。
(2) 修改 IPsec 安全策略配置，使本端 IPsec 安全策略的配置和对端匹配。

##### 2.17.4 身份信息无效导致IPsec SA协商失败

###### 1. 故障现象

(1) 通过 display ike sa 命令查看当前的 IKE SA 信息，发现 IKE SA 协商成功，其状态（Flags
字段）为 RD。但通过 命令查看当前的 时，发现没有协商出
display ipsec sa IPsec SA
相应的 IPsec SA。
(2) 打开 IKE 调试信息开关可以看到以下调试信息：
Notification INVALID_ID_INFORMATION is received.
或者：
Failed to get IPsec policy when renegotiating IPsec SA. Delete IPsec SA.
Construct notification packet: INVALID_ID_INFORMATION.

###### 2. 故障分析

响应方 IPsec 安全策略配置错误，导致在 IKE 第二阶段协商时找不到 IPsec 安全策略，原因可能为如下几点：
(1) 通过 display ike sa verbose 命令查看 IKE 一阶段协商中是否找到匹配的 IKE profile。
若没有找到 profile，则会查找全局的 参数，因此就要求这种情况下 安全策略中IKE IKE IPsec不能引用任何 IKE profile，否则协商失败。
通过如下显示信息可以看到，IKE SA 在协商过程中没有找到匹配的 IKE profile：
<Sysname> display ike sa verbose
----------------------------------------------- Connection ID: 3 Outside VPN:
Inside VPN:
Profile:
Transmitting entity: Responder
----------------------------------------------- Local IP: 192.168.222.5 Local ID type: IPV4_ADDR Local ID: 192.168.222.5 Remote IP: 192.168.222.71 Remote ID type: IPV4_ADDR Remote ID: 192.168.222.71 Authentication-method: PRE-SHARED-KEY Authentication-algorithm: MD5 Encryption-algorithm: 3DES-CBC Life duration(sec): 86400

Remaining key duration(sec): 85847 Exchange-mode: Main Diffie-Hellman group: Group 1 NAT traversal: Not detected但在 IPsec 策略中引用了 IKE profile profile1：
[Sysname] display ipsec policy
------------------------------------------- IPsec Policy: policy1 Interface: Ten-GigabitEthernet1/0/1
-------------------------------------------
----------------------------- Sequence number: 1 Mode: ISAKMP
----------------------------- Description:
Security data flow: 3000 Selector mode: aggregation Local address: 192.168.222.5 Remote address: 192.168.222.71 Transform set: transform1 IKE profile: profile1 SA duration(time based):
SA duration(traffic based):
SA idle time:
(2) 查看 IPsec 安全策略中引用的 ACL 配置是否正确。
例如，如发起方 ACL 流范围为网段到网段：
[Sysname] display acl 3000 Advanced IPv4 ACL 3000, 1 rule, ACL's step is 5 rule 0 permit ip source 192.168.222.0 0.0.0.255 destination 192.168.222.0 0.0.0.255响应方 ACL 流范围为主机到主机：
[Sysname] display acl 3000 Advanced IPv4 ACL 3000, 1 rule, ACL's step is 5 rule 0 permit ip source 192.168.222.71 0 destination 192.168.222.5 0以上配置中，响应方 规则定义的流范围小于发起方 规则定义的流范围，这会导致ACL ACL IPsec SA 协商失败。
(3) IPsec 安全策略配置不完整。具体包括：没有配置对端地址、没有配置 IPsec 提议、IPsec 提议配置不完整。
例如，如下 IPsec 安全策略中没有配置隧道的对端 IP 地址，因此 IPsec 安全策略是不完整的：
[Sysname] display ipsec policy
------------------------------------------- IPsec Policy: policy1 Interface: Ten-GigabitEthernet1/0/1

-------------------------------------------
-----------------------------
Sequence number: 1
Mode: ISAKMP
-----------------------------
Security data flow: 3000
Selector mode: aggregation
Local address: 192.168.222.5
Remote address:
Transform set: transform1
IKE profile: profile1
SA duration(time based):
SA duration(traffic based):
SA idle time:

###### 3. 处理过程

若在 第一阶段协商过程中没有找到 profile，建议在响应方 安全策略中去掉对
(1) IKE IKE IPsec IKE profile 的引用或者调整 IKE profile 的配置使之能够与发起端相匹配。
(2) 若响应方 ACL 规则定义的流范围小于发起方 ACL 规则定义的流范围，建议修改响应方 ACL的流范围大于或等于发起方 ACL 的流范围。以故障分析（2）中的配置为例，可以将响应方流范围修改为：
ACL [Sysname] display acl 3000 Advanced IPv4 ACL 3000, 2 rules, ACL's step is 5 rule 0 permit ip source 192.168.222.0 0.0.0.255 destination 192.168.222.0 0.0.0.255
(3) 将 IPsec 安全策略配置完整。以故障分析中的（3）中的配置为例，需要在 IPsec 安全策略中配置隧道的对端 IP 地址。

### 3 IKEv2

3 IKEv2

#### 3.1 IKEv2简介

IKEv2（Internet 2，互联网密钥交换协议第 版）是第 版本的 协议（本Key Exchange Version 2 1 IKE文简称 IKEv1）的增强版本。IKEv2 与 IKEv1 相同，具有一套自保护机制，可以在不安全的网络上安全地进行身份认证、密钥分发、建立 IPsec SA。相对于 IKEv1，IKEv2 具有抗攻击能力和密钥交换能力更强以及报文交互数量较少等特点。

##### 3.1.1 IKEv2的协商过程

要建立一对 IPsec SA，IKEv1 需要经历两个阶段，至少需要交换 6 条消息。在正常情况下，IKEv2只需要进行两次交互，使用 4 条消息就可以完成一个 IKEv2 SA 和一对 IPsec SA 的协商建立，如果要求建立的 的数目大于一对，则每增加一对 只需要额外增加一次交互，也就是IPsec SA IPsec SA两条消息就可以完成，这相比于 IKEv1 简化了设备的处理过程，提高了协商效率。
IKEv2 定义了三种交互：初始交换、创建子 SA 交换以及通知交换。
下面简单介绍一下 协商过程中的初始交换过程。
IKEv2图3-1 IKEv2 的初始交换过程Peer 1 Peer 2发送本地IKE策略确认对方使用的和密钥生成信息发起方策略和密钥信息 算法并产生密钥查找匹配的策略SA交换和并生成密钥接收方确认的策略和密钥交换密钥生成信息接受对端确认策略并生成密钥 发起方的身份、验证数据 验证对方身份并和IPsec提议 协商出IPsec SA ID交换验 身份验证、交换过程验证证及生成 响应方的身份、验证数据并协商出IPsec SA IPsec SA 和IPsec提议身份验证、交换过程验证并协商出IPsec SA如 图 3-1 所示，IKEv2 的初始交换过程中包含两个交换：IKE_SA_INIT交换（两条消息）和IKE_AUTH交换（两条消息）。
IKE_SA_INIT 交换：完成 IKEv2 SA 参数的协商以及密钥交换；
•
• IKE_AUTH 交换：完成通信对等体的身份认证以及 IPsec SA 的创建。
这两个交换过程顺序完成后，可以建立一个 IKEv2 SA 和一对 IPsec SA。

创建子 SA 交换：当一个 IKE SA 需要创建多个 IPsec SA 时，使用创建子 SA 交换来协商多于一个的 SA，另外还可用于进行 的重协商功能。
IKE SA通知交换：用于传递控制信息，例如错误信息或通告信息。

##### 3.1.2 IKEv2引入的新特性

###### 1. IKEv2支持DH猜想

在 IKE_SA_INIT 交换阶段，发起方采用“猜”的办法，猜一个响应方最可能使用的 DH 组携带在第一条消息中发送。响应方根据发起方“猜”的 DH 组来响应发起方。如果发起方猜测成功，则这样通过两条消息就可以完成 IKE_SA_INIT 交换。如果发起方猜测错误，则响应方会回应一个消息，并在该消息中指明将要使用的 组。之后，发起方采用响应方指INVALID_KE_PAYLOAD DH定的 DH 组重新发起协商。这种 DH 猜想机制，使得发起方的 DH 组配置更为灵活，可适应不同的响应方。

###### 2. IKEv2支持cookie-challenge机制

在 IKE_SA_INIT 交换中消息是明文传输的，响应方接收到第一个消息后无法确认该消息是否来自一个仿冒的地址。如果此时一个网络攻击者伪造大量地址向响应方发送 请求，根据IKE_SA_INIT IKEv1 协议，响应方需要维护这些半开的 IKE 会话信息，从而耗费大量响应方的系统资源，造成对响应方的 DoS 攻击。
IKEv2 使用 cookie-challenge 机制来解决这类 DoS 攻击问题。当响应方发现存在的半开 IKE SA 超过指定的数目时，就启用 机制。响应方收到 请求后，构造一个cookie-challenge IKE_SA_INIT Cookie通知载荷并响应发起方，若发起方能够正确携带收到的 Cookie 通知载荷向响应方重新发起IKE_SA_INIT 请求，则可以继续后续的协商过程。
半开状态的 IKEv2 SA 是指那些正在协商过程中的 IKEv2 SA。若半开状态的 IKEv2 SA 数目减少到阈值以下，则 cookie-challenge 功能将会停止工作

###### 3. IKEv2 SA重协商

为了保证安全，IKE 和 都有一个生命周期，超过生命周期的 需要重新协商，即SA IPsec SA SA SA的重协商。与 IKEv1 不同的是，IKEv2 SA 的生命周期不需要协商，由各自的配置决定，重协商总是由生命周期较小的一方发起，可尽量避免两端同时发起重协商造成冗余 SA 的生成，导致两端 SA状态不一致。

###### 4. IKEv2报文确认重传机制

与 不同，IKEv2 中所有消息都是以“请求–响应”对的形式出现，IKEv2 通过消息头中的一IKEv1个 Message ID 字段来标识一个“请求–响应”对。发起方发送的每一条消息都需要响应方给予确认，例如建立一个 IKE SA 一般需要两个“请求-响应”对。如果发起方在规定时间内没有接收到确认报文，则需要对该请求消息进行重传。IKEv2 消息的重传只能由发起方发起，且重传消息的 Message ID 必须与原始消息的 Message ID 一致。

##### 3.1.3 协议规范

与 IKEv2 相关的协议规范有：
• RFC 2408：Internet Security Association and Key Management Protocol (ISAKMP)
• RFC 4306：Internet Key Exchange (IKEv2) Protocol

RFC 4718：IKEv2 Clarifications and Implementation Guidelines
•RFC 2412：The OAKLEY Key Determination Protocol
•RFC 5996：Internet Key Exchange Protocol Version 2 (IKEv2)
•

#### 3.2 IKEv2配置任务简介

IKEv2 配置任务如下：
(1) 配置IKEv2 profile
a. 创建IKEv2 profile
b. 指定IKEv2 协商时本端和对端采用的身份认证方式
c. 配置Keychain或者PKI域
d. 配置本端身份信息
e. 配置匹配对端身份的规则
f. 配置IKEv2 profile所属的VPN实例配置内部VPN实例
g.
配置IKEv2 profile可选功能
h.
配置IKEv2 安全策略
(2)
配置IKEv2 安全提议
(3)
若 安全策略中指定了 提议，则必配。
IKEv2 IKEv2
(4) 配置IKEv2 keychain只要其中一端配置的认证方式为预共享密钥方式，则必选。
如果两端配置的认证方式都是 RSA 数字签名方式，则不需要配置。
(5) （可选）配置IKEv2 cookie-challenge功能该功能仅对于响应方有意义。
(6) （可选）配置全局IKEv2 DPD探测功能
(7) （可选）配置IKEv2 NAT Keepalive功能

#### 3.3 IKEv2配置准备

为了配置过程顺利进行，在 IKEv2 配置之前，用户需要确定以下几个因素：
• 确定 IKEv2 初始交换过程中使用的算法的强度，即确定对初始交换进行安全保护的强度（包括加密算法、完整性校验算法、PRF 算法和 DH 组算法）。不同的算法的强度不同，算法强度越高，受保护数据越难被破解，但消耗的计算资源越多。一般来说，密钥越长的算法强度越高。
确定本地认证方法以及对端的认证方法。若使用预共享密钥方式，则要确定通信双方预先约
•定的预共享密钥；若使用 RSA 数字签名方式，则要确定本端所使用的 PKI 域。关于 PKI 的配置，请参见“安全配置指导”中的“ PKI ”。

##### 3.4.1 创建IKEv2 profile

###### 2. 配置步骤

#### 3.4 配置IKEv2 profile

创建IKEv2
3.4.1 profile

###### 1. 功能简介

创建一个 IKEv2 profile，并进入 IKEv2 Profile 视图。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 创建一个 IKEv2 profile，并进入 IKEv2 Profile 视图。
ikev2 profile profile-name

##### 3.4.2 指定IKEv2协商时本端和对端采用的身份认证方式

###### 1. 配置限制与指导

IKEv2 协商时本端和对端采用的身份认证方式。只能指定一个本端身份认证方式，可以指定多个对端身份认证方式。本端和对端可以采用不同的身份认证方式。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 IKEv2 Profile 视图。
ikev2 profile profile-name
(3) 指定 IKEv2 本端和对端的身份认证方式。
authentication-method { local | remote } { dsa-signature |
ecdsa-signature | pre-share | rsa-signature }
缺省情况下，未配置本端和对端认证方式。

##### 3.4.3 配置Keychain或者PKI域

###### 1. 配置限制与指导

根据 IKEv2 profile 中配置的认证方法，配置 IKEv2 keychain 或 PKI 域。
如果任意一方指定的身份认证方式为数字签名（dsa-signature、rsa-signature 或者
•ecdsa-signature），则需要配置 域。
PKI如果任意一方指定的身份认证方式为预共享密钥（pre-share），则需要配置
• IKEv2 keychain。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 IKEv2 Profile 视图。
ikev2 profile profile-name

###### 2. 配置步骤

(3) 根据 IKEv2 profile 中配置的认证方法，配置 IKEv2 keychain 或 PKI 域
配置采用预共享密钥认证时使用的 Keychain
(cid:123)
keychain keychain-name
配置采用数字签名认证时使用的 PKI 域。
(cid:123)
certificate domain domain-name [ sign | verify ]
根据 authentication-method 命令使用的认证方法选择其中一个配置。

##### 3.4.4 配置本端身份信息

###### 1. 配置限制与指导

• 如果本端的认证方式为数字签名，则可以配置任何类型的身份信息。若配置的本端身份为 IP
地址，但这个 地址与本地证书中的 地址不同，设备将使用 类型的本端身份，该
IP IP FQDN
身份的内容为设备的名称（可通过 sysname 命令配置）。
• 如果本端的认证方式为预共享密钥，则只能配置除 DN 之外的其它类型的身份信息。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 IKEv2 Profile 视图。
ikev2 profile profile-name
(3) 配置本端身份信息。
identity local { address { ipv4-address | ipv6 ipv6-address } | dn | email
email-string | fqdn fqdn-name | key-id key-id-string }
缺省情况下，未配置本端身份信息。此时使用 IP 地址标识本端的身份，该 IP 地址为 IPsec 安
全策略应用的接口的 IP 地址。

##### 3.4.5 配置匹配对端身份的规则

###### 1. 功能简介

IKEv2 对等体需要根据对端的身份信息查找一个本端的 IKEv2 profile，然后使用此 IKEv2 profile 中的信息验证对端身份。对端身份信息若能满足本地某个 中指定的匹配规则，则该IKEv2 profile IKEv2 profile 为查找的结果。匹配 IKEv2 profile 的顺序取决于 IKEv2 profile 的优先级，优先级高的先匹配。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 IKEv2 Profile 视图。
ikev2 profile profile-name
(3) 配置匹配对端身份的规则。
match remote { certificate policy-name | identity { address { { ipv4-address [ mask | mask-length ] | range low-ipv4-address high-ipv4-address } | ipv6 { ipv6-address [ prefix-length ] | range

###### 2. 配置步骤

###### 2. 配置步骤

low-ipv6-address high-ipv6-address } } | fqdn fqdn-name | email email-string | key-id key-id-string } }协商双方都必须配置至少一个 规则，当对端的身份与 中配置的match remote IKEv2 profile match remote 规则匹配时，则使用此 IKEv2 profile 中的信息与对端完成认证。

##### 3.4.6 配置IKEv2 profile所属的VPN实例

###### 1. 功能简介

本功能限制 IKEv2 profile 只能在所属 VPN 实例的接口上协商。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 IKEv2 Profile 视图。
ikev2 profile profile-name
(3) 配置 IKEv2 profile 所属的 VPN 实例。
match vrf { name vrf-name | any }缺省情况下，IKEv2 profile 属于公网。

##### 3.4.7 配置内部VPN实例

###### 1. 功能简介

当 IPsec 解封装后的报文需要继续转发到不同的 VPN 时，设备需要知道在哪个 VPN 实例中查找相应的路由。缺省情况下，设备在与外网相同的 VPN 实例中查找路由，如果不希望在与外网相同的实例中查找路由，则可以指定一个内部 实例，通过查找该内部 实例的路由来转发报VPN VPN VPN文。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 IKEv2 Profile 视图。
ikev2 profile profile-name
(3) 配置内部 VPN 实例。
inside-vrf vrf-name缺省情况下，IKEv2 profile 未指定内部 VPN 实例，即内网与外网在同一个 VPN 中。

##### 3.4.8 配置IKEv2 profile可选功能

(1) 进入系统视图。
system-view
(2) 进入 IKEv2 Profile 视图。
ikev2 profile profile-name
(3) 配置 IKEv2 profile 的可选功能。

#### 3.5 配置IKEv2安全策略

配置 IKEv2 DPD 探测功能。
(cid:123)
dpd interval interval [ retry seconds ] { on-demand | periodic }缺省情况下，IKEv2 profile 视图下没有配置 DPD 探测功能，采用系统视图下的 DPD 配置。
若两者没有配置，则不进行 探测。
DPD配置 的使用范围。
IKEv2 profile (cid:123)
match local address { interface-type interface-number | ipv4-address | ipv6 ipv6-address }缺省情况下，未限制 IKEv2 profile 的使用范围。
限制 只能在指定的地址或指定接口的地址下使用（这里的地址指的是IKEv2 profile IPsec策略下配置的本端地址，若本端地址没有配置，则为引用 IPsec 策略的接口下地址）。
配置 IKEv2 profile 的优先级。
(cid:123)
priority priority缺省情况下，IKEv2 profile 的优先级为 100。
优先级仅用于响应方在查找 IKEv2 profile 时调整 IKEv2 profile 的匹配顺序。
配置 IKEv2 SA 生命周期。
(cid:123)
sa duration seconds缺省情况下，IKEv2 的生命周期为 秒。
SA 86400本端和对端的 生命周期可以不一致，也不需要进行协商，由生命周期较短的一IKEv2 SA方在本端 IKEv2 SA 生命周期到达之后发起重协商。
配置发送 NAT keepalive 的时间间隔。
(cid:123)
nat-keepalive seconds缺省条件下，使用全局的 配置。
IKEv2 NAT keepalive在 之间存在 网关的情况下，设备通过定期向对端发送 报IKEv2 peer NAT NAT keepalive文，防止已有的 NAT 会话表项因长时间无流量匹配而被老化。
开启指定的配置交换功能。
(cid:123)
config-exchange { request | set { accept | send } }缺省条件下，所有的配置交换功能均处于关闭状态。
该功能用于分支和总部虚拟隧道 IP 地址的请求和分配。
参数 说明request 用于分支侧向中心侧安全网关提交IP地址分配请求set accept 用于分支侧接受中心侧主动推送的IP地址set send 用于中心侧主动推送IP地址给分支侧配置 安全策略
3.5 IKEv2

##### 1. IKEv2安全策略及匹配机制简介

在进行 IKE_SA_INIT 协商时，系统需要查找到一个与本端相匹配的 IKEv2 安全策略，并使用其中引用的安全提议进行安全参数的协商，匹配的依据为本端安全网关的 IP 地址。

##### 1. 功能简介

若系统中配置了 IKEv2 安全策略，则根据本端安全网关的 IP 地址与所有已配置的 IKEv2 安全
•策略进行逐一匹配，如果未找到匹配的 安全策略或找到的安全策略中引用的安全提议IKEv2配置不完整，则 IKE_SA_INIT 协商将会失败。
• 若系统中未配置任何 IKEv2 安全策略，则直接采用缺省的 IKEv2 安全策略 default。
• 系统中存在多个 IKEv2 安全策略的情况下，系统根据安全策略的优先级从高到低的顺序依次匹配。如果通过 match local address 命令指定了匹配 IKEv2 安全策略的本端地址，则优先匹配指定了本端地址匹配条件的策略，其次匹配未指定本端地址匹配条件的策略。

##### 2. 配置步骤

进入系统视图。
(1)
system-view创建 安全策略，并进入 安全策略视图。
(2) IKEv2 IKEv2 ikev2 policy policy-name缺省情况下，存在一个名称为 的缺省 安全策略。
default IKEv2
(3) 指定匹配 IKEv2 安全策略的本端地址。
match local address { interface-type interface-number | ipv4-address | ipv6 ipv6-address }缺省情况下，未指定用于匹配 安全策略的本端地址，表示本策略可匹配所有本端地IKEv2址。
(4) 配置匹配 IKEv2 安全策略的 VPN 实例。
match vrf { name vrf-name | any }缺省情况下，未指定用于匹配 IKEv2 安全策略的 VPN 实例，表示本策略可匹配公网内的所有本端地址。
(5) 指定 IKEv2 安全策略引用的 IKEv2 安全提议。
proposal proposal-name缺省情况下，IKEv2 安全策略未引用 IKEv2 安全提议。
(6) 指定 IKEv2 安全策略的优先级。
priority priority缺省情况下，IKEv2 安全策略的优先级为 100。

#### 3.6 配置IKEv2安全提议

功能简介
1.
IKEv2 安全提议用于保存 IKE_SA_INIT 交换中使用的安全参数，包括加密算法、完整性验证算法、PRF 算法和 DH 组，其中每类安全参数均可以配置多个，其优先级按照配置顺序依次降低。

##### 2. 配置限制和指导

一个完整的 安全提议中至少应该包含一组安全参数，即一个加密算法、一个完整性验
• IKEv2证算法、一个 PRF 算法和一个 DH 组。
• 若同时指定了多个 IKEv2 安全提议，则它们的优先级按照配置顺序依次降低。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 创建 IKEv2 安全提议，并进入 IKEv2 提议视图。
ikev2 proposal proposal-name
缺省条件下，存在一个名称为 default 的缺省 IKEv2 安全提议。
非 FIPS 模式下，该提议中定义的加密算法为 aes-cbc-128 和 3des，完整性校验算法为
sha1 和 md5，PRF 算法为 sha1 和 md5，DH 组为 group5 和 group2。
FIPS模式下，该提议中定义的加密算法为 aes-cbc-128 和 aes-ctr-128，完整性校验算法
为 sha1 和 sha256，PRF 算法为 sha1 和 sha256，DH 组为 group14 和 group19。
(3) 指定 IKEv2 安全提议使用的加密算法。
（非 FIPS 模式）
encryption { 3des-cbc | aes-cbc-128 | aes-cbc-192 | aes-cbc-256 |
aes-ctr-128 | aes-ctr-192 | aes-ctr-256 | camellia-cbc-128 |
camellia-cbc-192 | camellia-cbc-256 | des-cbc } *
（FIPS 模式）
encryption { aes-cbc-128 | aes-cbc-192 | aes-cbc-256 | aes-ctr-128 |
aes-ctr-192 | aes-ctr-256 } *
缺省情况下，IKEv2 安全提议未定义加密算法。
(4) 指定 IKEv2 安全提议使用的完整性校验算法。
（非 FIPS 模式）
integrity { aes-xcbc-mac | md5 | sha1 | sha256 | sha384 | sha512 } *
（FIPS 模式）
integrity { sha1 | sha256 | sha384 | sha512 } *
缺省情况下，IKEv2 安全提议未定义完整性校验算法。
指定 安全提议使用的 组。
(5) IKEv2 DH
（非 FIPS 模式）
dh { group1 | group14 | group2 | group24 | group5 | group19 | group20 } *
（FIPS 模式）
dh { group14 | group19 | group20 } *
缺省情况下，IKEv2 安全提议未定义 DH 组。
(6) 指定 IKEv2 安全提议使用的 PRF 算法。
（非 FIPS 模式）
prf { aes-xcbc-mac | md5 | sha1 | sha256 | sha384 | sha512 } *
（FIPS 模式）
prf { sha1 | sha256 | sha384 | sha512 } *
缺省情况下，IKEv2 安全提议使用配置的完整性校验算法作为 PRF 算法。

###### 1. 功能简介

#### 3.7 配置IKEv2 keychain

##### 1. 功能简介

用来指定与对端进行 协商时使用的共享密钥信息。一个 下IKEv2 keychain IKEv2 IKEv2 keychain可以指定多个 IKEv2 peer，每个 IKEv2 peer 中包含了一个对称预共享密钥或一个非对称预共享密钥对，以及用于查找该 IKEv2 peer 的匹配参数（对等体的主机名称、IP 地址或地址范围、身份信息）。其中，IKEv2 协商的发起方使用对端的主机名称、IP 地址或地址范围查找 IKEv2 peer，响应方使用对端的 地址、地址范围或身份信息查找 peer。
IP IKEv2

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 创建 IKEv2 keychain，并进入 IKEv2 keychain 视图。
ikev2 keychain keychain-name
创建 peer，并进入 视图。
(3) IKEv2 IKEv2 peer
peer name
指定 的主机名称。
(4) IKEv2 peer
hostname name
缺省情况下，未配置 的主机名称。
IKEv2 peer
(5) 指定 IKEv2 peer 的主机地址。
address { ipv4-address [ mask | mask-length ] | ipv6 ipv6-address
[ prefix-length ] }
缺省情况下，未指定 的主机地址。
IKEv2 peer
不同的 中不能指定相同的主机地址。
IKEv2 peer
指定 的身份信息。
(6) IKEv2 peer
identity { address { ipv4-address | ipv6 { ipv6-address } } | fqdn
fqdn-name | email email-string | key-id key-id-string }
缺省情况下，未指定 的身份信息。
IKEv2 peer
配置 的预共享密钥。
(7) IKEv2 peer
pre-shared-key [ local | remote ] { ciphertext | plaintext } string
缺省情况下，未配置 的预共享密钥。
IKEv2 peer

#### 3.8 配置IKEv2全局参数

##### 3.8.1 配置IKEv2 cookie-challenge功能

功能简介
1.
IKEv2 cookie-challenge 功能用来防止攻击者通过源 IP 仿冒对响应方造成 DoS 攻击。
开启 IKEv2 cookie-challenge 功能的同时需要指定启用 cookie-challenge 功能的阈值，当响应方本地存在的半开状态的 IKEv2 SA 数目达到指定的阈值时，则 cookie-challenge 功能开始生效。

##### 3.8.3 配置IKEv2 NAT Keepalive功能

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 开启 IKEv2 cookie-challenge 功能。
ikev2 cookie-challenge number
缺省情况下，IKEv2 cookie-challenge 功能处于关闭状态。

##### 3.8.2 配置全局IKEv2 DPD探测功能

###### 1. 功能简介

IKEv2 DPD 探测功能用来探测对端是否存活，包括以下两种模式：
• 按需探测模式（on-demand）：根据流量来探测对端是否存活。在本端发送用户报文时，如果发现自最后一次收到对端报文之后，在指定的触发 IKEv2 DPD 的时间间隔内一直未收到对端报文，则发送 DPD 报文探测对端是否存活。
定时探测模式（periodic）：按照配置的触发 IKEv2 DPD 的时间间隔定时发送 DPD 报文，
•探测对端是否存活。

###### 2. 配置限制和指导

当系统视图下和 IKEv2 profile 视图下都配置 DPD 探测功能时，IKEv2 profile 视图下的 DPD 配置覆盖系统视图下的全局 DPD 配置。若 IKEv2 profile 视图下没有配置 DPD 探测功能，则应用全局 DPD配置。

###### 3. 配置步骤

进入系统视图。
(1)
system-view配置 探测功能。
(2) IKEv2 DPD ikev2 dpd interval interval [ retry seconds ] { on-demand | periodic }缺省情况下，全局 探测功能处于关闭状态。
IKEv2 DPD配置IKEv2 Keepalive功能
3.8.3 NAT

###### 1. 功能简介

功能仅对位于 之后的设备（即该设备位于 设备连接的私网侧）有IKEv2 NAT Keepalive NAT NAT意义。NAT 之后的 IKEv2 网关设备需要定时向 NAT 之外的 IKEv2 网关设备发送 NAT Keepalive 报文，以确保 NAT 设备上相应于该流量的会话存活，从而让 NAT 之外的设备可以访问 NAT 之后的设备。因此，配置的发送 NAT Keepalive 报文的时间间隔需要小于 NAT 设备上会话表项的存活时间。
本功能必须在探测到 NAT 之后才能生效。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置向对端发送 NAT Keepalive 报文的时间间隔。
ikev2 nat-keepalive seconds

###### 2. 故障分析

###### 3. 处理过程

缺省情况下，探测到 NAT 后发送 NAT Keepalive 报文的时间间隔为 10 秒。

#### 3.9 IKEv2显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 IKEv2 的运行情况，通过查看显示信息验证配置的效果。
在用户视图下执行 reset 命令可以删除 IKEv2 SA。
表3-1 IKEv2 显示和维护操作 命令显示IKEv2安全策略的配置信息 display ikev2 policy [ policy-name | default ]显示IKEv2 profile的配置信息 display ikev2 profile [ profile-name ]显示IKEv2安全提议的配置信息 display ikev2 proposal [ name | default ] display ikev2 sa [ count | [ { local | remote } { ipv4-address | ipv6 ipv6-address } [ vpn-instance显示当前IKEv2 SA的信息vpn-instance-name ] ] [ verbose [ tunnel tunnel-id ] ] ]显示IKEv2统计信息 display ikev2 statistics reset ikev2 sa [ [ { local | remote } { ipv4-address清除IKEv2 SA及其协商生成的Child SA | ipv6 ipv6-address } [ vpn-instance vpn-instance-name ] ] | tunnel tunnel-id ] [ fast ] reset ikev2 statistics清除IKEv2统计信息

#### 3.10 常见错误配置举例

##### 3.10.1 IKEv2提议不匹配导致IKEv2 SA协商失败

###### 1. 故障现象

通过如下命令查看当前的 IKEv2 SA 信息，发现 IKEv2 SA 的状态（Status 字段）为 IN-NEGO。
<Sysname> display ikev2 sa Tunnel ID Local Remote Status
--------------------------------------------------------------------------- 5 123.234.234.124/500 123.234.234.123/500 IN-NEGO Status:
IN-NEGO: Negotiating, EST: Established, DEL:Deleting故障分析
2.
IKEv2 提议配置错误。
处理过程
3.
(1) 排查 IKEv2 相关配置。具体包括：检查两端的 IKEv2 提议是否匹配，即 IKEv2 提议中的认证方法、认证算法、加密算法、PRF 算法是否匹配。
修改 提议的配置，使本端 提议的配置和对端匹配。
(2) IKEv2 IKEv2

###### 1. 故障现象

###### 2. 故障分析

###### 3. 处理过程

##### 3.10.2 IPsec提议不匹配导致IPsec SA协商失败

故障现象
1.
通过 display ikev2 sa 命令查看当前的 IKEv2 SA 信息，发现 IKEv2 SA 协商成功，其状态（Status字段）为 EST。但通过 display ipsec sa 命令查看当前的 时，发现没有协商出相应IPsec SA的 IPsec SA。

###### 2. 故障分析

IPsec 安全策略参数配置错误。
处理过程
3.
(1) 排查 IPsec 相关配置。具体包括：检查双方接口上应用的 IPsec 安全策略的参数是否匹配，即引用的 安全提议的协议、加密算法和认证算法是否匹配。
IPsec修改 策略配置，使本端 安全策略的配置和对端匹配。
(2) IPsec IPsec

##### 3.10.3 无法建立安全隧道

###### 1. 故障现象

双方的 配置正确，也有相匹配的 安全提议，但安全隧道无法建立或者存在安全隧道却ACL IKEv2无法通信。
故障分析
2.
这种情况一般是由于网络状态不稳定，安全隧道建立好以后，有一方的设备重启造成了两端的 IKEv2 SA 或者 IPsec SA 不对称。

###### 3. 处理过程

使用 命令检查双方是否都已建立 SA。如果有一端存在的 在display ikev2 sa IKEv2 IKEv2 SA另一端上不存在，请先使用 reset ikev2 sa 命令清除双方不对称存在的 IKEv2 SA，并重新发起协商；如果两端存在对称的 IKEv2 SA，则使用 display ipsec sa 命令查看接口上的安全策略是否已建立了对称的IPsec SA。如果一端存在的IPsec SA在另一端上不存在，请使用reset ipsec sa 命令清除双方不对称存在的 IPsec SA，并重新发起协商。

## 14-SSH配置

目 录简介服务器配置任务简介开启 服务器功能配置 客户端登录时使用的用户线配置 服务器所属的 域客户端配置任务简介Stelnet客户端删除保存在公钥文件中的服务器公钥客户端配置任务简介

SFTP客户端删除保存在公钥文件中的服务器公钥显示帮助信息客户端配置任务简介SCP客户端删除保存在公钥文件中的服务器公钥配置 协议 算法优先列表设备支持 配置举例（ ）
设备支持SCP B配置举例

### 1 SSH

1 SSH

#### 1.1 SSH简介

是 Shell（安全外壳）的简称，是一种在不安全的网络环境中，通过加密机制和认证机SSH Secure制，实现安全的远程访问以及文件传输等业务的网络安全协议。
SSH 协议采用了典型的客户端/服务器模式，并基于 TCP 协议协商建立用于保护数据传输的会话通道。SSH 协议有两个版本，SSH1.x 和 SSH2.0（本文简称 SSH1 和 SSH2），两者互不兼容。SSH2在性能和安全性方面比 SSH1 有所提高。

##### 1.1.1 设备支持的SSH应用

设备既可以支持 SSH 服务器功能，接受多个 SSH 客户端的连接，也可以支持 SSH 客户端功能，允许用户通过设备与远程 SSH 服务器建立 SSH 连接。
目前，设备支持以下几种 SSH 应用。
• Secure Telnet：简称 Stelnet，可提供安全可靠的网络终端访问服务，使得用户可以安全登录到远程设备，且能保护远程设备不受诸如 IP 地址欺诈、明文密码截取等攻击。设备可支持服务器、Stelnet 客户端功能。
Stelnet FTP：简称 SFTP，基于 SSH2，可提供安全可靠的网络文件传输服务，使得用户可
• Secure以安全登录到远程设备上进行文件管理操作，且能保证文件传输的安全性。设备可支持 SFTP服务器、SFTP 客户端功能。
• Secure Copy：简称 SCP，基于 SSH2，可提供安全的文件复制功能。设备可支持 SCP 服务器、SCP 客户端功能。
NETCONF over SSH：基于 SSH2，提供通过 SSH 连接给设备下发 NETCONF 指令的功能，
•使得用户可以安全登录到远程设备并直接进入到设备的 系统中进行配置和管理操NETCONF作。设备仅支持作为 NETCONF over SSH 连接的服务器端。关于 NETCONF 系统的详细介绍，请参见“网络管理和监控配置指导”中的“NETCONF”。
目前，设备作为 Stelnet 服务器、SFTP 服务器、SCP 服务器时，非 FIPS 模式下支持 SSH2 和 SSH1两个版本，FIPS 模式下只支持 SSH2 版本；设备作为 SSH 客户端时，只支持 SSH2 版本；设备作为 NETCONF over SSH 服务器端时，只支持 SSH2 版本。

##### 1.1.2 SSH工作过程

本小节以SSH2 为例介绍SSH工作的过程，具体分为 表 1-1 所述的几个阶段。
表1-1 SSH 工作过程阶段 说明SSH服务器在22号端口侦听客户端的连接请求，在客户端向服务器端发起连接请求后，连接建立双方建立一个TCP连接版本协商 双方通过版本协商确定最终使用的SSH版本号

阶段 说明SSH支持多种算法，双方根据本端和对端支持的算法，协商出最终用于产生会话密钥的算法协商 密钥交换算法、用于数据信息加密的加密算法、用于进行数字签名和认证的公钥算法，以及用于数据完整性保护的HMAC算法双方通过DH（Diffie-Hellman Exchange）交换，动态地生成用于保护数据传输的会话密钥交换密钥和用来标识该SSH连接的会话ID，并完成客户端对服务器端的身份认证用户认证 SSH客户端向服务器端发起认证请求，服务器端对客户端进行认证认证通过后，SSH客户端向服务器端发送会话请求，请求服务器提供某种类型的服务（目会话请求前支持Stelnet、SFTP、SCP、NETCONF），即请求与服务器建立相应的会话会话建立后，SSH服务器端和客户端在该会话上进行数据信息的交互该阶段，用户在客户端可以通过粘贴文本内容的方式执行命令，但文本会话不能超过会话交互2000字节，且粘贴的命令最好是同一视图下的命令，否则服务器可能无法正确执行该命令。如果粘贴的文本会话超过2000字节，可以采用将配置文件通过SFTP方式上传到服务器，利用新的配置文件重新启动的方式执行这些命令

##### 1.1.3 SSH认证方式

设备作为 服务器可提供以下四种对客户端的认证方式。
SSH

###### 1. password认证

利用 AAA（Authentication、Authorization、Accounting，认证、授权和计费）对客户端身份进行认证。客户端向服务器发出 password 认证请求，将用户名和密码加密后发送给服务器；服务器将认证请求解密后得到用户名和密码的明文，通过本地认证或远程认证验证用户名和密码的合法性，并返回认证成功或失败的消息。
客户端进行 认证时，如果远程认证服务器要求用户进行二次密码认证，则会在发送给服password务器端的认证回应消息中携带一个提示信息，该提示信息被服务器端透传给客户端，由客户端输出并要求用户再次输入一个指定类型的密码，当用户提交正确的密码并成功通过认证服务器的验证后，服务器端才会返回认证成功的消息。
SSH1 版本的 SSH 客户端不支持 AAA 服务器发起的二次密码认证。
关于 AAA 相关内容的介绍，请参考“安全配置指导”中的“AAA”。

###### 2. publickey认证

采用数字签名的方式来认证客户端。目前，设备上可以利用 DSA、ECDSA、RSA 三种公钥算法实现数字签名。客户端发送包含用户名、公钥和公钥算法或者携带公钥信息的数字证书的 publickey认证请求给服务器端。服务器对公钥进行合法性检查，如果合法，则发送消息请求客户端的数字签名；如果不合法，则直接发送失败消息；服务器收到客户端的数字签名之后，使用客户端的公钥对其进行解密，并根据计算结果返回认证成功或失败的消息。
关于公钥相关内容的介绍，请参考“安全配置指导”中的“公钥管理”。

###### 3. password-publickey认证

对于 SSH2 版本的客户端，要求同时进行 password 和 publickey 两种方式的认证，且只有两种认证均通过的情况下，才认为客户端身份认证通过；对于 SSH1 版本的客户端，只要通过其中任意一种认证即可。

###### 4. any认证

不指定客户端的认证方式，客户端可采用 password 认证或 publickey 认证，且只要通过其中任何一种认证即可。

##### 1.1.4 SSH支持Suite B

Suite B 算法集是一种通用的加密和认证算法集，可满足高级别的安全标准要求。RFC6239（Suite B Cryptographic Suites for Secure Shell (SSH)）中定义了 SSH 支持 SuiteB 的相关规范，以及 SSH服务器和 SSH 客户端在身份认证时的算法要求、协商过程以及认证过程。SSH 服务器和 SSH 客户端可基于 证书进行身份认证。
X.509v3

#### 1.2 FIPS相关说明

设备运行于 FIPS 模式时，本特性的相关配置相对于非 FIPS 模式有所变化，具体差异请见本文相关描述。有关 模式的详细介绍请参见“安全配置指导”中的“FIPS”。
FIPS

#### 1.3 配置SSH服务器

##### 1.3.1 SSH服务器配置任务简介

服务器端配置任务如下：
SSH生成本地密钥对
(1)
（可选）配置SSH服务端口号
(2)
开启 服务器
(3) SSH开启Stelnet服务器功能(cid:123)
开启SFTP服务器功能(cid:123)
开启SCP服务器功能(cid:123)
开启NETCONF over SSH服务器功能(cid:123)
(4) 配置SSH客户端登录时使用的用户线仅对 Stelnet 服务器和 NETCONF over SSH 服务器必选。
(5) 配置客户端的公钥采用 publickey、password-publickey 或 any 认证方式时必选。
(6) 配置SSH用户采用 publickey、password-publickey 或 any 认证方式时必选。
(cid:123)
采用 password 认证方式时可选。
(cid:123)
(7) （可选）配置SSH管理功能用户可通过配置认证参数、连接数控制等，提高 SSH 连接的安全性。
(8) （可选）配置 SSH 服务器所属的 PKI 域
(9) （可选）释放已建立的SSH连接

###### 1. 功能简介

##### 1.3.2 生成本地密钥对

功能简介
1.
服务器端的 DSA、ECDSA 或 RSA 密钥对有两个用途，其一是用于在密钥交换阶段生成会话密钥和会话 ID，另外一个是客户端用它来对连接的服务器进行认证。客户端验证服务器身份时，首先判断服务器发送的公钥与本地保存的服务器公钥是否一致，确认服务器公钥正确后，再使用该公钥对服务器发送的数字签名进行验证。
虽然一个客户端只会采用 DSA、ECDSA 或 RSA 公钥算法中的一种来认证服务器，但是由于不同客户端支持的公钥算法不同，为了确保客户端能够成功登录服务器，建议在服务器上同时生成 DSA、和 三种密钥对。
ECDSA RSA生成 密钥对时，将同时生成两个密钥对——服务器密钥对和主机密钥对。SSH1 利用
• RSA SSH服务器端的服务器公钥加密会话密钥，以保证会话密钥传输的安全；SSH2 通过 DH 算法在SSH 服务器和 SSH 客户端上生成会话密钥，不需要传输会话密钥，因此 SSH2 中没有利用服务器密钥对。
生成 DSA 密钥对时，只生成一个主机密钥对。 SSH1 不支持 DSA 算法。
•
• 生成 ECDSA 密钥对时，只生成一个主机密钥对。

###### 2. 配置限制和指导

仅支持默认名称的本地 DSA、ECDSA 或 密钥对，不支持指定名称的本地 DSA、ECDSA SSH RSA或 RSA 密钥对。关于密钥对生成命令的相关介绍请参见“安全命令参考”中的“公钥管理”。
生成 DSA 密钥对时，要求输入的密钥模数的长度必须小于 2048 比特。
服务器支持 和 类型的 密钥对。
SSH secp256r1 secp384r1 ECDSA如果服务器端不存在默认名称的本地 密钥对，则在服务器端执行 服务器相关命令行时（包RSA SSH括开启 Stelnet/SFTP/SCP/NETCONF over SSH 服务器、配置 SSH 用户、以及配置 SSH 服务器端的管理功能），系统会自动生成一个默认名称的本地 RSA 密钥对。
设备运行于 FIPS 模式时，服务器端仅支持 ECDSA、RSA 密钥对，因此请不要生成本地的 DSA 密钥对，否则会导致用户认证失败。

###### 3. 配置步骤

进入系统视图。
(1)
system-view生成本地密钥对。
(2)
public-key local create { dsa | ecdsa { secp256r1 | secp384r1 } | rsa }

##### 1.3.3 配置SSH服务端口号

###### 1. 功能简介

用户通过修改 服务端口号，可以提高 连接的安全性。
SSH SSH

###### 2. 配置限制和指导

如果修改端口号前 SSH 服务是开启的，则修改端口号后系统会自动重启 SSH 服务，正在访问的用户将被断开，用户需要重新建立 SSH 连接后才可以继续访问。
如果使用 1～1024 之间的知名端口号，有可能会导致其他服务启动失败。

###### 2. 配置步骤

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置 SSH 服务端口号。
ssh server port port-number
缺省情况下，SSH 服务的端口号为 22。

##### 1.3.4 开启Stelnet服务器功能

###### 1. 功能简介

本功能用于开启设备上的 Stelnet 服务器功能，使客户端能采用 Stelnet 的方式登录到设备。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 开启 Stelnet 服务器功能。
ssh server enable缺省情况下，Stelnet 服务器功能处于关闭状态。

##### 1.3.5 开启SFTP服务器功能

###### 1. 功能简介

本功能用于开启设备上的 SFTP 服务器功能，使客户端能采用 SFTP 的方式登录到设备。

###### 2. 配置限制和指导

设备作为 SFTP 服务器时，不支持 SSH1 版本的客户端发起的 SFTP 连接。

###### 3. 配置步骤

进入系统视图。
(1)
system-view
(2) 开启 SFTP 服务器功能。
sftp server enable缺省情况下，SFTP 服务器处于关闭状态。

##### 1.3.6 开启SCP服务器功能

###### 1. 功能简介

本功能用于开启设备上的 SCP 服务器功能，使客户端能采用 SCP 的方式登录到设备。

###### 2. 配置限制和指导

设备作为 服务器时，不支持 版本的客户端发起的 连接。
SCP SSH1 SCP

###### 3. 配置步骤

(1) 进入系统视图。

###### 3. 配置步骤

###### 1. 功能简介

###### 2. 配置步骤

system-view
(2) 开启 SCP 服务器功能。
scp server enable缺省情况下，SCP 服务器处于关闭状态。

##### 1.3.7 开启NETCONF over SSH服务器功能

###### 1. 功能简介

本功能用于开启设备上的 NETCONF over SSH 服务器功能，使得客户端能够使用支持 NETCONF连接的客户端配置工具给设备下发 指令来实现对设备的访问。
over SSH NETCONF

###### 2. 配置限制和指导

设备作为 NETCONF over SSH 服务器时，不支持 SSH1 版本的客户端发起的 SSH 连接。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 开启 NETCONF over SSH 服务器功能。
netconf ssh server enable缺省情况下，NETCONF over SSH 服务器处于关闭状态。
关于 NETCONF over SSH 服务器相关命令的详细介绍，请见“网络管理和监控命令参考”中的“NETCONF”。

##### 1.3.8 配置SSH客户端登录时使用的用户线

功能简介
1.
设备支持的 SSH 客户端根据不同的应用可分为：Stelnet 客户端、SFTP 客户端、SCP 客户端和客户端。
NETCONF over SSH Stelnet 客户端和 NETCONF over SSH 客户端通过 VTY（Virtual Type Terminal，虚拟类型终
•端）用户线访问设备。因此，需要配置客户端登录时采用的 VTY 用户线，使其支持 SSH 远程登录协议。配置将在客户端下次登录时生效。
• SFTP 客户端和 SCP 客户端不通过用户线访问设备，不需要配置登录时采用的 VTY 用户线。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入 VTY 用户线视图。
line vty number [ ending-number ]
(3) 配置登录用户线的认证方式为 scheme 方式。
authentication-mode scheme缺省情况下，用户线认证为 password 方式。
该命令的详细介绍，请参见“基础配置命令参考”中的“登录设备”。

###### 1. 功能简介

###### 2. 导入方式

##### 1.3.9 配置客户端的公钥

功能简介
1.
服务器在采用 publickey 方式验证客户端身份时，首先比较客户端发送的 SSH 用户名、主机公钥是否与本地配置的 用户名以及相应的客户端主机公钥一致，在确认用户名和客户端主机公钥正SSH确后，对客户端发送的数字签名进行验证，该签名是客户端利用主机公钥对应的私钥计算出的。
因此，在采用 publickey、password-publickey 或 any 认证方式时：
在服务器端配置客户端的 DSA、ECDSA 或 主机公钥。
• RSA在客户端为该 用户指定与主机公钥对应的 DSA、ECDSA 或 主机私钥（若设备作
• SSH RSA为客户端，则在向服务器发起连接时通过指定公钥算法来实现）。
导入方式
2.
服务器端可以通过手工配置和从公钥文件中导入两种方式来配置客户端的公钥。
• 手工配置事先在客户端上通过显示命令或其它方式查看其公钥信息，并记录客户端主机公钥的内容，然后采用手工输入的方式将客户端的公钥配置到服务器上。手工输入远端主机公钥时，可以逐个字符输入，也可以一次拷贝粘贴多个字符。这种方式要求手工输入或拷贝粘贴的主机公钥必须是未经转换的 DER（Distinguished Encoding Rules，特异编码规则）公钥编码格式。
手工配置客户端的公钥时，输入的主机公钥必须满足一定的格式要求。我司设备作为客户端时，通过 display public-key local public 命令显示的公钥可以作为输入的公钥内容；通过其他方式（如 public-key local export 命令）显示的公钥可能不满足格式要求，导致主机公钥保存失败。
• 从公钥文件导入事先将客户端的公钥文件保存到服务器上（例如，通过 FTP 或 TFTP，以二进制方式将客户端的公钥文件保存到服务器），服务器从本地保存的该公钥文件中导入客户端的公钥。导入公钥时，系统会自动将客户端公钥文件转换为 PKCS（Public Standards，Key Cryptography公共密钥加密标准）编码形式。

###### 3. 配置限制和指导

SSH 服务器上配置的 SSH 客户端公钥数目建议不要超过 20 个。
配置客户端公钥时建议选用从公钥文件导入的方式配置远端主机的公钥。

###### 4. 手工配置客户端的公钥

(1) 进入系统视图。
system-view
(2) 进入公钥视图。
public-key peer keyname
(3) 配置客户端的公钥。
逐个字符输入或拷贝粘贴公钥内容。
在输入公钥内容时，字符之间可以有空格，也可以按回车键继续输入数据。保存公钥数据时，
将删除空格和回车符。具体介绍请参见“安全配置指导”中的“公钥管理”。
(4) 退出公钥视图并保存配置的主机公钥。

peer-public-key end

###### 5. 从公钥文件中导入客户端的公钥

进入系统视图。
(1)
system-view从公钥文件中导入远端客户端的公钥。
(2)
public-key peer keyname import sshkey filename

##### 1.3.10 配置SSH用户

###### 1. 功能简介

本配置用于创建 用户，并指定 用户的服务类型、认证方式以及对应的客户端公钥或数字SSH SSH证书。SSH 用户的配置与服务器端采用的认证方式有关，具体如下：
• 如果服务器采用了 publickey 认证，则必须在设备上创建相应的 SSH 用户，以及同名的本地用户（用于下发授权属性：工作目录、用户角色）。
• 如果服务器采用了 password 认证，则必须在设备上创建相应的本地用户（适用于本地认证），或在远程服务器（如 RADIUS 服务器，适用于远程认证）上创建相应的 SSH 用户。这种情况下，并不需要通过本配置创建相应的 用户，如果创建了 用户，则必须保证指定了SSH SSH正确的服务类型以及认证方式。
• 如果服务器采用了 password-publickey 或 any 认证，则必须在设备上创建相应的 SSH 用户，以及在设备上创建同名的本地用户（适用于本地认证）或者在远程认证服务器上创建同名的SSH 用户（如 RADIUS 服务器，适用于远程认证）。

###### 2. 配置限制和指导

对 用户配置的修改，不会影响已经登录的 用户，仅对新登录的用户生效。
SSH SSH模式下，设备作为 服务器不支持 认证和 认证方式。
FIPS SSH any publickey或 用户登录时使用的工作目录与用户使用的认证方式有关：
SCP SFTP通过 publickey或 password-publickey认证登录服务器的用户使用的工作目录均为对应的本地
•用户视图下为该用户设置的工作目录。
• 通过 password 认证登录服务器的用户，使用的工作目录为通过 AAA 授权的工作目录。
用户登录时拥有的用户角色与用户使用的认证方式有关：
SSH通过 或 认证登录服务器的 用户将被授予对应的本地用户
• publickey password-publickey SSH视图下指定的用户角色。
• 通过 password 认证登录服务器的 SSH 用户将被授予远程 AAA 服务器或设备本地授权的用户角色。
除 password 认证方式外，其它认证方式下均需要指定客户端的公钥或证书。
• 对于使用公钥认证的SSH用户，服务器端必须指定客户端的公钥，且指定的公钥必须已经存在，公钥内容的配置请参见“1.3.9 配置客户端的公钥”。如果指定了多个用户公钥，则在验证 用户身份时，按照配置顺序使用指定的公钥依次对其进行验证，只要用户通过任意SSH一个公钥验证即可。
• 对于使用证书认证的 SSH 用户，服务器端必须指定用于验证客户端证书的 PKI 域，PKI 域的配置请参见“安全配置指导”中的“PKI 域配置”。为保证 SSH 用户可以成功通过认证，通

过 ssh user 命令或 ssh server pki-domain 命令指定的 PKI 域中必须存在用于验证客户端证书的 证书。
CA关于本地用户以及远程认证的相关配置请参见“安全配置指导”中的“AAA”。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 创建 SSH 用户，并指定 SSH 用户的服务类型和认证方式。
（非 FIPS 模式）
ssh user username service-type { all | netconf | scp | sftp | stelnet }
authentication-type { password | { any | password-publickey | publickey }
[ assign { pki-domain domain-name | publickey keyname&<1-6> } ] }
（FIPS 模式）
ssh user username service-type { all | netconf | scp | sftp | stelnet }
authentication-type { password | password-publickey [ assign
{ pki-domain domain-name | publickey keyname&<1-6> } ] }
服务器上最多可以创建 个 用户。
SSH 1024 SSH

##### 1.3.11 配置SSH管理功能

###### 1. 设置SSH服务器是否兼容SSH1版本的客户端

(1) 进入系统视图。
system-view
设置 服务器兼容 版本的客户端。
(2) SSH SSH1
ssh server compatible-ssh1x enable
缺省情况下，SSH 服务器不兼容 版本的客户端。
SSH1
模式下，不支持本命令。
FIPS

###### 2. 开启SSH算法重协商和密钥重交换功能

(1) 进入系统视图。
system-view
开启 算法重协商和密钥重交换功能。
(2) SSH
ssh server key-re-exchange enable [ interval interval ]
缺省情况下，SSH 算法重协商和密钥重交换功能处于关闭状态。
模式下，不支持本命令。
FIPS
本功能的开启和间隔时间变化不影响已存在的 SSH 连接。

###### 3. 设置RSA服务器密钥对的最小更新间隔时间

进入系统视图。
(1)
system-view设置 服务器密钥对的最小更新间隔时间。
(2) RSA ssh server rekey-interval interval

缺省情况下，系统不更新 RSA 服务器密钥对。
FIPS 模式下，不支持本命令。
本功能仅对 SSH 客户端版本为 SSH1 的用户有效。

###### 4. 设置SSH用户的认证超时时间

进入系统视图。
(1)
system-view
(2) 设置 SSH 用户的认证超时时间。
ssh server authentication-timeout time-out-value缺省情况下，SSH 用户的认证超时时间为 60 秒。
为了防止不法用户建立起 TCP 连接后，不进行接下来的认证而空占进程，妨碍其它合法用户的正常登录，可以设置验证超时时间，如果在规定的时间内没有完成认证就拒绝该连接。

###### 5. 设置SSH用户请求连接的认证尝试最大次数

(1) 进入系统视图。
system-view
(2) 设置 SSH 认证尝试的最大次数。
ssh server authentication-retries retries
缺省情况下，SSH 连接认证尝试的最大次数为 次。
3
本功能可以防止非法用户对用户名和密码进行恶意地猜测和破解。在 认证方式下，SSH
any
客户端通过 publickey 和 password 方式进行认证尝试的次数总和，不能超过配置最大次数。

###### 6. 设置对SSH客户端的访问控制

(1) 进入系统视图。
system-view
(2) 设置对 SSH 用户的访问控制。
（IPv4 网络）
ssh server acl { advanced-acl-number | basic-acl-number | mac
mac-acl-number }
（IPv6 网络）
ssh server ipv6 acl { ipv6 { advanced-acl-number | basic-acl-number } |
mac mac-acl-number }
缺省情况下，允许所有 SSH 用户向设备发起 SSH 访问。
通过配置本功能，使用 ACL 过滤向 SSH 服务器发起连接的 SSH 客户端。

###### 7. 开启匹配ACL deny规则后打印日志信息功能

进入系统视图。
(1)
system-view
(2) 开启匹配 ACL deny 规则后打印日志信息功能。
ssh server acl-deny-log enable缺省情况下，匹配 ACL deny 规则后打印日志信息功能处于关闭状态。

###### 2. 配置步骤

通过开启本功能，设备可以记录匹配 deny 规则的 IP 用户的登录日志，用户可以查看非法登录的地址信息。

###### 8. 设置SSH服务器向SSH客户端发送的报文的DSCP优先级

(1) 进入系统视图。
system-view
(2) 设置 SSH 服务器向 SSH 客户端发送的报文的 DSCP 优先级。
（IPv4 网络）
ssh server dscp dscp-value
（IPv6 网络）
ssh server ipv6 dscp dscp-value
缺省情况下，SSH 报文的 优先级为 48。
DSCP
携带在 报文中的 字段和 报文中的 字段，用来体现报文自身
DSCP IPv4 ToS IPv6 Trafic class
的优先等级，决定报文传输的优先程度。

###### 9. 设置SFTP用户连接的空闲超时时间

(1) 进入系统视图。
system-view
(2) 设置 SFTP 用户连接的空闲超时时间。
sftp server idle-timeout time-out-value
缺省情况下，SFTP 用户连接的空闲超时时间为 10 分钟。
当 SFTP 用户连接的空闲时间超过设定的阈值后，系统会自动断开此用户的连接，从而有效
避免用户长期占用连接而不进行任何操作。

###### 10. 设置同时在线的最大SSH用户连接数

(1) 进入系统视图。
system-view
(2) 设置同时在线的最大 SSH 用户连接数。
aaa session-limit ssh max-sessions
缺省情况下，同时在线的最大 SSH 用户连接数为 32。
系统资源有限，当前在线 SSH 用户数超过设定的最大值时，系统会拒绝新的 SSH 连接请求。
该值的修改不会对已经在线的用户连接造成影响，只会对新的用户连接生效。
关于该命令的详细介绍，请参见“安全命令参考”中的“AAA”。

##### 1.3.12 配置SSH服务器所属的PKI域

###### 1. 功能简介

SSH 服务器利用所属的 PKI 域在密钥交换阶段发送证书给客户端，在 ssh user 命令中没有指定验证客户端的 域的情况下，使用服务器所属的 域来认证客户端并用它来对连接的客户端进PKI PKI行认证。
配置步骤
2.
(1) 进入系统视图。

###### 2. 配置步骤

###### 1. 功能简介

system-view
(2) 配置 SSH 服务器所属的 PKI 域。
ssh server pki-domain domain-name缺省情况下，未配置 SSH 服务器所属的 PKI 域。

##### 1.3.13 释放已建立的SSH连接

###### 1. 功能简介

系统支持多个 SSH 用户同时对设备进行配置，当管理员在维护设备时，其他在线 SSH 用户的配置影响到管理员的操作，或者管理员正在进行一些重要配置不想被其他用户干扰时，可以强制断开该用户的连接。
配置步骤
2.
请在用户视图下执行本命令，释放已建立的 SSH 连接。
free ssh { user-ip { ip-address | ipv6 ipv6-address } [ port port-number ] | user-pid pid-number | username username }

#### 1.4 配置Stelnet客户端

##### 1.4.1 Stelnet客户端配置任务简介

Stelnet 客户端配置任务如下：
(1) 生成本地密钥对仅采用 publickey、password-publickey 或 any 认证方式时必选。
(2) （可选）配置Stelnet客户端发送SSH报文使用的源IP地址
(3) 建立与Stelnet服务器的连接
(4) （可选）客户端删除保存在公钥文件中的服务器公钥
(5) （可选）与远程的Stelnet服务器建立基于Suite B算法集的连接

##### 1.4.2 生成本地密钥对

功能简介
1.
客户端采用 publickey、password-publickey 或 any 认证方式时，需要生成本地密钥对。

###### 2. 配置限制和指导

SSH 仅支持默认名称的本地 DSA、ECDSA 或 RSA 密钥对，不支持指定名称的本地 DSA、ECDSA或 密钥对。关于密钥对生成命令的相关介绍请参见“安全命令参考”中的“公钥管理”。
RSA生成 密钥对时，要求输入的密钥模数的长度必须小于 比特。
DSA 2048客户端支持 和 类型的 密钥对。
SSH secp256r1 secp384r1 ECDSA设备运行于 模式时，仅支持 、 密钥对。
FIPS ECDSA RSA

###### 3. 配置步骤

(1) 进入系统视图。

system-view
(2) 生成本地密钥对。
public-key local create { dsa | ecdsa { secp256r1 | secp384r1 } | rsa }

##### 1.4.3 配置Stelnet客户端发送SSH报文使用的源IP地址

###### 1. 功能简介

Stelnet 客户端与 Stelnet 服务器通信时，缺省采用路由决定的源 IP 地址作为发送报文的源地址。如果使用本配置指定了源 地址或源接口，则采用该地址与服务器进行通信。
IP

###### 2. 配置限制和指导

为保证 Stelnet 客户端与 Stelnet 服务器通信链路的可达性，以及增加认证业务对 SFTP 客户端的可管理性，通常建议指定 Loopback 接口的 IP 地址作为源 IP 地址。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 配置 Stelnet 客户端发送 SSH 报文使用的源 IP 地址。
（IPv4 网络）
ssh client source { interface interface-type interface-number | ip
ip-address }
缺省情况下，IPv4 客户端采用设备路由指定的 报文出接口主 地址作为源
Stelnet SSH IP IP
地址。
（IPv6 网络）
ssh client ipv6 source { interface interface-type interface-number |
ipv6 ipv6-address }
缺省情况下，IPv6 Stelnet 客户端采用设备自动选择的 IPv6 地址作为源 IP 地址。

##### 1.4.4 建立与Stelnet服务器的连接

###### 1. 功能简介

该配置任务用来启动 Stelnet 客户端程序，与远程 Stelnet 服务器建立连接，并指定公钥算法、首选加密算法、首选 HMAC 算法和首选密钥交换算法等。
Stelnet 客户端访问服务器时，需要通过本地保存的服务器端的主机公钥来验证服务器的身份。设备作为 客户端时，默认支持首次认证，即当 客户端首次访问服务器，而客户端没有配Stelnet Stelnet置服务器端的主机公钥时，用户可以选择继续访问该服务器，并在客户端保存该主机公钥，不指定public-key，则会把服务器公钥保存到公钥文件中，但不会保存到配置文件中；当用户下次访问该服务器时，就以保存的主机公钥来认证该服务器。首次认证在比较安全的网络环境中可以简化客户端的配置，但由于该方式下客户端完全相信服务器公钥的正确性，因此存在一定的安全隐患。

###### 2. 配置限制和指导

客户端不能同时连接 IPv4 和 IPv6 类型的服务器。

###### 3. 与IPv4 Stelnet服务器端建立连接

请在用户视图下执行以下命令，与 IPv4 Stelnet 服务器端建立连接。
（非 FIPS 模式）
ssh2 server [ port-number ] [ vpn-instance vpn-instance-name ] [ identity-key { dsa | ecdsa-sha2-nistp256 | ecdsa-sha2-nistp384 | rsa | { x509v3-ecdsa-sha2-nistp256 | x509v3-ecdsa-sha2-nistp384 } pki-domain domain-name } | prefer-compress zlib | prefer-ctos-cipher { 3des-cbc | aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm | des-cbc } | prefer-ctos-hmac { md5 | md5-96 | sha1 | sha1-96 | sha2-256 | sha2-512 | sm3 } | prefer-kex { dh-group-exchange-sha1 | dh-group1-sha1 | dh-group14-sha1 | ecdh-sha2-nistp256 | ecdh-sha2-nistp384 } | prefer-stoc-cipher { 3des-cbc | aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm | des-cbc } | prefer-stoc-hmac { md5 | md5-96 | sha1 | sha1-96 | sha2-256 | sha2-512 | sm3 } ]
* [ dscp dscp-value | escape character | { public-key keyname | server-pki-domain domain-name } | source { interface interface-type interface-number | ip ip-address } ] *（FIPS 模式）
ssh2 server [ port-number ] [ vpn-instance vpn-instance-name ] [ identity-key { ecdsa-sha2-nistp256 | ecdsa-sha2-nistp384 | rsa | { x509v3-ecdsa-sha2-nistp256 | x509v3-ecdsa-sha2-nistp384 } pki-domain domain-name } | prefer-compress zlib | prefer-ctos-cipher { aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm } | prefer-ctos-hmac { sha1 | sha1-96 | sha2-256 | sha2-512 } | prefer-kex { dh-group14-sha1 | ecdh-sha2-nistp256 | ecdh-sha2-nistp384 } | prefer-stoc-cipher { aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm } | prefer-stoc-hmac { sha1 | sha1-96 | sha2-256 | sha2-512 } ] * [ escape character | { public-key keyname | server-pki-domain domain-name } | source { interface interface-type interface-number | ip ip-address } ] *

###### 4. 与IPv6 Stelnet服务器端建立连接

请在用户视图下执行以下命令，与 IPv6 Stelnet 服务器端建立连接。
（非 FIPS 模式）
ssh2 ipv6 server [ port-number ] [ vpn-instance vpn-instance-name ] [ -i interface-type interface-number ] [ identity-key { dsa | ecdsa-sha2-nistp256 | ecdsa-sha2-nistp384 | rsa | { x509v3-ecdsa-sha2-nistp256 | x509v3-ecdsa-sha2-nistp384 } pki-domain domain-name } | prefer-compress zlib | prefer-ctos-cipher { 3des-cbc | aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes 256-cbc | aes256-ctr | aes256-gcm | des-cbc } | prefer-ctos-hmac { md5 | md5-96 | sha1 | sha1-96 | sha2-256 | sha2-512 | sm3 } | prefer-kex { dh-group-exchange-sha1 | dh-group1-sha1 | dh-group14-sha1 |

ecdh-sha2-nistp256 | ecdh-sha2-nistp384 } | prefer-stoc-cipher { 3des-cbc | aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm | des-cbc } | prefer-stoc-hmac { md5 | md5-96 | sha1 | sha1-96 | sha2-256 | sha2-512 | sm3 } ] * [ dscp dscp-value | escape character | { public-key keyname | server-pki-domain domain-name } | source { interface interface-type interface-number | ipv6 ipv6-address } ] *（FIPS 模式）
ssh2 ipv6 server [ port-number ] [ vpn-instance vpn-instance-name ] [ -i interface-type interface-number ] [ identity-key { ecdsa-sha2-nistp256 | ecdsa-sha2-nistp384 | rsa | { x509v3-ecdsa-sha2-nistp256 | x509v3-ecdsa-sha2-nistp384 } pki-domain domain-name } | prefer-compress zlib | prefer-ctos-cipher { aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm } | prefer-ctos-hmac { sha1 | sha1-96 | sha2-256 | sha2-512 } | prefer-kex { dh-group14-sha1 | ecdh-sha2-nistp256 | ecdh-sha2-nistp384 } | prefer-stoc-cipher { aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm } | prefer-stoc-hmac { sha1 | sha1-96 | sha2-256 | sha2-512 } ] * [ escape character | { public-key keyname | server-pki-domain domain-name } | source { interface interface-type interface-number | ipv6 ipv6-address } ] *

##### 1.4.5 Stelnet客户端删除保存在公钥文件中的服务器公钥

###### 1. 功能简介

客户端切换到 FIPS 模式后，如果已经保存的服务器公钥不符合 FIPS 模式要求，则无法登录到服务器。如果客户端想要重新登录该服务器，则需要执行本配置删除本地文件中的指定服务器公钥，并保证服务器上已经生成了符合 模式要求的公钥。
FIPS

###### 2. 配置步骤

(1) 进入系统视图。
system-view
客户端删除保存在公钥文件中的服务器公钥。
(2) Stelnet
delete ssh client server-public-key [ server-ip ip-address ]

##### 1.4.6 与远程的Stelnet服务器建立基于Suite B算法集的连接

请在用户视图下执行本命令，与远程的 Stelnet 服务器建立基于 Suite B 算法集的连接。
（IPv4 网络）
ssh2 server [ port-number ] [ vpn-instance vpn-instance-name ] suite-b [ 128-bit | 192-bit ] pki-domain domain-name [ server-pki-domain domain-name ] [ prefer-compress zlib ] [ dscp dscp-value | escape character | source { interface interface-type interface-number | ip ip-address } ] *（IPv6 网络）

ssh2 ipv6 server [ port-number ] [ vpn-instance vpn-instance-name ] [ -i interface-type interface-number ] suite-b [ 128-bit | 192-bit ] pki-domain domain-name [ server-pki-domain domain-name ] [ prefer-compress zlib ] [ dscp dscp-value | escape character | source { interface interface-type interface-number | ipv6 ipv6-address } ] *

#### 1.5 配置SFTP客户端

##### 1.5.1 SFTP客户端配置任务简介

客户端配置任务如下：
SFTP
(1) 生成本地密钥对仅采用 publickey、password-publickey 或 any 认证方式时必选。
(2) （可选）配置SFTP客户端发送SFTP报文使用的源IP地址
(3) 建立与SFTP服务器的连接
(4) （可选）SFTP客户端删除保存在公钥文件中的服务器公钥
(5) （可选）与远程的SFTP服务器建立基于Suite B算法集的连接
(6) （可选）SFTP目录操作
(7) （可选）SFTP文件操作
(8) （可选）显示帮助信息
(9) （可选）终止与SFTP服务器的连接

##### 1.5.2 生成本地密钥对

###### 1. 功能简介

客户端采用 publickey、password-publickey 或 any 认证方式时，需要生成本地密钥对。

###### 2. 配置限制和指导

SSH 仅支持默认名称的本地 DSA、ECDSA 或 RSA 密钥对，不支持指定名称的本地 DSA、ECDSA或 密钥对。关于密钥对生成命令的相关介绍请参见“安全命令参考”中的“公钥管理”。
RSA生成 密钥对时，要求输入的密钥模数的长度必须小于 比特。
DSA 2048客户端支持 和 类型的 密钥对。
SSH secp256r1 secp384r1 ECDSA设备运行于 FIPS 模式时，仅支持 RSA、ECDSA 密钥对。

###### 3. 配置步骤

进入系统视图。
(1)
system-view生成本地密钥对。
(2)
public-key local create { dsa | ecdsa { secp256r1 | secp384r1 } | rsa }

###### 3. 配置步骤

###### 1. 功能简介

##### 1.5.3 配置SFTP客户端发送SFTP报文使用的源IP地址

功能简介
1.
SFTP 客户端与 SFTP 服务器通信时，缺省采用路由决定的源 IP 地址作为发送报文的源地址。如果使用本配置指定了源 地址或源接口，则采用该地址与服务器进行通信。
IP

###### 2. 配置限制和指导

为保证 SFTP 客户端与 SFTP 服务器通信链路的可达性，以及增加认证业务对 SFTP 客户端的可管理性，通常建议指定 Loopback 接口的 IP 地址作为源 IP 地址。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 配置 SFTP 客户端发送 SFTP 报文使用的源 IP 地址。
（IPv4 网络）
sftp client source { ip ip-address | interface interface-type interface-number }缺省情况下，IPv4客户端采用设备路由指定的 SFTP报文的出接口主 IP地址作为源 IP 地址。
（IPv6 网络）
sftp client ipv6 source { ipv6 ipv6-address | interface interface-type interface-number }缺省情况下，IPv6 客户端采用设备自动选择的 IPv6 地址作为源 IP 地址。

##### 1.5.4 建立与SFTP服务器的连接

###### 1. 功能简介

该配置任务用来启动 客户端程序，与远程 服务器建立连接，并指定公钥算法、首选加SFTP SFTP密算法、首选 HMAC 算法和首选密钥交换算法等。SFTP 客户端与服务器成功建立连接之后，用户即可进入到服务器端上的 SFTP 客户端视图下进行目录、文件等操作。
SFTP 客户端访问服务器时，需要通过本地保存的服务器端的主机公钥来验证服务器的身份。设备作为 SFTP 客户端时，默认支持首次认证，即当 SFTP 客户端首次访问服务器，而客户端没有配置服务器端的主机公钥时，用户可以选择继续访问该服务器，并在客户端保存该主机公钥，不指定public-key，则会把服务器公钥保存到公钥文件中，但不会保存到配置文件中；当用户下次访问该服务器时，就以保存的主机公钥来认证该服务器。首次认证在比较安全的网络环境中可以简化客户端的配置，但由于该方式下客户端完全相信服务器公钥的正确性，因此存在一定的安全隐患。

###### 2. 配置限制和指导

客户端不能同时连接 和 类型的服务器。
IPv4 IPv6

###### 3. 与IPv4 SFTP服务器建立连接，并进入SFTP客户端视图

请在用户视图下执行以下命令，与 IPv4 SFTP 服务器建立连接，并进入 SFTP 客户端视图。
（非 FIPS 模式）
sftp server [ port-number ] [ vpn-instance vpn-instance-name ] [ identity-key { dsa | ecdsa-sha2-nistp256 | ecdsa-sha2-nistp384 | rsa |

{ x509v3-ecdsa-sha2-nistp256 | x509v3-ecdsa-sha2-nistp384 } pki-domain domain-name } | prefer-compress zlib | prefer-ctos-cipher { 3des-cbc | aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm | des-cbc } | prefer-ctos-hmac { md5 | md5-96 | sha1 | sha1-96 | sha2-256 | sha2-512 | sm3 } | prefer-kex { dh-group-exchange-sha1 | dh-group1-sha1 | dh-group14-sha1 | ecdh-sha2-nistp256 | ecdh-sha2-nistp384 } | prefer-stoc-cipher { 3des-cbc | aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm | des-cbc } | prefer-stoc-hmac { md5 | md5-96 | sha1 | sha1-96 | sha2-256 | sha2-512 | sm3 } ]
* [ dscp dscp-value | { public-key keyname | server-pki-domain domain-name } | source { interface interface-type interface-number | ip ip-address } ] *（FIPS 模式）
sftp server [ port-number ] [ vpn-instance vpn-instance-name ] [ identity-key { ecdsa-sha2-nistp256 | ecdsa-sha2-nistp384 | rsa | { x509v3-ecdsa-sha2-nistp256 | x509v3-ecdsa-sha2-nistp384 } pki-domain domain-name } | prefer-compress zlib | prefer-ctos-cipher { aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm } | prefer-ctos-hmac { sha1 | sha1-96 | sha2-256 | sha2-512 } | prefer-kex { dh-group14-sha1 | ecdh-sha2-nistp256 | ecdh-sha2-nistp384 } | prefer-stoc-cipher { aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm } | prefer-stoc-hmac { sha1 | sha1-96 | sha2-256 | sha2-512 } ] * [ { public-key keyname | server-pki-domain domain-name } | source { interface interface-type interface-number | ip ip-address } ] *

###### 4. 与IPv6 SFTP服务器建立连接，并进入SFTP客户端视图

请在用户视图下执行以下命令，与 服务器建立连接，并进入 客户端视图。
IPv6 SFTP SFTP（非 FIPS 模式）
sftp ipv6 server [ port-number ] [ vpn-instance vpn-instance-name ] [ -i interface-type interface-number ] [ identity-key { dsa | ecdsa-sha2-nistp256 | ecdsa-sha2-nistp384 | rsa | { x509v3-ecdsa-sha2-nistp256 | x509v3-ecdsa-sha2-nistp384 } pki-domain domain-name } | prefer-compress zlib | prefer-ctos-cipher { 3des-cbc | aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm | des-cbc } | prefer-ctos-hmac { md5 | md5-96 | sha1 | sha1-96 | sha2-256 | sha2-512 | sm3 } | prefer-kex { dh-group-exchange-sha1 | dh-group1-sha1 | dh-group14-sha1 | ecdh-sha2-nistp256 | ecdh-sha2-nistp384 } | prefer-stoc-cipher { 3des-cbc | aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm | des-cbc } | prefer-stoc-hmac { md5 | md5-96 | sha1 | sha1-96 | sha2-256 | sha2-512 | sm3 } ] * [ dscp dscp-value | { public-key keyname | server-pki-domain domain-name } | source { interface interface-type interface-number | ipv6 ipv6-address } ] *（ FIPS 模式）

sftp ipv6 server [ port-number ] [ vpn-instance vpn-instance-name ] [ -i interface-type interface-number ] [ identity-key { ecdsa-sha2-nistp256 | ecdsa-sha2-nistp384 | rsa | { x509v3-ecdsa-sha2-nistp256 | x509v3-ecdsa-sha2-nistp384 } pki-domain domain-name } | prefer-compress zlib | prefer-ctos-cipher { aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm } | prefer-ctos-hmac { sha1 | sha1-96 | sha2-256 | sha2-512 } | prefer-kex { dh-group14-sha1 | ecdh-sha2-nistp256 | ecdh-sha2-nistp384 } | prefer-stoc-cipher { aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm } | prefer-stoc-hmac { sha1 | sha1-96 | sha2-256 | sha2-512 } ] * [ { public-key keyname | server-pki-domain domain-name } | source { interface interface-type interface-number | ipv6 ipv6-address } ] *

##### 1.5.5 SFTP客户端删除保存在公钥文件中的服务器公钥

###### 1. 功能简介

客户端切换到 模式后，如果已经保存的服务器公钥不符合 模式要求，则无法登录到服务FIPS FIPS器。如果客户端想要重新登录该服务器，则需要执行本配置删除本地文件中的指定服务器公钥，并保证服务器上已经生成了符合 FIPS 模式要求的公钥。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) SFTP 客户端删除保存在公钥文件中的服务器公钥。
delete ssh client server-public-key [ server-ip ip-address ]

##### 1.5.6 与远程的SFTP服务器建立基于Suite B算法集的连接

请在用户视图下执行本命令，与远程的 SFTP 服务器建立基于 Suite B 算法集的连接。
（IPv4 网络）
sftp server [ port-number ] [ vpn-instance vpn-instance-name ] suite-b [ 128-bit | 192-bit ] pki-domain domain-name [ server-pki-domain domain-name ] [ prefer-compress zlib ] [ dscp dscp-value | source { interface interface-type interface-number | ip ip-address } ] *（IPv6 网络）
sftp ipv6 server [ port-number ] [ vpn-instance vpn-instance-name ] [ -i interface-type interface-number ] suite-b [ 128-bit | 192-bit ] pki-domain domain-name [ server-pki-domain domain-name ] [ prefer-compress zlib ] [ dscp dscp-value | escape character | source { interface interface-type interface-number | ipv6 ipv6-address } ] *

###### 1. 功能简介

##### 1.5.7 SFTP目录操作

功能简介
1.
SFTP 目录操作包括：改变或显示当前的工作路径、显示指定目录下的文件或目录信息、改变服务器上指定的文件夹的名字、创建或删除目录等操作。

###### 2. 改变远程SFTP服务器上的工作路径

(1) 进入 SFTP 客户端视图。
具体命令请参考“1.5.4 建立与SFTP服务器的连接”。
改变远程 服务器上的工作路径。
(2) SFTP
cd [ remote-path ]
（可选）返回到上一级目录。
(3)
cdup

###### 3. 显示远程SFTP服务器上的当前工作目录

(1) 进入 SFTP 客户端视图。
具体命令请参考“1.5.4 建立与SFTP服务器的连接”。
显示远程 服务器上的当前工作目录。
(2) SFTP
pwd

###### 4. 显示指定目录下的文件列表

(1) 进入 SFTP 客户端视图。
具体命令请参考“1.5.4 建立与SFTP服务器的连接”。
显示指定目录下的文件列表。
(2)
dir [ -a | -l ] [ remote-path ]
(cid:123)
ls [ -a | -l ] [ remote-path ]
(cid:123)
和 两条命令的作用相同。
dir ls

###### 5. 改变SFTP服务器上指定的目录的名字

(1) 进入 SFTP 客户端视图。
具体命令请参考“1.5.4 建立与SFTP服务器的连接”。
改变 服务器上指定的目录的名字。
(2) SFTP
rename old-name new-name

###### 6. 在远程SFTP服务器上创建新的目录

(1) 进入 SFTP 客户端视图。
具体命令请参考“1.5.4 建立与SFTP服务器的连接”。
(2) 在远程 SFTP 服务器上创建新的目录。
mkdir remote-path

###### 7. 删除SFTP服务器上指定的目录

(1) 进入 SFTP 客户端视图。
具体命令请参考“1.5.4 建立与SFTP服务器的连接”。

(2) 删除 SFTP 服务器上指定的目录。
rmdir remote-path

##### 1.5.8 SFTP文件操作

###### 1. 功能简介

SFTP 文件操作包括：改变文件名、下载文件、上传文件、显示文件列表和删除文件。

###### 2. 改变SFTP服务器上指定的文件的名字

进入 客户端视图。
(1) SFTP具体命令请参考“1.5.4 建立与SFTP服务器的连接”。
改变 服务器上指定的文件的名字。
(2) SFTP rename old-name new-name

###### 3. 从远程服务器上下载文件并存储在本地

(1) 进入 SFTP 客户端视图。
具体命令请参考“1.5.4 建立与SFTP服务器的连接”。
从远程服务器上下载文件并存储在本地。
(2)
get remote-file [ local-file ]

###### 4. 将本地的文件上传到远程SFTP服务器

(1) 进入 SFTP 客户端视图。
具体命令请参考“1.5.4 建立与SFTP服务器的连接”。
(2) 将本地的文件上传到远程 SFTP 服务器。
put local-file [ remote-file ]

###### 5. 显示指定目录下的文件

(1) 进入 SFTP 客户端视图。
具体命令请参考“1.5.4 建立与SFTP服务器的连接”。
(2) 显示指定目录下的文件。
dir [ -a | -l ] [ remote-path ]
(cid:123)
ls [ -a | -l ] [ remote-path ]
(cid:123)
和 两条命令的作用相同。
dir ls

###### 6. 删除SFTP服务器上指定的文件

(1) 进入 SFTP 客户端视图。
具体命令请参考“1.5.4 建立与SFTP服务器的连接”。
(2) 删除 SFTP 服务器上指定的文件。
delete remote-file
(cid:123)
remove remote-file
(cid:123)
和 两条命令的功能相同。
delete remove

###### 1. 功能简介

###### 1. 功能简介

##### 1.5.9 显示帮助信息

功能简介
1.
本配置用于显示命令的帮助信息，如命令格式、参数配置等。

###### 2. 配置步骤

(1) 进入 SFTP 客户端视图。
具体命令请参考“1.5.4 建立与SFTP服务器的连接”。
(2) 显示 SFTP 客户端命令的帮助信息。
help
(cid:123)
？
(cid:123)
help 和？的功能相同。

##### 1.5.10 终止与SFTP服务器的连接

进入 客户端视图。
(1) SFTP具体命令请参考“1.5.4 建立与SFTP服务器的连接”。
终止与 服务器的连接，并退回用户视图。
(2) SFTP bye (cid:123)
exit (cid:123)
quit (cid:123)
bye、exit 和 quit 三条命令的功能相同。

#### 1.6 配置SCP客户端

##### 1.6.1 SCP客户端配置任务简介

SCP 客户端配置任务如下：
(1) 生成本地密钥对仅采用 publickey、password-publickey 或 any 认证方式时必选。
(2) （可选）配置 SCP 客户端发送 SCP 报文使用的源 IP 地址
(3) 与远程SCP服务器传输文件
(4) （可选）SCP客户端删除保存在公钥文件中的服务器公钥
(5) （可选）与远程的SCP服务器建立基于Suite B算法集的连接

##### 1.6.2 生成本地密钥对

功能简介
1.
客户端采用 publickey 、 password-publickey 或 any 认证方式时，需要生成本地密钥对。

###### 2. 配置限制和指导

SSH 仅支持默认名称的本地 DSA、ECDSA 或 RSA 密钥对，不支持指定名称的本地 DSA、ECDSA或 密钥对。关于密钥对生成命令的相关介绍请参见“安全命令参考”中的“公钥管理”。
RSA

生成 DSA 密钥对时，要求输入的密钥模数的长度必须小于 2048 比特。
SSH 客户端支持 secp256r1 和 secp384r1 类型的 ECDSA 密钥对。
设备运行于 FIPS 模式时，仅支持 ECDSA、RSA 密钥对。

###### 3. 配置步骤

进入系统视图。
(1)
system-view
(2) 生成本地密钥对。
public-key local create { dsa | ecdsa { secp256r1 | secp384r1 } | rsa }

##### 1.6.3 配置SCP客户端发送SCP报文使用的源IP地址

###### 1. 功能简介

客户端与 服务器通信时，缺省采用路由决定的源 地址作为发送报文的源地址。如果使SCP SCP IP用本配置指定了源 IP 地址或源接口，则采用该地址与服务器进行通信。

###### 2. 配置限制和指导

为保证 SCP 客户端与 SCP 服务器通信链路的可达性，以及增加认证业务对 SCP 客户端的可管理性，通常建议指定 Loopback 接口的 IP 地址作为源 IP 地址。

###### 3. 配置步骤

进入系统视图。
(1)
system-view
(2) 配置 SCP 客户端发送 SCP 报文使用的源 IP 地址。
（IPv4 网络）
scp client source { interface interface-type interface-number | ip ip-address }缺省情况下，未配置 客户端使用的源 地址，SCP 客户端发送 报文使用的源SCP IPv4 SCP IPv4 地址为设备路由指定的 SCP 报文出接口的主 IP 地址。
（IPv6 网络）
scp client ipv6 source { interface interface-type interface-number | ipv6 ipv6-address }缺省情况下，未配置 SCP 客户端使用的源 IPv6 地址，设备自动选择 IPv6 SCP 报文的源 IPv6地址，具体选择原则请参见 RFC 3484。

##### 1.6.4 与远程SCP服务器传输文件

###### 1. 功能简介

该配置任务用来启动 SCP 客户端程序，与远程 SCP 服务器建立连接，并进行安全的文件传输操作。
SCP 客户端访问服务器时，需要通过本地保存的服务器端的主机公钥来验证服务器的身份。设备作为 客户端时，默认支持首次认证，即当 客户端首次访问服务器，而客户端没有配置服务SCP SCP器端的主机公钥时，用户可以选择继续访问该服务器，并在客户端保存该主机公钥，不指定public-key ，则会把服务器公钥保存到公钥文件中，但不会保存到配置文件中；当用户下次访问

该服务器时，就以保存的主机公钥来认证该服务器。首次认证在比较安全的网络环境中可以简化客户端的配置，但由于该方式下客户端完全相信服务器公钥的正确性，因此存在一定的安全隐患。

###### 2. 配置限制和指导

客户端不能同时连接 IPv4 和 IPv6 类型的服务器。

###### 3. 与远程IPv4 SCP服务器建立连接，并进行文件传输

请在用户视图下执行以下命令，与远程 IPv4 SCP 服务器建立连接，并进行文件传输。
（非 FIPS 模式）
scp server [ port-number ] [ vpn-instance vpn-instance-name ] { put | get } source-file-name [ destination-file-name ] [ identity-key { dsa | ecdsa-sha2-nistp256 | ecdsa-sha2-nistp384 | rsa | { x509v3-ecdsa-sha2-nistp256 | x509v3-ecdsa-sha2-nistp384 } pki-domain domain-name } | prefer-compress zlib | prefer-ctos-cipher { 3des-cbc | aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm | des-cbc } | prefer-ctos-hmac { md5 | md5-96 | sha1 | sha1-96 | sha2-256 | sha2-512 | sm3 } | prefer-kex { dh-group-exchange-sha1 | dh-group1-sha1 | dh-group14-sha1 | ecdh-sha2-nistp256 | ecdh-sha2-nistp384 } | prefer-stoc-cipher { 3des-cbc | aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm | des-cbc } | prefer-stoc-hmac { md5 | md5-96 | sha1 | sha1-96 | sha2-256 | sha2-512 | sm3 } ]
* [ { public-key keyname | server-pki-domain domain-name } | source { interface interface-type interface-number | ip ip-address } ] * [ user username [ password password ] ]（FIPS 模式）
scp server [ port-number ] [ vpn-instance vpn-instance-name ] { put | get } source-file-name [ destination-file-name ] [ identity-key { ecdsa-sha2-nistp256 | ecdsa-sha2-nistp384 | rsa | { x509v3-ecdsa-sha2-nistp256 | x509v3-ecdsa-sha2-nistp384 } pki-domain domain-name } | prefer-compress zlib | prefer-ctos-cipher { aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm } | prefer-ctos-hmac { sha1 | sha1-96 | sha2-256 | sha2-512 } | prefer-kex { dh-group14-sha1 | ecdh-sha2-nistp256 | ecdh-sha2-nistp384 } | prefer-stoc-cipher { aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm } | prefer-stoc-hmac { sha1 | sha1-96 | sha2-256 | sha2-512 } ] * [ { public-key keyname | server-pki-domain domain-name } | source { interface interface-type interface-number | ip ip-address } ] * [ user username [ password password ] ]

###### 4. 与远程IPv6 SCP服务器建立连接，并进行文件传输

请在用户视图下执行以下命令，与远程 服务器建立连接，并进行文件传输。
IPv6 SCP（非 模式）
FIPS

scp ipv6 server [ port-number ] [ vpn-instance vpn-instance-name ] [ -i interface-type interface-number ] { put | get } source-file-name [ destination-file-name ] [ identity-key { dsa | ecdsa-sha2-nistp256 | ecdsa-sha2-nistp384 | rsa | { x509v3-ecdsa-sha2-nistp256 | x509v3-ecdsa-sha2-nistp384 } pki-domain domain-name } | prefer-compress zlib | prefer-ctos-cipher { 3des-cbc | aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm | des-cbc } | prefer-ctos-hmac { md5 | md5-96 | sha1 | sha1-96 | sha2-256 | sha2-512 | sm3 } | prefer-kex { dh-group-exchange-sha1 | dh-group1-sha1 | dh-group14-sha1 | ecdh-sha2-nistp256 | ecdh-sha2-nistp384 } | prefer-stoc-cipher { 3des-cbc | aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm | des-cbc } | prefer-stoc-hmac { md5 | md5-96 | sha1 | sha1-96 | sha2-256 | sha2-512 | sm3 } ] * [ { public-key keyname | server-pki-domain domain-name } | source { interface interface-type interface-number | ipv6 ipv6-address } ] * [ user username [ password password ] ]（FIPS 模式）
scp ipv6 server [ port-number ] [ vpn-instance vpn-instance-name ] [ -i interface-type interface-number ] { put | get } source-file-name [ destination-file-name ] [ identity-key { ecdsa-sha2-nistp256 | ecdsa-sha2-nistp384 | rsa | { x509v3-ecdsa-sha2-nistp256 | x509v3-ecdsa-sha2-nistp384 } pki-domain domain-name } | prefer-compress zlib | prefer-ctos-cipher { aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm } | prefer-ctos-hmac { sha1 | sha1-96 | sha2-256 | sha2-512 } | prefer-kex { dh-group14-sha1 | ecdh-sha2-nistp256 | ecdh-sha2-nistp384 } | prefer-stoc-cipher { aes128-cbc | aes128-ctr | aes128-gcm | aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm } | prefer-stoc-hmac { sha1 | sha1-96 | sha2-256 | sha2-512 } ] * [ { public-key keyname | server-pki-domain domain-name } | source { interface interface-type interface-number | ipv6 ipv6-address } ] * [ user username [ password password ] ]

##### 1.6.5 SCP客户端删除保存在公钥文件中的服务器公钥

###### 1. 功能简介

客户端切换到 FIPS 模式后，如果已经保存的服务器公钥不符合 FIPS 模式要求，则无法登录到服务器。如果客户端想要重新登录该服务器，则需要执行本配置删除本地文件中的指定服务器公钥，并保证服务器上已经生成了符合 模式要求的公钥。
FIPS

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) SCP 客户端删除保存在公钥文件中的服务器公钥。
delete ssh client server-public-key [ server-ip ip-address ]

##### 1.6.6 与远程的SCP服务器建立基于Suite B算法集的连接

请在用户视图下执行本命令，与远程的 服务器建立基于 算法集的连接。
SCP Suite B（IPv4 网络）
scp server [ port-number ] [ vpn-instance vpn-instance-name ] { put | get } source-file-name [ destination-file-name ] suite-b [ 128-bit | 192-bit ] pki-domain domain-name [ server-pki-domain domain-name ] [ prefer-compress zlib ] [ source { interface interface-type interface-number | ip ip-address } ]
* [ user username [ password password ] ]（IPv6 网络）
scp ipv6 server [ port-number ] [ vpn-instance vpn-instance-name ] [ -i interface-type interface-number ] { put | get } source-file-name [ destination-file-name ] suite-b [ 128-bit | 192-bit ] pki-domain domain-name [ server-pki-domain domain-name ] [ prefer-compress zlib ] [ source { interface interface-type inte rface-number | ipv6 ipv6-address } ] * [ user username [ password password ] ]

#### 1.7 配置SSH2协议算法集

##### 1.7.1 SSH协议算法集简介

设备作为服务器或者客户端与对端建立 Stelnet、SFTP、SCP 会话过程中，将使用指定的算法优先列表进行协商。指定的算法包括：
• 密钥交换算法
• 主机签名算法
• 加密算法
• MAC 算法协商过程中，客户端采用的算法匹配顺序为优先列表中各算法的配置顺序，服务器根据客户端的算法来匹配和协商。

##### 1.7.2 配置SSH2协议密钥交换算法优先列表

进入系统视图。
(1)
system-view配置 协议密钥交换算法优先列表。
(2) SSH2（非 模式）
FIPS ssh2 algorithm key-exchange { dh-group-exchange-sha1 | dh-group1-sha1 | dh-group14-sha1 | ecdh-sha2-nistp256 | ecdh-sha2-nistp384 } *缺省情况下， SSH2 协议采用的缺省密钥交换算法从高到底的优先级列表为ecdh-sha2-nistp256 、 ecdh-sha2-nistp384 、 dh-group-exchange-sha1 、dh-group14-sha1 和 dh-group1-sha1。
（FIPS 模式）

ssh2 algorithm key-exchange { dh-group14-sha1 | ecdh-sha2-nistp256 | ecdh-sha2-nistp384 } *缺省情况下，SSH2 协议采用的缺省密钥交换算法从高到底的优先级列表为ecdh-sha2-nistp256、ecdh-sha2-nistp384 和 dh-group14-sha1。

##### 1.7.3 配置SSH2协议主机签名算法优先列表

(1) 进入系统视图。
system-view
(2) 配置 SSH2 协议主机签名算法优先列表。
（非 FIPS 模式）
ssh2 algorithm public-key { dsa | ecdsa-sha2-nistp256 |
ecdsa-sha2-nistp384 | rsa | x509v3-ecdsa-sha2-nistp256 |
x509v3-ecdsa-sha2-nistp384 } *
缺省情况下，SSH2 协议使用的缺省主机签名算法从高到底的优先级列表为
x509v3-ecdsa-sha2-nistp256、x509v3-ecdsa-sha2-nistp384、
ecdsa-sha2-nistp256、ecdsa-sha2-nistp384、rsa 和 dsa。
（FIPS 模式）
ssh2 algorithm public-key { ecdsa-sha2-nistp256 | ecdsa-sha2-nistp384
| rsa | x509v3-ecdsa-sha2-nistp256 | x509v3-ecdsa-sha2-nistp384 } *
缺省情况下，SSH2 协议使用的缺省主机签名算法从高到底的优先级列表为
x509v3-ecdsa-sha2-nistp256、x509v3-ecdsa-sha2-nistp384、
ecdsa-sha2-nistp256、ecdsa-sha2-nistp384、rsa。

##### 1.7.4 配置SSH2协议加密算法优先列表

(1) 进入系统视图。
system-view
(2) 配置 SSH2 协议加密算法优先列表。
（非 FIPS 模式）
ssh2 algorithm cipher { 3des-cbc | aes128-cbc | aes128-ctr | aes128-gcm
| aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm | des-cbc } *
缺省情况下，SSH2 协议采用的缺省加密算法从高到底的优先级列表为 aes128-ctr、
aes192-ctr、aes256-ctr、aes128-gcm、aes256-gcm、aes128-cbc、3des-cbc、
aes256-cbc 和 des-cbc。
（FIPS 模式）
ssh2 algorithm cipher { aes128-cbc | aes128-ctr | aes128-gcm |
aes192-ctr | aes256-cbc | aes256-ctr | aes256-gcm } *
缺省情况下，SSH2 协议采用的缺省加密算法从高到底的优先级列表为 aes128-ctr 、
aes192-ctr 、 aes256-ctr 、 aes128-gcm 、 aes256-gcm 、 aes128-cbc 和
aes256-cbc。

##### 1.7.5 配置SSH2协议MAC算法优先列表

进入系统视图。
(1)
system-view配置 协议 算法优先列表。
(2) SSH2 MAC（非 FIPS 模式）
ssh2 algorithm mac { md5 | md5-96 | sha1 | sha1-96 | sha2-256 | sha2-512 | sm3 } *缺省情况下，SSH2 协议使用的缺省 算法从高到底的优先级列表为 sha2-256、MAC sha2-512、sha1、md5、sha1-96、md5-96 和 sm3。
（FIPS 模式）
ssh2 algorithm mac { sha1 | sha1-96 | sha2-256 | sha2-512 } *缺省情况下，SSH2 协议使用的缺省 MAC 算法从高到底的优先级列表为 sha2-256、sha2-512、sha1 和 sha1-96。

#### 1.8 SSH显示和维护

在完成上述配置后，在任意视图下执行 display 命令，可以显示配置后 SSH 的运行情况，通过查看显示信息验证配置的效果。
表1-2 SSH 显示和维护操作 命令display public-key local { dsa | ecdsa | rsa }显示本地密钥对中的公钥部分public [ name publickey-name ] display public-key peer [ brief | name显示保存在本地的远端主机的公钥信息publickey-name ]显示SCP客户端的源IP地址配置 display scp client source显示SFTP客户端的源IP地址配置 display sftp client source display ssh client server-public-key显示SSH客户端公钥文件中的服务器公钥信息[ server-ip ip-address ]显示Stelnet客户端的源IP地址配置 display ssh client source在SSH服务器端显示该服务器的状态信息或会display ssh server { session | status }话信息display ssh user-information在SSH服务器端显示SSH用户信息 [ username ]显示设备上配置的SSH2协议使用的算法优先列display ssh2 algorithm表

###### 3. 配置步骤

display public-key local 和 display public-key peer 命令的详细介绍请参见“安全

#### 1.9 Stelnet典型配置举例

• 举例中的设备运行于非 FIPS 模式下。
• 若设备运行于 FIPS 模式下，相关的配置和显示信息将有所变化，请以设备的实际情况为准。
设备作为服务器仅支持 ECDSA、RSA 密钥对，请不要生成 DSA 密钥对。

##### 1.9.1 设备作为Stelnet服务器配置举例（password认证）

###### 1. 组网需求

• 用户可以通过 Host 上运行的 Stelnet 客户端软件（SSH2 版本）安全地登录到 Switch 上，并
被授予用户角色 network-admin 进行配置管理；
• Switch 采用 password 认证方式对 Stelnet 客户端进行认证，客户端的用户名和密码保存在本
地。

###### 2. 组网图

图1-1 设备作为 服务器配置组网图Stelnet Stelnet client Stelnet server Vlan-int2
192.168.1.56/24 192.168.1.40/24 Host Switch配置步骤
3.
(1) 配置 Stelnet 服务器\# 生成 RSA 密钥对。
<Switch> system-view [Switch] public-key local create rsa The range of public key modulus is (512 ~ 4096).
If the key modulus is greater than 512, it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
..++++++++

Create the key pair successfully.
\# 生成 DSA 密钥对。
[Switch] public-key local create dsa The range of public key modulus is (512 ~ 2048).
If the key modulus is greater than 512, it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
.++++++++++++++++++++++++++++++++++++++++++++++++++* Create the key pair successfully.
\# 生成 ECDSA 密钥对。
[Switch] public-key local create ecdsa secp256r1 Generating Keys...
.
Create the key pair successfully.
\# 开启 Stelnet 服务器功能。
[Switch] ssh server enable配置 接口 的 地址，客户端将通过该地址连接 服务器。
\# VLAN 2 IP Stelnet [Switch] interface vlan-interface 2 [Switch-Vlan-interface2] ip address 192.168.1.40 255.255.255.0 [Switch-Vlan-interface2] quit设置 客户端登录用户线的认证方式为 认证。
\# Stelnet AAA [Switch] line vty 0 63 [Switch-line-vty0-63] authentication-mode scheme [Switch-line-vty0-63] quit创建设备管理类本地用户 client001，并设置密码为明文 aabbcc，服务类型为 SSH，用户角\#色为 network-admin。
[Switch] local-user client001 class manage [Switch-luser-manage-client001] password simple aabbcc [Switch-luser-manage-client001] service-type ssh [Switch-luser-manage-client001] authorization-attribute user-role network-admin [Switch-luser-manage-client001] quit \# 配置 SSH 用户 client001 的服务类型为 Stelnet，认证方式为 password 认证。（此步骤可以不配置）
[Switch] ssh user client001 service-type stelnet authentication-type password
(2) Stelnet 客户端建立与 Stelnet 服务器的连接Stelnet 客户端软件有很多，例如 PuTTY、OpenSSH 等。本文中仅以客户端软件 PuTTY0.58为例，说明 Stelnet 客户端的配置方法。

\# 建立与 Stelnet 服务器端的连接。
打开PuTTY.exe程序，出现如 图 1-2 所示的客户端配置界面。在“Host Name（or IP address）”文本框中输入Stelnet服务器的IP地址为 192.168.1.40。
图1-2 Stelnet 客户端配置界面在 图 1-2 中，单击<Open>按钮。按提示输入用户名client001 及密码aabbcc，即可进入Switch的配置界面。

##### 1.9.2 设备作为Stelnet服务器配置举例（publickey认证）

###### 1. 组网需求

• 用户可以通过 Host 上运行的 Stelnet 客户端软件（SSH2 版本）安全地登录到 Switch 上，并
被授予用户角色 network-admin 进行配置管理；
• Switch 采用 publickey 认证方式对 Stelnet 客户端进行认证，使用的公钥算法为 RSA。

###### 2. 组网图

图1-3 设备作为 Stelnet 服务器配置组网图Stelnet client Stelnet server Vlan-int2
192.168.1.40/24
192.168.1.56/24 Host Switch

###### 3. 配置步骤

在服务器的配置过程中需要指定客户端的公钥信息，因此建议首先完成客户端密钥对的配置，
•再进行服务器的配置。
• 客户端软件有很多，例如 PuTTY、OpenSSH 等。本文中仅以客户端软件 PuTTY0.58 为例，说明 Stelnet 客户端的配置方法。
配置 客户端
(1) Stelnet生成 密钥对。
\# RSA在客户端运行 PuTTYGen.exe，在参数栏中选择“SSH-2 RSA”，点击<Generate>，产生客户端密钥对。
图1-4 生成客户端密钥（步骤 1）

在产生密钥对的过程中需不停地移动鼠标，鼠标移动仅限于下图蓝色框中除绿色标记进程条外的地方，否则进程条的显示会不动，密钥对将停止产生，见 图 1-5。
图1-5 生成客户端密钥（步骤 2）
密钥对产生后，点击<Save key>，输入存储公钥的文件名 key.pub，点击<保存>按public钮。

图1-6 生成客户端密钥（步骤 3）
点击<Save private key>存储私钥，弹出警告框，提醒是否保存没做任何保护措施的私钥，点击<Yes>，输入私钥文件名为 private.ppk，点击保存。
图1-7 生成客户端密钥（步骤 4）
客户端生成密钥对后，需要将保存的公钥文件 通过 方式上传到服务器，key.pub FTP/TFTP具体过程略。
(2) 配置 Stelnet 服务器\# 生成 RSA 密钥对。
<Switch> system-view [Switch] public-key local create rsa The range of public key modulus is (512 ~ 4096).
If the key modulus is greater than 512, it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...

..++++++++ Create the key pair successfully.
\# 生成 DSA 密钥对。
[Switch] public-key local create dsa The range of public key modulus is (512 ~ 2048).
If the key modulus is greater than 512, it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
.++++++++++++++++++++++++++++++++++++++++++++++++++* Create the key pair successfully.
生成 密钥对。
\# ECDSA [Switch] public-key local create ecdsa secp256r1 Generating Keys...
.
Create the key pair successfully.
\# 开启 Stelnet 服务器功能。
[Switch] ssh server enable \# 配置 VLAN 接口 2 的 IP 地址，客户端将通过该地址连接 Stelnet 服务器。
[Switch] interface vlan-interface 2 [Switch-Vlan-interface2] ip address 192.168.1.40 255.255.255.0 [Switch-Vlan-interface2] quit \# 设置 Stelnet 客户端登录用户线的认证方式为 AAA 认证。
[Switch] line vty 0 63 [Switch-line-vty0-63] authentication-mode scheme [Switch-line-vty0-63] quit \# 从文件 key.pub 中导入远端的公钥，并命名为 switchkey。
[Switch] public-key peer switchkey import sshkey key.pub \# 设置 SSH 用户 client002 的认证方式为 publickey，并指定公钥为 switchkey。
[Switch] ssh user client002 service-type stelnet authentication-type publickey assign publickey switchkey \# 创建设备管理类本地用户 client002，并设置服务类型为 SSH，用户角色为network-admin。
[Switch] local-user client002 class manage [Switch-luser-manage-client002] service-type ssh [Switch-luser-manage-client002] authorization-attribute user-role network-admin [Switch-luser-manage-client002] quit
(3) Stelnet 客户端建立与 Stelnet 服务器的连接\# 指定私钥文件，并建立与 Stelnet 服务器的连接。
打开PuTTY.exe程序，出现如 图 1-8 所示的客户端配置界面。在“Host Name（or IP address）”文本框中输入Stelnet服务器的IP地址为 192.168.1.40。

图1-8 Stelnet 客户端配置界面\# 单击左侧导航栏“Connection->SSH”，出现如 图 1-9 的界面。选择“Preferred SSH protocol version”为“2”。

图1-9 Stelnet 客户端配置界面单击左侧导航栏“Connection->SSH”下面的“Auth”（认证），出现如 图 1-10 的界面。单击<Browse…>按钮，弹出文件选择窗口。选择与配置到服务器端的公钥对应的私钥文件private.ppk。

###### 1. 组网需求

图1-10 Stelnet 客户端配置界面如 图 1-10，单击<Open>按钮。按提示输入用户名client002，即可进入Switch的配置界面。

##### 1.9.3 设备作为Stelnet客户端配置举例（password认证）

组网需求
1.
• 配置 Switch A 作为 Stelnet 客户端，用户能够通过 Switch A 安全地登录到 Switch B 上，并被授予用户角色 network-admin 进行配置管理。
Switch B 作为 Stelnet 服务器采用 password 认证方式对 Stelnet 客户端进行认证，客户端的
•用户名和密码保存在 上。
Switch B

###### 2. 组网图

图1-11 设备作为 Stelnet 客户端配置组网图

###### 3. 配置步骤

配置 服务器
(1) Stelnet生成 密钥对。
\# RSA <SwitchB> system-view

[SwitchB] public-key local create rsa The range of public key modulus is (512 ~ 4096).
If the key modulus is greater than 512, it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
..++++++++ Create the key pair successfully.
\# 生成 DSA 密钥对。
[SwitchB] public-key local create dsa The range of public key modulus is (512 ~ 2048).
If the key modulus is greater than 512, it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
.++++++++++++++++++++++++++++++++++++++++++++++++++* Create the key pair successfully.
\# 生成 ECDSA 密钥对。
[SwitchB] public-key local create ecdsa secp256r1 Generating Keys...
.
Create the key pair successfully.
\# 开启 Stelnet 服务器功能。
[SwitchB] ssh server enable配置 接口 的 地址，客户端将通过该地址连接 服务器。
\# VLAN 2 IP Stelnet [SwitchB] interface vlan-interface 2 [SwitchB-Vlan-interface2] ip address 192.168.1.40 255.255.255.0 [SwitchB-Vlan-interface2] quit设置 客户端登录用户线的认证方式为 认证。
\# Stelnet AAA [SwitchB] line vty 0 63 [SwitchB-line-vty0-63] authentication-mode scheme [SwitchB-line-vty0-63] quit创建设备管理类本地用户 client001，并设置密码为明文 aabbcc，服务类型为 SSH，用户角\#色为 network-admin。
[SwitchB] local-user client001 class manage [SwitchB-luser-manage-client001] password simple aabbcc [SwitchB-luser-manage-client001] service-type ssh [SwitchB-luser-manage-client001] authorization-attribute user-role network-admin [SwitchB-luser-manage-client001] quit \# 配置 SSH 用户 client001 的服务类型为 Stelnet，认证方式为 password 认证。（此步骤可以不配置）

[SwitchB] ssh user client001 service-type stelnet authentication-type password
(2) Stelnet 客户端建立与 Stelnet 服务器的连接\# 配置 VLAN 接口 2 的 IP 地址。
<SwitchA> system-view [SwitchA] interface vlan-interface 2 [SwitchA-Vlan-interface2] ip address 192.168.1.56 255.255.255.0 [SwitchA-Vlan-interface2] quit [SwitchA] quit客户端本地没有服务器端的主机公钥，首次与服务器建立连接(cid:123)
\# 建立到服务器 192.168.1.40 的 SSH 连接，选择在不认证服务器的情况下继续访问服务网，并在客户端保存服务器端的本地公钥。
<SwitchA> ssh2 192.168.1.40 Username: client001 Press CTRL+C to abort.
Connecting to 192.168.1.40 port 22.
The server is not authenticated. Continue? [Y/N]:y Do you want to save the server public key? [Y/N]:y client001@192.168.1.40's password:
Enter a character ~ and a dot to abort.
******************************************************************************
* Copyright (c) 2004-2017 New H3C Technologies Co., Ltd. All rights reserved.*
* Without the owner's prior written consent, *
* no decompiling or reverse-engineering shall be allowed. *
******************************************************************************* <SwitchB>输入正确的密码之后，即可成功登录到 Switch B 上。由于选择在本地保存服务器端的主机公钥，下次用户登录 Switch B 时直接输入正确密码即可成功登录。
客户端配置服务器端的主机公钥后，与服务器建立连接(cid:123)
\# 在客户端配置 SSH 服务器端的主机公钥。在公钥视图输入服务器端的主机公钥，即在服务器端通过 display public-key local dsa public 命令显示的公钥内容。
[SwitchA] public-key peer key1 Enter public key view. Return to system view with "peer-public-key end" command.
[SwitchA-pkey-public-key-key1]308201B73082012C06072A8648CE3804013082011F0281810 0D757262C4584C44C211F18BD96E5F0 [SwitchA-pkey-public-key-key1]61C4F0A423F7FE6B6B85B34CEF72CE14A0D3A5222FE08CECE 65BE6C265854889DC1EDBD13EC8B274 [SwitchA-pkey-public-key-key1]DA9F75BA26CCB987723602787E922BA84421F22C3C89CB9B0 6FD60FE01941DDD77FE6B12893DA76E [SwitchA-pkey-public-key-key1]EBC1D128D97F0678D7722B5341C8506F358214B16A2FAC4B3 68950387811C7DA33021500C773218C [SwitchA-pkey-public-key-key1]737EC8EE993B4F2DED30F48EDACE915F0281810082269009E 14EC474BAF2932E69D3B1F18517AD95 [SwitchA-pkey-public-key-key1]94184CCDFCEAE96EC4D5EF93133E84B47093C52B20CD35D02

492B3959EC6499625BC4FA5082E22C5 [SwitchA-pkey-public-key-key1]B374E16DD00132CE71B020217091AC717B612391C76C1FB2E 88317C1BD8171D41ECB83E210C03CC9 [SwitchA-pkey-public-key-key1]B32E810561C21621C73D6DAAC028F4B1585DA7F42519718CC 9B09EEF0381840002818000AF995917 [SwitchA-pkey-public-key-key1]E1E570A3F6B1C2411948B3B4FFA256699B3BF871221CC9C5D F257523777D033BEE77FC378145F2AD [SwitchA-pkey-public-key-key1]D716D7DB9FCABB4ADBF6FB4FDB0CA25C761B308EF53009F71 01F7C62621216D5A572C379A32AC290 [SwitchA-pkey-public-key-key1]E55B394A217DA38B65B77F0185C8DB8095522D1EF044B465E 8716261214A5A3B493E866991113B2D [SwitchA-pkey-public-key-key1]485348 [SwitchA-pkey-public-key-key1] peer-public-key end [SwitchA] quit \# 建立到服务器 192.168.1.40 的 SSH 连接，并指定服务器端的主机公钥。
<SwitchA> ssh2 192.168.1.40 public-key key1 Username: client001 Press CTRL+C to abort.
Connecting to 192.168.1.40 port 22.
client001@192.168.1.40's password:
Enter a character ~ and a dot to abort.
******************************************************************************
* Copyright (c) 2004-2017 New H3C Technologies Co., Ltd. All rights reserved.*
* Without the owner's prior written consent, *
* no decompiling or reverse-engineering shall be allowed. *
****************************************************************************** <SwitchB>输入正确的密码之后，即可成功登录到 Switch B 上。
客户端本地已有服务器端的主机公钥，直接与服务器建立连接(cid:123)
<SwitchA> ssh2 192.168.1.40 Username: client001 Press CTRL+C to abort.
Connecting to 192.168.1.40 port 22.
client001@192.168.1.40's password:
Enter a character ~ and a dot to abort.
******************************************************************************
* Copyright (c) 2004-2017 New H3C Technologies Co., Ltd. All rights reserved.*
* Without the owner's prior written consent, *
* no decompiling or reverse-engineering shall be allowed. *
****************************************************************************** <SwitchB>输入正确的密码之后，即可成功登录到 Switch B 上。

###### 1. 组网需求

##### 1.9.4 设备作为Stelnet客户端配置举例（publickey认证）

组网需求
1.
• 配置 Switch A 作为 Stelnet 客户端，用户能够通过 Switch A 安全地登录到 Switch B 上，并被授予用户角色 进行配置管理。
network-admin Switch B 作为 Stelnet 服务器采用 publickey 认证方式对 Stelnet 客户端进行认证，使用的公钥
•算法为 DSA。

###### 2. 组网图

图1-12 设备作为 Stelnet 客户端配置组网图

###### 3. 配置步骤

配置 客户端
(1) Stelnet在服务器的配置过程中需要指定客户端的公钥信息，因此需要首先完成客户端密钥对的配置，再进行服务器的配置。
\# 配置 VLAN 接口 2 的 IP 地址。
<SwitchA> system-view [SwitchA] interface vlan-interface 2 [SwitchA-Vlan-interface2] ip address 192.168.1.56 255.255.255.0 [SwitchA-Vlan-interface2] quit \# 生成 DSA 密钥对。
[SwitchA] public-key local create dsa The range of public key modulus is (512 ~ 2048).
If the key modulus is greater than 512, it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
.++++++++++++++++++++++++++++++++++++++++++++++++++* Create the key pair successfully.
将生成的 主机公钥导出到指定文件 中。
\# DSA key.pub [SwitchA] public-key local export dsa ssh2 key.pub [SwitchA] quit客户端生成密钥对后，需要将保存的公钥文件 key.pub 通过 FTP/TFTP 方式上传到服务器，具体过程略。

(2) 配置 Stelnet 服务器
\# 生成 RSA 密钥对。
<SwitchB> system-view
[SwitchB] public-key local create rsa
The range of public key modulus is (512 ~ 4096)
If the key modulus is greater than 512, it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
..++++++++
Create the key pair successfully.
\# 生成 DSA 密钥对。
[SwitchB] public-key local create dsa
The range of public key modulus is (512 ~ 2048).
If the key modulus is greater than 512, it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
.++++++++++++++++++++++++++++++++++++++++++++++++++*
Create the key pair successfully.
\# 生成 ECDSA 密钥对。
[SwitchB] public-key local create ecdsa secp256r1
Generating Keys...
.
Create the key pair successfully.
开启 服务器功能。
\# Stelnet
[SwitchB] ssh server enable
\# 配置 VLAN 接口 2 的 IP 地址，客户端将通过该地址连接 SSH 服务器。
[SwitchB] interface vlan-interface 2
[SwitchB-Vlan-interface2] ip address 192.168.1.40 255.255.255.0
[SwitchB-Vlan-interface2] quit
\# 设置 Stelnet 客户端登录用户线的认证方式为 AAA 认证。
[SwitchB] line vty 0 63
[SwitchB-line-vty0-63] authentication-mode scheme
[SwitchB-line-vty0-63] quit
\# 从文件 key.pub 中导入远端的公钥，并命名为 switchkey。
[SwitchB] public-key peer switchkey import sshkey key.pub
设置 用户 的认证方式为 publickey，并指定公钥为 switchkey。
\# SSH client002
[SwitchB] ssh user client002 service-type stelnet authentication-type publickey assign
publickey switchkey

##### 1.9.5 设备支持Stelnet Suite B配置举例（128-bit）

###### 2. 组网图

\# 创建设备管理类本地用户 client002，并设置服务类型为 SSH，用户角色为network-admin。
[SwitchB] local-user client002 class manage [SwitchB-luser-manage-client002] service-type ssh [SwitchB-luser-manage-client002] authorization-attribute user-role network-admin [SwitchB-luser-manage-client002] quit
(3) Stelnet 客户端建立与 Stelnet 服务器的连接\# 建立到服务器 192.168.1.40 的 SSH 连接。
<SwitchA> ssh2 192.168.1.40 identity-key dsa Username: client002 Press CTRL+C to abort.
Connecting to 192.168.1.40 port 22.
The server is not authenticated. Continue? [Y/N]:y Do you want to save the server public key? [Y/N]:n Enter a character ~ and a dot to abort.
******************************************************************************
* Copyright (c) 2004-2017 New H3C Technologies Co., Ltd. All rights reserved.*
* Without the owner's prior written consent, *
* no decompiling or reverse-engineering shall be allowed. *
****************************************************************************** <SwitchB>由于本地未保存服务器端的主机公钥，因此在选择继续访问服务器之后，即可成功登录到上。
Switch B设备支持Stelnet B配置举例（128-bit）
1.9.5 Suite

###### 1. 组网需求

配置 作为 客户端，用户能够通过 安全地登录到
• Switch A Stelnet Suite B Switch A Switch B上
• SwitchB 设备配置为 suite-b 服务器模式。
• 用户可以通过 Switch A 上运行的 Stelnet Suite B 客户端软件（ SSH2 版本）安全地登录到Switch B 上，并被授予用户角色 network-admin 进行配置管理。
• Switch B 采用 publickey 认证方式对 Stelnet Suite B 客户端进行认证。
组网图
2.
图1-13 设备支持 Stelnet Suite B 组网图

###### 3. 配置步骤

• 在服务器的配置过程中需要指定服务器和客户端的证书信息，因此需要首先完成证书的配置，
再进行 Suite B 相关的服务器配置。
• 客户端软件支持 Suite B 的较少，OpenSSH 的 pkix 版本通过修改可以实现。本文中仅以我司
设备客户端为例，说明 客户端的配置方法。
Stelnet Suite B
(1) 配置 Stelnet Suite B 客户端
\# 通过 FTP/TFTP 方式上传服务器证书文件 ssh-server-ecdsa256.p12 和客户端证书文件
ssh-client-ecdsa256.p12 到客户端设备，具体过程略。
\# 配置验证服务器证书的 PKI 域。
<SwitchA> system-view
[SwitchA] pki domain server256
关闭 检查。
\# CRL
[SwitchA-pki-domain-server256] undo crl check enable
[SwitchA-pki-domain-server256] quit
\# 导入本地证书文件。
[SwitchA] pki import domain server256 p12 local filename ssh-server-ecdsa256.p12
The system is going to save the key pair. You must specify a key pair name, which is
a case-insensitive string of 1 to 64 characters. Valid characters include a to z, A to
Z, 0 to 9, and hyphens (-).
Please enter the key pair name[default name: server256]:
\# 显示导入本地证书文件信息。
[SwitchA] display pki certificate domain server256 local
Certificate:
Data:
Version: 3 (0x2)
Serial Number: 3 (0x3)
Signature Algorithm: ecdsa-with-SHA256
Issuer: C=CN, ST=Beijing, L=Beijing, O=H3C, OU=Software, CN=SuiteB CA
Validity
Not Before: Aug 21 08:39:51 2015 GMT
Not After : Aug 20 08:39:51 2016 GMT
Subject: C=CN, ST=Beijing, O=H3C, OU=Software, CN=SSH Server secp256
Subject Public Key Info:
Public Key Algorithm: id-ecPublicKey
Public-Key: (256 bit)
pub:
04:a2:b4:b4:66:1e:3b:d5:50:50:0e:55:19:8d:52:
6d:47:8c:3d:3d:96:75:88:2f:9a:ba:a2:a7:f9:ef:
0a:a9:20:b7:b6:6a:90:0e:f8:c6:de:15:a2:23:81:
3c:9e:a2:b7:83:87:b9:ad:28:c8:2a:5e:58:11:8e:
c7:61:4a:52:51
ASN1 OID: prime256v1

NIST CURVE: P-256 X509v3 extensions:
X509v3 Basic Constraints:
CA:FALSE Netscape Comment:
OpenSSL Generated Certificate X509v3 Subject Key Identifier:
08:C1:F1:AA:97:45:19:6A:DA:4A:F2:87:A1:1A:E8:30:BD:31:30:D7 X509v3 Authority Key Identifier:
keyid:5A:BE:85:49:16:E5:EB:33:80:25:EB:D8:91:50:B4:E6:3E:4F:B8:22 Signature Algorithm: ecdsa-with-SHA256 30:65:02:31:00:a9:16:e9:c1:76:f0:32:fc:4b:f9:8f:b6:7f:
31:a0:9f:de:a7:cc:33:29:27:2c:71:2e:f9:0d:74:cb:25:c9:
00:d2:52:18:7f:58:3f:cc:7e:8b:d3:42:65:00:cb:63:f8:02:
30:01:a2:f6:a1:51:04:1c:61:78:f6:6b:7e:f9:f9:42:8d:7c:
a7:bb:47:7c:2a:85:67:0d:81:12:0b:02:98:bc:06:1f:c1:3c:
9b:c2:1b:4c:44:38:5a:14:b2:48:63:02:2b \# 配置客户端向服务器发送证书所在的 PKI 域。
[SwitchA] pki domain client256 \# 关闭 CRL 检查。
[SwitchA-pki-domain-client256] undo crl check enable [SwitchA-pki-domain-client256] quit \# 导入本地证书文件。
[SwitchA] pki import domain client256 p12 local filename ssh-client-ecdsa256.p12 The system is going to save the key pair. You must specify a key pair name, which is a case-insensitive string of 1 to 64 characters. Valid characters include a to z, A to Z, 0 to 9, and hyphens (-).
Please enter the key pair name[default name: client256]:
\# 显示导入本地证书文件信息。
[SwitchA] display pki certificate domain client256 local Certificate:
Data:
Version: 3 (0x2)
Serial Number: 4 (0x4)
Signature Algorithm: ecdsa-with-SHA256 Issuer: C=CN, ST=Beijing, L=Beijing, O=H3C, OU=Software, CN=SuiteB CA Validity Not Before: Aug 21 08:41:09 2015 GMT Not After : Aug 20 08:41:09 2016 GMT Subject: C=CN, ST=Beijing, O=H3C, OU=Software, CN=SSH Client secp256 Subject Public Key Info:
Public Key Algorithm: id-ecPublicKey Public-Key: (256 bit)
pub:
04:da:e2:26:45:87:7a:63:20:e7:ca:7f:82:19:f5:
96:88:3e:25:46:f8:2f:9a:4c:70:61:35:db:e4:39:
b8:38:c4:60:4a:65:28:49:14:32:3c:cc:6d:cd:34:

29:83:84:74:a7:2d:0e:75:1c:c2:52:58:1e:22:16:
12:d0:b4:8a:92 ASN1 OID: prime256v1 NIST CURVE: P-256 X509v3 extensions:
X509v3 Basic Constraints:
CA:FALSE Netscape Comment:
OpenSSL Generated Certificate X509v3 Subject Key Identifier:
1A:61:60:4D:76:40:B8:BA:5D:A1:3C:60:BC:57:98:35:20:79:80:FC X509v3 Authority Key Identifier:
keyid:5A:BE:85:49:16:E5:EB:33:80:25:EB:D8:91:50:B4:E6:3E:4F:B8:22 Signature Algorithm: ecdsa-with-SHA256 30:66:02:31:00:9a:6d:fd:7d:ab:ae:54:9a:81:71:e6:bb:ad:
5a:2e:dc:1d:b3:8a:bf:ce:ee:71:4e:8f:d9:93:7f:a3:48:a1:
5c:17:cb:22:fa:8f:b3:e5:76:89:06:9f:96:47:dc:34:87:02:
31:00:e3:af:2a:8f:d6:8d:1f:3a:2b:ae:2f:97:b3:52:63:b6:
18:67:70:2c:93:2a:41:c0:e7:fa:93:20:09:4d:f4:bf:d0:11:
66:0f:48:56:01:1e:c3:be:37:4e:49:19:cf:c6 \# 配置 VLAN 接口 2 的 IP 地址。
<SwitchA> system-view [SwitchA] interface vlan-interface 2 [SwitchA-Vlan-interface2] ip address 192.168.1.56 255.255.255.0 [SwitchA-Vlan-interface2] quit
(2) 配置 Stelnet Suite B 服务器\# 服务器上配置证书的 PKI 域与客户端相同，具体过程略。
\# 配置服务器 suite-b 算法集。
<SwitchB> system-view [SwitchB] ssh2 algorithm key-exchange ecdh-sha2-nistp256 [SwitchB] ssh2 algorithm cipher aes128-gcm [SwitchB] ssh2 algorithm public-key x509v3-ecdsa-sha2-nistp256 x509v3-ecdsa-sha2-nistp384配置服务器证书所在的 域。
\# PKI [SwitchB] ssh server pki-domain server256 \# 开启 Stelnet 服务器功能。
[SwitchB] ssh server enable \# 配置 VLAN 接口 2 的 IP 地址，客户端将通过该地址连接 Stelnet 服务器。
[SwitchB] interface vlan-interface 2 [SwitchB-Vlan-interface2] ip address 192.168.1.40 255.255.255.0 [SwitchB-Vlan-interface2] quit \# 设置 Stelnet 客户端登录用户线的认证方式为 AAA 认证。
[SwitchB] line vty 0 63 [SwitchB-line-vty0-63] authentication-mode scheme [SwitchB-line-vty0-63] quit

###### 1. 组网需求

\# 创建设备管理类本地用户 client001，服务类型为 SSH，用户角色为 network-admin。
[SwitchB] local-user client001 class manage [SwitchB-luser-manage-client001] service-type ssh [SwitchB-luser-manage-client001] authorization-attribute user-role network-admin [SwitchB-luser-manage-client001] quit \# 设置 SSH 用户 client001 的认证方式为 publickey，并指定认证证书所在 PKI 域为client256。
[SwitchB] ssh user client001 service-type stelnet authentication-type publickey assign pki-domain client256
(3) Stelnet Suite B 客户端建立与 Stelnet suite-b 服务器的连接\# 建立到服务器 192.168.1.40 的 SSH 连接。
<SwitchA> ssh2 192.168.1.40 suite-b 128-bit pki-domain client256 server-pki-domain server256 Username: client001 Press CTRL+C to abort.
Connecting to 192.168.1.40 port 22.
Enter a character ~ and a dot to abort.
******************************************************************************
* Copyright (c) 2004-2017 New H3C Technologies Co., Ltd. All rights reserved.*
* Without the owner's prior written consent, *
* no decompiling or reverse-engineering shall be allowed. *
****************************************************************************** <SwitchB>

#### 1.10 SFTP典型配置举例

• 举例中的设备运行于非 FIPS 模式下。
• 若设备运行于 FIPS 模式下，相关的配置和显示信息将有所变化，请以设备的实际情况为准。
设备作为服务器仅支持 ECDSA、RSA 密钥对，请不要生成 密钥对。
DSA

##### 1.10.1 设备作为SFTP服务器配置举例（password认证）

组网需求
1.
• 用户可以通过 Host 上运行的 SFTP 客户端软件安全地登录到 Switch 上，并被授予用户角色network-admin 进行文件管理和文件传送等操作；
Switch采用 password认证方式对 SFTP客户端进行认证，客户端的用户名和密码保存在本地。
•

###### 2. 组网图

图1-14 设备作为 SFTP 服务器配置组网图

###### 3. 配置步骤

配置 服务器
(1) SFTP生成 密钥对。
\# RSA <Switch> system-view [Switch] public-key local create rsa The range of public key modulus is (512 ~ 4096).
If the key modulus is greater than 512, it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
..++++++++ Create the key pair successfully.
生成 密钥对。
\# DSA [Switch] public-key local create dsa The range of public key modulus is (512 ~ 2048).
If the key modulus is greater than 512, it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
.++++++++++++++++++++++++++++++++++++++++++++++++++* Create the key pair successfully.
\# 生成 ECDSA 密钥对。
[Switch] public-key local create ecdsa secp256r1 Generating Keys...
.
Create the key pair successfully.
\# 启动 SFTP 服务器。
[Switch] sftp server enable \# 配置 VLAN 接口 2 的 IP 地址，客户端将通过该地址连接 SSH 服务器。
[Switch] interface vlan-interface 2 [Switch-Vlan-interface2] ip address 192.168.1.45 255.255.255.0 [Switch-Vlan-interface2] quit

\# 创建设备管理类本地用户 client002，并设置密码为明文 aabbcc，服务类型为 SSH，用户角色为 network-admin，工作目录为 flash:/。
[Switch] local-user client002 class manage [Switch-luser-manage-client002] password simple aabbcc [Switch-luser-manage-client002] service-type ssh [Switch-luser-manage-client002] authorization-attribute user-role network-admin work-directory flash:/ [Switch-luser-manage-client002] quit \# 配置 SSH 用户认证方式为 password，服务类型为 SFTP。（此步骤可以不配置）
[Switch] ssh user client002 service-type sftp authentication-type password客户端建立与 服务器的连接
(2) SFTP SFTP SFTP 客户端软件有很多，本文中仅以客户端软件 PuTTY0.58 中的 PSFTP 为例，说明
•SFTP 客户端的配置方法。
只支持 认证，不支持 认证。
• PSFTP password publickey \# 建立与 SFTP 服务器的连接。
打开psftp.exe程序，出现如 图 1-15 所示的客户端配置界面。输入如下命令：
open 192.168.1.45根据提示输入用户名 client002，密码 aabbcc，即可登录 SFTP 服务器。
图1-15 SFTP 客户端登录界面

###### 1. 组网需求

##### 1.10.2 设备作为SFTP客户端配置举例（publickey认证）

组网需求
1.
• 配置 Switch A 作为 SFTP 客户端，用户能够通过 Switch A 安全地登录到 Switch B 上，并被授予用户角色 进行文件管理和文件传送等操作。
network-admin Switch B 作为 SFTP 服务器采用 publickey 认证方式对 SFTP 客户端进行认证，使用的公钥算
•法为 RSA。

###### 2. 组网图

图1-16 设备作为 SFTP 客户端配置组网图

###### 3. 配置步骤

配置 客户端
(1) SFTP在服务器的配置过程中需要指定客户端的公钥信息，因此建议首先完成客户端密钥对的配置，再进行服务器的配置。
\# 配置 VLAN 接口 2 的 IP 地址。
<SwitchA> system-view [SwitchA] interface vlan-interface 2 [SwitchA-Vlan-interface2] ip address 192.168.0.2 255.255.255.0 [SwitchA-Vlan-interface2] quit \# 生成 RSA 密钥对。
[SwitchA] public-key local create rsa The range of public key modulus is (512 ~ 4096).
If the key modulus is greater than 512, it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
..++++++++ Create the key pair successfully.
\# 将生成的 RSA 主机公钥导出到指定文件 pubkey 中。
[SwitchA] public-key local export rsa ssh2 pubkey [SwitchA] quit

客户端生成密钥对后，需要将保存的公钥文件 pubkey通过 FTP/TFTP 方式上传到服务器，具体过程略。
配置 服务器
(2) SFTP生成 密钥对。
\# RSA <SwitchB> system-view [SwitchB] public-key local create rsa The range of public key modulus is (512 ~ 4096).
If the key modulus is greater than 512, it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
..++++++++ Create the key pair successfully.
生成 密钥对。
\# DSA [SwitchB] public-key local create dsa The range of public key modulus is (512 ~ 2048).
If the key modulus is greater than 512, it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
.++++++++++++++++++++++++++++++++++++++++++++++++++* Create the key pair successfully.
\# 生成 ECDSA 密钥对。
[SwitchB] public-key local create ecdsa secp256r1 Generating Keys...
.
Create the key pair successfully.
\# 启动 SFTP 服务器。
[SwitchB] sftp server enable \# 配置 VLAN 接口 2 的 IP 地址，客户端将通过该地址连接 SSH 服务器。
[SwitchB] interface vlan-interface 2 [SwitchB-Vlan-interface2] ip address 192.168.0.1 255.255.255.0 [SwitchB-Vlan-interface2] quit \# 从文件 pubkey 中导入远端的公钥，并命名为 switchkey。
[SwitchB] public-key peer switchkey import sshkey pubkey \# 设置 SSH 用户 client001 的服务类型为 SFTP，认证方式为 publickey，并指定公钥为switchkey 。
[SwitchB] ssh user client001 service-type sftp authentication-type publickey assign publickey switchkey \# 创建设备管理类本地用户 client001，并设置服务类型为 SSH，用户角色为 network-admin，工作目录为 flash:/ 。

[SwitchB] local-user client001 class manage [SwitchB-luser-manage-client001] service-type ssh [SwitchB-luser-manage-client001] authorization-attribute user-role network-admin work-directory flash:/ [SwitchB-luser-manage-client001] quit
(3) SFTP 客户端建立与 SFTP 服务器端的连接\# 与远程 SFTP 服务器建立连接，进入 SFTP 客户端视图。
<SwitchA> sftp 192.168.0.1 identity-key rsa Username: client001 Press CTRL+C to abort.
Connecting to 192.168.0.1 port 22.
The server is not authenticated. Continue? [Y/N]:y Do you want to save the server public key? [Y/N]:n sftp>显示服务器的当前目录，删除文件 z，并检查此文件是否删除成功。
\# sftp> dir -l
-rwxrwxrwx 1 noone nogroup 1759 Aug 23 06:52 config.cfg
-rwxrwxrwx 1 noone nogroup 225 Aug 24 08:01 pubkey2
-rwxrwxrwx 1 noone nogroup 283 Aug 24 07:39 pubkey drwxrwxrwx 1 noone nogroup 0 Sep 01 06:22 new
-rwxrwxrwx 1 noone nogroup 225 Sep 01 06:55 pub
-rwxrwxrwx 1 noone nogroup 0 Sep 01 08:00 z sftp> delete z Removing /z sftp> dir -l
-rwxrwxrwx 1 noone nogroup 1759 Aug 23 06:52 config.cfg
-rwxrwxrwx 1 noone nogroup 225 Aug 24 08:01 pubkey2
-rwxrwxrwx 1 noone nogroup 283 Aug 24 07:39 pubkey drwxrwxrwx 1 noone nogroup 0 Sep 01 06:22 new
-rwxrwxrwx 1 noone nogroup 225 Sep 01 06:55 pub新增目录 new1，并检查新目录是否创建成功。
\# sftp> mkdir new1 sftp> dir -l
-rwxrwxrwx 1 noone nogroup 1759 Aug 23 06:52 config.cfg
-rwxrwxrwx 1 noone nogroup 225 Aug 24 08:01 pubkey2
-rwxrwxrwx 1 noone nogroup 283 Aug 24 07:39 pubkey drwxrwxrwx 1 noone nogroup 0 Sep 01 06:22 new
-rwxrwxrwx 1 noone nogroup 225 Sep 01 06:55 pub drwxrwxrwx 1 noone nogroup 0 Sep 02 06:30 new1 \# 将目录名 new1 更名为 new2，并查看是否更名成功。
sftp> rename new1 new2 sftp> dir -l
-rwxrwxrwx 1 noone nogroup 1759 Aug 23 06:52 config.cfg
-rwxrwxrwx 1 noone nogroup 225 Aug 24 08:01 pubkey2
-rwxrwxrwx 1 noone nogroup 283 Aug 24 07:39 pubkey drwxrwxrwx 1 noone nogroup 0 Sep 01 06:22 new
-rwxrwxrwx 1 noone nogroup 225 Sep 01 06:55 pub

##### 1.10.3 设备支持SFTP Suite B配置举例（192-bit）

###### 2. 组网图

drwxrwxrwx 1 noone nogroup 0 Sep 02 06:33 new2 \# 从服务器上下载文件 pubkey2 到本地，并更名为 public。
sftp> get pubkey2 public Fetching / pubkey2 to public /pubkey2 100% 225 1.4KB/s 00:00 \# 将本地文件 pu 上传到服务器上，更名为 puk，并查看上传是否成功。
sftp> put pu puk Uploading pu to / puk sftp> dir -l
-rwxrwxrwx 1 noone nogroup 1759 Aug 23 06:52 config.cfg
-rwxrwxrwx 1 noone nogroup 225 Aug 24 08:01 pubkey2
-rwxrwxrwx 1 noone nogroup 283 Aug 24 07:39 pubkey drwxrwxrwx 1 noone nogroup 0 Sep 01 06:22 new drwxrwxrwx 1 noone nogroup 0 Sep 02 06:33 new2
-rwxrwxrwx 1 noone nogroup 283 Sep 02 06:35 pub
-rwxrwxrwx 1 noone nogroup 283 Sep 02 06:36 puk sftp> \# 退出 SFTP 客户端视图。
sftp> quit <SwitchA>设备支持SFTP B配置举例（192-bit）
1.10.3 Suite

###### 1. 组网需求

• 配置 Switch A作为 SFTP Suite B客户端，用户能够通过 Switch A安全地登录到 Switch B上。
设备配置为 服务器模式。
• SwitchB Suite B
用户可以通过 上运行的 客户端软件（SSH2 版本）安全地登录到
• Switch A SFTP Suite B Switch
B 上，并被授予用户角色 network-admin 进行配置管理。
• Switch B 采用 publickey 认证方式对 SFTP Suite B 客户端进行认证。
组网图
2.
图1-17 设备支持 SFTP Suite B 配置组网图

###### 3. 配置步骤

• 在服务器的配置过程中需要指定服务器和客户端的证书信息，因此需要首先完成证书的配置，
再进行 Suite B 相关的服务器配置。
• 客户端软件支持 Suite B 的较少，OpenSSH 的 pkix 版本通过修改可以实现。本文中仅以我司
设备客户端为例，说明 客户端的配置方法。
SFTP Suite B
(1) 配置 SFTP Suite B 客户端
\# 通过 FTP/TFTP 方式上传服务器证书文件 ssh-server-ecdsa384.p12 和客户端证书文件
ssh-client-ecdsa384.p12 到客户端设备，具体过程略。
\# 配置验证服务器证书的 PKI 域。
<SwitchA> system-view
[SwitchA] pki domain server384
关闭 检查。
\# CRL
[SwitchA-pki-domain-server384] undo crl check enable
[SwitchA-pki-domain-server384] quit
\# 导入本地证书文件。
[SwitchA] pki import domain server384 p12 local filename ssh-server-ecdsa384.p12
The system is going to save the key pair. You must specify a key pair name, which is
a case-insensitive string of 1 to 64 characters. Valid characters include a to z, A to
Z, 0 to 9, and hyphens (-).
Please enter the key pair name[default name: server384]:
\# 显示导入本地证书信息。
[SwitchA] display pki certificate domain server384 local
Certificate:
Data:
Version: 3 (0x2)
Serial Number: 1 (0x1)
Signature Algorithm: ecdsa-with-SHA384
Issuer: C=CN, ST=Beijing, L=Beijing, O=H3C, OU=Software, CN=SuiteB CA
Validity
Not Before: Aug 20 10:08:41 2015 GMT
Not After : Aug 19 10:08:41 2016 GMT
Subject: C=CN, ST=Beijing, O=H3C, OU=Software, CN=ssh server
Subject Public Key Info:
Public Key Algorithm: id-ecPublicKey
Public-Key: (384 bit)
pub:
04:4a:33:e5:99:8d:49:45:a7:a3:24:7b:32:6a:ed:
b6:36:e1:4d:cc:8c:05:22:f4:3a:7c:5d:b7:be:d1:
e6:9e:f0:ce:95:39:ca:fd:a0:86:cd:54:ab:49:60:
10:be:67:9f:90:3a:18:e2:7d:d9:5f:72:27:09:e7:
bf:7e:64:0a:59:bb:b3:7d:ae:88:14:94:45:b9:34:
d2:f3:93:e1:ba:b4:50:15:eb:e5:45:24:31:10:c7:

07:01:f9:dc:a5:6f:81 ASN1 OID: secp384r1 NIST CURVE: P-384 X509v3 extensions:
X509v3 Basic Constraints:
CA:FALSE Netscape Comment:
OpenSSL Generated Certificate X509v3 Subject Key Identifier:
10:16:64:2C:DA:C1:D1:29:CD:C0:74:40:A9:70:BD:62:8A:BB:F4:D5 X509v3 Authority Key Identifier:
keyid:5A:BE:85:49:16:E5:EB:33:80:25:EB:D8:91:50:B4:E6:3E:4F:B8:22 Signature Algorithm: ecdsa-with-SHA384 30:65:02:31:00:80:50:7a:4f:c5:cd:6a:c3:57:13:7f:e9:da:
c1:72:7f:45:30:17:c2:a7:d3:ec:73:3d:5f:4d:e3:96:f6:a3:
33:fb:e4:b9:ff:47:f1:af:9d:e3:03:d2:24:53:40:09:5b:02:
30:45:d1:bf:51:fd:da:22:11:90:03:f9:d4:05:ec:d6:7c:41:
fc:9d:a1:fd:5b:8c:73:f8:b6:4c:c3:41:f7:c6:7f:2f:05:2d:
37:f8:52:52:26:99:28:97:ac:6e:f9:c7:01 \# 配置客户端向服务器发送证书所在的 PKI 域。
[SwitchA] pki domain client384 \#关闭 CRL 检查。
[SwitchA-pki-domain-client384] undo crl check enable [SwitchA-pki-domain-client384] quit \#导入本地证书文件。
[SwitchA] pki import domain client384 p12 local filename ssh-client-ecdsa384.p12 The system is going to save the key pair. You must specify a key pair name, which is a case-insensitive string of 1 to 64 characters. Valid characters include a to z, A to Z, 0 to 9, and hyphens (-).
Please enter the key pair name[default name: client384]:
\# 显示导入本地证书信息。
[SwitchA]display pki certificate domain client384 local Certificate:
Data:
Version: 3 (0x2)
Serial Number: 2 (0x2)
Signature Algorithm: ecdsa-with-SHA384 Issuer: C=CN, ST=Beijing, L=Beijing, O=H3C, OU=Software, CN=SuiteB CA Validity Not Before: Aug 20 10:10:59 2015 GMT Not After : Aug 19 10:10:59 2016 GMT Subject: C=CN, ST=Beijing, O=H3C, OU=Software, CN=ssh client Subject Public Key Info:
Public Key Algorithm: id-ecPublicKey Public-Key: (384 bit)
pub:

04:85:7c:8b:f4:7a:36:bf:74:f6:7c:72:f9:08:69:
d0:b9:ac:89:98:17:c9:fc:89:94:43:da:9a:a6:89:
41:d3:72:24:9b:9a:29:a8:d1:ba:b4:e5:77:ba:fc:
df:ae:c6:dd:46:72:ab:bc:d1:7f:18:7d:54:88:f6:
b4:06:54:7e:e7:4d:49:b4:07:dc:30:54:4b:b6:5b:
01:10:51:6b:0c:6d:a3:b1:4b:c9:d9:6c:d6:be:13:
91:70:31:2a:92:00:76 ASN1 OID: secp384r1 NIST CURVE: P-384 X509v3 extensions:
X509v3 Basic Constraints:
CA:FALSE Netscape Comment:
OpenSSL Generated Certificate X509v3 Subject Key Identifier:
BD:5F:8E:4F:7B:FE:74:03:5A:D1:94:DB:CA:A7:82:D6:F7:78:A1:B0 X509v3 Authority Key Identifier:
keyid:5A:BE:85:49:16:E5:EB:33:80:25:EB:D8:91:50:B4:E6:3E:4F:B8:22 Signature Algorithm: ecdsa-with-SHA384 30:66:02:31:00:d2:06:fa:2c:0b:0d:f0:81:90:01:c3:3d:bf:
97:b3:79:d8:25:a0:e2:0e:ed:00:c9:48:3e:c9:71:43:c9:b4:
2a:a6:0a:27:80:9e:d4:0f:f2:db:db:5b:40:b1:a9:0a:e4:02:
31:00:ee:00:e1:07:c0:2f:12:3f:88:ea:fe:19:05:ef:56:ca:
33:71:75:5e:11:c9:a6:51:4b:3e:7c:eb:2a:4d:87:2b:71:7c:
30:64:fe:14:ce:06:d5:0a:e2:cf:9a:69:19:ff \# 配置 VLAN 接口 2 的 IP 地址。
[SwitchA] interface vlan-interface 2 [SwitchA-Vlan-interface2] ip address 192.168.0.2 255.255.255.0 [SwitchA-Vlan-interface2] quit [SwitchA] quit
(2) 配置 Stelnet Suite B 服务器\# 服务器上配置证书的 PKI 域与客户端相同，具体过程略。
\# 配置服务器 Suite B 算法集。
[SwitchB] ssh2 algorithm key-exchange ecdh-sha2-nistp384 [SwitchB] ssh2 algorithm cipher aes256-gcm [SwitchB] ssh2 algorithm public-key x509v3-ecdsa-sha2-nistp384 \# 配置服务器证书所在的 PKI 域。
[SwitchB] ssh server pki-domain server384 \# 开启 SFTP 服务器功能。
[SwitchB] sftp server enable \# 配置 VLAN 接口 2 的 IP 地址，客户端将通过该地址连接 SFTP 服务器。
[SwitchB] interface vlan-interface 2 [SwitchB-Vlan-interface2] ip address 192.168.0.1 255.255.255.0 [SwitchB-Vlan-interface2] quit \# 设置 SFTP 客户端登录用户线的认证方式为 AAA 认证。

[SwitchB] line vty 0 63 [SwitchB-line-vty0-63] authentication-mode scheme [SwitchB-line-vty0-63] quit \# 创建设备管理类本地用户 client001，服务类型为 SSH，用户角色为 network-admin。
[SwitchB] local-user client001 class manage [SwitchB-luser-manage-client001] service-type ssh [SwitchB-luser-manage-client001] authorization-attribute user-role network-admin [SwitchB-luser-manage-client001] quit \# 设置 SSH 用户 client001 的认证方式为 publickey，并指定认证证书所在 PKI 域为client384。
[SwitchB] ssh user client001 service-type sftp authentication-type publickey assign pki-domain client384
(3) SFTP Suite B 客户端建立与 SFTP Suite B 服务器的连接\# 建立到服务器 192.168.0.1 的 SSH 连接。
<SwitchA> sftp 192.168.0.1 suite-b 192-bit pki-domain client384 server-pki-domain server384 Username: client001 Press CTRL+C to abort.
Connecting to 192.168.0.1 port 22.
sftp>

#### 1.11 SCP典型配置举例

• 举例中的设备运行于非 FIPS 模式下。
• 若设备运行于 FIPS 模式下，相关的配置和显示信息将有所变化，请以设备的实际情况为准。
设备作为服务器仅支持 ECDSA、RSA 密钥对，请不要生成 DSA 密钥对。

##### 1.11.1 SCP文件传输配置举例（password认证）

###### 1. 组网需求

如下图所示，Switch A 作为 SCP 客户端，Switch B 作为 SCP 服务器。现有如下具体需求：
• 用户能够通过 Switch A 安全地安全地登录到 Switch B 上，并被授予用户角色 network-admin与 Switch B 进行文件传输。
• Switch B 采用 password 认证对 SCP 客户端进行认证，客户端的用户名和密码保存在 Switch B 上。

###### 2. 组网图

图1-18 SCP 文件传输配置组网图

###### 3. 配置步骤

配组SSwC置网iPtc图S文h B件P 采传服 用输务配p a置s s组wo网rd图认 证对SCP客户端进行认证，客户端的用户名和密码保存在Switch B上。
C 器
(1) 配置 SCP 服务器生成 密钥对。
\# RSA <SwitchB> system-view [SwitchB] public-key local create rsa The range of public key modulus is (512 ~ 4096).
If the key modulus is greater than 512, it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
..++++++++ Create the key pair successfully.
生成 密钥对。
\# DSA [SwitchB] public-key local create dsa The range of public key modulus is (512 ~ 2048).
If the key modulus is greater than 512, it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
.++++++++++++++++++++++++++++++++++++++++++++++++++* Create the key pair successfully.
\# 生成 ECDSA 密钥对。
[SwitchB] public-key local create ecdsa secp256r1 Generating Keys...
.
Create the key pair successfully.
\# 开启 SCP 服务器功能。
[SwitchB] scp server enable配置接口 接口 的 地址，客户端将通过该地址连接 服务器。
\# VLAN 2 IP SCP [SwitchB] interface vlan-interface 2 [SwitchB-Vlan-interface2] ip address 192.168.0.1 255.255.255.0 [SwitchB-Vlan-interface2] quit

\# 创建设备管理类本地用户 client001，并设置密码为明文 aabbcc，服务类型为 SSH。
[SwitchB] local-user client001 class manage [SwitchB-luser-manage-client001] password simple aabbcc [SwitchB-luser-manage-client001] service-type ssh [SwitchB-luser-manage-client001] authorization-attribute user-role network-admin [SwitchB-luser-manage-client001] quit配置 用户 的服务类型为 scp，认证方式为 认证。（此步骤可以不\# SSH client001 password配置）
[SwitchB] ssh user client001 service-type scp authentication-type password配置 客户端
(2) SCP配置接口 的 地址。
\# VLAN 2 IP <SwitchA> system-view [SwitchA] interface vlan-interface 2 [SwitchA-Vlan-interface2] ip address 192.168.0.2 255.255.255.0 [SwitchA-Vlan-interface2] quit [SwitchA] quit
(3) SCP 客户端从 SCP 服务器下载文件\# 与远程 SCP 服务器建立连接，并下载远端的 remote.bin 文件，下载到本地后更名为local.bin。
<SwitchA> scp 192.168.0.1 get remote.bin local.bin Username: client001 Press CTRL+C to abort.
Connecting to 192.168.0.1 port 22.
The server is not authenticated. Continue? [Y/N]:y Do you want to save the server public key? [Y/N]:n client001@192.168.0.1’s password:
remote.bin 100% 2875 2.8KB/s 00:00

##### 1.11.2 设备支持SCP Suite B配置举例

###### 1. 组网需求

配置 作为 客户端，用户能够通过 安全地登录到 上。
• Switch A SCP Suite B Switch A Switch B SwitchB 设备配置为 Suite B 服务器模式。
•用户可以通过 Switch A 上运行的 SCP Suite B 客户端软件（SSH2 版本）安全地登录到 Switch
•上，并被授予用户角色 进行配置管理。
B network-admin采用 认证方式对 客户端进行认证。
• Switch B publickey SCP Suite B

###### 2. 组网图

图1-19 设备支持 SCP Suite B 配置组网图

###### 3. 配置步骤

• 在服务器的配置过程中需要指定服务器和客户端的证书信息，因此需要首先完成证书的配置，
再进行 Suite B 相关的服务器配置。
• 客户端软件支持 Suite B 的较少，OpenSSH 的 pkix 版本通过修改可以实现。本文中仅以我司
设备客户端为例，说明 客户端的配置方法。
SCP Suite B
(1) 配置 SCP Suite B 客户端，导入两种证书
\# 通过 FTP/TFTP 方式上传服务器证书文件 ssh-server-ecdsa256.p12、
ssh-server-ecdsa384.p12 和客户端证书文件 ssh-client-ecdsa256.p12、
到客户端设备，具体过程略。
ssh-client-ecdsa384.p12
配置验证服务器 证书的 域。
\# ecdsa256 PKI
<SwitchA> system-view
[SwitchA] pki domain server256
\# 关闭 CRL 检查。
[SwitchA-pki-domain-server256] undo crl check enable
[SwitchA-pki-domain-server256] quit
\# 导入 CA 证书。
[SwitchA] pki import domain server256 p12 local filename ssh-server-ecdsa256.p12
The system is going to save the key pair. You must specify a key pair name, which is
a case-insensitive string of 1 to 64 characters. Valid characters include a to z, A to
Z, 0 to 9, and hyphens (-).
Please enter the key pair name[default name: server256]:
\# 显示导入 CA 证书信息。
[SwitchA] display pki certificate domain server256 local
Certificate:
Data:
Version: 3 (0x2)
Serial Number: 3 (0x3)
Signature Algorithm: ecdsa-with-SHA256
Issuer: C=CN, ST=Beijing, L=Beijing, O=H3C, OU=Software, CN=SuiteB CA
Validity
Not Before: Aug 21 08:39:51 2015 GMT
Not After : Aug 20 08:39:51 2016 GMT
Subject: C=CN, ST=Beijing, O=H3C, OU=Software, CN=SSH Server secp256
Subject Public Key Info:
Public Key Algorithm: id-ecPublicKey
Public-Key: (256 bit)
pub:
04:a2:b4:b4:66:1e:3b:d5:50:50:0e:55:19:8d:52:
6d:47:8c:3d:3d:96:75:88:2f:9a:ba:a2:a7:f9:ef:
0a:a9:20:b7:b6:6a:90:0e:f8:c6:de:15:a2:23:81:
3c:9e:a2:b7:83:87:b9:ad:28:c8:2a:5e:58:11:8e:
c7:61:4a:52:51

ASN1 OID: prime256v1 NIST CURVE: P-256 X509v3 extensions:
X509v3 Basic Constraints:
CA:FALSE Netscape Comment:
OpenSSL Generated Certificate X509v3 Subject Key Identifier:
08:C1:F1:AA:97:45:19:6A:DA:4A:F2:87:A1:1A:E8:30:BD:31:30:D7 X509v3 Authority Key Identifier:
keyid:5A:BE:85:49:16:E5:EB:33:80:25:EB:D8:91:50:B4:E6:3E:4F:B8:22 Signature Algorithm: ecdsa-with-SHA256 30:65:02:31:00:a9:16:e9:c1:76:f0:32:fc:4b:f9:8f:b6:7f:
31:a0:9f:de:a7:cc:33:29:27:2c:71:2e:f9:0d:74:cb:25:c9:
00:d2:52:18:7f:58:3f:cc:7e:8b:d3:42:65:00:cb:63:f8:02:
30:01:a2:f6:a1:51:04:1c:61:78:f6:6b:7e:f9:f9:42:8d:7c:
a7:bb:47:7c:2a:85:67:0d:81:12:0b:02:98:bc:06:1f:c1:3c:
9b:c2:1b:4c:44:38:5a:14:b2:48:63:02:2b \# 配置客户端向服务器发送 ecdsa256 证书所在的 PKI 域。
[SwitchA] pki domain client256 \# 关闭 CRL 检查。
[SwitchA-pki-domain-client256] undo crl check enable [SwitchA-pki-domain-client256] quit导入 证书。
\# CA [SwitchA] pki import domain client256 p12 local filename ssh-client-ecdsa256.p12 The system is going to save the key pair. You must specify a key pair name, which is a case-insensitive string of 1 to 64 characters. Valid characters include a to z, A to Z, 0 to 9, and hyphens (-).
Please enter the key pair name[default name: client256]:
显示导入 证书信息。
\# CA [SwitchA] display pki certificate domain client256 local Certificate:
Data:
Version: 3 (0x2)
Serial Number: 4 (0x4)
Signature Algorithm: ecdsa-with-SHA256 Issuer: C=CN, ST=Beijing, L=Beijing, O=H3C, OU=Software, CN=SuiteB CA Validity Not Before: Aug 21 08:41:09 2015 GMT Not After : Aug 20 08:41:09 2016 GMT Subject: C=CN, ST=Beijing, O=H3C, OU=Software, CN=SSH Client secp256 Subject Public Key Info:
Public Key Algorithm: id-ecPublicKey Public-Key: (256 bit)
pub:
04:da:e2:26:45:87:7a:63:20:e7:ca:7f:82:19:f5:

96:88:3e:25:46:f8:2f:9a:4c:70:61:35:db:e4:39:
b8:38:c4:60:4a:65:28:49:14:32:3c:cc:6d:cd:34:
29:83:84:74:a7:2d:0e:75:1c:c2:52:58:1e:22:16:
12:d0:b4:8a:92 ASN1 OID: prime256v1 NIST CURVE: P-256 X509v3 extensions:
X509v3 Basic Constraints:
CA:FALSE Netscape Comment:
OpenSSL Generated Certificate X509v3 Subject Key Identifier:
1A:61:60:4D:76:40:B8:BA:5D:A1:3C:60:BC:57:98:35:20:79:80:FC X509v3 Authority Key Identifier:
keyid:5A:BE:85:49:16:E5:EB:33:80:25:EB:D8:91:50:B4:E6:3E:4F:B8:22 Signature Algorithm: ecdsa-with-SHA256 30:66:02:31:00:9a:6d:fd:7d:ab:ae:54:9a:81:71:e6:bb:ad:
5a:2e:dc:1d:b3:8a:bf:ce:ee:71:4e:8f:d9:93:7f:a3:48:a1:
5c:17:cb:22:fa:8f:b3:e5:76:89:06:9f:96:47:dc:34:87:02:
31:00:e3:af:2a:8f:d6:8d:1f:3a:2b:ae:2f:97:b3:52:63:b6:
18:67:70:2c:93:2a:41:c0:e7:fa:93:20:09:4d:f4:bf:d0:11:
66:0f:48:56:01:1e:c3:be:37:4e:49:19:cf:c6 \# 配置验证服务器 ecdsa384 证书的 PKI 域。
[SwitchA] pki domain server384 \# 关闭 CRL 检查。
[SwitchA-pki-domain-server384] undo crl check enable [SwitchA-pki-domain-server384] quit导入 证书。
\# CA [SwitchA] pki import domain server384 p12 local filename ssh-server-ecdsa384.p12 The system is going to save the key pair. You must specify a key pair name, which is a case-insensitive string of 1 to 64 characters. Valid characters include a to z, A to Z, 0 to 9, and hyphens (-).
Please enter the key pair name[default name: server384]:
显示导入 证书信息。
\# CA [SwitchA] display pki certificate domain server384 local Certificate:
Data:
Version: 3 (0x2)
Serial Number: 1 (0x1)
Signature Algorithm: ecdsa-with-SHA384 Issuer: C=CN, ST=Beijing, L=Beijing, O=H3C, OU=Software, CN=SuiteB CA Validity Not Before: Aug 20 10:08:41 2015 GMT Not After : Aug 19 10:08:41 2016 GMT Subject: C=CN, ST=Beijing, O=H3C, OU=Software, CN=ssh server Subject Public Key Info:
Public Key Algorithm: id-ecPublicKey

Public-Key: (384 bit)
pub:
04:4a:33:e5:99:8d:49:45:a7:a3:24:7b:32:6a:ed:
b6:36:e1:4d:cc:8c:05:22:f4:3a:7c:5d:b7:be:d1:
e6:9e:f0:ce:95:39:ca:fd:a0:86:cd:54:ab:49:60:
10:be:67:9f:90:3a:18:e2:7d:d9:5f:72:27:09:e7:
bf:7e:64:0a:59:bb:b3:7d:ae:88:14:94:45:b9:34:
d2:f3:93:e1:ba:b4:50:15:eb:e5:45:24:31:10:c7:
07:01:f9:dc:a5:6f:81 ASN1 OID: secp384r1 NIST CURVE: P-384 X509v3 extensions:
X509v3 Basic Constraints:
CA:FALSE Netscape Comment:
OpenSSL Generated Certificate X509v3 Subject Key Identifier:
10:16:64:2C:DA:C1:D1:29:CD:C0:74:40:A9:70:BD:62:8A:BB:F4:D5 X509v3 Authority Key Identifier:
keyid:5A:BE:85:49:16:E5:EB:33:80:25:EB:D8:91:50:B4:E6:3E:4F:B8:22 Signature Algorithm: ecdsa-with-SHA384 30:65:02:31:00:80:50:7a:4f:c5:cd:6a:c3:57:13:7f:e9:da:
c1:72:7f:45:30:17:c2:a7:d3:ec:73:3d:5f:4d:e3:96:f6:a3:
33:fb:e4:b9:ff:47:f1:af:9d:e3:03:d2:24:53:40:09:5b:02:
30:45:d1:bf:51:fd:da:22:11:90:03:f9:d4:05:ec:d6:7c:41:
fc:9d:a1:fd:5b:8c:73:f8:b6:4c:c3:41:f7:c6:7f:2f:05:2d:
37:f8:52:52:26:99:28:97:ac:6e:f9:c7:01 \# 配置客户端向服务器发送 ecdsa384 证书所在的 PKI 域。
[SwitchA] pki domain client384 \# 关闭 CRL 检查。
[SwitchA-pki-domain-client384] undo crl check enable [SwitchA-pki-domain-client384] quit导入 证书。
\# CA [SwitchA] pki import domain client384 p12 local filename ssh-client-ecdsa384.p12 The system is going to save the key pair. You must specify a key pair name, which is a case-insensitive string of 1 to 64 characters. Valid characters include a to z, A to Z, 0 to 9, and hyphens (-).
Please enter the key pair name[default name: client384]:
显示导入 证书信息。
\# CA [SwitchA] display pki certificate domain client384 local Certificate:
Data:
Version: 3 (0x2)
Serial Number: 2 (0x2)
Signature Algorithm: ecdsa-with-SHA384 Issuer: C=CN, ST=Beijing, L=Beijing, O=H3C, OU=Software, CN=SuiteB CA

Validity Not Before: Aug 20 10:10:59 2015 GMT Not After : Aug 19 10:10:59 2016 GMT Subject: C=CN, ST=Beijing, O=H3C, OU=Software, CN=ssh client Subject Public Key Info:
Public Key Algorithm: id-ecPublicKey Public-Key: (384 bit)
pub:
04:85:7c:8b:f4:7a:36:bf:74:f6:7c:72:f9:08:69:
d0:b9:ac:89:98:17:c9:fc:89:94:43:da:9a:a6:89:
41:d3:72:24:9b:9a:29:a8:d1:ba:b4:e5:77:ba:fc:
df:ae:c6:dd:46:72:ab:bc:d1:7f:18:7d:54:88:f6:
b4:06:54:7e:e7:4d:49:b4:07:dc:30:54:4b:b6:5b:
01:10:51:6b:0c:6d:a3:b1:4b:c9:d9:6c:d6:be:13:
91:70:31:2a:92:00:76 ASN1 OID: secp384r1 NIST CURVE: P-384 X509v3 extensions:
X509v3 Basic Constraints:
CA:FALSE Netscape Comment:
OpenSSL Generated Certificate X509v3 Subject Key Identifier:
BD:5F:8E:4F:7B:FE:74:03:5A:D1:94:DB:CA:A7:82:D6:F7:78:A1:B0 X509v3 Authority Key Identifier:
keyid:5A:BE:85:49:16:E5:EB:33:80:25:EB:D8:91:50:B4:E6:3E:4F:B8:22 Signature Algorithm: ecdsa-with-SHA384 30:66:02:31:00:d2:06:fa:2c:0b:0d:f0:81:90:01:c3:3d:bf:
97:b3:79:d8:25:a0:e2:0e:ed:00:c9:48:3e:c9:71:43:c9:b4:
2a:a6:0a:27:80:9e:d4:0f:f2:db:db:5b:40:b1:a9:0a:e4:02:
31:00:ee:00:e1:07:c0:2f:12:3f:88:ea:fe:19:05:ef:56:ca:
33:71:75:5e:11:c9:a6:51:4b:3e:7c:eb:2a:4d:87:2b:71:7c:
30:64:fe:14:ce:06:d5:0a:e2:cf:9a:69:19:ff \# 配置 VLAN 接口 2 的 IP 地址。
[SwitchA] interface vlan-interface 2 [SwitchA-Vlan-interface2] ip address 192.168.0.2 255.255.255.0 [SwitchA-Vlan-interface2] quit
(2) 配置 SCP Suite B 服务器，导入两种证书\# 服务器上配置证书的 PKI 域与客户端相同，具体过程略。
\# 配置服务器 Suite B 算法集。
<SwitchB> system-view [SwitchB] ssh2 algorithm key-exchange ecdh-sha2-nistp256 ecdh-sha2-nistp384 [SwitchB] ssh2 algorithm cipher aes128-gcm aes256-gcm [SwitchB] ssh2 algorithm public-key x509v3-ecdsa-sha2-nistp256 x509v3-ecdsa-sha2-nistp384开启 服务器功能。
\# SCP

[SwitchB] scp server enable \# 配置 VLAN 接口 2 的 IP 地址，客户端将通过该地址连接 SFTP 服务器。
[SwitchB] interface vlan-interface 2 [SwitchB-Vlan-interface2] ip address 192.168.0.1 255.255.255.0 [SwitchB-Vlan-interface2] quit \# 设置 SCP 客户端登录用户线的认证方式为 AAA 认证。
[SwitchB] line vty 0 63 [SwitchB-line-vty0-63] authentication-mode scheme [SwitchB-line-vty0-63] quit \# 创建设备管理类本地用户 client001，服务类型为 SSH，用户角色为 network-admin。
[SwitchB] local-user client001 class manage [SwitchB-luser-manage-client001] service-type ssh [SwitchB-luser-manage-client001] authorization-attribute user-role network-admin [SwitchB-luser-manage-client001] quit创建设备管理类本地用户 client002，服务类型为 SSH，用户角色为 network-admin。
\# [SwitchB] local-user client002 class manage [SwitchB-luser-manage-client002] service-type ssh [SwitchB-luser-manage-client002] authorization-attribute user-role network-admin [SwitchB-luser-manage-client002] quit
(3) SCP Suite B 客户端建立与 SCP Suite B 服务器的 128-bit 连接\# 配置服务器证书所在的 PKI 域。
[SwitchB]ssh server pki-domain server256 \# 设置 SSH 用户 client001 的认证方式为 publickey，并指定认证证书所在 PKI 域为client256。
[SwitchB] ssh user client001 service-type scp authentication-type publickey assign pki-domain client256建立到服务器 的 连接。
\# 192.168.0.1 SSH <SwitchA> scp 192.168.0.1 get src.cfg suite-b 128-bit pki-domain client256 server-pki
-domain server256 Username: client001 Press CTRL+C to abort.
Connecting to 192.168.0.1 port 22.
src.cfg 100% 4814 4.7KB/s 00:00 <SwitchA>
(4) SCP suite-b 客户端建立与 SCP suite-b 服务器的 192-bit 连接\# 配置服务器证书所在的 PKI 域。
[SwitchB] ssh server pki-domain server384 \# 设置 SSH 用户 client002 的认证方式为 publickey，并指定认证证书所在 PKI 域为client384。
[Switch] ssh user client002 service-type scp authentication-type publickey assign pki-domain client384 \# 建立到服务器 192.168.0.1 的 SSH 连接。
<SwitchA> scp 192.168.0.1 get src.cfg suite-b 192-bit pki-domain client384 server-pki
-domain server384 Username: client002

###### 3. 配置步骤

Press CTRL+C to abort.
Connecting to 192.168.0.1 port 22.
src.cfg 100% 4814 4.7KB/s 00:00 <SwitchA>

#### 1.12 NETCONF over SSH典型配置举例

• 举例中的设备运行于非 FIPS 模式下。
• 若设备运行于 FIPS 模式下，相关的配置和显示信息将有所变化，请以设备的实际情况为准。
设备作为服务器仅支持 ECDSA、RSA 密钥对，请不要生成 DSA 密钥对。

##### 1.12.1 NETCONF over SSH配置举例（password认证）

###### 1. 组网需求

• 用户可以通过 Host上运行的支持 NETCONF over SSH连接的 SSH客户端软件（SSH2版本）
安全地登录到 Switch 上，并被授予用户角色 network-admin 进行配置管理；
• Switch 采用 password 认证方式对 SSH 客户端进行认证，客户端的用户名和密码保存在本
地。

###### 2. 组网图

图1-20 设备作为 服务器配置组网图NETCONF over SSH配置步骤
3.
组网图 设备作为 NETCONF over SSH 服务器配置组网图配置步骤\# 生成 RSA 密钥对。
<Switch> system-view [Switch] public-key local create rsa The range of public key modulus is (512 ~ 4096).
If the key modulus is greater than 512, it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
..++++++++ Create the key pair successfully.
\# 生成 DSA 密钥对。

[Switch] public-key local create dsa The range of public key modulus is (512 ~ 2048).
If the key modulus is greater than 512, it will take a few minutes.
Press CTRL+C to abort.
Input the modulus length [default = 1024]:
Generating Keys...
.++++++++++++++++++++++++++++++++++++++++++++++++++* Create the key pair successfully.
\# 生成 ECDSA 密钥对。
[Switch] public-key local create ecdsa secp256r1 Generating Keys...
.
Create the key pair successfully.
开启 服务器功能。
\# NETCONF over SSH [Switch] netconf ssh server enable \# 配置 VLAN 接口 2 的 IP 地址，客户端将通过该地址连接 NETCONF over SSH 服务器。
[Switch] interface vlan-interface 2 [Switch-Vlan-interface2] ip address 192.168.1.40 255.255.255.0 [Switch-Vlan-interface2] quit \# 设置 NETCONF over SSH 客户端登录用户线的认证方式为 AAA 认证。
[Switch] line vty 0 63 [Switch-line-vty0-63] authentication-mode scheme [Switch-line-vty0-63] quit \# 创建设备管理类本地用户 client001，并设置密码为明文 aabbcc，服务类型为 SSH，用户角色为network-admin。
[Switch] local-user client001 class manage [Switch-luser-manage-client001] password simple aabbcc [Switch-luser-manage-client001] service-type ssh [Switch-luser-manage-client001] authorization-attribute user-role network-admin [Switch-luser-manage-client001] quit \# 配置 SSH 用户 client001 的服务类型为 NETCONF，认证方式为 password 认证。（此步骤可以不配置）
[Switch] ssh user client001 service-type netconf authentication-type password

###### 4. 验证配置

用户通过支持 NETCONF over SSH 连接的客户端软件与 Switch 建立 NETCONF over SSH 连接之后，可直接进入 Switch 的 NETCONF 配置模式。

## 15-SSL配置

目 录简介服务器端配置任务简介禁止 服务器使用指定的 版本进行 协商

### 1 SSL

1 SSL

#### 1.1 SSL简介

SSL（Secure Layer，安全套接字层）是一个安全协议，为基于 的应用层协议（如Sockets TCP HTTP）提供安全连接。SSL 协议广泛应用于电子商务、网上银行等领域，为应用层数据的传输提供安全性保证。

##### 1.1.1 SSL安全机制

提供的安全连接可以实现如下功能：
SSL保证数据传输的机密性：利用对称密钥算法对传输的数据进行加密，并利用密钥交换算法，
•如 RSA（Rivest Shamir and Adleman），加密传输对称密钥算法中使用的密钥。对称密钥算法、非对称密钥算法 RSA 的详细介绍请参见“安全配置指导”中的“公钥管理”。
• 验证数据源的身份：基于数字证书利用数字签名方法对 SSL 服务器和 SSL 客户端进行身份验证。SSL 服务器和 SSL 客户端通过 PKI（Public Key Infrastructure，公钥基础设施）提供的机制获取数字证书。PKI 及数字证书的详细介绍请参见“安全配置指导”中的“PKI”。
保证数据的完整性：消息传输过程中使用MAC（Message Code，消息验证码）
• Authentication来检验消息的完整性。MAC算法在密钥的参与下，将任意长度的原始数据转换为固定长度的数据，原始数据的任何变化都会导致计算出的固定长度数据发生变化。如 图 1-1 所示，利用MAC算法验证消息完整性的过程为：
a. 发送者在密钥的参与下，利用 MAC 算法计算出消息的 MAC 值，并将其加在消息之后发送给接收者。
接收者利用同样的密钥和 算法计算出消息的 值，并与接收到的 值比较。
b. MAC MAC MAC如果二者相同，则接收者认为报文没有被篡改；否则，认为报文在传输过程中被篡改，接
c.
收者将丢弃该报文。
图1-1 算法示意图MAC发送者 接收者密钥Message 发送给Message接收者计算MAC MAC Message计算MAC MAC MAC 比较密钥

##### 1.1.2 SSL协议结构

如 图 1-2 所示，SSL协议可以分为两层：下层为SSL记录协议（SSL Record Protocol）；上层为SSL握手协议（SSL Protocol）、SSL密码变化协议（SSL Protocol）
Handshake Change Cipher Spec和SSL告警协议（SSL Alert Protocol）。

图1-2 SSL 协议栈SSL 记录协议：主要负责对上层的数据进行分块、计算并添加 MAC、加密，最后把加密后的
•记录块传输给对方。
握手协议：用来协商通信过程中使用的加密套件（数据加密算法、密钥交换算法和
• SSL MAC算法等），实现服务器和客户端的身份验证，并在服务器和客户端之间安全地交换密钥。客户端和服务器通过握手协议建立会话。一个会话包含一组参数，主要有会话 ID、对方的数字证书、加密套件及主密钥。
SSL 密码变化协议：客户端和服务器端通过密码变化协议通知对端，随后的报文都将使用新
•协商的加密套件和密钥进行保护和传输。
告警协议：用来向对端报告告警信息，以便对端进行相应的处理。告警消息中包含告警
• SSL的严重级别和描述。

##### 1.1.3 SSL协议版本

目前，SSL 协议版本主要有 SSL2.0、SSL3.0、TLS1.0（TLS1.0 对应 SSL 协议的版本号为 3.1）、和 TLS1.2。
TLS1.1由于 版本存在一些已知的安全漏洞，当设备对系统安全性有较高要求时，可以在 服务SSL 3.0 SSL器上通过命令行关闭 SSL 3.0 版本。

#### 1.2 FIPS相关说明

设备运行于 模式时，本特性的相关配置相对于非 模式有所变化，具体差异请见本文相关FIPS FIPS描述。有关 FIPS 模式的详细介绍请参见“安全配置指导”中的“FIPS”。

#### 1.3 SSL配置限制和指导

设备作为 SSL 服务器时，可以与 SSL3.0、TLS1.0、TLS1.1 和 TLS1.2 版本的 SSL 客户端通信，还可以识别同时兼容 SSL2.0/SSL3.0/TLS1.0/TLS1.1/TLS1.2 版本的 SSL 客户端发送的报文，并通知该客户端采用 SSL3.0/TLS1.0/TLS1.1/TLS1.2 版本与 SSL 服务器通信。

#### 1.4 SSL配置任务简介

##### 1.4.1 SSL服务器端配置任务简介

SSL 服务器端配置任务如下：
• 配置SSL服务器端策略

##### 1. 功能简介

（可选）禁止SSL服务器使用指定的SSL版本进行SSL协商
•（可选）配置SSL服务器端关闭SSL重协商
•

##### 1.4.2 SSL客户端配置任务简介

SSL 客户端配置任务如下：
• 配置SSL客户端策略

#### 1.5 配置SSL服务器端策略

功能简介
1.
SSL 服务器端策略是设备作为服务器时使用的 SSL 参数。只有与 HTTPS（Hypertext Transfer Protocol Secure，超文本传输协议的安全版本）等应用关联后，SSL 服务器端策略才能生效。

##### 2. 配置步骤

进入系统视图。
(1)
system-view创建 服务器端策略，并进入 服务器端策略视图。
(2) SSL SSL ssl server-policy policy-name配置 服务器端策略所使用的 域。
(3) SSL PKI pki-domain domain-name缺省情况下，未指定 SSL 服务器端策略所使用的 PKI 域。
如果客户端需要对服务器端进行基于数字证书的身份验证，则必须在 SSL 服务器端指定 PKI域，并在该 域内为 服务器端申请本地数字证书。PKI 域的创建及配置方法，请参见PKI SSL“安全配置指导”中的“PKI”。
(4) 配置 SSL 服务器端策略支持的加密套件。
（非 FIPS 模式）
ciphersuite { dhe_rsa_aes_128_cbc_sha | dhe_rsa_aes_128_cbc_sha256 | dhe_rsa_aes_256_cbc_sha | dhe_rsa_aes_256_cbc_sha256 | ecdhe_ecdsa_aes_128_cbc_sha256 | ecdhe_ecdsa_aes_128_gcm_sha256 | ecdhe_ecdsa_aes_256_cbc_sha384 | ecdhe_ecdsa_aes_256_gcm_sha384 | ecdhe_rsa_aes_128_cbc_sha256 | ecdhe_rsa_aes_128_gcm_sha256 | ecdhe_rsa_aes_256_cbc_sha384 | ecdhe_rsa_aes_256_gcm_sha384 | exp_rsa_des_cbc_sha | exp_rsa_rc2_md5 | exp_rsa_rc4_md5 | rsa_3des_ede_cbc_sha | rsa_aes_128_cbc_sha | rsa_aes_128_cbc_sha256 | rsa_aes_256_cbc_sha | rsa_aes_256_cbc_sha256 | rsa_des_cbc_sha | rsa_rc4_128_md5 | rsa_rc4_128_sha } *（FIPS 模式）
ciphersuite { ecdhe_ecdsa_aes_128_cbc_sha256 | ecdhe_ecdsa_aes_256_cbc_sha384 | ecdhe_ecdsa_aes_128_gcm_sha256 | ecdhe_ecdsa_aes_256_gcm_sha384 | ecdhe_rsa_aes_128_cbc_sha256 | ecdhe_rsa_aes_128_gcm_sha256 | ecdhe_rsa_aes_256_cbc_sha384 |

ecdhe_rsa_aes_256_gcm_sha384 | rsa_aes_128_cbc_sha | rsa_aes_128_cbc_sha256 | rsa_aes_256_cbc_sha | rsa_aes_256_cbc_sha256 }
*缺省情况下，SSL 服务器端策略支持所有的加密套件。
(5) （可选）配置 SSL 服务器上缓存的最大会话数目和 SSL 会话缓存的超时时间。
session { cachesize size | timeout time } *缺省情况下，SSL 服务器上缓存的最大会话数目为 500 个，SSL 会话缓存的超时时间为 3600秒。
(6) 配置 SSL 服务器端对 SSL 客户端的身份验证方案。
client-verify { enable | optional }缺省情况下，SSL 服务器端不要求对 SSL 客户端进行基于数字证书的身份验证。
SSL 服务器端在基于数字证书对 SSL 客户端进行身份验证时，除了对 SSL 客户端发送的证书链进行验证，还要检查证书链中的除根 CA 证书外的每个证书是否均未被吊销。

#### 1.6 配置SSL客户端策略

##### 1. 功能简介

客户端策略是客户端连接 服务器时使用的参数。只有与应用层协议，如 FTP（File SSL SSL Transfer Protocol，文件传输协议），关联后，SSL 客户端策略才能生效。FTP 的详细配置请参见“基础配置指导”中的“FTP”。

##### 2. 配置限制和指导

对安全性要求较高的环境下，建议不要为 SSL 客户端指定 SSL3.0 版本。

##### 3. 配置步骤

进入系统视图。
(1)
system-view创建 客户端策略，并进入 客户端策略视图。
(2) SSL SSL ssl client-policy policy-name
(3) 配置 SSL 客户端策略所使用的 PKI 域。
pki-domain domain-name缺省情况下，未指定 SSL 客户端策略所使用的 PKI 域。
如果服务器端需要对客户端进行基于数字证书的身份验证，则必须在 SSL 客户端指定 PKI 域，并在该 域内为 客户端申请本地数字证书。PKI 域的创建及配置方法，请参见“安全PKI SSL配置指导”中的“PKI”。
(4) 配置 SSL 客户端策略支持的加密套件。
（非 模式）
FIPS prefer-cipher { dhe_rsa_aes_128_cbc_sha | dhe_rsa_aes_128_cbc_sha256 | dhe_rsa_aes_256_cbc_sha | dhe_rsa_aes_256_cbc_sha256 | ecdhe_ecdsa_aes_128_cbc_sha256 | ecdhe_ecdsa_aes_128_gcm_sha256 | ecdhe_ecdsa_aes_256_cbc_sha384 | ecdhe_ecdsa_aes_256_gcm_sha384 |

##### 1. 功能简介

##### 3. 配置步骤

ecdhe_rsa_aes_128_cbc_sha256 | ecdhe_rsa_aes_128_gcm_sha256 | ecdhe_rsa_aes_256_cbc_sha384 | ecdhe_rsa_aes_256_gcm_sha384 | exp_rsa_des_cbc_sha | exp_rsa_rc2_md5 | exp_rsa_rc4_md5 | rsa_3des_ede_cbc_sha | rsa_aes_128_cbc_sha | rsa_aes_128_cbc_sha256 | rsa_aes_256_cbc_sha | rsa_aes_256_cbc_sha256 | rsa_des_cbc_sha | rsa_rc4_128_md5 | rsa_rc4_128_sha }缺省情况下，SSL 客户端策略支持的加密套件为 rsa_rc4_128_md5。
（FIPS 模式）
prefer-cipher { ecdhe_ecdsa_aes_128_cbc_sha256 | ecdhe_ecdsa_aes_128_gcm_sha256 | ecdhe_ecdsa_aes_256_cbc_sha384 | ecdhe_ecdsa_aes_256_gcm_sha384 | ecdhe_rsa_aes_128_cbc_sha256 | ecdhe_rsa_aes_128_gcm_sha256 | ecdhe_rsa_aes_256_cbc_sha384 | ecdhe_rsa_aes_256_gcm_sha384 | rsa_aes_128_cbc_sha | rsa_aes_128_cbc_sha256 | rsa_aes_256_cbc_sha | rsa_aes_256_cbc_sha256 }缺省情况下，SSL 客户端策略支持的加密套件为 rsa_aes_128_cbc_sha。
(5) 配置 SSL 客户端策略使用的 SSL 协议版本。
（非 FIPS 模式）
version { ssl3.0 | tls1.0 | tls1.1 | tls1.2 }（FIPS 模式）
version { tls1.0 | tls1.1 | tls1.2 }缺省情况下，SSL 客户端策略使用的 SSL 协议版本为 TLS 1.0。
(6) 配置客户端需要对服务器端进行基于数字证书的身份验证。
server-verify enable缺省情况下，SSL 客户端需要对 SSL 服务器端进行基于数字证书的身份验证。

#### 1.7 禁止SSL服务器使用指定的SSL版本进行SSL协商

功能简介
1.
当设备对系统安全性有较高要求时可以通过配置本功能关闭对应版本号的 SSL 协商。

##### 2. 配置限制和指导

如果通过本功能关闭了指定版本的 协商功能，并不会同时关闭比其更低版本的 协商功能，SSL SSL例如，ssl version tls1.1 disable 命令仅表示关闭了 TLS1.1 版本的 SSL 协商功能，不会同时关闭 TLS1.0 版本。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) 禁止 SSL 服务器使用指定的 SSL 版本进行 SSL 协商。
（非 FIPS 模式）
ssl version { ssl3.0 | tls1.0 | tls1.1 } * disable

缺省情况下，允许 SSL 服务器使用 SSL3.0、TLS1.0、TLS1.1 和 TLS1.2 版本的协商功能。
（FIPS 模式）
ssl version { tls1.0 | tls1.1 } * disable缺省情况下，允许使用 TLS1.0、TLS1.1 和 TLS1.2 版本的协商功能。

#### 1.8 配置SSL服务器端关闭SSL重协商

##### 1. 功能简介

关闭 重协商是指，不允许复用已有的 会话进行 快速协商，每次 协商必须进行SSL SSL SSL SSL完整的 SSL 握手过程。关闭 SSL 重协商会导致系统付出更多的计算开销，但可以避免潜在的风险，安全性更高。

##### 2. 配置限制和指导

通常情况下，不建议关闭 SSL 重协商。本命令仅用于用户明确要求关闭重协商的场景。

##### 3. 配置步骤

进入系统视图。
(1)
system-view配置 服务器端关闭 重协商。
(2) SSL SSL ssl renegotiation disable缺省情况下，允许 重协商。
SSL

#### 1.9 SSL显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 SSL 的运行情况，通过查看显示信息验证配置的效果。
表1-1 SSL 显示和维护操作 命令显示SSL客户端策略的信息 display ssl client-policy [ policy-name ]显示SSL服务器端策略的信息 display ssl server-policy [ policy-name ]

## 16-攻击检测与防范配置

目 录攻击检测及防范简介

### 1 攻击检测及防范

#### 1.1 攻击检测及防范简介

攻击检测及防范是一个重要的网络安全特性，它通过分析经过设备的报文的内容和行为，判断报文是否具有攻击特征，并根据配置对具有攻击特征的报文执行一定的防范措施，例如丢弃报文。
设备仅支持 分片攻击防范和 用户字典序攻击防范功能。
TCP Login

##### 1.1.1 TCP分片攻击

设备的包过滤功能一般是通过判断 TCP 首个分片中的五元组（源 IP 地址、源端口号、目的 IP 地址、目的端口号、传输层协议号）信息来决定后续 TCP 分片是否允许通过。RFC 1858 对 TCP 分片报文进行了规定，认为 分片报文中，首片报文中 报文长度小于 字节，或后续分片报文TCP TCP 20中分片偏移量等于 8 字节的报文为 TCP 分片攻击报文。这类报文可以成功绕过上述包过滤功能，对设备造成攻击。
为防范这类攻击，可以在设备上配置 TCP 分片攻击防范功能，对 TCP 分片攻击报文进行丢弃。

##### 1.1.2 Login用户字典序攻击

字典序攻击是指攻击者通过收集用户密码可能包含的字符，使用各种密码组合逐一尝试登录设备，以达到猜测合法用户密码的目的。
为防范这类攻击，可以在设备上配置 Login 用户延时认证功能，在用户认证失败之后，延时期间不接受此用户的登录请求。

#### 1.2 配置TCP分片攻击防范

##### 1. 功能简介

设备上开启 分片攻击防范功能后，能够对收到的 分片报文的长度以及分片偏移量进行合TCP TCP法性检测，并丢弃非法的 TCP 分片报文。

##### 2. 配置限制和指导

如果设备上开启了 TCP 分片攻击防范功能，并应用了单包攻击防范策略，则 TCP 分片攻击防范功能会先于单包攻击防范策略检测并处理入方向的 TCP 报文。

##### 3. 配置步骤

进入系统视图。
(1)
system-view开启 分片攻击防范功能。
(2) TCP attack-defense tcp fragment enable缺省情况下，TCP 分片攻击防范功能处于开启状态。

##### 2. 配置步骤

#### 1.3 配置Login用户延时认证功能

##### 1. 功能简介

用户登录失败后，若设备上配置了重新进行认证的等待时长，则系统将会延迟一定的时长之Login后再允许用户进行认证，可以有效地避免设备受到 Login 用户字典序攻击。
Login 用户延迟认证功能与 Login 用户攻击防范功能无关，只要配置了延迟认证等待时间，即可生效。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 配置 Login 用户登录失败后重新进行认证的等待时长。
attack-defense login reauthentication-delay seconds缺省情况下，Login 用户登录失败后重新进行认证不需要等待。

## 17-TCP攻击防御配置

目 录攻击防御简介

### 1 TCP攻击防御

#### 1.1 TCP攻击防御简介

攻击者可以利用 TCP 连接的建立过程对与其建立连接的设备进行攻击，为了避免攻击带来的危害，设备提供了相应的技术对攻击进行检测和防范。

#### 1.2 配置防止Naptha攻击功能

##### 1. 功能简介

Naptha 属于 DDoS（Distributed Denial of Service，分布式拒绝服务）攻击方式，主要利用操作系统 TCP/IP 栈和网络应用程序需要使用一定的资源来控制 TCP 连接的特点，在短时间内不断地建立大量的 TCP 连接，并且使其保持在某个特定的状态（CLOSING、ESTABLISHED、FIN_WAIT_1、和 五种状态中的一种），而不请求任何数据，那么被攻击设备会因消耗大FIN_WAIT_2 LAST_ACK量的系统资源而陷入瘫痪。
防止 Naptha 攻击功能通过加速 TCP 状态的老化，来降低设备遭受 Naptha 攻击的风险。开启防止Naptha 攻击功能后，设备周期性地对各状态的 TCP 连接数进行检测。当某状态的最大 TCP 连接数超过指定的最大连接数后，将加速该状态下 TCP 连接的老化。

##### 2. 配置步骤

进入系统视图。
(1)
system-view开启防止 攻击功能。
(2) Naptha tcp anti-naptha enable缺省情况下，防止 Naptha 攻击功能处于关闭状态。
(3) （可选）配置 TCP 连接的某一状态下的最大 TCP 连接数。
tcp state { closing | established | fin-wait-1 | fin-wait-2 | last-ack } connection-limit number缺省情况下，CLOSING、ESTABLISHED、 FIN_WAIT_1、 和 五FIN_WAIT_2 LAST_ACK种状态最大 TCP 连接数均为 50。
如果最大 TCP 连接数为 0，则表示不会加速该状态下 TCP 连接的老化。
(4) （可选）配置 TCP 连接状态的检测周期。
tcp check-state interval interval缺省情况下，TCP 连接状态的检测周期为 秒。
30

## 18-IP Source Guard配置

目 录简介配置 静态绑定表项配置 静态绑定表项静态绑定表项配置举例与 配合的 动态地址绑定表项配置举例

### 1 IP Source Guard

#### 1.1 IP Source Guard简介

功能用于对接口收到的报文进行过滤控制，通常配置在接入用户侧的接口上，以IP Source Guard防止非法用户报文通过，从而限制了对网络资源的非法使用（比如非法主机仿冒合法用户 IP 接入网络），提高了接口的安全性。

##### 1.1.1 IP Source Guard工作原理

如 图 所示，配置了IP Guard功能的接口接收到用户报文后，根据IP Guard绑定1-1 Source Source表项匹配报文，如果报文的信息与某绑定表项匹配，则转发该报文；若匹配失败，则丢弃该报文。
IP Source Guard可以根据报文的源IP地址、源MAC地址和VLAN标签对报文进行过滤。报文的这些特征项可单独或组合起来与接口进行绑定，形成IP Guard绑定表项。
Source IP Source Guard 的绑定功能是针对接口的，一个接口配置了绑定功能后，仅对该接口接收的报文进行限制，其它接口不受影响。
绑定表项可以通过手工配置和动态获取两种方式生成。
IP Source Guard图1-1 IP Source Guard 功能示意图

##### 1.1.2 静态配置绑定表项

静态配置绑定表项是指通过命令行手工配置绑定表项，该方式适用于局域网络中主机数较少且主机使用静态配置 地址的情况，比如在接入某重要服务器的接口上配置绑定表项，仅允许该接口接收IP与该服务器通信的报文。
静态绑定表项可以用于：
• 过滤接口收到的 IP 报文。
• 与 ARP Detection 功能配合使用检查接入用户的合法性。ARP Detection 功能的详细介绍请参见“安全配置指导”中的“ARP 攻击防御”。
• 与 ND Detection 功能配合使用检查接入用户的合法性。 ND Detection 功能的详细介绍请参见“安全配置指导”中的“ND 攻击防御”。
静态绑定表项又包括全局静态绑定表项和接口静态绑定表项两种类型，这两种绑定表项的作用范围不同。

全局静态绑定表项
•全局静态绑定表项是在系统视图下配置的绑定了 IP 地址和 MAC 地址的表项，这类表项在设备的所有端口上生效。全局静态绑定表项适用于防御主机仿冒攻击，可有效过滤攻击者通过仿冒合法用户主机的 IP 地址或者 MAC 地址向设备发送的伪造 IP 报文。
• 接口静态绑定表项端口静态绑定是在端口上配置的绑定了 IP 地址、MAC 地址、VLAN 以及相关组合的表项，这类表项仅在当前端口上生效。只有端口收到的报文的 IP 地址、MAC 地址、VLAN 与端口上配置的绑定表项的各参数完全匹配时，报文才可以在该端口被正常转发，其它报文都不能被转发，该表项适用于检查端口上接入用户的合法性。

##### 1.1.3 动态获取绑定表项

动态获取绑定表项是指通过获取其它模块生成的用户信息来生成绑定表项。动态绑定表项中可能包含的内容：MAC 地址、IP 地址/IPv6 地址、VLAN 信息、入接口信息及表项类型（DHCPv4/v6 Snooping、DHCPv4/v6 中继等）。
这种动态获取绑定表项的方式，通常适用于局域网络中主机较多的情况。以主机使用 动态获DHCP取 IP 地址的情况为例，其原理是每当局域网内的主机通过 DHCP 服务器获取到 IP 地址时，DHCP服务器会生成一条 DHCP 服务器表项，DHCP 中继会生成一条 DHCP 中继表项，DHCP Snooping会生成一条 表项。IP 可以根据以上任何一条 表项相应地增DHCP Snooping Source Guard DHCP加一条 IP Source Guard 绑定表项来判断是否允许该用户访问网络。如果某个用户私自设置 IP 地址，则不会触发设备生成相应的 DHCP 表项，IP Source Guard 也不会增加相应的绑定表项，因此该用户的报文将会被丢弃。

###### 1. IPv4动态绑定功能

在配置了 动态绑定功能的接口上，IP 通过与不同的模块配合动态生成绑定表项：
IPv4 Source Guard表1-1 IPv4 动态绑定功能信息表

|  | 接口类型 |  |  | 表项来源模块 |  |  | 用途 |  |
|---|---|---|---|---|---|---|---|---|
|  |  |  | DHCP Snooping、802.1X |  |  |  |  |  |
|  |  |  | ARP Snooping |  |  |  |  |  |
|  |  |  | DHCP中继 |  |  |  |  |  |
|  |  |  | DHCP服务器 |  |  |  |  |  |
|  |  |  | ARP泛洪抑制 |  |  |  |  |  |

功能的详细介绍请参见“安全配置指导”中的“802.1X”。ARP 功能的详细介绍
802.1X Snooping请参见“三层技术 -IP 业务配置指导”中的“ ARP ”。 ARP 泛洪抑制功能的详细介绍请参见“ VXLAN配置指导”中的“VXLAN”。DHCP Snooping 功能的详细介绍请参见“三层技术-IP 业务配置指导”中的“DHCP Snooping”。DHCP 中继功能的详细介绍请参见“三层技术-IP 业务配置指导”中的“DHCP 中继”。DHCP 服务器功能的详细介绍请参见“三层技术-IP 业务配置指导”中的“DHCP服务器”。

###### 2. IPv6动态绑定功能

在配置了 IPv6 动态绑定功能的接口上，IP Source Guard 通过与不同模块配合动态生成绑定表项：
表1-2 动态绑定功能信息表IPv6

|  | 接口类型 |  |  | 表项来源模块 |  |  | 用途 |  |
|---|---|---|---|---|---|---|---|---|
|  |  |  | DHCPv6 Snooping、ND Snooping |  |  |  |  |  |
|  |  |  | 802.1X |  |  |  |  |  |
|  |  |  | DHCPv6中继 |  |  |  |  |  |
|  |  |  | ND泛洪抑制 |  |  |  |  |  |

功能的详细介绍请参见“三层技术-IP 业务配置指导”的“DHCPv6 Snooping”。
DHCPv6 Snooping ND Snooping 功能的详细介绍请参见“三层技术-IP 业务配置指导”的“IPv6 基础”。ND 泛洪抑制功能的详细介绍请参见“VXLAN 配置指导”中的“VXLAN”。DHCPv6 中继功能的详细介绍请参见“三层技术-IP 业务配置指导”中的“DHCPv6 中继”。

#### 1.2 IP Source Guard配置任务简介

IPv4 绑定功能配置任务如下：
(1) 配置IPv4 接口绑定功能
(2) （可选）配置IPv4 静态绑定表项
(3) （可选）配置IP Source Guard免过滤条件IPv6 绑定功能配置任务如下：
(1) 配置IPv6 接口绑定功能
(2) （可选）配置IPv6 静态绑定表项

#### 1.3 配置IPv4绑定功能

##### 1.3.1 配置IPv4接口绑定功能

###### 1. 功能简介

配置了IPv4 接口绑定功能的接口，将打开根据绑定表项过滤报文的开关，并利用配置的IPv4 静态绑定表项和从其它模块获取的IPv4 动态绑定表项对接口转发的报文进行过滤或者配合其它模块提供相关的安全服务。IPv4静态绑定表项中指定的信息均用于IP Source Guard过滤接口收到的报文，具体配置请参考“1.3.2 配置IPv4 静态绑定表项”。
IP Source Guard 依据该表项中的哪些信息过滤接口收到的报文，由 IPv4 接口绑定配置决定：
• 若接口上配置动态绑定功能时绑定了源 IP 地址和 MAC 地址，则只有接口上收到的报文的源地址和源 地址都与某动态绑定表项匹配，该报文才能被正常转发，否则将被丢弃；
IPv4 MAC若接口上配置动态绑定功能时仅绑定了源 IP 地址，则只有该接口收到的报文的源 IPv4 地址与
•某动态绑定表项匹配，该报文才会被正常转发，否则将被丢弃；

若接口上配置动态绑定功能时仅绑定了源 MAC 地址，则只有该接口收到的报文的源 MAC 地
•址与某动态绑定表项匹配，该报文才会被正常转发，否则将被丢弃。

###### 2. 配置限制和指导

要实现 IPv4 动态绑定功能，请保证网络中的 802.1X、ARP Snooping 、DHCP Snooping、DHCP中继或 DHCP 服务器配置有效且工作正常。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
可支持二层以太网端口/三层以太网接口/三层以太网子接口/三层聚合接口/三层聚合子接口
接口。
/VLAN
开启 接口绑定功能。
(3) IPv4
ip verify source { ip-address | ip-address mac-address | mac-address }
缺省情况下，接口的 IPv4 接口绑定功能处于关闭状态。

##### 1.3.2 配置IPv4静态绑定表项

###### 1. 功能简介

静态绑定表项包括全局的 静态绑定表项和接口的 静态绑定表项。接口的 静态IPv4 IPv4 IPv4 IPv4绑定表项和动态绑定表项的优先级高于全局的 IPv4 静态绑定表项，即接口优先使用本接口上的静态或动态绑定表项对收到的报文进行匹配，若匹配失败，再与全局的静态绑定表项进行匹配。

###### 2. 配置限制和指导

全局的 IPv4 静态绑定表项中定义了接口允许转发的报文的 IP 地址和 MAC 地址，对设备的所有接口都生效。
在与 功能配合时，绑定表项中必须指定 IP、MAC 和 参数，且该 为使ARP Detection VLAN VLAN能 ARP Detection 功能的 VLAN，否则 ARP 报文将无法通过接口的 IPv4 静态绑定表项的检查。

###### 3. 配置全局的IPv4静态绑定表项

(1) 进入系统视图。
system-view
(2) 配置全局的 IPv4 静态绑定表项。
ip source binding ip-address ip-address mac-address mac-address

###### 4. 配置接口的IPv4静态绑定表项

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
可支持二层以太网端口/三层以太网接口/三层以太网子接口/三层聚合接口/三层聚合子接口
/VLAN 接口。

##### 1.3.3 配置IP Source Guard免过滤条件

(3) 配置接口的 IPv4 静态绑定表项。
ip source binding { ip-address ip-address | ip-address ip-address
mac-address mac-address | mac-address mac-address } [ vlan vlan-id ]
同一个表项不能在同一个接口上重复绑定，但可以在不同的接口上绑定。
配置IP Guard免过滤条件
1.3.3 Source

###### 1. 功能简介

缺省情况下，在接口上配置了 绑定功能后，接口上会丢弃所有无绑定表项的 报文。为避IPv4 IPv4免特定用户的报文由于没有匹配的绑定表项而被丢弃，可配置 IP Source Guard 免过滤条件，允许接口直接放行匹配上免过滤条件的 IPv4 报文。

###### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 配置 IP Source Guard 免过滤条件。
ip verify source exclude vlan start-vlan-id [ to end-vlan-id ]缺省情况下，未配置免过滤条件。
可以通过多次执行本命令，配置多个 IP Source Guard 免过滤 VLAN，但不同命令中的 VLAN范围不能重叠。

#### 1.4 配置IPv6绑定功能

##### 1.4.1 配置IPv6接口绑定功能

###### 1. 功能简介

配置了IPv6 接口绑定功能的接口，将打开根据绑定表项过滤报文的开关，并利用配置的IPv6 静态绑定表项和从其他模块获取的IPv6 动态绑定表项对接口转发的报文进行过滤。IPv6 静态绑定表项中指定的信息均用于IP Guard过滤接口收到的报文，具体配置请参考“1.4.2 配置IPv6 静Source态绑定表项”。
IP Source Guard 依据该表项中的哪些信息过滤接口收到的报文，由 IPv6 接口绑定配置决定：
• 若接口上配置动态绑定功能时绑定了源 IP 地址和 MAC 地址，则只有接口上收到的报文的源IPv6 地址和源 MAC 地址都与某动态绑定表项匹配，该报文才能被正常转发，否则将被丢弃；
• 若接口上配置动态绑定功能时仅绑定了源 IP 地址，则只有该接口收到的报文的源 IPv6 地址与某动态绑定表项匹配，该报文才会被正常转发，否则将被丢弃；
若接口上配置动态绑定功能时仅绑定了源 MAC 地址，则只有该接口收到的报文的源 MAC 地
•址与某动态绑定表项匹配，该报文才会被正常转发，否则将被丢弃。

###### 2. 配置限制和指导

要实现 IPv6 动态绑定功能，请保证网络中的 DHCPv6 Snooping、DHCPv6 Relay 或 ND Snooping配置有效且工作正常。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
可支持二层以太网端口/三层以太网接口/三层以太网子接口/三层聚合接口/三层聚合子接口
/VLAN 接口。
(3) 配置 IPv6 接口绑定功能。
ipv6 verify source { ip-address | ip-address mac-address | mac-address }
缺省情况下，接口的 IPv6 接口绑定功能处于关闭状态。

##### 1.4.2 配置IPv6静态绑定表项

###### 1. 功能简介

IPv6 静态绑定功能包括全局的 IPv6 静态绑定功能和接口的 IPv6 静态绑定功能。接口的 IPv6 静态绑定表项和 IPv6 动态绑定表项的优先级高于全局的 IPv6 静态绑定表项，即接口优先使用本接口上的 静态或动态绑定表项对收到的报文进行匹配，若匹配失败，再与全局的 静态绑定表项IPv6 IPv6进行匹配。

###### 2. 配置限制和指导

全局的 IPv6 静态绑定表项中定义了接口允许转发的报文的 IPv6 地址和 MAC 地址，对设备的所有接口都生效。
在与 ND Detection 功能配合时，绑定表项中必须指定 VLAN 参数，且该 VLAN 为使能 ND Detection功能的 VLAN，否则 报文将无法通过接口的 静态绑定表项的检查。
ND IPv6

###### 3. 配置全局的IPv6静态绑定表项

(1) 进入系统视图。
system-view
(2) 配置全局的 IPv6 静态绑定表项。
ipv6 source binding ip-address ipv6-address mac-address mac-address

###### 4. 配置接口的IPv6静态绑定表项

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
可支持二层以太网端口/三层以太网接口/三层以太网子接口/三层聚合接口/三层聚合子接口
/VLAN 接口。
(3) 配置接口的 IPv6 静态绑定表项。
ipv6 source binding { ip-address ipv6-address | ip-address ipv6-address
mac-address mac-address | mac-address mac-address } [ vlan vlan-id ]
同一个表项不能在同一个接口上重复绑定，但可以在不同接口上绑定。

#### 1.5 IP Source Guard显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 IP Source Guard 的运行情况，通过查看显示信息验证配置的效果。
表1-3 IP Source Guard 显示和维护操作 命令display ip source binding [ static | [ vpn-instance vpn-instance-name ] [ arp-snooping | arp-suppression | dhcp-relay | dhcp-server | dhcp-snooping | dot1x ] ]显示IPv4绑定表项信息[ ip-address ip-address ] [ mac-address mac-address ] [ vlan vlan-id ] [ interface interface-type interface-number ] [ slot slot-number ]显示IP Source Guard免过 display ip verify source excluded [ vlan start-vlan-id [ to滤条件生效情况 end-vlan-id ] ] [ slot slot-number ] display ipv6 source binding static vpn-instance [ | [ vpn-instance-name ] [ dhcpv6-relay | dhcpv6-snooping | dot1x |显示IPv6地址绑定表项信息 nd-snooping | nd-suppression ] ] [ ip-address ipv6-address ] [ mac-address mac-address ] [ vlan vlan-id ] [ interface interface-type interface-number ] [ slot slot-number ] display ipv6 source binding pd [ vpn-instance vpn-instance-name ] [ prefix prefix/prefix-length ]显示IPv6前缀绑定表项信息[ mac-address mac-address ] [ vlan vlan-id ] [ interface slot interface-type interface-number ] [ slot-number ]

#### 1.6 IP Source Guard典型配置举例

##### 1.6.1 IPv4静态绑定表项配置举例

###### 1. 组网需求

如 图 所 示 ，Host 、 分 别 与Device 的 接 口Ten-GigabitEthernet1/0/2 、1-2 A Host B A Ten-GigabitEthernet1/0/1 相连。各主机均使用静态配置的IP地址。
要求通过在 Device A 上配置 IPv4 静态绑定表项，满足以下各项应用需求：
• Device A 上的所有接口都允许 Host A 发送的 IP 报文通过。
• Device A 的接口 Ten-GigabitEthernet1/0/1 上允许 Host B 发送的 IP 报文通过。

###### 2. 组网图

图1-2 配置静态表项组网图

###### 3. 配置步骤

\# 配置 Device A 各接口的 IP 地址（略）。
\# 在接口 Ten-GigabitEthernet1/0/2 上开启 IPv4 接口绑定功能，绑定源 IP 地址和 MAC 地址。
<DeviceA> system-view [DeviceA] interface ten-gigabitethernet 1/0/2 [DeviceA-Ten-GigabitEthernet1/0/2] ip verify source ip-address mac-address [DeviceA-Ten-GigabitEthernet1/0/2] quit配置 静态绑定表项，在 上的所有接口都允许 地址为 0001-0203-0406、IP 地\# IPv4 Device A MAC址为 192.168.0.1 的数据终端 Host A 发送的 IP 报文通过。
[DeviceA] ip source binding ip-address 192.168.0.1 mac-address 0001-0203-0406在接口 上开启 接口绑定功能，绑定源 地址和 地址。
\# Ten-GigabitEthernet1/0/1 IPv4 IP MAC [DeviceA] interface ten-gigabitethernet 1/0/1 [DeviceA-Ten-GigabitEthernet1/0/1] ip verify source ip-address mac-address \# 配置 IPv4 静态绑定表项，在 Device A 的 Ten-GigabitEthernet1/0/1 上允许 MAC 地址为0001-0203-0407 的数据终端 Host B 发送的 IP 报文通过。
[DeviceA-Ten-GigabitEthernet1/0/1] ip source binding mac-address 0001-0203-0407 [DeviceA-Ten-GigabitEthernet1/0/1] quit

###### 4. 验证配置

在 上显示 静态绑定表项，可以看出以上配置成功。
\# Device A IPv4 <DeviceA> display ip source binding static Total entries found: 2 IP Address MAC Address Interface VLAN Type
192.168.0.1 0001-0203-0406 N/A N/A Static N/A 0001-0203-0407 XGE1/0/1 N/A Static

##### 1.6.2 与DHCP Snooping配合的IPv4动态绑定功能配置举例

###### 1. 组网需求

DHCP 客户端通过 Device 的接口 Ten-GigabitEthernet1/0/1 接入网络，通过 DHCP 服务器获取 IPv4地址。
具体应用需求如下：
• Device 上使能 DHCP Snooping 功能，保证客户端从合法的服务器获取 IP 地址，且记录客户端 地址及 地址的绑定关系。
IPv4 MAC在接口Ten-GigabitEthernet1/0/1上启用IPv4动态绑定功能，利用动态生成的DHCP
• Snooping表项过滤接口接收的报文，只允许通过 DHCP 服务器动态获取 IP 地址的客户端接入网络。
DHCP 服务器的具体配置请参见“三层技术-IP 业务配置指导”中的“DHCP 服务器”。

###### 4. 验证配置

###### 2. 组网图

图1-3 配置与 DHCP Snooping 配合的 IPv4 动态绑定功能组网图

###### 3. 配置步骤

(1) 配置 DHCP Snooping
\# 配置各接口的 IP 地址（略）。
\# 开启 DHCP Snooping 功能。
<Device> system-view
[Device] dhcp snooping enable
\# 设置与 DHCP 服务器相连的接口 Ten-GigabitEthernet1/0/2 为信任接口。
[Device] interface ten-gigabitethernet 1/0/2
[Device-Ten-GigabitEthernet1/0/2] dhcp snooping trust
[Device-Ten-GigabitEthernet1/0/2] quit
(2) 配置 IPv4 接口绑定功能
\# 开启接口 Ten-GigabitEthernet1/0/1 的 IPv4 接口绑定功能，绑定源 IP 地址和 MAC 地址，
并启用接口的 DHCP Snooping 表项记录功能。
[Device] interface ten-gigabitethernet 1/0/1
[Device-Ten-GigabitEthernet1/0/1] ip verify source ip-address mac-address
[Device-Ten-GigabitEthernet1/0/1] dhcp snooping binding record
[Device-Ten-GigabitEthernet1/0/1] quit
验证配置
4.
\# 显示接口 Ten-GigabitEthernet1/0/1 从 DHCP Snooping 获取的动态表项。
[Device] display ip source binding dhcp-snooping
Total entries found: 1
IP Address MAC Address Interface VLAN Type
192.168.0.1 0001-0203-0406 XGE1/0/1 1 DHCP snooping
接口 Ten-GigabitEthernet1/0/1 在配置 IPv4 接口绑定功能之后，会根据该表项进行报文过滤。

##### 1.6.3 与DHCP中继配合的IPv4动态绑定功能配置举例

###### 1. 组网需求

Switch 通过接口 Vlan-interface100 和 Vlan-interface200 分别与客户端 Host 和 DHCP 服务器相连。
Switch 上使能 DHCP 中继功能。
具体应用需求如下：
• Host 通过 DHCP 中继从 DHCP 服务器上获取 IP 地址。
• 在接口 Vlan-interface100 上启用 IPv4 动态绑定功能，利用 Switch 上生成的 DHCP 中继表项，过滤接口接收的报文。

###### 1. 组网需求

###### 2. 组网图

图1-4 配置动态绑定功能组网图

###### 3. 配置步骤

(1) 配置 IPv4 动态绑定功能
\# 配置各接口的 IP 地址（略）。
\# 在接口 Vlan-interface100 上开启 IPv4 接口绑定功能，绑定源 IP 地址和 MAC 地址。
<Switch> system-view
[Switch] interface vlan-interface 100
[Switch-Vlan-interface100] ip verify source ip-address mac-address
[Switch-Vlan-interface100] quit
配置 中继
(2) DHCP
\# 开启 DHCP 服务。
[Switch] dhcp enable
\# 开启 DHCP 中继用户地址表项记录功能。
[Switch] dhcp relay client-information record
配置接口 工作在 中继模式。
\# Vlan-interface100 DHCP
[Switch] interface vlan-interface 100
[Switch-Vlan-interface100] dhcp select relay
\# 指定 DHCP 服务器的地址。
[Switch-Vlan-interface100] dhcp relay server-address 10.1.1.1
[Switch-Vlan-interface100] quit

###### 4. 验证配置

显示生成的 动态绑定表项信息。
\# IPv4 [Switch] display ip source binding dhcp-relay Total entries found: 1 IP Address MAC Address Interface VLAN Type
192.168.0.1 0001-0203-0406 Vlan100 100 DHCP relay

##### 1.6.4 IPv6静态绑定表项配置举例

组网需求
1.
IPv6 客户端通过 Device 的接口 Ten-GigabitEthernet1/0/1 接入网络。要求在 Device 上配置 IPv6静态绑定表项，使得接口 上只允许 （ 地址为 、Ten-GigabitEthernet1/0/1 Host MAC 0001-0202-0202 IPv6 地址为 2001::1）发送的 IPv6 报文通过。

###### 1. 组网需求

###### 2. 组网图

图1-5 配置 IPv6 静态绑定表项组网图

###### 3. 配置步骤

在接口 上开启 接口绑定功能，绑定源 地址和 地址。
\# Ten-GigabitEthernet1/0/1 IPv6 IP MAC <Device> system-view [Device] interface ten-gigabitethernet 1/0/1 [Device-Ten-GigabitEthernet1/0/1] ipv6 verify source ip-address mac-address在接口 上配置 静态绑定表项，绑定源 地址和 地址，只允\# Ten-GigabitEthernet1/0/1 IPv6 IP MAC许 IPv6 地址为 2001::1 且 MAC 地址为 00-01-02-02-02-02 的 IPv6 报文通过。
[Device-Ten-GigabitEthernet1/0/1] ipv6 source binding ip-address 2001::1 mac-address 0001-0202-0202 [Device-Ten-GigabitEthernet1/0/1] quit

###### 4. 验证配置

在 上显示 静态绑定表项，可以看出以上配置成功。
\# Device IPv6 [Device] display ipv6 source binding static Total entries found: 1 IPv6 Address MAC Address Interface VLAN Type 2001::1 0001-0202-0202 XGE1/0/1 N/A Static

##### 1.6.5 与DHCPv6 Snooping配合的IPv6动态地址绑定表项配置举例

组网需求
1.
DHCPv6 客户端通过 Device 的接口 Ten-GigabitEthernet1/0/1 接入网络，通过 DHCPv6 服务器获取 地址。
IPv6具体应用需求如下：
Device 上使能 DHCPv6 Snooping 功能，保证客户端从合法的服务器获取 IP 地址，且记录客
•户端 地址及 地址的绑定关系。
IPv6 MAC在接口 上启用 动态绑定功能，利用动态生成的
• Ten-GigabitEthernet1/0/1 IPv6 DHCPv6 Snooping 表项过滤接口接收的报文，只允许通过 DHCPv6 服务器动态获取 IP 地址的客户端接入网络。

###### 2. 组网图

图1-6 配置与 DHCPv6 Snooping 配合的 IPv6 动态地址绑定功能组网图

###### 3. 配置步骤

配置
(1) DHCPv6 Snooping全局使能 功能。
\# DHCPv6 Snooping <Device> system-view [Device] ipv6 dhcp snooping enable \# 配置接口 Ten-GigabitEthernet1/0/2 为信任接口。
[Device] interface ten-gigabitethernet 1/0/2 [Device-Ten-GigabitEthernet1/0/2] ipv6 dhcp snooping trust [Device-Ten-GigabitEthernet1/0/2] quit
(2) 配置 IPv6 接口绑定功能\# 开启接口 Ten-GigabitEthernet1/0/1 的 IPv6 接口绑定功能，绑定源 IP 地址和 MAC 地址，并启用接口的 DHCPv6 Snooping 地址表项记录功能。
[Device] interface ten-gigabitethernet 1/0/1 [Device-Ten-GigabitEthernet1/0/1] ipv6 verify source ip-address mac-address [Device-Ten-GigabitEthernet1/0/1] ipv6 dhcp snooping binding record [Device-Ten-GigabitEthernet1/0/1] quit

###### 4. 验证配置

\# 客户端通过 DHCPv6 server 成功获取 IP 地址之后，通过执行以下命令可查看到已生成的 IPv6 动态地址绑定表项信息。
[Device] display ipv6 source binding dhcpv6-snooping Total entries found: 1 IPv6 Address MAC Address Interface VLAN Type 2001::1 040a-0000-0001 XGE1/0/1 1 DHCPv6 snooping接口 Ten-GigabitEthernet1/0/1 在配置 IPv6 接口绑定功能之后，会根据该表项进行报文过滤。

##### 1.6.6 与DHCPv6 Snooping配合的IPv6动态前缀绑定表项配置举例

###### 1. 组网需求

DHCPv6 客户端通过 Device 的接口 Ten-GigabitEthernet1/0/1 接入网络，通过 DHCPv6 服务器获取 IPv6 前缀。
具体应用需求如下：
• Device 上开启了 DHCPv6 Snooping 功能，保证 DHCPv6 客户端从合法的服务器获取前缀，且记录对应的 DHCPv6 Snooping 前缀表项。

###### 2. 组网图

在接口 Ten-GigabitEthernet1/0/1 上启用 IPv6 动态绑定功能，利用动态生成的 DHCPv6
•前缀表项过滤接口接收的报文，只允许通过 服务器动态获取前缀生成Snooping DHCPv6 IPv6 地址的客户端接入网络。
组网图
2.
图1-7 配置与 DHCPv6 Snooping 配合的 IPv6 动态前缀绑定功能组网图

###### 3. 配置步骤

(1) 配置 DHCPv6 Snooping
\# 开启 DHCPv6 Snooping 功能。
<Device> system-view
[Device] ipv6 dhcp snooping enable
\# 配置接口 Ten-GigabitEthernet1/0/2 为 DHCPv6 Snooping 信任接口。
[Device] interface ten-gigabitethernet 1/0/2
[Device-Ten-GigabitEthernet1/0/2] ipv6 dhcp snooping trust
[Device-Ten-GigabitEthernet1/0/2] quit
\# 在接口 Ten-GigabitEthernet1/0/1 开启 DHCPv6 Snooping 前缀表项记录功能。
[Device] interface ten-gigabitethernet 1/0/1
[Device-Ten-GigabitEthernet1/0/1] ipv6 dhcp snooping pd binding record
(2) 配置 IPv6 接口绑定功能
\# 开启接口 Ten-GigabitEthernet1/0/1 的 IPv6 接口绑定功能。
[Device-Ten-GigabitEthernet1/0/1] ipv6 verify source ip-address mac-address
[Device-Ten-GigabitEthernet1/0/1] quit

###### 4. 验证配置

\# DHCPv6 客户端通过 DHCPv6 服务器成功获取前缀信息之后，可通过执行以下命令可查看到设备上生成的 DHCPv6 前缀表项信息。
[Device] display ipv6 source binding pd Total entries found: 1 IPv6 prefix MAC address Interface VLAN 2001:410:1::/48 0010-9400-0004 GE1/0/1 1接口 Ten-GigabitEthernet1/0/1 在配置 IPv6 接口绑定功能之后，会根据该表项进行报文过滤。

##### 1.6.7 与DHCPv6中继配合的IPv6动态绑定功能配置举例

###### 1. 组网需求

Switch 通过接口 Vlan-interface3 和 Vlan-interface2 分别与客户端和 DHCPv6 服务器相连。通过在Switch 上使能 DHCPv6 中继功能，实现如下需求：
• 客户端通过 DHCPv6 中继从 DHCPv6 服务器上获取 IPv6 地址。

###### 3. 配置步骤

###### 4. 验证配置

在接口 Vlan-interface3 上启用 IPv6 动态绑定功能，利用 Switch 上生成的 DHCPv6 中继表项，
•过滤接口接收的报文。

###### 2. 组网图

图1-8 配置与 DHCPv6 中继配合的 IPv6 动态绑定功能组网图配置步骤
3.
(1) 配置 DHCPv6 中继\# 创建 VLAN、将接口加入到 VLAN，并配置 VLAN 接口的 IPv6 地址（略）。
\# 配置接口 Vlan-interface3 工作在 DHCPv6 中继模式。
[Switch] interface vlan-interface 3 [Switch-Vlan-interface3] ipv6 dhcp select relay开启 中继用户地址表项记录功能。
\# DHCPv6 [Switch-Vlan-interface3] ipv6 dhcp relay client-information record \# 指定 DHCPv6 服务器的地址。
[Switch-Vlan-interface3] ipv6 dhcp relay server-address 2::2 [Switch-Vlan-interface3] quit
(2) 配置 IPv6 动态绑定功能\# 在接口 Vlan-interface3 上开启 IPv6 接口绑定功能，绑定源 IP 地址和 MAC 地址。
<Switch> system-view [Switch] interface vlan-interface 3 [Switch-Vlan-interface3] ipv6 verify source ip-address mac-address [Switch-Vlan-interface3] quit验证配置
4.
\# 显示生成的 IPv6 动态绑定表项信息。
[Switch] display ipv6 source binding dhcpv6-relay Total entries found: 1 IP Address MAC Address Interface VLAN Type 1::2 0001-0203-0406 Vlan3 3 DHCPv6 relay

## 19-ARP攻击防御配置

目 录攻击防御简介防止 报文攻击典型配置举例配置限制和指导源 地址固定的 攻击检测功能典型配置举例配置 主动确认功能配置步骤功能简介报文强制转发

Detection显示和维护配置 自动扫描、固化功能配置限制和指导功能简介配置步骤

### 1 ARP攻击防御

#### 1.1 ARP攻击防御简介

设备提供了多种 ARP 攻击防御技术对局域网中的 ARP 攻击和 ARP 病毒进行防范、检测和解决。
常见的 ARP 攻击方式包括：
攻击者通过向设备发送大量目标 IP 地址不能解析的 IP 报文，使得设备试图反复地对目标 IP
•地址进行解析，导致 负荷过重及网络流量过大。
CPU攻击者向设备发送大量 报文，对设备的 形成冲击。
• ARP CPU攻击者可以仿冒用户、仿冒网关发送伪造的 报文，使网关或主机的 表项不正确，
• ARP ARP从而对网络进行攻击。

#### 1.2 ARP攻击防御配置任务简介

如下所有配置均为可选，请根据实际情况选择配置。
防止泛洪攻击
•配置ARP防止IP报文攻击功能(cid:123)
配置ARP报文限速功能(cid:123)
配置源MAC地址固定的ARP攻击检测功能(cid:123)
• 防止仿冒用户、仿冒网关攻击配置ARP报文源MAC地址一致性检查功能(cid:123)
配置ARP主动确认功能(cid:123)
配置授权ARP功能(cid:123)
配置ARP Detection功能(cid:123)
配置ARP自动扫描、固化功能(cid:123)
配置ARP网关保护功能(cid:123)
配置ARP过滤保护功能(cid:123)
配置 ARP 报文发送端 IP 地址检查功能(cid:123)

#### 1.3 配置ARP防止IP报文攻击功能

##### 1.3.1 功能简介

如果网络中有主机通过向设备发送大量目标 IP 地址不能解析的 IP 报文来攻击设备，则会造成下面的危害：
• 设备向目的网段发送大量 ARP 请求报文，加重目的网段的负载。
• 设备会试图反复地对目标 IP 地址进行解析，增加了 CPU 的负担。
为避免这种 IP 报文攻击所带来的危害，设备提供了下列两个功能：
• ARP 源抑制功能：如果发送攻击报文的源是固定的，可以采用 ARP 源抑制功能。开启该功能后，如果网络中每 5 秒内从某 IP 地址向设备某接口发送目的 IP 地址不能解析的 IP 报文超过

了设置的阈值，则设备将不再处理由此 IP 地址发出的 IP 报文直至该 5 秒结束，从而避免了恶意攻击所造成的危害。
黑洞路由功能：无论发送攻击报文的源是否固定，都可以采用 黑洞路由功能。开启
• ARP ARP该功能后，一旦接收到目标 IP 地址不能解析的 IP 报文，设备立即产生一个黑洞路由，并同时发起 ARP 主动探测，如果在黑洞路由老化时间内 ARP 解析成功，则设备马上删除此黑洞路由并开始转发去往该地址的报文，否则设备直接丢弃该报文。在删除黑洞路由之前，后续去往该地址的 IP 报文都将被直接丢弃。用户可以通过命令配置 ARP 请求报文的发送次数和发送时间间隔。等待黑洞路由老化时间过后，如有报文触发则再次发起解析，如果解析成功则进行转发，否则仍然产生一个黑洞路由将去往该地址的报文丢弃。这种方式能够有效地防止 IP报文的攻击，减轻 的负担。
CPU

##### 1.3.2 配置ARP源抑制功能

(1) 进入系统视图。
system-view
(2) 开启 ARP 源抑制功能。
arp source-suppression enable
缺省情况下，ARP 源抑制功能处于关闭状态。
(3) 配置 ARP 源抑制的阈值。
arp source-suppression limit limit-value
缺省情况下，ARP 源抑制的阈值为 10。

##### 1.3.3 配置ARP黑洞路由功能

###### 1. 配置限制和指导

当用户配置的 ARP 主动探测总时长（发送次数×发送时间间隔）大于黑洞路由老化时间时，系统只会取小于等于该老化时间的最大值作为真正的探测总时长。
当发起 ARP 主动探测过程结束且生成的黑洞路由还未老化时，设备无法主动对黑洞路由对应的设备进行 ARP 解析，为了缓解该问题，用户可以配置较大的发送 ARP 请求报文次数。

###### 2. 配置步骤

进入系统视图。
(1)
system-view开启 黑洞路由功能。
(2) ARP arp resolving-route enable缺省情况下，ARP 黑洞路由功能处于开启状态。
(3) （可选）配置发送 ARP 请求报文的次数。
arp resolving-route probe-count count缺省情况下，发送 ARP 请求报文的次数为 3 次。
(4) （可选）配置发送 ARP 请求报文的时间间隔。
arp resolving-route probe-interval interval缺省情况下，发送 ARP 请求报文的时间间隔为 1 秒。

###### 2. 组网图

###### 3. 配置步骤

##### 1.3.4 ARP防止IP报文攻击显示和维护

在完成上述配置后，在任意视图下执行 命令可以显示配置后 源抑制的运行情况，通display ARP过查看显示信息验证配置的效果。
表1-1 防止 报文攻击显示和维护ARP IP操作 命令显示ARP源抑制的配置信息 display arp source-suppression

##### 1.3.5 ARP防止IP报文攻击典型配置举例

###### 1. 组网需求

某局域网内存在两个区域：研发区和办公区，分别属于VLAN 和VLAN 20，通过接入交换机连接10到网关Device，如 图 1-1 所示。
网络管理员在监控网络时发现办公区存在大量 ARP 请求报文，通过分析认为存在 IP 泛洪攻击，为避免这种 IP 报文攻击所带来的危害，可采用 ARP 源抑制功能和 ARP 黑洞路由功能。
组网图
2.
图1-1 ARP 防止 IP 报文攻击配置组网图配置步骤
3.
• 如果发送攻击报文的源地址是固定的，需要配置 ARP 源抑制功能\# 开启 ARP 源抑制功能，并配置 ARP 源抑制的阈值为 100。即当每 5 秒内的 ARP 请求报文的流量超过 后，对于由此 地址发出的 报文，设备不允许其触发 请求，直至100 IP IP ARP 5秒后再处理。

<Device> system-view [Device] arp source-suppression enable [Device] arp source-suppression limit 100如果发送攻击报文的源地址是不固定的，需要配置 ARP 黑洞路由功能
•\# 开启 ARP 黑洞路由功能。
[Device] arp resolving-route enable

#### 1.4 配置ARP报文限速功能

##### 1. 功能简介

ARP 报文限速功能是指对上送 CPU 的 ARP 报文进行限速，可以防止大量 ARP 报文对 CPU 进行冲击。例如，在配置了 功能后，设备会将收到的 报文重定向到 进行检查，ARP Detection ARP CPU这样引入了新的问题：如果攻击者恶意构造大量 ARP 报文发往设备，会导致设备的 CPU 负担过重，从而造成其他功能无法正常运行甚至设备瘫痪，这个时候可以配置 ARP 报文限速功能来控制接口收到 报文的速率。
ARP设备上配置 报文限速功能后，当接口上单位时间收到的 报文数量超过用户设定的限速值，ARP ARP设备处理方式如下：
• 当开启了 ARP 模块的告警功能后，设备将这个时间间隔内的超速峰值作为告警信息发送出去，生成的告警信息将发送到设备的 SNMP 模块，通过设置 SNMP 中告警信息的发送参数，来决定告警信息输出的相关特性。有关告警信息的详细介绍请参见“网络管理和监控命令参考”中的 SNMP；
当开启了 限速日志功能后，设备将这个时间间隔内的超速峰值作为日志的速率值发送到
• ARP设备的信息中心，通过设置信息中心的参数，最终决定日志报文的输出规则（即是否允许输出以及输出方向）。有关信息中心参数的配置请参见“网络管理和监控配置指导”中的“信息中心”。

##### 2. 配置限制和指导

建议用户在配置了 Detection、ARP Snooping、MFF，或者发现有 ARP泛洪攻击的情况
• ARP下，配置 ARP 报文限速功能。
• 为防止过多的告警和日志信息干扰用户工作，用户可以设定较大的信息发送时间间隔。当用户设定的时间间隔超时时，设备执行发送告警或日志的操作。
• 如果开启了 ARP 报文限速的告警和日志功能，并在二层聚合接口上开启了 ARP 报文限速功能，则只要聚合成员接口上的 ARP 报文速率超过用户设定的限速值，就会发送告警和日志信息。

##### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) （可选）开启 ARP 模块的告警功能。
snmp-agent trap enable arp [ rate-limit ]
缺省情况下，ARP 模块的告警功能处于关闭状态。
（可选）开启 报文限速日志功能。
(3) ARP
arp rate-limit log enable

缺省情况下，设备的 ARP 报文限速日志功能处于关闭状态。
(4) （可选）配置当设备收到的 ARP 报文速率超过用户设定的限速值时，设备发送告警或日志的时间间隔。
arp rate-limit log interval interval缺省情况下，当设备收到的 报文速率超过用户设定的限速值时，设备发送告警或日志的ARP时间间隔为 60 秒。
(5) 进入接口视图。
interface interface-type interface-number支持的接口类型包括二层以太网接口、二层聚合接口视图、三层以太网接口和三层聚合接口视图。
(6) 开启 ARP 报文限速功能，并指定 ARP 报文限速速率。
arp rate-limit [ pps ]缺省情况下，ARP 报文限速功能处于开启状态。

#### 1.5 配置源MAC地址固定的ARP攻击检测功能

##### 1.5.1 功能简介

本特性根据 ARP 报文的源 MAC 地址对上送 CPU 的 ARP 报文进行统计，在 5 秒内，如果收到同一源 MAC 地址（源 MAC 地址固定）的 ARP 报文超过一定的阈值，则认为存在攻击，系统会将此MAC 地址添加到攻击检测表项中。当开启了 ARP 日志信息功能（配置 arp check log enable命令），且在该攻击检测表项老化之前，如果设置的检查模式为过滤模式，则会打印日志信息并且将该源 MAC 地址发送的 ARP 报文过滤掉；如果设置的检查模式为监控模式，则只打印日志信息，不会将该源 MAC 地址发送的 ARP 报文过滤掉。
对于已添加到源 MAC 地址固定的 ARP 攻击检测表项中的 MAC 地址，在等待设置的老化时间后，会重新恢复成普通 MAC 地址。
关于 ARP 日志信息功能的详细描述，请参见“三层技术-IP 业务配置指导”中的“ARP”。

##### 1.5.2 配置限制和指导

切换源 MAC 地址固定的 ARP 攻击检查模式时，如果从监控模式切换到过滤模式，过滤模式马上生效；如果从过滤模式切换到监控模式，已生成的攻击检测表项，到表项老化前还会继续按照过滤模式处理。
对于网关或一些重要的服务器，可能会发送大量 ARP 报文，为了使这些 ARP 报文不被过滤掉，可以将这类设备的MAC地址配置成保护MAC地址，这样，即使该设备存在攻击也不会被检测或过滤。

##### 1.5.3 配置步骤

(1) 进入系统视图。
system-view
(2) 开启源 MAC 地址固定的 ARP 攻击检测功能，并选择检查模式。
arp source-mac { filter | monitor }

###### 1. 组网需求

缺省情况下，源 MAC 地址固定的 ARP 攻击检测功能处于关闭状态。
(3) 配置源 MAC 地址固定的 ARP 报文攻击检测的阈值。
arp source-mac threshold threshold-value缺省情况下，源 MAC 地址固定的 ARP 报文攻击检测的阈值为 30。
(4) 配置源 MAC 地址固定的 ARP 攻击检测表项的老化时间。
arp source-mac aging-time time缺省情况下，源 MAC 地址固定的 ARP 攻击检测表项的老化时间为 300 秒，即 5 分钟。
(5) （可选）配置保护 MAC 地址。
arp source-mac exclude-mac mac-address&<1-10>缺省情况下，未配置任何保护 MAC 地址。

##### 1.5.4 源MAC地址固定的ARP攻击检测显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后源 MAC 地址固定的 ARP 攻击检测的运行情况，通过查看显示信息验证配置的效果。
表1-2 源 MAC 地址固定的 ARP 攻击检测显示和维护操作 命令显示检测到的源MAC地址固定的ARP攻 display arp source-mac { interface interface-type击检测表项 interface-number | slot slot-number }

##### 1.5.5 源MAC地址固定的ARP攻击检测功能典型配置举例

组网需求
1.
某局域网内客户端通过网关与外部网络通信，网络环境如 图 1-2 所示。
网络管理员希望能够防止因恶意用户对网关 Device 发送大量 ARP 报文，造成设备 Device 瘫痪，并导致其它用户无法正常地访问外部网络；同时，Device 对于正常的大量 ARP 报文仍然会进行处理。

###### 2. 组网图

图1-2 源 MAC 地址固定的 ARP 攻击检测功能配置组网图

###### 3. 配置步骤

\# 开启源 MAC 固定 ARP 攻击检测功能，并选择过滤模式。
<Device> system-view [Device] arp source-mac filter \# 配置源 MAC 固定 ARP 报文攻击检测阈值为 30 个。
[Device] arp source-mac threshold 30 \# 配置源 MAC 地址固定的 ARP 攻击检测表项的老化时间为 60 秒。
[Device] arp source-mac aging-time 60配置源 固定攻击检查的保护 地址为 0012-3f86-e94c。
\# MAC MAC [Device] arp source-mac exclude-mac 0012-3f86-e94c

#### 1.6 配置ARP报文源MAC地址一致性检查功能

##### 1.6.1 功能简介

ARP 报文源 MAC 地址一致性检查功能主要应用于网关设备上，防御以太网数据帧首部中的源 MAC地址和 报文中的源 地址不同的 攻击。
ARP MAC ARP配置本特性后，网关设备在进行 ARP 学习前将对 ARP 报文进行检查。如果以太网数据帧首部中的源 MAC 地址和 ARP 报文中的源 MAC 地址不同，则认为是攻击报文，将其丢弃；否则，继续进行ARP 学习。

##### 1.6.2 配置步骤

进入系统视图。
(1)

system-view
(2) 开启 ARP 报文源 MAC 地址一致性检查功能。
arp valid-check enable缺省情况下，ARP 报文源 MAC 地址一致性检查功能处于关闭状态。

#### 1.7 配置ARP主动确认功能

##### 1. 功能简介

的主动确认功能主要应用于网关设备上，防止攻击者仿冒用户欺骗网关设备。
ARP配置 主动确认功能后，设备在新建或更新 表项前需进行主动确认，防止产生错误的ARP ARP ARP表项。
配置严格模式后，新建 ARP 表项前，ARP 主动确认功能会执行更严格的检查：
• 收到目标 IP 地址为自己的 ARP 请求报文时，设备会发送 ARP 应答报文，但不建立 ARP 表项；
• 收到 ARP 应答报文时，需要确认本设备是否对该报文中的源 IP 地址发起过 ARP 解析：若发起过解析，解析成功后则设备启动主动确认功能，主动确认流程成功完成后，设备可以建立该表项；若未发起过解析，则设备丢弃该报文。

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 开启 ARP 主动确认功能。
arp active-ack [ strict ] enable
缺省情况下，ARP 主动确认功能处于关闭状态。
在严格模式下，只有 黑洞路由功能处于开启状态，ARP 主动确认功能才能生效。
ARP

#### 1.8 配置授权ARP功能

##### 1.8.1 功能简介

所谓授权 （ ），就是动态学习 的过程中，只有和 服务器生成的租ARP Authorized ARP ARP DHCP约或 DHCP 中继生成的安全表项一致的 ARP 报文才能够被学习。关于 DHCP 服务器和 DHCP 中继的介绍，请参见“三层技术-IP 业务配置指导”中的“DHCP 服务器”和“DHCP 中继”。
配置接口的授权 ARP 功能后，可以防止用户仿冒其他用户的 IP 地址或 MAC 地址对网络进行攻击，保证只有合法的用户才能使用网络资源，增加了网络的安全性。

##### 1.8.2 配置步骤

(1) 进入系统视图。
system-view
进入接口视图。
(2)
interface interface-type interface-number

###### 2. 组网图

支持的接口类型包括三层以太网接口、三层以太网子接口、三层聚合接口、三层聚合子接口和 接口视图。
VLAN开启授权 功能。
(3) ARP arp authorized enable缺省情况下，接口下的授权 功能处于关闭状态。
ARP

##### 1.8.3 授权ARP功能在DHCP服务器上的典型配置举例

###### 1. 组网需求

A是DHCP服务器，为同一网段中的客户端动态分配IP地址，地址池网段为10.1.1.0/24。
• Device通过在接口 Ten-GigabitEthernet1/0/1 上开启授权 ARP 功能来保证客户端的合法性。
• Device B 是 DHCP 客户端，通过 DHCP 协议从 DHCP 服务器获取 IP 地址。
组网图
2.
图1-3 授权 ARP 功能典型配置组网图

###### 3. 配置步骤

(1) 配置 Device A
配置接口的 地址。
\# IP
<DeviceA> system-view
[DeviceA] interface ten-gigabitethernet 1/0/1
[DeviceA-Ten-GigabitEthernet1/0/1] ip address 10.1.1.1 24
[DeviceA-Ten-GigabitEthernet1/0/1] quit
\# 开启 DHCP 服务。
[DeviceA] dhcp enable
[DeviceA] dhcp server ip-pool 1
[DeviceA-dhcp-pool-1] network 10.1.1.0 mask 255.255.255.0
[DeviceA-dhcp-pool-1] quit
\# 进入三层以太网接口视图。
[DeviceA] interface ten-gigabitethernet 1/0/1
开启接口授权 功能。
\# ARP
[DeviceA-Ten-GigabitEthernet1/0/1] arp authorized enable
[DeviceA-Ten-GigabitEthernet1/0/1] quit
(2) 配置 Device B
<DeviceB> system-view
[DeviceB] interface ten-gigabitethernet 1/0/1
[DeviceB-Ten-GigabitEthernet1/0/1] ip address dhcp-alloc
[DeviceB-Ten-GigabitEthernet1/0/1] quit

###### 4. 验证配置

Device B 获得 Device A 分配的 IP 后，在 Device A 查看授权 ARP 信息。
[DeviceA] display arp all Type: S-Static D-Dynamic O-Openflow R-Rule M-Multiport I-Invalid IP address MAC address VLAN/VSI Interface Aging Type
10.1.1.2 0012-3f86-e94c -- XGE1/0/1 960 D从以上信息可以获知 为 动态分配的 地址为 10.1.1.2。
Device A Device B IP此后，Device 与 通信时采用的 地址、MAC 地址等信息必须和授权 表项中的一B Device A IP ARP致，否则将无法通信，保证了客户端的合法性。

##### 1.8.4 授权ARP功能在DHCP中继上的典型配置举例

###### 1. 组网需求

• Device A 是 DHCP 服务器，为不同网段中的客户端动态分配 IP 地址，地址池网段为
10.10.1.0/24。
• Device B 是 DHCP 中继，通过在接口 Ten-GigabitEthernet1/0/2 上开启授权 ARP 功能来保证
客户端的合法性。
Device C 是 DHCP 客户端，通过 DHCP 中继从 DHCP 服务器获取 IP 地址。
•

###### 2. 组网图

图1-4 授权 功能典型配置组网图ARP

###### 3. 配置步骤

(1) 配置 Device A
配置接口的 地址。
\# IP
<DeviceA> system-view
[DeviceA] interface ten-gigabitethernet 1/0/1
[DeviceA-Ten-GigabitEthernet1/0/1] ip address 10.1.1.1 24
[DeviceA-Ten-GigabitEthernet1/0/1] quit
\# 开启 DHCP 服务。
[DeviceA] dhcp enable
[DeviceA] dhcp server ip-pool 1
[DeviceA-dhcp-pool-1] network 10.10.1.0 mask 255.255.255.0
[DeviceA-dhcp-pool-1] gateway-list 10.10.1.1

[DeviceA-dhcp-pool-1] quit [DeviceA] ip route-static 10.10.1.0 24 10.1.1.2
(2) 配置 Device B开启 服务。
\# DHCP <DeviceB> system-view [DeviceB] dhcp enable \# 配置接口的 IP 地址。
[DeviceB] interface ten-gigabitethernet 1/0/1 [DeviceB-Ten-GigabitEthernet1/0/1] ip address 10.1.1.2 24 [DeviceB-Ten-GigabitEthernet1/0/1] quit [DeviceB] interface ten-gigabitethernet 1/0/2 [DeviceB-Ten-GigabitEthernet1/0/2] ip address 10.10.1.1 24 \# 配置 Ten-GigabitEthernet1/0/2 接口工作在 DHCP 中继模式。
[DeviceB-Ten-GigabitEthernet1/0/2] dhcp select relay \# 配置 DHCP 服务器的地址。
[DeviceB-Ten-GigabitEthernet1/0/2] dhcp relay server-address 10.1.1.1开启接口授权 功能。
\# ARP [DeviceB-Ten-GigabitEthernet1/0/2] arp authorized enable [DeviceB-Ten-GigabitEthernet1/0/2] quit \# 开启 DHCP 中继用户地址表项记录功能。
[DeviceB] dhcp relay client-information record
(3) 配置 Device C <DeviceC> system-view [DeviceC] ip route-static 10.1.1.0 24 10.10.1.1 [DeviceC] interface ten-gigabitethernet 1/0/2 [DeviceC-Ten-GigabitEthernet1/0/2] ip address dhcp-alloc [DeviceC-Ten-GigabitEthernet1/0/2] quit

###### 4. 验证配置

(1) Device C 获得 Device A 分配的 IP 后，在 Device B 查看授权 ARP 信息。
[DeviceB] display arp all
Type: S-Static D-Dynamic O-Openflow R-Rule M-Multiport I-Invalid
IP address MAC address VLAN/VSI Interface Aging Type
10.10.1.2 0012-3f86-e94c -- XGE1/0/2 960 D
从以上信息可以获知 为 动态分配的 地址为 10.10.1.2。
Device A Device C IP
此后，Device 与 通信时采用的 地址、MAC 地址等信息必须和授权 表项
(2) C Device B IP ARP
中的一致，否则将无法通信，保证了客户端的合法性。

#### 1.9 配置ARP Detection功能

##### 1.9.1 功能简介

ARP Detection功能主要应用于接入设备上，通过检测并丢弃非法用户的ARP报文来防止仿冒用户、仿冒网关的攻击，具体包括以下几个功能：
• 用户合法性检查；

###### 3. 配置步骤

ARP 报文有效性检查；
•ARP 报文强制转发；
•ARP Detection 忽略端口匹配检查；
•
• ARP Detection 支持 VSI；
• ARP Detection 日志功能。
如果既配置了报文有效性检查功能，又配置了用户合法性检查功能，那么先进行报文有效性检查，然后进行用户合法性检查。
ARP Detection 功能与 ARP Snooping 功能不能同时配置，否则会导致 ARP Snooping 表项无法生成。

##### 1.9.2 用户合法性检查

###### 1. 功能简介

对于 ARP 信任接口，不进行用户合法性检查；对于 ARP 非信任接口，需要进行用户合法性检查，以防止仿冒用户的攻击。
用户合法性检查是根据 ARP 报文中源 IP 地址和源 MAC 地址检查用户是否是所属 VLAN 所在接口上的合法用户，包括基于用户合法性规则检查、IP Source Guard 静态绑定表项的检查、基于 DHCP表项的检查和基于 安全表项的检查。设备收到 报文后，首先进行基于用户Snooping 802.1X ARP合法性规则检查，如果找到与报文匹配的规则，则按照该规则对报文进行处理；如果未找到与报文匹配的规则，则继续进行基于 IP Source Guard 静态绑定表项的检查、基于 DHCP Snooping 表项的检查和基于 802.1X 安全表项的检查。只要符合三者中的任何一个，就认为该 ARP 报文合法，进行转发。如果所有检查都没有找到匹配的表项，则认为是非法报文，直接丢弃。
静态绑定表项通过 命令生成，详细介绍请参见“安全配置IP Source Guard ip source binding指导”中的“IP Source Guard”。DHCP Snooping 安全表项通过 DHCP Snooping 功能自动生成，详细介绍请参见“三层技术-IP 业务配置指导”中的“DHCP Snooping”。
802.1X 安全表项通过 802.1X 功能产生，802.1X 用户需要使用支持将 IP 地址上传的客户端，用户通过了 802.1X 认证并且将 IP 地址上传至配置 ARP Detection 的设备后，设备自动生成可用于 ARP Detection 的用户合法性检查的 802.1X 安全表项。802.1X 的详细介绍请参见“安全配置指导”中的“802.1X”。

###### 2. 配置限制和指导

配置用户合法性检查功能时，必须至少配置用户合法性规则或者 IP Source Guard 静态绑定表项、功能和 功能四者之一，否则所有从 非信任接口收到的 报文都将DHCP Snooping 802.1X ARP ARP被丢弃。
在配置 IP Source Guard 静态绑定表项时，必须指定 IP、MAC 和 VLAN 参数，否则 ARP 报文将无法通过基于 IP Source Guard 静态绑定表项的检查。
配置步骤
3.
(1) 进入系统视图。
system-view
(2) （可选）配置用户合法性检查规则。

arp detection rule rule-id { deny | permit } ip { ip-address [ mask ] | any } mac { mac-address [ mask ] | any } [ vlan vlan-id ]缺省情况下，未配置用户合法性检查规则。
进入 视图。
(3) VLAN vlan vlan-id开启 功能。
(4) ARP Detection arp detection enable缺省情况下，ARP Detection 功能处于关闭状态，即不进行用户合法性检查。
(5) （可选）将不需要进行用户合法性检查的接口配置为 ARP 信任接口。
a. 退回系统视图。
quit
b. 进入接口视图。
interface interface-type interface-number支持的接口类型包括二层以太网接口和二层聚合接口视图。
c. 将不需要进行用户合法性检查的接口配置为 ARP 信任接口。
arp detection trust缺省情况下，接口为 ARP 非信任接口。

##### 1.9.3 ARP报文有效性检查

###### 1. 功能简介

对于 ARP 信任接口，不进行报文有效性检查；对于 ARP 非信任接口，需要根据配置对 MAC 地址和 IP 地址不合法的报文进行过滤。可以选择配置源 MAC 地址、目的 MAC 地址或 IP 地址检查模式。
• 源 MAC 地址的检查模式：会检查 ARP 报文中的源 MAC 地址和以太网报文头中的源 MAC 地址是否一致，一致则认为有效，否则丢弃报文；
目的 地址的检查模式（只针对 应答报文）：会检查 应答报文中的目的 地
• MAC ARP ARP MAC址是否为全 0 或者全 1，是否和以太网报文头中的目的 MAC 地址一致。全 0、全 1、不一致的报文都是无效的，需要被丢弃；
• IP 地址检查模式：会检查 ARP 报文中的源 IP 或目的 IP 地址，如全 1、或者组播 IP 地址都是不合法的，需要被丢弃。对于 ARP 应答报文，源 IP 和目的 IP 地址都进行检查；对于 ARP 请求报文，只检查源 地址。
IP

###### 2. 配置准备

配置本功能前需保证已经配置了“1.9.2 用户合法性检查”。

###### 3. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 VLAN 视图。
vlan vlan-id
(3) 开启 ARP Detection 功能。

arp detection enable缺省情况下，ARP Detection 功能处于关闭状态。
(4) 开启 ARP 报文有效性检查功能。
a. 退回系统视图。
quit
b. 开启 ARP 报文有效性检查功能。
arp detection validate { dst-mac | ip | src-mac } *缺省情况下，ARP 报文有效性检查功能处于关闭状态。
(5) （可选）将不需要进行 ARP 报文有效性检查的接口配置为 ARP 信任接口。
a. 进入接口视图。
interface interface-type interface-number支持的接口类型包括二层以太网接口和二层聚合接口。
b. 将不需要进行 ARP 报文有效性检查的接口配置为 ARP 信任接口。
arp detection trust缺省情况下，接口为 ARP 非信任接口。

##### 1.9.4 ARP报文强制转发

###### 1. 功能简介

对于从 ARP 信任接口接收到的 ARP 报文不受此功能影响，按照正常流程进行转发；对于从 ARP非信任接口接收到的并且已经通过用户合法性检查的 ARP 报文的处理过程如下：
• 对于 ARP 请求报文，通过信任接口进行转发；
• 对于 ARP 应答报文，首先按照报文中的以太网目的 MAC 地址进行转发，若在 MAC 地址表中没有查到目的 MAC 地址对应的表项，则将此 ARP 应答报文通过信任接口进行转发。

###### 2. 配置限制和指导

报文强制转发功能不支持目的 地址为多端口 的情况。
ARP MAC MAC

###### 3. 配置准备

配置本功能前需保证已经配置了“1.9.2 用户合法性检查”。

###### 4. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 VLAN 视图。
vlan vlan-id
(3) 开启 ARP 报文强制转发功能。
arp restricted-forwarding enable
缺省情况下，ARP 报文强制转发功能处于关闭状态。

###### 1. 功能简介

##### 1.9.5 配置ARP Detection忽略端口匹配检查功能

功能简介
1.
设备开启 ARP Detection 功能后，会对非信任端口执行用户合法性检查，包括基于 IP Source Guard静态绑定表项的检查、基于 安全表项的检查、基于 安全表项的检查。使DHCP Snooping 802.1X用这些表项进行检查时，其中会检查 ARP 报文入端口和表项中的端口是否匹配，如果不匹配则丢弃此报文。
开启 ARP Detection 忽略端口匹配检查功能后，ARP Detection 在根据表项进行用户合法性检查时，会忽略 ARP 报文入端口和表项中的端口是否匹配的检查。

###### 2. 配置步骤

进入系统视图。
(1)
system-view
(2) 开启 ARP Detection 忽略端口匹配检查功能。
arp detection port-match-ignore缺省情况下，ARP Detection 忽略端口匹配检查功能处于关闭状态。

##### 1.9.6 ARP Detection支持VSI

###### 1. 功能简介

在 VXLAN 组网中，用户可以在 VTEP 设备上的 VSI 内配置用户合法性检查和 ARP 报文有效性检查。与 VLAN 内不同的是，在 VLAN 内，这两项检查针对的是 ARP 非信任接口，而在 VSI 内，这两项检查均针对的是 ARP 非信任 AC。在 VXLAN 中，与 VSI 关联的以太网服务实例统称为 AC（Attachment Circuit，接入电路），详细介绍请参见“VXLAN”。
VSI 内的用户合法性检查和 ARP 报文有效性检查所依赖的安全表项和检查过程与 VLAN 环境下的相同。

###### 2. 配置VSI内用户合法性检查功能

(1) 进入系统视图。
system-view
（可选）配置用户合法性检查规则。
(2)
arp detection rule rule-id { deny | permit } ip { ip-address [ mask ] | any }
mac { mac-address [ mask ] | any } [ vlan vlan-id ]
缺省情况下，未配置用户合法性检查规则。
(3) 进入 VSI 视图。
vsi vsi-name
开启 功能。
(4) ARP Detection
arp detection enable
缺省情况下， 功能处于关闭状态，即不进行用户合法性检查。
ARP Detection
（可选）配置 信任 AC。
(5) ARP Detection
退回系统视图。
a.
quit

b. 进入二层以太网接口或者二层聚合接口视图。
interface interface-type interface-number
c. 进入以太网服务实例视图。
service-instance instance-id
d. 配置 ARP Detection 信任 AC。
arp detection trust
缺省情况下，AC 为 ARP Detection 非信任 AC。

###### 3. 配置VSI内ARP报文有效性检查功能

(1) 进入系统视图。
system-view
(2) 进入 VSI 视图。
vsi vsi-name
(3) 开启 ARP Detection 功能。
arp detection enable
缺省情况下，ARP Detection 功能处于关闭状态，即不进行用户合法性检查。
(4) 退回系统视图。
quit
(5) 开启 ARP 报文有效性检查功能。
arp detection validate { dst-mac | ip | src-mac } *
缺省情况下，ARP 报文有效性检查功能处于关闭状态。
(6) （可选）配置 ARP Detection 信任 AC。
进入二层以太网接口或者二层聚合接口视图。
a.
interface interface-type interface-number
进入以太网服务实例视图。
b.
service-instance instance-id
配置 信任 AC。
c. ARP Detection
arp detection trust
缺省情况下， AC 为 ARP Detection 非信任 AC 。

##### 1.9.7 配置ARP Detection日志功能

###### 1. 功能简介

配置 日志功能后，设备在检测到非法 报文时将生成检测日志，日志内容包括：
ARP Detection ARP受到攻击的端口编号；
•非法 ARP 报文的源 IP 地址；
•丢弃的 ARP 报文总数。
•

###### 2. 配置步骤

进入系统视图。
(1)

system-view
(2) 开启 ARP Detection 日志功能。
arp detection log enable [ interval interval | number number ]缺省情况下，ARP Detection 日志功能处于关闭状态。

##### 1.9.8 ARP Detection显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 ARP Detection 的运行情况，通过查看显示信息验证配置的效果。
在用户视图下，用户可以执行 reset 命令清除 ARP Detection 的统计信息。
表1-3 显示和维护ARP Detection操作 命令显示开启了ARP Detection功能的VLAN display arp detection display arp detection statistics attack-source显示 ARP Detection 攻击源统计信息slot slot-number display arp detection statistics packet-drop显示ARP Detection丢弃报文的统计信息 [ interface interface-type interface-number [ service-instance instance-id ] ] reset arp detection statistics attack-source清除ARP Detection攻击源统计信息[ slot slot-number ] reset arp detection statistics packet-drop清除ARP DetectionARP Detection的报文丢弃[ interface interface-type interface-number统计信息[ service-instance service-instance-id ] ]

##### 1.9.9 用户合法性检查典型配置举例

###### 1. 组网需求

• Device A 是 DHCP 服务器；Device B 是支持 802.1X 的设备，在 VLAN 10 内配置 ARP
Detection 功能，对认证客户端进行保护，保证合法用户可以正常转发报文，否则丢弃。
• Host A 和 Host B 是本地 802.1X 接入用户。

###### 3. 配置步骤

###### 2. 组网图

图1-5 配置用户合法性检查组网图Gateway DHCP server Device A XGE1/0/3 Vlan-int10
10.1.1.1/24 VLAN 10 XGE1/0/3 Device B XGE1/0/1 XGE1/0/2 Host A Host B配置步骤
3.
(1) 配置组网图中所有接口属于 VLAN 及 Switch A 对应 VLAN 接口的 IP 地址（略）
(2) 配置 DHCP 服务器 Device A \# 配置 DHCP 地址池 0。
<DeviceA> system-view [DeviceA] dhcp enable [DeviceA] dhcp server ip-pool 0 [DeviceA-dhcp-pool-0] network 10.1.1.0 mask 255.255.255.0
(3) 配置客户端 Host A 和 Host B（略），必须使用上传 IP 地址方式。
配置设备
(4) Device B配置 功能。
\# 802.1X <DeviceB> system-view [DeviceB] dot1x [DeviceB] interface ten-gigabitethernet 1/0/1 [DeviceB-Ten-GigabitEthernet1/0/1] dot1x [DeviceB-Ten-GigabitEthernet1/0/1] quit [DeviceB] interface ten-gigabitethernet 1/0/2 [DeviceB-Ten-GigabitEthernet1/0/2] dot1x [DeviceB-Ten-GigabitEthernet1/0/2] quit \# 添加本地接入用户。
[DeviceB] local-user test [DeviceB-luser-test] service-type lan-access [DeviceB-luser-test] password simple test [DeviceB-luser-test] quit开启 功能，对用户合法性进行检查。
\# ARP Detection [DeviceB] vlan 10 [DeviceB-vlan10] arp detection enable

\# 接口状态缺省为非信任状态，上行接口配置为信任状态，下行接口按缺省配置。
[DeviceB-vlan10] interface ten-gigabitethernet 1/0/3 [DeviceB-Ten-GigabitEthernet1/0/3] arp detection trust [DeviceB-Ten-GigabitEthernet1/0/3] quit

###### 4. 验证配置

完成上述配置后，对于接口 和 收到的 报Ten-GigabitEthernet1/0/1 Ten-GigabitEthernet1/0/2 ARP文，需基于 802.1X 安全表项进行用户合法性检查。

##### 1.9.10 用户合法性检查和报文有效性检查典型配置举例

###### 1. 组网需求

• Device A 是 DHCP 服务器；
• Host A 是 DHCP 客户端；用户 Host B 的 IP 地址是 10.1.1.6，MAC 地址是 0001-0203-0607。
• Device B 是 DHCP Snooping 设备，在 VLAN 10 内配置 ARP Detection 功能，对 DHCP 客户
端和用户进行用户合法性检查和报文有效性检查。

###### 2. 组网图

图1-6 配置用户合法性检查和报文有效性检查组网图

###### 3. 配置步骤

(1) 配置组网图中所有接口属于 VLAN 及 Device A 对应 VLAN 接口的 IP 地址（略）
(2) 配置 DHCP 服务器 Device A
\# 配置 DHCP 地址池 0。
<DeviceA> system-view
[DeviceA] dhcp enable
[DeviceA] dhcp server ip-pool 0
[DeviceA-dhcp-pool-0] network 10.1.1.0 mask 255.255.255.0
(3) 配置 DHCP 客户端 Host A 和用户 Host B（略）

###### 1. 组网需求

(4) 配置设备 Device B
\# 开启 DHCP Snooping 功能。
<DeviceB> system-view
[DeviceB] dhcp snooping enable
[DeviceB] interface ten-gigabitethernet 1/0/3
[DeviceB-Ten-GigabitEthernet1/0/3] dhcp snooping trust
[DeviceB-Ten-GigabitEthernet1/0/3] quit
在接口 上开启 表项记录功能。
\# Ten-GigabitEthernet1/0/1 DHCP Snooping
[DeviceB] interface ten-gigabitethernet 1/0/1
[DeviceB-Ten-GigabitEthernet1/0/1] dhcp snooping binding record
[DeviceB-Ten-GigabitEthernet1/0/1] quit
开启 功能，对用户合法性进行检查。
\# ARP Detection
[DeviceB] vlan 10
[DeviceB-vlan10] arp detection enable
\# 接口状态缺省为非信任状态，上行接口配置为信任状态，下行接口按缺省配置。
[DeviceB-vlan10] interface ten-gigabitethernet 1/0/3
[DeviceB-Ten-GigabitEthernet1/0/3] arp detection trust
[DeviceB-Ten-GigabitEthernet1/0/3] quit
\# 在接口 Ten-GigabitEthernet1/0/2 上配置 IP Source Guard 静态绑定表项。
[DeviceB] interface ten-gigabitethernet 1/0/2
[DeviceB-Ten-GigabitEthernet1/0/2] ip source binding ip-address 10.1.1.6 mac-address
0001-0203-0607 vlan 10
[DeviceB-Ten-GigabitEthernet1/0/2] quit
\# 配置进行报文有效性检查。
[DeviceB] arp detection validate dst-mac ip src-mac

###### 4. 验证配置

完成上述配置后，对于接口 和 收到的 报Ten-GigabitEthernet1/0/1 Ten-GigabitEthernet1/0/2 ARP文，先进行报文有效性检查，然后基于 IP Source Guard 静态绑定表项、DHCP Snooping 安全表项进行用户合法性检查。

##### 1.9.11 ARP报文强制转发典型配置举例

组网需求
1.
Device A 是 DHCP 服务器。
•
• Host A 是 DHCP 客户端；用户 Host B 的 IP 地址是 10.1.1.6，MAC 地址是 0001-0203-0607。
• Host A 和 Host B 在设备 Device B 上端口隔离，但是均和网关 Device A 相通，Ten-GigabitEthernet1/0/1、Ten-GigabitEthernet1/0/2、Ten-GigabitEthernet1/0/3 均属于VLAN 10。
• Device B 是 DHCP Snooping 设备，在 VLAN 10 内开启 ARP Detection 功能，对 DHCP 客户端和用户进行保护，保证合法用户可以正常转发报文，否则丢弃。
要求：Device B 在开启 ARP Detection 功能后，对于 ARP 广播请求报文仍然能够进行端口隔离。

###### 2. 组网图

图1-7 配置 ARP 报文强制转发组网图

###### 3. 配置步骤

配置组网图中所有接口属于 及 对应 接口的 地址（略）
(1) VLAN Device A VLAN IP配置 服务器
(2) DHCP Device A \# 配置 DHCP 地址池 0。
<DeviceA> system-view [DeviceA] dhcp enable [DeviceA] dhcp server ip-pool 0 [DeviceA-dhcp-pool-0] network 10.1.1.0 mask 255.255.255.0
(3) 配置 DHCP 客户端 Host A 和用户 Host B（略）
(4) 配置设备 Device B \# 开启 DHCP Snooping 功能。
<DeviceB> system-view [DeviceB] dhcp snooping enable [DeviceB] interface ten-gigabitethernet 1/0/3 [DeviceB-Ten-GigabitEthernet1/0/3] dhcp snooping trust [DeviceB-Ten-GigabitEthernet1/0/3] quit \# 开启 ARP Detection 功能，对用户合法性进行检查。
[DeviceB] vlan 10 [DeviceB-vlan10] arp detection enable配置上行接口为信任状态，下行接口为缺省配置（非信任状态）。
\# [DeviceB-vlan10] interface ten-gigabitethernet 1/0/3 [DeviceB-Ten-GigabitEthernet1/0/3] arp detection trust [DeviceB-Ten-GigabitEthernet1/0/3] quit \# 在接口 Ten-GigabitEthernet1/0/2 上配置 IP Source Guard 静态绑定表项。
[DeviceB] interface ten-gigabitethernet 1/0/2

[DeviceB-Ten-GigabitEthernet1/0/2] ip source binding ip-address 10.1.1.6 mac-address 0001-0203-0607 vlan 10 [DeviceB-Ten-GigabitEthernet1/0/2] quit \# 配置进行报文有效性检查。
[DeviceB] arp detection validate dst-mac ip src-mac \# 配置端口隔离。
[DeviceB] port-isolate group 1 [DeviceB] interface ten-gigabitethernet 1/0/1 [DeviceB-Ten-GigabitEthernet1/0/1] port-isolate enable group 1 [DeviceB-Ten-GigabitEthernet1/0/1] quit [DeviceB] interface ten-gigabitethernet 1/0/2 [DeviceB-Ten-GigabitEthernet1/0/2] port-isolate enable group 1 [DeviceB-Ten-GigabitEthernet1/0/2] quit完成上述配置后，对于接口 Ten-GigabitEthernet1/0/1 和 Ten-GigabitEthernet1/0/2 收到的ARP 报文，先进行报文有效性检查，然后基于 IP Source Guard 静态绑定表项、DHCP安全表项进行用户合法性检查。但是，Host 发往 的 广播请求报文，Snooping A Device A ARP由于通过了用户合法性检查，所以能够被转发到 Host B，端口隔离功能失效。
\# 开启 ARP 报文强制转发功能。
[DeviceB] vlan 10 [DeviceB-vlan10] arp restricted-forwarding enable [DeviceB-vlan10] quit

###### 4. 验证配置

此时，Host A 发往 Device A 的合法 ARP 广播请求报文只能通过信任接口 Ten-GigabitEthernet1/0/3转发，不能被 Host B 接收到，端口隔离功能可以正常工作。

#### 1.10 配置ARP自动扫描、固化功能

##### 1. 功能简介

建议在网吧这种环境稳定的小型网络中使用 自动扫描、固化功能。ARP 自动扫描功能一般与ARP ARP 固化功能配合使用：
• 配置 ARP 自动扫描功能后，设备会对局域网内的邻居自动进行扫描（向邻居发送 ARP 请求报文，获取邻居的 MAC 地址，从而建立动态 ARP 表项）。
• ARP 固化用来将当前的 ARP 动态表项（包括 ARP 自动扫描生成的动态 ARP 表项）转换为静态 ARP 表项。通过对动态 ARP 表项的固化，可以有效防止攻击者修改 ARP 表项。
固化后的静态 ARP 表项与配置产生的静态 ARP 表项相同。
接口上开启了 ARP 自动扫描功能后，会向扫描区间的所有 IP 地址同时发送 ARP 请求报文，这会造成设备瞬间 利用率过高、网络负载过大的问题。用户可以通过设置接口发送 报文的速CPU ARP率解决此问题。

##### 2. 配置限制和指导

• 对于已存在 ARP 表项的 IP 地址不进行扫描。
• 扫描操作可能比较耗时，用户可以通过<Ctrl_C>来终止扫描（在终止扫描时，对于已经收到
的邻居应答，会建立该邻居的动态 ARP 表项）。

固化生成的静态 ARP 表项数量同样受到设备可以支持的静态 ARP 表项数目的限制，由于静
•态 表项数量的限制可能导致只有部分动态 表项被固化。
ARP ARP通过 命令将当前的动态 表项转换为静态 表项后，后续学习到的动态
• arp fixup ARP ARP ARP 表项可以通过再次执行 arp fixup 命令进行固化。
• 通过固化生成的静态 ARP 表项，可以通过命令行 undo arp ip-address [ vpn-instance-name ]逐条删除，也可以通过命令行 reset arp all 或 reset arp static 全部删除。

##### 3. 配置步骤

进入系统视图。
(1)
system-view进入接口视图。
(2)
interface interface-type interface-number开启 自动扫描功能。
(3) ARP arp scan [ start-ip-address to end-ip-address ] [ send-rate pps ]
(4) 退回系统视图。
quit
(5) 将设备上的动态 ARP 表项转化成静态 ARP 表项。
arp fixup

#### 1.11 配置ARP网关保护功能

##### 1.11.1 功能简介

在设备上不与网关相连的接口上配置此功能，可以防止伪造网关攻击。
在接口上开启此功能后，当接口收到 ARP 报文时，将检查 ARP 报文的源 IP 地址是否和配置的被保护网关的 IP 地址相同。如果相同，则认为此报文非法，将其丢弃；否则，认为此报文合法，继续进行后续处理。

##### 1.11.2 配置限制和指导

• 每个接口最多支持配置 8 个被保护的网关 IP 地址。
• 不能在同一接口下同时配置命令 arp filter source 和 arp filter binding。
• 本功能与 ARP Detection、MFF、ARP Snooping 配合使用时，先进行本功能检查，本功能检
查通过后才会进行其他配合功能的处理。

##### 1.11.3 配置步骤

(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number

支持的接口类型包括二层以太网接口和二层聚合接口。
(3) 开启 ARP 网关保护功能，配置被保护的网关 IP 地址。
arp filter source ip-address缺省情况下，ARP 网关保护功能处于关闭状态。

##### 1.11.4 ARP网关保护功能典型配置举例

###### 1. 组网需求

与 Device B 相连的 Host B 进行了仿造网关 Device A（IP 地址为 10.1.1.1）的 ARP 攻击，导致与相连的设备与网关 通信时错误发往了 B。
Device B Device A Host要求：通过配置防止这种仿造网关攻击。

###### 2. 组网图

图1-8 配置 ARP 网关保护功能组网图

###### 3. 配置步骤

\# 在 Device B 上开启 ARP 网关保护功能。
<DeviceB> system-view [DeviceB] interface ten-gigabitethernet 1/0/1 [DeviceB-Ten-GigabitEthernet1/0/1] arp filter source 10.1.1.1 [DeviceB-Ten-GigabitEthernet1/0/1] quit [DeviceB] interface ten-gigabitethernet 1/0/2 [DeviceB-Ten-GigabitEthernet1/0/2] arp filter source 10.1.1.1完成上述配置后，对于 发送的伪造的源 地址为网关 地址的 报文将会被丢弃，不Host B IP IP ARP会再被转发。

#### 1.12 配置ARP过滤保护功能

##### 1.12.1 功能简介

本功能用来限制接口下允许通过的 ARP 报文，可以防止仿冒网关和仿冒用户的攻击。

在接口上配置此功能后，当接口收到 ARP 报文时，将检查 ARP 报文的源 IP 地址和源 MAC 地址是否和允许通过的 地址和 地址相同：
IP MAC如果相同，则认为此报文合法，继续进行后续处理；
•如果不相同，则认为此报文非法，将其丢弃。
•

##### 1.12.2 配置限制和指导

• 每个接口最多支持配置 8 组允许通过的 ARP 报文的源 IP 地址和源 MAC 地址。
• 不能在同一接口下同时配置命令 arp filter source 和 arp filter binding。
• 本功能与 ARP Detection、MFF、ARP Snooping 配合使用时，先进行本功能检查，本功能检
查通过后才会进行其他配合功能的处理。

##### 1.12.3 配置步骤

(1) 进入系统视图。
system-view
进入接口视图。
(2)
interface interface-type interface-number
支持的接口类型包括二层以太网接口和二层聚合接口。
开启 过滤保护功能，配置允许通过的 报文的源 地址和源 地址。
(3) ARP ARP IP MAC
arp filter binding ip-address mac-address
缺省情况下，ARP 过滤保护功能处于关闭状态。

##### 1.12.4 ARP过滤保护功能典型配置举例

###### 1. 组网需求

Host A 的 IP 地址为 10.1.1.2，MAC 地址为 000f-e349-1233。
•Host B 的 IP 地址为 10.1.1.3，MAC 地址为 000f-e349-1234。
•限制 Device B 的 Ten-GigabitEthernet1/0/1、Ten-GigabitEthernet1/0/2 接口只允许指定用户
•接入，不允许其他用户接入。

###### 4. 验证配置

###### 2. 组网图

图1-9 配置 ARP 过滤保护功能组网图Device A XGE1/0/3 Device B XGE1/0/1 XGE1/0/2 Host A Host B

###### 3. 配置步骤

\# 开启 Device B 的 ARP 过滤保护功能。
<DeviceB> system-view [DeviceB] interface ten-gigabitethernet 1/0/1 [DeviceB-Ten-GigabitEthernet1/0/1] arp filter binding 10.1.1.2 000f-e349-1233 [DeviceB-Ten-GigabitEthernet1/0/1] quit [DeviceB] interface ten-gigabitethernet 1/0/2 [DeviceB-Ten-GigabitEthernet1/0/2] arp filter binding 10.1.1.3 000f-e349-1234验证配置
4.
完成上述配置后，接口 Ten-GigabitEthernet1/0/1 收到 Host A 发出的源 IP 地址为 10.1.1.2、源 MAC地 址 为 的 报 文 将 被 允 许 通 过 ， 其 他 报 文 将 被 丢 弃 ； 接 口000f-e349-1233 ARP ARP Ten-GigabitEthernet1/0/2 收到 Host B 发出的源 IP 地址为 10.1.1.3、源 MAC 地址为 000f-e349-1234的 ARP 报文将被允许通过，其他 ARP 报文将被丢弃。

#### 1.13 配置ARP报文发送端IP地址检查功能

##### 1.13.1 功能简介

配置本功能后，网关设备在进行 ARP 学习前将对 ARP 报文进行检查。如果指定 VLAN 内的 ARP报文的发送端 IP 地址不在指定源 IP 地址范围内，则认为是攻击报文，将其丢弃；否则，继续进行学习。
ARP

##### 1.13.2 配置限制和指导

• 当 Super VLAN 与 Sub VLAN 间建立映射关系时，本功能在 Sub VLAN 内配置。
• 如果配置了 Primary VLAN 和指定的 Secondary VLAN 间三层互通，则本功能必须 Primary
VLAN 中配置；否则，本功能可在 Primary VLAN 或任意 Secondary VLAN 中配置。

###### 2. 组网图

##### 1.13.3 配置步骤

进入系统视图。
(1)
system-view进入 视图。
(2) VLAN vlan vlan-id
(3) 配置 ARP 报文发送端 IP 地址检查功能，并配置允许学习 ARP 报文的发送端 IP 地址范围。
arp sender-ip-range start-ip-address end-ip-address缺省情况下，ARP 报文发送端 IP 地址检查功能处于关闭状态。

##### 1.13.4 ARP报文发送端IP地址检查功能典型配置举例

###### 1. 组网需求

Device 为网关设备连接不同的 VLAN。现有如下组网需求：
通过创建 Super VLAN ，实现 Device 连接的各 VLAN 用户（均在 10.1.1.0/24 网段）之间能够
•二层隔离和三层互通，且各 的用户公用 地址 作为三层通信的网关地址。
VLAN IP 10.1.1.1/24通过配置 报文发送端 地址检查功能，实现 内只允许 地址范围为 10.1.1.1～
• ARP IP VLAN 2 IP
10.1.1.10 的用户访网关设备。
组网图
2.
图1-10 ARP 报文发送端 IP 地址检查功能组网图

###### 3. 配置步骤

\# 创建 VLAN 10，配置 VLAN 接口的 IP 地址为 10.1.1.1/24。
<Device> system-view [Device] vlan 10 [Device-vlan10] quit [Device] interface vlan-interface 10 [Device-Vlan-interface10] ip address 10.1.1.1 255.255.255.0 [Device] quit

\# 创 建 VLAN 2 ， 并 向 VLAN 2 中 添 加 端 口 Ten-GigabitEthernet1/0/1 和 端 口Ten-GigabitEthernet1/0/2。
[Device] vlan 2 [Device-vlan2] port ten-gigabitethernet 1/0/1 ten-gigabitethernet 1/0/2 [Device-vlan2] quit创 建 ， 并 向 中 添 加 端 口 和 端 口\# VLAN 3 VLAN 3 Ten-GigabitEthernet1/0/3 Ten-GigabitEthernet1/0/4。
[Device] vlan 3 [Device-vlan3] port ten-gigabitethernet 1/0/3 ten-gigabitethernet 1/0/4 [Device-vlan3] quit \# 创 建 VLAN 4 ， 并 向 VLAN 4 中 添 加 端 口 Ten-GigabitEthernet1/0/5 和 端 口Ten-GigabitEthernet1/0/6。
[Device] vlan 4 [Device-vlan4] port ten-gigabitethernet 1/0/5 ten-gigabitethernet 1/0/6 [Device-vlan4] quit \# 配置 VLAN 10 为 Super VLAN ，其关联的 Sub VLAN 为 VLAN 2 、 VLAN 3 和 VLAN 4 。
[Device] vlan 10 [Device-vlan10] supervlan [Device-vlan10] subvlan 2 3 4 [Device-vlan10] quit \# 在 VLAN 2 内，配置 ARP 报文发送端 IP 地址检查功能，并指定允许学习 ARP 报文的发送端 IP地址范围为 10.1.1.1～10.1.1.10。
[Device] vlan 2 [Device-vlan2] arp sender-ip-range 10.1.1.1 10.1.1.10

###### 4. 验证配置

完成上述配置后，只有当 内的 报文的发送端 地址属于 10.1.1.1～10.1.1.10 地址范VLAN 2 ARP IP围时，才允许用户访问网关设备 Device，其他不属于该地址范围内的 ARP 报文将被丢弃。

## 20-ND攻击防御配置

目 录攻击防御简介支持配置 功能配置及应用 策略

### 1 ND攻击防御

1 ND攻击防御

#### 1.1 ND攻击防御简介

ND协议功能强大，但是却没有任何安全机制，容易被攻击者利用。如 图 1-1 所示，当Device作为接入设备时，攻击者Host B可以仿冒其他用户、仿冒网关发送伪造的ND报文，对网络进行攻击：
如果攻击者仿冒其他用户的 IPv6 地址发送 NS/NA/RS 报文，将会改写网关或者其他用户的
•表项，导致被仿冒用户的报文错误的发送到攻击者的终端上。
ND如果攻击者仿冒网关发送 报文，会导致其他用户的 配置参数错误和 表项被改写。
• RA IPv6 ND图1-1 ND 攻击示意图伪造的 ND 报文具有如下特点：
• 伪造的 ND 报文中源 MAC 地址和源链路层选项地址中的 MAC 地址不一致。
• 伪造的 ND 报文中源 IPv6 地址和源 MAC 地址的映射关系不是合法用户真实的映射关系。
根据上述攻击报文的特点，设备开发了多种功能对 ND 攻击进行检测，可以有效地防范 ND 攻击带来的危害。

#### 1.2 ND攻击防御配置任务简介

如下所有配置均为可选，请根据实际情况选择配置。
• 开启 ND 协议报文源 MAC 地址一致性检查功能
• 配置ND Detection功能配置RA Guard功能
•

#### 1.3 开启ND协议报文源MAC地址一致性检查功能

##### 1. 功能简介

协议报文源 地址一致性检查功能主要应用于网关设备上，防御 报文中的源 地址ND MAC ND MAC和以太网数据帧首部中的源 MAC 地址不同的 ND 攻击。
开启本特性后，网关设备会对接收的 ND 协议报文进行检查。如果 ND 报文中的源 MAC 地址和以太网数据帧首部中的源 MAC 地址不一致，则认为是攻击报文，将其丢弃；否则，继续进行 ND 学习。
若开启 ND 日志信息功能，当用户 ND 报文中的源 MAC 地址和以太网数据帧首部中的源 MAC 地址不同时，会有相关的日志信息输出。设备生成的 日志信息会交给信息中心模块处理，信息中心ND模块的配置将决定日志信息的发送规则和发送方向。关于信息中心的详细描述请参见“网络管理和监控配置指导”中的“信息中心”。

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 开启 ND 协议报文源 MAC 地址一致性检查功能。
ipv6 nd mac-check enable
缺省情况下，ND 协议报文源 MAC 地址一致性检查功能处于关闭状态。
(3) （可选）开启 ND 日志信息功能。
ipv6 nd check log enable
缺省情况下，ND 日志信息功能处于关闭状态。
为了防止设备输出过多的 ND 日志信息，一般情况下建议不要开启此功能。

#### 1.4 配置ND Detection功能

##### 1.4.1 功能简介

ND Detection 功能主要应用于接入设备上，检查用户的合法性。对于合法用户的 ND 报文进行正常转发，否则直接丢弃，从而防止仿冒用户、仿冒网关的攻击，具体包括以下几个功能：
• 用户合法性检查；
• ND Detection 支持 VSI；
• ND Detection 日志功能。
ND Detection 功能将接入设备上的接口分为两种：ND 信任接口、ND 非信任接口。
• 对于 ND 信任接口，不进行用户合法性检查；
• 对于 ND 非信任接口，如果收到 RA 和 RR 消息，则认为是非法报文直接丢弃，如果收到其它类型的 ND 报文，则需要进行用户合法性检查，以防止仿冒用户的攻击。
用户合法性检查是根据 ND 报文中源 IPv6 地址和源 MAC 地址，检查用户是否是报文收到接口所属VLAN 上的合法用户，包括 IPv6 Source Guard 静态绑定表项、ND Snooping 表项和 DHCPv6安全表项的检查。只要能查询到表项，就认为该 报文合法，进行转发。如果没有匹配Snooping ND的表项，则认为是非法报文，直接丢弃。

IPv6 Source Guard 静态绑定表项通过 ipv6 source binding 命令生成，详细介绍请参见“安全配置指导”中的“IP Guard”。DHCPv6 安全表项通过 功能Source Snooping DHCPv6 Snooping自动生成，详细介绍请参见“三层技术-IP 业务配置指导”中的“DHCPv6 Snooping”。ND Snooping表项通过 ND Snooping 功能自动生成，详细介绍请参见“三层技术-IP 业务配置指导”中的“IPv6基础”。

##### 1.4.2 配置限制和指导

• 配置 ND Detection 功能时，必须至少配置 IPv6 Source Guard 静态绑定表项、DHCPv6
Snooping 功能和 ND Snooping 功能三者之一，否则所有从 ND 非信任接口收到的 ND 报文都
将被丢弃。
在与 功能配合时，IPv6 绑定表项中必须指定 参数，且该
• ND Detection Source Guard VLAN
VLAN 为配置 ND Detection 功能的 VLAN，否则 ND 报文将无法通过接口的 IPv6 Source
Guard 静态绑定表项的检查。

##### 1.4.3 配置步骤

进入系统视图。
(1)
system-view进入 视图。
(2) VLAN vlan vlan-id
(3) 开启 ND Detection 功能。
ipv6 nd detection enable缺省情况下，ND Detection 功能处于关闭状态。即不进行用户合法性检查。
(4) （可选）将不需要进行用户合法性检查的接口配置为 ND 信任接口。
a. 退回系统视图。
quit
b. 进入接口视图。
interface interface-type interface-number
c. 将不需要进行用户合法性检查的接口配置为 ND 信任接口。
ipv6 nd detection trust缺省情况下，接口为 ND 非信任接口。

##### 1.4.4 ND Detection支持VSI

###### 1. 功能简介

在 VXLAN 组网中，用户可以在 VTEP 设备上的 VSI 内配置用户合法性检查。与 VLAN 内不同的是，在 VLAN 内，这项检查针对的是 ND 非信接口，而在 VSI 内，这项检查针对的是 ND 非信任 AC。
在 中，与 关联的以太网服务实例统称为 （ ，接入电路），详细介VXLAN VSI AC Attachment Circuit绍请参见“VXLAN”。
VSI 内的用户合法性检查所依赖的安全表项和检查过程与 VLAN 环境下的相同。

###### 1. 功能简介

###### 2. 配置步骤

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 进入 VSI 视图。
vsi vsi-name
(3) 开启 ND Detection 功能。
ipv6 nd detection enable
缺省情况下，ND Detection 功能处于关闭状态。即不进行用户合法性检查。
（可选）配置 信任 AC。
(4) ND Detection
退回系统视图。
a.
quit
进入接口视图。
b.
interface interface-type interface-number
c. 进入以太网服务实例视图。
service-instance instance-id
d. 将不需要进行用户合法性检查的接口配置为 ND 信任接口。
ipv6 nd detection trust
缺省情况下，接口为 ND 非信任接口。

##### 1.4.5 配置ND Detection日志功能

功能简介
1.
配置 ND Detection 日志功能后，设备在检测到非法 ND 报文时将生成检测日志，日志内容包括：
• 在 VLAN 组网中，显示的是受到攻击的端口编号；
• 非法 ND 报文的源 IP 地址；
• 非法 ND 报文的源 MAC 地址；
• 非法 ND 报文所属的 VLAN ID；
• 丢弃的 ND 报文总数。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 开启 ND Detection 日志功能。
ipv6 nd detection log enable缺省情况下，ND Detection 日志功能处于关闭状态。

##### 1.4.6 ND Detection功能显示和维护

在完成上述配置后，在任意视图下执行 命令可以显示配置后 的运行情况，display ND Detection通过查看显示信息验证配置的效果。

###### 2. 组网图

在用户视图下，用户可以执行 reset 命令清除 ND Detection 的统计信息。
表1-1 ND Detection 功能显示和维护操作 命令display ipv6 nd detection statistics [ interface显示ND Detection丢弃报文的统计信息 interface-type interface-number [ service-instance instance-id ] ] reset ipv6 nd detection statistics [ interface清除ND Detection的统计信息 interface-type interface-number [ service-instance instance-id ] ]

##### 1.4.7 ND Detection功能典型配置举例

###### 1. 组网需求

用户 Host A 和 Host B 通过 DeviceB 接入网关 Device A。用户 Host A 的 IPv6 地址是 10::5/64，MAC地址是 0001-0203-0405。用户 的 地址是 10::6/64，MAC 地址是 0001-0203-0607。
Host B IPv6要求：在 上配置 功能对用户的合法性进行检查，保证合法用户的报文可以Device B ND Detection被正常转发，非法用户的报文被丢弃。
组网图
2.
图1-2 配置 ND Detection 组网图Internet Gateway Device A XGE1/0/3 Vlan-int10 10::1/64 VLAN 10 ND snooping XGE1/03 Device B XGE1/01 XGE1/0/2 Host A Host B 10::5/64 10::6/64 0001-0203-0405 0001-0203-0607

###### 3. 配置步骤

(1) 配置 Device A
\# 创建 VLAN 10。

<DeviceA> system-view [DeviceA] vlan 10 [DeviceA-vlan10] quit \# 配置接口 Ten-GigabitEthernet1/0/3 允许 VLAN 10 的报文通过。
[DeviceA] interface ten-gigabitethernet 1/0/3 [DeviceA-Ten-GigabitEthernet1/0/3] port link-type trunk [DeviceA-Ten-GigabitEthernet1/0/3] port trunk permit vlan 10 [DeviceA-Ten-GigabitEthernet1/0/3] quit \# 配置 VLAN 接口 10 的 IPv6 地址。
[DeviceA] interface vlan-interface 10 [DeviceA-Vlan-interface10] ipv6 address 10::1/64 [DeviceA-Vlan-interface10] quit
(2) 配置 Device B \# 创建 VLAN 10。
<DeviceB> system-view [DeviceB] vlan 10 [DeviceB-vlan10] quit \# 配置接口 Ten-GigabitEthernet1/0/1～Ten-GigabitEthernet1/0/3 允许 VLAN 10 的报文通过。
[DeviceB] interface ten-gigabitethernet 1/0/1 [DeviceB-Ten-GigabitEthernet1/0/1] port link-type access [DeviceB-Ten-GigabitEthernet1/0/1] port access vlan 10 [DeviceB-Ten-GigabitEthernet1/0/1] quit [DeviceB] interface ten-gigabitethernet 1/0/2 [DeviceB-Ten-GigabitEthernet1/0/2] port link-type access [DeviceB-Ten-GigabitEthernet1/0/2] port access vlan 10 [DeviceB-Ten-GigabitEthernet1/0/2] quit [DeviceB] interface ten-gigabitethernet 1/0/3 [DeviceB-Ten-GigabitEthernet1/0/3] port link-type trunk [DeviceB-Ten-GigabitEthernet1/0/3] port trunk permit vlan 10 [DeviceB-Ten-GigabitEthernet1/0/3] quit \# 开启 ND Detection 功能。
[DeviceB] vlan 10 [DeviceB-vlan10] ipv6 nd detection enable \# 开启 ND Snooping 表项获取功能，通过 ND 报文的源地址（包括全球单播地址和链路本地地址）生成 表项。
ND Snooping [DeviceB-vlan10] ipv6 nd snooping enable global [DeviceB-vlan10] ipv6 nd snooping enable link-local [DeviceB-vlan10] quit将上行接口 配置为 信任接口，下行接口\# Ten-GigabitEthernet1/0/3 ND Ten-GigabitEthernet1/0/1和Ten-GigabitEthernet1/0/2采用缺省配置，即为ND非信任接口。
[DeviceB] interface ten-gigabitethernet 1/0/3 [DeviceB-Ten-GigabitEthernet1/0/3] ipv6 nd detection trust

###### 4. 验证配置

完成上述配置后，对于接口Ten-GigabitEthernet1/0/1和Ten-GigabitEthernet1/0/2收到的ND报文，基于 ND Snooping 安全表项进行检查。

#### 1.5 配置RA Guard功能

##### 1.5.1 功能简介

RA Guard 功能用来在二层接入设备上防范路由通告报文（RA 报文）欺骗攻击。
二层接入设备收到目的 MAC 地址为单播或组播地址的 RA 报文后，RA Guard 功能按照如下方式处理 报文：
RA如果接收 RA 报文的接口配置了接口角色，则通过系统根据接口角色来选择转发还是丢弃该报
•文：
若接口角色为路由器，则直接转发 报文；
RA (cid:123)
若接口角色为用户，则直接丢弃 报文。
RA (cid:123)
如果接收RA报文的接口没有配置接口角色，则该报文继续匹配该接口属VLAN内的RA
• Guard策略：
若 RA Guard 策略中未配置任何匹配规则，则应用该策略的接口直接转发 RA 报文；
(cid:123)
若 RA Guard 策略中配置了匹配规则，则 RA 报文需匹配策略下所有规则成功才会被转发；
(cid:123)
否则，该报文即被丢弃。

##### 1.5.2 配置接口角色

###### 1. 配置限制和指导

可根据接口在组网中的位置来配置接口的角色。如果确认接口连接的是用户主机，则配置接口角色为用户角色（host）；如果确定接口连接的是路由器，则配置接口角色为路由器角色（router）。

###### 2. 配置步骤

进入系统视图。
(1)
system-view进入接口视图。
(2)
进入二层以太网接口视图(cid:123)
interface interface-type interface-number进入二层聚合接口视图(cid:123)
interface bridge-aggregation interface-number
(3) 配置接口角色。
ipv6 nd raguard role { host | router }缺省情况下，未配置接口角色。

###### 1. 功能简介

###### 1. 功能简介

##### 1.5.3 配置及应用RA Guard策略

功能简介
1.
对于下面两种情况，可通过配置 RA Guard 策略对 RA 报文按规则匹配条件进行过滤：
• 不能判断接口连接的设备/终端类型，即不能通过配置接口角色来选择丢弃还是转发 RA 报文；
• 确认接口连接的是路由器，但用户不希望直接转发 RA 报文而是进行过滤。

###### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 创建 RA Guard 策略，并进入 RA Guard 策略视图。
ipv6 nd raguard policy policy-name
(3) 配置 RA Guard 策略。请至少选择其中一项进行配置。
配置 ACL 匹配规则。
(cid:123)
if-match acl { ipv6-acl-number | name ipv6-acl-name }
配置前缀匹配规则。
(cid:123)
if-match prefix acl { ipv6-acl-number | name ipv6-acl-name }
配置路由最高优先级匹配规则。
(cid:123)
if-match router-preference maximum { high | low | medium }
配置被管理地址标志位匹配规则。
(cid:123)
if-match autoconfig managed-address-flag { off | on }
配置其他信息配置标志位匹配规则。
(cid:123)
if-match autoconfig other-flag { off | on }
配置 报文内跳数最大值或最小值匹配规则。
RA
(cid:123)
if-match hop-limit { maximum | minimum } limit
缺省情况下，未配置 策略。
RA Guard
(4) 退回系统视图。
quit
(5) 进入 VLAN 视图。
vlan vlan-number
(6) 应用 RA Guard 策略。
ipv6 nd raguard apply policy [ policy-name ]
缺省情况下，未应用 RA Guard 策略。

##### 1.5.4 配置RA Guard日志功能

功能简介
1.
RA Guard 日志可以方便管理员定位问题和解决问题，对处理 RA 报文的信息进行的记录。开启 RA日志功能后，设备在检测到非法 报文时将生成检测日志，日志内容包括：受到攻击的接Guard RA口名称、RA 报文的源 IP 地址和丢弃的 RA 报文总数。

###### 2. 配置步骤

设备生成的 RA Guard 日志信息会交给信息中心模块处理，信息中心模块的配置将决定日志信息的发送规则和发送方向。关于信息中心的详细描述请参见“网络管理和监控配置指导”中的“信息中心”。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 开启 RA Guard 日志功能。
ipv6 nd raguard log enable缺省情况下，RA Guard 日志功能处于关闭状态。

##### 1.5.5 RA Guard功能显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示 策略的信息。
RA Guard表1-2 RA Guard 功能显示和维护操作 命令显示已创建的RA Guard策略信息 display ipv6 nd raguard policy [ policy-name ] display ipv6 nd raguard statistics [ interface显示RA Guard的报文统计信息interface-type interface-number ] reset ipv6 nd raguard statistics [ interface清除RA Guard的报文统计信息interface-type interface-number ]

##### 1.5.6 RA Guard功能典型配置举例

###### 1. 组网需求

如 图 1-3 所示，在Device B上通过接口Ten-GigabitEthernet1/0/1 和Ten-GigabitEthernet1/0/2 分别连 接 主 机 和 ， 通 过 接 口Ten-GigabitEthernet1/0/3 连 接Device 。 接 口Host Device C A Ten-GigabitEthernet1/0/1、Ten-GigabitEthernet1/0/2 和Ten-GigabitEthernet1/0/3 都属于VLAN 10。
为防范路由通告报文（RA 报文）欺骗攻击，可在 Device B 上配置 RA Guard 策略规则，并在 VLAN 10 下应用该策略规则：
• 接口 Ten-GigabitEthernet1/0/2 连接的是未知设备，用户希望该接口对 RA 报文按 RA Guard策略规则进行匹配过滤；
接口 Ten-GigabitEthernet1/0/1 连接的是用户，用户希望该接口完全过滤 RA 报文将其直接丢
•弃；
接口 连接的是 A，用户希望该接口完全信任 报文将其直
• Ten-GigabitEthernet1/0/3 Device RA接转发。

###### 2. 组网图

图1-3 RA Guard 功能组网图Device A VLAN10 XGE1/0/3 Device B XGE1/0/1 XGE1/0/2 Device C Host

###### 3. 配置步骤

\# 在 Device B 上创建 RA Guard 策略 policy1，并配置匹配规则。匹配最高路由优先级为高，被管理地址标志位置为 1、其他信息配置标志位置为 1、跳数最小值为 且最大值为 的 报文。
100 120 RA <DeviceB> system-view [DeviceB] ipv6 nd raguard policy policy1 [DeviceB-raguard-policy-policy1] if-match router-preference maximum high [DeviceB-raguard-policy-policy1] if-match autoconfig managed-address-flag on [DeviceB-raguard-policy-policy1] if-match autoconfig other-flag on [DeviceB-raguard-policy-policy1] if-match hop-limit maximum 120 [DeviceB-raguard-policy-policy1] if-match hop-limit minimum 100 [DeviceB-raguard-policy-policy1] quit \# 配置接口 Ten-GigabitEthernet1/0/1～Ten-GigabitEthernet1/0/3 允许 VLAN 10 的报文通过，并在VLAN 10 下应用 RA Guard 策略。
[DeviceB] interface ten-gigabitethernet 1/0/1 [DeviceB-Ten-GigabitEthernet1/0/1] port link-type access [DeviceB-Ten-GigabitEthernet1/0/1] port access vlan 10 [DeviceB-Ten-GigabitEthernet1/0/1] quit [DeviceB] interface ten-gigabitethernet 1/0/2 [DeviceB-Ten-GigabitEthernet1/0/2] port link-type access [DeviceB-Ten-GigabitEthernet1/0/2] port access vlan 10 [DeviceB-Ten-GigabitEthernet1/0/2] quit [DeviceB] interface ten-gigabitethernet 1/0/3 [DeviceB-Ten-GigabitEthernet1/0/3] port link-type trunk [DeviceB-Ten-GigabitEthernet1/0/3] port trunk permit vlan 10 [DeviceB-Ten-GigabitEthernet1/0/3] quit [DeviceB] vlan 10 [DeviceB-vlan10] ipv6 nd raguard apply policy policy1 [DeviceB-vlan10] quit \# 配置接口 Ten-GigabitEthernet1/0/1 为用户角色。
[DeviceB] interface ten-gigabitethernet 1/0/1 [DeviceB-Ten-GigabitEthernet1/0/1] ipv6 nd raguard role host

###### 4. 验证配置

[DeviceB-Ten-GigabitEthernet1/0/1] quit \# 配置接口 Ten-GigabitEthernet1/0/3 为路由器角色。
[DeviceB] interface ten-gigabitethernet 1/0/3 [DeviceB-Ten-GigabitEthernet1/0/3] ipv6 nd raguard role router [DeviceB-Ten-GigabitEthernet1/0/3] quit验证配置
4.
完成上述配置后：
• 从接口 Ten-GigabitEthernet1/0/2 收到的 RA 报文，会匹配 RA Guard 策略 policy1：
如果匹配失败则丢弃；
(cid:123)
如果匹配成功，报文会被转发到 VLAN 10 下其他接口。
(cid:123)
• 从接口 Ten-GigabitEthernet1/0/1 收到的 RA 报文，不会匹配 RA Guard 策略 policy1，RA 报文都被直接丢弃。
对于接口 Ten-GigabitEthernet1/0/3收到的 RA报文，不会和策略 policy1下的规则进行匹配，
•报文都直接被转发，在同一 的其他接口也会收到此 报文。
RA VLAN RA

## 21-uRPF配置

目 录简介

### 1 uRPF

1 uRPF

#### 1.1 uRPF简介

uRPF（unicast Forwarding，单播反向路径转发）是一种单播逆向路由查找技术，用Reverse Path来防范基于源地址欺骗的攻击手段，例如基于源地址欺骗的 DoS（Denial of Service，拒绝服务）
攻击和 DDoS（Distributed Denial of Service，分布式拒绝服务）攻击。

##### 1.1.1 uRPF应用场景

对于使用基于 地址验证的应用来说，基于源地址欺骗的攻击手段可能导致未被授权用户以他IPv4人，甚至是管理员的身份获得访问系统的权限。因此即使响应报文没有发送给攻击者或其它主机，此攻击方法也可能会造成对被攻击对象的破坏。
图1-1 源地址欺骗攻击示意图如 图 1-1 所示，攻击者在Router A上伪造并向Router B发送大量源地址为 2.2.2.1 的报文，Router B响应这些报文并向真正的“2.2.2.1”（Router C）回复报文。因此这种非法报文对Router B和Router C都造成了攻击。如果此时网络管理员错误地切断了Router C的连接，可能会导致网络业务中断甚至更严重的后果。
攻击者也可以同时伪造不同源地址的攻击报文或者同时攻击多个服务器，从而造成网络阻塞甚至网络瘫痪。
uRPF 可以有效防范上述攻击。一般情况下，设备在收到报文后会根据报文的目的地址对报文进行转发或丢弃。而 可以在转发表中查找报文源地址对应的接口是否与报文的入接口相匹配，如uRPF果不匹配则认为源地址是伪装的并丢弃该报文，从而有效地防范网络中基于源地址欺骗的恶意攻击行为的发生。

##### 1.1.2 uRPF检查方式

检查有严格（strict）型和松散（loose）型两种。
uRPF

###### 1. 严格型uRPF检查

不仅检查报文的源地址是否在转发表中存在，而且检查报文的入接口与转发表是否匹配。
在一些特殊情况下（如非对称路由，即设备上行流量的入接口和下行流量的出接口不相同），严格型 uRPF 检查会错误地丢弃非攻击报文。
一般将严格型 uRPF 检查布置在 ISP 的用户端和 ISP 端之间。
严格型 uRPF 不能与等价路由功能同时使用，否则匹配等价路由的业务报文无法通过严格型 uRPF的检查，导致业务报文被丢弃。

###### 2. 松散型uRPF检查

仅检查报文的源地址是否在转发表中存在，而不再检查报文的入接口与转发表是否匹配。
松散型 uRPF 检查可以避免错误的拦截合法用户的报文，但是也容易忽略一些攻击报文。
一般将松散型 uRPF 检查布置在 ISP-ISP 端。另外，如果用户无法保证路由对称，可以使用松散型uRPF 检查。

##### 1.1.3 uRPF典型组网应用

图1-2 典型组网应用uRPF ISP B uRPF(loose)
ISP A ISP C uRPF(strict)
User通常在 ISP 上配置 uRPF，在 ISP 与用户端，配置严格型 uRPF 检查，在 ISP 与 ISP 端，配置松散型 uRPF 检查。

#### 1.2 全局开启uRPF

##### 1. 配置限制和指导

全局配置的 对设备的所有接口生效。
uRPF

##### 2. 配置步骤

(1) 进入系统视图。
system-view
(2) 开启全局 uRPF 功能。
ip urpf { loose | strict }
缺省情况下，uRPF 功能处于关闭状态。

#### 1.3 uRPF显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置 uRPF 后的运行情况，通过查看显示信息验证配置的效果。
表1-1 uRPF 显示和维护配置步骤 命令显示uRPF的配置应用情况 display ip urpf [ slot slot-number ]

## 22-SAVI配置

目 录简介配置动态绑定表项的延迟删除时间与 混合场景中的 配置举例

### 1 SAVI

#### 1.4 开启SAVI

1 SAVI

#### 1.1 SAVI简介

SAVI（Source Improvement，源地址有效性验证）特性用来在接入设备上以Address Validation ND Snooping、DHCPv6 Snooping 及 IP Source Guard 中 IPv6 静态绑定表项为依据对源地址为全球单播类型的 IPv6 报文进行检查，避免非法报文通过接入设备进入内部网络。只要报文源地址与某绑定表项匹配，则认为该报文为合法报文，正常转发；否则将该报文丢弃。对于源地址为本地链路地址的 IPv6 报文，设备进行转发时不作 SAVI 检查。

#### 1.2 SAVI典型应用场景

##### 1. DHCPv6-Only场景下的SAVI

在该场景中，主机与配置了 SAVI 的设备相连，只能通过 DHCPv6 方式动态获取地址。SAVI 设备对 DHCPv6 协议报文、ND 协议报文（除了 RA 报文和 RR 报文）和 IPv6 数据报文基于 DHCPv6 Snooping 表项和手工配置的 IPv6 静态绑定表项进行源地址的合法性检查。

##### 2. SLAAC-Only场景下的SAVI

在该场景中，主机与配置了 SAVI 的设备相连，除了能手工配置地址外，只能通过 SLAAC（Stateless Address Autoconfiguration，无状态地址自动配置）方式动态获取地址。SAVI 设备丢弃所有的协议报文，对 协议报文和 数据报文基于 表项和手工配置的DHCPv6 ND IPv6 ND Snooping IPv6静态绑定表项进行源地址的合法性检查。

##### 3. DHCPv6与SLAAC混合场景下的SAVI

在该场景中，主机与配置了 SAVI 的设备相连，除了能手工配置地址外，还可以通过 DHCPv6 和SLAAC 两种方式动态获取地址。SAVI 设备会对 DHCPv6 协议报文、ND 协议报文和 IPv6 数据报文基于 表项、ND 表项和手工配置的 静态绑定表项进行源地址的DHCPv6 Snooping Snooping IPv6合法性检查。

#### 1.3 SAVI配置任务简介

配置任务如下：
SAVI开启SAVI
(1)
配置IPv6
(2) Source Guard配置DHCPv6 Snooping基本功能
(3)
(4) 配置ND相关参数
(5) （可选）配置动态绑定表项的延迟删除时间开启
1.4 SAVI
(1) 进入系统视图。
system-view

#### 1.5 配置IPv6 Source Guard

(2) 开启 SAVI 功能。
ipv6 savi strict
缺省情况下，SAVI 功能处于关闭状态。
配置IPv6
1.5 Source Guard
(1) 开启 IPv6 接口绑定功能。
(2) （可选）配置 IPv6 静态绑定表项。
IPv6 绑定功能的具体配置请参见“安全配置指导”中的“IP Source Guard”。

#### 1.6 配置DHCPv6 Snooping基本功能

##### 1. 配置限制和指导

SLAAC-Only 场景下，仅开启 DHCPv6 Snooping 功能即可。

##### 2. 配置步骤

开启 功能。
(1) DHCPv6 Snooping配置 信任端口。
(2) DHCPv6 Snooping开启端口的 表项记录功能。
(3) DHCPv6 Snooping DHCPv6 Snooping 基本功能的具体配置请参见“三层技术-IP 业务配置指导”中的“DHCPv6 Snooping”。

#### 1.7 配置ND相关参数

##### 1. 配置限制和指导

DHCPv6-Only 场景下，仅开启 ND Detection 功能即可。

##### 2. 配置步骤

(1) 开启学习表项地址类型为全球单播地址的 ND Snooping 表项的功能。ND Snooping 表项的具
体配置请参见“三层技术-IP 业务配置指导”中的“IPv6 基础”。
开启 功能。ND 功能的具体配置请参见“安全配置指导”中的“ND
(2) ND Detection Detection
攻击防御”。
(3) 配置 ND 信任端口。ND 信任端口的具体配置请参见“安全配置指导”中的“ND 攻击防
御”。

#### 1.8 配置动态绑定表项的延迟删除时间

##### 1. 功能简介

开启 功能后，如果端口在 状态的持续时间超过所配置的延迟删除时间，系统将会删除SAVI down该端口上相关的 DHCPv6 Snooping 表项和 ND Snooping 表项。

##### 2. 配置步骤

(1) 进入系统视图。

system-view
(2) 配置动态绑定表项的延迟删除时间。
ipv6 savi down-delay delay-time缺省情况下，端口状态为 down 后动态绑定表项的延迟删除时间为 30 秒。

#### 1.9 SAVI典型配置举例

##### 1.9.1 DHCPv6-Only场景中的SAVI配置举例

###### 1. 组网需求

如 图 1-1 所示，在Switch上配置SAVI，满足如下用户需求：
• DHCPv6 客户端只能通过 DHCPv6 方式获取 IPv6 地址。
• 从端口 Ten-GigabitEthernet1/0/2 和 Ten-GigabitEthernet1/0/3 上收到的 DHCPv6 协议报文、ND 协议报文（除 RA、RR 报文）和 IPv6 数据报文基于 DHCPv6 Snooping 绑定表项做源地址的合法性检查。

###### 2. 组网图

图1-1 配置 场景组网图DHCPv6-Only

###### 3. 配置步骤

\# 开启 SAVI 功能。
<Switch> system-view [Switch] ipv6 savi strict \# 将端口 Ten-GigabitEthernet1/0/1、Ten-GigabitEthernet1/0/2 和 Ten-GigabitEthernet1/0/3 加入VLAN 2。
[Switch] vlan 2 [Switch-vlan2] port ten-gigabitethernet 1/0/1 ten-gigabitethernet 1/0/2 ten-gigabitethernet 1/0/3 [Switch-vlan2] quit \# 开启 DHCPv6 Snooping 功能。
[Switch] ipv6 dhcp snooping enable

\# 配置 Ten-GigabitEthernet1/0/1 端口为 DHCPv6 Snooping 信任端口。
[Switch] interface ten-gigabitethernet 1/0/1 [Switch-Ten-GigabitEthernet1/0/1] ipv6 dhcp snooping trust [Switch-Ten-GigabitEthernet1/0/1] quit \# 在端口 Ten-GigabitEthernet1/0/2 和 Ten-GigabitEthernet1/0/3 开启 DHCPv6 Snooping 表项记录功能。
[Switch] interface ten-gigabitethernet 1/0/2 [Switch-Ten-GigabitEthernet1/0/2] ipv6 dhcp snooping binding record [Switch-Ten-GigabitEthernet1/0/2] quit [Switch] interface ten-gigabitethernet 1/0/3 [Switch-Ten-GigabitEthernet1/0/3] ipv6 dhcp snooping binding record [Switch-Ten-GigabitEthernet1/0/3] quit开启 功能。
\# ND Detection [Switch] vlan 2 [Switch-vlan2] ipv6 nd detection enable [Switch-vlan2] quit在端口 和 上开启 接口绑定功能。
\# Ten-GigabitEthernet1/0/2 Ten-GigabitEthernet1/0/3 IPv6 [Switch] interface ten-gigabitethernet 1/0/2 [Switch-Ten-GigabitEthernet1/0/2] ipv6 verify source ip-address mac-address [Switch-Ten-GigabitEthernet1/0/2] quit [Switch] interface ten-gigabitethernet 1/0/3 [Switch-Ten-GigabitEthernet1/0/3] ipv6 verify source ip-address mac-address [Switch-Ten-GigabitEthernet1/0/3] quit

##### 1.9.2 SLAAC-Only场景中的SAVI配置举例

###### 1. 组网需求

如 图 所示，在Switch B上配置SAVI，满足如下用户需求：
1-2主机只能通过无状态地址自动配置方式获取地址。
•内端口收到的所有 协议报文被丢弃。
• VLAN 2 DHCPv6从端口 和 上收到的 协议报文和
• Ten-GigabitEthernet1/0/1 Ten-GigabitEthernet1/0/2 ND IPv6数据报文基于 ND Snooping 绑定表项做源地址合法性的检查。

###### 2. 组网图

图1-2 配置 SLAAC-Only 场景组网图Internet Gateway Switch A GE1/0/3 Vlan-int2 10::1 VLAN 2 ND snooping GE1/0/3 Switch B GE1/0/1 GE1/0/2 Host A Host B

###### 3. 配置步骤

\# 开启 SAVI 功能。
<SwitchB> system-view [SwitchB] ipv6 savi strict \# 将端口 Ten-GigabitEthernet1/0/1、Ten-GigabitEthernet1/0/2 和 Ten-GigabitEthernet1/0/3 加入2。
VLAN [SwitchB] vlan 2 [SwitchB-vlan2] port ten-gigabitethernet 1/0/1 ten-gigabitethernet 1/0/2 ten-gigabitethernet 1/0/3 [SwitchB-vlan2] quit开启 下的全球单播类型地址的 功能和 功能。
\# VLAN 2 ND Snooping ND Detection [SwitchB] vlan 2 [SwitchB-vlan2] ipv6 nd snooping enable global [SwitchB-vlan2] ipv6 nd detection enable [SwitchB-vlan2] quit \# 开启 DHCPv6 Snooping 功能来禁止 DHCPv6 协议报文转发。
[SwitchB] ipv6 dhcp snooping enable \# 配置端口 Ten-GigabitEthernet1/0/3 为 ND 信任端口。
[SwitchB] interface ten-gigabitethernet 1/0/3 [SwitchB-Ten-GigabitEthernet1/0/3] ipv6 nd detection trust [SwitchB-Ten-GigabitEthernet1/0/3] quit \# 在端口 Ten-GigabitEthernet1/0/1 和 Ten-GigabitEthernet1/0/2 上开启 IPv6 接口绑定功能。
[SwitchB] interface ten-gigabitethernet 1/0/1 [SwitchB-Ten-GigabitEthernet1/0/1] ipv6 verify source ip-address mac-address

###### 1. 组网需求

###### 3. 配置步骤

[SwitchB-Ten-GigabitEthernet1/0/1] quit [SwitchB] interface ten-gigabitethernet 1/0/2 [SwitchB-Ten-GigabitEthernet1/0/2] ipv6 verify source ip-address mac-address [SwitchB-Ten-GigabitEthernet1/0/2] quit

##### 1.9.3 DHCPv6与SLAAC混合场景中的SAVI配置举例

组网需求
1.
如 图 1-3 所示，在Switch B上配置SAVI，满足如下用户需求：
• 主机可以通过 DHCPv6 方式和无状态地址自动配置方式获取地址。
• 从端口 Ten-GigabitEthernet1/0/3、Ten-GigabitEthernet1/0/4 和 Ten-GigabitEthernet1/0/5 上收到的 DHCPv6 协议报文、ND 协议报文和 IPv6 数据报文基于 DHCPv6 Snooping 绑定表项和 绑定表项做源地址合法性检查。
ND Snooping

###### 2. 组网图

图1-3 配置 DHCPv6 与 SLAAC 混合场景组网图Switch A DHCPv6 server Gateway VLAN 2 GE1/0/2 GE1/0/1 ND snooping DHCPv6 snooping Switch B GE1/0/3 GE1/0/4 GE1/0/5 DHCPv6 Host A Host B client配置步骤
3.
\# 开启 SAVI 功能。
<SwitchB> system-view [SwitchB] ipv6 savi strict \# 将 端 口 Ten-GigabitEthernet1/0/1 、 Ten-GigabitEthernet1/0/2 、 Ten-GigabitEthernet1/0/3 、和 加入 2。
Ten-GigabitEthernet1/0/4 Ten-GigabitEthernet1/0/5 VLAN [SwitchB] vlan 2 [SwitchB-vlan2] port ten-gigabitethernet 1/0/1 ten-gigabitethernet 1/0/2 ten-gigabitethernet 1/0/3 ten-gigabitethernet 1/0/4 ten-gigabitethernet 1/0/5 \# 开启 DHCPv6 Snooping 功能。
[SwitchB] ipv6 dhcp snooping enable在端口 Ten-GigabitEthernet1/0/3、Ten-GigabitEthernet1/0/4 和 开启\# Ten-GigabitEthernet1/0/5 DHCPv6 Snooping 表项记录功能。

[SwitchB] interface ten-gigabitethernet 1/0/3 [SwitchB-Ten-GigabitEthernet1/0/3] ipv6 dhcp snooping binding record [SwitchB-Ten-GigabitEthernet1/0/3] quit [SwitchB] interface ten-gigabitethernet 1/0/4 [SwitchB-Ten-GigabitEthernet1/0/4] ipv6 dhcp snooping binding record [SwitchB-Ten-GigabitEthernet1/0/4] quit [SwitchB] interface ten-gigabitethernet 1/0/5 [SwitchB-Ten-GigabitEthernet1/0/5] ipv6 dhcp snooping binding record [SwitchB-Ten-GigabitEthernet1/0/5] quit \# 配置端口 Ten-GigabitEthernet1/0/1 为 DHCPv6 Snooping 信任端口。
[SwitchB] interface ten-gigabitethernet 1/0/1 [SwitchB-Ten-GigabitEthernet1/0/1] ipv6 dhcp snooping trust [SwitchB-Ten-GigabitEthernet1/0/1] quit \#开启 VLAN 2 下的全球单播类型地址的 ND Snooping 功能和 ND Detection 功能。
[SwitchB] vlan 2 [SwitchB-vlan2] ipv6 nd snooping enable global [SwitchB-vlan2] ipv6 nd detection enable [SwitchB-vlan2] quit \# 配置 Ten-GigabitEthernet1/0/2 端口为 ND detection 信任端口。
[SwitchB] interface ten-gigabitethernet 1/0/2 [SwitchB-Ten-GigabitEthernet1/0/2] ipv6 nd detection trust [SwitchB-Ten-GigabitEthernet1/0/2] quit \# 在端口 Ten-GigabitEthernet1/0/3、Ten-GigabitEthernet1/0/4 和 Ten-GigabitEthernet1/0/5 上开启IPv6 接口绑定功能。
[SwitchB] interface ten-gigabitethernet 1/0/3 [SwitchB-Ten-GigabitEthernet1/0/3] ipv6 verify source ip-address mac-address [SwitchB-Ten-GigabitEthernet1/0/3] quit [SwitchB] interface ten-gigabitethernet 1/0/4 [SwitchB-Ten-GigabitEthernet1/0/4] ipv6 verify source ip-address mac-address [SwitchB-Ten-GigabitEthernet1/0/4] quit [SwitchB] interface ten-gigabitethernet 1/0/5 [SwitchB-Ten-GigabitEthernet1/0/5] ipv6 verify source ip-address mac-address

## 23-MFF配置

目 录简介开启 功能显示和维护环型组网配置举例

### 1 MFF

1 MFF

#### 1.1 MFF简介

MFF（MAC-Forced Forwarding，MAC 强制转发）可实现广播域内终端设备间的二层隔离和三层互通而无须划分 VLAN 或为每个 VLAN 规划不同的 IP 网段。MFF 通过 ARP 代答机制，强制终端设备将所有流量（包括同一子网内的流量）发送到网关，使网关可以监控数据流量，防止终端设备之间的恶意攻击。

##### 1.1.1 MFF组网应用

如 1.1.1 所示，Switch A和Switch B作为EAN（Ethernet Access Node，以太网接入节点），提供了终端设备与汇聚节点（Switch C）之间的连接。在以太网接入节点上配置MFF功能，可以使终端设备的数据报文交互全部通过Gateway转发，实现了终端设备之间的三层互通，又保证了二层数据的隔离，即：终端设备不会了解相互的MAC地址。
图1-1 应用组网图MFF 通常与其他功能配合使用，在以太网接入节点上实现终端设备的流量过滤、二层隔离和三层互通，提高接入层网络的安全性。和 MFF 配合使用的特性包括：
• ARP Snooping，关于 ARP Snooping 功能的介绍，请参见“三层技术-IP 业务配置指导”中的“ARP Snooping”。
Guard，关于 功能的介绍，请参见“安全配置指导”中的“IP
• IP Source IP Source Guard Source Guard”。
• ARP Detection，关于 ARP Detection 功能的介绍，请参见“安全配置指导”中的“ARP Detection”。
• VLAN 映射，关于 VLAN 映射功能的介绍，请参见“二层技术-以太网交换配置指导”中的“VLAN 映射”。

##### 1.1.2 MFF端口角色

设备上开启 功能的 内存在两种端口角色：用户端口及网络端口。
MFF VLAN

###### 1. 用户端口

MFF 的用户端口是指直接连接终端设备的端口。
用户端口上对于不同的报文处理如下：
• 允许组播报文通过；
对于 报文则上送 进行处理；
• ARP CPU对于单播报文，处理如下：
•若已经学习到网关 地址，则仅允许目的 地址为网关 地址的单播报文通过，MAC MAC MAC (cid:123)
其他报文都将被丢弃；
若没有学习到网关 MAC 地址，所有单播报文都将被丢弃。
(cid:123)

###### 2. 网络端口

MFF 的网络端口是指连接其他网络设备如接入交换机、汇聚交换机、网关或服务器的端口。
网络端口上对于不同的报文处理如下：
• 允许组播报文通过；
• 对于 ARP 报文则上送 CPU 进行处理；
• 拒绝其他广播报文通过。

##### 1.1.3 MFF的ARP代答机制

MFF 环境下的终端设备之间的三层互通是通过 ARP 代答机制实现的，这种代答机制在一定程度上减少了网络侧和用户侧之间的广播报文数量。
设备对 报文进行如下处理：
MFF ARP代答终端设备 请求。代替网关给终端设备回应 报文，使终端设备之间的报文交互
• ARP ARP都通过网关进行三层转发。终端设备的 ARP 请求，既包括对于网关的请求，也包括对于其他终端设备 IP 的 ARP 请求。
• 代答网关 ARP 请求。代替终端设备给网关回应 ARP 报文。如果网关请求的表项在 MFF 设备上存在，就根据表项进行代答。如果表项还没有建立，则转发请求。以达到减少广播的目的。
• 转发终端设备和网关发来的 ARP 应答。
• 监听网络中的 ARP 报文。更新网关 IP 地址和 MAC 地址对应表并广播。

##### 1.1.4 MFF的缺省网关

只适用于用户静态配置 地址的组网环境，因此 无法通过 报文自动获取网关信MFF IP MFF DHCP息，只能通过配置 mac-forced-forwarding default-gateway 命令手工指定缺省网关。MFF在一个 VLAN 下只支持维护一个缺省网关。当 MFF 学习到缺省网关的 MAC 地址后，如果收到来自缺省网关的 报文中的源 地址与当前记录的缺省网关 地址不同， 会自动更新记ARP MAC MAC MFF录的缺省网关 MAC 地址。

#### 1.3 开启MFF功能

##### 2. 配置准备

##### 1.1.5 协议规范

4562：MAC-Forced
• RFC Forwarding

#### 1.2 MFF配置任务简介

MFF 配置任务如下：
(1) 开启MFF功能
(2) 配置网络端口
(3) （可选）配置对MFF维护的网关进行定时探测
(4) 配置网络中部署的服务器的IP地址如果网络中部署了服务器，就需要在开启 MFF 功能的设备的服务器列表中添加此服务器的 IP地址，否则，终端设备与服务器之间不能进行通信。
开启 功能
1.3 MFF

##### 1. 配置限制和指导

• 终端设备与配置了 MFF 功能的设备之间是隔离的，即不能 ping 通。
• IP Source Guard 静态绑定表项和 MFF 配合使用时，必须配置 VLAN 信息。若不配置 VLAN
信息，符合 IP Source Guard 条件的 IP 报文在不匹配 MFF 网关 MAC 情况下也会允许通过。
• MFF 不支持网关的 VRRPE 组网应用。
配置准备
2.
在开启 MFF 的 VLAN 中需要同时开启 ARP Snooping 功能，以便 MFF 根据 ARP Snooping 表项应
答终端用户的 请求。
ARP

##### 3. 配置步骤

(1) 进入系统视图。
system-view
进入 视图。
(2) VLAN
vlan vlan-id
开启 功能。
(3) MFF
mac-forced-forwarding default-gateway gateway-ip
缺省情况下，MFF 功能处于关闭状态。

#### 1.4 配置网络端口

##### 1. 配置限制和指导

开启 MFF 的 VLAN 内，设备上行连接网关的端口以及连接其他 MFF 设备的端口，都应该配置为网络端口。

##### 2. 配置步骤

##### 1. 功能简介

在开启 MFF 的 VLAN 内，只有网络端口支持链路聚合，用户端口不支持链路聚合。即网络端口可以加入链路聚合组，而用户端口不能加入链路聚合组。关于链路聚合的介绍请参见“二层技术-以太网交换配置指导”中的“以太网链路聚合”。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 进入接口视图。
interface interface-type interface-number
(3) 配置网络端口。
mac-forced-forwarding network-port缺省情况下，端口为用户端口。

#### 1.5 配置对MFF维护的网关进行定时探测

功能简介
1.
对 MFF 维护的网关进行定时探测，可以感知网关 MAC 地址的变化。
对网关进行定时探测的时间间隔为 30 秒。探测使用伪造 ARP 报文，其源 IP 地址为 0.0.0.0，源 MAC地址为设备桥 地址。
MAC

##### 2. 配置步骤

(1) 进入系统视图。
system-view
进入 视图。
(2) VLAN
vlan vlan-id
开启网关定时探测功能。
(3)
mac-forced-forwarding gateway probe
缺省情况下，网关定时探测功能处于关闭状态。

#### 1.6 配置网络中部署的服务器的IP地址

##### 1. 功能简介

服务器 IP 地址可以是 VRRP 备份组中某个路由器的接口 IP 地址，也可以是相关业务的服务器的 IP地址（如 RADIUS 服务器）。
如果 MFF 设备的网络端口收到了源 IP 地址为服务器 IP 地址的 ARP 请求，则查询本设备记录的用户信息，利用查询到的用户信息代替客户端应答给服务器。即客户端发送给服务器的报文，都会通过网关进行转发，而服务器发送给终端设备的报文，则不需经过网关转发。
不检查服务器的 地址和网关 地址是否在同一个网段，只检查是否是全 或全 的 地MFF IP IP 0 1 IP址，全 0 或全 1 的 IP 地址不能作为服务器 IP 地址进行配置。

###### 1. 组网需求

##### 2. 配置限制和指导

为了防止 MFF 设备的网络接口拦截服务器发送的 ARP 报文，必须将服务器发送 ARP 报文时填充的源 IP 地址加入到 MFF 设备的服务器 IP 地址列表中。

##### 3. 配置步骤

进入系统视图。
(1)
system-view
(2) 进入 VLAN 视图。
vlan vlan-id
(3) 配置网络中部署的服务器的 IP 地址。
mac-forced-forwarding server server-ip&<1-10>缺省情况下，未配置网络中部署的服务器的 IP 地址。

#### 1.7 MFF显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 MFF 的运行情况，通过查看显示信息验证配置的效果。
表1-1 MFF 显示和维护操作 命令显示MFF端口配置信息 display mac-forced-forwarding interface显示指定VLAN的MFF信息 display mac-forced-forwarding vlan vlan-id

#### 1.8 MFF典型配置举例

##### 1.8.1 树型组网配置举例

组网需求
1.
如 图 1-2 所示，Host A、Host B和Host C配置静态IP地址，所有设备都在VLAN 100 内。为了实现主机之间二层隔离，同时又可以通过 Gateway 进行三层互通，在 Switch A 和 Switch B 上开启 MFF 功能。为了实现主机与Server互通，需要手工配置网络中部署服务器的IP地址。Switch A和Switch B通过Switch C连接到Gateway。Gateway的IP地址为 10.1.1.100/24，Server和网络相连的网卡的IP地址为 10.1.1.200/24。

###### 2. 组网图

图1-2 树型组网图Switch C Switch A Gateway XGE1/0/2 XGE1/0/1 XGE1/0/2 XGE1/0/1
10.1.1.100/24 Host A XGE1/0/3 XGE1/0/3
10.1.1.1/24 Host B
10.1.1.2/24 XGE1/0/1 XGE1/0/2 Host C Switch B Server
10.1.1.3/24 10.1.1.200/24

###### 3. 配置步骤

如 图 配置客户端和Gateway的静态IP地址
(1) 1-2配置
(2) Switch A在 上开启 功能。
\# VLAN 100 MFF [SwitchA] vlan 100 [SwitchA-vlan100] mac-forced-forwarding default-gateway 10.1.1.100 \# 配置网络中部署的服务器的 IP 地址为 10.1.1.200。
[SwitchA-vlan100] mac-forced-forwarding server 10.1.1.200在 上开启 功能。
\# VLAN 100 ARP Snooping [SwitchA-vlan100] arp snooping enable [SwitchA-vlan100] quit \# 配置 Ten-GigabitEthernet1/0/1 为网络端口。
[SwitchA] interface ten-gigabitethernet 1/0/1 [SwitchA-Ten-GigabitEthernet1/0/1] mac-forced-forwarding network-port
(3) 配置 Switch B \# 在 VLAN 100 上开启 MFF 功能。
[SwitchB] vlan 100 [SwitchB-vlan100] mac-forced-forwarding default-gateway 10.1.1.100 \# 配置网络中部署的服务器的 IP 地址为 10.1.1.200。
[SwitchB-vlan100] mac-forced-forwarding server 10.1.1.200 \# 在 VLAN 100 上开启 ARP Snooping 功能。
[SwitchB-vlan100] arp snooping enable [SwitchB-vlan100] quit \# 配置 Ten-GigabitEthernet1/0/2 为网络端口。
[SwitchB] interface ten-gigabitethernet 1/0/2 [SwitchB-Ten-GigabitEthernet1/0/2] mac-forced-forwarding network-port

###### 1. 组网需求

##### 1.8.2 环型组网配置举例

组网需求
1.
如 图 1-3 所示，Host A、Host B和Host C配置静态IP地址，网络中存在环路，所有设备都在VLAN 100内。为了实现主机之间二层隔离，同时又可以通过Gateway进行三层互通，在Switch A和Switch B上开启MFF功能。为了实现主机与Server互通，需要手工配置网络中部署服务器的IP地址。Switch A和Switch B通过Switch C连接到Gateway。Gateway的IP地址为 10.1.1.100/24，Server和网络相连的网卡的IP地址为 10.1.1.200/24。

###### 2. 组网图

图1-3 环型组网图

###### 3. 配置步骤

如 图 配置客户端和Gateway的静态IP地址
(1) 1-3
(2) 配置 Switch A \# 开启全局 STP 协议，保证接口下 STP 协议处于开启状态。
[SwitchA] stp global enable \# 在 VLAN 100 上开启 MFF 功能。
[SwitchA] vlan 100 [SwitchA-vlan100] mac-forced-forwarding default-gateway 10.1.1.100 \# 配置网络中部署的服务器的 IP 地址为 10.1.1.200。
[SwitchA-vlan100] mac-forced-forwarding server 10.1.1.200 \# 在 VLAN 100 上开启 ARP Snooping 功能。
[SwitchA-vlan100] arp snooping enable [SwitchA-vlan100] quit \# 配置 Ten-GigabitEthernet1/0/2 和 Ten-GigabitEthernet1/0/3 为网络端口。
[SwitchA] interface ten-gigabitethernet 1/0/2 [SwitchA-Ten-GigabitEthernet1/0/2] mac-forced-forwarding network-port [SwitchA-Ten-GigabitEthernet1/0/2] quit [SwitchA] interface ten-gigabitethernet 1/0/3 [SwitchA-Ten-GigabitEthernet1/0/3] mac-forced-forwarding network-port

(3) 配置 Switch B
\# 开启全局 STP 协议，保证接口下 STP 协议处于开启状态。
[SwitchB] stp global enable
\# 在 VLAN 100 上开启 MFF 功能。
[SwitchB] vlan 100
[SwitchB-vlan100] mac-forced-forwarding default-gateway 10.1.1.100
\# 配置网络中部署的服务器的 IP 地址为 10.1.1.200。
[SwitchB-vlan100] mac-forced-forwarding server 10.1.1.200
\# 在 VLAN 100 上开启 ARP Snooping 功能。
[SwitchB-vlan100] arp snooping enable
[SwitchB-vlan100] quit
\# 配置 Ten-GigabitEthernet1/0/1 和 Ten-GigabitEthernet1/0/3 为网络端口。
[SwitchB] interface ten-gigabitethernet 1/0/1
[SwitchB-Ten-GigabitEthernet1/0/1] mac-forced-forwarding network-port
[SwitchB-Ten-GigabitEthernet1/0/1] quit
[SwitchB] interface ten-gigabitethernet 1/0/3
[SwitchB-ten-gigabitethernet 1/0/3] mac-forced-forwarding network-port
(4) 配置 Switch C
\# 开启全局 STP 协议，保证接口下 STP 协议处于开启状态。
<SwitchC> system-view
[SwitchC] stp global enable

## 24-加密引擎配置

目 录加密引擎简介

### 1 加密引擎

1加密引擎

#### 1.1 加密引擎简介

加密引擎是专门用于提供数据加/解密服务的硬件及软件的统称。目前设备仅支持软件加密引擎，且软件加密引擎功能始终开启，不可配置。加密引擎可以为需要加密的业务模块服务，与业务模块的交互过程是：各业务模块将需要加/解密的数据发送给加密引擎，加密引擎对数据进行加/解密处理，然后加密引擎将处理后的数据发送回各业务模块。

#### 1.2 加密引擎显示和维护

在任意视图下执行 命令可以显示加密引擎的运行情况，通过查看显示信息验证配置的效display果。
在用户视图下执行 reset 命令可以清除加密引擎的统计信息。
表1-1 加密引擎显示和维护操作 命令显示加密引擎的基本信息 display crypto-engine display crypto-engine statistics [ engine-id engine-id slot显示加密引擎的统计信息slot-number ] reset crypto-engine statistics [ engine-id engine-id slot清除加密引擎的统计计数slot-number ]

## 25-FIPS配置

目 录简介配置限制和指导退出 模式自动重启设备进入 模式

### 1 FIPS

1 FIPS

#### 1.1 FIPS简介

FIPS（Federal Standards，联邦信息处理标准）140-2 是 NIST（National Information Processing Institute of Standards and Technology，美国国家标准与技术研究院）颁布的针对密码算法安全的一个标准，它规定了一个安全系统中的密码模块应该满足的安全性要求。

##### 1.1.1 FIPS的安全级别

定义了四个安全级别：Level 1、Level 2、Level 和 4，它们安全等级依次递增，FIPS 140-2 3 Level可广泛适用于密码模块的各种应用环境。目前，设备支持 Level 2 级别的 FIPS 140-2。
若无特殊说明，本文中的 FIPS 即表示 Level 2 级别的 FIPS 140-2。

##### 1.1.2 FIPS的作用

在 FIPS 模式下，设备具有更为严格的安全性要求，并会对密码模块进行相应的自检处理，以确认其处于正常运行状态。
进入 模式的设备同时也符合 CC（Common Criteria，公共准则）中的 NDPP（Network FIPS Device Protection Profile，网络设备保护特性）定义的功能要求。

##### 1.1.3 FIPS密码算法自检处理

设备进入 FIPS 模式之后，为确保密码算法模块的功能正常运行，系统会进行自检处理，具体包括启动自检、条件自检。启动自检失败后，自检进程所在的设备自动重启。条件自检失败后，自检进程所在的设备不重启，但系统会输出密码算法自检失败的提示信息。
如果自检失败，请联系售后技术服务工程师解决。

###### 1. 启动自检（Power-up Self-tests）

启动自检是在设备启动过程中对 允许使用的密码算法进行的自检。
FIPS启动自检包括：
KAT（Known-answer Test，已知结果测试）：即使用密码算法对已知的密钥和明文进行运算，
•如果运算结果与已知结果相同，则表示该算法的启动自检通过，否则表示自检失败。
• PWCT（Pairwise Conditional Test，密钥对有效性测试）
签名和验证：生成 非对称密钥对时进行的自检，具体为，首先使用私DSA/RSA/ECDSA (cid:123)
钥对指定数据进行签名，然后使用公钥对该签名数据进行验证，如果解密成功，则表示自检通过，否则自检失败。

加密和解密：生成 RSA 非对称密钥对时进行的自检，具体为，首先使用公钥加密任意一(cid:123)
段明文，然后使用对应的私钥对生成的密文进行解密，如果解密成功，则表示自检通过，否则自检失败。
启动自检具体内容如 表 1-1 所示。
表1-1 启动自检列表启动自检类型 自检操作对以下软件加密算法进行自检：
• SHA1、SHA224、SHA256、SHA384、SHA512（KAT）
• HMAC-SHA1、HMAC-SHA224、HMAC-SHA256、HMAC-SHA384、HMAC-SHA512（KAT）
• AES（KAT）
• RSA 签名和验证（KAT）
• 签名和验证（PWCT）
RSA软件加密算法自检
• RSA 加密和解密（ PWCT ）
• 签名和验证（PWCT）
DSA
• ECDSA 签名和验证（PWCT）
• DRBG（KAT）
• ECDH（KAT）
• GCM（KAT）
• GMAC（KAT）

###### 2. 条件自检（Conditional Self-tests）

条件自检是在非对称密码模块和随机数生成模块被使用时进行的自检，具体包括以下两种测试：
• 签名和验证的 PWCT：生成 DSA/RSA 非对称密钥对时进行的自检，具体为，首先使用私钥对指定数据进行签名，然后使用公钥对该签名数据进行验证，如果验证成功，则表示自检通过，否则自检失败。
随机数连续性测试：生成随机数的过程中进行的自检，如果前后两次生成的随机数不同，则
•表示自检通过，否则自检失败。该自检过程也会在生成 DSA/RSA 非对称密钥对时进行。

#### 1.2 FIPS配置限制和指导

##### 1. FIPS模式对密码要求的注意事项

设备重启进入 FIPS 模式之前，系统会自动删除所有非 FIPS 模式下配置的密钥对和不符合
•标准（密钥位数小于 位，签名 算法为 MD5）的数字证书。因此，由非FIPS 2048 HSAH FIPS模式切换到 FIPS 模式后，用户将无法直接通过 SSH 方式登录设备。若需要进行 SSH 登录，必须先在 FIPS 模式下，通过 Console 口登录设备，并创建 SSH 服务器所需的密钥对，才能支持 SSH 用户登录。
登录 FIPS 模式下的设备时使用的用户密码必须符合 Password Control 密码管理策略，例如
•必须符合一定的密码长度策略、密码复杂度策略以及密码老化策略等。其中，密码的老化时间策略需要关注。当密码的使用时间超过老化时间后，系统会要求用户及时更换密码。一般

设备的出厂系统时间比较早，等到进入 FIPS 模式之后再去调整正确的系统时间很可能会导致登录密码在下一次登录系统时过期。

##### 2. FIPS模式下配置回滚的注意事项

• FIPS 模式下的配置支持配置回滚，FIPS 模式与非 FIPS 模式之间的配置也支持配置回滚。需
要注意的是，对 FIPS 模式与非 FIPS 模式之间的配置执行回滚操作后，建议删除登录设备的
本地用户并重新设置登录设备的本地用户（包括密码、用户角色和服务类型等属性），然后保
存当前配置并设置为下次启动配置文件，最后重启设备。重启之后，回滚后的配置才能生效。
此过程期间，请勿退出系统或进行其它操作，否则可能会登录失败。
• 为保证自动重启方式进入的 FIPS 模式与非 FIPS 模式之间的配置成功进行回滚，设备进入
FIPS 模式后请首先保存配置，然后进行其它操作；为保证自动重启方式进入的非 FIPS 模式
与 模式之间的配置成功进行回滚，设备进入非 模式后请首先保存配置，然后进行
FIPS FIPS
其它操作。

##### 3. FIPS模式与IRF

• 建议不要将 FIPS 模式状态不相同的设备进行 IRF 搭建。
• 如果在 IRF 环境下切换 FIPS 模式，需要重新启动整个 IRF 之后才能生效。

##### 4. 进入FIPS模式后功能变化的注意事项

• 仅支持 scheme 类型的用户登录认证方式。
• FTP/TFTP 服务器和客户端功能被禁用。
• Telnet 服务器和客户端功能被禁用。
• HTTP 服务器功能被禁用。
• SNMPv1 和 SNMPv2c 版本的 SNMP 功能被禁用，只允许使用 SNMPv3 版本。
• SSL 服务器功能只支持 TLS1.0、TLS1.1、TLS1.2 协议。
• SSH 服务器功能不兼容 SSHv1 客户端，不支持 DSA 类型的密钥对。
• 仅支持生成 2048 位的 RSA 密钥对和 2048 位的 DSA 密钥对。因此设备作为服务器时，若要
求对客户端进行公钥认证，则客户端的密钥对也需要为 2048 位，否则服务器将会拒绝客户端
的连接。
仅支持 256 位以上的 ECDSA 密钥对。因此设备作为服务器时，若要求对客户端进行公钥认
•
证，则客户端的密钥对也需要为 256 位以上，否则服务器将会拒绝客户端的连接。
SSH、SNMPv3、IPsec 和 不支持 DES、3DES、RC4、MD5 算法。
• SSL
不能关闭全局 功能，即 命令执行后
• Password Control undo password-control enable
不生效。
• 部分特性中的密码设置将具有更严格的安全性要求：
AAA 服务器的共享密钥、IKE 协商的预共享密钥、SNMPv3 用户的认证密钥都必须满足固
(cid:123)
定的要求：密码最小长度为 15，密码元素的最少组合类型为 4（必须包括数字、大写字母、
小写字母以及特殊字符）。
设备管理类本地用户的密码和用户角色切换密码受 Password Control 密码策略的管理，缺
(cid:123)
省要求为：密码最小长度为 15，密码元素的最少组合类型为 4（必须包括数字、大写字母、
小写字母以及特殊字符）。

###### 2. 配置步骤

#### 1.3 进入FIPS模式

##### 1.3.1 FIPS模式进入方式

系统提供了两种启动选择来进入 FIPS 模式：自动重启方式和手动重启方式。
• 自动重启方式下，系统以交互式方式要求用户完成配置下次登录设备所需的用户名和密码，之后自动创建一个 FIPS 缺省配置文件（名称为 fips-startup.cfg），将其指定为下次启动配置文件，然后自动使用 缺省配置文件重启。
FIPS手动重启方式下，系统不自动创建进入 FIPS模式的下次启动配置文件，需要用户手工完成进
•入 FIPS 模式所需的所有必要配置之后，手工重启设备。

##### 1.3.2 配置限制和指导

当系统提示是否使用自动重启方式进入FIPS模式时，若使用组合键<Ctrl+C>退出或用户未在
•秒内做出选择，则相当于输入“n”，设备将通过手动重启方式进入FIPS模式。需要注意30的是，手动重启方式必须完成相关配置准备，具体请参见 1.3.4 手动重启方式进入 FIPS 模式中的配置准备，否则切换为FIPS模式后，无法正常登录。
• 当系统提示是否使用自动重启方式进入 FIPS 模式时，若输入“y”选择自动重启后想退出配置流程，可以使用组合键<Ctrl+C>中断配置流程。配置流程中断后，已输入的开启FIPS模式的命令将不被执行。

##### 1.3.3 自动重启方式进入FIPS模式

###### 1. 配置准备

为避免进入 FIPS 模式之后，登录密码因为 Password Control 密码老化策略的限制而过期，建议在执行 fips mode enable 命令之前确认系统时间正确。
配置步骤
2.
(1) 进入系统视图。
system-view
(2) 开启 FIPS 模式。
fips mode enable缺省情况下，FIPS 模式处于关闭状态。
(3) 系统提示是否使用自动重启方式进入 FIPS 模式，在 30 秒内输入“y”，设备将开始自动配置流程。
(4) 根据命令提示输入登录 FIPS 模式的设备时所使用的用户名和密码。
用户通过交互式方式输入用户名和密码后，设备会自动创建设备管理类本地用户，该用户将会成为 模式中安全管理员（Crypto Officer），其密码必须是大写字母、小写字母、数字FIPS以及特殊字符的组合，且最小长度为 15 位；服务类型为 terminal，角色为 network-admin。
(5) 设备自动重启并进入 FIPS 模式。
进入FIPS模式后，用户只能通过步骤（4）设置的用户名和密码登录运行于FIPS模式的设备。

###### 1. 配置准备

##### 1. 功能简介

##### 2. 配置步骤

##### 1.3.4 手动重启方式进入FIPS模式

配置准备
1.
(1) 为避免进入 FIPS 模式之后，登录密码因为 Password Control 密码老化策略的限制而过期，建议在配置进入 模式使用的本地用户名和密码之前确认系统时间正确。
FIPS
(2) 配置密码管理功能
a. 开启全局 Password Control 功能。
b. 设置全局 Password Control 密码组合类型的个数为 4，每种类型至少 1 个字符；设置全局的密码最小长度为 15。
Password Control关于密码管理功能的详细介绍，请参考“安全配置指导”中的“Password Control”。
配置本地用户
(3)
创建设备管理类本地用户。
a.
b. 配置符合密码管理规则的本地用户密码。
c. 配置用户角色为 network-admin 。
d. 配置服务类型为 terminal。

###### 2. 配置步骤

进入系统视图。
(1)
system-view开启 模式。
(2) FIPS fips mode enable缺省情况下，FIPS 模式处于关闭状态。
执行 fips mode enable 命令之后到系统重启之前的这个时间段，不建议执行除 reboot、以及相应的配置准备之外的其它命令，否则可能会不能达到预期的执行效果。
save根据命令提示选择手动重启。
(3)
保存当前配置文件并设置为下次启动配置文件。
(4)
(5) 删除二进制类型的下次启动配置文件（文件名后缀为“.mdb”）。如果不删除二进制类型的下次启动配置文件，则设备使用二进制配置文件启动时，FIPS 模式下不支持的命令（如果存在于配置文件中）也会被恢复，从而影响 FIPS 模式下系统的正常运行。
(6) 手工重启设备，进入 FIPS 模式。
进入 FIPS 模式后，用户只能通过预先设置的本地用户名和密码登录处于 FIPS 模式的设备。

#### 1.4 手工触发密码算法自检

功能简介
1.
在设备运行过程中，当用户或管理员需要确认当前 FIPS 模式下的系统中的密码算法模块是否正常工作时，可以通过执行命令来手工触发系统进行密码算法自检工作。手工触发的密码算法自检内容与设备启动时自动进行的启动自检内容相同。该自检失败后，设备会自动重启。
配置步骤
2.
(1) 进入系统视图。

system-view
(2) 手工触发密码算法自检。
fips self-test

#### 1.5 退出FIPS模式

##### 1. 功能简介

关闭 模式并重启设备之后，设备会返回到非 的工作模式下。
FIPS FIPS系统提供了两种方式来退出 模式：
FIPS自动重启方式：系统自动创建一个非 缺省配置文件（名称为 non-fips-startup.cfg），同
• FIPS时将其指定为下次启动配置文件，之后自动使用非 FIPS 缺省配置文件重启。重启之后，当前登录用户不需要输入任何信息即可直接登录到非 FIPS 模式的系统。
• 手动重启方式：系统不自动创建进入非 FIPS 模式的下次启动配置文件，需要用户手工完成进入非 FIPS 模式所需的所有必要配置之后，手工重启设备。重启之后，当前登录用户需要根据配置的登录认证方式输入相应的用户信息登录到非 模式的系统。
FIPS从 模式切换到非 模式时，登录设备的缺省认证方式如下，用户也可根据实际情况修改登FIPS FIPS录认证方式：
• 通过 VTY 用户线登录设备时的缺省认证方式为 password。
• 通过 Console 口登录设备时的缺省认证方式均为 none。

##### 2. 自动重启方式退出FIPS模式

(1) 进入系统视图。
system-view
(2) 关闭 FIPS 模式。
undo fips mode enable
缺省情况下，FIPS 模式处于关闭状态。
(3) 根据命令提示选择自动重启退出 FIPS。

##### 3. 手工重启方式退出FIPS模式

(1) 进入系统视图。
system-view
(2) 关闭 FIPS 模式。
undo fips mode enable
缺省情况下，FIPS 模式处于关闭状态。
(3) 设置登录认证方式和登录用户名、密码。
对于当前远程登录的用户，若要登录非 FIPS 模式，则必须在不退出当前用户线的情况下，
(cid:123)
重新设置登录设备的认证方式为 scheme，并设置对应的登录用户和密码（也可使用当前
的登录用户和密码）。
对于当前通过Console口登录的用户，若要登录非FIPS模式的系统，根据用户当前的不同
(cid:123)
登录方式，需要进行不同的设置，如 表 所示。
1-2

###### 1. 组网需求

表1-2 登录方式与设置要求对照表用户当前登录方式 设置要求password设置认证方式为password，并设置对应的登录密码设置认证方式为scheme，并设置对应的登录用户和密码（也可使用当前的登录scheme用户和密码）
none 需要认证方式为none根据命令提示选择手动重启。
(4)
保存当前配置文件并设置为下次启动配置文件。
(5)
删除二进制类型的下次启动配置文件（文件名后缀为“.mdb”）。
(6)
(7) 重启设备。

#### 1.6 FIPS显示和维护

在完成上述配置后，在任意视图下执行 display 命令可以显示配置后 FIPS 模式的状态，通过查看显示信息验证配置的效果。
表1-3 FIPS 的显示和维护操作 命令显示算法库的版本号 display crypto version显示FIPS模式的状态 display fips status

#### 1.7 FIPS典型配置举例

##### 1.7.1 自动重启设备进入FIPS模式

组网需求
1.
自动重启设备进入 FIPS 模式，并采用 Console 口登录 FIPS 模式的设备。

###### 2. 配置步骤

若要保存当前配置，请在开启 模式之前，执行 命令。
\# FIPS save开启 模式，并选择自动重启方式进入 模式。设置用户名为 root，对应的密码为\# FIPS FIPS 12345zxcvb!@#$%ZXCVB。
<Sysname> system-view [Sysname] fips mode enable FIPS mode change requires a device reboot. Continue? [Y/N]:y Reboot the device automatically? [Y/N]:y The system will create a new startup configuration file for FIPS mode. After you set the login username and password for FIPS mode, the device will reboot automatically.
Enter username(1-55 characters):root Enter password(15-63 characters):

###### 1. 组网需求

Confirm password:
Waiting for reboot... After reboot, the device will enter FIPS mode.

###### 3. 验证结果

重启设备后，输入用户名 root 和对应的密码。首次登录时，系统会提示重置密码。重置密码成功后，进入 FIPS 模式的系统。重置的密码必须是大写字母、小写字母、数字以及特殊字符的组合，最小长度为 位，且需要与旧密码不同（具体要求请见系统提示）。
15 Press ENTER to get started.
login: root Password:
First login or password reset. For security reason, you need to change your password. Please enter your password.
old password:
new password:
confirm:
Updating user information. Please wait ... ...
… （略）
<Sysname> \# 显示当前 FIPS 模式状态。
<Sysname> display fips status FIPS mode is enabled.
查看缺省的配置文件内容。
\# <Sysname> more fips-startup.cfg \# password-control enable \# local-user root class manage service-type terminal authorization-attribute user-role network-admin \# fips mode enable \# return <Sysname>

##### 1.7.2 手动重启设备进入FIPS模式

组网需求
1.
手动重启设备进入 FIPS 模式，并采用 Console 口登录 FIPS 模式的设备。

###### 2. 配置步骤

开启全局 功能。
\# Password Control <Sysname> system-view [Sysname] password-control enable \# 设置全局 Password Control 密码组合类型的个数为 4，每种类型至少一个字符。
[Sysname] password-control composition type-number 4 type-length 1

\# 设置全局 Password Control 的密码最小长度为 15。
[Sysname] password-control length 15 \# 添加设备管理类本地用户：用户名为 test、密码为 12345zxcvb!@#$%ZXCVB、用户角色为network-admin，服务类型为 Terminal。
[Sysname] local-user test class manage [Sysname-luser-manage-test] password simple 12345zxcvb!@#$%ZXCVB [Sysname-luser-manage-test] authorization-attribute user-role network-admin [Sysname-luser-manage-test] service-type terminal [Sysname-luser-manage-test] quit开启 模式，并选择手动重启方式进入 模式。
\# FIPS FIPS [Sysname] fips mode enable FIPS mode change requires a device reboot. Continue? [Y/N]:y Reboot the device automatically? [Y/N]:n Change the configuration to meet FIPS mode requirements, save the configuration to the next-startup configuration file, and then reboot to enter FIPS mode.
\# 将当前配置保存到存储介质的根目录，并将该文件设置为下次启动配置文件。
[Sysname] save The current configuration will be written to the device. Are you sure? [Y/N]:y Please input the file name(*.cfg)[flash:/startup.cfg] (To leave the existing filename unchanged, press the enter key):
flash:/startup.cfg exists, overwrite? [Y/N]:y Validating file. Please wait...
Saved the current configuration to mainboard device successfully.
[Sysname] quit删除二进制类型的下次启动配置文件。
\# <Sysname> delete flash:/startup.mdb Delete flash:/startup.mdb?[Y/N]:y Deleting file flash:/startup.mdb...Done.
\# 重启设备。
<Sysname> reboot

###### 3. 验证结果

重启设备后，输入用户名 test 和对应的密码首次登录时，系统会提示重置密码。重置密码成功后，进入 模式的系统。重置的密码必须是大写字母、小写字母、数字以及特殊字符的组合，最小FIPS长度为 15 位，且需要与旧密码不同（具体要求请见系统提示）。
Press ENTER to get started.
login: test Password:
First login or password reset. For security reason, you need to change your pass word. Please enter your password.
old password:
new password:
confirm:
Updating user information. Please wait ... ...
… （略）
<Sysname> \# 显示当前 FIPS 模式状态，可见设备工作在 FIPS 模式下。

###### 2. 配置步骤

<Sysname> display fips status FIPS mode is enabled.

##### 1.7.3 自动重启设备退出FIPS模式

###### 1. 组网需求

当前用户已使用 Console 口登录到 FIPS 模式，要求自动重启设备退出 FIPS 模式。
配置步骤
2.
\# 关闭 FIPS 模式。
[Sysname] undo fips mode enable FIPS mode change requires a device reboot. Continue? [Y/N]:y The system will create a new startup configuration file for non-FIPS mode and then reboot automatically. Continue? [Y/N]:y Waiting for reboot... After reboot, the device will enter non-FIPS mode.

###### 3. 验证结果

重启设备后，用户可直接进入系统。
<Sysname>显示当前 模式状态。
\# FIPS <Sysname> display fips status FIPS mode is disabled.

##### 1.7.4 手动重启设备退出FIPS模式

###### 1. 组网需求

当前用户已使用 SSH 远程登录到 FIPS 模式，用户名为 test、密码为 12345zxcvb!@#$%ZXCVB，要求手动重启设备退出 FIPS 模式。

###### 2. 配置步骤

关闭 模式。
\# FIPS [Sysname] undo fips mode enable FIPS mode change requires a device reboot. Continue? [Y/N]:y The system will create a new startup configuration file for non-FIPS mode, and then reboot automatically. Continue? [Y/N]:n Change the configuration to meet non-FIPS mode requirements, save the configuration to the next-startup configuration file, and then reboot to enter non-FIPS mode.
\# 设置登录 VTY 用户线的登录认证方式为 scheme。
[Sysname] line vty 0 63 [Sysname-line-vty0-63] authentication-mode scheme将当前配置保存到存储介质的根目录，并将该文件设置为下次启动配置文件。
\# [Sysname] save The current configuration will be written to the device. Are you sure? [Y/N]:y Please input the file name(*.cfg)[flash:/startup.cfg] (To leave the existing filename unchanged, press the enter key):
flash:/startup.cfg exists, overwrite? [Y/N]:y Validating file. Please wait...
Saved the current configuration to mainboard device successfully.

[Sysname] quit \# 删除二进制类型的下次启动配置文件。
<Sysname> delete flash:/startup.mdb Delete flash:/startup.mdb?[Y/N]:y Deleting file flash:/startup.mdb...Done.
\# 重启设备。
<Sysname> reboot

###### 3. 验证结果

重启设备后，输入用户名 test 和对应的密码 12345zxcvb!@#$%ZXCVB，进入非 FIPS 模式的系统。
Press ENTER to get started.
login: test Password:
Last successfully login time:…（略）
<Sysname> \# 显示当前 FIPS 模式状态，可见设备工作在非 FIPS 模式下。
<Sysname> display fips status FIPS mode is disabled.
