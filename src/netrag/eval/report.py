import datetime
import subprocess
from pathlib import Path


def write_report(path: Path, title: str, summary_rows: dict[str, str], body_md: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        rev = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        rev = "unknown"
    lines = [
        f"# {title}", "",
        f"- 日期：{datetime.date.today().isoformat()}",
        f"- git：`{rev}`", "",
        "| 指标 | 值 |", "|---|---|",
    ]
    lines += [f"| {k} | {v} |" for k, v in summary_rows.items()]
    lines += ["", body_md, ""]
    path.write_text("\n".join(lines))
    print(f"report written: {path}")
