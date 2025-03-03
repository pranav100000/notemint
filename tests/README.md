# notemint Tests

This directory contains tests for the notemint service.

## Running Tests

To run all tests:

```bash
./run_tests.sh
```

To run tests and include performance tests:

```bash
./run_tests.sh --perf
```

To run a specific test file:

```bash
pytest tests/test_api.py -v
```

## Test Categories

The tests are organized into the following categories:

1. **Unit Tests**
   - `test_models.py`: Tests data model validation
   - `test_midi_generator.py`: Tests MIDI file generation 
   - `test_storage.py`: Tests composition storage
   - `test_config.py`: Tests configuration

2. **Integration Tests**
   - `test_api.py`: Tests API endpoints
   - `test_integration.py`: Tests full workflow scenarios

3. **Edge Cases**
   - `test_edge_cases.py`: Tests behavior with unusual inputs

4. **Performance Tests**
   - `test_performance.py`: Tests resource usage and timing

## Test Coverage

The test suite aims to achieve high coverage of the codebase. A coverage report is generated when running the tests using `run_tests.sh`.

## Fixtures

Common fixtures are defined in `conftest.py` and include:

- `temp_midi_dir`: Creates a temporary directory for testing
- `sample_composition_data`: Provides a simple composition for testing
- `complex_composition_data`: Provides a more complex composition for testing
- `sample_composition_request`: Provides a sample API request