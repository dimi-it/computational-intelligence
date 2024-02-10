from typing import Optional
import networkx as nx


class GeneticProgrammingAgent:
    def __init__(self, genome: Optional[nx.DiGraph]):
        self.genome = genome

    def print(self):
        pass

    def initialize(self):
        self.genome = nx.DiGraph()
