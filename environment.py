import random
from dataclasses import dataclass, field
from typing import List, Tuple, Set, Dict

Coord = Tuple[int, int]

@dataclass
class WildfireWorld:
    width: int = 20
    height: int = 20
    fire_start: Coord = (5, 5)
    initial_spread_prob: float = 0.3
    wind_direction: str = "NE"  # North-East
    wind_strength: float = 0.5
    
    # Internal state
    grid: Dict[Coord, str] = field(default_factory=dict) # 'forest', 'fire', 'burnt', 'water'
    fire_cells: Set[Coord] = field(default_factory=set)
    steps: int = 0
    rng: random.Random = field(default_factory=random.Random)

    def __post_init__(self):
        self.reset()

    def reset(self):
        self.grid = {}
        for y in range(self.height):
            for x in range(self.width):
                self.grid[(x, y)] = "forest"
        
        self.fire_cells = {self.fire_start}
        self.grid[self.fire_start] = "fire"
        self.steps = 0

    def get_neighbors(self, pos: Coord) -> List[Coord]:
        x, y = pos
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append((nx, ny))
        return neighbors

    def get_wind_bias(self, from_pos: Coord, to_pos: Coord) -> float:
        fx, fy = from_pos
        tx, ty = to_pos
        dx, dy = tx - fx, ty - fy
        
        bias = 1.0
        if "N" in self.wind_direction and dy < 0: bias += self.wind_strength
        if "S" in self.wind_direction and dy > 0: bias += self.wind_strength
        if "E" in self.wind_direction and dx > 0: bias += self.wind_strength
        if "W" in self.wind_direction and dx < 0: bias += self.wind_strength
        
        return bias

    def step(self) -> Dict[str, any]:
        new_fires = set()
        burnt_out = set()
        
        # Fire spread logic
        for fire_pos in self.fire_cells:
            for neighbor in self.get_neighbors(fire_pos):
                if self.grid[neighbor] == "forest":
                    bias = self.get_wind_bias(fire_pos, neighbor)
                    if self.rng.random() < (self.initial_spread_prob * bias):
                        new_fires.add(neighbor)
            
            # Probability of burning out
            if self.rng.random() < 0.2:
                burnt_out.add(fire_pos)

        for pos in new_fires:
            self.grid[pos] = "fire"
            self.fire_cells.add(pos)
        
        for pos in burnt_out:
            self.grid[pos] = "burnt"
            self.fire_cells.discard(pos)

        self.steps += 1
        return {
            "step": self.steps,
            "fire_count": len(self.fire_cells),
            "new_fires": list(new_fires),
            "extinguished": list(burnt_out)
        }

    def apply_action(self, pos: Coord, action_type: str):
        """Apply a response action (e.g., water drop) to a cell."""
        if action_type == "water_drop":
            if self.grid.get(pos) == "fire":
                self.grid[pos] = "burnt" # Effectively extinguished
                self.fire_cells.discard(pos)

    def get_state_summary(self) -> Dict[str, any]:
        return {
            "step": self.steps,
            "fire_cells": list(self.fire_cells),
            "wind": self.wind_direction,
            "grid_snapshot": self.grid # Simplified for simulation
        }
