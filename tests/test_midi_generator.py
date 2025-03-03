import os
import pytest
import pretty_midi

from app.utils.midi_generator import MidiGenerator


def test_generate_midi_file_basic(temp_midi_dir, sample_composition_data):
    """Test basic MIDI file generation with simple composition data"""
    # Generate MIDI file
    result = MidiGenerator.generate_midi_file(sample_composition_data)
    
    # Check if the file was created
    assert os.path.exists(result["file_path"])
    
    # Check if metadata is correct
    assert result["title"] == "Test Composition"
    assert "id" in result
    assert "created_at" in result
    
    # Verify MIDI file content
    midi = pretty_midi.PrettyMIDI(result["file_path"])
    assert len(midi.instruments) == 1
    assert midi.instruments[0].program == 0  # Piano
    assert len(midi.instruments[0].notes) == 4
    assert midi.get_tempo_changes()[1][0] == 120


def test_generate_midi_file_complex(temp_midi_dir, complex_composition_data):
    """Test MIDI file generation with more complex composition data"""
    # Generate MIDI file
    result = MidiGenerator.generate_midi_file(complex_composition_data)
    
    # Check if the file was created
    assert os.path.exists(result["file_path"])
    
    # Verify MIDI file content
    midi = pretty_midi.PrettyMIDI(result["file_path"])
    
    # Should have 3 instruments: piano, bass, and strings
    assert len(midi.instruments) == 3
    
    # Verify instruments and notes
    instruments = sorted(midi.instruments, key=lambda i: i.program)
    
    # Piano (program 0)
    assert instruments[0].program == 0
    assert len(instruments[0].notes) == 6  # 4 notes from intro + 2 from chorus
    
    # Bass (program 32)
    assert instruments[1].program == 32
    assert len(instruments[1].notes) == 2
    
    # Strings (program 48)
    assert instruments[2].program == 48
    assert len(instruments[2].notes) == 1
    
    # Verify tempo - allow for small rounding errors
    assert abs(midi.get_tempo_changes()[1][0] - 140) < 0.1


def test_generate_midi_file_error_handling(temp_midi_dir, sample_composition_data):
    """Test error handling in MIDI file generation"""
    # Create an invalid composition by setting an invalid value
    invalid_composition = sample_composition_data.model_copy(deep=True)
    # Force notes to be empty which should cause an error during generation
    invalid_composition.sections[0].tracks[0].notes = []
    
    # Generation should still work (empty track is valid)
    result = MidiGenerator.generate_midi_file(invalid_composition)
    assert os.path.exists(result["file_path"])
    
    # Load the MIDI file to confirm it was created correctly
    midi = pretty_midi.PrettyMIDI(result["file_path"])
    # With empty notes, no instruments should be added (our implementation skips empty instruments)
    assert len(midi.instruments) == 0