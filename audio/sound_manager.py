import pygame
import os

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music_playing = False
        self.volume = 0.7
        
        # Load sound effects
        self.load_sounds()
        
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