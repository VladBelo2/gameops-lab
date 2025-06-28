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

def init_sounds(base_path):
    global SOUNDS
    if not _mixer_available:
        return
    sound_names = [
        "click_fun", "pause_fun", "level_up_fun", "win_fun",
        "bounce", "break", "gameover_fun"
    ]
    for name in sound_names:
        path = os.path.join(base_path, f"{name}.wav")
        if os.path.exists(path):
            SOUNDS[name] = pygame.mixer.Sound(path)

def play(name):
    if _mixer_available and not _muted and name in SOUNDS:
        SOUNDS[name].play()

def toggle_mute():
    global _muted
    _muted = not _muted
    return _muted

def is_muted():
    return _muted
