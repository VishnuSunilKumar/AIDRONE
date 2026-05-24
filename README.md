# AI Drone

An AI-powered drone system designed for real-time human detection and facial detection using computer vision and deep learning technologies.

This project combines intelligent software modules with drone hardware to create a smart aerial monitoring system capable of live visual analysis and AI-assisted surveillance.

---

## Project Overview

The AI Drone project was developed to explore practical applications of artificial intelligence in drone systems. The project focuses on integrating computer vision models with a drone setup to enable intelligent monitoring and detection capabilities in real time.

The system currently includes:

- Human Detection Module
- Facial Detection Module
- Real-time Video Processing
- Live AI Inference
- Drone Hardware Integration
- YOLO-based Object Detection

The project demonstrates how AI can transform traditional drone systems into intelligent autonomous platforms for surveillance, monitoring, research, and automation.

---

## Hardware Setup

The drone hardware setup includes the drone frame, onboard camera system, processing environment, and AI integration components.

### Hardware Image

![Drone Setup](https://github.com/user-attachments/assets/cd7bc8d5-52bc-4551-bfaf-8a7e39685e2a)

---

## AI Detection System

The software side of the project handles live detection and intelligent processing using computer vision models.

### Human Detection

The drone can detect human presence in real time through live video streams using AI-based object detection models.

### Facial Detection

The facial detection module identifies and processes human faces from the drone camera feed for enhanced monitoring and analysis.

### AI System Images

#### Human Detection

![Human Detection](https://github.com/user-attachments/assets/59c7457a-90c0-4ddd-b9b8-c5abe672b731)

---

## Tech Stack

### AI & Computer Vision

- Python
- YOLO
- OpenCV
- NumPy

### Development Tools

- VS Code
- Git
- GitHub

### Hardware

- Drone Frame
- Camera Module
- AI Processing Environment

---

## Features

- Real-time Human Detection
- Facial Detection System
- Live Video Stream Processing
- AI-powered Monitoring
- Lightweight Detection Pipeline
- Hardware and Software Integration
- Scalable AI Architecture

---

## Repository

GitHub Repository:

```bash
https://github.com/VishnuSunilKumar/AIDRONE
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/VishnuSunilKumar/AIDRONE.git
```

Move into the project directory:

```bash
cd AIDRONE
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the project:

```bash
python app.py
```

---

## Project Structure

```bash
AIDRONE/
│
├── cascades/               # Haar cascade models for face detection
├── snapshots/              # Captured detection snapshots
├── static/                 # Static assets
├── templates/              # HTML templates for UI
├── test_images/            # Testing images
├── utils/                  # Utility/helper functions
│
├── app.py                  # Main application entry point
├── av_usb_check.py         # USB camera checking module
├── face.py                 # Facial detection module
├── lap_webcam_check.py     # Webcam testing/check module
├── requirements.txt        # Project dependencies
└── README.md
```

---

## Future Improvements

- Autonomous Navigation
- GPS Integration
- Advanced Object Tracking
- Obstacle Avoidance
- Cloud Monitoring Dashboard
- Mobile Application Integration

---

## Contributors

### Vishnu Sunil Kumar

AI | Software Development | Computer Vision

---

## Project Status

Completed and open for future improvements, research, and advanced AI drone integrations.

---

## License

This project is intended for educational, research, and learning purposes.
