# BYOP-Vityarthi-Computer-Vision-
# Real-Time Drowsiness Detection System

## Project Description

This is a simple yet effective command-line Computer Vision project built in Python. It utilizes OpenCV and pre-trained Haar Cascades to detect a person's face and eyes using a webcam feed in real-time. 

If the system detects that the user's eyes have been closed (or are undetectable within the face region) for a continuous number of frames (set to 15), it triggers a visual **"DROWSINESS ALERT"** warning and emits an audible beep sound on Windows to wake the user up. 

## Technical Highlights
- Developed with Python & OpenCV (`cv2`).
- Relies on lightweight Haar Cascades for rapid and efficient object tracking, minimizing the need for complex machine learning models or GPU acceleration.
- Fully runnable via standard Terminal/Command Prompt without needing an elaborate Graphical User Interface (GUI).
- Runs an asynchronous alert sound (`winsound.Beep`) so it doesn't freeze the camera frame rate when a user gets drowsy.

## Prerequisites

Before running the application, ensure you have Python installed on your system.

## Installation Steps

1. **Navigate to the Project Directory:**
   ```bash
   cd C:\Users\Acer\.gemini\antigravity\scratch\drowsiness-detection
   ```

2. **(Optional but recommended) Create a Virtual Environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

1. Simply run the main Python script from your terminal:
   ```bash
   python main.py
   ```
2. Your system's default webcam should turn on, displaying:
    - Bounding boxes outlining your face (blue) and open eyes (green circles).
    - Status text indicating whether you are "Awake", "Eyes Closed", or triggering a "DROWSINESS ALERT!!!".
3. **To stop the project**, click on the video feed window and press the **`q`** key on your keyboard. 

## Project Architecture
- `main.py`: Contains the logic for webcam initialization, frame preprocessing, object tracking, and alert triggering.
- `requirements.txt`: Outlines the necessary Python package (`opencv-python`).
- `haarcascade_frontalface_default.xml`: Core definitions needed by OpenCV for face detection.
- `haarcascade_eye.xml`: Core definitions needed by OpenCV for eye detection.
