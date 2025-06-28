import pygame
import os

_muted = False
_mixer_available = False
SOUNDS = {}

try:
    pygame.mixer.init()
    _mixer_available = True
except pygame.error:
    print("⚠️ Pygame mixer not available. Sound disabled.")

def init_sounds(path):
    global SOUNDS
    if not _mixer_available:
        return
    names = ["click", "eat", "gameover", "pause"]
    for name in names:
        file = os.path.join(path, f"{name}.wav")
        if os.path.exists(file):
            SOUNDS[name] = pygame.mixer.Sound(file)

def play(name):
    if _mixer_available and not _muted and name in SOUNDS:
        SOUNDS[name].play()

def toggle_mute():
    global _muted
    _muted = not _muted
    return _muted
