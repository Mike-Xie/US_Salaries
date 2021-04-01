import pandas as pd 
from us_states_and_territories import states_and_territories
from debug_tools import dprint


"""
    Pre-processing function to replace $ string values with floats so we can perform arithmetic on the dataframes 
"""
def replace_dollar_with_float(df: pd.DataFrame) -> pd.DataFrame:
    
    if(not type(df) is pd.DataFrame):
        return False

    dprint('df:')
    dprint(df.head())
    

    df = df.apply(lambda x: x.replace('[$,]', '').astype(float) if '$' in x else x)

    return df 

def clean_income_tax_data(income_tax_data_all_states: pd.DataFrame) -> pd.DataFrame:
    df = income_tax_data_all_states.fillna(0)
    return df
