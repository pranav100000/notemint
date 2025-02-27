import requests
import json
import time
import os

def test_service():
    """Manual test of the service"""
    print("Testing the notemint service...")
    
    # Start the service in a separate process
    from subprocess import Popen
    import sys
    
    # Create MIDI files directory if needed
    os.makedirs("midi_files", exist_ok=True)
    
    # Prepare the request data
    composition_request = {
        "composition": {
            "title": "Final Test Composition",
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
    
    try:
        # Generate the MIDI file
        print("\n1. Generating a MIDI file...")
        response = requests.post(
            "http://localhost:8000/api/v1/compositions/generate",
            json=composition_request
        )
        
        if response.status_code == 201:
            print("✓ MIDI file generated successfully!")
            print(f"  Status: {response.status_code}")
            print(f"  Response: {json.dumps(response.json(), indent=2)}")
            
            composition_id = response.json()["id"]
            
            # Get the composition
            print("\n2. Retrieving the composition...")
            response = requests.get(f"http://localhost:8000/api/v1/compositions/{composition_id}")
            
            if response.status_code == 200:
                print("✓ Composition retrieved successfully!")
                print(f"  Status: {response.status_code}")
                print(f"  Response: {json.dumps(response.json(), indent=2)}")
            else:
                print(f"❌ Failed to retrieve composition: {response.status_code}")
                print(response.text)
            
            # List compositions
            print("\n3. Listing all compositions...")
            response = requests.get("http://localhost:8000/api/v1/compositions")
            
            if response.status_code == 200:
                print("✓ Compositions listed successfully!")
                print(f"  Status: {response.status_code}")
                compositions = response.json()["compositions"]
                total = response.json()["total"]
                print(f"  Total compositions: {total}")
                
                if compositions:
                    print(f"  Latest composition: {compositions[0]['title']}")
            else:
                print(f"❌ Failed to list compositions: {response.status_code}")
                print(response.text)
            
            # Download the MIDI file
            print("\n4. Downloading the MIDI file...")
            response = requests.get(f"http://localhost:8000/api/v1/compositions/{composition_id}/download")
            
            if response.status_code == 200:
                print("✓ MIDI file downloaded successfully!")
                print(f"  Status: {response.status_code}")
                print(f"  Content-Type: {response.headers['Content-Type']}")
                print(f"  Content-Length: {len(response.content)} bytes")
            else:
                print(f"❌ Failed to download MIDI file: {response.status_code}")
                print(response.text)
            
            print("\n✨ All manual tests passed!")
        else:
            print(f"❌ Failed to generate MIDI file: {response.status_code}")
            print(response.text)
    
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
    
    finally:
        print("\nTests completed.")

if __name__ == "__main__":
    print("Starting server...")
    # Start the service in a subprocess
    import subprocess
    import sys
    import time
    
    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd="/Users/pranavsharan/Developer/notemint/notemint"
    )
    
    try:
        # Wait for the server to start
        print("Waiting for server to start...")
        time.sleep(3)
        
        # Run the tests
        test_service()
    
    finally:
        # Clean up
        print("Stopping the server...")
        server_process.terminate()
        server_process.wait()