from typing import Optional
import networkx as nx
import matplotlib.pyplot as plt


# from networkx.drawing.nx_agraph import write_dot, graphviz_layout

class GeneticProgrammingAgent:
    def __init__(self, genome: Optional[nx.DiGraph]):
        self._genome = genome

    @property
    def genome(self) -> nx.DiGraph:
        assert self._genome is not None, "Genome not defined"
        return self._genome

    def print_graph(self):
        # pos = graphviz_layout(self._genome, prog='dot')
        nx.draw(self._genome, pos=nx.spring_layout(self._genome), with_labels=True, arrows=True,
                node_color=['blue' if n.is_terminal else 'red' for n in self._genome], alpha=0.5)
        plt.show()
