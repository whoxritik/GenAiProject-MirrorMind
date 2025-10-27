import streamlit as st
from gtts import gTTS
import pygame
import io
import tempfile
import os
import threading
import time
from typing import Optional

class VoiceHandler:
    """
    Handle text-to-speech functionality for the smart mirror
    """
    
    def __init__(self):
        self.is_speaking = False
        self.current_audio_thread = None
        
        # Initialize pygame mixer for audio playback
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)
        except pygame.error as e:
            print(f"Error initializing pygame mixer: {e}")
    
    def speak_text(self, text: str, language: str = 'en') -> bool:
        """
        Convert text to speech and play it
        
        Args:
            text: Text to speak
            language: Language code ('en' for English, 'hi' for Hindi)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Stop any current speech
            self.stop_speaking()
            
            # Set speaking flag
            self.is_speaking = True
            
            # Generate speech in a separate thread
            self.current_audio_thread = threading.Thread(
                target=self._generate_and_play_audio,
                args=(text, language),
                daemon=True
            )
            self.current_audio_thread.start()
            
            return True
            
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
            self.is_speaking = False
            return False
    
    def _generate_and_play_audio(self, text: str, language: str):
        """
        Generate audio and play it (runs in separate thread)
        """
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Use temporary file for audio
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts.save(tmp_file.name)
                
                # Load and play audio with pygame
                try:
                    if pygame.mixer.get_init():
                        pygame.mixer.music.load(tmp_file.name)
                        pygame.mixer.music.play()
                        
                        # Wait for audio to finish
                        while pygame.mixer.music.get_busy() and self.is_speaking:
                            time.sleep(0.1)
                    else:
                        print("Pygame mixer not initialized, skipping audio playback")
                        # Simulate audio duration for consistent behavior
                        time.sleep(len(text) * 0.1)  # Rough estimate
                        
                except pygame.error as e:
                    print(f"Error playing audio: {e}")
                
                finally:
                    # Clean up temporary file
                    try:
                        os.unlink(tmp_file.name)
                    except OSError:
                        pass
            
        except Exception as e:
            print(f"Error generating audio: {e}")
        
        finally:
            self.is_speaking = False
    
    def stop_speaking(self):
        """Stop current speech playback"""
        try:
            self.is_speaking = False
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
        except pygame.error:
            pass
    
    def is_currently_speaking(self) -> bool:
        """Check if currently speaking"""
        try:
            return self.is_speaking and pygame.mixer.music.get_busy()
        except pygame.error:
            # If mixer not initialized, just return the flag state
            return self.is_speaking
    
    def speak_bilingual(self, english_text: str, hindi_text: str, delay_between: float = 1.0):
        """
        Speak both English and Hindi text with a delay
        
        Args:
            english_text: English text to speak
            hindi_text: Hindi text to speak  
            delay_between: Delay in seconds between the two speeches
        """
        def _speak_both():
            # Speak English first
            self.speak_text(english_text, 'en')
            
            # Wait for English to finish
            while self.is_currently_speaking():
                time.sleep(0.1)
            
            # Small delay
            time.sleep(delay_between)
            
            # Speak Hindi
            self.speak_text(hindi_text, 'hi')
        
        # Run in separate thread
        threading.Thread(target=_speak_both, daemon=True).start()
    
    def get_voice_status(self) -> dict:
        """
        Get current voice status for UI
        
        Returns:
            Dictionary with voice status information
        """
        try:
            mixer_init = pygame.mixer.get_init() is not None
        except pygame.error:
            mixer_init = False
            
        return {
            'is_speaking': self.is_currently_speaking(),
            'mixer_initialized': mixer_init
        }