from typing import Sequence

import numpy as np

from quixo.game import Game, Move, Player
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
        if self._board[pos] != self.current_player_idx and self._board[pos] != -1:
            return True
        return False

    def is_void_pos(self, pos: Sequence[int]) -> bool:
        self._check_pos(pos)
        if self._board[pos] == -1:
            return True
        return False

    def is_move_doable(self, move: MyMove) -> bool:
        #check if the piece can be moved by the current player
        if self.is_other_player_pos(move.position_reversed):
            return False

        acceptable: bool = (
                               # check if it is in the first row
                               (move.position_reversed[0] == 0 and move.position_reversed[1] < 5)
                               # check if it is in the last row
                               or (move.position_reversed[0] == 4 and move.position_reversed[1] < 5)
                               # check if it is in the first column
                               or (move.position_reversed[1] == 0 and move.position_reversed[0] < 5)
                               # check if it is in the last column
                               or (move.position_reversed[1] == 4 and move.position_reversed[0] < 5)
        )
        if not acceptable:
            return False

        # define the corners
        SIDES = [(0, 0), (0, 4), (4, 0), (4, 4)]
        # if the piece position_reverted is not in a corner
        if move.position_reversed not in SIDES:
            # if it is at the TOP, it can be moved down, left or right
            acceptable_top: bool = move.position_reversed[0] == 0 and (
                    move.move == Move.BOTTOM or move.move == Move.LEFT or move.move == Move.RIGHT
            )
            # if it is at the BOTTOM, it can be moved up, left or right
            acceptable_bottom: bool = move.position_reversed[0] == 4 and (
                    move.move == Move.TOP or move.move == Move.LEFT or move.move == Move.RIGHT
            )
            # if it is on the LEFT, it can be moved up, down or right
            acceptable_left: bool = move.position_reversed[1] == 0 and (
                    move.move == Move.BOTTOM or move.move == Move.TOP or move.move == Move.RIGHT
            )
            # if it is on the RIGHT, it can be moved up, down or left
            acceptable_right: bool = move.position_reversed[1] == 4 and (
                    move.move == Move.BOTTOM or move.move == Move.TOP or move.move == Move.LEFT
            )
        # if the piece position_reverted is in a corner
        else:
            # if it is in the upper left corner, it can be moved to the right and down
            acceptable_top: bool = move.position_reversed == (0, 0) and (
                    move.move == Move.BOTTOM or move.move == Move.RIGHT)
            # if it is in the lower left corner, it can be moved to the right and up
            acceptable_left: bool = move.position_reversed == (4, 0) and (
                    move.move == Move.TOP or move.move == Move.RIGHT)
            # if it is in the upper right corner, it can be moved to the left and down
            acceptable_right: bool = move.position_reversed == (0, 4) and (
                    move.move == Move.BOTTOM or move.move == Move.LEFT)
            # if it is in the lower right corner, it can be moved to the left and up
            acceptable_bottom: bool = move.position_reversed == (4, 4) and (
                    move.move == Move.TOP or move.move == Move.LEFT)
        # check if the move is acceptable
        acceptable: bool = acceptable_top or acceptable_bottom or acceptable_left or acceptable_right
        return acceptable

    # def play(self, player1: Player, player2: Player) -> int:
    #     '''Play the game. Returns the winning player'''
    #     players = [player1, player2]
    #     winner = -1
    #     while winner < 0:
    #         self.current_player_idx += 1
    #         self.current_player_idx %= len(players)
    #         ok = False
    #         while not ok:
    #             from_pos, slide = players[self.current_player_idx].make_move(
    #                 self, self.current_player_idx)
    #             ok = self.__move(from_pos, slide, self.current_player_idx)
    #             print(f"Player:{self.current_player_idx}, Pos:{from_pos}, Move:{slide}, Checked:{ok}")
    #         winner = self.check_winner()
    #         self.print()
    #     return winner
