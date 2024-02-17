from functools import cached_property
from random import Random
from typing import Optional, List, Sequence
import networkx as nx
import matplotlib.pyplot as plt
import pickle

from quixo.decorator import classproperty
from quixo.node import Node


# from networkx.drawing.nx_agraph import write_dot, graphviz_layout

class Individual:
    def __init__(self, id: Optional[int] = None, genome: Optional[nx.DiGraph] = None, parents_id: Optional[Sequence[int]] = None):
        self._genome = genome
        self._id = id
        self._parenst_id = parents_id
        self._fitness = None

    def __str__(self):
        return f"Individual {self._id}, {self._genome.adj}"

    def __repr__(self):
        return f"I_{self._id}"

    def __hash__(self):
        return hash(self.id + hash(self.genome_adj_str))

    @property
    def genome(self) -> nx.DiGraph:
        assert self._genome is not None, "Genome not defined"
        return self._genome

    @property
    def id(self) -> int:
        assert self._id is not None, "Id not defined"
        return self._id

    @property
    def fitness(self) -> float:
        return self._fitness

    @fitness.setter
    def fitness(self, value: float):
        self._fitness = value

    @cached_property
    def genome_adj_str(self):
        return str(self._genome.adj)

    @cached_property
    def traversal_list(self) -> List[Node]:
        assert self._genome is not None, "Genome not defined"
        return list(nx.dfs_preorder_nodes(self._genome, source=list(self._genome.nodes)[0]))

    @cached_property
    def random_seed(self):
        return str(self.id) + self.genome_adj_str

    @staticmethod
    def generate_random_individual(id: int) -> 'Individual':
        return Individual(id, nx.DiGraph())

    @staticmethod
    def generate_from_file(filename: str) -> 'Individual':
        genome = pickle.load(open(filename, 'rb'))
        return Individual(Random(filename).randint(-100000000, 0), genome)

    def save_to_file(self, filename: str):
        pickle.dump(self._genome, open(filename, 'wb'))

    def print_graph(self):
        # pos = graphviz_layout(self._genome, prog='dot')
        nx.draw(self._genome, pos=nx.planar_layout(self._genome), with_labels=True, arrows=True,
                node_color=['blue' if n.is_terminal else 'red' for n in self._genome], alpha=0.5)
        plt.show()
