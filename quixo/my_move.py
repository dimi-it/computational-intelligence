from dataclasses import dataclass
from functools import cached_property
from typing import Sequence

from quixo.game import Move


@dataclass
class MyMove:
    position: Sequence[int]
    move: Move

    def __str__(self):
        return f"Position: {self.position}, Move: {self.move}"

    @property
    def to_tuple(self) -> tuple[tuple[int, int], Move]:
        return (self.position[0], self.position[1]), self.move

    @cached_property
    def position_reversed(self) -> Sequence[int]:
        return self.position[1], self.position[0]
