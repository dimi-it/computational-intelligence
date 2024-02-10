from quixo.game import Player, Move, Game


class GeneticProgrammingPlayer(Player):
    def __int__(self):
        super().__init__()

    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        pass

