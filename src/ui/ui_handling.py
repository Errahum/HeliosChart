import json
import locale
import os

from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QFileDialog
from matplotlib.figure import Figure

from src.core.data_handling import plot_candles, fetch_data

locale.setlocale(locale.LC_TIME, 'french')


def save_json(df, file_path, selector_var):
    try:
        df_json_ready = df.copy()
        df_json_ready['time'] = df_json_ready['time'].astype(str)  # Convertir datetime en string
        data_to_save = {
            "columns": df_json_ready.columns.tolist(),
            "data_types": df_json_ready.dtypes.astype(str).to_dict(),
            "data": df_json_ready.to_dict(orient='records')
        }
        with open(os.path.join(file_path, f"{selector_var}.json"), 'w') as file:
            json.dump(data_to_save, file, indent=4)
        print(f"Fichier '{selector_var}.json' enregistré avec succès.")
        return 0  # Aucune erreur
    except Exception as e:
        print(f"Erreur lors de l'enregistrement du fichier JSON : {e}")
        return -1  # Code d'erreur pour un échec d'enregistrement


def load_initial_data(parent, fig, ax, slider, bars_to_display, selector_var, selector_info, time_info_label):
    # Chemin du dossier du projet (un niveau au-dessus du dossier contenant ce script)
    project_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    # Chemin du dossier 'data' dans le dossier du projet
    data_folder = os.path.join(project_folder, 'data')
    file_path = os.path.join(data_folder, f"{selector_var}.json")

    # Initialisation de df et error_code
    df, error_code = None, 0

    if os.path.exists(file_path):
        df, error_code = fetch_data(file_path, selector_var)
    else:
        selected_file_path = select_file(parent)
        if selected_file_path:
            df, error_code = fetch_data(selected_file_path, selector_var)
            if df is not None and not df.empty and error_code == 0:
                save_json(df, data_folder, selector_var)

    # Vérification du code d'erreur
    if error_code != 0:
        print(f"Une erreur s'est produite lors du chargement des données: Code d'erreur {error_code}")
        return

    if df is not None and not df.empty:
        last_bar_index = df.shape[0] - 1
        slider.setMaximum(last_bar_index)
        slider.setValue(last_bar_index)
        update_source(df, fig, ax, slider, bars_to_display, selector_var, selector_info)
        show_bar_time(df, slider, time_info_label)
    else:
        print("Aucune donnée valide chargée.")

    return df


def get_display_range(slider, bars_to_display):
    end = int(slider.value())
    start = max(0, end - bars_to_display)
    return start, end


def update_source(df, fig, ax, slider, bars_to_display, selector_var, selector_info):
    if df is not None:
        start, end = get_display_range(slider, bars_to_display)
        df_view = df.iloc[start:end]
        plot_candles(df_view, fig, ax, selector_var)
        selector_info.setText(f"Selected: {selector_var}")


def select_file(parent):
    file_path, _ = QFileDialog.getOpenFileName(parent, "Select a file", "", "JSON files (*.json)")
    return file_path


def make_plot():
    fig = Figure(figsize=(19.2, 10.8))
    ax = fig.add_subplot(111)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    return fig, ax


def slider_update(df, fig, ax, slider, bars_to_display, selector_var, selector_info):
    update_source(df, fig, ax, slider, bars_to_display, selector_var, selector_info)


def dropdown_handler(df, selector_var, parent, fig, ax, slider, selector_info):
    data_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
    file_path = os.path.join(data_folder, f"{selector_var}.json")

    print(f"dropdown_handler {file_path}")

    if os.path.exists(file_path):
        df = fetch_data(file_path, selector_var)
    else:
        selected_file_path = select_file(parent)
        if selected_file_path:
            df = fetch_data(selected_file_path, selector_var)
            if df is not None and not df.empty:
                error_code = save_json(df, data_folder, selector_var)
                if error_code != 0:
                    print("Erreur lors de l'enregistrement des données.")
                    return None

    if df is not None and not df.empty:
        last_bar_index = df.shape[0] - 1
        slider.setMaximum(last_bar_index)
        slider.setValue(last_bar_index)
        update_source(df, fig, ax, slider, 1, selector_var, selector_info)

    return df



def move_slider(df, fig, ax, slider, bars_to_display, selector_var, selector_info, direction):
    if slider is not None:
        current_val = slider.value()
        new_val = max(current_val + direction, slider.minimum()) if direction < 0 else min(current_val + direction,
                                                                                           slider.maximum())
        slider.setValue(new_val)
        slider_update(df, fig, ax, slider, bars_to_display, selector_var, selector_info)


def move_slider_to_bar(slider, bar_index):
    if slider is not None:
        slider.setValue(bar_index)


def show_bar_time(df, slider, time_info_label):
    if df is not None and not df.empty:
        bar_index = int(slider.value() - 1)
        if 0 <= bar_index < len(df):
            bar_time = df.iloc[bar_index]['time'].strftime('%A %d %B %Y %Hh')
            time_info_label.setText(f"Selected Bar Time: {bar_time}")
        else:
            time_info_label.setText("Selected Bar Time: N/A")
    else:
        time_info_label.setText("Selected Bar Time: N/A")


def on_closing(popup, app, root, plt):
    try:
        if popup:
            popup.close()
            popup.deleteLater()
        plt.close('all')
        app.quit()
        if root:
            root.destroy()
    except Exception as e:
        print(f"Erreur lors de la fermeture : {e}")


def center_window(window):
    framegm = window.frameGeometry()
    centerpoint = QDesktopWidget().availableGeometry().center()
    framegm.moveCenter(centerpoint)
    window.move(framegm.topLeft())
