#!/bin/sh
# netops FRR 节点启动脚本
# 1) 依据环境变量 NETOPS_VLANS（格式 "父接口:VLANID ..."，如 "eth2:100"）
#    在 FRR 启动前创建 dot1q 子接口（幂等，已存在则跳过）。
#    注意：clab 在容器启动后才挂数据面链路，父接口需等待出现（最多 ~30s）。
# 2) 拉起 sshd（后台，root/root）
# 3) 进入 FRR 官方启动流程（watchfrr 会 apply /etc/frr/frr.conf）
for pair in $NETOPS_VLANS; do
  parent="${pair%%:*}"
  vid="${pair##*:}"
  [ "$parent" = "$pair" ] && continue
  i=0
  while [ $i -lt 60 ] && ! ip link show "$parent" >/dev/null 2>&1; do
    sleep 0.5
    i=$((i + 1))
  done
  ip link add link "$parent" name "$parent.$vid" type vlan id "$vid" 2>/dev/null || true
  ip link set "$parent.$vid" up
done
/usr/sbin/sshd
exec /usr/lib/frr/docker-start
