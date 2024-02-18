from copy import deepcopy
from typing import Optional

import numpy as np

from quixo.game import Player, MoveDirection
from quixo.my_move import MyMove
from quixo.quixo_game import QuixoGame


class MinMaxPlayer(Player):
    MAX_VALUE = 1000

    def __init__(self, search_depth: int = 2):
        super().__init__()
        self._search_depth = search_depth

    def reset(self, also_rnd: bool = False):
        pass

    def make_move(self, game: QuixoGame) -> tuple[tuple[int, int], MoveDirection]:
        """
        Make the move
        """
        _, move = self._recursive_analysis(game, self._search_depth, True, - MinMaxPlayer.MAX_VALUE,
                                           MinMaxPlayer.MAX_VALUE)
        return move.to_tuple

    def _game_evaluation(self, game: QuixoGame, winner: int) -> int:
        """
        Evaluate the current game situation
        """
        if winner == -1:
            return self._player_evaluation(game, game.player_id) - self._player_evaluation(game,
                                                                                           (game.player_id + 1) % 2)
        elif winner == game.player_id:
            return MinMaxPlayer.MAX_VALUE
        else:
            return - MinMaxPlayer.MAX_VALUE

    def _player_evaluation(self, game: QuixoGame, player_id: int) -> int:
        """
        Evaluate the player situation
        """
        columns_occurrencies = (game.board == player_id).sum(axis=0).tolist()
        rows_occurrencies = (game.board == player_id).sum(axis=1).tolist()
        diagonals_occurrencies = [(game.board.diagonal() == player_id).sum(),
                                  (np.fliplr(game.board).diagonal() == player_id).sum()]
        all_combinations = [*columns_occurrencies, *rows_occurrencies, *diagonals_occurrencies]
        result = 0
        for c in all_combinations:
            if c == 1:
                result += c
            if c == 2:
                result += c * 2
            if c == 3:
                result += c * 4
            if c == 4:
                result += c * 8
        return result

    def _recursive_analysis(self, game: QuixoGame, current_depth: int, is_maximizing: bool, alpha: int, beta: int) -> tuple[int, Optional[MyMove]]:
        """
        Do the minmax algorithm by recursevly analyze and evaluating possible solution
        """
        available_moves = game.current_player_available_move_list
        top_evaluation = - MinMaxPlayer.MAX_VALUE if is_maximizing else MinMaxPlayer.MAX_VALUE
        top_move = None

        winner = game.check_winner()
        if winner != -1 or current_depth == 0:
            return self._game_evaluation(game, winner), None

        for move in available_moves:
            pos, dir = move.to_tuple
            test_game = deepcopy(game)
            test_game.move(pos, dir, game.player_id)

            evaluation, _ = self._recursive_analysis(test_game, current_depth - 1, not is_maximizing, alpha, beta)

            if is_maximizing:
                if evaluation > top_evaluation:
                    top_evaluation = evaluation
                    top_move = move
                alpha = max(alpha, top_evaluation)
            else:
                if evaluation < top_evaluation:
                    top_evaluation = evaluation
                    top_move = move
                beta = min(beta, top_evaluation)

            if beta <= alpha:
                break

        return top_evaluation, top_move
