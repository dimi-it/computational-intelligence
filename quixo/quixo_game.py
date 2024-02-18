from copy import deepcopy
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
        """
        Returned the cached list of all the available moves
        """
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

    @property
    def current_player_available_move_list(self):
        """
        Return the player effectively available moves
        """
        possible_values = (self.player_id, -1)
        return [m for m in self.available_moves_list if self.board[m.position] in possible_values]

    @cached_property
    def available_moves_set(self) -> Set[MyMove]:
        """
        Return the cached set of the available moves
        """
        return set(self.available_moves_list)

    @property
    def move_count(self) -> int:
        """
        Return the move count
        """
        return self._move_count

    @property
    def player_id(self) -> int:
        """
        Return the current player id
        """
        return self.current_player_idx

    @property
    def board(self) -> np.ndarray:
        """
        Return the board
        """
        return self._board

    @property
    def board_clone(self) -> np.ndarray:
        """
        Return the board clone
        """
        return deepcopy(self._board)

    @staticmethod
    def get_results_over_x_games(p1: Player, p2: Player, games: int, change_order: bool = True, reset_rnd_gen: bool = False) -> tuple[int, int]:
        """
        Play x games and return the per player scores
        """
        tot = 0
        order = True if change_order else False
        for i in range(games):
            p1.reset(reset_rnd_gen)
            p2.reset(reset_rnd_gen)
            game = QuixoGame()
            if order == change_order:
                w = game.play(p1, p2)
            else:
                w = game.play(p2, p1)
                w = (w+1) % 2
            # game.print()
            tot += w
            if change_order:
                order = not order
        return games - tot, tot

    def check_winner(self) -> int:
        """
        Check the winner
        """
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
        """
        Check the position validity
        """
        assert len(pos) == 2, f"Expected 2 dimensions instead got {pos}"
        assert pos[0] >= 0 or pos[0] < self.BOARD_DIM, f"Expected pos between 0-{self.BOARD_DIM} got {pos[0]}"
        assert pos[1] >= 0 or pos[1] < self.BOARD_DIM, f"Expected pos between 0-{self.BOARD_DIM} got {pos[1]}"

    def is_current_player_pos(self, pos: Sequence[int]) -> bool:
        """
        Return true if is the player position
        """
        self._check_pos(pos)
        if self._board[pos] == self.current_player_idx:
            return True
        return False

    def is_other_player_pos(self, pos: Sequence[int]) -> bool:
        """
        Return true if is the opponent position
        """
        self._check_pos(pos)
        if self._board[pos] != self.current_player_idx and self._board[pos] != -1:
            return True
        return False

    def is_void_pos(self, pos: Sequence[int]) -> bool:
        """
        Return true if is a void position
        """
        self._check_pos(pos)
        if self._board[pos] == -1:
            return True
        return False

    def is_move_doable(self, move: MyMove) -> bool:
        """
        Return true if the move is really doable
        """
        if move not in self.available_moves_set or self.is_other_player_pos(move.position_reversed):
            return False
        return True

    def play(self, player1: Player, player2: Player) -> int:
        """
        Play the game
        """
        players = [player1, player2]
        winner = -1
        while winner < 0:
            self.current_player_idx += 1
            self.current_player_idx %= len(players)

            from_pos, slide = players[self.current_player_idx].make_move(self)
            self.__move(from_pos, slide, self.current_player_idx)
            self._move_count += 1

            winner = self.check_winner()
            if self._move_count > 1000:
                return 0
            # self.print()
        return winner

    def move(self, from_pos: tuple[int, int], slide: MoveDirection, player_id: int):
        """
        Make single move from outside
        """
        self.__move(from_pos, slide, player_id)
        self.current_player_idx = (self.current_player_idx + 1) % 2
        self._move_count += 1

    def __move(self, from_pos: tuple[int, int], slide: MoveDirection, player_id: int):
        """
        Make move
        """
        if player_id > 2:
            return False
        self.__take((from_pos[1], from_pos[0]), player_id)
        self.__slide((from_pos[1], from_pos[0]), slide)

    def __take(self, from_pos: tuple[int, int], player_id: int):
        """
        Take piece
        """
        self._board[from_pos] = player_id

    def __slide(self, from_pos: tuple[int, int], slide: MoveDirection):
        """
        Slide piece
        """
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
