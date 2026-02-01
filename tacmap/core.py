"""
Core tactical map implementation
"""
import pygame
import math
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Vector3:
    """3D vector for positions and velocities"""
    x: float
    y: float
    z: float


@dataclass
class Entity:
    """Represents a game entity (vehicle, aircraft, etc.)"""
    position: Vector3
    velocity: Vector3
    team: int
    entity_type: str
    health: float
    name: str = ""


class TacticalMap:
    """Main tactical map display class"""
    
    def __init__(self, width: int = 1920, height: int = 1080):
        """
        Initialize the tactical map
        
        Args:
            width: Display width in pixels
            height: Display height in pixels
        """
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("TacMap - War Thunder Tactical Overlay")
        
        # Colors - Cyberpunk theme
        self.BG_COLOR = (10, 15, 25)
        self.GRID_COLOR = (30, 40, 60)
        self.FRIENDLY_COLOR = (50, 200, 50)
        self.ENEMY_COLOR = (200, 50, 50)
        self.NEUTRAL_COLOR = (200, 200, 50)
        self.TEXT_COLOR = (200, 220, 255)
        self.HUD_COLOR = (100, 150, 255)
        
        # Map settings
        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.map_scale = 10  # meters per pixel
        
        # Fonts
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # Game data
        self.player_pos = Vector3(0, 0, 0)
        self.entities: List[Entity] = []
        
    def world_to_screen(self, world_pos: Vector3) -> Tuple[int, int]:
        """Convert world coordinates to screen coordinates"""
        # Center map on player
        rel_x = world_pos.x - self.player_pos.x
        rel_y = world_pos.z - self.player_pos.z  # Using Z as top-down Y
        
        screen_x = int(self.width / 2 + (rel_x / self.map_scale) * self.zoom + self.offset_x)
        screen_y = int(self.height / 2 - (rel_y / self.map_scale) * self.zoom + self.offset_y)
        
        return screen_x, screen_y
    
    def draw_grid(self):
        """Draw background grid"""
        grid_spacing = 100  # 100 meters
        
        for x in range(-2000, 2000, grid_spacing):
            sx, sy1 = self.world_to_screen(Vector3(x, 0, -2000))
            _, sy2 = self.world_to_screen(Vector3(x, 0, 2000))
            pygame.draw.line(self.screen, self.GRID_COLOR, (sx, sy1), (sx, sy2), 1)
        
        for y in range(-2000, 2000, grid_spacing):
            sx1, sy = self.world_to_screen(Vector3(-2000, 0, y))
            sx2, _ = self.world_to_screen(Vector3(2000, 0, y))
            pygame.draw.line(self.screen, self.GRID_COLOR, (sx1, sy), (sx2, sy), 1)
    
    def draw_entity(self, entity: Entity, is_player: bool = False):
        """Draw an entity on the map"""
        sx, sy = self.world_to_screen(entity.position)
        
        # Determine color and size based on team
        if is_player:
            color = self.HUD_COLOR
            size = 8
        elif entity.team == 1:
            color = self.FRIENDLY_COLOR
            size = 6
        elif entity.team == 2:
            color = self.ENEMY_COLOR
            size = 6
        else:
            color = self.NEUTRAL_COLOR
            size = 5
        
        # Draw entity icon based on type
        if entity.entity_type == "aircraft":
            # Triangle for aircraft
            points = [
                (sx, sy - size),
                (sx - size, sy + size),
                (sx + size, sy + size)
            ]
            pygame.draw.polygon(self.screen, color, points)
            pygame.draw.polygon(self.screen, self.TEXT_COLOR, points, 1)
        elif entity.entity_type == "ground":
            # Square for ground vehicles
            pygame.draw.rect(self.screen, color, (sx - size, sy - size, size * 2, size * 2))
            pygame.draw.rect(self.screen, self.TEXT_COLOR, (sx - size, sy - size, size * 2, size * 2), 1)
        else:
            # Default circle
            pygame.draw.circle(self.screen, color, (sx, sy), size)
            pygame.draw.circle(self.screen, self.TEXT_COLOR, (sx, sy), size, 1)
        
        # Draw velocity indicator
        if entity.velocity.x != 0 or entity.velocity.z != 0:
            vel_length = math.sqrt(entity.velocity.x**2 + entity.velocity.z**2)
            if vel_length > 1:
                vel_norm_x = entity.velocity.x / vel_length
                vel_norm_z = entity.velocity.z / vel_length
                end_x = sx + int(vel_norm_x * 20)
                end_y = sy - int(vel_norm_z * 20)
                pygame.draw.line(self.screen, color, (sx, sy), (end_x, end_y), 2)
        
        # Draw health bar
        if entity.health < 100:
            bar_width = 30
            bar_height = 4
            health_width = int((entity.health / 100) * bar_width)
            pygame.draw.rect(self.screen, (100, 100, 100), 
                           (sx - bar_width//2, sy + size + 3, bar_width, bar_height))
            pygame.draw.rect(self.screen, (200, 50, 50), 
                           (sx - bar_width//2, sy + size + 3, health_width, bar_height))
        
        # Draw name/distance
        if entity.name:
            distance = math.sqrt(
                (entity.position.x - self.player_pos.x)**2 +
                (entity.position.z - self.player_pos.z)**2
            )
            text = f"{entity.name} ({int(distance)}m)"
            text_surf = self.font_small.render(text, True, self.TEXT_COLOR)
            self.screen.blit(text_surf, (sx + size + 5, sy - 8))
    
    def draw_hud(self):
        """Draw HUD information"""
        y_offset = 10
        
        # Title
        title = self.font_large.render("TACMAP - WAR THUNDER", True, self.HUD_COLOR)
        self.screen.blit(title, (10, y_offset))
        y_offset += 40
        
        # Player position
        pos_text = f"Position: X:{self.player_pos.x:.1f} Y:{self.player_pos.y:.1f} Z:{self.player_pos.z:.1f}"
        pos_surf = self.font_medium.render(pos_text, True, self.TEXT_COLOR)
        self.screen.blit(pos_surf, (10, y_offset))
        y_offset += 30
        
        # Zoom level
        zoom_text = f"Zoom: {self.zoom:.2f}x | Scale: {self.map_scale}m/px"
        zoom_surf = self.font_small.render(zoom_text, True, self.TEXT_COLOR)
        self.screen.blit(zoom_surf, (10, y_offset))
        y_offset += 25
        
        # Entity count
        friendly = sum(1 for e in self.entities if e.team == 1)
        enemy = sum(1 for e in self.entities if e.team == 2)
        entity_text = f"Entities: {len(self.entities)} | Friendly: {friendly} | Enemy: {enemy}"
        entity_surf = self.font_small.render(entity_text, True, self.TEXT_COLOR)
        self.screen.blit(entity_surf, (10, y_offset))
        
        # Legend
        legend_y = self.height - 100
        legend_items = [
            ("Player", self.HUD_COLOR),
            ("Friendly", self.FRIENDLY_COLOR),
            ("Enemy", self.ENEMY_COLOR),
            ("Neutral", self.NEUTRAL_COLOR)
        ]
        
        for i, (label, color) in enumerate(legend_items):
            x = self.width - 150
            y = legend_y + i * 25
            pygame.draw.circle(self.screen, color, (x, y), 6)
            text = self.font_small.render(label, True, self.TEXT_COLOR)
            self.screen.blit(text, (x + 15, y - 8))
        
        # Controls help
        help_y = self.height - 120
        help_text = [
            "Controls:",
            "Arrow Keys: Pan map",
            "+/- or Mouse Wheel: Zoom",
            "R: Reset view",
            "ESC: Exit"
        ]
        for i, text in enumerate(help_text):
            surf = self.font_small.render(text, True, self.TEXT_COLOR)
            self.screen.blit(surf, (10, help_y + i * 20))
    
    def handle_input(self):
        """Handle user input"""
        keys = pygame.key.get_pressed()
        
        # Pan
        pan_speed = 5
        if keys[pygame.K_LEFT]:
            self.offset_x -= pan_speed
        if keys[pygame.K_RIGHT]:
            self.offset_x += pan_speed
        if keys[pygame.K_UP]:
            self.offset_y -= pan_speed
        if keys[pygame.K_DOWN]:
            self.offset_y += pan_speed
        
        # Zoom
        if keys[pygame.K_EQUALS] or keys[pygame.K_PLUS]:
            self.zoom *= 1.05
        if keys[pygame.K_MINUS]:
            self.zoom *= 0.95
        
        # Reset view
        if keys[pygame.K_r]:
            self.zoom = 1.0
            self.offset_x = 0
            self.offset_y = 0
    
    def update(self, player_pos: Vector3, entities: List[Entity]):
        """Update map data"""
        self.player_pos = player_pos
        self.entities = entities
    
    def render(self):
        """Render the tactical map"""
        self.screen.fill(self.BG_COLOR)
        
        # Draw grid
        self.draw_grid()
        
        # Draw entities
        for entity in self.entities:
            self.draw_entity(entity)
        
        # Draw player
        player_entity = Entity(
            position=self.player_pos,
            velocity=Vector3(0, 0, 0),
            team=1,
            entity_type="player",
            health=100,
            name="YOU"
        )
        self.draw_entity(player_entity, is_player=True)
        
        # Draw HUD
        self.draw_hud()
        
        pygame.display.flip()
