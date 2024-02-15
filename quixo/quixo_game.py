from functools import cached_property
from typing import Sequence, Set, List

import numpy as np

from quixo.game import Game, MoveDirection, Player
from quixo.my_move import MyMove


class QuixoGame(Game):
    def __init__(self) -> None:
        super().__init__()

    @cached_property
    def available_moves_list(self) -> List[MyMove]:
        moves = list()
        for i in range(self.BOARD_DIM):
            for j in range(self.BOARD_DIM):
                if i == 0:
                    moves.append(MyMove((i, j), MoveDirection.RIGHT))
                    if 0 < j < self.BOARD_DIM - 1:
                        moves.append(MyMove((i, j), MoveDirection.BOTTOM))
                        moves.append(MyMove((i, j), MoveDirection.TOP))
                if i == 4:
                    moves.append(MyMove((i, j), MoveDirection.LEFT))
                    if 0 < j < self.BOARD_DIM - 1:
                        moves.append(MyMove((i, j), MoveDirection.BOTTOM))
                        moves.append(MyMove((i, j), MoveDirection.TOP))
                if j == 0:
                    moves.append(MyMove((i, j), MoveDirection.BOTTOM))
                    if 0 < i < self.BOARD_DIM - 1:
                        moves.append(MyMove((i, j), MoveDirection.RIGHT))
                        moves.append(MyMove((i, j), MoveDirection.LEFT))
                if j == 4:
                    moves.append(MyMove((i, j), MoveDirection.TOP))
                    if 0 < i < self.BOARD_DIM - 1:
                        moves.append(MyMove((i, j), MoveDirection.RIGHT))
                        moves.append(MyMove((i, j), MoveDirection.LEFT))
        return moves

    @cached_property
    def available_moves_set(self) -> Set[MyMove]:
        return set(self.available_moves_list)

    def _check_pos(self, pos: Sequence[int]):
        assert len(pos) == 2, f"Expected 2 dimensions instead got {pos}"
        assert pos[0] >= 0 or pos[0] < self.BOARD_DIM, f"Expected pos between 0-{self.BOARD_DIM} got {pos[0]}"
        assert pos[1] >= 0 or pos[1] < self.BOARD_DIM, f"Expected pos between 0-{self.BOARD_DIM} got {pos[1]}"

    def is_current_player_pos(self, pos: Sequence[int]) -> bool:
        self._check_pos(pos)
        if self._board[pos] == self.current_player_idx:
            return True
        return False

    def is_other_player_pos(self, pos: Sequence[int]) -> bool:
        self._check_pos(pos)
        if self._board[pos] != self.current_player_idx and self._board[pos] != -1:
            return True
        return False

    def is_void_pos(self, pos: Sequence[int]) -> bool:
        self._check_pos(pos)
        if self._board[pos] == -1:
            return True
        return False

    def is_move_doable(self, move: MyMove) -> bool:
        if move not in self.available_moves_set or self.is_other_player_pos(move.position_reversed):
            return False
        return True


    def play(self, player1: Player, player2: Player) -> int:
        '''Play the game. Returns the winning player'''
        players = [player1, player2]
        winner = -1
        while winner < 0:
            self.current_player_idx += 1
            self.current_player_idx %= len(players)
            ok = False
            while not ok:
                from_pos, slide = players[self.current_player_idx].make_move(
                    self, self.current_player_idx)
                ok = self.__move(from_pos, slide, self.current_player_idx)
                print(f"Player:{self.current_player_idx}, Pos:{from_pos}, Move:{slide}, Checked:{ok}")
            winner = self.check_winner()
            self.print()
        return winner
