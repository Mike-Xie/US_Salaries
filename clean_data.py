import pandas as pd 

"""
    Pre-processing function to replace $ value strings with floats so we can perform arithmetic on dataframes 
"""
def replace_dollar_with_float(df: pd.DataFrame) -> pd.DataFrame:
    
    df = df.set_index('State').apply(lambda x: (x.str.replace('[$,]', '').astype(float)))

    return df 