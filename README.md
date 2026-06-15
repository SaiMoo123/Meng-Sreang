# 🚀 Space Flappy

A space-themed Flappy Bird remake built with **Python + pygame**.

---

## Features

| Feature | Details |
|---|---|
| **Character** | Rocket ship (auto-generated PNG) |
| **Background** | Deep-space starfield with nebula + planet |
| **Obstacles** | Jagged asteroid columns |
| **Levels** | 10 levels: Easy (1-3), Medium (4-6), Hard (7-10) |
| **Menu** | Start · Continue · Level · Sound · Exit |
| **Save system** | Progress saved to `save_data.json` |
| **High scores** | Per-level best recorded |

---

## Quick Start

### 1 — Install dependencies

```bash
pip install pygame pillow
```

### 2 — Generate art assets

```bash
python generate_images.py
```

This creates `images/background.png`, `images/rocket.png`,
`images/asteroid_top.png`, `images/asteroid_bot.png`, `images/icon.png`.

### 3 — Play

```bash
python main.py
```

---

## Controls

| Key | Action |
|---|---|
| `↑` / `Space` / `W` / Click | Flap / jump |
| `↑` / `↓` / `W` / `S` | Navigate menu |
| `Enter` / `Space` | Select menu item |
| `Esc` | Back to menu |

---

## Level Progression

Pass **10 asteroid pairs** to clear a level and unlock the next.

| Level | Difficulty | Speed | Gap |
|---|---|---|---|
| 1–3 | Easy | Slow | Wide |
| 4–6 | Medium | Moderate | Medium |
| 7–10 | Hard | Fast | Narrow |

---

## Code Structure

```
space_flappy/
├── main.py             # Full game (menu, gameplay, HUD, save)
├── generate_images.py  # Creates all PNG assets with Pillow
├── images/             # Auto-generated assets (created by generate_images.py)
│   ├── background.png
│   ├── rocket.png
│   ├── asteroid_top.png
│   ├── asteroid_bot.png
│   └── icon.png
├── save_data.json      # Auto-created on first run
└── README.md
```

### Python patterns used

- **Docstrings** — module, class, and function level
- **Type annotations** — throughout (`int`, `float`, `list[Star]`, etc.)
- **Custom exceptions** — `GameError`, `AssetLoadError`, `SaveDataError`, `LevelRangeError`
- **try / except / finally** — asset loading, save I/O, main loop teardown
- **Dataclasses** — `SaveData`, `Star`
- **`__slots__`** — on `Rocket` and `Asteroid` for memory efficiency
- **`NOTE:` markers** — inline design explanations

---

## Requirements

- Python 3.10+
- `pygame >= 2.0`
- `Pillow >= 9.0` (only for `generate_images.py`)
