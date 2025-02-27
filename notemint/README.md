# notemint

A FastAPI-based service that generates MIDI files based on structured musical instructions. The service accepts detailed JSON composition data and outputs MIDI files.

## Features

- FastAPI-based service with JSON input and MIDI file output
- Flexible composition format with support for multiple tracks and instruments
- Configurable tempo, time signature, key, and scale
- Storage and retrieval of generated compositions
- Docker support for easy deployment

## Installation

### Using Docker

The easiest way to run notemint is with Docker:

```bash
docker-compose up -d
```

This will start the service on port 8000.

### Manual Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the service:

```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Generate a MIDI file

```
POST /api/v1/compositions/generate
```

Accepts a JSON payload with composition data and returns information about the generated MIDI file.

Example input:

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

### Get a composition

```
GET /api/v1/compositions/{composition_id}
```

Retrieves information about a specific composition.

### List compositions

```
GET /api/v1/compositions
```

Lists all generated compositions with support for pagination.

Query parameters:
- `skip`: Number of compositions to skip (default: 0)
- `limit`: Maximum number of compositions to return (default: 100)

### Download MIDI file

```
GET /api/v1/compositions/{composition_id}/download
```

Downloads the MIDI file for a specific composition.

## Environment Variables

notemint can be configured using the following environment variables:

- `MIDI_FILES_DIR`: Directory to store generated MIDI files
- `CORS_ORIGINS`: Origins allowed for CORS (comma-separated, default: "*")

## Testing

Run tests with pytest:

```bash
pytest
```

## License

MIT