import pandas as pd

# fully qualified file_name (i.e. with extension)
def write_df(df: pd.DataFrame, file_name: str) -> None:
    pd.to_csv(df, str)

def read_df(file_name: str) -> pd.DataFrame:
    return pd.from_csv(str)


# TODO: connect to AWS as credentialed app
