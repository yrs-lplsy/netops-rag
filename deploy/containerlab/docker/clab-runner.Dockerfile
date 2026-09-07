# containerlab 运行器镜像（netops lab 专用）
#
# 本机 docker daemon 为 Docker Desktop 形态：容器/网桥位于 daemon 侧独立 netns，
# 宿主 distro 中原生 clab 的 netlink 操作（查 mgmt 网桥、创建 veth）不可达
# （报 "Failed to lookup link br-..."）。按 containerlab 官方 "clab in docker"
# 方案，以特权容器（--privileged --network host）运行 clab，使 clab 与
# daemon 处于同一 netns。调用方式见 Makefile 的 CLAB_RUN / task-11 报告。
#
# 构建需要 .clab.tar.gz（已 gitignore）：make clab-runner 会自动下载（ghproxy 镜像）。
FROM docker.m.daocloud.io/library/alpine:3.20

# Alpine CDN 直连不可达，切换阿里云源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk add --no-cache bash iproute2 iputils iptables

COPY .clab.tar.gz /tmp/clab.tar.gz
RUN tar -xzf /tmp/clab.tar.gz -C /usr/local/bin containerlab && \
    mv /usr/local/bin/containerlab /usr/local/bin/clab && \
    chmod +x /usr/local/bin/clab && \
    rm -f /tmp/clab.tar.gz && \
    clab version | grep version

ENTRYPOINT ["clab"]
