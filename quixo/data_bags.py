from dataclasses import dataclass, field
from random import Random
from typing import Set, List, Callable

from quixo.function import Function
from quixo.function_set import FunctionSet
from quixo.terminal_set import TerminalSet
from quixo.value_point import ValuePoint


@dataclass
class InitParameters:
    """
    Initialization parameters
    """
    use_grow: bool = field(default=True)
    use_full: bool = field(default=True)
    use_different_depth: bool = field(default=True)
    extend_probability_fun: Callable[[int], float] = field(default=lambda depth: 1 - (1 / depth))


@dataclass
class AgentParameters:
    """
    Agent specific parameters
    """
    max_depth: int


@dataclass
class PlayerParameters:
    """
    Player specific parameters
    """
    enable_random_move: bool = field(default=True)
    loop_avoidance_limit: int = field(default=5)


@dataclass
class PopulationParameters:
    """
    Population parameters
    """
    agent_param: AgentParameters
    init_param: InitParameters
    player_param: PlayerParameters
    population_size: int
    tournament_depth: int
    selection_size: int
    rnd: Random = field(default=Random(123456))
    keep_best: bool = field(default=True)
    crossover_probability: float = field(default=.8)
    mutation_probability: float = field(default=.5)
    round_against_random: int = field(default=100)

    @property
    def random_bool(self) -> bool:
        return self.rnd.choice([True, False])
