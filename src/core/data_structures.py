from dataclasses import dataclass
from enum import IntEnum


class Quality(IntEnum):
    POOR = 1
    STANDARD = 2
    FINE = 3
    EXCEPTIONAL = 4
    MASTERWORK = 5


@dataclass
class Personality:
    openness: int
    conscientiousness: int
    extraversion: int
    agreeableness: int
    neuroticism: int
