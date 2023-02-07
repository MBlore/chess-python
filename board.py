# --------------------------------------------------------------------------------------------------------
# Chess with PyGame
# Created by Martin Blore 2023
# Full explanation can be found at https://codewithmartin.io/articles/how-to-code-a-chess-game-in-python
# --------------------------------------------------------------------------------------------------------
import math
import pygame
from board_render import BoardRender
from board_setup import BoardSetup
from move_result import MoveResult
from piece import Piece
from piece_moves import PieceMoves
    
class Board:
    def __init__(self):
        self.board_state = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        '''
        Board indexes for reference:

        0,0 	0,1     0,2     0,3     0,4     0,5     0,6     0,7
        1,0     1,1     1,2     1,3     1,4     1,5     1,6     1,7
        2,0     2,1     2,2     2,3     2,4     2,5     2,6     2,7
        3,0     3,1     3,2     3,3     3,4     3,5     3,6     3,7
        4,0     4,1     4,2     4,3     4,4     4,5     4,6     4,7
        5,0     5,1     5,2     5,3     5,4     5,5     5,6     5,7
        6,0     6,1     6,2     6,3     6,4     6,5     6,6     6,7
        7,0     7,1     7,2     7,3     7,4     7,5     7,6     7,7
        '''

        self.cell_size = 100
        self.board_start_x = 100
        self.board_start_y = 100
        self.hide_row_index = -1
        self.hide_col_index = -1
        self.white_square_color = (230, 230, 230)
        self.black_square_color = (100, 150, 100)
        self.start_drag_square = (-1, -1)
        self.dragging_piece = Piece.NONE

        # Castling state variables.
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_king_side_rook_moved = False
        self.white_queen_side_rook_moved = False
        self.black_king_side_rook_moved = False
        self.black_queen_side_rook_moved = False

        # Last moved piece to assist with the en-passant logic.
        self.last_moved_piece = Piece.NONE
        self.last_moved_piece_from = (0,0)

    # Clears the board.
    def clear(self):
        for row_index, row in enumerate(self.board_state):
            for col_index, col in enumerate(row):
                self.board_state[row_index][col_index] = Piece.NONE

    # Set up the board state for a new game.
    def setup(self):
        self.clear()
        BoardSetup.setup_standard(self)
        # BoardSetup.setup_stale_mate(self)

    # Causes the specific square to not be drawn, used for when drag operations are happening.
    def hide_square(self, row, col):
        self.hide_row_index = row
        self.hide_col_index = col

    # Unhides the hidden square.
    def unhide_square(self):
        self.hide_row_index = -1
        self.hide_col_index = -1

    # Draw the board and pieces.
    def draw(self, screen, images):
        BoardRender.draw_board(self, screen)
        BoardRender.draw_pieces(self, screen, images)

    # Gets the current board square that the mouse cursor is over.
    def board_index_from_mouse_pos(self):
        mouse_pos = pygame.mouse.get_pos()

        grid_x = mouse_pos[0] - self.board_start_x
        grid_y = mouse_pos[1] - self.board_start_y

        clicked_in_grid = True

        if (grid_x < 0 or grid_y < 0):
            clicked_in_grid = False

        if (grid_x > self.cell_size * 8 or grid_y > self.cell_size * 8):
            clicked_in_grid = False

        if (clicked_in_grid):
            col_index = math.floor(grid_x / self.cell_size)
            row_index = math.floor(grid_y / self.cell_size)

            return (row_index, col_index)
        else:
            return (-1, -1)

    def is_piece_on_square(self, row, col):
        return self.board_state[row][col] != Piece.NONE

    def start_drag(self, row, col):
        self.hide_square(row, col)
        self.start_drag_square = row, col
        self.dragging_piece = self.board_state[row][col]

    def stop_drag(self):
        self.unhide_square()
        self.dragging_piece = Piece.NONE

    # When a piece has been dragged, and its the correct players turn, the piece movement
    # on the board needs to be validated.
    def perform_move(self, end_square):
        result = MoveResult()

        if self.dragging_piece == Piece.NONE:
            result.move_performed = False
            return result
        
        start_square = self.start_drag_square
        piece = self.dragging_piece
        whites_turn = Piece.is_white_piece(piece)

        moves = PieceMoves.get_moves_for_piece(self, piece, start_square)
        move_allowed = end_square in moves

        if not move_allowed:
            result.move_performed = False
            return result

        result.move_performed = True
             
        # Are we about to perform en-passant?
        en_passant_movement = self._is_en_passant_movement(piece, start_square, end_square)

        # Perform the piece move.
        self.board_state[start_square[0]][start_square[1]] = Piece.NONE
        self.board_state[end_square[0]][end_square[1]] = piece

        if en_passant_movement:
            # Capture the pawn we just moved behind.
            if piece == Piece.WHITE_PAWN:
                self.board_state[end_square[0]+1][end_square[1]] = Piece.NONE
            else:
                self.board_state[end_square[0]-1][end_square[1]] = Piece.NONE

        # Did we just castle? If so, move the rooks.
        if (piece == Piece.WHITE_KING and
            start_square[0] == 7 and start_square[1] == 4 and
            end_square[0] == 7 and end_square[1] == 6):
            # White king side castle.
            self.board_state[7][7] = Piece.NONE
            self.board_state[7][5] = Piece.WHITE_ROOK

        if (piece == Piece.WHITE_KING and
            start_square[0] == 7 and start_square[1] == 4 and
            end_square[0] == 7 and end_square[1] == 2):
            # White queen side castle.
            self.board_state[7][0] = Piece.NONE
            self.board_state[7][3] = Piece.WHITE_ROOK

        if (piece == Piece.BLACK_KING and
            start_square[0] == 0 and start_square[1] == 4 and
            end_square[0] == 0 and end_square[1] == 6):
            # White king side castle.
            self.board_state[0][7] = Piece.NONE
            self.board_state[0][5] = Piece.BLACK_ROOK

        if (piece == Piece.BLACK_KING and
            start_square[0] == 0 and start_square[1] == 4 and
            end_square[0] == 0 and end_square[1] == 2):
            # White queen side castle.
            self.board_state[0][0] = Piece.NONE
            self.board_state[0][3] = Piece.BLACK_ROOK
       
        # Check if we put ourselves in check.
        if self._is_player_in_check(self.board_state, whites_turn):
            # Undo the move.
            self.board_state[start_square[0]][start_square[1]] = piece
            self.board_state[end_square[0]][end_square[1]] = Piece.NONE

            # Undo en-passant capture.
            if en_passant_movement:
                if piece == Piece.WHITE_PAWN:
                    self.board_state[end_square[0]+1][end_square[1]] = Piece.BLACK_PAWN
                else:
                    self.board_state[end_square[0]-1][end_square[1]] = Piece.WHITE_PAWN

            result.move_performed = False
            result.move_denied_self_check = True
            return result
        
        # Have we checked the opponent?
        if self._is_player_in_check(self.board_state, not whites_turn):
            result.opponent_now_in_check = True

            # Have we check mated / stale mated?
            if self._is_player_in_check_mate(not whites_turn):
                result.opponent_check_mate = True

        # Is the opponent in stale mate?
        result.opponent_stale_mate = self._is_stale_mate(whites_turn)

        # Record this move.
        self.last_moved_piece = piece
        self.last_moved_piece_from = start_square

        # Did we move the kings?
        if piece == Piece.WHITE_KING:
            self.white_king_moved = True
        if piece == Piece.BLACK_KING:
            self.black_king_moved = True

        # Did we move the rooks?
        if start_square[0] == 7 and start_square[1] == 0:
            self.white_queen_side_rook_moved = True
        if start_square[0] == 7 and start_square[1] == 7:
            self.white_king_side_rook_moved = True
        if start_square[0] == 0 and start_square[1] == 0:
            self.black_queen_side_rook_moved = True
        if start_square[0] == 0 and start_square[1] == 7:
            self.black_king_side_rook_moved = True

        # Did a pawn make it to the last rank for promotion?
        if ((piece == Piece.WHITE_PAWN and end_square[0] == 0) or
            (piece == Piece.BLACK_PAWN and end_square[0] == 7)):
            result.promote_available = True
            result.promote_position = end_square
       
        return result

    # Returns true if the specified pawn movement is detected as being en-passant.
    def _is_en_passant_movement(self, piece, start_square, end_square):
        # We detect this by seeing if the pawn has been allowed to capture an empty square.
        # White pawns left diagonal check.
        if piece == Piece.WHITE_PAWN:
            if end_square[1] == start_square[1]-1 and end_square[0] == start_square[0]-1:
                if self.board_state[end_square[0]][end_square[1]] == Piece.NONE:
                    return True

        # White pawns right diagonal check.
        if piece == Piece.WHITE_PAWN:
            if end_square[1] == start_square[1]+1 and end_square[0] == start_square[0]-1:
                if self.board_state[end_square[0]][end_square[1]] == Piece.NONE:
                    return True

        # Black pawns left diagonal check.
        if piece == Piece.BLACK_PAWN:
            if end_square[1] == start_square[1]-1 and end_square[0] == start_square[0]+1:
                if self.board_state[end_square[0]][end_square[1]] == Piece.NONE:
                    return True

        # Black pawns right diagonal check.
        if piece == Piece.BLACK_PAWN:
            if end_square[1] == start_square[1]+1 and end_square[0] == start_square[0]+1:
                if self.board_state[end_square[0]][end_square[1]] == Piece.NONE:
                    return True

        return False

    # Find the king and return his coordinates.
    def _find_king(self, board, white):
        found = False
        for row in range(0, 8):
            for col in range(0, 8):
                if board[row][col] == Piece.WHITE_KING if white else board[row][col] == Piece.BLACK_KING:
                    found = True
                    break
            if found:
                break

        return row, col
        
    def _is_player_in_check(self, board, white):
        king = self._find_king(board, white)

        king_row = king[0]
        king_col = king[1]

        # Let's traverse all the pieces to check for check.
        for row in range(0, 8):
            for col in range(0, 8):
                check_piece = False
                piece = board[row][col]
                
                if piece == Piece.NONE:
                    continue

                if white:
                    check_piece = Piece.is_black_piece(piece)
                else:
                    check_piece = Piece.is_white_piece(piece)

                if not check_piece:
                    continue

                moves = PieceMoves.get_moves_for_piece(self, piece, (row, col))

                if (king_row, king_col) in moves:
                    return True

    def _is_player_in_check_mate(self, white):
        # For each piece, see if we can we save the king (we're assuming the king is already in check here).
        for row in range(0, 8):
            for col in range(0, 8):
                check_piece = False
                piece = self.board_state[row][col]
                
                if piece == Piece.NONE:
                    continue

                if white:
                    check_piece = Piece.is_white_piece(piece)
                else:
                    check_piece = Piece.is_black_piece(piece)

                if not check_piece:
                    continue

                moves = PieceMoves.get_moves_for_piece(self, piece, (row, col))

                # Move this piece in to all of its availble positions seeing if it saves the king at each move.
                for move in moves:
                    # Move the piece.
                    piece_at_target = self.board_state[move[0]][move[1]]
                    self.board_state[row][col] = Piece.NONE
                    self.board_state[move[0]][move[1]] = piece

                    if not self._is_player_in_check(self.board_state, white):
                        # Undo the move.
                        self.board_state[row][col] = piece
                        self.board_state[move[0]][move[1]] = piece_at_target

                        # We can get out of check with this move
                        return False
                    else:
                        # Undo the move, carry on and keep trying.
                        self.board_state[row][col] = piece
                        self.board_state[move[0]][move[1]] = piece_at_target

        # Failed to get out of the check state, we are truly in check mate here.
        return True

    # Returns true if the opponent is now in stale mate.
    def _is_stale_mate(self, whites_turn):
        for row in range(0, 8):
            for col in range(0, 8):

                piece = self.board_state[row][col]
                if piece == Piece.NONE:
                    continue
                if whites_turn and Piece.is_white_piece(piece):
                    continue
                if not whites_turn and Piece.is_black_piece(piece):
                    continue

                moves = PieceMoves.get_moves_for_piece(self, piece, (row, col))
                    
                # We need to see if we can move in to these available movements without causing a check.
                for move in moves:
                    target_piece = self.board_state[move[0]][move[1]]

                    # Lets sim the move.
                    self.board_state[row][col] = Piece.NONE
                    self.board_state[move[0]][move[1]] = piece

                    # Does it result in a check?
                    if not self._is_player_in_check(self.board_state, not whites_turn):
                        # Undo the move.
                        self.board_state[row][col] = piece
                        self.board_state[move[0]][move[1]] = target_piece
                        return False

                    # Undo the move.
                    self.board_state[row][col] = piece
                    self.board_state[move[0]][move[1]] = target_piece

        return True

    def promote_pawn(self, pos, new_piece_id):
        if pos[1] != 0 and pos[1] != 7:
            raise Exception("Invalid rank for promotion.")

        piece = self.board_state[pos[0]][pos[1]]

        if piece != Piece.WHITE_PAWN and piece != Piece.BLACK_PAWN:
            raise Exception("Piece is not a pawn.")

        if piece == Piece.WHITE_PAWN:
            if (new_piece_id != Piece.WHITE_KNIGHT and
                new_piece_id != Piece.WHITE_BISHOP and
                new_piece_id != Piece.WHITE_ROOK and
                new_piece_id != Piece.WHITE_QUEEN):
                raise Exception("Invalid new piece id.")

        if piece == Piece.BLACK_PAWN:
            if (new_piece_id != Piece.BLACK_KNIGHT and
                new_piece_id != Piece.BLACK_BISHOP and
                new_piece_id != Piece.BLACK_ROOK and
                new_piece_id != Piece.BLACK_QUEEN):
                raise Exception("Invalid new piece id.")

        # Allow the promotion.  
        self.board_state[pos[0]][pos[1]] = new_piece_id

        

        