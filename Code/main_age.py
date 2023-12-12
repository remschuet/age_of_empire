import sys
from PySide6.QtWidgets import QApplication

from GameEngine.game_app import GameApp


def main():
    app = QApplication(sys.argv)
    m = GameApp(app)
    m.window.btn_start.connect(m.btn_start_clicked)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
