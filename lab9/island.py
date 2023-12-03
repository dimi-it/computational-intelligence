from collections.abc import Callable, Sequence
import numpy as np
from population_builder import PopulationBuilder
from population import Population
from matplotlib import pyplot as plt



class Island:
    # Builders must be without initializations
    def __init__(self, population_size, genome_len, builders: Sequence[PopulationBuilder], repeat_builder=1, ):
        self._builders: Sequence[PopulationBuilder] = [b for _ in range(repeat_builder) for b in builders]
        self._populations = [b.initialize_random(population_size, genome_len).build() for b in self._builders]
        self._population_size = population_size
        self._rng = np.random.default_rng()
        self._history_fitness = []

    @property
    def max_population(self):
        return max(self._populations, key=lambda p: p.max_fitness)

    @property
    def max_fitness(self):
        return self.max_population.max_fitness

    def log_history_fitness(self):
        history = np.array(self._history_fitness)
        plt.figure(figsize=(14, 4))
        plt.plot(history[:, 0], history[:, 1], marker=".")

    def run(self, epochs, generation_per_epoch=100, migrants=None, log_data=False):
        migrants = migrants if migrants is not None else int(self._population_size / 10)
        assert migrants != 0, "There are no migrants"
        assert migrants < self._population_size / 2, "Invalid configuration, is not possible a number of migrant greater than half of the population size"
        for epoch in range(epochs):
            self._run_epoch(generation_per_epoch, log_data)
            if log_data:
                self._log_epoch(epoch)
            self._history_fitness.append((epoch, self.max_fitness))
            self._migrate(migrants)

    def _run_epoch(self, generations, log_data):
        for population in self._populations:
            population.run_for_generations_or_until_no_upgrades(generations, log_data=log_data)

    def _migrate(self, migrants):
        permutation = self._rng.permutation(len(self._populations))
        new_populations_genomes = []
        for i in range(len(self._populations)):
            new_genome = self._populations[i].genome
            new_genome[-migrants:, :] = self._populations[permutation[i]].genome[:migrants, ]
            new_populations_genomes.append(new_genome)
        self._populations = [b.initialize_with_genome(new_populations_genomes[i]).build() for i, b in
                             enumerate(self._builders)]

    def _log_epoch(self, epoch):
        print(f"####EPOCH {epoch}####")
        for i, population in enumerate(self._populations):
            print(f"Population #{i}\n{population}")