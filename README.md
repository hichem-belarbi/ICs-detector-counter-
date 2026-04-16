# Component Counter 

<p align="center">
  <strong>Real-time electronic component detection and counting using YOLOv8</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python">
  <img src="https://img.shields.io/badge/YOLOv8-Ultralytics-red">
  <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-green">
  <img src="https://img.shields.io/badge/PyQt5-Desktop%20UI-orange">
</p>

---

## Overview

This application provides an automated solution for detecting and counting electronic components in real time. It uses a deep learning model trained on a labeled dataset of components, allowing it to recognize and count multiple objects simultaneously from a video stream.

The system is designed to be simple to use while delivering reliable results in practical scenarios such as labs, workshops, or demonstrations.

---

## How It Works

The application relies on a YOLOv8 object detection model trained on a custom dataset of electronic components.

* The model processes each frame from the camera in real time
* It detects and localizes components using bounding boxes
* Each detected object is classified (resistor, capacitor, IC, etc.)
* The system counts the number of detected components per frame
* A target quantity can be defined, and the system tracks progress toward it

When the target is reached or exceeded:

* A visual indicator updates the status
* An audio alert is triggered

---

## Features

* Real-time object detection and counting
* Support for webcam and DroidCam (mobile camera)
* Configurable target count per component type
* Visual feedback with progress tracking
* Audio alert when the target is reached
* Snapshot capture for analysis or documentation
* Clean desktop interface built with PyQt5

---

## Model

The application uses a YOLOv8 model trained on a labeled dataset of electronic components.

You can:

* Use your own trained model
* Replace the provided `.pt` file with another compatible YOLOv8 model

Training can be done using the Ultralytics framework on custom datasets.

---

## Usage

1. A trained model already exists (best (1).pt) but you can place your trained YOLOv8 model (`.pt`) in the project directory 
2. Run the application:

```bash
python main.py
```

3. Select a camera source
4. Choose the target component and quantity
5. Start detection

The system will process the video stream and display results in real time.

---

## Screenshot

![Application Screenshot](screenshots/ss.jfif)



---

## License

MIT
