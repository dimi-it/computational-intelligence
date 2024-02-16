import math
from dataclasses import dataclass, field
from typing import List

from quixo.data_bags import PopulationParameters
from quixo.function_set import FunctionSet
from quixo.gp_player import GeneticProgrammingPlayer
from quixo.individual import Individual
from quixo.initializer import Initializer
from quixo.quixo_game import QuixoGame
from quixo.terminal_set import TerminalSet


class Population:
    def __init__(self, population_param: PopulationParameters):
        self._population_param = population_param
        self._individuals = []
        self._bests = []
        self._generation = 0

    def __str__(self):
        return f"""Generation: {self._generation}
        Individuals: {len(self._individuals)}"""

    @property
    def individuals(self) -> List[Individual]:
        return self._individuals

    def initialize(self):
        initializer = Initializer(self._population_param)
        self._individuals = initializer.initialize_population()

    def selection(self):
        selected = []
        results = {}
        tournament_size = 2 ** self._population_param.tournament_depth
        for i in range(self._population_param.selection_size):
            if tournament_size < self._population_param.population_size:
                tournament_individuals = self._population_param.rnd.sample(self.individuals, k=tournament_size)
            else:
                tournament_individuals = self._population_param.rnd.choices(self.individuals, k=tournament_size)
            # print(f"Tournament {i}: {tournament_individuals}")
            winner = self._tournament(tournament_individuals)
            if winner in results:
                results[winner] += 1
            else:
                results[winner] = 1
            selected.append(winner)
            # print(f"Tournament {i} WINNER: {repr(winner)}")
        best_points = max(results.values())
        best = self._population_param.rnd.choice([k for k, v in results.items() if v == best_points])
        # print(f"Best: {repr(best)}")
        self._bests.append(best)
        # print(f"Selected: {selected}")

    def _tournament(self, individuals: List[Individual]) -> Individual:
        this_level_individuals = individuals
        next_level_individuals = []
        for d in range(self._population_param.tournament_depth):
            for i in range(0, len(this_level_individuals), 2):
                next_level_individuals.append(this_level_individuals[
                                                  i + self._match(this_level_individuals[i],
                                                                  this_level_individuals[i + 1])
                                                  ])
            this_level_individuals = next_level_individuals
            next_level_individuals = []
        assert len(this_level_individuals) == 1, f"Expected only one individual left, got {len(this_level_individuals)}"
        return this_level_individuals[0]

    def _match(self, i1: Individual, i2: Individual) -> int:
        game = QuixoGame()
        p1 = GeneticProgrammingPlayer(i1, enable_random_move=self._population_param.player_param.enable_random_move,
                                      loop_avoidance_limit=self._population_param.player_param.loop_avoidance_limit)
        p2 = GeneticProgrammingPlayer(i2, enable_random_move=self._population_param.player_param.enable_random_move,
                                      loop_avoidance_limit=self._population_param.player_param.loop_avoidance_limit)
        w = game.play(p1, p2)
        # print(f"W: {w}")
        return w
