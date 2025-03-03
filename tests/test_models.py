import pytest
from pydantic import ValidationError

from app.models.composition import (
    Note, Track, Section, CompositionData, 
    CompositionRequest, CompositionResponse
)


def test_note_model_validation():
    """Test Note model validation"""
    # Valid note
    note = Note(pitch=60, start_time=0.0, duration=1.0, velocity=80)
    assert note.pitch == 60
    assert note.start_time == 0.0
    assert note.duration == 1.0
    assert note.velocity == 80
    
    # Invalid pitch (too high)
    with pytest.raises(ValidationError):
        Note(pitch=128, start_time=0.0, duration=1.0, velocity=80)
    
    # Invalid velocity (too high)
    with pytest.raises(ValidationError):
        Note(pitch=60, start_time=0.0, duration=1.0, velocity=128)
    
    # Invalid velocity (negative)
    with pytest.raises(ValidationError):
        Note(pitch=60, start_time=0.0, duration=1.0, velocity=-1)


def test_track_model_validation():
    """Test Track model validation"""
    # Valid track
    track = Track(
        instrument="piano",
        midi_program=0,
        notes=[
            Note(pitch=60, start_time=0.0, duration=1.0, velocity=80),
            Note(pitch=64, start_time=1.0, duration=1.0, velocity=80)
        ]
    )
    assert track.instrument == "piano"
    assert track.midi_program == 0
    assert len(track.notes) == 2
    
    # Invalid midi_program (too high)
    with pytest.raises(ValidationError):
        Track(
            instrument="piano",
            midi_program=128,
            notes=[
                Note(pitch=60, start_time=0.0, duration=1.0, velocity=80)
            ]
        )


def test_section_model_validation():
    """Test Section model validation"""
    # Valid section
    section = Section(
        name="Main",
        bars=4,
        tracks=[
            Track(
                instrument="piano",
                midi_program=0,
                notes=[
                    Note(pitch=60, start_time=0.0, duration=1.0, velocity=80)
                ]
            )
        ]
    )
    assert section.name == "Main"
    assert section.bars == 4
    assert len(section.tracks) == 1
    
    # Invalid bars (zero or negative)
    with pytest.raises(ValidationError):
        Section(
            name="Main",
            bars=0,
            tracks=[
                Track(
                    instrument="piano",
                    midi_program=0,
                    notes=[
                        Note(pitch=60, start_time=0.0, duration=1.0, velocity=80)
                    ]
                )
            ]
        )


def test_composition_data_validation():
    """Test CompositionData model validation"""
    # Valid composition data
    composition_data = CompositionData(
        title="Test Composition",
        tempo=120,
        time_signature="4/4",
        key="C",
        scale="major",
        length_bars=4,
        sections=[
            Section(
                name="Main",
                bars=4,
                tracks=[
                    Track(
                        instrument="piano",
                        midi_program=0,
                        notes=[
                            Note(pitch=60, start_time=0.0, duration=1.0, velocity=80)
                        ]
                    )
                ]
            )
        ]
    )
    assert composition_data.title == "Test Composition"
    assert composition_data.tempo == 120
    assert composition_data.time_signature == "4/4"
    
    # Invalid tempo (zero or negative)
    with pytest.raises(ValidationError):
        CompositionData(
            title="Test Composition",
            tempo=0,
            time_signature="4/4",
            key="C",
            scale="major",
            length_bars=4,
            sections=[
                Section(
                    name="Main",
                    bars=4,
                    tracks=[
                        Track(
                            instrument="piano",
                            midi_program=0,
                            notes=[
                                Note(pitch=60, start_time=0.0, duration=1.0, velocity=80)
                            ]
                        )
                    ]
                )
            ]
        )


def test_composition_request_validation():
    """Test CompositionRequest model validation"""
    # Valid composition request
    composition_request = CompositionRequest(
        composition=CompositionData(
            title="Test Composition",
            tempo=120,
            time_signature="4/4",
            key="C",
            scale="major",
            length_bars=4,
            sections=[
                Section(
                    name="Main",
                    bars=4,
                    tracks=[
                        Track(
                            instrument="piano",
                            midi_program=0,
                            notes=[
                                Note(pitch=60, start_time=0.0, duration=1.0, velocity=80)
                            ]
                        )
                    ]
                )
            ]
        )
    )
    assert composition_request.composition.title == "Test Composition"


def test_composition_response_validation():
    """Test CompositionResponse model validation"""
    # Valid composition response
    composition_response = CompositionResponse(
        id="test-id",
        title="Test Composition",
        file_path="/path/to/midi/file.mid",
        created_at="2023-01-01T12:00:00"
    )
    assert composition_response.id == "test-id"
    assert composition_response.title == "Test Composition"
    assert composition_response.file_path == "/path/to/midi/file.mid"
    assert composition_response.created_at == "2023-01-01T12:00:00"