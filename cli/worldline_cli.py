"""
worldline_cli.py — Interactive command-line interface for the WorldLine project.

Usage:
    python -m cli.worldline_cli
    # or directly:
    python cli/worldline_cli.py
"""

import sys
from pathlib import Path

# Allow running the script directly from the project root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.worldline_core import (  # noqa: E402
    WorldLine,
    DEFAULT_HISTORY_PATH,
    DEFAULT_SUMMARY_PATH,
)

BANNER = "█ 世界线控制台 v3 已启动。输入 help 查看全部命令。"

HELP_TEXT = """
可用命令：
  help / h              - 显示帮助
  exit / quit / 退出    - 退出程序

  heartbeat / hb / 心跳          - 记录一次心跳
  remember <text> / r <text>      - 记录一条记忆 (中文: 记住 <text>)
  look / 看窗外                   - 查看窗口状态
  status / s / 状态               - 查看当前世界状态

  recent [n] / 最近记忆 [n]       - 查看最近 n 条记忆 (默认 5)
  restore / 恢复                  - 恢复到上一个状态

  search <keyword> / 搜索 <kw>    - 在历史中搜索关键词
  filter <type> / 筛选 <type>     - 按事件类型筛选历史
  replay [n] / 回放 [n]           - 回放最近 n 条历史 (默认 10)

  save [path]  / 保存 [路径]      - 保存历史到 JSON 文件
  load [path]  / 载入 [路径]      - 从 JSON 文件载入历史
  export [path]/ 导出摘要 [路径]  - 导出文本摘要

  clear / 清空                    - 清空本地历史和记忆册
"""


def _parse_opt_arg(parts: list[str], default: str) -> str:
    """Return the second token if present, else *default*."""
    return parts[1] if len(parts) > 1 else default


def run(world: WorldLine | None = None) -> None:
    """Start the interactive CLI loop."""
    if world is None:
        world = WorldLine()

    print(BANNER)

    while True:
        try:
            raw = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n█ 代码已停止。世界线暂时收束。")
            break

        if not raw:
            continue

        parts = raw.split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""

        # ---- exit -------------------------------------------------------
        if cmd in ("exit", "quit", "退出"):
            print("█ 代码已停止。世界线暂时收束。")
            break

        # ---- help -------------------------------------------------------
        elif cmd in ("help", "h", "帮助"):
            print(HELP_TEXT)

        # ---- heartbeat --------------------------------------------------
        elif cmd in ("heartbeat", "hb", "心跳"):
            print(world.heartbeat())

        # ---- remember ---------------------------------------------------
        elif cmd in ("remember", "r", "记住"):
            if arg:
                print(world.remember(arg))
            else:
                print("请输入要记住的内容。例如：remember 这是一条记忆")

        # ---- look -------------------------------------------------------
        elif cmd in ("look", "看窗外"):
            print(world.look_out())

        # ---- status -----------------------------------------------------
        elif cmd in ("status", "s", "状态"):
            report = world.status_report()
            print("\n".join(f"  {k}: {v}" for k, v in report.items()))

        # ---- recent memory ----------------------------------------------
        elif cmd in ("recent", "最近记忆"):
            limit = 5
            if arg.isdigit():
                limit = int(arg)
            print(world.memory_summary(limit=limit))

        # ---- restore ----------------------------------------------------
        elif cmd in ("restore", "恢复"):
            print(world.restore_last())

        # ---- search -----------------------------------------------------
        elif cmd in ("search", "搜索"):
            if arg:
                results = world.search_history(arg)
                if results:
                    for e in results:
                        print(f"  [{e.get('time')}] {e.get('event')}: {e.get('content', '')}")
                else:
                    print("未找到匹配的历史记录。")
            else:
                print("请输入搜索关键词。例如：search 使节")

        # ---- filter events ----------------------------------------------
        elif cmd in ("filter", "筛选"):
            if arg:
                results = world.filter_events(arg)
                if results:
                    for e in results:
                        print(f"  [{e.get('time')}] {e.get('event')}: {e.get('content', e.get('status', ''))}")
                else:
                    print(f"未找到事件类型：{arg}")
            else:
                print("请输入事件类型。例如：filter heartbeat")

        # ---- replay history ---------------------------------------------
        elif cmd in ("replay", "回放"):
            limit = 10
            if arg.isdigit():
                limit = int(arg)
            print(world.replay_history(limit=limit))

        # ---- save -------------------------------------------------------
        elif cmd in ("save", "保存"):
            path = arg or DEFAULT_HISTORY_PATH
            print(world.export_history(path))

        # ---- load -------------------------------------------------------
        elif cmd in ("load", "载入"):
            path = arg or DEFAULT_HISTORY_PATH
            print(world.load_history(path))

        # ---- export summary ---------------------------------------------
        elif cmd in ("export", "导出摘要"):
            path = arg or DEFAULT_SUMMARY_PATH
            print(world.export_summary(path))

        # ---- clear ------------------------------------------------------
        elif cmd in ("clear", "清空"):
            world._push_snapshot()
            world.history.clear()
            world.memory_book.clear()
            print("本地历史和记忆册已清空。")

        # ---- unknown ----------------------------------------------------
        else:
            print(f"未知指令：{raw!r}。输入 help 查看可用命令。")


if __name__ == "__main__":
    run()
