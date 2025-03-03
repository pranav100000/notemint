import os
import pytest
import json
from fastapi.testclient import TestClient
import pretty_midi

from app.main import app
from app.models.composition import CompositionData
from app.utils.midi_generator import MidiGenerator

client = TestClient(app)


def test_multi_section_composition(temp_midi_dir):
    """Test a composition with multiple sections"""
    # Create a composition with multiple sections
    request_data = {
        "composition": {
            "title": "Multi-Section Test",
            "tempo": 120,
            "time_signature": "4/4",
            "key": "C",
            "scale": "major",
            "length_bars": 8,
            "sections": [
                {
                    "name": "Intro",
                    "bars": 4,
                    "tracks": [
                        {
                            "instrument": "piano",
                            "midi_program": 0,
                            "notes": [
                                {"pitch": 60, "start_time": 0.0, "duration": 1.0, "velocity": 80},
                                {"pitch": 64, "start_time": 1.0, "duration": 1.0, "velocity": 80}
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
                                {"pitch": 67, "start_time": 4.0, "duration": 1.0, "velocity": 80},
                                {"pitch": 72, "start_time": 5.0, "duration": 1.0, "velocity": 80}
                            ]
                        }
                    ]
                }
            ]
        }
    }
    
    # Generate composition
    response = client.post("/api/v1/compositions/generate", json=request_data)
    assert response.status_code == 201
    data = response.json()
    
    # Verify the MIDI file
    midi = pretty_midi.PrettyMIDI(data["file_path"])
    assert len(midi.instruments) == 1
    assert len(midi.instruments[0].notes) == 4  # Total notes from both sections


def test_multiple_instruments(temp_midi_dir):
    """Test a composition with multiple instruments in a single section"""
    request_data = {
        "composition": {
            "title": "Multi-Instrument Test",
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
                                {"pitch": 64, "start_time": 1.0, "duration": 1.0, "velocity": 80}
                            ]
                        },
                        {
                            "instrument": "bass",
                            "midi_program": 32,
                            "notes": [
                                {"pitch": 36, "start_time": 0.0, "duration": 2.0, "velocity": 100}
                            ]
                        },
                        {
                            "instrument": "drums",
                            "midi_program": 0,
                            "notes": [
                                {"pitch": 36, "start_time": 0.0, "duration": 0.25, "velocity": 100},
                                {"pitch": 36, "start_time": 1.0, "duration": 0.25, "velocity": 100}
                            ]
                        }
                    ]
                }
            ]
        }
    }
    
    # Generate composition
    response = client.post("/api/v1/compositions/generate", json=request_data)
    assert response.status_code == 201
    data = response.json()
    
    # Verify the MIDI file
    midi = pretty_midi.PrettyMIDI(data["file_path"])
    assert len(midi.instruments) == 3
    
    # Check that the instruments have the correct number of notes
    piano = next(i for i in midi.instruments if i.name == "piano")
    bass = next(i for i in midi.instruments if i.name == "bass")
    drums = next(i for i in midi.instruments if i.name == "drums")
    
    assert len(piano.notes) == 2
    assert len(bass.notes) == 1
    assert len(drums.notes) == 2


def test_empty_composition(temp_midi_dir):
    """Test a composition with no notes"""
    request_data = {
        "composition": {
            "title": "Empty Composition",
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
                            "notes": []
                        }
                    ]
                }
            ]
        }
    }
    
    # Generate composition
    response = client.post("/api/v1/compositions/generate", json=request_data)
    assert response.status_code == 201
    data = response.json()
    
    # Verify the MIDI file
    midi = pretty_midi.PrettyMIDI(data["file_path"])
    # Our implementation skips empty instruments
    assert len(midi.instruments) == 0


def test_invalid_request_handling(temp_midi_dir):
    """Test handling invalid requests"""
    # Missing required field
    invalid_request = {
        "composition": {
            # Missing title
            "tempo": 120,
            "time_signature": "4/4",
            "key": "C",
            "scale": "major",
            "length_bars": 4,
            "sections": []
        }
    }
    
    response = client.post("/api/v1/compositions/generate", json=invalid_request)
    assert response.status_code == 422  # Validation error
    
    # Invalid values
    invalid_request = {
        "composition": {
            "title": "Invalid Values",
            "tempo": -120,  # Negative tempo
            "time_signature": "4/4",
            "key": "C",
            "scale": "major",
            "length_bars": 4,
            "sections": []
        }
    }
    
    response = client.post("/api/v1/compositions/generate", json=invalid_request)
    assert response.status_code == 422  # Validation error


def test_overlapping_notes(temp_midi_dir):
    """Test a composition with overlapping notes"""
    request_data = {
        "composition": {
            "title": "Overlapping Notes",
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
                                {"pitch": 60, "start_time": 0.0, "duration": 2.0, "velocity": 80},
                                {"pitch": 64, "start_time": 0.5, "duration": 1.0, "velocity": 80},
                                {"pitch": 67, "start_time": 1.0, "duration": 1.5, "velocity": 80}
                            ]
                        }
                    ]
                }
            ]
        }
    }
    
    # Generate composition
    response = client.post("/api/v1/compositions/generate", json=request_data)
    assert response.status_code == 201
    data = response.json()
    
    # Verify the MIDI file has all notes despite overlaps
    midi = pretty_midi.PrettyMIDI(data["file_path"])
    assert len(midi.instruments) == 1
    assert len(midi.instruments[0].notes) == 3
    
    # Check that the notes have the correct durations
    notes = sorted(midi.instruments[0].notes, key=lambda n: n.start)
    assert notes[0].end - notes[0].start == 2.0
    assert notes[1].end - notes[1].start == 1.0
    assert notes[2].end - notes[2].start == 1.5


def test_extreme_values(temp_midi_dir):
    """Test a composition with extreme but valid values"""
    request_data = {
        "composition": {
            "title": "Extreme Values",
            "tempo": 500,  # Very fast tempo
            "time_signature": "7/8",  # Unusual time signature
            "key": "F#",
            "scale": "diminished",
            "length_bars": 100,  # Long composition
            "sections": [
                {
                    "name": "Main",
                    "bars": 100,
                    "tracks": [
                        {
                            "instrument": "violin",
                            "midi_program": 40,
                            "notes": [
                                {"pitch": 127, "start_time": 0.0, "duration": 0.01, "velocity": 127},  # Extremely high note, short duration, max velocity
                                {"pitch": 0, "start_time": 0.5, "duration": 10.0, "velocity": 1}  # Extremely low note, long duration, min velocity
                            ]
                        }
                    ]
                }
            ]
        }
    }
    
    # Generate composition
    response = client.post("/api/v1/compositions/generate", json=request_data)
    assert response.status_code == 201
    data = response.json()
    
    # Verify the MIDI file
    midi = pretty_midi.PrettyMIDI(data["file_path"])
    assert len(midi.instruments) == 1
    assert len(midi.instruments[0].notes) == 2
    
    # Check extreme tempo (allow for floating point imprecision)
    assert abs(midi.get_tempo_changes()[1][0] - 500) < 0.1