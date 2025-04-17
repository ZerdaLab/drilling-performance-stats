import os
import pandas as pd
import lasio


def read_formation_data():
    """
    Reads the first CSV file found in the 'formation_data' folder.
    """
    folder_path = "formation_data"
    
    # Find the first CSV file in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            return pd.read_csv(file_path)
    
    # Raise an error if no CSV file is found
    raise FileNotFoundError(f"No CSV file found in the folder: {folder_path}")


def read_dh_las():
    """
    Reads the first LAS file found in the 'downhole_data' folder.
    """
    folder_path = "downhole_data"
    
    # Find the first LAS file in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".las"):
            file_path = os.path.join(folder_path, file_name)
            dh_las = lasio.read(file_path)
            dh_df = dh_las.df()
            dh_df.reset_index(inplace=True)
            dh_df['TIME'] = pd.to_datetime(dh_df['TIME'], unit='s')
            return dh_df
    
    # Raise an error if no LAS file is found
    raise FileNotFoundError(f"No LAS file found in the folder: {folder_path}")


def read_runs_data():
    """
    Reads the first CSV file found in the 'bit_data' folder.
    """
    folder_path = "bit_run_data"
    
    # Find the first CSV file in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            runs_df = pd.read_csv(file_path)
            # Remove leading and trailing spaces from column names
            runs_df.columns = runs_df.columns.str.strip()
            return runs_df
    
    # Raise an error if no CSV file is found
    raise FileNotFoundError(f"No CSV file found in the folder: {folder_path}")

