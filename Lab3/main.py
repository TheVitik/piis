import chess
from game import Game


def play(game: Game, count=10):
    for step in range(count):
        move = game.move(Game.PVSEARCH, 2)
        if step % 2 == 0:
            print(" White:  ", move)
        else:
            print(" Black:  ", move)
        game.board.push_uci(move)


def init():
    board = chess.Board()
    game = Game(board)
    print("=====CHESS=====")
    print(board)
    print("===============")
    print(" List of moves")
    print("===============")
    play(game)
    print("======END======")
    print(board)
    print("===============")


if __name__ == '__main__':
    init()
