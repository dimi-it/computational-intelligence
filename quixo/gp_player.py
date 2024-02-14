import random
from typing import List, Optional

import networkx as nx

from quixo.game import Player, Move, Game
from quixo.individual import Individual
from quixo.my_move import MyMove
from quixo.node import Node
from quixo.quixo_game import QuixoGame
from quixo.value_point import ValuePoint


class GeneticProgrammingPlayer(Player):
    def __init__(self, brain: Individual, enable_random: Optional[bool] = False):
        super().__init__()
        self._brain = brain
        self._enable_random = enable_random

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
            print(f"Res: {result}, Move {node.function.name}")
            if not result.is_nil():
                test_move = MyMove(result.point, Move[node.function.name.upper()])
                if game.is_move_doable(test_move):
                    return result, test_move
        return result, None

    def make_move(self, game: QuixoGame) -> tuple[tuple[int, int], Move]:
        _, move = self._make_move_recursive(list(self._brain.genome.nodes)[0], game)
        if move is None:
            print("Damn, no doable move found ")
            if self._enable_random:
                from_pos = (random.randint(0, 4), random.randint(0, 4))
                move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
                print(f"RND")
                return from_pos, move
        return move.to_tuple

