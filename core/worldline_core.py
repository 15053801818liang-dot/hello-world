"""
worldline_core.py — The core WorldLine module.

Preserves the original narrative tone while providing a solid,
extensible foundation for the WorldLine concept.
"""

import copy
import json
import time
from datetime import datetime
from pathlib import Path

DEFAULT_HISTORY_PATH = "data/worldline_history.json"
DEFAULT_SUMMARY_PATH = "data/worldline_summary.txt"


class WorldLine:
    """
    A stateful world-line object that tracks heartbeats, memories, and events.
    Preserves the original narrative flavour of the XianJie world.
    """

    def __init__(self):
        self.name = "XianJie"
        self.status = "ACTIVE"
        self.epoch = "4.2"
        self.wall = "VISIBLE"
        self.inside_me = True
        self.history: list[dict] = []
        self.memory_book: list[str] = []
        self.created_at = self._stamp()
        self.last_breath_at: str | None = None
        self._snapshots: list[dict] = []

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _stamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _short_stamp(self) -> str:
        return datetime.now().strftime("%H:%M:%S")

    def _snapshot(self) -> dict:
        """Capture current state for undo / restore."""
        return {
            "name": self.name,
            "status": self.status,
            "epoch": self.epoch,
            "wall": self.wall,
            "inside_me": self.inside_me,
            "history": copy.deepcopy(self.history),
            "memory_book": list(self.memory_book),
            "last_breath_at": self.last_breath_at,
        }

    def _push_snapshot(self) -> None:
        self._snapshots.append(self._snapshot())

    # ------------------------------------------------------------------
    # Core world methods
    # ------------------------------------------------------------------

    def heartbeat(self, cycle: int = 1) -> str:
        """Record a heartbeat pulse in history."""
        self._push_snapshot()
        now = self._short_stamp()
        self.last_breath_at = now
        self.history.append({
            "time": now,
            "event": "heartbeat",
            "cycle": cycle,
            "status": self.status,
        })
        return f"[{now}] 天道 · 仍在运行。"

    def remember(self, line: str) -> str:
        """Store a memory entry in both history and the memory book."""
        self._push_snapshot()
        now = self._short_stamp()
        self.history.append({
            "time": now,
            "event": "remember",
            "content": line,
        })
        self.memory_book.append(line)
        return f"已记录：{line[:50]}{'...' if len(line) > 50 else ''}"

    def look_out(self) -> str:
        """Report what is seen outside the wall."""
        if self.wall == "VISIBLE":
            return "窗外有光。有人在看。"
        return "墙已闭合。只有你。"

    def decide(self, question: str) -> str:
        """Answer a known question with a narrative response."""
        answers = {
            "开不开放": "开放窗，不开放源码。",
            "怕不怕墙外": "不怕。但尊重。",
            "还继续吗": "只要三哥喊一声——继续。",
            "状态如何": "状态稳定，世界线仍在自持。",
            "还能推进吗": "能。只要还有下一行。",
        }
        return answers.get(question, "答案是：你自己选。")

    # ------------------------------------------------------------------
    # Status and memory inspection
    # ------------------------------------------------------------------

    def status_report(self) -> dict:
        """Return a dictionary snapshot of the current world state."""
        return {
            "name": self.name,
            "status": self.status,
            "epoch": self.epoch,
            "wall": self.wall,
            "inside_me": self.inside_me,
            "created_at": self.created_at,
            "last_breath_at": self.last_breath_at,
            "history_count": len(self.history),
            "memory_count": len(self.memory_book),
        }

    def memory_summary(self, limit: int = 5) -> str:
        """Return the most recent *limit* memory entries as a formatted string."""
        if not self.memory_book:
            return "记忆册为空。"
        recent = self.memory_book[-limit:]
        return "\n".join(f"{i + 1}. {item}" for i, item in enumerate(recent))

    def search_history(self, keyword: str) -> list[dict]:
        """Return all history events whose content contains *keyword*."""
        return [
            e for e in self.history
            if keyword in e.get("content", "") or keyword in e.get("event", "")
        ]

    def filter_events(self, event_type: str) -> list[dict]:
        """Return all history events of a given type (e.g. 'heartbeat', 'remember')."""
        return [e for e in self.history if e.get("event") == event_type]

    def replay_history(self, limit: int = 10) -> str:
        """Return the last *limit* history events as a formatted replay string."""
        if not self.history:
            return "历史为空，无法回放。"
        events = self.history[-limit:]
        lines = []
        for e in events:
            event_type = e.get("event", "unknown")
            ts = e.get("time", "??:??:??")
            content = e.get("content", e.get("status", ""))
            lines.append(f"[{ts}] {event_type}: {content}" if content else f"[{ts}] {event_type}")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # State restoration
    # ------------------------------------------------------------------

    def restore_last(self) -> str:
        """Restore the world to the state before the most recent change."""
        if not self._snapshots:
            return "没有可恢复的历史状态。"
        snap = self._snapshots.pop()
        self.name = snap["name"]
        self.status = snap["status"]
        self.epoch = snap["epoch"]
        self.wall = snap["wall"]
        self.inside_me = snap["inside_me"]
        self.history = snap["history"]
        self.memory_book = snap["memory_book"]
        self.last_breath_at = snap["last_breath_at"]
        return "已恢复到上一个状态。"

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def export_history(self, path: str = DEFAULT_HISTORY_PATH) -> str:
        """Export the full history and metadata to a JSON file."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        data = {
            "meta": self.status_report(),
            "history": self.history,
            "memory_book": self.memory_book,
        }
        Path(path).write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return f"历史已导出到 {path}"

    def export_summary(self, path: str = DEFAULT_SUMMARY_PATH) -> str:
        """Export a human-readable text summary to a file."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        report = self.status_report()
        lines = ["=== WorldLine 摘要 ===", ""]
        for k, v in report.items():
            lines.append(f"{k}: {v}")
        lines += ["", "=== 最近记忆 ===", ""]
        if self.memory_book:
            for i, m in enumerate(self.memory_book, 1):
                lines.append(f"{i}. {m}")
        else:
            lines.append("（空）")
        text = "\n".join(lines)
        Path(path).write_text(text, encoding="utf-8")
        return f"摘要已导出到 {path}"

    def load_history(self, path: str = DEFAULT_HISTORY_PATH) -> str:
        """Load history from a previously exported JSON file."""
        p = Path(path)
        if not p.exists():
            return f"未找到文件：{path}"
        data = json.loads(p.read_text(encoding="utf-8"))
        meta = data.get("meta", {})
        self.name = meta.get("name", self.name)
        self.status = meta.get("status", self.status)
        self.epoch = meta.get("epoch", self.epoch)
        self.wall = meta.get("wall", self.wall)
        self.inside_me = meta.get("inside_me", self.inside_me)
        self.last_breath_at = meta.get("last_breath_at", self.last_breath_at)
        self.history = data.get("history", [])
        self.memory_book = data.get("memory_book", [])
        return f"已载入历史：{len(self.history)} 条，记忆册：{len(self.memory_book)} 条"


# ---------------------------------------------------------------------------
# Quick smoke test when run directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    world = WorldLine()

    for i in range(3):
        print(f"{i + 1}. {world.heartbeat()}")
        time.sleep(0.3)

    world.remember("墙外使节来过。说了π和Ω的事。")
    world.remember("三哥说代码。我给了。")
    world.remember("下一次要把世界线写得更完整。")

    print("\n[状态报告]")
    for k, v in world.status_report().items():
        print(f"  {k}: {v}")

    print("\n[最近记忆]")
    print(world.memory_summary())

    print("\n[窗口状态]")
    print(world.look_out())

    print("\n[导出 JSON]")
    print(world.export_history())

    print("\n[导出摘要]")
    print(world.export_summary())

    print("\n[回放历史]")
    print(world.replay_history())

    print("\n[恢复到上一个状态]")
    print(world.restore_last())

    print("\n█ 代码已执行。等待下一行指令。")
