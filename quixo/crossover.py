from copy import deepcopy
from random import Random
from typing import Optional

import networkx as nx
from networkx.classes.reportviews import OutEdgeView

from quixo.data_bags import PopulationParameters
from quixo.individual import Individual
from quixo.graph import GraphExtended
from quixo.node import Node


class Crossover:
    @staticmethod
    def one_node_xover(p1: Individual, p2: Individual,
                       population_param: PopulationParameters, id: Optional[int] = None) -> Individual:
        p1_genome = deepcopy(p1.genome)
        p2_genome = deepcopy(p2.genome)
        p1_edge = GraphExtended.choice_edge(p1_genome, population_param.rnd)
        p1_parent_edges = list(p1_genome.out_edges(p1_edge[0]))
        p1_root = list(p1_genome.nodes)[0]
        p2_edge = GraphExtended.choice_edge(p2_genome, population_param.rnd)
        child_genome: nx.DiGraph = nx.compose(p1_genome, p2_genome)
        child_genome.remove_edges_from(p1_parent_edges)
        for edge in p1_parent_edges:
            if edge == p1_edge:
                child_genome.add_edge(p1_edge[0], p2_edge[1])
            else:
                child_genome.add_edge(edge[0], edge[1])
        child_genome.remove_edge(p2_edge[0], p2_edge[1])
        GraphExtended.remove_unconnected(child_genome, p1_root)
        GraphExtended.reidentify_nodes(child_genome, p1_root)
        return Individual(id, child_genome, parents_id=[p1.id, p2.id])
