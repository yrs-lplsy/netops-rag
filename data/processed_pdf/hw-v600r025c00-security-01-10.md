# S1700, S5700, S6700 V600R025C00 配置指南-安全 01-10 PKI配置

## 10 PKI配置

10 PKI 配置

### 10.1 PKI简介

10.2 PKI原理描述
10.3 PKI配置注意事项
10.4 PKI缺省配置
10.5 申请本地证书的预配置
10.6 离线申请证书
10.7 通过CMPv2协议在线申请和更新证书
10.8 配置自签名证书
10.9 验证对端实体证书
10.10 导入导出证书
10.11 维护PKI
10.12 PKI配置举例
10.13 PKI常见配置错误
10.1 PKI 简介
定义
公钥基础设施PKI（Public Key Infrastructure）是一种遵循既定标准的证书管理平台，
它利用公钥技术为所有网络应用提供安全服务，是信息安全技术的核心。
目的
随着网络技术和信息技术的发展，设备间通信时会存在如下问题：
● 通信双方无法确认对方的合法身份。
● 通过网络传输时信息易被窃取和篡改，无法保证信息的安全性。

为了解决上述问题，PKI技术应运而生，其利用公钥技术保证在通信过程中通信双方能够实现身份认证并确保数据完整性，因而得到了广泛的应用。
受益
● 用户角度
– 通过PKI证书认证技术，用户可以验证接入设备的合法性，从而可以保证用户接入安全、合法的网络中。
– 通过PKI加密技术，可以保证网络中传输数据的私密性，数据不会被窥探和篡改。
– 通过PKI签名技术，可以保证网络中传输数据的安全性，未授权的用户无法查看该数据。
● 企业角度
– 可以防止非法用户接入企业网络中。
– 企业分支之间可以建立安全通道，保证企业数据的安全性。

### 10.2 PKI原理描述

#### 10.2.1 PKI基本概念

##### 10.2.1.1 加密

加密就是利用数学方法将明文（需要被隐蔽的数据）转换为密文（不可读的数据），从而达到保护数据的目的。加密算法分为可逆和不可逆两大类，其中可逆算法又可分为对称密钥加密和非对称密钥加密。
不可逆加密顾名思义，不可逆加密是指无法通过密文推测出原本的明文信息，通过比较两个加密后的密文是否相同来校验数据在传输过程中是否被修改。常见的不可逆加密算法为信息摘要算法MD5（Message Digest algorithm 5）、安全散列算法SHA（Secure Hash Algorithm）和需要密钥的散列消息验证码HMAC（Hash Message Authentication Code），其中SHA包括SHA1、SHA256、SHA512等。
对称密钥加密对称密钥加密又称共享密钥加密，是指使用同一个密钥对数据进行加密和解密，包括流加密和分组加密两类。
对称密钥的加解密过程如图10-1所示。

图 10-1 对称密钥加解密过程示意图甲和乙事先协商好对称密钥，具体加解密过程如下：
1. 甲使用对称密钥对明文加密，并将密文发送给乙。
2. 乙接收到密文后，使用对称密钥对密文解密，得到最初的明文。
对称密钥加密的优点是效率高、算法简单、系统开销小，适合加密大量数据。缺点是实现困难且扩展性差，实现困难的原因在于进行安全通信前需要以安全方式进行密钥交换；扩展性差表现在每两个通信用户之间都需要协商密钥，n个用户就需要协商n*(n-1)/2个不同的密钥。
目前比较常用的对称密钥加密算法主要包含DES（Data Encryption Standard）、3DES（Triple Data Encryption Standard）和AES（Advanced Encryption Standard）
算法，这些都属于分组加密算法。
非对称密钥加密非对称密钥加密又称公钥加密，它使用了两个不同的密钥：一个可对外界公开，称为“公钥”；一个只有所有者知道，称为“私钥”。
非对称加密解决了对称密钥的发布和管理问题，通信双方无需事先交换密钥就可进行保密通信。通常以公钥作为加密密钥，以私钥作为解密密钥。由于其他人没有对应的私钥，发送的加密信息仅该用户可以解读，从而实现信息的加密传输。
公钥加解密的过程如图10-2所示。
图 10-2 公钥加解密过程示意图甲事先获得乙的公钥，具体加解密过程如下：

1. 甲使用乙的公钥对明文加密，并将密文发送给乙。
2. 乙收到密文后，使用自己的私钥对密文解密，得到最初的明文。
公钥加密的优点是加密的信息只能用私钥进行解密，无法从一个密钥推导出另一个密
钥，适合对密钥或身份信息等敏感信息加密，在安全性上满足用户的需求。缺点是算
法非常复杂，导致加密大量数据所用的时间较长，而且加密后的报文较长，不利于网
络传输。
目前比较常用的非对称加密算法主要包含DH（Diffie-Hellman）密钥交换、RSA（Ron
Rivest、Adi Shamirh、LenAdleman）、DSA（Digital Signature Algorithm）数字签
名和ECC（Elliptic Curve Cryptography）椭圆曲线加密算法。
国密算法
国密是指经国家密码管理局批准可用于对不涉及国家秘密内容的信息进行加密的国产
密码算法，即商用密码。为了保障商用密码的安全性，国家制定了一系列密码标准，
其中包括了对称加密算法、椭圆曲线非对称加密算法和杂凑（哈希、散列）算法等。
国密算法套件中包含的算法如表10-1所示。PKI中使用的主要是SM2、SM3和SM4算
法。
表 10-1 国密算法套件总览表

| 算法 | 类型 | 功能 | 对应的国际算法 | 是否公开 |
|---|---|---|---|---|
| SM1 | 对称加密 | 分组密码算法 | AES128 | 否，仅以IP核的形式存在于硬件中。 |
| SM2 | 椭圆曲线非对称加密 | ECC加解密，签名验签，密钥交换 | RSA、ECC | 是，已纳入ISO 国际标准。 |
| SM3 | 哈希 | 商用密码应用中的数字签名和验证，消息认证码的生成与验证以及随机数的生成 | SHA256 | 是，已纳入ISO 国际标准。 |
| SM4 | 分组加密 | 分组加解密，在加密算法和解密算法中保持一致，只是解密密钥是加密密钥的逆序 | DES、AES | 是 |
| SM7 | 分组加密 | 分组加解密 | - | 否，仅以IP核的形式存在于硬件中。 |
| SM9 | 基于身份标识的非对称加密 | 标识密码算法：签名校验，密钥交换，密钥封装与加解密 | - | 是，已纳入ISO 国际标准。 |
| ZUC | 流加密 | 祖冲之序列密码算法，一种对称加密算法 | EEA3 & EIA3 | 是 |
| SSF33 | 分组加密 | 分组加解密 | - | 否 |

##### 10.2.1.2 数字信封和数字签名

数字信封数字信封是指发送方采用接收方的公钥加密对称密钥后与密文组合在一起所得的数据。采用数字信封时，接收方需要使用自己的私钥才能打开数字信封，得到对称密钥。数字信封技术结合了对称密钥加密和公钥加密的优点，解决了对称密钥发布和公钥加密速度慢等问题，提高了安全性、扩展性和网络传输效率。
数字信封的加解密过程如图10-3所示。
图 10-3 数字信封的加解密过程示意图甲事先获得乙的公钥，具体加解密过程如下：
1. 甲使用对称密钥对明文进行加密，生成密文信息。
甲使用乙的公钥加密对称密钥，和密文一起生成数字信封。
2.
3. 甲将加密后的对称密钥和密文信息以数字信封的形式发送给乙。
4. 乙接收到甲的加密信息后，使用自己的私钥打开数字信封，得到对称密钥。
5. 乙使用对称密钥对密文信息进行解密，得到最初的明文。
从加解密的过程中可以发现，其实数字信封技术也存在问题，如果攻击者拦截甲的信息，用自己的对称密钥加密伪造的信息，并用乙的公钥加密自己的对称密钥，然后发送给乙。乙收到加密信息后，解密得到的明文会被误认为是甲发送的信息。此时，需要一种方法确保接收方收到的信息就是指定的发送方发送的。
数字签名数字信封无法保证接收方收到的信息就是指定的发送方发送的，数字签名可以解决这个问题。它不但可以验证信息是否被篡改，还可以证明发送方的身份。
数字签名是指发送方用自己的私钥对数字指纹进行加密后所得的数据，接收方需要使用发送方的公钥才能解开数字签名，得到数字指纹。
数字指纹又称信息摘要，是指发送方通过HASH算法对明文信息计算后得出的数据。采用数字指纹时，发送方会将数字指纹和明文一起发送给接收方，接收方用同样的HASH算法对明文计算生成的数字指纹，与收到的数字指纹进行匹配，如果一致，便可确定明文信息没有被篡改。
数字签名的加解密过程如图10-4所示。

图 10-4 数字签名的加解密过程示意图甲事先获得乙的公钥，具体加解密过程如下：
1. 甲使用乙的公钥对明文进行加密，生成密文信息。
2. 甲使用HASH算法对明文进行HASH运算，生成数字指纹。
甲使用自己的私钥对数字指纹进行加密，生成数字签名。
3.
4. 甲将密文信息和数字签名一起发送给乙。
5. 乙使用甲的公钥对数字签名进行解密，得到数字指纹。
6. 乙接收到甲的加密信息后，使用自己的私钥对密文信息进行解密，得到最初的明文。
7. 乙使用HASH算法对明文进行HASH运算，生成数字指纹。
8. 乙将生成的数字指纹与得到的数字指纹进行比较，如果一致，乙接收明文；如果不一致，乙丢弃明文。比较的过程也称为验签。
从加解密的过程中可以看出，数字签名技术不但可以验证信息是否被篡改，还可以证明发送方的身份。数字签名和数字信封技术也可以组合使用。
但是，数字签名技术还有个问题，如果攻击者更改乙的公钥，甲获得的是攻击者的公钥，攻击者拦截乙发送给甲的信息，用自己的私钥对伪造的信息进行数字签名，然后与使用甲的公钥的加密伪造的信息一起发送给甲。甲收到加密信息后，解密得到的明文，并验证明文没有被篡改，则甲始终认为是乙发送的信息。

##### 10.2.1.3 数字证书

数字签名无法确定某个特定的公钥属于特定的拥有者，因为谁都可以生成公钥和私钥，仅凭一个公钥无法判断收到的公钥是不是对方的。因此需要一个安全可信的载体来交换公钥，这个载体就是数字证书。
数字证书简称证书，它是一个经证书授权中心数字签名的文件，包含拥有者的公钥及相关身份信息。
数字证书可以说是网络上的安全护照或身份证，提供的是网络上的身份证明。数字证书技术解决了数字签名技术中无法确定公钥是指定拥有者的问题。
说明设备通过OpenSSL库管理和应用数字证书，目前使用的OpenSSL库版本为3.0.9。

证书结构最简单的证书包含一个公钥、名称以及证书授权中心的数字签名。一般情况下证书中还包括密钥的有效期、颁发者（证书授权中心）的名称和该证书的序列号等信息。证书的结构遵循X.509 v3版本的规范。图10-5展示了一种常见的证书结构。
图 10-5 证书结构示意图证书的各字段解释如下：
● 版本：即使用X.509的版本，目前普遍使用的是v3版本（0x2）。
● 序列号：颁发者分配给证书的一个正整数，同一颁发者颁发的证书序列号各不相同，可与颁发者名称一起作为证书的唯一标识。
● 签名算法：颁发者颁发证书时使用的签名算法。
● 颁发者：颁发该证书的设备名称，必须与颁发者证书中的主体名一致。通常为CA（Certificate Authority，证书颁发中心）服务器的名称。
● 有效期：包含有效的起、止日期，不在有效期范围内的证书为无效证书。
● 主体名：证书拥有者的名称，如果与颁发者相同则该证书是一个自签名证书。
● 公钥信息：用户对外公开的公钥以及公钥算法信息。
● 扩展信息：通常包含证书的用法、CRL的发布地址、OCSP服务器的URL等可选字段。
● 签名：颁发者用私钥对证书信息的签名。
证书签名的形成过程如下：首先，CA使用签名算法中的HASH密码学算法生成证书的摘要信息，然后使用签名算法中的公钥密码学算法，配合CA的私钥对摘要信息进行加密，最终形成签名。这些操作都是证书颁发之前在CA上进行的。
证书分类证书有三种类型，如表10-2所示。

表 10-2 证书类型

| 类型 | 描述 | 说明 |
|---|---|---|
| CA证书 | CA自身的证书。如果有多层级CA，则会形成一个CA 层次结构，最上层的CA是一本自签名证书，即根 CA；如果PKI系统中没有多层级CA，CA证书就是自签名证书。 | 申请者通过验证CA的数字签名从而信任CA，任何申请者都可以得到CA的证书（含公钥），用以验证它所颁发的本地证书。 |
| 本地证书 | CA颁发给申请者的证书。 | - |
| 自签名证书 | ● 自签名证书是用自己的私钥签署的数字证书，证书颁发者和证书主题名相同。 ● 设备缺省内置一本自签名证书，且支持创建新的自签名证书。自签名证书带有签名信息，不需要向其他机构申请签名。 ● 设备支持使用缺省内置的自签名证书颁发本地证书。 | 设备通过生成自签名证书和使用缺省内置的自签名证书颁发本地证书，可以实现简单的证书颁发功能。设备不支持对其生成的自签名证书和使用缺省内置的自签名证书颁发的本地证书进行生命周期管理（如证书更新、证书撤销等），为了确保设备和证书的安全，建议用户替换为自己的本地证书。 |

证书格式设备支持使用以下三种文件格式保存，如表10-3所示。
表 10-3 证书格式

| 格式 | 描述 | 说明 |
|---|---|---|
| PKCS#12 | 以二进制格式保存证书，可以包含私钥，也可以不包含私钥。常用的后缀有.P12 和.PFX。 | 如果证书后缀为.CER或.CRT，可以用记事本打开证书，通过查看证书内容来区分格式。 ● 如果有类似＂-----BEGIN CERTIFICATE-----＂ 和＂-----END CERTIFICATE-----＂的头尾标记，则证书格式为PEM。 ● 如果是乱码，则证书格式为DER。 |
| DER | 以二进制格式保存证书，不包含私钥。常用的后缀有.DER、.CER 和.CRT。 |  |

| 格式 | 描述 | 说明 |
|---|---|---|
| PEM | 以ASCII码格式保存证书，可以包含私钥，也可以不包含私钥。常用的后缀有.PEM、.CER 和.CRT。 |  |

国密证书通常情况下，设备仅会部署一张证书同时用于签名和加密，该证书为单证书，公私钥均由设备负责保存。按照规范，国密需要采用双证书体系，根据证书的使用目的和功能可分为签名证书和加密证书两种，签名证书仅用于验证身份，其公私钥均由设备本身生成并负责保管，签名密钥的用法为Digital Signature, Non-Repudiation，加密证书在密钥协商时使用，其公私钥均由 CA 产生，加密密钥的用法为 Key Encipherment, Data Encipherment, Key Agreement。一般情况下，设备产生签名密钥对，生成只包含公钥信息的签名证书请求后发送签名证书给CA，CA验证设备的签名密钥对，生成加密密钥对和加密证书，设备获得加密证书和私钥的过程如图10-6所示。签名证书和加密证书的密钥对均为SM2密钥对。
图 10-6 国密数字信封的加解密过程示意图
1. CA生成对称密钥，使用设备的签名公钥加密对称密钥，生成对称密钥的密文。
2. CA使用对称密钥对加密证书对应的私钥进行加密，生成加密私钥的密文。
3. CA将加密证书、签名证书、对称密钥的密文和加密私钥的密文发给设备。
4. 设备使用自己的签名私钥解密对称密钥的密文，得到对称密钥。
5. 设备使用对称密钥对加密私钥的密文进行解密，得到加密私钥的明文。

#### 10.2.2 PKI体系架构

PKI 的体系组成如图10-7所示，一个PKI体系由终端实体、证书注册机构、证书认证机构和证书/CRL存储库四部分组成。
图 10-7 PKI 体系组成终端实体EE（End Entity）
终端实体也称为PKI实体，它是PKI产品或服务的最终使用者，可以是个人、组织、设备（如路由器、防火墙）或计算机中运行的进程。
证书认证机构CA（Certificate Authority）
CA是PKI的信任基础，是一个用于颁发并管理数字证书的可信实体。它是一种具备权威性、可信任性和公正性的第三方机构。CA颁发证书的功能由CA服务器实现。
如图10-8所示，CA通常采用多层次的分级结构，根据证书颁发机构的层次，可以划分为根CA和从属CA。
图 10-8 CA 层次示意图

● 根CA是公钥体系中的第一个证书颁发机构，它是信任的起源。根CA可以为其他
CA颁发证书，也可以为其他计算机、用户、服务颁发证书。对大多数基于证书的
应用程序来说，使用证书的认证都可以通过证书链追溯到根CA。根CA通常持有一
个自签名证书。
● 从属CA必须从上级CA处获取证书。上级CA可以是根CA或者是一个已由根CA授权
可颁发从属CA证书的从属CA。上级CA负责签发和管理下级CA的证书，最下一级
的CA直接面向用户。例如，CA2和CA3是从属CA，持有CA1发行的CA证书；
CA4、CA5和CA6是从属CA，持有CA2发行的CA证书。
当某个PKI实体信任一个CA，则可以通过证书链来传递信任，证书链就是从用户的证书
到根证书所经过的一系列证书的集合。当通信的PKI实体收到待验证的证书时，会沿着
证书链依次验证其颁发者的合法性。
CA的核心功能就是发放和管理数字证书，包括：证书的颁发、撤销、查询、归档和证
书废除列表CRL（Certificate Revocation List）的发布等。
证书注册机构RA（Registration Authority）
RA是数字证书注册审批机构，是CA面对用户的窗口和CA证书发放、管理功能的延伸，
它负责接收用户的证书注册和撤销申请，对用户的身份信息进行审查，并决定是否向
提交签发或撤销数字证书的申请。
CA
在实际应用中，RA通常与CA合并在一起。RA也可以独立出来，减轻CA的压力，增强
CA系统的安全性。
证书/CRL（Certificate Revocation List，证书撤销列表）存储库
证书/CRL存储库用于对证书和CRL等信息进行存储和管理，并提供查询功能。
由于用户名称改变、私钥泄露或业务中止等原因，需要一种方法将现行的证书吊销，
即撤销公钥与PKI实体身份信息的绑定关系。这种方法为证书废除列表CRL。
任何一个证书被撤销以后，CA就要发布CRL来声明该证书是无效的，并列出所有被废
除的证书的序列号。因此，CRL提供了一种检验证书有效性的方式。
证书相关操作
PKI的核心技术就围绕着证书的申请、颁发、存储、下载、安装、验证、更新和撤销的
整个生命周期进行展开。
证书申请
证书申请即证书注册，是PKI实体向CA自我介绍并获取证书的过程。通常情况下，PKI
实体会生成一对公私钥。公钥和PKI实体的身份信息（包含在证书注册请求消息中）被
发送给CA，用来生成本地证书。私钥由PKI实体自己保存，用来生成数字签名和解密对
端实体发送过来的密文。当前设备支持离线申请证书和通过CMPv2协议在线申请证
书。
证书颁发
PKI实体向CA申请本地证书时，如果有RA，则先由RA审核PKI实体的身份信息，审核通
过后，RA将申请信息发送给CA，CA再根据PKI实体的公钥和身份信息生成本地证书，
并将本地证书信息发送给RA。如果没有RA，则直接由CA审核PKI实体身份信息。
此外， PKI 实体可以为自己颁发一个自签名证书并用自签名证书颁发本地证书，实现简
单的证书颁发功能。
证书存储

CA生成本地证书后，CA/RA会将本地证书发布到证书/CRL存储库中，为用户提供下载服务和目录浏览服务。
证书下载PKI实体通过LDAP或带外方式下载已颁发的证书。该证书可以是自己的本地证书，也可以是CA/RA证书，或其他PKI实体的本地证书。
证书安装PKI实体下载证书后还需安装证书，即将证书导入到设备的内存中，否则证书不生效。
该证书可以是自己的本地证书，也可以是CA/RA证书，或其他PKI实体的本地证书。
证书验证安装CA/RA证书和本地证书以后，使用之前必须对本地设备的证书进行验证，确保证书的合法性。证书验证的核心是检查CA在证书上的签名，并确定证书仍在有效期内且未被撤销。
证书更新当证书过期或密钥泄露时，PKI实体必须更换证书，可以通过手动申请或配置CMPv2协议自动更新证书来实现。
证书撤销当用户的身份、信息、公钥发生改变或业务中止时，用户需要将自己的数字证书撤销，即撤销公钥与用户身份信息的绑定关系。CA机构提供证书撤销功能。当PKI实体通过带外方式申请撤销自己的证书时，CA会将这些证书存储在CRL存储库或OCSP服务器中。

#### 10.2.3 PKI工作机制

离线申请证书和在线申请证书的工作流程不同，具体如下。

离线申请证书工作流程图 10-9 PKI 离线申请工作过程示意图PKI实体通过磁盘、电子邮件等方式将证书请求文件发送给CA，请求制作证书。
1.
2. CA检测证书请求文件合法性，如果通过，则根据证书请求文件制作证书。
3. PKI实体通过磁盘、电子邮件等方式将证书下载到本地。
4. 安装本地证书到设备的内存中。
5. 可选:
PKI实体间互相通信时，需获取对端实体的本地证书和CA证书。
6. 通过CRL或OCSP方式验证对端实体的本地证书的有效性。
7. 对端实体的本地证书有效时，PKI实体间才可以使用对端证书的公钥进行加密通信。

通过 CMPv2 协议在线申请证书工作流程图 10-10 PKI 在线申请证书工作过程示意图
1. PKI实体向CA发送证书注册请求消息（包括RSA密钥对中的公钥和PKI实体信息）。
当PKI实体通过CMPv2协议申请本地证书时，PKI实体可以使用签名或消息认证码方式向CA机构进行身份认证。
– 签名方式：PKI实体对证书注册请求消息使用CA证书的公钥进行加密；使用PKI实体的额外证书（其他CA颁发的本地证书）相对应的私钥进行数字签名。
– 消息认证码方式： PKI 实体对证书注册请求消息使用 CA 证书的公钥进行加密，证书注册请求消息必须包含消息认证码的参考值和秘密值（与CA的消息认证码的参考值和秘密值一致）。
2. CA收到PKI实体的证书注册请求消息，审核证书注册请求消息并颁发证书。
– 签名方式：CA使用自己的私钥解密，使用PKI实体的额外证书中的公钥解密数字签名，并验证数字指纹。当数字指纹一致时，CA才会审核PKI实体身份等信息，审核通过后，同意PKI实体的申请，颁发本地证书。然后CA使用PKI实体的额外证书中的公钥进行加密，使用自己的私钥进行数字签名后将证书发送给PKI实体，同时也会发送到证书/CRL存储库。
– 消息认证码方式： CA 使用自己的私钥解密并验证消息认证码的参考值和秘密值，当两者和CA的参考值、秘密值一致时，CA才会审核PKI实体身份等信息，审核通过后，同意PKI实体的申请，颁发本地证书。然后CA使用PKI实体的公钥进行加密，将证书发送给PKI实体，同时也会发送到证书/CRL存储库。

3. PKI实体收到CA发送的证书信息，安装本地证书到设备的内存中。
– 签名方式：PKI实体使用额外证书相对应的私钥解密，并使用CA的公钥解密数
字签名并验证数字指纹。数字指纹一致时，PKI实体确认证书信息，然后安装
本地证书到设备的内存中。
– 消息认证码方式：PKI实体使用自己的私钥解密，并验证消息认证码的参考值
和秘密值。参考值和秘密值均一致时，PKI实体确认证书信息，然后安装本地
证书到设备的内存中。
4. 可选:
PKI实体间互相通信时，需各自获取对端实体的本地证书和CA证书。
5. PKI实体通过CRL或OCSP方式验证对端实体的本地证书有效性。
6. 对端实体的本地证书有效时，PKI实体间才可以使用对端证书的公钥进行加密通
信。
如果PKI认证中心有RA，则PKI实体也会下载RA证书。由RA审核PKI实体的本地证书申
请，审核通过后将申请信息发送给CA来颁发本地证书。

### 10.3 PKI配置注意事项

License 依赖PKI无需License许可即可使用。
硬件依赖表 10-4 支持本特性的硬件

| 系列 | 支持产品 |
|---|---|
| S6750-H | S6750-H36C，S6750-H48X8C，S6750-H48Y8C |
| S1730S-S3 | S1730S-S24P4S-A3，S1730S-S24P4X-A3， S1730S-S24T4S-QA3，S1730S-S24T4X-QA3， S1730S-S48P4S-A3，S1730S-S48T4S-A3， S1730S-S48T4X-A3，S1730S-S8P4X-QA3， S1730S-S8T4X-QA3 |
| S6730E-H-V2 | S6730E-H6FX4Y2CZ-V2 |
| S5735E-S-V2 | S5735E-S24HJ4XE-V2，S5735E-S24HS4XE-V2， S5735E-S24J4XE-V2，S5735E-S48HJ4XE-V2， S5735E-S48HS4XE-V2，S5735E-S48J4XE-V2 |

| 系列 | 支持产品 |
|---|---|
| S5735-S-V2 | S5735-S24HJ4XE-V2，S5735-S24HS4XE-V2， S5735-S24J4XE-V2，S5735-S24P4XE-V2，S5735- S24P4XEZ-V2，S5735-S24P8J4XEZ-V2，S5735- S24PN4XE-V2，S5735-S24ST4XE-V2，S5735- S24T4XE-C-V2，S5735-S24T4XE-V2，S5735- S24T4XEZ-V2，S5735-S24T8J4XE-XA-V2，S5735- S24T8J4XEZ-V2，S5735-S24U4XE-V2，S5735- S48HJ4XE-V2，S5735-S48HS4XE-V2，S5735- S48J4XE-V2，S5735-S48P4XE-V2，S5735- S48P4XEZ-V2，S5735-S48PN4XE-V2，S5735- S48S4XE-V2，S5735-S48T4XE-C-V2，S5735- S48T4XE-V2，S5735-S48T4XE-XA-V2，S5735- S48T4XEZ-V2，S5735-S48U4XE-V2 |
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
| S5735E-L-V2 | S5735E-L16LP2UM2X-QA-V2，S5735E-L16LP2X- QA-V2，S5735E-L24HJ4XE-A-V2，S5735E- L24P4S-A-V2，S5735E-L24P4XE-A-V2，S5735E- L24ST4XE-A-V2，S5735E-L24T4XE-A-V2， S5735E-L48LP4S-A-V2，S5735E-L48LP4XE-A-V2， S5735E-L48S4XE-A-V2，S5735E-L48T4XE-A-V2， S5735E-L8P4X-QA-V2，S5735E-L8T4X-QA-V2 |
| S5755-S | S5755-S24N8YZ，S5755-S24P8J8YZ，S5755- S24P8Y，S5755-S24T8J8YZ，S5755-S24T8Y， S5755-S24U8J8YZ，S5755-S24U8Y，S5755- S24UN8YZ，S5755-S48N8YZ，S5755-S48P8Y， S5755-S48P8YZ，S5755-S48T8Y，S5755- S48T8YZ，S5755-S48T8YZ-B，S5755-S48U8Y， S5755-S48U8YZ，S5755-S48UN8YZ |
| S5735R-L-V2 | S5735R-L16LP2S-QA-V2，S5735R-L16LP2UM2X- QA-V2，S5735R-L16LP2X-QA-V2，S5735R- L16T4S-A-V2，S5735R-L16T4X-QA-V2，S5735R- L24P4S-A-V2，S5735R-L24P4X-A-V2，S5735R- L24T4S-A-V2，S5735R-L24T4X-QA-V2，S5735R- L48LP4S-A-V2，S5735R-L48LP4X-A-V2，S5735R- L48P4X-A-V2，S5735R-L48T4S-A-V2，S5735R- L48T4X-A-V2，S5735R-L8P4S-A-V2，S5735R- L8P4X-QA-V2，S5735R-L8T4S-A-V2，S5735R- L8T4X-QA-V2 |
| S5735-L-V2 | S5735-L10T4X-A-V2，S5735-L14P2S-QA-V2， S5735-L16LP2UM2X-QA-V2，S5735-L16LP2X-QA- V2，S5735-L16P2UM2X-QA-V2，S5735-L16T4S- A-V2，S5735-L16T4X-QA-V2，S5735-L24HJ4XE- A-V2，S5735-L24J4X-A-V2，S5735-L24J4X-D- V2，S5735-L24LU8S4XE-QA-V2，S5735-L24P4S- A-V2，S5735-L24P4XE-A-V2，S5735-L24PN4XE- A-V2，S5735-L24ST4XE-A-V2，S5735-L24T4S-A- V2，S5735-L24T4X-QA-V2，S5735-L24T4XE-A- V2，S5735-L24T4XE-D-V2，S5735-L24T8J4XE-A- V2，S5735-L48J4X-A-V2，S5735-L48J4X-D-V2， S5735-L48LP4S-A-V2，S5735-L48LP4XE-A-V2， S5735-L48LPN4XE-A-V2，S5735-L48P4XE-A-V2， S5735-L48PN4XE-A-V2，S5735-L48S4X-A-V2， S5735-L48S4XE-A-V2，S5735-L48T4S-A-V2， S5735-L48T4XE-A-V2，S5735-L48T4XE-D-V2， S5735-L8P2T4X-A-V2，S5735-L8P4S-A-V2， S5735-L8P4X-QA-V2，S5735-L8T4S-A-V2， S5735-L8T4X-QA-V2 |
| S6730-S-V2 | S6730-S24X6Q-V2，S6730-S48X6Q-V2 |

| 系列 | 支持产品 |
|---|---|
| S5735I-S-V2 | S5735I-S16T2S4XN-V2，S5735I-S16T8S4XE-QD- V2，S5735I-S24T4XE-V2，S5735I-S24T8S4XE-QA- V2，S5735I-S24U4XE-V2，S5735I-S48T4XE-V2， S5735I-S8T4SN-V2，S5735I-S8T4XN-V2，S5735I- S8T8P2S4XN-V2，S5735I-S8U2XN-V2，S5735I- S8U4XN-V2 |
| S5732-H-V2 | S5732-H24S4X6QZ-TV2，S5732-H24S4X6QZ- V2，S5732-H24UM4Y2CZ-KV2，S5732- H24UM4Y2CZ-V2，S5732-H44S4X6QZ-V2， S5732-H48UM4Y2CZ-KV2，S5732-H48UM4Y2CZ- TV2，S5732-H48UM4Y2CZ-V2 |

查询工具如需了解硬件规格、产品部件的配套关系，请点击硬件中心进行查询；如需了解关键规格、全量软件规格，请点击规格查询进行查询。
特性限制表 10-5 本特性的使用限制

| 特性 | 特性限制 |
|---|---|
| 证书申请和管理 | 在申请证书前需要确认设备上的时钟是否正确。设备会检查当前时间是否在证书的有效范围内。如果在有效范围之外，证书会注册失败。 |
| 证书申请和管理 | 由于Windows Server 2003服务器处理能力有限，与该型号服务器对接时，设备上不能配置过多实体信息或携带密钥对位数过大的密钥对。否则可能导致设备与服务器对接失败。 |
| 证书申请和管理 | 只能通过配置源IP地址的方式指定vrrp备份组的虚拟IP作为源IP地址，未配置源IP地址时无法自动根据路由选择vrrp备份组的虚拟IP作为源IP 地址。 |
| 证书申请和管理 | 必须在当前证书过期之前将证书导入到所有需要导入证书的设备上。如果证书已过期，管理员没有及时安装新的证书，证书验证会失败。 |
| 证书申请和管理 | 禁止导入或替换非初始证书的本地证书到default域下。 |
| 证书申请和管理 | SM2证书校验仅支持GM/T 0009-2012标准定义的默认用户身份标识 ID，无用户身份标识ID或非默认用户身份标识ID的SM2证书无法校验。 |
| 安全管理 | 出于安全性考虑，不建议使用该特性提供的弱安全算法或弱安全协议。如果确实需要使用，请执行命令install feature-software WEAKEA安装弱安全算法/协议特性包WEAKEA。设备默认自带弱安全算法/协议特性包WEAKEA，特性包安装或卸载的详细步骤请参见《CLI配置指南-系统管理配置》中的“升级维护配置”。 |

### 10.4 PKI缺省配置

PKI的主要缺省配置如表10-6所示。
表 10-6 PKI 的缺省配置

| 参数 | 缺省配置 |
|---|---|
| PKI域 | 设备缺省存在一个域名为default的PKI 域，此域可以修改但不能删除。 |
| RSA密钥对 | 设备缺省存在一个名称为default的RSA 密钥对文件 |
| 设备保存证书请求、证书和CRL时的文件格式 | PEM |
| 证书状态检查方式 | CRL方式 |
| 本地证书/CA证书的过期预告警时间 | 90天 |
| 本地证书/CA证书/CRL的过期检查周期 | 24小时 |
| CRL过期检查功能 | 开启 |
| CRL的过期预告警剩余百分比 | 5 |

### 10.5 申请本地证书的预配置

#### 10.5.1 配置RSA/SM2/ECC密钥对

背景信息本地证书由CA进行数字签名并颁发，是公钥与PKI实体身份信息的绑定。申请本地证书时，需先配置RSA/SM2/ECC密钥对，生成公钥和私钥。公钥由PKI实体发送给CA，用来加密明文；私钥由PKI实体保留，用来进行数字签名和解密对端发送过来的密文。
配置RSA/SM2/ECC密钥对有以下两种方式：
● 创建RSA/SM2/ECC密钥对。
设备上可以直接创建密钥对，无需再将密钥对导入到设备的内存中。创建RSA/SM2/ECC密钥对的过程中，系统会提示输入公钥的位数，长度范围从2048到4096。公钥的位数越长，其安全性就越高，但计算速度也越慢。
● 导入RSA/SM2/ECC密钥对。
当需要使用其他 PKI 实体产生的密钥对时，可以通过 FTP/SFTP 传到设备上，然后将密钥对导入到内存中，否则密钥对不生效。

操作步骤步骤1 进入系统视图。
system-view步骤2 根据实际情况选择配置RSA/SM2/ECC密钥对的方法。

| 操作 | 命令 | 说明 |
|---|---|---|
| 创建 RSA/SM2/ ECC密钥对 | pki rsa local-key-pair create key-name [ modulus modulus-size ] [ exportable ] | 仅当配置exportable参数时，创建的RSA密钥对才是可导出的。 |
|  | pki sm2 local-key-pair create key-name [ exportable ] | 仅当配置exportable参数时，创建的SM2密钥对才是可导出的。 |
|  | pki ecc curve-name { prime256v1 | ec192wapi | secp384r1 | secp521r1 } local-key-pair create key- name [ exportable ] | 仅当配置exportable参数时，创建的ECC密钥对才是可导出的。 |
| 导入 RSA/SM2/ ECC密钥对 | pki import rsa-key-pair keyname [ exclude-cert ] { pem | pkcs12 } filename [ exportable ] [ password password ] | 配置exclude-cert参数时，系统不会导入文件中存在的证书。 |
|  | pki import sm2-key-pair keyname pem filename [ exportable ] signkey signkey-name [ certificate certificate-name ] | 仅当配置exportable参数时，导入的SM2密钥对才是可导出的。 |
|  | pki import ecc-key-pair keyname [ exclude-cert ] { pem | pkcs12 } filename [ exportable ] [ password password ] | 配置exclude-cert参数时，系统不会导入文件中存在的证书。 |

---- 结束
检查配置结果
● 执行命令display pki rsa local-key-pair { pem | pkcs12 } file-name
[ password password ]，查看RSA密钥对信息。
● 执行命令display pki rsa local-key-pair [ name key-name ] public，查看RSA
公钥信息。
● 执行命令display pki sm2 local-key-pair [ name key-name ] public，查看
SM2 密钥对及公钥信息。
● 执行命令display pki ecc local-key-pair [ name key-name ] public，查看ECC
密钥对及公钥信息。

后续处理表 10-7

| 操作 | 命令 | 说明 |
|---|---|---|
| 导出 RSA/SM2/ ECC密钥对 | pki export rsa-key-pair keyname [ and-certificate certificate-name ] { pem filename [ aes ] | pkcs12 filename } password password | 当需要备份RSA密钥对或者需要将 RSA密钥对导出给其他设备使用时，可以在系统视图下执行此命令，将 RSA密钥对导出到设备的存储介质中，同时支持导出与其关联的证书及证书链，然后可以通过FTP/SFTP 获取RSA密钥对。 |
|  | pki export sm2-key-pair keyname pem filename [ password password ] | 当需要备份SM2密钥对或者需要将 SM2密钥对导出给其他设备使用时，可以在系统视图下执行此命令，将SM2密钥对导出到设备的存储介质中，然后可以通过FTP/SFTP 获取SM2密钥对。 |
|  | pki export ecc-key-pair keyname [ and-certificate certificate-name ] { pem filename [ aes ] | pkcs12 filename } password password | 当需要备份ECC密钥对或者需要将 ECC密钥对导出给其他设备使用时，可以在系统视图下执行此命令，将 ECC密钥对导出到设备的存储介质中，同时支持导出与其关联的证书及证书链，然后可以通过FTP/SFTP 获取ECC密钥对。 |
| 销毁指定的 RSA/SM2/ ECC密钥对 | pki rsa local-key-pair destroy key-name | RSA密钥对泄露、损坏、不用或丢失时，可以在系统视图下执行此命令，销毁指定的RSA密钥对。配置后，系统会销毁设备中对应名称的 RSA密钥对。 |
|  | pki sm2 local-key-pair destroy key-name | SM2密钥对泄露、损坏、不用或丢失时，可以在系统视图下执行此命令，销毁指定的SM2密钥对。配置后，系统会销毁设备中对应名称的 SM2密钥对。 |
|  | pki ecc local-key-pair destroy key-name | ECC密钥对泄露、损坏、不用或丢失时，可以在系统视图下执行此命令，销毁指定的ECC密钥对。配置后，系统会销毁设备中对应名称的 ECC密钥对。 |
| 查找证书所对应的 RSA/SM2/ ECC密钥对 | pki match-rsa-key certificate-filename file- name | 用户不知道证书所对应的RSA密钥对时，可以在系统视图下执行此命令，查找证书所对应的RSA密钥对。 |
|  | pki match-sm2-key certificate-filename file- name | 用户不知道证书所对应的SM2密钥对时，可以在系统视图下执行此命令，查找证书所对应的SM2密钥对。 |

| 操作 | 命令 | 说明 |
|---|---|---|
|  | pki match-ecc-key certificate-filename file- name | 用户不知道证书所对应的ECC密钥对时，可以在系统视图下执行此命令，查找证书所对应的ECC密钥对。 |

#### 10.5.2 配置PKI实体信息

背景信息本地证书由CA进行数字签名并颁发，是公钥与PKI实体身份信息的绑定。PKI实体身份信息即为PKI实体信息，CA根据PKI实体信息唯一标识证书申请者，因此在申请本地证书时必须将PKI实体信息发送给CA。
PKI实体信息包括：通用名称（Common Name）、FQDN（Fully Qualified Domain Name）名称、IP地址、电子邮箱地址等，其中通用名称必须配置，其他几项是可选配置。这些信息都将包含在证书中。
操作步骤步骤1 进入系统视图。
system-view步骤2 创建PKI实体并进入PKI实体视图，或者直接进入PKI实体视图。
pki entity entity-name步骤3 配置PKI实体的通用名称。
common-name common-name步骤4 可选: 配置PKI实体的其他参数。
为了更好的标识证书申请者的唯一身份，还可配置以下可选参数作为PKI实体的别名。
否则，当PKI实体间的通用名称相同时，会导致PKI实体申请证书失败。

| 操作 | 命令 |
|---|---|
| 配置PKI实体的IP地址。 | ip-address { ipv4-address | ipv6- address | interface-type interface- number [ ipv6 ] } |
| 配置PKI实体的FQDN名称。 | fqdn fqdn-name |
| 配置PKI实体的电子邮箱地址。 | email email-address |
| 配置PKI实体所属的国家代码。 | country country-code |
| 配置PKI实体所在的地理区域名称。 | locality locality-name |
| 配置PKI实体所属的州或省。 | state state-name |
| 配置PKI实体所属的组织名称。 | organization organization-name |
| 配置PKI实体所属的部门名称。 | organization-unit organization-unit- name |

#### 10.5.4 安装CA证书

步骤5 退出PKI实体视图。
quit
----结束检查配置结果执行命令display pki entity [ entity-name ]，查看PKI实体信息。

#### 10.5.3 下载CA证书

背景信息申请本地证书时，PKI实体会将证书注册请求消息发送给CA。为了提高传输过程中的安全性，PKI实体必须使用CA的公钥对证书注册请求消息进行加密保护。因此，PKI实体必须先下载并获取CA证书后从中获取CA的公钥。
下载CA证书有如下几种方式，可根据CA提供的服务方式进行选择。
● 通过CMPv2协议从CMPv2服务器下载CA证书，将CA证书下载到设备的存储介质中。
● 通过LDAP协议从存放证书的服务器上下载CA证书，将CA证书下载到设备的存储介质中。
● 通过带外方式（磁盘、电子邮件等）获得CA证书后，上传到设备的存储介质中。
操作步骤
● 通过CMPv2协议下载CA证书。
通过CMPv2协议下载CA证书的具体配置请参见10.7.2 通过CMPv2协议在线申请和更新本地证书。
● 通过LDAP协议下载CA证书。
system-view pki ldap-server-template template-name attribute attr-value save-name dn dn-value
● 通过带外方式获得CA证书。
用户通过磁盘、电子邮件等方式获得CA证书后，需要手工上传到设备的存储介质中。此外，也可以选择通过管理PC下载证书后，使用FTP/SFTP方式上传到设备的存储介质中。由于 FTP 协议本身存在安全风险，建议使用 SFTP 安全协议。
----结束安装 证书
10.5.4 CA背景信息下载CA证书后，设备会自动将CA证书存放在flash:/pki/public存储路径下。
通过带外方式（磁盘、电子邮件等）获得CA证书后，需要将CA证书上传到设备指定的存储路径下。安装 CA 证书前，需要先将 CA 证书上传到 flash:/pki/public 存储路径下。
CA证书存放在上述指定路径后，还需手动导入到设备的内存中。只有将CA证书导入到设备的内存中，设备重启后系统才能自动加载证书文件。

说明请确保CA证书文件不超过1M，避免安装失败。
缺省情况下存在名称为default的PKI域。default域可以修改但不能删除。
操作步骤步骤1 可选: 进入用户视图，将CA证书下载到flash:/pki/public目录下。
通过带外方式获取到CA证书，然后使用FTP/SFTP上传到设备的存储介质中时，需执行以下操作。由于FTP协议本身存在安全风险，建议使用SFTP安全协议。
cd pki cd public/ ftp 172.16.104.110 Trying 172.16.104.110...
Press CTRL+K to abort Connected to 172.16.104.110.
220 FTP service ready.
User(172.16.104.110:(none)):ftpuser 331 Password required for ftpuser Enter password:
230 User logged in.
get ca.cer 200 Port command okay.
150 Opening ASCII mode data connection for temp1.c.
226 Transfer complete.
FTP: 4 byte(s) received in 8.190 second(s) .48byte(s)/sec.
步骤2 进入系统视图。
system-view步骤3 可选: 将初始的CA证书导入到default域下。
pki import-certificate default_ca realm default设备出厂前会将初始的CA证书存放在NVRAM内存中，如需使用初始CA证书，可以执行此命令将证书加载到default域下。初始CA证书可以被删除，删除后可以在default域下导入其他CA证书，由于default_ca.cer为系统预留的初始CA证书名称，导入的证书不能命名为default_ca.cer。如果想要恢复被删除的初始CA证书，也可以执行此命令将证书加载到default域下。
步骤4 创建PKI域。
pki realm realm-name quit步骤5 将CA证书导入到设备的内存中。
pki import-certificate ca [ [ realm realm-name ] { der | pkcs12 | pem } ] filename file-name [ cert-name cert-name ] [ no-check-hash-alg ] [ no-check-same-name ]步骤6 可选: 配置内存中的CA证书的过期预告警时间。
pki set-certificate expire-prewarning day步骤7 可选: 配置内存中的CA证书的过期检查周期。
pki certificate expiration-check interval interval-time
----结束检查配置结果执行命令display pki certificate ca [ realm realm-name | filename file-name ]，查看设备上已加载的CA证书的内容。

### 10.6 离线申请证书

#### 10.6.1 了解离线证书申请

证书申请即证书注册，就是一个PKI实体向CA自我介绍并获取证书的过程。离线申请本地证书需要配置PKI实体信息、RSA密钥对、申请本地证书、安装本地证书。离线方式申请证书流程如图10-11所示。
图 10-11 离线证书申请流程
1. 创建公私密钥对。首先，在DeviceA上创建的公私密钥对，因为在申请证书时会用到公钥信息。
2. 配置实体信息。申请证书时，DeviceA必须向CA提供能够证明自己身份的信息，实体信息代表的就是设备的身份信息，包括：通用名称（Common Name）、FQDN（Fully Qualified Domain Name）名称、IP地址、电子邮箱地址等。其中，通用名称是必须配置的，而其他几项是可选配置的。实体信息配置完成后，还需要在PKI域中引用实体信息。
3. 生成证书请求文件。生成的证书请求文件以“PKI域名.req”的名字保存在DeviceA的存储介质中。
4. 证书请求文件生成后，可以将该文件通过磁盘、电子邮件等方式将该文件发送给CA。
5. CA审核通过后，根据证书请求文件制作证书。
6. 证书生成后，通过磁盘、电子邮件等方式获取到DeviceA的本地证书DeviceA.cer。
7. 将DeviceA.cer下载到DeviceA的flash:/pki/public存储路径下。
8. 将DeviceA.cer证书导入到DeviceA的内存中。

#### 10.6.2 离线申请本地证书

前提条件已完成申请本地证书的预配置操作，具体可以参见申请证书预配置。
背景信息离线申请本地证书需要用户在设备上生成证书申请文件，然后通过磁盘、电子邮件等带外方式将证书申请文件发送给CA，向CA申请本地证书。
说明离线申请国密数字信封时，为了确保导入成功，需要申请PEM编码格式且符合GM/T 0009-2012标准的数字信封。
操作步骤步骤1 进入系统视图。
system-view步骤2 创建PKI域并进入PKI域视图，或者直接进入已存在的PKI域视图。
pki realm realm-name缺省情况下，系统下存在名称为default的PKI域，该域可以修改但不能删除。
PKI域是一个本地概念，一个设备上配置的PKI域对CA和其他设备是不可见的，每一个PKI域有单独的参数配置信息。
步骤3 指定申请证书的PKI实体。
entity entity-name entity-name是一个已经通过pki entity命令创建的PKI实体。
步骤4 根据实际情况选择配置使用离线方式申请证书时使用的密钥对。
● 配置使用离线方式申请证书时使用的RSA密钥对。
rsa local-key-pair key-name
● 配置使用离线方式申请证书时使用的SM2密钥对。
sm2 local-key-pair key-name
● 配置使用离线方式申请证书时使用的ECC密钥对。
ecc local-key-pair key-name步骤5 配置签名证书注册请求消息使用的摘要算法。
enrollment-request signature message-digest-method { md5 | sha1| sha-256 | sha-384 | sha-512 | sm3 }缺省情况下，签名证书注册请求消息使用的摘要算法为sha-256。
PKI实体使用的摘要算法必须与CA服务器上的摘要算法一致。由于MD5和SHA1算法为不安全算法，建议使用SHA2算法（SHA-256、SHA-384和SHA-512）。
在某个PKI域下，当使用SM2密钥对离线申请证书时，签名证书注册请求消息使用的摘要算法必须配置为SM3；当使用RSA/ECC密钥对离线申请证书时，签名证书注册请求消息使用的摘要算法不可配置为SM3，否则会导致离线申请证书失败。

说明出于安全性考虑，不建议使用该特性提供的弱安全算法或弱安全协议。如果确实需要使用，请执行命令install feature-software WEAKEA安装弱安全算法/协议特性包WEAKEA。设备默认自带弱安全算法/协议特性包WEAKEA，特性包安装或卸载的详细步骤请参见《CLI配置指南-系统管理配置》中的“升级维护配置”。
步骤6 可选: 配置证书公钥用途属性。
key-usage { signature | encipherment } quit步骤7 在系统视图下，配置设备保存证书和证书请求时的文件格式。
pki file-format { der | pem }缺省情况下，设备保存证书和证书请求时的文件格式为PEM。
步骤8 配置以PKCS#10格式保存证书申请信息到文件中。
pki enroll-certificate realm realm-name pkcs10 [ filename filename ] [ password password ] PKI实体使用的挑战密码必须与CA服务器上设置的密码一致。如果CA服务器不要求使用挑战密码，则不用配置挑战密码。
步骤9 通过磁盘、电子邮件等带外方式将证书申请文件发送给CA，向CA申请本地证书。
----结束检查配置结果
● 执行命令display pki realm [ realm-name ]，查看PKI域的信息。
● 执行命令display pki cert-req filename file-name，查看证书请求文件的内容。

#### 10.6.3 下载本地证书

背景信息通常采用以下方式获得本地证书，设备采用哪种方式下载证书，取决于CA服务器提供的服务方式：
● 通过LDAP协议从存放证书的服务器上下载本地证书，设备会自动将本地证书保存到设备的flash:/pki/public存储路径下。
● 通过带外方式（磁盘、电子邮件等）获得本地证书后，上传到设备的存储介质中。
操作步骤
● 通过LDAP方式下载本地证书。
system-view pki ldap-server-template template-name attribute attr-value save-name dn dn-value
● 通过带外方式下载本地证书。
用户通过磁盘、电子邮件等方式获得本地证书后，需要手工上传到设备的存储介质中。也可以选择通过管理 PC 下载证书后，使用 FTP/SFTP 方式上传到设备的存储介质中。由于FTP协议本身存在安全风险，建议使用SFTP安全协议。
----结束

检查配置结果
● 执行命令display pki credential-storage-path，查看证书的缺省保存路径。
● 执行命令dir（用户视图），查看存储介质中的本地证书文件。

#### 10.6.4 安装本地证书

背景信息通过带外方式（磁盘、电子邮件等）获取到本地证书，需要将本地证书上传到设备的指定存储路径下。安装本地证书需要先将证书上传到flash:/pki/public存储路径下。
通过LDAP协议下载本地证书，设备会自动将本地证书存放在flash:/pki/public存储路径下。
本地证书存放在上述指定路径下后，还需手动导入到设备的内存中。只有将本地证书导入到设备的内存中，在设备重启后系统才能自动加载证书文件。
说明请确保本地证书文件不超过1M，避免安装失败。
缺省情况下，根系统下存在名称为default的PKI域。设备初始的本地证书默认存放在default域下。default域可以修改但不能删除。
初始的本地证书作为华为设备的身份标识，缺省情况下为设备中的用户登录业务提供证书认证。
操作步骤步骤1 可选: 进入用户视图，将本地证书下载到flash:/pki/public目录下。
通过带外方式获取到本地证书，然后使用FTP/SFTP上传到设备的存储介质中时，需执行以下操作，由于FTP协议本身存在安全风险，建议使用SFTP安全协议。通过LDAP协议方式获取本地证书不需要执行如下操作。
cd pki cd public/ ftp 172.16.104.110 Trying 172.16.104.110...
Press CTRL+K to abort Connected to 172.16.104.110.
220 FTP service ready.
User(172.16.104.110:(none)):ftpuser 331 Password required for ftpuser Enter password:
230 User logged in.
get device.cer 200 Port command okay.
150 Opening ASCII mode data connection for temp1.c.
226 Transfer complete.
FTP: 4 byte(s) received in 8.190 second(s) .48byte(s)/sec.
步骤2 进入系统视图。
system-view步骤3 可选: 将初始的本地证书导入到default域下。
pki import-certificate default_local realm default初始的本地证书可以被删除，如果想要恢复被删除的初始Local证书，可以执行此命令将证书从NVRAM中加载到default域下。

步骤4 创建PKI域。
pki realm realm-name quit步骤5 在系统视图下，将本地证书导入到设备的内存中。
● 当在本PKI实体下创建RSA密钥对，通过PKI实体信息和RSA密钥对去CA申请本地证书时，只需执行如下命令，导入本地证书到内存中即可，因为在本地创建RSA密钥对时RSA密钥已经默认导入到设备的内存中。
pki import-certificate local [ [ realm realm-name ] { der | pkcs12 | pem } ] filename file-name [ cert-name cert-name ] [ no-check-hash-alg ] [ no-check-same-name ]
● 当使用其他PKI实体产生的密钥对和其他PKI实体的证书时，需要导入证书和密钥对文件。一般证书及其密钥对有两种存在形式，一种是证书文件中包含密钥对文件，两者以一个文件的形式存在；另一种是证书和密钥对相互独立以两个文件形式存在。不同形式下，将其导入内存使用的方法不同，具体如下。
– 证书文件中包含密钥对文件。
pki import rsa-key-pair keyname { pem | pkcs12 } file-name [ exportable ] [ password password ]
– 证书文件和密钥对文件独立存在。
\# 导入证书文件。
pki import-certificate local [ [ realm realm-name ] { der | pkcs12 | pem } ] filename file- name [ cert-name cert-name ] [ no-check-hash-alg ] [ no-check-same-name ] \# 导入密钥对文件。
pki import rsa-key-pair keyname exclude-cert { pem | pkcs12 } file-name [ exportable ] [ password password ]说明若不指定待导入证书的格式，系统将自行识别导入。
步骤6 可选: 配置内存中的本地证书的过期预告警时间。
pki set-certificate expire-prewarning day步骤7 可选: 配置内存中的本地证书的过期检查周期。
pki certificate expiration-check interval interval-time
----结束检查配置结果执行命令display pki certificate local [ realm realm-name | filename filename ]，查看设备上已加载的本地证书的内容。

#### 10.6.5 检查证书有效性

前提条件已在设备上安装CA证书和本地证书。
背景信息在安装 CA 证书和本地证书以后，使用每一个证书之前，必须对本地设备的证书进行验证，以确保证书的合法性。证书验证包括对签发时间、签发者信息以及证书的有效性几方面进行验证。证书验证的核心是检查CA在证书上的签名，并确定证书仍在有效期内，而且未被撤销。

为完成证书验证，本地设备需要下面的信息：CA证书、CRL、本地证书及其私钥及证书认证相关配置信息。
本地证书验证的主要过程如下：
1. 使用CA证书的公钥验证CA的签名是否正确。
为验证一个证书的合法性，首先需要获得颁发这个证书的CA的公钥（即获得CA证书），以便检查该证书上CA的签名。一个CA可以让另一个更高层次的CA来证明其证书的合法性，这样顺着证书链，验证证书就变成了一个迭代过程，最终这个链必须在某个“信任点”（一般是持有自签名证书的根CA或者是PKI实体信任的中间CA）处结束。
任何PKI实体，如果它们共享相同的根CA或子CA，并且已获取CA证书，都可以验证对端证书。
证书链的验证过程是一个从目标证书（待验证的PKI实体证书）到信任点证书逐层验证的过程。一般情况下，当验证对端证书链时，验证过程在碰到第一个可信任的证书或CA机构时结束。
2. 根据证书的有效期，验证证书是否过期。
3. 检查证书的状态，即通过 CRL 、 OCSP 和 None 方式检查证书是否被撤销。
操作步骤步骤1 进入系统视图。
system-view步骤2 检查CA证书或本地证书的有效性。
pki validate-certificate { ca | local } { realm realm-name | filename file-name } pki validate-certificate ca命令只能验证根CA的CA证书有效性，不能验证从属CA的CA证书有效性。在多级CA的环境中，当设备上导入了多个CA证书时，只能使用pki validate-certificate local命令来验证从属CA的CA证书有效性。
----结束

### 10.7 通过CMPv2协议在线申请和更新证书

#### 10.7.1 了解通过CMPv2协议在线申请和更新证书

当设备可以访问CA，并且CA支持CMPv2协议时，可选择此方式申请和更新本地证书。
证书申请证书申请即证书注册，就是一个PKI实体向CA自我介绍并获取证书的过程。用户可以通过CMPv2协议在线方式申请本地证书，CA根据证书注册请求消息为PKI实体制作证书。完成制作后，CA会自动触发将本地证书保存到设备的flash:/pki/public存储路径下，然后手动将本地证书保存到设备的内存中即可。
在线申请本地证书需要配置PKI实体信息、RSA密钥对、安装CA证书、申请本地证书、安装本地证书。通过CMPv2协议在线申请证书流程如图10-12所示。

图 10-12 在线证书申请流程
1. 创建公私密钥对。首先，在DeviceA上创建公私密钥对，因为在申请证书时会用到公钥信息。
2. 创建实体信息。申请证书时，DeviceA必须向CA提供能够证明自己身份的信息，实体信息代表的就是设备的身份信息，包括：通用名称（Common Name）、FQDN（Fully Qualified Domain Name）名称、IP地址、电子邮箱地址等。其中，通用名称是必须配置的，而其他几项是可选配置的。
3. 获取并安装CA证书。PKI实体向CA发送证书注册请求消息时需要使用CA的公钥。
4. PKI实体向CA发送证书注册请求消息。
通过CMPv2协议申请本地证书有首次申请本地证书和签名方式非首次申请本地证书两种方式。首次证书申请适用于设备第一次向CA申请证书的情况。CA制作完本地证书后，会返回CA证书和本地证书；签名方式非首次申请本地证书，CA只会返回本地证书，不会返回CA证书。
– 首次申请本地证书IR（Initialization Request）
首次申请本地证书提供以下两种CMPv2服务器认证PKI实体的方式。
▪消息认证码方式：设备和CMPv2服务器共享一对消息认证码的参考值和秘密值。在进行首次证书申请的时候，设备会将这对参考值和秘密值加入到请求报文当中发送到CMPv2服务器，CMPv2服务器通过验证参考值和秘密值来鉴定设备的身份。
▪签名方式：适用于当设备已经有了额外本地证书，向CA发起证书请求时，设备使用已有的额外本地证书的私钥来进行签名。
– 签名方式非首次申请本地证书CR（Certification Request）
适用于当设备已经有了额外本地证书，需要再申请本地证书的情况。向CA发起证书请求时，设备使用已有的额外本地证书的私钥来进行签名。
5. CA根据证书注册请求消息制作证书。经过CA的处理，最终获取到了DeviceA的证书DeviceA.cer。
6. CA自动将DeviceA.cer上传到DeviceA的flash:/pki/public存储路径下。
7. 导入证书。将证书导入到DeviceA的内存中。

证书更新当证书过期、密钥泄露时，PKI实体必须更换证书，此时可以通过重新申请来达到更新的目的。通过CMPv2协议更新本地证书有两种方式：
● 手工更新证书，即密钥更新请求KUR（Key Update Request）
密钥更新请求又称为证书更新请求，是对设备已有的证书（尚未过期且没有被吊销）进行更新操作。在更新过程中，使用现有的证书作为身份认证的手段。更新操作可以使用新的公钥，也可以使用原来的公钥。
● 自动更新证书为了避免业务的中断，在有效期截止前必须申请新的证书，而使用手工更新证书的方式容易出现忘记更新证书的情况。设备支持证书的自动更新功能，当系统检测到时间超过了设置的证书自动更新时间之后，会自动向CMPv2服务器发起证书的更新请求。申请的新证书会同时替换存储介质中的证书文件和内存中对应的证书，业务不会中断。
此方式可以对IR方式申请的本地证书或KUR方式更新的本地证书进行自动更新。

#### 10.7.2 通过CMPv2协议在线申请和更新本地证书

前提条件已完成申请证书的预配置操作，具体可以参见申请证书预配置。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置设备保存证书时的文件格式。
pki file-format { der | pem }步骤3 创建CMP会话并进入CMP会话视图，或者直接进入CMP会话视图。
pki cmp session session-name CMP会话是一个本地概念，一个设备上配置的CMP会话对CA和其他设备是不可见的。
步骤4 配置设备使用CMPv2方式申请证书时使用的PKI实体名称。
cmp-request entity entity-name步骤 5 为 CMP 会话配置 CA 的名称。
cmp-request ca-name ca-name配置的CA名称中各个字段的顺序必须要和实际CA证书中的顺序保持一致，否则CMPv2服务器会认为是错误的。
步骤6 配置CMPv2服务器的URL。
cmp-request server url [ esc ] url-addr步骤7 配置CMPv2方式申请证书时使用的RSA密钥对。
cmp-request rsa local-key-pair key-name [ regenerate [ key-bit ] ]如果配置了regenerate参数，则证书自动更新时，系统会生成新的RSA密钥对去申请新证书，并且用新的证书和RSA密钥对替换原有的证书和RSA密钥对。否则证书自动更新时，系统会继续使用原来的RSA密钥对。

步骤8 可选: 配置建立TCP连接使用的源地址。
source { interface interface-type interface-number | ip-address }如果指定接口，请确保该接口为三层接口，且接口下已经配置了IP地址。
步骤9 可选: 配置使用CMPv2协议进行证书申请的报文加密方式。
cmp-request integrity-algorithm { hmac-sha256 | hmac-sha1 }使用CMPv2协议进行证书申请时，报文需要哈希算法进行加密。缺省情况下，使用CMPv2协议进行证书申请时使用的加密算法为SHA256。
说明出于安全性考虑，不建议使用该特性提供的弱安全算法或弱安全协议。如果确实需要使用，请执行命令install feature-software WEAKEA安装弱安全算法/协议特性包WEAKEA。设备默认自带弱安全算法/协议特性包WEAKEA，特性包安装或卸载的详细步骤请参见《CLI配置指南-系统管理配置》中的“升级维护配置”。
步骤10 可选: 配置验证CA响应签名的证书文件。
当使用签名方式申请本地证书时，设备需要验证本地证书是否是合法CA颁发的，此时需要执行以下操作。消息认证码方式不需执行如下操作。
cmp-request verification-cert cert-file-name
● 如果配置了此命令，并且CMPv2服务器的响应报文是签名方式时，则设备使用该命令行配置的cert-file-name证书来验证CMPv2服务器的响应签名。此处配置的证书为CA证书，即CA自身的证书。
说明如果存在RA，且证书注册请求消息由RA机构进行签发，此时cert-file-name需要配置为RA机构的CA证书，否则证书校验失败，证书申请失败。
● 如果未配置此命令，并且CMPv2服务器的响应报文是签名方式时，则依据设备以及CMPv2服务器响应中的证书构建证书链，验证CMPv2服务器的响应签名。
步骤11 根据实际情况配置申请本地证书的方式。
● 使用消息认证码方式首次申请本地证书（IR）。
a. 配置使用CMPv2协议进行首次证书申请（IR）的认证方式。
cmp-request origin-authentication-method message-authentication-code缺省情况下，使用CMPv2协议进行首次证书申请（IR）的认证方式为消息认证码方式。
b. 配置消息认证码的参考值和秘密值。
cmp-request message-authentication-code reference-value [ secret-value ] quit说明消息认证码的秘密值，可以从CMPv2服务器Web界面下的“CMP secret key”参数获取。参考值用户可以自己设置：输入字符串形式，区分大小写，不支持问号，明文时输入长度范围是1～128，密文时输入长度范围是48～188。
c. 在系统视图下，根据CMP会话的配置信息向CMPv2服务器进行首次证书申请（IR）。
pki cmp initial-request session session-name配置后，系统首先会检查CMP会话中的配置是否可以进行证书申请。如果条件不满足，会给出错误的提示信息。如果条件满足，会依据配置内容发起首次证书请求。申请下来的证书将以文件的形式保存到存储介质中，不会执行

导入内存的操作。同时，若服务器端在响应中给出CA证书，则CA证书也会以文件形式保存起来。
● 使用签名方式首次申请本地证书（IR）。
a. 配置使用CMPv2协议进行首次证书申请（IR）的认证方式。
cmp-request origin-authentication-method signature
b. 配置CMPv2请求中用于证明身份的证书。
cmp-request authentication-cert cert-name quit此证书是额外证书，并且必须由受CA信任的证书申请机构为设备颁发。
c. 在系统视图下，根据CMP会话的配置信息向CMPv2服务器进行首次证书申请（IR）。
pki cmp initial-request session session-name配置后，系统首先会检查CMP会话中的配置是否可以进行证书申请。如果条件不满足，会给出错误的提示信息。如果条件满足，会依据配置内容发起首次证书请求。申请下来的证书将以文件的形式保存到flash:/pki/public存储路径下，不会执行导入到设备内存的操作。同时，若服务器端在响应中给出CA证书，则CA证书也会以文件形式保存起来。
● 使用签名方式非首次申请本地证书（CR）
a. 配置CMPv2请求中用于证明身份的证书。
cmp-request authentication-cert cert-name quit此证书是额外证书，并且必须由受CA信任的证书申请机构为设备颁发。
b. 在系统视图下，根据CMP会话的配置信息向CMPv2服务器进行证书申请（CR）。
pki cmp certificate-request session session-name配置后，系统首先会检查CMP会话中的配置是否可以进行证书申请。如果条件不满足，会给出错误的提示信息。如果条件满足，会依据配置内容发起证书请求。申请下来的证书将以文件的形式保存到存储介质中，不会执行导入内存的操作。
步骤12 根据实际情况选择更新本地证书的方式。
● 手动更新本地证书
a. 进入CMP会话视图，配置CMPv2请求中用于证明身份的证书。
pki cmp session session-name cmp-request authentication-cert cert-name quit此证书是CA已经颁发给设备的本地证书，同时也是将要被更新的本地证书。
b. 在系统视图下，根据 CMP 会话的配置信息向 CMPv2 服务器进行密钥更新请求（KUR）。
pki cmp keyupdate-request session session-name向CMPv2服务器进行密钥更新请求时，同时也会重新申请本地证书。
配置后，系统首先会检查CMP会话中的配置是否可以进行证书更新申请。如果条件不满足，会给出错误的提示信息。如果条件满足，会依据配置内容发起证书更新请求。申请下来的证书将以文件的形式保存到存储介质中，不会执行导入内存的操作。
● 自动更新证书
a. 进入 CMP 会话视图，配置 CMPv2 请求中用于证明身份的证书。
pki cmp session session-name cmp-request authentication-cert cert-name此证书是CA已经颁发给设备的本地证书，同时也是将要被更新的本地证书。

b. 开启使用CMPv2方式自动更新证书功能。
certificate auto-update enable
c. 配置证书自动更新的时间，以当前使用证书有效期的百分比形式体现。
certificate update expire-time valid-percent
quit
缺省情况下，证书更新时间的默认百分比是50%。
配置后，当系统检测到时间达到valid-percent时，会自动发起证书更新请
求，并依据cmp-request rsa local-key-pair命令的配置决定是否创建新的
RSA密钥对。申请到新的证书后，系统会使用新的证书和RSA密钥对替换原有
的证书和RSA密钥对。
----结束
检查配置结果
执行命令display pki cmp statistics [ session session-name ]，查看CMP会话的统
计信息。

#### 10.7.3 安装本地证书

背景信息通过CMPv2协议在线申请本地证书，系统会自动将本地证书存放在flash:/pki/public存储路径下。
通过自动更新获取的本地证书会自动安装，手动方式获取的本地证书存放在上述指定路径下后，还需手动导入到设备的内存中。只有将本地证书导入到设备的内存中，在设备重启后系统才能自动加载证书文件。
说明请确保本地证书文件不超过1M，避免安装失败。
初始的本地证书作为华为设备的身份标识，缺省情况下为设备中的用户登录业务提供证书认证。
操作步骤步骤1 进入系统视图。
system-view步骤 2 将本地证书导入到设备的内存中。
● 当在本PKI实体下创建RSA密钥对，通过PKI实体信息和RSA密钥对去CA申请本地证书时，只需执行如下命令导入本地证书到内存中即可，因为在本地创建RSA密钥对时RSA密钥已经默认导入到设备的内存中。
pki import-certificate local [ [ realm realm-name ] { der | pkcs12 | pem } ] filename file-name [ cert-name cert-name ] [ no-check-hash-alg ] [ no-check-same-name ]
● 当使用其他PKI实体产生的密钥对和其他PKI实体的证书时，需要导入证书和密钥对文件。一般证书及其密钥对有两种存在形式，一种是证书文件中包含密钥对文件，两者以一个文件的形式存在；另一种是证书和密钥对相互独立以两个文件形式存在。
不同形式下，将其导入内存所使用的方法不同，具体如下。
– 证书文件中包含密钥对文件。
pki import rsa-key-pair keyname { pem | pkcs12 } filename [ exportable ] [ password password ]

– 证书文件和密钥对文件独立存在。
\# 导入证书文件。
pki import-certificate local [ [ realm realm-name ] { der | pkcs12 | pem } ] filename file-
name [ cert-name cert-name ] [ no-check-hash-alg ] [ no-check-same-name ]
\# 导入密钥对文件。
pki import rsa-key-pair keyname exclude-cert { pem | pkcs12 } filename [ exportable ]
[ password password ]
说明
若不指定待导入证书的格式，系统将自行识别导入。
步骤3 可选: 配置内存中的本地证书的过期预告警时间。
pki set-certificate expire-prewarning day
步骤4 可选: 配置内存中的本地证书的过期检查周期。
pki certificate expiration-check interval interval-time
----结束
检查配置结果
执行命令display pki certificate local [ realm realm-name | filename
filename ]，查看设备上已加载的本地证书的内容。

#### 10.7.4 检查证书有效性

前提条件已在设备上安装CA证书和本地证书。
背景信息在安装CA证书和本地证书以后，使用每一个证书之前，必须对本地设备的证书进行验证，以确保证书的合法性。证书验证包括对签发时间、签发者信息以及证书的有效性几方面进行验证。证书验证的核心是检查CA在证书上的签名，并确定证书仍在有效期内，而且未被撤销。
为完成证书验证，本地设备需要下面的信息：CA证书、CRL、本地证书及其私钥及证书认证相关配置信息。
本地证书验证的主要过程如下：
1. 使用CA证书的公钥验证CA的签名是否正确。
为验证一个证书的合法性，首先需要获得颁发这个证书的CA的公钥（即获得CA证书），以便检查该证书上CA的签名。一个CA可以让另一个更高层次的CA来证明其证书的合法性，这样顺着证书链，验证证书就变成了一个迭代过程，最终这个链必须在某个“信任点”（一般是持有自签名证书的根CA或者是PKI实体信任的中间CA）处结束。
任何PKI实体，如果它们共享相同的根CA或子CA，并且已获取CA证书，都可以验证对端证书。
证书链的验证过程是一个从目标证书（待验证的PKI实体证书）到信任点证书逐层验证的过程。一般情况下，当验证对端证书链时，验证过程在碰到第一个可信任的证书或CA机构时结束。

2. 根据证书的有效期，验证证书是否过期。
3. 检查证书的状态，即通过CRL、OCSP和None方式检查证书是否被撤销。
操作步骤
步骤1 进入系统视图。
system-view
步骤2 检查CA证书或本地证书的有效性。
pki validate-certificate { ca | local } { realm realm-name | filename file-name }
pki validate-certificate ca命令只能验证根CA的CA证书有效性，不能验证从属CA的
CA证书有效性。在多级CA的环境中，当设备上导入了多个CA证书时，只能使用pki
validate-certificate local命令来验证从属CA的CA证书有效性。
----结束

### 10.8 配置自签名证书

背景信息如果设备无法向CA申请本地证书，可以通过设备生成自签名证书，生成的证书以文件形式保存在存储器中，实现简单的证书颁发功能。用户可以将证书导出供其他设备使用。自签名证书是用自己的私钥签署的数字证书，证书颁发者和证书主题名相同。
说明设备不支持对其生成的自签名证书和使用缺省内置的自签名证书颁发的本地证书进行生命周期管理（如证书更新、证书撤销等），为了确保设备和证书的安全，建议用户替换为自己的本地证书。
操作步骤步骤1 进入系统视图。
system-view步骤2 创建自签名证书或本地证书。
pki create-certificate [ self-signed ] filename file-name配置时，会提示用户输入证书的一些信息，比如PKI实体属性、证书文件名称、证书有效期和RSA密钥长度等。
指定self-signed参数时，创建自签名证书。不指定此参数时，设备使用缺省内置的自签名证书颁发本地证书。
创建的自签名证书或本地证书的文件格式为PEM。
----结束

### 10.9 验证对端实体证书

#### 10.9.1 配置证书撤销状态检查

背景信息PKI实体两端建立安全连接时，经常需要检查对端实体的本地证书是否有效，如果无效，两端就不能建立连接。但由于用户名称的改变、私钥泄露或业务中止等原因，有时CA机构需要撤销公钥及相关的PKI实体的绑定关系。PKI实体需要及时获取到对端实体证书的状态才能保证两端的通信安全。
设备提供几种检查证书状态的方式：CRL方式、None方式。
如果配置了多种撤销状态的检查方式，系统会按照配置的先后顺序执行。当前一种方式不可用（如服务器连接不上）时才会使用后边的方式。当前面配置的CRL方式不可用时，如果配置了None方式，此时认为证书有效。以配置了certificate-check crl ocsp none命令为例，先使用CRL方式检查证书是否有效，如果CRL方式不可用，则认为证书是有效的。
用户可以根据实际需求灵活选取检查证书状态的方式。
● CRL 方式CRL方式是利用CRL存储库对CRL信息存储的功能，通过查询证书是否包含在证书撤销列表中，确定证书的状态。任何一个证书被撤销以后，证书的序列号都会被记录在CRL证书撤销列表中。当PKI实体验证本地证书时，先查找本地内存的CRL，如果本地内存没有CRL，则需下载CRL并安装到本地内存中，如果对端实体的本地证书在CRL中，表示此证书已被撤销。
图 10-13 CRL 方式证书验证流程说明PKI实体可以通过LDAPv3模板方式下载CRL。PKI实体必须经常下载CRL以确保列表的更新。设备缺省分配了大约5K的内存空间用于处理和缓存CRL，如果超出设备给CRL预留的存储空间大小，则新的证书撤销数据不能导入进去。如果想要导入新的证书撤销数据，需要删除旧的证书撤销数据。
● None方式如果PKI实体没有可用的CRL，或者不需要检查PKI实体的本地证书状态，可以采用None方式，即不检查证书是否被撤销。

说明全局证书撤销状态检查方式有CRL方式和None方式。
PKI域中的证书撤销状态检查方式有CRL方式和None方式。
操作步骤步骤1 进入系统视图。
system-view步骤2 创建PKI域并进入PKI域视图，或者直接进入PKI域视图。
pki realm realm-name缺省情况下，系统下存在名称为default的PKI域，该域可以修改但不能删除。
步骤3 配置PKI域中证书撤销状态的检查方式。
* certificate-check { { crl | ocsp } [ none ] | none }缺省情况下，系统未配置PKI域中证书撤销状态的检查方式。
如果没有配置本命令，将以全局的证书撤销状态检查方式为准，即以在系统视图下配置的pki certificate-check crl [ none ]命令、pki certificate-check none命令或undo pki certificate-check命令为准。
步骤4 请根据CA提供的服务方式选择配置检查对端实体本地证书状态的方式。
● 自动更新CRL方式
a. 退出到系统视图。
quit
b. 配置设备保存CRL时的文件格式。
pki file-format { der |pem }说明缺省情况下，设备保存CRL时的文件格式为PEM。
可选: 开启全局证书撤销状态CRL方式检查功能。
c.
pki certificate-check crl [ none ]缺省情况下，全局证书吊销状态的CRL检查处于开启状态，且当CRL方式不可用时认为证书有效。
d. 进入PKI域视图，开启CRL自动更新功能。
pki realm realm-name crl auto-update enable缺省情况下，CRL自动更新功能处于关闭状态。
配置CRL自动更新的时间间隔。
e.
crl update-period interval缺省情况下，CRL自动更新的时间间隔为8小时。
f. 配置向LDAP服务器获取CRL时使用的属性和标识符。
crl ldap [ attribute attr-value ] dn dn-value缺省情况下，系统未配置向LDAP服务器获取CRL时使用的属性和标识符。
g. 配置通过LDAPv3模板方式自动更新CRL。
ldap-server-template template-name ldap-server-template template-name用来在PKI域下引用LDAP服务器模板。LDAP服务器模板的具体配置，请参见《CLI配置指南-用户接入与认证配置》的“AAA配置”中的“配置对接的LDAP服务器”节点。

h. 可选: 立即更新CRL，将CRL导入设备的内存中。
自动更新CRL需要达到CRL自动更新的时间时才能更新，如果想要立刻更新
CRL信息，则可以使用立即更新CRL功能。
pki get-crl realm realm-name
pki import-crl realm realm-name filename file-name
立即更新CRL后，新的CRL会替换设备存储介质中原来的CRL，同时新的CRL
也会被自动导入设备内存中替换原来的CRL。
i. 可选: 打开CRL过期检查开关，配置内存中的CRL过期检查周期和CRL过期预
告警剩余百分比。
pki crl expiration-check enable
pki crl expiration-check interval interval-time
pki crl expiration-check prewarning remain-percent percent
● 手动更新CRL方式
a. 退出到系统视图。
quit
b. 配置设备保存CRL时的文件格式。
pki file-format { der | pem }
c. 根据LDAP方式下载CRL。
pki ldap-server-template template-name attribute attr-value save-name dn dn-value
d. 将CRL导入设备的内存中。
pki import-crl [ realm realm-name ] filename file-name
----结束
检查配置结果
● 执行命令display pki crl [ realm realm-name | filename file-name ]，查看设
备中的CRL内容。
● 执行命令display pki certificate ocsp [ realm realm-name | filename file-
name ]，查看设备上已加载的OCSP服务器证书的内容。
后续处理
如果CRL过期或者不使用时，可以执行命令pki delete-crl { realm realm-name |
filename filename }，从内存中删除CRL。

#### 10.9.2 配置证书属性过滤实现访问控制

背景信息证书属性过滤是证书验证的一种方式，通过配置证书属性访问控制策略，使得只有符合特定属性条件的证书才能通过验证，进而对访问权限进行精细化控制。
证书属性访问控制策略是由证书属性组、证书属性条件和证书属性控制原则组成，通过在证书属性组里定义证书的属性条件，当某个证书与所有的证书条件匹配时，证书属性控制规则决定是否允许此证书通过。
证书属性条件包含如下：

| 证书属性条件 | 说明 |
|---|---|
| 证书有效期的开始和结束的时间 | PKI实体本地证书的有效的起、止日期 |

| 证书属性条件 | 说明 |
|---|---|
| FQDN名称（域名） | PKI实体本地证书的FQDN名称 FQDN由一个主机名和域名组成，例如 www.example.com。 |
| 证书的IP地址 | PKI实体本地证书的IP地址 |
| 证书颁发者名 | PKI实体本地证书的颁发者名称 |
| 证书主题名 | PKI实体本地证书的主题名 |

证书属性控制规则包含permit和deny两种动作。他决定对满足证书属性条件的证书是允许通过还是阻断，用户可以根据不同场景灵活使用。
通过证书属性过滤实现访问控制的匹配规则如下：
● 如果业务已经指定了证书属性访问控制策略，则使用其指定的证书属性访问控制策略，否则使用缺省的证书属性访问策略。缺省情况下，设备上缺省的证书属性访问控制策略中的证书属性控制规则动作为Permit，即允许证书通过验证。
● 如果一个证书属性访问控制策略中配置了多条控制规则，它们之间的关系为“或”，即待验证的证书匹配上了一条属性规则，并执行相应的动作后，不再继续匹配余下的属性规则。
● 如果一个证书属性组中配置了多条证书属性条件，它们之间的关系为“与”，即待验证的证书匹配上了所有的证书属性条件后，才会执行相应的证书属性控制规则中定义的动作。
操作步骤步骤1 进入系统视图。
system-view步骤2 配置缺省的证书属性访问控制策略。
pki certificate access-control-policy default { deny | permit }缺省情况下，缺省的证书属性访问控制策略中的动作为permit，即允许证书通过验证。
步骤3 创建证书属性组并进入证书属性组视图，或者直接进入证书属性组视图。
pki certificate attribute-group group-name步骤4 配置证书的属性条件。

| 操作 | 命令 |
|---|---|
| 配置证书有效期的开始和结束的时间 | attribute id validity from begintime begindate to endtime enddate |
| 配置FQDN名称 | attribute id alt-subject-name fqdn { ctn | equ | nctn | nequ } attribute- value |

| 操作 | 命令 |
|---|---|
| 配置证书的IP地址 | attribute id alt-subject-name ip { ctn | equ | nctn | nequ } ip-address |
| 配置证书颁发者名 | attribute id issuer-name dn { ctn | equ | nctn | nequ } attribute-value |
| 配置证书主题名 | attribute id subject-name dn { ctn | equ | nctn | nequ } attribute-value |

步骤5 返回至系统视图。
quit步骤6 创建证书属性访问控制策略并进入证书属性访问控制策略视图，或者直接进入证书属性访问控制策略视图。
pki certificate access-control-policy name policy-name缺省情况下，未创建证书属性访问控制策略。
步骤7 配置证书属性控制规则。
rule id { permit | deny } group-name缺省情况下，系统未配置证书属性控制规则。
步骤8 配置证书属性访问控制策略的描述信息。
description description缺省情况下，系统没有配置证书属性访问控制策略的描述信息。
步骤9 调整证书属性访问控制策略规则的先后顺序。
pki certificate access-control-policy [ policy-name policy-name ] rule move rule-id1 { before | after } rule-id2调整证书属性访问控制策略规则时，rule-id保持不变，只是进行内容交换。例如：
原证书属性访问控制策略a的规则如下：
pki certificate access-control-policy name a rule 5 permit test1 rule 20 permit test2执行pki certificate access-control-policy policy-name a rule move 20 before 5命令后，规则如下：
pki certificate access-control-policy name a rule 5 permit test2 rule 20 permit test1步骤10 退出证书属性访问控制策略视图。
quit
----结束检查配置结果
● 在用户视图下执行命令 display pki certificate access-control-policy all ，查看所有访问控制策略的信息。
● 在用户视图下执行命令display pki certificate attribute-group all，查看所有的证书属性组信息。

#### 10.9.3 配置证书白名单实现访问控制

前提条件证书白名单文件需要提前存放在设备的flash:/pki/public存储路径下。
背景信息证书白名单是指将基站证书的通用名称（CN）或序列号加入到白名单列表中。当本端设备收到对端设备的证书认证时，如果对端证书的通用名称或序列号可以匹配设备中的证书白名单，则证书认证就会通过。
要使PKI证书白名单检查功能生效，需将证书白名单导入到设备的内存中。
操作步骤
● 导入证书白名单到设备的内存中。
system-view pki import whitelist filename file-name
● 删除证书白名单。
system-view pki delete whitelist filename file-name
----结束检查配置结果执行命令display pki whitelist { all | filename file-name }，查看设备上证书白名单的内容。

### 10.10 导入导出证书

#### 10.10.1 导入其他设备的RSA/SM2/ECC密钥对和证书

背景信息现网场景中，如果自己的设备没有申请证书需要将其他设备的证书导入到自己设备中使用，可以通过导入其他设备的 RSA/SM2/ECC 密钥对和证书功能实现。
操作步骤步骤1 在设备A上导出RSA/SM2/ECC密钥对和证书。
pki export rsa-key-pair keyname [ and-certificate certificate-name ] { pem filename [ aes ] | pkcs12 filename } password password pki export sm2-key-pair keyname pem filename [ password password ] pki export ecc-key-pair keyname [ and-certificate certificate-name ] { pem filename [ aes ] | pkcs12 filename } password password步骤 2 通过 SFTP 等方式将设备 A 存储卡中的密钥文件保存到 PC 。
步骤3 通过SFTP等方式将PC中密钥文件保存到设备B的存储卡中。
步骤4 在设备B上导入设备A上的RSA/SM2/ECC密钥对和证书。

pki import rsa-key-pair keyname [ exclude-cert ] { pem | pkcs12 } filename [ exportable ] [ password password ] pki import sm2-key-pair keyname pem filename [ exportable ] signkey signkey-name [ certificate certificate-name ] pki import ecc-key-pair keyname [ exclude-cert ] { pem | pkcs12 } filename [ exportable ] [ password password ]
----结束

#### 10.10.2 导入对端实体的证书

背景信息导入对端实体的证书场景适合在大规模网络时部署。
当导入的对端实体的证书不需要使用时，可以将对端实体的证书释放。
操作步骤
● 导入对端实体的证书到设备的内存中。
system-view pki import-certificate peer peer-name { der | pem | pkcs12 } filename filename [ cert-name cert- name ] [ no-check-same-name ]
● 释放对端实体的证书。
system-view pki release-certificate peer { name peer-name | all }
----结束检查配置结果执行命令display pki peer-certificate { name peer-name | all }，查看已导入的对端实体证书。

#### 10.10.3 导出证书

背景信息设备支持把CA证书、本地证书、OCSP服务器证书拷贝到其他设备上使用，证书可以灵活导出，方便其他设备使用。执行如下命令操作可以将证书导出到设备存储介质中，然后用户可以通过FTP/SFTP取出证书。
操作步骤
● 在系统视图下将CA证书导出，拷贝到其他设备上使用。
pki export-certificate ca realm realm-name { pem | pkcs12 }
● 在系统视图下将系统缺省内置的CA证书拷贝到其他设备上使用。
pki export-certificate default ca filename file-name
● 在系统视图下将本地证书拷贝到其他设备上使用。
pki export-certificate local realm realm-name { pem | pkcs12 }
● 在系统视图下将 OCSP 服务器证书拷贝到其他设备上使用。
pki export-certificate ocsp realm realm-name { pem | pkcs12 }
----结束

### 10.11 维护PKI

#### 10.11.1 删除证书

背景信息本地证书过期或者重新申请新的证书时，可以删除设备内存中的本地证书。如果需要删除内存中的证书，可选择在系统视图下执行以下命令。
表 10-8 删除证书和 RSA 密钥对

| 操作 | 命令 |
|---|---|
| 从内存中删除本地证书 | pki delete-certificate local { realm realm- name | filename file-name } |
| 从内存中删除CA证书 | pki delete-certificate ca { realm realm-name | filename file-name } |
| 从内存中删除OCSP服务器证书 | pki delete-certificate ocsp { realm realm- name | filename file-name } |

#### 10.11.2 清除PKI信息

背景信息清空PKI信息后，以前的信息将无法恢复，务必仔细确认。请在用户视图下执行以下命令。
操作步骤
● 清除OCSP响应缓存。
reset pki ocsp response cache
● 清除设备上记录的OCSP服务器DOWN状态信息。
reset pki ocsp server down-information [ url [ esc ] url-addr ]
● 清除已经导入内存的CA证书、CRL、本地证书和OCSP响应器证书的内容。
reset pki global-ca说明该命令行将删除已经导入设备内存中的所有CA证书、CRL和本地证书、OCSP响应器证书等内容，请谨慎操作。
----结束

#### 10.11.3 将被覆盖的文件移动到回收站

背景信息覆盖文件时，被覆盖的文件默认彻底删除，无法恢复。如果用户希望被覆盖的文件能够恢复，以防止新文件不可用，此时可以配置被覆盖的文件删除到回收站功能。
该功能仅适用于以下场景：
● 执行命令pki get-crl、pki import-crl覆盖已有的CRL。
● 执行命令pki enroll-certificate、pki create-certificate、pki export- certificate、pki export-certificate default、pki import-certificate peer覆盖已有的证书。
● 执行命令pki import rsa-key-pair、pki export rsa-key-pair覆盖已有的RSA密钥对、证书。
操作步骤步骤1 进入系统视图。
system-view步骤2 开启被覆盖的文件删除到回收站功能。
pki recycle-bin enable缺省情况下，被覆盖的文件被彻底删除。
----结束

#### 10.11.4 配置PKI加入到指定的VPN内

背景信息当CA等服务器位于某个VPN内时，为了让设备可以与这些服务器进行通信以实现证书的获取或有效性校验等功能，此时需配置PKI域加入到指定的VPN内。
操作步骤
● PKI域视图
a. 进入系统视图。
system-view
b. 创建PKI域并进入PKI域视图，或者直接进入PKI域视图。
pki realm realm-name
c. 将PKI加入到指定的VPN内。
vpn-instance { vpn-instance-name }缺省情况下，系统未将PKI加入到任何VPN内。
vpn-instance-name参数可通过命令ip vpn-instance配置。
d. 退出PKI实体视图。
quit
● CMP会话视图

#### 10.12.1 举例：为PKI实体离线申请本地证书

CMP会话视图下，将PKI到指定的VPN内。仅在通过CMPv2在线申请和更新证书场景下使用。
a. 进入系统视图。
system-view
b. 创建CMP会话并进入CMP会话视图，或者直接进入CMP会话视图。
pki cmp session session-name缺省情况下，系统未创建CMP会话。
CMP会话是一个本地概念，一个设备上配置的CMP会话对CA和其他设备是不可见的。
c. 将PKI加入到指定的VPN内。
vpn-instance vpn-name { vpn-instance-name } quit缺省情况下，系统未将PKI加入到任何VPN内。
vpn-instance-name参数可通过命令ip vpn-instance配置。
----结束

#### 10.11.5 校验和查看初始证书

背景信息设备出厂时，设备会加载CA证书和本地证书，并存放到NVRAM内存中，且不支持删除和修改。该初始证书可以作为设备的身份标识，导入到default域中，保证设备及外部通信的安全性。
缺省情况下，设备出厂时已校验初始证书的有效性，一般情况下，用户无需对初始证书进行校验。
操作步骤
● 校验初始证书有效性。
pki validate-certificate device slot slot-id
● 查看初始证书的内容。
display pki certificate device slot slot-id
----结束

### 10.12 PKI配置举例

举例：为 实体离线申请本地证书
10.12.1 PKI组网需求如图 10-14 所示，设备向公网上的 CA 服务器离线申请本地证书。
说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。

图 10-14 配置为 PKI 实体离线申请本地证书组网图配置思路采用如下思路配置为PKI实体离线申请本地证书：
1. 创建RSA密钥对，实现申请本地证书时携带的公钥。
2. 配置PKI实体，实现申请本地证书时携带的PKI实体信息，用来标识PKI实体的身份。
3. 配置为PKI实体离线申请本地证书，生成本地证书请求文件。
4. 通过带外方式发送本地证书请求文件来申请本地证书，并通过带外方式下载本地证书。
5. 安装本地证书，使得设备可以使用证书来保护通信。
操作步骤步骤1 配置接口的IP地址。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] undo portswitch [DeviceA-10GE1/0/1] ip address 10.2.0.2 24 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] undo portswitch [DeviceA-10GE1/0/2] ip address 10.1.0.2 24 [DeviceA-10GE1/0/2] quit步骤2 创建RSA密钥对。
创建一个3072位的RSA密钥对rsakey，并设置为可以从设备上导出。
[DeviceA] pki rsa local-key-pair create rsakey exportable Info: The name of the new key-pair will be: rsakey The size of the public key ranges from 2048 to 4096.
Input the bits in the modulus:3072 Generating key-pairs...
Generating key-pairs finished步骤3 配置PKI实体，标识申请证书PKI实体的身份信息。
配置PKI实体为user01。
[DeviceA] pki entity user01 [DeviceA-pki-entity-user01] common-name hello

[DeviceA-pki-entity-user01] country cn [DeviceA-pki-entity-user01] email user@test.abc.com [DeviceA-pki-entity-user01] fqdn test.abc.com [DeviceA-pki-entity-user01] ip-address 10.2.0.2 [DeviceA-pki-entity-user01] state jiangsu [DeviceA-pki-entity-user01] organization huawei [DeviceA-pki-entity-user01] organization-unit info [DeviceA-pki-entity-user01] quit步骤4 配置为PKI实体离线申请本地证书。
[DeviceA] pki realm abc [DeviceA-pki-realm-abc] entity user01 [DeviceA-pki-realm-abc] rsa local-key-pair rsakey [DeviceA-pki-realm-abc] quit [DeviceA] pki enroll-certificate realm abc pkcs10 filename cer_req Info: Creating certificate request file...
Info: Create certificate request file successfully.
已完成配置后，可执行命令display pki cert-req查看证书请求文件的内容。
[DeviceA] display pki cert-req filename cer_req Certificate Request:
Data:
Version: 1 (0x0)
Subject: C=cn, ST=jiangsu, O=huawei, OU=info, CN=hello Subject Public Key Info:
Public Key Algorithm: rsaEncryption RSA Public-Key: (3072 bits)
Modulus:
00:a2:db:e3:30:17:8e:f6:2d:2e:64:15:46:51:ad:
70:86:dd:32:c4:bb:6b:58:3a:8c:5f:a0:06:a1:e1:
56:2e:a4:eb:7e:12:06:05:04:28:b2:6d:64:7a:9c:
4f:85:24:c1:aa:b8:99:dc:e9:bb:c4:1e:e2:9d:a0:
18:51:1f:ad:b5:2f:60:18:06:8b:c1:cc:6f:32:58:
f2:21:2c:16:e8:29:c2:a8:c5:aa:9d:6c:1e:ca:14:
fc:7a:e9:bc:07:91:ce:ed:a0:c0:52:d9:0c:e9:ba:
9b:64:43:e0:9a:3f:c5:d1:2c:86:36:96:6b:4b:4f:
d4:df:05:d0:4b:41:2c:ec:0a:d7:0e:45:83:ed:cd:
07:78:40:ed:d5:3d:7f:fe:0f:08:90:04:2e:ac:e5:
42:b9:81:ea:ec:77:e2:cc:04:6e:e4:63:9f:69:ed:
60:06:5e:c7:e8:bf:30:57:6a:5d:e0:46:68:d3:ee:
b0:da:47:24:e3:b6:a5:f3:20:d8:5a:75:92:70:c2:
a9:a6:97:07:07:0d:1c:94:9a:03:6f:f7:8c:db:6f:
b7:06:de:51:50:9e:71:fd:86:f3:b5:c9:99:05:bf:
f1:10:20:28:d3:a6:29:3d:e0:f4:a7:ba:1e:27:85:
a9:66:fc:a9:90:49:f0:35:f7:d9:6d:06:a2:43:3f:
18:87 Exponent: 65537 (0x10001)
Attributes:
Requested Extensions:
X509v3 Key Usage:
Digital Signature, Non Repudiation, Key Encipherment, Data Encipherment X509v3 Subject Alternative Name:
IP Address:10.2.0.2, DNS:test.abc.com, email:user@test.abc.com Signature Algorithm: sha256WithRSAEncryption 0e:0a:a5:b7:d5:54:11:10:c4:ea:ff:77:da:f9:24:4b:a9:98:
a1:75:36:08:10:59:60:fa:1a:30:70:2c:b7:f6:5f:5e:31:b7:
55:a5:7a:26:e5:af:4a:cd:83:c5:f3:90:f3:b9:d5:f9:0a:6d:
6e:8f:25:b4:ed:95:9c:75:a5:d7:b6:25:fc:8d:39:89:fb:af:
37:fc:01:7b:09:07:9c:96:7c:fa:28:6d:e2:11:49:a7:95:94:
ed:26:5b:ca:f8:98:b0:e7:64:7e:dd:2d:75:ff:89:03:b7:0a:
92:53:25:d4:a1:23:b9:5c:eb:5b:29:1d:8a:92:8f:36:68:7b:
77:32:bc:48:92:48:84:fa:87:5a:d7:2e:3e:be:d5:6b:e4:df:
b1:f2:02:35:91:6a:eb:cd:fc:5a:ea:37:85:6c:12:74:5f:a5:
5c:c0:05:09:cd:34:59:0d:c6:c8:75:ca:1c:18:d6:48:e5:4b:
e7:8e:e3:ff:25:99:0f:2e:a8:b4:c5:8e:4d:8f:dd:64:c5:1f:
61:3c:58:21:4f:d5:35:ba:c8:8e:5f:76:41:9f:27:41:0a:94:
59:2c:59:25:2d:de:60:5c:92:07:ac:8a:a5:7a:ba:75:af:2c:

82:5f:bb:55:a8:48:49:54:0f:99:54:af:8d:12:4d:4b:7d:8b:
95:28:ce:dc步骤5 通过磁盘、电子邮件等带外方式将证书申请文件发送给CA服务器，向CA服务器申请本地证书。
本地证书注册成功后，可以通过带外方式下载本地证书abc_local.cer。下载后，可以通过文件传输协议导入到设备的flash:/pki/public存储路径下。
步骤6 安装本地证书。
证书导入成功后，flash:/pki/public存储路径下的abc_local.cer默认删除，如果不需删除，请根据设备上的提示信息选择N进行保留。
[DeviceA] pki import-certificate local realm abc pem filename abc_local.cer Info: Succeeded in importing the certificate.
Warning: The file in the flash will be deleted. Please select 'N' if you want to keep it. Please select [Y/N]:y Info: Delete Success.
----结束检查配置结果安装本地证书后，两端设备可以使用证书来保护通信。
[DeviceA] display pki certificate local filename abc_local.cer Info: It will take a few seconds or more to collect data for displaying. Please wait a moment.
Total Number: 1 Certificate:
Data:
Version: 3 (0x2)
Serial Number: 8372560407419635446 (0x74314f54b0bf46f6)
Signature Algorithm: sha256WithRSAEncryption Issuer: CN=HUAWEI BRAS CA, O=HUAWEI BRAS, C=AT Validity Not Before: Sep 12 22:18:27 2022 GMT Not After : Sep 7 22:18:27 2042 GMT Subject: C=cn, ST=jiangsu, O=huawei, OU=info, CN=hello Subject Public Key Info:
Public Key Algorithm: rsaEncryption RSA Public-Key: (3072 bits)
Modulus:
00:c8:4f:09:9d:6a:53:95:6d:98:fa:22:f4:7c:5e:
f7:4b:08:3b:d2:19:3b:2d:4c:6c:0d:5f:b7:a2:91:
e8:99:de:91:12:df:3d:f5:c4:89:00:30:e7:7c:a6:
7a:03:18:1e:31:6a:65:34:05:cb:8a:29:f8:65:49:
7c:bd:81:cd:93:8d:be:63:e5:87:99:5d:28:6f:b6:
5c:c6:5c:4e:85:dc:26:26:db:a9:81:1a:19:b4:c4:
72:b7:8f:01:8d:55:8c:a0:58:cd:ef:d2:bd:d2:04:
5c:62:ab:3a:c5:71:d8:46:68:db:30:11:9b:48:46:
f7:5a:f7:70:a9:bf:ce:df:67:50:31:6c:c5:b3:f7:
0c:73:74:33:94:69:18:5b:57:74:5b:6b:49:bf:15:
05:17:01:9f:d0:13:71:c0:fe:45:13:07:2d:95:42:
55:e8:9e:77:e8:4e:f8:80:42:97:4f:26:78:a9:81:
61:8e:d3:ac:e8:5e:e0:61:37:84:f4:82:fa:8a:f9:
08:df:c3:70:50:9a:8e:3b:78:a1:f2:5d:3d:0b:fb:
fa:f4:67:ec:31:35:ff:4a:70:29:86:8c:a8:e2:46:
97:39:f7:58:0e:9e:ff:26:f1:7f:10:6b:68:33:f3:
7e:fd:ce:f3:a2:b1:b5:a4:81:88:52:2f:82:e0:28:
d3:f5 Exponent: 65537 (0x10001)
X509v3 extensions:
X509v3 Authority Key Identifier:
keyid:33:06:DB:08:3C:3F:61:9B:C4:04:A5:36:8C:FD:34:D3:4C:73:B9:92 X509v3 Subject Key Identifier:

78:4C:65:05:E7:F6:B5:C8:48:C3:9D:E5:CE:3F:83:3A:62:84:EA:F9 X509v3 CRL Distribution Points:
Full Name:
DirName:CN = pre_crl, OU = CRL, O = HUAWEI BRAS, C = AT Full Name:
URI:http://192.168.1.1:8080/allcrl/pre_crl.crl Full Name:
URI:ldap://www.jitldap.com:5389/CN=pre_crl,OU=CRL,O=HUAWEI BRAS,C=AT?
certificateRevocationList?base?objectclass=cRLDistributionPoint Signature Algorithm: sha256WithRSAEncryption 80:34:0d:ea:a0:7f:b8:a8:cb:8b:ae:a9:b3:85:b3:af:b2:1c:
15:fc:7e:75:70:be:ff:37:75:6e:67:f8:37:33:ed:5c:5e:5b:
3b:13:dc:44:7e:12:b6:85:b3:5c:b9:49:90:6c:96:33:57:a8:
f3:c7:c4:04:2d:36:2a:54:fe:52:9a:16:64:66:a0:2e:a6:f1:
0e:e0:29:f0:ac:69:d6:8a:f6:0d:43:41:ff:df:fd:06:03:39:
75:8c:36:50:99:c3:89:c7:59:8c:65:7c:0c:6b:86:66:f3:a1:
b1:6a:b7:43:0b:6d:3f:7d:82:27:45:b0:75:da:95:07:1d:d2:
59:78:88:12:67:26:0f:65:fd:4f:05:4c:7c:74:16:4b:7d:ac:
f8:a9:d1:2f:d6:57:4a:ad:aa:a3:ac:7c:30:de:6f:cf:3f:b4:
d6:c5:84:e1:55:88:a2:40:52:12:5f:08:d8:50:54:ea:e7:c3:
43:e2:6e:98:2a:5d:a4:e9:38:06:36:d6:40:25:a2:2e:0f:e1:
95:cc:e8:f9:25:37:75:dd:67:0e:b9:0f:a9:5a:83:9c:6b:6c:
f6:e1:bc:9d:fc:c1:a7:76:3f:33:81:e9:6d:25:a2:9f:1b:4e:
61:f8:a9:12:de:33:02:2a:98:9d:04:a1:87:98:94:c4:11:cc:
af:07:1b:68 Pki realm name: abc Certificate file name: abc_local.cer Certificate peer name: -配置脚本\# sysname DeviceA \# pki entity user01 country cn state jiangsu organization huawei organization-unit info common-name hello fqdn test.abc.com ip-address 10.2.0.2 email user@test.abc.com \# pki realm abc entity user01 rsa local-key-pair rsakey \# interface 10GE1/0/1 ip address 10.2.0.2 255.255.255.0 \# interface 10GE1/0/2 ip address 10.1.0.2 255.255.255.0 \# return

#### 10.12.2 举例：通过CMPv2协议在线申请和更新本地证书

组网需求如图所示，某企业在网络边界处部署了DeviceA作为出口网关，使用CMPv2协议向公网上的CA服务器在线首次申请证书，申请成功后自动将本地证书下载到设备存储介质中。当证书的有效期时间达到80%时，自动更新本地证书。
图 10-15 配置为 PKI 实体在线申请本地证书组网图说明本例中interface1、interface2分别代表10GE1/0/1、10GE1/0/2。
说明配置前请确保各设备之间路由可达。
配置思路采用如下思路配置通过CMPv2协议为PKI实体首次申请本地证书：
1. 配置接口的IP地址。
2. 创建RSA密钥对，实现申请本地证书时携带公钥。
3. 配置 PKI 实体，实现申请本地证书时携带 PKI 实体信息用来标识 PKI 实体的身份。
4. 通过CMPv2协议申请和自动更新证书，并使用消息认证码来验证消息，实现自动下载CA和本地证书。
5. 安装本地证书，实现证书生效，即设备可以使用证书来保护通信。
数据准备为完成此配置示例，需准备如下的数据：
● CA名称：为CA证书的主题字段。
● 消息认证码的参考值和秘密值：需要从CMPv2服务器上获取消息认证码的参考值和秘密值。
● 在设备上导入CA服务器的CA证书。

操作步骤步骤1 配置接口的IP地址。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] interface 10ge 1/0/1 [DeviceA-10GE1/0/1] undo portswitch [DeviceA-10GE1/0/1] ip address 10.2.0.2 24 [DeviceA-10GE1/0/1] quit [DeviceA] interface 10ge 1/0/2 [DeviceA-10GE1/0/2] undo portswitch [DeviceA-10GE1/0/2] ip address 10.1.0.2 24 [DeviceA-10GE1/0/2] quit步骤2 创建RSA密钥对。
创建一个3072位的RSA密钥对rsa_cmp，并设置为可以从设备上导出。
[DeviceA] pki rsa local-key-pair create rsa_cmp exportable Info: The name of the new key-pair will be: rsa_cmp The size of the public key ranges from 2048 to 4096.
Input the bits in the modulus:3072 Generating key-pairs...
Generating key-pairs finished步骤3 配置PKI实体，标识申请证书PKI实体的身份信息。
配置PKI实体为user01。
[DeviceA] pki entity user01 [DeviceA-pki-entity-user01] common-name hello [DeviceA-pki-entity-user01] country cn [DeviceA-pki-entity-user01] email user@test.abc.com [DeviceA-pki-entity-user01] fqdn test.abc.com [DeviceA-pki-entity-user01] ip-address 10.2.0.2 [DeviceA-pki-entity-user01] state jiangsu [DeviceA-pki-entity-user01] organization huawei [DeviceA-pki-entity-user01] organization-unit info [DeviceA-pki-entity-user01] quit步骤4 配置CMP会话。
\# 创建CMP会话cmp。
[DeviceA] pki cmp session cmp \# 指定CMP会话引用的PKI实体名称。
[DeviceA-pki-cmp-session-cmp] cmp-request entity user01配置CA的名称，举例中假设为“C=cn,ST=beijing,L=SD,O=BB,OU=BB,CN=BB”。
\#说明配置的CA名称中各个字段的顺序必须要和实际CA证书中的顺序保持一致，否则服务器端会认为是错误的。
[DeviceA-pki-cmp-session-cmp] cmp-request ca-name "C=cn,ST=beijing,L=SD,O=BB,OU=BB,CN=BB"
\# 配置CMPv2服务器的URL，用于PKI实体向该服务器提出证书申请。
[DeviceA-pki-cmp-session-cmp] cmp-request server url http://10.3.0.1:8080 \# 指定申请证书时使用的RSA密钥对，并设置为证书自动更新时同时更新RSA密钥对。
[DeviceA-pki-cmp-session-cmp] cmp-request rsa local-key-pair rsa_cmp regenerate

\# 首次申请证书时，使用消息认证码认证。配置消息认证码的参考值和秘密值，举例中假设分别为“1234”和“Huawei@RSA1234”。
[DeviceA-pki-cmp-session-cmp] cmp-request message-authentication-code 1234 Huawei@RSA1234 [DeviceA-pki-cmp-session-cmp] quit [DeviceA] pki cmp initial-request session cmp获取到的CA、本地证书将会分别被命名为cmp_ca1.cer和cmp_ir.cer保存在设备存储介质中。
步骤5 安装证书。
证书导入后，设备存储介质中cmp_ca1.cer和cmp_ir.cer默认删除，如果不需要删除，请根据设备提示信息选择N进行保留。
\# 导入CA证书到内存。
[DeviceA] pki import-certificate ca filename cmp_ca1.cer The CA's Subject is /C=cn/ST=beijing/L=BB/O=BB/OU=BB/CN=BB The CA's fingerprint is:
SHA1 fingerprint:2C:2B:C0:31:66:A6:95:A0:7A:AC:EF:3D:37:1C:9A:4D:01:BA:09:4D SHA256 fingerprint:CA:FC:6B:94:53:E9:E3:D7:D3:E1:F4:75:3F:DB:C4:0F:0A:B9:F1:AD:03:0B:A8:0D:EE:73:4A:83:54:EF:1F:81 Is the fingerprint correct?(Y/N):y Info: Succeeded in importing the certificate.
Warning: The file in the flash will be deleted. Please select 'N' if you want to keep it. Please select [Y/N]:y Info: Delete Success.
\# 导入本地证书到内存。
[DeviceA] pki import-certificate local filename cmp_ir.cer Info: Succeeded in importing the certificate.
Warning: The file in the flash will be deleted. Please select 'N' if you want to keep it. Please select [Y/N]:y Info: Delete Success.
步骤6 配置自动更新证书功能。
\# 在CMP会话视图下开启使用CMPv2方式自动更新证书功能。
[DeviceA] pki cmp session cmp [DeviceA-pki-cmp-session-cmp] cmp-request authentication-cert cmp_ir.cer [DeviceA-pki-cmp-session-cmp] certificate auto-update enable [DeviceA-pki-cmp-session-cmp] quit \# 在CMP会话视图下配置证书自动更新的时间，设置为当前证书有效期的80%。
[DeviceA] pki cmp session cmp [DeviceA-pki-cmp-session-cmp] certificate update expire-time 80 [DeviceA-pki-cmp-session-cmp] quit
----结束检查配置结果
● 证书申请成功后，可执行命令display pki certificate local查看已经导入内存的本地证书的内容。
[DeviceA] display pki certificate local filename cmp_ir.cer The x509_obj type is Cert:
Certificate:
Data:
Version: 3 (0x2)
Serial Number: 1144733510 (0x443b3f46)
Signature Algorithm: sha1WithRSAEncryption Issuer: C=cn, ST=beijing, L=BB, O=BB, OU=BB, CN=BB Validity Not Before: Jun 12 09:33:10 2012 GMT Not After : Aug 13 02:38:27 2016 GMT Subject: C=cn, ST=jiangsu, O=huawei, OU=info, CN=hello Subject Public Key Info:

Public Key Algorithm: rsaEncryption RSA Public-Key: (3072 bit)
Modulus:
00:d3:12:fe:57:48:c6:a5:10:12:e9:2f:f9:2a:ff:
7b:2a:d8:45:69:11:c4:85:30:c4:9a:4d:0f:ad:58:
e7:56:cd:5c:f0:18:e1:c3:6d:44:c2:c3:5e:64:22:
d1:28:c9:c3:37:3c:34:ed:28:04:7f:62:9e:8b:94:
af:bc:72:de:f6:72:7f:e4:d8:45:31:fd:f9:ac:ce:
5a:b9:c7:1b:23:53:00:28:a6:3b:f5:61:69:5d:ab:
67:cb:bb:e8:96:2f:ce:ab:2c:6b:91:5b:26:91:86:
8f:80:a9:b0:66:c1:16:3d:31:55:a2:d4:b5:5a:af:
85:88:6e:99:f8:f8:53:58:77:26:91:ed:0e:94:ad:
c5:8d:53:67:67:55:08:8d:90:38:e0:5e:96:37:b9:
64:0e:36:e7:cf:9a:d2:77:e4:b0:24:05:a6:eb:03:
6e:ff:f7:ab:be:93:9e:8c:66:7d:31:66:be:6d:c8:
f3:17:9d:86:19:88:21:2d:d9:69:86:5f:b2:55:a4:
db:bc:d7:d0:6b:ac:66:ac:e4:63:9c:66:79:9c:42:
5c:83:b8:9e:4b:6e:67:85:a2:47:19:f1:5c:c0:3c:
c9:a3:47:02:a8:53:69:59:9e:d9:c7:5e:90:83:8d:
ac:cd:21:3c:d5:31:39:49:84:e6:f8:f4:e0:44:dd:
5d:7b Exponent: 65537 (0x10001)
X509v3 extensions:
X509v3 Subject Alternative Name:
IP Address:10.2.0.2, DNS:test.abc.com, email:user@test.abc.com Signature Algorithm: sha1WithRSAEncryption 53:d5:79:31:7b:40:52:aa:ec:a9:35:ed:07:62:32:c4:ce:22:
d3:37:0e:83:0c:4c:fa:61:dd:8c:db:a8:d3:fd:6a:ca:0e:3c:
91:2c:91:ab:92:31:34:b5:87:1e:30:a4:ff:94:9c:d2:71:3c:
6b:1f:4f:be:a7:20:f2:e1:c2:ad:71:8b:c2:79:0f:50:1f:3c:
f9:87:df:1d:ee:3d:38:8c:f3:30:b7:3b:00:9b:72:38:b0:68:
e1:c0:08:f4:02:91:81:a8:fa:51:9e:53:0d:03:b3:6b:0e:e2:
62:80:ef:2a:a0:cb:9b:9b:91:21:7c:df:fe:6a:38:cc:03:36:
9c:fc Pki realm name: - Certificate file name: cmp_ir.cer Certificate peer name: -
● 证书申请成功后，可执行命令display pki certificate ca查看已经导入内存的CA证书的内容。
[DeviceA] display pki certificate ca filename cmp_ca1.cer The x509 object type is certificate:
Certificate:
Data:
Version: 3 (0x2)
Serial Number: 2 (0x2)
Signature Algorithm: sha1WithRSAEncryption Issuer: C=cn, ST=beijing, L=BB, O=BB, OU=BB, CN=BB Validity Not Before: Aug 15 02:38:27 2011 GMT Not After : Aug 13 02:38:27 2016 GMT Subject: C=cn, ST=jiangsu, O=huawei, OU=info, CN=hello Subject Public Key Info:
Public Key Algorithm: rsaEncryption RSA Public-Key: (1024 bit)
Modulus:
00:b7:3e:65:7f:3b:3c:18:b8:87:34:39:76:3c:87:
39:f7:a9:b3:35:9b:e0:e0:5b:c7:4f:3c:bb:fa:dd:
da:93:0b:55:6e:eb:ba:52:c8:86:d1:cf:14:1e:1c:
35:c6:53:68:f3:51:e7:2c:d4:b8:fa:0f:b3:04:ef:
3f:a0:b3:4d:78:c1:26:88:26:15:41:3d:14:7f:67:
3e:2f:35:32:ce:c7:73:73:43:5c:12:d3:0f:a0:ec:
96:ae:55:61:27:32:39:a4:f8:32:a1:68:50:e6:3d:
2b:39:6d:42:e8:09:5d:4f:98:46:6e:fc:80:87:0e:
36:ca:09:7a:ca:2f:dd:ad:d3 Exponent: 65537 (0x10001)
X509v3 extensions:
X509v3 Basic Constraints: critical CA:TRUE

X509v3 Subject Key Identifier:
4F:67:F4:CB:F4:C3:F7:61:2C:BD:FF:1D:D1:29:FD:39:28:9F:3B:8B X509v3 Key Usage:
Certificate Sign, CRL Sign Netscape Cert Type:
SSL CA, S/MIME CA, Object Signing CA Netscape Comment:
xca certificate Signature Algorithm: sha1WithRSAEncryption 75:43:24:eb:db:ee:7d:05:30:88:b8:1b:d5:32:ca:51:49:74:
04:94:fe:d0:31:29:6f:72:c7:4a:86:ac:2a:4c:45:24:9d:3c:
b4:30:b5:d1:43:88:29:f7:b4:88:b8:37:dc:dd:f4:fa:42:34:
1c:e6:a5:bc:bb:0b:37:ef:db:8c:b2:b0:bd:97:7f:15:ae:6c:
71:1b:ff:f1:90:13:74:a4:1f:7c:f7:4e:80:5b:42:aa:6b:22:
2a:cf:04:48:29:20:c0:b2:95:38:11:06:be:76:f0:cb:8d:4a:
c6:1a:50:af:31:81:58:ac:14:fe:89:f2:e0:bb:95:3c:94:d0:
54:96 Pki realm name: - Certificate file name: cmp_ca1.cer Certificate peer name: -配置脚本DeviceA 的配置文件\# sysname DeviceA \# pki entity user01 country cn state jiangsu organization huawei organization-unit info common-name hello fqdn user@test.abc.com ip-address 10.2.0.2 email user@user@test.abc.com \# interface 10GE1/0/1 ip address 10.2.0.2 255.255.255.0 \# interface 10GE1/0/2 ip address 10.1.0.2 255.255.255.0 \# pki import-certificate ca filename cmp_cal.cer pki import-certificate local filename cmp_ir.cer pki cmp session cmp cmp-request ca-name "C=cn,ST=beijing,L=SD,O=BB,OU=BB,CN=BB"
cmp-request authentication-cert cmp_ir.cer cmp-request entity user01 cmp-request server url http://10.3.0.1:8080 cmp-request rsa local-key-pair rsa_cmp regenerate cmp-request message-authentication-code 1234 %@%##!!!!!!!!!"!!!!'!!!!*!!!!# ~ Yt'T`/_H5O<-:ydTz$hk./ U,Huq3[u0w8!!!!!!!!!!!!!!! ~ !!!!h#a6(1U`jWv[fB3ZRI\7 ~ b5jYCD+l0/R)RMFWV,:%@%# certificate auto-update enable certificate update expire-time 80 \# return

#### 10.12.3 举例：通过证书属性过滤实现访问控制

组网需求如图10-16所示，设备作为内部网络的网关，网络A和网络B中的设备通过证书方式与设备进行身份验证，通过证书过滤的设备才可以建立连接，访问网络C资源。

基于证书属性的访问控制策略，符合如下要求的证书才能通过验证：
● 证书颁发者的名称为networkb_ca。
● 证书的主题名为cert_ca。
图 10-16 配置证书过滤实现访问控制组网图说明本举例只列出了证书属性的访问控制策略的相关配置。
配置思路采用如下思路配置证书过滤实现访问控制：
1. 创建证书属性组，并在证书属性组中创建属性规则指定证书颁发者的名称和证书的主题名。
2. 创建证书属性访问控制策略，并允许证书属性组中的属性规则通过。
操作步骤步骤1 配置缺省的证书属性访问控制策略中的动作为Deny，即不允许证书通过验证。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] pki certificate access-control-policy default deny步骤2 创建证书属性组group。
[DeviceA] pki certificate attribute-group group步骤3 创建属性规则，配置证书颁发者的名称为networkb_ca，证书的主题名为cert_ca。
[DeviceA-pki-attribute-group] attribute 1 issuer-name dn equ networkb_ca [DeviceA-pki-attribute-group] attribute 2 subject-name dn equ cert_ca [DeviceA-pki-attribute-group] quit步骤 4 创建证书属性访问控制策略 policy 。
[DeviceA] pki certificate access-control-policy name policy步骤5 配置证书属性控制规则，匹配证书属性组中的属性规则允许通过。

[DeviceA-pki-access-policy] rule 1 permit group [DeviceA-pki-access-policy] quit
----结束检查配置结果完成配置后，只有证书颁发者的名称为networkb_ca和证书的主题名为cert_ca的设备与DeviceA建立隧道。
配置脚本\# sysname DeviceA \# pki certificate access-control-policy default deny \# pki certificate attribute-group group attribute 1 issuer-name dn equ networkb_ca attribute 2 subject-name dn equ cert_ca \# pki certificate access-control-policy name policy rule 1 permit group \# return

#### 10.12.4 举例：配置手工导入其他设备的RSA密钥对和证书

组网需求如图10-17所示，某企业在网络边界处部署了DeviceA作为出口网关，DeviceA已向公网上的CA服务器申请到本地证书。
因为DeviceA设备太旧，用户希望使用DeviceB设备替换DeviceA，但是由于网络的原因，用户无法手动更新证书和RSA密钥对，只能在DeviceB上手工导入DeviceA的RSA密钥对和证书。
图 10-17 配置手工导入其他设备的 RSA 密钥对和证书组网图说明DeviceA设备为其他厂商设备时，相关命令请参见其配置手册。

配置思路采用如下思路配置手工导入其他设备的RSA密钥对和证书：
1. 将DeviceA的RSA密钥对和证书导出到存储卡中。
2. 通过SFTP等方式将DeviceA存储卡中的RSA密钥对和证书文件保存到PC。
3. 通过SFTP等方式将PC中DeviceA的RSA密钥对和证书文件保存到DeviceB存储卡中。
4. 将DeviceB存储卡中的RSA密钥对和证书导入到内存中。
操作步骤步骤1 导出DeviceA的RSA密钥对和证书。
\# 将RSA密钥对rsa_key和其对应的证书cer_test.cer按PEM格式导出到文件test02.pem，加密方式为AES。
<HUAWEI> system-view [HUAWEI] sysname DeviceA [DeviceA] pki export rsa-key-pair rsa_key and-certificate cer_test.cer pem test02.pem aes password YsHsjx_202206 Warning: Exporting the key pair impose security risks, are you sure you want to export it? [y/n]:y Info: Succeeded in exporting the RSA key pair in PEM format.
说明在DeviceA上执行命令pki rsa local-key-pair create创建RSA密钥对时，如果未配置exportable参数，则该RSA密钥对不允许被导出。
\# 检查存储卡中是否存在test02.pem文件。
[DeviceA] quit <DeviceA> dir flash:/pki/public/ Directory of flash:/pki/public/ Idx Attr Size(Byte) Date Time FileName 0 -rw- 3,016 Jun 15 2017 18:48:26 test02.pem 1,179,616 KB total (434,592 KB free)
步骤2 通过SFTP等方式将DeviceA存储卡中的test02.pem文件保存到PC。
步骤3 通过SFTP等方式将PC中test02.pem文件保存到DeviceB存储卡的flash:/pki/public目录中。该目录需和DeviceA的保持一致，否则将导入失败。
步骤 4 在 DeviceB 上导入 DeviceA 的 RSA 密钥对和证书。
导入PEM格式的RSA密钥对文件test02.pem，RSA密钥对在系统中的名称为rsakey，密码为YsHsjx_202206，且标记为可导出。
导入test02.pem后，存储卡中的test02.pem默认删除，如不需删除，请根据设备上的提示信息选择N进行保留。
<HUAWEI> system-view [HUAWEI] sysname DeviceB [DeviceB] pki import rsa-key-pair rsakey pem test02.pem exportable password YsHsjx_202206 Info: Succeeded in importing the RSA key pair in PEM format.
Warning: The file in the flash will be deleted. Please select 'N' if you want to keep it. Please select [Y/N]:y Info: Delete Success.
导入test02.pem后，DeviceB内存中生成RSA密钥对rsakey、本地证书rsakey_local.cer和CA证书rsakey_ca.cer文件。

说明DeviceA导出的test02.pem文件里不包含CA证书时，DeviceB导入test02.pem文件后，内存中不会生成CA证书。如果用户需导入CA证书，则可以按照上面步骤逻辑来执行命令pki export- certificate ca和pki import-certificate ca。
----结束检查配置结果
1. 执行命令display pki rsa local-key-pair查看到已导入内存的RSA密钥对信息。
[DeviceB] display pki rsa local-key-pair name rsakey public Info: It will take a few seconds or more. Please wait a moment.
Total Number: 1 ===================================================== Time of Key pair created: 10:40:22 2021/3/13 Key Name: rsakey Key Modulus: 3072 bits Key Exportable: Yes ===================================================== RSA Public-Key: (3072 bits)
Modulus:
00:9d:e2:3b:3b:d9:19:48:3a:62:59:11:c4:af:08:
03:dd:9c:4a:61:e8:ed:a3:4b:a2:44:7f:a6:ea:10:
12:04:8f:93:f2:ab:dc:09:f9:bc:e5:6b:4c:d3:29:
f6:22:9e:da:83:bf:17:b2:8e:6b:65:6c:17:7e:83:
dc:8e:33:1f:33:2d:96:4f:3d:ed:03:6d:91:45:47:
49:79:8b:89:8a:7b:e5:f8:12:c0:41:45:77:ff:30:
4c:a1:d4:f2:d0:9f:02:84:82:6d:02:10:bd:f1:5a:
64:d0:8d:21:aa:a5:e6:61:ee:bb:55:a1:99:3f:ad:
fb:6c:13:c9:dd:23:c6:ab:02:24:07:e4:76:4b:ef:
3e:fa:56:31:80:b2:75:a2:b5:cc:12:0b:33:0a:e7:
19:ed:6b:36:93:9f:78:e1:37:13:e2:b5:47:6f:d1:
f1:7c:d8:01:49:f6:82:d9:3a:d6:1a:fd:bb:c4:71:
05:fd:a4:ea:73:5b:db:b5:1a:2b:a5:e3:e2:78:b4:
ec:9b:92:36:72:35:4f:7b:cc:05:91:db:14:1f:da:
c5:22:89:f0:64:4a:76:b3:27:69:cf:b6:a6:1d:bd:
ec:4c:24:0d:9e:ff:27:46:94:2e:b0:68:61:c6:ce:
bd:e3:b0:4b:26:66:ee:f1:8a:3f:8c:30:7f:6f:bd:
77:d1 Exponent: 65537 (0x10001)
2. 执行命令display pki certificate local filename查看到已导入内存的本地证书的内容。
[DeviceB] display pki certificate local filename rsakey_local.cer The x509_obj type is Cert:
Certificate:
Data:
Version: 3 (0x2)
Serial Number: 1144733510 (0x443b3f46)
Signature Algorithm: sha1WithRSAEncryption Issuer: C=cn, ST=beijing, L=BB, O=BB, OU=BB, CN=BB Validity Not Before: Jun 12 09:33:10 2012 GMT Not After : Aug 13 02:38:27 2016 GMT Subject: C=CN, ST=jiangsu, O=huawei, OU=info, CN=hello Subject Public Key Info:
Public Key Algorithm: rsaEncryption RSA Public-Key: (3072 bit)
Modulus:
00:d3:12:fe:57:48:c6:a5:10:12:e9:2f:f9:2a:ff:
7b:2a:d8:45:69:11:c4:85:30:c4:9a:4d:0f:ad:58:
e7:56:cd:5c:f0:18:e1:c3:6d:44:c2:c3:5e:64:22:
d1:28:c9:c3:37:3c:34:ed:28:04:7f:62:9e:8b:94:
af:bc:72:de:f6:72:7f:e4:d8:45:31:fd:f9:ac:ce:
5a:b9:c7:1b:23:53:00:28:a6:3b:f5:61:69:5d:ab:
67:cb:bb:e8:96:2f:ce:ab:2c:6b:91:5b:26:91:86:

8f:80:a9:b0:66:c1:16:3d:31:55:a2:d4:b5:5a:af:
85:88:6e:99:f8:f8:53:58:77:26:91:ed:0e:94:ad:
c5:8d:53:67:67:55:08:8d:90:38:e0:5e:96:37:b9:
64:0e:36:e7:cf:9a:d2:77:e4:b0:24:05:a6:eb:03:
6e:ff:f7:ab:be:93:9e:8c:66:7d:31:66:be:6d:c8:
f3:17:9d:86:19:88:21:2d:d9:69:86:5f:b2:55:a4:
db:bc:d7:d0:6b:ac:66:ac:e4:63:9c:66:79:9c:42:
5c:83:b8:9e:4b:6e:67:85:a2:47:19:f1:5c:c0:3c:
c9:a3:47:02:a8:53:69:59:9e:d9:c7:5e:90:83:8d:
ac:cd:21:3c:d5:31:39:49:84:e6:f8:f4:e0:44:dd:
5d:7b Exponent: 65537 (0x10001)
X509v3 extensions:
X509v3 Subject Alternative Name:
IP Address:10.2.0.2, DNS:test.abc.com Signature Algorithm: sha1WithRSAEncryption 53:d5:79:31:7b:40:52:aa:ec:a9:35:ed:07:62:32:c4:ce:22:
d3:37:0e:83:0c:4c:fa:61:dd:8c:db:a8:d3:fd:6a:ca:0e:3c:
91:2c:91:ab:92:31:34:b5:87:1e:30:a4:ff:94:9c:d2:71:3c:
6b:1f:4f:be:a7:20:f2:e1:c2:ad:71:8b:c2:79:0f:50:1f:3c:
f9:87:df:1d:ee:3d:38:8c:f3:30:b7:3b:00:9b:72:38:b0:68:
e1:c0:08:f4:02:91:81:a8:fa:51:9e:53:0d:03:b3:6b:0e:e2:
62:80:ef:2a:a0:cb:9b:9b:91:21:7c:df:fe:6a:38:cc:03:36:
9c:fc Pki realm name: - Certificate file name: rsakey_local.cer Certificate peer name: -
3. 执行命令display pki certificate ca filename查看到已导入内存的CA证书的内容。
[DeviceB] display pki certificate ca filename rsakey_ca.cer The x509 object type is certificate:
Certificate:
Data:
Version: 3 (0x2)
Serial Number: 2 (0x2)
Signature Algorithm: sha1WithRSAEncryption Issuer: C=cn, ST=beijing, L=BB, O=BB, OU=BB, CN=BB Validity Not Before: Aug 15 02:38:27 2011 GMT Not After : Aug 13 02:38:27 2016 GMT Subject: C=CN, ST=jiangsu, O=huawei, OU=info, CN=hello Subject Public Key Info:
Public Key Algorithm: rsaEncryption RSA Public-Key: (1024 bit)
Modulus:
00:b7:3e:65:7f:3b:3c:18:b8:87:34:39:76:3c:87:
39:f7:a9:b3:35:9b:e0:e0:5b:c7:4f:3c:bb:fa:dd:
da:93:0b:55:6e:eb:ba:52:c8:86:d1:cf:14:1e:1c:
35:c6:53:68:f3:51:e7:2c:d4:b8:fa:0f:b3:04:ef:
3f:a0:b3:4d:78:c1:26:88:26:15:41:3d:14:7f:67:
3e:2f:35:32:ce:c7:73:73:43:5c:12:d3:0f:a0:ec:
96:ae:55:61:27:32:39:a4:f8:32:a1:68:50:e6:3d:
2b:39:6d:42:e8:09:5d:4f:98:46:6e:fc:80:87:0e:
36:ca:09:7a:ca:2f:dd:ad:d3 Exponent: 65537 (0x10001)
X509v3 extensions:
X509v3 Basic Constraints: critical CA:TRUE X509v3 Subject Key Identifier:
4F:67:F4:CB:F4:C3:F7:61:2C:BD:FF:1D:D1:29:FD:39:28:9F:3B:8B X509v3 Key Usage:
Certificate Sign, CRL Sign Netscape Cert Type:
SSL CA, S/MIME CA, Object Signing CA Netscape Comment:
xca certificate Signature Algorithm: sha1WithRSAEncryption 75:43:24:eb:db:ee:7d:05:30:88:b8:1b:d5:32:ca:51:49:74:

04:94:fe:d0:31:29:6f:72:c7:4a:86:ac:2a:4c:45:24:9d:3c:
b4:30:b5:d1:43:88:29:f7:b4:88:b8:37:dc:dd:f4:fa:42:34:
1c:e6:a5:bc:bb:0b:37:ef:db:8c:b2:b0:bd:97:7f:15:ae:6c:
71:1b:ff:f1:90:13:74:a4:1f:7c:f7:4e:80:5b:42:aa:6b:22:
2a:cf:04:48:29:20:c0:b2:95:38:11:06:be:76:f0:cb:8d:4a:
c6:1a:50:af:31:81:58:ac:14:fe:89:f2:e0:bb:95:3c:94:d0:
54:96 Pki realm name: - Certificate file name: rsakey_ca.cer Certificate peer name: -

### 10.13 PKI常见配置错误

#### 10.13.1 获取CA证书失败

故障现象通过手工方式获取CA证书，查看设备存储介质中没有下载到CA证书，其失败的原因为通过LDAP方式下载CA证书时配置的不正确。
操作步骤
● 检查LDAP方式下载CA证书的配置是否正确。如果不正确，请修改相应的内容。详情请参见命令pki ldap-server-template template-name attribute attr-value save-name dn dn-value。
----结束

#### 10.13.2 获取本地证书失败

故障现象
● 通过手工方式离线获取本地证书，查看设备存储介质中没有下载到本地证书，其失败的原因如下：
– 指定的PKI实体配置不正确。
– 挑战密码配置的不正确或未配置。
– 通过LDAP方式下载本地证书时配置不正确。
● 通过 CMPv2 协议获取本地证书，查看设备存储介质中没有下载到本地证书，其失败的原因如下：
– 执行获取操作之前PKI域中没有CA证书。
– 指定的PKI实体配置不正确或未配置。
– 信任的CA名称配置不正确或未配置。
– 证书注册服务器的URL配置不正确或未配置。
– 使用的RSA密钥对未配置。
– TCP连接使用的源接口配置不正确。
– 签名证书注册请求消息使用的摘要算法配置的不正确。
– 挑战密码配置的不正确或未配置。
– 消息认证码的参考值和秘密值配置不正确或未配置。

– 用于证明身份的证书配置不正确。
操作步骤
● 通过手工方式获取本地证书
a. 检查配置的PKI实体配置是否正确。
在PKI域下指定的PKI实体，可以执行命令display pki entity查看配置的PKI实
体信息。
如果某些内容配置错误，例如PKI实体所属的国家代码配置错误，请修改相应
的内容。
b. 检查挑战密码配置是否正确。
请先确定CA服务器是否要验证挑战密码，如果是，请配置CA服务器的挑战密
码，两者要一致。详情请参见命令pki enroll-certificate。
c. 检查LDAP方式下载本地证书的配置是否正确。
如果不正确，请修改相应的内容。详情请参见命令 pki ldap-server-
template template-name attribute attr-value save-name dn dn-value。
● 通过CMPv2协议获取本地证书
a. 检查CA证书是否已导入设备的内存中。
可以执行命令display pki certificate查看设备内存中的CA证书。
如果没有请获取CA证书并执行命令pki import-certificate将CA证书导入设
备的内存中。
b. 检查配置的PKI实体配置是否正确。
在PKI域下指定的PKI实体，可以执行命令display pki entity查看配置的PKI实
体信息。
如果某些内容配置错误，例如PKI实体所属的国家代码配置错误，请修改相应
的内容。
c. 检查CMP会话下配置的申请CA证书的相关配置是否正确。
可以在CMP会话下执行命令display this查看。
如下所示，这里例举申请 CA 证书所需的配置。
pki cmp session cmp
cmp-request ca-name "C=cn,ST=beijing,L=SD,O=BB,OU=BB,CN=BB" //配置CA的名称，CA名称中
各个字段的顺序必须要和实际CA证书中的顺序保持一致
//配置CMPv2请求中用于证明身份的证书，用于更新证
cmp-request authentication-cert local.cer
书或为其他设备申请证书等
cmp-request entity user01 //指定使用的PKI实体
cmp-request server url http://10.3.0.1:8080 //配置CMPv2服务器的URL
cmp-request rsa local-key-pair rsa regenerate //指定使用的RSA密钥对
cmp-request message-authentication-code 1234 %^%#ZodFBGH[^BkU2( ~ >[NRBv|#b>se|
@I7"'A,llG_B%^%# //配置消息认证码的参考值和秘密值，与CA服务器一致
如果相关配置不正确，请修改相应的内容。
----结束
