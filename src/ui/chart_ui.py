import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QLabel, QSlider, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from src.core.data_handling import fetch_data
from src.utils.doji import find_doji_patterns
from src.utils.popup_handling import InfoPopup
from src.utils.popup_outil import CustomInfoPopup
from src.utils.raccourci import key_press_event
from src.ui.ui_handling import center_window, make_plot, load_initial_data, show_bar_time, slider_update, \
    save_json, select_file


class MainApp(QMainWindow):
    def __init__(self):
        self.popups = []  # Ajout d'une liste pour garder une trace des popups ouverts

        super().__init__()
        self.setWindowTitle("Matplotlib Plot with PyQt")
        self.setGeometry(100, 100, 1800, 1000)

        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)

        self.config_file = os.path.join(os.path.dirname(__file__), '..', '..','last_selector_var.txt')
        self.selector_var = self.load_last_selector_var()

        self.selector = QComboBox()
        self.selector.addItems(["Oil", "Gold", "Coal"])
        self.selector.setCurrentIndex(self.selector.findText(self.selector_var))
        self.selector.currentIndexChanged.connect(self.selector_changed)
        layout.addWidget(self.selector)

        self.load_button = QPushButton("Update", self)
        self.load_button.clicked.connect(self.load_new_data)
        self.load_button.setFixedSize(100, 30)
        layout.addWidget(self.load_button)

        self.selector_info = QLabel(f"Selected: {self.selector_var}")
        layout.addWidget(self.selector_info)

        self.fig, self.ax = make_plot()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        self.slider = QSlider()
        self.slider.setOrientation(1)
        layout.addWidget(self.slider)

        self.df = None
        self.bars_to_display = 60

        self.time_info_label = QLabel("Selected Bar Time: N/A")
        layout.addWidget(self.time_info_label)

        self.load_initial_data()
        self.slider.valueChanged.connect(self.slider_changed)

        self.canvas.mpl_connect('button_press_event', self.handle_canvas_click)
        self.show_custom_popup()
        center_window(self)

        # Doji gauche
        find_doji_patterns(self.selector_var)

    def reset_variables(self):
        # Réinitialisez ici toutes les variables nécessaires
        self.df = None
        # Ajoutez ici toute autre variable qui doit être réinitialisée

    def load_new_data(self):
        try:
            file_path = select_file(self)
            if file_path:
                self.df, error_code = fetch_data(file_path, self.selector_var)
                if error_code == 0 and self.df is not None and not self.df.empty:
                    save_json(self.df, os.path.join(os.path.dirname(__file__), '..', '..' 'data'), self.selector_var)
                    self.load_initial_data()
                else:
                    print(f"Erreur lors du chargement des données: Code d'erreur {error_code}")
            return 0  # Aucune erreur
        except Exception as e:
            print(f"Erreur lors de la mise à jour des données: {e}")
            return -1  # Code d'erreur pour un échec de mise à jour des données

    def load_initial_data(self):
        try:
            self.df = load_initial_data(self, self.fig, self.ax, self.slider, self.bars_to_display, self.selector_var,
                                        self.selector_info, self.time_info_label)
            if self.df is None:
                return -2  # Code d'erreur si aucune donnée n'est chargée
            return 0  # Aucune erreur
        except Exception as e:
            print(f"Erreur lors du chargement des données initiales: {e}")
            return -3  # Code d'erreur pour un échec de chargement des données initiales

    def load_last_selector_var(self):
        try:
            with open(self.config_file, 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            return "Oil"

    def save_last_selector_var(self):
        with open(self.config_file, 'w') as file:
            file.write(self.selector_var)

    def selector_changed(self):
        self.selector_var = self.selector.currentText()
        self.save_last_selector_var()
        self.load_initial_data()

    def slider_changed(self):
        slider_update(self.df, self.fig, self.ax, self.slider, self.bars_to_display, self.selector_var,
                      self.selector_info)
        show_bar_time(self.df, self.slider, self.time_info_label)

    def handle_canvas_click(self, event):
        try:
            if event.inaxes == self.ax and event.xdata is not None and self.df is not None:
                index = int(round(event.xdata))
                if 0 <= index < len(self.df):
                    info_popup = InfoPopup(self)
                    info_popup.update_content(self.df.iloc[index])
                    info_popup.show()
                    self.popups.append(info_popup)  # Ajoutez le popup à la liste
            return 0  # Aucune erreur
        except Exception as e:
            print(f"Erreur lors de la gestion du clic sur le canvas: {e}")
            return -4  # Code d'erreur pour un échec de la gestion du clic sur le canvas

    def closeEvent(self, event):
        # Fermez et supprimez tous les popups
        for popup in self.popups:
            if popup:
                popup.close()
                popup.deleteLater()

        # Nettoyez les ressources de la figure Matplotlib
        if self.fig:
            self.fig.clear()

        # Nettoyez et supprimez le canvas Matplotlib
        if self.canvas:
            self.canvas.close()
            self.canvas.deleteLater()

        # Nettoyez et réinitialisez d'autres variables si nécessaire
        self.df = None
        # Réinitialisez ici d'autres variables si nécessaire

        # Fermez la fenêtre principale
        super().closeEvent(event)

        # Assurez-vous que l'application se termine correctement
        event.accept()  # Acceptez l'événement de fermeture
        QApplication.quit()

    def keyPressEvent(self, event):
        key_press_event(self, event)

    def show_custom_popup(self):
        self.custom_popup = CustomInfoPopup(self)
        self.custom_popup.show()
        self.popups.append(self.custom_popup)  # Ajoutez le popup à la liste des popups ouverts
