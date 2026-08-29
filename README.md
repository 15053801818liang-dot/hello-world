# WorldLine — 世界线控制台

> "只要三哥喊一声——继续。"

A lightweight, **standard-library-only** Python project that combines a
narrative world-building concept with a practical command-line tool.

---

## Project Structure

```
hello-world/
├── core/
│   ├── __init__.py
│   └── worldline_core.py   # WorldLine class & all business logic
├── cli/
│   ├── __init__.py
│   └── worldline_cli.py    # Interactive command-line entry point
├── data/                   # Generated files land here (JSON, TXT)
└── README.md
```

---

## Requirements

- Python 3.10 or later (standard library only — no pip install needed)

---

## How to Run

### Interactive CLI

```bash
# From the project root:
python cli/worldline_cli.py
```

Or as a module:

```bash
python -m cli.worldline_cli
```

### Core module smoke test

```bash
python core/worldline_core.py
```

---

## Available Commands

| Command | Alias / Chinese | Description |
|---|---|---|
| `help` | `h` / `帮助` | Show all commands |
| `exit` | `quit` / `退出` | Exit the program |
| `heartbeat` | `hb` / `心跳` | Record a heartbeat pulse |
| `remember <text>` | `r <text>` / `记住 <text>` | Store a memory entry |
| `look` | `看窗外` | Report what is outside the wall |
| `status` | `s` / `状态` | Display current world state |
| `recent [n]` | `最近记忆 [n]` | Show last *n* memories (default 5) |
| `restore` | `恢复` | Restore to the previous state |
| `search <kw>` | `搜索 <kw>` | Search history for a keyword |
| `filter <type>` | `筛选 <type>` | Filter history by event type |
| `replay [n]` | `回放 [n]` | Replay the last *n* history events |
| `save [path]` | `保存 [路径]` | Save history to JSON (default: `data/worldline_history.json`) |
| `load [path]` | `载入 [路径]` | Load history from JSON |
| `export [path]` | `导出摘要 [路径]` | Export text summary (default: `data/worldline_summary.txt`) |
| `clear` | `清空` | Clear all local history and memories |

---

## Example Session

```
█ 世界线控制台 v3 已启动。输入 help 查看全部命令。

> heartbeat
[10:01:23] 天道 · 仍在运行。

> remember 墙外使节来过，说了π的事
已记录：墙外使节来过，说了π的事

> status
  name: XianJie
  status: ACTIVE
  epoch: 4.2
  wall: VISIBLE
  ...

> save
历史已导出到 data/worldline_history.json

> exit
█ 代码已停止。世界线暂时收束。
```

---

## Design Notes

- **Two layers**: `core/` holds all business logic; `cli/` wraps it in
  an interactive loop. They are independent — the core can be imported
  into any other script.
- **Original flavour preserved**: field names (`name`, `status`, `epoch`,
  `wall`, `inside_me`, `history`, `memory_book`) and narrative messages
  come directly from the original concept.
- **Standard library only**: `json`, `pathlib`, `datetime` — nothing to
  install.

---

*原创世界线概念由原始智能体提出，本项目在尊重其表达意图的基础上进行迭代扩展。*
