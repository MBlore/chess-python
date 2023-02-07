# --------------------------------------------------------------------------------------------------------
# Chess with PyGame
# Created by Martin Blore 2023
# Full explanation can be found at https://codewithmartin.io/articles/how-to-code-a-chess-game-in-python
# --------------------------------------------------------------------------------------------------------
from piece import Piece

# Premade board setups.
class BoardSetup:
    def setup_stale_mate(board):
        board.board_state[0][0] = Piece.BLACK_KING
        board.board_state[7][7] = Piece.WHITE_KING
        board.board_state[4][4] = Piece.WHITE_QUEEN

    def setup_standard(board):
        # Place pawns on 2nd row.
        for i, cell in enumerate(board.board_state[1]):
            board.board_state[1][i] = Piece.BLACK_PAWN

        # Place pawns on 7th row.
        for i, cell in enumerate(board.board_state[6]):
            board.board_state[6][i] = Piece.WHITE_PAWN

        # Rooks
        board.board_state[0][0] = board.board_state[0][7] = Piece.BLACK_ROOK
        board.board_state[7][0] = board.board_state[7][7] = Piece.WHITE_ROOK

        # Knights
        board.board_state[0][1] = board.board_state[0][6] = Piece.BLACK_KNIGHT
        board.board_state[7][1] = board.board_state[7][6] = Piece.WHITE_KNIGHT

        # Bishops
        board.board_state[0][2] = board.board_state[0][5] = Piece.BLACK_BISHOP
        board.board_state[7][2] = board.board_state[7][5] = Piece.WHITE_BISHOP

        # Queens
        board.board_state[0][3] = Piece.BLACK_QUEEN
        board.board_state[7][3] = Piece.WHITE_QUEEN

        # Kings
        board.board_state[0][4] = Piece.BLACK_KING
        board.board_state[7][4] = Piece.WHITE_KING