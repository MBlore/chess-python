# --------------------------------------------------------------------------------------------------------
# Chess with PyGame
# Created by Martin Blore 2023
# Full explanation can be found at https://codewithmartin.io/articles/how-to-code-a-chess-game-in-python
# --------------------------------------------------------------------------------------------------------
import pygame
from piece import Piece
from images import Images

class BoardRender:
    def draw_pieces(board, screen, images: Images):
        for row_index, row in enumerate(board.board_state):
            for col_index, col in enumerate(row):
                # Dont draw hidden cells.
                if (row_index == board.hide_row_index and col_index == board.hide_col_index):
                    continue

                # Draw pieces.
                if (row[col_index] != Piece.NONE):
                    xpos = board.board_start_x + (board.cell_size * col_index)
                    ypos = board.board_start_y + (board.cell_size * row_index)

                    img = images.get_image_for_piece(row[col_index])
                    screen.blit(img, (xpos, ypos))

        BoardRender._draw_drag_piece(board, screen, images)

    def _draw_drag_piece(board, screen, images):
        # Draw dragging piece.
        if (board.dragging_piece != Piece.NONE):
            mouse_pos = pygame.mouse.get_pos()
            img = images.get_image_for_piece(board.dragging_piece)
            screen.blit(img, (mouse_pos[0]-(board.cell_size/2), mouse_pos[1]-(board.cell_size/2)))

    def draw_board(board, screen):
        white_square = True

        # Draw the board, starting with the cell column, and then draw each cell going down.
        for x in range(0, 8):
            # If the X cell index is divisble by 2, we start drawing white squares.
            if x % 2 == 0:
                white_square = True
            else:
                white_square = False

            # Now for this X cell index, we start drawing the column going down.
            for y in range(0, 8):

                # Lets calculate the position of our rectangle depending on the X/Y of the cell we're drawing.
                xpos = board.board_start_x + (x * board.cell_size)
                ypos = board.board_start_y + (y * board.cell_size)

                # Draw the square.
                if (white_square == True):
                    pygame.draw.rect(screen, board.white_square_color,
                                    pygame.Rect(xpos, ypos, board.cell_size, board.cell_size))
                else:
                    pygame.draw.rect(screen, board.black_square_color,
                                    pygame.Rect(xpos, ypos, board.cell_size, board.cell_size))

                # Flip our white square flag, so our next square will be the opposite color.
                white_square = not white_square