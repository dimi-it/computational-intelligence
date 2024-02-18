import concurrent.futures
import math
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import List, Optional, Callable
from itertools import chain
from tqdm import tqdm
from multiprocessing.pool import ThreadPool

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
        """
        Return individuals
        """
        return self._individuals

    @property
    def bests(self) -> List[Individual]:
        """
        Return bests across generations
        """
        return self._bests

    @property
    def selected_parents(self) -> List[Individual]:
        """
        Return selected parent of current generation
        """
        return self._selected_parents

    def initialize(self):
        """
        Initialize population
        """
        initializer = Initializer(self._population_param)
        self._individuals = initializer.initialize_population()

    def _fitness_evaluation_no_coevolution(self, individuals: List[individuals]) -> List[Individual]:
        """
        Evaluate fitness against random players
        """
        fitnesses = []
        selected = []
        randoms = [Individual.generate_random_individual(self._population_param.rnd.randint(-100000000, 0)) for _ in
                   range(self._population_param.round_against_random)]

        for individual in individuals:
            flag = True
            count = 0
            for r in randoms:
                if flag:
                    w = self._match(individual, r)
                    if w == 0:
                        count += 1
                else:
                    w = self._match(r, individual)
                    if w == 1:
                        count += 1
                flag = not flag
            fitness = count / self._population_param.round_against_random
            fitnesses.append(fitness)
            individual.fitness = fitness
        print(f"Ind avg: {sum([i.fitness for i in individuals]) / self._population_param.population_size}")
        selected = self._fitness_selection_roulette(individuals, fitnesses)
        print(f"Sel avg: {sum([i.fitness for i in selected]) / self._population_param.selection_size}")
        return selected

    def _fitness_evaluation_no_coevolution_mixed(self, individuals: List[individuals]) -> List[Individual]:
        """
        Evaluate fitness against random and pre-trained players
        """
        fitnesses = []
        selected = []
        pre_trained_count = 10
        randoms = [Individual.generate_random_individual(self._population_param.rnd.randint(-100000000, 0)) for _ in
                   range(self._population_param.round_against_random)]
        pre_trained = [Individual.generate_from_file(f"dev_stuff/bests/run_1/{f}.graph") for f in range(pre_trained_count)]
        pre_trained = list(chain.from_iterable((x, x) for x in pre_trained))
        adversaries = [*randoms, *pre_trained]
        for individual in individuals:
            flag = True
            count = 0
            for a in adversaries:
                if flag:
                    w = self._match(individual, a)
                    if w == 0:
                        count += 1
                else:
                    w = self._match(a, individual)
                    if w == 1:
                        count += 1
                flag = not flag
            fitness = count / len(adversaries)
            fitnesses.append(fitness)
            individual.fitness = fitness
        print(f"Ind avg: {sum([i.fitness for i in individuals]) / self._population_param.population_size}")
        selected = self._fitness_selection_roulette(individuals, fitnesses)
        print(f"Sel avg: {sum([i.fitness for i in selected]) / self._population_param.selection_size}")
        return selected

    def _fitness_selection_roulette(self, individuals: List[individuals], fitnesses: List[float]) -> List[Individual]:
        """
        Selection based on the roulette wheel approach
        """
        selected = self._population_param.rnd.choices(individuals, weights=fitnesses,
                                                      k=self._population_param.selection_size)
        return selected

    def _fitness_selection_tournament(self, individuals: List[individuals], fitnesses: List[float]) -> List[Individual]:
        """
        Selection based on the tournament approach
        """
        selected = []
        for i in range(self._population_param.selection_size):
            tournament_individuals = self._population_param.rnd.choices(individuals,
                                                                        k=2 ** self._population_param.tournament_depth)
            selected.append(self._tournament(tournament_individuals, self._tournament_fitness))
        return selected

    def _fitnessless_selection_coevolution(self, individuals: List[individuals]) -> List[Individual]:
        """
        Coevolution selection, tournament based, no fitness
        """
        selected = []
        results = {}
        tournament_size = 2 ** self._population_param.tournament_depth
        for i in range(self._population_param.selection_size):
            if tournament_size < self._population_param.population_size:
                tournament_individuals = self._population_param.rnd.sample(individuals, k=tournament_size)
            else:
                tournament_individuals = self._population_param.rnd.choices(individuals, k=tournament_size)
            # print(f"Tournament {i}: {tournament_individuals}")
            winner = self._tournament(tournament_individuals, self._tournament_match)
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
        """
        Interactive selection against random player
        """
        selected = []
        for ind in individuals:
            tournament_individuals = [
                ind,
                Individual.generate_random_individual(self._population_param.rnd.randint(-100000000, 0)),
                Individual.generate_random_individual(self._population_param.rnd.randint(-100000000, 0)),
                ind
            ]
            winner = self._tournament(tournament_individuals, self._tournament_match, override_depth=2)
            # print(f"W{repr(winner)}")
            if winner == ind:
                selected.append(winner)
        print(f"Selected(interactive): {len(selected)}")
        return selected

    def _tournament(self, individuals: List[Individual], tournament_fun: Callable[[int, Individual, Individual], int],
                    override_depth: Optional[int] = None, ) -> Individual:
        """
        TOurnament
        """
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

    def _tournament_match(self, id: int, i1: Individual, i2: Individual) -> int:
        """
        Tournament based on match
        """
        return id + self._match(i1, i2)

    def _tournament_fitness(self, id: int, i1: Individual, i2: Individual) -> int:
        """
        Tournament based on fitness
        """
        if i1.fitness > i2.fitness:
            return id + 0
        else:
            return id + 1

    def _match(self, i1: Individual, i2: Individual) -> int:
        """
        Match between individuals
        """
        p1 = GeneticProgrammingPlayer(i1, enable_random_move=self._population_param.player_param.enable_random_move,
                                      loop_avoidance_limit=self._population_param.player_param.loop_avoidance_limit)
        p2 = GeneticProgrammingPlayer(i2, enable_random_move=self._population_param.player_param.enable_random_move,
                                      loop_avoidance_limit=self._population_param.player_param.loop_avoidance_limit)
        return Population._match_players(p1, p2)

    @staticmethod
    def _match_players(p1: Player, p2: Player) -> int:
        """
        Match between players
        """
        game = QuixoGame()
        w = game.play(p1, p2)
        # print(f"p1{repr(p1.brain)}, p2{repr(p2.brain)}")
        # print(f"W: {w}")
        return w

    def recombination(self, selected_parents: List[individuals]) -> List[Individual]:
        """
        Recombination process, crossover and reproduction, then mutation
        """
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

    def _set_best(self, individuals: List[Individual]):
        best = max(individuals, key=lambda ind: ind.fitness)
        self._bests.append(best)
        print(f"Best fitness: {best.fitness}")

    def proceed_generation(self):
        """
        Make a generation
        """
        print(self)
        # self._selected_parents = self._fitnessless_selection_coevolution()
        # self._selected_parents = self._interactive_selection_against_random(self._individuals)
        # self._selected_parents = self._fitnessless_selection_coevolution(self._selected_parents)
        self._selected_parents = self._fitness_evaluation_no_coevolution(self.individuals)
        # self._selected_parents = self._fitness_evaluation_no_coevolution_mixed(self.individuals)
        self._set_best(self.individuals)
        childs = self.recombination(self._selected_parents)
        self._individuals = childs
        self._generation += 1
        # for i in self._individuals:
        #     i.print_graph()

    def proceed_x_generation(self, x):
        """
        Proceed for x generations
        """
        for _ in tqdm(range(x)):
            self.proceed_generation()
