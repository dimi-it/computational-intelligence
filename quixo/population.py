from dataclasses import dataclass, field

from quixo.data_bags import PopulationParameters
from quixo.function_set import FunctionSet
from quixo.terminal_set import TerminalSet


class Population:
    def __init__(self, population_param: PopulationParameters):
        self.population_param = population_param

    def initialize(self, ):

