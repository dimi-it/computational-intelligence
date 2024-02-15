from random import Random
from typing import List, Optional

import networkx as nx

from quixo.game import Player, MoveDirection, Game
from quixo.individual import Individual
from quixo.my_move import MyMove
from quixo.node import Node
from quixo.quixo_game import QuixoGame
from quixo.value_point import ValuePoint


class GeneticProgrammingPlayer(Player):
    def __init__(self, brain: Individual, enable_random_move: Optional[bool] = False):
        super().__init__()
        self._brain = brain
        self._enable_random_move = enable_random_move
        self._rnd = Random(brain.genome_adj_str)

    def _make_move_recursive(self, node: Node, game: QuixoGame) -> tuple[ValuePoint, Optional[MyMove]]:
        if node.is_terminal:
            return node.value_point, None

        descendant: List[Node] = [v for u,v in self._brain.genome.out_edges(node)]
        descendants_results = []
        for d in descendant:
            res, move = self._make_move_recursive(d, game)
            if move is not None:
                return res, move
            descendants_results.append(res)
        result = node.function.op(descendants_results, game)
        if node.function.is_action:
            # print(f"Node Res: {result}, Move {node.function.name}")
            if not result.is_nil():
                test_move = MyMove(result.point, MoveDirection[node.function.name.upper()])
                if game.is_move_doable(test_move):
                    print(f"AGENT => Pos: {result}, Dir {node.function.name}")
                    return result, test_move
        return result, None

    def make_move(self, game: QuixoGame) -> tuple[tuple[int, int], MoveDirection]:
        _, move = self._make_move_recursive(list(self._brain.genome.nodes)[0], game)
        if move is None:
            # print("Damn, no doable move found ")
            assert self._enable_random_move, "Random move not enabled, no move available"
            while True:
                move = self._rnd.choice(game.available_moves_list)
                if game.is_move_doable(move):
                    break
            print(f"AGENT RND => Pos: {move.position}, Dir: {move.direction}")
        return move.to_tuple

