import os
import pandas as pd

def load_and_merge_raw_data(
    raw_data_dir,
    variable_files=None,
    mean_vars=None,
    sum_vars=None,
    time_col="time"
):
    """
    Carga y une los datasets de la carpeta raw_data_dir.
    Toma solo los valores 'mean' para mean_vars y 'sum' para sum_vars.
    El índice será la columna 'time' en formato datetime.
    """
    if variable_files is None:
        variable_files = {
            "temp2m": "temp2m_hourly_2018_2025.csv",
            "vel": "vel_hourly_2018_2025.csv",
            "press": "press_hourly_2018_2025.csv",
            "radinf": "radinf_hourly_2018_2025.csv",
            "HR": "HR_hourly_2018_2025.csv",
            "pp": "pp_hourly_2018_2025.csv",
            "dir": "dir_hourly_2018_2025.csv"
        }
    if mean_vars is None:
        mean_vars = ["temp2m", "vel", "press", "radinf", "HR", "dir"]
    if sum_vars is None:
        sum_vars = ["pp"]

    dfs = []
    for var, fname in variable_files.items():
        fpath = os.path.join(raw_data_dir, fname)
        if not os.path.exists(fpath):
            raise FileNotFoundError(f"No se encontró el archivo: {fpath}")

        # Lee el archivo con encabezado multinivel y el índice en la columna 0
        df = pd.read_csv(fpath, header=[0, 1], index_col=0)

        # El primer índice es "time" como texto, lo eliminamos
        df = df[df.index != time_col]

        # Selecciona la columna adecuada usando solo el nivel de la estadística
        if var in mean_vars:
            stat = "mean"
        elif var in sum_vars:
            stat = "sum"
        else:
            raise ValueError(f"Variable {var} no está en mean_vars ni sum_vars.")

        try:
            # Tomar la columna con nivel 1 = stat (ignora el nombre del nivel 0)
            col = df.xs(stat, level=1, axis=1).iloc[:, 0]
        except KeyError:
            raise KeyError(
                f"No se encontró la columna '{stat}' en {fname}. "
                f"Columnas disponibles: {df.columns.tolist()}"
            )

        serie = col.rename(var)
        serie.index = pd.to_datetime(serie.index)
        dfs.append(serie)

    merged_df = pd.concat(dfs, axis=1)
    return merged_df

# Ejemplo de uso:
if __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(__file__))
    raw_dir = os.path.join(project_root, "data", "raw")
    processed_dir = os.path.join(project_root, "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)
    df = load_and_merge_raw_data(raw_dir)
    print(df.head())
    # Guarda el DataFrame unido en processed
    output_path = os.path.join(processed_dir, "merged_hourly_2018_2025.csv")
    df.to_csv(output_path)
    print(f"Archivo guardado en: {output_path}")
