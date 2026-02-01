"""
Main entry point for TacMap tactical overlay
"""
import pygame
import sys
import time
import math
import json
import os
from pathlib import Path

from .core import TacticalMap, Vector3, Entity
from .memory_reader import MemoryReader


def run_demo_mode(tac_map: TacticalMap):
    """Run in demo mode with simulated entities"""
    clock = pygame.time.Clock()
    running = True
    demo_time = 0
    
    print("\n" + "="*60)
    print("TacMap - War Thunder Tactical Overlay")
    print("="*60)
    print("Running in DEMO mode - showing simulated data")
    print("To use with War Thunder, you'll need to find memory addresses")
    print("\nControls:")
    print("  Arrow Keys: Pan map")
    print("  +/- or Mouse Wheel: Zoom")
    print("  R: Reset view")
    print("  ESC: Exit")
    print("="*60 + "\n")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    tac_map.zoom *= 1.1
                else:
                    tac_map.zoom *= 0.9
        
        tac_map.handle_input()
        
        # Simulate player movement
        demo_time += 0.016
        player_pos = Vector3(
            math.sin(demo_time * 0.3) * 500,
            100,
            math.cos(demo_time * 0.3) * 500
        )
        
        # Simulate entities
        entities = []
        for i in range(10):
            angle = (i / 10) * math.pi * 2 + demo_time * 0.1
            dist = 300 + i * 50
            entities.append(Entity(
                position=Vector3(
                    math.cos(angle) * dist,
                    100,
                    math.sin(angle) * dist
                ),
                velocity=Vector3(
                    math.cos(angle + math.pi/2) * 20,
                    0,
                    math.sin(angle + math.pi/2) * 20
                ),
                team=1 if i % 3 == 0 else 2,
                entity_type="aircraft" if i % 2 == 0 else "ground",
                health=50 + (i * 5) % 50,
                name=f"Target_{i+1}"
            ))
        
        tac_map.update(player_pos, entities)
        tac_map.render()
        clock.tick(60)
    
    pygame.quit()


def load_config():
    """Load configuration from config file"""
    # Try to find config in multiple locations
    config_paths = [
        Path.cwd() / "tacmap_config.json",
        Path.home() / ".tacmap" / "config.json",
        Path(__file__).parent / "config" / "default_config.json",
    ]
    
    for config_path in config_paths:
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except:
                continue
    
    # Return default config
    return {
        "process_name": "aces.exe",
        "addresses": {
            "player": {
                "x_position": "0x00000000",
                "y_position": "0x00000000",
                "z_position": "0x00000000",
            }
        },
        "display": {
            "width": 1920,
            "height": 1080,
        }
    }


def run_live_mode(tac_map: TacticalMap, config: dict):
    """Run with real game data"""
    mem_reader = MemoryReader(config.get("process_name", "aces.exe"))
    
    print("\n" + "="*60)
    print("TacMap - War Thunder Tactical Overlay")
    print("="*60)
    print("Searching for War Thunder process...")
    
    pid = mem_reader.find_process()
    if not pid:
        print("ERROR: War Thunder process not found!")
        print("Make sure War Thunder is running.")
        print("\nFalling back to DEMO mode...")
        time.sleep(2)
        return False
    
    print(f"Found War Thunder (PID: {pid})")
    print("Attaching to process...")
    
    if not mem_reader.open_process(pid):
        print("ERROR: Failed to attach to process!")
        print("Try running as Administrator.")
        print("\nFalling back to DEMO mode...")
        time.sleep(2)
        return False
    
    print("Successfully attached!")
    
    # Check if addresses are configured
    player_config = config.get("addresses", {}).get("player", {})
    x_addr = player_config.get("x_position", "0x00000000")
    
    if x_addr == "0x00000000":
        print("\nWARNING: No memory addresses configured!")
        print("Run 'tacmap-scanner' first to find addresses.")
        print("\nFalling back to DEMO mode...")
        mem_reader.close_process()
        time.sleep(2)
        return False
    
    print(f"Using address: {x_addr}")
    print("\nControls:")
    print("  Arrow Keys: Pan map")
    print("  +/- or Mouse Wheel: Zoom")
    print("  R: Reset view")
    print("  ESC: Exit")
    print("="*60 + "\n")
    
    clock = pygame.time.Clock()
    running = True
    
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        tac_map.zoom *= 1.1
                    else:
                        tac_map.zoom *= 0.9
            
            tac_map.handle_input()
            
            # Read player position
            try:
                x_addr_int = int(x_addr, 16)
                y_addr_int = int(player_config.get("y_position", hex(x_addr_int + 4)), 16)
                z_addr_int = int(player_config.get("z_position", hex(x_addr_int + 8)), 16)
                
                x = mem_reader.read_float(x_addr_int) or 0.0
                y = mem_reader.read_float(y_addr_int) or 0.0
                z = mem_reader.read_float(z_addr_int) or 0.0
                
                player_pos = Vector3(x, y, z)
                
                # For now, just show player position
                # Entity tracking would need additional addresses
                entities = []
                
                tac_map.update(player_pos, entities)
            except Exception as e:
                print(f"Error reading memory: {e}")
            
            tac_map.render()
            clock.tick(60)
    
    finally:
        mem_reader.close_process()
        pygame.quit()
    
    return True


def main():
    """Main entry point"""
    # Load configuration
    config = load_config()
    
    # Initialize tactical map
    width = config.get("display", {}).get("width", 1920)
    height = config.get("display", {}).get("height", 1080)
    tac_map = TacticalMap(width, height)
    
    # Try to run in live mode, fall back to demo if needed
    success = run_live_mode(tac_map, config)
    
    if not success:
        run_demo_mode(tac_map)
    
    sys.exit()


if __name__ == "__main__":
    main()
