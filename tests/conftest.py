import os
import pytest
import tempfile
from pathlib import Path

from app.core.config import settings
from app.models.composition import CompositionData


@pytest.fixture(scope="function")
def temp_midi_dir():
    """Create a temporary directory for MIDI files during tests"""
    with tempfile.TemporaryDirectory() as temp_dir:
        original_dir = settings.MIDI_FILES_DIR
        settings.MIDI_FILES_DIR = Path(temp_dir)
        yield temp_dir
        settings.MIDI_FILES_DIR = original_dir


@pytest.fixture
def sample_composition_data():
    """Sample composition data for testing"""
    return CompositionData(
        title="Test Composition",
        tempo=120,
        time_signature="4/4",
        key="C",
        scale="major",
        length_bars=4,
        sections=[
            {
                "name": "Main",
                "bars": 4,
                "tracks": [
                    {
                        "instrument": "piano",
                        "midi_program": 0,
                        "notes": [
                            {"pitch": 60, "start_time": 0.0, "duration": 1.0, "velocity": 80},
                            {"pitch": 64, "start_time": 1.0, "duration": 1.0, "velocity": 80},
                            {"pitch": 67, "start_time": 2.0, "duration": 1.0, "velocity": 80},
                            {"pitch": 72, "start_time": 3.0, "duration": 1.0, "velocity": 80}
                        ]
                    }
                ]
            }
        ]
    )


@pytest.fixture
def complex_composition_data():
    """More complex composition data for testing edge cases"""
    return CompositionData(
        title="Complex Test Composition",
        tempo=140,
        time_signature="3/4",
        key="F",
        scale="minor",
        length_bars=8,
        sections=[
            {
                "name": "Intro",
                "bars": 4,
                "tracks": [
                    {
                        "instrument": "piano",
                        "midi_program": 0,
                        "notes": [
                            {"pitch": 53, "start_time": 0.0, "duration": 0.5, "velocity": 90},
                            {"pitch": 57, "start_time": 0.5, "duration": 0.5, "velocity": 90},
                            {"pitch": 60, "start_time": 1.0, "duration": 0.5, "velocity": 90},
                            {"pitch": 65, "start_time": 1.5, "duration": 0.5, "velocity": 90}
                        ]
                    },
                    {
                        "instrument": "bass",
                        "midi_program": 32,
                        "notes": [
                            {"pitch": 41, "start_time": 0.0, "duration": 1.0, "velocity": 100},
                            {"pitch": 41, "start_time": 1.0, "duration": 1.0, "velocity": 100}
                        ]
                    }
                ]
            },
            {
                "name": "Chorus",
                "bars": 4,
                "tracks": [
                    {
                        "instrument": "piano",
                        "midi_program": 0,
                        "notes": [
                            {"pitch": 60, "start_time": 2.0, "duration": 1.0, "velocity": 90},
                            {"pitch": 64, "start_time": 3.0, "duration": 1.0, "velocity": 90}
                        ]
                    },
                    {
                        "instrument": "strings",
                        "midi_program": 48,
                        "notes": [
                            {"pitch": 72, "start_time": 2.0, "duration": 2.0, "velocity": 70}
                        ]
                    }
                ]
            }
        ]
    )


@pytest.fixture
def sample_composition_request():
    """Sample composition request for API testing"""
    return {
        "composition": {
            "title": "Test Composition",
            "tempo": 120,
            "time_signature": "4/4",
            "key": "C",
            "scale": "major",
            "length_bars": 4,
            "sections": [
                {
                    "name": "Main",
                    "bars": 4,
                    "tracks": [
                        {
                            "instrument": "piano",
                            "midi_program": 0,
                            "notes": [
                                {"pitch": 60, "start_time": 0.0, "duration": 1.0, "velocity": 80},
                                {"pitch": 64, "start_time": 1.0, "duration": 1.0, "velocity": 80},
                                {"pitch": 67, "start_time": 2.0, "duration": 1.0, "velocity": 80},
                                {"pitch": 72, "start_time": 3.0, "duration": 1.0, "velocity": 80}
                            ]
                        }
                    ]
                }
            ]
        }
    }