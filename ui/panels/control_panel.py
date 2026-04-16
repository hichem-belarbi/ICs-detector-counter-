from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSpinBox, QComboBox,
    QProgressBar, QFrame, QGridLayout,
    QCheckBox,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor

from ui.styles import Palette


class ControlPanel(QWidget):
    """
    Panneau droit : compteur principal, barre de progression, paramètres.
    """

    target_count_changed = pyqtSignal(int)
    class_changed        = pyqtSignal(str)
    reset_requested      = pyqtSignal()
    buzzer_toggled       = pyqtSignal(bool)

    def __init__(self, palette: Palette = None, parent=None):
        super().__init__(parent)
        self._p = palette or Palette()
        self._build()

    # ── Construction ────────────────────────────────────────────────────────

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self._build_count_card())
        layout.addWidget(self._build_progress_card())
        layout.addWidget(self._build_settings_card(), stretch=1)
        layout.addWidget(self._build_total_card())

    def _build_count_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(20, 18, 20, 18)
        lay.setSpacing(4)

        self.lbl_class_title = QLabel("Aucune classe")
        self.lbl_class_title.setAlignment(Qt.AlignCenter)
        self.lbl_class_title.setObjectName("classTitle")

        self.lbl_big_count = QLabel("0")
        self.lbl_big_count.setAlignment(Qt.AlignCenter)
        self.lbl_big_count.setObjectName("bigCount")

        self.lbl_status = QLabel("En attente…")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.lbl_status.setObjectName("statusMsg")

        lay.addWidget(self.lbl_class_title)
        lay.addWidget(self.lbl_big_count)
        lay.addWidget(self.lbl_status)
        return card

    def _build_progress_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(20, 14, 20, 14)
        lay.setSpacing(8)

        hdr = QHBoxLayout()
        lbl = QLabel("Progression")
        lbl.setObjectName("sectionLabel")
        hdr.addWidget(lbl)
        hdr.addStretch()
        self.lbl_prog_text = QLabel("0 / 10")
        self.lbl_prog_text.setObjectName("progText")
        hdr.addWidget(self.lbl_prog_text)
        lay.addLayout(hdr)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(10)
        lay.addWidget(self.progress_bar)
        return card

    def _build_settings_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(20, 16, 20, 16)
        lay.setSpacing(16)

        # En-tête de section
        header = QLabel("Paramètres")
        header.setObjectName("cardHeader")
        lay.addWidget(header)

        # Séparateur
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setObjectName("divider")
        lay.addWidget(divider)

        # Grille de champs
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setColumnStretch(1, 1)

        lbl_class = QLabel("Classe cible")
        lbl_class.setObjectName("fieldLabel")
        self.class_combo = QComboBox()
        self.class_combo.addItem("— Toutes —")
        self.class_combo.setMinimumHeight(32)
        grid.addWidget(lbl_class,        0, 0)
        grid.addWidget(self.class_combo, 0, 1)

        lbl_qty = QLabel("Quantité cible")
        lbl_qty.setObjectName("fieldLabel")
        self.target_spin = QSpinBox()
        self.target_spin.setRange(1, 9999)
        self.target_spin.setValue(10)
        self.target_spin.setMinimumHeight(32)
        grid.addWidget(lbl_qty,          1, 0)
        grid.addWidget(self.target_spin, 1, 1)

        lbl_buzz = QLabel("Son d'alerte")
        lbl_buzz.setObjectName("fieldLabel")
        self.chk_buzzer = QCheckBox("Activer")
        self.chk_buzzer.setChecked(True)
        grid.addWidget(lbl_buzz,        2, 0)
        grid.addWidget(self.chk_buzzer, 2, 1)

        lay.addLayout(grid)
        lay.addStretch()

        # Bouton reset
        self.btn_reset = QPushButton("Réinitialiser le compteur")
        self.btn_reset.setObjectName("resetBtn")
        self.btn_reset.setMinimumHeight(36)
        lay.addWidget(self.btn_reset)

        # Connexions
        self.target_spin.valueChanged.connect(self.target_count_changed)
        self.class_combo.currentIndexChanged.connect(self._on_class_changed)
        self.chk_buzzer.toggled.connect(self.buzzer_toggled)
        self.btn_reset.clicked.connect(self.reset_requested)

        return card

    def _build_total_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("totalCard")
        tl = QHBoxLayout(card)
        tl.setContentsMargins(20, 14, 20, 14)
        lbl = QLabel("Total détecté")
        lbl.setObjectName("fieldLabel")
        tl.addWidget(lbl)
        tl.addStretch()
        self.lbl_total = QLabel("0")
        self.lbl_total.setObjectName("totalLabel")
        tl.addWidget(self.lbl_total)
        return card

    # ── API publique ─────────────────────────────────────────────────────────

    def update_count(self, current: int, target: int, state: str, msg: str, total: int):
        p = self._p
        self.lbl_big_count.setText(str(current))
        self.lbl_total.setText(str(total))

        pct = min(int(current / target * 100), 100) if target > 0 else 0
        self.progress_bar.setValue(pct)
        self.lbl_prog_text.setText(f"{current} / {target}")
        self.lbl_status.setText(msg)

        self.lbl_big_count.setProperty("state", state)
        self.lbl_big_count.style().unpolish(self.lbl_big_count)
        self.lbl_big_count.style().polish(self.lbl_big_count)

        if state == "ok":
            chunk = f"background: {p.GREEN}; border-radius: 5px;"
        elif state == "over":
            chunk = f"background: {p.RED}; border-radius: 5px;"
        else:
            chunk = f"background: {p.ACCENT}; border-radius: 5px;"
        base = self.progress_bar.styleSheet().split("QProgressBar::chunk")[0]
        self.progress_bar.setStyleSheet(base + f"QProgressBar::chunk {{ {chunk} }}")

    def populate_classes(self, names: list[str]):
        existing = {self.class_combo.itemText(i) for i in range(self.class_combo.count())}
        for name in names:
            if name not in existing:
                self.class_combo.addItem(name)

    def add_log(self, msg: str):
        pass  # log tab removed — kept for API compatibility

    def reset_big_count_style(self):
        self.lbl_big_count.setProperty("state", "")
        self.lbl_big_count.style().unpolish(self.lbl_big_count)
        self.lbl_big_count.style().polish(self.lbl_big_count)

    def set_class_title(self, title: str):
        self.lbl_class_title.setText(title)

    @property
    def target_count(self) -> int:
        return self.target_spin.value()

    @property
    def selected_class(self) -> str | None:
        txt = self.class_combo.currentText()
        return None if txt == "— Toutes —" else txt

    # ── Slot privé ───────────────────────────────────────────────────────────

    def _on_class_changed(self):
        self.class_changed.emit(self.class_combo.currentText())