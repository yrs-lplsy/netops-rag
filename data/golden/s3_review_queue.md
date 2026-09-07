# S3 golden set 抽查队列（40 条）与生成台账

- 全集：`s3_full.yaml` 共 200 条；分布：factual×cisco=25，factual×h3c=25，factual×hw24=25，factual×hw25=25，multihop×cisco=8，multihop×h3c=8，multihop×hw24=5，multihop×hw25=9，reject×reject=30，troubleshoot×cisco=4，troubleshoot×h3c=8，troubleshoot×hw24=8，troubleshoot×hw25=14，troubleshoot×hwcase=6

## 分类抽样

### factual（16 条）

- `hw-v600r025c00-eth-switch-01-03#c30#ver` 在华为 V600R025C00 版本文档中，配置Eth-Trunk自协商功能支持哪种模式的Eth-Trunk？
  - 期望：hw-v600r025c00-eth-switch-01-03#c30 filters={V600R025C00}
- `hw-v600r025c00-eth-switch-01-04#c15#ver` 在华为 V600R025C00 版本文档中，当Host1发送ARP广播请求报文给Host2时，DeviceA的接口interface1会给报文添加VID为多少的Tag？
  - 期望：hw-v600r025c00-eth-switch-01-04#c15 filters={V600R025C00}
- `hw-v600r025c00-eth-switch-01-07#c94#ver` 在华为 V600R025C00 版本文档中，配置接口路径开销计算方法为 dot1t 时，参数 cost 的取值范围是多少？
  - 期望：hw-v600r025c00-eth-switch-01-07#c94 filters={V600R025C00}
- `hw-v600r025c00-eth-switch-01-10#c26#ver` 在华为 V600R025C00 版本文档中，当DeviceD上与DeviceE相连的端口故障恢复时，哪个设备的RPL owner端口将被阻塞？
  - 期望：hw-v600r025c00-eth-switch-01-10#c26 filters={V600R025C00}
- `h3c-r1110-l2sw-cmd#h3c-r1110-l2sw-cmd#c103` display mac-address 命令中，参数 dynamic 用来显示什么类型的 MAC 地址表项？
  - 期望：h3c-r1110-l2sw-cmd#c103
- `hw-v600r024c10-security-01-10#hw-v600r024c10-security-01-10#c10` 证书签名过程中，CA使用哪种算法生成证书的摘要信息？
  - 期望：hw-v600r024c10-security-01-10#c10
- `hw-v600r025c00-alarm-01-55#hw-v600r025c00-alarm-01-55#c15` 在处理对端无响应导致的心跳报文未收到的问题时，需要在所有视图下执行什么命令来检查两端设备的端口状态？
  - 期望：hw-v600r025c00-alarm-01-55#c15
- `h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c1001` 如何配置 OSPFv3 进程 1 的 GR 重启间隔时间为 100 秒？
  - 期望：h3c-r1110-iproute-cmd#c1001
- `h3c-r1110-security-cfg#h3c-r1110-security-cfg#c10` 如何配置RADIUS服务器的状态？
  - 期望：h3c-r1110-security-cfg#c10
- `cisco-c9300-17.9-ip-routing-cg#cisco-c9300-17.9-ip-routing-cg#c100` 如何在未运行MBGP的情况下配置MSDP的默认对等体？
  - 期望：cisco-c9300-17.9-ip-routing-cg#c100
- `h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c1` H3C S6520X-EI & S6520X-HI系列以太网交换机的资料版本是什么？
  - 期望：h3c-r1110-iproute-cmd#c1
- `hw-v600r025c00-alarm-01-105#hw-v600r025c00-alarm-01-105#c1000` 哪些设备形态支持"The CA certificate is invalid."的告警？
  - 期望：hw-v600r025c00-alarm-01-105#c1000
- `hw-v600r024c10-ip-route-01-07#hw-v600r024c10-ip-route-01-07#c10` 通过执行什么命令可以修改BGP路由的缺省本地优先级？
  - 期望：hw-v600r024c10-ip-route-01-07#c10
- `hw-v600r025c00-security-01-18#hw-v600r025c00-security-01-18#c15` 如何查看HIPS各检测模块的启用情况？可以在任意视图下执行什么命令？
  - 期望：hw-v600r025c00-security-01-18#c15
- `cisco-c9300-17.9-layer2-cg#cisco-c9300-17.9-layer2-cg#c10` 启用MST时，使用spanning-tree mode mst全局配置命令会自动启用什么协议？
  - 期望：cisco-c9300-17.9-layer2-cg#c109
- `hw-v600r024c10-eth-switch-01-09#hw-v600r024c10-eth-switch-01-09#c15` 在邻居协商机制中，如果一端端口在超时时间内没有收到对端发送的邻居协议报文，端口的邻居状态会被置为什么？
  - 期望：hw-v600r024c10-eth-switch-01-09#c15

### troubleshoot（10 条）

- `hw-v600r025c00-alarm-01-47#hw-v600r025c00-alarm-01-47#c187` 静态PW承载的业务出现恢复，该如何排查或处理？
  - 期望：hw-v600r025c00-alarm-01-47#c187
- `hw-v600r025c00-alarm-01-99#hw-v600r025c00-alarm-01-99#c45` 电源模块的A平面输入过压，该如何排查和处理？
  - 期望：hw-v600r025c00-alarm-01-99#c45
- `hw-v600-case-01-03#hw-v600-case-01-03#c575` 在网络设备中，我观察到建立了一个多跳（Multiple Hops）的BFD会话，且状态为Up。但是，当对DeviceA的Vlanif100接口执行shutdown操作，模拟链路故障后，再次查看DeviceA上的BFD会话状态时，发现会话状态变为Down。这种情况下，该如何排查或处理？
  - 期望：hw-v600-case-01-03#c575
- `hw-v600r024c10-ip-route-01-07#hw-v600r024c10-ip-route-01-07#c57` 在配置BGP时，如果将4字节AS号的显示格式从点分形式切换到整数形式，发现AS-Path正则表达式和扩展团体属性过滤器的匹配结果受到影响，导致路由不能匹配出口或入口策略，该如何重新配置AS-Path正则表达式和扩展团体属性过滤器以避免网络故障？
  - 期望：hw-v600r024c10-ip-route-01-07#c57
- `hw-v600r025c00-alarm-01-16#hw-v600r025c00-alarm-01-16#c22` 网络中出现了丢弃非法DHCP报文的告警，该如何排查或处理？
  - 期望：hw-v600r025c00-alarm-01-16#c22
- `hw-v600r025c00-ip-route-01-03#hw-v600r025c00-ip-route-01-03#c89` 在DeviceA和DeviceB之间配置了BFD会话检测链路故障后，如果发现BFD会话无法正常建立，该如何排查或处理？
  - 期望：hw-v600r025c00-ip-route-01-03#c89
- `hw-v600r025c00-alarm-01-08#hw-v600r025c00-alarm-01-08#c49` BFD会话所检测的链路转发能力恢复或BFD会话恢复后，业务流量恢复正常，这种情况该如何处理？
  - 期望：hw-v600r025c00-alarm-01-08#c49
- `hw-v600r025c00-alarm-01-13#hw-v600r025c00-alarm-01-13#c102` 主备板之间数据无法同步，主备回退点文件出现不一致，该如何排查或处理？
  - 期望：hw-v600r025c00-alarm-01-13#c102
- `h3c-r1110-iproute-cfg#h3c-r1110-iproute-cfg#c1278` 在网络中配置了静态路由后，如果网络拓扑发生变化导致路由失效，该如何排查和处理？
  - 期望：h3c-r1110-iproute-cfg#c1278
- `hw-v600r024c10-eth-switch-01-03#hw-v600r024c10-eth-switch-01-03#c10~2` 在DeviceA与DeviceB之间配置了手工模式Eth-Trunk，三条活动链路都参与数据转发并分担流量。如果其中一条链路故障，导致该链路无法转发数据，链路聚合组自动在剩余的两条活动链路中分担流量，这种情况下该如何排查或处理？
  - 期望：hw-v600r024c10-eth-switch-01-03#c10

### multihop（8 条）

- `hw-v600r024c10-ip-route-01-10#hw-v600r024c10-ip-route-01-10#c37+hw-v600r024c10-ip-route-01-10#c36` 如何使用display rip process-id命令查看RIP路由，并结合timers rip triggered命令调整RIP触发更新定时器以优化网络收敛时间？
  - 期望：hw-v600r024c10-ip-route-01-10#c37, hw-v600r024c10-ip-route-01-10#c36
- `h3c-r1110-iproute-cfg#h3c-r1110-iproute-cfg#c1015+h3c-r1110-iproute-cfg#c1094` 在配置BGP GTSM时，如果指定本地设备到达某个对等体的最大跳数为5，使用命令`display bgp [ instance instance-name ] paths`显示BGP的路由属性信息时，接收到的BGP报文的合法TTL范围是多少？
  - 期望：h3c-r1110-iproute-cfg#c1015, h3c-r1110-iproute-cfg#c1094
- `cisco-c9300-17.9-layer2-cg#cisco-c9300-17.9-layer2-cg#c274+cisco-c9300-17.9-layer2-cg#c42` 在配置Layer 2 EtherChannels时，如果使用LACP模式并指定了16个以太网端口，其中8个端口处于活动状态，另外8个端口处于备用状态，那么这些端口在参与PVST+或Rapid PVST+协议时，如何确保在发生拓扑变化时，活动端口和备用端口之间的切换不会导致网络环路？
  - 期望：cisco-c9300-17.9-layer2-cg#c274, cisco-c9300-17.9-layer2-cg#c42
- `h3c-r1110-security-cfg#h3c-r1110-security-cfg#c1485+h3c-r1110-security-cfg#c190` 如何在配置 Stelnet Suite B 客户端时，确保设备上传到服务器的用户在线时间中包含由 AAA 授权的闲置切断时间，同时正确导入并验证服务器证书文件 ssh-server-ecdsa256.p12？
  - 期望：h3c-r1110-security-cfg#c1485, h3c-r1110-security-cfg#c190
- `cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c1025+cisco-c9300-17.9-security-cg#c1080` 在配置IPv6 FQDN ACL时，如果需要在指定接口上控制访问，为什么不能同时配置源和目的主机地址的动态主机配置，且该接口必须是Layer 3接口？
  - 期望：cisco-c9300-17.9-security-cg#c1025, cisco-c9300-17.9-security-cg#c1080
- `hw-v600r025c00-ip-route-01-09#hw-v600r025c00-ip-route-01-09#c125+hw-v600r025c00-ip-route-01-09#c128` 在配置IS-IS智能收敛功能时，如果接口状态频繁在Up和Down之间切换，导致邻居状态震荡，应该如何设置detecting-interval和resume-interval参数，以确保快速收敛的同时有效抑制邻居震荡？
  - 期望：hw-v600r025c00-ip-route-01-09#c125, hw-v600r025c00-ip-route-01-09#c128
- `hw-v600r025c00-ip-route-01-10#hw-v600r025c00-ip-route-01-10#c30+hw-v600r025c00-ip-route-01-10#c31` 如何使用display rip process-id route命令查看RIP路由，并结合水平分割（Split Horizon）机制解释在广播网、P2P和P2MP网络中防止路由环路的具体原理？
  - 期望：hw-v600r025c00-ip-route-01-10#c30, hw-v600r025c00-ip-route-01-10#c31
- `hw-v600r024c10-ip-route-01-05#hw-v600r024c10-ip-route-01-05#c294+hw-v600r024c10-ip-route-01-05#c80` 在配置OSPF区域路由聚合功能时，如何确保DeviceB的Router ID在自治系统中唯一，且正确配置Vlanif10、Vlanif20、Vlanif30接口的IP地址以实现DeviceA与DeviceB、DeviceB与DeviceC之间的OSPF互连？
  - 期望：hw-v600r024c10-ip-route-01-05#c294, hw-v600r024c10-ip-route-01-05#c80

### reject（6 条）

- `reject-Docker容器端口映射配置-26` 在Docker中，如何配置容器的端口映射，使宿主机的8080端口映射到容器的80端口？
  - 期望：（空，应拒答）
- `reject-Kubernetes节点亲和性调度配置-14` Kubernetes节点亲和性调度中，如何配置pod反亲和性以避免同一应用的多个实例调度到同一个节点上？
  - 期望：（空，应拒答）
- `reject-大模型推理服务的部署与扩缩容-02` 在部署大模型推理服务时，如何根据实际的推理请求量动态调整GPU资源，以确保服务的高效运行和成本优化？具体来说，使用Kubernetes进行扩缩容时，应该设置哪些关键参数，才能在保证模型性能的同时，避免资源浪费？
  - 期望：（空，应拒答）
- `reject-Ansible playbook批量配置下发-17` Ansible playbook批量配置下发时，如何确保所有网络设备配置同步完成后再进行下一步操作？
  - 期望：（空，应拒答）
- `reject-网络配置基线核查工具选型-22` 在进行网络配置基线核查时，如何选择合适的工具来确保与现有网络设备的兼容性？
  - 期望：（空，应拒答）
- `reject-Kubernetes Helm应用发布回滚-15` 在使用Helm发布Kubernetes应用时，如何通过命令行快速回滚到上一个稳定版本？
  - 期望：（空，应拒答）

## reject 主题缺席核验（全语料 processed_pdf 238 文档 grep 实测）

- 大模型: `大模型`×0, `LLM`×0, `神经网络`×0, `ChatGPT`×0 → 全部 0，确认缺席
- Kubernetes容器网络: `Kubernetes`×0, `k8s`×0, `容器编排`×0 → 全部 0，确认缺席
- 自动化运维工具链: `Ansible`×0, `Zabbix`×0, `Prometheus`×0, `自动化运维`×0 → 全部 0，确认缺席
- Docker容器技术: `Docker`×0, `docker`×0 → 全部 0，确认缺席

## 淘汰台账（QC 全量）

- length: 27 条
- duplicate: 10 条
- non-CJK: 2 条
- referent: 2 条
- grounding(cjk 0.00): 2 条

- [duplicate] `hw-v600r024c10-eth-switch-01-06#hw-v600r024c10-eth-switch-01-06#c10` 执行什么命令会清除已经保存的配置文件并导致vlan.dat文件被自动删除？
- [duplicate] `hw-v600r024c10-security-01-24#hw-v600r024c10-security-01-24#c3` 数字签名机制在设置下次启动大包、设置下次启动补丁、补丁加载等场景中如何保证软件包的合法性和完整性？
- [duplicate] `hw-v600r024c10-security-01-18#hw-v600r024c10-security-01-18#c15` 如何查看HIPS各检测模块的启用情况？
- [non-CJK] `hw-v600r024c10-security-01-16#hw-v600r024c10-security-01-16#c9` 如何使用命令`system-view trustem start dynamic-integrity-measurement right-now`立即启动DIM
- [referent] `hw-v600r024c10-ip-route-01-01#hw-v600r024c10-ip-route-01-01#c1` 在本文档中，符号约定部分提到的标志代表什么含义？
- [referent] `hw-v600r024c10-eth-switch-01-01#hw-v600r024c10-eth-switch-01-01#c1` 在本文档中，符号约定部分提到的标志代表什么含义？
- [duplicate] `cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c1` Cisco的TCP头部压缩实现是基于哪家大学开发的程序？
- [duplicate] `cisco-c9300-17.9-layer2-cg#cisco-c9300-17.9-layer2-cg#c1` Cisco的TCP头部压缩实现是基于哪家大学开发的程序？
- [duplicate] `cisco-c9300-17.9-vlan-cg#cisco-c9300-17.9-vlan-cg#c1` Cisco的TCP头部压缩实现是基于哪家大学开发的程序？
- [grounding(cjk 0.00)] `cisco-c9300-17.9-layer2-cg#cisco-c9300-17.9-layer2-cg#c101` 这些功能是在哪个版本之后的所有版本中都可用的，除非另有说明？
- [grounding(cjk 0.00)] `cisco-c9300-17.9-vlan-cg#cisco-c9300-17.9-vlan-cg#c104` 这个模块中解释的功能特性是在哪个命令或参数名之后的所有版本中都可用，除非另有说明？
- [duplicate] `cisco-c9300-17.9-vlan-cg#cisco-c9300-17.9-vlan-cg#c106` 如何使用Cisco Feature Navigator查找关于平台和软件镜像支持的信息？ 若要访问Cisco Feature Navigator，应前往哪个网址
- [non-CJK] `cisco-c9300-17.9-ip-routing-cg#cisco-c9300-17.9-ip-routing-cg#c1004` 如何使用命令`match ip-address {acl-number [acl-number | acl-name ]| acl-name [acl-name
- [duplicate] `cisco-c9300-17.9-ip-routing-cg#cisco-c9300-17.9-ip-routing-cg#c1007` 使用set ipv6 global next hop命令可以指示什么？
- [length] `h3c-r1110-l2sw-cmd#h3c-r1110-l2sw-cmd#c1` H3C S6520X-EI & S6520X-HI系列以太网交换机的命令参考手册中提到的商标H3C、H3CS、H3CIE、H3CNE、Aolynk、H Care
- [duplicate] `h3c-r1110-l2sw-cfg#h3c-r1110-l2sw-cfg#c1` H3C S6520X-EI & S6520X-HI系列以太网交换机的资料版本是什么？
- [length] `h3c-r1110-security-cmd#h3c-r1110-security-cmd#c1` H3C S6520X-EI & S6520X-HI系列以太网交换机的安全命令参考手册中提到的商标H3C、H3CS、H3CIE、H3CNE、Aolynk、H Ca
- [duplicate] `h3c-r1110-iproute-cfg#h3c-r1110-iproute-cfg#c1` H3C S6520X-EI & S6520X-HI系列以太网交换机的资料版本是什么？
- [length] `hw-v600r025c00-alarm-01-52#hw-v600r025c00-alarm-01-52#c45` 在网络设备中配置LDP会话时，如果出现链路参数配置不一致的情况，导致多链路不能按照预期创建，该如何排查或处理？如果告警中的ConfigType是Keepaliv
- [length] `hw-v600r024c10-ip-route-01-05#hw-v600r024c10-ip-route-01-05#c200` 在网络中，当DeviceB发生故障并恢复后，从DeviceA到10.3.1.0/30的流量在回切到DeviceB时出现了流量丢失的现象。这是由于IGP收敛速度比
- [length] `hw-v600r024c10-ip-route-01-03#hw-v600r024c10-ip-route-01-03#c90` 在DeviceA、DeviceB和DeviceC组成的OSPF网络中，DeviceB和DeviceC都配置了到用户的静态路由，并通过OSPF路由协议引入静态路由
- [length] `hw-v600r024c10-eth-switch-01-09#hw-v600r024c10-eth-switch-01-09#c17` 在网络中，当Device1和Device5上的P1端口角色相同，且Device1的P1端口MAC地址大于Device5的P1端口MAC地址时，Device1的P
- [length] `h3c-r1110-iproute-cfg#h3c-r1110-iproute-cfg#c217` Switch A 和 Switch C 通过二层交换机互连，它们的接口 Vlan-interface100 都运行 RIP 进程 1。Switch A 的接口 
- [length] `h3c-r1110-l2sw-cfg#h3c-r1110-l2sw-cfg#c240` Device A 通过二层以太网接口 Ten-GigabitEthernet1/0/1～Ten-GigabitEthernet1/0/3 分别与 Device 
- [length] `h3c-r1110-iproute-cfg#h3c-r1110-iproute-cfg#c856` 开启 BGP 模块的告警功能后，当 BGP 的邻居状态变化时，设备会产生 RFC 4273 中规定的告警信息，该信息包含邻居地址、最近一次出现错误的错误码和错误
- [length] `h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c82` 在网络设备上，如果未开启IPv4路由快速切换功能，当某个物理接口作为大量路由（包括等价路由和主备路由的主路由）的下一跳出接口时，如果该接口所在的链路发生故障，设
- [length] `hw-v600-case-01-03#hw-v600-case-01-03#c352` 在组网需求中，PC1和PC2通过4台Device相连，数据从PC1到PC2有两条路径可以到达，分别是PC1-DeviceA-DeviceB-DeviceC-PC
- [length] `hw-v600-case-01-03#hw-v600-case-01-03#c123` 在网络中，用户的两个网管NMS1和NMS2与设备通过公网相连。根据业务需求，NMS2可以管理设备上的所有节点，而NMS1不再管理该设备。为了确保告警信息的准确性
- [length] `hw-v600r025c00-eth-switch-01-03#hw-v600r025c00-eth-switch-01-03#c54+hw-v600r025c00-eth-switch-01-03#c64` 在配置Eth-Trunk接口时，如果已经通过命令`trunkport interface-type interface-number`将一个物理接口加入到Eth
- [length] `hw-v600r024c10-ip-route-01-06#hw-v600r024c10-ip-route-01-06#c106+hw-v600r024c10-ip-route-01-06#c130` 在配置OSPFv3的LSA更新时间间隔时，使用了命令`lsa-originate-interval intelligent-timer max-interval
- [length] `h3c-r1110-security-cfg#h3c-r1110-security-cfg#c1274+h3c-r1110-security-cfg#c1316` 在配置 IKEv2 安全提议时，如果发现通过 `display ike sa` 命令查看的 IKE SA 状态为 Unknown，并且在 IKE 事件调试信息中
- [length] `reject-Kubernetes Ingress流量暴露配置-10` 我在配置Kubernetes Ingress时，遇到了一个问题。我的服务需要通过Ingress暴露到外部，但是目前外部访问时总是返回404 Not Found错
- [length] `reject-Kubernetes NetworkPolicy网络策略下发-11` 我在配置Kubernetes的NetworkPolicy时遇到了一个问题，NetworkPolicy规则已经定义并应用到了Pod上，但是Pod之间的隔离策略似乎
- [length] `reject-Kubernetes节点亲和性调度配置-14` 在Kubernetes中，如何配置节点亲和性（Node Affinity）以确保特定的工作负载只调度到具有特定标签的节点上？具体来说，我想了解如何使用requi
- [length] `reject-Kubernetes Helm应用发布回滚-15` 我在使用Helm发布Kubernetes应用时，遇到了一个问题。我之前用Helm安装了一个应用，版本是1.2.3，后来升级到了1.2.4，但是新版本有一些问题，
- [length] `reject-Kubernetes跨集群服务发现-16` 在Kubernetes跨集群服务发现中，如何配置Service Entry以实现多集群间的相互访问？具体来说，如果我有两个Kubernetes集群，Cluste
- [length] `reject-Ansible playbook批量配置下发-17` 我在使用Ansible playbook批量配置下发时，遇到了一个问题。我的playbook中定义了多个任务，每个任务都需要在不同的网络设备上执行特定的配置命令
- [length] `reject-Grafana可视化监控大盘搭建-20` 我在搭建Grafana可视化监控大盘时，遇到了一个问题。我使用Prometheus作为数据源，已经成功配置了Prometheus抓取目标，但是在Grafana中
- [length] `reject-网络配置基线核查工具选型-22` 在进行网络配置基线核查时，我们通常会用到一些专业的工具，比如Nessus、Nmap、Cisco Config Auditor等。这些工具各有特点，但在实际应用中
- [length] `reject-Docker容器端口映射配置-26` 我在配置Docker容器的端口映射时，发现有时候宿主机的端口并没有正确映射到容器的端口上，导致外部无法访问容器内的服务。我已经检查了Docker的网络模式，使用
- [length] `reject-docker0网桥网段修改-27` 我在使用Docker时，发现默认的docker0网桥网段是172.17.0.0/16，但是我的内部网络已经使用了这个网段，导致了一些冲突。我想要修改docker
- [length] `reject-Docker日志驱动与轮转-29` 我在配置Docker容器的日志驱动时，发现有多种日志驱动可以选择，比如json-file、syslog、journald等。我想了解一下，如果我选择使用json
- [length] `reject-Docker Swarm集群组网-30` 我在配置Docker Swarm集群时，遇到了一个问题。我的集群中有多个管理节点和工作节点，分布在不同的物理服务器上。我已经通过overlay网络实现了节点间的

## TOC修复台账（2026-09-06）

缺陷：11 条期望 chunk 为 cisco 整本书 PDF 的目录页（book 级 Contents 页 / 章首 mini-TOC），无法答题——生成管线把 TOC chunk 采为出题源，grounding 审计因 TOC 文本提及特性名而放行。修复：
1. `build_golden_s3.py` 新增 `is_toc_chunk` 判别（breadcrumb 含 Contents，或点线目录行主导），采样池构造与 QC 双重拦截；
2. 以下 qid 保持不变（评测历史可比），题目/期望 chunk 自真实内容 chunk 重生成（同 qtype、同 cisco 桶、原题均无版本 filter 语义、与全集查重不重复）：

- `cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c10`（factual）期望 c10 → c1007
  - 旧题：如何设置或更改静态启用密码（Setting or Changing a Static Enable Password）？
  - 新题：在配置访问控制列表时，如何使用`igmp-type`参数匹配特定的IGMP消息类型？
- `cisco-c9300-17.9-layer2-cg#cisco-c9300-17.9-layer2-cg#c10`（factual）期望 c10 → c109
  - 旧题：如何配置MSTP中的Hello Time参数？
  - 新题：启用MST时，使用spanning-tree mode mst全局配置命令会自动启用什么协议？
- `cisco-c9300-17.9-vlan-cg#cisco-c9300-17.9-vlan-cg#c10`（factual）期望 c10 → c115
  - 旧题：如何配置私有VLAN端口？
  - 新题：当你在配置了语音VLAN的接口上启用端口安全时，必须将该端口上的最大允许安全地址设置为多少？
- `cisco-c9300-17.9-layer2-cg#cisco-c9300-17.9-layer2-cg#c104`（factual）期望 c104 → c113
  - 旧题：如何配置MSTP及其参数？
  - 新题：MSTP中，哪个实例是唯一发送和接收BPDUs的实例？
- `cisco-c9300-17.9-vlan-cg#cisco-c9300-17.9-vlan-cg#c107`（factual）期望 c107 → c117
  - 旧题：如何配置Voice VLANs？
  - 新题：如何配置Cisco IP Phone通过指定的语音VLAN发送带有Layer 2 CoS值的语音流量？
- `cisco-c9300-17.9-vlan-cg#cisco-c9300-17.9-vlan-cg#c11`（factual）期望 c11 → c114
  - 旧题：如何配置Layer 2接口作为Private VLAN Promiscuous端口？
  - 新题：使用show vlan命令可以查看哪些信息？
- `cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c19`（troubleshoot）期望 c19 → c244
  - 旧题：在网络设备中配置了RADIUS服务器负载均衡后，发现RADIUS服务器状态检测失败，该如何排查或处理？
  - 新题：在网络设备上配置了RADIUS授权后，如果网络访问服务器在联系RADIUS服务器时遇到错误，导致用户登录时无法启动EXEC shell，该如何排查或处理？
- `cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c14`（troubleshoot）期望 c14 → c2148
  - 旧题：在网络设备上配置了AAA Accounting后，发现设备在主备切换时仍然生成了系统会计记录，这导致了不必要的日志条目和存储空间占用。应该如何配置以抑制主备切换时生成系统会计记录？
  - 新题：设备在4月22日23:11:14.203时出现了证书过期的告警，CRYPTO_PKI_AAA协议检测到cert-lifetime-end已过期，导致授权失败。这种情况下，该如何排查或处理？
- `cisco-c9300-17.9-layer2-cg#cisco-c9300-17.9-layer2-cg#c19`（troubleshoot）期望 c19 → c345
  - 旧题：在网络设备上配置了FlexLink+的VLAN负载均衡后，发现FlexLink+拓扑变更消息的传播配置不正确，该如何排查或处理？
  - 新题：在网络中，Best Master Clock Algorithm (BMCA) 基于 IEEE 1588-2008 协议运行，用于确定子域中的最佳主时钟。如果网络中出现两个主时钟或没有主时钟的告警，该如何排查或处理？
- `cisco-c9300-17.9-layer2-cg#cisco-c9300-17.9-layer2-cg#c13+cisco-c9300-17.9-layer2-cg#c103`（multihop）期望 c13+c103 → c174+c184
  - 旧题：如何在EtherChannel接口上配置Precision Time Protocol (PTP)以实现精确的时间同步，并且在配置过程中需要关注哪些限制和局限性？
  - 新题：如何在Cisco设备上配置BPDU的跳数限制，并确保该配置符合Cisco Feature Navigator中关于平台和软件镜像的支持信息？
- `cisco-c9300-17.9-ip-routing-cg#cisco-c9300-17.9-ip-routing-cg#c191+cisco-c9300-17.9-ip-routing-cg#c352`（multihop）期望 c191+c352 → c1054+c1122
  - 旧题：在配置OSPF时，使用了哪些命令来确保配置的正确性和持久性，并且这些命令在哪个步骤中被提及？同时，配置OSPF的基本参数示例可以在手册的哪一页找到？
  - 新题：如何在Cisco IOS中配置VRF-aware服务以实现对特定VRF的主机进行ping操作，并查看该VRF的ARP条目？
