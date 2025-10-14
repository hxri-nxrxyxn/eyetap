# client.py
import cv2
import numpy as np
import websockets
import asyncio
import threading
import time
import base64

class WebSocketVideoStream:
    """
    Receives a Base64 encoded video stream from a WebSocket and
    behaves like a cv2.VideoCapture object.
    """
    def __init__(self, websocket_url):
        self.websocket_url = websocket_url
        self.latest_frame = None
        self.is_running = False
        self.lock = threading.Lock()
        
        # Start the thread that will connect and receive frames
        self.thread = threading.Thread(target=self._run_client, daemon=True)

    def start(self):
        """Starts the WebSocket client thread."""
        print("Starting WebSocket client thread...")
        self.is_running = True
        self.thread.start()

    async def _receiver(self):
        """The core coroutine to connect and receive frames."""
        async with websockets.connect(self.websocket_url) as websocket:
            print(f"✅ Connected to WebSocket server at {self.websocket_url}")
            async for message in websocket:
                # Decode the Base64 string back to bytes
                decoded_data = base64.b64decode(message)
                
                # Convert bytes to a NumPy array for OpenCV
                np_arr = np.frombuffer(decoded_data, np.uint8)
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                
                # Use a lock to safely update the latest frame
                with self.lock:
                    self.latest_frame = frame

    def _run_client(self):
        """Runs the asyncio event loop in a separate thread."""
        try:
            asyncio.run(self._receiver())
        except Exception as e:
            print(f"WebSocket client error: {e}")
        finally:
            self.is_running = False

    def read(self):
        """
        Mimics the cv2.VideoCapture.read() method.
        Returns a tuple (boolean, frame).
        """
        with self.lock:
            if self.latest_frame is not None:
                # Return a copy to prevent race conditions
                return True, self.latest_frame.copy()
            else:
                return False, None

    def stop(self):
        """Stops the client."""
        print("Stopping WebSocket client.")
        self.is_running = False

# --- Main execution block to demonstrate usage ---
if __name__ == "__main__":
    # ⚠️ IMPORTANT: Replace with the actual IP of your server
    WEBSOCKET_URL = "ws://localhost:8765" 

    webcam = WebSocketVideoStream(WEBSOCKET_URL)
    webcam.start()

    print("Connecting to stream... Press 'q' to quit.")

    # Robust loop that patiently waits for the first frame
    while True:
        ret, frame = webcam.read()

        if not ret:
            print("⏳ Waiting for first frame...")
            time.sleep(0.5)
            continue
        
        # Display the resulting frame
        cv2.imshow('WebSocket Base64 Video Stream', frame)

        # Press 'q' on the keyboard to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up
    webcam.stop()
    cv2.destroyAllWindows()
    print("Stream stopped and windows closed.")