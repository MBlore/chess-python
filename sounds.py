# --------------------------------------------------------------------------------------------------------
# Chess with PyGame
# Created by Martin Blore 2023
# Full explanation can be found at https://codewithmartin.io/articles/how-to-code-a-chess-game-in-python
# --------------------------------------------------------------------------------------------------------

import os
import pygame

class Sounds():
    def init(self):
        location = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        self.move_sound = pygame.mixer.Sound(os.path.join(location, "sounds\\move.wav"))
        self.check_sound = pygame.mixer.Sound(os.path.join(location, "sounds\\check.wav"))
        self.check_mate_sound = pygame.mixer.Sound(os.path.join(location, "sounds\\check_mate.wav"))

    def play_move(self):
        self.move_sound.play()

    def play_check(self):
        self.check_sound.play()

    def play_check_mate(self):
        self.check_mate_sound.play()