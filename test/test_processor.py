import pytest
from multiprocessing import Queue
from src.processor import audio_processor
import threading


def run_processor(task_queue, result_queue):
    audio_processor(task_queue, result_queue)


def test_audio_processor_puts_transcription():
    task_queue = Queue()
    result_queue = Queue()
    
    # Start the processor in a separate thread
    processor_thread = threading.Thread(target=run_processor, args=(task_queue, result_queue))
    processor_thread.start()

    # Send a mock audio chunk
    fake_audio_chunk = b'\x00' * 2048
    task_queue.put(fake_audio_chunk)
    # Signal the processor to exit
    task_queue.put(None)

    # Wait for the processor to finish
    processor_thread.join(timeout=2)

    # Check the result
    transcript = result_queue.get(timeout=1)
    assert transcript == "It's a mock transcription of 2048"