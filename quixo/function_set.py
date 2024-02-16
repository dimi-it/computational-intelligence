from random import Random
from typing import Set, Sequence, List, Optional

import numpy as np

from quixo.decorator import classproperty
from quixo.function import Function
from quixo.quixo_game import QuixoGame
from quixo.value_point import ValuePoint


def _fun_and(inputs: Sequence[ValuePoint], game: QuixoGame) -> ValuePoint:
    assert len(inputs) == 2, f"Expected 2 inputs got {len(inputs)}"

    if inputs[0].is_nil() or inputs[1].is_nil():
        return ValuePoint.NIL
    else:
        return inputs[1]


def _fun_or(inputs: Sequence[ValuePoint], game: QuixoGame) -> ValuePoint:
    assert len(inputs) == 2, f"Expected 2 inputs got {len(inputs)}"

    if not inputs[0].is_nil():
        return inputs[0]
    else:
        return inputs[1]


def _fun_if(inputs: Sequence[ValuePoint], game: QuixoGame) -> ValuePoint:
    assert len(inputs) == 3, f"Expected 3 inputs got {len(inputs)}"

    if not inputs[0].is_nil():
        return inputs[1]
    else:
        return inputs[2]


def _fun_mine(inputs: Sequence[ValuePoint], game: QuixoGame) -> ValuePoint:
    assert len(inputs) == 1, f"Expected 1 inputs got {len(inputs)}"

    if not inputs[0].is_nil() and game.is_current_player_pos(inputs[0].point):
        return inputs[0]
    else:
        return ValuePoint.NIL


def _fun_yours(inputs: Sequence[ValuePoint], game: QuixoGame) -> ValuePoint:
    assert len(inputs) == 1, f"Expected 1 inputs got {len(inputs)}"

    if not inputs[0].is_nil() and game.is_other_player_pos(inputs[0].point):
        return inputs[0]
    else:
        return ValuePoint.NIL


def _fun_open(inputs: Sequence[ValuePoint], game: QuixoGame) -> ValuePoint:
    assert len(inputs) == 1, f"Expected 1 inputs got {len(inputs)}"

    if not inputs[0].is_nil() and game.is_void_pos(inputs[0].point):
        return inputs[0]
    else:
        return ValuePoint.NIL


def _get_random_from_set(in_set: List[Function | ValuePoint], rnd: Random, to_exclude: None | Function | ValuePoint):
    if to_exclude is None:
        return rnd.choice(in_set)
    else:
        return rnd.choice([f for f in in_set if f != to_exclude])


class FunctionSet:
    _actions_set: List[Function] = [
        Function(
            name="Left",
            inputs=1,
            is_action=True
        ),
        Function(
            name="Right",
            inputs=1,
            is_action=True
        ),
        Function(
            name="Top",
            inputs=1,
            is_action=True
        ),
        Function(
            name="Bottom",
            inputs=1,
            is_action=True
        )
    ]
    _set: List[Function] = [
        Function(
            name="And",
            inputs=2,
            op=_fun_and
        ),
        Function(
            name="Or",
            inputs=2,
            op=_fun_or
        ),
        Function(
            name="If",
            inputs=3,
            op=_fun_if
        ),
        Function(
            name="Mine",
            inputs=1,
            op=_fun_mine
        ),
        Function(
            name="Yours",
            inputs=1,
            op=_fun_yours
        ),
        Function(
            name="Open",
            inputs=1,
            op=_fun_open
        ),
        *_actions_set
    ]

    @classproperty
    def set(cls) -> List[Function]:
        return cls._set

    @classproperty
    def actions_set(cls) -> List[Function]:
        return cls._actions_set

    @classmethod
    def get_random_function(cls, rnd: Random, to_exclude: Optional[Function] = None, inputs: Optional[int] = None, outputs: Optional[int] = None):
        set = cls._set
        if inputs is not None:
            set = [f for f in set if f.inputs == inputs]
        if outputs is not None:
            set = [f for f in set if f.outputs == outputs]
        return _get_random_from_set(set, rnd, to_exclude)

    @classmethod
    def get_random_functions(cls, rnd: Random, count) -> List[Function]:
        return rnd.choices(cls._set, k=count)

    @classmethod
    def get_random_action_function(cls, rnd: Random, to_exclude: Optional[Function] = None):
        return _get_random_from_set(cls._actions_set, rnd, to_exclude)
