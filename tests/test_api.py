import os
import json
from pathlib import Path
from fastapi.testclient import TestClient

from app.main import app
from app.core.storage import CompositionStorage


client = TestClient(app)


def test_generate_composition_endpoint(temp_midi_dir, sample_composition_request):
    """Test the generate composition endpoint"""
    # Send request to generate a composition
    response = client.post("/api/v1/compositions/generate", json=sample_composition_request)
    
    # Check response
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Composition"
    assert "file_path" in data
    assert "created_at" in data
    
    # Check if file exists
    assert os.path.exists(data["file_path"])


def test_get_composition_by_id(temp_midi_dir, sample_composition_request):
    """Test retrieving a composition by ID"""
    # First create a composition
    response = client.post("/api/v1/compositions/generate", json=sample_composition_request)
    assert response.status_code == 201
    created_data = response.json()
    composition_id = created_data["id"]
    
    # Then retrieve it by ID
    response = client.get(f"/api/v1/compositions/{composition_id}")
    assert response.status_code == 200
    retrieved_data = response.json()
    
    # Verify it's the same composition
    assert retrieved_data["id"] == composition_id
    assert retrieved_data["title"] == "Test Composition"
    assert retrieved_data["file_path"] == created_data["file_path"]


def test_get_nonexistent_composition(temp_midi_dir):
    """Test retrieving a composition that doesn't exist"""
    response = client.get("/api/v1/compositions/nonexistent-id")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_list_compositions(temp_midi_dir, sample_composition_request):
    """Test listing compositions with pagination"""
    # Get current composition count
    initial_response = client.get("/api/v1/compositions")
    initial_count = initial_response.json()["total"]
    
    # Create multiple compositions
    new_composition_ids = []
    for i in range(3):
        request_data = sample_composition_request.copy()
        request_data["composition"]["title"] = f"Test Composition {i+1}"
        response = client.post("/api/v1/compositions/generate", json=request_data)
        assert response.status_code == 201
        new_composition_ids.append(response.json()["id"])
    
    # Test listing all compositions
    response = client.get("/api/v1/compositions")
    assert response.status_code == 200
    data = response.json()
    
    assert "compositions" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data
    
    # Check that we have 3 more compositions than before
    assert data["total"] == initial_count + 3
    
    # Check that our new compositions are present
    composition_ids = [comp["id"] for comp in data["compositions"]]
    for new_id in new_composition_ids:
        assert new_id in composition_ids
        
    assert data["page"] == 1
    
    # Test pagination
    response = client.get("/api/v1/compositions?skip=1&limit=1")
    assert response.status_code == 200
    data = response.json()
    
    assert data["total"] > 0
    assert len(data["compositions"]) == 1
    assert data["page"] == 2
    assert data["size"] == 1


def test_download_midi_file(temp_midi_dir, sample_composition_request):
    """Test downloading a MIDI file"""
    # First create a composition
    response = client.post("/api/v1/compositions/generate", json=sample_composition_request)
    assert response.status_code == 201
    created_data = response.json()
    composition_id = created_data["id"]
    
    # Then download the MIDI file
    response = client.get(f"/api/v1/compositions/{composition_id}/download")
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/midi"
    assert "attachment" in response.headers["content-disposition"]
    
    # Verify file content is returned
    assert len(response.content) > 0


def test_download_nonexistent_midi_file(temp_midi_dir):
    """Test downloading a MIDI file that doesn't exist"""
    response = client.get("/api/v1/compositions/nonexistent-id/download")
    assert response.status_code == 404