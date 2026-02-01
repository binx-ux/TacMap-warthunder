# TacMap Quick Reference

## Install
```bash
pip install tacmap
```

## Commands
```bash
tacmap           # Run tactical map
tacmap-scanner   # Find memory addresses
```

## Controls
- **Arrow Keys** - Pan map
- **+/-** - Zoom
- **R** - Reset view
- **ESC** - Exit

## Config File

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

## Finding Addresses

1. Start War Thunder
2. Run `tacmap-scanner` as Admin
3. Scan for X coordinate
4. Move vehicle
5. Scan for new X value
6. Repeat until <50 results
7. Use addresses in config

## Troubleshooting

**Process not found** - Run as Admin, check process name  
**Wrong position** - Addresses changed, re-scan  
**Can't attach** - Run as Administrator

---

**Contact:** antmanitis7@gmail.com | Discord: S4nPV2Rx7F
