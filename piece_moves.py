# --------------------------------------------------------------------------------------------------------
# Chess with PyGame
# Created by Martin Blore 2023
# Full explanation can be found at https://codewithmartin.io/articles/how-to-code-a-chess-game-in-python
# --------------------------------------------------------------------------------------------------------

from piece import Piece

# Contains all functions that build possible movement squares for all piece types.
class PieceMoves:

    # Get the available moves for a specific piece on the board.
    def get_moves_for_piece(board, piece, square, disable_castling = False):
        if piece == Piece.WHITE_PAWN:
            return PieceMoves.moves_for_white_pawn(board, square)
        elif piece == Piece.BLACK_PAWN:
            return PieceMoves.moves_for_black_pawn(board, square)
        elif piece == Piece.WHITE_BISHOP or piece == Piece.BLACK_BISHOP:
            return PieceMoves.moves_for_bishop(board, square)
        elif piece == Piece.WHITE_ROOK or piece == Piece.BLACK_ROOK:
            return PieceMoves.moves_for_rook(board, square)
        elif piece == Piece.WHITE_QUEEN or piece == Piece.BLACK_QUEEN:
            return PieceMoves.moves_for_queen(board, square)
        elif piece == Piece.WHITE_KING or piece == Piece.BLACK_KING:
            return PieceMoves.moves_for_king(board, square, disable_castling)
        elif piece == Piece.WHITE_KNIGHT or piece == Piece.BLACK_KNIGHT:
            return PieceMoves.moves_for_knight(board, square)

        raise Exception("No moves for specified piece.")

    def moves_for_white_pawn(board, pos):
        possible_moves = []

        # Top of the board.
        if pos[0] == 0:
            return possible_moves

        # Left diagonal attack.
        if (pos[1] > 0 and Piece.is_enemy_piece(Piece.WHITE_PAWN, board.board_state[pos[0]-1][pos[1]-1])):
            possible_moves.append((pos[0]-1, pos[1]-1))

        # Right diagonal attack.
        if (pos[1] < 7 and Piece.is_enemy_piece(Piece.WHITE_PAWN, board.board_state[pos[0]-1][pos[1]+1])):
            possible_moves.append((pos[0]-1, pos[1]+1))

        # One move up.
        if (board.board_state[pos[0]-1][pos[1]] == Piece.NONE):
            possible_moves.append((pos[0]-1, pos[1]))

        # Two move from start.
        if (pos[0] == 6 and board.board_state[pos[0]-1][pos[1]] == Piece.NONE and
            board.board_state[pos[0]-2][pos[1]] == Piece.NONE):
            possible_moves.append((pos[0]-2, pos[1]))

        # Check for en-passant.
        # An enemy pawn should be on the left or right of this pawn position, and must have moved 2 squares in its movement.
        # Check left side pawn.
        if pos[1] > 0 and board.board_state[pos[0]][pos[1]-1] == Piece.BLACK_PAWN:
            # Check if the enemy pawn did move 2 squares in the last turn.
            if board.last_moved_piece == Piece.BLACK_PAWN and board.last_moved_piece_from[0] == pos[0]-2 and board.last_moved_piece_from[1] == pos[1]-1:
                # Check we didn't already add this left diagonal attack from above.
                if not (pos[0]-1, pos[1]-1) in possible_moves:
                    possible_moves.append((pos[0]-1, pos[1]-1))

        # Check right side pawn.
        if pos[1] < 7 and board.board_state[pos[0]][pos[1]+1] == Piece.BLACK_PAWN:
            # Check if the enemy pawn did move 2 squares in the last turn.
            if board.last_moved_piece == Piece.BLACK_PAWN and board.last_moved_piece_from[0] == pos[0]-2 and board.last_moved_piece_from[1] == pos[1]+1:
                # Check we didn't already add this right diagonal attack from above.
                if not (pos[0]-1, pos[1]+1) in possible_moves:
                    possible_moves.append((pos[0]-1, pos[1]+1))

        return possible_moves

    def moves_for_black_pawn(board, pos):
        possible_moves = []

        # Bottom of the board.
        if pos[0] == 7:
            return possible_moves

        # Left diagonal attack.
        if (pos[1] > 0 and Piece.is_enemy_piece(Piece.BLACK_PAWN, board.board_state[pos[0]+1][pos[1]-1])):
            possible_moves.append((pos[0]+1, pos[1]-1))

        # Right diagonal attack.
        if (pos[1] < 7 and Piece.is_enemy_piece(Piece.BLACK_PAWN, board.board_state[pos[0]+1][pos[1]+1])):
            possible_moves.append((pos[0]+1, pos[1]+1))

        # One move down.
        if (board.board_state[pos[0]+1][pos[1]] == Piece.NONE):
            possible_moves.append((pos[0]+1, pos[1]))

        # Two move from start.
        if (pos[0] == 1 and board.board_state[pos[0]+1][pos[1]] == Piece.NONE and
            board.board_state[pos[0]+2][pos[1]] == Piece.NONE):
            possible_moves.append((pos[0]+2, pos[1]))

        # Check for en-passant.
        # An enemy pawn should be on the left or right of this pawn position, and must have moved 2 squares in its movement.
        # Check left side pawn.
        if pos[1] > 0 and board.board_state[pos[0]][pos[1]-1] == Piece.WHITE_PAWN:
            # Check if the enemy pawn did move 2 squares in the last turn.
            if board.last_moved_piece == Piece.WHITE_PAWN and board.last_moved_piece_from[0] == pos[0]+2 and board.last_moved_piece_from[1] == pos[1]-1:
                # Check we didn't already add this left diagonal attack from above.
                if not (pos[0]+1, pos[1]-1) in possible_moves:
                    possible_moves.append((pos[0]+1, pos[1]-1))

        # Check right side pawn.
        if pos[1] < 7 and board.board_state[pos[0]][pos[1]+1] == Piece.WHITE_PAWN:
            # Check if the enemy pawn did move 2 squares in the last turn.
            if board.last_moved_piece == Piece.WHITE_PAWN and board.last_moved_piece_from[0] == pos[0]+2 and board.last_moved_piece_from[1] == pos[1]+1:
                # Check we didn't already add this right diagonal attack from above.
                if not (pos[0]+1, pos[1]+1) in possible_moves:
                    possible_moves.append((pos[0]+1, pos[1]+1))

        return possible_moves

    def moves_for_bishop(board, start):
        # Bishops move diagonally only.
        # It cant pass through its own pieces and stops at possible capture squares.
        piece = board.board_state[start[0]][start[1]]
        
        possible_moves = []
        
        # Go up-right.
        row = start[0] - 1
        col = start[1] + 1

        while row >= 0 and col <= 7:
            if board.board_state[row][col] == Piece.NONE:
                # Empty square.
                possible_moves.append((row, col))
            elif Piece.is_enemy_piece(piece, board.board_state[row][col]):
                # Capturable square.
                possible_moves.append((row, col))
                break
            else:
                # Can't move through your own pieces.
                break

            row -= 1
            col += 1
        
        # Go down-right.
        row = start[0] + 1
        col = start[1] + 1

        while row <= 7 and col <= 7:
            if board.board_state[row][col] == Piece.NONE:
                # Empty square.
                possible_moves.append((row, col))
            elif Piece.is_enemy_piece(piece, board.board_state[row][col]):
                # Capturable square.
                possible_moves.append((row, col))
                break
            else:
                # Can't move through your own pieces.
                break

            row += 1
            col += 1

        # Go up-left.
        row = start[0] - 1
        col = start[1] - 1

        while row >= 0 and col >= 0:
            if board.board_state[row][col] == Piece.NONE:
                # Empty square.
                possible_moves.append((row, col))
            elif Piece.is_enemy_piece(piece, board.board_state[row][col]):
                # Capturable square.
                possible_moves.append((row, col))
                break
            else:
                # Can't move through your own pieces.
                break

            row -= 1
            col -= 1

        # Go down-left.
        row = start[0] + 1
        col = start[1] - 1

        while row <= 7 and col >= 0:
            if board.board_state[row][col] == Piece.NONE:
                # Empty square.
                possible_moves.append((row, col))
            elif Piece.is_enemy_piece(piece, board.board_state[row][col]):
                # Capturable square.
                possible_moves.append((row, col))
                break
            else:
                # Can't move through your own pieces.
                break

            row += 1
            col -= 1

        return possible_moves

    def moves_for_knight(board, start):
        piece = board.board_state[start[0]][start[1]]       

        possible_moves = []

        try_moves = [
            (start[0] - 2, start[1] + 1),       # Top right
            (start[0] - 2, start[1] - 1),       # Top left
            (start[0] + 2, start[1] - 1),       # Bottom left
            (start[0] + 2, start[1] + 1),       # Bottom right
            (start[0] + 1, start[1] + 2),       # Right down
            (start[0] - 1, start[1] + 2),       # Right up
            (start[0] - 1, start[1] - 2),       # Left up
            (start[0] + 1, start[1] - 2),       # Left down
        ]

        for move in try_moves:
            row = move[0]
            col = move[1]
            is_in_bounds = row >= 0 and row <= 7 and col >= 0 and col <= 7

            if is_in_bounds and (board.board_state[row][col] == Piece.NONE or Piece.is_enemy_piece(piece, board.board_state[row][col])):
                possible_moves.append((row, col))

        return possible_moves

    def moves_for_rook(board, start):
        # Rooks move orthogonally only.
        # It cant pass through its own pieces and stops at possible capture squares.
        piece = board.board_state[start[0]][start[1]]
        
        possible_moves = []
        
        # Go right.
        row = start[0]
        col = start[1] + 1

        while col <= 7:
            if board.board_state[row][col] == Piece.NONE:
                # Empty square.
                possible_moves.append((row, col))
            elif Piece.is_enemy_piece(piece, board.board_state[row][col]):
                # Capturable square.
                possible_moves.append((row, col))
                break
            else:
                # Can't move through your own pieces.
                break

            col += 1

        # Go left.
        row = start[0]
        col = start[1] - 1

        while col >= 0:
            if board.board_state[row][col] == Piece.NONE:
                # Empty square.
                possible_moves.append((row, col))
            elif Piece.is_enemy_piece(piece, board.board_state[row][col]):
                # Capturable square.
                possible_moves.append((row, col))
                break
            else:
                # Can't move through your own pieces.
                break

            col -= 1

        # Go up.
        row = start[0] - 1
        col = start[1]

        while row >= 0:
            if board.board_state[row][col] == Piece.NONE:
                # Empty square.
                possible_moves.append((row, col))
            elif Piece.is_enemy_piece(piece, board.board_state[row][col]):
                # Capturable square.
                possible_moves.append((row, col))
                break
            else:
                # Can't move through your own pieces.
                break

            row -= 1

        # Go down.
        row = start[0] + 1
        col = start[1]

        while row <= 7:
            if board.board_state[row][col] == Piece.NONE:
                # Empty square.
                possible_moves.append((row, col))
            elif Piece.is_enemy_piece(piece, board.board_state[row][col]):
                # Capturable square.
                possible_moves.append((row, col))
                break
            else:
                # Can't move through your own pieces.
                break

            row += 1

        return possible_moves
    
    def moves_for_queen(board, start):
        # Queens behave just like a bishop+rook.
        return PieceMoves.moves_for_bishop(board, start) + PieceMoves.moves_for_rook(board, start)

    def moves_for_king(board, start, disable_castling = False):
        # Kings move 1 space.
        # Kings can capture.
        
        # disable_castling prevents an endless loop when figuring out if a king can castle when checking if its squares are under attack
        # from all the possible moves that can happen with the opponent. If disable_castling was disabled, the opponent would also check for castling
        # during its valid move generation which it also needs to ask, are my squares under attack? Which triggers another castle check on
        # the opposites colour and so on. So when validating these squares, a castle movement from the opponent doesn't threaten the squares
        # at all, so it doesn't need to be done when a side is checking if it can castle.

        piece = board.board_state[start[0]][start[1]]

        possible_moves = []

        try_moves = [
            (start[0], start[1] + 1),           # Right
            (start[0], start[1] - 1),           # Left
            (start[0] - 1, start[1]),           # Up
            (start[0] + 1, start[1]),           # Down
            (start[0] - 1, start[1] + 1),       # Top Right
            (start[0] - 1, start[1] - 1),       # Top Left
            (start[0] + 1, start[1] + 1),       # Bottom Right
            (start[0] + 1, start[1] - 1)        # Bottom Left
        ]

        for move in try_moves:
            row = move[0]
            col = move[1]
            is_in_bounds = row >= 0 and row <= 7 and col >= 0 and col <= 7
    
            if is_in_bounds and (board.board_state[row][col] == Piece.NONE or Piece.is_enemy_piece(piece, board.board_state[row][col])):
                possible_moves.append((row, col))

        # Check castling movements.
        if not disable_castling:
            if piece == Piece.WHITE_KING and not board.white_king_moved:
                # Check white king castling options.
                # King side.
                if (not board.white_king_side_rook_moved and
                    board.board_state[7][5] == Piece.NONE and
                    board.board_state[7][6] == Piece.NONE and
                    not PieceMoves._is_square_under_attack(board, (7, 5), False) and
                    not PieceMoves._is_square_under_attack(board, (7, 6), False)):
                    
                    # Allow the castle to king side.
                    possible_moves.append((7, 6))

                # Queen side.
                if (not board.white_queen_side_rook_moved and
                    board.board_state[7][2] == Piece.NONE and
                    board.board_state[7][3] == Piece.NONE and
                    not PieceMoves._is_square_under_attack(board, (7, 2), False) and
                    not PieceMoves._is_square_under_attack(board, (7, 3), False)):
                    
                    # Allow the castle to queen side.
                    possible_moves.append((7, 2))
            
            if piece == Piece.BLACK_KING and not board.black_king_moved:
                # Check black kings castling options.
                if (not board.black_king_side_rook_moved and
                    board.board_state[0][5] == Piece.NONE and
                    board.board_state[0][6] == Piece.NONE and
                    not PieceMoves._is_square_under_attack(board, (0, 5), True) and
                    not PieceMoves._is_square_under_attack(board, (0, 6), True)):
                    
                    # Allow the castle to king side.
                    possible_moves.append((0, 6))

                # Queen side.
                if (not board.black_queen_side_rook_moved and
                    board.board_state[0][2] == Piece.NONE and
                    board.board_state[0][3] == Piece.NONE and
                    not PieceMoves._is_square_under_attack(board, (0, 2), True) and
                    not PieceMoves._is_square_under_attack(board, (0, 3), True)):
                    
                    # Allow the castle to queen side.
                    possible_moves.append((0, 2))

        return possible_moves

    # Returns true if the target square is under attack by the specified attacking pieces.
    def _is_square_under_attack(board, target_square, white_attacking):
        # Loop over the attackers pieces, and test if the square is in one of their target movement squares.
        for row in range(0, 8):
            for col in range(0, 8):
                piece = board.board_state[row][col]
                
                if piece == Piece.NONE:
                    continue
                if white_attacking and Piece.is_black_piece(piece):
                    continue
                if not white_attacking and Piece.is_white_piece(piece):
                    continue

                moves = PieceMoves.get_moves_for_piece(board, piece, (row, col), True)
                if target_square in moves:
                    return True

        return False