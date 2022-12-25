import chess

from algorithms import Algorithm


class Game:
    NEGAMAX = 1
    NEGASCOUT = 2
    PVSEARCH = 3

    def __init__(self, board: chess.Board):
        self.board = board
        self.alg = Algorithm()

    def move(self, func, depth=2):
        result = None
        if func == self.NEGAMAX:
            result = self.__move_negamax(depth)
        elif func == self.NEGASCOUT:
            result = self.__move_negascout(depth)
        elif func == self.PVSEARCH:
            result = self.__move_pvsearch(depth)
        else:
            print("Function not found")
        return result

    def __move_negamax(self, depth):
        resultMove = None
        if depth == 0:
            return self.alg.evaluate(self.board, self.board.turn)
        maxValue = float('-inf')
        for move in list(map(str, list(self.board.legal_moves))):
            nextBoard = self.board.copy()
            nextBoard.push_uci(move)
            score = -self.alg.negamax(self.board, depth)
            if score > maxValue:
                maxValue = score
                resultMove = move
        return resultMove

    def __move_negascout(self, depth):
        resultMove = None
        if depth == 0:
            return self.alg.evaluate(self.board, self.board.turn)
        maxValue = float('-inf')
        for move in list(map(str, list(self.board.legal_moves))):
            nextBoard = self.board.copy()
            nextBoard.push_uci(move)
            score = self.alg.negascout(self.board, depth, float('-inf'), float('+inf'))
            if score > maxValue:
                maxValue = score
                resultMove = move
        return resultMove

    def __move_pvsearch(self, depth):
        resultMove = None
        if depth == 0:
            return self.alg.evaluate(self.board, self.board.turn)
        maxValue = float('-inf')
        for move in list(map(str, list(self.board.legal_moves))):
            nextBoard = self.board.copy()
            nextBoard.push_uci(move)
            score = -self.alg.pvsearch(self.board, depth, float('-inf'), float('+inf'))
            if score > maxValue:
                maxValue = score
                resultMove = move
        return resultMove
