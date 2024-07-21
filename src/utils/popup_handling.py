from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPlainTextEdit, QPushButton, QApplication
from PyQt5.QtCore import Qt


class InfoPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle("Information")
        self.setGeometry(100, 100, 300, 150)
        self.setWindowModality(Qt.NonModal)
        self.layout = QVBoxLayout(self)

        self.info_text = QPlainTextEdit("")
        self.info_text.setReadOnly(True)
        self.layout.addWidget(self.info_text)

        copier_button = QPushButton("Copy Text")
        copier_button.clicked.connect(self.copy_text)
        self.layout.addWidget(copier_button)

        # Set the position of the dialog to the top-left corner
        # self.move(0, 0)

    def update_content(self, row):
        info_text = (
            f"High: {row['high']}\n"
            f"Open: {row['open_price']}\n"
            f"Close: {row['close']}\n"
            f"Low: {row['low']}\n"
            f"Time of Bar: {row['time'].strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Pattern: {row.get('pattern', 'N/A')}\n"
            f"Volume: {row.get('Volume', 'N/A')}"
        )
        self.info_text.setPlainText(info_text)

    def copy_text(self):
        text_to_copy = self.info_text.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(text_to_copy)


def show_info_popup(index, df, parent):
    try:
        row = df.iloc[index]
        popup = InfoPopup(parent)
        popup.update_content(row)
        popup.exec_()
    except IndexError as e:
        print(f"Erreur d'index : {e}")
        return -1  # Code d'erreur pour un problème d'index
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return -2  # Code d'erreur pour d'autres exceptions
    return 0  # Aucune erreur



def on_bar_click(event, df, parent, ax):
    if event.inaxes == ax:
        if event.xdata is not None:
            try:
                index = int(round(event.xdata))
                if 0 <= index < len(df):
                    error_code = show_info_popup(index, df, parent)
                    if error_code != 0:
                        print(f"Erreur lors de l'affichage du popup : Code d'erreur {error_code}")
            except ValueError as e:
                print(f"Erreur de valeur : {e}")
            except Exception as e:
                print(f"Erreur inattendue : {e}")

