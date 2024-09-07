from flask import Flask, render_template, Response, request
import cv2
import numpy as np
import threading
import main

app = Flask(__name__)

camera_active = False
cap = None
background = None
frame_generator_thread = None

# Define color ranges for masking (you may need to adjust these as per your need)
lower1 = np.array([90, 50, 50])
upper1 = np.array([130, 255, 255])
lower2 = np.array([110, 50, 50])
upper2 = np.array([140, 255, 255])

def generate_frames():
    global cap, background
    while camera_active:
        success, frame = cap.read()  # Read frame from webcam
        if not success:
            break

        # Process the frame using functions from main.py
        mask = main.masking(frame, lower1, upper1, lower2, upper2)
        result = main.cloak_effect(frame, mask, background)
        
        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', result)
        frame = buffer.tobytes()

        # Yield frame as response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_camera')
def start_camera():
    global camera_active, cap, background, frame_generator_thread
    if not camera_active:
        camera_active = True
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return "Error: Could not open camera", 500
        try:
            background = main.background_create(cap)
        except ValueError as e:
            return f"Error: {e}", 500
        frame_generator_thread = threading.Thread(target=generate_frames)
        frame_generator_thread.start()
        return "Camera started"
    return "Camera already active"

@app.route('/stop_camera')
def stop_camera():
    global camera_active, cap
    if camera_active:
        camera_active = False
        cap.release()
        if frame_generator_thread is not None:
            frame_generator_thread.join()
        return "Camera stopped"
    return "Camera is not active"

@app.route('/video_feed')
def video_feed():
    if camera_active:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "Camera is not active", 503

if __name__ == '__main__':
    app.run(debug=True)
