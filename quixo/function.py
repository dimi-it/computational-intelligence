from dataclasses import dataclass, field
from typing import Callable, Sequence
import numpy as np

from quixo.quixo_game import QuixoGame
from quixo.value import ValuePoint


@dataclass
class Function:
    name: str
    inputs: int
    outputs: int = field(default=1)
    op: Callable[[ValuePoint | Sequence[ValuePoint], QuixoGame], ValuePoint] = field(default=lambda x, _: x)
    is_action: bool = field(default=False)

    def __str__(self):
        return self.name.upper()
