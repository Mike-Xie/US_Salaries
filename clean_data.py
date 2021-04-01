import pandas as pd 
from us_states_and_territories import states_and_territories


"""
    Pre-processing function to replace $ string values with floats so we can perform arithmetic on the dataframes 
"""
def replace_dollar_with_float(df: pd.DataFrame) -> pd.DataFrame:
    
    if(not type(df) is pd.DataFrame):
        return False

    df = df.apply(lambda x: (x.str.replace('[$,]', '').astype(float)))

    return df 

def engineer_features(base_salary_table: pd.DataFrame, ppp_table: pd.DataFrame, income_tax_table: pd.DataFrame) -> pd.DataFrame:

    # pre-process
    base_salary_table = base_salary_table.set_index('State')
    ppp_table = ppp_table.set_index('State')
    base_salary_table = replace_dollar_with_float(base_salary_table)
    ppp_table = replace_dollar_with_float(ppp_table)
    adjusted_salary_table = base_salary_table.join(ppp_table)

    adjusted_salary_table['Adjusted Annual Salary'] = adjusted_salary_table['Annual Salary'] * adjusted_salary_table['Value of a Dollar']
    adjusted_salary_table['Monthly Salary Minus Rent'] = adjusted_salary_table['Monthly Pay'] - adjusted_salary_table['Median Monthly Rent']
    adjusted_salary_table['DS All Jobs Multiple'] = adjusted_salary_table['Annual Salary'] / adjusted_salary_table['Annual Mean Wage (All Occupations)']
    adjusted_salary_table['Median Yearly Rent'] = adjusted_salary_table['Median Monthly Rent'] * 12
    adjusted_salary_table['Yearly Salary Minus Rent'] = adjusted_salary_table['Annual Salary'] - adjusted_salary_table['Median Yearly Rent']
    adjusted_salary_table['Adjusted Yearly Salary Minus Rent'] = adjusted_salary_table['Yearly Salary Minus Rent'] * adjusted_salary_table['Value of a Dollar']

    # Mean Wage Money left over after Expenses
    adjusted_salary_table['Median Salary Minus Rent'] = adjusted_salary_table['Annual Mean Wage (All Occupations)'] - adjusted_salary_table['Median Yearly Rent']
    adjusted_salary_table['Adjusted Median Salary Minus Rent'] = adjusted_salary_table['Median Salary Minus Rent'] * adjusted_salary_table['Value of a Dollar']

    # state initial column necessary for plotly geometry arguments & merging with tax API returned values
    adjusted_salary_table['State Initial'] = adjusted_salary_table.index.map(states_and_territories)
    adjusted_salary_table.merge(income_tax_table, left_on=['State Initial'], right_on=['State Initial'], how='right', inplace=True)
    
    return adjusted_salary_table

def clean_income_tax_data(income_tax_data_all_states: pd.DataFrame) -> pd.DataFrame:
    df = income_tax_data_all_states.fillna(0)
    return df
