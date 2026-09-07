"""FastAPI 服务启动脚本（uvicorn）。

用法：
    uv run python scripts/run_server.py [--host 127.0.0.1] [--port 8000]

app 工厂在 import 期零副作用：Milvus/嵌入模型/LLM/MCP 网关等重组件在首个
用到图的请求上才懒构建（见 netrag/api/app.py）。写操作不经过本服务——
/diagnose 至多给出变更计划提案，执行须走审批门（/approvals/{id}/approve
取一次性 token 后由运维侧显式调用 MCP 写工具）。
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import uvicorn

from netrag.api.app import create_app

app = create_app()  # 廉价：仅注册路由，组件懒构建


def main() -> None:
    ap = argparse.ArgumentParser(description="netops-rag API server")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()
    if args.host not in ("127.0.0.1", "localhost", "::1"):
        # 评审 Finding 1：approve 端点仅受共享密钥门（APPROVE_SECRET）保护，
        # 未配置时完全无鉴权；非回环绑定 = 扩大自批拿写 token 的暴露面
        print(
            "[安全警告] --host 非本机回环：POST /approvals/{id}/approve 仅受共享"
            "密钥门（.env 的 APPROVE_SECRET，未配置则无鉴权）保护，写执行面保持在"
            "服务外；请勿将本服务暴露公网。",
            file=sys.stderr,
        )
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
