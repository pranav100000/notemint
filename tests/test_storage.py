import os
import json
import tempfile
from pathlib import Path
import pytest

from app.core.storage import CompositionStorage
from app.core.config import settings


def test_add_composition(temp_midi_dir):
    """Test adding a composition to storage"""
    metadata_file = os.path.join(temp_midi_dir, "metadata.json")
    # Reset the singleton for testing
    CompositionStorage._instance = None
    storage = CompositionStorage(metadata_file=metadata_file)
    
    # Sample composition data
    composition_data = {
        "id": "test-id-1",
        "title": "Test Composition",
        "file_path": "/path/to/midi/file.mid",
        "created_at": "2023-01-01T12:00:00"
    }
    
    # Add to storage
    result = storage.add_composition(composition_data)
    
    # Verify result
    assert result == composition_data
    
    # Verify it was stored
    assert "test-id-1" in storage._compositions
    assert storage._compositions["test-id-1"] == composition_data
    
    # Verify it was saved to file
    metadata_file = os.path.join(temp_midi_dir, "metadata.json")
    assert os.path.exists(metadata_file)
    
    with open(metadata_file, "r") as f:
        saved_data = json.load(f)
        assert "test-id-1" in saved_data
        assert saved_data["test-id-1"] == composition_data


def test_get_composition(temp_midi_dir):
    """Test getting a composition from storage"""
    metadata_file = os.path.join(temp_midi_dir, "metadata.json")
    # Reset the singleton for testing
    CompositionStorage._instance = None
    storage = CompositionStorage(metadata_file=metadata_file)
    
    # Sample composition data
    composition_data = {
        "id": "test-id-2",
        "title": "Test Composition 2",
        "file_path": "/path/to/midi/file2.mid",
        "created_at": "2023-01-02T12:00:00"
    }
    
    # Add to storage
    storage.add_composition(composition_data)
    
    # Get from storage
    result = storage.get_composition("test-id-2")
    assert result == composition_data
    
    # Get nonexistent composition
    result = storage.get_composition("nonexistent-id")
    assert result is None


def test_list_compositions(temp_midi_dir):
    """Test listing compositions with pagination"""
    metadata_file = os.path.join(temp_midi_dir, "metadata.json")
    # Reset the singleton for testing
    CompositionStorage._instance = None
    storage = CompositionStorage(metadata_file=metadata_file)
    
    # Add multiple compositions
    compositions = []
    for i in range(5):
        composition_data = {
            "id": f"test-id-{i}",
            "title": f"Test Composition {i}",
            "file_path": f"/path/to/midi/file{i}.mid",
            "created_at": f"2023-01-0{i+1}T12:00:00"
        }
        storage.add_composition(composition_data)
        compositions.append(composition_data)
    
    # List all compositions
    result = storage.list_compositions()
    assert result["total"] == 5
    assert len(result["compositions"]) == 5
    assert result["page"] == 1
    assert result["size"] == 100
    
    # Test pagination
    result = storage.list_compositions(skip=2, limit=2)
    assert result["total"] == 5
    assert len(result["compositions"]) == 2
    assert result["page"] == 2
    assert result["size"] == 2
    
    # Test sorting (newest first)
    result = storage.list_compositions()
    # The compositions should be sorted by created_at in descending order
    sorted_compositions = sorted(
        compositions, 
        key=lambda c: c["created_at"], 
        reverse=True
    )
    assert result["compositions"][0]["id"] == sorted_compositions[0]["id"]


def test_storage_persistence(temp_midi_dir):
    """Test storage persistence across instances"""
    metadata_file = os.path.join(temp_midi_dir, "metadata.json")
    # Reset the singleton for testing
    CompositionStorage._instance = None
    
    # First instance
    storage1 = CompositionStorage(metadata_file=metadata_file)
    
    # Add composition
    composition_data = {
        "id": "test-id-persistence",
        "title": "Test Persistence",
        "file_path": "/path/to/midi/file.mid",
        "created_at": "2023-01-01T12:00:00"
    }
    storage1.add_composition(composition_data)
    
    # Create new instance (should load from file)
    CompositionStorage._instance = None  # Reset singleton
    storage2 = CompositionStorage(metadata_file=metadata_file)
    
    # Verify composition is available in new instance
    result = storage2.get_composition("test-id-persistence")
    assert result == composition_data