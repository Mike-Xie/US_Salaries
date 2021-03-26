import pandas as pd

# fully qualified file_name (i.e. with extension)
def write_df(df: pd.DataFrame, file_name: str) -> None:
    df.to_csv(file_name, index=False)

def read_df(file_name: str) -> pd.DataFrame:
    return pd.read_csv(file_name)


# TODO: connect to AWS as credentialed app
