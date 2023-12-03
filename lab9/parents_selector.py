from collections.abc import Callable
import numpy as np


class ParentSelector:
    _rng = np.random.default_rng()

    @staticmethod
    def tournament_selector(tournament_size: int, offspring_size: int, population_genome: np.ndarray,
                            population_fitness: np.ndarray) -> (np.ndarray, np.ndarray):
        pool = ParentSelector._rng.integers(0, population_fitness.shape[0], (offspring_size, tournament_size))
        fitpool = population_fitness[pool]
        fitpool_sorted_indices = np.argsort(fitpool, axis=1)
        parents_indices = np.take_along_axis(pool, fitpool_sorted_indices, axis=1)[:, -1]
        return population_genome[parents_indices, :], population_fitness[parents_indices]

    @staticmethod
    def roulette_wheel(offspring_size: int, population_genome: np.ndarray, population_fitness: np.ndarray) -> (
    np.ndarray, np.ndarray):
        # TODO
        pass