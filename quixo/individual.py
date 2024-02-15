from functools import cached_property
from typing import Optional, List
import networkx as nx
import matplotlib.pyplot as plt

from quixo.node import Node


# from networkx.drawing.nx_agraph import write_dot, graphviz_layout

class Individual:
    def __init__(self, id: Optional[int] = None, genome: Optional[nx.DiGraph] = None):
        self._genome = genome
        self._id = id

    def __str__(self):
        return f"Individual {self._id}, {self._genome.adj}"

    def __hash__(self):
        return hash(self.genome_adj_str)

    @property
    def genome(self) -> nx.DiGraph:
        assert self._genome is not None, "Genome not defined"
        return self._genome

    @property
    def id(self) -> int:
        assert self._id is not None, "Id not defined"
        return self._id

    @cached_property
    def genome_adj_str(self):
        return str(self._genome.adj)

    @cached_property
    def traversal_list(self) -> List[Node]:
        assert self._genome is not None, "Genome not defined"
        return list(nx.dfs_preorder_nodes(self._genome, source=list(self._genome.nodes)[0]))

    def print_graph(self):
        # pos = graphviz_layout(self._genome, prog='dot')
        nx.draw(self._genome, pos=nx.planar_layout(self._genome), with_labels=True, arrows=True,
                node_color=['blue' if n.is_terminal else 'red' for n in self._genome], alpha=0.5)
        plt.show()