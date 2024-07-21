import os
import pandas as pd
import matplotlib.pyplot as plt
import json


def convert_json_data(json_data):
    converted_data = []
    for date, times in json_data.items():
        for time, entry in times.items():
            direction = "Long" if 'LB0' in entry else "Short"
            pattern = entry.get('Pattern', '')  # Récupère le pattern s'il existe
            data_entry = {
                'time': f"{date} {time}",
                'high': float(entry.get('LA1') or entry.get('SA1')),
                'open_price': float(entry.get('LB0') or entry.get('SA0')),
                'close': float(entry.get('LA0') or entry.get('SB0')),
                'low': float(entry.get('LB1') or entry.get('SB1')),
                'direction': direction,
                'pattern': pattern  # Ajoute le pattern à l'entrée
            }
            converted_data.append(data_entry)

    df = pd.DataFrame(converted_data)
    if 'time' in df.columns:
        df['time'] = pd.to_datetime(df['time'])
    return df


def store_and_display_used_data(df, selector_var):
    if df is not None:
        data_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        json_file_path = os.path.join(data_folder, f"{selector_var}.json")
        print(f"dropdown_handler {json_file_path}")

        if not os.path.exists(json_file_path):
            try:
                df_json_ready = df.copy()
                # Convertir les colonnes datetime ou object en string
                for col in df_json_ready.columns:
                    if pd.api.types.is_datetime64_any_dtype(df_json_ready[col]) or pd.api.types.is_object_dtype(
                            df_json_ready[col]):
                        df_json_ready[col] = df_json_ready[col].astype(str)

                used_data = {
                    "columns": df_json_ready.columns.tolist(),
                    "data_types": df_json_ready.dtypes.astype(str).to_dict(),
                    "data": df_json_ready.to_dict(orient='records'),
                    "shape": df_json_ready.shape
                }

                with open(json_file_path, 'w') as file:
                    json.dump(used_data, file, indent=4)
                print(f"Data saved to '{json_file_path}'")
            except Exception as e:
                print(f"Error saving data: {e}")
                return -1  # Retourne un code d'erreur
        else:
            print(f"File '{json_file_path}' already exists. No need to save again.")
    else:
        print("No DataFrame created, no data to save.")
        return -2  # Retourne un code d'erreur différent pour indiquer un autre type d'erreur

    return 0  # Retourne 0 si aucune erreur ne s'est produite


def fetch_data(file_path, selector_var):
    if not file_path:
        return None, -3  # Retourne un code d'erreur si le chemin du fichier n'est pas fourni

    try:
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()

        if file_extension != '.json':
            print("Unsupported file format.")
            return None, -4  # Retourne un code d'erreur pour un format de fichier non pris en charge

        with open(file_path, 'r') as file:
            json_data = json.load(file)

        if 'data' in json_data and isinstance(json_data['data'], list):
            df = pd.DataFrame(json_data['data'])
        else:
            df = convert_json_data(json_data)

        if 'time' in df.columns:
            df['time'] = pd.to_datetime(df['time'])

        df['bar'] = df.index

        error_code = store_and_display_used_data(df, selector_var)
        if error_code != 0:
            return None, error_code  # Retourne un code d'erreur si la sauvegarde échoue

        print("DataFrame loaded successfully.")
        print(df.head())
        return df, 0  # Retourne 0 si aucune erreur ne s'est produite

    except Exception as e:
        print(f"Error loading data: {e}")
        return None, -5  # Retourne un code d'erreur pour une erreur de chargement


def plot_candles(df_view, fig, ax, selector_var):
    if ax is None or df_view.empty:
        return
    ax.clear()
    ax.set_title(f"{selector_var} daily")
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)
    time_mapping = df_view['time'].dt.strftime('%H:%M').to_dict()
    ax.xaxis.set_major_locator(plt.MultipleLocator(base=3))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(
        lambda x, pos: time_mapping.get(int(round(x)), '')
    ))
    if 'close' in df_view.columns and 'open_price' in df_view.columns:
        colors = ['green' if close >= open_price else 'red' for close, open_price in
                  zip(df_view['close'], df_view['open_price'])]
    elif 'direction' in df_view.columns:
        colors = ['green' if direction == "Long" else 'red' for direction in df_view['direction']]
    else:
        colors = []
    ax.bar(
        df_view['bar'],
        df_view['close'] - df_view['open_price'],
        bottom=df_view['open_price'],
        color=colors,
        width=0.8
    )
    ax.vlines(
        df_view['bar'],
        df_view['low'],
        df_view['high'],
        color=colors
    )
    fig.canvas.draw()


def get_display_range(slider, bars_to_display):
    end = int(slider.value())
    start = max(0, end - bars_to_display)
    return start, end
