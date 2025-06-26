import asyncio
import websockets
import random

async def send_audio_chunks():
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to {uri}")

            async def receive_messages():
                try:
                    async for message in websocket:
                        print(f"< Received from server: {message}")
                except websockets.exceptions.ConnectionClosed:
                    print("Connection closed.")

            receiver_task = asyncio.create_task(receive_messages())

            for i in range(5):
                chunk_size = random.randint(1024, 4096)
                fake_audio_chunk = b'\x00' * chunk_size

                try:
                    await websocket.send(fake_audio_chunk)
                    print(f"> Sent chunk {i+1} of {len(fake_audio_chunk)} bytes")
                except Exception as e:
                    print(f"Failed to send chunk {i+1}: {e}")
                    break
                
                await asyncio.sleep(3)

            print("All chunks were sent to the server. Waiting for the server to process them...")
            await asyncio.sleep(3)

            receiver_task.cancel()
            try:
                await receiver_task
            except asyncio.CancelledError:
                pass

            print("All chunks were processed. Closing the connection...")
            await websocket.close()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(send_audio_chunks())