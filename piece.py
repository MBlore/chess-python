# --------------------------------------------------------------------------------------------------------
# Chess with PyGame
# Created by Martin Blore 2023
# Full explanation can be found at https://codewithmartin.io/articles/how-to-code-a-chess-game-in-python
# --------------------------------------------------------------------------------------------------------

from enum import Enum

class Piece(Enum):
    NONE = 0
    WHITE_PAWN = 1
    WHITE_KNIGHT = 2
    WHITE_BISHOP = 3
    WHITE_ROOK = 4
    WHITE_QUEEN = 5
    WHITE_KING = 6
    BLACK_PAWN = 7
    BLACK_KNIGHT = 8
    BLACK_BISHOP = 9
    BLACK_ROOK = 10
    BLACK_QUEEN = 11
    BLACK_KING = 12

    def is_white_piece(piece):
        return (piece == Piece.WHITE_PAWN or
            piece == Piece.WHITE_BISHOP or
            piece == Piece.WHITE_ROOK or
            piece == Piece.WHITE_KNIGHT or
            piece == Piece.WHITE_KING or
            piece == Piece.WHITE_QUEEN)

    def is_black_piece(piece):
        return not Piece.is_white_piece(piece)

    def is_enemy_piece(piece, target):
        if (target == Piece.NONE):
            return False
        if Piece.is_white_piece(piece) and Piece.is_black_piece(target):
            return True
        if Piece.is_black_piece(piece) and Piece.is_white_piece(target):
            return True

        return False