"""FastMCP 设备工具链：10 只读 + 2 写（审批门/幂等/快照回滚）。

模块划分：
  - ``device``：netmiko/ncclient 连接封装与 ConfigTransaction 回滚状态机
  - ``approval``：审批 pending 队列（data/approvals.jsonl，一次性 token）
  - ``server``：FastMCP("netops-devices") 注册 12 个工具
"""
