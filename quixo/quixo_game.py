from typing import Sequence

import numpy as np

from quixo.game import Game, Move
from quixo.my_move import MyMove


class QuixoGame(Game):
    def __init__(self) -> None:
        super().__init__()

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
        if self._board[pos] == - self.current_player_idx:
            return True
        return False

    def is_void_pos(self, pos: Sequence[int]) -> bool:
        self._check_pos(pos)
        if self._board[pos] == 0:
            return True
        return False

    def is_move_doable(self, move: MyMove) -> bool:
        acceptable: bool = (
                               # check if it is in the first row
                                   (move.position[0] == 0 and move.position[1] < 5)
                                   # check if it is in the last row
                                   or (move.position[0] == 4 and move.position[1] < 5)
                                   # check if it is in the first column
                                   or (move.position[1] == 0 and move.position[0] < 5)
                                   # check if it is in the last column
                                   or (move.position[1] == 4 and move.position[0] < 5)
                               # and check if the piece can be moved by the current player
                           ) and (self._board[move.position] < 0 or self._board[move.position] == move.position)
        if not acceptable:
            return False

        # define the corners
        SIDES = [(0, 0), (0, 4), (4, 0), (4, 4)]
        # if the piece position is not in a corner
        if move.position not in SIDES:
            # if it is at the TOP, it can be moved down, left or right
            acceptable_top: bool = move.position[0] == 0 and (
                    move.move == Move.BOTTOM or move.move == Move.LEFT or move.move == Move.RIGHT
            )
            # if it is at the BOTTOM, it can be moved up, left or right
            acceptable_bottom: bool = move.position[0] == 4 and (
                    move.move == Move.TOP or move.move == Move.LEFT or move.move == Move.RIGHT
            )
            # if it is on the LEFT, it can be moved up, down or right
            acceptable_left: bool = move.position[1] == 0 and (
                    move.move == Move.BOTTOM or move.move == Move.TOP or move.move == Move.RIGHT
            )
            # if it is on the RIGHT, it can be moved up, down or left
            acceptable_right: bool = move.position[1] == 4 and (
                    move.move == Move.BOTTOM or move.move == Move.TOP or move.move == Move.LEFT
            )
        # if the piece position is in a corner
        else:
            # if it is in the upper left corner, it can be moved to the right and down
            acceptable_top: bool = move.position == (0, 0) and (
                    move.move == Move.BOTTOM or move.move == Move.RIGHT)
            # if it is in the lower left corner, it can be moved to the right and up
            acceptable_left: bool = move.position == (4, 0) and (
                    move.move == Move.TOP or move.move == Move.RIGHT)
            # if it is in the upper right corner, it can be moved to the left and down
            acceptable_right: bool = move.position == (0, 4) and (
                    move.move == Move.BOTTOM or move.move == Move.LEFT)
            # if it is in the lower right corner, it can be moved to the left and up
            acceptable_bottom: bool = move.position == (4, 4) and (
                    move.move == Move.TOP or move.move == Move.LEFT)
        # check if the move is acceptable
        acceptable: bool = acceptable_top or acceptable_bottom or acceptable_left or acceptable_right
        return acceptable