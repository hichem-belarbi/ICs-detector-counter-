from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSlider, QComboBox, QSizePolicy,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, pyqtSignal

class CameraPanel(QWidget):
    """
    Panneau gauche : flux vidéo + boutons de contrôle
    + slider de confiance + sélecteur de caméra.
    """

    # Signaux émis vers la fenêtre principale
    start_requested    = pyqtSignal()
    pause_requested    = pyqtSignal()
    stop_requested     = pyqtSignal()
    snapshot_requested = pyqtSignal()
    model_requested    = pyqtSignal()
    conf_changed       = pyqtSignal(int)   # valeur 10-95

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build()

    # ── Construction ────────────────────────────────────────────────────────
    
    

    def _btn(self,label: str, icon_path: str) -> QPushButton:
        btn = QPushButton(label)
        btn.setFixedHeight(38)
        icon = QIcon(icon_path)
        if not icon.isNull():
            btn.setIcon(icon)
            btn.setIconSize(QSize(18, 18))
        return btn


    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)

        # Flux vidéo
        self.feed_label = QLabel("Caméra non démarrée")
        self.feed_label.setAlignment(Qt.AlignCenter)
        self.feed_label.setMinimumSize(800, 540)
        self.feed_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.feed_label.setObjectName("feed")
        layout.addWidget(self.feed_label)

        # Boutons caméra
        cam_bar = QHBoxLayout()
        self.btn_start    = self._btn("Démarrer",  "ui/panels/icons/start.png")
        self.btn_pause    = self._btn("Pause",     "ui/panels/icons/pause.png")
        self.btn_stop     = self._btn("Arrêter",   "ui/panels/icons/stop.png")
        self.btn_snapshot = self._btn("Snapshot",  "ui/panels/icons/snapshot.png")
        self.btn_model    = self._btn("Modèle…",   "ui/panels/icons/model.png")

        for btn in (self.btn_start, self.btn_pause, self.btn_stop,
                    self.btn_snapshot, self.btn_model):
            btn.setFixedHeight(38)
            cam_bar.addWidget(btn)

        self.btn_pause.setEnabled(False)
        self.btn_stop.setEnabled(False)
        self.btn_snapshot.setEnabled(False)
        layout.addLayout(cam_bar)

        # Slider de confiance
        conf_row = QHBoxLayout()
        conf_row.addWidget(QLabel("Confiance :"))
        self.conf_slider = QSlider(Qt.Horizontal)
        self.conf_slider.setRange(10, 95)
        self.conf_slider.setValue(50)
        self.conf_value_label = QLabel("0.50")
        self.conf_value_label.setFixedWidth(36)
        conf_row.addWidget(self.conf_slider)
        conf_row.addWidget(self.conf_value_label)
        layout.addLayout(conf_row)

        # Sélecteur de caméra
        cam_sel = QHBoxLayout()
        cam_sel.addWidget(QLabel("Caméra :"))
        self.cam_combo = QComboBox()
        for i in range(4):
            self.cam_combo.addItem(f"Caméra {i}", i)
        cam_sel.addWidget(self.cam_combo)
        cam_sel.addStretch()
        layout.addLayout(cam_sel)

        # Connexions internes
        self.btn_start.clicked.connect(self.start_requested)
        self.btn_pause.clicked.connect(self.pause_requested)
        self.btn_stop.clicked.connect(self.stop_requested)
        self.btn_snapshot.clicked.connect(self.snapshot_requested)
        self.btn_model.clicked.connect(self.model_requested)
        self.conf_slider.valueChanged.connect(self._on_conf_changed)

    # ── Helpers publics ──────────────────────────────────────────────────────

    def set_running(self, running: bool):
        """Met à jour l'état des boutons selon si la détection tourne."""
        self.btn_start.setEnabled(not running)
        self.btn_pause.setEnabled(running)
        self.btn_stop.setEnabled(running)
        self.btn_snapshot.setEnabled(running)

    def set_paused(self, paused: bool):
        if paused:
            self.btn_pause.setText("Reprendre")
            self.btn_pause.setIcon(QIcon("ui/panels/icons/play.png"))
        else:
            self.btn_pause.setText("Pause")
            self.btn_pause.setIcon(QIcon("ui/panels/icons/pause.png"))

    def reset_feed(self):
        from PyQt5.QtGui import QPixmap
        self.feed_label.setText("Caméra arrêtée")
        self.feed_label.setPixmap(QPixmap())

    @property
    def selected_camera(self) -> int:
        return self.cam_combo.currentData()

    @property
    def confidence(self) -> float:
        return self.conf_slider.value() / 100.0

    # ── Slot privé ───────────────────────────────────────────────────────────

    def _on_conf_changed(self, value: int):
        self.conf_value_label.setText(f"{value / 100:.2f}")
        self.conf_changed.emit(value)
