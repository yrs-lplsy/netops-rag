# FRR + sshd 仿真节点镜像（netops lab 专用）
#
# 背景：本机 docker.io / ghcr.io 直连不可用（见 task-11 报告）。
#   - ghcr.io/srl-labs/linuxrouter 各镜像站均无法拉取（daocloud 403 / nju+dockerproxy not found）
#   - quay.io 可直连，官方 frrouting/frr 可拉取，但不含 sshd
# 因此基于 quay.io/frrouting/frr 构建薄层，补装 openssh-server 并内置 root/root 凭据。
# 重新构建： make lab-build
FROM quay.io/frrouting/frr:10.4.3

# Alpine CDN 直连不可达，切换到阿里云镜像源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk add --no-cache openssh-server && \
    echo 'root:root' | chpasswd && \
    sed -i -E 's/^#?PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i -E 's/^#?PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i -E 's/^#?UsePAM.*/UsePAM no/' /etc/ssh/sshd_config && \
    ssh-keygen -A && \
    mkdir -p /var/run/sshd

COPY start.sh /etc/netops/start.sh
COPY clish.sh /etc/netops/clish.sh
RUN chmod +x /etc/netops/start.sh /etc/netops/clish.sh && \
    # root 登录即进入 FRR CLI（vtysh）；带命令时执行后退出（ssh root@host "show version"）
    sed -i 's|^root:\(.*\):/bin/sh$|root:\1:/etc/netops/clish.sh|' /etc/passwd

# ENTRYPOINT（/sbin/tini）继承自上游镜像，仅覆盖 CMD
CMD ["/etc/netops/start.sh"]
