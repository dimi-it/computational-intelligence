from collections.abc import Callable
import numpy as np
from matplotlib import pyplot as plt


class Population:
    def __init__(self,
                 population_genome: np.ndarray,
                 parents_selector: Callable[[np.ndarray, np.ndarray], (np.ndarray, np.ndarray)],
                 survivals_selector: Callable[
                     [np.ndarray, np.ndarray, np.ndarray, np.ndarray], (np.ndarray, np.ndarray)],
                 offspring_generator: Callable[[np.ndarray], np.ndarray],
                 fitness_calculator: Callable[[np.ndarray], np.ndarray]):

        self._population_genome = population_genome
        self._parents_selector = parents_selector
        self._survivals_selector = survivals_selector
        self._offspring_generator = offspring_generator
        self._fitness_calculator = fitness_calculator
        self._population_fitness = self._fitness_calculator(population_genome)
        sorting_indices = self._population_fitness.argsort()[::-1]
        self._population_genome = self._population_genome[sorting_indices]
        self._population_fitness = self._population_fitness[sorting_indices]
        self._generations_ran = 0
        self._history_fitness = [(0, self.max_fitness), ]

    def __str__(self):
        return f"""Generation: {self._generations_ran}
Max fitness: {self.max_fitness}"""

    def log_data(self):
        print(self)
        print(f"Genome\n{self._population_genome}")
        print(f"Fitness\n{self._population_fitness}")

    @property
    def genome(self):
        return self._population_genome

    @property
    def fitness(self):
        return self._population_fitness

    @property
    def generations_ran(self):
        return self._generations_ran

    @property
    def max_fitness(self):
        return self._population_fitness[0]

    @property
    def history_fitness(self):
        return self._history_fitness

    def log_history_fitness(self):
        history = np.array(self._history_fitness)
        print(history)
        plt.figure(figsize=(14, 4))
        plt.plot(history[:, 0], history[:, 1], marker=".")

    def run_generation(self):
        self._generations_ran += 1
        parents_genome, parents_fitness = self._parents_selector(self._population_genome, self._population_fitness)
        offspring_genome = self._offspring_generator(parents_genome)
        offspring_fitness = self._fitness_calculator(offspring_genome)
        self._population_genome, self._population_fitness = self._survivals_selector(self._population_genome,
                                                                                     self._population_fitness,
                                                                                     offspring_genome,
                                                                                     offspring_fitness)
        self._history_fitness.append((self._generations_ran, self.max_fitness))

    def run_for_generations(self, n_generations, log_data=False):
        for _ in range(n_generations):
            self.run_generation()
            if log_data:
                self.log_data()

    def run_for_generations_or_until_no_upgrades(self, n_generations, n_generations_without_upgrade= None, log_data=False):
        n_generations_without_upgrade = n_generations_without_upgrade if n_generations_without_upgrade is not None else int(n_generations/4)
        max_fit = 0
        gen_without_upgrade = 0
        for i in range(n_generations):
            if gen_without_upgrade > n_generations_without_upgrade:
                break
            self.run_generation()
            if max_fit < self.max_fitness:
                max_fit = self.max_fitness
                gen_without_upgrade = 0
            else:
                gen_without_upgrade += 1
            if log_data:
                self.log_data()
