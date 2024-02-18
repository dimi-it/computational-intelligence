from quixo.game import Player, MoveDirection
from random import Random

from quixo.my_move import MyMove
from quixo.quixo_game import QuixoGame


class MyRandomPlayer(Player):

    def __init__(self, seed: int) -> None:
        super().__init__()
        self._seed = seed
        self._rnd = None
        self._set_rnd()

    def _set_rnd(self):
        """
        Set the random generator
        """
        self._rnd = Random(self._seed)

    def reset(self, also_rnd: bool = False):
        """
        Reset the player
        """
        if also_rnd:
            self._set_rnd()

    def make_move(self, game: QuixoGame) -> tuple[tuple[int, int], MoveDirection]:
        """
        Make a random move
        """
        while True:
            move = self._rnd.choice(game.available_moves_list)
            if game.is_move_doable(move):
                break
        # print(f"RANDOM => Pos: {move.position}, Dir: {move.direction}")
        return move.to_tuple
