from copy import deepcopy
from typing import Optional

from quixo.data_bags import PopulationParameters
from quixo.function_set import FunctionSet
from quixo.individual import Individual
from quixo.graph import GraphExtended
from quixo.node import Node
from quixo.terminal_set import TerminalSet


class Mutation:
    @staticmethod
    def one_node_mutation(p: Individual,
                          population_param: PopulationParameters, id: Optional[int] = None) -> Individual:
        """
        Mutate a random node of the individual genome, changing it with a similar one
        """
        p_genome = deepcopy(p.genome)
        p_edge = GraphExtended.choice_edge(p_genome, population_param.rnd)
        p_root = list(p_genome.nodes)[0]
        node = p_edge[1]
        # print(node)
        p_parent_edges = list(p_genome.out_edges(p_edge[0]))
        p_node_edges = list(p_genome.out_edges(node))
        if node.is_terminal:
            new_node = Node(node.id, TerminalSet.get_random_terminal(population_param.rnd, to_exclude=node))
        else:
            new_node = Node(node.id,
                            FunctionSet.get_random_function(population_param.rnd, to_exclude=node,
                                                            inputs=node.function.inputs, outputs=node.function.outputs)
                            if node != p_root else
                            FunctionSet.get_random_action_function(population_param.rnd, to_exclude=node)
                            )
        # print(new_node)
        p_genome.remove_node(node)
        p_genome.add_node(new_node)
        for edge in p_parent_edges:
            if edge[1] == node:
                p_genome.add_edge(edge[0], new_node)
            else:
                p_genome.add_edge(edge[0], edge[1])
        for edge in p_node_edges:
            p_genome.add_edge(new_node, edge[1])
        return Individual(id, p_genome, parents_id=[p.id])
