from detection import DetectionThread
import time

import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStatusBar, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap

from utils import play_buzzer
from ui.styles import Palette, build_stylesheet
from ui.panels import CameraPanel, ControlPanel


class ComponentCounter(QMainWindow):
    """
    Fenêtre principale de l'application Component Counter.
    Orchestre le thread de détection et les deux panneaux UI.
    """

    def __init__(self):
        super().__init__()

        self._detection_thread: DetectionThread | None = None
        self._last_frame: np.ndarray | None = None
        self._current_counts: dict = {}
        self._total_detected: int = 0
        self._buzzer_played: bool = False
        self._buzzer_enabled: bool = True
        self._model_path: str = "best (1).pt"
        self._snapshot_dir: str = "."
        self._palette = Palette()

        self._build_ui()
        self.setStyleSheet(build_stylesheet(self._palette))
        self.setWindowTitle("Component Counter")
        self.resize(1400, 860)

    # ── Construction UI ──────────────────────────────────────────────────────

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        self._cam_panel  = CameraPanel()
        self._ctrl_panel = ControlPanel(self._palette)

        root.addWidget(self._cam_panel, 3)
        root.addWidget(self._ctrl_panel, 1)

        self._status_bar = QStatusBar()
        self.setStatusBar(self._status_bar)
        self._status_bar.showMessage("Prêt — chargez un modèle et démarrez la caméra.")

        self._cam_panel.start_requested.connect(self._start)
        self._cam_panel.pause_requested.connect(self._pause)
        self._cam_panel.stop_requested.connect(self._stop)
        self._cam_panel.snapshot_requested.connect(self._snapshot)
        self._cam_panel.model_requested.connect(self._pick_model)
        self._cam_panel.conf_changed.connect(self._on_conf_changed)

        self._ctrl_panel.target_count_changed.connect(self._on_target_changed)
        self._ctrl_panel.class_changed.connect(self._on_class_changed)
        self._ctrl_panel.reset_requested.connect(self._reset_counter)
        self._ctrl_panel.buzzer_toggled.connect(self._on_buzzer_toggled)

    # ── Contrôle de la détection ─────────────────────────────────────────────

    def _start(self):
        self._detection_thread = DetectionThread(
            self._model_path,
            self._cam_panel.selected_camera,
            self._cam_panel.confidence,
        )
        self._detection_thread.frame_ready.connect(self._on_frame)
        self._detection_thread.error_occurred.connect(self._on_error)
        self._detection_thread.start()

        self._cam_panel.set_running(True)
        self._status_bar.showMessage("Détection en cours…")

    def _pause(self):
        if not self._detection_thread:
            return
        self._detection_thread.paused = not self._detection_thread.paused
        paused = self._detection_thread.paused
        self._cam_panel.set_paused(paused)
        self._status_bar.showMessage("En pause" if paused else "Détection en cours…")

    def _stop(self):
        if self._detection_thread:
            self._detection_thread.stop()
            self._detection_thread.wait()
            self._detection_thread = None

        self._cam_panel.set_running(False)
        self._cam_panel.set_paused(False)
        self._cam_panel.reset_feed()
        self._status_bar.showMessage("Arrêté.")

    # ── Slots des panneaux ───────────────────────────────────────────────────

    def _snapshot(self):
        if self._last_frame is None:
            return
        fname = f"{self._snapshot_dir}/snapshot_{int(time.time())}.jpg"
        cv2.imwrite(fname, self._last_frame)
        self._status_bar.showMessage(f"Snapshot : {fname}")

    def _pick_model(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choisir un modèle", ".", "Modèles (*.pt)")
        if path:
            self._model_path = path
            self._status_bar.showMessage(f"Modèle : {path}")

    def _on_conf_changed(self, value: int):
        if self._detection_thread:
            self._detection_thread.set_conf(value / 100.0)

    def _on_target_changed(self, value: int):
        self._buzzer_played = False
        self._refresh_counter()

    def _on_class_changed(self, txt: str):
        title = txt if txt != "— Toutes —" else "Toutes classes"
        self._ctrl_panel.set_class_title(title)
        self._buzzer_played = False
        self._refresh_counter()

    def _on_buzzer_toggled(self, enabled: bool):
        self._buzzer_enabled = enabled

    def _reset_counter(self):
        self._buzzer_played = False
        self._ctrl_panel.reset_big_count_style()
        self._status_bar.showMessage("Compteur réinitialisé.")

    # ── Réception des frames ─────────────────────────────────────────────────

    def _on_frame(self, frame: np.ndarray, counts: dict, total: int):
        self._last_frame     = frame
        self._current_counts = counts
        self._total_detected = total

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qt_img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        pix = QPixmap.fromImage(qt_img).scaled(
            self._cam_panel.feed_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self._cam_panel.feed_label.setPixmap(pix)

        if counts:
            self._ctrl_panel.populate_classes(list(counts.keys()))

        self._refresh_counter()

    def _refresh_counter(self):
        counts = self._current_counts
        target = self._ctrl_panel.target_count
        cls    = self._ctrl_panel.selected_class

        if cls and cls in counts:
            current = counts[cls]
        elif cls is None:
            current = self._total_detected
        else:
            current = 0

        if current == target:
            state = "ok"
            msg   = "✅ Objectif atteint !"
            if self._buzzer_enabled and not self._buzzer_played:
                play_buzzer()
                self._buzzer_played = True
        elif current > target:
            state = "over"
            msg   = f"⚠ Excédent : {current - target} de trop"
            self._buzzer_played = False
        else:
            state = ""
            msg   = f"{target - current} restants"
            self._buzzer_played = False

        self._ctrl_panel.update_count(current, target, state, msg, self._total_detected)

    def _on_error(self, msg: str):
        QMessageBox.critical(self, "Erreur", msg)
        self._stop()

    # ── Fermeture ────────────────────────────────────────────────────────────

    def closeEvent(self, event):
        self._stop()
        event.accept()