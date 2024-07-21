import sys

from PyQt5.QtWidgets import QApplication

from src.ui.chart_ui import MainApp


def helioschart():
    # Vérifiez si une instance de QApplication existe déjà
    app = QApplication.instance()
    if not app:  # Créez-en une si elle n'existe pas
        app = QApplication(sys.argv)

    mainapp = MainApp()
    mainapp.show()
    app.exec_()


if __name__ == "__main__":
    helioschart()
