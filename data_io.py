import pandas as pd
import os.path

# fully qualified file_name (i.e. with extension)
def write_df(df: pd.DataFrame, file_name: str) -> None:
    df.to_csv(file_name, index=False)

def read_df(file_name: str) -> pd.DataFrame:
    return pd.read_csv(file_name)

def file_exists(file_name: str) -> bool:
    return os.path.isfile(ppp_name)

# TODO: connect to AWS as credentialed app
