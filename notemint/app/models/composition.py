from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class Note(BaseModel):
    pitch: int = Field(..., ge=0, le=127, description="MIDI note number (0-127)")
    start_time: float = Field(..., description="Start time in beats")
    duration: float = Field(..., description="Duration in beats")
    velocity: int = Field(..., ge=0, le=127, description="Note velocity (0-127)")


class Track(BaseModel):
    instrument: str = Field(..., description="Instrument name")
    midi_program: int = Field(..., ge=0, le=127, description="MIDI program number (0-127)")
    notes: List[Note] = Field(..., description="List of notes in the track")


class Section(BaseModel):
    name: str = Field(..., description="Section name")
    bars: int = Field(..., gt=0, description="Number of bars in the section")
    tracks: List[Track] = Field(..., description="List of tracks in the section")


class CompositionData(BaseModel):
    title: str = Field(..., description="Composition title")
    tempo: int = Field(..., gt=0, description="Tempo in beats per minute")
    time_signature: str = Field(..., description="Time signature (e.g., '4/4')")
    key: str = Field(..., description="Key of the composition")
    scale: str = Field(..., description="Scale type (e.g., 'major', 'minor')")
    length_bars: int = Field(..., gt=0, description="Total length in bars")
    sections: List[Section] = Field(..., description="List of composition sections")


class CompositionRequest(BaseModel):
    composition: CompositionData = Field(..., description="Composition data")


class CompositionResponse(BaseModel):
    id: str = Field(..., description="Composition ID")
    title: str = Field(..., description="Composition title")
    file_path: str = Field(..., description="Path to the generated MIDI file")
    created_at: str = Field(..., description="Creation timestamp")


class CompositionList(BaseModel):
    compositions: List[CompositionResponse] = Field(..., description="List of compositions")
    total: int = Field(..., description="Total number of compositions")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")