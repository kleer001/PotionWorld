from dataclasses import dataclass, field


@dataclass
class Character:
    name: str
    hp: int
    max_hp: int
    strength: int
    defense: int
    active_effects: list = field(default_factory=list)


@dataclass
class GameState:
    hero: Character
    enemy: Character
    mana: int
    max_mana: int
    deck: list          # Card dicts remaining in deck
    hand: list          # Card dicts in hand
    lock: list          # [Card|None] per slot
    slot_count: int
    hand_size: int
    phase: str          # "preview", "build", "resolve", "reward"
    smooth_draws: int = 0    # how many full-hand draws get Arena-style smoothing
    smooth_draws_left: int = 0  # remaining smoothed draws this battle
    battle_log: list = field(default_factory=list)
    turn: int = 0
