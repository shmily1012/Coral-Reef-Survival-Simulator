import pygame
import os

"""
Sound Manager Module

Handles all audio aspects of the game, including sound effects and background music.
Manages loading, playing, and volume control of various audio elements.

Features:
- Background music management
- Sound effect handling
- Volume control
- Warning sound system
- Error handling for missing audio files
"""

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music_playing = False
        self.volume = 0.7
        
        # Load sound effects
        self.load_sounds()
        try:
            self.warning_sound = pygame.mixer.Sound("assets/audio/warning.wav")
        except:
            self.warning_sound = None
            print("Warning: Could not load warning sound")
        self.warning_played = False
        
    def load_sounds(self):
        sound_files = {
            "bubble": "bubble.wav",
            "splash": "splash.wav",
            "alert": "alert.wav",
            "success": "success.wav",
            "fail": "fail.wav"
        }
        
        for sound_name, filename in sound_files.items():
            try:
                path = os.path.join("assets", "sounds", filename)
                self.sounds[sound_name] = pygame.mixer.Sound(path)
                self.sounds[sound_name].set_volume(self.volume)
            except:
                print(f"Warning: Could not load sound {filename}")
                
    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
            
    def play_background_music(self):
        try:
            pygame.mixer.music.load(os.path.join("assets", "sounds", "ocean_ambient.mp3"))
            pygame.mixer.music.set_volume(self.volume * 0.5)
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            self.music_playing = True
        except:
            print("Warning: Could not load background music")
            
    def stop_background_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False
        
    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume)
        if self.music_playing:
            pygame.mixer.music.set_volume(self.volume * 0.5) 
            
    def play_warning(self):
        if not self.warning_played:
            if self.warning_sound:
                self.warning_sound.play()
            else:
                print("Warning: No warning sound loaded")
            
            self.warning_played = True
    def reset_warning(self):
        self.warning_played = False 