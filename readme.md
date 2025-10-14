#  EyeTap

EyeTap is an assistive web application designed for **bedridden patients** such as those who are **paralyzed, injured, or unable to move freely**.  
It enables users to interact with a system **using only their eye movements**, providing them with autonomy and a way to communicate or request help effortlessly.

---

##  Project Overview

EyeTap monitors **eye movements** in real-time using a webcam feed.  
The captured video is streamed from the **frontend (SvelteKit)** to the **backend (Python Flask)** through **WebSockets**, where it is analyzed using the **GazeTracking** tool.  

Based on the direction and pattern of the user’s gaze, the system triggers corresponding actions in the web app.

---

##  Core Functionalities

Eye movements are used to select specific actions as follows:

| Eye Movement | Action Triggered | Description |
|---------------|------------------|--------------|
|  Move Left Once | **Greet** | Selects the "Greet" option. After a short timeout, the system confirms the selection. |
|  Move Left Twice | **Food** | Selects the "Food" option. Useful for requesting meals or assistance related to food. |
|  Move Right Once | **Help** | Selects the "Help" option. After a short timeout, the system confirms the selection. |
|  Move Right Twice | **Binge** | Selects the "Binge" option, typically for entertainment or relaxation requests. |

This gaze-based selection allows users to **perform actions without physical interaction**, making it ideal for **assistive healthcare environments**.

---

##  Tech Stack

### 🔹 Frontend
- **Framework:** [SvelteKit](https://kit.svelte.dev/)  
- **Purpose:** Captures live webcam video and provides an intuitive user interface.  
- **Communication:** Streams video frames to the backend using WebSockets.  

### 🔹 Backend
- **Language:** Python  
- **Framework:** Flask  
- **WebSocket Communication:** Used to receive live frames from the frontend and send back gaze-based responses.  
- **Tool Used:** [GazeTracking](https://github.com/antoinelame/GazeTracking) — for detecting eye movement direction and gaze position.

---

##  System Architecture

1. **Frontend (SvelteKit):**
   - Captures webcam feed using browser APIs.
   - Encodes each frame in base64.
   - Sends frames to the Flask backend via WebSocket.

2. **Backend (Flask + GazeTracking):**
   - Receives the frame stream.
   - Processes frames in real time using GazeTracking.
   - Determines gaze direction (left, right, or center).
   - Detects the number of consecutive movements (single or double).
   - Sends corresponding action updates (Greet, Help, Food, Binge) to the frontend.

---

##  Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js & npm
- WebSocket-compatible browser
- Working webcam

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/eyetap.git
   ```
2.**Backend Setup**
  ```bash
  cd backend
  pip install -r requirements.txt
  python app.py
 ```
3.**Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```



