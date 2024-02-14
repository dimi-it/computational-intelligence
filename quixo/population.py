from dataclasses import dataclass, field
from typing import List

from quixo.data_bags import PopulationParameters
from quixo.function_set import FunctionSet
from quixo.individual import Individual
from quixo.initializer import Initializer
from quixo.terminal_set import TerminalSet


class Population:
    def __init__(self, population_param: PopulationParameters):
        self.population_param = population_param
        self._individuals = []
        self._generation = 0

    def __str__(self):
        return f"""Generation: {self._generation}
        Individuals: {len(self._individuals)}"""

    @property
    def individuals(self) -> List[Individual]:
        return self._individuals

    def initialize(self):
        initializer = Initializer(self.population_param)
        self._individuals = initializer.initialize_population()

