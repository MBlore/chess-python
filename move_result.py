# --------------------------------------------------------------------------------------------------------
# Chess with PyGame
# Created by Martin Blore 2023
# Full explanation can be found at https://codewithmartin.io/articles/how-to-code-a-chess-game-in-python
# --------------------------------------------------------------------------------------------------------

# This object communicates the move result from the board engine.
class MoveResult:
    def __init__(self):
        # If false, the move is not legal.
        self.move_performed = False
        
        # If this is true, the move put the opponent player in check.
        self.opponent_now_in_check = False

        # If this is true, the move was denied because it puts you in check.
        self.move_denied_self_check = False

        # Set to true when the opponent is now in check mate.
        self.opponent_check_mate = False

        # Set to true when the opponent is now in stale mate.
        self.opponent_stale_mate = False

        # Set to true if a pawn is now available to be promoted.
        self.promote_available = False

        # The position of the pawn that can be promoted.
        self.promote_position = (0,0)
        