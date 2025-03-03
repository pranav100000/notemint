import os
import tempfile
from pathlib import Path

from app.core.config import Settings


def test_settings_initialization():
    """Test settings initialization with default values"""
    settings = Settings()
    
    assert settings.API_V1_STR == "/api/v1"
    assert settings.CORS_ORIGINS == ["*"]
    assert isinstance(settings.MIDI_FILES_DIR, Path)
    assert os.path.exists(settings.MIDI_FILES_DIR)


def test_settings_custom_midi_dir():
    """Test settings with custom MIDI files directory"""
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = os.path.join(temp_dir, "custom_midi_dir")
        
        # Directory shouldn't exist yet
        assert not os.path.exists(test_dir)
        
        # Initialize settings with custom dir
        settings = Settings(MIDI_FILES_DIR=Path(test_dir))
        
        # Directory should be created
        assert os.path.exists(test_dir)
        assert settings.MIDI_FILES_DIR == Path(test_dir)