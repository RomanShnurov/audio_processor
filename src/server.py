import asyncio
import json
import logging
from typing import Any
import uuid
from multiprocessing import Process, Queue

import websockets

from processor import audio_processor

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

CLIENTS: dict[str, dict[str, Any]] = {}

async def transcription_sender(websocket, client_id: str):
    """
    Asynchronously sends transcription results to a WebSocket client.

    This function continuously retrieves transcriptions from a result queue
    and sends them to the connected WebSocket client associated with the given
    client ID. It runs in an infinite loop until a termination signal (None) 
    is received from the queue. 

    Args:
        websocket: The WebSocket connection to the client.
        client_id (str): A unique identifier for the client.
    """

    logging.info(f"[{client_id}] Starting to send transcriptions.")
    result_queue: Queue = CLIENTS[client_id]["result_queue"]

    try:
        while True:
            loop = asyncio.get_running_loop()
            transcript = await loop.run_in_executor(None, result_queue.get)

            if transcript is None:
                break

            response = {"status": "ok", "transcript": transcript}
            await websocket.send(json.dumps(response))
            logging.info(f"[{client_id}] Sent transcript: {transcript}")

    except asyncio.CancelledError:
        logging.info(f"[{client_id}] Task for sending transcriptions was cancelled.")
    except Exception as e:
        logging.error(f"[{client_id}] An error occurred: {e}")


async def handler(websocket) -> None:
    """
    Handles WebSocket connections.

    This function is the entry point for handling a new WebSocket connection.
    It creates a new client ID and sets up a separate process and queues for
    IPC with the client. It runs in an infinite loop until the client disconnects.
    During this time, it waits for messages from the client and processes them
    accordingly. When the client disconnects, it cleans up all resources associated
    with the client.

    Args:
        websocket: The WebSocket connection to the client.
    """
    client_id = str(uuid.uuid4())
    logging.info(f"New client connected: {client_id}")

    task_queue: Queue = Queue()
    result_queue: Queue = Queue()

    process = Process(
        target=audio_processor,
        args=(task_queue, result_queue)
    )
    process.start()

    sender_task = asyncio.create_task(transcription_sender(websocket, client_id))

    CLIENTS[client_id] = {
        "process": process,
        "task_queue": task_queue,
        "result_queue": result_queue,
        "sender_task": sender_task,
    }

    try:
        async for message in websocket:
            if isinstance(message, bytes):
                logging.info(f"[{client_id}] Received audio chunk of {len(message)} bytes.")
                task_queue.put(message)
            else:
                logging.warning(f"[{client_id}] Received non-audio message: {message}. Let's ignore it.")

    except websockets.exceptions.ConnectionClosed as e:
        logging.info(f"[{client_id}] Client disconnected: {e.code} {e.reason}")
    except Exception as e:
        logging.error(f"[{client_id}] An error occurred: {e}")
        if websocket.open:
            error_response = {"status": "error", "message": str(e)}
            await websocket.send(json.dumps(error_response))
    finally:
        logging.info(f"[{client_id}] Cleaning up resources...")

        CLIENTS[client_id]["sender_task"].cancel()
        CLIENTS[client_id]["task_queue"].put(None)

        CLIENTS[client_id]["process"].join(timeout=5)
        if CLIENTS[client_id]["process"].is_alive():
            logging.warning(f"[{client_id}] Process did not terminate within 5 seconds. Forcefully terminating...")
            CLIENTS[client_id]["process"].terminate()

        del CLIENTS[client_id]
        logging.info(f"[{client_id}] Resources cleaned. Clients count: {len(CLIENTS)}")


async def main():
    host = "0.0.0.0"  # Listen on all interfaces
    port = 8765
    try:
        async with websockets.serve(handler, host, port):
            logging.info(f"WebSocket server started on ws://{host}:{port}")
            await asyncio.Future()
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    import multiprocessing as mp
    try:
        mp.set_start_method("spawn")
    except RuntimeError:
        pass

    asyncio.run(main())