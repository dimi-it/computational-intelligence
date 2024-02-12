from dataclasses import dataclass, field
from random import Random
from typing import Set, List, Callable

from quixo.function import Function
from quixo.function_set import FunctionSet
from quixo.terminal_set import TerminalSet
from quixo.value import ValuePoint


@dataclass
class InitParameters:
    use_grow: bool = field(default=True)
    use_full: bool = field(default=True)
    use_different_depth: bool = field(default=True)
    extend_probability_fun: Callable[[int], float] = field(default=lambda depth: 1 - (1 / depth))


@dataclass
class AgentParameters:
    max_depth: int


@dataclass
class PopulationParameters:
    agent_param: AgentParameters
    init_param: InitParameters
    population_size: int
    rnd: Random = field(default=Random(123456))

    @property
    def random_bool(self) -> bool:
        return self.rnd.choice([True, False])
