import os
import uuid
from datetime import datetime
from pathlib import Path
import logging
from typing import Dict, Any

import pretty_midi

from app.models.composition import CompositionData
from app.core.config import settings

logger = logging.getLogger(__name__)


class MidiGenerator:
    @staticmethod
    def generate_midi_file(composition_data: CompositionData) -> Dict[str, Any]:
        """
        Generate a MIDI file from composition data
        
        Args:
            composition_data: The composition data structure
            
        Returns:
            Dictionary with metadata about the generated file
        """
        try:
            # Create a PrettyMIDI object
            midi = pretty_midi.PrettyMIDI(initial_tempo=composition_data.tempo)
            
            # Dictionary to keep track of instruments by name and program
            instruments = {}
            
            # Process each section in the composition
            for section in composition_data.sections:
                # Process each track in the section
                for track in section.tracks:
                    # Create a unique key for the instrument
                    instrument_key = f"{track.instrument}_{track.midi_program}"
                    
                    # Get or create the instrument
                    if instrument_key not in instruments:
                        instrument = pretty_midi.Instrument(
                            program=track.midi_program,
                            name=track.instrument
                        )
                        instruments[instrument_key] = instrument
                    else:
                        instrument = instruments[instrument_key]
                    
                    # Add notes to the instrument
                    for note_data in track.notes:
                        if not hasattr(note_data, 'pitch') or note_data.pitch is None:
                            continue  # Skip invalid notes
                            
                        note = pretty_midi.Note(
                            velocity=note_data.velocity,
                            pitch=note_data.pitch,
                            start=note_data.start_time,
                            end=note_data.start_time + note_data.duration
                        )
                        instrument.notes.append(note)
            
            # Add all instruments to the MIDI data
            for instrument in instruments.values():
                if instrument.notes:  # Only add instruments with notes
                    midi.instruments.append(instrument)
            
            # Generate a unique filename
            composition_id = str(uuid.uuid4())
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{composition_id}_{timestamp}.mid"
            file_path = os.path.join(settings.MIDI_FILES_DIR, filename)
            
            # Write the MIDI file
            midi.write(file_path)
            
            return {
                "id": composition_id,
                "title": composition_data.title,
                "file_path": str(file_path),
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating MIDI file: {str(e)}")
            raise