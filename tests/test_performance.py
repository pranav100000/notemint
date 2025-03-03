import os
import time
import pytest
from fastapi.testclient import TestClient
import psutil
import tempfile

from app.main import app

client = TestClient(app)

# Skip these tests by default as they're for performance benchmarking
pytestmark = pytest.mark.skip(reason="Performance tests are only run manually")


def test_memory_usage(temp_midi_dir):
    """Test memory usage when generating compositions"""
    process = psutil.Process(os.getpid())
    
    # Baseline memory usage
    base_memory = process.memory_info().rss / 1024 / 1024  # Convert to MB
    
    # Create a large composition
    large_composition = {
        "composition": {
            "title": "Memory Test",
            "tempo": 120,
            "time_signature": "4/4",
            "key": "C",
            "scale": "major",
            "length_bars": 100,
            "sections": [
                {
                    "name": "Main",
                    "bars": 100,
                    "tracks": [
                        {
                            "instrument": "piano",
                            "midi_program": 0,
                            "notes": [
                                {"pitch": 60 + i % 24, "start_time": i * 0.25, "duration": 0.25, "velocity": 80}
                                for i in range(400)  # 400 notes
                            ]
                        }
                    ]
                }
            ]
        }
    }
    
    # Generate composition
    response = client.post("/api/v1/compositions/generate", json=large_composition)
    assert response.status_code == 201
    
    # Check memory usage after generation
    post_memory = process.memory_info().rss / 1024 / 1024  # Convert to MB
    
    # Calculate memory increase
    memory_increase = post_memory - base_memory
    
    # Print memory usage info
    print(f"Base memory usage: {base_memory:.2f} MB")
    print(f"Memory usage after generation: {post_memory:.2f} MB")
    print(f"Memory increase: {memory_increase:.2f} MB")
    
    # Optional assertion - adjust threshold as needed
    # This is a soft check that can be adjusted based on observed performance
    assert memory_increase < 100  # Memory increase should be less than 100 MB


def test_response_time(temp_midi_dir):
    """Test response time for different composition sizes"""
    
    def measure_generation_time(num_notes):
        """Measure time to generate a composition with given number of notes"""
        composition = {
            "composition": {
                "title": f"Response Time Test ({num_notes} notes)",
                "tempo": 120,
                "time_signature": "4/4",
                "key": "C",
                "scale": "major",
                "length_bars": max(4, num_notes // 16),  # Reasonable number of bars
                "sections": [
                    {
                        "name": "Main",
                        "bars": max(4, num_notes // 16),
                        "tracks": [
                            {
                                "instrument": "piano",
                                "midi_program": 0,
                                "notes": [
                                    {"pitch": 60 + i % 24, "start_time": i * 0.25, "duration": 0.25, "velocity": 80}
                                    for i in range(num_notes)
                                ]
                            }
                        ]
                    }
                ]
            }
        }
        
        start_time = time.time()
        response = client.post("/api/v1/compositions/generate", json=composition)
        end_time = time.time()
        
        assert response.status_code == 201
        
        generation_time = end_time - start_time
        return generation_time
    
    # Test with different numbers of notes
    note_counts = [10, 50, 100, 200, 500]
    results = {}
    
    for count in note_counts:
        time_taken = measure_generation_time(count)
        results[count] = time_taken
        print(f"Time to generate composition with {count} notes: {time_taken:.4f} seconds")
    
    # Check that generation time scales reasonably
    # This is a soft check - the specific thresholds can be adjusted based on observed performance
    for i in range(1, len(note_counts)):
        ratio = results[note_counts[i]] / results[note_counts[0]]
        note_ratio = note_counts[i] / note_counts[0]
        
        # Generation time should increase sub-linearly with the number of notes
        # (i.e., doubling the notes should less than double the time)
        # This is a rough heuristic and may need adjustment
        assert ratio < note_ratio * 1.5, f"Performance scaling worse than expected for {note_counts[i]} notes"


def test_file_size(temp_midi_dir):
    """Test the file size of generated MIDI files"""
    
    def measure_file_size(num_notes):
        """Measure the file size of a MIDI file with the given number of notes"""
        composition = {
            "composition": {
                "title": f"File Size Test ({num_notes} notes)",
                "tempo": 120,
                "time_signature": "4/4",
                "key": "C",
                "scale": "major",
                "length_bars": max(4, num_notes // 16),
                "sections": [
                    {
                        "name": "Main",
                        "bars": max(4, num_notes // 16),
                        "tracks": [
                            {
                                "instrument": "piano",
                                "midi_program": 0,
                                "notes": [
                                    {"pitch": 60 + i % 24, "start_time": i * 0.25, "duration": 0.25, "velocity": 80}
                                    for i in range(num_notes)
                                ]
                            }
                        ]
                    }
                ]
            }
        }
        
        response = client.post("/api/v1/compositions/generate", json=composition)
        assert response.status_code == 201
        
        file_path = response.json()["file_path"]
        file_size = os.path.getsize(file_path) / 1024  # Convert to KB
        
        return file_size
    
    # Test with different numbers of notes
    note_counts = [10, 50, 100, 500, 1000]
    results = {}
    
    for count in note_counts:
        size = measure_file_size(count)
        results[count] = size
        print(f"File size for composition with {count} notes: {size:.2f} KB")
    
    # Check that file size scales reasonably with the number of notes
    # MIDI file size should scale roughly linearly with note count
    # but with overhead for headers, etc.
    small_file_size = results[note_counts[0]]
    large_file_size = results[note_counts[-1]]
    note_ratio = note_counts[-1] / note_counts[0]
    
    # Size ratio should be less than note ratio due to fixed overhead in MIDI files
    size_ratio = large_file_size / small_file_size
    assert size_ratio < note_ratio, "File size scaling worse than expected"
    
    # Even large compositions should produce reasonably sized MIDI files
    assert large_file_size < 1000, "Large composition produced unexpectedly large MIDI file"