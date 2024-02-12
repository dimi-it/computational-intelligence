import math
from typing import Sequence, List

import networkx as nx

from quixo.data_bags import InitParameters, AgentParameters, PopulationParameters
from quixo.function import Function
from quixo.function_set import FunctionSet
from quixo.gp_agent import GeneticProgrammingAgent
from quixo.node import Node
from quixo.terminal_set import TerminalSet
from quixo.value import ValuePoint


class Initializer:
    def __init__(self, population_param: PopulationParameters):
        self._population_param = population_param

    def initialize_population(self) -> Sequence[GeneticProgrammingAgent]:
        assert self._population_param.init_param.use_grow or self._population_param.init_param.use_full, "No initialization method defined(use grow, full or both)"

        usable_depth = self._population_param.agent_param.max_depth - 1
        if self._population_param.init_param.use_different_depth:
            individuals_max_per_depth = math.ceil(self._population_param.population_size / usable_depth)
            surplus = (usable_depth * individuals_max_per_depth) - self._population_param.population_size - 1
            individuals_per_depth = [individuals_max_per_depth if i > surplus else individuals_max_per_depth - 1 for i
                                     in range(usable_depth)]
            depths = [2 + i for i in range(usable_depth)]
            individuals_and_depth = zip(individuals_per_depth, depths)
        else:
            individuals_and_depth = [
                (self._population_param.population_size, self._population_param.agent_param.max_depth)]

        use_both_method = self._population_param.init_param.use_grow and self._population_param.init_param.use_full
        is_grow = self._population_param.init_param.use_grow
        genomes = []
        for individuals, depth in individuals_and_depth:
            for _ in range(individuals):
                if use_both_method:
                    is_grow = not is_grow
                if is_grow:
                    genomes.append(GeneticProgrammingAgent(self._create_tree(depth, not is_grow)))
                else:
                    genomes.append(GeneticProgrammingAgent(self._create_tree(depth, not is_grow)))

        assert len(genomes) == self._population_param.population_size, f"Something went wrong, generated {len(genomes)} individuals instead of {self._population_param.population_size}"
        return genomes

    def _create_tree(self, depth: int, is_full: bool) -> nx.DiGraph:
        def _add_node_to_graph(graph: nx.DiGraph, previous_layer_nodes: List[Node], in_layer_nodes: List[Node], ):
            in_layer_count = 0
            for p_n in previous_layer_nodes:
                for _ in range(p_n.function.inputs):
                    node_to_add = in_layer_nodes[in_layer_count]
                    graph.add_edge(p_n, node_to_add)
                    in_layer_count += 1

        extend_prob = self._population_param.init_param.extend_probability_fun(depth)
        node_count = 0
        graph = nx.DiGraph()
        start_node = Node(node_count, FunctionSet.get_random_action_function(self._population_param.rnd))
        graph.add_node(start_node)
        previous_layer_nodes = [start_node]
        node_count += 1
        for d in range(1, depth):
            previous_layer_inputs_count = sum(node.function.inputs for node in previous_layer_nodes)
            if is_full:
                previous_layer_inputs = [True for _ in range(previous_layer_inputs_count)]
            else:
                previous_layer_inputs = self._population_param.rnd.choices([True, False], [extend_prob, 1 - extend_prob],
                                                                           k=previous_layer_inputs_count)

            in_layer_nodes = [Node(node_count + i, n) for i, n in enumerate(
                [FunctionSet.get_random_function(self._population_param.rnd) if b else TerminalSet.get_random_terminal(self._population_param.rnd) for b in previous_layer_inputs]
            )]
            node_count += len(in_layer_nodes)

            _add_node_to_graph(graph, previous_layer_nodes, in_layer_nodes)
            previous_layer_nodes = [n for n in in_layer_nodes if not n.is_terminal]

        last_leafs = [Node(node_count + i, l) for i, l in enumerate(
            TerminalSet.get_random_terminals(self._population_param.rnd, sum(node.function.inputs for node in previous_layer_nodes))
        )]
        _add_node_to_graph(graph, previous_layer_nodes, last_leafs)
        return graph
