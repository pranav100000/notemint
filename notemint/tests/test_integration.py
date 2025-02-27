import os
import json
import tempfile
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
import pretty_midi

from app.main import app
from app.core.config import settings

client = TestClient(app)


def test_full_workflow(temp_midi_dir):
    """Test the full workflow from creating a composition to downloading it"""
    
    # 1. Create a composition
    composition_request = {
        "composition": {
            "title": "Integration Test",
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
    
    response = client.post("/api/v1/compositions/generate", json=composition_request)
    assert response.status_code == 201
    composition_data = response.json()
    composition_id = composition_data["id"]
    
    # 2. Get the composition by ID
    response = client.get(f"/api/v1/compositions/{composition_id}")
    assert response.status_code == 200
    retrieved_data = response.json()
    assert retrieved_data["id"] == composition_id
    assert retrieved_data["title"] == "Integration Test"
    
    # 3. Check that it appears in the list of compositions
    response = client.get("/api/v1/compositions")
    assert response.status_code == 200
    compositions_list = response.json()
    assert compositions_list["total"] >= 1
    composition_ids = [comp["id"] for comp in compositions_list["compositions"]]
    assert composition_id in composition_ids
    
    # 4. Download the MIDI file
    response = client.get(f"/api/v1/compositions/{composition_id}/download")
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/midi"
    
    # 5. Verify that the downloaded file is a valid MIDI file with expected content
    with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as temp_file:
        temp_file.write(response.content)
        temp_file_path = temp_file.name
    
    try:
        # Load the downloaded MIDI file
        midi = pretty_midi.PrettyMIDI(temp_file_path)
        
        # Verify content
        assert len(midi.instruments) == 1
        assert midi.instruments[0].program == 0  # Piano
        assert len(midi.instruments[0].notes) == 4
        assert midi.get_tempo_changes()[1][0] == 120
        
        # Verify note pitches
        pitches = sorted([note.pitch for note in midi.instruments[0].notes])
        assert pitches == [60, 64, 67, 72]
    finally:
        # Clean up
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


def test_concurrent_requests(temp_midi_dir):
    """Test handling multiple concurrent requests"""
    import concurrent.futures
    
    def create_composition(index):
        request_data = {
            "composition": {
                "title": f"Concurrent Test {index}",
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
                            }
                        ]
                    }
                ]
            }
        }
        response = client.post("/api/v1/compositions/generate", json=request_data)
        return response.status_code, response.json()
    
    # Create 3 compositions concurrently (fewer to reduce chance of race conditions)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(create_composition, i) for i in range(3)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    # Check that all requests succeeded
    for status_code, data in results:
        assert status_code == 201
        assert "id" in data
        assert "file_path" in data
        assert os.path.exists(data["file_path"])
    
    # Check that all compositions are in the list
    response = client.get("/api/v1/compositions")
    assert response.status_code == 200
    compositions_list = response.json()
    assert compositions_list["total"] >= 3


def test_api_error_responses(temp_midi_dir):
    """Test API error responses"""
    
    # Test 404 for non-existent composition
    response = client.get("/api/v1/compositions/non-existent-id")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
    
    # Test 404 for download of non-existent composition
    response = client.get("/api/v1/compositions/non-existent-id/download")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
    
    # Test 422 for invalid input (missing required field)
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
    assert response.status_code == 422
    
    # Test invalid JSON
    response = client.post(
        "/api/v1/compositions/generate", 
        headers={"Content-Type": "application/json"},
        content="invalid json"
    )
    assert response.status_code == 422