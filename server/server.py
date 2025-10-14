import cv2
import websockets
import asyncio

# The ONLY change is on the next line: remove ', path'
async def video_streamer(websocket):
    """
    Captures video from the webcam and streams it to the connected client.
    """
    print("Client connected.")
    # Use 0 for the default webcam
    cap = cv2.VideoCapture(0) 

    if not cap.isOpened():
        print("Error: Could not open video source.")
        return

    try:
        while cap.isOpened():
            # Read a frame from the webcam
            ret, frame = cap.read()
            if not ret:
                break
            
            # Encode the frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            if not ret:
                continue

            # Send the frame bytes to the client
            await websocket.send(buffer.tobytes())
            
            await asyncio.sleep(0.03) 
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected.")
    finally:
        # Release the webcam
        cap.release()

async def main():
    # Start the WebSocket server
    host = '0.0.0.0'
    port = 8765
    print(f"Starting WebSocket server on ws://{host}:{port}")
    # The call to websockets.serve remains the same
    async with websockets.serve(video_streamer, host, port):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())