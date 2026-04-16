class Palette:
    """Palette Corporate Blue — thème clair professionnel."""

    BG      = "#F8FAFD"   # fond général (bleu-gris très clair)
    SURFACE = "#FFFFFF"   # surfaces, cartes, inputs
    CARD    = "#FFFFFF"   # cartes principales
    BORDER  = "#E2E8F0"   # bordures légères
    ACCENT  = "#1A56DB"   # bleu corporate primaire
    ACCENT2 = "#1E429F"   # bleu corporate foncé (hover, secondaire)
    GREEN   = "#057A55"   # succès (vert sobre)
    AMBER   = "#B45309"   # avertissement (ambre foncé lisible)
    RED     = "#C81E1E"   # erreur / excédent
    TEXT    = "#1E293B"   # texte principal (quasi-noir)
    MUTED   = "#64748B"   # texte secondaire / placeholders


def build_stylesheet(p: Palette = Palette()) -> str:
    """Retourne la feuille de style QSS complète — thème Corporate Blue."""
    return f"""
    QMainWindow, QWidget {{
        background: {p.BG};
        color: {p.TEXT};
        font-family: 'Segoe UI', sans-serif;
        font-size: 13px;
    }}
    QFrame#card {{
        background: {p.CARD};
        border: 1px solid {p.BORDER};
        border-radius: 10px;
    }}
    QLabel#feed {{
        background: {p.SURFACE};
        border: 2px solid {p.BORDER};
        border-radius: 10px;
        color: {p.MUTED};
        font-size: 16px;
    }}
    QLabel#classTitle {{
        color: {p.ACCENT};
        font-size: 15px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
    }}
    QLabel#bigCount {{
        color: {p.TEXT};
        font-size: 96px;
        font-weight: 700;
        line-height: 1;
    }}
    QLabel#bigCount[state="ok"]   {{ color: {p.GREEN}; }}
    QLabel#bigCount[state="over"] {{ color: {p.RED};   }}
    QLabel#statusMsg {{
        color: {p.MUTED};
        font-size: 13px;
    }}
    QLabel#progText {{
        color: {p.ACCENT};
        font-weight: 600;
        font-size: 14px;
    }}
    QLabel#totalLabel {{
        color: {p.ACCENT2};
        font-size: 20px;
        font-weight: 700;
    }}
    QProgressBar {{
        background: {p.BORDER};
        border: 1px solid {p.BORDER};
        border-radius: 8px;
    }}
    QProgressBar::chunk {{
        background: {p.ACCENT};
        border-radius: 8px;
    }}
    QPushButton {{
        background: {p.SURFACE};
        color: {p.TEXT};
        border: 1px solid {p.BORDER};
        border-radius: 7px;
        padding: 6px 14px;
        font-size: 13px;
    }}
    QPushButton:hover    {{ background: #EFF6FF; border-color: {p.ACCENT}; color: {p.ACCENT}; }}
    QPushButton:pressed  {{ background: {p.ACCENT}; color: #FFFFFF; border-color: {p.ACCENT2}; }}
    QPushButton:disabled {{ color: {p.MUTED}; background: {p.BG}; }}
    QComboBox, QSpinBox, QDoubleSpinBox {{
        background: {p.SURFACE};
        border: 1px solid {p.BORDER};
        border-radius: 6px;
        padding: 4px 8px;
        color: {p.TEXT};
    }}
    QComboBox:hover, QSpinBox:hover {{ border-color: {p.ACCENT}; }}
    QComboBox::drop-down {{ border: none; }}
    QSlider::groove:horizontal {{
        background: {p.BORDER};
        height: 4px;
        border-radius: 2px;
    }}
    QSlider::handle:horizontal {{
        background: {p.ACCENT};
        width: 14px; height: 14px;
        margin: -5px 0;
        border-radius: 7px;
    }}
    QSlider::sub-page:horizontal {{
        background: {p.ACCENT};
        border-radius: 2px;
    }}
    QTabWidget::pane {{
        background: {p.CARD};
        border: 1px solid {p.BORDER};
        border-radius: 10px;
    }}
    QTabBar::tab {{
        background: {p.BG};
        color: {p.MUTED};
        border: 1px solid {p.BORDER};
        padding: 6px 14px;
        margin-right: 2px;
        border-top-left-radius: 7px;
        border-top-right-radius: 7px;
    }}
    QTabBar::tab:selected {{ background: {p.CARD}; color: {p.ACCENT}; border-bottom-color: {p.CARD}; }}
    QTabBar::tab:hover    {{ color: {p.ACCENT}; }}
    QListWidget {{
        background: {p.SURFACE};
        border: 1px solid {p.BORDER};
        border-radius: 8px;
        padding: 4px;
    }}
    QListWidget::item           {{ padding: 5px 8px; border-radius: 5px; color: {p.TEXT}; }}
    QListWidget::item:alternate  {{ background: {p.BG}; }}
    QListWidget::item:selected   {{ background: #EFF6FF; color: {p.ACCENT}; }}
    QStatusBar {{ background: {p.SURFACE}; color: {p.MUTED}; font-size: 12px; border-top: 1px solid {p.BORDER}; }}
    QCheckBox::indicator {{
        width: 16px; height: 16px;
        border: 1px solid {p.BORDER};
        border-radius: 4px;
        background: {p.SURFACE};
    }}
    QCheckBox::indicator:checked {{ background: {p.ACCENT}; border-color: {p.ACCENT}; }}
    """