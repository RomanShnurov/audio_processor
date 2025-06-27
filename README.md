# Audio Processor

[![CI](https://github.com/RomanShnurov/audio_processor/actions/workflows/ci.yml/badge.svg)](https://github.com/RomanShnurov/audio_processor/actions/workflows/ci.yml)

A Python-based WebSocket server for processing audio streams in real time. This project demonstrates a simple architecture for receiving audio chunks from clients, processing them (mock transcription), and sending results back asynchronously.

## Features
- WebSocket server for real-time audio chunk processing
- Multiprocessing for handling audio processing tasks
- Example client for sending audio data
- Support for running multiple clients simultaneously
- Docker support for easy deployment

## Project Structure
```
audio_processor/
├── client/
│   ├── client.py            # Example client to send audio chunks
├── scripts/
│   └── run_clients.sh       # Script to run multiple clients
├── src/
│   ├── __init__.py
│   ├── processor.py         # Audio processing logic (mock transcription)
│   └── server.py            # WebSocket server handling clients and processing
├── test/
│   ├── __init__.py
│   └── test_processor.py    # Unit tests for audio processor
├── requirements.txt         # Python dependencies
├── pyproject.toml           # Project metadata and dependencies
├── uv.lock                  # Locked dependencies for reproducible builds
├── Dockerfile               # Docker image definition
└── .github/
    └── workflows/
        └── ci.yml           # CI workflow
```

## Requirements
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended Python package manager)
- Docker (optional, for containerized deployment)

## Installation
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd audio_processor
   ```
2. Install dependencies using uv (recommended):
   ```bash
   uv sync --locked --no-dev
   ```
   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run the Server
```bash
uv run src/server.py
# or
python src/server.py
```

### Run the Example Client
In a separate terminal:
```bash
uv run client/client.py
# or
python client/client.py
```

### Run Multiple Clients
Use the provided script to run multiple clients simultaneously:
```bash
chmod +x scripts/run_clients.sh
./scripts/run_clients.sh
```
This will prompt for the number of clients to start, and logs will be saved in the `client/` directory.

### Using Docker
Build and run the Docker image:
```bash
docker build -t audio-processor .
docker run -p 8765:8765 audio-processor
```

## How It Works
- The server listens for WebSocket connections on port 8765
- Clients send audio chunks (as bytes) to the server
- The server processes each chunk using a separate process (mock transcription)
- Results are sent back to clients asynchronously via WebSocket
- The system supports multiple concurrent clients

## Development
This project uses `uv` for dependency management with a lockfile (`uv.lock`) for reproducible builds. The Docker image is optimized for production deployment with bytecode compilation enabled.

## Testing

This project uses [pytest](https://pytest.org/) for unit testing.

To run the tests, first ensure you have pytest installed:

```bash
uv pip install pytest
# or
pip install pytest
```

Then run the tests from the project root:

```bash
pytest
```

This will automatically discover and run all tests, including the sample test in `test/test_processor.py`.
