import pygame
import os

class Player:
    def __init__(self):
        self.tracks = []
        self.index = 0
        self.is_playing = False

        for file in os.listdir("music"):
            if file.endswith(".mp3"):
                self.tracks.append("music/" + file)

    def play(self):
        if len(self.tracks) == 0:
            print("No music found")
            return

        pygame.mixer.music.load(self.tracks[self.index])
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next(self):
        if len(self.tracks) == 0:
            return

        self.index += 1
        if self.index >= len(self.tracks):
            self.index = 0

        self.play()

    def prev(self):
        if len(self.tracks) == 0:
            return

        self.index -= 1
        if self.index < 0:
            self.index = len(self.tracks) - 1

        self.play()

    def current(self):
        if len(self.tracks) == 0:
            return "No track"

        return self.tracks[self.index].split("/")[-1]