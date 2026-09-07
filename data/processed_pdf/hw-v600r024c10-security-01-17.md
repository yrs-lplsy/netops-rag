# S1700, S5700, S6700 V600R024C10 配置指南-安全 01-17 远程证明配置

## 17 远程证明配置

### 17.1 远程证明简介

17.2 远程证明原理描述
17.3 远程证明配置注意事项
17.4 远程证明缺省配置
17.5 配置远程证明
17.1 远程证明简介
定义
可信计算技术是一种可信度量技术，它以硬件可信模块HTM（Hardware Trust
Module）为信任根，从设备上电开始，到BIOS启动、GRUB及操作系统内核加载，在
整个启动过程中对启动部件进行逐级度量，并将度量结果保存在HTM芯片的PCR
（Platform Configure Register）寄存器中，并记录存储度量日志SML（Storage
Measurement Log）。
远程证明RA（Remote Attestation）是可信计算技术的关键技术之一。远程证明根据
设备在启动阶段获取到的PCR值与SML计算出设备当前的真实状态，然后与基线文件中
的参考值比较，从而判断设备的可信性状态。
目的
通信设备或其系统软件可能被攻击者更换，一旦被更换的设备接入网络就可能破坏整
个网络的安全。因此，为了使网络成为一个可信环境，在每个设备接入网络之前，都
要对设备的身份进行验证，以确保接入网络的设备是可信的。远程证明在设备的外
部，部署独立的验证程序，为客户提供了一种远程审计设备可信状态的手段。被远程
证明审计为不可信的设备，不允许接入网络，从而提高网络的安全性。

### 17.2 远程证明原理描述

基本概念远程证明系统由基线文件、RA Server、RA Client及证书颁发机构CA（Certificate Authority）组成。管理员对整个远程证明系统进行管理，包括下载基线文件，申请并上传CA证书等，如图1所示。
图 17-1 远程证明体系架构
● 基线文件：提供给RA Server，包含了度量对象的参考值，作为远程证明挑战的参考基线，用于校验从RA Client获得的SML，从而验证RA Client的可信状态。基线文件受数字签名保护并上传到华为技术支持网站。基线文件名称：product- name_version_RABASE.tar.gz。
SML是由RA Client产生，其记录了度量对象的真实哈希值和度量顺序。
● RA Server：远程证明服务器，提供远程证明用户界面，供用户Web登录。RA Server 是远程证明的核心部件，并向 RA Client 发起挑战请求，收集 RA Client 的PCR值和SML，根据基线文件验证RA Client的可信状态。
● RA Client：远程证明客户端，待验证可信状态的网络设备。RA Client是带有HTM芯片并支持可信启动功能的设备，负责响应RA Server的挑战请求，将设备上的PCR值和SML反馈给RA Server。
● CA：证书颁发机构，负责创建和分配证书，是用户信任的权威机构。CA用来给RA Client颁发AK（Attestation Key）证书，用于验证RA Client的身份的合法性，防止RA Client被仿冒。
RA Client的AK证书，包含IAK和LAK两种类型：
● IAK（Initial Attestation Key）：设备出厂前已经在HTM芯片内设置的证明密钥，用于对HTM产生的数据（如PCR值等）进行签名。设备在出厂时自带了IAK证书，不需要再进行CA证书申请。

● LAK（Local Attestation Key）：设备交付给用户后，由用户本地创建的证明密
钥，用于对HTM产生的数据（如PCR值等）进行签名。用户可以通过PKI向CA申请
LAK证书。
工作原理
在可信启动阶段，设备的BIOS、BootLoader及OS等二进制程序在启动过程中会被度
量，所谓度量就是对度量对象（比如软件包、软件包内程序文件等）的单向Hash计
算。度量结果被保存在HTM芯片的PCR寄存器中（即PCR值），度量的顺序也会被记
录在SML中。只要度量的顺序或者被度量的对象内容发生变化，度量结果也会变化。
远程证明就是根据设备启动阶段获取的PCR值与SML计算出设备当前的真实状态，然后
与基线文件里的参考值比较，从而判断设备是否可信。
RA Client在可信启动阶段，计算出各启动部件的哈希值并保存到PCR寄存器中。RA
Server作为挑战方，定期向RA Client发起挑战，请求RA Client将可信启动阶段保存的
PCR值和SML发送给RA Server。RA Server上预先加载了从华为技术支持网站上下载的
基线文件，这些基线文件里有各个度量对象的参考值。RA Server收到RA Client发来的
PCR值和SML后，使用PCR值验证SML的合法性，验证通过后，将SML中度量对象的真
实哈希值与基线文件里的参考值进行比较，根据比较结果判断设备的可信状态。如果
SML 中所有度量对象的真实哈希值在基线文件里都能匹配，则说明设备处于可信状
态，否则说明设备处于不可信状态。
验证过程
RA Client的AK证书，包含IAK和LAK两种类型，如果用户使用LAK证书，需要先配置
RA Client获取LAK证书，具体配置请参见17.5 配置远程证明。
管理员需要先完成以下几项任务后，才能保证RA Server和RA Client之间的远程证明功
能顺利进行：
1. 管理员到华为技术支持网站上下载基线文件、华为根证书、华为二级CA证书。如
果RA Client使用LAK证书，还需要获取颁发LAK证书的CA证书链。
2. 管理员通过Web方式登录RA Server，把步骤1中准备的文件上传到RA Server上。
3. 管理员在RA Server上添加RA Client的设备信息，包含IP地址、端口等。
4. 管理员检查RA Client和RA Server之间网络连接是否正常，保证RA Client上电
后，可以被RA Server纳管。RA Client和RA Server之间通过NETCONF进行通信。
当RA Client和RA Server之间网络连通后，RA Server就可以通过远程证明功能验证RA
Client的可信状态。下面介绍远程证明详细的验证过程，如图2所示。

图 17-2 远程证明验证过程
1. RA Server向RA Client收集设备信息，包含产品信息、HTM厂商和版本信息等，用于纳管RA Client设备，验证其可信状态。
2. RA Client将产品名称、产品版本、设备序列号、HTM规范版本、HTM厂商和HTM状态等设备信息返回给RA Server。
3. RA Server向RA Client发起挑战请求，收集该RA Client上指定的PCR值和AK证书。
4. RA Client收到RA Server发送的挑战请求后，和HTM模块交互，获取对应的PCR值和AK证书。
RA Client根据指定的AK证书类型给RA Server返回不同的证书内容，其中：
– 当RA Server指定RA Client的AK证书类型为IAK时，RA Client给RA Server返回IAK证书。
– 当RA Server指定RA Client的AK证书类型为LAK时，RA Client给RA Server返回LAK证书、IAK证书。
5. RA Client给RA Server返回AK证书、PCR值。RA Server进行AK证书和PCR值验证。
a. 用 RA Server 配置的信任证书验证 AK 证书是否可信，如果验证通过，则进行下一步，否则将RA Client的状态置为不可信。
b. 用AK证书中的公钥验证PCR值是否可信，如果验证通过，进行下一步，否则将RA Client的状态置为不可信。
6. RA Server请求获取RA Client设备记录的SML。
7. RA Client返回设备记录的SML，RA Server根据收到的SML验证RA Client是否可信。RA Server使用步骤5中的PCR值验证SML的合法性，验证通过后，将SML中度量对象的真实哈希值与基线文件里的参考值进行比较，根据比较结果判断RA Client的可信状态。如果SML中所有度量对象的真实哈希值在基线文件里都能匹配，则将 RA Client 的状态置为可信，否则将 RA Client 的状态置为不可信。

### 17.3 远程证明配置注意事项

依赖License远程证明无需License许可即可使用。
硬件依赖表 17-1 支持本特性的硬件

| 系列 | 支持产品 |
|---|---|
| S6730-H-V2 | S6730-H48Y6C-TV2, S6730-H48X6C-TV2 |
| S5732-H-V2 | S5732-H48UM4Y2CZ-TV2, S5732-H24S4X6QZ- TV2 |

特性限制表 17-2 本特性的使用限制

| 特性 | 特性限制 |
|---|---|
| 证书管理 | LAK是用户为HTM器件赋予的身份证明，设备出厂时默认使用华为为HTM器件赋予的身份证明IAK。启用LAK，必须在设备上配置颁发证书的服务器地址，为LAK颁发数字证书。 |
| 证书管理 | 远程证明第一阶段是进行证书校验，发起远程证明的RA Server 需要支持ECC算法的证书校验。 |
| 远程证明业务 | 硬件上具备HTM模块的设备才能使用远程证明功能。 |

### 17.4 远程证明缺省配置

远程证明的缺省配置如表1所示。
表 17-3 远程证明缺省配置

| 参数 | 缺省值 |
|---|---|
| 远程证明使能功能 | 未使能 |

### 17.5 配置远程证明

背景信息远程证明系统由RA Server和RA Client共同组成，管理员需要在RA Server和RA Client两端同时完成配置后，才能实现远程证明功能。本章节是RA Client端的配置，RA Server端的配置请查阅相关网管设备的产品文档。
华为公司提供了两套华为根证书和华为二级CA证书用于颁发IAK证书，两套华为根证书和华为二级CA证书分别为：
● 华为根证书：Huawei Equipment CA，华为二级CA证书：Huawei Enterprise Network Product CA
● 华为根证书：Huawei RSA Equipment Root CA 2，华为二级CA证书：Huawei DataCom RSA Equipment CA 2建议在RA Sever端加载这两套华为根证书和华为二级CA证书。华为根证书和华为二级CA 证书下载链接： https://support.huawei.com/additionalres/pki 。
用户可通过如下步骤查看RA Client当前使用的IAK证书，从而获取其配套的华为根证书和华为二级CA证书。
1. 在诊断视图下执行命令display remote-attestation iak certificate slot slotid，查看IAK证书信息，复制显示信息中“-----BEGIN CERTIFICATE-----”至“----- END CERTIFICATE-----”的内容，包含“-----BEGIN CERTIFICATE-----”和“-----END CERTIFICATE-----”，并保存到用户PC，且格式为.pem。
2. 在用户PC安装OpenSSL。
3. 在PC的命令行界面执行openssl x509 -in filename -text -noout，查看Issuer字段中的CN内容。filename：表示证书路径含证书名。
4. 根据查询到的CN内容，从https://support.huawei.com/additionalres/pki上下载华为二级CA证书，根据华为二级CA证书，再下载华为根证书。
前置条件在配置远程证明功能之前，需要完成以下任务：
● 配置设备与RA Server正常通信，并在RA Server侧完成远程证明功能的设置。
● 获取基线文件、华为根证书、华为二级 CA 证书。如果 RA Client 使用 LAK 证书，还需要获取颁发LAK证书的CA证书链。将获取的文件上传至RA Server。
● 配置设备的NETCONF功能，使RA Server与设备可以进行NETCONF会话。
操作步骤步骤1 进入系统视图。
system-view步骤2 进入可信管理视图，配置远程证明功能。
trustem缺省情况下，没有创建可信管理视图。进入可信管理视图后，设备会自动使能远程证明功能。

步骤3 （可选）退出至用户视图。
return步骤4 （可选）设置HTM模块的密码。
set htm password { slot slot-id | all }缺省情况下，HTM使用的是硬件出厂时随机生成的密码。设备会对设置的密码进行加密保护，存储到安全位置，提高远程证明功能的安全性。
步骤5 （可选）为HTM模块申请LAK证书。
1. 创建PKI实体并进入PKI实体视图，或者直接进入PKI实体视图。
system-view pki entity entity-name缺省情况下，系统未配置PKI实体。
2. 配置PKI实体的通用名称。
common-name common-name缺省情况下，系统未配置PKI实体的通用名称。
3. 退出PKI实体视图quit
4. 创建PKI CMP会话并进入PKI CMP会话视图，或者直接进入PKI CMP会话视图。
pki cmp session session-name缺省情况下，系统未创建PKI CMP会话。
5. 配置设备使用CMPv2方式申请证书时使用的PKI实体名称。
cmp-request entity entity-name entity-name必须为步骤步骤5.1中的PKI实体名称。
6. 为PKI CMP会话配置CA的名称。
cmp-request ca-name ca-name配置的CA名称中各个字段的顺序必须要和实际CA证书中的顺序保持一致，否则CMPv2服务器会认为是错误的。
7. 配置CMPv2服务器的URL。
cmp-request server url [ esc ] url-addr
8. 配置使用CMPv2协议进行首次证书申请（IR）的认证方式为签名方式。
cmp-request origin-authentication-method signature缺省情况下，使用CMPv2协议进行首次证书申请（IR）的认证方式为消息认证码方式。在远程证明场景下，必须使用签名方式进行CMPv2协议进行首次证书申请（IR）的认证方式。
9. 退出PKI CMP会话视图。
quit
10. 获取颁发LAK证书的CA证书链、IAK证书的华为二级CA证书，通过SFTP方式上传至设备的flash:/pki/public目录下。
11. 导入LAK证书的CA证书链、IAK证书的华为二级CA证书。
pki import-certificate ca { der | pem } filename file-name说明建议导入两套华为根证书和华为二级CA证书，不能重复导入相同的CA证书。
当前CA服务器不进行IAK证书校验时，可以不导入华为二级CA证书。

12. 配置远程证明绑定PKI的CMP会话。
trustem
remote-attestation pki bind cmp-session session-name
缺省情况下，没有配置远程证明绑定PKI的CMP会话。
session-name必须为步骤步骤5.4中的CMP会话名称。
证书申请成功后，设备默认在证书有效期超过50%时会自动向CA服务器申请更新
证书。
步骤6 （可选）为HTM模块手动更新LAK证书。
remote-attestation pki update-request { all | slot slotID }
在配置远程证明功能的场景下，如果PKI证书失效，例如证书信息泄露导致证书被撤
销，那么需要更新PKI证书。执行该命令后，设备会立即向CA服务器申请更新证书。
----结束
检查配置结果
执行命令 display htm status { slot slot-id | all } ，查询 HTM 芯片的状态。
