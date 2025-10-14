# server.py
import cv2
import websockets
import asyncio
import base64

async def video_streamer(websocket):
    """
    Captures video from the webcam, encodes it to Base64, and streams it.
    """
    print("✅ Client connected.")
    # Use 0 for the default webcam. Change to 1, 2, etc., if you have multiple cameras.
    cap = cv2.VideoCapture(0) 

    if not cap.isOpened():
        print("❌ Error: Could not open video source.")
        return

    try:
        while cap.isOpened():
            # Read a frame from the webcam
            ret, frame = cap.read()
            if not ret:
                print("⚠️ Warning: Could not read frame. Stopping stream.")
                break
            
            # Encode the frame as JPEG with 80% quality
            ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            if not ret:
                continue

            # Encode the JPEG bytes to a Base64 string
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')

            # Send the Base64 string to the client
            await websocket.send(jpg_as_text)
            
            # Control the frame rate (e.g., ~30 FPS)
            await asyncio.sleep(0.03) 
    except websockets.exceptions.ConnectionClosed:
        print("🔌 Client disconnected.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Release the webcam when the stream is done
        cap.release()
        print("Camera released.")

async def main():
    host = '0.0.0.0' # Listen on all available network interfaces
    port = 8765
    print(f"🚀 Starting WebSocket server on ws://{host}:{port}")
    async with websockets.serve(video_streamer, host, port):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())