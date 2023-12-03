from collections.abc import Callable
import numpy as np


class OffspringGenerator:
    @staticmethod
    def sequential_generator(probability_mutation: float, parents_genome: np.ndarray,
                             recombinator: Callable[[np.ndarray], np.ndarray] | None,
                             mutator: Callable[[np.ndarray], np.ndarray] | None) -> np.ndarray:
        _ = recombinator(parents_genome)
        mutate_until_index = int(parents_genome.shape[0] * probability_mutation)
        _ = mutator(parents_genome[:mutate_until_index, :])
        return parents_genome

    @staticmethod
    def mutualexclusive_generator(probability_recombination_over_mutation: float, parents_genome: np.ndarray,
                                  recombinator: Callable[[np.ndarray], np.ndarray] | None,
                                  mutator: Callable[[np.ndarray], np.ndarray] | None) -> np.ndarray:
        recombinate_until_index = int(parents_genome.shape[0] * probability_recombination_over_mutation)
        recombinate_until_index += 0 if recombinate_until_index % 2 == 0 else 1
        _ = recombinator(parents_genome[:recombinate_until_index, :])
        _ = mutator(parents_genome[recombinate_until_index:, :])
        return parents_genome