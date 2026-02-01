# Changelog

All notable changes to TacMap will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-01

### Added
- Initial release of TacMap
- Real-time tactical map overlay for War Thunder
- Read-only memory reading functionality
- Interactive memory scanner tool
- Entity tracking system (aircraft, ground vehicles)
- Position and velocity visualization
- Team identification (friendly/enemy/neutral)
- Health bars and distance indicators
- Zoom and pan controls
- Grid overlay with distance markers
- Demo mode for testing without game
- Configurable display settings
- Command-line entry points (`tacmap` and `tacmap-scanner`)
- Comprehensive documentation and README
- MIT License

### Features
- Windows API integration for process memory reading
- Pygame-based visualization
- Cyberpunk-themed UI
- 60 FPS rendering
- Automatic process detection
- Support for aces.exe and aces_BE.exe

### Security
- Read-only memory access (no game modification)
- No network communication
- No data collection
- Open source code

### Known Limitations
- Windows only (requires Windows API)
- Memory addresses change with game updates
- Requires manual address configuration
- Limited entity tracking (requires address discovery)
- May trigger anti-cheat detection
- Educational/offline use recommended

## [Unreleased]

### Planned Features
- Automatic address pattern detection
- Entity list scanning
- Improved UI customization
- Configuration GUI
- Replay system
- Statistics tracking
- Multiple display profiles
- Better error handling

---

For more information, see the [README](README.md).
