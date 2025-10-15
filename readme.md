# EyeTap

https://github.com/user-attachments/assets/4a6ecfcb-70d0-4287-bc30-58f808343ac5


EyeTap is an assistive **web and mobile application** designed for **bedridden patients**, such as those who are paralyzed, injured, or unable to move freely.
It enables users to interact with a system **using only their eye movements**, providing them with autonomy and a way to communicate or request help effortlessly.

---

## Project Overview

EyeTap monitors **eye movements** in real-time using a device's camera feed.
The captured video is streamed from the **frontend (SvelteKit)** to the **Python backend** through **WebSockets**, where it is analyzed using the **GazeTracking** library.

Based on the direction and pattern of the user’s gaze, the system triggers corresponding actions in the app.

---

## Core Functionalities

Eye movements are used to select specific actions as follows:

| Eye Movement     | Action Triggered | Description                                                                          |
| ---------------- | ---------------- | ------------------------------------------------------------------------------------ |
| Move Left Once   | **Greet** | Selects the "Greet" option. After a short timeout, the system confirms the selection. |
| Move Left Twice  | **Food** | Selects the "Food" option, useful for requesting meals or related assistance.        |
| Move Right Once  | **Help** | Selects the "Help" option. After a short timeout, the system confirms the selection. |
| Move Right Twice | **Binge** | Selects the "Binge" option, typically for entertainment or relaxation requests.      |

This gaze-based selection allows users to **perform actions without physical interaction**, making it ideal for **assistive healthcare environments**.

---

## Tech Stack

### 🔹 Frontend

-   **Framework:** [SvelteKit](https://kit.svelte.dev/)
-   **Mobile Integration:** [CapacitorJS](https://capacitorjs.com/) — Used to package the web app into a native **Android application**.
-   **Purpose:** Captures live camera video and provides an intuitive user interface on both web and mobile.
-   **Communication:** Streams video frames to the backend as JPEG blobs using WebSockets for efficiency.

### 🔹 Backend

-   **Language:** Python
-   **WebSocket Communication:** Used to receive live frames from the frontend and send back gaze-based responses.
-   **Tool Used:** [GazeTracking](https://github.com/antoinelame/GazeTracking) — for detecting eye movement direction and gaze position.

---

## System Architecture

1.  **Frontend (SvelteKit + CapacitorJS):**
    -   Captures camera feed using browser or native device APIs.
    -   Converts each frame into a **JPEG blob** for efficient streaming.
    -   Sends the blob data to the Python backend via WebSocket.

2.  **Backend (Python + GazeTracking):**
    -   Receives the frame stream.
    -   Processes frames in real-time using GazeTracking.
    -   Determines gaze direction (left, right, or center).
    -   Detects the number of consecutive movements (single or double).
    -   Sends corresponding action updates (Greet, Help, Food, Binge) back to the frontend.

---

## Installation & Setup

### Prerequisites

-   Python 3.8+
-   A WebSocket-compatible browser or an Android device
-   A working webcam or phone camera

### Steps

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/eyetap.git](https://github.com/yourusername/eyetap.git)
    ```
2.  **Backend Setup**
    ```bash
    cd backend
    pip install -r requirements.txt
    python app.py
    ```
3.  **Frontend Setup**
    -   Follow the specific build and run instructions provided in the `frontend` directory for deploying the web app or building the Android application.
