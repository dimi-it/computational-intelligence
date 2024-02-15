from quixo.game import Player, MoveDirection
from random import Random

from quixo.my_move import MyMove
from quixo.quixo_game import QuixoGame


class MyRandomPlayer(Player):
    def __init__(self, seed: int) -> None:
        super().__init__()
        self._rnd = Random(seed)

    def make_move(self, game: QuixoGame) -> tuple[tuple[int, int], MoveDirection]:
        while True:
            move = self._rnd.choice(game.available_moves_list)
            if game.is_move_doable(move):
                break
        print(f"RANDOM => Pos: {move.position}, Dir: {move.direction}")
        return move.to_tuple
