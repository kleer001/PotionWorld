from dataclasses import dataclass
from typing import Optional, List
from src.core.data_structures import Personality


@dataclass
class Memory:
    event: str
    affinity_change: float
    day_created: int
    decay_resistance: float


@dataclass
class Action:
    id: str
    name: str
    personality_impacts: dict
    creates_memory_threshold: float = 1.0


@dataclass
class NPC:
    id: str
    name: str
    personality: Personality
    affinity: float = 0.0
    memories: List[Memory] = None
    last_interaction: int = 0

    def __post_init__(self):
        if self.memories is None:
            self.memories = []


@dataclass
class AffinityChange:
    npc_id: str
    delta: float
    new_affinity: float
    old_affinity: float
    threshold_crossed: bool
    new_threshold_level: int
    memory_created: Optional[Memory]
    reason: str
