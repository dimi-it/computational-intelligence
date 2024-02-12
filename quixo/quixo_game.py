from typing import Sequence

import numpy as np

from quixo.game import Game


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
