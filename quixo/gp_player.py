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

    def __init__(self, brain: Individual, enable_random_move: Optional[bool] = True, loop_avoidance_limit: int = 5):
        super().__init__()
        self._brain = brain
        self._enable_random_move = enable_random_move
        self._loop_avoidance_limit = loop_avoidance_limit
        self._rnd = None
        self._set_rnd()
        self._move_count = 0
        self._rnd_move_count = 0
        self._last_move = None
        self._last_move_occurrences = 0

    @property
    def brain(self):
        """
        Return the individual
        """
        return self._brain

    @property
    def move_count(self) -> int:
        """
        Return the move played
        """
        return self._move_count

    @property
    def rnd_move_count(self) -> int:
        """
        Return the random move played
        """
        return self._rnd_move_count

    @property
    def rnd_move_percentage(self) -> float:
        """
        Return the random move percentage
        """
        return self._rnd_move_count / self._move_count * 100

    def _set_rnd(self):
        """
        Set random seed
        """
        self._rnd = Random(self._brain.random_seed)

    def reset_counters(self):
        """
        Reset counters
        """
        self._move_count = 0
        self._rnd_move_count = 0
        self._last_move = None
        self._last_move_occurrences = 0

    def reset(self, also_rnd: bool = False):
        """
        Reset player
        """
        self.reset_counters()
        if also_rnd:
            self._set_rnd()

    def _make_move_recursive(self, node: Node, game: QuixoGame) -> tuple[ValuePoint, Optional[MyMove]]:
        """
        Make move recursively, analyze the genome graph, depth first, in search of the first doable move.
        Return the tuple[value returned by the node, final move]
        """
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
                move = MyMove(result.point, MoveDirection[node.function.name.upper()])
                if game.is_move_doable(move):
                    if self._last_move == move and self._last_move_occurrences == self._loop_avoidance_limit:
                        # print("Loop limit reached")
                        return result, None
                    else:
                        if self._last_move == move:
                            self._last_move_occurrences += 1
                        else:
                            self._last_move = move
                            self._last_move_occurrences = 1
                        # print(f"AGENT => Pos: {move.position}, Dir {move.direction}")
                        return result, move
        return result, None

    def make_move(self, game: QuixoGame) -> tuple[tuple[int, int], MoveDirection]:
        """
        Make the move, if no move found analyzing the graph, make a random move.
        """
        if len(self._brain.genome) == 0:
            move = None
        else:
            _, move = self._make_move_recursive(list(self._brain.genome.nodes)[0], game)
        if move is None:
            # print("Damn, no doable move found ")
            assert self._enable_random_move, "Random move not enabled, no move available"
            while True:
                move = self._rnd.choice(game.available_moves_list)
                if game.is_move_doable(move):
                    break
            self._last_move = move
            self._last_move_occurrences = 1
            self._rnd_move_count += 1
            # print(f"AGENT RND => Pos: {move.position}, Dir: {move.direction}")
        self._move_count += 1
        return move.to_tuple

