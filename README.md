# TacMap - War Thunder Tactical Overlay

**A read-only tactical map overlay for War Thunder that displays real-time game data on a second monitor.**

[![PyPI](https://img.shields.io/pypi/v/tacmap)](https://pypi.org/project/tacmap/)
[![Python](https://img.shields.io/pypi/pyversions/tacmap)](https://pypi.org/project/tacmap/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ⚠️ Disclaimer

**Educational purposes only.** This tool:
- Only **reads** game memory (does not modify)
- May violate War Thunder's Terms of Service
- May trigger anti-cheat detection
- Should be used **offline or in custom matches only**
- Comes with **no warranty**

**Use at your own risk.** Not responsible for bans or consequences.

---

## ✨ Features

- 🗺️ Real-time tactical map on secondary monitor
- ✈️ Entity tracking (aircraft, ground vehicles)
- 📊 Position & velocity visualization
- 🎨 Team colors (friendly/enemy/neutral)
- ❤️ Health bars and distance indicators
- 🔍 Zoom & pan controls
- 📐 Grid overlay with distance markers
- 🎮 Demo mode for testing

---

## 🚀 Quick Start

### Install
```bash
pip install tacmap
```

### Run Demo
```bash
tacmap
```

### Find Addresses
```bash
tacmap-scanner  # Run as Administrator
```

### Configure
Create `tacmap_config.json`:
```json
{
  "process_name": "aces_BE.exe",
  "addresses": {
    "player": {
      "x_position": "0x12345678",
      "y_position": "0x1234567C",
      "z_position": "0x12345680"
    }
  }
}
```

### Run with Game
```bash
tacmap
```

---

## 🎮 Controls

| Key | Action |
|-----|--------|
| Arrow Keys | Pan map |
| +/- | Zoom |
| Mouse Wheel | Zoom |
| R | Reset view |
| ESC | Exit |

---

## 🔍 Finding Addresses

Memory addresses change with every game update. To find them:

1. Start War Thunder (match/test drive)
2. Run `tacmap-scanner` as Admin
3. Note your X coordinate in game
4. Scan for that value
5. Move vehicle significantly
6. Scan again with new value
7. Repeat until <50 addresses
8. Use addresses in config

**Tip:** Position is usually 3 consecutive floats. If X is at `0x12345678`, try Y at `+4` and Z at `+8`.

---

## 📊 Display Guide

**Icons:**
- ▲ Aircraft
- ■ Ground vehicle
- ● Other

**Colors:**
- 🔵 Blue = You
- 🟢 Green = Friendly
- 🔴 Red = Enemy
- 🟡 Yellow = Neutral

---

## 🛠️ Troubleshooting

**Process not found:**
- Ensure War Thunder is running
- Run as Administrator
- Check process name (aces.exe vs aces_BE.exe)

**Failed to attach:**
- Run as Administrator (required)
- Close other memory tools
- Check antivirus

**Wrong position:**
- Addresses changed (game updated)
- Re-scan for new addresses

---

## 📝 License

MIT License - Educational purposes only.

---

## 💬 Contact

- Email: antmanitis7@gmail.com
- Discord: S4nPV2Rx7F
- Issues: [GitHub](https://github.com/binx-ux/tacmap/issues)

---

**Made by binxix | Use responsibly! 🎮**
