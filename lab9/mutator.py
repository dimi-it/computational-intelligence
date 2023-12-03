from collections.abc import Callable
import numpy as np


class Mutator:
    _rng = np.random.default_rng()

    @staticmethod
    def single_flip_mutation(parents_genome: np.ndarray) -> np.ndarray:
        col_id_to_change = Mutator._rng.integers(0, parents_genome.shape[1], (parents_genome.shape[0]))
        row_id_range = np.arange(parents_genome.shape[0])
        parents_genome[row_id_range, col_id_to_change] = ~parents_genome[row_id_range, col_id_to_change]
        return parents_genome