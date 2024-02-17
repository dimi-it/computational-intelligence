import math
from dataclasses import dataclass, field
from typing import List, Optional
from itertools import chain

from quixo.crossover import Crossover
from quixo.data_bags import PopulationParameters
from quixo.function_set import FunctionSet
from quixo.game import Player
from quixo.gp_player import GeneticProgrammingPlayer
from quixo.individual import Individual
from quixo.initializer import Initializer
from quixo.mutation import Mutation
from quixo.my_random_player import MyRandomPlayer
from quixo.quixo_game import QuixoGame
from quixo.terminal_set import TerminalSet


class Population:
    def __init__(self, population_param: PopulationParameters, initial_population: Optional[List[Individual]] = None):
        self._population_param = population_param
        self._individuals = [] if initial_population is None else initial_population
        self._selected_parents = []
        self._bests = []
        self._generation = 0

    def __str__(self):
        return f"""Generation: {self._generation}
Individuals: {len(self._individuals)}"""

    @property
    def individuals(self) -> List[Individual]:
        return self._individuals

    @property
    def bests(self) -> List[Individual]:
        return self._bests

    def initialize(self):
        initializer = Initializer(self._population_param)
        self._individuals = initializer.initialize_population()

    def _fitnessless_selection(self) -> List[Individual]:
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
        return selected

    def _interactive_selection_against_random(self, individuals: List[individuals]):
        selected = []
        for ind in individuals:
            tournament_individuals = [
                ind,
                Individual.generate_random_individual(self._population_param.rnd.randint(-100000000, 0)),
                Individual.generate_random_individual(self._population_param.rnd.randint(-100000000, 0)),
                ind
            ]
            winner = self._tournament(tournament_individuals, override_depth=2)
            # print(f"W{repr(winner)}")
            if winner == ind:
                selected.append(winner)
        print(f"Selected(interactive): {len(selected)}")
        return selected

    def _tournament(self, individuals: List[Individual], override_depth: Optional[int] = None) -> Individual:
        # print(individuals)
        this_level_individuals = individuals
        next_level_individuals = []
        depth = self._population_param.tournament_depth if override_depth is None else override_depth
        for d in range(depth):
            for i in range(0, len(this_level_individuals), 2):
                i1 = this_level_individuals[i]
                i2 = this_level_individuals[i + 1]
                if i1 == i2:
                    next_level_individuals.append(i1)
                else:
                    next_level_individuals.append(this_level_individuals[i + self._match(i1, i2)])
            this_level_individuals = next_level_individuals
            next_level_individuals = []
        assert len(this_level_individuals) == 1, f"Expected only one individual left, got {len(this_level_individuals)}"
        return this_level_individuals[0]

    def _match(self, i1: Individual, i2: Individual) -> int:
        p1 = GeneticProgrammingPlayer(i1, enable_random_move=self._population_param.player_param.enable_random_move,
                                      loop_avoidance_limit=self._population_param.player_param.loop_avoidance_limit)
        p2 = GeneticProgrammingPlayer(i2, enable_random_move=self._population_param.player_param.enable_random_move,
                                      loop_avoidance_limit=self._population_param.player_param.loop_avoidance_limit)
        return Population._match_players(p1, p2)

    # def _match_random(self, i: Individual, is_first: bool = True) -> int:
    #     p1 = GeneticProgrammingPlayer(i, enable_random_move=self._population_param.player_param.enable_random_move,
    #                                   loop_avoidance_limit=self._population_param.player_param.loop_avoidance_limit)
    #     p2 = MyRandomPlayer(self._population_param.rnd.randint(1,10000))
    ################ check return order point
    #     if is_first:
    #         return Population._match_players(p1, p2)
    #     else:
    #         return Population._match_players(p2, p1)

    @staticmethod
    def _match_players(p1: Player, p2: Player) -> int:
        game = QuixoGame()
        w = game.play(p1, p2)
        # print(f"p1{repr(p1.brain)}, p2{repr(p2.brain)}")
        # print(f"W: {w}")
        return w

    def recombination(self, selected_parents: List[individuals]) -> List[Individual]:
        count = 0
        id_offset = (self._generation + 1) * 1000
        childs = []
        mutations = self._population_param.rnd.choices([True, False],
                                                       weights=[self._population_param.mutation_probability,
                                                                self._population_param.mutation_probability],
                                                       k=self._population_param.population_size)

        crossover_count = int(self._population_param.crossover_probability * self._population_param.population_size)
        crossover_parents = self._population_param.rnd.choices(selected_parents, k=crossover_count * 2)
        for i in range(crossover_count):
            child = Crossover.one_node_xover(crossover_parents[2 * i], crossover_parents[2 * i + 1],
                                             self._population_param, count + id_offset)
            if mutations[count]:
                child = Mutation.one_node_mutation(child, self._population_param, child.id)
            childs.append(child)
            count += 1

        reproduction_count = self._population_param.population_size - crossover_count
        reproduction_parents = self._population_param.rnd.choices(selected_parents, k=reproduction_count)
        for i in range(reproduction_count):
            child = Individual(count + id_offset, reproduction_parents[i].genome,
                               parents_id=[reproduction_parents[i].id])
            if mutations[count]:
                child = Mutation.one_node_mutation(child, self._population_param, child.id)
            childs.append(child)
            count += 1
        return childs

    def proceed_generation(self):
        print(self)
        self._selected_parents = self._fitnessless_selection()
        self._selected_parents = self._interactive_selection_against_random(self._selected_parents)
        childs = self.recombination(self._selected_parents)
        self._individuals = childs
        self._generation += 1
        # for i in self._individuals:
        #     i.print_graph()

    def proceed_x_generation(self, x):
        for _ in range(x):
            self.proceed_generation()
