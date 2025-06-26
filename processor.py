import time
import logging
from multiprocessing import Queue

logger = logging.getLogger(__name__)

def audio_processor(task_queue: Queue, result_queue: Queue):
    """
    Processes audio chunks from the task queue and sends transcriptions to the result queue.

    This function runs in an infinite loop, continuously retrieving audio chunks from the
    provided task queue. Each audio chunk is processed to generate a mock transcription,
    which is then placed into the result queue. If a None value is received from the task
    queue, it signals the function to terminate its execution. The function logs various
    stages of processing, including the receipt and processing of audio chunks, and any
    errors that occur during execution.

    Args:
        task_queue (Queue): The queue from which audio chunks are retrieved for processing.
        result_queue (Queue): The queue to which the resulting transcriptions are sent.
    """

    logger.info("Run audio processor...")

    while True:
        try:
            audio_chunk = task_queue.get()

            if audio_chunk is None:
                logger.info("Received None from task queue. Exiting...")
                break

            logger.info(f"Received audio chunk of {len(audio_chunk)} bytes. Processing...")

            # --- Imitate processing delay ---
            time.sleep(0.5)
            # ---------------------------------

            transcript = f"It's a mock transcription of {len(audio_chunk)}"
            result_queue.put(transcript)
            logger.info(f"Transcript '{transcript}' sent to result queue.")

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            break

    logger.info("Processor exited.")