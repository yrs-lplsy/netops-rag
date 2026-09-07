# S1700, S5700, S6700 V600R024C10 配置指南-安全 01-21 安全风险查询配置

## 21 安全风险查询配置

### 21.1 查询安全风险

21.2 查询安全配置
21.1 查询安全风险
背景信息
由于协议自身的安全性能不同，用户配置时使用的某些协议可能存在安全风险。通过
display security risk命令可查看系统中存在的安全风险，并根据给出的修复建议解除
风险。例如，用户配置了SNMPv1功能，该功能存在安全风险，系统会提示并建议使
用SNMPv3协议。
操作步骤
步骤1 查看当前系统中存在的安全风险信息及修复建议。
display security risk [ [ feature feature-name ] | [ level level-para ] | [ type type-para ] ] *
----结束
任务示例
执行命令 display security risk ，查看系统中存在的安全风险信息。
<HUAWEI> display security risk
Risk level : high
Feature name : SNMP
Risk Type : insecure-protocol
Risk information : SNMP V1/V2c is enabled.
Repair action : Disable SNMP V1/V2c and enable SNMP V3 only.
Risk Level : medium
Feature Name : FTPS
Risk Type : insecure-protocol
Risk Information : FTP is not a secure protocol.
Repair Action : It is recommended to use SFTP

### 21.2 查询安全配置

背景信息由于协议自身的安全性能不同，用户配置时使用的某些协议可能存在安全风险，用户可以通过display security configuration查看系统中存在的安全配置。
操作步骤步骤1 查看当前系统中存在的安全配置信息。
display security configuration [ feature feature-name ]
----结束任务示例执行命令display security configuration，查看系统中存在的安全配置信息，示例中只取了部分回显字段。
<HUAWEI> display security configuration Feature Name : FTPS Security Item : ftp security configuration Item content : Ftp server is disabled.Ftp Ipv6 server is disabled.IP block feature is disabled.The FTP server does not bind all interface.
Feature Name : TELNET Security Item : telnet security configuration Item content : The Telnet server function is used.The TELNET server bind all interface.
Feature Name : VTY Security Item : Protocol used by VTY Item content : SSH
