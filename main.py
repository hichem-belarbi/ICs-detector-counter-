
import sys
from ui import ComponentCounter
from PyQt5.QtWidgets import QApplication



def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = ComponentCounter()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
