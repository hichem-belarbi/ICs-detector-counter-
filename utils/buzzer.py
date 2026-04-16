import time


def play_buzzer():
    """Joue 3 bips (Windows) ou un beep terminal en fallback."""
    try:
        import winsound
        for _ in range(3):
            winsound.Beep(1000, 200)
            time.sleep(0.05)
    except Exception:
        print("\a")  # beep ASCII fallback
