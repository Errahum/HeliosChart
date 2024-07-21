import json
import os
import pandas as pd
from src.ui.ui_handling import move_slider_to_bar


def find_closest_left_doji(df, current_bar_index, slider):
    current_bar_index = int(slider.value() - 1)  # Obtenez l'index actuel du curseur
    doji_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'data_doji.json')
    try:
        with open(doji_file_path, 'r') as file:
            doji_data = json.load(file)
        doji_df = pd.DataFrame(doji_data)

        # Parcourir doji_df de la fin jusqu'au début
        for index, row in doji_df.iloc[::-1].iterrows():
            doji_bar_index = row['bar']
            if doji_bar_index < current_bar_index:
                move_slider_to_bar(slider, doji_bar_index)
                slider.setValue(doji_bar_index + 1)  # Mise à jour de la valeur du curseur
                return
        print("Aucun Doji trouvé à gauche.")
    except Exception as e:
        print(f"Erreur : {e}")


def find_closest_right_doji(df, current_bar_index, slider):
    current_bar_index = int(slider.value() - 1)  # Obtenez l'index actuel du curseur
    doji_file_path = os.path.join(os.path.dirname(__file__), '..', '..' 'data', 'data_doji.json')
    try:
        with open(doji_file_path, 'r') as file:
            doji_data = json.load(file)
        doji_df = pd.DataFrame(doji_data)

        # Parcourir doji_df du début jusqu'à la fin
        for index, row in doji_df.iterrows():
            doji_bar_index = row['bar']
            if doji_bar_index > current_bar_index:
                move_slider_to_bar(slider, doji_bar_index)
                slider.setValue(doji_bar_index + 1)  # Mise à jour de la valeur du curseur
                return
        print("Aucun Doji trouvé à droite.")
    except Exception as e:
        print(f"Erreur : {e}")


def find_doji_patterns(selector_var):
    data_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'data')

    input_file_path = os.path.join(data_folder, f"{selector_var}.json")
    output_file_path = os.path.join(data_folder, 'data_doji.json')

    try:
        with open(input_file_path, 'r') as file:
            data = json.load(file)
        doji_entries = [entry for entry in data['data'] if 'Doji' in entry.get('pattern', '')]
        with open(output_file_path, 'w') as file:
            json.dump(doji_entries, file, indent=4)
        print(f"Doji data saved to '{output_file_path}'")
    except Exception as e:
        print(f"Error processing file: {e}")
