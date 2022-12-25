import chess


class Algorithm:
    # Pieces scores
    KING = 200
    QUEEN = 9
    ROOK = 5
    BISHOP = 3
    KNIGHT = 3
    PAWN = 1
    MOBILITY_WEIGHT = 0.1

    RESULT_MOVE = None

    def evaluate(self, board: chess.Board, white: bool):
        whiteMaterialScore = self.KING * len(board.pieces(chess.KING, True)) \
                             + self.QUEEN * len(board.pieces(chess.QUEEN, True)) \
                             + self.ROOK * len(board.pieces(chess.ROOK, True)) \
                             + self.KNIGHT * len(board.pieces(chess.KNIGHT, True)) \
                             + self.BISHOP * len(board.pieces(chess.BISHOP, True)) \
                             + self.PAWN * len(board.pieces(chess.PAWN, True))

        blackMaterialScore = self.KING * len(board.pieces(chess.KING, False)) \
                             + self.QUEEN * len(board.pieces(chess.QUEEN, False)) \
                             + self.ROOK * len(board.pieces(chess.ROOK, False)) \
                             + self.KNIGHT * len(board.pieces(chess.KNIGHT, False)) \
                             + self.BISHOP * len(board.pieces(chess.BISHOP, False)) \
                             + self.PAWN * len(board.pieces(chess.PAWN, False))

        materialScore = whiteMaterialScore - blackMaterialScore

        currentMoveMobility = board.legal_moves.count()

        board.push(chess.Move.null())
        nextMoveMobility = board.legal_moves.count()
        board.pop()

        mobilityScore = self.MOBILITY_WEIGHT * (currentMoveMobility - nextMoveMobility)

        who2move = -1
        if board.turn is white:
            who2move = 1

        return (materialScore + mobilityScore) * who2move

    def negamax(self, board: chess.Board, depth: int):
        if depth == 0:
            return self.evaluate(board, board.turn)
        maxValue = float('-inf')
        for move in list(map(str, list(board.legal_moves))):
            nextBoard = board.copy()
            nextBoard.push_uci(move)
            score = -self.negamax(nextBoard, depth - 1)
            if score > maxValue:
                maxValue = score
        return maxValue

    def negascout(self, board: chess.Board, depth: int, alpha: float, beta: float):
        if depth == 0:
            return self.evaluate(board, board.turn)
        maxValue = float('-inf')
        b = beta
        for move in list(map(str, list(board.legal_moves))):
            nextBoard = board.copy()
            nextBoard.push_uci(move)
            score = -self.negascout(nextBoard, depth - 1, -b, -alpha)
            if score > maxValue:
                if b == beta or depth <= 2:
                    maxValue = score
                else:
                    maxValue = -self.negascout(nextBoard, depth - 1, -beta, -score)

            if maxValue > alpha:
                alpha = maxValue
            if alpha > beta:
                return alpha
            b = alpha + 1
        return maxValue

    def pvsearch(self, board: chess.Board, depth: int, alpha: float, beta: float):
        if depth == 0:
            return self.evaluate(board, board.turn)
        bSearchPv = True
        for move in list(map(str, list(board.legal_moves))):
            nextBoard = board.copy()
            nextBoard.push_uci(move)
            if bSearchPv:
                score = -self.pvsearch(nextBoard, depth - 1, -beta, -alpha)
            else:
                score = -self.pvsearch(nextBoard, depth - 1, -alpha - 1, -alpha)
                if score > alpha:
                    score = -self.pvsearch(nextBoard, depth - 1, -beta, -alpha)

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
                bSearchPv = False

        return alpha
