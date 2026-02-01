"""
TacMap - War Thunder Tactical Map Overlay
==========================================

A read-only tactical map overlay for War Thunder that displays
real-time game information on a secondary monitor.

Features:
- Real-time entity tracking
- Position and velocity visualization
- Team identification (friendly/enemy)
- Health bars and distance indicators
- Zoom and pan controls
- Grid overlay with distance markers

Usage:
    # Run the tactical map
    $ tacmap
    
    # Run the memory scanner
    $ tacmap-scanner

Author: binxix
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "binxix"
__license__ = "MIT"

from .core import TacticalMap, Vector3, Entity
from .memory_reader import MemoryReader
from .memory_scanner import MemoryScanner

__all__ = [
    "TacticalMap",
    "Vector3",
    "Entity",
    "MemoryReader",
    "MemoryScanner",
]
