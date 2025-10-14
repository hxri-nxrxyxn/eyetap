import cv2
import websockets
import asyncio
import json
import numpy as np

connected_clients = set()

async def message_handler(websocket):
    """
    Handles incoming frames and gaze events from clients.
    Forwards frames and optionally gaze events to all other clients.
    """
    connected_clients.add(websocket)
    print(f"Client connected. Total clients: {len(connected_clients)}")

    try:
        async for message in websocket:
            # 1. Binary frame (JPEG image)
            if isinstance(message, bytes):
                await broadcast_to_others(websocket, message)

            # 2. JSON gaze event or other message
            elif isinstance(message, str):
                try:
                    data = json.loads(message)
                    if data.get("type") == "gaze_event":
                        print(f"✅ Gaze Event Received: {data['direction']} (From: {websocket.remote_address})")
                        # Optionally broadcast gaze events
                        # await broadcast_to_others(websocket, message)
                    else:
                        print(f"Unrecognized JSON message: {data}")
                except json.JSONDecodeError:
                    print(f"Received invalid JSON: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connected_clients.remove(websocket)
        print(f"Client removed. Total clients: {len(connected_clients)}")

async def broadcast_to_others(sender, message):
    """
    Sends the message to all connected clients except the sender.
    """
    recipients = [client for client in connected_clients if client != sender and client.open]
    if recipients:
        await asyncio.gather(*(client.send(message) for client in recipients))

async def main():
    host = '0.0.0.0'
    port = 8765
    print(f"Relay server running at ws://{host}:{port}")

    async with websockets.serve(message_handler, host, port, max_size=4 * 1024 * 1024):
        await asyncio.Future()  # Keep running

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server shut down.")
