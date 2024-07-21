from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMenu, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from src.utils.doji import find_closest_left_doji, find_closest_right_doji


class CustomInfoPopup(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setGeometry(100, 100, 300, 150)
        self.setWindowTitle("Chart tools")
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setFocusPolicy(Qt.NoFocus)

        self.parent = parent
        self.selected_tool = ""

        popup_frame = QWidget(self)
        popup_layout = QVBoxLayout(popup_frame)

        self.outil_label = QLabel("Outil", popup_frame)
        popup_layout.addWidget(self.outil_label)

        selection_outil = QPushButton("Sélection d'outil", popup_frame)
        popup_layout.addWidget(selection_outil)

        tool_menu = QMenu(popup_frame)
        tool_menu.addAction("Doji")
        tool_menu.triggered.connect(self.handle_menu_selection)
        selection_outil.setMenu(tool_menu)

        button_layout = QHBoxLayout()
        self.button_left = QPushButton("Gauche", popup_frame)
        self.button_right = QPushButton("Droite", popup_frame)
        self.button_left.setEnabled(False)
        self.button_right.setEnabled(False)
        self.button_left.clicked.connect(self.on_left_button_clicked)
        self.button_right.clicked.connect(self.on_right_button_clicked)
        button_layout.addWidget(self.button_left)
        button_layout.addWidget(self.button_right)
        popup_layout.addLayout(button_layout)

        self.setCentralWidget(popup_frame)
        # self.move(parent.pos().x() + parent.width(), parent.pos().y())
        self.move(1080, 0)

    def handle_menu_selection(self, action):
        self.selected_tool = action.text()
        self.button_left.setEnabled(self.selected_tool == "Doji")
        self.button_right.setEnabled(self.selected_tool == "Doji")
        self.outil_label.setText(f"Outil: {self.selected_tool}")

    def on_left_button_clicked(self):
        if self.parent and self.selected_tool == "Doji":
            current_bar_index = int(self.parent.slider.value() - 1)
            error_code = find_closest_left_doji(self.parent.df, current_bar_index, self.parent.slider)
            if error_code != 0:
                print(f"Erreur lors de la recherche du Doji le plus proche à gauche: Code d'erreur {error_code}")

    def on_right_button_clicked(self):
        if self.parent and self.selected_tool == "Doji":
            current_bar_index = int(self.parent.slider.value() - 1)
            error_code = find_closest_right_doji(self.parent.df, current_bar_index, self.parent.slider)
            if error_code != 0:
                print(f"Erreur lors de la recherche du Doji le plus proche à droite: Code d'erreur {error_code}")
