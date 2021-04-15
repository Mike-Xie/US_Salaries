import pandas as pd 
from debug_tools import dprint

"""
    Pre-processing function to replace string values like "$32,443" with float 32443 so we can perform arithmetic on the dataframes in engineer_features
"""
def replace_dollar_with_float(df: pd.DataFrame) -> pd.DataFrame:
    
    if(not type(df) is pd.DataFrame):
        return False
    df = df.applymap(lambda x: float(x.replace('$', '').replace(',', '')) if '$' in x else x)
    return df 
"""
    Replaces empty dataframe cell values with 0 so we can perform arithmetic on the dataframes in engineer_features
"""
def clean_income_tax_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.fillna(0)
    return df
