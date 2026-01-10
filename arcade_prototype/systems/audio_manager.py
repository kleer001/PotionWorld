"""
Audio manager for music and sound effects.
"""
import arcade
from typing import Dict, Optional
from pathlib import Path
from systems.game_events import GameEvents


class AudioManager:
    """
    Singleton audio manager for music and sound effects.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        # Current music
        self.current_music: Optional[arcade.Sound] = None
        self.current_music_player: Optional[arcade.media.Player] = None
        self.current_music_name: str = ""

        # Sound cache
        self.sounds: Dict[str, arcade.Sound] = {}

        # Volume settings
        self.music_volume: float = 0.5
        self.sfx_volume: float = 0.7

        # Event system
        self.events = GameEvents()

        # Subscribe to audio events
        self.events.subscribe("music_change_requested", self.on_music_change_requested)
        self.events.subscribe("sfx_requested", self.on_sfx_requested)

    def play_music(self, music_name: str, loop: bool = True, fade_duration: float = 1.0) -> None:
        """
        Play music track.

        Args:
            music_name: Name of the music file (without extension)
            loop: Whether to loop the music
            fade_duration: Fade transition time in seconds (not implemented yet)
        """
        # Don't restart if already playing
        if self.current_music_name == music_name and self.current_music_player:
            return

        # Stop current music
        self.stop_music()

        # Load and play new music
        try:
            music_path = f"assets/audio/music/{music_name}.ogg"

            # Check if file exists
            if not Path(music_path).exists():
                print(f"⚠️ Music file not found: {music_path} (using placeholder)")
                return

            self.current_music = arcade.load_sound(music_path, streaming=True)
            self.current_music_player = self.current_music.play(
                volume=self.music_volume,
                loop=loop
            )
            self.current_music_name = music_name

            print(f"🎵 Playing music: {music_name}")

        except Exception as e:
            print(f"❌ Failed to play music '{music_name}': {e}")

    def stop_music(self) -> None:
        """Stop current music."""
        if self.current_music_player:
            self.current_music_player.pause()
            self.current_music_player = None
            self.current_music = None
            self.current_music_name = ""

    def set_music_volume(self, volume: float) -> None:
        """Set music volume (0.0 to 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.current_music_player:
            self.current_music_player.volume = self.music_volume

    def play_sfx(self, sfx_name: str, volume: float = 1.0) -> None:
        """
        Play sound effect.

        Args:
            sfx_name: Name of the sound file (without extension)
            volume: Volume multiplier (0.0 to 1.0)
        """
        try:
            # Load from cache or file
            if sfx_name not in self.sounds:
                sfx_path = f"assets/audio/sfx/{sfx_name}.wav"

                # Check if file exists
                if not Path(sfx_path).exists():
                    print(f"⚠️ SFX file not found: {sfx_path}")
                    return

                self.sounds[sfx_name] = arcade.load_sound(sfx_path)

            # Play sound
            self.sounds[sfx_name].play(volume=self.sfx_volume * volume)

        except Exception as e:
            print(f"❌ Failed to play SFX '{sfx_name}': {e}")

    def set_sfx_volume(self, volume: float) -> None:
        """Set SFX volume (0.0 to 1.0)."""
        self.sfx_volume = max(0.0, min(1.0, volume))

    # Event handlers

    def on_music_change_requested(self, music_name: str) -> None:
        """Handle music change event."""
        self.play_music(music_name)

    def on_sfx_requested(self, sfx_name: str, volume: float = 1.0) -> None:
        """Handle SFX event."""
        self.play_sfx(sfx_name, volume)

    # Auto-reactions to game events (optional)

    def setup_auto_reactions(self) -> None:
        """Set up automatic audio reactions to game events."""
        self.events.subscribe("ingredient_gathered", lambda **kwargs: self.play_sfx("gather", 0.5))
        self.events.subscribe("potion_crafted", lambda **kwargs: self.play_sfx("craft_success", 0.8))
        self.events.subscribe("crafting_failed", lambda **kwargs: self.play_sfx("craft_fail", 0.6))
        self.events.subscribe("stat_increased", lambda **kwargs: self.play_sfx("level_up", 0.7))
        self.events.subscribe("notification_requested", lambda **kwargs: self.play_sfx("notification", 0.3))
