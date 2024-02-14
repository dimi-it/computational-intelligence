from dataclasses import dataclass, field
from typing import Callable, Sequence
import numpy as np

from quixo.quixo_game import QuixoGame
from quixo.value_point import ValuePoint


def _fun_default(inputs: Sequence[ValuePoint], game: QuixoGame) -> ValuePoint:
    assert len(inputs) == 1, f"Expected 1 inputs got {len(inputs)}"
    return inputs[0]


@dataclass
class Function:
    name: str
    inputs: int
    outputs: int = field(default=1)
    op: Callable[[Sequence[ValuePoint], QuixoGame], ValuePoint] = field(default=_fun_default)
    is_action: bool = field(default=False)

    def __str__(self):
        return self.name.upper()
