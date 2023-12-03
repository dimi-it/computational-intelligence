from collections.abc import Callable
import numpy as np
from population import Population
from parents_selector import ParentSelector
from survivals_selector import SurvivalSelector
from offspring_generator import OffspringGenerator
from recombinator import Recombinator
from mutator import Mutator


class PopulationBuilder:
    def __init__(self):
        # Initialization
        self.initialization_function: Callable[[], np.ndarray] | None = None
        self.population_size = 0
        self.offspring_size = 0
        # Selectors
        self.parents_selector: Callable[[np.ndarray, np.ndarray], (np.ndarray, np.ndarray)] | None = None
        self.survivals_selector: Callable[[np.ndarray, np.ndarray, np.ndarray, np.ndarray], (
        np.ndarray, np.ndarray)] | None = None
        self.is_survivals_selector_generational = False
        # Offspring generator
        self.recombinator: Callable[[np.ndarray], np.ndarray] | None = None
        self.mutator: Callable[[np.ndarray], np.ndarray] | None = None
        self.partial_offspring_generator: Callable[[np.ndarray, Callable[[np.ndarray], np.ndarray] | None, Callable[
            [np.ndarray], np.ndarray] | None], np.ndarray] | None = None
        # Fitness
        self.fitness_calculator: Callable[[np.ndarray], np.ndarray] | None = None
        # Util
        self.rng = np.random.default_rng()

    ####################
    ## INITIALIZATION ##
    ####################
    def initialize_with_genome(self, population_genome):
        def initialize_by_genome() -> np.ndarray:
            return population_genome

        self.initialization_function = initialize_by_genome
        self.population_size = population_genome.shape[0]
        return self

    def initialize_random(self, population_size, genome_len, zero_probability=0.5):
        def initialize_random_genome() -> np.ndarray:
            return self.rng.choice((True, False), (population_size, genome_len),
                                   p=(1 - zero_probability, zero_probability))

        self.initialization_function = initialize_random_genome
        self.population_size = population_size
        return self

    ######################
    ## PARENT SELECTORS ##
    ######################
    def add_parents_selector_tournament(self, tournament_size, offspring_size):
        def function(population_genome: np.ndarray, population_fitness: np.ndarray) -> (np.ndarray, np.ndarray):
            return ParentSelector.tournament_selector(tournament_size, offspring_size, population_genome,
                                                      population_fitness)

        self.parents_selector = function
        self.offspring_size = offspring_size
        return self

    def add_parents_selector_roulette_wheel(self, offspring_size):
        def function(population_genome: np.ndarray, population_fitness: np.ndarray) -> (np.ndarray, np.ndarray):
            return ParentSelector.roulette_wheel(offspring_size, population_genome, population_fitness)

        self.parents_selector = function
        self.offspring_size = offspring_size
        return self

    ########################
    ## SURVIVAL SELECTORS ##
    ########################
    def add_survivals_selector_steady_state(self):
        self.survivals_selector = SurvivalSelector.steady_state_selector
        return self

    def add_survivals_selector_generational(self):
        self.survivals_selector = SurvivalSelector.generational_selector
        self.is_survivals_selector_generational = True
        return self

    #########################
    ## OFFSPRING GENERATOR ##
    #########################
    def add_mutation_single_flip(self):
        self.mutator = Mutator.single_flip_mutation
        return self

    def add_recombination_one_point_xover(self):
        self.recombinator = Recombinator.one_point_xover
        return self

    def add_recombination_uniform_xover(self):
        self.recombinator = Recombinator.uniform_xover
        return self

    def set_mutation_sequential_to_recombination(self, probability_mutation):
        def function(parents_genome: np.ndarray, recombinator: Callable[[np.ndarray], np.ndarray] | None,
                     mutator: Callable[[np.ndarray], np.ndarray] | None) -> np.ndarray:
            return OffspringGenerator.sequential_generator(probability_mutation, parents_genome, recombinator, mutator)

        self.partial_offspring_generator = function
        return self

    def set_recombination_and_mutation_mutualexclusive(self, probability_recombination_over_mutation):
        def function(parents_genome: np.ndarray, recombinator: Callable[[np.ndarray], np.ndarray] | None,
                     mutator: Callable[[np.ndarray], np.ndarray] | None) -> np.ndarray:
            return OffspringGenerator.mutualexclusive_generator(probability_recombination_over_mutation, parents_genome,
                                                                recombinator, mutator)

        self.partial_offspring_generator = function
        return self

    #############
    ## FITNESS ##
    #############
    def add_fitness_function(self, fitness_function):
        def fitness(population_genome: np.ndarray) -> np.ndarray:
            return np.apply_along_axis(fitness_function, axis=1, arr=population_genome)

        self.fitness_calculator = fitness
        return self

    ###########
    ## BUILD ##
    ###########
    def build(self):
        assert not self.is_survivals_selector_generational or self.offspring_size >= self.population_size, "Invalid configuration, if the survival selector is generational the offspring size must be greater or equal than the population size"

        def offspring_generator(parents_genome: np.ndarray) -> np.ndarray:
            return self.partial_offspring_generator(parents_genome, self.recombinator, self.mutator)

        return Population(population_genome=self.initialization_function(), parents_selector=self.parents_selector,
                          survivals_selector=self.survivals_selector, offspring_generator=offspring_generator,
                          fitness_calculator=self.fitness_calculator)