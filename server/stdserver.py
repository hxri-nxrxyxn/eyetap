import cv2
import websockets
import asyncio
import json
import numpy as np # Import NumPy

# --- Coroutine for processing messages ---
async def message_handler(websocket):
    """
    Receives and processes messages from the client.
    Handles both binary video frames and text-based gaze events.
    """
    try:
        async for message in websocket:
            # 1. CHECK IF THE MESSAGE IS BINARY (A VIDEO FRAME)
            if isinstance(message, bytes):
                # Convert the byte data to a NumPy array
                np_arr = np.frombuffer(message, np.uint8)
               
                # Decode the NumPy array as a JPEG image
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                # --- DO YOUR IMAGE PROCESSING HERE ---
                # For demonstration, we'll just display the frame in a window.
                if frame is not None:
                    cv2.imshow("Webcam Stream", frame)
                    # Exit if 'q' is pressed
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                # ----------------------------------------
           
            # 2. CHECK IF THE MESSAGE IS TEXT (A JSON EVENT)
            elif isinstance(message, str):
                try:
                    data = json.loads(message)
                    if data.get("type") == "gaze_event" and "direction" in data:
                        print(f"✅ Gaze Event Received: {data['direction']}")
                    else:
                        print(f"Received unrecognized JSON message: {data}")
                except json.JSONDecodeError:
                    print(f"Received non-JSON text message: {message}")

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up the OpenCV window when done
        cv2.destroyAllWindows()


async def main():
    host = '0.0.0.0'
    port = 8765
    print(f"Starting WebSocket server on ws://{host}:{port}")
   
    # Increase the max message size to handle larger video frames
    async with websockets.serve(message_handler, host, port, max_size=1024*1024*4):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped manually.")