.PHONY: setup milvus-up milvus-down milvus-ps models test lab-pull lab-build clab-runner lab-up lab-down lab-inspect

CLAB_VERSION ?= 0.79.0
CLAB_TARBALL_URL := https://ghproxy.net/https://github.com/srl-labs/containerlab/releases/download/v$(CLAB_VERSION)/containerlab_$(CLAB_VERSION)_linux_amd64.tar.gz
CLAB_RUNNER ?= netops/clab-runner:$(CLAB_VERSION)
LAB_DIR := deploy/containerlab
LAB_DIR_ABS := $(CURDIR)/$(LAB_DIR)

# 本机 daemon 为 Docker Desktop 形态（容器/网桥在 daemon 侧 netns，原生 clab 的
# netlink 操作不可达），故按官方 "clab in docker" 方案以特权容器运行 clab，
# 与 daemon 共享宿主 netns（--privileged --network host + 挂载 docker.sock）。
# topology 内 binds 使用同路径挂载，保证 daemon 侧路径翻译可用。
CLAB_RUN := docker run --rm --privileged --network host --pid host \
	-v /var/run/docker.sock:/var/run/docker.sock \
	-v $(LAB_DIR_ABS):$(LAB_DIR_ABS) \
	-w $(LAB_DIR_ABS) \
	$(CLAB_RUNNER)

setup:
	uv sync
	cp -n .env.example .env || true

milvus-up:
	docker compose -f deploy/docker-compose.milvus.yml up -d

milvus-down:
	docker compose -f deploy/docker-compose.milvus.yml down

milvus-ps:
	docker compose -f deploy/docker-compose.milvus.yml ps

models:
	uv run python scripts/download_models.py

test:
	uv run pytest -m "not milvus and not gpu and not lab"

# —— Containerlab 仿真拓扑（详见 deploy/containerlab/netops.clab.yml）——

# 拉取不可直连的外部镜像（fresh-clone 自含；幂等：镜像已存在则跳过）。
# FRR 基础镜像（quay.io 可直连）由 lab-build 的 docker build 自动拉取，无需在此处理。
lab-pull:
	@if docker image inspect sysrepo/netopeer2:latest >/dev/null 2>&1; then \
		echo "sysrepo/netopeer2:latest 已存在，跳过（幂等）"; \
	else \
		echo "拉取 sysrepo/netopeer2（经 docker.1ms.run 镜像）..."; \
		docker pull docker.1ms.run/sysrepo/netopeer2:latest && \
		docker tag docker.1ms.run/sysrepo/netopeer2:latest sysrepo/netopeer2:latest; \
	fi

# FRR+sshd 节点镜像（quay.io/frrouting/frr 直连可拉，薄层补 openssh-server）
lab-build:
	docker build -f $(LAB_DIR)/docker/frr-ssh.Dockerfile \
		-t netops/frr-ssh:10.4.3 $(LAB_DIR)/docker

# containerlab 运行器镜像（clab v$(CLAB_VERSION)；tarball 经 ghproxy 系镜像下载，
# 已 gitignore；下载失败有清晰报错）
clab-runner: $(LAB_DIR)/docker/.clab.tar.gz
	docker build -f $(LAB_DIR)/docker/clab-runner.Dockerfile \
		-t $(CLAB_RUNNER) $(LAB_DIR)/docker

$(LAB_DIR)/docker/.clab.tar.gz:
	@wget -qO $@ "$(CLAB_TARBALL_URL)" \
		|| wget -qO $@ "$(subst ghproxy.net,gh-proxy.com,$(CLAB_TARBALL_URL))" \
		|| { echo "ERROR: containerlab tarball 下载失败（ghproxy.net / gh-proxy.com 均不可达）；" \
		     "请手动下载 $(CLAB_TARBALL_URL) 并放置为 $@ 后重试"; exit 1; }

lab-up: lab-pull lab-build clab-runner
	$(CLAB_RUN) deploy -t netops.clab.yml

lab-down: clab-runner
	$(CLAB_RUN) destroy -t netops.clab.yml --cleanup

lab-inspect: clab-runner
	$(CLAB_RUN) inspect -t netops.clab.yml
