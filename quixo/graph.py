from random import Random

import networkx as nx

from quixo.node import Node


class GraphExtended:
    @staticmethod
    def remove_unconnected(G: nx.DiGraph, root: Node):
        H = nx.Graph()
        H.add_edges_from(G.edges)
        H.add_nodes_from(G.nodes)
        connected = nx.node_connected_component(H, root)
        G.remove_nodes_from(H.nodes - connected)

    @staticmethod
    def reidentify_nodes(G: nx.DiGraph, node: Node):
        node.id = 0
        _ = GraphExtended._reidentify_nodes_recursive(G, node, 1)

    @staticmethod
    def _reidentify_nodes_recursive(G: nx.DiGraph, node: Node, count: int) -> int:
        fan_out = [v for (u, v) in G.out_edges(node)]
        for n in fan_out:
            n.id = count
            count += 1
        for n in fan_out:
            count = GraphExtended._reidentify_nodes_recursive(G, n, count)
        return count

    @staticmethod
    def choice_edge(p_genome: nx.DiGraph, rnd: Random) -> (Node, Node):
        p_node = rnd.choice(list(p_genome.nodes)[1:])
        p_parent_edge = list(p_genome.in_edges(p_node))
        assert len(
            p_parent_edge) == 1, f"Something strange appened, {len(p_parent_edge)} edges from parent node to node"
        return p_parent_edge[0]
