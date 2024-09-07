# Invisibility Cloak Using OpenCV and Flask

This project creates an "invisibility cloak" effect using OpenCV and Python, and it is integrated into a Flask web application. The application captures a background, identifies specific cloak colors, and makes the wearer appear invisible by blending the cloak with the background.

## Features

- Real-time "invisibility" effect using a webcam.
- Detects cloak color and blends it with the background to create the illusion of invisibility.
- Flask web application interface for controlling the effect.
- Live video stream displayed on a web page.

## Requirements

- Python 3.x
- OpenCV
- NumPy
- Flask

## Usage

1. **Run the Flask app:**

    ```bash
    python app.py
    ```

2. **Open your browser and go to `http://localhost:5000`.**

3. **Click "Start Camera" to begin the effect.**

4. **Click "Stop Camera" to terminate the camera process.**

