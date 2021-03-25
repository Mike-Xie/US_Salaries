import pandas as pd 

us_state_abbrev = {
    'Alabama': 'AL','Alaska': 'AK','American Samoa': 'AS','Arizona': 'AZ','Arkansas': 'AR','California': 'CA','Colorado': 'CO','Connecticut': 'CT','Delaware': 'DE','District of Columbia': 'DC','Florida': 'FL','Georgia': 'GA','Guam': 'GU','Hawaii': 'HI','Idaho': 'ID','Illinois': 'IL','Indiana': 'IN','Iowa': 'IA','Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA','Maine': 'ME','Maryland': 'MD','Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS','Missouri': 'MO','Montana': 'MT','Nebraska': 'NE','Nevada': 'NV','New Hampshire': 'NH','New Jersey': 'NJ','New Mexico': 'NM','New York': 'NY','North Carolina': 'NC','North Dakota': 'ND','Northern Mariana Islands':'MP','Ohio': 'OH','Oklahoma': 'OK','Oregon': 'OR','Pennsylvania': 'PA','Puerto Rico': 'PR','Rhode Island': 'RI','South Carolina': 'SC','South Dakota': 'SD','Tennessee': 'TN','Texas': 'TX','Utah': 'UT','Vermont': 'VT','Virgin Islands': 'VI','Virginia': 'VA','Washington': 'WA','West Virginia': 'WV','Wisconsin': 'WI','Wyoming': 'WY'
}

"""
    Pre-processing function to replace $ string values with floats so we can perform arithmetic on the dataframes 
"""
def replace_dollar_with_float(df: pd.DataFrame) -> pd.DataFrame:
    
    df = df.set_index('State').apply(lambda x: (x.str.replace('[$,]', '').astype(float)))

    return df 

def engineer_features(base_salary_table: pd.DataFrame, ppp_table: pd.DataFrame) -> pd.DataFrame:

    # pre-process 
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


    index = adjusted_salary_table.index.map(us_state_abbrev)
    adjusted_salary_table['state initial'] = index 
    # adjusted_salary_table.to_csv('salaries.csv')
    return adjusted_salary_table