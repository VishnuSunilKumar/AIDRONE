from flask import Flask, render_template, Response, jsonify, request
import cv2
import threading
import os
import datetime
import numpy as np
import torch

device = 0 if torch.cuda.is_available() else "cpu"

# Try to import YOLOv8
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("Warning: ultralytics not available. Human detection disabled.")

app = Flask(__name__)

# ---------------- FACE DETECTOR ----------------
face_cascade = cv2.CascadeClassifier(
    'cascades/haarcascade_frontalface_default.xml'
)

# ---------------- YOLO MODEL ----------------
yolo_model = None

yolo_model_paths = [
    "weights/yolov8n.pt",
    r"C:\Users\vishn\OneDrive\Desktop\AI DRONE S8\human detectiin\yolov8-silva\weights\yolov8n.pt",
]

if YOLO_AVAILABLE:
    try:
        yolo_model_path = None

        for path in yolo_model_paths:
            if os.path.exists(path):
                yolo_model_path = path
                break

        if yolo_model_path:
            yolo_model = YOLO(yolo_model_path)
            print("YOLOv8 model loaded:", yolo_model_path)
        else:
            print("YOLO model not found.")

    except Exception as e:
        print("YOLO loading error:", e)
        yolo_model = None


# ---------------- GLOBAL VARIABLES ----------------

INPUT_MODE = "webcam"

# Laptop webcam
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# AV → USB capture card
live_camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)

face_count = 0
human_count = 0

frame_lock = threading.Lock()
current_frame = None

image_path = os.path.join("test_images", "testimg4.jpg")

os.makedirs("snapshots", exist_ok=True)


# ---------------- FRAME GENERATOR ----------------

def generate_frames():
    global face_count, human_count, current_frame, INPUT_MODE

    while True:

        # -------- SELECT INPUT SOURCE --------

        if INPUT_MODE == "webcam":

            success, frame = camera.read()
            if not success:
                continue

        elif INPUT_MODE == "live":

            success, frame = live_camera.read()
            if not success:
                continue

        elif INPUT_MODE == "image":

            if not os.path.exists(image_path):
                print("Test image missing")
                continue

            frame = cv2.imread(image_path)

        else:
            continue

        frame_resized = frame.copy()

        # -------- FACE DETECTION --------

        gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5
        )

        face_count = len(faces)

        for (x, y, w, h) in faces:

            cv2.rectangle(
                frame_resized,
                (x, y),
                (x + w, y + h),
                (255, 100, 0),
                1
            )

            cv2.putText(
                frame_resized,
                "FACE-TGT",
                (x, y - 5),
                cv2.FONT_HERSHEY_PLAIN,
                1.2,
                (255, 100, 0),
                1
            )

        # -------- HUMAN DETECTION --------

        human_count = 0

        if yolo_model is not None:

            try:

                results = yolo_model(
                    frame_resized,
                    conf=0.25,
                    imgsz=1280,
                    device=device
                )

                for r in results:

                    for box in r.boxes:

                        clsID = int(box.cls[0])

                        if clsID == 0:   # person

                            human_count += 1

                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            conf = float(box.conf[0])

                            cv2.rectangle(
                                frame_resized,
                                (x1, y1),
                                (x2, y2),
                                (0, 255, 100),
                                1
                            )

                            cv2.putText(
                                frame_resized,
                                f"HMN-TGT {conf:.2f}",
                                (x1, y1 - 5),
                                cv2.FONT_HERSHEY_PLAIN,
                                1.2,
                                (0, 255, 100),
                                1
                            )

            except Exception as e:
                print("YOLO error:", e)

        # -------- DISPLAY COUNTS --------

        cv2.putText(
            frame_resized,
            f"SYS::FACE_CNT: {face_count}",
            (10, 25),
            cv2.FONT_HERSHEY_PLAIN,
            1.5,
            (255, 100, 0),
            2
        )

        cv2.putText(
            frame_resized,
            f"SYS::HMN_CNT: {human_count}",
            (10, 55),
            cv2.FONT_HERSHEY_PLAIN,
            1.5,
            (0, 255, 100),
            2
        )

        # -------- SAVE FRAME --------

        with frame_lock:
            current_frame = frame_resized.copy()

        ret, buffer = cv2.imencode('.jpg', frame_resized)
        frame_bytes = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame_bytes +
            b'\r\n'
        )


# ---------------- API ROUTES ----------------

@app.route('/api/mode', methods=['POST'])
def set_mode():
    global INPUT_MODE

    data = request.get_json()
    mode = data.get("mode")

    if mode in ["webcam", "image", "live"]:

        INPUT_MODE = mode

        return jsonify({
            "message": f"Mode switched to {mode}"
        })

    return jsonify({"error": "Invalid mode"}), 400


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():

    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/api/face_count')
def get_face_count():

    return jsonify({
        'face_count': face_count,
        'human_count': human_count
    })


@app.route('/api/snapshot', methods=['POST'])
def take_snapshot():

    global current_frame

    if current_frame is not None:

        filename = f"snapshots/snapshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

        with frame_lock:
            cv2.imwrite(filename, current_frame)

        return jsonify({
            'message': 'Snapshot saved',
            'filename': filename
        })

    return jsonify({'error': 'No frame available'}), 400


# ---------------- LOCATION API ----------------

device_location = {'lat': None, 'lng': None}


@app.route('/api/location', methods=['POST'])
def update_location():

    data = request.get_json()

    device_location['lat'] = data.get('lat')
    device_location['lng'] = data.get('lng')

    return jsonify({'message': 'Location updated'})


@app.route('/api/location', methods=['GET'])
def get_location():

    return jsonify(device_location)


# ---------------- START SERVER ----------------

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000
    )