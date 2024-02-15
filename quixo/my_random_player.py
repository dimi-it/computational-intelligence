from quixo.game import Player, Move
from random import Random


class MyRandomPlayer(Player):
    def __init__(self, seed: int) -> None:
        super().__init__()
        self.rnd = Random(seed)

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (self.rnd.randint(0, 4), self.rnd.randint(0, 4))
        move = self.rnd.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        print(f"RANDOM => Res: {from_pos}, Move {move}")
        return from_pos, move
