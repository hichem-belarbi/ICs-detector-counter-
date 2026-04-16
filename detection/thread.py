from ultralytics import YOLO
import time

from collections import defaultdict

import cv2
import numpy as np

from PyQt5.QtCore import QThread, pyqtSignal


class DetectionThread(QThread):
    """Thread de détection YOLO en temps réel."""

    frame_ready    = pyqtSignal(np.ndarray, dict, int)
    error_occurred = pyqtSignal(str)

    def __init__(self, model_path: str, camera_index: int = 0, conf: float = 0.5):
        super().__init__()
        self.model_path   = model_path
        self.camera_index = camera_index
        self.conf         = conf
        self.running      = False
        self.paused       = False
        self.model        = None

    # ── Cycle de vie ────────────────────────────────────────────────────────

    def run(self):
        try:
            self.model = YOLO(self.model_path)
        except Exception as exc:
            self.error_occurred.emit(f"Impossible de charger le modèle : {exc}")
            return

        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            self.error_occurred.emit("Impossible d'ouvrir la caméra.")
            return

        cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.running = True

        while self.running:
            if self.paused:
                time.sleep(0.05)
                continue

            ret, frame = cap.read()
            if not ret:
                continue

            results  = self.model(frame, conf=self.conf, verbose=False)
            boxes    = results[0].boxes
            counts: dict[str, int] = defaultdict(int)

            for cls in boxes.cls:
                name = self.model.names[int(cls)]
                counts[name] += 1

            annotated = results[0].plot()
            total     = int(sum(counts.values()))
            self.frame_ready.emit(annotated, dict(counts), total)

        cap.release()

    def stop(self):
        self.running = False

    # ── Setters thread-safe ──────────────────────────────────────────────────

    def set_conf(self, value: float):
        self.conf = value
