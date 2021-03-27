import pandas as pd
import os.path
import csv
from debug_tools import *

# fully qualified file_name (i.e. with extension)
def write_df(df: pd.DataFrame, file_name: str) -> None:
    df.to_csv(file_name, index=False)

def read_df(file_name: str) -> pd.DataFrame:
    return pd.read_csv(file_name)

def file_exists(file_name: str) -> bool:
    return os.path.isfile(file_name)

# TODO: connect to AWS as credentialed app

def read_csv_to_list(file_name: str) -> list:
    lines = []
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            lines+=row
    if(len(lines)>0):
        return lines

def write_list_to_csv(data: list, file_name: str):
    data_str = ','.join(data)
    with open(file_name, 'w') as csvfile:
        csvfile.write(data_str)