from random import Random
from typing import Set, List, Optional

from quixo.decorator import classproperty
from quixo.function_set import _get_random_from_set
from quixo.quixo_game import QuixoGame
from quixo.value_point import ValuePoint


class TerminalSet:
    _set: List[ValuePoint] = [
        *[ValuePoint((i, j)) for i in range(QuixoGame.BOARD_DIM) for j in range(QuixoGame.BOARD_DIM)],
        ValuePoint.NIL
    ]

    @classproperty
    def set(cls) -> List[ValuePoint]:
        """
        Return the terminal set
        """
        return cls._set

    @classmethod
    def get_random_terminal(cls, rnd: Random, to_exclude: Optional[ValuePoint] = None) -> ValuePoint:
        """
        Get random value point from terminal set
        """
        return _get_random_from_set(cls._set, rnd, to_exclude)

    @classmethod
    def get_random_terminals(cls, rnd: Random, count) -> List[ValuePoint]:
        """
        Get randoms value points from terminal set
        """
        return rnd.choices(cls._set, k=count)
