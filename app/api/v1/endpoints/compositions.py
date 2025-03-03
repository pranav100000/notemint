import os
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Query, Path, UploadFile, File, Response
from fastapi.responses import FileResponse

from app.models.composition import CompositionRequest, CompositionResponse, CompositionList
from app.utils.midi_generator import MidiGenerator
from app.core.storage import CompositionStorage
from app.core.config import settings

router = APIRouter()
storage = CompositionStorage()


@router.post("/generate", response_model=CompositionResponse, status_code=201)
async def generate_composition(request: CompositionRequest) -> Dict[str, Any]:
    """
    Generate a MIDI file from composition data
    """
    try:
        # Generate the MIDI file
        composition_data = MidiGenerator.generate_midi_file(request.composition)
        
        # Store the composition metadata
        composition = storage.add_composition(composition_data)
        
        return composition
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating MIDI file: {str(e)}")


@router.get("/{composition_id}", response_model=CompositionResponse)
async def get_composition(
    composition_id: str = Path(..., description="The ID of the composition to retrieve")
) -> Dict[str, Any]:
    """
    Retrieve information about a specific composition
    """
    composition = storage.get_composition(composition_id)
    if not composition:
        raise HTTPException(status_code=404, detail="Composition not found")
    
    return composition


@router.get("", response_model=CompositionList)
async def list_compositions(
    skip: int = Query(0, ge=0, description="Number of compositions to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of compositions to return")
) -> Dict[str, Any]:
    """
    List all generated compositions with pagination
    """
    return storage.list_compositions(skip, limit)


@router.get("/{composition_id}/download")
async def download_midi(
    composition_id: str = Path(..., description="The ID of the composition to download")
):
    """
    Download a generated MIDI file
    """
    composition = storage.get_composition(composition_id)
    if not composition:
        raise HTTPException(status_code=404, detail="Composition not found")
    
    file_path = composition["file_path"]
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="MIDI file not found")
    
    return FileResponse(
        path=file_path,
        filename=os.path.basename(file_path),
        media_type="audio/midi"
    )