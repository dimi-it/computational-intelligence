from functools import cached_property
from typing import Sequence, Set, List

import numpy as np

from quixo.game import MoveDirection, Player, Game
from quixo.my_move import MyMove


class QuixoGame(Game):
    def __init__(self) -> None:
        super().__init__()
        self._move_count = 0

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

    @property
    def move_count(self) -> int:
        return self._move_count

    def check_winner(self) -> int:
        '''Check the winner. Returns the player ID of the winner if any, otherwise returns -1'''
        # for each row
        for x in range(self._board.shape[0]):
            # if a player has completed an entire row
            if self._board[x, 0] != -1 and all(self._board[x, :] == self._board[x, 0]):
                # return the relative id
                return self._board[x, 0]
        # for each column
        for y in range(self._board.shape[1]):
            # if a player has completed an entire column
            if self._board[0, y] != -1 and all(self._board[:, y] == self._board[0, y]):
                # return the relative id
                return self._board[0, y]
        # if a player has completed the principal diagonal
        if self._board[0, 0] != -1 and all(
            [self._board[x, x]
                for x in range(self._board.shape[0])] == self._board[0, 0]
        ):
            # return the relative id
            return self._board[0, 0]
        # if a player has completed the secondary diagonal
        if self._board[0, -1] != -1 and all(
            [self._board[x, -(x + 1)]
             for x in range(self._board.shape[0])] == self._board[0, -1]
        ):
            # return the relative id
            return self._board[0, -1]
        return -1

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

            from_pos, slide = players[self.current_player_idx].make_move(self)
            self.__move(from_pos, slide, self.current_player_idx)
            self._move_count += 1

            winner = self.check_winner()
            # self.print()
        return winner

    def __move(self, from_pos: tuple[int, int], slide: MoveDirection, player_id: int):
        '''Perform a move'''
        if player_id > 2:
            return False
        # Oh God, Numpy arrays
        self.__take((from_pos[1], from_pos[0]), player_id)
        self.__slide((from_pos[1], from_pos[0]), slide)

    def __take(self, from_pos: tuple[int, int], player_id: int):
        self._board[from_pos] = player_id

    def __slide(self, from_pos: tuple[int, int], slide: MoveDirection):
        '''Slide the other pieces'''
        piece = self._board[from_pos]
        # if the player wants to slide it to the left
        if slide == MoveDirection.LEFT:
            # for each column starting from the column of the piece and moving to the left
            for i in range(from_pos[1], 0, -1):
                # copy the value contained in the same row and the previous column
                self._board[(from_pos[0], i)] = self._board[(
                    from_pos[0], i - 1)]
            # move the piece to the left
            self._board[(from_pos[0], 0)] = piece
        # if the player wants to slide it to the right
        elif slide == MoveDirection.RIGHT:
            # for each column starting from the column of the piece and moving to the right
            for i in range(from_pos[1], self._board.shape[1] - 1, 1):
                # copy the value contained in the same row and the following column
                self._board[(from_pos[0], i)] = self._board[(
                    from_pos[0], i + 1)]
            # move the piece to the right
            self._board[(from_pos[0], self._board.shape[1] - 1)] = piece
        # if the player wants to slide it upward
        elif slide == MoveDirection.TOP:
            # for each row starting from the row of the piece and going upward
            for i in range(from_pos[0], 0, -1):
                # copy the value contained in the same column and the previous row
                self._board[(i, from_pos[1])] = self._board[(
                    i - 1, from_pos[1])]
            # move the piece up
            self._board[(0, from_pos[1])] = piece
        # if the player wants to slide it downward
        elif slide == MoveDirection.BOTTOM:
            # for each row starting from the row of the piece and going downward
            for i in range(from_pos[0], self._board.shape[0] - 1, 1):
                # copy the value contained in the same column and the following row
                self._board[(i, from_pos[1])] = self._board[(
                    i + 1, from_pos[1])]
            # move the piece down
            self._board[(self._board.shape[0] - 1, from_pos[1])] = piece
