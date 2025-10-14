import cv2
import websockets
import asyncio
import json

# --- New Coroutine for Receiving Gaze Events ---
async def gaze_event_receiver(websocket):
    """
    Receives messages from the client, checking if they are text (gaze event)
    or binary (video frame, which is ignored).
    """
    try:
        async for message in websocket:
            
            # Check if the message is a string (TEXT message, like the JSON gaze event)
            if isinstance(message, str):
                try:
                    # Decode the JSON string into a Python dictionary
                    data = json.loads(message)
                    
                    # Check for the specific gaze event structure
                    if data.get("type") == "gaze_event" and "direction" in data:
                        # Success! The gaze event is received.
                        print(f"✅ Gaze Event Received: {data['direction']}")
                        
                        # OPTIONAL: If you want to broadcast this event to other clients, do it here.
                        # Example: await websocket.send(message) # Echoing back to the sender
                        
                    else:
                        print(f"Received unrecognized JSON message: {data}")
                        
                except json.JSONDecodeError:
                    print(f"Received non-JSON text message: {message}")
            
            # If the message is bytes (BINARY message, like the video frames)
            elif isinstance(message, bytes):
                # Ignore binary data since this part of the server only cares about text events
                pass
            
            else:
                print(f"Received unknown message type: {type(message)}")
                
    except websockets.exceptions.ConnectionClosed:
        print("Receiver stopped: Client disconnected.")
    except Exception as e:
        print(f"Receiver error: {e}")

# --- Modified Coroutine for Streaming and Gathering Tasks ---
async def video_streamer(websocket):
    """
    Handles both video streaming (sending) and gaze event processing (receiving)
    for the connected client concurrently.
    """
    print("Client connected.")
    # Use 0 for the default webcam
    cap = cv2.VideoCapture(0) 

    if not cap.isOpened():
        print("Error: Could not open video source.")
        return

    # Coroutine for sending the video stream
    async def video_sender():
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Encode the frame as JPEG
                ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                if not ret:
                    continue

                # Send the frame bytes to the client
                await websocket.send(buffer.tobytes())
                
                # Control frame rate
                await asyncio.sleep(0.03) 
        except websockets.exceptions.ConnectionClosed:
            print("Sender stopped: Client disconnected.")
        except Exception as e:
            print(f"Sender error: {e}")
        finally:
            # Release the webcam once the sender stops
            if cap.isOpened():
                cap.release()


    # Run both the video sender and the event receiver concurrently
    try:
        await asyncio.gather(
            video_sender(),
            gaze_event_receiver(websocket)
        )
    except Exception as e:
        print(f"Streamer process error: {e}")
    finally:
        print("Client handlers finished.")


async def main():
    # Start the WebSocket server
    host = '0.0.0.0'
    port = 8765
    print(f"Starting WebSocket server on ws://{host}:{port}")
    
    # Run the server
    async with websockets.serve(video_streamer, host, port):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped manually.")