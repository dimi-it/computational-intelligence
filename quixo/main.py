import random
from game import Game, MoveDirection, Player


class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game', player_id: int) -> tuple[tuple[int, int], MoveDirection]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([MoveDirection.TOP, MoveDirection.BOTTOM, MoveDirection.LEFT, MoveDirection.RIGHT])
        return from_pos, move


class MyPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game', player_id: int) -> tuple[tuple[int, int], MoveDirection]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([MoveDirection.TOP, MoveDirection.BOTTOM, MoveDirection.LEFT, MoveDirection.RIGHT])
        return from_pos, move


if __name__ == '__main__':
    g = Game()
    g.print()
    player1 = MyPlayer()
    player2 = RandomPlayer()
    winner = g.play(player1, player2)
    g.print()
    print(f"Winner: Player {winner}")
