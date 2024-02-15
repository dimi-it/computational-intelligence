from dataclasses import dataclass
from functools import cached_property
from typing import Sequence, List, Tuple

from quixo.game import MoveDirection


@dataclass
class MyMove:
    position: Tuple[int, int]
    direction: MoveDirection

    def __hash__(self):
        return hash((self.position, self.direction))

    def __str__(self):
        return f"Position: {self.position}, Direction: {self.direction}"

    @property
    def to_tuple(self) -> tuple[tuple[int, int], MoveDirection]:
        return (self.position[0], self.position[1]), self.direction

    @cached_property
    def position_reversed(self) -> Tuple[int, int]:
        return self.position[1], self.position[0]
