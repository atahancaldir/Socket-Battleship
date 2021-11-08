from playsound import playsound
import os

class Player():
    def __init__(self):
        self.bomb_sound = os.path.join(os.getcwd(), "bomb_sound.mp3")