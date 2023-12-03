from collections.abc import Callable
import numpy as np


class SurvivalSelector:
    @staticmethod
    def steady_state_selector(oldgen_genome: np.ndarray, oldgen_fitness: np.ndarray, offspring_genome: np.ndarray,
                              offspring_fitness: np.ndarray) -> (np.ndarray, np.ndarray):
        population_size = oldgen_genome.shape[0]
        population_genome = np.vstack((oldgen_genome, offspring_genome))
        population_fitness = np.concatenate((oldgen_fitness, offspring_fitness))
        sorting_indices = population_fitness.argsort()[::-1]
        population_genome = population_genome[sorting_indices]
        population_fitness = population_fitness[sorting_indices]
        return population_genome[:population_size, :], population_fitness[:population_size]

    @staticmethod
    def generational_selector(oldgen_genome: np.ndarray, oldgen_fitness: np.ndarray, offspring_genome: np.ndarray,
                              offspring_fitness: np.ndarray) -> (np.ndarray, np.ndarray):
        population_size = oldgen_genome.shape[0]
        sorting_indices = offspring_fitness.argsort()[::-1]
        population_genome = offspring_genome[sorting_indices]
        population_fitness = offspring_fitness[sorting_indices]
        return population_genome[:population_size, :], population_fitness[:population_size]