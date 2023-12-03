from collections.abc import Callable
import numpy as np


class Recombinator:
    _rng = np.random.default_rng()

    @staticmethod
    def one_point_xover(parents_genome: np.ndarray) -> np.ndarray:
        parent_count = parents_genome.shape[0]
        assert parent_count % 2 == 0, "The number of parents for the crossover must be even"
        genome_len = parents_genome.shape[1]
        couple_count = int(parent_count / 2)
        points_of_xover = Recombinator._rng.integers(0, genome_len - 1, couple_count).reshape(couple_count, 1)
        mask_change_per_couple = np.arange(genome_len) <= points_of_xover
        return Recombinator._mask_couple_to_recombination(parents_genome, mask_change_per_couple)

    @staticmethod
    def uniform_xover(parents_genome: np.ndarray) -> np.ndarray:
        parent_count = parents_genome.shape[0]
        assert parent_count % 2 == 0, "The number of parents for the crossover must be even"
        genome_len = parents_genome.shape[1]
        couple_count = int(parent_count / 2)
        mask_change_per_couple = Recombinator._rng.choice((True, False), (couple_count, genome_len))
        return Recombinator._mask_couple_to_recombination(parents_genome, mask_change_per_couple)

    @staticmethod
    def _mask_couple_to_recombination(parents_genome, mask_change_per_couple):
        parent_count = parents_genome.shape[0]
        genome_len = parents_genome.shape[1]
        mask_change_per_parents = np.hstack((mask_change_per_couple, ~mask_change_per_couple)).reshape(-1, genome_len)
        mask = mask_change_per_parents + np.broadcast_to(np.repeat(np.arange(0, parent_count, 2), 2),
                                                         (genome_len, parent_count)).T
        return np.take_along_axis(parents_genome, mask, axis=0)