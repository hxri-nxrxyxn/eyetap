import cv2
import websockets
import asyncio
import json

# --- Coroutine for Receiving Gaze Events ---
async def gaze_event_receiver(websocket):
    """
    Receives messages from the client, checking if they are text (gaze event)
    or binary (video frame, which is ignored).
    """
    try:
        async for message in websocket:
            if isinstance(message, str):
                try:
                    data = json.loads(message)
                    if data.get("type") == "gaze_event" and "direction" in data:
                        print(f"✅ Gaze Event Received: {data['direction']}")
                    else:
                        print(f"Received unrecognized JSON message: {data}")
                except json.JSONDecodeError:
                    print(f"Received non-JSON text message: {message}")
            elif isinstance(message, bytes):
                # If clients send video frames, ignore them here
                pass
            else:
                print(f"Received unknown message type: {type(message)}")
    except websockets.exceptions.ConnectionClosed:
        print("Receiver stopped: Client disconnected.")
    except Exception as e:
        print(f"Receiver error: {e}")


# --- Modified Coroutine: Only Receiving, No Sending ---
async def client_handler(websocket):
    """
    Handles gaze event processing only. Assumes video is sent from client to server.
    """
    print("Client connected.")
    try:
        await gaze_event_receiver(websocket)
    except Exception as e:
        print(f"Handler error: {e}")
    finally:
        print("Client handler finished.")


async def main():
    # Start the WebSocket server
    host = '0.0.0.0'
    port = 8765
    print(f"Starting WebSocket server on ws://{host}:{port}")
    
    async with websockets.serve(client_handler, host, port):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped manually.")
