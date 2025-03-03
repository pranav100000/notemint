# notemint

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A powerful Python service for generating MIDI files from structured musical instructions. notemint accepts detailed JSON composition data and outputs standard MIDI files that can be used with any digital audio workstation or music software.

## 🎵 Features

- **JSON to MIDI Conversion**: Transform structured musical data into properly formatted MIDI files
- **Multiple Tracks**: Support for compositions with multiple instruments and sections
- **Configurable Parameters**: Control tempo, time signature, key, scale, and more
- **Composition Management**: Store, retrieve, and download generated compositions
- **Robust API**: Well-documented RESTful API with validation and error handling
- **Containerized**: Easy deployment with Docker

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

**Option 1: Using Docker (recommended)**

```bash
# Clone the repository
git clone https://github.com/yourusername/notemint.git
cd notemint

# Build and start the service with Docker
docker-compose up -d
```

**Option 2: Manual Installation**

```bash
# Clone the repository
git clone https://github.com/yourusername/notemint.git
cd notemint

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the service
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000 with interactive documentation at http://localhost:8000/docs.

## 📊 API Endpoints

### Generate a MIDI File

```
POST /api/v1/compositions/generate
```

Accepts a JSON payload with composition data and returns information about the generated MIDI file.

**Example Request:**

```json
{
  "composition": {
    "title": "Simple Melody",
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
```

**Example Response:**

```json
{
  "id": "392cfb3d-35d6-480d-9b79-3822763cbb6e",
  "title": "Simple Melody",
  "file_path": "midi_files/392cfb3d-35d6-480d-9b79-3822763cbb6e_20250226183648.mid",
  "created_at": "2025-02-26T18:36:48.936791"
}
```

### Retrieve a Composition

```
GET /api/v1/compositions/{composition_id}
```

Retrieves information about a specific composition.

### List All Compositions

```
GET /api/v1/compositions
```

Lists all generated compositions with support for pagination.

**Query Parameters:**
- `skip`: Number of compositions to skip (default: 0)
- `limit`: Maximum number of compositions to return (default: 100)

### Download a MIDI File

```
GET /api/v1/compositions/{composition_id}/download
```

Downloads the MIDI file for a specific composition.

## 🎹 Data Model

### Note Object

| Field       | Type   | Description                         |
|-------------|--------|-------------------------------------|
| pitch       | int    | MIDI note number (0-127)            |
| start_time  | float  | Start time in beats                 |
| duration    | float  | Duration in beats                   |
| velocity    | int    | Note velocity/volume (0-127)        |

### Track Object

| Field        | Type     | Description                        |
|--------------|----------|------------------------------------|
| instrument   | string   | Instrument name                    |
| midi_program | int      | MIDI program number (0-127)        |
| notes        | Note[]   | List of notes in the track         |

### Section Object

| Field  | Type     | Description                         |
|--------|----------|-------------------------------------|
| name   | string   | Section name                        |
| bars   | int      | Number of bars in the section       |
| tracks | Track[]  | List of tracks in the section       |

### Composition Object

| Field           | Type       | Description                          |
|-----------------|------------|--------------------------------------|
| title           | string     | Composition title                    |
| tempo           | int        | Tempo in beats per minute            |
| time_signature  | string     | Time signature (e.g., "4/4")         |
| key             | string     | Key of the composition               |
| scale           | string     | Scale type (e.g., "major", "minor")  |
| length_bars     | int        | Total length in bars                 |
| sections        | Section[]  | List of composition sections         |

## ⚙️ Configuration

notemint can be configured using environment variables:

| Variable        | Description                                   | Default      |
|-----------------|-----------------------------------------------|--------------|
| MIDI_FILES_DIR  | Directory to store generated MIDI files       | ./midi_files |
| CORS_ORIGINS    | Origins allowed for CORS (comma-separated)    | *            |

You can set these in a `.env` file in the root directory, or in your environment.

## 🧪 Testing

notemint includes comprehensive tests covering core functionality, edge cases, and integration.

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
./run_tests.sh

# Run specific test categories
pytest tests/test_models.py -v
pytest tests/test_api.py -v
pytest tests/test_edge_cases.py -v

# Run with coverage report
pytest --cov=app tests/
```

## 🔍 Limitations and Future Work

Current limitations compared to a full-featured DAW:

- **Single Tempo**: No support for tempo changes or time signature changes
- **Limited MIDI Events**: No support for pitch bend, aftertouch, or continuous controllers
- **No Audio Effects**: No support for reverb, delay, EQ, etc. (MIDI limitation)
- **No Timeline Automation**: No support for parameter automation over time

Future enhancements may include:

- Support for tempo changes and time signature changes
- Additional MIDI event types (pitch bend, controllers, etc.)
- Integration with VST instruments for audio rendering
- Algorithmic composition tools
- Musical notation import/export

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request