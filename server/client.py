import cv2
import numpy as np
import websockets
import asyncio
import threading
import time

class WebSocketVideoStream:
    """
    A class to receive a video stream from a WebSocket and behave like cv2.VideoCapture.
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
        # Give the connection a moment to establish
        time.sleep(2) 
        print("Client thread started.")

    async def _receiver(self):
        """The core coroutine to connect to the WebSocket and receive frames."""
        async with websockets.connect(self.websocket_url) as websocket:
            print(f"Connected to WebSocket server at {self.websocket_url}")
            async for message in websocket:
                # Assuming the message is the raw bytes of a JPEG image
                np_arr = np.frombuffer(message, np.uint8)
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
        The boolean is True if a frame is available, False otherwise.
        """
        with self.lock:
            if self.latest_frame is not None:
                # Return a copy to prevent race conditions
                return True, self.latest_frame.copy()
            else:
                return False, None

    def isOpened(self):
        """Mimics the cv2.VideoCapture.isOpened() method."""
        return self.is_running and self.latest_frame is not None

    def stop(self):
        """Stops the client."""
        print("Stopping WebSocket client.")
        self.is_running = False
        # The thread will exit because the asyncio loop will end when the connection is closed
        # or an error occurs. Since it's a daemon, it will be cleaned up automatically.


# --- Main execution block to demonstrate usage ---
if __name__ == "__main__":
    # ⚠️ IMPORTANT: Replace with the actual URL of your WebSocket server
    WEBSOCKET_URL = "ws://192.168.14.111:8765"

    # Here is what you asked for: initialising 'webcam' with your video stream
    webcam = WebSocketVideoStream(WEBSOCKET_URL)
    webcam.start()

    if not webcam.isOpened():
        print("Error: Could not connect to WebSocket stream. Please ensure the server is running.")
    else:
        print("Successfully connected to stream. Press 'q' to quit.")
        while True:
            # The usage is now identical to cv2.VideoCapture
            ret, frame = webcam.read()

            if not ret:
                print("Waiting for frame...")
                time.sleep(0.1)
                continue
            
            # Display the resulting frame
            cv2.imshow('WebSocket Video Stream', frame)

            # Press 'q' on the keyboard to exit the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Clean up
    webcam.stop()
    cv2.destroyAllWindows()
    print("Stream stopped and windows closed.")